"""Candidate lines and the clean-win rate of the best one (Ian's change of
2026-09-30, relayed by the Overseer; out/design.md, "The reading").

A line is a policy with responses, not a sequence of inputs: which
Pokemon leads, which answer comes in when each of the trainer's Pokemon
appears, when to switch out of a losing exchange, when to spend a turn on
a status or setup move, and otherwise the strongest attack. `decide`
applies a line to whatever state a run has reached. `search` draws X such
lines around the greedy defaults, screens each on a few random runs,
re-tests the best on fresh runs, and reports that rate with how the best
screening rate grew with X (the convergence check).

Runs use RunDice: Ian's luck rules inside them (a secondary status against
the player always lands, at most one critical hit on the player), real
dice for the rest. The trainer plays its own AI with real dice.
"""
import random

from . import fightsim as fs
from . import perfectline as pl

RUN_TURN_CAP = 80
SWITCH_RULES = ("losing", "losing", "hp", "never")


class Line:
    __slots__ = ("lead", "answers", "switch_rule", "hp_floor", "setup_turns", "setup_full",
                 "use_status", "seed")

    def __init__(self, lead, answers, switch_rule="losing", hp_floor=0.4, setup_turns=3,
                 setup_full=True, use_status=True, seed=0):
        self.lead = lead
        self.answers = answers            # {foe key: team index or None}
        self.switch_rule = switch_rule    # losing: leave a losing exchange for a winning one
        self.hp_floor = hp_floor          # hp: leave a losing exchange only below this share
        self.setup_turns = setup_turns    # a status or setup move needs this many safe turns
        self.setup_full = setup_full      # setup only at full HP
        self.use_status = use_status
        self.seed = seed

    def describe(self, st, team):
        ans = ", ".join(f"{st['pokemon'][k]['species']}->{st['pokemon'][team[i]]['species']}"
                        for k, i in self.answers.items() if i is not None)
        return (f"lead {st['pokemon'][team[self.lead]]['species']}; answers {ans or 'none'}; "
                f"switch {self.switch_rule}{f' below {self.hp_floor:.1f}' if self.switch_rule == 'hp' else ''}; "
                f"setup at {self.setup_turns}+ safe turns{' at full HP' if self.setup_full else ''}"
                f"{'' if self.use_status else '; no status moves'}")


# ---- applying a line ---------------------------------------------------------------------------------

def crit_possible(b):
    d = getattr(b, "dice", None)
    if isinstance(d, pl.RunDice):
        return not d.crit_used
    return b.luck_spent * pl.CRIT_RATE[0] >= pl.BUDGET - 1e-12


def exchange(b, me=None, foe=None):
    """As perfectline.exchange, for any pair, with the crit allowed while
    the run has not had one."""
    me = me or b.p.cur()
    foe = foe or b.b.cur()
    mine = max((pl.dmg_low(b, me, foe, mv) for mv in me.moves
                if mv.damaging() and me.pp.get(mv.name, 1) > 0 and mv.effect not in fs.SELF_KO
                and (not me.choice or mv.name == me.choice)), default=0)
    theirs = [(pl.dmg_top(b, foe, me, mv), pl.damage_of(b, foe, me, mv, True, True) or 0)
              for mv in foe.moves if mv.damaging() and foe.pp.get(mv.name, 1) > 0]
    plain = max((t[0] for t in theirs), default=0)
    crit = max((t[1] for t in theirs), default=0) if crit_possible(b) else plain
    t_me = -(-foe.hp // mine) if mine > 0 else 99
    if plain <= 0:
        t_foe = 99
    else:
        left = me.hp - crit
        t_foe = 1 if left <= 0 else 1 + -(-left // plain)
    sm, sf = b.speed(me), b.speed(foe)
    if b.trick_room:
        sm, sf = -sm, -sf
    first = sm > sf
    return (t_me < t_foe or (t_me == t_foe and first)), t_me, t_foe, plain, crit


def expected_damage(b, me, foe, mv):
    """A move's damage a turn as a player reckons it: the middle roll times
    its accuracy, nothing for a move that could faint the user."""
    if not mv.damaging() or me.pp.get(mv.name, 1) <= 0 or mv.effect in fs.SELF_KO:
        return 0.0
    if mv.effect in fs.RECOIL and me.ability != "Rock Head":
        top = pl.dmg_top(b, me, foe, mv)
        if int(min(top, foe.hp) * fs.RECOIL[mv.effect]) >= me.hp:
            return 0.0
    d = pl.damage_of(b, me, foe, mv, False, False, roll=7) or 0
    acc = 1.0 if mv.acc == 0 else min(1.0, mv.acc / 100)
    if mv.effect in fs.TWO_TURN or mv.effect == "RECHARGE_AFTER":
        d /= 2
    return d * acc


def usable(b, me, foe, mv):
    if me.pp.get(mv.name, 1) <= 0 or (me.taunt and mv.cat == "Status"):
        return False
    if me.choice and mv.name != me.choice:
        return False
    from tools.oxide.balance import fightai
    f = fightai.figure(b, me, foe, mv)
    return fightai.basic(b, me, foe, mv, f) > -8


def best_switch(b, me, foe):
    """The bench member that wins its exchange after taking the foe's
    strongest hit on the way in, soonest; None when there is none."""
    best = None
    for i, m in enumerate(b.p.mons):
        if i == b.p.active or not m.alive():
            continue
        hit = max((pl.dmg_top(b, foe, m, mv) for mv in foe.moves if mv.damaging()), default=0)
        if crit_possible(b):
            hit = max(hit, max((pl.damage_of(b, foe, m, mv, True, True) or 0
                                for mv in foe.moves if mv.damaging()), default=0))
        if hit >= m.hp:
            continue
        saved = m.hp
        m.hp -= hit
        try:
            win, t_me, t_foe, _p, _c = exchange(b, m, foe)
        finally:
            m.hp = saved
        if win:
            key = (t_me, -(m.hp - hit) / m.maxhp)
            if best is None or key < best[0]:
                best = (key, i)
    return best[1] if best else None


def decide(b, line):
    """('move', Move) or ('switch', index) for the player under this line."""
    me, foe = b.p.cur(), b.b.cur()
    if me.lock:
        return "move", me.lock[0]
    if me.charging is not None:
        return "move", me.charging
    if me.recharge:
        return "move", me.moves[0]
    moves = [mv for mv in me.moves if usable(b, me, foe, mv)]
    attacks = [mv for mv in moves if mv.damaging()]
    can_switch = not me.bound and b.p.bench()
    win, t_me, t_foe, _plain, _crit = exchange(b)
    first = (b.speed(me) > b.speed(foe)) if not b.trick_room else (b.speed(me) < b.speed(foe))
    # A knockout this turn that the foe cannot answer first.
    for mv in sorted(attacks, key=lambda m: -m.pri):
        if (mv.acc == 0 or mv.acc >= 100) and pl.dmg_low(b, me, foe, mv) >= foe.hp \
                and (mv.pri > 0 or first or t_foe > 1):
            return "move", mv
    # The answer to this foe comes in when it appears.
    if can_switch and foe.turns_in == 0:
        ans = line.answers.get(foe.key)
        if ans is not None and ans != b.p.active and b.p.mons[ans].alive():
            return "switch", ans
    # Leaving a losing exchange.
    if can_switch and not win and line.switch_rule != "never":
        if line.switch_rule == "losing" or me.hp / me.maxhp < line.hp_floor:
            idx = best_switch(b, me, foe)
            if idx is not None:
                return "switch", idx
    # A status or setup move when there is time for it.
    safe = t_foe - (0 if first else 1)
    if line.use_status and safe >= line.setup_turns:
        for mv in moves:
            if mv.damaging():
                continue
            e = mv.effect
            if e in fs.STATUS_OF and fs.can_status(b, foe, fs.STATUS_OF[e]) and t_me >= 2:
                return "move", mv
            if e in fs.SELF_STAGES and (me.hp == me.maxhp or not line.setup_full):
                stat = "atk" if any(m.cat == "Physical" for m in attacks) else "spa"
                if me.stages.get(stat, 0) < 2 and fs.SELF_STAGES[e].get(stat, 0) > 0:
                    return "move", mv
            if e in fs.HEAL_HALF and me.hp * 2 < me.maxhp:
                return "move", mv
    if attacks:
        return "move", max(attacks, key=lambda m: expected_damage(b, me, foe, m))
    if moves:
        return "move", moves[0]
    if can_switch:
        return "switch", next(i for i, m in enumerate(b.p.mons) if i != b.p.active and m.alive())
    return "move", me.moves[0]


# ---- runs ----------------------------------------------------------------------------------------------

def play_run(st, team, boss_keys, flags, line, rng, one_crit=True, to_end=False):
    """One random run under the line: (clean win, won, turns, deaths). It
    stops at the player's first death unless `to_end`, which plays on to a
    win or a wipe; the dice are the same up to that death either way, so a
    run's clean result does not depend on it."""
    b = pl.make_battle(st, team, boss_keys, flags, line.lead)
    b.dice = pl.RunDice(rng, one_crit)
    b.rng = rng
    dead = lambda: sum(1 for m in b.p.mons if not m.alive())
    while b.turn < RUN_TURN_CAP:
        if not b.p.alive():
            return False, False, b.turn, dead()
        if pl.player_lost(b) and not to_end:
            return False, False, b.turn, dead()
        if not b.b.alive():
            return dead() == 0, True, b.turn, dead()
        pl.play_turn(b, decide(b, line), rng, one_crit)
    return False, False, b.turn, dead()


def clean_rate(st, team, boss_keys, flags, line, runs, rng, one_crit=True):
    clean = 0
    for _ in range(runs):
        c, _w, _t, _d = play_run(st, team, boss_keys, flags, line, rng, one_crit)
        clean += c
    return clean / runs


def line_stats(st, team, boss_keys, flags, line, runs, rng, one_crit=True):
    """(clean-win rate, mean deaths, wipe chance) over runs played to the
    end (Ian, 2026-09-30: the hardest fights, where no line wins cleanly,
    still separate by what the best line costs)."""
    clean = deaths = wipes = 0
    for _ in range(runs):
        c, w, _t, d = play_run(st, team, boss_keys, flags, line, rng, one_crit, to_end=True)
        clean += c
        deaths += d
        wipes += not w and d == len(team)
    return clean / runs, deaths / runs, wipes / runs


# ---- candidate lines ------------------------------------------------------------------------------------

def greedy_line(st, team, boss_keys, flags, rng, jitter=0.0):
    """The default line: the lead and the answers by the exchange reading,
    switching out of losing exchanges, setup at three safe turns. With
    jitter, each choice is perturbed at that rate."""
    b = pl.make_battle(st, team, boss_keys, flags, 0)
    bm = {k: m for k, m in zip(boss_keys, b.b.mons)}
    scores = {}
    for i, m in enumerate(b.p.mons):
        for k in boss_keys:
            win, t_me, t_foe, _p, _c = exchange(b, m, bm[k])
            scores[(i, k)] = (1 if win else 0, t_foe - t_me, -t_me)
    lead_key = boss_keys[0]
    order = sorted(range(len(team)), key=lambda i: scores[(i, lead_key)], reverse=True)
    lead = order[0] if rng.random() >= jitter else rng.randrange(len(team))
    answers = {}
    for k in boss_keys:
        best = max(range(len(team)), key=lambda i: scores[(i, k)])
        if scores[(best, k)][0] == 0:
            best = None
        if rng.random() < jitter:
            best = rng.choice([None] + list(range(len(team))))
        answers[k] = best
    line = Line(lead, answers)
    if rng.random() < jitter:
        line.switch_rule = rng.choice(SWITCH_RULES)
    if rng.random() < jitter:
        line.hp_floor = rng.uniform(0.2, 0.7)
    if rng.random() < jitter:
        line.setup_turns = rng.choice([2, 3, 4, 5])
    if rng.random() < jitter:
        line.setup_full = rng.random() < 0.5
    if rng.random() < jitter:
        line.use_status = rng.random() < 0.7
    return line


def search(st, team, boss_keys, flags, candidates=50, screen_runs=20, keep=3, confirm_runs=300,
           seed=0, one_crit=True):
    """The best line's clean-win rate for this six: {"rate", "screen"
    (the best screening rate after 10, 20, ... candidates), "line",
    "candidates", "runs"}."""
    rng = random.Random(seed)
    lines = [greedy_line(st, team, boss_keys, flags, rng, 0.0)]
    while len(lines) < candidates:
        lines.append(greedy_line(st, team, boss_keys, flags, rng, rng.choice([0.15, 0.3, 0.5, 0.8])))
    scored = []
    curve = {}
    for i, line in enumerate(lines):
        r = clean_rate(st, team, boss_keys, flags, line, screen_runs, random.Random(seed * 7919 + i), one_crit)
        scored.append((r, i, line))
        if (i + 1) % 10 == 0 or i + 1 == len(lines):
            curve[i + 1] = max(x[0] for x in scored)
        if r >= 1.0 and i >= 4:
            break                                  # a line that never failed screening
    curve[len(scored)] = max(x[0] for x in scored)
    scored.sort(key=lambda x: (-x[0], x[1]))
    best = None
    for r, i, line in scored[:keep]:
        rate, deaths, wipe = line_stats(st, team, boss_keys, flags, line, confirm_runs,
                                        random.Random(seed * 104729 + i), one_crit)
        if best is None or (rate, -deaths) > (best[0], -best[3]):
            best = (rate, r, line, deaths, wipe)
    rate, screened, line, deaths, wipe = best
    return {"rate": round(rate, 3), "deaths": round(deaths, 3), "wipe": round(wipe, 3),
            "screened": round(screened, 3), "screen": curve,
            "line": line.describe(st, team), "candidates": len(scored),
            "runs": len(scored) * screen_runs + min(keep, len(scored)) * confirm_runs}

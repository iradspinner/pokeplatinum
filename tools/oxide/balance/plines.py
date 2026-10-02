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
# A search still climbing when its candidates run out may take up to this many
# times its base budget (convergence per six).
EXTEND_TIMES = 3
SWITCH_RULES = ("losing", "losing", "hp", "never")


class Line:
    __slots__ = ("lead", "answers", "switch_rule", "hp_floor", "setup_turns", "setup_full",
                 "use_status", "seed", "bait_lock", "free_pivot", "stall", "reserved",
                 "screens", "hazards", "pairs", "def_setup", "foe_drop", "sleep_open")

    def __init__(self, lead, answers, switch_rule="losing", hp_floor=0.4, setup_turns=3,
                 setup_full=True, use_status=True, seed=0, bait_lock=False, free_pivot=False,
                 stall=0, reserved=None, screens=False, hazards=False, pairs=None,
                 def_setup=False, foe_drop=False, sleep_open=False):
        self.lead = lead
        self.answers = answers            # {foe key: team index or None}
        self.switch_rule = switch_rule    # losing: leave a losing exchange for a winning one
        self.hp_floor = hp_floor          # hp: leave a losing exchange only below this share
        self.setup_turns = setup_turns    # a status or setup move needs this many safe turns
        self.setup_full = setup_full      # setup only at full HP
        self.use_status = use_status
        self.seed = seed
        # Ian's own plans (2026-09-30), each a rule with a parameter:
        self.bait_lock = bait_lock        # once a foe is Choice-locked, switch to what the lock cannot hurt
        self.free_pivot = free_pivot      # leave a losing exchange through a Pokemon immune to the foe's hit
        self.stall = stall                # stall a foe's timed effect with this many turns or fewer left
        self.reserved = reserved or {}    # {team index: foe key} saved for that later foe
        self.screens = screens            # Reflect or Light Screen against the foe's kind of hit
        self.hazards = hazards            # rocks, spikes or toxic spikes with foes still to come
        self.pairs = pairs or {}          # {foe key: (chipper, finisher)}: two on one foe
        self.def_setup = def_setup        # raise Defense against a physical foe (Simple doubles it)
        self.foe_drop = foe_drop          # lower the foe's attacking stat, or its accuracy
        self.sleep_open = sleep_open      # open with sleep against the foe's strongest

    def describe(self, st, team):
        ans = ", ".join(f"{st['pokemon'][k]['species']}->{st['pokemon'][team[i]]['species']}"
                        for k, i in self.answers.items() if i is not None)
        return (f"lead {st['pokemon'][team[self.lead]]['species']}; answers {ans or 'none'}; "
                f"switch {self.switch_rule}{f' below {self.hp_floor:.1f}' if self.switch_rule == 'hp' else ''}; "
                f"setup at {self.setup_turns}+ safe turns{' at full HP' if self.setup_full else ''}"
                f"{'' if self.use_status else '; no status moves'}"
                f"{'; bait locks' if self.bait_lock else ''}{'; free pivots' if self.free_pivot else ''}"
                f"{f'; stall timed effects at {self.stall} turns' if self.stall else ''}"
                + "".join(f"; save {st['pokemon'][team[i]]['species']} for {st['pokemon'][k]['species']}"
                          for i, k in self.reserved.items())
                + f"{'; screens' if self.screens else ''}{'; hazards' if self.hazards else ''}"
                + f"{'; Defense setup' if self.def_setup else ''}{'; stat drops' if self.foe_drop else ''}"
                + f"{'; sleep opener' if self.sleep_open else ''}"
                + "".join(f"; {st['pokemon'][team[a]]['species']} then {st['pokemon'][team[c]]['species']} "
                          f"on {st['pokemon'][k]['species']}" for k, (a, c) in self.pairs.items()))


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


def _held(line, i, foe):
    """Whether team member i is saved for a later foe other than this one."""
    k = line.reserved.get(i)
    return k is not None and k != foe.key


def _free_against(b, foe, mv_types):
    """The bench members the foe's moves of these types do nothing to."""
    return [i for i, m in enumerate(b.p.mons)
            if i != b.p.active and m.alive()
            and all(fs.effectiveness(b.st["chart"], t, m.types) == 0 for t in mv_types)]


def _timed_left(b):
    """Turns left on the foe side's screens and tailwind, and Trick Room; the
    fewest of those running, or None."""
    side = b.b
    left = [v for v in side.screens.values() if v] + ([side.tailwind] if side.tailwind else [])
    if b.trick_room and b.trick_room < 999:
        left.append(b.trick_room)
    return min(left) if left else None


def _strongest(b):
    """The foe side's strongest Pokemon: the highest level, then the most HP."""
    return max(b.b.mons, key=lambda m: (m.level, m.maxhp)).key


def _why(b, rule, act):
    """The action, with the rule that chose it kept on the battle for a
    traced run to print (plstep3)."""
    b.why = rule
    return act


def decide(b, line):
    """('move', Move) or ('switch', index) for the player under this line."""
    me, foe = b.p.cur(), b.b.cur()
    if me.lock:
        return _why(b, "locked into a move", ("move", me.lock[0]))
    if me.charging is not None:
        return _why(b, "charging", ("move", me.charging))
    if me.recharge:
        return _why(b, "recharging", ("move", me.moves[0]))
    moves = [mv for mv in me.moves if usable(b, me, foe, mv)]
    attacks = [mv for mv in moves if mv.damaging()]
    can_switch = not me.bound and fs.can_switch(me) and b.p.bench()
    win, t_me, t_foe, _plain, _crit = exchange(b)
    first = (b.speed(me) > b.speed(foe)) if not b.trick_room else (b.speed(me) < b.speed(foe))
    # A knockout this turn that the foe cannot answer first.
    for mv in sorted(attacks, key=lambda m: -m.pri):
        if (mv.acc == 0 or mv.acc >= 100) and pl.dmg_low(b, me, foe, mv) >= foe.hp \
                and (mv.pri > 0 or first or t_foe > 1):
            return _why(b, "a knockout it cannot answer first", ("move", mv))
    # Baiting a lock: the foe is locked into one Choice move; switch to a
    # Pokemon that move cannot touch, so its turns are spent for nothing.
    if line.bait_lock and can_switch and foe.choice:
        locked = fs.move(foe.choice)
        if locked is not None and locked.damaging() and pl.dmg_top(b, foe, me, locked) > 0:
            free = [i for i in _free_against(b, foe, [locked.type]) if not _held(line, i, foe)]
            if free:
                return _why(b, "baiting a Choice lock", ("switch", free[0]))
    # The answer to this foe comes in when it appears; with no single
    # answer, the first of a pair (the chipper).
    if can_switch and foe.turns_in == 0:
        ans = line.answers.get(foe.key)
        if ans is None and foe.key in line.pairs:
            ans = line.pairs[foe.key][0]
        if ans is not None and ans != b.p.active and b.p.mons[ans].alive():
            return _why(b, "this foe's answer comes in", ("switch", ans))
    # A pair: the chipper leaves for the finisher while it can still take
    # the foe's hardest hit, crit included.
    pair = line.pairs.get(foe.key)
    if pair and can_switch and b.p.active == pair[0] and b.p.mons[pair[1]].alive():
        _w, _tm, _tf, _plain, crit_hit = exchange(b)
        if me.hp <= crit_hit * 2:
            return _why(b, "the pair's chipper hands over", ("switch", pair[1]))
    # Screens: Reflect against a foe whose hits are physical, Light Screen
    # against special, while ours is down and this Pokemon lives the turn.
    if line.screens and t_foe >= 2:
        cats = [mv.cat for mv in foe.moves if mv.damaging()]
        if cats:
            want = "Reflect" if cats.count("Physical") >= cats.count("Special") else "Light Screen"
            eff = "SET_REFLECT" if want == "Reflect" else "SET_LIGHT_SCREEN"
            if not b.p.screens[want]:
                mv = next((m for m in moves if m.effect == eff), None)
                if mv is not None:
                    return _why(b, "a screen against its kind of hit", ("move", mv))
    phys = sum(1 for mv in foe.moves if mv.damaging() and mv.cat == "Physical")
    spec = sum(1 for mv in foe.moves if mv.damaging() and mv.cat == "Special")
    # Sleep as the opening against the foe's strongest Pokemon.
    if line.sleep_open and t_foe >= 2 and foe.status is None and foe.key == _strongest(b):
        mv = next((m for m in moves if m.effect == "STATUS_SLEEP" and fs.can_status(b, foe, "slp")), None)
        if mv is not None:
            return _why(b, "sleep against its strongest", ("move", mv))
    # Defense setup against a physical foe, to +4 (Simple doubles each use).
    if line.def_setup and phys and phys >= spec and t_foe >= 2 and me.stages["def"] < 4:
        mv = next((m for m in moves if m.effect in fs.SELF_STAGES
                   and fs.SELF_STAGES[m.effect].get("def", 0) > 0), None)
        if mv is not None:
            return _why(b, "Defense setup", ("move", mv))
    # A drop on the foe's attacking stat, else its accuracy, to -2.
    if line.foe_drop and t_foe >= 2 and t_me >= 2 and (phys or spec):
        for stat in ("atk" if phys >= spec else "spa", "acc"):
            if foe.stages[stat] <= -2:
                continue
            mv = next((m for m in moves if m.effect in fs.FOE_STAGES
                       and fs.FOE_STAGES[m.effect].get(stat, 0) < 0), None)
            if mv is not None:
                return _why(b, "a stat drop on the foe", ("move", mv))
    # Hazards, with two or more of the foe's Pokemon still to come.
    if line.hazards and t_foe >= 2 and sum(1 for m in b.b.mons if m.alive()) >= 3:
        hz = b.b.hazards
        for mv in moves:
            if (mv.effect == "STEALTH_ROCK" and not hz["rocks"]) or \
                    (mv.effect == "SET_SPIKES" and hz["spikes"] < 3) or \
                    (mv.effect == "TOXIC_SPIKES" and hz["tspikes"] < 2):
                return _why(b, "hazards", ("move", mv))
    # Stalling a timed effect: with none of our hits a knockout, wait out the
    # foe's screens, tailwind or Trick Room behind Protect when it is nearly
    # over, or through a free switch.
    left = _timed_left(b) if line.stall else None
    if left is not None and left <= line.stall and not win:
        guard = next((mv for mv in moves if mv.effect == "PROTECT" and not me.protect_streak), None) \
            if hasattr(me, "protect_streak") else next((mv for mv in moves if mv.effect == "PROTECT"), None)
        if guard is not None:
            return _why(b, "Protect while a timed effect runs out", ("move", guard))
        if can_switch:
            hits = [mv.type for mv in foe.moves if mv.damaging()]
            free = [i for i in _free_against(b, foe, hits) if not _held(line, i, foe)]
            if free:
                return _why(b, "a free switch while a timed effect runs out", ("switch", free[0]))
    # Leaving a losing exchange.
    if can_switch and not win and line.switch_rule != "never":
        if line.switch_rule == "losing" or me.hp / me.maxhp < line.hp_floor:
            idx = best_switch(b, me, foe)
            if idx is not None and _held(line, idx, foe):
                idx = None
            if idx is None and line.free_pivot:
                # A free pivot: through a Pokemon the foe's hardest hit on us
                # cannot touch, to choose again next turn.
                hard = max((mv for mv in foe.moves if mv.damaging()),
                           key=lambda mv: pl.dmg_top(b, foe, me, mv), default=None)
                if hard is not None:
                    free = [i for i in _free_against(b, foe, [hard.type]) if not _held(line, i, foe)]
                    if free:
                        return _why(b, "a free pivot out of a losing exchange", ("switch", free[0]))
            if idx is not None:
                return _why(b, "leaving a losing exchange", ("switch", idx))
    # A status or setup move when there is time for it.
    safe = t_foe - (0 if first else 1)
    if line.use_status and safe >= line.setup_turns:
        for mv in moves:
            if mv.damaging():
                continue
            e = mv.effect
            if e in fs.STATUS_OF and fs.can_status(b, foe, fs.STATUS_OF[e]) and t_me >= 2:
                return _why(b, "a status move with time for it", ("move", mv))
            if e in fs.SELF_STAGES and (me.hp == me.maxhp or not line.setup_full):
                stat = "atk" if any(m.cat == "Physical" for m in attacks) else "spa"
                if me.stages.get(stat, 0) < 2 and fs.SELF_STAGES[e].get(stat, 0) > 0:
                    return _why(b, "setup with time for it", ("move", mv))
            if e in fs.HEAL_HALF and me.hp * 2 < me.maxhp:
                return _why(b, "healing below half", ("move", mv))
    if attacks:
        return _why(b, "the strongest attack", ("move", max(attacks, key=lambda m: expected_damage(b, me, foe, m))))
    if moves:
        return _why(b, "its only usable move", ("move", moves[0]))
    if can_switch:
        return _why(b, "no usable move, so a switch", ("switch", next(i for i, m in enumerate(b.p.mons) if i != b.p.active and m.alive())))
    return _why(b, "nothing usable", ("move", me.moves[0]))


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

def best_pair(b, foe):
    """(chipper, finisher) for a foe no single member beats: the chipper
    hits until the foe's next hit could knock it out, the finisher comes
    in taking one hit, and together their damage must cover the foe's HP.
    None when no pair does."""
    best = None
    for i, a in enumerate(b.p.mons):
        _w, _tm, tf_a, _p, _c = exchange(b, a, foe)
        dmg_a = max((pl.dmg_low(b, a, foe, mv) for mv in a.moves if mv.damaging()), default=0)
        chip = dmg_a * max(0, tf_a - 1)
        for j, c in enumerate(b.p.mons):
            if j == i:
                continue
            _w2, _tm2, tf_c, _p2, _c2 = exchange(b, c, foe)
            dmg_c = max((pl.dmg_low(b, c, foe, mv) for mv in c.moves if mv.damaging()), default=0)
            total = chip + dmg_c * max(0, tf_c - 1)
            if total >= foe.hp and (best is None or total > best[0]):
                best = (total, (i, j))
    return best[1] if best else None


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
    pairs = {}
    for k in boss_keys:
        if answers[k] is not None:
            continue
        pair = best_pair(b, bm[k])
        if pair is not None:
            pairs[k] = pair
    line = Line(lead, answers, screens=True, hazards=True, pairs=pairs,
                def_setup=True, foe_drop=True, sleep_open=True)
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
    if rng.random() < jitter:
        line.def_setup = rng.random() < 0.7
    if rng.random() < jitter:
        line.foe_drop = rng.random() < 0.6
    if rng.random() < jitter:
        line.sleep_open = rng.random() < 0.7
    if rng.random() < jitter:
        line.screens = rng.random() < 0.8
    if rng.random() < jitter:
        line.hazards = rng.random() < 0.7
    if rng.random() < jitter and line.pairs:
        line.pairs.pop(rng.choice(sorted(line.pairs)))
    if rng.random() < jitter:
        line.bait_lock = rng.random() < 0.7
    if rng.random() < jitter:
        line.free_pivot = rng.random() < 0.7
    if rng.random() < jitter:
        line.stall = rng.choice([0, 1, 2, 3])
    if rng.random() < jitter:
        # Save the answer to one of the later foes for it.
        later = [k for k in boss_keys[1:] if answers.get(k) is not None]
        if later:
            k = rng.choice(later)
            line.reserved = {answers[k]: k}
    return line


def search(st, team, boss_keys, flags, candidates=50, screen_runs=20, keep=3, confirm_runs=300,
           seed=0, one_crit=True, keep_line=False):
    """The best line's clean-win rate for this six: {"rate", "screen"
    (the best screening rate after 10, 20, ... candidates), "line",
    "candidates", "runs"}, and with `keep_line` the Line itself under
    "policy", for replaying it (plstep3)."""
    rng = random.Random(seed)
    scored = []
    curve = {}
    budget, stopped = candidates, False
    # Candidates are drawn and screened one at a time. When the budget is
    # spent and the best rate was last raised in its final quarter, the
    # search is still climbing: it takes half as many again, up to
    # EXTEND_TIMES the base, and records the budget it ended at.
    while not stopped:
        i = len(scored)
        if i >= budget:
            best_at = max(scored, key=lambda x: (x[0], -x[1]))[1] + 1
            if best_at > 0.75 * budget and budget < candidates * EXTEND_TIMES:
                budget = min(candidates * EXTEND_TIMES, budget + max(1, candidates // 2))
                continue
            break
        line = greedy_line(st, team, boss_keys, flags, rng,
                           0.0 if i == 0 else rng.choice([0.15, 0.3, 0.5, 0.8]))
        r = clean_rate(st, team, boss_keys, flags, line, screen_runs, random.Random(seed * 7919 + i), one_crit)
        scored.append((r, i, line))
        if (i + 1) % 10 == 0:
            curve[i + 1] = max(x[0] for x in scored)
        if r >= 1.0 and i >= 4:
            stopped = True                         # a line that never failed screening
    curve[len(scored)] = max(x[0] for x in scored)
    converged = stopped or budget < candidates * EXTEND_TIMES or \
        max(scored, key=lambda x: (x[0], -x[1]))[1] + 1 <= 0.75 * budget
    scored.sort(key=lambda x: (-x[0], x[1]))
    best = None
    for r, i, line in scored[:keep]:
        rate, deaths, wipe = line_stats(st, team, boss_keys, flags, line, confirm_runs,
                                        random.Random(seed * 104729 + i), one_crit)
        if best is None or (rate, -deaths) > (best[0], -best[3]):
            best = (rate, r, line, deaths, wipe)
    rate, screened, line, deaths, wipe = best
    out = {"rate": round(rate, 3), "deaths": round(deaths, 3), "wipe": round(wipe, 3),
           "screened": round(screened, 3), "screen": curve,
           "line": line.describe(st, team), "candidates": len(scored), "converged": converged,
           "runs": len(scored) * screen_runs + min(keep, len(scored)) * confirm_runs}
    if keep_line:
        out["policy"] = line
    return out

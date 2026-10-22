"""The team search: a boss's six and moves chosen by the scorer itself (Ian,
2026-10-02; the plan in docs/oxide/trainer-scoring-handoff.md, "The team
search: plan and costs").

1. Screen, with no simulated fights. Every box member's whole move pool is
   prepared against the boss, so the damage calculator's rows give each
   member's expected damage on each enemy and back, with speed. Each member
   gets four moves picked against this fight, and every six is scored by how
   well it answers every enemy (a member that needs fewer hits to knock an
   enemy out than the enemy needs for it, with who moves first), with the
   least overlap. The top sixes, kept apart from one another, go on.
2. Labels. The play-out planner labels the screen's top five sixes and five
   drawn at random from the box (a tenth of a round, budget 64; the spread
   round from the network's own play helped once and hurt twice, at
   Gardenia and at Mars 1 at 19, so it is left out), and two networks train
   from scratch on everything but this fight's old labels plus these.
3. Race, on the network planner, by Ian's member ratings: sixes are drawn by
   member weights, each read on a few fights, and the weights move toward
   the members of the best sixes (the cross-entropy method); then the best
   full sixes race by halving, which settles pairs that work only together.
4. Finalists: two or three sixes, 75 fights at real odds and 25 very unlucky.
5. The play-out check: the play-out planner reads every finalist on 25
   fights, and the best by Ian's order goes on. The network erred both
   ways in the first test (too kind at Roark, too harsh at Gardenia), so
   its race gives a shortlist, not a verdict.
6. The loop (improve): the enemies that caused the best six's faints pick
   the members that answer them by the screen's margins, sixes built from
   those are read on the same check, and the best is kept, up to three
   rounds.

search() runs all five on one box; plteam_test (the hand run's boxes) and
plgoal2 (goal 2's fights) call it.

A six's score in the race is Ian's order made one number: its win share
first, its faints second (a win outweighs any number of faints the race can
see, since each fight's faints count a tenth of a win).

    PYTHONPATH=. python3 -m tools.oxide.balance.plteam_test   # the first test
"""
import itertools
import json
import math
import os
import random
import subprocess
import zlib

from . import plthreads  # noqa: F401  (one numpy thread per process, before numpy loads)
import numpy as np  # noqa: E402

from . import fightsim as fs, pldata, plfeat, plplan, plscore, pool  # noqa: E402

ROOT = os.path.expanduser("~/oxide-trials/scorer-stage2")
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
MOVES = None


def move_names():
    global MOVES
    if MOVES is None:
        MOVES = pool._move_names()
    return MOVES


# ---- a box member's moves -------------------------------------------------------------------------

def mon_data(sp):
    """A species' data as the tree has it; with OXIDE_LEARNSETS naming a file
    of other level-up lists ({species: [[level, move], ...]}, such as a
    learnset proposal's), its list there instead, the rest unchanged."""
    with open(os.path.join(REPO, "res/pokemon", sp[len("SPECIES_"):].lower(), "data.json")) as fh:
        d = json.load(fh)
    other = _other_learnsets()
    if sp in other:
        d["learnset"] = dict(d.get("learnset") or {}, by_level=[list(e) for e in other[sp]])
    return d


_OTHER = {}


def _other_learnsets():
    path = os.environ.get("OXIDE_LEARNSETS")
    if not path:
        return {}
    if path not in _OTHER:
        with open(path) as fh:
            _OTHER[path] = json.load(fh)
    return _OTHER[path]


def species_name(sp):
    """A species constant as the calculator spells it."""
    blob = fs.calc.blob()
    n = sp[len("SPECIES_"):].replace("_", " ").title().replace(" ", "-")
    if n in blob["poks"] or n.replace("-", "") in blob["poks"]:
        return n if n in blob["poks"] else n.replace("-", "")
    # Regional forms and punctuated names (Ninetales-Alola, Mr. Rime), which
    # the calculator fails on under the plain spelling.
    from ..encounters import canon
    alt = canon.showdown_name(sp)
    return alt if alt in blob["poks"] else n.replace("-", "")


# Level evolutions that also ask something the member is or has: its
# personality (Wurmple: the coin's parity stands for it), its gender, or how
# its Attack compares with its Defense (with equal IVs and a neutral nature,
# as its base stats compare).
_LEVEL_IF = {
    "EVO_LEVEL_PID_LOW": lambda d, gender, coin: coin % 2 == 0,
    "EVO_LEVEL_PID_HIGH": lambda d, gender, coin: coin % 2 == 1,
    "EVO_LEVEL_FEMALE": lambda d, gender, coin: gender == "F",
    "EVO_LEVEL_MALE": lambda d, gender, coin: gender == "M",
    "EVO_LEVEL_ATK_GT_DEF": lambda d, gender, coin: d["base_stats"]["attack"] > d["base_stats"]["defense"],
    "EVO_LEVEL_ATK_LT_DEF": lambda d, gender, coin: d["base_stats"]["attack"] < d["base_stats"]["defense"],
    "EVO_LEVEL_ATK_EQ_DEF": lambda d, gender, coin: d["base_stats"]["attack"] == d["base_stats"]["defense"],
    "EVO_LEVEL_NINJASK": lambda d, gender, coin: True,
}


def chain(sp, caught, cap, holds=None, magnetic=False, places=(), gender=None, coin=None):
    """[(species, from level)] as a member levels from `caught` to `cap`:
    level evolutions (each delayed to its hold, if any), those that ask its
    personality, gender or stats too, evolving by knowing a move once the
    move is learned, and by a place (the magnetic field, the Moss and Ice
    Rocks: `places` names those the run has reached, as place_maps does);
    stones, held items, trades, friendship and Shedinja are not taken. Where
    several evolutions are open (Eevee's), the last listed is taken, or with
    a `coin` the coin's pick of them, the same coin always the same pick."""
    holds = holds or {}
    places = set(places) | ({"LEVEL_MAGNETIC_FIELD"} if magnetic else set())
    path, cur, lvl = [(sp, caught)], sp, caught
    while True:
        open_ = []
        d = mon_data(cur)
        known = {mv for l, mv in d["learnset"]["by_level"] if l <= cap}
        for e in d.get("evolutions") or []:
            kind, target = e[0], e[-1]
            if kind == "EVO_LEVEL" and isinstance(e[1], int):
                at = max(e[1], holds.get(cur, 0), lvl)
                if at <= cap:
                    open_.append((target, at))
            elif kind in _LEVEL_IF and isinstance(e[1], int) and _LEVEL_IF[kind](d, gender, coin or 0):
                at = max(e[1], holds.get(cur, 0), lvl)
                if at <= cap:
                    open_.append((target, at))
            elif kind == "EVO_LEVEL_KNOW_MOVE" and e[1] in known:
                at = max(lvl, next(l for l, mv in d["learnset"]["by_level"] if mv == e[1]))
                if at <= cap:
                    open_.append((target, at))
            elif kind.startswith("EVO_LEVEL_") and kind[len("EVO_"):] in places:
                open_.append((target, lvl))
        if not open_:
            return path
        nxt = open_[-1] if coin is None else open_[coin % len(open_)]
        cur, lvl = nxt
        path.append(nxt)


def move_pool(sp, caught, cap, holds=None, magnetic=False, known=None, places=(), gender=None, coin=None):
    """(final species, its move pool as the calculator names them): the
    capture rule's moves, the last four by the catch level (or `known`, the
    moves a record already has), and every level-up move learned after it up
    to the cap, along its evolutions (chain's, with its places, gender and
    coin)."""
    names = move_names()
    path = chain(sp, caught, cap, holds, magnetic, places, gender, coin)
    by_name = {v: k for k, v in names.items()}
    first = ([by_name[m] for m in known if m in by_name] if known is not None else
             [mv for l, mv in mon_data(sp)["learnset"]["by_level"] if l <= caught][-4:])
    later = []
    for k, (s, frm) in enumerate(path):
        to = path[k + 1][1] if k + 1 < len(path) else cap
        later += [mv for l, mv in mon_data(s)["learnset"]["by_level"] if caught < l <= cap and frm <= l <= to]
    return path[-1][0], [names[m] for m in dict.fromkeys(first + later) if m in names]


def record(sp, level, nature, ability, ivs, moves, label=None, **extra):
    """A box member as the simulator reads it; `extra` carries its gender
    where the box records one (else the simulator rolls it from the
    record)."""
    iv = {k: ivs for k in ("hp", "at", "df", "sp", "sa", "sd")}
    return dict({"constant": sp, "species": species_name(sp), "how": "plan", "level": level, "nature": nature,
                 "ivs": iv, "evs": {k: 0 for k in iv}, "ability": ability, "moves": list(moves), "fill": False,
                 "label": label or species_name(sp)}, **extra)


# ---- held-back versions (Ian, 2026-10-15 and 2026-10-21) -----------------------------------------
#
# A box offers each pre-evolution held back as well as evolved on time
# wherever holding it back reaches, by the fight, a move sooner than its
# evolution does, or one its evolution never gets. Which holds count
# depends on the Pokemon and the move, never a power threshold (Ian,
# 2026-10-21: "It entirely depends on the pokemon and the move"): status
# moves, pivots and coverage count, and the team search judges which matter
# in each fight. His examples: a Fletchling held for Will-O-Wisp before
# Gardenia, a Popplio for Flip Turn before Byron, a Venonat to 37 for Zen
# Headbutt before Maylene, and (2026-10-15) a Starly for Brave Bird by
# Maylene's split. The learnset rules' floor stays: a wait counts only from
# HOLD_MIN levels past the level the stage could evolve at, since within
# four levels it counts as no wait (none of Ian's examples is that close).

HOLD_MIN = 5
# The evolutions a hold can delay (chain's): by level alone, or by level with
# the member's personality, gender or stats.
HELD_KINDS = {"EVO_LEVEL"} | set(_LEVEL_IF)


def _level_evolves(stage, target):
    """Whether this stage evolves into `target` by a kind a hold delays."""
    return any(e[-1] == target and e[0] in HELD_KINDS and isinstance(e[1], int)
               for e in mon_data(stage).get("evolutions") or [])


def holds_open(sp, caught, cap, base=None, places=(), gender=None, coin=None):
    """[(holds, gained, wait)]: each way to keep one stage of this member back
    longer than `base` keeps it that brings a move by `cap` which the member
    under `base` lacks, of any kind. The stage must evolve by level under
    base, at some level E, and learn the move by its own list at HOLD_MIN or
    more levels past E. `holds` is base with that stage held to the move's
    level, from which it evolves on as soon as it can; `gained` names the
    moves it brings that base lacks, `wait` the levels it is held past E.
    Shortest wait first. Rule A, which earlier fights' choices rule a hold
    out, is the caller's (plgoal3.box)."""
    base = dict(base or {})
    path = chain(sp, caught, cap, base, places=places, gender=gender, coin=coin)
    have = set(move_pool(sp, caught, cap, base, places=places, gender=gender, coin=coin)[1])
    names = move_names()
    out = []
    for k in range(len(path) - 1):
        stage, (nxt, at) = path[k][0], path[k + 1]
        if not _level_evolves(stage, nxt):
            continue
        for lv in sorted({l for l, mv in mon_data(stage)["learnset"]["by_level"]
                          if at + HOLD_MIN <= l <= cap and mv in names and names[mv] not in have}):
            held = dict(base, **{stage: lv})
            got = move_pool(sp, caught, cap, held, places=places, gender=gender, coin=coin)[1]
            gained = sorted(set(got) - have)
            if gained:
                out.append((held, gained, lv - at))
    out.sort(key=lambda t: t[2])
    return out


def hold_moves(base, holds, gained):
    """The moves a hold is for, of those it brings (`gained`): the ones its
    held stage learns at the level it is held to, the stage being the one
    `holds` keeps back past `base`. The play-off puts them in first
    (with_gain), since the hold exists for them (Ian, 2026-10-21)."""
    names = move_names()
    at = set()
    for stage, lv in holds.items():
        if (base or {}).get(stage) != lv:
            at |= {names[mv] for l, mv in mon_data(stage)["learnset"]["by_level"] if l == lv and mv in names}
    return [m for m in gained if m in at]


def hold_label(rec_species, holds):
    """A member's name with the holds its line carries, for the logs and the
    reports: "Staraptor (Starly held to 37)"."""
    if not holds:
        return rec_species
    return f"{rec_species} (" + ", ".join(f"{species_name(s)} held to {l}" for s, l in sorted(holds.items(),
                                                                                         key=lambda t: t[1])) + ")"


def member_name(rec):
    """The name the team search logs a member by: its species, or for a line
    that carries a hold its label, so that a held-back version and the same
    catch evolved on time are told apart."""
    return (rec.get("label") or rec["species"]) if rec.get("hold") else rec["species"]


class Slots:
    """A box's catches as the team search weighs them (Ian, 2026-10-21): a
    catch's versions, evolved on time and each held back (a record's
    "catch" names its catch), share one slot, so a six is six catches and
    holds do not multiply the sixes. Each six takes, for each of its
    catches, the version that gives that six the best score by the screen's
    own reckoning (score_rows over the margin table M), and the race, the
    loop and the readings see those versions. A held version no better
    than another of its catch against every enemy is never taken, since it
    can raise no six's score (the score never falls as a margin rises); of
    versions equal against every enemy, the first in box order is taken.
    The version on time (the line as it stands, not held) is never dropped
    and comes first, so where a held version is better against one enemy
    but a six scores the same with either, the six takes the version on
    time (Ian, 2026-10-21): a held version taken for nothing would set off
    the paired reading and commit the seed's later fights to its hold.
    A member without a catch is a slot of its own, so a box without held
    versions is searched exactly as before."""

    def __init__(self, st, keys, M=None):
        self.keys, self.M = list(keys), M
        self.pos = {k: i for i, k in enumerate(self.keys)}
        self.slots, self.versions, self.slot_of = [], {}, {}
        first = {}
        for k in self.keys:
            s = first.setdefault(st["pokemon"][k].get("catch") or k, k)   # a slot goes by its first version
            if s == k:
                self.slots.append(k)
                self.versions[k] = []
            self.versions[s].append(k)
            self.slot_of[k] = s
        self.multi = any(len(v) > 1 for v in self.versions.values())
        self.on_time = {s: next((k for k in v if not st["pokemon"][k].get("held")), v[0])
                        for s, v in self.versions.items()}
        self.cands = {s: self._undominated(v, self.on_time[s]) for s, v in self.versions.items()}
        self._best = {}

    @classmethod
    def of_state(cls, st, keys, boss_keys):
        """The box's slots, with the margin table worked out from the state's
        moves where a catch has several versions to choose between."""
        sl = cls(st, keys)
        if not sl.multi:
            return sl
        mine, theirs, speed = matchups(st, keys, boss_keys)
        return cls(st, keys, margins(st, keys, boss_keys, {k: st["moves"][k] for k in keys}, mine, theirs, speed))

    def _undominated(self, vs, on_time):
        """The versions a six may take: the one on time first, then each held
        version that no other version of the catch matches or beats against
        every enemy."""
        if len(vs) == 1 or self.M is None:
            return list(vs)
        R = self.M[[self.pos[k] for k in vs]]
        kept = [k for i, k in enumerate(vs)
                if k == on_time or not any(j != i and (R[j] >= R[i]).all() and ((R[j] > R[i]).any() or j < i)
                                           for j in range(len(vs)))]
        return [on_time] + [k for k in kept if k != on_time]

    def upper(self):
        """Each slot's margins at the best of its versions against each enemy:
        no choice of versions scores a six of these catches higher."""
        return np.array([self.M[[self.pos[k] for k in self.cands[s]]].max(axis=0) for s in self.slots])

    def team(self, members):
        """The six these catches make (given by slots or any versions' keys):
        each catch at its best version for that six, in box order."""
        slots = sorted({self.slot_of[k] for k in members}, key=self.pos.get)
        if all(len(self.cands[s]) == 1 for s in slots):
            return tuple(self.cands[s][0] for s in slots)
        return self.best(slots)[1]

    def best(self, slots):
        """(score, six): the version of each of these catches that gives the
        six the screen's best score, the earliest combination of the best;
        beyond BEST_CAP combinations, which no box measured had, the best
        found by changing one catch's version at a time."""
        slots = tuple(sorted({self.slot_of[k] for k in slots}, key=self.pos.get))
        if slots not in self._best:
            opts = [self.cands[s] for s in slots]
            rows = lambda team: self.M[[self.pos[k] for k in team]]
            if math.prod(len(o) for o in opts) <= BEST_CAP:
                combos = list(itertools.product(*opts))
                scores = score_rows(self.M[np.array([[self.pos[k] for k in c] for c in combos])])
                j = int(np.argmax(scores))
                got = (float(scores[j]), combos[j])
            else:
                team = [o[0] for o in opts]
                got = (float(score_rows(rows(team))), tuple(team))
                better = True
                while better:
                    better = False
                    for i, o in enumerate(opts):
                        for k in o:
                            trial = list(got[1][:i]) + [k] + list(got[1][i + 1:])
                            sc = float(score_rows(rows(trial)))
                            if sc > got[0]:
                                got, better = (sc, tuple(trial)), True
            self._best[slots] = (got[0], tuple(sorted(got[1], key=self.pos.get)))
        return self._best[slots]

    def top(self, n=20, apart=2):
        """The screen's top sixes, [(score, six)] best first, each six of
        catches at their best versions for it and differing from every one
        kept before it in at least `apart` catches. The sixes of catches are
        scored first at each catch's best against each enemy (upper), which
        bounds what any choice of versions can score; they are then scored
        at their best versions in the bound's order, only as far as the top
        needs, so the list is exact. Without held versions the bound is the
        score, and the screen is today's: by score, ties in the order the
        sixes are drawn up."""
        U = self.upper()
        total = math.comb(len(self.slots), min(6, len(self.slots)))
        keep = SCREEN_KEEP
        while True:
            listed = score_sixes(U, keep=keep, index=True)
            complete = keep is None or len(listed) < keep
            done, at, kept = [], 0, []
            while True:
                for bound, idx, drawn in listed[at:at + 2000]:
                    slots = [self.slots[i] for i in idx]
                    if any(len(self.cands[s]) > 1 for s in slots):
                        score, six = self.best(slots)
                    else:
                        score, six = bound, tuple(self.cands[s][0] for s in slots)
                    done.append((-score, drawn, six, idx))
                at = min(at + 2000, len(listed))
                done.sort()
                # Every six not yet scored at its best versions scores at most
                # this, so the sixes scoring more are in their final order.
                limit = listed[at][0] if at < len(listed) else (float("-inf") if complete else listed[-1][0])
                kept = []
                for neg, _d, six, idx in done:
                    if -neg <= limit:
                        break
                    if all(len(set(idx) - set(j)) >= apart for _s, _t, j in kept):
                        kept.append((-neg, six, idx))
                        if len(kept) >= n:
                            return [(sc, t) for sc, t, _j in kept]
                if at >= len(listed):
                    break
            if complete:
                return [(sc, t) for sc, t, _j in kept]
            keep = None if keep * 4 >= total else keep * 4


# Beyond this many combinations of versions for one six, Slots.best improves
# one catch's version at a time instead of trying them all.
BEST_CAP = 4096


# ---- 1. the screen ---------------------------------------------------------------------------------------

def prepare(fight_key, records, item_stock, variant=0):
    """The fight against the whole box, every member with its whole pool:
    (st, the members' keys, the boss variant's (keys, flags)). `variant`
    picks the trainer's team where it depends on the player's starter."""
    prep = plscore.prepare(plscore.parse_fight(fight_key), given_side=records)
    st = prep["st"]
    st["item_stock"] = dict(item_stock)
    keys = [f"p{i}" for i in range(len(records))]
    boss_keys, flags, _s = prep["variants"][variant]
    return st, keys, boss_keys, flags


def matchups(st, keys, boss_keys):
    """For the fight's first weather: each member's expected share of each
    enemy's HP a turn by each of its moves, each enemy's best share of each
    member's HP, and speeds."""
    w = sorted({x for x, _a, _d in st["rows"]}, key=str)[0]

    def row(a, t):
        return st["rows"].get((w, a, t)) or st["rows"].get((None, a, t))

    def expected(k, e, name, mv):
        info = st["info"].get(k)         # its ability and item, for a Population Bomb's row (plfeat._expected)
        if name == "Magnitude":
            # Its power is rolled on use, so its rows are one per power, under
            # twin keys (fightsim.prepare); the expectation weighs them by odds.
            return sum(pct / 100 * plfeat._expected((row(f"{k}#m{p}", e) or {}).get("moves", {}).get(name), mv, info)
                       for p, pct in fs.MAGNITUDE_POWERS.items())
        if name == "Heat Crash":
            # Its power is set by the two weights, so its row is the one made
            # at that power under a twin key (fightsim.prepare's heat_crash).
            power = (st.get("heat_crash") or {}).get((k, e))
            return plfeat._expected((row(f"{k}#hc{power}", e) or {}).get("moves", {}).get(name), mv, info) if power else 0.0
        raw = (st.get("metal_raw") or {}).get(e) if name in fs.WEIGHT_MOVES else None
        if raw and row(k, raw):
            # a Mold Breaker's weight move reads a Heavy Metal or Light Metal
            # foe at its own weight (fightsim.metal_raw_key)
            return plfeat._expected(row(k, raw).get("moves", {}).get(name), mv, info)
        return plfeat._expected((row(k, e) or {}).get("moves", {}).get(name), mv, info)

    mine = {}       # (member, move): [share of each enemy's HP]
    for k in keys:
        for name in st["moves"][k]:
            mv = fs.move(name)
            if not mv.damaging():
                continue
            mine[(k, name)] = [expected(k, e, name, mv) / st["info"][e]["hp"] for e in boss_keys]
    theirs = {}     # (enemy, member): best share of the member's HP
    for e in boss_keys:
        for k in keys:
            r = row(e, k)
            best = 0.0
            for name in st["moves"][e]:
                mv = fs.move(name)
                if mv.damaging() and r:
                    best = max(best, plfeat._expected(r["moves"].get(name), mv, st["info"].get(e)))
            theirs[(e, k)] = best / st["info"][k]["hp"]
    speed = {k: st["speed"].get((w, k)) or st["speed"].get((None, k)) or 1 for k in keys + list(boss_keys)}
    return mine, theirs, speed


def pick_moves(st, k, boss_keys, mine):
    """A member's four moves against this fight: up to three attacks of
    different types chosen for coverage (each adds the most to its best hit
    on every enemy), then the scorer's status rule (the best policy status
    move of tier A, else attacks, else status moves of tier B), as
    fightsim.player_moves fills a set."""
    attacks = [(n, s) for (kk, n), s in mine.items() if kk == k]
    chosen, types, best = [], set(), [0.0] * len(boss_keys)
    while len(chosen) < 3:
        gain, pick = 0.0, None
        for n, s in attacks:
            if n in chosen or fs.move(n).type in types:
                continue
            g = sum(max(0.0, min(1.0, x) - b) for x, b in zip(s, best))
            if g > gain:
                gain, pick = g, (n, s)
        if pick is None:
            break
        chosen.append(pick[0])
        types.add(fs.move(pick[0]).type)
        best = [max(b, min(1.0, x)) for b, x in zip(best, pick[1])]
    tiers = fs.status_tiers()
    # Every status move it has, best tier first: Ian's tiers rate Screech,
    # Play Nice and Leer low, yet our lines won Roark and Mars 1 with them,
    # so a spare slot takes a status move before a weaker attack of a type
    # already chosen (a move that does nothing in a position is never
    # offered by the planner, so a useless one costs nothing).
    idle = IDLE | idle_sports(st, boss_keys)
    status = sorted([n for n in st["moves"][k] if fs.move(n).cat == "Status" and n not in idle],
                    key=lambda n: -tiers.get(n, 0))
    out = chosen + [n for n in status[:1] if tiers.get(n, 0) >= fs.TIERS["A"]]
    rest = sorted((n for n, _s in attacks if n not in out), key=lambda n: -sum(mine[(k, n)]))
    new_type, seen = [], set(types)
    for n in rest:                       # the best attack of each type not yet covered
        if fs.move(n).type not in seen:
            new_type.append(n)
            seen.add(fs.move(n).type)
    same_type = [n for n in rest if n not in new_type]
    for n in new_type + status + same_type + [n for n in st["moves"][k] if n not in out]:
        if len(out) >= 4:
            break
        if n not in out:
            out.append(n)
    return out[:4]


# Status moves that do nothing in these fights (field effects and the like),
# filled only when nothing else is left. Mud Sport and Magic Room left the
# list on 2026-10-15, as the simulator now runs both (Ian approved), and
# Copycat and Water Sport on 2026-10-20, which it runs since batches 10
# and 6 (Ian approved: he plans to use Copycat often); the two Sports are
# idle still against a team with nothing for them to halve (idle_sports).
IDLE = {"Splash", "Teleport", "Celebrate", "Hold Hands", "Follow Me",
        "Helping Hand", "Ally Switch", "Wonder Room"}
# Water Sport halves only Fire moves and Mud Sport only Electric ones
# (fightsim.sport_half), so each is idle in a fight whose trainer's team
# has no damaging move of its type (Ian, 2026-10-20: "have it be lacking a
# damaging move of that type"; a Fire or Electric status move does not
# count). Batch 11 found the search giving Barboach and Goldeen Water Sport
# against Roark, who has no Fire move, in place of Aqua Jet and Mud-Slap.
SPORT_TYPE = {"Water Sport": "Fire", "Mud Sport": "Electric"}


def idle_sports(st, boss_keys):
    """The Sports idle against this team (SPORT_TYPE): those whose type no
    damaging move of the team's has, typed as sport_half types it
    (fightsim.move_type_used: Weather Ball in each weather the fight can
    have, its own and what the team's abilities and moves set, as prepare
    finds them; Hidden Power by its IVs, Natural Gift by its Berry, an
    ability that retypes moves). A few dozen moves at most, so it is
    worked out at each call."""
    recs = [st["pokemon"].get(e) or {} for e in boss_keys]
    weathers = {None, st.get("base_weather")} | {fs.ABILITY_WEATHER[r["ability"]] for r in recs
                                                  if r.get("ability") in fs.ABILITY_WEATHER}
    weathers |= {fs.WEATHER_OF[fs.move(n).effect] for e in boss_keys for n in st["moves"].get(e, ())
                 if fs.move(n).effect in fs.WEATHER_OF}
    types = set()
    for e, rec in zip(boss_keys, recs):
        for name in st["moves"].get(e, ()):
            mv = fs.move(name)
            if mv.damaging():
                types |= {fs.move_type_used(rec.get("ability"), mv, rec.get("ivs") or {}, rec.get("item"), w)
                          for w in weathers}
    return frozenset(s for s, t in SPORT_TYPE.items() if t not in types)


def margins(st, keys, boss_keys, moves, mine, theirs, speed):
    """For each member and enemy, how far the member wins their one-on-one:
    the hits the enemy needs to knock the member out less the hits the
    member needs, half a hit more for moving first and half a hit less for
    moving second. Positive means the member answers the enemy."""
    out = np.zeros((len(keys), len(boss_keys)))
    for i, k in enumerate(keys):
        for j, e in enumerate(boss_keys):
            share = max([mine[(k, n)][j] for n in moves[k] if (k, n) in mine] or [0.0])
            hits = math.ceil(1.0 / share) if share > 0.01 else 99
            taken = math.ceil(1.0 / theirs[(e, k)]) if theirs[(e, k)] > 0.01 else 99
            out[i, j] = min(taken - hits + (0.5 if speed[k] > speed[e] else -0.5), 3.0)
    return out


_STRENGTH = {}


def split_strength(st, keys, split, cap, leave_out=()):
    """Each box member's strength in its split, for the blind draw: its mean
    margin, as the screen reckons it and clipped to 3 either way, against
    every Pokemon of the split's ordinary singles trainers (plgen.trainers),
    with its own moves. No trainer being read is in view, so the reading
    stays blind (`leave_out`: trainer ids kept out of the panel, such as the
    one read). {key: strength}, cached by the box and the panel."""
    from . import data, plgen
    recs = [st["pokemon"][k] for k in keys]
    panel = [tr for tr in plgen.trainers((split,)) if tr not in set(leave_out)]
    tag = json.dumps([split, cap, panel, [(r["species"], r["level"], list(st["moves"][k]))
                                          for r, k in zip(recs, keys)]])
    if tag not in _STRENGTH:
        parties = [plscore.with_genders(data.oxide_trainers()[tr]) for tr in panel]
        s2 = fs.prepare(split, parties, None, cap=cap, given_side=[dict(r, moves=list(st["moves"][k]))
                                                                   for r, k in zip(recs, keys)])
        own = [f"p{i}" for i in range(len(recs))]
        foes = [k for party in s2["bosses"] for k in party]
        mine, theirs, speed = matchups(s2, own, foes)
        M = np.clip(margins(s2, own, foes, {k: s2["moves"][k] for k in own}, mine, theirs, speed), -3, 3)
        _STRENGTH[tag] = {k: float(M[i].mean()) for i, k in enumerate(keys)}
    return _STRENGTH[tag]


def blind_pool(st, keys, split, cap=None, leave_out=()):
    """The members an ordinary trainer's blind six is drawn from (Ian,
    2026-10-04): never one held below the cap (the box's top level when no
    cap is given), and of the rest the stronger half by split_strength, six
    at least while the box has them, in box order."""
    levels = {k: st["pokemon"][k]["level"] for k in keys}
    top = cap if cap is not None else max(levels.values())
    ready = [k for k in keys if levels[k] >= top] or list(keys)
    power = split_strength(st, ready, split, top, leave_out)
    ranked = sorted(ready, key=lambda k: -power[k])
    kept = set(ranked[:max(6, (len(ranked) + 1) // 2)])
    return [k for k in keys if k in kept]


def score_rows(R, depth=0.3, hole=2.0):
    """The screen's score of sixes given by their members' rows of the margin
    table (... x members x enemies): per enemy, its best answer's margin and
    a little for a second answer, less a penalty for each enemy no member
    answers."""
    top = np.sort(R, axis=-2)
    best = top[..., -1, :]
    second = top[..., -2, :] if R.shape[-2] > 1 else np.zeros_like(best)
    return (np.clip(best, -3, 3) + depth * np.clip(second, 0, 3)).sum(-1) - hole * (best <= 0).sum(-1)


def score_sixes(M, size=6, depth=0.3, hole=2.0, keep=None, index=False):
    """Every six of the box scored at once (score_rows). [(score, member
    indices)], best first, ties in the order the sixes are drawn up; with
    `index`, [(score, member indices, the order it was drawn up in)]. With
    `keep`, only the best `keep` come back, exactly the first `keep` of the
    whole list: the sixes are drawn up and scored a block at a time and
    only the best of each block are held, so a box of fifty or more fits in
    memory (every six of a 51-member box held at once took 5.3 GB, the best
    100,000 take 0.2)."""
    n = M.shape[0]
    size = min(size, n)
    it = itertools.combinations(range(n), size)
    Ss, Cs, Is = [], [], []          # the blocks held so far: scores, sixes, the order they were drawn in
    held, drawn = 0, 0
    while True:
        block = list(itertools.islice(it, 50000))
        if not block:
            break
        c = np.array(block)
        idx = np.arange(drawn, drawn + len(c))
        drawn += len(c)
        s = score_rows(M[c], depth, hole)            # M[c]: sixes x members x enemies
        Ss.append(s), Cs.append(c), Is.append(idx)
        held += len(s)
        if keep is not None and held > 2 * keep:
            # Hold the best `keep`, with every six tied with the last of them,
            # so that the final order over what is held is the whole list's.
            S, C, I = np.concatenate(Ss), np.concatenate(Cs), np.concatenate(Is)
            bar = np.partition(S, len(S) - keep)[len(S) - keep]
            ok = S >= bar
            Ss, Cs, Is = [S[ok]], [C[ok]], [I[ok]]
            held = int(ok.sum())
    if not Ss:
        return []
    S, C, I = np.concatenate(Ss), np.concatenate(Cs), np.concatenate(Is)
    order = np.lexsort((I, -S))
    if keep is not None:
        order = order[:keep]
    if index:
        return [(float(S[j]), tuple(C[j].tolist()), int(I[j])) for j in order]
    return [(float(S[j]), tuple(C[j].tolist())) for j in order]


# The sixes the screen holds while it looks for its top ones (score_sixes'
# `keep`); it looks again over more of them in the rare case these run out.
SCREEN_KEEP = 100000


def screen(st, keys, boss_keys, top=20, apart=2):
    """The screen: each member's moves for this fight (set into the state,
    so every later fight uses them) and the top sixes, each six of the box's
    catches at their best versions for it (Slots: a catch's versions share
    one slot) and differing from every one kept before it in at least
    `apart` catches. Returns (sixes as key lists, their scores, the margin
    table, each member's moves)."""
    mine, theirs, speed = matchups(st, keys, boss_keys)
    moves = {k: pick_moves(st, k, boss_keys, mine) for k in keys}
    for k in keys:
        st["moves"][k] = moves[k]
        st["pokemon"][k] = dict(st["pokemon"][k], moves=moves[k])
    M = margins(st, keys, boss_keys, moves, mine, theirs, speed)
    kept = Slots(st, keys, M).top(top, apart)
    return [list(six) for _s, six in kept], [s for s, _six in kept], M, moves


# ---- 2. labels and networks --------------------------------------------------------------------------------

_JOB = {}


def _label_job(args):
    team, positions, seed, out_dir, name = args
    j = _JOB
    return pldata.distill(j["st"], team, j["boss_keys"], j["flags"], positions, seed, out_dir,
                          {"fight": name, "six": [j["st"]["pokemon"][k]["species"] for k in team]})


def label(st, sixes, boss_keys, flags, name, out_dir, positions=4500, budget=64, procs=None, seed=1):
    """The play-out planner's labels on these sixes (a job each), at the
    given budget: a tenth of a round over ten sixes by default."""
    _JOB.update(st=st, boss_keys=boss_keys, flags=flags)
    pldata.LABEL_BUDGET = budget
    jobs = [(six, positions, seed * 1000 + i, out_dir, name) for i, six in enumerate(sixes)]
    with plplan.fork_pool(procs or min(len(jobs), plplan.pool_size())) as pool_:
        return list(pool_.imap_unordered(_label_job, jobs, chunksize=1))


def without(fight_names, out):
    """A folder of links to every labelled shard so far except these fights'
    (their old labels would have seen other teams of the same fight)."""
    os.makedirs(out, exist_ok=True)
    for folder in ("data-gen", "data-gen-held", "data-d1", "data-d2", "data-d3"):
        for p in __import__("glob").glob(os.path.join(ROOT, folder, "*.json")):
            with open(p) as fh:
                if json.load(fh)["fight"] in fight_names:
                    continue
            for ext in (".json", ".npz"):
                t = os.path.join(out, f"{folder}-{os.path.basename(p)[:-5]}{ext}")
                if not os.path.exists(t):
                    os.symlink(p[:-5] + ext, t)
    return out


def train(name, data_dirs, seeds=(1, 2)):
    """Networks from scratch on these folders, one per seed, under the
    memory cap; their average's name. A lock file makes searches running
    side by side train one at a time, since each training run loads every
    labelled position and two at once would not fit in memory."""
    import fcntl
    with open(os.path.join(ROOT, "train.lock"), "w") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        for s in seeds:
            subprocess.run([os.path.join(REPO, "tools/oxide/capped"), "--max", "22G",
                            os.path.expanduser("~/venvs/oxide-ml/bin/python"), "-m", "tools.oxide.balance.plnet",
                            "--name", f"{name}-s{s}", "--data", *data_dirs, "--held-out", "0", "--epochs", "10",
                            "--lr", "1e-3", "--seed", str(s)],
                           cwd=REPO, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                           env=dict(os.environ, PYTHONPATH="."))
    return "+".join(f"{name}-s{s}" for s in seeds)


# ---- 3 and 4. the race and the finalists ---------------------------------------------------------------------

_LEADS = {}


def _fight_job(args):
    team, seed, cfg, luck, used = args
    j = _JOB
    lk = (tuple(team), json.dumps(cfg, sort_keys=True))
    if lk not in _LEADS:
        _LEADS[lk] = plplan.Planner(0, **cfg).lead(j["st"], list(team), j["boss_keys"], j["flags"])[0]
    turns = [] if used else None
    r = plplan.play(j["st"], list(team), j["boss_keys"], j["flags"], _LEADS[lk], seed, cfg, luck, record=turns)
    # With `used`, the moves the player chose in the fight, switches left
    # out, for the reading's report of what its wins lean on.
    chose = sorted({t["chose"] for t in turns if not str(t["chose"]).startswith("switch to ")}) if used else None
    return (tuple(team), r["won"], r["deaths"], r["clean"], [tuple(x) for x in r["faints"]], r["seconds"], chose,
            (seed, luck))


class Tally:
    """Every fight read for each six, and the race's score from them; the
    fights themselves, (seed, luck), so that another six can be played on
    the same ones (`fights`, the play-off's); and where the reading asked
    for them, the moves the player chose in each fight (`chose`). Both in
    the order of `rows`."""

    def __init__(self):
        self.rows = {}
        self.chose = {}
        self.fights = {}

    def add(self, team, won, deaths, clean, faints, chose=None, fight=None):
        self.rows.setdefault(tuple(team), []).append((won, deaths, clean, faints))
        if chose is not None:
            self.chose.setdefault(tuple(team), []).append(chose)
        if fight is not None:
            self.fights.setdefault(tuple(team), []).append(tuple(fight))

    def score(self, team):
        r = self.rows.get(tuple(team), [])
        if not r:
            return -1.0
        return sum(w for w, *_ in r) / len(r) - 0.1 * sum(d for _w, d, *_ in r) / len(r)

    def numbers(self, team):
        r = self.rows.get(tuple(team), [])
        n = max(1, len(r))
        return {"fights": len(r), "won": sum(w for w, *_ in r) / n, "faints": sum(d for _w, d, *_ in r) / n,
                "clean": sum(c for _w, _d, c, _f in r) / n}


def read(st, boss_keys, flags, teams, fights, cfg, luck="real", seed0=0, procs=None, tally=None, used=False):
    """Each team read on `fights` more fights; the tally. With `used`, the
    tally keeps the moves the player chose in each fight."""
    _JOB.update(st=st, boss_keys=boss_keys, flags=flags)
    tally = tally or Tally()
    jobs = []
    for t in teams:
        # Each team's seeds follow from its members (a checksum, the same in
        # every process) and the fights it has had, so a reading repeats.
        start = seed0 * 1_000_003 + zlib.crc32(",".join(t).encode()) + len(tally.rows.get(tuple(t), []))
        jobs += [(tuple(t), start + i, cfg, luck, used) for i in range(fights)]
    return play_jobs(st, boss_keys, flags, jobs, procs, tally)


def play_jobs(st, boss_keys, flags, jobs, procs=None, tally=None):
    """Fights given one by one, (team, seed, cfg, luck, used), played in a
    pool of workers and added to the tally."""
    _JOB.update(st=st, boss_keys=boss_keys, flags=flags)
    tally = tally or Tally()
    with plplan.fork_pool(procs or plplan.pool_size()) as pool_:
        for team, won, deaths, clean, faints, _s, chose, fight in pool_.imap_unordered(_fight_job, jobs, chunksize=1):
            tally.add(team, won, deaths, clean, faints, chose, fight)
    return tally


# ---- 3b. the play-off -----------------------------------------------------------------------------

def with_gain(st, k, picks=None):
    """The four moves a held version plays the play-off with, from the
    screen's picks (`picks`, else its moves now). The screen's margins
    count hits only, so its picks can leave out the very move the hold
    exists for (Will-O-Wisp on a Fletchling held to 25). The move the hold
    is for (the record's "hold_for", learned at the hold's level) goes in
    first, then the hold's other moves ("gained"), each in place of a pick
    from the last back; the first two picks are always kept, and so is a
    pick the hold itself brought (Ian, 2026-10-21: Sharpedo held as
    Carvanha to 38 lost Take Down, its hold's move, to Agility, and Liepard
    held as Purrloin to 36 played two gained moves by name and not Sucker
    Punch). Should no other place be left, the hold's own move takes the
    last place past the first two that holds another gained move."""
    picks = list(st["moves"][k] if picks is None else picks)
    rec = st["pokemon"][k]
    gained = list(rec.get("gained") or ())
    why = list(rec.get("hold_for") or ())
    extra = [m for m in why if m not in picks] + [m for m in gained if m not in picks and m not in why]
    if not extra:
        return picks
    out = picks[:4]
    while len(out) < 4 and extra:
        out.append(extra.pop(0))
    free = [i for i in range(len(out) - 1, 1, -1) if out[i] not in gained]
    for i, m in zip(free, extra):
        out[i] = m
    for m in why:
        if m not in out:
            spare = [i for i in range(len(out) - 1, 1, -1) if out[i] not in why]
            if spare:
                out[spare[0]] = m
    return out


def playoff(st, boss_keys, flags, finalists, tally, cfg, slots, procs=None, log=print):
    """Ian's play-off (2026-10-21, his option 1), after the race, for the
    held versions the screen cannot see (a status move or a pivot gains no
    hits in its margins). Each finalist is also played with every other
    version of each of its members, one member swapped at a time, on the
    same fights the race read it on (tally.fights, the race's own luck and
    planner), every held version included, those the screen dropped as
    dominated among them, since they are the point; a held version plays
    with the moves its hold brings (with_gain), built from the screen's
    picks every time, so a version tried for two finalists plays the same
    four. A version a kept six takes keeps that four; after each finalist
    every other version goes back to the screen's picks, so that the loop
    and the readings, which choose by the screen's margins for those picks,
    never meet a four the play-off left behind (Ian, 2026-10-21).
    A swap is kept where it scores better than the finalist by more than
    the race's tolerance (WIN_TOL) on the race's own tally (Tally.score),
    since one fight in about 30 moves a score three or four points and the
    best of several swaps would otherwise often win on luck (Ian,
    2026-10-21: the margin alone, with no confirmation read, to keep the
    readings fast); of several winning swaps of one member, the
    best. Where more than one member's swap wins, their combination is
    played once more on the same fights and kept if it scores at least as
    well as the best single swap, else that swap is. Returns (the finalists
    after it, in order, a six that two finalists became counted once, and
    a record for each finalist). A finalist with no other versions plays
    nothing, so a box without held versions reads exactly as before."""
    sl = slots
    pos = sl.pos
    name = lambda t: [member_name(st["pokemon"][k]) for k in t]
    # Every version's moves and record as the screen left them, to build the
    # play-off's fours from and to put back where a version is not kept.
    screen = {k: (list(st["moves"][k]), st["pokemon"][k]) for vs in sl.versions.values() for k in vs
              if k in st["moves"]}

    def restore(kept):
        for k, (four, rec) in screen.items():
            if k not in kept:
                st["moves"][k] = list(four)
                st["pokemon"][k] = rec

    out, record = [], []
    for fin in map(tuple, finalists):
        fights = tally.fights.get(fin, [])
        swaps = [(i, k, v, tuple(sorted(fin[:i] + (v,) + fin[i + 1:], key=pos.get)))
                 for i, k in enumerate(fin) for v in sl.versions[sl.slot_of[k]] if v != k]
        if not swaps or not fights:
            out.append(fin)
            record.append({"six": name(fin), "swaps": [], "kept": name(fin)})
            continue
        for _i, _k, v, _t in swaps:
            if st["pokemon"][v].get("held"):
                four = with_gain(st, v, screen[v][0])
                st["moves"][v] = four
                st["pokemon"][v] = dict(screen[v][1], moves=four)
        played = play_jobs(st, boss_keys, flags, [(t, seed, cfg, luck, False) for _i, _k, _v, t in swaps
                                                  for seed, luck in fights], procs)
        base = tally.score(fin)
        best = {}
        for i, _k, v, t in swaps:
            sc = played.score(t)
            if sc > base + WIN_TOL + 1e-9 and sc > best.get(i, (float("-inf"),))[0]:
                best[i] = (sc, v, t)
        rec = {"six": name(fin), "score": round(base, 3), "fights": len(fights),
               "swaps": [{"out": member_name(st["pokemon"][k]), "in": member_name(st["pokemon"][v]),
                          "score": round(played.score(t), 3)} for _i, k, v, t in swaps]}
        kept = fin
        if len(best) == 1:
            kept = next(iter(best.values()))[2]
        elif best:
            combo = list(fin)
            for i, (_sc, v, _t) in best.items():
                combo[i] = v
            combo = tuple(sorted(combo, key=pos.get))
            play_jobs(st, boss_keys, flags, [(combo, seed, cfg, luck, False) for seed, luck in fights], procs, played)
            top = max(best.values(), key=lambda b: b[0])
            holds = played.score(combo) >= top[0]
            kept = combo if holds else top[2]
            rec["combined"] = {"six": name(combo), "score": round(played.score(combo), 3), "kept": holds}
        rec["kept"] = name(kept)
        log(f"  play-off on {', '.join(rec['six'])} ({base:.2f} on {len(fights)}): {len(swaps)} swaps; "
            + (f"kept {', '.join(rec['kept'])}" if kept != fin else "no swap led by more than the tolerance"))
        out.append(kept)
        record.append(rec)
        restore({k for t in out for k in t})
    return list(dict.fromkeys(out)), record


def round_size(slots, per_round):
    """(team size, sixes a race round draws). A small box holds fewer
    different sixes than a round draws (seven members make seven): a round
    then takes them all, where it used to draw for ever (Lucas and Dawn 1,
    goal 3, 2026-10-07); a box under six fields all it has. `slots` are the
    box's catches (Slots.slots), so a catch's versions count once."""
    size = min(6, len(slots))
    return size, min(per_round, math.comb(len(slots), size))


def spread_room(slots, top):
    """How many sixes drawn at random the labels can add beside the screen's
    `top` ones: five, or as many as the box's catches have left."""
    return min(5, math.comb(len(slots), 6) - len(top)) if len(slots) > 6 else 0


def race(st, keys, boss_keys, flags, screened, cfg, rounds=5, per_round=16, fights=4, elite=4, rate=0.3,
         log=print, seed=1, slots=None):
    """Ian's member ratings, then halving: (finalists best first, the tally,
    the members' final weights). The members are the box's catches (Slots:
    a catch's versions share one slot), each six drawn taking its catches'
    best versions for it. Weights start from how often each catch is in
    the screen's sixes; each round draws `per_round` sixes by weight (the
    screen's best always among the first round's), reads each on `fights`
    fights, and moves the weights toward the catches of the `elite` best
    sixes so far."""
    sl = slots or Slots.of_state(st, keys, boss_keys)
    of = sl.slot_of
    rng = random.Random(seed)
    counts = {c: 1.0 + sum(any(of[k] == c for k in s) for s in screened) for c in sl.slots}
    w = {c: n / sum(counts.values()) for c, n in counts.items()}
    tally = Tally()
    size, per_round = round_size(sl.slots, per_round)
    for r in range(rounds):
        teams = [tuple(s) for s in screened[:per_round // 2]] if r == 0 else []
        while len(teams) < per_round:
            pool_ = list(sl.slots)
            six = []
            for _ in range(size):
                pick = rng.choices(pool_, weights=[w[k] for k in pool_])[0]
                six.append(pick)
                pool_.remove(pick)
            t = tuple(sorted(sl.team(six), key=keys.index))
            if t not in teams:
                teams.append(t)
        read(st, boss_keys, flags, teams, fights, cfg, seed0=seed * 7919 + r, tally=tally)
        best = sorted(tally.rows, key=lambda t: -tally.score(t))[:elite]
        share = {c: sum(any(of[k] == c for k in t) for t in best) / elite for c in sl.slots}
        w = {c: (1 - rate) * w[c] + rate * (share[c] + 0.01) for c in sl.slots}
        log(f"  race round {r + 1}: best {[st['pokemon'][k]['species'] for k in best[0]]} "
            f"score {tally.score(best[0]):.2f}; heaviest {sorted(w, key=lambda k: -w[k])[:6]}")
    cands = sorted(tally.rows, key=lambda t: -tally.score(t))[:5]
    for fights_more, keep in ((8, 3), (16, 3)):
        read(st, boss_keys, flags, cands, fights_more, cfg, seed0=seed * 104729, tally=tally)
        cands = sorted(cands, key=lambda t: -tally.score(t))[:keep]
    return cands, tally, w


def full_reading(st, boss_keys, flags, team, cfg, real=75, unlucky=25, procs=None, seed=9, tallies=None):
    """The reading Ian rules: 75 fights at real odds and 25 very unlucky.
    With `tallies` (a list), its two tallies are added to it, each keeping
    the moves the player chose in every fight."""
    used = tallies is not None
    a = read(st, boss_keys, flags, [team], real, cfg, "real", seed0=seed * 31337, procs=procs, used=used)
    b = read(st, boss_keys, flags, [team], unlucky, cfg, "unlucky", seed0=seed * 31337 + 1, procs=procs, used=used)
    if used:
        tallies.extend([a, b])
    return a.numbers(team), b.numbers(team), a.rows[tuple(team)]


def losing_enemies(rows):
    """Which enemy Pokemon a reading's faints fell to, most first, from its
    rows' (fainted, enemy out) pairs."""
    tally = {}
    for _w, _d, _c, faints in rows:
        for _mine, foe in faints:
            tally[foe] = tally.get(foe, 0) + 1
    return sorted(tally.items(), key=lambda kv: -kv[1])


# Win rates this close count as equal before faints decide (Ian,
# 2026-10-03): on a 25-fight check one fight moves the rate four points, and
# with no tolerance one fight's luck chose Gardenia's winner at budget 64.
WIN_TOL = 0.05


def ian_best(teams, numbers):
    """The best of these sixes by Ian's order: the highest win rate, any
    within WIN_TOL of it counted as equal, then the fewest faints; a tie
    keeps the given order. `numbers` gives a six's reading."""
    top = max(numbers(t)["won"] for t in teams)
    near = [t for t in teams if numbers(t)["won"] >= top - WIN_TOL - 1e-9]
    return min(near, key=lambda t: numbers(t)["faints"])


def improve(st, keys, boss_keys, flags, M, best, po, check=25, procs=None, rounds=3, log=print, slots=None):
    """Ian's diagnose-and-loop, read by the play-outs: the enemies the best
    six's faints fell to, weighted by how many, pick the box members whose
    screen margins answer them best; two candidates built from those (the
    six that answers them best, and the best six with its two weakest
    answerers swapped for the two strongest it lacks) are read on the same
    play-out check (`po`, a Tally), and the best by Ian's order is kept.
    Up to `rounds` rounds, stopping when no candidate beats the best or no
    faint is left to diagnose. Built after Fantina, where the race, run on
    a network that read the finalists at 40% won against the play-outs' 92
    to 96%, kept a core whose margins against Mismagius, Rotom and Sableye
    were among the box's worst, and two sixes built this way won every
    fight with 2.8 faints against the winner's 96% and 4.2. The members are
    the box's catches (Slots), each answering as its best version does, and
    each candidate takes its catches' best versions for it. Returns the
    best six (a tuple of keys)."""
    sl = slots or Slots(st, keys, M)
    of = sl.slot_of
    names = {k: member_name(st["pokemon"][k]) for k in keys}
    foes = [st["pokemon"][k]["species"] for k in boss_keys]
    for r in range(rounds):
        lost = dict(losing_enemies(po.rows[tuple(best)]))
        if not lost:
            break
        weight = [lost.get(f, 0) for f in foes]
        answer = {k: sum(weight[j] * M[i][j] for j in range(len(foes))) for i, k in enumerate(keys)}
        ranked = sorted(sl.slots, key=lambda c: -max(answer[k] for k in sl.cands[c]))
        weakest = [of[k] for k in sorted(best, key=lambda k: answer[k])[:2]]
        stay = [of[k] for k in best if of[k] not in weakest]
        incoming = [c for c in ranked if c not in {of[k] for k in best}][:2]
        cands = [tuple(sorted(sl.team(ranked[:6]), key=keys.index)),
                 tuple(sorted(sl.team(stay + incoming), key=keys.index))]
        cands = [c for c in dict.fromkeys(cands) if c not in po.rows]
        if not cands:
            break
        read(st, boss_keys, flags, cands, check, {}, procs=procs, seed0=77, tally=po)
        for c in cands:
            n = po.numbers(c)
            log(f"  loop {r + 1}: {', '.join(names[k] for k in c)}: {n['won']:.1%} won, {n['faints']:.3f} faints, "
                f"{n['clean']:.1%} clean")
        new = ian_best([tuple(best)] + cands, po.numbers)
        if new == tuple(best):
            break
        best = new
    return tuple(best)


# ---- the whole search on one box ----------------------------------------------------------------------

def search(fight, key, recs, stock, out_dir, variant=0, ours=None, bar=None, procs=10, check=25, prepared=None,
           model=None):
    """The five stages on one box, with a log and result.json in `out_dir`.
    `key` is the story fight (fights.json), `recs` the box's records with
    their whole move pools, `stock` the items the run has by then (in
    fightsim.player_items' form), `variant` the trainer's team a run with
    this starter meets. `ours`, a hand-played six's species names, is read
    beside the finalists where one exists, against `bar`. `model`, networks
    already trained for this boss, skips the labels and the training.

    The labels are the screen's top five sixes and five drawn at random from
    the box (labelled on the top sixes alone, which share a core, the first
    Roark test's networks read our six at 52% won and misled the race). The
    play-out planner then reads every finalist on `check` fights and the
    winner is the one it ranks best by Ian's order: the network erred both
    ways in that test, too kind at Roark and too harsh at Gardenia, so its
    race is a shortlist and not a verdict. Last, the winner's fight on the
    trace seed is written out turn by turn (line.txt), for Ian to read."""
    import time
    os.makedirs(out_dir, exist_ok=True)
    logf = open(os.path.join(out_dir, "log.txt"), "a")

    def log(*a):
        line = " ".join(str(x) for x in a)
        print(line, flush=True)
        logf.write(line + "\n")
        logf.flush()

    t0 = time.time()
    # `prepared`: a fight already made (st, keys, boss_keys, flags), as plstudy
    # makes one from a trainer file outside res/.
    st, keys, boss_keys, flags = prepared or prepare(key, recs, stock, variant)
    # A held-back version goes by its label ("Staraptor (Starly held to
    # 37)"), so that it and the same catch evolved on time are told apart.
    names = {k: member_name(st["pokemon"][k]) for k in keys}
    foes = [f"{st['pokemon'][k]['species']} {st['pokemon'][k]['level']}" for k in boss_keys]
    log(f"== {fight}: {', '.join(foes)}; box of {len(keys)}: {', '.join(names[k] for k in keys)}; "
        f"items {stock}; prepared in {time.time() - t0:.0f} s")
    sixes, scores, M, moves = screen(st, keys, boss_keys)
    # The box's catches, a catch's versions sharing one slot: every six the
    # labels, the race and the loop read takes its catches' best versions.
    sl = Slots(st, keys, M)
    log("screen, top sixes:")
    for s, sc in list(zip(sixes, scores))[:10]:
        log(f"  {sc:6.2f}  {', '.join(names[k] for k in s)}")
    mine = [k for k in keys if names[k] in ours] if ours else None
    rank = None
    if mine:
        all_scores = score_sixes(M)
        rank = next((i for i, (_s, idx) in enumerate(all_scores) if {keys[j] for j in idx} == set(mine)), None)
        log(f"our six ({', '.join(names[k] for k in mine)}): screen rank {rank} of {len(all_scores)}")
    log("moves picked: " + "; ".join(f"{names[k]} {', '.join(moves[k])}" for k in keys))

    if model is not None:
        # Networks trained on another box of the same boss (goal 3's reuse,
        # Ian's yes of 2026-10-07): the race is a shortlist either way, and
        # the play-out check and the loop below still decide on this box.
        log(f"networks {model} reused, no labels or training on this box")
    else:
        t1 = time.time()
        rng = random.Random(fight)
        spread = []
        room = spread_room(sl.slots, sixes[:5])
        while len(spread) < room:
            s = list(sl.team(rng.sample(sl.slots, 6)))
            if s not in sixes[:5] and s not in spread:
                spread.append(s)
        lab_dir = os.path.join(out_dir, "labels")
        metas = label(st, sixes[:5] + spread, boss_keys, flags, f"team:{fight}", lab_dir, procs=procs)
        log(f"labels: {sum(m['positions'] for m in metas)} positions from {sum(m['games'] for m in metas)} "
            f"fights in {time.time() - t1:.0f} s")
        t1 = time.time()
        base = without([fight], os.path.join(ROOT, "subsets", f"no-{fight}-team"))
        model = train(f"team-{fight}", [base, lab_dir])
        log(f"networks {model} trained in {time.time() - t1:.0f} s")
    cfg = {"value": model}

    t1 = time.time()
    finalists, tally, w = race(st, keys, boss_keys, flags, sixes, cfg, log=log, slots=sl)
    log(f"race in {time.time() - t1:.0f} s; finalists: " +
        "; ".join(f"{', '.join(names[k] for k in t)} ({tally.score(t):.2f} on {tally.numbers(t)['fights']})"
                  for t in finalists))
    log("member weights: " + ", ".join(f"{names[k]} {w[k]:.3f}" for k in sorted(w, key=lambda k: -w[k])))
    t1 = time.time()
    finalists, played = playoff(st, boss_keys, flags, finalists, tally, cfg, sl, procs=procs, log=log)
    log(f"play-off in {time.time() - t1:.0f} s; finalists: " + "; ".join(", ".join(names[k] for k in t) for t in finalists))
    results = []
    for t in finalists:
        real, unlucky, _rows = full_reading(st, boss_keys, flags, list(t), cfg, procs=procs)
        results.append((t, real, unlucky))
        log(f"finalist {', '.join(names[k] for k in t)}: real {real['won']:.1%} won, {real['faints']:.3f} faints, "
            f"{real['clean']:.1%} clean; very unlucky {unlucky['won']:.1%} won, {unlucky['faints']:.3f} faints")
    ours_net = None
    if mine:
        real, unlucky, _rows = full_reading(st, boss_keys, flags, mine, cfg, procs=procs)
        ours_net = {"real": real, "unlucky": unlucky}
        log(f"our six read the same way (its members with the screen's moves): real {real['won']:.1%} won, "
            f"{real['faints']:.3f} faints, {real['clean']:.1%} clean; the bar: {bar}")

    t1 = time.time()
    teams = [t for t, *_x in results] + ([tuple(mine)] if mine else [])
    po = read(st, boss_keys, flags, teams, check, {}, procs=procs, seed0=77)
    for t, real, _u in results:
        n = po.numbers(t)
        log(f"play-outs on {', '.join(names[k] for k in t)}: {n['won']:.1%} won, {n['faints']:.3f} faints, "
            f"{n['clean']:.1%} clean (the network: {real['won']:.1%}, {real['faints']:.3f})")
    ours_po = po.numbers(tuple(mine)) if mine else None
    if mine:
        log(f"play-outs on our six: {ours_po['won']:.1%} won, {ours_po['faints']:.3f} faints, "
            f"{ours_po['clean']:.1%} clean")
    log(f"play-out check in {time.time() - t1:.0f} s")
    top = ian_best([r[0] for r in results], po.numbers)
    best = next(r for r in results if r[0] == top)
    log(f"best finalist by the play-outs: {', '.join(names[k] for k in best[0])}; its faints fell to: "
        + str(losing_enemies(po.rows[tuple(best[0])])[:4]))
    t1 = time.time()
    win = list(improve(st, keys, boss_keys, flags, M, best[0], po, check, procs, log=log, slots=sl))
    log(f"winner by the play-outs after the loop ({time.time() - t1:.0f} s): {', '.join(names[k] for k in win)}; "
        f"{po.numbers(tuple(win))}; its faints fell to: " + str(losing_enemies(po.rows[tuple(win)])[:4]))

    # The winner's line: one fight on the trace seed by the play-out
    # planner, turn by turn, with the lead it chose and why.
    lead, vals = plplan.Planner(0).lead(st, win, boss_keys, flags)
    with open(os.path.join(out_dir, "line.txt"), "w") as fh:
        print(f"{fight}: {', '.join(names[k] for k in win)} with "
              + "; ".join(f"{names[k]} {', '.join(st['moves'][k])}" for k in win), file=fh)
        print("items: " + ", ".join(f"{names[k]} {it}" for k, it in fs.assign_items(st, win).items() if it), file=fh)
        print(f"lead {names[win[lead]]} (lead values: "
              + ", ".join(f"{names[k]} {v:+.2f}" for k, v in zip(win, vals)) + ")", file=fh)
        r = plplan.play(st, win, boss_keys, flags, lead, 30, {}, "real", log=fh)
        print(f"{'won' if r['won'] else 'lost'}; fainted: {', '.join(a for a, _b in r['faints']) or 'none'}",
              file=fh)
    summary = {"fight": fight, "key": key, "variant": variant, "foes": foes, "box": [names[k] for k in keys],
               "items": stock, "screen": [[names[k] for k in s] for s in sixes], "our_rank": rank,
               "moves": {names[k]: moves[k] for k in keys},
               "finalists": [{"six": [names[k] for k in t], "real": r, "unlucky": u, "playouts": po.numbers(t)}
                             for t, r, u in results],
               "ours": {"network": ours_net, "playouts": ours_po} if mine else None, "bar": bar,
               "winner": [names[k] for k in win], "winner_keys": list(win), "model": model, "playoff": played,
               "playouts_on_winner": po.numbers(tuple(win)),
               "winner_faints_to": losing_enemies(po.rows[tuple(win)]),
               # Every six the play-out check read, the loop's included.
               "checked": {", ".join(names[k] for k in t): po.numbers(t) for t in po.rows},
               "minutes": round((time.time() - t0) / 60, 1)}
    with open(os.path.join(out_dir, "result.json"), "w") as fh:
        json.dump(summary, fh, indent=1)
    log(f"== {fight} done in {(time.time() - t0) / 60:.0f} minutes")
    return summary

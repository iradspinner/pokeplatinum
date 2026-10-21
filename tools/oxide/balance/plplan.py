"""The planner: the scorer's step 3 under Ian's rulings of 2026-10-01 and
2026-10-02 (docs/oxide/trainer-scoring-handoff.md, "Ian's ruling on step 3").

The player's choices are made one at a time, as a player makes them: the
lead, each turn's action, and the replacement after a faint. Nothing here
names a plan. A choice is made by playing each option forward in the
simulator, at the game's real odds, and comparing where it leads:

- The trainer's AI is known exactly, so its choice distribution at a turn
  is computed from fightai itself: every chance() roll it makes is
  enumerated with its odds, and ties split evenly (ai_distribution).
- The option's turn is weighed exactly: every chance in it (the Quick Claw
  rolls, the trainer's choice, accuracy, crits, secondary effects, durations)
  is enumerated with its real odds (turn_outcomes). Of the 16 damage rolls,
  those that knock out count together and the rest fall in a few bands of
  like damage. Outcomes that leave a like position are merged.
- Each position the turn can reach is valued by playing the fight on from it
  (playout): to its end, by a plain policy whose judgement of an exchange is
  itself a short simulation (duel), at real odds, on dice keyed alike for
  every option so that options meet the same later luck. The end position
  is valued by its faints, a loss, and what HP the survivors keep (value).

    PYTHONPATH=. python3 -m tools.oxide.balance.plplan roark          # the three numbers
    PYTHONPATH=. python3 -m tools.oxide.balance.plplan roark --trace  # one run, turn by turn
"""
import argparse
import collections
import json
import math
import multiprocessing as mp
import os
import random
import sys
import time
import zlib

from . import plthreads  # noqa: F401  (one numpy thread per process, before numpy loads)
import numpy as np  # noqa: E402

from . import fightai
from . import fightsim as fs
from . import perfectline as pl

# ---- the value of a position -----------------------------------------------------------------

# A faint costs FAINT, since every loss narrows the run's later teams; a lost
# fight ends the run, so it costs LOSS on top of its faints. Each survivor's
# HP share adds HP_SHARE, a margin of safety between equal results. A
# play-out that reaches its turn cap unfinished counts the trainer's HP
# share left against the player at UNFINISHED.
FAINT = 1.0
LOSS = 10.0
HP_SHARE = 0.1
UNFINISHED = 2.0

# How the planner ranks its options (Ian, 2026-10-02): the chance of losing
# the fight first, then the faints expected, then the value above (which
# carries the survivors' HP). "A fight with 0% clean, 100% win and 1.00
# average faints means a single sacrifice wins every time, and I would take
# that every time over 90% clean, 90% win and 0.60 average deaths", since one
# unlucky turn there ends the run; a fixed weight of ten let a point of win
# rate trade for a tenth of a faint, which his order forbids. Options whose
# chance of losing is within LOSS_TOL of the lowest count as tied on it (the
# networks' estimate of that chance errs by 0.05 at Gardenia and 0.08 at
# Mars 1 on positions they never trained on), and among those, options
# within FAINT_TOL of the fewest faints count as tied on faints. RANK
# "value" restores the old ranking by the value alone, for comparison.
RANK = "win"
LOSS_TOL = 0.05
FAINT_TOL = 0.1
# Among options tied on both (within the tolerances), the faster finish
# first (Ian, 2026-10-02, to stop wasted turns): the one that takes the most
# of the trainer's HP this turn, read from the turn's outcomes the planner
# has already enumerated, so it costs no search. A stall that helps is never
# touched, since it would win more or lose fewer Pokemon than the tolerance.
# Only options whose value is also within FAST_EPS of the best of the tied
# count as genuine ties: with the tolerances alone, Roark over 2,000 fights
# fell from 97.9% clean and 0.022 faints to 89.5% and 0.115, because taking
# the most damage within them, turn after turn, gave up real safety. With
# FAST_EPS at 0.02 the showcase seed still wastes its turns (the network's
# values there differ by about 0.1 where play-outs call them equal), so the
# tie-break stays off by default (--fast-tie turns it on) until a setting
# keeps Roark's numbers at the bar's size. A window of 0.1 clears the
# showcase seed's wasted turns but reads Roark at 91.3% clean and 0.095
# faints over 2,000 fights (Barboach kept attacking into Cranidos), at half
# the turns and core time, so it does not pass Ian's condition either.
FAST_TIE = False
FAST_EPS = 0.02
# The learned stand-in player (plpolicy) that plays the play-outs in place of
# the plain policy, by name, or None for the plain policy (--standin).
STANDIN = None


def choose(q, parts, among):
    """The best of the options `among`, by Ian's order: parts[i] is option
    i's (chance of losing, faints expected[, the trainer's HP share taken
    this turn]), q[i] its value."""
    if RANK == "value" or parts is None:
        return max(among, key=lambda i: q[i])
    low = min(parts[i][0] for i in among)
    safe = [i for i in among if parts[i][0] <= low + LOSS_TOL]
    few = min(parts[i][1] for i in safe)
    tied = [i for i in safe if parts[i][1] <= few + FAINT_TOL]
    best = max(tied, key=lambda i: q[i])
    if FAST_TIE and len(parts[best]) > 2:
        even = [i for i in tied if q[i] >= q[best] - FAST_EPS]
        return max(even, key=lambda i: (round(parts[i][2], 3), q[i]))
    return best


def foe_left(b):
    """The trainer's HP left, as a share of its whole party's."""
    return sum(m.hp / m.maxhp for m in b.b.mons if m.alive()) / len(b.b.mons)


def ends(b):
    """A finished or stopped position's (faints, lost)."""
    return sum(1 for m in b.p.mons if not m.alive()), not b.p.alive()


def value(b):
    """The position's worth to the player at the end of a play-out."""
    alive = [m for m in b.p.mons if m.alive()]
    v = -FAINT * (len(b.p.mons) - len(alive)) + HP_SHARE * sum(m.hp / m.maxhp for m in alive)
    if not alive:
        return v - LOSS
    if b.b.alive():
        v -= UNFINISHED * sum(m.hp / m.maxhp for m in b.b.mons if m.alive()) / len(b.b.mons)
    return v


# ---- copies and random numbers -----------------------------------------------------------------

def clone(b):
    """A copy of the battle to play forward. perfectline's copy shares each
    Pokemon's list of moves the AI has seen, which a simulated turn appends
    to, so that list is copied here too."""
    c = fs.Battle.__new__(fs.Battle)
    c.__dict__.update(b.__dict__)
    c.p, c.b = _side(b.p), _side(b.b)
    c.log = []
    c.dice = c.rng = None
    return c


def _side(s):
    c = pl.clone_side(s)
    for m in c.mons:
        m.shown = list(m.shown)
    return c


_MASK = (1 << 64) - 1


def _mix(*parts):
    return zlib.crc32(":".join(str(x) for x in parts).encode())


class KeyedRandom(random.Random):
    """Random numbers fixed by a key, the battle's turn and the draw's place
    within that turn, rather than by their place in one long stream. Two
    positions played on with the same key then meet each later turn's luck
    alike (the same miss, the same roll on the same turn), where a single
    stream would drift apart after their first different draw. This cuts the
    noise between options without changing any odds."""

    def __init__(self, key, battle):
        super().__init__(0)
        self.key = key & _MASK
        self.battle = battle
        self.turn = None
        self.n = 0

    def _u64(self):
        t = self.battle.turn
        if t != self.turn:
            self.turn, self.n = t, 0
        self.n += 1
        x = (self.key * 0x9E3779B97F4A7C15 + t * 0xBF58476D1CE4E5B9 + self.n * 0x94D049BB133111EB) & _MASK
        x ^= x >> 30
        x = (x * 0xBF58476D1CE4E5B9) & _MASK
        x ^= x >> 27
        x = (x * 0x94D049BB133111EB) & _MASK
        return x ^ (x >> 31)

    def random(self):
        return (self._u64() >> 11) * (1.0 / 9007199254740992.0)

    def getrandbits(self, k):
        if k <= 64:
            return self._u64() >> (64 - k)
        return (self.getrandbits(k - 64) << 64) | self._u64()


# ---- one turn's outcomes, exactly ------------------------------------------------------------

# The damage rolls that do not knock out fall in at most this many bands of
# like damage; every roll that knocks out counts in one group of its own.
ROLL_BANDS = 3
# A turn is not split more ways than this; past it the remaining branches
# are left out and the rest weighed up to a whole.
BRANCH_CAP = 3000
# Positions after a turn are merged when they agree on everything but HP
# within a sixteenth of each Pokemon's maximum (a faint is never merged with
# a survivor).
HP_BUCKETS = 16


class EnumDice:
    """Dice that enumerate a turn: every chance is an event with its outcomes'
    real odds. The script answers the first events; each later one takes its
    first outcome and is recorded, so turn_outcomes can try the others."""
    mode = "run"
    luck = "real"
    one_crit = False

    def __init__(self, script, rng):
        self.script, self.rng = script, rng
        self.events, self.picked = [], []
        self.crit_used = False

    def _ev(self, probs):
        i = len(self.events)
        self.events.append(probs)
        o = self.script[i] if i < len(self.script) else 0
        self.picked.append(o)
        return o

    def _yes(self, p):
        if p <= 0:
            return False
        if p >= 1:
            return True
        return self._ev((1 - p, p)) == 1

    def bad(self, kind, p):
        return self._yes(p)

    def good(self, p, kind=None):
        return self._yes(p)

    def lands_on_player(self, kind, p):
        return self._yes(p)

    def roll(self, top):
        return self._ev((1 / 16,) * 16)

    def roll_grouped(self, damage, hp):
        """A damage roll, its 16 rolls grouped: those that knock out, then
        bands of like damage among the rest; each group stands for itself
        by its middle roll."""
        dmg = [damage(r) for r in range(16)]
        groups = []
        kills = [r for r in range(16) if dmg[r] >= hp]
        if kills:
            groups.append(kills)
        rest = [r for r in range(16) if dmg[r] < hp]
        values = sorted({dmg[r] for r in rest})
        if len(values) <= ROLL_BANDS:
            groups += [[r for r in rest if dmg[r] == v] for v in values]
        else:
            n = len(rest)
            cuts = [round(n * k / ROLL_BANDS) for k in range(ROLL_BANDS + 1)]
            groups += [rest[cuts[k]:cuts[k + 1]] for k in range(ROLL_BANDS) if cuts[k + 1] > cuts[k]]
        if len(groups) == 1:
            g = groups[0]
        else:
            g = groups[self._ev(tuple(len(x) / 16 for x in groups))]
        return g[len(g) // 2]

    def pick_weighted(self, items, weights):
        tot = sum(weights)
        return items[self._ev(tuple(w / tot for w in weights))]

    def crit_count(self, n, p):
        """How many of a move's n hits land critical, each at p
        (perfectline.crit_hits): one event at the binomial odds."""
        if p >= 1:
            return n
        return self._ev(tuple(math.comb(n, k) * p ** k * (1 - p) ** (n - k) for k in range(n + 1)))

    def sleep(self, side):
        return 1 + self._ev((0.25,) * 4)

    def confusion(self, side):
        return 2 + self._ev((0.25,) * 4)

    def taunt(self, side):
        return 3 + self._ev((1 / 3,) * 3)

    def bind(self, side):
        return 3 + self._ev((0.25,) * 4)

    def outrage(self, side):
        return 2 + self._ev((0.5, 0.5))

    def thaws(self, mon):
        return self._yes(0.2)

    def tie_player_first(self):
        return self._yes(0.5)

    def choice(self, kind, n):
        return self._ev((1 / n,) * n) if n > 1 else 0

    def confusion_roll(self):
        return 85 + self._ev((1 / 16,) * 16)


def turn_outcomes(c0, a, aa, key):
    """[(position, probability)] after the player's `a` against the
    trainer's `aa` from c0, over every chance in the turn, positions that
    agree merged (merge_key)."""
    raw, stack = [], [()]
    while stack and len(raw) < BRANCH_CAP:
        script = stack.pop()
        c = clone(c0)
        d = EnumDice(script, random.Random(_mix(key, len(raw))))
        c.dice, c.rng = d, d.rng
        pl._turn(c, a, aa)
        prob = 1.0
        for probs, o in zip(d.events, d.picked):
            prob *= probs[o]
        raw.append((c, prob))
        for i in range(len(script), len(d.events)):
            for o in range(1, len(d.events[i])):
                if d.events[i][o] > 0:
                    stack.append(script + (0,) * (i - len(script)) + (o,))
    total = sum(p for _c, p in raw)
    merged = {}
    for c, p in raw:
        k = merge_key(c)
        if k in merged:
            rep, q = merged[k]
            merged[k] = (rep if q >= p else c, q + p)
        else:
            merged[k] = (c, p)
    return [(c, p / total) for c, p in merged.values()]


def merge_key(c):
    """What tells two positions a turn reaches apart, so that only like
    ones merge: each side's Pokemon by an HP band and every other state its
    key holds (perfectline.mon_key), the side's conditions, and the field.
    The side conditions and field states most fights never have are kept
    out of the key while they are not there, as perfectline's state_key
    keeps them: Aurora Veil, and since 2026-10-15 Lucky Chant's turns and
    Sticky Web on a side, and Gravity's and Magic Room's turns, Copycat's
    last move and deep fog on the field, which the batches added to the
    battle and this key had left out, so positions that differed only by
    them merged (Ian approved the fix); and since 2026-10-20 the Pokemon
    states mon_key gained (Ingrain, Aqua Ring, a trap's holder, a lit
    Flash Fire, Rollout's count, Defense Curl, Rage and Truant's loafing,
    Ian approved)."""
    def side(s):
        key = (s.active, tuple(((m.hp * HP_BUCKETS + m.maxhp - 1) // m.maxhp,) + pl.mon_key(m)[1:]
                               for m in s.mons),
               tuple(s.screens.values()), s.tailwind, tuple(s.hazards.values()), s.safeguard,
               getattr(s, "wish", 0), s.future, s.future_sight, getattr(s, "mist", 0))
        if s.aurora_veil:
            key += (s.aurora_veil,)          # Aurora Veil, out of the key while down
        if s.lucky_chant or s.web:
            key += (("lucky chant", s.lucky_chant, "web", s.web),)
        return key
    key = (side(c.p), side(c.b), c.weather, c.weather_turns, c.trick_room)
    if c.gravity or c.last_move is not None or c.magic_room or c.fog or c.wonder_room:
        key += pl._field_extra(c)            # Gravity, Copycat's last move, Magic Room, Wonder Room, deep fog
    return key


def quick_outcomes(b):
    """[(Quick Claw rolls, probability)] for the turn: each holder on the
    field fires one time in five, drawn before anyone chooses."""
    out = [({}, 1.0)]
    for m in (b.p.cur(), b.b.cur()):
        if fs.custap_fires(m, b):
            out = [(dict(q, **{m.key: True}), p) for q, p in out]      # a Custap Berry that fires
        elif m.item == "Quick Claw":
            out = [(dict(q, **{m.key: f}), p * (0.2 if f else 0.8)) for q, p in out for f in (False, True)]
        else:
            out = [(dict(q, **{m.key: False}), p) for q, p in out]
    return out


# ---- the trainer's choice, exactly ---------------------------------------------------------------

class _Script:
    """Answers to fightai.chance: the script's answers first, then "no" to
    every later roll, each roll's odds recorded."""

    def __init__(self, script):
        self.script = script
        self.asked = []

    def roll(self, p):
        i = len(self.asked)
        self.asked.append(p)
        return self.script[i] if i < len(self.script) else False


_SCRIPT = None
_chance = fightai.chance


def _scripted_chance(b, p):
    if _SCRIPT is not None:
        return _SCRIPT.roll(p)
    return _chance(b, p)


fightai.chance = _scripted_chance

# A function whose rolls branch more ways than this is not enumerated.
ENUM_CAP = 20000


def outcomes(fn):
    """[(fn(), probability)] over every outcome of the chance() rolls fn
    makes, each roll true at its own odds. fn must draw nothing else."""
    global _SCRIPT
    out, stack, runs = [], [()], 0
    while stack:
        script = stack.pop()
        runs += 1
        if runs > ENUM_CAP:
            raise RuntimeError(f"more than {ENUM_CAP} roll outcomes to enumerate")
        _SCRIPT = s = _Script(script)
        try:
            r = fn()
        finally:
            _SCRIPT = None
        prob = 1.0
        for i, p in enumerate(s.asked):
            q = min(max(p / 100.0, 0.0), 1.0)
            prob *= q if (script[i] if i < len(script) else False) else 1.0 - q
        if prob > 0:
            out.append((r, prob))
        # Every roll past the script was answered "no"; each is tried "yes"
        # in turn, with the rolls before it kept at "no".
        for i in range(len(script), len(s.asked)):
            if s.asked[i] > 0:
                stack.append(script + (False,) * (i - len(script)) + (True,))
    return out


def pick_odds(dists):
    """Each slot's chance of being picked when every slot's score is drawn
    from its own distribution ({score: probability}) and the highest score
    wins, ties at random (fightai.choose)."""
    out = []
    for i, di in enumerate(dists):
        total = 0.0
        for s, p in di.items():
            # poly[k]: the chance that exactly k other slots tie at s and
            # none scores higher.
            poly = [1.0]
            for j, dj in enumerate(dists):
                if j == i:
                    continue
                lt = sum(q for s2, q in dj.items() if s2 < s)
                eq = dj.get(s, 0.0)
                nxt = [0.0] * (len(poly) + 1)
                for k, cf in enumerate(poly):
                    nxt[k] += cf * lt
                    nxt[k + 1] += cf * eq
                poly = nxt
            total += p * sum(cf / (k + 1) for k, cf in enumerate(poly))
        out.append(total)
    return out


class Store:
    """A bounded cache keyed by a compact fingerprint of a large key: two
    independent hashes of it (the key's own and its reverse order's), so the
    large tuple itself is never kept. A fingerprint whose second hash
    disagrees counts as a miss. It holds at most `cap` entries and empties
    itself when full or when the fight changes (`reset`)."""

    def __init__(self, cap):
        self.cap = cap
        self.d = {}

    def get(self, key):
        h = hash(key)
        got = self.d.get(h)
        if got is not None and got[0] == hash(key[::-1]):
            return got[1]
        return None

    def put(self, key, value):
        if len(self.d) >= self.cap:
            self.d.clear()
        self.d[hash(key)] = (hash(key[::-1]), value)
        return value

    def clear(self):
        self.d.clear()


# The AI's exact choice odds by position: about 300 bytes an entry.
_ODDS = Store(100000)


def reset():
    """Empty every per-fight cache: at the start of each fight and whenever
    the fight's prepared state changes."""
    _ODDS.clear()
    _DUELS.clear()


_ODDS_ST = None


def _odds(b, u, t):
    """The AI's exact choice odds at this state, [((kind, what), p)], cached
    by a fingerprint of what it reads (perfectline.ai_key). Only the odds are
    kept: the trees that give them are dropped once read. Like
    fightai.choose, it records the player's last move as seen."""
    global _ODDS_ST
    if _ODDS_ST is not b.st:
        reset()
        _ODDS_ST = b.st
    k = pl.ai_key(b)
    fightai.record_last_move(t)
    got = _ODDS.get(k)
    if got is None:
        got = _ODDS.put(k, _build(b, u, t))
    return got


def _build(b, u, t):
    saved = b.rng
    b.rng = None             # any draw not made through chance() fails loudly
    try:
        side = fightai._side(b, u)
        dist = collections.defaultdict(float)
        stay = 0.0
        for r, p in outcomes(lambda: fightai.should_switch(b, side, u, t)):
            if r is None:
                stay += p
            else:
                dist[("switch", r)] += p
        if stay > 0:
            fixed = fightai.fixed_move(b, u)
            if fixed is not None:
                dist[("move", fixed[1].name)] += stay
            else:
                figs = [fightai.figure(b, u, t, m) for m in u.moves]
                best = max((f for f in figs if f is not None), default=None)
                dists = []
                for i in range(len(u.moves)):
                    d = collections.defaultdict(float)
                    for s, p in outcomes(lambda i=i: fightai.score_slot(b, u, t, i, figs, best, b.ai_flags)):
                        d[s] += p
                    dists.append(d)
                for i, p in enumerate(pick_odds(dists)):
                    if p > 1e-12:
                        dist[("move", u.moves[i].name)] += stay * p
    finally:
        b.rng = saved
    return tuple(sorted(dist.items(), key=lambda x: -x[1]))


def _action(u, kind, what):
    if kind == "switch":
        return "switch", what
    if what == "Struggle":
        return "move", fs.move("Struggle")
    return "move", next(m for m in u.moves if m.name == what)


def ai_distribution(b):
    """The trainer's choices at this state with their exact odds:
    [(('move', Move) or ('switch', index), probability)], most likely
    first. The turn's Quick Claw rolls (b.quick) must already be set, since
    the AI reads them."""
    u, t = b.b.cur(), b.p.cur()
    forced = fightai.forced_choice(u)
    if forced is not None:
        return [(forced, 1.0)]
    return [(_action(u, kind, what), p) for (kind, what), p in _odds(b, u, t)]


# ---- the player's options, and the play-out's plain policy ---------------------------------------

def would_fail(b, me, foe, mv):
    """Whether the player's move would fail or do nothing in this position
    by the battle's own rules, which rules it out of the options. The
    trainer's AI's Basic check (fightai.basic) reads most such cases from
    the battle as it stands, the player's Pokemon and the trainer's as they
    are (a status on a target that has one, a screen up already, a target
    immune to the move), and is asked first, as it is cheap; a move it
    scores -8 or below is ruled out only when that score is the battle's
    rule and not the AI's own preference (still_works). Until 2026-10-15
    every move Basic scored -8 or below was ruled out, those it merely
    discourages too, so the player was never offered Healing Wish, nor
    Knock Off on a target with no item (Ian approved the fix)."""
    if fightai.basic(b, me, foe, mv, fightai.figure(b, me, foe, mv)) > -8:
        return False
    if fightai._basic_entry(b, me, foe, mv) is not None:
        return True          # an immune target, an absorbing ability, Soundproof, Bulletproof, Prankster on a Dark type
    return not still_works(b, me, foe, mv)


def _changes(u, t, stats):
    """Whether swapping or copying these stages between u and t changes any."""
    return any(u.stages[k] != t.stages[k] for k in stats)


def still_works(b, u, t, mv):
    """For a move Basic scores -8 or below past its entry checks: whether it
    would still do something by the battle's own rules, the score being
    one of the AI's preferences. Those let through: Explosion with the
    user's last Pokemon; Knock Off, which hits whether or not there is an
    item to take; Upper Hand while the target knows a priority move it has
    not shown; a raise of several stats while one of them can still rise,
    and a Speed raise or drop under Trick Room or against Speed Boost; Take
    Heart with a status or a stat that can rise; Haze where it changes a
    stage or ends a Focus Energy; Psych Up, Heart Swap, Power Swap and
    Guard Swap where they change a stage; poison and
    a burn on a Magic Guard or Poison Heal holder, or a Hydration holder
    in rain, which still land; Swagger and Flatter on an Own Tempo or
    safeguarded target, which still raise its stat; a non-Ghost Curse while
    a stat can still change; Perish Song while its user has no count yet;
    Memento and Tickle while one of their stats can still fall, Memento
    with the user's last Pokemon too; Future Sight while only the user's
    own side has one waiting; Trick with an item to hand over; Imprison
    while a foe shares a move; Healing Wish and Lunar Dance while a bench
    Pokemon has something to mend; Tailwind and Trick Room whatever their
    effect on speed; Acupressure while a stage can rise; a second Power
    Trick, which swaps the stats back; Gastro Acid on an ability that can
    be suppressed; Worry Seed on a sleeping target; and Copycat whenever
    a move it can copy has been or may be used before it. Everything else
    Basic rules out, it rules out by the battle's rules: a status already
    there, a screen up, a stat at its limit, a hazard laid in full or with
    no one left to meet it, a move that fails outright."""
    e, c = mv.effect, mv.const
    own, foe = (b.p, b.b) if u.side == "p" else (b.b, b.p)
    mold = fightai.mold(u, t)
    ab = t.ability
    if mv.cat != "Status":
        if e == "HALVE_DEFENSE":         # with the user's last Pokemon: the AI's rule, not the battle's
            return mold or not any(m.alive() and m.ability == "Damp" for m in b.p.on_field() + b.b.on_field())
        if e == "REMOVE_HELD_ITEM":      # Knock Off hits whatever the target holds
            return True
        if e == "UPPER_HAND":            # it lands if the target uses a priority move, shown or not
            return any(fs.move_priority(t, m) > 0 for m in t.moves)
        return False
    # Basic_CheckPowderImmunity and Basic_CheckSapSipper, the battle's own rules.
    if c in fightai.BASIC_POWDERS and ("Grass" in t.types or (not mold and ab == "Overcoat")):
        return False
    if (c in fightai.BASIC_POWDERS or c in fightai.GRASS_STATUS) and not mold and ab == "Sap Sipper" \
            and mv.type == "Grass":
        return False
    if e in fightai.RAISES:
        first, rest, _room = fightai.RAISES[e]
        stats = (first,) + tuple(rest)
        if e == "RAISE_ALL_STATS_LOSE_THIRD_MAX_HP" and u.hp <= u.maxhp // 3:
            return False                 # fightsim.clangorous_soul
        if e == "ATK_SP_ATK_SPEED_UP_2_LOSE_HALF_MAX_HP" and u.hp <= u.maxhp // 2:
            return False
        return any(u.stages[k] < 6 for k in stats)
    if e == "TAKE_HEART":
        return bool(u.status) or u.stages["spa"] < 6 or u.stages["spd"] < 6
    if e in fightai.LOWERS:
        k = fightai.LOWERS[e]
        # Under Trick Room and against Speed Boost a Speed drop is the AI's
        # preference; every other -10 there is a block or a stage at -6.
        return k == "spe" and t.stages["spe"] > -6 and fightai._clear_body(b, u, t) == 0
    if e == "RESET_STAT_CHANGES":
        # Haze ends a Focus Energy too (fightsim.reset_all_stats).
        return any(v for m in (u, t) for v in m.stages.values()) or bool(u.crit_stage or t.crit_stage)
    if e in ("COPY_STAT_CHANGES", "SWAP_STAT_CHANGES"):
        return _changes(u, t, fs.STAGE_KEYS) and not (e == "SWAP_STAT_CHANGES" and fs.sub_blocks(u, t, mv))
    if e == "SWAP_ATK_SP_ATK_STAT_CHANGES":
        return _changes(u, t, ("atk", "spa"))
    if e == "SWAP_DEF_SP_DEF_STAT_CHANGES":
        return _changes(u, t, ("def", "spd"))
    if e in ("STATUS_POISON", "STATUS_BADLY_POISON", "STATUS_BURN"):
        # Basic refuses a Magic Guard, Poison Heal or rain-time Hydration
        # holder; the status lands on each all the same (fightsim.can_status).
        saved, b.status_src = getattr(b, "status_src", None), u
        try:
            return fs.can_status(b, t, "brn" if e == "STATUS_BURN" else "psn") and not fs.leaf_guarded(b, t)
        finally:
            b.status_src = saved
    if e in ("ATK_UP_2_STATUS_CONFUSION", "SP_ATK_UP_CAUSE_CONFUSION"):
        # Own Tempo or Safeguard stops the confusion, not the stat's rise.
        return t.stages["atk" if e == "ATK_UP_2_STATUS_CONFUSION" else "spa"] < 6 and not fs.sub_blocks(u, t, mv)
    if e == "CURSE":
        return "Ghost" not in u.types and (u.stages["atk"] < 6 or u.stages["def"] < 6 or u.stages["spe"] > -6)
    if e == "ALL_FAINT_3_TURNS":
        return not u.perish
    if e == "FAINT_AND_ATK_SP_ATK_DOWN_2":
        if not mold and ab in ("Clear Body", "White Smoke"):
            return False
        return (t.stages["atk"] > -6 or t.stages["spa"] > -6) and not fs.sub_blocks(u, t, mv)
    if e == "ATK_DEF_DOWN":
        if not mold and ab in ("Clear Body", "White Smoke"):
            return False
        return t.stages["atk"] > -6 or t.stages["def"] > -6
    if e == "HIT_IN_3_TURNS":
        return not getattr(foe, "future_sight", False)
    if e == "SWITCH_HELD_ITEMS":
        if (ab == "Sticky Hold" and not mold) or fs.sub_blocks(u, t, mv) or u.knocked_off or t.knocked_off:
            return False
        return u.side == "p" and bool(u.item or t.item) and "Multitype" not in (u.ability, ab) \
            and "Griseous Orb" not in (u.item, t.item)
    if e == "MAKE_SHARED_MOVES_UNUSEABLE":
        mine = {m.name for m in u.moves}
        return not u.imprisoning and any(m.name in mine for f in foe.on_field() for m in f.moves)
    if e in ("FAINT_AND_FULL_HEAL_NEXT_MON", "FAINT_FULL_RESTORE_NEXT_MON"):
        lunar = e == "FAINT_FULL_RESTORE_NEXT_MON"
        return any(m.hp < m.maxhp or m.status or (lunar and any(m.pp.get(x.name, x.pp) < x.pp for x in m.moves))
                   for m in own.bench())
    if e == "DOUBLE_SPEED_3_TURNS":
        return not own.tailwind
    if e == "RANDOM_STAT_UP_2":
        return any(v < 6 for v in u.stages.values())
    if e == "SWAP_ATK_DEF":
        return True
    if e == "SUPRESS_ABILITY":
        return not getattr(t, "suppressed", False) and not fs.refuses(fs.raw_ability(t), "suppress") \
            and t.item != "Ability Shield"
    if e == "SET_ABILITY_TO_INSOMNIA":
        return ab not in ("Truant", "Insomnia", "Vital Spirit", "Multitype")
    if e == "TRICK_ROOM":
        return b.trick_room < 999
    if e in fs.WEATHER_OF:
        return b.weather != fs.WEATHER_OF[e] and not fs.weather_move_fails(b, e)
    if e == "USE_LAST_USED_MOVE":
        return copycat_works(b, u, t, mv)
    return False


def copycat_works(b, u, t, mv):
    """Whether Copycat can copy anything this turn: the battle's last move
    (b.last_move) as it stands, if it is one Copycat copies, or a move the
    target may use before it, one of higher priority or of Copycat's own
    from a target no slower (fightsim.called_move's rules)."""
    def copyable(m):
        return m is not None and m.const not in fs.INVOKERS and fs.metronome_callable(b, u, m)
    if copyable(b.last_move):
        return True
    p = fs.move_priority(u, mv)
    return any(copyable(m) and (fs.move_priority(t, m) > p or (fs.move_priority(t, m) == p
                                                               and not fs.moves_first(b, u, t)))
               for m in t.moves)


def options(b):
    """The player's options: each move with PP that would do something
    (would_fail rules out one that would fail or do nothing by the battle's
    own rules), and each switch to a living bench member."""
    me, foe = b.p.cur(), b.b.cur()
    forced = fightai.forced_choice(me)
    if forced is not None:
        return [forced]
    out = []
    saved = b.rng
    b.rng = saved or random.Random(0)
    try:
        for mv in me.moves:
            if me.pp.get(mv.name, 1) <= 0 or (me.taunt and mv.cat == "Status") or fs.tormented_out(me, mv) \
                    or fs.move_heal_blocked(me, mv) or fs.disabled_out(me, mv) \
                    or ((me.rare or b.gravity) and fs.move_barred(b, me, mv)):
                continue
            if me.choice and mv.name != me.choice:
                continue
            if me.encore is not None and mv.name != me.encore:
                continue                 # Encore leaves the one move to choose
            if would_fail(b, me, foe, mv):
                continue
            out.append(("move", mv))
    finally:
        b.rng = saved
    if not out:
        left = [m for m in me.moves if me.pp.get(m.name, 1) > 0 and not fs.tormented_out(me, m)
                and not fs.disabled_out(me, m) and (me.encore is None or m.name == me.encore)]
        out.append(("move", left[0] if left else fs.move("Struggle")))
    if not fs.trapped(b, me):
        out += [("switch", i) for i, m in enumerate(b.p.mons) if i != b.p.active and m.alive()]
    return out


def option_slot(b, a):
    """An option's place among the stand-in player's ten slots: a move by its
    place in the active Pokemon's set (0 to 3), a switch by its target's
    place on the bench as plfeat lists it, the active Pokemon left out (4 to
    8), so the slot means the same thing as the features it is read from."""
    me = b.p.cur()
    if a[0] == "move":
        return next((k for k, m in enumerate(me.moves) if m is a[1] or m.name == a[1].name), 0)
    bench = [i for i in range(len(b.p.mons)) if i != b.p.active]
    return 4 + bench.index(a[1])


class ModeDice:
    """Every chance at its likeliest outcome, for a duel: a check above even
    odds passes, one below fails, the middle damage roll, no crit."""
    mode = "run"
    luck = "real"
    one_crit = False
    crit_used = False

    def __init__(self):
        self.rng = random.Random(0)

    def bad(self, kind, p):
        return p > 0.5

    def good(self, p, kind=None):
        return p > 0.5

    def lands_on_player(self, kind, p):
        return p > 0.5

    def roll(self, top):
        return 7

    def pick_weighted(self, items, weights):
        return items[weights.index(max(weights))]

    def sleep(self, side):
        return 2

    def confusion(self, side):
        return 3

    def taunt(self, side):
        return 4

    def bind(self, side):
        return 4

    def outrage(self, side):
        return 2

    def thaws(self, mon):
        return False

    def tie_player_first(self):
        return False

    def choice(self, kind, n):
        return 0

    def confusion_roll(self):
        return 92


DUEL_TURNS = 8


def strongest(b):
    """The active Pokemon's attack with the most expected damage that cannot
    faint its user, else its first move with PP."""
    me, foe = b.p.cur(), b.b.cur()
    forced = fightai.forced_choice(me)
    if forced is not None:
        return forced
    mv, d = fs.safe_attack(b, me, foe)
    if mv is not None and d > 0:
        return "move", mv
    left = [m for m in me.moves if me.pp.get(m.name, 1) > 0 and not fs.tormented_out(me, m)
            and not fs.disabled_out(me, m)]
    return "move", left[0] if left else fs.move("Struggle")


def likeliest(c):
    """The trainer's likeliest choice at c, with no Quick Claw fired."""
    c.quick = {}
    return ai_distribution(c)[0][0]


# Duel results by exact position: about 150 bytes an entry.
_DUELS = Store(200000)
_DUELS_ST = None


def duel(b, idx=None, entry=False):
    """duel_at, remembered by a fingerprint of the exact position: every
    play-out from one position opens with the same duels."""
    global _DUELS_ST
    if _DUELS_ST is not b.st:
        reset()
        _DUELS_ST = b.st
    k = (pl.state_key(b), pl._ai_mon(b.p.cur()), pl._ai_mon(b.b.cur()), b.turn == 0, idx, entry)
    got = _DUELS.get(k)
    if got is None:
        got = _DUELS.put(k, duel_at(b, idx, entry))
    return got


def duel_at(b, idx=None, entry=False):
    """The player's Pokemon idx (the active one by default) and the trainer's
    active Pokemon fighting it out in the simulator at the likeliest dice:
    the player's side using its strongest attack, the trainer its AI's
    likeliest pick. With `entry`, idx comes in on a switch and takes the
    trainer's pick first. (won, its HP share left or -1 if it fainted, the
    trainer's HP share left); won is the trainer's Pokemon fainting or
    leaving first. Healing, drain, stat drops and abilities all happen in
    the simulation, which a damage formula would miss."""
    c = clone(b)
    c.dice, c.rng = ModeDice(), random.Random(0)
    c.in_duel = True
    if idx is not None and idx != c.p.active:
        if entry:
            pl._turn(c, ("switch", idx), likeliest(c))
        else:
            fs.switch_in(c, c.p, idx)
    mine = c.p.active if idx is None or not entry else idx
    me = c.p.mons[mine]
    foe_i = c.b.active
    foe = c.b.mons[foe_i]
    for _ in range(DUEL_TURNS):
        if not me.alive() or not foe.alive() or c.p.active != mine or c.b.active != foe_i:
            break
        aa = likeliest(c)
        if aa[0] == "switch":
            break
        pl._turn(c, strongest(c), aa)
    left = me.hp / me.maxhp if me.alive() else -1.0
    theirs = foe.hp / foe.maxhp if foe.alive() else 0.0
    won = me.alive() and (not foe.alive() or c.b.active != foe_i)
    return won, left, theirs


def _duel_key(r):
    won, left, theirs = r
    return (won, left - theirs)


PLAIN_SWITCHES = 2


def plain(b):
    """The play-out's policy, deliberately plain: a knockout this turn that
    the foe cannot answer first; else, when a matchup first forms and its
    duel says this Pokemon faints first, a switch to the bench member whose
    duel, after taking the foe's pick on the way in, goes best and is won;
    else the strongest attack."""
    me, foe = b.p.cur(), b.b.cur()
    forced = fightai.forced_choice(me)
    if forced is not None:
        return forced
    first = fs.moves_first(b, me, foe)
    attacks = [m for m in me.moves if m.damaging() and me.pp.get(m.name, 1) > 0
               and (not me.choice or m.name == me.choice) and m.effect not in fs.SELF_KO
               and not fs.tormented_out(me, m) and not fs.disabled_out(me, m)]
    for m in sorted(attacks, key=lambda m: -m.pri):
        if (m.acc == 0 or m.acc >= 90) and pl.dmg_low(b, me, foe, m) >= foe.hp and (m.pri > 0 or first):
            return "move", m
    pair = (me.key, foe.key)
    if getattr(b, "pair", None) != pair:
        b.pair = pair
        if getattr(b, "plain_switches", 0) < PLAIN_SWITCHES and not fs.trapped(b, me) \
                and b.p.bench():
            won, left, _t = duel(b)
            if not won and left < 0:
                best = None
                for i, m in enumerate(b.p.mons):
                    if i != b.p.active and m.alive():
                        r = duel(b, i, entry=True)
                        if r[0] and (best is None or _duel_key(r) > best[0]):
                            best = (_duel_key(r), i)
                if best is not None:
                    b.plain_switches = getattr(b, "plain_switches", 0) + 1
                    return "switch", best[1]
    return strongest(b)


def plain_replacement(b):
    """The play-out's replacement after a faint: the bench member whose duel
    with the trainer's Pokemon goes best."""
    cands = [i for i, m in enumerate(b.p.mons) if m.alive() and i != b.p.active]
    if not cands:
        return None
    if len(cands) == 1 or getattr(b, "in_duel", False):
        return cands[0]
    return max(cands, key=lambda i: _duel_key(duel(b, i)))


# ---- the planner ---------------------------------------------------------------------------------

PLAYOUT_TURNS = 80   # a play-out stops this many turns on
TURN_CAP = 150       # the harness's cap on a fight
PLAYOUTS = 1         # play-outs per position after the turn, without a budget
# With a budget, options are weighed in stages: every option gets each of
# these budgets in turn, and one trailing the leader by more than RACE_Z
# standard errors of the difference is dropped before the next.
# Budget 64 for every play-out reading (Ian, 2026-10-03): at Roark, Mars 1
# and Gardenia it chose about as well as 192 at a quarter to a third of the
# cost (the handoff's "The learned stand-in player, and smaller budgets").
BUDGET = 64
STAGES = (24, 64)
RACE_Z = 2.0


def _var(v):
    m = sum(v) / len(v)
    return sum((x - m) ** 2 for x in v) / (len(v) - 1)


def _name(a, b):
    if a[0] == "move":
        return a[1].name
    return "switch to " + b.p.mons[a[1]].species


_NETS = {}       # trained networks by name, loaded once per process
_TABLES = {}     # plfeat's tables for the fight in hand


class Planner:
    """One run's player."""

    def __init__(self, seed, playouts=PLAYOUTS, budget=BUDGET, value=None, standin=None):
        self.seed = seed
        self.playouts = playouts
        # The learned stand-in player that plays this planner's play-outs (a
        # plpolicy network's name), or the module's STANDIN when not given,
        # so a check can hold planners with and without one side by side.
        self.standin = standin or STANDIN
        # With a budget, each option's turn against each trainer pick gets
        # this many play-outs in all, shared among the turn's outcomes by
        # their probability (at least one each), rather than `playouts` for
        # every outcome however unlikely.
        self.budget = budget
        # With `value`, a trained network's name (plvalue), the positions the
        # turn can reach are valued by the network instead of by play-outs.
        self.net = None
        if value:
            from . import plvalue
            self.net = _NETS.get(value) or _NETS.setdefault(value, plvalue.Value(value))
        self.decisions = 0
        self.notes = []          # per decision: what was weighed and chosen
        # With `record` set to a list, every position the play-outs value is
        # kept in it with their results, as training labels (keep).
        self.record = None
        self.last_end = None     # the last play-out's final position
        self.last_parts = None   # the last weighing's (chance of losing, faints) per option
        self.choices = None      # with a list: every decision kept for the stand-in player (record_choice)

    def tables(self, b):
        """plfeat's per-fight tables for b's fight, made once per fight."""
        from . import plfeat
        k = id(b.st)
        got = _TABLES.get(k)
        if got is None or got[0] is not b.st:
            _TABLES.clear()
            got = _TABLES[k] = (b.st, plfeat.Fight(b.st, [m.key for m in b.p.mons], [m.key for m in b.b.mons]))
        return got[1]

    def net_values(self, positions):
        """The network's value of each position, in one batch."""
        return [v for v, _f, _p in self.net_heads(positions)]

    def net_heads(self, positions):
        """The network's (value, faints still to come, chance of losing) for
        each position, in one batch."""
        from . import plfeat
        if not positions:
            return []
        fight = self.tables(positions[0])
        feats = [plfeat.features(c, fight) for c in positions]
        v, f, p = self.net.heads(np.stack([f for f, _i in feats]), np.stack([i for _f, i in feats]))
        return list(zip(v, f, p))

    def q(self, b, acts, key):
        """Each option's expected value: over the turn's Quick Claw rolls,
        the trainer's exact choice odds and every chance in the turn, each
        position reached valued by playing on from it. With a budget, an
        option that is clearly behind is dropped early (weigh)."""
        return self.weigh(b, acts, key)[0]

    def weigh(self, b, acts, key):
        """(each option's value, the options still in the running at the
        end). Every option's turn is enumerated once; its outcomes are then
        played on in stages (STAGES, then the full budget), each stage
        reusing the play-outs of the last. After each stage an option whose
        value trails the leader's by more than RACE_Z standard errors of the
        difference is dropped, so only close options get the full budget."""
        cells = [[] for _ in acts]
        for quick, pq in quick_outcomes(b):
            c0 = clone(b)
            c0.quick = quick
            for aa, pa in ai_distribution(c0):
                for i, a in enumerate(acts):
                    for c, p in turn_outcomes(c0, a, aa, key):
                        done = not c.p.alive() or not c.b.alive()
                        cells[i].append({"w": pq * pa * p, "p": p, "c": c, "done": done,
                                         "v": [value(c)] if done else [], "e": [ends(c)] if done else []})
        if self.net is not None:
            # Every position the turn can reach, valued by the network in one
            # batch (its value, the faints still to come and the chance of
            # losing); a finished fight keeps its own.
            open_cells = [cell for cs in cells for cell in cs if not cell["done"]]
            for cell, (v, f, pl_) in zip(open_cells, self.net_heads([cell["c"] for cell in open_cells])):
                cell["v"] = [float(v)]
                cell["e"] = [(ends(cell["c"])[0] + float(f), float(pl_))]
            self.last_parts = self.parts(cells, foe_left(b))
            return [sum(cell["w"] * cell["v"][0] for cell in cs) for cs in cells], list(range(len(acts)))
        alive = list(range(len(acts)))
        stages = [s for s in STAGES if self.budget and s < self.budget] + [self.budget]
        est = {}
        for k, s in enumerate(stages):
            for i in alive:
                for cell in cells[i]:
                    if cell["done"]:
                        continue
                    n = self.playouts if s is None else max(1, round(s * cell["p"]))
                    while len(cell["v"]) < n:
                        cell["v"].append(self.playout(clone(cell["c"]), _mix(key, len(cell["v"]))))
                        cell["e"].append(ends(self.last_end))
            spreads = [_var(cell["v"]) for i in alive for cell in cells[i] if len(cell["v"]) > 1]
            pooled = sum(spreads) / len(spreads) if spreads else 1.0
            for i in alive:
                mean = sum(cell["w"] * sum(cell["v"]) / len(cell["v"]) for cell in cells[i])
                var = sum(cell["w"] ** 2 * (0 if cell["done"] else
                                            (_var(cell["v"]) if len(cell["v"]) > 1 else pooled) / len(cell["v"]))
                          for cell in cells[i])
                est[i] = (mean, var)
            if k == len(stages) - 1 or len(alive) == 1:
                break
            lead = max(alive, key=lambda i: est[i][0])
            alive = [i for i in alive
                     if est[lead][0] - est[i][0] <= RACE_Z * (est[lead][1] + est[i][1]) ** 0.5]
        if self.record is not None:
            self.keep(cells)
        self.last_parts = self.parts(cells, foe_left(b))
        return [est[i][0] for i in range(len(acts))], alive

    @staticmethod
    def parts(cells, before=None):
        """Each option's (chance of losing, faints expected, the trainer's HP
        share taken this turn), over the turn's outcomes by their weight:
        from the play-outs' ends, the network's heads, or a finished fight's
        own result. An option dropped before any play-out of an outcome
        counts that outcome's mean over the rest. `before` is the trainer's
        HP share before the turn (foe_left)."""
        out = []
        for cs in cells:
            w = sum(cell["w"] for cell in cs if cell["e"])
            if not w:
                out.append((1.0, 6.0, 0.0))
                continue
            lost = sum(cell["w"] * sum(float(e[1]) for e in cell["e"]) / len(cell["e"]) for cell in cs if cell["e"])
            faints = sum(cell["w"] * sum(e[0] for e in cell["e"]) / len(cell["e"]) for cell in cs if cell["e"])
            taken = 0.0
            if before is not None:
                total = sum(cell["w"] for cell in cs)
                taken = sum(cell["w"] * (before - foe_left(cell["c"])) for cell in cs) / total
            out.append((lost / w, faints / w, taken))
        return out

    def keep(self, cells):
        """For stage 2's training (pldata.distill_job): every unfinished
        position the turn reached, as the network reads it, with what its
        play-outs found (their values, and each one's faints and loss)."""
        from . import plfeat
        fight = None
        for cs in cells:
            for cell in cs:
                if cell["done"] or not cell["v"]:
                    continue
                c = cell["c"]
                fight = fight or self.tables(c)
                x, i = plfeat.features(c, fight)
                before = sum(1 for m in c.p.mons if not m.alive())
                self.record.append((x, i, cell["v"], cell["e"], before))

    def leaf(self, c, key, n=None):
        if not c.p.alive() or not c.b.alive():
            return value(c)
        n = n or self.playouts
        return sum(self.playout(clone(c), _mix(key, r)) for r in range(n)) / n

    def playout(self, c, key):
        """The fight from c played on by the plain policy at real odds, on
        dice keyed by `key`, and valued at its end."""
        rng = KeyedRandom(key, c)
        c.dice, c.rng = pl.RunDice(rng, luck="real"), rng
        c.plain_switches = 0
        stop = c.turn + PLAYOUT_TURNS
        while c.turn < stop and c.p.alive() and c.b.alive():
            pl.play_turn(c, self.standin_action(c) if self.standin else plain(c), rng)
        self.last_end = c
        return value(c)

    def standin_action(self, c):
        """The learned stand-in player's option (self.standin, a plpolicy
        network): the legal option it scores highest, over the ten slots
        record_choice uses."""
        from . import plfeat, plvalue
        name = self.standin
        pol = _NETS.get(("policy", name)) or _NETS.setdefault(("policy", name), plvalue.Policy(name))
        acts = options(c)
        if len(acts) == 1:
            return acts[0]
        x, ids = (plfeat.compact if pol.compact else plfeat.features)(c, self.tables(c))
        scores = pol.logits(x[None], ids[None])[0]
        return max(acts, key=lambda a: scores[option_slot(c, a)])

    def decide(self, b):
        """The turn's action."""
        self.decisions += 1
        key = _mix(self.seed, "turn", self.decisions)
        acts = options(b)
        if len(acts) == 1:
            self.notes.append({"turn": b.turn, "options": [(_name(acts[0], b), None)], "chose": 0})
            return acts[0]
        t0 = time.perf_counter()
        q, alive = self.weigh(b, acts, key)
        parts = self.last_parts
        best = choose(q, parts, alive)
        self.notes.append({"turn": b.turn, "options": [(_name(a, b) + ("" if i in alive else " (dropped)"),
                                                        v) for i, (a, v) in enumerate(zip(acts, q))],
                           "parts": parts, "chose": best, "seconds": round(time.perf_counter() - t0, 2)})
        if self.choices is not None:
            self.record_choice(b, acts, q, alive, best)
        return acts[best]

    def record_choice(self, b, acts, q, alive, best):
        """For the learned stand-in player (pldata --choices): the position as
        the network reads it, and over ten slots (option_slot: the active
        Pokemon's four moves, then a switch to each bench place in the order
        the network's features list them) which were options, the value of
        each option still in the running, and the slot chosen."""
        from . import plfeat
        x, ids = plfeat.features(b, self.tables(b))
        legal = np.zeros(10, bool)
        values = np.full(10, np.nan, np.float32)
        chosen = 0
        for i, a in enumerate(acts):
            slot = option_slot(b, a)
            legal[slot] = True
            if i in alive:
                values[slot] = q[i]
            if i == best:
                chosen = slot
        self.choices.append((x, ids, legal, values, chosen))

    def position(self, c, key):
        """A position's worth when the player is to choose, as its best
        option's (chance of losing, faints expected, value)."""
        q, alive = self.weigh(c, options(c), key)
        parts = self.last_parts
        i = choose(q, parts, alive)
        return (parts[i][0], parts[i][1], q[i]) if parts else (0.0, 0.0, q[i])

    def replacement(self, b):
        """The Pokemon sent in after a faint: each candidate's best option
        read from the position it comes into, on the same dice."""
        cands = [i for i, m in enumerate(b.p.mons) if m.alive() and i != b.p.active]
        if len(cands) <= 1:
            return cands[0] if cands else None
        self.decisions += 1
        key = _mix(self.seed, "replace", self.decisions)
        t0 = time.perf_counter()
        vals = []
        for i in cands:
            c = clone(b)
            c.dice, c.rng = ModeDice(), random.Random(0)
            fs.switch_in(c, c.p, i)
            c.dice = c.rng = None
            vals.append(self.position(c, key))
        best = choose([v[2] for v in vals], [v[:2] for v in vals], range(len(cands)))
        self.notes.append({"turn": b.turn, "replacement": True, "seconds": round(time.perf_counter() - t0, 2),
                           "options": [(b.p.mons[i].species, v[2]) for i, v in zip(cands, vals)],
                           "parts": [v[:2] for v in vals], "chose": best})
        return cands[best]

    def lead(self, st, team, boss_keys, flags):
        """The lead: each candidate's best first option, on the same dice;
        (the lead, each candidate's value). In a section (CARRY), only a
        member still standing can lead."""
        key = _mix(self.seed, "lead")
        up = [i for i in range(len(team)) if CARRY is None or CARRY[i][0] > 0]
        vals = [self.position(make_battle(st, team, boss_keys, flags, i), key) if i in up else (1.0, 9.0, -99.0)
                for i in range(len(team))]
        best = choose([v[2] for v in vals], [v[:2] for v in vals], up)
        return best, [v[2] for v in vals]


# ---- the real run: the planner's replacements ---------------------------------------------------

_REAL = {"b": None, "planner": None}


def _player_replacement(b):
    """fightsim's replacement after a faint: the planner's for the run it is
    playing, the play-out's own inside its look-ahead."""
    if _REAL["b"] is b:
        return _REAL["planner"].replacement(b)
    return plain_replacement(b)


fs.player_replacement = _player_replacement


def real_turn(b, a, rng):
    """perfectline.play_turn, returning the trainer's choice as well."""
    b.rng = rng
    b.dice.rng = rng
    b.quick = {m.key: fs.custap_fires(m, b) or (m.item == "Quick Claw" and (b.dice.good(0.2, "quickclaw") if pl.player(m) else b.dice.bad("quickclaw", 0.2)))
               for m in (b.p.cur(), b.b.cur())}
    aa = fightai.choose(b, b.b.cur(), b.p.cur())
    pl._turn(b, a, aa)
    return aa


def play(st, team, boss_keys, flags, lead, seed, cfg, luck="real", log=None, record=None):
    """One run on the harness's dice for this seed, the world's luck `luck`
    ("real", or "unlucky" for the stress test; the planner itself always
    reckons at real odds): {"clean", "won", "deaths", "faints" [(fainted,
    foe out)], "seconds", "decisions", "notes"}. With `log`, each turn is
    written to it with the options the planner weighed; with `record` (a
    list), each turn's whole outcome is appended to it, for plspeed's
    seed-for-seed comparison."""
    reset()                  # each fight starts with empty caches, so memory stays bounded
    rng = random.Random(seed)
    b = make_battle(st, team, boss_keys, flags, lead)
    b.dice = pl.RunDice(rng, luck=luck)
    b.rng = rng
    planner = Planner(seed, **cfg)
    _REAL.update(b=b, planner=planner)
    faints = []
    t0 = time.perf_counter()

    def mon(m):
        s = f"{m.species} {m.hp}/{m.maxhp}"
        if m.status:
            s += f" {m.status}"
        boosts = {k: v for k, v in m.stages.items() if v}
        return s + (f" {boosts}" if boosts else "")
    try:
        while b.turn < TURN_CAP and b.p.alive() and b.b.alive():
            me, foe = b.p.cur().species, b.b.cur().species
            alive = [m.alive() for m in b.p.mons]
            n = len(planner.notes)
            a = planner.decide(b)
            name = _name(a, b)
            aa = real_turn(b, a, rng)
            for m, was in zip(b.p.mons, alive):
                if was and not m.alive():
                    faints.append((m.species, foe))
            if record is not None:
                record.append({"turn": b.turn, "me": me, "foe": foe, "chose": name,
                               "trainer": aa[1].name if aa[0] == "move" else ["switch", aa[1]],
                               "player": [[m.hp, m.status, sorted(m.stages.items())] for m in b.p.mons],
                               "trainer_side": [[m.hp, m.status, sorted(m.stages.items())] for m in b.b.mons],
                               "weather": [b.weather, b.weather_turns],
                               "notes": [dict(n2) for n2 in planner.notes[n:]]})
            if log is not None:
                theirs = aa[1].name if aa[0] == "move" else "switch to " + b.b.mons[aa[1]].species
                print(f"T{b.turn} [{b.weather or 'clear'}] {me}: {name} | {foe}: {theirs} "
                      f"-> you {mon(b.p.cur())} | foe {mon(b.b.cur())}", file=log)
                for note in planner.notes[n:]:
                    kind = "replacement" if note.get("replacement") else "options"
                    opts = ", ".join(f"{o} {v:+.2f}" if v is not None else o for o, v in note["options"])
                    print(f"      {kind}: {opts}", file=log)
    finally:
        _REAL.update(b=None, planner=None)
    deaths = sum(1 for m in b.p.mons if not m.alive())
    won = not b.b.alive()
    return {"clean": won and deaths == 0, "won": won, "deaths": deaths, "faints": faints,
            "seconds": round(time.perf_counter() - t0, 2), "decisions": planner.decisions,
            "turns": b.turn, "notes": planner.notes,
            # What the player's side carries into a section's next fight.
            "carry": [[m.hp, m.status, m.sleep, m.toxic, dict(m.pp), m.item] for m in b.p.mons]}


# A gauntlet section's carried state (plstudy.section): each team member's
# [hp, status, sleep, toxic, pp, item] going into the next fight, or None
# for a fight from full health.
CARRY = None


def make_battle(st, team, boss_keys, flags, lead):
    """perfectline's battle, with a section's carried state applied."""
    b = pl.make_battle(st, team, boss_keys, flags, lead)
    if CARRY is not None:
        for m, (hp, status, sleep, toxic, pp, item) in zip(b.p.mons, CARRY):
            m.hp, m.status, m.sleep, m.toxic, m.pp = hp, status, sleep, toxic, dict(pp)
            fs.hold(st, m, item)         # a Plate types its Judgment (fightsim.hold)
            m.had_item = bool(item)
    return b


# ---- reading a fight -------------------------------------------------------------------------------

# Memory for a pool of workers (in MB): a budget under tools/oxide/capped's
# 22 GB stop, and each worker's own memory beyond what it shares with the
# parent, as plspeed measures it (WORKER_MB, refreshed from its readings).
MEM_BUDGET_MB = 18000
WORKER_MB = 600


def memory():
    """(resident, private) MB of this process now: private is what it holds
    that no other process shares, which is what each forked worker adds."""
    out = {}
    with open("/proc/self/smaps_rollup") as fh:
        for line in fh:
            parts = line.split()
            if parts and parts[0] in ("Rss:", "Private_Clean:", "Private_Dirty:"):
                out[parts[0]] = int(parts[1])
    return out.get("Rss:", 0) // 1024, (out.get("Private_Clean:", 0) + out.get("Private_Dirty:", 0)) // 1024


def pool_size(worker_mb=WORKER_MB, budget_mb=MEM_BUDGET_MB):
    """Workers to run: no more than the cores allow (two left free), nor than
    the memory budget holds after this process's own share."""
    by_cores = max(1, os.cpu_count() - 2)
    by_memory = max(1, (budget_mb - memory()[0]) // worker_mb)
    return min(by_cores, by_memory)


def fork_pool(procs):
    """A pool of forked workers. The prepared fight is frozen first, so the
    collector never touches its objects in a worker and they stay shared."""
    import gc
    gc.collect()
    gc.freeze()
    return mp.get_context("fork").Pool(procs)


_JOB = {}


def _run(seed):
    j = _JOB
    r = play(j["st"], j["team"], j["boss_keys"], j["flags"], j["lead"], seed, j["cfg"], j["luck"])
    r.pop("notes")
    r["private_mb"] = memory()[1]
    return r


# Another six from the fight's box than its hand-played one, and another of
# the trainer's variants than the first (a rival has one per starter), when
# set (--six, --variant): a reading of a fight with no hand-played line, or a
# spread of sixes from one box.
_PICK = {"six": None, "variant": None}


def setup(fight, cfg):
    """The hand-played six of one of the three gyms (plstep3.FIGHTS) with
    its items, and the planner's lead for it."""
    from . import plstep3
    f = dict(plstep3.FIGHTS[fight])
    if _PICK["six"]:
        f["items"] = {n: it for n, it in f["items"].items() if n in _PICK["six"]}
        f["six"] = list(_PICK["six"])
    f["variant"] = _PICK["variant"] or 0
    prep = plstep3.prepare(f, f["six"], f["items"])
    st = prep["st"]
    boss_keys, flags, _s = prep["variants"][f["variant"]]
    team = [f"p{i}" for i in range(len(f["six"]))]
    t0 = time.perf_counter()
    lead, vals = Planner(0, **cfg).lead(st, team, boss_keys, flags)
    return f, st, team, boss_keys, flags, lead, vals, time.perf_counter() - t0


def read(fight, runs=200, cfg=None, procs=None, luck="real", log=sys.stdout):
    """The planner on a gym's hand-played six over the harness's seeds: the
    three numbers, the faints by who and against whom, and the cost."""
    cfg = dict(cfg or {})
    f, st, team, boss_keys, flags, lead, lead_vals, lead_s = setup(fight, cfg)
    _JOB.update(st=st, team=team, boss_keys=boss_keys, flags=flags, lead=lead, cfg=cfg, luck=luck)
    seeds = [f["seed0"] + i for i in range(runs)]
    t0 = time.perf_counter()
    procs = procs or pool_size()
    with fork_pool(procs) as pool:
        rows = pool.map(_run, seeds, chunksize=1)
    wall = time.perf_counter() - t0
    clean = sum(r["clean"] for r in rows)
    won = sum(r["won"] for r in rows)
    deaths = sum(r["deaths"] for r in rows) / runs
    tally = collections.Counter(tuple(x) for r in rows for x in r["faints"])
    cpu = sum(r["seconds"] for r in rows)
    out = {"fight": fight, "six": f["six"], "variant": f["variant"],
           "foes": [st["pokemon"][k]["species"] + f" {st['pokemon'][k]['level']}" for k in boss_keys],
           "cfg": cfg, "luck": luck, "rank": RANK, "fast_tie": FAST_TIE, "standin": STANDIN, "lead": f["six"][lead],
           "lead_values": {n: round(v, 3) for n, v in zip(f["six"], lead_vals)},
           "clean": clean, "won": won, "deaths": round(deaths, 3), "runs": runs,
           "faints": [[a, b, n] for (a, b), n in tally.most_common()],
           "cpu_seconds_per_run": round(cpu / runs, 2),
           "decisions_per_run": round(sum(r["decisions"] for r in rows) / runs, 1),
           "turns_per_run": round(sum(r["turns"] for r in rows) / runs, 1),
           "lead_seconds": round(lead_s, 1), "wall_seconds": round(wall, 1), "procs": procs,
           "fights_per_hour": round(runs / wall * 3600, 1),
           "worker_private_mb_max": max(r["private_mb"] for r in rows),
           "parent_mb": memory()[0],
           # The seeds of the fights lost, so any of them can be replayed
           # turn by turn (--trace --seed).
           "lost_seeds": [s for s, r in zip(seeds, rows) if not r["won"]]}
    print(f"{fight} ({luck} odds): clean {clean}/{runs}, won {won}/{runs}, deaths {deaths:.3f}; "
          f"lead {out['lead']}; {out['cpu_seconds_per_run']} s of one core per run, "
          f"{out['decisions_per_run']} decisions, {wall:.0f} s wall", file=log)
    for a, b, n in out["faints"]:
        print(f"  {a:12} fainted to {b:12} {n}", file=log)
    if out["lost_seeds"]:
        print(f"  lost: seeds {', '.join(map(str, out['lost_seeds']))}", file=log)
    return out


def compare(fight, value, seed=None, log=sys.stdout, drive="playouts"):
    """A spot check of a trained network (Ian's legibility condition for
    stage 2): one fight played by the play-out planner, and at each of its
    decisions the same options valued by the network too, side by side, with
    whether the two would choose alike. With drive="network" the network's
    planner plays the fight instead, so its own line is checked against the
    play-outs' values. (agreements, decisions)."""
    f, st, team, boss_keys, flags, lead, _vals, _s = setup(fight, {"value": value} if drive == "network" else {})
    seed = f["trace_seed"] if seed is None else seed
    netp = Planner(seed, value=value)
    rng = random.Random(seed)
    b = make_battle(st, team, boss_keys, flags, lead)
    b.dice = pl.RunDice(rng, luck="real")
    b.rng = rng
    planner = Planner(seed)
    _REAL.update(b=b, planner=netp if drive == "network" else planner)
    agree = total = 0
    regret = 0.0
    win_regret = [0.0, 0.0]      # chance of losing and faints added, where the choices differ
    try:
        while b.turn < TURN_CAP and b.p.alive() and b.b.alive():
            acts = options(b)
            if len(acts) > 1:
                key = _mix(seed, "compare", b.turn)
                q, alive = planner.weigh(b, acts, key)
                qn, _all = netp.weigh(b, acts, key)
                best = choose(q, planner.last_parts, alive)
                best_n = choose(qn, netp.last_parts, range(len(acts)))
                total += 1
                agree += best == best_n
                # Regret: what the network's choice gives up by the play-outs' own values.
                lost = q[best] - q[best_n]
                regret += lost
                # And by Ian's order: the chance of losing and the faints the
                # network's choice adds, by the play-outs' own estimates.
                pp = planner.last_parts
                d_loss = pp[best_n][0] - pp[best][0] if pp else 0.0
                d_faints = pp[best_n][1] - pp[best][1] if pp else 0.0
                if best != best_n:
                    win_regret[0] += d_loss
                    win_regret[1] += d_faints
                print(f"T{b.turn + 1} {b.p.cur().species} {b.p.cur().hp}/{b.p.cur().maxhp} against "
                      f"{b.b.cur().species} {b.b.cur().hp}/{b.b.cur().maxhp}: play-outs choose "
                      f"{_name(acts[best], b)}, the network {_name(acts[best_n], b)}"
                      f"{'' if best == best_n else f'  (differs; gives up {lost:.2f}, chance of losing {d_loss:+.3f}, faints {d_faints:+.2f})'}",
                      file=log)
                print("      " + ", ".join(f"{_name(a, b)} {q[i]:+.2f}/{qn[i]:+.2f}" for i, a in enumerate(acts)),
                      file=log)
                if pp:
                    print("      by play-outs (chance of losing, faints): " + ", ".join(
                        f"{_name(a, b)} {pp[i][0]:.2f} {pp[i][1]:.2f}" for i, a in enumerate(acts)), file=log)
                a = acts[best_n if drive == "network" else best]
            else:
                a = acts[0]
            real_turn(b, a, rng)
    finally:
        _REAL.update(b=None, planner=None)
    print(f"{agree} of {total} decisions alike (values shown as play-outs/network); the network's choices "
          f"give up {regret:.2f} in all by the play-outs' values, {regret / max(1, total):.3f} a decision; "
          f"by Ian's order they add {win_regret[0]:+.3f} to the chance of losing and {win_regret[1]:+.2f} "
          f"faints in all, by the play-outs' estimates", file=log)
    return agree, total, regret


def _budget_job(seed):
    """One fight played by the full play-out planner; at each of its
    decisions every smaller planner of _JOB["small"] chooses too, on dice of
    its own (shared dice would make a small reading a subset of the full
    one's and flatter the agreement). Per small planner: [decisions alike,
    decisions, chance of losing added, faints added, seconds weighing], by
    the full planner's own estimates; and the full planner's seconds."""
    j = _JOB
    rng = random.Random(seed)
    b = make_battle(j["st"], j["team"], j["boss_keys"], j["flags"], j["lead"])
    b.dice, b.rng = pl.RunDice(rng, luck="real"), rng
    full = Planner(seed)
    small = [Planner(seed, budget=budget, standin=standin) for _label, budget, standin in j["small"]]
    out = [[0, 0, 0.0, 0.0, 0.0] for _p in small]
    full_s = 0.0
    _REAL.update(b=b, planner=full)
    try:
        while b.turn < TURN_CAP and b.p.alive() and b.b.alive():
            acts = options(b)
            if len(acts) > 1:
                t0 = time.perf_counter()
                q, alive = full.weigh(b, acts, _mix(seed, "budget", b.turn))
                full_s += time.perf_counter() - t0
                pp = full.last_parts
                best = choose(q, pp, alive)
                for p, o in zip(small, out):
                    t0 = time.perf_counter()
                    qs, alive_s = p.weigh(b, acts, _mix(seed, "budget-small", b.turn))
                    o[4] += time.perf_counter() - t0
                    pick = choose(qs, p.last_parts, alive_s)
                    o[0] += pick == best
                    o[1] += 1
                    if pick != best and pp:
                        o[2] += pp[pick][0] - pp[best][0]
                        o[3] += pp[pick][1] - pp[best][1]
                a = acts[best]
            else:
                a = acts[0]
            real_turn(b, a, rng)
    finally:
        _REAL.update(b=None, planner=None)
    return out, full_s


def budget_check(fight, small, fights=12, procs=None, log=sys.stdout):
    """Does a smaller play-out budget, with or without the learned stand-in
    player, choose as the full budget does? Fights played by the full
    planner from the fight's trace seed on; at each decision every planner
    in `small` ((label, budget, stand-in or None) each) chooses too. A second
    full-budget planner on its own dice belongs in `small` as the ceiling:
    two readings at the full budget do not always agree either."""
    f, st, team, boss_keys, flags, lead, _vals, _s = setup(fight, {})
    _JOB.update(st=st, team=team, boss_keys=boss_keys, flags=flags, lead=lead, small=small)
    seeds = [f["trace_seed"] + i for i in range(fights)]
    with fork_pool(procs or min(fights, pool_size())) as pool:
        rows = pool.map(_budget_job, seeds, chunksize=1)
    full_s = sum(r[1] for r in rows)
    total = sum(r[0][0][1] for r in rows)
    print(f"{fight}: {fights} fights played by the full planner (budget {BUDGET}), {total} decisions, "
          f"{full_s / max(1, total):.2f} s of one core a decision", file=log)
    out = {"fight": fight, "fights": fights, "decisions": total, "full_seconds": round(full_s, 1), "small": {}}
    for i, (label, budget, standin) in enumerate(small):
        agree = sum(r[0][i][0] for r in rows)
        loss = sum(r[0][i][2] for r in rows)
        faints = sum(r[0][i][3] for r in rows)
        secs = sum(r[0][i][4] for r in rows)
        print(f"  {label}: {agree} of {total} alike ({agree / max(1, total):.1%}); where they differ, "
              f"{loss:+.3f} chance of losing and {faints:+.2f} faints in all by the full planner's estimates; "
              f"{secs / max(1, total):.2f} s a decision", file=log)
        out["small"][label] = {"budget": budget, "standin": standin, "alike": agree, "loss_added": round(loss, 3),
                               "faints_added": round(faints, 2), "seconds": round(secs, 1)}
    return out


def trace(fight, seed=None, cfg=None, luck="real", log=sys.stdout):
    cfg = dict(cfg or {})
    f, st, team, boss_keys, flags, lead, vals, _s = setup(fight, cfg)
    seed = f["trace_seed"] if seed is None else seed
    print(f"{fight}, seed {seed}, {luck} odds; lead {f['six'][lead]} (lead values: "
          + ", ".join(f"{n} {v:+.2f}" for n, v in zip(f["six"], vals)) + ")", file=log)
    r = play(st, team, boss_keys, flags, lead, seed, cfg, luck, log=log)
    print(f"{'won' if r['won'] else 'lost'}; fainted: "
          f"{', '.join(a for a, _b in r['faints']) or 'none'}; {r['seconds']} s", file=log)
    return r


OUT = os.path.join(os.path.dirname(__file__), "perfectline_results", "step3")


def main(argv=None):
    global RANK, FAST_TIE, FAST_EPS, STANDIN
    ap = argparse.ArgumentParser()
    ap.add_argument("fight")
    ap.add_argument("--runs", type=int, default=200)
    ap.add_argument("--trace", action="store_true")
    ap.add_argument("--compare", metavar="MODEL",
                    help="a spot check: the play-out planner's fight, each decision also valued by MODEL")
    ap.add_argument("--drive", choices=("playouts", "network"), default="playouts",
                    help="with --compare: whose choices play the fight")
    ap.add_argument("--seed", type=int)
    ap.add_argument("--playouts", type=int, default=PLAYOUTS)
    ap.add_argument("--value", help="a trained network (plvalue) to value positions instead of play-outs")
    ap.add_argument("--budget", type=int, default=BUDGET,
                    help="play-outs per option and trainer pick, shared by probability (0: none)")
    ap.add_argument("--luck", default="real", choices=("real", "unlucky"))
    ap.add_argument("--rank", default=RANK, choices=("win", "value"),
                    help="Ian's order (the chance of losing, then faints) or the old value alone")
    ap.add_argument("--fast-tie", action="store_true",
                    help="break genuine ties on losing and faints toward the faster finish (off by default)")
    ap.add_argument("--fast-eps", type=float, default=FAST_EPS,
                    help="with --fast-tie: how close in value a tie must be")
    ap.add_argument("--standin", help="a learned stand-in player (plpolicy) to play the play-outs; with "
                                      "--budget-check, several may be given, joined by commas")
    ap.add_argument("--procs", type=int)
    ap.add_argument("--save", help="write the reading to perfectline_results/step3/<name>.json")
    ap.add_argument("--six", nargs="+", metavar="NAME", help="another six from the fight's box")
    ap.add_argument("--variant", type=int, help="another of the trainer's variants (a rival's, by starter)")
    ap.add_argument("--budget-check", metavar="BUDGET[,BUDGET...]",
                    help="do these smaller budgets (plain, and the first with --standin) choose as the full one "
                         "does?")
    ap.add_argument("--check-fights", type=int, default=12, help="with --budget-check: fights to play")
    args = ap.parse_args(argv)
    if args.budget_check:
        # The full planner and the ceiling play out with the plain policy;
        # only the small planner named for it uses the stand-in.
        budgets = [int(x) for x in args.budget_check.split(",")]
        small = [(f"budget {BUDGET} again", BUDGET, None)] + [(f"budget {n}", n, None) for n in budgets]
        for name in (args.standin or "").split(","):
            if name:
                small.append((f"budget {budgets[0]} with {name}", budgets[0], name))
        _PICK.update(six=args.six, variant=args.variant)
        RANK = args.rank
        out = budget_check(args.fight, small, args.check_fights, args.procs)
        if args.save:
            os.makedirs(OUT, exist_ok=True)
            with open(os.path.join(OUT, args.save + ".json"), "w") as fh:
                json.dump(out, fh, indent=1)
        return 0
    cfg = dict(playouts=args.playouts, budget=args.budget or None, value=args.value)
    _PICK.update(six=args.six, variant=args.variant)
    RANK = args.rank
    FAST_TIE, FAST_EPS = args.fast_tie, args.fast_eps
    STANDIN = args.standin
    if args.compare:
        compare(args.fight, args.compare, args.seed, drive=args.drive)
        return 0
    if args.trace:
        trace(args.fight, args.seed, cfg, args.luck)
        return 0
    out = read(args.fight, args.runs, cfg, args.procs, args.luck)
    if args.save:
        os.makedirs(OUT, exist_ok=True)
        with open(os.path.join(OUT, args.save + ".json"), "w") as fh:
            json.dump(out, fh, indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main())

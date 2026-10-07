"""A fight position as numbers, for stage 2's learned position value
(docs/oxide/scorer-speed-plan.md, "Stage 2, the learned value").

A position is read from the player's side at the start of a turn, before
either side chooses. It becomes two arrays:

- floats: the field (weather and its turns, Trick Room, screens, Tailwind,
  Safeguard and hazards on each side, the turn), then each of the twelve
  Pokemon (HP, level, stats, stat stages, status, volatile state, whether
  it holds an item, and each move's power, accuracy, priority, category,
  PP left and secondary chance), then the matchup grid: for each player
  Pokemon against each trainer Pokemon, the share of the other's HP each
  does a turn with its best attack, how many turns each needs, and who
  moves first;
- ids: each Pokemon's types, ability and item, and each move's type and
  effect, as small whole numbers the network looks up in its own tables.

The twelve slots are fixed: the player's active Pokemon, then the player's
other five in team order, then the trainer's active one, then its others in
party order. Names that are not types become ids through a stable hash, so
every process and every fight number them alike.

The matchup grid's damage comes from the calculator's rows the fight was
prepared with (the middle roll, times accuracy), worked out once per fight
and weather; the two active Pokemon's entries are worked out afresh at each
position, with their stat stages, screens and burn.
"""
import math
import zlib

from . import plthreads  # noqa: F401  (one numpy thread per process, before numpy loads)
import numpy as np  # noqa: E402

from . import fightsim as fs

TYPES = ("Normal", "Fire", "Water", "Electric", "Grass", "Ice", "Fighting", "Poison", "Ground", "Flying",
         "Psychic", "Bug", "Rock", "Ghost", "Dragon", "Dark", "Steel", "Fairy")
TYPE_ID = {t: i + 1 for i, t in enumerate(TYPES)}       # 0: none
WEATHERS = (None, "Sun", "Rain", "Sand", "Hail")
STATUSES = (None, "par", "brn", "psn", "tox", "slp", "frz")
CATEGORIES = ("Physical", "Special", "Status")
# Id tables for names that are not types: abilities and items share one,
# effects have their own. 0 is "none".
NAME_IDS = 1024
EFFECT_IDS = 512
SLOTS = 12
MOVES = 4


def name_id(name, size=NAME_IDS):
    if not name:
        return 0
    return 1 + zlib.crc32(name.encode()) % (size - 1)


def type_id(t):
    return TYPE_ID.get((t or "").title(), 0)


# ---- the per-fight tables ----------------------------------------------------------------------------

def _expected(rec, mv):
    """A move's expected damage a turn from a calculator row's entry: the
    middle roll times its accuracy, a two-turn move at half."""
    if rec is None or "error" in rec or not rec.get("rolls"):
        return 0.0
    rolls = rec["rolls"]
    d = rolls[len(rolls) // 2] * fs.expected_hit_scale(mv)     # Fury Cutter's later hits
    acc = 1.0 if mv.acc == 0 else min(1.0, mv.acc / 100)
    if mv.effect in fs.TWO_TURN or mv.effect == "RECHARGE_AFTER":
        d /= 2
    if mv.effect in fs.SELF_KO:
        return 0.0
    return d * acc


class Fight:
    """What a fight's positions share, worked out once: each side's keys in
    team order, and for each weather the fight can have, each player
    Pokemon's best expected damage a turn on each trainer Pokemon and back
    (as a share of the target's maximum HP), and each one's speed."""

    def __init__(self, st, team, boss_keys):
        self.st = st
        self.team = list(team)
        self.boss = list(boss_keys)
        self.weathers = sorted({w for w, _a, _d in st["rows"]}, key=str)
        self.moves = {k: [fs.move(n) for n in st["moves"][k]][:MOVES] for k in self.team + self.boss}
        self.dmg = {}         # weather: {(attacker, defender): share of the defender's HP}
        self.speed = {}
        for w in self.weathers:
            d = {}
            for a in self.team + self.boss:
                for t in (self.boss if a in self.team else self.team):
                    row = st["rows"].get((w, a, t)) or st["rows"].get((None, a, t))
                    best = 0.0
                    if row:
                        for mv in self.moves[a]:
                            if mv.damaging():
                                best = max(best, _expected(row["moves"].get(mv.name), mv))
                    d[(a, t)] = best / st["info"][t]["hp"]
            self.dmg[w] = d
            self.speed[w] = {k: st["speed"].get((w, k)) or st["speed"].get((None, k)) or 1
                             for k in self.team + self.boss}

    def table(self, weather):
        w = weather if weather in self.dmg else None
        if w not in self.dmg:
            w = self.weathers[0]
        return self.dmg[w], self.speed[w]


# ---- the arrays ------------------------------------------------------------------------------------

def slots(b):
    """The twelve Pokemon in slot order (None for an empty slot)."""
    def side(s):
        rest = [m for i, m in enumerate(s.mons) if i != s.active]
        out = [s.mons[s.active]] + rest
        return out + [None] * (6 - len(out))
    return side(b.p) + side(b.b)


def _mon(m, active, out, ids):
    if m is None:
        out.extend([0.0] * MON_FLOATS)
        ids.extend([0] * MON_IDS)
        return
    st = m.stats
    out += [1.0, float(m.alive()), float(active), m.hp / m.maxhp, m.maxhp / 300, (m.level or 50) / 100,
            st.get("atk", 0) / 300, st.get("def", 0) / 300, st.get("spa", 0) / 300, st.get("spd", 0) / 300,
            st.get("spe", 0) / 300]
    out += [m.stages[k] / 6 for k in fs.STAGE_KEYS]
    out += [float(m.status == s) for s in STATUSES]
    out += [m.sleep / 4, m.toxic / 8]
    out += [float(bool(m.confused)), float(bool(m.seeded)), float(bool(m.ingrained)),
            float(m.trapped_by is not None), float(bool(m.bound)), (m.sub or 0) / m.maxhp,
            float(m.charging is not None), float(bool(m.recharge)), float(m.lock is not None),
            float(bool(m.taunt)), float(m.choice is not None), float(bool(m.aqua_ring)),
            float(bool(m.flash_fire)), float(bool(m.cursed)), (m.perish or 0) / 4, float(bool(m.yawn)),
            m.crit_stage / 3, float(bool(m.curled)), (m.rollout or 0) / 5, float(bool(m.item))]
    ids += [type_id(m.types[0] if m.types else None), type_id(m.types[1] if len(m.types) > 1 else None),
            name_id(m.ability), name_id(m.item)]
    for i in range(MOVES):
        mv = m.moves[i] if i < len(m.moves) else None
        if mv is None:
            out.extend([0.0] * MOVE_FLOATS)
            ids.extend([0, 0])
            continue
        out += [1.0, mv.power / 150, 1.0 if mv.acc == 0 else mv.acc / 100, mv.pri / 3]
        out += [float(mv.cat == c) for c in CATEGORIES]
        out += [m.pp.get(mv.name, mv.pp) / max(1, mv.pp), (mv.chance or 0) / 100]
        ids += [type_id(mv.type), name_id(mv.effect, EFFECT_IDS)]


MOVE_FLOATS = 9
MON_FLOATS = 11 + 7 + 7 + 2 + 20 + MOVES * MOVE_FLOATS
MON_IDS = 4 + MOVES * 2
FIELD_FLOATS = len(WEATHERS) + 1 + 2 + 8 + 6 + 3
PAIR_FLOATS = 6 * 6 * 5
FLOATS = FIELD_FLOATS + SLOTS * MON_FLOATS + PAIR_FLOATS
IDS = SLOTS * MON_IDS


def features(b, fight):
    """(floats, ids) for the position b, as numpy arrays of FLOATS float32 and
    IDS int16."""
    out, ids = [], []
    out += [float(b.weather == w) for w in WEATHERS] + [(b.weather_turns or 0) / 8]
    out += [float(b.trick_room > 0), min(b.trick_room, 5) / 5 if b.trick_room < 999 else 1.0]
    for s in (b.p, b.b):
        out += [s.screens["Reflect"] / 5, s.screens["Light Screen"] / 5, s.tailwind / 4, s.safeguard / 5]
    for s in (b.p, b.b):
        out += [float(bool(s.hazards["rocks"])), s.hazards["spikes"] / 3, s.hazards["tspikes"] / 2]
    out += [min(b.turn, 100) / 50, len(b.p.alive()) / 6, len(b.b.alive()) / 6]
    mons = slots(b)
    for i, m in enumerate(mons):
        _mon(m, i in (0, 6), out, ids)
    dmg, speed = fight.table(b.weather)
    me, foe = b.p.cur(), b.b.cur()
    for m in mons[:6]:
        for t in mons[6:]:
            if m is None or t is None:
                out.extend([0.0] * 5)
                continue
            if m is me and t is foe:
                mine = max((fs.exp_damage(b, me, foe, mv) for mv in me.moves if mv.damaging()), default=0.0) / foe.maxhp
                theirs = max((fs.exp_damage(b, foe, me, mv) for mv in foe.moves if mv.damaging()), default=0.0) / me.maxhp
                sm, sf = b.speed(me), b.speed(foe)
            else:
                mine, theirs = dmg.get((m.key, t.key), 0.0), dmg.get((t.key, m.key), 0.0)
                sm, sf = speed.get(m.key, 1), speed.get(t.key, 1)
            if b.trick_room:
                sm, sf = -sm, -sf
            out += [mine, theirs, _turns(t.hp / t.maxhp, mine), _turns(m.hp / m.maxhp, theirs),
                    float(sm > sf) - float(sm < sf)]
    f = np.asarray(out, dtype=np.float32)
    i = np.asarray(ids, dtype=np.int16)
    if f.shape[0] != FLOATS or i.shape[0] != IDS:
        raise AssertionError(f"features: {f.shape[0]} floats and {i.shape[0]} ids, expected {FLOATS} and {IDS}")
    return f, i


# The learned stand-in player reads a compact part of the features, enough to
# choose a turn's option: the field, the two active Pokemon and the matchup
# grid (every player Pokemon against every trainer Pokemon). These are the
# columns of `features` it takes, so it trains on positions stored whole.
ACTIVE_ME = slice(FIELD_FLOATS, FIELD_FLOATS + MON_FLOATS)
ACTIVE_FOE = slice(FIELD_FLOATS + 6 * MON_FLOATS, FIELD_FLOATS + 7 * MON_FLOATS)
PAIRS = slice(FIELD_FLOATS + SLOTS * MON_FLOATS, FLOATS)
COMPACT_FLOATS = FIELD_FLOATS + 2 * MON_FLOATS + PAIR_FLOATS
COMPACT_IDS = 2 * MON_IDS


def compact_of(x, ids):
    """The compact part of whole features (arrays of one position or many)."""
    x = np.asarray(x)
    ids = np.asarray(ids)
    f = np.concatenate([x[..., :FIELD_FLOATS], x[..., ACTIVE_ME], x[..., ACTIVE_FOE], x[..., PAIRS]], axis=-1)
    i = np.concatenate([ids[..., :MON_IDS], ids[..., 6 * MON_IDS:7 * MON_IDS]], axis=-1)
    return f, i


def compact(b, fight):
    """The compact features of a position, computed directly: the same
    numbers as compact_of(features(b, fight)) at a fraction of the cost."""
    out, ids = [], []
    out += [float(b.weather == w) for w in WEATHERS] + [(b.weather_turns or 0) / 8]
    out += [float(b.trick_room > 0), min(b.trick_room, 5) / 5 if b.trick_room < 999 else 1.0]
    for s in (b.p, b.b):
        out += [s.screens["Reflect"] / 5, s.screens["Light Screen"] / 5, s.tailwind / 4, s.safeguard / 5]
    for s in (b.p, b.b):
        out += [float(bool(s.hazards["rocks"])), s.hazards["spikes"] / 3, s.hazards["tspikes"] / 2]
    out += [min(b.turn, 100) / 50, len(b.p.alive()) / 6, len(b.b.alive()) / 6]
    mons = slots(b)
    _mon(mons[0], True, out, ids)
    _mon(mons[6], True, out, ids)
    dmg, speed = fight.table(b.weather)
    me, foe = b.p.cur(), b.b.cur()
    for m in mons[:6]:
        for t in mons[6:]:
            if m is None or t is None:
                out.extend([0.0] * 5)
                continue
            if m is me and t is foe:
                mine = max((fs.exp_damage(b, me, foe, mv) for mv in me.moves if mv.damaging()), default=0.0) / foe.maxhp
                theirs = max((fs.exp_damage(b, foe, me, mv) for mv in foe.moves if mv.damaging()), default=0.0) / me.maxhp
                sm, sf = b.speed(me), b.speed(foe)
            else:
                mine, theirs = dmg.get((m.key, t.key), 0.0), dmg.get((t.key, m.key), 0.0)
                sm, sf = speed.get(m.key, 1), speed.get(t.key, 1)
            if b.trick_room:
                sm, sf = -sm, -sf
            out += [mine, theirs, _turns(t.hp / t.maxhp, mine), _turns(m.hp / m.maxhp, theirs),
                    float(sm > sf) - float(sm < sf)]
    return np.asarray(out, dtype=np.float32), np.asarray(ids, dtype=np.int16)


def _turns(left, per_turn):
    """Turns to take a HP share `left` at `per_turn` a turn, out of 8 (1.0 for
    never or eight or more)."""
    if left <= 0:
        return 0.0
    if per_turn <= 0:
        return 1.0
    return min(8, math.ceil(left / per_turn - 1e-9)) / 8

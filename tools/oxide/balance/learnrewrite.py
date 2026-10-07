"""The learnset rewrite's generator: step 4 of docs/oxide/learnset-checks.md.

    PYTHONPATH=. python3 -m tools.oxide.balance.learnrewrite plan               # build every list, print what changed
    PYTHONPATH=. python3 -m tools.oxide.balance.learnrewrite write              # ... and write them into res/pokemon/
    PYTHONPATH=. python3 -m tools.oxide.balance.learnrewrite show GIBLE SHINX   # lines before and after, with reasons

It rewrites every level-up list by the locked rules of
docs/oxide/learnset-insights.md, starting from Oxide's lists as they were
before the rewrite (learncheck.BASE_REF), so a list keeps what already
works and every change has a rule behind it. Ian's reasons are general
rules and weights here, never a patch for one species. The five held-out
lines get no special treatment.

The passes, in order:

1. Clean every list. The moves leaving player lists or the game go (R24,
   Fury Attack, Feint, the first cut, the dead weight); a move good only
   for building a trainer's fight goes to level 1, the trainers' palette
   (R26); a phazing move stays only where a wild catch knows it (R18); an
   attack under 90% accuracy gives way to an accurate one of its type
   (R37); nothing stays past the League's cap.
2. Fix the structure of each line the player can own. A move below the
   lowest level a stage can be had at moves up to it (R25); a move the
   pre-evolution learns inside its evolution's split joins the evolved
   form at the same level, so holding is no fake choice (R8); an evolution
   that needs a known move gets that move by level-up.
3. Fill. Each line is walked from its earliest catch, split by split, as
   the player meets it. In each split a stage is held at the cap it gains
   two or three new moves (R2), and the first split gives five or six with
   little filler (R1). Each addition is the best candidate for what the line
   still lacks by then: an attack of each of its types (R11), a same-type
   attack of 50 (check 1), coverage by the second split and three types over
   the game (R4, R5), a good utility move (R7), a strong same-type attack by
   mid-game (R30), a later-generation move (R16). Candidates come from every
   working move Oxide has (Ian, 2026-10-06), scored by fit: same-type or
   coverage on a stat that fits (R3, R15), abilities (R31), the line's own
   stats (R17), and a link to the line in Oxide's lists, a later game, or
   Kaizo, which counts in a move's favour without limiting the choice. An
   added attack keeps to a power ceiling for its split (stronger lines a
   split later), never weaker than a move of its type the line already has
   unless it brings something else (R6), and never under 90% accuracy (R37).
4. Tidy each list: one move a level, no move twice, at most 34 entries
   (the engine's MAX_LEARNSET_ENTRIES), and every catch knowing an attack.

A line the player cannot own gets the clean and the tidy only: its list is
the trainers' palette. learnrewrite_log.tsv records every change with its rule.
"""
import argparse
import collections
import csv
import functools
import json
import os
import re
import sys

from .. import jsonstyle
from ..encounters import calc_trainers, learnsets as canon_ls, pokedex
from . import b6, data, learncheck as lc, learnstudy as ls, pool, weather_moves

BASE = "oxide"
SPLITS = lc.SPLITS
LOG = os.path.join(data.ROOT, "tools", "oxide", "balance", "learnrewrite_log.tsv")
MAX_ENTRIES = 34                 # include/struct_defs/species.h, MAX_LEARNSET_ENTRIES
MAX_EGG_MOVES = 16               # include/constants/daycare.h
GEN4_LAST_ID = 467               # Shadow Force, the last move Platinum has


def si(split):
    return lc.si(split)


def caps():
    return lc.caps()


def top():
    return caps()[SPLITS[-1]]


def M():
    return lc.moves()


def name(const):
    return lc.move_name(const)


# ---- what a move is ------------------------------------------------------------------------------

# The dead weight of 2026-09-27 (balance-rules): weak attacks that go from
# every list. Octazooka is not here: Oxide's is 85 power at full accuracy.
DEAD_WEIGHT = {"MOVE_ABSORB", "MOVE_WRAP", "MOVE_CONSTRICT", "MOVE_BARRAGE", "MOVE_SNORE",
               "MOVE_RAGE", "MOVE_RAZOR_WIND", "MOVE_BIDE", "MOVE_COMEUPPANCE", "MOVE_SUBMISSION"}
# R26: bad for a player in a permadeath run, useful to a trainer's design:
# Destiny Bond, and every move that knocks its own user out.
TRAINER_PALETTE = lc.SELF_KO | {"MOVE_DESTINY_BOND"}
# R18: a phazing move's use is on a wild catch, which it can end.
PHAZING = {"MOVE_ROAR", "MOVE_WHIRLWIND"}
# Ian's rulings on one move of one line (2026-09-30, and 2026-10-06 in
# Charmander's session: "Dragon Rage leaves the line's early list").
RULED_OFF = {("SPECIES_CHARMANDER", "MOVE_DRAGON_RAGE"), ("SPECIES_CHARMELEON", "MOVE_DRAGON_RAGE")}
# Ian's calls for one move on one egg list, the trainers' palette, recorded
# as his, not a rule of the generator.
IAN_EGG_MOVES = {
    "SPECIES_DARKRAI": [("MOVE_DARK_VOID", "Ian, 2026-10-06: Officer Somnu's Darkrai keeps Dark Void, which "
                                           "Darkrai learns only at 66, above Somnu's levels; the player never "
                                           "reaches an egg list")],
}
# Damage that needs a condition the user rarely has, or comes out random:
# never added (learnstudy's conditional moves, and Natural Gift, which Ian
# wants used sparingly).
CONDITIONAL = {"MOVE_DREAM_EATER", "MOVE_FOCUS_PUNCH", "MOVE_LAST_RESORT", "MOVE_BELCH",
               "MOVE_SPIT_UP", "MOVE_NATURAL_GIFT", "MOVE_FLING", "MOVE_TRUMP_CARD",
               "MOVE_PRESENT", "MOVE_SNORE"}
PLAIN = lc.PLAIN_EFFECTS
PIVOT_EFFECTS = {"SWITCH_HIT"}
DRAIN_EFFECTS = {"RECOVER_HALF_DAMAGE_DEALT", "RECOVER_THREE_QUARTERS_DAMAGE_DEALT"}
# Defensive boosts: worth placing only on a bulky line, or one an ability
# shields from the critical hits that ignore them (R31, Iron Defense).
DEFENSIVE_EFFECTS = {"DEF_UP", "DEF_UP_2", "DEF_UP_3", "SP_DEF_UP_2", "DEF_SPD_UP",
                     "DEF_UP_DOUBLE_ROLLOUT_POWER", "STOCKPILE"}
CRIT_SHIELDS = {"SHELL_ARMOR", "BATTLE_ARMOR"}
BULKY = 90


def later_gen(const):
    return (M()[const].get("id") or 0) > GEN4_LAST_ID


def is_attack(const):
    """A damaging move a list may rely on, with a power to weigh."""
    return lc.damaging(const) and lc.effective_power(const) > 0 and const not in CONDITIONAL


def speed_control(const):
    m = M()[const]
    return m["class"] != "STATUS" and m["effect"] in lc.SPEED_CONTROL_EFFECTS and m["effect_chance"] == 100


# Attacks whose cost or condition makes them poor for a player in a
# permadeath run with no weather of their own: Solar Beam and Solar Blade
# charge a turn without sun; the power that falls with the user's HP; and
# the moves that cost the user half its HP or more.
SITUATIONAL_EFFECTS = {"SKIP_CHARGE_TURN_IN_SUN", "DECREASE_POWER_WITH_LESS_USER_HP",
                       "RECOIL_HALF_MAX_HP", "MIND_BLOWN", "RECOIL_HALF", "CHARGE_TURN_SP_ATK_UP",
                       "CHARGE_TURN_SP_ATK_UP_RAIN_SKIPS", "HIT_IN_3_TURNS"}
# By name: Steel Beam's half-HP cost; Tera Blast, which needs Terastallizing
# Oxide does not have; Defog, held to 1 PP and good for nothing but fog; and
# Ian's removed TMs (2026-09-28), which no pass spreads by level-up either.
HEAVY_COST_BY_NAME = {"MOVE_STEEL_BEAM", "MOVE_TERA_BLAST", "MOVE_DEFOG"} | set(lc.REMOVED_TMS)
# Cut, Rock Smash and Flash leave where they were only HMs (Ian, 2026-09-27),
# so no pass spreads them by level-up.
FIELD_MOVES = {"MOVE_CUT", "MOVE_ROCK_SMASH", "MOVE_FLASH"}
# Moves that call a random or borrowed move: too random, like Metronome
# (Ian, "useless (too random)").
RANDOM_EFFECTS = {"CALL_RANDOM_MOVE", "USE_RANDOM_ALLY_MOVE", "USE_LAST_USED_MOVE", "USE_MOVE_FIRST",
                  "USE_RANDOM_LEARNED_MOVE_SLEEP", "NATURE_POWER"}
# An added attack weaker than this needs a reason beyond filling a count:
# weak attacks are never added (balance-rules), save a first type attack,
# priority (R29) and sure speed control (R27).
WEAK_POWER = 50
# An attack the line has no link to may come in for its type only when most
# lines can learn it in some game (a staple, like Water Pulse), never a niche
# one (Aqua Jet on a cat); a same-type one needs a few dozen learners.
STAPLE_LEARNERS, STAB_LEARNERS = 100, 30


def never_added(const):
    """Moves the generator never adds to a list (it may keep some it finds)."""
    m = M().get(const)
    if not m or not lc.reliable(const) or const in DEAD_WEIGHT or const in TRAINER_PALETTE \
            or const in PHAZING or const in CONDITIONAL or const in weather_moves.WEATHER_MOVES \
            or m["effect"] in SITUATIONAL_EFFECTS or const in HEAVY_COST_BY_NAME \
            or const in FIELD_MOVES or m["effect"] in RANDOM_EFFECTS:
        return True
    if m["class"] != "STATUS" and m["accuracy"] and m["accuracy"] < lc.R37_ACCURACY:
        return True
    if m["class"] == "STATUS":
        t = lc.tier(const)
        return t is None or t[0] < lc.TIER_RANK["Okay"]
    return lc.effective_power(const) <= 0


@functools.lru_cache(maxsize=None)
def abilities(species):
    return frozenset((pokedex.load(data.ROOT, species) or {}).get("abilities") or [])


def ratio(const, holder):
    """The share of the holder's better attacking stat the move uses (R3, R15)."""
    atk, spa = lc.attack_stats(holder)
    use = atk if M()[const]["class"] == "PHYSICAL" else spa
    return use / max(atk, spa, 1)


def attack_value(const, holder):
    """An attack's worth to one Pokemon: effective power, the same-type
    bonus, the share of its better stat, and what the move adds beside its
    damage: a secondary effect (more under Serene Grace; Sheer Force trades
    it for power, R31), priority (R29), sure speed control (R27), draining,
    switching out; less for imperfect accuracy."""
    m = M()[const]
    base = lc.effective_power(const)
    if base <= 0:
        return 0.0
    stab = 1.5 if m["type"] in lc.types_of(holder) else 1.0
    v = base * stab * ratio(const, holder)
    chance = m["effect_chance"] or 0
    abil = abilities(holder)
    if m["effect"] not in PLAIN and chance:
        if "SHEER_FORCE" in abil:
            v *= 1.3
        else:
            v += base * min(chance, 100) / 100 * (0.6 if "SERENE_GRACE" in abil else 0.3)
    if (m["priority"] or 0) > 0:
        v += 15
    if speed_control(const):
        v += 15
    if m["effect"] in DRAIN_EFFECTS:
        v += 8
    if m["effect"] in PIVOT_EFFECTS:
        v += 10
    if m["accuracy"] and m["accuracy"] < 100:
        v *= m["accuracy"] / 100
    return v


def distinct(const):
    """What lets a weaker attack earn a place beside a stronger one of its
    type (R6 as narrowed): priority, sure speed control, switching out,
    draining, or a secondary effect of 30% or more."""
    m = M()[const]
    return ((m["priority"] or 0) > 0 or speed_control(const) or m["effect"] in PIVOT_EFFECTS
            or m["effect"] in DRAIN_EFFECTS
            or (m["effect"] not in PLAIN | WEAK_SECONDARY and (m["effect_chance"] or 0) >= 30))


def _property(const):
    """What an attack brings beside its power, by kind, or None."""
    m = M()[const]
    if (m["priority"] or 0) > 0:
        return "priority"
    if m["effect"] in PIVOT_EFFECTS:
        return "switch"
    if speed_control(const):
        return "speed control"
    if m["effect"] in DRAIN_EFFECTS:
        return "drain"
    return None


# Secondary effects too slight to earn a weaker attack its place: an
# accuracy drop (Mud-Slap) makes fights random, which R37 sets against.
WEAK_SECONDARY = {"LOWER_ACCURACY_HIT"}


# ---- what fits a line ------------------------------------------------------------------------------

@functools.lru_cache(maxsize=None)
def canon_index():
    """({canon species key: {MOVE_X: weight}}, {canon key: {MOVE_X: [levels]}},
    Counter of how many canon species learn each move): Showdown's lists for
    Generation 4 and each species' latest game. A level-up entry weighs 1.0,
    any other way 0.85. Ian's word (2026-10-06): inspiration, not pick lists."""
    table = canon_ls.canon_lists()
    ids = canon_ls.move_ids(data.ROOT)
    keys = sorted((k for k, r in table.items() if not k.startswith("_") and isinstance(r, dict)), key=len)
    # A form's key extends its base species' key (palkiaorigin, arceusfire):
    # the learner count is by base species, so forms do not inflate it.
    base = {}
    for k in keys:
        base[k] = next((b for b in keys if len(b) >= 4 and len(b) < len(k) and k.startswith(b)), k)
    per, levels = {}, {}
    learner_sets = collections.defaultdict(set)
    for key in keys:
        rec = table[key]
        got, lv = {}, collections.defaultdict(list)
        for src in (rec.get("gen4") or [], (rec.get("latest") or {}).get("moves") or []):
            for item in src:
                mv = ids.get(item[0])
                if not mv:
                    continue
                # Event-only and Dream World sources are no way to learn a move in play.
                codes = [c for c in item[1].split(",") if c and c[0] not in "SD"]
                if not codes:
                    continue
                level_codes = [int(c[1:]) for c in codes if c.startswith("L") and c[1:].isdigit()]
                got[mv] = max(got.get(mv, 0), 1.0 if level_codes else 0.85)
                lv[mv] += level_codes
        per[key] = got
        levels[key] = dict(lv)
        for mv in got:
            learner_sets[mv].add(base[key])
    learners = collections.Counter({mv: len(s) for mv, s in learner_sets.items()})
    return per, levels, learners


@functools.lru_cache(maxsize=None)
def canon_key(species):
    return canon_ls.showdown_id(data.ROOT, species)


def links(fam):
    """{MOVE_X: weight}: the moves the line is linked to by any of its
    members: Oxide's lists before the rewrite (level-up 1.0; TM, tutor and
    egg 0.85), the canon lists, and Kaizo's lists (1.0). The TM lists are
    read with the TM records of the same commit, never the TM pass's: the
    new TMs are no link (on 2026-10-07 reading them gave 136 species 203
    entries, Block from Substitute's TM90 among them)."""
    return links_of(frozenset(lc.families()[fam]))


def branch_links(holder):
    """The links of the holder's own branch (itself, what it evolves from and
    into): one branch's Moonlight is no link for its sibling (the exam's
    regressions, 2026-10-06: the same filler on every branch of a line)."""
    return links_of(frozenset(lc.families()[lc.family(holder)]) & related(holder))


@functools.lru_cache(maxsize=None)
def links_of(members):
    per, _lv, _n = canon_index()
    kz = lc.learnstudy_kaizo()
    names = lc._by_compact_name()
    machines = lc.base_machines()
    out = {}

    def add(mv, w):
        if mv in M():
            out[mv] = max(out.get(mv, 0), w)
    for sp in sorted(members):
        # Read from Oxide's lists before the rewrite, so a run's own egg-list
        # changes never feed the next run.
        rec = pokedex.load(data.ROOT, sp, ref=lc.BASE_REF) or {}
        for _lv, mv in lc.learnset(BASE, sp):
            add(mv, 1.0)
        for label in rec.get("by_tm") or []:
            add(machines.get(label), 0.85)
        for mv in (rec.get("by_tutor") or []) + (rec.get("egg_moves") or []):
            add(mv, 0.85)
        for mv, w in per.get(canon_key(sp), {}).items():
            add(mv, w)
        for _lv, nm in (kz.get(sp) or {}).get("list", []):
            add(names.get(lc._compact(ls.SPELLING.get(nm, nm))), 1.0)
    return out


@functools.lru_cache(maxsize=None)
def species_links(species, const):
    """Whether one species (not just its line) learns the move some way in
    canon or in Oxide's lists: a move moved onto a pre-evolution must suit
    it, not only its evolution (R25; Vespiquen's Defend Order is not Combee's)."""
    per, _lv, _n = canon_index()
    if const in per.get(canon_key(species), {}):
        return True
    rec = pokedex.load(data.ROOT, species, ref=lc.BASE_REF) or {}
    machines = lc.base_machines()
    return (any(m == const for _l, m in lc.learnset(BASE, species))
            or const in (rec.get("by_tutor") or []) or const in (rec.get("egg_moves") or [])
            or any(machines.get(label) == const for label in rec.get("by_tm") or []))


@functools.lru_cache(maxsize=None)
def linked_types(fam):
    return frozenset(M()[mv]["type"] for mv in links(fam) if M()[mv]["class"] != "STATUS")


@functools.lru_cache(maxsize=None)
def level_hints(fam, const):
    """The levels a later game or Generation 4 teaches the move to the line by level-up."""
    _per, levels, _n = canon_index()
    out = []
    for sp in lc.families()[fam]:
        out += [lv for lv in levels.get(canon_key(sp), {}).get(const, []) if lv > 1]
    return tuple(sorted(set(out)))


SIGNATURE_LEARNERS = 5   # canon counts each form apart (Deoxys is four)


def signature(const, fam):
    """A move canon gives five species entries or fewer, none of them this
    line's: another line's signature, not a candidate."""
    _per, _lv, learners = canon_index()
    return learners.get(const, 0) <= SIGNATURE_LEARNERS and const not in links(fam)


def plausibility(const, fam, holder):
    """How well a move suits the line, 0 to 1: its link weight; else, for
    an attack, 0.35 for one of the holder's types and 0.25 for a coverage
    type the line reaches elsewhere; 0.15 for an unlinked status move. Any
    working move may come in (Ian, 2026-10-06), but a linked one comes first."""
    w = branch_links(holder).get(const)
    if w:
        return w
    if signature(const, fam):
        return 0.0
    m = M()[const]
    if m["class"] == "STATUS":
        return 0.0      # a status move suits a line only through its own links
    learners = canon_index()[2].get(const, 0)
    if m["type"] in lc.types_of(holder):
        return 0.35 if learners >= STAB_LEARNERS else 0.0
    return 0.25 if m["type"] in linked_types(fam) and learners >= STAPLE_LEARNERS else 0.0


# ---- how strong an added attack may be, and when ---------------------------------------------------

# The ceiling on an added attack's effective power, times the share of the
# holder's better stat it uses, by split. Coverage sits ten lower (R5: weaker
# early, stronger later). Oxide's own lists stay where they are; this binds
# only what the generator adds or moves.
CEILING = {"Roark": 60, "Gardenia": 75, "Fantina": 80, "Maylene": 90, "Wake": 90, "Byron": 100,
           "Candice": 100, "HQ": 110, "Galactic": 120, "Volkner": 130, "Barry": 150, "League": 150}


def flagged(species):
    """Ian's power flag (balance-rules): base Speed over 100, or a better
    attacking stat over 100. Such a stage gets its strong moves a split later."""
    s = lc.stats(species)
    return s.get("speed", 0) > 100 or max(lc.attack_stats(species)) > 100


@functools.lru_cache(maxsize=None)
def finals(species):
    """The final forms a stage can reach."""
    out, todo, seen = [], [species], {species}
    while todo:
        sp = todo.pop()
        kids = [t for _n, _i, t in pool.evolutions(sp) if t not in seen]
        if not kids:
            out.append(sp)
        for k in kids:
            seen.add(k)
            todo.append(k)
    return tuple(out)


def weak(species):
    """A middling line (R36), which may carry early: its added attacks get a
    split's head start. Judged on its strongest final form, so a weak first
    stage of a strong line (Budew) does not count."""
    best = max(finals(species), key=lambda f: sum(lc.stats(f).values()))
    return sum(lc.stats(best).values()) < 420 and max(lc.attack_stats(best)) < 75


def _shifted(holder, split_idx):
    shift = 1 if flagged(holder) else (-1 if weak(holder) else 0)
    return max(0, min(len(SPLITS) - 1, split_idx - shift))


def ceiling(holder, split_idx, cover):
    """The ceiling for an added attack; coverage sits lower, most of all in
    the first three splits (R5: weaker early, stronger later)."""
    idx = _shifted(holder, split_idx)
    return CEILING[SPLITS[idx]] - ((15 if idx <= 2 else 10) if cover else 0)


RAW_MARGIN = 15   # an off-stat attack may exceed the ceiling by its stat share, not by more than this


# ---- the type ladders: climb, don't jump (Ian, 2026-10-06) ------------------------------------
#
# Ian on the early kits: "It entirely depends on the pokemon, and keeping it
# to hard rules destroys the variability between pokemon; giga drain in
# roark is clearly too much, but bubblebeam on corphish is probably fine."
# So each type's attacks form a ladder by power, physical and special side
# by side, and a line climbs it: a gap is filled from the rung that fits the
# point in the game, a rung or two above what the line has, never the
# strongest move a ceiling lets through. A rung is read by the power the
# holder feels (its share of its better attacking stat), so an off-stat
# BubbleBeam sits low on a physical Corphish and a Giga Drain high on any
# Grass line in Roark's split. The old ceilings still set the point in the
# game a first move of a type starts at (start_power: the ceiling less 20),
# and otherwise weigh the score; start_power is the lever if early kits
# feel off in play.

FIRST_RUNG = 40     # a line's first attacks come from the ladder's foot; below it is dead weight


# The multi-hit moves stand on a ladder by their power a hit, as Ian's Grass
# ladder has it ("Bullet Seed 25 a hit", near the foot, 2026-10-06), not by
# their average total, which the checks read.
MULTI_HIT = {"MULTI_HIT", "HIT_TWICE", "POISON_MULTI_HIT", "HIT_THREE_TIMES", "HIT_THREE_TIMES_RISING_10",
             "HIT_THREE_TIMES_INCREMENT_BASE_POWER_20", "HIT_THREE_TIMES_FIXED_POWER",
             "HIT_THREE_TIMES_ALWAYS_CRITICAL", "UP_TO_10_HITS", "HIT_TWICE_AND_FLINCH"}


def ladder_power(const):
    """A move's power for the ladders: a hit's for a multi-hit move, else effective power."""
    m = M()[const]
    return float(m["power"] or 0) if m["effect"] in MULTI_HIT else lc.effective_power(const)


@functools.lru_cache(maxsize=None)
def ladder(typ, side=None):
    """The type's rungs on one side (PHYSICAL or SPECIAL; both when None):
    the distinct ladder powers of the attacks a list may rely on, lowest
    first. A line climbs the side of its better attacking stat; a side with
    no attack of the type falls back to both."""
    out = tuple(sorted({round(ladder_power(c)) for c, m in M().items()
                        if m["type"] == typ and is_attack(c) and lc.reliable(c) and ladder_power(c) >= 20
                        and (side is None or m["class"] == side)}))
    return out if out or side is None else ladder(typ)


def side_of(holder):
    atk, spa = lc.attack_stats(holder)
    return "PHYSICAL" if atk >= spa else "SPECIAL"


def rung(power, typ, side=None):
    """The highest rung of the type's ladder at or under the power; -1 when
    the power is under the ladder's foot."""
    return max((i for i, p in enumerate(ladder(typ, side)) if p <= power + 0.5), default=-1)


def rung_up(power, typ, side=None):
    """The lowest rung of the type's ladder at or over the power."""
    steps = ladder(typ, side)
    return next((i for i, p in enumerate(steps) if p >= power - 0.5), len(steps) - 1)


def side_for(const, holder):
    """The ladder side a move is read on: its own class where it fits the
    holder (a mixed attacker climbs both), else the holder's better side, so
    an off-stat move sits low there (Corphish's BubbleBeam)."""
    return M()[const]["class"] if lc.fits(const, holder) else side_of(holder)


def rung_of(const, holder):
    """Where an attack stands on its type's ladder for the holder."""
    return rung(standing(const, holder), M()[const]["type"], side_for(const, holder))


def felt(const, holder):
    """An attack's power as the holder feels it: effective power times its
    share of the holder's better attacking stat."""
    return lc.effective_power(const) * ratio(const, holder)


def standing(const, holder):
    """Where an attack stands on its ladder for the holder: halfway between
    its power as the player reads it and as the holder feels it, so an
    off-stat move sits lower (Corphish's BubbleBeam) without a 90-power move
    passing for a weak one at level 3 (Chinchou's Wild Charge). A pivot
    (Flip Turn, U-turn, Volt Switch) stands at least at the middle of its
    type's ladder: Ian, 2026-10-06, "pivoting is incredibly strong", so it
    is never a first move."""
    power = ladder_power(const)
    s = (power + power * ratio(const, holder)) / 2
    if M()[const]["effect"] in PIVOT_EFFECTS:
        steps = ladder(M()[const]["type"])
        s = max(s, steps[len(steps) // 2] if steps else s)
    return s


def pace(holder):
    """Rungs a line climbs a split: one for a flagged stage, which gets its
    strong moves later (balance-rules), two for the rest."""
    return 1 if flagged(holder) else 2


def start_power(holder, split_idx):
    """Where a line meets a type's ladder for the first time at a split:
    the old ceiling less 20, read as the point in the game (40 in Roark's
    split, 55 in Gardenia's), never under the ladder's foot."""
    return max(FIRST_RUNG, ceiling(holder, split_idx, False) - 20)


def climb_room(holder, typ, before, split_idx, first=False, side=None):
    """The highest rung of the type, on the holder's side, a move added to
    it at the split may stand on: a rung or two (pace) above the best of the
    type it had before the split, one rung fewer in the split it is caught
    in, where it starts. For a type it has none of: its own type from the
    first rung at or over the lower of its best attack and the split's
    starting point, since a line's first moves come from the low rungs
    (Zubat's first Flying move is Gust, not the Wing Attack two rungs up); a
    coverage type no higher than the line's own level, so a sparse ladder
    (special Steel starts at Flash Cannon) gives no early spike."""
    side = side or side_of(holder)
    held = [standing(m, holder) for m in before if m in M() and is_attack(m) and M()[m]["type"] == typ]
    if held:
        return rung(max(held), typ, side) + pace(holder) - (1 if first else 0)
    known = [standing(m, holder) for m in before if m in M() and is_attack(m)]
    start = start_power(holder, split_idx)
    if typ in lc.types_of(holder):
        # The first rung at or over the base on the holder's better side,
        # read as a power on the side asked about, so a sparse side does not
        # start high (Nosepass's special Rock starts at AncientPower 60,
        # its physical at Rock Throw 50).
        base = max(FIRST_RUNG, min(max(known), start) if known else start)
        better = side_of(holder)
        steps = ladder(typ, better)
        power = steps[rung_up(base, typ, better)] if steps else base
        return rung(power, typ, side)
    return rung(max(known + [start]), typ, side)


def climbs(const, holder, before, split_idx, first=False):
    """Whether an attack added at the split climbs rather than jumps."""
    return rung_of(const, holder) <= climb_room(holder, M()[const]["type"], before, split_idx, first,
                                                side_for(const, holder))


def within_ceiling(const, holder, split_idx):
    # Normal hits nothing hard, so it is no coverage (learncheck.coverage)
    # and takes the plain ceiling.
    cover = M()[const]["type"] not in lc.types_of(holder) and M()[const]["type"] != "NORMAL"
    cap = ceiling(holder, split_idx, cover)
    eff = lc.effective_power(const)
    return eff * ratio(const, holder) <= cap and eff <= cap + RAW_MARGIN


# The best utility tier an added move may have, by split: the strongest
# status moves are not early gifts (Ian on Houndoom's Toxic, 2026-09-27).
UTILITY_CEILING = {"Roark": lc.TIER_RANK["Good"], "Gardenia": lc.TIER_RANK["Incredible"],
                   "Fantina": lc.TIER_RANK["Fantastic"]}


def utility_within(const, holder, split_idx):
    return rank(const) <= UTILITY_CEILING.get(SPLITS[_shifted(holder, split_idx)], lc.TIER_RANK["SSS"])


# The generator's reading of status moves Ian has not rated, where the
# Generation 9 list sits far from his scale: sure paralysis and burn beside
# his good Stun Spore, and the healing moves beside his incredible Synthesis,
# which they match or beat. Used only to choose and time additions; the
# checks keep his tiers and the list's.
RANK_READING = {"MOVE_THUNDER_WAVE": 6, "MOVE_WILL_O_WISP": 6, "MOVE_GLARE": 6, "MOVE_SPORE": 8,
                "MOVE_LEECH_SEED": 5, "MOVE_TAUNT": 5, "MOVE_RECOVER": 7, "MOVE_ROOST": 7,
                "MOVE_SOFTBOILED": 7, "MOVE_SLACK_OFF": 7, "MOVE_MILK_DRINK": 7, "MOVE_MOONLIGHT": 7,
                "MOVE_MORNING_SUN": 7, "MOVE_SHORE_UP": 7, "MOVE_HEAL_ORDER": 7, "MOVE_STRENGTH_SAP": 7}


def rank(const):
    t = lc.tier(const)
    return RANK_READING.get(const, t[0] if t else 0)


# A late addition must be worth a slot: from Byron's split on, an attack of
# at least this effective power unless it brings priority, sure speed
# control or a switch.
LATE_SPLIT, LATE_POWER, LATE_DISTINCT_POWER = 5, 70, 60


@functools.lru_cache(maxsize=None)
def kaizo_floor(fam, const):
    """For a flagged line's strong move, the earliest level Kaizo allows:
    Kaizo's own level for the line, but never later than the end of the
    Oxide split that level falls in (balance-rules, 2026-09-27). None when
    Kaizo does not teach the line the move."""
    kz = lc.learnstudy_kaizo()
    names = lc._by_compact_name()
    best = None
    for sp in lc.families()[fam]:
        for lv, nm in (kz.get(sp) or {}).get("list", []):
            if lv > 1 and names.get(lc._compact(ls.SPELLING.get(nm, nm))) == const:
                best = lv if best is None else min(best, lv)
    if best is None:
        return None
    split = ls.split_of("kaizo", best)
    oxide_cap = caps().get(split.title() if split else "", top())
    return min(best, oxide_cap)


# ---- the draft and its log ----------------------------------------------------------------------------

class Draft:
    """Every species' list being rewritten, and the log of each change."""

    def __init__(self):
        self.lists = {sp: [list(e) for e in lc.learnset(BASE, sp)] for sp in lc.species_set()}
        # The egg lists as they were before the rewrite, so a second run
        # starts from the same place as the first.
        self.eggs = {sp: list((pokedex.load(data.ROOT, sp, ref=lc.BASE_REF) or {}).get("egg_moves") or [])
                     for sp in lc.species_set()}
        # {family: {MOVE_X: {species}}}: moves added only to fill a count, so
        # one filler is not handed to every branch of a line (Ian, 2026-10-06).
        self.filler = collections.defaultdict(lambda: collections.defaultdict(set))
        self.log = []

    def note(self, species, level, move, action, rule, detail=""):
        self.log.append((species, level, move, action, rule, detail))

    def levels(self, species):
        return {lv for lv, _m in self.lists[species] if lv >= 2}

    def has(self, species, move, at_least=2):
        return any(m == move and lv >= at_least for lv, m in self.lists[species])

    def remove(self, species, entry, rule, detail=""):
        self.lists[species].remove(entry)
        self.note(species, entry[0], entry[1], "removed", rule, detail)

    def add(self, species, level, move, rule, detail=""):
        lst = self.lists[species]
        # Insert after every entry of a lower or equal level, so the list's
        # order stays the game's (level order, earlier entries first).
        at = len([e for e in lst if e[0] <= level])
        lst.insert(at, [level, move])
        self.note(species, level, move, "added", rule, detail)

    def move(self, species, entry, level, rule, detail=""):
        old = entry[0]
        self.lists[species].remove(entry)
        lst = self.lists[species]
        at = len([e for e in lst if e[0] <= level])
        lst.insert(at, [level, entry[1]])
        self.note(species, level, entry[1], f"moved from {old}", rule, detail)

    def to_palette(self, species, entry, rule, detail=""):
        """Take an entry off the level-up list for the trainers' palette. A
        trainer-only move (R26) goes to the egg list of the line's first
        stage, which trainers' teams draw on and no catch ever knows (Ian,
        2026-10-06: a trainer's move never lands in a wild catch's four).
        Anything else, or an R26 move with that list full, goes to level 1,
        first in the list, where a capture drops it before any other (R18,
        R7). A species the player can catch knows its level-1 entries when
        caught low, so there the entry just goes."""
        self.lists[species].remove(entry)
        mv = entry[1]
        egg = lc.family(species)
        if rule == "R26" and has_egg_list(egg):
            if mv in self.eggs[egg]:
                self.note(species, entry[0], mv, "removed", rule, f"{detail}; {lc.species_name(egg)}'s egg list has it")
                return
            if len(self.eggs[egg]) < MAX_EGG_MOVES:
                self.eggs[egg].append(mv)
                self.note(species, entry[0], mv, f"moved from {entry[0]} to {lc.species_name(egg)}'s egg list",
                          rule, detail)
                return
        if catchable(species) and not (rule == "R26" and not _wild_knows_at_1(species, mv, self.lists[species])):
            self.note(species, entry[0], mv, "removed", rule, detail + "; a catch would know it at level 1")
            return
        if not any(m == mv and lv == 1 for lv, m in self.lists[species]):
            self.lists[species].insert(0, [1, mv])
        self.note(species, 1, mv, f"moved from {entry[0]} to level 1", rule, detail)


@functools.lru_cache(maxsize=None)
def has_egg_list(species):
    """Whether the species' file has an egg list (a legendary's or a form's may not)."""
    path = os.path.join(data.ROOT, "res", "pokemon", pokedex.folder_of(species), "data.json")
    with open(path, encoding="utf-8") as f:
        return file_eggs(f.read()) is not None


def _wild_knows_at_1(species, move, lst):
    """Whether a wild catch would know the move with it put at level 1 of `lst`."""
    trial = [[1, move]] + [list(e) for e in lst]
    return any(sp == species and how in WILD and move in calc_trainers.default_moves(trial, lv)
               for sp, _s, lv, how, _p in lc.catch_rows())


@functools.lru_cache(maxsize=None)
def _catchable():
    return frozenset(r[0] for r in lc.catch_rows())


def catchable(species):
    return species in _catchable()


# ---- pass 1: clean ---------------------------------------------------------------------------------------

WILD = {"wild", "surf", "old_rod", "good_rod", "super_rod", "honey"}


def _wild_knows(species, move):
    """Whether some wild catch of the species knows the move at capture."""
    return any(sp == species and how in WILD and move in lc.at_capture(BASE, sp, lv)
               for sp, _s, lv, how, _p in lc.catch_rows())


def accurate_twin(const, species, fam):
    """An accurate move of the same type and class worth at least 85% of
    what the inaccurate one does on average (its power times its accuracy),
    which suits the line: R37's replacement, a linked move first. Ian would
    rather lose a little power than gamble (R37: inaccuracy makes fights
    random), so Rock Slide stands in for Stone Edge."""
    m = M()[const]
    want = lc.effective_power(const) * (m["accuracy"] or 100) / 100 * 0.85
    best = None
    for c, mm in M().items():
        if mm["type"] != m["type"] or mm["class"] != m["class"] or never_added(c) \
                or lc.effective_power(c) < want or c == const or plausibility(c, fam, species) <= 0:
            continue
        key = (branch_links(species).get(c, 0), lc.effective_power(c))
        if best is None or key > best[0]:
            best = (key, c)
    return best[1] if best else None


# The moves the rework Ian accepted made stronger (2026-10-06, cloud/main-
# move-reworks): the rampage moves in one turn, the recharge and charge-turn
# moves without their lost turn, and every multi-hit move at 25 a hit. An
# entry of one on a list Oxide had would be an early spike where it stands
# (Larvitar's Thrash at 23, a one-turn 120 in Gardenia's split), so it moves
# to where the line can climb to it.
REWORKED = {"MOVE_THRASH", "MOVE_PETAL_DANCE", "MOVE_OUTRAGE", "MOVE_UPROAR", "MOVE_RAGING_FURY",
            "MOVE_HYPER_BEAM", "MOVE_GIGA_IMPACT", "MOVE_ROCK_WRECKER", "MOVE_ROAR_OF_TIME",
            "MOVE_BLAST_BURN", "MOVE_FRENZY_PLANT", "MOVE_HYDRO_CANNON", "MOVE_SKY_ATTACK"}


def reworked(const):
    """A move the rework made stronger in one turn. The multi-hit moves are
    not among them: the ladders read them by their power a hit (Ian's Grass
    ladder puts Bullet Seed, 25 a hit, near the foot), so they stay put."""
    return const in REWORKED


def place_reworked(d, species, entry):
    """R9 after the rework: an entry of a move the rework made stronger stays
    where the line can climb to it on the type ladders by its level's split,
    with what the stage and those it evolves from know by then, and else
    moves to the first split where it can, at its new numbers, so the rework
    brings no early spike. An entry below the level the stage is first had
    at is left to R25."""
    lv, mv = entry
    if lv < lowest_had().get(species, 2):
        return
    own = [species] + list(pool.pre_evolutions().get(species) or [])
    x0 = si(lc.split_of_level(lv))
    for x in range(x0, len(SPLITS)):
        level = max(lv, lc.window(SPLITS[x])[0])
        before = [m for s in own for l, m in d.lists[s] if 2 <= l < level and m != mv]
        if climbs(mv, species, before, x):
            break
    else:
        return
    if x == x0:
        return
    free = next((l for l in range(max(lv, lc.window(SPLITS[x])[0]), top() + 1) if l not in d.levels(species)), None)
    if free is not None:
        d.move(species, entry, free, "R9", f"at its reworked numbers the line climbs to it in {SPLITS[x]}'s split")


def starter_kit(d, species):
    """Ian's ruling of 2026-10-07 on Rowan's starters: at or below the level
    they are given at, exactly a basic weak attack and a basic status move,
    each the one the list had before the rewrite where it had one, else
    Tackle and Growl, at the list's own level. Any other entry there moves
    to the first free level after it, if the list has it nowhere later, so
    the starter's own type comes after 5 (a Fire starter's Ember)."""
    if species not in lc.STARTERS:
        return
    low = lc.STARTER_LEVEL
    base = lc.learnset(BASE, species)
    attack = next((m for lv, m in base if lv <= low and lc.basic_attack(m)), "MOVE_TACKLE")
    status = next((m for lv, m in base if lv <= low and m in lc.BASIC_STATUS), "MOVE_GROWL")
    kit = {mv: next((lv for lv, m in base if m == mv and lv <= low), 1) for mv in (attack, status)}
    why = "a starter knows a basic attack and a basic status move at 5 (Ian, 2026-10-07)"
    kept = set()
    for entry in [e for e in d.lists[species] if e[0] <= low]:
        lv, mv = entry
        if mv in kit and mv not in kept:
            kept.add(mv)
            if lv != kit[mv]:
                d.move(species, entry, kit[mv], "Ian's ruling", why)
            continue
        if lc.counts(mv) and not d.has(species, mv, at_least=low + 1):
            free = next(l for l in range(low + 1, top() + 1) if l not in d.levels(species))
            d.move(species, entry, free, "Ian's ruling", why)
        else:
            d.remove(species, entry, "Ian's ruling", why)
    for mv, lv in kit.items():
        if mv not in kept:
            d.add(species, lv, mv, "Ian's ruling", why)


@functools.lru_cache(maxsize=None)
def type_multi_hit():
    """{TYPE: MOVE_X}: the one physical two-to-five-hit move each type keeps
    (Ian, 2026-10-06), Normal's being Fury Swipes. Water Shuriken, Water's
    only one, is left out: it is special and strikes first, so it would not
    stand in for a physical slap like for like."""
    out = {"NORMAL": "MOVE_FURY_SWIPES"}
    for c, m in sorted(M().items()):
        if m["effect"] == "MULTI_HIT" and m["class"] == "PHYSICAL" and m["type"] != "NORMAL" \
                and c not in lc.REMOVED and not lc.not_working(c):
            if m["type"] in out:
                raise SystemExit(f"two multi-hit moves for {m['type']}: {out[m['type']]} and {c}")
            out[m["type"]] = c
    return out


@functools.lru_cache(maxsize=None)
def ordered_types(species):
    return tuple((pokedex.load(data.ROOT, species) or {}).get("types") or [])


@functools.lru_cache(maxsize=None)
def line_members(species):
    fam = lc.family(species)
    return tuple(sp for sp in sorted(lc.species_set()) if lc.family(sp) == fam)


def multi_hit_pick(species):
    """The stand-in for a cut multi-hit move: the stage's own type's, first
    type first, else Fury Swipes."""
    return next((type_multi_hit()[t] for t in ordered_types(species) if t in type_multi_hit()),
                "MOVE_FURY_SWIPES")


def multi_hit_stand_in(d, species, entry):
    """Ian's ruling of 2026-10-06 on one list entry of a cut multi-hit move.
    A stage that already learns a multi-hit move of its line's types by that
    level, or whose earlier stages do, needs no stand-in (Shellder has Icicle
    Spear from 13, so Cloyster has it too). One that learns the stand-in
    later has it brought down to this level, so the line keeps one multi-hit
    move where it had it (Omastar's Rock Blast). Else the stand-in takes the
    level."""
    lv, mv = entry
    pick = multi_hit_pick(species)
    line = {t for sp in line_members(species) for t in ordered_types(sp)}
    covering = {type_multi_hit()[t] for t in line if t in type_multi_hit()} | {pick}
    why = "one two-to-five-hit move per type (Ian, 2026-10-06)"
    d.remove(species, entry, "Ian's ruling", f"{name(mv)} leaves the game: {why}")
    have = [(l, m, species) for l, m in d.lists[species] if m in covering and (2 <= l <= lv or l == lv == 1)]
    # An earlier stage's entry counts as what it will be once its own cut
    # moves have their stand-ins, so the order the species are walked in
    # does not matter.
    for pre in pool.pre_evolutions().get(species) or []:
        for l, m in d.lists[pre]:
            if m in lc.MULTI_HIT_CUT and m not in DEAD_WEIGHT:
                m = multi_hit_pick(pre)
            if m in covering and 2 <= l <= lv:
                have.append((l, m, pre))
    if have:
        l, m, who = have[0]
        whose = "" if who == species else f"{lc.species_name(who)} "
        d.note(species, lv, mv, "no stand-in", "Ian's ruling", f"{whose}learns {name(m)} at {l}")
        return
    later = [e for e in d.lists[species] if e[1] == pick and e[0] > lv]
    if later and lv >= 2:
        d.move(species, later[0], lv, "Ian's ruling", f"in place of {name(mv)}: {why}")
    else:
        d.add(species, lv, pick, "Ian's ruling", f"in place of {name(mv)}: {why}")


def clean(d, species):
    fam = lc.family(species)
    # The egg list, the trainers' palette, takes the same swap.
    eggs = d.eggs[species]
    if any(m in lc.REPLACED or m in lc.MULTI_HIT_CUT for m in eggs):
        swap = {m: lc.REPLACED.get(m) or multi_hit_pick(species) for m in eggs
                if m in lc.REPLACED or m in lc.MULTI_HIT_CUT}
        d.eggs[species] = list(dict.fromkeys(swap.get(m, m) for m in eggs))
        for m, new in swap.items():
            d.note(species, 0, m, "egg list", "Ian's ruling" if m in lc.MULTI_HIT_CUT else "Ian's rework",
                   f"{name(new)} in its place")
    for entry in list(d.lists[species]):
        # A stand-in can move a later entry down, ahead of the walk.
        if entry not in d.lists[species]:
            continue
        lv, mv = entry
        m = M().get(mv)
        if m is None:
            d.remove(species, entry, "unknown move")
        elif lc.out_of_lists(mv):
            d.remove(species, entry, "R24", "out of every player list")
        elif mv in lc.REPLACED:
            new = lc.REPLACED[mv]
            d.remove(species, entry, "Ian's rework", f"{name(mv)} leaves the game; {name(new)} takes its place")
            if not any(m == new for _l, m in d.lists[species]):
                d.add(species, lv, new, "Ian's rework", f"in place of {name(mv)} (2026-10-06)")
        elif mv in lc.MULTI_HIT_CUT and mv not in DEAD_WEIGHT:
            # Barrage went as dead weight on 2026-09-27, with nothing in its place.
            multi_hit_stand_in(d, species, entry)
        elif mv in lc.REMOVED:
            d.remove(species, entry, "removed", "leaves the game or every player list")
        elif mv in weather_moves.WEATHER_MOVES:
            d.remove(species, entry, "weather", "the player never controls weather")
        elif lc.not_working(mv):
            d.remove(species, entry, "engine", "its effect never happens")
        elif mv in lc.UNCHECKED:
            d.remove(species, entry, "engine", "its condition is not built yet (the move rework's cloud job)")
        elif mv in lc.CATCH_ONLY and lv > caps()[lc.CATCH_ONLY_UNTIL]:
            d.remove(species, entry, "catch-only", "it helps only to catch: early or not at all (Ian, 2026-10-06)")
        elif mv in DEAD_WEIGHT:
            d.remove(species, entry, "dead weight", "a weak attack that goes from every list (2026-09-27)")
        elif (species, mv) in RULED_OFF:
            d.remove(species, entry, "Ian's ruling", "Dragon Rage leaves the line's early list")
        elif mv in TRAINER_PALETTE and (lv != 1 or _wild_knows(species, mv)):
            d.to_palette(species, entry, "R26", "bad for the player, good for a trainer's fight")
        elif mv in PHAZING and lv >= 2 and not _wild_knows(species, mv):
            d.to_palette(species, entry, "R18", "Roar's use is on a wild catch, which this list's level never is")
        elif (lc.tier(mv) or (1,))[0] == 0 and (lv >= 2 or catchable(species)) and mv not in TRAINER_PALETTE:
            d.to_palette(species, entry, "R7", "a move Ian rates useless or terrible")
        elif m["effect"] in RANDOM_EFFECTS and lv >= 2:
            d.to_palette(species, entry, "R7", "calls a random or borrowed move, too random like Metronome")
        elif m["class"] != "STATUS" and m["accuracy"] and m["accuracy"] < lc.R37_ACCURACY \
                and not lc.ohko(mv) and 2 <= lv <= top():
            twin = accurate_twin(mv, species, fam)
            if twin and not d.has(species, twin):
                d.remove(species, entry, "R37", f"under 90% accuracy; {name(twin)} takes its place")
                d.add(species, lv, twin, "R37", f"in place of {name(mv)}")
            elif twin:
                d.remove(species, entry, "R37", f"under 90% accuracy, beside {name(twin)}")
            elif any(l <= lv and M()[x]["type"] == m["type"] and M()[x]["class"] != "STATUS"
                     and lc.reliable(x) and lc._acc(x) >= lc.R37_ACCURACY
                     and lc.effective_power(x) >= 0.85 * lc.effective_power(mv)
                     for l, x in d.lists[species] if x != mv):
                d.remove(species, entry, "R37", "under 90% accuracy, beside an accurate move of its type")
            else:
                d.note(species, lv, mv, "kept for Ian", "R37", "under 90% accuracy, no accurate twin fits")
        elif reworked(mv) and 2 <= lv <= top():
            place_reworked(d, species, entry)
        elif lv > top():
            free = [l for l in range(top(), caps()[SPLITS[-2]], -1) if l not in d.levels(species)]
            if lc.counts(mv) and free and not d.has(species, mv):
                d.move(species, entry, free[0], "past the League", "nothing is placed past 78")
            else:
                d.remove(species, entry, "past the League", "nothing is placed past 78")


# ---- pass 2: the structure of a line --------------------------------------------------------------------

@functools.lru_cache(maxsize=None)
def lowest_had():
    """{species: the lowest level any player can first have it at}."""
    return {sp: min(st.level for st, _r in routes) for sp, routes in lc.stage_routes(BASE).items()}


def fix_lost(d, species):
    """R25: an entry below the lowest level the stage can be had at, which no
    earlier stage learns, goes onto the pre-evolution's list at the same
    point where the pre-evolution is had by then; else it moves up to the
    stage's lowest level. A move that counts for nothing just goes."""
    pres = pool.pre_evolutions().get(species) or []
    if not pres or species not in lowest_had():
        return
    lowest = lowest_had()[species]
    parent = pres[0]
    parent_low = lowest_had().get(parent)
    earlier = {m for p in pres for lv, m in d.lists[p] if lv >= 2}
    for entry in sorted(d.lists[species]):
        lv, mv = entry
        if not (2 <= lv < lowest) or mv in earlier:
            continue
        if any(m == mv and l >= lowest for l, m in d.lists[species]) or not lc.counts(mv) \
                or (lc.tier(mv) or (9,))[0] <= lc.BAD:
            d.remove(species, entry, "R25", f"below {lowest}, the lowest level it is had at")
            continue
        if parent_low is not None and parent_low < lv and species_links(parent, mv):
            split = lc.split_of_level(lv)
            lo, hi = lc.window(split)
            free = sorted((l for l in range(max(lo, parent_low + 1), min(hi, lowest) + 1)
                           if l not in d.levels(parent) and holds(parent, mv, l)), key=lambda l: (abs(l - lv), l))
            if free:
                d.lists[species].remove(entry)
                d.note(species, lv, mv, "removed", "R25", f"below {lowest}; onto {lc.species_name(parent)}'s list")
                d.add(parent, free[0], mv, "R25", f"from {lc.species_name(species)}'s {lv}, below its {lowest}")
                earlier.add(mv)
                continue
        free = next((l for l in range(lowest, top() + 1) if l not in d.levels(species) and holds(species, mv, l)),
                    None)
        if free is None:
            d.remove(species, entry, "R25", f"below {lowest}, the lowest level it is had at")
        else:
            d.move(species, entry, free, "R25", f"was below {lowest}, the lowest level it is had at")


def earliest_split(species, level):
    """The earliest split index a player can have the stage at `level`, over
    every way it is first had: the later of that way's split and the split
    the level is reached in. A level below the stage's arrival counts as its
    arrival, where a catch knows the move or the relearner offers it."""
    best = None
    for st, _row in lc.stage_routes(BASE).get(species, ()):
        reached = lc.split_of_level(max(level, st.level, 1)) or SPLITS[-1]
        x = max(si(st.split), si(reached))
        best = x if best is None else min(best, x)
    return best


def holds(species, mv, level):
    """Whether the ceilings hold a move placed or moved to `level` on the
    species' list: an attack at the earliest split a player has it there."""
    x = earliest_split(species, level)
    if x is None:
        return True
    if is_attack(mv):
        return within_ceiling(mv, species, x)
    return M()[mv]["class"] != "STATUS" or utility_within(mv, species, x)


def strong(mv):
    """A move worth bringing within reach: an attack of WEAK_POWER or more,
    or a status move Ian's scale rates good or better."""
    return lc.counts(mv) and ((is_attack(mv) and lc.effective_power(mv) >= WEAK_POWER)
                              or (M()[mv]["class"] == "STATUS" and rank(mv) >= lc.GOOD))


def bring_up(d, species):
    """Ian on a strong move at 6 that every catch at 29 misses (the exam,
    2026-10-06): "a travesty with how good it is". On a line's first stage,
    a strong move below the lowest level it is caught or hatched at, which
    that catch does not know among its four, is lost but for the relearner;
    where it would better that catch's kit (learncheck.move_worth), it moves
    to that level or just after, where the ceilings hold it as for an added
    move. An evolved stage's lost moves are fix_lost's (R25)."""
    if pool.pre_evolutions().get(species) or species not in lowest_had():
        return
    low = lowest_had()[species]
    known = calc_trainers.default_moves(d.lists[species], low)
    floor = min((lc.move_worth(m, species) for m in known), default=0) if len(known) >= 4 else 0
    lost = [e for e in d.lists[species] if 2 <= e[0] < low and e[1] not in known and strong(e[1])
            and not any(m == e[1] and lv >= low for lv, m in d.lists[species])
            and lc.move_worth(e[1], species) > floor]
    for entry in sorted(lost, key=lambda e: (-lc.move_worth(e[1], species), e[0])):
        at = next((l for l in range(low, top() + 1) if l not in d.levels(species) and holds(species, entry[1], l)),
                  None)
        if at is not None:
            d.move(species, entry, at, "R25", f"below {low}, the lowest catch, which would not know it")


# ---- pass 3: fill ------------------------------------------------------------------------------------------

def gains(d, path):
    """((level, stage index, MOVE_X, how), ...) along a path, from the draft
    lists: learncheck.path_events's rule, read from the lists being written."""
    first = path[0]
    lst0 = d.lists[first.species]
    ev = [(first.level, 0, m, "capture") for m in calc_trainers.default_moves(lst0, first.level)]
    for i, st in enumerate(path):
        lst = d.lists[st.species]
        nxt = path[i + 1].level if i + 1 < len(path) else None
        lo = st.level + 1 if i == 0 else max(st.level, 2)
        if i:
            ev += [(st.level, i, m, "evolving") for lv, m in lst if lv == 0]
        ev += [(lv, i, m, "level-up") for lv, m in lst
               if lv >= lo and lv <= top() and (nxt is None or lv <= nxt)]
    return sorted(ev, key=lambda e: (e[0], e[1]))


def stage_held(d, path, i, level):
    """The moves stage i of a path has by `level` while it is held: what it
    arrives with (known at capture, or carried and learnt on evolving), then
    its own list from its first level up. Unlike gains(), this reads a stage
    past its on-time evolution, as a held stage is (R2, check 8)."""
    st = path[i]
    out = [m for lv, j, m, how in gains(d, path) if j < i or (j == i and how in ("capture", "evolving"))]
    start = st.level + 1 if i == 0 else max(st.level, 2)
    out += [m for lv, m in d.lists[st.species] if start <= lv <= min(level, top())]
    return list(dict.fromkeys(out))


def stage_end(d, path, i):
    """The last level a stage of a path learns from its own list: its
    evolution level when it evolves by level, the League's cap when it is
    final, and for one waiting on an item, the cap of the split after its
    item comes in reach (learncheck.held_splits)."""
    if i + 1 == len(path):
        return top()
    nxt = path[i + 1]
    if nxt.via == "level":
        return nxt.level
    return caps()[SPLITS[min(si(nxt.split) + 1, len(SPLITS) - 1)]]


Slot = collections.namedtuple("Slot", "path index split lo hi kind need")
SPLIT_MOST = 3      # new moves a held stage learns in one split, at most (Ian, 2026-10-06)


def windows(d, path, i):
    """The slots a stage is planned in. "first": the path's first stage in
    its catch split, from the catch level up (R1 and R2; a late catch or gift
    learns everything up to the cap there, R20). "arrival": an evolved
    stage's own split, for what the line needs by then, not for R2; a stage
    reached by an item starts at the level it can first be evolved at (Ian's
    exam verdicts, 2026-10-06). "held": each band of R2_BAND levels
    it is held through (learncheck.held_bands), asking band_need new moves
    (R2 by band, 2026-10-06); its split, for the ceilings, is that of the
    band's first level. A final form reached by an item keeps quiet for two
    splits (R10), but what is due by then still comes in."""
    st = path[i]
    a = si(st.split)
    start = st.level + 1 if i == 0 else max(st.level, 2)
    end = stage_end(d, path, i)
    by_item = i > 0 and st.via not in ("caught", "level")
    out = []
    xs = [(a, "first" if i == 0 else "arrival")]
    if i + 1 == len(path) and by_item and lc.family(st.species) not in lc.STONE_EXCEPTIONS:
        xs += [(x, "arrival") for x in range(a + 1, a + 3)]
    # The levels a stage spends in the split it evolves in by level, before
    # evolving: no R2 count asks for them, but what is due may come there
    # (Steenee's 17 to 25 in Gardenia's split, before Tsareena at 26).
    if i + 1 < len(path) and path[i + 1].via == "level":
        e = si(path[i + 1].split)
        if e > a and e not in lc.held_splits(path, i):
            xs.append((e, "arrival"))
    for x, kind in xs:
        if x >= len(SPLITS):
            continue
        lo, hi = lc.window(SPLITS[x])
        lo = start if kind == "first" or (by_item and x == a) else max(lo, start)
        hi = min(hi, end)
        if lo <= hi:
            out.append(Slot(path, i, x, lo, hi, kind, 0))
    for lo, hi in lc.held_bands(path, i):
        need = lc.band_need(lo, hi)
        lo, hi = max(lo, start), min(hi, end)
        if lo <= hi:
            out.append(Slot(path, i, si(lc.split_of_level(lo)), lo, hi, "held", need))
    return out


def split_new(d, holder, x):
    """How many counted moves the holder's list teaches in split x's levels."""
    lo, hi = lc.window(SPLITS[x])
    return len({m for lv, m in d.lists[holder] if lo <= lv <= hi and lc.counts(m)})


class Needs:
    """What a line still lacks at a point of its path, by the locked rules."""

    def __init__(self, d, fam, path, slot, first):
        self.fam, self.slot, self.first = fam, slot, first
        st = path[slot.index]
        self.holder = st.species
        self.held = stage_held(d, path, slot.index, slot.hi)
        self.before = set(stage_held(d, path, slot.index, slot.lo - 1))
        holder = self.holder
        types = lc.types_of(holder)
        x = slot.split
        # R11 and check 1: an attack of each type, a same-type one of 50,
        # due within a split of the stage being had; asked for from its first split.
        due = x <= si(st.split) + 1 or x <= first + 1
        self.types = {t for t in types if not any(is_attack(m) and M()[m]["type"] == t for m in self.held)}
        self.stab50 = due and not any(is_attack(m) and M()[m]["type"] in types and lc.usable(m, types)
                                      for m in self.held)
        if not due:
            self.types = set()
        # R4 and R5: coverage by the second split, then a new type every few splits.
        cover = {M()[m]["type"] for m in self.held if lc.coverage(m, holder, lc.COVER_LATE)}
        any_cover = any(lc.coverage(m, holder, lc.COVER_EARLY) for m in self.held)
        final = path[-1].species
        need_types = lc.R5_STRONG_TYPES if sum(lc.stats(final).values()) >= lc.R5_STRONG_BST else lc.R5_TYPES
        target = 0 if x < first + 1 else 1 if x < first + 4 else 2 if x < first + 6 else need_types
        self.cover_early = not any_cover and x <= first + 1
        self.cover_more = len(cover) < target
        self.cover_have = cover | {M()[m]["type"] for m in self.held if lc.coverage(m, holder, lc.COVER_EARLY)}
        # The coverage a line may have by level-up: R5's count and one more;
        # one more again for a mixed attacker strong on both stats (R23, R34).
        atk, spa = lc.attack_stats(final)
        mixed = min(atk, spa) >= 80 and min(atk, spa) >= 0.85 * max(atk, spa)
        self.room = len(self.cover_have) < need_types + 1 + (1 if mixed else 0)
        self.kaizo = set(lc._kaizo_cover(path, final))
        # R7: a good utility move by the second split; two over the game
        # for a less offensive line.
        good = [m for m in self.held if lc.utility(m) and (lc.tier(m) or (0,))[0] >= lc.GOOD]
        offense = max(lc.attack_stats(final))
        self.utility = (not good and x <= first + 1) or \
            (offense < lc.R7_LOW_OFFENSE and len(good) < lc.R7_LOW_GOOD and x >= first + 2)
        self.utilities = sum(1 for m in self.held if lc.utility(m) and not is_attack(m))
        self.attacks = sum(1 for m in self.held if is_attack(m))
        # R30: a strong same-type attack on the stage by mid-game.
        self.strong = x >= max(first + 3, si(st.split)) and not any(
            is_attack(m) and M()[m]["type"] in types and lc.effective_power(m) * ratio(m, holder) >= 80
            for m in self.held)
        # R16: a later-generation move on every line.
        self.later = not any(later_gen(m) for m in self.held)
        self.r1 = 0     # how many moves R1 still lacks; fill_slot sets it in a first split
        # A real move from 61 on each final form (2026-09-28), asked for from
        # the Galactic split.
        self.late = slot.index == len(path) - 1 and x >= SPLITS.index("Galactic") and not any(
            lc.LATE_FROM <= lv <= top() and lc.counts(m) for lv, m in d.lists[holder])

    def unmet(self):
        # R30 asks for the final form's strong same-type attack in good time,
        # so on a final stage it is due, not only welcome.
        final_strong = self.strong and self.slot.index == len(self.slot.path) - 1
        # R16 is due from the line's third split: every line gets a newer move.
        later_due = self.later and self.slot.split >= self.first + 2
        # R5's coverage over the game is due on the final form, now that the
        # bands no longer ask a count of every split (2026-10-06).
        final_cover = self.cover_more and self.slot.index == len(self.slot.path) - 1
        return bool(self.types or self.stab50 or self.cover_early or self.utility or self.late
                    or final_strong or later_due or final_cover)


@functools.lru_cache(maxsize=None)
def family_pool(fam):
    """The moves worth scoring for a line: every move the generator may add
    that is not another line's signature and, for an attack, is linked to
    the line or of a type its members have or reach."""
    types = set(linked_types(fam))
    for sp in lc.families()[fam]:
        types |= lc.types_of(sp)
    out = []
    for c, m in M().items():
        if never_added(c) or signature(c, fam):
            continue
        if m["class"] != "STATUS" and c not in links(fam) and m["type"] not in types:
            continue
        out.append(c)
    return tuple(out)


def candidates(d, fam, holder, slot, needs):
    """[(score, MOVE_X, what it answers)], best first, for one slot."""
    out = []
    holder_types = lc.types_of(holder)
    on_list = {m for lv, m in d.lists[holder] if lv >= 2}
    # A move the list teaches after the slot may come into it (fill_slot
    # moves the entry), under the same ceilings: while R1 is short, or to
    # answer something due (a form's first attack of its type, at 35).
    later = {m for lv, m in d.lists[holder] if lv > slot.hi and not never_added(m)}
    held = set(needs.held)
    # The line's recovery so far: one recovery move at most is added, and
    # only to a path with none (Ian, 2026-10-06: few recovery moves a list).
    path_moves = held | {m for st in slot.path for lv, m in d.lists[st.species] if lv >= 2}
    line_heals = any(heals(m) for m in path_moves)
    kin = related(holder)
    # The lowest rung of each type the holder has a move to stand on, so
    # that where a type's ladder has nothing for it at the climbing point,
    # the next rung up with something is the step, not a gap left open
    # (R11, R4). A coverage move may do so only up to the line's own level,
    # the higher of its best attack and the split's starting point: Chinchou's
    # only Bug move, Signal Beam, is no level-4 move.
    first = slot.kind == "first"
    no_attack = {t for t in holder_types if not any(is_attack(h) and M()[h]["type"] == t for h in held)}
    foot = {}
    for c in family_pool(fam):
        t = M()[c]["type"]
        if t not in no_attack or c in held or not is_attack(c) or plausibility(c, fam, holder) <= 0:
            continue
        if not lc.fits(c, holder) and slot.split > 1:
            continue
        # The lowest move the line has of the type, as a power, over both
        # sides: Vullaby's Bite, not the Dark Pulse at the foot of special Dark.
        foot[t] = min(foot.get(t, 999), standing(c, holder))
    room_cache = {}

    def reach_of(c):
        """The highest rung the candidate's type and side allow it here."""
        k = (M()[c]["type"], side_for(c, holder))
        if k not in room_cache:
            reach = climb_room(holder, k[0], needs.before, slot.split, first, k[1])
            if k[0] in foot:
                reach = max(reach, rung(foot[k[0]], k[0], k[1]))
            room_cache[k] = reach
        return room_cache[k]
    # Whether a move on the line's better stat stands within reach of each
    # type: an off-stat one fills an early gap only where none does (Abra's
    # Psycho Cut, Geodude's Mud Bomb).
    fit_in_reach = collections.defaultdict(bool)
    for c in family_pool(fam):
        if is_attack(c) and lc.fits(c, holder) and c not in held and plausibility(c, fam, holder) > 0 \
                and rung_of(c, holder) <= reach_of(c):
            fit_in_reach[M()[c]["type"]] = True
    for c in family_pool(fam) + tuple(sorted(later - set(family_pool(fam)))):
        if c in held or (c in on_list and c not in later):
            continue
        if line_heals and heals(c):
            continue
        if c in lc.CATCH_ONLY and slot.split > si(lc.CATCH_ONLY_UNTIL):
            continue
        p = plausibility(c, fam, holder)
        if p <= 0:
            continue
        m = M()[c]
        why, score = [], 0.0
        if m["class"] != "STATUS":
            stab = m["type"] in holder_types
            # Climb, don't jump: the attack stands no more than a rung or two
            # above what the line had before this slot (the type ladders).
            if not is_attack(c):
                continue
            if rung_of(c, holder) > reach_of(c):
                continue
            # An attack uses a stat that fits (R15); an off-stat one of the
            # holder's type fills only an early gap, a type with no attack
            # (R11) or no usable same-type attack (check 1), in the first two
            # splits, and only where no move on its better stat is in reach
            # (R3; Ian, 2026-10-06).
            # A line whose ability sets its side (Huge Power) takes no
            # off-stat move at all (Ian, 2026-10-06, on Marill's Alluring Voice).
            if not lc.fits(c, holder) and not (stab and slot.split <= 1 and not fit_in_reach.get(m["type"])
                                               and not abilities(holder) & lc.ATTACK_DOUBLERS
                                               and (m["type"] in needs.types or needs.stab50)):
                continue
            value = attack_value(c, holder)
            if slot.split >= LATE_SPLIT and lc.effective_power(c) < LATE_POWER \
                    and not (distinct(c) and lc.effective_power(c) >= LATE_DISTINCT_POWER):
                continue
            same = [h for h in held if is_attack(h) and M()[h]["type"] == m["type"]]
            best_same = max((attack_value(h, holder) for h in same), default=0)
            upgrade = value > 1.05 * best_same
            # A weaker move of the type earns its place by what it brings
            # (priority, a switch, sure speed control, draining) when nothing
            # of the type held brings it already, or by a strong secondary
            # effect close to the best of the type (R6 as narrowed).
            brings = _property(c)
            new_property = brings and not any(_property(h) == brings for h in same)
            if same and not upgrade and not new_property \
                    and not (distinct(c) and value >= 0.85 * best_same):
                continue
            if not stab and m["type"] not in needs.cover_have and not needs.room:
                continue    # the line has all the coverage types it may (R5, R35)
            if flagged(holder) and lc.effective_power(c) >= 80:
                floor = kaizo_floor(fam, c)
                if floor and floor > slot.hi:
                    continue
            score = value / 2
            # The old ceiling stays only as a weight: power felt over it costs score.
            cover = not stab and m["type"] != "NORMAL"
            score -= max(0.0, felt(c, holder) - ceiling(holder, slot.split, cover))
            if m["type"] in needs.types:
                score += 200
                why.append("R11")
            if needs.stab50 and stab and lc.usable(c, holder_types):
                score += 150
                why.append("check 1")
            if not stab and lc.coverage(c, holder, lc.COVER_EARLY) and needs.cover_early:
                score += 120
                why.append("R4")
            if not stab and lc.coverage(c, holder, lc.COVER_LATE) and m["type"] not in needs.cover_have:
                score += 60 if needs.cover_more else 15
                score += 25 if m["type"] in needs.kaizo else 0
                why.append("R5")
            if needs.strong and stab and lc.effective_power(c) * ratio(c, holder) >= 80:
                score += 100
                why.append("R30")
            if needs.attacks < needs.utilities:
                score += 10
            if not stab and c in relearn_only(fam):
                score += 30     # the line's own coverage, else only relearnt (Ian's exam verdicts, 2026-10-06)
                why.append("relearner-only")
        else:
            listed = (lc.tier(c) or (0,))[0]    # Ian's tier or the list's, as the checks read it
            r = rank(c)                 # with the generator's reading of the unrated ones
            if listed == lc.TIER_RANK["SSS"] and branch_links(holder).get(c, 0) < 1.0:
                continue    # SSS is rationed: only with a strong link to the line
            if r < lc.TIER_RANK["Okay"]:
                continue    # a bad, useless or terrible move is never added
            if r < lc.GOOD and (branch_links(holder).get(c, 0) < 1.0 or slot.split > 1):
                continue    # an okay one only early, and only with a strong link (Popplio's Sing)
            if not utility_within(c, holder, slot.split) or not utility_fits(d, c, holder, fam):
                continue
            kind = lc.boosts(c)
            if kind and not (c == "MOVE_CURSE" and "GHOST" in holder_types):
                # R32 at the moment of choosing: the line has a strong attack
                # this boosts by the end of the next split, as settle_family
                # will ask.
                evs = [(lv, slot.path[j].species, m2) for lv, j, m2, _h in gains(d, slot.path)]
                horizon = caps()[SPLITS[min(slot.split + 1, len(SPLITS) - 1)]]
                if not _boost_ready(kind, evs, horizon):
                    continue
            score = r * 7
            if needs.utility and listed >= lc.GOOD:
                score += 120
                why.append("R7")
            if needs.utilities >= 4:
                score -= 40
            if needs.utilities > needs.attacks:
                score -= 15
        # A move answering nothing due comes in only on the line's own
        # links: a status move the line learns by level-up somewhere (canon,
        # Kaizo or Oxide), an attack it learns by any way, or a stronger
        # attack of its own type. The whole pool serves what the rules ask
        # for; filling a count does not reach into it (R2 left short instead).
        if needs.late:
            score += 50
            why.append("late move")
        if m["class"] != "STATUS" and lc.effective_power(c) < WEAK_POWER and not (m["priority"] or 0) > 0 \
                and not speed_control(c) and not ("R11" in why and slot.kind == "first") \
                and "R4" not in why \
                and not (slot.kind == "first" and needs.r1 > 0 and m["type"] in holder_types
                         and lc.effective_power(c) >= lc.COVER_EARLY):
            continue
        if needs.later and later_gen(c):
            due = slot.split >= needs.first + 2
            score += 60 if due else 20
            why.append("R16 due" if due else "R16")
        need = bool(set(why) & {"R11", "check 1", "R4", "R7", "R30", "late move", "R16 due"}) \
            or ("R5" in why and needs.cover_more)
        link = branch_links(holder).get(c, 0)
        if c in later and not need and needs.r1 <= 0:
            continue    # moving a move earlier only to fill a count is no change worth making
        if not need:
            # A move that only fills a count must fit the line well (Ian,
            # 2026-10-06): a status move it learns by level-up somewhere and
            # Ian rates good or better; an attack on its better stat, linked
            # to it or a stronger one of its own type; and never a filler a
            # sibling branch got already, so branches do not share filler.
            if m["class"] == "STATUS" and (link < 1.0 or rank(c) < lc.GOOD):
                continue
            if m["class"] != "STATUS" and (not lc.fits(c, holder) or
                                           (link < 0.85 and not (m["type"] in holder_types and upgrade))):
                continue
            if any(sp not in kin for sp in d.filler[fam].get(c, ())):
                continue
        hints = level_hints(fam, c)
        if any(slot.lo - 5 <= h <= slot.hi + 5 for h in hints):
            score += 10
        out.append((score * p, c, tuple(why) or ("R2",)))
    out.sort(key=lambda e: (-e[0], e[1]))
    return out


@functools.lru_cache(maxsize=None)
def relearn_only(fam):
    """The moves the line's lists teach only at level 1 of an evolved form:
    the relearner's alone, worth almost nothing to the player (Ian,
    2026-09-27), though they are the line's own. Ian in the exam
    (2026-10-06): a line's "total move pool is very slim given no elemental
    fang coverage", which its evolution had only at level 1."""
    line = lc.families()[fam]
    later = {m for sp in line for lv, m in lc.learnset(BASE, sp) if lv >= 2 or lv == 0}
    return frozenset(m for sp in line if pool.pre_evolutions().get(sp)
                     for lv, m in lc.learnset(BASE, sp) if lv == 1 and m not in later)


@functools.lru_cache(maxsize=None)
def related(species):
    """The species on the holder's own branch: itself, what it evolves from
    and what it can evolve into."""
    up = set(pool.pre_evolutions().get(species) or [])
    down, todo = set(), [species]
    while todo:
        for _n, _i, t in pool.evolutions(todo.pop()):
            if t not in down:
                down.add(t)
                todo.append(t)
    return frozenset(up | down | {species})


def can_boost(d, holder):
    """R21's test for Baton Pass: the holder itself has a boost to pass, on
    its own list or one it carries from what it evolves from (the exam's
    regressions, 2026-10-06: Baton Pass on a first stage with none of its own)."""
    own = [holder] + list(pool.pre_evolutions().get(holder) or [])
    setup = set(lc.setup_moves())       # check 15's reading
    return any(mv in setup for s in own for lv, mv in d.lists[s] if lv >= 2)


def utility_fits(d, c, holder, fam):
    """Whether a status move suits the holder: setup only beside attacks it
    boosts (R32), Baton Pass only with a boost on the line (R21), defensive
    boosts only on a bulky line or one shielded from critical hits (R31)."""
    m = M()[c]
    kind = lc.boosts(c)
    if kind:
        atk, spa = lc.attack_stats(holder)
        if kind == "PHYSICAL" and atk < 0.85 * max(atk, spa):
            return False
        if kind == "SPECIAL" and spa < 0.85 * max(atk, spa):
            return False
        if kind == "ELECTRIC" and "ELECTRIC" not in lc.types_of(holder):
            return False
    if c == "MOVE_BATON_PASS":
        return can_boost(d, holder)
    if m["effect"] in DEFENSIVE_EFFECTS:
        s = lc.stats(holder)
        return max(s.get("defense", 0), s.get("special_defense", 0)) >= BULKY or abilities(holder) & CRIT_SHIELDS
    return True


def pick_level(d, holder, fam, c, slot, due=False):
    """A free level in the slot for the move: nearest a later game's or
    Generation 4's level for it when one falls inside, else the earliest
    free level (lists fill from the front). Outside a first split, none in a
    split whose levels already teach SPLIT_MOST new moves, one more for a
    move a rule makes due (`due`); a catch-only move only by Fantina's cap."""
    used = d.levels(holder)
    free = [l for l in range(slot.lo, slot.hi + 1) if l not in used]
    starter = holder in lc.STARTERS
    if starter:
        # Nothing joins a starter's two basics at or below 5 (Ian, 2026-10-07).
        free = [l for l in free if l > lc.STARTER_LEVEL]
    if flagged(holder) and lc.effective_power(c) >= 80:
        floor = kaizo_floor(fam, c)
        if floor:
            free = [l for l in free if l >= floor]
    if slot.kind != "first":
        free = [l for l in free if split_new(d, holder, si(lc.split_of_level(l))) < SPLIT_MOST + (1 if due else 0)]
    else:
        # A catch that would know fewer than KIT_AT_CATCH counted moves takes
        # the move at or just below its level, so it knows it when caught (the
        # exam's regressions, 2026-10-06: a line caught at 9 knew only Pound).
        caught = slot.lo - 1
        known = [m for m in calc_trainers.default_moves(d.lists[holder], caught) if lc.counts(m)]
        floor = kaizo_floor(fam, c) if flagged(holder) and lc.effective_power(c) >= 80 else None
        if len(known) < KIT_AT_CATCH and not (floor and floor > caught) and not starter:
            below = [l for l in range(caught, max(2, caught - 3) - 1, -1) if l not in used]
            if below:
                return below[0]
    if c in lc.CATCH_ONLY:
        free = [l for l in free if l <= caps()[lc.CATCH_ONLY_UNTIL]]
    if not free:
        return None
    # A late catch or gift learns its first split's moves all at once (R20),
    # so they sit in the split's own levels where there is room, as a list
    # reads naturally.
    if slot.kind == "first":
        own = [l for l in free if l >= lc.window(SPLITS[slot.split])[0]]
        free = own or free
    hints = [h for h in level_hints(fam, c) if slot.lo <= h <= slot.hi]
    if hints:
        return min(free, key=lambda l: (min(abs(l - h) for h in hints), l))
    # Lists fill from the front (Ian, 2026-10-06): the earliest free level
    # not next to another move, else the earliest free level.
    return next((l for l in free if l - 1 not in used and l + 1 not in used), free[0])


R1_EXTRA = 2      # the first split may take two moves more than R2's three (a catch may know none)
KIT_AT_CATCH = 3  # counted moves a catch should know when caught, where the first split adds any


DUE = {"R11", "check 1", "R4", "R7", "late move", "R30", "R16 due"}


def count_only(why, needs):
    """Whether an addition answers nothing the line lacks: it only fills a count (R1, R2)."""
    return not set(why) & DUE and not ("R5" in why and needs.cover_more)


def fill_slot(d, fam, slot, first):
    """Add moves to one slot until it has the new moves its band asks for
    (R2) and the line lacks nothing due, at most three additions (R2's "two
    or three"), two more in the first split (R1)."""
    path, i = slot.path, slot.index
    holder = path[i].species
    added = 0
    limit = 3 + (R1_EXTRA if slot.kind == "first" else 0)
    while added < limit:
        needs = Needs(d, fam, path, slot, first)
        new = [m for lv, m in d.lists[holder]
               if slot.lo <= lv <= slot.hi and lc.counts(m) and m not in needs.before]
        new = list(dict.fromkeys(new))
        r1 = _r1_short(d, path, first) if slot.kind == "first" else 0
        needs.r1 = r1
        short = (slot.kind == "held" and len(new) < slot.need) or r1 > 0
        if not short and not needs.unmet():
            return
        cands = candidates(d, fam, holder, slot, needs)
        if not short:
            # Counts are met; only a move that answers something due may come in.
            cands = [c for c in cands if not count_only(c[2], needs)]
        level = None
        for score, c, why in cands:
            level = pick_level(d, holder, fam, c, slot, due=not count_only(why, needs))
            if level is not None:
                break
        if level is None:
            return
        if count_only(why, needs):
            d.filler[fam][c].add(holder)
        rule = "R1" if r1 > 0 and "R2" in why else ", ".join(why)
        old = next((e for e in d.lists[holder] if e[1] == c and e[0] > slot.hi), None)
        if old:
            d.move(holder, old, level, rule, f"brought into {SPLITS[slot.split]}'s split; score {score:.0f}")
        else:
            d.add(holder, level, c, rule, f"{SPLITS[slot.split]}'s split; score {score:.0f}")
        added += 1


def _r1_short(d, path, first):
    """How many moves the line's first split still lacks for R1: counted
    moves by the cap, at most one of them filler."""
    if si(path[0].split) != first:
        return 0
    cap = caps()[path[0].split]
    got, fill = [], 0
    for lv, i, m, _h in gains(d, path):
        if lv <= cap and m not in got and lc.counts(m):
            got.append(m)
            fill += lc.filler(m, path[i].species)
    return max(lc.R1_MOVES - len(got), lc.R1_MOVES - lc.R1_FILLER - (len(got) - fill))


def trim_filler(d, path, first):
    """R1's flavour: past one, a filler move known at capture or learnt in
    the first split gives way, the weakest first (a plain Normal attack
    stays when it is the catch's only attack)."""
    if si(path[0].split) != first:
        return
    cap = caps()[path[0].split]
    sp = path[0].species
    fill = list(dict.fromkeys(m for lv, i, m, _h in gains(d, path)
                              if lv <= cap and i == 0 and lc.counts(m) and lc.filler(m, sp)))
    remaining = len(fill)
    # Status filler goes before an attacking opener, the lowest tier first.
    for mv in sorted(fill, key=lambda m: (is_attack(m), (lc.tier(m) or (5,))[0], m)):
        if remaining <= lc.R1_FILLER:
            break
        lst = d.lists[sp]
        entry = next((e for e in lst if e[1] == mv), None)
        if entry is None:
            continue
        rest = [m for lv, m in lst if m != mv and is_attack(m) and lv <= path[0].level]
        if is_attack(mv) and not rest:
            continue        # the catch's only attack stays, and still counts
        d.remove(sp, entry, "R1", "filler past the one a first split may carry")
        remaining -= 1


def known_move_evolutions(d, fam):
    """Every evolution that needs a known move gets the move on the
    pre-evolution's list by level-up, in the first split it is held at the
    cap of (check 20)."""
    for pre, mv, target in lc.know_move_evolutions():
        if lc.family(pre) != fam or d.has(pre, mv):
            continue
        for path in lc.line_paths(BASE, fam):
            idx = next((i for i, st in enumerate(path) if st.species == pre), None)
            if idx is None:
                continue
            slots = windows(d, path, idx)
            if not slots:
                continue
            slot = slots[1] if len(slots) > 1 and idx == 0 else slots[0]
            level = pick_level(d, pre, fam, mv, slot)
            if level is not None:
                d.add(pre, level, mv, "check 20", f"{lc.species_name(target)} needs it known")
            break


def by_depth(fam):
    """A line's species, earliest stage first, so a pass over the line sees
    a pre-evolution's list settled before its evolution's."""
    return sorted(lc.families()[fam], key=lambda s: (len(pool.pre_evolutions().get(s) or []), s))


def _boost_ready(kind, evs, upto):
    grades = {m2: lc._boosted(kind, m2, path_species) for lv2, path_species, m2 in evs if lv2 <= upto}
    return 2 in grades.values() or sum(1 for g in grades.values() if g) >= 2


def place_setup(d, path, i, entry, kind):
    """R32: a setup move with no strong attack it boosts by the next split
    moves to the split before the one where the line has such attacks, on
    the stage that holds it then; with none by the League, it goes to the
    palette."""
    holder = path[i].species
    evs = [(lv, path[j].species, m) for lv, j, m, _h in gains(d, path)]
    ready = next((lv for lv, _s, _m in sorted(evs) if _boost_ready(kind, evs, lv)), None)
    if ready is None:
        d.to_palette(holder, entry, "R32", "no strong attack it boosts on the line")
        return
    want = max(entry[0], lc.window(SPLITS[max(si(lc.split_of_level(ready)) - 1, 0)])[0])
    for j in range(i, len(path)):
        st = path[j]
        lo = max(want, st.level + 1 if j == 0 else max(st.level, 2))
        hi = stage_end(d, path, j)
        free = [l for l in range(lo, hi + 1) if l not in d.levels(st.species)]
        if free:
            d.lists[holder].remove(entry)
            d.note(holder, entry[0], entry[1], "removed", "R32", f"too early: strong attacks it boosts come at {ready}")
            d.add(st.species, free[0], entry[1], "R32", f"moved from {lc.species_name(holder)}'s {entry[0]}, "
                                                      f"beside the attacks it boosts")
            return
    d.to_palette(holder, entry, "R32", "no level free once the attacks it boosts arrive")


def settle_family(d, fam):
    """After the fill, the rules no single addition could see: Baton Pass
    goes to the palette where the line has no boost to pass (R21); a setup
    move without a strong attack it boosts by the next split moves to where
    it has one (R32); a plain attack learnt after a stronger one of its type
    and class goes (R6). R25 runs first, over what the fill moved, so
    nothing it brings back escapes the rest. R8's choices inside one split
    are left alone: they cost the player nothing (Ian, 2026-10-06)."""
    line = by_depth(fam)
    for sp in line:
        fix_lost(d, sp)
    for s in line:
        if not can_boost(d, s):
            for e in [e for e in d.lists[s] if e[1] == "MOVE_BATON_PASS" and e[0] >= 2]:
                d.to_palette(s, e, "R21", "no boost of its own to pass")
    last = len(SPLITS) - 1
    for path in lc.line_paths(BASE, fam):
        for lv, i, mv, how in gains(d, path):
            holder = path[i].species
            kind = lc.boosts(mv)
            if not kind or (mv == "MOVE_CURSE" and "GHOST" in lc.types_of(holder)):
                continue
            evs = [(lv2, path[j].species, m2) for lv2, j, m2, _h in gains(d, path)]
            horizon = caps()[SPLITS[min(lc.event_split(path, i, lv) + 1, last)]]
            if _boost_ready(kind, evs, horizon):
                continue
            src = path[0].species if how == "capture" else holder
            entry = next((e for e in d.lists[src] if e[1] == mv and (how == "capture" or e[0] == lv)), None)
            if entry:
                place_setup(d, path, 0 if how == "capture" else i, entry, kind)
        held = []
        for lv, i, mv, how in gains(d, path):
            m = M()[mv]
            holder = path[i].species
            if how in ("level-up", "evolving") and m["class"] != "STATUS" and not m["priority"]:
                # A plain attack, or one whose effect a stronger held attack
                # brings as well (Mega Drain after Giga Drain), brings nothing.
                same_effect = lambda n: (M()[n]["effect"] == m["effect"]
                                         and (M()[n]["effect_chance"] or 0) >= (m["effect_chance"] or 0))
                stronger = next((n for n in held if n != mv and M()[n]["type"] == m["type"]
                                 and M()[n]["class"] == m["class"] and lc.reliable(n)
                                 and lc.effective_power(n) > lc.effective_power(mv)
                                 and lc._acc(n) >= lc._acc(mv)
                                 and (m["effect"] in PLAIN or same_effect(n))), None)
                entry = next((e for e in d.lists[holder] if e[1] == mv and e[0] == (0 if how == "evolving" else lv)),
                             None)
                if stronger and entry:
                    d.remove(holder, entry, "R6", f"weaker than {name(stronger)}, already had")
                    continue
            if mv not in held:
                held.append(mv)


# R19's second kind of delay demon: a middle stage that evolves by level
# late into a strong final form, held past about 66, earns payoff moves the
# early evolver never gets by level-up, a top setup move among the prizes.
DEMON_LEVEL, DEMON_BST, DEMON_LEVELS, DEMON_POWER = 30, 530, (66, 69), 100


def delay_demons(d, fam):
    """R19 for one line: on each middle stage that evolves by level at
    DEMON_LEVEL or later into a final form of DEMON_BST or more, the
    strongest linked same-type attack its final form does not learn by
    level-up by the League, and the best linked setup move that boosts its
    attacking stat, at 66 and 69."""
    for pre, level, target in lc.level_evolutions():
        if lc.family(pre) != fam or level < DEMON_LEVEL or not pool.pre_evolutions().get(pre):
            continue
        if sum(lc.stats(target).values()) < DEMON_BST or target not in b6.obtainable():
            continue
        final_has = {m for lv, m in d.lists[target] if lv == 0 or level <= lv <= top()}
        on_pre = {m for lv, m in d.lists[pre]}
        # The prize must be big (Ian: "a very big payoff", "incredible payoff
        # moves"): a same-type attack of DEMON_POWER or more, stronger than any
        # of its type the final form learns, or an SSS setup move.
        final_best = {t: max((attack_value(m, target) for m in final_has
                              if is_attack(m) and M()[m]["type"] == t), default=0)
                      for t in lc.types_of(pre)}
        prizes = []
        # A rampage move may be the prize at its reworked, one-turn numbers.
        power = lambda c: lc.effective_power(c) if is_attack(c) else 0
        value = lambda c, sp: power(c) * (1.5 if M()[c]["type"] in lc.types_of(sp) else 1.0) * ratio(c, sp)
        attacks = sorted((c for c in branch_links(pre) if is_attack(c) and not never_added(c)
                          and M()[c]["type"] in lc.types_of(pre) and lc.fits(c, pre)
                          and power(c) >= DEMON_POWER
                          and value(c, target) > final_best.get(M()[c]["type"], 0)
                          and c not in final_has and c not in on_pre),
                         key=lambda c: (-value(c, pre), c))
        if attacks:
            prizes.append((attacks[0], "R19", "payoff for holding past 66"))
        setups = sorted((c for c in branch_links(pre) if lc.boosts(c) and not never_added(c) and c not in on_pre
                         and (lc.tier(c) or (0,))[0] == lc.TIER_RANK["SSS"]
                         and utility_fits(d, c, pre, fam) and c not in final_has),
                        key=lambda c: (-branch_links(pre).get(c, 0), c))
        if setups:
            prizes.append((setups[0], "R19", "setup prize for holding past 66"))
        for (c, rule, why), want in zip(prizes, DEMON_LEVELS):
            free = next((l for l in range(want, top() + 1) if l not in d.levels(pre)), None)
            if free is not None:
                d.add(pre, free, c, rule, f"{why}; {lc.species_name(target)} comes at {level}")


def heals(const):
    return const in M() and M()[const]["effect"] in lc.RECOVERY_EFFECTS


def boost_branch(d, fam, path, j, cap, current):
    """Add to stage j of a path the fitting move that adds most to its kit
    by `cap` (learncheck.kit_worth), inside the ceilings and SPLIT_MOST, a
    linked move first. Returns whether one went in."""
    st = path[j]
    holder = st.species
    lo, hi = max(st.level, 2), min(cap, stage_end(d, path, j))
    held = [m for lv, _i, m, _h in gains(d, path) if lv <= cap]
    line_heals = any(heals(m) for m in held) or any(heals(m) for s in path for lv, m in d.lists[s.species]
                                                    if lv >= 2)
    best = None
    for c in family_pool(fam):
        if c in held or d.has(holder, c) or c in lc.CATCH_ONLY or (line_heals and heals(c)):
            continue
        p = plausibility(c, fam, holder)
        if p <= 0:
            continue
        if M()[c]["class"] == "STATUS":
            if branch_links(holder).get(c, 0) < 1.0 or rank(c) < lc.GOOD or not utility_fits(d, c, holder, fam):
                continue
            fits = lambda l: utility_within(c, holder, max(si(st.split), si(lc.split_of_level(l))))
        else:
            if not is_attack(c) or not lc.fits(c, holder):
                continue
            fits = lambda l: climbs(c, holder, held, max(si(st.split), si(lc.split_of_level(l))))
        gain = lc.kit_worth(held + [c], holder) - current
        if gain <= 0:
            continue
        level = next((l for l in range(lo, hi + 1) if l not in d.levels(holder) and fits(l)
                      and split_new(d, holder, si(lc.split_of_level(l))) < SPLIT_MOST), None)
        if level is None:
            continue
        key = (gain * p, -level, c)
        if best is None or key > best[0]:
            best = (key, c, level, gain)
    if best is None:
        return False
    _k, c, level, gain = best
    d.add(holder, level, c, "check 24", f"branch parity by {lc.split_of_level(cap)}'s cap; adds {gain:.0f} to its kit")
    return True


def balance_branches(d, fam):
    """Branches of one line close in worth by the split where the player
    chooses between them (Ian's exam verdicts, 2026-10-06; check
    24): while the weakest branch's kit is under BRANCH_PARITY of the
    strongest's by that split's cap, the weakest branch that can take a move
    gets one, at most three a branch."""
    groups = collections.defaultdict(dict)
    for path in lc.line_paths(BASE, fam):
        for i in range(len(path) - 1):
            groups[tuple(st.species for st in path[:i + 1])].setdefault(path[i + 1].species, (path, i + 1))
    for key, branches in sorted(groups.items()):
        if len(branches) < 2:
            continue
        cap = caps()[SPLITS[max(si(p[j].split) for p, j in branches.values())]]
        given = collections.Counter()
        while True:
            ws = {t: lc.kit_worth([m for lv, _i, m, _h in gains(d, p) if lv <= cap], t)
                  for t, (p, j) in branches.items()}
            top_worth = max(ws.values())
            weak = sorted((t for t in ws if ws[t] < lc.BRANCH_PARITY * top_worth and given[t] < 3),
                          key=lambda t: ws[t])
            if not weak:
                break
            for t in weak:
                if boost_branch(d, fam, *branches[t], cap, ws[t]):
                    given[t] += 1
                    break
                given[t] = 3        # nothing fits: this branch is done
            else:
                break


def rework_stone_forms(d, fam):
    """Ian's exception to R10 (learncheck.STONE_EXCEPTIONS): each stone form
    gets a list of its own from the level it arrives at. The copies of the
    first stage's list it carries that count for nothing or that Ian rates
    below good go (the exam's regressions, 2026-10-06: Last Resort 50,
    Sand-Attack and Baby-Doll Eyes on every stone form); the fill then
    builds each form's list by its own links."""
    if fam not in lc.STONE_EXCEPTIONS:
        return
    base = {m for lv, m in d.lists[fam] if lv >= 2}
    for sp in lc.families()[fam]:
        if sp == fam:
            continue
        for entry in [e for e in d.lists[sp] if e[0] >= 2 and e[1] in base]:
            mv = entry[1]
            if not lc.counts(mv) or (M()[mv]["class"] == "STATUS" and rank(mv) < lc.GOOD):
                d.remove(sp, entry, "R10 exception", f"a copy of {lc.species_name(fam)}'s list; "
                                                     "each form gets its own (Ian, 2026-10-06)")


def plan_family(d, fam):
    rework_stone_forms(d, fam)
    paths = lc.line_paths(BASE, fam)
    first = si(paths[0][0].split)
    for sp in by_depth(fam):
        fix_lost(d, sp)
    known_move_evolutions(d, fam)
    for path in paths:
        trim_filler(d, path, first)
    # Settle what the lists already hold before filling, so the fill sees the
    # gaps the settle would open (a setup move moved off an early level).
    settle_family(d, fam)
    done = set()
    for path in paths:
        for i, st in enumerate(path):
            if st.species in done:
                continue
            done.add(st.species)
            for slot in windows(d, path, i):
                fill_slot(d, fam, slot, first)
    # R1's flavour once more: the fill may have given the catch the attack a
    # filler opener was kept for, so the filler can go now, and the first
    # split is filled again.
    for path in paths:
        trim_filler(d, path, first)
        for slot in windows(d, path, 0):
            if slot.kind == "first":
                fill_slot(d, fam, slot, first)
    balance_branches(d, fam)
    delay_demons(d, fam)
    settle_family(d, fam)
    # The settle can take an opener R1 counted (R6: Bubble after BubbleBeam),
    # so the first split is filled once more, and settled again.
    for path in paths:
        for slot in windows(d, path, 0):
            if slot.kind == "first":
                fill_slot(d, fam, slot, first)
    settle_family(d, fam)


# ---- pass 4: tidy ------------------------------------------------------------------------------------------

def tidy(d, species):
    lst = d.lists[species]
    # No move twice above level 1: the first a player can reach stays (one
    # below the lowest level the stage is had at is the relearner's only).
    low = lowest_had().get(species, 2)
    by_move = collections.defaultdict(list)
    for entry in lst:
        if entry[0] >= 2:
            by_move[entry[1]].append(entry)
    for mv, entries in by_move.items():
        if len(entries) < 2:
            continue
        keep = next((e for e in entries if e[0] >= low), entries[0])
        for entry in entries:
            if entry is not keep:
                d.remove(species, entry, "tidy", "on the list twice")
    # One move a level: a second move on a level moves to the nearest free
    # level of the same split, else goes.
    by = collections.defaultdict(list)
    for entry in lst:
        if entry[0] >= 2:
            by[entry[0]].append(entry)
    for lv, entries in sorted(by.items()):
        for entry in entries[1:]:
            split = lc.split_of_level(lv)
            lo, hi = lc.window(split) if split else (lv, lv)
            free = sorted((l for l in range(lo, hi + 1) if l not in d.levels(species)),
                          key=lambda l: (abs(l - lv), l))
            if free:
                d.move(species, entry, free[0], "tidy", "one move a level")
            else:
                d.remove(species, entry, "tidy", "no free level in its split")
    # At most MAX_ENTRIES: extra level-1 entries go first (the trainers'
    # palette keeps the rest), then the weakest additions.
    while len(lst) > MAX_ENTRIES:
        ones = [e for e in lst if e[0] == 1]
        victim = ones[0] if len(ones) > 4 else min(
            (e for e in lst if e[0] >= 2), key=lambda e: (_worth(e[1], species), -e[0]))
        d.remove(species, victim, "tidy", f"the list is capped at {MAX_ENTRIES} entries")
    lst.sort(key=lambda e: e[0])


def _worth(mv, species):
    if is_attack(mv):
        return attack_value(mv, species)
    t = lc.tier(mv)
    return (t[0] if t else 2) * 10


def no_wild_trainer_move(d, species):
    """A wild Pokemon knows its last four moves by its level, level-1
    entries included when it is met low. A trainer-only move (R26) never
    lands among them (Ian, 2026-10-06, on a wild catch that knew Destiny
    Bond): where a wild catch would know one, the entry goes to the line's
    egg list, the trainers' palette."""
    for sp, _s, lv, how, _p in lc.catch_rows():
        if sp != species or how not in WILD:
            continue
        for mv in calc_trainers.default_moves(d.lists[sp], lv):
            if mv in lc.TRAINER_ONLY:
                entry = next(e for e in d.lists[sp] if e[1] == mv and e[0] <= lv)
                d.to_palette(sp, entry, "R26", f"a wild catch at {lv} would know it")


def ensure_attack_at_capture(d, species):
    """Every catch knows an attack. Where one would know none, the best
    fitting same-type attack from the foot of its ladder goes in (climbing
    from nothing, as a first move does): at level 1 for a catch made that
    low, else at the catch level, the last move the catch knows, a status
    move holding that level moving up one."""
    fam = lc.family(species)
    for sp, split, lv, _h, _p in lc.catch_rows():
        if sp != species:
            continue
        known = calc_trainers.default_moves(d.lists[sp], lv)
        if any(M()[m]["class"] != "STATUS" for m in known if m in M()):
            continue
        # The ceiling of the split the catch's level falls in, not the split
        # it is had in: an egg hatched at 1 late in the game is still level 1.
        level_split = si(lc.split_of_level(max(lv, 1)) or split)
        # A move the list does not teach yet, so no earlier catch loses one,
        # and not one a stronger move the list teaches lower down outclasses (R6).
        on_list = {m for _l, m in d.lists[sp]}
        lower = [m for l, m in d.lists[sp] if l < lv and is_attack(m)]

        def outclassed(c):
            mc = M()[c]
            return mc["effect"] in PLAIN and not mc["priority"] and any(
                M()[x]["type"] == mc["type"] and M()[x]["class"] == mc["class"]
                and lc.effective_power(x) > lc.effective_power(c) and lc._acc(x) >= lc._acc(c) for x in lower)
        cands = sorted((c for c, m in M().items()
                        if m["type"] in lc.types_of(sp) and is_attack(c) and not never_added(c)
                        and climbs(c, sp, (), min(level_split, si(split))) and plausibility(c, fam, sp) > 0
                        and c not in known and c not in on_list and not outclassed(c)),
                       key=lambda c: (-plausibility(c, fam, sp), -attack_value(c, sp), c))
        mv = cands[0] if cands else "MOVE_TACKLE"
        at = 1 if lv <= 1 else lv
        if at >= 2:
            for entry in [e for e in d.lists[sp] if e[0] == at]:
                free = next((l for l in range(at + 1, top() + 1) if l not in d.levels(sp)), None)
                if free is not None:
                    d.move(sp, entry, free, "every catch knows an attack", f"to make room at {at}")
                else:
                    d.remove(sp, entry, "every catch knows an attack", f"to make room at {at}")
            for entry in [e for e in d.lists[sp] if e[1] == mv and e[0] >= 2]:
                d.remove(sp, entry, "every catch knows an attack", f"moved to {at}")
        d.add(sp, at, mv, "every catch knows an attack", f"caught at {lv} in {split}'s split")


# ---- the run ----------------------------------------------------------------------------------------------

def build():
    d = Draft()
    for sp in sorted(d.lists):
        clean(d, sp)
        starter_kit(d, sp)
        bring_up(d, sp)
    for fam in sorted(lc.line_catches()):
        plan_family(d, fam)
    for sp in sorted(d.lists):
        tidy(d, sp)
    # The tidy can shift a level; the line rules run over the result twice,
    # since R6 can take a pre-evolution's copy that R25 counted on.
    for _pass in range(2):
        for fam in sorted(lc.line_catches()):
            settle_family(d, fam)
    for sp in sorted(d.lists):
        tidy(d, sp)
        no_wild_trainer_move(d, sp)
        ensure_attack_at_capture(d, sp)
        # Last, so no step before it can put a third move at a starter's 5.
        starter_kit(d, sp)
    for sp, adds in IAN_EGG_MOVES.items():
        for mv, why in adds:
            if mv not in d.eggs[sp]:
                d.eggs[sp].append(mv)
                d.note(sp, 0, mv, "egg list", "Ian's ruling", why)
    return d


def write(d):
    """Write every changed list into its species file, in the file's own
    style (inline entries or one value a line), touching nothing else."""
    changed = 0
    for sp, lst in sorted(d.lists.items()):
        path = os.path.join(data.ROOT, "res", "pokemon", pokedex.folder_of(sp), "data.json")
        with open(path, encoding="utf-8") as f:
            text = f.read()
        # Compared with the file as it is now, not with Oxide's list: a list a
        # former run changed must be rewritten even when it comes back to Oxide's.
        new = text
        if [tuple(e) for e in lst] != [tuple(e) for e in jsonstyle.get_value(text, ["learnset", "by_level"])]:
            new = render(new, lst)
        eggs = file_eggs(text)
        if eggs is None and d.eggs[sp]:
            # A file with no egg list gets one after its last learnset list.
            raw = json.loads(text)["learnset"]
            last = next(k for k in ("by_tutor", "by_tm", "by_level") if k in raw)
            new = jsonstyle.insert_key(new, ["learnset"], last, "egg_moves", [])
            eggs = []
        if eggs is not None and d.eggs[sp] != eggs:
            new = render_eggs(new, d.eggs[sp])
        if new == text:
            continue
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(new)
        changed += 1
    with open(LOG, "w", encoding="utf-8", newline="\n") as f:
        w = csv.writer(f, delimiter="\t", lineterminator="\n")
        w.writerow(["species", "level", "move", "action", "rule", "detail"])
        for sp, lv, mv, action, rule, detail in d.log:
            w.writerow([sp, lv, name(mv) if mv in M() else mv, action, rule, detail])
    return changed


def render(text, lst):
    """The file's text with its level-up list replaced, in its own style."""
    vs, ve, indent = jsonstyle._find_key(text, ["learnset", "by_level"])
    inline = re.search(r'\[ \d+, "MOVE_', text[vs:ve]) is not None or not text[vs:ve].strip("[] \n")
    body = jsonstyle.dumps([list(e) for e in lst], indent, max_inline=2 if inline else 0)
    return text[:vs] + body + text[ve:]


def file_eggs(text):
    """The file's egg list, or None for a file with none (a form's)."""
    try:
        return jsonstyle.get_value(text, ["learnset", "egg_moves"])
    except KeyError:
        return None


def render_eggs(text, eggs):
    """The file's text with its egg list replaced, in the files' style: one
    move a line, or [] when empty."""
    vs, ve, indent = jsonstyle._find_key(text, ["learnset", "egg_moves"])
    return text[:vs] + jsonstyle.dumps(list(eggs), indent, max_inline=0, empty_array="[]") + text[ve:]


def round_trip():
    """[species] whose file would change if its own lists were written back:
    the writer must reproduce every file byte for byte before it is trusted."""
    bad = []
    for sp in sorted(lc.species_set()):
        path = os.path.join(data.ROOT, "res", "pokemon", pokedex.folder_of(sp), "data.json")
        with open(path, encoding="utf-8") as f:
            text = f.read()
        lst = jsonstyle.get_value(text, ["learnset", "by_level"])
        eggs = file_eggs(text)
        if render(text, lst) != text or (eggs is not None and render_eggs(text, eggs) != text):
            bad.append(sp)
    return bad


def show(d, names, out=sys.stdout):
    for nm in names:
        sp = nm if nm.startswith("SPECIES_") else "SPECIES_" + nm.upper()
        fam = lc.family(sp)
        for s in sorted(lc.families()[fam], key=lambda s: (lowest_had().get(s, 99), s)):
            before = lc.learnset(BASE, s)
            after = d.lists[s]
            print(f"== {lc.species_name(s)}", file=out)
            print("   before: " + ", ".join(f"{name(m)} {lv}" for lv, m in before), file=out)
            print("   after:  " + ", ".join(f"{name(m)} {lv}" for lv, m in after), file=out)
            for row in d.log:
                if row[0] == s:
                    print(f"     {row[3]:28} {name(row[2]) if row[2] in M() else row[2]:16} {row[1]:>3}  "
                          f"{row[4]}: {row[5]}", file=out)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("what", choices=["plan", "write", "show", "roundtrip"])
    ap.add_argument("species", nargs="*")
    args = ap.parse_args(argv)
    if args.what == "roundtrip":
        bad = round_trip()
        print(f"{len(lc.species_set()) - len(bad)} files round-trip; differ: {bad[:10]}")
        return 1 if bad else 0
    d = build()
    if args.what == "show":
        show(d, args.species)
        return 0
    counts = collections.Counter((row[3].split(" ")[0], row[4]) for row in d.log)
    for (action, rule), n in sorted(counts.items(), key=lambda kv: -kv[1]):
        print(f"{n:5}  {action:9} {rule}")
    changed = sum(1 for sp, lst in d.lists.items()
                  if [tuple(e) for e in lst] != [tuple(e) for e in lc.learnset(BASE, sp)])
    print(f"{changed} lists change")
    if args.what == "write":
        print(f"wrote {write(d)} species files and {os.path.relpath(LOG, data.ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

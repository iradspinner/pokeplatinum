"""The learnset generator's second design (Ian and the Overseer, 2026-09-27).

    PYTHONPATH=. python3 -m tools.oxide.balance.learnplan sample        # the sample lines for Ian
    PYTHONPATH=. python3 -m tools.oxide.balance.learnplan line houndour  # one line
    PYTHONPATH=. python3 -m tools.oxide.balance.learnplan flags         # every line's power flags

It writes no game data. Ian sent the first design (learngen.py's propose)
back: it placed each move at its usual level across all of Kaizo, which gave
strong lines their best tools early and pushed weak first attacks late. This
one starts from Oxide's list as it is and changes an entry only where a rule
here requires it.

Placement is per species. A Kaizo entry is translated by split: the Kaizo
split its level falls in, carried to the same point of that split in Oxide
(learngen.LEVEL_MAP). Kaizo's League runs to 100, so nothing Kaizo places
lands past Oxide's 78. Reachability is judged in Oxide's terms after the
translation: a placement below the level the player can have the stage at
is not available. An entry counts only where Kaizo's move is Oxide's at like
values (same type and category, strength within a tenth), so Kaizo's 95-power
Crunch or one-turn Dig is no evidence for Oxide's. A species Kaizo lacks
takes its evidence from the Kaizo species nearest it in power, by its line's
final stage (stat total, best attacking stat, Speed).

What moves, by kind:

- An attack under the good bar (70 a turn same-type, 85 any) keeps Oxide's
  level and is never added.
- A good attack moves to Kaizo's translated level. On a line the power flags
  mark, it never comes earlier than Oxide has it now, and no new coverage is
  added. A good attack Kaizo gives the species and Oxide lacks is added at
  Kaizo's level.
- A status move follows Ian's tier list (docs/oxide/status-move-tiers.md).
  S and SSS count as strong: never earlier than now, and added only where
  Kaizo gives the species the move. A-tier moves move to Kaizo's level (no
  earlier than now on a marked line) and are never added. The rest keep
  Oxide's level. The instant-death moves and the entry hazards other than
  Toxic Spikes and Sticky Web are unrated, as Ian ruled.
- A move Kaizo gives only to a pre-evolution (an exclusive delay) goes to
  the pre-evolution at Kaizo's translated level, and the evolved stage's
  level-up entry of it moves to its level 1 (the relearner).
- The dead-weight rule, the move pool's cut and the weather ruling remove
  entries; a first stage whose first attack goes takes a weak attack of its
  type at the same level, so no gap opens.

The power flags are Ian's (2026-09-27): base Speed over 100, or base Attack
or Special Attack over 100 with a move of 100 or more power of that category
the stage can have by the split (level-up under the capture rule, TMs and
tutors; moves that knock the user out are left out). Owned so in a split
before Maylene's, the line is brought to Ian by name; in Maylene's, a very
close look; in Wake's, a close look. The power bar (Ian's Talonflame test)
waits for his thresholds.
"""
import argparse
import collections
import csv
import functools
import os
import re
import statistics
import sys

from ..encounters import calc_trainers, pokedex
from . import data, learngen as g, learnstudy as ls, pool

GOOD_STAB, GOOD_ANY = g.GOOD_STAB, g.GOOD_ANY
LIKE = 0.10                     # like values: strength within a tenth
TIERS_DOC = os.path.join(data.ROOT, "docs", "oxide", "status-move-tiers.md")
TIER_RANK = {"SSS": 6, "S": 5, "A": 4, "B": 3, "C": 2, "D": 1, "F": 0, "Useless": 0}
STRONG_RANK = 5
# Ian does not rate these (2026-09-27): the instant-death moves and every
# entry hazard but Toxic Spikes and Sticky Web.
UNRATED = {"Revival Blessing", "Destiny Bond", "Memento", "Healing Wish", "Lunar Dance",
           "Stealth Rock", "Spikes"}
# Oxide's versions read differently from the list's Generation 9 ones. Dark
# Void keeps its Generation 4 accuracy (80) and hits both foes; the list's D
# is for Generation 9's weaker version, so it reads as A here, beside Yawn.
OXIDE_TIER = {"Dark Void": "A"}
SELF_KO = {"MOVE_EXPLOSION", "MOVE_SELF_DESTRUCT", "MOVE_SELFDESTRUCT", "MOVE_MEMENTO",
           "MOVE_MISTY_EXPLOSION", "MOVE_FINAL_GAMBIT", "MOVE_HEALING_WISH", "MOVE_LUNAR_DANCE"}
FLAG_LEVELS = {"Maylene": "very close look", "Wake": "close look"}
SPLITS = pool.SPLITS


def M():
    return g._oxide_moves()


def name(const):
    return M()[const]["name"]


# A move's downside, weighed into its strength (Ian, 2026-09-27): a lock-in
# takes the choice out of the player's hands ("letting Jesus take the
# wheel", Uproar the worst of them), and a self-drop weakens the next use.
# The strength model already counts recoil (a fifth to a tenth off) and a
# recharge turn (half), so those are not charged twice.
DOWNSIDE = {"UPROAR": 0.5, "CONTINUE_AND_CONFUSE_SELF": 0.6, "USER_SP_ATK_DOWN_2": 0.8,
            "LOWER_OWN_ATK_AND_DEF": 0.85, "DEF_SPD_DOWN_HIT": 0.9, "SPEED_DOWN_HIT": 0.95}


def strength(const):
    """(kind, strength a turn) with the move's downside weighed in."""
    kind, p = ls.strength(ls.oxide_move(M()[const]))
    return kind, p * DOWNSIDE.get(M()[const].get("effect"), 1.0)


def effective_power(const):
    """A move's power for the power flags: its listed power after recoil, a
    recharge turn and its downside, but not its accuracy."""
    m = M()[const]
    rec = ls.oxide_move(m)
    kind, per_turn = ls.strength(rec)
    if kind != "damage":
        return 0
    hit = min(m.get("accuracy") or 100, 100) / 100 if m.get("accuracy") else 1.0
    return per_turn / hit * DOWNSIDE.get(m.get("effect"), 1.0)


def is_good(const, types):
    kind, p = strength(const)
    return kind == "damage" and (p >= GOOD_ANY or (M()[const]["type"].title() in types and p >= GOOD_STAB))


def good_attack(const, types):
    """A good attack the method may move or add. A move that knocks the user
    out is no tool to place by power (it ends a wild encounter besides), so
    it keeps Oxide's level."""
    return is_good(const, types) and const not in SELF_KO


# ---- Ian's status tiers ---------------------------------------------------------

@functools.lru_cache(maxsize=None)
def tiers():
    """{MOVE_X: tier} from the transcribed list, with Oxide's readings."""
    by_name = g._by_name()
    out = {}
    with open(TIERS_DOC, encoding="utf-8") as f:
        for line in f:
            m = re.match(r"\|\s*(SSS|S|A|B|C|D|F|Useless)\s*\|(.*)\|\s*$", line)
            if not m:
                continue
            for n in m.group(2).split(","):
                n = n.strip()
                const = by_name.get(ls.metrics._compact(n))
                if const and n not in UNRATED:
                    out[const] = OXIDE_TIER.get(n, m.group(1))
    for n, t in OXIDE_TIER.items():
        const = by_name.get(ls.metrics._compact(n))
        if const:
            out[const] = t
    return out


def rank(const):
    t = tiers().get(const)
    return TIER_RANK[t] if t else None


# ---- Kaizo's evidence, translated by split -----------------------------------------

def translate(kaizo_level):
    """A Kaizo level carried to the same point of the same split in Oxide.
    Kaizo's League runs to 100, so the result is at most 78."""
    return 1 if kaizo_level <= 1 else g.oxide_level(kaizo_level)


def like_values(kaizo_name, const):
    """Whether Kaizo's move of that name is Oxide's at like values: same type
    and category, and strength within a tenth (a status move: accuracy
    within ten points)."""
    km = ls.kaizo_moves()
    k = km.get(ls.resolve(kaizo_name, km) or "")
    if not k:
        return False
    m = M()[const]
    if (k["type"] or "").title() != m["type"].title() or (k["category"] or "").upper() != m["class"]:
        return False
    ks, os_ = ls.strength(k), ls.strength(ls.oxide_move(m))
    if ks[0] != os_[0]:
        return False
    if os_[0] != "damage":
        return abs((k.get("accuracy") or 100) - min(m.get("accuracy") or 100, 100)) <= 10
    return abs(ks[1] - os_[1]) <= LIKE * max(ks[1], os_[1])


@functools.lru_cache(maxsize=None)
def _source_levels():
    """{species: [level]} for every scripted source, whatever its split
    (the post-game statics included)."""
    out = collections.defaultdict(list)
    with open(pool.SOURCES, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            try:
                out[row["species"]].append(pool._source_level(row["level"]))
            except (ValueError, TypeError):
                continue
    return out


# The drawn legendaries take the lake guardians' slots (the encounter plan's
# legendary pool), so they are met at those slots' levels.
GUARDIANS = ("SPECIES_UXIE", "SPECIES_MESPRIT", "SPECIES_AZELF")


@functools.lru_cache(maxsize=None)
def catch_level(species):
    """The lowest level any source gives the species at (a wild table, a
    static, a gift, a trade, a hatched egg); for an obtainable species with
    no source of its own and no earlier stage (a drawn legendary), the lake
    guardians' lowest; None when nothing gives it."""
    levels = [lv for _s, lv, _how in pool.catches().get(species) or []] + _source_levels().get(species, [])
    if not levels and species in g._obtainable() and not pool.pre_evolutions().get(species):
        levels = [lv for s in GUARDIANS for lv in _source_levels().get(s, [])]
    return min(levels, default=None)


def reach(species):
    """The level the player can first have the stage at in Oxide: the level
    it can first be evolved into (evolved_at), or a lower catch; a first
    stage's lowest catch, gift or hatch level; 1 for a first stage nothing
    gives. A placement below it is learnt by nobody, so it means unavailable
    in play (Ian, 2026-09-27), not early: Kaizo's legendaries' low entries
    and a level 2 Iron Head for a Togedemaru first met at 20 both stay out."""
    found = [x for x in (evolved_at(species), catch_level(species)) if x is not None]
    return min(found) if found else 1


def _split_start(split):
    """A split's first level: one past the cap of the split before it."""
    i = SPLITS.index(split)
    return 1 if i == 0 else pool.caps()[SPLITS[i - 1]] + 1


@functools.lru_cache(maxsize=None)
def evolved_at(species):
    """The level the player can first evolve into the stage, None for a first
    stage, and never below the pre-evolution's own reach. A level evolution
    is at its level. A stone or a held item is at the first level of the
    split where the item is first in reach (pool.evolution_items_first, the
    stone plan and the item census), where the encounter tool's stand-in
    levels (30 or 32) took Rhydon's Protector, first had in Byron's split,
    as level 32. Oxide has no friendship or trade evolutions: the base ROM
    made them levels or held items (Munchlax at 36, Togepi at 10, Rhydon
    with the Protector). The location, known-move, partner and Beauty
    evolutions keep the stand-in levels (Magnezone, Lickilicky, Mantine,
    Milotic)."""
    if species not in g.oxide_reached():
        return None
    parent = g.oxide_reached()[species][0]
    options = []
    for need, item, target in pool.evolutions(parent):
        if target != species:
            continue
        if item:
            first = pool.evolution_items_first().get(item)
            if first in SPLITS:
                options.append(_split_start(first))
        else:
            options.append(need)
    at = min(options) if options else max(1, g.reached("oxide", species))
    return max(at, reach(parent))


def next_stages(species):
    """The stages the species evolves into directly."""
    return [s for s, (p, _lv) in g.oxide_reached().items() if p == species]


def kaizo_evidence(species):
    """{MOVE_X: (Kaizo level, translated level, why it does not count or None)}
    from Kaizo's list for the same species, each move's first entry."""
    out = {}
    rec = ls.kaizo_lists().get(species)
    if not rec:
        return None
    first_stage = species not in g.oxide_reached()
    for lv, kname in rec["list"]:
        const = g._by_name().get(ls.metrics._compact(ls.SPELLING.get(kname, kname)))
        if not const or const in out:
            continue
        t = translate(lv)
        if not like_values(kname, const):
            km = ls.kaizo_moves().get(ls.resolve(kname, ls.kaizo_moves()) or "") or {}
            why = f"Kaizo's is {km.get('power')} power, Oxide's {M()[const]['power']}" \
                if km.get("power") != M()[const]["power"] else "Kaizo's is another move"
            out[const] = (lv, t, why)
        elif lv <= 1 and not first_stage:
            out[const] = (lv, t, "an evolved stage's level 1 (the relearner)")
        elif t < reach(species):
            out[const] = (lv, t, f"lands at {t}, below {reach(species)}, where the player can have it")
        else:
            out[const] = (lv, t, None)
    return out


def _final(species):
    line = next((ln for ln in g.oxide_lines() if species in ln), [species])
    return line[-1], line.index(species)


def _power_vector(species):
    st = (pokedex.load(data.ROOT, species) or {}).get("stats") or {}
    return (sum(st.values()) / 600, max(st.get("attack", 0), st.get("special_attack", 0)) / 150,
            st.get("speed", 0) / 150)


@functools.lru_cache(maxsize=None)
def nearest_kaizo(species, k=5):
    """The Kaizo species nearest this one in power, at the same stage of their
    lines: by the final stage's stat total, best attacking stat and Speed."""
    final, idx = _final(species)
    me = _power_vector(final)
    rows = []
    for ks in ls.kaizo_lists():
        if ks == species or not pokedex.load(data.ROOT, ks):
            continue
        kf, kidx = _final(ks)
        if kidx != idx:
            continue
        v = _power_vector(kf)
        rows.append((sum((a - b) ** 2 for a, b in zip(me, v)) ** 0.5, ks))
    return [ks for _d, ks in sorted(rows)[:k]]


def analogue_level(species, const):
    """A species Kaizo lacks: the median translated level at which its nearest
    Kaizo species learn a like move (the same status move; an attack of the
    same category, same-type-ness and strength within a tenth), or None."""
    got = _analogue(species, const)
    return round(statistics.median(t for t, _kl in got)) if got else None


def analogue_kaizo_level(species, const):
    """The same, at Kaizo's own levels (untranslated), or None."""
    got = _analogue(species, const)
    return round(statistics.median(kl for _t, kl in got)) if got else None


@functools.lru_cache(maxsize=None)
def _analogue(species, const):
    """[(translated level, Kaizo's level)], one per nearest Kaizo species that
    learns a like move, each its earliest."""
    m = M()[const]
    kind, p = strength(const)
    types = {t.title() for t in (pokedex.load(data.ROOT, species) or {}).get("types", [])}
    stab = m["type"].title() in types
    levels = []
    for ks in nearest_kaizo(species):
        ev = kaizo_evidence(ks) or {}
        ktypes = {t.title() for t in (pokedex.load(data.ROOT, ks) or {}).get("types", [])}
        best = None
        for c, (kl, t, why) in ev.items():
            if why:
                continue
            if kind != "damage":
                ok = c == const
            else:
                kk, kp = strength(c)
                ok = (kk == "damage" and M()[c]["class"] == m["class"]
                      and (M()[c]["type"].title() in ktypes) == stab
                      and abs(kp - p) <= LIKE * max(kp, p))
            if ok and (best is None or t < best[0]):
                best = (t, kl)
        if best is not None:
            levels.append(best)
    return tuple(levels)


# ---- the power flags ------------------------------------------------------------------

PROPOSED = {}


@functools.lru_cache(maxsize=None)
def _owned_from(species):
    for split in SPLITS:
        if species in pool.species_by_split()[split]:
            return split
    return None


def _can_have(species, split):
    """Every move the stage can have by the split, with the proposal's lists."""
    original = pool._learnset
    pool._learnset = lambda sp: PROPOSED.get(sp) or original(sp)
    try:
        return pool.moves_at(species, split)
    finally:
        pool._learnset = original


def stage_flag(species):
    """(split, why) for the first split the stage trips Ian's flags in, or None."""
    st = (pokedex.load(data.ROOT, species) or {}).get("stats") or {}
    start = _owned_from(species)
    if not start:
        return None
    for split in SPLITS[SPLITS.index(start):SPLITS.index("Byron")]:
        if st.get("speed", 0) > 100:
            return split, f"base Speed {st['speed']}"
        for stat, cls in (("attack", "PHYSICAL"), ("special_attack", "SPECIAL")):
            if st.get(stat, 0) <= 100:
                continue
            big = sorted((M()[c]["power"], name(c)) for c in _can_have(species, split)
                         if c in M() and M()[c]["class"] == cls and effective_power(c) >= 100
                         and c not in SELF_KO and name(c) not in pool.UNRELIABLE)
            if big:
                label = "Attack" if cls == "PHYSICAL" else "Special Attack"
                return split, f"base {label} {st[stat]} with {big[-1][1]} ({big[-1][0]})"
    return None


def severity(split):
    if split is None:
        return None
    if SPLITS.index(split) < SPLITS.index("Maylene"):
        return "brought to Ian by name"
    return FLAG_LEVELS.get(split)


def line_of(species):
    return next((ln for ln in g.oxide_lines() if species in ln), [species])


def family(species):
    """Every stage of every branch of the species' line, first stage first."""
    first = line_of(species)[0]
    out = []
    for ln in g.oxide_lines():
        if ln[0] == first:
            out += [s for s in ln if s not in out]
    return out


def marked(species):
    """Whether any stage of the family trips a flag before Byron's split."""
    return any(stage_flag(s) for s in family(species))


# The power bar (Ian's Talonflame test; his provisional thresholds of
# 2026-09-27): a stage is strong for a split when, at the split's cap with
# the moves it can have by then, it outspeeds more than half the split's
# trainer Pokemon and knocks out more than a quarter in one hit (the middle
# roll, from full HP).
BAR_SPEED, BAR_ONE_HIT = 0.5, 0.25


@functools.lru_cache(maxsize=None)
def _split_trainer_mons(split):
    """Every trainer Pokemon the player meets in the split: its placed
    trainers' and its story fights' (each rival variant once)."""
    from . import b6, pressure
    ox = data.oxide_trainers()
    mons = [m for tr, p in b6.placements().items() if p["split"] == split for m in ox[tr]["party"]]
    for f in data.fights()["fights"]:
        if f["split"] == split:
            for party in pressure.boss_parties(f)[0]:
                mons += party
    return mons


def _bar_record(species, split, blob):
    from ..encounters import canon, calc_trainers
    name_ = canon.showdown_name(species)
    if not name_ or name_ not in blob["poks"]:
        return None
    names = pool._move_names()
    moves = pool.damaging_moves(sorted({names[c] for c in _can_have(species, split) if c in names}), blob)
    iv = {k: pool.AVERAGE_IV for k in ("hp", "at", "df", "sa", "sd", "sp")}
    return {"species": name_, "level": pool.caps()[split],
            "ability": (blob["poks"][name_].get("abilities") or {}).get("0"),
            "item": None, "nature": "Hardy", "ivs": iv, "evs": {k: 0 for k in iv}, "moves": moves}


@functools.lru_cache(maxsize=None)
def bar_reading(species, split):
    """(share outsped, share knocked out in one hit) against the split's
    trainer Pokemon, or None when the stage is not the player's by then."""
    from . import pressure, teamscore
    if species not in pool.species_by_split().get(split, {}):
        return None
    blob = teamscore._blob()
    rec = _bar_record(species, split, blob)
    foes = _split_trainer_mons(split)
    if rec is None or not foes or not rec["moves"]:
        return None
    jobs = {"pokemon": {"me": rec}, "pairs": []}
    for i, m in enumerate(foes):
        jobs["pokemon"][f"f{i}"] = m
        jobs["pairs"].append(["me", f"f{i}", rec["moves"], None])
    out = pressure.run_node(teamscore._blob_path(), jobs)
    hp = {k: v["hp"] for k, v in out["pokemon"].items()}
    faster = one_hit = 0
    for r in out["results"]:
        sa, sd = r["speeds"]
        faster += sa > sd
        best = max((v["rolls"][len(v["rolls"]) // 2] for v in r["moves"].values()
                    if "rolls" in v and v["rolls"]), default=0)
        one_hit += best >= hp[r["d"]]
    n = len(out["results"])
    return round(faster / n, 3), round(one_hit / n, 3)


def passes_bar(species):
    """(split, reading) for the first split before Byron's where the stage
    passes the power bar, or None."""
    start = _owned_from(species)
    if not start:
        return None
    for split in SPLITS[SPLITS.index(start):SPLITS.index("Byron")]:
        r = bar_reading(species, split)
        if r and r[0] > BAR_SPEED and r[1] > BAR_ONE_HIT:
            return split, r
    return None


def strong_stage(species):
    """A stage its own list treats as strong (Ian, 2026-09-27): flagged
    before Byron's split, or over the power bar, on Oxide's lists or on the
    proposal's (FORCED). Its own list is held to "no earlier than now", and
    so is what a pre-evolution learns without a real wait (WAIT); a
    pre-evolution kept back longer is the price of a delay, and stays free."""
    return (species in FORCED or stage_flag(species) is not None
            or (USE_BAR and passes_bar(species) is not None))


USE_BAR = True
# Stages the proposal's own moves would flag or put over the bar: proposed
# again as strong (propose_family).
FORCED = set()
# A route through a pre-evolution is a delay only when the wait unevolved is
# at least this many levels past the strong stage's evolution, as delay test
# 3 asks: Kaizo's Kirlia learns Thunderbolt at 30, the level it becomes
# Gardevoir, which is no wait at all, while Joltik's Bug Buzz at 38, eight
# levels past Galvantula at 30, is one.
WAIT = 5


def passes_bar_proposed(species):
    """passes_bar on the proposal's lists (PROPOSED), not the cached reading."""
    start = _owned_from(species)
    if not start:
        return None
    for split in SPLITS[SPLITS.index(start):SPLITS.index("Byron")]:
        r = bar_reading.__wrapped__(species, split)
        if r and r[0] > BAR_SPEED and r[1] > BAR_ONE_HIT:
            return split, r
    return None


def strong_later_stages(species):
    """[(a strong later stage, the last level at which what this stage learns
    comes along into it without a real wait)]. The wait is measured from the
    stage's own next evolution on the branch, at the level that evolution
    first becomes possible: a stage kept back past it is a delay the player
    chose, whatever comes after (Togepi's Moonblast at 43 is a wait of 33
    levels past Togetic at 10, though Togekiss comes only with the Shiny
    Stone at 40)."""
    out = {}
    for nxt in next_stages(species):
        until = (evolved_at(nxt) or reach(nxt)) + WAIT - 1
        for e in [nxt] + later_stages(nxt):
            if strong_stage(e):
                out[e] = max(out.get(e, 0), until)
    return list(out.items())


def later_stages(species):
    """Every stage that comes after this one on any branch of its line."""
    out = []
    for ln in g.oxide_lines():
        if species in ln:
            out += [s for s in ln[ln.index(species) + 1:] if s not in out]
    return out


def _now(species):
    return [tuple(e) for e in (pokedex.load(data.ROOT, species) or {}).get("learnset", [])]


def first_good_of_type(species, move_type, lst=None):
    """The level of the stage's first good attack of a type that it can
    learn (at or above the level it is had at), on its list now."""
    types = _types(species)
    here = reach(species) if species in g.oxide_reached() else 1
    return min((lv for lv, c in (lst if lst is not None else _now(species))
                if lv > 1 and lv >= here and c in M() and M()[c]["type"] == move_type
                and good_attack(c, types)), default=None)


# ---- the own-type gap (Ian, 2026-09-27) ----------------------------------------------
# No stage the player can have goes more than one split without an attack of
# its own type of 50 or more, by effective power (Bonemerang's two hits
# count). What a pre-evolution kept back learns does not count here; what a
# player who evolves on time has does.
STAB_GAP_POWER = 50
# [(stage, MOVE_X, the stage whose list holds it, its level)] kept at its
# level by the rule, and those that would reach a flagged or barred stage,
# listed for Ian rather than decided.
STAB_KEPT = []
STAB_FOR_IAN = []


def _own_type_attack(c, types):
    return c in M() and M()[c]["type"].title() in types and effective_power(c) >= STAB_GAP_POWER


def had_from(species, lists):
    """{MOVE_X: the level the stage has it from}: what a first stage knows at
    capture, what an evolved stage brings from its pre-evolution evolved on
    time (everything it has by the evolution level), and its own level-up
    moves from the level it is had at."""
    here = reach(species)
    own = lists.get(species) if species in lists else _now(species)
    out = {}
    if species in g.oxide_reached():
        parent = g.oxide_reached()[species][0]
        for c, lv in had_from(parent, lists).items():
            if lv <= here:
                out[c] = here
        for lv, c in own:
            if lv == 0:
                out[c] = here             # an evolution move, taught on evolving
    else:
        for c in at_capture(own, here):
            out[c] = here
    for lv, c in own:
        if lv >= here and (lv > 1 or species not in g.oxide_reached()):
            out[c] = min(out.get(c, 999), lv)
    return out


def evolves_early(species):
    """Whether the player can evolve the stage by the end of Gardenia's split,
    by level or by a stone in reach by then (Ian, 2026-09-27): its gap bites
    only a player who chooses to keep it back, who is already trading the
    power away."""
    return any(pool.reachable(need, item, "Gardenia") for need, item, _t in pool.evolutions(species))


def gap_applies(species):
    """Whether the rule reads the stage: one the player can have by the
    League, and not one it can evolve by the end of Gardenia's split."""
    return (species in g._obtainable() and _split_of(reach(species)) in SPLITS
            and not evolves_early(species))


def stab_gap(species, lists):
    """The splits from the one the stage is first had in to the one it first
    has an attack of its own type of 50 or more in; None if never by the
    League's cap."""
    types = _types(species)
    firsts = [lv for c, lv in had_from(species, lists).items() if _own_type_attack(c, types)]
    first = min(firsts, default=None)
    if first is None or _split_of(first) not in SPLITS:
        return None
    return SPLITS.index(_split_of(first)) - SPLITS.index(_split_of(reach(species)))


def breaks_gap(species, lists):
    gap = stab_gap(species, lists)
    return gap is None or gap >= 2


def widens_gap(species, now, new):
    """Whether the proposal leaves the stage more than one split without an
    attack of its own type, or longer than Oxide's lists now do where they
    already break the rule (Grovyle, first had at Roark's cap, waits for
    Leaf Blade into Fantina's split now; the proposal must not make it
    longer)."""
    g_now, g_new = stab_gap(species, now), stab_gap(species, new)
    g_now = 99 if g_now is None else g_now
    g_new = 99 if g_new is None else g_new
    return g_new > max(1, g_now)


def _entry_list(lst, c, lv):
    """The list with its level-up entries of the move replaced by one at lv."""
    return sorted([e for e in lst if not (e[1] == c and e[0] > 1)] + [(lv, c)], key=lambda e: e[0])


def close_gaps(fam, res):
    """Where the proposal leaves a stage more than one split without an
    attack of its own type and Oxide's lists now do not, the nearest such
    move it has now stays at its current level (Ian, 2026-09-27). If keeping
    it would reach a flagged or barred stage, it is listed for Ian instead."""
    now = {s: _now(s) for s in fam}
    for s in fam:
        if not gap_applies(s):
            continue
        new = {x: res[x][0] for x in fam}
        if not widens_gap(s, now, new):
            continue
        types = _types(s)
        # Each own-type attack it has now, earliest first, and every stage of
        # its chain whose list holds it: the one that gives it the move (its
        # own list, or a pre-evolution's before the evolution) is found by
        # trying each.
        options = []
        for c, lv_had in sorted(had_from(s, now).items(), key=lambda kv: kv[1]):
            if not _own_type_attack(c, types):
                continue
            for holder in g._chain(s)[::-1]:
                lv = next((l for l, cc in now[holder] if cc == c and l > 1), None)
                if lv is not None:
                    options.append((lv_had, c, holder, lv))
        for _lv_had, c, holder, lv in options:
            trial = dict(new, **{holder: _entry_list(new[holder], c, lv)})
            if widens_gap(s, now, trial):
                continue
            reached = [x for x in [holder] + later_stages(holder)
                       if strong_stage(x) and (x == holder or lv <= reach(x))]
            if reached:
                STAB_FOR_IAN.append((s, c, holder, lv, reached))
                break
            was = next((l for l, cc in new[holder] if cc == c and l > 1), None)
            notes = res[holder][1] + [(c, f"{'dropped' if was is None else 'at ' + str(was)} to {lv}: Ian's rule "
                                          f"that no stage goes more than one split without an attack of "
                                          f"its own type, for {_sp(s)}")]
            res[holder] = (trial[holder], notes)
            FLOORS.pop((holder, c), None)
            STAB_KEPT.append((s, c, holder, lv))
            break
    return res


# ---- after an evolution not by level, and in the last splits (Ian, 2026-09-28) ---------

LATE = 61                     # the Galactic split's first level
NOT_BY_LEVEL = ("USE_ITEM", "LEVEL_WITH_HELD_ITEM", "LEVEL_KNOW_MOVE", "LEVEL_MAGNETIC_FIELD",
                "LEVEL_MOSS_ROCK", "LEVEL_ICE_ROCK", "LEVEL_BEAUTY", "LEVEL_SPECIES_IN_PARTY")
# A stage Oxide gives no pre-evolution, whose later-game pre-evolution's
# list stands in for one: Alolan Ninetales, caught from Gardenia's split
# and, once element 7's Ice Stone lands, evolved from a Vulpix (Ian).
VIRTUAL_PARENT = {"SPECIES_ALOLAN_NINETALES": "SPECIES_VULPIX_ALOLAN",
                  "SPECIES_GALARIAN_RAPIDASH": "SPECIES_PONYTA_GALARIAN"}
# Stone branches Ian has ruled in whose evolution records the main track
# adds (2026-09-28): the stage, the Oxide pre-evolution, and the stone. The
# stage's list must work from the wild catch and from the stone at any
# level after the pre-evolution's first catch.
PLANNED_PARENT = {"SPECIES_ALOLAN_NINETALES": ("SPECIES_VULPIX", "ITEM_ICE_STONE"),
                  "SPECIES_GALARIAN_WEEZING": ("SPECIES_KOFFING", "ITEM_MOON_STONE"),
                  "SPECIES_GALARIAN_RAPIDASH": ("SPECIES_PONYTA", "ITEM_MOON_STONE")}
# The type an evolution move brings, where Ian names it: the Moon Stone
# forms' Fairy, which Koffing and Ponyta carry none of.
EVOLUTION_MOVE_TYPES = {"SPECIES_GALARIAN_WEEZING": {"Fairy"}, "SPECIES_GALARIAN_RAPIDASH": {"Fairy"},
                        "SPECIES_ALOLAN_NINETALES": {"Ice"}}


@functools.lru_cache(maxsize=None)
def later_moves_any(species):
    """(MOVE_X) any later game teaches the species by level-up, TM or tutor."""
    from . import laterlearn as ll
    out = set()
    for gkey, _name in ll.GAMES:
        rec = ll.game(gkey).get(hg_key(species)) or ll.game(gkey).get(species)
        for kind in ("LevelMoves", "MachineMoves", "TutorMoves"):
            for e in (rec or {}).get(kind) or []:
                out.add(ll.oxide_move(e["Move"] if isinstance(e, dict) else e))
    return tuple(sorted(out))
REGIONS = ("ALOLAN", "GALARIAN", "HISUIAN", "PALDEAN")


def hg_key(species):
    """hg-engine's key for an Oxide species: a regional form names the
    region last (SPECIES_ALOLAN_NINETALES is SPECIES_NINETALES_ALOLAN)."""
    for r in REGIONS:
        if species.startswith(f"SPECIES_{r}_"):
            return f"SPECIES_{species[len('SPECIES_' + r + '_'):]}_{r}"
    return species


@functools.lru_cache(maxsize=None)
def later_level_list(species):
    """[(level, MOVE_X)] the latest later game teaches the species by level
    up, every move, level 0 kept as 0."""
    from . import laterlearn as ll
    for gkey, _name in reversed(ll.GAMES):
        rec = ll.game(gkey).get(hg_key(species)) or ll.game(gkey).get(species)
        if rec and rec.get("LevelMoves"):
            return tuple(sorted({(e["Level"], ll.oxide_move(e["Move"]))
                                 for e in rec["LevelMoves"] if ll.oxide_move(e["Move"]) in M()}))
    return ()


def planned_since(species):
    """The first level the stage can be had at by either route: its wild
    catch, or the stone used on its planned pre-evolution from that one's
    first catch, once the stone is in reach."""
    parent, stone = PLANNED_PARENT[species]
    first = pool.evolution_items_first().get(stone)
    stone_at = _split_start(first) if first in SPLITS else None
    by_stone = max(reach(parent), stone_at) if stone_at else None
    found = [x for x in (catch_level(species), by_stone) if x is not None]
    return min(found) if found else reach(species)
CARRIED = []                  # (stage, move, source level, placed level or None, why)
LATE_ADDED = []               # (stage, move, level, source)
LATE_FOR_IAN = []             # stages with no real late move to give
# (stage, move) that Ian's two rulings place past a flag's first-of-type
# test: an attack of the stage's own type where it has none good by then,
# and any move in the last splits, which the flags do not look at.
RULED = set()
EVOLUTION_MOVES = []          # (stage, move, why), each for Ian
# Moves that fail without weather the player can never set (Ian, 2026-09-26).
NEEDS_WEATHER = {"MOVE_AURORA_VEIL"}
# Evasion, which Ian took off the TMs (Double Team): never a key or late pick.
EVASION = {"MOVE_MINIMIZE", "MOVE_DOUBLE_TEAM"}
# Moves the generator never picks as a key or late move: evasion, and the
# generic protection Ian took off the TMs as too generic (Protect, and Detect
# with it). A wall whose own or Kaizo's list gives it Protect keeps it.
NOT_PICKED = EVASION | {"MOVE_PROTECT", "MOVE_DETECT"}
# A charging turn, a turn out of reach, or a recharge: Ian's downsides
# (ruling 11), so such a move is a late pick only when nothing else is.
TWO_TURN = {"FLY", "DIVE", "DIG", "BOUNCE", "SHADOW_FORCE", "SKY_DROP", "SKIP_CHARGE_TURN_IN_SUN",
            "RECHARGE_AFTER"}
# A stage whose better attacking stat leads the other by this much never
# takes an attack of the other category as a late pick.
STAT_GAP = 20
# Lists Ian has asked for by name, placed past the flags' first-of-type test
# and listed for him: Alolan Ninetales, a proper list for the wild catch and
# the Ice Stone route (ruling 19; the Overseer's read of 2026-09-28): a Fairy
# attack in Fantina's split and a stronger Ice move in Byron's.
RULED_LISTS = {"SPECIES_ALOLAN_NINETALES": [(30, "MOVE_DRAINING_KISS"), (45, "MOVE_ICE_BEAM")]}
RULED_PLACED = []             # (stage, move, level), for Ian by name
DEAD_MOVED = []               # (stage, move, moved to, action), moved entries undone


def not_by_level(species):
    """Whether the stage is reached by an evolution with no level of its own
    (a stone, a held item, a known move, a place, a partner or Beauty), or
    has a stand-in pre-evolution."""
    if species in VIRTUAL_PARENT or species in PLANNED_PARENT:
        return True
    if species not in g.oxide_reached():
        return False
    parent = g.oxide_reached()[species][0]
    return any(e.get("into") == species and e["method"].startswith(NOT_BY_LEVEL)
               for e in (pokedex.load(data.ROOT, parent) or {}).get("evolutions", []))


@functools.lru_cache(maxsize=None)
def virtual_parent_list(species):
    """[(level, MOVE_X)] of the stand-in pre-evolution, from the latest game
    in hg-engine's per-game lists that has it."""
    from . import laterlearn as ll
    key = VIRTUAL_PARENT[species]
    for gkey, _name in reversed(ll.GAMES):
        rec = ll.game(gkey).get(key)
        if rec and rec.get("LevelMoves"):
            return tuple(sorted({(max(1, e["Level"]), ll.oxide_move(e["Move"]))
                                 for e in rec["LevelMoves"] if ll.oxide_move(e["Move"]) in M()}))
    return ()


def _real(species, c, lv, lst):
    """A move worth a level-up slot where it lands: an attack that is not
    dead weight, or a status move Ian's tiers rate B or better."""
    from . import laterlearn as ll
    if c not in M() or c in NEEDS_WEATHER or c in SELF_KO or c in ll._doubles_only() \
            or g._dropped(c, species, lv, _types(species), lst):
        return False
    return strength(c)[0] == "damage" or (rank(c) or 0) >= 3


def _substance(c):
    """A move a player looks forward to: an attack of 60 or more by effective
    power, or a status move rated A or better."""
    return (strength(c)[0] == "damage" and effective_power(c) >= 60) or (rank(c) or 0) >= 4


def _worth(species, c):
    """What a move adds, to choose among candidates: an attack's effective
    power, half again for its own type, scaled by the attacking stat it uses
    against the stage's better one; a status move's tier, on the same scale
    (B 75, A 100, S 125)."""
    if strength(c)[0] == "damage":
        st = (pokedex.load(data.ROOT, species) or {}).get("stats") or {}
        atk, spa = st.get("attack", 1) or 1, st.get("special_attack", 1) or 1
        used = spa if M()[c]["class"] == "SPECIAL" else atk
        return effective_power(c) * (1.5 if _own_type_attack(c, _types(species)) else 1.0) * used / max(atk, spa)
    return (rank(c) or 0) * 25


def at_capture(lst, level):
    """The four moves a Pokemon caught, received or met at `level` knows by
    the capture rule. A level-0 entry is an evolution move, taught only on
    evolving and never known at capture (the engine's rule, 2026-09-28)."""
    return calc_trainers.default_moves([list(e) for e in lst if e[0] != 0], level)


def _place(species, lst, c, lv, carried=False, ruled=False):
    """(level, why, meta) for adding a move to the stage's list at `lv` or
    later by the generator's rules, or (None, why not, {}): the engine runs
    it, it is not dead weight, a strong move no earlier than Kaizo's level
    for like moves, never an S or SSS status move (the rules add those only
    where Kaizo gives the species the move), a stage the flags or the bar
    hold taking a new attack no earlier than its first good one of that type
    (unless it has no attack of its own type of 50 or more yet, or the move
    lands in the last splits), nothing that ends a wild encounter in the
    wild levels, nothing past 78, and the one-level rule within the split.
    It records nothing, so a pass can try many; _commit records the one
    placed. `carried` is kept for the callers' reading only."""
    from . import laterlearn as ll
    types = _types(species)
    if c not in M() or not ll.placeable(c):
        return None, "the engine does not run it in full", {}
    drop = g._dropped(c, species, lv, types, lst)
    if drop:
        return None, f"dead weight: {drop}", {}
    kind, _p = strength(c)
    r = rank(c)
    good = good_attack(c, types)
    strong_move = good or (r or 0) >= STRONG_RANK
    why = []
    if kind != "damage" and (r or 0) >= STRONG_RANK:
        return None, "an S or SSS status move, which the rules add only where Kaizo gives it", {}
    if strong_move:
        kl = analogue_kaizo_level(species, c)
        if kl and kl <= 78 and floor_level(kl) > lv:
            why.append(f"{lv} to {floor_level(kl)}: no earlier than Kaizo's level for like moves ({kl})")
            lv = floor_level(kl)
    # A list Ian asked for by name (`ruled`) passes the flags' first-of-type
    # test; so does a stage's first attack of its own type.
    exempt = ruled
    if strong_stage(species) and good and lv < LATE and not ruled:
        own = _own_type_attack(c, types)
        has_own = any(1 < l <= lv and _own_type_attack(cc, types) for l, cc in lst)
        first = first_good_of_type(species, M()[c]["type"], lst)
        if own and not has_own:
            exempt = True
        elif first is None or lv < first:
            return None, ("a stage the power flags or the bar hold takes a new attack only no earlier "
                          "than its first good one of that type"), {}
    if ls.metrics._compact(name(c)) in g._ends() and 1 < lv <= g.wild_top(species):
        return None, "it ends a wild encounter, at a level the species is met wild at", {}
    if lv > 78:
        return None, f"at {lv}, past 78", {}
    taken = {l for l, _c in lst if l > 1}
    crowded = False
    if lv in taken:
        split = _split_of(lv)
        steps = [d for k in range(1, 12) for d in ((k, -k) if strong_move else (-k, k))]
        new = next((lv + d for d in steps if 2 <= lv + d <= 78 and lv + d not in taken
                    and _split_of(lv + d) == split and (not strong_move or d > 0)), None)
        if new is not None:
            why.append(f"{lv} to {new}: the one-level rule")
            lv = new
        else:
            crowded = True
    return lv, "; ".join(why), {"ruled": exempt or lv >= LATE, "crowded": crowded}


def _commit(species, c, lv, meta, lst=()):
    """Record what placing a move entails: its exemption from the flags'
    first-of-type test, and a level it must share, for it and for each move
    already there (a strong move's floor at its split's cap, where an
    earlier one sits, has no free level above it in the split)."""
    if meta.get("ruled"):
        RULED.add((species, c))
    if meta.get("crowded"):
        CROWDED.setdefault(species, []).extend([(c, lv)] + [(cc, l) for l, cc in lst if l == lv])


def _evolution_source(s, res):
    """(the candidate moves after the evolution, where they start, a label):
    the pre-evolution's list, or the stand-in's for a stage Oxide gives none."""
    since = planned_since(s) if s in PLANNED_PARENT else reach(s)
    if s in VIRTUAL_PARENT:
        return list(virtual_parent_list(s)), since, "the later games' " + _sp(VIRTUAL_PARENT[s])
    if s in PLANNED_PARENT and s not in g.oxide_reached():
        parent = PLANNED_PARENT[s][0]
        source = res[parent][0] if parent in res else (PROPOSED.get(parent) or _now(parent))
        return list(source), since, _sp(parent)
    parent = g.oxide_reached()[s][0]
    source = res[parent][0] if parent in res else (PROPOSED.get(parent) or _now(parent))
    return list(source), evolved_at(s) or reach(s), _sp(parent)


def _slot_worthy(c, types):
    """A move worth a level-up slot after an evolution: a good attack, an
    attack of the stage's own type, or a status move rated B or better, and
    never one that needs weather the player cannot set."""
    from . import laterlearn as ll
    return c in M() and c not in NEEDS_WEATHER and c not in SELF_KO and c not in ll._doubles_only() \
        and c not in NOT_PICKED and (
        good_attack(c, types) or _own_type_attack(c, types) or (rank(c) or 0) >= 3)


def carry_evolved(fam, res):
    """Ian (2026-09-28): a stage reached by an evolution with no level of its
    own gets its own, sparser list after it: its key moves, fewer than the
    pre-evolution learns after that point, so evolving early still costs
    moves and waiting stays a real choice. The candidates are the moves the
    pre-evolution learns after the evolution first becomes possible that are
    worth a slot for it, and its own good level-1-only moves at Kaizo's level
    for it or its nearest lines'. Its key moves, each at its source's level
    and by the generator's rules: (a) an attack of its own type of 50 or more
    that is not a strong one, when it has none by where it is first had;
    (b) its best attack of its own type; (c) its best other move, only when
    the pre-evolution learns four or more such moves after that point.
    Point 1's late move comes on top where it has none."""
    for s in fam:
        if s not in g._obtainable() or not not_by_level(s):
            continue
        lst, notes = list(res[s][0]), list(res[s][1])
        types, here = _types(s), reach(s)
        source, since, label = _evolution_source(s, res)
        have = {c for l, c in lst if l > 1 or l == 0}
        cands = [(lv, c, f"{label}'s {lv}") for lv, c in sorted(source)
                 if lv > since and c not in have and _slot_worthy(c, types)]
        pre_count = len({c for _lv, c, _src in cands})
        ev = kaizo_evidence(s)
        for _l1, c in [(l, c) for l, c in lst if l == 1]:
            if c in have or not (good_attack(c, types) or (rank(c) or 0) >= 4) or c in NEEDS_WEATHER:
                continue
            t = ev[c][1] if ev and c in ev and ev[c][2] is None else (analogue_level(s, c) if ev is None else None)
            if t and t > here:
                cands.append((t, c, "its own level 1, at Kaizo's level for it or its nearest lines'"))
        allowed = max(1, min(3, pre_count - 1)) if pre_count else 1

        def own_by(level, lst_):
            return any(_own_type_attack(cc, types) for l, cc in lst_
                       if (1 < l <= level) or (l == 0 and s in g.oxide_reached()))
        own = [x for x in cands if _own_type_attack(x[1], types)]
        roles = []
        if not own_by(here, lst):
            roles.append(sorted((x for x in own if not good_attack(x[1], types)), key=lambda x: x[0]))
        roles.append(sorted(own, key=lambda x: -_worth(s, x[1])))
        if pre_count >= 4:
            roles.append(sorted((x for x in cands if not _own_type_attack(x[1], types)
                                 and (good_attack(x[1], types) or (rank(x[1]) or 0) >= 4)),
                                key=lambda x: -_worth(s, x[1])))
        done = 0
        for role in roles:
            if done >= allowed:
                break
            for lv, c, src in role:
                if c in {cc for _l, cc in lst if _l > 1}:
                    continue
                placed, why, meta = _place(s, lst, c, lv, carried=True)
                CARRIED.append((s, c, lv, placed, why))
                if placed is None:
                    continue
                _commit(s, c, placed, meta, lst)
                lst = sorted(lst + [(placed, c)], key=lambda e: e[0])
                notes.append((c, f"new at {placed}: a key move after the evolution, from {src}"
                                 + (f"; {why}" if why else "")))
                done += 1
                break
        res[s] = (lst, notes)
    return res


def evolution_moves(fam, res):
    """Ian (2026-09-28): an evolution move (level 0, taught the moment the
    Pokemon evolves; never known by a wild, gift or trainer Pokemon), used
    sparingly. A stand-in-parent stage gets one: the strongest attack of its
    own type in the stand-in's list that the rules do not count as strong
    (Alolan Ninetales's Aurora Beam, since a Fire Vulpix carries no Ice move
    into the Ice Stone evolution). A stage reached by a stone or a held item
    that still goes more than one split without an attack of its own type
    gets one only where a single attack of its own type, never a strong one,
    closes the gap: the later games' own evolution move first, else the
    weakest that does it. Each is listed for Ian."""
    from . import laterlearn as ll
    for s in fam:
        if s not in g._obtainable():
            continue
        types = _types(s)
        lst, notes = list(res[s][0]), list(res[s][1])
        if any(l == 0 for l, _c in lst):
            continue
        pick = None
        if s in VIRTUAL_PARENT or s in PLANNED_PARENT:
            want = EVOLUTION_MOVE_TYPES.get(s, types)
            listed = ([c for _lv, c in virtual_parent_list(s)] if s in VIRTUAL_PARENT else []) \
                + [c for _lv, c in later_level_list(s)]
            def fitting(moves):
                return [c for c in dict.fromkeys(moves) if c in M() and M()[c]["type"].title() in want
                        and strength(c)[0] == "damage" and not good_attack(c, types)
                        and effective_power(c) >= STAB_GAP_POWER and c not in SELF_KO]
            own = fitting(listed)
            src = (f"the later games' {_sp(VIRTUAL_PARENT[s])} and {_sp(s)} lists" if s in VIRTUAL_PARENT
                   else f"the later games' {_sp(s)} list")
            if not own:
                # Nothing in the level lists (Galarian Weezing's Fairy Wind is
                # under 50): the later games' TM and tutor moves for it.
                own = fitting(later_moves_any(s))
                src = f"the later games' TM and tutor moves for {_sp(s)}, its level lists having none"
            if not own:
                # Nothing it learns in any game fits (its Fairy attacks are
                # Fairy Wind, under 50, or strong ones): the whole move table,
                # for Ian to weigh against the alternatives.
                own = fitting(M())
                src = (f"Oxide's whole move table, since nothing {_sp(s)} learns in any game fits "
                       f"(Ian may prefer one of its own, weaker or strong)")
            pick = max(own, key=lambda c: effective_power(c), default=None)
            why = f"the strongest {'/'.join(sorted(want))} attack that is not a strong move, from {src}"
        elif s in g.oxide_reached() and any(
                e.get("into") == s and e["method"].startswith(("USE_ITEM", "LEVEL_WITH_HELD_ITEM"))
                for e in (pokedex.load(data.ROOT, g.oxide_reached()[s][0]) or {}).get("evolutions", [])):
            if not gap_applies(s):
                continue
            lists = {x: res[x][0] for x in fam}
            if not breaks_gap(s, lists):
                continue
            modern = []
            for gkey, _name in reversed(ll.GAMES):
                rec = ll.game(gkey).get(s)
                if rec:
                    modern = [ll.oxide_move(e["Move"]) for e in rec.get("LevelMoves") or [] if e["Level"] == 0]
                    break
            source, _since, _label = _evolution_source(s, res)
            pool_ = modern + [c for _lv, c in sorted(source, key=lambda x: effective_power(x[1]))]                 + [c for l, c in lst if l == 1]
            for c in pool_:
                if c not in M() or not _own_type_attack(c, types) or good_attack(c, types)                         or effective_power(c) < STAB_GAP_POWER:
                    continue
                trial = dict(lists, **{s: [(0, c)] + lst})
                if not breaks_gap(s, trial):
                    pick = c
                    why = ("the later games' own evolution move" if c in modern else
                           "the weakest attack of its own type that closes its gap")
                    break
        if not pick:
            continue
        lst = [(0, pick)] + lst                 # an evolution move comes first, as the games list them
        notes.append((pick, f"new at 0: an evolution move, {why}; for Ian"))
        EVOLUTION_MOVES.append((s, pick, why))
        res[s] = (lst, notes)
    return res


def _two_turn(c):
    e = M()[c].get("effect") or ""
    return e in TWO_TURN or e.startswith("CHARGE_TURN")


def _stats(species):
    st = (pokedex.load(data.ROOT, species) or {}).get("stats") or {}
    return st.get("attack", 0) or 0, st.get("special_attack", 0) or 0


def _hit(species, c):
    """(strength, accuracy) of an attack for the stage: its effective power,
    with Skill Link's five hits for a multi-hit move, and a never-miss move
    at 101."""
    e = effective_power(c)
    if M()[c].get("effect") == "MULTI_HIT" and "SKILL_LINK" in ((pokedex.load(data.ROOT, species) or {}).get("abilities") or []):
        e = e * 5 / 3
    acc = M()[c].get("accuracy") or 101
    return e, acc


def adds(species, c, known):
    """Whether a move gives the stage something it lacks, given the moves it
    has by then (the Overseer's rule, 2026-09-28): a status move rated A or
    better it does not know; or an attack in its better category (either,
    when its attacking stats are within STAT_GAP) that is of a new type for
    it, or stronger or more reliable than every same-type, same-category
    attack it knows (Thunder beside Thunderbolt counts; Flamethrower after
    Fire Blast does not)."""
    if c in known or c in NOT_PICKED:
        return False
    if M()[c]["class"] == "STATUS":
        return (rank(c) or 0) >= 4
    atk, spa = _stats(species)
    cat = M()[c]["class"]
    if abs(atk - spa) >= STAT_GAP and cat != ("PHYSICAL" if atk > spa else "SPECIAL"):
        return False
    mine = [k for k in known if k in M() and M()[k]["class"] == cat and M()[k]["type"] == M()[c]["type"]]
    e, acc = _hit(species, c)
    for k in mine:
        ek, acck = _hit(species, k)
        # Stronger, or 20 points more accurate while keeping three quarters of
        # the power (Thunderbolt beside Thunder; not Flamethrower after Fire
        # Blast, nor BubbleBeam after Hydro Pump).
        if not (e > ek or (acc - acck >= 20 and e >= 0.75 * ek)):
            return False
    return True


def dominated(species, c, others):
    """Whether an attack is no better than a same-type, same-category attack
    among `others`: at least as strong and at least as accurate."""
    e, acc = _hit(species, c)
    return any(k in M() and M()[k]["type"] == M()[c]["type"] and M()[k]["class"] == M()[c]["class"]
               and _hit(species, k)[0] >= e and _hit(species, k)[1] >= acc for k in others if k != c)


@functools.lru_cache(maxsize=None)
def _power_rank():
    """{final stage the player can own: its base stat total's place among
    them, 0 the weakest to 1 the strongest}."""
    totals = {}
    for s in g._obtainable():
        if later_stages(s):
            continue
        st = (pokedex.load(data.ROOT, s) or {}).get("stats") or {}
        totals[s] = sum(st.values()) if st else 0
    order = sorted(totals.values())
    n = max(1, len(order) - 1)
    return {s: order.index(t) / n for s, t in totals.items()}


def late_level(species):
    """Where a stage's late move goes by its power: the weakest at 61, the
    strongest at 78, the rest between."""
    return LATE + round((78 - LATE) * _power_rank().get(species, 0))


def late_moves(fam, res):
    """Ian (2026-09-28): every final stage the player can own learns at least
    one real move by level-up in the Galactic split or later (61 to 78). Where
    its list has none, the candidate that adds most goes in: it must give the
    stage something it lacks by then (adds: a better or more reliable attack
    of its type in its better category, a new type, or a status move rated A
    or better), never a self-knockout, partner or evasion move, and a
    charging or out-of-reach move only when nothing else adds. Candidates come
    from Kaizo's list for it, the later games' level-up lists, its own level-1
    moves, then its TM and tutor moves; the one of most substance, then from
    the earliest of those sources, then of most worth. It goes to the later of
    its source's level and a level spread across 61 to 78 by the stage's
    power. A stage with nothing that adds is listed for Ian."""
    from . import laterlearn as ll
    lists = dict(PROPOSED)
    lists.update({x: res[x][0] for x in fam})
    for s in fam:
        if s not in g._obtainable() or later_stages(s) or reach(s) > 78:
            continue
        lst, notes = list(res[s][0]), list(res[s][1])
        if any(lv >= LATE and _real(s, c, lv, lst) for lv, c in lst):
            continue
        at = late_level(s)
        known = {c for c, l in had_from(s, dict(lists, **{s: lst})).items() if l <= at}
        cands = []
        for c, (kl, t, why) in (kaizo_evidence(s) or {}).items():
            if why is None:
                cands.append((c, t, f"Kaizo's {_sp(s)} at {kl}", 0))
        level_moves, _other = ll.later(s)
        for c, srcs in level_moves.items():
            game_name, lv = ll.latest_level(srcs)
            cands.append((c, lv, f"{game_name} at {lv}", 1))
        cands += [(c, LATE, "its own level 1", 2) for lv, c in lst if lv <= 1]
        rec = pokedex.load(data.ROOT, s) or {}
        machines = pokedex.machines(data.ROOT)
        cands += [(machines[m], LATE, "a TM it learns", 3) for m in rec.get("by_tm") or [] if m in machines]
        cands += [(c, LATE, "a tutor move it learns", 3) for c in rec.get("by_tutor") or []]
        best = None
        above_one = {c for l, c in lst if l > 1}
        for c, lv, src, prio in cands:
            if c not in M() or c in above_one or not adds(s, c, known):
                continue
            placed, why, meta = _place(s, lst, c, max(lv or LATE, at))
            if placed is None or not _real(s, c, placed, lst):
                continue
            key = (not _two_turn(c), _substance(c), -prio, _worth(s, c))
            if best is None or key > best[0]:
                best = (key, c, placed, src, why, meta)
        if best is None:
            LATE_FOR_IAN.append(s)
            continue
        _key, c, placed, src, why, meta = best
        _commit(s, c, placed, meta, lst)
        lst = sorted(lst + [(placed, c)], key=lambda e: e[0])
        notes.append((c, f"new at {placed}: a move in the last splits, from {src}" + (f"; {why}" if why else "")))
        LATE_ADDED.append((s, c, placed, src))
        res[s] = (lst, notes)
    return res


def ruled_lists(fam, res):
    """The lists Ian has asked for by name (RULED_LISTS), placed by the
    generator's rules but past the flags' first-of-type test, and listed for
    him by name."""
    for s in fam:
        if s not in RULED_LISTS or s not in g._obtainable():
            continue
        lst, notes = list(res[s][0]), list(res[s][1])
        for lv, c in RULED_LISTS[s]:
            if any(l > 1 and cc == c for l, cc in lst):
                continue
            placed, why, meta = _place(s, lst, c, lv, ruled=True)
            if placed is None:
                continue
            _commit(s, c, placed, dict(meta, ruled=True), lst)
            lst = sorted(lst + [(placed, c)], key=lambda e: e[0])
            notes.append((c, f"new at {placed}: Ian's list for it by name" + (f"; {why}" if why else "")))
            RULED_PLACED.append((s, c, placed))
        res[s] = (lst, notes)
    return res


def undo_dead_moves(fam, res):
    """The Overseer's check (2026-09-28): a moved entry must not land after a
    stronger same-type, same-category attack the stage has by then, where it
    is dead weight (Decidueye's Seed Bomb, moved from 32 to 60 after Leaf
    Blade at 55). Such a move goes back to its current level where it is not
    dead there and no Kaizo floor lies past that level; else it leaves (Ian's
    floor ruling wins over keeping it early). A delay counts only if waiting
    is a real choice. Repeated until nothing changes, since a move put back
    can make another dead."""
    lists = dict(PROPOSED)
    lists.update({x: res[x][0] for x in fam})
    for s in fam:
        now = {}
        for lv, c in _now(s):
            now.setdefault(c, lv)
        lst, notes = list(res[s][0]), list(res[s][1])
        evolved = s in g.oxide_reached()
        changed = False
        for _round in range(6):
            again = False
            for lv, c in list(lst):
                if lv <= 1 or c not in now or now[c] <= 1 or now[c] == lv or c not in M() \
                        or M()[c]["class"] == "STATUS":
                    continue
                others = [k for l, k in lst if k != c and ((1 < l <= lv) or (l == 0 and evolved))]
                others += [k for k, l in had_from(s, dict(lists, **{s: lst})).items() if l <= lv and k != c]
                if not dominated(s, c, set(others)):
                    continue
                lst = [e for e in lst if e != (lv, c)]
                back = now[c]
                others_back = [k for l, k in lst if k != c and ((1 < l <= back) or (l == 0 and evolved))]
                floor = FLOORS.get((s, c))
                if (back <= 1 or not dominated(s, c, set(others_back))) and not (floor and back < floor):
                    lst = sorted(lst + [(back, c)], key=lambda e: e[0])
                    notes.append((c, f"back at {back}: moved to {lv} it would come after a stronger move of its "
                                     f"type the stage has by then"))
                    DEAD_MOVED.append((s, c, lv, f"kept at {back}"))
                else:
                    why = (f"its Kaizo floor ({floor}) is past its old level ({back})" if floor and back < floor
                           else f"at {back} too it comes after a stronger move of its type")
                    notes.append((c, f"leaves: moved to {lv} it comes after a stronger move of its type the "
                                     f"stage has, and {why}"))
                    DEAD_MOVED.append((s, c, lv, "dropped"))
                    FLOORS.pop((s, c), None)
                changed = again = True
                break
            if not again:
                break
        if changed:
            res[s] = (lst, notes)
    return res


def dedupe(fam, res):
    """Drop repeated entries: the same move twice at one level, and a level-1
    entry of a move the stage also learns at level 0 or by level-up, except
    where it is one of the four a first stage knows when first had."""
    for s in fam:
        lst, notes = list(res[s][0]), list(res[s][1])
        keep_first = set(at_capture(lst, reach(s))) if s not in g.oxide_reached() else set()
        later = {c for l, c in lst if l == 0 or l > 1}
        out, seen = [], set()
        for l, c in lst:
            if (l, c) in seen:
                continue
            if l == 1 and c in later and c not in keep_first:
                continue
            seen.add((l, c))
            out.append((l, c))
        if len(out) != len(lst):
            res[s] = (out, notes)
    return res


def propose_family(fam):
    """{species: (list, notes)} for a family, proposed twice where the first
    proposal's own moves flag a stage or put it over the bar: that stage is
    held from the start in the second."""
    before = {s: strong_stage(s) for s in fam}
    res = {s: propose(s) for s in fam}
    PROPOSED.update({s: res[s][0] for s in fam})
    forced = [s for s in fam if not before[s] and (stage_flag(s) is not None
                                                   or (USE_BAR and passes_bar_proposed(s) is not None))]
    if forced:
        FORCED.update(forced)
        for s in fam:
            PROPOSED.pop(s, None)
        res = {s: propose(s) for s in fam}
        PROPOSED.update({s: res[s][0] for s in fam})
    res = carry_evolved(fam, res)
    res = ruled_lists(fam, res)
    res = late_moves(fam, res)
    res = evolution_moves(fam, res)
    PROPOSED.update({s: res[s][0] for s in fam})
    res = close_gaps(fam, res)
    res = undo_dead_moves(fam, res)
    res = dedupe(fam, res)
    PROPOSED.update({s: res[s][0] for s in fam})
    return res, forced


# ---- the proposal -----------------------------------------------------------------------

def _types(species):
    return {t.title() for t in (pokedex.load(data.ROOT, species) or {}).get("types", [])}


def _exclusives(species):
    """{MOVE_X: translated level} Kaizo gives this pre-evolution and none of
    its later stages by a reachable level-up."""
    ev = kaizo_evidence(species) or {}
    later = [s for ln in g.oxide_lines() if species in ln for s in ln[ln.index(species) + 1:]]
    if not later:
        return {}
    out = {}
    nxt = min(reach(s) for s in later[:1])
    for const, (_kl, t, why) in ev.items():
        # Only a move learnt after the level it could evolve at is one a
        # Pokemon kept from evolving alone gets.
        if why or t <= nxt:
            continue
        if any((kaizo_evidence(s) or {}).get(const, (0, 0, "x"))[2] is None for s in later):
            continue
        if all(ls.kaizo_lists().get(s) for s in later):
            out[const] = t
    return out


# Ian (2026-09-27): these five early moves go back to the split in which
# Kaizo gives the move to the species, or to its nearest Kaizo lines where
# Kaizo lacks it, and no earlier; the rest of the proposal stands.
KAIZO_SPLIT_FLOOR = {("SPECIES_VIKAVOLT", "MOVE_DISCHARGE"), ("SPECIES_MAGNEZONE", "MOVE_DISCHARGE"),
                     ("SPECIES_FRILLISH", "MOVE_SHADOW_BALL"), ("SPECIES_FRILLISH", "MOVE_SCALD"),
                     ("SPECIES_FLOETTE", "MOVE_MOONBLAST"), ("SPECIES_SPIRITOMB", "MOVE_DARK_PULSE")}


def kaizo_reach(species):
    """The level a Kaizo player can first have the stage at by evolving, 1 for a first stage."""
    return max(1, g.reached("kaizo", species)) if species in g.kaizo_reached() else 1


def kaizo_split_floor(species, const):
    """(the first Oxide level of the split in which Kaizo gives the move, the
    reason), or (None, the reason) when no Kaizo split gives it: the
    species' own entry, or where Kaizo lacks the species the same move on its
    nearest Kaizo lines. An entry below the level a Kaizo player can have the
    stage at is unavailable in Kaizo's play, and gives no split."""
    names = [n for n, _cap in ls.splits("kaizo")]

    def played(ks):
        entry = (kaizo_evidence(ks) or {}).get(const)
        if entry is None:
            return None
        kl = entry[0]
        if kl < kaizo_reach(ks):
            return "unavailable"
        return ls.split_of("kaizo", max(kl, kaizo_reach(ks)))
    if kaizo_evidence(species) is not None:
        got = played(species)
        if got in (None, "unavailable"):
            return None, (f"Kaizo's {_sp(species)} has it below level {kaizo_reach(species)}, where a "
                          f"Kaizo player first has it, so no Kaizo split gives it; Oxide's level stays"
                          if got else "Kaizo does not give it; Oxide's level stays")
        split = got
        why = f"Kaizo gives it in its {split} split"
    else:
        splits_ = [s for s in (played(ks) for ks in nearest_kaizo(species)) if s not in (None, "unavailable")]
        if not splits_:
            return None, "none of its nearest Kaizo lines learns it, so no Kaizo split gives it; Oxide's level stays"
        idx = sorted(names.index(s) for s in splits_)
        split = names[idx[(len(idx) - 1) // 2 if len(idx) % 2 else len(idx) // 2]]
        why = f"its nearest Kaizo lines get it in their {split} split"
    order = SPLITS
    prev = order[order.index(split) - 1] if split in order and order.index(split) > 0 else None
    return (pool.caps()[prev] + 1 if prev else 1), why


def kaizo_level_floor(species, const):
    """Kaizo's own level for the move: the species' own entry, or where Kaizo
    lacks it the median over its nearest Kaizo lines that learn the same move
    where a Kaizo player can; None when none does."""
    def played(ks):
        entry = (kaizo_evidence(ks) or {}).get(const)
        if entry is None or entry[0] < kaizo_reach(ks):
            return None
        return entry[0]
    if kaizo_evidence(species) is not None:
        return played(species)
    levels = [lv for lv in (played(ks) for ks in nearest_kaizo(species)) if lv is not None]
    return round(statistics.median(levels)) if levels else None


# {(species, MOVE_X): the level no placement goes below}: for the strong
# moves the proposal places from Kaizo (Ian, 2026-09-27), Kaizo's own level,
# but never past the end of the Oxide split that level translates to.
FLOORS = {}


def floor_level(kaizo_level):
    """Kaizo's own level, held to the last level of the Oxide split it
    translates to (Ian, 2026-09-27): Houndoom's Dark Pulse, Kaizo's 70,
    translates into Candice's split, so it goes no earlier than 56."""
    return min(kaizo_level, pool.caps()[_split_of(translate(kaizo_level))])
# Entries the one-level rule put a level or so under their floor to keep them
# in their split, when the split had no free level at or above it.
UNDER_FLOOR = set()
# {(species, MOVE_X): the translated placement a floor raised}, the lowest
# the one-level rule may then put it.
TRANSLATED = {}
# [(species, MOVE_X, Kaizo's level, the place kept)] where Kaizo's own level
# is past Oxide's 78: listed for Ian rather than taken out of play.
PAST_CAP = []


def propose(species):
    """(the proposed list, [(MOVE_X, what changed and why)])."""
    rec = pokedex.load(data.ROOT, species)
    if not rec:
        return [], []
    now = [tuple(e) for e in rec["learnset"]]
    types = _types(species)
    # A species the player can never own keeps its list but for the drops:
    # it only feeds trainers' default moves, which the trainer pass sets.
    obtainable = species in g._obtainable()
    ev = kaizo_evidence(species) if obtainable else {}
    # "No earlier than now" holds for a strong stage's own list (Ian,
    # 2026-09-27), and for what a pre-evolution learns without a real wait,
    # since that comes along into the strong stage; a longer wait is the
    # price of a delay, and stays free.
    strong_line = strong_stage(species)
    strong_later = strong_later_stages(species)
    held_until = max((h for _e, h in strong_later), default=0)
    held = lambda level: strong_line or level <= held_until
    notes = []
    first_level = {}
    for lv, c in now:
        first_level.setdefault(c, lv)
    out = []
    for lv, c in now:
        if c not in M():
            continue
        why = g._dropped(c, species, first_level[c], types, now)
        if why:
            if first_level[c] == lv:
                notes.append((c, f"leaves: {why}"))
            continue
        if lv > 1 and first_level[c] != lv:
            out.append((lv, c))          # a repeat keeps its place
            continue
        target = lv
        if lv > 1:
            kind, _p = strength(c)
            r = rank(c)
            t, src, kaizo_level = None, None, None
            if ev is not None and c in ev and ev[c][2] is None:
                t, src, kaizo_level = ev[c][1], f"Kaizo's {species[8:].title()} at {ev[c][0]}", ev[c][0]
            elif ev is None:
                t = analogue_level(species, c)
                src = "its nearest Kaizo lines" if t else None
                kaizo_level = analogue_kaizo_level(species, c) if t else None
                if t is not None and t < reach(species):
                    t, src = None, None      # below where the player can have it: unavailable
            if t is not None:
                if good_attack(c, types):
                    target = max(lv, t) if held(t) else t
                elif kind != "damage" and r is not None and r >= STRONG_RANK:
                    target = max(lv, t)
                elif kind != "damage" and r == 4:
                    target = max(lv, t) if held(t) else t
                # An entry below the level the stage is had at is the
                # relearner's; moving it to where the stage learns it adds the
                # move, so the rules for additions decide.
                here = reach(species) if species in g.oxide_reached() else 1
                if lv < here <= target:
                    kaizo_own = ev is not None and c in ev and ev[c][2] is None
                    if kind == "damage" and good_attack(c, types) and strong_line:
                        first = first_good_of_type(species, M()[c]["type"])
                        if first is None or target < first:
                            target = lv
                    elif kind != "damage" and (r or 0) >= STRONG_RANK and not kaizo_own:
                        target = lv
                # Ian (2026-09-27): a strong move's translated placement is
                # never earlier than Kaizo's own level, held to the end of the
                # Oxide split that level translates to (floor_level). Past
                # Oxide's 78 the rule would take it out of play, which his rule
                # of no level past 78 forbids; those keep the translated place
                # and are listed.
                strong_move = good_attack(c, types) or (r or 0) >= STRONG_RANK
                raised, fl = False, None
                if (target != lv and strong_move and kaizo_level
                        and (species, c) not in KAIZO_SPLIT_FLOOR):
                    if kaizo_level > 78:
                        PAST_CAP.append((species, c, kaizo_level, target))
                    else:
                        fl = floor_level(kaizo_level)
                        FLOORS[(species, c)] = fl
                        TRANSLATED[(species, c)] = target
                        raised = target < fl
                if raised:
                    if fl != lv:
                        notes.append((c, f"{lv} to {fl}: {src}, translated to {t}, and no earlier "
                                         f"than Kaizo's level of {kaizo_level} within its split"))
                    target = fl
                elif target != lv:
                    notes.append((c, f"{lv} to {target}: {src}, translated to {t}"))
        out.append((target, c))
    have = {c for _lv, c in out}
    # Kaizo's moves for this species that Oxide lacks: good attacks and S or
    # SSS status moves. A strong stage takes an attack only no earlier than
    # its first good one of that type now: an alternative, not earlier power.
    for c, (kl, t, why) in (ev or {}).items():
        if why or c in have or t <= 1:
            continue
        kind, _p = strength(c)
        r = rank(c)
        if kind == "damage":
            add = good_attack(c, types)
            if add and strong_line:
                first_same = first_good_of_type(species, M()[c]["type"])
                add = first_same is not None and t >= first_same
            # Learnt without a real wait, it reaches each strong later stage:
            # there too, only as an alternative to a good move of its type.
            for e, until in strong_later:
                if add and t <= until:
                    first_e = first_good_of_type(e, M()[c]["type"])
                    add = first_e is not None and t >= first_e
        else:
            add = r is not None and r >= STRONG_RANK
            for e, until in strong_later:
                if add and t <= until:
                    add = any(cc == c and lv2 <= t for lv2, cc in _now(e))
        if not add or g._signature_elsewhere(c, g._chain(species)):
            continue
        if kind == "damage":
            # No attack under nine tenths of a same-type one the stage
            # already knows by then (Kaizo's Slash beside Hyper Fang).
            best = max((strength(cc)[1] for lv2, cc in out if lv2 <= t and strength(cc)[0] == "damage"
                        and M()[cc]["type"] == M()[c]["type"]), default=0)
            if strength(c)[1] < 0.9 * best:
                continue
        drop = g._dropped(c, species, t, types, now)
        if drop:
            continue
        # No earlier than Kaizo's own level within its split (Ian, 2026-09-27).
        if kl > 78:
            PAST_CAP.append((species, c, kl, t))
        elif t < floor_level(kl):
            fl = floor_level(kl)
            FLOORS[(species, c)] = fl
            TRANSLATED[(species, c)] = t
            out.append((fl, c))
            notes.append((c, f"new at {fl}: Kaizo's {species[8:].title()} at {kl}, no earlier than "
                             f"that within its split (translated to {t})"))
            continue
        else:
            FLOORS[(species, c)] = floor_level(kl)
            TRANSLATED[(species, c)] = t
        out.append((t, c))
        notes.append((c, f"new at {t}: Kaizo's {species[8:].title()} at {kl}"))
    # Exclusive delays from Kaizo: the pre-evolution keeps the move, and a
    # later stage's level-up entry of it moves to level 1.
    for c, t in _exclusives(species).items():
        if not any(cc == c for _lv, cc in out):
            continue
        kind, _p = strength(c)
        r = rank(c)
        if not (good_attack(c, types) or (r is not None and r >= STRONG_RANK)):
            continue
        notes.append((c, f"an exclusive delay: Kaizo gives it to no later stage"))
    for pre in (g._chain(species)[:-1] if obtainable else []):
        for c, t in _exclusives(pre).items():
            kind, _p = strength(c)
            r = rank(c)
            if not (good_attack(c, _types(pre)) or (r is not None and r >= STRONG_RANK)):
                continue
            hit = [(lv, cc) for lv, cc in out if cc == c and lv > 1]
            if hit:
                out = [e for e in out if e not in hit] + [(1, c)]
                notes.append((c, f"{hit[0][0]} to 1: an exclusive delay, Kaizo gives it only to "
                                 f"{pre[8:].title()}"))
    # Ian's five (2026-09-27): no earlier than the split Kaizo gives the move
    # in; where no Kaizo split gives it, Oxide's own level.
    for c in [c for (s, c) in KAIZO_SPLIT_FLOOR if s == species]:
        hit = [(lv, cc) for lv, cc in out if cc == c and lv > 1]
        was = next((lv for lv, cc in now if cc == c), None)
        if not hit or was is None:
            continue
        floor, why = kaizo_split_floor(species, c)
        # And no earlier than Kaizo's own level (Ian, 2026-09-27): Spiritomb's
        # 37, Vikavolt's the level its nearest lines learn the move at.
        level = kaizo_level_floor(species, c) if floor else None
        new = max(hit[0][0], floor, level or 0) if floor else was
        if level:
            FLOORS[(species, c)] = level
            why += f", and no earlier than Kaizo's level of {level}"
        if new != hit[0][0]:
            out = [e for e in out if e != hit[0]] + [(new, c)]
            notes.append((c, f"{hit[0][0]} to {new}: Ian's ruling on five early moves, {why}"))
    # The move-pool survey's level-1 picks, for the species whose only start
    # was Splash or Teleport (Ian, 2026-09-27; Hoppip's is Leafage).
    pick = g.RULED_FIRST.get(species)
    if pick in M() and (1, pick) not in out:
        out = [e for e in out if e[1] != pick] + [(1, pick)]
        notes.append((pick, "new at 1: the move-pool survey's pick"))
    # A first stage keeps an attack where its first one was.
    if species not in g.oxide_reached():
        attacks = lambda lst: sorted(lv for lv, cc in lst if lv > 1 and strength(cc)[0] == "damage")
        before, after = attacks(now), attacks(out)
        if before and (not after or after[0] > before[0]):
            filler = g.STARTER_BY_TYPE.get(sorted(types)[0] if types else "Normal", "MOVE_TACKLE")
            first_type = (rec.get("types") or ["NORMAL"])[0].title()
            filler = g.STARTER_BY_TYPE.get(first_type, filler)
            if filler in M() and filler not in {cc for _lv, cc in out}:
                out.append((before[0], filler))
                notes.append((filler, f"new at {before[0]}: keeps the first attack's level"))
    out, crowded = spread_levels(species, now, out, notes, strong_line, held_until)
    CROWDED[species] = crowded
    order = {c: i for i, (_lv, c) in enumerate(now)}
    out.sort(key=lambda e: (e[0], order.get(e[1], 999), e[1]))
    return out, notes


# {species: [(MOVE_X, level)]} the same-level rule found no room for.
CROWDED = {}


def spread_levels(species, now, out, notes, strong_line, held_until=0):
    """Ian's rule (2026-09-27): no two moves on one level. An entry the
    method moved or added that shares its level with another goes to the
    nearest free level in the same split, keeping the other rules: a good
    attack or a strong status move no earlier than Oxide has it now on a
    marked line (ties go later), a weak attack no later than now (ties go
    earlier), nothing at 1 or past 78. Oxide's own pairs (Rest and Sleep
    Talk) stay. A case with no room is returned, not forced."""
    kept = set(now)
    was = {}
    for lv, c in now:
        was.setdefault(c, lv)
    types = _types(species)
    crowded = []
    taken = collections.Counter(lv for lv, _c in out if lv > 1)
    result = []
    for lv, c in sorted(out, key=lambda e: ((e[0], e[1]) in kept, e[0])):
        if lv <= 1 or (lv, c) in kept or taken[lv] <= 1:
            result.append((lv, c))
            continue
        strong = good_attack(c, types) or (rank(c) or 0) >= STRONG_RANK
        lo = was.get(c, 2) if strong and (strong_line or lv <= held_until) and c in was else 2
        lo = max(lo, FLOORS.get((species, c), 2))    # never below Kaizo's own level
        hi = was.get(c, 78) if strength(c)[0] == "damage" and not good_attack(c, types) and c in was else 78
        split = _split_of(lv)
        step = [d for k in range(1, 12) for d in ((k, -k) if strong else (-k, k))]
        new = next((lv + d for d in step if lo <= lv + d <= min(hi, 78) and taken[lv + d] == 0
                    and _split_of(lv + d) == split), None)
        if new is None and strong and (species, c) in FLOORS:
            # No room in the split at or above the floor, which is Kaizo's
            # level held to the split's end: the move stays in the split its
            # level translates to (Ian, 2026-09-27), a level or so under the
            # floor, as long as it is not earlier than now on a strong stage.
            lo_now = was.get(c, 2) if strong_line or lv <= held_until else 2
            lo_now = max(lo_now, TRANSLATED.get((species, c), 2))   # never under its translated place
            new = next((lv + d for d in step if lo_now <= lv + d <= min(hi, 78) and taken[lv + d] == 0
                        and _split_of(lv + d) == split), None)
            if new is not None:
                UNDER_FLOOR.add((species, c))
        if new is None and strong:
            # Still no room: a strong move may go later, into the next split,
            # which never makes it earlier.
            new = next((lv + d for d in range(1, 12) if lv + d <= min(hi, 78) and taken[lv + d] == 0), None)
        if new is None:
            crowded.append((c, lv))
            result.append((lv, c))
            continue
        taken[lv] -= 1
        taken[new] += 1
        result.append((new, c))
        notes.append((c, f"{lv} to {new}: the same-level rule (another move is at {lv})"
                         + ("; its split has no free level at or above its floor, so it stays in the "
                            "split a level under it" if (species, c) in UNDER_FLOOR and new < lv else "")))
    return result, crowded


def propose_all(species_list):
    PROPOSED.clear()
    for sp in species_list:
        PROPOSED[sp] = propose(sp)[0]


# ---- delays --------------------------------------------------------------------------

def _split_of(level):
    caps = pool.caps()
    return next((s for s in SPLITS if level <= caps[s]), "Post")


def delays(pre, evo, lists):
    """Each move the pre-evolution learns from the level it can evolve, with
    Ian's four tests: (1) strong, or the line's first good move of its type;
    (2) learnt by the cap of the split it can evolve in; (3) the evolved
    stage gets it, or a same-type attack at least as strong, a split or more
    later, or never; (4) nothing the evolved stage learns in between is a
    same-type attack within a tenth of it."""
    at = evolved_at(evo) or 0
    if at <= 1 or at > 100:
        return []
    caps = pool.caps()
    evolve_split = _split_of(at)
    types = _types(pre)
    out = []
    firsts = {}
    for lv, c in sorted(lists[pre]):
        kind, p = strength(c)
        if kind == "damage" and is_good(c, types):
            firsts.setdefault(M()[c]["type"], lv)
    for lv, c in lists[pre]:
        kind, p = strength(c)
        # A wait means keeping it back past the level it could evolve at: a
        # move learnt at that very level comes before the evolution.
        if lv <= at or c in SELF_KO or (kind != "damage" and (rank(c) or 0) < STRONG_RANK):
            continue
        t1 = (kind == "damage" and (p >= GOOD_ANY or firsts.get(M()[c]["type"]) == lv)) or \
             (kind != "damage" and (rank(c) or 0) >= STRONG_RANK)
        if not t1:
            continue
        # Test 2 is reported, not applied: Ian ruled a wait longer than a
        # split worth it (2026-09-27), so the wait is given in splits.
        t2 = SPLITS.index(_split_of(lv)) - SPLITS.index(evolve_split) \
            if _split_of(lv) in SPLITS and evolve_split in SPLITS else None
        evo_levels = [e for e, cc in lists[evo] if e > 1 and e >= at and (
            cc == c or (kind == "damage" and strength(cc)[0] == "damage"
                        and M()[cc]["type"] == M()[c]["type"] and strength(cc)[1] >= 0.9 * p))]
        first_evo = min(evo_levels) if evo_levels else None
        if first_evo is None:
            t3, t4 = True, True
        else:
            # A split or more later, and at least five levels: a two-level
            # wait across a split's boundary is no real choice.
            t3 = first_evo - lv >= 5 and (
                SPLITS.index(_split_of(first_evo)) >= SPLITS.index(_split_of(lv)) + 1
                if _split_of(first_evo) in SPLITS and _split_of(lv) in SPLITS else True)
            t4 = first_evo > lv
        out.append((c, lv, first_evo, t1, t2, t3, t4))
    return out


# ---- the report ------------------------------------------------------------------------

def _names(lst):
    return ", ".join(f"{lv} {name(c)}" for lv, c in lst) or "(none)"


def _first_wild(species):
    rows = [(e["lo"], e["split"], e["area"]) for e in _wild() if e["species"] == species]
    return min(rows) if rows else None


@functools.lru_cache(maxsize=None)
def _wild_rows():
    from . import learnwild
    return tuple(learnwild.oxide_encounters())


def _wild():
    return _wild_rows()


def routes(species, lists):
    """{MOVE_X: the earliest level the stage can know it by any route}, for
    good attacks and S or SSS status moves: its own list from the level it
    is had, or a pre-evolution's, kept back until it learns the move and
    then evolved (known from max(that level, the stage's own))."""
    here = reach(species) if species in g.oxide_reached() else 1
    types = _types(species)
    out = {}
    for stage in g._chain(species):
        start = reach(stage) if stage in g.oxide_reached() else 1
        for lv, c in lists.get(stage, []):
            if lv < start or (lv <= 1 and stage in g.oxide_reached()):
                continue
            if not (good_attack(c, types) or (rank(c) or 0) >= STRONG_RANK):
                continue
            at = max(lv, here)
            out[c] = min(out.get(c, 999), at)
    return out


def nowait_routes(species, lists):
    """{MOVE_X: (the earliest level a stage knows it by, the stage whose
    list gives it)} for its good attacks and S or SSS status moves, from its
    own list from the level it is had, or from a pre-evolution's without a
    real wait (under WAIT levels past the stage's own), which comes along
    when it evolves."""
    here = reach(species) if species in g.oxide_reached() else 1
    types = _types(species)
    out = {}
    chain = g._chain(species)
    for i, stage in enumerate(chain):
        own = stage == species
        start = reach(stage) if stage in g.oxide_reached() else 1
        # A pre-evolution's move comes along only when learnt under WAIT
        # levels past the level it can first evolve at (strong_later_stages).
        until = None if own else (evolved_at(chain[i + 1]) or here) + WAIT - 1
        for lv, c in lists.get(stage, []):
            if c not in M() or lv < start or (lv <= 1 and stage in g.oxide_reached()):
                continue
            if not (good_attack(c, types) or (rank(c) or 0) >= STRONG_RANK):
                continue
            if own and lv < here:
                continue
            if not own and lv > until:
                continue
            at = max(lv, here)
            if c not in out or at < out[c][0]:
                out[c] = (at, stage)
    return out


def line_report(first, out=sys.stdout):
    fam = family(first)
    lists_now = {s: [tuple(e) for e in (pokedex.load(data.ROOT, s) or {}).get("learnset", [])] for s in fam}
    results, forced = propose_family(fam)
    lists_new = {s: results[s][0] for s in fam}
    flags = {s: stage_flag(s) for s in fam}
    print(f"\n## {' / '.join(s[8:].title() for s in fam)}", file=out)
    mark = any(flags.values())
    if forced:
        print(f"\nHeld as strong because the first proposal's own moves flagged them or put them "
              f"over the bar: {', '.join(s[8:].title() for s in forced)}.", file=out)
    print(f"\nPower flags: " + ("; ".join(
        f"{s[8:].title()} in {f[0]}'s split ({f[1]}), {severity(f[0])}" for s, f in flags.items() if f)
        if mark else "none before Byron's split") + ".", file=out)
    for s in fam:
        ev = kaizo_evidence(s)
        src = "Kaizo's own list" if ev is not None else \
            "Kaizo lacks it; nearest Kaizo lines " + ", ".join(k[8:].title() for k in nearest_kaizo(s))
        print(f"\n**{s[8:].title()}**, had from {reach(s) if reach(s) > 1 else 'the start'}"
              f" ({src}).", file=out)
        print(f"\n- Now: {_names(lists_now[s])}", file=out)
        print(f"- Proposed: {_names(lists_new[s])}", file=out)
        for c, why in results[s][1]:
            print(f"- {name(c)}: {why}", file=out)
        if ev:
            skipped = [(c, v) for c, v in ev.items() if v[2] and "level 1" not in v[2]
                       and (strength(c)[0] == "damage" and is_good(c, _types(s)) or (rank(c) or 0) >= 4)]
            for c, (kl, t, why) in skipped:
                print(f"- Kaizo's {name(c)} at {kl} does not count: {why}", file=out)
        if flags.get(s):
            a, b = routes(s, lists_now), routes(s, lists_new)
            moved = [(name(c), a.get(c), b.get(c)) for c in sorted(set(a) | set(b), key=name)
                     if a.get(c) != b.get(c)]
            if moved:
                print(f"- By any route (a pre-evolution kept back where that is sooner): " + "; ".join(
                    f"{n} {'never' if x is None else 'from ' + str(x)} now, "
                    f"{'never' if y is None else 'from ' + str(y)} proposed" for n, x, y in moved)
                      + ".", file=out)
            else:
                print("- By any route, its good moves come no sooner than now.", file=out)
        fw = _first_wild(s)
        if fw:
            lv, split, area = fw
            print(f"- Caught wild from {lv} ({area.replace('encounters_', '').replace('_', ' ').title()}, "
                  f"{split}'s split): knows {', '.join(name(c) for c in at_capture(lists_now[s], lv))} "
                  f"now; {', '.join(name(c) for c in at_capture(lists_new[s], lv))} proposed.",
                  file=out)
    for pre in fam:
        for evo in fam:
            if g.oxide_reached().get(evo, (None,))[0] != pre:
                continue
            ds = delays(pre, evo, lists_new)
            if ds:
                for c, lv, fe, t1, wait, t3, t4 in ds:
                    fails = [str(i) for i, t in ((1, t1), (3, t3), (4, t4)) if not t]
                    splits = "" if wait is None else \
                        f", {wait} split{'s' if wait != 1 else ''} past the split it can evolve in"
                    print(f"- Delay, {pre[8:].title()} to {evo[8:].title()}: {name(c)} at {lv}{splits}; "
                          f"{evo[8:].title()} {'at ' + str(fe) if fe else 'never'}: "
                          f"{'counts' if not fails else 'does not count (fails test ' + ', '.join(fails) + ')'}.",
                          file=out)
    crowded = [(s, c, lv) for s in fam for c, lv in CROWDED.get(s, [])]
    if crowded:
        print("- No free level in its split for: " + "; ".join(
            f"{s[8:].title()}'s {name(c)} at {lv}" for s, c, lv in crowded) + " (listed for Ian).",
              file=out)
    print("\n" + checks(fam, lists_now, lists_new, mark), file=out)


def checks(fam, now, new, mark):
    """The check list, as one line of results."""
    res = [(label, not bad) for label, bad in check_results(fam, now, new)]
    return "Checks: " + "; ".join(f"{label}, {'yes' if ok else 'NO'}" for label, ok in res) + "."


def check_results(fam, now, new):
    """[(check, [what breaks it])] for one family's lists now and proposed."""
    res = []
    over = [(s, lv, c) for s in fam for lv, c in new[s] if lv > 78 and (lv, c) not in now[s]]
    res.append(("nothing new past 78", over))
    weather = [(s, c) for s in fam for _lv, c in new[s] if c in g.WEATHER_MOVES and s in g._obtainable()]
    res.append(("no weather move", weather))
    from . import b6
    cut = [(s, c) for s in fam for _lv, c in new[s] if c in b6.DEAD_MOVES]
    res.append(("no cut move", cut))
    added_dead = [(s, c) for s in fam for lv, c in new[s]
                  if c not in {cc for _l, cc in now[s]} and g._dropped(c, s, lv, _types(s))]
    res.append(("no dead weight added", added_dead))
    later_weak = []
    earlier_strong = []
    for s in fam:
        types = _types(s)
        a = {}
        for lv, c in now[s]:
            a.setdefault(c, lv)
        kept = set(now[s])
        for lv, c in new[s]:
            if c not in a or lv <= 1 or a[c] <= 1 or (lv, c) in kept:
                continue
            kind, _p = strength(c)
            if kind == "damage" and not is_good(c, types) and lv > a[c]:
                later_weak.append((s, c))
            if strong_stage(s) and lv < a[c] and (good_attack(c, types) or (rank(c) or 0) >= STRONG_RANK):
                earlier_strong.append((s, c))
            if kind != "damage" and (rank(c) or 0) >= STRONG_RANK and lv < a[c]:
                earlier_strong.append((s, c))
        # What a strong stage has without a real wait, by any route.
        if strong_stage(s):
            was, will = nowait_routes(s, now), nowait_routes(s, new)
            for c, (lv, via) in will.items():
                if c in was:
                    bad = lv < was[c][0]
                elif strength(c)[0] == "damage":
                    firsts = [was[cc][0] for cc in was if strength(cc)[0] == "damage"
                              and M()[cc]["type"] == M()[c]["type"]]
                    bad = not firsts or lv < min(firsts)
                else:
                    # A new S or SSS move: only on the stage's own list, where
                    # Kaizo gives that species the move.
                    kaizo_own = (kaizo_evidence(via) or {}).get(c, (0, 0, "none"))[2] is None
                    bad = via != s or not kaizo_own
                # Ian's rulings of 2026-09-28 place past the first-of-type
                # test: an attack of the stage's own type where it has none
                # good by then, and moves in the last splits.
                if bad and (s, c) not in earlier_strong and (s, c) not in RULED:
                    earlier_strong.append((s, c))
    res.append(("no weak attack later than now", later_weak))
    res.append(("no strong move earlier than now on a strong stage, nor any S or SSS status move",
                earlier_strong))
    shared = []
    for s in fam:
        kept = set(now[s])
        levels = collections.Counter(lv for lv, _c in new[s] if lv > 1)
        shared += [(s, lv, c) for lv, c in new[s] if lv > 1 and levels[lv] > 1 and (lv, c) not in kept
                   and (c, lv) not in CROWDED.get(s, [])]
    res.append(("no two moves on one level that the method placed", shared))
    under = [(s, c) for s in fam for lv, c in new[s] if (s, c) in FLOORS and 1 < lv < FLOORS[(s, c)]
             and (s, c) not in UNDER_FLOOR]
    res.append(("no strong move placed earlier than Kaizo's level within its split", under))
    for_ian = {x[0] for x in STAB_FOR_IAN}
    gaps = [(s, "no attack of its own type") for s in fam if gap_applies(s) and widens_gap(s, now, new)
            and s not in for_ian]
    res.append(("no stage more than one split without an attack of its own type of 50 or more", gaps))
    ends = g._ends()
    wild_end = [(s, c) for s in fam for lv, c in new[s]
                if ls.metrics._compact(name(c)) in ends and 1 < lv <= g.wild_top(s)
                and (lv, c) not in now[s]]
    res.append(("no move that ends a wild encounter moved into the wild levels", wild_end))
    no_late = [(s, "no real move at 61 or later") for s in fam
               if s in g._obtainable() and not later_stages(s) and reach(s) <= 78
               and not any(lv >= LATE and _real(s, c, lv, new[s]) for lv, c in new[s])
               and s not in LATE_FOR_IAN]
    res.append(("every final stage has a real move in the last splits, or is listed for Ian", no_late))
    bare = [(s, "nothing after it is first had") for s in fam
            if s in g._obtainable() and not_by_level(s)
            and not any((lv > reach(s) or lv == 0) and _real(s, c, max(lv, reach(s)), new[s])
                        for lv, c in new[s])]
    res.append(("every stage reached without a level learns a real move after it is first had", bare))
    dead = []
    for s in fam:
        first_now = {}
        for lv, c in now[s]:
            first_now.setdefault(c, lv)
        for lv, c in new[s]:
            if lv <= 1 or c not in first_now or first_now[c] <= 1 or first_now[c] == lv or c not in M() \
                    or M()[c]["class"] == "STATUS":
                continue
            others = {k for l, k in new[s] if k != c and ((1 < l <= lv) or (l == 0 and s in g.oxide_reached()))}
            if dominated(s, c, others):
                dead.append((s, c))
    res.append(("no moved entry lands after a stronger move of its type and category", dead))
    return res


def flags_report(out=sys.stdout):
    rows = []
    for ln in g.oxide_lines():
        for s in ln:
            f = stage_flag(s)
            if f:
                rows.append((SPLITS.index(f[0]), s, f))
    seen = set()
    for _i, s, (split, why) in sorted(rows):
        if s in seen:
            continue
        seen.add(s)
        print(f"{s[8:].title():16} {split:9} {severity(split):24} {why}", file=out)


# ---- the full proposal ------------------------------------------------------------------

PROPOSAL_MD = os.path.join(data.ROOT, "docs", "oxide", "learnset-proposal.md")
PROPOSAL_TSV = os.path.join(data.ROOT, "docs", "oxide", "learnset-proposal.tsv")


def families():
    """Each family once, by its first stage, in Oxide's species order."""
    seen, out = set(), []
    for ln in g.oxide_lines():
        if ln[0] not in seen:
            seen.add(ln[0])
            out.append(ln[0])
    return out


def full_run(log=None):
    """Every family proposed as line_report proposes one: each species' list
    and notes, and each stage's flags, bar reading, delays, crowded cases
    and check failures."""
    PROPOSED.clear()
    CROWDED.clear()
    FORCED.clear()
    FLOORS.clear()
    UNDER_FLOOR.clear()
    STAB_KEPT.clear()
    STAB_FOR_IAN.clear()
    for held in (CARRIED, LATE_ADDED, LATE_FOR_IAN, EVOLUTION_MOVES, RULED_PLACED, DEAD_MOVED):
        held.clear()
    RULED.clear()
    TRANSLATED.clear()
    PAST_CAP.clear()
    run = {"now": {}, "lists": {}, "notes": {}, "flags": {}, "bar": {}, "delays": [],
           "checks": collections.defaultdict(list), "crowded": [], "forced": []}
    fams = families()
    for n, first in enumerate(fams, 1):
        fam = [s for s in family(first) if s not in run["lists"]]
        if not fam:
            continue
        now = {s: _now(s) for s in fam}
        res, forced = propose_family(fam)
        run["forced"] += forced
        new = {s: res[s][0] for s in fam}
        for s in fam:
            run["now"][s], run["lists"][s], run["notes"][s] = now[s], new[s], res[s][1]
            run["flags"][s] = stage_flag(s)
            if USE_BAR and not run["flags"][s]:
                run["bar"][s] = passes_bar(s)
        for pre in fam:
            for evo in fam:
                if g.oxide_reached().get(evo, (None,))[0] == pre:
                    run["delays"] += [(pre, evo) + row for row in delays(pre, evo, new)]
        for label, bad in check_results(fam, now, new):
            run["checks"][label] += bad
        run["crowded"] += [(s, c, lv) for s in fam for c, lv in CROWDED.get(s, [])]
        if log and n % 25 == 0:
            print(f"  {n} of {len(fams)} families", file=log, flush=True)
    return run


def _first(lst):
    out = {}
    for lv, c in lst:
        out.setdefault(c, lv)
    return out


def _kind_of(why):
    """A note's reason, grouped for the counts."""
    for key, label in (("leaves:", None),
                       ("a key move after the evolution", "a key move after an evolution without a level (Ian, 2026-09-28)"),
                       ("a move in the last splits", "a move in the last splits (Ian, 2026-09-28)"),
                       ("an evolution move", "an evolution move, for Ian (2026-09-28)"),
                       ("same-level rule", "the one-level rule"),
                       ("exclusive delay", "an exclusive delay from Kaizo"),
                       ("survey's pick", "the move-pool survey's first move"),
                       ("keeps the first attack", "a first stage keeps its first attack"),
                       ("nearest Kaizo lines", "Kaizo's nearest lines, translated by split"),
                       ("Kaizo's", "Kaizo's own list for the species, translated by split")):
        if key in why:
            return label if label else "leaves: " + why.split("leaves: ", 1)[1]
    return why


def _sp(s):
    return s[8:].replace("_", " ").title()


def cap(text):
    """The first letter upper case, the rest as written (S, SSS and names keep theirs)."""
    return text[:1].upper() + text[1:]


def full_report(md=PROPOSAL_MD, tsv=PROPOSAL_TSV, log=sys.stdout):
    """Run every family and write the proposal's summary and its entries."""
    from . import learnwild
    run = full_run(log)
    lists, now = run["lists"], run["now"]
    # The entries, for the apply step: every proposed entry and every dropped move.
    counts, dropped, moved_by = collections.Counter(), collections.Counter(), collections.Counter()
    with open(tsv, "w", encoding="utf-8") as f:
        f.write("species\tmove\tlevel_now\tlevel_proposed\tchange\twhy\n")
        for s in sorted(lists):
            a, b = _first(now[s]), _first(lists[s])
            why = collections.defaultdict(list)
            for c, w in run["notes"][s]:
                why[c].append(w)
            for lv, c in lists[s]:
                if c not in M():
                    continue
                change = "added" if c not in a else "moved" if b.get(c) != a[c] and lv == b[c] else "same"
                if lv != b[c]:
                    change = "same"          # a repeat keeps its place
                counts[change] += 1
                was = lv if (lv, c) in set(now[s]) else a.get(c, "")
                f.write(f"{s}\t{name(c)}\t{was}\t{lv}\t{change}\t{'; '.join(why[c])}\n")
                for w in why[c]:
                    if change in ("added", "moved"):
                        moved_by[(change, _kind_of(w))] += 1
            for c, lv in a.items():
                if c not in b and c in M():
                    counts["dropped"] += 1
                    reason = next((_kind_of(w) for w in why[c] if "leaves" in w), "leaves")
                    dropped[reason] += 1
                    f.write(f"{s}\t{name(c)}\t{lv}\t\tdropped\t{'; '.join(why[c])}\n")
    changed = sum(1 for s in lists if lists[s] != now[s])
    run["unobtainable"] = sorted(s for s in lists if s not in g._obtainable())
    # Good attacks and strong status moves that come a split or more sooner.
    sooner = []
    for s in sorted(lists):
        types = _types(s)
        a, b = _first(now[s]), _first(lists[s])
        for c, lv in b.items():
            if lv <= 1 or not (good_attack(c, types) or (rank(c) or 0) >= STRONG_RANK):
                continue
            was = a.get(c)
            at = lambda level: SPLITS.index(_split_of(level)) if _split_of(level) in SPLITS else len(SPLITS)
            if was is not None and (was <= lv or at(lv) >= at(was)):
                continue
            if was is None and _split_of(lv) not in SPLITS[:SPLITS.index("Byron")]:
                continue
            sooner.append((s, c, was, lv))
    # The analyses on Oxide now and on the proposal.
    g.PROPOSED.clear()
    g.PROPOSED.update({s: [list(e) for e in lst] for s, lst in lists.items()})
    learnwild.clear()
    analyses = {}
    for game in ("oxide", "proposal"):
        rows, later = learnwild.readings(game)
        caps = learnwild._caps(game)
        by = collections.defaultdict(lambda: [0, 0])
        for r in rows:
            by[r["split"]][0] += 1
            by[r["split"]][1] += any(g._good(e) for e in g.worth(game, r, caps.get(r["split"], 100)))
        analyses[game] = {"slots": len(rows), "ends": sum(1 for r in rows if r["ends"]),
                          "self_ko": sum(1 for r in rows if r["self_ko"]), "later": len(later),
                          "bare": len(g.bare_catches(game)), "good": dict(by)}
    for game in ("kaizo", "oxide", "proposal"):
        dl = [r for r in g.delays(game) if r[8] == "delay" and g.real_wait(game, r)]
        n, strong = g.never_learnt(game)
        analyses.setdefault(game, {}).update({"wait": len({r[1] for r in dl}), "never": n,
                                              "never_strong": strong})
    learnwild.clear()
    with open(md, "w", encoding="utf-8") as out:
        _write_md(out, run, counts, changed, dropped, moved_by, sooner, analyses)
    print(f"wrote {os.path.relpath(md, data.ROOT)} and {os.path.relpath(tsv, data.ROOT)}", file=log)
    return run


def _write_md(out, run, counts, changed, dropped, moved_by, sooner, analyses):
    lists = run["lists"]
    p = lambda *a: print(*a, file=out)
    p("# The learnset proposal\n")
    p(f"Written by `learnplan.py full` (2026-09-27) for the Overseer to read before Ian. It "
      f"proposes level-up lists for all {len(lists)} species; nothing here is in the game "
      f"data. `docs/oxide/learnset-proposal.tsv` has every entry, now and proposed, with the "
      f"reason for each change, and `learnplan.py line <species>` prints one line in full, "
      f"with its delays and check list.\n")
    p("## The rules it applies\n")
    p("It starts from Oxide's lists as they are and changes an entry only where one of Ian's "
      "rules asks for it:\n")
    for rule in (
            "Kaizo's placements count per species, translated by split: a Kaizo level goes to the "
            "same point of the same split in Oxide, so nothing lands past 78. An entry counts only "
            "where Kaizo's move is Oxide's at like values, and one that lands below the level the "
            "player can have the stage at (its evolution level, or a first stage's earliest catch, "
            "gift or hatch) means unavailable, not early.",
            "A species Kaizo lacks takes its placements from the Kaizo species nearest it in power "
            "at the same stage of their lines, under the same test of where the player can have it.",
            "A move's worth is what the Pokemon knows at capture plus what it learns by level-up "
            "after (the capture rule); a move's downsides count against it (lock-in, Uproar the "
            "worst, a recharge turn, heavy recoil and self-drops).",
            "A weak attack never moves later than now, and none is added.",
            "Status moves follow Ian's tier list (`docs/oxide/status-move-tiers.md`): S and SSS "
            "are strong, never earlier than now and added only where Kaizo gives the species the "
            "move; the instant-death moves and the hazards other than Toxic Spikes and Sticky Web "
            "are unrated.",
            "The power flags (base Speed over 100, or base Attack or Special Attack over 100 with a "
            "move of 100 or more of that kind the stage can have) run over the splits before "
            "Byron's: before Maylene's the line is brought to Ian by name, in Maylene's a very "
            "close look, in Wake's a close look.",
            "The power bar (Ian's Talonflame test, thresholds provisional): a stage at the split's "
            "cap with the moves it can have that outspeeds more than half the split's trainer "
            "Pokemon and knocks out more than a quarter in one hit.",
            "A flagged stage, or one over the bar, gets no strong move earlier than now on its own "
            "list and no new coverage ahead of its first good move of that type. The same holds for "
            "what a pre-evolution learns within four levels of the strong stage's evolution, since "
            "that comes along with no real wait. A pre-evolution kept back five levels or more "
            "may still reach a move sooner; that route is a delay, and it stays.",
            "A stage is judged strong on Oxide's lists now and again on the proposal's: one that "
            "the proposal's own moves would flag or put over the bar is proposed again as held.",
            "A delay counts only when waiting is a real choice: a strong move learnt past the "
            "level the stage could evolve at, that the evolved stage gets a split and five levels "
            "later or never, with no same-type move within a tenth of it between.",
            "No two moves on one level: a moved or added entry that shares a level goes to the "
            "nearest free level in the same split, within the other rules.",
            "The dead-weight rule, the move pool's first cut and the weather ruling remove "
            "entries; nothing that ends a wild encounter moves into the levels the species is "
            "met wild at.",
            "A strong move placed from Kaizo is never earlier than Kaizo's own level (Ian, "
            "2026-09-27), or, where Kaizo lacks the species, its nearest lines' level, but never "
            "past the end of the Oxide split that level translates to (Houndoom's Dark Pulse, "
            "Kaizo's 70, no earlier than 56, the end of Candice's split); where that level is past "
            "78 the translated place stays, listed below for Ian.",
            "No stage the player can have goes more than one split without an attack of its own "
            "type of 50 or more by effective power (Ian, 2026-09-27), counting what it brings "
            "from a pre-evolution evolved on time; a stage the player can evolve by the end of "
            "Gardenia's split is exempt, since only a player who keeps it back meets the gap. "
            "Where the proposal would break the rule, the nearest such move stays at its current "
            "level, or goes to Ian when it would reach a stage the flags or the bar hold.",
            "Fletchling keeps Will-O-Wisp at 25."):
        p(f"- {rule}")
    p("\n## What it changes\n")
    p(f"It changes the lists of {changed} of the {len(lists)} species. The "
      f"{len(run['unobtainable'])} that no source gives the player, by the League or after it "
      f"(Groudon, Xerneas and the like), keep their lists but for the drops: those lists only "
      f"feed trainers' default moves, which the trainer pass sets.\n")
    p("| Entries | Count |\n|---|---|")
    for k, label in (("same", "kept where they are"), ("moved", "moved"), ("added", "added"),
                     ("dropped", "dropped")):
        p(f"| {cap(label)} | {counts[k]} |")
    p("\nThe reasons given for the moves and additions (an entry moved twice, by Kaizo and then "
      "by the one-level rule, counts under both):\n")
    p("| Change | Reason | Count |\n|---|---|---|")
    for (change, why), n in sorted(moved_by.items(), key=lambda kv: -kv[1]):
        p(f"| {cap(change)} | {why} | {n} |")
    p("\nWhy entries left:\n")
    p("| Reason | Count |\n|---|---|")
    for why, n in dropped.most_common():
        p(f"| {cap(why.replace('leaves: ', ''))} | {n} |")
    flagged = [(s, f) for s, f in run["flags"].items() if f]
    flagged.sort(key=lambda x: (SPLITS.index(x[1][0]), x[0]))
    p("\n## The power flags\n")
    p(f"{len(flagged)} stages trip a flag before Byron's split. Each is held to no strong move "
      f"earlier than now on its own list; the last column is what the proposal does to its "
      f"strong moves, the earliest each can be known by any route, a pre-evolution kept back "
      f"included.\n")
    p("| Stage | Split | Look | Why | Strong moves, now and proposed |\n|---|---|---|---|---|")
    for s, (split, why) in flagged:
        a, b = routes(s, {x: run["now"][x] for x in g._chain(s)}), routes(s, {x: lists[x] for x in g._chain(s)})
        moved = [f"{name(c)} {a.get(c, 'never')} to {b.get(c, 'never')}" for c in sorted(set(a) | set(b), key=name)
                 if a.get(c) != b.get(c)]
        p(f"| {_sp(s)} | {split} | {severity(split)} | {why} | {'; '.join(moved) or 'as now'} |")
    barred = sorted(((s, r) for s, r in run["bar"].items() if r), key=lambda x: (SPLITS.index(x[1][0]), x[0]))
    p("\n## The power bar\n")
    p(f"{len(barred)} stages with no flag pass the bar before Byron's split on Oxide's lists "
      f"now, and are held the same way. The thresholds are provisional; Ian's Talonflame at "
      f"39 outsped 92 of Maylene's 93 trainer Pokemon and knocked out 38 in one hit, well "
      f"over both.\n")
    p("| Stage | Split | Outsped | Knocked out in one hit |\n|---|---|---|---|")
    for s, (split, (fast, ko)) in barred:
        p(f"| {_sp(s)} | {split} | {fast:.0%} | {ko:.0%} |")
    if run["forced"]:
        p(f"\nA further {len(run['forced'])} stages would trip a flag or pass the bar only with "
          f"the moves a first proposal gave them, so they are proposed again as held: "
          + ", ".join(_sp(s) for s in sorted(run["forced"])) + ".")
    p("\n## Strong moves that come sooner\n")
    p(f"Every good attack or S or SSS status move that the proposal gives a stage a split or "
      f"more sooner than now, or new before Byron's split: {len(sooner)} in all. These are the "
      f"entries to read as a player would. A stage marked held is flagged or over the bar, so "
      f"its entry here is a new move no earlier than its first good one of that type.\n")
    p("| Stage | Move | Now | Proposed | Held |\n|---|---|---|---|---|")
    for s, c, was, lv in sooner:
        held = "yes" if run["flags"].get(s) or run["bar"].get(s) else ""
        p(f"| {_sp(s)} | {name(c)} | {was if was is not None else 'not learnt'} | {lv} | {held} |")
    real = [d for d in run["delays"] if d[5] and d[7] and d[8]]
    p("\n## Delays\n")
    p(f"{len(real)} delays pass Ian's tests on the proposed lists (a strong move past the "
      f"evolution level, the evolved stage a split and five levels later or never, nothing "
      f"like it between). The wait is given in splits past the one the stage can evolve in.\n")
    p("| Pre-evolution | Evolves to | Move | Learnt at | Wait in splits | Evolved stage |\n"
      "|---|---|---|---|---|---|")
    for pre, evo, c, lv, fe, _t1, wait, _t3, _t4 in sorted(real, key=lambda d: (d[0], d[3])):
        p(f"| {_sp(pre)} | {_sp(evo)} | {name(c)} | {lv} | {wait if wait is not None else ''} | "
          f"{fe if fe else 'never'} |")
    p("\n## The three analyses\n")
    p("On Oxide's lists now and on the proposal, the same readings as the first generator's:\n")
    p("| Reading | Kaizo | Oxide now | The proposal |\n|---|---|---|---|")
    k, o, q = analyses["kaizo"], analyses["oxide"], analyses["proposal"]
    p(f"| Pre-evolutions that reward a wait of a split or less | {k['wait']} | {o['wait']} | {q['wait']} |")
    p(f"| Moves only a Pokemon kept from evolving gets | {k['never']} | {o['never']} | {q['never']} |")
    p(f"| Of those, strong | {k['never_strong']} | {o['never_strong']} | {q['never_strong']} |")
    p(f"| Wild slots that can end the encounter | | {o['ends']} | {q['ends']} |")
    p(f"| Wild slots that can knock themselves out | | {o['self_ko']} | {q['self_ko']} |")
    p(f"| Wild slots with a better version later | | {o['later']} | {q['later']} |")
    p(f"| Evolved catches with no good move by the split's cap | | {o['bare']} | {q['bare']} |")
    p("\nThe share of catches with a good move known at capture or learnt by level-up before "
      "the split's cap:\n")
    p("| Split | Oxide now | The proposal |\n|---|---|---|")
    for split in SPLITS:
        a, b = o["good"].get(split), q["good"].get(split)
        if a and b:
            p(f"| {split} | {a[1] / a[0]:.2f} | {b[1] / b[0]:.2f} |")
    p("\n## The checks\n")
    p("Every family's check list, totalled over all of them:\n")
    p("| Check | Failures |\n|---|---|")
    for label, bad in run["checks"].items():
        p(f"| {cap(label)} | {len(bad)} |")
    fails = [(label, bad) for label, bad in run["checks"].items() if bad]
    for label, bad in fails:
        p(f"\n{cap(label)}: " + "; ".join(
            f"{_sp(x[0])} {name(x[-1]) if x[-1] in M() else x[-1]}" for x in bad[:40]) + ".")
    kept = sorted(set(STAB_KEPT))
    if kept:
        p(f"\nThe own-type rule keeps {len(kept)} moves at their current level, where the proposal "
          f"would have left a stage more than one split without an attack of its own type of 50 "
          f"or more:\n")
        p("| Stage | Move | In the list of | Kept at |\n|---|---|---|---|")
        for s, c, holder, lv in kept:
            p(f"| {_sp(s)} | {name(c)} | {_sp(holder)} | {lv} |")
    asked = collections.defaultdict(set)
    for s, c, h, lv, r in STAB_FOR_IAN:
        asked[(h, c, lv, tuple(r))].add(s)
    if asked:
        p(f"\nFor Ian: {len(asked)} such moves would reach a stage the power flags or the bar hold, "
          f"so they are not kept until he rules; the stages they are for go without an attack of "
          f"their own type meanwhile:\n")
        p("| Move | In the list of | Its level now | For | Would reach |\n|---|---|---|---|---|")
        for (holder, c, lv, reached), stages in sorted(asked.items()):
            p(f"| {name(c)} | {_sp(holder)} | {lv} | {', '.join(_sp(x) for x in sorted(stages))} | "
              f"{', '.join(_sp(x) for x in reached)} |")
    already = sorted(s for s in lists if gap_applies(s) and breaks_gap(s, run["now"])
                     and not widens_gap(s, run["now"], lists))
    if already:
        p(f"\n{len(already)} stages go more than one split without an attack of their own type on "
          f"Oxide's lists now, and the proposal does not make it longer (stages the player can "
          f"evolve by the end of Gardenia's split are exempt); the later-moves proposal fills "
          f"them where a later game offers one: " + ", ".join(_sp(s) for s in already) + ".")
    past = sorted(set(PAST_CAP))
    if past:
        p(f"\nWhere Kaizo's own level is past Oxide's 78, the rule would take the move out of "
          f"play, against the rule that nothing goes past 78, so these {len(past)} keep their "
          f"translated place for Ian to decide:\n")
        p("| Stage | Move | Kaizo's level | Kept at |\n|---|---|---|---|")
        for s, c, kl, kept in past:
            p(f"| {_sp(s)} | {name(c)} | {kl} | {kept} |")
    if run["crowded"]:
        p(f"\n{len(run['crowded'])} moved entries found no free level in their split and share "
          f"one: " + "; ".join(f"{_sp(s)}'s {name(c)} at {lv}" for s, c, lv in run["crowded"]) + ".")
    _write_rulings(p)


def _write_rulings(p):
    """The report's sections for Ian's rulings of 2026-09-28."""
    placed = [x for x in CARRIED if x[3] is not None]
    stages = sorted({x[0] for x in placed})
    p("\n## After an evolution without a level\n")
    p(f"Ian's ruling (2026-09-28): a stage reached by a stone, a held item, a known move, a place, a "
      f"partner or Beauty gets its own sparser list after the evolution: its key moves, fewer than "
      f"the pre-evolution learns after that point, so evolving early still costs moves. "
      f"{len(placed)} key moves go to {len(stages)} stages; {len(CARRIED) - len(placed)} candidates "
      f"a rule kept out.\n")
    if placed:
        p("| Stage | Move | Level | From the source's |\n|---|---|---|---|")
        for s, c, lv, at, _why in sorted(placed):
            p(f"| {_sp(s)} | {name(c)} | {at} | {lv} |")
    if EVOLUTION_MOVES:
        p("\n## Evolution moves, for Ian\n")
        p("A level-0 entry is taught the moment the Pokemon evolves, never known by a wild, gift "
          "or trainer Pokemon, and offered by the relearner (the engine support follows). Used "
          "sparingly, each listed here for Ian:\n")
        p("| Stage | Move | Why |\n|---|---|---|")
        for s, c, why in sorted(EVOLUTION_MOVES):
            p(f"| {_sp(s)} | {name(c)} | {why} |")
    p("\n## A move in the last splits\n")
    by_src = collections.Counter(src.split(" at ")[0].split(" ")[0] if src.startswith("Kaizo") else
                                 ("the later games" if " at " in src else src) for _s, _c, _lv, src in LATE_ADDED)
    p(f"Ian's ruling (2026-09-28): every final stage the player can own learns at least one real "
      f"move by level-up in the Galactic split or later (61 to 78). {len(LATE_ADDED)} stages had "
      f"none and get one; the source of each: "
      + ", ".join(f"{k} {n}" for k, n in by_src.most_common()) + ".\n")
    if LATE_ADDED:
        p("| Stage | Move | Level | From |\n|---|---|---|---|")
        for s, c, lv, src in sorted(LATE_ADDED):
            p(f"| {_sp(s)} | {name(c)} | {lv} | {src} |")
    if LATE_FOR_IAN:
        p(f"\nFor Ian, with nothing that qualifies: " + ", ".join(_sp(s) for s in sorted(LATE_FOR_IAN)) + ".")
    if RULED_PLACED:
        p("\n## By name, for Ian\n")
        p("Lists Ian asked for by name, placed past the flags' first-of-type test (ruling 19: a proper "
          "list for Alolan Ninetales, for the wild catch and the Ice Stone route alike): "
          + "; ".join(f"{_sp(s)}'s {name(c)} at {lv}" for s, c, lv in RULED_PLACED) + ".")
    p("\n## What the Overseer's read changed\n")
    kept = [x for x in DEAD_MOVED if x[3] != "dropped"]
    dropped = [x for x in DEAD_MOVED if x[3] == "dropped"]
    p("The Overseer read the first version of these rulings as a player (2026-09-28). A late move now "
      "has to give the stage something it lacks by then: a stronger attack of its type in its better "
      "category, one twenty points more accurate that keeps three quarters of the power, a new type, "
      "or a status move rated A or better. An attack in the weaker category across a gap of 20 in the "
      "attacking stats, a charging or out-of-reach move (unless nothing else adds), a self-knockout, "
      "partner, evasion or Protect move never counts. The late levels spread from 61 to 78 by the "
      "stage's base stat total, the weakest earliest. A moved entry that would come after a stronger "
      f"move of its type and category goes back to its current level ({len(kept)}) or leaves "
      f"({len(dropped)}): " + "; ".join(f"{_sp(s)}'s {name(c)} ({act}, not {lv})" for s, c, lv, act in DEAD_MOVED[:30])
      + ". Repeated entries leave every list, except what a first stage knows when first had. Evasion "
      "and Protect are never a key or late pick, so Clefable's Minimize at 19 is gone.")


def main(argv=None):
    from . import learnplan as mod
    ap = argparse.ArgumentParser()
    ap.add_argument("what", choices=["sample", "line", "flags", "full"])
    ap.add_argument("species", nargs="*")
    args = ap.parse_args(argv)
    if args.what == "full":
        mod.full_report()
    elif args.what == "flags":
        mod.flags_report()
    elif args.what == "line":
        for n in args.species:
            mod.line_report(n.upper() if n.upper().startswith("SPECIES_") else "SPECIES_" + n.upper())
    else:
        mod.sample_report()
    return 0


# Ian's six (Houndour, Fletchinder, Talonflame, Rattata, Ralts, Whismur), then
# two lines the before-Maylene flag brings to him by name (Abra's Kadabra from
# Roark's split, Turtwig's Torterra from Fantina's), an exclusive delay carried
# from Kaizo (Gulpin's Sludge Bomb), and a line Kaizo lacks (Scorbunny).
SAMPLE = ["SPECIES_HOUNDOUR", "SPECIES_FLETCHLING", "SPECIES_RATTATA", "SPECIES_RALTS",
          "SPECIES_WHISMUR", "SPECIES_ABRA", "SPECIES_TURTWIG", "SPECIES_GULPIN",
          "SPECIES_SCORBUNNY"]


def translation_table():
    """[(Kaizo split, its levels, Oxide levels)] under the split translation."""
    rows, lo = [], 1
    for (k0, o0), (k1, o1) in zip(g.LEVEL_MAP, g.LEVEL_MAP[1:]):
        split = next(n for n, c in ls.splits("kaizo") if c == k1)
        rows.append((split, f"{k0 + 1} to {k1}", f"{translate(k0 + 1)} to {o1}"))
    return rows


def sample_report(out=sys.stdout):
    print("# The learnset method's sample\n", file=out)
    print("Written by `learnplan.py sample` (the learnset generator's second design, 2026-09-27) "
          "for the Overseer to read before Ian. It proposes; nothing here is in the game data. "
          "Each line gives its lists now and proposed, what moved and why, the Kaizo entries "
          "that do not count, the four a wild catch knows, its delays under Ian's tests, and "
          "the check list.\n", file=out)
    print("Kaizo's levels, translated by split (a Kaizo level carried to the same point of the "
          "same split in Oxide):\n", file=out)
    print("| Kaizo split | Kaizo levels | Oxide levels |\n|---|---|---|", file=out)
    for split, k, o in translation_table():
        print(f"| {split} | {k} | {o} |", file=out)
    hd = kaizo_evidence("SPECIES_HOUNDOOM")["MOVE_TOXIC"]
    ex = (kaizo_evidence("SPECIES_EXPLOUD") or {}).get("MOVE_EARTHQUAKE")
    print(f"\nKaizo's League split runs to 100 (all five League fights are at 100 in its "
          f"data), so no Kaizo placement lands past it, and none lands past Oxide's 78. "
          f"Ian's Stone Edge at 87 translates to {translate(87)}, inside Oxide's League "
          f"split. A level above 78 stays in a list only where Oxide's own list has it.", file=out)
    side = "" if not ex else (
        f" The reading has a side effect to see: Kaizo's Exploud (reached at "
        f"{g.reached('kaizo', 'SPECIES_EXPLOUD')} in Kaizo) learns Earthquake at {ex[0]}, which "
        f"translates to {ex[1]}, below Oxide's evolution level of {reach('SPECIES_EXPLOUD')}, so "
        f"Exploud does not get it. The translation compresses Kaizo's levels while Oxide's "
        f"evolution levels stay as they are.")
    print(f"\nUnreachable after translation: Kaizo's Houndoom has Toxic at {hd[0]}, which "
          f"translates to {hd[1]}; Houndoom comes at {reach('SPECIES_HOUNDOOM')}, so it stays "
          f"unavailable.{side}", file=out)
    print("\nReadings to confirm: the power flags leave out moves that knock the user out "
          "(Explosion) and moves whose damage needs a condition (Focus Punch, Dream Eater, "
          "Future Sight), as the scores do. Dark Void reads as A, beside Yawn, for its "
          "Generation 4 accuracy. Test 2 of a delay is reported as the wait's length, not "
          "applied, since Ian ruled a wait longer than a split worth it; test 3 also asks for "
          "at least five levels. A line any stage of which is flagged before Byron's split "
          "counts as marked: its good moves and S or SSS status moves come no earlier than "
          "now, and it takes no new coverage; a flagged stage itself takes a new attack only "
          "no earlier than its first good one of that type now. Kaizo's evidence counts only "
          "where its move matches Oxide's, which rules out Kaizo's buffed moves (Crunch and "
          "Hyper Fang at 95, Double-Edge at 140, Poison Fang at 90) wherever they appear.",
          file=out)
    print("\nFor Ian, from what the sample shows:\n", file=out)
    print("1. A flagged stage can still gain a good move early through a pre-evolution kept "
          "back: Houndoom's Dark Pulse from 43 through Houndour, Torterra's Leaf Blade from "
          "32 through Turtwig, Gardevoir's and Gallade's Zen Headbutt from 30 through Kirlia "
          "(each flagged stage's \"by any route\" line). That is what makes these delays real "
          "choices, and it also brings the strong stage its tool sooner. Should a flagged "
          "stage's route through a pre-evolution also be held to no earlier than now? That "
          "would remove most delays on marked lines.", file=out)
    print("2. The power bar's two thresholds (Ian's Talonflame test) are still to set; until "
          "then the flags alone mark a line.", file=out)
    print("3. The readings above: conditional and self-KO moves left out of the flags, Dark "
          "Void at A, test 2 reported rather than applied, and five levels in test 3.",
          file=out)
    for n in SAMPLE:
        line_report(n, out=out)

if __name__ == "__main__":
    sys.exit(main())

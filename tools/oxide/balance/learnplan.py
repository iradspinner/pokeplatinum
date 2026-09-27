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
    """The level the player can first have the stage at in Oxide: an evolved
    stage's evolution level (or a lower catch), a first stage's lowest
    catch, gift or hatch level, 1 for a first stage nothing gives. A
    placement below it is learnt by nobody, so it means unavailable in play
    (Ian, 2026-09-27), not early: Kaizo's legendaries' low entries and a
    level 2 Iron Head for a Togedemaru first met at 20 both stay out."""
    evo = max(1, g.reached("oxide", species)) if species in g.oxide_reached() else None
    found = [x for x in (evo, catch_level(species)) if x is not None]
    return min(found) if found else 1


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
    m = M()[const]
    kind, p = strength(const)
    types = {t.title() for t in (pokedex.load(data.ROOT, species) or {}).get("types", [])}
    stab = m["type"].title() in types
    levels = []
    for ks in nearest_kaizo(species):
        ev = kaizo_evidence(ks) or {}
        ktypes = {t.title() for t in (pokedex.load(data.ROOT, ks) or {}).get("types", [])}
        best = None
        for c, (_kl, t, why) in ev.items():
            if why:
                continue
            if kind != "damage":
                ok = c == const
            else:
                kk, kp = strength(c)
                ok = (kk == "damage" and M()[c]["class"] == m["class"]
                      and (M()[c]["type"].title() in ktypes) == stab
                      and abs(kp - p) <= LIKE * max(kp, p))
            if ok and (best is None or t < best):
                best = t
        if best is not None:
            levels.append(best)
    return round(statistics.median(levels)) if levels else None


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
    strong_later = [(e, reach(e) + WAIT - 1) for e in later_stages(species) if strong_stage(e)]
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
        why = g._dropped(c, species, first_level[c], types)
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
            t, src = None, None
            if ev is not None and c in ev and ev[c][2] is None:
                t, src = ev[c][1], f"Kaizo's {species[8:].title()} at {ev[c][0]}"
            elif ev is None:
                t = analogue_level(species, c)
                src = "its nearest Kaizo lines" if t else None
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
                if target != lv:
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
        drop = g._dropped(c, species, t, types)
        if drop:
            continue
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
        hi = was.get(c, 78) if strength(c)[0] == "damage" and not good_attack(c, types) and c in was else 78
        split = _split_of(lv)
        step = [d for k in range(1, 12) for d in ((k, -k) if strong else (-k, k))]
        new = next((lv + d for d in step if lo <= lv + d <= min(hi, 78) and taken[lv + d] == 0
                    and _split_of(lv + d) == split), None)
        if new is None:
            crowded.append((c, lv))
            result.append((lv, c))
            continue
        taken[lv] -= 1
        taken[new] += 1
        result.append((new, c))
        notes.append((c, f"{lv} to {new}: the same-level rule (another move is at {lv})"))
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
    at = g.reached("oxide", evo)
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
    for stage in g._chain(species):
        own = stage == species
        start = reach(stage) if stage in g.oxide_reached() else 1
        for lv, c in lists.get(stage, []):
            if c not in M() or lv < start or (lv <= 1 and stage in g.oxide_reached()):
                continue
            if not (good_attack(c, types) or (rank(c) or 0) >= STRONG_RANK):
                continue
            if own and lv < here:
                continue
            if not own and lv > here + WAIT - 1:
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
                  f"{split}'s split): knows {', '.join(name(c) for c in calc_trainers.default_moves(lists_now[s], lv))} "
                  f"now; {', '.join(name(c) for c in calc_trainers.default_moves(lists_new[s], lv))} proposed.",
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
                if bad and (s, c) not in earlier_strong:
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
    ends = g._ends()
    wild_end = [(s, c) for s in fam for lv, c in new[s]
                if ls.metrics._compact(name(c)) in ends and 1 < lv <= g.wild_top(s)
                and (lv, c) not in now[s]]
    res.append(("no move that ends a wild encounter moved into the wild levels", wild_end))
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
    for key, label in (("leaves:", None), ("same-level rule", "the one-level rule"),
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
    if run["crowded"]:
        p(f"\n{len(run['crowded'])} moved entries found no free level in their split and share "
          f"one: " + "; ".join(f"{_sp(s)}'s {name(c)} at {lv}" for s, c, lv in run["crowded"]) + ".")


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

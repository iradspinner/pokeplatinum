"""The defensive index of a typing: a r/stunfisk post's formula, read on
Oxide's own type chart and engine, and reweighted by what is used in Oxide
(Ian, 2026-11-03; docs/oxide/defensive-index.md).

    PYTHONPATH=. python3 -m tools.oxide.balance.defensive_index          # print the tables
    PYTHONPATH=. python3 -m tools.oxide.balance.defensive_index --write  # and write the doc's data

The post's formula, for one defending typing:

    2 x (UC immunities) + 3 x (CC immunities) + (UC resistances)
    + 1.5 x (CC resistances) - (UC weaknesses) - 2 x (CC weaknesses)
    + 0.5 x (status or move group immunities) - 0.5 x (Stealth Rock weakness)
    + 0.5 x (Web or Spikes immunity, or Stealth Rock resistance)

CC, the common coverage types, are Fire, Ice, Rock, Ground, Fighting, Dark
and Bug; the rest are UC. Every count in it comes from one weakness weight
w per attacking type (1 for UC, 2 for CC): a resistance is worth (1 + w) / 2
and an immunity 1 + w, which gives the post's 1, 1.5, 2 and 3 exactly. The
Oxide versions keep that relation and set w from use: w = 25 x the type's
share of the attacks counted, so the 18 weights still sum to the post's 25.

It is a defensive measure only. It says nothing of offence, Speed, stats or
a line's moves.
"""
import argparse
import collections
import functools
import json
import math
import os
import re

from . import data, gauntlet, pool, splits
from ..encounters import evolve, model, pokedex, scripted, simulate

ROOT = data.ROOT
TYPES = ["NORMAL", "FIRE", "WATER", "ELECTRIC", "GRASS", "ICE", "FIGHTING", "POISON", "GROUND",
         "FLYING", "PSYCHIC", "BUG", "ROCK", "GHOST", "DRAGON", "DARK", "STEEL", "FAIRY"]
POST_CC = {"FIRE", "ICE", "ROCK", "GROUND", "FIGHTING", "DARK", "BUG"}
# The post's own single-type ranking, as Ian pasted it.
POST_RANKING = {"STEEL": 8.5, "FAIRY": 4.5, "GHOST": 4.5, "POISON": 3.5, "WATER": 3, "FIRE": 2.5,
                "FLYING": 2, "FIGHTING": 2, "ELECTRIC": 1.5, "GROUND": 1, "DRAGON": 0.5, "DARK": 0,
                "NORMAL": 0, "BUG": -1.5, "GRASS": -2, "PSYCHIC": -2.5, "ROCK": -2.5, "ICE": -5.5}
POST_WEAK_SUM = 2 * len(POST_CC) + (len(TYPES) - len(POST_CC))   # 25

# The later games' chart (Generation 6 on), which the post was written for:
# attacking type -> (super effective on, not very effective on, no effect on).
LATER_CHART_ROWS = {
    "NORMAL": ((), ("ROCK", "STEEL"), ("GHOST",)),
    "FIRE": (("GRASS", "ICE", "BUG", "STEEL"), ("FIRE", "WATER", "ROCK", "DRAGON"), ()),
    "WATER": (("FIRE", "GROUND", "ROCK"), ("WATER", "GRASS", "DRAGON"), ()),
    "ELECTRIC": (("WATER", "FLYING"), ("ELECTRIC", "GRASS", "DRAGON"), ("GROUND",)),
    "GRASS": (("WATER", "GROUND", "ROCK"),
              ("FIRE", "GRASS", "POISON", "FLYING", "BUG", "DRAGON", "STEEL"), ()),
    "ICE": (("GRASS", "GROUND", "FLYING", "DRAGON"), ("FIRE", "WATER", "ICE", "STEEL"), ()),
    "FIGHTING": (("NORMAL", "ICE", "ROCK", "DARK", "STEEL"),
                 ("POISON", "FLYING", "PSYCHIC", "BUG", "FAIRY"), ("GHOST",)),
    "POISON": (("GRASS", "FAIRY"), ("POISON", "GROUND", "ROCK", "GHOST"), ("STEEL",)),
    "GROUND": (("FIRE", "ELECTRIC", "POISON", "ROCK", "STEEL"), ("GRASS", "BUG"), ("FLYING",)),
    "FLYING": (("GRASS", "FIGHTING", "BUG"), ("ELECTRIC", "ROCK", "STEEL"), ()),
    "PSYCHIC": (("FIGHTING", "POISON"), ("PSYCHIC", "STEEL"), ("DARK",)),
    "BUG": (("GRASS", "PSYCHIC", "DARK"),
            ("FIRE", "FIGHTING", "POISON", "FLYING", "GHOST", "STEEL", "FAIRY"), ()),
    "ROCK": (("FIRE", "ICE", "FLYING", "BUG"), ("FIGHTING", "GROUND", "STEEL"), ()),
    "GHOST": (("PSYCHIC", "GHOST"), ("DARK",), ("NORMAL",)),
    "DRAGON": (("DRAGON",), ("STEEL",), ("FAIRY",)),
    "DARK": (("PSYCHIC", "GHOST"), ("FIGHTING", "DARK", "FAIRY"), ()),
    "STEEL": (("ICE", "ROCK", "FAIRY"), ("FIRE", "WATER", "ELECTRIC", "STEEL"), ()),
    "FAIRY": (("FIGHTING", "DRAGON", "DARK"), ("FIRE", "POISON", "STEEL"), ()),
}


def later_chart():
    """{(attacking, defending): multiplier} for the later games, entries off 1x only."""
    out = {}
    for atk, (se, nve, none) in LATER_CHART_ROWS.items():
        out.update({(atk, d): 2.0 for d in se})
        out.update({(atk, d): 0.5 for d in nve})
        out.update({(atk, d): 0.0 for d in none})
    return out


def oxide_chart():
    return pokedex.type_chart(ROOT)


def chart_differences():
    """[(attacking, defending, Oxide's multiplier, the later games')] where they differ."""
    ox, lt = oxide_chart(), later_chart()
    keys = sorted(set(ox) | set(lt), key=lambda k: (TYPES.index(k[0]), TYPES.index(k[1])))
    return [(a, d, ox.get((a, d), 1.0), lt.get((a, d), 1.0)) for a, d in keys
            if ox.get((a, d), 1.0) != lt.get((a, d), 1.0)]


# -- what Oxide's engine gives each type and ability ---------------------------

# The status and move-group immunities, by type, each with where the engine
# says so. The post counts each group at 0.5.
TYPE_GROUPS = {
    "burn": {"FIRE"},                    # subscript_burn.s, the TYPE_FIRE checks
    "poison": {"POISON", "STEEL"},       # subscript_poison.s and subscript_badly_poison.s
    "paralysis": {"ELECTRIC"},           # subscript_paralyze.s, "Electric types cannot be paralysed"
    "freeze": {"ICE"},                   # subscript_freeze.s
    "powder": {"GRASS"},                 # battle_controller_player.c, Move_IsPowder on a Grass type
    "leech_seed": {"GRASS"},             # subscript_leech_seed_start.s
    "prankster": {"DARK"},               # battle_controller_player.c, subscript_prankster_dark_immunity
    "trap": {"GHOST"},                   # battle_lib.c, "a Ghost type cannot be trapped by anything"
    "sand": {"ROCK", "GROUND", "STEEL"},  # battle_script.c, the weather damage command
    "hail": {"ICE"},                     # the same command
}
# The groups the post's own numbers count: its single-type ranking is
# reproduced with these and not with sand, hail, trapping or Toxic Spikes
# (Rock, Ground and Steel would each be half a point higher with sand).
POST_GROUPS = ("burn", "poison", "paralysis", "freeze", "powder", "leech_seed", "prankster")
STATUS_GROUPS = ("burn", "poison", "paralysis", "freeze", "powder", "leech_seed")
# Situational terms: they matter only when the other side brings the thing,
# so the Oxide views scale them by how often it does.
SITUATIONAL = ("stealth_rock", "spikes_web", "toxic_spikes", "prankster", "trap", "sand", "hail")

# Abilities that change a matchup in Oxide's engine, with the code that does it.
IMMUNE_ABILITY = {
    "LEVITATE": "GROUND",                # battle_lib.c, MOVE_STATUS_LEVITATED
    "FLASH_FIRE": "FIRE",                # BattleSystem_TriggerImmunityAbility
    "WATER_ABSORB": "WATER", "STORM_DRAIN": "WATER", "DRY_SKIN": "WATER",
    "VOLT_ABSORB": "ELECTRIC", "MOTOR_DRIVE": "ELECTRIC", "LIGHTNING_ROD": "ELECTRIC",
    "SAP_SIPPER": "GRASS",
}
SCALE_ABILITY = {                         # the damage formula's power and damage changes
    "THICK_FAT": {"FIRE": 0.5, "ICE": 0.5},
    "HEATPROOF": {"FIRE": 0.5},
    "WATER_BUBBLE": {"FIRE": 0.5},
    "PURIFYING_SALT": {"GHOST": 0.5},
    "DRY_SKIN": {"FIRE": 1.25},
    "FLUFFY": {"FIRE": 2.0},
}
FILTERS = {"FILTER", "SOLID_ROCK"}       # super-effective damage x0.75
ABILITY_GROUPS = {                        # the status subscripts' ability checks
    "LIMBER": {"paralysis"},
    "WATER_VEIL": {"burn"}, "WATER_BUBBLE": {"burn"},
    "IMMUNITY": {"poison"}, "PASTEL_VEIL": {"poison"},
    "MAGMA_ARMOR": {"freeze"},
    "PURIFYING_SALT": {"burn", "poison", "paralysis", "freeze"},
    "OVERCOAT": {"powder", "sand", "hail"},
    "SAND_VEIL": {"sand"}, "SAND_RUSH": {"sand"}, "SAND_FORCE": {"sand"},
    "SNOW_CLOAK": {"hail"}, "ICE_BODY": {"hail"},
    "MAGIC_GUARD": {"sand", "hail"},
}
MATCHUP_ABILITIES = (set(IMMUNE_ABILITY) | set(SCALE_ABILITY) | FILTERS | set(ABILITY_GROUPS)
                     | {"WONDER_GUARD"})


def multiplier(chart, attacking, types, ability=None):
    """What one attacking type does to a typing, the ability included."""
    m = pokedex.effectiveness(chart, attacking, types)
    if ability == "WONDER_GUARD" and m <= 1:
        return 0.0
    if IMMUNE_ABILITY.get(ability) == attacking:
        return 0.0
    m *= SCALE_ABILITY.get(ability, {}).get(attacking, 1.0)
    if ability in FILTERS and m > 1:
        m *= 0.75
    return m


def resist_credit(m):
    """How many resistances a multiplier under 1 counts as: one for a half,
    and half again for each further halving (a quarter counts 1.5)."""
    steps = -math.log2(m)
    return min(steps, 1.0) + 0.5 * max(steps - 1.0, 0.0)


def groups(types, ability=None):
    """The status and move-group immunities a typing has, the ability included."""
    out = {g for g, ts in TYPE_GROUPS.items() if set(types) & ts}
    out |= ABILITY_GROUPS.get(ability, set())
    return out


def grounded(types, ability=None):
    return "FLYING" not in types and ability != "LEVITATE"


# -- the index ------------------------------------------------------------------

def index(types, chart, w, status=0.5, situ=None, count=POST_GROUPS, ability=None, parts=False):
    """The index of one typing. `w` is the weakness weight of each attacking
    type, `status` the weight of each status group, `situ` the weight of each
    situational term (the post's 0.5 when not given), and `count` the groups
    counted at all."""
    situ = situ if situ is not None else {k: 0.5 for k in SITUATIONAL}
    types = list(dict.fromkeys(types))
    matchup = 0.0
    for atk in TYPES:
        m = multiplier(chart, atk, types, ability)
        if m == 0:
            matchup += 1 + w[atk]
        elif m < 1:
            matchup += (1 + w[atk]) / 2 * resist_credit(m)
        elif m > 1:
            matchup -= w[atk] * math.log2(m)
    have = groups(types, ability) & set(count)
    st = sum(status for g in have if g in STATUS_GROUPS)
    sit = sum(situ.get(g, 0.5) for g in have if g not in STATUS_GROUPS)
    # Stealth Rock: half a point for each step of weakness or resistance;
    # Magic Guard takes no damage from it, which counts as a resistance.
    rock = multiplier(chart, "ROCK", types)
    if ability == "MAGIC_GUARD":
        sit += situ["stealth_rock"]
    elif rock > 1:
        sit -= situ["stealth_rock"] * math.log2(rock)
    elif rock < 1:
        sit += situ["stealth_rock"] * resist_credit(rock)
    if not grounded(types, ability) or ability == "MAGIC_GUARD":
        sit += situ["spikes_web"]
    # Toxic Spikes, which the post does not count: a Poison or Steel type, or
    # one off the ground, is not poisoned by them (a grounded Poison type
    # takes them away: battle_script.c, BtlCmd_CheckToxicSpikes).
    if "toxic_spikes" in count and (not grounded(types, ability) or "poison" in groups(types, ability)):
        sit += situ["toxic_spikes"]
    total = matchup + st + sit
    return (total, matchup, st, sit) if parts else total


def post_weights():
    return {t: (2.0 if t in POST_CC else 1.0) for t in TYPES}


def weights_from_shares(shares):
    """The weakness weights from usage shares: 25 x share, so the weights
    sum to the post's 25 and a type used at the average rate weighs 1.39."""
    total = sum(shares.values()) or 1.0
    return {t: POST_WEAK_SUM * shares.get(t, 0.0) / total for t in TYPES}


# -- what trainers attack with ---------------------------------------------------

BOSS, MINI, ORDINARY = "boss", "mini-boss", "ordinary"
KIND_WEIGHT = {BOSS: 3.0, MINI: 2.0, ORDINARY: 1.0}
# The fights.json keys whose trainers are named Galactic officers, which are
# mini-bosses (Ian, 2026-10-31); every other fights.json entry is a boss
# (rivals, commanders, Cyrus, leaders, Frontier Brains, the League).
OFFICER_FIGHTS = {"phobos_deimos_1", "phobos_deimos_3", "pal_park_double", "tyche_hermes_1",
                  "tyche_hermes_2", "hesperid_1", "hesperid_hq", "argo_1", "argo_hq",
                  "somnu_moira", "boreas_laverna_2"}
ACE_CLASSES = {"TRAINER_CLASS_ACE_TRAINER_MALE", "TRAINER_CLASS_ACE_TRAINER_FEMALE",
               "TRAINER_CLASS_ACE_TRAINER_SNOW_MALE", "TRAINER_CLASS_ACE_TRAINER_SNOW_FEMALE"}
HAZARD_MOVES = {"stealth_rock": {"MOVE_STEALTH_ROCK"}, "spikes": {"MOVE_SPIKES"},
                "toxic_spikes": {"MOVE_TOXIC_SPIKES"}, "sticky_web": {"MOVE_STICKY_WEB"}}
TRAP_MOVES = {"MOVE_MEAN_LOOK", "MOVE_BLOCK", "MOVE_SPIDER_WEB", "MOVE_WRAP", "MOVE_BIND",
              "MOVE_FIRE_SPIN", "MOVE_WHIRLPOOL", "MOVE_SAND_TOMB", "MOVE_CLAMP", "MOVE_MAGMA_STORM",
              "MOVE_INFESTATION", "MOVE_SNAP_TRAP", "MOVE_THUNDER_CAGE", "MOVE_ANCHOR_SHOT",
              "MOVE_SPIRIT_SHACKLE", "MOVE_JAW_LOCK", "MOVE_OCTOLOCK", "MOVE_FAIRY_LOCK"}
TRAP_ABILITIES = {"Shadow Tag", "Arena Trap"}
SAND_SET = ({"MOVE_SANDSTORM"}, {"Sand Stream", "Sand Spit"})
HAIL_SET = ({"MOVE_HAIL", "MOVE_SNOWSCAPE"}, {"Snow Warning"})
# Moves that keep their type under Pixilate (battle_lib.c, sMovesKeepTheirType).
KEEP_TYPE = {"MOVE_HIDDEN_POWER", "MOVE_WEATHER_BALL", "MOVE_NATURAL_GIFT", "MOVE_JUDGMENT",
             "MOVE_TECHNO_BLAST", "MOVE_MULTI_ATTACK", "MOVE_TERRAIN_PULSE", "MOVE_STRUGGLE"}
PLATES = {"Flame": "FIRE", "Splash": "WATER", "Zap": "ELECTRIC", "Meadow": "GRASS", "Icicle": "ICE",
          "Fist": "FIGHTING", "Toxic": "POISON", "Earth": "GROUND", "Sky": "FLYING", "Mind": "PSYCHIC",
          "Insect": "BUG", "Stone": "ROCK", "Spooky": "GHOST", "Draco": "DRAGON", "Dread": "DARK",
          "Iron": "STEEL", "Pixie": "FAIRY"}
SPLIT_ORDER = pool.SPLITS
PHASES = {"early": SPLIT_ORDER[0:4], "middle": SPLIT_ORDER[4:8], "late": SPLIT_ORDER[8:12]}


@functools.lru_cache(maxsize=None)
def sound_moves():
    """The sound moves Liquid Voice turns Water, read from battle_lib.c."""
    with open(os.path.join(ROOT, "src", "battle", "battle_lib.c"), encoding="utf-8") as f:
        src = f.read()
    start = src.index("static u16 sSoundMoves[] = {")
    return set(re.findall(r"MOVE_\w+", src[start:src.index("};", start)]))


def hidden_power_type(ivs):
    """Hidden Power's type from the IVs, as Move_CalcVariableType works it out."""
    bits = [ivs["hp"], ivs["at"], ivs["df"], ivs["sp"], ivs["sa"], ivs["sd"]]
    n = sum((v & 1) << i for i, v in enumerate(bits))
    order = ["FIGHTING", "FLYING", "POISON", "GROUND", "ROCK", "BUG", "GHOST", "STEEL",
             "FIRE", "WATER", "GRASS", "ELECTRIC", "PSYCHIC", "ICE", "DRAGON", "DARK"]
    return order[n * 15 // 63]


def move_type(move, rec, mon):
    """The type the engine gives one trainer Pokemon's move."""
    t = rec["type"]
    ability = (mon.get("ability") or "").replace(" ", "_").upper()
    if move == "MOVE_HIDDEN_POWER" and mon.get("ivs"):
        return hidden_power_type(mon["ivs"])
    if move == "MOVE_JUDGMENT":
        item = mon.get("item") or ""
        return next((ty for p, ty in PLATES.items() if item == f"{p} Plate"), "NORMAL")
    if ability == "NORMALIZE" and move != "MOVE_STRUGGLE":
        return "NORMAL"
    if ability == "PIXILATE" and t == "NORMAL" and move not in KEEP_TYPE:
        return "FAIRY"
    if ability == "LIQUID_VOICE" and move in sound_moves():
        return "WATER"
    return t


def _raw_party(stem):
    with open(os.path.join(ROOT, "res", "trainers", "data", stem + ".json"), encoding="utf-8") as f:
        return json.load(f)


@functools.lru_cache(maxsize=None)
def trainer_roster():
    """[{tr_id, stem, split, kind, weight, mons: [(species, moves, built mon)]}]
    for every trainer the player fights in the twelve splits. A rival fight's
    teams (one per starter, and Lucas or Dawn) share the fight's weight, so
    each fight counts once. Partners in a tag fight are left out."""
    ox = data.oxide_trainers()
    spec = data.fights()
    by_id, partners = {}, set()
    for f in spec["fights"]:
        kind = MINI if f["key"] in OFFICER_FIGHTS else BOSS
        share = len(f["tr_ids"]) if f["key"].startswith(("barry_", "lucas_dawn_")) else 1
        for tr in f["tr_ids"]:
            by_id[tr] = (f["split"], kind, KIND_WEIGHT[kind] / share)
        partners |= set(f.get("partner_ids") or [])
    sections = set()
    for area, secs in gauntlet.SECTIONS.items():
        for sec in secs:
            sections |= set(gauntlet.section_trainers(area, sec))
    out = []
    for tr, t in ox.items():
        if tr in partners:
            continue
        raw = _raw_party(t["stem"])
        if tr in by_id:
            split, kind, weight = by_id[tr]
        else:
            split = splits.trainer_split(tr)
            kind = MINI if raw.get("class") in ACE_CLASSES or tr in sections else ORDINARY
            weight = KIND_WEIGHT[kind]
        if split not in SPLIT_ORDER:
            continue
        mons = []
        for i, m in enumerate(raw["party"]):
            built = next((b for b in t["party"] if b.get("sub_index") == i), None) or {}
            moves = [mv for mv in m.get("moves") or [] if mv and mv != "MOVE_NONE"]
            mons.append((m["species"], moves, built))
        out.append({"tr_id": tr, "stem": t["stem"], "name": t["name"], "split": split, "kind": kind,
                    "weight": weight, "mons": mons})
    return out


def damaging(rec):
    return rec and rec["class"] in ("PHYSICAL", "SPECIAL") and rec["move"] != "MOVE_STRUGGLE"


@functools.lru_cache(maxsize=None)
def trainer_attacks():
    """{split: {type: kind-weighted count of damaging moves}}, and the counts by kind."""
    moves = pokedex.moves(ROOT)
    by_split = {s: collections.Counter() for s in SPLIT_ORDER}
    by_kind = {k: collections.Counter() for k in KIND_WEIGHT}
    changed = collections.Counter()
    for t in trainer_roster():
        for _sp, mvs, built in t["mons"]:
            for mv in mvs:
                rec = moves.get(mv)
                if not damaging(rec):
                    continue
                ty = move_type(mv, rec, built)
                if ty != rec["type"]:
                    changed[(mv, ty)] += 1
                by_split[t["split"]][ty] += t["weight"]
                by_kind[t["kind"]][ty] += 1
    return by_split, by_kind, changed


@functools.lru_cache(maxsize=None)
def trainer_situations():
    """{split: {term: kind-weighted share of the split's teams that bring it}}."""
    out = {}
    weather = {}
    for t in trainer_roster():
        weather[t["tr_id"]] = splits.trainer_weather(t["tr_id"])
    for split in SPLIT_ORDER:
        teams = [t for t in trainer_roster() if t["split"] == split]
        total = sum(t["weight"] for t in teams) or 1.0
        have = collections.Counter()
        for t in teams:
            mvs = {mv for _sp, ms, _b in t["mons"] for mv in ms}
            abil = {b.get("ability") for _sp, _ms, b in t["mons"]}
            flags = set()
            for k, ms in HAZARD_MOVES.items():
                if mvs & ms:
                    flags.add(k)
            if flags & {"spikes", "sticky_web"}:
                flags.add("spikes_web")
            if mvs & TRAP_MOVES or abil & TRAP_ABILITIES:
                flags.add("trap")
            if "Prankster" in abil:
                flags.add("prankster")
            if mvs & SAND_SET[0] or abil & SAND_SET[1] or "Sand" in weather[t["tr_id"]]:
                flags.add("sand")
            if mvs & HAIL_SET[0] or abil & HAIL_SET[1] or "Hail" in weather[t["tr_id"]]:
                flags.add("hail")
            for k in flags:
                have[k] += t["weight"]
        out[split] = {k: have[k] / total for k in
                      ("stealth_rock", "spikes", "toxic_spikes", "sticky_web", "spikes_web", "trap",
                       "prankster", "sand", "hail")}
        out[split]["teams"] = len(teams)
        out[split]["count"] = {k: sum(1 for t in teams if k in _flags_of(t, weather)) for k in
                               ("stealth_rock", "spikes", "toxic_spikes", "sticky_web")}
    return out


def _flags_of(t, weather):
    mvs = {mv for _sp, ms, _b in t["mons"] for mv in ms}
    return {k for k, ms in HAZARD_MOVES.items() if mvs & ms}


def shares(counter):
    total = sum(counter.values()) or 1.0
    return {t: counter.get(t, 0.0) / total for t in TYPES}


def mean_shares(list_of_shares):
    return {t: sum(s[t] for s in list_of_shares) / len(list_of_shares) for t in TYPES}


def player_view(splits_in):
    """(weights, situational weights) for the player's Pokemon over some
    splits: trainer move use for the weights, and each situational term at
    the post's 0.5 times the share of trainer teams that bring it."""
    by_split, _k, _c = trainer_attacks()
    w = weights_from_shares(mean_shares([shares(by_split[s]) for s in splits_in]))
    sit = trainer_situations()
    situ = {}
    for k in SITUATIONAL:
        key = k
        situ[k] = 0.5 * sum(sit[s][key] for s in splits_in) / len(splits_in)
    return w, situ


# -- what the player attacks with ------------------------------------------------

# The player's moves count when they deal real damage: power 40 and up, or a
# move whose power the engine works out (listed as 1: Low Kick, Seismic
# Toss), less the ones pool.py already calls unreliable or a sacrifice.
MIN_POWER = 40
# The player's situational terms are close to nothing (Ian, 2026-11-03): the
# player seldom spends a turn on a hazard, trapping or Prankster, and the AI
# switches only on a knockout or a pivot, so a hazard meets each trainer
# Pokemon at most once. A tenth of the post's 0.5 keeps their sign and makes
# them unable to move a rank on their own. The player sets no weather at all.
PLAYER_SITUATIONAL = 0.05


@functools.lru_cache(maxsize=None)
def player_attacks():
    """{split: {type: number of the player's lines that can hit with it}}.
    A line is the most evolved stage the player owns by the split's end
    (pool.species_by_split); it counts a type once if any of its moves by
    then (pool.moves_at: level-up by the capture rule, TMs and tutors placed
    by then) is a real attack of that type."""
    moves = pokedex.moves(ROOT)
    skip = {m for m, r in moves.items() if r["name"] in pool.CONDITIONAL}
    out = {}
    for split in SPLIT_ORDER:
        owned = pool.species_by_split()[split]
        evolved_from = set()
        for sp in owned:
            for _need, _item, target in pool.evolutions(sp):
                if target in owned:
                    evolved_from.add(sp)
        c = collections.Counter()
        for sp in owned:
            if sp in evolved_from:
                continue
            got = set()
            for mv in pool.moves_at(sp, split):
                rec = moves.get(mv)
                if not damaging(rec) or mv in skip:
                    continue
                if (rec["power"] or 0) >= MIN_POWER or rec["power"] == 1:
                    got.add(rec["type"])
            c.update(got)
        out[split] = c
    return out


def trainer_view(splits_in):
    by_split = player_attacks()
    w = weights_from_shares(mean_shares([shares(by_split[s]) for s in splits_in]))
    situ = {k: PLAYER_SITUATIONAL for k in SITUATIONAL}
    situ["sand"] = situ["hail"] = 0.0
    return w, situ


OXIDE_GROUPS = POST_GROUPS + ("trap", "sand", "hail", "toxic_spikes")


# -- the player's lines -----------------------------------------------------------

@functools.lru_cache(maxsize=None)
def obtainable():
    """{species: the split it can first be owned in} for every stage a run to
    the League can hold: what the Box sim's capture areas can give
    (simulate.world, the starter's choice added, as simulate.context does),
    and each evolution reachable by the League's end (pool.reachable)."""
    root = model.repo_root()
    rank = {s: i for i, s in enumerate(SPLIT_ORDER)}
    first = {}
    for area in simulate.world("League", root):
        for o in area["options"]:
            for sp in o.shares:
                if o.split in rank and (sp not in first or rank[o.split] < rank[first[sp]]):
                    first[sp] = o.split
    starter = next(s for s in scripted.load(root) if s["kind"] == "starter")
    for sp in starter["pool"]:
        first[sp] = SPLIT_ORDER[0]
    todo = list(first)
    while todo:
        sp = todo.pop()
        for need, item, target in pool.evolutions(sp):
            if not pool.reachable(need, item, "League"):
                continue
            at = first[sp]
            for s in SPLIT_ORDER[rank[at]:]:
                if pool.reachable(need, item, s):
                    at = s
                    break
            if target not in first or rank[at] < rank[first[target]]:
                first[target] = at
                todo.append(target)
    return first


def final_stages():
    have = obtainable()
    out = []
    for sp in have:
        if any(t in have and pool.reachable(n, i, "League") for n, i, t in pool.evolutions(sp)):
            continue
        rec = pokedex.load(ROOT, sp)
        if rec and not rec.get("mega_of"):
            out.append(sp)
    return sorted(out)


def line_record(sp):
    rec = pokedex.load(ROOT, sp)
    s = rec["stats"]
    return {"species": sp, "name": rec["name"], "types": rec["types"], "bst": rec["bst"],
            "hp": s["hp"], "def": s["defense"], "spd": s["special_defense"], "spe": s["speed"],
            "abilities": rec["abilities"], "hidden": rec["hidden_ability"],
            "first": obtainable()[sp]}


def counted_ability(rec):
    """The matchup ability that counts: one every regular slot holds."""
    reg = rec["abilities"]
    if len(reg) == 1 and reg[0] in MATCHUP_ABILITIES:
        return reg[0]
    return None


def other_abilities(rec):
    """[(ability, 'slot' or 'hidden')] matchup abilities that do not count."""
    out = []
    if len(rec["abilities"]) > 1:
        out += [(a, "slot") for a in rec["abilities"] if a in MATCHUP_ABILITIES]
    if rec["hidden"] in MATCHUP_ABILITIES and rec["hidden"] not in rec["abilities"]:
        out.append((rec["hidden"], "hidden"))
    return out


def trainer_typings():
    """{typing: kind-weighted count of trainer Pokemon of that typing}."""
    c = collections.Counter()
    for t in trainer_roster():
        for sp, _m, _b in t["mons"]:
            rec = pokedex.load(ROOT, sp)
            if rec:
                c[canonical(rec["types"])] += t["weight"]
    return c


def rank_of(scores):
    """{key: 1-based rank, best first}, ties sharing the better rank."""
    ordered = sorted(scores.values(), reverse=True)
    return {k: 1 + ordered.index(v) for k, v in scores.items()}


def spearman(a, b):
    keys = list(a)
    ra, rb = rank_of(a), rank_of(b)
    n = len(keys)
    d2 = sum((ra[k] - rb[k]) ** 2 for k in keys)
    return 1 - 6 * d2 / (n * (n * n - 1)) if n > 1 else 1.0


def canonical(types):
    """A typing as an unordered pair, in the chart's type order."""
    return tuple(sorted(dict.fromkeys(types), key=TYPES.index))


def typing_name(types):
    return "/".join(t.title() for t in types)


def zscores(values):
    vals = list(values.values())
    mu = sum(vals) / len(vals)
    sd = (sum((v - mu) ** 2 for v in vals) / len(vals)) ** 0.5 or 1.0
    return {k: (v - mu) / sd for k, v in values.items()}


def compute():
    """Every number the doc shows, as one JSON-ready dict."""
    ox, lt = oxide_chart(), later_chart()
    out = {"chart_differences": chart_differences()}
    # Part 1.
    pw = post_weights()
    part1 = {}
    for t in TYPES:
        part1[t] = {"post": POST_RANKING[t],
                    "later_chart": index([t], lt, pw),
                    "oxide_post_terms": index([t], ox, pw),
                    "oxide_all_terms": index([t], ox, pw, count=OXIDE_GROUPS)}
    out["part1"] = part1
    # Part 2.
    by_split, by_kind, changed = trainer_attacks()
    out["trainer_attacks"] = {s: dict(c) for s, c in by_split.items()}
    out["trainer_attacks_by_kind"] = {k: dict(c) for k, c in by_kind.items()}
    out["retyped_moves"] = {f"{m} as {t}": n for (m, t), n in changed.items()}
    out["player_attacks"] = {s: dict(c) for s, c in player_attacks().items()}
    out["situations"] = trainer_situations()
    roster = trainer_roster()
    out["roster"] = {s: {k: sum(1 for t in roster if t["split"] == s and t["kind"] == k)
                         for k in KIND_WEIGHT} for s in SPLIT_ORDER}
    views = {}
    for name, sp in [("overall", SPLIT_ORDER)] + list(PHASES.items()):
        views[("player", name)] = player_view(sp)
        views[("trainer", name)] = trainer_view(sp)
    out["weights"] = {f"{v}/{p}": {"w": w, "situ": s} for (v, p), (w, s) in views.items()}
    part2 = {}
    for t in TYPES:
        part2[t] = {f"{v}/{p}": index([t], ox, w, situ=s, count=OXIDE_GROUPS)
                    for (v, p), (w, s) in views.items()}
    out["part2"] = part2
    # The same, with every situational term at the post's full 0.5, to show
    # how little the hazard scaling moves.
    w_all, _s = views[("player", "overall")]
    out["part2_full_hazards"] = {t: index([t], ox, w_all, count=OXIDE_GROUPS) for t in TYPES}
    # Part 3: every typing an obtainable stage has.
    have = obtainable()
    typings = collections.defaultdict(list)
    for sp in have:
        rec = pokedex.load(ROOT, sp)
        if rec and not rec.get("mega_of"):
            typings[canonical(rec["types"])].append(rec["name"])
    fielded = trainer_typings()
    part3 = {}
    for ty, names in typings.items():
        key = typing_name(ty)
        row = {"lines": sorted(set(names)), "post": index(list(ty), ox, pw),
               "fielded": fielded.get(ty, 0.0)}
        for (v, p), (w, s) in views.items():
            row[f"{v}/{p}"] = index(list(ty), ox, w, situ=s, count=OXIDE_GROUPS)
        part3[key] = row
    out["part3"] = part3
    # Part 4: every final stage, with its counted ability.
    pw_all, ps_all = views[("player", "overall")]
    tw_all, ts_all = views[("trainer", "overall")]
    part4 = {}
    for sp in final_stages():
        rec = line_record(sp)
        ab = counted_ability(rec)
        row = dict(rec)
        row["counted_ability"] = ab
        row["player"] = index(rec["types"], ox, pw_all, situ=ps_all, count=OXIDE_GROUPS, ability=ab)
        row["trainer"] = index(rec["types"], ox, tw_all, situ=ts_all, count=OXIDE_GROUPS, ability=ab)
        row["typing_only"] = index(rec["types"], ox, pw_all, situ=ps_all, count=OXIDE_GROUPS)
        row["other"] = [(a, how, index(rec["types"], ox, pw_all, situ=ps_all, count=OXIDE_GROUPS,
                                       ability=a)) for a, how in other_abilities(rec)]
        part4[sp] = row
    zi = zscores({k: r["player"] for k, r in part4.items()})
    zb = zscores({k: r["bst"] for k, r in part4.items()})
    zbulk = zscores({k: r["hp"] + r["def"] + r["spd"] for k, r in part4.items()})
    for k, r in part4.items():
        r["z_index"], r["z_bst"], r["z_bulk"] = zi[k], zb[k], zbulk[k]
        r["placement"] = zi[k] + zbulk[k]
    out["part4"] = part4
    return out


# -- the doc's tables ---------------------------------------------------------------

def _f(x, nd=1):
    return f"{x:+.{nd}f}" if x else f"{0:.{nd}f}"


def _table(head, rows):
    out = ["| " + " | ".join(head) + " |", "|" + "|".join("---" for _ in head) + "|"]
    out += ["| " + " | ".join(str(c) for c in r) + " |" for r in rows]
    return out


def _abil(a):
    return a.replace("_", " ").title() if a else ""


def render(out):
    """The four parts' tables, as Markdown lines, for the doc."""
    L = []
    T = lambda t: t.title()   # noqa: E731
    # Part 1.
    L += ["### chart"] + _table(["Attacking", "Defending", "Oxide", "Later games"],
                                [[T(a), T(d), f"{o:g}x", f"{lt:g}x"] for a, d, o, lt in out["chart_differences"]])
    p1 = out["part1"]
    ranks = {k: rank_of({t: p1[t][k] for t in TYPES})
             for k in ("post", "later_chart", "oxide_post_terms", "oxide_all_terms")}
    rows = []
    for t in sorted(TYPES, key=lambda t: (-p1[t]["oxide_post_terms"], -p1[t]["post"])):
        r = p1[t]
        rows.append([ranks["oxide_post_terms"][t], T(t), _f(r["post"]), _f(r["later_chart"]),
                     _f(r["oxide_post_terms"]), _f(r["oxide_all_terms"]), ranks["post"][t]])
    L += ["### part1-singles"] + _table(
        ["Rank in Oxide", "Type", "Post's figure", "Post's formula, later chart (check)",
         "Oxide's chart, post's terms", "Oxide's chart, every engine term", "Post's rank"], rows)
    # Part 2: attack shares by split.
    att = out["trainer_attacks"]
    sh = {s: shares(collections.Counter(att[s])) for s in SPLIT_ORDER}
    rows = [[T(t)] + [f"{100 * sh[s][t]:.0f}" for s in SPLIT_ORDER] for t in TYPES]
    L += ["### part2-trainer-shares"] + _table(["Type"] + SPLIT_ORDER, rows)
    pa = out["player_attacks"]
    psh = {s: shares(collections.Counter(pa[s])) for s in SPLIT_ORDER}
    rows = [[T(t)] + [f"{100 * psh[s][t]:.0f}" for s in SPLIT_ORDER] for t in TYPES]
    L += ["### part2-player-shares"] + _table(["Type"] + SPLIT_ORDER, rows)
    W = out["weights"]
    cols = ["player/overall", "player/early", "player/middle", "player/late",
            "trainer/overall", "trainer/early", "trainer/middle", "trainer/late"]
    rows = [[T(t), "2" if t in POST_CC else "1"] + [f"{W[c]['w'][t]:.2f}" for c in cols] for t in TYPES]
    L += ["### part2-weights"] + _table(
        ["Type", "Post"] + ["Player's view, " + c.split("/")[1] for c in cols[:4]]
        + ["Trainers' view, " + c.split("/")[1] for c in cols[4:]], rows)
    sit = out["situations"]
    rows = []
    for s in SPLIT_ORDER:
        r = sit[s]
        rows.append([s, r["teams"], r["count"]["stealth_rock"], r["count"]["spikes"],
                     r["count"]["toxic_spikes"], r["count"]["sticky_web"],
                     f"{100 * r['stealth_rock']:.0f}", f"{100 * r['spikes_web']:.0f}",
                     f"{100 * r['toxic_spikes']:.0f}", f"{100 * r['sand']:.0f}", f"{100 * r['hail']:.0f}",
                     f"{100 * r['trap']:.0f}", f"{100 * r['prankster']:.0f}"])
    L += ["### part2-situations"] + _table(
        ["Split", "Teams", "Stealth Rock teams", "Spikes teams", "Toxic Spikes teams", "Sticky Web teams",
         "Stealth Rock %", "Spikes or Web %", "Toxic Spikes %", "Sand %", "Hail %", "Trapping %",
         "Prankster %"], rows)
    rows = [[k.replace("/", ", ")] + [f"{v['situ'][x]:.3f}" for x in SITUATIONAL] for k, v in W.items()
            if k.endswith("overall") or k.startswith("player")]
    L += ["### part2-situational-weights"] + _table(["View"] + [x.replace("_", " ") for x in SITUATIONAL], rows)
    p2 = out["part2"]
    rk = {c: rank_of({t: p2[t][c] for t in TYPES}) for c in cols}
    rows = []
    for t in sorted(TYPES, key=lambda t: -p2[t]["player/overall"]):
        rows.append([T(t), _f(p1[t]["oxide_post_terms"])]
                    + [f"{_f(p2[t][c], 2)} ({rk[c][t]})" for c in cols])
    L += ["### part2-singles"] + _table(
        ["Type", "Post's terms"] + ["Player, " + c.split("/")[1] for c in cols[:4]]
        + ["Trainer, " + c.split("/")[1] for c in cols[4:]], rows)
    full = out["part2_full_hazards"]
    rf = rank_of(full)
    moved = [(T(t), rk["player/overall"][t], rf[t]) for t in TYPES if rk["player/overall"][t] != rf[t]]
    L += ["### part2-full-hazards", "Ranks that change with every situational term at the full 0.5: "
          + ("; ".join(f"{a} {b} to {c}" for a, b, c in moved) if moved else "none") + "."]
    # Part 3.
    p3 = out["part3"]
    pr = rank_of({k: r["player/overall"] for k, r in p3.items()})
    tr = rank_of({k: r["trainer/overall"] for k, r in p3.items()})
    po = rank_of({k: r["post"] for k, r in p3.items()})
    ordered = sorted(p3, key=lambda k: -p3[k]["player/overall"])

    def row3(k):
        r = p3[k]
        names = r["lines"]
        shown = ", ".join(names[:5]) + (f" and {len(names) - 5} more" if len(names) > 5 else "")
        return [pr[k], k, _f(r["player/overall"], 2), _f(r["trainer/overall"], 2), tr[k], _f(r["post"]),
                po[k], f"{r['fielded']:.0f}", shown]
    head3 = ["Rank", "Typing", "Player's view", "Trainers' view", "Trainers' rank", "Post's formula",
             "Post's rank", "Fielded by trainers (weighted)", "Obtainable stages"]
    L += ["### part3-best"] + _table(head3, [row3(k) for k in ordered[:20]])
    L += ["### part3-worst"] + _table(head3, [row3(k) for k in ordered[-20:]])
    movers = sorted(p3, key=lambda k: -abs(pr[k] - tr[k]))
    big = [k for k in movers if abs(pr[k] - tr[k]) >= 15]
    L += ["### part3-movers"] + _table(
        ["Typing", "Player's rank", "Trainers' rank", "Player's view", "Trainers' view"],
        [[k, pr[k], tr[k], _f(p3[k]["player/overall"], 2), _f(p3[k]["trainer/overall"], 2)] for k in big])
    L += ["### part3-stats",
          f"Typings: {len(p3)}. Rank correlation (Spearman) of the player's view with the trainers' view: "
          f"{spearman({k: r['player/overall'] for k, r in p3.items()}, {k: r['trainer/overall'] for k, r in p3.items()}):.2f}; "
          f"with the post's formula: "
          f"{spearman({k: r['player/overall'] for k, r in p3.items()}, {k: r['post'] for k, r in p3.items()}):.2f}. "
          f"Typings moving 15 places or more between the views: {len(big)}."]
    # Part 4.
    p4 = out["part4"]

    def ab4(r):
        bits = []
        if r["counted_ability"]:
            bits.append(_abil(r["counted_ability"]) + " (counted)")
        for a, how, val in r["other"]:
            if abs(val - r["typing_only"]) >= 0.05:
                bits.append(f"{_abil(a)} ({'one slot' if how == 'slot' else 'hidden'}, {_f(val, 1)})")
        return "; ".join(bits)

    def row4(r, extra=()):
        return [r["name"], "/".join(T(t) for t in r["types"]), _f(r["player"], 2), _f(r["trainer"], 2),
                r["bst"], r["hp"], r["def"], r["spd"], r["spe"], r["first"]] + list(extra) + [ab4(r)]
    head4 = ["Line", "Typing", "Index, player's view", "Index, trainers' view", "BST", "HP", "Def",
             "SpD", "Spe", "First owned"]
    pl = sorted(p4.values(), key=lambda r: -r["placement"])
    L += ["### part4-most"] + _table(head4 + ["Placement", "Abilities"],
                                     [row4(r, [f"{r['placement']:+.2f}"]) for r in pl[:20]])
    L += ["### part4-least"] + _table(head4 + ["Placement", "Abilities"],
                                      [row4(r, [f"{r['placement']:+.2f}"]) for r in pl[-20:][::-1]])
    strong = sorted([r for r in p4.values() if r["z_index"] > 0.5 and r["z_bst"] > 0.5],
                    key=lambda r: -(r["z_index"] + r["z_bst"]))
    weak = sorted([r for r in p4.values() if r["z_index"] < -0.5 and r["z_bst"] < -0.5],
                  key=lambda r: (r["z_index"] + r["z_bst"]))
    L += ["### part4-strong"] + _table(head4 + ["Abilities"], [row4(r) for r in strong])
    L += ["### part4-weak"] + _table(head4 + ["Abilities"], [row4(r) for r in weak])
    by = collections.defaultdict(list)
    for r in p4.values():
        for t in r["types"]:
            by[t].append(r)
    rows = []
    for t in sorted(by, key=lambda t: -sum(r["player"] for r in by[t]) / len(by[t])):
        rs = by[t]
        n = len(rs)
        rows.append([T(t), n, _f(sum(r["player"] for r in rs) / n, 2), _f(sum(r["trainer"] for r in rs) / n, 2),
                     f"{sum(r['bst'] for r in rs) / n:.0f}",
                     f"{sum(r['hp'] + r['def'] + r['spd'] for r in rs) / n:.0f}",
                     f"{sum(r['spe'] for r in rs) / n:.0f}"])
    L += ["### part4-by-type"] + _table(
        ["Type", "Lines", "Mean index, player's view", "Mean index, trainers' view", "Mean BST",
         "Mean HP+Def+SpD", "Mean Spe"], rows)
    allr = sorted(p4.values(), key=lambda r: -r["player"])
    L += ["### part4-all"] + _table(head4 + ["Abilities"], [row4(r) for r in allr])
    return L


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--json", help="write every number to this file")
    ap.add_argument("--tables", help="write the doc's tables, as Markdown sections, to this file")
    args = ap.parse_args(argv)
    out = compute()
    for t in sorted(TYPES, key=lambda t: -out["part1"][t]["oxide_post_terms"]):
        r = out["part1"][t]
        print(f"{t:9} post {r['post']:5} later {r['later_chart']:5.1f} oxide {r['oxide_post_terms']:5.1f} "
              f"all {r['oxide_all_terms']:5.1f}")
    if args.tables:
        with open(args.tables, "w", encoding="utf-8") as f:
            f.write("\n".join(render(out)) + "\n")
    if args.json:
        with open(args.json, "w", encoding="utf-8") as f:
            json.dump(out, f, indent=1, default=str)


if __name__ == "__main__":
    main()

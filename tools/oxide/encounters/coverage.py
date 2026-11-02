"""A trainer team's type coverage, for the Trainers tab (Ian, 2026-11-02).

Three tables, all drawn under the team:

- defence: for each of the eighteen attacking types, how many of the team's
  members take x4, x2, x1, x1/2, x1/4 and x0 from it;
- offence: for each member, its best effectiveness against every Pokemon in
  scope over its damaging moves (status moves do not count), grouped as
  pokemondb's coverage tool groups them;
- walls: for each Pokemon in scope, the members whose best damaging move
  does x1/2 or less against it, worst walls first.

The scope is what the player can have by the trainer's split, from the Box
sim's own availability (simulate.world and can_give, plus the starter pool,
with each stage reachable by that split's cap or stones as simulate.Values
judges it), or the whole dex.

The type chart is Oxide's own (pokedex.type_chart). Abilities count, with the
engine as the authority; every rule below names where in src/battle/ it
comes from. A member's ability is the one the game builds it with. A Pokemon
in scope has an ability only when every one of its regular slots holds it.
"""
import functools
import json
import math
import os
import re

from . import dex
from . import evolve
from . import model
from . import pokedex
from . import progression
from . import scripted
from . import simulate

# The eighteen attacking types in the order the games list them, the Dex
# tab's matchup grid's order (ui/index.html's TYPES).
TYPES = ["NORMAL", "FIRE", "WATER", "ELECTRIC", "GRASS", "ICE", "FIGHTING",
         "POISON", "GROUND", "FLYING", "PSYCHIC", "BUG", "ROCK", "GHOST", "DRAGON",
         "DARK", "STEEL", "FAIRY"]
# The columns of the defence table, strongest first.
BUCKETS = [4, 2, 1, 0.5, 0.25, 0]

# Abilities that take every move of one type, so their holder takes nothing
# from it. Levitate is read in BattleSystem_ApplyTypeChart (battle_lib.c),
# which lets Thousand Arrows through; the rest in
# BattleSystem_TriggerImmunityAbility (battle_lib.c), which absorbs the move
# before any damage is dealt.
IMMUNE = {
    "LEVITATE": "GROUND",
    "VOLT_ABSORB": "ELECTRIC", "MOTOR_DRIVE": "ELECTRIC", "LIGHTNING_ROD": "ELECTRIC",
    "WATER_ABSORB": "WATER", "DRY_SKIN": "WATER", "STORM_DRAIN": "WATER",
    "FLASH_FIRE": "FIRE",
    "SAP_SIPPER": "GRASS",
}
# Abilities that scale the damage their holder takes from one type, from
# BattleSystem_CalcMoveDamage (battle_lib.c): Thick Fat, Purifying Salt,
# Water Bubble and Heatproof halve the move's power, Dry Skin raises a Fire
# move's by a quarter, and Fluffy doubles a Fire move's damage.
SCALES = {
    "THICK_FAT": {"FIRE": 0.5, "ICE": 0.5},
    "HEATPROOF": {"FIRE": 0.5},
    "WATER_BUBBLE": {"FIRE": 0.5},
    "PURIFYING_SALT": {"GHOST": 0.5},
    "DRY_SKIN": {"FIRE": 1.25},
    "FLUFFY": {"FIRE": 2.0},
}
# Filter and Solid Rock cut a super effective hit to three quarters
# (BattleSystem_ApplyTypeChart).
SOFTEN_SUPER = ("FILTER", "SOLID_ROCK")

# Moves whose chart reading the engine changes (BattleSystem_ApplyTypeChart,
# MoveReadsChartEntry, MoveChartMultiplier, BasicTypeMulApplies).
FLYING_PRESS, FREEZE_DRY, THOUSAND_ARROWS = "MOVE_FLYING_PRESS", "MOVE_FREEZE_DRY", "MOVE_THOUSAND_ARROWS"

# The moves whose type the engine works out in battle are Hidden Power,
# Judgment, Natural Gift and Weather Ball (CalcMoveType, battle_lib.c, and
# BtlCmd_CalcHiddenPowerParams, battle_script.c); move_type gives the first
# three theirs. Weather Ball is left at its listed Normal, since the weather
# is not known here. Terrain Pulse, Techno Blast and Multi-Attack are not
# among the engine's cases, so in Oxide they always keep their listed type.
NOTE = ("Abilities count as Oxide's engine applies them. Hidden Power, Judgment and "
        "Natural Gift take the type the engine gives them from the member's IVs and held "
        "item. Weather Ball counts as Normal, its type in clear weather, and Terrain Pulse, "
        "Techno Blast and Multi-Attack keep their listed type, as Oxide's engine never "
        "changes it. Held items count only there: an Air Balloon or a Ring Target is left out.")


def bucket(mult):
    """The column a multiplier falls in: the nearest of x4 to x1/4 on a
    doubling scale, so Filter's x1.5 stays super effective and Dry Skin's
    x1.25 stays neutral, as the game's own messages put them."""
    if mult <= 0:
        return 0
    step = max(-2, min(2, round(math.log2(mult))))
    return 2.0 ** step if step < 0 else int(2 ** step)


def multiplier(chart, foresight, move_type, def_types, move=None, atk=None, dfn=None,
               fixed=False):
    """(multiplier, abilities that moved it) for one hit of `move_type`
    from an attacker with ability `atk` on a Pokemon of `def_types` with
    ability `dfn`. `move` names a move the engine reads specially, and
    `fixed` marks one whose damage ignores the chart but for its immunities."""
    used = []
    # Mold Breaker ignores every defending ability above
    # (Battler_IgnorableAbility, battle_lib.c).
    if atk == "MOLD_BREAKER" and dfn:
        if multiplier(chart, foresight, move_type, def_types, move, None, dfn, fixed)[1]:
            used.append("MOLD_BREAKER")
        dfn = None
    if dfn in IMMUNE and IMMUNE[dfn] == move_type and not (dfn == "LEVITATE" and move == THOUSAND_ARROWS):
        return 0.0, [dfn]
    reads = [move_type] + (["FLYING"] if move == FLYING_PRESS and move_type != "FLYING" else [])
    mult = 1.0
    for d in dict.fromkeys(def_types):
        for a in reads:
            m = chart.get((a, d), 1.0)
            # Scrappy stops reading the chart at its Foresight marker, which
            # drops Normal and Fighting's Ghost immunity.
            if atk == "SCRAPPY" and (a, d) in foresight:
                if m != 1.0:
                    used.append("SCRAPPY")
                continue
            if move == THOUSAND_ARROWS and d == "FLYING" and m == 0:
                continue
            if move == FREEZE_DRY and d == "WATER":
                m = 2.0
            mult *= m
    # Wonder Guard lets through only a damaging hit that is super effective
    # on balance (BattleSystem_ApplyTypeChart).
    if dfn == "WONDER_GUARD" and 0 < mult <= 1:
        return 0.0, used + [dfn]
    # Seismic Toss, Counter, Super Fang and the like set
    # SYSCTL_IGNORE_TYPE_CHECKS in their effect scripts, so the chart's
    # multipliers never touch their damage (ApplyTypeMultiplier, battle_lib.c);
    # its immunities still stop them.
    if fixed:
        return (1.0 if mult > 0 else 0.0), list(dict.fromkeys(used))
    if mult > 1 and dfn in SOFTEN_SUPER:
        mult *= 0.75
        used.append(dfn)
    # Tinted Lens doubles a not very effective hit (BattleSystem_ApplyTypeChart).
    if 0 < mult < 1 and atk == "TINTED_LENS":
        mult *= 2
        used.append(atk)
    scale = (SCALES.get(dfn) or {}).get(move_type)
    if scale and mult > 0:
        mult *= scale
        used.append(dfn)
    return mult, list(dict.fromkeys(used))


# -- move types ----------------------------------------------------------------


@functools.lru_cache(maxsize=4)
def _c_list(root, name):
    """The MOVE_ constants of one static move list in battle_lib.c."""
    with open(os.path.join(root, pokedex.BATTLE_LIB), encoding="utf-8") as f:
        src = f.read()
    m = re.search(r"\b" + re.escape(name) + r"\[\]\s*=\s*\{(.*?)\};", src, re.S)
    return frozenset(re.findall(r"MOVE_\w+", m.group(1))) if m else frozenset()


@functools.lru_cache(maxsize=4)
def fixed_effects(root):
    """The effect ids whose scripts set SYSCTL_IGNORE_TYPE_CHECKS: the moves
    whose damage the type chart does not scale."""
    base = os.path.join(root, "res", "battle", "scripts", "effects")
    out = set()
    for name in os.listdir(base):
        m = re.fullmatch(r"effect_script_(\d+)\.s", name)
        if m:
            with open(os.path.join(base, name), encoding="utf-8") as f:
                if "SYSCTL_IGNORE_TYPE_CHECKS" in f.read():
                    out.add(int(m.group(1)))
    return frozenset(out)


@functools.lru_cache(maxsize=256)
def _item(root, item):
    """An item's data file, or {}."""
    if not item or item == "ITEM_NONE":
        return {}
    path = os.path.join(root, "res", "items", "data", item.replace("ITEM_", "").lower() + ".json")
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, ValueError):
        return {}


def hidden_power_type(ivs):
    """Hidden Power's type from the six IVs (HP, Attack, Defense, Speed,
    Sp. Atk, Sp. Def), by BtlCmd_CalcHiddenPowerParams (battle_script.c):
    one bit from each, scaled to 1..16, skipping the Mystery type's slot."""
    bits = sum((iv & 1) << i for i, iv in enumerate(ivs))
    index = bits * 15 // 63 + 1
    # The engine steps an index at or past Mystery's one place on; a list
    # without Mystery in it lands on the same type at the unstepped index.
    order = [t for t in _type_order(model.repo_root()) if t != "MYSTERY"]
    return order[index]


@functools.lru_cache(maxsize=2)
def _type_order(root):
    with open(os.path.join(root, "generated", "pokemon_types.txt"), encoding="utf-8") as f:
        return [l.strip().replace("TYPE_", "") for l in f if l.strip().startswith("TYPE_")]


def move_type(root, rec, ability, item=None, iv=0):
    """(type, note or None) a member's move has in battle, or (None, why)
    when the move fails as the member is built."""
    move, listed = rec["move"], rec["type"]
    # Normalize makes every move Normal (BattleSystem_ApplyTypeChart).
    if ability == "NORMALIZE":
        return "NORMAL", "Normal by Normalize" if listed != "NORMAL" else None
    kind, note = listed, None
    if move == "MOVE_HIDDEN_POWER":
        kind = hidden_power_type([iv] * 6)
        note = f"{kind.title()} by its IVs"
    elif move == "MOVE_JUDGMENT":
        effect = _item(root, item).get("holdEffect") or ""
        if effect.startswith("HOLD_EFFECT_ARCEUS_"):
            kind = effect.replace("HOLD_EFFECT_ARCEUS_", "")
            note = f"{kind.title()} by its plate"
    elif move == "MOVE_NATURAL_GIFT":
        gift = _item(root, item).get("naturalGiftType")
        if not gift:
            return None, "fails without a berry"
        kind = gift.replace("TYPE_", "")
        note = f"{kind.title()} by its berry"
    elif move == "MOVE_WEATHER_BALL":
        note = "Normal in clear weather"
    # Pixilate turns a move listed as Normal Fairy, but not the moves that
    # keep their type, and Liquid Voice turns sound moves Water
    # (BattleSystem_SetMoveTypeByAbility).
    if ability == "PIXILATE" and listed == "NORMAL" and move not in _c_list(root, "sMovesKeepTheirType"):
        kind, note = "FAIRY", "Fairy by Pixilate"
    elif ability == "LIQUID_VOICE" and move in _c_list(root, "sSoundMoves"):
        kind, note = "WATER", "Water by Liquid Voice"
    return kind, note


# -- the scope -----------------------------------------------------------------


def _scope_stamp(root):
    """Changes whenever what the Box sim reads does: the encounter tables,
    the sidecar and the scripted sources, and the species records."""
    newest = 0
    for rel in (("res", "field", "encounters"), ("docs", "oxide", "encounters")):
        base = os.path.join(root, *rel)
        if os.path.isdir(base):
            for e in os.scandir(base):
                if e.is_file():
                    newest = max(newest, e.stat().st_mtime_ns)
    base = os.path.join(root, "res", "pokemon")
    for e in os.scandir(base):
        path = os.path.join(e.path, "data.json")
        if os.path.isfile(path):
            newest = max(newest, os.stat(path).st_mtime_ns)
    return newest


def split_scope(root, split):
    """Every species the player can have by `split`, in dex order, or None
    when the split is not one the Box sim knows."""
    rank = progression.split_index(model.load_sidecar() or {})
    if split not in rank:
        return None
    return _split_scope(root, split, _scope_stamp(root))


@functools.lru_cache(maxsize=32)
def _split_scope(root, split, stamp):
    sidecar = model.load_sidecar() or {}
    rank = progression.split_index(sidecar)
    caught = set()
    # The Box sim's capture areas up to this split, and every species each
    # can give.
    for area in simulate.world(split, root):
        caught.update(simulate.can_give(area))
    # The starter, which the Box sim handles apart from the areas.
    for src in scripted.load(root):
        if src["kind"] == "starter" and rank.get(src["split"], 99) <= rank[split]:
            caught.update(src["pool"])
    # Then every stage those reach by this split, by the Box sim's rule: a
    # level under the cap, or a stone once it is in reach.
    values = simulate.Values(root, split, sidecar)
    have, todo = set(), list(caught)
    while todo:
        sp = todo.pop()
        if sp in have:
            continue
        have.add(sp)
        for target, level, item, _fixed in evolve.routes(root, sp):
            if target in values.on_list and values._ready(level, item):
                todo.append(target)
    order = {sp: i for i, sp in enumerate(pokedex.species_list(root))}
    return tuple(sorted((sp for sp in have if sp in order), key=order.get))


def warm(root=None):
    """Works out every split's scope once, off to one side when the server
    starts: the first takes several seconds (the Box sim's values read the
    balance census), each later one under half a second."""
    root = root or model.repo_root()
    try:
        for split in progression.split_index(model.load_sidecar() or {}):
            split_scope(root, split)
    except Exception:
        pass


def dex_scope(root):
    return tuple(pokedex.species_list(root))


def defender(root, species):
    """A Pokemon in scope as the tables read it: its types, and its ability
    when every regular slot holds the same one."""
    rec = pokedex.load(root, species) or {}
    abilities = set(rec.get("abilities") or [])
    return {"types": rec.get("types") or ["NORMAL"],
            "ability": abilities.pop() if len(abilities) == 1 else None}


# -- the tables ----------------------------------------------------------------


def defence(root, members):
    """One row per attacking type: the members in each column, with the
    ability that moved any of them."""
    chart, foresight = pokedex.type_chart(root), pokedex.foresight_entries(root)
    rows = []
    for t in TYPES:
        cells = {str(b): [] for b in BUCKETS}
        for i, m in enumerate(members):
            mult, used = multiplier(chart, foresight, t, m["types"], dfn=m["ability"])
            plain, _ = multiplier(chart, foresight, t, m["types"])
            entry = {"i": i, "mult": mult}
            if bucket(mult) != bucket(plain):
                entry["ability"] = m["ability"]
                entry["plain"] = plain
            elif used:
                # An ability that changed the number but not the column,
                # such as Filter's x1.5 or Dry Skin's x2.5.
                entry["ability"] = m["ability"]
            cells[str(bucket(mult))].append(entry)
        rows.append({"type": t, "cells": cells})
    return rows


def _attacks(root, member, moves):
    """A member's damaging moves with the type each has in battle."""
    out, notes = [], []
    for mv in member["moves"]:
        rec = moves.get(mv)
        if not rec or rec["class"] == "STATUS" or mv == "MOVE_NONE":
            continue
        kind, note = move_type(root, rec, member["ability"], member.get("item"), member.get("iv", 0))
        entry = {"move": mv, "name": rec["name"], "type": kind, "class": rec["class"]}
        if rec.get("effect_id") in fixed_effects(root):
            entry["fixed"] = True
            note = "damage ignores type" + (", " + note if note else "")
        if note:
            entry["note"] = note
        if kind is None:
            notes.append(f"{rec['name']} {note}")
            continue
        out.append(entry)
    return out, notes


GROUP = {4: "super", 2: "super", 1: "neutral", 0.5: "resisted", 0.25: "resisted", 0: "immune"}


def _best(chart, foresight, attacks, atk, target):
    """The best hit of a member's attacks on one Pokemon in scope: (mult,
    the best without either side's ability, the abilities that changed any
    move's hit)."""
    best, plain, used = None, None, []
    for a in attacks:
        fixed = bool(a.get("fixed"))
        mult, why = multiplier(chart, foresight, a["type"], target["types"], a["move"],
                               atk, target["ability"], fixed)
        bare, _ = multiplier(chart, foresight, a["type"], target["types"], a["move"], fixed=fixed)
        best = mult if best is None else max(best, mult)
        plain = bare if plain is None else max(plain, bare)
        if mult != bare:
            used += why
    return best, plain, list(dict.fromkeys(used))


def offence(root, members, scope):
    """Per member, how it hits every Pokemon in scope; and the walls."""
    chart, foresight = pokedex.type_chart(root), pokedex.foresight_entries(root)
    moves = pokedex.moves(root)
    targets = {sp: defender(root, sp) for sp in scope}
    per, walls = [], {sp: [] for sp in scope}
    for i, m in enumerate(members):
        attacks, notes = _attacks(root, m, moves)
        row = {"i": i, "attacks": attacks, "notes": notes,
               "counts": {g: 0 for g in ("super", "neutral", "resisted", "immune")},
               "moved": {g: [] for g in ("super", "neutral", "resisted", "immune")},
               "resisted": [], "immune": []}
        if not attacks:
            row["counts"] = None
            per.append(row)
            continue
        for sp in scope:
            mult, plain, used = _best(chart, foresight, attacks, m["ability"], targets[sp])
            group = GROUP[bucket(mult)]
            row["counts"][group] += 1
            entry = {"sp": sp, "mult": bucket(mult)}
            if GROUP[bucket(plain)] != group:
                entry["ability"] = used
                row["moved"][group].append(entry)
            if group in ("resisted", "immune"):
                row[group].append(entry)
                # Walled is x1/2 or worse (Ian, 2026-11-02); an ability is
                # named when the member would not be walled without it.
                wall = {"i": i, "mult": bucket(mult)}
                if bucket(plain) > 0.5:
                    wall["ability"] = used
                walls[sp].append(wall)
        per.append(row)
    rows = [{"sp": sp, "members": w} for sp, w in walls.items() if w]
    order = {sp: n for n, sp in enumerate(scope)}
    rows.sort(key=lambda r: (-len(r["members"]), order[r["sp"]]))
    return {"members": per, "walls": rows, "size": len(scope),
            "clear": len(scope) - len(rows)}


def team(root, members, split):
    """Everything the coverage tables draw, for one team. `members` are
    dicts of species, types, ability (no prefix), move constants, item and
    IV, as trainers.detail builds them."""
    out = {"types": TYPES, "note": NOTE, "defence": defence(root, members), "scopes": {}}
    scoped = split_scope(root, split) if split else None
    if scoped is not None:
        out["scopes"]["split"] = offence(root, members, scoped)
    out["scopes"]["dex"] = offence(root, members, dex_scope(root))
    # Name, types and icon folder for every Pokemon the lists can show.
    shown = set()
    for s in out["scopes"].values():
        for r in s["members"]:
            for g in ("resisted", "immune"):
                shown.update(e["sp"] for e in r[g])
            for g in r["moved"].values():
                shown.update(e["sp"] for e in g)
        shown.update(r["sp"] for r in s["walls"])
    out["species"] = {}
    for sp in shown:
        rec = pokedex.load(root, sp) or {}
        d = defender(root, sp)
        out["species"][sp] = {"name": rec.get("name") or dex.display_name(sp),
                              "folder": rec.get("folder"), "types": d["types"],
                              "ability": d["ability"]}
    return out

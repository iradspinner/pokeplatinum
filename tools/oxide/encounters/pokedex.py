"""Species, moves and the type chart, read out of `res/` rather than out of a ROM.

M8's data layer. Everything the dex shows comes from the same JSON the build
consumes, so a viewer built on it cannot drift from the game. That is not only
convenient: uploading the built ROM to a tool written for vanilla Platinum
garbles the dex, the encounter tables and the location names, because Phase 4
gave the species archives 667 members instead of 508 and grew the species record
from 44 bytes to 48 and the evolution record from 44 to 56. Reading `res/` is
correct by construction.

`dex.py` next door is about pick-list *lines* and stays as it is; this module is
about the species themselves.

The vanilla baseline is `git show main:res/pokemon/<folder>/data.json`, the same
trick the linter uses for tables. A species with no row on `main` is one of the
159 this project added, and reads as new rather than as a change.
"""
import functools
import json
import os
import re
import subprocess

from . import model

BATTLE_LIB = os.path.join("src", "battle", "battle_lib.c")
STAT_KEYS = ("hp", "attack", "defense", "special_attack", "special_defense", "speed")
SPRITES = ("male_front", "female_front", "male_back", "female_back", "icon",
           "footprint")


def folder_of(species):
    """SPECIES_MR_MIME -> mr_mime, which is what res/pokemon is keyed by."""
    return species.replace("SPECIES_", "").lower()


def _strip(value, prefix):
    return value[len(prefix):] if value.startswith(prefix) else value


@functools.lru_cache(maxsize=4)
def species_list(root):
    """Every species with a folder, in the generated list's order (dex order)."""
    path = os.path.join(root, "generated", "species.txt")
    with open(path, encoding="utf-8") as f:
        names = [l.strip() for l in f if l.strip()]
    out = []
    for name in names:
        if name in ("SPECIES_NONE", "SPECIES_EGG", "SPECIES_BAD_EGG"):
            continue
        if os.path.isdir(os.path.join(root, "res", "pokemon", folder_of(name))):
            out.append(name)
    return out


def _read(root, rel, ref=None):
    """A res/ file from the working tree, or from a git ref."""
    if ref is None:
        try:
            with open(os.path.join(root, rel), encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, ValueError):
            return None
    out = subprocess.run(["git", "-C", root, "show", f"{ref}:{rel}"],
                         capture_output=True, text=True)
    if out.returncode != 0:
        return None
    try:
        return json.loads(out.stdout)
    except ValueError:
        return None


@functools.lru_cache(maxsize=4096)
def load(root, species, ref=None):
    """One species as the dex wants it, or None when the ref has no such file."""
    raw = _read(root, f"res/pokemon/{folder_of(species)}/data.json", ref)
    if raw is None:
        return None
    stats = raw.get("base_stats") or {}
    abilities = [_strip(a, "ABILITY_") for a in (raw.get("abilities") or [])]
    # Two ordinary abilities and, on the species this project added, a hidden one
    # in a third slot. A species with only one ability either repeats it or fills
    # the second slot with NONE, and both mean the same thing.
    hidden = abilities[2] if len(abilities) > 2 else None
    if hidden in ("NONE", ""):
        hidden = None
    ordinary = [a for a in abilities[:2] if a not in ("NONE", "")]
    if len(ordinary) == 2 and ordinary[0] == ordinary[1]:
        ordinary = ordinary[:1]
    pokedex = (raw.get("pokedex_data") or {})
    en = pokedex.get("en") or {}
    learnset = raw.get("learnset") or {}
    return {
        "species": species,
        "folder": folder_of(species),
        # The twelve alternate-form records carry "-----" for a name, because a
        # form is named after its base in game. Derive one from the folder
        # rather than show dashes: Alolan Ninetales is a species Ian put in
        # tables on purpose, not a placeholder.
        "name": _name_of(en.get("name"), folder_of(species)),
        "mega_of": _mega_of(species),
        "stats": {k: stats.get(k, 0) for k in STAT_KEYS},
        "bst": sum(stats.get(k, 0) for k in STAT_KEYS),
        # Order matters: the first is the primary type. A single-typed species
        # repeats it, which is one type, not two.
        "types": list(dict.fromkeys(_strip(t, "TYPE_")
                                    for t in (raw.get("types") or []))) or ["NORMAL"],
        "abilities": ordinary,
        "hidden_ability": hidden,
        "gender_ratio": _strip(raw.get("gender_ratio") or "", "GENDER_RATIO_"),
        "egg_groups": [_strip(g, "EGG_GROUP_") for g in (raw.get("egg_groups") or [])],
        "catch_rate": raw.get("catch_rate"),
        "base_exp": raw.get("base_exp_reward"),
        "base_friendship": raw.get("base_friendship"),
        "hatch_cycles": raw.get("hatch_cycles"),
        "exp_rate": _strip(raw.get("exp_rate") or "", "EXP_RATE_"),
        "ev_yields": raw.get("ev_yields") or {},
        "held_items": raw.get("held_items") or {},
        "evolutions": [_evolution(e) for e in (raw.get("evolutions") or [])
                       if isinstance(e, list) and e],
        "learnset": [[lv, mv] for lv, mv in (learnset.get("by_level") or [])],
        "by_tm": learnset.get("by_tm") or [],
        "by_tutor": learnset.get("by_tutor") or [],
        "category": en.get("category"),
        "entry": "".join(en.get("entry_text") or []).strip(),
        "height_inches": pokedex.get("height_inches"),
        "weight_pounds": pokedex.get("weight_pounds"),
    }


def _name_of(name, folder):
    name = (name or "").strip()
    if not name or set(name) <= {"-"}:
        return folder.replace("_", " ").title()
    return name.title()


def _mega_of(species):
    """The species this is a mega of, or None. Megas are the base's constant
    with `_M`; a regional form is its own species with its own name, and a
    stage like Porygon-Z only looks like a suffix."""
    return species[:-2] if species.endswith("_M") else None


def _evolution(entry):
    """One evolution as {method, level, item, into}; the arity varies."""
    method = entry[0] if isinstance(entry[0], str) else ""
    ints = [x for x in entry if isinstance(x, int) and not isinstance(x, bool)]
    item = next((x for x in entry if isinstance(x, str) and x.startswith("ITEM_")), None)
    into = next((x for x in entry if isinstance(x, str) and x.startswith("SPECIES_")), None)
    return {
        "method": _strip(method, "EVO_"),
        "level": ints[0] if method.startswith("EVO_LEVEL") and ints else None,
        "item": _strip(item, "ITEM_") if item else None,
        "into": into,
        "form": bool(into and _mega_of(into)),
    }


def delta(root, species, ref="main"):
    """What changed from vanilla: None for an unchanged species, {"new": True}
    for one this project added, otherwise only the fields that moved."""
    now = load(root, species)
    was = load(root, species, ref)
    if now is None:
        return None
    if was is None:
        return {"new": True}
    out = {}
    stats = {k: now["stats"][k] - was["stats"][k] for k in STAT_KEYS
             if now["stats"][k] != was["stats"][k]}
    if stats:
        out["stats"] = stats
        out["bst"] = now["bst"] - was["bst"]
    if now["types"] != was["types"]:
        out["types"] = {"was": was["types"], "now": now["types"]}
    if now["abilities"] != was["abilities"]:
        out["abilities"] = {"was": was["abilities"], "now": now["abilities"]}
    # Every native gained a hidden-ability slot in Phase 4, so a hidden ability
    # is only worth reporting as a change when there is one.
    if now["hidden_ability"] and not was["hidden_ability"]:
        out["hidden_ability"] = now["hidden_ability"]
    if now["evolutions"] != was["evolutions"]:
        out["evolutions"] = {"was": was["evolutions"], "now": now["evolutions"]}
    if now["learnset"] != was["learnset"]:
        out["learnset"] = True
    return out or None


@functools.lru_cache(maxsize=4)
def moves(root):
    """{MOVE_X: record} for every move in res/moves."""
    base = os.path.join(root, "res", "moves")
    out = {}
    for folder in sorted(os.listdir(base)):
        if not os.path.isdir(os.path.join(base, folder)):
            continue          # meson.build sits alongside the move folders
        raw = _read(root, f"res/moves/{folder}/data.json")
        if raw is None:
            continue
        out["MOVE_" + folder.upper()] = {
            "move": "MOVE_" + folder.upper(),
            "folder": folder,
            "name": raw.get("name") or folder.title(),
            "type": _strip(raw.get("type") or "", "TYPE_"),
            "class": _strip(raw.get("class") or "", "CLASS_"),
            "power": raw.get("power"),
            "accuracy": raw.get("accuracy"),
            "pp": raw.get("pp"),
            "priority": raw.get("priority"),
            "range": _strip(raw.get("range") or "", "RANGE_"),
            "flags": [_strip(f, "MOVE_FLAG_") for f in (raw.get("flags") or [])],
            "effect": _strip((raw.get("effect") or {}).get("type") or "",
                             "BATTLE_EFFECT_"),
            "effect_chance": (raw.get("effect") or {}).get("chance"),
            "description": "".join(raw.get("description") or []).strip(),
        }
    return out


# The chart lives in the battle code rather than in res/, as a flat list of
# (attacking type, defending type, multiplier) triples ended by 0xFF.
_ROW = re.compile(r"\{\s*(TYPE_\w+|0xFF)\s*,\s*(TYPE_\w+|0xFF)\s*,"
                  r"\s*(TYPE_MULTI_\w+|\d+)\s*\}")
_MULT = {"TYPE_MULTI_IMMUNE": 0.0, "TYPE_MULTI_NOT_VERY_EFF": 0.5,
         "TYPE_MULTI_SUPER_EFF": 2.0}


@functools.lru_cache(maxsize=4)
def type_chart(root):
    """{(attacking, defending): multiplier} for every entry that is not 1x.

    Worth knowing what this fork's chart actually is, because it is neither
    generation's: Fairy is in and complete, but Steel still resists Dark and
    Ghost, which Generation 6 removed. No stock setting in a damage calculator
    matches that, so the chart travels with the data.
    """
    with open(os.path.join(root, BATTLE_LIB), encoding="utf-8") as f:
        src = f.read()
    start = src.index("static const u8 sTypeMatchupMultipliers[][3] = {")
    body = src[start:src.index("};", start)]
    out = {}
    for atk, dfn, mul in _ROW.findall(body):
        if atk == "0xFF" or dfn == "0xFF":
            continue
        value = _MULT.get(mul)
        if value is None:
            value = int(mul) / 10
        out[(_strip(atk, "TYPE_"), _strip(dfn, "TYPE_"))] = value
    return out


def effectiveness(chart, attacking, defending):
    """The multiplier of one attacking type against one or two defending ones."""
    mult = 1.0
    for d in dict.fromkeys(defending):
        mult *= chart.get((attacking, d), 1.0)
    return mult


def sprites(root, species):
    """{kind: path relative to the repo} for the sprite files a species has."""
    folder = folder_of(species)
    out = {}
    for kind in SPRITES:
        rel = f"res/pokemon/{folder}/{kind}.png"
        if os.path.isfile(os.path.join(root, rel)):
            out[kind] = rel
    return out


def captures(ref=None):
    """{SPECIES_X: [appearance]} over every table, which is the cross-link the
    dex exists for: from a species, every table, kind, share and level it is in.

    Shares come from the table's own rates rather than from the archetype, so
    this describes the game rather than the design."""
    from . import analysis
    from . import locations
    from . import progression
    root = model.repo_root()
    sidecar = model.load_sidecar() or {}
    entries = sidecar.get("areas") or {}
    loc_of = locations.location_of(root)
    split_of = progression.split_of(sidecar)
    out = {}

    def note(species, row):
        out.setdefault(species, []).append(row)

    for area in model.load_all(ref):
        entry = entries.get(area.name) or {}
        common = {
            "area": area.name,
            "location": loc_of.get(area.name),
            "split": entry.get("split") or split_of.get(area.name),
        }
        if area.has_land and area.land_active:
            shares = analysis.merged(area.slots)
            levels = {}
            for species, level in area.slots:
                levels.setdefault(species, []).append(level)
            for species, share in shares.items():
                lv = levels.get(species) or [0]
                note(species, dict(common, kind="land", share=share,
                                   level_min=min(lv), level_max=max(lv)))
        for kind in ("surf", "old_rod", "good_rod", "super_rod"):
            rows = area.data.get(kind + "_encounters") or []
            if not rows or not area.kind_rate(kind):
                continue
            for i, row in enumerate(rows):
                if not row.get("species"):
                    continue
                note(row["species"], dict(
                    common, kind=kind, share=None,
                    level_min=row.get("level_min"), level_max=row.get("level_max")))
    return out

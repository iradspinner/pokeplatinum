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


def _mtime(path):
    try:
        return os.stat(path).st_mtime_ns
    except OSError:
        return None


# The readers below are cached, and each cache is keyed on the modification
# time of the files it read, so a species or move edited by hand while the
# server runs shows on the next request rather than after a restart. That
# matches the server's promise that nothing it shows is stale.
def species_list(root):
    """Every species with a folder, in the generated list's order (dex order)."""
    path = os.path.join(root, "generated", "species.txt")
    return _species_list(root, _mtime(path))


@functools.lru_cache(maxsize=4)
def _species_list(root, stamp):
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


def load(root, species, ref=None):
    """One species as the dex wants it, or None when the ref has no such file."""
    rel = f"res/pokemon/{folder_of(species)}/data.json"
    # A git ref never changes under us; the working tree can.
    stamp = _mtime(os.path.join(root, rel)) if ref is None else None
    return _load(root, species, ref, stamp)


@functools.lru_cache(maxsize=4096)
def _load(root, species, ref, stamp):
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
        "mega_of": _mega_of(root, species),
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
        "evolutions": [_evolution(root, e) for e in (raw.get("evolutions") or [])
                       if isinstance(e, list) and e],
        "learnset": [[lv, mv] for lv, mv in (learnset.get("by_level") or [])],
        "by_tm": learnset.get("by_tm") or [],
        "by_tutor": learnset.get("by_tutor") or [],
        "egg_moves": learnset.get("egg_moves") or [],
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


def _mega_of(root, species):
    """The species this is a mega of, or None. Megas are the base's constant
    with `_M`; a regional form is its own species with its own name, and a
    stage like Porygon-Z only looks like a suffix. The base has to exist:
    Nidoran's male constant ends in `_M` too, and there is no SPECIES_NIDORAN
    for it to be a mega of."""
    if not species.endswith("_M"):
        return None
    base = species[:-2]
    return base if base in set(species_list(root)) else None


def _evolution(root, entry):
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
        "form": bool(into and _mega_of(root, into)),
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


def moves(root):
    """{MOVE_X: record} for every move in res/moves."""
    base = os.path.join(root, "res", "moves")
    stamp = max((_mtime(os.path.join(base, f, "data.json")) or 0)
                for f in os.listdir(base))
    # The stub flag follows the effect scripts, so it is part of the key: a
    # script written while the server runs clears the flag on the next call.
    return _moves(root, stamp, stub_effects(root))


@functools.lru_cache(maxsize=4)
def _moves(root, stamp, stubs):
    base = os.path.join(root, "res", "moves")
    ids = _move_ids(root)
    effect_ids = _effect_ids(root)
    out = {}
    for folder in sorted(os.listdir(base)):
        if not os.path.isdir(os.path.join(base, folder)):
            continue          # meson.build sits alongside the move folders
        raw = _read(root, f"res/moves/{folder}/data.json")
        if raw is None:
            continue
        rec = _move_record(folder, raw)
        rec["id"] = ids.get(rec["move"])
        rec["effect_id"] = effect_ids.get(rec["effect"])
        rec["stub"] = rec["effect"] in stubs
        out[rec["move"]] = rec
    return out


def _move_record(folder, raw):
    """One move as the dex wants it, from its data.json. Shared by the working
    tree and the vanilla baseline, so the two compare field for field."""
    return {
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
        "description": " ".join(l.strip() for l in (raw.get("description") or [])
                                if l.strip()),
    }


def _lines(root, rel):
    with open(os.path.join(root, rel), encoding="utf-8") as f:
        return [l.strip() for l in f if l.strip()]


def _move_ids(root):
    """{MOVE_X: id}. The move enum is positional, one constant a line."""
    return {n: i for i, n in enumerate(_lines(root, "generated/moves.txt"))
            if n.startswith("MOVE_")}


def _effect_ids(root):
    """{EFFECT_NAME: id}, prefix stripped, from the positional effect list."""
    names = _lines(root, "generated/move_battle_effects.txt")
    return {_strip(n, "BATTLE_EFFECT_"): i for i, n in enumerate(names)}


# Platinum's own effects are 0 to 276. Phase 4 element 4 appended hg-engine's
# 277 to 406 with placeholder scripts, so a move using one does its damage and
# skips its extra, or says "But nothing happened!" if it is a status move.
FIRST_DONOR_EFFECT = 277
EFFECT_SCRIPTS = os.path.join("res", "battle", "scripts", "effects")
# Donor effects the engine carries out in C, for which a plain hit is the
# right script: the always-critical moves' crit is forced in battle_lib.c.
EFFECTS_DONE_IN_C = frozenset({"ALWAYS_CRITICAL"})


def stub_effects(root):
    """The donor effects whose script is still a placeholder.

    A placeholder is a copy of effect 0's script (a plain hit) or of
    BATTLE_EFFECT_DO_NOTHING's (Splash), which is exactly what element 4
    wrote into all 130 of them. Read from the scripts rather than listed, so
    an effect stops being flagged the moment its real script lands."""
    names = _lines(root, "generated/move_battle_effects.txt")
    base = os.path.join(root, EFFECT_SCRIPTS)
    stamp = max((_mtime(os.path.join(base, f)) or 0) for f in os.listdir(base))
    return _stub_effects(root, tuple(names), stamp)


@functools.lru_cache(maxsize=4)
def _stub_effects(root, names, stamp):
    def body(i):
        path = os.path.join(root, EFFECT_SCRIPTS, f"effect_script_{i:04d}.s")
        try:
            with open(path, encoding="utf-8") as f:
                return tuple(tuple(l.split()) for l in f if l.strip())
        except OSError:
            return None
    stubs = {body(0), body(names.index("BATTLE_EFFECT_DO_NOTHING"))}
    return frozenset(_strip(names[i], "BATTLE_EFFECT_")
                     for i in range(FIRST_DONOR_EFFECT, len(names))
                     if body(i) in stubs
                     and _strip(names[i], "BATTLE_EFFECT_") not in EFFECTS_DONE_IN_C)


# The abilities that set or cancel weather. The player never sets, changes or
# ends weather in Oxide, so no Pokemon the player can obtain may have one in a
# regular slot (Ian, 2026-09-26, staples survey). The hidden slot is allowed,
# since the game's one Ability Patch is the intended way to reach it. The
# main track's ability pass removes them; until then the tool flags them.
WEATHER_ABILITIES = ("DRIZZLE", "DROUGHT", "SAND_STREAM", "SNOW_WARNING", "SAND_SPIT",
                     "CLOUD_NINE", "AIR_LOCK", "PRIMORDIAL_SEA", "DESOLATE_LAND",
                     "DELTA_STREAM", "ORICHALCUM_PULSE")


def weather_abilities(root, species):
    """The weather abilities in a species' regular slots, empty for none."""
    rec = load(root, species)
    return [a for a in (rec or {}).get("abilities", []) if a in WEATHER_ABILITIES]


def vanilla_moves(root, ref="main"):
    """{MOVE_X: record} for every move a git ref has, read in one git call.

    One `git show` per move would be 923 processes for the list view, so the
    blobs are listed with ls-tree and read in a single cat-file batch."""
    sha = subprocess.run(["git", "-C", root, "rev-parse", "--verify", "-q", ref],
                         capture_output=True, text=True).stdout.strip()
    return _vanilla_moves(root, sha) if sha else {}


@functools.lru_cache(maxsize=2)
def _vanilla_moves(root, sha):
    listing = subprocess.run(
        ["git", "-C", root, "ls-tree", "-r", sha, "--", "res/moves"],
        capture_output=True, text=True).stdout
    blobs = []
    for line in listing.splitlines():
        meta, path = line.split("\t", 1)
        parts = path.split("/")
        if len(parts) == 4 and parts[3] == "data.json":
            blobs.append((meta.split()[2], parts[2]))
    batch = subprocess.run(["git", "-C", root, "cat-file", "--batch"],
                           input="".join(b + "\n" for b, _ in blobs).encode(),
                           capture_output=True).stdout
    out, at = {}, 0
    for _, folder in blobs:
        header_end = batch.index(b"\n", at)
        size = int(batch[at:header_end].split()[2])
        raw = json.loads(batch[header_end + 1:header_end + 1 + size])
        at = header_end + 1 + size + 1        # the content, then its newline
        rec = _move_record(folder, raw)
        out[rec["move"]] = rec
    return out


MOVE_FIELDS = ("name", "type", "class", "power", "accuracy", "pp", "priority",
               "range", "effect", "effect_chance", "description")


def move_delta(now, was):
    """What changed in one move: None when nothing did, {"new": True} for one
    this project added, otherwise {field: {"was", "now"}} and the flags each
    way. Takes both records so the list can compare 923 without re-reading."""
    if was is None:
        return {"new": True}
    out = {k: {"was": was[k], "now": now[k]} for k in MOVE_FIELDS
           if now[k] != was[k]}
    gained = sorted(set(now["flags"]) - set(was["flags"]))
    lost = sorted(set(was["flags"]) - set(now["flags"]))
    if gained or lost:
        out["flags"] = {"gained": gained, "lost": lost}
    return out or None


def machines(root):
    """{"TM02": MOVE_DRAGON_CLAW, ...}: a species' by_tm list names machines,
    and each machine's item record says what it teaches."""
    base = os.path.join(root, "res", "items", "data")
    out = {}
    for name in sorted(os.listdir(base)):
        if not re.fullmatch(r"(tm|hm)\d+\.json", name):
            continue
        raw = _read(root, f"res/items/data/{name}") or {}
        if raw.get("teachesMove"):
            out[name[:-5].upper()] = raw["teachesMove"]
    return out


LEARN_KINDS = ("level", "machine", "tutor", "egg")


def learners(root):
    """{MOVE_X: [{species, how, level, machine}]}: the reverse of every
    species' learnset, by level-up, machine, tutor and egg.

    Built from `load`, whose cache follows each species file, so an edited
    learnset shows here on the next call as it does on the species page."""
    by_machine = machines(root)
    out = {}

    def add(move, species, how, level=None, machine=None):
        out.setdefault(move, []).append(
            {"species": species, "how": how, "level": level, "machine": machine})

    for species in species_list(root):
        rec = load(root, species)
        if rec is None:
            continue
        for level, move in rec["learnset"]:
            add(move, species, "level", level=level)
        for machine in rec["by_tm"]:
            if machine in by_machine:
                add(by_machine[machine], species, "machine", machine=machine)
        for move in rec["by_tutor"]:
            add(move, species, "tutor")
        for move in rec["egg_moves"]:
            add(move, species, "egg")
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
    Ghost, which Generation 6 removed. That is deliberate (Ian, 2026-09-22).
    No stock setting in a damage calculator matches it, so the chart travels
    with the data.
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

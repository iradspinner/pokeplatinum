#!/usr/bin/env python3
"""Carry species, move, trainer, encounter and npc-trade edits from a modified
Platinum ROM into this source tree.

Platinum Oxide project. The "base" ROM is Ian's earlier DSPRE-edited
Platinum; the "vanilla" ROM is the one this tree builds unmodified. For every
species and move whose binary record differs between the two, the differing
fields are written into the matching res/pokemon/<name>/data.json or
res/moves/<name>/data.json. Only the keys that changed are rewritten, so the
git diff shows exactly the edits and nothing else.

Usage:
    python3 tools/oxide/import_base_rom.py --base BASE.nds --vanilla VANILLA.nds [--dry-run]

Run from the repository root. Requires ndspy (pip install ndspy).
After running, rebuild and check with tools/oxide/verify_narcs.py.
"""
import argparse
import json
import os
import struct
import sys

import ndspy.narc
import ndspy.rom

sys.path.insert(0, os.path.dirname(__file__))
import jsonstyle  # noqa: E402

ROOT = os.getcwd()


# ---------------------------------------------------------------- name tables
_ENUM_CACHE = {}


def load_enum(name):
    """Value -> NAME for a generated enum. Reads build/generated/<name>.h
    (which carries the exact values, including bit-mask enums such as move
    ranges) and falls back to generated/<name>.txt (sequential values)."""
    import re
    if name in _ENUM_CACHE:
        return _ENUM_CACHE[name]
    header = os.path.join(ROOT, "build", "generated", name + ".h")
    table = {}
    if os.path.exists(header):
        body = open(header).read()
        m = re.search(r"enum \w+ \{(.*?)\};", body, re.S)
        for line in m.group(1).splitlines():
            # lowercase matters: plenty of generated names carry a hex suffix,
            # FLAG_UNK_0x0A8D and VAR_MAP_LOCAL_0x01 among them, and an
            # uppercase-only pattern drops them from the value-to-name map
            mm = re.match(r"\s*([A-Za-z0-9_]+)\s*=\s*(.+?),?\s*$", line)
            if mm:
                # evaluated against the members already seen, never this
                # module's namespace, so an alias resolves and a surprise raises
                table[eval(mm.group(2), {"__builtins__": {}}, {v: k for k, v in table.items()})] = mm.group(1)
        if table:
            _ENUM_CACHE[name] = table
            return table
    with open(os.path.join(ROOT, "generated", name + ".txt")) as f:
        for i, line in enumerate(l.strip() for l in f):
            if not line:
                continue
            if "=" in line:
                k, v = (x.strip() for x in line.split("=", 1))
                table[int(v, 0)] = k
            else:
                table[i] = line
    _ENUM_CACHE[name] = table
    return table


_ENUM_VALUE_CACHE = {}


def load_enum_values(name):
    """NAME -> value for a generated enum. load_enum() maps the other way and
    so loses aliases, which vars_flags has plenty of: VAR_MAP_LOCAL_0x00 and
    MAP_LOCAL_VARS_START are the same number. Values are evaluated against the
    members already parsed and nothing else, so an entry defined in terms of an
    earlier one resolves and anything stranger raises instead of reaching into
    this module's namespace."""
    import re
    if name in _ENUM_VALUE_CACHE:
        return _ENUM_VALUE_CACHE[name]
    header = os.path.join(ROOT, "build", "generated", name + ".h")
    body = open(header).read()
    found = re.search(r"enum \w+ \{(.*?)\};", body, re.S)
    table = {}
    for line in found.group(1).splitlines():
        entry = re.match(r"\s*([A-Za-z0-9_]+)\s*=\s*(.+?),?\s*$", line)
        if entry:
            table[entry.group(1)] = eval(entry.group(2), {"__builtins__": {}}, dict(table))
    _ENUM_VALUE_CACHE[name] = table
    return table


SPECIES = load_enum("species")
TRAINERS = load_enum("trainers")
TRAINER_CLASSES = load_enum("trainer_classes")
AI_FLAGS = load_enum("ai_flags")
ITEMS = load_enum("items")
MOVES = load_enum("moves")
TYPES = load_enum("pokemon_types")
ABILITIES = load_enum("abilities")
EGG_GROUPS = load_enum("egg_groups")
EXP_RATES = load_enum("exp_rates")
GENDER_RATIOS = load_enum("gender_ratios")
COLORS = load_enum("pokemon_colors")
EVO_METHODS = load_enum("evolution_methods")
MOVE_EFFECTS = load_enum("move_battle_effects")
MOVE_CLASSES = load_enum("move_classes")
MOVE_RANGES = load_enum("move_ranges")
MOVE_FLAGS = load_enum("move_flags")
CONTEST_EFFECTS = load_enum("move_contest_effects")
CONTEST_TYPES = load_enum("pokemon_contest_types")
GENDERS = load_enum("genders")

# include/constants/versions.h; not a generated enum, so it is spelled out here
LANGUAGES = {
    0: "LANGUAGE_NONE", 1: "LANGUAGE_JAPANESE", 2: "LANGUAGE_ENGLISH",
    3: "LANGUAGE_FRENCH", 4: "LANGUAGE_ITALIAN", 5: "LANGUAGE_GERMAN",
    6: "LANGUAGE_UNUSED_6", 7: "LANGUAGE_SPANISH", 8: "LANGUAGE_KOREAN",
}

NUM_TMS = 92  # include/constants/items.h: TM01..TM92, HM01..HM08

# Alternate forms that have their own personal/learnset/evolution records,
# in NARC order after SPECIES_BAD_EGG (495). Mirrors alt_forms_with_data[] in
# tools/dataproc/src/speciesproc.c.
ALT_FORMS = [
    "deoxys/forms/attack", "deoxys/forms/defense", "deoxys/forms/speed",
    "wormadam/forms/sandy", "wormadam/forms/trash",
    "giratina/forms/origin", "shaymin/forms/sky",
    "rotom/forms/heat", "rotom/forms/wash", "rotom/forms/frost",
    "rotom/forms/fan", "rotom/forms/mow",
]


def species_dir(index):
    """Path under res/pokemon for a personal-NARC index, or None."""
    if index == 0:
        return None
    if index <= 493:
        name = SPECIES[index][len("SPECIES_"):].lower()
        # folder names use underscores and drop punctuation (mr_mime, farfetchd, ho_oh, nidoran_f)
        fixed = {"nidoran_f": "nidoran_f", "nidoran_m": "nidoran_m"}
        name = fixed.get(name, name)
        path = os.path.join(ROOT, "res", "pokemon", name)
        if not os.path.isdir(path):
            raise FileNotFoundError(f"no species folder for index {index} ({name})")
        return path
    if index in (494, 495):
        return None  # egg, bad egg
    alt = index - 496
    if 0 <= alt < len(ALT_FORMS):
        return os.path.join(ROOT, "res", "pokemon", ALT_FORMS[alt])
    return None


def move_dir(index):
    if index == 0:
        return None
    name = MOVES.get(index)
    if name is None:
        return None
    path = os.path.join(ROOT, "res", "moves", name[len("MOVE_"):].lower())
    return path if os.path.isdir(path) else None


def encounter_json(index):
    """Path under res/field/encounters for a pl_enc_data.narc member index.
    encounters.order is the authority on that mapping: line N names member N."""
    global _ENC_ORDER
    if _ENC_ORDER is None:
        path = os.path.join(ROOT, "res", "field", "encounters", "encounters.order")
        _ENC_ORDER = [l.strip() for l in open(path) if l.strip()]
    if index >= len(_ENC_ORDER):
        return None
    path = os.path.join(ROOT, "res", "field", "encounters", _ENC_ORDER[index] + ".json")
    return path if os.path.isfile(path) else None


_ENC_ORDER = None

# enum NPCTradeID in include/constants/npc_trades.h, which is also the order
# npctradeproc packs npc_trades.narc in
NPC_TRADES = ["kazza_abra", "charap_chatot", "gaspar_haunter", "foppa_magikarp"]


def trade_json(index):
    if index >= len(NPC_TRADES):
        return None
    path = os.path.join(ROOT, "res", "npc_trades", NPC_TRADES[index] + ".json")
    return path if os.path.isfile(path) else None


def item_json(index):
    name = ITEMS.get(index)
    if name is None:
        return None
    path = os.path.join(ROOT, "res", "items", "data", name[len("ITEM_"):].lower() + ".json")
    return path if os.path.isfile(path) else None


def trainer_json(index):
    name = TRAINERS.get(index)
    if name is None:
        return None
    path = os.path.join(ROOT, "res", "trainers", "data", name[len("TRAINER_"):].lower() + ".json")
    return path if os.path.isfile(path) else None


# ---------------------------------------------------------------- ROM access
def walk(folder, prefix=""):
    out = {}
    for i, name in enumerate(folder.files):
        out[prefix + name] = folder.firstID + i
    for sub, f in folder.folders:
        out.update(walk(f, prefix + sub + "/"))
    return out


class Rom:
    def __init__(self, path):
        self.rom = ndspy.rom.NintendoDSRom.fromFile(path)
        self.names = walk(self.rom.filenames)
        self.arm9 = self.rom.arm9

    def narc(self, path):
        return ndspy.narc.NARC(self.rom.files[self.names[path]]).files


# ---------------------------------------------------------------- decoders
def decode_personal(b):
    (hp, atk, dfn, spe, spa, spd, t1, t2, catch, bexp, ev, item1, item2,
     gender, hatch, friend, growth, egg1, egg2, ab1, ab2, flee, colorflip) = \
        struct.unpack_from("<6B2BBBH2H4B2B2BBB", b, 0)
    tm = struct.unpack_from("<4I", b, 28)
    by_tm = []
    for idx in range(4):
        for bit in range(32):
            if tm[idx] & (1 << bit):
                v = idx * 32 + bit
                by_tm.append(f"HM{v - NUM_TMS + 1:02d}" if v >= NUM_TMS else f"TM{v + 1:02d}")
    return {
        "base_stats": {"hp": hp, "attack": atk, "defense": dfn, "speed": spe,
                       "special_attack": spa, "special_defense": spd},
        "types": [TYPES[t1], TYPES[t2]],
        "catch_rate": catch,
        "base_exp_reward": bexp,
        "ev_yields": {"hp": ev & 3, "attack": (ev >> 2) & 3, "defense": (ev >> 4) & 3,
                      "speed": (ev >> 6) & 3, "special_attack": (ev >> 8) & 3,
                      "special_defense": (ev >> 10) & 3},
        "held_items": {"common": ITEMS[item1], "rare": ITEMS[item2]},
        "gender_ratio": GENDER_RATIOS[gender],
        "hatch_cycles": hatch,
        "base_friendship": friend,
        "exp_rate": EXP_RATES[growth],
        "egg_groups": [EGG_GROUPS[egg1], EGG_GROUPS[egg2]],
        "abilities": [ABILITIES[ab1], ABILITIES[ab2]],
        "safari_flee_rate": flee,
        "body_color": COLORS[colorflip & 0x7F],
        "flip_sprite": bool(colorflip >> 7),
        "learnset.by_tm": by_tm,
    }


def decode_learnset(b):
    out = []
    for off in range(0, len(b) - 1, 2):
        v = struct.unpack_from("<H", b, off)[0]
        if v == 0xFFFF:
            break
        out.append([v >> 9, MOVES[v & 0x1FF]])
    return out


LEVEL_PARAM = {"EVO_LEVEL", "EVO_LEVEL_ATK_GT_DEF", "EVO_LEVEL_ATK_EQ_DEF", "EVO_LEVEL_ATK_LT_DEF",
               "EVO_LEVEL_PID_LOW", "EVO_LEVEL_PID_HIGH", "EVO_LEVEL_NINJASK", "EVO_LEVEL_SHEDINJA",
               "EVO_LEVEL_BEAUTY", "EVO_LEVEL_MALE", "EVO_LEVEL_FEMALE"}
ITEM_PARAM = {"EVO_TRADE_WITH_HELD_ITEM", "EVO_USE_ITEM", "EVO_USE_ITEM_MALE", "EVO_USE_ITEM_FEMALE",
              "EVO_LEVEL_WITH_HELD_ITEM_DAY", "EVO_LEVEL_WITH_HELD_ITEM_NIGHT"}


def decode_evolutions(b):
    out = []
    for i in range(7):
        method, param, target = struct.unpack_from("<3H", b, i * 6)
        if method == 0:
            continue
        m = EVO_METHODS[method]
        if m in LEVEL_PARAM:
            out.append([m, param, SPECIES[target]])
        elif m in ITEM_PARAM:
            out.append([m, ITEMS[param], SPECIES[target]])
        elif m == "EVO_LEVEL_KNOW_MOVE":
            out.append([m, MOVES[param], SPECIES[target]])
        elif m == "EVO_LEVEL_SPECIES_IN_PARTY":
            out.append([m, SPECIES[param], SPECIES[target]])
        else:
            out.append([m, SPECIES[target]])
    return out


def decode_move(b):
    effect, cls, power, typ, acc, pp, chance, rng, prio, flags, ceff, ctype = \
        struct.unpack_from("<HBBBBBBHbBBB", b, 0)
    return {
        "class": MOVE_CLASSES[cls],
        "type": TYPES[typ],
        "power": power,
        "accuracy": acc,
        "pp": pp,
        "effect": {"type": MOVE_EFFECTS[effect], "chance": chance},
        "range": MOVE_RANGES[rng],
        "priority": prio,
        "flags": [MOVE_FLAGS[1 << i] for i in range(8) if flags & (1 << i)],
        "contest": {"effect": CONTEST_EFFECTS[ceff], "type": CONTEST_TYPES[ctype]},
    }


BATTLE_TYPE_DOUBLES = 1 << 1  # include/constants/battle.h

# monDataType -> (struct format for one TrainerMon record, has_item, has_moves)
# matches include/struct_defs/trainer_data.h's four TrainerMon* variants
TRAINER_MON_FORMATS = {
    0: ("<4H", False, False),  # TrainerMonBase: ivScale, level, species, cbSeal
    1: ("<8H", False, True),   # TrainerMonWithMoves: + moves[4]
    2: ("<5H", True, False),   # TrainerMonWithItem: + item
    3: ("<9H", True, True),    # TrainerMonWithMovesAndItem: + item, moves[4]
}


def decode_trainer_header(b):
    monDataType, trainerType, _sprite, partySize = struct.unpack_from("<4B", b, 0)
    items = struct.unpack_from("<4H", b, 4)
    aiMask, battleType = struct.unpack_from("<2I", b, 12)
    header = {
        "class": TRAINER_CLASSES[trainerType],
        "items": [ITEMS[i] for i in items if i != 0],
        "ai_flags": [AI_FLAGS[1 << bit] for bit in range(32) if aiMask & (1 << bit)],
        "double_battle": bool(battleType & BATTLE_TYPE_DOUBLES),
    }
    return header, monDataType, partySize


def decode_trainer_party(buf, partySize, monDataType):
    """Decode a trainer's party. ivScale's low byte is iv_scale as vanilla
    uses it; the base ROM's DSPRE-compiled patch repurposed the high byte's
    two nibbles as {high nibble: force ability slot 1/2, low nibble: force
    gender}, per docs/oxide/phase3-answers-and-trainer-format.md section 2.
    Which raw nibble value (1 or 2) means male vs female could not be
    recovered from the ROM bytes (the compiled patch's bug made both behave
    identically in-game); 1=male, 2=female is Ian's own best guess (2026-09-15),
    to revisit if anything reads wrong in-game."""
    fmt, has_item, has_moves = TRAINER_MON_FORMATS[monDataType]
    mon_size = struct.calcsize(fmt)
    mons = []
    for i in range(partySize):
        vals = struct.unpack_from(fmt, buf, i * mon_size)
        pos = 0
        ivScale = vals[pos]; pos += 1
        level = vals[pos]; pos += 1
        speciesRaw = vals[pos]; pos += 1
        item = None
        if has_item:
            item = vals[pos]; pos += 1
        moves = None
        if has_moves:
            moves = vals[pos:pos + 4]; pos += 4
        cbSeal = vals[pos]

        low = ivScale & 0xFF
        high = (ivScale >> 8) & 0xFF
        ability_nibble = (high >> 4) & 0xF
        gender_nibble = high & 0xF

        mons.append({
            "species": SPECIES[speciesRaw & 0x3FF],
            "form": (speciesRaw >> 10) & 0x3F,
            "level": level,
            "item": ITEMS[item] if has_item else None,
            "moves": [MOVES[m] for m in moves] if has_moves else None,
            "iv_scale": low,
            "ball_seal": cbSeal,
            "ability": ability_nibble if ability_nibble in (1, 2) else 0,
            "gender": {1: "male", 2: "female"}.get(gender_nibble),
        })
    return mons


def decode_encounter(b):
    """tools/jsoncnv/encounter.py run backwards. The JSON's map_category block
    is not part of the 424-byte packed record, so nothing here touches it."""
    o = 0

    def u32():
        nonlocal o
        v = struct.unpack_from("<I", b, o)[0]
        o += 4
        return v

    def species():
        return SPECIES[u32()]

    def water():
        nonlocal o
        out = []
        for _ in range(5):
            level_max, level_min = struct.unpack_from("<2B", b, o)
            o += 4  # the two levels are followed by two bytes of padding
            out.append({"level_max": level_max, "level_min": level_min, "species": species()})
        return out

    d = {"land_rate": u32()}
    d["land_encounters"] = [{"level": u32(), "species": species()} for _ in range(12)]
    for key in ("swarms", "day", "night"):
        d[key] = [species() for _ in range(2)]
    d["radar"] = [species() for _ in range(4)]
    for key in ("rate_form0", "rate_form1", "rate_form2", "rate_form3", "rate_form4", "unown_table"):
        d[key] = u32()
    for key in ("ruby", "sapphire", "emerald", "firered", "leafgreen"):
        d[key] = [species() for _ in range(2)]
    d["surf_rate"] = u32()
    d["surf_encounters"] = water()
    o += 44  # unused block between the surf and rod tables
    for rod in ("old", "good", "super"):
        d[f"{rod}_rod_rate"] = u32()
        d[f"{rod}_rod_encounters"] = water()

    assert o == len(b), f"encounter record is {len(b)} bytes, decoder read {o}"
    return d


# Fields decoded from the encounter record but deliberately not carried over.
# DSPRE rewrites both of them on every table it saves, whether or not the map
# has anything that reads them, and the rewrite is not value-preserving:
#
#   unown_table: 98 tables go 0 -> 1, which the game reads identically
#     (WildEncounters_TrySetForm subtracts one from any non-zero value), so those
#     are pure noise. The 17 that change for real are every room in Solaceon
#     Ruins, all set to 8. Table 8 is UnownOnlyExcQue, the two-form secret-room
#     set, so importing this would leave the whole ruins spawning only Unown !
#     and ? and make the F-R-I-E-N-D letters and the 20-form dead-end group
#     unobtainable. That is a tool default, not a design choice.
#
#   rate_form0/rate_form1: pick the Shellos and Gastrodon form (west/east), read
#     as a boolean. Vanilla stores 100 on most tables; the base ROM has 34 going
#     to 1 (same meaning) and 29 to 0 (opposite meaning). Of those 29, exactly
#     two are maps that contain Shellos or Gastrodon at all (Route 212 north and
#     south), which reads as a checkbox being normalised rather than two maps
#     being deliberately flipped to the west form.
#
# rate_form2..4 are unused by the game and move with the other two.
ENCOUNTER_SKIP_KEYS = ("unown_table", "rate_form0", "rate_form1", "rate_form2", "rate_form3", "rate_form4")

# Encounter files the authoring pass has rewritten from the species pick-list
# (docs/oxide/encounter-authoring-plan.md). The base ROM's table is no longer
# the truth for these, so the importer must not carry it back over them; the
# dry run reports them as "authored, skipped" and does not count them. Mirrors
# bulk_scripts.py's DIVERGED: stem -> why. Any area whose sidecar entry
# (docs/oxide/encounters/design.json) carries a `cast` is authored by
# definition and is added automatically by authored_encounters(), so this
# literal set is only for tables authored outside the sidecar.
AUTHORED = {
}


def authored_encounters():
    """{stem: reason} for every encounter file the importer must leave alone:
    AUTHORED plus every sidecar area with a cast."""
    out = dict(AUTHORED)
    path = os.path.join(ROOT, "docs", "oxide", "encounters", "design.json")
    try:
        with open(path, encoding="utf-8") as f:
            areas = json.load(f).get("areas") or {}
    except (FileNotFoundError, ValueError):
        areas = {}
    for name, entry in areas.items():
        if entry.get("cast"):
            out.setdefault(name, "authored from the pick-list (sidecar entry has a cast)")
    return out


TRADE_FIELDS = [
    ("species", SPECIES), ("hpIV", None), ("atkIV", None), ("defIV", None),
    ("speedIV", None), ("spAtkIV", None), ("spDefIV", None), ("unused1", None),
    ("otID", None), ("cool", None), ("beauty", None), ("cute", None),
    ("smart", None), ("tough", None), ("personality", None), ("heldItem", ITEMS),
    ("otGender", GENDERS), ("unused2", None), ("language", LANGUAGES),
    ("requestedSpecies", SPECIES),
]


def decode_trade(b):
    """NPCTradeMon (include/overlay006/npc_trade.h): 20 u32 fields, in the same
    order the res/npc_trades/*.json files list them."""
    vals = struct.unpack_from("<20I", b, 0)
    return {name: (table[v] if table else v) for (name, table), v in zip(TRADE_FIELDS, vals)}


# ---------------------------------------------------------------- apply
def flatten(d, prefix=""):
    """{'a': {'b': 1}} -> {'a.b': 1}, but lists stay whole."""
    out = {}
    for k, v in d.items():
        key = f"{prefix}{k}"
        if isinstance(v, dict):
            out.update(flatten(v, key + "."))
        else:
            out[key] = v
    return out


def apply_diff(json_path, new, old, dry_run, log):
    """Write every key whose decoded value differs between new and old."""
    text = open(json_path, encoding="utf-8").read()
    fn, fo = flatten(new), flatten(old)
    changed = []
    for key, val in fn.items():
        if fo.get(key) == val:
            continue
        path = key.split(".")
        current = jsonstyle.get_value(text, path)
        if current == val:
            continue
        text = jsonstyle.replace_value(text, path, val)
        changed.append(f"{key}: {fo.get(key)!r} -> {val!r}")
    if changed:
        rel = os.path.relpath(json_path, ROOT)
        log.append((rel, changed))
        if not dry_run:
            with open(json_path, "w", encoding="utf-8", newline="\n") as f:
                f.write(text)
    return bool(changed)


def scalar_paths(obj, prefix=()):
    """Yield (path, value) for every scalar leaf, descending into lists as well
    as dicts so a list element is reached by index. flatten() deliberately stops
    at a list and treats it as one value; records that are mostly arrays
    (encounters, npc trades) need the finer grain to keep diffs small."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield from scalar_paths(v, prefix + (k,))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from scalar_paths(v, prefix + (i,))
    else:
        yield list(prefix), obj


def apply_scalar_diff(json_path, new, old, dry_run, log):
    """apply_diff's array-aware sibling: patches one number or name at a time,
    wherever it sits in the record, and never rewrites a whole list."""
    text = open(json_path, encoding="utf-8").read()
    olds = {tuple(p): v for p, v in scalar_paths(old)}
    changed = []
    for path, val in scalar_paths(new):
        if olds.get(tuple(path)) == val:
            continue
        if jsonstyle.get_value(text, path) == val:
            continue
        text = jsonstyle.replace_value(text, path, val)
        pretty = ".".join(str(p) for p in path)
        changed.append(f"{pretty}: {olds.get(tuple(path))!r} -> {val!r}")
    if changed:
        rel = os.path.relpath(json_path, ROOT)
        log.append((rel, changed))
        if not dry_run:
            with open(json_path, "w", encoding="utf-8", newline="\n") as f:
                f.write(text)
    return bool(changed)


def apply_trainer_diff(json_path, new_header, new_party, old_header, old_party, dry_run, log):
    """Like apply_diff, but for trainers: `party` is a list of objects, which
    the flatten()-based apply_diff can't reach into (it treats any list as
    one opaque value), so per-mon fields are patched individually here, and
    `ability`/`gender` are inserted as new keys the first time either is
    needed. When the party size itself changed, the whole array is rewritten
    at once instead (see below)."""
    text = open(json_path, encoding="utf-8").read()
    changed = []
    rel = os.path.relpath(json_path, ROOT)

    fn, fo = flatten(new_header), flatten(old_header)
    for key, val in fn.items():
        if fo.get(key) == val:
            continue
        path = key.split(".")
        if jsonstyle.get_value(text, path) == val:
            continue
        text = jsonstyle.replace_value(text, path, val)
        changed.append(f"{key}: {fo.get(key)!r} -> {val!r}")

    if len(new_party) != len(old_party):
        # Party size changed, so this isn't a per-field patch anymore - rewrite
        # the whole array. jsonstyle.dumps() round-trips this repo's party
        # arrays byte-for-byte in the overwhelming majority of cases (checked
        # against all 928 trainer files); the one known miss is a 2-element
        # "moves" list, which this repo always hand-formats one-per-line but
        # dumps() inlines (its general "<=2 scalars" rule). Still valid JSON,
        # just occasionally not matching this file's existing hand style.
        current = jsonstyle.get_value(text, ["party"])
        if current != new_party:
            text = jsonstyle.replace_value(text, ["party"], new_party)
            changed.append(f"party: {len(old_party)} -> {len(new_party)} mons (full rewrite, size changed)")
    else:
        for i, (nm, om) in enumerate(zip(new_party, old_party)):
            for key in ("species", "form", "level", "item", "moves", "iv_scale", "ball_seal"):
                val = nm[key]
                if om.get(key) == val:
                    continue
                path = ["party", i, key]
                if jsonstyle.get_value(text, path) == val:
                    continue
                text = jsonstyle.replace_value(text, path, val)
                changed.append(f"party[{i}].{key}: {om.get(key)!r} -> {val!r}")

            if nm["ability"] != om.get("ability", 0) or nm["gender"] != om.get("gender"):
                try:
                    jsonstyle.get_value(text, ["party", i, "ability"])
                except KeyError:
                    text = jsonstyle.insert_key(text, ["party", i], "ball_seal", "ability", 0)
                    text = jsonstyle.insert_key(text, ["party", i], "ability", "gender", None)
                # the outer test compares the base ROM against vanilla, which never
                # carries either field, so it fires on every mon that has one even
                # when this file already holds the right value. Only report what
                # actually gets written.
                wrote = False
                if jsonstyle.get_value(text, ["party", i, "ability"]) != nm["ability"]:
                    text = jsonstyle.replace_value(text, ["party", i, "ability"], nm["ability"])
                    wrote = True
                if jsonstyle.get_value(text, ["party", i, "gender"]) != nm["gender"]:
                    text = jsonstyle.replace_value(text, ["party", i, "gender"], nm["gender"])
                    wrote = True
                if wrote:
                    changed.append(f"party[{i}].ability/gender: {om.get('ability')!r}/{om.get('gender')!r} "
                                    f"-> {nm['ability']!r}/{nm['gender']!r}")

    if changed:
        log.append((rel, changed))
        if not dry_run:
            with open(json_path, "w", encoding="utf-8", newline="\n") as f:
                f.write(text)
    return bool(changed)


# ---------------------------------------------------------------- map events
#
# zone_event.narc holds one record per map: four length-prefixed arrays of
# background events (20 bytes each), object events (32), warps (12) and coord
# events (16). tools/jsoncnv/event.py packs them; this decodes them back.
#
# An object event's first field is its local id, which event.py writes as the
# array index unless the JSON overrides it with clone_id. The `id` string beside
# it is not packed: it names the LOCALID_* constant that
# res/field/events/events_<map>.h generates for the scripts to use. New objects
# imported here therefore need a name, and the name has to mean something to
# whoever writes the script that talks to them, so they are given a descriptive
# placeholder and listed in the report.
EVENTS_NARC = "fielddata/eventdata/zone_event.narc"
EVENTS_DIR = os.path.join("res", "field", "events")

BG_EVENT_DIRS = {}
MOVEMENT_TYPES = None
OBJECT_EVENT_GFX = None
TRAINER_TYPES = None
VARS_FLAGS = None


def _event_enums():
    global BG_EVENT_DIRS, MOVEMENT_TYPES, OBJECT_EVENT_GFX, TRAINER_TYPES, VARS_FLAGS
    if MOVEMENT_TYPES is None:
        BG_EVENT_DIRS = load_enum("bg_event_dirs")
        MOVEMENT_TYPES = load_enum("movement_types")
        OBJECT_EVENT_GFX = load_enum("object_events_gfx")
        TRAINER_TYPES = load_enum("trainer_types")
        VARS_FLAGS = load_enum("vars_flags")


def trim_trailing_zeros(values):
    """event.py pads an object event's data up to three on the way out, so the
    repo's files only spell out the entries that carry something."""
    out = list(values)
    while out and out[-1] == 0:
        out.pop()
    return out


def decode_script_ref(value):
    """event.py's from_script() in reverse: a trainer object stores its trainer
    id offset by 3000, or 5000 for the second trainer in a double battle.
    Anything else is a plain script number."""
    for base_, double in ((5000, 2), (3000, 1)):
        if base_ <= value < base_ + 1000:
            name = TRAINERS.get(value - base_ + 1)
            if name is not None:
                return name, double
    return value, None


def decode_events(buf):
    _event_enums()
    o = 0

    def take(fmt):
        nonlocal o
        vals = struct.unpack_from(fmt, buf, o)
        o += struct.calcsize(fmt)
        return vals

    d = {}
    (count,) = take("<I")
    d["bg_events"] = []
    for _ in range(count):
        script, type_, x, z, y, facing = take("<HHIIIH")
        o += 2  # padding
        d["bg_events"].append({"script": script, "type": type_, "x": x, "z": z, "y": y,
                               "player_facing_dir": BG_EVENT_DIRS[facing]})

    (count,) = take("<I")
    d["object_events"] = []
    for i in range(count):
        (clone_id, gfx, movement, trainer_type, hidden, script, initial_dir,
         d0, d1, d2, range_x, range_z, x, z, y) = take("<14HI")
        script_val, double = decode_script_ref(script)
        obj = {
            "graphics_id": OBJECT_EVENT_GFX[gfx],
            "movement_type": MOVEMENT_TYPES[movement],
            "trainer_type": TRAINER_TYPES[trainer_type],
            # left numeric on purpose: event.py's from_var_flag_or_map_header
            # accepts either a VarFlag or a MapHeaderID name here, and the two
            # enums overlap, so a number cannot be turned back into the right
            # name without looking at what the file already says. Comparison and
            # rendering both happen in apply_events_diff.
            "hidden_flag": hidden,
            "script": script_val,
            "initial_dir": initial_dir,
            "data": trim_trailing_zeros([d0, d1, d2]),
            "movement_range_x": range_x,
            "movement_range_z": range_z,
            "x": x, "z": z, "y": y // 0x10000,
        }
        if double == 2:
            obj["double_battle_id"] = 2
        if clone_id != i:
            obj["clone_id"] = clone_id
        d["object_events"].append(obj)

    (count,) = take("<I")
    d["warp_events"] = []
    for _ in range(count):
        x, z, dest_header, dest_warp = take("<4H")
        o += 4  # padding
        d["warp_events"].append({"x": x, "z": z,
                                 "dest_header_id": load_enum("map_headers")[dest_header],
                                 "dest_warp_id": dest_warp})

    (count,) = take("<I")
    d["coord_events"] = []
    for _ in range(count):
        script, x, z, width, length, y, value, var = take("<8H")
        d["coord_events"].append({"script": script, "x": x, "z": z, "width": width,
                                  "length": length, "y": y, "value": value,
                                  "var": var})  # numeric, as hidden_flag above

    assert o == len(buf), f"event record is {len(buf)} bytes, decoder read {o}"
    return d


def render_var_or_header(value, current):
    """Spell a hidden_flag or coord var the way this file already spells that
    kind of field: as a var/flag name, or a map header name, or a bare 0."""
    _event_enums()
    if value == 0:
        return "0"
    if isinstance(current, str) and current.startswith("MAP_HEADER_"):
        return load_enum("map_headers").get(value, value)
    return VARS_FLAGS.get(value, value)


def var_or_header_value(current):
    """The number `current` stands for, whichever enum it came from."""
    _event_enums()
    if current == "0" or current == 0:
        return 0
    if isinstance(current, int):
        return current
    if current.startswith("MAP_HEADER_"):
        return load_enum_values("map_headers")[current]
    return load_enum_values("vars_flags")[current]


def events_json(index):
    global _EVENT_ORDER
    if _EVENT_ORDER is None:
        path = os.path.join(ROOT, EVENTS_DIR, "zone_event.order")
        _EVENT_ORDER = [l.strip() for l in open(path) if l.strip()]
    if index >= len(_EVENT_ORDER):
        return None
    path = os.path.join(ROOT, EVENTS_DIR, _EVENT_ORDER[index] + ".json")
    return path if os.path.isfile(path) else None


_EVENT_ORDER = None


def events_to_scripts(van_arm9):
    """events archive id -> the script archive ids of every map header that uses
    it. Matching events to scripts by filename looks right and is not: a handful
    of maps, Mt Coronet's among them, do not line up by name."""
    count = sum(1 for line in open(os.path.join(ROOT, MAP_HEADERS_H))
                if line.startswith("    [MAP_HEADER_"))
    off = find_map_header_table(van_arm9, count)
    pairs = {}
    for i in range(count):
        h = decode_map_header(van_arm9[off + i * MAP_HEADER_SIZE: off + (i + 1) * MAP_HEADER_SIZE])
        pairs.setdefault(h["eventsArchiveID"], set()).add(h["scriptsArchiveID"])
    return pairs


def import_events(base, van, dry_run, log):
    """Carry over the event edits that stand on their own.

    A map is only touched when its script file is unchanged, its arrays are the
    same length, and every script id its events point at already exists. That
    leaves in-place edits to existing objects, which is what most of these are:
    the base ROM mostly re-itemises the balls lying around the overworld, and a
    ball's script id is SCRIPT_ID_OFFSET_VISIBLE_ITEMS plus an index.

    Anything else is left for the per-map carry-over, because a new object event
    is an NPC that needs a LOCALID name and a script to run."""
    import scriptdis
    be, ve = base.narc(EVENTS_NARC), van.narc(EVENTS_NARC)
    bs, vs = base.narc(scriptdis.SCRIPTS_NARC), van.narc(scriptdis.SCRIPTS_NARC)
    changed_scripts = {i for i in range(len(bs)) if bytes(bs[i]) != bytes(vs[i])}
    ev2scr = events_to_scripts(van.arm9)

    def entries(buf):
        try:
            return len(scriptdis.script_entries(buf)[0])
        except Exception:
            return 0

    touched, deferred = 0, []
    for i in range(len(be)):
        if bytes(be[i]) == bytes(ve[i]):
            continue
        path = events_json(i)
        name = os.path.basename(path) if path else f"events member {i}"
        scripts = ev2scr.get(i, set())
        if not scripts:
            deferred.append(f"{name}: no map header points at it"); continue
        if scripts & changed_scripts:
            deferred.append(f"{name}: its script file changed too"); continue
        new, old_ = decode_events(be[i]), decode_events(ve[i])
        if any(len(new[k]) != len(old_[k]) for k in old_):
            deferred.append(f"{name}: gained or lost events, so new LOCALID names are needed"); continue
        limit = max((entries(vs[s]) for s in scripts), default=0)
        refs = {o["script"] for o in new["object_events"] if isinstance(o["script"], int)}
        refs |= {b["script"] for b in new["bg_events"]} | {c["script"] for c in new["coord_events"]}
        unknown = sorted(r for r in refs if 0 < r <= 2000 and r > limit)
        if unknown:
            deferred.append(f"{name}: points at script {unknown} but the file has {limit} entries"); continue
        if path is None:
            deferred.append(f"{name}: no json in res/"); continue

        text = open(path, encoding="utf-8").read()
        changes = []
        for key in old_:
            for idx, (nrec, orec) in enumerate(zip(new[key], old_[key])):
                for field, value in nrec.items():
                    if orec[field] == value:
                        continue
                    keypath = [key, idx, field]
                    if field in ("hidden_flag", "var"):
                        value = render_var_or_header(value, jsonstyle.get_value(text, keypath))
                    if jsonstyle.get_value(text, keypath) == value:
                        continue
                    text = jsonstyle.replace_value(text, keypath, value)
                    changes.append(f"{key}[{idx}].{field}: {orec[field]!r} -> {value!r}")
        if changes:
            if not dry_run:
                with open(path, "w", encoding="utf-8", newline="\n") as f:
                    f.write(text)
            log.append((os.path.relpath(path, ROOT), changes))
            touched += 1
    log.append((EVENTS_NARC + " (partially imported)",
                [f"{len(deferred)} maps left for the per-map carry-over:"] + deferred))
    return touched


# ---------------------------------------------------------------- map headers
#
# sMapHeaders is a 593-entry array of 24-byte MapHeader records in arm9. It has
# no symbol in the ROM, and anchoring on the address from a local build does not
# work, because any source change ahead of it in the link order moves it. So the
# table is found by scanning for the offset at which several known headers'
# msgArchiveID fields all land on the text bank this repo assigns them; the
# match is unique and self-checking.
MAP_HEADER_SIZE = 24
MAP_HEADER_FMT = "<BBHHHHHHHHHBBH"
MAP_HEADER_FIELDS = [
    "areaDataArchiveID", "preloadedMapObjectsArchiveID", "mapMatrixID", "scriptsArchiveID",
    "initScriptsArchiveID", "msgArchiveID", "dayMusicID", "nightMusicID",
    "wildEncountersArchiveID", "eventsArchiveID", "label", "weather", "cameraType", "flags",
]
MAP_HEADERS_H = os.path.join("include", "data", "map_headers.h")

# Anchors for the scan: (map header name, the text bank its header points at).
MAP_HEADER_ANCHORS = [
    ("MAP_HEADER_ROUTE_202", "TEXT_BANK_ROUTE_202"),
    ("MAP_HEADER_POKEMON_LEAGUE", "TEXT_BANK_POKEMON_LEAGUE"),
    ("MAP_HEADER_TWINLEAF_TOWN", "TEXT_BANK_TWINLEAF_TOWN"),
]


def load_weather_names():
    import re
    table = {}
    path = os.path.join(ROOT, "include", "constants", "overworld_weather.h")
    for line in open(path):
        mm = re.match(r"\s*#define\s+(OVERWORLD_WEATHER_\w+)\s+(\d+)\s*$", line)
        if mm:
            table.setdefault(int(mm.group(2)), mm.group(1))
    return table


def find_map_header_table(arm9, count):
    maps = load_enum("map_headers")
    banks = load_enum("text_banks")
    by_map = {v: k for k, v in maps.items()}
    by_bank = {v: k for k, v in banks.items()}
    anchors = [(by_map[m] * MAP_HEADER_SIZE + 8, by_bank[b]) for m, b in MAP_HEADER_ANCHORS]
    hits = []
    for off in range(0, len(arm9) - count * MAP_HEADER_SIZE):
        if all(struct.unpack_from("<H", arm9, off + o)[0] == want for o, want in anchors):
            hits.append(off)
    if len(hits) != 1:
        raise LookupError(f"expected exactly one sMapHeaders offset, found {hits}")
    return hits[0]


def decode_map_header(b):
    return dict(zip(MAP_HEADER_FIELDS, struct.unpack(MAP_HEADER_FMT, b)))


def set_map_header_field(text, map_name, field, value):
    """Replace one `.field = ...,` line inside one `[MAP_HEADER_X] = { ... },`
    block. Returns (new text, what was there before)."""
    import re
    marker = f"[{map_name}] = {{"
    start = text.index(marker)
    end = text.index("\n    },", start)
    block = text[start:end]
    pat = re.compile(rf"(\.{field} = )([^,\n]+)(,)")
    mm = pat.search(block)
    if mm is None:
        raise KeyError(f"{map_name} has no .{field}")
    was = mm.group(2)
    if was == str(value):
        return text, was  # already carried over by an earlier run
    block = block[:mm.start()] + mm.group(1) + str(value) + mm.group(3) + block[mm.end():]
    return text[:start] + block + text[end:], was


def import_map_headers(base_arm9, van_arm9, dry_run, log):
    """Carry over the base ROM's map-header edits. Only the fields that actually
    differ are touched, and each is written as the named constant the repo uses
    rather than a bare number."""
    maps = load_enum("map_headers")
    weather = load_weather_names()
    backgrounds = load_enum("battle_backgrounds")
    count = sum(1 for _ in open(os.path.join(ROOT, MAP_HEADERS_H)) if _.startswith("    [MAP_HEADER_"))
    off = find_map_header_table(van_arm9, count)
    if base_arm9[off:off + count * MAP_HEADER_SIZE] == van_arm9[off:off + count * MAP_HEADER_SIZE]:
        return 0

    text = open(os.path.join(ROOT, MAP_HEADERS_H), encoding="utf-8").read()
    changed, skipped = [], []
    for i in range(count):
        o = off + i * MAP_HEADER_SIZE
        nb, vb = base_arm9[o:o + MAP_HEADER_SIZE], van_arm9[o:o + MAP_HEADER_SIZE]
        if nb == vb:
            continue
        new, old = decode_map_header(nb), decode_map_header(vb)
        name = maps[i]
        for field, value in new.items():
            if old[field] == value:
                continue
            if field == "weather":
                if value not in weather:
                    skipped.append(f"{name}: weather {old[field]} -> {value}, which has no constant; skipped")
                    continue
                text, was = set_map_header_field(text, name, "weather", weather[value])
                if was != weather[value]:
                    changed.append(f"{name}: weather {was} -> {weather[value]}")
            elif field == "flags":
                # mapType:7, battleBG:5, then one bit each for bike, running,
                # escape rope and fly
                for sub, shift, mask, table in (("mapType", 0, 0x7F, None),
                                                ("battleBG", 7, 0x1F, backgrounds),
                                                ("isBikeAllowed", 12, 1, None),
                                                ("isRunningAllowed", 13, 1, None),
                                                ("isEscapeRopeAllowed", 14, 1, None),
                                                ("isFlyAllowed", 15, 1, None)):
                    nv, ov = (value >> shift) & mask, (old[field] >> shift) & mask
                    if nv == ov:
                        continue
                    if mask == 1:
                        nv = "TRUE" if nv else "FALSE"
                    elif table is not None:
                        nv = table[nv]
                    text, was = set_map_header_field(text, name, sub, nv)
                    if was != str(nv):
                        changed.append(f"{name}: {sub} {was} -> {nv}")
            else:
                skipped.append(f"{name}: {field} {old[field]} -> {value}; not carried over, "
                               f"this importer only handles weather and the flags word")
    if changed and not dry_run:
        with open(os.path.join(ROOT, MAP_HEADERS_H), "w", encoding="utf-8", newline="\n") as f:
            f.write(text)
    if changed or skipped:
        log.append((MAP_HEADERS_H, changed + skipped))
    return len(changed)


# ---------------------------------------------------------------- text banks
#
# pl_msg.narc is 724 message banks. 78 differ. They split cleanly in two:
#
#   60 have more (or fewer) messages than vanilla and, with a handful of
#   exceptions, nothing changed in the messages they share. Those are the NPC
#   dialogue for Ian's 91 edited field scripts: he appended lines rather than
#   rewriting them. Importing that text without the scripts that call it would
#   land half a change, and new messages need new symbolic ids, so they are left
#   for the script carry-over, which is already its own tracker item.
#
#   18 have exactly as many messages as vanilla, so every change is one message
#   swapped for another and the import is a straight per-index text replacement.
#   Those are handled here.
#
# Where a bank's text lives in res/ depends on the bank. Ten are free-standing
# res/text/<name>.json files. The rest are generated from other res/ data: item
# names and descriptions from res/items/data, move descriptions from res/moves,
# trainer names from res/trainers/data, species names and Pokedex entries from
# res/pokemon. TEXT_BANKS_BY_INDEX routes each one.
TEXT_BANK_TRAINER_NAMES = 618
TEXT_BANK_ITEM_DESCRIPTIONS = 391
TEXT_BANK_ITEM_NAMES = 392
TEXT_BANK_MOVE_DESCRIPTIONS = 646

# Banks with an unchanged message count that this importer deliberately leaves
# alone, with why.
TEXT_BANKS_SKIPPED = {
    412: "species names decode identically; the bank differs only in bytes the decoder does not read",
    706: "Pokedex entries decode identically, same as species names",
    617: "trainer battle messages are keyed by TRMSG_* type per trainer, not by a flat bank index; "
         "mapping the 2,497 entries back needs trainerproc's packing order, which is its own job",
}


def text_bank_names():
    return [l.strip() for l in open(os.path.join(ROOT, "generated", "text_banks.txt")) if l.strip()]


def decode_text_bank(msgenc, charmap, data, tmpdir, tag):
    """Run the repo's own msgenc in decode mode over one bank's bytes."""
    import subprocess
    binpath = os.path.join(tmpdir, tag + ".bin")
    jsonpath = os.path.join(tmpdir, tag + ".json")
    with open(binpath, "wb") as f:
        f.write(data)
    subprocess.run([msgenc, "-d", "--json", "-c", charmap, jsonpath, binpath],
                   check=True, capture_output=True)
    with open(jsonpath, encoding="utf-8") as f:
        return json.load(f)["messages"]


def message_body(msg):
    """A decoded message is either text or an unused slot msgenc calls garbage."""
    return msg["en_US"] if "en_US" in msg else ("garbage", msg.get("garbage"))


def text_targets(index, count):
    """[(json path, key path)] for each message in bank `index`, or None if this
    importer does not know where that bank's text lives. Index into the bank is
    the item / move / trainer id for the generated banks."""
    if index == TEXT_BANK_TRAINER_NAMES:
        return [(trainer_json(i), ["name"]) for i in range(count)]
    if index == TEXT_BANK_ITEM_NAMES:
        return [(item_json(i), ["name"]) for i in range(count)]
    if index == TEXT_BANK_ITEM_DESCRIPTIONS:
        return [(item_json(i), ["description"]) for i in range(count)]
    if index == TEXT_BANK_MOVE_DESCRIPTIONS:
        d = [move_dir(i) for i in range(count)]
        return [(os.path.join(x, "data.json") if x else None, ["description"]) for x in d]
    name = text_bank_names()[index][len("TEXT_BANK_"):].lower()
    path = os.path.join(ROOT, "res", "text", name + ".json")
    if os.path.isfile(path):
        return [(path, ["messages", i, "en_US"]) for i in range(count)]
    return None


def import_text(base, van, msgenc, charmap, tmpdir, dry_run, log):
    """Carry over the banks whose message count is unchanged. Returns the number
    of res/ files changed."""
    bb, vb = base.narc("msgdata/pl_msg.narc"), van.narc("msgdata/pl_msg.narc")
    names = text_bank_names()
    touched, resized, unknown = set(), [], []
    for i in range(len(bb)):
        if bb[i] == vb[i]:
            continue
        new = decode_text_bank(msgenc, charmap, bb[i], tmpdir, f"{i}_base")
        old = decode_text_bank(msgenc, charmap, vb[i], tmpdir, f"{i}_van")
        if len(new) != len(old):
            resized.append((i, names[i], len(old), len(new)))
            continue
        if i in TEXT_BANKS_SKIPPED:
            continue
        targets = text_targets(i, len(new))
        if targets is None:
            unknown.append((i, names[i]))
            continue
        for slot, (nm, om) in enumerate(zip(new, old)):
            nv, ov = message_body(nm), message_body(om)
            if nv == ov:
                continue
            path, keys = targets[slot]
            if path is None:
                log.append((f"{names[i]}[{slot}]", [f"text changed but no res/ file for it; skipped: {ov!r} -> {nv!r}"]))
                continue
            if isinstance(nv, tuple) or isinstance(ov, tuple):
                log.append((f"{names[i]}[{slot}]", [f"unused slot gained or lost text; skipped: {ov!r} -> {nv!r}"]))
                continue
            # {TRNAME} is a text-compression tag, not part of the name.
            # trainerproc decides per trainer whether to emit it (emit_name's
            # uncompressed_classes and uncompressed_trainers leave it off for
            # rivals, the Frontier brains and the five Battleground trainers),
            # and the base ROM has it on every entry because DSPRE re-tagged the
            # whole bank when it saved. Strip it and let trainerproc's rule
            # stand, which also means 38 entries where the base ROM tags a name
            # vanilla leaves untagged are correctly not treated as edits.
            if i == TEXT_BANK_TRAINER_NAMES:
                nv = nv.replace("{TRNAME}", "")
            text = open(path, encoding="utf-8").read()
            if jsonstyle.get_value(text, keys) == nv:
                continue
            text = jsonstyle.replace_value(text, keys, nv)
            if not dry_run:
                with open(path, "w", encoding="utf-8", newline="\n") as f:
                    f.write(text)
            touched.add(path)
            log.append((os.path.relpath(path, ROOT), [f"{names[i]}[{slot}]: {ov!r} -> {nv!r}"]))
    log.append(("pl_msg.narc (partially imported)", [
        f"{len(resized)} banks changed message count and are left for the script carry-over: "
        + ", ".join(f"{n} ({a}->{b})" for _, n, a, b in resized),
    ] + [f"{names[i]}: skipped, {why}" for i, why in TEXT_BANKS_SKIPPED.items()]
      + [f"{n}: same message count but no known res/ home; skipped" for _, n in unknown]))
    return len(touched)


def report_skipped_heights(base, van, log):
    """Sprite Y-offsets are deliberately not carried over; this only writes the
    evidence into the report so a later run re-confirms it rather than
    re-deciding it.

    height.narc holds four members per species (back female, back male, front
    female, front male, empty where that gender has no sprite). 298 of them
    differ, but the pattern says DSPRE re-saved the table rather than Ian
    editing it: 164 of the differences are a zero byte written where vanilla has
    an empty member, and of the 116 species where vanilla had male and female
    offsets equal, every single one has only the male offset changed. A hand
    edit to a shared sprite's offset would move both. See the inventory's note
    that 2,788 of 2,964 pl_pokegra files also differ by a few header bytes
    each."""
    b, v = base.narc("poketool/pokegra/height.narc"), van.narc("poketool/pokegra/height.narc")
    differ = [i for i in range(len(b)) if b[i] != v[i]]
    wrote_into_empty = sum(1 for i in differ if not v[i] and b[i])
    broke_symmetry = 0
    for sp in sorted({i // 4 for i in differ}):
        vals_v = [v[4 * sp + k] for k in range(4)]
        vals_b = [b[4 * sp + k] for k in range(4)]
        if all(x for x in vals_v) and vals_v[0] == vals_v[1] and vals_v[2] == vals_v[3]:
            if vals_b[0] != vals_b[1] or vals_b[2] != vals_b[3]:
                broke_symmetry += 1
    log.append(("height.narc (not imported)", [
        f"{len(differ)} of {len(b)} members differ",
        f"{wrote_into_empty} of them write a byte where vanilla has an empty member "
        f"(a gender the species does not have; the decomp derives this from the gender ratio "
        f"and cannot express it as an edit)",
        f"{broke_symmetry} species had male == female in vanilla and have only the male "
        f"offset changed in the base ROM, which a hand edit would not do",
        "reading this as a DSPRE re-save, not an edit; skipped pending Ian",
    ]))
    return 0


def report_skipped_items(base, van, log):
    """The six vitamin records are malformed in the base ROM, so there is
    nothing to carry over; this records why."""
    b, v = base.narc("itemtool/itemdata/pl_item_data.narc"), van.narc("itemtool/itemdata/pl_item_data.narc")
    differ = [i for i in range(len(b)) if b[i] != v[i]]
    changes = [f"{len(differ)} of {len(b)} records differ: "
               + ", ".join(ITEMS.get(i, str(i)) for i in differ)]
    for i in differ:
        changes.append(f"{ITEMS.get(i, i)}: {len(v[i])} bytes -> {len(b[i])} bytes")
    changes.append("every differing record grew from ItemData's 34 bytes to 36, with the "
                   "vitamin's EV amount zeroed and everything after it shifted one byte right, "
                   "so the friendship values no longer line up with the struct")
    changes.append("reading this as DSPRE writing a malformed record, not an edit; skipped "
                   "pending Ian. The vitamin change he described is the EV cap (100 -> 252), "
                   "which is a code edit and is already its own tracker item")
    log.append(("pl_item_data.narc (not imported)", changes))
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", required=True)
    ap.add_argument("--vanilla", required=True)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--msgenc", default="build/tools/msgenc/msgenc",
                    help="the repo's own message tool, used to decode text banks")
    ap.add_argument("--charmap", default="tools/msgenc/charmap.txt")
    ap.add_argument("--skip-text", action="store_true",
                    help="skip the text banks (they need a built msgenc)")
    ap.add_argument("--report", default="tools/oxide/import_report.md")
    a = ap.parse_args()

    base, van = Rom(a.base), Rom(a.vanilla)
    log = []
    counts = {}

    # Species whose evolutions Phase 4 element 3 added to, so the base ROM's
    # list is no longer the whole truth and re-importing it would drop the new
    # entry. Everything else about these species is still carried over.
    EVOLUTIONS_EXTENDED = {
        57: "Primeape gains Annihilape", 123: "Scyther gains Kleavor",
        130: "Gyarados gains Gyarados M", 133: "Eevee gains Sylveon",
        194: "Wooper gains Clodsire", 370: "Luvdisc gains Alomomola",
        428: "Lopunny gains Lopunny M",
    }

    # species: personal + learnset + evolutions live in one data.json
    bp, vp = base.narc("poketool/personal/pl_personal.narc"), van.narc("poketool/personal/pl_personal.narc")
    bl, vl = base.narc("poketool/personal/wotbl.narc"), van.narc("poketool/personal/wotbl.narc")
    be, ve = base.narc("poketool/personal/evo.narc"), van.narc("poketool/personal/evo.narc")
    n = 0
    for i in range(len(bp)):
        if bp[i] == vp[i] and bl[i] == vl[i] and be[i] == ve[i]:
            continue
        d = species_dir(i)
        if d is None:
            log.append((f"personal index {i}", ["record differs but has no data.json (egg/unknown form); skipped"]))
            continue
        new = decode_personal(bp[i]); old = decode_personal(vp[i])
        new["learnset.by_level"] = decode_learnset(bl[i]); old["learnset.by_level"] = decode_learnset(vl[i])
        if i in EVOLUTIONS_EXTENDED:
            log.append((d, [f"evolutions not carried over, {EVOLUTIONS_EXTENDED[i]} "
                            f"(Phase 4 element 3); the rest of the record still is"]))
        else:
            new["evolutions"] = decode_evolutions(be[i]); old["evolutions"] = decode_evolutions(ve[i])
        # nested keys expressed with dots need to become real nesting for flatten()
        for k in ("learnset.by_tm", "learnset.by_level"):
            for dd in (new, old):
                dd.setdefault("learnset", {})[k.split(".")[1]] = dd.pop(k)
        if apply_diff(os.path.join(d, "data.json"), new, old, a.dry_run, log):
            n += 1
    counts["species"] = n

    # moves
    bm, vm = base.narc("poketool/waza/pl_waza_tbl.narc"), van.narc("poketool/waza/pl_waza_tbl.narc")
    n = 0
    for i in range(len(bm)):
        if bm[i] == vm[i]:
            continue
        d = move_dir(i)
        if d is None:
            log.append((f"move index {i}", ["record differs but has no data.json; skipped"]))
            continue
        if apply_diff(os.path.join(d, "data.json"), decode_move(bm[i]), decode_move(vm[i]), a.dry_run, log):
            n += 1
    counts["moves"] = n

    # trainers
    bh, vh = base.narc("poketool/trainer/trdata.narc"), van.narc("poketool/trainer/trdata.narc")
    bpk, vpk = base.narc("poketool/trainer/trpoke.narc"), van.narc("poketool/trainer/trpoke.narc")
    n = 0
    resized = 0
    for i in range(len(bh)):
        if bh[i] == vh[i] and bpk[i] == vpk[i]:
            continue
        d = trainer_json(i)
        if d is None:
            log.append((f"trainer index {i}", ["record differs but has no data.json; skipped"]))
            continue
        new_header, new_mdt, new_ps = decode_trainer_header(bh[i])
        old_header, old_mdt, old_ps = decode_trainer_header(vh[i])
        new_party = decode_trainer_party(bpk[i], new_ps, new_mdt)
        old_party = decode_trainer_party(vpk[i], old_ps, old_mdt)
        # Count a resize only when the file actually needs rewriting, so a dry run
        # on an already-imported tree reports 0 here like every other counter.
        if apply_trainer_diff(d, new_header, new_party, old_header, old_party, a.dry_run, log):
            n += 1
            if len(new_party) != len(old_party):
                resized += 1
    counts["trainers"] = n
    counts["trainers_party_resized"] = resized

    # wild encounters
    bencs, vencs = base.narc("fielddata/encountdata/pl_enc_data.narc"), van.narc("fielddata/encountdata/pl_enc_data.narc")
    n = 0
    skipped_fields = 0
    authored = authored_encounters()
    authored_skipped = []
    for i in range(len(bencs)):
        if bencs[i] == vencs[i]:
            continue
        d = encounter_json(i)
        if d is None:
            log.append((f"encounter index {i}", ["record differs but has no json; skipped"]))
            continue
        stem = os.path.basename(d)[:-len(".json")]
        if stem in authored:
            authored_skipped.append(f"{stem}: authored, skipped ({authored[stem]})")
            continue
        new_enc, old_enc = decode_encounter(bencs[i]), decode_encounter(vencs[i])
        for key in ENCOUNTER_SKIP_KEYS:
            if new_enc[key] != old_enc[key]:
                skipped_fields += 1
            del new_enc[key], old_enc[key]
        if apply_scalar_diff(d, new_enc, old_enc, a.dry_run, log):
            n += 1
    counts["encounters"] = n
    log.append(("pl_enc_data.narc (partially imported)", [
        f"{skipped_fields} differing values in {', '.join(ENCOUNTER_SKIP_KEYS)} were not carried "
        f"over; see ENCOUNTER_SKIP_KEYS in this importer for why",
        f"{len(authored_skipped)} authored table(s) left alone; see AUTHORED and the sidecar",
    ] + authored_skipped))

    # in-game trades
    btr, vtr = base.narc("fielddata/pokemon_trade/fld_trade.narc"), van.narc("fielddata/pokemon_trade/fld_trade.narc")
    n = 0
    for i in range(len(btr)):
        if btr[i] == vtr[i]:
            continue
        d = trade_json(i)
        if d is None:
            log.append((f"npc trade index {i}", ["record differs but has no json; skipped"]))
            continue
        if apply_scalar_diff(d, decode_trade(btr[i]), decode_trade(vtr[i]), a.dry_run, log):
            n += 1
    counts["npc_trades"] = n

    if a.skip_text:
        counts["text"] = "skipped"
    else:
        import tempfile
        with tempfile.TemporaryDirectory() as tmpdir:
            counts["text"] = import_text(base, van, a.msgenc, a.charmap, tmpdir, a.dry_run, log)

    counts["map_headers"] = import_map_headers(base.arm9, van.arm9, a.dry_run, log)
    counts["events"] = import_events(base, van, a.dry_run, log)

    counts["heights"] = report_skipped_heights(base, van, log)
    counts["items"] = report_skipped_items(base, van, log)

    with open(a.report, "w", encoding="utf-8") as f:
        f.write("# Base ROM import report\n\n")
        f.write(f"base: `{os.path.basename(a.base)}`  vanilla: `{os.path.basename(a.vanilla)}`  ")
        f.write(f"dry run: {a.dry_run}\n\nFiles changed: {counts}\n\n")
        for rel, changes in log:
            f.write(f"## {rel}\n")
            for c in changes:
                f.write(f"- {c}\n")
            f.write("\n")
    print(f"{'would change' if a.dry_run else 'changed'}: {counts}; report at {a.report}")


if __name__ == "__main__":
    main()

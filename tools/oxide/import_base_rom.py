#!/usr/bin/env python3
"""Carry species, move, evolution and learnset edits from a modified Platinum
ROM into this source tree.

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
def load_enum(name):
    """Value -> NAME for a generated enum. Reads build/generated/<name>.h
    (which carries the exact values, including bit-mask enums such as move
    ranges) and falls back to generated/<name>.txt (sequential values)."""
    import re
    header = os.path.join(ROOT, "build", "generated", name + ".h")
    table = {}
    if os.path.exists(header):
        body = open(header).read()
        m = re.search(r"enum \w+ \{(.*?)\};", body, re.S)
        for line in m.group(1).splitlines():
            mm = re.match(r"\s*([A-Z0-9_]+)\s*=\s*(.+?),?\s*$", line)
            if mm:
                table[eval(mm.group(2))] = mm.group(1)  # values are simple int expressions
        if table:
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


def apply_trainer_diff(json_path, new_header, new_party, old_header, old_party, dry_run, log):
    """Like apply_diff, but for trainers: `party` is a list of objects, which
    the flatten()-based apply_diff can't reach into (it treats any list as
    one opaque value), so per-mon fields are patched individually here, and
    `ability`/`gender` are inserted as new keys the first time either is
    needed. Trainers whose party size changed are logged, not applied - that
    needs inserting whole new party-member objects, which this tool doesn't
    support yet."""
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
        log.append((rel, [f"party size changed ({len(old_party)} -> {len(new_party)} mons); "
                           "needs a human to add/remove party-member objects, not applied"]))
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
                if jsonstyle.get_value(text, ["party", i, "ability"]) != nm["ability"]:
                    text = jsonstyle.replace_value(text, ["party", i, "ability"], nm["ability"])
                if jsonstyle.get_value(text, ["party", i, "gender"]) != nm["gender"]:
                    text = jsonstyle.replace_value(text, ["party", i, "gender"], nm["gender"])
                changed.append(f"party[{i}].ability/gender: {om.get('ability')!r}/{om.get('gender')!r} "
                                f"-> {nm['ability']!r}/{nm['gender']!r}")

    if changed:
        log.append((rel, changed))
        if not dry_run:
            with open(json_path, "w", encoding="utf-8", newline="\n") as f:
                f.write(text)
    return bool(changed)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", required=True)
    ap.add_argument("--vanilla", required=True)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--report", default="tools/oxide/import_report.md")
    a = ap.parse_args()

    base, van = Rom(a.base), Rom(a.vanilla)
    log = []
    counts = {}

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
    skipped_size = 0
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
        if len(new_party) != len(old_party):
            skipped_size += 1
        if apply_trainer_diff(d, new_header, new_party, old_header, old_party, a.dry_run, log):
            n += 1
    counts["trainers"] = n
    counts["trainers_party_size_changed_skipped"] = skipped_size

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

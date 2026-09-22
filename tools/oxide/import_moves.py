#!/usr/bin/env python3
"""Import Hardlove Gold's moves into res/moves, one directory per move.

Phase 4 element 4. `docs/oxide/donor-move-tables.md` is the evidence for every
claim this relies on; the short version is that the donor's move record is
Platinum's record field for field, and its ids agree with Platinum's for 0..467,
so the 452 new moves at 471..922 append with no translation layer.

What it writes, and nothing else:

  * `generated/moves.txt`            grows from 468 entries to 923
  * `res/moves/<slug>/data.json`     one per new move, in the res/moves style
  * `res/moves/<slug>/script.s`      `GoToEffectScript`, which is what 447 of
                                     the 468 existing moves already say
  * `res/moves/<slug>/anim.s`        copied from an existing move's animation,
                                     per `docs/oxide/move-animation-map.json`
  * `generated/move_battle_effects.txt`  grows from 277 entries to 407
  * `res/battle/scripts/effects/effect_script_0277.s` .. `_0406.s` as stubs,
    plus their lines in that folder's `meson.build`

Ids 468, 469 and 470 are the three inaccessible tail records the retail game
ships. They used to be packed by `pack_extra_moves()` in
`tools/dataproc/src/moveproc.c`; they are ordinary move directories now, with
the same bytes, because the enum is positional and Hone Claws cannot be 471
unless three entries sit in front of it. Those three records still match the
base ROM byte for byte, which `verify_narcs.py` checks.

    tools/oxide/oxide-python tools/oxide/import_moves.py --dry-run
    tools/oxide/oxide-python tools/oxide/import_moves.py

A re-run rewrites the move data and the generated lists but leaves an existing
`anim.s` or `effect_script_NNNN.s` alone, because those are where hand work
lands (a ported effect, a tuned animation); pass `--force` to regenerate them.
"""

import argparse
import json
import os
import re
import shutil
import sys
from collections import Counter, OrderedDict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import donor_moves  # noqa: E402
import jsonstyle  # noqa: E402
import textfit  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

MOVES_TXT = os.path.join(ROOT, "generated", "moves.txt")
EFFECTS_TXT = os.path.join(ROOT, "generated", "move_battle_effects.txt")
MOVES_DIR = os.path.join(ROOT, "res", "moves")
EFFECTS_DIR = os.path.join(ROOT, "res", "battle", "scripts", "effects")
EFFECTS_MESON = os.path.join(EFFECTS_DIR, "meson.build")
ANIM_MAP = os.path.join(ROOT, "docs", "oxide", "move-animation-map.json")
DESC_OVERRIDE = os.path.join(ROOT, "docs", "oxide", "move-descriptions.json")
EFFECT_NAMES = os.path.join(ROOT, "docs", "oxide", "battle-effect-names.json")

FIRST_NEW = 468          # the first id this tool owns; 468..470 are the retail tail
LAST_NEW = 922           # the donor's last named move
PLATINUM_EFFECTS = 277   # Platinum's own BATTLE_EFFECT_* count
LAST_EFFECT = 406        # the donor's highest effect id


# ---------------------------------------------------------------- enum names

def enum_from_name(name):
    """A move's enum name from its display name.

    The rule is the repo's own: split camelCase humps, drop apostrophes, and
    turn every other run of non-alphanumerics into one underscore. Checked
    against all 467 existing moves, where it reproduces the enum exactly,
    including ViceGrip -> MOVE_VICE_GRIP and Double-Edge -> MOVE_DOUBLE_EDGE.
    """
    s = re.sub(r"(?<=[a-z])(?=[A-Z])", " ", name)
    s = s.replace("’", "").replace("'", "")
    s = re.sub(r"[^A-Za-z0-9]+", "_", s)
    return "MOVE_" + s.upper().strip("_")


CLASS_SUFFIX = {0: "_PHYSICAL", 1: "_SPECIAL", 2: "_STATUS"}


def assign_enums(names, recs):
    """Enum name per new move id, with the eighteen duplicate names resolved.

    The generic Z-moves are stored twice, once physical and once special, under
    one display name each (two "Breakneck Blitz" records, and so on). The
    display name stays as the donor has it, because that is what the game would
    print; only the enum and the directory take a `_PHYSICAL` / `_SPECIAL`
    suffix, since those have to be unique.
    """
    ids = [i for i in range(FIRST_NEW, LAST_NEW + 1) if i not in PLACEHOLDERS]
    counts = Counter(enum_from_name(names[i]) for i in ids)
    out = {}
    for i in ids:
        e = enum_from_name(names[i])
        out[i] = e + CLASS_SUFFIX[recs[i]["class"]] if counts[e] > 1 else e
    return out


# ------------------------------------------------------- the retail tail three
# Reproduced from pack_extra_moves() in tools/dataproc/src/moveproc.c, which
# this import deletes. Same bytes, so pl_waza_tbl.narc members 468..470 still
# match the base ROM. They are unreachable: nothing names them and nothing
# teaches them.

PLACEHOLDERS = {
    468: ("MOVE_UNUSED_468", "CONTEST_EFFECT_LOW_VOLTAGE_ADVANTAGE", "CONTEST_TYPE_BEAUTY"),
    469: ("MOVE_UNUSED_469", "CONTEST_EFFECT_FIRST_PERFORMANCE_ADVANTAGE", "CONTEST_TYPE_CUTE"),
    470: ("MOVE_UNUSED_470", "CONTEST_EFFECT_FINAL_PERFORMANCE_ADVANTAGE", "CONTEST_TYPE_SMART"),
}


def placeholder_data(contest_effect, contest_type):
    return OrderedDict([
        ("name", "-"),
        ("description", ["-"]),
        ("class", "CLASS_SPECIAL"),
        ("type", "TYPE_NORMAL"),
        ("power", 100),
        ("accuracy", 100),
        ("pp", 10),
        ("effect", OrderedDict([("type", "BATTLE_EFFECT_HIT"), ("chance", 0)])),
        ("range", "RANGE_SINGLE_TARGET"),
        ("priority", 0),
        ("flags", ["MOVE_FLAG_CAN_PROTECT",
                   "MOVE_FLAG_CAN_MIRROR_MOVE",
                   "MOVE_FLAG_TRIGGERS_KINGS_ROCK"]),
        ("contest", OrderedDict([("effect", contest_effect), ("type", contest_type)])),
    ])


# ------------------------------------------------------------ field conversion

CLASSES = ("CLASS_PHYSICAL", "CLASS_SPECIAL", "CLASS_STATUS")

# Platinum's own move type -> the contest type most of its moves carry. The
# donor authored no contest data for its new moves (the survey measured the
# field as noise), and Oxide has Super Contests, so a coherent default beats
# copying the noise. Measured over Platinum's 467; the weakest column is Normal,
# where nothing dominates and Cute is only a plurality.
CONTEST_TYPE_BY_TYPE = {
    "TYPE_NORMAL": "CONTEST_TYPE_CUTE",
    "TYPE_FIGHTING": "CONTEST_TYPE_COOL",
    "TYPE_FLYING": "CONTEST_TYPE_COOL",
    "TYPE_POISON": "CONTEST_TYPE_SMART",
    "TYPE_GROUND": "CONTEST_TYPE_TOUGH",
    "TYPE_ROCK": "CONTEST_TYPE_TOUGH",
    "TYPE_BUG": "CONTEST_TYPE_SMART",
    "TYPE_GHOST": "CONTEST_TYPE_SMART",
    "TYPE_STEEL": "CONTEST_TYPE_COOL",
    "TYPE_MYSTERY": "CONTEST_TYPE_TOUGH",
    "TYPE_FIRE": "CONTEST_TYPE_BEAUTY",
    "TYPE_WATER": "CONTEST_TYPE_BEAUTY",
    "TYPE_GRASS": "CONTEST_TYPE_SMART",
    "TYPE_ELECTRIC": "CONTEST_TYPE_COOL",
    "TYPE_PSYCHIC": "CONTEST_TYPE_SMART",
    "TYPE_ICE": "CONTEST_TYPE_BEAUTY",
    "TYPE_DRAGON": "CONTEST_TYPE_COOL",
    "TYPE_DARK": "CONTEST_TYPE_SMART",
    "TYPE_FAIRY": "CONTEST_TYPE_CUTE",
}

# The donor packs range as a bitmask where bit n-1 is Platinum's range n. Three
# moves store 8|16, all-adjacent plus the user, which Platinum has no single
# range for; that is exactly what RANGE_ALL means, so they take it.
RANGE_ALL = "RANGE_ALL"


def read_list(path):
    return [l.strip() for l in open(path, encoding="utf-8") if l.strip()]


def description(i, donor_lines, override):
    """The move's description, wrapped to Platinum's box.

    The donor's text is wrapped for HeartGold's wider window, so it is rejoined
    into one paragraph and re-wrapped here rather than carried over as it came.
    Where even the rewrap will not fit in five lines of 120 pixels, a shortened
    paragraph from `docs/oxide/move-descriptions.json` is used instead; the
    donor's own text has no way of fitting.
    """
    text = override[i]["text"] if i in override else textfit.flatten(donor_lines)
    return textfit.as_description(textfit.wrap(text, textfit.MOVE_DESC_WIDTH))


def convert(i, rec, name, desc, types, ranges, flags, effects):
    """One donor record as a res/moves data.json object."""
    mtype = types[donor_moves.type_to_oxide(rec["type"])]
    cls = CLASSES[rec["class"]]

    ri = rec["range_platinum"]
    rng = RANGE_ALL if ri is None else ranges[ri]

    flag_names = [flags[b] for b in range(8) if rec["flags"] >> b & 1]
    # King's Rock is set on one record in the donor's whole 924 and on 202 of
    # Platinum's 467, so hg-engine dropped the bit rather than curated it.
    # Platinum's own pattern is per-move curation with no rule behind it, so
    # the new moves take the later generations' rule instead: the item works on
    # any damaging move. The natives keep their own byte; nothing here edits them.
    kr = "MOVE_FLAG_TRIGGERS_KINGS_ROCK"
    if cls != "CLASS_STATUS" and kr not in flag_names:
        flag_names.append(kr)
    flag_names.sort(key=flags.index)

    return OrderedDict([
        ("name", name),
        ("description", desc),
        ("class", cls),
        ("type", mtype),
        ("power", rec["power"]),
        ("accuracy", rec["accuracy"]),
        ("pp", rec["pp"]),
        ("effect", OrderedDict([("type", effects[rec["effect"]]),
                                ("chance", rec["effect_chance"])])),
        ("range", rng),
        ("priority", rec["priority"]),
        ("flags", flag_names),
        ("contest", OrderedDict([
            ("effect", "CONTEST_EFFECT_BASIC" if rec["contest_effect"] else "CONTEST_EFFECT_NONE"),
            ("type", CONTEST_TYPE_BY_TYPE[mtype]),
        ])),
    ])


# ------------------------------------------------------------- effect naming

def name_effects(recs, enums):
    """Names for the donor's battle effects 277..406.

    The donor ROM carries no names, but hg-engine's source does: it keeps them
    in its filenames, `effect_script_0277_ATK_ACC_UP.s`. Those are the names
    used here, from `docs/oxide/battle-effect-names.json`, so that an Oxide
    constant and the hg-engine file whose script has to be ported into it are
    called the same thing. That also makes the shared range check out:
    hg-engine and Platinum agree on the name of 256 of the first 277 effects,
    and the 21 that differ are two projects' words for the same behaviour, so
    the numbering really is shared and not just consistent.

    One deviation, and it is the only one. hg-engine calls effect 299
    `HIT_THREE_TIMES`, which is already Platinum's name for effect 104; the two
    are different, 299 being a flat three hits (Triple Dive) and 104 the one
    that gains ten power a hit (Triple Kick). hg-engine's own name for 104 says
    so, `HIT_THREE_TIMES_INCREMENT_BASE_POWER_10`, but Platinum's constant
    cannot be renamed without touching every move that points at it, so 299 is
    `HIT_THREE_TIMES_FIXED_POWER` here.

    If the names file is missing, each effect falls back to the first move that
    uses it, which keeps the tool working without a clone of hg-engine on disk.
    """
    names = {}
    if os.path.exists(EFFECT_NAMES):
        names = {int(k): v
                 for k, v in json.load(open(EFFECT_NAMES, encoding="utf-8")).items()}
    first = {}
    for i in range(1, LAST_NEW + 1):
        e = recs[i]["effect"]
        if e >= PLATINUM_EFFECTS and e not in first and i in enums:
            first[e] = enums[i][len("MOVE_"):]
    out = []
    for e in range(PLATINUM_EFFECTS, LAST_EFFECT + 1):
        if e in names:
            out.append("BATTLE_EFFECT_" + names[e])
        elif e in first:
            out.append("BATTLE_EFFECT_" + first[e])
        else:
            out.append("BATTLE_EFFECT_UNUSED_%d" % e)
    return out


DAMAGE_STUB = """#include "macros/btlcmd.inc"


_000:
    CalcCrit
    CalcDamage
    End
"""

# BATTLE_EFFECT_DO_NOTHING's own script. The move announces "But nothing
# happened!" rather than silently doing nothing, which is the honest thing for
# a status effect that is not written yet.
STATUS_STUB = """#include "macros/btlcmd.inc"


_000:
    UpdateVar OPCODE_FLAG_ON, BTLVAR_MOVE_STATUS_FLAGS, MOVE_STATUS_SPLASH
    End
"""


def effect_stub(effect_id, recs):
    """Which stub an unwritten effect gets. A damaging move should still do its
    damage; a status move should say nothing happened."""
    users = [i for i in range(1, LAST_NEW + 1) if recs[i]["effect"] == effect_id]
    return STATUS_STUB if all(recs[i]["class"] == 2 for i in users) else DAMAGE_STUB


SCRIPT_S = """#include "macros/btlcmd.inc"


_000:
    GoToEffectScript
"""


# ------------------------------------------------------------------ the write

def move_json(obj):
    """res/moves style: never inline an array, empty arrays are `[]`, and
    non-ASCII stays literal. Verified to round-trip all 468 existing files."""
    return jsonstyle.dumps(obj, max_inline=0, ascii_strings=False, empty_array="[]")


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--dry-run", action="store_true", help="report, write nothing")
    ap.add_argument("--rom", default=donor_moves.donor.DEFAULT_ROM)
    ap.add_argument("--force", action="store_true",
                    help="also overwrite existing anim.s and effect_script files")
    a = ap.parse_args()

    dm = donor_moves.DonorMoves(a.rom)
    recs = dm.moves()
    names = dm.names()
    descs = dm.descriptions()

    types = read_list(os.path.join(ROOT, "generated", "pokemon_types.txt"))
    ranges = read_list(os.path.join(ROOT, "generated", "move_ranges.txt"))
    flags = read_list(os.path.join(ROOT, "generated", "move_flags.txt"))
    effects = read_list(EFFECTS_TXT)
    # Re-runnable: the tool owns everything from FIRST_NEW up, so a second run
    # rebuilds those entries rather than appending to its own output. Platinum's
    # own 468 are never touched.
    old_moves = read_list(MOVES_TXT)
    if old_moves[-1] != "MAX_MOVES":
        sys.exit("moves.txt does not end in MAX_MOVES; refusing to rewrite it")
    if len(old_moves) - 1 < FIRST_NEW:
        sys.exit("moves.txt has only %d entries, expected at least %d"
                 % (len(old_moves) - 1, FIRST_NEW))
    natives = old_moves[:FIRST_NEW]
    effects = effects[:PLATINUM_EFFECTS]

    enums = assign_enums(names, recs)
    effect_names = name_effects(recs, enums)
    all_effects = effects + effect_names

    anim = {}
    if os.path.exists(ANIM_MAP):
        anim = {int(k): v["reuse"]
                for k, v in json.load(open(ANIM_MAP, encoding="utf-8")).items()}
    override = {}
    if os.path.exists(DESC_OVERRIDE):
        override = {int(k): v
                    for k, v in json.load(open(DESC_OVERRIDE, encoding="utf-8")).items()}

    written = []
    fallback = []
    overflow = []
    wide_names = []
    for i in range(FIRST_NEW, LAST_NEW + 1):
        if i in PLACEHOLDERS:
            enum, ce, ct = PLACEHOLDERS[i]
            data = placeholder_data(ce, ct)
            src = None
        else:
            enum = enums[i]
            desc = description(i, descs[i], override)
            data = convert(i, recs[i], names[i], desc,
                           types, ranges, flags, all_effects)
            src = anim.get(i)
            if src is None:
                fallback.append(i)
            plain = [l.rstrip("\n") for l in desc]
            if not textfit.fits(plain):
                overflow.append((i, names[i], len(plain), max(textfit.px(l) for l in plain)))
            if textfit.px(names[i]) > textfit.MOVE_NAME_WIDTH:
                wide_names.append((i, names[i], textfit.px(names[i])))
        slug = enum[len("MOVE_"):].lower()
        written.append((i, enum, slug, data, src))

    seen = {}
    for i, enum, slug, _, _ in written:
        if enum in natives:
            sys.exit("%s (move %d) collides with an existing enum" % (enum, i))
        if enum in seen:
            sys.exit("%s is used by moves %d and %d" % (enum, seen[enum], i))
        seen[enum] = i

    print("new move directories: %d (ids %d..%d, of which %d are the retail tail)"
          % (len(written), FIRST_NEW, LAST_NEW, len(PLACEHOLDERS)))
    print("new battle effect ids: %d (%d..%d), %d named from hg-engine, %d unnamed"
          % (len(effect_names), PLATINUM_EFFECTS, LAST_EFFECT,
             sum(1 for n in effect_names if "_UNUSED_" not in n),
             sum(1 for n in effect_names if "_UNUSED_" in n)))
    if fallback:
        print("moves with no animation in the map, taking the placeholder: %d %s"
              % (len(fallback), fallback[:10]))
    else:
        print("every new move reuses an existing move's animation, per %s"
              % os.path.relpath(ANIM_MAP, ROOT))
    print("descriptions shortened to fit Platinum's box: %d" % len(override))
    if overflow:
        print("descriptions that STILL overflow %d px x %d lines: %d"
              % (textfit.MOVE_DESC_WIDTH, textfit.MOVE_DESC_LINES, len(overflow)))
        for row in overflow[:5]:
            print("    %4d %-18s %d lines, widest %d px" % row)
    if wide_names:
        print("names wider than the %d px move-name window: %d %s"
              % (textfit.MOVE_NAME_WIDTH, len(wide_names),
                 [n for _, n, _ in wide_names]))
    if a.dry_run:
        print("dry run, nothing written")
        return

    for i, enum, slug, data, src in written:
        d = os.path.join(MOVES_DIR, slug)
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "data.json"), "w", encoding="utf-8", newline="\n") as f:
            f.write(move_json(data))
        with open(os.path.join(d, "script.s"), "w", encoding="utf-8", newline="\n") as f:
            f.write(SCRIPT_S)
        anim_src = (os.path.join(MOVES_DIR, src, "anim.s") if src else
                    os.path.join(MOVES_DIR, "unused_468", "anim.s"))
        anim_dst = os.path.join(d, "anim.s")
        if a.force or not os.path.exists(anim_dst):
            shutil.copyfile(anim_src, anim_dst)

    with open(MOVES_TXT, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(natives + [e for _, e, _, _, _ in written]
                          + ["MAX_MOVES"]) + "\n")

    with open(EFFECTS_TXT, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(all_effects) + "\n")

    for n, name in enumerate(effect_names, start=PLATINUM_EFFECTS):
        p = os.path.join(EFFECTS_DIR, "effect_script_%04d.s" % n)
        if not a.force and os.path.exists(p):
            continue
        with open(p, "w", encoding="utf-8", newline="\n") as f:
            f.write(effect_stub(n, recs))

    lines = ["effect_script_files = files("]
    lines += ["    'effect_script_%04d.s'," % n for n in range(LAST_EFFECT)]
    lines.append("    'effect_script_%04d.s'" % LAST_EFFECT)
    lines.append(")")
    with open(EFFECTS_MESON, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines) + "\n")

    print("written")


if __name__ == "__main__":
    import os as _os, sys as _sys
    _sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
    import pinned_python
    pinned_python.ensure()
    main()

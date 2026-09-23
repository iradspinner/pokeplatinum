#!/usr/bin/env python3
"""Compare NARCs inside a freshly built ROM against the same NARCs in a
reference ROM, member by member. Used to prove that data imported into res/
rebuilds to exactly the bytes the reference ROM carries.

Usage:
    python3 tools/oxide/verify_narcs.py --built build/pokeplatinum.us.nds --ref BASE.nds [PATH ...]

With no PATH arguments, checks the tables the importer handles byte-for-byte.
With --encounters, checks pl_enc_data.narc field by field instead, which is what
that table needs: a few fields are deliberately not imported, so its bytes are
not expected to match.
"""
import argparse
import importlib.util
import os
import sys
import struct

import ndspy.narc
import ndspy.rom

DEFAULT = [
    "poketool/personal/pl_personal.narc",
    "poketool/personal/wotbl.narc",
    "poketool/personal/evo.narc",
    "poketool/waza/pl_waza_tbl.narc",
]


def walk(folder, prefix=""):
    out = {}
    for i, name in enumerate(folder.files):
        out[prefix + name] = folder.firstID + i
    for sub, f in folder.folders:
        out.update(walk(f, prefix + sub + "/"))
    return out


def load_importer():
    """The encounter decoder lives in import_base_rom.py; importing it by path
    keeps the two tools from needing a package."""
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "import_base_rom.py")
    spec = importlib.util.spec_from_file_location("import_base_rom", path)
    mod = importlib.util.module_from_spec(spec)
    argv, sys.argv = sys.argv, [path]
    try:
        spec.loader.exec_module(mod)
    finally:
        sys.argv = argv
    return mod


def check_encounters(built, ref, nb, nr):
    """Field-level check for pl_enc_data.narc, which a byte comparison cannot
    do: the importer deliberately leaves unown_table and rate_form0..4 at their
    vanilla values (see ENCOUNTER_SKIP_KEYS). Everything else must match the
    reference exactly."""
    imp = load_importer()
    path = "fielddata/encountdata/pl_enc_data.narc"
    b = ndspy.narc.NARC(built.files[nb[path]]).files
    r = ndspy.narc.NARC(ref.files[nr[path]]).files
    order = [l.strip() for l in open(os.path.join("res", "field", "encounters", "encounters.order")) if l.strip()]
    # Tables the authoring pass rewrote no longer match the base ROM on
    # purpose; --source is their check. They are skipped here, and named, so
    # this mode stays usable for the tables that still track the reference.
    authored = imp.authored_encounters()
    mismatches, skipped, authored_skipped = 0, 0, []
    for i in range(min(len(b), len(r))):
        if i < len(order) and order[i] in authored:
            authored_skipped.append(order[i])
            continue
        db, dr = imp.decode_encounter(b[i]), imp.decode_encounter(r[i])
        for key in imp.ENCOUNTER_SKIP_KEYS:
            if db[key] != dr[key]:
                skipped += 1
            del db[key], dr[key]
        if db != dr:
            mismatches += 1
            name = order[i] if i < len(order) else f"member {i}"
            want = {tuple(p): v for p, v in imp.scalar_paths(dr)}
            diffs = [f"{'.'.join(str(x) for x in p)}: built {v!r} != ref {want.get(tuple(p))!r}"
                     for p, v in imp.scalar_paths(db) if want.get(tuple(p)) != v]
            print(f"{name}: {len(diffs)} fields differ: {diffs[:4]}")
    if mismatches:
        print(f"{path}: {mismatches} of {len(b)} tables differ outside the skipped fields")
    else:
        print(f"{path}: all {len(b) - len(authored_skipped)} unauthored tables match the "
              f"reference outside the skipped fields "
              f"({skipped} skipped-field differences left at their vanilla values, as intended)")
    if authored_skipped:
        print(f"  {len(authored_skipped)} authored table(s) not compared to the base ROM "
              f"(use --source for them): {', '.join(authored_skipped[:6])}"
              + (" ..." if len(authored_skipped) > 6 else ""))
    return mismatches == 0


def check_encounters_source(built, nb):
    """M7: the built pl_enc_data.narc against res/field/encounters/*.json,
    field by field.

    The --ref check proves the build matches the base ROM, which stops being
    the truth the moment a table is authored. This proves the build matches
    the source, which is the only thing that stays authoritative. Nothing is
    skipped: the JSON is what the build wrote from, so every field, including
    unown_table and rate_form0..4, must round-trip.

    encounters.order names the 183 land tables in NARC order; the two non-land
    files (Great Marsh lookout, honey tree) are built separately and are not
    members here. The decoder is the converter run backwards and yields
    species by name, so a decoded record compares directly against the JSON
    on the keys the packed record carries (map_category is not packed).
    """
    import json
    imp = load_importer()
    path = "fielddata/encountdata/pl_enc_data.narc"
    b = ndspy.narc.NARC(built.files[nb[path]]).files
    enc_dir = os.path.join("res", "field", "encounters")
    order = [l.strip() for l in open(os.path.join(enc_dir, "encounters.order"))
             if l.strip()]
    if len(b) != len(order):
        print(f"{path}: NARC has {len(b)} members but encounters.order names "
              f"{len(order)}; comparing the first {min(len(b), len(order))}")
    mismatches = fields_checked = 0
    unpacked_keys = set()
    for i in range(min(len(b), len(order))):
        name = order[i]
        with open(os.path.join(enc_dir, name + ".json"), encoding="utf-8") as f:
            src = json.load(f)
        got = imp.decode_encounter(b[i])
        unpacked_keys |= set(src) - set(got)
        want = {tuple(p): v for p, v in imp.scalar_paths({k: src[k] for k in got})}
        have = {tuple(p): v for p, v in imp.scalar_paths(got)}
        fields_checked += len(have)
        diffs = [f"{'.'.join(str(x) for x in p)}: rom {v!r} != json {want.get(p)!r}"
                 for p, v in have.items() if want.get(p) != v]
        diffs += [f"{'.'.join(str(x) for x in p)}: missing from rom"
                  for p in want if p not in have]
        if diffs:
            mismatches += 1
            print(f"{name}: {len(diffs)} field(s) differ: {diffs[:4]}")
    if mismatches:
        print(f"{path}: {mismatches} of {len(order)} tables differ from their "
              f"source JSON")
    else:
        print(f"{path}: all {len(order)} tables match their source JSON, "
              f"{fields_checked} fields checked, nothing skipped")
    if unpacked_keys:
        print(f"  (JSON keys not in the packed record, so not compared: "
              f"{', '.join(sorted(unpacked_keys))})")
    return mismatches == 0


def check_text(built, ref, nb, nr, msgenc, charmap):
    """Field-level check for pl_msg.narc. Only the banks whose message count is
    unchanged were imported, so the expected result is: those banks match the
    reference message for message, except the handful of slots the importer
    logged as skipped."""
    import tempfile
    imp = load_importer()
    path = "msgdata/pl_msg.narc"
    b = ndspy.narc.NARC(built.files[nb[path]]).files
    r = ndspy.narc.NARC(ref.files[nr[path]]).files
    names = imp.text_bank_names()
    checked = mismatches = skipped_slots = deferred = 0
    prefixed = prefix_bad = 0
    with tempfile.TemporaryDirectory() as tmp:
        for i in range(min(len(b), len(r))):
            if b[i] == r[i]:
                continue
            new = imp.decode_text_bank(msgenc, charmap, r[i], tmp, f"{i}_ref")
            got = imp.decode_text_bank(msgenc, charmap, b[i], tmp, f"{i}_built")
            if len(new) != len(got) or i in imp.TEXT_BANKS_SKIPPED:
                deferred += 1
                # A bank Phase 4 appended to cannot be compared entry for entry
                # against a reference that predates the append, but its shared
                # prefix still has to match, and without this nothing would
                # notice a native species name or move name coming out wrong.
                # Only a bank that grew qualifies: one that shrank or was
                # rewritten has no prefix to speak of.
                if (len(got) > len(new) and i not in imp.TEXT_BANKS_SKIPPED
                        and not isinstance(imp.message_body(new[0]), tuple)):
                    prefixed += 1
                    bad = [f"[{s}] built {imp.message_body(h)!r} != ref {imp.message_body(w)!r}"
                           for s, (w, h) in enumerate(zip(new, got))
                           if imp.message_body(w) != imp.message_body(h)
                           and not isinstance(imp.message_body(w), tuple)
                           and not isinstance(imp.message_body(h), tuple)]
                    if bad:
                        prefix_bad += 1
                        print(f"{names[i]}: {len(bad)} of the {len(new)} entries it "
                              f"shares with the reference differ: {bad[:3]}")
                continue
            if imp.text_targets(i, len(new)) is None:
                deferred += 1
                continue
            checked += 1
            bad = []
            for slot, (want, have) in enumerate(zip(new, got)):
                wv, hv = imp.message_body(want), imp.message_body(have)
                if i == imp.TEXT_BANK_TRAINER_NAMES:
                    # The base ROM carries a {TRNAME} compression tag on every
                    # trainer name; vanilla leaves it off for rivals, the
                    # Frontier brains and the five Battleground trainers, and so
                    # does trainerproc (emit_name's uncompressed_classes and
                    # uncompressed_trainers). DSPRE re-tagged the whole bank on
                    # save, so the tag is not part of any edit and the built ROM
                    # is right to follow vanilla's rule. Compare the names only.
                    wv = wv.replace("{TRNAME}", "") if isinstance(wv, str) else wv
                    hv = hv.replace("{TRNAME}", "") if isinstance(hv, str) else hv
                if wv == hv:
                    continue
                if isinstance(wv, tuple) or isinstance(hv, tuple):
                    skipped_slots += 1  # unused slot that gained or lost text
                    continue
                bad.append(f"[{slot}] built {hv!r} != ref {wv!r}")
            if bad:
                mismatches += 1
                print(f"{names[i]}: {len(bad)} messages differ: {bad[:3]}")
    print(f"{path}: {checked} imported banks checked, {mismatches} with unexpected differences; "
          f"{skipped_slots} unused slots left empty and {deferred} banks deferred, both as intended")
    print(f"{path}: of the deferred, {prefixed} grew in Phase 4 and were compared on the "
          f"entries they still share with the reference; {prefix_bad} disagree")
    return mismatches == 0 and prefix_bad == 0


def check_map_headers(built, ref):
    """sMapHeaders lives in arm9, not a NARC, and sits at a different address in
    every build, so both copies are located by content before being compared."""
    imp = load_importer()
    a, b = built.arm9, ref.arm9
    count = sum(1 for line in open(os.path.join("include", "data", "map_headers.h"))
                if line.startswith("    [MAP_HEADER_"))
    size = count * imp.MAP_HEADER_SIZE
    oa, ob = imp.find_map_header_table(a, count), imp.find_map_header_table(b, count)
    bad = [i for i in range(count)
           if a[oa + i * imp.MAP_HEADER_SIZE : oa + (i + 1) * imp.MAP_HEADER_SIZE]
           != b[ob + i * imp.MAP_HEADER_SIZE : ob + (i + 1) * imp.MAP_HEADER_SIZE]]
    if bad:
        maps = imp.load_enum("map_headers")
        print(f"sMapHeaders: {len(bad)} of {count} headers differ: "
              f"{[maps.get(i, i) for i in bad[:6]]}")
    else:
        print(f"sMapHeaders: all {count} headers identical to the reference")
    return not bad


# Members that no longer match the base ROM on purpose. Phase 4 changes the game
# beyond what the base ROM had, so "identical to the base ROM" stops being the
# truth for these. Each entry names the members, the byte offsets allowed to
# differ, and why; a listed member that differs anywhere else still fails, and an
# unlisted member that differs at all still fails. Same idea as bulk_scripts.py's
# DIVERGED and import_base_rom.py's AUTHORED.
# The 95 native damaging moves that lacked the King's Rock flag, by move id.
# The new moves all carry it, so Ian gave it to these too (2026-09-22).
KINGS_ROCK_NATIVES = {
    7, 8, 9, 12, 23, 29, 32, 34, 40, 41, 44, 51, 52, 53, 58, 59, 60, 61, 62,
    68, 71, 72, 84, 85, 87, 90, 93, 94, 122, 123, 124, 125, 126, 132, 138,
    141, 145, 146, 157, 158, 161, 162, 168, 172, 181, 188, 189, 190, 192,
    196, 202, 209, 217, 221, 223, 228, 231, 232, 242, 243, 246, 247, 248,
    249, 252, 257, 263, 264, 265, 276, 282, 290, 295, 296, 299, 302, 304,
    305, 306, 310, 317, 323, 326, 329, 343, 353, 363, 364, 368, 374, 394,
    405, 411, 412, 448,
}

DIVERGED = {
    "poketool/personal/pl_personal.narc": {
        "offsets": (6, 7),  # type1, type2
        "members": {35, 36, 39, 40, 122, 173, 174, 175, 176, 183, 184,
                    209, 210, 280, 281, 282, 298, 303, 439, 468},
        "why": "twenty species retyped to Fairy (Phase 4 element 1, commit 64021978c)",
    },
    # A list when more than one change touches the archive; a member passes if
    # any one entry allows every byte it differs at.
    "poketool/waza/pl_waza_tbl.narc": [
        {
            "offsets": (4,),  # type
            "members": {186, 204, 236},
            "why": "Charm, Sweet Kiss and Moonlight retyped to Fairy (Phase 4 element 1)",
        },
        {
            "offsets": (11,),  # flags
            "members": KINGS_ROCK_NATIVES,
            "why": "native damaging moves given the King's Rock flag (Ian, 2026-09-22)",
        },
        {
            "offsets": (8, 9),  # range
            "members": {139},
            "why": "Poison Gas hits both foes, not the partner too (Ian, 2026-09-22)",
        },
    ],
}


def diverged_rules(path):
    """DIVERGED's entries for path, always as a list."""
    rule = DIVERGED.get(path, [])
    return rule if isinstance(rule, list) else [rule]


def diverged_why(path):
    return "; ".join(r["why"] for r in diverged_rules(path))


# The three per-species archives are built from one registry, in this order:
# nothing, the species, EGG, BAD_EGG, then the twelve alternate-form records.
# Phase 4 element 3 inserted 159 species before EGG, so everything after the
# natives sits at a different index from the reference ROM's. This maps a
# reference index onto the built one so the two can still be compared.
SPECIES_ARCHIVES = ("poketool/personal/pl_personal.narc",
                    "poketool/personal/evo.narc",
                    "poketool/personal/wotbl.narc")

# Whole members of a species archive that no longer match the reference on
# purpose, where the difference is not confined to a few byte offsets the way
# DIVERGED's entries are. Keyed by the reference's member index.
DIVERGED_MEMBERS = {
    "poketool/personal/evo.narc": {
        "members": {57, 123, 130, 133, 194, 370, 428},
        "why": "seven natives gain an evolution into a new species "
               "(Primeape, Scyther, Gyarados, Eevee, Wooper, Luvdisc, Lopunny; "
               "Phase 4 element 3)",
    },
}
REF_NATIVE_COUNT = 494  # 0 plus the 493 species the reference ROM has


def reference_to_built(i, n_built, n_ref):
    """Where reference member i lives in the built archive."""
    if i < REF_NATIVE_COUNT:
        return i
    return i + (n_built - n_ref)


# The species record grew from 44 bytes to 48 in Phase 4 element 2, so
# pl_personal can no longer be compared byte for byte against a reference ROM
# that still has the old one. This lays the two layouts side by side instead.
# Both are the same fields in the same order; only the abilities moved.
PERSONAL_OLD_SIZE = 44
PERSONAL_NEW_SIZE = 48
PERSONAL_ABILITIES_AT = 0x16
PERSONAL_BASE_EXP_AT = 0x09


def personal_fields(member):
    """(head, abilities, base exp, tail) for a species record of either size.
    Two fields have moved since the reference ROM was made: the abilities are
    u16 now, and base experience left its byte at 0x09 for the two bytes of
    padding at the end, because Generation 7 values run past 255. Both are
    pulled out so what is left can be compared straight across."""
    head = bytearray(member[:PERSONAL_ABILITIES_AT])
    base_exp = head[PERSONAL_BASE_EXP_AT]
    head[PERSONAL_BASE_EXP_AT] = 0
    if len(member) == PERSONAL_OLD_SIZE:
        abilities = (member[0x16], member[0x17], 0)
        # 0x1A..0x1B is padding in the old layout and the hidden ability in the
        # new one, so it is left out of both tails.
        tail = member[0x18:0x1A] + member[0x1C:]
    else:
        abilities = struct.unpack("<3H", member[0x16:0x1C])
        base_exp = struct.unpack("<H", member[0x1E:0x20])[0]
        tail = member[0x1C:0x1E] + member[0x20:]
    return bytes(head), abilities, base_exp, tail


def check_personal(b, r, path):
    """Compare pl_personal field by field. The built archive holds more species
    than the reference and the ones after the natives have moved, so each
    reference member is looked up where it now lives; the shared ones have to
    agree, allowing the Fairy retypes and a hidden-ability slot the reference
    has no room for."""
    rule = DIVERGED.get(path, {"members": set(), "offsets": ()})
    bad, intended, extra = [], [], max(0, len(b) - len(r))
    for i in range(len(r)):
        j = reference_to_built(i, len(b), len(r))
        if j >= len(b):
            bad.append(i)
            continue
        bh, ba, bx, bt = personal_fields(b[j])
        rh, ra, rx, rt = personal_fields(r[i])
        if bt.rstrip(b"\0") != rt.rstrip(b"\0") or ba[:2] != ra[:2] or bx != rx:
            bad.append(i)
            continue
        if bh == rh:
            continue
        if i in rule["members"] and all(bh[o] == rh[o] or o in rule["offsets"]
                                        for o in range(len(bh))):
            intended.append(i)
        else:
            bad.append(i)
    print(f"{path}: {len(b)} members against the reference's {len(r)}; "
          f"{len(bad)} disagree, {len(intended)} differ only at the intended bytes"
          + (f", {extra} are new species" if extra else ""))
    if bad:
        i = bad[0]
        j = reference_to_built(i, len(b), len(r))
        print(f"   first: reference member {i} against built {j}\n"
              f"          built {b[j].hex() if j < len(b) else '(missing)'}\n"
              f"          ref   {r[i].hex()}")
    return not bad


def intended_divergence(path, i, built_member, ref_member):
    """True when member i of `path` differs from the reference only at bytes a
    DIVERGED entry allows for it."""
    if len(built_member) != len(ref_member):
        return False
    return any(i in rule["members"]
               and all(built_member[o] == ref_member[o] or o in rule["offsets"]
                       for o in range(len(built_member)))
               for rule in diverged_rules(path))


# The level-up learnset entry grew from one packed u16, move:9 / level:7, to a
# pair of whole halfwords in Phase 4 element 4, because there are more than 511
# moves now. So wotbl can no longer be compared byte for byte against a
# reference ROM that still has the packed one; both sides are decoded to
# [(level, move)] and those are compared instead.
WOTBL = "poketool/personal/wotbl.narc"


def learnset_entries(member, packed):
    """[(level, move)] for one wotbl member, in either layout."""
    out = []
    if packed:
        for i in range(0, len(member) - 1, 2):
            (entry,) = struct.unpack_from("<H", member, i)
            if entry == 0xFFFF:
                break
            out.append((entry >> 9, entry & 0x1FF))
    else:
        for i in range(0, len(member) - 3, 4):
            level, move = struct.unpack_from("<2H", member, i)
            if level == 0xFFFF:
                break
            out.append((level, move))
    return out


def check_species_archive(b, r, path):
    """evo and wotbl, which are a straight byte comparison once the reference's
    indices are mapped onto the built archive's."""
    allowed = DIVERGED_MEMBERS.get(path, {"members": set(), "why": ""})
    learnsets = path == WOTBL
    bad, padded, intended = [], [], []
    for i in range(len(r)):
        j = reference_to_built(i, len(b), len(r))
        if j >= len(b):
            bad.append(i)
            continue
        if learnsets:
            if learnset_entries(b[j], False) != learnset_entries(r[i], True):
                (intended if i in allowed["members"] else bad).append(i)
            continue
        if b[j] != r[i]:
            if i in allowed["members"]:
                intended.append(i)
            else:
                (padded if b[j].rstrip(b"\0") == r[i].rstrip(b"\0") else bad).append(i)
    extra = len(b) - len(r)
    if padded:
        print(f"{path}: {len(padded)} members differ only in trailing zero padding: {padded[:20]}")
    if intended:
        print(f"{path}: {len(intended)} members differ on purpose, {allowed['why']}: {intended}")
    print(f"{path}: {len(b)} members against the reference's {len(r)}; {len(bad)} disagree"
          + (" (compared as decoded learnsets, the entry format widened in element 4)"
             if learnsets else "")
          + (f", {extra} are new species" if extra > 0 else ""))
    if bad:
        i = bad[0]
        j = reference_to_built(i, len(b), len(r))
        print(f"   first: reference member {i} against built {j}\n"
              f"          built {b[j].hex() if j < len(b) else '(missing)'}\n"
              f"          ref   {r[i].hex()}")
    return not bad


WAZA = "poketool/waza/pl_waza_tbl.narc"


def check_move_table(b, r, path):
    """pl_waza_tbl, which element 4 appended to rather than rearranged.

    The reference's members stay where they are, all 471 of them, including the
    three inaccessible retail records at 468..470 that are ordinary move
    directories now. Everything from 471 up is a move Hardlove added, so the
    check is the ordinary byte comparison over the reference's range plus a
    count of the tail.
    """
    bad, intended = [], []
    for i in range(len(r)):
        if i >= len(b):
            bad.append(i)
        elif b[i] != r[i]:
            (intended if intended_divergence(path, i, b[i], r[i]) else bad).append(i)
    extra = len(b) - len(r)
    if intended:
        print(f"{path}: {len(intended)} members differ only at the intended bytes, "
              f"{diverged_why(path)}: {intended}")
    print(f"{path}: {len(b)} members against the reference's {len(r)}; "
          f"{len(bad)} disagree"
          + (f", {extra} are new moves" if extra > 0 else ""))
    if bad:
        i = bad[0]
        print(f"   first: member {i}\n"
              f"          built {b[i].hex() if i < len(b) else '(missing)'}\n"
              f"          ref   {r[i].hex()}")
    return not bad


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--built", required=True)
    ap.add_argument("--ref", help="reference ROM; not needed with --source")
    ap.add_argument("--source", action="store_true",
                    help="M7: check pl_enc_data.narc against res/field/encounters/*.json "
                         "field by field, no reference ROM involved")
    ap.add_argument("--map-headers", action="store_true",
                    help="compare arm9's sMapHeaders against the reference ROM's")
    ap.add_argument("--text", action="store_true",
                    help="message-level check of pl_msg.narc instead of a byte comparison")
    ap.add_argument("--msgenc", default="build/tools/msgenc/msgenc")
    ap.add_argument("--charmap", default="tools/msgenc/charmap.txt")
    ap.add_argument("--encounters", action="store_true",
                    help="field-level check of pl_enc_data.narc instead of a byte comparison")
    ap.add_argument("paths", nargs="*", default=DEFAULT)
    a = ap.parse_args()
    built = ndspy.rom.NintendoDSRom.fromFile(a.built)
    nb = walk(built.filenames)
    if a.source:
        sys.exit(0 if check_encounters_source(built, nb) else 1)
    if not a.ref:
        ap.error("--ref is required for every check except --source")
    ref = ndspy.rom.NintendoDSRom.fromFile(a.ref)
    nr = walk(ref.filenames)
    ok = True
    if a.encounters:
        sys.exit(0 if check_encounters(built, ref, nb, nr) else 1)
    if a.text:
        sys.exit(0 if check_text(built, ref, nb, nr, a.msgenc, a.charmap) else 1)
    if a.map_headers:
        sys.exit(0 if check_map_headers(built, ref) else 1)
    for p in a.paths:
        b, r = ndspy.narc.NARC(built.files[nb[p]]).files, ndspy.narc.NARC(ref.files[nr[p]]).files
        if p == "poketool/personal/pl_personal.narc":
            ok = check_personal(b, r, p) and ok
            continue
        if p in SPECIES_ARCHIVES:
            ok = check_species_archive(b, r, p) and ok
            continue
        if p == WAZA:
            ok = check_move_table(b, r, p) and ok
            continue
        if len(b) != len(r):
            print(f"{p}: member count {len(b)} vs {len(r)}"); ok = False
        bad = [i for i in range(min(len(b), len(r))) if b[i] != r[i]]
        # DSPRE pads some members with extra zero bytes; content is what matters
        padded = [i for i in bad if b[i].rstrip(b"\0") == r[i].rstrip(b"\0")]
        bad = [i for i in bad if i not in padded]
        if padded:
            print(f"{p}: {len(padded)} members differ only in trailing zero padding: {padded[:20]}")
        intended = [i for i in bad if intended_divergence(p, i, b[i], r[i])]
        bad = [i for i in bad if i not in intended]
        if intended:
            print(f"{p}: {len(intended)} members differ only at the intended bytes, "
                  f"{diverged_why(p)}: {intended[:20]}")
        if bad:
            ok = False
            print(f"{p}: {len(bad)} members differ: {bad[:20]}{' ...' if len(bad) > 20 else ''}")
            i = bad[0]
            print(f"   first: built {b[i][:48].hex()}\n          ref   {r[i][:48].hex()}")
        elif intended:
            print(f"{p}: identical apart from the intended bytes ({len(b)} members)")
        else:
            print(f"{p}: identical ({len(b)} members)")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()

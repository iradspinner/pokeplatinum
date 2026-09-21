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
    with tempfile.TemporaryDirectory() as tmp:
        for i in range(min(len(b), len(r))):
            if b[i] == r[i]:
                continue
            new = imp.decode_text_bank(msgenc, charmap, r[i], tmp, f"{i}_ref")
            got = imp.decode_text_bank(msgenc, charmap, b[i], tmp, f"{i}_built")
            if len(new) != len(got) or i in imp.TEXT_BANKS_SKIPPED:
                deferred += 1
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
    return mismatches == 0


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
        if len(b) != len(r):
            print(f"{p}: member count {len(b)} vs {len(r)}"); ok = False
        bad = [i for i in range(min(len(b), len(r))) if b[i] != r[i]]
        # DSPRE pads some members with extra zero bytes; content is what matters
        padded = [i for i in bad if b[i].rstrip(b"\0") == r[i].rstrip(b"\0")]
        bad = [i for i in bad if i not in padded]
        if padded:
            print(f"{p}: {len(padded)} members differ only in trailing zero padding: {padded[:20]}")
        if bad:
            ok = False
            print(f"{p}: {len(bad)} members differ: {bad[:20]}{' ...' if len(bad) > 20 else ''}")
            i = bad[0]
            print(f"   first: built {b[i][:48].hex()}\n          ref   {r[i][:48].hex()}")
        else:
            print(f"{p}: identical ({len(b)} members)")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()

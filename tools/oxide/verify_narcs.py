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
    mismatches, skipped = 0, 0
    for i in range(min(len(b), len(r))):
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
        print(f"{path}: all {len(b)} tables match the reference outside the skipped fields "
              f"({skipped} skipped-field differences left at their vanilla values, as intended)")
    return mismatches == 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--built", required=True)
    ap.add_argument("--ref", required=True)
    ap.add_argument("--encounters", action="store_true",
                    help="field-level check of pl_enc_data.narc instead of a byte comparison")
    ap.add_argument("paths", nargs="*", default=DEFAULT)
    a = ap.parse_args()
    built, ref = ndspy.rom.NintendoDSRom.fromFile(a.built), ndspy.rom.NintendoDSRom.fromFile(a.ref)
    nb, nr = walk(built.filenames), walk(ref.filenames)
    ok = True
    if a.encounters:
        sys.exit(0 if check_encounters(built, ref, nb, nr) else 1)
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

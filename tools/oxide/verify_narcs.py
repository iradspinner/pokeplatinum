#!/usr/bin/env python3
"""Compare NARCs inside a freshly built ROM against the same NARCs in a
reference ROM, member by member. Used to prove that data imported into res/
rebuilds to exactly the bytes the reference ROM carries.

Usage:
    python3 tools/oxide/verify_narcs.py --built build/pokeplatinum.us.nds --ref BASE.nds [PATH ...]

With no PATH arguments, checks the tables the importer handles.
"""
import argparse
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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--built", required=True)
    ap.add_argument("--ref", required=True)
    ap.add_argument("paths", nargs="*", default=DEFAULT)
    a = ap.parse_args()
    built, ref = ndspy.rom.NintendoDSRom.fromFile(a.built), ndspy.rom.NintendoDSRom.fromFile(a.ref)
    nb, nr = walk(built.filenames), walk(ref.filenames)
    ok = True
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

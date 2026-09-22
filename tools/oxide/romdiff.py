#!/usr/bin/env python3
"""Say exactly what differs between two ROMs, down to archive members.

Used to prove a change touched only what it meant to: build the new ROM, then
compare it with a verified ROM of the previous commit (one fetched with
tools/oxide/fetch-rom, whose hash GitHub vouches for). Element 4's effect
scripts, for instance, should change members of battle/skill/be_seq.narc and
nothing else, not arm9, not an overlay, not another archive.

    tools/oxide/romdiff.py OLD.nds NEW.nds
"""
import sys

import ndspy.narc
import ndspy.rom


def names(rom):
    """Path to file id for every named file in the ROM's filesystem."""
    out = {}

    def walk(folder, prefix=""):
        for i, n in enumerate(folder.files):
            out[prefix + n] = folder.firstID + i
        for sub, f in folder.folders:
            walk(f, prefix + sub + "/")

    walk(rom.filenames)
    return out


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__.strip())
    a = ndspy.rom.NintendoDSRom.fromFile(sys.argv[1])
    b = ndspy.rom.NintendoDSRom.fromFile(sys.argv[2])
    print("arm9 identical:", a.arm9 == b.arm9, "| arm7 identical:", a.arm7 == b.arm7)
    if len(a.files) != len(b.files):
        print("file count differs: %d vs %d" % (len(a.files), len(b.files)))
    differing = [i for i in range(min(len(a.files), len(b.files))) if a.files[i] != b.files[i]]
    by_id = {v: k for k, v in names(b).items()}
    # Files with no name are the code overlays; a data change should leave them all alone.
    print("differing files: %d" % len(differing))
    for i in differing:
        path = by_id.get(i, "(overlay or unnamed file %d)" % i)
        line = "    %s" % path
        if path.endswith(".narc"):
            ma = ndspy.narc.NARC(a.files[i]).files
            mb = ndspy.narc.NARC(b.files[i]).files
            members = [k for k in range(min(len(ma), len(mb))) if ma[k] != mb[k]]
            line += ": %d vs %d members, differing %s" % (len(ma), len(mb), members)
        print(line)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Say exactly what differs between two ROMs, down to archive members.

Used to prove a change touched only what it meant to: build the new ROM, then
compare it with a verified ROM of the previous commit (one fetched with
tools/oxide/fetch-rom, whose hash GitHub vouches for). Element 4's effect
scripts, for instance, should change members of battle/skill/be_seq.narc and
nothing else, not arm9, not an overlay, not another archive.

A change to C is different, because it can grow an overlay, and then every
call into that overlay from elsewhere moves with it. So when an overlay's size
changes, the other code files are checked word by word: a difference is
explained if it is a branch or an address whose old and new values both point
into a grown overlay. Anything else is printed as unexplained, and an
unexplained difference means the change reached further than it should have.
Element 4's first C batch (2026-09-22) grew overlay 16 by 128 bytes, and the
137 differences it caused in arm9 and overlays 13 and 14 were all of the
explained kind.

    tools/oxide/romdiff.py OLD.nds NEW.nds
"""
import struct
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


def thumb_bl(data, at, base):
    """Target of a Thumb BL or BLX pair starting at `at`, or None."""
    if at < 0 or at + 4 > len(data):
        return None
    h1, h2 = struct.unpack_from("<HH", data, at)
    if (h1 & 0xF800) != 0xF000 or (h2 & 0xE800) != 0xE800:
        return None
    off = ((h1 & 0x7FF) << 12) | ((h2 & 0x7FF) << 1)
    if off & 0x400000:
        off -= 0x800000
    return base + at + 4 + off


def arm_bl(data, at, base):
    """Target of an ARM-mode BL at word `at`, or None."""
    if at < 0 or at + 4 > len(data):
        return None
    w, = struct.unpack_from("<I", data, at)
    if (w & 0x0F000000) != 0x0B000000:
        return None
    off = w & 0xFFFFFF
    if off & 0x800000:
        off -= 0x1000000
    return base + at + 8 + (off << 2)


def explain(old, new, base, regions):
    """Sort the differing bytes of one code file into branches into a grown
    overlay, addresses into one, and the rest."""
    def inside(addr):
        return addr is not None and any(lo <= addr <= hi for lo, hi in regions)

    branches = addresses = 0
    unexplained = []
    covered = set()
    for j in range(min(len(old), len(new))):
        if old[j] == new[j] or j in covered:
            continue
        found = None
        for at in (j & ~1, (j & ~1) - 2):
            if inside(thumb_bl(old, at, base)) and inside(thumb_bl(new, at, base)):
                found = ("branch", at)
                break
        word = j & ~3
        if found is None and inside(arm_bl(old, word, base)) and inside(arm_bl(new, word, base)):
            found = ("branch", word)
        if found is None and word + 4 <= min(len(old), len(new)):
            pa, = struct.unpack_from("<I", old, word)
            pb, = struct.unpack_from("<I", new, word)
            if inside(pa) and inside(pb):
                found = ("address", word)
        if found is None:
            unexplained.append(base + j)
            continue
        covered.update(range(found[1], found[1] + 4))
        if found[0] == "branch":
            branches += 1
        else:
            addresses += 1
    return branches, addresses, unexplained


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
    oa, ob = a.loadArm9Overlays(), b.loadArm9Overlays()
    overlay_of_file = {ov.fileID: k for k, ov in ob.items()}
    # Files with no name are the code overlays; a data change should leave them all alone.
    print("differing files: %d" % len(differing))
    for i in differing:
        path = by_id.get(i)
        if path is None:
            path = ("overlay %d" % overlay_of_file[i]) if i in overlay_of_file else "(unnamed file %d)" % i
        line = "    %s" % path
        if path.endswith(".narc"):
            ma = ndspy.narc.NARC(a.files[i]).files
            mb = ndspy.narc.NARC(b.files[i]).files
            members = [k for k in range(min(len(ma), len(mb))) if ma[k] != mb[k]]
            line += ": %d vs %d members, differing %s" % (len(ma), len(mb), members)
        print(line)

    grown = [k for k in sorted(ob) if k in oa and len(oa[k].data) != len(ob[k].data)]
    if not grown:
        return 0
    # An address may point one past an overlay's code, at its end, so the
    # region runs to the larger of the two ends inclusive.
    regions = [(ob[k].ramAddress, ob[k].ramAddress + max(len(oa[k].data), len(ob[k].data)))
               for k in grown]
    for k in grown:
        print("code relink: overlay %d changed size, %d to %d bytes (%+d)"
              % (k, len(oa[k].data), len(ob[k].data), len(ob[k].data) - len(oa[k].data)))
    code = [("arm9", a.arm9, b.arm9, a.arm9RamAddress)]
    code += [("overlay %d" % k, oa[k].data, ob[k].data, ob[k].ramAddress)
             for k in sorted(ob) if k in oa and k not in grown and oa[k].data != ob[k].data]
    bad = 0
    for label, old, new, base in code:
        if old == new:
            continue
        if len(old) != len(new):
            print("    %s: also changed size, %d to %d bytes; not explained by a relink"
                  % (label, len(old), len(new)))
            bad += 1
            continue
        branches, addresses, unexplained = explain(old, new, base, regions)
        print("    %s: %d branches and %d addresses into a grown overlay, %d bytes unexplained%s"
              % (label, branches, addresses, len(unexplained),
                 (" at " + ", ".join("0x%08x" % x for x in unexplained[:8])) if unexplained else ""))
        bad += bool(unexplained)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())

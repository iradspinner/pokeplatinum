#!/usr/bin/env python3
"""Say which functions and variables a C change really touched, symbol by symbol.

romdiff.py explains the knock-on differences of an overlay that changed size,
but a change to arm9 (`src/pokemon.c`, `src/item.c` and the rest of the static
module) moves every overlay's load address with it, so every overlay differs
and romdiff has nothing to anchor on. Element 7's first commit (2026-09-27)
grew arm9 by 192 bytes for 24 new item ids and changed all 119 code files.

`symdiff.py` compares the two maps alone, which says what was added,
removed or resized but not what changed inside a symbol that kept its size.
This tool anchors on the linker's own map as well, and then reads the bytes. Each build writes
`build/main.nef.xMAP`, which lists every symbol with its address, size and
object file. Keep the map beside each ROM you compare. For every symbol in
both builds it compares the old bytes with the new, and a difference is
explained when it is an address, or a BL or BLX target, that points at the
same place in both builds: the same symbol, at the same offset into it, even
though that symbol moved. What is left is printed as a changed symbol, and
the list should be exactly the functions and tables the commit meant to
change. Symbols that exist in one build only are listed too.

    tools/oxide/symcheck.py OLD.nds OLD.xMAP NEW.nds NEW.xMAP

It exits non-zero when a symbol changed, so read the list rather than the
exit code; the point is that the list is short and every entry is intended.
Data archives are romdiff's; run both.
"""
import bisect
import re
import struct
import sys

import ndspy.rom

SYM = re.compile(r"^  ([0-9A-F]{8}) ([0-9A-F]{8}) (\S+)\s+(\S+)\t\((.*)\)$")
SECTION = re.compile(r"^# \.(\S+)$")
OVERLAY_ID = re.compile(r"^#>([0-9A-F]{8})\s+SDK_OVERLAY_(\S+)_ID ")
ANCHOR = re.compile(r"^#>([0-9A-F]{8})\s+(\S+) \(linker command file\)")


class Map:
    """One build's symbols, grouped by the module they are linked into."""

    def __init__(self, path):
        self.symbols = {}  # module -> list of (addr, size, key)
        self.overlay_ids = {}  # module name -> overlay id
        module = None
        for line in open(path, encoding="latin-1"):
            line = line.rstrip("\n")
            m = SECTION.match(line)
            if m:
                name = m.group(1)
                module = name[:-4] if name.endswith(".bss") else name
                continue
            m = OVERLAY_ID.match(line)
            if m:
                self.overlay_ids[m.group(2)] = int(m.group(1), 16)
                continue
            if module is None:
                continue
            m = ANCHOR.match(line)
            if m and int(m.group(1), 16) >= 0x01000000 and "SIZE" not in m.group(2):
                # The linker's own labels (section ends, the arena start) are
                # kept as empty symbols, so an address that points at one
                # still has something to be matched by.
                self.symbols.setdefault(module, []).append((int(m.group(1), 16), 0, (m.group(2), "linker")))
                continue
            m = SYM.match(line)
            if not m:
                continue
            addr, size = int(m.group(1), 16), int(m.group(2), 16)
            name, obj = m.group(4), m.group(5)
            if name.startswith("$") or name.startswith(".") or (size == 0 and not name[0].isalpha()):
                continue
            self.symbols.setdefault(module, []).append((addr, size, (name, obj)))
        self.by_key = {}
        for module, syms in self.symbols.items():
            syms.sort()
            # The compiler numbers its anonymous constants and static locals
            # (@14123, pillarRooms$28162), and the numbers shift whenever a
            # file recompiles, so those are keyed by their order within their
            # object file instead of by name.
            for i, (addr, size, (name, obj)) in enumerate(syms):
                if name.startswith("@") or "$" in name[1:]:
                    syms[i] = (addr, size, (name.split("$")[0] if "$" in name[1:] else "@", obj))
            seen = {}
            for i, (addr, size, key) in enumerate(syms):
                n = seen.get(key, 0)
                seen[key] = n + 1
                self.by_key[(module, key, n)] = (addr, size)
                syms[i] = (addr, size, key, n)
        self.starts = {m: [s[0] for s in syms] for m, syms in self.symbols.items()}
        # How far the module's own symbols reach; a gap past this is not the
        # module's, even if a linker label lies beyond it.
        self.ends = {m: max([s[0] + s[1] for s in syms if s[2][1] != "linker"] or [0])
                     for m, syms in self.symbols.items()}

    def locate(self, module, addr):
        """The symbol key and offset that `addr` falls in within `module`, or
        None. An address one past a symbol's end counts as its end."""
        syms = self.symbols.get(module)
        if not syms:
            return None
        i = bisect.bisect_right(self.starts[module], addr) - 1
        if i < 0:
            return None
        # The last symbol starting at or before addr; an address in a gap
        # between symbols (padding, the exception tables) is placed by the
        # symbol before it, which moves the gap with it.
        # A linker label only places an address that is exactly on it.
        while i >= 0 and syms[i][2][1] == "linker" and syms[i][0] != addr:
            i -= 1
        if i < 0:
            return None
        lo, size, key, n = syms[i]
        if addr > lo + size and addr > self.ends[module]:
            return None
        return key, n, addr - lo


def module_bytes(rom, mp):
    """Bytes of each module as the ROM stores them, keyed by module name."""
    out = {}
    base = 0x02000000
    out["main"] = (base, rom.arm9)
    ovs = rom.loadArm9Overlays()
    for name, oid in mp.overlay_ids.items():
        if oid in ovs:
            out[name] = (ovs[oid].ramAddress, ovs[oid].data)
    return out


_cache = {}


def translate(old, new, module, addr):
    """Every address `addr` (an old-build address seen from `module`) could be
    in the new build: its own module first, then arm9, then any overlay."""
    if (module, addr) in _cache:
        return _cache[(module, addr)]
    found = set()
    for m in [module, "main", "ITCM", "DTCM"] + [k for k in old.symbols if k not in (module, "main")]:
        loc = old.locate(m, addr)
        if loc is None:
            continue
        key, n, off = loc
        hit = new.by_key.get((m, key, n))
        if hit is not None:
            found.add(hit[0] + off)
        if found and m in (module, "main"):
            break
    _cache[(module, addr)] = found
    return found


def thumb_bl(data, at, base):
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
    if at < 0 or at + 4 > len(data) or at & 3:
        return None
    w, = struct.unpack_from("<I", data, at)
    if (w & 0x0E000000) != 0x0A000000:
        return None
    off = w & 0xFFFFFF
    if off & 0x800000:
        off -= 0x1000000
    return base + at + 8 + (off << 2)


def compare(old, new, module, a_bytes, a_base, b_bytes, b_base, a_addr, b_addr, size):
    """Offsets inside one symbol that no moved address or branch explains."""
    ao, bo = a_addr - a_base, b_addr - b_base
    size = min(size, len(a_bytes) - ao, len(b_bytes) - bo)
    A, B = a_bytes[ao:ao + size], b_bytes[bo:bo + size]
    bad, covered = [], set()

    def ok(ta, tb):
        return ta is not None and tb is not None and (ta == tb or tb in translate(old, new, module, ta)
                                                     or (tb & ~3) in {t & ~3 for t in translate(old, new, module, ta)})

    for j in range(size):
        if A[j] == B[j] or j in covered:
            continue
        span = None
        for at in (j & ~1, (j & ~1) - 2):
            if at >= 0 and ok(thumb_bl(a_bytes, ao + at, a_base), thumb_bl(b_bytes, bo + at, b_base)):
                span = at
                break
        w = j & ~3
        if span is None and ok(arm_bl(a_bytes, ao + w, a_base), arm_bl(b_bytes, bo + w, b_base)):
            span = w
        if span is None and w + 4 <= size:
            pa, = struct.unpack_from("<I", A, w)
            pb, = struct.unpack_from("<I", B, w)
            if ok(pa, pb):
                span = w
        if span is None:
            bad.append(j)
            continue
        covered.update(range(span, span + 4))
    return bad


def main():
    if len(sys.argv) != 5:
        sys.exit(__doc__.strip())
    ra, ma = ndspy.rom.NintendoDSRom.fromFile(sys.argv[1]), Map(sys.argv[2])
    rb, mb = ndspy.rom.NintendoDSRom.fromFile(sys.argv[3]), Map(sys.argv[4])
    ba, bb = module_bytes(ra, ma), module_bytes(rb, mb)
    changed, added, removed = [], [], []
    for (module, key, n), (a_addr, a_size) in sorted(ma.by_key.items(), key=lambda kv: kv[1][0]):
        hit = mb.by_key.get((module, key, n))
        if hit is None:
            removed.append((module, key))
            continue
        if module not in ba or module not in bb:
            continue
        b_addr, b_size = hit
        a_base, a_bytes = ba[module]
        b_base, b_bytes = bb[module]
        if a_addr - a_base >= len(a_bytes) or b_addr - b_base >= len(b_bytes):
            continue  # .bss: no bytes in the ROM
        if a_size != b_size:
            changed.append((module, key, "size %d to %d" % (a_size, b_size)))
            continue
        bad = compare(ma, mb, module, a_bytes, a_base, b_bytes, b_base, a_addr, b_addr, a_size)
        if bad:
            changed.append((module, key, "%d bytes from +0x%x" % (len(bad), bad[0])))
    for k in mb.by_key:
        if k not in ma.by_key:
            added.append((k[0], k[1]))
    for label, rows in (("changed", changed), ("only in the new build", added), ("only in the old build", removed)):
        print("%s: %d" % (label, len(rows)))
        for r in rows:
            print("    %s %s (%s)%s" % (r[0], r[1][0], r[1][1], (": " + r[2]) if len(r) > 2 else ""))
    return 1 if changed or added or removed else 0


if __name__ == "__main__":
    sys.exit(main())

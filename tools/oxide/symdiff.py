"""Say which symbols differ between two builds' linker maps.

romdiff.py explains a relink only when an overlay changes size. When arm9
itself grows, every overlay's calls into arm9 move and romdiff reports them
all as unexplained, so a byte comparison cannot show what a C change
touched. The linker map can: this lists the symbols one build has and the
other lacks, and the ones whose size changed. The design doc's findings log
(2026-09-21) is the reasoning: after a relink the symbol table is the
evidence, not the bytes.

The compiler numbers its anonymous constants and static locals (@14123,
pillarRooms$28162), and the numbers shift whenever a file recompiles, so
those are compared as counts of (object file, name without the number,
size) rather than by name.

    tools/oxide/symdiff.py OLD/main.nef.xMAP NEW/main.nef.xMAP

The map is build/main.nef.xMAP after `make rom`. Keep a copy of the
previous commit's before building the next.
"""
import re
import sys
from collections import Counter

LINE = re.compile(r"^\s+([0-9A-F]{8}) ([0-9A-F]{8}) (\S+)\s+(\S+)\s+\((\S+)\)")


def load(path):
    named, numbered = {}, Counter()
    with open(path, errors="replace") as f:
        for line in f:
            m = LINE.match(line)
            if not m:
                continue
            _addr, size, _section, name, obj = m.groups()
            size = int(size, 16)
            if name in ("$a", "$t", "$d"):
                continue  # ARM, Thumb and data mapping symbols, not code or data
            if name.startswith("@"):
                numbered[(obj, "@", size)] += 1
            elif "$" in name[1:]:
                numbered[(obj, name.split("$")[0], size)] += 1
            else:
                named[(name, obj)] = size
    return named, numbered


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__.strip())
    (a, an), (b, bn) = load(sys.argv[1]), load(sys.argv[2])
    print("named symbols: %d vs %d; numbered: %d vs %d"
          % (len(a), len(b), sum(an.values()), sum(bn.values())))
    for k in sorted(set(b) - set(a)):
        print("added    %s (%s) size %d" % (k[0], k[1], b[k]))
    for k in sorted(set(a) - set(b)):
        print("removed  %s (%s)" % k)
    for k in sorted(set(a) & set(b)):
        if a[k] != b[k]:
            print("resized  %s (%s) %d -> %d" % (k[0], k[1], a[k], b[k]))
    for k in sorted(bn - an):
        print("numbered added    %s %s size %d" % k)
    for k in sorted(an - bn):
        print("numbered removed  %s %s size %d" % k)
    return 0


if __name__ == "__main__":
    sys.exit(main())

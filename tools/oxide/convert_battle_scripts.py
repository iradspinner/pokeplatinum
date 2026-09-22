#!/usr/bin/env python3
"""Convert hg-engine's battle scripts into Platinum's dialect.

Phase 4 element 4. The 452 imported moves reference 116 battle effects Platinum
does not have, currently stubs. hg-engine has all 116, and the two projects'
battle scripts turn out to be the same language: the opcodes are the same, the
structure is the same, and what differs is a header and about sixty constant
names. `effect_script_0006` is identical in both once those are applied.

**The rename map is derived, not written down.** Both projects ship effect
scripts 0 to 276, so this tool lines those 277 pairs up and reads the renames
straight off them: where hg-engine has one identifier in a position and
Platinum has another, that is a rename, witnessed by however many files agree.
198 of the 277 pairs line up token for token and yield 56 renames with no
ambiguity. That means the map cannot drift from the tree, and a bad rename
would have to be wrong in the same way in every file that witnesses it.

Two details the alignment has to get right. A `|`-joined flag list carries no
order, so the two sides are compared as sets and only the leftovers pair up;
without that, four `MOVE_SIDE_EFFECT_*` flags that both projects already share
look like renames of each other. And 79 of the 277 pairs do not line up,
because those effects genuinely differ between the games; they are excluded
from the derivation and reported by `--selftest`.

**What the self-test says, and why the map is finished at 56.** Of the 198
pairs that line up, 161 convert to Platinum's own script exactly. Every one of
the remaining 37 differs only in which `MOVE_SIDE_EFFECT_*` flag or which
subscript the effect uses, and those four flags are defined with identical
values in both projects (`CHECK_HP` 1<<28 through `TO_DEFENDER` 1<<31), so they
are not renames and must never be translated. hg-engine simply made some
effects behave differently, which is its right and not something a converter
should paper over. There is no identifier left unaccounted for.

    python3 tools/oxide/convert_battle_scripts.py --selftest
    python3 tools/oxide/convert_battle_scripts.py --map
"""

import argparse
import collections
import glob
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HG = os.environ.get("HG_ENGINE", os.path.expanduser("~/hg-engine"))
HG_EFFECTS = os.path.join(HG, "data", "battle_scripts", "effects")
HG_SUBSCRIPTS = os.path.join(HG, "data", "battle_scripts", "subscripts")
PLAT_EFFECTS = os.path.join(ROOT, "res", "battle", "scripts", "effects")

PLATINUM_EFFECTS = 277      # the ids both projects have
HEADER = '#include "macros/btlcmd.inc"\n\n\n'

TOKEN = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")


def hg_index(folder, prefix):
    out = {}
    for p in glob.glob(os.path.join(folder, prefix + "_*.s")):
        m = re.match(prefix + r"_(\d{4})_(.+)\.s$", os.path.basename(p))
        if m:
            out[int(m.group(1))] = (m.group(2), p)
    return out


def body_lines(path):
    """A script's meaningful lines, with each project's own preamble dropped."""
    out = []
    for line in open(path, encoding="utf-8"):
        line = line.split("//")[0].rstrip()
        if not line.strip():
            continue
        if line.startswith(("#include", ".include")) or line.strip() == ".data":
            continue
        out.append(line.strip())
    return out


def split_args(line):
    head, _, rest = line.partition(" ")
    return head, ([a.strip() for a in rest.split(",")] if rest.strip() else [])


def derive_renames(effects=None):
    """The hg-engine to Platinum identifier map, read off the shared scripts.

    Returns (map, aligned, skipped). A pair that does not line up argument for
    argument is skipped rather than guessed at: those are the effects the two
    games implement differently, and forcing an alignment there would invent
    renames that are really behaviour differences.
    """
    effects = effects if effects is not None else hg_index(HG_EFFECTS, "effect_script")
    pairs = collections.Counter()
    aligned, skipped = 0, []
    for n in range(PLATINUM_EFFECTS):
        plat = os.path.join(PLAT_EFFECTS, "effect_script_%04d.s" % n)
        if n not in effects or not os.path.exists(plat):
            continue
        a, b = body_lines(effects[n][1]), body_lines(plat)
        if len(a) != len(b):
            skipped.append(n)
            continue
        local, ok = [], True
        for la, lb in zip(a, b):
            ha, aa = split_args(la)
            hb, ab = split_args(lb)
            if ha != hb:
                local.append((ha, hb))
            if len(aa) != len(ab):
                ok = False
                break
            for x, y in zip(aa, ab):
                xs, ys = x.split("|"), y.split("|")
                if len(xs) != len(ys):
                    ok = False
                    break
                if len(xs) > 1:
                    # A flag list has no order. Pair only what the two sides do
                    # not already share, so flags both projects spell the same
                    # way are never mistaken for renames of each other.
                    rx, ry = sorted(set(xs) - set(ys)), sorted(set(ys) - set(xs))
                    if len(rx) == len(ry):
                        local += list(zip(rx, ry))
                    continue
                tx, ty = TOKEN.findall(x), TOKEN.findall(y)
                if len(tx) != len(ty):
                    ok = False
                    break
                local += [(p, q) for p, q in zip(tx, ty) if p != q]
            if not ok:
                break
        if not ok:
            skipped.append(n)
            continue
        aligned += 1
        for pr in local:
            pairs[pr] += 1

    votes = collections.defaultdict(collections.Counter)
    for (x, y), c in pairs.items():
        votes[x][y] += c
    conflicts = {x: dict(ys) for x, ys in votes.items() if len(ys) > 1}
    return ({x: ys.most_common(1)[0][0] for x, ys in votes.items()},
            aligned, skipped, conflicts)


def convert(path, renames):
    """One hg-engine script in Platinum's dialect."""
    out = [HEADER.rstrip("\n"), "", ""]
    for line in open(path, encoding="utf-8"):
        raw = line.rstrip("\n")
        stripped = raw.split("//")[0].rstrip()
        if stripped.startswith(("#include", ".include")) or stripped.strip() == ".data":
            continue
        if not stripped.strip():
            continue
        out.append(TOKEN.sub(lambda m: renames.get(m.group(0), m.group(0)), raw.rstrip()))
    return "\n".join(out) + "\n"


def same_line(a, b):
    """Two script lines that mean the same thing. A `|`-joined flag list is a
    set, so `A|B` and `B|A` are the same line and a text comparison would call
    them different."""
    ha, aa = split_args(a)
    hb, ab = split_args(b)
    if ha != hb or len(aa) != len(ab):
        return False
    return all(set(x.split("|")) == set(y.split("|")) for x, y in zip(aa, ab))


def selftest(renames, skipped):
    """Convert the 277 effects both projects have and compare to Platinum's.

    Scored on the pairs that line up structurally, because those are the ones
    that say anything about the rename map. The rest are effects the two games
    implement differently, hg-engine having moved work out of the script that
    Platinum still does in it (effect 7, Selfdestruct, is the clearest: hg's is
    a bare hit, Platinum's carries the whole Damp check). A difference there is
    not a gap in the map and cannot be fixed by renaming anything.

    A map that rebuilds Platinum's own scripts from hg-engine's is good enough
    to bring the new ones across; that is the whole claim this test supports.
    """
    effects = hg_index(HG_EFFECTS, "effect_script")
    exact, differ, structural = 0, [], 0
    for n in range(PLATINUM_EFFECTS):
        plat = os.path.join(PLAT_EFFECTS, "effect_script_%04d.s" % n)
        if n not in effects or not os.path.exists(plat):
            continue
        if n in skipped:
            structural += 1
            continue
        got = body_lines_from_text(convert(effects[n][1], renames))
        want = body_lines(plat)
        if len(got) == len(want) and all(same_line(x, y) for x, y in zip(got, want)):
            exact += 1
        else:
            differ.append(n)
    return exact, differ, structural


def body_lines_from_text(text):
    out = []
    for line in text.splitlines():
        line = line.split("//")[0].rstrip()
        if not line.strip():
            continue
        if line.startswith(("#include", ".include")) or line.strip() == ".data":
            continue
        out.append(line.strip())
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--map", action="store_true", help="print the derived renames")
    ap.add_argument("--selftest", action="store_true",
                    help="convert the shared 277 effects and compare to Platinum's")
    ap.add_argument("--show", type=int, metavar="N",
                    help="print the conversion of hg-engine effect N")
    a = ap.parse_args()

    if not os.path.isdir(HG_EFFECTS):
        sys.exit("no hg-engine checkout at %s; set HG_ENGINE or clone it "
                 "(see the tracker's element 4 entry)" % HG)

    renames, aligned, skipped, conflicts = derive_renames()
    # The summary goes to stderr: `--show N > effect_script_NNNN.s` must leave
    # nothing but the script on stdout (2026-09-22 review finding).
    print("rename map: %d entries, derived from %d aligned script pairs of %d; "
          "%d pairs differ in shape and were not used"
          % (len(renames), aligned, PLATINUM_EFFECTS, len(skipped)), file=sys.stderr)
    if conflicts:
        print("AMBIGUOUS, the map is not trustworthy until these are resolved:", file=sys.stderr)
        for x, ys in conflicts.items():
            print("    %-44s %s" % (x, ys), file=sys.stderr)

    if a.map:
        for x, y in sorted(renames.items()):
            print("    %-46s -> %s" % (x, y))
    if a.show is not None:
        effects = hg_index(HG_EFFECTS, "effect_script")
        sys.stdout.write(convert(effects[a.show][1], renames))
    if a.selftest:
        exact, differ, structural = selftest(renames, set(skipped))
        total = exact + len(differ)
        print("selftest: of the %d shared effects that line up structurally, "
              "%d convert to Platinum's own script exactly and %d differ"
              % (total, exact, len(differ)))
        print("  %d more were not scored: the two games implement those "
              "differently, which no rename can fix" % structural)
        if differ:
            print("  differing ids: %s%s" % (differ[:25], " ..." if len(differ) > 25 else ""))
        return 0 if not differ else 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

"""The learnset rewrite's generator (learnrewrite.py) against what it must do.

    PYTHONPATH=. python3 -m tools.oxide.balance.test_learnrewrite

Builds every list in memory (about half a minute) and checks the generator's
rules on them, and reports which species files differ from its output.
Nothing is written.
"""
import os
import re
import sys

from . import data, learncheck as lc, learnrewrite as lg


def check_writer(results):
    """The writer reproduces every species file byte for byte from its own
    list, so writing touches nothing but the lists that change."""
    bad = lg.round_trip()
    results.append(("the writer round-trips every species file", not bad,
                    f"{len(lc.species_set())} files" if not bad else f"differ: {bad[:5]}"))


def report_tree(d):
    """Which species files hold a level-up list the generator would not build.
    The files are the authority now, hand edits included, so this reports and
    never fails (Ian, 2026-10-13): it failed two landings in two days, and
    both times the answer was to keep the lists as they were. The guard it
    gave moved to the writer, which changes only the species named on its
    command line: before, a write over every species reset any hand edit not
    held in learnsets_by_hand.txt, as one reset Nacli's egg list on
    2026-10-12."""
    differ = sorted(sp for sp in lc.species_set()
                    if [tuple(e) for e in d.lists[sp]] != [tuple(e) for e in lc.learnset("rewrite", sp)])
    if not differ:
        return "every species file matches the generator's output"
    more = f" and {len(differ) - 5} more" if len(differ) > 5 else ""
    return (f"{len(differ)} species files differ from the generator's output ({', '.join(differ[:5])}{more}); "
            "a write changes only the species it is given")


def check_hand_eggs(results, d):
    """A species set by hand keeps its egg list as its file holds it, as it
    keeps its level-up list; a run of write once reset Nacli's (2026-10-12)."""
    differ = sorted(sp for sp in lg.by_hand() if sp in d.eggs
                    and d.eggs[sp] != list((lg.pokedex.load(data.ROOT, sp) or {}).get("egg_moves") or []))
    results.append(("a species set by hand keeps its egg list", not differ,
                    f"{len(lg.by_hand())} species set by hand" if not differ else f"differ: {differ[:5]}"))


def check_log(results, d):
    """Every change in the log names the rule behind it."""
    blank = [row for row in d.log if not row[4]]
    results.append(("every change names its rule", not blank and len(d.log) > 0,
                    f"{len(d.log)} changes" if not blank else f"no rule: {blank[:3]}"))


def check_limits(results, d):
    """No list exceeds the engine's 34 entries, none places a move past 78,
    and no catch knows no attack."""
    long = [sp for sp, lst in d.lists.items() if len(lst) > lg.MAX_ENTRIES]
    past = [sp for sp, lst in d.lists.items() if any(lv > lg.top() for lv, _m in lst)]
    bare = lc.bare_captures("rewrite")
    ok = not long and not past and not bare
    results.append(("at most 34 entries, none past 78, every catch knows an attack", ok,
                    f"long {long[:3]}, past 78 {past[:3]}, no attack at capture {sorted(bare)[:3]}"))


def check_held_out(results):
    """The five held-out lines get no special treatment: the generator's
    source names none of their species, so no rule can be a patch for one
    (learnset-checks.md, step 4's brief)."""
    with open(os.path.join(data.ROOT, "tools", "oxide", "balance", "learnrewrite.py"), encoding="utf-8") as f:
        source = f.read()
    named = []
    for fam in lc.held_out():
        for sp in lc.families()[fam]:
            word = sp.replace("SPECIES_", "")
            if re.search(r"\b" + word + r"\b", source, re.IGNORECASE) or sp in source:
                named.append(sp)
    results.append(("the generator names no held-out line", not named,
                    f"{len(lc.held_out())} lines checked" if not named else f"named: {named}"))


def check_egg_keys(results):
    """IAN_EGG_MOVES names each species once. A dict literal keeps only the
    last of two equal keys, without a word, so a second entry for a line
    drops the first one's moves (Torchic and Rotom, both 2026-10-31)."""
    with open(os.path.join(data.ROOT, "tools", "oxide", "balance", "learnrewrite.py"), encoding="utf-8") as f:
        source = f.read()
    start = source.index("IAN_EGG_MOVES = {")
    body = source[start:source.index("\n}\n", start)]
    keys = re.findall(r'^\s+"(SPECIES_[A-Z0-9_]+)":', body, re.MULTILINE)
    twice = sorted({k for k in keys if keys.count(k) > 1})
    results.append(("IAN_EGG_MOVES names each species once", not twice,
                    f"{len(keys)} species" if not twice else f"twice: {twice}"))


def main():
    results = []
    d = lg.build()
    check_writer(results)
    check_hand_eggs(results, d)
    check_log(results, d)
    check_limits(results, d)
    check_held_out(results)
    check_egg_keys(results)
    width = max(len(label) for label, _, _ in results)
    failed = 0
    for label, ok, note in results:
        failed += not ok
        print(f"  {'ok  ' if ok else 'FAIL'}  {label:{width}}  {note}")
    print(f"  note  {report_tree(d)}")
    print(f"\n{len(results) - failed}/{len(results)} passed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())

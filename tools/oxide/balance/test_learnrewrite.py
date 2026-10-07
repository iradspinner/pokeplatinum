"""The learnset rewrite's generator (learnrewrite.py) against what it must do.

    PYTHONPATH=. python3 -m tools.oxide.balance.test_learnrewrite

Builds every list in memory (about half a minute) and compares it with the
species files. Nothing is written.
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


def check_tree(results, d):
    """The tree holds what the generator builds: no list was edited by hand
    after the run."""
    differ = sorted(sp for sp in lc.species_set()
                    if [tuple(e) for e in d.lists[sp]] != [tuple(e) for e in lc.learnset("rewrite", sp)])
    results.append(("the species files are the generator's output", not differ,
                    "every list matches" if not differ else f"differ: {differ[:5]}"))


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


def check_starters(results):
    """Rowan's starters know Tackle and Growl or their equivalents at 5,
    and nothing else (Ian, 2026-10-07; learncheck's check 25), so no rerun
    of the generator can give one a third move there."""
    rows = lc.check25("rewrite")
    bad = [f"{lc.species_name(sp)}: {', '.join(f'{lc.move_name(m)} {lv}' for lv, m in low)}"
           for sp, low, verdict in rows if verdict == "fail"]
    results.append(("Rowan's starters know a basic attack and a basic status move at 5, nothing else",
                    not bad and len(rows) == 3, "; ".join(bad) if bad else
                    "; ".join(f"{lc.species_name(sp)}: {', '.join(lc.move_name(m) for _lv, m in low)}"
                              for sp, low, _v in rows)))


def main():
    results = []
    d = lg.build()
    check_writer(results)
    check_tree(results, d)
    check_log(results, d)
    check_limits(results, d)
    check_held_out(results)
    check_starters(results)
    width = max(len(label) for label, _, _ in results)
    failed = 0
    for label, ok, note in results:
        failed += not ok
        print(f"  {'ok  ' if ok else 'FAIL'}  {label:{width}}  {note}")
    print(f"\n{len(results) - failed}/{len(results)} passed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())

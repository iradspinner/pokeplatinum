"""The learnset study's acceptance: its reading of Kaizo and its rules (learnstudy.py).

    PYTHONPATH=. python3 -m tools.oxide.balance.test_learnstudy

Reads Kaizo's lists and calculator file, vanilla from main and Oxide's
moves; runs no Node.
"""
import sys

from . import learnstudy as ls


def check_reading(results):
    """Every move in Ian's Kaizo lists is found in Kaizo's data, every species
    has Kaizo's types, and every species sits in exactly one line's family."""
    lists = ls.kaizo_lists()
    missing = sorted({e["move"] for sp in lists for e in ls.entries(sp) if e["kind"] == "unknown"})
    untyped = [r["name"] for r in lists.values() if not r["types"]]
    placed = {sp for line in ls.lines() for sp in line}
    ok = not missing and not untyped and placed == set(lists)
    results.append(("Kaizo's lists read in full", ok,
                    f"missing {missing[:5]}, untyped {untyped[:5]}, "
                    f"{len(set(lists) - placed)} species in no line" if not ok else
                    f"{len(lists)} species, {len(ls.lines())} lines"))


def check_named(results):
    """The dead-weight rule catches each move Ian named as never good, in
    every split and as a starting move (Octazooka at vanilla's values)."""
    kept = {name: where for name, where in ls.named_check().items() if where}
    results.append(("the rule catches every move Ian named, everywhere", not kept,
                    f"{kept}" if kept else f"{len(ls.NAMED)} moves"))


def check_kaizo_rate(results):
    """The rule is read off Kaizo's lists, so Kaizo's own lists rarely break it."""
    n, start, later = ls.kaizo_dead_weight()
    share = (sum(start.values()) + sum(later.values())) / n
    results.append(("Kaizo's own lists break the rule in under 5% of entries", share < 0.05,
                    f"{share:.3f} of {n}"))


def check_placement(results):
    """A move's usual split places Kaizo's moves on held-out families better
    than the strength curve or vanilla's timing, and a move Kaizo never used
    is placed better by moves of like strength than by the curve."""
    r = ls.placement_test()
    usual = r["a known move's usual split, damaging moves only"]["mean"]
    unseen = r["an unseen move, by moves of like strength"]["mean"]
    curve = r["an unseen move, by the curve"]["mean"]
    vanilla = r["vanilla's split, where vanilla has the move"]["mean"]
    ok = usual < unseen < curve and usual < vanilla
    results.append(("usual split beats the curve and vanilla on held-out families", ok,
                    f"usual {usual:.2f}, like strength {unseen:.2f}, curve {curve:.2f}, "
                    f"vanilla {vanilla:.2f}"))


def main():
    results = []
    for check in (check_reading, check_named, check_kaizo_rate, check_placement):
        check(results)
    width = max(len(label) for label, _, _ in results)
    failed = 0
    for label, ok, note in results:
        failed += not ok
        print(f"  {'ok  ' if ok else 'FAIL'}  {label:{width}}  {note}")
    print(f"\n{len(results) - failed}/{len(results)} passed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())

"""The learnset study's reading of Kaizo (learnstudy.py), which the learnset
rules (learncheck.py) read Kaizo's lists through.

    PYTHONPATH=. python3 -m tools.oxide.balance.test_learnstudy

Reads Kaizo's lists and calculator file; runs no Node. Its checks of the
study's dead-weight rule and placement, and of the v3 generator and Kaizo's
documentation, went with that generator (learngen.py, learnwild.py and
kaizo_docs.py) on 2026-10-13.
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


def check_splits(results):
    """The reference splits the learnset generator places Kaizo's moves by
    (learnrewrite reads split_of("kaizo", ...)): each game's gym aces and
    League as they stood in the retired reference seats."""
    got = {h: ls.splits(h) for h in ("kaizo", "vanilla")}
    ok = (got["kaizo"][0] == ("Roark", 16) and got["kaizo"][-1] == ("League", 100)
          and got["vanilla"][-2] == ("Volkner", 50) and ls.split_of("kaizo", 29) == "Fantina"
          and ls.split_of("kaizo", 101) == "League")
    results.append(("Kaizo's and vanilla's splits close at their gym aces", ok, str(got["kaizo"])))


def main():
    results = []
    for check in (check_reading, check_splits):
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

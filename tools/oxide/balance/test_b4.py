"""B4 acceptance: the level curve (levels.py) and the split-shape model (shape.py).

    PYTHONPATH=. python3 -m tools.oxide.balance.test_b4

Runs no Node: the shape grid is read from shape.json as shape.py saved it.
Writes nothing.
"""
import sys

from . import data, levels, shape

RATES = ("EXP_RATE_MEDIUM_FAST", "EXP_RATE_MEDIUM_SLOW", "EXP_RATE_FAST", "EXP_RATE_SLOW")


def check_growth(results):
    """The four common growth rates at the levels every guide quotes, and
    level_for as their exact inverse."""
    known = levels.exp_at("EXP_RATE_MEDIUM_SLOW", 5) == 135 and \
        [levels.exp_at(r, 100) for r in RATES] == [1_000_000, 1_059_860, 800_000, 1_250_000]
    inverse = all(levels.level_for(r, levels.exp_at(r, n)) == n
                  and levels.level_for(r, levels.exp_at(r, n) - 1) == n - 1
                  for r in RATES for n in range(3, 101))
    results.append(("growth rates and their inverse", known and inverse, ""))


def check_experience(results):
    """A fainted Pokemon's experience is base times level over 7, rounded
    down, then half again for a trainer battle (battle_script.c). Every
    Pokemon in every Oxide trainer's party and every Renegade story fight
    has a base experience."""
    mon = {"species": "Bidoof", "level": 7}
    b = levels.base_exp("Bidoof")
    formula = levels.foe_exp(mon) == (b * 7 // 7) * 150 // 100
    missing = set()
    for t in data.oxide_trainers().values():
        for m in t["party"]:
            try:
                levels.base_exp(m["species"])
            except KeyError:
                missing.add(m["species"])
    for fight in data.fights()["fights"]:
        for t in data.fight_trainers("renegade", fight):
            for m in t["party"]:
                try:
                    levels.base_exp(m["species"])
                except KeyError:
                    missing.add(m["species"])
    results.append(("experience formula, and every trainer Pokemon has a base experience",
                    formula and not missing, f"missing {sorted(missing)[:5]}" if missing else ""))


def check_curves(results):
    """The floor never gives more than the ceiling; a capped curve never
    passes its cap; levels never fall from one split to the next; and the
    candy budget's arithmetic holds (needed is team times the gap)."""
    ok, notes = True, []
    for rate in ("EXP_RATE_MEDIUM_SLOW", "EXP_RATE_MEDIUM_FAST"):
        floor, ceiling = levels.curve("oxide", "floor", 6, rate), levels.curve("oxide", "ceiling", 6, rate)
        for f, c in zip(floor, ceiling):
            ok &= f[2] <= c[2] and f[3] <= c[3] <= c[1]
        ok &= all(a[3] <= b[3] for a, b in zip(ceiling, ceiling[1:]))
    for split, cap, reached, needed, _offered, _balance in levels.candy_budget("ceiling"):
        if needed != 6 * (cap - reached):
            ok, notes = False, notes + [split]
    results.append(("curves bracket each other, stay under the caps and never fall", ok,
                    f"budget off in {notes}" if notes else ""))


def check_shape_helpers(results):
    """A shifted party puts its strongest Pokemon exactly `delta` from the
    cap, moves every Pokemon by the same amount, and leaves the party it was
    given alone; the caps are as fights.json holds them."""
    parties = [[{"species": "A", "level": 58}, {"species": "B", "level": 55}]]
    moved = shape.shifted(parties, 66, -2)
    ok = [m["level"] for m in moved[0]] == [64, 61] and parties[0][0]["level"] == 58
    before = dict(data.fights()["caps"])
    results.append(("a shifted party keeps its spread and the original", ok and
                    data.fights()["caps"] == before, ""))


def check_shape_grid(results):
    """The saved grid covers every group at every gap, and a boss scores no
    softer as its levels rise: threat never falls and answers never rise
    across the gap, allowing 0.01 for rounding."""
    saved = shape.load()
    bad = []
    for group, fights in saved.get("bosses", {}).items():
        for key, by_delta in fights.items():
            rows = [by_delta[str(d)] for d in shape.DELTAS if str(d) in by_delta]
            if len(rows) != len(shape.DELTAS):
                bad.append(f"{key} incomplete")
                continue
            for a, b in zip(rows, rows[1:]):
                if b["threat"] < a["threat"] - 0.01 or b["answers"] > a["answers"] + 0.01:
                    bad.append(key)
                    break
    groups = set(saved.get("bosses", {}))
    ok = not bad and groups == set(shape.GROUPS) | {"zone"}
    results.append(("the shape grid is complete and rises with the level gap", ok,
                    f"{sorted(groups)}" + (f"; {bad}" if bad else "")))


def main():
    results = []
    for check in (check_growth, check_experience, check_curves, check_shape_helpers,
                  check_shape_grid):
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

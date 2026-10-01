"""The perfect-line scorer against Ian's forty pairs (fightfit.PAIRS),
from the readings plscore saved.

    PYTHONPATH=. python3 -m tools.oxide.balance.ppairs

A boss (a story fight or a named Galactic officer) is compared by its
planned clean-win rate, an ordinary trainer by its blind rate, as the
scoring review read them. The lower rate reads harder. Ian's rulings of
2026-09-30 add the best line's cost: where the two rates are within TIE of
each other (both near nothing, say), the fight whose line costs more
deaths reads harder. Both rules are reported, the review's first. A pair
Ian called "the same" or "very close" agrees when the two sit within
CLOSE. Held-out pairs are the fifteen fightfit holds out.
"""
import json
import os
import sys

from . import fightfit

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(HERE, "perfectline_results")
CLOSE = 0.10
TIE = 0.02


def load(folder=RESULTS):
    out = {}
    for name in sorted(os.listdir(folder)):
        if not name.endswith(".json") or "-" in name[:-5]:
            continue                 # a strict, planned-box or save-box reading
        with open(os.path.join(folder, name), encoding="utf-8") as f:
            r = json.load(f)
        out[r["key"]] = r
    return out


def fight_key(f):
    kind, key = f
    return key if kind == "story" else f"tr{key}"


def reading(r, kind):
    """(rate, deaths) a pair compares on."""
    boss = kind == "story" or r["label"].startswith(("Galactic Officer", "Commander"))
    if boss:
        return r["planned_rate"], r.get("planned_deaths", 0.0)
    return r["blind_rate"], r.get("blind_deaths", 0.0)


def agrees(harder, grade, a, b, use_deaths):
    (ra, da), (rb, db) = a, b
    if harder is None or grade in ("same", "very close"):
        return abs(ra - rb) <= CLOSE
    if use_deaths and abs(ra - rb) <= TIE:
        return da > db if harder == "A" else db > da
    return ra < rb if harder == "A" else rb < ra


def check(res, out=sys.stdout):
    """{rule: (held agreed, held read, all agreed, all read)} and the table."""
    tallies = {"rate": [0, 0, 0, 0], "rate and deaths": [0, 0, 0, 0]}
    print("| Pair | Fights | Ian | A: rate, deaths | B: rate, deaths | Rate agrees | With deaths |", file=out)
    print("|---|---|---|---|---|---|---|", file=out)
    for i, (a, b, harder, grade, held) in enumerate(fightfit.PAIRS, 1):
        ra, rb = res.get(fight_key(a)), res.get(fight_key(b))
        if ra is None or rb is None:
            print(f"| {i} | {fight_key(a)} against {fight_key(b)} | {harder or 'same'}, {grade} | not read | | | |",
                  file=out)
            continue
        va, vb = reading(ra, a[0]), reading(rb, b[0])
        oks = {}
        for rule, use in (("rate", False), ("rate and deaths", True)):
            ok = agrees(harder, grade, va, vb, use)
            oks[rule] = ok
            t = tallies[rule]
            t[2] += ok
            t[3] += 1
            if held:
                t[0] += ok
                t[1] += 1
        named = {"A": ra["label"], "B": rb["label"], None: "the same"}[harder]
        print(f"| {i}{'*' if held else ''} | {ra['label']} against {rb['label']} | {named}, {grade} | "
              f"{va[0]:.2f}, {va[1]:.2f} | {vb[0]:.2f}, {vb[1]:.2f} | {'yes' if oks['rate'] else 'no'} | "
              f"{'yes' if oks['rate and deaths'] else 'no'} |", file=out)
    print(file=out)
    for rule, (h, hn, a_, an) in tallies.items():
        print(f"By {rule}: {h} of {hn} held-out pairs (marked *), {a_} of {an} read.", file=out)
    return tallies


def main(argv=None):
    check(load())
    return 0


if __name__ == "__main__":
    sys.exit(main())

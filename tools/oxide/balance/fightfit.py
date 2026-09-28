"""Fitting the rebuilt headline to Ian's pairwise judgements, and the test it must pass.

    PYTHONPATH=. python3 -m tools.oxide.balance.fightfit          # read, fit, test
    PYTHONPATH=. python3 -m tools.oxide.balance.fightfit --cached # fit and test from the saved readings

Ian judged forty pairs of fights on 2026-09-27
(docs/oxide/pairwise-candidates.md): which of the two is harder for a
player at that split's cap, and by how much, in six grades. Twenty-five
fit the headline's weights; fifteen are held out, and the headline
replaces today's score only when it agrees with at least 13 of those.

The headline is a weighted sum of a fight's readings (fightsim.py): the
Pokemon lost a battle, the chance of losing three or more, the chance of a
wipe, and the share of HP spent. The weights are fitted so that each
fitted pair's difference in headline matches its grade's gap on Ian's
1-to-10 scale, none of them negative. The level of the scale comes from
Ian's own ratings of sixteen fights (calibrate.IAN_RATINGS). A held-out
pair agrees when the headline puts the fight Ian named above the other;
for his "very close" and "the same", when the two sit within half a point.
"""
import argparse
import itertools
import json
import os
import statistics
import sys

import numpy as np

from . import b6, calibrate, data, fightsim, splits

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "fightfit.json")
FEATURES = ("losses", "three_plus", "wipe", "hp_lost")
# A grade's gap on Ian's 1-to-10 scale: this track's reading of his six words.
GAP = {"same": 0.0, "very close": 0.3, "a bit": 0.8, "a lot": 1.6, "massive": 2.6, "comical": 4.0}
CLOSE = 0.5

# The forty pairs in the doc's order: (fight A, fight B, the harder one,
# Ian's grade, held out). A fight is ("story", key) or ("tr", trainer id).
S, T = "story", "tr"
PAIRS = [
    ((S, "roark"), (S, "barry_2"), "A", "a lot", False),
    ((T, 323), (T, 245), "A", "a bit", True),
    ((S, "gardenia"), (S, "mars_1"), "A", "massive", False),
    ((T, 299), (T, 326), "A", "massive", False),
    ((T, 78), (T, 203), "B", "a bit", True),
    ((S, "fantina"), (S, "lucas_dawn_2"), "A", "massive", False),
    ((T, 266), (T, 36), "B", "a lot", False),
    ((T, 423), (S, "jupiter_1"), "B", "a bit", True),
    ((S, "maylene"), (S, "barry_3"), "A", "comical", False),
    ((T, 294), (T, 127), "A", "a bit", False),
    ((T, 532), (T, 310), "A", "a lot", True),
    ((T, 65), (T, 290), None, "same", False),
    ((S, "wake"), (S, "barry_4"), "A", "comical", False),
    ((T, 795), (T, 293), "A", "comical", False),
    ((T, 382), (T, 105), "A", "massive", True),
    ((S, "byron"), (S, "cyrus_1"), "A", "a bit", False),
    ((T, 283), (T, 392), "B", "a lot", False),
    ((S, "barry_5"), (T, 416), "A", "a lot", True),
    ((T, 68), (T, 505), "A", "a lot", True),
    ((S, "candice"), (S, "mars_2"), "A", "massive", False),
    ((T, 141), (T, 138), "A", "comical", False),
    ((S, "saturn_1"), (T, 418), "B", "very close", True),
    ((T, 420), (T, 419), "A", "comical", True),
    ((S, "cyrus_2"), (S, "saturn_2"), "B", "a lot", False),
    ((T, 830), (T, 509), "A", "a bit", True),
    ((T, 525), (T, 507), "A", "comical", False),
    ((S, "mars_jupiter"), (S, "cyrus_3"), "B", "a bit", False),
    ((T, 561), (T, 584), "A", "a lot", True),
    ((T, 520), (T, 526), "B", "massive", False),
    ((T, 578), (T, 565), "A", "a bit", False),
    ((T, 926), (T, 927), "B", "a bit", True),
    ((S, "volkner"), (T, 281), "A", "comical", True),
    ((T, 331), (T, 341), None, "same", False),
    ((S, "cynthia"), (S, "lucian"), "A", "a bit", False),
    ((S, "flint_volkner"), (S, "lucas_dawn_3"), "B", "a bit", True),
    ((S, "lucian"), (S, "bertha"), "A", "a lot", False),
    ((S, "aaron"), (S, "flint"), "A", "a bit", False),
    ((T, 230), (T, 228), "A", "comical", True),
    ((T, 236), (T, 234), "A", "a bit", False),
    ((S, "barry_6"), (S, "aaron"), "A", "a lot", False),
]
# Ian's ratings (calibrate.IAN_RATINGS) name one fight that is not a story
# fight: Hesperid at Lake Valor.
RATED_TRAINERS = {"hesperid_valor": 418}


def fight_id(f):
    return f"{f[0]}:{f[1]}"


def read(f, runs=fightsim.RUNS):
    kind, key = f
    if kind == S:
        return fightsim.story(key, runs)
    if key not in b6.placements():
        # A trainer B6 does not place is read in its map's split.
        split = splits.trainer_split(key)
        t = data.oxide_trainers()[key]
        st = fightsim.prepare(split, [t["party"]], fightsim.pressure.fight_weather([key]),
                              cap=fightsim.fight_cap(split))
        return fightsim.read_fight(st, [t["ai"]], runs)
    return fightsim.trainer(key, runs)


def all_fights():
    out = []
    for a, b_, *_ in PAIRS:
        for f in (a, b_):
            if f not in out:
                out.append(f)
    for key in calibrate.IAN_RATINGS:
        f = (T, RATED_TRAINERS[key]) if key in RATED_TRAINERS else (S, key)
        if f not in out:
            out.append(f)
    return out


def cache_path():
    return CACHE.replace(".json", "_box.json") if fightsim.BOX_MODE else CACHE


def readings(cached=False):
    """{fight id: reading}, read now or from the saved file."""
    if cached and os.path.exists(cache_path()):
        with open(cache_path(), encoding="utf-8") as f:
            return json.load(f)
    out = {}
    for f in all_fights():
        out[fight_id(f)] = read(f)
        print(f"  {fight_id(f):22} {out[fight_id(f)]}", flush=True)
    with open(cache_path(), "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1)
        fh.write("\n")
    return out


def vec(r):
    return np.array([r[k] for k in FEATURES], dtype=float)


def fit(reads):
    """Non-negative weights for the features, from the fitted pairs'
    differences, and the scale's level from Ian's ratings."""
    rows, target = [], []
    for a, b_, harder, grade, held in PAIRS:
        if held:
            continue
        d = vec(reads[fight_id(a)]) - vec(reads[fight_id(b_)])
        sign = 1 if harder == "A" else -1 if harder == "B" else 0
        rows.append(d)
        target.append(sign * GAP[grade])
    X, y = np.array(rows), np.array(target)
    best = None
    # Every subset of the features, least squares on each, keeping only
    # solutions with no negative weight: four features make sixteen tries.
    for k in range(1, len(FEATURES) + 1):
        for cols in itertools.combinations(range(len(FEATURES)), k):
            w, *_ = np.linalg.lstsq(X[:, cols], y, rcond=None)
            if (w < 0).any():
                continue
            full = np.zeros(len(FEATURES))
            full[list(cols)] = w
            err = float(((X @ full - y) ** 2).sum())
            if best is None or err < best[0]:
                best = (err, full)
    weights = best[1]
    rated = []
    for key, rating in calibrate.IAN_RATINGS.items():
        f = (T, RATED_TRAINERS[key]) if key in RATED_TRAINERS else (S, key)
        rated.append(rating - float(vec(reads[fight_id(f)]) @ weights))
    return weights, statistics.mean(rated), best[0]


def headline(r, weights, level):
    return level + float(vec(r) @ weights)


def test(reads, weights, level, out=sys.stdout):
    """The held-out pairs: how many agree, and each one's reading."""
    agree = 0
    held = [p for p in PAIRS if p[4]]
    for n, (a, b_, harder, grade, held_) in enumerate(PAIRS, 1):
        if not held_:
            continue
        ha, hb = headline(reads[fight_id(a)], weights, level), headline(reads[fight_id(b_)], weights, level)
        if grade in ("same", "very close"):
            ok = abs(ha - hb) <= CLOSE or (harder == "A" and ha > hb) or (harder == "B" and hb > ha)
        else:
            ok = ha > hb if harder == "A" else hb > ha
        agree += ok
        print(f"  pair {n:>2}: {fight_id(a):20} {ha:5.2f}  {fight_id(b_):20} {hb:5.2f}  Ian: "
              f"{'A' if harder == 'A' else 'B' if harder == 'B' else '='} {grade:10} "
              f"{'agrees' if ok else 'DISAGREES'}", file=out)
    print(f"held out: {agree} of {len(held)} agree (the bar is 13)", file=out)
    return agree


def main(argv=None):
    from . import fightfit as mod
    ap = argparse.ArgumentParser()
    ap.add_argument("--cached", action="store_true")
    ap.add_argument("--box", action="store_true", help="plan each six from a realistic box")
    args = ap.parse_args(argv)
    fightsim.BOX_MODE = args.box
    # Ian judged his pairs as singles, the four doubles trainers among them too.
    fightsim.PLAY_DOUBLES = False
    reads = mod.readings(args.cached)
    weights, level, err = mod.fit(reads)
    print("weights:", dict(zip(FEATURES, (round(float(w), 3) for w in weights))),
          f"level {level:.2f}, fitted error {err:.2f}")
    mod.test(reads, weights, level)
    return 0


if __name__ == "__main__":
    sys.exit(main())

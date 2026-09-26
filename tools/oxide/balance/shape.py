"""The Galactic stretch's shape: which caps and trainer levels meet Ian's targets.

    PYTHONPATH=. python3 -m tools.oxide.balance.shape --run bosses   # score the grid
    PYTHONPATH=. python3 -m tools.oxide.balance.shape --run filler
    PYTHONPATH=. python3 -m tools.oxide.balance.shape --report

Ian's ruling of 2026-09-26: after Candice (cap 56) the story runs Lake
Acuity, the Galactic HQ, the Battle Zone, the Mt. Coronet climb and Spear
Pillar, then Volkner, then the League (cap 78). His targets, relative to
the caps: the HQ hard, the Battle Zone medium hard, the climb and the last
Galactic fights very hard.

Pressure (B3) depends mostly on the gap between a boss's level and the
player's cap, so each group of fights is scored across that gap: its party
is shifted so its strongest Pokemon sits `delta` levels from the cap, and
the player's side is built at that cap. The side is the one the player has
at that point: before the zone's captures for the HQ, after them for the
climb and Volkner. Each score also carries answers counting a Choice lock
(Ian's ruling of 2026-09-23), since a locked boss can be baited.

The zone's route trainers are scored the same way, against the game's own
ordinary trainers in Candice's and Wake's splits at their real levels, so
"medium hard" for the zone reads against filler rather than against bosses.

Results go to shape.json; nothing in res/ changes.
"""
import argparse
import copy
import functools
import json
import os
import sys
import tempfile

from ..encounters import calc_export
from . import data, metrics, pool, pressure, splits

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "shape.json")

# The groups Ian named, by fight key; the zone's boss is Mars and Jupiter's
# tag at Stark Mountain, which fights.json does not list.
GROUPS = {
    "hq": ["cyrus_2", "saturn_2"],
    "climb": ["mars_jupiter", "cyrus_3"],
    "volkner": ["volkner"],
}
ZONE_BOSS = ("TRAINER_COMMANDER_MARS_STARK_MOUNTAIN", "TRAINER_COMMANDER_JUPITER_STARK_MOUNTAIN")
# Which side the player has: before the zone's captures (Candice's species)
# or after them (the Galactic split's, which holds the zone and the climb).
SIDE_OF = {"hq": "HQ", "zone": "Galactic", "climb": "Galactic", "volkner": "Volkner"}
DELTAS = (-8, -6, -4, -2, 0, 2)
FILLER_DELTAS = (-10, -7, -4)
REFERENCE_CAP = {"hq": 60, "zone": 65, "climb": 65, "volkner": 68}   # Ian's caps since 2026-09-25


def _clear_pool_caches():
    for name in dir(pool):
        fn = getattr(pool, name)
        if hasattr(fn, "cache_clear"):
            fn.cache_clear()


def side_at(split, cap, blob):
    """The player's side from `split`'s species, built at `cap`: level,
    evolutions and moves as of that cap."""
    caps = data.fights()["caps"]
    old = caps[split]
    caps[split] = cap
    _clear_pool_caches()
    try:
        return pool.pool(split, blob)
    finally:
        caps[split] = old
        _clear_pool_caches()


def shifted(parties, cap, delta):
    """The parties with every level moved by the same amount, so the
    strongest Pokemon sits `delta` levels from the cap."""
    ace = max(m["level"] for party in parties for m in party)
    move = cap + delta - ace
    out = copy.deepcopy(parties)
    for party in out:
        for m in party:
            m["level"] = max(1, m["level"] + move)
    return out


def _zone_boss_fight():
    by_constant = {t["constant"]: t for t in data.oxide_trainers().values()}
    trainers = [by_constant[c] for c in ZONE_BOSS]
    return ({"key": "mars_jupiter_stark", "label": "Mars and Jupiter, Stark Mountain",
             "split": "Galactic", "tag": True, "tr_ids": [t["tr_id"] for t in trainers]},
            [[m for t in trainers for m in t["party"]]])


def _fight_parties(key):
    fight = next(f for f in data.fights()["fights"] if f["key"] == key)
    parties, _ids = pressure.boss_parties(fight)
    return fight, parties


def _zone_filler():
    """The Battle Zone's route and Stark Mountain trainers, less the tag
    fights: every trainer the zone's maps battle."""
    zone = ("ROUTE_225", "ROUTE_226", "ROUTE_227", "ROUTE_228", "ROUTE_229", "ROUTE_230",
            "STARK_MOUNTAIN")
    skip = set(ZONE_BOSS) | {"TRAINER_BUCK_STARK_MOUNTAIN"}
    ox = data.oxide_trainers()
    return [tr for tr, maps in splits.trainer_maps().items()
            if tr in ox and ox[tr]["constant"] not in skip and any(m.startswith(zone) for m in maps)]


def _reference_filler():
    """Candice's and Wake's scored filler at their real levels and caps."""
    ids = metrics.filler_ids()
    return {"Candice": ids.get("Candice", []), "Wake": ids.get("Wake", [])}


def _filler_fight(tr, split):
    t = data.oxide_trainers()[tr]
    return {"key": f"filler_{tr}", "label": t["name"], "split": split, "tr_ids": [tr]}, [t["party"]]


def _score(fight, parties, side, cap, blob, blob_path):
    r = pressure.score_fight(fight, blob, blob_path, side=side, parties=parties, cap=cap)
    return {k: r[k] for k in ("threat", "answers", "answers_lock", "max_threat", "min_answers",
                              "min_answers_lock", "choice_mons", "pool", "cap")}


def load():
    if os.path.exists(OUT):
        with open(OUT, encoding="utf-8") as f:
            return json.load(f)
    return {"_comment": __doc__.strip().split("\n\n")[0], "bosses": {}, "filler": {}}


def save(results):
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=1, sort_keys=True)
        f.write("\n")


def run_bosses(results, blob, blob_path):
    jobs = [(g, key) + _fight_parties(key) for g, keys in GROUPS.items() for key in keys]
    fight, parties = _zone_boss_fight()
    jobs.append(("zone", fight["key"], fight, parties))
    for group, key, fight, parties in jobs:
        cap = REFERENCE_CAP[group]
        side = side_at(SIDE_OF[group], cap, blob)
        for delta in DELTAS:
            r = _score(fight, shifted(parties, cap, delta), side, cap, blob, blob_path)
            results["bosses"].setdefault(group, {}).setdefault(key, {})[str(delta)] = r
            save(results)
            print(f"{group:8} {key:20} delta {delta:>3}: threat {r['threat']:.2f}, answers "
                  f"{r['answers']:.2f}, with the lock {r['answers_lock']:.2f}", flush=True)


def run_filler(results, blob, blob_path):
    caps = data.fights()["caps"]
    for split, ids in _reference_filler().items():
        side = side_at(split, caps[split], blob)
        for tr in ids:
            fight, parties = _filler_fight(tr, split)
            r = _score(fight, parties, side, caps[split], blob, blob_path)
            r["ace_below_cap"] = caps[split] - max(m["level"] for m in parties[0])
            results["filler"].setdefault(split, {})[str(tr)] = r
        save(results)
        print(f"reference filler, {split}: {len(ids)} trainers", flush=True)
    cap = REFERENCE_CAP["zone"]
    side = side_at(SIDE_OF["zone"], cap, blob)
    for tr in _zone_filler():
        fight, parties = _filler_fight(tr, "Galactic")
        for delta in FILLER_DELTAS:
            r = _score(fight, shifted(parties, cap, delta), side, cap, blob, blob_path)
            results["filler"].setdefault(f"zone {delta}", {})[str(tr)] = r
        save(results)
    print(f"zone filler: {len(_zone_filler())} trainers at {FILLER_DELTAS}", flush=True)


def _mean(rows, key):
    return round(sum(r[key] for r in rows) / len(rows), 2) if rows else None


def report(results, out=sys.stdout):
    print("Bosses: each group's mean over its fights, by its ace's gap to the cap", file=out)
    print(f"{'group':8}{'delta':>6}{'threat':>8}{'answers':>9}{'lock':>7}", file=out)
    for group, fights in results["bosses"].items():
        for delta in map(str, DELTAS):
            rows = [f[delta] for f in fights.values() if delta in f]
            print(f"{group:8}{delta:>6}{_mean(rows, 'threat'):>8}{_mean(rows, 'answers'):>9}"
                  f"{_mean(rows, 'answers_lock'):>7}", file=out)
    print("\nFiller: mean over each set's trainers", file=out)
    for name, rows in results["filler"].items():
        rs = list(rows.values())
        extra = (f", ace a mean {_mean(rs, 'ace_below_cap')} under the cap"
                 if rs and "ace_below_cap" in rs[0] else "")
        print(f"{name:12} {len(rs):>3} trainers: threat {_mean(rs, 'threat')}, answers "
              f"{_mean(rs, 'answers')}, with the lock {_mean(rs, 'answers_lock')}{extra}", file=out)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", choices=("bosses", "filler"))
    ap.add_argument("--report", action="store_true")
    args = ap.parse_args(argv)
    results = load()
    if args.run:
        blob = calc_export.build()
        with tempfile.TemporaryDirectory(prefix="oxide-shape-") as tmp:
            blob_path = os.path.join(tmp, "blob.json")
            with open(blob_path, "w", encoding="utf-8") as f:
                json.dump(blob, f)
            (run_bosses if args.run == "bosses" else run_filler)(results, blob, blob_path)
    if args.report or not args.run:
        report(results)
    return 0


if __name__ == "__main__":
    sys.exit(main())

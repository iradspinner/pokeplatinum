"""The perfect-line scorer's stored readings, recomputed only when their
inputs change and verified by a second run (the rescore's rules, for the
new scorer; Ian, 2026-09-30).

    PYTHONPATH=. python3 -m tools.oxide.balance.plrescore            # recompute what is stale
    PYTHONPATH=. python3 -m tools.oxide.balance.plrescore --verify   # recompute each unverified one; must agree
    PYTHONPATH=. python3 -m tools.oxide.balance.plrescore --status

Every story fight and every ordinary trainer B6 places is read. A boss (a
story fight or a named Galactic officer) is read in full, blind and
planned; an ordinary trainer is read blind only, since that is how it is
judged, which is most of the saving. Each reading is stored with a
fingerprint of everything that decides it: the scorer's code (every
module it runs), the calculator's data, the fight's trainers and field,
the split and its cap, the player's side there, the encounter data the
boxes are drawn from, and the search's settings. A stale reading is
recomputed; a recomputed one is unverified until a second run gives the
same numbers. test_pline checks that every fingerprint matches.
"""
import argparse
import functools
import glob
import hashlib
import json
import os
import sys

from . import b6, data, plscore, pool

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "perfectline.json")
CODE = ("perfectline.py", "plines.py", "pboxes.py", "plscore.py", "pdoubles.py", "fightsim.py",
        "fightai.py", "plrescore.py")
KEEP = ("blind_rate", "blind_deaths", "blind_wipe", "planned_rate", "planned_deaths", "planned_wipe",
        "best_rate", "convergence", "search_budget", "converged_share", "split", "label")


def load():
    if os.path.exists(OUT):
        with open(OUT, encoding="utf-8") as f:
            return json.load(f)
    return {"_comment": __doc__.strip().split("\n\n")[0], "fights": {}}


def save(store):
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(store, f, indent=1, sort_keys=True)
        f.write("\n")


def fights():
    """[(("story", key) | ("tr", id), boss)] for the whole game."""
    out = [(("story", f["key"]), True) for f in data.fights()["fights"]]
    ox = data.oxide_trainers()
    for tr in sorted(b6.placements()):
        out.append((("tr", tr), ox[tr]["name"].startswith(("Galactic Officer", "Commander"))))
    return out


def key_of(f):
    kind, key = f
    return key if kind == "story" else f"tr{key}"


def _sha(*parts):
    h = hashlib.sha256()
    for p in parts:
        h.update(json.dumps(p, sort_keys=True, default=str).encode())
    return h.hexdigest()


@functools.lru_cache(maxsize=None)
def code_hash():
    return _sha(*[open(os.path.join(HERE, name), encoding="utf-8").read() for name in CODE])


@functools.lru_cache(maxsize=None)
def blob_hash():
    from ..encounters import calc_export
    return _sha(calc_export.build())


@functools.lru_cache(maxsize=None)
def encounter_hash():
    root = data.ROOT
    files = sorted(glob.glob(os.path.join(root, "res", "field", "encounters", "*.json"))
                   + glob.glob(os.path.join(root, "docs", "oxide", "encounters", "*.json")))
    return _sha(*[(os.path.relpath(p, root), open(p, encoding="utf-8").read()) for p in files])


@functools.lru_cache(maxsize=None)
def side_hash(split):
    from ..encounters import calc_export
    return _sha(pool.pool(split, calc_export.build()), pool.caps()[split])


def settings(boss):
    return {"boxes": plscore.BOXES, "blind": plscore.BLIND, "planned": plscore.PLANNED if boss else 0,
            "seed": plscore.SEED, "blind_search": plscore.BLIND_SEARCH,
            "planned_search": plscore.PLANNED_SEARCH}


def fight_inputs(f):
    """What the fight itself brings: its trainers' parties and field."""
    kind, key = f
    if kind == "story":
        fight = next(x for x in data.fights()["fights"] if x["key"] == key)
        trainers = data.fight_trainers("oxide", fight)
        return {"fight": fight, "parties": [t["party"] for t in trainers], "ai": [t["ai"] for t in trainers]}
    t = data.oxide_trainers()[key]
    return {"party": t["party"], "ai": t["ai"], "battle": t.get("battle_type"),
            "placement": b6.placements().get(key)}


def split_of(f):
    kind, key = f
    if kind == "story":
        return next(x for x in data.fights()["fights"] if x["key"] == key)["split"]
    return b6.placements()[key]["split"]


def fingerprint(f, boss):
    split = split_of(f)
    return _sha(code_hash(), blob_hash(), encounter_hash(), side_hash(split), split,
                fight_inputs(f), settings(boss))[:20]


def read(f, boss):
    prep = plscore.prepare(f)
    out = plscore.read_fight(prep, plscore.BOXES, plscore.BLIND, plscore.PLANNED if boss else 0,
                             log=open(os.devnull, "w"))
    # Through JSON, so a fresh reading compares with a stored one (its
    # convergence table's keys become strings).
    return json.loads(json.dumps({k: out.get(k) for k in KEEP} | {"boss": boss}))


def same(a, b):
    return all(a.get(k) == b.get(k) for k in KEEP)


def run(verify=False, only=None):
    store = load()
    todo = [(f, boss) for f, boss in fights() if only is None or key_of(f) in only]
    done = 0
    for f, boss in todo:
        k = key_of(f)
        fp = fingerprint(f, boss)
        old = store["fights"].get(k)
        if verify:
            if old is None or old.get("fingerprint") != fp or old.get("verified"):
                continue
            new = read(f, boss)
            if same(new, old):
                old["verified"] = True
                print(f"verify {k}: verified", flush=True)
            else:
                print(f"verify {k}: DIFFERS", flush=True)
                store["fights"][k] = dict(new, fingerprint=fp, verified=False)
        else:
            if old is not None and old.get("fingerprint") == fp:
                continue
            store["fights"][k] = dict(read(f, boss), fingerprint=fp, verified=False)
            print(f"rescore {k}: recomputed", flush=True)
        done += 1
        save(store)            # after each fight, so a stopped run resumes
    return done


def status():
    store = load()
    stale = unverified = 0
    for f, boss in fights():
        r = store["fights"].get(key_of(f))
        if r is None or r.get("fingerprint") != fingerprint(f, boss):
            stale += 1
        elif not r.get("verified"):
            unverified += 1
    print(f"{len(fights())} fights: {stale} stale or missing, {unverified} unverified")
    return stale, unverified


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--verify", action="store_true")
    ap.add_argument("--status", action="store_true")
    ap.add_argument("--only", nargs="*")
    args = ap.parse_args(argv)
    if args.status:
        status()
        return 0
    n = run(verify=args.verify, only=set(args.only) if args.only else None)
    print(f"{n} fights {'verified' if args.verify else 'recomputed'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

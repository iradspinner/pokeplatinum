"""Can one network judge a trainer it has never seen? (stage 2, 2026-10-02)

A network trained without a trainer's positions could not play it (Gardenia
won 2 of 500), but it had seen only three trainers, so most species and moves
meant nothing to it. The whole game in hours needs one network that judges
trainers well from positions of many others. This tests that on the ordinary
singles trainers of the first three splits: every fifth is held out, the rest
are labelled by the play-out planner on random boxes (fightsim.random_box,
the blind reading's boxes), and networks trained with and without the
held-out trainers' positions are read on them beside the play-out planner.

    PYTHONPATH=. tools/oxide/capped python3 -m tools.oxide.balance.plgen data --boxes 2
    PYTHONPATH=. tools/oxide/capped python3 -m tools.oxide.balance.plgen data --boxes 2 --held
    PYTHONPATH=. tools/oxide/capped python3 -m tools.oxide.balance.plgen read --value MODEL --runs 40
"""
import argparse
import json
import os
import random
import sys
import time

from . import plthreads  # noqa: F401  (one numpy thread per process, before numpy loads)

from . import b6, data, fightsim as fs, pldata, plplan, plscore, splits  # noqa: E402

SPLITS = ("Roark", "Gardenia", "Fantina")
HOLD_EVERY = 5            # every fifth trainer, in key order, is held out
ROOT = os.path.expanduser("~/oxide-trials/scorer-stage2")
READ_BOX = 0              # the box seed the readings use; the data's boxes start at 1


def trainer_split(key):
    """The scorer's own split for a trainer (plscore.prepare's rule)."""
    return plscore.SPLIT_OVERRIDE.get(key) or (b6.placements()[key]["split"] if key in b6.placements()
                                               else splits.trainer_split(key))


def trainers(which=SPLITS):
    """The ordinary singles trainers of these splits, in key order: not in a
    story fight, with a party, not a double battle, and not a gym leader's
    rematch team (placed by its map in the leader's early split)."""
    story = {c for f in data.fights()["fights"] for c in f["trainers"]}
    out = []
    for key, t in sorted(data.oxide_trainers().items()):
        if t.get("constant") in story or not t.get("party") or t["name"].startswith("Leader "):
            continue
        if t.get("battle_type") == "Doubles" and len(t["party"]) > 1:
            continue
        if trainer_split(key) in which:
            out.append(key)
    return out


def held_out(keys):
    return keys[::HOLD_EVERY]


_PREP = {}


def prep(key, box_seed):
    """A trainer's fight against one random box of its split and one six from
    it: (st, team, boss_keys, flags, the six's species). Seeded by trainer
    and box, so every process and every run builds the same one."""
    k = (key, box_seed)
    if k not in _PREP:
        _PREP.clear()
        rng = random.Random(box_seed * 100003 + key)
        p = plscore.prepare(("tr", key))
        st = p["st"]
        box = fs.random_box(p["split"], rng)
        keys = plscore.box_keys(st, box, rng)
        team = plscore.sixes(keys, 1, rng)[0]
        boss_keys, flags, _s = p["variants"][0]
        _PREP[k] = (st, team, boss_keys, flags, [st["pokemon"][x]["species"] for x in team])
    return _PREP[k]


def data_job(args):
    key, box_seed, positions, seed, out_dir = args
    st, team, boss_keys, flags, names = prep(key, box_seed)
    return pldata.distill(st, team, boss_keys, flags, positions, seed, out_dir,
                          {"fight": f"tr:{key}", "six": names, "box_seed": box_seed})


_LEADS = {}


def read_job(args):
    """One fight of a held-out trainer: the planner's lead for the box (once
    per process), then the fight on the seed's dice."""
    key, box_seed, seed, cfg, luck = args
    st, team, boss_keys, flags, names = prep(key, box_seed)
    lk = (key, box_seed, json.dumps(cfg, sort_keys=True))
    if lk not in _LEADS:
        _LEADS[lk] = plplan.Planner(0, **cfg).lead(st, team, boss_keys, flags)[0]
    r = plplan.play(st, team, boss_keys, flags, _LEADS[lk], seed, cfg, luck)
    return {"key": key, "clean": r["clean"], "won": r["won"], "deaths": r["deaths"], "seconds": r["seconds"]}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("what", choices=("data", "read", "list"))
    ap.add_argument("--boxes", type=int, default=2, help="data: random boxes per trainer")
    ap.add_argument("--positions", type=int, default=2000, help="data: positions per trainer and box")
    ap.add_argument("--held", action="store_true", help="data: the held-out trainers instead of the rest")
    ap.add_argument("--value", help="read: a trained network (plvalue); without it, the play-out planner")
    ap.add_argument("--runs", type=int, default=40, help="read: fights per held-out trainer")
    ap.add_argument("--luck", default="real", choices=("real", "unlucky"))
    ap.add_argument("--procs", type=int)
    ap.add_argument("--save", help="read: write the per-trainer results to ROOT/<name>.json")
    ap.add_argument("--keys", nargs="+", type=int,
                    help="these trainers instead of the held-out ones (read) or the training ones (data)")
    ap.add_argument("--first-box", type=int, default=1, help="data: the first box seed (readings use 0)")
    args = ap.parse_args(argv)
    keys = trainers()
    held = args.keys or held_out(keys)
    if args.what == "list":
        for k in keys:
            t = data.oxide_trainers()[k]
            print(k, trainer_split(k), t["name"], "held out" if k in held else "",
                  ", ".join(m.get("species", "?") for m in t["party"]))
        print(f"{len(keys)} trainers, {len(held)} held out")
        return 0
    procs = args.procs or plplan.pool_size()
    t0 = time.perf_counter()
    if args.what == "data":
        if args.keys:
            chosen, out_dir = args.keys, os.path.join(ROOT, "data-gen-" + "-".join(map(str, args.keys)))
        else:
            chosen = held if args.held else [k for k in keys if k not in held]
            out_dir = os.path.join(ROOT, "data-gen-held" if args.held else "data-gen")
        jobs = [(k, b, args.positions, 1000 * k + b, out_dir) for k in chosen
                for b in range(args.first_box, args.first_box + args.boxes)]
        done = 0
        with plplan.fork_pool(procs) as pool:
            for meta in pool.imap_unordered(data_job, jobs, chunksize=1):
                done += meta["positions"]
                print(f"{meta['fight']} box {meta['box_seed']} ({','.join(meta['six'])}): {meta['positions']} "
                      f"positions from {meta['games']} fights in {meta['seconds']} s", flush=True)
        print(f"{done} positions from {len(jobs)} jobs in {time.perf_counter() - t0:.0f} s on {procs} workers")
        return 0
    cfg = {"value": args.value} if args.value else {}
    jobs = [(k, READ_BOX, 50000 + i, cfg, args.luck) for k in held for i in range(args.runs)]
    with plplan.fork_pool(procs) as pool:
        rows = pool.map(read_job, jobs, chunksize=1)
    per = {}
    for r in rows:
        p = per.setdefault(r["key"], {"clean": 0, "won": 0, "deaths": 0, "runs": 0, "seconds": 0.0})
        p["clean"] += r["clean"]
        p["won"] += r["won"]
        p["deaths"] += r["deaths"]
        p["runs"] += 1
        p["seconds"] += r["seconds"]
    n = len(rows)
    clean = sum(p["clean"] for p in per.values())
    won = sum(p["won"] for p in per.values())
    deaths = sum(p["deaths"] for p in per.values()) / n
    label = args.value or "play-outs"
    print(f"{label} on {len(per)} held-out trainers ({args.luck} odds): clean {clean}/{n}, won {won}/{n}, "
          f"deaths {deaths:.3f}; {sum(p['seconds'] for p in per.values()) / n:.2f} s of one core a fight, "
          f"{time.perf_counter() - t0:.0f} s wall", flush=True)
    for k, p in sorted(per.items()):
        print(f"  {k} {data.oxide_trainers()[k]['name']}: clean {p['clean']}/{p['runs']}, won {p['won']}, "
              f"deaths {p['deaths'] / p['runs']:.2f}")
    if args.save:
        with open(os.path.join(ROOT, args.save + ".json"), "w") as fh:
            json.dump({"value": args.value, "luck": args.luck, "runs": args.runs, "per": per}, fh, indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main())

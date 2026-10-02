"""Stage 1 of the scorer speed plan (docs/oxide/scorer-speed-plan.md): a
record of fixed-seed fights by the planner, to show that a faster version
plays exactly the same fights, and the throughput in fights finished per
hour on the whole machine.

The seeds are the harness's first ones for each of the three gyms. Each
fight's lead is worked out once, as a reading does, then every seed is played
to its end with every turn recorded in full: the planner's options with their
values, its choice, the trainer's pick, and both sides' HP, status and stat
stages after the turn.

    PYTHONPATH=. python3 -m tools.oxide.balance.plspeed record NAME
    PYTHONPATH=. python3 -m tools.oxide.balance.plspeed compare NAME_A NAME_B
"""
import argparse
import json
import multiprocessing as mp
import os
import sys
import time

from . import plplan

SEEDS = {"roark": range(2000, 2012), "mars": range(7000, 7006), "gardenia": range(9000, 9006)}
OUT = os.path.join(os.path.dirname(__file__), "perfectline_results", "step3", "speed")

_FIGHTS = {}


def _lead_value(job):
    fight, i = job
    j = _FIGHTS[fight]
    b = plplan.pl.make_battle(j["st"], j["team"], j["boss_keys"], j["flags"], i)
    return fight, i, plplan.Planner(0).position(b, plplan._mix(0, "lead"))


def _play(job):
    fight, seed = job
    j = _FIGHTS[fight]
    rec = []
    t0 = time.perf_counter()
    r = plplan.play(j["st"], j["team"], j["boss_keys"], j["flags"], j["lead"], seed, {}, "real", record=rec)
    import resource
    return {"fight": fight, "seed": seed, "lead": j["lead"], "won": r["won"], "deaths": r["deaths"],
            "turns": rec, "seconds": round(time.perf_counter() - t0, 2),
            "private_mb": plplan.memory()[1],
            "peak_rss_mb": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss // 1024}


def record(name, procs=None, log=sys.stdout):
    from . import plstep3
    t_setup = time.perf_counter()
    for fight in SEEDS:
        f = plstep3.FIGHTS[fight]
        prep = plstep3.prepare(f, f["six"], f["items"])
        boss_keys, flags, _s = prep["variants"][0]
        _FIGHTS[fight] = {"st": prep["st"], "team": [f"p{i}" for i in range(len(f["six"]))],
                          "boss_keys": boss_keys, "flags": flags}
    setup = time.perf_counter() - t_setup
    parent_mb = plplan.memory()[0]
    procs = procs or plplan.pool_size()
    t0 = time.perf_counter()
    # Each fight's lead is the same planner reading a reading makes (Planner.lead,
    # one candidate per process).
    with plplan.fork_pool(procs) as pool:
        vals = pool.map(_lead_value, [(fight, i) for fight in SEEDS for i in range(6)], chunksize=1)
    leads = {}
    for fight in SEEDS:
        v = [x for f2, i, x in sorted(vals) if f2 == fight]
        _FIGHTS[fight]["lead"] = leads[fight] = max(range(6), key=lambda i: v[i])
    t_lead = time.perf_counter() - t0
    jobs = [(fight, seed) for fight, seeds in SEEDS.items() for seed in seeds]
    t0 = time.perf_counter()
    with plplan.fork_pool(procs) as pool:
        rows = pool.map(_play, jobs, chunksize=1)
    wall = time.perf_counter() - t0
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, name + ".jsonl"), "w") as fh:
        for r in rows:
            fh.write(json.dumps({k: r[k] for k in ("fight", "seed", "lead", "won", "deaths", "turns")}) + "\n")
    summary = {"name": name, "python": sys.version.split()[0], "implementation": sys.implementation.name,
               "procs": procs, "fights": len(rows), "setup_seconds": round(setup, 1),
               "lead_seconds": round(t_lead, 1), "play_wall_seconds": round(wall, 1),
               "fights_per_hour": round(len(rows) / wall * 3600, 1),
               "seconds_per_fight": {f: round(sum(r["seconds"] for r in rows if r["fight"] == f)
                                              / sum(1 for r in rows if r["fight"] == f), 1) for f in SEEDS},
               "leads": leads, "parent_mb": parent_mb,
               "worker_private_mb_max": max(r["private_mb"] for r in rows),
               "worker_peak_rss_mb_max": max(r["peak_rss_mb"] for r in rows)}
    with open(os.path.join(OUT, name + ".summary.json"), "w") as fh:
        json.dump(summary, fh, indent=1)
    print(json.dumps(summary, indent=1), file=log)
    return summary


def load(name):
    """A record's fights by (fight, seed), each decision's timing left out:
    how long a decision took is not part of the answer."""
    out = {}
    with open(os.path.join(OUT, name + ".jsonl")) as fh:
        for r in map(json.loads, fh):
            for t in r["turns"]:
                for note in t["notes"]:
                    note.pop("seconds", None)
            out[(r["fight"], r["seed"])] = r
    return out


def compare(a, b, log=sys.stdout):
    """Every fight of record a against record b, turn by turn: the first
    difference in each fight that has one."""
    ra, rb = load(a), load(b)
    diffs = 0
    for k in sorted(set(ra) | set(rb)):
        x, y = ra.get(k), rb.get(k)
        if x is None or y is None:
            print(f"{k}: in only one record", file=log)
            diffs += 1
            continue
        if x["lead"] != y["lead"]:
            print(f"{k}: leads differ ({x['lead']} against {y['lead']})", file=log)
            diffs += 1
            continue
        for t, (u, v) in enumerate(zip(x["turns"], y["turns"])):
            if u != v:
                keys = [kk for kk in u if u[kk] != v.get(kk)]
                print(f"{k}: turn {t + 1} differs in {keys}", file=log)
                for kk in keys:
                    print(f"    {a}: {json.dumps(u[kk])[:300]}\n    {b}: {json.dumps(v[kk])[:300]}", file=log)
                diffs += 1
                break
        else:
            if len(x["turns"]) != len(y["turns"]):
                print(f"{k}: lengths differ ({len(x['turns'])} against {len(y['turns'])})", file=log)
                diffs += 1
    print(f"{len(ra)} fights against {len(rb)}: {diffs} differ", file=log)
    return diffs


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("action", choices=("record", "compare"))
    ap.add_argument("names", nargs="+")
    ap.add_argument("--procs", type=int, help="workers; by default as many as cores and memory allow")
    args = ap.parse_args(argv)
    if args.action == "record":
        record(args.names[0], args.procs)
        return 0
    return 1 if compare(*args.names[:2]) else 0


if __name__ == "__main__":
    sys.exit(main())

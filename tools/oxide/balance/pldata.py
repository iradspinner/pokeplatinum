"""Labelled positions for stage 2's learned position value
(docs/oxide/scorer-speed-plan.md, "Stage 2, the learned value").

The network is first taught what the planner's play-outs measure today: from
a position, how the fight ends when the plain play-out policy plays it on at
real odds. Each job takes one fight and one six (our hand-played six, or a
random six from the run's box at that fight), and repeats:

1. start from a random lead and play a random number of turns, each turn
   either the plain policy's choice or a random option, so the positions
   cover good play and bad;
2. from there, play the fight to its end with the plain policy, as a
   play-out does, recording every position along the way (plfeat) with the
   fight's end: its value (plplan.value), the faints still to come, and
   whether it was lost.

Shards are written to OUT, outside the repo, each with its fight, six and
seed, so a run can be rebuilt.

    PYTHONPATH=. tools/oxide/capped python3 -m tools.oxide.balance.pldata --sixes 20 --positions 25000
"""
import argparse
import json
import os
import random
import sys
import time

from . import plthreads  # noqa: F401  (one numpy thread per process, before numpy loads)
import numpy as np  # noqa: E402

from . import perfectline as pl
from . import plfeat
from . import plplan

OUT = os.path.expanduser("~/oxide-trials/scorer-stage2/data")
EXPLORE_TURNS = 25        # explore up to this many turns before the play-out
RANDOM_SHARE = 0.5        # the share of exploring turns spent on a random option


def parts(b):
    """A finished position's value in its parts (plplan.value is their
    weighted sum), stored beside the value so another weighting, of a loss
    against a faint for instance, can be applied later without generating
    the data again: the player's faints, whether the fight was lost, the
    survivors' HP shares summed, and when a play-out stopped unfinished the
    trainer's HP share left (averaged over its party)."""
    alive = [m for m in b.p.mons if m.alive()]
    unfinished = bool(alive) and b.b.alive()
    foe = sum(m.hp / m.maxhp for m in b.b.mons if m.alive()) / len(b.b.mons) if unfinished else 0.0
    return (len(b.p.mons) - len(alive), not alive, sum(m.hp / m.maxhp for m in alive), foe)


def save(out_dir, name, xs, ids, vals, future, lost, ends):
    """A shard: the positions, their labels, and each label's parts."""
    np.savez_compressed(os.path.join(out_dir, name + ".npz"), x=np.stack(xs), ids=np.stack(ids),
                        value=np.asarray(vals, np.float32), future=np.asarray(future, np.int8),
                        lost=np.asarray(lost, np.int8),
                        end_faints=np.asarray([e[0] for e in ends], np.int8),
                        end_hp=np.asarray([e[2] for e in ends], np.float32),
                        end_foe_left=np.asarray([e[3] for e in ends], np.float32))


def sixes(fight, n, seed):
    """Our hand-played six first, then n - 1 distinct random sixes from the
    run's box at this fight."""
    from . import plstep3
    f = plstep3.FIGHTS[fight]
    rng = random.Random(seed)
    names = list(f["box"])
    out = [tuple(f["six"])]
    seen = {tuple(sorted(f["six"]))}
    while len(out) < n and len(seen) < 5000:
        six = tuple(rng.sample(names, 6))
        if tuple(sorted(six)) not in seen:
            seen.add(tuple(sorted(six)))
            out.append(six)
    return out


def job(args):
    """One fight and six: its labelled positions written to one shard."""
    fight, six, positions, seed, out_dir = args
    from . import plstep3
    t0 = time.perf_counter()
    f = plstep3.FIGHTS[fight]
    items = f["items"] if list(six) == list(f["six"]) else None
    prep = plstep3.prepare(f, list(six), items)
    st = prep["st"]
    boss_keys, flags, _s = prep["variants"][0]
    team = [f"p{i}" for i in range(len(six))]
    tables = plfeat.Fight(st, team, boss_keys)
    rng = random.Random(seed)
    xs, ids, vals, future, lost, ends = [], [], [], [], [], []
    playouts = 0
    while len(vals) < positions:
        b = pl.make_battle(st, team, boss_keys, flags, rng.randrange(len(team)))
        run = random.Random(rng.getrandbits(32))
        b.dice, b.rng = pl.RunDice(run, luck="real"), run
        plplan.reset()
        for _ in range(rng.randrange(EXPLORE_TURNS + 1)):
            if not b.p.alive() or not b.b.alive():
                break
            if rng.random() < RANDOM_SHARE:
                acts = plplan.options(b)
                a = acts[rng.randrange(len(acts))]
            else:
                a = plplan.plain(b)
            pl.play_turn(b, a, run)
        if not b.p.alive() or not b.b.alive():
            continue
        # The play-out: the plain policy to the end, every position recorded.
        b.plain_switches = 0
        b.pair = None
        seen = []
        stop = b.turn + plplan.PLAYOUT_TURNS
        while b.turn < stop and b.p.alive() and b.b.alive():
            x, i = plfeat.features(b, tables)
            seen.append((x, i, sum(1 for m in b.p.mons if not m.alive())))
            pl.play_turn(b, plplan.plain(b), run)
        playouts += 1
        v = plplan.value(b)
        end = parts(b)
        for x, i, before in seen:
            xs.append(x.astype(np.float16))
            ids.append(i)
            vals.append(v)
            future.append(end[0] - before)
            lost.append(end[1])
            ends.append(end)
    os.makedirs(out_dir, exist_ok=True)
    name = f"{fight}-{seed}"
    save(out_dir, name, xs, ids, vals, future, lost, ends)
    meta = {"fight": fight, "six": list(six), "seed": seed, "positions": len(vals), "playouts": playouts,
            "seconds": round(time.perf_counter() - t0, 1), "private_mb": plplan.memory()[1],
            "floats": plfeat.FLOATS, "ids": plfeat.IDS}
    with open(os.path.join(out_dir, name + ".json"), "w") as fh:
        json.dump(meta, fh)
    return meta


EXPLORE = 0.15        # self-play: the share of turns spent on a random option


def selfplay_job(args):
    """One fight and six played many times by the planner guided by a trained
    network (the speed plan's step 4, the loop that made AlphaZero strong):
    each position where the planner chose is recorded with how the fight
    ended, so the next network learns the value of positions under the
    planner's own play rather than the plain play-out policy's. A random
    lead, and on EXPLORE of the turns a random option, keep the positions
    from narrowing to one line."""
    fight, six, positions, seed, out_dir, model = args
    from . import plstep3
    t0 = time.perf_counter()
    f = plstep3.FIGHTS[fight]
    items = f["items"] if list(six) == list(f["six"]) else None
    prep = plstep3.prepare(f, list(six), items)
    st = prep["st"]
    boss_keys, flags, _s = prep["variants"][0]
    team = [f"p{i}" for i in range(len(six))]
    tables = plfeat.Fight(st, team, boss_keys)
    rng = random.Random(seed)
    xs, ids, vals, future, lost, ends = [], [], [], [], [], []
    games = 0
    while len(vals) < positions:
        b = pl.make_battle(st, team, boss_keys, flags, rng.randrange(len(team)))
        run = random.Random(rng.getrandbits(32))
        b.dice, b.rng = pl.RunDice(run, luck="real"), run
        plplan.reset()
        planner = plplan.Planner(rng.getrandbits(32), value=model)
        plplan._REAL.update(b=b, planner=planner)
        seen = []
        try:
            while b.turn < plplan.TURN_CAP and b.p.alive() and b.b.alive():
                x, i = plfeat.features(b, tables)
                seen.append((x, i, sum(1 for m in b.p.mons if not m.alive())))
                acts = plplan.options(b)
                a = acts[rng.randrange(len(acts))] if rng.random() < EXPLORE else planner.decide(b)
                pl.play_turn(b, a, run)
        finally:
            plplan._REAL.update(b=None, planner=None)
        games += 1
        v = plplan.value(b)
        end = parts(b)
        for x, i, before in seen:
            xs.append(x.astype(np.float16))
            ids.append(i)
            vals.append(v)
            future.append(end[0] - before)
            lost.append(end[1])
            ends.append(end)
    os.makedirs(out_dir, exist_ok=True)
    name = f"{fight}-{seed}"
    save(out_dir, name, xs, ids, vals, future, lost, ends)
    meta = {"fight": fight, "six": list(six), "seed": seed, "positions": len(vals), "playouts": games,
            "games": games, "model": model, "seconds": round(time.perf_counter() - t0, 1),
            "private_mb": plplan.memory()[1], "floats": plfeat.FLOATS, "ids": plfeat.IDS}
    with open(os.path.join(out_dir, name + ".json"), "w") as fh:
        json.dump(meta, fh)
    return meta


def eval_job(args):
    """One fight and six: positions reached as job() reaches them, each
    valued by `k` play-outs of its own (the plain policy to the end, each on
    its own dice), so the mean is a close estimate of the value a single
    play-out labels. The network and the planner's play-out averages are
    both judged against it."""
    fight, six, positions, k, seed, out_dir = args
    from . import plstep3
    f = plstep3.FIGHTS[fight]
    items = f["items"] if list(six) == list(f["six"]) else None
    prep = plstep3.prepare(f, list(six), items)
    st = prep["st"]
    boss_keys, flags, _s = prep["variants"][0]
    team = [f"p{i}" for i in range(len(six))]
    tables = plfeat.Fight(st, team, boss_keys)
    rng = random.Random(seed)
    xs, ids, means, sds = [], [], [], []
    while len(means) < positions:
        b = pl.make_battle(st, team, boss_keys, flags, rng.randrange(len(team)))
        run = random.Random(rng.getrandbits(32))
        b.dice, b.rng = pl.RunDice(run, luck="real"), run
        plplan.reset()
        for _ in range(rng.randrange(EXPLORE_TURNS + 1)):
            if not b.p.alive() or not b.b.alive():
                break
            acts = plplan.options(b)
            a = acts[rng.randrange(len(acts))] if rng.random() < RANDOM_SHARE else plplan.plain(b)
            pl.play_turn(b, a, run)
        if not b.p.alive() or not b.b.alive():
            continue
        x, i = plfeat.features(b, tables)
        vals = []
        for r in range(k):
            c = plplan.clone(b)
            c.dice = c.rng = None
            vals.append(plplan.Planner(0).playout(c, rng.getrandbits(32)))
        xs.append(x.astype(np.float16))
        ids.append(i)
        means.append(float(np.mean(vals)))
        sds.append(float(np.std(vals)))
    os.makedirs(out_dir, exist_ok=True)
    name = f"eval-{fight}-{seed}"
    np.savez_compressed(os.path.join(out_dir, name + ".npz"), x=np.stack(xs), ids=np.stack(ids),
                        mean=np.asarray(means, np.float32), sd=np.asarray(sds, np.float32), k=k)
    meta = {"fight": fight, "six": list(six), "seed": seed, "positions": len(means), "playouts_each": k}
    with open(os.path.join(out_dir, name + ".json"), "w") as fh:
        json.dump(meta, fh)
    return meta


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--fights", nargs="+", default=["roark", "mars", "gardenia"])
    ap.add_argument("--sixes", type=int, default=20, help="sixes per fight, our hand-played six first")
    ap.add_argument("--positions", type=int, default=25000, help="positions per six")
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--repeat", type=int, default=1, help="jobs per six, each with its own seed")
    ap.add_argument("--hand", action="store_true", help="our hand-played six only (with --eval: it alone)")
    ap.add_argument("--out", default=OUT)
    ap.add_argument("--procs", type=int)
    ap.add_argument("--eval", type=int, metavar="K",
                    help="an evaluation set instead: the last --sixes held-out sixes of each fight, "
                         "--positions positions each, each valued by K play-outs")
    ap.add_argument("--of", type=int, default=30, help="with --eval: the sixes drawn per fight in training")
    ap.add_argument("--selfplay", metavar="MODEL",
                    help="positions from fights played by the planner guided by MODEL, labelled by how they ended")
    args = ap.parse_args(argv)
    if args.selfplay:
        jobs = []
        for fight in args.fights:
            for six in sixes(fight, 1 if args.hand else args.sixes, args.seed):
                for _r in range(args.repeat):
                    jobs.append((fight, six, args.positions, args.seed * 100000 + len(jobs), args.out,
                                 args.selfplay))
        procs = args.procs or plplan.pool_size()
        t0 = time.perf_counter()
        done = games = 0
        with plplan.fork_pool(procs) as pool:
            for meta in pool.imap_unordered(selfplay_job, jobs, chunksize=1):
                done += meta["positions"]
                games += meta["games"]
                print(f"selfplay {meta['fight']} {','.join(meta['six'])}: {meta['positions']} positions from "
                      f"{meta['games']} fights in {meta['seconds']} s", flush=True)
        wall = time.perf_counter() - t0
        print(f"{done} positions from {games} fights in {wall:.0f} s on {procs} workers", flush=True)
        return 0
    if args.eval:
        jobs = []
        for fight in args.fights:
            held = sixes(fight, 1, args.seed) if args.hand else sixes(fight, args.of, args.seed)[-args.sixes:]
            for six in held:
                jobs.append((fight, six, args.positions, args.eval, args.seed * 100000 + 900 + len(jobs),
                             args.out + ("-eval-hand" if args.hand else "-eval")))
        procs = args.procs or plplan.pool_size()
        with plplan.fork_pool(procs) as pool:
            for meta in pool.imap_unordered(eval_job, jobs, chunksize=1):
                print(f"eval {meta['fight']} {','.join(meta['six'])}: {meta['positions']} positions, "
                      f"{meta['playouts_each']} play-outs each", flush=True)
        return 0
    jobs = []
    for fight in args.fights:
        for k, six in enumerate(sixes(fight, 1 if args.hand else args.sixes, args.seed)):
            for _r in range(args.repeat):
                jobs.append((fight, six, args.positions, args.seed * 100000 + len(jobs), args.out))
    procs = args.procs or plplan.pool_size()
    t0 = time.perf_counter()
    done = 0
    with plplan.fork_pool(procs) as pool:
        for meta in pool.imap_unordered(job, jobs, chunksize=1):
            done += meta["positions"]
            print(f"{meta['fight']} {','.join(meta['six'])}: {meta['positions']} positions from "
                  f"{meta['playouts']} play-outs in {meta['seconds']} s, {meta['private_mb']} MB", flush=True)
    wall = time.perf_counter() - t0
    print(f"{done} positions in {wall:.0f} s on {procs} workers ({done / wall:.0f} a second)", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())

"""The counterpiece check (Ian, 2026-11-02: "Build it"): a cheap bridge
between the cheap checks and the scorer.

It plays a candidate team for a boss against the six the scorer already
chose to beat the old team on each box of an earlier reading, with the
scorer's own planner, on the reading's final stage: 75 fights at real odds
and 25 very unlucky a box (plteam.full_reading). It skips the team search
(the screen, the race, the play-off and the loop) and reports won, faints
and clean per box, as a reading does.

Its logic is one-sided. A full search could only find a stronger six for
the player than the old one. So a candidate the old six still beats about
as often as it beat the old team (within plteam.WIN_TOL), or that reads
over the fight's target, is too easy for certain. A lower number says only
that the full reading should decide.

Each box is rebuilt by plgoal3.setup with the old reading's run name, so
its level, items, history (rules A and B) and seed are the reading's own,
and the driver refuses a box that does not match the one the reading
recorded. The six takes the reading's moves; its items follow from them as
they did (fightsim.assign_items). Only the trainer's team changes, and it
changes because the tree the driver runs in holds the candidate's trainer
file: no scorer function is patched. `tree` makes such a tree, a copy of a
reading's tree with the candidate's file in it.

    # a tree for the candidate: a copy of the base tree with its file in place
    python3 -m tools.oxide.balance.plcounter tree BASE_TREE DEST --file leader_byron=candidate.json
    # the check, run from inside that tree
    cd DEST && PYTHONPATH=. tools/oxide/capped --max 10G python3 -m tools.oxide.balance.plcounter \\
        read ~/oxide-trials/goal3/byron-0db1aeaee byron --name C3 --target 88

docs/oxide/counterpiece-check.md has the method and the checks it passed.
"""
import argparse
import json
import os
import shutil
import sys
import time

from . import plthreads  # noqa: F401  (one numpy thread per process, before anything loads numpy)
from . import data, fightsim as fs, plgoal3, plstudy, plteam

TRAINERS = os.path.join("res", "trainers", "data")
OUT = os.path.join(plgoal3.OUT, "counterpiece")
FIRST_SEED = 9          # full_reading's own seed: trial 0 replays the reading's dice


class Mismatch(Exception):
    """The rebuilt box is not the one the old reading read."""


# ---- one box ------------------------------------------------------------------------------------------------

def old_result(run_dir, slug, seed):
    path = os.path.join(run_dir, slug, f"box{seed}", "result.json")
    with open(path) as fh:
        r = json.load(fh)
    if r.get("how") != "search":
        raise SystemExit(f"{path}: not a boss's search reading (how {r.get('how')!r}), so it chose no six")
    return r


def rebuild(run, slug, seed, old):
    """The box as the old reading built it, against the trainer file this
    tree holds: (st, keys, boss_keys, flags, setup). Refuses a box whose
    members, level, starter or history differ from the reading's. (The
    run's item stock is not in the result, whose "items" became the six's;
    the_six checks those.)"""
    s = plgoal3.setup(run, slug, seed)
    recs = s["built"]["records"]
    got = [f"{r['label']} ({r['area']})" for r in recs]
    wrong = []
    if got != old["box"]:
        extra = [x for x in got if x not in old["box"]]
        missing = [x for x in old["box"] if x not in got]
        wrong.append(f"box differs: {len(got)} members against {len(old['box'])}; new {extra[:5]}, "
                     f"missing {missing[:5]}")
    for what, mine, theirs in (("level", s["lvl"], old["level"]), ("starter", s["whole"][0].species, old["starter"]),
                               ("history", s["hist_from"], old.get("history_from", []))):
        if mine != theirs:
            wrong.append(f"{what} differs: {mine!r} against the reading's {theirs!r}")
    if wrong:
        raise Mismatch(f"{slug} box {seed}: " + "; ".join(wrong))
    st, keys, boss_keys, flags = plgoal3.fight_state(s["key"], recs, s["stock"], s["v"], slug)
    return st, keys, boss_keys, flags, s


def the_six(st, keys, old):
    """The reading's six as keys of this state, with the reading's moves
    set on each member, in the reading's order. Members are matched by
    label and catch (the reading's "chosen"), so two versions of one catch
    are told apart."""
    by = {(st["pokemon"][k]["label"], st["pokemon"][k]["area"]): k for k in keys}
    win = []
    for u in old["chosen"]:
        k = by.get((u["label"], u["area"]))
        if k is None:
            raise Mismatch(f"the reading's member {u['label']} ({u['area']}) is not in the rebuilt box")
        win.append(k)
    names = [plteam.member_name(st["pokemon"][k]) for k in win]
    if names != old["winner"]:
        raise Mismatch(f"the six reads {names}, the reading's was {old['winner']}")
    # The reading keyed its moves by species, in the six's order; two
    # members of one species would share a key, so then go by species.
    moves = list(old["moves"].values())
    if len(moves) != len(win):
        moves = [old["moves"][st["pokemon"][k]["species"]] for k in win]
    for k, four in zip(win, moves):
        st["moves"][k] = list(four)
        st["pokemon"][k] = dict(st["pokemon"][k], moves=list(four))
    items = {st["pokemon"][k]["species"]: it for k, it in fs.assign_items(st, win).items() if it}
    # The result's "items" is the six's, as fightsim gave them from the
    # run's stock; the same moves and stock must give the same items.
    if items != old["items"]:
        raise Mismatch(f"the six's items come out {items}, the reading's were {old['items']}")
    return win


def box_check(run, slug, seed, old, trials=1, procs=None, cfg=None, real=75, unlucky=25):
    """One box: the reading's six against the trainer file this tree holds,
    on `trials` full readings, the first on the reading's own dice."""
    st, keys, boss_keys, flags, _s = rebuild(run, slug, seed, old)
    win = the_six(st, keys, old)
    out = {"seed": seed, "six": old["winner"], "moves": {plteam.member_name(st["pokemon"][k]): st["moves"][k]
                                                         for k in win},
           "items": {plteam.member_name(st["pokemon"][k]): it for k, it in fs.assign_items(st, win).items() if it},
           "foes": [f"{st['pokemon'][k]['species']} {st['pokemon'][k]['level']}" for k in boss_keys],
           "old": {"real": old["real"], "unlucky": old["unlucky"], "foes": old["foes"]}, "trials": []}
    rows_real = []
    for i in range(trials):
        t0 = time.time()
        r, u, rows = plteam.full_reading(st, boss_keys, flags, win, cfg or {}, real=real, unlucky=unlucky,
                                         procs=procs, seed=FIRST_SEED + i)
        rows_real += rows
        out["trials"].append({"seed": FIRST_SEED + i, "real": r, "unlucky": u,
                              "faints_to": plteam.losing_enemies(rows), "fainted": plstudy.fainted(rows),
                              "minutes": round((time.time() - t0) / 60, 1)})
    out["real"] = pooled([t["real"] for t in out["trials"]])
    out["unlucky"] = pooled([t["unlucky"] for t in out["trials"]])
    out["faints_to"] = plteam.losing_enemies(rows_real)
    return out


def pooled(nums):
    """Readings' numbers pooled, each weighted by its fights."""
    n = sum(x["fights"] for x in nums)
    if not n:
        return {"fights": 0, "won": 0.0, "faints": 0.0, "clean": 0.0}
    return {"fights": n, **{k: sum(x[k] * x["fights"] for x in nums) / n for k in ("won", "faints", "clean")}}


# ---- the verdict ----------------------------------------------------------------------------------------------

def verdict(won, old_won, target=None, tol=plteam.WIN_TOL):
    """The check's one-sided answer for a rate won at real odds: "too easy"
    where the old six still wins about as often as it beat the old team, or
    the rate is over the target (a fraction); else "reading decides"."""
    if won >= old_won - tol:
        return "too easy (old six wins as often)"
    if target is not None and won > target:
        return "too easy (over the target)"
    return "reading decides"


def judge(boxes, target=None):
    """Each box's verdict and the pooled one, the old reading pooled the same way."""
    for b in boxes:
        b["verdict"] = verdict(b["real"]["won"], b["old"]["real"]["won"], target)
    real = pooled([b["real"] for b in boxes])
    old = pooled([b["old"]["real"] for b in boxes])
    return {"real": real, "unlucky": pooled([b["unlucky"] for b in boxes]), "old_real": old,
            "verdict": verdict(real["won"], old["won"], target)}


def pct(x):
    return f"{100 * x:.0f}"


def table(res):
    """The short table: each box and the pool, the old reading beside."""
    lines = [f"{res['name']} against {res['run']}'s sixes ({res['slug']}), tree {res['tree']}",
             "the team met: " + ", ".join(res["foes"]),
             "",
             "| Box | Won | Faints | Clean | Very unlucky: won, faints | Trials' won | Old reading: won, faints, clean "
             "| Verdict |",
             "|---|---:|---:|---:|---|---|---|---|"]
    for b in res["boxes"]:
        r, u, o = b["real"], b["unlucky"], b["old"]["real"]
        spread = ", ".join(pct(t["real"]["won"]) for t in b["trials"])
        lines.append(f"| {b['seed']} | {pct(r['won'])} | {r['faints']:.2f} | {pct(r['clean'])} | {pct(u['won'])}, "
                     f"{u['faints']:.2f} | {spread} | {pct(o['won'])}, {o['faints']:.2f}, {pct(o['clean'])} "
                     f"| {b['verdict']} |")
    p, u, o = res["pool"]["real"], res["pool"]["unlucky"], res["pool"]["old_real"]
    lines.append(f"| all | {pct(p['won'])} | {p['faints']:.2f} | {pct(p['clean'])} | {pct(u['won'])}, "
                 f"{u['faints']:.2f} | | {pct(o['won'])}, {o['faints']:.2f}, {pct(o['clean'])} "
                 f"| {res['pool']['verdict']} |")
    for b in res["boxes"]:
        lines.append(f"box {b['seed']}: {', '.join(b['six'])}; its faints fell to {b['faints_to'][:4]}")
    return "\n".join(lines)


def check(run_dir, slug, name, seeds=plgoal3.SEEDS, trials=1, procs=None, target=None, cfg=None, real=75,
          unlucky=25, log=print):
    run_dir = os.path.abspath(os.path.expanduser(run_dir))
    run = os.path.basename(run_dir)
    t0 = time.time()
    boxes = []
    for seed in seeds:
        old = old_result(run_dir, slug, seed)
        boxes.append(box_check(run, slug, seed, old, trials, procs, cfg, real, unlucky))
        b = boxes[-1]
        log(f"{name} box {seed}: real {pct(b['real']['won'])}% won, {b['real']['faints']:.2f} faints, "
            f"{pct(b['real']['clean'])}% clean; very unlucky {pct(b['unlucky']['won'])}%, "
            f"{b['unlucky']['faints']:.2f} (the old reading {pct(b['old']['real']['won'])}%)")
    res = {"check": "counterpiece", "name": name, "run": run, "slug": slug, "tree": data.ROOT,
           "trainer": old_result(run_dir, slug, seeds[0])["trainer"],
           "foes": boxes[0]["foes"], "same_team_as_reading": all(b["foes"] == b["old"]["foes"] for b in boxes),
           "trials": trials, "fights_per_trial": {"real": real, "unlucky": unlucky}, "target": target,
           "boxes": boxes, "minutes": None}
    res["pool"] = judge(boxes, target)
    res["minutes"] = round((time.time() - t0) / 60, 1)
    return res


# ---- a tree for a candidate ----------------------------------------------------------------------------------

def trainer_file(src, stem, base):
    """The candidate's trainer file for `stem`: a whole trainer file; a
    tree's own (`src` a directory); or a partial file, such as {"party":
    [...], "ai_flags": [...]}, laid over the base tree's file."""
    if os.path.isdir(src):
        src = os.path.join(src, TRAINERS, stem + ".json")
    with open(src) as fh:
        tr = json.load(fh)
    if "class" not in tr:
        with open(os.path.join(base, TRAINERS, stem + ".json")) as fh:
            tr = dict(json.load(fh), **tr)
    return tr, src


def make_tree(base, dest, files, note=None):
    """A copy of `base` at `dest` with each (stem, source) trainer file in
    place, and this driver in it should the base tree be older than it.
    Each change is listed in the copy's PATCHED.txt."""
    base, dest = os.path.abspath(os.path.expanduser(base)), os.path.abspath(os.path.expanduser(dest))
    if os.path.exists(dest):
        raise SystemExit(f"{dest} exists; give a new directory")
    shutil.copytree(base, dest, symlinks=True, ignore=shutil.ignore_patterns("__pycache__"))
    notes = []
    for stem, src in files:
        tr, where = trainer_file(os.path.expanduser(src), stem, base)
        with open(os.path.join(dest, TRAINERS, stem + ".json"), "w") as fh:
            json.dump(tr, fh, indent=4)
            fh.write("\n")
        notes.append(f"{TRAINERS}/{stem}.json from {where} (plcounter tree)")
    mine = os.path.join(dest, "tools", "oxide", "balance", "plcounter.py")
    if not os.path.exists(mine):
        shutil.copy2(os.path.abspath(__file__), mine)
        notes.append("tools/oxide/balance/plcounter.py copied in (plcounter tree)")
    if note:
        notes.append(note)
    with open(os.path.join(dest, "PATCHED.txt"), "a") as fh:
        fh.write("".join(n + "\n" for n in notes))
    return notes


# ---- the command line ------------------------------------------------------------------------------------------

def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = p.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("read", help="the check, against the trainer file of the tree it runs in")
    r.add_argument("run_dir", help="the old reading's run directory, e.g. ~/oxide-trials/goal3/byron-0db1aeaee")
    r.add_argument("slug", help="the fight's slug, e.g. byron")
    r.add_argument("--name", required=True, help="the candidate's name, for the table and the file")
    r.add_argument("--boxes", default=",".join(map(str, plgoal3.SEEDS)), help="box seeds, comma-separated")
    r.add_argument("--trials", type=int, default=1, help="full readings a box; the first on the reading's dice")
    r.add_argument("--procs", type=int, default=8)
    r.add_argument("--target", type=float, help="the fight's highest acceptable percent won, e.g. 88")
    r.add_argument("--out", help="the JSON file (default: ~/oxide-trials/goal3/counterpiece/<run>-<name>.json)")
    t = sub.add_parser("tree", help="a copy of a tree with a candidate's trainer files in it")
    t.add_argument("base")
    t.add_argument("dest")
    t.add_argument("--file", action="append", default=[], metavar="STEM=SOURCE",
                   help="a trainer file (whole, or partial over the base's) or a tree whose file to take")
    t.add_argument("--note", help="a line for PATCHED.txt")
    a = p.parse_args(argv)
    if a.cmd == "tree":
        for n in make_tree(a.base, a.dest, [tuple(f.split("=", 1)) for f in a.file], a.note):
            print(n)
        return 0
    seeds = tuple(int(s) for s in a.boxes.split(","))
    target = a.target / 100 if a.target is not None else None
    res = check(a.run_dir, a.slug, a.name, seeds, a.trials, a.procs, target)
    out = a.out or os.path.join(OUT, f"{res['run']}-{a.name}.json")
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    with open(out + ".part", "w") as fh:
        json.dump(res, fh, indent=1)
    os.replace(out + ".part", out)
    print(table(res))
    print(f"written to {out}; {res['minutes']} minutes")
    return 0


if __name__ == "__main__":
    sys.exit(main())

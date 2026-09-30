"""The perfect-line readings of Oxide's fights (out/design.md).

    PYTHONPATH=~/pokeplatinum python3 run.py roark gardenia tr:323     # read fights
    PYTHONPATH=~/pokeplatinum python3 run.py roark --team Marshtomp,Wartortle,Prinplup,Turtwig,Kricketune,Luxio --trace
    PYTHONPATH=~/pokeplatinum python3 run.py --report                  # the table from saved readings

A fight is a story key from tools/oxide/balance/fights.json or tr:<trainer
id>. For each, BOXES random boxes are drawn by the fight's split; from each
box BLIND random sixes are searched as they come (step 1, the blind share)
and PLANNED sixes are searched for the planned share (step 2). A rival's
variant is the one the box's starter meets. Doubles and tag fights are not
read (design.md). Readings are saved to results/<fight>.json.
"""
import argparse
import collections
import json
import multiprocessing as mp
import os
import random
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))


from . import b6, calibrate, data, fightsim as fs, pool, pressure, splits
from . import pboxes as boxes
from . import perfectline as pl

RESULTS = os.path.join(HERE, "perfectline_results")
BOXES = 10
BLIND = 5
PLANNED = 8
SEED = 20260930
# Barry's starter beats the player's, so the rival variant a box meets is
# named by the player's starter (the data files are named that way too).
# Trainers the placements leave to their map's split although the player
# meets them later: Officer Somnu at Lake Verity is the return visit
# before Mars 2 (docs/oxide/pairwise-candidates.md, pair 23).
SPLIT_OVERRIDE = {420: "Candice"}
STARTER_VARIANT = {"SPECIES_TURTWIG": "TURTWIG", "SPECIES_CHIMCHAR": "CHIMCHAR", "SPECIES_PIPLUP": "PIPLUP"}


# ---- Ian's movesets --------------------------------------------------------------------------------

def ian_moves(rec, can_names, tiers, types):
    """Four moves in Ian's order (2026-09-30): the strongest same-type
    attack, then the strongest attack of another type (a second same-type
    or coverage), then a third type, then the highest-tier status move the
    engine models (B or better), else a fourth attack."""
    damaging = [n for n in can_names if fs.move(n).damaging() and n not in pool.CONDITIONAL
                and fs.play_strength(n, types) > 0]
    ranked = sorted(damaging, key=lambda n: -fs.play_strength(n, types))
    attacks, seen = [], set()
    stab = [n for n in ranked if fs.move(n).type in types]
    if stab:
        attacks.append(stab[0])
        seen.add(fs.move(stab[0]).type)
    for n in ranked:
        if len(attacks) == 3:
            break
        if fs.move(n).type not in seen:
            attacks.append(n)
            seen.add(fs.move(n).type)
    status = [n for n in can_names if fs.move(n).cat == "Status" and fs.move(n).effect in fs.POLICY_STATUS
              and tiers.get(n, 0) >= fs.TIERS["B"]]
    status.sort(key=lambda n: -tiers.get(n, 0))
    if status:
        return attacks + status[:1]
    rest = [n for n in ranked if n not in attacks]
    return attacks + rest[:1]


fs.player_moves = ian_moves
fs.BOX_MODE = True


# ---- fights ----------------------------------------------------------------------------------------------

def parse_fight(name):
    if name.startswith("tr:"):
        return ("tr", int(name[3:]))
    return ("story", name)


def fight_label(f):
    kind, key = f
    if kind == "story":
        return next(x["label"] for x in data.fights()["fights"] if x["key"] == key)
    return data.oxide_trainers()[key]["name"]


def prepare(f):
    """The fight's state for the search: {"st", "flags", "variants": [(boss
    keys, flags, starter or None)], "split", "label"}, or None when the
    fight is a double battle."""
    kind, key = f
    if kind == "story":
        fight = next(x for x in data.fights()["fights"] if x["key"] == key)
        if fight.get("tag"):
            return None
        trainers = data.fight_trainers("oxide", fight)
        parties = [t["party"] for t in trainers]
        weather = pressure.fight_weather([t["tr_id"] for t in trainers])
        split = fight["split"]
        cap = fs.fight_cap(split, key)
        st = fs.prepare(split, parties, weather, bool(fight.get("trick_room")), cap=cap)
        variants = []
        for v, t in enumerate(trainers):
            starter = next((sp for sp, tag in STARTER_VARIANT.items() if t["constant"].endswith("_" + tag)), None)
            variants.append((st["bosses"][v], t["ai"], starter))
        return {"st": st, "variants": variants, "split": split, "label": fight["label"], "key": key}
    t = data.oxide_trainers()[key]
    if t.get("battle_type") == "Doubles" and len(t["party"]) > 1:
        return None
    split = SPLIT_OVERRIDE.get(key) or (b6.placements()[key]["split"] if key in b6.placements()
                                        else splits.trainer_split(key))
    st = fs.prepare(split, [t["party"]], pressure.fight_weather([key]), cap=fs.fight_cap(split))
    return {"st": st, "variants": [(st["bosses"][0], t["ai"], None)], "split": split,
            "label": t["name"], "key": f"tr{key}"}


# ---- teams from boxes -------------------------------------------------------------------------------------

def box_keys(st, box, rng):
    """The state's keys for a box's species, one of each species' regular
    abilities drawn at random; a stage the side lacks falls back to its
    pre-evolution in the side, else is left out."""
    by_species = {}
    for k in st["player"]:
        by_species.setdefault(st["pokemon"][k]["constant"], k)
    pre = pool.pre_evolutions()
    keys = []
    for sp in box:
        k = by_species.get(sp)
        if k is None:
            k = next((by_species[p] for p in pre.get(sp, []) if p in by_species), None)
        if k is None:
            continue
        keys.append(rng.choice(st["variants"].get(k, [k])))
    return keys


def sixes(keys, n, rng, weights=None):
    """n distinct sixes from the box's keys (all of them when the box has
    six or fewer): random, or with `weights` the first is the six with the
    highest weights and the rest are drawn leaning on them, as a player
    planning for the fight picks."""
    if len(keys) <= 6:
        return [list(keys)]
    out, seen = [], set()
    if weights:
        best = sorted(keys, key=lambda k: (-weights.get(k, 0), rng.random()))[:6]
        seen.add(tuple(sorted(best)))
        out.append(sorted(best))
    tries = 0
    while len(out) < n and tries < n * 20:
        tries += 1
        if weights:
            pick = sorted(keys, key=lambda k: -rng.random() ** (1 / (1 + 2 * weights.get(k, 0))))[:6]
        else:
            pick = rng.sample(keys, 6)
        team = tuple(sorted(pick))
        if team not in seen:
            seen.add(team)
            out.append(list(team))
    return out


def variant_for(prep, box):
    """The boss variant this box meets: a rival by the box's starter."""
    vs = prep["variants"]
    if len(vs) == 1:
        return vs[0]
    starter = box[0]
    return next((v for v in vs if v[2] == starter), vs[0])


# ---- the jobs -------------------------------------------------------------------------------------------------

_PREP = None
# The line search per six (lines.py): candidates, screening runs each, and
# the fresh runs the best is confirmed on. A blind six gets fewer
# candidates than a planned one, since no one plans a blind fight.
BLIND_SEARCH = dict(candidates=60, screen_runs=20, confirm_runs=200)
PLANNED_SEARCH = dict(candidates=300, screen_runs=20, confirm_runs=300)


def _init(prep):
    global _PREP
    _PREP = prep


def _job(args):
    team, boss_keys, flags, kind, budget, strict, seed = args
    st = _PREP["st"]
    species = [st["pokemon"][k]["species"] for k in team]
    if strict:
        r = pl.perfect(st, team, boss_keys, flags, budget=budget)
        return {"kind": kind, "team": species, "found": r["found"], "nodes": r["nodes"],
                "seconds": r["seconds"], "disc": r["disc"]}
    from . import plines as lines
    t0 = time.time()
    r = lines.search(st, team, boss_keys, flags, seed=seed,
                     **(BLIND_SEARCH if kind.startswith("blind") else PLANNED_SEARCH))
    r.update({"kind": kind, "team": species, "seconds": round(time.time() - t0, 1)})
    return r


def read_fight(prep, n_boxes=BOXES, blind=BLIND, planned=PLANNED, procs=None, seed=SEED,
               budget=pl.BUDGET, strict=False, log=sys.stdout):
    st = prep["st"]
    rng = random.Random(seed)
    jobs = []
    for bi in range(n_boxes):
        box = boxes.random_box(prep["split"], random.Random(seed * 100 + bi))
        keys = box_keys(st, box, rng)
        boss_keys, flags, _starter = variant_for(prep, box)
        for j, team in enumerate(sixes(keys, blind, rng)):
            jobs.append((team, boss_keys, flags, f"blind:{bi}", budget, strict, seed + 1000 * bi + j))
        weights = pl.matchup_wins(st, keys, boss_keys, flags, budget)
        for j, team in enumerate(sixes(keys, planned, rng, weights)):
            jobs.append((team, boss_keys, flags, f"planned:{bi}", budget, strict, seed + 1000 * bi + 100 + j))
    t0 = time.time()
    ctx = mp.get_context("fork")
    with ctx.Pool(procs or max(1, os.cpu_count() - 2), initializer=_init, initargs=(prep,)) as pool_:
        rows = pool_.map(_job, jobs, chunksize=1)
    out = summarise_strict(rows) if strict else summarise(rows)
    out.update({"label": prep["label"], "split": prep["split"], "boxes": n_boxes, "blind": blind,
                "planned": planned, "budget": budget, "strict": strict,
                "seconds": round(time.time() - t0, 1), "rows": rows})
    if strict:
        print(f"{prep['label']:28} blind {out['blind_share']:.2f}  planned {out['planned_share']:.2f}  "
              f"boxes with a line {out['box_share']:.2f}  undecided {out['undecided']:.2f}  "
              f"({len(rows)} searches, {out['seconds']} s)", file=log, flush=True)
    else:
        print(f"{prep['label']:28} blind {out['blind_rate']:.2f}  planned {out['planned_rate']:.2f}  "
              f"deaths {out['planned_deaths']:.2f}  wipe {out['planned_wipe']:.2f}  "
              f"best {out['best_rate']:.2f}  conv {out['convergence']}  ({len(rows)} sixes, {out['seconds']} s)",
              file=log, flush=True)
    return out


def summarise(rows):
    """The fight's readings from its sixes: the blind rate (the mean best
    clean-win rate over random sixes), the planned rate (each box's best
    six, averaged over boxes), the best six anywhere, and the convergence
    curve (the mean best screening rate after 10, 50, 100 and all
    candidates over the planned sixes)."""
    blind = [r for r in rows if r["kind"].startswith("blind")]
    planned = [r for r in rows if r["kind"].startswith("planned")]
    by_box = collections.defaultdict(list)
    boxes_rows = collections.defaultdict(list)
    for r in planned:
        by_box[r["kind"].split(":")[1]].append(r["rate"])
        boxes_rows[r["kind"].split(":")[1]].append(r)
    # Each box's best six: the highest clean-win rate, then the fewest deaths.
    best_six = [max(rs, key=lambda r: (r["rate"], -r.get("deaths", 0.0))) for rs in boxes_rows.values()]
    def at_most(screen, at):
        """The best screening rate once `at` candidates had been tried: the
        curve's last point at or before it, else its first (a search that
        stopped early had found a line that never failed)."""
        keys = sorted(int(k) for k in screen)
        below = [k for k in keys if k <= at]
        return screen[str(below[-1])] if below else screen[str(keys[0])]
    curve = {}
    for at in (10, 50, 100, PLANNED_SEARCH["candidates"]):
        vals = [at_most({str(k): v for k, v in r["screen"].items()}, at) for r in planned]
        if vals:
            curve[at] = round(sum(vals) / len(vals), 3)
    mean = lambda xs: round(sum(xs) / len(xs), 3) if xs else 0.0
    return {"blind_rate": mean([r["rate"] for r in blind]),
            "blind_clean_share": mean([1.0 if r["rate"] >= 0.9 else 0.0 for r in blind]),
            "planned_rate": mean([max(v) for v in by_box.values()]),
            "planned_clean_share": mean([1.0 if max(v) >= 0.9 else 0.0 for v in by_box.values()]),
            "best_rate": max((r["rate"] for r in planned + blind), default=0.0),
            # What the best line costs where it does not win cleanly: its mean
            # deaths and the chance of a wipe, for each box's best six and
            # over the blind sixes.
            "planned_deaths": mean([r.get("deaths", 0.0) for r in best_six]),
            "planned_wipe": mean([r.get("wipe", 0.0) for r in best_six]),
            "blind_deaths": mean([r.get("deaths", 0.0) for r in blind]),
            "blind_wipe": mean([r.get("wipe", 0.0) for r in blind]),
            "convergence": curve,
            "runs": sum(r.get("runs", 0) for r in rows)}


def summarise_strict(rows):
    blind = [r for r in rows if r["kind"].startswith("blind")]
    planned = [r for r in rows if r["kind"].startswith("planned")]
    by_box = collections.defaultdict(list)
    for r in rows:
        by_box[r["kind"].split(":")[1]].append(r)

    def share(rs):
        return sum(1 for r in rs if r["found"]) / len(rs) if rs else 0.0
    return {"blind_share": round(share(blind), 3), "planned_share": round(share(planned), 3),
            "box_share": round(sum(1 for rs in by_box.values() if any(r["found"] for r in rs)) / len(by_box), 3)
            if by_box else 0.0,
            "undecided": round(sum(1 for r in rows if r["found"] is None) / len(rows), 3) if rows else 0.0,
            "mean_nodes": round(sum(r["nodes"] for r in rows) / len(rows)) if rows else 0}


# ---- the report -----------------------------------------------------------------------------------------------

def report(out=sys.stdout, strict=False):
    rows = []
    for name in sorted(os.listdir(RESULTS)) if os.path.isdir(RESULTS) else []:
        with open(os.path.join(RESULTS, name), encoding="utf-8") as f:
            r = json.load(f)
        if bool(r.get("strict")) == strict:
            rows.append(r)
    if strict:
        print(f"{'fight':30}{'split':10}{'blind':>7}{'planned':>9}{'boxes':>7}{'undec.':>8}{'Ian':>5}", file=out)
        for r in sorted(rows, key=lambda r: -r["planned_share"]):
            ian = calibrate.IAN_RATINGS.get(r.get("key"), "")
            print(f"{r['label'][:29]:30}{r['split']:10}{r['blind_share']:>7.2f}{r['planned_share']:>9.2f}"
                  f"{r['box_share']:>7.2f}{r['undecided']:>8.2f}{str(ian):>5}", file=out)
        return
    print(f"{'fight':30}{'split':10}{'blind':>7}{'planned':>9}{'deaths':>8}{'wipe':>6}{'best':>6}"
          f"{'conv 10/50/100/all':>22}{'Ian':>5}", file=out)
    for r in sorted(rows, key=lambda r: -r["planned_rate"]):
        ian = calibrate.IAN_RATINGS.get(r.get("key"), "")
        conv = "/".join(f"{v:.2f}" for v in r["convergence"].values())
        print(f"{r['label'][:29]:30}{r['split']:10}{r['blind_rate']:>7.2f}{r['planned_rate']:>9.2f}"
              f"{r.get('planned_deaths', 0):>8.2f}{r.get('planned_wipe', 0):>6.2f}"
              f"{r['best_rate']:>6.2f}{conv:>22}{str(ian):>5}", file=out)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("fights", nargs="*")
    ap.add_argument("--boxes", type=int, default=BOXES)
    ap.add_argument("--blind", type=int, default=BLIND)
    ap.add_argument("--planned", type=int, default=PLANNED)
    ap.add_argument("--procs", type=int)
    ap.add_argument("--budget", type=float, default=pl.BUDGET)
    ap.add_argument("--team", help="one six by species names, searched alone")
    ap.add_argument("--trace", action="store_true")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--strict", action="store_true", help="the strict perfect-line search instead of lines")
    args = ap.parse_args(argv)
    if args.report:
        report(strict=args.strict)
        return 0
    os.makedirs(RESULTS, exist_ok=True)
    for name in args.fights:
        prep = prepare(parse_fight(name))
        if prep is None:
            print(f"{name}: a double battle, not read", flush=True)
            continue
        if args.team:
            st = prep["st"]
            team = [next(k for k in st["player"] if st["pokemon"][k]["species"] == sp)
                    for sp in args.team.split(",")]
            boss_keys, flags, _s = prep["variants"][0]
            print([(st["pokemon"][k]["species"], st["moves"][k], st["info"][k]["hp"]) for k in team])
            if args.strict:
                r = pl.perfect(st, team, boss_keys, flags, budget=args.budget, want_trace=args.trace,
                               node_cap=100000, time_cap=120)
                print(prep["label"], r["found"], "nodes", r["nodes"], "secs", r["seconds"], "disc", r["disc"])
                if r["trace"]:
                    print("\n".join("   " + x for x in r["trace"]))
            else:
                from . import plines as lines
                r = lines.search(st, team, boss_keys, flags, **PLANNED_SEARCH)
                print(prep["label"], r)
            continue
        out = read_fight(prep, args.boxes, args.blind, args.planned, args.procs, budget=args.budget,
                         strict=args.strict)
        out["key"] = prep["key"]
        name = f"{prep['key']}{'-strict' if args.strict else ''}.json"
        with open(os.path.join(RESULTS, name), "w", encoding="utf-8") as f:
            json.dump(out, f, indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main())

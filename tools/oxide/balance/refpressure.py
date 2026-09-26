"""B3b: the reference hacks' bosses scored against Oxide's side.

    PYTHONPATH=. python3 -m tools.oxide.balance.refpressure --hack renegade --split Roark
    PYTHONPATH=. python3 -m tools.oxide.balance.refpressure --hack null --fight roark
    PYTHONPATH=. python3 -m tools.oxide.balance.refpressure --report
    PYTHONPATH=. python3 -m tools.oxide.balance.refpressure --report --hack kaizo

The same scores as pressure.py gives Oxide's own fights (threat, answers,
and answers counting a Choice lock), for each reference hack's fight in the
same seat. The player's side is Oxide's at that seat's split and cap
(pool.py), so every score answers one question: if this fight were in
Oxide, how hard would it be? A Platinum-based hack's fight is its own fight
at the same trainer id; a hack built on another game fills the seat its
milestone map gives it (fights.json), which covers the gyms and the League.

Each boss Pokemon is built from its own game's data, since every hack
rebalances species and moves: base stats and types from the hack's species
table (metrics.mon_stats; Unbound and Run & Bun have none and use the
current canonical stats), and each move's type, power, category and
priority from the hack's move table (metrics.lookup_move). The Oxide engine
does the damage, with Oxide's type chart. A Mega is scored as its Mega form.
A Pokemon whose species no table knows, and a move no table knows, are left
out and listed per fight.

Weather: a reference fight starts in no field weather, only in what a boss
Pokemon's own ability sets up. The references' data carry no map weather,
and vanilla Platinum's gyms have none; Oxide's four weather fights keep
theirs in pressure.json, since that weather is part of Oxide. Trick Room is
the same: Oxide's Saturn 2 is fought under it (fights.json), but a
reference hack's fight in that seat is scored at ordinary Speed order.

Each hack's results go to pressure_refs/<hack>.json, one file per hack, so
runs for different hacks can go side by side without sharing a file.
"""
import argparse
import json
import os
import sys
import tempfile
import time

from ..encounters import calc_export
from . import data, metrics, pool, pressure

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(HERE, "pressure_refs")
HACKS = [h for h in data.REFS]
# Hidden Power written with its type ("Hidden Power Fire") is the later
# games' fixed 60-power special move of that type.
HIDDEN_POWER_BP = 60


def out_path(hack):
    return os.path.join(OUT_DIR, f"{hack}.json")


def parties(hack, fight):
    """[[boss Pokemon]] per variant, as metrics.fight_metrics groups them: a
    rival's starters are variants, and any other fight with more than one
    trainer (a tag battle, Tate and Liza) is one party."""
    trainers = data.fight_trainers(hack, fight)
    if len(trainers) > 1 and not fight["key"].startswith("barry"):
        return [[m for t in trainers for m in t["party"]]]
    return [t["party"] for t in trainers]


def _weight(hack, name, blob):
    """The Pokemon's weight for Low Kick and Grass Knot: Oxide's record, else
    the hack's own, else None, which leaves the engine's own species table
    to supply it (a species that table lacks too gets no weight, and a
    weight-based move against it is reported as an error, not scored)."""
    own = (data.raw(hack).get("poks", {}).get(name)
           if data.REFS[hack].get("source") is None else None)
    for rec in (blob["poks"].get(name), own):
        if rec and rec.get("weightkg"):
            return rec["weightkg"]
    return None


def _full(stats, default):
    """All six stats, since some sources list only some (vanilla's file gives
    EVs as {"df": 0}); a missing IV is the calculator's own default of 31,
    and a missing EV is 0."""
    if not stats:
        return None
    return {k: stats.get(k, default) for k in metrics.STATS}


def boss_mon(hack, mon, blob, notes):
    """The job record for one reference Pokemon, or None when its species is
    known to no table. `notes` gathers what was left out or guessed."""
    name = mon.get("mega") or mon["species"]
    probe = {"species": name} if mon.get("mega") else mon
    bs, types, source = metrics.mon_stats(hack, probe)
    if bs is None and mon.get("mega"):
        notes["mega_as_base"].add(name)
        name = mon["species"]
        bs, types, source = metrics.mon_stats(hack, mon)
    if bs is None:
        if name not in blob["poks"]:
            notes["species"].add(name)
            return None
        rec = blob["poks"][name]
        bs, types, source = metrics._norm_stats(rec["bs"]), rec["types"], "oxide"
    weight = _weight(hack, name, blob)
    move_data, moves = {}, []
    for mv in metrics.default_moves(hack, mon):
        if mv == "Hidden Power":
            moves.append(mv)      # the engine works its type out from the IVs
            continue
        if mv.startswith("Hidden Power"):
            move_data[mv] = {"type": mv[len("Hidden Power"):].strip().title(),
                             "category": "Special", "basePower": HIDDEN_POWER_BP, "priority": 0}
            moves.append(mv)
            continue
        if mv in pool.UNRELIABLE:
            continue
        rec, _src = metrics.lookup_move(hack, mv)
        if rec is None:
            notes["moves"].add(mv)
            continue
        if not metrics.damaging(rec, mv) or rec["category"] not in ("Physical", "Special"):
            continue
        d = {"type": rec["type"], "category": rec["category"], "priority": rec["priority"] or 0}
        if rec["power"] and rec["power"] > 1:
            d["basePower"] = rec["power"]
        move_data[mv] = d
        moves.append(mv)
    return {
        "species": name, "level": mon["level"], "item": mon.get("item"),
        "ability": mon.get("ability"), "nature": mon.get("nature"),
        "ivs": _full(mon.get("ivs"), 31), "evs": _full(mon.get("evs"), 0),
        "species_data": dict({"bs": bs, "types": [t for t in (types or []) if t]},
                             **({"weightkg": weight} if weight else {})),
        "move_data": move_data, "moves": moves, "stats_from": source,
    }


def _category(hack, move):
    rec, _src = metrics.lookup_move(hack, move)
    return rec["category"] if rec else None


def score_ref_fight(hack, fight, blob, blob_path):
    """One reference fight's scores in Oxide's seat, or None if the hack has
    no fight there."""
    ps = parties(hack, fight)
    if not ps:
        return None
    split = fight["split"]
    side = pool.pool(split, blob)
    notes = {k: set() for k in ("species", "moves", "mega_as_base")}
    jobs = {"pokemon": {f"p{i}": p for i, p in enumerate(side)}, "pairs": []}
    bosses, sources = [], {}
    for v, party in enumerate(ps):
        for j, mon in enumerate(party):
            job = boss_mon(hack, mon, blob, notes)
            if job is None:
                continue
            key = f"b{v}.{j}"
            jobs["pokemon"][key] = job
            sources[job["stats_from"]] = sources.get(job["stats_from"], 0) + 1
            w = pressure.CALC_WEATHER.get(pressure.ABILITY_WEATHER.get(job["ability"]))
            bosses.append((v, key, dict(mon, species=job["species"]), w))
            for i, p in enumerate(side):
                jobs["pairs"].append([key, f"p{i}", job["moves"], w])
                jobs["pairs"].append([f"p{i}", key, p["moves"], w])
    if not bosses:
        return None
    t0 = time.time()
    out = pressure.run_node(blob_path, jobs)
    seconds = time.time() - t0
    rows = {(r["a"], r["d"]): r for r in out["results"]}
    errors = sorted({f"{r['a']} {m}: {v['error']}" for r in out["results"]
                     for m, v in r["moves"].items() if "error" in v})
    per_mon = pressure.score_mons(bosses, [f"p{i}" for i in range(len(side))], rows, out["pokemon"])
    return {
        "key": fight["key"], "label": fight["label"], "split": split, "hack": hack,
        "cap": pool.caps()[split], "pool": len(side),
        "trainers": [t["name"] for t in data.fight_trainers(hack, fight)],
        "ace": max(m["level"] for p in ps for m in p),
        **pressure.roll_up(per_mon), **pressure.unseen(ps),
        "predictable": pressure.predictability(ps, lambda mv: _category(hack, mv)),
        "mons": per_mon, "stats_from": sources,
        "left_out": {k: sorted(v) for k, v in notes.items() if v},
        "calcs": sum(len(r["moves"]) for r in out["results"]),
        "errors": errors, "node_seconds": round(out.get("seconds", 0), 2),
        "wall_seconds": round(seconds, 2),
    }


def load(hack):
    path = out_path(hack)
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    return {"_comment": __doc__.strip().split("\n\n")[0], "hack": hack,
            "title": data.REFS[hack]["title"], "rating": data.REFS[hack]["rating"],
            "fights": {}}


def save(hack, results):
    order = [f["key"] for f in data.fights()["fights"]]
    results["fights"] = {k: results["fights"][k] for k in order if k in results["fights"]}
    os.makedirs(OUT_DIR, exist_ok=True)
    with open(out_path(hack), "w", encoding="utf-8") as f:
        json.dump(results, f, indent=1)
        f.write("\n")


def _cell(r, lock=False):
    if not r:
        return f"{'':>11}"
    mark = "*" if r["choice_mons"] else " "
    ans = r["answers_lock"] if lock else r["answers"]
    return f"{r['threat']:>5.2f}/{ans:.2f}{mark}"


def report(hacks, out=sys.stdout, lock=False):
    """Threat/answers per fight, Oxide first, then each hack. A star marks a
    fight with a Choice holder; with lock, answers count the lock."""
    oxide = pressure.load()["fights"]
    refs = {h: load(h)["fights"] for h in hacks}
    head = f"{'fight':17}{'oxide':>12}" + "".join(f"{h[:10]:>12}" for h in hacks)
    print(head, file=out)
    for f in data.fights()["fights"]:
        k = f["key"]
        if not any(k in refs[h] for h in hacks):
            continue
        print(f"{f['label']:17} {_cell(oxide.get(k), lock)}"
              + "".join(" " + _cell(refs[h].get(k), lock) for h in hacks), file=out)


def report_hack(hack, out=sys.stdout):
    """One hack's fights, Pokemon by Pokemon, Choice holders marked."""
    for r in load(hack)["fights"].values():
        print(f"{r['label']} ({', '.join(r['trainers'])}; ace {r['ace']}, cap {r['cap']}): "
              f"threat {r['threat']:.2f}, answers {r['answers']:.2f}, "
              f"with the lock {r['answers_lock']:.2f}", file=out)
        for m in r["mons"]:
            lock = (f"  CHOICE, locks into {m['locked_move']}: answers {m['answers_lock']:.2f}"
                    if m["choice"] else "")
            print(f"    {m['species']:18}{m['level']:>4} {str(m['item']):16}"
                  f"{m['threat']:>6.2f}{m['answers']:>6.2f}{lock}", file=out)
        if r["left_out"]:
            print(f"    left out: {r['left_out']}", file=out)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--hack", action="append", default=[])
    ap.add_argument("--fight", action="append", default=[])
    ap.add_argument("--split", action="append", default=[])
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--lock", action="store_true", help="report answers counting the Choice lock")
    args = ap.parse_args(argv)
    if args.report:
        if len(args.hack) == 1:
            report_hack(args.hack[0])
        else:
            report(args.hack or [h for h in HACKS if os.path.exists(out_path(h))], lock=args.lock)
        return 0
    if len(args.hack) != 1:
        ap.error("name one --hack, so each run writes one file")
    hack = args.hack[0]
    wanted = [f for f in data.fights()["fights"]
              if f["key"] in args.fight or f["split"] in args.split]
    if not wanted:
        ap.error("name a --fight or a --split")
    results = load(hack)
    blob = calc_export.build()
    with tempfile.TemporaryDirectory(prefix="oxide-b3b-blob-") as tmp:
        blob_path = os.path.join(tmp, "blob.json")
        with open(blob_path, "w", encoding="utf-8") as f:
            json.dump(blob, f)
        for fight in wanted:
            r = score_ref_fight(hack, fight, blob, blob_path)
            if r is None:
                continue
            results["fights"][fight["key"]] = r
            save(hack, results)
            print(f"{hack} {r['label']}: threat {r['threat']:.2f}, answers {r['answers']:.2f} "
                  f"(lock {r['answers_lock']:.2f}), {r['calcs']} calculations, "
                  f"node {r['node_seconds']}s, wall {r['wall_seconds']}s, "
                  f"{len(r['errors'])} errors, left out {r['left_out'] or 'nothing'}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())

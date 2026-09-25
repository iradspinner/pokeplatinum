"""B3: pressure scores for each of Oxide's story fights.

    PYTHONPATH=. python3 -m tools.oxide.balance.pressure --fight roark
    PYTHONPATH=. python3 -m tools.oxide.balance.pressure --split Gardenia
    PYTHONPATH=. python3 -m tools.oxide.balance.pressure --report

Each boss Pokemon is set against the player's side at its fight's split
(pool.py), and the vendored calculator's own engine does the damage
(calc_headless.js, one Node process). For each boss Pokemon it reports:

- threat: the share of the player's side it knocks out in one or two hits
  while moving first;
- answers: the share of the player's side that does the same to it.

Rolled up per fight as the mean over its Pokemon; a rival fight is the mean
over its three starter variants, and a tag battle counts both opponents.

What a hit and a KO mean here. A move knocks out in n hits when n times its
middle roll (the ninth of sixteen, so at least half the rolls) reaches the
target's HP. A charging move (Solar Beam out of sun, Fly, Dig) spends two
turns a hit, and a recharging one (Hyper Beam) a turn after each hit but the
last, so "two hits" means two turns. Moving first is a positive priority
move, or equal priority and strictly more Speed (the engine's own final
Speed, so Choice Scarf and Swift Swim count); a Speed tie counts for neither
side. A boss holding a Focus Sash cannot be knocked out in one hit.

What this leaves out, and so reads as a ceiling for the boss: accuracy,
secondary effects, status and setup, switching, and the AI's real choice of
move (it assumes the boss's best move; element 6 documents how Platinum's AI
actually picks). Each boss Pokemon starts the fight in its map's battle
weather, or in its own ability's weather. Doubles are scored as singles.

The runs are staged and kept small, one split at a time, because this CPU
fails under load: every calculation is one process, run one after another.
Results go to pressure.json beside this file, one entry per fight.
"""
import argparse
import json
import os
import subprocess
import sys
import tempfile
import time

from ..encounters import calc_export
from . import data, pool, splits

HERE = os.path.dirname(os.path.abspath(__file__))
RUNNER = os.path.join(HERE, "calc_headless.js")
OUT = os.path.join(HERE, "pressure.json")

CHARGE = {"Solar Beam", "SolarBeam", "Solar Blade", "Sky Attack", "Skull Bash", "Razor Wind",
          "Fly", "Dig", "Dive", "Bounce", "Shadow Force", "Phantom Force", "Meteor Beam",
          "Freeze Shock", "Ice Burn", "Geomancy", "Electro Shot"}
SUN_SKIPS_CHARGE = {"Solar Beam", "SolarBeam", "Solar Blade"}
RECHARGE = {"Hyper Beam", "Giga Impact", "Blast Burn", "Frenzy Plant", "Hydro Cannon",
            "Rock Wrecker", "Roar of Time", "Eternabeam", "Prismatic Laser", "Meteor Assault"}
ABILITY_WEATHER = {"Drizzle": "Rain", "Drought": "Sun", "Sand Stream": "Sand",
                   "Snow Warning": "Hail"}
CALC_WEATHER = {"Rain": "Rain", "Sun": "Sun", "Sand": "Sand", "Hail": "Hail"}   # fog: none


def hits_to_ko(rolls, hp):
    """The fewest hits whose middle roll reaches hp, or None if it never does."""
    mid = rolls[len(rolls) // 2]
    if mid <= 0:
        return None
    return -(-hp // mid)


def turns(move, hits, weather):
    """Turns the hits take: two a hit for a charging move, one more between
    hits for a recharging one."""
    if move in CHARGE and not (move in SUN_SKIPS_CHARGE and weather == "Sun"):
        return 2 * hits
    if move in RECHARGE:
        return 2 * hits - 1
    return hits


def wins(row, def_info, speeds, weather, sash=False):
    """True when some move of the attacker's knocks the defender out within
    two turns while moving first. `speeds` is (attacker, defender)."""
    for move, r in row["moves"].items():
        if "error" in r:
            continue
        n = hits_to_ko(r["rolls"], def_info["hp"])
        if n is None:
            continue
        if sash and n == 1:
            n = 2
        if turns(move, n, weather) > 2:
            continue
        pr = r["priority"]
        if pr > 0 or (pr == 0 and speeds[0] > speeds[1]):
            return True
    return False


def boss_parties(fight):
    """[[boss Pokemon]] per variant: a rival's three starters are three
    variants, a tag battle's two opponents one party."""
    trainers = data.fight_trainers("oxide", fight)
    if fight.get("tag"):
        return [[m for t in trainers for m in t["party"]]], [t["tr_id"] for t in trainers]
    return [t["party"] for t in trainers], [t["tr_id"] for t in trainers]


def fight_weather(tr_ids):
    for tr in tr_ids:
        for w in splits.trainer_weather(tr):
            if w in CALC_WEATHER:
                return CALC_WEATHER[w]
    return None


def boss_moves(mon, blob):
    return [m for m in mon["moves"]
            if m in blob["moves"] and blob["moves"][m].get("category") != "Status"
            and m not in pool.UNRELIABLE]


def run_node(blob_path, jobs):
    """One Node process, waited on, so nothing else runs beside it."""
    with tempfile.TemporaryDirectory(prefix="oxide-b3-") as tmp:
        jobs_path, out_path = os.path.join(tmp, "jobs.json"), os.path.join(tmp, "out.json")
        with open(jobs_path, "w", encoding="utf-8") as f:
            json.dump(jobs, f)
        subprocess.run(["node", RUNNER, blob_path, jobs_path, out_path], check=True)
        with open(out_path, encoding="utf-8") as f:
            return json.load(f)


def score_fight(fight, blob, blob_path):
    """One fight's scores, and how many calculations it took."""
    split = fight["split"]
    side = pool.pool(split, blob)
    parties, tr_ids = boss_parties(fight)
    weather = fight_weather(tr_ids)
    jobs = {"pokemon": {}, "pairs": []}
    for i, p in enumerate(side):
        jobs["pokemon"][f"p{i}"] = p
    bosses = []
    for v, party in enumerate(parties):
        for j, mon in enumerate(party):
            key = f"b{v}.{j}"
            jobs["pokemon"][key] = mon
            w = CALC_WEATHER.get(ABILITY_WEATHER.get(mon.get("ability")), weather)
            bosses.append((v, key, mon, w))
            for i, p in enumerate(side):
                jobs["pairs"].append([key, f"p{i}", boss_moves(mon, blob), w])
                jobs["pairs"].append([f"p{i}", key, p["moves"], w])
    t0 = time.time()
    out = run_node(blob_path, jobs)
    seconds = time.time() - t0
    rows = {(r["a"], r["d"]): r for r in out["results"]}
    info = out["pokemon"]
    errors = sorted({f"{r['a']} {m}: {v['error']}" for r in out["results"]
                     for m, v in r["moves"].items() if "error" in v})
    per_mon = []
    for v, key, mon, w in bosses:
        threat = answer = 0
        for i in range(len(side)):
            pk = f"p{i}"
            down = rows[(key, pk)]
            up = rows[(pk, key)]
            if wins(down, info[pk], down["speeds"], w):
                threat += 1
            if wins(up, info[key], up["speeds"], w, sash=mon.get("item") == "Focus Sash"):
                answer += 1
        per_mon.append({"variant": v, "species": mon["species"], "level": mon["level"],
                        "item": mon.get("item"), "weather": w,
                        "threat": round(threat / len(side), 3),
                        "answers": round(answer / len(side), 3)})
    by_variant = {}
    for m in per_mon:
        by_variant.setdefault(m["variant"], []).append(m)

    def mean(k):
        return round(sum(sum(m[k] for m in ms) / len(ms) for ms in by_variant.values())
                     / len(by_variant), 3)

    return {
        "key": fight["key"], "label": fight["label"], "split": split,
        "cap": pool.caps()[split], "pool": len(side), "weather": weather,
        "threat": mean("threat"), "answers": mean("answers"),
        "max_threat": max(m["threat"] for m in per_mon),
        "min_answers": min(m["answers"] for m in per_mon),
        "mons": per_mon, "calcs": sum(len(r["moves"]) for r in out["results"]),
        "errors": errors, "node_seconds": round(out.get("seconds", 0), 2),
        "wall_seconds": round(seconds, 2),
    }


def load():
    if os.path.exists(OUT):
        with open(OUT, encoding="utf-8") as f:
            return json.load(f)
    return {"_comment": __doc__.strip().split("\n\n")[0], "fights": {}}


def save(results):
    order = [f["key"] for f in data.fights()["fights"]]
    results["fights"] = {k: results["fights"][k] for k in order if k in results["fights"]}
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=1)
        f.write("\n")


def report(results, out=sys.stdout):
    print(f"{'fight':18}{'split':10}{'cap':>4}{'pool':>6}{'threat':>8}{'answers':>9}"
          f"{'worst mon':>11}{'fewest':>8}", file=out)
    for r in results["fights"].values():
        print(f"{r['label']:18}{r['split']:10}{r['cap']:>4}{r['pool']:>6}{r['threat']:>8.2f}"
              f"{r['answers']:>9.2f}{r['max_threat']:>11.2f}{r['min_answers']:>8.2f}", file=out)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--fight", action="append", default=[])
    ap.add_argument("--split", action="append", default=[])
    ap.add_argument("--report", action="store_true")
    args = ap.parse_args(argv)
    results = load()
    if args.report:
        report(results)
        return 0
    wanted = [f for f in data.fights()["fights"]
              if f["key"] in args.fight or f["split"] in args.split]
    if not wanted:
        ap.error("name a --fight or a --split")
    blob = calc_export.build()
    with tempfile.TemporaryDirectory(prefix="oxide-b3-blob-") as tmp:
        blob_path = os.path.join(tmp, "blob.json")
        with open(blob_path, "w", encoding="utf-8") as f:
            json.dump(blob, f)
        for fight in wanted:
            r = score_fight(fight, blob, blob_path)
            results["fights"][fight["key"]] = r
            save(results)
            print(f"{r['label']}: threat {r['threat']:.2f}, answers {r['answers']:.2f}, "
                  f"{r['calcs']} calculations, node {r['node_seconds']}s, "
                  f"wall {r['wall_seconds']}s, {len(r['errors'])} errors", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())

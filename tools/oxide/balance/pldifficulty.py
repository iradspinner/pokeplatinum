"""The fight difficulty store (difficulty.json beside this file): the
scorer's readings of each fight, which the OxiDex Trainers tab shows as one
number, Ian's formula of 2026-10-07 applied to the three stored ones.

A key is a trainer constant, or a story fight's key (fights.json) where the
fight has several constants: a rival's starter teams, Lucas and Dawn. Each
key holds a list of readings, one per team read: "oxide" (the trainer's own
file), "study" (the Kaizo study's rewrite) or "kaizo" (Kaizo's own team on
Oxide's box). "sections" holds gauntlet sections read as a whole, each
naming its trainers. Goal 3 writes its readings through put().
"""
import datetime
import json
import os

from . import data

PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "difficulty.json")
TEAMS = ("oxide", "study", "kaizo")
FIELDS = ("label", "team", "source", "trainer", "won", "clean", "faints", "fights", "unlucky", "date", "stale")
LOSS_WEIGHT = 40          # Ian, 2026-10-07: a losing rate of one in ten weighs as four Pokemon lost


def load(path=PATH):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def difficulty(reading):
    """Average faints plus 40 times the losing rate, at real odds."""
    return reading["faints"] + LOSS_WEIGHT * (1 - reading["won"])


def put(key, reading, path=PATH):
    """Records a reading under key, replacing the one of the same team and
    trainer; the store keeps its order (oxide, study, kaizo)."""
    store = load(path)
    readings = [r for r in store["fights"].get(key, [])
                if (r["team"], r["trainer"]) != (reading["team"], reading["trainer"])]
    readings.append({f: reading.get(f) for f in FIELDS})
    store["fights"][key] = sorted(readings, key=lambda r: TEAMS.index(r["team"]))
    store["fights"] = dict(sorted(store["fights"].items()))
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(store, fh, indent=1)
        fh.write("\n")


def problems(store):
    """Everything wrong with a store's shape: an unknown key or trainer, a
    missing field, a number out of range, a bad date or team."""
    constants = {t["constant"] for t in data.oxide_trainers().values()}
    multi = {f["key"]: set(f["trainers"]) for f in data.fights()["fights"] if len(f["trainers"]) > 1}
    out = []

    def check(where, r, allowed):
        missing = [f for f in FIELDS if f not in r]
        if missing:
            out.append(f"{where}: missing {missing}")
            return
        if r["team"] not in TEAMS:
            out.append(f"{where}: team {r['team']!r}")
        if r["trainer"] is not None and r["trainer"] not in allowed:
            out.append(f"{where}: trainer {r['trainer']} is not this key's")
        if r["team"] != "kaizo" and r["trainer"] is None and where.split(" ")[0] != "section":
            out.append(f"{where}: an Oxide or study reading names its trainer")
        for side in (r, r["unlucky"]):
            if not (0 <= side["won"] <= 1 and 0 <= side["clean"] <= side["won"] and 0 <= side["faints"] <= 6
                    and isinstance(side["fights"], int) and side["fights"] > 0):
                out.append(f"{where}: numbers out of range {side}")
        try:
            datetime.date.fromisoformat(r["date"])
        except (TypeError, ValueError):
            out.append(f"{where}: date {r['date']!r}")
        if r["stale"] is not None and not (isinstance(r["stale"], str) and r["stale"]):
            out.append(f"{where}: stale {r['stale']!r}")

    for key, readings in store["fights"].items():
        if key in constants:
            allowed = {key}
        elif key in multi:
            allowed = multi[key]
        else:
            out.append(f"{key}: neither a trainer constant nor a story fight with several")
            continue
        if not readings:
            out.append(f"{key}: no readings")
        for i, r in enumerate(readings):
            check(f"{key} #{i}", r, allowed)
    for name, sec in store.get("sections", {}).items():
        bad = [t for t in sec["trainers"] if t not in constants]
        if bad:
            out.append(f"section {name}: unknown trainers {bad}")
        for i, r in enumerate(sec["readings"]):
            check(f"section {name} #{i}", r, set(sec["trainers"]))
    return out

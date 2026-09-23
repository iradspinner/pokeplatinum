"""B1 acceptance, first part: the reference data and the story fights.

    PYTHONPATH=. python3 -m tools.oxide.balance.test_b1

Reads the pinned reference files in ~/roms/balance-refs and res/trainers/.
Writes nothing.
"""
import glob
import hashlib
import json
import os
import re
import sys

from . import data

# Sets per file, counted by hand from the raw JSON on 2026-09-22. A loader
# that drops or duplicates members fails here before anything is scored.
SET_COUNTS = {"vanilla": 1873, "renegade": 2823, "redux": 2829, "redux_hc": 2829,
              "kaizo": 3077, "hardlove": 1871, "null": 2282, "unbound": 357}
# Words a trainer's name must contain for a fight to count as found. The
# calculator's data calls the rival "Pkmn Trainer Cedric".
NAME_WORD = {"barry": "Cedric", "mars": "Mars", "jupiter": "Jupiter",
             "saturn": "Saturn", "cyrus": "Cyrus"}
PLATINUM_HACKS = [h for h in data.REFS if data.REFS[h]["game"] == "platinum"]


def check_pinned_files(results):
    """Every reference file is the copy MANIFEST.txt pinned. A changed file
    would silently change every score calibrated on it."""
    with open(os.path.join(data.REFS_DIR, "MANIFEST.txt"), encoding="utf-8") as f:
        pinned = dict(reversed(line.split(None, 1)) for line in f
                      if line.strip() and not line.startswith("#"))
    bad = []
    for name, digest in pinned.items():
        with open(os.path.join(data.REFS_DIR, name.strip()), "rb") as f:
            if hashlib.sha256(f.read()).hexdigest() != digest:
                bad.append(name.strip())
    results.append(("every pinned reference file matches its SHA-256", not bad,
                    f"{len(pinned)} files" + (f", changed: {bad}" if bad else "")))


def check_set_counts(results):
    """The loader keeps every set each file holds, no more and no fewer."""
    for hack, want in SET_COUNTS.items():
        raw = sum(len(v) for v in data.raw(hack)["formatted_sets"].values())
        loaded = sum(len(t["party"]) for t in data.ref_trainers(hack).values())
        results.append((f"{hack}: every set is read once", raw == want == loaded,
                        f"{raw} in the file, {loaded} loaded, {want} expected"))


def check_oxide_members(results):
    """Oxide is read per trainer, so every party member of every real
    trainer arrives, duplicates of a species included."""
    want = 0
    for path in glob.glob(os.path.join(data.ROOT, "res", "trainers", "data", "*.json")):
        if not os.path.basename(path).startswith("dummy_"):
            with open(path, encoding="utf-8") as f:
                want += len(json.load(f)["party"])
    got = sum(len(t["party"]) for t in data.oxide_trainers().values())
    results.append(("oxide: every party member of every real trainer is read",
                    got == want, f"{got} of {want}"))


def _word(fight):
    return NAME_WORD.get(fight["key"].split("_")[0], fight["label"].split()[0])


def check_fights_resolve(results):
    """Each story fight finds its trainers in Oxide and in every hack that
    keeps Platinum's ids, under a name that says who they are."""
    for hack in ["oxide"] + PLATINUM_HACKS:
        word_ok = lambda f, n: (_word(f) in n or (hack == "oxide" and _word(f) == "Cedric"
                                                  and "Barry" in n)
                                or (f["key"] == "mars_jupiter" and ("Mars" in n or "Jupiter" in n)))
        missing = []
        for fight in data.fights()["fights"]:
            ts = data.fight_trainers(hack, fight)
            if not ts or not all(word_ok(fight, t["name"]) for t in ts):
                missing.append(fight["key"])
        results.append((f"{hack}: all {len(data.fights()['fights'])} story fights resolve",
                        not missing, f"unresolved: {missing}" if missing else ""))


def check_sheet_levels(results):
    """Oxide's aces match Ian's Level Caps sheet, apart from the fights
    whose note says why not."""
    off = []
    for fight in data.fights()["fights"]:
        if fight["sheet_ace"] is None or "note" in fight:
            continue
        ace = max(m["level"] for t in data.fight_trainers("oxide", fight) for m in t["party"])
        if ace != fight["sheet_ace"]:
            off.append(f"{fight['key']} {ace} vs {fight['sheet_ace']}")
    results.append(("oxide's boss aces match the Level Caps sheet", not off, "; ".join(off)))


def check_league_after_volkner(results):
    """No hack's League is weaker than its last gym. This is the check that
    caught Kaizo and Redux keeping vanilla's League in Platinum's slots."""
    by_key = {f["key"]: f for f in data.fights()["fights"]}
    for hack in ["oxide"] + PLATINUM_HACKS:
        ace = lambda k: max(m["level"] for t in data.fight_trainers(hack, by_key[k])
                            for m in t["party"])
        low = [k for k in ("aaron", "bertha", "flint", "lucian", "cynthia")
               if ace(k) < ace("volkner")]
        results.append((f"{hack}: the League is at or above Volkner", not low,
                        f"Volkner {ace('volkner')}" + (f", below it: {low}" if low else "")))


def check_roark(results):
    """Roark's party sizes, as read by hand from each file."""
    roark = next(f for f in data.fights()["fights"] if f["key"] == "roark")
    got = {h: len(data.fight_trainers(h, roark)[0]["party"])
           for h in ("oxide", "vanilla", "renegade", "kaizo")}
    want = {"oxide": 4, "vanilla": 3, "renegade": 6, "kaizo": 6}
    results.append(("Roark's party sizes", got == want, str(got)))


def main():
    results = []
    for check in (check_pinned_files, check_set_counts, check_oxide_members,
                  check_fights_resolve, check_sheet_levels,
                  check_league_after_volkner, check_roark):
        check(results)
    width = max(len(label) for label, _, _ in results)
    failed = 0
    for label, ok, note in results:
        failed += not ok
        print(f"  {'ok  ' if ok else 'FAIL'}  {label:{width}}  {note}")
    print(f"\n{len(results) - failed}/{len(results)} passed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())

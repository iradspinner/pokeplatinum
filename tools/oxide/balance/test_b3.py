"""B3 acceptance: the player's side and the pressure scores.

    PYTHONPATH=. python3 -m tools.oxide.balance.test_b3

Runs one Node process for a handful of matchups and reads pressure.json;
it does not rerun the fights (pressure.py does that, a split at a time).
The plan's check is that damage agrees with the calculator's page and with
Ian's in-game roll; the second waits on Ian (encounter build plan, M8).
"""
import json
import os
import sys
import tempfile

from ..encounters import calc_export
from . import data, metrics, pool, pressure

# The five matchups D5 checked on the calculator (level 50, every IV 31, no
# EVs, a neutral nature), and the range it showed for each. Crunch into
# Bronzor comes out 42 to 50 only on this fork's chart, where Steel still
# resists Dark; a Generation 6 chart would double it.
D5 = [("Garchomp", "Clefairy", "Earthquake", (126, 148)),
      ("Garchomp", "Clefairy", "Dragon Claw", (0, 0)),
      ("Machamp", "Bronzor", "Crunch", (42, 50)),
      ("Machamp", "Bronzor", "Cross Chop", (81, 96)),
      ("Machamp", "Clefairy", "Cross Chop", (63, 74))]
# Ian's caps: the Level Caps sheet, with HQ 60, Galactic 65 and Volkner 68
# from his Battle Zone rulings of 2026-09-25.
CAPS = {"Roark": 16, "Gardenia": 26, "Fantina": 33, "Maylene": 39, "Wake": 44,
        "Byron": 53, "Candice": 56, "HQ": 60, "Galactic": 65, "Volkner": 68, "League": 78}
# Moves the calculator's Generation 4 mechanics give no number for (they are
# handled only in its later-generation code); each is reported, not scored.
UNMODELLED = {"Electro Ball", "Heavy Slam", "Psywave", "Super Fang", "Trump Card"}


def _run(blob, jobs):
    with tempfile.TemporaryDirectory(prefix="oxide-b3-test-") as tmp:
        path = os.path.join(tmp, "blob.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(blob, f)
        return pressure.run_node(path, jobs)


def check_damage(results, blob):
    """The headless engine gives D5's numbers, and Hidden Power follows the IVs."""
    iv = {k: 31 for k in ("hp", "at", "df", "sa", "sd", "sp")}
    ev = {k: 0 for k in iv}
    names = sorted({a for a, _, _, _ in D5} | {d for _, d, _, _ in D5})
    jobs = {"pokemon": {n: {"species": n, "level": 50, "nature": "Hardy", "ivs": iv, "evs": ev}
                        for n in names},
            "pairs": [[a, d, [m], None] for a, d, m, _ in D5]}
    jobs["pokemon"]["low"] = dict(jobs["pokemon"]["Machamp"], ivs={k: 30 for k in iv})
    jobs["pokemon"]["Gengar"] = dict(jobs["pokemon"]["Machamp"], species="Gengar")
    jobs["pairs"].append(["Machamp", "Gengar", ["Hidden Power"], None])
    jobs["pairs"].append(["low", "Gengar", ["Hidden Power"], None])
    out = _run(blob, jobs)
    got = [(r["a"], r["d"], m, (v["rolls"][0], v["rolls"][-1]))
           for r in out["results"][:len(D5)] for m, v in r["moves"].items()]
    want = [(a, d, m, rng) for a, d, m, rng in D5]
    results.append(("the headless engine gives D5's five ranges", got == want,
                    "; ".join(f"{m} into {d} {lo}-{hi}" for _a, d, m, (lo, hi) in got)))
    # Every IV 31 makes a Dark Hidden Power, which hits Gengar hard; every
    # IV 30 a Fighting one, which cannot touch a Ghost.
    dark = out["results"][len(D5)]["moves"]["Hidden Power"]["rolls"]
    fighting = out["results"][len(D5) + 1]["moves"]["Hidden Power"]["rolls"]
    results.append(("Hidden Power takes its type from the IVs",
                    dark[0] > 0 and fighting[-1] == 0,
                    f"IVs 31 into Gengar {dark[0]}-{dark[-1]}, IVs 30 {fighting[0]}-{fighting[-1]}"))


def check_ref_overrides(results, blob):
    """B3b's reference Pokemon bring their own game's species and move data.
    Oxide's own data passed that way changes nothing; a move the engine has
    never heard of, given Earthquake's data, hits exactly as Earthquake does;
    twice the power does more; and a Clefairy given the Flying type takes
    nothing from it."""
    iv = {k: 31 for k in ("hp", "at", "df", "sa", "sd", "sp")}
    ev = {k: 0 for k in iv}
    base = {"level": 50, "nature": "Hardy", "ivs": iv, "evs": ev}
    chomp, clef = blob["poks"]["Garchomp"], blob["poks"]["Clefairy"]
    own = {"bs": metrics._norm_stats(chomp["bs"]), "types": chomp["types"]}
    quake = {"type": "Ground", "category": "Physical", "basePower": 100, "priority": 0}
    jobs = {"pokemon": {
        "chomp": dict(base, species="Garchomp"),
        "own": dict(base, species="Garchomp", species_data=own,
                    move_data={"Test Quake": quake, "Earthquake": dict(quake, basePower=200)}),
        "clef": dict(base, species="Clefairy"),
        "bird": dict(base, species="Clefairy",
                     species_data={"bs": metrics._norm_stats(clef["bs"]), "types": ["Flying"]}),
    }, "pairs": [["chomp", "clef", ["Earthquake"], None],
                 ["own", "clef", ["Test Quake", "Earthquake"], None],
                 ["chomp", "bird", ["Earthquake"], None]]}
    out = _run(blob, jobs)
    plain, own_row, bird = (r["moves"] for r in out["results"])
    ok = (own_row["Test Quake"]["rolls"] == plain["Earthquake"]["rolls"]
          and own_row["Earthquake"]["rolls"][0] > plain["Earthquake"]["rolls"][-1]
          and bird["Earthquake"]["rolls"][-1] == 0)
    results.append(("a reference Pokemon's own species and move data are used", ok,
                    f"Earthquake {plain['Earthquake']['rolls'][0]}-{plain['Earthquake']['rolls'][-1]}, "
                    f"at 200 power {own_row['Earthquake']['rolls'][0]}, "
                    f"into a Flying Clefairy {bird['Earthquake']['rolls'][-1]}"))


def check_engine(results):
    """The engine is the page's: the same files, in the page's order."""
    import subprocess
    listing = subprocess.run(
        ["node", "-e", "console.log(JSON.stringify(require(process.argv[1]).engineFiles()))",
         os.path.join(os.path.dirname(os.path.abspath(__file__)), "calc_headless.js")],
        check=True, capture_output=True, text=True).stdout
    files = json.loads(listing)
    ok = (files[0] == "calc/util.js" and files[-1] == "calc/index.js"
          and files.count("calc/data/evos.js") == 2 and "calc/mechanics/gen4.js" in files)
    results.append(("the engine files are the page's, in its order", ok, f"{len(files)} files"))


def check_pool(results, blob):
    """The player's side grows split by split, at each split's cap."""
    # The caps are Ian's, and no closing boss may sit above its split's cap.
    # Galactic's (Cyrus 3) and Volkner's aces are below theirs until the
    # trainer pass raises them.
    aces = pool.closing_aces()
    over = {s: aces[s] for s in CAPS if aces[s] > CAPS[s]}
    ok_caps = pool.caps() == CAPS and not over
    results.append(("the caps are Ian's, and no closing boss is above its cap", ok_caps,
                    f"closing aces {aces}" + (f"; over: {over}" if over else "")))
    sizes, grows, bad = {}, True, []
    before = set()
    for split in pool.SPLITS:
        side = pool.pool(split, blob)
        names = {m["species"] for m in side}
        grows &= before <= names
        before = names
        sizes[split] = len(side)
        for m in side:
            if m["level"] != CAPS[split]:
                bad.append(f"{m['species']} at {m['level']}")
            for mv in m["moves"]:
                rec = blob["moves"][mv]
                if rec.get("category") == "Status" or mv in pool.CONDITIONAL:
                    bad.append(f"{m['species']} {mv}")
    results.append(("no species leaves the side, and every one is at the cap with "
                    "damaging moves only", grows and not bad,
                    ", ".join(f"{s} {n}" for s, n in sizes.items()) if not bad else str(bad[:5])))
    roark = {m["species"] for m in pool.pool("Roark", blob)}
    starters = {"Turtwig", "Piplup", "Scorbunny"}
    results.append(("the three starters are in Roark's split", starters <= roark,
                    str(sorted(starters - roark))))


def check_rules(results):
    """A hit count, a charging turn and a Focus Sash, by hand."""
    rolls = sorted(range(85, 101))
    row = {"moves": {"Tackle": {"rolls": rolls, "priority": 0},
                     "Fly": {"rolls": [200] * 16, "priority": 0}}}
    cases = [
        pressure.hits_to_ko(rolls, 186) == 2,                    # middle roll 93, 2 x 93 = 186
        pressure.hits_to_ko(rolls, 187) == 3,
        pressure.hits_to_ko([0] * 16, 10) is None,
        pressure.turns("Fly", 1, None) == 2 and pressure.turns("Solar Beam", 1, "Sun") == 1,
        pressure.turns("Hyper Beam", 2, None) == 3,
        pressure.wins(row, {"hp": 150}, (60, 50), None),         # Fly, one hit, two turns
        not pressure.wins(row, {"hp": 150}, (50, 50), None),     # a Speed tie counts for no one
        not pressure.wins({"moves": {"Tackle": {"rolls": [100] * 16, "priority": 0}}},
                          {"hp": 250}, (60, 50), None),          # three hits is too many
        pressure.wins({"moves": {"Tackle": {"rolls": [100] * 16, "priority": 0}}},
                      {"hp": 150}, (60, 50), None, sash=True),   # sash: 1 hit becomes 2
    ]
    results.append(("hits, charging turns, Speed ties and Focus Sash", all(cases),
                    str([i for i, c in enumerate(cases) if not c])))


def check_scores(results, blob):
    """Every story fight is scored, against the side as it is now."""
    saved = pressure.load()["fights"]
    keys = [f["key"] for f in data.fights()["fights"]]
    missing = [k for k in keys if k not in saved]
    sizes = {s: len(pool.pool(s, blob)) for s in pool.SPLITS}
    stale = [k for k in keys if k in saved and (saved[k]["cap"] != CAPS[saved[k]["split"]]
                                                 or saved[k]["pool"] != sizes[saved[k]["split"]])]
    boss_errors = [k for k in keys if k in saved
                   and any(e.startswith("b") for e in saved[k]["errors"])]
    unknown = {e.split(" ", 1)[1].split(":")[0] for k in keys if k in saved
               for e in saved[k]["errors"]} - UNMODELLED
    ok = not missing and not stale and not boss_errors and not unknown
    results.append(("all 28 fights scored; no boss move fails, and the player's failures "
                    "are the five unmodelled moves", ok,
                    f"missing {missing}, stale {stale}, boss errors {boss_errors}, "
                    f"other failures {sorted(unknown)}" if not ok else
                    f"{len(keys)} fights, pools {min(sizes.values())} to {max(sizes.values())}"))


def main():
    results = []
    blob = calc_export.build()
    check_engine(results)
    check_damage(results, blob)
    check_ref_overrides(results, blob)
    check_pool(results, blob)
    check_rules(results)
    check_scores(results, blob)
    width = max(len(label) for label, _, _ in results)
    failed = 0
    for label, ok, note in results:
        failed += not ok
        print(f"  {'ok  ' if ok else 'FAIL'}  {label:{width}}  {note}")
    print(f"\n{len(results) - failed}/{len(results)} passed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())

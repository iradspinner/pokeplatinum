"""The calculator runner, the player's side and the census's flag numbers.

    PYTHONPATH=. python3 -m tools.oxide.balance.test_b3

Runs one Node process for a handful of matchups through the runner every
fight reading uses (calc.py). The plan's check is that damage agrees with
the calculator's page and with Ian's in-game roll; the second waits on Ian
(encounter build plan, M8). The first scoring system's own rules and stored
scores, which this file also checked, were retired with it on 2026-10-13.
"""
import json
import os
import sys
import tempfile

from ..encounters import calc_export
from . import calc, pool, splits

# The calculator's six base stat keys.
STATS = ("hp", "at", "df", "sa", "sd", "sp")

# The five matchups D5 checked on the calculator (level 50, every IV 31, no
# EVs, a neutral nature), and the range it shows for each since the encounter
# track's Oxide profile applies a dual type's two factors in the game's order
# (Crunch into Bronzor 43 to 51, as Ian's in-game roll gave, where it was 42
# to 50). Crunch into Bronzor comes out that low only on this fork's chart,
# where Steel still resists Dark; a Generation 6 chart would double it.
D5 = [("Garchomp", "Clefairy", "Earthquake", (126, 148)),
      ("Garchomp", "Clefairy", "Dragon Claw", (0, 0)),
      ("Machamp", "Bronzor", "Crunch", (43, 51)),
      ("Machamp", "Bronzor", "Cross Chop", (80, 96)),
      ("Machamp", "Clefairy", "Cross Chop", (63, 74))]
# Ian's caps: the Level Caps sheet, with HQ 60, Galactic 65 and Volkner 68
# from his Battle Zone rulings of 2026-09-25.
CAPS = {"Roark": 16, "Gardenia": 26, "Fantina": 33, "Maylene": 39, "Wake": 44,
        "Byron": 53, "Candice": 56, "HQ": 60, "Galactic": 65, "Volkner": 68, "Barry": 71, "League": 78}


def _run(blob, jobs):
    with tempfile.TemporaryDirectory(prefix="oxide-b3-test-") as tmp:
        path = os.path.join(tmp, "blob.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(blob, f)
        return calc.run_node(path, jobs)


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


def check_eviolite(results, blob):
    """The Eviolite works by the engine's rule, on any species that can still
    evolve: an old one (Lileep), one added after Generation 4 (Naclstack),
    and not on a final stage (Garganacl)."""
    iv = {k: 31 for k in ("hp", "at", "df", "sa", "sd", "sp")}
    ev = {k: 0 for k in iv}
    mon = lambda sp, item=None: {"species": sp, "level": 50, "nature": "Hardy", "ivs": iv, "evs": ev, "item": item}
    defenders = ("Lileep", "Naclstack", "Garganacl")
    pk = {"att": mon("Barboach")}
    for sp in defenders:
        pk[sp + "+"] = mon(sp, "Eviolite")
        pk[sp] = mon(sp)
    out = _run(blob, {"pokemon": pk, "pairs": [["att", d, ["Mud Bomb", "Tackle"], None] for d in pk if d != "att"]})
    top = {r["d"]: {m: v["rolls"][-1] for m, v in r["moves"].items()} for r in out["results"]}
    ok = all(top[sp + "+"][m] < top[sp][m] for sp in ("Lileep", "Naclstack") for m in ("Mud Bomb", "Tackle")) \
        and top["Garganacl+"] == top["Garganacl"]
    results.append(("the Eviolite cuts damage to a species that can still evolve, of any generation", ok,
                    "; ".join(f"{sp} {top[sp + '+']} with, {top[sp]} without" for sp in defenders)))


def check_ref_overrides(results, blob):
    """A Pokemon may bring its own species and move data (the runner's
    species_data and move_data; the simulator passes Magnitude's rolled
    powers this way). Oxide's own data passed that way changes nothing; a move the engine has
    never heard of, given Earthquake's data, hits exactly as Earthquake does;
    twice the power does more; and a Clefairy given the Flying type takes
    nothing from it."""
    iv = {k: 31 for k in ("hp", "at", "df", "sa", "sd", "sp")}
    ev = {k: 0 for k in iv}
    base = {"level": 50, "nature": "Hardy", "ivs": iv, "evs": ev}
    chomp, clef = blob["poks"]["Garchomp"], blob["poks"]["Clefairy"]
    own = {"bs": {k: chomp["bs"][k] for k in STATS}, "types": chomp["types"]}
    quake = {"type": "Ground", "category": "Physical", "basePower": 100, "priority": 0}
    jobs = {"pokemon": {
        "chomp": dict(base, species="Garchomp"),
        "own": dict(base, species="Garchomp", species_data=own,
                    move_data={"Test Quake": quake, "Earthquake": dict(quake, basePower=200)}),
        "clef": dict(base, species="Clefairy"),
        "bird": dict(base, species="Clefairy",
                     species_data={"bs": {k: clef["bs"][k] for k in STATS}, "types": ["Flying"]}),
    }, "pairs": [["chomp", "clef", ["Earthquake"], None],
                 ["own", "clef", ["Test Quake", "Earthquake"], None],
                 ["chomp", "bird", ["Earthquake"], None]]}
    out = _run(blob, jobs)
    plain, own_row, bird = (r["moves"] for r in out["results"])
    ok = (own_row["Test Quake"]["rolls"] == plain["Earthquake"]["rolls"]
          and own_row["Earthquake"]["rolls"][0] > plain["Earthquake"]["rolls"][-1]
          and bird["Earthquake"]["rolls"][-1] == 0)
    results.append(("a Pokemon's own species and move data are used", ok,
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
    # The stone plan: the Leaf Stone is in Floaroma Meadow (Gardenia's split),
    # the Thunder Stone first in the Solaceon Ruins (Maylene's); a stone
    # evolution joins the side where its stone does, not at a judged level.
    have = pool.species_by_split()
    cases = [("SPECIES_SHIFTRY", "Gardenia", True), ("SPECIES_RAICHU", "Fantina", False),
             ("SPECIES_RAICHU", "Maylene", True)]
    wrong = [f"{sp} {'missing from' if want else 'already in'} {s}"
             for sp, s, want in cases if (sp in have[s]) != want]
    results.append(("stone evolutions join the side where their stone is first in reach",
                    not wrong, ", ".join(wrong)))
    # The encounter tool's scripted sources the sources file places nowhere:
    # the fossils in Fantina's split, and Acuity Cavern's draw in Volkner's.
    cases = [("SPECIES_CRANIDOS", "Gardenia", False), ("SPECIES_CRANIDOS", "Fantina", True),
             ("SPECIES_LILEEP", "Fantina", True), ("SPECIES_CRESSELIA", "Galactic", False),
             ("SPECIES_CRESSELIA", "Volkner", True), ("SPECIES_PHEROMOSA", "Volkner", True)]
    wrong = [f"{sp} {'missing from' if want else 'already in'} {s}"
             for sp, s, want in cases if (sp in have[s]) != want]
    results.append(("the fossils and the Acuity Cavern draw join where the encounter tool has them",
                    not wrong, ", ".join(wrong)))


def check_flag_numbers(results):
    """The split map numbers the tree's own flag list rather than reading a
    shared build header: every hidden item's flag has a number of its own,
    inside HIDDEN_ITEM_FLAGS_START to HIDDEN_ITEM_FLAGS_END."""
    flags = splits.flag_values()
    start, end = flags["HIDDEN_ITEM_FLAGS_START"], flags["HIDDEN_ITEM_FLAGS_END"]
    used = [flag for _item, flag in
            splits._HIDDEN.findall(splits._read("include", "data", "field", "hidden_items.h"))]
    missing = [flag for flag in used if flag not in flags]
    values = [flags[flag] for flag in used if flag in flags]
    ok = (not missing and len(set(values)) == len(values)
          and all(start <= v <= end for v in values))
    results.append(("hidden-item flags numbered from the tree's own list", ok,
                    f"{len(values)} flags in {start} to {end}" if ok
                    else f"missing {missing[:3]}, {len(values) - len(set(values))} shared"))


def main():
    results = []
    blob = calc_export.build()
    check_engine(results)
    check_damage(results, blob)
    check_eviolite(results, blob)
    check_ref_overrides(results, blob)
    check_pool(results, blob)
    check_flag_numbers(results)
    width = max(len(label) for label, _, _ in results)
    failed = 0
    for label, ok, note in results:
        failed += not ok
        print(f"  {'ok  ' if ok else 'FAIL'}  {label:{width}}  {note}")
    print(f"\n{len(results) - failed}/{len(results)} passed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())

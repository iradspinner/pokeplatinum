"""The box simulator keeps Ian's rules (simulate.py).

    PYTHONPATH=. python3 -m tools.oxide.encounters.test_sim

Read-only. Plays a handful of seeded runs and checks each against the rules
the simulator promises: one capture per area, the dupes clause over
families, one repel before Gardenia's split, the deaths asked for, nothing
from past the target split, and the same run again from the same seed.
"""
import collections
import os
import sys

from . import dex
from . import evolve
from . import model
from . import progression
from . import simulate

SEEDS = (1, 2, 3, 4, 5)


def check_runs(results):
    root = model.repo_root()
    rank = progression.split_index(model.load_sidecar())
    runs = [simulate.run("League", deaths=4, seed=s) for s in SEEDS]
    catches = [[e for e in r["log"] if e.get("species")] for r in runs]

    results.append(("the same seed plays the same run",
                    simulate.run("League", deaths=4, seed=SEEDS[0]) == runs[0], ""))
    results.append(("one capture per capture area",
                    all(len({e["area"] for e in c}) == len(c) for c in catches),
                    ", ".join(str(len(c)) for c in catches) + " captures"))
    results.append(("the dupes clause: no two catches share a family, dead ones included",
                    all(len({dex.line_of(root, m["species"]) for m in r["box"]}) == len(r["box"])
                        for r in runs), ""))
    repels = [sum(1 for e in c if e["split"] == "Roark" and "repel" in (e.get("choice") or ""))
              for c in catches]
    results.append(("at most one repel manipulation in Roark's split",
                    all(n <= 1 for n in repels), ", ".join(map(str, repels))))
    results.append(("four deaths asked for, four dead",
                    all(r["dead"] == 4 for r in runs), ", ".join(str(r["dead"]) for r in runs)))
    results.append(("every catch is made in a split no later than the target",
                    all(rank[e["split"]] <= rank["League"] for c in catches for e in c), ""))

    # Ian's sample boxes (2026-09-26) came up empty at Route 223 and the
    # Pokemon League: every line there was a family the box already had, so
    # the dupes clause left nothing (Route 223 in 31 of 40 League runs). The
    # seventeen water lines fixed it; this keeps any area from going dead.
    empty = collections.Counter(e["area"] for r in runs for e in r["log"]
                                if e.get("area") and not e.get("species")
                                and not e.get("wait") and not e.get("death"))
    results.append(("no capture area comes up empty in more than one of the five League runs",
                    all(n <= 1 for n in empty.values()),
                    ", ".join(f"{a} {n}" for a, n in empty.most_common(3)) or "none empty"))

    short = simulate.run("Gardenia", deaths=0, starter="SPECIES_PIPLUP", seed=9)
    results.append(("a run to Gardenia's split starts with the chosen starter and "
                    "catches nothing later",
                    short["starter"] == "SPECIES_PIPLUP"
                    and short["log"][0]["species"] == "SPECIES_PIPLUP"
                    and all(rank[e["split"]] <= rank["Gardenia"]
                            for e in short["log"] if e.get("species")),
                    f"{short['alive']} caught"))
    worth = [r["worth"] for r in runs]
    results.append(("a box's worth is its living sum plus a quarter of its best six",
                    all(abs(r["worth"] - (r["sum_alive"] + simulate.TOP_SIX_WEIGHT * r["top_six"]))
                        < 0.2 for r in runs),
                    ", ".join(f"{w:.0f}" for w in worth)))


def check_scarcity(results):
    """Ian (2026-09-26): no Pokemon worth about 85 or more should be better
    than even odds with best play, a box going into the Elite Four holding
    one to three of them, not a party. The two eggs he accepted as they are."""
    # The two eggs, and Ian's super-wanted lines, which may stay near-guaranteed
    # (values.json, `wanted`); the check compares final stages.
    import json as _json
    wanted = _json.load(open(os.path.join(model.repo_root(), "docs", "oxide", "encounters",
                                          "values.json")))["wanted"]
    root = model.repo_root()
    wanted_lines = {dex.line_of(root, w) for w in wanted
                    if os.path.isdir(os.path.join(root, "res", "pokemon", w[8:].lower()))}
    exempt = {"SPECIES_MANAPHY", "SPECIES_TOGEKISS"}
    n = 20
    got, per_box = collections.Counter(), []
    for seed in range(n):
        r = simulate.run("League", deaths=0, seed=5000 + seed)
        strong = {m["stage"] for m in r["box"] if m["value"] >= 85}
        got.update(sp for sp in strong - exempt if dex.line_of(root, sp) not in wanted_lines)
        per_box.append(len(strong))
    worst = got.most_common(3)
    results.append(("with best play no line worth 85 or more lands in over half of 20 League "
                    "runs (bar the two eggs and Ian's super-wanted lines)",
                    all(c * 2 <= n for _, c in worst),
                    ", ".join(f"{sp[8:].title()} {c}/{n}" for sp, c in worst)
                    + f"; per box median {sorted(per_box)[n // 2]}"))


def check_areas(results):
    rows = simulate.area_values("Wake")
    results.append(("the per-area analysis prices every area to Wake's split, best option first",
                    rows and all(r["options"] and r["options"][0][2] >= r["options"][-1][2]
                                 for r in rows),
                    f"{len(rows)} areas"))


def check_requests(results):
    """Ian's three Box sim requests of 2026-09-27: picks locked by drop list,
    a start from the save, and how sure the sim is of its next calls."""
    root = model.repo_root()
    free = simulate.run("Gardenia", seed=1)
    places = [e for e in free["log"] if e.get("can_give") and e.get("species")
              and e["area"] != free["log"][0]["area"]]
    a, b = places[0], places[1]
    pick = next(o["value"] for o in a["can_give"] if o["value"] != a["species"])
    locked = simulate.run("Gardenia", seed=1, locks={a["area"]: pick, b["area"]: ""})
    at = {e["area"]: e for e in locked["log"] if e.get("area") and not e.get("wait")}
    results.append(("a locked place gives the Pokemon picked for it, a place left unused gives "
                    "nothing, and every other place is still played",
                    at[a["area"]].get("species") == pick and at[a["area"]].get("locked")
                    and at[b["area"]].get("species") is None and at[b["area"]].get("locked")
                    and len([e for e in locked["log"] if e.get("species")]) >= len(places) - 1,
                    f"{a['area']}: {dex.display_name(pick)}; {b['area']}: unused"))

    # A save, as savefile.parse gives it: one Pokemon in the party and a
    # graveyard that has run back from the last box into the one before.
    world = simulate.world("Wake", root)
    spots = [(w["name"], simulate.can_give(w)[0]) for w in world if simulate.can_give(w)][:34]

    def mon(i, box=None, slot=0):
        name, sp = spots[i]
        return {"species": sp, "name": dex.display_name(sp), "met_location": name,
                "egg_location": None, "slot": f"box {box}" if box else "party 1",
                **({"box": box, "box_slot": slot} if box else {})}

    boxes = [mon(1 + i, 18, i + 1) for i in range(30)] + [mon(31, 17, 1), mon(32, 16, 1)]
    save = {"party": [mon(0)], "boxes": boxes, "box_count": 18,
            "progress": {"split": {"index": 1, "name": "Gardenia", "cap": 26}}}
    where = {stem: loc for stem, loc in __import__(
        "tools.oxide.encounters.locations", fromlist=["x"]).location_of(root).items()}
    caught_stem = next(stem for stem, loc in where.items()
                       if loc == spots[33][0] and stem.startswith("encounters_"))
    start = simulate.start_from_save(save, {caught_stem: spots[33][1]}, "Wake", root)
    alive = {m["area"]: m["alive"] for m in start["members"]}
    results.append(("a save's places are spent and its Pokemon counted; the graveyard is the "
                    "last box and, while that is full, the one before it",
                    start["graveyard"] == [17, 18] and alive[spots[1][0]] is False
                    and alive[spots[31][0]] is False and alive[spots[32][0]] is True
                    and alive[spots[0][0]] is True and spots[33][0] in start["used"]
                    and start["split"] == "Gardenia" and not start["unmatched"],
                    f"graveyard {start['graveyard']}, {len(start['used'])} places spent"))
    resumed = simulate.run("Wake", seed=2, start=start)
    played = [e for e in resumed["log"] if e.get("area") and not e.get("from_save")
              and not e.get("death")]
    results.append(("the run resumes from the save: no spent place is played again and "
                    "nothing is played in a split before the save's",
                    not {e["area"] for e in played} & start["used"]
                    and all(rank_of(e["split"]) >= rank_of("Gardenia") for e in played)
                    and sum(1 for e in resumed["log"] if e.get("from_save")) == len(start["members"]),
                    f"{len(played)} places played"))

    conf = simulate.confidence("Gardenia", runs=6, areas=5, seed=3)
    again = simulate.confidence("Gardenia", runs=6, areas=5, seed=3)
    results.append(("confidence names the next five calls, how many of the replays make each, "
                    "and its lead; the same seed gives the same answer",
                    len(conf["areas"]) == 5 and conf == again
                    and all(0 < r["share"] <= 1 and r["runs"] == 6 and r["margin"] >= 0
                            for r in conf["areas"]),
                    "; ".join(f"{r['area']} {r['share']:.0%}" for r in conf["areas"][:3])))


def check_stones(results):
    """Stone branches (Ian, 2026-09-28): a caught Koffing or Ponyta reaches
    its Galarian form by the Moon Stone from the stone's split in the
    balance track's census, and the branch is rated on its own."""
    from . import dex, model
    root, sidecar = model.repo_root(), model.load_sidecar()
    roark = simulate.Values(root, "Roark", sidecar)
    gardenia = simulate.Values(root, "Gardenia", sidecar)
    maylene = simulate.Values(root, "Maylene", sidecar)
    stone = gardenia.stone_first.get("ITEM_MOON_STONE")
    results.append(("a Koffing or Ponyta caught early reaches its Galarian form by the Moon "
                    "Stone from the stone's split, before its level evolution",
                    stone == "Gardenia"
                    and roark.stage("SPECIES_KOFFING") == "SPECIES_KOFFING"
                    and gardenia.stage("SPECIES_KOFFING") == "SPECIES_GALARIAN_WEEZING"
                    and gardenia.stage("SPECIES_PONYTA") == "SPECIES_GALARIAN_RAPIDASH"
                    and gardenia.of("SPECIES_KOFFING") > roark.of("SPECIES_KOFFING"),
                    f"Moon Stone from {stone}; Koffing {gardenia.of('SPECIES_KOFFING')} "
                    f"against {roark.of('SPECIES_KOFFING')}"))
    results.append(("one family: Koffing and Galarian Weezing share a line for the dupes "
                    "clause, and the branch is rated by its own form",
                    dex.line_of(root, "SPECIES_KOFFING") == dex.line_of(root, "SPECIES_GALARIAN_WEEZING")
                    and dex.branch_of(root, "SPECIES_GALARIAN_WEEZING") == "SPECIES_GALARIAN_WEEZING"
                    and dex.branch_of(root, "SPECIES_WEEZING") is None, ""))
    results.append(("a stone for one sex still yields to a level evolution (Snorunt does not "
                    "become Froslass by the Dawn Stone)",
                    maylene.stage("SPECIES_SNORUNT") != "SPECIES_FROSLASS",
                    dex.display_name(maylene.stage("SPECIES_SNORUNT"))))
    # A branch the Pokemon decides (Wurmple by personality, Burmy and Combee
    # by sex) is not the player's pick: the sim takes the worse outcome.
    wurmple = maylene.stage("SPECIES_WURMPLE")
    worse = min(("SPECIES_BEAUTIFLY", "SPECIES_DUSTOX"), key=lambda s: (maylene.worth(s), s))
    results.append(("a branch the Pokemon decides takes the worse outcome (Wurmple, Burmy); "
                    "a male Combee stays one under 50; Nincada becomes Ninjask, not Shedinja",
                    wurmple == worse
                    and maylene.stage("SPECIES_BURMY") == min(("SPECIES_WORMADAM", "SPECIES_MOTHIM"),
                                                               key=lambda s: (maylene.worth(s), s))
                    and maylene.stage("SPECIES_COMBEE") == "SPECIES_COMBEE"
                    # Ninjask is off the pick-list, so the route list is the check.
                    and [r[0] for r in evolve.routes(root, "SPECIES_NINCADA")] == ["SPECIES_NINJASK"],
                    f"Wurmple to {dex.display_name(wurmple)}"))


def rank_of(split):
    return progression.split_index(model.load_sidecar()).get(split, 99)


def main():
    results = []
    for check in (check_runs, check_scarcity, check_areas, check_requests, check_stones):
        check(results)
    width = max(len(l) for l, _, _ in results)
    failed = 0
    for label, ok, note in results:
        failed += not ok
        print(f"  {'ok  ' if ok else 'FAIL'}  {label:{width}}  {note}")
    print(f"\n{len(results) - failed}/{len(results)} passed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())

"""The box simulator keeps Ian's rules (simulate.py).

    PYTHONPATH=. python3 -m tools.oxide.encounters.test_sim

Read-only. Plays a handful of seeded runs and checks each against the rules
the simulator promises: one capture per area, the dupes clause over
families, one repel before Gardenia's split, the deaths asked for, nothing
from past the target split, and the same run again from the same seed.
"""
import sys

from . import dex
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


def check_areas(results):
    rows = simulate.area_values("Wake")
    results.append(("the per-area analysis prices every area to Wake's split, best option first",
                    rows and all(r["options"] and r["options"][0][2] >= r["options"][-1][2]
                                 for r in rows),
                    f"{len(rows)} areas"))


def main():
    results = []
    for check in (check_runs, check_areas):
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

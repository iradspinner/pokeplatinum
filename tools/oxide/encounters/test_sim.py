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


def main():
    results = []
    for check in (check_runs, check_scarcity, check_areas):
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

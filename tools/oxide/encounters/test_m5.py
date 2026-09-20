"""M5 acceptance: the planner produces a correct multi-step plan.

    PYTHONPATH=. python3 -m tools.oxide.encounters.test_m5

The gate is the design doc's: one hand-verified case, worked out on paper
first and then matched. The paper case is the doc's own thought experiment --
99% junk in front of a 1% prize, with the junk catchable earlier -- built as
two synthetic tables small enough to do the arithmetic by hand:

  Area A (earlier):  Rattata in slots 0-9 (98%) at level 5,
                     Pidgey in slots 10-11 (2%) at level 6.
  Area T (target):   Rattata in slots 0-9 (98%) at level 10,
                     Mewtwo in slots 10-11 (2%) at level 10.

Unplanned, T gives Mewtwo at 2% and every encounter counts, so the first
counting encounter costs 1 battle: (cost 1, P 0.02).

Planned: catch Rattata at A. Its best rung is lead 5 (the whole table), where
it is 98%, so expected encounters 1/0.98 = 1.0204. Then Rattata is duped out
of T, Mewtwo is the only thing that counts, so P = 1.0, and the first
counting encounter costs 1/0.02 = 50 battles. Total 51.0204.

The Pareto front is exactly those two points, in that order.

The rest checks the per-area rules on the real tables: sources are earlier
than the target, each source is used once, an area with a recorded encounter
is never a source, and the target's own line is never acquired.
"""
import sys

from . import analysis as A
from . import dex
from . import model
from . import planner


def synthetic():
    rat, pid, mew = "SPECIES_RATTATA", "SPECIES_PIDGEY", "SPECIES_MEWTWO"
    a = [(rat, 5)] * 10 + [(pid, 6)] * 2
    t = [(rat, 10)] * 10 + [(mew, 10)] * 2
    areas = [
        {"name": "A", "order": 0, "used": False, "tables": {"land": a}},
        {"name": "T", "order": 1, "used": False, "tables": {"land": t}},
    ]
    line_of = {rat: rat, pid: pid, mew: mew}
    members_of = {rat: [rat], pid: [pid], mew: [mew]}
    return areas, line_of, members_of, rat, mew


def check_paper_case(results):
    areas, line_of, members_of, rat, mew = synthetic()
    out = planner.plan("T", mew, "land", areas, set(), line_of, members_of)
    front = out["front"]
    results.append(("front has exactly the two paper points",
                    len(front) == 2, f"{len(front)} points"))
    if len(front) == 2:
        u, p = front
        results.append(("unplanned: P 0.02 at cost 1",
                        abs(u["p"] - 0.02) < 1e-12 and abs(u["cost"] - 1) < 1e-12
                        and not u["lines"],
                        f"P {u['p']:.4f} cost {u['cost']:.4f}"))
        results.append(("planned: P 1.0 at cost 1/0.98 + 50",
                        abs(p["p"] - 1.0) < 1e-12
                        and abs(p["cost"] - (1 / 0.98 + 50)) < 1e-9
                        and p["lines"] == [rat],
                        f"P {p['p']:.4f} cost {p['cost']:.4f}"))
        acq = p["acquisitions"][0] if p["acquisitions"] else {}
        results.append(("the acquisition is Rattata at A, lead 5, 98%",
                        acq.get("area") == "A" and acq.get("lead") == 5
                        and abs(acq.get("p", 0) - 0.98) < 1e-12,
                        f"{acq.get('area')} lead {acq.get('lead')} "
                        f"p {acq.get('p', 0):.3f}"))
    results.append(("baseline is the unplanned point",
                    out["baseline"] and not out["baseline"]["lines"]
                    and abs(out["baseline"]["p"] - 0.02) < 1e-12, ""))


def check_used_area_is_not_a_source(results):
    areas, line_of, members_of, rat, mew = synthetic()
    areas[0]["used"] = True
    out = planner.plan("T", mew, "land", areas, set(), line_of, members_of)
    results.append(("an area with a recorded encounter is never a source",
                    len(out["front"]) == 1 and not out["front"][0]["lines"],
                    f"{len(out['front'])} point(s)"))


def check_owned_line_costs_nothing(results):
    areas, line_of, members_of, rat, mew = synthetic()
    out = planner.plan("T", mew, "land", areas, {rat}, line_of, members_of)
    results.append(("an already-owned line is removed at no cost",
                    len(out["front"]) == 1 and abs(out["front"][0]["p"] - 1.0)
                    < 1e-12 and out["front"][0]["cost_acquire"] == 0,
                    f"P {out['front'][0]['p']:.3f}" if out["front"] else "-"))


def _real_areas():
    """The live tables in play order, with the per-area encounter record."""
    root = model.repo_root()
    live = [a for a in model.load_all() if a.land_active]
    live.sort(key=lambda a: (A.median(a.levels), min(a.levels), a.name))
    from . import server
    enc = server.load_encounters()
    areas = []
    for i, a in enumerate(live):
        areas.append({"name": a.name, "order": i, "used": a.name in enc,
                      "tables": {k: a.kind_slots(k) for k in a.kinds_present()}})
    lines = dex.lines(root)
    members = {}
    for sp, l in lines.items():
        members.setdefault(l, []).append(sp)
    return areas, lines, members


def check_real_tables(results):
    areas, line_of, members_of = _real_areas()
    # Route 214's rarest, the doc's own worked example target
    name = "encounters_route_214"
    target = next(a for a in areas if a["name"] == name)
    slots = target["tables"]["land"]
    y = A.rarest(A.merged(slots))
    y_line = line_of.get(y, y)
    out = planner.plan(name, y, "land", areas, set(), line_of, members_of)
    front = out["front"]
    results.append(("real table produces a front",
                    len(front) >= 2, f"{len(front)} points from "
                    f"{out['n_candidates']} candidates"))
    t_order = target["order"]
    ok_order = all(
        next(a["order"] for a in areas if a["name"] == acq["area"]) < t_order
        for c in front for acq in c["acquisitions"])
    results.append(("every source is earlier than the target", ok_order, ""))
    ok_distinct = all(len({acq["area"] for acq in c["acquisitions"]})
                      == len(c["acquisitions"]) for c in front)
    results.append(("no source area is used twice in one plan", ok_distinct,
                    ""))
    results.append(("the target's own line is never acquired",
                    all(y_line not in c["lines"] for c in front), ""))
    costs = [c["cost"] for c in front]
    ps = [c["p"] for c in front]
    results.append(("front is sorted by cost and strictly rises in P",
                    costs == sorted(costs)
                    and all(b > a for a, b in zip(ps, ps[1:])), ""))
    results.append(("planning beats the unplanned odds",
                    front[-1]["p"] > out["baseline"]["p"],
                    f"{out['baseline']['p']:.3f} -> {front[-1]['p']:.3f}"))


def main():
    results = []
    for check in (check_paper_case, check_used_area_is_not_a_source,
                  check_owned_line_costs_nothing, check_real_tables):
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

"""Authoring plan Step 1: the progression order and the tiers are written,
and R12 evaluates instead of reporting itself skipped.

    PYTHONPATH=. python3 -m tools.oxide.encounters.test_step1

Read-only: it checks the committed sidecar and pick-list as they are. The
one-off writers (`cli order-init`, `cli tier-init`) are exercised through
their refusal to overwrite what Ian may have edited.
"""
import contextlib
import io
import sys

from . import audit
from . import cli
from . import dex
from . import lint
from . import model
from . import progression
from . import tiers


def run_cli(*argv):
    out = io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(io.StringIO()):
        try:
            rc = cli.main(list(argv))
        except SystemExit as e:
            rc = e.code
    return rc, out.getvalue()


def check_order(results):
    sidecar = model.load_sidecar()
    areas = sidecar["areas"]
    names = model.area_names()
    orders = {n: areas.get(n, {}).get("order") for n in names}
    missing = [n for n, o in orders.items() if o is None]
    values = [o for o in orders.values() if o is not None]
    # 185 files, 186 with Verity Lakefront's (2026-09-21), 188 with Amity
    # Square's and Snowpoint City's (2026-09-25)
    results.append(("every one of the 188 areas carries an order",
                    len(names) == 188 and not missing, f"missing {missing[:4]}"))
    results.append(("orders are the integers 1..188 with no duplicates",
                    sorted(values) == list(range(1, len(names) + 1)), f"{len(set(values))} distinct"))

    def pos(stem):
        return orders["encounters_" + stem]
    results.append(("the corridor runs Twinleaf, 201, 202, 203, Eterna Forest in that order",
                    pos("twinleaf_town") < pos("route_201") < pos("route_202")
                    < pos("route_203") < pos("eterna_forest") < pos("route_206"), ""))
    results.append(("multi-file areas take consecutive integers in floor order",
                    [pos(f"route_209_lost_tower_{f}f") for f in range(1, 6)]
                    == list(range(pos("route_209_lost_tower_1f"),
                                  pos("route_209_lost_tower_1f") + 5))
                    and pos("victory_road_1f") < pos("victory_road_2f") < pos("victory_road_b1f"),
                    ""))
    results.append(("the Battle Zone and the unknown rooms come last",
                    pos("pokemon_league") < pos("route_225") < pos("route_230")
                    < pos("unknown_533") < pos("unknown_557") == len(names), ""))
    live = [a for a in model.load_all() if a.land_active]
    ordered = progression.sorted_by_order(sidecar, [a.name for a in live])
    results.append(("sorted_by_order puts the early band first and the late band last",
                    ordered[0] == "encounters_route_201"
                    and ordered[-1] == "encounters_unknown_557", ordered[0]))
    rc, _ = run_cli("order-init")
    results.append(("`order-init` refuses to overwrite an existing order without --force",
                    rc == 1, f"exit {rc}"))
    results.append(("the R12 ceilings are in the sidecar's thresholds",
                    set((sidecar.get("thresholds") or {}).get("r12_max_cost") or {})
                    == {"starter-adjacent", "preferred", "filler"}, ""))


def check_tiers(results):
    root = model.repo_root()
    rows = dex.pick_list(root)
    bad = [r["name"] for r in rows if r.get("tier") not in tiers.TIERS]
    # 360 rows from Ian's sheet, plus the seven cave rows (Nosepass, Geodude
    # and Phanpy lines), the fourteen fishing rows (Goldeen, Corphish,
    # Chinchou, Carvanha, Remoraid, Buizel, Shellos lines), Mantyke and Mantine,
    # and the five ghost rows (Gastly and Misdreavus lines) Ian added for the
    # Old Chateau on 2026-09-21.
    results.append(("every pick-list row has one of the four tiers",
                    len(rows) == 388 and not bad, f"{len(rows)} rows, bad {bad[:4]}"))
    by = {r["name"]: r["tier"] for r in rows}
    results.append(("legendaries, starters, fossils and static battles are gate",
                    by["Articuno"] == by["Charmander"] == by["Cranidos"]
                    == by["Dialga"] == by["Rotom"] == "gate", ""))
    results.append(("a native line shares one tier across its stages",
                    by["Zubat"] == by["Golbat"] == by["Crobat"]
                    and by["Pichu"] == by["Pikachu"] == by["Raichu"], ""))
    results.append(("starter-adjacent comes from vanilla's early routes",
                    by["Zubat"] == "starter-adjacent" and by["Shinx"] == "starter-adjacent"
                    and by["Budew"] == "starter-adjacent", ""))
    results.append(("the Sinnoh dex is preferred, the rest filler, first-route lines starter-adjacent",
                    by["Pikachu"] == "preferred" and by["Koffing"] == "filler"
                    and by["Toxel"] == "filler" and by["Nidoran F"] == "starter-adjacent"
                    and by["Wooloo"] == "starter-adjacent", ""))
    rc, _ = run_cli("tier-init")
    results.append(("`tier-init` refuses to overwrite existing tiers without --force",
                    rc == 1, f"exit {rc}"))


def check_r12(results):
    avail = audit.availability()
    # 99 native lines before Phase 4 element 3, 177 with the 159 new species
    # in, 187 with Ian's three cave lines and seven fishing lines, 189 with the
    # Gastly and Misdreavus lines.
    results.append(("availability rows exist once the tiers are written",
                    avail is not None and len(avail) == 189
                    and all(r["tier"] for r in avail), f"{len(avail or [])} rows"))
    by = {r["name"]: r for r in avail}
    results.append(("a scripted line is non_wild; a wild face has a cost near 1/share",
                    by["Dialga"]["non_wild"] and by["Turtwig"]["non_wild"]
                    and by["Zubat"]["cost"] is not None and by["Zubat"]["cost"] < 5, ""))
    areas = [a for a in model.load_all() if a.land_active]
    sidecar = model.load_sidecar()
    payload = [(a.name, a.slots, sidecar["areas"].get(a.name), a.data) for a in areas]
    findings = lint.lint_all(payload, sidecar, avail)
    r12 = [f for f in findings if f.rule == "R12"]
    results.append(("R12 evaluates on the working tree: no skip finding, errors named by line",
                    r12 and not any(f.severity == "skip" for f in r12)
                    and all(f.target != "*" for f in r12), f"{len(r12)} findings"))
    errors = {f.target for f in r12 if f.severity == "error"}
    # Snivy used to be here; it is wild on Route 204 since Ian's review.
    results.append(("the roamers pass R12 through their vanilla mechanism; new gate lines "
                    "with no script fail it",
                    not {"Articuno", "Mesprit", "Cresselia"} & errors
                    and {"Nihilego", "Xurkitree"} <= errors and "Snivy" not in errors, ""))
    skipped = lint.lint_all(payload, sidecar, None)
    results.append(("without availability rows R12 still reports itself skipped",
                    any(f.rule == "R12" and f.severity == "skip" for f in skipped), ""))
    rc, text = run_cli("--ref", "main", "lint", "--rule", "R12")
    results.append(("`lint --ref main` evaluates R12 too, and fails loudly",
                    rc == 0 and "0 skipped" in text and "error R12" in text, ""))
    rc, text = run_cli("--ref", "main", "lint", "--fail-on", "error", "--ignore", "R12")
    results.append(("vanilla passes every other error-level rule with R12 ignored (the integrate check)",
                    rc == 0 and "0 error(s)" in text, f"exit {rc}"))


def main():
    results = []
    for check in (check_order, check_tiers, check_r12):
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

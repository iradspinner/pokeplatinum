"""Authoring plan Step 2: the availability plan exists, passes its gate, and
the committed document is what the plan generates.

    PYTHONPATH=. python3 -m tools.oxide.encounters.test_step2

Read-only: it checks availability-plan.json and availability.md as
committed, so a hand edit to the plan without a regenerate fails here.
"""
import contextlib
import io
import os
import sys

from . import availability
from . import cli
from . import model


def run_cli(*argv):
    out = io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(io.StringIO()):
        try:
            rc = cli.main(list(argv))
        except SystemExit as e:
            rc = e.code
    return rc, out.getvalue()


def main():
    results = []
    out = availability.build()
    rows = out["rows"]
    by = {r["name"]: r for r in rows}
    g = out["gate"]

    results.append(("the plan file loads, names only real areas and pick-list lines",
                    not out["problems"], "; ".join(out["problems"][:3])))
    results.append(("every one of the 177 lines has a row",
                    len(rows) == 177, f"{len(rows)} rows"))
    results.append(("no line is without a source: every wild line has a home, "
                    "every gate line a script or a proposal",
                    not g["no_source"], ", ".join(g["no_source"][:5])))
    tails = {"Litten", "Froakie"}   # Ian's call: tails a dupe-out plan pays off, no home
    results.append(("every non-gate line has exactly one planned home or a non-wild, water or "
                    "honey source, bar the two deliberate tails",
                    all(len(r["home"]) == 1 or r["non_wild"] or r["status"] in ("water", "honey")
                        or r["name"] in tails
                        for r in rows if r["tier"] != "gate"),
                    ", ".join(r["name"] for r in rows
                              if r["tier"] != "gate" and not (len(r["home"]) == 1 or r["non_wild"]
                                                              or r["status"] in ("water", "honey")
                                                              or r["name"] in tails))[:120]))
    results.append(("no gate line is planned in the wild",
                    not any(r["home"] or r["cameo"] for r in rows if r["tier"] == "gate"), ""))
    results.append(("the corridor carries only starter-adjacent and scripted lines",
                    not g["corridor_intruders"], ", ".join(g["corridor_intruders"][:4])))
    results.append(("every starter-adjacent line is at home in the corridor",
                    not g["early_home_outside"], ", ".join(g["early_home_outside"][:4])))
    results.append(("every early-band table has 2-5 lines planned, 2 only for a duo",
                    not g["early_fit"], ", ".join(g["early_fit"][:3])))
    results.append(("every live land table has something planned",
                    not g["unplanned_tables"], ", ".join(g["unplanned_tables"][:4])))
    results.append(("the corridor ends at Eterna Forest and holds 17 live tables",
                    out["plan"]["corridor_end"] == "encounters_eterna_forest"
                    and len(out["corridor"]) == 17, f"{len(out['corridor'])} tables"))
    results.append(("known placements: Gible at home in Wayward Cave B1F, Shinx on Route 202, "
                    "Wooper in the marsh",
                    by["Gible"]["home"] == ["encounters_wayward_cave_b1f"]
                    and by["Shinx"]["home"] == ["encounters_route_202"]
                    and by["Wooper"]["home"] == ["encounters_great_marsh_1"], ""))
    results.append(("scripted lines carry their source, not a home (Turtwig, Dialga, Togepi)",
                    all(by[n]["status"] == "non-wild" and not by[n]["home"]
                        for n in ("Turtwig", "Dialga", "Togepi")), ""))
    results.append(("the roamers and Phione are sourced by their vanilla mechanism",
                    all(by[n]["status"] == "non-wild" for n in
                        ("Articuno", "Mesprit", "Cresselia", "Phione")), ""))
    proposed = [r["name"] for r in rows if r["status"] == "proposed"]
    pool = [r["name"] for r in rows if r["status"] == "pool"]
    results.append(("every new legendary is in the pool or, for the two box legendaries, proposed",
                    all(r["status"] in ("pool", "proposed") for r in rows
                        if r["tier"] == "gate" and not r["non_wild"])
                    and sorted(proposed) == ["Xerneas", "Yveltal"]
                    and "Nihilego" in pool and "Tapu Koko" in pool,
                    f"{len(pool)} in the pool, {len(proposed)} proposed"))
    results.append(("the starters are wild: Fennekin and Scorbunny at home, Popplio on water, "
                    "the grass three in the honey trees, none gate",
                    by["Fennekin"]["home"] == ["encounters_route_214"]
                    and by["Scorbunny"]["home"] == ["encounters_route_206"]
                    and by["Popplio"]["status"] == "water"
                    and all(by[n]["status"] == "honey" for n in ("Rowlet", "Snivy", "Sprigatito"))
                    and all(by[n]["tier"] == "preferred" for n in
                            ("Fennekin", "Scorbunny", "Popplio", "Rowlet", "Litten", "Froakie")),
                    ""))
    results.append(("water lines are homed on water tables",
                    all(r["water"] for r in rows if r["status"] == "water")
                    and by["Tentacool"]["status"] == "water", ""))

    path = os.path.join(model.repo_root(), availability.DOC)
    with open(path, encoding="utf-8") as f:
        committed = f.read()
    results.append(("availability.md is exactly what the plan renders (regenerate after editing the plan)",
                    committed == availability.render(out), ""))
    rc, text = run_cli("availability")
    results.append(("`cli availability` passes the gate", rc == 0, f"exit {rc}"))

    width = max(len(l) for l, _, _ in results)
    failed = 0
    for label, ok, note in results:
        failed += not ok
        print(f"  {'ok  ' if ok else 'FAIL'}  {label:{width}}  {note}")
    print(f"\n{len(results) - failed}/{len(results)} passed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())

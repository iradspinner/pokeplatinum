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
    # 177 lines, 180 with Ian's three cave additions, 187 with his seven
    # fishing lines, 189 with the Gastly and Misdreavus lines (all 2026-09-21),
    # 206 with the seventeen water lines, 205 with the Magikarp line cut
    # and 239 with the 34 lines of the Platinum-size pick-list (all 2026-09-26)
    # 238 since Fomantis evolves into Lurantis (main-scripts, 2026-09-27), one line,
    # and 239 since Remoraid and Mantyke are two lines again (the same day: the
    # tool read the Remoraid in Mantyke's party method as its evolution), and
    # 237 since the Moon Stone joins Galarian Weezing to Koffing's family and
    # Galarian Rapidash to Ponyta's (2026-09-28, Ian: one family each). Still
    # 237 with Meloetta's line in and Alolan Ninetales joined to Vulpix's family
    # by the Ice Stone (element 7, the same day).
    results.append(("every one of the 237 lines has a row",
                    len(rows) == 237, f"{len(rows)} rows"))
    results.append(("no line is without a source: every wild line has a home, "
                    "every gate line a script or a proposal",
                    not g["no_source"], ", ".join(g["no_source"][:5])))
    # Every line is somewhere. A home is the one table designed around a line
    # and a line has at most one; since Ian's scarcity ruling and the larger
    # pick-list (2026-09-26) a line may also live only as cameos or tails,
    # below the 10% a home needs (Larvitar beside Gible, Kricketot, Abra...).
    sourced = ("water", "honey", "cameo-only", "tail-only")
    # A regional branch (Galarian Weezing in Koffing's family) keeps a home of
    # its own beside the family's: one home per branch (2026-09-28).
    one_each = lambda r: all(len(a) <= 1 for a in (r.get("branch_homes") or {}).values())
    placed = lambda r: (r["home"] or r["non_wild"] or r["status"] in sourced) and one_each(r)
    results.append(("every non-gate line has one planned home, a non-wild, water or honey "
                    "source, or a place as a cameo or tail; none has two homes for one branch",
                    all(placed(r) for r in rows if r["tier"] != "gate"),
                    ", ".join(r["name"] for r in rows if r["tier"] != "gate" and not placed(r))[:120]))
    koffing, ponyta = by["Koffing"], by["Ponyta"]
    results.append(("a regional branch keeps its own home in its base's family, and is reached "
                    "by the stone from the later of the base's first split and the stone's "
                    "(Galarian Weezing from Koffing, Galarian Rapidash from Ponyta)",
                    [b["name"] for b in koffing["branches"]] == ["Galarian Weezing"]
                    and koffing["branches"][0]["home"] == ["encounters_stark_mountain_outside"]
                    and [b["name"] for b in ponyta["branches"]] == ["Galarian Rapidash"]
                    and all(b["via_split"] and b["stone"] == "ITEM_MOON_STONE"
                            for b in koffing["branches"] + ponyta["branches"]),
                    "; ".join(f"{b['name']} via {b['via_split']}, wild {b['wild_split']}"
                              for b in koffing["branches"] + ponyta["branches"])))
    # A gate-tier starter may be a cameo or a tail (Ian: starters are the reason
    # to take a delay), never a home; a legendary is neither.
    results.append(("no gate line is planned as a wild home, and no legendary is planned wild at all",
                    not any(r["home"] for r in rows if r["tier"] == "gate")
                    and not any(r["cameo"] or r["tail"] for r in rows
                                if r["tier"] == "gate" and r["name"] in ("Dialga", "Uxie", "Nihilego", "Xerneas")), ""))
    results.append(("the first split carries only starter-adjacent, scripted and tail lines",
                    not g["corridor_intruders"], ", ".join(g["corridor_intruders"][:4])))
    results.append(("every starter-adjacent line is at home in the corridor",
                    not g["early_home_outside"], ", ".join(g["early_home_outside"][:4])))
    results.append(("every early-band table has 4-7 lines planned (Ian's cap: flat tables)",
                    not g["early_fit"], ", ".join(g["early_fit"][:3])))
    results.append(("every live land table has something planned",
                    not g["unplanned_tables"], ", ".join(g["unplanned_tables"][:4])))
    # 20 until 2026-09-27; 23 with the grass of Sandgem, Jubilife and Floaroma.
    results.append(("the corridor is the Roark and Gardenia splits: 23 live land tables",
                    out["plan"]["corridor_splits"] == ["Roark", "Gardenia"]
                    and len(out["corridor"]) == 23, f"{len(out['corridor'])} tables"))
    results.append(("known placements: Gible at home in Wayward Cave B1F, Shinx on Route 202, "
                    "Wooper in the marsh",
                    by["Gible"]["home"] == ["encounters_wayward_cave_b1f"]
                    and by["Shinx"]["home"] == ["encounters_route_202"]
                    and by["Wooper"]["home"] == ["encounters_great_marsh_1"], ""))
    results.append(("scripted lines carry their source, not a home (Turtwig, Dialga, Togepi)",
                    all(by[n]["status"] == "non-wild" and not by[n]["home"]
                        for n in ("Turtwig", "Dialga", "Togepi")), ""))
    # Mesprit's roamer is the pool's roamer draw, held back since 2026-09-27.
    results.append(("the roamers and Phione are sourced by their vanilla mechanism; Mesprit "
                    "waits in the held-back roamer draw",
                    all(by[n]["status"] == "non-wild" for n in ("Articuno", "Cresselia", "Phione"))
                    and by["Mesprit"]["status"] == "pool", by["Mesprit"]["status"]))
    proposed = [r["name"] for r in rows if r["status"] == "proposed"]
    pool = [r["name"] for r in rows if r["status"] == "pool"]
    results.append(("every new legendary is in the pool or, for the two box legendaries, proposed",
                    all(r["status"] in ("pool", "proposed") for r in rows
                        if r["tier"] == "gate" and not r["non_wild"])
                    and sorted(proposed) == ["Xerneas", "Yveltal"]
                    and "Nihilego" in pool and "Guzzlord" in pool
                    # the roamer's draw named Tapu Koko until Ian held it back
                    # (2026-09-27); its lines now wait in the pool
                    and "Tapu Koko" in pool
                    and not next(r for r in rows if r["name"] == "Tapu Koko")["non_wild"],
                    f"{len(pool)} in the pool, {len(proposed)} proposed"))
    # Scorbunny replaced Chimchar in Rowan's briefcase on 2026-09-21 (Ian), so it
    # is gate tier and out of the wild; Litten took over its home on Route 204
    # north, which is what made that half of the route worth delaying for.
    results.append(("the starters are wild: Fennekin and Litten at home (Litten on Route "
                    "204 north, the delay), Popplio only from the Eterna trade, the grass three at home on land "
                    "since the honey trees lost their rare tier, none gate but Scorbunny, "
                    "which is the starter now",
                    by["Fennekin"]["home"] == ["encounters_route_214"]
                    and by["Litten"]["home"] == ["encounters_route_204_north"]
                    # A line the player can always have is in no table (Ian,
                    # 2026-09-26), so Popplio is the Eterna trade's alone.
                    and not by["Popplio"]["water"] and not by["Popplio"]["cameo"]
                    and by["Popplio"]["status"] == "non-wild"
                    and by["Scorbunny"]["tier"] == "gate"
                    and by["Scorbunny"]["non_wild"]
                    and by["Rowlet"]["home"] == ["encounters_eterna_forest"]
                    and by["Snivy"]["home"] == ["encounters_route_204_north"]
                    and by["Sprigatito"]["home"] == ["encounters_route_210_south"]
                    and all(by[n]["tier"] == "preferred" for n in
                            ("Fennekin", "Popplio", "Rowlet", "Litten", "Froakie")),
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

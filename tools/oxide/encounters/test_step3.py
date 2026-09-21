"""Authoring plan Step 3, as revised on Ian's review of 2026-09-21: capture
areas by location name, gym splits with rod gating and caps, the flat
archetypes under his cap, rod tables through apply, and the regenerated
Roark and Gardenia splits.

    PYTHONPATH=. python3 -m tools.oxide.encounters.test_step3

Read-only against the committed tree. Do not run it alongside test_step0,
which rewrites shared files under a restore.
"""
import contextlib
import io
import sys

from . import analysis as A
from . import audit
from . import availability
from . import cli
from . import dex
from . import layout
from . import lint
from . import locations
from . import model
from . import progression


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
    root = model.repo_root()
    sidecar = model.load_sidecar()
    entries = sidecar["areas"]

    # -- locations ----------------------------------------------------------
    loc = locations.location_of(root)
    by = locations.by_location(root)
    results.append(("every header-used encounter file has an English location name",
                    all(v and not v.startswith("LocationNames_") for v in loc.values())
                    and len(by) >= 60, f"{len(loc)} files, {len(by)} locations"))
    results.append(("tables sharing a name are one capture area: Lake Verity, Route 204, "
                    "Route 205, Oreburgh Gate, Mt. Coronet",
                    set(by.get("Lake Verity", [])) == {"encounters_lake_verity", "encounters_lake_verity_low_water"}
                    and set(by.get("Route 204", [])) == {"encounters_route_204_north", "encounters_route_204_south"}
                    and "encounters_mt_coronet_1f_north_room_1" in by.get("Mt. Coronet", [])
                    and set(by.get("Oreburgh Gate", [])) == {"encounters_oreburgh_gate_1f", "encounters_oreburgh_gate_b1f"},
                    ""))
    results.append(("Verity Lakefront's file exists but no header uses it yet (backlog: header and grass)",
                    "encounters_verity_lakefront" in model.area_names()
                    and locations.location("encounters_verity_lakefront") is None, ""))

    # -- splits -------------------------------------------------------------
    sp = progression.split_of(sidecar)
    idx = progression.split_index(sidecar)
    results.append(("every sidecar area carries a split, and the split table has the nine gyms "
                    "plus post-game in order",
                    len(sp) == len(entries) and list(idx) == progression.SPLITS, f"{len(sp)}/{len(entries)}"))
    results.append(("Ian's boundaries: Route 207 and both mine floors in Roark's split, Ravaged Path, "
                    "Route 204 north, 211 west and Coronet's first room in Gardenia's, Route 206 later",
                    sp["encounters_route_207"] == "Roark" and sp["encounters_oreburgh_mine_b2f"] == "Roark"
                    and sp["encounters_route_204_south"] == "Roark"
                    and sp["encounters_ravaged_path"] == "Gardenia" and sp["encounters_route_204_north"] == "Gardenia"
                    and sp["encounters_route_211_west"] == "Gardenia"
                    and sp["encounters_mt_coronet_1f_north_room_1"] == "Gardenia"
                    and idx[sp["encounters_route_206"]] > idx["Gardenia"], ""))
    results.append(("rods arrive by split: Old Rod Roark, Good Rod Maylene, Super Rod Candice; "
                    "Gardenia's cap is 26, the others are Ian's to fill",
                    progression.rod_split(sidecar, "old_rod") == "Roark"
                    and progression.rod_split(sidecar, "good_rod") == "Maylene"
                    and progression.rod_split(sidecar, "super_rod") == "Candice"
                    and progression.cap_of(sidecar, "Gardenia") == 26
                    and progression.cap_of(sidecar, "Roark") is None, ""))
    rc, _ = run_cli("split-init")
    results.append(("`split-init` refuses to overwrite existing splits without --force",
                    rc == 1, f"exit {rc}"))

    # -- evolution levels ---------------------------------------------------
    results.append(("final_by_level: Magikarp 20, Sentret 15, a final stage 0, Zubat and Nidoran None "
                    "(friendship, a stone), a mega form is not a stage",
                    dex.final_by_level(root, "SPECIES_MAGIKARP") == 20
                    and dex.final_by_level(root, "SPECIES_SENTRET") == 15
                    and dex.final_by_level(root, "SPECIES_GYARADOS") == 0
                    and dex.final_by_level(root, "SPECIES_ZUBAT") is None
                    and dex.final_by_level(root, "SPECIES_NIDORAN_F") is None, ""))

    # -- archetypes and the cap ---------------------------------------------
    results.append(("A11 and A12 sum to 100, top share 30, and the thresholds carry the cap",
                    sum(lint.ARCHETYPES["A11"]["signature"]) == 100
                    and sum(lint.ARCHETYPES["A12"]["signature"]) == 100
                    and lint.ARCHETYPES["A12"]["tail"] == "real"
                    and lint.thresholds_from(sidecar)["r11_top_share_max"] == 0.35
                    and lint.thresholds_from(sidecar)["bands"]["early"]["top"][1] == 0.35, ""))
    slots = layout.layout({"archetype": "A12", "base_level": 10,
                           "cast": [f"SPECIES_S{k}" for k in range(7)]})
    merged = A.merged(slots)
    results.append(("an A12 lays out with its 4% and 1% as real tails on the top rungs",
                    abs(merged["SPECIES_S5"] - 0.04) < 1e-9 and abs(merged["SPECIES_S6"] - 0.01) < 1e-9
                    and max(merged.values()) <= 0.30 + 1e-9, ""))

    # -- rod tables through apply -------------------------------------------
    rows = layout.water("old_rod", {"cast": ["SPECIES_A"] * 5, "levels": [3, 7]})
    results.append(("layout.water gives five slots with the level range, and refuses a short cast",
                    len(rows) == 5 and rows[0] == ("SPECIES_A", 3, 7)
                    and _raises(lambda: layout.water("old_rod", {"cast": ["SPECIES_A"] * 4, "levels": [3, 7]})),
                    ""))
    tw = model.load_area("encounters_twinleaf_town")
    spec = entries["encounters_twinleaf_town"]["old_rod"]
    results.append(("Twinleaf's Old Rod table is what its sidecar entry says, slot for slot",
                    [s for s, _, _ in tw.kind_slots("old_rod")] == spec["cast"]
                    and all((lo, hi) == tuple(spec["levels"]) for _, lo, hi in tw.kind_slots("old_rod")),
                    ""))
    rc, text = run_cli("apply", "--all", "--dry-run")
    results.append(("`apply --all --dry-run` finds every designed table already laid out",
                    rc == 0 and "0 failed" in text and "would change" not in text, f"exit {rc}"))

    # -- the regenerated splits ---------------------------------------------
    designed = [n for n, e in entries.items() if e.get("cast")]
    first_two = [n for n in designed if sp.get(n) in ("Roark", "Gardenia")]
    results.append(("every land table in the first two splits is designed (20) and Route 201 counts",
                    len(first_two) == 20 and "encounters_route_201" in first_two
                    and not entries["encounters_route_201"].get("no_capture"), f"{len(first_two)}"))
    tops = {}
    for n in designed:
        a = model.load_area(n)
        tops[n] = A.table_metrics(a.slots)["top_share"]
    results.append(("no designed table puts a species over 30% (Ian's cap is ~35)",
                    all(t <= 0.30 + 1e-9 for t in tops.values()),
                    ", ".join(f"{n.replace('encounters_', '')} {t:.2f}" for n, t in tops.items() if t > 0.30)))
    listed = audit.on_list(root)
    leaks = []
    for n in designed:
        a = model.load_area(n)
        for kind in a.kinds_present():
            if kind == "land" or entries[n].get(kind):
                leaks += [s for s, _, _ in a.kind_slots(kind) if s not in listed]
        leaks += [s for s in (a.data.get("day") or []) + (a.data.get("night") or []) if s not in listed]
    results.append(("no designed land, day/night or rod slot holds an off-list species",
                    not leaks, ", ".join(sorted(set(leaks))[:5])))
    tails = {n: e["cast"][-2:] for n, e in entries.items() if e.get("archetype") == "A12"}
    starters = {"SPECIES_CHARMANDER", "SPECIES_TREECKO", "SPECIES_TORCHIC", "SPECIES_MUDKIP"}
    # Lake Verity's two tables are one location, so Mudkip's 1% counts once.
    results.append(("the classic starters appear as 1% tails only, in one location each on land",
                    all(any(t[-1] == s for t in tails.values()) for s in starters)
                    and all(len({loc.get(n) or n for n, e in entries.items()
                                 if s in (e.get("cast") or [])}) == 1
                            for s in starters), ""))
    results.append(("Route 204 north is the delay's better half: Scorbunny at home, Riolu and Eevee its tail",
                    entries["encounters_route_204_north"]["cast"][0] == "SPECIES_SCORBUNNY"
                    and tails["encounters_route_204_north"] == ["SPECIES_RIOLU", "SPECIES_EEVEE"], ""))
    caves = ["encounters_oreburgh_gate_1f", "encounters_oreburgh_gate_b1f",
             "encounters_oreburgh_mine_b1f", "encounters_oreburgh_mine_b2f", "encounters_ravaged_path"]
    results.append(("the early caves carry five lines each, with Ian's additions",
                    all(len({s for s in entries[n]["cast"]}) >= 5 for n in caves)
                    and any("SPECIES_NOSEPASS" in entries[n]["cast"] for n in caves)
                    and any("SPECIES_GEODUDE" in entries[n]["cast"] for n in caves)
                    and any("SPECIES_PHANPY" in entries[n]["cast"] for n in caves)
                    and any("SPECIES_MAKUHITA" in entries[n]["cast"] for n in caves), ""))
    per_lint = []
    for n in designed:
        a = model.load_area(n)
        f = lint.lint_table(n, a.slots, entries[n], lint.thresholds_from(sidecar), data=a.data)
        per_lint += [x for x in f if x.severity == "error"]
    results.append(("per-table lint has no errors on any designed table",
                    not per_lint, "; ".join(f"{x.target} {x.rule}" for x in per_lint[:3])))

    # -- the availability plan under the new rules --------------------------
    out = availability.build()
    g = out["gate"]
    results.append(("the plan loads and its gate passes",
                    not out["problems"] and not any(g[k] for k in ("no_source", "corridor_intruders",
                                                                    "early_home_outside", "early_fit")),
                    "; ".join((out["problems"] + g["corridor_intruders"] + g["early_fit"])[:3])))
    rows = {r["name"]: r for r in out["rows"]}
    results.append(("captures are per location and split: Wooloo first in Roark's split, "
                    "Scorbunny first in Gardenia's on Route 204, Squirtle by Old Rod in Roark's",
                    rows["Wooloo"]["first_split"] == "Roark"
                    and rows["Scorbunny"]["first_split"] == "Gardenia"
                    and ("Gardenia", "Route 204") in rows["Scorbunny"]["captures"]
                    and rows["Squirtle"]["first_split"] == "Roark", ""))
    results.append(("a gate-tier starter is tail-only on land and keeps its scripted source",
                    rows["Charmander"]["tail"] == ["encounters_route_207"]
                    and rows["Charmander"]["status"] == "non-wild", ""))
    results.append(("cap candidates are reported, not gated, and name the split and cap",
                    "cap_candidates" in g and all("cap Gardenia 26" in c for c in g["cap_candidates"]),
                    f"{len(g['cap_candidates'])} listed"))
    with open(model.repo_root() + "/" + availability.DOC, encoding="utf-8") as f:
        committed = f.read()
    results.append(("availability.md is exactly what the plan renders",
                    committed == availability.render(out), ""))

    width = max(len(l) for l, _, _ in results)
    failed = 0
    for label, ok, note in results:
        failed += not ok
        print(f"  {'ok  ' if ok else 'FAIL'}  {label:{width}}  {note}")
    print(f"\n{len(results) - failed}/{len(results)} passed")
    return 1 if failed else 0


def _raises(fn):
    try:
        fn()
    except layout.LayoutError:
        return True
    return False


if __name__ == "__main__":
    sys.exit(main())

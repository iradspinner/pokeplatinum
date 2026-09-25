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
                    "Route 205, Oreburgh Gate",
                    set(by.get("Lake Verity", [])) == {"encounters_lake_verity", "encounters_lake_verity_low_water"}
                    and set(by.get("Route 204", [])) == {"encounters_route_204_north", "encounters_route_204_south"}
                    and set(by.get("Oreburgh Gate", [])) == {"encounters_oreburgh_gate_1f", "encounters_oreburgh_gate_b1f"},
                    ""))
    # Mt. Coronet is five captures, not one (Ian, 2026-09-26), by the
    # sidecar's capture_area over the game's single name.
    results.append(("Mt. Coronet is five capture areas: North, South, B1F, Peak and Mountainside",
                    "Mt. Coronet" not in by
                    and by.get("Mt. Coronet North") == ["encounters_mt_coronet_1f_north_room_1"]
                    and set(by.get("Mt. Coronet B1F", [])) == {"encounters_mt_coronet_b1f",
                                                               "encounters_mt_coronet_1f_north_room_2"}
                    and len(by.get("Mt. Coronet Peak", [])) == 7
                    and len(by.get("Mt. Coronet Mountainside", [])) == 2,
                    str(sorted(k for k in by if k.startswith("Mt. Coronet")))))
    # Three tables are built ahead of their maps: no header uses them yet
    # (backlog: the headers, and grass for the two land tables), so each
    # counts as the location its sidecar entry plans for it.
    ahead = {"encounters_verity_lakefront": "Verity Lakefront",
             "encounters_amity_square": "Amity Square",
             "encounters_snowpoint_city": "Snowpoint City"}
    uses = locations.header_uses(root)
    results.append(("Verity Lakefront, Amity Square and Snowpoint City exist, no header uses "
                    "them yet, and each counts as its planned location",
                    all(n in model.area_names() and n not in uses
                        and locations.location(n) == want for n, want in ahead.items()),
                    str({n: locations.location(n) for n in ahead})))

    # -- one-spot groups (Ian, 2026-09-26) ------------------------------------
    t = lint.thresholds_from(sidecar)
    live = [(a.name, a.slots, entries.get(a.name), a.data) for a in model.load_all() if a.land_active]
    results.append(("R15: every same group is identical and every distinct group keeps its "
                    "faces apart and shares little",
                    not lint.lint_groups(live, sidecar, t), ""))
    # Break one Old Chateau room and give a Great Marsh area another's face:
    # R15 has to notice both.
    broken = []
    for name, slots, entry, data in live:
        if name == "encounters_old_chateau_corridor":
            slots = [(slots[1][0], slots[0][1])] + list(slots[1:])
        if name == "encounters_great_marsh_2":
            slots = [("SPECIES_WOOPER", lv) for _, lv in slots]
        broken.append((name, slots, entry, data))
    hits = {f.target for f in lint.lint_groups(broken, sidecar, t)}
    results.append(("R15 catches a room that differs from its group and a part that copies "
                    "another's face",
                    {"encounters_old_chateau_corridor", "encounters_great_marsh_2"} <= hits,
                    str(sorted(hits))))
    groups = progression.group_of(sidecar)
    results.append(("Victory Road's side rooms are post-game and its three floors are not",
                    all(entries["encounters_victory_road_" + s]["split"] == "Post"
                        for s in ("1f_room_1", "1f_room_2", "1f_room_3"))
                    and all(entries["encounters_victory_road_" + s]["split"] == "League"
                            for s in ("1f", "2f", "b1f"))
                    and groups["encounters_victory_road_1f"] == ("Victory Road", "distinct"), ""))

    # -- the top rung (Ian, 2026-09-26) ---------------------------------------
    # Outside Roark's split and the post-game, a max-level lead meets three
    # lines, one at 80%: never a guaranteed manip.
    r16 = [f for name, slots, entry, data in live
           for f in lint.lint_table(name, slots, entry or {}, t, data=data) if f.rule == "R16"]
    tops = [name for name, _, entry, _ in live if lint.uses_top_form(entry)]
    results.append(("every table from Gardenia's split to the League keeps a three-line top rung "
                    "led at 80% (R16)", not r16 and len(tops) > 90, f"{len(tops)} tables, {len(r16)} findings"))
    e201 = entries["encounters_route_201"]
    results.append(("Roark's split keeps its old shapes, since repels are scarce there",
                     not lint.uses_top_form(e201), ""))
    chateau = next(sl for name, sl, _, _ in live if name == "encounters_old_chateau")
    top_lv = max(lv for _, lv in chateau)
    flat = [(sp, lv) for sp, lv in chateau]
    flat[10] = (flat[8][0], top_lv)
    flat[11] = (flat[8][0], top_lv)
    hits = [f for f in lint.lint_table("encounters_old_chateau", flat, entries["encounters_old_chateau"], t)
            if f.rule == "R16"]
    results.append(("R16 catches a top rung that one line fills", bool(hits), ""))

    # -- splits -------------------------------------------------------------
    sp = progression.split_of(sidecar)
    idx = progression.split_index(sidecar)
    results.append(("every sidecar area carries a split, and the split table has the nine gyms "
                    "plus post-game in order",
                    len(sp) == len(entries) and list(idx) == progression.SPLITS, f"{len(sp)}/{len(entries)}"))
    # Ravaged Path moved to Roark's split on Ian's correction of 2026-09-22.
    results.append(("Ian's boundaries: Route 207, both mine floors and Ravaged Path in Roark's split, "
                    "Route 204 north, 211 west and Coronet's first room in Gardenia's, Route 206 later",
                    sp["encounters_route_207"] == "Roark" and sp["encounters_oreburgh_mine_b2f"] == "Roark"
                    and sp["encounters_route_204_south"] == "Roark"
                    and sp["encounters_ravaged_path"] == "Roark" and sp["encounters_route_204_north"] == "Gardenia"
                    and sp["encounters_route_211_west"] == "Gardenia"
                    and sp["encounters_mt_coronet_1f_north_room_1"] == "Gardenia"
                    and idx[sp["encounters_route_206"]] > idx["Gardenia"], ""))
    results.append(("rods arrive by split: Old Rod Roark, Good Rod Maylene, Super Rod Candice; "
                    "Gardenia's cap is 26, the others are Ian's to fill",
                    progression.rod_split(sidecar, "old_rod") == "Roark"
                    and progression.rod_split(sidecar, "good_rod") == "Maylene"
                    and progression.rod_split(sidecar, "super_rod") == "Candice"
                    and progression.cap_of(sidecar, "Gardenia") == 26
                    and progression.cap_of(sidecar, "Post") is None, ""))
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
    results.append(("no designed table puts a species over 35% (Ian's cap), and the first two "
                    "splits stay at or under 30",
                    all(t <= 0.35 + 1e-9 for t in tops.values())
                    and all(t <= 0.30 + 1e-9 for n, t in tops.items() if n in first_two),
                    ", ".join(f"{n.replace('encounters_', '')} {t:.2f}" for n, t in tops.items() if t > 0.35)))
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
    def wild_in(s):
        return {n for n, e in entries.items()
                if s in (e.get("cast") or []) + (e.get("day") or []) + (e.get("night") or [])
                or s in ((e.get("old_rod") or {}).get("cast") or [])}
    starters = {"SPECIES_CHARMANDER", "SPECIES_TREECKO", "SPECIES_TORCHIC", "SPECIES_MUDKIP",
                "SPECIES_SQUIRTLE"}
    results.append(("every classic starter on the list is wild somewhere in the first two splits "
                    "(grass or Old Rod) and none is a home",
                    all(wild_in(s) for s in starters)
                    and not any(r for r in availability.build()["rows"]
                                if r["tier"] == "gate" and r["home"]), ""))
    r204 = entries["encounters_route_204_north"]
    shares = A.merged(model.load_area("encounters_route_204_north").slots)
    # Since the top-rung ruling (2026-09-26) an ordinary line leads, so a
    # manip meets Sewaddle, not a starter, four times in five.
    results.append(("Route 204 north is the delay: Sewaddle leads, Litten at home at 20, Treecko 20, "
                    "Snivy 15, Torchic by day; no Riolu or Eevee",
                    r204["cast"][0] == "SPECIES_SEWADDLE"
                    and abs(shares["SPECIES_LITTEN"] - 0.20) < 1e-9 and abs(shares["SPECIES_TREECKO"] - 0.20) < 1e-9
                    and abs(shares["SPECIES_SNIVY"] - 0.15) < 1e-9 and "SPECIES_TORCHIC" in r204["day"]
                    and not {"SPECIES_RIOLU", "SPECIES_EEVEE"} & set(r204["cast"] + r204["day"] + r204["night"]),
                    ""))
    widths = {n: len(set(e["cast"]) | set(e.get("day") or []) | set(e.get("night") or []))
              for n, e in entries.items() if e.get("cast")}
    # The first two splits are Kaizo-wide; a room in a group (a chateau room,
    # a marsh area, a cave floor) may run five to seven.
    results.append(("Kaizo's width: the first two splits carry 8-16 distinct lines with day and night, "
                    "every designed table 5-16, and at least seven shapes are in use",
                    all(8 <= widths[n] <= 16 for n in first_two)
                    and all(5 <= w <= 16 for w in widths.values())
                    and len({e["archetype"] for e in entries.values() if e.get("cast")}) >= 7,
                    ", ".join(f"{n.replace('encounters_', '')} {w}" for n, w in widths.items() if not 5 <= w <= 16)))
    rods = {n: e["old_rod"]["cast"] for n, e in entries.items() if e.get("old_rod")
            and (e.get("water_split") or e.get("split")) in ("Roark", "Gardenia")}
    results.append(("every Old Rod table in the two splits ends in a starter at 4% or 1%",
                    all(any(s in starters | {"SPECIES_POPPLIO", "SPECIES_FROAKIE"} for s in c[3:])
                        for c in rods.values()) and len(rods) == 14, f"{len(rods)} rod tables"))
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
                    "Litten first in Gardenia's on Route 204, Squirtle by Old Rod in Roark's",
                    rows["Wooloo"]["first_split"] == "Roark"
                    and rows["Litten"]["first_split"] == "Gardenia"
                    and ("Gardenia", "Route 204") in rows["Litten"]["captures"]
                    and rows["Squirtle"]["first_split"] == "Roark", ""))
    results.append(("a gate-tier starter appears as a tail or cameo and keeps its scripted source",
                    "encounters_route_207" in rows["Charmander"]["tail"]
                    and "encounters_route_204_north" in rows["Treecko"]["cameo"]
                    and rows["Charmander"]["status"] == "non-wild", ""))
    results.append(("the caps are Ian's: Roark 16 through League 78, Galactic 64 and Volkner 68",
                    [progression.cap_of(sidecar, s) for s in ("Roark", "Gardenia", "Fantina", "Maylene",
                                                              "Wake", "Byron", "Candice", "Galactic",
                                                              "Volkner", "League")]
                    == [16, 26, 33, 38, 44, 53, 56, 64, 68, 78], ""))
    results.append(("cap candidates are reported, not gated, name the split and cap, and none "
                    "is for the first two splits (those lines are all placed)",
                    "cap_candidates" in g and all(" cap " in c for c in g["cap_candidates"])
                    and not any("cap Roark" in c or "cap Gardenia" in c for c in g["cap_candidates"]),
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

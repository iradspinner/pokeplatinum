"""Authoring plan Step 5, the no-leak pass on everything that is not a land
or water slot: swarms, the Poke Radar, the five dual-slot lists, the honey
tree tiers, the Great Marsh lookout pools, the Trophy Garden's daily
visitor, and the thirteen land tables the game never rolls.

    PYTHONPATH=. python3 -m tools.oxide.encounters.test_step5

Almost read-only: the three writer checks edit one file each and put the
exact text back. They compare against a snapshot taken a moment earlier
rather than against HEAD, because this checkout is shared and a
`git checkout --` would throw away whatever else is uncommitted in that
file, Step 5's own work included.
"""
import contextlib
import io
import json
import os
import subprocess
import sys
import tempfile

from . import audit
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


def changed_lines(before, path):
    """The +/- lines one write produced, from `git diff -U0` between the
    file's text before the write and the file on disk now."""
    full = os.path.join(model.repo_root(), path)
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False,
                                     encoding="utf-8", newline="\n") as f:
        f.write(before)
        snapshot = f.name
    try:
        out = subprocess.run(
            ["git", "diff", "--no-index", "-U0", "--", snapshot, full],
            cwd=model.repo_root(), capture_output=True, text=True).stdout
    finally:
        os.unlink(snapshot)
    lines = out.splitlines()
    add = [l for l in lines if l.startswith("+") and not l.startswith("+++")]
    rem = [l for l in lines if l.startswith("-") and not l.startswith("---")]
    return add, rem


def restore(area, text):
    with open(os.path.join(model.repo_root(), area.path), "w",
              encoding="utf-8", newline="\n") as f:
        f.write(text)


def raises(fn, *args, exc=Exception):
    try:
        fn(*args)
    except exc:
        return True
    except Exception:
        return False
    return False


# -- the writers ------------------------------------------------------------


def check_writers(results):
    # Each case names how to read its slot back out of the reloaded file.
    cases = [
        (model.HONEY_TREE, "set_honey_tier", (8, "uncommon", 2, "SPECIES_ABRA"),
         lambda d: d["tables"][7]["uncommon"][2]),
        (model.GREAT_MARSH_LOOKOUT, "set_marsh_lookout",
         ("after_national_dex", 31, "SPECIES_ABRA"),
         lambda d: d["after_national_dex"][31]),
        (model.TROPHY_GARDEN, "set_daily", (15, "SPECIES_ABRA"),
         lambda d: d[model.DAILY_KEY][15]),
    ]
    landed, read_back = [], []
    for name, writer, args, slot in cases:
        a = model.load_area(name)
        before = a.text
        try:
            getattr(a, writer)(*args)
            a.save()
            add, rem = changed_lines(before, a.path)
            landed.append((writer, len(add), len(rem)))
            read_back.append(slot(model.load_area(name).data) == "SPECIES_ABRA")
        finally:
            restore(a, before)
    results.append(("the honey tier, marsh lookout and daily writers each land on exactly one line",
                    all(n == 1 and m == 1 for _, n, m in landed),
                    ", ".join(f"{w} +{n}/-{m}" for w, n, m in landed)))
    results.append(("what they wrote reads back, and the file is exactly as it was afterwards",
                    all(read_back)
                    and not any(model.load_area(n).text != t for n, t in
                                [(n, model.load_area(n).text) for n, _, _, _ in cases]),
                    ""))

    honey = model.load_area(model.HONEY_TREE)
    marsh = model.load_area(model.GREAT_MARSH_LOOKOUT)
    garden = model.load_area(model.TROPHY_GARDEN)
    refused = [
        raises(honey.set_honey_tier, 1, "common", 6, "SPECIES_ABRA", exc=IndexError),
        raises(honey.set_honey_tier, 9, "common", 0, "SPECIES_ABRA", exc=IndexError),
        raises(honey.set_honey_tier, 1, "rare", 0, "SPECIES_ABRA", exc=ValueError),
        raises(honey.set_honey_levels, 1, 20, 10, exc=ValueError),
        raises(marsh.set_marsh_lookout, "after_national_dex", 32, "SPECIES_ABRA",
               exc=IndexError),
        raises(marsh.set_marsh_lookout, "sometime", 0, "SPECIES_ABRA", exc=ValueError),
        raises(garden.set_daily, 16, "SPECIES_ABRA", exc=IndexError),
        raises(garden.set_daily, -1, "SPECIES_ABRA", exc=IndexError),
    ]
    results.append(("an index past the end of a tier, a pool or the daily list is refused, "
                    "and so is a tier, table, pool or level range that does not exist",
                    all(refused), str(refused)))
    results.append(("the list sizes are declared, not guessed: 6, 32 and 16",
                    model.HONEY_TIER_SIZE == 6
                    and model.LIST_KEY_SIZES["before_national_dex"] == 32
                    and model.LIST_KEY_SIZES[model.DAILY_KEY] == 16, ""))


# -- the audit --------------------------------------------------------------


def check_audit(results):
    out = audit.audit()
    s = out["summary"]
    leaking = {k: d["off"] for k, d in s["by_key"].items() if d["off"]}
    results.append(("every key the game can roll an encounter from is 0 off-list",
                    not leaking and s["off_list_references"] == 0,
                    f"{s['references']} references in {s['files']} files, "
                    f"{s['off_list_references']} off-list"
                    + (f"; leaking: {leaking}" if leaking else "")))
    # The swarm, radar and GBA lists hold nothing since they were turned off
    # (2026-09-26), so they are no longer among the keys the audit reaches.
    expected = {"land_encounters", "day", "night", "surf_encounters", "old_rod_encounters",
                "good_rod_encounters", "super_rod_encounters",
                *model.HONEY_TREE_KEYS, *model.GREAT_MARSH_KEYS, model.DAILY_KEY}
    results.append(("the audit still reaches every live key, so nothing went 0 by "
                    "disappearing",
                    expected <= set(s["by_key"]),
                    ", ".join(sorted(expected - set(s["by_key"])))))
    results.append(("the scripts are reported and left alone: they still name off-list "
                    "species (decision 8)",
                    s["script_references"] > 0 and s["script_off_list"] > 0,
                    f"{s['script_off_list']} of {s['script_references']} off-list"))
    rc, text = run_cli("audit", "--summary", "--fail-on-leak")
    results.append(("`audit --summary --fail-on-leak` now passes",
                    rc == 0, f"exit {rc}"))


# -- what the keys hold -----------------------------------------------------


def check_per_area(results):
    root = model.repo_root()
    listed = audit.on_list(root)
    areas = [a for a in model.load_all() if a.has_land]
    # Swarms, the Poke Radar and the GBA dual slots are turned off in Oxide
    # (Ian, 2026-09-26): the lists keep their shape, since the format and
    # the engine read fixed counts, and every entry is SPECIES_NONE.
    bad_size, held = [], []
    for a in areas:
        for key, size in ((model.SWARM_KEY, 2), (model.RADAR_KEY, 4),
                          *((g, 2) for g in model.DUAL_SLOT_KEYS)):
            vals = a.data.get(key)
            if not isinstance(vals, list) or len(vals) != size:
                bad_size.append((a.name, key))
                continue
            held += [(a.name, key, s) for s in vals if s != "SPECIES_NONE"]
    results.append(("every land file keeps two swarm, four radar and two entries per "
                    "dual-slot game, and every one is empty",
                    not bad_size and not held,
                    f"{len(areas)} files; {len(bad_size)} misshapen, {len(held)} held "
                    + ", ".join(f"{n} {k} {s}" for n, k, s in held[:3])))


def check_inactive(results):
    root = model.repo_root()
    listed = audit.on_list(root)
    sidecar = model.load_sidecar()
    dead = [a for a in model.load_all() if a.has_land and not a.land_active]
    off, levels = [], []
    for a in dead:
        for sp, lv in a.slots:
            if sp not in listed:
                off.append((a.name, sp))
            if lv <= 0:
                levels.append((a.name, lv))
        for layer in ("day", "night"):
            off += [(a.name, s) for s in (a.data.get(layer) or []) if s not in listed]
    results.append(("all thirteen tables the game never rolls (land_rate 0) hold on-list "
                    "species at a real level, day and night included",
                    len(dead) == 13 and not off and not levels,
                    f"{len(dead)} tables; {len(off)} off-list, {len(levels)} at level 0"))
    results.append(("they are the thirteen the sidecar names inactive",
                    sorted(a.name for a in dead) == sorted(sidecar["inactive_areas"]), ""))


def check_species_only(results):
    root = model.repo_root()
    listed = audit.on_list(root)
    with open(os.path.join(root, "docs", "oxide", "encounters",
                           "availability-plan.json"), encoding="utf-8") as f:
        plan = json.load(f)
    honey_plan = plan["honey"]
    tables = model.honey_tree_tables()
    honey = model.honey_tree_species(badges=None)
    results.append(("the honey trees have a table per badge count, 1 to 8, six slots a "
                    "tier and levels that never fall from one table to the next",
                    [t["badges"] for t in tables] == list(range(1, model.HONEY_TABLES + 1))
                    and all(len(t[k]) == model.HONEY_TIER_SIZE
                            for t in tables for k in model.HONEY_TREE_KEYS)
                    and all(a["level_min"] <= b["level_min"] and a["level_max"] <= b["level_max"]
                            for a, b in zip(tables, tables[1:])),
                    ", ".join(f'{t["level_min"]}-{t["level_max"]}' for t in tables)))
    results.append(("the honey tiers are the availability plan's, and the grass starters "
                    "are out of them (Ian, 2026-09-26)",
                    all(set(honey[t]) == set(honey_plan[t]) for t in model.HONEY_TREE_KEYS)
                    and "rare" not in honey_plan
                    and not {"SPECIES_ROWLET", "SPECIES_SNIVY", "SPECIES_SPRIGATITO"}
                    & set(honey["common"] + honey["uncommon"]),
                    ", ".join(f"{t} {len(set(honey[t]))} species"
                              for t in model.HONEY_TREE_KEYS)))

    marsh_lines = set()
    for i in range(1, 7):
        e = sidecar_entry(f"encounters_great_marsh_{i}")
        marsh_lines |= set(e.get("cast") or []) | set(e.get("day") or []) | set(e.get("night") or [])
    marsh_water = {"SPECIES_BARBOACH", "SPECIES_CARVANHA", "SPECIES_FRILLISH"}
    marsh = model.great_marsh_lookout_species()
    stray = {k: sorted(set(v) - marsh_lines - marsh_water) for k, v in marsh.items()}
    results.append(("both lookout pools are 32 long and drawn only from the marsh's own "
                    "lines and its water lines, the post-dex pool the wider of the two",
                    all(len(v) == 32 for v in marsh.values())
                    and not any(stray.values())
                    and len(set(marsh["after_national_dex"]))
                    > len(set(marsh["before_national_dex"])),
                    ", ".join(f"{k} {len(set(v))} lines" for k, v in marsh.items())
                    + ("; stray " + str(stray) if any(stray.values()) else "")))

    garden = sidecar_entry("encounters_trophy_garden")
    cute = {"SPECIES_PICHU", "SPECIES_EEVEE", "SPECIES_TOGEPI", "SPECIES_SKITTY",
            "SPECIES_BUNEARY", "SPECIES_FLABEBE", "SPECIES_MINCCINO",
            "SPECIES_PACHIRISU", "SPECIES_COMBEE", "SPECIES_BOUNSWEET",
            "SPECIES_SMOLIV", "SPECIES_EMOLGA", "SPECIES_GALARIAN_MR_MIME",
            "SPECIES_ROWLET", "SPECIES_SPRIGATITO", "SPECIES_FLETCHLING"}
    allowed = cute | set(garden.get("cast") or []) | set(garden.get("day") or []) \
        | set(garden.get("night") or [])
    daily = model.trophy_garden_daily_species()
    results.append(("Mr. Backlot's garden rotates sixteen distinct on-list species from its "
                    "own cast and the cute lines",
                    len(daily) == 16 and len(set(daily)) == 16
                    and not set(daily) - allowed
                    and not [s for s in daily if s not in listed],
                    ", ".join(sorted(set(daily) - allowed)) or f"{len(set(daily))} distinct"))


_SIDECAR = None


def check_scripted(results):
    """The scripted captures the area list shows (scripted.json): each one
    resolves against the sources catalogue, sits in a known split, and gives
    only pick-list species; and the honey trees are all accounted for."""
    from . import locations
    from . import progression
    from . import scripted
    root = model.repo_root()
    listed = audit.on_list(root)
    try:
        sources = scripted.load(root)
        err = ""
    except ValueError as exc:
        sources, err = [], str(exc)
    splits = set(progression.split_index(model.load_sidecar()))
    results.append(("every scripted source resolves to species in the sources catalogue, "
                    "in a known split, with unique ids",
                    bool(sources) and not err
                    and all(s["pool"] and s["split"] in splits for s in sources)
                    and len({s["id"] for s in sources}) == len(sources),
                    err or f"{len(sources)} sources"))
    off = sorted({sp for s in sources for sp in s["pool"] if sp not in listed})
    results.append(("scripted pools hold only pick-list species",
                    not off, ", ".join(off)))
    wild = locations.by_location(root)
    by_id = {s["id"]: s for s in sources}
    results.append(("an egg has no capture area; the starter and the Eterna gifts share "
                    "their places' tables; Sandgem's clown is a capture of its own",
                    all(s["capture_area"] is None for s in sources if s["kind"] == "egg")
                    and by_id["starter"]["shares_table"]
                    and by_id["eterna_condo"]["shares_table"]
                    and not by_id["sandgem_clown"]["shares_table"]
                    and "Sandgem Town" not in wild, ""))
    trees = scripted.honey_tree_locations(root)
    stems = scripted.honey_tree_stems(root)
    no_table = {loc: n for loc, n in trees.items() if loc not in wild}
    results.append(("all 21 honey trees are placed: on a table's map, on its place's "
                    "first table, or with Floaroma Meadow's gift",
                    sum(trees.values()) == 21
                    and sum(stems.values()) + sum(no_table.values()) == 21
                    and no_table == {"Floaroma Meadow": 1}
                    and any(s["capture_area"] == "Floaroma Meadow" for s in sources),
                    f"{sum(stems.values())} on tables, {no_table}"))


def sidecar_entry(name):
    global _SIDECAR
    if _SIDECAR is None:
        _SIDECAR = model.load_sidecar()["areas"]
    return _SIDECAR.get(name, {})


def main():
    results = []
    for check in (check_writers, check_audit, check_per_area, check_inactive,
                  check_species_only, check_scripted):
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

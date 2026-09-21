"""Authoring plan Step 0: the tooling the pass needs, checked before any table
is written.

    PYTHONPATH=. python3 -m tools.oxide.encounters.test_step0

What it covers, in the plan's order: the writers for swarms, radar and the
dual-slot lists and the readers for the three species-only sources
(model.py); the pick-list name mapping and line bases (dex.py); `cli audit`
and `cli coverage` against the numbers the plan measured; the layout rule
behind `cli apply`, and an apply on a real table that lands only in the
land keys and is restored afterwards; the importer's authored set; and the
M7 source check when a build exists in this checkout.

Every file the checks touch is put back from the text it held a moment
before, the sidecar included. Restoring with `git checkout` would be wrong
here: the checkout is shared, and uncommitted work in the same file is not
this test's to discard.
"""
import contextlib
import importlib.util
import io
import os
import subprocess
import sys

from . import analysis as A
from . import audit
from . import cli
from . import dex
from . import layout
from . import lint
from . import model

AREA = "encounters_route_214"


def git(*args):
    return subprocess.run(["git", *args], cwd=model.repo_root(),
                          capture_output=True, text=True).stdout


def changed_lines(path):
    out = git("diff", "-U0", "--", path).splitlines()
    add = [l for l in out if l.startswith("+") and not l.startswith("+++")]
    rem = [l for l in out if l.startswith("-") and not l.startswith("---")]
    return add, rem


def changed_since(before, path):
    """The +/- lines one write produced: `git diff -U0` between the text the
    file held before the write and the file on disk now, rather than against
    HEAD, so other uncommitted work in the same file is not counted."""
    import tempfile
    full = os.path.join(model.repo_root(), path)
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False,
                                     encoding="utf-8", newline="\n") as f:
        f.write(before)
        snapshot = f.name
    try:
        out = git("diff", "--no-index", "-U0", "--", snapshot, full).splitlines()
    finally:
        os.unlink(snapshot)
    add = [l for l in out if l.startswith("+") and not l.startswith("+++")]
    rem = [l for l in out if l.startswith("-") and not l.startswith("---")]
    return add, rem


def run_cli(*argv):
    """(exit code, stdout) for one cli invocation."""
    out = io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(io.StringIO()):
        try:
            rc = cli.main(list(argv))
        except SystemExit as e:
            rc = e.code
    return rc, out.getvalue()


@contextlib.contextmanager
def sidecar_with(name, **fields):
    """Temporarily rewrite one sidecar entry, restoring the file's exact
    text afterwards."""
    path = model.sidecar_path()
    with open(path, encoding="utf-8") as f:
        original = f.read()
    obj = model.load_sidecar()
    obj["areas"][name] = {**obj["areas"][name], **fields}
    model.save_sidecar(obj)
    try:
        yield
    finally:
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(original)


# -- dex --------------------------------------------------------------------


def check_dex(results):
    root = model.repo_root()
    rows = dex.pick_list(root)
    natives = [r for r in rows if r["status"] == "native"]
    new = [r for r in rows if r["status"] == "new"]
    unresolved = [r["name"] for r in natives if not r["constant"]]
    # 199 natives on Ian's sheet, 220 with the seven cave and fourteen fishing rows of 2026-09-21.
    results.append(("every native on the pick-list resolves to a species in the tree",
                    len(natives) == 220 and not unresolved,
                    f"{len(natives)} natives, unresolved {unresolved[:5]}"))
    # Phase 4 element 3 landed the 159 new species (2026-09-20), so every
    # `new` row must now resolve too; before that this asserted the opposite.
    unported = [r["name"] for r in new if not r["constant"]]
    results.append(("every `new` row resolves (element 3 ported all 159)",
                    len(new) == 159 and not unported, f"{len(new)} new, unresolved {unported[:5]}"))
    results.append(("awkward names map: Nidoran F, Mr. Mime, Farfetch'd, Porygon-Z",
                    dex.constant_of(root, "Nidoran F") == "SPECIES_NIDORAN_F"
                    and dex.constant_of(root, "Mr. Mime") == "SPECIES_MR_MIME"
                    and dex.constant_of(root, "Farfetch'd") == "SPECIES_FARFETCHD"
                    and dex.constant_of(root, "Porygon-Z") == "SPECIES_PORYGON_Z", ""))
    results.append(("constant_of inverts display_name for the whole dex",
                    all(dex.constant_of(root, dex.display_name(s)) == s
                        for s in dex.species_universe(root)), ""))
    eevee = dex.line_base(root, dex.line_of(root, "SPECIES_JOLTEON"))
    starly = dex.line_base(root, dex.line_of(root, "SPECIES_STARAPTOR"))
    results.append(("line_base finds the first stage (Eevee, Starly)",
                    eevee == ["SPECIES_EEVEE"] and starly == ["SPECIES_STARLY"],
                    f"{eevee} {starly}"))


# -- model ------------------------------------------------------------------


def check_model(results):
    # The diff is taken against the file's own text a moment earlier, and the
    # text is written back afterwards. It used to be `git diff` against HEAD
    # and `git checkout --`, which measured every uncommitted change in the
    # file as well as this one and then threw them away; this checkout is
    # shared, so that cost Route 214 its authored table once already.
    path = os.path.join(model.ENC_DIR, AREA + ".json")
    a = model.load_area(AREA)
    before = a.text
    try:
        a.set_swarm(0, "SPECIES_ABRA")
        a.set_radar(3, "SPECIES_ABRA")
        a.set_dual_slot("emerald", 1, "SPECIES_ABRA")
        a.save()
        add, rem = changed_since(before, path)
        results.append(("swarm, radar and dual-slot writers each land on exactly one line",
                        len(add) == 3 and len(rem) == 3
                        and all("SPECIES_ABRA" in l for l in add),
                        f"{len(add)} added, {len(rem)} removed"))
        back = model.load_area(AREA)
        results.append(("the written values read back",
                        back.data["swarms"][0] == "SPECIES_ABRA"
                        and back.data["radar"][3] == "SPECIES_ABRA"
                        and back.data["emerald"][1] == "SPECIES_ABRA", ""))
    finally:
        with open(os.path.join(model.repo_root(), path), "w",
                  encoding="utf-8", newline="\n") as f:
            f.write(before)
    a = model.load_area(AREA)
    bad = []
    for fn, args, exc in ((a.set_swarm, (2, "SPECIES_ABRA"), IndexError),
                          (a.set_radar, (4, "SPECIES_ABRA"), IndexError),
                          (a.set_dual_slot, ("crystal", 0, "SPECIES_ABRA"), ValueError)):
        try:
            fn(*args)
            bad.append(fn.__name__)
        except exc:
            pass
    results.append(("out-of-range index and unknown game are refused", not bad, str(bad)))

    honey = model.honey_tree_species()
    marsh = model.great_marsh_lookout_species()
    daily = model.trophy_garden_daily_species()
    results.append(("readers: honey tree 3x6, marsh lookout 2x32, garden dailies 16",
                    [len(v) for v in honey.values()] == [6, 6, 6]
                    and [len(v) for v in marsh.values()] == [32, 32]
                    and len(daily) == 16
                    and all(s.startswith("SPECIES_") for s in daily), ""))
    refs = model.load_area("encounters_route_201").reference_species()
    results.append(("reference_species lists every key with a species, no SPECIES_NONE",
                    {"land_encounters", "swarms", "day", "night", "radar", "ruby",
                     "leafgreen"} <= set(refs)
                    and "surf_encounters" not in refs
                    and not any("SPECIES_NONE" in v for v in refs.values()),
                    ", ".join(sorted(refs))))
    failures = sum(len(a.rewrite_identity()) for a in model.load_all())
    results.append(("round-trip still clean with the dual-slot lists included",
                    failures == 0, f"{failures} keys"))


# -- audit and coverage -----------------------------------------------------


def check_audit(results):
    out = audit.audit()
    s = out["summary"]
    # The plan measured 2052 live land slots, 1250 off-list, before any table
    # was authored. The slot count is fixed by the format; the off-list count
    # only falls as tables are authored, and an authored table leaks nothing.
    sidecar = model.load_sidecar() or {}
    authored = {n for n, e in (sidecar.get("areas") or {}).items() if e.get("cast")}
    live = [r for r in out["rows"] if r["key"] == "land_encounters" and r["live"]]
    authored_off = sum(1 for r in live if r["file"] in authored and not r["on_list"])
    # 2052 slots before Verity Lakefront's file (2064 with it: twelve per live table).
    n_live = sum(1 for a in model.load_all() if a.land_active)
    results.append(("audit reproduces the plan's live land figures: twelve slots per live table, "
                    "at most 1250 off-list, none of them in an authored table",
                    s["live_land_slots"] == 12 * n_live and s["live_land_slots_off_list"] <= 1250
                    and authored_off == 0,
                    f"{s['live_land_slots']} / {s['live_land_slots_off_list']} off-list, "
                    f"{authored_off} in {len(authored)} authored table(s)"))
    # "natives" in the audit means pick-list species present in the tree: all
    # 358 obtainable rows since element 3 (199 before it), 365 with Ian's
    # three cave lines; the files are every JSON in res/field/encounters.
    n_files = len(model.area_names())
    results.append(("audit sees all 379 pick-list species and every encounter file",
                    s["natives"] == 379 and s["files"] == n_files,
                    f"{s['natives']} natives, {s['files']} files"))
    water = sum(s["by_key"][k]["off"] for k in
                ("surf_encounters", "old_rod_encounters", "good_rod_encounters",
                 "super_rod_encounters"))
    # 641 before any water table was designed; the count only falls.
    results.append(("water and rods carry at most the 641 off-list references of the base ROM",
                    water <= 641, str(water)))
    trio = {(r["script"], r["command"], r["species"]) for r in out["scripts"]}
    results.append(("scripts list the two StartWildBattle species and a legendary",
                    ("scripts_route_209", "StartWildBattle", "SPECIES_SPIRITOMB") in trio
                    and ("scripts_old_chateau_back_middle_west_room", "StartWildBattle",
                         "SPECIES_ROTOM") in trio
                    and any(c == "StartLegendaryBattle" for _, c, _ in trio),
                    f"{len(trio)} commands"))
    rc, text = run_cli("audit", "--summary", "--fail-on-leak")
    # It failed on the base ROM's tables (1250 off-list land slots); since
    # Step 5 every source outside scripts is on-list and it passes.
    results.append(("`audit --fail-on-leak` passes: every source outside scripts is on-list",
                    rc == 0 and "0 are off-list" in text, f"exit {rc}"))


def check_coverage(results):
    out = audit.coverage()
    lines = out["lines"]
    covered = sum(len(r["members"]) for r in lines)
    results.append(("coverage groups all 379 pick-list species into lines, each on one row",
                    covered == 379 and len({m for r in lines for m in r["members"]}) == 379,
                    f"{covered} members over {len(lines)} lines"))
    by = {r["name"]: r for r in lines}
    results.append(("gift, trade, static battle and starter sources are found",
                    any(m == "eterna_city" for m, _, _ in by["Togepi"]["gifts"])
                    and any(n == "foppa_magikarp" for n, _ in by["Magikarp"]["trades"])
                    and any(sp == "SPECIES_DIALGA" for _, _, sp in by["Dialga"]["static"])
                    and by["Turtwig"]["scripted"] and by["Turtwig"]["status"] == "non-wild",
                    ""))
    results.append(("a home needs the first stage at >= 10% of a live land table",
                    all(sh >= audit.HOME_SHARE for r in lines for _, sh in r["home"])
                    and by["Nidoran♀"]["status"] == "home", ""))
    none = [r for r in lines if r["status"] == "none"]
    results.append(("`none` means no source of any kind",
                    all(not (r["home"] or r["cameo"] or r["water"] or r["other"]
                             or r["gifts"] or r["trades"] or r["static"] or r["scripted"])
                        for r in none),
                    ", ".join(r["name"] for r in none)))
    s = out["summary"]
    results.append(("summary counts add up and the new species are listed separately",
                    sum(s["by_status"].values()) == s["native_lines"]
                    and s["new_species"] == 159 == len(out["new"]), str(s["by_status"])))


# -- layout and apply ---------------------------------------------------------


def check_layout(results):
    bad = []
    for name, arch in lint.ARCHETYPES.items():
        cast = [f"SPECIES_X{k}" for k in range(len(arch["signature"]))]
        slots = layout.layout({"archetype": name, "cast": cast, "base_level": 10})
        m = A.table_metrics(slots)
        levels = [lv for _, lv in slots]
        lo, hi = arch["rungs"]
        if (tuple(m["signature"]) != tuple(arch["signature"])
                or any(levels[i] > levels[i + 1] for i in range(11))
                or not lo <= m["rung_count"] <= hi
                or slots[0][0] != cast[0]):
            bad.append(name)
    results.append(("every archetype lays out to its exact signature, monotonic, "
                    "first-listed species on top", not bad, str(bad)))

    entry = {"archetype": "A1", "base_level": 2,
             "cast": [{"species": "SPECIES_STARLY", "rung": 3}, "SPECIES_BIDOOF",
                      "SPECIES_KRICKETOT", "SPECIES_SHINX", "SPECIES_BUDEW"]}
    slots = layout.layout(entry)
    top = max(lv for _, lv in slots)
    on_top = {sp for sp, lv in slots if lv == top}
    share = A.merged(slots)["SPECIES_STARLY"]
    results.append(("a pin puts the 40% face on the top rung too, share unchanged",
                    "SPECIES_STARLY" in on_top and len(on_top) >= 2
                    and abs(share - 0.40) < 1e-9 and slots[0][0] == "SPECIES_STARLY",
                    f"top rung {sorted(on_top)}"))

    wide = (0, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3)
    entry = {"archetype": "A1", "base_level": 5, "ladder": list(wide),
             "cast": [{"species": "SPECIES_STARLY", "rung": 3}, "SPECIES_BIDOOF",
                      "SPECIES_KRICKETOT", "SPECIES_SHINX",
                      {"species": "SPECIES_BUDEW", "rung": 3}]}
    slots = layout.layout(entry)
    levels = [lv for _, lv in slots]
    results.append(("an explicit ladder is honoured and two pins share the widened top rung",
                    levels == [5 + o for o in wide]
                    and {sp for sp, lv in slots if lv == 8} >= {"SPECIES_STARLY", "SPECIES_BUDEW"}
                    and tuple(A.signature(A.merged(slots))) == lint.ARCHETYPES["A1"]["signature"],
                    f"levels {levels}"))
    try:
        layout.layout({"archetype": "A5", "base_level": 5,
                       "cast": [{"species": "SPECIES_S0", "rung": 3}] + [f"SPECIES_S{k}" for k in range(1, 7)]})
        a5_pin = "laid out"
    except layout.LayoutError as e:
        a5_pin = "refused: " + str(e)[:40]
    results.append(("an A5 head pinned to the top rung is refused (its 40 is the two 20s)",
                    a5_pin.startswith("refused"), a5_pin))

    errors = []
    for label, bad_entry in (
            ("cast too short", {"archetype": "A1", "base_level": 5, "cast": ["SPECIES_A"]}),
            ("unknown archetype", {"archetype": "A99", "base_level": 5, "cast": ["SPECIES_A"]}),
            ("pin off the ladder", {"archetype": "A2", "base_level": 5,
                                    "cast": [{"species": "SPECIES_A", "rung": 3}]}),
            ("ladder not monotonic", {"archetype": "A1", "base_level": 5,
                                      "ladder": [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                      "cast": ["SPECIES_A"] * 5})):
        try:
            layout.layout(bad_entry)
            errors.append(label)
        except layout.LayoutError:
            pass
    results.append(("malformed entries raise LayoutError", not errors, str(errors)))


def check_apply(results):
    path = os.path.join(model.ENC_DIR, AREA + ".json")
    cast = ["SPECIES_RHYHORN", "SPECIES_HOUNDOUR", "SPECIES_ZUBAT",
            "SPECIES_GRAVELER", "SPECIES_STUNKY"]
    start = model.load_area(AREA).text
    try:
        with sidecar_with(AREA, archetype="A1", cast=cast, base_level=22,
                          day=["SPECIES_HOUNDOUR", "SPECIES_ZUBAT"]):
            rc, text = run_cli("apply", AREA, "--dry-run")
            add, rem = changed_since(start, path)
            results.append(("`apply --dry-run` prints the diff and writes nothing",
                            rc == 0 and "would change" in text and not add and not rem,
                            f"exit {rc}, {len(add)} lines changed"))
            rc, text = run_cli("apply", AREA)
            add, rem = changed_since(start, path)
            import re
            allowed = re.compile(r'^\+\s*("species": "SPECIES_\w+"|"level": \d+|"SPECIES_\w+"),?$')
            stray = [l for l in add if not allowed.match(l)]
            results.append(("`apply` writes only species, level and day entries",
                            rc == 0 and add and not stray,
                            f"exit {rc}, {len(add)} lines, stray {stray[:2]}"))
            a = model.load_area(AREA)
            m = A.table_metrics(a.slots)
            results.append(("the written table is the A1 signature at base 22 with day slots set",
                            tuple(m["signature"]) == lint.ARCHETYPES["A1"]["signature"]
                            and min(a.levels) == 22
                            and a.data["day"] == ["SPECIES_HOUNDOUR", "SPECIES_ZUBAT"],
                            f"{m['signature']} levels {a.levels}"))
            sidecar = model.load_sidecar()
            findings = lint.lint_table(AREA, a.slots, sidecar["areas"][AREA],
                                       lint.thresholds_from(sidecar), data=a.data)
            rules = {f.rule for f in findings}
            results.append(("the applied table passes R1, R4 and R7",
                            not rules & {"R1", "R4", "R7"}, f"findings {sorted(rules)}"))
            rc, text = run_cli("apply", AREA)
            results.append(("a second apply is a no-op", rc == 0 and "no change" in text, ""))
        with sidecar_with(AREA, archetype="A1", cast=cast, base_level=30,
                          locked=["land_encounters[0]"]):
            before = model.load_area(AREA).text
            rc, _ = run_cli("apply", AREA)
            results.append(("a locked slot the layout would change refuses the apply",
                            rc == 1 and model.load_area(AREA).text == before, f"exit {rc}"))
    finally:
        with open(os.path.join(model.repo_root(), path), "w",
                  encoding="utf-8", newline="\n") as f:
            f.write(start)


# -- importer and verifier ----------------------------------------------------


def load_importer():
    path = os.path.join(model.repo_root(), "tools", "oxide", "import_base_rom.py")
    spec = importlib.util.spec_from_file_location("import_base_rom", path)
    mod = importlib.util.module_from_spec(spec)
    argv, sys.argv = sys.argv, [path]
    try:
        spec.loader.exec_module(mod)
    finally:
        sys.argv = argv
    return mod


def check_importer(results):
    try:
        imp = load_importer()
    except Exception as e:   # the enum loader needs build/generated or generated/
        results.append(("importer loads", False, f"{type(e).__name__}: {e}"))
        return
    base = imp.authored_encounters()
    sidecar = model.load_sidecar() or {}
    with_cast = {n for n, e in (sidecar.get("areas") or {}).items() if e.get("cast")}
    results.append(("AUTHORED is a stem -> reason table; authored_encounters() is it plus "
                    "every sidecar area with a cast",
                    isinstance(imp.AUTHORED, dict)
                    and set(base) == set(imp.AUTHORED) | with_cast,
                    f"{len(base)} authored now, {len(with_cast)} from the sidecar"))
    # Every land table carries a cast since Step 4, so the honey tree (a
    # species-only file with a minimal sidecar entry) is the one to try.
    probe = model.HONEY_TREE
    with sidecar_with(probe, archetype="A1", base_level=22,
                      cast=["SPECIES_RHYHORN"] * 5):
        authored = imp.authored_encounters()
    results.append(("a sidecar entry with a cast is authored by definition",
                    probe in authored and probe not in imp.authored_encounters(), ""))


def check_verify_source(results):
    rom = os.path.join(model.repo_root(), "build", "pokeplatinum.us.nds")
    if not os.path.exists(rom):
        results.append(("verify_narcs --source (no build in this checkout, not run)",
                        True, "M7's own gate ran it; integrate.sh runs it after make rom"))
        return
    out = subprocess.run([sys.executable, "tools/oxide/verify_narcs.py", "--built", rom,
                          "--encounters", "--source"],
                         cwd=model.repo_root(), capture_output=True, text=True)
    results.append(("verify_narcs --encounters --source passes on this checkout's build",
                    out.returncode == 0 and "match their source JSON" in out.stdout,
                    out.stdout.strip().splitlines()[-1][:80] if out.stdout else out.stderr[-80:]))


def main():
    results = []
    for check in (check_dex, check_model, check_audit, check_coverage,
                  check_layout, check_apply, check_importer, check_verify_source):
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

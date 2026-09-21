"""Headless entry points for the encounter tool.

    python3 -m tools.oxide.encounters.cli roundtrip
    python3 -m tools.oxide.encounters.cli areas   [--ref main] [--json]
    python3 -m tools.oxide.encounters.cli show    <area> [--ref main] [--json]
    python3 -m tools.oxide.encounters.cli set     <area> <slot> [--species X] [--level N]
    python3 -m tools.oxide.encounters.cli sidecar-init [--force]

M1 shipped these; `report`, `lint`, `plan` and `generate` arrived with M2,
M3, M5 and M6. The authoring pass (docs/oxide/encounter-authoring-plan.md,
Step 0) added:

    python3 -m tools.oxide.encounters.cli audit    [--summary] [--fail-on-leak] [--json]
    python3 -m tools.oxide.encounters.cli coverage [--status none] [--json]
    python3 -m tools.oxide.encounters.cli apply    <area> | --all  [--dry-run]

and Step 1 added the two one-off writers, each refusing to run twice:

    python3 -m tools.oxide.encounters.cli order-init [--force]
    python3 -m tools.oxide.encounters.cli tier-init  [--rom ~/roms/vanilla.nds] [--force]

and Step 2 the availability plan, read from availability-plan.json:

    python3 -m tools.oxide.encounters.cli availability [--write] [--json]

--ref reads a git ref instead of the working tree. The vanilla corpus is on
`main`; this branch holds the base ROM's rewritten tables.
"""
import argparse
import json
import sys

from . import analysis
from . import lint
from . import model


def _areas(args):
    return model.load_all(args.ref, active_only=not args.all)


def cmd_areas(args):
    rows = []
    for a in _areas(args):
        rows.append({
            "area": a.name,
            "band": a.band,
            "land_rate": a.data.get("land_rate"),
            "species": len({s for s, _ in a.slots}) if a.has_land else 0,
            "levels": (min(a.levels), max(a.levels)) if a.has_land else None,
            "active": a.land_active,
        })
    if args.json:
        json.dump(rows, sys.stdout, indent=2)
        print()
        return 0
    print(f"{'area':44} {'band':6} {'rate':>4} {'sp':>3}  levels")
    for r in rows:
        lv = f"{r['levels'][0]}-{r['levels'][1]}" if r["levels"] else "-"
        print(f"{r['area']:44} {r['band'] or '-':6} {r['land_rate'] or 0:>4} "
              f"{r['species']:>3}  {lv}")
    print(f"\n{len(rows)} areas")
    return 0


def cmd_show(args):
    a = model.load_area(args.area, args.ref)
    if not a.has_land:
        print(f"{a.name} is not a land table", file=sys.stderr)
        return 1
    if args.json:
        json.dump({
            "area": a.name, "band": a.band,
            "land_rate": a.data.get("land_rate"),
            "slots": [{"slot": i, "rate": model.LAND_RATES[i],
                       "species": s, "level": lv}
                      for i, (s, lv) in enumerate(a.slots)],
            "day": a.data.get("day"), "night": a.data.get("night"),
        }, sys.stdout, indent=2)
        print()
        return 0
    print(f"{a.name}   band={a.band}   land_rate={a.data.get('land_rate')}")
    print(f"{'slot':>4} {'rate':>4} {'lvl':>4}  species")
    for i, (s, lv) in enumerate(a.slots):
        print(f"{i:>4} {model.LAND_RATES[i]:>4}% {lv:>4}  {s}")
    for layer in ("day", "night"):
        vals = a.data.get(layer)
        if vals:
            print(f"{layer:>8}: slots {model.DAY_NIGHT_SLOTS} <- "
                  f"{', '.join(vals)}")
    return 0


def cmd_set(args):
    if args.species is None and args.level is None:
        print("nothing to set: pass --species and/or --level", file=sys.stderr)
        return 2
    a = model.load_area(args.area)
    before = a.text
    a.set_slot(args.slot, species=args.species, level=args.level)
    if a.text == before:
        print("no change")
        return 0
    a.save()
    print(f"{a.name} slot {args.slot} -> "
          f"{a.slots[args.slot][0]} lv{a.slots[args.slot][1]}")
    return 0


def cmd_roundtrip(args):
    """The M1 gate. Every land value is replaced with the value it already
    holds; the text must come back byte-identical for all 185 files."""
    areas = model.load_all(args.ref)
    failures = []
    checked = 0
    for a in areas:
        bad = a.rewrite_identity()
        checked += 1
        for path, before, after in bad:
            failures.append((a.name, path, before, after))
    land = sum(1 for a in areas if a.has_land)
    active = sum(1 for a in areas if a.land_active)
    print(f"{checked} files, {land} land tables, {active} with land_rate > 0")
    if not failures:
        print("round-trip clean: every land key re-renders byte-identically")
        return 0
    print(f"\n{len(failures)} key(s) did not survive a rewrite:")
    for name, path, before, after in failures[:20]:
        key = ".".join(str(p) for p in path)
        print(f"  {name}  {key}")
        if args.verbose:
            import difflib
            for line in difflib.unified_diff(
                    before.splitlines(), after.splitlines(),
                    "before", "after", lineterm="", n=1):
                print("    " + line)
    return 1


def cmd_sidecar_init(args):
    existing = model.load_sidecar()
    if existing and not args.force:
        print(f"{model.SIDECAR} already exists; pass --force to rebuild",
              file=sys.stderr)
        return 1
    obj = model.build_sidecar()
    model.save_sidecar(obj)
    print(f"wrote {model.SIDECAR}: {len(obj['areas'])} areas, "
          f"{len(obj['inactive_areas'])} inactive, "
          f"{len(obj['non_land_files'])} non-land files")
    bands = {}
    for e in obj["areas"].values():
        bands[e["band"]] = bands.get(e["band"], 0) + 1
    print("  bands: " + ", ".join(f"{k} {v}" for k, v in sorted(bands.items())))
    return 0


def cmd_report(args):
    """Section 6.5 and 6.6 metrics, for one area or the whole game."""
    if args.area:
        a = model.load_area(args.area, args.ref)
        if not a.has_land:
            print(f"{a.name} is not a land table", file=sys.stderr)
            return 1
        m = analysis.table_metrics(a.slots)
        m["area"], m["band"] = a.name, a.band
        if args.json:
            json.dump(m, sys.stdout, indent=2)
            print()
            return 0
        print(f"{a.name}   band={a.band}   archetype fit: "
              f"{'/'.join(str(int(x)) for x in m['signature'])}")
        print(f"  {m['n_species']} species, top {m['top_share']:.0%}, "
              f"rarest {m['min_share']:.0%}, HHI {m['hhi']:.3f}")
        print(f"  levels {m['level_min']}-{m['level_max']}, "
              f"{m['rung_count']} rungs at {m['rung_levels']}, "
              f"pools {m['pool_sizes']}")
        print(f"  rarest {m['rarest_species']}: "
              f"{m['uplift_on_rarest']:.2f}x"
              + (f" with a level-{m['uplift_at_level']} lead"
                 if m["uplift_at_level"] else " (no repel helps it)"))
        print(f"  best manip {m['best_uplift']:.2f}x on "
              f"{m['best_uplift_species']}"
              + (f" at level {m['best_uplift_at_level']}"
                 if m["best_uplift_at_level"] else ""))
        print("\n  rungs:")
        for level, p in analysis.distinct_rungs(a.slots):
            ranked = sorted(p.items(), key=lambda kv: -kv[1])
            body = ", ".join(f"{sp.replace('SPECIES_', '')} {s:.0%}"
                             for sp, s in ranked)
            print(f"    lead {level:>3}: {body}")
        return 0

    areas = [a for a in model.load_all(args.ref) if a.land_active]
    g = analysis.game_metrics([a.slots for a in areas], [a.band for a in areas])
    if args.json:
        json.dump(g, sys.stdout, indent=2)
        print()
        return 0
    ref = args.ref or "working tree"
    print(f"{g['n_tables']} live land tables   [{ref}]\n")
    print(f"  HHI            median {g['hhi_median']:.3f}   "
          f"p10 {g['hhi_p10']:.3f}   p90 {g['hhi_p90']:.3f}   "
          f"spread {g['hhi_spread']:.2f}x")
    print(f"  signatures     {g['distinct_signatures']} distinct   "
          f"{g['signatures_per_table']:.2f} per table")
    print(f"  table shape    {g['median_species']:.0f} species   "
          f"top {g['median_top_share']:.0%}   "
          f"rarest {g['median_min_share']:.0%}")
    print(f"  repel          best manip median "
          f"{g['best_uplift_median']:.2f}x, works on "
          f"{g['best_uplift_working_frac']:.0%}")
    print(f"                 rarest-species median "
          f"{g['uplift_median']:.2f}x, survives on "
          f"{g['uplift_working_frac']:.0%}")
    print(f"  arc            early {g['hhi_early']:.3f} ({g['n_early']})   "
          f"mid {g['hhi_mid']:.3f} ({g['n_mid']})   "
          f"late {g['hhi_late']:.3f} ({g['n_late']})")
    print(f"  ladder         "
          f"{[round(x) for x in g['ladder']]}")
    print(f"  real tails     {g['real_tail_frac']:.0%} of tables")
    print(f"  binary manips  {g['singleton_rung_frac']:.0%} of rungs "
          f"collapse to one species")
    return 0


def cmd_lint(args):
    """Section 7's rules. `--fail-on error` is what runs before a commit."""
    areas = [a for a in model.load_all(args.ref) if a.land_active]
    sidecar = model.load_sidecar()
    entries = (sidecar or {}).get("areas") or {}
    # The band must come from the sidecar where it is declared, falling back
    # to the table's own median level. Passing None here silently disables
    # every band-aware rule, R11 included, without reporting anything.
    payload = [(a.name, a.slots,
                entries.get(a.name) or {"band": a.band},
                a.data)
               for a in areas]
    # R12 reads the pick-list's tiers and each line's cheapest wild source;
    # None until `tier-init` has written the column, and the rule says so.
    from . import audit
    findings = lint.lint_all(payload, sidecar, audit.availability(args.ref))
    if args.rule:
        wanted = {r.upper() for r in args.rule.split(",")}
        findings = [f for f in findings if f.rule.upper() in wanted]
    if args.ignore:
        dropped = {r.upper() for r in args.ignore.split(",")}
        findings = [f for f in findings if f.rule.upper() not in dropped]
    if args.area:
        findings = [f for f in findings if f.target == args.area]

    if args.json:
        json.dump([f._asdict() for f in findings], sys.stdout, indent=2)
        print()
    else:
        ref = args.ref or "working tree"
        counts = lint.summarise(findings)
        print(f"{len(areas)} live land tables   [{ref}]")
        print(f"{counts['errors']} error(s), {counts['warns']} warning(s), "
              f"{counts['skipped']} skipped\n")
        order = {"error": 0, "warn": 1, "skip": 2}
        shown = sorted(findings, key=lambda f: (order[f.severity], f.rule))
        limit = None if args.all else 40
        for f in shown[:limit]:
            tag = "aspirational" if f.rule in lint.ASPIRATIONAL else ""
            print(f"  {f.severity:5} {f.rule:4} {f.target:38} {f.message}"
                  + (f"  [{tag}]" if tag else ""))
        if limit and len(shown) > limit:
            print(f"  ... {len(shown) - limit} more (pass --all)")
        print("\n  by rule: " + ", ".join(
            f"{k} {v}" for k, v in sorted(counts["by_rule"].items())))

    if args.fail_on == "error":
        return 1 if any(f.severity == "error" for f in findings) else 0
    if args.fail_on == "warn":
        return 1 if any(f.severity in ("error", "warn") for f in findings) else 0
    return 0


def cmd_plan(args):
    """The dupe-out planner: what to catch first, and where, so that the one
    counting encounter on the target table is the species wanted."""
    from . import dex, planner
    from .server import KIND_LABELS, State, _area_label
    st = State(args.ref)
    areas, line_of, members_of = planner.plan_inputs(args.ref)
    species = args.species if args.species.startswith("SPECIES_") \
        else "SPECIES_" + args.species.upper()
    if not any(a["name"] == args.area for a in areas):
        print(f"no live table called {args.area}", file=sys.stderr)
        return 1
    out = planner.plan(args.area, species, args.kind, areas, st.owned,
                       line_of, members_of)
    out["lines"] = planner.describe(out, dex.display_name, _area_label,
                                    KIND_LABELS)
    if args.json:
        json.dump(out, sys.stdout, indent=2)
        print()
        return 0
    print(f"{_area_label(args.area)}, {KIND_LABELS[args.kind].lower()}: "
          f"how to make the counting encounter {dex.display_name(species)}")
    print(f"  {len(out['removable_lines'])} lines could be duped out first; "
          f"{out['n_candidates']} plans considered, "
          f"{len(out['front'])} worth showing\n")
    for i, line in enumerate(out["lines"], 1):
        print(f"  {i}. {line}\n")
    return 0


def cmd_generate(args):
    """Levels-only: choose each slot's level so the repel ladder under the
    species already placed pays. Species stay where Ian put them. Writes one
    key per changed slot, or with --dry-run just shows the proposal."""
    from . import generate
    sidecar = model.load_sidecar()
    entries = (sidecar or {}).get("areas") or {}
    t = lint.thresholds_from(sidecar)
    live = [a for a in model.load_all() if a.land_active]
    if args.area:
        areas = [a for a in live if a.name == args.area]
        if not areas:
            print(f"no live table called {args.area}", file=sys.stderr)
            return 1
    elif args.band:
        areas = [a for a in live
                 if (entries.get(a.name) or {}).get("band", a.band) == args.band]
    else:
        print("say which: --area NAME or --band early|mid|late", file=sys.stderr)
        return 2

    proposals = [generate.propose(a, entries.get(a.name), t, span=args.span,
                                  base=args.base, aim=args.aim) for a in areas]
    if args.json:
        json.dump(proposals, sys.stdout, indent=2)
        print()
        return 0

    touched = 0
    for a, p in zip(areas, proposals):
        label = a.name.replace("encounters_", "")
        if not p["deltas"]:
            print(f"{label:34} already best: {p['uplift']:.2f}x, "
                  f"{p['rungs']} rungs")
            continue
        print(f"{label:34} {p['uplift_before']:.2f}x -> {p['uplift']:.2f}x, "
              f"{p['rungs_before']} -> {p['rungs']} rungs, "
              f"{len(p['deltas'])} slot(s)"
              + (f", violations {p['violations']}" if p["violations"] else "")
              + (f", locked {p['locked']}" if p["locked"] else ""))
        for i, was, now in p["deltas"]:
            sp = a.slots[i][0].replace("SPECIES_", "").title()
            print(f"    slot {i:>2} {sp:<12} lv {was:>2} -> {now}")
        if not args.dry_run:
            for i, _, now in p["deltas"]:
                a.set_slot(i, level=now)
            a.save()
            touched += 1
    changed = sum(1 for p in proposals if p["deltas"])
    dropped = sum(1 for p in proposals
                  if p["uplift"] < p["uplift_before"] - 1e-9)
    print(f"\n{len(areas)} table(s), {changed} changed"
          + (f" ({dropped} pay less than before because the old ladder broke "
             f"R1, levels must not fall with slot index)" if dropped else "")
          + (f", {touched} written" if not args.dry_run else ", nothing written"))
    return 0


def cmd_audit(args):
    """The leak table: every species reference in every encounter source,
    flagged on-list or off-list, plus the scripts that give or battle one.
    `--fail-on-leak` is Step 5's zero check."""
    from . import audit
    out = audit.audit(args.ref)
    s = out["summary"]
    if args.json:
        s = dict(s)
        s["by_key"] = {k: dict(v) for k, v in s["by_key"].items()}
        json.dump({"summary": s, "rows": out["rows"], "scripts": out["scripts"]},
                  sys.stdout, indent=2)
        print()
    else:
        ref = args.ref or "working tree"
        print(f"leak audit   [{ref}]   pick-list natives: {s['natives']}\n")
        print(f"  {s['references']} species references in {s['files']} files; "
              f"{s['off_list_references']} are off-list, "
              f"in {s['files_with_leak']} files")
        print(f"  {s['distinct_species']} distinct species referenced, "
              f"{s['distinct_off_list']} off-list")
        print(f"  live land slots {s['live_land_slots']}, "
              f"off-list {s['live_land_slots_off_list']}")
        print(f"  natives in no live land table {s['natives_in_no_live_land_table']}, "
              f"in no encounter source at all {s['natives_in_no_source']}")
        print(f"\n  {'key':24} {'refs':>5} {'off':>5} {'species':>8}")
        for key, d in s["by_key"].items():
            print(f"  {key:24} {d['refs']:>5} {d['off']:>5} {d['off_species']:>8}")
        if not args.summary:
            print("\n  off-list references by file:")
            by_file = {}
            for r in out["rows"]:
                if not r["on_list"]:
                    by_file.setdefault(r["file"], {}).setdefault(r["key"], []).append(
                        r["species"].replace("SPECIES_", ""))
            for name in sorted(by_file):
                print(f"    {name}")
                for key, sps in by_file[name].items():
                    counted = sorted({f"{sp}x{sps.count(sp)}" if sps.count(sp) > 1 else sp
                                      for sp in sps})
                    print(f"      {key:24} {', '.join(counted)}")
        print(f"\n  scripts: {s['script_references']} give/battle commands name a "
              f"species, {s['script_off_list']} off-list"
              + (" (reported, not changed: decision 8)" if s["script_off_list"] else ""))
        for r in out["scripts"]:
            flag = "" if r["on_list"] else "  OFF-LIST"
            print(f"    {r['script']:44} {r['command']:26} "
                  f"{r['species'].replace('SPECIES_', '')}{flag}")
    if args.fail_on_leak and s["off_list_references"]:
        return 1
    return 0


def cmd_coverage(args):
    """For every line on the pick-list, where it is obtainable. R12's input
    made visible; Step 2 writes the availability plan from it."""
    from . import audit
    out = audit.coverage(args.ref)
    s = out["summary"]
    if args.json:
        json.dump(out, sys.stdout, indent=2)
        print()
        return 0
    ref = args.ref or "working tree"
    print(f"availability coverage   [{ref}]\n")
    print(f"  {s['native_lines']} lines: "
          + ", ".join(f"{k} {v}" for k, v in sorted(s["by_status"].items()))
          + (f"; {s['not_in_tree']} pick-list rows not in the tree yet"
             if s.get("not_in_tree") else
             f"; every pick-list row is in the tree ({s['new_species']} new species)"))
    rows = out["lines"]
    if args.status:
        rows = [r for r in rows if r["status"] == args.status]
    print(f"\n  {'line':14} {'tier':10} {'status':11} sources")
    for r in rows:
        parts = []
        if r["home"]:
            parts.append("home " + ", ".join(
                f"{a.replace('encounters_', '')} {sh:.0%}" for a, sh in r["home"][:3])
                + (f" +{len(r['home']) - 3}" if len(r["home"]) > 3 else ""))
        if r["cameo"]:
            parts.append(f"cameo x{len(r['cameo'])}")
        if r["water"]:
            parts.append(f"water x{len(r['water'])}")
        if r["other"]:
            keys = sorted({k for _, k, _ in r["other"]})
            parts.append("other " + "/".join(keys))
        if r["gifts"]:
            parts.append("gift " + ", ".join(m for m, _, _ in r["gifts"][:2]))
        if r["trades"]:
            parts.append("trade " + ", ".join(n for n, _ in r["trades"]))
        if r["static"]:
            parts.append("static " + ", ".join(
                s.replace("scripts_", "") for s, _, _ in r["static"][:2]))
        if r["scripted"]:
            parts.append(", ".join(how for how, _ in r["scripted"]))
        print(f"  {r['name']:14} {r['tier'] or '-':10} {r['status']:11} "
              f"{'; '.join(parts) or '-'}")
    return 0


def cmd_apply(args):
    """Materialise an area's land table from its sidecar entry (authoring
    plan decision 4). The archetype fixes the shares, the cast fills them,
    the ladder fixes the levels; every write goes through model.py."""
    import difflib
    from . import layout
    sidecar = model.load_sidecar()
    entries = (sidecar or {}).get("areas") or {}
    if args.all:
        names = [n for n, e in entries.items() if e.get("cast")]
        if not names:
            print("no sidecar entry has a cast yet", file=sys.stderr)
            return 1
    elif args.area:
        names = [args.area]
    else:
        print("say which: AREA or --all", file=sys.stderr)
        return 2

    failed = written = 0
    for name in names:
        entry = entries.get(name)
        if entry is None:
            print(f"{name}: no sidecar entry", file=sys.stderr)
            failed += 1
            continue
        if not entry.get("cast"):
            print(f"{name}: sidecar entry has no cast", file=sys.stderr)
            failed += 1
            continue
        try:
            slots = layout.layout(entry)
        except layout.LayoutError as e:
            print(f"{name}: {e}", file=sys.stderr)
            failed += 1
            continue
        a = model.load_area(name)
        if not a.has_land:
            print(f"{name}: not a land table", file=sys.stderr)
            failed += 1
            continue
        # A locked slot is Ian's hand-placed decision (design doc 3.2). The
        # layout must reproduce it, or the entry is contradicting itself.
        clash = []
        for spec in entry.get("locked") or []:
            m = spec if isinstance(spec, int) else None
            if m is None:
                digits = "".join(ch for ch in str(spec) if ch.isdigit())
                m = int(digits) if digits else None
            if m is not None and 0 <= m < len(slots) and slots[m] != a.slots[m]:
                clash.append(m)
        if clash:
            print(f"{name}: layout would change locked slot(s) {clash}; "
                  f"express the lock as a cast pin instead", file=sys.stderr)
            failed += 1
            continue
        before = a.text
        for i, (sp, lv) in enumerate(slots):
            cur_sp, cur_lv = a.slots[i]
            a.set_slot(i, species=sp if sp != cur_sp else None,
                       level=lv if lv != cur_lv else None)
        if entry.get("land_rate") is not None \
                and entry["land_rate"] != a.data.get("land_rate"):
            a.set_land_rate(entry["land_rate"])
        for layer in ("day", "night"):
            want = entry.get(layer)
            if want:
                for i, sp in enumerate(want):
                    if (a.data.get(layer) or [None, None])[i] != sp:
                        a.set_time_slot(layer, i, sp)
        label = name.replace("encounters_", "")
        print(f"{label}: {entry['archetype']} at base {entry['base_level']}, "
              + "; ".join(layout.describe(slots)))
        if a.text == before:
            print("  already laid out, no change")
            continue
        diff = list(difflib.unified_diff(
            before.splitlines(), a.text.splitlines(), name, name, lineterm="", n=0))
        changed = sum(1 for l in diff if l.startswith("+") and not l.startswith("+++"))
        if args.dry_run:
            for l in diff[2:]:
                print("  " + l)
            print(f"  dry run: {changed} value(s) would change, nothing written")
        else:
            a.save()
            written += 1
            print(f"  wrote {changed} value(s)")
    print(f"\n{len(names)} area(s), {written} written, {failed} failed"
          + (" (dry run)" if args.dry_run else ""))
    return 1 if failed else 0


def cmd_order_init(args):
    """Write the progression `order` onto every sidecar area from the
    default in progression.py (authoring plan decision 6). Run once; after
    that the sidecar is the source and Ian edits it there. Also seeds the
    R12 ceilings into the sidecar's thresholds so they are visible to edit."""
    from . import progression
    sidecar = model.load_sidecar()
    if sidecar is None:
        print(f"{model.SIDECAR} does not exist; run sidecar-init first", file=sys.stderr)
        return 1
    have = [n for n, e in sidecar["areas"].items() if e.get("order") is not None]
    if have and not args.force:
        print(f"{len(have)} areas already carry an order; pass --force to overwrite "
              f"Ian's edits with the default", file=sys.stderr)
        return 1
    names = model.area_names()
    missing = progression.write_order(sidecar, names)
    extra = sorted(set(progression.default_order()) - set(names))
    sidecar.setdefault("thresholds", {}).setdefault(
        "r12_max_cost", lint.DEFAULT_THRESHOLDS["r12_max_cost"])
    model.save_sidecar(sidecar)
    print(f"wrote order for {len(names) - len(missing)} of {len(names)} areas")
    if missing:
        print(f"  no default order for: {', '.join(missing)}")
    if extra:
        print(f"  default names no file: {', '.join(extra)}")
    return 1 if missing or extra else 0


def cmd_tier_init(args):
    """Write the pick-list's `tier` column from the defaults in tiers.py
    (authoring plan decision 7). Run once; Ian edits the CSV afterwards."""
    from . import dex, tiers
    rows = dex.pick_list(model.repo_root())
    if any(r.get("tier") for r in rows) and not args.force:
        print("the pick-list already has tiers; pass --force to overwrite Ian's "
              "edits with the defaults", file=sys.stderr)
        return 1
    tier = tiers.defaults(args.rom, args.ref or "main")
    n = tiers.write_column(tier)
    counts = {}
    for t in tier.values():
        counts[t] = counts.get(t, 0) + 1
    print(f"wrote tier for {n} rows: "
          + ", ".join(f"{k} {counts[k]}" for k in tiers.TIERS if k in counts))
    return 0


def cmd_availability(args):
    """Step 2: the availability plan, per line, from availability-plan.json
    and the tree; --write renders docs/oxide/encounters/availability.md.
    Exit 1 when the step's gate fails."""
    from . import availability
    out = availability.build(args.ref)
    g, s = out["gate"], out["summary"]
    if args.json:
        json.dump({"summary": dict(s), "gate": g, "problems": out["problems"],
                   "rows": out["rows"]}, sys.stdout, indent=2)
        print()
    else:
        print(f"availability plan   [{args.ref or 'working tree'}]")
        print("  " + ", ".join(f"{k} {s[k]}" for k in availability.STATUSES if s.get(k)))
        for key, label in (("no_source", "no source"),
                           ("corridor_intruders", "corridor intruders"),
                           ("early_home_outside", "starter-adjacent home outside corridor"),
                           ("early_fit", "early tables outside 3-5"),
                           ("unplanned_tables", "tables with nothing planned (warning)")):
            print(f"  {label:42} {len(g[key])}"
                  + (f": {', '.join(g[key][:6])}" + (" ..." if len(g[key]) > 6 else "")
                     if g[key] else ""))
        for p in out["problems"]:
            print(f"  problem: {p}")
        if args.write:
            print(f"  wrote {availability.write(out)}")
    failed = out["problems"] or any(g[k] for k in ("no_source", "corridor_intruders",
                                                    "early_home_outside", "early_fit"))
    return 1 if failed else 0


def cmd_later(args):
    print(f"'{args.command}' arrives with a later milestone; see "
          f"docs/oxide/encounter-tool-build-plan.md", file=sys.stderr)
    return 2


def main(argv=None):
    p = argparse.ArgumentParser(prog="encounters")
    p.add_argument("--ref", default=None,
                   help="read from a git ref instead of the working tree "
                        "(the vanilla corpus is on 'main')")
    sub = p.add_subparsers(dest="command", required=True)

    a = sub.add_parser("areas", help="list areas")
    a.add_argument("--all", action="store_true",
                   help="include land_rate 0 and non-land files")
    a.add_argument("--json", action="store_true")
    a.set_defaults(func=cmd_areas)

    s = sub.add_parser("show", help="print one table")
    s.add_argument("area")
    s.add_argument("--json", action="store_true")
    s.set_defaults(func=cmd_show)

    w = sub.add_parser("set", help="rewrite one land slot")
    w.add_argument("area")
    w.add_argument("slot", type=int)
    w.add_argument("--species")
    w.add_argument("--level", type=int)
    w.set_defaults(func=cmd_set)

    r = sub.add_parser("roundtrip", help="the M1 gate")
    r.add_argument("--verbose", action="store_true")
    r.set_defaults(func=cmd_roundtrip)

    c = sub.add_parser("sidecar-init", help="write docs/oxide/encounters/design.json")
    c.add_argument("--force", action="store_true")
    c.set_defaults(func=cmd_sidecar_init)

    rep = sub.add_parser("report", help="section 6 metrics")
    rep.add_argument("area", nargs="?")
    rep.add_argument("--json", action="store_true")
    rep.set_defaults(func=cmd_report)

    ln = sub.add_parser("lint", help="section 7's rules")
    ln.add_argument("area", nargs="?")
    ln.add_argument("--rule", help="comma-separated rule ids, e.g. R8,R9")
    ln.add_argument("--ignore", help="comma-separated rule ids to drop, e.g. R12 "
                                     "when linting vanilla, which was never built "
                                     "for the pick-list")
    ln.add_argument("--fail-on", choices=("error", "warn"), default=None)
    ln.add_argument("--all", action="store_true", help="do not truncate")
    ln.add_argument("--json", action="store_true")
    ln.set_defaults(func=cmd_lint)

    pl = sub.add_parser("plan", help="the dupe-out planner")
    pl.add_argument("area")
    pl.add_argument("species", help="SPECIES_GIBLE or just gible")
    pl.add_argument("--kind", default="land",
                    choices=("land", "surf", "old_rod", "good_rod", "super_rod"))
    pl.add_argument("--json", action="store_true")
    pl.set_defaults(func=cmd_plan)

    ge = sub.add_parser("generate",
                        help="levels-only: build the repel ladder under the "
                             "species already placed")
    ge.add_argument("--area")
    ge.add_argument("--band", choices=("early", "mid", "late"))
    ge.add_argument("--dry-run", action="store_true",
                    help="show the proposal, write nothing")
    ge.add_argument("--aim", type=float, default=None,
                    help="uplift to reach on the rarest species (default: "
                         "the R3 threshold); higher isolates harder")
    ge.add_argument("--span", type=int, default=3,
                    help="levels above base to use (default 3, four rungs)")
    ge.add_argument("--base", type=int, default=None,
                    help="bottom level (default: the sidecar's base_level, "
                         "else the table's current minimum)")
    ge.add_argument("--json", action="store_true")
    ge.set_defaults(func=cmd_generate)

    au = sub.add_parser("audit", help="every species reference, on-list or off-list")
    au.add_argument("--summary", action="store_true", help="numbers only, no leak table")
    au.add_argument("--fail-on-leak", action="store_true",
                    help="exit 1 if any encounter source names an off-list species")
    au.add_argument("--json", action="store_true")
    au.set_defaults(func=cmd_audit)

    cov = sub.add_parser("coverage", help="where every pick-list line is obtainable")
    cov.add_argument("--status", choices=("home", "non-wild", "water-only",
                                          "cameo-only", "other-only", "none"),
                     help="show only lines in this state")
    cov.add_argument("--json", action="store_true")
    cov.set_defaults(func=cmd_coverage)

    ap = sub.add_parser("apply", help="lay a table out from its sidecar entry")
    ap.add_argument("area", nargs="?")
    ap.add_argument("--all", action="store_true", help="every area with a cast")
    ap.add_argument("--dry-run", action="store_true", help="print the diff, write nothing")
    ap.set_defaults(func=cmd_apply)

    oi = sub.add_parser("order-init", help="write the default progression order "
                                          "into the sidecar (once)")
    oi.add_argument("--force", action="store_true")
    oi.set_defaults(func=cmd_order_init)

    ti = sub.add_parser("tier-init", help="write the default tier column onto the "
                                         "pick-list (once)")
    ti.add_argument("--rom", default="~/roms/vanilla.nds",
                    help="a Platinum ROM, for the Sinnoh dex table")
    ti.add_argument("--force", action="store_true")
    ti.set_defaults(func=cmd_tier_init)

    av = sub.add_parser("availability", help="Step 2: the per-line availability plan "
                                              "and its gate")
    av.add_argument("--write", action="store_true",
                    help="render docs/oxide/encounters/availability.md")
    av.add_argument("--json", action="store_true")
    av.set_defaults(func=cmd_availability)

    args = p.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())

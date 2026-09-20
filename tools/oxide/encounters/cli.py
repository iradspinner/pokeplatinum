"""Headless entry points for the encounter tool.

    python3 -m tools.oxide.encounters.cli roundtrip
    python3 -m tools.oxide.encounters.cli areas   [--ref main] [--json]
    python3 -m tools.oxide.encounters.cli show    <area> [--ref main] [--json]
    python3 -m tools.oxide.encounters.cli set     <area> <slot> [--species X] [--level N]
    python3 -m tools.oxide.encounters.cli sidecar-init [--force]

M1 shipped these; `report`, `lint`, `plan` and `generate` arrived with M2,
M3, M5 and M6.

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
    findings = lint.lint_all(payload, sidecar)
    if args.rule:
        wanted = {r.upper() for r in args.rule.split(",")}
        findings = [f for f in findings if f.rule.upper() in wanted]
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

    args = p.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())

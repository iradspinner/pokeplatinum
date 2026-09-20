"""Headless entry points for the encounter tool.

    python3 -m tools.oxide.encounters.cli roundtrip
    python3 -m tools.oxide.encounters.cli areas   [--ref main] [--json]
    python3 -m tools.oxide.encounters.cli show    <area> [--ref main] [--json]
    python3 -m tools.oxide.encounters.cli set     <area> <slot> [--species X] [--level N]
    python3 -m tools.oxide.encounters.cli sidecar-init [--force]

M1 ships these. `report`, `lint`, `plan` and `generate` arrive with M2, M3,
M5 and M6; they are declared here so the surface is visible from the start.

--ref reads a git ref instead of the working tree. The vanilla corpus is on
`main`; this branch holds the base ROM's rewritten tables.
"""
import argparse
import json
import sys

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

    for name in ("report", "lint", "plan", "generate"):
        later = sub.add_parser(name, help="not yet built")
        later.set_defaults(func=cmd_later)

    args = p.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())

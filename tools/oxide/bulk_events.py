#!/usr/bin/env python3
"""Rewrite every remaining changed map's events from the base ROM, in bulk.

Platinum Oxide project. import_base_rom.py's events pass only takes maps where
the edit stands alone; this takes the rest, including the ones that gain or lose
events, by writing the whole json from the base ROM's record.

New object events need an `id`, because that is what generates the LOCALID_*
constants scripts use. Existing ids are kept so nothing already referenced moves;
anything new gets LOCALID_OBJECT_<n>, which is honest about being generated and
can be renamed once someone reads what the object is for.

Usage:
    python3 tools/oxide/bulk_events.py [--dry-run]

Run from the repository root.
"""
import argparse
import json
import os
import sys

ROOT = os.getcwd()
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import import_base_rom as imp  # noqa: E402
import jsonstyle  # noqa: E402


def render(record, existing, index):
    """One object event as the repo spells it, keeping the existing id."""
    out = {}
    if index < len(existing) and "id" in existing[index]:
        out["id"] = existing[index]["id"]
    else:
        out["id"] = f"LOCALID_OBJECT_{index}"
    for key, value in record.items():
        if key == "hidden_flag":
            prior = existing[index].get("hidden_flag") if index < len(existing) else None
            value = imp.render_var_or_header(value, prior)
        out[key] = value
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default=os.path.expanduser("~/roms/base.nds"))
    ap.add_argument("--vanilla", default=os.path.expanduser("~/roms/vanilla.nds"))
    ap.add_argument("--built", default="build/pokeplatinum.us.nds")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    base, van = imp.Rom(a.base), imp.Rom(a.vanilla)
    be, ve = base.narc(imp.EVENTS_NARC), van.narc(imp.EVENTS_NARC)
    already = set()
    if os.path.isfile(a.built):
        built = imp.Rom(a.built).narc(imp.EVENTS_NARC)
        already = {i for i in range(min(len(built), len(be)))
                   if bytes(built[i]) == bytes(be[i])}

    written, skipped = 0, []
    for i in range(len(be)):
        if bytes(be[i]) == bytes(ve[i]) or i in already:
            continue
        path = imp.events_json(i)
        if path is None:
            skipped.append(f"events member {i}: no json in res/")
            continue
        current = json.load(open(path, encoding="utf-8"))
        decoded = imp.decode_events(be[i])
        out = {
            "bg_events": decoded["bg_events"],
            "object_events": [
                render(rec, current.get("object_events", []), n)
                for n, rec in enumerate(decoded["object_events"])
            ],
            "warp_events": decoded["warp_events"],
            "coord_events": [
                {**rec, "var": imp.render_var_or_header(
                    rec["var"],
                    current["coord_events"][n].get("var") if n < len(current.get("coord_events", [])) else None)}
                for n, rec in enumerate(decoded["coord_events"])
            ],
        }
        if not a.dry_run:
            jsonstyle.dump_file(out, path)
        written += 1

    print(f"{'would write' if a.dry_run else 'wrote'} {written} event files; {len(skipped)} skipped")
    for line in skipped[:10]:
        print("  " + line)


if __name__ == "__main__":
    main()

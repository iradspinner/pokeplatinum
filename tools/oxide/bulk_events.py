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

# Event files that deliberately gained events the base ROM does not have, and
# must not be rewritten from it. Each already carries every base ROM edit to
# its existing events; rewriting would keep those and drop the additions.
DIVERGED = {
    "events_victory_road_1f": "the level 71 Lucas and Dawn fight at the start of "
                              "Victory Road adds the counterpart and a trigger "
                              "(docs/oxide/battle-zone-plan.md)",
    "events_pastoria_city_north_house": "the clown the base ROM added moved to the "
                                        "Restaurant with its gift (Ian, 2026-09-25)",
}
# The gift clowns the base ROM added are gone (Ian, 2026-09-27).
DIVERGED.update({
    f"events_{m}": "the gift clown the base ROM added removed (Ian, 2026-09-27)"
    for m in ("sandgem_town_house", "jubilife_city_south_house_1f", "oreburgh_city_middle_house",
              "floaroma_town_middle_house", "floaroma_meadow_house", "eterna_city_condominiums_1f",
              "solaceon_town_northeast_house", "veilstone_city_northeast_house",
              "canalave_library_2f")
})
# The teleporting Abra the base ROM added are hidden behind FLAG_HIDE_TELEPORT_ABRA,
# town teleporters and dungeon shortcuts alike; the gym shortcuts stay (Ian,
# 2026-09-27; docs/oxide/pocket-pc.md).
DIVERGED.update({
    f"events_{m}": "the teleporting Abra the base ROM added is hidden (Ian, 2026-09-27)"
    for m in (
    "canalave_city",
    "celestic_town",
    "eterna_city",
    "fight_area",
    "floaroma_town",
    "hearthome_city",
    "jubilife_city",
    "mt_coronet_6f",
    "mt_coronet_outside_north",
    "mt_coronet_outside_south",
    "oreburgh_city",
    "pastoria_city",
    "pokemon_league",
    "resort_area",
    "route_207",
    "route_221",
    "route_224",
    "sandgem_town",
    "snowpoint_city",
    "solaceon_town",
    "stark_mountain_outside",
    "stark_mountain_room_2",
    "sunyshore_city",
    "survival_area",
    "turnback_cave_entrance",
    "turnback_cave_giratina_room",
    "twinleaf_town",
    "veilstone_city",
    )
})
# The base ROM's free evolution stones are gone (Ian, 2026-09-27): Galactic HQ
# B2F loses the nine stone balls appended to the end of its object list.
DIVERGED["events_galactic_hq_b2f"] = (
    "the nine evolution stone balls the base ROM added removed (Ian, 2026-09-27)")


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
        stem = os.path.basename(path)[:-len(".json")]
        if stem in DIVERGED:
            skipped.append(f"{stem}: deliberately diverged, left alone ({DIVERGED[stem]})")
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

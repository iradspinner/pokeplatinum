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
                              "(docs/oxide/battle-zone-plan.md); then the gauntlet "
                              "line between its two halves, three coord events "
                              "(docs/oxide/gauntlets.md)",
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
# Ian's approved stone plan (2026-09-27, from the balance track's stone census):
# thirteen stone finds go, and the Oreburgh Mine B2F ball the base ROM added
# holds an Everstone rather than an Old Amber.
for _m, _why in (
    ("fuego_ironworks_building", "its Fire Stone ball removed"),
    ("stark_mountain_room_2", "its hidden Fire Stone removed"),
    ("route_230", "its hidden Water Stone removed"),
    ("resort_area", "its copy of Route 229's hidden Thunder Stone removed"),
    ("route_229", "its hidden Thunder Stone removed"),
    ("great_marsh_3", "its hidden Leaf Stone removed"),
    ("route_225", "its hidden Leaf Stone and its Dawn Stone ball removed"),
    ("route_211_west", "its copy of Eterna City's hidden Moon Stone removed"),
    ("mt_coronet_4f_rooms_1_and_2", "its hidden Sun Stone removed"),
    ("route_210_north", "its hidden Shiny Stone removed"),
    ("oreburgh_mine_b2f", "the base ROM's Old Amber ball holds an Everstone"),
):
    _why += " (Ian's stone plan, 2026-09-27)"
    DIVERGED[f"events_{_m}"] = (DIVERGED[f"events_{_m}"] + "; then " + _why
                                if f"events_{_m}" in DIVERGED else _why)
# Two base ROM item balls hid behind daily flags, so they came back every day
# (the Overseer's ruling, 2026-09-27). The Secret Key becomes a one-time find;
# the Old Amber goes, since Ian deleted it (2026-09-21), and the two fossil
# balls whose swapped explicit local ids would then collide lose them.
DIVERGED["events_galactic_hq_b2f"] += (
    "; then the Secret Key ball given a one-time flag of its own in place of a daily one")
DIVERGED["events_stark_mountain_room_2"] += (
    "; then the base ROM's Old Amber ball removed (Ian deleted the Old Amber, 2026-09-21)")
# The base ROM's Helix, Dome and Claw Fossil balls go too, under the same
# ruling (Ian, 2026-09-21: those fossils and anything that hands them out).
for _m in ("oreburgh_mine_b2f", "stark_mountain_room_2"):
    DIVERGED[f"events_{_m}"] += (
        "; then the base ROM's Helix, Dome and Claw Fossil balls removed (Ian, 2026-09-21)")
# The fossils that stay are one-time finds on flags of their own, all three in
# Oreburgh Mine B2F, so Stark Mountain room 2 loses its Root Fossil (Ian, 2026-09-27).
DIVERGED["events_oreburgh_mine_b2f"] += (
    "; then the Root, Armor and Skull Fossil balls each given a one-time flag of its own "
    "(Ian, 2026-09-27)")
DIVERGED["events_stark_mountain_room_2"] += (
    "; then its Root Fossil ball removed, the Root Fossil being Oreburgh Mine B2F's "
    "(Ian, 2026-09-27)")
# The Game Corner's challenger, an optional trainer beside the coins clerk
# whose win gives the TM she gave for ten straight bonus rounds (Ian,
# 2026-10-06).
_why = "the optional trainer Rocco added beside the coins clerk (Ian, 2026-10-06)"
DIVERGED["events_stark_mountain_outside"] += (
    "; the Life Orb ball gives a PP Up instead (visible item script 7051), since the player "
    "never gets a Life Orb (Ian, 2026-09-27 and 2026-10-13); its flag keeps its old name")
DIVERGED["events_game_corner"] = (
    DIVERGED["events_game_corner"] + "; " + _why if "events_game_corner" in DIVERGED else _why)
# The reward table (step 10 of docs/oxide/alpha-readiness.md, applied
# 2026-10-07 by tools/oxide/place_rewards.py) put its items in these maps'
# balls; regenerating would bring back the base ROM's.
_why = "item balls the reward table changed (2026-10-07)"
for _m in ("jubilife_city", "mt_coronet_2f", "stark_mountain_room_1"):
    DIVERGED[f"events_{_m}"] = (DIVERGED[f"events_{_m}"] + "; " + _why
                                if f"events_{_m}" in DIVERGED else _why)
# Two of the items the table gained later (Ian, 2026-10-13); the third, the
# Ability Patch, is a trainer reward in scripts_battles.
for _m, _why in (
    ("wayward_cave_1f", "its Revive ball holds the one Ice Stone (visible item script 7472; "
                        "Ian, 2026-10-13)"),
    ("pastoria_city", "an Ability Capsule ball at the end of the strip between the southwest "
                      "ponds (visible item script 7473; Ian, 2026-10-13), removed again when the "
                      "Capsule became the Pokemon Mansion's knockout prize (Ian, 2026-10-31)"),
):
    DIVERGED[f"events_{_m}"] = (DIVERGED[f"events_{_m}"] + "; " + _why
                                if f"events_{_m}" in DIVERGED else _why)
# Solaceon's "Utility Stop" vendors are gone (Ian, 2026-10-07; bulk_scripts.py
# says why), so the north house's events are vanilla's again.
DIVERGED["events_solaceon_town_north_house"] = (
    "the Utility Stop's three vendors removed, so the events are vanilla's (Ian, 2026-10-07)")
DIVERGED["events_survival_area_south_house"] = (
    "the second Utility Stop's greeter and three vendors removed; the Black Belt stays "
    "where the base ROM moved him (2026-10-07)")
# Ian asked on 2026-10-29 for about a dozen mandatory fights in each of
# Fantina's and Maylene's splits, so trainers the player could walk around
# were moved or re-aimed onto the story path (docs/oxide/mandatory-fights.md
# lists each one); regenerating would put them back where they can be skipped.
_why = "trainers moved onto the story path to make them mandatory (Ian, 2026-10-29)"
for _m in ("route_207", "route_208", "route_209", "route_210_south", "route_215"):
    DIVERGED[f"events_{_m}"] = (DIVERGED[f"events_{_m}"] + "; " + _why
                                if f"events_{_m}" in DIVERGED else _why)
# The two warehouse grunts of the Veilstone tag battle are Officers Tyche and
# Hermes (Ian, 2026-10-29), so the north one, Tyche, wears the female grunt's
# sprite; regenerating would dress her as a male grunt again.
DIVERGED["events_veilstone_city"] += (
    "; then the north warehouse grunt, Officer Tyche, given the female grunt's sprite "
    "(Ian, 2026-10-29)")
# The same day Ian asked for 8 in Roark's split and 12 or more in Gardenia's
# (docs/oxide/mandatory-fights-early.md). Fishermen Andrew and Joseph left
# Route 205 North's piers for the banks at both ends of Route 205 South's
# bridge, so the one map loses them and the other gains them.
_why = "trainers moved onto the story path to make them mandatory (Ian, 2026-10-29)"
for _m in ("route_203", "oreburgh_gate_1f", "oreburgh_mine_b2f", "route_204_south",
           "route_204_north", "eterna_forest", "route_205_south", "route_205_north"):
    DIVERGED[f"events_{_m}"] = (DIVERGED[f"events_{_m}"] + "; then " + _why
                                if f"events_{_m}" in DIVERGED else _why)

# Wake's split (docs/oxide/wake-split.md): three of Route 213's land trainers
# stand at its chokepoints, Fisherman Travis leaves Route 212 South's bridge for
# Route 213's neck by the grass, and Gentleman Jeremy and Socialite Reina leave
# Route 212 North for Valor Lakefront's two narrows, so those maps lose them and
# the others gain them (2026-10-31). On Route 214, with Ian's yes the same day,
# Psychic Abigail looks only west, Psychic Mitchell stands looking south, and PI
# Carlos stands at the narrows south of the berry field, looking west.
for _m in ("route_213", "valor_lakefront", "route_212_north", "route_212_south", "route_214"):
    DIVERGED[f"events_{_m}"] = (DIVERGED[f"events_{_m}"] + "; then " + _why
                                if f"events_{_m}" in DIVERGED else _why)

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

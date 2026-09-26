#!/usr/bin/env python3
"""Regenerate every changed field script from the base ROM, in bulk.

Platinum Oxide project. The per-map carry-over reads each script and rewrites it
in the repo's idiom, which is the better source but is slow. This does the whole
remaining set at once instead, by emitting each changed script straight from the
base ROM's bytecode with `scriptdis.emit_source`.

What that costs, stated plainly so nobody is surprised by it later: the output
has machine labels (`JubilifeCity_0A4C`) and numeric operands where a
hand-written file would use named labels, `NPCMessage`, and text-bank constants.
It is byte-exact, because the emitter round-trips all 574 files in both ROMs,
but it is not the readable decomp source the repo otherwise keeps, and it
replaces hand-written upstream source in the files it touches. Those versions
stay in git history, and every generated file says at the top that it was
generated, so they can be re-humanised a map at a time later.

Usage:
    python3 tools/oxide/bulk_scripts.py [--dry-run] [--limit N]

Run from the repository root.
"""
import argparse
import os
import sys

ROOT = os.getcwd()
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import scriptdis as sd  # noqa: E402
import import_base_rom as imp  # noqa: E402

# Scripts that deliberately no longer match the base ROM, and must not be
# regenerated from it. Without this the restart check-list quietly undoes a fix:
# the tool's whole job is to make the build match the base ROM again.
DIVERGED = {
    "scripts_common": "uses SetRepelSteps instead of the base ROM's scratch-address "
                      "poke plus repurposed Dummy088; regenerating would reintroduce "
                      "the Repel prompt defect (Phase 3 hard stop 3)",
    "scripts_init_battleground": "the base ROM's member is the terminator byte followed "
                                 "by 53 bytes of unreachable leftovers; this builds the "
                                 "4-byte equivalent, which the engine reads identically",
}

# The scripted gifts. Each of these hands out a pool of species, and the
# encounter authoring pass re-pooled every one of them onto the species
# pick-list (Ian, 2026-09-21): a gift is a capture area in a town that has no
# grass, so its pool is designed the way a table is. Every one of them is also
# flag-guarded now, where the base ROM let them repeat. Regenerating any of them
# from the base ROM would put the off-list species back and drop the guard.
DIVERGED.update({
    stem: "gift pool re-pooled onto pick-list species and flag-guarded by the "
          "encounter pass (docs/oxide/encounters/scripted-sources.md)"
    for stem in (
        "scripts_pokemon_day_care",
        # Not a gift: the Oreburgh trade, which takes any Pokemon now that the
        # two lines comparing your choice against a species are gone.
        "scripts_oreburgh_city_north_house_1f",
        "scripts_sandgem_town_house",
        "scripts_jubilife_city_south_house_1f",
        "scripts_unused_jubilife_city_south_house_3f",
        "scripts_oreburgh_city_middle_house",
        "scripts_floaroma_town_middle_house",
        "scripts_floaroma_meadow_house",
        "scripts_eterna_city_condominiums_1f",
        "scripts_hearthome_city_pokemon_fan_club",
        "scripts_solaceon_town_northeast_house",
        "scripts_veilstone_city_northeast_house",
        "scripts_pastoria_city_north_house",
        "scripts_canalave_library_2f",
    )
})

# Test.nds, the base ROM since 2026-09-25 (exported 2026-08-31), changed six
# of these after the encounter pass took them over. Five only reorder the
# same gifts, rolling first and giving after; Sandgem turns its pick menu into
# a random roll, which Oxide's version already does. So Oxide's versions stay.
for _stem in ("scripts_jubilife_city_south_house_1f", "scripts_eterna_city_condominiums_1f",
              "scripts_pastoria_city_north_house", "scripts_veilstone_city_northeast_house",
              "scripts_floaroma_meadow_house"):
    DIVERGED[_stem] += ("; Test.nds (2026-08-31) changed it only by reordering the same "
                        "gifts, which this version already gives")
DIVERGED["scripts_sandgem_town_house"] += (
    "; Test.nds (2026-08-31) turned its pick menu into a random roll, which this "
    "version already does")

# Valley Windworks' balloon Drifloon, a scripted battle before the second gym,
# is gone (Ian, 2026-09-26): the object never shows and its battle entry only
# ends, so Drifloon is met in the wild. Regenerating would bring the battle back.
DIVERGED["scripts_valley_windworks_outside"] = (
    "the Drifloon balloon battle removed by the encounter pass; Drifloon is wild "
    "(docs/oxide/encounters/scripted-sources.md)")

# Riley's egg is rolled from eight species rather than always Riolu (Ian,
# 2026-09-26). This map is upstream's, not generated, so it would otherwise
# look like a file the base ROM should overwrite.
DIVERGED["scripts_iron_island_b2f_left_room"] = (
    "Riley's egg made random by the encounter pass "
    "(docs/oxide/encounters/scripted-sources.md)")

BANNER = """@ Generated by tools/oxide/bulk_scripts.py from the base ROM's bytecode.
@ Byte-exact but machine-shaped: labels are offsets and operands are mostly
@ numbers. Rewrite in the repo's idiom when this map gets proper attention.
"""


def prefix_for(stem):
    return "".join(part.capitalize() for part in stem.split("_"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default=os.path.expanduser("~/roms/base.nds"))
    ap.add_argument("--vanilla", default=os.path.expanduser("~/roms/vanilla.nds"))
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--limit", type=int)
    ap.add_argument("--built", default="build/pokeplatinum.us.nds",
                    help="skip scripts this build already gets right, so maps "
                         "already carried over by hand keep their idiomatic source")
    a = ap.parse_args()

    base, van = imp.Rom(a.base), imp.Rom(a.vanilla)
    already = set()
    if os.path.isfile(a.built):
        built = imp.Rom(a.built).narc(sd.SCRIPTS_NARC)
        ref = base.narc(sd.SCRIPTS_NARC)
        already = {i for i in range(min(len(built), len(ref)))
                   if bytes(built[i]) == bytes(ref[i])}
    bs, vs = base.narc(sd.SCRIPTS_NARC), van.narc(sd.SCRIPTS_NARC)
    order = [l.strip() for l in open(os.path.join(ROOT, "res/field/scripts/scripts.order")) if l.strip()]

    sd.use_base_rom_table(True)
    written, skipped, failed = 0, [], []
    for i in range(len(bs)):
        if bytes(bs[i]) == bytes(vs[i]):
            continue
        if i in already:
            continue  # this build already matches the base ROM here
        if i >= len(order):
            skipped.append(f"member {i}: not in scripts.order")
            continue
        stem = order[i]
        path = os.path.join(ROOT, "res", "field", "scripts", stem + ".s")
        if not os.path.isfile(path):
            skipped.append(f"{stem}: no .s in res/")
            continue
        # the diverged reason first: it is the more useful one to read
        if stem in DIVERGED:
            skipped.append(f"{stem}: deliberately diverged, left alone ({DIVERGED[stem]})")
            continue
        if sd.is_init_script(stem):
            skipped.append(f"{stem}: init script, different format")
            continue
        try:
            body = sd.emit_source(bs[i], prefix_for(stem[len("scripts_"):]))
        except Exception as exc:
            failed.append(f"{stem}: {exc}")
            continue
        text = BANNER + body
        if not a.dry_run:
            with open(path, "w", encoding="utf-8", newline="\n") as f:
                f.write(text)
        written += 1
        if a.limit and written >= a.limit:
            break

    print(f"{'would write' if a.dry_run else 'wrote'} {written} script files; "
          f"{len(skipped)} skipped, {len(failed)} failed")
    for line in (skipped + failed)[:12]:
        print("  " + line)


if __name__ == "__main__":
    main()

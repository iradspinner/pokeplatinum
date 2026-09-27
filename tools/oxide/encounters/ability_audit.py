"""Which obtainable Pokemon carry an ability Oxide rules out or cannot use.

    PYTHONPATH=. python3 -m tools.oxide.encounters.ability_audit            # print it
    PYTHONPATH=. python3 -m tools.oxide.encounters.ability_audit --write    # the doc

The starting list for the ability pass (Ian, 2026-09-27, through the
Overseer), written to docs/oxide/encounters/ability-audit.md. Two lists:

- a weather-setting or weather-cancelling ability in a regular slot, which
  Ian's standing rule of 2026-09-26 allows only as a hidden ability, reached
  through the game's single Ability Patch;
- an ability that does nothing because terrain is not in the game
  (src/battle/battle_lib.c: "terrain is not ported").

A species counts as obtainable when a table the game rolls, a honey tree or
a live scripted source (scripted.json) gives it, or when it evolves from one
that is. Each row names the split it is first obtainable in and how. The doc
is a snapshot: the ability pass changes these abilities, and this reruns.
Nothing here changes game data.
"""
import argparse
import collections
import datetime
import json
import os
import sys

from . import audit
from . import dex
from . import locations
from . import model
from . import pokedex
from . import progression
from . import scripted

DOC = os.path.join("docs", "oxide", "encounters", "ability-audit.md")

# What each ability does that Oxide has no use for.
WEATHER = {
    "DRIZZLE": "sets rain", "DROUGHT": "sets sun", "SAND_STREAM": "sets a sandstorm",
    "SNOW_WARNING": "sets snow", "SAND_SPIT": "sets a sandstorm when hit",
    "ORICHALCUM_PULSE": "sets sun", "PRIMORDIAL_SEA": "sets heavy rain",
    "DESOLATE_LAND": "sets harsh sun", "DELTA_STREAM": "sets strong winds",
    "CLOUD_NINE": "cancels weather", "AIR_LOCK": "cancels weather",
    "TERAFORM_ZERO": "cancels weather and terrain",
}
TERRAIN = {
    "ELECTRIC_SURGE": "sets Electric Terrain", "PSYCHIC_SURGE": "sets Psychic Terrain",
    "MISTY_SURGE": "sets Misty Terrain", "GRASSY_SURGE": "sets Grassy Terrain",
    "SEED_SOWER": "sets Grassy Terrain when hit",
    "SURGE_SURFER": "doubles Speed on Electric Terrain",
    "GRASS_PELT": "raises Defense on Grassy Terrain",
    "MIMICRY": "takes the terrain's type",
    "QUARK_DRIVE": "boosts a stat on Electric Terrain or with Booster Energy, "
                   "which Oxide does not have",
    "HADRON_ENGINE": "sets Electric Terrain and powers up on it",
}
LAND_HOW = {"land": "grass", "land by day": "grass by day", "land at night": "grass at night"}
WATER_HOW = {"surf": "Surf", "old_rod": "Old Rod", "good_rod": "Good Rod", "super_rod": "Super Rod"}


def _abilities(root, species):
    """(slot 1, slot 2, hidden) from the species record, NONE as None."""
    path = os.path.join(root, "res", "pokemon", pokedex.folder_of(species), "data.json")
    try:
        with open(path, encoding="utf-8") as f:
            abilities = json.load(f).get("abilities") or []
    except FileNotFoundError:
        abilities = []
    a = [(x.replace("ABILITY_", "") if x and x != "ABILITY_NONE" else None)
         for x in (abilities + [None] * 3)[:3]]
    return a[0], a[1], a[2]


def direct_sources(root):
    """{species: [(split index, split, place, how)]} for every way a species
    is met as itself: a table's grass, time of day or water, a honey tree, or
    a live scripted source."""
    side = model.load_sidecar()
    entries = side.get("areas") or {}
    idx = progression.split_index(side)
    places = locations.location_of(root)
    out = collections.defaultdict(list)

    def add(sp, split, place, how):
        if sp and sp.startswith("SPECIES_") and split in idx:
            out[sp].append((idx[split], split, place, how))
    for area in model.load_all():
        entry = entries.get(area.name) or {}
        split = entry.get("split")
        place = places.get(area.name) or area.name
        for kind in area.kinds_present():
            if kind == "land":
                if not area.land_active:
                    continue
                for sp, _ in area.slots:
                    add(sp, split, place, "grass")
                for layer, how in (("day", "grass by day"), ("night", "grass at night")):
                    for sp in area.data.get(layer) or []:
                        add(sp, split, place, how)
                continue
            s = entry.get("water_split") or split
            rod = progression.rod_split(side, kind)
            if rod and (s not in idx or idx.get(rod, 99) > idx[s]):
                s = rod
            for sp, _, _ in area.kind_slots(kind):
                add(sp, s, place, WATER_HOW.get(kind, kind))
    # Honey trees read one table per badge count, from the first split with a tree.
    tables = model.honey_tree_tables()
    for split in progression.SPLITS:
        table = scripted.honey_table_for(split, idx, tables)
        if not table:
            continue
        for tier in ("common", "uncommon"):
            for sp in table.get(tier) or []:
                add(sp, split, "a honey tree", "honey tree")
    acuity_split = None
    for src in scripted.load(root):
        if src["id"] == "acuity_cavern":
            acuity_split = src.get("split")
        if not src.get("simulate", True):
            continue
        how = src.get("kind", "scripted") + (", planned, not yet scripted"
                                             if src.get("planned") else "")
        if len(src.get("pool") or []) > 1 and src.get("pick") != "choice":
            how += f", one of {len(src['pool'])} at random"
        for sp in src.get("pool") or []:
            add(sp, src.get("split"), src.get("label") or src.get("capture_area") or src["id"], how)
    # The roamer is drawn from its third of the legendary pool at a new game
    # and released at Lake Verity once the lake Pokemon are free; no script
    # names it, so scripted.json has no source for it. It is placed in the
    # Acuity draw's split, the same pool's static.
    # Held back since 2026-09-27 (audit.empty_thirds), when it has no species.
    pool = audit.pool_block(root)
    roamers = [] if "roamer" in audit.empty_thirds(pool) else \
        (pool.get("thirds") or {}).get("roamer") or []
    for sp in roamers:
        add(sp, acuity_split, "Lake Verity's roamer",
            f"roamer, one of {len(roamers)} at random (split as the Acuity draw's)")
    return out


def _earlier(root, species):
    """{earlier stage: the evolution into `species`}, from the dex's records."""
    out = {}
    dex.lines(root)
    for prev, into in (dex._CACHE.get("evolves_into") or {}).items():
        if species in into:
            evos = (pokedex.load(root, prev) or {}).get("evolutions") or []
            e = next((e for e in evos if e.get("into") == species), None)
            out[prev] = e
    return out


PLACE_METHODS = {"LEVEL_MOSS_ROCK": "by the Moss Rock", "LEVEL_ICE_ROCK": "by the Ice Rock",
                 "LEVEL_MAGNETIC_FIELD": "in Mt. Coronet's magnetic field",
                 "LEVEL_KNOW_MOVE": "knowing a set move", "LEVEL_BEAUTY": "with high Beauty"}


def _method(e):
    """An evolution's requirement, in words."""
    if not e:
        return "evolving"
    method = e.get("method") or ""
    item = e["item"].replace("_", " ").title().replace("Kings Rock", "King's Rock") \
        if e.get("item") else None
    if e.get("level"):
        return f"level {e['level']}"
    if item:
        return f"holding a {item}" if "HELD" in method else f"a {item}"
    if e.get("partner"):
        return f"with {dex.display_name(e['partner'])} in the party"
    return PLACE_METHODS.get(method, method.replace("_", " ").lower())


def first_obtainable(root, species, direct, seen=None):
    """(split index, split, place, how) for the earliest way to get `species`:
    as itself, or by evolving the stage the earliest source gives, the chain
    named in `how` ("grass, as Larvitar; Pupitar at level 30, then Tyranitar
    at level 55"). None when it is out of reach."""
    seen = seen or set()
    own = min(direct.get(species) or [], default=None)
    best = (own[0], own[1], own[2], own[3], []) if own else None
    for prev, e in _earlier(root, species).items():
        if prev in seen:
            continue
        got = first_obtainable(root, prev, direct, seen | {species})
        if got and (best is None or got[0] < best[0]):
            chain = got[4] or [(dex.display_name(prev), None)]
            best = (got[0], got[1], got[2], got[3],
                    chain + [(dex.display_name(species), _method(e))])
    return best


def _how(got):
    """The source, and the evolutions after it, in words."""
    how = got[3]
    chain = got[4]
    if not chain:
        return how
    first, rest = chain[0][0], chain[1:]
    steps = ", then ".join(f"{name} by {method}" for name, method in rest)
    return f"{how}, as {first}; {steps}"


def rows(root=None):
    root = root or model.repo_root()
    from . import audit
    listed = audit.on_list(root)
    direct = direct_sources(root)
    weather, terrain, hidden_weather, unreachable = [], [], [], []
    for sp in sorted(listed):
        a1, a2, hidden = _abilities(root, sp)
        slots = []
        if a1:
            slots.append(("both slots" if a2 in (None, a1) else "slot 1", a1))
        if a2 and a2 != a1:
            slots.append(("slot 2", a2))
        found_w = [(s, a) for s, a in slots if a in WEATHER]
        found_t = [(s, a) for s, a in slots if a in TERRAIN]
        if hidden in TERRAIN:
            found_t.append(("hidden", hidden))
        if not (found_w or found_t or hidden in WEATHER):
            continue
        got = first_obtainable(root, sp, direct)
        name = dex.display_name(sp)
        for slot, ab in found_w:
            row = (name, slot, ab, got)
            (weather if got else unreachable).append(row)
        for slot, ab in found_t:
            row = (name, slot, ab, got)
            (terrain if got else unreachable).append(row)
        if hidden in WEATHER and got:
            hidden_weather.append((name, "hidden", hidden, got))
    def key(r):
        return (r[3][0] if r[3] else 99, r[0])
    return {"weather": sorted(weather, key=key), "terrain": sorted(terrain, key=key),
            "hidden_weather": sorted(hidden_weather, key=key),
            "unreachable": sorted(unreachable, key=key)}


def _table(rs, what):
    if not rs:
        return "None.\n"
    lines = ["| Species | Slot | Ability | What it does | First split | How |",
             "|---|---|---|---|---|---|"]
    for name, slot, ab, got in rs:
        lines.append(f"| {name} | {slot} | {ab.replace('_', ' ').title()} | {what[ab]} | "
                     f"{got[1] if got else ''} | {(got[2] + ': ' + _how(got)) if got else ''} |")
    return "\n".join(lines) + "\n"


def render(out, today=None):
    today = today or datetime.date.today().isoformat()
    un = out["unreachable"]
    return (
        "# Ability audit for the ability pass\n\n"
        f"A snapshot of {today}, from `tools/oxide/encounters/ability_audit.py`, "
        "which reruns it. It lists every Pokemon the player can obtain (on the "
        "species pick-list, and given by a table, a honey tree or a live scripted "
        "source, or evolved from one that is) whose abilities Oxide rules out or "
        "cannot use. Nothing here changes game data; the ability pass decides the "
        "replacements. The split is the first one the species can be had in, and "
        "the place is where; an evolved stage names the stage it comes from.\n\n"
        "The first list is the weather abilities in a regular slot. Ian's standing "
        "rule (2026-09-26) keeps weather out of the player's hands, allowing a "
        "weather ability only as a hidden one, which the game's single Ability "
        "Patch reaches.\n\n"
        + _table(out["weather"], WEATHER) +
        "\nThe second list is the abilities that do nothing, because terrain is not "
        "in the game (`src/battle/battle_lib.c`). A hidden slot is listed too, "
        "since the Ability Patch can give it.\n\n"
        + _table(out["terrain"], TERRAIN) +
        "\nFor reference, the obtainable species whose hidden ability sets or "
        "cancels weather. The rule allows these, and lint R18 keeps any script "
        "from handing one out.\n\n"
        + _table(out["hidden_weather"], WEATHER) +
        ("\nFlagged species with no way to obtain them now (held back, or with no "
         "source), left out of the lists above:\n\n" + _table(un, {**WEATHER, **TERRAIN})
         if un else "")
    )


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--write", action="store_true", help=f"write {DOC}")
    a = p.parse_args(argv)
    root = model.repo_root()
    text = render(rows(root))
    if a.write:
        with open(os.path.join(root, DOC), "w", encoding="utf-8", newline="\n") as f:
            f.write(text)
        print(f"wrote {DOC}")
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())

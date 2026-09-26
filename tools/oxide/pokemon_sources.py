#!/usr/bin/env python3
"""Catalogue every non-standard way a Pokemon can be obtained or met.

"Non-standard" means anything that is not an ordinary grass/cave land slot:
the starter, gift scripts, eggs, in-game trades, fossils, scripted static and
legendary battles, roamers, swarms, Poke Radar slots, the dual-slot GBA lists,
honey trees, the Great Marsh daily rotation, the Trophy Garden dailies, the
Feebas tile pool, the Unown rooms, Pal Park and Day Care breeding.

Everything is read from this tree; nothing comes from a wiki.

  res/field/encounters/*.json      swarm / radar / dual-slot / daily / rod keys
  res/field/encounters/encounters_honey_tree.json
  res/field/encounters/encounters_great_marsh_lookout.json
  res/field/scripts/*.s            gives, eggs, static battles, trade hookups
  res/npc_trades/*.json            what each trade NPC hands over and wants
  include/data/map_headers.h       map -> script/encounter archive -> location
  res/text/location_names.json     the in-game name of each location
  src/overlay005/honey_tree.c      which maps have a honey tree
  src/overlay006/swarm.c           which maps can hold a swarm
  src/overlay006/wild_encounters.c which land slots each key overwrites
  src/roaming_pokemon.c            the roamer slots, their species and levels
  src/scrcmd_fossil.c              fossil item -> species
  src/choose_starter/...           the three starter options
  docs/oxide/pokemon-gifts.csv     the gift survey (for the vanilla/new flag)
  docs/oxide/species-pick-list.csv via tools/oxide/encounters/dex.py

`git show main:<path>` is vanilla, so each row's origin is decided by asking
whether main's copy of the same file carries the same value.

Run from the repo root:

    PYTHONPATH=. python3 tools/oxide/pokemon_sources.py

It writes docs/oxide/pokemon-sources.csv and docs/oxide/pokemon-sources.md and
changes nothing else.
"""
import collections
import csv
import datetime
import glob
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)

from tools.oxide.encounters import dex  # noqa: E402

ENC_DIR = os.path.join("res", "field", "encounters")
SCRIPT_DIR = os.path.join("res", "field", "scripts")

HONEY_TREE = "encounters_honey_tree"
MARSH_POOL = "encounters_great_marsh_lookout"

# Which land slots each replacement key overwrites, from
# src/overlay006/wild_encounters.c (and great_marsh_binoculars.c).
SLOTS = {
    "swarms": (0, 1),
    "day": (2, 3),
    "night": (2, 3),
    "radar": (4, 5, 10, 11),
    "trophy_garden": (6, 7),
    "great_marsh": (6, 7),
    "dual_slot": (8, 9),
}

DUAL_SLOT_GAMES = {
    "ruby": "Ruby", "sapphire": "Sapphire", "emerald": "Emerald",
    "firered": "FireRed", "leafgreen": "LeafGreen",
}

# src/overlay006/wild_encounters.c, WildEncounters_UnownTables. The json's
# unown_table value is the index plus one.
UNOWN_TABLES = [
    "A B C G H J K L M O P Q S T U V W X Y Z",
    "F", "R", "I", "N", "E", "D", "! ?",
]


def run(args):
    return subprocess.run(args, cwd=ROOT, capture_output=True, text=True)


def vanilla_text(path):
    """main's copy of a file, or None when main does not have it."""
    r = run(["git", "show", "main:" + path])
    return r.stdout if r.returncode == 0 else None


def vanilla_json(path):
    t = vanilla_text(path)
    if t is None:
        return None
    try:
        return json.loads(t)
    except json.JSONDecodeError:
        return None


# -- locations --------------------------------------------------------------


def map_headers():
    """[(MAP_HEADER_x, {field: value})] straight out of the generated table."""
    src = open(os.path.join(ROOT, "include", "data", "map_headers.h"),
               encoding="utf-8").read()
    out = []
    for name, body in re.findall(r"\[(MAP_HEADER_[A-Z0-9_]+)\]\s*=\s*\{(.*?)\n    \},",
                                 src, re.S):
        out.append((name, dict(re.findall(r"\.(\w+)\s*=\s*([A-Za-z0-9_]+)", body))))
    return out


def location_names():
    d = json.load(open(os.path.join(ROOT, "res", "text", "location_names.json"),
                       encoding="utf-8"))
    return {m["id"]: m["en_US"] for m in d["messages"]}


class Locations:
    """Archive name -> the in-game location name of the map that uses it."""

    # Archives no map header points at, or where the header's label is not the
    # name Ian would use for the thing.
    EXTRA = {
        HONEY_TREE: "Honey trees (21 routes)",
        MARSH_POOL: "Great Marsh",
        "scripts_common": "Any Pokemon Center (PC menu)",
    }

    def __init__(self):
        names = location_names()
        self.by_encounter = collections.defaultdict(set)
        self.by_script = collections.defaultdict(set)
        self.by_map = {}
        for header, f in map_headers():
            label = names.get(f.get("mapLabelTextID"), "")
            self.by_map[header] = label
            if f.get("wildEncountersArchiveID"):
                self.by_encounter[f["wildEncountersArchiveID"]].add(label)
            if f.get("scriptsArchiveID"):
                self.by_script[f["scriptsArchiveID"]].add(label)

    @staticmethod
    def _pick(labels, archive):
        labels = sorted(x for x in labels if x and x != "Mystery Zone")
        if labels:
            return " / ".join(labels)
        return archive.split("_", 1)[-1].replace("_", " ").title()

    def encounter(self, archive):
        if archive in self.EXTRA:
            return self.EXTRA[archive]
        return self._pick(self.by_encounter.get(archive, ()), archive)

    def script(self, archive):
        if archive in self.EXTRA:
            return self.EXTRA[archive]
        return self._pick(self.by_script.get(archive, ()), archive)

    def map(self, header):
        return self.by_map.get(header, header)


# -- source lists read out of src/ ------------------------------------------


def c_source(path):
    return open(os.path.join(ROOT, path), encoding="utf-8").read()


def swarm_maps():
    """The 22 maps a swarm can land on, from src/overlay006/swarm.c."""
    src = c_source(os.path.join("src", "overlay006", "swarm.c"))
    body = re.search(r"sSwarmMapIdTable\[NUM_SWARMS\]\s*=\s*\{(.*?)\};", src, re.S)
    return re.findall(r"(MAP_HEADER_[A-Z0-9_]+)", body.group(1))


def honey_tree_maps():
    src = c_source(os.path.join("src", "overlay005", "honey_tree.c"))
    body = re.search(r"sHoneyTreeMapHeaderIDs\[NUM_HONEY_TREES\]\s*=\s*\{(.*?)\};",
                     src, re.S)
    return re.findall(r"(MAP_HEADER_[A-Z0-9_]+)", body.group(1))


def roamer_slots():
    """[(slot constant, species, level)] from RoamingPokemon_ActivateSlot."""
    src = c_source(os.path.join("src", "roaming_pokemon.c"))
    body = src[src.index("void RoamingPokemon_ActivateSlot"):]
    body = body[:body.index("Roamer_SetData")]
    return re.findall(
        r"case\s+(ROAMING_SLOT_\w+):\s*species\s*=\s*(SPECIES_\w+);\s*"
        r"level\s*=\s*(\d+);", body)


def fossil_species():
    src = c_source(os.path.join("src", "scrcmd_fossil.c"))
    return re.findall(r"\.item\s*=\s*ITEM_(\w+),\s*\.species\s*=\s*(SPECIES_\w+)", src)


def starter_species():
    src = c_source(os.path.join("src", "choose_starter", "choose_starter_app.c"))
    return re.findall(r"#define STARTER_OPTION_\d\s+(SPECIES_\w+)", src)


# The test kit's field script code (make testkit, docs/oxide/test-kit.md) sits
# in #ifdef OXIDE_TESTKIT blocks that the ROM of record never contains, so none
# of its gifts or wild battles is a source of anything in the game.
TESTKIT_BLOCK_RE = re.compile(r"^#ifdef OXIDE_TESTKIT\n.*?^#endif[^\n]*\n?", re.M | re.S)


def game_script_text(path):
    """A field script's text as the ROM of record builds it: kit blocks removed."""
    return TESTKIT_BLOCK_RE.sub("", open(path, encoding="utf-8").read())


def roamer_activations():
    """{slot constant: [script archive]} for every ActivateRoamingPokemon."""
    out = collections.defaultdict(list)
    for path in sorted(glob.glob(os.path.join(ROOT, SCRIPT_DIR, "*.s"))):
        name = os.path.basename(path)[:-2]
        for m in re.finditer(r"ActivateRoamingPokemon\s+(\S+)",
                             game_script_text(path)):
            out[m.group(1)].append(name)
    return out


# -- script commands --------------------------------------------------------

BATTLE_RE = re.compile(
    r"^\s*(StartWildBattle|StartLegendaryBattle|StartFatefulEncounter"
    r"|StartGiratinaOriginBattle)\s+(SPECIES_[A-Z0-9_]+),\s*(\d+)")
GIVE_RE = re.compile(
    r"^\s*(GivePokemon|GivePokemonWithMoves|GiveDesignedPokemon)"
    r"\s+(SPECIES_[A-Z0-9_]+),\s*(\d+)"
    r"(?:,\s*([A-Za-z0-9_]+))?")
# GiveEgg's second operand is not a level: it is the egg's giver, an index into
# the special met-location names (Riley by name, Cynthia and the Mansion's
# "Distant land" by number), which the hatched Pokemon's summary shows.
EGG_RE = re.compile(r"^\s*(GiveEgg)\s+(SPECIES_[A-Z0-9_]+),\s*([A-Za-z0-9_]+)")
EGG_LEVEL = 1


def script_commands(regex):
    """[(script archive, species, level, extra, in_vanilla)] for one command
    family, with the vanilla check done line-for-line against main."""
    rows = []
    for path in sorted(glob.glob(os.path.join(ROOT, SCRIPT_DIR, "*.s"))):
        name = os.path.basename(path)[:-2]
        text = game_script_text(path)
        hits = [m for m in (regex.match(l) for l in text.split("\n")) if m]
        if not hits:
            continue
        van = vanilla_text(os.path.join(SCRIPT_DIR, name + ".s")) or ""
        # An egg's giver is spelled as a constant on main and as its index in
        # the scripts generated from the base ROM, so eggs compare by name.
        def keyof(m):
            third = egg_giver(m.group(3)) if regex is EGG_RE else m.group(3)
            return (m.group(1), m.group(2), third)
        van_hits = {keyof(m) for m in (regex.match(l) for l in van.split("\n")) if m}
        seen = set()
        for m in hits:
            key = keyof(m)
            if key in seen:
                continue
            seen.add(key)
            if regex is EGG_RE:
                level, extra = EGG_LEVEL, m.group(3)
            else:
                level = int(m.group(3))
                extra = m.group(4) if regex is GIVE_RE else None
            rows.append((name, m.group(1), m.group(2), level, extra,
                         key in van_hits))
    return rows


def egg_giver(operand):
    """GiveEgg's giver operand as its English name: a SPECIAL_METLOC_NAME_
    constant or its index in the special met-location names bank."""
    path = os.path.join(ROOT, "res", "text", "special_met_location_names.json")
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    entries = data.get("messages") if isinstance(data, dict) else data
    for i, e in enumerate(entries or []):
        if operand in (e.get("id"), str(i)):
            return e.get("en_US") or operand
    return operand


def trade_hookups():
    """{trade index: script archive} from the InitNPCTrade calls."""
    order = ["kazza_abra", "charap_chatot", "gaspar_haunter", "foppa_magikarp"]
    by_name = {f"NPC_TRADE_{n.upper()}": i for i, n in enumerate(order)}
    out = {}
    for path in sorted(glob.glob(os.path.join(ROOT, SCRIPT_DIR, "*.s"))):
        name = os.path.basename(path)[:-2]
        for m in re.finditer(r"InitNPCTrade\s+(\S+)",
                             game_script_text(path)):
            arg = m.group(1)
            idx = by_name.get(arg, int(arg) if arg.isdigit() else None)
            if idx is not None:
                out[idx] = name
    return out, order


# -- encounter files --------------------------------------------------------


def encounter_files():
    names = sorted(os.path.basename(p)[:-5]
                   for p in glob.glob(os.path.join(ROOT, ENC_DIR, "*.json")))
    out = {}
    for n in names:
        rel = os.path.join(ENC_DIR, n + ".json")
        out[n] = (json.load(open(os.path.join(ROOT, rel), encoding="utf-8")),
                  vanilla_json(rel))
    return out


def slot_levels(data, slots):
    """The level printed for the land slots a key overwrites."""
    enc = data.get("land_encounters") or []
    lv = sorted({enc[i]["level"] for i in slots if i < len(enc)})
    if not lv:
        return ""
    return str(lv[0]) if len(lv) == 1 else f"{lv[0]}-{lv[-1]}"


def origin_of(cur, van, key, index):
    """vanilla when main's file holds the same species at the same index."""
    if van is None or key not in van:
        return "base-rom"
    try:
        return "vanilla" if van[key][index] == cur[key][index] else "base-rom"
    except (IndexError, KeyError, TypeError):
        return "base-rom"


# -- the catalogue ----------------------------------------------------------

# Ian's decision, 2026-09-21: Oxide will never use swarms, the Poke Radar,
# the dual-slot GBA lists, the Trophy Garden dailies or the base ROM's
# Twinleaf Town legendary menu, so none of them count as a source and they are
# left out of the catalogue. The reading code for them stays so the exclusion
# is one line to lift.
EXCLUDED_METHODS = ("swarm", "poke radar", "dual-slot ", "trophy garden daily")
EXCLUDED_SCRIPTS = ("scripts_twinleaf_town.s",)


def excluded(map_or_file, method):
    return (method.startswith(EXCLUDED_METHODS)
            or (method == "static battle" and map_or_file in EXCLUDED_SCRIPTS))

Row = collections.namedtuple(
    "Row", "location map_or_file species method level conditions origin")


def build():
    loc = Locations()
    files = encounter_files()
    rows = []

    def add(location, mof, species, method, level, conditions, origin):
        if excluded(mof, method):
            return
        rows.append(Row(location, mof, species, method, str(level),
                        conditions, origin))

    # 1. The starter.
    for sp in starter_species():
        add(loc.script("scripts_route_201"), "scripts_route_201.s", sp,
            "starter", 5,
            "chosen from Rowan's briefcase; once per game; the operand is a "
            "variable (GivePokemon 32768), the three options are in "
            "src/choose_starter/choose_starter_app.c",
            "vanilla")

    # 2. Gifts and eggs from scripts.
    gift_status = {}
    gifts_csv = os.path.join(ROOT, "docs", "oxide", "pokemon-gifts.csv")
    if os.path.exists(gifts_csv):
        with open(gifts_csv, encoding="utf-8", newline="") as f:
            for r in csv.DictReader(f):
                gift_status[(r["map"], r["species"], r["level"])] = r["status"]
    for script, cmd, sp, level, item, in_van in (script_commands(GIVE_RE)
                                                 + script_commands(EGG_RE)):
        mapname = script[len("scripts_"):]
        status = gift_status.get((mapname, sp, str(level)))
        origin = "vanilla" if (in_van or status == "vanilla") else "base-rom"
        method = "egg gift" if cmd == "GiveEgg" else "gift"
        note = GIFT_NOTES.get(mapname, "NPC gift")
        if cmd == "GiveEgg":
            # item is the giver here; the met location is wherever it hatches
            note += (f"; hatches at level {EGG_LEVEL} and counts where it hatches; "
                     f"giver {egg_giver(item)}")
        elif item and item not in ("0", "ITEM_NONE"):
            note += f"; holds {item}"
        add(loc.script(script), script + ".s", sp, method, level, note, origin)

    # 3. Fossils.
    for item, sp in fossil_species():
        add(loc.script("scripts_mining_museum"), "scripts_mining_museum.s", sp,
            "fossil", 20,
            f"revive ITEM_{item} at the Oreburgh Mining Museum; the fossil "
            "comes from the Underground or a route; repeatable, one at a "
            "time; the script's operand is VAR_REVIVED_POKEMON_SPECIES and "
            "the item-to-species table is src/scrcmd_fossil.c",
            "vanilla")

    # 4. In-game trades.
    hookups, order = trade_hookups()
    for idx, fname in enumerate(order):
        rel = os.path.join("res", "npc_trades", fname + ".json")
        cur = json.load(open(os.path.join(ROOT, rel), encoding="utf-8"))
        van = vanilla_json(rel)
        origin = "vanilla" if van and van["species"] == cur["species"] else "base-rom"
        script = hookups.get(idx, "")
        where = loc.script(script) if script else "unknown"
        note = (f"trade away {cur['requestedSpecies']} to get it; once only; "
                f"OT {cur['otName']}, holds {cur['heldItem']}")
        if origin == "base-rom" and van:
            note += f"; vanilla gave {van['species']} holding {van['heldItem']}"
        add(where, rel, cur["species"], "in-game trade", "(traded mon's level)",
            note, origin)

    # 5. Scripted static and legendary battles.
    for script, cmd, sp, level, _x, in_van in script_commands(BATTLE_RE):
        note = BATTLE_NOTES.get(script, "scripted encounter, walk up and talk to it")
        add(loc.script(script), script + ".s", sp, "static battle", level,
            note, "vanilla" if in_van else "base-rom")

    # 6. Roamers.
    activations = roamer_activations()
    for slot, sp, level in roamer_slots():
        scripts = activations.get(slot, [])
        starters = [s for s in scripts if s != "scripts_common"]
        if starters:
            where = " / ".join(sorted({loc.script(s) for s in starters}))
            note = ROAMER_NOTES.get(slot, "roams Sinnoh's routes once released")
            mof = ", ".join(sorted(set(starters))) + ".s"
        else:
            where = "(not released by any script)"
            note = ("the slot exists in src/roaming_pokemon.c but no script "
                    "calls ActivateRoamingPokemon for it, in this ROM or in "
                    "vanilla, so it is unreachable")
            mof = "src/roaming_pokemon.c"
        add(where, mof, sp, "roamer", level, note, "vanilla")

    # 7. Swarms: slots 0 and 1 of the 22 swarm maps.
    header_to_enc = {}
    for header, f in map_headers():
        if f.get("wildEncountersArchiveID"):
            header_to_enc[header] = f["wildEncountersArchiveID"]
    for header in swarm_maps():
        archive = header_to_enc.get(header)
        if not archive or archive not in files:
            continue
        cur, van = files[archive]
        for i, sp in enumerate(cur.get("swarms", [])):
            add(loc.map(header), archive + ".json", sp, "swarm",
                slot_levels(cur, SLOTS["swarms"]),
                "one route swarms per day, picked from the 22 in "
                "src/overlay006/swarm.c; swarms need the Dowsing/《swarm》 "
                "news unlocked (EnableSwarms) and are announced on TV; the "
                f"pair overwrites land slots 0 and 1 (this is slot {i})",
                origin_of(cur, van, "swarms", i))

    # 8. Poke Radar, dual-slot, Trophy Garden dailies, Feebas.
    for archive in sorted(files):
        cur, van = files[archive]
        where = loc.encounter(archive)
        seen = set()
        for i, sp in enumerate(cur.get("radar", [])):
            if ("radar", sp) in seen:
                continue
            seen.add(("radar", sp))
            add(where, archive + ".json", sp, "poke radar",
                slot_levels(cur, SLOTS["radar"]),
                "only in a Poke Radar patch (needs the Radar, National Dex "
                "and a grass tile); overwrites land slots 4, 5, 10 and 11",
                origin_of(cur, van, "radar", i))
        for key, game in DUAL_SLOT_GAMES.items():
            for i, sp in enumerate(cur.get(key, [])):
                if (key, sp) in seen:
                    continue
                seen.add((key, sp))
                add(where, archive + ".json", sp, f"dual-slot {game}",
                    slot_levels(cur, SLOTS["dual_slot"]),
                    f"needs Pokemon {game} in the GBA slot and the National "
                    "Dex; overwrites land slots 8 and 9",
                    origin_of(cur, van, key, i))
        for i, sp in enumerate(cur.get("daily_encounters", [])):
            add(where, archive + ".json", sp, "trophy garden daily",
                slot_levels(cur, SLOTS["trophy_garden"]),
                "two of the sixteen are in the garden each day, rotated by "
                "TrophyGarden_AddNewMon when the Mansion's owner is spoken "
                "to; needs the National Dex; overwrites land slots 6 and 7",
                origin_of(cur, van, "daily_encounters", i))
        er = cur.get("elusive_rod_encounter")
        if er:
            van_er = (van or {}).get("elusive_rod_encounter") or {}
            add(where, archive + ".json", er["species"], "special tile (rod)",
                "10-20",
                "four tiles out of the lake's fishing tiles hold it, chosen "
                "from the record-mixing RNG and re-rolled on a record mix; "
                "Super Rod only, 50% per cast on a good tile "
                "(src/overlay006/feebas_fishing.c)",
                "vanilla" if van_er.get("species") == er["species"] else "base-rom")
        ut = cur.get("unown_table")
        if ut:
            forms = UNOWN_TABLES[ut - 1]
            note = ("the room's Unown forms are fixed by unown_table "
                    f"{ut}: {forms}")
            if ut == 1:
                note += " (a dead-end room)"
            elif ut == 8:
                note += ("; the Maniac Tunnel secret room, open after all 26 "
                         "other forms have been seen")
            else:
                note += " (a room on the F-R-I-E-N-D path)"
            add(where, archive + ".json", "SPECIES_UNOWN", "unown room",
                slot_levels(cur, (0,)), note,
                "vanilla" if (van or {}).get("unown_table") == ut else "base-rom")

    # 9. Honey trees. Platinum Oxide has one table per badge count, each with
    # its own levels (Ian, 2026-09-26); vanilla had one table at 5-15 and a
    # rare tier only four Munchlax trees could roll, which Oxide dropped.
    rel = os.path.join(ENC_DIR, HONEY_TREE + ".json")
    cur = json.load(open(os.path.join(ROOT, rel), encoding="utf-8"))
    van = vanilla_json(rel) or {}
    van_species = {sp for k in ("common", "uncommon", "rare") for sp in van.get(k) or []}
    tier_note = {
        "common": "group A, 70% of a shaking tree",
        "uncommon": "group B, 20% of a shaking tree",
    }
    for table in cur["tables"]:
        for key in ("common", "uncommon"):
            seen = set()
            for sp in table[key]:
                if sp in seen:
                    continue
                seen.add(sp)
                add("Honey trees (21 routes)", HONEY_TREE + ".json", sp,
                    f"honey tree ({key}, {table['badges']} badge"
                    f"{'' if table['badges'] == 1 else 's'})",
                    f"{table['level_min']}-{table['level_max']}",
                    tier_note[key] + f"; the table for {table['badges']} badge"
                    f"{'' if table['badges'] == 1 else 's'} ({table['split']} split), "
                    "read when the tree is shaken; slather with Honey, wait "
                    "6 hours, 24-hour window; slot rates 40/20/20/10/5/5 "
                    "(src/overlay005/honey_tree.c)",
                    "vanilla" if sp in van_species else "base-rom")

    # 10. Great Marsh daily rotation.
    rel = os.path.join(ENC_DIR, MARSH_POOL + ".json")
    cur = json.load(open(os.path.join(ROOT, rel), encoding="utf-8"))
    van = vanilla_json(rel) or {}
    for key, label, cond in (
        ("before_national_dex", "great marsh daily (pre-natdex)",
         "one of these 32 is in each of the six marsh areas per day, index "
         "= 5 bits of the daily seed per area; only while a Safari Game is "
         "running; overwrites land slots 6 and 7"),
        ("after_national_dex", "great marsh daily (post-natdex)",
         "the same rotation once the National Dex is in hand; the binoculars "
         "on the lookout show a random slot of the same table"),
    ):
        seen = set()
        for i, sp in enumerate(cur[key]):
            if sp in seen:
                continue
            seen.add(sp)
            add("Great Marsh", MARSH_POOL + ".json", sp, label, "22-30",
                cond, origin_of(cur, van, key, i))

    # 11. Pal Park and the Day Care, which have no species list in the tree.
    add("Pal Park", "src/catching_show.c", "(from the GBA save)",
        "pal park migration", "(as migrated)",
        "six Pokemon at a time migrated out of a Ruby/Sapphire/Emerald/"
        "FireRed/LeafGreen cartridge, then caught in the catching show; the "
        "species come from that save, not from any table in this tree; needs "
        "the National Dex and a DS with a GBA slot", "vanilla")
    add("Solaceon Town", "src/egg.c", "(egg of the mother's line)",
        "day care egg", "1",
        "breeding at the Solaceon Day Care; the only route to baby stages "
        "and to any egg move; the Day Care man's gift is a Floette rather "
        "than the base ROM's Ditto, so there is no longer a universal "
        "breeding partner, which Ian ruled out of scope on 2026-09-21", "vanilla")

    return rows


GIFT_NOTES = {
    "canalave_library_2f": "clown gift, one of seven rolled at random "
        "(GetRandom 7); once only (FLAG_RECEIVED_CANALAVE_LIBRARY_GIFT)",
    "eterna_city_condominiums_1f": "clown gift, one of three rolled at random; "
        "once only (FLAG_RECEIVED_ETERNA_CITY_CONDOMINIUMS_GIFT)",
    "eterna_city": "Egg from Cynthia in Eterna City; once only",
    "floaroma_meadow_house": "clown gift, one of three rolled at random; "
        "once only (FLAG_RECEIVED_FLOAROMA_MEADOW_HOUSE_GIFT)",
    "floaroma_town_middle_house": "clown gift, one of four rolled at random; "
        "once only (FLAG_RECEIVED_FLOAROMA_TOWN_MIDDLE_HOUSE_GIFT)",
    "hearthome_city_northwest_house": "gift from the woman in the house; once "
        "only (FLAG_RECEIVED_...EEVEE), cleared again by the post-game "
        "Trades/Gifts Reset",
    "hearthome_city_pokemon_fan_club": "pick one of nine first partners from a "
        "list menu; once only "
        "(FLAG_RECEIVED_HEARTHOME_CITY_POKEMON_FAN_CLUB_GIFT)",
    "iron_island_b2f_left_room": "Egg from Riley after the Iron Island "
        "partner section; once only",
    "jubilife_city_south_house_1f": "clown gift, one of three rolled at "
        "random; once only (FLAG_RECEIVED_JUBILIFE_CITY_SOUTH_HOUSE_GIFT)",
    "oreburgh_city_middle_house": "clown gift, one of three rolled at random; "
        "once only (FLAG_RECEIVED_OREBURGH_CITY_MIDDLE_HOUSE_GIFT)",
    "pastoria_city_north_house": "clown gift, one of six rolled at random; the "
        "roll was GetRandom 3 with six branches, so three could never come "
        "out, and was widened to six; once only "
        "(FLAG_RECEIVED_PASTORIA_CITY_NORTH_HOUSE_GIFT)",
    "pokemon_day_care": "the Day Care man hands it over on a yes/no prompt; "
        "once only (FLAG_RECEIVED_POKEMON_DAY_CARE_GIFT); shiny, perfect "
        "IVs and a neutral nature, through GiveDesignedPokemon",
    "pokemon_mansion_office": "Egg from the Mansion's owner; once only "
        "(FLAG_UNK_0x0A65), cleared again by the post-game Trades/Gifts "
        "Reset; vanilla only ever gave this through Mystery Gift",
    "sandgem_town_house": "pick one of three from a list menu; once only "
        "(FLAG_RECEIVED_SANDGEM_TOWN_HOUSE_GIFT)",
    "solaceon_town_northeast_house": "clown gift, one of three rolled at "
        "random; once only "
        "(FLAG_RECEIVED_SOLACEON_TOWN_NORTHEAST_HOUSE_GIFT)",
    "unused_jubilife_city_south_house_3f": "a third-floor copy of the "
        "Jubilife clown; once only "
        "(FLAG_RECEIVED_UNUSED_JUBILIFE_CITY_SOUTH_HOUSE_3F_GIFT); check the "
        "map is reachable before counting it",
    "veilstone_city_northeast_house": "clown gift, one of three rolled at "
        "random; once only "
        "(FLAG_RECEIVED_VEILSTONE_CITY_NORTHEAST_HOUSE_GIFT); the Porygon slot "
        "beside it is a separate gift with its own vanilla flag",
}

BATTLE_NOTES = {
    "scripts_acuity_cavern": "after the Galactic plot at Lake Acuity; once, "
        "unless the post-game Legendary Reset is used",
    "scripts_old_chateau_back_middle_west_room": "the TV in the Old Chateau, "
        "once per day (FLAG_DAILY_BATTLED_OLD_CHATEAU_ROTOM)",
    "scripts_valley_windworks_outside": "the balloon by the Windworks, Friday "
        "only, once per week",
    "scripts_valor_cavern": "after the Galactic plot at Lake Valor; once",
    "scripts_distortion_world_giratina_room": "the story battle in the "
        "Distortion World; Origin Forme; once",
    "scripts_flower_paradise": "needs Oak's Letter and the Seabreak Path; in "
        "vanilla the Letter was a Mystery Gift item, here the Sandgem lab "
        "hands it over with the National Dex",
    "scripts_hall_of_origin": "needs the Azure Flute at the Spear Pillar; in "
        "vanilla the Flute was never distributed, here the Sandgem lab hands "
        "it over with the National Dex",
    "scripts_iceberg_ruins": "the Snowpoint Temple Regi puzzle, post-game",
    "scripts_iron_ruins": "the Iron Island Regi puzzle, post-game",
    "scripts_rock_peak_ruins": "the Route 228 Regi puzzle, post-game",
    "scripts_newmoon_island_forest": "needs the Member Card for the Canalave "
        "sailor; in vanilla the Card was a Mystery Gift item, here the "
        "Sandgem lab hands it over with the National Dex",
    "scripts_route_209": "put an Odd Keystone in the Hallowed Tower, talk to "
        "32 Underground players, then check the tower; once",
    "scripts_snowpoint_temple_b5f": "at the bottom of Snowpoint Temple with "
        "Regirock, Regice and Registeel in the party; level 1",
    "scripts_spear_pillar_dialga": "the story battle at the Spear Pillar",
    "scripts_spear_pillar_palkia": "the story battle at the Spear Pillar",
    "scripts_stark_mountain_room_3": "after the Stark Mountain / Buck story; "
        "once",
    "scripts_turnback_cave_giratina_room": "Turnback Cave, after the "
        "Distortion World; Altered Forme",
    "scripts_twinleaf_town": "the esper NPC in Twinleaf Town offers all "
        "fifteen from a list menu once the Hall of Fame is entered "
        "(CheckGameCompleted); no flag is set afterwards, so each of them is "
        "repeatable without limit",
}

ROAMER_NOTES = {
    "ROAMING_SLOT_MESPRIT": "released when you reach it in Verity Cavern "
        "after the Galactic plot; then roams; the Marking Map app tracks it",
    "ROAMING_SLOT_CRESSELIA": "released on Fullmoon Island (reached with the "
        "Lunar Wing errand); then roams",
    "ROAMING_SLOT_MOLTRES": "released by Prof. Oak in the Eterna City south "
        "house once the National Dex is in hand; then roams",
    "ROAMING_SLOT_ZAPDOS": "released by Prof. Oak in the Eterna City south "
        "house once the National Dex is in hand; then roams",
    "ROAMING_SLOT_ARTICUNO": "released by Prof. Oak in the Eterna City south "
        "house once the National Dex is in hand; then roams",
}


# -- output -----------------------------------------------------------------

HEADER = """# Pokemon sources other than an ordinary land table

Generated by `tools/oxide/pokemon_sources.py`, read out of this tree and not
from any wiki. Regenerate with:

    cd ~/pokeplatinum && PYTHONPATH=. python3 tools/oxide/pokemon_sources.py

It writes this file and `pokemon-sources.csv` beside it, and touches nothing
else. `docs/oxide/pokemon-gifts.md` is the companion survey of the gift
scripts alone; this file is the whole list.

Every row says where the fact came from (a `res/` file or a `src/` file), what
the conditions are, whether it is vanilla or something the base ROM added
(`git show main:<path>` is vanilla), and whether the species is on
`docs/oxide/species-pick-list.csv`. An off-list species reachable from one of
these rows is a leak the encounter authoring pass has to decide on
(authoring plan decision 8).

**What "non-standard" leaves out.** Ordinary land slots, and the day/night
pair, are not listed: the day and night lists simply overwrite land slots 2
and 3 outside the morning, so they are part of the ordinary table. Surf and
the three rods are not listed either, having been checked for anything
exclusive and found to hold nothing a land, gift or scripted source does not
already reach, except the Feebas tiles, which are listed.

**Left out on Ian's decision (2026-09-21):** swarms, the Poke Radar, the
dual-slot GBA lists, the Trophy Garden dailies and the base ROM's Twinleaf
Town legendary menu. Oxide will never use any of them, so they are not sources
and the authoring pass does not have to de-leak them; the generator still reads
them and `EXCLUDED_METHODS` in `tools/oxide/pokemon_sources.py` is the switch.

**How a land table gets overwritten.** Several of the methods below are not
separate tables at all; they replace numbered slots of the map's own land
table, so they compete with it rather than adding to it
(`src/overlay006/wild_encounters.c`):

| Slots | Replaced by | When |
|---|---|---|
| 0, 1 | the map's `swarms` pair | that map is today's swarm and swarms are enabled |
| 2, 3 | `day` or `night` | any time except morning |
| 4, 5, 10, 11 | `radar` | the encounter came out of a Poke Radar patch |
| 6, 7 | `daily_encounters` (Trophy Garden) or the Great Marsh daily | National Dex, or a running Safari Game |
| 8, 9 | `ruby`..`leafgreen` | National Dex and that GBA cartridge in the slot |

"""


def write_csv(rows, on_list, path):
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["location", "map_or_file", "species", "method", "level",
                    "conditions", "origin", "on_pick_list"])
        for r in rows:
            w.writerow([r.location, r.map_or_file, r.species, r.method,
                        r.level, r.conditions, r.origin,
                        on_list(r.species)])


def write_md(rows, on_list, path, counts):
    by_loc = collections.OrderedDict()
    for r in sorted(rows, key=lambda r: (r.location.lower(), r.method,
                                         r.species)):
        by_loc.setdefault(r.location, []).append(r)
    with open(path, "w", encoding="utf-8") as f:
        f.write(HEADER)
        f.write(f"{len(rows)} rows across {len(by_loc)} locations, "
                f"generated {datetime.date.today().isoformat()}.\n\n")
        f.write("## Rows by method\n\n| Method | Rows |\n|---|---|\n")
        for k, v in sorted(counts.items(), key=lambda kv: -kv[1]):
            f.write(f"| {k} | {v} |\n")
        f.write("\n## By location\n\n")
        for location, group in by_loc.items():
            f.write(f"### {location}\n\n")
            f.write("| Species | Method | Level | Conditions | Origin | "
                    "On pick-list | Source |\n|---|---|---|---|---|---|---|\n")
            for r in group:
                name = (dex.display_name(r.species)
                        if r.species.startswith("SPECIES_") else r.species)
                origin = ("vanilla" if r.origin == "vanilla"
                          else "**base-ROM**")
                f.write(f"| {name} | {r.method} | {r.level} | {r.conditions} "
                        f"| {origin} | {on_list(r.species)} "
                        f"| `{r.map_or_file}` |\n")
            f.write("\n")


def main():
    rows = build()
    listed = {row["constant"] for row in dex.pick_list(ROOT)
              if row["status"] != "cut" and row["constant"]}

    def on_list(species):
        if not species.startswith("SPECIES_"):
            return "n/a"
        return "yes" if species in listed else "no"

    counts = collections.Counter(r.method for r in rows)
    out_csv = os.path.join(ROOT, "docs", "oxide", "pokemon-sources.csv")
    out_md = os.path.join(ROOT, "docs", "oxide", "pokemon-sources.md")
    write_csv(rows, on_list, out_csv)
    write_md(rows, on_list, out_md, counts)
    print(f"{len(rows)} rows -> {out_csv}, {out_md}")
    for k, v in sorted(counts.items(), key=lambda kv: -kv[1]):
        print(f"  {v:5d}  {k}")
    off = sorted({r.species for r in rows
                  if r.species.startswith("SPECIES_") and on_list(r.species) == "no"})
    print(f"  {len(off)} distinct off-pick-list species referenced")


if __name__ == "__main__":
    main()

"""B1d: which split every map, trainer and item belongs to in Oxide.

    PYTHONPATH=. python3 -m tools.oxide.balance.splits

A split is the stretch of the game before a gym, named for its leader
(Roark to Volkner), then League and Post. Two splits have no gym, both
between Candice and Volkner (Ian, 2026-09-25; docs/oxide/battle-zone-plan.md):
HQ holds the Galactic Warehouse and HQ, and Galactic holds the Battle Zone,
the Mt. Coronet climb, Spear Pillar and the Distortion World. A map belongs to the split in
which the player can first reach it. It is resolved in this order:

1. A map named in MAP_SPLITS, for the few whose name or location misleads
   (the Galactic building in Eterna is Fantina's, not Gardenia's).
2. The map's own wild encounter table, whose split the encounter design
   records (docs/oxide/encounters/design.json). This is what separates
   Route 204's south half (Roark) from its north (Gardenia).
3. LOCATION_SPLITS, by the map's location name, for towns and the places
   with no encounter table.
4. The map whose name is the longest prefix of this one's, so a house on
   Route 212 north takes Route 212 north's split.
5. The maps whose warps lead into it, so a building takes the split of the
   route or town outside its door.
6. The earliest split any other map with the same location name has.

A trainer belongs to the splits of the maps that field it: those whose
events place it as a sight trainer, or whose scripts start a battle with
it. Story bosses keep the split Ian's Level Caps sheet gives them
(fights.json); some are fought on maps first reached earlier, and
STORY_REVISITS lists them.

Items come from four places: item balls (events scripts 7000 and up, whose
entry in scripts_visible_items.s names the item), hidden items (bg events of
type 2, whose script is 8000 plus the item's obtained-flag offset in
gHiddenItems), NPC gifts (the item set into VAR_0x8004 before a give
script), and shops: marts (a common stock gated by badge count, and each
city's specialties) and the Veilstone Game Corner's prize counter. The
Battle Frontier's prize counters are not read.
"""
import collections
import functools
import json
import os
import re
import sys

from ..encounters import locations
from . import data

SPLITS = ["Roark", "Gardenia", "Fantina", "Maylene", "Wake", "Byron", "Candice",
          "HQ", "Galactic", "Volkner", "Barry", "League", "Post"]

# Maps whose location name or position would place them wrong. Checked
# against the story fights fought on them.
MAP_SPLITS = {
    "ETERNA_CITY_GALACTIC_BUILDING": "Fantina",   # Jupiter 1, after Gardenia
    "GALACTIC_HQ": "HQ",
    "VEILSTONE_CITY_GALACTIC_WAREHOUSE": "HQ",
    # The Elite Four's and the Champion's rooms, the lifts to them and the
    # Hall of Fame are the League split; the rest of the League (its front,
    # Pokemon Centers and mart) comes before them, in the Barry split. The
    # first pattern a map's name starts with wins, so the rooms come first.
    "POKEMON_LEAGUE_AARON_ROOM": "League", "POKEMON_LEAGUE_BERTHA_ROOM": "League",
    "POKEMON_LEAGUE_FLINT_ROOM": "League", "POKEMON_LEAGUE_LUCIAN_ROOM": "League",
    "POKEMON_LEAGUE_CHAMPION_ROOM": "League", "POKEMON_LEAGUE_ELEVATOR_TO_": "League",
    "POKEMON_LEAGUE_HALLWAY_TO_HALL_OF_FAME": "League", "POKEMON_LEAGUE_HALL_OF_FAME": "League",
    "POKEMON_LEAGUE": "Barry",
}

# Where the player first arrives, for location names with no wild table of
# their own. Towns take the split whose gym is next when the player gets
# there; the Battle Frontier and the islands and ruins past the League are
# Post. "Mystery Zone" is the name of internal maps and stays unplaced.
LOCATION_SPLITS = {
    "Sandgem Town": "Roark", "Jubilife City": "Roark", "Jubilife TV": "Roark",
    "Pokétch Co.": "Roark", "Global Terminal": "Roark", "Trainers’ School": "Roark",
    "Oreburgh City": "Roark", "Mining Museum": "Roark", "Verity Lakefront": "Roark",
    "Floaroma Town": "Gardenia", "Floaroma Meadow": "Gardenia", "Flower Shop": "Gardenia",
    "Eterna City": "Gardenia", "Cycle Shop": "Gardenia",
    "T.G. Eterna Bldg": "Fantina", "Hearthome City": "Fantina", "Contest Hall": "Fantina",
    "Amity Square": "Fantina", "Poffin House": "Fantina", "Foreign Building": "Fantina",
    "Solaceon Town": "Maylene", "Pokémon Day Care": "Maylene", "Veilstone City": "Maylene",
    "Veilstone Store": "Maylene", "Game Corner": "Maylene",
    "Pastoria City": "Wake", "Grand Lake": "Wake",
    "Celestic Town": "Byron", "Canalave City": "Byron", "Canalave Library": "Byron",
    "Snowpoint City": "Candice", "Valor Cavern": "Candice", "Verity Cavern": "Candice",
    "Acuity Cavern": "Candice",
    "Galactic HQ": "HQ", "Spear Pillar": "Galactic", "Distortion World": "Galactic",
    # The Battle Zone opens with Snowpoint's ferry, after Candice. The
    # Battleground's rematches and the Villa stay after the League.
    "Fight Area": "Galactic", "Survival Area": "Galactic", "Resort Area": "Galactic",
    "Sunyshore City": "Volkner", "Sunyshore Market": "Volkner", "Vista Lighthouse": "Volkner",
    "Pokémon League": "Barry",
    "Villa": "Post",
    "Battleground": "Post", "Battle Frontier": "Post", "Battle Tower": "Post",
    "Battle Park": "Post", "Battle Factory": "Post", "Battle Hall": "Post",
    "Battle Castle": "Post", "Battle Arcade": "Post", "Fullmoon Island": "Post",
    "Newmoon Island": "Post", "Iron Ruins": "Post", "Iceberg Ruins": "Post",
    "Rock Peak Ruins": "Post", "Hall of Origin": "Post", "Flower Paradise": "Post",
    "Seabreak Path": "Post", "Spring Path": "Post", "Pal Park": "Post", "ROTOM’s Room": "Post",
}

# Story bosses fought on a map the player first reached in an earlier split.
# Their split comes from fights.json; the map's own split is not wrong, the
# fight just happens on a return visit.
STORY_REVISITS = {
    "mars_2": "Lake Verity, first reached in Roark's split, fought in Candice's",
    "somnu_moira": "Lake Verity, as Mars 2",
    "lucas_dawn_2": "Route 207, first reached in Roark's split, fought in Fantina's "
                    "on the way from Eterna to Hearthome (its aces are 30)",
    "flint_volkner": "the Fight Area, first reached in the Galactic split, fought in the "
                     "Barry split once the Beacon Badge is won",
}

_HEADER = re.compile(r"\[(MAP_HEADER_\w+)\] = \{(.*?)\n    \},", re.S)
_FIELD = re.compile(r"\.(\w+) = (\w+)")
# The commands that start a battle with a trainer, and how many leading
# operands are not opponents: a tag battle names the partner's variable
# first, then both opponents.
_BATTLE = re.compile(r"^\s*(StartTrainerBattle|StartFirstBattle|StartTagBattle)\s+([\w ,]+)$", re.M)
_NOT_OPPONENTS = {"StartTrainerBattle": 0, "StartFirstBattle": 0, "StartTagBattle": 1}
_VISIBLE = re.compile(r"^VisibleItems_Entry(\d+):\n\s*SetVarFromValue VAR_0x8008, (\w+)", re.M)
_HIDDEN = re.compile(r"HIDDEN_ITEM_ENTRY\((ITEM_\w+),\s*\d+,\s*\d+,\s*(FLAG_\w+)\)")
_NUMBER = re.compile(r"0x[0-9a-fA-F]+|\d+")


@functools.lru_cache(maxsize=None)
def flag_values():
    """{flag or var name: its number}, from the tree's own
    generated/vars_flags.txt, numbered as metang numbers it for the build:
    each name one past the name before, unless it is set to a number or to
    an earlier name, which the count then continues from. This used to be
    read from the build's generated header, but build/ is shared by every
    session and holds whichever tree last built it, so on 2026-09-27 a
    rename in another tree's list left this tree's hidden items unread."""
    out, nxt = {}, 0
    for line in _read("generated", "vars_flags.txt").splitlines():
        line = line.strip()
        if not line:
            continue
        if "=" in line:
            name, expr = (s.strip() for s in line.split("=", 1))
            value = int(expr, 0) if _NUMBER.fullmatch(expr) else out[expr]
        else:
            name, value = line, nxt
        out[name] = value
        nxt = value + 1
    return out
VISIBLE_ITEM_SCRIPT, HIDDEN_ITEM_SCRIPT = 7000, 8000
BG_HIDDEN_ITEM = 2   # bg event type; the others are signs and triggers


def _read(*rel):
    with open(os.path.join(data.ROOT, *rel), encoding="utf-8") as f:
        return f.read()


def _script(stem):
    """A field script without the test kit, which a normal ROM never has."""
    return data.read_script(os.path.join(data.ROOT, "res", "field", "scripts", f"{stem}.s"))


@functools.lru_cache(maxsize=None)
def headers():
    """Every map header's fields, by name without the MAP_HEADER_ prefix."""
    out = {}
    for m in _HEADER.finditer(_read("include", "data", "map_headers.h")):
        out[m.group(1)[len("MAP_HEADER_"):]] = dict(_FIELD.findall(m.group(2)))
    return out


@functools.lru_cache(maxsize=None)
def _area_splits():
    with open(os.path.join(data.ROOT, "docs", "oxide", "encounters", "design.json"),
              encoding="utf-8") as f:
        areas = json.load(f)["areas"]
    return {stem: a.get("split") for stem, a in areas.items() if a.get("split")}


@functools.lru_cache(maxsize=None)
def location_name(header):
    return locations.label_names().get(headers()[header].get("mapLabelTextID"))


def _direct(header):
    """Steps 1 to 4 of the module docstring, without looking at neighbours."""
    for pattern, split in MAP_SPLITS.items():
        if header.startswith(pattern):
            return split, "named"
    encounters = headers()[header].get("wildEncountersArchiveID", "").lower()
    if encounters in _area_splits():
        return _area_splits()[encounters], "encounters"
    name = location_name(header)
    if name in LOCATION_SPLITS:
        return LOCATION_SPLITS[name], "location"
    parts = header.split("_")
    for n in range(len(parts) - 1, 0, -1):
        prefix = "_".join(parts[:n])
        if prefix in headers():
            split, _how = _direct(prefix)
            if split:
                return split, "prefix"
    return None, "unplaced"


@functools.lru_cache(maxsize=None)
def _warps_into():
    """Map to the set of maps whose warps lead into it."""
    out = collections.defaultdict(set)
    for header, fields in headers().items():
        events = fields.get("eventsArchiveID")
        path = os.path.join(data.ROOT, "res", "field", "events", f"{events}.json") if events else None
        if path and os.path.exists(path):
            with open(path, encoding="utf-8") as f:
                for warp in json.load(f).get("warp_events", []):
                    dest = warp.get("dest_header_id", "")
                    if dest.startswith("MAP_HEADER_"):
                        out[dest[len("MAP_HEADER_"):]].add(header)
    return out


@functools.lru_cache(maxsize=None)
def _resolved():
    """Every map's (split, how). Maps the direct steps leave unplaced take
    the earliest split of the placed maps that warp into them, repeated so a
    split reaches a building through its gate; any still unplaced take the
    earliest split recorded for their location name."""
    out = {h: _direct(h) for h in headers()}
    for _ in range(4):
        for h, (split, _how) in list(out.items()):
            if split:
                continue
            around = [out[n][0] for n in _warps_into().get(h, ()) if n in out and out[n][0]]
            if around:
                out[h] = (min(around, key=SPLITS.index), "warp")
    by_name = collections.defaultdict(list)
    for h, (split, _how) in out.items():
        if split:
            by_name[location_name(h)].append(split)
    for h, (split, _how) in list(out.items()):
        if not split and by_name.get(location_name(h)) and location_name(h) != "Mystery Zone":
            out[h] = (min(by_name[location_name(h)], key=SPLITS.index), "location area")
    return out


def map_split(header):
    """(split, how) for one map; split is None where nothing places it."""
    return _resolved()[header]


@functools.lru_cache(maxsize=None)
def _trainer_ids():
    """Trainer constants and numbers both resolve to an Oxide trainer id."""
    ids = {t["constant"]: tr_id for tr_id, t in data.oxide_trainers().items()}
    return ids


def _trainer_id(token):
    if token.isdigit():
        return int(token)
    return _trainer_ids().get(token)


@functools.lru_cache(maxsize=None)
def trainer_maps():
    """Oxide trainer id to the set of maps that field it."""
    out = collections.defaultdict(set)
    for header, fields in headers().items():
        events = fields.get("eventsArchiveID")
        if events:
            path = os.path.join(data.ROOT, "res", "field", "events", f"{events}.json")
            if os.path.exists(path):
                with open(path, encoding="utf-8") as f:
                    for obj in json.load(f).get("object_events", []):
                        script = str(obj.get("script", ""))
                        if script.startswith("TRAINER_"):
                            tr_id = _trainer_id(script)
                            if tr_id is not None:
                                out[tr_id].add(header)
        scripts = fields.get("scriptsArchiveID")
        if scripts:
            path = os.path.join(data.ROOT, "res", "field", "scripts", f"{scripts}.s")
            if os.path.exists(path):
                for command, operands in _BATTLE.findall(_script(scripts)):
                    tokens = [t.strip() for t in operands.split(",")]
                    for token in tokens[_NOT_OPPONENTS[command]:]:
                        tr_id = _trainer_id(token)
                        if tr_id and tr_id in data.oxide_trainers():
                            out[tr_id].add(header)
    return out


_TRAINER_REF = re.compile(r"\b(TRAINER_[A-Z0-9_]+)\b")


@functools.lru_cache(maxsize=None)
def trainer_mentions():
    """Oxide trainer id to the maps whose scripts name it at all: a
    defeated check, a trainer flag. The Pokemon Mansion's daily battle
    starts through a variable and is only found this way."""
    out = collections.defaultdict(set)
    for header, fields in headers().items():
        scripts = fields.get("scriptsArchiveID")
        path = os.path.join(data.ROOT, "res", "field", "scripts", f"{scripts}.s") if scripts else None
        if path and os.path.exists(path):
            for const in set(_TRAINER_REF.findall(_script(scripts))):
                tr_id = _trainer_ids().get(const)
                if tr_id is not None:
                    out[tr_id].add(header)
    return out


# Shared script files that start battles but belong to no single map. The
# Pokemon Center visitors are Platinum's after-the-League daily battles
# (unverified in Oxide's scripts beyond the file's name and use).
SHARED_SCRIPT_SPLITS = {"scripts_pokemon_center_daily_trainers": "Post"}


@functools.lru_cache(maxsize=None)
def _shared_mentions():
    out = {}
    for stem, split in SHARED_SCRIPT_SPLITS.items():
        for const in set(_TRAINER_REF.findall(_script(stem))):
            tr_id = _trainer_ids().get(const)
            if tr_id is not None:
                out[tr_id] = split
    return out


def trainer_split(tr_id):
    """The earliest split among the maps that battle a trainer, or, for a
    trainer no map battles directly, among the maps whose scripts name it.
    The fallback is only a fallback because a town's script often checks
    whether some gym leader is beaten, which must not move the leader."""
    for maps in (trainer_maps().get(tr_id, ()), trainer_mentions().get(tr_id, ())):
        placed = [map_split(h)[0] for h in maps]
        placed = [s for s in placed if s]
        if placed:
            return min(placed, key=SPLITS.index)
    return _shared_mentions().get(tr_id)


# An NPC gift sets VAR_0x8004 (0x8004 is 32772 in generated scripts) to the
# item and then calls one of the two give scripts, by macro in hand-written
# scripts and by number in generated ones; AddItem gives directly.
_SET_ITEM = re.compile(r"^\s*SetVar(?:FromValue)?\s+VAR_0x8004,\s*(\w+)")
_GIVE = re.compile(r"^\s*(?:Common_GiveItemQuantity(?:NoLineFeed)?|CallCommonScript\s+(?:2044|2016|0x7FC|0x7E0))\s*$")
_ADD_ITEM = re.compile(r"^\s*AddItem\s+(\w+),")
_ITEM_VAR = {"VAR_0x8004", "32772"}


@functools.lru_cache(maxsize=None)
def gifts():
    """Every item an NPC script gives: (split, map, item constant)."""
    out = []
    for header, fields in headers().items():
        scripts = fields.get("scriptsArchiveID")
        path = os.path.join(data.ROOT, "res", "field", "scripts", f"{scripts}.s") if scripts else None
        if not path or not os.path.exists(path):
            continue
        split, last = map_split(header)[0], None
        for line in _script(scripts).split("\n"):
            m = _SET_ITEM.match(line)
            if m:
                last = m.group(1)
                continue
            m = _ADD_ITEM.match(line)
            token = (last if m.group(1) in _ITEM_VAR else m.group(1)) if m else \
                (last if _GIVE.match(line) else None)
            if token and (token.startswith("ITEM_") or token.isdigit()):
                item = _item(token)
                if item.startswith("ITEM_") and item != "ITEM_NONE":
                    out.append((split, header, item))
    return sorted(set(out))


# The overworld weathers a battle starts in (battle_lib.c, the field
# weather switch-in check). Everything else a map header can hold (ashfall,
# the cave darkness values 27 to 30) starts no battle weather. Harsh sun and
# Trick Room exist too, but only scripts set them, never a map header.
BATTLE_WEATHER = {
    "OVERWORLD_WEATHER_RAINING": "Rain", "OVERWORLD_WEATHER_HEAVY_RAIN": "Rain",
    "OVERWORLD_WEATHER_THUNDERSTORM": "Rain", "OVERWORLD_WEATHER_SNOWING": "Hail",
    "OVERWORLD_WEATHER_HEAVY_SNOW": "Hail", "OVERWORLD_WEATHER_BLIZZARD": "Hail",
    "OVERWORLD_WEATHER_SANDSTORM": "Sand", "OVERWORLD_WEATHER_FOG": "Fog",
    "OVERWORLD_WEATHER_DEEP_FOG": "Fog",
}


def battle_weather(header):
    """The weather a battle on this map starts in, or None."""
    return BATTLE_WEATHER.get(headers()[header].get("weather"))


def trainer_weather(tr_id):
    """The battle weathers of the maps that battle a trainer."""
    return sorted({battle_weather(h) for h in trainer_maps().get(tr_id, ()) if battle_weather(h)})


# A mart's common stock opens in tiers by badge count (scrcmd_shop.c): tier 1
# with none, 2 with one, 3 with three, 4 with five, 5 with seven, 6 with
# eight. The split a tier opens in is the first split with that many badges;
# seven badges come with Candice's, so tier 5 opens in HQ.
MART_TIER_SPLIT = {1: "Roark", 2: "Gardenia", 3: "Maylene", 4: "Byron", 5: "HQ", 6: "Barry"}
# Each specialty stock, by the start of its table name, to its city's split.
MART_TABLE_SPLIT = {
    "Jubilife": "Roark", "Oreburgh": "Roark", "Floaroma": "Gardenia", "Eterna": "Gardenia",
    "Hearthome": "Fantina", "Solaceon": "Maylene", "Veilstone": "Maylene", "Pastoria": "Wake",
    "Celestic": "Byron", "Canalave": "Byron", "Snowpoint": "Candice", "Sunyshore": "Volkner",
    "PokemonLeague": "Barry",
}
_COMMON = re.compile(r"\{ (ITEM_\w+), (0x[0-9a-fA-F]+|\d+) \}")
_TABLE = re.compile(r"const u16 (\w+)\[\] = \{(.*?)\};", re.S)


@functools.lru_cache(maxsize=None)
def marts():
    """Every item a mart sells: (split, table, item constant)."""
    text = _read("include", "data", "mart_items.h")
    common = text[text.index("PokeMartCommonItems"):]
    common = common[:common.index("};")]
    out = [(MART_TIER_SPLIT[int(tier, 0)], "common", item) for item, tier in _COMMON.findall(common)]
    for table, body in _TABLE.findall(text):
        city = next((c for c in MART_TABLE_SPLIT if table.startswith(c)), None)
        for item in re.findall(r"ITEM_\w+", body):
            out.append((MART_TABLE_SPLIT.get(city), table, item))
    # The Veilstone Game Corner's prize counter sells for coins, which money
    # buys, so it opens with Veilstone.
    prizes = _read("src", "scrcmd_game_corner_prize.c")
    for item in re.findall(r"\{ (ITEM_\w+), \d+ \}", prizes):
        out.append(("Maylene", "GameCornerPrizes", item))
    return out


@functools.lru_cache(maxsize=None)
def _item_names():
    return _read("generated", "items.txt").split()


def _item(token):
    return _item_names()[int(token)] if token.isdigit() else token


def items():
    """Every item ball and hidden item: (split, map, item constant, how)."""
    return [(split, header, item, how) for split, header, item, how, _needs in item_reach()]


# Tiles the player crosses only by Surf: the ones the game flags surfable
# (map_tile_behavior.c's flag table), less the bridges over water, which it
# flags so the player can surf beneath them but which are walked (or, the
# bike bridges, ridden) across. A waterfall needs Waterfall as well, and a
# Rock Climb wall, which carries the collision bit, needs Rock Climb.
_TILE_FLAG = re.compile(r"\[(TILE_BEHAVIOR_\w+)\]\s*=\s*(TILE_BEHAVIOR_FLAG_\w+)")
WATERFALL = "TILE_BEHAVIOR_WATERFALL"
ROCK_CLIMB = ("TILE_BEHAVIOR_ROCK_CLIMB_N_S", "TILE_BEHAVIOR_ROCK_CLIMB_E_W")
# The Bicycle's tiles: ramps (which carry the collision bit), slopes and
# narrow bridges, ridden only. A bike bridge over water is surfed beneath.
BIKE_PARKING = "TILE_BEHAVIOR_BIKE_PARKING"
# Ian's split definition (progression.py, 2026-09-21): Gardenia's split has
# no bike. The Cycle Shop's gift waits on the Galactic building in Eterna,
# which the story clears in Fantina's split.
BICYCLE_FROM = "Fantina"
# The objects on a map that a field move clears (a boulder, pushed aside).
OBSTACLES = {"OBJ_EVENT_GFX_ROCK_SMASH": "Rock Smash", "OBJ_EVENT_GFX_CUT_TREE": "Cut",
             "OBJ_EVENT_GFX_STRENGTH_BOULDER": "Strength"}
# The field moves that open a way: the HM that teaches each, and the name of
# its check in field_move_tasks.c, which names the badge it asks for. The
# Bicycle is a key item with no badge.
FIELD_MOVES = {"Bicycle": ("ITEM_BICYCLE", None), "Rock Smash": ("ITEM_HM06", "RockSmash"), "Cut": ("ITEM_HM01", "Cut"),
               "Surf": ("ITEM_HM03", "Surf"), "Strength": ("ITEM_HM04", "Strength"),
               "Rock Climb": ("ITEM_HM08", "RockClimb"), "Waterfall": ("ITEM_HM07", "Waterfall")}
# Each badge's gym; the badge is won as the gym's split closes.
BADGE_GYM = {"BADGE_ID_COAL": "Roark", "BADGE_ID_FOREST": "Gardenia", "BADGE_ID_RELIC": "Fantina",
             "BADGE_ID_COBBLE": "Maylene", "BADGE_ID_FEN": "Wake", "BADGE_ID_MINE": "Byron",
             "BADGE_ID_ICICLE": "Candice", "BADGE_ID_BEACON": "Volkner"}
_CHECK = re.compile(r"FieldMoves_Check(\w+)\(const FieldMoveContext \*fieldMoveContext\)\n\{(.*?)\n\}",
                    re.S)


@functools.lru_cache(maxsize=None)
def _surf_flagged():
    return {name for name, flag in _TILE_FLAG.findall(_read("src", "map_tile_behavior.c"))
            if "SURFABLE" in flag}


def _surfable():
    return {name for name in _surf_flagged() if "BRIDGE" not in name}


def _bike_tile(behaviour):
    return behaviour.startswith("TILE_BEHAVIOR_BIKE_") and behaviour != BIKE_PARKING


@functools.lru_cache(maxsize=None)
def surf_split():
    """The split Surf is usable in, as the encounter tool has it (the HM is
    Celestic Town's, so Byron's). field_move_splits works it out again from
    the game, and test_b1 checks that the two agree."""
    from ..encounters import model, progression
    return progression.rod_split(model.load_sidecar() or {}, "surf")


@functools.lru_cache(maxsize=None)
def field_move_badges():
    """{move: the badge its field check asks for}, read from the game."""
    checks = {name: re.search(r"BADGE_ID_\w+", body)
              for name, body in _CHECK.findall(_read("src", "field_move_tasks.c"))}
    return {move: checks[check].group(0) for move, (_hm, check) in FIELD_MOVES.items()
            if checks.get(check)}


@functools.lru_cache(maxsize=None)
def field_move_splits():
    """{move: the first split it can be used in}: the later of the split its
    HM is first in hand (a script's gift, a mart, or a ball or hidden item
    reached on foot) and the split after its badge's gym."""
    first = {}

    def seen(split, item):
        if split in SPLITS and (item not in first or SPLITS.index(split) < SPLITS.index(first[item])):
            first[item] = split
    for split, _h, item in gifts():
        seen(split, item)
    for split, _t, item in marts():
        seen(split, item)
    for _key, (split, _h, item, _how, needs) in _item_copies(((None, frozenset()),)):
        if needs == "foot":
            seen(split, item)
    out = {}
    for move, (hm, check) in FIELD_MOVES.items():
        gym = BADGE_GYM.get(field_move_badges().get(move))
        if hm in first and check is None:
            out[move] = max(first[hm], BICYCLE_FROM, key=SPLITS.index)
        elif hm in first and gym in SPLITS[:-1]:
            out[move] = max(first[hm], SPLITS[SPLITS.index(gym) + 1], key=SPLITS.index)
    return out


def _stages():
    """((split, the moves usable by then), ...) in split order, from walking
    with none."""
    usable = field_move_splits()
    out = [(None, frozenset())]
    for split in SPLITS:
        have = frozenset(m for m, s in usable.items() if SPLITS.index(s) <= SPLITS.index(split))
        if have != out[-1][1]:
            out.append((split, have))
    return tuple(out)


def _grid(header):
    """{(x, z): (collision, behaviour name)} for every tile of a map, in the
    event files' coordinates, and the set of its edge tiles. The map
    renderer's readers do the work, so the two cannot disagree."""
    sys.path.insert(0, os.path.join(data.ROOT, "tools", "oxide"))
    import maprender as mr  # noqa: E402
    import mapperm as mp  # noqa: E402
    _by_name, names = mp.behaviours()
    header = "MAP_HEADER_" + header
    chunks, global_coords = mr.chunks_of(header, mr.header_fields(header))
    r0 = min(r for r, _c, _n in chunks)
    c0 = min(c for _r, c, _n in chunks)
    gx0, gz0 = (c0 * mr.CHUNK, r0 * mr.CHUNK) if global_coords else (0, 0)
    out = {}
    for r, c, n in chunks:
        with open(mp.path_of(n), "rb") as f:
            raw = f.read()
        for lz in range(mr.CHUNK):
            for lx in range(mr.CHUNK):
                v = mp.read_tile(raw, lx, lz)
                out[(gx0 + (c - c0) * mr.CHUNK + lx, gz0 + (r - r0) * mr.CHUNK + lz)] = \
                    (v >> 15, names.get(v & 0xFF, ""))
    edge = {t for t in out if any((t[0] + dx, t[1] + dz) not in out
                                  for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)))}
    return out, edge


# A ledge: stepping onto it in its direction jumps the player past it, one
# way only, to the tile beyond (two beyond for a double ledge). Ledges carry
# the collision bit, so without this the flood takes them for walls.
_STEPS = {"EAST": (1, 0), "WEST": (-1, 0), "NORTH": (0, -1), "SOUTH": (0, 1)}
_LEDGES = {f"TILE_BEHAVIOR_JUMP_{d}{twice}": (step, 2 if twice else 1)
           for d, step in _STEPS.items() for twice in ("", "_TWICE")}


def _flood(grid, starts, ok):
    """The tiles reachable from the start tiles through tiles `ok` passes,
    jumping down ledges; `ok` takes a tile's position and its (collision,
    behaviour)."""
    seen = {t for t in starts if t in grid and ok(t, grid[t])}
    todo = list(seen)
    while todo:
        x, z = todo.pop()
        for dx, dz in _STEPS.values():
            t = (x + dx, z + dz)
            if t not in grid:
                continue
            ledge = _LEDGES.get(grid[t][1])
            if ledge:
                (lx, lz), n = ledge
                if (lx, lz) != (dx, dz):
                    continue
                t = (t[0] + lx * n, t[1] + lz * n)
                if t not in grid or grid[t][1] in _LEDGES:
                    continue
            if t not in seen and ok(t, grid[t]):
                seen.add(t)
                todo.append(t)
    return seen


def _passable(moves, blocked):
    """Whether a tile can be crossed with `moves` in hand: not a wall, not an
    obstacle whose move is missing, and not water, a waterfall, a Rock Climb
    wall or a bike ramp, slope or narrow bridge without the move for it."""
    surf = _surfable()

    def ok(pos, tile):
        collision, behaviour = tile
        if blocked.get(pos, "") and blocked[pos] not in moves:
            return False
        if behaviour in ROCK_CLIMB:
            return "Rock Climb" in moves
        if _bike_tile(behaviour):
            return "Bicycle" in moves or ("Surf" in moves and behaviour in _surf_flagged())
        if collision:
            return False
        if behaviour == WATERFALL:
            return {"Surf", "Waterfall"} <= moves
        return behaviour not in surf or "Surf" in moves
    return ok


def _reach(header, warps, blocked, spots, stages):
    """{(x, z): (the index in `stages` of the first stage whose moves reach
    a tile at or beside it from the map's warps and edges, and the moves
    that stage opened that it needs), or (None, None)}. A move is needed
    when the stage without it does not reach the spot; where no single one
    is, all the stage opened are named. A map the readers cannot lay out
    counts as walked."""
    try:
        grid, edge = _grid(header)
    except (SystemExit, OSError, KeyError, ValueError):
        return {s: (0, frozenset()) for s in spots}

    def near(spot, reached):
        x, z = spot
        return bool({(x, z), (x + 1, z), (x - 1, z), (x, z + 1), (x, z - 1)} & reached)
    out = {s: (None, None) for s in spots}
    for i, (_split, moves) in enumerate(stages):
        reached = _flood(grid, warps | edge, _passable(moves, blocked))
        new = [s for s in spots if out[s][0] is None and near(s, reached)]
        opened = moves - stages[i - 1][1] if i else frozenset()
        needed = {s: set() for s in new}
        if len(opened) > 1:
            for m in opened:
                without = _flood(grid, warps | edge, _passable(moves - {m}, blocked))
                for s in new:
                    if not near(s, without):
                        needed[s].add(m)
        for s in new:
            out[s] = (i, frozenset(needed[s] or opened))
        if all(v[0] is not None for v in out.values()):
            break
    return out


@functools.lru_cache(maxsize=None)
def item_reach():
    """Every item ball and hidden item: (split, map, item constant, how,
    needs). An item behind water, a waterfall, a Rock Climb wall, or a Rock
    Smash rock, Cut tree or Strength boulder, or on a bike path, counts
    from the later of its
    map's split and the split the field moves that reach it are first usable
    in (field_move_splits); `needs` names the move that last opened the way,
    "foot" for none. The census had Lake Verity's TM38 in Roark's split.
    The flood follows ledges down, and the Bicycle's ramps, slopes and
    narrow bridges from the split the bike is had in. "unreached" is an item
    the flood reaches with nothing in hand (a fenced pen, a cave's upper
    level it cannot see the way to); it has no split, so no count takes it,
    and test_b1 names each one.

    An item on several maps under one pickup flag is one item: a lake and
    its drained or low-water variant, two Old Chateau rooms, a hidden item on
    the seam of two maps (where one copy lies off its map's tiles). It
    counts once, from the copy reached in the earliest split, a copy the
    flood reaches before one it does not. Before this, 17 copies counted
    twice, and Lake Verity's sealed low-water copy kept TM38 in Roark's."""
    return [row for row, _maps in pickups().values()]


@functools.lru_cache(maxsize=None)
def pickups():
    """{pickup key: (the item_reach row, every map a copy is on)}."""
    copies = collections.defaultdict(list)
    for key, row in _item_copies(_stages()):
        copies[key].append(row)

    def rank(row):
        return (row[4] == "unreached", SPLITS.index(row[0]) if row[0] in SPLITS else len(SPLITS))
    return {key: (min(rows, key=rank), sorted({r[1] for r in rows})) for key, rows in copies.items()}


def _item_copies(stages):
    """[(pickup key, (split, map, item, how, needs))] for every copy of every
    item ball and hidden item, reached through `stages` (_stages). A ball's
    key is its hidden flag, a hidden item's its script (the flag follows
    from it)."""
    visible = {int(n): _item(tok) for n, tok in
               _VISIBLE.findall(_script("scripts_visible_items"))}
    # A hidden item's bg event script is 8000 plus its obtained-flag's offset
    # from HIDDEN_ITEM_FLAGS_START, not its position in gHiddenItems. The
    # flag numbers come from the tree's own flag list (flag_values).
    flags = flag_values()
    start = flags["HIDDEN_ITEM_FLAGS_START"]
    hidden = {flags[flag] - start: item for item, flag in
              _HIDDEN.findall(_read("include", "data", "field", "hidden_items.h"))}
    out = []
    for header, fields in headers().items():
        events = fields.get("eventsArchiveID")
        path = os.path.join(data.ROOT, "res", "field", "events", f"{events}.json") if events else None
        if not path or not os.path.exists(path):
            continue
        with open(path, encoding="utf-8") as f:
            ev = json.load(f)
        split = map_split(header)[0]
        found = []
        for obj in ev.get("object_events", []):
            script = obj.get("script")
            if isinstance(script, int) and VISIBLE_ITEM_SCRIPT <= script < HIDDEN_ITEM_SCRIPT:
                key = obj.get("hidden_flag") or (header, script, obj["x"], obj["z"])
                found.append((key, visible.get(script - VISIBLE_ITEM_SCRIPT), "ball", obj["x"], obj["z"]))
        for bg in ev.get("bg_events", []):
            script = bg.get("script")
            if bg.get("type") == BG_HIDDEN_ITEM and isinstance(script, int):
                found.append((script, hidden.get(script - HIDDEN_ITEM_SCRIPT), "hidden", bg["x"], bg["z"]))
        if not found:
            continue
        blocked = {(o["x"], o["z"]): OBSTACLES[o.get("graphics_id")] for o in ev.get("object_events", [])
                   if o.get("graphics_id") in OBSTACLES}
        reach = _reach(header, {(w["x"], w["z"]) for w in ev.get("warp_events", [])}, blocked,
                       {(x, z) for _k, _i, _h, x, z in found}, stages)
        for key, item, how, x, z in found:
            i, moves = reach[(x, z)]
            at, needs = None, "unreached"
            if i == 0:
                at, needs = split, "foot"
            elif i is not None:
                needs = " and ".join(sorted(moves))
                at = max(split, stages[i][0], key=SPLITS.index) if split in SPLITS else split
            out.append((key, (at, header, item, how, needs)))
    return out


def main(argv=None):
    by_how = collections.Counter(map_split(h)[1] for h in headers())
    print(f"{len(headers())} maps: " + ", ".join(f"{n} {how}" for how, n in by_how.most_common()))
    print("unplaced locations:", sorted({location_name(h) for h in headers()
                                         if map_split(h)[0] is None}))
    placed = collections.Counter(trainer_split(t) for t in data.oxide_trainers())
    print("trainers by split:", {s: placed.get(s, 0) for s in SPLITS + [None]})
    ms = collections.Counter(sp for sp, _t, _i in marts())
    print("mart items by split:", {sp: ms.get(sp, 0) for sp in SPLITS + [None]})
    wx = collections.Counter((map_split(h)[0], battle_weather(h)) for h in headers() if battle_weather(h))
    print("maps with battle weather:", {sp: {w: n for (s2, w), n in wx.items() if s2 == sp}
                                        for sp in SPLITS if any(s2 == sp for s2, _w in wx)})
    gs = collections.Counter(sp for sp, _h, _i in gifts())
    print("gifts by split:", {sp: gs.get(sp, 0) for sp in SPLITS + [None]})
    it = collections.Counter((s, how) for s, _h, _i, how in items())
    print("items by split:", {s: (it.get((s, "ball"), 0), it.get((s, "hidden"), 0)) for s in SPLITS + [None]})
    return 0


if __name__ == "__main__":
    sys.exit(main())

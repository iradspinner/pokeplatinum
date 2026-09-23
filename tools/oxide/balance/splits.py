"""B1d: which split every map, trainer and item belongs to in Oxide.

    PYTHONPATH=. python3 -m tools.oxide.balance.splits

A split is the stretch of the game before a gym, named for its leader
(Roark to Volkner), then League and Post. A map belongs to the split in
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
          "Volkner", "League", "Post"]

# Maps whose location name or position would place them wrong. Checked
# against the story fights fought on them.
MAP_SPLITS = {
    "ETERNA_CITY_GALACTIC_BUILDING": "Fantina",   # Jupiter 1, after Gardenia
    "GALACTIC_HQ": "Volkner",
    "VEILSTONE_CITY_GALACTIC_WAREHOUSE": "Volkner",
    "POKEMON_LEAGUE": "League",
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
    "Galactic HQ": "Volkner", "Spear Pillar": "Volkner", "Distortion World": "Volkner",
    "Sunyshore City": "Volkner", "Sunyshore Market": "Volkner", "Vista Lighthouse": "Volkner",
    "Pokémon League": "League",
    "Fight Area": "Post", "Survival Area": "Post", "Resort Area": "Post", "Villa": "Post",
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
_FLAG = re.compile(r"#define (FLAG_OBTAINED_HIDDEN_\w+|HIDDEN_ITEM_FLAGS_START)\s+(\d+)")
VISIBLE_ITEM_SCRIPT, HIDDEN_ITEM_SCRIPT = 7000, 8000
BG_HIDDEN_ITEM = 2   # bg event type; the others are signs and triggers


def _read(*rel):
    with open(os.path.join(data.ROOT, *rel), encoding="utf-8") as f:
        return f.read()


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
                with open(path, encoding="utf-8") as f:
                    for command, operands in _BATTLE.findall(f.read()):
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
            for const in set(_TRAINER_REF.findall(_read("res", "field", "scripts", f"{scripts}.s"))):
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
        for const in set(_TRAINER_REF.findall(_read("res", "field", "scripts", f"{stem}.s"))):
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
        for line in _read("res", "field", "scripts", f"{scripts}.s").split("\n"):
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
# eight. The split a tier opens in is the split after that many badges.
MART_TIER_SPLIT = {1: "Roark", 2: "Gardenia", 3: "Maylene", 4: "Byron", 5: "Volkner", 6: "League"}
# Each specialty stock, by the start of its table name, to its city's split.
MART_TABLE_SPLIT = {
    "Jubilife": "Roark", "Oreburgh": "Roark", "Floaroma": "Gardenia", "Eterna": "Gardenia",
    "Hearthome": "Fantina", "Solaceon": "Maylene", "Veilstone": "Maylene", "Pastoria": "Wake",
    "Celestic": "Byron", "Canalave": "Byron", "Snowpoint": "Candice", "Sunyshore": "Volkner",
    "PokemonLeague": "League",
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


@functools.lru_cache(maxsize=None)
def items():
    """Every item ball and hidden item: (split, map, item constant, how)."""
    visible = {int(n): _item(tok) for n, tok in
               _VISIBLE.findall(_read("res", "field", "scripts", "scripts_visible_items.s"))}
    # A hidden item's bg event script is 8000 plus its obtained-flag's offset
    # from HIDDEN_ITEM_FLAGS_START, not its position in gHiddenItems. The
    # flag numbers come from the build's generated header.
    flags = dict(_FLAG.findall(_read("build", "generated", "vars_flags.h")))
    start = int(flags["HIDDEN_ITEM_FLAGS_START"])
    hidden = {int(flags[flag]) - start: item for item, flag in
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
        for obj in ev.get("object_events", []):
            script = obj.get("script")
            if isinstance(script, int) and VISIBLE_ITEM_SCRIPT <= script < HIDDEN_ITEM_SCRIPT:
                out.append((split, header, visible.get(script - VISIBLE_ITEM_SCRIPT), "ball"))
        for bg in ev.get("bg_events", []):
            script = bg.get("script")
            if bg.get("type") == BG_HIDDEN_ITEM and isinstance(script, int):
                out.append((split, header, hidden.get(script - HIDDEN_ITEM_SCRIPT), "hidden"))
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

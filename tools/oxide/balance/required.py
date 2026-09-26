"""B1e: which trainers the player cannot walk around.

    PYTHONPATH=. python3 -m tools.oxide.balance.required            # the report
    PYTHONPATH=. python3 -m tools.oxide.balance.required ROUTE_202  # one map's trainers

A trainer is required on a crossing of its map when no walkable path from
where the player enters to where they must leave avoids every tile it sees.
Each trainer is tested alone: the others' sight lines are allowed, since the
question is whether this one can be skipped.

What the game does, and where this reads it:

- A trainer sees along its facing, up to the range in its event record
  (data[0]), and the line stops at the first tile with terrain collision or
  an object on it (trainer_encounter.c, IsPathInterrupted). Only
  TRAINER_TYPE_NORMAL and VIEW_ALL_DIRECTIONS trainers look at all
  (GetTrainerType); the turning and spinning types count as normal and
  see whichever way they face at the time.
- A tile with bit 15 set is solid, except that Rock Climb walls carry it
  too. Water needs Surf, a waterfall Waterfall, a bike bridge or slope the
  bike. A ledge tile is jumped: stepping onto it in its direction lands one
  tile beyond, and it cannot be entered from any other side
  (player_move.c, PlayerAvatar_WillJump).
- Objects block. Cut trees, breakable rocks and Strength boulders stop
  blocking once the split's field moves allow them. An object that a story
  flag hides is taken as gone, and one with no flag as always there.

Limits, which the report names per map rather than hiding:

- A trainer that turns or walks sees more than one line; it is scored as
  seeing every direction it can face, from where it starts, so it may come
  out required when a well-timed player could slip past.
- The field is read flat. Bridges (Route 206's Cycling Road over the path
  below) are two levels in the game and one here.
- Gyms with moving parts (every gym after Roark's), multi-floor dungeons
  and the Galactic HQ are not modelled, and nor are battles a script
  starts with no sight line.
- The crossings are a hand table of the story path (CROSSINGS), from
  vanilla Platinum's route. A route the story does not send the player
  along is off the path, so all its trainers are avoidable by not going.
"""
import collections
import functools
import sys

from . import data
from . import world

SPLITS = ["Roark", "Gardenia", "Fantina", "Maylene", "Wake", "Byron", "Candice",
          "HQ", "Galactic", "Volkner", "League"]

# The first split in which each field ability can open a path: the later of
# the split its HM or item is found in (splits.gifts and splits.items, B1d)
# and the split after the badge that allows it outside battle
# (field_move_tasks.c). Rock Smash: HM06 in Oreburgh Gate, Coal Badge. Cut:
# HM01 in Eterna, Forest Badge. The bike: the Cycle Shop hands it over
# after the Galactic building, which is Fantina's split (Jupiter 1). Surf:
# HM03 at Celestic, Relic Badge. Strength: HM04 on Iron Island, Mine Badge.
# Rock Climb: HM08 on Route 217, Icicle Badge. Waterfall: HM07 in
# Sunyshore, Beacon Badge.
ABILITY_SPLIT = {"rock_smash": "Gardenia", "cut": "Fantina", "bike": "Fantina",
                 "surf": "Byron", "strength": "Candice", "rock_climb": "HQ",
                 "waterfall": "League"}

WATER = {"WATER_SEA", "WATER_RIVER", "DEEP_WATER", "WATER_CAVE"}
BIKE = {"BIKE_BRIDGE_N_S", "BIKE_BRIDGE_E_W", "BIKE_BRIDGE_E_W_OVER_WATER",
        "BIKE_BRIDGE_N_S_OVER_SAND", "BIKE_BRIDGE_E_W_OVER_SAND", "BIKE_SLOPE_TOP",
        "BIKE_SLOPE_BOTTOM", "BIKE_RAMP_WESTWARD", "BIKE_RAMP_EASTWARD"}
ROCK_CLIMB = {"ROCK_CLIMB_N_S": "NS", "ROCK_CLIMB_E_W": "EW"}
JUMPS = {"JUMP_NORTH": "N", "JUMP_SOUTH": "S", "JUMP_WEST": "W", "JUMP_EAST": "E"}
BRIDGES = {"BRIDGE", "BRIDGE_START", "BRIDGE_OVER_WATER", "BRIDGE_OVER_SNOW",
           "BRIDGE_OVER_SAND"}
OBSTACLES = {"OBJ_EVENT_GFX_CUT_TREE": "cut", "OBJ_EVENT_GFX_ROCK_SMASH": "rock_smash",
             "OBJ_EVENT_GFX_STRENGTH_BOULDER": "strength"}
SEEING_TYPES = {"TRAINER_TYPE_NORMAL", "TRAINER_TYPE_VIEW_ALL_DIRECTIONS",
                "TRAINER_TYPE_FACE_SIDES", "TRAINER_TYPE_FACE_COUNTERCLOCKWISE",
                "TRAINER_TYPE_FACE_CLOCKWISE", "TRAINER_TYPE_SPIN_COUNTERCLOCKWISE",
                "TRAINER_TYPE_SPIN_CLOCKWISE"}
WORD_DIR = {"NORTH": "N", "SOUTH": "S", "WEST": "W", "EAST": "E"}

# The story path's crossings of maps that hold trainers, in play order:
# (split, map, where the player comes from, where they must get to). An end
# is a neighbouring header on the overworld, the header a warp leads to, or
# "@LOCALID" for the tiles beside an object. "A|B" means either will do.
CROSSINGS = [
    ("Roark", "ROUTE_202", "SANDGEM_TOWN", "JUBILIFE_CITY"),
    ("Roark", "ROUTE_203", "JUBILIFE_CITY", "OREBURGH_GATE_1F"),
    ("Roark", "OREBURGH_GATE_1F", "ROUTE_203", "OREBURGH_CITY"),
    ("Roark", "OREBURGH_MINE_B2F", "OREBURGH_MINE_B1F", "@LOCALID_ROARK"),
    ("Roark", "OREBURGH_CITY_GYM", "OREBURGH_CITY", "@LOCALID_ROARK"),
    ("Gardenia", "ROUTE_204_SOUTH", "JUBILIFE_CITY", "RAVAGED_PATH|ROUTE_204_NORTH"),
    ("Gardenia", "ROUTE_204_NORTH", "RAVAGED_PATH|ROUTE_204_SOUTH", "FLOAROMA_TOWN"),
    ("Gardenia", "ROUTE_205_SOUTH", "FLOAROMA_TOWN", "VALLEY_WINDWORKS_OUTSIDE"),
    ("Gardenia", "VALLEY_WINDWORKS_BUILDING", "VALLEY_WINDWORKS_OUTSIDE", "@LOCALID_MARS"),
    ("Gardenia", "ROUTE_205_SOUTH", "VALLEY_WINDWORKS_OUTSIDE", "ETERNA_FOREST"),
    ("Gardenia", "ETERNA_FOREST", "ROUTE_205_SOUTH", "ROUTE_205_NORTH"),
    ("Gardenia", "ROUTE_205_NORTH", "ETERNA_FOREST", "ETERNA_CITY"),
    ("Fantina", "TEAM_GALACTIC_ETERNA_BUILDING_1F", "ETERNA_CITY", "TEAM_GALACTIC_ETERNA_BUILDING_2F"),
    ("Fantina", "TEAM_GALACTIC_ETERNA_BUILDING_2F", "TEAM_GALACTIC_ETERNA_BUILDING_1F",
     "TEAM_GALACTIC_ETERNA_BUILDING_3F"),
    ("Fantina", "TEAM_GALACTIC_ETERNA_BUILDING_3F", "TEAM_GALACTIC_ETERNA_BUILDING_2F",
     "TEAM_GALACTIC_ETERNA_BUILDING_4F"),
    ("Fantina", "ROUTE_206", "ETERNA_CITY|ROUTE_206_CYCLING_ROAD_NORTH_GATE", "ROUTE_207"),
    ("Fantina", "ROUTE_207", "ROUTE_206", "MT_CORONET_1F_SOUTH"),
    ("Fantina", "ROUTE_208", "MT_CORONET_1F_SOUTH", "HEARTHOME_CITY|ROUTE_208_GATE_TO_HEARTHOME_CITY"),
    ("Maylene", "ROUTE_209", "HEARTHOME_CITY|ROUTE_209_GATE_TO_HEARTHOME_CITY", "SOLACEON_TOWN"),
    ("Maylene", "ROUTE_210_SOUTH", "SOLACEON_TOWN", "ROUTE_215"),
    ("Maylene", "ROUTE_215", "ROUTE_210_SOUTH", "VEILSTONE_CITY|ROUTE_215_GATE_TO_VEILSTONE_CITY"),
    ("Wake", "ROUTE_214", "VEILSTONE_CITY|ROUTE_214_GATE_TO_VEILSTONE_CITY", "VALOR_LAKEFRONT"),
    ("Wake", "ROUTE_213", "VALOR_LAKEFRONT", "PASTORIA_CITY|ROUTE_213_GATE_TO_PASTORIA_CITY"),
    ("Byron", "ROUTE_210_SOUTH", "SOLACEON_TOWN", "ROUTE_210_NORTH"),
    ("Byron", "ROUTE_210_NORTH", "ROUTE_210_SOUTH", "CELESTIC_TOWN"),
    ("Byron", "ROUTE_218", "JUBILIFE_CITY|ROUTE_218_GATE_TO_JUBILIFE_CITY",
     "CANALAVE_CITY|ROUTE_218_GATE_TO_CANALAVE_CITY"),
    ("Byron", "IRON_ISLAND_B2F_LEFT_ROOM", "IRON_ISLAND_B1F_RIGHT_ROOM", "IRON_ISLAND_B3F"),
    ("Candice", "LAKE_VALOR_DRAINED", "VALOR_LAKEFRONT", "VALOR_CAVERN"),
    ("Candice", "LAKE_VERITY", "VERITY_LAKEFRONT", "@LOCALID_MARS"),
    ("Candice", "ROUTE_216", "MT_CORONET_1F_NORTH_ROOM_2", "ROUTE_217"),
    ("Candice", "ROUTE_217", "ROUTE_216", "ACUITY_LAKEFRONT"),
    ("Volkner", "ROUTE_222", "VALOR_LAKEFRONT", "SUNYSHORE_CITY|ROUTE_222_GATE_TO_SUNYSHORE_CITY"),
    ("League", "ROUTE_223", "SUNYSHORE_CITY", "POKEMON_LEAGUE"),
]

# Objects a story flag hides that stand in the way until a split: the
# Psyduck on Route 210 South leave once Cynthia's SecretPotion is used, on
# the way to Celestic in Byron's split.
STORY_BLOCKERS = {
    "ROUTE_210_SOUTH": {f"LOCALID_PSYDUCK_{i}": "Byron" for i in range(1, 5)},
}

# Maps with trainers that the table leaves out, and why.
NOT_MODELLED = {
    "gym with moving parts": ["HEARTHOME_CITY_GYM_", "HEARTHOME_CITY_DP_GYM_", "VEILSTONE_CITY_GYM",
                              "PASTORIA_CITY_GYM", "CANALAVE_CITY_GYM", "SNOWPOINT_CITY_GYM",
                              "SUNYSHORE_CITY_GYM_", "ETERNA_CITY_GYM"],
    "multi-floor dungeon": ["GALACTIC_HQ_", "VICTORY_ROAD_", "MT_CORONET_", "IRON_ISLAND_B1F",
                            "IRON_ISLAND_B2F_RIGHT", "WAYWARD_CAVE_", "SOLACEON_RUINS_",
                            "ROUTE_209_LOST_TOWER_", "OREBURGH_GATE_B1F", "STARK_MOUNTAIN_"],
}


def abilities(split):
    """The field abilities the player has in a split."""
    i = SPLITS.index(split)
    return {a for a, s in ABILITY_SPLIT.items() if SPLITS.index(s) <= i}


class Field:
    """One map as the player crosses it in one split."""

    def __init__(self, header, split):
        self.header, self.split = header, split
        self.tiles = world.tiles(header)
        self.can = abilities(split)
        self.objects = {}      # tile -> object record, for everything that blocks
        self.trainers = []     # trainer object records
        for o in world.events(header)["object_events"]:
            xz = (o["x"], o["z"])
            gate = OBSTACLES.get(o["graphics_id"])
            if gate:
                if gate not in self.can:
                    self.objects[xz] = o
                continue
            script = str(o["script"])
            if script.startswith("TRAINER_") and o.get("trainer_type") in SEEING_TYPES:
                self.trainers.append(o)
                self.objects[xz] = o
            elif self._blocks(o):
                self.objects[xz] = o

    def _blocks(self, o):
        """Whether a non-trainer object stands in the way in this split."""
        gone = STORY_BLOCKERS.get(self.header, {}).get(o["id"])
        if gone:
            return SPLITS.index(self.split) < SPLITS.index(gone)
        return (str(o.get("hidden_flag", "0")) == "0"
                and o.get("trainer_type") != "TRAINER_TYPE_UNK_003")

    def standable(self, xz):
        """Whether the player can end a step on this tile in this split."""
        if xz not in self.tiles or xz in self.objects:
            return False
        behavior, solid = self.tiles.attr(xz)
        if behavior in JUMPS:
            return False
        if behavior in ROCK_CLIMB:
            return "rock_climb" in self.can
        if behavior in WATER:
            return "surf" in self.can
        if behavior == "WATERFALL":
            return "waterfall" in self.can
        if behavior in BIKE:
            return "bike" in self.can and not solid
        return not solid

    def steps(self, xz):
        """Tiles reachable from this one in one move, ledges included."""
        for d, (dx, dz) in world.DIRS.items():
            nxt = (xz[0] + dx, xz[1] + dz)
            attr = self.tiles.attr(nxt)
            if attr and JUMPS.get(attr[0]) == d:
                land = (nxt[0] + dx, nxt[1] + dz)
                if self.standable(land):
                    yield land
            elif self.standable(nxt):
                yield nxt

    def sight(self, trainer):
        """The tiles a trainer sees from where it stands."""
        rng = (trainer.get("data") or [0])[0]
        seen = set()
        for d in facing(trainer):
            dx, dz = world.DIRS[d]
            x, z = trainer["x"], trainer["z"]
            for _ in range(rng):
                x, z = x + dx, z + dz
                attr = self.tiles.attr((x, z))
                if attr is None or attr[1] or (x, z) in self.objects:
                    break
                seen.add((x, z))
        return seen

    def ends(self, spec):
        """The tiles an end of a crossing stands for."""
        out = set()
        for part in spec.split("|"):
            if part.startswith("@"):
                obj = next(o for o in world.events(self.header)["object_events"] if o["id"] == part[1:])
                out |= {(obj["x"] + dx, obj["z"] + dz) for dx, dz in world.DIRS.values()}
            else:
                out |= world.warps_to(self.header, part)
                if self.tiles.overworld:
                    out |= self.tiles.touching(part)
        return out

    def links(self):
        """Groups of warps into one building, which the player walks
        through: a building with two doors onto this map is a passage (a
        route gate, or Hotel Grand Lake's lobby on Route 213)."""
        by_dest = collections.defaultdict(set)
        for w in world.events(self.header)["warp_events"]:
            # Only gates and lobbies: a cave with two mouths on one route
            # (Mt. Coronet on Route 208) may need a field move inside.
            if "_GATE" in w["dest_header_id"] or w["dest_header_id"].endswith("_LOBBY"):
                by_dest[w["dest_header_id"]].add((w["x"], w["z"]))
        # Two doors side by side are one wide door, not a passage.
        return [tiles for tiles in by_dest.values()
                if len(tiles) > 1 and max(abs(a[0] - b[0]) + abs(a[1] - b[1])
                                          for a in tiles for b in tiles) > 1]

    def reach(self, start, avoid=frozenset()):
        """Every tile the player can stand on from start without standing
        on a tile in avoid. Warp tiles in start count as standable."""
        warps = {(w["x"], w["z"]) for w in world.events(self.header)["warp_events"]}
        links = self.links()
        frontier = [xz for xz in start if xz not in avoid and (self.standable(xz) or xz in warps)]
        seen = set(frontier)
        while frontier:
            xz = frontier.pop()
            nxt = list(self.steps(xz))
            for d in world.DIRS.values():
                w = (xz[0] + d[0], xz[1] + d[1])
                if w in warps:
                    nxt.append(w)
            for group in links:
                if xz in group:
                    nxt += list(group)
            for n in nxt:
                if n not in seen and n not in avoid:
                    seen.add(n)
                    frontier.append(n)
        return seen

    def path(self, start, goal, avoid=frozenset()):
        """Whether any tile of goal can be reached from start without
        standing on a tile in avoid."""
        return bool(self.reach(start, avoid) & goal)


def _adjacent(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1]) == 1


def facing(trainer):
    """Every direction a trainer can look in. A fixed look is one direction;
    LOOK_A_AND_B and the like are those; looking around, rotating, walking,
    wandering and the all-direction types are all four."""
    move = trainer["movement_type"][len("MOVEMENT_TYPE_"):]
    ttype = trainer.get("trainer_type")
    if ttype != "TRAINER_TYPE_NORMAL" or move.startswith(("LOOK_AROUND", "ROTATE", "WALK", "WANDER")):
        return set(world.DIRS)
    if move.startswith("LOOK_"):
        return {WORD_DIR[w] for w in move[len("LOOK_"):].split("_") if w in WORD_DIR}
    return {world.DIR_BY_NUMBER.get(trainer.get("initial_dir"), "S")}


def moves_or_turns(trainer):
    return len(facing(trainer)) > 1


@functools.lru_cache(maxsize=None)
def trainer_ids():
    return {t["constant"]: tr_id for tr_id, t in data.oxide_trainers().items()}


def crossing(split, header, src, dst):
    """[(trainer object, verdict)] for one crossing. The verdict is
    'required' or 'avoidable'; 'not reached' when the player cannot get
    near it on this crossing (it belongs to a later one); or 'no path',
    when even with no trainer in the way the ends do not connect, which is
    a limit of the model worth reading."""
    f = Field(header, split)
    start, goal = f.ends(src), f.ends(dst)
    if not start or not goal:
        raise ValueError(f"{header}: no tiles for {src if not start else dst}")
    reached = f.reach(start)
    if not reached & goal:
        return [(t, "no path") for t in f.trainers]
    out = []
    for t in f.trainers:
        near = f.sight(t) | {(t["x"] + dx, t["z"] + dz) for dx, dz in world.DIRS.values()}
        if not near & reached:
            out.append((t, "not reached"))
        else:
            out.append((t, "avoidable" if f.path(start, goal, frozenset(f.sight(t)))
                        else "required"))
    return out


def flat_limits(header):
    """What the map has that the flat model reads loosely."""
    t = world.tiles(header)
    notes = []
    if any(t.attr(xz)[0] in BRIDGES for xz in t):
        notes.append("bridges")
    return notes


@functools.lru_cache(maxsize=None)
def report():
    """[(split, header, trainer constant, tr_id, verdict, notes)] for every
    crossing, then [(header, reason, trainer constants)] for trainer maps
    left out."""
    rows = []
    for split, header, src, dst in CROSSINGS:
        limits = flat_limits(header)
        for t, verdict in crossing(split, header, src, dst):
            notes = list(limits) + (["turns or walks"] if moves_or_turns(t) else [])
            rows.append((split, header, t["script"], trainer_ids().get(t["script"]), verdict, notes))
    crossed = {h for _s, h, _a, _b in CROSSINGS}
    left = []
    from . import splits
    for header in sorted(splits.headers()):
        ts = [o["script"] for o in world.events(header)["object_events"]
              if str(o["script"]).startswith("TRAINER_") and o.get("trainer_type") in SEEING_TYPES]
        if not ts or header in crossed:
            continue
        reason = next((r for r, prefixes in NOT_MODELLED.items()
                       if header.startswith(tuple(prefixes))), "off the story path")
        left.append((header, reason, ts))
    return rows, left


def first_crossings():
    """{trainer constant: (split, header, verdict)} at the first crossing
    that reaches each trainer. This is also the split the player first
    meets it in, which is how B1e re-places the filler B1d put too early."""
    rows, _left = report()
    first = {}
    for split, header, const, tr_id, verdict, notes in rows:
        if verdict != "not reached":
            first.setdefault(const, (split, header, verdict))
    return first


def never_reached():
    """Trainers on crossed maps that no crossing reaches: they sit behind a
    field move or a story gate the story path never asks for."""
    rows, _left = report()
    first = first_crossings()
    return sorted({r[2] for r in rows if r[2] not in first})


def summary():
    """{split: Counter of verdicts}, each trainer at its first crossing."""
    out = collections.OrderedDict((s, collections.Counter()) for s in SPLITS)
    for split, _header, verdict in first_crossings().values():
        out[split][verdict] += 1
    return out


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    rows, left = report()
    if argv:
        for r in rows:
            if r[1] == argv[0]:
                print(f"{r[0]:9} {r[2]:45} {str(r[3]):>4} {r[4]:10} {', '.join(r[5])}")
        return 0
    for split, header, const, tr_id, verdict, notes in rows:
        print(f"{split:9} {header:34} {const:45} {verdict:10} {', '.join(notes)}")
    print()
    for split, c in summary().items():
        print(f"{split:9} " + ", ".join(f"{k} {v}" for k, v in sorted(c.items())))
    print(f"never reached on a crossing: {', '.join(never_reached())}")
    print()
    by_reason = collections.defaultdict(int)
    for header, reason, ts in left:
        by_reason[reason] += len(ts)
    for reason, n in by_reason.items():
        print(f"not modelled, {reason}: {n} trainers")
    return 0


if __name__ == "__main__":
    sys.exit(main())

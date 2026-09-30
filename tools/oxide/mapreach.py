#!/usr/bin/env python3
"""Walk one or more maps on foot and print their pockets: the areas the player
can reach without taking a warp, each with the warps and trainers in it, and
where each warp leads. Nothing here writes.

Platinum Oxide project. Written for the gauntlets (docs/oxide/gauntlets.md),
whose sections are drawn from these pockets: a section's way back, its way
forward and the detours whose dead ends keep its lock.

    python3 tools/oxide/mapreach.py GALACTIC_HQ_B2F GALACTIC_HQ_1F ...
    python3 tools/oxide/mapreach.py GALACTIC_HQ_3F --wall GALACTIC_HQ_3F:27,19

How a step is modelled, from the tile permissions maprender.py reads:
  - a tile with the collision bit is a wall, apart from a Rock Climb wall,
    which is climbed along its axis (pass --no-climb to wall it off);
  - a ledge (a JUMP_ tile) is taken only in its direction, landing beyond it;
  - a bridge tile is the deck when entered from a bridge end or from the deck,
    and the floor under the bridge otherwise; on the deck the player moves only
    along the bridge and steps off at an end;
  - objects are not walls: Strength boulders, Rock Smash rocks and locked
    doors are ignored unless a door's tiles are passed as --wall MAP:x,z.
A trainer counts as reached when a tile beside it is.
"""

import argparse
import json
import os
import re
import struct
import sys
from collections import deque

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "tools", "oxide"))
import maprender  # noqa: E402


def tile_behaviors():
    text = open(os.path.join(ROOT, "include/constants/field/map_tile_behaviors.h")).read()
    body = text[text.index("{") + 1:text.index("}")]
    values, n = {}, 0
    for line in body.split(","):
        line = re.sub(r"//.*", "", line).strip()
        if not line:
            continue
        if "=" in line:
            name, v = [s.strip() for s in line.split("=")]
            n = int(v, 0)
        else:
            name = line
        values[name] = n
        n += 1
    return values


B = tile_behaviors()
JUMP = {B["TILE_BEHAVIOR_JUMP_EAST"]: (1, 0), B["TILE_BEHAVIOR_JUMP_WEST"]: (-1, 0),
        B["TILE_BEHAVIOR_JUMP_NORTH"]: (0, -1), B["TILE_BEHAVIOR_JUMP_SOUTH"]: (0, 1)}
BRIDGE_START = B["TILE_BEHAVIOR_BRIDGE_START"]
BRIDGE = {v for k, v in B.items()
          if (k.startswith("TILE_BEHAVIOR_BRIDGE") or k.startswith("TILE_BEHAVIOR_BIKE_BRIDGE")) and v != BRIDGE_START}
# Rock Climb walls, and the axis (0 x, 1 z) they are climbed along.
CLIMB_AXIS = {B["TILE_BEHAVIOR_ROCK_CLIMB_N_S"]: 1, B["TILE_BEHAVIOR_ROCK_CLIMB_E_W"]: 0}
STEPS = ((1, 0), (-1, 0), (0, 1), (0, -1))


class MapWalk:
    def __init__(self, header, walls=(), climb=True):
        self.header = header
        fields = maprender.header_fields(header)
        chunks, global_coords = maprender.chunks_of(header, fields)
        r0 = min(r for r, _, _ in chunks)
        c0 = min(c for _, c, _ in chunks)
        self.grid = {}
        for r, c, num in chunks:
            path = os.path.join(ROOT, "res/field/maps/data/map_data_%03d.bin" % num)
            perm = maprender.split_land(open(path, "rb").read())[0]
            tiles = struct.unpack_from("<%dH" % (len(perm) // 2), perm)
            for i, t in enumerate(tiles):
                x, z = i % 32, i // 32
                # Overworld maps use matrix-global coordinates; the rest count from their first chunk.
                if global_coords:
                    self.grid[(c * 32 + x, r * 32 + z)] = t
                else:
                    self.grid[((c - c0) * 32 + x, (r - r0) * 32 + z)] = t
        events = os.path.join(ROOT, "res/field/events", fields["eventsArchiveID"] + ".json")
        ev = json.load(open(events, encoding="utf-8"))
        self.warps = ev["warp_events"]
        self.trainers = [(str(o["script"]), o["x"], o["z"]) for o in ev["object_events"]
                         if str(o["script"]).startswith("TRAINER_")]
        self.walls = set(walls)
        self.climb = climb

    def behavior(self, p):
        return self.grid[p] & 0xFF if p in self.grid else None

    def can_enter(self, p, d):
        t = self.grid.get(p)
        if t is None or p in self.walls:
            return False
        if (t & 0xFF) in CLIMB_AXIS:
            return self.climb and d[CLIMB_AXIS[t & 0xFF]] != 0
        return not t & 0x8000

    def moves(self, state):
        x, z, deck = state
        here = self.behavior((x, z))
        for d in STEPS:
            q = (x + d[0], z + d[1])
            if not self.can_enter(q, d):
                continue
            b = self.behavior(q)
            if deck:
                if b in BRIDGE:
                    yield (q[0], q[1], True)
                elif b == BRIDGE_START:
                    yield (q[0], q[1], False)
            elif b in JUMP:
                land = (q[0] + d[0], q[1] + d[1])
                if JUMP[b] == d and self.can_enter(land, d):
                    yield (land[0], land[1], False)
            elif b in BRIDGE:
                yield (q[0], q[1], here == BRIDGE_START)
            elif b == BRIDGE_START:
                if here not in BRIDGE:
                    yield (q[0], q[1], False)
            else:
                yield (q[0], q[1], False)

    def reach(self, x, z):
        start = (x, z, False)
        seen = {start}
        todo = deque([start])
        while todo:
            for t in self.moves(todo.popleft()):
                if t not in seen:
                    seen.add(t)
                    todo.append(t)
        return {(sx, sz) for sx, sz, _deck in seen}

    @staticmethod
    def touches(tiles, x, z):
        return (x, z) in tiles or any((x + dx, z + dz) in tiles for dx, dz in STEPS)

    def pockets(self):
        """[(warp indices, trainer constants)] for each pocket that holds a warp."""
        out, done = [], set()
        for i, w in enumerate(self.warps):
            if i in done:
                continue
            tiles = self.reach(w["x"], w["z"])
            ws = [j for j, v in enumerate(self.warps) if self.touches(tiles, v["x"], v["z"])]
            done |= set(ws)
            out.append((ws, [t for t, x, z in self.trainers if self.touches(tiles, x, z)]))
        return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("maps", nargs="+", help="map header names, with or without MAP_HEADER_")
    ap.add_argument("--wall", action="append", default=[], metavar="MAP:x,z",
                    help="treat this tile as a wall, such as a locked door (repeatable)")
    ap.add_argument("--no-climb", action="store_true", help="wall off Rock Climb walls")
    args = ap.parse_args()

    names = [m.replace("MAP_HEADER_", "") for m in args.maps]
    walls = {}
    for w in args.wall:
        m, xz = w.split(":")
        walls.setdefault(m.replace("MAP_HEADER_", ""), []).append(tuple(int(v) for v in xz.split(",")))

    pocket_of, listing = {}, []
    for m in names:
        walk = MapWalk("MAP_HEADER_" + m, walls.get(m, ()), climb=not args.no_climb)
        for ws, ts in walk.pockets():
            name = "%s%s" % (m, ws)
            for j in ws:
                pocket_of[(m, j)] = name
            listing.append((name, walk, ws, ts))

    for name, walk, ws, ts in listing:
        print(name + ("  trainers: " + ", ".join(t.replace("TRAINER_", "") for t in ts) if ts else ""))
        for j in ws:
            w = walk.warps[j]
            dest = w["dest_header_id"].replace("MAP_HEADER_", "")
            print("    #%-2d (%d,%d) -> %s" % (j, w["x"], w["z"],
                                            pocket_of.get((dest, w["dest_warp_id"]), "%s #%d" % (dest, w["dest_warp_id"]))))


if __name__ == "__main__":
    main()

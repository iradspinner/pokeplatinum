"""The field as the player walks it: tiles, collision, objects and warps.

B1e's ground layer. A map header's tiles come from its map matrix, a grid of
32 by 32 tile blocks. Each block is one land data file
(res/field/maps/data/map_data_NNN.bin), whose first section after a 16-byte
header is 1,024 u16 terrain attributes: the low byte is the tile behavior,
bit 15 is collision (terrain_collision_manager.c, include/constants/field/
map.h). The overworld is matrix 0, where every header owns the blocks its
cells name and event coordinates are global tiles; every other header has a
matrix of its own and local coordinates.

Reads res/, include/ and generated/; writes nothing.
"""
import functools
import json
import os
import re
import struct

from . import data

MATRICES = os.path.join(data.ROOT, "res", "field", "matrices")
LAND_DATA = os.path.join(data.ROOT, "res", "field", "maps", "data")
EVENTS = os.path.join(data.ROOT, "res", "field", "events")
BLOCK = 32
COLLISION = 0x8000
DIRS = {"N": (0, -1), "S": (0, 1), "W": (-1, 0), "E": (1, 0)}
# The game's direction numbers (MapObject facing, initial_dir in events).
DIR_BY_NUMBER = {0: "N", 1: "S", 2: "W", 3: "E"}


@functools.lru_cache(maxsize=None)
def behaviors():
    """{value: name without TILE_BEHAVIOR_} from the TileBehavior enum."""
    with open(os.path.join(data.ROOT, "include", "constants", "field", "map_tile_behaviors.h"),
              encoding="utf-8") as f:
        src = f.read()
    body = src[src.index("enum TileBehavior"):]
    body = body[:body.index("};")]
    out, value = {}, -1
    for m in re.finditer(r"^\s+TILE_BEHAVIOR_(\w+)(?:\s*=\s*(\w+))?,", body, re.M):
        value = int(m.group(2), 0) if m.group(2) else value + 1
        out[value] = m.group(1)
    return out


@functools.lru_cache(maxsize=None)
def block_attributes(map_id):
    """The 1,024 terrain attributes of one land data file, row by row."""
    path = os.path.join(LAND_DATA, f"map_data_{map_id:03d}.bin")
    with open(path, "rb") as f:
        head = f.read(16)
        size = struct.unpack("<i", head[:4])[0]
        assert size == BLOCK * BLOCK * 2, (path, size)
        return struct.unpack(f"<{BLOCK * BLOCK}H", f.read(size))


@functools.lru_cache(maxsize=None)
def matrix(matrix_id):
    with open(os.path.join(MATRICES, f"{matrix_id}.json"), encoding="utf-8") as f:
        return json.load(f)


@functools.lru_cache(maxsize=None)
def blocks(matrix_id):
    """{(block x, block z): (owning header or None, attributes)} for a
    matrix. A cell whose header is EVERYWHERE, or a matrix with no header
    grid, belongs to whichever header uses the matrix, shown as None."""
    m = matrix(matrix_id)
    grid = m.get("headers")
    out = {}
    for bz, row in enumerate(m["maps"]):
        for bx, map_name in enumerate(row):
            if not map_name.startswith("MAP_") or map_name == "MAP_NONE":
                continue
            cell = grid[bz][bx] if grid else None
            owner = cell[len("MAP_HEADER_"):] if cell and cell.startswith("MAP_HEADER_") else None
            out[(bx, bz)] = (None if owner == "EVERYWHERE" else owner,
                             block_attributes(int(map_name[len("MAP_"):])))
    return out


class Tiles:
    """The tiles one header owns, read on demand from its matrix's blocks."""

    def __init__(self, header):
        from . import splits
        self.header = header
        self.matrix_id = splits.headers()[header]["mapMatrixID"]
        self.overworld = self.matrix_id == "map_matrix_000"
        self._blocks = blocks(self.matrix_id)
        # On the overworld an EVERYWHERE cell is the open sea around the
        # region, which no header owns; elsewhere it is the header's own.
        self._default = None if self.overworld else header
        self.own = {b for b, (owner, _a) in self._blocks.items()
                    if (owner or self._default) == header}

    def owner(self, xz):
        b = self._blocks.get((xz[0] // BLOCK, xz[1] // BLOCK))
        if b is None:
            return None
        return b[0] or self._default

    def attr(self, xz):
        """(behavior name, collision) of any tile in the matrix, or None."""
        b = self._blocks.get((xz[0] // BLOCK, xz[1] // BLOCK))
        if b is None:
            return None
        a = b[1][(xz[1] % BLOCK) * BLOCK + xz[0] % BLOCK]
        return behaviors().get(a & 0xFF, hex(a & 0xFF)), bool(a & COLLISION)

    def __contains__(self, xz):
        return (xz[0] // BLOCK, xz[1] // BLOCK) in self.own

    def __iter__(self):
        for bx, bz in sorted(self.own):
            for i in range(BLOCK * BLOCK):
                yield (bx * BLOCK + i % BLOCK, bz * BLOCK + i // BLOCK)

    def touching(self, other):
        """Tiles of this header next to a tile the other header owns."""
        out = set()
        for (x, z) in self:
            for dx, dz in DIRS.values():
                if self.owner((x + dx, z + dz)) == other:
                    out.add((x, z))
        return out


@functools.lru_cache(maxsize=None)
def tiles(header):
    return Tiles(header)


@functools.lru_cache(maxsize=None)
def events(header):
    """The header's event file, or empty lists where it has none."""
    from . import splits
    stem = splits.headers()[header].get("eventsArchiveID")
    path = os.path.join(EVENTS, f"{stem}.json") if stem else None
    if not path or not os.path.exists(path):
        return {"object_events": [], "warp_events": [], "coord_events": [], "bg_events": []}
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def warps_to(header, dest):
    """The tiles of a header's warps that lead to another header."""
    return {(w["x"], w["z"]) for w in events(header)["warp_events"]
            if w["dest_header_id"] == "MAP_HEADER_" + dest}

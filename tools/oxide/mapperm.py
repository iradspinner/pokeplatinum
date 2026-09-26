#!/usr/bin/env python3
"""Show or set tile behaviours in a map's land data, and record every change.

Platinum Oxide project. Added 2026-09-27 for the tall grass that replaces the
gift clowns (Ian's option A): a patch that already looks distinct, a lawn or
a flower bed, is given the tall-grass behaviour, which alone makes wild
encounters and the grass rustle happen there. The look of the ground is the
terrain model's and is not touched.

A tile's behaviour is the low byte of its u16 in the 32 x 32 permission grid
at the head of res/field/maps/data/map_data_NNN.bin; bit 15 is collision.
`set` changes only the low byte, and only on tiles without collision, so a
wall or a tree inside the rectangle stays as it is.

Every change is recorded in tools/oxide/land_data_diverged.json, per map
data file and chunk-local tile, with the behaviour it had and the reason.
`verify_narcs.py --land-data` reads that registry: the built ROM's land data
must match the base ROM's except at exactly those tiles, which must hold
exactly the recorded behaviour. So a change made any other way fails the gate.

Coordinates are the ones event files use: global on the overworld matrix,
local to the map elsewhere. `tools/oxide/maprender.py` draws the same
coordinates, with --mark to preview a rectangle.

    python3 tools/oxide/mapperm.py show MAP_HEADER_SANDGEM_TOWN 170 844 183 851
    python3 tools/oxide/mapperm.py set MAP_HEADER_SANDGEM_TOWN 174 847 180 849 \\
        TILE_BEHAVIOR_TALL_GRASS --why "Sandgem's grass (Ian, 2026-09-27)"
"""

import argparse
import json
import os
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import maprender as mr  # noqa: E402

ROOT = mr.ROOT
REGISTRY = os.path.join(ROOT, "tools", "oxide", "land_data_diverged.json")


def behaviours():
    """TILE_BEHAVIOR_* name <-> value, from the enum the game is built with."""
    src = open(os.path.join(ROOT, "include", "constants", "field", "map_tile_behaviors.h")).read()
    body = src[src.index("{") + 1:src.index("}")]
    value, by_name = -1, {}
    for line in body.splitlines():
        line = line.split("//")[0].strip().rstrip(",")
        if not line:
            continue
        if "=" in line:
            name, v = (s.strip() for s in line.split("="))
            value = int(v, 0)
        else:
            name, value = line, value + 1
        by_name[name] = value
    return by_name, {v: k for k, v in by_name.items()}


def tiles_of(header, x0, z0, x1, z1):
    """[(x, z, map_data number, chunk-local x, chunk-local z)] for a rectangle."""
    fields = mr.header_fields(header)
    chunks, global_coords = mr.chunks_of(header, fields)
    r0 = min(r for r, _, _ in chunks)
    c0 = min(c for _, c, _ in chunks)
    where = {(r, c): n for r, c, n in chunks}
    gx0, gz0 = (c0 * mr.CHUNK, r0 * mr.CHUNK) if global_coords else (0, 0)
    out = []
    for z in range(z0, z1 + 1):
        for x in range(x0, x1 + 1):
            lx, lz = x - gx0, z - gz0
            key = (r0 + lz // mr.CHUNK, c0 + lx // mr.CHUNK)
            if lx < 0 or lz < 0 or key not in where:
                sys.exit(f"{header}: tile {x},{z} is outside the map")
            out.append((x, z, where[key], lx % mr.CHUNK, lz % mr.CHUNK))
    return out


def path_of(n):
    return os.path.join(ROOT, "res", "field", "maps", "data", f"map_data_{n:03d}.bin")


def read_tile(data, lx, lz):
    return struct.unpack_from("<H", data, 16 + (lz * mr.CHUNK + lx) * 2)[0]


def load_registry():
    if os.path.exists(REGISTRY):
        with open(REGISTRY, encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_registry(reg):
    with open(REGISTRY, "w", encoding="utf-8", newline="\n") as f:
        json.dump({k: reg[k] for k in sorted(reg)}, f, indent=4)
        f.write("\n")


def show(a):
    _, names = behaviours()
    rows = {}
    for x, z, n, lx, lz in tiles_of(a.header, a.x0, a.z0, a.x1, a.z1):
        v = read_tile(open(path_of(n), "rb").read(), lx, lz)
        ch = "#" if v >> 15 else ("g" if v & 0xFF in (2, 3) else ("." if v & 0xFF == 0 else "b"))
        rows.setdefault(z, []).append(ch)
    print("     " + "".join(str(x % 10) for x in range(a.x0, a.x1 + 1)))
    for z in sorted(rows):
        print(f"{z:4d} {''.join(rows[z])}")
    print("# wall, . no behaviour, g tall grass, b another behaviour")


def set_(a):
    by_name, names = behaviours()
    if a.behaviour not in by_name:
        sys.exit(f"{a.behaviour}: not a tile behaviour")
    new = by_name[a.behaviour]
    reg = load_registry()
    files, changed, walls = {}, 0, 0
    for x, z, n, lx, lz in tiles_of(a.header, a.x0, a.z0, a.x1, a.z1):
        if n not in files:
            files[n] = bytearray(open(path_of(n), "rb").read())
        data = files[n]
        v = read_tile(data, lx, lz)
        if v >> 15:
            walls += 1
            continue
        key = f"map_data_{n:03d}"
        entry = reg.setdefault(key, {"why": [], "tiles": {}})
        tile = f"{lx},{lz}"
        was = entry["tiles"].get(tile, {}).get("from", names.get(v & 0xFF, v & 0xFF))
        entry["tiles"][tile] = {"from": was, "to": a.behaviour, "event_xz": [x, z]}
        if a.why not in entry["why"]:
            entry["why"].append(a.why)
        if v & 0xFF != new:
            struct.pack_into("<H", data, 16 + (lz * mr.CHUNK + lx) * 2, (v & 0xFF00) | new)
            changed += 1
    print(f"{a.header}: {changed} tiles set to {a.behaviour}, {walls} wall tiles left alone"
          + (" (dry run)" if a.dry_run else ""))
    if not a.dry_run:
        for n, data in files.items():
            with open(path_of(n), "wb") as f:
                f.write(data)
        save_registry(reg)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("show", "set"):
        p = sub.add_parser(name)
        p.add_argument("header")
        for c in ("x0", "z0", "x1", "z1"):
            p.add_argument(c, type=int)
        if name == "set":
            p.add_argument("behaviour", help="a TILE_BEHAVIOR_* name")
            p.add_argument("--why", required=True, help="the reason, recorded in the registry")
            p.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    (show if a.cmd == "show" else set_)(a)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""The land data check's own test, so a stray map edit provably fails the gate.

    python3 tools/oxide/test_land_data.py [--base ~/roms/base.nds]

Builds a copy of the base ROM in memory with one map chunk edited and runs
verify_narcs.check_land_data against the base ROM with a registry given
directly. Writes nothing.
"""
import argparse
import os
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ndspy.narc  # noqa: E402
import ndspy.rom  # noqa: E402

import verify_narcs as vn  # noqa: E402

PATH = "fielddata/land_data/land_data.narc"
MEMBER, LX, LZ = 5, 12, 20  # a Route 201 chunk and a tile inside it


def edited(rom, nb, change):
    """A copy of rom whose land data member MEMBER has `change` applied."""
    copy = ndspy.rom.NintendoDSRom(rom.save())
    narc = ndspy.narc.NARC(copy.files[nb[PATH]])
    data = bytearray(narc.files[MEMBER])
    change(data)
    narc.files[MEMBER] = bytes(data)
    copy.files[nb[PATH]] = narc.save()
    return copy


def set_behaviour(value):
    def change(data):
        o = 16 + (LZ * 32 + LX) * 2
        v = struct.unpack_from("<H", data, o)[0]
        struct.pack_into("<H", data, o, (v & 0xFF00) | value)
    return change


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default=os.path.expanduser("~/roms/base.nds"))
    a = ap.parse_args()
    ref = ndspy.rom.NintendoDSRom.fromFile(a.base)
    nb = vn.walk(ref.filenames)
    member = f"map_data_{MEMBER:03d}"
    grass = {member: {"why": ["test"], "tiles": {f"{LX},{LZ}": {"from": "TILE_BEHAVIOR_NONE",
                                                                 "to": "TILE_BEHAVIOR_TALL_GRASS"}}}}
    with_grass = edited(ref, nb, set_behaviour(2))
    stray = edited(with_grass, nb, lambda d: d.__setitem__(len(d) - 1, d[-1] ^ 1))
    cases = [
        ("an unchanged ROM with nothing registered passes", ref, {}, True),
        ("a registered tile set as registered passes", with_grass, grass, True),
        ("the same edit with nothing registered fails", with_grass, {}, False),
        ("a registered tile never applied fails", ref, grass, False),
        ("a byte changed outside the registered tile fails", stray, grass, False),
    ]
    failed = 0
    for name, built, reg, want in cases:
        got = vn.check_land_data(built, ref, nb, nb, reg)
        ok = got == want
        failed += not ok
        print(("ok     " if ok else "FAILED ") + name)
    print(f"{len(cases) - failed} passed, {failed} failed")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()

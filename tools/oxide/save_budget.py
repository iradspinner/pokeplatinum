#!/usr/bin/env python3
"""Measure the save's layout and memory budget from a build.

The save's size is decided by functions, one per save table entry, so the
numbers that matter (how big each block is, whether the battle log still fits
beside the main save, whether the heaps still fit in main memory) are only
known once the game is built. This reads them from the build itself: the save
table from the ARM9 binary, each entry's size by decoding its size function,
then lays the blocks out the way src/savedata.c does and checks the budget.

    python3 tools/oxide/save_budget.py            # after make rom
    python3 tools/oxide/save_budget.py --json     # the same numbers as JSON

Exit status 1 if any check fails. docs/oxide/save-layout.md records what each
number was when it last moved.
"""
import argparse
import json
import os
import re
import struct
import subprocess
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", ".."))
BUILD = os.path.join(ROOT, "build")

ARM9_BASE = 0x02000000
# The ARM9's share of main memory ends here (NitroSDK's HW_MAIN_MEM_MAIN_END
# for a 4 MB system); the main arena runs from SDK_MAIN_ARENA_LO up to it.
MAIN_ARENA_HI = 0x023E0000
SECTOR = 0x1000
SECTORS_PER_HALF = 64                 # BACKUP_SECTOR_START - PRIMARY_SECTOR_START
BLOCK_FOOTER = 20                     # sizeof(SaveBlockFooter)
BATTLE_LOG_BYTES = 0xDB8              # sizeof(BattleLog), fixed by battle_log.c
# Vanilla's HEAP_SIZE_SAVE left this much beside the image for SaveData's other
# fields and the heap's own overhead; a larger image must keep it.
VANILLA_SAVE_HEAP_SPARE = 0x20E00 - 32 * SECTOR
# The boot code's other claims on the arena (src/heap.c, src/system.c): the
# random offset (at most 256), the heap handle tables (well under 1 KB), and
# the four task managers (52 bytes each plus 32 per task: 160, 32, 32 and 4).
ARENA_OTHER = 256 + 1024 + 4 * 52 + 32 * (160 + 32 + 32 + 4)


def define(path, name):
    text = open(os.path.join(ROOT, path)).read()
    m = re.search(r"#define\s+%s\s+(\S+)" % name, text) or re.search(r"\b%s\s*=\s*(\S+?),?\s*$" % name, text, re.M)
    if not m:
        raise SystemExit("%s not found in %s" % (name, path))
    return int(m.group(1).rstrip(","), 0)


def symbols(nef):
    out = subprocess.run(["arm-none-eabi-objdump", "-t", nef], capture_output=True, text=True, check=True).stdout
    table = {}
    for line in out.splitlines():
        parts = line.split()
        if len(parts) >= 6 and re.fullmatch(r"[0-9a-f]{8}", parts[0]):
            table[parts[-1]] = int(parts[0], 16)
    return table


class Code:
    def __init__(self, sbin):
        self.data = open(sbin, "rb").read()

    def u16(self, addr):
        return struct.unpack_from("<H", self.data, addr - ARM9_BASE)[0]

    def u32(self, addr):
        return struct.unpack_from("<I", self.data, addr - ARM9_BASE)[0]

    def constant(self, addr, depth=0):
        """The value a size function returns. The compiler writes them as a
        literal load, a small move, a move and a shift, or a call to another
        size function; anything else is reported rather than guessed."""
        addr &= ~1
        ops = [self.u16(addr + 2 * i) for i in range(6)]
        a, b, c = ops[0], ops[1], ops[2]
        if a & 0xF800 == 0x4800 and (a >> 8) & 7 == 0 and b == 0x4770:      # ldr r0,[pc,#n]; bx lr
            return self.u32(((addr + 4) & ~3) + (a & 0xFF) * 4)
        if a & 0xFF00 == 0x2000 and b == 0x4770:                            # movs r0,#n; bx lr
            return a & 0xFF
        if a & 0xFF00 == 0x2000 and b & 0xF83F == 0x0000 and c == 0x4770:  # movs r0,#n; lsls r0,r0,#k; bx lr
            return (a & 0xFF) << ((b >> 6) & 31)
        if depth < 3:
            for i in range(4):                                              # push; bl target; pop, or b target
                hi, lo = ops[i], ops[i + 1]
                if hi & 0xF800 == 0xF000 and lo & 0xF800 == 0xF800:
                    off = ((hi & 0x7FF) << 12) | ((lo & 0x7FF) << 1)
                    if off & 0x400000:
                        off -= 0x800000
                    return self.constant(addr + 2 * i + 4 + off, depth + 1)
                if hi & 0xF800 == 0xE000:
                    off = (hi & 0x7FF) << 1
                    if off & 0x800:
                        off -= 0x1000
                    return self.constant(addr + 2 * i + 4 + off, depth + 1)
        raise ValueError("size function at %08x not decoded: %s" % (addr, " ".join("%04x" % o for o in ops)))


def body_size(size):
    # SaveTableEntry_BodySize: padded to the next multiple of 4 (a whole 4
    # more when already aligned), then 4 more.
    return size + (4 - size % 4) + 4


def measure(build):
    syms = symbols(os.path.join(build, "main.nef"))
    code = Code(os.path.join(build, "main.sbin"))
    page_max = define("include/constants/savedata/save_table.h", "SAVE_PAGE_MAX")
    log_sector = define("include/battle_log.h", "BATTLE_LOG_SECTOR")

    entries = []
    table, count = syms["gSaveTable"], code.u32(syms["gSaveTableSize"])
    for i in range(count):
        data_id, block_id, size_func, _ = struct.unpack_from("<iIII", code.data, table + 16 * i - ARM9_BASE)
        entries.append({"id": data_id, "block": block_id, "size": code.constant(size_func)})

    blocks = []
    for block_id in sorted({e["block"] for e in entries}):
        size = sum(body_size(e["size"]) for e in entries if e["block"] == block_id) + BLOCK_FOOTER
        blocks.append({"block": block_id, "size": size, "sectors": -(-size // SECTOR)})
    main_end = sum(b["size"] for b in blocks)

    extras = []
    table, count = syms["gExtraSaveTable"], code.u32(syms["gExtraSaveTableSize"])
    for i in range(count):
        data_id, sector, size_func, _ = struct.unpack_from("<iIII", code.data, table + 16 * i - ARM9_BASE)
        size = code.constant(size_func) + 16               # SaveCheckFooter
        extras.append({"id": data_id, "sector": sector, "size": size, "sectors": -(-size // SECTOR)})

    heap = {n: define("include/constants/heap.h", "HEAP_SIZE_" + n) for n in ("SYSTEM", "SAVE", "DEBUG", "APPLICATION")}
    arena_lo = None
    xmap = os.path.join(build, "main.nef.xMAP")
    if os.path.exists(xmap):
        m = re.search(r"#>([0-9A-F]{8})\s+SDK_MAIN_ARENA_LO", open(xmap, errors="replace").read())
        arena_lo = int(m.group(1), 16) if m else None
    header = open(os.path.join(build, "pokeplatinum.us.nds"), "rb").read(0x50)
    fnt_size, fat_size = struct.unpack_from("<I", header, 0x44)[0], struct.unpack_from("<I", header, 0x4C)[0]
    arena_used = sum(heap.values()) + ARENA_OTHER + fnt_size + fat_size

    return {
        "entries": entries, "blocks": blocks, "main_end": main_end, "page_max": page_max,
        "image": page_max * SECTOR, "log_sector": log_sector, "extras": extras, "heap": heap,
        "arena_lo": arena_lo, "arena_used": arena_used,
        "arena_slack": (MAIN_ARENA_HI - arena_lo - arena_used) if arena_lo else None,
    }


def checks(m):
    tail = m["image"] - ((m["main_end"] + 3) & ~3)
    last_extra = max(e["sector"] + e["sectors"] for e in m["extras"])
    out = [
        ("the blocks fit the image", m["main_end"] <= m["image"], "%d of %d bytes" % (m["main_end"], m["image"])),
        ("the blocks fit SAVE_PAGE_MAX in whole sectors (SaveBlockInfo_Init's assert)",
         sum(b["sectors"] for b in m["blocks"]) <= m["page_max"],
         "%d of %d" % (sum(b["sectors"] for b in m["blocks"]), m["page_max"])),
        ("the battle log's RAM copy fits the image's tail", tail >= BATTLE_LOG_BYTES,
         "%d bytes free for %d, %d to spare" % (tail, BATTLE_LOG_BYTES, tail - BATTLE_LOG_BYTES)),
        ("the main save ends before the battle log's sector", m["main_end"] <= m["log_sector"] * SECTOR,
         "%d of %d bytes, %d to spare" % (m["main_end"], m["log_sector"] * SECTOR, m["log_sector"] * SECTOR - m["main_end"])),
        ("the extra entries start after the battle log's sector",
         min(e["sector"] for e in m["extras"]) > m["log_sector"], "first at %d" % min(e["sector"] for e in m["extras"])),
        ("each extra entry ends before the next begins", all(
            a["sector"] + a["sectors"] <= b["sector"] for a, b in zip(sorted(m["extras"], key=lambda e: e["sector"]),
                                                                    sorted(m["extras"], key=lambda e: e["sector"])[1:])), ""),
        ("the extra entries end inside the half", last_extra <= SECTORS_PER_HALF, "last ends at sector %d" % last_extra),
        ("HEAP_SIZE_SAVE keeps vanilla's spare beside the image",
         m["heap"]["SAVE"] - m["image"] >= VANILLA_SAVE_HEAP_SPARE,
         "0x%X for an image of 0x%X" % (m["heap"]["SAVE"], m["image"])),
    ]
    if m["arena_slack"] is not None:
        out.append(("the heaps fit in main memory", m["arena_slack"] > 0,
                    "about %d bytes of the arena left unclaimed" % m["arena_slack"]))
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--build", default=BUILD)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    m = measure(args.build)
    results = checks(m)
    if args.json:
        print(json.dumps({"measured": m, "checks": [{"check": c, "ok": ok, "detail": d} for c, ok, d in results]}, indent=2))
    else:
        for b in m["blocks"]:
            print("block %d: %d bytes (0x%X), %d sectors" % (b["block"], b["size"], b["size"], b["sectors"]))
        print("main save: %d bytes, image %d pages (%d bytes)" % (m["main_end"], m["page_max"], m["image"]))
        for e in m["extras"]:
            print("extra entry %d: sector %d, %d bytes, %d sectors" % (e["id"], e["sector"], e["size"], e["sectors"]))
        for c, ok, d in results:
            print("%s  %s%s" % ("ok  " if ok else "FAIL", c, ("  (%s)" % d) if d else ""))
    return 0 if all(ok for _, ok, _ in results) else 1


if __name__ == "__main__":
    sys.exit(main())

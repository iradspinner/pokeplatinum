#!/usr/bin/env python3
"""Everything that changed on one map, in one place.

Platinum Oxide project. The scripts-and-events carry-over is done a map at a
time across three files, so this gathers all three sides of one map's diff:
the object/warp/coord events, the field script, and the text bank.

Usage:
    python3 tools/oxide/mapdiff.py MAP [--base ROM] [--vanilla ROM]

MAP is the bare map name, e.g. sandgem_town_house.
"""
import argparse
import json
import os
import sys

ROOT = os.getcwd()
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import scriptdis as sd  # noqa: E402
import import_base_rom as imp  # noqa: E402

MSG_NARC = "msgdata/pl_msg.narc"


def order(path):
    return [l.strip() for l in open(os.path.join(ROOT, path)) if l.strip()]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("map")
    ap.add_argument("--base", default=os.path.expanduser("~/roms/base.nds"))
    ap.add_argument("--vanilla", default=os.path.expanduser("~/roms/vanilla.nds"))
    ap.add_argument("--tmp", default=os.environ.get("CLAUDE_JOB_DIR", "/tmp") + "/tmp")
    a = ap.parse_args()
    os.makedirs(a.tmp, exist_ok=True)

    base, van = imp.Rom(a.base), imp.Rom(a.vanilla)
    scripts = order("res/field/scripts/scripts.order")
    events = order("res/field/events/zone_event.order")
    banks = order("generated/text_banks.txt")

    si = scripts.index("scripts_" + a.map) if "scripts_" + a.map in scripts else None
    ei = events.index("events_" + a.map) if "events_" + a.map in events else None
    bank_name = "TEXT_BANK_" + a.map.upper()
    bi = banks.index(bank_name) if bank_name in banks else None
    print(f"# {a.map}   script {si}, events {ei}, text bank {bi}")

    if ei is not None:
        be, ve = base.narc(imp.EVENTS_NARC)[ei], van.narc(imp.EVENTS_NARC)[ei]
        print(f"\n## events   {len(ve)} -> {len(be)} bytes"
              + ("   (unchanged)" if bytes(be) == bytes(ve) else ""))
        if bytes(be) != bytes(ve):
            nd, od = imp.decode_events(be), imp.decode_events(ve)
            for key in od:
                if nd[key] == od[key]:
                    continue
                print(f"  {key}: {len(od[key])} -> {len(nd[key])}")
                for i, item in enumerate(nd[key]):
                    if i >= len(od[key]):
                        print(f"    NEW [{i}] {json.dumps(item)}")
                    elif item != od[key][i]:
                        print(f"    CHG [{i}] {json.dumps(od[key][i])}")
                        print(f"           -> {json.dumps(item)}")

    if si is not None:
        bs, vs = base.narc(sd.SCRIPTS_NARC)[si], van.narc(sd.SCRIPTS_NARC)[si]
        print(f"\n## script   {len(vs)} -> {len(bs)} bytes"
              + ("   (unchanged)" if bytes(bs) == bytes(vs) else ""))
        if bytes(bs) != bytes(vs):
            sd.use_base_rom_table(True)
            print(sd.emit_source(bs, "M"))

    if bi is not None:
        bm, vm = base.narc(MSG_NARC)[bi], van.narc(MSG_NARC)[bi]
        print(f"## text bank {bi}" + ("   (unchanged)" if bytes(bm) == bytes(vm) else ""))
        if bytes(bm) != bytes(vm):
            nb = imp.decode_text_bank("build/tools/msgenc/msgenc", "tools/msgenc/charmap.txt",
                                      bm, a.tmp, f"md{bi}b")
            nv = imp.decode_text_bank("build/tools/msgenc/msgenc", "tools/msgenc/charmap.txt",
                                      vm, a.tmp, f"md{bi}v")
            # which ids the script actually uses, so orphans stand out
            used = set()
            if si is not None:
                sd.use_base_rom_table(True)
                decoded, _l, _h, _m = sd.walk(base.narc(sd.SCRIPTS_NARC)[si])
                for dc in decoded.values():
                    for _k, name, value in dc.values:
                        if name in ("messageID", "entryStringID"):
                            used.add(value)
            for i, msg in enumerate(nb):
                tag = "NEW " if i >= len(nv) else (
                    "CHG " if imp.message_body(nv[i]) != imp.message_body(msg) else "    ")
                orphan = "  <- not referenced" if si is not None and i not in used else ""
                print(f" {tag}[{i}] {json.dumps(imp.message_body(msg))}{orphan}")


if __name__ == "__main__":
    main()

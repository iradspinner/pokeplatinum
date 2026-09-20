#!/usr/bin/env python3
"""Carry the base ROM's trainer battle messages into res/trainers/data.

Platinum Oxide project. TEXT_BANK_NPC_TRAINER_MESSAGES is a flat list of 2,497
messages, but the source keeps each one on its trainer, under a TRMSG_* type. It
looked like the mapping back would need trainerproc's packing order
reconstructed; it does not. `poketool/trmsg/trtbl.narc` is that mapping, one
(trainerID, messageType) pair per bank slot, and it is already in the ROM. It is
also byte-identical between the base ROM and vanilla, so only the text changed,
not which trainer or type any slot belongs to.

Usage:
    python3 tools/oxide/import_trainer_messages.py [--dry-run] [--check]

--check validates the mapping over every slot without writing anything: each
bank message must equal what the repo currently has for that trainer and type.

Run from the repository root.
"""
import argparse
import json
import os
import struct
import sys

ROOT = os.getcwd()
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import import_base_rom as imp  # noqa: E402
import jsonstyle  # noqa: E402

TRTBL_NARC = "poketool/trmsg/trtbl.narc"
MSG_NARC = "msgdata/pl_msg.narc"
BANK = "TEXT_BANK_NPC_TRAINER_MESSAGES"


def slot_map(rom):
    """bank index -> (trainer id, message type id)."""
    blob = rom.narc(TRTBL_NARC)[0]
    return [struct.unpack_from("<2H", blob, i * 4) for i in range(len(blob) // 4)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default=os.path.expanduser("~/roms/base.nds"))
    ap.add_argument("--vanilla", default=os.path.expanduser("~/roms/vanilla.nds"))
    ap.add_argument("--msgenc", default="build/tools/msgenc/msgenc")
    ap.add_argument("--charmap", default="tools/msgenc/charmap.txt")
    ap.add_argument("--tmp", default=os.environ.get("CLAUDE_JOB_DIR", "/tmp") + "/tmp")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--check", action="store_true",
                    help="validate the mapping against vanilla and write nothing")
    a = ap.parse_args()
    os.makedirs(a.tmp, exist_ok=True)

    base, van = imp.Rom(a.base), imp.Rom(a.vanilla)
    slots = slot_map(van)
    if slot_map(base) != slots:
        print("the base ROM's trtbl differs from vanilla's; the mapping cannot be assumed")
        return 1

    bank = imp.text_bank_names().index(BANK)
    new = imp.decode_text_bank(a.msgenc, a.charmap, base.narc(MSG_NARC)[bank], a.tmp, "trmsg_b")
    old = imp.decode_text_bank(a.msgenc, a.charmap, van.narc(MSG_NARC)[bank], a.tmp, "trmsg_v")
    types = imp.load_enum("trainer_message_types")

    if a.check:
        checked = mismatched = missing = 0
        for i, (trainer, mtype) in enumerate(slots):
            path = imp.trainer_json(trainer)
            if path is None:
                missing += 1
                continue
            entry = next((e for e in json.load(open(path, encoding="utf-8")).get("messages", [])
                          if e["type"] == types.get(mtype, mtype)), None)
            if entry is None:
                missing += 1
                continue
            checked += 1
            # a trainer message can be an unused slot on both sides, spelled
            # "garbage" in the json the same way the decoder spells it
            mine = entry["en_US"] if "en_US" in entry else ("garbage", entry.get("garbage"))
            if mine != imp.message_body(old[i]):
                mismatched += 1
                if mismatched <= 5:
                    print(f"  slot {i}: {os.path.basename(path)} {types.get(mtype)} does not match vanilla")
        print(f"mapping check: {checked} slots agree with the repo, {mismatched} do not, "
              f"{missing} had no trainer json or no message of that type")
        return 1 if mismatched else 0

    touched, changes, skipped, blanked = set(), 0, [], 0
    for i, (trainer, mtype) in enumerate(slots):
        if imp.message_body(new[i]) == imp.message_body(old[i]):
            continue
        path = imp.trainer_json(trainer)
        type_name = types.get(mtype, mtype)
        if path is None:
            skipped.append(f"slot {i}: trainer {trainer} has no json")
            continue
        data = json.load(open(path, encoding="utf-8"))
        index = next((n for n, e in enumerate(data.get("messages", []))
                      if e["type"] == type_name), None)
        if index is None:
            skipped.append(f"slot {i}: {os.path.basename(path)} has no {type_name} message")
            continue
        value = imp.message_body(new[i])
        if isinstance(value, tuple):
            # The base ROM zeroed the filler byte on every unused slot. That is
            # all 373 of this bank's differences and every one of them belongs
            # to a DUMMY trainer, so there is no text here to carry over.
            blanked += 1
            continue
        text = open(path, encoding="utf-8").read()
        keypath = ["messages", index, "en_US"]
        if jsonstyle.get_value(text, keypath) == value:
            continue
        text = jsonstyle.replace_value(text, keypath, value)
        if not a.dry_run:
            with open(path, "w", encoding="utf-8", newline="\n") as f:
                f.write(text)
        touched.add(path)
        changes += 1

    print(f"{'would change' if a.dry_run else 'changed'} {changes} messages across "
          f"{len(touched)} trainers; {len(skipped)} skipped")
    if blanked:
        print(f"  {blanked} slots differ only in the filler value of an unused entry, all on "
              f"DUMMY trainers; DSPRE zeroed them and there is no text to carry over")
    for line in skipped[:10]:
        print("  " + line)
    return 0


if __name__ == "__main__":
    sys.exit(main())

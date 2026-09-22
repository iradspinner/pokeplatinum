#!/usr/bin/env python3
"""Rewrite every remaining changed text bank from the base ROM, in bulk.

Platinum Oxide project. import_base_rom.py's text pass only takes banks whose
message count is unchanged, because a new message needs a new symbolic id. This
takes the rest, keeping each existing message's id so nothing already referenced
by a script moves, and giving new ones a generated id.

Generated ids are `<Bank>_Text_<n>`, which says plainly that nobody has read the
line yet. The scripts these banks serve are now generated too and refer to
messages by number, so nothing depends on the names; they exist so the file
looks like the others and so a human can rename them later.

Usage:
    python3 tools/oxide/bulk_text.py [--dry-run]

Run from the repository root. Needs a built msgenc.
"""
import argparse
import json
import os
import sys

ROOT = os.getcwd()
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import import_base_rom as imp  # noqa: E402

MSG_NARC = "msgdata/pl_msg.narc"


def bank_prefix(bank_name):
    stem = bank_name[len("TEXT_BANK_"):].lower()
    return "".join(part.capitalize() for part in stem.split("_"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default=os.path.expanduser("~/roms/base.nds"))
    ap.add_argument("--vanilla", default=os.path.expanduser("~/roms/vanilla.nds"))
    ap.add_argument("--built", default="build/pokeplatinum.us.nds")
    ap.add_argument("--msgenc", default="build/tools/msgenc/msgenc")
    ap.add_argument("--charmap", default="tools/msgenc/charmap.txt")
    ap.add_argument("--tmp", default=os.environ.get("CLAUDE_JOB_DIR", "/tmp") + "/tmp")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    os.makedirs(a.tmp, exist_ok=True)

    base, van = imp.Rom(a.base), imp.Rom(a.vanilla)
    bm, vm = base.narc(MSG_NARC), van.narc(MSG_NARC)
    already = set()
    built_banks = None
    if os.path.isfile(a.built):
        built_banks = imp.Rom(a.built).narc(MSG_NARC)
        already = {i for i in range(min(len(built_banks), len(bm)))
                   if bytes(built_banks[i]) == bytes(bm[i])}
    names = imp.text_bank_names()

    written, skipped = 0, []
    for i in range(len(bm)):
        if bytes(bm[i]) == bytes(vm[i]) or i in already:
            continue
        if i in imp.TEXT_BANKS_SKIPPED:
            skipped.append(f"{names[i]}: {imp.TEXT_BANKS_SKIPPED[i]}")
            continue
        stem = names[i][len("TEXT_BANK_"):].lower()
        path = os.path.join(ROOT, "res", "text", stem + ".json")
        if not os.path.isfile(path):
            skipped.append(f"{names[i]}: generated from other res/ data, not a res/text file")
            continue
        current = json.load(open(path, encoding="utf-8"))
        decoded = imp.decode_text_bank(a.msgenc, a.charmap, bm[i], a.tmp, f"bt{i}")
        if built_banks is not None and i < len(built_banks):
            # A bank whose text already matches is done, whatever its bytes say.
            # DSPRE re-encrypted a couple of banks with its own key, and the key
            # is stored in the bank, so any value decodes the same. Rewriting
            # them would change nothing and would make the restart check-list
            # look like something had moved.
            mine = imp.decode_text_bank(a.msgenc, a.charmap, built_banks[i], a.tmp, f"bc{i}")
            if [imp.message_body(x) for x in mine] == [imp.message_body(x) for x in decoded]:
                continue
        prefix = bank_prefix(names[i])
        out = {"key": current["key"], "messages": []}
        for n, msg in enumerate(decoded):
            if n < len(current["messages"]) and "id" in current["messages"][n]:
                entry = {"id": current["messages"][n]["id"]}
            else:
                entry = {"id": f"{prefix}_Text_{n}"}
            if "en_US" in msg:
                entry["en_US"] = msg["en_US"]
            else:
                entry["garbage"] = msg.get("garbage", 0)
            out["messages"].append(entry)
        if not a.dry_run:
            with open(path, "w", encoding="utf-8", newline="\n") as f:
                json.dump(out, f, indent=2, ensure_ascii=False)
                f.write("\n")
        written += 1

    print(f"{'would write' if a.dry_run else 'wrote'} {written} text banks; {len(skipped)} skipped")
    for line in skipped[:10]:
        print("  " + line)


if __name__ == "__main__":
    import os as _os, sys as _sys
    _sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
    import pinned_python
    pinned_python.ensure()
    main()

#!/usr/bin/env python3
"""Merge a test kit fragment into a map's events file or text bank, at build time.

Platinum Oxide's test kit (docs/oxide/test-kit.md) adds an NPC to the player's
bedroom. The events JSON and the text bank have no preprocessor, so instead of
keeping a hand-made copy of each that could drift from the real file, the kit
build runs this: it reads the real file, appends every list in the fragment to
the list of the same name (object_events, messages), and writes the result
under the same file name in the build folder. Builds without the kit never run
it, so the real files and the ROM of record are untouched.

Usage: testkit_merge.py <real.json> <fragment.json> <out.json> [<kit script>]

Given the kit's script, it also refuses a list menu of more entries than a
field menu holds (FIELD_MENU_ENTRIES_MAX), which would write past the menu's
arrays and corrupt memory when opened (move set page 3 did, 2026-10-07).
"""
import json
import os
import re
import sys


FIELD_MENU_H = "include/overlay005/field_menu.h"


def check_menus(script_path, header_path):
    """Every list menu in the kit's script, Init to Show, against the most a
    field menu holds."""
    with open(header_path, encoding="utf-8") as f:
        limit = int(re.search(r"#define FIELD_MENU_ENTRIES_MAX (\d+)", f.read()).group(1))
    errors, label, count = [], None, None
    with open(script_path, encoding="utf-8") as f:
        for line in f:
            s = line.strip()
            if re.match(r"^\w+:$", s):
                label = s[:-1]
            elif s.startswith(("InitLocalTextListMenu", "InitGlobalTextListMenu")):
                count = 0
            elif s.startswith("AddListMenuEntry") and count is not None:
                count += 1
            elif s.startswith("ShowListMenu") and count is not None:
                if count > limit:
                    errors.append(f"{label}: {count} entries, but a field menu holds {limit}")
                count = None
    if errors:
        sys.exit("testkit_merge: " + script_path + ": " + "; ".join(errors))


def main():
    if len(sys.argv) not in (4, 5):
        sys.exit(__doc__)
    real_path, fragment_path, out_path = sys.argv[1:4]
    if len(sys.argv) == 5:
        root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        check_menus(sys.argv[4], os.path.join(root, FIELD_MENU_H))
    with open(real_path, encoding="utf-8") as f:
        merged = json.load(f)
    with open(fragment_path, encoding="utf-8") as f:
        fragment = json.load(f)

    for key, extra in fragment.items():
        if key.startswith("//"):
            continue  # a comment key in the fragment, not data
        if not isinstance(extra, list) or not isinstance(merged.get(key, []), list):
            sys.exit("testkit_merge: %s: only lists can be appended, and %r is not one" % (fragment_path, key))
        merged.setdefault(key, []).extend(extra)

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(merged, f, indent=4, ensure_ascii=False)
        f.write("\n")


if __name__ == "__main__":
    main()

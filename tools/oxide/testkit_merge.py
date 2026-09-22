#!/usr/bin/env python3
"""Merge a test kit fragment into a map's events file or text bank, at build time.

Platinum Oxide's test kit (docs/oxide/test-kit.md) adds an NPC to the player's
bedroom. The events JSON and the text bank have no preprocessor, so instead of
keeping a hand-made copy of each that could drift from the real file, the kit
build runs this: it reads the real file, appends every list in the fragment to
the list of the same name (object_events, messages), and writes the result
under the same file name in the build folder. Builds without the kit never run
it, so the real files and the ROM of record are untouched.

Usage: testkit_merge.py <real.json> <fragment.json> <out.json>
"""
import json
import sys


def main():
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    real_path, fragment_path, out_path = sys.argv[1:]
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

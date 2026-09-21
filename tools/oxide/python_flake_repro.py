"""Minimal reproduction of an interpreter fault seen on this machine's
Python 3.14.4 (2026-09-21): pure-Python string work in jsonstyle.py returns
wrong results after a few hundred repetitions of the same call on the same
text, with no writes and no threads. The failures are random in position
and kind (KeyError on a key that is there, "unbalanced container" on a
balanced one, "'int' object is not callable" on the builtin len), survive
PYTHONHASHSEED pinning, PYTHON_JIT=0 and the pure-Python json scanner, and
appear under both pymalloc and PYTHONMALLOC=malloc. PYTHONMALLOC=debug hid
them in six attempts, which points at the interpreter's memory handling.

    python3 tools/oxide/python_flake_repro.py     # from the repo root

Expected: "done, failures: 0" every time. Seen: 0 on some runs, 2-6 on
others. It is what makes tools/oxide/encounters/test_step0 fail on random
files now and then; the other suites do far fewer string passes. Ian's call
whether to report it upstream or move the box to another Python.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from tools.oxide import jsonstyle  # noqa: E402


def main():
    root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    path = os.path.join(root, "res", "field", "encounters", "encounters_route_209.json")
    with open(path, encoding="utf-8") as f:
        text = f.read()
    paths = ([["land_encounters", i, k] for i in range(12) for k in ("species", "level")]
             + [["day", 0], ["night", 1], ["ruby", 0]])
    fails = 0
    for n in range(400):
        for p in paths:
            try:
                v = jsonstyle.get_value(text, p)
                if jsonstyle.replace_value(text, p, v) != text:
                    fails += 1
                    print("iteration", n, p, "rewrite changed the text")
            except Exception as e:
                fails += 1
                print("iteration", n, p, type(e).__name__, str(e)[:60])
            if fails > 5:
                break
        if fails > 5:
            break
    print("done, failures:", fails)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())

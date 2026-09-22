"""Stability check for this machine's CPU, which is degraded.

The i9-14900K in this box returns wrong answers and crashes processes under
load; the warranty replacement is pending (design doc findings log,
2026-09-22). This script does the same pure-Python string work 400 times on
one input and reports any result that differs, so on a sound machine it
prints "done, failures: 0" every time. Wrong answers show up as a KeyError on
a key that is there, "unbalanced container" on a balanced one, or a rewrite
that silently changes the text; crashes show up as a segfault or a fatal
Python error.

It was first read as an interpreter bug, because one Python failed more than
another on a small sample, and the project pinned its interpreter for a day.
The same fault then showed on every interpreter, on Windows-native Python and
in the C compilers, which is what put it in the hardware.

One copy at a time is clean with the CPU capped; the fault needs many cores
busy, so run several at once to test it:

    for i in $(seq 16); do python3 tools/oxide/python_flake_repro.py & done; wait
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

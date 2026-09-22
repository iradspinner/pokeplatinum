"""Regression check for the interpreter fault that made this project pin its
Python. Run it after changing the pinned interpreter, and nowhere else.

**The fault.** Ubuntu 26.04's Python 3.14.4-1ubuntu0.2 intermittently returns
wrong results from pure-Python string work: a KeyError on a key that is there,
"unbalanced container" on a balanced one, "'int' object is not callable" on the
builtin len, or, worst of all, a rewrite that silently changes the text. No
threads, no writes, the same input every iteration.

**It is not the hardware and it is not Python 3.14.** Measured 2026-09-22 on
this machine, same code and same input, only the interpreter binary changing:

    /usr/bin/python3.14  3.14.4-1ubuntu0.2   10 of 15 runs, 37 wrong / 30,000 iterations
    uv cpython 3.13.15                        0 of 15 runs,  0 wrong / 30,000
    uv cpython 3.14.7                         0 of 27 runs,  0 wrong / 54,000

If it were RAM or CPU, swapping the interpreter would not move that. Also
checked and cleared: 8GiB written with a pattern and verified twice, three
synthetic Python workloads (integer math, C-level hashing, string and container
churn) at 3,000 iterations each, and the C json extension, which makes no
difference when disabled. `gc.disable()` cuts the rate but does not remove it.

**Two things earlier notes got wrong.** The failures are not a warm-up effect:
first failures were seen at iterations 1, 2, 63 and 193. And PYTHONMALLOC=debug,
which hid it in this small repro, does not hide it at real workloads; it failed
twice in three runs of import_base_rom.py.

**Why 3.13 and not 3.14.7**, although both measured clean here: the astral 3.14
build is compiled --with-tail-call-interp, and that interpreter aborted a
`meson setup` outright with "Fatal Python error: _TAIL_CALL_CACHE: Executing a
cache." An interpreter that can kill the build configuration is worse than one
that occasionally returns a wrong string. 3.13 has no tail-call interpreter.

The pin lives in `tools/oxide/oxide-python`, which the Makefile and
`integrate.sh` both go through. It mattered beyond the tools because `make rom`
runs Python about 227 times to generate event data, map matrices and the
encounter archives.

    tools/oxide/oxide-python tools/oxide/python_flake_repro.py     # the pinned one
    python3 tools/oxide/python_flake_repro.py                      # the system one

Expected on a good interpreter: "done, failures: 0" every time. On Ubuntu's
3.14.4, about two runs in three report failures.
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

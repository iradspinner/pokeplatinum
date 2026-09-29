#!/usr/bin/env python3
"""Checks oxide_guard.py's three rules: sweeping `git add`, launching an
emulator, and committing the scratch marker.

Run from anywhere: python3 .claude/hooks/test_oxide_guard.py
Prints "N passed" or the first failure, and exits non-zero on a failure.
"""
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import oxide_guard  # noqa: E402


def main():
    passed = 0

    def expect(name, cond):
        nonlocal passed
        if not cond:
            print("FAIL", name)
            sys.exit(1)
        passed += 1

    # True means refused. Builds are allowed again since the new CPU
    # (2026-09-29), and text inside a heredoc is never read as a command.
    cases = {
        "git add -A": True, "git add .": True, "git add --all": True,
        "cd x && git add -A": True, "git add docs/oxide/tracker.md": False,
        "melonDS.exe": True, "nohup ./melonDS": True, "./AppRun": True,
        "cat melonDS.toml": False,
        "make rom": False, "ninja -C build": False,
        "git commit -F - <<'EOF'\nSubject\n\ngit add -A was not used\nEOF": False,
    }
    for cmd, refused in cases.items():
        got = oxide_guard.check(cmd, "/") is not None
        expect("%r %s" % (cmd, "refused" if refused else "allowed"), got == refused)

    # The marker rule reads what is staged, so it needs a real repository.
    with tempfile.TemporaryDirectory() as repo:
        run = lambda *a: subprocess.run(["git", "-C", repo] + list(a), capture_output=True)
        run("init", "-q")
        with open(os.path.join(repo, "clean.txt"), "w") as f:
            f.write("nothing to see\n")
        run("add", "clean.txt")
        expect("a clean staged file commits", oxide_guard.check("git commit -m x", repo) is None)
        with open(os.path.join(repo, "scratch.txt"), "w") as f:
            f.write("temporary, %s\n" % oxide_guard.MARKER)
        run("add", "scratch.txt")
        expect("a staged marker is refused", oxide_guard.check("git commit -m x", repo) is not None)

    print("%d passed" % passed)


if __name__ == "__main__":
    main()

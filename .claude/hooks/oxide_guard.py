#!/usr/bin/env python3
"""PreToolUse guard for Bash commands in the Platinum Oxide repo.

Refuses three things the project rules forbid, by exiting 2 with the reason on
stderr (Claude Code then blocks the command and shows the reason to the agent):

- `git add -A`, `git add --all` or `git add .`: sessions share this checkout,
  so a sweep commits another session's in-progress files. Stage by name.
- Launching melonDS (or an AppImage's AppRun): agents attach to Ian's own
  melonDS on Windows over its GDB stub, and never start one of their own.
- A `git commit` whose staged changes add a line carrying the scratch marker
  (MARKER below): that marker is how a file says it must never be committed.

Anything it cannot parse it lets through; this is a guard rail, not a sandbox.
"""
import json
import os
import re
import shlex
import subprocess
import sys

# Split in two so this file does not carry the marker it refuses.
MARKER = "do not " "commit"

# Leading words that run another program, which is then the real command.
WRAPPERS = {"nohup", "setsid", "exec", "env", "timeout", "xvfb-run", "sudo",
            "nice", "stdbuf", "wine", "wine64", "cmd.exe", "powershell.exe",
            "pwsh.exe", "start", "start-process", "/c", "-command"}


def segments(command):
    """Split a shell command line into simple commands, roughly."""
    return [s.strip() for s in re.split(r"&&|\|\||[;|\n&]", command) if s.strip()]


def words(segment):
    try:
        return shlex.split(segment)
    except ValueError:
        return segment.split()


def git_args(ws):
    """(args after the git subcommand, subcommand, -C path) or None."""
    if not ws or os.path.basename(ws[0]) != "git":
        return None
    i, cwd = 1, None
    while i < len(ws) and ws[i].startswith("-"):
        if ws[i] == "-C" and i + 1 < len(ws):
            cwd = ws[i + 1]
            i += 2
            continue
        i += 1
    if i >= len(ws):
        return None
    return ws[i + 1:], ws[i], cwd


def strip_env(ws):
    """Drop leading VAR=value assignments and wrapper programs."""
    out = list(ws)
    while out and (re.match(r"^[A-Za-z_][A-Za-z0-9_]*=", out[0])
                   or out[0].lower() in WRAPPERS
                   or re.match(r"^-?\d+[smh]?$", out[0])):
        out.pop(0)
    return out


def is_emulator(word):
    base = os.path.basename(word.replace("\\", "/")).lower()
    return base == "apprun" or base.startswith("melonds")


def added_lines(repo, commit_all):
    """Lines added by what `git commit` is about to record, with file names."""
    cmd = ["git", "-C", repo, "diff", "--unified=0", "--no-color"]
    cmd += ["HEAD"] if commit_all else ["--cached"]
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=30).stdout
    except (OSError, subprocess.SubprocessError):
        return []
    found, current = [], None
    for line in out.splitlines():
        if line.startswith("+++ "):
            current = line[6:] if line.startswith("+++ b/") else line[4:]
        elif line.startswith("+") and not line.startswith("+++"):
            found.append((current, line[1:]))
    return found


def check(command, cwd):
    for seg in segments(command):
        ws = strip_env(words(seg))
        if not ws:
            continue
        if is_emulator(ws[0]):
            return ("Refused: this launches an emulator. Agents never run their own "
                    "melonDS; attach to Ian's over its GDB stub while Ian drives the "
                    "game (docs/oxide/setup-fork-and-wsl2.md part 5b).")
        g = git_args(ws)
        if not g:
            continue
        args, sub, gcwd = g
        if sub == "add":
            for a in args:
                if a in (".", "--all", ":/", "./") or re.match(r"^-[a-zA-Z]*A[a-zA-Z]*$", a):
                    return ("Refused: `git add %s` sweeps in other sessions' files, "
                            "because sessions share this checkout. Stage files by "
                            "name." % a)
        if sub == "commit":
            repo = os.path.join(cwd, gcwd) if gcwd else cwd
            commit_all = any(a in ("-a", "--all") or re.match(r"^-[a-zA-Z]*a[a-zA-Z]*$", a)
                             for a in args if not a.startswith("--") or a == "--all")
            hits = sorted({f for f, l in added_lines(repo, commit_all)
                           if MARKER in l.lower()})
            if hits:
                return ("Refused: the changes being committed add a line containing "
                        "\"%s\" in: %s. Unstage those files or remove the "
                        "marker." % (MARKER, ", ".join(hits)))
    return None


def main():
    try:
        data = json.load(sys.stdin)
    except ValueError:
        return 0
    if data.get("tool_name") != "Bash":
        return 0
    command = (data.get("tool_input") or {}).get("command") or ""
    reason = check(command, data.get("cwd") or os.getcwd())
    if reason:
        print(reason, file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())

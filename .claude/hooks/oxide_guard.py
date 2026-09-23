#!/usr/bin/env python3
"""PreToolUse guard for Bash commands in the Platinum Oxide repo.

Refuses four things, by exiting 2 with the reason on stderr (Claude Code then
blocks the command and shows the reason to the agent):

- `git add -A`, `git add --all` or `git add .`: sessions share this checkout,
  so a sweep commits another session's in-progress files. Stage by name.
- Launching melonDS (or an AppImage's AppRun): agents attach to Ian's own
  melonDS on Windows over its GDB stub, and never start one of their own.
- A `git commit` whose staged changes add a line carrying the scratch marker
  (MARKER below): that marker is how a file says it must never be committed.
- `ps`, `pgrep`, `pkill`, `top`, `htop` or `pidof` while a process is wedged
  in the kernel on `__vma_start_write`. Until the replacement CPU is in, that
  wedge happens, and anything that reads the stuck process's details then
  blocks for good; a session lost two shells that way. Only these commands pay
  for the /proc scan. Delete this rule, and `wedge_status.sh` beside it, when
  the new chip is in.
- A full local build (`make`, `make rom`, `make testkit`, `ninja` without a
  small -j, `meson compile`, or `integrate.sh` without --rom, --no-build or
  --dry-run), from 2026-09-23 until the replacement CPU is in: builds load every
  core, and that is where this chip crashes and wedges. Build on GitHub instead
  (push, then tools/oxide/fetch-rom) and check the downloaded ROM, for instance
  with `integrate.sh --rom PATH`. `ninja -j1` or `-j2` for a few targets is
  allowed. Prefix the command with OXIDE_LOCAL_BUILD_OK=1 when Ian has said a
  local build is wanted anyway. Delete this rule when the new chip is in.

Anything it cannot parse it lets through; this is a guard rail, not a sandbox.
"""
import glob
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


# Commands that read every process's details, so one wedged process hangs them.
PROC_READERS = {"ps", "pgrep", "pkill", "top", "htop", "pidof"}
WEDGE = "__vma_start_write"


def wedged(proc_root="/proc"):
    """(pid, name) of every process stuck on the kernel's memory-map lock.

    Reads only wchan and comm, the two per-process files that do not need the
    lock the wedged process holds; cmdline, status and stat would block too.
    proc_root lets a test point this at a fake /proc tree.
    """
    found = []
    for d in glob.glob(os.path.join(proc_root, "[0-9]*")):
        try:
            with open(os.path.join(d, "wchan")) as f:
                if WEDGE not in f.read():
                    continue
            with open(os.path.join(d, "comm")) as f:
                name = f.read().strip()
        except OSError:
            continue
        found.append((os.path.basename(d), name))
    return sorted(found, key=lambda p: int(p[0]) if p[0].isdigit() else 0)


# make targets that run the full build; anything else (clean, format) is let by.
MAKE_BUILD_TARGETS = {"", "all", "rom", "testkit", "debug", "release", "check", "target"}


def full_build(raw_words, ws):
    """Why this command would run a full local build, or None."""
    if any(w.startswith("OXIDE_LOCAL_BUILD_OK=1") for w in raw_words):
        return None
    prog = os.path.basename(ws[0])
    args = ws[1:]
    if prog == "make":
        targets = [a for a in args if not a.startswith("-") and "=" not in a]
        if not targets or any(t in MAKE_BUILD_TARGETS for t in targets):
            return "`make %s`" % " ".join(targets or ["(default)"])
    if prog == "ninja":
        jobs = None
        for i, a in enumerate(args):
            if a == "-j" and i + 1 < len(args):
                jobs = args[i + 1]
            elif a.startswith("-j"):
                jobs = a[2:]
        if not (jobs and jobs.isdigit() and 0 < int(jobs) <= 2) and "-n" not in args and "-t" not in args:
            return "`ninja` on every core"
    if prog in ("meson", "meson.py") and args[:1] == ["compile"]:
        return "`meson compile`"
    if prog == "integrate.sh" or (prog == "bash" and args and os.path.basename(args[0]) == "integrate.sh"):
        if not any(a in ("--no-build", "--dry-run") or a.startswith("--rom") for a in args):
            return "`integrate.sh`, which runs `make rom`"
    return None


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


# A heredoc body (a commit message, a file being written) is data, not commands,
# so it is removed before the command line is split and checked.
HEREDOC_RE = re.compile(r"<<-?\s*(['\"]?)(\w+)\1[^\n]*\n.*?\n\s*\2[ \t]*(?=\n|$)", re.S)


def check(command, cwd, proc_root="/proc"):
    command = HEREDOC_RE.sub("<<heredoc", command)
    for seg in segments(command):
        raw = words(seg)
        ws = strip_env(raw)
        if not ws:
            continue
        why = full_build(raw, ws)
        if why:
            return ("Refused: %s is a full local build, and until the replacement CPU "
                    "is in, builds crash or wedge on this chip. Push and build on "
                    "GitHub instead: tools/oxide/fetch-rom <commit> downloads the ROM, "
                    "and `bash tools/oxide/integrate.sh --verify-only --rom <that ROM>` "
                    "checks it. `ninja -C build -j2 <targets>` is allowed for a few "
                    "targets. If Ian has asked for a local build anyway, prefix the "
                    "command with OXIDE_LOCAL_BUILD_OK=1." % why)
        if is_emulator(ws[0]):
            return ("Refused: this launches an emulator. Agents never run their own "
                    "melonDS; attach to Ian's over its GDB stub while Ian drives the "
                    "game (docs/oxide/setup-fork-and-wsl2.md part 5b).")
        if os.path.basename(ws[0]) in PROC_READERS:
            stuck = wedged(proc_root)
            if stuck:
                who = ", ".join("pid %s (%s)" % p for p in stuck)
                return ("Refused: %s is wedged in the kernel on %s, and `%s` would "
                        "block for good reading it. Only Ian can clear it, with "
                        "`wsl --shutdown`; tell him. To list processes safely, read "
                        "only comm: for d in /proc/[0-9]*; do echo \"${d#/proc/} "
                        "$(cat $d/comm)\"; done" % (who, WEDGE, os.path.basename(ws[0])))
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

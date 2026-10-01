#!/usr/bin/env python3
"""Check Platinum Oxide's deferred instructions: everything a doc says to do
on a later day or once something happens.

On 2026-10-01 the Overseer followed a tracker note dated that day ("switch
the private repos' workflows back on") without asking whether it was still
needed. The new CPU had made those workflows unnecessary two days before, but
the note gave a date and no reason, so nothing showed that it had gone
stale. Ian's rule since then: every deferred instruction lives in one place,
the tracker's **Scheduled** list, and says why it exists and what would make
it unneeded. Before a session carries one out, it checks that reason against
today's state, and asks Ian if the reason no longer holds.

This check enforces the part a script can see:

- every Scheduled entry has a "Why:" and an "Unneeded if:";
- an entry whose date has passed is an error: it was due and nobody resolved
  it (done, dropped or moved, each with its reason checked);
- an entry due today is a warning, so the session checks it before acting;
- a deferral to a day still to come ("until", "by", "after", "from" or "on"
  a future date) anywhere else in the docs, rules, skills, commands or a local
  session's memory is an error. A dated deferral outside the list is how the
  2026-10-01 note was written; it belongs in the list, and the other places
  point at it.

Conditional entries ("**Once MSYS2 is installed**") have no date, so only
their fields are checked; the reason check is the session's.

Usage:
    python3 tools/oxide/deferred_check.py              # list, check, exit 1 on an error
    python3 tools/oxide/deferred_check.py --today 2026-10-05
"""
import argparse
import datetime
import glob
import os
import re
import sys

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
TRACKER = "docs/oxide/tracker.md"
MEMORY = os.path.expanduser("~/.claude/projects/-home-ian-pokeplatinum/memory")

DATE = r"(\d{4}-\d{2}-\d{2})"
# A deferral to a day: "until 2026-10-01", "from 2026-10-01", "On 2026-10-01".
# It counts only while the day is still to come. On the day itself the same
# words are as often history written that day ("it was shallow until
# 2026-09-30", "on 2026-10-01 Ian ruled"), and a deferral written ahead of
# time has already been caught on every day before it.
DEFER = re.compile(r"\b(until|by|after|from|on)\s+" + DATE, re.I)
ENTRY_DATE = re.compile(r"^-\s+\*\*" + DATE)


def scanned_files(include_memory=True):
    """Every file a session reads for instructions, archives excepted (they
    are history by definition)."""
    pats = ["CLAUDE.md", ".claude/rules/*.md", ".claude/skills/*/SKILL.md",
            ".claude/commands/*.md", "docs/oxide/**/*.md"]
    out = []
    for p in pats:
        for f in sorted(glob.glob(os.path.join(REPO, p), recursive=True)):
            if "archive" not in os.path.basename(f):
                out.append(f)
    if include_memory and os.path.isdir(MEMORY):
        out += sorted(glob.glob(os.path.join(MEMORY, "*.md")))
    return out


def scheduled_block(lines):
    """The line range of the tracker's Scheduled list: from its bold label to
    the next paragraph that is not a bullet or a bullet's continuation."""
    start = next((i for i, l in enumerate(lines) if l.startswith("**Scheduled**")), None)
    if start is None:
        return None
    end = start + 1
    while end < len(lines):
        l = lines[end]
        if l.startswith(("**", "#")):
            break
        end += 1
    return start, end


def entries(lines, block):
    """The Scheduled list's bullets, each with its first line number and its
    whole text (continuation lines joined)."""
    out = []
    start, end = block
    for i in range(start + 1, end):
        l = lines[i]
        if l.startswith("- "):
            out.append([i + 1, l.strip()])
        elif out and l.startswith("  ") and l.strip():
            out[-1][1] += " " + l.strip()
    return out


def check(today, include_memory=True):
    errors, warnings, notes = [], [], []
    path = os.path.join(REPO, TRACKER)
    with open(path, encoding="utf-8") as f:
        tlines = f.read().split("\n")
    block = scheduled_block(tlines)
    if block is None:
        errors.append(f"{TRACKER}: no **Scheduled** list; deferred instructions have nowhere to live")
        block = (0, 0)
    for line, text in entries(tlines, block):
        where = f"{TRACKER}:{line}"
        for field in ("Why:", "Unneeded if:"):
            if field not in text:
                errors.append(f"{where}: Scheduled entry without \"{field}\": {text[:90]}")
        m = ENTRY_DATE.match(text)
        if m:
            day = datetime.date.fromisoformat(m.group(1))
            if day < today:
                errors.append(f"{where}: Scheduled entry past due since {day}; resolve it (check its reason first): {text[:90]}")
            elif day == today:
                warnings.append(f"{where}: Scheduled entry due today; check its reason against today's state before acting, and ask Ian if it no longer holds: {text[:90]}")
            else:
                notes.append(f"{where}: scheduled for {day}")
        else:
            notes.append(f"{where}: conditional: {text[:90]}")

    for f in scanned_files(include_memory):
        rel = os.path.relpath(f, REPO) if f.startswith(REPO) else f.replace(os.path.expanduser("~"), "~")
        with open(f, encoding="utf-8") as fh:
            lines = fh.read().split("\n")
        skip = range(block[0], block[1]) if rel == TRACKER else range(0)
        for i, l in enumerate(lines):
            if i in skip:
                continue
            for m in DEFER.finditer(l):
                day = datetime.date.fromisoformat(m.group(2))
                if day > today:
                    errors.append(f"{rel}:{i + 1}: a deferral to {day} outside the tracker's Scheduled list "
                                  f"(\"{m.group(0)}\"): move it there with its Why: and Unneeded if:, and point to it")
    return errors, warnings, notes


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--today", type=datetime.date.fromisoformat, default=datetime.date.today())
    ap.add_argument("--no-memory", action="store_true", help="skip the local session memory folder")
    ap.add_argument("-v", "--verbose", action="store_true", help="also list entries not yet due")
    a = ap.parse_args()
    errors, warnings, notes = check(a.today, not a.no_memory)
    for n in notes if a.verbose else ():
        print("NOTE  " + n)
    for w in warnings:
        print("WARN  " + w)
    for e in errors:
        print("ERROR " + e)
    print(f"deferred instructions: {len(errors)} errors, {len(warnings)} due today, {len(notes)} waiting")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())

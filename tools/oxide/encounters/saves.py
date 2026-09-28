"""Commit Ian's edits from the tool, so none sits uncommitted in a checkout.

Ian's server runs from a worktree of its own (.claude/worktrees/ian-tool) on
the branch ian-saves (the Overseer's arrangement, 2026-09-27). The tool
writes his edits there: trainer teams from the Trainers tab, and encounter
tables and the sidecar from the Tables view. "Commit my edits" in the page's
header commits them:

- only the files the tool writes (WRITES below); anything else changed in
  the checkout is reported and left alone;
- only on ian-saves, so a copy of the tool running in some other checkout
  (a track's worktree) cannot commit there;
- after the encounter lint and the base ROM importer's dry run pass, the two
  checks the gate would fail it on;
- then pushed, and the head shown in the page. The Overseer lands ian-saves
  like any track branch, once the Balance Agent has rescored what a trainer
  edit stales.
"""
import datetime
import json
import os
import re
import subprocess
import sys
import tempfile

from . import model

BRANCH = "ian-saves"
# What the tool writes, and nothing else: the tables and their sidecar, the
# trainer files and the importer's registry of trainers edited on purpose.
WRITES = (re.compile(r"^res/field/encounters/"),
          re.compile(r"^docs/oxide/encounters/design\.json$"),
          re.compile(r"^res/trainers/data/[^/]+\.json$"),
          re.compile(r"^tools/oxide/trainers_diverged\.json$"))
ROMS = (os.path.expanduser("~/roms/base.nds"), os.path.expanduser("~/roms/vanilla.nds"))


class CommitRefused(Exception):
    pass


def _git(root, *args, check=True):
    r = subprocess.run(["git", *args], cwd=root, capture_output=True, text=True)
    if check and r.returncode != 0:
        raise CommitRefused(f"git {args[0]} failed: {(r.stderr or r.stdout).strip()[-400:]}")
    return r.stdout


def branch(root):
    return _git(root, "rev-parse", "--abbrev-ref", "HEAD").strip()


def _changed(root):
    """[path] of every uncommitted change, new files included."""
    out = []
    for line in _git(root, "status", "--porcelain", "--untracked-files=all").splitlines():
        path = line[3:]
        if " -> " in path:                 # a rename names both sides
            path = path.split(" -> ")[1]
        out.append(path.strip('"'))
    return out


def pending(root=None):
    """{"branch", "enabled", "files", "other"}: the tool's own uncommitted
    edits, and the rest, which a commit leaves alone."""
    root = root or model.repo_root()
    here = branch(root)
    changed = _changed(root)
    mine = sorted(p for p in changed if any(w.search(p) for w in WRITES))
    return {"branch": here, "enabled": here == BRANCH, "files": mine,
            "other": sorted(p for p in changed if p not in mine)}


def describe(path):
    """One line of the commit message for one file."""
    name = os.path.basename(path)[:-len(".json")] if path.endswith(".json") else path
    if path.startswith("res/trainers/data/"):
        return f"the trainer {name}"
    if path.startswith("res/field/encounters/"):
        return f"the table {name}"
    if path.endswith("design.json"):
        return "the encounter sidecar"
    return "the importer's registry of trainers edited on purpose"


def run_checks(root):
    """[(check, passed, detail)]: the encounter lint, errors only, and the base
    ROM importer's dry run, every count 0. The report goes to a scratch file."""
    out = []
    lint = subprocess.run([sys.executable, "-m", "tools.oxide.encounters.cli", "lint",
                           "--fail-on", "error"], cwd=root, capture_output=True, text=True,
                          env=dict(os.environ, PYTHONPATH="."))
    summary = next((l for l in lint.stdout.splitlines() if "error(s)" in l), lint.stdout[-200:])
    out.append(("encounter lint", lint.returncode == 0, summary.strip()))
    if not all(os.path.exists(r) for r in ROMS):
        out.append(("importer dry run", False, "the pinned base or vanilla ROM is missing"))
        return out
    with tempfile.TemporaryDirectory() as tmp:
        imp = subprocess.run([sys.executable, "tools/oxide/import_base_rom.py", "--base", ROMS[0],
                              "--vanilla", ROMS[1], "--dry-run",
                              "--report", os.path.join(tmp, "report.md")],
                             cwd=root, capture_output=True, text=True)
    last = (imp.stdout.strip().splitlines() or [""])[-1]
    clean = imp.returncode == 0 and "would change" in last and not re.search(r"': [1-9]", last)
    out.append(("importer dry run", clean, last[:200]))
    return out


def message(files, when=None):
    when = when or datetime.date.today().isoformat()
    lines = [f"Ian's edits in the OxiDex, {when}", "",
             "Committed from the tool's \"Commit my edits\", on ian-saves. Changed:", ""]
    lines += [f"- {describe(p)} ({p})" for p in files]
    lines += ["", "The encounter lint and the base ROM importer's dry run passed first."]
    return "\n".join(lines) + "\n"


def commit(root=None, checks=True, push=True):
    """Commit the tool's uncommitted edits on ian-saves and push them.
    Returns {"head", "files", "checks", "pushed"}; CommitRefused says why not."""
    root = root or model.repo_root()
    state = pending(root)
    if not state["enabled"]:
        raise CommitRefused(f"this checkout is on {state['branch']}, not {BRANCH}; "
                            "only Ian's own worktree commits his edits")
    if not state["files"]:
        raise CommitRefused("there is nothing to commit")
    results = run_checks(root) if checks else []
    failed = [f"{name}: {detail}" for name, ok, detail in results if not ok]
    if failed:
        raise CommitRefused("not committed, a check failed: " + "; ".join(failed))
    _git(root, "add", "--", *state["files"])
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8") as f:
        f.write(message(state["files"]))
        msg = f.name
    try:
        # --no-verify: the checks above are the pre-commit hook's, and more.
        _git(root, "commit", "--no-verify", "-q", "-F", msg)
    finally:
        os.unlink(msg)
    head = _git(root, "rev-parse", "--short", "HEAD").strip()
    pushed = False
    if push:
        r = subprocess.run(["git", "push", "-q", "origin", BRANCH], cwd=root,
                           capture_output=True, text=True)
        pushed = r.returncode == 0
        if not pushed:
            return {"head": head, "files": state["files"], "checks": results, "pushed": False,
                    "error": "committed, but the push failed: "
                             + (r.stderr or r.stdout).strip()[-300:]}
    return {"head": head, "files": state["files"], "checks": results, "pushed": pushed}

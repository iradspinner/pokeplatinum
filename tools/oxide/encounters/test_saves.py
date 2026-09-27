"""Commit my edits (saves.py): Ian's edits from the tool, committed on ian-saves.

    PYTHONPATH=. python3 -m tools.oxide.encounters.test_saves

Every commit here happens in a throwaway git repository made for the test,
never in the checkout. The route test asks the real server to commit only
when this checkout is not on ian-saves, where it must refuse.
"""
import http.client
import json
import os
import subprocess
import sys
import tempfile
import threading

from . import model
from . import saves
from . import server


def git(root, *args):
    return subprocess.run(["git", *args], cwd=root, capture_output=True, text=True).stdout


def write(root, rel, text):
    path = os.path.join(root, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def scratch_repo(tmp, branch):
    """A small repository shaped like the tree where the tool writes."""
    git(tmp, "init", "-q", "-b", branch)
    git(tmp, "config", "user.name", "test")
    git(tmp, "config", "user.email", "test@example.com")
    for rel in ("res/trainers/data/leader_roark.json", "res/field/encounters/encounters_route_201.json",
                "docs/oxide/encounters/design.json", "README.md"):
        write(tmp, rel, "{}\n")
    git(tmp, "add", "-A")
    git(tmp, "commit", "-q", "-m", "base")


def check_commit(results):
    with tempfile.TemporaryDirectory() as tmp:
        scratch_repo(tmp, saves.BRANCH)
        write(tmp, "res/trainers/data/leader_roark.json", '{"edited": true}\n')
        write(tmp, "res/field/encounters/encounters_route_201.json", '{"edited": true}\n')
        write(tmp, "tools/oxide/trainers_diverged.json", '{"leader_roark": {}}\n')
        write(tmp, "README.md", "someone else's work in progress\n")
        state = saves.pending(tmp)
        results.append(("the badge counts only what the tool writes; anything else is left alone",
                        state["enabled"] and state["files"] == [
                            "res/field/encounters/encounters_route_201.json",
                            "res/trainers/data/leader_roark.json",
                            "tools/oxide/trainers_diverged.json"]
                        and state["other"] == ["README.md"], str(state)))
        out = saves.commit(tmp, checks=False, push=False)
        log = git(tmp, "log", "-1", "--format=%B")
        committed = git(tmp, "show", "--name-only", "--format=", "HEAD").split()
        left = git(tmp, "status", "--porcelain").split()
        results.append(("a commit takes the tool's files and names each one, and leaves the rest",
                        out["head"] and sorted(committed) == state["files"]
                        and "the trainer leader_roark" in log and "the table encounters_route_201" in log
                        and left == ["M", "README.md"], f"{out['head']}: {committed}"))
        try:
            saves.commit(tmp, checks=False, push=False)
            nothing = False
        except saves.CommitRefused:
            nothing = True
        results.append(("with nothing waiting, a commit is refused", nothing, ""))
    with tempfile.TemporaryDirectory() as tmp:
        scratch_repo(tmp, "oxide")
        write(tmp, "res/trainers/data/leader_roark.json", '{"edited": true}\n')
        try:
            saves.commit(tmp, checks=False, push=False)
            refused = False
        except saves.CommitRefused:
            refused = True
        results.append(("a checkout on any branch but ian-saves never commits",
                        refused and not saves.pending(tmp)["enabled"]
                        and git(tmp, "rev-list", "--count", "HEAD").strip() == "1", ""))


def check_routes(results):
    root = model.repo_root()
    httpd = server.Server(("127.0.0.1", 0), server.Handler)
    port = httpd.server_address[1]
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    try:
        conn = http.client.HTTPConnection("127.0.0.1", port, timeout=60)
        conn.request("GET", "/api/saves")
        r = conn.getresponse()
        state = json.loads(r.read())
        refused = None
        # Only where a commit must be refused: never on Ian's own branch.
        if not state.get("enabled"):
            conn.request("POST", "/api/saves/commit", "{}", {"Content-Type": "application/json"})
            r2 = conn.getresponse()
            refused = r2.status == 409 and "not ian-saves" in json.loads(r2.read())["error"]
        conn.close()
    finally:
        httpd.shutdown()
        httpd.server_close()
    results.append(("/api/saves reports the branch and the edits; a commit outside ian-saves "
                    "is refused (409)", r.status == 200 and "files" in state
                    and state["branch"] == saves.branch(root) and refused in (True, None),
                    f"{state.get('branch')}, {len(state.get('files', []))} waiting"))


def main():
    results = []
    check_commit(results)
    check_routes(results)
    width = max(len(l) for l, _, _ in results)
    failed = 0
    for label, ok, note in results:
        failed += not ok
        print(f"  {'ok  ' if ok else 'FAIL'}  {label:{width}}  {note}")
    print(f"\n{len(results) - failed}/{len(results)} passed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())

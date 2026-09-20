"""M4 acceptance: the server's endpoints, and that an edit stays local.

    PYTHONPATH=. python3 -m tools.oxide.encounters.test_m4

Starts the server on a spare port, drives it over HTTP the way the page does,
and restores every file it touched. The gate is the design doc's: an edit made
through the UI lands in git diff at the right key with no other key touched.
"""
import json
import subprocess
import sys
import threading
import urllib.error
import urllib.request

from . import model
from . import server as srv

PORT = 8799
BASE = f"http://127.0.0.1:{PORT}"
AREA = "encounters_route_214"


def get(path):
    with urllib.request.urlopen(BASE + path, timeout=10) as r:
        return json.loads(r.read())


def post(path, body):
    req = urllib.request.Request(
        BASE + path, data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            return r.status, json.loads(r.read())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read())


def git(*args):
    return subprocess.run(["git", *args], cwd=model.repo_root(),
                          capture_output=True, text=True).stdout


def changed_lines(path):
    """(added, removed) content lines for one file, headers excluded."""
    out = git("diff", "-U0", "--", path).splitlines()
    add = [l for l in out if l.startswith("+") and not l.startswith("+++")]
    rem = [l for l in out if l.startswith("-") and not l.startswith("---")]
    return add, rem


def check_endpoints(results):
    areas = get("/api/areas")
    results.append(("GET /api/areas returns every live table",
                    len(areas["rows"]) == 171, f"{len(areas['rows'])} rows"))
    results.append(("areas carries game metrics and lint",
                    "game" in areas and "game_findings" in areas
                    and "thresholds" in areas, ""))
    sp = get("/api/species")["species"]
    results.append(("GET /api/species is clean",
                    len(sp) > 400 and not any("." in s for s in sp),
                    f"{len(sp)} species"))
    d = get(f"/api/area/{AREA}")
    results.append(("GET /api/area has slots, rungs, merged, lint",
                    len(d["slots"]) == 12 and d["rungs"] and d["merged"]
                    and "findings" in d,
                    f"{len(d['rungs'])} rungs, {len(d['merged'])} species"))


def check_rejections(results):
    """The page's datalist is a suggestion, not a constraint, so the server is
    the only thing standing between a typo and a broken build."""
    cases = [
        ("bad species refused", f"/api/area/{AREA}/slot",
         {"slot": 0, "species": "SPECIES_GIBEL"}, 400),
        ("bad level refused", f"/api/area/{AREA}/slot",
         {"slot": 0, "level": 999}, 400),
        ("bad slot refused", f"/api/area/{AREA}/slot",
         {"slot": 12, "level": 5}, 400),
        ("bad time index refused", f"/api/area/{AREA}/time",
         {"layer": "night", "index": 7, "species": "SPECIES_ABRA"}, 400),
        ("non-time layer refused", f"/api/area/{AREA}/time",
         {"layer": "radar", "index": 0, "species": "SPECIES_ABRA"}, 400),
    ]
    for label, path, body, want in cases:
        code, payload = post(path, body)
        results.append((label, code == want,
                        f"HTTP {code} {payload.get('error', '')[:60]}"))
    add, rem = changed_lines(f"{model.ENC_DIR}/{AREA}.json")
    results.append(("a refused write changes nothing on disk",
                    not add and not rem, f"{len(add)} added, {len(rem)} removed"))


def check_edit_is_local(results):
    """The M4 gate itself."""
    path = f"{model.ENC_DIR}/{AREA}.json"
    before = get(f"/api/area/{AREA}")
    try:
        code, out = post(f"/api/area/{AREA}/slot",
                         {"slot": 4, "level": before["slots"][4]["level"] + 1})
        results.append(("slot write accepted", code == 200 and out.get("changed"),
                        f"HTTP {code}"))
        add, rem = changed_lines(path)
        results.append(("one slot edit -> one line in git diff",
                        len(add) == 1 and len(rem) == 1,
                        f"+{len(add)} -{len(rem)}"))
        results.append(("the line that moved is the level",
                        bool(add) and '"level"' in add[0],
                        add[0].strip() if add else ""))

        code, _ = post(f"/api/area/{AREA}/time",
                       {"layer": "day", "index": 0, "species": "SPECIES_ABRA"})
        add, rem = changed_lines(path)
        results.append(("a day-layer write adds exactly one more line",
                        len(add) == 2 and len(rem) == 2,
                        f"+{len(add)} -{len(rem)}"))

        code, out = post(f"/api/area/{AREA}/rate", {"land_rate": 25})
        add, _ = changed_lines(path)
        results.append(("a land_rate write adds exactly one more line",
                        len(add) == 3, f"+{len(add)}"))
        results.append(("the response carries fresh metrics",
                        out["land_rate"] == 25 and "metrics" in out, ""))
    finally:
        subprocess.run(["git", "checkout", "--", path], cwd=model.repo_root())
    add, rem = changed_lines(path)
    results.append(("test restored the file", not add and not rem, ""))


def main():
    httpd = srv.Server(("127.0.0.1", PORT), srv.Handler)
    t = threading.Thread(target=httpd.serve_forever, daemon=True)
    t.start()
    results = []
    try:
        for check in (check_endpoints, check_rejections, check_edit_is_local):
            check(results)
    finally:
        httpd.shutdown()
    width = max(len(l) for l, _, _ in results)
    failed = 0
    for label, ok, note in results:
        failed += not ok
        print(f"  {'ok  ' if ok else 'FAIL'}  {label:{width}}  {note}")
    print(f"\n{len(results) - failed}/{len(results)} passed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())

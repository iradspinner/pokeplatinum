"""M4 acceptance: the server's endpoints, and that an edit stays local.

    PYTHONPATH=. python3 -m tools.oxide.encounters.test_m4

Starts the server on a spare port, drives it over HTTP the way the page does,
and restores every file it touched. The gate is the design doc's: an edit made
through the UI lands in git diff at the right key with no other key touched.
"""
import json
import os
import subprocess
import sys
import threading
import urllib.error
import urllib.request

from . import analysis as A
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


_SNAPSHOTS = {}


def snapshot(path):
    """Remember a file's text so writes can be measured against it and undone.
    Restoring with `git checkout --` would throw away every uncommitted change
    in the file, not just this suite's; in this shared checkout that reverted
    Route 214 and Route 205 south to stale tables more than once."""
    with open(os.path.join(model.repo_root(), path), encoding="utf-8") as f:
        _SNAPSHOTS[path] = f.read()


def restore(path):
    with open(os.path.join(model.repo_root(), path), "w",
              encoding="utf-8", newline="\n") as f:
        f.write(_SNAPSHOTS[path])


def changed_lines(path):
    """(added, removed) content lines for one file, headers excluded: against
    the snapshot when one was taken, else against HEAD."""
    if path in _SNAPSHOTS:
        import tempfile
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False,
                                         encoding="utf-8", newline="\n") as f:
            f.write(_SNAPSHOTS[path])
            snap = f.name
        try:
            out = git("diff", "--no-index", "-U0", "--", snap,
                      os.path.join(model.repo_root(), path)).splitlines()
        finally:
            os.unlink(snap)
    else:
        out = git("diff", "-U0", "--", path).splitlines()
    add = [l for l in out if l.startswith("+") and not l.startswith("+++")]
    rem = [l for l in out if l.startswith("-") and not l.startswith("---")]
    return add, rem


def check_endpoints(results):
    areas = get("/api/areas")
    # Every area with a table of any kind: the live grass tables plus the
    # water-only areas (Twinleaf Town, Route 219 and the cities), which are
    # capture areas by their rods (Ian, 2026-09-21).
    want = sum(1 for a in model.load_all() if a.land_active or a.kinds_present())
    results.append(("GET /api/areas returns every area with a table of any kind",
                    len(areas["rows"]) == want, f"{len(areas['rows'])} rows, want {want}"))
    results.append(("areas carries game metrics and lint",
                    "game" in areas and "game_findings" in areas
                    and "thresholds" in areas, ""))
    sp = get("/api/species")["species"]
    results.append(("GET /api/species is the whole dex, labelled",
                    len(sp) > 400
                    and all("value" in r and "label" in r for r in sp)
                    and not any("." in r["value"] for r in sp),
                    f"{len(sp)} species"))
    d = get(f"/api/area/{AREA}")
    results.append(("GET /api/area has slots, rungs, merged, lint",
                    len(d["slots"]) == 12 and d["rungs"] and d["merged"]
                    and "findings" in d,
                    f"{len(d['rungs'])} rungs, {len(d['merged'])} species"))
    results.append(("rows carry play order and caught state",
                    all(k in areas["rows"][0] for k in
                        ("level_min", "level_med", "live_species",
                         "best_share", "holds")), ""))


def check_display_names(results):
    """The page never shows a raw constant. Six names plus farfetchd need
    special handling; everything else title-cases."""
    labels = {r["value"]: r["label"] for r in get("/api/species")["species"]}
    want = {
        "SPECIES_GLALIE": "Glalie",
        "SPECIES_NIDORAN_F": "Nidoran♀",
        "SPECIES_NIDORAN_M": "Nidoran♂",
        "SPECIES_MR_MIME": "Mr. Mime",
        "SPECIES_MIME_JR": "Mime Jr.",
        "SPECIES_HO_OH": "Ho-Oh",
        "SPECIES_PORYGON_Z": "Porygon-Z",
        "SPECIES_FARFETCHD": "Farfetch'd",
        "SPECIES_PORYGON2": "Porygon2",
    }
    bad = {k: labels.get(k) for k, v in want.items() if labels.get(k) != v}
    results.append(("special-cased names are right", not bad, str(bad)))
    results.append(("no label leaks SPECIES_ or shouts",
                    not any("SPECIES_" in v or v.isupper()
                            for v in labels.values()), ""))
    d = get(f"/api/area/{AREA}")
    results.append(("area payload labels every species",
                    all("label" in s for s in d["slots"])
                    and all("label" in m for m in d["merged"])
                    and all("label" in p for r in d["rungs"] for p in r["pool"]),
                    ""))


def check_caught_is_global(results):
    """Ticking one species has to move every table that holds it, because the
    dupes clause is what makes a distant table worth walking to."""
    post("/api/caught", {"clear": True})
    before = {r["area"]: r for r in get("/api/areas")["rows"]}
    code, payload = post("/api/caught",
                         {"area": "encounters_route_201",
                          "species": "SPECIES_WOOLOO"})
    results.append(("caught write is recorded against its area",
                    code == 200
                    and payload["encounters"] == {"encounters_route_201":
                                                  "SPECIES_WOOLOO"},
                    f"HTTP {code}"))
    rows = {r["area"]: r for r in get("/api/areas")["rows"]}
    results.append(("the area list shows what was caught there",
                    rows["encounters_route_201"]["encounter_label"] == "Wooloo"
                    and rows["encounters_route_202"]["encounter_label"] is None,
                    ""))
    code, payload = post("/api/caught",
                         {"area": "encounters_route_201",
                          "species": "SPECIES_SHINX"})
    results.append(("a second tick on the same area replaces the first",
                    payload["encounters"] == {"encounters_route_201":
                                              "SPECIES_SHINX"}, ""))
    post("/api/caught", {"area": "encounters_route_201",
                         "species": "SPECIES_WOOLOO"})
    after = {r["area"]: r for r in get("/api/areas")["rows"]}
    moved = [a for a in before
             if before[a]["live_species"] != after[a]["live_species"]]
    results.append(("one tick moves every table holding it",
                    len(moved) > 1, f"{len(moved)} tables"))
    improved = [a for a in moved
                if after[a]["best_share"] > before[a]["best_share"]]
    results.append(("removing owned mass lifts the odds elsewhere",
                    bool(improved),
                    f"{len(improved)} tables, e.g. "
                    f"{improved[0] if improved else '-'}"))

    d = get(f"/api/area/encounters_route_201")
    bidoof = [s for s in d["slots"] if s["species"] == "SPECIES_WOOLOO"]
    results.append(("slots report caught state",
                    bidoof and all(s["caught"] for s in bidoof), ""))
    pool = d["rungs"][0]["pool"]
    live = [p for p in pool if not p["caught"]]
    total = sum(p["cond"] for p in live if p["cond"] is not None)
    results.append(("conditional odds renormalise over the uncaught",
                    abs(total - 1.0) < 1e-9, f"sum {total:.6f}"))
    results.append(("caught species carry no conditional share",
                    all(p["cond"] is None for p in pool if p["caught"]), ""))

    code, _ = post("/api/caught", {"area": "encounters_route_201",
                                   "species": "SPECIES_NOPE"})
    results.append(("unknown species refused", code == 400, f"HTTP {code}"))
    code, _ = post("/api/caught", {"species": "SPECIES_WOOLOO"})
    results.append(("a tick without an area is refused", code == 400,
                    f"HTTP {code}"))
    post("/api/caught", {"clear": True})
    results.append(("clear empties every encounter",
                    get("/api/caught")["encounters"] == {}, ""))


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
    snapshot(f"{model.ENC_DIR}/{AREA}.json")
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
    snapshot(path)
    before = get(f"/api/area/{AREA}")
    try:
        code, out = post(f"/api/area/{AREA}/slot",
                         {"slot": 4, "level": before["slots"][4]["level_min"] + 1})
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
                        out["rate"] == 25 and "metrics" in out, ""))
    finally:
        restore(path)
    add, rem = changed_lines(path)
    results.append(("test restored the file", not add and not rem, ""))


def check_lines_dupe_out(results):
    """The dupes clause works on families, not species. Catching Shinx on
    Route 201 has to zero every Shinx-line entry everywhere."""
    post("/api/caught", {"clear": True})
    _, payload = post("/api/caught",
                      {"area": "encounters_route_201",
                       "species": "SPECIES_SHINX"})
    results.append(("catching one species owns its whole line",
                    set(payload["owned"]) == {"SPECIES_SHINX",
                                              "SPECIES_LUXIO",
                                              "SPECIES_LUXRAY"},
                    ", ".join(payload["owned"])))

    d = get("/api/area/encounters_route_202?kind=land")
    starly = [m for m in d["merged"] if m["species"] == "SPECIES_SHINX"][0]
    others = [m for m in d["merged"] if m["species"] != "SPECIES_SHINX"]
    results.append(("a caught species drops to zero",
                    starly["cond"] == 0, f"{starly['cond']}"))
    results.append(("everything else renormalises to 100%",
                    abs(sum(m["cond"] for m in others) - 1.0) < 1e-9,
                    f"{sum(m['cond'] for m in others) * 100:.4f}%"))
    results.append(("the rest actually rise",
                    all(m["cond"] > m["share"] for m in others), ""))
    results.append(("slot odds match the merged view",
                    abs(sum(s["odds"] for s in d["slots"]) - 1.0) < 1e-9, ""))

    # Every authored land table holds first stages only, so the evolved line
    # member to find is on a Super Rod table: Gyarados in Twinleaf's water,
    # duped out by a Magikarp caught on Lake Verity's Old Rod.
    post("/api/caught", {"area": "encounters_lake_verity", "species": "SPECIES_MAGIKARP"})
    n = get("/api/area/encounters_twinleaf_town?kind=super_rod")
    staravia = [m for m in n["merged"] if m["species"] == "SPECIES_GYARADOS"]
    results.append(("an uncaught line member reads as duped",
                    bool(staravia) and staravia[0]["duped"]
                    and not staravia[0]["caught"]
                    and staravia[0]["cond"] == 0, ""))
    results.append(("a duped row says where and by what",
                    bool(staravia) and staravia[0]["caught_at"] == "lake verity"
                    and staravia[0]["via"] == "Magikarp",
                    f"{staravia[0]['via'] if staravia else '-'}, "
                    f"{staravia[0]['caught_at'] if staravia else '-'}"))
    d201 = get("/api/area/encounters_route_201?kind=land")
    results.append(("the centre carries the area's encounter",
                    d201["encounter_label"] == "Shinx", ""))
    post("/api/caught", {"clear": True})


def check_plan_endpoint(results):
    """The planner over HTTP, the way the page calls it."""
    post("/api/caught", {"clear": True})
    d = get("/api/plan?area=encounters_route_214&species=SPECIES_GROWLITHE"
            "&kind=land")
    results.append(("GET /api/plan returns a front with prose",
                    d.get("front") and len(d["lines"]) == len(d["front"]),
                    f"{len(d.get('front', []))} points"))
    results.append(("plan prose names species, not constants",
                    all("SPECIES_" not in s for s in d.get("lines", [])), ""))
    code, err = post("/api/caught", {"clear": True})
    d2 = get("/api/plan?area=encounters_route_214&species=SPECIES_NOPE")
    results.append(("plan for an absent species has no front",
                    not d2.get("front"), ""))


def check_water_tables(results):
    """Surf and the three rods, with the fractional repel their level ranges
    require."""
    d = get("/api/area/encounters_route_205_south?kind=surf")
    results.append(("surf table loads with five slots",
                    len(d["slots"]) == 5 and d["ranged"],
                    f"rate {d['rate']}"))
    results.append(("all four water kinds are offered",
                    set(d["kinds"]) == {"land", "surf", "old_rod",
                                        "good_rod", "super_rod"},
                    ", ".join(d["kinds"])))
    results.append(("water slots carry a level range",
                    all("level_min" in s and "level_max" in s
                        for s in d["slots"]), ""))
    results.append(("lint does not run on water tables",
                    d["findings"] == [], "rules are calibrated on land"))

    rates = A.SURF_RATES
    slots = [(s["species"], s["level_min"], s["level_max"]) for s in d["slots"]]
    base = A.merged(slots, rates)
    top = A.pool(slots, slots[0][2], rates)
    first = slots[0][0]
    results.append(("a mid-range lead shrinks a slot rather than cutting it",
                    0 < top.get(first, 0) < base[first],
                    f"{base[first]:.3f} -> {top.get(first, 0):.3f}"))

    path = f"{model.ENC_DIR}/encounters_route_205_south.json"
    snapshot(path)
    try:
        code, out = post("/api/area/encounters_route_205_south/slot",
                         {"kind": "surf", "slot": 0,
                          "level_max": d["slots"][0]["level_max"] + 1})
        add, rem = changed_lines(path)
        results.append(("a surf edit is one line at the right key",
                        code == 200 and len(add) == 1 and len(rem) == 1
                        and "level_max" in add[0],
                        add[0].strip() if add else f"HTTP {code}"))
    finally:
        restore(path)


def main():
    httpd = srv.Server(("127.0.0.1", PORT), srv.Handler)
    t = threading.Thread(target=httpd.serve_forever, daemon=True)
    t.start()
    results = []
    try:
        for check in (check_endpoints, check_display_names,
                      check_caught_is_global, check_lines_dupe_out,
                      check_water_tables, check_rejections,
                      check_edit_is_local):
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

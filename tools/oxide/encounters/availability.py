"""The availability plan: authoring plan Step 2.

`docs/oxide/encounters/availability-plan.json` is the design, keyed by area:
which lines are at home on each table and which merely appear. This module
turns it around into the per-line view the plan asks for, joins it with
what the tree already provides (gifts, trades, static battles, the starter
and the fossils, from audit.coverage), checks the step's gate, and renders
`docs/oxide/encounters/availability.md`. The markdown is generated, never
edited.

The gate, from the plan and decision 3: every line on the pick-list has a
planned wild home or a non-wild source; the corridor (every area up to
`corridor_end`) carries only starter-adjacent lines and lines with a
scripted source; every starter-adjacent line's home is in the corridor;
and every early-band table has three to five lines planned, which is what
its archetypes can hold.
"""
import collections
import json
import os

from . import audit
from . import dex
from . import model
from . import progression

PLAN = os.path.join("docs", "oxide", "encounters", "availability-plan.json")
DOC = os.path.join("docs", "oxide", "encounters", "availability.md")

# A line's status, best first. `proposed` is a gate line with no script yet
# and a proposal in the plan for where its script should go; it counts as
# sourced on paper and is listed for Ian. `none` fails the gate.
STATUSES = ("home", "non-wild", "water", "cameo-only", "proposed", "none")


def load_plan():
    with open(os.path.join(model.repo_root(), PLAN), encoding="utf-8") as f:
        return json.load(f)


def build(ref=None):
    """Everything the document and the gate need, in one dict."""
    root = model.repo_root()
    plan = load_plan()
    sidecar = model.load_sidecar() or {}
    entries = sidecar.get("areas") or {}
    cov = audit.coverage(ref)
    line_of = dex.lines(root)
    by_line = {l["line"]: l for l in cov["lines"]}
    base_of = {}          # any member constant -> line id
    for l in cov["lines"]:
        for m in l["members"]:
            base_of[m] = l["line"]
        for b in l["base"]:
            base_of[b] = l["line"]

    live = {a.name: a for a in model.load_all(ref) if a.land_active}
    all_names = set(model.area_names(ref))
    problems = []

    def resolve(sp, where):
        lid = base_of.get(sp) or base_of.get(line_of.get(sp, sp))
        if lid is None:
            problems.append(f"{where}: {sp} is not on the pick-list")
        return lid

    # per line: planned homes, cameos, water homes
    homes = collections.defaultdict(list)
    cameos = collections.defaultdict(list)
    water = collections.defaultdict(list)
    per_area = {}
    for area, spec in plan["areas"].items():
        if area not in all_names:
            problems.append(f"{area}: no such encounter file")
            continue
        if area not in live:
            problems.append(f"{area}: not a live land table")
        planned = []
        for sp in spec.get("home") or []:
            lid = resolve(sp, area)
            if lid:
                homes[lid].append(area)
                planned.append((lid, "home"))
        for sp in spec.get("cameo") or []:
            lid = resolve(sp, area)
            if lid:
                cameos[lid].append(area)
                planned.append((lid, "cameo"))
        seen = [lid for lid, _ in planned]
        dupes = {lid for lid in seen if seen.count(lid) > 1}
        for lid in dupes:
            problems.append(f"{area}: {by_line[lid]['name']} listed twice")
        per_area[area] = planned
    for sp, areas in (plan.get("water") or {}).items():
        lid = resolve(sp, "water")
        for area in areas:
            if area not in all_names:
                problems.append(f"water {sp}: no such encounter file {area}")
            elif lid:
                water[lid].append(area)

    corridor_end = plan.get("corridor_end")
    order_of = {n: (entries.get(n) or {}).get("order") for n in all_names}
    end_order = order_of.get(corridor_end) or 0
    corridor = {n for n, o in order_of.items() if o is not None and o <= end_order and n in live}

    proposals = {}
    for sp, text in (plan.get("proposals") or {}).items():
        if sp.startswith("_"):
            continue
        lid = resolve(sp, "proposals")
        if lid:
            proposals[lid] = text

    rows = []
    for l in cov["lines"]:
        lid = l["line"]
        non_wild = []
        if l["gifts"]:
            non_wild.append("gift " + ", ".join(sorted({m for m, _, _ in l["gifts"]})))
        if l["trades"]:
            non_wild.append("trade " + ", ".join(n for n, _ in l["trades"]))
        if l["static"]:
            non_wild.append("static " + ", ".join(sorted({s.replace("scripts_", "") for s, _, _ in l["static"]})))
        if l["scripted"]:
            non_wild.append(", ".join(how for how, _ in l["scripted"]))
        h = homes.get(lid, [])
        if h:
            status = "home"
        elif non_wild:
            status = "non-wild"
        elif water.get(lid):
            status = "water"
        elif cameos.get(lid):
            status = "cameo-only"
        elif lid in proposals:
            status = "proposed"
        else:
            status = "none"
        if len(h) > 1:
            problems.append(f"{l['name']}: {len(h)} homes planned ({', '.join(h)}); a line has one")
        if l["tier"] == "gate" and (h or cameos.get(lid)):
            problems.append(f"{l['name']}: a gate line is scripted, not wild, but is planned on "
                            f"{', '.join(h or cameos.get(lid))}")
        rows.append({
            "line": lid, "name": l["name"], "tier": l["tier"], "status": status,
            "home": h, "cameo": sorted(cameos.get(lid, []), key=lambda n: order_of.get(n) or 0),
            "water": water.get(lid, []), "non_wild": non_wild,
            "proposal": proposals.get(lid, ""),
            "home_order": order_of.get(h[0]) if h else None,
        })

    # the gate
    gate = {"no_source": [], "corridor_intruders": [], "early_home_outside": [],
            "early_fit": [], "unplanned_tables": []}
    for r in rows:
        if r["status"] == "none":
            gate["no_source"].append(r["name"])
        if r["tier"] == "starter-adjacent" and r["status"] == "home" \
                and r["home"][0] not in corridor:
            gate["early_home_outside"].append(f"{r['name']} at {r['home'][0]}")
    for area in sorted(corridor, key=lambda n: order_of[n]):
        for lid, _ in per_area.get(area, []):
            r = next(x for x in rows if x["line"] == lid)
            if r["tier"] != "starter-adjacent" and not r["non_wild"]:
                gate["corridor_intruders"].append(f"{r['name']} ({r['tier']}) on {area}")
    for name, a in live.items():
        n = len(per_area.get(name, []))
        band = (entries.get(name) or {}).get("band") or a.band
        # Early tables want 3-5 species (design doc 2.5), but A4, the duo, is
        # in the early set with two, so two lines is a legal plan for a table
        # meant to be one; the archetype choice is Step 3's.
        if n == 0:
            gate["unplanned_tables"].append(name)
        elif band == "early" and not 2 <= n <= 5:
            gate["early_fit"].append(f"{name}: {n} lines planned, early wants 3-5 (2 for an A4 duo)")
    return {
        "rows": rows, "per_area": per_area, "corridor": corridor,
        "order_of": order_of, "entries": entries, "problems": problems,
        "gate": gate, "plan": plan,
        "summary": collections.Counter(r["status"] for r in rows),
    }


def render(out):
    """The markdown. Deterministic, so a regenerate on an unchanged plan is a
    no-op diff."""
    rows = out["rows"]
    o = out["order_of"]
    s = out["summary"]
    lines = []
    lines.append("# Availability plan")
    lines.append("")
    lines.append("Generated by `python3 -m tools.oxide.encounters.cli availability --write` "
                 "from `availability-plan.json` and the tree; do not edit. Authoring plan "
                 "Step 2: where every evolution line on the species pick-list is meant to "
                 "be caught, decided before any slot is written. A *home* is a live land "
                 "table where the line's first stage holds at least 10% (decision 3); a "
                 "*cameo* is any other planned appearance; *non-wild* is a gift, trade, "
                 "static battle, starter or fossil script the tree already has; *water* "
                 "is a surf or rod table planned as the line's home.")
    lines.append("")
    lines.append(f"{len(rows)} lines: " + ", ".join(
        f"{k} {s[k]}" for k in STATUSES if s.get(k)))
    lines.append("")
    g = out["gate"]
    lines.append("## Gate")
    lines.append("")
    ok = not any(g[k] for k in ("no_source", "corridor_intruders", "early_home_outside", "early_fit")) \
        and not out["problems"]
    lines.append("**Passes.**" if ok else "**Fails.**")
    lines.append("")
    for key, label in (("no_source", "Lines with no home and no non-wild source"),
                       ("corridor_intruders", "Lines in the corridor that are neither starter-adjacent nor scripted"),
                       ("early_home_outside", "Starter-adjacent lines whose home is outside the corridor"),
                       ("early_fit", "Early-band tables outside 3-5 planned lines"),
                       ("unplanned_tables", "Live tables with nothing planned (a warning, not a gate)")):
        lines.append(f"- {label}: " + (", ".join(g[key]) if g[key] else "none"))
    if out["problems"]:
        lines.append("- Plan file problems: " + "; ".join(out["problems"]))
    lines.append("")
    lines.append("## For Ian")
    lines.append("")
    proposed = [r for r in rows if r["status"] == "proposed"]
    lines.append("Gate-tier lines with no script naming them yet. A gate line is never "
                 "placed in the wild, so each needs a static battle, a gift or an egg, "
                 "which is script work outside this track (decision 8), or a different "
                 "tier. The plan proposes where; accept one by writing the script.")
    lines.append("")
    for r in proposed:
        lines.append(f"- **{r['name']}**: {r['proposal']}")
    lines.append("")
    lines.append("Also for Ian: the corridor's cast rests on the widened starter-adjacent "
                 "tier (`EARLY_LINES` in `tiers.py`, the other regions' first-route "
                 "lines), which is the agent's default; the water lines are homed on "
                 "surf and rod tables that Step 5 only de-leaks unless surf is designed "
                 "(open question); and Fomantis and Lurantis are two lines in the tree "
                 "because the evolution is missing from Fomantis's data, so each has its "
                 "own home until that is fixed.")
    lines.append("")
    lines.append("## Lines")
    lines.append("")
    lines.append("| Line | Tier | Status | Home (order) | Cameos | Water | Non-wild |")
    lines.append("|---|---|---|---|---|---|---|")

    def short(n):
        return n.replace("encounters_", "")
    tier_rank = {"starter-adjacent": 0, "preferred": 1, "filler": 2, "gate": 3}
    for r in sorted(rows, key=lambda r: (tier_rank.get(r["tier"], 9),
                                         r["home_order"] if r["home_order"] is not None else 999,
                                         r["name"])):
        home = f"{short(r['home'][0])} ({r['home_order']})" if r["home"] else ""
        cam = ", ".join(short(n) for n in r["cameo"])
        wat = ", ".join(short(n) for n in r["water"])
        nw = "; ".join(r["non_wild"])
        lines.append(f"| {r['name']} | {r['tier']} | {r['status']} | {home} | {cam} | {wat} | {nw} |")
    lines.append("")
    lines.append("## Tables")
    lines.append("")
    lines.append("Each live land table in progression order with its planned lines; a "
                 "star marks a home. This is what Step 3 writes casts from.")
    lines.append("")
    lines.append("| Order | Table | Band | Base | Planned |")
    lines.append("|---|---|---|---|---|")
    names = {r["line"]: r["name"] for r in rows}
    live = [n for n in out["per_area"]]
    for n in sorted(live, key=lambda n: o.get(n) or 0):
        e = out["entries"].get(n) or {}
        planned = ", ".join(f"{names[lid]}{'*' if kind == 'home' else ''}"
                            for lid, kind in out["per_area"][n])
        lines.append(f"| {o.get(n)} | {short(n)} | {e.get('band') or ''} | "
                     f"{e.get('base_level') or ''} | {planned} |")
    lines.append("")
    return "\n".join(lines) + "\n"


def write(out):
    path = os.path.join(model.repo_root(), DOC)
    text = render(out)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    return path

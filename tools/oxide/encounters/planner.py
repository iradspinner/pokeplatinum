"""The dupe-out planner. Design doc section 6.4; pure functions, no I/O.

The question it answers: I want species Y on table T. What should I catch
first, and where, so that when I get to T my one counting encounter is Y?

Ian's model, from the design doc: "if a late game encounter table has 99%
rattata and 1% mewtwo, a previous table that has rattata as part of a repel
manip is suddenly very enticing because it can guarantee you a later mewtwo."
So the value of a table is also what it lets you *remove* from a later one.

Two things the per-area caught model (M4, third round) adds to the doc's
description, both enforced here:

  * A source consumes its area's one encounter. Sources must therefore be
    areas earlier in progression than T, with no encounter recorded yet, and
    each source supplies exactly one line. The doc's own example -- pre-catch
    Hippopotas on Route 214 itself -- is not legal under this rule.
  * The dupes clause works on lines, so what gets removed from T is a whole
    family, and any member of it caught anywhere earlier will do.

Cost model, from the doc: total = sum of acquisition costs + expected
encounters at T. Acquisition cost of a line is the fewest expected encounters
to meet a member at the best rung of the best source, 1/P; this assumes the
player can flee non-targets and keep going, which is what "manip" means in
the doc. The one-shot odds -- the chance the very first counting encounter is
the target -- are reported beside it so both readings are visible.

Search space is small (a table has at most 12 species, so at most 12 lines,
and only rungs where Y survives are worth considering), so it is enumerated
exhaustively. Do not get clever.
"""
import itertools

from . import analysis as A

INF = float("inf")


def _line_members(line_id, members_of):
    return set(members_of.get(line_id, (line_id,)))


def acquisition_options(line_id, areas, target_name, owned, line_of,
                        members_of):
    """Where could any member of this line be caught, before target_name?

    Returns [(cost, area_name, kind, lead_level, species, p, one_shot)] sorted
    by cost, one entry per area (its best kind and rung). Areas at or after
    the target, and areas whose encounter is already used, are excluded.
    """
    members = _line_members(line_id, members_of)
    out = []
    target_order = next(a["order"] for a in areas if a["name"] == target_name)
    for area in areas:
        if area["order"] >= target_order or area["used"]:
            continue
        best = None
        for kind, slots in area["tables"].items():
            _, _, rates = A.TABLE_KINDS[kind]
            present = {A._norm(s)[0] for s in slots} & members
            if not present:
                continue
            for lead, pool in A.distinct_rungs(slots, rates):
                cond = A.conditional(pool, owned)
                for sp in present:
                    p = pool.get(sp, 0.0)
                    if p <= 0:
                        continue
                    cand = (1.0 / p, area["name"], kind, lead, sp, p,
                            cond.get(sp, 0.0))
                    if best is None or cand[0] < best[0]:
                        best = cand
        if best:
            out.append(best)
    out.sort(key=lambda c: c[0])
    return out


def assign_sources(lines, options_by_line):
    """Give each line a distinct source area, cheapest first.

    Greedy with fallback: lines are taken in order of their cheapest option,
    each gets the cheapest area not already spoken for. Exact matching would
    be overkill for at most a dozen lines; this is close and explainable.
    Returns (assignments, total_cost) or (None, INF) if some line has no
    source left.
    """
    order = sorted(lines, key=lambda l: (options_by_line[l][0][0]
                                         if options_by_line[l] else INF))
    taken, assignments, total = set(), [], 0.0
    for line in order:
        chosen = next((o for o in options_by_line[line] if o[1] not in taken),
                      None)
        if chosen is None:
            return None, INF
        taken.add(chosen[1])
        assignments.append((line, chosen))
        total += chosen[0]
    return assignments, total


def plan(target_name, target_species, kind, areas, owned, line_of,
         members_of):
    """The Pareto front of (total cost, P(Y)) over every subset of removable
    lines and every rung of the target table.

    areas: [{"name", "order", "used", "tables": {kind: slots}}] in
    progression order. owned: the expanded set of species already duped out.
    line_of / members_of: species -> line id, line id -> members.
    """
    target = next(a for a in areas if a["name"] == target_name)
    slots = target["tables"][kind]
    _, _, rates = A.TABLE_KINDS[kind]
    y_line = line_of.get(target_species, target_species)

    # lines on T that could be removed: not Y's, not already owned
    removable = sorted({
        line_of.get(A._norm(s)[0], A._norm(s)[0]) for s in slots
        if A._norm(s)[0] not in owned
        and line_of.get(A._norm(s)[0], A._norm(s)[0]) != y_line})

    options = {l: acquisition_options(l, areas, target_name, owned, line_of,
                                      members_of) for l in removable}
    rungs = A.distinct_rungs(slots, rates)

    candidates = []
    for r in range(len(removable) + 1):
        for subset in itertools.combinations(removable, r):
            gone = set(owned)
            for l in subset:
                gone |= _line_members(l, members_of)
            assignments, acq_cost = ((None, 0.0) if not subset
                                     else assign_sources(subset, options))
            if subset and assignments is None:
                continue
            for lead, pool in rungs:
                if pool.get(target_species, 0.0) <= 0:
                    continue
                p = A.conditional(pool, gone).get(target_species, 0.0)
                at_t = A.throughput(pool, gone)
                if at_t == INF:
                    continue
                acqs = [
                    {"line": l, "area": o[1], "kind": o[2], "lead": o[3],
                     "species": o[4], "p": o[5], "one_shot": o[6],
                     "cost": o[0],
                     "order": next(a["order"] for a in areas
                                   if a["name"] == o[1])}
                    for l, o in (assignments or [])]
                # The latest source is the earliest point in the game the
                # plan can be finished, so it is how long the target has to
                # wait. A proxy for progression until the sidecar has a real
                # order.
                latest = max(acqs, key=lambda x: x["order"], default=None)
                candidates.append({
                    "lines": list(subset),
                    "lead": lead,
                    "p": p,
                    "cost_at_target": at_t,
                    "cost_acquire": acq_cost,
                    "cost": at_t + acq_cost,
                    "acquisitions": acqs,
                    "latest_source": latest["area"] if latest else None,
                    "latest_order": latest["order"] if latest else None,
                    "pool_size": sum(1 for s in pool if s not in gone),
                })

    # Pareto: cheapest first, keep every point that raises P(Y)
    candidates.sort(key=lambda c: (c["cost"], -c["p"]))
    front, best_p = [], -1.0
    for c in candidates:
        if c["p"] > best_p + 1e-12:
            front.append(c)
            best_p = c["p"]

    baseline = max((c for c in candidates if not c["lines"]),
                   key=lambda c: c["p"], default=None)
    return {
        "target": target_name, "species": target_species, "kind": kind,
        "removable_lines": removable,
        "baseline": baseline,
        "front": front,
        "n_candidates": len(candidates),
    }


def describe(result, name, area_label, kind_label):
    """Each front point in plain language, the way the design doc renders it:

        Repel with a level-29 lead -> Growlithe at 3%.
        Pre-catch Doduo (route 205 north, lead 10, 40%, ~2.5 encounters) and
        Rhyhorn (...) -> Growlithe at 100%. About 35 encounters, versus 34
        unplanned.
    """
    y = name(result["species"])
    base = result["baseline"]
    out = []
    for c in result["front"]:
        parts = [f"Repel with a level {c['lead']} lead"]
        if c["acquisitions"]:
            steps = []
            for a in c["acquisitions"]:
                where = area_label(a["area"])
                if a["kind"] != "land":
                    where += f", {kind_label.get(a['kind'], a['kind']).lower()}"
                steps.append(
                    f"{name(a['species'])} ({where}, lead {a['lead']}, "
                    f"{a['p']*100:.0f}%, about {a['cost']:.1f} encounters)")
            parts.append("first catch " + "; then ".join(steps))
        head = ", ".join(parts)
        pool = (f"{c['pool_size']} species still count"
                if c["pool_size"] > 1 else "only it counts")
        line = (f"{head}: {y} at {c['p']*100:.0f}% ({pool}). "
                f"About {c['cost']:.0f} encounters in all")
        if base and c is not base and base["p"] > 0:
            line += f", versus {base['p']*100:.0f}% unplanned"
        if c["latest_source"]:
            line += (f". Needs {area_label(c['latest_source'])} first, "
                     f"so the catch waits until then")
        out.append(line + ".")
    return out


# -- the one impure function ----------------------------------------------


def plan_inputs(ref=None):
    """The live tables in play order, with the per-area encounter record and
    the evolution lines. Everything plan() needs, loaded once."""
    from . import dex, model
    root = model.repo_root()
    live = [a for a in model.load_all(ref) if a.land_active]
    # play order is the sidecar's `order` (authoring plan Step 1); an area
    # without one falls back to its encounter level, the old approximation
    entries = (model.load_sidecar() or {}).get("areas") or {}
    live.sort(key=lambda a: (entries.get(a.name, {}).get("order") is None,
                             entries.get(a.name, {}).get("order") or 0,
                             A.median(a.levels), min(a.levels), a.name))
    enc = model.load_encounters()
    areas = [{"name": a.name, "order": i, "used": a.name in enc,
              "tables": {k: a.kind_slots(k) for k in a.kinds_present()}}
             for i, a in enumerate(live)]
    line_of = dex.lines(root)
    members_of = {}
    for sp, l in line_of.items():
        members_of.setdefault(l, []).append(sp)
    return areas, line_of, members_of

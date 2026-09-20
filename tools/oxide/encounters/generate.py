"""The generator, levels-only form. Design doc section 8.2, step 3.

Given a table's species as already placed, choose the level of each slot so
that the repel ladder under them pays. This is the step the plan calls the
highest value per line of code in the pipeline, and the one that ships
alone: species placement stays Ian's.

The house rule R1 for authored tables -- levels non-decreasing with slot
index -- makes the search tiny. A non-decreasing sequence of twelve levels
drawn from four rungs is a choice of where the three steps fall, and there
are only C(15, 3) = 455 of them. So this does not hill-climb as the doc
sketched; it enumerates every ladder and picks the best exactly.

Best means, in order: every hard rule satisfied (R1 by construction; R2 rung
count; R6 no more than one singleton rung, top rung 2-4 species); then the
smallest shortfall below the aim on the rarest species' uplift (R3's
threshold by default, so any ladder at or above it ties at zero); then the
fewest slots changed from what is there now; then the widest top rung; and
only then the highest uplift. A high aim therefore pulls toward the best
reachable uplift; a low one changes as little as possible.

One consequence to know about: the search only ever yields ladders that obey
R1, and 88% of the tables on this branch do not, so on those the generator
always changes something, and a table whose illegal ladder happened to pay
well can come out paying less. Valley Windworks Outside goes from 20x to
16.7x for that reason. That is the house rule doing its job, not a defect;
the rule is Ian's to relax.

That order is deliberate. Maximising uplift outright, tried first, turned
every early table into the same thing -- the 1% species isolated with its
lightest companion at 50%, a 50x uplift on all sixteen -- which is the
homogenisation the whole design exists to prevent. Satisficing keeps a table
that already pays untouched and changes the rest as little as it can, so
route-to-route variety survives the generator. Ask for more with `aim`.

Locked slots keep their level; the sidecar's `locked` list is honoured.
Pure functions; the CLI does the reading and the writing.
"""
import itertools

from . import analysis as A


def ladders(n_slots, base, span, locked=None):
    """Every non-decreasing level assignment from base to base+span, with
    locked slots pinned to their given level."""
    locked = locked or {}
    levels = range(base, base + span + 1)
    for steps in itertools.combinations_with_replacement(levels, n_slots):
        # combinations_with_replacement yields sorted tuples: non-decreasing
        if all(steps[i] == lv for i, lv in locked.items()):
            yield steps


def score(species, levels, rates, rung_range, t):
    """(violations, uplift, metrics) for one ladder."""
    slots = list(zip(species, levels))
    m = A.table_metrics(slots, rates)
    lo, hi = rung_range
    violations = 0
    if not lo <= m["rung_count"] <= hi:
        violations += 1
    if m["singleton_rungs"] > t["r6_max_singleton_rungs"]:
        violations += 1
    top = m["pool_sizes"][-1] if m["pool_sizes"] else 0
    if not t["r6_top_rung_min"] <= top <= t["r6_top_rung_max"]:
        violations += 1
    return violations, m["uplift_on_rarest"], m


def best_ladder(species, current, rates, base, span, locked, rung_range, t,
                aim=None):
    """The best level assignment for these species, and why."""
    if aim is None:
        aim = t["r3_uplift_min"]
    best = None
    n_distinct = len(set(species))
    # a table with fewer species than rungs cannot hold the default range
    lo, hi = rung_range
    lo = min(lo, max(1, n_distinct))
    considered = 0
    for levels in ladders(len(species), base, span, locked):
        considered += 1
        violations, uplift, m = score(species, levels, rates, (lo, hi), t)
        changed = sum(1 for a, b in zip(levels, current) if a != b)
        top = m["pool_sizes"][-1] if m["pool_sizes"] else 0
        shortfall = round(max(0.0, aim - uplift), 6)
        key = (violations, shortfall, changed, -top, -uplift)
        if best is None or key < best[0]:
            best = (key, levels, m, changed)
    key, levels, m, changed = best
    return {
        "levels": list(levels),
        "violations": key[0],
        "uplift": -key[4],
        "aim": aim,
        "reached_aim": key[1] == 0,
        "changed": changed,
        "considered": considered,
        "rungs": m["rung_count"],
        "pool_sizes": m["pool_sizes"],
        "singleton_rungs": m["singleton_rungs"],
    }


def propose(area, entry, thresholds, span=3, base=None, aim=None):
    """One area's proposal: current levels, best levels, and the deltas."""
    slots = area.slots
    species = [s for s, _ in slots]
    current = [lv for _, lv in slots]
    _, _, rates = A.TABLE_KINDS["land"]
    entry = entry or {}
    if base is None:
        base = entry.get("base_level") or min(current)
    locked = {}
    for ref in entry.get("locked") or []:
        # "land_encounters[10]" pins that slot to its current level
        if ref.startswith("land_encounters[") and ref.endswith("]"):
            i = int(ref[len("land_encounters["):-1])
            locked[i] = current[i]
    rung_range = (thresholds["r2_rungs_min"], thresholds["r2_rungs_max"])
    before = A.table_metrics(slots, rates)
    out = best_ladder(species, current, rates, base, span, locked, rung_range,
                      thresholds, aim=aim)
    out.update({
        "area": area.name,
        "base": base,
        "span": span,
        "locked": sorted(locked),
        "current": current,
        "uplift_before": before["uplift_on_rarest"],
        "rungs_before": before["rung_count"],
        "deltas": [(i, current[i], out["levels"][i])
                   for i in range(len(current)) if current[i] != out["levels"][i]],
    })
    return out

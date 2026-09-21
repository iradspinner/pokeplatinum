"""Lay a table out from its sidecar entry. Authoring plan decision 4.

The sidecar entry says *what* a table is for: an archetype (the merged-share
shape), a base level, and a cast (the species, in the order they take the
signature's shares, each optionally pinned to a rung). This module turns
that into the twelve land slots the game format wants, deterministically,
so the JSON is never hand-edited and the archetype's shape holds by
construction. It chooses no species; that stays the author's decision.

Two rules produce the layout:

  * **Shares.** The archetype's signature gives each cast member a share in
    percent, first-listed first. Walk the twelve slot rates and hand each
    slot to a species whose remaining share covers it, so that every
    species' slots sum to exactly its share. A share larger than one slot's
    rate is filled with duplicates, which is where the tail re-weighting of
    design doc 2.2 comes from. Slots are walked in index order and the
    first-listed species take the common head, so the cast's first entry is
    the 20% face.

  * **Ladder.** Each slot's level is `base_level` plus the ladder's offset
    for that slot. The ladder is the sidecar entry's own `ladder` if it has
    one, else the default for the archetype's rung count. Offsets are
    non-decreasing by slot index, so R1 holds by construction.

A cast entry may pin a species to a rung: `{"species": X, "rung": 3}`. The
pinned species is guaranteed at least one slot on that rung: the walk
offers it that rung's slots first and backtracks any partial layout that
would leave it without one, while the rest of its share lays out as usual. That is
how a head species also gets a slot on the top rung (the "duplicate of a
head species up there with it" of the authoring rules) and how a real 1%
prize is placed on the rung a repel manip reaches.

Pure functions. The CLI does the reading and writing.
"""
from . import lint

LAND_RATES = (20, 20, 10, 10, 10, 10, 5, 5, 4, 4, 1, 1)

# Default ladders by rung count, as level offsets per slot. The four-rung one
# is vanilla's median (design doc 2.2); the shorter ones drop rungs from the
# top down so the common head stays at base level.
DEFAULT_LADDERS = {
    1: (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    2: (0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1),
    3: (0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2),
    4: (0, 1, 1, 1, 2, 2, 2, 2, 2, 2, 3, 3),
}


class LayoutError(ValueError):
    """The entry cannot be laid out as written; the message says why."""


def parse_cast(cast):
    """[(species, rung_or_None)] from the sidecar's cast list, whose entries
    are either a species string or {"species": ..., "rung": n}."""
    out = []
    for i, entry in enumerate(cast or []):
        if isinstance(entry, str):
            out.append((entry, None))
        elif isinstance(entry, dict) and "species" in entry:
            rung = entry.get("rung")
            if rung is not None and not isinstance(rung, int):
                raise LayoutError(f"cast[{i}]: rung must be an integer, got {rung!r}")
            out.append((entry["species"], rung))
        else:
            raise LayoutError(f"cast[{i}]: expected a species or "
                              f"{{\"species\": ..., \"rung\": n}}, got {entry!r}")
    return out


def ladder_for(archetype, explicit=None):
    """The per-slot level offsets, validated non-decreasing."""
    if explicit is not None:
        ladder = tuple(explicit)
        if len(ladder) != len(LAND_RATES):
            raise LayoutError(f"ladder has {len(ladder)} entries, wanted {len(LAND_RATES)}")
        if any(ladder[i] > ladder[i + 1] for i in range(len(ladder) - 1)):
            raise LayoutError(f"ladder is not non-decreasing by slot: {list(ladder)}")
        return ladder
    if archetype not in lint.ARCHETYPES:
        raise LayoutError(f"unknown archetype {archetype!r}; "
                          f"one of {', '.join(lint.ARCHETYPES)}")
    _, hi = lint.ARCHETYPES[archetype]["rungs"]
    return DEFAULT_LADDERS[hi]


def rung_index(ladder):
    """slot -> rung number (0 = base), from the ladder's distinct offsets."""
    levels = sorted(set(ladder))
    return [levels.index(off) for off in ladder]


def assign_slots(shares, rates=LAND_RATES, pins=None, rungs=None):
    """{slot: species_index} so each species' slot rates sum to its share.

    `shares` is the signature in cast order. `pins` maps species index to a
    rung; `rungs` maps slot to its rung. Pinned species get one slot on
    their rung first (the lowest-rate slot on that rung still free), then
    the remaining shares are walked slot by slot in cast order, backtracking
    when a partial assignment cannot complete. Deterministic.
    """
    pins = pins or {}
    rungs = rungs or [0] * len(rates)
    if sum(shares) != sum(rates):
        raise LayoutError(f"signature sums to {sum(shares)}, slots to {sum(rates)}")
    for k, rung in pins.items():
        if rung not in set(rungs):
            raise LayoutError(f"cast[{k}] pinned to rung {rung}, but the ladder "
                              f"has rungs 0-{max(rungs)}")
    remaining = list(shares)
    taken = {}
    n = len(rates)

    def satisfied(k):
        """Has pinned species k got a slot on its rung yet?"""
        return any(taken.get(i) == k and rungs[i] == pins[k] for i in range(n))

    def feasible(pos):
        # Every unfinished share must still fit some free slot, and every
        # unsatisfied pin must still have a free slot on its rung it can pay
        # for. Both prune early; the walk is exact regardless.
        left = [rates[i] for i in range(pos, n)]
        smallest = min(left) if left else 0
        if any(0 < r < smallest for r in remaining):
            return False
        for k, rung in pins.items():
            if satisfied(k):
                continue
            if not any(rungs[i] == rung and rates[i] <= remaining[k]
                       for i in range(pos, n)):
                return False
        return True

    def candidates(slot):
        # A pinned species that still needs this rung goes first, so the pin
        # is honoured at the earliest slot that can carry it; the rest follow
        # in cast order, which is what puts the first-listed face on slot 0.
        first = [k for k, rung in sorted(pins.items())
                 if rung == rungs[slot] and not satisfied(k)]
        return first + [k for k in range(len(shares)) if k not in first]

    def walk(pos):
        if pos == n:
            return all(r == 0 for r in remaining) and all(satisfied(k) for k in pins)
        for k in candidates(pos):
            if remaining[k] < rates[pos]:
                continue
            taken[pos] = k
            remaining[k] -= rates[pos]
            if feasible(pos + 1) and walk(pos + 1):
                return True
            remaining[k] += rates[pos]
            del taken[pos]
        return False

    if not walk(0):
        raise LayoutError(
            f"no slot assignment realises shares {list(shares)} with pins "
            f"{pins}: every share must be a sum of free slot rates, and a "
            f"pinned rung must have a slot left for each species that needs "
            f"one there. Tight signatures decompose only one way: an A5's "
            f"40 is the two 20% slots and its 1s are the two 1% slots, so its "
            f"head can never reach the top rung; A1's 10 and 5 leave room "
            f"(5+4+1 and 4+1), which is where a head duplicate on the top "
            f"rung comes from")
    return taken


def layout(entry, rates=LAND_RATES):
    """[(species, level)] for the twelve slots, from a sidecar entry.

    Needs `archetype`, `cast` and `base_level`; honours `ladder` when
    present. The cast must have exactly as many entries as the archetype's
    signature has shares, since R4 would flag anything else.
    """
    archetype = entry.get("archetype")
    cast = parse_cast(entry.get("cast"))
    base = entry.get("base_level")
    if archetype not in lint.ARCHETYPES:
        raise LayoutError(f"archetype {archetype!r} is not one of "
                          f"{', '.join(lint.ARCHETYPES)}")
    if not isinstance(base, int):
        raise LayoutError(f"base_level must be an integer, got {base!r}")
    signature = lint.ARCHETYPES[archetype]["signature"]
    if len(cast) != len(signature):
        raise LayoutError(f"{archetype} has {len(signature)} shares "
                          f"{list(signature)} but the cast lists {len(cast)} species")
    ladder = ladder_for(archetype, entry.get("ladder"))
    rungs = rung_index(ladder)
    pins = {k: rung for k, (_, rung) in enumerate(cast) if rung is not None}
    taken = assign_slots(signature, rates, pins, rungs)
    return [(cast[taken[i]][0], base + ladder[i]) for i in range(len(rates))]


def describe(slots, rates=LAND_RATES):
    """One line per species: its share and the rungs it sits on."""
    by = {}
    for i, (sp, lv) in enumerate(slots):
        d = by.setdefault(sp, {"share": 0, "levels": set()})
        d["share"] += rates[i]
        d["levels"].add(lv)
    return [f"{sp.replace('SPECIES_', '')} {d['share']}% at "
            f"lv {'/'.join(str(l) for l in sorted(d['levels']))}"
            for sp, d in sorted(by.items(), key=lambda kv: -kv[1]["share"])]


def water(kind, spec):
    """[(species, level_min, level_max)] for a surf or rod table from its
    sidecar spec: {"cast": [five species, slot order], "levels": [lo, hi]}
    with one range for every slot, or "levels" as five [lo, hi] pairs. The
    format fixes the slot rates (60/30/5/4/1 for surf and the Old Rod,
    40/40/15/4/1 for the Good and Super Rods), so the cast order is the
    layout: first listed is the 60% or first 40% slot, last is the 1%.
    """
    from . import analysis
    if kind not in analysis.TABLE_KINDS or kind == "land":
        raise LayoutError(f"{kind!r} is not a water kind")
    rates = analysis.TABLE_KINDS[kind][2]
    cast = spec.get("cast") if isinstance(spec, dict) else None
    if not isinstance(cast, list) or len(cast) != len(rates):
        raise LayoutError(f"cast must list {len(rates)} species, one per slot "
                          f"({'/'.join(str(r) for r in rates)})")
    if not all(isinstance(s, str) and s for s in cast):
        raise LayoutError("cast entries must be species constants")
    levels = spec.get("levels")
    if (isinstance(levels, list) and len(levels) == 2
            and all(isinstance(v, int) for v in levels)):
        ranges = [tuple(levels)] * len(rates)
    elif (isinstance(levels, list) and len(levels) == len(rates)
          and all(isinstance(p, list) and len(p) == 2 and all(isinstance(v, int) for v in p)
                  for p in levels)):
        ranges = [tuple(p) for p in levels]
    else:
        raise LayoutError("levels must be [lo, hi] or one [lo, hi] per slot")
    for lo, hi in ranges:
        if not 1 <= lo <= hi <= 100:
            raise LayoutError(f"level range {lo}-{hi} is not 1 <= lo <= hi <= 100")
    return [(sp, lo, hi) for sp, (lo, hi) in zip(cast, ranges)]


def describe_water(kind, rows):
    """One line: each species with its slot rate and level range."""
    from . import analysis
    rates = analysis.TABLE_KINDS[kind][2]
    return "; ".join(f"{sp.replace('SPECIES_', '')} {r}% lv {lo}-{hi}"
                     for (sp, lo, hi), r in zip(rows, rates))

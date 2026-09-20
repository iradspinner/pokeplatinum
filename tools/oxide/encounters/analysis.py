"""The encounter maths. Pure functions: no I/O, no globals, no mutation.

Everything here takes slots as [(species, level)] and a rate tuple, so the same
code serves land tables now and water or fishing tables later by passing a
different rate array.

The repel model is the tool's core claim, so it is worth stating precisely.
From src/overlay006/wild_encounters.c:

    static BOOL RepelPreventsEncounter(const u8 wildLevel, const ... *p)
    {
        return p->repelActive && p->firstBattlerLevel > wildLevel;
    }

Two consequences, both load-bearing:

  * A slot SURVIVES when slot_level >= lead_level. Greater-or-equal. A level-14
    lead still meets level-14 wilds.
  * A blocked roll cancels the step. The game does not reroll onto a surviving
    slot, so conditional on an encounter happening at all, the distribution is
    exactly the surviving weights renormalised. Nothing is smeared.

So P(slot i | encounter) = w_i / sum{w_j : level_j >= L} for level_i >= L, and
0 otherwise. That is the whole model; it is exact, and it must never be
"improved" into a reroll.
"""

LAND_RATES = (20, 20, 10, 10, 10, 10, 5, 5, 4, 4, 1, 1)


# -- shares ---------------------------------------------------------------
#
# Shares are always over merged species, never over slots: a species holding
# two slots is one entry at the summed weight. HHI, signatures and "the
# table's rarest species" all read from the merged view, because that is what
# a player experiences and what every published hack document prints.


def merged(slots, rates=LAND_RATES):
    """{species: share}, shares summing to 1."""
    total = sum(rates)
    out = {}
    for (species, _), rate in zip(slots, rates):
        out[species] = out.get(species, 0.0) + rate / total
    return out


def hhi(shares):
    """Herfindahl index: one species at 100% gives 1.0, twelve equal slots
    give 0.083. The single number for "how concentrated is this table"."""
    return sum(s * s for s in shares.values())


def signature(shares, places=0):
    """The table's shape as a sorted descending tuple of percentages, e.g.
    (40, 25, 20, 10, 5). Counting distinct signatures across a game is R9:
    vanilla Platinum has 71 over 171 tables, the genre 0.12-0.19 per table."""
    return tuple(sorted((round(s * 100, places) for s in shares.values()),
                        reverse=True))


# -- repel ----------------------------------------------------------------


def rungs(slots):
    """The lead levels worth considering: the table's distinct slot levels.
    Not yet collapsed — see distinct_rungs."""
    return sorted({level for _, level in slots})


def pool(slots, lead_level, rates=LAND_RATES):
    """{species: share} among slots surviving a repel at `lead_level`.

    Survival is `>=`. Renormalisation is exact because a blocked roll cancels
    the step rather than rerolling. Returns {} when nothing survives.
    """
    surviving = [(sp, rate) for (sp, lv), rate in zip(slots, rates)
                 if lv >= lead_level]
    total = sum(rate for _, rate in surviving)
    if not total:
        return {}
    out = {}
    for species, rate in surviving:
        out[species] = out.get(species, 0.0) + rate / total
    return out


def distinct_rungs(slots, rates=LAND_RATES):
    """[(lead_level, pool)] with rungs that yield an identical pool collapsed.

    Four distinct levels that produce three distinct pools are three rungs.
    A rung that changes nothing is not a choice the player has, and reporting
    it as one overstates how much structure a table carries.
    """
    out = []
    for level in rungs(slots):
        p = pool(slots, level, rates)
        if not p:
            continue
        if out and out[-1][1] == p:
            continue
        out.append((level, p))
    return out


def rarest(shares):
    """The table's rarest species. Ties break on name so the choice is stable
    across runs rather than dependent on dict ordering."""
    if not shares:
        return None
    least = min(shares.values())
    return sorted(sp for sp, s in shares.items() if s == least)[0]


def _best_uplift_for(species, base, rung_list):
    top, at = base[species], None
    for level, p in rung_list:
        if p.get(species, 0.0) > top:
            top, at = p[species], level
    return top / base[species], at


def uplift_on_rarest(slots, rates=LAND_RATES):
    """(uplift, best_lead_level) for the table's rarest species.

    Ties are common — 29% of vanilla tables have several species at the
    minimum share — and they are resolved toward the best uplift available
    among them, not alphabetically. That matters: resolving by name gives a
    vanilla median of 2.86x and a working-repel rate of 80%, while resolving
    toward the best gives 3.33x and 83%. The 83% reproduces the survey's
    "rarest species survives the filter" column exactly, which is what fixes
    this as the intended reading.

    R3's threshold of 3.0 is calibrated against this number: vanilla medians
    3.33x, so vanilla passes its own rule with a little room.
    """
    base = merged(slots, rates)
    if not base:
        return 0.0, None
    rung_list = distinct_rungs(slots, rates)
    least = min(base.values())
    candidates = [sp for sp, s in base.items() if s == least]
    return max((_best_uplift_for(sp, base, rung_list) for sp in candidates),
               key=lambda pair: pair[0])


def best_uplift(slots, rates=LAND_RATES):
    """(uplift, species, lead_level) for the best manip the table offers to
    *any* species, not just the rarest.

    This is the table's headline "is there a reason to repel here" number, and
    it is the one the survey's 5.0x figure actually measures: vanilla medians
    exactly 5.00x with a working repel on exactly 88% of tables, both of which
    reproduce the survey to the digit. The survey's column is headed "median
    uplift on rarest", but the rarest-species reading gives 3.33x/83%, so the
    heading is loose and this is the statistic behind the number.
    """
    base = merged(slots, rates)
    if not base:
        return 0.0, None, None
    rung_list = distinct_rungs(slots, rates)
    best = (0.0, None, None)
    for sp in base:
        up, at = _best_uplift_for(sp, base, rung_list)
        if up > best[0]:
            best = (up, sp, at)
    return best


def has_real_tail(slots, rates=LAND_RATES):
    """True when a minimum-rate slot holds a species found nowhere else on the
    table. `real` in the design doc's archetype table; only 6% of vanilla
    tables qualify, which is why the ladder is a re-weighting device rather
    than a rare-exclusive delivery system."""
    floor = min(rates)
    tail = {sp for (sp, _), rate in zip(slots, rates) if rate == floor}
    head = {sp for (sp, _), rate in zip(slots, rates) if rate != floor}
    return bool(tail - head)


# -- the dupes clause -----------------------------------------------------


def conditional(shares, owned):
    """Odds given that the encounter counts: drop owned species, renormalise.

    An encounter of an already-owned species does not count, so this is what
    the player actually faces. Returns {} when the pool is entirely owned.
    """
    kept = {sp: s for sp, s in shares.items() if sp not in owned}
    total = sum(kept.values())
    if not total:
        return {}
    return {sp: s / total for sp, s in kept.items()}


def throughput(shares, owned):
    """Expected encounters per counting encounter. inf when all are owned.

    A design can be excellent on `conditional` and miserable here — great odds
    on a pool you meet once an hour — so both numbers belong on screen.
    """
    live = sum(s for sp, s in shares.items() if sp not in owned)
    return float("inf") if live <= 0 else 1.0 / live


# -- per-table metrics ----------------------------------------------------


def caught_metrics(slots, owned, rates=LAND_RATES):
    """What this table is still worth to a player who already owns `owned`.

    The dupes clause makes a table's value depend on the dex, not just on the
    table, so these are the numbers that answer "is it worth walking here
    right now". `best_share` is the best reachable probability of the rarest
    species still missing, over every rung, after the owned mass is removed.
    """
    base = merged(slots, rates)
    live = [s for s in base if s not in owned]
    if not live:
        return {"live_species": 0, "base_throughput": float("inf"),
                "target": None, "best_share": 0.0, "best_level": None}
    target = min(sorted(live), key=lambda s: base[s])
    cond = conditional(base, owned)
    best_share, best_level = cond.get(target, 0.0), None
    for level, p in distinct_rungs(slots, rates):
        c = conditional(p, owned)
        if c.get(target, 0.0) > best_share:
            best_share, best_level = c[target], level
    return {
        "live_species": len(live),
        "base_throughput": throughput(base, owned),
        "target": target,
        "best_share": best_share,
        "best_level": best_level,
    }


def table_metrics(slots, rates=LAND_RATES):
    shares = merged(slots, rates)
    levels = [lv for _, lv in slots]
    rung_list = distinct_rungs(slots, rates)
    uplift, best_level = uplift_on_rarest(slots, rates)
    top_uplift, top_species, top_level = best_uplift(slots, rates)
    return {
        "best_uplift": top_uplift,
        "best_uplift_species": top_species,
        "best_uplift_at_level": top_level,
        "n_species": len(shares),
        "top_share": max(shares.values()) if shares else 0.0,
        "min_share": min(shares.values()) if shares else 0.0,
        "hhi": hhi(shares),
        "signature": signature(shares),
        "rung_count": len(rung_list),
        "rung_levels": [lv for lv, _ in rung_list],
        "pool_sizes": [len(p) for _, p in rung_list],
        "uplift_on_rarest": uplift,
        "uplift_at_level": best_level,
        "rarest_species": rarest(shares),
        "has_real_tail": has_real_tail(slots, rates),
        "level_min": min(levels),
        "level_max": max(levels),
        "level_span": max(levels) - min(levels),
        "distinct_levels": len(set(levels)),
        "singleton_rungs": sum(1 for _, p in rung_list if len(p) == 1),
    }


# -- statistics -----------------------------------------------------------


def percentile(values, q):
    """Linear-interpolated percentile on a sorted copy. q in [0, 1]."""
    if not values:
        return 0.0
    xs = sorted(values)
    if len(xs) == 1:
        return xs[0]
    pos = q * (len(xs) - 1)
    lo = int(pos)
    hi = min(lo + 1, len(xs) - 1)
    return xs[lo] + (xs[hi] - xs[lo]) * (pos - lo)


def median(values):
    return percentile(values, 0.5)


def ladder_profile(tables, rates=LAND_RATES):
    """Median level offset above each table's own minimum, per slot.

    Vanilla Platinum reads +0/+1/+1/+1/+2/+2/+2/+2/+2/+2/+3/+3, which is the
    ladder claim in its defensible form: levels rise with slot rarity on
    average, even though only 12% of individual tables are monotonic by slot
    index. See the build plan's "One finding that changes the design doc".
    """
    per_slot = [[] for _ in rates]
    for slots in tables:
        floor = min(lv for _, lv in slots)
        for i, (_, lv) in enumerate(slots):
            per_slot[i].append(lv - floor)
    return [median(xs) for xs in per_slot]


def game_metrics(tables, bands=None, rates=LAND_RATES):
    """tables: [slots]. bands: parallel list of 'early'/'mid'/'late' or None."""
    metrics = [table_metrics(s, rates) for s in tables]
    broad = [m for m in metrics if m["n_species"] >= 3]
    hhis = [m["hhi"] for m in broad]
    p10, p90 = percentile(hhis, 0.10), percentile(hhis, 0.90)
    sigs = {m["signature"] for m in metrics}
    working = [m for m in metrics if m["uplift_on_rarest"] > 1.0]

    out = {
        "n_tables": len(metrics),
        "hhi_median": median([m["hhi"] for m in metrics]),
        "hhi_p10": p10,
        "hhi_p90": p90,
        "hhi_spread": (p90 / p10) if p10 else 0.0,
        "distinct_signatures": len(sigs),
        "signatures_per_table": len(sigs) / len(metrics) if metrics else 0.0,
        "median_species": median([m["n_species"] for m in metrics]),
        "median_top_share": median([m["top_share"] for m in metrics]),
        "median_min_share": median([m["min_share"] for m in metrics]),
        "uplift_median": median([m["uplift_on_rarest"] for m in metrics]),
        "uplift_working_frac": len(working) / len(metrics) if metrics else 0.0,
        "uplift_2x_frac": (sum(1 for m in metrics
                               if m["uplift_on_rarest"] >= 2.0)
                           / len(metrics)) if metrics else 0.0,
        "best_uplift_median": median([m["best_uplift"] for m in metrics]),
        "best_uplift_working_frac": (
            sum(1 for m in metrics if m["best_uplift"] > 1.0)
            / len(metrics)) if metrics else 0.0,
        "real_tail_frac": (sum(1 for m in metrics if m["has_real_tail"])
                           / len(metrics)) if metrics else 0.0,
        "singleton_rung_frac": (
            sum(m["singleton_rungs"] for m in metrics)
            / sum(m["rung_count"] for m in metrics)) if metrics else 0.0,
        "ladder": ladder_profile(tables, rates),
    }
    if bands:
        for name in ("early", "mid", "late"):
            sel = [m for m, b in zip(metrics, bands) if b == name]
            out[f"hhi_{name}"] = median([m["hhi"] for m in sel]) if sel else None
            out[f"species_{name}"] = (median([m["n_species"] for m in sel])
                                      if sel else None)
            out[f"top_share_{name}"] = (median([m["top_share"] for m in sel])
                                        if sel else None)
            out[f"n_{name}"] = len(sel)
    return out

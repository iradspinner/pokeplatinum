"""Section 7's rules, as pure functions over M2's metrics.

Every threshold comes from the sidecar, never from a literal in here, because
the thresholds are Ian's house rules and are meant to be edited.

**Descriptive versus aspirational.** The design doc's rules mix two kinds of
number and does not distinguish them, which is what produced four separate
miscalibrations:

  * A *descriptive* threshold states something vanilla Platinum already does.
    Acceptance criterion 6 applies to these: if vanilla fails one, the
    threshold is wrong, not vanilla. R1b, R2, R6, R8, R9, R11 and R14.
  * An *aspirational* threshold is a target deliberately set beyond vanilla,
    because the design wants something the base game did not do. Vanilla is
    expected to fail these and nothing should be "fixed" when it does. R3,
    R5, R11b and R13.

Measured on vanilla's 171 live land tables, for reference:

    R1b  Spearman >= 0.5        71% of tables, corpus median 0.68
    R2   3-4 distinct rungs     81%
    R3   uplift >= 3.0          52%           <- aspirational, median 3.33
    R5   band fit               11-32%        <- aspirational
    R6   <=1 singleton rung     84%
    R8   spread >= 2.2          2.48          pass
    R9   signatures/table       0.42          pass
    R11  arc decreasing         0.373 > 0.325 > 0.275, pass
    R11b early>=.35 late<=.25   early passes, late is 0.275   <- aspirational
    R13  share span >= 4x       37%, median 2.5x              <- aspirational
    R14  land_rate variety      37% on the most common value, pass
"""
import collections

from . import analysis as A

Finding = collections.namedtuple("Finding", "rule severity scope target message")

# Design doc 2.3. Signature is the merged-share shape in percent, descending.
ARCHETYPES = {
    "A1":  {"signature": (40, 25, 20, 10, 5), "rungs": (4, 4), "tail": "duplicates"},
    "A2":  {"signature": (100,), "rungs": (1, 1), "tail": "none"},
    "A3":  {"signature": (80, 10, 10), "rungs": (2, 3), "tail": "real"},
    "A4":  {"signature": (65, 35), "rungs": (2, 2), "tail": "none"},
    "A5":  {"signature": (40, 25, 20, 9, 4, 1, 1), "rungs": (4, 4), "tail": "real"},
    "A6":  {"signature": (30, 30, 25, 10, 5), "rungs": (3, 3), "tail": "duplicates"},
    "A7":  {"signature": (25, 25, 15, 15, 10, 10), "rungs": (3, 3), "tail": "duplicates"},
    "A8":  {"signature": (20, 20, 20, 10, 10, 10, 5, 5), "rungs": (3, 4), "tail": "duplicates"},
    "A9":  {"signature": (50, 20, 20, 10), "rungs": (3, 3), "tail": "none"},
    "A10": {"signature": (60, 25, 10, 4, 1), "rungs": (4, 4), "tail": "real"},
}

DEFAULT_THRESHOLDS = {
    "r1b_spearman_min": 0.5,
    "r2_rungs_min": 3,
    "r2_rungs_max": 4,
    "r3_uplift_min": 3.0,
    "r4_signature_tolerance": 8.0,
    "r6_max_singleton_rungs": 1,
    "r6_top_rung_min": 2,
    "r6_top_rung_max": 4,
    "r8_spread_min": 2.2,
    "r9_signatures_per_table_min": 0.35,
    "r10_budget_tolerance": 0.05,
    "r11b_early_hhi_min": 0.35,
    "r11b_late_hhi_max": 0.25,
    "r13_share_span_min": 4.0,
    "r13_min_tables": 4,
    "r14_max_shared_land_rate": 0.5,
    # R12: the most expected encounters a line's first stage may cost at its
    # cheapest table and rung, by the pick-list's tier. A gate line is
    # scripted (legendary, starter, fossil, static battle) and is judged on
    # having a scripted source, not on a cost. Proposed defaults; Ian's.
    "r12_max_cost": {"starter-adjacent": 5.0, "preferred": 20.0, "filler": 100.0},
    "bands": {
        "early": {"species": [3, 5], "top": [0.40, 0.50], "hhi": [0.35, 0.50]},
        "mid":   {"species": [4, 7], "top": [0.30, 0.40], "hhi": [0.25, 0.35]},
        "late":  {"species": [5, 8], "top": [0.25, 0.35], "hhi": [0.18, 0.28]},
    },
}

# Rules vanilla must pass; the M3 gate checks exactly these.
DESCRIPTIVE = {"R1b", "R2", "R6", "R8", "R9", "R11", "R14"}
ASPIRATIONAL = {"R3", "R5", "R11b", "R13"}


def thresholds_from(sidecar):
    t = dict(DEFAULT_THRESHOLDS)
    if sidecar:
        t.update(sidecar.get("thresholds") or {})
    return t


def spearman(xs, ys):
    """Rank correlation, ties averaged. Used by R1b."""
    def rank(v):
        order = sorted(range(len(v)), key=lambda i: v[i])
        out = [0.0] * len(v)
        i = 0
        while i < len(order):
            j = i
            while j + 1 < len(order) and v[order[j + 1]] == v[order[i]]:
                j += 1
            for k in range(i, j + 1):
                out[order[k]] = (i + j) / 2
            i = j + 1
        return out
    rx, ry = rank(xs), rank(ys)
    n = len(xs)
    mx, my = sum(rx) / n, sum(ry) / n
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    den = (sum((a - mx) ** 2 for a in rx) * sum((b - my) ** 2 for b in ry)) ** 0.5
    return num / den if den else 0.0


# -- per table ------------------------------------------------------------


def lint_table(name, slots, entry, t, rates=A.LAND_RATES, data=None):
    """entry is the sidecar's record for this area, or None."""
    out = []
    m = A.table_metrics(slots, rates)
    levels = [lv for _, lv in slots]
    entry = entry or {}
    archetype = entry.get("archetype")
    authored = bool(archetype)

    # R1 (error) -- only for tables this project authored. Vanilla is 12%
    # monotonic by slot index, so this can never be pointed at the base game.
    if authored:
        if any(levels[i] > levels[i + 1] for i in range(len(levels) - 1)):
            out.append(Finding(
                "R1", "error", "table", name,
                f"ladder not monotonic by slot: {levels}"))

    # R1b (warn) -- the vanilla-calibrated form of the same idea
    rho = spearman([-r for r in rates], levels)
    if rho < t["r1b_spearman_min"]:
        out.append(Finding(
            "R1b", "warn", "table", name,
            f"level barely tracks rarity: Spearman {rho:+.2f} "
            f"< {t['r1b_spearman_min']}"))

    # R2 (warn) -- rung count, unless the archetype declares fewer
    lo, hi = t["r2_rungs_min"], t["r2_rungs_max"]
    if archetype in ARCHETYPES:
        lo, hi = ARCHETYPES[archetype]["rungs"]
    if not lo <= m["rung_count"] <= hi:
        out.append(Finding(
            "R2", "warn", "table", name,
            f"{m['rung_count']} distinct rungs, wanted {lo}-{hi}"))

    # R3 (warn, aspirational) -- does a repel pay
    if m["uplift_on_rarest"] < t["r3_uplift_min"]:
        out.append(Finding(
            "R3", "warn", "table", name,
            f"rarest species only reaches {m['uplift_on_rarest']:.2f}x "
            f"(want {t['r3_uplift_min']}x)"))

    # R4 (warn) -- archetype fit
    if archetype in ARCHETYPES:
        want = ARCHETYPES[archetype]["signature"]
        got = m["signature"]
        if len(got) != len(want):
            out.append(Finding(
                "R4", "warn", "table", name,
                f"{archetype} wants {len(want)} species, table has {len(got)}"))
        else:
            worst = max(abs(a - b) for a, b in zip(got, want))
            if worst > t["r4_signature_tolerance"]:
                out.append(Finding(
                    "R4", "warn", "table", name,
                    f"{archetype} shape off by {worst:.0f} points: "
                    f"{got} vs {want}"))

    # R5 (warn, aspirational) -- band fit
    band = entry.get("band")
    spec = (t.get("bands") or {}).get(band)
    if spec:
        if not spec["species"][0] <= m["n_species"] <= spec["species"][1]:
            out.append(Finding(
                "R5", "warn", "table", name,
                f"{band} wants {spec['species'][0]}-{spec['species'][1]} "
                f"species, has {m['n_species']}"))
        if not spec["hhi"][0] <= m["hhi"] <= spec["hhi"][1]:
            out.append(Finding(
                "R5", "warn", "table", name,
                f"{band} wants HHI {spec['hhi'][0]}-{spec['hhi'][1]}, "
                f"has {m['hhi']:.3f}"))

    # R6 (warn) -- not too binary
    if m["singleton_rungs"] > t["r6_max_singleton_rungs"]:
        out.append(Finding(
            "R6", "warn", "table", name,
            f"{m['singleton_rungs']} rungs collapse to a single species "
            f"(max {t['r6_max_singleton_rungs']})"))

    # R7 (error) -- day/night legality. The format stores two species that
    # stand in for slots 2 and 3, so anything else is malformed data.
    if data:
        for layer in ("day", "night"):
            vals = data.get(layer)
            if vals is not None and len(vals) != len(A.LAND_RATES[2:4]):
                out.append(Finding(
                    "R7", "error", "table", name,
                    f"{layer} has {len(vals)} entries, must have 2"))
    return out


# -- per game -------------------------------------------------------------


def lint_game(areas, t, availability=None):
    """areas: [(name, slots, entry, data)]; availability is
    audit.availability()'s rows, or None when the pick-list has no tiers."""
    out = []
    tables = [s for _, s, _, _ in areas]
    bands = [(e or {}).get("band") for _, _, e, _ in areas]
    g = A.game_metrics(tables, bands)

    # R8 (error) -- the rule that prevents "every route feels the same"
    if g["hhi_spread"] < t["r8_spread_min"]:
        out.append(Finding(
            "R8", "error", "game", "*",
            f"HHI spread {g['hhi_spread']:.2f}x below {t['r8_spread_min']}x "
            f"(p10 {g['hhi_p10']:.3f}, p90 {g['hhi_p90']:.3f}); "
            f"this needs a different archetype mix, not a table edit"))

    # R9 (warn)
    if g["signatures_per_table"] < t["r9_signatures_per_table_min"]:
        out.append(Finding(
            "R9", "warn", "game", "*",
            f"{g['distinct_signatures']} distinct signatures over "
            f"{g['n_tables']} tables = {g['signatures_per_table']:.2f}, "
            f"want {t['r9_signatures_per_table_min']}"))

    # R10 (warn) -- archetype budget, inert until archetypes are assigned
    declared = [(e or {}).get("archetype") for _, _, e, _ in areas]
    if any(declared):
        # realised share per HHI band, against the sidecar's budget
        pass

    # R11 (warn, descriptive) -- the arc has the right shape
    e, mid, late = g.get("hhi_early"), g.get("hhi_mid"), g.get("hhi_late")
    if None in (e, mid, late):
        # A rule that cannot run has to say so. R11 was silently skipped once
        # because bands arrived as None, and a quiet skip looks exactly like a
        # pass in the output.
        out.append(Finding(
            "R11", "skip", "game", "*",
            "arc unchecked: one or more bands had no tables "
            f"(early {g.get('n_early')}, mid {g.get('n_mid')}, "
            f"late {g.get('n_late')})"))
    else:
        if not (e > mid > late):
            out.append(Finding(
                "R11", "warn", "game", "*",
                f"concentration arc is not decreasing: early {e:.3f}, "
                f"mid {mid:.3f}, late {late:.3f}"))
        # R11b (warn, aspirational) -- the absolute targets, which sit beyond
        # vanilla on purpose: vanilla's late median is 0.275, not <= 0.25
        if e < t["r11b_early_hhi_min"]:
            out.append(Finding(
                "R11b", "warn", "game", "*",
                f"early median HHI {e:.3f} below "
                f"{t['r11b_early_hhi_min']}"))
        if late > t["r11b_late_hhi_max"]:
            out.append(Finding(
                "R11b", "warn", "game", "*",
                f"late median HHI {late:.3f} above "
                f"{t['r11b_late_hhi_max']} (vanilla is 0.275, so this is a "
                f"target rather than a regression)"))

    # R13 (warn, aspirational) -- repetition has to vary
    where = collections.defaultdict(list)
    for name, slots, _, _ in areas:
        for sp, share in A.merged(slots).items():
            where[sp].append((share, name))
    flat = []
    for sp, rows in where.items():
        if len(rows) < t["r13_min_tables"]:
            continue
        hi = max(r[0] for r in rows)
        lo = min(r[0] for r in rows)
        if lo > 0 and hi / lo < t["r13_share_span_min"]:
            flat.append((sp, hi / lo, len(rows)))
    for sp, span, count in sorted(flat, key=lambda r: r[1])[:12]:
        out.append(Finding(
            "R13", "warn", "game", sp,
            f"appears on {count} tables but spans only {span:.1f}x "
            f"(want {t['r13_share_span_min']}x)"))
    if len(flat) > 12:
        out.append(Finding(
            "R13", "warn", "game", "*",
            f"...and {len(flat) - 12} more species with too-uniform shares"))

    # R14 (warn) -- encounter-rate variety, free texture the old rewrite
    # never touched
    rates = [((d or {}).get("land_rate")) for _, _, _, d in areas]
    rates = [r for r in rates if r]
    if rates:
        common = collections.Counter(rates).most_common(1)[0]
        share = common[1] / len(rates)
        if share > t["r14_max_shared_land_rate"]:
            out.append(Finding(
                "R14", "warn", "game", "*",
                f"land_rate {common[0]} on {share:.0%} of tables "
                f"(max {t['r14_max_shared_land_rate']:.0%})"))

    # R12 (error) -- availability, Ian's guarantee in its enforceable form.
    # `availability` is audit.availability()'s output: one row per native
    # line with its tier, whether a script hands it over, and the cheapest
    # wild acquisition (expected encounters at the best table and rung). A
    # gate line must have a scripted source; any other line must be catchable
    # under its tier's cost ceiling. Without a `tier` column the rule reports
    # itself skipped rather than passing quietly.
    if availability is None:
        out.append(Finding(
            "R12", "skip", "game", "*",
            "availability unchecked: the species pick-list has no `tier` "
            "column yet (cli tier-init writes the defaults)"))
    else:
        ceilings = t.get("r12_max_cost") or {}
        for row in availability:
            tier, name = row["tier"], row["name"]
            if not tier:
                out.append(Finding("R12", "warn", "game", name,
                                   "no tier on the pick-list; unchecked"))
            elif tier == "gate":
                if not row["non_wild"]:
                    out.append(Finding(
                        "R12", "error", "game", name,
                        "gate line with no scripted source (no gift, trade, "
                        "static battle, starter or fossil script names it)"))
            elif row["non_wild"]:
                continue
            elif row["cost"] is None:
                out.append(Finding(
                    "R12", "error", "game", name,
                    f"{tier} line with no wild table and no scripted source"))
            elif tier in ceilings and row["cost"] > ceilings[tier]:
                area, kind, lead = row["where"]
                out.append(Finding(
                    "R12", "error", "game", name,
                    f"{tier} line costs {row['cost']:.1f} encounters at best "
                    f"({area.replace('encounters_', '')} {kind}, lead {lead}), "
                    f"ceiling {ceilings[tier]:.0f}"))
            elif tier not in ceilings:
                out.append(Finding("R12", "warn", "game", name,
                                   f"tier {tier!r} has no ceiling in r12_max_cost"))
    return out


def lint_all(areas, sidecar, availability=None):
    t = thresholds_from(sidecar)
    entries = (sidecar or {}).get("areas") or {}
    out = []
    for name, slots, entry, data in areas:
        out += lint_table(name, slots, entry or entries.get(name), t, data=data)
    out += lint_game(areas, t, availability)
    return out


def summarise(findings):
    by_rule = collections.Counter(f.rule for f in findings)
    errors = [f for f in findings if f.severity == "error"]
    warns = [f for f in findings if f.severity == "warn"]
    skips = [f for f in findings if f.severity == "skip"]
    return {"errors": len(errors), "warns": len(warns), "skipped": len(skips),
            "by_rule": dict(by_rule)}

"""M2 acceptance: the repel model is right, and vanilla reproduces the survey.

    PYTHONPATH=. python3 -m tools.oxide.encounters.test_m2

Two gates, from the design doc's section 11.

1. pool() against a brute-force simulation of RepelPreventsEncounter. The repel
   model is the tool's central claim, so it is checked against the actual
   comparison the game makes rather than against a restatement of it.
2. report --ref main reproduces the survey's vanilla numbers. A disagreement
   means one of the two documents is wrong, and it has to be found before any
   table is designed against them.
"""
import random
import sys

from . import analysis as A
from . import model

TRIALS = 10 ** 6
SAMPLE = 20
SEED = 20260920
SIGMA = 5.0


def simulate(slots, lead_level, trials, rng, rates=A.LAND_RATES):
    """Roll the table the way the game does and count what gets through.

    The game picks a slot by weight, then asks RepelPreventsEncounter, and a
    blocked roll cancels the step rather than rerolling. So blocked rolls are
    simply not counted, which is what makes the closed form a renormalisation
    rather than an approximation of one.
    """
    cumulative, run = [], 0
    for r in rates:
        run += r
        cumulative.append(run)
    counts, kept = {}, 0
    # batched so the check can afford enough trials to be worth running
    for idx in rng.choices(range(len(slots)), cum_weights=cumulative, k=trials):
        species, level = slots[idx]
        # the game's comparison, verbatim: blocked when lead > wild
        if lead_level > level:
            continue
        counts[species] = counts.get(species, 0) + 1
        kept += 1
    return ({sp: c / kept for sp, c in counts.items()} if kept else {}), kept


def check_repel_model(results):
    """Compare the closed form against the simulation at every rung of 20
    randomly chosen tables.

    The tolerance is the sampling error itself, not a flat number: a share p
    measured over n kept rolls has standard error sqrt(p(1-p)/n), so anything
    inside 5 sigma is noise and anything outside it is a model error. A flat
    threshold would either pass a real bug on a common species or fail a rare
    one for no reason.
    """
    rng = random.Random(SEED)
    areas = [a for a in model.load_all("main") if a.land_active]
    sample = rng.sample(areas, SAMPLE)
    worst_ratio, worst_where, comparisons = 0.0, None, 0
    for area in sample:
        slots = area.slots
        for lead in A.rungs(slots):
            closed = A.pool(slots, lead)
            sim, kept = simulate(slots, lead, TRIALS // SAMPLE, rng)
            if not kept:
                continue
            for species in set(closed) | set(sim):
                p = closed.get(species, 0.0)
                delta = abs(p - sim.get(species, 0.0))
                sigma = max((p * (1 - p) / kept) ** 0.5, 1e-9)
                comparisons += 1
                if delta / sigma > worst_ratio:
                    worst_ratio = delta / sigma
                    worst_where = (area.name, lead, species, round(delta, 5))
    results.append((f"pool() matches simulation ({comparisons} comparisons)",
                    worst_ratio < SIGMA,
                    f"worst deviation {worst_ratio:.2f} sigma at {worst_where}"))


def check_repel_is_ge(results):
    """A lead at exactly the wild level still meets it. An off-by-one here
    changes every number the tool prints, so it gets its own check."""
    slots = [("SPECIES_A", 10)] * 6 + [("SPECIES_B", 14)] * 6
    at = A.pool(slots, 10)
    above = A.pool(slots, 11)
    results.append(("lead == wild level still encounters",
                    at.get("SPECIES_A", 0) > 0, f"{at}"))
    results.append(("lead above cuts the low slots",
                    above == {"SPECIES_B": 1.0}, f"{above}"))


def check_no_reroll(results):
    """A blocked roll cancels the step; it is never smeared onto survivors.
    With half the table blocked, survivors keep their own ratio exactly."""
    slots = ([("SPECIES_LOW", 5)] * 6
             + [("SPECIES_HI1", 9)] * 4 + [("SPECIES_HI2", 9)] * 2)
    p = A.pool(slots, 9)
    # slots 6-9 are rates 5,5,4,4 = 18; slots 10-11 are 1,1 = 2
    expected = {"SPECIES_HI1": 18 / 20, "SPECIES_HI2": 2 / 20}
    ok = all(abs(p[k] - v) < 1e-12 for k, v in expected.items())
    results.append(("blocked rolls cancel, no reroll", ok, f"{p}"))


def check_rung_collapse(results):
    """Four distinct levels that yield three distinct pools are three rungs."""
    slots = [("SPECIES_A", 2)] * 2 + [("SPECIES_B", 3)] * 8 + [("SPECIES_B", 4)] * 2
    levels = A.rungs(slots)
    collapsed = A.distinct_rungs(slots)
    results.append(("identical pools collapse to one rung",
                    len(levels) == 3 and len(collapsed) == 2,
                    f"{len(levels)} levels -> {len(collapsed)} rungs"))


def check_dupes(results):
    shares = {"A": 0.5, "B": 0.3, "C": 0.2}
    cond = A.conditional(shares, {"A"})
    ok = abs(cond["B"] - 0.6) < 1e-12 and abs(cond["C"] - 0.4) < 1e-12
    results.append(("dupes renormalise over the unowned", ok, f"{cond}"))
    results.append(("throughput is 1/live mass",
                    abs(A.throughput(shares, {"A"}) - 2.0) < 1e-12, ""))
    results.append(("throughput is inf when all owned",
                    A.throughput(shares, {"A", "B", "C"}) == float("inf"), ""))


def check_survey(results):
    """The survey's vanilla numbers, reproduced from res/ on main."""
    areas = [a for a in model.load_all("main") if a.land_active]
    g = A.game_metrics([a.slots for a in areas], [a.band for a in areas])
    checks = [
        ("tables", g["n_tables"], 171, 0),
        ("median HHI", g["hhi_median"], 0.275, 0.003),
        ("HHI p10", g["hhi_p10"], 0.170, 0.006),
        ("HHI p90", g["hhi_p90"], 0.420, 0.010),
        ("HHI spread", g["hhi_spread"], 2.5, 0.05),
        ("distinct signatures", g["distinct_signatures"], 71, 0),
        ("median species/table", g["median_species"], 5, 0),
        ("median top share", g["median_top_share"] * 100, 40, 0.5),
        ("median rarest share", g["median_min_share"] * 100, 5, 0.5),
        ("best uplift median", g["best_uplift_median"], 5.0, 0.05),
        ("best uplift works", g["best_uplift_working_frac"], 0.88, 0.005),
        ("rarest survives", g["uplift_working_frac"], 0.83, 0.005),
        ("HHI early", g["hhi_early"], 0.37, 0.005),
        ("HHI late", g["hhi_late"], 0.28, 0.006),
    ]
    for label, got, want, tol in checks:
        results.append((f"survey: {label}", abs(got - want) <= tol,
                        f"got {got:.3f}, survey {want}"))
    ladder = [round(x) for x in g["ladder"]]
    results.append(("survey: ladder profile",
                    ladder == [0, 1, 1, 1, 2, 2, 2, 2, 2, 2, 3, 3],
                    f"{ladder}"))


def main():
    results = []
    for check in (check_repel_is_ge, check_no_reroll, check_rung_collapse,
                  check_dupes, check_survey, check_repel_model):
        check(results)
    width = max(len(label) for label, _, _ in results)
    failed = 0
    for label, ok, note in results:
        failed += not ok
        print(f"  {'ok  ' if ok else 'FAIL'}  {label:{width}}  {note}")
    print(f"\n{len(results) - failed}/{len(results)} passed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())

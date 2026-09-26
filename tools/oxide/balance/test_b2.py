"""B2 acceptance: the structural metrics.

    PYTHONPATH=. python3 -m tools.oxide.balance.test_b2

Reads the same sources as test_b1 and writes nothing. The plan's check is
that vanilla, Renegade and Kaizo come out in that order on almost every
metric; this file pins which metrics do and which do not, so a change to
either list is seen (docs/oxide/balance-plan.md, "What B2 found").
"""
import sys

from . import data
from . import metrics as M

# The ordered metrics on which vanilla, Renegade and Kaizo do not come out in
# that order, as found on 2026-09-23. IVs sit at the ceiling in both hacks,
# Kaizo picks natures less often than Renegade, and Kaizo's bosses carry
# fewer priority, speed control and recovery moves than Renegade's.
NOT_IN_ORDER = {"mean_iv", "nature_fit", "priority", "speed_control", "recovery"}
# Moves no table knows: an Unbound custom move.
UNKNOWN_MOVES = {"unbound": {"Leech Fang"}}
# Filler that B1d's map split puts in a split whose cap it is above.
# Filler above its split's cap: 18 early-split revisits, and Volkner and
# Flint's tag at the Fight Area (74 to 75), which sits in the Galactic split
# (cap 65) until the main track gates it behind the Beacon Badge. The rest of
# the Battle Zone counted here too (73 in all) until it came down 18 levels
# on 2026-09-25.
LATE_VISITS = 20


def check_coverage(results):
    """Every story fight has metrics in Oxide and every Platinum-based hack,
    and every milestone hack has its 13 gym and League seats."""
    rows, unresolved = M.all_metrics()
    n = len(data.fights()["fights"])
    short = {h: len(rows[h]) for h in M.PLATINUM if len(rows[h]) != n}
    short.update({h: len(rows[h]) for h in data.fights()["milestones"]
                  if not h.startswith("_") and len(rows[h]) != 13})
    results.append(("every fight is scored in every hack", not short, str(short) if short else
                    f"{n} fights in {len(M.PLATINUM)} Platinum-based hacks, 13 seats in 4 others"))
    species = {h: sorted(u["species"]) for h, u in unresolved.items() if u["species"]}
    moves = {h: u["moves"] for h, u in unresolved.items() if u["moves"]}
    results.append(("every species and move resolves, bar one Unbound move",
                    not species and moves == UNKNOWN_MOVES, f"species {species}, moves {moves}"))


def check_order(results):
    """The plan's check, as far as it holds: vanilla, Renegade and Kaizo in
    order on the nine metrics that measure strength, and out of order on
    the five that NOT_IN_ORDER names."""
    _keys, table = M.order_table()
    out = {metric for metric, means, _share in table if means is None or not M.in_order(means)}
    held = len(table) - len(out)
    results.append(("vanilla, Renegade, Kaizo in order on all but the known five",
                    out == NOT_IN_ORDER, f"{held} of {len(table)} in order; out: {sorted(out)}"))


def check_natures(results):
    """Nature fit reads rolled natures as chance and picked ones as picked:
    vanilla, whose trainers roll, lands near 8 in 25; Renegade, which picks,
    well above it. And the rule itself, on four cases."""
    rows, _ = M.all_metrics()
    mean = lambda h: sum(r["nature_fit"] for r in rows[h].values()) / len(rows[h])
    cases = [M.nature_fits("Adamant", "at", 80), not M.nature_fits("Modest", "at", 80),
             M.nature_fits("Brave", "at", 40), not M.nature_fits("Brave", "at", 100),
             not M.nature_fits("Hardy", "sa", 80), M.nature_fits("Bold", "sa", 80)]
    ok = 0.25 <= mean("vanilla") <= 0.40 and mean("renegade") >= 0.6 and all(cases)
    results.append(("nature fit: vanilla at chance, Renegade picked, rule cases",
                    ok, f"vanilla {mean('vanilla'):.2f}, renegade {mean('renegade'):.2f}"))


def check_renegade_roark(results):
    """Renegade's Roark, counted by hand from its six sets: three Stealth
    Rocks; nine speed control moves (Thunder Wave, then Rock Tomb, Bulldoze
    and Scary Face); every Pokemon holds an item and none is fully evolved;
    and its moves hit 15 of the 17 types super effectively (not Ground or
    Dragon)."""
    rows, _ = M.all_metrics()
    r = rows["renegade"]["roark"]
    got = (r["party_size"], r["hazards"], r["speed_control"], r["item_share"],
           r["evolved_share"], r["coverage"])
    results.append(("Renegade's Roark matches the hand count", got == (6, 3, 9, 1.0, 0.0, 15),
                    str(got)))


def check_evolution(results):
    """Fully evolved is read per game: Girafarig is final in Generation 4,
    Kirlia is not, and a Mega is."""
    mon = lambda sp, **kw: dict({"species": sp, "mega": None}, **kw)
    ok = (M.is_evolved("vanilla", mon("Girafarig")) and not M.is_evolved("vanilla", mon("Kirlia"))
          and not M.is_evolved("oxide", mon("Kirlia"))
          and M.is_evolved("run_and_bun", mon("Latios-Mega"))
          and M.is_evolved("null", mon("Aerodactyl", mega="Aerodactyl-Mega")))
    results.append(("fully evolved reads each game's own evolutions", ok, ""))


def check_filler(results):
    """The filler numbers leave out the later visits B1d misplaces, and a
    reference keeps a filler id only when it holds vanilla's trainer:
    Renegade drops one, Redux about a fifth."""
    late = M.late_visits()
    drops = {h: M.filler_summary(h)[1] for h in ("renegade", "redux")}
    counts = sum(len(v) for v in M.filler_ids().values())
    ok = len(late) == LATE_VISITS and drops["renegade"] <= 1 and drops["redux"] < counts / 4
    results.append(("filler: later visits left out, reused ids dropped", ok,
                    f"{counts} filler, {len(late)} later visits, dropped {drops}"))


def main():
    results = []
    for check in (check_coverage, check_order, check_natures, check_renegade_roark,
                  check_evolution, check_filler):
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

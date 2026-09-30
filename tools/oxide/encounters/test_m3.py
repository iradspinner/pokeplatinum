"""M3 acceptance: vanilla passes the rules that were derived from vanilla.

    PYTHONPATH=. python3 -m tools.oxide.encounters.test_m3

Design doc acceptance criterion 6: "lint on vanilla Platinum passes R1, R8, R9
and R11 -- because vanilla *is* the target for those four. If vanilla fails a
rule, the rule's threshold is wrong."

That is the right idea with the wrong list. R1 cannot be checked against
vanilla at all (12% of tables are monotonic by slot index), so R1b replaces it
here. The list is otherwise extended to every rule tagged DESCRIPTIVE, since
the same reasoning applies to all of them.

Rules tagged ASPIRATIONAL are deliberately set beyond vanilla and are asserted
to *fail* on it, so that nobody later "fixes" a threshold that is doing its
job, and so a silent re-tagging shows up as a test failure.
"""
import sys

from . import analysis as A
from . import lint
from . import model


def _corpus(ref="main"):
    areas = [a for a in model.load_all(ref) if a.land_active]
    sidecar = model.load_sidecar()
    entries = (sidecar or {}).get("areas") or {}
    # The one-spot groups are Oxide's design too (R15), so a reference tree is
    # linted without them, as it is without its archetypes.
    if ref is not None:
        sidecar = {k: v for k, v in sidecar.items() if k != "groups"}
    # Vanilla was never laid out from the sidecar, so its archetype must not
    # mark a table as authored (R1 and R4 would judge vanilla's slots against
    # Oxide's design); `cli lint --ref` drops it the same way.
    payload = []
    for a in areas:
        e = dict(entries.get(a.name) or {"band": a.band})
        if ref is not None:
            e.pop("archetype", None)
        payload.append((a.name, a.slots, e, a.data))
    return areas, payload, sidecar


def check_no_errors(results):
    """Nothing in vanilla may trip an error-severity rule."""
    _, payload, sidecar = _corpus()
    findings = lint.lint_all(payload, sidecar)
    errors = [f for f in findings if f.severity == "error"]
    results.append(("vanilla trips no errors", not errors,
                    "clean" if not errors
                    else f"{len(errors)}: {errors[0].rule} {errors[0].message}"))


def check_descriptive_game_rules(results):
    """The four game-wide descriptive rules must be silent on vanilla. These
    are the ones that carry the design, and they cannot be satisfied by
    editing a single table."""
    _, payload, sidecar = _corpus()
    findings = lint.lint_all(payload, sidecar)
    for rule in ("R8", "R9", "R14"):
        hits = [f for f in findings if f.rule == rule]
        results.append((f"vanilla passes {rule}", not hits,
                        "silent" if not hits else hits[0].message))
    # R11 became Ian's cap on 2026-09-21 (no band's median top share over
    # about a third), a house rule vanilla was never built for: its early
    # routes run a 45-48% face. So vanilla must trip it, as a warning.
    hits = [f for f in findings if f.rule == "R11" and f.severity == "warn"]
    results.append(("vanilla trips R11, the cap, on its early band",
                    any("early" in f.message for f in hits),
                    hits[0].message if hits else "silent"))


def check_r11_actually_ran(results):
    """R11 was silently skipped once because bands arrived as None, and a
    quiet skip is indistinguishable from a pass. Assert it ran."""
    _, payload, sidecar = _corpus()
    findings = lint.lint_all(payload, sidecar)
    skipped = [f for f in findings if f.rule == "R11" and f.severity == "skip"]
    results.append(("R11 evaluated rather than skipped", not skipped,
                    "" if not skipped else skipped[0].message))


def check_r1b_corpus(results):
    """R1b is a per-table warning, so a minority of vanilla tables trip it by
    design. What must hold is the corpus statistic the threshold came from."""
    areas, _, _ = _corpus()
    rhos = [lint.spearman([-r for r in A.LAND_RATES], [lv for _, lv in a.slots])
            for a in areas]
    med = A.median(rhos)
    results.append(("R1b corpus median Spearman >= 0.5", med >= 0.5,
                    f"{med:.2f}"))


def check_descriptive_table_rules(results):
    """Per-table descriptive rules should warn on a minority only. If one of
    these ever warns on most of vanilla, its threshold has drifted off the
    thing it was derived from."""
    areas, payload, sidecar = _corpus()
    findings = lint.lint_all(payload, sidecar)
    n = len(areas)
    for rule, ceiling in (("R1b", 0.40), ("R2", 0.30), ("R6", 0.30)):
        hit = len({f.target for f in findings if f.rule == rule})
        results.append((f"{rule} warns on a minority of vanilla",
                        hit / n <= ceiling,
                        f"{hit}/{n} = {hit/n:.0%} (ceiling {ceiling:.0%})"))


def check_aspirational_fail(results):
    """The aspirational rules must fail on vanilla; that is what makes them
    aspirational. R3, R5 and R13 warn per-table or per-species; R11b trips on
    vanilla's late-band median of 0.275 against a 0.25 target."""
    _, payload, sidecar = _corpus()
    findings = lint.lint_all(payload, sidecar)
    for rule in ("R3", "R5", "R11b", "R13"):
        hits = [f for f in findings if f.rule == rule]
        results.append((f"{rule} is aspirational, so vanilla trips it",
                        bool(hits),
                        f"{len(hits)} finding(s)"))
    # The water rules are aspirational too (2026-09-29); vanilla is linted
    # without biomes, so check_water_rules tests them.
    results.append(("aspirational set matches lint.py's tag",
                    lint.ASPIRATIONAL == {"R3", "R5", "R11b", "R13", "R19", "R19b", "R20",
                                          "R21", "R22", "R23", "R24"},
                    f"{sorted(lint.ASPIRATIONAL)}"))


def check_thresholds_come_from_sidecar(results):
    """A threshold edited in design.json must change the verdict; if it does
    not, lint is reading a literal somewhere."""
    _, payload, sidecar = _corpus()
    base = lint.lint_all(payload, sidecar)
    r8_before = [f for f in base if f.rule == "R8"]

    harsh = dict(sidecar or {})
    harsh["thresholds"] = dict(lint.thresholds_from(sidecar))
    harsh["thresholds"]["r8_spread_min"] = 99.0
    after = lint.lint_all(payload, harsh)
    r8_after = [f for f in after if f.rule == "R8"]
    results.append(("R8 threshold is read from the sidecar",
                    not r8_before and len(r8_after) == 1,
                    f"{len(r8_before)} -> {len(r8_after)} at spread_min 99"))


def check_authored_only_r1(results):
    """R1 is an error, so it must not fire on tables this project did not
    author. An area with no archetype declared is not authored."""
    t = lint.thresholds_from(None)
    backwards = [("SPECIES_A", 9)] * 2 + [("SPECIES_B", 2)] * 10
    unauthored = lint.lint_table("x", backwards, {"band": "mid"}, t)
    authored = lint.lint_table("x", backwards,
                               {"band": "mid", "archetype": "A1"}, t)
    results.append(("R1 silent on an unauthored table",
                    not [f for f in unauthored if f.rule == "R1"], ""))
    results.append(("R1 fires on an authored table",
                    bool([f for f in authored if f.rule == "R1"]), ""))


def check_water_rules(results):
    """The water rules (the blind review's principles, 2026-09-29) on small
    made-up tables, each rule once firing and once held: R19 and R19b the
    biome and the sea, R20 one line per area with the Super Rod 1% allowance,
    R21 the 1% gag, R22 the per-split top pair with R15's same-group
    exemption, R23 non-Water off the caves, R24 five lines a table."""
    t = lint.thresholds_from(None)
    G, SK, B, P, W, PS, Z, C, F = ("GOLDEEN", "SEAKING", "BARBOACH", "POLIWAG", "WOOPER",
                                   "PSYDUCK", "ZUBAT", "CHINCHOU", "FROAKIE")
    line = {s: "L_" + s for s in (G, B, P, W, PS, Z, C, F)}
    line[SK] = "L_GOLDEEN"
    info = {"line": line, "name": {}, "line_name": {},
            "water_type": {s: s != Z for s in line},
            "palettes": {"pond": {"L_" + s for s in (G, B, P, W, PS, Z)},
                         "cave_pool": {"L_" + s for s in (G, B, P, W, PS, Z)}},
            "inland": {"pond", "cave_pool"}, "sea_only": {C},
            "split_idx": {"Roark": 0, "Gardenia": 1}, "same_groups": [{"g1", "g2"}]}

    def tb(name, area, biome="pond", split="Roark", earned=(), **slots):
        return {"name": name, "area": area, "biome": biome, "earned": set(earned),
                "opens": {k: split for k in slots}, "slots": slots}

    def rules(*tables, rule):
        return [f for f in lint.lint_water(list(tables), info, t) if f.rule == rule]

    sea = tb("a", "A", old_rod=[G, B, P, W, C])
    results.append(("R19 and R19b: a sea line in a pond is off its palette and at sea, "
                    "unless the place earns it; a table with no biome is reported",
                    rules(sea, rule="R19") and rules(sea, rule="R19b")
                    and not rules(tb("a", "A", earned={"L_" + C}, old_rod=[G, B, P, W, C]),
                                  rule="R19b")
                    and rules(tb("a", "A", biome=None, old_rod=[G, B, P, W, PS]), rule="R19"), ""))
    allowed = tb("a", "A", good_rod=[G, B, P, W, PS], super_rod=[B, P, W, PS, SK])
    grown = tb("a", "A", good_rod=[G, B, P, W, PS], super_rod=[SK, B, P, W, PS])
    two_tables = [tb("a", "A", old_rod=[W, B, P, G, PS]), tb("b", "A", surf=[W, B, P, G, PS])]
    results.append(("R20: the Super Rod's 1% may be a Good Rod line's adult; anywhere else, or "
                    "in two tables of one capture area, a line in two methods is reported",
                    not [f for f in rules(allowed, rule="R20") if "Goldeen" in f.message.title()]
                    and any("Goldeen" in f.message.title() for f in rules(grown, rule="R20"))
                    and any("Wooper" in f.message.title() for f in rules(*two_tables, rule="R20")), ""))
    gag = [tb(f"t{i}", f"Area {i}", old_rod=[G, B, P, W, F]) for i in range(4)]
    results.append(("R21: one line as the 1% in four capture areas is a gag; in three it is not",
                    rules(*gag, rule="R21") and not rules(*gag[:3], rule="R21"), ""))
    pair = [tb("x", "X", old_rod=[G, B, P, W, PS]), tb("y", "Y", old_rod=[B, G, P, W, PS])]
    results.append(("R22: two areas opening in one split with the same top pair are reported; "
                    "different splits, or one R15 'same' group, are not",
                    rules(*pair, rule="R22")
                    and not rules(pair[0], tb("y", "Y", split="Gardenia", old_rod=[B, G, P, W, PS]),
                                  rule="R22")
                    and not rules(tb("g1", "X", old_rod=[G, B, P, W, PS]),
                                  tb("g2", "Y", old_rod=[G, B, P, W, PS]), rule="R22"), ""))
    results.append(("R23: a bat at 60% of a pond's Surf is too much non-Water; in a cave it leads",
                    rules(tb("a", "A", surf=[Z, G, B, P, W]), rule="R23")
                    and not rules(tb("a", "A", biome="cave_pool", surf=[Z, G, B, P, W]), rule="R23"), ""))
    results.append(("R24: a water table of four lines is under five; five distinct lines pass",
                    rules(tb("a", "A", old_rod=[G, SK, B, P, W]), rule="R24")
                    and not rules(tb("a", "A", old_rod=[G, B, P, W, PS]), rule="R24"), ""))
    results.append(("the water rules are aspirational warnings",
                    {"R19", "R19b", "R20", "R21", "R22", "R23", "R24"} <= lint.ASPIRATIONAL
                    and all(f.severity == "warn" for f in lint.lint_water(gag + [sea], info, t)), ""))


def main():
    results = []
    for check in (check_no_errors, check_descriptive_game_rules,
                  check_r11_actually_ran, check_r1b_corpus,
                  check_descriptive_table_rules, check_aspirational_fail,
                  check_thresholds_come_from_sidecar, check_authored_only_r1,
                  check_water_rules):
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

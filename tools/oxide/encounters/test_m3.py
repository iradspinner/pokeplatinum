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
    results.append(("aspirational set matches lint.py's tag",
                    lint.ASPIRATIONAL == {"R3", "R5", "R11b", "R13"},
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


def main():
    results = []
    for check in (check_no_errors, check_descriptive_game_rules,
                  check_r11_actually_ran, check_r1b_corpus,
                  check_descriptive_table_rules, check_aspirational_fail,
                  check_thresholds_come_from_sidecar, check_authored_only_r1):
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

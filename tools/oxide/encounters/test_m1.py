"""M1 acceptance: the I/O layer round-trips and edits stay local.

    PYTHONPATH=. python3 tools/oxide/encounters/test_m1.py

Writes nothing. The edit checks run against in-memory text so a failure can
never leave res/field/encounters/ dirty.
"""
import sys

from . import model

RATES = model.LAND_RATES


def _counts(areas):
    return (len(areas),
            sum(1 for a in areas if a.has_land),
            sum(1 for a in areas if a.land_active))


def check_inventory(results):
    """The corpus is 185 files: 183 land tables, of which 171 are live.
    The two that are not land tables are a different format entirely, and
    twelve more carry twelve slots the game never rolls because land_rate
    is 0. Conflating those two categories is how a loader quietly drops
    files, so they are asserted apart."""
    # The working tree gained encounters_verity_lakefront.json on 2026-09-21
    # (a live land table), and encounters_amity_square.json (live land) and
    # encounters_snowpoint_city.json (rods only, land at rate 0) on
    # 2026-09-25; vanilla on main still has 185.
    for ref, label, want in ((None, "working tree", (188, 186, 173)),
                             ("main", "main", (185, 183, 171))):
        n, land, active = _counts(model.load_all(ref))
        results.append((f"inventory [{label}]",
                        (n, land, active) == want,
                        f"{n} files, {land} land, {active} active"))


def check_roundtrip(results):
    """Every land key, replaced by the value it already holds, must re-render
    byte-identically. This is the gate the design doc calls most likely to
    fail: the repo's JSON style is not reproducible from Python in general,
    so the edit path has to be proved on every slot of every file."""
    for ref, label in ((None, "working tree"), ("main", "main")):
        bad = []
        for a in model.load_all(ref):
            bad += [(a.name, p) for p, _, _ in a.rewrite_identity()]
        results.append((f"round-trip [{label}]", not bad,
                        "clean" if not bad else f"{len(bad)} keys moved: "
                        f"{bad[:3]}"))


def check_edit_is_local(results):
    """A slot write moves one line and no other. Checked on every live table
    rather than a sample, because the failure mode is formatting-dependent
    and one odd file is exactly what would slip through."""
    worst = None
    for a in model.load_all(active_only=True):
        before = a.text.splitlines()
        a.set_slot(5, level=a.levels[5] + 1)
        after = a.text.splitlines()
        moved = sum(1 for x, y in zip(before, after) if x != y)
        if len(before) != len(after) or moved != 1:
            worst = (a.name, moved, len(before), len(after))
            break
    results.append(("one slot edit -> one line", worst is None,
                    "all 171 tables" if worst is None else str(worst)))


def check_species_and_level_independent(results):
    """Writing species must not disturb level, and vice versa."""
    a = model.load_area("encounters_route_201")
    a.set_slot(0, species="SPECIES_SHINX")
    ok_level = a.levels == model.load_area("encounters_route_201").levels
    b = model.load_area("encounters_route_201")
    b.set_slot(0, level=b.levels[0] + 7)
    ok_species = ([s for s, _ in b.slots]
                  == [s for s, _ in model.load_area("encounters_route_201").slots])
    results.append(("species write leaves levels alone", ok_level, ""))
    results.append(("level write leaves species alone", ok_species, ""))


def check_guards(results):
    """The ways this layer is allowed to refuse."""
    ro = model.load_area("encounters_route_201", ref="main")
    live = model.load_area("encounters_route_201")
    cases = [
        ("ref-loaded area is read-only", RuntimeError,
         lambda: ro.set_slot(0, level=5)),
        ("ref-loaded area will not save", RuntimeError, ro.save),
        ("slot 12 rejected", IndexError, lambda: live.set_slot(12, level=5)),
        ("day/night third entry rejected", IndexError,
         lambda: live.set_time_slot("night", 2, "SPECIES_ABRA")),
        ("non-time layer rejected", ValueError,
         lambda: live.set_time_slot("radar", 0, "SPECIES_ABRA")),
    ]
    for label, exc, fn in cases:
        try:
            fn()
            results.append((label, False, "was allowed"))
        except exc:
            results.append((label, True, ""))
        except Exception as e:  # noqa: BLE001
            results.append((label, False, f"raised {type(e).__name__}: {e}"))


def check_ref_is_really_a_ref(results):
    """--ref must read the ref, not the working tree. The two corpora differ
    in species on most tables, so a loader that silently fell back would show
    zero difference here."""
    v = {a.name: a.slots for a in model.load_all("main", active_only=True)}
    o = {a.name: a.slots for a in model.load_all(None, active_only=True)}
    ds = sum(1 for n in v if [s for s, _ in v[n]] != [s for s, _ in o[n]])
    results.append(("--ref reads a different corpus", ds > 0,
                    f"{ds}/{len(v)} tables differ in species"))


def main():
    results = []
    for check in (check_inventory, check_roundtrip, check_edit_is_local,
                  check_species_and_level_independent, check_guards,
                  check_ref_is_really_a_ref):
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

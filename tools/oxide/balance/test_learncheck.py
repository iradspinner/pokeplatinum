"""The learnset baseline's checks on real cases (learncheck.py).

    PYTHONPATH=. python3 -m tools.oxide.balance.test_learncheck

Reads the tree and, for v3, origin/balance-learngen-v2 through git (fetch it
first). Nothing is written.
"""
import collections
import json
import os
import sys

from . import learncheck as lc, pool


def check_catches(results):
    """The capture areas are pool's catches, row for row, with only the
    place added."""
    ours = collections.Counter(r[:4] for r in lc.catch_rows())
    theirs = collections.Counter((sp, split, level, how) for sp, rows in pool.catches().items()
                                 for split, level, how in rows)
    ok = ours == theirs
    results.append(("catch rows are pool.catches()", ok,
                    f"{sum(ours.values())} rows" if ok else
                    f"ours only {list((ours - theirs).items())[:3]}, pool only "
                    f"{list((theirs - ours).items())[:3]}"))


def check_at_capture(results):
    """The four moves known at capture follow the game's rule. Alolan
    Ninetales, caught wild at 13 on Route 211, has twenty level-1 entries
    (Dazzling Gleam twice); it knows the last four. Charmander at 8 has only
    three entries by then and knows all three, in list order."""
    nine = [lc.move_name(m) for m in lc.at_capture("oxide", "SPECIES_ALOLAN_NINETALES", 13)]
    char = [lc.move_name(m) for m in lc.at_capture("oxide", "SPECIES_CHARMANDER", 8)]
    route = any(r[:3] == ("SPECIES_ALOLAN_NINETALES", "Gardenia", 13) and r[4] == "Route 211"
                for r in lc.catch_rows())
    # The rule written out again here, independently: in order up to the
    # level, level 0 skipped, a known move skipped, the oldest dropped at five.
    def by_hand(lst, level):
        known = []
        for lv, mv in lst:
            if lv == 0:
                continue
            if lv > level:
                break
            if mv not in known:
                known = (known + [mv])[-4:]
        return known
    agree = all(lc.at_capture(v, sp, lv) == by_hand(list(lc.learnset(v, sp)), lv)
                for v in lc.VERSIONS for sp, _s, lv, _h, _p in lc.catch_rows()
                if sp in lc.species_set())
    ok = (route and nine == ["Tail Whip", "Disable", "Ice Shard", "Safeguard"]
          and char == ["Scratch", "Growl", "Ember"] and agree)
    results.append(("known at capture is the last four by the catch level", ok,
                    f"Alolan Ninetales at 13: {nine}; Charmander at 8: {char}; every catch agrees "
                    f"with the rule written out: {agree}"))


def check_dragon_rage(results):
    """Check 4 flags Charmander's Dragon Rage at 16, in Roark's split, as
    the ruling Ian made still broken."""
    hit = lc.check4_early("oxide").get(("SPECIES_CHARMANDER", "MOVE_DRAGON_RAGE"))
    state = lc.ruling_state("SPECIES_CHARMANDER", "MOVE_DRAGON_RAGE", hit[0]) if hit else None
    ok = hit == ("Roark", 16, "level-up") and state == "broken"
    results.append(("check 4 flags Charmander's Dragon Rage at 16", ok, f"{hit}, ruling {state}"))


def check_setup_pp(results):
    """Check 5 reads Swords Dance, Dragon Dance and Bulk Up as setup and
    judges their PP by 1 to 3; Growl is a stat-lowering move, judged by 3 to
    6, and fails while it keeps its 40 (the PP pass still open in the
    tracker)."""
    rows = {c: (pp, ok) for c, pp, ok in lc.lint_pp()["setup"]}
    low = {c: (pp, ok, rule) for c, pp, ok, rule in lc.lint_pp()["lowering"]}
    named = all(c in rows and rows[c][1] == (1 <= lc.moves()[c]["pp"] <= 3)
                for c in ("MOVE_SWORDS_DANCE", "MOVE_DRAGON_DANCE", "MOVE_BULK_UP"))
    growl = low.get("MOVE_GROWL")
    judged = growl and growl[2] == "3 to 6" and growl[1] == (3 <= lc.moves()["MOVE_GROWL"]["pp"] <= 6)
    not_setup = "MOVE_GROWL" not in rows and "MOVE_SWORDS_DANCE" not in low
    ok = named and judged and not_setup and lc.SETUP_PP == (1, 3)
    results.append(("check 5 judges setup and stat-lowering PP", ok,
                    f"Swords Dance {rows.get('MOVE_SWORDS_DANCE')}, Bulk Up {rows.get('MOVE_BULK_UP')}, "
                    f"Growl {growl}"))


def check_v3_reading(results):
    """v3's lists read as the scoring track's build_v3.py read them, where its
    output is on this machine; every v3 species is one of the tree's."""
    path = os.path.expanduser("~/oxide-trials/learnset-baseline/v3_learnsets.json")
    unknown = sorted(set(lc.v3_lists()) - lc.species_set())
    if not os.path.exists(path):
        results.append(("v3 read as the scoring track reads it", not unknown,
                        f"{len(lc.v3_lists())} species; the scoring track's copy is not here"))
        return
    with open(path, encoding="utf-8") as f:
        theirs = {sp: [tuple(e) for e in lst] for sp, lst in json.load(f).items()}
    ours = {sp: list(lst) for sp, lst in lc.v3_lists().items()}
    differ = sorted(sp for sp in set(ours) | set(theirs) if ours.get(sp) != theirs.get(sp))
    ok = not differ and not unknown
    results.append(("v3 read as the scoring track reads it", ok,
                    f"{len(ours)} species alike" if ok else f"differ {differ[:5]}, unknown {unknown[:5]}"))


def check_held_out(results):
    """The draw is fixed: five distinct lines from the twenty, the same each run."""
    a, b = lc.held_out(), lc.held_out()
    ok = (a == b and len(set(a)) == lc.HELD_OUT_COUNT and set(a) <= set(lc.INSIGHT_LINES)
          and len(set(lc.INSIGHT_LINES)) == 20)
    results.append(("five held out by the fixed seed", ok, ", ".join(lc.species_name(s) for s in a)))


def main():
    results = []
    for check in (check_catches, check_at_capture, check_dragon_rage, check_setup_pp,
                  check_v3_reading, check_held_out):
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

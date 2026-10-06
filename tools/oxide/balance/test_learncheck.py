"""The learnset checks on real cases (learncheck.py): checks 1, 4 and 5 of
the baseline, and checks 7 to 22 of the locked rules, each against a case
Ian judged in the insight sessions (docs/oxide/learnset-insights.md), read
from Oxide's lists as they were before the rewrite (learncheck.BASE_REF).

    PYTHONPATH=. python3 -m tools.oxide.balance.test_learncheck

Reads the tree, the base ref and, for v3, origin/balance-learngen-v2
through git (fetch it first). Nothing is written.
"""
import collections
import json
import os
import sys

from . import learncheck as lc, pool

O = "oxide"


def names(moves):
    return [lc.move_name(m) for m in moves]


def check_catches(results):
    """The capture areas are pool's catches, row for row, with only the
    place added, but for Ian's two corrections: Amity Square's unmet table
    left out, and Cynthia's Togepi egg read in Fantina's split."""
    raw = lc._pool_rows()
    ours = collections.Counter(r[:4] for r in raw)
    theirs = collections.Counter((sp, split, level, how) for sp, rows in pool.catches().items()
                                 for split, level, how in rows)
    fixed = lc.catch_rows()
    amity = sum(1 for r in raw if r[4] in lc.UNMET_PLACES)
    togepi = [r[1] for r in fixed if r[0] == "SPECIES_TOGEPI" and r[3] == "egg gift"]
    raw_fossils = {(r[0], r[3]) for r in raw if r[3] == "fossil"}
    fossils = [r for r in fixed if r[3] == "fossil"]
    added = [r for r in fossils if (r[0], r[3]) not in raw_fossils]
    ok = ours == theirs and len(fixed) == len(raw) - amity + len(added) and amity > 0 \
        and togepi == ["Fantina"] and not any(r[4] in lc.UNMET_PLACES for r in fixed) \
        and len(added) >= 4 and all(r[1] == "Fantina" for r in added)
    results.append(("catch rows are pool.catches(), Ian's three fixes apart", ok,
                    f"{sum(ours.values())} rows, {amity} Amity Square rows left out, Togepi's egg in "
                    f"{togepi}, {len(fossils)} fossils in Fantina's split" if ours == theirs else
                    f"ours only {list((ours - theirs).items())[:3]}, pool only "
                    f"{list((theirs - ours).items())[:3]}"))


def check_named_moves(results):
    """Every move the rule sets and tiers name exists in the tree, and the
    sets read as meant: Thrash a rampage move, Hyper Beam, Dig and Bullet Seed
    waiting on their rework, Detect and Fissure off the lists, Fury Attack
    removed; Rock Tomb an incredible speed control attack; Swords Dance not
    rated by Ian, so the Generation 9 list's S, a good move."""
    named = set(lc.REMOVED) | lc.OUT_BY_NAME | lc.PENDING_BY_NAME | \
        {"MOVE_" + m for ms in lc.IAN_TIERS.values() for m in ms}
    missing = sorted(m for m in named if m not in lc.moves())
    ok = (not missing and lc.rampage("MOVE_THRASH") and all(lc.pending(m) for m in
          ("MOVE_HYPER_BEAM", "MOVE_DIG", "MOVE_BULLET_SEED", "MOVE_FURY_CUTTER"))
          and lc.out_of_lists("MOVE_DETECT") and lc.out_of_lists("MOVE_FISSURE")
          and not lc.reliable("MOVE_FURY_ATTACK") and lc.reliable("MOVE_FLAMETHROWER")
          and lc.tier("MOVE_ROCK_TOMB") == (lc.TIER_RANK["Incredible"], "Ian")
          and lc.tier("MOVE_SWORDS_DANCE") == (lc.GOOD, "Generation 9 list")
          and not lc.pending("MOVE_SOLAR_BEAM"))
    results.append(("the rule sets name real moves and read as meant", ok,
                    f"missing {missing}" if missing else f"{len(named)} named"))


def check_r1(results):
    """Check 7: Charmander has four moves by Roark's cap once Dragon Rage is
    gone, three of them filler (Ian: "ideally 5-6 moves by 16"); Popplio
    passes, with Disarming Voice early coverage, not filler."""
    char = lc.check7(O)["SPECIES_CHARMANDER"]
    pop = lc.check7(O)["SPECIES_POPPLIO"]
    ok = (char["verdict"] == "fail" and names(char["moves"]) == ["Scratch", "Growl", "Ember", "SmokeScreen"]
          and names(char["filler"]) == ["Scratch", "Growl", "SmokeScreen"]
          and pop["verdict"] == "pass" and "MOVE_DISARMING_VOICE" not in pop["filler"])
    results.append(("check 7 (R1) reads Charmander and Popplio as Ian did", ok,
                    f"Charmander {names(char['moves'])}, Popplio's filler {names(pop['filler'])}"))


def check_r2(results):
    """Check 8, by bands of eight levels (2026-10-06): Charmeleon learns only
    Scary Face from 17 to 24 ("farcical" in Gardenia's split); Onix, waiting
    on a Metal Coat, is read past its on-time evolution, DragonBreath at 33
    in the short band its hold ends with."""
    cm = lc.check8(O)["SPECIES_CHARMELEON"]
    onix = lc.check8(O)["SPECIES_ONIX"]["bands"]
    ok = (cm["verdict"] == "fail" and cm["short"] == ("17-24",) and names(cm["bands"]["17-24"]) == ["Scary Face"]
          and names(onix.get("17-24", ())) == ["Rock Tomb"] and names(onix.get("33-33", ())) == ["DragonBreath"])
    results.append(("check 8 (R2) reads Charmeleon's first band and Onix's hold", ok,
                    f"Charmeleon {names(cm['bands'].get('17-24', ()))}, "
                    f"Onix {dict((b, names(m)) for b, m in onix.items())}"))


def check_fit_rows(results):
    """Check 22's rows from the exam's regressions (2026-10-06), on Oxide's
    lists: Koffing's wild catches know Selfdestruct, a trainer-only move; Grovyle's
    False Swipe at 53 is past Fantina's split. And check 24: Oxide's lists
    leave the Eevee line's branches far apart, with Vaporeon among the weak."""
    c22 = lc.check22(O)
    koffing = [d for sp, d in c22["trainer-only move a wild catch knows"] if sp == "SPECIES_KOFFING"]
    late = [sp for sp, _d in c22["catch-only move after Fantina's split"]]
    eevee = next((r for r in lc.check24(O) if r[0] == "SPECIES_EEVEE"), None)
    ok = (any(d.startswith("Selfdestruct") for d in koffing) and "SPECIES_GROVYLE" in late
          and eevee is not None and eevee[3] == "fail"
          and min(eevee[2], key=eevee[2].get) in ("SPECIES_VAPOREON", "SPECIES_GLACEON"))
    results.append(("check 22's new rows and check 24 read the exam's cases", ok,
                    f"Koffing {koffing}, late catch-only {late}, "
                    f"Eevee {eevee[2] if eevee else None}"))


def check_r4_r5(results):
    """Checks 9 and 10: the Charmander line learns no coverage at all by level-up
    (Ian: "precisely 0"), with Kaizo's Dark, Flying and Steel beside it;
    Shinx's first is Luxio's Bite at 18, in its second split."""
    c9 = lc.check9(O)
    c10 = lc.check10(O)["SPECIES_CHARIZARD"]
    shinx = c9["SPECIES_SHINX"]["first"]
    ok = (c9["SPECIES_CHARMANDER"]["verdict"] == "fail" and c9["SPECIES_CHARMANDER"]["first"] is None
          and c10["verdict"] == "fail" and not c10["types"]
          and {"DARK", "FLYING", "STEEL"} <= set(c10["kaizo"])
          and shinx and shinx[1:3] == (18, "MOVE_BITE") and c9["SPECIES_SHINX"]["verdict"] == "pass")
    results.append(("checks 9 and 10 (R4, R5) read Charmander's and Shinx's coverage", ok,
                    f"Charizard {c10['types']}, Kaizo {c10['kaizo']}; Shinx {shinx}"))


def check_r6(results):
    """Check 11: Delphox's Expanding Force after Psychic is dominated; Charizard's
    Fire Spin after Flamethrower is not, since it binds (R6 as narrowed)."""
    hits = {(sp, mv) for sp, _lv, mv, _n in lc.check11(O)}
    ok = ("SPECIES_DELPHOX", "MOVE_EXPANDING_FORCE") in hits and \
        ("SPECIES_CHARIZARD", "MOVE_FIRE_SPIN") not in hits
    results.append(("check 11 (R6) flags a plain weaker move only", ok, f"{len(hits)} entries"))


def check_r7(results):
    """Check 12: Charizard passes on Scary Face; Altaria, a less offensive line,
    has Dragon Dance alone and fails for want of a second good move."""
    c12 = lc.check12(O)
    cz, alt = c12["SPECIES_CHARIZARD"], c12["SPECIES_ALTARIA"]
    ok = (cz["verdict"] == "pass" and "MOVE_SCARY_FACE" in cz["early"]
          and alt["verdict"] == "fail" and alt["offense"] < lc.R7_LOW_OFFENSE)
    results.append(("check 12 (R7) reads Charizard and Altaria", ok,
                    f"Charizard {names(cz['early'])}, Altaria {names(alt['total'])} at {alt['offense']}"))


def check_r8(results):
    """Check 13: Charmeleon's Flamethrower at 39, after Charizard at 36 in the
    same split (Ian: "always better to delay"), and Gabite's Dragon Rush at
    49, after Garchomp at 48, are free holds."""
    holds = {(pre, mv, a) for kind, pre, _t, mv, a, _b in lc.check13(O) if kind == "free hold"}
    ok = {("SPECIES_CHARMELEON", "MOVE_FLAMETHROWER", 39), ("SPECIES_GABITE", "MOVE_DRAGON_RUSH", 49)} <= holds
    results.append(("check 13 (R8) finds the holds inside one split", ok, f"{len(holds)} free holds"))


def check_r11(results):
    """Check 14: Steelix has no Ground attack (Ian: "a travesty"), Glalie no
    Rock attack, Charizard no Dragon attack."""
    c14 = lc.check14(O)
    ok = ("GROUND" in c14["SPECIES_STEELIX"]["missing"] and "ROCK" in c14["SPECIES_GLALIE"]["missing"]
          and "DRAGON" in c14["SPECIES_CHARIZARD"]["missing"]
          and all(c14[s]["verdict"] == "fail" for s in ("SPECIES_STEELIX", "SPECIES_GLALIE")))
    results.append(("check 14 (R11) finds the missing types", ok,
                    f"Steelix {c14['SPECIES_STEELIX']['missing']}, Glalie {c14['SPECIES_GLALIE']['missing']}"))


def check_mechanical(results):
    """Checks 15 to 19: Togetic's Baton Pass with no boost (R21); Snorunt's
    Double Team and Protect, and Abra's Teleport (R24, removed); Glalie's Ice
    Beam at 37, below its 42 (R25); Budew's Growth with only Absorb and Mega
    Drain, and Altaria's Dragon Dance with only Take Down (R32); Onix's Stone
    Edge and Iron Tail (R37)."""
    c16 = {(sp, m) for sp, w, m, _r in lc.check16(O) if w.startswith("level")}
    c17 = {(sp, lv, m) for sp, lv, m, _lo in lc.check17(O)}
    c18 = {(sp, m) for sp, _lv, m, _k in lc.check18(O)}
    c19 = {(sp, m) for sp, _lv, m, _a in lc.check19(O)}
    want = [("SPECIES_TOGETIC" in lc.check15(O), "Togetic's Baton Pass"),
            (("SPECIES_SNORUNT", "MOVE_DOUBLE_TEAM") in c16 and ("SPECIES_SNORUNT", "MOVE_PROTECT") in c16,
             "Snorunt's Double Team and Protect"),
            (("SPECIES_ABRA", "MOVE_TELEPORT") in c16, "Abra's Teleport"),
            (("SPECIES_GLALIE", 37, "MOVE_ICE_BEAM") in c17, "Glalie's Ice Beam 37"),
            (("SPECIES_BUDEW", "MOVE_GROWTH") in c18, "Budew's Growth"),
            (("SPECIES_ALTARIA", "MOVE_DRAGON_DANCE") in c18, "Altaria's Dragon Dance"),
            (("SPECIES_ONIX", "MOVE_STONE_EDGE") in c19 and ("SPECIES_ONIX", "MOVE_IRON_TAIL") in c19,
             "Onix's Stone Edge and Iron Tail")]
    missed = [label for ok, label in want if not ok]
    results.append(("checks 15 to 19 find Ian's named cases", not missed,
                    f"missed {missed}" if missed else f"{len(want)} cases"))


def check_evolutions_and_late(results):
    """Check 20: Sylveon is unreachable (Eevee has Charm only on its egg list),
    Tangrowth reachable. Check 21: Charizard's Flare Blitz is a late move.
    Check 22: Trapinch's Fissure at 89 is past the League."""
    c20 = {(pre, t): verdict for pre, _m, t, _how, verdict in lc.check20(O)}
    past = {sp for sp, _d in lc.check22(O)["past the League"]}
    c23 = lc.check23(O)
    ok = (c20.get(("SPECIES_EEVEE", "SPECIES_SYLVEON")) == "fail"
          and c20.get(("SPECIES_TANGELA", "SPECIES_TANGROWTH")) == "pass"
          and "MOVE_FLARE_BLITZ" in lc.check21(O)["SPECIES_CHARIZARD"]
          and "SPECIES_TRAPINCH" in past
          and not c23["SPECIES_CHARMANDER"] and not c23["SPECIES_ONIX"] and not c23["SPECIES_BUDEW"]
          and lc.moves()["MOVE_SHADOW_FORCE"]["id"] == lc.GEN4_LAST_ID)
    results.append(("checks 20 to 23 read Sylveon, Charizard, Trapinch and the newer moves", ok,
                    f"Sylveon {c20.get(('SPECIES_EEVEE', 'SPECIES_SYLVEON'))}, {len(past)} species past 78; "
                    f"Charmander, Onix and Budew learn no newer move (Ian: '0 newer gen moves')"))


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
                  check_v3_reading, check_held_out, check_named_moves, check_r1, check_r2,
                  check_r4_r5, check_r6, check_r7, check_r8, check_r11, check_mechanical,
                  check_evolutions_and_late, check_fit_rows):
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

"""The line tester (docs/oxide/line-tester.md): checks 2, 3 and 6 of its
version 1, and what they rest on.

    PYTHONPATH=. python3 -m tools.oxide.encounters.test_linetester

Check 2: the page's AI odds are plplan.ai_distribution's, mixed over the
turn's Quick Claw rolls, in every position of a test line (Quick Claws
included). Check 3: the page's overview of a turn is the simulator's own
enumeration (turn_outcomes), and following an outcome plays an exact roll
inside its band, the one picked, the band's worst or one drawn, never the
band's stand-in. Check 6: a pinned check plays as pinned and the rest are
drawn at their real odds. Beside them: every check is labelled with its
Pokemon and move, the pass-throughs change nothing the planner finds, a
saved line reloads to the same tree, and a trainer read from a branch is
the trainer the tree has. The test line is Ian's Gardenia six of
2026-10-13 against Gardenia, built from records so that it does not hang on
where the encounter tables put each catch. Lines go to a folder of their
own, removed at the end. About a minute.
"""
import collections
import math
import random
import shutil
import sys
import tempfile

from ..balance import fightsim as fs
from ..balance import plplan
from ..balance import plteam
from . import linetester as lt

SIX = [("SPECIES_TSAREENA", ["Razor Leaf", "Rapid Spin", "Double Kick", "Taunt"]),
       ("SPECIES_CARBINK", ["Reflect", "Ancient Power", "Draining Kiss", "Rock Throw"]),
       ("SPECIES_NUZLEAF", ["Fake Out", "Silver Wind", "Snarl", "Bullet Seed"]),
       ("SPECIES_GOLBAT", ["Dual Wingbeat", "Leech Life", "Bite", "Poison Sting"]),
       ("SPECIES_BRELOOM", ["Bullet Seed", "Mach Punch", "Headbutt", "Leech Seed"]),
       ("SPECIES_CORVISQUIRE", ["Dual Wingbeat", "Drill Peck", "Steel Wing", "Taunt"])]


def setup():
    """Ian's six at the reading's rules: level 26, Hardy, IVs of 15, the
    first ability, the scorer's own items."""
    blob = fs.calc.blob()["poks"]
    recs = []
    for const, moves in SIX:
        name = plteam.species_name(const)
        recs.append(plteam.record(const, 26, "Hardy", blob[name]["abilities"]["0"], 15, moves))
    return {"source": "records", "fight": "gardenia", "variant": 0, "records": recs,
            "moves": [m for _c, m in SIX], "held": None, "lead": 0, "level": 26, "label": "test line"}


def menu_actions(line, nid):
    v = lt.menu(line.node(nid).b)
    return ([["move", m["name"]] for m in v["moves"] if m["ok"]]
            + [["switch", s["index"]] for s in v["switches"]])


def play(line, nid, action, pins, seed, rng):
    """Line.play, choosing any replacement it asks for at random."""
    pins = dict(pins)
    while True:
        out = line.play(nid, action, pins, seed)
        if "needs" not in out:
            return out["node"]
        pins[out["needs"]["key"]] = rng.choice(out["needs"]["options"])["index"]


def build_line(rng):
    """The test line: random actions from the menu for six turns, then a
    position set by hand with a Quick Claw on every Pokemon, played on with
    random actions for fourteen turns, so the AI's odds are mixed over four
    rolls in most of its positions; and two branches from the start set by
    hand, a confused Pokemon at +2 Attack and a paralysed one, each using
    its moves."""
    line = lt.Line(setup(), name="test-line")
    nid = 0
    for _t in range(6):
        nid = play(line, nid, rng.choice(menu_actions(line, nid)), {}, rng.randrange(1 << 30), rng)
    b = line.node(nid).b
    claws = {"item": "Quick Claw"}
    edits = {"player": {"mons": {str(i): claws for i in range(len(b.p.mons))}},
             "trainer": {"mons": {str(i): claws for i in range(len(b.b.mons))}}}
    nid = line.set_position(nid, edits)["node"]
    for _t in range(14):
        if lt.finished(line.node(nid).b):
            break
        nid = play(line, nid, rng.choice(menu_actions(line, nid)), {}, rng.randrange(1 << 30), rng)
    # Two branches from the start set by hand, as Ian's Gardenia questions
    # were: Nuzleaf confused at +2 Attack in front of Lumineon, and a
    # paralysed Breloom, each played on for three turns.
    for edits in ({"player": {"active": 2, "mons": {"2": {"confused": 4, "stages": {"atk": 2}}}},
                   "trainer": {"active": 2}},
                  {"player": {"active": 4, "mons": {"4": {"status": "par"}}}}):
        nid = line.set_position(0, edits)["node"]
        for _t in range(3):
            if lt.finished(line.node(nid).b):
                break
            moves = [a for a in menu_actions(line, nid) if a[0] == "move"]
            nid = play(line, nid, rng.choice(moves), {}, rng.randrange(1 << 30), rng)
    return line


def check_ai_odds(results, line):
    """Check 2: in every position, the odds the page shows are
    ai_distribution's at each Quick Claw roll, mixed by that roll's
    chance."""
    bad, mixed, positions = [], 0, 0
    for nid, n in line.nodes.items():
        b = n.b
        if lt.finished(b):
            continue
        positions += 1
        v = line.view(nid)
        shown = dict(v["ai"]["odds"])
        want = collections.defaultdict(float)
        cases = plplan.quick_outcomes(b)
        for (quick, pq), case in zip(cases, v["ai"]["by_quick"]):
            c = plplan.clone(b)
            c.quick = quick
            dist = [(lt.ai_label(c, a), p) for a, p in plplan.ai_distribution(c)]
            for lab, p in dist:
                want[lab] += pq * p
            if case["quick"] != quick or abs(case["p"] - pq) > 1e-12 or \
                    {k: round(p, 12) for k, p in case["odds"]} != {k: round(p, 12) for k, p in dist}:
                bad.append((nid, "case", quick))
        mixed += len(cases) > 1
        if shown.keys() != want.keys() or any(abs(shown[k] - want[k]) > 1e-12 for k in want) \
                or abs(sum(shown.values()) - 1) > 1e-9:
            bad.append((nid, shown, dict(want)))
    results.append(("check 2: the page's AI odds are ai_distribution's mixed over the Quick Claw rolls, "
                    "in every position of the test line",
                    not bad and positions >= 15 and mixed >= 8,
                    f"{positions} positions, {mixed} with Quick Claw rolls to mix; differences {bad[:2]}"))


def check_overview(results, line):
    """Check 3, first half: each overview is turn_outcomes' own merged
    positions, with their chances, for every Quick Claw roll and AI choice,
    for every action in the menu of every position."""
    bad, compared, actions = [], 0, 0
    for nid, n in line.nodes.items():
        b = n.b
        if lt.finished(b):
            continue
        for action in menu_actions(line, nid):
            actions += 1
            lines = line.overview(nid, action)
            key = lt._mix(line.name, nid, "overview")
            got = collections.defaultdict(dict)
            for ln in lines:
                k = (tuple(sorted(ln["quick"].items())), ln["ai"])
                got[k][ln["out"]["merge"]] = (round(ln["p"], 12), round(ln["chance"], 12), lt.fingerprint(ln["out"]["c"]))
            want = collections.defaultdict(dict)
            a = lt.resolve_action(b, action)
            for quick, pq in plplan.quick_outcomes(b):
                c0 = plplan.clone(b)
                c0.quick = quick
                for aa, pa in plplan.ai_distribution(c0):
                    k = (tuple(sorted(quick.items())), lt.ai_label(c0, aa))
                    for c, p in plplan.turn_outcomes(c0, a, aa, key):
                        want[k][plplan.merge_key(c)] = (round(p, 12), round(pq * pa * p, 12), lt.fingerprint(c))
                    compared += 1
            total = sum(ln["chance"] for ln in lines)
            if got != want or abs(total - 1) > 1e-9:
                bad.append((nid, action))
            view = line.overview_view(nid, action)
            if [round(o["chance"], 12) for o in view] != [round(ln["chance"], 12) for ln in lines]:
                bad.append((nid, action, "view"))
    results.append(("check 3: the overview of every action in every position is turn_outcomes' own "
                    "enumeration, each outcome's chance its Quick Claw roll's times the AI's odds times its own",
                    not bad and compared >= 150, f"{actions} actions, {compared} enumerations compared; "
                                                 f"differences {bad[:3]}"))


def _band_events(ln):
    d = ln["out"]["dice"]
    for rec in d.notes:
        if rec["method"] == "roll" and rec["event"] is not None and "groups" in (rec.get("rolls") or {}):
            band = rec["rolls"]["groups"][d.picked[rec["event"]]]
            yield rec, band


def check_follow(results, line, rng):
    """Check 3, second half: following an outcome plays an exact roll inside
    its band (the one picked, the band's worst for Ian, or one drawn), lands
    in that outcome with its chance, and where the roll's damage differs from
    the band's stand-in the position does too."""
    cases = bad = exact = 0
    notes = []
    for nid in list(line.nodes):
        b = line.node(nid).b
        if lt.finished(b):
            continue
        for action in menu_actions(line, nid)[:4]:
            for i, ln in enumerate(line.overview(nid, action)):
                bands = list(_band_events(ln))
                if not bands or len(bands) > 1:
                    continue
                rec, band = bands[0]
                dmg = rec["rolls"]["dmg"]
                if len({dmg[r] for r in band}) < 2:
                    continue
                victim = rec["rolls"]["victim"]
                worst = (max if victim == "p" else min)(band, key=lambda r: (dmg[r], r))
                stand_in = band[len(band) // 2]
                pick = next((r for r in band if dmg[r] != dmg[stand_in]), band[0])
                for mode, rolls, want in (("worst", {}, worst), ("draw", {}, None), ("worst", {rec["key"]: pick}, pick)):
                    out = line.follow(nid, action, i, mode, rolls, seed=rng.randrange(1 << 30))
                    while "needs" in out:
                        pins = dict(out["pins"], **{out["needs"]["key"]: out["needs"]["options"][0]["index"]})
                        out = line.play(nid, action, pins, out["seed"], followed=out["followed"])
                    node = line.node(out["node"])
                    cases += 1
                    played = next((ch for ch in node.checks if ch["key"] == rec["key"]), None)
                    ok = (played is not None and played["outcome"] in band and played["how"] == "pinned"
                          and (want is None or played["outcome"] == want)
                          and node.outcome == i and abs(node.chance - ln["chance"]) < 1e-12)
                    # The stand-in's position is the overview's: where only this
                    # hit moved the victim's HP there, it moves it by the exact
                    # roll's damage here.
                    if ok and played is not None:
                        r = played["outcome"]
                        side0 = b.p if victim == "p" else b.b
                        rep = ln["out"]["c"]
                        idx = next(j for j, m in enumerate(side0.mons) if m.species == rec["rolls"]["victim_name"]
                                   and m is side0.cur())
                        before = side0.mons[idx].hp
                        rep_hp = (rep.p if victim == "p" else rep.b).mons[idx].hp
                        new_hp = (node.b.p if victim == "p" else node.b.b).mons[idx].hp
                        if before - rep_hp == min(before, dmg[stand_in]):
                            ok = before - new_hp == min(before, dmg[r])
                            if dmg[r] != dmg[stand_in]:
                                exact += 1
                    if not ok:
                        bad += 1
                        notes.append((nid, action, i, mode, played and played["outcome"], want))
                if cases >= 45:
                    break
            if cases >= 45:
                break
        if cases >= 45:
            break
    results.append(("check 3: following an outcome plays an exact roll in its band (picked, the worst for "
                    "Ian, or drawn), lands in that outcome, and never plays the band's stand-in",
                    not bad and cases >= 30 and exact >= 10,
                    f"{cases} follows, {exact} with a roll whose damage differs from the stand-in's; "
                    f"failures {notes[:3]}"))


def _tally(line, nid, action, pins, runs, seed0):
    """Each check's outcomes over many plays of one turn, by run_turn as
    Line.play runs it: ({key: Counter of outcomes}, {key: (odds, label)},
    {key: Counter of the AI's choices by name})."""
    counts = collections.defaultdict(collections.Counter)
    named = collections.defaultdict(collections.Counter)
    odds = {}
    b = line.node(nid).b
    pins = dict(pins, **{"replace|p#0": 1, "replace|p#1": 2})
    for s in range(runs):
        _c, p = lt.run_turn(b, action, pins, seed0 + s)
        for ch in p.checks:
            if ch["kind"] == "replacement":
                continue
            counts[ch["key"]][ch["outcome"]] += 1
            if ch["kind"] == "ai":
                named[ch["key"]][ch["value"]] += 1
            odds.setdefault(ch["key"], (ch["probs"], ch["label"]))
    return counts, odds, named


def _at_odds(counts, odds, runs_min=200):
    """The checks whose outcomes stray from their odds: each outcome's count
    within 4.5 standard deviations of its expectation (and a chi-square under
    its 99.99th percentile for a sixteen-way roll)."""
    off = []
    for key, c in counts.items():
        n = sum(c.values())
        probs, label = odds[key]
        if n < runs_min:
            continue
        if len(probs) >= 8:
            chi = sum((c.get(i, 0) - n * p) ** 2 / (n * p) for i, p in enumerate(probs) if p > 0)
            if chi > 45:          # 15 degrees of freedom: 99.99th percentile about 44.3
                off.append((label, round(chi, 1)))
            continue
        for i, p in enumerate(probs):
            sd = math.sqrt(n * p * (1 - p)) or 1
            if abs(c.get(i, 0) - n * p) > 4.5 * sd + 1:
                off.append((label, i, c.get(i, 0), round(n * p, 1)))
    return off


def check_pins(results, line):
    """Check 6: a turn played many times with nothing pinned draws each
    check at its odds; with a critical hit, a damage roll or the AI's move
    pinned, that check never varies and the others still do."""
    action = ["move", "Razor Leaf"]
    counts, odds, named = _tally(line, 0, action, {}, 3000, 1)
    off = _at_odds(counts, odds)
    tested = [odds[k][1] for k, c in counts.items() if sum(c.values()) >= 200]
    results.append(("check 6: with nothing pinned, each check of a turn played 3000 times comes up at its odds",
                    not off and len(tested) >= 4, f"{len(tested)} checks tested: {tested}; off {off[:3]}"))
    crit = next(k for k in counts if k.startswith("p0|Razor Leaf|move|good:crit"))
    roll = next(k for k in counts if k.startswith("p0|Razor Leaf|move|roll"))
    report, ok = [], True
    for name, pins, key in (("a critical hit", {crit: 1}, crit), ("a damage roll", {roll: 3}, roll),
                            ("the AI's move", {"ai|choice#0": "Zen Headbutt"}, "ai|choice#0")):
        c, o, nm = _tally(line, 0, action, pins, 400, 50000)
        # A check that some plays do not make (no damage roll where a critical
        # hit knocks out with every roll) is held if it never varies where made.
        made = sum(c[key].values())
        if key == "ai|choice#0":
            held = dict(nm[key]) == {"Zen Headbutt": 400}
        else:
            held = set(c[key]) == {pins[key]} and made >= 300
        varying = [o[k][1] for k in c if k != key and len(c[k]) > 1]
        ok = ok and held and len(varying) >= 1
        report.append(f"{name}: {'held' if held else 'VARIED'} in the {made} plays that made it, "
                      f"still varying: {varying}")
    results.append(("check 6: a pinned critical hit, damage roll or AI move never varies over 400 plays, while "
                    "the turn's other checks still do", ok, "; ".join(report)))


def check_labels(results, line):
    """Every check of every turn in the line names its Pokemon, and its
    move where it belongs to one; a check of the field says so."""
    bad, seen, kinds = [], 0, set()
    for n in line.nodes.values():
        b = line.nodes[n.parent].b if n.parent is not None else n.b
        mons = {m.key: m for m in b.p.mons + b.b.mons + n.b.p.mons + n.b.b.mons}
        moves = {mv.name for m in mons.values() for mv in m.moves}
        for ch in n.checks:
            seen += 1
            kinds.add(ch["kind"])
            label = ch.get("label") or ""
            who = ch.get("who")
            if not label:
                bad.append(("empty", ch["key"]))
                continue
            if who in mons:
                if mons[who].species not in label:
                    bad.append((ch["key"], label))
                parts = ch["key"].split("|")
                if len(parts) >= 3 and parts[1] in moves and parts[1] not in label:
                    bad.append((ch["key"], label))
            elif not label.startswith(("Speed tie", "End of turn", "This turn")):
                bad.append((ch["key"], label))
    results.append(("every check of the test line is labelled with its Pokemon, and its move where it has one",
                    not bad and seen >= 60 and {"paralysis", "confusion", "confusion roll"} <= kinds, f"{seen} checks of {len(kinds)} kinds ({', '.join(sorted(kinds))}); "
                                            f"unlabelled {bad[:3]}"))


def check_pass_through(results, line):
    """The wrappers that label the checks change nothing the planner finds:
    turn_outcomes gives the same positions with them and without."""
    same, tried = True, 0
    for nid in list(line.nodes)[:6]:
        b = line.node(nid).b
        if lt.finished(b):
            continue
        for action in menu_actions(line, nid)[:3]:
            a = lt.resolve_action(b, action)
            c0 = plplan.clone(b)
            c0.quick = {}
            aa = plplan.ai_distribution(c0)[0][0]
            lt.uninstall()
            try:
                without = [(plplan.merge_key(c), p, lt.fingerprint(c)) for c, p in plplan.turn_outcomes(c0, a, aa, 5)]
            finally:
                lt.install()
            with_ = [(plplan.merge_key(c), p, lt.fingerprint(c)) for c, p in plplan.turn_outcomes(c0, a, aa, 5)]
            same = same and without == with_
            tried += 1
    results.append(("the labelling pass-throughs change nothing turn_outcomes finds", same and tried >= 10,
                    f"{tried} turns"))


def check_reload(results, line):
    """A saved line reloads to the same tree: every position replayed from
    its checks' recorded outcomes is the position saved."""
    path = line.save()
    again, diffs = lt.load(path)
    same = len(again.nodes) == len(line.nodes) and all(
        lt.fingerprint(again.nodes[k].b) == lt.fingerprint(line.nodes[k].b) for k in line.nodes)
    text = again.transcript()
    results.append(("a saved line reloads to the same tree, and exports as a transcript",
                    not diffs and same and text.count("turn ") >= 10,
                    f"{len(line.nodes)} positions, differences {diffs[:2]}"))


def check_calc_route(results, line):
    """What the calculator's Fight button sends becomes the same battle: its
    sets as records keeping their IVs and EVs, against the fight its trainer
    id names, a rival's id naming its own variant."""
    from ..balance import data as bdata
    blob = fs.calc.blob()["poks"]
    held = [m.item for m in line.node(0).b.p.mons]
    party = []
    for (const, moves), item in zip(SIX, held):
        name = plteam.species_name(const)
        party.append({"species": name, "level": 26, "nature": "Hardy", "ability": blob[name]["abilities"]["0"],
                      "item": item, "moves": moves, "ivs": {k: 15 for k in ("hp", "at", "df", "sa", "sd", "sp")},
                      "evs": {k: 0 for k in ("hp", "at", "df", "sa", "sd", "sp")}})
    gardenia = next(f for f in bdata.fights()["fights"] if f["key"] == "gardenia")
    s = lt.setup_from_calc({"party": party, "trainer": {"tr_id": gardenia["tr_ids"][0]}})
    calc_line = lt.Line(s, name="test-calc")
    a, b = calc_line.node(0).b, line.node(0).b
    same = all((x.species, x.maxhp, x.stats, x.ability, x.item, [m.name for m in x.moves])
               == (y.species, y.maxhp, y.stats, y.ability, y.item, [m.name for m in y.moves])
               for x, y in zip(a.p.mons + a.b.mons, b.p.mons + b.b.mons))
    rivals = [f for f in bdata.fights()["fights"] if len(f["tr_ids"]) > 1]
    variants = all(lt.fight_of_trainer(t) == (f["key"], i) for f in rivals[:4] for i, t in enumerate(f["tr_ids"]))
    results.append(("the calculator's party and trainer id make the same battle as the records, and a rival's id "
                    "names its own variant", same and s["fight"] == "gardenia" and variants and len(rivals) >= 2,
                    f"{len(rivals)} fights with variants"))


def check_branch(results):
    """A trainer read from a branch with git show: here the tree's own
    commit, so the fight must come out as the tree's own."""
    recs = setup()["records"]
    here = lt.prepare_fight("gardenia", recs)
    there = lt.prepare_fight("gardenia", recs, branch="HEAD")
    keys = here["variants"][0][0]
    same = keys == there["variants"][0][0] and all(
        here["st"]["pokemon"][k] == there["st"]["pokemon"][k] and here["st"]["moves"][k] == there["st"]["moves"][k]
        for k in keys) and here["variants"][0][1] == there["variants"][0][1]
    results.append(("a trainer read from a branch (here HEAD) comes out as the tree's own",
                    same, f"{len(keys)} Pokemon"))


def main():
    folder = tempfile.mkdtemp(prefix="oxide-lines-test-")
    lt.LINES = folder
    lt.install()
    results = []
    try:
        rng = random.Random(20261021)
        line = build_line(rng)
        check_ai_odds(results, line)
        check_overview(results, line)
        check_follow(results, line, rng)
        check_pins(results, line)
        check_labels(results, line)
        check_pass_through(results, line)
        check_reload(results, line)
        check_calc_route(results, line)
        check_branch(results)
    finally:
        shutil.rmtree(folder, ignore_errors=True)
    width = max(len(label) for label, _ok, _note in results)
    failed = 0
    for label, ok, note in results:
        failed += not ok
        print(f"  {'ok  ' if ok else 'FAIL'}  {label:{width}}  {note}")
    print(f"\n{len(results) - failed}/{len(results)} passed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())

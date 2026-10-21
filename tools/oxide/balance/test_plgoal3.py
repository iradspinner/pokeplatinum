"""Goal 3's driver (plgoal3): the fights it reads, the team each box's
starter meets, the levels rule of Ian's answers of 2026-10-07, the boxes
and their cut at a fight's place, and the pooling into the store's shape.

    PYTHONPATH=. python3 -m tools.oxide.balance.test_plgoal3
"""
import contextlib
import io
import itertools
import json
import os
import sys
import tempfile

import numpy as np

from . import fightsim as fs, plgoal3 as g, plteam as pt, pool


def old_score_sixes(M, size=6, depth=0.3, hole=2.0):
    """plteam.score_sixes as it was before 2026-10-20, every six held at once."""
    n = M.shape[0]
    combos = np.array(list(itertools.combinations(range(n), min(size, n))))
    out = []
    for lo in range(0, len(combos), 50000):
        c = combos[lo:lo + 50000]
        m = M[c]
        top = np.sort(m, axis=1)
        best, second = top[:, -1, :], top[:, -2, :] if m.shape[1] > 1 else np.zeros_like(top[:, -1, :])
        s = (np.clip(best, -3, 3) + depth * np.clip(second, 0, 3)).sum(1) - hole * (best <= 0).sum(1)
        out += list(zip(s.tolist(), [tuple(x) for x in c.tolist()]))
    out.sort(key=lambda t: -t[0])
    return out


def use_of(rec, f, lvl):
    """A reading's use of this member at fight f (plgoal3.uses' form)."""
    return g.uses({"pokemon": {"p0": rec}}, ["p0"], f, lvl)[0]


def holds_checks(by):
    """Held-back versions (Ian, 2026-10-15): the delays a box offers, rules
    A and B on hand-built cases, the play order the seeds read in, and the
    team search never taking two versions of one catch."""
    out = []
    starly = [g.Catch("SPECIES_STARLY", "Roark", 1, "Route 201")]
    may, fan, wake = by["maylene"], by["fantina"], by["wake"]

    def held(b):
        return [r["label"] for r in b["records"] if r["held"]]

    # The delay: only a Starly held back has Brave Bird by Maylene's split.
    b = g.box(starly, may, 39, 1)
    out.append(("a Starly is offered held back at Maylene, with Brave Bird",
                held(b) == ["Staraptor (Starly held to 37)"]
                and "Brave Bird" in b["records"][1]["moves"] and "Brave Bird" not in b["records"][0]["moves"]
                and b["records"][0]["catch"] == b["records"][1]["catch"], str(held(b))))
    out.append(("no hold is offered where it brings no strong move by the fight (Fantina at 33)",
                held(g.box(starly, fan, 33, 1)) == [], str(held(g.box(starly, fan, 33, 1)))))
    # Of two holds that bring the same moves, the shorter: Staravia held to
    # 43 (9 levels past 34) before Starly held to 37 (23 past 14) at Wake.
    out.append(("of holds bringing the same moves the shortest is offered",
                held(g.box(starly, wake, 44, 1)) == ["Staraptor (Staravia held to 43)"],
                str(held(g.box(starly, wake, 44, 1)))))
    hm, pt.HOLD_MIN = pt.HOLD_MIN, 30
    try:
        short = held(g.box(starly, may, 39, 1))
    finally:
        pt.HOLD_MIN = hm
    out.append(("a wait under HOLD_MIN levels past the evolution is no delay", short == [], str(short)))
    out.append(("an Ace Trainer's box (holds off) offers none", held(g.box(starly, may, 39, 1, holds=False)) == [],
                "on time only"))

    # Rule A: a catch used evolved at an earlier fight is not offered held
    # back later, and the hold is listed, not modelled.
    on_time = g.box(starly, fan, 33, 1)["records"][0]
    hist = {"Route 201": [use_of(on_time, fan, 33)]}
    b = g.box(starly, may, 39, 1, hist)
    out.append(("rule A: Starly used as a Staravia at Fantina is not offered held back at Maylene",
                held(b) == [] and [(h["label"], h["used_at"], h["used_as"]) for h in b["ruled_out"]]
                == [("Staraptor (Starly held to 37)", "fantina", "Staravia")],
                f"{held(b)}; ruled out {[(h['label'], h['used_at']) for h in b['ruled_out']]}"))
    # Used before it could evolve, it is no evolved form: the hold stays open.
    young = g.box(starly, by["barry_2"], 11, 1)["records"][0]
    b = g.box(starly, may, 39, 1, {"Route 201": [use_of(young, by["barry_2"], 11)]})
    out.append(("rule A: a Starly used at level 11, before it evolves, can still be held back later",
                held(b) == ["Staraptor (Starly held to 37)"] and not b["ruled_out"], str(held(b))))
    # Used on time at Fantina as a Staravia, it may still be held as a
    # Staravia: Staravia held to 43 keeps Fantina's form at 33.
    b = g.box(starly, wake, 44, 1, hist)
    out.append(("rule A: a hold that keeps the earlier fight's form stays open (Staravia to 43 after Fantina)",
                held(b) == ["Staraptor (Staravia held to 43)"], str(held(b))))

    # Rule B: a hold used at one fight carries to the next.
    held_rec = g.box(starly, may, 39, 1)["records"][1]
    b = g.box(starly, wake, 44, 1, {"Route 201": [use_of(held_rec, may, 39)]})
    recs = b["records"]
    out.append(("rule B: a Starly held to 37 at Maylene is the same Staraptor at Wake, never on time",
                [(r["label"], r["held"], r["hold"]) for r in recs]
                == [("Staraptor (Starly held to 37)", False, {"SPECIES_STARLY": 37})]
                and "Brave Bird" in recs[0]["moves"],
                str([(r["label"], r["held"]) for r in recs])))

    # The history a box is built from: the seed's earlier readings' chosen,
    # in play order, and none of a later fight or another seed.
    with tempfile.TemporaryDirectory() as tmp:
        keep, g.OUT = g.OUT, tmp
        try:
            for slug, seed, area in (("fantina", 1, "A"), ("wake", 1, "B"), ("fantina", 2, "C")):
                os.makedirs(g.box_dir("t", slug, seed))
                with open(os.path.join(g.box_dir("t", slug, seed), "result.json"), "w") as fh:
                    json.dump({"chosen": [{"area": area, "caught": "x"}]}, fh)
            hist, src = g.history("t", 1, "maylene")
        finally:
            g.OUT = keep
    out.append(("a box's history is its seed's earlier readings' choices", (sorted(hist), src) == (["A"], ["fantina"]),
                f"{sorted(hist)} from {src}"))

    # The order the seeds read in: the story path, each officer before the
    # commander of its place, every fight of a split before its closing one.
    order = g.play_order()
    at = {s: i for i, s in enumerate(order)}
    story = [x["key"] for x in g.data.fights()["fights"] if x["key"] in at]
    coronet = [s for s in order if s.startswith("galactic_grunt_mt_coronet") or s == "dummy_834"]
    ok = (story == sorted(story, key=at.get) and at["galactic_grunt_valley_windworks_3"] < at["mars_1"]
          and at["galactic_grunt_team_galactic_eterna_building_3f"] < at["jupiter_1"] < at["lucas_dawn_2"]
          and all(at[s] < at["cyrus_3"] for s in coronet) and len(order) == len(g.fights())
          and all(at[f["slug"]] < at[pool.CLOSING[f["split"]]] for f in g.fights()
                  if not f["story"] and pool.CLOSING[f["split"]] in at))
    out.append(("the play order: the story path, officers before their commanders and their split's close", ok,
                " > ".join(order[:8]) + " ..."))
    # The scheduler: a box waits on its seed's earlier bosses and, for a
    # later box, its fight's first box, whose networks it reuses.
    todo = g.jobs(None, ("boss", "ace"), g.SEEDS)
    w = g.waits_on(("maylene", 2), todo)
    ace = next(f["slug"] for f in g.fights() if f["kind"] == g.ACE and f["split"] == "Maylene")
    wa = g.waits_on((ace, 2), todo)
    out.append(("a box waits on its seed's earlier bosses and its fight's first box",
                ("fantina", 2) in w and ("maylene", 1) in w and ("fantina", 1) not in w
                and not any(by[s]["kind"] == g.ACE for s, _b in w) and (ace, 1) not in wa,
                f"{len(w)} for Maylene box 2"))

    # The team search never takes two versions of one catch, and its screen,
    # now drawn up a block at a time, gives the list the old one gave.
    rng = np.random.default_rng(7)
    M = np.clip(np.round(rng.normal(size=(12, 5)) * 2) / 2, -3, 3)   # half hits, so ties are many
    groups = [0, 0, 1, 2, 2, 2, 3, 4, 5, 6, 7, 8]
    whole = pt.score_sixes(M)
    grouped = pt.score_sixes(M, groups=groups)
    out.append(("the six screen gives the old screen's list, and its head with keep",
                whole == old_score_sixes(M) and pt.score_sixes(M, keep=40) == whole[:40], f"{len(whole)} sixes"))
    out.append(("the six screen never takes two versions of one catch",
                grouped == [t for t in whole if len({groups[i] for i in t[1]}) == 6], f"{len(grouped)} sixes"))
    keys = [f"p{i}" for i in range(12)]
    group = dict(zip(keys, groups))
    got = (pt.six_count(keys, 6, group), pt.round_size(keys, 1000, group), pt.spread_room(keys, [1] * 3, group),
           pt.take(["p0", "p1", "p2", "p3", "p4"], 3, group), pt.take(["p1", "p4", "p5"], 3, group, ["p3"]),
           pt.valid_six(["p0", "p1"], group), pt.six_count(keys, 6))
    out.append(("the race and the loop count and fill sixes one version a catch",
                got == (len(grouped), (6, len(grouped)), 5, ["p0", "p2", "p3"], ["p3", "p1"], False, 924)
                , str(got)))
    return out


def stubbed_read(run, slug, seed, screen_held):
    """read_box on a real box with the team search and the full reading
    stubbed, in a scratch output folder: (its result, the searches it ran).
    The stub's winner takes the box's held-back versions first; its screen
    shows them in a top six or not, as `screen_held` says; the first
    reading wins 90% of its fights, any later one 70%."""
    calls = []

    def search(fight, key, recs, stock, out_dir, procs=None, prepared=None, model=None, **_kw):
        st, keys, _bk, _fl = prepared
        group = pt.groups_of(st, keys)
        held = [k for k in keys if st["pokemon"][k].get("held")]
        names = {k: pt.member_name(st["pokemon"][k]) for k in keys}
        win = pt.take(held + [k for k in keys if k not in held], 6, group)
        top = win if screen_held else pt.take([k for k in keys if k not in held], 6, group)
        calls.append({"fight": fight, "held": len(held), "model": model})
        return {"winner_keys": win, "winner": [names[k] for k in win], "screen": [[names[k] for k in top]],
                "model": model or "networks-x"}

    def full_reading(st, boss_keys, flags, team, cfg, procs=None, **_kw):
        won = 0.9 if len(calls) == 1 else 0.7
        side = {"fights": 75, "won": won, "faints": 1.0, "clean": 0.5}
        return side, dict(side, fights=25), [(True, 1, False, [("Shinx", "Foe")])] * 75

    keep = g.OUT, g.plteam.search, g.plteam.full_reading, g.web_report
    with tempfile.TemporaryDirectory() as tmp:
        # The web report reads fights of its own where a six carries the
        # web; web_checks tests it, so here it is stubbed too.
        g.OUT, g.plteam.search, g.plteam.full_reading, g.web_report = (tmp, search, full_reading,
                                                                       lambda *_a, **_k: {"carried_by": []})
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                r = g.read_box(run, slug, seed, 1)
        finally:
            g.OUT, g.plteam.search, g.plteam.full_reading, g.web_report = keep
    return r, calls


def paired_checks():
    """The paired reading (Ian, 2026-10-15) on Lucas and Dawn 2's box 1,
    whose box offers Luxray (Shinx held to 29): read again without the
    held-back versions where the screen puts one in a top six, once where
    it puts none."""
    out = []
    r, calls = stubbed_read("t", "lucas_dawn_2", 1, True)
    pair = r.get("without_holds") or {}
    out.append(("a box whose screen holds a held-back version is read again without it, both kept",
                r["held_in_screen"] == ["Luxray (Shinx held to 29)"] and r["real"]["won"] == 0.9
                and pair.get("real", {}).get("won") == 0.7 and [c["held"] for c in calls] == [1, 0]
                and calls[1]["model"] == "networks-x" and "Luxray (Shinx held to 29)" not in pair["winner"],
                f"with {r['real']['won']:.0%}, without {pair.get('real', {}).get('won', 0):.0%}; searches "
                f"{[(c['fight'].rsplit('-', 2)[-1], c['held']) for c in calls]}"))
    out.append(("the reading's chosen six keeps its held-back member for the seed's later fights",
                r["held_used"] == ["Luxray (Shinx held to 29)"]
                and any(u["hold"] == {"SPECIES_SHINX": 29} and u["held"] for u in r["chosen"]),
                f"{len(r['chosen'])} chosen"))
    table = g.paired_table({"lucas_dawn_2": [r]}, {f["slug"]: f for f in g.fights()})
    out.append(("the summary puts both readings side by side",
                any("| Lucas and Dawn 2 | 1 | 90%, 1.00 | 70%, 1.00 | Luxray (Shinx held to 29) |" == t for t in table),
                table[-1] if table else "no table"))
    r, calls = stubbed_read("t", "lucas_dawn_2", 1, False)
    out.append(("a box whose screen holds none is read once", "without_holds" not in r and len(calls) == 1,
                f"{len(calls)} search"))
    return out


def web_checks():
    """The Sticky Web report (Ian, 2026-10-15): on a hand-built six whose
    Ariados carries the web, the fights it was laid in, the wins each way,
    and the check without it (stubbed) with its strongest other attack in
    its place; and, on a real Roark fight at a small budget, that keeping
    the moves chosen in each fight changes no fight's outcome."""
    out = []
    st = {"moves": {"p0": ["Sticky Web", "Bug Bite", "Poison Jab", "Shadow Sneak"], "p1": ["Tackle"]},
          "pokemon": {"p0": {"species": "Ariados", "moves": ["Sticky Web", "Bug Bite", "Poison Jab", "Shadow Sneak"]},
                      "p1": {"species": "Bidoof", "moves": ["Tackle"]}}}
    recs = [{"moves": ["Sticky Web", "Bug Bite", "Poison Jab", "Shadow Sneak", "Megahorn", "Night Shade"]},
            {"moves": ["Tackle"]}]
    real, unl = pt.Tally(), pt.Tally()
    for i in range(10):
        laid = i < 4
        real.add(("p0", "p1"), laid or i % 2 == 0, 1, False, [], ["Bug Bite"] + (["Sticky Web"] if laid else []))
    unl.add(("p0", "p1"), False, 2, False, [], ["Sticky Web"])
    seen = {}

    def read(st_, boss_keys, flags, teams, fights, cfg, procs=None, **_kw):
        seen["moves"] = list(st_["moves"]["p0"])
        t = pt.Tally()
        for i in range(fights):
            t.add(tuple(teams[0]), i % 2 == 0, 2, False, [])
        return t

    keep, g.plteam.read = g.plteam.read, read
    try:
        w = g.web_report(st, [], {}, ["p0", "p1"], [real, unl], recs, real.numbers(("p0", "p1")), 1, check=10)
    finally:
        g.plteam.read = keep
    out.append(("the reading reports the web's carriers, the fights it was laid in and the wins each way",
                w["carried_by"] == ["Ariados"] and w["real"] == {"fights": 10, "laid": 4, "won_laid": 4,
                                                                  "won_not_laid": 3}
                and w["unlucky"]["laid"] == 1, str({k: w[k] for k in ("carried_by", "real")})))
    out.append(("where the six carries it, it is read again without it, which says whether the wins lean on it",
                seen["moves"] == ["Bug Bite", "Poison Jab", "Shadow Sneak", "Megahorn"]
                and w["without"]["swapped"] == {"Ariados": "Megahorn"} and w["without"]["won"] == 0.5
                and w["leans"] and st["moves"]["p0"][0] == "Sticky Web",
                f"won {real.numbers(('p0', 'p1'))['won']:.0%} with it, {w['without']['won']:.0%} without"))
    w = g.web_report(st, [], {}, ["p1"], [real, unl], recs, real.numbers(("p0", "p1")), 1)
    out.append(("a six without it says so and reads nothing more", w == {"carried_by": []}, str(w)))

    # Keeping the chosen moves changes no fight's outcome.
    f = next(x for x in g.fights() if x["slug"] == "roark")
    recs = g.records(g.cut(g.roll("Roark", 1), f), f, 16, 1)
    key, v, _t = g.met(f, recs[0]["constant"])
    st, keys, boss_keys, flags = g.fight_state(key, recs, g.fs.player_items("Roark"), v, "roark")
    # Two members, so that the fights are short (they lose to Roark fast).
    team, cfg = keys[:2], {"budget": 2}
    pick = ("won", "deaths", "faints", "turns")
    plain = g.plteam.plplan.play(st, team, boss_keys, flags, 0, 5, cfg, "real")
    kept = g.plteam.plplan.play(st, team, boss_keys, flags, 0, 5, cfg, "real", record=[])
    with contextlib.redirect_stdout(io.StringIO()):
        t = pt.read(st, boss_keys, flags, [team], 1, cfg, procs=1, used=True)
    out.append(("keeping the moves chosen in each fight changes no fight's outcome",
                {k: plain[k] for k in pick} == {k: kept[k] for k in pick} and len(t.chose[tuple(team)]) == 1
                and t.chose[tuple(team)][0], f"{plain['turns']} turns; chose {t.chose[tuple(team)][0]}"))
    return out


def planned_checks():
    """The planned-box sample (Ian, 2026-10-15): the option adds the planning
    player's box to the four sample fights only, read in play order like a
    seed; its catches keep the planner's waits; it reads as any box does,
    and the summary shows it beside the random boxes, outside their pool."""
    out = []
    todo = g.jobs(None, ("boss",), g.SEEDS, True)
    planned = [slug for slug, s in todo if s == g.PLANNED]
    w = g.waits_on(("gardenia", g.PLANNED), todo)
    out.append(("the option adds the planned box to Mars 1, Gardenia, Maylene and Wake, read in play order",
                planned == list(g.PLANNED_FIGHTS) and ("mars_1", g.PLANNED) in w and ("gardenia", 1) in w
                and not any(s == g.PLANNED for _x, s in g.jobs(None, ("boss",), g.SEEDS))
                and g.box_dir("t", "wake", g.PLANNED).endswith("boxplanned"), f"{planned}; Gardenia waits on {w}"))
    plan = g.planned("Gardenia")
    waited = [c for c in plan[1:] if c.place is None]
    by = {f["slug"]: f for f in g.fights()}
    mars, gard = g.cut(plan, by["mars_1"]), g.cut(plan, by["gardenia"])
    out.append(("the planned box keeps the planner's waits: a catch it came back for is made at its split's end",
                plan[0].split is None and waited and all(c.split == "Gardenia" for c in waited)
                and not set(waited) & set(mars) and set(waited) <= set(gard) and len(gard) == len(plan),
                f"{len(plan)} catches, {len(waited)} waited for: {', '.join(c.area for c in waited)}"))
    r, calls = stubbed_read("t", "mars_1", g.PLANNED, False)
    out.append(("a planned box reads as any box does", r["seed"] == g.PLANNED and len(calls) == 1
                and len(r["box"]) == len(mars) and r["chosen"], f"{len(r['box'])} members, starter {r['starter']}"))
    with tempfile.TemporaryDirectory() as tmp:
        keep, g.OUT = g.OUT, tmp
        try:
            for seed, res in ((1, dict(r, seed=1, real=dict(r["real"], won=0.5))), (g.PLANNED, r)):
                os.makedirs(g.box_dir("t", "mars_1", seed))
                with open(os.path.join(g.box_dir("t", "mars_1", seed), "result.json"), "w") as fh:
                    json.dump(res, fh)
            pooled = g.results("t")
            table = g.planned_table("t", by)
        finally:
            g.OUT = keep
    out.append(("the summary shows the planned box beside the random boxes, which alone are pooled",
                [x["seed"] for x in pooled["mars_1"]] == [1]
                and any(t.startswith("| Mars 1 |") and "| 90% |" in t and "| 50% |" in t for t in table),
                table[-1] if table else "no table"))
    return out


def search_checks():
    """The team search on a real box with held-back versions (Maylene's box
    1, which offers six), its fights stubbed: the screen's sixes, the
    race's draws and the loop's candidates never take two versions of one
    catch."""
    s = g.setup("t", "maylene", 1)
    recs = s["built"]["records"]
    st, keys, boss_keys, flags = g.fight_state(s["key"], recs, s["stock"], s["v"], "maylene")
    sixes, _scores, M, _moves = pt.screen(st, keys, boss_keys)
    group = pt.groups_of(st, keys)
    seen = []
    rng = __import__("random").Random(3)

    def read(st_, bk, fl, teams, fights, cfg, luck="real", seed0=0, procs=None, tally=None, used=False):
        tally = tally or pt.Tally()
        for t in teams:
            seen.append(tuple(t))
            for _i in range(fights):
                tally.add(tuple(t), rng.random() < 0.6, rng.randrange(3), False,
                          [(st_["pokemon"][t[0]]["species"], st_["pokemon"][bk[0]]["species"])])
        return tally

    keep, pt.read = pt.read, read
    try:
        _cands, po, _w = pt.race(st, keys, boss_keys, flags, sixes, {}, rounds=2, log=lambda *_a: None)
        best = max(po.rows, key=po.score)
        pt.improve(st, keys, boss_keys, flags, M, best, po, check=2, log=lambda *_a: None)
    finally:
        pt.read = keep
    bad = [t for t in sixes + seen if not pt.valid_six(t, group)]
    held = sum(any(st["pokemon"][k]["held"] for k in t) for t in seen)
    return [("the screen, the race and the loop never take two versions of one catch (Maylene's box 1)",
             not bad and held > 0 and len(set(seen)) > 16,
             f"{len(set(seen))} sixes read, {held} with a held-back version; {len(bad)} with two of one catch")]


def main():
    results = []
    rows = g.fights()
    bosses = [f for f in rows if f["kind"] != g.ACE]
    aces = [f for f in rows if f["kind"] == g.ACE]
    results.append(("goal 3 reads its 80 single battles: 39 bosses and 41 Ace Trainers",
                    (len(bosses), len(aces)) == (39, 41), f"{len(bosses)} bosses, {len(aces)} Ace Trainers"))

    # The team each starter meets: Barry's slots by the player's starter
    # (Scorbunny meets the _CHIMCHAR slot), Lucas and Dawn's by the
    # counterpart's line (it carries the starter weak to the player's).
    by = {f["slug"]: f for f in rows}
    got = {sp: g.met(by["barry_2"], sp)[2]["constant"].rsplit("_", 1)[-1]
           for sp in ("SPECIES_TURTWIG", "SPECIES_SCORBUNNY", "SPECIES_PIPLUP", "SPECIES_CHIMCHAR")}
    results.append(("a rival meets each starter with its own slot, Scorbunny's the _CHIMCHAR one",
                    got == {"SPECIES_TURTWIG": "TURTWIG", "SPECIES_SCORBUNNY": "CHIMCHAR", "SPECIES_PIPLUP": "PIPLUP",
                            "SPECIES_CHIMCHAR": "CHIMCHAR"}, str(got)))
    lines = {"SPECIES_TURTWIG": "Prinplup", "SPECIES_SCORBUNNY": "Grotle", "SPECIES_PIPLUP": "Monferno"}
    got = {sp: [m["species"] for m in g.met(by["lucas_dawn_2"], sp)[2]["party"]] for sp in lines}
    results.append(("Lucas and Dawn meet each starter with the line weak to it",
                    all(lines[sp] in party for sp, party in got.items()), str(got)))

    # The levels rule.
    bad = []
    for f in rows:
        _k, _v, t = g.met(f, "SPECIES_TURTWIG")
        lvl, cap = g.level(f, t), pool.caps()[f["split"]]
        if g.closes(f):
            want = fs.fight_cap(f["split"], f["story"])
        elif f["kind"] != g.ACE:
            want = min(g.ace([t]), cap)
        else:
            want = None
        if (want is not None and lvl != want) or lvl > cap:
            bad.append(f"{f['slug']} {lvl} (want {want}, cap {cap})")
    results.append(("closing fights at the cap, the Elite Four at their aces, other bosses at their ace",
                    not bad, "; ".join(bad[:5]) or f"{len(rows)} fights"))
    e4 = {k: g.level(by[k], g.met(by[k], "SPECIES_TURTWIG")[2]) for k in ("aaron", "lucian", "cynthia")}
    results.append(("the Elite Four's levels are their aces", e4 == {"aaron": 72, "lucian": 75, "cynthia": 78},
                    str(e4)))
    falls = []
    for f in aces:
        lvl = g.level(f, g.met(f, "SPECIES_TURTWIG")[2])
        i = pool.SPLITS.index(f["split"])
        if i and lvl < pool.caps()[pool.SPLITS[i - 1]]:
            falls.append(f"{f['slug']} {lvl}")
    results.append(("no Ace Trainer is read below the split before's cap", not falls, ", ".join(falls) or "none"))

    # Places: a revisited zone takes its split's start, or its split's own
    # area of that name.
    p = {k: g.place(k) for k in ("mars_2", "saturn_2", "mars_1", "galactic_grunt_mt_coronet_6f")}
    results.append(("a fight in a revisited zone takes its split's start or own area of that name",
                    p["mars_2"] == g.START and p["saturn_2"] == g.START and p["mars_1"] not in (None, g.START)
                    and p["galactic_grunt_mt_coronet_6f"] >= min(o for o, _n in g.own_areas("Galactic")), str(p)))

    # The boxes.
    starters = [g.roll("Gardenia", s)[0].species for s in g.SEEDS]
    pool_ = g.pboxes.context("Gardenia")["starter_src"]["pool"]
    results.append(("box k's starter is the k-th in turn", starters == [pool_[(s - 1) % 3] for s in g.SEEDS],
                    str(starters)))
    whole = g.roll("Gardenia", 1)
    mars, gardenia = g.cut(whole, by["mars_1"]), g.cut(whole, by["gardenia"])
    rank = g.pboxes.context("Gardenia")["rank"]
    obeys = all(c.split is None or rank[c.split] < rank["Gardenia"] or (c.place is not None and c.place <= 20)
                for c in mars)
    results.append(("Mars 1's box is Gardenia's cut at Valley Windworks, the starter kept",
                    len(gardenia) == len(whole) and set(mars) <= set(whole) and mars[0] == whole[0] and obeys
                    and len(mars) < len(whole),
                    f"{len(mars)} of {len(whole)}: {', '.join(c.species[8:].title() for c in mars)}"))
    recs = g.records(mars, by["mars_1"], 19, 1)
    results.append(("a box's members stand at the fight's level, each with a gender and a move pool",
                    all(r["level"] == 19 and "gender" in r and r["moves"] for r in recs),
                    ", ".join(f"{r['species']} {r['gender']}" for r in recs)))

    # One run per seed (Ian, 2026-10-15): every fight of a seed draws on the
    # same catches, so an area gives one Pokemon all game. Until then
    # Gardenia's and Maylene's seed 1 agreed on 17 of 25 areas' catches.
    clash = []
    for s in g.SEEDS:
        seen = {}
        for f in rows:
            for c in g.cut(g.roll(f["split"], s), f):
                if seen.setdefault(c.area, c.species) != c.species:
                    clash.append(f"seed {s} {c.area}: {seen[c.area]} and {c.species} ({f['slug']})")
    results.append(("a seed's catches agree across all its fights", not clash, "; ".join(clash[:3]) or
                    f"{len(rows)} fights on seeds {', '.join(map(str, g.SEEDS))}"))
    gard = {c.area: c.species for c in g.cut(g.roll("Gardenia", 1), by["gardenia"])}
    may = {c.area: c.species for c in g.cut(g.roll("Maylene", 1), by["maylene"])}
    agree = sum(may.get(a) == sp for a, sp in gard.items())
    results.append(("Gardenia's and Maylene's seed 1 agree on every area Gardenia's box has",
                    agree == len(gard) and set(gard) <= set(may), f"{agree} of {len(gard)}"))
    # The box sizes over 20 seeds hold the Overseer's measure of 2026-10-15
    # (boxsizes.py's first-visit mode), the per-split rolls' sizes.
    want = {"roark": 17.0, "mars_1": 21.0, "gardenia": 25.0, "jupiter_1": 27.0, "fantina": 34.0,
            "maylene": 41.0, "wake": 51.0}
    got = {k: round(sum(len(g.cut(g.roll(by[k]["split"], s), by[k])) for s in range(1, 21)) / 20, 1)
           for k in want}
    results.append(("one run per seed keeps the box sizes over 20 seeds", got == want, str(got)))

    results += holds_checks(by)
    results += search_checks()
    results += paired_checks()
    results += web_checks()
    results += planned_checks()

    got = {k: sorted(g.places(by[k])) for k in ("mars_1", "gardenia", "jupiter_1", "fantina", "candice")}
    # Mt. Coronet 1F North Room 1, off Route 211, is the first magnetic map.
    want = {"mars_1": [], "gardenia": ["LEVEL_MAGNETIC_FIELD", "LEVEL_MOSS_ROCK"],
            "jupiter_1": ["LEVEL_MAGNETIC_FIELD", "LEVEL_MOSS_ROCK"],
            "fantina": ["LEVEL_MAGNETIC_FIELD", "LEVEL_MOSS_ROCK"],
            "candice": ["LEVEL_ICE_ROCK", "LEVEL_MAGNETIC_FIELD", "LEVEL_MOSS_ROCK"]}
    results.append(("the place evolutions open where the walk reaches the engine's maps for them", got == want,
                    str(got)))

    # Evolutions that ask more than a level: personality, gender, stats.
    pt = g.plteam
    evo = {"Wurmple": {pt.chain("SPECIES_WURMPLE", 5, 20, coin=c)[-1][0] for c in (0, 1)},
           "Burmy": {pt.chain("SPECIES_BURMY", 10, 30, gender=s)[-1][0] for s in ("F", "M")},
           "Tyrogue": pt.chain("SPECIES_TYROGUE", 10, 30)[-1][0],
           "Nincada": pt.chain("SPECIES_NINCADA", 10, 30)[-1][0],
           "Eevee at the Moss Rock": pt.chain("SPECIES_EEVEE", 20, 21, places={"LEVEL_MOSS_ROCK"})[-1][0]}
    ok = (evo["Wurmple"] == {"SPECIES_BEAUTIFLY", "SPECIES_DUSTOX"} and evo["Burmy"] == {"SPECIES_WORMADAM",
          "SPECIES_MOTHIM"} and evo["Tyrogue"].startswith("SPECIES_HITMON") and evo["Nincada"] == "SPECIES_NINJASK"
          and evo["Eevee at the Moss Rock"] == "SPECIES_LEAFEON")
    results.append(("a box member takes its personality's, gender's, stats' and place's evolutions", ok, str(evo)))

    # One pair of networks per boss: a later box reuses the first box's.
    import json, os, tempfile
    with tempfile.TemporaryDirectory() as tmp:
        out, g.OUT = g.OUT, tmp
        try:
            os.makedirs(g.box_dir("t", "roark", g.SEEDS[0]))
            with open(os.path.join(g.box_dir("t", "roark", g.SEEDS[0]), "result.json"), "w") as fh:
                json.dump({"model": "team-x-s1+team-x-s2"}, fh)
            got = (g.first_box_model("t", "roark", g.SEEDS[0]), g.first_box_model("t", "roark", g.SEEDS[1]),
                   g.first_box_model("t", "gardenia", g.SEEDS[1]))
        finally:
            g.OUT = out
    results.append(("a boss's later boxes reuse its first box's networks, the first trains its own",
                    got == (None, "team-x-s1+team-x-s2", None), str(got)))

    # A small box: the race and the labels take what sixes it has.
    ks = [f"p{i}" for i in range(7)]
    got = (pt.round_size(ks, 16), pt.round_size(ks[:5], 16), pt.round_size([f"p{i}" for i in range(20)], 16),
           pt.spread_room(ks, [1]), pt.spread_room(ks, [1, 2, 3, 4, 5]), pt.spread_room(ks[:6], []))
    results.append(("a small box's race draws only the sixes it has, and the labels as many",
                    got == ((6, 7), (5, 1), (6, 16), 5, 2, 0), str(got)))

    # Pooling and the store's key.
    side = g.pool_side([{"won": 1.0, "clean": 1.0, "faints": 0.0, "fights": 15},
                        {"won": 0.5, "clean": 0.0, "faints": 2.0, "fights": 5}])
    results.append(("readings pool weighted by their fights", side == {"won": 0.875, "clean": 0.75, "faints": 0.5,
                                                                      "fights": 20}, str(side)))
    keys = (g.store_key(by["roark"], "TRAINER_LEADER_ROARK"), g.store_key(by["barry_2"], "TRAINER_RIVAL_ROUTE_203_PIPLUP"))
    results.append(("the store's key is the constant, or the story key of a fight with several",
                    keys == ("TRAINER_LEADER_ROARK", "barry_2"), str(keys)))

    width = max(len(r[0]) for r in results)
    failed = 0
    for label, ok, note in results:
        failed += not ok
        print(f"  {'ok  ' if ok else 'FAIL'}  {label:{width}}  {note}")
    print(f"\n{len(results) - failed}/{len(results)} passed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())

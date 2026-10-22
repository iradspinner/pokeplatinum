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


def hold_rule_checks(by):
    """Which holds count (Ian, 2026-10-21): by the Pokemon and the move, never
    a power threshold. His three examples are offered, a status move, a
    pivot and a coverage move, and the learnset rules' floor stays: a hold
    of one to four levels past the evolution is no delay."""
    out = []

    def held(b):
        return [(r["label"], r["moves"]) for r in b["records"] if r["held"]]

    def offers(b, label, move):
        on_time = b["records"][0]
        return any(lab == label and move in mv for lab, mv in held(b)) and move not in on_time["moves"]

    for sp, split, area, fight, lvl, label, move in (
            ("SPECIES_FLETCHLING", "Roark", "Route 202", "gardenia", 26, "Fletchinder (Fletchling held to 25)",
             "Will-O-Wisp"),
            ("SPECIES_POPPLIO", "Gardenia", "Popplio's trade", "byron", 53, "Primarina (Popplio held to 51)",
             "Flip Turn"),
            ("SPECIES_VENONAT", "Fantina", "Venonat's place", "maylene", 39, "Venomoth (Venonat held to 37)",
             "Zen Headbutt")):
        b = g.box([g.Catch(sp, split, 1, area)], by[fight], lvl, 1)
        out.append((f"Ian's example: {label} is offered for {move} at {by[fight]['name']}", offers(b, label, move),
                    str([lab for lab, _m in held(b)])))
    # Roost: Fletchling learns it at 20, four levels past its evolution at 16,
    # and Fletchinder only at 22, so at 21 it is a hold the floor turns down.
    fletchling = [g.Catch("SPECIES_FLETCHLING", "Roark", 1, "Route 202")]
    b = g.box(fletchling, by["gardenia"], 21, 1)
    hm, pt.HOLD_MIN = pt.HOLD_MIN, 4
    try:
        low = g.box(fletchling, by["gardenia"], 21, 1)
    finally:
        pt.HOLD_MIN = hm
    out.append(("a hold of one to four levels past the evolution is no delay (Fletchling for Roost at 21)",
                held(b) == [] and offers(low, "Fletchinder (Fletchling held to 20)", "Roost"),
                f"floor 5: {[lab for lab, _m in held(b)]}; floor 4: {[lab for lab, _m in held(low)]}"))
    return out


def holds_checks(by):
    """Held-back versions (Ian, 2026-10-15): the delays a box offers, rules
    A and B on hand-built cases, the play order the seeds read in, and the
    team search never taking two versions of one catch."""
    out = []
    starly = [g.Catch("SPECIES_STARLY", "Roark", 1, "Route 201")]
    may, fan, wake = by["maylene"], by["fantina"], by["wake"]

    def held(b):
        return [r["label"] for r in b["records"] if r["held"]]

    def rec(b, label):
        return next(r for r in b["records"] if r["label"] == label)

    # The delay: only a Starly held back has Brave Bird by Maylene's split.
    # Held to 33 it brings Agility, which a Staraptor learns only at 41.
    b = g.box(starly, may, 39, 1)
    bb = rec(b, "Staraptor (Starly held to 37)") if "Staraptor (Starly held to 37)" in held(b) else {"moves": []}
    out.append(("a Starly is offered held back at Maylene, for Agility and for Brave Bird",
                held(b) == ["Staraptor (Starly held to 33)", "Staraptor (Starly held to 37)"]
                and "Brave Bird" in bb["moves"] and "Brave Bird" not in b["records"][0]["moves"]
                and "Agility" in rec(b, "Staraptor (Starly held to 33)")["moves"]
                and "Agility" not in b["records"][0]["moves"]
                and len({r["catch"] for r in b["records"]}) == 1, str(held(b))))
    out.append(("no hold is offered where it brings nothing by the fight (Mars 1 at 19)",
                held(g.box(starly, by["mars_1"], 19, 1)) == [], str(held(g.box(starly, by["mars_1"], 19, 1)))))
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
                == [("Staraptor (Starly held to 33)", "fantina", "Staravia"),
                    ("Staraptor (Starly held to 37)", "fantina", "Staravia")],
                f"{held(b)}; ruled out {[(h['label'], h['used_at']) for h in b['ruled_out']]}"))
    # Used before it could evolve, it is no evolved form: the hold stays open.
    young = g.box(starly, by["barry_2"], 11, 1)["records"][0]
    b = g.box(starly, may, 39, 1, {"Route 201": [use_of(young, by["barry_2"], 11)]})
    out.append(("rule A: a Starly used at level 11, before it evolves, can still be held back later",
                held(b) == ["Staraptor (Starly held to 33)", "Staraptor (Starly held to 37)"]
                and not b["ruled_out"], str(held(b))))
    # Used on time at Fantina as a Staravia, it may still be held as a
    # Staravia: Staravia held to 43 keeps Fantina's form at 33.
    b = g.box(starly, wake, 44, 1, hist)
    out.append(("rule A: a hold that keeps the earlier fight's form stays open (Staravia to 43 after Fantina)",
                held(b) == ["Staraptor (Staravia held to 43)"], str(held(b))))

    # Rule B: a hold used at one fight carries to the next.
    held_rec = rec(g.box(starly, may, 39, 1), "Staraptor (Starly held to 37)")
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

    # The screen, drawn up a block at a time, gives the list the old one
    # gave; and a box without held versions (Gardenia's box 1 with its
    # holds left off) is screened exactly as the old screen did.
    rng = np.random.default_rng(7)
    M = np.clip(np.round(rng.normal(size=(12, 5)) * 2) / 2, -3, 3)   # half hits, so ties are many
    whole = pt.score_sixes(M)
    out.append(("the six screen gives the old screen's list, and its head with keep",
                whole == old_score_sixes(M) and pt.score_sixes(M, keep=40) == whole[:40], f"{len(whole)} sixes"))
    s = g.setup("t", "gardenia", 1)
    recs = g.box(s["caught"], s["f"], s["lvl"], 1, holds=False)["records"]
    st, keys, boss_keys, _fl = g.fight_state(s["key"], recs, s["stock"], s["v"], "gardenia")
    sixes, scores, Mg, _moves = pt.screen(st, keys, boss_keys)
    kept = []
    for sc, idx in old_score_sixes(Mg):
        if all(len(set(idx) - set(j)) >= 2 for _s, j in kept):
            kept.append((sc, idx))
        if len(kept) >= 20:
            break
    out.append(("a box without held versions is screened as before",
                not any(r["held"] for r in recs) and [[keys[i] for i in j] for _s, j in kept] == sixes
                and np.allclose([sc for sc, _j in kept], scores), f"{len(sixes)} top sixes of {len(keys)} members"))
    return out


def stubbed_read(run, slug, seed, screen_held, win_held=True):
    """read_box on a real box with the team search and the full reading
    stubbed, in a scratch output folder: (its result, the searches it ran).
    The stub's winner takes the box's held-back versions first, or none, as
    `win_held` says; its screen shows held versions in a top six or not, as
    `screen_held` says; the first reading wins 90% of its fights, any later
    one 70%."""
    calls = []

    def search(fight, key, recs, stock, out_dir, procs=None, prepared=None, model=None, **_kw):
        st, keys, _bk, _fl = prepared
        held = [k for k in keys if st["pokemon"][k].get("held")]
        names = {k: pt.member_name(st["pokemon"][k]) for k in keys}

        def six(ranked):
            """The first six of `ranked`, one version a catch."""
            out, seen = [], set()
            for k in ranked:
                if st["pokemon"][k]["catch"] not in seen and len(out) < 6:
                    out.append(k)
                    seen.add(st["pokemon"][k]["catch"])
            return out

        win = six(held + [k for k in keys if k not in held]) if win_held else six([k for k in keys if k not in held])
        top = six(held + [k for k in keys if k not in held]) if screen_held else six([k for k in keys if k not in held])
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
    """The paired reading (Ian, 2026-10-15, narrowed on 2026-10-21) on Lucas
    and Dawn 2's box 1, whose box offers Luxray (Shinx held to 29) among
    others: read again without the held-back versions only where the
    reading's chosen six uses one, whatever the screen's top sixes hold."""
    out = []
    r, calls = stubbed_read("t", "lucas_dawn_2", 1, False, True)
    pair = r.get("without_holds") or {}
    out.append(("a box whose chosen six uses a held version is read again without holds, both kept",
                "Luxray (Shinx held to 29)" in r["held_used"] and not r["held_in_screen"] and r["real"]["won"] == 0.9
                and pair.get("real", {}).get("won") == 0.7 and [c["held"] for c in calls] == [len(r["offered"]), 0]
                and calls[1]["model"] == "networks-x" and "Luxray (Shinx held to 29)" not in pair.get("winner", []),
                f"with {r['real']['won']:.0%}, without {pair.get('real', {}).get('won', 0):.0%}; searches "
                f"{[(c['fight'].rsplit('-', 2)[-1], c['held']) for c in calls]}"))
    out.append(("the reading's chosen six keeps its held-back member for the seed's later fights",
                "Luxray (Shinx held to 29)" in r["held_used"]
                and any(u["hold"] == {"SPECIES_SHINX": 29} and u["held"] for u in r["chosen"]),
                f"{len(r['chosen'])} chosen"))
    table = g.paired_table({"lucas_dawn_2": [r]}, {f["slug"]: f for f in g.fights()})
    out.append(("the summary puts both readings side by side, with the chosen six's held versions",
                any(t.startswith("| Lucas and Dawn 2 | 1 | 90%, 1.00 | 70%, 1.00 | ") and "Luxray (Shinx held to 29)" in t
                    for t in table) and any("chosen six" in t for t in table),
                table[-1] if table else "no table"))
    r, calls = stubbed_read("t", "lucas_dawn_2", 1, True, False)
    out.append(("a box whose chosen six uses none is read once, though its screen's top sixes hold some",
                "without_holds" not in r and len(calls) == 1 and r["held_in_screen"] and not r["held_used"],
                f"{len(calls)} search; {len(r['held_in_screen'])} held versions in the screen's top sixes"))
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


ELEKID_LINE = {"SPECIES_ELEKID", "SPECIES_ELECTABUZZ", "SPECIES_ELECTIVIRE"}


def held_back_checks(by):
    """The Veilstone Elekid stays out of every box (Ian, 2026-10-21, until he
    decides the gift's future): no random seed's box and no planned box at
    the fights after Veilstone holds the Elekid line, and leaving it out
    changes nothing else in the box."""
    out, found = [], []
    for slug in ("maylene", "wake", "byron"):
        f = by[slug]
        for s in g.SEEDS + ((g.PLANNED,) if slug in g.PLANNED_FIGHTS else ()):
            box = g.cut(g.roll(f["split"], s), f)
            found += [f"{slug} seed {s}: {c.species}" for c in box if c.species in ELEKID_LINE]
    out.append(("no box at Maylene, Wake or Byron offers the Veilstone Elekid or its evolutions",
                not found, "; ".join(found[:4]) or "seeds 1 to 3, and the planned box at Maylene and Wake"))
    for slug in ("byron", "maylene"):
        f = by[slug]
        with_it, without = {}, {}
        for s in g.SEEDS + (g.PLANNED,):
            without[s] = [(c.area, c.species) for c in g.cut(g.roll(f["split"], s), f)]
        keep = getattr(g.pboxes, "HELD_BACK", frozenset())
        caches = (g.run_of, g.roll, g.planned)
        try:
            g.pboxes.HELD_BACK = frozenset()
            for c in caches:
                c.cache_clear()
            for s in g.SEEDS + (g.PLANNED,):
                with_it[s] = [(c.area, c.species) for c in g.cut(g.roll(f["split"], s), f)]
        finally:
            g.pboxes.HELD_BACK = keep
            for c in caches:
                c.cache_clear()
        only = all([x for x in with_it[s] if x not in keep] == without[s] for s in with_it)
        dropped = all(any(x in keep for x in with_it[s]) for s in with_it)
        out.append((f"leaving the Elekid out of {f['name']}'s boxes changes nothing else",
                    only and dropped, f"{len(without[1])} catches in seed 1's box, the Elekid gone from each"))
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
    r, calls = stubbed_read("t", "mars_1", g.PLANNED, False, False)
    out.append(("a planned box reads as any box does", r["seed"] == g.PLANNED and len(calls) == 1
                and len(r["box"]) - len(r["offered"]) == len(mars) and r["chosen"],
                f"{len(r['box'])} members, starter {r['starter']}"))
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


def screen_score(M, rows):
    """The screen's score of one six (plteam.score_sixes' reckoning), from
    its members' rows of the margin table."""
    top = np.sort(M[rows], axis=0)
    return float((np.clip(top[-1], -3, 3) + 0.3 * np.clip(top[-2], 0, 3)).sum() - 2.0 * (top[-1] <= 0).sum())


def search_checks():
    """A catch's versions share one slot (Ian, 2026-10-21): on Maylene's box
    1 (41 catches, each held version beside its catch), the fights stubbed,
    the screen's top sixes differ from one another in two catches or more,
    and every six the screen, the race and the loop read takes one version
    of each of its catches, the one that gives that six the screen's best
    score. On a box of seven catches, one with a held version, the race
    counts seven sixes, not thirteen."""
    out = []
    s = g.setup("t", "maylene", 1)
    recs = s["built"]["records"]
    st, keys, boss_keys, flags = g.fight_state(s["key"], recs, s["stock"], s["v"], "maylene")
    sixes, _scores, M, _moves = pt.screen(st, keys, boss_keys)
    pos = {k: i for i, k in enumerate(keys)}
    catch = {k: st["pokemon"][k]["catch"] for k in keys}
    versions = {}
    for k in keys:
        versions.setdefault(catch[k], []).append(k)
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

    def best_of(team):
        return max(screen_score(M, [pos[k] for k in c]) for c in itertools.product(*(versions[catch[k]] for k in team)))

    teams = list(dict.fromkeys([tuple(t) for t in sixes] + seen))
    two = [t for t in teams if len({catch[k] for k in t}) < len(t)]
    worse = [t for t in teams if screen_score(M, [pos[k] for k in t]) < best_of(t) - 1e-9]
    close = [(a, b) for a, b in itertools.combinations(sixes, 2)
             if len({catch[k] for k in a} - {catch[k] for k in b}) < 2]
    held = sum(any(st["pokemon"][k]["held"] for k in t) for t in teams)
    out.append(("every six the screen, the race and the loop read takes its catches' best versions for it",
                not two and not worse and held > 0 and len(teams) > 16,
                f"{len(teams)} sixes, {held} with a held version; {len(worse)} not at their best versions, "
                f"{len(two)} with two of one catch"))
    out.append(("the screen's top sixes differ from one another in two catches or more", not close,
                f"{len(close)} pairs of its {len(sixes)} top sixes share five catches"))

    # Holds do not multiply the sixes: seven catches, one with a held
    # version, make seven sixes.
    ks = [f"p{i}" for i in range(8)]
    small = {"pokemon": {k: {"catch": "A" if k in ("p0", "p1") else k, "held": k == "p1", "species": "Bidoof"}
                         for k in ks}}
    m = np.clip(np.round(np.random.default_rng(5).normal(size=(8, 4)) * 2) / 2, -3, 3)
    try:
        sl = pt.Slots(small, ks, m)
        got = (len(sl.slots), pt.round_size(sl.slots, 100), pt.spread_room(sl.slots, []))
        team = sl.team(["p0", "p2", "p3", "p4", "p5", "p6"])
        best_ok = screen_score(m, [ks.index(k) for k in team]) >= max(
            screen_score(m, [ks.index(v), 2, 3, 4, 5, 6]) for v in ("p0", "p1")) - 1e-9
    except AttributeError as e:
        got, best_ok = str(e), False
    out.append(("a catch's versions share one slot: seven catches, one held version, make seven sixes",
                got == (7, (6, 7), 5) and best_ok, str(got)))
    return out


def playoff_checks():
    """The play-off (Ian, 2026-10-21, his option 1) on Gardenia's box 1,
    whose Will-O-Wisp Fletchinder, Swagger Luxio and Yawn Bibarel the screen
    drops as dominated, the fights stubbed. A race finalist is played with
    every other version of each member, one swap at a time, on the fights
    the race read it on; a swap scoring better by the race's tally is kept;
    where two win, their combination is played and kept if it holds. A held
    version plays with the moves its hold brings. A box without held
    versions plays no swap."""
    out = []
    s = g.setup("t", "gardenia", 1)
    recs = s["built"]["records"]
    st, keys, bk, fl = g.fight_state(s["key"], recs, s["stock"], s["v"], "gardenia")
    sixes, _sc, M, _mv = pt.screen(st, keys, bk)
    sl = pt.Slots(st, keys, M)
    key = {pt.member_name(st["pokemon"][k]): k for k in keys}
    wanted = {"Fletchinder (Fletchling held to 25)": "Will-O-Wisp", "Luxio (Shinx held to 25)": "Swagger",
              "Bibarel (Bidoof held to 25)": "Yawn"}
    held = [key[n] for n in wanted]
    dominated = all(k not in sl.cands[sl.slot_of[k]] for k in held)
    on_time = [sl.slot_of[k] for k in held]
    fin = tuple(sorted(on_time + [k for k in sixes[0] if sl.slot_of[k] not in on_time][:3], key=keys.index))
    played, moves = [], {}

    def play_jobs(st_, bk_, fl_, jobs, procs=None, tally=None):
        t = tally or pt.Tally()
        for team, seed, _cfg, luck, _used in jobs:
            names = {pt.member_name(st_["pokemon"][k]) for k in team}
            for k in team:
                moves[pt.member_name(st_["pokemon"][k])] = list(st_["moves"][k])
            fletch, bib = "Fletchinder (Fletchling held to 25)" in names, "Bibarel (Bidoof held to 25)" in names
            won = fletch or (bib and seed % 10 < 8) or seed % 10 < 5
            t.add(team, won, 0 if fletch and bib else 1, False, [], fight=(seed, luck))
            played.append((team, seed))
        return t

    keep = getattr(pt, "play_jobs", None)
    pt.play_jobs = play_jobs
    screen_four = {k: list(st["moves"][k]) for k in keys}
    left = None
    try:
        race = pt.Tally()
        for i in range(10):
            race.add(fin, i < 5, 1, False, [], fight=(100 + i, "real"))
        finalists, record = pt.playoff(st, bk, fl, [fin], race, {}, sl, log=lambda *_a: None)
        # Fix 3 (Ian, 2026-10-21): a version the play-off tried and did not
        # keep goes back to the screen's four.
        left = {pt.member_name(st["pokemon"][k]): st["moves"][k] for k in keys
                if k not in finalists[0] and st["moves"][k] != screen_four[k]}
        names = [pt.member_name(st["pokemon"][k]) for k in finalists[0]]
        none = pt.playoff(st, bk, fl, [fin], race, {}, pt.Slots({"pokemon": {k: dict(st["pokemon"][k], catch=k)
                                                                              for k in keys}}, keys, M),
                          log=lambda *_a: None)[0]
    except (AttributeError, TypeError) as e:
        names, record, none = [str(e)], [], None
    finally:
        pt.play_jobs = keep
    tried = {t for t, _s in played}
    swapped_in = {pt.member_name(st["pokemon"][k]) for t in tried for k in t} & set(wanted)
    out.append(("the play-off plays every held version of a finalist's members, the screen's dominated ones too",
                dominated and swapped_in == set(wanted) and all(s_ >= 100 and s_ < 110 for _t, s_ in played),
                f"dominated in the screen: {dominated}; swapped in {sorted(swapped_in)}; {len(tried)} sixes played"))
    out.append(("a held version plays with the move its hold brings",
                all(mv in moves.get(n, []) for n, mv in wanted.items()), str({n: moves.get(n) for n in wanted})))
    out.append(("two winning swaps are played together and kept where the combination holds",
                "Fletchinder (Fletchling held to 25)" in names and "Bibarel (Bidoof held to 25)" in names
                and "Luxio" in names and record and record[0].get("combined"), str(names)))
    out.append(("a box without held versions plays no swap", none == [fin] and len(played) == len(tried) * 10,
                str(none)))
    out.append(("on Gardenia's box 1 every version the play-off did not keep has the screen's four again",
                left == {}, str(left)))
    return out


def hold_move_checks():
    """The play-off's fix 1 (Ian, 2026-10-21): the box records which move each
    hold is for, the one its held stage learns at the hold's level, and the
    play-off's four put that move in, then the hold's other moves, never over
    the first two picks or a pick the hold itself brought. On Maylene's box 1
    the screen's picks for Sharpedo (Carvanha held to 38) already carry Take
    Down, which the old four overwrote with Agility; on her box 2 Liepard
    (Purrloin held to 36) gains three moves and the old four took the first
    two by name, leaving out Sucker Punch."""
    out = []
    for seed, label, move in ((1, "Sharpedo (Carvanha held to 38)", "Take Down"),
                              (2, "Liepard (Purrloin held to 36)", "Sucker Punch")):
        s = g.setup("t", "maylene", seed)
        st, keys, bk, _fl = g.fight_state(s["key"], s["built"]["records"], s["stock"], s["v"], "maylene")
        pt.screen(st, keys, bk)
        k = next(k for k in keys if pt.member_name(st["pokemon"][k]) == label)
        picks = list(st["moves"][k])
        four = pt.with_gain(st, k)
        brought = [m for m in picks[2:] if m in st["pokemon"][k]["gained"]]
        out.append((f"the play-off plays {label} with {move}, the move its hold is for",
                    st["pokemon"][k].get("hold_for") == [move] and move in four and four[:2] == picks[:2]
                    and all(m in four for m in brought),
                    f"for {st['pokemon'][k].get('hold_for')}; picks {picks}; plays {four}"))
    return out


def playoff_fix_checks():
    """The play-off's fixes 2 and 3 (Ian, 2026-10-21), on a made-up box with
    the fights stubbed. Two finalists share a catch whose held version gains
    three moves. A swap leading its finalist by one fight in 30 (3.3 points,
    under the race's tolerance) is luck and not kept; one leading by 5 fights
    in 30 is kept. After the play-off every version outside a kept six has
    the screen's four again, and the version tried for both finalists plays
    the same four both times."""
    out = []
    ks = [f"p{i}" for i in range(10)]
    catch = {"p1": "p0", "p3": "p2", "p9": "p8"}
    held = {"p1": (["Cut", "Pound", "Tackle", "Scratch"], ["Bite", "Growl", "Leer"], ["Leer"]),
            "p3": (["Cut", "Pound", "Tackle", "Scratch"], ["Bite"], ["Bite"]),
            "p9": (["Cut", "Pound", "Tackle", "Scratch"], ["Bite"], ["Bite"])}
    st = {"pokemon": {}, "moves": {}}
    for k in ks:
        picks, gained, why = held.get(k, (["Cut", "Pound", "Tackle", "Scratch"], [], []))
        st["pokemon"][k] = {"species": f"Mon{k}", "catch": catch.get(k, k), "held": k in held, "gained": gained,
                            "hold": {"X": 30} if k in held else {}, "label": f"Mon{k} (held)" if k in held else None,
                            "moves": list(picks)}
        if why:
            st["pokemon"][k]["hold_for"] = why
        st["moves"][k] = list(picks)
    screen = {k: list(v) for k, v in st["moves"].items()}
    sl = pt.Slots(st, ks)
    fin1 = ("p0", "p2", "p4", "p5", "p6", "p7")
    fin2 = ("p0", "p4", "p5", "p6", "p7", "p8")
    played = {}

    def play_jobs(st_, bk_, fl_, jobs, procs=None, tally=None):
        t = tally or pt.Tally()
        for team, seed, _cfg, luck, _used in jobs:
            if "p1" in team:
                played.setdefault(team, list(st_["moves"]["p1"]))
            wins = 16 if "p3" in team else 20 if "p9" in team else 15
            t.add(team, seed < wins, 1, False, [], fight=(seed, luck))
        return t

    race = pt.Tally()
    for fin in (fin1, fin2):
        for seed in range(30):
            race.add(fin, seed < 15, 1, False, [], fight=(seed, "real"))
    keep = pt.play_jobs
    pt.play_jobs = play_jobs
    try:
        after, _rec = pt.playoff(st, [], {}, [fin1, fin2], race, {}, sl, log=lambda *_a: None)
    finally:
        pt.play_jobs = keep
    out.append(("a swap leading its finalist by 3.3 points, under the tolerance, is not kept",
                fin1 in after and not any("p3" in t for t in after), str(after)))
    out.append(("a swap leading its finalist by more than the tolerance is kept",
                any("p9" in t for t in after), str(after)))
    kept = {k for t in after for k in t}
    left = {k: st["moves"][k] for k in ks if k not in kept and st["moves"][k] != screen[k]}
    out.append(("after the play-off every version outside a kept six has the screen's four", not left, str(left)))
    fours = list(played.values())
    out.append(("a version tried for two finalists plays the same four both times",
                len(fours) == 2 and fours[0] == fours[1] and "Leer" in fours[0], str(fours)))
    return out


def playoff_gap_checks():
    """The play-off's gap of 2026-10-21 (Ian: "Fix it now"), on a made-up box
    with the fights stubbed. Finalist 1 keeps a swap to p1, a held version
    whose hold brings Leer, so p1 keeps the play-off's four. Finalist 2
    carries p1 as a member, and the race read it with p1 on the screen's
    four. Every swap of finalist 2 must play p1 with that same four, or it
    is compared against a baseline that played other moves. The stub makes
    Leer worth seven fights in 30, so that a swap of finalist 2 playing p1
    with Leer leads its baseline by Leer alone, and today is kept for it."""
    out = []
    ks = [f"p{i}" for i in range(10)]
    catch = {"p1": "p0", "p9": "p8"}
    held = {"p1": (["Cut", "Pound", "Tackle", "Scratch"], ["Leer"], ["Leer"]),
            "p9": (["Cut", "Pound", "Tackle", "Scratch"], ["Bite"], ["Bite"])}
    st = {"pokemon": {}, "moves": {}}
    for k in ks:
        picks, gained, why = held.get(k, (["Cut", "Pound", "Tackle", "Scratch"], [], []))
        st["pokemon"][k] = {"species": f"Mon{k}", "catch": catch.get(k, k), "held": k in held, "gained": gained,
                            "hold": {"X": 30} if k in held else {}, "label": f"Mon{k} (held)" if k in held else None,
                            "moves": list(picks)}
        if why:
            st["pokemon"][k]["hold_for"] = why
        st["moves"][k] = list(picks)
    screen = {k: list(v) for k, v in st["moves"].items()}
    sl = pt.Slots(st, ks)
    fin1 = ("p0", "p2", "p3", "p4", "p5", "p6")
    fin2 = ("p1", "p4", "p5", "p6", "p7", "p8")
    # p1's moves in every fight of a six that carries it: the race's and each swap's.
    p1_moves = {}

    def play_jobs(st_, bk_, fl_, jobs, procs=None, tally=None):
        t = tally or pt.Tally()
        for team, seed, _cfg, luck, _used in jobs:
            leer = "p1" in team and "Leer" in st_["moves"]["p1"]
            if "p1" in team:
                p1_moves.setdefault(team, list(st_["moves"]["p1"]))
            t.add(team, seed < (22 if leer else 15), 1, False, [], fight=(seed, luck))
        return t

    keep = pt.play_jobs
    pt.play_jobs = play_jobs
    try:
        # The race, played by the same stub on the screen's fours.
        race = pt.play_jobs(st, [], {}, [(fin, seed, {}, "real", False) for fin in (fin1, fin2) for seed in range(30)])
        baseline = p1_moves[fin2]
        after, rec = pt.playoff(st, [], {}, [fin1, fin2], race, {}, sl, log=lambda *_a: None)
    finally:
        pt.play_jobs = keep
    gain = pt.with_gain(st, "p1", screen["p1"])
    # Finalist 2's swaps that keep p1: the sixes with p7, which finalist 1 lacks.
    swaps2 = {t: m for t, m in p1_moves.items() if t != fin2 and "p7" in t}
    out.append(("finalist 1 keeps its swap to the held p1, which keeps the play-off's four",
                after[0] == tuple(sorted(("p1",) + fin1[1:], key=ks.index)) and st["moves"]["p1"] == gain,
                f"{after[0]}; p1 plays {st['moves']['p1']}"))
    out.append(("every swap of finalist 2 plays p1 with the four its race baseline played",
                swaps2 and all(m == baseline for m in swaps2.values()),
                f"baseline {baseline}; swaps {sorted(swaps2.items())}"))
    out.append(("no swap of finalist 2 is kept for the moves its baseline lacked",
                fin2 in after and len(after) == 2, f"{after}; swap scores {rec[1]['swaps'] if len(rec) > 1 else rec}"))
    kept = {k for t in after for k in t}
    left = {k: st["moves"][k] for k in ks if k not in kept and st["moves"][k] != screen[k]}
    out.append(("after it every version outside a kept six has the screen's four", not left, str(left)))
    return out


def on_time_checks():
    """The screen's fix 4 (Ian, 2026-10-21): the on-time version of a catch is
    never dropped as dominated, so where a held version is better against
    one enemy only and another member already answers it, the six scores
    the same either way and takes the version on time; where the held
    version raises the six's score, it is taken. On Wake's box 2 no top six
    takes a held version whose catch on time scores the same in its place
    (Cinderace held as Raboot to 44 was in 12 such sixes)."""
    out = []
    ks = [f"q{i}" for i in range(7)]
    small = {"pokemon": {k: {"catch": "A" if k in ("q0", "q1") else k, "held": k == "q1", "species": "Bidoof"}
                         for k in ks}}
    rest = [[0.0, 3.0], [0.5, 0.5], [0.5, 0.5], [0.5, 0.5], [0.5, 0.5]]
    tie = pt.Slots(small, ks, np.array([[2.0, 0.0], [2.0, 0.5]] + rest))
    gain = pt.Slots(small, ks, np.array([[2.0, 0.0], [2.0, 1.0]] + rest))
    six = ["q0", "q2", "q3", "q4", "q5", "q6"]
    out.append(("a held version equal in the six gives way to the catch on time, a better one is taken",
                "q0" in tie.team(six) and "q1" in gain.team(six), f"tie {tie.team(six)}; gain {gain.team(six)}"))

    s = g.setup("t", "wake", 2)
    st, keys, bk, _fl = g.fight_state(s["key"], s["built"]["records"], s["stock"], s["v"], "wake")
    sixes, scores, M, _mv = pt.screen(st, keys, bk)
    sl = pt.Slots(st, keys, M)
    on_time = {sl.slot_of[k]: next(v for v in sl.versions[sl.slot_of[k]] if not st["pokemon"][v]["held"])
               for k in keys}
    equal = []
    for t, sc in zip(sixes, scores):
        for k in t:
            if st["pokemon"][k]["held"]:
                alt = [on_time[sl.slot_of[k]] if x == k else x for x in t]
                if float(pt.score_rows(M[[sl.pos[x] for x in alt]])) >= sc - 1e-9:
                    equal.append(pt.member_name(st["pokemon"][k]))
    out.append(("Wake's box 2: no top six takes a held version its catch on time equals",
                not equal, f"{len(equal)} such: {sorted(set(equal))}"))
    return out


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
    # (boxsizes.py's first-visit mode), the per-split rolls' sizes, less the
    # Veilstone Elekid from Maylene's split on (held out since 2026-10-21;
    # held_back_checks).
    want = {"roark": 17.0, "mars_1": 21.0, "gardenia": 25.0, "jupiter_1": 27.0, "fantina": 34.0,
            "maylene": 40.0, "wake": 50.0}
    got = {k: round(sum(len(g.cut(g.roll(by[k]["split"], s), by[k])) for s in range(1, 21)) / 20, 1)
           for k in want}
    results.append(("one run per seed keeps the box sizes over 20 seeds", got == want, str(got)))

    results += hold_rule_checks(by)
    results += holds_checks(by)
    results += search_checks()
    results += paired_checks()
    results += web_checks()
    results += planned_checks()
    results += held_back_checks(by)
    results += playoff_checks()
    results += hold_move_checks()
    results += playoff_fix_checks()
    results += playoff_gap_checks()
    results += on_time_checks()

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

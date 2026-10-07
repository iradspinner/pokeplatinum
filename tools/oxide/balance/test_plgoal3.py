"""Goal 3's driver (plgoal3): the fights it reads, the team each box's
starter meets, the levels rule of Ian's answers of 2026-10-07, the boxes
and their cut at a fight's place, and the pooling into the store's shape.

    PYTHONPATH=. python3 -m tools.oxide.balance.test_plgoal3
"""
import sys

from . import fightsim as fs, plgoal3 as g, pool


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

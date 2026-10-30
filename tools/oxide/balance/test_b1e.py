"""B1e acceptance, as far as it goes without Ian: required trainers.

    PYTHONPATH=. python3 -m tools.oxide.balance.test_b1e

The plan's check has two halves. The story fights come out required: they
are started by scripts, which this model does not read, so they are
required by definition and not tested here. And a handful of route
trainers Ian knows to be avoidable come out avoidable: that list is his
to give (docs/oxide/balance-plan.md, open questions). Until then this
file checks the mechanics against cases traced by hand.
"""
import sys

from . import data
from . import pool
from . import required as R

# Totals at each trainer's first crossing, pinned so that a change to the
# maps, the table or the model shows up here. 36 required on 2026-09-23; 40
# since Test.nds became the base ROM (2026-09-25), whose moved trainers make
# one more required in Gardenia's split (the Valley Windworks building) and
# three more in Wake's (Routes 214 and 215). 50 since 2026-10-29, when ten
# trainers moved onto the story path for Ian's dozen mandatory fights a
# split, three in Fantina's and seven in Maylene's
# (docs/oxide/mandatory-fights.md); 52 once Black Belt Derek and Twins Teri
# and Tia joined them the same day, after Ian ruled that spinners are optional.
TOTALS = {"required": 52, "avoidable": 119, "never reached": 12}


def check_crossings_resolve(results):
    """Every crossing's two ends exist, and they connect when no trainer is
    in the way."""
    bad = []
    for split, header, src, dst in R.CROSSINGS:
        try:
            verdicts = R.crossing(split, header, src, dst)
        except (ValueError, StopIteration) as e:
            bad.append(f"{header}: {e}")
            continue
        if any(v == "no path" for _t, v in verdicts):
            bad.append(f"{header} ({split}): no path")
    results.append(("every crossing's ends exist and connect", not bad,
                    f"{len(R.CROSSINGS)} crossings" + (f"; {bad}" if bad else "")))


def check_sight_and_ledges(results):
    """Tristan on Route 202 looks south with a range of 5 and sees exactly
    the five tiles below him; a Route 202 ledge can be jumped down and not
    climbed."""
    f = R.Field("ROUTE_202", "Roark")
    tristan = next(t for t in f.trainers if t["script"] == "TRAINER_YOUNGSTER_TRISTAN")
    sight_ok = f.sight(tristan) == {(166, z) for z in range(814, 819)}
    down = (168, 824) in set(f.steps((168, 822)))
    up = (168, 822) in set(f.steps((168, 824)))
    results.append(("sight lines and ledges read as the game has them",
                    sight_ok and down and not up, f"sight {sight_ok}, down {down}, up {up}"))


def check_route_202(results):
    """Route 202, traced by hand on its collision map: coming north from
    Sandgem, the ledges send the player through the west grass, and each of
    the three trainers watches the only way on (Tristan's column, then
    Natalie's, then Logan's). All three are required."""
    got = {t["script"]: v for t, v in R.crossing("Roark", "ROUTE_202", "SANDGEM_TOWN",
                                                 "JUBILIFE_CITY")}
    ok = set(got.values()) == {"required"} and len(got) == 3
    results.append(("Route 202's three trainers are required", ok, str(got)))


def check_ian_examples(results):
    """Ian's own reading of the base ROM (2026-09-25): Route 203's five,
    Route 206's nine and Route 218's four trainers can all be walked around,
    and Route 202's three cannot. This is B1e's check against play."""
    def verdicts(split, header):
        row = next(c for c in R.CROSSINGS if c[:2] == (split, header))
        return [v for _t, v in R.crossing(*row)]
    got = {h: verdicts(s, h) for s, h in (("Roark", "ROUTE_203"), ("Fantina", "ROUTE_206"),
                                          ("Byron", "ROUTE_218"))}
    want = {"ROUTE_203": 5, "ROUTE_206": 9, "ROUTE_218": 4}
    ok = all(len(got[h]) == n and set(got[h]) == {"avoidable"} for h, n in want.items())
    results.append(("Ian's avoidable routes come out avoidable", ok,
                    ", ".join(f"{h} {len(v)} {sorted(set(v))}" for h, v in got.items())))


def check_gates(results):
    """Field moves and story gates hold trainers back until their split:
    Route 213's swimmers need Surf, which Wake's split lacks, and the
    Psyduck on Route 210 South keep the ninja boys out of reach until
    Byron's split."""
    def verdicts(split, header):
        row = next(c for c in R.CROSSINGS if c[:2] == (split, header))
        return {t["script"]: v for t, v in R.crossing(*row)}
    swim = verdicts("Wake", "ROUTE_213")
    before = verdicts("Maylene", "ROUTE_210_SOUTH")
    after = verdicts("Byron", "ROUTE_210_SOUTH")
    ninjas = [k for k in before if "NINJA_BOY" in k]
    ok = (swim["TRAINER_SWIMMER_MARY"] == "not reached"
          and all(before[k] == "not reached" for k in ninjas)
          and all(after[k] != "not reached" for k in ninjas) and len(ninjas) == 3)
    results.append(("Surf and the Psyduck gate the trainers behind them", ok,
                    f"Mary {swim['TRAINER_SWIMMER_MARY']}, ninja boys "
                    f"{[before[k] for k in ninjas]} then {[after[k] for k in ninjas]}"))


def check_late_visits(results):
    """The 22 later visits (required.late_visits; 16 until the Kaizo comb's
    levels, step 12, put six more teams in a later split than their map's;
    18 until Somnu and Moira at Lake Verity became a story fight): every one
    a crossing reaches lands in a split whose closing boss's ace covers its
    own, and the rest are off the story path."""
    first = R.first_crossings()
    ox = data.oxide_trainers()
    aces = pool.closing_aces()
    placed, off, wrong = 0, 0, []
    for _split, tr_id in R.late_visits():
        hit = first.get(ox[tr_id]["constant"])
        if not hit:
            off += 1
            continue
        cap = aces[hit[0]]
        ace = max(m["level"] for m in ox[tr_id]["party"])
        placed += 1
        if ace > cap:
            wrong.append(ox[tr_id]["stem"])
    results.append(("the 22 later visits land under their split's cap", not wrong and placed == 15,
                    f"{placed} placed, {off} off the story path" + (f"; over cap {wrong}" if wrong else "")))


def check_gauntlet_sections(results):
    """The sections keep Ian's rulings: 2 to 5 trainers each, the built ten
    (src/gauntlet.c), Victory Road 1F halved as the code lists it with its
    2F and B1F detours left out, and Mt. Coronet's bosses and hard officers
    out. Moved here from test_b6 when the first scoring system retired
    (2026-10-13)."""
    from . import gauntlet
    sizes = {(area, s[0]): len(gauntlet.section_trainers(area, s))
             for area, sections in gauntlet.SECTIONS.items() for s in sections}
    coronet = {tr for s in gauntlet.SECTIONS["mt_coronet"]
               for tr in gauntlet.section_trainers("mt_coronet", s)}
    names = {tr: t["constant"] for tr, t in data.oxide_trainers().items()}
    vr = [{names[tr] for tr in gauntlet.section_trainers("victory_road", s)}
          for s in gauntlet.SECTIONS["victory_road"]]
    ok = (len(sizes) == 10 and all(2 <= n <= 5 for n in sizes.values()) and not coronet & {520, 526, 834}
          and vr == [{"TRAINER_PSYCHIC_BRYCE", "TRAINER_BIRD_KEEPER_HANA", "TRAINER_ACE_TRAINER_MARIAH"},
                     {"TRAINER_BLACK_BELT_MILES", "TRAINER_DRAGON_TAMER_CLINTON", "TRAINER_VETERAN_EDGAR"}])
    results.append(("gauntlet sections hold 2 to 5 trainers, bosses left out", ok,
                    f"{len(sizes)} sections" if ok else f"{sizes}, Coronet {coronet}, 1F {vr}"))


def check_totals(results):
    got = {"required": 0, "avoidable": 0}
    for c in R.summary().values():
        for k, v in c.items():
            got[k] = got.get(k, 0) + v
    got["never reached"] = len(R.never_reached())
    results.append(("totals match the pinned reading", got == TOTALS, str(got)))


def main():
    results = []
    for check in (check_crossings_resolve, check_sight_and_ledges, check_route_202, check_ian_examples,
                  check_gates, check_late_visits, check_gauntlet_sections, check_totals):
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

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
# 64 once Roark's split gained five and Gardenia's seven the same day
# (docs/oxide/mandatory-fights-early.md): twelve moved trainers, Hiker
# Daniel too, since a required verdict on a map's second crossing in a split
# now wins over an avoidable one on its first.
# 67 in Wake's split's pass (2026-10-31, docs/oxide/wake-split.md): Valor
# Lakefront is now a crossing, and Gentleman Jeremy and Socialite Reina,
# moved there from Route 212 North (off the path), read required, as does
# Fisherman Travis, moved from Route 212 South to Route 213's west neck.
# Route 213's three turners were already read required and now look one way.
# 68 once Ian approved three Route 214 changes the same day: PI Carlos, moved
# to the narrows south of the berry field, turns from avoidable to required;
# Psychics Abigail and Mitchell were read required and now look one way.
# Unchanged when unpushable boulders became walls (2026-10-31): Lake
# Verity's grunts 3 and 4 stay avoidable, since Surf takes the player round
# them by the lake's west edge, boulders or not. Unchanged again the same
# day when Ian's recollection that the water there cannot be reached was
# checked against the game's code, which allows it (check_lake_verity_surf).
# 77 in Byron's split's pass (2026-10-31, docs/oxide/byron-split.md):
# nine trainers moved or now look one way, which turns nine avoidable
# verdicts required (Ninja Boy Fabian on Route 210 South; Bird Keeper
# Brianna and Black Belt Adam on Route 210 North; Guitarist Tony and Sailor
# Skyler on Route 218; Iron Island B2F's two pairs). Veteran Brian was read
# required already and now looks one way. Ace Trainer Ernest and Zac and
# Jen look one way too; they read avoidable here, since the model gives the
# split Surf and the river walks round them, but the player meets them
# before Surf.
# 80 once Route 221 (to Pal Park's lobby) and Iron Island B1F's right room
# became crossings the same day: they read Swimmer Dillon, Collector Ivan
# and Picnicker Summer required and four more of Route 221's trainers
# (Vanessa, Cory, Jake and Shannon) avoidable, all seven left out before.
TOTALS = {"required": 80, "avoidable": 101, "never reached": 12}


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
    and Route 202's three cannot. This is B1e's check against play. Route
    203's Sebastian and Madeline moved onto the story path on 2026-10-29
    (docs/oxide/mandatory-fights-early.md), so the check holds for its other
    three. Route 218's Tony and Skyler moved to its west neck in Byron's
    split's pass (2026-10-31, docs/oxide/byron-split.md), so it holds for
    its other two."""
    moved = {"TRAINER_YOUNGSTER_SEBASTIAN", "TRAINER_LASS_MADELINE",
             "TRAINER_GUITARIST_TONY", "TRAINER_SAILOR_SKYLER"}

    def verdicts(split, header):
        row = next(c for c in R.CROSSINGS if c[:2] == (split, header))
        return [v for t, v in R.crossing(*row) if t["script"] not in moved]
    got = {h: verdicts(s, h) for s, h in (("Roark", "ROUTE_203"), ("Fantina", "ROUTE_206"),
                                          ("Byron", "ROUTE_218"))}
    want = {"ROUTE_203": 3, "ROUTE_206": 9, "ROUTE_218": 2}
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
    """The sections keep Ian's rulings: 2 to 5 trainers each, the built nine
    (src/gauntlet.c), Victory Road 1F halved as the code lists it with its
    2F and B1F detours left out, and Mt. Coronet's bosses and hard officers
    out. Moved here from test_b6 when the first scoring system retired
    (2026-10-13). Ten until the Eterna building's 3F, with Officer Moira,
    left the gauntlets (Ian, 2026-10-31), and neither of its trainers may
    sit in a section."""
    from . import gauntlet
    sizes = {(area, s[0]): len(gauntlet.section_trainers(area, s))
             for area, sections in gauntlet.SECTIONS.items() for s in sections}
    coronet = {tr for s in gauntlet.SECTIONS["mt_coronet"]
               for tr in gauntlet.section_trainers("mt_coronet", s)}
    names = {tr: t["constant"] for tr, t in data.oxide_trainers().items()}
    vr = [{names[tr] for tr in gauntlet.section_trainers("victory_road", s)}
          for s in gauntlet.SECTIONS["victory_road"]]
    eterna = {names[tr] for s in gauntlet.SECTIONS["galactic_eterna"]
              for tr in gauntlet.section_trainers("galactic_eterna", s)}
    ok = (len(sizes) == 9 and all(2 <= n <= 5 for n in sizes.values()) and not coronet & {520, 526, 834}
          and not eterna & {"TRAINER_SCIENTIST_TRAVON", "TRAINER_GALACTIC_GRUNT_TEAM_GALACTIC_ETERNA_BUILDING_3F"}
          and vr == [{"TRAINER_PSYCHIC_BRYCE", "TRAINER_BIRD_KEEPER_HANA", "TRAINER_ACE_TRAINER_MARIAH"},
                     {"TRAINER_BLACK_BELT_MILES", "TRAINER_DRAGON_TAMER_CLINTON", "TRAINER_VETERAN_EDGAR"}])
    results.append(("gauntlet sections hold 2 to 5 trainers, bosses left out", ok,
                    f"{len(sizes)} sections" if ok else f"{sizes}, Coronet {coronet}, 1F {vr}"))


def _canalave_gym_floor():
    """The open tiles of Canalave Gym's ground floor, from the collision map
    the game reads there in place of the tiles' own bit
    (src/overlay008/gym_features.c, sCanalaveGymCollisionMaps[0])."""
    import os
    import re
    with open(os.path.join(data.ROOT, "src", "overlay008", "gym_features.c"), encoding="utf-8") as f:
        src = f.read()
    body = src[src.index("sCanalaveGymCollisionMaps"):]
    body = body[body.index("=") + 1:body.index("};")]
    floor = [int(v) for v in re.findall(r"\b[01]\b", body)][:32 * 32]
    return {(x, z) for z in range(32) for x in range(32) if not floor[z * 32 + x]}


def check_byron_order(results):
    """Byron's split runs Canalave, Iron Island, the gym, then the library
    (Ian, 2026-10-31). From Route 218's gate the player reaches the sailor to
    Iron Island and the gym's door; the island is walked from the boat to
    Riley's grunts on B2F; inside the gym, the trigger across the row past
    the entrance (its coord event, which holds until Riley's tag battle is
    won) leaves the player nowhere to go but out; and Barry at the library
    door, who waits for the same battle, keeps the library shut."""
    from . import world
    canalave = R.Field("CANALAVE_CITY", "Byron")
    start = canalave.ends("ROUTE_218_GATE_TO_CANALAVE_CITY")
    gym_door = world.warps_to("CANALAVE_CITY", "CANALAVE_CITY_GYM")
    library = world.warps_to("CANALAVE_CITY", "CANALAVE_LIBRARY_1F")
    seen = canalave.reach(start)
    got = {"sailor": bool(seen & canalave.ends("@LOCALID_SAILOR_ELDRITCH")),
           "gym door": bool(seen & gym_door)}
    barry = next(o for o in world.events("CANALAVE_CITY")["object_events"]
                 if o["id"] == "LOCALID_RIVAL_LIBRARY")
    canalave.objects[(barry["x"], barry["z"])] = barry
    got["library past Barry"] = bool(canalave.reach(start) & library)

    # The island, floor by floor, from the boat's landing beside its sailor.
    walk = [("IRON_ISLAND", {(100, 502)}, world.warps_to("IRON_ISLAND", "IRON_ISLAND_1F")),
            ("IRON_ISLAND_1F", world.warps_to("IRON_ISLAND_1F", "IRON_ISLAND"),
             world.warps_to("IRON_ISLAND_1F", "IRON_ISLAND_B1F_RIGHT_ROOM")),
            ("IRON_ISLAND_B1F_RIGHT_ROOM", world.warps_to("IRON_ISLAND_B1F_RIGHT_ROOM", "IRON_ISLAND_1F"),
             world.warps_to("IRON_ISLAND_B1F_RIGHT_ROOM", "IRON_ISLAND_B2F_LEFT_ROOM")),
            ("IRON_ISLAND_B2F_LEFT_ROOM",
             world.warps_to("IRON_ISLAND_B2F_LEFT_ROOM", "IRON_ISLAND_B1F_RIGHT_ROOM"), {(21, 40), (21, 41)})]
    got["island to Riley's grunts"] = all(R.Field(h, "Byron").path(a, b) for h, a, b in walk)

    gym = next((c for c in world.events("CANALAVE_CITY_GYM")["coord_events"]
                if c["var"] == "VAR_MAP_LOCAL_0x00"), {"x": 0, "z": 0, "width": 0})
    trigger = {(gym["x"] + i, gym["z"]) for i in range(gym["width"])}
    floor = _canalave_gym_floor()
    entrance = {(w["x"], w["z"]) for w in world.events("CANALAVE_CITY_GYM")["warp_events"]}
    inside, frontier = set(entrance), list(entrance)
    while frontier:
        x, z = frontier.pop()
        for dx, dz in world.DIRS.values():
            n = (x + dx, z + dz)
            if n in floor and n not in trigger and n not in inside:
                inside.add(n)
                frontier.append(n)
    # Past the row the entrance opens onto, two rows north of the door.
    door_z = min(z for _x, z in entrance)
    got["gym past the entrance row"] = any(z < door_z - 1 for _x, z in inside)
    want = {"sailor": True, "gym door": True, "library past Barry": False,
            "island to Riley's grunts": True, "gym past the entrance row": False}
    results.append(("Byron's split runs the island, the gym, then the library", got == want,
                    ", ".join(f"{k} {v}" for k, v in got.items())))


def check_unpushable_boulders(results):
    """A Strength boulder the game cannot push stays a wall once Strength is
    held, and one it can push is taken as gone (2026-10-31). Lake Verity's
    boulder beside grunt 4, at (53,45), has solid tiles to its east and
    south and the grunt to its north, so no push moves it. The one beside
    grunt 3, at (46,45), can be pushed west onto the lake from the grass at
    (47,45), since water does not stop a boulder. Route 215's two, which
    close Dennis and Maya's corridor, cannot be pushed either."""
    verity = R.Field("LAKE_VERITY", "Candice")
    route_215 = R.Field("ROUTE_215", "League")

    def held(field, xz):
        o = field.objects.get(xz)
        return bool(o) and o["graphics_id"] == "OBJ_EVENT_GFX_STRENGTH_BOULDER"
    got = {"Verity (53,45)": held(verity, (53, 45)), "Verity (46,45)": held(verity, (46, 45)),
           "Route 215 (647,596)": held(route_215, (647, 596)),
           "Route 215 (647,599)": held(route_215, (647, 599))}
    want = {"Verity (53,45)": True, "Verity (46,45)": False,
            "Route 215 (647,596)": True, "Route 215 (647,599)": True}
    results.append(("a boulder that cannot be pushed stays a wall with Strength", got == want,
                    ", ".join(f"{k} {'wall' if v else 'gone'}" for k, v in got.items())))


def check_lake_verity_surf(results):
    """Lake Verity's grunts 3 and 4 read avoidable on Surf alone (2026-10-31).
    Ian recalled that the water round them cannot be reached and that a
    boulder cannot be pushed into water; the game's code allows both. Surf
    is offered when the faced tile is surfable, unless the player stands on
    a raised bridge (PlayerAvatar_CanUseSurf), and Oxide asks only for the
    Fen Badge and Celestic's story (field_control.c); no collision bit,
    tile side or height is read. The shore at (44,46) stands at height 16
    and the water at 8, under the 20 that stops a step
    (terrain_collision_manager.c, GetVerticalDirection), and the same holds
    at the landing, (48,43). A boulder's push refuses only the collision
    bit, a wall behaviour, a missing tile or an object (sub_02063E18). So
    the verdicts stand: with Surf both grunts are avoidable, boulder or no
    boulder, and without it both are required. If Ian wants the pair
    mandatory, the map must change."""
    def verdicts(field):
        start, goal = field.ends("VERITY_LAKEFRONT"), field.ends("@LOCALID_MARS")
        return {t["script"][-1]: "avoidable" if field.path(start, goal, frozenset(field.sight(t)))
                else "required" for t in field.trainers if t["script"][-1] in "34"}
    built = R.Field("LAKE_VERITY", "Candice")
    held = R.Field("LAKE_VERITY", "Candice")
    held.objects[(46, 45)] = {"graphics_id": "OBJ_EVENT_GFX_STRENGTH_BOULDER"}
    dry = R.Field("LAKE_VERITY", "Candice")
    dry.can = dry.can - {"surf"}
    got = {"with Surf": verdicts(built), "boulder held": verdicts(held), "no Surf": verdicts(dry)}
    ok = (set(got["with Surf"].values()) == {"avoidable"} and got["boulder held"] == got["with Surf"]
          and set(got["no Surf"].values()) == {"required"} and len(got["no Surf"]) == 2)
    results.append(("Lake Verity's grunts 3 and 4 hang on Surf alone", ok,
                    "; ".join(f"{k} {sorted(set(v.values()))}" for k, v in got.items())))


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
                  check_gates, check_late_visits, check_gauntlet_sections, check_byron_order,
                  check_unpushable_boulders, check_lake_verity_surf, check_totals):
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

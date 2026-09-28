"""The fight simulator's rules, on small battles built by hand (fightsim.py, fightai.py).

    PYTHONPATH=. python3 -m tools.oxide.balance.test_fightsim

Runs no Node: each check builds the calculator's rows itself, so what it
tests is the simulator's own arithmetic and rules.
"""
import random
import sys

from . import fightai, fightsim as fs

CHART = {"Normal": {"Ghost": 0.0, "Rock": 0.5}, "Fire": {"Grass": 2.0, "Water": 0.5},
         "Water": {"Fire": 2.0}, "Grass": {"Water": 2.0}, "Ghost": {"Normal": 0.0}}


def _chart():
    types = ["Normal", "Fire", "Water", "Grass", "Ghost", "Rock"]
    return {a: {d: CHART.get(a, {}).get(d, 1.0) for d in types} for a in types}


def battle(p_moves, b_moves, rolls, p_speed=100, b_speed=50, p_types=("Normal",), b_types=("Normal",),
           hp=100, seed=1):
    """A one-against-one battle: rolls[(side, move)] is the move's roll list."""
    st = {"rows": {}, "speed": {(None, "p0"): p_speed, (None, "b0.0"): b_speed},
          "info": {}, "pokemon": {}, "moves": {"p0": p_moves, "b0.0": b_moves},
          "chart": _chart(), "rock_eff": {}, "base_weather": None, "trick_room": False}
    for key, types in (("p0", p_types), ("b0.0", b_types)):
        st["info"][key] = {"hp": hp, "stats": {"atk": 100, "def": 100, "spa": 100, "spd": 100, "spe": 100},
                           "types": list(types), "ability": None, "item": None}
        st["pokemon"][key] = {"species": key, "level": 50}
    st["rows"][(None, "p0", "b0.0")] = {"moves": {m: {"rolls": rolls.get(("p", m), [0])} for m in p_moves}}
    st["rows"][(None, "b0.0", "p0")] = {"moves": {m: {"rolls": rolls.get(("b", m), [0])} for m in b_moves}}
    p = fs.Mon("p0", st["pokemon"]["p0"], st["info"]["p0"], p_moves, "p")
    b = fs.Mon("b0.0", st["pokemon"]["b0.0"], st["info"]["b0.0"], b_moves, "b")
    return fs.Battle(st, fs.Side([p], "p"), fs.Side([b], "b"), random.Random(seed), ai_flags=7), p, b


def check_damage(results):
    """Stages, burn and screens change damage as Generation 4 does."""
    b, p, foe = battle(["Tackle"], ["Tackle"], {("p", "Tackle"): [40] * 16})
    t = fs.move("Tackle")
    plain = b.damage(p, foe, t, roll=0)
    p.stages["atk"] = 2
    boosted = b.damage(p, foe, t, roll=0)
    p.stages["atk"], p.status = 0, "brn"
    burned = b.damage(p, foe, t, roll=0)
    p.status = None
    b.b.screens["Reflect"] = 5
    screened = b.damage(p, foe, t, roll=0)
    crit = b.damage(p, foe, t, crit=True, roll=0)
    ok = (plain, boosted, burned, screened, crit) == (40, 80, 20, 20, 80)
    results.append(("stages, burn, Reflect and critical hits scale damage", ok,
                    f"plain {plain}, +2 {boosted}, burned {burned}, Reflect {screened}, crit {crit}"))


def check_status(results):
    """Paralysis quarters Speed; sleep lasts one to four turns; a Fire type
    cannot burn; a statused Pokemon takes no second status."""
    b, p, foe = battle(["Tackle"], ["Tackle"], {})
    before = b.speed(p)
    fs.give_status(b, p, "par")
    after = b.speed(p)
    fire = battle(["Tackle"], ["Tackle"], {}, p_types=("Fire",))[1]
    no_burn = not fs.can_status(b, fire, "brn")
    second = not fs.give_status(b, p, "slp")
    turns = set()
    for seed in range(200):
        bb, pp, _f = battle(["Tackle"], ["Tackle"], {}, seed=seed)
        fs.give_status(bb, pp, "slp")
        turns.add(pp.sleep)
    ok = after == before // 4 and no_burn and second and turns == {1, 2, 3, 4}
    results.append(("paralysis, sleep and immunities", ok,
                    f"speed {before}->{after}, sleep turns {sorted(turns)}, Fire burned "
                    f"{not no_burn}, second status {not second}"))


def check_sleep_turns(results):
    """A Pokemon given N turns of sleep misses exactly N turns, then wakes
    and acts the same turn (Generation 4)."""
    b, p, foe = battle(["Tackle"], ["Tackle"], {("p", "Tackle"): [10] * 16})
    p.status, p.sleep = "slp", 2
    hp = []
    for _ in range(3):
        fs.use_move(b, p, fs.move("Tackle"), foe, True)
        hp.append(foe.hp)
    ok = hp == [100, 100, 90] and p.status is None
    results.append(("sleep lasts its turns, then the Pokemon acts", ok, f"foe HP {hp}"))


def check_binding(results):
    """A binding move takes an eighth of max HP a turn, a sixth when the
    binder holds a Binding Band (Ian, 2026-09-28)."""
    lost = []
    for band in (False, True):
        b, p, foe = battle(["Tackle"], ["Tackle"], {}, hp=96)
        foe.bound, foe.bound_band = 3, band
        fs._end_of_turn_mon(b, b.b, foe)
        lost.append(96 - foe.hp)
    results.append(("binding takes an eighth a turn, a sixth with the Binding Band", lost == [12, 16],
                    f"lost {lost[0]}, with the band {lost[1]}"))


def check_ai_kill(results):
    """Evaluate Attack: a move that kills scores above the strongest that
    does not, and Basic refuses a move the target is immune to."""
    b, p, foe = battle(["Tackle"], ["Tackle", "Ember", "Lick"],
                       {("b", "Tackle"): [30] * 16, ("b", "Ember"): [60] * 16, ("b", "Lick"): [0] * 16},
                       p_types=("Normal",))
    p.hp = 50
    scores = fightai.score_moves(b, foe, p, 1 | 2)
    kill_best = scores[1] == max(scores) and scores[1] > 100
    lick_refused = scores[2] < 100
    ok = kill_best and lick_refused
    results.append(("the AI takes a kill and refuses an immune move", ok, f"scores {scores}"))


def check_ai_status(results):
    """Basic takes 10 from a status move at a target already statused."""
    b, p, foe = battle(["Tackle"], ["Tackle", "Thunder Wave"], {("b", "Tackle"): [10] * 16})
    fresh = fightai.score_moves(b, foe, p, 1)[1]
    fs.give_status(b, p, "brn")
    statused = fightai.score_moves(b, foe, p, 1)[1]
    ok = fresh == 100 and statused == 90
    results.append(("the AI does not status a statused target", ok, f"{fresh} then {statused}"))


def check_battle(results):
    """A battle runs to its end: the side with the stronger hit wins."""
    st = {"rows": {}, "speed": {}, "info": {}, "pokemon": {}, "moves": {}, "chart": _chart(),
          "rock_eff": {}, "base_weather": None, "trick_room": False}
    for key, hit in (("p0", 60), ("p1", 60), ("b0.0", 20), ("b0.1", 20)):
        st["info"][key] = {"hp": 100, "stats": {"atk": 100, "def": 100}, "types": ["Normal"],
                           "ability": None, "item": None}
        st["pokemon"][key] = {"species": key, "level": 50}
        st["moves"][key] = ["Tackle"]
        st["speed"][(None, key)] = 100 if key.startswith("p") else 50
    for a in ("p0", "p1"):
        for d in ("b0.0", "b0.1"):
            st["rows"][(None, a, d)] = {"moves": {"Tackle": {"rolls": [60] * 16}}}
            st["rows"][(None, d, a)] = {"moves": {"Tackle": {"rolls": [20] * 16}}}
    lost, won = fs.run_battle(st, ["p0", "p1"], ["b0.0", "b0.1"], random.Random(3), 7)
    ok = won and lost == 0
    results.append(("a battle runs to its end", ok, f"lost {lost}, won {won}"))


def check_doubles(results):
    """A double battle runs to its end, and a spread move hits both foes at
    three quarters."""
    st = {"rows": {}, "speed": {}, "info": {}, "pokemon": {}, "moves": {}, "chart": _chart(),
          "rock_eff": {}, "base_weather": None, "trick_room": False}
    keys = ("p0", "p1", "b0.0", "b0.1")
    for key in keys:
        st["info"][key] = {"hp": 100, "stats": {"atk": 100, "def": 100}, "types": ["Normal"],
                           "ability": None, "item": None}
        st["pokemon"][key] = {"species": key, "level": 50}
        st["moves"][key] = ["Rock Slide"] if key.startswith("p") else ["Tackle"]
        st["speed"][(None, key)] = 100 if key.startswith("p") else 50
    for a in ("p0", "p1"):
        for d in ("b0.0", "b0.1"):
            st["rows"][(None, a, d)] = {"moves": {"Rock Slide": {"rolls": [40] * 16}}}
            st["rows"][(None, d, a)] = {"moves": {"Tackle": {"rolls": [10] * 16}}}
    b, p, foe = battle(["Rock Slide"], ["Tackle"], {})
    rs = fs.move("Rock Slide")
    lost, won = fs.run_doubles(st, ["p0", "p1"], [["b0.0", "b0.1"]], random.Random(5), [7])
    spread_ok = rs.range == "ADJACENT_OPPONENTS"
    ok = won and lost == 0 and spread_ok
    results.append(("a double battle runs to its end with a spread move", ok,
                    f"lost {lost}, won {won}, Rock Slide's range {rs.range}"))


def field(mons, rows, speeds=None):
    """A singles battle from a sketch: mons is {key: (types, moves)}, the
    player's keys starting with p (the first leads) and the trainer's with
    b; rows is {(attacker, target): {move: damage}}; every Pokemon has 100 HP."""
    st = {"rows": {}, "speed": {}, "info": {}, "pokemon": {}, "moves": {}, "chart": _chart(),
          "rock_eff": {}, "base_weather": None, "trick_room": False}
    for key, (types, moves) in mons.items():
        st["info"][key] = {"hp": 100, "stats": {"atk": 100, "def": 100, "spa": 100, "spd": 100, "spe": 100},
                           "types": list(types), "ability": None, "item": None}
        st["pokemon"][key] = {"species": key, "level": 50}
        st["moves"][key] = moves
        st["speed"][(None, key)] = (speeds or {}).get(key, 100 if key.startswith("p") else 50)
    for a in mons:
        for d in mons:
            if a[0] != d[0]:
                got = rows.get((a, d), {})
                st["rows"][(None, a, d)] = {"moves": {m: {"rolls": [got.get(m, 0)] * 16}
                                                      for m in mons[a][1]}}
    side = {s: [fs.Mon(k, st["pokemon"][k], st["info"][k], st["moves"][k], s) for k in mons if k[0] == s]
            for s in "pb"}
    return fs.Battle(st, fs.Side(side["p"], "p"), fs.Side(side["b"], "b"), random.Random(1), ai_flags=7)


def check_pivot(results):
    """A Pokemon that would win the exchange but not after taking the move
    aimed at the lead goes in through one that resists that move."""
    b = field({"p0": (["Normal"], ["Scratch"]), "p1": (["Grass"], ["Scratch"]),
               "p2": (["Water"], ["Scratch"]), "b0": (["Fire"], ["Ember", "Scratch"])},
              {("p0", "b0"): {"Scratch": 10}, ("p1", "b0"): {"Scratch": 50}, ("p2", "b0"): {"Scratch": 5},
               ("b0", "p0"): {"Ember": 60, "Scratch": 15}, ("b0", "p1"): {"Ember": 70, "Scratch": 20},
               ("b0", "p2"): {"Ember": 10, "Scratch": 15}})
    got = fs.player_choice(b)
    ok = got == ("switch", 2)
    results.append(("the player pivots through a resist", ok, f"choice {got}"))


def check_stall(results):
    """With the foe's Light Screen up and Pokemon that take little, the
    player trades places until it runs out; with none up it attacks."""
    mons = {"p0": (["Normal"], ["Ember"]), "p1": (["Normal"], ["Scratch"]), "b0": (["Normal"], ["Scratch"])}
    rows = {("p0", "b0"): {"Ember": 40}, ("p1", "b0"): {"Scratch": 10},
            ("b0", "p0"): {"Scratch": 10}, ("b0", "p1"): {"Scratch": 10}}
    b = field(mons, rows)
    b.b.screens["Light Screen"] = 5
    screened = fs.player_choice(b)
    plain = fs.player_choice(field(mons, rows))
    ok = screened == ("switch", 1) and plain[0] == "move"
    results.append(("the player stalls out the foe's screens", ok, f"screened {screened}, plain {plain[0]}"))


def check_pp_stall(results):
    """A threat nearly out of PP is drained by a Pokemon that takes it easily."""
    b = field({"p0": (["Grass"], ["Scratch"]), "p1": (["Water"], ["Scratch"]),
               "b0": (["Fire"], ["Flamethrower", "Scratch"])},
              {("p0", "b0"): {"Scratch": 30}, ("p1", "b0"): {"Scratch": 5},
               ("b0", "p0"): {"Flamethrower": 60, "Scratch": 10},
               ("b0", "p1"): {"Flamethrower": 10, "Scratch": 15}})
    b.b.cur().pp["Flamethrower"] = 3
    drained = fs.player_choice(b)
    b.b.cur().pp["Flamethrower"] = 10
    full = fs.player_choice(b)
    ok = drained == ("switch", 1) and full != drained
    results.append(("the player drains a threat's last PP", ok, f"3 PP {drained}, 10 PP {full}"))


def check_setup(results):
    """Setup while the foe needs many hits, up to +2 against a last Pokemon."""
    b = field({"p0": (["Normal"], ["Scratch", "Swords Dance"]), "b0": (["Normal"], ["Scratch"])},
              {("p0", "b0"): {"Scratch": 20}, ("b0", "p0"): {"Scratch": 10}})
    first = fs.player_choice(b)
    b.p.cur().stages["atk"] = 2
    capped = fs.player_choice(b)
    ok = first[1].name == "Swords Dance" and capped[1].name == "Scratch"
    results.append(("the player sets up when safe, to its cap", ok, f"{first[1].name} then {capped[1].name}"))


def check_self_risk(results):
    """The player does not faint its own Pokemon with recoil while another
    attack does damage, and uses the recoil move when it is safe."""
    mons = {"p0": (["Fire"], ["Flare Blitz", "Scratch"]), "b0": (["Normal"], ["Scratch"])}
    rows = {("p0", "b0"): {"Flare Blitz": 90, "Scratch": 30}, ("b0", "p0"): {"Scratch": 5}}
    healthy = fs.player_choice(field(mons, rows))
    b = field(mons, rows)
    b.p.cur().hp = 20
    low = fs.player_choice(b)
    ok = healthy[1].name == "Flare Blitz" and low[1].name == "Scratch"
    results.append(("the player does not recoil its own Pokemon to death", ok,
                    f"full HP {healthy[1].name}, 20 HP {low[1].name}"))


def check_sure(results):
    """The sure Pokemon: the starters, the one-species gifts and eggs, the
    trades that ask nothing and the statics; no random gift, and no trade
    that asks for a catch."""
    sure = fs.sure_catches()
    want = {"SPECIES_TURTWIG", "SPECIES_PIPLUP", "SPECIES_SCORBUNNY", "SPECIES_EEVEE", "SPECIES_TOGEPI",
            "SPECIES_VULLABY", "SPECIES_POPPLIO", "SPECIES_ROTOM"}
    not_sure = {"SPECIES_RIOLU", "SPECIES_GLAMEOW", "SPECIES_ELEKID", "SPECIES_SUICUNE"}
    ok = want <= set(sure) and not (not_sure & set(sure))
    results.append(("the sure Pokemon are the ones every run has", ok,
                    f"{len(sure)} sure; missing {sorted(want - set(sure))}; wrongly in "
                    f"{sorted(not_sure & set(sure))}"))


def main():
    results = []
    for check in (check_damage, check_status, check_sleep_turns, check_binding, check_ai_kill, check_ai_status,
                  check_battle, check_doubles, check_pivot, check_stall, check_pp_stall, check_setup,
                  check_self_risk, check_sure):
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

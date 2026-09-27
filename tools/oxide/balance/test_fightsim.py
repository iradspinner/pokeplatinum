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


def main():
    results = []
    for check in (check_damage, check_status, check_ai_kill, check_ai_status, check_battle):
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

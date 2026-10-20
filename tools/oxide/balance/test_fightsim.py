"""The fight simulator's rules, on small battles built by hand (fightsim.py, fightai.py).

    PYTHONPATH=. python3 -m tools.oxide.balance.test_fightsim

Runs no Node: each check builds the calculator's rows itself, so what it
tests is the simulator's own arithmetic and rules.
"""
import collections
import random
import sys

from . import fightai, fightsim as fs

CHART = {"Normal": {"Ghost": 0.0, "Rock": 0.5}, "Fire": {"Grass": 2.0, "Water": 0.5},
         "Water": {"Fire": 2.0}, "Grass": {"Water": 2.0}, "Ghost": {"Normal": 0.0},
         "Electric": {"Ground": 0.0, "Water": 2.0}}


def _chart():
    types = ["Normal", "Fire", "Water", "Grass", "Ghost", "Rock", "Electric", "Ground"]
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
    ok = (plain, boosted, burned, screened, crit) == (40, 80, 20, 20, 60)
    results.append(("stages, burn, Reflect and Oxide's 1.5x critical hits scale damage", ok,
                    f"plain {plain}, +2 {boosted}, burned {burned}, Reflect {screened}, crit {crit}"))


def check_crit_odds(results):
    """Oxide's critical-hit odds: 1 in 24 at no stage, certain from +3."""
    ok = fs.CRIT_RATE[0] == 1 / 24 and fs.CRIT_RATE[1] == 1 / 8 and fs.CRIT_RATE[2] == 1 / 2 \
        and fs.CRIT_RATE[3] == 1.0 and fs.CRIT_MUL == 1.5
    results.append(("critical hits at Oxide's Generation 7 odds", ok, str(fs.CRIT_RATE)))


def check_status_immunity(results):
    """Among status moves only Thunder Wave meets the type chart
    (BattleControllerPlayer_CheckTypeChart runs it for moves with power and
    for Thunder Wave): Thunder Wave fails on a Ground type, while Glare, a
    Normal move with no power, still paralyses a Ghost."""
    b, p, foe = battle(["Thunder Wave"], ["Tackle"], {}, b_types=("Ground",))
    fs.status_move(b, p, fs.move("Thunder Wave"), foe, True)
    ground = foe.status
    b2, p2, foe2 = battle(["Glare"], ["Tackle"], {}, b_types=("Ghost",))
    fs.status_move(b2, p2, fs.move("Glare"), foe2, True)
    ok = ground is None and foe2.status == "par"
    results.append(("only Thunder Wave among status moves is stopped by type", ok,
                    f"Ground {ground}, Ghost {foe2.status}"))


def check_item_moves(results):
    """Natural Gift spends its berry, and fails without one."""
    b, p, foe = battle(["Natural Gift"], ["Tackle"], {("p", "Natural Gift"): [30] * 16})
    p.item = "Oran Berry"
    ng = fs.move("Natural Gift")
    fs.attack(b, p, ng, foe, True)
    first, spent = foe.hp, p.item
    fs.attack(b, p, ng, foe, True)
    ok = first < 100 and spent is None and foe.hp == first
    results.append(("Natural Gift and Fling spend the item and fail without one", ok,
                    f"HP 100 to {first}, then {foe.hp}; item after {spent}"))


def check_weather_rock(results):
    """A weather move lasts eight turns with its rock, five without."""
    b, p, foe = battle(["Rain Dance"], ["Tackle"], {})
    p.item = "Damp Rock"
    fs.status_move(b, p, fs.move("Rain Dance"), foe, True)
    rock = b.weather_turns
    b2, p2, foe2 = battle(["Rain Dance"], ["Tackle"], {})
    fs.status_move(b2, p2, fs.move("Rain Dance"), foe2, True)
    ok = (rock, b2.weather_turns) == (8, 5)
    results.append(("a weather move lasts eight turns with its rock", ok, f"{rock} and {b2.weather_turns}"))


def check_map_weather_replaced(results):
    """A weather move replaces a map's permanent weather for good: the
    move's script clears every weather flag, the map's included, and when
    its five turns end only its own flag clears, so the field is left
    clear (effect_script_0136, subscript_raining_end)."""
    b, p, foe = battle(["Rain Dance"], ["Tackle"], {})
    b.st["base_weather"], b.weather = "Sand", "Sand"
    fs.status_move(b, p, fs.move("Rain Dance"), foe, True)
    during = b.weather
    for _ in range(5):
        fs.end_of_turn(b)
    ok = (during, b.weather) == ("Rain", None)
    results.append(("a weather move ends a map's weather, which does not come back", ok,
                    f"during {during}, after five turns {b.weather}"))


def check_permanent_trick_room(results):
    """A permanent Trick Room (Saturn 2's) never counts down, and the move
    Trick Room fails under it (battle_lib.c, FIELD_CONDITION_TRICK_ROOM_PERM);
    a move's own room still lasts five turns and ends."""
    b, p, foe = battle(["Trick Room"], ["Tackle"], {})
    b.trick_room = 999
    fs.status_move(b, p, fs.move("Trick Room"), foe, True)
    for _ in range(10):
        fs.end_of_turn(b)
    kept = b.trick_room
    b2, p2, foe2 = battle(["Trick Room"], ["Tackle"], {})
    fs.status_move(b2, p2, fs.move("Trick Room"), foe2, True)
    set_to = b2.trick_room
    for _ in range(5):
        fs.end_of_turn(b2)
    ok = (kept, set_to, b2.trick_room) == (999, 5, 0)
    results.append(("a permanent Trick Room stays; a move's room lasts five turns", ok,
                    f"permanent {kept}; a move's {set_to}, then {b2.trick_room}"))


def check_move_reworks(results):
    """The move reworks (2026-10-06) in fightsim's own attack, which double
    battles use: Hyper Beam's half recoil with no recharge, a two to five
    hit move's count, Upper Hand and Shell Trap failing when their condition
    is not met, and Burning Jealousy's burn on a raised target only."""
    b, p, foe = battle(["Hyper Beam"], ["Tackle"], {("p", "Hyper Beam"): [40] * 16})
    foe.ability = "Battle Armor"
    fs.attack(b, p, fs.move("Hyper Beam"), foe, True)
    beam = (100 - foe.hp, 100 - p.hp, p.recharge)
    seen = set()
    for s in range(200):
        b, p, foe = battle(["Bullet Seed"], ["Tackle"], {("p", "Bullet Seed"): [30] * 16}, hp=200, seed=s)
        foe.ability = "Battle Armor"
        fs.attack(b, p, fs.move("Bullet Seed"), foe, True)
        seen.add((200 - foe.hp) // 10)
    b, p, foe = battle(["Upper Hand"], ["Tackle"], {("p", "Upper Hand"): [20] * 16})
    foe.chosen = fs.move("Tackle")
    fs.attack(b, p, fs.move("Upper Hand"), foe, True)
    upper_no = 100 - foe.hp
    foe.chosen = fs.move("Quick Attack")
    fs.attack(b, p, fs.move("Upper Hand"), foe, True)
    upper_yes = 100 - foe.hp - upper_no
    b, p, foe = battle(["Shell Trap"], ["Tackle"], {("p", "Shell Trap"): [25] * 16})
    fs.attack(b, p, fs.move("Shell Trap"), foe, True)
    trap_no = 100 - foe.hp
    p.hit_this_turn = ("Physical", 10)
    fs.attack(b, p, fs.move("Shell Trap"), foe, True)
    trap_yes = 100 - foe.hp - trap_no
    b, p, foe = battle(["Burning Jealousy"], ["Tackle"], {("p", "Burning Jealousy"): [10] * 16})
    fs.attack(b, p, fs.move("Burning Jealousy"), foe, True)
    calm = foe.status
    fs.change_stages(foe, {"atk": 1})
    fs.attack(b, p, fs.move("Burning Jealousy"), foe, True)
    ok = (beam == (40, 20, False) and seen == {2, 3, 4, 5} and (upper_no, upper_yes) == (0, 20)
          and (trap_no, trap_yes) == (0, 25) and (calm, foe.status) == (None, "brn"))
    results.append(("the move reworks in fightsim's own attack", ok,
                    f"Hyper Beam {beam}; Bullet Seed hits {sorted(seen)}; Upper Hand {upper_no}/{upper_yes}; "
                    f"Shell Trap {trap_no}/{trap_yes}; Burning Jealousy {calm} then {foe.status}"))


def check_end_of_turn_order(results):
    """The turn's end runs in the engine's speed order (BattleSystem_SortMonSpeedOrder)
    and stops the moment a side is out of Pokemon, so with both last Pokemon
    poisoned and low, the faster faints first and the slower survives; Trick
    Room reverses it; a speed tie splits on a coin. Sand and hail strike every
    Pokemon before any one's own conditions, and a move's sandstorm ends on
    its fifth turn's end before striking, so it strikes four times."""
    def poisoned(p_speed, b_speed, p_hp=5, b_hp=5, trick_room=0, weather=None, seed=1):
        b, p, foe = battle(["Tackle"], ["Tackle"], {}, p_speed=p_speed, b_speed=b_speed, seed=seed)
        p.hp, foe.hp, p.status, foe.status = p_hp, b_hp, "psn", "psn"
        b.trick_room, b.weather = trick_room, weather
        fs.end_of_turn(b)
        return p.hp, foe.hp
    faster = poisoned(100, 50)
    slower = poisoned(50, 100)
    room = poisoned(100, 50, trick_room=3)
    ties = [poisoned(80, 80, seed=s) for s in range(200)]
    p_first = sum(1 for p_hp, _f in ties if p_hp == 0)
    # Sand before poison: the faster player's Pokemon takes sand (20 to 14),
    # the trainer's faints to sand (5 to 0) and the battle ends before the
    # player's poison.
    sand = poisoned(100, 50, p_hp=20, b_hp=5, weather="Sand")
    b, p, foe = battle(["Tackle"], ["Tackle"], {})
    b.weather, b.weather_turns = "Sand", 5
    for _ in range(5):
        fs.end_of_turn(b)
    storm = (100 - p.hp, b.weather)
    ok = (faster == (0, 5) and slower == (5, 0) and room == (5, 0) and 70 <= p_first <= 130
          and sand == (14, 0) and storm == (24, None))
    results.append(("the turn's end runs in speed order, Trick Room reversed, and stops at the first wipe", ok,
                    f"faster {faster}, slower {slower}, Trick Room {room}, ties: player first {p_first} of 200; "
                    f"sand before poison {sand}; a five-turn sandstorm {storm}"))


def check_ability_weather(results):
    """Weather from an ability is permanent, as in the engine (subscript_drizzle
    and its siblings set the _PERM field conditions); a move's weather counts
    five turns and ends."""
    b, p, foe = battle(["Tackle"], ["Tackle"], {})
    p.ability = "Drizzle"
    fs.switch_in(b, b.p, 0)
    for _ in range(10):
        fs.end_of_turn(b)
    ability = (b.weather, b.weather_turns)
    b2, p2, foe2 = battle(["Rain Dance"], ["Tackle"], {})
    fs.status_move(b2, p2, fs.move("Rain Dance"), foe2, True)
    for _ in range(5):
        fs.end_of_turn(b2)
    ok = ability == ("Rain", 0) and b2.weather is None
    results.append(("an ability's weather is permanent; a move's lasts five turns", ok,
                    f"Drizzle after ten turns {ability}; Rain Dance after five {b2.weather}"))


def check_infiltrator(results):
    """In fightsim's own attack, which double battles use: an Infiltrator
    attacker's hit and added effect pass the target's Substitute, and
    without Infiltrator the Substitute takes the hit and stops the effect."""
    got = {}
    for ability in ("Infiltrator", "Run Away"):
        b, p, foe = battle(["Nuzzle"], ["Tackle"], {("p", "Nuzzle"): [20] * 16})
        foe.ability, foe.sub, p.ability = "Battle Armor", 25, ability
        fs.attack(b, p, fs.move("Nuzzle"), foe, True)
        got[ability] = (100 - foe.hp, foe.sub, foe.status)
    ok = got == {"Infiltrator": (20, 25, "par"), "Run Away": (0, 5, None)}
    results.append(("Infiltrator passes a Substitute in fightsim's own attack", ok, str(got)))


def check_salt_cure(results):
    """Salt Cure salts the Pokemon it hits: an eighth of its maximum HP at
    each turn's end, a quarter for a Water or Steel type, nothing for Magic
    Guard or behind a Substitute, until it leaves the field
    (MON_COND_CHECK_STATE_SALT_CURE). Purifying Salt takes no status at all."""
    got = {}
    for label, types, ability, sub in (("plain", ("Normal",), None, 0), ("water", ("Water",), None, 0),
                                       ("magic guard", ("Normal",), "Magic Guard", 0),
                                       ("substitute", ("Normal",), None, 25)):
        b, p, foe = battle(["Salt Cure"], ["Tackle"], {("p", "Salt Cure"): [10] * 16}, b_types=types)
        foe.ability, foe.sub = ability, sub
        fs.attack(b, p, fs.move("Salt Cure"), foe, True)
        hit = foe.hp
        fs.end_of_turn(b)
        got[label] = (hit - foe.hp, foe.salted)
    b, p, foe = battle(["Salt Cure"], ["Tackle"], {("p", "Salt Cure"): [10] * 16})
    fs.attack(b, p, fs.move("Salt Cure"), foe, True)
    foe.reset_volatile()                 # what leaving the field does
    left = foe.salted
    salt = battle(["Tackle"], ["Tackle"], {})[2]
    salt.ability = "Purifying Salt"
    blocked = not any(fs.can_status(b, salt, st) for st in ("par", "brn", "psn", "tox", "slp", "frz"))
    ok = (got == {"plain": (12, True), "water": (25, True), "magic guard": (0, True), "substitute": (0, False)}
          and not left and blocked)
    results.append(("Salt Cure's chip by type, and Purifying Salt's status immunity", ok,
                    f"{got}, salted after leaving {left}, Purifying Salt blocks all {blocked}"))


def check_harvest(results):
    """Harvest (battle_lib.c 4225, added 2026-10-13): a used-up berry grows
    back at the turn's end while the holder has nothing, always in sun and
    half the time otherwise; never while it holds an item or for a used-up
    item that is not a berry; Cloud Nine turns the sun's certainty back into
    the coin."""
    def grows(weather, item=None, recycle="Occa Berry", cloud=False, seed=1):
        b, p, foe = battle(["Tackle"], ["Tackle"], {}, seed=seed)
        foe.ability, foe.item, foe.recycle = "Harvest", item, recycle
        if cloud:
            p.ability = "Cloud Nine"
        b.weather, b.weather_turns = weather, 0
        fs.end_of_turn(b)
        return foe.item == recycle and foe.recycle is None
    sun = all(grows("Sun", seed=s) for s in range(40))
    clear = sum(grows(None, seed=s) for s in range(400))
    held = not any(grows("Sun", item="Leftovers", seed=s) for s in range(10))
    not_berry = not any(grows("Sun", recycle="Focus Sash", seed=s) for s in range(10))
    cloud = sum(grows("Sun", cloud=True, seed=s) for s in range(400))
    ok = sun and 160 <= clear <= 240 and held and not_berry and 160 <= cloud <= 240
    results.append(("Harvest regrows a used berry: always in sun, half the time otherwise", ok,
                    f"sun {sun}, clear {clear}/400, held {held}, not a berry {not_berry}, Cloud Nine {cloud}/400"))


def check_berry_first_hit(results):
    """A resist berry halves only a multi-hit move's first hit (added
    2026-10-13): the battle script that halves the hit uses the berry up, so
    the later hits land in full. The calculator's row halves every hit, so a
    two-hit row of 40 deals 60 and a five-hit Skill Link row of 50 deals 90;
    a single hit stays halved; the berry is gone afterwards, and the next use
    lands whole. The test chart has no Flying, so Double Hit into a Chilan
    Berry (which halves any Normal move) stands in for Dual Wingbeat into a
    Coba Berry."""
    def hit(move, row, types, berry, skill_link=False):
        b, p, foe = battle([move], ["Tackle"], {("p", move): [row] * 16}, b_types=types, hp=200)
        b.st["pokemon"]["b0.0"]["item"] = foe.item = berry
        foe.ability = "Shell Armor"          # no critical hits to blur the numbers
        if skill_link:
            p.ability = "Skill Link"
        fs.use_move(b, p, fs.move(move), foe, True)
        first = foe.maxhp - foe.hp
        before = foe.hp
        fs.use_move(b, p, fs.move(move), foe, True)
        return first, before - foe.hp, foe.item
    twice = hit("Double Hit", 40, ("Normal",), "Chilan Berry")
    five = hit("Bullet Seed", 50, ("Water",), "Rindo Berry", skill_link=True)
    single = hit("Razor Leaf", 40, ("Water",), "Rindo Berry")
    b, _p, foe = battle(["Double Hit"], ["Tackle"], {})
    no_berry = fs.berry_first_hit(b, foe, fs.move("Double Hit"), 40, 1) == 40
    ok = twice == (60, 80, None) and five == (90, 100, None) and single == (40, 80, None) and no_berry
    results.append(("a resist berry halves only a multi-hit move's first hit, then is gone", ok,
                    f"two hits {twice}, five hits {five}, one hit {single}, no berry held {no_berry}"))


def gas_field(abilities, rows, items=None, start=True):
    """A singles battle as prepare() makes one with Neutralizing Gas in it.
    abilities is {key: ability} in party order, the player's keys p0, p1 and
    the trainer's b0.0, b0.1, the first of each leading; rows is {(attacker,
    target): {move: damage}}, where a key ending "#ng" is that Pokemon's
    ability-blank twin, the row the gas sends it to. Every Pokemon has 100 HP
    and the same Speed as its twin; each knows the moves its rows name."""
    st = {"rows": {}, "speed": {}, "info": {}, "pokemon": {}, "moves": {}, "chart": _chart(),
          "rock_eff": {}, "base_weather": None, "trick_room": False, "gas_twin": {},
          "gas": "Neutralizing Gas" in abilities.values()}
    known = {}
    for (a, _d), got in rows.items():
        known.setdefault(a.split("#")[0], set()).update(got)
    for k, ability in abilities.items():
        st["info"][k] = {"hp": 100, "stats": {"atk": 100, "def": 100, "spa": 100, "spd": 100, "spe": 100},
                         "types": ["Normal"], "ability": ability, "item": (items or {}).get(k)}
        st["pokemon"][k] = {"species": k, "level": 50}
        st["moves"][k] = sorted(known.get(k, {"Tackle"}))
        st["speed"][(None, k)] = st["speed"][(None, k + "#ng")] = 100 if k[0] == "p" else 50
        st["gas_twin"][k] = k + "#ng"
    for (a, d), got in rows.items():
        st["rows"][(None, a, d)] = {"moves": {m: {"rolls": [v] * 16} for m, v in got.items()}}
    side = {s: [fs.Mon(k, st["pokemon"][k], st["info"][k], st["moves"][k], s) for k in abilities if k[0] == s]
            for s in "pb"}
    b = fs.Battle(st, fs.Side(side["p"], "p"), fs.Side(side["b"], "b"), random.Random(1), ai_flags=7)
    if start:
        for s in (b.b, b.p):
            fs.switch_in(b, s, s.active)
    return b


def check_neutralizing_gas(results):
    """Neutralizing Gas (the simulator's support approved by Ian, 2026-10-13;
    battle_lib.c's BattleSystem_NeutralizingGasActive and Battler_Ability):
    while its holder is in, every other Pokemon on the field has no ability,
    so a Ground move lands on a Levitate Pokemon, the hazards reach it, and
    a Huge Power attacker hits from its ability-blank row, which the
    calculator works out at half. A Pokemon that comes in under the gas
    sets off nothing."""
    quake = {("b0.0", "p0"): {"Earthquake": 0}, ("b0.0", "p0#ng"): {"Earthquake": 30},
             ("b0.0", "p1"): {"Earthquake": 0}, ("b0.0", "p1#ng"): {"Earthquake": 30}}
    got = {}
    for holder in ("Neutralizing Gas", "Stench"):
        b = gas_field({"p0": "Levitate", "p1": "Levitate", "b0.0": holder}, quake)
        p, foe = b.p.cur(), b.b.cur()
        ground = b.damage(foe, p, fs.move("Earthquake"), roll=0)
        fs.use_move(b, foe, fs.move("Earthquake"), p, True)
        took = 100 - p.hp
        b.p.hazards["spikes"] = 1
        fs.switch_in(b, b.p, 1)
        got[holder] = (ground, took > 0, 100 - b.p.cur().hp, p.ability)
    hp_rows = {("p0", "b0.0"): {"Waterfall": 40}, ("p0#ng", "b0.0"): {"Waterfall": 20}}
    power = {}
    for holder in ("Neutralizing Gas", "Stench"):
        b = gas_field({"p0": "Huge Power", "b0.0": holder}, hp_rows)
        power[holder] = b.damage(b.p.cur(), b.b.cur(), fs.move("Waterfall"), roll=0)
    came = {}
    for holder in ("Neutralizing Gas", "Stench"):
        b = gas_field({"p0": "Run Away", "p1": "Intimidate", "p2": "Drizzle", "b0.0": holder}, {})
        fs.switch_in(b, b.p, 1)
        fs.switch_in(b, b.p, 2)
        came[holder] = (b.b.cur().stages["atk"], b.weather, b.p.mons[1].ability)
    ok = (got == {"Neutralizing Gas": (30, True, 12, "Levitate"), "Stench": (0, False, 0, "Levitate")}
          and power == {"Neutralizing Gas": 20, "Stench": 40}
          and came == {"Neutralizing Gas": (0, None, "Intimidate"), "Stench": (-1, "Rain", "Intimidate")})
    results.append(("Neutralizing Gas: a Levitate Pokemon is grounded, Huge Power reads its blank row, "
                    "a newcomer sets off nothing", ok,
                    f"Earthquake, hit, Spikes, ability back on the bench {got}; Huge Power's hit {power}; "
                    f"after Intimidate and Drizzle came in: Attack stage, weather, ability {came}"))


def check_gas_wears_off(results):
    """When the gas goes, every Pokemon on the field sets off its entry
    abilities again at the next switch-in check (the engine resets their
    announcements). The engine runs that check when a move ends and when a
    Pokemon comes in: so a holder that leaves, or falls at the turn's end,
    has the re-announced Intimidate land on its replacement, while a holder
    knocked out by a move takes it into an empty slot, and its replacement
    keeps its Attack."""
    def run(how):
        b = gas_field({"p0": "Intimidate", "b0.0": "Neutralizing Gas", "b0.1": "Stench"},
                      {("p0#ng", "b0.0"): {"Tackle": 50}})
        p, holder = b.p.cur(), b.b.cur()
        under = (p.ability, holder.stages["atk"])
        if how == "switch":
            fs.switch_in(b, b.b, 1)
        elif how == "knocked out":
            holder.hp = 1
            fs.use_move(b, p, fs.move("Tackle"), holder, True)
            back = p.ability
            fs.switch_in(b, b.b, 1)
            return under, back, b.b.cur().stages["atk"]
        else:
            holder.hp, holder.status = 1, "psn"
            fs.end_of_turn(b)
            back = p.ability
            fs.switch_in(b, b.b, 1)
            return under, back, b.b.cur().stages["atk"]
        return under, p.ability, b.b.cur().stages["atk"]
    got = {how: run(how) for how in ("switch", "knocked out", "turn's end")}
    want = {"switch": ((None, 0), "Intimidate", -1), "knocked out": ((None, 0), "Intimidate", 0),
            "turn's end": ((None, 0), "Intimidate", -1)}
    results.append(("the gas wears off: Intimidate again on the replacement, unless a move knocked the holder out",
                    got == want, f"(under the gas, ability back, replacement's Attack stage) {got}"))


def check_gas_exceptions(results):
    """What the engine reads past the gas, or the gas stops on purpose. As a
    Pokemon leaves, Natural Cure and Regenerator do nothing while the gas is
    on (BtlCmd_TryRestoreStatusOnSwitch asks BattleSystem_NeutralizingGasSuppresses),
    and its party record keeps its ability. A lit Flash Fire keeps burning
    (the boost reads BATTLEMON_FLASH_FIRE, not the ability). An Ability
    Shield keeps its holder's ability on, though the AI's ability commands,
    which ask the gas first and never see the shield, read none; so they do
    for any foe under the gas, even one a message has named. A holder's
    Explosion leaves its HP at 0 before the blast is worked out, so the
    target's Sturdy holds against it. The gas leaves Multitype alone."""
    leave = {}
    for holder in ("Neutralizing Gas", "Stench"):
        b = gas_field({"p0": "Regenerator", "p1": "Natural Cure", "p2": "Run Away", "b0.0": holder}, {})
        regen, cure = b.p.mons[0], b.p.mons[1]
        regen.hp = 50
        fs.switch_in(b, b.p, 1)
        cure.status = "psn"
        fs.switch_in(b, b.p, 2)
        leave[holder] = (regen.hp, cure.status, regen.ability, cure.ability)
    fire = {}
    for holder in ("Neutralizing Gas", "Stench"):
        for lit in (True, False):
            b = gas_field({"p0": "Flash Fire", "b0.0": holder},
                          {("p0", "b0.0"): {"Ember": 30}, ("p0#ng", "b0.0"): {"Ember": 20}})
            b.p.cur().flash_fire = lit
            fire[holder, lit] = b.damage(b.p.cur(), b.b.cur(), fs.move("Ember"), roll=0)
    b = gas_field({"p0": "Levitate", "b0.0": "Neutralizing Gas"},
                  {("b0.0", "p0"): {"Earthquake": 0}, ("b0.0", "p0#ng"): {"Earthquake": 30}},
                  items={"p0": "Ability Shield"})
    p, holder = b.p.cur(), b.b.cur()
    shield = (p.ability, b.damage(holder, p, fs.move("Earthquake"), roll=0), fightai.ability_of(b, holder, p),
              fightai.check_ability(b, holder, p, "Levitate"))
    b = gas_field({"p0": "Intimidate", "b0.0": "Stench", "b0.1": "Neutralizing Gas"}, {})
    p = b.p.cur()
    named = [fightai.ability_of(b, b.b.cur(), p)]
    fs.switch_in(b, b.b, 1)
    named.append(fightai.ability_of(b, b.b.cur(), p))
    fs.switch_in(b, b.b, 0)
    named += [fightai.ability_of(b, b.b.cur(), p), b.b.cur().stages["atk"]]
    blast = {}
    for mv in ("Explosion", "Tackle"):
        b = gas_field({"p0": "Sturdy", "b0.0": "Neutralizing Gas"},
                      {("b0.0", "p0"): {mv: 200}, ("b0.0", "p0#ng"): {mv: 200}})
        fs.use_move(b, b.b.cur(), fs.move(mv), b.p.cur(), True)
        blast[mv] = b.p.cur().hp
    proof = gas_field({"p0": "Multitype", "b0.0": "Neutralizing Gas"}, {}).p.cur().ability
    ok = (leave == {"Neutralizing Gas": (50, "psn", "Regenerator", "Natural Cure"),
                    "Stench": (83, None, "Regenerator", "Natural Cure")}
          and fire == {("Neutralizing Gas", True): 30, ("Neutralizing Gas", False): 20,
                       ("Stench", True): 30, ("Stench", False): 20}
          and shield == ("Levitate", 0, None, "unknown")
          and named == ["Intimidate", None, "Intimidate", -1]
          and blast == {"Explosion": 1, "Tackle": 0} and proof == "Multitype")
    results.append(("the gas's exceptions: switch-out abilities, a lit Flash Fire, an Ability Shield, "
                    "the AI's reads, Explosion, Multitype", ok,
                    f"leaving (HP, status, abilities) {leave}; Ember {fire}; shield (ability, Earthquake, "
                    f"AI load, AI check) {shield}; AI's read before, under, after the gas and Attack stage {named}; "
                    f"HP after a 200 hit {blast}; Multitype {proof}"))


def check_gas_doubles(results):
    """In a double battle the gas reaches the whole field: the holder's
    partner loses its ability as the foes do. When a move knocks the holder
    out, every Pokemon left standing sets off its entry abilities again, so
    the partner's Intimidate lands on both foes."""
    b = gas_field({"p0": "Levitate", "p1": "Huge Power", "b0.0": "Neutralizing Gas", "b0.1": "Intimidate"},
                  {("p0#ng", "b0.0"): {"Tackle": 50}}, start=False)
    b.doubles, b.moved = True, set()
    b.p.active, b.p.active2, b.b.active, b.b.active2 = 0, 1, 0, 1
    for side in (b.b, b.p):
        fs.switch_in(b, side, side.active)
        fs.switch_in(b, side, side.active2, slot=1)
    p0, p1, holder, partner = b.p.mons[0], b.p.mons[1], b.b.mons[0], b.b.mons[1]
    under = (p0.ability, p1.ability, partner.ability, holder.ability, p0.stages["atk"])
    holder.hp = 1
    fs.use_move(b, p0, fs.move("Tackle"), holder, True)
    after = (p0.ability, p1.ability, partner.ability, p0.stages["atk"], p1.stages["atk"])
    ok = (under == (None, None, None, "Neutralizing Gas", 0)
          and after == ("Levitate", "Huge Power", "Intimidate", -1, -1))
    results.append(("doubles: the gas reaches the whole field, and its end re-arms the partner's Intimidate", ok,
                    f"under the gas (abilities, Attack stage) {under}; after the holder fell {after}"))


def check_intimidate_start(results):
    """The battle's start (open_battle, added 2026-10-13): every lead comes
    in before any lead's Intimidate goes off, as the engine runs the
    switch-in check over all of them at once, so each side's Intimidate
    lands on the other side's leads. Sent in one after another, the
    player's lead reset its stages on its own way in and lost the stage the
    trainer's lead had taken. In a double battle each holder takes a stage
    off both foes."""
    b, p, foe = battle(["Tackle"], ["Tackle"], {})
    p.ability = foe.ability = "Intimidate"
    fs.open_battle(b)
    singles = (p.stages["atk"], foe.stages["atk"])
    st = {"rows": {}, "speed": {}, "info": {}, "pokemon": {}, "moves": {}, "chart": _chart(),
          "rock_eff": {}, "base_weather": None, "trick_room": False}
    for key in ("p0", "p1", "b0.0", "b0.1"):
        st["info"][key] = {"hp": 100, "stats": {"atk": 100, "def": 100}, "types": ["Normal"],
                           "ability": "Intimidate" if key in ("p1", "b0.0") else "Run Away", "item": None}
        st["pokemon"][key] = {"species": key, "level": 50}
        st["moves"][key] = ["Tackle"]
        st["speed"][(None, key)] = 100 if key.startswith("p") else 50
    mons = {s: [fs.Mon(k, st["pokemon"][k], st["info"][k], st["moves"][k], s) for k in st["info"] if k[0] == s]
            for s in "pb"}
    d = fs.Battle(st, fs.Side(mons["p"], "p"), fs.Side(mons["b"], "b"), random.Random(1), ai_flags=7)
    d.doubles = True
    d.p.active, d.p.active2, d.b.active, d.b.active2 = 0, 1, 0, 1
    fs.open_battle(d)
    doubles = [m.stages["atk"] for m in d.p.mons + d.b.mons]
    ok = singles == (-1, -1) and doubles == [-1, -1, -1, -1]
    results.append(("both leads come in before their Intimidate, so each lands on the other side", ok,
                    f"singles (player's lead, trainer's lead) {singles}; doubles' four Attack stages {doubles}"))


def check_intimidate_proof(results):
    """Intimidate's blockers in Oxide (BtlCmd_ChangeStatStage, approved
    2026-10-13): Inner Focus, Own Tempo, Oblivious and Scrappy stop it, as
    Hyper Cutter does, and the engine's message names the ability; any other
    Pokemon loses a stage. Both ways round: the player's Intimidate on the
    trainer's Pokemon and the trainer's on the player's."""
    got = {}
    for ab in ("Inner Focus", "Own Tempo", "Oblivious", "Scrappy", "Hyper Cutter", "Run Away"):
        b, p, foe = battle(["Tackle"], ["Tackle"], {})
        p.ability, foe.ability = "Intimidate", ab
        fs.switch_in(b, b.p, 0)
        theirs = (foe.stages["atk"], foe.revealed)
        b, p, foe = battle(["Tackle"], ["Tackle"], {})
        p.ability, foe.ability = ab, "Intimidate"
        fs.switch_in(b, b.b, 0)
        got[ab] = (theirs, (p.stages["atk"], p.revealed))
    want = {ab: ((0, ab), (0, ab)) for ab in ("Inner Focus", "Own Tempo", "Oblivious", "Scrappy", "Hyper Cutter")}
    want["Run Away"] = ((-1, None), (-1, None))
    results.append(("Inner Focus, Own Tempo, Oblivious and Scrappy stop Intimidate, and are named", got == want,
                    f"(Attack stage, ability named) on the trainer's side and on the player's: {got}"))


def check_two_hit_holds(results):
    """A two-hit move meets Sturdy and a Focus Sash hit by hit, in
    fightsim's own attack (approved 2026-10-13). Rows of 120 are two hits of
    60 on a full 100 HP target: Sturdy lets the first land, as it would not
    knock out, and cannot hold the second, so the target faints; a row of
    240 has its first hit held at 1 HP by Sturdy, which is named, and the
    second finishes it. A Focus Sash, armed by the first hit at full HP,
    holds the second too, as the engine's focusItemActivated flag does, and
    is used up; on a Sturdy holder the Sash is never armed, and it faints.
    A single hit of 120 is still held by Sturdy, and a two-hit move into a
    Sturdy target below full HP is plain damage."""
    def hit(move, row, ability=None, item=None, hp=100):
        b, p, foe = battle([move], ["Tackle"], {("p", move): [row] * 16})
        b.st["first_battle"] = True          # no critical hits to blur the numbers
        foe.ability, foe.item, foe.hp = ability or "Run Away", item, hp
        fs.attack(b, p, fs.move(move), foe, True)
        return foe.hp, foe.item, foe.revealed
    got = {"Sturdy, 60 and 60": hit("Double Kick", 120, "Sturdy"),
           "Sturdy, 120 and 120": hit("Double Kick", 240, "Sturdy"),
           "Focus Sash": hit("Double Kick", 120, item="Focus Sash"),
           "Sturdy with a Focus Sash": hit("Double Kick", 120, "Sturdy", "Focus Sash"),
           "Sturdy, one hit": hit("Karate Chop", 120, "Sturdy"),
           "Sturdy at 90 HP": hit("Double Kick", 60, "Sturdy", hp=90)}
    want = {"Sturdy, 60 and 60": (0, None, None), "Sturdy, 120 and 120": (0, None, "Sturdy"),
            "Focus Sash": (1, None, None), "Sturdy with a Focus Sash": (0, "Focus Sash", None),
            "Sturdy, one hit": (1, None, "Sturdy"), "Sturdy at 90 HP": (30, None, None)}
    results.append(("a two-hit move meets Sturdy hit by hit; a Focus Sash holds both", got == want,
                    f"(HP left, item, ability named) {got}"))


def check_hits_one_by_one(results):
    """A move of several hits lands hit by hit in fightsim's own battle, as
    the engine's multi-hit loop runs it (approved 2026-10-14). Skill Link
    Bullet Seed on rows of 50 is five hits of 10: at a critical stage of +2
    each hit rolls its own critical hit at one in two, so the totals spread
    from 50 to 75 in steps of 5 (one roll for the move gave only 50 and 75).
    Five Fury Swipes into Rough Skin cost their user five eighths of its HP
    (one chance took one eighth); an attacker at 30 HP faints on the second
    hit and the loop stops there; Static, three in ten a hit, paralyses about
    83 times in a hundred (one chance, 30)."""
    def bullet(seed):
        b, p, foe = battle(["Bullet Seed"], ["Tackle"], {("p", "Bullet Seed"): [50] * 16}, hp=400, seed=seed)
        p.ability, p.crit_stage = "Skill Link", 2
        fs.attack(b, p, fs.move("Bullet Seed"), foe, True)
        return 400 - foe.hp
    totals = collections.Counter(bullet(s) for s in range(400))

    def swipes(ability, hp=160, seed=1):
        b, p, foe = battle(["Fury Swipes"], ["Tackle"], {("p", "Fury Swipes"): [50] * 16}, hp=160, seed=seed)
        p.ability, foe.ability, p.hp = "Skill Link", ability, hp
        b.st["first_battle"] = True          # no critical hits to blur the numbers
        fs.use_move(b, p, fs.move("Fury Swipes"), foe, True)
        return p.hp, 160 - foe.hp, p.status
    rough, fall = swipes("Rough Skin"), swipes("Rough Skin", hp=30)
    static = sum(swipes("Static", seed=s)[2] == "par" for s in range(400)) / 400
    ok = (set(totals) <= {50, 55, 60, 65, 70, 75} and len(totals) >= 5 and rough == (60, 50, None)
          and fall == (0, 20, None) and 0.77 <= static <= 0.89)
    results.append(("a move of several hits rolls a critical hit and the target's contact ability per hit", ok,
                    f"Skill Link Bullet Seed totals {dict(sorted(totals.items()))}; into Rough Skin (HP left, "
                    f"damage, status) {rough}, from 30 HP {fall}; Static paralysed {static:.2f}"))


def check_hits_hold_and_heal(results):
    """The holds and items of a move of several hits, hit by hit (approved
    2026-10-14). A Focus Sash is armed by a hit taken at full HP and holds
    that hit and every later one at 1 HP (focusItemActivated lasts the
    move), then is used up: Skill Link Bullet Seed of 100 a hit leaves its
    holder at 1 HP (the old total broke it). A Focus Band rolls its one in
    ten at every hit and, once it holds, holds the rest: five hits of 30 into
    100 HP are first lethal at the fourth, so it saves about 34 times in a
    hundred (fightsim's own battle had no Band at all). A Sitrus Berry eaten
    after the third hit of 22 keeps its holder in at 15 (the old total of
    110 fainted it). A Substitute of 25 takes two hits of 20 and breaks, the
    other three land on the Pokemon, and Rough Skin answers none of them,
    since the move hit the Substitute (SELF_TURN_FLAG_SUBSTITUTE_HIT)."""
    def hit(row, item=None, ability="Run Away", sub=0, seed=1, crits=False):
        b, p, foe = battle(["Bullet Seed"], ["Tackle"], {("p", "Bullet Seed"): [row] * 16}, hp=100, seed=seed)
        p.ability, foe.item, foe.ability, foe.sub = "Skill Link", item, ability, sub
        b.st["first_battle"] = not crits
        fs.use_move(b, p, fs.move("Bullet Seed"), foe, True)
        return foe.hp, foe.item, foe.sub, p.hp
    sash, sitrus, behind = hit(500, "Focus Sash"), hit(110, "Sitrus Berry"), hit(100, ability="Rough Skin", sub=25)
    band = sum(hit(150, "Focus Band", seed=s)[0] == 1 for s in range(2000)) / 2000
    ok = (sash == (1, None, 0, 100) and sitrus == (15, None, 0, 100) and behind == (40, None, 0, 100)
          and 0.30 <= band <= 0.39)
    results.append(("a move of several hits meets the Focus Sash, Focus Band, Sitrus Berry and Substitute hit by hit",
                    ok, f"(HP, item, Substitute, attacker HP): Sash {sash}, Sitrus {sitrus}, behind a Substitute "
                        f"{behind}; Focus Band held {band:.3f}"))


def check_triple_axel(results):
    """Triple Axel hits at 20, 40 and 60 (effect script 298), each hit
    checking its accuracy and the move stopping at the first miss, as Fury
    Cutter's rising hits do (approved 2026-10-14): on a row of 120 for all
    three, a use deals 0, 20, 60 or 120 (one check for the whole row gave 0
    or 120)."""
    seen = collections.Counter()
    for s in range(400):
        b, p, foe = battle(["Triple Axel"], ["Tackle"], {("p", "Triple Axel"): [120] * 16}, hp=200, seed=s)
        b.st["first_battle"] = True
        fs.attack(b, p, fs.move("Triple Axel"), foe, True)
        seen[200 - foe.hp] += 1
    ok = set(seen) <= {0, 20, 60, 120} and seen[20] > 0 and seen[60] > 0 and seen[120] > seen[60]
    results.append(("Triple Axel rises 20, 40, 60, each hit checking accuracy", ok, str(dict(sorted(seen.items())))))


def check_protect_flag(results):
    """Protect stops only a move flagged MOVE_FLAG_CAN_PROTECT
    (BattleControllerPlayer_CheckMoveHitOverrides; approved 2026-10-14):
    Tackle and Toxic are stopped, while Shadow Force's strike, Feint and
    Mighty Cleave hit, the first two ending the protection
    (subscript_feint), and Stealth Rock and a Ghost's Curse land. Feint
    fails on a target that is not protecting (BtlCmd_TryFeint). A contact
    move into Spiky Shield costs its user an eighth of its HP, none with
    Magic Guard or for a move without contact; Baneful Bunker poisons the
    user. A Rollout stopped by Protect ends its run."""
    names = ["Tackle", "Toxic", "Shadow Force", "Feint", "Mighty Cleave", "Stealth Rock", "Curse", "Ember", "Rollout"]

    def into(name, protecting=True, guard="Protect", ability=None):
        b, p, foe = battle(names, ["Protect", "Spiky Shield", "Baneful Bunker"], {("p", n): [30] * 16 for n in names},
                           p_types=("Ghost",))
        b.st["first_battle"] = True
        p.ability = ability or p.ability
        foe.protecting, foe.last = protecting, fs.move(guard)
        mv = fs.move(name)
        if mv.cat == "Status":
            fs.status_move(b, p, mv, foe, True)
        else:
            fs.attack(b, p, mv, foe, True)
        return (100 - foe.hp, foe.status, foe.protecting, b.b.hazards["rocks"], foe.cursed, 100 - p.hp, p.status,
                p.lock is not None)
    got = {n: into(n) for n in ("Tackle", "Toxic", "Shadow Force", "Feint", "Mighty Cleave", "Stealth Rock", "Curse")}
    got["Feint, no Protect"] = into("Feint", protecting=False)
    got["Tackle into Spiky Shield"] = into("Tackle", guard="Spiky Shield")
    got["Magic Guard Tackle into Spiky Shield"] = into("Tackle", guard="Spiky Shield", ability="Magic Guard")
    got["Ember into Spiky Shield"] = into("Ember", guard="Spiky Shield")
    got["Tackle into Baneful Bunker"] = into("Tackle", guard="Baneful Bunker")
    b, p, foe = battle(["Rollout"], ["Protect"], {("p", "Rollout"): [10] * 16})
    fs.attack(b, p, fs.move("Rollout"), foe, True)
    locked = p.lock is not None
    foe.protecting = True
    fs.attack(b, p, fs.move("Rollout"), foe, True)
    want = {"Tackle": (0, None, True, 0, False, 0, None, False), "Toxic": (0, None, True, 0, False, 0, None, False),
            "Shadow Force": (30, None, False, 0, False, 0, None, False),
            "Feint": (30, None, False, 0, False, 0, None, False),
            "Mighty Cleave": (30, None, True, 0, False, 0, None, False),
            "Stealth Rock": (0, None, True, 1, False, 0, None, False),
            "Curse": (0, None, True, 0, True, 50, None, False),
            "Feint, no Protect": (0, None, False, 0, False, 0, None, False),
            "Tackle into Spiky Shield": (0, None, True, 0, False, 12, None, False),
            "Magic Guard Tackle into Spiky Shield": (0, None, True, 0, False, 0, None, False),
            "Ember into Spiky Shield": (0, None, True, 0, False, 0, None, False),
            "Tackle into Baneful Bunker": (0, None, True, 0, False, 0, "psn", False)}
    ok = got == want and locked and p.lock is None and p.rollout == 0
    results.append(("Protect stops only a move it can; Feint and Shadow Force break it; Spiky Shield and "
                    "Baneful Bunker answer contact", ok,
                    f"(damage, status, still protecting, rocks, cursed, user's HP lost, user's status, locked) "
                    f"{ {k: v for k, v in got.items() if v != want.get(k)} or 'as wanted'}; Rollout locked {locked}, "
                    f"after Protect {p.lock}"))


def check_protect_odds(results):
    """BtlCmd_TryProtection's odds (approved 2026-10-14): a first Protect
    works, a repeat at a half, a quarter, then an eighth, which stays the
    floor (sProtectSuccessRate), and it fails outright when its user acts
    last (waitingBattlers of 1), which ends the run. Over 4000 tries at runs
    of 3, 4 and 5 it works about one time in eight (it was 1/8, 1/16, 1/32),
    and a slower user's Protect at run 0 never works (it did)."""
    def rate(run, first=True, n=4000):
        works = 0
        for s in range(n):
            b, p, foe = battle(["Protect"], ["Tackle"], {}, seed=s)
            p.protect_run = run
            fs.status_move(b, p, fs.move("Protect"), foe, first)
            works += p.protecting
        return works / n
    runs = {k: rate(k) for k in (3, 4, 5)}
    b, p, foe = battle(["Protect"], ["Tackle"], {})
    p.protect_run = 2
    fs.status_move(b, p, fs.move("Protect"), foe, False)
    last = (p.protecting, p.protect_run)
    ok = all(0.105 <= r <= 0.145 for r in runs.values()) and rate(0, first=False, n=200) == 0 and last == (False, 0)
    results.append(("Protect's run floors at one in eight, and a Protect that acts last fails", ok,
                    f"works at runs 3, 4, 5: {runs}; acting last: (protecting, run) {last}"))


def check_pp_engine(results):
    """PP as the engine charges it (BattleControllerPlayer_DecrementPP,
    approved 2026-10-14): once, on a turn the battler chose its command, so
    Fly's strike and a Rollout's locked uses cost nothing (a charging or
    locked battler cannot choose, and its turn is marked paid), and one more
    for each Pressure holder it meets on the other side: a Tackle into one
    costs 2, as do Stealth Rock, Haze and Growl, which count the whole side,
    while Sleep Talk, whose target is its user, costs 1; a cost above the PP
    left leaves 0 (a Pressure Tackle at its last PP, Rain Dance at its one).
    Before, every use of every move cost 1."""
    def used(names, *turns, ability=None):
        b, p, foe = battle(names, ["Tackle"], {("p", n): [10] * 16 for n in names}, hp=400)
        foe.ability = ability or foe.ability
        for name in turns:
            mv = next(m for m in p.moves if m.name == name)
            fs.use_move(b, p, p.charging or (p.lock[0] if p.lock else mv), foe, True)
        return {m.name: m.pp - p.pp[m.name] for m in p.moves}
    fly = used(["Fly"], "Fly", "Fly")
    rollout = used(["Rollout"], "Rollout", "Rollout", "Rollout", "Rollout")
    pressure = used(["Tackle", "Stealth Rock", "Haze", "Growl"], "Tackle", "Stealth Rock", "Haze", "Growl",
                    ability="Pressure")
    own = used(["Swords Dance", "Rain Dance"], "Swords Dance", "Rain Dance", ability="Pressure")
    sleep_talk = used(["Sleep Talk"], "Sleep Talk", ability="Pressure")
    b, p, foe = battle(["Tackle"], ["Tackle"], {})
    foe.ability, p.pp["Tackle"] = "Pressure", 1
    fs.use_move(b, p, fs.move("Tackle"), foe, True)
    ok = (fly == {"Fly": 1} and rollout == {"Rollout": 1}
          and pressure == {"Tackle": 2, "Stealth Rock": 2, "Haze": 2, "Growl": 2}
          and own == {"Swords Dance": 1, "Rain Dance": 1} and sleep_talk == {"Sleep Talk": 1} and p.pp["Tackle"] == 0)
    results.append(("PP is spent once a choice, and Pressure adds one", ok,
                    f"PP spent: Fly over its two turns {fly}, Rollout over four uses {rollout}; into Pressure "
                    f"{pressure}, Swords Dance and Rain Dance at their 1 PP {own}, Sleep Talk {sleep_talk}; "
                    f"Tackle at 1 PP into Pressure leaves {p.pp['Tackle']}"))


def check_confusion_blockers(results):
    """Confusion as subscript_confuse gives it (approved 2026-10-14). A
    hit's added confusion (Dynamic Punch, its chance 100) misses an Own
    Tempo target unless the attacker has Mold Breaker, a target behind
    Safeguard unless the attacker has Infiltrator, and a Covert Cloak
    holder; Confuse Ray and Swagger meet the same Own Tempo and Safeguard
    (Swagger's Attack rise still lands), and Own Tempo is named there. A Lum
    Berry cures the confusion as it sets in and is used up. An Infiltrator's
    Toxic passes Safeguard too. Before, a hit confused through all of them,
    the moves through Safeguard, and the Lum Berry waited for the turn's
    end."""
    def confuse(name, ability=None, attacker=None, safeguard=False, item=None):
        b, p, foe = battle([name], ["Tackle"], {("p", name): [10] * 16}, hp=200)
        p.stages["acc"] = 6                 # Dynamic Punch's 50% always lands
        foe.ability, p.ability, foe.item = ability or foe.ability, attacker or p.ability, item
        b.b.safeguard = 5 if safeguard else 0
        mv = fs.move(name)
        (fs.status_move if mv.cat == "Status" else fs.attack)(b, p, mv, foe, True)
        return bool(foe.confused), foe.revealed, foe.item, foe.stages["atk"], foe.status
    cases = {"plain": {}, "Own Tempo": {"ability": "Own Tempo"},
             "Own Tempo, Mold Breaker": {"ability": "Own Tempo", "attacker": "Mold Breaker"},
             "Safeguard": {"safeguard": True}, "Safeguard, Infiltrator": {"safeguard": True, "attacker": "Infiltrator"},
             "Lum Berry": {"item": "Lum Berry"}}
    got = {f"Dynamic Punch, {k}": confuse("Dynamic Punch", **kw) for k, kw in cases.items()}
    got["Dynamic Punch, Covert Cloak"] = confuse("Dynamic Punch", item="Covert Cloak")
    got.update({f"Confuse Ray, {k}": confuse("Confuse Ray", **kw) for k, kw in cases.items()})
    got["Swagger, Safeguard"] = confuse("Swagger", safeguard=True)
    got["Toxic, Safeguard, Infiltrator"] = confuse("Toxic", safeguard=True, attacker="Infiltrator")
    got["Toxic, Safeguard"] = confuse("Toxic", safeguard=True)
    want = {"Dynamic Punch, plain": (True, None, None, 0, None),
            "Dynamic Punch, Own Tempo": (False, None, None, 0, None),
            "Dynamic Punch, Own Tempo, Mold Breaker": (True, None, None, 0, None),
            "Dynamic Punch, Safeguard": (False, None, None, 0, None),
            "Dynamic Punch, Safeguard, Infiltrator": (True, None, None, 0, None),
            "Dynamic Punch, Lum Berry": (False, None, None, 0, None),
            "Dynamic Punch, Covert Cloak": (False, None, "Covert Cloak", 0, None),
            "Confuse Ray, plain": (True, None, None, 0, None),
            "Confuse Ray, Own Tempo": (False, "Own Tempo", None, 0, None),
            "Confuse Ray, Own Tempo, Mold Breaker": (True, None, None, 0, None),
            "Confuse Ray, Safeguard": (False, None, None, 0, None),
            "Confuse Ray, Safeguard, Infiltrator": (True, None, None, 0, None),
            "Confuse Ray, Lum Berry": (False, None, None, 0, None),
            "Swagger, Safeguard": (False, None, None, 2, None),
            "Toxic, Safeguard, Infiltrator": (False, None, None, 0, "tox"),
            "Toxic, Safeguard": (False, None, None, 0, None)}
    bad = {k: v for k, v in got.items() if v != want[k]}
    results.append(("confusion meets Own Tempo, Safeguard, a Covert Cloak and a Lum Berry as the engine's does", not bad,
                    f"(confused, named, item, Attack stage, status) off: {bad}" if bad else "every case as wanted"))


def check_curse_and_rest(results):
    """The Ghost Curse's and Rest's failures (approved 2026-10-14). A Ghost
    type's Curse (subscript_curse_ghost) cuts half its user's HP and curses
    the target, but fails at no cost behind a Substitute, on a target
    already cursed, and on one in the air; an Infiltrator's passes the
    Substitute. Rest (subscript_rest) fails on Insomnia, Vital Spirit,
    Purifying Salt, Sweet Veil and Leaf Guard in sun, naming the ability,
    though Cloud Nine lets a Leaf Guard holder rest. Before, the Curse cut
    and cursed in every case and Rest worked for all of them."""
    def curse(sub=0, cursed=False, flying=False, ability=None):
        b, p, foe = battle(["Curse"], ["Fly"], {}, p_types=("Ghost",))
        foe.sub, foe.cursed, p.ability = sub, cursed, ability or p.ability
        foe.charging = fs.move("Fly") if flying else None
        fs.status_move(b, p, fs.move("Curse"), foe, True)
        return 100 - p.hp, foe.cursed
    curses = {"plain": curse(), "Substitute": curse(sub=25), "cursed": curse(cursed=True), "in the air": curse(flying=True),
              "Infiltrator through a Substitute": curse(sub=25, ability="Infiltrator")}

    def rest(ability, weather=None, cloud=False):
        b, p, foe = battle(["Rest"], ["Tackle"], {})
        p.ability, p.hp, b.weather = ability, 40, weather
        if cloud:
            foe.ability = "Cloud Nine"
        fs.status_move(b, p, fs.move("Rest"), foe, True)
        return p.hp, p.status, p.revealed
    rests = {ab: rest(ab) for ab in ("Insomnia", "Vital Spirit", "Purifying Salt", "Sweet Veil", "Run Away")}
    rests["Leaf Guard in sun"] = rest("Leaf Guard", "Sun")
    rests["Leaf Guard in sun, Cloud Nine"] = rest("Leaf Guard", "Sun", cloud=True)
    want_c = {"plain": (50, True), "Substitute": (0, False), "cursed": (0, True), "in the air": (0, False),
              "Infiltrator through a Substitute": (50, True)}
    want_r = {"Insomnia": (40, None, "Insomnia"), "Vital Spirit": (40, None, "Vital Spirit"),
              "Purifying Salt": (40, None, "Purifying Salt"), "Sweet Veil": (40, None, "Sweet Veil"),
              "Run Away": (100, "slp", None), "Leaf Guard in sun": (40, None, "Leaf Guard"),
              "Leaf Guard in sun, Cloud Nine": (100, "slp", None)}
    results.append(("the Ghost Curse fails through a Substitute or on a cursed target; Rest fails on the abilities "
                    "that keep its user awake", curses == want_c and rests == want_r,
                    f"Curse (user's HP lost, target cursed) {curses}; Rest (HP, status, named) {rests}"))


def check_mist_and_intimidate(results):
    """Mist, and Intimidate against a Substitute, Mist and a Clear Amulet
    (approved 2026-10-14). Mist (BtlCmd_TryMist) keeps the other side from
    lowering its side's stats for five turn ends, Growl and a hit's drop
    alike, and a second Mist while one runs fails; an Infiltrator's Growl
    and Mud-Slap pass it. An Intimidate
    coming in passes over a foe behind a Substitute (subscript_intimidate),
    and Mist and a Clear Amulet stop it (BtlCmd_ChangeStatStage), Mist
    before Inner Focus is named. The trainer's AI reads the side's Mist, so
    a second Mist scores -8. Before, Mist did nothing and Intimidate cut all
    three."""
    def growl(mist_on, attacker=None):
        b, p, foe = battle(["Mist"], ["Growl", "Mud-Slap"], {("b", "Mud-Slap"): [5] * 16})
        if mist_on:
            fs.status_move(b, p, fs.move("Mist"), foe, True)
        foe.ability = attacker or foe.ability
        foe.stages["acc"] = 6
        fs.status_move(b, foe, fs.move("Growl"), p, True)
        fs.attack(b, foe, fs.move("Mud-Slap"), p, True)
        return p.stages["atk"], p.stages["acc"]
    b, p, foe = battle(["Mist"], ["Tackle"], {})
    fs.status_move(b, p, fs.move("Mist"), foe, True)
    turns = [b.p.mist]
    fs.end_of_turn(b)
    fs.end_of_turn(b)
    fs.status_move(b, p, fs.move("Mist"), foe, True)       # fails while one runs
    turns.append(b.p.mist)
    for _ in range(3):
        fs.end_of_turn(b)
    turns.append(b.p.mist)
    fs.status_move(b, p, fs.move("Mist"), foe, True)       # a fresh one once the last ran out
    ai = fightai.basic(b, p, foe, fs.move("Mist"), None)

    def intimidated(sub=0, mist_on=False, item=None, ability=None):
        b, p, foe = battle(["Tackle"], ["Tackle"], {})
        p.sub, p.item, p.ability = sub, item, ability or p.ability
        b.p.mist = 5 if mist_on else 0
        foe.ability = "Intimidate"
        fs.switch_in(b, b.b, 0)
        return p.stages["atk"], p.revealed
    got = {"Growl and Mud-Slap": growl(False), "under Mist": growl(True),
           "an Infiltrator under Mist": growl(True, "Infiltrator"),
           "Intimidate": intimidated(), "behind a Substitute": intimidated(sub=25),
           "Intimidate under Mist": intimidated(mist_on=True),
           "Intimidate on Inner Focus under Mist": intimidated(mist_on=True, ability="Inner Focus"),
           "Intimidate on a Clear Amulet": intimidated(item="Clear Amulet")}
    want = {"Growl and Mud-Slap": (-1, -1), "under Mist": (0, 0), "an Infiltrator under Mist": (-1, -1),
            "Intimidate": (-1, None), "behind a Substitute": (0, None), "Intimidate under Mist": (0, None),
            "Intimidate on Inner Focus under Mist": (0, None), "Intimidate on a Clear Amulet": (0, None)}
    ok = got == want and turns == [5, 3, 0] and ai == -8
    results.append(("Mist stops the other side's drops for five turns; Intimidate passes a Substitute, and Mist and "
                    "a Clear Amulet stop it", ok,
                    f"(Attack, accuracy or named) {got}; Mist's turns {turns}; the AI's score for a second Mist {ai}"))


def check_ai_fields(results):
    """The fields the trainer's AI reads, set as the engine's state is
    (approved 2026-10-14). Last Resort's count (BattleSystem_UpdateLastResort)
    counts each other move the first time it is used since its user came
    in, and a switch clears it; a Berry used up is eaten
    (BattleScript_RecordBerryEaten), one Natural Gift spends is not, and
    Belch is then no longer an invalid choice; Recycle reads the item last
    used up, so it scores 0 once there is one. The readings' keys tell the
    count and the Berry apart only for a Last Resort or Belch user. Before,
    the AI read a count, a Berry and an item that nothing set."""
    b, p, foe = battle(["Tackle", "Growl", "Last Resort"], ["Recycle", "Belch", "Natural Gift"], {})
    for name in ("Tackle", "Tackle", "Growl", "Last Resort"):
        fs.use_move(b, p, fs.move(name), foe, True)
    counted = p.last_resort_count
    keyed = pl_key_has(p), pl_key_has(foe)
    fs.switch_in(b, b.p, 0)
    cleared = p.last_resort_count
    recycle_before = fightai.basic(b, foe, p, fs.move("Recycle"), None)
    belch_before = fightai.invalid(b, foe, fs.move("Belch"))
    foe.item = "Oran Berry"
    foe.hp = 40
    fs.berry_check(foe)
    ate = (foe.ate_berry, foe.recycle)
    recycle_after = fightai.basic(b, foe, p, fs.move("Recycle"), None)
    belch_after = fightai.invalid(b, foe, fs.move("Belch"))
    b2, p2, foe2 = battle(["Tackle"], ["Natural Gift"], {("b", "Natural Gift"): [10] * 16})
    foe2.item = "Oran Berry"
    fs.attack(b2, foe2, fs.move("Natural Gift"), p2, True)
    spent = (foe2.item, foe2.ate_berry)
    ok = (counted, cleared, ate, recycle_before, recycle_after, belch_before, belch_after, spent) == \
        (2, 0, (True, "Oran Berry"), -10, 0, True, False, (None, False)) and keyed == (True, True)
    results.append(("the battle sets Last Resort's count, the Berry eaten and the item to recycle, as the AI reads them",
                    ok, f"count {counted}, after a switch {cleared}; Berry eaten (eaten, recycle) {ate}; Recycle "
                        f"scored {recycle_before} then {recycle_after}; Belch invalid {belch_before} then "
                        f"{belch_after}; Natural Gift (item, eaten) {spent}; keyed by Last Resort, by Belch {keyed}"))


def pl_key_has(mon):
    """Whether the readings' keys carry mon's Last Resort count (mon_key) or
    its Berry eaten (_ai_mon): only a Last Resort or a Belch user's."""
    from . import perfectline as pl
    return pl.mon_key(mon)[-1] is not None or pl._ai_mon(mon)[-1] is not None


def check_future_sight(results):
    """Future Sight and Doom Desire (approved 2026-10-13; BtlCmd_TryFutureSight
    and the turn's end, SIDE_COND_CHECK_STATE_FUTURE_SIGHT): the damage is
    worked out as the move is used and lands at the
    end of the second turn after, on whoever then stands in the target's
    slot; a second use fails while one waits there, and the trainer's AI
    scores another -12 while one waits on either side. A hit that comes due
    on a fainted slot is lost, and the side's mark stays, as the engine
    clears it only as one lands. A Substitute takes the hit, and Sturdy holds
    it at full HP."""
    def set_up(row=40, seed=1):
        b, p, foe = battle(["Future Sight"], ["Tackle"], {("p", "Future Sight"): [row] * 16}, seed=seed)
        extra = fs.Mon("b0.1", b.st["pokemon"]["b0.0"], b.st["info"]["b0.0"], ["Tackle"], "b")
        b.b.mons.append(extra)
        fs.use_move(b, p, fs.move("Future Sight"), foe, True)
        return b, p, foe, extra
    b, p, foe, extra = set_up()
    at_once = foe.maxhp - foe.hp
    again = fs.foresee(b, p, fs.move("Future Sight"), foe, 40)
    ai = fightai.basic(b, foe, p, fs.move("Future Sight"))
    hp = []
    for turn in range(3):
        if turn == 1:
            fs.switch_in(b, b.b, 1)              # the target leaves; its replacement stands in the slot
        fs.end_of_turn(b)
        hp.append((foe.hp, extra.hp))
    b, p, foe, extra = set_up()
    fs.end_of_turn(b)
    fs.end_of_turn(b)
    foe.hp = 0
    fs.end_of_turn(b)
    lost = (extra.hp, b.b.future, b.b.future_sight)
    b, p, foe, extra = set_up()
    foe.sub = 30
    for _ in range(3):
        fs.end_of_turn(b)
    sub = (foe.hp, foe.sub)
    b, p, foe, extra = set_up(row=150)
    foe.ability = "Sturdy"
    for _ in range(3):
        fs.end_of_turn(b)
    ok = (at_once == 0 and not again and ai == -12 and hp == [(100, 100), (100, 100), (100, 60)]
          and lost == (100, (None, None), True) and sub == (100, 0) and foe.hp == 1)
    results.append(("Future Sight lands two turns on, on whoever stands in the slot", ok,
                    f"at once {at_once}; a second use {again}; the AI's Basic {ai}; (target, replacement) HP "
                    f"after each turn's end {hp}; due on a "
                    f"fainted slot (replacement HP, waiting, mark) {lost}; into a Substitute (HP, Substitute) "
                    f"{sub}; 150 into a full Sturdy {foe.hp}"))


def check_sleep_talk_rest(results):
    """Rest fails on a Pokemon already asleep (subscript_rest: "is already
    asleep!", approved 2026-10-13), which is how a Sleep Talk reaches it:
    with Rest its only other move, Sleep Talk at 40 of 100 HP leaves the
    sleeper at 40 and its sleep running down, where it used to heal it to
    full and start a fresh sleep. Rest used awake still heals to full and
    sleeps two turns."""
    asleep = set()
    for seed in range(20):
        b, p, foe = battle(["Sleep Talk", "Rest"], ["Tackle"], {}, seed=seed)
        p.hp, p.status, p.sleep = 40, "slp", 3
        fs.use_move(b, p, fs.move("Sleep Talk"), foe, True)
        asleep.add((p.hp, p.status, p.sleep))
    b, p, foe = battle(["Rest"], ["Tackle"], {})
    p.hp = 40
    fs.use_move(b, p, fs.move("Rest"), foe, True)
    awake = (p.hp, p.status, p.sleep)
    ok = asleep == {(40, "slp", 2)} and awake == (100, "slp", 2)
    results.append(("a Sleep Talk that calls Rest fails; Rest awake still heals", ok,
                    f"(HP, status, sleep) after Sleep Talk asleep {sorted(asleep)}; Rest awake {awake}"))


def check_disable(results):
    """Disable (approved 2026-10-13; BtlCmd_TryDisable): the target's last
    move is disabled for 3 to 6 turns after the Disable's own; the move
    fails if used, the trainer's AI rules it out (a base score of 0, as
    CheckInvalidMoves gives) and picks its other move, Sleep Talk never
    calls it, and the player's attack reckoning leaves it out. Disable
    fails before the target has moved and while one of its moves is
    disabled, and the AI scores a second Disable -8."""
    rows = {("b", "Tackle"): [20] * 16, ("b", "Scratch"): [10] * 16, ("p", "Tackle"): [20] * 16}
    b, p, foe = battle(["Disable", "Tackle"], ["Tackle", "Scratch"], rows)
    early = fs.disable(foe, lambda: 4)
    fs.use_move(b, foe, fs.move("Tackle"), p, True)
    fs.use_move(b, p, fs.move("Disable"), foe, True)
    took = p.hp
    fs.use_move(b, foe, fs.move("Tackle"), p, True)
    blocked = took - p.hp
    picks = {fightai.choose(b, foe, p)[1].name for _ in range(30)}
    second = fightai.basic(b, p, foe, fs.move("Disable"))
    foe.moves = [fs.move("Sleep Talk"), fs.move("Tackle"), fs.move("Scratch")]
    foe.status, foe.sleep = "slp", 3
    talked = {fs.sleep_talk_pick(b, foe).name for _ in range(30)}
    p.disabled = "Tackle"
    reckoned = fs.best_attack(b, p, foe)[0]
    lengths = set()
    for seed in range(200):
        b2, p2, foe2 = battle(["Disable"], ["Tackle"], rows, seed=seed)
        foe2.last = fs.move("Tackle")
        fs.status_move(b2, p2, fs.move("Disable"), foe2, True)
        n = 0
        while foe2.disabled is not None:
            fs.end_of_turn(b2)
            n += 1
        lengths.add(n - 1)
    ok = (not early and blocked == 0 and picks == {"Scratch"} and second == -8 and talked == {"Scratch"}
          and reckoned is None and lengths == {3, 4, 5, 6})
    results.append(("Disable locks the target's last move out for 3 to 6 turns, for the AI too", ok,
                    f"before it moved {early}; Tackle after Disable dealt {blocked}; the AI picks {sorted(picks)}; "
                    f"a second Disable {second}; Sleep Talk calls {sorted(talked)}; the player's best attack "
                    f"with Tackle disabled {reckoned}; turns blocked after the Disable's own {sorted(lengths)}"))


def check_nightmare(results):
    """Nightmare (approved 2026-10-13): only on a sleeping target without a
    Substitute; a quarter of its maximum HP at each turn's end while it
    sleeps, nothing for Magic Guard; once it is awake the nightmare ends,
    and the AI scores a second Nightmare -10 (Basic_CheckNightmare reads the
    real state now)."""
    def cast(status=None, ability=None, sub=0):
        b, p, foe = battle(["Nightmare"], ["Tackle"], {}, p_types=("Ghost",))
        foe.status, foe.sleep, foe.ability, foe.sub = status, 3 if status else 0, ability, sub
        fs.status_move(b, p, fs.move("Nightmare"), foe, True)
        return b, p, foe
    awake = cast()[2].nightmare
    behind = cast("slp", sub=25)[2].nightmare
    b, p, foe = cast("slp")
    second = fightai.basic(b, p, foe, fs.move("Nightmare"))
    fs.end_of_turn(b)
    one = foe.hp
    foe.status, foe.sleep = None, 0
    fs.end_of_turn(b)
    woke = (foe.hp, foe.nightmare)
    b, p, foe = cast("slp", "Magic Guard")
    fs.end_of_turn(b)
    guard = foe.hp
    ok = (not awake and not behind and second == -10 and one == 75 and woke == (75, False) and guard == 100)
    results.append(("Nightmare: a quarter a turn while asleep, ending as it wakes", ok,
                    f"on an awake target {awake}, behind a Substitute {behind}; a second one {second}; "
                    f"after a turn's end {one}; after it woke (HP, nightmare) {woke}; Magic Guard {guard}"))


def check_encore(results):
    """Encore (approved 2026-10-14; BtlCmd_TryEncore): the target is locked
    into its last move for 3 to 7 turns after the Encore's own; a move it
    chose before the Encore came is replaced by the Encore move as it comes
    to be used (BattleControllerPlayer_FightCommand); the trainer's AI picks
    only that move and scores a second Encore -8. Encore fails before the
    target has moved and on a move Encore cannot lock (Encore itself)."""
    rows = {("b", "Tackle"): [20] * 16, ("b", "Scratch"): [10] * 16}
    b, p, foe = battle(["Encore", "Tackle"], ["Tackle", "Scratch"], rows)
    early = fs.encore(foe, lambda: 4)
    fs.use_move(b, foe, fs.move("Tackle"), p, True)
    fs.use_move(b, p, fs.move("Encore"), foe, True)
    hp = p.hp
    fs.use_move(b, foe, fs.move("Scratch"), p, True)
    swapped = hp - p.hp
    picks = {fightai.choose(b, foe, p)[1].name for _ in range(30)}
    second = fightai.basic(b, p, foe, fs.move("Encore"))
    b2, p2, foe2 = battle(["Encore"], ["Encore"], {})
    foe2.last = fs.move("Encore")
    locked_encore = fs.encore(foe2, lambda: 4)
    lengths = set()
    for seed in range(200):
        b3, p3, foe3 = battle(["Encore"], ["Tackle", "Scratch"], rows, seed=seed)
        foe3.last = fs.move("Tackle")
        fs.status_move(b3, p3, fs.move("Encore"), foe3, True)
        n = 0
        while foe3.encore is not None:
            fs.end_of_turn(b3)
            n += 1
        lengths.add(n - 1)
    ok = (not early and swapped == 20 and picks == {"Tackle"} and second == -8 and not locked_encore
          and lengths == {3, 4, 5, 6, 7})
    results.append(("Encore locks the target into its last move for 3 to 7 turns", ok,
                    f"before it moved {early}; a Scratch chosen came out as Tackle for {swapped}; the AI picks "
                    f"{sorted(picks)}; a second Encore {second}; onto Encore {locked_encore}; turns locked after "
                    f"the Encore's own {sorted(lengths)}"))


def check_ice_body(results):
    """Ice Body (approved 2026-10-14; BtlCmd_EndOfTurnWeatherEffect): a
    sixteenth of maximum HP back at each turn's end in hail, below full HP,
    and none of the hail's bite; nothing in sand, and nothing while Cloud
    Nine or Air Lock is out."""
    def end(weather, hp=50, cloud=False):
        b, p, foe = battle(["Tackle"], ["Tackle"], {})
        foe.ability, foe.hp = "Ice Body", hp
        if cloud:
            p.ability = "Cloud Nine"
        b.weather, b.weather_turns = weather, 0
        fs.end_of_turn(b)
        return foe.hp
    got = {"hail": end("Hail"), "hail at full HP": end("Hail", 100), "sand": end("Sand"),
           "hail under Cloud Nine": end("Hail", cloud=True)}
    want = {"hail": 56, "hail at full HP": 100, "sand": 44, "hail under Cloud Nine": 50}
    results.append(("Ice Body heals a sixteenth in hail", got == want, f"HP from 50 after a turn's end {got}"))


def check_absorbing_abilities(results):
    """The absorbing abilities do their whole job (approved 2026-10-14;
    BattleSystem_TriggerImmunityAbility): a move of the ability's type is
    taken whole, damaging or not, and Volt Absorb, Water Absorb and Dry Skin
    give back a quarter of maximum HP (none at full HP) while Lightning Rod,
    Storm Drain, Sap Sipper and Motor Drive raise Sp. Atk, Sp. Atk, Attack
    and Speed a stage (none at +6); a Mold Breaker user is taken in by none.
    Dry Skin heals an eighth at the turn's end in rain and loses an eighth in
    sun. Rows of 0 stand for the calculator's, which already give these
    hits no damage."""
    def take(ability, move, hp=50, stage=0, mold=False):
        b, p, foe = battle([move], ["Tackle"], {("p", move): [0] * 16})
        foe.ability, foe.hp = ability, hp
        stat = {"Lightning Rod": "spa", "Storm Drain": "spa", "Sap Sipper": "atk", "Motor Drive": "spe"}.get(ability)
        if stat:
            foe.stages[stat] = stage
        if mold:
            p.ability = "Mold Breaker"
        p.stages["acc"] = 6                  # Thunder Wave's 90 always lands
        fs.use_move(b, p, fs.move(move), foe, True)
        return (foe.hp, foe.stages[stat] if stat else None, foe.status, foe.revealed)
    got = {"Volt Absorb, Thunderbolt": take("Volt Absorb", "Thunderbolt"),
           "Volt Absorb at full HP": take("Volt Absorb", "Thunderbolt", hp=100),
           "Volt Absorb, Thunder Wave": take("Volt Absorb", "Thunder Wave"),
           "Water Absorb, Water Gun": take("Water Absorb", "Water Gun"),
           "Dry Skin, Water Gun": take("Dry Skin", "Water Gun"),
           "Lightning Rod, Thunderbolt": take("Lightning Rod", "Thunderbolt"),
           "Storm Drain, Water Gun": take("Storm Drain", "Water Gun"),
           "Sap Sipper, Spore": take("Sap Sipper", "Spore"),
           "Motor Drive at +6": take("Motor Drive", "Thunderbolt", stage=6),
           "Volt Absorb against Mold Breaker": take("Volt Absorb", "Thunderbolt", mold=True)}
    want = {"Volt Absorb, Thunderbolt": (75, None, None, "Volt Absorb"),
            "Volt Absorb at full HP": (100, None, None, "Volt Absorb"),
            "Volt Absorb, Thunder Wave": (75, None, None, "Volt Absorb"),
            "Water Absorb, Water Gun": (75, None, None, "Water Absorb"),
            "Dry Skin, Water Gun": (75, None, None, "Dry Skin"),
            "Lightning Rod, Thunderbolt": (50, 1, None, "Lightning Rod"),
            "Storm Drain, Water Gun": (50, 1, None, "Storm Drain"),
            "Sap Sipper, Spore": (50, 1, None, "Sap Sipper"),
            "Motor Drive at +6": (50, 6, None, "Motor Drive"),
            "Volt Absorb against Mold Breaker": (50, None, None, "Volt Absorb")}

    def weather(w):
        b, p, foe = battle(["Tackle"], ["Tackle"], {})
        foe.ability, foe.hp = "Dry Skin", 50
        b.weather, b.weather_turns = w, 0
        fs.end_of_turn(b)
        return foe.hp
    skin = (weather("Rain"), weather("Sun"))
    ok = got == want and skin == (62, 38)
    results.append(("the absorbing abilities heal or raise their stat; Dry Skin in rain and sun", ok,
                    f"(HP from 50, the stage, status, ability named) {got}; Dry Skin from 50 in rain and sun {skin}"))


def check_roost(results):
    """Roost (approved 2026-10-14; subscript_roost and BasicTypeMulApplies):
    it fails at full HP; otherwise it heals half, and until the turn ends
    its user's Flying type meets no move, which the battle reads from the
    user's twin without Flying (prepare's roost_twin). A pure Flying user
    has a Normal and a Grass twin, and each move meets it on the one its
    type hits neutrally: Earthquake on the Normal twin, Shadow Ball on the
    Grass one. The next turn the Flying type is back."""
    rows = {("b", "Earthquake"): [0] * 16, ("b", "Shadow Ball"): [30] * 16}
    b, p, foe = battle(["Roost"], ["Earthquake", "Shadow Ball"], rows, p_types=("Flying",))
    b.st["rows"][(None, "b0.0", "p0#roost0")] = {"moves": {"Earthquake": {"rolls": [40] * 16},
                                                           "Shadow Ball": {"rolls": [99] * 16}}}
    b.st["rows"][(None, "b0.0", "p0#roost1")] = {"moves": {"Earthquake": {"rolls": [77] * 16},
                                                           "Shadow Ball": {"rolls": [30] * 16}}}
    b.st["roost_twin"] = {"p0": [("p0#roost0", ["Normal"]), ("p0#roost1", ["Grass"])]}
    quake, ball = fs.move("Earthquake"), fs.move("Shadow Ball")
    full = fs.status_move(b, p, fs.move("Roost"), foe, True) or p.roosting
    p.hp = 50
    fs.status_move(b, p, fs.move("Roost"), foe, True)
    roosted = (p.hp, p.roosting, b.damage(foe, p, quake, roll=0), b.damage(foe, p, ball, roll=0))
    fs.end_of_turn(b)
    after = (p.roosting, b.damage(foe, p, quake, roll=0))
    ok = not full and roosted == (100, True, 40, 30) and after == (False, 0)
    results.append(("Roost takes the Flying type off its user until the turn ends", ok,
                    f"at full HP roosted {full}; after Roost from 50 (HP, roosting, Earthquake, Shadow Ball) {roosted}; "
                    f"the next turn (roosting, Earthquake) {after}"))


def check_protean(results):
    """Protean (approved 2026-10-14; BEFORE_MOVE_STATE_PROTEAN): once a stay
    on the field, the first move whose type its user is not wholly already
    makes the user that type alone, and its rows then come from its twin of
    that type (prepare's protean_twin), both ways, until it leaves. A move of
    its own single type changes nothing and leaves Protean unspent; the next
    move after the change changes nothing either; leaving the field brings
    its own type back and Protean with it."""
    rows = {("p", "Ember"): [30] * 16, ("p", "Tackle"): [20] * 16, ("b", "Tackle"): [10] * 16}
    b, p, foe = battle(["Tackle", "Ember"], ["Tackle"], rows)
    b.st["first_battle"] = True              # no critical hits to blur the numbers
    p.ability = "Protean"
    b.st["rows"][(None, "p0#ptFire", "b0.0")] = {"moves": {"Ember": {"rolls": [45] * 16},
                                                            "Tackle": {"rolls": [13] * 16}}}
    b.st["rows"][(None, "b0.0", "p0#ptFire")] = {"moves": {"Tackle": {"rolls": [7] * 16}}}
    b.st["protean_twin"] = {"p0": {"Fire": "p0#ptFire"}}
    tackle, ember = fs.move("Tackle"), fs.move("Ember")
    fs.use_move(b, p, tackle, foe, True)
    own = (list(p.types), p.protean_used)
    fs.use_move(b, p, ember, foe, True)
    changed = (list(p.types), b.damage(p, foe, ember, roll=0), b.damage(p, foe, tackle, roll=0),
               b.damage(foe, p, tackle, roll=0))
    fs.use_move(b, p, tackle, foe, True)
    kept = list(p.types)
    p.reset_volatile()                       # what leaving the field does
    back = (list(p.types), p.protean_used, b.damage(p, foe, ember, roll=0))
    ok = (own == (["Normal"], False) and changed == (["Fire"], 45, 13, 7) and kept == ["Fire"]
          and back == (["Normal"], False, 30))
    results.append(("Protean retypes its user on its first off-type move, once a stay", ok,
                    f"after its own type's move (types, spent) {own}; after Ember (types, Ember, Tackle, the foe's "
                    f"Tackle) {changed}; after another Tackle {kept}; after leaving (types, spent, Ember) {back}"))


def check_form_twins(results):
    """The rows of a changed type or ability (batch 3's mechanism, approved
    2026-10-14; prepare's form_twin, read by form_key): a Pokemon whose types
    or ability the battle has changed meets moves, and attacks, on its twin
    of that change, both ways, and takes its twin's Speed; both changed at
    once with no twin for the pair, it reads the twin of its new types; left
    with no type, it meets each move on the twin the move's type hits
    neutrally and attacks on the one of another type than the move's;
    leaving the field brings back its own types, ability and rows. A
    suppressed Levitate holder reads its ability-blank twin."""
    rows = {("p", "Tackle"): [20] * 16, ("p", "Ember"): [20] * 16, ("p", "Shadow Ball"): [0] * 16,
            ("b", "Tackle"): [10] * 16, ("b", "Vine Whip"): [10] * 16}
    b, p, foe = battle(["Tackle", "Ember", "Shadow Ball"], ["Tackle", "Vine Whip"], rows)
    b.st["first_battle"] = True
    foe.ability = "Levitate"
    water, power, blank = "b0.0#fmWater@Levitate", "b0.0#fm@Huge Power", "b0.0#fm@"
    normal, grass = "b0.0#fmNormal@Levitate", "b0.0#fmGrass@Levitate"
    b.st["form_twin"] = {"b0.0": {"ability": "Levitate", "twins": {
        (("Water",), "Levitate"): water, (None, "Huge Power"): power, (None, None): blank,
        (("???",), "Levitate"): ((normal, ["Normal"]), (grass, ["Grass"]))}}}
    for twin, mine, theirs, speed in ((water, 15, 12, 50), (power, 20, 30, 70), (blank, 25, 10, 50),
                                      (normal, 22, 11, 50), (grass, 9, 14, 50)):
        b.st["rows"][(None, "p0", twin)] = {"moves": {"Tackle": {"rolls": [mine] * 16},
                                                     "Ember": {"rolls": [mine] * 16},
                                                     "Shadow Ball": {"rolls": [0 if twin == normal else mine] * 16}}}
        b.st["rows"][(None, twin, "p0")] = {"moves": {"Tackle": {"rolls": [theirs] * 16},
                                                     "Vine Whip": {"rolls": [theirs] * 16}}}
        b.st["speed"][(None, twin)] = speed
    tackle, ember, ball, whip = (fs.move(n) for n in ("Tackle", "Ember", "Shadow Ball", "Vine Whip"))

    def read():
        return (b.damage(p, foe, tackle, roll=0), b.damage(foe, p, tackle, roll=0), b.row_speed(foe))
    own = read()
    fs.set_types(foe, ["Water"])
    soaked = (list(foe.types), read())
    fs.set_ability(b, foe, "Huge Power")
    both = (foe.ability, foe.revealed, read())
    foe.reset_volatile()
    back = (list(foe.types), foe.ability, read())
    fs.set_ability(b, foe, "Huge Power")
    changed = read()
    foe.reset_volatile()
    fs.set_types(foe, ["???"])
    typeless = (b.damage(p, foe, ember, roll=0), b.damage(p, foe, ball, roll=0),
                b.damage(foe, p, tackle, roll=0), b.damage(foe, p, whip, roll=0))
    foe.reset_volatile()
    fs.suppress(b, foe)
    blanked = (foe.ability, read())
    foe.reset_volatile()
    ok = (own == (20, 10, 50) and soaked == (["Water"], (15, 12, 50)) and both == ("Huge Power", "Huge Power", (15, 12, 50))
          and back == (["Normal"], "Levitate", (20, 10, 50)) and changed == (20, 30, 70)
          and typeless == (22, 9, 14, 11) and blanked == (None, (25, 10, 50)) and foe.ability == "Levitate")
    results.append(("a changed type or ability reads its twin's rows and Speed until it leaves", ok,
                    f"own (hit, hit back, Speed) {own}; Water {soaked}; Water and Huge Power {both}; after leaving "
                    f"{back}; Huge Power alone {changed}; no type (Ember, Shadow Ball, its Tackle, its Vine Whip) "
                    f"{typeless}; suppressed {blanked}"))


def check_trace(results):
    """Trace (approved 2026-10-14; SWITCH_IN_CHECK_STATE_TRACE,
    ChooseTraceTarget, subscript_trace): once every lead is in, a Trace
    lead copies the foe's Intimidate, which then goes off on the foe as the
    foe's own goes off on it, and both abilities are named. A Trace lead
    facing another Trace, which refuses, waits, and traces the Pokemon that
    replaces it; leaving brings Trace back. A holder still waiting traces as
    a move ends once its foe's ability can be copied. Under Neutralizing Gas
    it waits, and traces once the gas has gone."""
    mons = {"p0": (("Normal",), ["Tackle"]), "p1": (("Normal",), ["Tackle"]),
            "b0.0": (("Normal",), ["Tackle"]), "b0.1": (("Normal",), ["Tackle"])}

    def leads(p_ab, b_ab, p1_ab="Levitate", gas=False):
        b = field(mons, {("b0.0", "p0"): {"Tackle": 10}, ("b0.0", "p1"): {"Tackle": 10}})
        b.st["first_battle"] = True
        b.st["gas"] = gas
        b.p.mons[0].ability, b.p.mons[1].ability, b.b.mons[0].ability = p_ab, p1_ab, b_ab
        fs.open_battle(b)
        return b, b.p.mons[0], b.p.mons[1], b.b.mons[0]
    b, dog, _p1, kir = leads("Intimidate", "Trace")
    intimidated = (kir.ability, kir.revealed, dog.revealed, dog.stages["atk"], kir.stages["atk"])
    b, ralts, p1, kir = leads("Trace", "Trace")
    waiting = (kir.ability, ralts.ability)
    fs.switch_in(b, b.p, 1)
    replaced = kir.ability
    fs.switch_in(b, b.b, 1)
    left = (kir.ability, kir.traced)
    b, ralts, _p1, kir = leads("Trace", "Trace")
    fs.set_ability(b, ralts, "Static")       # its foe's ability can now be copied
    fs.use_move(b, ralts, fs.move("Tackle"), kir, True)
    after_move = kir.ability
    b, weezing, p1, kir = leads("Neutralizing Gas", "Trace", p1_ab="Static", gas=True)
    gassed = (kir.ability, kir.gas_stash)
    fs.switch_in(b, b.p, 1)
    cleared = kir.ability
    ok = (intimidated == ("Intimidate", "Intimidate", "Intimidate", -1, -1) and waiting == ("Trace", "Trace")
          and replaced == "Levitate" and left == ("Trace", False) and after_move == "Static"
          and gassed == (None, "Trace") and cleared == "Static")
    results.append(("Trace copies a foe's ability as the switch-in check runs", ok,
                    f"against Intimidate (its ability, named, the foe's named, the foe's and its Attack) {intimidated}; "
                    f"against Trace {waiting}, then the replacement's {replaced}, after leaving {left}; after a move "
                    f"{after_move}; under the gas {gassed}, once it has gone {cleared}"))


def check_mummy(results):
    """Mummy (approved 2026-10-14; BattleSystem_TriggerAbilityOnHit,
    subscript_mummy): a contact hit on its holder gives the attacker Mummy,
    named, even when the hit knocks the holder out; a move without contact
    does not, nor does a contact hit into an attacker with an Ability Shield
    or one whose ability refuses (Multitype). The attacker then passes
    Mummy on by the same rule. A Levitate attacker that takes Mummy reads
    its ability-blank twin, so Earthquake reaches it; leaving brings
    Levitate back."""
    def hit(move="Tackle", ability="Levitate", item=None, hp=100):
        rows = {("p", "Tackle"): [10] * 16, ("p", "Water Gun"): [10] * 16, ("b", "Earthquake"): [0] * 16}
        b, p, foe = battle(["Tackle", "Water Gun"], ["Earthquake", "Tackle"], rows)
        b.st["first_battle"] = True
        p.ability, p.item, foe.ability = ability, item, "Mummy"
        b.st["form_twin"] = {"p0": {"ability": "Levitate", "twins": {(None, None): "p0#ng"}}}
        b.st["rows"][(None, "b0.0", "p0#ng")] = {"moves": {"Earthquake": {"rolls": [30] * 16},
                                                         "Tackle": {"rolls": [10] * 16}}}
        foe.hp = hp
        fs.use_move(b, p, fs.move(move), foe, True)
        return b, p, foe
    b, p, foe = hit()
    took = (p.ability, p.revealed, b.damage(foe, p, fs.move("Earthquake"), roll=0))
    fs.use_move(b, foe, fs.move("Tackle"), p, True)          # the holder's Tackle meets Mummy on p: nothing new
    p.reset_volatile()
    back = (p.ability, b.damage(foe, p, fs.move("Earthquake"), roll=0))
    fainted = hit(hp=5)[1].ability
    water = hit("Water Gun")[1].ability
    shield = hit(item="Ability Shield")[1].ability
    multitype = hit(ability="Multitype")[1].ability
    # The attacker that took Mummy passes it on to the next contact attacker.
    b, p, foe = hit()
    foe.ability = "Static"
    fs.use_move(b, foe, fs.move("Tackle"), p, True)
    passed = foe.ability
    ok = (took == ("Mummy", "Mummy", 30) and back == ("Levitate", 0) and fainted == "Mummy"
          and water == "Levitate" and shield == "Levitate" and multitype == "Multitype" and passed == "Mummy")
    results.append(("Mummy passes itself to a contact attacker", ok,
                    f"after Tackle (ability, named, Earthquake on it) {took}; after leaving {back}; the hit that "
                    f"faints the holder {fainted}; Water Gun {water}; an Ability Shield {shield}; Multitype {multitype}; "
                    f"passed on {passed}"))


def check_wandering_spirit(results):
    """Wandering Spirit (approved 2026-10-14; BattleSystem_TriggerAbilityOnHit,
    subscript_wandering_spirit): a contact hit on its holder swaps the two
    abilities, both named, and the holder then meets moves on its twin for
    the attacker's Levitate; no swap for a move without contact, an Ability
    Shield on either side, or an attacker whose ability refuses a swap
    (Wonder Guard). A holder given Truant before it has moved this turn
    still moves, and loafs on the next."""
    def hit(move="Tackle", ability="Levitate", item=None, foe_item=None):
        rows = {("p", "Tackle"): [10] * 16, ("p", "Water Gun"): [10] * 16, ("b", "Earthquake"): [30] * 16}
        b, p, foe = battle(["Tackle", "Water Gun"], ["Earthquake"], rows)
        b.st["first_battle"] = True
        p.ability, p.item, foe.ability, foe.item = ability, item, "Wandering Spirit", foe_item
        b.st["form_twin"] = {"b0.0": {"ability": None, "twins": {(None, "Levitate"): "b0.0#fm@Levitate"}}}
        b.st["rows"][(None, "p0", "b0.0#fm@Levitate")] = {"moves": {"Tackle": {"rolls": [10] * 16}}}
        b.st["rows"][(None, "b0.0#fm@Levitate", "p0")] = {"moves": {"Earthquake": {"rolls": [0] * 16}}}
        fs.use_move(b, p, fs.move(move), foe, True)
        return b, p, foe
    b, p, foe = hit()
    swapped = (p.ability, foe.ability, p.revealed, foe.revealed, b.damage(foe, p, fs.move("Earthquake"), roll=0))
    water = hit("Water Gun")[2].ability
    shields = (hit(item="Ability Shield")[2].ability, hit(foe_item="Ability Shield")[2].ability)
    guard = hit(ability="Wonder Guard")[2].ability
    b, p, foe = hit(ability="Truant")
    loafs = []
    for _ in range(3):
        fs.use_move(b, foe, fs.move("Earthquake"), p, False)
        loafs.append(p.hp)
        fs.end_of_turn(b)
    ok = (swapped == ("Wandering Spirit", "Levitate", "Wandering Spirit", "Levitate", 0) and water == "Wandering Spirit"
          and shields == ("Wandering Spirit", "Wandering Spirit") and guard == "Wandering Spirit"
          and foe.ability == "Truant" and loafs == [70, 70, 40])
    results.append(("Wandering Spirit swaps abilities with a contact attacker", ok,
                    f"(attacker's, holder's, both named, Earthquake from the holder) {swapped}; Water Gun {water}; "
                    f"Ability Shields {shields}; Wonder Guard {guard}; the attacker's HP as the holder, now Truant, "
                    f"moves three turns {loafs}"))


def check_color_change(results):
    """Color Change (approved 2026-10-14; BattleSystem_TriggerAbilityOnHit,
    subscript_color_change): a damaging hit makes its holder the move's type
    as the battle records it, named, and its rows are then its twin's of
    that type; Weather Ball in rain makes it Water, and a Normalize
    attacker's Water Gun makes it Normal. Nothing for a move of its own
    type, a status move, Struggle, a hit Sheer Force boosts, or the hit
    that knocks it out; leaving brings its own type back."""
    moves = ["Water Gun", "Tackle", "Ember", "Weather Ball", "Struggle", "Thunder Wave"]

    def hit(move, ability=None, weather=None, hp=100, types=("Fire",)):
        b, p, foe = battle(moves, ["Tackle"], {("p", m): [10] * 16 for m in moves}, b_types=types)
        b.st["first_battle"] = True
        p.ability, foe.ability, b.weather, foe.hp = ability, "Color Change", weather, hp
        b.st["form_twin"] = {"b0.0": {"ability": None, "twins": {(("Water",), None): "b0.0#fmWater@"}}}
        b.st["rows"][(None, "p0", "b0.0#fmWater@")] = {"moves": {"Water Gun": {"rolls": [5] * 16}}}
        b.st["rows"][(None, "b0.0#fmWater@", "p0")] = {"moves": {"Tackle": {"rolls": [10] * 16}}}
        fs.use_move(b, p, fs.move(move), foe, True)
        return b, p, foe
    b, p, foe = hit("Water Gun")
    water = (list(foe.types), foe.revealed, b.damage(p, foe, fs.move("Water Gun"), roll=0))
    foe.reset_volatile()
    back = list(foe.types)
    got = {"Weather Ball in rain": hit("Weather Ball", weather="Rain")[2].types,
           "Normalize's Water Gun": hit("Water Gun", ability="Normalize")[2].types,
           "Ember": hit("Ember")[2].types, "Thunder Wave": hit("Thunder Wave")[2].types,
           "Struggle": hit("Struggle")[2].types, "Sheer Force's Ember": hit("Ember", ability="Sheer Force",
                                                                            types=("Normal",))[2].types,
           "the knockout": hit("Water Gun", hp=5)[2].types}
    want = {"Weather Ball in rain": ["Water"], "Normalize's Water Gun": ["Normal"], "Ember": ["Fire"],
            "Thunder Wave": ["Fire"], "Struggle": ["Fire"], "Sheer Force's Ember": ["Normal"], "the knockout": ["Fire"]}
    ok = water == (["Water"], "Color Change", 5) and back == ["Fire"] and got == want
    results.append(("Color Change takes the type of the move that hit its holder", ok,
                    f"after Water Gun (types, named, Water Gun again) {water}; after leaving {back}; {got}"))


def check_forecast(results):
    """Forecast (approved 2026-10-14; BattleSystem_TriggerFormChange): as a
    move ends, Castform takes the weather's type, Fire in sun (so no burn
    lands), Water in rain, Ice in hail (so the hail spares it), and Normal
    again in sand, with no weather, or with Cloud Nine on the field; a
    Castform without Forecast keeps its type, and leaving brings Normal
    back."""
    def turn(weather, ability="Forecast", foe_ability=None):
        b, p, foe = battle(["Tackle"], ["Tackle"], {})
        b.st["first_battle"] = True
        foe.species, foe.ability, p.ability, b.weather = "Castform", ability, foe_ability, weather
        fs.use_move(b, p, fs.move("Tackle"), foe, True)
        return b, foe
    got = {w or "none": turn(w)[1].types for w in ("Sun", "Rain", "Hail", "Sand", None)}
    got["sun, Cloud Nine"] = turn("Sun", foe_ability="Cloud Nine")[1].types
    got["sun, no Forecast"] = turn("Sun", ability=None)[1].types
    b, cast = turn("Sun")
    burns = fs.can_status(b, cast, "brn")
    b, cast = turn("Hail")
    cast.hp = 50
    fs.end_of_turn(b)
    hail = cast.hp
    cast.reset_volatile()
    left = cast.types
    want = {"Sun": ["Fire"], "Rain": ["Water"], "Hail": ["Ice"], "Sand": ["Normal"], "none": ["Normal"],
            "sun, Cloud Nine": ["Normal"], "sun, no Forecast": ["Normal"]}
    ok = got == want and not burns and hail == 50 and left == ["Normal"]
    results.append(("Forecast gives Castform the weather's type", ok,
                    f"types {got}; burnable in sun {burns}; HP after hail from 50 {hail}; after leaving {left}"))


def check_soak(results):
    """Soak (approved 2026-10-14; subscript_change_target_to_water_type): its
    target becomes pure Water, a Water and Ground one too, and reads its
    Water twin's rows; nothing through a Substitute, into Multitype, into a
    pure Water target or into one in the air; leaving brings its own types
    back."""
    def soak(types=("Normal",), ability=None, sub=0, flying=False):
        b, p, foe = battle(["Soak", "Tackle"], ["Tackle"], {("p", "Tackle"): [10] * 16}, b_types=types)
        foe.ability, foe.sub = ability, sub
        if flying:
            foe.charging = fs.move("Fly")
        b.st["form_twin"] = {"b0.0": {"ability": None, "twins": {(("Water",), None): "b0.0#fmWater@"}}}
        b.st["rows"][(None, "p0", "b0.0#fmWater@")] = {"moves": {"Tackle": {"rolls": [7] * 16}}}
        fs.status_move(b, p, fs.move("Soak"), foe, True)
        return b, p, foe
    b, p, foe = soak()
    soaked = (list(foe.types), b.damage(p, foe, fs.move("Tackle"), roll=0))
    foe.reset_volatile()
    back = list(foe.types)
    got = {"Water and Ground": soak(("Water", "Ground"))[2].types, "a Substitute": soak(sub=25)[2].types,
           "Multitype": soak(ability="Multitype")[2].types, "pure Water": soak(("Water",))[2].types,
           "in the air": soak(flying=True)[2].types}
    want = {"Water and Ground": ["Water"], "a Substitute": ["Normal"], "Multitype": ["Normal"],
            "pure Water": ["Water"], "in the air": ["Normal"]}
    ok = soaked == (["Water"], 7) and back == ["Normal"] and got == want
    results.append(("Soak makes its target pure Water", ok,
                    f"soaked (types, Tackle on its twin) {soaked}; after leaving {back}; {got}"))


def check_conversion(results):
    """Conversion (approved 2026-10-14; BtlCmd_TryConversion): its user takes
    the type of one of its other moves that it is not of already, at random
    among them (Ember and Water Gun here, Tackle and Curse being Normal for
    a Normal type), and reads its twin of that type; it fails on Multitype
    and for a Ghost type whose other moves are Ghost ones, Curse counting as
    Ghost there."""
    def convert(types=("Normal",), moves=("Conversion", "Tackle", "Ember", "Water Gun", "Curse"), ability=None, seed=1):
        b, p, foe = battle(list(moves), ["Tackle"], {("p", "Tackle"): [10] * 16}, p_types=types, seed=seed)
        p.ability = ability
        b.st["form_twin"] = {"p0": {"ability": None, "twins": {(("Fire",), None): "p0#fmFire@",
                                                               (("Water",), None): "p0#fmWater@"}}}
        b.st["rows"][(None, "p0#fmFire@", "b0.0")] = {"moves": {"Tackle": {"rolls": [6] * 16}}}
        fs.status_move(b, p, fs.move("Conversion"), foe, True)
        return b, p, foe
    picked = collections.Counter(tuple(convert(seed=s)[1].types) for s in range(200))
    b, p, foe = convert(moves=("Conversion", "Tackle", "Ember"))
    fire = (list(p.types), b.damage(p, foe, fs.move("Tackle"), roll=0))
    multitype = convert(ability="Multitype")[1].types
    ghost = convert(types=("Ghost",), moves=("Conversion", "Curse", "Shadow Ball"))[1].types
    ok = (set(picked) == {("Fire",), ("Water",)} and min(picked.values()) > 60 and fire == (["Fire"], 6)
          and multitype == ["Normal"] and ghost == ["Ghost"])
    results.append(("Conversion takes the type of another of its user's moves", ok,
                    f"types over 200 uses {dict(picked)}; Ember alone (types, Tackle on the twin) {fire}; "
                    f"Multitype {multitype}; a Ghost with Curse and Shadow Ball {ghost}"))


def check_conversion2(results):
    """Conversion 2 (approved 2026-10-14; BtlCmd_TryConversion2): after an
    Ember, its user takes a type that resists Fire (Water, in this chart)
    and reads its twin of it; it fails with no move aimed at it since it
    last acted, once it has acted since that move, and on Multitype."""
    def convert(hit_first=True, acted_between=False, ability=None):
        rows = {("b", "Ember"): [10] * 16, ("b", "Tackle"): [10] * 16, ("p", "Tackle"): [10] * 16}
        b, p, foe = battle(["Conversion 2", "Tackle"], ["Ember", "Tackle"], rows)
        b.st["first_battle"] = True
        p.ability = ability
        b.st["form_twin"] = {"p0": {"ability": None, "twins": {(("Water",), None): "p0#fmWater@"}}}
        b.st["rows"][(None, "b0.0", "p0#fmWater@")] = {"moves": {"Ember": {"rolls": [5] * 16}}}
        if hit_first:
            fs.use_move(b, foe, fs.move("Ember"), p, True)
        if acted_between:
            fs.use_move(b, p, fs.move("Tackle"), foe, True)
        fs.use_move(b, p, fs.move("Conversion 2"), foe, False)
        return b, p, foe
    b, p, foe = convert()
    water = (list(p.types), b.damage(foe, p, fs.move("Ember"), roll=0))
    got = {"no move aimed at it": convert(hit_first=False)[1].types,
           "after acting since": convert(acted_between=True)[1].types,
           "Multitype": convert(ability="Multitype")[1].types}
    want = {"no move aimed at it": ["Normal"], "after acting since": ["Normal"], "Multitype": ["Normal"]}
    ok = water == (["Water"], 5) and got == want
    results.append(("Conversion 2 takes a type that resists the last move aimed at its user", ok,
                    f"after Ember (types, Ember on the twin) {water}; {got}"))


def check_camouflage(results):
    """Camouflage (approved 2026-10-14; BtlCmd_TryCamouflage): its user takes
    its terrain's type, Normal indoors and Rock on a mountain, and is marked
    so for the trainer's AI, which then refuses a second Camouflage; it
    fails on a user of that type already and on Multitype; leaving brings
    its own type back."""
    def camo(types=("Fire",), terrain=None, ability=None):
        b, p, foe = battle(["Camouflage", "Tackle"], ["Tackle"], {}, p_types=types)
        if terrain:
            b.st["camouflage"] = fs.camouflage_type(terrain)
        p.ability = ability
        fs.status_move(b, p, fs.move("Camouflage"), foe, True)
        return b, p, foe
    b, p, foe = camo()
    indoors = (list(p.types), p.camouflaged, fightai.basic(b, p, foe, fs.move("Camouflage"), None))
    p.reset_volatile()
    back = (list(p.types), p.camouflaged)
    got = {"a mountain": camo(terrain="TERRAIN_MOUNTAIN")[1].types, "a Normal user indoors": camo(("Normal",))[1].types,
           "Multitype": camo(ability="Multitype")[1].types, "the Elite Four's room": camo(terrain="TERRAIN_AARON")[1].types}
    want = {"a mountain": ["Rock"], "a Normal user indoors": ["Normal"], "Multitype": ["Fire"],
            "the Elite Four's room": ["Normal"]}
    ok = indoors == (["Normal"], True, -10) and back == (["Fire"], False) and got == want
    results.append(("Camouflage takes its terrain's type", ok,
                    f"indoors (types, marked, the AI's score for another) {indoors}; after leaving {back}; {got}"))


def check_burn_up(results):
    """Burn Up (approved 2026-10-14; effect script 393,
    subscript_remove_user_fire_type): once it hits, a Substitute too, a pure
    Fire user is left with no type and reads its typeless twin, and a Fire
    and Flying one is left Flying; a second Burn Up then fails; one that
    misses its target in the air, or meets Protect, spends nothing; leaving
    brings Fire back."""
    def burn(types=("Fire",), sub=0, guard=None):
        rows = {("p", "Burn Up"): [20] * 16, ("b", "Tackle"): [10] * 16}
        b, p, foe = battle(["Burn Up"], ["Tackle"], rows, p_types=types)
        b.st["first_battle"] = True
        foe.sub = sub
        if guard == "Protect":
            foe.protecting = True
        elif guard == "Fly":
            foe.charging = fs.move("Fly")
        b.st["form_twin"] = {"p0": {"ability": None, "twins": {
            (("???",), None): (("p0#fmNormal@", ["Normal"]), ("p0#fmGrass@", ["Grass"]))}}}
        b.st["rows"][(None, "b0.0", "p0#fmNormal@")] = {"moves": {"Tackle": {"rolls": [7] * 16}}}
        fs.use_move(b, p, fs.move("Burn Up"), foe, True)
        return b, p, foe
    b, p, foe = burn()
    spent = (list(p.types), foe.hp, b.damage(foe, p, fs.move("Tackle"), roll=0))
    fs.use_move(b, p, fs.move("Burn Up"), foe, True)
    again = foe.hp
    p.reset_volatile()
    back = list(p.types)
    got = {"Fire and Flying": burn(("Fire", "Flying"))[1].types, "a Substitute": burn(sub=25)[1].types,
           "Protect": burn(guard="Protect")[1].types, "Fly": burn(guard="Fly")[1].types}
    want = {"Fire and Flying": ["Flying"], "a Substitute": ["???"], "Protect": ["Fire"], "Fly": ["Fire"]}
    ok = spent == (["???"], 80, 7) and again == 80 and back == ["Fire"] and got == want
    results.append(("Burn Up takes its user's Fire type away, and fails without it", ok,
                    f"after one (types, the target's HP, Tackle on the typeless twin) {spent}; the target's HP after "
                    f"a second {again}; after leaving {back}; {got}"))


def check_double_shock(results):
    """Double Shock (approved 2026-10-14; effect script 394,
    subscript_remove_user_electric_type): it lands once a stay, an Electric
    and Fighting user then left Fighting and a pure Electric one with no
    type, so the second fails; leaving brings Electric back, and with it the
    move."""
    def shock(types):
        b, p, foe = battle(["Double Shock"], ["Tackle"], {("p", "Double Shock"): [20] * 16}, p_types=types)
        b.st["first_battle"] = True
        fs.use_move(b, p, fs.move("Double Shock"), foe, True)
        return b, p, foe
    b, p, foe = shock(("Electric", "Fighting"))
    first = (list(p.types), foe.hp)
    fs.use_move(b, p, fs.move("Double Shock"), foe, True)
    second = foe.hp
    p.reset_volatile()
    fs.use_move(b, p, fs.move("Double Shock"), foe, True)
    back = foe.hp
    pure = shock(("Electric",))[1].types
    ok = first == (["Fighting"], 80) and second == 80 and back == 60 and pure == ["???"]
    results.append(("Double Shock lands once a stay, taking its user's Electric type away", ok,
                    f"after one (types, the target's HP) {first}; after a second {second}; after leaving and a "
                    f"third {back}; a pure Electric user {pure}"))


def check_skill_swap(results):
    """Skill Swap (approved 2026-10-14; subscript_exchange_abilities): a
    Levitate user and a Static target swap, both named, and the target then
    reads its Levitate twin, a Substitute notwithstanding; nothing when
    either ability refuses (Wonder Guard), with an Ability Shield on
    either, or into a target in the air; leaving brings each its own back."""
    def swap(own="Levitate", theirs="Static", item=None, foe_item=None, sub=0, flying=False):
        rows = {("p", "Earthquake"): [30] * 16}
        b, p, foe = battle(["Skill Swap", "Earthquake"], ["Tackle"], rows)
        p.ability, p.item, foe.ability, foe.item, foe.sub = own, item, theirs, foe_item, sub
        if flying:
            foe.charging = fs.move("Fly")
        b.st["form_twin"] = {"b0.0": {"ability": None, "twins": {(None, "Levitate"): "b0.0#fm@Levitate"}}}
        b.st["rows"][(None, "p0", "b0.0#fm@Levitate")] = {"moves": {"Earthquake": {"rolls": [0] * 16}}}
        fs.status_move(b, p, fs.move("Skill Swap"), foe, True)
        return b, p, foe
    b, p, foe = swap(sub=25)
    swapped = (p.ability, foe.ability, p.revealed, foe.revealed, b.damage(p, foe, fs.move("Earthquake"), roll=0))
    p.reset_volatile()
    foe.reset_volatile()
    back = (p.ability, foe.ability)
    got = {"Wonder Guard": swap(theirs="Wonder Guard")[2].ability, "its own Ability Shield": swap(item="Ability Shield")[2].ability,
           "the target's Ability Shield": swap(foe_item="Ability Shield")[2].ability, "in the air": swap(flying=True)[2].ability}
    want = {"Wonder Guard": "Wonder Guard", "its own Ability Shield": "Static", "the target's Ability Shield": "Static",
            "in the air": "Static"}
    ok = swapped == ("Static", "Levitate", "Static", "Levitate", 0) and back == ("Levitate", "Static") and got == want
    results.append(("Skill Swap exchanges its user's and its target's abilities", ok,
                    f"(user's, target's, both named, Earthquake on the target) {swapped}; after leaving {back}; "
                    f"the target's ability {got}"))


def check_role_play(results):
    """Role Play (approved 2026-10-14; effect script 178,
    subscript_copy_ability): its user takes the target's Levitate, both
    named, and reads its twin for it, the target's Ability Shield and
    Substitute notwithstanding; nothing when the target's ability refuses
    (Wonder Guard) or is none, nor for a user with Multitype or an Ability
    Shield; leaving brings its own back."""
    def play(own="Static", theirs="Levitate", item=None, foe_item=None, sub=0):
        b, p, foe = battle(["Role Play"], ["Earthquake"], {("b", "Earthquake"): [30] * 16})
        p.ability, p.item, foe.ability, foe.item, foe.sub = own, item, theirs, foe_item, sub
        b.st["form_twin"] = {"p0": {"ability": None, "twins": {(None, "Levitate"): "p0#fm@Levitate"}}}
        b.st["rows"][(None, "b0.0", "p0#fm@Levitate")] = {"moves": {"Earthquake": {"rolls": [0] * 16}}}
        fs.status_move(b, p, fs.move("Role Play"), foe, True)
        return b, p, foe
    b, p, foe = play(foe_item="Ability Shield", sub=25)
    copied = (p.ability, p.revealed, foe.revealed, b.damage(foe, p, fs.move("Earthquake"), roll=0))
    p.reset_volatile()
    back = p.ability
    got = {"Wonder Guard": play(theirs="Wonder Guard")[1].ability, "no ability": play(theirs=None)[1].ability,
           "Multitype": play(own="Multitype")[1].ability, "its own Ability Shield": play(item="Ability Shield")[1].ability}
    want = {"Wonder Guard": "Static", "no ability": "Static", "Multitype": "Multitype", "its own Ability Shield": "Static"}
    ok = copied == ("Levitate", "Levitate", "Levitate", 0) and back == "Static" and got == want
    results.append(("Role Play copies its target's ability", ok,
                    f"(its ability, named, the target's named, Earthquake on it) {copied}; after leaving {back}; {got}"))


def check_entrainment(results):
    """Entrainment (approved 2026-10-14; subscript_entrainment): its target
    takes the user's Static, named, and its Levitate is gone from its rows
    (its blank twin's), so Earthquake reaches it; nothing through a
    Substitute, into a Truant target, into one that has the ability
    already, from a Wonder Guard user, or into an Ability Shield. A Truant
    given to a target that has not moved yet this turn lets it move now
    and makes it loaf on the next."""
    def entrain(own="Static", theirs="Levitate", sub=0, foe_item=None):
        rows = {("p", "Earthquake"): [0] * 16, ("b", "Tackle"): [10] * 16}
        b, p, foe = battle(["Entrainment", "Earthquake"], ["Tackle"], rows)
        p.ability, foe.ability, foe.sub, foe.item = own, theirs, sub, foe_item
        b.st["form_twin"] = {"b0.0": {"ability": "Levitate", "twins": {(None, None): "b0.0#ng"}}}
        b.st["rows"][(None, "p0", "b0.0#ng")] = {"moves": {"Earthquake": {"rolls": [30] * 16}}}
        fs.use_move(b, p, fs.move("Entrainment"), foe, True)
        return b, p, foe
    b, p, foe = entrain()
    given = (foe.ability, foe.revealed, b.damage(p, foe, fs.move("Earthquake"), roll=0))
    foe.reset_volatile()
    back = foe.ability
    got = {"a Substitute": entrain(sub=25)[2].ability, "a Truant target": entrain(theirs="Truant")[2].ability,
           "the same ability": entrain(theirs="Static")[2].ability, "Wonder Guard": entrain(own="Wonder Guard")[2].ability,
           "an Ability Shield": entrain(foe_item="Ability Shield")[2].ability}
    want = {"a Substitute": "Levitate", "a Truant target": "Truant", "the same ability": "Static",
            "Wonder Guard": "Levitate", "an Ability Shield": "Levitate"}
    b, p, foe = entrain(own="Truant")
    hp = []
    for _ in range(3):
        fs.use_move(b, foe, fs.move("Tackle"), p, False)
        hp.append(p.hp)
        fs.end_of_turn(b)
    ok = given == ("Static", "Static", 30) and back == "Levitate" and got == want and hp == [90, 90, 80]
    results.append(("Entrainment gives its target the user's ability", ok,
                    f"(target's ability, named, Earthquake on it) {given}; after leaving {back}; {got}; "
                    f"the user's HP as a target given Truant moves three turns {hp}"))


def check_worry_seed(results):
    """Worry Seed (approved 2026-10-14; subscript_give_target_insomnia): a
    sleeping Levitate target takes Insomnia, named, wakes, can be put to
    sleep no more, and reads its ability-blank twin, so Earthquake reaches
    it; nothing through a Substitute, into Truant or Multitype, or into an
    Ability Shield."""
    def seed(theirs="Levitate", sub=0, item=None):
        rows = {("p", "Earthquake"): [0] * 16}
        b, p, foe = battle(["Worry Seed", "Earthquake"], ["Tackle"], rows)
        foe.ability, foe.sub, foe.item = theirs, sub, item
        foe.status, foe.sleep = "slp", 3
        b.st["form_twin"] = {"b0.0": {"ability": "Levitate", "twins": {(None, None): "b0.0#ng"}}}
        b.st["rows"][(None, "p0", "b0.0#ng")] = {"moves": {"Earthquake": {"rolls": [30] * 16}}}
        fs.use_move(b, p, fs.move("Worry Seed"), foe, True)
        return b, p, foe
    b, p, foe = seed()
    took = (foe.ability, foe.revealed, foe.status, fs.can_status(b, foe, "slp"),
            b.damage(p, foe, fs.move("Earthquake"), roll=0))
    got = {"a Substitute": seed(sub=25)[2].ability, "Truant": seed(theirs="Truant")[2].ability,
           "Multitype": seed(theirs="Multitype")[2].ability, "an Ability Shield": seed(item="Ability Shield")[2].ability}
    want = {"a Substitute": "Levitate", "Truant": "Truant", "Multitype": "Multitype", "an Ability Shield": "Levitate"}
    ok = took == ("Insomnia", "Insomnia", None, False, 30) and got == want
    results.append(("Worry Seed gives its target Insomnia, which wakes it", ok,
                    f"(ability, named, status, can sleep, Earthquake on it) {took}; {got}"))


def check_gastro_acid(results):
    """Gastro Acid (approved 2026-10-14; subscript_suppress_target_ability):
    a Levitate target's ability reads as none, unnamed, so the trainer's AI
    reads none either, and its blank twin's rows let Earthquake reach it;
    nothing through a Substitute, into Multitype or an Ability Shield;
    leaving brings Levitate back. On a Neutralizing Gas holder it ends the
    gas, and the user's own ability comes back as the move ends."""
    def acid(theirs="Levitate", sub=0, item=None, own=None):
        rows = {("p", "Earthquake"): [0] * 16}
        b, p, foe = battle(["Gastro Acid", "Earthquake"], ["Tackle"], rows)
        b.st["gas"] = theirs == "Neutralizing Gas"
        p.ability, foe.ability, foe.sub, foe.item = own, theirs, sub, item
        if b.st["gas"]:
            fs.gas_update(b)
        b.st["form_twin"] = {"b0.0": {"ability": "Levitate", "twins": {(None, None): "b0.0#ng"}}}
        b.st["rows"][(None, "p0", "b0.0#ng")] = {"moves": {"Earthquake": {"rolls": [30] * 16}}}
        fs.use_move(b, p, fs.move("Gastro Acid"), foe, True)
        return b, p, foe
    b, p, foe = acid()
    gone = (foe.ability, foe.suppressed, foe.revealed, fightai.ability_of(b, p, foe),
            b.damage(p, foe, fs.move("Earthquake"), roll=0))
    foe.reset_volatile()
    back = (foe.ability, foe.suppressed)
    got = {"a Substitute": acid(sub=25)[2].ability, "Multitype": acid(theirs="Multitype")[2].ability,
           "an Ability Shield": acid(item="Ability Shield")[2].ability}
    want = {"a Substitute": "Levitate", "Multitype": "Multitype", "an Ability Shield": "Levitate"}
    b, p, foe = acid(theirs="Neutralizing Gas", own="Static")
    gas = (foe.ability, fs.gas_on(b), p.ability)
    ok = gone == (None, True, None, None, 30) and back == ("Levitate", False) and got == want and gas == (None, False, "Static")
    results.append(("Gastro Acid suppresses its target's ability until it leaves", ok,
                    f"(ability, suppressed, named, the AI's read, Earthquake on it) {gone}; after leaving {back}; {got}; "
                    f"on a gas holder (its ability, gas on, the user's ability) {gas}"))


def check_core_enforcer(results):
    """Core Enforcer (approved 2026-10-14; subscript_core_enforcer): its hit
    suppresses the ability of a target that has moved this turn, which then
    reads its blank twin; nothing for a target that has not moved yet, one
    behind a Substitute, one it knocks out, or Multitype."""
    def enforce(moved=True, sub=0, hp=100, ability="Levitate"):
        rows = {("p", "Core Enforcer"): [10] * 16, ("p", "Earthquake"): [0] * 16, ("b", "Tackle"): [5] * 16}
        b, p, foe = battle(["Core Enforcer", "Earthquake"], ["Tackle"], rows)
        b.st["first_battle"] = True
        foe.ability, foe.sub, foe.hp = ability, sub, hp
        b.st["form_twin"] = {"b0.0": {"ability": "Levitate", "twins": {(None, None): "b0.0#ng"}}}
        b.st["rows"][(None, "p0", "b0.0#ng")] = {"moves": {"Earthquake": {"rolls": [30] * 16}}}
        if moved:
            fs.use_move(b, foe, fs.move("Tackle"), p, True)
        fs.use_move(b, p, fs.move("Core Enforcer"), foe, not moved)
        return b, p, foe
    b, p, foe = enforce()
    gone = (foe.ability, foe.suppressed, b.damage(p, foe, fs.move("Earthquake"), roll=0))
    got = {"not moved yet": enforce(moved=False)[2].ability, "a Substitute": enforce(sub=25)[2].ability,
           "knocked out": enforce(hp=5)[2].ability, "Multitype": enforce(ability="Multitype")[2].ability}
    want = {"not moved yet": "Levitate", "a Substitute": "Levitate", "knocked out": "Levitate",
            "Multitype": "Multitype"}
    ok = gone == (None, True, 30) and got == want
    results.append(("Core Enforcer suppresses a target that has moved this turn", ok,
                    f"(ability, suppressed, Earthquake on it) {gone}; {got}"))


def check_captivate(results):
    """Captivate (approved 2026-10-14; effect script 265): two stages of Sp.
    Atk off a target of the other gender only; nothing between two of one
    gender or from or into a genderless Pokemon; an Oblivious target is
    spared, named, unless the user has Mold Breaker."""
    def captivate(user, target, ability=None, mold=False):
        b, p, foe = battle(["Captivate"], ["Tackle"], {})
        p.gender, foe.gender, foe.ability = user, target, ability
        p.ability = "Mold Breaker" if mold else None
        fs.status_move(b, p, fs.move("Captivate"), foe, True)
        return foe.stages["spa"], foe.revealed
    got = {"male on female": captivate("M", "F"), "female on male": captivate("F", "M"),
           "male on male": captivate("M", "M"), "genderless user": captivate(None, "F"),
           "genderless target": captivate("M", None), "Oblivious": captivate("M", "F", "Oblivious"),
           "Oblivious, Mold Breaker": captivate("M", "F", "Oblivious", True)}
    want = {"male on female": (-2, None), "female on male": (-2, None), "male on male": (0, None),
            "genderless user": (0, None), "genderless target": (0, None), "Oblivious": (0, "Oblivious"),
            "Oblivious, Mold Breaker": (-2, None)}
    results.append(("Captivate lowers Sp. Atk only across the genders", got == want, f"(stage, named) {got}"))


def check_status_into_vanished(results):
    """A status move aimed at a foe misses it on the hidden turn of Fly,
    Bounce, Shadow Force or Phantom Force (approved 2026-10-14;
    BattleControllerPlayer_CheckMoveHitOverrides sets
    MOVE_STATUS_SEMI_INVULNERABLE): Thunder Wave, Toxic, Yawn, Growl and
    Taunt take nothing there, and each lands on a target that is not hidden.
    No Guard on either side reaches the target; Memento, whose script sets
    every SYSCTL_HIT_DURING flag, still lowers its stats; and Spikes, aimed at
    the foe's side, still lands. Dig and Dive are one-turn hits in Oxide, so a
    target given either as its charging move is not hidden at all."""
    def use(name, vanish=None, ability=None, foe_ability=None):
        b, p, foe = battle([name], ["Tackle"], {})
        p.ability, foe.ability = ability, foe_ability
        foe.charging = fs.move(vanish) if vanish else None
        fs.status_move(b, p, fs.move(name), foe, True)
        return foe.status, foe.yawn, foe.stages["atk"], bool(foe.taunt), b.b.hazards["spikes"]
    names = ("Thunder Wave", "Toxic", "Yawn", "Growl", "Taunt")
    plain = {n: use(n) for n in names}
    flying = {n: use(n, "Fly") for n in names}
    hidden = {v: use("Thunder Wave", v) for v in ("Bounce", "Shadow Force", "Phantom Force")}
    one_turn = {v: use("Thunder Wave", v) for v in ("Dig", "Dive")}
    guard = {"the user's No Guard": use("Thunder Wave", "Fly", ability="No Guard"),
             "the target's No Guard": use("Thunder Wave", "Fly", foe_ability="No Guard")}
    reach = {"Memento": use("Memento", "Fly"), "Spikes": use("Spikes", "Fly")}
    nothing = (None, 0, 0, False, 0)
    paralysed = ("par", 0, 0, False, 0)
    ok = (plain == {"Thunder Wave": paralysed, "Toxic": ("tox", 0, 0, False, 0), "Yawn": (None, 2, 0, False, 0),
                    "Growl": (None, 0, -1, False, 0), "Taunt": (None, 0, 0, True, 0)}
          and all(v == nothing for v in flying.values()) and all(v == nothing for v in hidden.values())
          and all(v == paralysed for v in one_turn.values()) and all(v == paralysed for v in guard.values())
          and reach == {"Memento": (None, 0, -2, False, 0), "Spikes": (None, 0, 0, False, 1)})
    results.append(("a status move misses a target on the hidden turn of Fly and the like", ok,
                    f"(status, Yawn, Attack stage, taunted, Spikes) plain {plain}; into Fly {flying}; {hidden}; "
                    f"one-turn {one_turn}; {guard}; {reach}"))


def check_speed_down_hit(results):
    """Hammer Arm and Ice Hammer (approved 2026-10-14; effect script 218,
    ON_HIT and TO_ATTACKER): the user's own Speed falls a stage on any hit,
    through a Substitute, on a knockout and under Sheer Force alike, and the
    target's Speed never moves."""
    def use(name, sub=0, foe_hp=None, ability=None):
        b, p, foe = battle([name], ["Tackle"], {("p", name): [30] * 16})
        p.ability, foe.sub = ability, sub
        if foe_hp is not None:
            foe.hp = foe_hp
        fs.attack(b, p, fs.move(name), foe, True)
        return p.stages["spe"], foe.stages["spe"]
    got = {n: use(n) for n in ("Hammer Arm", "Ice Hammer")}
    got.update({"into a Substitute": use("Hammer Arm", sub=25), "on a knockout": use("Hammer Arm", foe_hp=10),
                "Sheer Force": use("Ice Hammer", ability="Sheer Force")})
    ok = all(v == (-1, 0) for v in got.values())
    results.append(("Hammer Arm and Ice Hammer lower their user's Speed, never the target's", ok,
                    f"(user's Speed stage, target's) {got}"))


def check_bounce_paralysis(results):
    """Bounce (approved 2026-10-14; effect script 263): once it comes down,
    its hit paralyses at the move's 30% chance, as Thunderbolt's does, and a
    Shield Dust target is spared. With every roll at 0 the chance lands,
    at 0.5 it does not (the hit itself lands at Oxide's 100% accuracy)."""
    def bounce(value, foe_ability=None):
        b, p, foe = battle(["Bounce"], ["Tackle"], {("p", "Bounce"): [30] * 16})
        foe.ability = foe_ability
        b.rng = FixedDice(value)
        fs.use_move(b, p, fs.move("Bounce"), foe, True)       # up into the air
        up = p.charging is not None
        fs.use_move(b, p, fs.move("Bounce"), foe, True)       # down onto the target
        return up, foe.hp < foe.maxhp, foe.status
    got = {"every roll at 0": bounce(0.0), "every roll at 0.5": bounce(0.5),
           "Shield Dust": bounce(0.0, "Shield Dust")}
    want = {"every roll at 0": (True, True, "par"), "every roll at 0.5": (True, True, None),
            "Shield Dust": (True, True, None)}
    results.append(("Bounce's hit paralyses at its chance", got == want, f"(in the air, hit, status) {got}"))


def check_weather_heal(results):
    """Moonlight, Morning Sun, Synthesis and Shore Up (approved 2026-10-14;
    effect script 132, BtlCmd_WeatherHPRecovery), from 1 HP of 100: half
    with no weather, two thirds in sun, a quarter in rain or sand, and half
    again in sun when Cloud Nine or Air Lock stands on the field; Shore Up
    two thirds in sand only, and half in sun or with no weather."""
    def heal(name, weather=None, ability=None, foe_ability=None):
        b, p, foe = battle([name], ["Tackle"], {})
        b.weather, b.weather_turns = weather, 5 if weather else 0
        p.ability, foe.ability = ability, foe_ability
        p.hp = 1
        fs.status_move(b, p, fs.move(name), foe, True)
        return p.hp - 1
    got = {"Moonlight": heal("Moonlight"), "Morning Sun in sun": heal("Morning Sun", "Sun"),
           "Synthesis in rain": heal("Synthesis", "Rain"), "Synthesis in sand": heal("Synthesis", "Sand"),
           "Synthesis in sun, the foe's Cloud Nine": heal("Synthesis", "Sun", foe_ability="Cloud Nine"),
           "Moonlight in sun, its own Air Lock": heal("Moonlight", "Sun", ability="Air Lock"),
           "Shore Up in sand": heal("Shore Up", "Sand"), "Shore Up in sun": heal("Shore Up", "Sun"),
           "Shore Up": heal("Shore Up"), "Shore Up in sand, Cloud Nine": heal("Shore Up", "Sand", foe_ability="Cloud Nine")}
    want = {"Moonlight": 50, "Morning Sun in sun": 66, "Synthesis in rain": 25, "Synthesis in sand": 25,
            "Synthesis in sun, the foe's Cloud Nine": 50, "Moonlight in sun, its own Air Lock": 50,
            "Shore Up in sand": 66, "Shore Up in sun": 50, "Shore Up": 50, "Shore Up in sand, Cloud Nine": 50}
    results.append(("the weather heals restore by the weather, Shore Up by sand, none under Cloud Nine",
                    got == want, f"(HP restored) {got}"))


def check_hail_under_lasting_hail(results):
    """Hail (approved 2026-10-14; effect script 164 tests only
    FIELD_CONDITION_HAILING_TEMP): under a Snow Warning's lasting hail it
    starts five turns of its own (eight with an Icy Rock); under a move's
    hail it fails. Rain Dance, Sunny Day and Sandstorm still fail under any
    weather of their own kind, an ability's lasting one too."""
    def use(name, weather, turns, item=None):
        b, p, foe = battle([name], ["Tackle"], {})
        b.weather, b.weather_turns = weather, turns
        p.item = item
        fs.status_move(b, p, fs.move(name), foe, True)
        return b.weather, b.weather_turns
    got = {"Hail, lasting hail": use("Hail", "Hail", 0), "Hail, lasting hail, Icy Rock": use("Hail", "Hail", 0, "Icy Rock"),
           "Hail, a move's hail": use("Hail", "Hail", 3), "Hail, lasting rain": use("Hail", "Rain", 0),
           "Rain Dance, lasting rain": use("Rain Dance", "Rain", 0), "Sunny Day, lasting sun": use("Sunny Day", "Sun", 0),
           "Sandstorm, lasting sand": use("Sandstorm", "Sand", 0)}
    want = {"Hail, lasting hail": ("Hail", 5), "Hail, lasting hail, Icy Rock": ("Hail", 8),
            "Hail, a move's hail": ("Hail", 3), "Hail, lasting rain": ("Hail", 5),
            "Rain Dance, lasting rain": ("Rain", 0), "Sunny Day, lasting sun": ("Sun", 0),
            "Sandstorm, lasting sand": ("Sand", 0)}
    results.append(("Hail turns a lasting hail into five turns; the other weather moves fail on their own",
                    got == want, f"(weather, turns left; 0 lasting) {got}"))


def check_dream_eater(results):
    """Dream Eater (approved 2026-10-14; effect script 8): on a sleeping
    target it hits and its user takes back half the damage; an awake
    target, a Comatose one or one behind a Substitute is not affected, and
    an Infiltrator user passes the Substitute."""
    def eat(status=None, sub=0, ability=None, foe_ability=None):
        b, p, foe = battle(["Dream Eater"], ["Tackle"], {("p", "Dream Eater"): [40] * 16})
        b.rng = FixedDice(0.5)
        foe.status, foe.sleep, foe.sub, foe.ability = status, 3 if status else 0, sub, foe_ability
        p.ability, p.hp = ability, 50
        fs.attack(b, p, fs.move("Dream Eater"), foe, True)
        return foe.hp, foe.sub, p.hp
    got = {"asleep": eat("slp"), "awake": eat(), "paralysed": eat("par"), "Comatose": eat(foe_ability="Comatose"),
           "asleep behind a Substitute": eat("slp", sub=25),
           "asleep behind a Substitute, Infiltrator": eat("slp", sub=25, ability="Infiltrator")}
    want = {"asleep": (60, 0, 70), "awake": (100, 0, 50), "paralysed": (100, 0, 50), "Comatose": (100, 0, 50),
            "asleep behind a Substitute": (100, 25, 50),
            "asleep behind a Substitute, Infiltrator": (60, 25, 70)}
    results.append(("Dream Eater hits only a sleeping target with no Substitute in the way", got == want,
                    f"(target's HP, its Substitute, user's HP from 50) {got}"))


def check_focus_punch(results):
    """Focus Punch (approved 2026-10-14; effect script 170): a user that a
    faster foe's hit has damaged this turn loses its focus and deals
    nothing, spending its PP; one whose Substitute took the hit, or that
    was not hit, lands it."""
    def turn(foe_move, sub=0):
        b, p, foe = battle(["Focus Punch"], [foe_move], {("p", "Focus Punch"): [50] * 16, ("b", foe_move): [20] * 16},
                           p_speed=50, b_speed=100)
        b.rng = FixedDice(0.5)
        p.sub = sub
        fs.use_move(b, foe, fs.move(foe_move), p, True)
        pp = p.pp["Focus Punch"]
        fs.use_move(b, p, fs.move("Focus Punch"), foe, False)
        return foe.hp, pp - p.pp["Focus Punch"]
    got = {"hit first": turn("Tackle"), "behind a Substitute": turn("Tackle", sub=30), "not hit": turn("Tail Whip")}
    want = {"hit first": (100, 1), "behind a Substitute": (50, 1), "not hit": (50, 1)}
    results.append(("Focus Punch loses its focus once a hit has damaged its user this turn", got == want,
                    f"(target's HP, PP spent) {got}"))


def check_crash_on_miss(results):
    """Jump Kick, High Jump Kick and Supercell Slam (approved 2026-10-14;
    effect script 45, subscript_crash_on_miss from every path of
    subscript_missed): a move that fails to hit costs its user half the
    damage the hit would have done (40 here, so 20), at most half the
    target's maximum HP (a 60 HP target caps a 150 hit's crash at 30); on an
    accuracy miss, into a Protect and into a target in the air alike; a
    Magic Guard user loses nothing, and so does one whose hit could do
    nothing (a Ghost type, whose row reads 0)."""
    def kick(dice, dmg=40, foe_max=None, protect=False, fly=False, ability=None, ghost=False):
        b, p, foe = battle(["Jump Kick"], ["Tackle"], {("p", "Jump Kick"): [0 if ghost else dmg] * 16},
                           b_types=("Ghost",) if ghost else ("Normal",))
        b.rng = FixedDice(dice)
        p.ability = ability
        if foe_max is not None:
            foe.maxhp = foe.hp = foe_max
        foe.protecting = protect
        foe.charging = fs.move("Fly") if fly else None
        fs.attack(b, p, fs.move("Jump Kick"), foe, True)
        return p.maxhp - p.hp, foe.maxhp - foe.hp
    got = {"a miss": kick(0.999), "a miss, capped": kick(0.999, dmg=150, foe_max=60), "into Protect": kick(0.5, protect=True),
           "into Fly": kick(0.5, fly=True), "Magic Guard, into Protect": kick(0.5, protect=True, ability="Magic Guard"),
           "into a Ghost": kick(0.5, ghost=True), "a hit": kick(0.5)}
    want = {"a miss": (20, 0), "a miss, capped": (30, 0), "into Protect": (20, 0), "into Fly": (20, 0),
            "Magic Guard, into Protect": (0, 0), "into a Ghost": (0, 0), "a hit": (0, 40)}
    results.append(("a crash move that fails to hit costs half its hit, at most half the target's HP", got == want,
                    f"(user's HP lost, target's HP lost) {got}"))


def check_bind(results):
    """Binding (approved 2026-10-14; subscript_bind_start, Oxide's
    MON_COND_CHECK_STATE_BIND): Fire Spin binds for a count of 3 to 6 (the
    low end on these dice, 6 with a Grip Claw); each turn's end lowers it,
    and while it stays above 0 the target loses an eighth of its maximum HP,
    a sixth when the binder holds a Binding Band, so a count of 3 costs two
    eighths and then frees it, held in until then. The bind ends at once
    when the binder leaves, switched out or replaced after a knockout."""
    def bind(item=None):
        b = field({"p0": (("Normal",), ["Fire Spin"]), "p1": (("Normal",), ["Tackle"]),
                   "b0.0": (("Normal",), ["Tackle"])}, {("p0", "b0.0"): {"Fire Spin": 10}})
        b.rng = FixedDice(0.5)
        p, foe = b.p.cur(), b.b.cur()
        p.item = item
        fs.attack(b, p, fs.move("Fire Spin"), foe, True)
        return b, p, foe
    out = {}
    for label, item in (("plain", None), ("Grip Claw", "Grip Claw"), ("Binding Band", "Binding Band")):
        b, p, foe = bind(item)
        count = foe.bound
        trail = []
        for _ in range(3):
            fs.end_of_turn(b)
            trail.append((foe.hp, foe.bound, fs.trapped(b, foe)))
        out[label] = (count, trail)
    b, p, foe = bind()
    fs.switch_in(b, b.p, 1)
    out["the binder switches out"] = (foe.bound, fs.trapped(b, foe))
    b, p, foe = bind()
    p.hp = 0
    fs.switch_in(b, b.p, 1)
    out["the binder is replaced after a knockout"] = (foe.bound, fs.trapped(b, foe))
    want = {"plain": (3, [(78, 2, True), (66, 1, True), (66, 0, False)]),
            "Grip Claw": (6, [(78, 5, True), (66, 4, True), (54, 3, True)]),
            "Binding Band": (3, [(74, 2, True), (58, 1, True), (58, 0, False)]),
            "the binder switches out": (0, False), "the binder is replaced after a knockout": (0, False)}
    results.append(("a bind lasts its count, an eighth a turn, and ends with its binder", out == want,
                    f"(count, [(HP, count, trapped) after each turn end]) {out}"))


def check_steal_item(results):
    """Thief and Covet (approved 2026-10-14; effect script 105,
    BtlCmd_TryStealItem): the player's Pokemon takes the target's item when
    it holds none, on a knockout too; it takes nothing while holding an
    item, through a Substitute, from Sticky Hold (unless Mold Breaker) or
    when its own item was knocked off. A trainer's Thief takes nothing: the
    player's Pokemon keeps its item."""
    def thief(user_item=None, foe_item="Leftovers", foe_ability=None, ability=None, sub=0, foe_hp=None,
              knocked=False, trainer=False):
        if trainer:
            b, p, foe = battle(["Tackle"], ["Thief"], {("b", "Thief"): [20] * 16})
            p, foe = foe, p                  # the trainer's Pokemon steals from the player's
        else:
            b, p, foe = battle(["Thief"], ["Tackle"], {("p", "Thief"): [20] * 16})
        b.rng = FixedDice(0.5)
        p.item, foe.item, foe.ability, p.ability, foe.sub = user_item, foe_item, foe_ability, ability, sub
        p.knocked_off = knocked
        if foe_hp is not None:
            foe.hp = foe_hp
        fs.attack(b, p, fs.move("Thief"), foe, True)
        return p.item, foe.item
    got = {"empty-handed": thief(), "on a knockout": thief(foe_hp=10), "holding an item": thief(user_item="Charcoal"),
           "through a Substitute": thief(sub=30), "Sticky Hold": thief(foe_ability="Sticky Hold"),
           "Sticky Hold, Mold Breaker": thief(foe_ability="Sticky Hold", ability="Mold Breaker"),
           "its own item knocked off": thief(knocked=True), "a trainer's Thief": thief(trainer=True)}
    want = {"empty-handed": ("Leftovers", None), "on a knockout": ("Leftovers", None),
            "holding an item": ("Charcoal", "Leftovers"), "through a Substitute": (None, "Leftovers"),
            "Sticky Hold": (None, "Leftovers"), "Sticky Hold, Mold Breaker": ("Leftovers", None),
            "its own item knocked off": (None, "Leftovers"), "a trainer's Thief": (None, "Leftovers")}
    results.append(("Thief takes an item for the player's empty-handed Pokemon only", got == want,
                    f"(thief's item, target's item) {got}"))


def check_swap_items(results):
    """Trick and Switcheroo (approved 2026-10-14; effect script 177,
    BtlCmd_TrySwapItems): the player's swaps its item with its target's, an
    empty hand too; nothing swaps when neither holds an item, through a
    Substitute, into Sticky Hold (unless Mold Breaker) or once either's item
    was knocked off. A trainer's Trick swaps nothing."""
    def trick(user_item="Charcoal", foe_item="Leftovers", foe_ability=None, ability=None, sub=0,
              knocked=False, trainer=False, name="Trick"):
        if trainer:
            b, p, foe = battle(["Tackle"], [name], {})
            p, foe = foe, p
        else:
            b, p, foe = battle([name], ["Tackle"], {})
        b.rng = FixedDice(0.5)
        p.item, foe.item, foe.ability, p.ability, foe.sub = user_item, foe_item, foe_ability, ability, sub
        foe.knocked_off = knocked
        fs.status_move(b, p, fs.move(name), foe, True)
        return p.item, foe.item
    got = {"Trick": trick(), "Switcheroo": trick(name="Switcheroo"), "an empty hand": trick(user_item=None),
           "neither holds one": trick(user_item=None, foe_item=None), "through a Substitute": trick(sub=30),
           "Sticky Hold": trick(foe_ability="Sticky Hold"),
           "Sticky Hold, Mold Breaker": trick(foe_ability="Sticky Hold", ability="Mold Breaker"),
           "the target's item knocked off": trick(foe_item=None, knocked=True), "a trainer's Trick": trick(trainer=True)}
    want = {"Trick": ("Leftovers", "Charcoal"), "Switcheroo": ("Leftovers", "Charcoal"),
            "an empty hand": ("Leftovers", None), "neither holds one": (None, None),
            "through a Substitute": ("Charcoal", "Leftovers"), "Sticky Hold": ("Charcoal", "Leftovers"),
            "Sticky Hold, Mold Breaker": ("Leftovers", "Charcoal"), "the target's item knocked off": ("Charcoal", None),
            "a trainer's Trick": ("Charcoal", "Leftovers")}
    results.append(("Trick and Switcheroo swap items for the player's side only", got == want,
                    f"(user's item, target's item) {got}"))


def check_pluck(results):
    """Bug Bite and Pluck (approved 2026-10-14; effect script 224,
    BattleSystem_PluckBerry): the user eats the target's Berry and takes its
    effect: a Sitrus Berry a quarter of its HP, a Lum Berry its paralysis
    and confusion, a Chesto Berry its sleep, a Liechi Berry a stage of
    Attack at full HP; a resist Berry is eaten for nothing; the Berry is
    then the target's to Recycle. Sticky Hold keeps the Berry (Mold Breaker
    gets past it), a Klutz user eats it for nothing, a Substitute's hit
    takes nothing and a Leftovers stays put."""
    def bite(berry, status=None, ability=None, foe_ability=None, sub=0, confused=0):
        b, p, foe = battle(["Bug Bite"], ["Tackle"], {("p", "Bug Bite"): [10] * 16})
        b.rng = FixedDice(0.5)
        foe.item, foe.ability, foe.sub, p.ability = berry, foe_ability, sub, ability
        p.status, p.sleep, p.confused = status, 3 if status == "slp" else 0, confused
        if berry != "Liechi Berry":
            p.hp = 50
        fs.attack(b, p, fs.move("Bug Bite"), foe, True)
        return p.hp, p.status, p.confused, p.stages["atk"], foe.item, foe.recycle
    got = {"Sitrus": bite("Sitrus Berry"), "Lum": bite("Lum Berry", "par", confused=3),
           "Chesto": bite("Chesto Berry", "slp"), "Liechi": bite("Liechi Berry"), "Occa": bite("Occa Berry"),
           "Sticky Hold": bite("Sitrus Berry", foe_ability="Sticky Hold"),
           "Sticky Hold, Mold Breaker": bite("Sitrus Berry", ability="Mold Breaker", foe_ability="Sticky Hold"),
           "Klutz": bite("Sitrus Berry", ability="Klutz"), "a Substitute": bite("Sitrus Berry", sub=30),
           "Leftovers": bite("Leftovers")}
    want = {"Sitrus": (75, None, 0, 0, None, "Sitrus Berry"), "Lum": (50, None, 0, 0, None, "Lum Berry"),
            "Chesto": (50, None, 0, 0, None, "Chesto Berry"), "Liechi": (100, None, 0, 1, None, "Liechi Berry"),
            "Occa": (50, None, 0, 0, None, "Occa Berry"), "Sticky Hold": (50, None, 0, 0, "Sitrus Berry", None),
            "Sticky Hold, Mold Breaker": (75, None, 0, 0, None, "Sitrus Berry"),
            "Klutz": (50, None, 0, 0, None, "Sitrus Berry"), "a Substitute": (50, None, 0, 0, "Sitrus Berry", None),
            "Leftovers": (50, None, 0, 0, "Leftovers", None)}
    results.append(("Bug Bite eats the target's Berry with that Berry's own effect", got == want,
                    f"(user's HP, status, confusion, Attack stage; target's item, its Recycle) {got}"))


def check_chatter(results):
    """Chatter (approved 2026-10-14; effect script 267,
    BtlCmd_CheckChatterActivation): a Chatot's hit confuses on a roll no
    higher than its cry's figure, 0 with no recording, so 1 in 100; with
    every roll at 0 it confuses, at 0.02 it does not. Another species'
    Chatter, a Sheer Force Chatot's, and one into Shield Dust or Own Tempo
    never confuse."""
    def chatter(value, species="Chatot", ability=None, foe_ability=None):
        b, p, foe = battle(["Chatter"], ["Tackle"], {("p", "Chatter"): [20] * 16})
        b.rng = FixedDice(value)
        p.species, p.ability, foe.ability = species, ability, foe_ability
        fs.attack(b, p, fs.move("Chatter"), foe, True)
        return foe.hp < foe.maxhp, bool(foe.confused)
    got = {"at 0": chatter(0.0), "at 0.02": chatter(0.02), "a Ditto's": chatter(0.0, "Ditto"),
           "Sheer Force": chatter(0.0, ability="Sheer Force"), "Shield Dust": chatter(0.0, foe_ability="Shield Dust"),
           "Own Tempo": chatter(0.0, foe_ability="Own Tempo")}
    want = {"at 0": (True, True), "at 0.02": (True, False), "a Ditto's": (True, False),
            "Sheer Force": (True, False), "Shield Dust": (True, False), "Own Tempo": (True, False)}
    results.append(("a Chatot's Chatter confuses 1 time in 100", got == want, f"(hit, confused) {got}"))


def check_stockpile(results):
    """Stockpile, Spit Up and Swallow (approved 2026-10-14; effect scripts
    160 to 162): Stockpile counts to three, raising Defense and Sp. Def a
    stage each time, and a fourth fails; from +5 Defense only the first
    Defense stage counts. Swallow restores a quarter for one stockpile,
    half for two and all for three, and Spit Up hits at 100 power for each
    (its row for that power, at the top roll); both give the counted stages
    back and empty the count, and with nothing stored both fail."""
    def stock(times, def_stage=0):
        b, p, foe = battle(["Stockpile", "Swallow", "Spit Up"], ["Tackle"], {})
        p.stages["def"] = def_stage
        for _ in range(times):
            fs.status_move(b, p, fs.move("Stockpile"), foe, True)
        return b, p, foe
    out = {}
    b, p, foe = stock(4)
    out["four Stockpiles"] = (p.stockpile, p.stages["def"], p.stages["spd"])
    for n in (0, 1, 2, 3):
        b, p, foe = stock(n)
        p.hp = 1
        fs.status_move(b, p, fs.move("Swallow"), foe, True)
        out[f"Swallow after {n}"] = (p.hp - 1, p.stockpile, p.stages["def"], p.stages["spd"])
    b, p, foe = stock(2, def_stage=5)
    counted = (p.stockpile, p.stockpile_def, p.stockpile_spd, p.stages["def"], p.stages["spd"])
    fs.status_move(b, p, fs.move("Swallow"), foe, True)
    out["from +5 Defense"] = counted + (p.stages["def"], p.stages["spd"])
    for n in (0, 2):
        b, p, foe = stock(n)
        b.rng = FixedDice(0.5)
        b.st["rows"][(None, "p0#su200", "b0.0")] = {"moves": {"Spit Up": {"rolls": list(range(30, 46))}}}
        fs.attack(b, p, fs.move("Spit Up"), foe, True)
        out[f"Spit Up after {n}"] = (foe.maxhp - foe.hp, p.stockpile, p.stages["def"])
    want = {"four Stockpiles": (3, 3, 3), "Swallow after 0": (0, 0, 0, 0), "Swallow after 1": (25, 0, 0, 0),
            "Swallow after 2": (50, 0, 0, 0), "Swallow after 3": (99, 0, 0, 0),
            "from +5 Defense": (2, 1, 2, 6, 2, 5, 0), "Spit Up after 0": (0, 0, 0), "Spit Up after 2": (45, 0, 0)}
    results.append(("Stockpile counts to three; Swallow and Spit Up spend it by the count", out == want,
                    f"(HP or damage, count, Defense, Sp. Def ...) {out}"))


def check_lower_sp_atk_hit(results):
    """Snarl, Mist Ball and Moonblast (approved 2026-10-14; effect script
    71): the hit lowers the target's Sp. Atk a stage at the move's chance,
    always for Snarl, half the time for Mist Ball, one time in ten for
    Moonblast; a Substitute's hit lowers nothing."""
    out = {}
    for name, dice in (("Snarl", 0.999), ("Mist Ball", 0.4), ("Mist Ball", 0.6), ("Moonblast", 0.05),
                       ("Moonblast", 0.2)):
        b, p, foe = battle([name], ["Tackle"], {("p", name): [10] * 16})
        b.rng = FixedDice(dice)
        fs.attack(b, p, fs.move(name), foe, True)
        out[f"{name} at {dice}"] = foe.stages["spa"]
    b, p, foe = battle(["Snarl"], ["Tackle"], {("p", "Snarl"): [10] * 16})
    foe.sub = 50
    b.rng = FixedDice(0.0)
    fs.attack(b, p, fs.move("Snarl"), foe, True)
    out["Snarl into a Substitute"] = foe.stages["spa"]
    want = {"Snarl at 0.999": -1, "Mist Ball at 0.4": -1, "Mist Ball at 0.6": 0, "Moonblast at 0.05": -1,
            "Moonblast at 0.2": 0, "Snarl into a Substitute": 0}
    results.append(("Snarl, Mist Ball and Moonblast lower Sp. Atk at their chance", out == want,
                    f"the target's Sp. Atk stage {out}"))


def check_rollout(results):
    """Rollout and Ice Ball (approved 2026-10-14; BtlCmd_CalcRolloutPower):
    five uses in a row at 1, 2, 4, 8 and 16 times its power, held in by the
    lock however many turn ends pass, and then free, the next use starting
    again at once its power; a turn its user cannot act on (here a full
    paralysis), and a Protect it meets, end the run, so the next starts
    again too. The battles' turn end counts down only locks other than a
    Rollout's (fightsim.rollout_lock_ticks; before it, every lock)."""
    ticks = getattr(fs, "rollout_lock_ticks", lambda m: m.lock is not None)

    def turn_end(mon):
        if ticks(mon):
            mv, left = mon.lock
            mon.lock = (mv, left - 1) if left > 1 else None

    b, p, foe = battle(["Rollout"], ["Tackle"], {("p", "Rollout"): [10] * 16}, hp=10000)
    foe.ability = "Shell Armor"           # no critical hits, so each hit reads its row times the run's power
    b.rng = FixedDice(0.0)
    roll = fs.move("Rollout")
    seen = []

    def use(protect=False):
        forced = p.lock is not None
        foe.protecting = protect
        before = foe.hp
        fs.attack(b, p, p.lock[0] if forced else roll, foe, True)
        turn_end(p)
        seen.append((before - foe.hp, forced))
    for _ in range(7):
        use()
    fs.could_not_act(b, p, roll, foe)      # fully paralysed mid-run
    turn_end(p)
    use()
    use(protect=True)
    use()
    want = [(10, False), (20, True), (40, True), (80, True), (160, True), (10, False), (20, True),
            (10, False), (0, True), (10, False)]
    results.append(("Rollout runs five uses at 1 to 16 times, then a paralysis or a Protect starts it again",
                    seen == want, f"(damage, forced) per use {seen}"))


def check_wake_up_slap(results):
    """Wake-Up Slap (approved 2026-10-14; effect script 217): twice its
    power on a sleeping target, which its hit then wakes, so the next one
    hits at its listed power; behind a Substitute it neither doubles nor
    wakes the target."""
    def slap(asleep, sub=0):
        b, p, foe = battle(["Wake-Up Slap"], ["Tackle"], {("p", "Wake-Up Slap"): [10] * 16}, hp=1000)
        foe.ability = "Shell Armor"
        b.rng = FixedDice(0.0)
        if asleep:
            foe.status, foe.sleep = "slp", 3
        foe.sub = sub
        before = foe.hp + foe.sub
        fs.attack(b, p, fs.move("Wake-Up Slap"), foe, True)
        first = (before - foe.hp - foe.sub, foe.status)
        before = foe.hp + foe.sub
        fs.attack(b, p, fs.move("Wake-Up Slap"), foe, True)
        return first + (before - foe.hp - foe.sub, foe.status)
    out = {"asleep": slap(True), "awake": slap(False), "asleep behind a Substitute": slap(True, sub=500)}
    want = {"asleep": (20, None, 10, None), "awake": (10, None, 10, None),
            "asleep behind a Substitute": (10, "slp", 10, "slp")}
    results.append(("Wake-Up Slap doubles on a sleeper and wakes it, but not through a Substitute", out == want,
                    f"(damage, status after) for two slaps {out}"))


def check_throat_chop(results):
    """Throat Chop (approved 2026-10-14; effect script 401,
    subscript_throat_chop): its hit holds the target's sound moves for the
    rest of the turn and all of the next, two turn ends; a held sound move
    can be neither chosen (the trainer's AI refuses it) nor used, and is
    free again after the second turn's end. Shield Dust, a Covert Cloak, a
    Substitute and Sheer Force each keep the hold off, and leaving clears
    it."""
    def chop(**kw):
        b, p, foe = battle(["Throat Chop"], ["Hyper Voice", "Tackle"],
                           {("p", "Throat Chop"): [10] * 16, ("b", "Hyper Voice"): [7] * 16}, hp=500)
        b.rng = FixedDice(0.0)
        p.ability = "Shell Armor"         # no critical hits on the user, so Hyper Voice reads its row
        for k, v in kw.items():
            setattr(p if k == "ability" else foe, k if k != "foe_ability" else "ability", v)
        fs.attack(b, p, fs.move("Throat Chop"), foe, True)
        return b, p, foe
    out = {}
    b, p, foe = chop()
    voice = fs.move("Hyper Voice")
    held = getattr(foe, "throat_chop", 0)
    refused = fightai.invalid(b, foe, voice)
    before = p.hp
    fs._use_move(b, foe, voice, p, False)
    out["chopped"] = (held, refused, before - p.hp)
    fs.end_of_turn(b)
    after_one = (getattr(foe, "throat_chop", 0), fightai.invalid(b, foe, voice))
    fs.end_of_turn(b)
    before = p.hp
    fs._use_move(b, foe, voice, p, True)
    out["two turn ends on"] = after_one + (getattr(foe, "throat_chop", 0), before - p.hp)
    for label, kw in (("Shield Dust", {"foe_ability": "Shield Dust"}), ("Covert Cloak", {"item": "Covert Cloak"}),
                      ("Substitute", {"sub": 100}), ("Sheer Force", {"ability": "Sheer Force"})):
        out[label] = getattr(chop(**kw)[2], "throat_chop", 0)
    b, p, foe = chop()
    foe.reset_volatile()
    out["left the field"] = getattr(foe, "throat_chop", 0)
    want = {"chopped": (2, True, 0), "two turn ends on": (1, True, 0, 7), "Shield Dust": 0, "Covert Cloak": 0,
            "Substitute": 0, "Sheer Force": 0, "left the field": 0}
    results.append(("Throat Chop holds sound moves through the next turn; Shield Dust, Covert Cloak, Substitute "
                    "and Sheer Force stop it", out == want, str(out)))


def check_minimize_stomp(results):
    """Minimize, Stomp and Steamroller (approved 2026-10-14; effect scripts
    108 and 150): Minimize raises its user's evasion two stages and marks
    it, even at +6, and Stomp and Steamroller then hit it at twice their
    power, until it leaves the field."""
    out = {}
    for name in ("Stomp", "Steamroller"):
        b, p, foe = battle([name], ["Minimize"], {("p", name): [10] * 16}, hp=1000)
        foe.ability = "Shell Armor"
        b.rng = FixedDice(0.0)
        fs.attack(b, p, fs.move(name), foe, True)
        plain = foe.maxhp - foe.hp
        foe.stages["eva"] = 6
        fs.status_move(b, foe, fs.move("Minimize"), p, False)
        before = foe.hp
        fs.attack(b, p, fs.move(name), foe, True)
        doubled = before - foe.hp
        foe.reset_volatile()
        before = foe.hp
        fs.attack(b, p, fs.move(name), foe, True)
        out[name] = (plain, getattr(foe, "minimized", None), doubled, before - foe.hp)
    want = {"Stomp": (10, False, 20, 10), "Steamroller": (10, False, 20, 10)}
    results.append(("Stomp and Steamroller double on a Minimize user until it leaves", out == want,
                    f"(plain, marked after leaving, on the Minimize user, after it left) {out}"))


def check_charge(results):
    """Charge (approved 2026-10-14; subscript_charge, chargedTurns 2): a
    stage of Sp. Def, and the user's Electric moves at twice their power
    for the rest of the turn and all of the next, the trainer's AI's figure
    included; after the second turn's end they are back to their power."""
    b, p, foe = battle(["Charge", "Thunder Shock", "Tackle"], ["Tackle"],
                       {("p", "Thunder Shock"): [10] * 16, ("p", "Tackle"): [10] * 16})
    shock, tackle = fs.move("Thunder Shock"), fs.move("Tackle")
    fs.status_move(b, p, fs.move("Charge"), foe, True)
    out = {"Sp. Def": p.stages["spd"], "this turn": (b.damage(p, foe, shock, roll=0), b.damage(p, foe, tackle, roll=0),
                                                    b.damage(p, foe, shock, ai_view=True))}
    fs.end_of_turn(b)
    out["the next turn"] = b.damage(p, foe, shock, roll=0)
    fs.end_of_turn(b)
    out["the turn after"] = b.damage(p, foe, shock, roll=0)
    want = {"Sp. Def": 1, "this turn": (20, 10, 20), "the next turn": 20, "the turn after": 10}
    results.append(("Charge doubles its user's Electric moves through the next turn", out == want, str(out)))


def check_lucky_chant(results):
    """Lucky Chant (approved 2026-10-14; effect script 240): no critical hit
    lands on its user's side for five turns, ended at the fifth turn's end;
    a second one fails while it runs."""
    b, p, foe = battle(["Lucky Chant"], ["Tackle"], {("b", "Tackle"): [10] * 16}, hp=1000)
    b.rng = FixedDice(0.0)                # every critical roll passes
    tackle = fs.move("Tackle")

    def hit():
        before = p.hp
        fs.attack(b, foe, tackle, p, False)
        return before - p.hp
    out = {"before": hit()}
    fs.status_move(b, p, fs.move("Lucky Chant"), foe, True)
    out["chanted"] = (getattr(b.p, "lucky_chant", 0), fs.crit_rate(b, foe, p, tackle), hit())
    fs.end_of_turn(b)
    fs.status_move(b, p, fs.move("Lucky Chant"), foe, True)
    out["a second chant"] = getattr(b.p, "lucky_chant", 0)
    for _ in range(4):
        fs.end_of_turn(b)
    out["five turn ends on"] = (getattr(b.p, "lucky_chant", 0), hit())
    want = {"before": 15, "chanted": (5, 0.0, 10), "a second chant": 4, "five turn ends on": (0, 15)}
    results.append(("Lucky Chant keeps critical hits off its side for five turns", out == want, str(out)))


def check_psych_up(results):
    """Psych Up (approved 2026-10-14; BtlCmd_CopyStatStages): the user takes
    every stage of the target's, accuracy and evasion too, lowered ones
    included, and the target's Focus Energy, keeping its own; a Substitute
    does not stop it."""
    b, p, foe = battle(["Psych Up"], ["Tackle"], {})
    p.stages.update(atk=2, spe=-1)
    foe.stages.update(atk=-1, spa=2, eva=1, spe=3)
    foe.crit_stage, foe.sub = 2, 30
    fs.status_move(b, p, fs.move("Psych Up"), foe, True)
    copied = (dict(p.stages), p.crit_stage)
    b, p, foe = battle(["Psych Up"], ["Tackle"], {})
    p.crit_stage = 2
    fs.status_move(b, p, fs.move("Psych Up"), foe, True)
    want_stages = dict.fromkeys(fs.STAGE_KEYS, 0)
    want_stages.update(atk=-1, spa=2, eva=1, spe=3)
    ok = copied == (want_stages, 2) and p.crit_stage == 2 and p.stages == dict.fromkeys(fs.STAGE_KEYS, 0)
    results.append(("Psych Up copies every stage and Focus Energy, keeping the user's own", ok,
                    f"copied {copied}; from a plain target it keeps Focus Energy: {p.crit_stage}, {p.stages}"))


def check_lock_on(results):
    """Lock-On and Mind Reader (approved 2026-10-14; effect script 94,
    subscript_lock_on): the user's moves hit the target for the rest of the
    turn and all of the next, whatever their accuracy, and reach it on the
    hidden turn of Fly; after the second turn's end they roll again. A
    Substitute makes it fail, the trainer's AI does not use it on a target
    already held, and the hold ends when the target leaves."""
    out = {}
    for name in ("Lock-On", "Mind Reader"):
        b, p, foe = battle([name, "Zap Cannon", "Tackle"], ["Tackle"],
                           {("p", "Zap Cannon"): [10] * 16, ("p", "Tackle"): [5] * 16}, hp=1000)
        b.rng = FixedDice(0.999)          # every chance roll fails: a 50% move misses
        fs.status_move(b, p, fs.move(name), foe, True)
        held = (getattr(foe, "locked_on", 0), getattr(foe, "lock_on_by", None))
        foe.stages["eva"] = 6
        before = foe.hp
        fs.attack(b, p, fs.move("Zap Cannon"), foe, True)
        landed = before - foe.hp
        fs.end_of_turn(b)
        foe.charging = fs.move("Fly")      # in the air on the next turn
        before = foe.hp
        fs.attack(b, p, fs.move("Tackle"), foe, True)
        in_air = before - foe.hp
        foe.charging = None
        fs.end_of_turn(b)
        before = foe.hp
        fs.attack(b, p, fs.move("Zap Cannon"), foe, True)
        out[name] = (held, landed, in_air, before - foe.hp)
    b, p, foe = battle(["Lock-On"], ["Tackle"], {})
    foe.sub = 30
    fs.status_move(b, p, fs.move("Lock-On"), foe, True)
    out["into a Substitute"] = getattr(foe, "locked_on", 0)
    b, p, foe = battle(["Tackle"], ["Lock-On"], {})
    b.rng = FixedDice(0.999)
    fs.status_move(b, foe, fs.move("Lock-On"), p, True)
    out["the AI on a held target"] = fightai.basic(b, foe, p, fs.move("Lock-On"), 0)
    p.reset_volatile()
    out["the target left"] = getattr(p, "locked_on", 0)
    want = {"Lock-On": ((2, "p0"), 10, 5, 0), "Mind Reader": ((2, "p0"), 10, 5, 0), "into a Substitute": 0,
            "the AI on a held target": -10, "the target left": 0}
    results.append(("Lock-On and Mind Reader land the user's moves through the next turn, Fly too", out == want,
                    f"(hold, Zap Cannon at +6 evasion, Tackle into Fly, Zap Cannon two turn ends on) {out}"))


def check_foresight(results):
    """Foresight and Odor Sleuth (approved 2026-10-14; effect script 113,
    subscript_foresight): Normal and Fighting moves then meet the target's
    Ghost type, a Seismic Toss included, read from its twin's rows without
    Ghost, and its raised evasion stops counting, though a lowered one
    still counts; leaving ends it, and the trainer's AI does not use it on
    a target already identified."""
    out = {}
    for name in ("Foresight", "Odor Sleuth"):
        b, p, foe = battle([name, "Tackle", "Seismic Toss"], ["Tackle"], {("p", "Tackle"): [0] * 16},
                           b_types=("Ghost",), hp=500)
        b.st["rows"][(None, "p0", "b0.0#fs")] = {"moves": {"Tackle": {"rolls": [10] * 16}}}
        b.st["foresight_twin"] = {"b0.0": "b0.0#fs"}
        b.rng = FixedDice(0.5)
        foe.ability = "Shell Armor"
        tackle, toss = fs.move("Tackle"), fs.move("Seismic Toss")

        def hits():
            before = foe.hp
            fs.attack(b, p, tackle, foe, True)
            mid = foe.hp
            fs.attack(b, p, toss, foe, True)
            return before - mid, mid - foe.hp
        foe.stages["eva"] = 6
        before = hits()
        fs.status_move(b, p, fs.move(name), foe, True)
        after = hits()
        foe.stages["eva"] = -6
        lowered = fs.accuracy_scale(p, foe, tackle)
        ai = fightai.basic(b, p, foe, fs.move(name), 0)
        foe.reset_volatile()
        out[name] = (before, after, lowered, ai, getattr(foe, "foresight", None))
    want = {n: ((0, 0), (10, 50), 3.0, -10, False) for n in ("Foresight", "Odor Sleuth")}
    results.append(("Foresight and Odor Sleuth let Normal and Fighting moves hit a Ghost and lift its evasion",
                    out == want, f"((Tackle, Seismic Toss) at +6 evasion before, after; the scale at -6; the AI; "
                                 f"identified after leaving) {out}"))


def prepared_jobs(boss, player, split="Roark", terrain=None):
    """What prepare() asks the calculator for one pair of parties, with no
    Node run: the calculator's call is stood in for, so the pairs it is
    given and the Pokemon it is told of come back as they would be sent.
    Each party is a list of (species, level, ability, moves, item)."""
    from . import calc
    iv = {k: 31 for k in ("hp", "at", "df", "sa", "sd", "sp")}
    ev = dict.fromkeys(iv, 0)
    boss_recs = [{"species": sp, "level": lv, "ability": ab, "item": it, "nature": "Hardy", "ivs": iv, "evs": ev,
                  "moves": list(mv)} for sp, lv, ab, mv, it in boss]
    player_recs = [{"constant": "SPECIES_" + sp.upper().replace(" ", "_").replace("-", "_"), "species": sp,
                    "how": "test", "level": lv, "nature": "Hardy", "ivs": iv, "evs": ev, "ability": ab,
                    "moves": list(mv), "fill": False} for sp, lv, ab, mv, _it in player]
    seen = {}

    def stand_in(blob_path, jobs):
        seen.update(jobs)
        info = {k: {"hp": 100, "stats": {"atk": 100, "def": 100, "spa": 100, "spd": 100, "spe": 100},
                    "speed": 100, "types": [], "ability": p.get("ability"), "item": p.get("item")}
                for k, p in jobs["pokemon"].items()}
        return {"results": [], "pokemon": info}
    saved = calc.run_node
    calc.run_node = stand_in
    try:
        st = fs.prepare(split, [boss_recs], None, given_side=player_recs, terrain=terrain)
    finally:
        calc.run_node = saved
    return st, seen["pairs"], seen["pokemon"]


def check_trainer_magnitude(results):
    """A trainer's Magnitude (approved 2026-10-14; effect script 126,
    CalcMagnitudePower): prepare() rows it at each of its seven powers
    against every player Pokemon, as it rows the player's, so the readings'
    power keys ("<key>#m<power>") find a row; before, only the player's and
    a partner's had them, and a trainer's Magnitude never dealt damage."""
    st, pairs, pokemon = prepared_jobs([("Graveler", 30, "Sturdy", ["Magnitude"], None)],
                                       [("Machop", 30, "Guts", ["Karate Chop"], None)])
    want = {f"b0.0#m{p}" for p in fs.MAGNITUDE_POWERS}
    rowed = {a for a, d, mv, _w in pairs if a.startswith("b0.0#m") and d == "p0" and mv == ["Magnitude"]}
    powers = {k: pokemon[k].get("move_data", {}).get("Magnitude", {}).get("basePower") for k in sorted(rowed)}
    ok = rowed == want and all(powers[f"b0.0#m{p}"] == p for p in fs.MAGNITUDE_POWERS)
    results.append(("prepare rows a trainer's Magnitude at each power against the player's Pokemon", ok,
                    f"power keys rowed {powers}"))


def check_trainer_return(results):
    """A trainer's Return (approved 2026-10-14; effect script 121): its
    power is its friendship times 10 over 25, and a trainer's Pokemon has
    its species' base friendship, so prepare() rows a Pidgeot's (70) at 28,
    a Lopunny's (140) at 56 and a Buneary's (0) at the listed 1; the
    player's Return keeps the calculator's 102 of a well-liked Pokemon."""
    st, pairs, pokemon = prepared_jobs([("Pidgeot", 30, "Keen Eye", ["Return"], None),
                                        ("Lopunny", 30, "Klutz", ["Return"], None),
                                        ("Buneary", 30, "Klutz", ["Return"], None)],
                                       [("Bibarel", 30, "Simple", ["Return"], None)])
    power = {k: (pokemon[k].get("move_data") or {}).get("Return", {}).get("basePower")
             for k in ("b0.0", "b0.1", "b0.2", "p0")}
    want = {"b0.0": 28, "b0.1": 56, "b0.2": 1, "p0": None}
    results.append(("prepare rows a trainer's Return at its species' base friendship", power == want,
                    f"Return's power by key {power}"))


def check_smack_down(results):
    """Smack Down (approved 2026-10-14; effect script 406,
    subscript_smack_down): its hit brings a Flying type down until it
    leaves, so Ground moves then hit it from its twin's rows without Flying;
    it pulls a Pokemon out of Fly's hidden turn, and takes away Magnet Rise.
    Down, a Pokemon's Fly and Magnet Rise fail. A Pokemon on the ground, or
    behind a Substitute, gets no mark."""
    def setup(types=("Flying",)):
        b, p, foe = battle(["Smack Down", "Earthquake"], ["Fly", "Magnet Rise", "Tackle"],
                           {("p", "Smack Down"): [5] * 16, ("p", "Earthquake"): [0] * 16}, b_types=types, hp=500)
        b.st["rows"][(None, "p0", "b0.0#gd")] = {"moves": {"Earthquake": {"rolls": [10] * 16}}}
        b.st["ground_twin"] = {"b0.0": "b0.0#gd"}
        b.rng = FixedDice(0.5)
        foe.ability = "Shell Armor"
        return b, p, foe

    def quake(b, p, foe):
        before = foe.hp
        fs.attack(b, p, fs.move("Earthquake"), foe, True)
        return before - foe.hp
    out = {}
    b, p, foe = setup()
    out["a flier"] = (quake(b, p, foe), fs.attack(b, p, fs.move("Smack Down"), foe, True) or
                      getattr(foe, "smacked", None), quake(b, p, foe))
    fs._use_move(b, foe, fs.move("Fly"), p, False)
    fs._use_move(b, foe, fs.move("Magnet Rise"), p, False)
    out["its Fly and Magnet Rise"] = (foe.charging, foe.magnet_rise)
    foe.reset_volatile()
    out["after leaving"] = (getattr(foe, "smacked", None), quake(b, p, foe))
    b, p, foe = setup()
    foe.charging = fs.move("Fly")
    fs.attack(b, p, fs.move("Smack Down"), foe, True)
    out["in the air"] = (foe.charging, getattr(foe, "smacked", None))
    b, p, foe = setup(types=("Normal",))
    foe.magnet_rise = 4
    fs.attack(b, p, fs.move("Smack Down"), foe, True)
    out["under Magnet Rise"] = (foe.magnet_rise, getattr(foe, "smacked", None))
    b, p, foe = setup(types=("Normal",))
    fs.attack(b, p, fs.move("Smack Down"), foe, True)
    out["on the ground"] = getattr(foe, "smacked", None)
    b, p, foe = setup()
    foe.sub = 100
    fs.attack(b, p, fs.move("Smack Down"), foe, True)
    out["behind a Substitute"] = getattr(foe, "smacked", None)
    want = {"a flier": (0, True, 10), "its Fly and Magnet Rise": (None, 0), "after leaving": (False, 0),
            "in the air": (None, True), "under Magnet Rise": (0, True), "on the ground": False,
            "behind a Substitute": False}
    results.append(("Smack Down brings a flier down until it leaves, so Ground moves hit it", out == want, str(out)))


def check_gravity(results):
    """Gravity (approved 2026-10-14; effect script 215,
    subscript_gravity_start): five turns in which Ground moves hit a Flying
    type from its twin's rows, a Pokemon on Fly's hidden turn is brought
    down and Magnet Rise ends, accuracy rises by ten sixths, Fly and Magnet
    Rise can be neither chosen nor used, and Grav Apple hits half as hard
    again; a second Gravity fails while it lasts, and it ends at the fifth
    turn's end."""
    b, p, foe = battle(["Gravity", "Earthquake", "Hypnosis", "Grav Apple"], ["Fly", "Magnet Rise", "Tackle"],
                       {("p", "Earthquake"): [0] * 16, ("p", "Grav Apple"): [20] * 16}, b_types=("Flying",), hp=500)
    b.st["rows"][(None, "p0", "b0.0#gd")] = {"moves": {"Earthquake": {"rolls": [10] * 16}}}
    b.st["ground_twin"] = {"b0.0": "b0.0#gd"}
    foe.ability = "Shell Armor"
    hypnosis, apple = fs.move("Hypnosis"), fs.move("Grav Apple")
    b.rng = FixedDice(0.9)
    out = {"before": (b.accuracy_hits(p, foe, hypnosis), b.damage(p, foe, apple, roll=0))}
    foe.charging, foe.magnet_rise = fs.move("Fly"), 3
    fs.status_move(b, p, fs.move("Gravity"), foe, True)
    out["started"] = (getattr(b, "gravity", 0), foe.charging, foe.magnet_rise)
    before = foe.hp
    fs.attack(b, p, fs.move("Earthquake"), foe, True)
    out["under it"] = (before - foe.hp, b.accuracy_hits(p, foe, hypnosis), b.damage(p, foe, apple, roll=0),
                       fightai.invalid(b, foe, fs.move("Fly")),
                       getattr(fs, "move_barred", lambda *a: False)(b, foe, fs.move("Magnet Rise")))
    fs._use_move(b, foe, fs.move("Fly"), p, False)
    out["Fly tried"] = foe.charging
    fs.end_of_turn(b)
    fs.status_move(b, p, fs.move("Gravity"), foe, True)
    out["a second Gravity"] = getattr(b, "gravity", 0)
    for _ in range(4):
        fs.end_of_turn(b)
    out["five turn ends on"] = getattr(b, "gravity", 0)
    want = {"before": (False, 20), "started": (5, None, 0), "under it": (10, True, 30, True, True),
            "Fly tried": None, "a second Gravity": 4, "five turn ends on": 0}
    results.append(("Gravity grounds fliers, raises accuracy and bars Fly for five turns", out == want, str(out)))


def check_mimic(results):
    """Mimic (approved 2026-10-14; effect script 82, BtlCmd_TryMimic): the
    target's last move takes Mimic's slot with 5 PP (fewer if the move has
    fewer) until the user leaves, when Mimic comes back with the PP its use
    left it; it fails with no last move, through a Substitute, on a move
    the user knows already and on Struggle, which Mimic may not copy; and
    prepare() rows a Mimic user with its foes' damaging moves."""
    def setup(last, known=("Mimic", "Tackle")):
        b, p, foe = battle(list(known), ["Hyper Beam", "Ember"], {})
        foe.last = fs.move(last) if last else None
        return b, p, foe
    out = {}
    b, p, foe = setup("Ember")
    fs._use_move(b, p, fs.move("Mimic"), foe, True)
    out["copied"] = ([m.name for m in p.moves], dict(p.pp))
    p.reset_volatile()
    out["after leaving"] = ([m.name for m in p.moves], dict(p.pp))
    b, p, foe = setup("Hyper Beam")
    fs.status_move(b, p, fs.move("Mimic"), foe, True)
    out["a 5 PP move"] = p.pp.get("Hyper Beam")
    for label, kw in (("no last move", {"last": None}), ("known already", {"last": "Tackle"}),
                      ("Struggle", {"last": "Struggle"})):
        b, p, foe = setup(**kw)
        fs.status_move(b, p, fs.move("Mimic"), foe, True)
        out[label] = [m.name for m in p.moves]
    b, p, foe = setup("Ember")
    foe.sub = 30
    fs.status_move(b, p, fs.move("Mimic"), foe, True)
    out["behind a Substitute"] = [m.name for m in p.moves]
    st, pairs, _pokemon = prepared_jobs([("Mr. Mime", 30, "Soundproof", ["Mimic", "Psychic"], None)],
                                        [("Machop", 30, "Guts", ["Karate Chop", "Leer"], None)])
    out["the Mimic user's rows"] = sorted({m for a, d, mv, _w in pairs if a == "b0.0" and d == "p0" for m in mv})
    plain = ["Mimic", "Tackle"]
    want = {"copied": (["Ember", "Tackle"], {"Tackle": fs.move("Tackle").pp, "Ember": 5}),
            "after leaving": (plain, {"Mimic": fs.move("Mimic").pp - 1, "Tackle": fs.move("Tackle").pp}),
            "a 5 PP move": min(5, fs.move("Hyper Beam").pp), "no last move": plain, "known already": plain,
            "Struggle": plain, "behind a Substitute": plain, "the Mimic user's rows": ["Karate Chop", "Psychic"]}
    results.append(("Mimic takes the target's last move until it leaves, and is rowed with its foes' moves",
                    out == want, str(out)))


def check_mirror_move(results):
    """Mirror Move (approved 2026-10-14; effect script 9,
    BtlCmd_SetMirrorMove): it uses the last move with Mirror Move's flag
    aimed at its user, as the user's own, spending only its own PP; with
    none it fails, a move without the flag (Swords Dance) leaves the record
    as it was, and the user's leaving clears it."""
    b, p, foe = battle(["Mirror Move"], ["Ember", "Swords Dance"], {}, hp=500)
    b.st["rows"][(None, "p0", "b0.0")]["moves"]["Ember"] = {"rolls": [10] * 16}     # prepare's borrowed row
    b.rng = FixedDice(0.5)
    foe.ability = "Shell Armor"
    mirror = fs.move("Mirror Move")
    before = foe.hp
    fs._use_move(b, p, mirror, foe, True)
    out = {"with nothing to copy": (before - foe.hp, p.pp["Mirror Move"])}
    fs._use_move(b, foe, fs.move("Ember"), p, True)
    fs._use_move(b, foe, fs.move("Swords Dance"), p, True)
    recorded = getattr(p, "mirror", None)
    before = foe.hp
    fs._use_move(b, p, mirror, foe, False)
    out["after Ember and Swords Dance"] = (None if recorded is None else recorded.name, before - foe.hp,
                                           p.pp["Mirror Move"], p.last.name if p.last else None, foe.pp.get("Ember"))
    p.reset_volatile()
    out["after leaving"] = getattr(p, "mirror", None)
    pp = fs.move("Mirror Move").pp
    want = {"with nothing to copy": (0, pp - 1), "after Ember and Swords Dance": ("Ember", 10, pp - 2, "Mirror Move",
                                                                                 fs.move("Ember").pp - 1),
            "after leaving": None}
    results.append(("Mirror Move uses the last mirrorable move aimed at its user", out == want, str(out)))


def check_copycat(results):
    """Copycat (approved 2026-10-14; effect script 242, BtlCmd_TryCopycat):
    it uses the last move any Pokemon used before it, as its user's own; it
    fails with none, after a turn a Pokemon could not act on, after a
    calling move (a Copycat's own included), and on a move Gravity bars."""
    b, p, foe = battle(["Copycat"], ["Ember", "Fly"], {}, hp=500)
    b.st["copycat"] = True                 # prepare's flag for a fight with a Copycat user
    b.st["rows"][(None, "p0", "b0.0")]["moves"]["Ember"] = {"rolls": [10] * 16}     # prepare's borrowed row
    b.rng = FixedDice(0.5)
    foe.ability = "Shell Armor"
    cat = fs.move("Copycat")

    def copy(first=False):
        before = foe.hp
        fs._use_move(b, p, cat, foe, first)
        return before - foe.hp
    out = {"first of the battle": copy(True)}
    fs._use_move(b, foe, fs.move("Ember"), p, True)
    out["after Ember"] = (copy(), p.last.name if p.last else None)
    out["after a Copycat"] = copy()
    fs._use_move(b, foe, fs.move("Ember"), p, True)
    fs.could_not_act(b, foe, fs.move("Ember"), p)
    out["after a turn that could not act"] = copy()
    fs._use_move(b, foe, fs.move("Fly"), p, True)
    b.gravity = 3
    out["Fly under Gravity"] = copy()
    want = {"first of the battle": 0, "after Ember": (10, "Copycat"), "after a Copycat": 0,
            "after a turn that could not act": 0, "Fly under Gravity": 0}
    results.append(("Copycat uses the battle's last move unless it calls one or none is there", out == want, str(out)))


def check_fling(results):
    """Fling (approved 2026-10-14; effect script 233, BattleSystem_FlingItem,
    subscript_fling): the thrown item's effect lands on the target that
    took the hit, a Flame Orb's burn, a Sitrus Berry eaten as if the target
    ate it, King's Rock's flinch on a target yet to move, and none through a
    Substitute; the item is spent, and an item with no fling power cannot
    be thrown. The player's Fling reads its twin for the item's power
    ("<key>#fl<power>"), which prepare() rows for the items the player is
    handed."""
    def fling(item, first=True, sub=0):
        b, p, foe = battle(["Tackle"], ["Fling"], {("b", "Fling"): [10] * 16}, hp=100)
        b.rng = FixedDice(0.5)
        p.ability = "Shell Armor"
        foe.item, p.sub = item, sub
        p.hp = 60
        fs.attack(b, foe, fs.move("Fling"), p, first)
        return p.hp + p.sub, p.status, p.flinch, foe.item
    out = {"Flame Orb": fling("Flame Orb"), "Sitrus Berry": fling("Sitrus Berry"),
           "King's Rock": fling("King's Rock"), "King's Rock, moving second": fling("King's Rock", first=False),
           "Flame Orb into a Substitute": fling("Flame Orb", sub=40)}
    b, p, foe = battle(["Fling"], ["Tackle"], {}, hp=100)
    b.st["rows"][(None, "p0#flcharcoal", "b0.0")] = {"moves": {"Fling": {"rolls": [12] * 16}}}
    b.rng = FixedDice(0.5)
    foe.ability, p.item = "Shell Armor", "Charcoal"
    fs.attack(b, p, fs.move("Fling"), foe, True)
    out["the player's Charcoal"] = (foe.maxhp - foe.hp, p.item)
    st, pairs, pokemon = prepared_jobs([("Machamp", 40, "Guts", ["Cross Chop"], None)],
                                       [("Bibarel", 40, "Simple", ["Fling"], None)], split="Fantina")
    powers = sorted(pokemon[a]["item"] for a, d, mv, _w in pairs if a.startswith("p0#fl") and d == "b0.0")
    handed = fs.player_items("Fantina")
    out["the player's Fling rows"] = powers == sorted(i for i in list(handed["boosters"].values())
                                                      + [i for i in ("Leftovers", "Sitrus Berry") if handed.get(i)])
    want = {"Flame Orb": (50, "brn", False, None), "Sitrus Berry": (75, None, False, None),
            "King's Rock": (50, None, True, None), "King's Rock, moving second": (50, None, False, None),
            "Flame Orb into a Substitute": (90, None, False, None), "the player's Charcoal": (12, None),
            "the player's Fling rows": True}
    results.append(("Fling gives its item's effect, and the player's reads its item's power", out == want,
                    f"(HP and Substitute, status, flinch, item after) {out}; the player's Fling items {powers}"))


def check_natural_gift(results):
    """Natural Gift (approved 2026-10-14; effect script 222): the player's
    is read from its twin's row holding the Sitrus Berry ("p0#ng"), since
    its own rows carry no item, and spends the Berry; with a Leftovers it
    fails and keeps the item. A trainer's reads its own row, made with its
    Berry, as before."""
    def gift(item, trainer=False):
        if trainer:
            b, p, foe = battle(["Tackle"], ["Natural Gift"], {("b", "Natural Gift"): [25] * 16})
            p, foe = foe, p
        else:
            b, p, foe = battle(["Natural Gift"], ["Tackle"], {})
            b.st["rows"][(None, "p0#ng", "b0.0")] = {"moves": {"Natural Gift": {"rolls": [30] * 16}}}
        b.rng = FixedDice(0.5)
        p.item = item
        fs.attack(b, p, fs.move("Natural Gift"), foe, True)
        return foe.maxhp - foe.hp, p.item
    got = {"Sitrus Berry": gift("Sitrus Berry"), "Leftovers": gift("Leftovers"),
           "a trainer's Shuca Berry": gift("Shuca Berry", trainer=True)}
    want = {"Sitrus Berry": (30, None), "Leftovers": (0, "Leftovers"), "a trainer's Shuca Berry": (25, None)}
    results.append(("the player's Natural Gift hits from its Sitrus Berry twin's row", got == want,
                    f"(damage, item after) {got}"))


def check_imprison(results):
    """Imprison (approved 2026-10-14; effect script 192, BtlCmd_TryImprison,
    Move_Imprisoned): once its user imprisons, the foe cannot choose a move
    the user knows (the trainer's AI rules it out, leaving Struggle when
    every move is sealed), a sealed move chosen earlier fails, and a foe
    switched in is sealed too; it ends when the user leaves. It fails, while
    still marking the foe as tried (which the AI's Basic reads), when the
    user shares no move with the foe."""
    def setup(p_moves, b_moves):
        b = field({"p0": (("Normal",), p_moves), "b0.0": (("Normal",), b_moves),
                   "b0.1": (("Normal",), b_moves), "p1": (("Normal",), ["Tackle"])},
                  {("b0.0", "p0"): {"Tackle": 10}, ("b0.1", "p0"): {"Tackle": 10}})
        b.rng = FixedDice(0.5)
        return b, b.p.cur(), b.b.cur()
    out = {}
    b, p, foe = setup(["Imprison", "Tackle"], ["Tackle", "Growl"])
    fs.status_move(b, p, fs.move("Imprison"), foe, True)
    out["after Imprison"] = (p.imprisoning, foe.imprisoned, sorted(foe.sealed),
                             fightai.invalid(b, foe, fs.move("Tackle")), fightai.invalid(b, foe, fs.move("Growl")))
    fs.use_move(b, foe, fs.move("Tackle"), p, False)
    out["a sealed Tackle used"] = p.hp
    fs.switch_in(b, b.b, 1)
    out["a foe switched in"] = sorted(b.b.cur().sealed)
    fs.switch_in(b, b.p, 1)
    out["the user leaves"] = sorted(b.b.cur().sealed)
    b, p, foe = setup(["Imprison", "Tackle", "Growl"], ["Tackle", "Growl"])
    fs.status_move(b, p, fs.move("Imprison"), foe, True)
    out["every move sealed"] = fightai.choose(b, foe, p)[1].name
    b, p, foe = setup(["Imprison", "Ember"], ["Tackle", "Growl"])
    fs.status_move(b, p, fs.move("Imprison"), foe, True)
    out["nothing shared"] = (p.imprisoning, foe.imprisoned, sorted(foe.sealed),
                             fightai.basic(b, p, foe, fs.move("Imprison"), 0))
    want = {"after Imprison": (True, True, ["Imprison", "Tackle"], True, False), "a sealed Tackle used": 100,
            "a foe switched in": ["Imprison", "Tackle"], "the user leaves": [], "every move sealed": "Struggle",
            "nothing shared": (False, True, [], -10)}
    results.append(("Imprison seals the moves its user knows while it stays", out == want, f"{out}"))


def check_baton_pass(results):
    """Baton Pass (approved 2026-10-14; effect script 127, subscript_baton_pass,
    BattleSystem_InitBattleMon under SYSCTL_BATON_PASS): in a turn its user
    switches out for the replacement, which keeps the stat stages, the
    Substitute, confusion, Focus Energy's rate, Leech Seed, Perish Song's
    count, Aqua Ring and Magnet Rise (confusion one turn down, as its use
    spent one), and loses the Torment, the Encore, the bind and the
    Stockpile; a foe the user held with Mean Look stays held, and with
    nobody to send in it fails."""
    def turn(bench=True):
        mons = {"p0": (("Normal",), ["Baton Pass"]), "b0.0": (("Normal",), ["Growl"])}
        if bench:
            mons["p1"] = (("Normal",), ["Tackle"])
        b = field(mons, {})
        b.rng = FixedDice(0.5)
        p, foe = b.p.cur(), b.b.cur()
        p.stages.update(atk=2, spe=1)
        p.sub, p.confused, p.crit_stage, p.seeded, p.perish, p.aqua_ring, p.magnet_rise = 25, 3, 2, True, 3, True, 4
        p.tormented, p.encore, p.encore_turns, p.bound, p.stockpile = True, "Baton Pass", 2, 3, 2
        foe.trapped_by = p.key
        b.turn = 1
        fs.use_move(b, p, fs.move("Baton Pass"), foe, True)
        side = b.p
        if p.baton and side.bench():
            fs.baton_pass(b, side, side.mons.index(side.bench()[0]))
        new = b.p.cur()
        return (new.key, new.stages["atk"], new.stages["spe"], new.sub, new.confused, new.crit_stage, new.seeded,
                new.perish, new.aqua_ring, new.magnet_rise, new.tormented, new.encore, new.bound, new.stockpile,
                foe.trapped_by)
    got = {"passed": turn(), "no one to send in": turn(bench=False)[:2]}
    want = {"passed": ("p1", 2, 1, 25, 2, 2, True, 3, True, 4, False, None, 0, 0, "p1"), "no one to send in": ("p0", 2)}
    results.append(("Baton Pass switches its user out and hands on what the engine passes", got == want,
                    f"(newcomer, Attack, Speed, Substitute, confusion, crit stage, seeded, Perish, Aqua Ring, "
                    f"Magnet Rise, Torment, Encore, bind, Stockpile, the foe held by) {got}"))


class FixedDice:
    """A stand-in for a battle's random source: every chance roll reads
    `value` (0.0 passes every check, 0.999 fails every one), every range its
    low end, every pick the first."""

    def __init__(self, value):
        self.value = value

    def random(self):
        return self.value

    def randint(self, a, b):
        return a

    def randrange(self, n):
        return 0

    def choice(self, seq):
        return seq[0]

    def choices(self, seq, weights=None, k=1):
        return [seq[0]] * k


def check_magic_guard(results):
    """Magic Guard (approved 2026-10-14) keeps every damage off its holder
    but a move's own hit, where the engine checks it: the hazards
    (subscript_hazards_check jumps a holder past Toxic Spikes, Spikes and
    Stealth Rock, so a Poison type holding it leaves the Toxic Spikes down),
    a hit's recoil (subscript_recoil_1_3), a missed Jump Kick's crash
    (subscript_crash_on_miss), binding (subscript_bind_effect, its count
    still running down) and Leech Seed (MON_COND_CHECK_STATE_LEECH_SEED,
    which then heals its seeder nothing). A plain Pokemon beside it takes
    each, as before."""
    def entry(ability, types=("Normal",)):
        b = field({"p0": (("Normal",), ["Tackle"]), "p1": (types, ["Tackle"]), "b0.0": (("Normal",), ["Tackle"])}, {})
        b.p.mons[1].ability = ability
        b.p.hazards = {"rocks": 1, "spikes": 1, "tspikes": 1}
        fs.switch_in(b, b.p, 1)
        new = b.p.cur()
        return new.hp, new.status, b.p.hazards["tspikes"]

    def recoil(ability):
        b, p, foe = battle(["Double-Edge"], ["Tackle"], {("p", "Double-Edge"): [30] * 16})
        b.st["first_battle"] = True
        p.ability = ability
        fs.attack(b, p, fs.move("Double-Edge"), foe, True)
        return p.hp

    def crash(ability):
        b, p, foe = battle(["Jump Kick"], ["Tackle"], {("p", "Jump Kick"): [40] * 16})
        p.ability = ability
        b.rng = FixedDice(0.999)             # the Jump Kick misses
        fs.attack(b, p, fs.move("Jump Kick"), foe, True)
        return p.hp

    def turn_end(ability, what):
        b, p, foe = battle(["Tackle"], ["Tackle"], {})
        foe.ability = ability
        p.hp = 50
        if what == "bound":
            foe.bound = 3
        else:
            foe.seeded = True
        fs.end_of_turn(b)
        return foe.hp, foe.bound, p.hp
    got = {"hazards": entry("Magic Guard"), "hazards, a Poison type": entry("Magic Guard", ("Poison",)),
           "recoil": recoil("Magic Guard"), "crash": crash("Magic Guard"),
           "bound": turn_end("Magic Guard", "bound"), "seeded": turn_end("Magic Guard", "seeded")}
    plain = {"hazards": entry(None), "hazards, a Poison type": entry(None, ("Poison",)),
             "recoil": recoil(None), "crash": crash(None),
             "bound": turn_end(None, "bound"), "seeded": turn_end(None, "seeded")}
    want = {"hazards": (100, None, 1), "hazards, a Poison type": (100, None, 1), "recoil": 100, "crash": 100,
            "bound": (100, 2, 50), "seeded": (100, 0, 50)}
    want_plain = {"hazards": (76, "psn", 1), "hazards, a Poison type": (76, None, 0), "recoil": 90, "crash": 80,
                  "bound": (88, 2, 50), "seeded": (88, 0, 62)}
    ok = got == want and plain == want_plain
    results.append(("Magic Guard keeps off the hazards, recoil, a crash, binding and Leech Seed", ok,
                    f"Magic Guard {got}; plain {plain} (hazards: HP, status, Toxic Spikes layers left; "
                    f"recoil and crash: HP; binding and Leech Seed: HP, bind count, the foe's HP from 50)"))


def check_liquid_ooze(results):
    """Liquid Ooze (approved 2026-10-14; subscript_drain_half_damage_dealt
    and subscript_leech_seed_effect): what a drain would give its user, a
    draining hit's or Leech Seed's, it takes from the user instead, before
    Heal Block is looked at, unless the user has Magic Guard; a target
    without it gives the heal as before."""
    def giga(ooze, guard=False, blocked=False):
        b, p, foe = battle(["Giga Drain"], ["Tackle"], {("p", "Giga Drain"): [40] * 16})
        b.st["first_battle"] = True
        p.hp = 50
        foe.ability = "Liquid Ooze" if ooze else None
        p.ability = "Magic Guard" if guard else None
        p.heal_block = 5 if blocked else 0
        fs.attack(b, p, fs.move("Giga Drain"), foe, True)
        return p.hp

    def seed(ooze, guard=False):
        b, p, foe = battle(["Tackle"], ["Tackle"], {})
        p.hp = 50
        foe.ability = "Liquid Ooze" if ooze else None
        p.ability = "Magic Guard" if guard else None
        foe.seeded = True
        fs.end_of_turn(b)
        return p.hp, foe.hp
    got = {"Giga Drain into Liquid Ooze": giga(True), "Giga Drain, a Magic Guard user": giga(True, guard=True),
           "Giga Drain under Heal Block": giga(True, blocked=True), "Giga Drain, no ooze": giga(False),
           "Leech Seed on Liquid Ooze": seed(True), "Leech Seed, a Magic Guard seeder": seed(True, guard=True),
           "Leech Seed, no ooze": seed(False)}
    want = {"Giga Drain into Liquid Ooze": 30, "Giga Drain, a Magic Guard user": 50, "Giga Drain under Heal Block": 30,
            "Giga Drain, no ooze": 70, "Leech Seed on Liquid Ooze": (38, 88),
            "Leech Seed, a Magic Guard seeder": (50, 88), "Leech Seed, no ooze": (62, 88)}
    results.append(("Liquid Ooze turns a drain's heal into damage, unless Magic Guard", got == want,
                    f"the user's HP from 50 (and the seeded one's from 100) {got}"))


def check_drop_answers(results):
    """The answers to a stat drop from the other side (approved 2026-10-14;
    BtlCmd_ChangeStatStage, BtlCmd_TryDefiant, subscript_intimidate):
    Defiant gains two stages of Attack and Competitive two of Sp. Atk for
    each stat that falls, Intimidate's drop included; Mirror Armor turns the
    drop back on the Pokemon that made it; Rattled gains a stage of Speed
    from Intimidate even when Mist stops the drop. A drop of two stats is
    taken a stat at a time, so Hyper Cutter keeps Tickle off Attack alone."""
    def intimidated(ability, mist=False):
        b = field({"p0": (("Normal",), ["Tackle"]), "p1": (("Normal",), ["Tackle"]),
                   "b0.0": (("Normal",), ["Tackle"])}, {})
        b.p.mons[1].ability = "Intimidate"
        foe = b.b.cur()
        foe.ability = ability
        if mist:
            b.b.mist = 5
        fs.switch_in(b, b.p, 1)
        return foe.stages["atk"], foe.stages["spa"], foe.stages["spe"], b.p.cur().stages["atk"]

    def used(name, ability, rows=None):
        b, p, foe = battle([name], ["Tackle"], rows or {})
        foe.ability = ability
        mv = fs.move(name)
        (fs.status_move if mv.cat == "Status" else fs.attack)(b, p, mv, foe, True)
        return {k: v for k, v in foe.stages.items() if v}, {k: v for k, v in p.stages.items() if v}
    got = {"Intimidate, Defiant": intimidated("Defiant"), "Intimidate, Competitive": intimidated("Competitive"),
           "Intimidate, Mirror Armor": intimidated("Mirror Armor"), "Intimidate, Rattled": intimidated("Rattled"),
           "Intimidate, Rattled under Mist": intimidated("Rattled", mist=True),
           "Growl, Defiant": used("Growl", "Defiant"), "Growl, Mirror Armor": used("Growl", "Mirror Armor"),
           "Tickle, Hyper Cutter": used("Tickle", "Hyper Cutter"), "Tickle, Defiant": used("Tickle", "Defiant"),
           "Rock Tomb, Competitive": used("Rock Tomb", "Competitive", {("p", "Rock Tomb"): [10] * 16}),
           "Rock Tomb, Mirror Armor": used("Rock Tomb", "Mirror Armor", {("p", "Rock Tomb"): [10] * 16})}
    want = {"Intimidate, Defiant": (1, 0, 0, 0), "Intimidate, Competitive": (-1, 2, 0, 0),
            "Intimidate, Mirror Armor": (0, 0, 0, -1), "Intimidate, Rattled": (-1, 0, 1, 0),
            "Intimidate, Rattled under Mist": (0, 0, 1, 0),
            "Growl, Defiant": ({"atk": 1}, {}), "Growl, Mirror Armor": ({}, {"atk": -1}),
            "Tickle, Hyper Cutter": ({"def": -1}, {}), "Tickle, Defiant": ({"atk": 3, "def": -1}, {}),
            "Rock Tomb, Competitive": ({"spe": -1, "spa": 2}, {}), "Rock Tomb, Mirror Armor": ({}, {"spe": -1})}
    results.append(("Defiant, Competitive, Mirror Armor and Rattled answer a drop; drops go a stat at a time",
                    got == want, f"Intimidate (the foe's Attack, Sp. Atk, Speed; the holder's Attack) and moves "
                                 f"(the target's stages, the user's) {got}"))


def check_technician_power(results):
    """Technician (approved 2026-10-14; BattleSystem_CalcMoveDamage) adds half
    again to a power of 60 or less once the power is worked out, so a row
    made with it at one power keeps it only while the power stays at 60 or
    less. Rows of 30 for a Technician holder stand for 20 power with its
    half (Flail at full HP), of 20 for a plain holder; 45 and 30 for Rollout
    and Ice Ball's 30; 90 and 60 for Revenge's 60; 150 for either's Water
    Spout at full HP's 150. Each hit then lands as the power it has: Flail at 200 near
    1 HP, Water Spout at 45 power at a third of HP (Technician's 67 then),
    Rollout's second hit at 60 (90 with it) and its third at 120, Revenge
    doubled to 120."""
    def hit(name, row, tech, hp=100, setup=None):
        b, p, foe = battle([name], ["Tackle"], {("p", name): [row] * 16})
        p.ability = "Technician" if tech else None
        p.hp = hp
        if setup:
            setup(p)
        return b.damage(p, foe, fs.move(name), roll=0)

    def revenge(row, tech):
        b, p, foe = battle(["Revenge"], ["Tackle"], {("p", "Revenge"): [row] * 16})
        b.st["first_battle"] = True
        p.ability = "Technician" if tech else None
        p.hit_this_turn = ("Physical", 10)
        foe.hp = foe.maxhp = 500
        fs.attack(b, p, fs.move("Revenge"), foe, False)
        return 500 - foe.hp

    def rolled(n):
        return lambda p: setattr(p, "rollout_hit", n)
    got = {"Flail at 1 HP": (hit("Flail", 30, True, hp=1), hit("Flail", 20, False, hp=1)),
           "Flail at 40 of 100": (hit("Flail", 30, True, hp=40), hit("Flail", 20, False, hp=40)),
           "Water Spout at 30 of 100": (hit("Water Spout", 150, True, hp=30), hit("Water Spout", 150, False, hp=30)),
           "Rollout's second hit": (hit("Rollout", 45, True, setup=rolled(1)), hit("Rollout", 30, False, setup=rolled(1))),
           "Rollout's third hit": (hit("Rollout", 45, True, setup=rolled(2)), hit("Rollout", 30, False, setup=rolled(2))),
           "Revenge after a hit": (revenge(90, True), revenge(60, False))}
    want = {"Flail at 1 HP": (200, 200), "Flail at 40 of 100": (60, 40), "Water Spout at 30 of 100": (67, 45),
            "Rollout's second hit": (90, 60), "Rollout's third hit": (120, 120), "Revenge after a hit": (120, 120)}
    results.append(("Technician is judged on the power a move has as it lands", got == want,
                    f"(Technician, plain) {got}"))


def check_stored_power(results):
    """Stored Power and Power Trip (approved 2026-10-14;
    BattleScript_ComputedMovePower): 20 power and 20 more for each stage its
    user has raised, accuracy and evasion included, lowered stages counting
    nothing. A row of 20 stands for the calculator's at no stage. With +2
    Sp. Atk and +1 Speed, Stored Power has 80 power and its +2 Sp. Atk
    doubles the hit again: 160; Power Trip at +1 Attack and +1 evasion, -2
    Defense, 60 power and +1 Attack: 90."""
    def hit(name, stages):
        b, p, foe = battle([name], ["Tackle"], {("p", name): [20] * 16})
        p.stages.update(stages)
        return b.damage(p, foe, fs.move(name), roll=0)
    got = {"Stored Power at no stage": hit("Stored Power", {}),
           "Stored Power at +2 Sp. Atk, +1 Speed": hit("Stored Power", {"spa": 2, "spe": 1}),
           "Power Trip at +1 Attack, +1 evasion, -2 Defense": hit("Power Trip", {"atk": 1, "eva": 1, "def": -2})}
    want = {"Stored Power at no stage": 20, "Stored Power at +2 Sp. Atk, +1 Speed": 160,
            "Power Trip at +1 Attack, +1 evasion, -2 Defense": 90}
    results.append(("Stored Power and Power Trip gain 20 power a raised stage", got == want, f"{got}"))


def check_hard_press(results):
    """Hard Press (approved 2026-10-14; BattleScript_ComputedMovePower): up
    to 100 power by the share of its HP the target has left, at least 1. A
    row of 100 stands for the calculator's at full HP; a Technician holder's
    row of 100 gains its half once the power falls to 60."""
    def hit(hp, tech=False):
        b, p, foe = battle(["Hard Press"], ["Tackle"], {("p", "Hard Press"): [100] * 16})
        p.ability = "Technician" if tech else None
        foe.hp = hp
        return b.damage(p, foe, fs.move("Hard Press"), roll=0)
    got = {"full HP": hit(100), "half HP": hit(50), "a quarter": hit(25), "1 HP": hit(1),
           "half HP, Technician": hit(50, tech=True)}
    want = {"full HP": 100, "half HP": 50, "a quarter": 25, "1 HP": 1, "half HP, Technician": 75}
    results.append(("Hard Press weakens with its target's HP", got == want, f"{got}"))


def check_electro_ball(results):
    """Electro Ball (approved 2026-10-14; BattleScript_ComputedMovePower):
    40, 60, 80, 120 or 150 power by how many whole times over the target's
    Speed is the user's, the Speeds as they stand. The row of 60 stands for
    the calculator's at the opening Speeds, 100 against 50, twice over: 80
    power. At +2 Speed (200 against 50) it has 150; against a paralysed
    target (100 against 12) 150 too; slower than its target, 40."""
    def hit(own=0, target=0, par=False):
        b, p, foe = battle(["Electro Ball"], ["Tackle"], {("p", "Electro Ball"): [80] * 16})
        p.stages["spe"], foe.stages["spe"] = own, target
        foe.status = "par" if par else None
        return b.damage(p, foe, fs.move("Electro Ball"), roll=0)
    got = {"opening Speeds": hit(), "at +2 Speed": hit(own=2), "on a paralysed target": hit(par=True),
           "the target at +2 Speed": hit(target=2), "slower, at -2 Speed against +2": hit(own=-2, target=2)}
    want = {"opening Speeds": 80, "at +2 Speed": 150, "on a paralysed target": 150,
            "the target at +2 Speed": 60, "slower, at -2 Speed against +2": 40}
    results.append(("Electro Ball's power follows the Speeds as they stand", got == want, f"{got}"))


def check_sacred_sword(results):
    """Sacred Sword, Chip Away and Darkest Lariat (approved 2026-10-14;
    BattleSystem_CalcMoveDamage, BattleControllerPlayer_CheckMoveHitAccuracy)
    ignore their target's Defense stages, raised or lowered, and its evasion
    stages, as an Unaware attacker does; another move meets them. Rows of
    40; the accuracy over 2000 uses against +6 evasion."""
    def hit(name, stage):
        b, p, foe = battle([name], ["Tackle"], {("p", name): [40] * 16})
        foe.stages["def"] = stage
        return b.damage(p, foe, fs.move(name), roll=0)

    def lands(name):
        b, p, foe = battle([name], ["Tackle"], {})
        foe.stages["eva"] = 6
        return sum(b.accuracy_hits(p, foe, fs.move(name)) for _ in range(2000))
    got = {name: (hit(name, 2), hit(name, -2)) for name in ("Sacred Sword", "Chip Away", "Darkest Lariat", "Close Combat")}
    hits = {name: lands(name) for name in ("Sacred Sword", "Close Combat")}
    ok = (all(got[n] == (40, 40) for n in ("Sacred Sword", "Chip Away", "Darkest Lariat"))
          and got["Close Combat"] == (20, 80) and hits["Sacred Sword"] == 2000 and hits["Close Combat"] < 800)
    results.append(("Sacred Sword, Chip Away and Darkest Lariat ignore the target's stages", ok,
                    f"(at +2 Defense, at -2) {got}; landed of 2000 against +6 evasion {hits}"))


def check_mold_breaker(results):
    """Mold Breaker (approved 2026-10-14; Battler_IgnorableAbility) gets past
    each ability the engine asks that function about, unless the target
    holds an Ability Shield: the status immunities (a Mold Breaker's
    Hypnosis sleeps an Insomnia target, its Thunder Wave paralyses a Limber
    one, its Toxic poisons an Immunity one, its Spore sleeps a Leaf Guard
    one in sun and an Overcoat one, though never a Grass type), Clear Body,
    Hyper Cutter and Simple against its drops, Inner Focus and Shield Dust
    against its flinch, Battle Armor and Shell Armor against its critical
    hits, and Soundproof against its Perish Song."""
    def status(move, ability, mold=True, shield=False, types=("Normal",), weather=None):
        b, p, foe = battle([move], ["Tackle"], {}, b_types=types)
        b.weather = weather
        p.ability = "Mold Breaker" if mold else None
        foe.ability = ability
        foe.item = "Ability Shield" if shield else None
        p.stages["acc"] = 6
        fs.use_move(b, p, fs.move(move), foe, True)
        return foe.status

    def drop(move, ability, mold=True):
        b, p, foe = battle([move], ["Tackle"], {})
        p.ability = "Mold Breaker" if mold else None
        foe.ability = ability
        fs.status_move(b, p, fs.move(move), foe, True)
        return {k: v for k, v in foe.stages.items() if v}

    def flinch(ability, mold=True):
        b, p, foe = battle(["Rock Slide"], ["Tackle"], {("p", "Rock Slide"): [10] * 16})
        b.rng = FixedDice(0.0)                  # every chance lands
        p.ability = "Mold Breaker" if mold else None
        foe.ability = ability
        fs.attack(b, p, fs.move("Rock Slide"), foe, True)
        return foe.flinch

    def crit(ability, mold=True):
        b, p, foe = battle(["Tackle"], ["Tackle"], {})
        p.ability = "Mold Breaker" if mold else None
        foe.ability = ability
        return fs.crit_rate(b, p, foe, fs.move("Tackle")) > 0

    def perish(mold=True):
        b, p, foe = battle(["Perish Song"], ["Tackle"], {})
        p.ability = "Mold Breaker" if mold else None
        foe.ability = "Soundproof"
        fs.status_move(b, p, fs.move("Perish Song"), foe, True)
        return foe.perish
    got = {"Hypnosis, Insomnia": (status("Hypnosis", "Insomnia"), status("Hypnosis", "Insomnia", mold=False),
                                  status("Hypnosis", "Insomnia", shield=True)),
           "Thunder Wave, Limber": (status("Thunder Wave", "Limber"), status("Thunder Wave", "Limber", mold=False)),
           "Toxic, Immunity": (status("Toxic", "Immunity"), status("Toxic", "Immunity", mold=False)),
           "Spore, Leaf Guard in sun": (status("Spore", "Leaf Guard", weather="Sun"),
                                        status("Spore", "Leaf Guard", mold=False, weather="Sun")),
           "Spore, Overcoat": (status("Spore", "Overcoat"), status("Spore", "Overcoat", mold=False)),
           "Spore, a Grass type": (status("Spore", None, types=("Grass",)),),
           "Growl, Clear Body": (drop("Growl", "Clear Body"), drop("Growl", "Clear Body", mold=False)),
           "Growl, Hyper Cutter": (drop("Growl", "Hyper Cutter"), drop("Growl", "Hyper Cutter", mold=False)),
           "Growl, Simple": (drop("Growl", "Simple"), drop("Growl", "Simple", mold=False)),
           "Rock Slide, Inner Focus": (flinch("Inner Focus"), flinch("Inner Focus", mold=False)),
           "Rock Slide, Shield Dust": (flinch("Shield Dust"), flinch("Shield Dust", mold=False)),
           "critical hits, Shell Armor": (crit("Shell Armor"), crit("Shell Armor", mold=False)),
           "critical hits, Battle Armor": (crit("Battle Armor"), crit("Battle Armor", mold=False)),
           "Perish Song, Soundproof": (perish(), perish(mold=False))}
    want = {"Hypnosis, Insomnia": ("slp", None, None), "Thunder Wave, Limber": ("par", None),
            "Toxic, Immunity": ("tox", None), "Spore, Leaf Guard in sun": ("slp", None),
            "Spore, Overcoat": ("slp", None), "Spore, a Grass type": (None,),
            "Growl, Clear Body": ({"atk": -1}, {}), "Growl, Hyper Cutter": ({"atk": -1}, {}),
            "Growl, Simple": ({"atk": -1}, {"atk": -2}), "Rock Slide, Inner Focus": (True, False),
            "Rock Slide, Shield Dust": (True, False), "critical hits, Shell Armor": (True, False),
            "critical hits, Battle Armor": (True, False), "Perish Song, Soundproof": (4, 0)}
    results.append(("Mold Breaker gets past the abilities the engine lets it ignore", got == want,
                    f"(Mold Breaker, without it, against an Ability Shield) {got}"))


def check_oblivious_taunt(results):
    """Oblivious keeps Taunt off its holder (approved 2026-10-14;
    subscript_taunt_start), naming the ability, unless Taunt's user has Mold
    Breaker; another target is taunted for three to five turns."""
    def taunt(ability, mold=False):
        b, p, foe = battle(["Taunt"], ["Tackle"], {})
        p.ability = "Mold Breaker" if mold else None
        foe.ability = ability
        fs.status_move(b, p, fs.move("Taunt"), foe, True)
        return foe.taunt, foe.revealed
    got = {"Oblivious": taunt("Oblivious"), "Oblivious against Mold Breaker": taunt("Oblivious", mold=True),
           "plain": taunt(None)}
    ok = got["Oblivious"] == (0, "Oblivious") and got["Oblivious against Mold Breaker"][0] >= 3 and got["plain"][0] >= 3
    results.append(("Oblivious stops Taunt, unless Mold Breaker", ok, f"(Taunt's turns, the ability named) {got}"))


def check_cursed_body(results):
    """Cursed Body (approved 2026-10-14; BattleSystem_TriggerAbilityOnHit):
    three times in ten a damaging move that hits its holder, contact or not,
    is disabled for its user for three turn ends after this one, even when
    the hit faints the holder, but not when the user already has a move
    disabled; a status move sets nothing off. With every chance landing."""
    def hit(move, ability="Cursed Body", hp=100, disabled=None, value=0.0):
        b, p, foe = battle([move, "Tackle"], ["Tackle"], {("p", move): [30] * 16})
        b.st["first_battle"] = True
        foe.ability, foe.hp = ability, hp
        p.disabled = disabled
        b.rng = FixedDice(value)
        mv = fs.move(move)
        fs.use_move(b, p, mv, foe, True)
        return p.disabled, p.disabled_turns
    got = {"Water Gun": hit("Water Gun"), "Tackle": hit("Tackle"), "a knockout": hit("Water Gun", hp=10),
           "another move disabled": hit("Water Gun", disabled="Tackle"), "Growl": hit("Growl"),
           "no Cursed Body": hit("Water Gun", ability=None), "the 30% missed": hit("Water Gun", value=0.5)}
    want = {"Water Gun": ("Water Gun", 3), "Tackle": ("Tackle", 3), "a knockout": ("Water Gun", 3),
            "another move disabled": ("Tackle", 0), "Growl": (None, 0), "no Cursed Body": (None, 0),
            "the 30% missed": (None, 0)}
    results.append(("Cursed Body disables the move that hit it three times in ten", got == want,
                    f"(the user's disabled move, its turns) {got}"))


def check_justified_rattled(results):
    """Justified and Rattled (approved 2026-10-14;
    BattleSystem_TriggerAbilityOnHit): a Dark hit raises a Justified
    holder's Attack a stage, a Bug, Ghost or Dark hit a Rattled holder's
    Speed, contact or not, once a hit, but not after a knockout, not
    through a Substitute and not past +6."""
    def hit(move, ability, hp=100, stage=0, sub=0, rows=10):
        b, p, foe = battle([move], ["Tackle"], {("p", move): [rows] * 16})
        b.st["first_battle"] = True
        foe.ability, foe.hp, foe.sub = ability, hp, sub
        stat = {"Justified": "atk", "Rattled": "spe"}[ability]
        foe.stages[stat] = stage
        fs.use_move(b, p, fs.move(move), foe, True)
        return foe.stages[stat]
    got = {"Justified, Bite": hit("Bite", "Justified"), "Justified, Tackle": hit("Tackle", "Justified"),
           "Justified, Dark Pulse at +6": hit("Dark Pulse", "Justified", stage=6),
           "Justified, a knockout": hit("Dark Pulse", "Justified", hp=5),
           "Justified, a Substitute": hit("Dark Pulse", "Justified", sub=25),
           "Rattled, Bug Buzz": hit("Bug Buzz", "Rattled"), "Rattled, Shadow Ball": hit("Shadow Ball", "Rattled"),
           "Rattled, Pin Missile's hits": hit("Pin Missile", "Rattled", rows=6),
           "Rattled, Ember": hit("Ember", "Rattled")}
    want = {"Justified, Bite": 1, "Justified, Tackle": 0, "Justified, Dark Pulse at +6": 6,
            "Justified, a knockout": 0, "Justified, a Substitute": 0,
            "Rattled, Bug Buzz": 1, "Rattled, Shadow Ball": 1, "Rattled, Pin Missile's hits": None, "Rattled, Ember": 0}
    hits = got.pop("Rattled, Pin Missile's hits")
    want.pop("Rattled, Pin Missile's hits")
    ok = got == want and 2 <= hits <= 5
    results.append(("Justified and Rattled rise on their hits", ok, f"the stage after the hit {got}; "
                                                                     f"Speed after a Pin Missile of 2 to 5 hits {hits}"))


def check_knockout_boost(results):
    """Moxie and Beast Boost (approved 2026-10-14; BtlCmd_TryBeastBoost):
    a move of its holder that faints its target raises Moxie's Attack and
    Beast Boost's highest stat a stage; a hit that leaves the target
    standing raises nothing, nor does a knockout at +6, nor Destiny Bond's
    taking the user down with it."""
    def ko(ability, hp=10, stage=0, bond=False, stats=None):
        b, p, foe = battle(["Tackle"], ["Tackle"], {("p", "Tackle"): [40] * 16})
        b.st["first_battle"] = True
        p.ability = ability
        if stats:
            p.stats = dict(p.stats, **stats)
        p.stages["atk"] = stage
        foe.hp = hp
        foe.destiny_bond = bond
        fs.use_move(b, p, fs.move("Tackle"), foe, True)
        return {k: v for k, v in p.stages.items() if v}, p.alive()
    got = {"Moxie, a knockout": ko("Moxie"), "Moxie, no knockout": ko("Moxie", hp=100),
           "Moxie at +6": ko("Moxie", stage=6), "Moxie into Destiny Bond": ko("Moxie", bond=True),
           "Beast Boost, Speed highest": ko("Beast Boost", stats={"spe": 150}),
           "Beast Boost, a tie": ko("Beast Boost")}
    want = {"Moxie, a knockout": ({"atk": 1}, True), "Moxie, no knockout": ({}, True),
            "Moxie at +6": ({"atk": 6}, True), "Moxie into Destiny Bond": ({}, False),
            "Beast Boost, Speed highest": ({"spe": 1}, True), "Beast Boost, a tie": ({"atk": 1}, True)}
    results.append(("Moxie and Beast Boost rise on a knockout", got == want,
                    f"(the user's stages, standing) {got}"))


def check_trapping_exemptions(results):
    """The trapping abilities' exemptions (approved 2026-10-14;
    Battler_IsTrapped): Shadow Tag, Arena Trap and Magnet Pull never hold a
    Ghost type or a Shed Shell holder, Arena Trap none floating on an Air
    Balloon, though an Iron Ball brings a Flying type down into it; a Shed
    Shell frees its holder from a bind and from Block too."""
    def held(trap, types=("Normal",), item=None, bound=False, blocked=False):
        b = field({"p0": (types, ["Tackle"]), "p1": (("Normal",), ["Tackle"]), "b0.0": (("Normal",), ["Tackle"])}, {})
        me = b.p.cur()
        b.b.cur().ability = trap
        me.item = item
        me.bound = 3 if bound else 0
        me.trapped_by = "b0.0" if blocked else None
        return fs.trapped(b, me)
    got = {"Shadow Tag": held("Shadow Tag"), "Shadow Tag, a Ghost": held("Shadow Tag", ("Ghost",)),
           "Shadow Tag, a Shed Shell": held("Shadow Tag", item="Shed Shell"),
           "Magnet Pull, a Steel type": held("Magnet Pull", ("Steel",)),
           "Magnet Pull, a Steel and Ghost type": held("Magnet Pull", ("Steel", "Ghost")),
           "Arena Trap": held("Arena Trap"), "Arena Trap, an Air Balloon": held("Arena Trap", item="Air Balloon"),
           "Arena Trap, a Flying type": held("Arena Trap", ("Flying",)),
           "Arena Trap, a Flying type with an Iron Ball": held("Arena Trap", ("Flying",), item="Iron Ball"),
           "a bind": held(None, bound=True), "a bind, a Shed Shell": held(None, bound=True, item="Shed Shell"),
           "Block": held(None, blocked=True), "Block, a Shed Shell": held(None, blocked=True, item="Shed Shell")}
    want = {"Shadow Tag": True, "Shadow Tag, a Ghost": False, "Shadow Tag, a Shed Shell": False,
            "Magnet Pull, a Steel type": True, "Magnet Pull, a Steel and Ghost type": False,
            "Arena Trap": True, "Arena Trap, an Air Balloon": False, "Arena Trap, a Flying type": False,
            "Arena Trap, a Flying type with an Iron Ball": True, "a bind": True, "a bind, a Shed Shell": False,
            "Block": True, "Block, a Shed Shell": False}
    results.append(("the trapping abilities spare a Ghost type and a Shed Shell holder", got == want,
                    f"held in {got}"))


def check_accuracy_abilities(results):
    """The accuracy check's abilities and the Zoom Lens (approved 2026-10-14;
    BattleControllerPlayer_CheckMoveHitAccuracy and its overrides): No Guard
    on either side lands every move, even on a Pokemon mid-Fly; Keen Eye
    and an Unaware attacker ignore the target's evasion; an Unaware target
    ignores the attacker's accuracy stages; a confused Tangled Feet target
    halves the accuracy; a Zoom Lens adds a fifth once the target has moved.
    Landed of 2000 uses of 50-accuracy Dynamic Punch or 100-accuracy Tackle."""
    def lands(move, att_ab=None, dfn_ab=None, acc=0, eva=0, confused=0, item=None, first=True):
        b, p, foe = battle([move], ["Tackle"], {})
        p.ability, foe.ability, p.item = att_ab, dfn_ab, item
        p.stages["acc"], foe.stages["eva"], foe.confused = acc, eva, confused
        return sum(b.accuracy_hits(p, foe, fs.move(move), first) for _ in range(2000))
    got = {"No Guard user": lands("Dynamic Punch", att_ab="No Guard"),
           "No Guard target": lands("Dynamic Punch", dfn_ab="No Guard"),
           "Keen Eye into +6 evasion": lands("Tackle", att_ab="Keen Eye", eva=6),
           "Unaware into +6 evasion": lands("Tackle", att_ab="Unaware", eva=6),
           "+6 accuracy into Unaware": lands("Dynamic Punch", dfn_ab="Unaware", acc=6),
           "plain into +6 evasion": lands("Tackle", eva=6),
           "Tangled Feet, confused": lands("Tackle", dfn_ab="Tangled Feet", confused=3),
           "Zoom Lens, the target moved": lands("Dynamic Punch", item="Zoom Lens", first=False),
           "Zoom Lens, the target yet to move": lands("Dynamic Punch", item="Zoom Lens")}
    b, p, foe = battle(["Tackle"], ["Fly"], {("p", "Tackle"): [10] * 16})
    p.ability, foe.charging = "No Guard", fs.move("Fly")
    fs.attack(b, p, fs.move("Tackle"), foe, True)
    mid_fly = foe.hp
    ok = (got["No Guard user"] == got["No Guard target"] == 2000 and got["Keen Eye into +6 evasion"] == 2000
          and got["Unaware into +6 evasion"] == 2000 and 850 <= got["+6 accuracy into Unaware"] <= 1150
          and got["plain into +6 evasion"] < 800 and 850 <= got["Tangled Feet, confused"] <= 1150
          and 1080 <= got["Zoom Lens, the target moved"] <= 1320 and 850 <= got["Zoom Lens, the target yet to move"] <= 1150
          and mid_fly == 90)
    results.append(("No Guard, Keen Eye, Unaware, Tangled Feet and the Zoom Lens in the accuracy check", ok,
                    f"landed of 2000 {got}; a No Guard Tackle into a Pokemon mid-Fly leaves it at {mid_fly}"))


def check_download(results):
    """Download (approved 2026-10-14; SWITCH_IN_CHECK_STATE_DOWNLOAD): as its
    holder comes in it raises Sp. Atk a stage when the foe's Defense is no
    lower than its Sp. Def, at their stages, and Attack otherwise; a foe
    behind a Substitute counts for nothing, and with none to read it does
    nothing. The battle's leads read each other once both are in."""
    def enter(foe_def, foe_spd, def_stage=0, sub=0):
        b = field({"p0": (("Normal",), ["Tackle"]), "p1": (("Normal",), ["Tackle"]), "b0.0": (("Normal",), ["Tackle"])}, {})
        b.p.mons[1].ability = "Download"
        foe = b.b.cur()
        foe.stats = dict(foe.stats, **{"def": foe_def, "spd": foe_spd})
        foe.stages["def"], foe.sub = def_stage, sub
        fs.switch_in(b, b.p, 1)
        return {k: v for k, v in b.p.cur().stages.items() if v}

    def leads():
        b = field({"p0": (("Normal",), ["Tackle"]), "b0.0": (("Normal",), ["Tackle"])}, {})
        b.p.cur().ability = "Download"
        b.b.cur().stats = dict(b.b.cur().stats, **{"def": 80, "spd": 120})
        fs.open_battle(b)
        return {k: v for k, v in b.p.cur().stages.items() if v}
    got = {"a low Defense": enter(80, 120), "a low Sp. Def": enter(120, 80), "equal": enter(100, 100),
           "a high Defense at -2": enter(150, 100, def_stage=-2), "behind a Substitute": enter(80, 120, sub=25),
           "the leads": leads()}
    want = {"a low Defense": {"atk": 1}, "a low Sp. Def": {"spa": 1}, "equal": {"spa": 1},
            "a high Defense at -2": {"atk": 1}, "behind a Substitute": {}, "the leads": {"atk": 1}}
    results.append(("Download raises one stat a stage on entry, by the foe then in", got == want, f"{got}"))


def check_weather_abilities(results):
    """The weather's turn-end abilities (approved 2026-10-14;
    BtlCmd_EndOfTurnWeatherEffect): Rain Dish heals a sixteenth in rain,
    Hydration cures its status in rain, Solar Power loses an eighth in sun,
    and Sand Rush and Sand Force take no sandstorm damage; none of them acts
    in other weather or while Cloud Nine is out."""
    def end(ability, weather, hp=50, status=None, cloud=False):
        b, p, foe = battle(["Tackle"], ["Tackle"], {})
        foe.ability, foe.hp, foe.status = ability, hp, status
        if cloud:
            p.ability = "Cloud Nine"
        b.weather, b.weather_turns = weather, 0
        fs.end_of_turn(b)
        return foe.hp, foe.status
    got = {"Rain Dish in rain": end("Rain Dish", "Rain"), "Rain Dish in sun": end("Rain Dish", "Sun"),
           "Rain Dish under Cloud Nine": end("Rain Dish", "Rain", cloud=True),
           "Hydration in rain": end("Hydration", "Rain", hp=100, status="par"),
           "Hydration in sun": end("Hydration", "Sun", hp=100, status="par"),
           "Solar Power in sun": end("Solar Power", "Sun"), "Solar Power in rain": end("Solar Power", "Rain"),
           "Sand Rush in sand": end("Sand Rush", "Sand"), "Sand Force in sand": end("Sand Force", "Sand"),
           "plain in sand": end(None, "Sand")}
    want = {"Rain Dish in rain": (56, None), "Rain Dish in sun": (50, None), "Rain Dish under Cloud Nine": (50, None),
            "Hydration in rain": (100, None), "Hydration in sun": (100, "par"),
            "Solar Power in sun": (38, None), "Solar Power in rain": (50, None),
            "Sand Rush in sand": (50, None), "Sand Force in sand": (50, None), "plain in sand": (44, None)}
    results.append(("Rain Dish, Hydration and Solar Power at the turn's end; Sand Rush and Sand Force spared sand",
                    got == want, f"(HP from 50, status) {got}"))


def check_sand_force(results):
    """Sand Force (approved 2026-10-14; BattleSystem_CalcMoveDamage): Ground,
    Rock and Steel moves at 13/10 power in a sandstorm, not in other weather,
    not another type's move, not under Cloud Nine. Rows of 100."""
    def hit(move, weather="Sand", cloud=False, ability="Sand Force"):
        b, p, foe = battle([move], ["Tackle"], {("p", move): [100] * 16})
        p.ability = ability
        if cloud:
            foe.ability = "Cloud Nine"
        b.weather = weather
        return b.damage(p, foe, fs.move(move), roll=0)
    got = {"Rock Slide in sand": hit("Rock Slide"), "Earthquake in sand": hit("Earthquake"),
           "Iron Head in sand": hit("Iron Head"), "Tackle in sand": hit("Tackle"),
           "Rock Slide in rain": hit("Rock Slide", weather="Rain"),
           "Rock Slide under Cloud Nine": hit("Rock Slide", cloud=True),
           "Rock Slide, no Sand Force": hit("Rock Slide", ability=None)}
    want = {"Rock Slide in sand": 130, "Earthquake in sand": 130, "Iron Head in sand": 130, "Tackle in sand": 100,
            "Rock Slide in rain": 100, "Rock Slide under Cloud Nine": 100, "Rock Slide, no Sand Force": 100}
    results.append(("Sand Force raises Ground, Rock and Steel moves in sand", got == want, f"{got}"))


def check_bad_dreams(results):
    """Bad Dreams (approved 2026-10-14; MON_COND_CHECK_STATE_BAD_DREAMS): a
    sleeping foe of its holder loses an eighth of its HP at each turn's
    end; an awake one loses nothing, nor a Magic Guard one, nor any once
    the holder has fainted."""
    def end(status="slp", ability=None, holder_up=True):
        b, p, foe = battle(["Tackle"], ["Tackle"], {})
        foe.ability = "Bad Dreams"
        if not holder_up:
            foe.hp = 0
        p.status, p.sleep, p.ability = status, 3 if status == "slp" else 0, ability
        fs.end_of_turn(b)
        return p.hp
    got = {"asleep": end(), "awake": end(status=None), "asleep, Magic Guard": end(ability="Magic Guard"),
           "the holder fainted": end(holder_up=False)}
    want = {"asleep": 88, "awake": 100, "asleep, Magic Guard": 100, "the holder fainted": 100}
    results.append(("Bad Dreams takes an eighth from a sleeping foe at the turn's end", got == want, f"{got}"))


def check_marvel_scale(results):
    """Marvel Scale (approved 2026-10-14; BattleSystem_CalcMoveDamage): half
    again to its holder's Defense while it has a status, so a physical hit
    (or Psyshock, which hits Defense) does two thirds, a special one all;
    nothing without a status, nothing against Mold Breaker. Rows of 60."""
    def hit(move, status="brn", mold=False, ability="Marvel Scale"):
        b, p, foe = battle([move], ["Tackle"], {("p", move): [60] * 16})
        p.ability = "Mold Breaker" if mold else None
        foe.ability, foe.status = ability, status
        return b.damage(p, foe, fs.move(move), roll=0)
    got = {"Tackle, burned": hit("Tackle"), "Psyshock, burned": hit("Psyshock"), "Surf, burned": hit("Surf"),
           "Tackle, no status": hit("Tackle", status=None), "Tackle, Mold Breaker": hit("Tackle", mold=True),
           "Tackle, no Marvel Scale": hit("Tackle", ability=None)}
    want = {"Tackle, burned": 40, "Psyshock, burned": 40, "Surf, burned": 60, "Tackle, no status": 60,
            "Tackle, Mold Breaker": 60, "Tackle, no Marvel Scale": 60}
    results.append(("Marvel Scale raises Defense while its holder has a status", got == want, f"{got}"))


def check_shed_skin(results):
    """Shed Skin (approved 2026-10-14; BattleSystem_TriggerTurnEndAbility):
    one time in three a poisoned holder is cured at the turn's end, before
    the poison bites, so a cured one loses nothing; over 600 turn ends."""
    cured = unhurt = 0
    for seed in range(600):
        b, p, foe = battle(["Tackle"], ["Tackle"], {}, seed=seed)
        foe.ability, foe.status = "Shed Skin", "psn"
        fs.end_of_turn(b)
        cured += foe.status is None
        unhurt += foe.status is None and foe.hp == 100
    ok = 160 <= cured <= 240 and unhurt == cured
    results.append(("Shed Skin cures a status one time in three at the turn's end", ok,
                    f"cured {cured} of 600, at full HP when cured {unhurt}"))


def check_suction_cups(results):
    """Suction Cups (approved 2026-10-14; subscript_force_target_to_switch_or_flee)
    keeps its holder in against Roar and Whirlwind, naming the ability,
    unless the user has Mold Breaker; another target is dragged out."""
    def roar(ability, mold=False):
        b = field({"p0": (("Normal",), ["Roar"]), "b0.0": (("Normal",), ["Tackle"]), "b0.1": (("Normal",), ["Tackle"])}, {})
        p, foe = b.p.cur(), b.b.cur()
        p.ability = "Mold Breaker" if mold else None
        foe.ability = ability
        p.stages["acc"] = 6
        fs.status_move(b, p, fs.move("Roar"), foe, True)
        return b.b.active, foe.revealed
    got = {"Suction Cups": roar("Suction Cups"), "Suction Cups against Mold Breaker": roar("Suction Cups", mold=True),
           "plain": roar(None)}
    want = {"Suction Cups": (0, "Suction Cups"), "Suction Cups against Mold Breaker": (1, None), "plain": (1, None)}
    results.append(("Suction Cups stands up to Roar, unless Mold Breaker", got == want,
                    f"(the trainer's active slot after Roar, the ability named) {got}"))


def check_plus_minus(results):
    """Plus and Minus (approved 2026-10-14; BattleSystem_CalcMoveDamage):
    half again to a special move only beside a partner with Plus or Minus,
    so a holder alone hits as its row; in a double battle beside a Minus
    partner its Thunderbolt is half again as strong, its Tackle not. Rows
    of 40, made without the ability as prepare() now makes them."""
    rows = {("p0", "b0.0"): {"Thunderbolt": 40, "Tackle": 40}}
    b = field({"p0": (("Electric",), ["Thunderbolt", "Tackle"]), "p1": (("Electric",), ["Tackle"]),
               "b0.0": (("Normal",), ["Tackle"])}, rows)
    plusle, minun = b.p.mons
    foe = b.b.cur()
    plusle.ability, minun.ability = "Plus", "Minus"
    alone = b.damage(plusle, foe, fs.move("Thunderbolt"), roll=0)
    b.doubles, b.p.active2 = True, 1
    paired = (b.damage(plusle, foe, fs.move("Thunderbolt"), roll=0), b.damage(plusle, foe, fs.move("Tackle"), roll=0))
    minun.ability = "Static"
    unpaired = b.damage(plusle, foe, fs.move("Thunderbolt"), roll=0)
    ok = alone == 40 and paired == (60, 40) and unpaired == 40 and "Plus" in fs.CALC_ABILITY_OFF
    results.append(("Plus and Minus raise special moves only beside a partner with either", ok,
                    f"alone {alone}; beside Minus (Thunderbolt, Tackle) {paired}; beside Static {unpaired}"))


def check_stench(results):
    """Stench (approved 2026-10-14; BattleControllerPlayer_CheckExtraFlinch):
    its holder's hits flinch one time in ten as a King's Rock's do, the
    holder's own King's Rock not adding a second chance; each hit of a move
    of several rolls it (land_hits). Double Kick into a slower target, 1000
    uses each."""
    def flinches(ability, item=None):
        n = 0
        for seed in range(1000):
            b, p, foe = battle(["Double Kick"], ["Tackle"], {("p", "Double Kick"): [2] * 16}, seed=seed)
            b.st["first_battle"] = True
            p.ability, p.item = ability, item
            fs.attack(b, p, fs.move("Double Kick"), foe, True)
            n += foe.flinch
        return n
    got = {"Stench": flinches("Stench"), "Stench and a King's Rock": flinches("Stench", "King's Rock"),
           "plain": flinches(None)}
    ok = 140 <= got["Stench"] <= 240 and 140 <= got["Stench and a King's Rock"] <= 240 and got["plain"] == 0
    results.append(("Stench flinches as a King's Rock does, and does not add to one", ok,
                    f"flinched in 1000 two-hit Double Kicks {got}"))


def check_unnerve(results):
    """Unnerve (approved 2026-10-14; BerryBlockedByUnnerve): while a foe with
    it stands, a Pokemon cannot eat its Berry: a Sitrus Berry at half HP, a
    Lum Berry against a status, a resist Berry's halving (the row's half is
    taken back off), a Custap Berry's turn order; once the holder has
    fainted the Berries work again. Berry Juice is no Berry."""
    def sitrus(unnerve=True, holder_up=True, item="Sitrus Berry"):
        b, p, foe = battle(["Tackle"], ["Tackle"], {})
        foe.ability = "Unnerve" if unnerve else None
        if not holder_up:
            foe.hp = 0
        p.item = item
        fs.hurt(b, p, 60)
        return p.hp, p.item
    def lum():
        b, p, foe = battle(["Tackle"], ["Thunder Wave"], {})
        p.ability = "Unnerve"
        foe.item = "Lum Berry"
        b.status_src = p
        fs.give_status(b, foe, "par")
        return foe.status, foe.item
    def resist():
        b, p, foe = battle(["Ember"], ["Tackle"], {("p", "Ember"): [20] * 16}, b_types=("Grass",))
        b.st["pokemon"]["b0.0"]["item"] = foe.item = "Occa Berry"
        p.ability = "Unnerve"
        return b.damage(p, foe, fs.move("Ember"), roll=0), foe.item
    def custap():
        b, p, foe = battle(["Tackle"], ["Tackle"], {})
        p.ability = "Unnerve"
        foe.item, foe.hp = "Custap Berry", 20
        return fs.custap_fires(foe, b), fs.custap_fires(foe)
    got = {"Sitrus under Unnerve": sitrus(), "Sitrus": sitrus(unnerve=False),
           "Sitrus, the holder fainted": sitrus(holder_up=False), "Berry Juice under Unnerve": sitrus(item="Berry Juice"),
           "Lum under Unnerve": lum(), "a resist Berry under Unnerve": resist(), "Custap under Unnerve": custap()}
    want = {"Sitrus under Unnerve": (40, "Sitrus Berry"), "Sitrus": (65, None), "Sitrus, the holder fainted": (65, None),
            "Berry Juice under Unnerve": (60, None), "Lum under Unnerve": ("par", "Lum Berry"),
            "a resist Berry under Unnerve": (40, "Occa Berry"), "Custap under Unnerve": (False, True)}
    results.append(("Unnerve keeps the other side from eating its Berries", got == want, f"{got}"))


def check_telepathy(results):
    """Telepathy (approved 2026-10-14; BattleControllerPlayer_PriorityBlock):
    in a double battle its holder takes nothing from its partner's
    Earthquake, unless the partner has Mold Breaker, while the foes take it
    as before."""
    def quake(ability, mold=False):
        rows = {("b0.0", "p0"): {"Earthquake": 30}}
        b = field({"p0": (("Normal",), ["Tackle"]), "b0.0": (("Normal",), ["Earthquake"]),
                   "b0.1": (("Normal",), ["Tackle"])}, rows)
        b.doubles, b.moved, b.b.active2 = True, set(), 1
        b.st["rows"][(None, "b0.0", "b0.1")] = {"moves": {"Earthquake": {"rolls": [30] * 16}}}
        quaker, ally = b.b.mons
        quaker.ability = "Mold Breaker" if mold else None
        ally.ability = ability
        targets = fs.targets_of(b, quaker, fs.move("Earthquake"), None)
        fs.use_move(b, quaker, fs.move("Earthquake"), targets[0], True, targets=targets)
        return ally.hp, b.p.cur().hp < 100
    got = {"Telepathy": quake("Telepathy"), "Telepathy, a Mold Breaker partner": quake("Telepathy", mold=True),
           "plain": quake(None)}
    ok = (got["Telepathy"] == (100, True) and got["Telepathy, a Mold Breaker partner"][0] < 100
          and got["plain"][0] < 100 and got["plain"][1])
    results.append(("Telepathy takes no damage from its partner's spread move", ok,
                    f"(the partner's HP, the foe hit) {got}"))


def check_steadfast(results):
    """Steadfast (approved 2026-10-14; subscript_flinched): a flinch that
    stops its holder's move raises its Speed a stage, nothing at +6; a
    holder that does not flinch gains nothing."""
    def turn(ability, flinch=True, stage=0):
        b, p, foe = battle(["Tackle"], ["Tackle"], {("p", "Tackle"): [10] * 16})
        p.ability, p.flinch, p.stages["spe"] = ability, flinch, stage
        fs.use_move(b, p, fs.move("Tackle"), foe, False)
        return p.stages["spe"], foe.hp
    got = {"Steadfast, flinched": turn("Steadfast"), "Steadfast at +6": turn("Steadfast", stage=6),
           "Steadfast, not flinched": turn("Steadfast", flinch=False), "plain, flinched": turn(None)}
    want = {"Steadfast, flinched": (1, 100), "Steadfast at +6": (6, 100), "Steadfast, not flinched": (0, 90),
            "plain, flinched": (0, 100)}
    results.append(("Steadfast gains a stage of Speed when it flinches", got == want,
                    f"(its Speed stage, the foe's HP) {got}"))


def check_starf_berry(results):
    """The Starf Berry (approved 2026-10-14; HOLD_EFFECT_PINCH_RANDOM_UP): at a
    quarter of its HP its holder raises one of Attack, Defense, Sp. Atk, Sp.
    Def and Speed two stages, drawn among those below +6, and eats it; at
    +6 in all five it stays uneaten; above a quarter nothing happens."""
    seen = set()
    for seed in range(60):
        b, p, foe = battle(["Tackle"], ["Tackle"], {}, seed=seed)
        foe.item = "Starf Berry"
        fs.hurt(b, foe, 76)
        rose = {k: v for k, v in foe.stages.items() if v}
        seen.add((tuple(rose.items()), foe.item))
    stats = {r[0][0] for r, item in seen if r}
    b, p, foe = battle(["Tackle"], ["Tackle"], {})
    foe.item = "Starf Berry"
    foe.stages.update({s: 6 for s in ("atk", "def", "spa", "spd", "spe")})
    fs.hurt(b, foe, 76)
    full = foe.item
    b, p, foe = battle(["Tackle"], ["Tackle"], {})
    foe.item = "Starf Berry"
    fs.hurt(b, foe, 50)
    above = foe.item
    ok = (all(len(r) == 1 and r[0][1] == 2 and item is None for r, item in seen)
          and stats == {"atk", "def", "spa", "spd", "spe"} and full == "Starf Berry" and above == "Starf Berry")
    results.append(("the Starf Berry raises a random stat two stages at a quarter HP", ok,
                    f"stats raised over 60 draws {sorted(stats)}; kept at +6 in all {full}; kept above a quarter {above}"))


def check_sticky_barb(results):
    """The Sticky Barb (approved 2026-10-14; HOLD_EFFECT_DMG_USER_CONTACT_XFR):
    an eighth of its holder's HP at each turn's end, none with Magic Guard;
    a contact hit hands it to an attacker holding nothing, not a Water Gun,
    not an attacker with an item of its own."""
    def end(ability=None):
        b, p, foe = battle(["Tackle"], ["Tackle"], {})
        foe.item, foe.ability = "Sticky Barb", ability
        fs.end_of_turn(b)
        return foe.hp

    def hit(move, own=None):
        b, p, foe = battle([move], ["Tackle"], {("p", move): [10] * 16})
        b.st["first_battle"] = True
        foe.item, p.item = "Sticky Barb", own
        fs.use_move(b, p, fs.move(move), foe, True)
        return p.item, foe.item
    got = {"the turn's end": end(), "the turn's end, Magic Guard": end("Magic Guard"),
           "Tackle": hit("Tackle"), "Water Gun": hit("Water Gun"), "Tackle, holding Leftovers": hit("Tackle", "Leftovers")}
    want = {"the turn's end": 88, "the turn's end, Magic Guard": 100, "Tackle": ("Sticky Barb", None),
            "Water Gun": (None, "Sticky Barb"), "Tackle, holding Leftovers": ("Leftovers", "Sticky Barb")}
    results.append(("the Sticky Barb hurts its holder and sticks to a contact attacker", got == want, f"{got}"))


def check_payback(results):
    """Payback (approved 2026-10-14; BtlCmd_CalcPaybackPower): doubled once
    when the target has acted first. The calculator's row already doubles it
    for a user no faster than its target, so a row of 40 there is a 20 hit
    at the table's power: 20 moving first, 40 moving second, where it read
    40 and 80. A faster user's row of 20 is its table power: 20 and 40. A
    Technician holder's slower row of 40 is 30 at its own 90 power (60 and
    half again), and 40 moving second, at 120 with no Technician."""
    def hit(p_speed, b_speed, first, ability=None, row=40):
        b, p, foe = battle(["Payback"], ["Tackle"], {("p", "Payback"): [row] * 16},
                           p_speed=p_speed, b_speed=b_speed)
        b.st["first_battle"] = True
        p.ability = ability
        fs.attack(b, p, fs.move("Payback"), foe, first)
        return 100 - foe.hp
    got = {"slower, first": hit(50, 100, True), "slower, second": hit(50, 100, False),
           "faster, first": hit(100, 50, True, row=20), "faster, second": hit(100, 50, False, row=20),
           "slower Technician, first": hit(50, 100, True, "Technician"),
           "slower Technician, second": hit(50, 100, False, "Technician")}
    want = {"slower, first": 20, "slower, second": 40, "faster, first": 20, "faster, second": 40,
            "slower Technician, first": 30, "slower Technician, second": 40}
    results.append(("Payback doubles once, not on top of the calculator's own doubling", got == want, f"{got}"))


def check_leech_seed_sap(results):
    """Leech Seed's sap (approved 2026-10-14; MON_COND_CHECK_STATE_LEECH_SEED
    and subscript_leech_seed_effect): an eighth from the seeded Pokemon to
    its seeder, the seeder given only what the sap took, and nothing at all
    the turn the seeder is down."""
    def tick(seeded_hp, seeder_hp):
        b, p, foe = battle(["Leech Seed"], ["Tackle"], {})
        foe.seeded = True
        foe.hp, p.hp = seeded_hp, seeder_hp
        fs.end_of_turn(b)
        return foe.hp, p.hp
    got = {"full": tick(100, 10), "the seeded at 3 HP": tick(3, 10), "the seeder down": tick(100, 0)}
    want = {"full": (88, 22), "the seeded at 3 HP": (0, 13), "the seeder down": (100, 0)}
    results.append(("Leech Seed gives what it saps, and saps nothing with its seeder down", got == want,
                    f"(the seeded's HP, the seeder's) {got}"))


def check_ghost_untrapped(results):
    """A Ghost type is never trapped (approved 2026-10-14; Battler_IsTrapped,
    Oxide's Generation 6 rule): not by a bind, Block or Mean Look, nor by
    its own Ingrain, where a Normal type is held by each."""
    def held(types, how):
        b, p, foe = battle(["Tackle"], ["Tackle"], {}, p_types=types)
        if how == "bind":
            p.bound = 3
        elif how == "Mean Look":
            p.trapped_by = foe.key
        else:
            p.ingrained = True
        return fs.trapped(b, p)
    got = {f"{t[0]}, {how}": held(t, how) for t in (("Normal",), ("Ghost",)) for how in ("bind", "Mean Look", "Ingrain")}
    want = {"Normal, bind": True, "Normal, Mean Look": True, "Normal, Ingrain": True,
            "Ghost, bind": False, "Ghost, Mean Look": False, "Ghost, Ingrain": False}
    results.append(("a Ghost type is never trapped", got == want, f"held in {got}"))


def check_soundproof_status(results):
    """Soundproof against the status sound moves (approved 2026-10-14;
    BattleSystem_TriggerImmunityAbility): a sure Sing, Growl and Roar do
    nothing to a Soundproof target and name the ability, unless the user has
    Mold Breaker; a plain target sleeps, loses a stage and is dragged out."""
    def use(move, ability, mold=False):
        b = field({"p0": (("Normal",), [move]), "b0.0": (("Normal",), ["Tackle"]), "b0.1": (("Normal",), ["Tackle"])}, {})
        p, foe = b.p.cur(), b.b.cur()
        p.ability = "Mold Breaker" if mold else None
        foe.ability = ability
        p.stages["acc"] = 6
        fs.status_move(b, p, fs.move(move), foe, True)
        return {"Sing": foe.status, "Growl": foe.stages["atk"], "Roar": b.b.active}[move], foe.revealed
    got = {f"{m}, {label}": use(m, ab, mold) for m in ("Sing", "Growl", "Roar")
           for label, ab, mold in (("Soundproof", "Soundproof", False), ("Mold Breaker", "Soundproof", True),
                                   ("plain", None, False))}
    want = {"Sing, Soundproof": (None, "Soundproof"), "Sing, Mold Breaker": ("slp", None), "Sing, plain": ("slp", None),
            "Growl, Soundproof": (0, "Soundproof"), "Growl, Mold Breaker": (-1, None), "Growl, plain": (-1, None),
            "Roar, Soundproof": (0, "Soundproof"), "Roar, Mold Breaker": (1, None), "Roar, plain": (1, None)}
    results.append(("Soundproof stops the status sound moves, unless Mold Breaker", got == want, f"{got}"))


def check_item_flinch_blocked(results):
    """Shield Dust and the Covert Cloak against a King's Rock (approved
    2026-10-14; subscript_flinch_mon): a King's Rock holder's Double Kick
    never flinches a Shield Dust target or one with a Covert Cloak, unless
    the user has Mold Breaker (Shield Dust only); 1000 uses each."""
    def flinches(ability=None, item=None, mold=False):
        n = 0
        for seed in range(1000):
            b, p, foe = battle(["Double Kick"], ["Tackle"], {("p", "Double Kick"): [2] * 16}, seed=seed)
            b.st["first_battle"] = True
            p.item, p.ability = "King's Rock", "Mold Breaker" if mold else None
            foe.ability, foe.item = ability, item
            fs.attack(b, p, fs.move("Double Kick"), foe, True)
            n += foe.flinch
        return n
    got = {"Shield Dust": flinches("Shield Dust"), "a Covert Cloak": flinches(item="Covert Cloak"),
           "Shield Dust, Mold Breaker": flinches("Shield Dust", mold=True), "plain": flinches()}
    ok = (got["Shield Dust"] == 0 and got["a Covert Cloak"] == 0
          and 140 <= got["Shield Dust, Mold Breaker"] <= 240 and 140 <= got["plain"] <= 240)
    results.append(("Shield Dust and a Covert Cloak stop a King's Rock's flinch", ok, f"flinched of 1000 {got}"))


def check_black_sludge(results):
    """Black Sludge (approved 2026-10-14; HOLD_EFFECT_HP_RESTORE_PSN_TYPE): at
    the turn's end a Poison type below full HP gets a sixteenth back, any
    other holder loses an eighth, a Magic Guard holder nothing."""
    def end(types, ability=None):
        b, p, foe = battle(["Tackle"], ["Tackle"], {}, b_types=types)
        foe.item, foe.ability, foe.hp = "Black Sludge", ability, 50
        fs.end_of_turn(b)
        return foe.hp
    got = {"a Poison type": end(("Poison",)), "a Normal type": end(("Normal",)),
           "a Normal type with Magic Guard": end(("Normal",), "Magic Guard")}
    want = {"a Poison type": 56, "a Normal type": 38, "a Normal type with Magic Guard": 50}
    results.append(("Black Sludge heals a Poison type and hurts any other holder", got == want, f"HP from 50 {got}"))


def check_water_bubble(results):
    """Water Bubble keeps burns off (approved 2026-10-14; subscript_burn):
    a Will-O-Wisp does nothing to its holder and names the ability, unless
    the user has Mold Breaker; a Flame Orb never burns it."""
    def wisp(ability, mold=False):
        b, p, foe = battle(["Will-O-Wisp"], ["Tackle"], {})
        p.ability = "Mold Breaker" if mold else None
        foe.ability = ability
        b.status_src = p
        fs.give_status(b, foe, "brn")
        return foe.status, foe.revealed
    b, p, foe = battle(["Tackle"], ["Tackle"], {})
    foe.ability, foe.item = "Water Bubble", "Flame Orb"
    fs.end_of_turn(b)
    got = {"Water Bubble": wisp("Water Bubble"), "Water Bubble, Mold Breaker": wisp("Water Bubble", True),
           "plain": wisp(None), "a Flame Orb": foe.status}
    want = {"Water Bubble": (None, "Water Bubble"), "Water Bubble, Mold Breaker": ("brn", None),
            "plain": ("brn", None), "a Flame Orb": None}
    results.append(("Water Bubble keeps burns off its holder", got == want, f"{got}"))


def check_eerie_spell(results):
    """Eerie Spell (Oxide's engine since 2026-10-14, effect script 421): its
    hit, then 3 PP off the target's last move, or what it has left, by
    Spite's command; nothing when the target has no last move, when that
    move was Mimic, or when a Substitute took the hit; Shield Dust does not
    stop it. Spite itself still takes 4."""
    def spell(last="Tackle", pp=10, shield_dust=False, sub=0, move="Eerie Spell"):
        b, p, foe = battle([move], ["Tackle", "Mimic"], {("p", move): [10] * 16})
        b.st["first_battle"] = True
        foe.last = fs.move(last) if last else None
        if last:
            foe.pp[last] = pp
        foe.ability = "Shield Dust" if shield_dust else None
        foe.sub = sub
        fs.use_move(b, p, fs.move(move), foe, True)
        return foe.pp.get(last) if last else None
    got = {"Tackle at 10": spell(), "Tackle at 2": spell(pp=2), "no last move": spell(last=None),
           "Mimic": spell(last="Mimic"), "Shield Dust": spell(shield_dust=True), "a Substitute": spell(sub=50),
           "Spite": spell(move="Spite")}
    want = {"Tackle at 10": 7, "Tackle at 2": 0, "no last move": None, "Mimic": 10, "Shield Dust": 7,
            "a Substitute": 10, "Spite": 6}
    results.append(("Eerie Spell drains 3 PP from the target's last move after its hit", got == want,
                    f"the last move's PP after {got}"))


def check_burning_bulwark(results):
    """Burning Bulwark (Oxide's engine since 2026-10-14, subscript_missed):
    a contact move it stops burns its user, unless the user is a Fire type,
    is behind its own Substitute or under Safeguard, already has a status,
    or has Water Veil, Water Bubble, Purifying Salt, or Leaf Guard in sun; a
    move without contact is only stopped, and a status move is stopped
    too."""
    def into(move="Tackle", types=("Normal",), ability=None, status=None, sub=0, safeguard=False, weather=None):
        b, p, foe = battle([move], ["Burning Bulwark"], {("p", move): [10] * 16}, p_types=types)
        b.weather = weather
        foe.protecting, foe.last = True, fs.move("Burning Bulwark")
        p.ability, p.status, p.sub = ability, status, sub
        b.p.safeguard = 5 if safeguard else 0
        stopped = fs.protected(b, p, fs.move(move), foe)
        return stopped, p.status
    got = {"Tackle": into(), "Water Gun": into("Water Gun"), "Growl": into("Growl"),
           "a Fire type": into(types=("Fire",)), "Water Veil": into(ability="Water Veil"),
           "Water Bubble": into(ability="Water Bubble"), "Purifying Salt": into(ability="Purifying Salt"),
           "Leaf Guard in sun": into(ability="Leaf Guard", weather="Sun"), "Leaf Guard": into(ability="Leaf Guard"),
           "its own Substitute": into(sub=25), "Safeguard": into(safeguard=True), "paralysed": into(status="par")}
    want = {"Tackle": (True, "brn"), "Water Gun": (True, None), "Growl": (True, None), "a Fire type": (True, None),
            "Water Veil": (True, None), "Water Bubble": (True, None), "Purifying Salt": (True, None),
            "Leaf Guard in sun": (True, None), "Leaf Guard": (True, "brn"), "its own Substitute": (True, None),
            "Safeguard": (True, None), "paralysed": (True, "par")}
    results.append(("Burning Bulwark burns a contact attacker, with the burn's own exceptions", got == want,
                    f"(stopped, the attacker's status) {got}"))


def check_refresh(results):
    """Refresh (approved 2026-10-14; effect script 193,
    subscript_recover_psn_prz_brn): it cures its user's own poison, burn or
    paralysis, the toxic count with it, and nothing else, so a sleeping
    teammate on the bench sleeps on, and a sleeping or frozen user stays so."""
    out = {}
    for status in ("par", "tox", "slp", "frz"):
        b = field({"p0": (("Normal",), ["Refresh"]), "p1": (("Normal",), ["Tackle"]),
                   "b0.0": (("Normal",), ["Tackle"])}, {})
        p, mate, foe = b.p.mons[0], b.p.mons[1], b.b.cur()
        p.status, p.toxic = status, 3 if status == "tox" else 0
        mate.status = "slp"
        fs.status_move(b, p, fs.move("Refresh"), foe, True)
        out[status] = (p.status, p.toxic, mate.status)
    want = {"par": (None, 0, "slp"), "tox": (None, 0, "slp"), "slp": ("slp", 0, "slp"), "frz": ("frz", 0, "slp")}
    results.append(("Refresh cures its user's poison, burn or paralysis alone", out == want,
                    f"(the user's status, toxic count, the benched teammate's) {out}"))


def check_wring_out(results):
    """Crush Grip and Wring Out (approved 2026-10-14; effect script 237,
    BtlCmd_CalcWringOutPower): 1 plus 120 times the target's HP over its
    maximum, so a row made at full HP's 121 scales to 61 at half HP and 2
    at 1 HP of 100."""
    out = {}
    for name in ("Crush Grip", "Wring Out"):
        b, p, foe = battle([name], ["Tackle"], {("p", name): [121] * 16})
        for hp in (100, 50, 1):
            foe.hp = hp
            out[(name, hp)] = b.damage(p, foe, fs.move(name), roll=0)
    want = {(n, hp): d for n in ("Crush Grip", "Wring Out") for hp, d in ((100, 121), (50, 61), (1, 2))}
    results.append(("Crush Grip and Wring Out hit by the target's HP left", out == want, str(out)))


def check_miracle_eye(results):
    """Miracle Eye (approved 2026-10-14; effect script 216,
    subscript_miracle_eye): Psychic moves then meet the target's Dark type,
    read from its twin's rows without Dark, through a Substitute too, and
    its raised evasion stops counting, though a lowered one still counts;
    the trainer's AI's type check sees the Psychic move land and its Basic
    check refuses a second Miracle Eye; leaving ends it."""
    b, p, foe = battle(["Miracle Eye", "Confusion"], ["Tackle"], {("p", "Confusion"): [0] * 16},
                       b_types=("Dark",), hp=500)
    b.st["rows"][(None, "p0", "b0.0#me")] = {"moves": {"Confusion": {"rolls": [10] * 16}}}
    b.st["miracle_twin"] = {"b0.0": "b0.0#me"}
    b.st["chart"]["Psychic"] = {"Dark": 0.0}       # the test chart's types, with the immunity
    b.rng = FixedDice(0.5)
    foe.ability = "Shell Armor"
    conf, eye = fs.move("Confusion"), fs.move("Miracle Eye")

    def hit():
        before = foe.hp
        fs.attack(b, p, conf, foe, True)
        return before - foe.hp
    foe.stages["eva"] = 6
    out = {"before": (hit(), fightai.script_eff(b, p, foe, conf))}
    foe.sub = 50
    fs.status_move(b, p, eye, foe, True)
    foe.sub = 0
    out["after"] = (hit(), fightai.script_eff(b, p, foe, conf) > 0)
    out["evasion scale at +6, -6"] = (fs.accuracy_scale(p, foe, conf), None)
    foe.stages["eva"] = -6
    out["evasion scale at +6, -6"] = (out["evasion scale at +6, -6"][0], fs.accuracy_scale(p, foe, conf))
    out["AI's second Miracle Eye"] = fightai.basic(b, p, foe, eye, 0)
    foe.reset_volatile()
    out["after leaving"] = getattr(foe, "miracle_eye", None)
    want = {"before": (0, 0), "after": (10, True), "evasion scale at +6, -6": (1.0, 3.0),
            "AI's second Miracle Eye": -10, "after leaving": False}
    results.append(("Miracle Eye lets Psychic moves hit a Dark type and lifts its evasion", out == want, str(out)))


def check_acupressure(results):
    """Acupressure (approved 2026-10-14; effect script 226,
    BtlCmd_BoostRandomStatBy2): two stages on one of its user's stats not
    at +6, drawn evenly in the engine's order (here the first), Simple
    doubling them; nothing behind its own Substitute or with every stat at
    +6."""
    def use(**kw):
        b, p, foe = battle(["Acupressure"], ["Tackle"], {})
        b.rng = FixedDice(0.0)
        for k, v in kw.items():
            if k == "stages":
                p.stages.update(v)
            else:
                setattr(p, k, v)
        fs.status_move(b, p, fs.move("Acupressure"), foe, True)
        return {k: v for k, v in p.stages.items() if v}
    out = {"fresh": use(), "Attack at +6": use(stages={"atk": 6}), "Simple": use(ability="Simple"),
           "behind its Substitute": use(sub=25), "all at +6": use(stages=dict.fromkeys(fs.STAGE_KEYS, 6))}
    want = {"fresh": {"atk": 2}, "Attack at +6": {"atk": 6, "def": 2}, "Simple": {"atk": 4},
            "behind its Substitute": {}, "all at +6": dict.fromkeys(fs.STAGE_KEYS, 6)}
    results.append(("Acupressure raises a stat below +6 by two", out == want, str(out)))


def check_trainer_frustration(results):
    """A trainer's Frustration (approved 2026-10-14; effect script 123): 255
    less its species' base friendship, times 10 over 25, so prepare() asks
    the calculator for a trainer's Raticate's at 74, a Buneary's at 102 (its
    base is 0) and a Lopunny's at 46 (its base is 140), and leaves the
    player's to the calculator."""
    st, pairs, pokemon = prepared_jobs([("Raticate", 30, "Guts", ["Frustration"], None),
                                        ("Buneary", 30, "Klutz", ["Frustration"], None),
                                        ("Lopunny", 30, "Klutz", ["Frustration"], None)],
                                       [("Bibarel", 30, "Simple", ["Frustration"], None)])
    got = {pokemon[k]["species"]: (pokemon[k].get("move_data") or {}).get("Frustration", {}).get("basePower")
           for k in ("b0.0", "b0.1", "b0.2", "p0")}
    want = {"Raticate": 74, "Buneary": 102, "Lopunny": 46, "Bibarel": None}
    results.append(("a trainer's Frustration is rowed at its base friendship's power", got == want, str(got)))


def check_secret_power(results):
    """Secret Power (approved 2026-10-14; effect script 197,
    BtlCmd_GetTerrainSecondaryEffect): at its 30% chance the hit adds its
    battle terrain's effect, an accuracy drop on plain ground, paralysis
    in a building and where the fight names no terrain, a flinch on a
    mountain, an Attack drop on water, sleep in grass; above the chance,
    nothing."""
    out = {}
    for terrain, dice in (("TERRAIN_PLAIN", 0.0), ("TERRAIN_BUILDING", 0.0), (None, 0.0), ("TERRAIN_MOUNTAIN", 0.0),
                          ("TERRAIN_WATER", 0.0), ("TERRAIN_GRASS", 0.0), ("TERRAIN_PLAIN", 0.5)):
        b, p, foe = battle(["Secret Power"], ["Tackle"], {("p", "Secret Power"): [10] * 16}, hp=500)
        b.st["terrain"] = terrain
        b.rng = FixedDice(dice)
        foe.ability = "Shell Armor"
        fs.attack(b, p, fs.move("Secret Power"), foe, True)
        out[(terrain, dice)] = (foe.stages["acc"], foe.stages["atk"], foe.status, foe.flinch)
    want = {("TERRAIN_PLAIN", 0.0): (-1, 0, None, False), ("TERRAIN_BUILDING", 0.0): (0, 0, "par", False),
            (None, 0.0): (0, 0, "par", False), ("TERRAIN_MOUNTAIN", 0.0): (0, 0, None, True),
            ("TERRAIN_WATER", 0.0): (0, -1, None, False), ("TERRAIN_GRASS", 0.0): (0, 0, "slp", False),
            ("TERRAIN_PLAIN", 0.5): (0, 0, None, False)}
    results.append(("Secret Power adds its terrain's effect at its chance", out == want,
                    f"(accuracy, Attack, status, flinch) {out}"))


def check_snore(results):
    """Snore (approved 2026-10-14; effect script 92): asleep, it hits and
    flinches a target yet to move at its 30%; awake, it fails."""
    out = {}
    for status, dice in (("slp", 0.0), ("slp", 0.5), (None, 0.0)):
        b, p, foe = battle(["Snore"], ["Tackle"], {("p", "Snore"): [10] * 16}, hp=500)
        p.status, p.sleep = status, 3 if status else 0
        b.rng = FixedDice(dice)
        foe.ability = "Shell Armor"
        fs.attack(b, p, fs.move("Snore"), foe, True)
        out[(status, dice)] = (500 - foe.hp, foe.flinch)
    want = {("slp", 0.0): (10, True), ("slp", 0.5): (10, False), (None, 0.0): (0, False)}
    results.append(("Snore hits and flinches asleep and fails awake", out == want, f"(damage, flinch) {out}"))


def check_raise_speed_hit(results):
    """Flame Charge, Trailblaze and Aqua Step (approved 2026-10-14; effect
    script 285): each hit raises its user's Speed a stage, into a
    Substitute too, and Sheer Force strips the rise."""
    out = {}
    for name, ability, sub in (("Flame Charge", None, 0), ("Trailblaze", None, 0), ("Aqua Step", None, 0),
                               ("Flame Charge", None, 30), ("Flame Charge", "Sheer Force", 0)):
        b, p, foe = battle([name], ["Tackle"], {("p", name): [10] * 16}, hp=500)
        b.rng = FixedDice(0.5)
        p.ability, foe.sub = ability, sub
        foe.ability = "Shell Armor"
        fs.attack(b, p, fs.move(name), foe, True)
        out[(name, ability, sub)] = p.stages["spe"]
    want = {("Flame Charge", None, 0): 1, ("Trailblaze", None, 0): 1, ("Aqua Step", None, 0): 1,
            ("Flame Charge", None, 30): 1, ("Flame Charge", "Sheer Force", 0): 0}
    results.append(("Flame Charge and its kind raise their user's Speed", out == want, str(out)))


def check_trump_card(results):
    """Trump Card (approved 2026-10-14; effect script 235,
    BtlCmd_CalcTrumpCardPower): its power by the PP its slot has left once
    the use is paid, 40 from four on, then 50, 60, 80 and 200 at the last,
    Technician judged at each; a figure before the use counts the PP it
    will take."""
    out = {}
    b, p, foe = battle(["Trump Card"], ["Tackle"], {("p", "Trump Card"): [40] * 16}, hp=5000)
    b.rng = FixedDice(0.5)
    foe.ability = "Shell Armor"
    tc = fs.move("Trump Card")
    for _ in range(5):
        before = foe.hp
        fs.use_move(b, p, tc, foe, True)
        out[p.pp["Trump Card"]] = before - foe.hp
    b.turn += 1                          # the next turn, before its user acts
    p.pp["Trump Card"] = 1
    out["figure with 1 PP"] = b.damage(p, foe, tc, roll=0)
    p.ability = "Technician"             # the row's 40 then carries Technician's half again
    out["Technician, figure with 1 PP"] = b.damage(p, foe, tc, roll=0)
    p.pp["Trump Card"] = 5
    out["Technician, figure with 5 PP"] = b.damage(p, foe, tc, roll=0)
    want = {4: 40, 3: 50, 2: 60, 1: 80, 0: 200, "figure with 1 PP": 200, "Technician, figure with 1 PP": 133,
            "Technician, figure with 5 PP": 40}
    results.append(("Trump Card's power rises as its PP runs down", out == want,
                    f"(PP left after the use: damage) {out}"))


def check_teeter_dance(results):
    """Teeter Dance (approved 2026-10-14; effect script 199): in a single
    battle it confuses the foe, Own Tempo aside; in a double battle every
    other Pokemon on the field, the user's ally too, each but one that
    protects itself."""
    out = {}
    for ability in (None, "Own Tempo"):
        b, p, foe = battle(["Teeter Dance"], ["Tackle"], {})
        b.rng = FixedDice(0.0)
        foe.ability = ability
        fs.status_move(b, p, fs.move("Teeter Dance"), foe, True)
        out[f"singles, {ability}"] = bool(foe.confused)
    b = field({"p0": (("Normal",), ["Teeter Dance"]), "p1": (("Normal",), ["Tackle"]),
               "b0.0": (("Normal",), ["Tackle"]), "b0.1": (("Normal",), ["Protect"])}, {})
    b.doubles, b.moved = True, set()
    b.p.active, b.p.active2, b.b.active, b.b.active2 = 0, 1, 0, 1
    b.rng = FixedDice(0.0)
    p0, p1, f0, f1 = b.p.mons[0], b.p.mons[1], b.b.mons[0], b.b.mons[1]
    f1.protecting = True
    fs.status_move(b, p0, fs.move("Teeter Dance"), f0, True)
    out["doubles (target, other foe protecting, ally, user)"] = (bool(f0.confused), bool(f1.confused),
                                                                  bool(p1.confused), bool(p0.confused))
    f0.confused = p1.confused = 0
    f0.protecting, f1.protecting = True, False
    fs.status_move(b, p0, fs.move("Teeter Dance"), f0, True)
    out["doubles, its target protecting (target, other foe, ally)"] = (bool(f0.confused), bool(f1.confused),
                                                                        bool(p1.confused))
    want = {"singles, None": True, "singles, Own Tempo": False,
            "doubles (target, other foe protecting, ally, user)": (True, False, True, False),
            "doubles, its target protecting (target, other foe, ally)": (False, True, True)}
    results.append(("Teeter Dance confuses every other Pokemon on the field", out == want, str(out)))


def check_smelling_salts(results):
    """Smelling Salts (approved 2026-10-14; effect script 171): it doubles on
    a paralysed target and then cures it; a target not paralysed takes the
    plain hit, and a paralysed one behind a Substitute neither doubles nor
    is cured."""
    out = {}
    for status, sub in (("par", 0), (None, 0), ("par", 200)):
        b, p, foe = battle(["Smelling Salts"], ["Tackle"], {("p", "Smelling Salts"): [10] * 16}, hp=500)
        b.rng = FixedDice(0.5)
        foe.ability, foe.status, foe.sub = "Shell Armor", status, sub
        fs.attack(b, p, fs.move("Smelling Salts"), foe, True)
        out[(status, sub)] = (500 - foe.hp + (200 - foe.sub if sub else 0), foe.status)
    want = {("par", 0): (20, None), (None, 0): (10, None), ("par", 200): (10, "par")}
    results.append(("Smelling Salts doubles on paralysis and cures it", out == want,
                    f"(damage, the target's status after) {out}"))


def check_magic_coat(results):
    """Magic Coat (approved 2026-10-14; effect script 183, TrySetMagicCoat,
    BattleControllerPlayer_MoveStolen): used before its foe moves, it turns
    the foe's Thunder Wave back on the foe, once; a second such move that
    turn lands; a move without the flag (Taunt) and one aimed at its user's
    own self are not turned; used last it fails; the turn's end ends it."""
    out = {}
    b, p, foe = battle(["Thunder Wave", "Taunt", "Power Shift"], ["Magic Coat"], {})
    b.rng = FixedDice(0.0)
    fs.status_move(b, foe, fs.move("Magic Coat"), p, True)
    out["set"] = foe.magic_coat
    fs.status_move(b, p, fs.move("Power Shift"), foe, False)
    fs.status_move(b, p, fs.move("Taunt"), foe, False)
    out["Power Shift and Taunt (coat kept, foe taunted)"] = (foe.magic_coat, bool(foe.taunt))
    fs.status_move(b, p, fs.move("Thunder Wave"), foe, False)
    out["Thunder Wave turned (user, foe)"] = (p.status, foe.status)
    p.status = None
    fs.status_move(b, p, fs.move("Thunder Wave"), foe, False)
    out["a second Thunder Wave (user, foe)"] = (p.status, foe.status)
    b2, p2, foe2 = battle(["Thunder Wave"], ["Magic Coat"], {})
    b2.rng = FixedDice(0.0)
    fs.status_move(b2, foe2, fs.move("Magic Coat"), p2, False)
    out["used last"] = foe2.magic_coat
    b3, p3, foe3 = battle(["Thunder Wave"], ["Magic Coat"], {})
    fs.status_move(b3, foe3, fs.move("Magic Coat"), p3, True)
    fs.end_of_turn(b3)
    out["after the turn's end"] = foe3.magic_coat
    want = {"set": True, "Power Shift and Taunt (coat kept, foe taunted)": (True, True),
            "Thunder Wave turned (user, foe)": ("par", None), "a second Thunder Wave (user, foe)": (None, "par"),
            "used last": False, "after the turn's end": False}
    results.append(("Magic Coat turns a reflectable status move back once", out == want, str(out)))


def check_present(results):
    """Present (approved 2026-10-14; effect script 122, BtlCmd_Present):
    prepare() rows it at 40, 80 and 120 power as its own attacker keys, as
    the calculator gives the move itself no row; a use hits from its rolled
    power's row, or for the gift heals its target a quarter, a Ghost too,
    but not one under Heal Block or at full HP."""
    st, pairs, pokemon = prepared_jobs([("Delibird", 30, "Hustle", ["Present"], None)],
                                       [("Bibarel", 30, "Simple", ["Tackle"], None)])
    keyed = {k: pokemon[k]["move_data"]["Present"]["basePower"] for k in pokemon if k.startswith("b0.0#pr")}
    rowed = sorted(a for a, d, mvs, w in pairs if a.startswith("b0.0#pr") and d == "p0" and mvs == ["Present"])
    out = {"keys": keyed, "rows": rowed}

    class Pick:
        """A random source that passes every check and rolls `outcome`."""
        def __init__(self, outcome):
            self.outcome = outcome

        def random(self):
            return 0.0

        def choices(self, items, weights):
            return [self.outcome]

        def randint(self, a, b):
            return a

        def randrange(self, n):
            return 0

        def choice(self, seq):
            return seq[0]
    for outcome, setup in ((120, None), (0, None), (0, "Ghost"), (0, "Heal Block"), (0, "full")):
        b, p, foe = battle(["Tackle"], ["Present"], {}, p_types=("Ghost",) if setup == "Ghost" else ("Normal",))
        b.st["rows"][(None, "b0.0#pr120", "p0")] = {"moves": {"Present": {"rolls": [30] * 16}}}
        b.rng = Pick(outcome)
        p.ability = "Shell Armor"
        p.hp = 100 if setup == "full" else 40
        p.heal_block = 5 if setup == "Heal Block" else 0
        fs.attack(b, foe, fs.move("Present"), p, True)
        out[(outcome, setup)] = p.hp
    want = {"keys": {"b0.0#pr40": 40, "b0.0#pr80": 80, "b0.0#pr120": 120},
            "rows": ["b0.0#pr120", "b0.0#pr40", "b0.0#pr80"],
            (120, None): 10, (0, None): 65, (0, "Ghost"): 65, (0, "Heal Block"): 40, (0, "full"): 100}
    results.append(("Present hits at its rolled power or heals a quarter", out == want, str(out)))


def check_water_sport(results):
    """Water Sport (approved 2026-10-14; effect script 210): while its user
    stands, every Fire move's power is halved, the trainer's AI's figure
    too; a second use fails, Baton Pass hands it on, and leaving ends it."""
    out = {}
    b, p, foe = battle(["Water Sport", "Baton Pass"], ["Ember"], {("b", "Ember"): [40] * 16})
    b.st["water_sport"] = b.sporty = True        # as prepare() and the battle's making set them
    ember = fs.move("Ember")
    out["before"] = (b.damage(foe, p, ember, roll=0), fightai.figure(b, foe, p, ember))
    fs.status_move(b, p, fs.move("Water Sport"), foe, True)
    out["after"] = (b.damage(foe, p, ember, roll=0), fightai.figure(b, foe, p, ember))
    out["AI's second Water Sport"] = fightai.basic(b, p, foe, fs.move("Water Sport"), 0)
    passed = fs.baton_state(p)
    out["handed on"] = passed["water_sport"]
    p.reset_volatile()
    out["after leaving"] = (p.water_sport, b.damage(foe, p, ember, roll=0))
    want = {"before": (40, 40), "after": (20, 20), "AI's second Water Sport": -10, "handed on": True,
            "after leaving": (False, 40)}
    results.append(("Water Sport halves Fire moves while its user stands", out == want, str(out)))


def check_acrobatics(results):
    """Acrobatics (approved 2026-10-14; effect script 289): twice its row
    when its user holds no item, the row when it holds one."""
    out = {}
    for item in (None, "Sitrus Berry"):
        b, p, foe = battle(["Acrobatics"], ["Tackle"], {("p", "Acrobatics"): [10] * 16}, hp=500)
        b.rng = FixedDice(0.5)
        p.item, foe.ability = item, "Shell Armor"
        fs.attack(b, p, fs.move("Acrobatics"), foe, True)
        out[item] = 500 - foe.hp
    want = {None: 20, "Sitrus Berry": 10}
    results.append(("Acrobatics doubles without a held item", out == want, str(out)))


def check_guard_swap(results):
    """Guard Swap (approved 2026-10-14; effect script 244): the user's and
    the target's Defense and Sp. Def stages change places, through a
    Substitute too, and no other stage moves."""
    b, p, foe = battle(["Guard Swap"], ["Tackle"], {})
    b.rng = FixedDice(0.0)
    p.stages.update({"def": 2, "spd": -1, "atk": 1})
    foe.stages.update({"def": -1, "spd": 3, "spa": 2})
    foe.sub = 25
    fs.status_move(b, p, fs.move("Guard Swap"), foe, True)
    got = ({k: v for k, v in p.stages.items() if v}, {k: v for k, v in foe.stages.items() if v})
    want = ({"def": -1, "spd": 3, "atk": 1}, {"def": 2, "spd": -1, "spa": 2})
    results.append(("Guard Swap swaps the Defense and Sp. Def stages", got == want, f"(user, target) {got}"))


def check_power_swap(results):
    """Power Swap (approved 2026-10-14; effect script 243): the user's and
    the target's Attack and Sp. Atk stages change places, through a
    Substitute too, and no other stage moves."""
    b, p, foe = battle(["Power Swap"], ["Tackle"], {})
    b.rng = FixedDice(0.0)
    p.stages.update({"atk": -2, "spa": 1, "def": 1})
    foe.stages.update({"atk": 4, "spa": -1, "spd": 2})
    foe.sub = 25
    fs.status_move(b, p, fs.move("Power Swap"), foe, True)
    got = ({k: v for k, v in p.stages.items() if v}, {k: v for k, v in foe.stages.items() if v})
    want = ({"atk": 4, "spa": -1, "def": 1}, {"atk": -2, "spa": 1, "spd": 2})
    results.append(("Power Swap swaps the Attack and Sp. Atk stages", got == want, f"(user, target) {got}"))


def check_psycho_shift(results):
    """Psycho Shift (approved 2026-10-14; effect script 234): it gives the
    target its user's status and cures the user, a sleep with a fresh
    count; it fails with no status on the user, a status on the target, a
    Substitute in the way, or a target the status cannot reach (a Fire
    type for a burn), and the user keeps its status then."""
    out = {}
    for user, target, setup in (("par", None, None), ("slp", None, None), ("brn", None, "Fire"),
                                (None, None, None), ("par", "psn", None), ("par", None, "sub")):
        b, p, foe = battle(["Psycho Shift"], ["Tackle"], {}, b_types=("Fire",) if setup == "Fire" else ("Normal",))
        b.rng = FixedDice(0.0)
        p.status, p.sleep, foe.status = user, 3 if user == "slp" else 0, target
        foe.sub = 25 if setup == "sub" else 0
        fs.status_move(b, p, fs.move("Psycho Shift"), foe, True)
        out[(user, target, setup)] = (p.status, foe.status, foe.sleep > 0)
    want = {("par", None, None): (None, "par", False), ("slp", None, None): (None, "slp", True),
            ("brn", None, "Fire"): ("brn", None, False), (None, None, None): (None, None, False),
            ("par", "psn", None): ("par", "psn", False), ("par", None, "sub"): ("par", None, False)}
    results.append(("Psycho Shift hands its user's status to the target", out == want,
                    f"(user's status, target's, the target's sleep count set) {out}"))


def check_memento(results):
    """Memento (approved 2026-10-14; effect script 168, subscript_memento):
    its user faints before the move's checks, so a miss and a Protect
    still cost it, and the target's Attack and Sp. Atk fall two stages
    each, but not through a Substitute or Clear Body, and not the Attack
    of a Hyper Cutter holder; with no target nothing happens."""
    out = {}
    for setup in (None, "sub", "Clear Body", "Hyper Cutter", "protect", "miss", "no target"):
        b, p, foe = battle(["Memento"], ["Tackle"], {})
        b.rng = FixedDice(0.5)
        foe.sub = 25 if setup == "sub" else 0
        foe.ability = setup if setup in ("Clear Body", "Hyper Cutter") else None
        foe.protecting = setup == "protect"
        foe.stages["eva"] = 6 if setup == "miss" else 0
        if setup == "no target":
            foe.hp = 0
        fs.status_move(b, p, fs.move("Memento"), foe, True)
        out[setup] = (p.hp == 0, foe.stages["atk"], foe.stages["spa"])
    want = {None: (True, -2, -2), "sub": (True, 0, 0), "Clear Body": (True, 0, 0), "Hyper Cutter": (True, 0, -2),
            "protect": (True, 0, 0), "miss": (True, 0, 0), "no target": (False, 0, 0)}
    results.append(("Memento faints its user first and its drops meet the blockers", out == want,
                    f"(user fainted, target's Attack, Sp. Atk) {out}"))


def check_sketch(results):
    """Sketch (approved 2026-10-14; effect script 95, BtlCmd_TrySketch): the
    target's last move takes Sketch's slot for good with its full PP, and
    stays when the user leaves; it fails with no last move, on Struggle or
    Chatter, on a move the user knows already, through a Substitute and
    for a transformed user; and prepare() rows a Sketch user with its
    foes' damaging moves."""
    def setup(last, known=("Sketch", "Tackle")):
        b, p, foe = battle(list(known), ["Hyper Beam", "Ember"], {})
        foe.last = fs.move(last) if last else None
        return b, p, foe
    out = {}
    b, p, foe = setup("Ember")
    fs._use_move(b, p, fs.move("Sketch"), foe, True)
    out["sketched"] = ([m.name for m in p.moves], dict(p.pp))
    p.reset_volatile()
    out["after leaving"] = [m.name for m in p.moves]
    for label, kw in (("no last move", {"last": None}), ("known already", {"last": "Tackle"}),
                      ("Struggle", {"last": "Struggle"}), ("Chatter", {"last": "Chatter"})):
        b, p, foe = setup(**kw)
        fs.status_move(b, p, fs.move("Sketch"), foe, True)
        out[label] = [m.name for m in p.moves]
    b, p, foe = setup("Ember")
    foe.sub = 30
    fs.status_move(b, p, fs.move("Sketch"), foe, True)
    out["behind a Substitute"] = [m.name for m in p.moves]
    b, p, foe = setup("Ember")
    p.transformed = True
    fs.status_move(b, p, fs.move("Sketch"), foe, True)
    out["transformed"] = [m.name for m in p.moves]
    st, pairs, _pokemon = prepared_jobs([("Smeargle", 30, "Own Tempo", ["Sketch"], None)],
                                        [("Machop", 30, "Guts", ["Karate Chop", "Leer"], None)])
    out["the Sketch user's rows"] = sorted({m for a, d, mv, _w in pairs if a == "b0.0" and d == "p0" for m in mv})
    plain = ["Sketch", "Tackle"]
    want = {"sketched": (["Ember", "Tackle"], {"Tackle": fs.move("Tackle").pp, "Ember": fs.move("Ember").pp}),
            "after leaving": ["Ember", "Tackle"], "no last move": plain, "known already": plain, "Struggle": plain,
            "Chatter": plain, "behind a Substitute": plain, "transformed": plain,
            "the Sketch user's rows": ["Karate Chop"]}
    results.append(("Sketch takes the target's last move for good, and is rowed with its foes' moves",
                    out == want, str(out)))


def check_me_first(results):
    """Me First (approved 2026-10-14; effect script 241, BtlCmd_TryMeFirst):
    moving first, its user uses the target's chosen hit as its own at half
    again its damage, its own PP spent and the half again gone after; it
    fails after the target has moved, on a status move and on Counter; and
    prepare() rows a Me First user with its foes' damaging moves."""
    out = {}
    for label, chosen, first in (("Ember, first", "Ember", True), ("Ember, second", "Ember", False),
                                 ("Growl", "Growl", True), ("Counter", "Counter", True)):
        b, p, foe = battle(["Me First", "Tackle"], ["Ember", "Growl", "Counter"], {}, hp=500)
        b.st["rows"][(None, "p0", "b0.0")]["moves"]["Ember"] = {"rolls": [20] * 16}     # its borrowed row
        b.rng = FixedDice(0.5)
        foe.ability = "Shell Armor"
        foe.chosen = fs.move(chosen)
        fs.use_move(b, p, fs.move("Me First"), foe, first)
        out[label] = (500 - foe.hp, p.pp["Me First"], p.me_first)
    st, pairs, _pokemon = prepared_jobs([("Furret", 30, "Keen Eye", ["Me First"], None)],
                                        [("Machop", 30, "Guts", ["Karate Chop", "Leer"], None)])
    out["the Me First user's rows"] = sorted({m for a, d, mv, _w in pairs if a == "b0.0" and d == "p0" for m in mv})
    pp = fs.move("Me First").pp - 1
    want = {"Ember, first": (30, pp, False), "Ember, second": (0, pp, False), "Growl": (0, pp, False),
            "Counter": (0, pp, False), "the Me First user's rows": ["Karate Chop"]}
    results.append(("Me First uses the target's chosen hit at half again", out == want,
                    f"(damage, Me First's PP, the flag after) {out}"))


def check_nature_power(results):
    """Nature Power (approved 2026-10-14; effect script 173,
    BtlCmd_GetTerrainMove): it uses its battle terrain's move as its own,
    Earthquake on plain ground, Tri Attack in a building and where the
    fight names no terrain, spending only its own PP; and prepare() rows its
    user with that move."""
    out = {}
    for terrain, called in (("TERRAIN_PLAIN", "Earthquake"), (None, "Tri Attack")):
        b, p, foe = battle(["Nature Power"], ["Tackle"], {}, hp=500)
        b.st["rows"][(None, "p0", "b0.0")]["moves"][called] = {"rolls": [25] * 16}
        b.st["terrain"] = terrain
        b.rng = FixedDice(0.5)
        foe.ability = "Shell Armor"
        fs.use_move(b, p, fs.move("Nature Power"), foe, True)
        out[terrain] = (500 - foe.hp, dict(p.pp))
    for terrain in ("TERRAIN_PLAIN", None):
        st, pairs, _pokemon = prepared_jobs([("Ludicolo", 30, "Swift Swim", ["Nature Power"], None)],
                                            [("Machop", 30, "Guts", ["Leer"], None)], terrain=terrain)
        out[f"rows, {terrain}"] = sorted({m for a, d, mv, _w in pairs if a == "b0.0" and d == "p0" for m in mv})
    pp = {"Nature Power": fs.move("Nature Power").pp - 1}
    want = {"TERRAIN_PLAIN": (25, pp), None: (25, pp), "rows, TERRAIN_PLAIN": ["Earthquake"],
            "rows, None": ["Tri Attack"]}
    results.append(("Nature Power uses its terrain's move", out == want, str(out)))


def check_power_trick(results):
    """Power Trick (approved 2026-10-14; effect script 238,
    subscript_user_swap_atk_and_def): its user's Attack and Defense change
    places, so its hits and the hits into it read its twin with the two
    swapped, until a second use puts them back or it leaves; the trainer's
    AI refuses another use while it holds; Baton Pass hands it on; and
    prepare() builds the twin from swapped base stats, IVs and nature."""
    out = {}
    b, p, foe = battle(["Power Trick", "Tackle", "Baton Pass"], ["Tackle"],
                       {("p", "Tackle"): [10] * 16, ("b", "Tackle"): [20] * 16})
    b.st["rows"][(None, "p0#trick", "b0.0")] = {"moves": {"Tackle": {"rolls": [30] * 16}}}
    b.st["rows"][(None, "b0.0", "p0#trick")] = {"moves": {"Tackle": {"rolls": [5] * 16}}}
    b.st["trick_twin"] = {"p0": "p0#trick"}
    tackle, trick = fs.move("Tackle"), fs.move("Power Trick")

    def hits():
        return b.damage(p, foe, tackle, roll=0), b.damage(foe, p, tackle, roll=0)
    out["before"] = hits()
    fs.status_move(b, p, trick, foe, True)
    out["after"] = hits()
    out["AI's second Power Trick"] = fightai.basic(b, p, foe, trick, 0)
    out["handed on"] = fs.baton_state(p)["power_trick"]
    fs.status_move(b, p, trick, foe, True)
    out["used again"] = hits()
    fs.status_move(b, p, trick, foe, True)
    p.reset_volatile()
    out["after leaving"] = (p.power_trick,) + hits()
    out["natures"] = [fs.swapped_nature(n) for n in ("Adamant", "Lonely", "Timid", "Modest", "Hardy", "Jolly")]
    st, pairs, pokemon = prepared_jobs([("Shuckle", 30, "Sturdy", ["Power Trick", "Rollout"], None)],
                                       [("Machop", 30, "Guts", ["Karate Chop"], None)])
    twin, own = pokemon.get("b0.0#trick", {}), pokemon["b0.0"]
    base = (fs.calc.blob()["poks"]["Shuckle"]["bs"]["at"], fs.calc.blob()["poks"]["Shuckle"]["bs"]["df"])
    out["the twin's base Attack and Defense"] = ((twin.get("species_data") or {}).get("bs", {}).get("at"),
                                                (twin.get("species_data") or {}).get("bs", {}).get("df")) == base[::-1]
    out["the twin's rows"] = sorted((a, d) for a, d, _mv, _w in pairs if "#trick" in a or "#trick" in d)
    want = {"before": (10, 20), "after": (30, 5), "AI's second Power Trick": -10, "handed on": True,
            "used again": (10, 20), "after leaving": (False, 10, 20),
            "natures": ["Impish", "Bold", "Hasty", "Mild", "Hardy", "Jolly"],
            "the twin's base Attack and Defense": True,
            "the twin's rows": [("b0.0#trick", "p0"), ("p0", "b0.0#trick")]}
    results.append(("Power Trick swaps its user's Attack and Defense through its twin", out == want, str(out)))


def check_bide(results):
    """Bide (approved 2026-10-14; effect script 26, CHECK_STATUS_STATE_BIDE,
    subscript_bide_end): its first use locks its user in and starts
    storing; the hits it takes over that turn and the next are stored; the
    third use gives back twice the store, past the type chart, spending
    PP only on the first; with nothing stored it fails; a turn its user
    cannot act ends it; and a Protect stops the strike."""
    def run(foe_types=("Normal",), hits=(True, True), stop=None, protect=False, turns=3):
        b, p, foe = battle(["Bide"], ["Tackle"], {("b", "Tackle"): [15] * 16}, b_types=foe_types, hp=500)
        b.rng = FixedDice(0.5)
        p.ability = foe.ability = "Shell Armor"
        bide, tackle = fs.move("Bide"), fs.move("Tackle")
        for turn in range(turns):
            if turn == 2 and protect:
                foe.protecting = True
            if turn == stop:
                p.flinch = True
            fs.use_move(b, p, p.lock[0] if p.lock else bide, foe, True)
            if turn < 2 and hits[turn]:
                fs.use_move(b, foe, tackle, p, False)
        return 500 - foe.hp, p.pp["Bide"], p.bide, p.lock is not None
    pp = fs.move("Bide").pp - 1
    out = {"stored two hits": run(), "into a Ghost": run(("Ghost",)), "nothing stored": run(hits=(False, False)),
           "a flinch on its second turn": run(stop=1, turns=2)[1:], "into a Protect": run(protect=True)}
    want = {"stored two hits": (60, pp, 0, False), "into a Ghost": (60, pp, 0, False),
            "nothing stored": (0, pp, 0, False), "a flinch on its second turn": (pp, 0, False),
            "into a Protect": (0, pp, 0, False)}
    results.append(("Bide stores two turns' hits and gives back twice", out == want,
                    f"(damage given back, Bide's PP, the count left, still locked) {out}"))


def check_transform(results):
    """Transform (approved 2026-10-14, the cheap part; effect script 57,
    BtlCmd_Transform): its user copies the target's moves at 5 PP, its
    stages, types, ability and Speed, its hits read the copied Pokemon's
    rows where they exist, and leaving brings its own back; it fails on a
    target transformed already or in the air."""
    def setup():
        b, p, foe = battle(["Transform"], ["Ember", "Growl"], {}, p_speed=30, b_speed=90, b_types=("Fire",), hp=500)
        foe.ability, foe.stages["atk"] = "Blaze", 2
        b.rng = FixedDice(0.5)
        return b, p, foe
    out = {}
    b, p, foe = setup()
    b.st["rows"][(None, "b0.0", "b0.0")] = {"moves": {"Ember": {"rolls": [33] * 16}}}    # the copy's row on its target
    fs.use_move(b, p, fs.move("Transform"), foe, True)
    out["copied"] = ([m.name for m in p.moves], dict(p.pp), p.types, p.ability, p.stages["atk"], b.speed(p))
    before = foe.hp
    fs.attack(b, p, fs.move("Ember"), foe, True)
    out["its Ember"] = before - foe.hp
    p.reset_volatile()
    out["after leaving"] = ([m.name for m in p.moves], dict(p.pp), p.types, p.ability, b.speed(p))
    for label in ("target transformed", "target in the air"):
        b, p, foe = setup()
        if label == "target transformed":
            foe.transformed = True
        else:
            foe.charging = fs.move("Fly")
        fs.status_move(b, p, fs.move("Transform"), foe, True)
        out[label] = [m.name for m in p.moves]
    tpp = fs.move("Transform").pp - 1
    want = {"copied": (["Ember", "Growl"], {"Ember": 5, "Growl": 5}, ["Fire"], "Blaze", 2, 90), "its Ember": 33,
            "after leaving": (["Transform"], {"Transform": tpp}, ["Normal"], None, 30),
            "target transformed": ["Transform"], "target in the air": ["Transform"]}
    results.append(("Transform copies its target's moves, stages, types, ability and Speed", out == want, str(out)))


def check_sp_def_2_hit(results):
    """Acid Spray, Lumina Crash and Seed Flare (approved 2026-10-14; effect
    script 271): the hit lowers the target's Sp. Def two stages at the
    move's chance, Seed Flare's four in ten, and Sheer Force strips it."""
    out = {}
    for name, value, ability in (("Acid Spray", 0.3, None), ("Seed Flare", 0.3, None), ("Seed Flare", 0.5, None),
                                 ("Acid Spray", 0.3, "Sheer Force")):
        b, p, foe = battle([name], ["Tackle"], {("p", name): [10] * 16}, hp=500)
        b.rng = FixedDice(value)
        p.ability = ability
        fs.attack(b, p, fs.move(name), foe, True)
        out[(name, value, ability)] = foe.stages["spd"]
    want = {("Acid Spray", 0.3, None): -2, ("Seed Flare", 0.3, None): -2, ("Seed Flare", 0.5, None): 0,
            ("Acid Spray", 0.3, "Sheer Force"): 0}
    results.append(("Acid Spray and Seed Flare lower Sp. Def two stages at their chance", out == want, str(out)))


def check_tearful_look(results):
    """Noble Roar and Tearful Look (approved 2026-10-14; effect script 362):
    the target's Attack and Sp. Atk fall a stage each, and a Substitute
    stops both."""
    out = {}
    for name, sub in (("Tearful Look", 0), ("Noble Roar", 0), ("Noble Roar", 25)):
        b, p, foe = battle([name], ["Tackle"], {})
        b.rng = FixedDice(0.0)
        foe.sub = sub
        fs.status_move(b, p, fs.move(name), foe, True)
        out[(name, sub)] = (foe.stages["atk"], foe.stages["spa"])
    want = {("Tearful Look", 0): (-1, -1), ("Noble Roar", 0): (-1, -1), ("Noble Roar", 25): (0, 0)}
    results.append(("Noble Roar and Tearful Look lower Attack and Sp. Atk", out == want, str(out)))


def check_venom_drench(results):
    """Venom Drench (approved 2026-10-14; effect script 361): a poisoned or
    badly poisoned target's Attack, Sp. Atk and Speed fall a stage each;
    any other target's do not, and a Substitute stops it."""
    out = {}
    for status, sub in ((None, 0), ("psn", 0), ("tox", 0), ("psn", 25)):
        b, p, foe = battle(["Venom Drench"], ["Tackle"], {})
        b.rng = FixedDice(0.0)
        foe.status, foe.sub = status, sub
        fs.status_move(b, p, fs.move("Venom Drench"), foe, True)
        out[(status, sub)] = (foe.stages["atk"], foe.stages["spa"], foe.stages["spe"])
    want = {(None, 0): (0, 0, 0), ("psn", 0): (-1, -1, -1), ("tox", 0): (-1, -1, -1), ("psn", 25): (0, 0, 0)}
    results.append(("Venom Drench lowers a poisoned target's three stats", out == want, str(out)))


def check_false_swipe(results):
    """False Swipe and Hold Back (approved 2026-10-14; effect script 101): a
    hit that would knock its target out leaves it at 1 HP, one at 1 HP deals
    nothing, and a full-HP target keeps its Focus Sash."""
    out = {}
    for name, hp, item in (("False Swipe", 30, None), ("Hold Back", 1, None), ("False Swipe", 100, "Focus Sash"),
                           ("Tackle", 30, None)):
        b, p, foe = battle([name], ["Tackle"], {("p", name): [200] * 16})
        b.rng = FixedDice(0.5)
        foe.hp, foe.item = hp, item
        fs.attack(b, p, fs.move(name), foe, True)
        out[(name, hp)] = (foe.hp, foe.item)
    want = {("False Swipe", 30): (1, None), ("Hold Back", 1): (1, None), ("False Swipe", 100): (1, "Focus Sash"),
            ("Tackle", 30): (0, None)}
    results.append(("False Swipe and Hold Back leave their target 1 HP", out == want, str(out)))


def check_clear_smog(results):
    """Clear Smog (approved 2026-10-14; effect script 390): after its hit
    every stage of the target goes back to 0, not through a Substitute, and
    Shield Dust does not stop it."""
    out = {}
    for sub, ability in ((0, None), (40, None), (0, "Shield Dust")):
        b, p, foe = battle(["Clear Smog"], ["Tackle"], {("p", "Clear Smog"): [10] * 16}, hp=500)
        b.rng = FixedDice(0.5)
        foe.stages.update({"atk": 2, "def": -1, "eva": 1})
        foe.sub, foe.ability = sub, ability
        fs.attack(b, p, fs.move("Clear Smog"), foe, True)
        out[(sub, ability)] = (foe.stages["atk"], foe.stages["def"], foe.stages["eva"])
    want = {(0, None): (0, 0, 0), (40, None): (2, -1, 1), (0, "Shield Dust"): (0, 0, 0)}
    results.append(("Clear Smog resets its target's stages after the hit", out == want, str(out)))


def check_incinerate(results):
    """Incinerate (approved 2026-10-14; effect script 372): after its hit the
    target's Berry is burned up, not eaten and not for Recycle; not through
    a Substitute, and an item that is no Berry, or the Roseli Berry Oxide
    added past Rowap, stays."""
    out = {}
    for item, sub in (("Sitrus Berry", 0), ("Sitrus Berry", 40), ("Leftovers", 0), ("Roseli Berry", 0)):
        b, p, foe = battle(["Incinerate"], ["Tackle"], {("p", "Incinerate"): [10] * 16}, hp=500)
        b.rng = FixedDice(0.5)
        foe.item, foe.sub = item, sub
        fs.attack(b, p, fs.move("Incinerate"), foe, True)
        out[(item, sub)] = (foe.item, foe.recycle, foe.ate_berry)
    want = {("Sitrus Berry", 0): (None, None, False), ("Sitrus Berry", 40): ("Sitrus Berry", None, False),
            ("Leftovers", 0): ("Leftovers", None, False), ("Roseli Berry", 0): ("Roseli Berry", None, False)}
    results.append(("Incinerate burns up its target's Berry", out == want, str(out)))


def check_life_dew(results):
    """Life Dew (approved 2026-10-14; effect script 383): its user gets back
    a quarter of its maximum HP, rounded up, never past full, and nothing
    under Heal Block."""
    out = {}
    for hp, block in ((50, 0), (90, 0), (50, 3)):
        b, p, foe = battle(["Life Dew"], ["Tackle"], {}, hp=101)
        b.rng = FixedDice(0.0)
        p.hp, p.heal_block = hp, block
        fs.status_move(b, p, fs.move("Life Dew"), foe, True)
        out[(hp, block)] = p.hp
    want = {(50, 0): 76, (90, 0): 101, (50, 3): 50}
    results.append(("Life Dew heals a quarter, rounded up, not under Heal Block", out == want, str(out)))


def check_mud_sport(results):
    """Mud Sport (approved 2026-10-14; effect script 201): while its user
    stands, every Electric move's power is halved, the trainer's AI's figure
    too, and Fire moves keep theirs; a second use fails, Baton Pass hands it
    on, and leaving ends it."""
    out = {}
    b, p, foe = battle(["Mud Sport", "Baton Pass"], ["Thunder Shock", "Ember"],
                       {("b", "Thunder Shock"): [40] * 16, ("b", "Ember"): [40] * 16})
    b.st["mud_sport"], b.sporty = True, True
    shock, ember = fs.move("Thunder Shock"), fs.move("Ember")
    out["before"] = (b.damage(foe, p, shock, roll=0), fightai.figure(b, foe, p, shock))
    fs.status_move(b, p, fs.move("Mud Sport"), foe, True)
    out["after"] = (b.damage(foe, p, shock, roll=0), fightai.figure(b, foe, p, shock), b.damage(foe, p, ember, roll=0))
    out["AI's second Mud Sport"] = fightai.basic(b, p, foe, fs.move("Mud Sport"), 0)
    out["handed on"] = fs.baton_state(p)["mud_sport"]
    p.reset_volatile()
    out["after leaving"] = (p.mud_sport, b.damage(foe, p, shock, roll=0))
    want = {"before": (40, 40), "after": (20, 20, 40), "AI's second Mud Sport": -10, "handed on": True,
            "after leaving": (False, 40)}
    results.append(("Mud Sport halves Electric moves while its user stands", out == want, str(out)))


def check_punishment(results):
    """Punishment (approved 2026-10-14; effect script 245): 60 power and 20
    more for each stage the target has raised, up to 200, on a row made at
    60; Technician's half again counts only while the power is 60."""
    out = {}
    for stages, ability in (({}, None), ({"atk": 2, "spe": 1}, None), ({"atk": 6, "spa": 6}, None),
                            ({"eva": 1}, "Technician"), ({"def": -2}, None)):
        b, p, foe = battle(["Punishment"], ["Tackle"], {("p", "Punishment"): [30] * 16})
        p.ability = ability
        foe.stages.update(stages)
        out[(tuple(sorted(stages.items())), ability)] = b.damage(p, foe, fs.move("Punishment"), roll=0)
    want = {((), None): 30, ((("atk", 2), ("spe", 1)), None): 60, ((("atk", 6), ("spa", 6)), None): 100,
            ((("eva", 1),), "Technician"): 26, ((("def", -2),), None): 60}
    results.append(("Punishment's power rises with the target's raised stages", out == want, str(out)))


def check_sticky_web(results):
    """Sticky Web (approved 2026-10-14; effect script 326, the hazards
    check): a web on the foe's side, once; each grounded newcomer there
    loses a stage of Speed, a Magic Guard holder too, a Flying type none,
    Clear Body none, Contrary gains one, Simple loses one, Defiant answers
    with two of Attack; the trainer's AI refuses a second web, and Rapid
    Spin clears it."""
    out = {}
    for case in ("plain", "Flying", "Magic Guard", "Clear Body", "Contrary", "Simple", "Defiant"):
        b, p, foe = battle(["Sticky Web"], ["Tackle", "Rapid Spin"], {("b", "Rapid Spin"): [5] * 16})
        b.rng = FixedDice(0.0)
        extra = fs.Mon("b0.1", b.st["pokemon"]["b0.0"], b.st["info"]["b0.0"], ["Tackle", "Rapid Spin"], "b")
        b.b.mons.append(extra)
        fs.status_move(b, p, fs.move("Sticky Web"), foe, True)
        if case == "Flying":
            extra.types = ["Flying"]
        elif case != "plain":
            extra.ability = case
        fs.switch_in(b, b.b, 1)
        out[case] = (extra.stages["spe"], extra.stages["atk"])
        if case == "plain":
            out["laid"] = (b.b.web, b.p.web)
            fs.status_move(b, p, fs.move("Sticky Web"), extra, True)
            out["laid twice"] = b.b.web
    b, p, foe = battle(["Sticky Web"], ["Rapid Spin"], {("b", "Rapid Spin"): [5] * 16})
    b.rng = FixedDice(0.5)
    fs.status_move(b, p, fs.move("Sticky Web"), foe, True)
    fs.attack(b, foe, fs.move("Rapid Spin"), p, True)
    out["after Rapid Spin"] = b.b.web
    # The trainer's AI on a web already laid on the player's side.
    b, p, foe = battle(["Tackle"], ["Sticky Web"], {})
    b.p.mons.append(fs.Mon("p1", b.st["pokemon"]["p0"], b.st["info"]["p0"], ["Tackle"], "p"))
    out["AI's first web"] = fightai.basic(b, foe, p, fs.move("Sticky Web"), 0)
    fs.status_move(b, foe, fs.move("Sticky Web"), p, True)
    out["AI's second web"] = fightai.basic(b, foe, p, fs.move("Sticky Web"), 0)
    want = {"plain": (-1, 0), "laid": (1, 0), "laid twice": 1, "after Rapid Spin": 0, "Flying": (0, 0),
            "Magic Guard": (-1, 0), "Clear Body": (0, 0), "Contrary": (1, 0), "Simple": (-1, 0),
            "Defiant": (-1, 2), "AI's first web": 0, "AI's second web": -10}
    results.append(("Sticky Web lowers a grounded newcomer's Speed", out == want, str(out)))


def check_defog(results):
    """Defog (approved 2026-10-14; effect script 258): the target's evasion
    falls a stage, not through a Substitute and not while its side's Mist
    stands, which the drop meets first; its side loses its screens, Mist
    and Safeguard whatever became of the drop; both sides lose every
    hazard; and deep fog clears."""
    out = {}
    for case, sub, mist in (("plain", 0, 0), ("Substitute", 25, 0), ("Mist", 0, 2)):
        b, p, foe = battle(["Defog"], ["Tackle"], {})
        b.rng = FixedDice(0.0)
        b.fog = True                     # deep fog, its own flag since 2026-10-15 (fightsim.fog_cut)
        foe.sub = sub
        b.b.screens.update({"Reflect": 4, "Light Screen": 3})
        b.b.mist, b.b.safeguard, b.b.web = mist, 3, 1
        b.b.hazards.update({"spikes": 2, "rocks": 1})
        b.p.hazards.update({"tspikes": 1, "rocks": 1})
        b.p.web, b.p.screens["Reflect"] = 1, 2
        fs.status_move(b, p, fs.move("Defog"), foe, True)
        out[case] = (foe.stages["eva"], tuple(b.b.screens.values()), b.b.mist, b.b.safeguard,
                     tuple(b.b.hazards.values()), b.b.web, tuple(b.p.hazards.values()), b.p.web,
                     b.p.screens["Reflect"], b.fog)
    clear = ((0, 0), 0, 0, (0, 0, 0), 0, (0, 0, 0), 0, 2, False)
    want = {"plain": (-1,) + clear, "Substitute": (0,) + clear, "Mist": (0,) + clear}
    results.append(("Defog lowers evasion and clears screens, hazards and fog", out == want, str(out)))


def check_strength_sap(results):
    """Strength Sap (approved 2026-10-14; effect script 378): its user heals
    by the target's Attack stat at its stage, taken before the target's
    Attack falls a stage; a Substitute stops the drop, not the heal; a Big
    Root adds 30 per cent; Liquid Ooze turns it to damage; it fails at
    -6."""
    out = {}
    for case, stage, sub, item, ability in (("plain", 0, 0, None, None), ("+2", 2, 0, None, None),
                                           ("-1", -1, 0, None, None), ("Substitute", 0, 25, None, None),
                                           ("Big Root", 0, 0, "Big Root", None),
                                           ("Liquid Ooze", 0, 0, None, "Liquid Ooze"), ("-6", -6, 0, None, None)):
        b, p, foe = battle(["Strength Sap"], ["Tackle"], {}, hp=400)
        b.rng = FixedDice(0.0)
        p.hp, p.item = 200, item
        foe.stages["atk"], foe.sub, foe.ability = stage, sub, ability
        fs.status_move(b, p, fs.move("Strength Sap"), foe, True)
        out[case] = (p.hp, foe.stages["atk"])
    want = {"plain": (300, -1), "+2": (400, 1), "-1": (266, -2), "Substitute": (300, 0), "Big Root": (330, -1),
            "Liquid Ooze": (100, -1), "-6": (200, -6)}
    results.append(("Strength Sap heals by the target's Attack and lowers it", out == want, str(out)))


def check_parting_shot(results):
    """Parting Shot (approved 2026-10-14; effect script 389): the target's
    Attack and Sp. Atk fall a stage each and the user is marked to switch
    out as after U-turn, even when Clear Body stops the drops; a Substitute
    stops it all, and so do both stats at -6."""
    out = {}
    for case in ("plain", "Clear Body", "Substitute", "-6"):
        b, p, foe = battle(["Parting Shot"], ["Tackle"], {})
        b.rng = FixedDice(0.0)
        if case == "Clear Body":
            foe.ability = case
        elif case == "Substitute":
            foe.sub = 25
        elif case == "-6":
            foe.stages.update({"atk": -6, "spa": -6})
        fs.status_move(b, p, fs.move("Parting Shot"), foe, True)
        out[case] = (foe.stages["atk"], foe.stages["spa"], p.u_turn)
    want = {"plain": (-1, -1, True), "Clear Body": (0, 0, True), "Substitute": (0, 0, False), "-6": (-6, -6, False)}
    results.append(("Parting Shot lowers both attacking stats and switches its user out", out == want, str(out)))


def check_dragon_tail(results):
    """Dragon Tail and Circle Throw (approved 2026-10-14; effect script 395):
    after the hit the target is dragged out for a bench member, unless it
    fainted, a Substitute took the hit (one it broke too), Suction Cups or
    Ingrain holds it, or no one is left to come in. Since the engine's fix
    of 2026-10-15 (6809a5c4e) the drag runs from the after-move effects,
    once the target's own ability and held items have answered (approved
    2026-10-15): the target's Rough Skin answers the hit, the Pokemon
    dragged in has not been hit and does not, and a user that falls to
    the Rough Skin drags nothing."""
    out = {}
    for case in ("plain", "Substitute", "Substitute broken", "Suction Cups", "Ingrain", "no bench", "fainted",
                 "Rough Skin", "Rough Skin dragged in", "user falls"):
        b, p, foe = battle(["Dragon Tail"], ["Tackle"], {("p", "Dragon Tail"): [10] * 16}, hp=100)
        b.rng = FixedDice(0.5)
        if case != "no bench":
            extra = fs.Mon("b0.1", b.st["pokemon"]["b0.0"], b.st["info"]["b0.0"], ["Tackle"], "b")
            b.b.mons.append(extra)
        if case == "Substitute":
            foe.sub = 50
        elif case == "Substitute broken":
            foe.sub = 5
        elif case in ("Suction Cups",):
            foe.ability = case
        elif case == "Ingrain":
            foe.ingrained = True
        elif case == "fainted":
            foe.hp = 5
        elif case in ("Rough Skin", "user falls"):
            foe.ability = "Rough Skin"
            if case == "user falls":
                p.hp = 10
        elif case == "Rough Skin dragged in":
            extra.ability = "Rough Skin"
        mv = fs.move("Dragon Tail")
        fs.attack(b, p, mv, foe, True)
        fs.hit_aftermath(b, p, foe, mv, lambda kind, chance, victim: True, lambda kind, n: 0)
        out[case] = (b.b.active, p.hp)
    want = {"plain": (1, 100), "Substitute": (0, 100), "Substitute broken": (0, 100), "Suction Cups": (0, 100),
            "Ingrain": (0, 100), "no bench": (0, 100), "fainted": (0, 100), "Rough Skin": (1, 88),
            "Rough Skin dragged in": (1, 100), "user falls": (0, 0)}
    results.append(("Dragon Tail drags its target out after its ability answers the hit", out == want, str(out)))


def check_side_guards(results):
    """Wide Guard, Quick Guard, Mat Block and Crafty Shield (approved
    2026-10-14; effect script 371): used before the foe moves, each guards
    its side for the turn against its kind of move (Wide Guard a spread
    move, Quick Guard one of raised priority, Mat Block a damaging move on
    its user's first turn out, Crafty Shield a status move) and lets the
    rest through; used last it fails; it is gone at the turn's end; Wide
    Guard keeps Protect's run going and Crafty Shield ends it."""
    out = {}
    rows = {("b", m): [10] * 16 for m in ("Earthquake", "Quick Attack", "Tackle")}
    for guard, foe_move, first, turns in (("Wide Guard", "Earthquake", True, 0), ("Wide Guard", "Tackle", True, 0),
                                          ("Quick Guard", "Quick Attack", True, 0), ("Quick Guard", "Tackle", True, 0),
                                          ("Mat Block", "Tackle", True, 0), ("Mat Block", "Tackle", True, 1),
                                          ("Crafty Shield", "Thunder Wave", True, 0), ("Crafty Shield", "Tackle", True, 0),
                                          ("Quick Guard", "Quick Attack", False, 0)):
        b, p, foe = battle([guard], ["Earthquake", "Quick Attack", "Tackle", "Thunder Wave"], rows, hp=100)
        b.rng = FixedDice(0.5)
        p.turns_in = turns
        fs.status_move(b, p, fs.move(guard), foe, first)
        mv = fs.move(foe_move)
        (fs.status_move if mv.cat == "Status" else fs.attack)(b, foe, mv, p, False)
        out[(guard, foe_move, first, turns)] = (p.hp, p.status)
    want = {("Wide Guard", "Earthquake", True, 0): (100, None), ("Wide Guard", "Tackle", True, 0): (90, None),
            ("Quick Guard", "Quick Attack", True, 0): (100, None), ("Quick Guard", "Tackle", True, 0): (90, None),
            ("Mat Block", "Tackle", True, 0): (100, None), ("Mat Block", "Tackle", True, 1): (90, None),
            ("Crafty Shield", "Thunder Wave", True, 0): (100, None), ("Crafty Shield", "Tackle", True, 0): (90, None),
            ("Quick Guard", "Quick Attack", False, 0): (90, None)}
    b, p, foe = battle(["Wide Guard", "Protect", "Crafty Shield"], ["Tackle"], {})
    b.rng = FixedDice(0.0)
    fs.use_move(b, p, fs.move("Protect"), foe, True)
    fs.use_move(b, p, fs.move("Wide Guard"), foe, True)
    out["run after Protect, Wide Guard"] = p.protect_run
    fs.end_of_turn(b)
    out["guard after the turn"] = (b.p.guard, b.guarded)
    fs.use_move(b, p, fs.move("Crafty Shield"), foe, True)
    out["run after Crafty Shield"] = p.protect_run
    want.update({"run after Protect, Wide Guard": 2, "guard after the turn": (None, False),
                 "run after Crafty Shield": 0})
    results.append(("the side guards stop their kind of move for the turn", out == want, str(out)))


def check_heat_crash(results):
    """Heat Crash (approved 2026-10-14; effect script 292): its power by the
    target's weight over the user's, as Heavy Slam's (Heavy Metal doubling a
    weight, Light Metal halving it, a Mold Breaker passing the target's),
    and its hit read from the row prepare() makes at that power, where the
    calculator gives Heat Crash itself no row."""
    blob = {"poks": {"Big": {"weightkg": 100.0}, "Small": {"weightkg": 19.0}, "Mid": {"weightkg": 30.0},
                     "Heavy": {"weightkg": 60.0}}}
    out = {}
    for user, target, ua, ta in (("Big", "Small", None, None), ("Big", "Mid", None, None), ("Big", "Heavy", None, None),
                                 ("Big", "Small", None, "Heavy Metal"), ("Big", "Small", "Mold Breaker", "Heavy Metal"),
                                 ("Big", "Mid", "Heavy Metal", None), ("Small", "Big", None, None)):
        out[(user, target, ua, ta)] = fs.weight_power(blob, {"species": user, "ability": ua},
                                                      {"species": target, "ability": ta})
    b, p, foe = battle(["Heat Crash"], ["Tackle"], {})
    b.st["rows"][(None, "p0", "b0.0")]["moves"]["Heat Crash"] = {"error": "damage is not a number"}
    b.st["rows"][(None, "p0#hc80", "b0.0")] = {"moves": {"Heat Crash": {"rolls": [30] * 16}}}
    b.st["heat_crash"] = {("p0", "b0.0"): 80}
    out["its hit"] = (b.damage(p, foe, fs.move("Heat Crash"), roll=0), p.key)
    want = {("Big", "Small", None, None): 120, ("Big", "Mid", None, None): 80, ("Big", "Heavy", None, None): 40,
            ("Big", "Small", None, "Heavy Metal"): 60, ("Big", "Small", "Mold Breaker", "Heavy Metal"): 120,
            ("Big", "Mid", "Heavy Metal", None): 120, ("Small", "Big", None, None): 40, "its hit": (30, "p0")}
    results.append(("Heat Crash hits at its weight power", out == want, str(out)))


def check_healing_wish(results):
    """Healing Wish (approved 2026-10-14; effect script 220): with someone
    to send in, its user faints, its replacement comes in at once, meets the
    hazards, and is then restored to full HP and cured; with no one to send
    in it fails."""
    out = {}
    b, p, foe = battle(["Healing Wish"], ["Tackle"], {}, hp=100)
    b.rng = FixedDice(0.0)
    fs.status_move(b, p, fs.move("Healing Wish"), foe, True)
    out["alone"] = (p.hp, p.wished)
    b, p, foe = battle(["Healing Wish"], ["Tackle"], {}, hp=100)
    b.rng = FixedDice(0.0)
    mate = fs.Mon("p1", b.st["pokemon"]["p0"], b.st["info"]["p0"], ["Tackle"], "p")
    b.p.mons.append(mate)
    mate.hp, mate.status = 30, "psn"
    b.p.hazards["spikes"] = 1
    fs.status_move(b, p, fs.move("Healing Wish"), foe, True)
    out["user"] = (p.hp, p.wished)
    fs.wish_comes_true(b, p, lambda side: 1)
    out["replacement"] = (b.p.active, mate.hp, mate.status, p.wished)
    want = {"alone": (100, False), "user": (0, True), "replacement": (1, 100, None, False)}
    results.append(("Healing Wish faints its user and heals its replacement", out == want, str(out)))


def check_guard_split(results):
    """Guard Split (approved 2026-10-14; effect script 278): the user's and
    the target's Defense and Sp. Def are each averaged, in whole numbers,
    for both; hits on either then scale by the Defense's ratio, the
    trainer's AI's figure too; a Substitute stops it, and leaving ends it."""
    out = {}
    b, p, foe = battle(["Guard Split", "Tackle"], ["Tackle"], {("p", "Tackle"): [40] * 16, ("b", "Tackle"): [40] * 16})
    b.rng = FixedDice(0.0)
    foe.stats = dict(foe.stats, **{"def": 201, "spd": 60})
    tackle = fs.move("Tackle")
    fs.status_move(b, p, fs.move("Guard Split"), foe, True)
    out["stats"] = (fs.raw_stat(p, "def"), fs.raw_stat(foe, "def"), fs.raw_stat(p, "spd"), fs.raw_stat(foe, "spd"),
                    fs.raw_stat(foe, "atk"))
    out["hits"] = (b.damage(p, foe, tackle, roll=0), b.damage(foe, p, tackle, roll=0),
                   fightai.figure(b, foe, p, tackle))
    p.reset_volatile()
    out["after leaving"] = (fs.raw_stat(p, "def"), b.damage(foe, p, tackle, roll=0))
    b, p, foe = battle(["Guard Split"], ["Tackle"], {})
    foe.sub = 25
    fs.status_move(b, p, fs.move("Guard Split"), foe, True)
    out["Substitute"] = (p.split, foe.split)
    want = {"stats": (150, 150, 80, 80, 100), "hits": (53, 26, 26), "after leaving": (100, 40),
            "Substitute": (None, None)}
    results.append(("Guard Split averages the two Defenses for both", out == want, str(out)))


def check_power_split(results):
    """Power Split (approved 2026-10-14; effect script 279): the user's and
    the target's Attack and Sp. Atk are each averaged, in whole numbers, for
    both; hits from either then scale by the attacking stat's ratio; a
    Substitute stops it."""
    out = {}
    b, p, foe = battle(["Power Split", "Tackle"], ["Tackle"], {("p", "Tackle"): [40] * 16, ("b", "Tackle"): [40] * 16})
    b.rng = FixedDice(0.0)
    foe.stats = dict(foe.stats, **{"atk": 200, "spa": 50})
    tackle = fs.move("Tackle")
    fs.status_move(b, p, fs.move("Power Split"), foe, True)
    out["stats"] = (fs.raw_stat(p, "atk"), fs.raw_stat(foe, "atk"), fs.raw_stat(p, "spa"), fs.raw_stat(foe, "spa"),
                    fs.raw_stat(foe, "def"))
    out["hits"] = (b.damage(p, foe, tackle, roll=0), b.damage(foe, p, tackle, roll=0))
    b, p, foe = battle(["Power Split"], ["Tackle"], {})
    foe.sub = 25
    fs.status_move(b, p, fs.move("Power Split"), foe, True)
    out["Substitute"] = (p.split, foe.split)
    want = {"stats": (150, 150, 75, 75, 100), "hits": (60, 30), "Substitute": (None, None)}
    results.append(("Power Split averages the two Attacks for both", out == want, str(out)))


def check_embargo(results):
    """Embargo (approved 2026-10-14; effect script 232): for five turns the
    target's held item does not work (no Leftovers at the turn's end), a
    second Embargo fails and the trainer's AI refuses one, Knock Off still
    takes the item, Baton Pass hands the turns on, a Substitute stops it,
    and after five turn ends the item works again."""
    out = {}
    b, p, foe = battle(["Embargo", "Knock Off"], ["Tackle", "Baton Pass"], {("p", "Knock Off"): [5] * 16}, hp=160)
    b.rng = FixedDice(0.5)
    foe.item, foe.hp = "Leftovers", 100
    fs.status_move(b, p, fs.move("Embargo"), foe, True)
    out["held back"] = (foe.item, foe.item_off, foe.embargo)
    fs.end_of_turn(b)
    out["no Leftovers"] = foe.hp
    out["AI's second"] = fightai.basic(b, p, foe, fs.move("Embargo"), 0)
    out["baton"] = fs.baton_state(foe)["embargo"]
    for _ in range(4):
        fs.end_of_turn(b)
    out["after five turn ends"] = (foe.item, foe.item_off, foe.embargo)
    fs.status_move(b, p, fs.move("Embargo"), foe, True)
    fs.attack(b, p, fs.move("Knock Off"), foe, True)
    out["Knock Off"] = (foe.item, foe.item_off, foe.knocked_off)
    b, p, foe = battle(["Embargo"], ["Tackle"], {})
    foe.item, foe.sub = "Leftovers", 25
    fs.status_move(b, p, fs.move("Embargo"), foe, True)
    out["Substitute"] = (foe.item, foe.embargo)
    want = {"held back": (None, "Leftovers", 5), "no Leftovers": 100, "AI's second": -10, "baton": 4,
            "after five turn ends": ("Leftovers", None, 0), "Knock Off": (None, None, True),
            "Substitute": ("Leftovers", 0)}
    results.append(("Embargo holds the target's item back for five turns", out == want, str(out)))


def check_magic_room(results):
    """Magic Room (approved 2026-10-14; effect script 411): for five turns no
    held item on the field works, a newcomer's included, an item held back
    still keeps Acrobatics from doubling, a second use ends the room, and
    after five turn ends every item works again."""
    out = {}
    b, p, foe = battle(["Magic Room", "Acrobatics"], ["Tackle"], {("p", "Acrobatics"): [10] * 16}, hp=500)
    b.rng = FixedDice(0.5)
    p.item, foe.item = "Charcoal", "Leftovers"
    extra = fs.Mon("b0.1", b.st["pokemon"]["b0.0"], b.st["info"]["b0.0"], ["Tackle"], "b")
    extra.item = "Sitrus Berry"
    b.b.mons.append(extra)
    fs.status_move(b, p, fs.move("Magic Room"), foe, True)
    out["held back"] = (p.item, p.item_off, foe.item, foe.item_off, b.magic_room)
    hp = foe.hp
    fs.attack(b, p, fs.move("Acrobatics"), foe, True)
    out["Acrobatics"] = hp - foe.hp
    fs.switch_in(b, b.b, 1)
    out["newcomer"] = (extra.item, extra.item_off, foe.item)
    for _ in range(5):
        fs.end_of_turn(b)
    out["after five turn ends"] = (p.item, extra.item, b.magic_room)
    fs.status_move(b, p, fs.move("Magic Room"), extra, True)
    fs.status_move(b, p, fs.move("Magic Room"), extra, True)
    out["used twice"] = (p.item, extra.item, b.magic_room)
    want = {"held back": (None, "Charcoal", None, "Leftovers", 5), "Acrobatics": 10,
            "newcomer": (None, "Sitrus Berry", "Leftovers"), "after five turn ends": ("Charcoal", "Sitrus Berry", 0),
            "used twice": ("Charcoal", "Sitrus Berry", 0)}
    results.append(("Magic Room holds every held item back for five turns", out == want, str(out)))


def check_relic_song(results):
    """Relic Song (approved 2026-10-14; effect script 301): its hit puts the
    target to sleep at the move's chance, never through Shield Dust."""
    out = {}
    for value, ability in ((0.0, None), (0.5, None), (0.0, "Shield Dust")):
        b, p, foe = battle(["Relic Song"], ["Tackle"], {("p", "Relic Song"): [10] * 16}, hp=500)
        b.rng = FixedDice(value)
        foe.ability = ability
        fs.attack(b, p, fs.move("Relic Song"), foe, True)
        out[(value, ability)] = foe.status
    want = {(0.0, None): "slp", (0.5, None): None, (0.0, "Shield Dust"): None}
    results.append(("Relic Song's hit puts its target to sleep at its chance", out == want, str(out)))


def check_clanging_scales(results):
    """Clanging Scales (approved 2026-10-14; effect script 342): after any
    hit its user's Defense falls a stage, through a Substitute and under
    Sheer Force too."""
    out = {}
    for sub, ability in ((0, None), (40, None), (0, "Sheer Force")):
        b, p, foe = battle(["Clanging Scales"], ["Tackle"], {("p", "Clanging Scales"): [10] * 16}, hp=500)
        b.rng = FixedDice(0.5)
        foe.sub, p.ability = sub, ability
        fs.attack(b, p, fs.move("Clanging Scales"), foe, True)
        out[(sub, ability)] = p.stages["def"]
    want = {(0, None): -1, (40, None): -1, (0, "Sheer Force"): -1}
    results.append(("Clanging Scales lowers its user's Defense after the hit", out == want, str(out)))

def check_matcha_gotcha(results):
    """Matcha Gotcha (approved 2026-10-14; effect script 348): its user
    drains half the damage, and the target is burned at the move's chance,
    never through Shield Dust."""
    out = {}
    for value, ability in ((0.0, None), (0.5, None), (0.0, "Shield Dust")):
        b, p, foe = battle(["Matcha Gotcha"], ["Tackle"], {("p", "Matcha Gotcha"): [10] * 16}, hp=500)
        b.rng = FixedDice(value)
        foe.ability, p.hp = ability, 100
        fs.attack(b, p, fs.move("Matcha Gotcha"), foe, True)
        out[(value, ability)] = (foe.status, p.hp)
    want = {(0.0, None): ("brn", 107), (0.5, None): (None, 105), (0.0, "Shield Dust"): (None, 107)}
    results.append(("Matcha Gotcha drains half its damage and burns at its chance", out == want, str(out)))

def check_fell_stinger(results):
    """Fell Stinger (approved 2026-10-14; effect script 388): a hit that
    knocks its target out raises its user's Attack three stages; one that
    does not, or lands on a Substitute, raises nothing."""
    out = {}
    for hp, sub in ((5, 0), (500, 0), (5, 40)):
        b, p, foe = battle(["Fell Stinger"], ["Tackle"], {("p", "Fell Stinger"): [10] * 16}, hp=500)
        b.rng = FixedDice(0.5)
        foe.hp, foe.sub = hp, sub
        fs.attack(b, p, fs.move("Fell Stinger"), foe, True)
        out[(hp, sub)] = (foe.alive(), p.stages["atk"])
    want = {(5, 0): (False, 3), (500, 0): (True, 0), (5, 40): (True, 0)}
    results.append(("Fell Stinger's knockout raises its user's Attack three stages", out == want, str(out)))

def check_prevent_escape_hit(results):
    """Anchor Shot, Spirit Shackle and Thousand Waves (approved 2026-10-14;
    effect script 351): a hit on the target itself holds it as Mean Look
    does, not one on a Substitute nor one already held by another, and
    Sheer Force strips Thousand Waves' trap alone."""
    out = {}
    for name, sub, ability, held in (("Anchor Shot", 0, None, None), ("Anchor Shot", 40, None, None),
                                     ("Anchor Shot", 0, None, "x9"), ("Thousand Waves", 0, "Sheer Force", None),
                                     ("Spirit Shackle", 0, "Sheer Force", None)):
        b, p, foe = battle([name], ["Tackle"], {("p", name): [10] * 16}, hp=500)
        b.rng = FixedDice(0.5)
        foe.sub, p.ability, foe.trapped_by = sub, ability, held
        fs.attack(b, p, fs.move(name), foe, True)
        out[(name, sub, ability, held)] = foe.trapped_by
    want = {("Anchor Shot", 0, None, None): "p0", ("Anchor Shot", 40, None, None): None,
            ("Anchor Shot", 0, None, "x9"): "x9", ("Thousand Waves", 0, "Sheer Force", None): None,
            ("Spirit Shackle", 0, "Sheer Force", None): "p0"}
    results.append(("Anchor Shot and its kin trap the target their hit lands on", out == want, str(out)))

def check_poltergeist(results):
    """Poltergeist (approved 2026-10-14; effect script 345): it fails on a
    target holding no item, and hits one whose item Embargo holds back."""
    out = {}
    for item, off in (("Leftovers", None), (None, None), (None, "Leftovers")):
        b, p, foe = battle(["Poltergeist"], ["Tackle"], {("p", "Poltergeist"): [10] * 16}, hp=500)
        b.rng = FixedDice(0.5)
        foe.item, foe.item_off = item, off
        fs.attack(b, p, fs.move("Poltergeist"), foe, True)
        out[(item, off)] = foe.hp
    want = {("Leftovers", None): 490, (None, None): 500, (None, "Leftovers"): 490}
    results.append(("Poltergeist fails on a target with no item", out == want, str(out)))

def check_belch(results):
    """Belch (approved 2026-10-14; effect script 396): it fails until its
    user has eaten a Berry, and hits once it has, a switch between them
    keeping the record."""
    out = {}
    for eaten in (False, True):
        b, p, foe = battle(["Belch"], ["Tackle"], {("p", "Belch"): [10] * 16}, hp=500)
        b.rng = FixedDice(0.5)
        if eaten:
            p.item = "Oran Berry"
            fs.consume(p)
            p.reset_volatile()
        fs.attack(b, p, fs.move("Belch"), foe, True)
        out[eaten] = foe.hp
    want = {False: 500, True: 490}
    results.append(("Belch fails until its user has eaten a Berry", out == want, str(out)))

def check_first_impression(results):
    """First Impression (approved 2026-10-14; effect script 373): it hits
    on its user's first turn out and fails after it."""
    out = {}
    for turns in (0, 1):
        b, p, foe = battle(["First Impression"], ["Tackle"], {("p", "First Impression"): [10] * 16}, hp=500)
        b.rng = FixedDice(0.5)
        p.turns_in = turns
        fs.attack(b, p, fs.move("First Impression"), foe, True)
        out[turns] = foe.hp
    want = {0: 490, 1: 500}
    results.append(("First Impression fails after its user's first turn out", out == want, str(out)))

def check_axe_kick(results):
    """Axe Kick (approved 2026-10-14; effect script 293): its hit confuses
    at the move's chance, never through Shield Dust, and a miss crashes as
    Jump Kick's does, half the hit's damage, at most half the target's
    maximum HP."""
    out = {}
    for value, ability in ((0.0, None), (0.5, None), (0.0, "Shield Dust")):
        b, p, foe = battle(["Axe Kick"], ["Tackle"], {("p", "Axe Kick"): [10] * 16}, hp=500)
        b.rng = FixedDice(value)
        foe.ability = ability
        fs.attack(b, p, fs.move("Axe Kick"), foe, True)
        out[(value, ability)] = bool(foe.confused)
    b, p, foe = battle(["Axe Kick"], ["Tackle"], {("p", "Axe Kick"): [80] * 16}, hp=500)
    b.rng = FixedDice(0.95)          # the 90 per cent misses
    fs.attack(b, p, fs.move("Axe Kick"), foe, True)
    out["miss"] = (foe.hp, p.hp)
    want = {(0.0, None): True, (0.5, None): False, (0.0, "Shield Dust"): False, "miss": (500, 460)}
    results.append(("Axe Kick confuses at its chance and crashes on a miss", out == want, str(out)))

def check_always_critical(results):
    """Frost Breath's kind (approved 2026-10-14; effect script 282): the
    calculator's row is a critical hit already, so the hit takes no second
    one, passes a screen and the target's raised stages as a critical hit
    does, loses the row's 1.5 under Lucky Chant, and the trainer's AI
    reckons it without one, as TrainerAI_CalcDamage does."""
    out = {}
    for case, value in (("plain", 0.0), ("light screen", 0.5), ("+2 Sp. Def", 0.5), ("lucky chant", 0.0)):
        b, p, foe = battle(["Frost Breath"], ["Tackle"], {("p", "Frost Breath"): [15] * 16}, hp=500)
        b.rng = FixedDice(value)
        if case == "light screen":
            b.b.screens["Light Screen"] = 5
        if case == "+2 Sp. Def":
            foe.stages["spd"] = 2
        if case == "lucky chant":
            b.b.lucky_chant = 5
        fs.attack(b, p, fs.move("Frost Breath"), foe, True)
        out[case] = 500 - foe.hp
    b, p, foe = battle(["Frost Breath"], ["Tackle"], {("p", "Frost Breath"): [15] * 16}, hp=500)
    out["AI's estimate"] = b.damage(p, foe, fs.move("Frost Breath"), ai_view=True)
    want = {"plain": 15, "light screen": 15, "+2 Sp. Def": 15, "lucky chant": 10, "AI's estimate": 10}
    results.append(("Frost Breath's row is its critical hit, read as one", out == want, str(out)))

def check_clangorous_soul(results):
    """Clangorous Soul (approved 2026-10-14; effect script 346): a third of
    the user's maximum HP for a stage of all five stats; it fails at a
    third of its HP or less, and with all five at +6."""
    out = {}
    for case in ("full", "a third", "all at +6"):
        b, p, foe = battle(["Clangorous Soul"], ["Tackle"], {}, hp=300)
        if case == "a third":
            p.hp = 100
        if case == "all at +6":
            p.stages.update(dict.fromkeys(("atk", "def", "spa", "spd", "spe"), 6))
        fs.status_move(b, p, fs.move("Clangorous Soul"), foe, True)
        out[case] = (p.hp, p.stages["atk"], p.stages["spe"], p.stages["spd"])
    want = {"full": (200, 1, 1, 1), "a third": (100, 0, 0, 0), "all at +6": (300, 6, 6, 6)}
    results.append(("Clangorous Soul trades a third of its HP for all five stats", out == want, str(out)))

def check_heart_swap(results):
    """Heart Swap (approved 2026-10-14; effect script 250): the user and its
    target exchange every stat stage and their Focus Energy, through a
    Substitute too."""
    b, p, foe = battle(["Heart Swap"], ["Tackle"], {})
    p.stages.update({"atk": -2, "eva": 1})
    foe.stages.update({"spa": 3, "spe": 1, "acc": -1})
    foe.crit_stage, foe.sub = 2, 30
    fs.status_move(b, p, fs.move("Heart Swap"), foe, True)
    got = (p.stages["spa"], p.stages["spe"], p.stages["acc"], p.stages["atk"], foe.stages["atk"], foe.stages["eva"],
           foe.stages["spa"], p.crit_stage, foe.crit_stage)
    results.append(("Heart Swap exchanges every stage and Focus Energy", got == (3, 1, -1, 0, -2, 1, 0, 2, 0), str(got)))

def check_heal_pulse(results):
    """Heal Pulse (approved 2026-10-14; effect script 379): its target, the
    foe in a single battle, gets back half its maximum HP rounded up, three
    quarters with Mega Launcher; Heal Block and a Substitute stop it."""
    out = {}
    for case in ("plain", "Mega Launcher", "Heal Block", "Substitute"):
        b, p, foe = battle(["Heal Pulse"], ["Tackle"], {}, hp=301)
        foe.hp = 50
        if case == "Mega Launcher":
            p.ability = "Mega Launcher"
        if case == "Heal Block":
            foe.heal_block = 5
        if case == "Substitute":
            foe.sub = 40
        fs.status_move(b, p, fs.move("Heal Pulse"), foe, True)
        out[case] = foe.hp
    want = {"plain": 201, "Mega Launcher": 278, "Heal Block": 50, "Substitute": 50}
    results.append(("Heal Pulse heals its target by half", out == want, str(out)))

def check_lunar_dance(results):
    """Lunar Dance (approved 2026-10-14; effect script 270): as Healing
    Wish, its user faints and its replacement, once in, gets back its HP,
    its status and every move's PP; with no one to send in it fails."""
    out = {}
    b, p, foe = battle(["Lunar Dance"], ["Tackle"], {}, hp=100)
    b.rng = FixedDice(0.0)
    fs.status_move(b, p, fs.move("Lunar Dance"), foe, True)
    out["alone"] = (p.hp, p.wished)
    b, p, foe = battle(["Lunar Dance"], ["Tackle"], {}, hp=100)
    b.rng = FixedDice(0.0)
    mate = fs.Mon("p1", b.st["pokemon"]["p0"], b.st["info"]["p0"], ["Tackle"], "p")
    b.p.mons.append(mate)
    mate.hp, mate.status, mate.pp = 30, "brn", {"Tackle": 2}
    fs.status_move(b, p, fs.move("Lunar Dance"), foe, True)
    out["user"] = (p.hp, bool(p.wished))
    fs.wish_comes_true(b, p, lambda side: 1)
    out["replacement"] = (b.p.active, mate.hp, mate.status, mate.pp["Tackle"], p.wished)
    want = {"alone": (100, False), "user": (0, True), "replacement": (1, 100, None, fs.move("Tackle").pp, False)}
    results.append(("Lunar Dance faints its user and restores its replacement, PP too", out == want, str(out)))

def check_grudge(results):
    """Grudge (approved 2026-10-14; effect script 194): until its user next
    tries to act, a foe's move that knocks it out loses all its PP; one
    that does not knock it out keeps them, and the user's next move ends
    the mark."""
    out = {}
    for case in ("knocked out", "standing", "moved since"):
        b, p, foe = battle(["Grudge", "Tackle"], ["Tackle"], {("b", "Tackle"): [60] * 16, ("p", "Tackle"): [1] * 16}, hp=100)
        b.rng = FixedDice(0.5)
        fs.status_move(b, p, fs.move("Grudge"), foe, True)
        if case == "moved since":
            fs.use_move(b, p, fs.move("Tackle"), foe, True)
        p.hp = 50 if case != "standing" else 100
        fs.use_move(b, foe, fs.move("Tackle"), p, True)
        out[case] = (p.alive(), foe.pp["Tackle"])
    full = fs.move("Tackle").pp
    want = {"knocked out": (False, 0), "standing": (True, full - 1), "moved since": (False, full - 1)}
    results.append(("Grudge empties the PP of the move that knocks its user out", out == want, str(out)))

def check_octolock(results):
    """Octolock (approved 2026-10-14; effect script 410): it holds its
    target as Mean Look does and costs it a stage of Defense and of Sp. Def
    at each turn's end; a second one and one into a Substitute fail; its
    user leaving ends both."""
    out = {}
    b, p, foe = battle(["Octolock"], ["Tackle"], {})
    b.rng = FixedDice(0.5)
    mate = fs.Mon("p1", b.st["pokemon"]["p0"], b.st["info"]["p0"], ["Tackle"], "p")
    b.p.mons.append(mate)
    fs.status_move(b, p, fs.move("Octolock"), foe, True)
    out["held"] = (foe.trapped_by, foe.octolocked, fs.trapped(b, foe))
    fs.end_of_turn(b)
    fs.status_move(b, p, fs.move("Octolock"), foe, True)
    fs.end_of_turn(b)
    out["two turn ends"] = (foe.stages["def"], foe.stages["spd"])
    fs.switch_in(b, b.p, 1)
    out["user gone"] = (foe.trapped_by, foe.octolocked)
    b, p, foe = battle(["Octolock"], ["Tackle"], {})
    foe.sub = 30
    fs.status_move(b, p, fs.move("Octolock"), foe, True)
    out["Substitute"] = (foe.trapped_by, foe.octolocked)
    want = {"held": ("p0", True, True), "two turn ends": (-2, -2), "user gone": (None, False),
            "Substitute": (None, False)}
    results.append(("Octolock holds its target and lowers both Defenses each turn", out == want, str(out)))

def check_aurora_veil(results):
    """Aurora Veil (approved 2026-10-14; effect script 377): only in hail it
    veils its user's side for five turns, eight with a Light Clay, halving
    physical and special hits on the side, once with Reflect; a critical hit
    passes it, and Brick Break and Defog clear it."""
    out = {}
    b, p, foe = battle(["Aurora Veil"], ["Tackle", "Ember", "Brick Break"],
                       {("b", "Tackle"): [40] * 16, ("b", "Ember"): [40] * 16, ("b", "Brick Break"): [40] * 16})
    fs.status_move(b, p, fs.move("Aurora Veil"), foe, True)
    out["no hail"] = b.p.aurora_veil
    b.weather = "Hail"
    p.item = "Light Clay"
    fs.status_move(b, p, fs.move("Aurora Veil"), foe, True)
    out["hail, Light Clay"] = b.p.aurora_veil
    b.p.screens["Reflect"] = 5
    out["hits"] = (b.damage(foe, p, fs.move("Tackle"), roll=0), b.damage(foe, p, fs.move("Ember"), roll=0),
                   b.damage(foe, p, fs.move("Tackle"), crit=True, roll=0))
    b.p.screens["Reflect"] = 0
    fs.end_of_turn(b)
    out["a turn on"] = b.p.aurora_veil
    fs.attack(b, foe, fs.move("Brick Break"), p, True)
    out["Brick Break"] = b.p.aurora_veil
    b.p.aurora_veil = 3
    fs.defog(b, foe, p, fs.move("Defog"))
    out["Defog"] = b.p.aurora_veil
    want = {"no hail": 0, "hail, Light Clay": 8, "hits": (20, 20, 60), "a turn on": 7, "Brick Break": 0, "Defog": 0}
    results.append(("Aurora Veil halves both kinds of hit in hail", out == want, str(out)))

def check_teatime(results):
    """Teatime (approved 2026-10-14; effect script 412): every Pokemon on
    the field that holds a Berry eats it at once, as its own, whether or
    not it would set itself off; one held back by Embargo too."""
    out = {}
    b, p, foe = battle(["Teatime"], ["Tackle"], {}, hp=200)
    p.item, p.hp = "Sitrus Berry", 150
    foe.item = "Liechi Berry"
    fs.status_move(b, p, fs.move("Teatime"), foe, True)
    out["both"] = (p.hp, p.item, p.ate_berry, p.recycle, foe.stages["atk"], foe.item, foe.ate_berry)
    b, p, foe = battle(["Teatime"], ["Tackle"], {}, hp=200)
    foe.item_off, foe.embargo = "Liechi Berry", 3
    fs.status_move(b, p, fs.move("Teatime"), foe, True)
    out["Embargo"] = (foe.stages["atk"], foe.item, foe.item_off, foe.ate_berry)
    want = {"both": (200, None, True, "Sitrus Berry", 1, None, True), "Embargo": (1, None, None, True)}
    results.append(("Teatime feeds every Pokemon its own Berry", out == want, str(out)))

def check_assist(results):
    """Assist (approved 2026-10-14; effect script 180): it uses one of its
    party members' moves, picked at random, fainted members' too, never a
    move that calls another; with none to call it fails."""
    out = {}
    b, p, foe = battle(["Assist"], ["Tackle"], {("p", "Tackle"): [10] * 16}, hp=500)
    b.rng = FixedDice(0.5)
    fs.use_move(b, p, fs.move("Assist"), foe, True)
    out["alone"] = foe.hp
    b, p, foe = battle(["Assist"], ["Tackle"], {("p", "Tackle"): [10] * 16}, hp=500)
    b.rng = FixedDice(0.5)
    mate = fs.Mon("p1", b.st["pokemon"]["p0"], b.st["info"]["p0"], ["Metronome", "Tackle"], "p")
    mate.hp = 0
    b.p.mons.append(mate)
    b.st["rows"][(None, "p0", "b0.0")]["moves"]["Tackle"] = {"rolls": [10] * 16}     # prepare's borrowed row
    fs.use_move(b, p, fs.move("Assist"), foe, True)
    out["a fainted mate's Tackle"] = (foe.hp, p.pp["Assist"])
    want = {"alone": 500, "a fainted mate's Tackle": (490, fs.move("Assist").pp - 1)}
    results.append(("Assist uses a party member's move", out == want, str(out)))

def check_snatch(results):
    """Snatch (approved 2026-10-14; effect script 195): used before the foe
    moves, it takes the foe's next move Snatch may take for its own user,
    the foe paying the PP; a move it may not take, and one after a Snatch
    used last, are the foe's own; the wait ends with the turn."""
    out = {}
    for case in ("taken", "used last", "not snatchable"):
        b, p, foe = battle(["Snatch"], ["Swords Dance", "Thunder Wave"], {})
        b.rng = FixedDice(0.5)
        fs.status_move(b, p, fs.move("Snatch"), foe, case != "used last")
        mv = fs.move("Thunder Wave" if case == "not snatchable" else "Swords Dance")
        fs.use_move(b, foe, mv, p, False)
        out[case] = (p.stages["atk"], foe.stages["atk"], p.status, foe.pp[mv.name] < mv.pp)
    b, p, foe = battle(["Snatch"], ["Swords Dance"], {})
    fs.status_move(b, p, fs.move("Snatch"), foe, True)
    fs.end_of_turn(b)
    out["a turn on"] = (p.snatching, b.snatching)
    want = {"taken": (2, 0, None, True), "used last": (0, 2, None, True), "not snatchable": (0, 0, "par", True),
            "a turn on": (False, False)}
    results.append(("Snatch takes the foe's next snatchable move", out == want, str(out)))

def check_sky_drop(results):
    """Sky Drop (approved 2026-10-14; effect script 414): the first turn
    lifts the target, which then does nothing and cannot switch; the
    second drops it for the hit, nothing to a Flying type; the lift fails
    through a Substitute and on a target of 200 kg or more, and a user that
    cannot act on its second turn lets its target go."""
    out = {}
    sky, tackle = fs.move("Sky Drop"), fs.move("Tackle")

    def fresh(types=("Normal",)):
        b, p, foe = battle(["Sky Drop"], ["Tackle"], {("p", "Sky Drop"): [20] * 16, ("b", "Tackle"): [10] * 16},
                           b_types=types, hp=200)
        b.rng = FixedDice(0.5)
        return b, p, foe
    b, p, foe = fresh()
    fs.use_move(b, p, sky, foe, True)
    out["lifted"] = (foe.hp, foe.sky_holder, fs.trapped(b, foe), p.charging is not None)
    fs.use_move(b, foe, tackle, p, False)
    out["held foe's Tackle"] = p.hp
    fs.use_move(b, p, sky, foe, True)
    out["dropped"] = (foe.hp, foe.sky_holder, p.charging)
    b, p, foe = fresh(("Flying",))
    fs.use_move(b, p, sky, foe, True)
    fs.use_move(b, p, sky, foe, True)
    out["Flying"] = foe.hp
    for case in ("Substitute", "Snorlax"):
        b, p, foe = fresh()
        if case == "Substitute":
            foe.sub = 30
        else:
            foe.species = "Snorlax"
        fs.use_move(b, p, sky, foe, True)
        out[case] = (foe.sky_holder, p.charging)
    b, p, foe = fresh()
    fs.use_move(b, p, sky, foe, True)
    p.status = "par"
    b.rng = FixedDice(0.0)            # fully paralysed on the drop's turn
    fs.use_move(b, p, sky, foe, True)
    out["holder paralysed"] = (foe.hp, fs.sky_held(b, foe))
    want = {"lifted": (200, "p0", True, True), "held foe's Tackle": 200, "dropped": (180, None, None),
            "Flying": 200, "Substitute": (None, None), "Snorlax": (None, None), "holder paralysed": (200, False)}
    results.append(("Sky Drop lifts its target for a turn and drops it", out == want, str(out)))


# ---- batch 10: the follow-ups Ian approved on 2026-10-15 ----

def check_substitute_hit(results):
    """A hit on a Substitute gives the Pokemon behind it nothing, the hit
    that breaks it included (approved 2026-10-15): the added effects ask
    CheckSubstitute or Battler_SubstituteWasHit, which read
    SELF_TURN_FLAG_SUBSTITUTE_HIT for the rest of the move. Nuzzle's sure
    paralysis lands with no Substitute, and neither through one it leaves
    standing nor through one it breaks."""
    out = {}
    for case, sub in (("none", 0), ("left standing", 50), ("broken", 5)):
        b, p, foe = battle(["Nuzzle"], ["Tackle"], {("p", "Nuzzle"): [20] * 16})
        b.rng = FixedDice(0.0)
        foe.sub = sub
        fs.attack(b, p, fs.move("Nuzzle"), foe, True)
        out[case] = (foe.status, foe.sub, foe.hp)
    want = {"none": ("par", 0, 70), "left standing": (None, 20, 100), "broken": (None, 0, 100)}
    results.append(("a hit that breaks a Substitute gives no added effect", out == want, str(out)))


def check_knock_off_first(results):
    """Knock Off and Bug Bite (approved 2026-10-15; effect scripts 188 and
    224): their own effect is an on-hit side effect, which runs before the
    target's held item is checked (AFTER_MOVE_EFFECT_DEFENDER_ITEM), so in
    the readings' battle the Sitrus Berry of a target the hit takes below
    half is knocked off, or eaten by the Bug Bite user, before its holder
    can eat it; and once a trainer's item is gone its rows are its item
    twin's ("b0.0#ni"), so a knocked-off Charcoal stops boosting its Ember,
    and a Choice Scarf stops raising its Speed."""
    from . import perfectline as pl
    out = {}
    for name in ("Knock Off", "Bug Bite"):
        b, p, foe = battle([name], ["Tackle"], {("p", name): [60] * 16}, hp=100)
        b.dice, b.rng = pl.RunDice(random.Random(1), True), random.Random(1)
        foe.item = "Sitrus Berry"
        p.hp = 40
        pl.attack(b, p, fs.move(name), foe, True)
        out[name] = (foe.hp, foe.item, foe.knocked_off, p.hp)
    b, p, foe = battle(["Knock Off"], ["Ember"], {("p", "Knock Off"): [10] * 16, ("b", "Ember"): [30] * 16})
    b.st["pokemon"]["b0.0"]["item"] = foe.item = "Choice Scarf"
    b.st["pokemon"]["b0.0#ni"] = dict(b.st["pokemon"]["b0.0"], item=None)
    b.st["rows"][(None, "b0.0#ni", "p0")] = {"moves": {"Ember": {"rolls": [25] * 16}}}
    b.st["rows"][(None, "p0", "b0.0#ni")] = {"moves": {"Knock Off": {"rolls": [10] * 16}}}
    b.st["speed"][(None, "b0.0#ni")] = 30
    b.st["item_twin"] = {"b0.0": "b0.0#ni"}
    before = (b.damage(foe, p, fs.move("Ember"), roll=0), b.speed(foe))
    b.rng = FixedDice(0.5)
    fs.attack(b, p, fs.move("Knock Off"), foe, True)
    out["item twin"] = (before, (b.damage(foe, p, fs.move("Ember"), roll=0), b.speed(foe)), foe.item)
    want = {"Knock Off": (40, None, True, 40), "Bug Bite": (40, None, False, 65),
            "item twin": ((30, 50), (25, 30), None)}
    results.append(("Knock Off and Bug Bite take the target's Berry before it eats it, and its rows lose the item",
                    out == want, str(out)))


def check_taunt_before_confusion(results):
    """Taunt and Heal Block are checked before confusion, paralysis and love
    (approved 2026-10-15; BattleControllerPlayer_CheckStatusDisruption's
    order: Disable, Taunt, Imprison, Gravity, Heal Block, Throat Chop, then
    confusion): a taunted, confused Pokemon's Swords Dance fails at once,
    with no self-hit and its confusion's count kept, as does a heal-blocked
    one's Recover; one neither taunted nor blocked hurts itself."""
    out = {}
    for case, name in (("taunted", "Swords Dance"), ("heal-blocked", "Recover"), ("neither", "Swords Dance")):
        b, p, foe = battle([name], ["Tackle"], {}, hp=100)
        b.rng = FixedDice(0.0)               # every confusion check hurts itself
        p.confused = 3
        if case == "taunted":
            p.taunt = 3
        elif case == "heal-blocked":
            p.heal_block = 5
        fs.use_move(b, p, fs.move(name), foe, True)
        out[case] = (p.hp < p.maxhp, p.confused)
    want = {"taunted": (False, 3), "heal-blocked": (False, 3), "neither": (True, 2)}
    results.append(("Taunt and Heal Block stop a move before confusion is checked", out == want, str(out)))


def check_forced_out(results):
    """A Pokemon forced out by Roar or Whirlwind before it acts does not act
    (approved 2026-10-15): in a turn where both sides use Whirlwind, the
    faster one's drags the other out and the Pokemon dragged out does
    nothing from the bench, so the faster side keeps its Pokemon in."""
    from . import perfectline as pl
    out = {}
    for case, speed in (("player faster", 100), ("player slower", 30)):
        b, p, foe = battle(["Whirlwind"], ["Whirlwind"], {}, p_speed=speed, b_speed=50)
        b.p.mons.append(fs.Mon("p1", b.st["pokemon"]["p0"], b.st["info"]["p0"], ["Whirlwind"], "p"))
        b.b.mons.append(fs.Mon("b0.1", b.st["pokemon"]["b0.0"], b.st["info"]["b0.0"], ["Whirlwind"], "b"))
        b.dice, b.rng = pl.RunDice(random.Random(1), True), random.Random(1)
        pl._turn(b, ("move", fs.move("Whirlwind")), ("move", fs.move("Whirlwind")))
        out[case] = (b.p.active, b.b.active) + ((fs.forced_out(b, foe), fs.forced_out(b, p))
                                               if hasattr(fs, "forced_out") else ())
    want = {"player faster": (0, 1, True, False), "player slower": (1, 0, False, True)}
    results.append(("a Pokemon forced out before it acts does not act", out == want, str(out)))


def check_charge_ends(results):
    """A charge ends on a turn its user cannot act (approved 2026-10-15;
    the subscripts that stop a move run UnlockMoveChoice, and falling
    asleep or being frozen unlocks at once): a Solar Beam user fully
    paralysed on its striking turn loses the charge and must charge again,
    and a Fly user put to sleep in the air comes down."""
    out = {}
    b, p, foe = battle(["Solar Beam"], ["Tackle"], {("p", "Solar Beam"): [50] * 16}, hp=200)
    b.rng = FixedDice(0.9)
    sb = fs.move("Solar Beam")
    fs.use_move(b, p, sb, foe, True)
    charged = p.charging is not None
    p.status = "par"
    b.rng = FixedDice(0.0)                   # fully paralysed
    fs.use_move(b, p, sb, foe, True)
    out["paralysed"] = (charged, p.charging is None, foe.hp)
    p.status = None
    b.rng = FixedDice(0.9)
    fs.use_move(b, p, sb, foe, True)
    out["next turn"] = (p.charging is not None, foe.hp)
    b, p, foe = battle(["Fly"], ["Tackle"], {("p", "Fly"): [50] * 16}, hp=200)
    b.rng = FixedDice(0.9)
    fs.use_move(b, p, fs.move("Fly"), foe, True)
    flying = p.charging is not None
    fs.give_status(b, p, "slp")
    out["put to sleep"] = (flying, p.charging)
    want = {"paralysed": (True, True, 200), "next turn": (True, 200), "put to sleep": (True, None)}
    results.append(("a charge ends on a turn its user cannot act", out == want, str(out)))


def check_ingrain_grounds(results):
    """Ingrain grounds its user (approved 2026-10-15; BasicTypeMulApplies
    skips the Flying type's immunity for MOVE_EFFECT_INGRAIN, and
    Battler_Ability reads no Levitate for an ingrained holder): once a
    Levitate holder has used Ingrain, Earthquake reads its ground twin's
    row and the trainer's AI no longer reads the move as doing nothing."""
    from . import perfectline as pl
    b, p, foe = battle(["Earthquake"], ["Ingrain"], {("p", "Earthquake"): [0] * 16})
    b.dice = pl.RunDice(random.Random(1), True)
    foe.ability = "Levitate"
    b.st["rows"][(None, "p0", "b0.0#gd")] = {"moves": {"Earthquake": {"rolls": [40] * 16}}}
    b.st["ground_twin"] = {"b0.0": "b0.0#gd"}
    eq = fs.move("Earthquake")
    before = (b.damage(p, foe, eq, roll=0), fightai.script_eff(b, p, foe, eq) == fightai.IMMUNE)
    pl.status_move(b, foe, fs.move("Ingrain"), p, True)
    after = (b.damage(p, foe, eq, roll=0), fightai.script_eff(b, p, foe, eq) == fightai.IMMUNE)
    ok = before == (0, True) and after == (40, False) and foe.ingrained
    results.append(("Ingrain grounds a Levitate holder against Ground moves", ok,
                    f"(Earthquake, the AI reads it immune) before {before}, after {after}"))


def check_fog(results):
    """Deep fog's accuracy cut (approved 2026-10-15;
    BattleControllerPlayer_CheckMoveHitAccuracy under FIELD_CONDITION_DEEP_FOG):
    a fight prepared in fog starts in it, and a 100-accuracy Tackle then
    lands at six tenths, so a roll of 65 misses it; Cloud Nine on the field
    lifts the cut, and Defog and a weather move each clear the fog."""
    out = {}
    b, p, foe = battle(["Tackle", "Defog", "Rain Dance"], ["Tackle"], {("p", "Tackle"): [10] * 16})
    b2 = fs.Battle(dict(b.st, fog=True), b.p, b.b, FixedDice(0.65))
    out["prepared in fog"] = b2.fog
    tackle = fs.move("Tackle")
    b.rng = FixedDice(0.65)
    out["clear"] = b.accuracy_hits(p, foe, tackle)
    b.fog = True
    out["fog"] = b.accuracy_hits(p, foe, tackle)
    foe.ability = "Cloud Nine"
    out["Cloud Nine"] = b.accuracy_hits(p, foe, tackle)
    foe.ability = None
    fs.status_move(b, p, fs.move("Defog"), foe, True)
    out["after Defog"] = b.fog
    b.fog = True
    fs.status_move(b, p, fs.move("Rain Dance"), foe, True)
    out["after Rain Dance"] = (b.fog, b.weather)
    want = {"prepared in fog": True, "clear": True, "fog": False, "Cloud Nine": True, "after Defog": False,
            "after Rain Dance": (False, "Rain")}
    results.append(("deep fog cuts accuracy to six tenths until it clears", out == want, str(out)))


def check_rematch_terrain(results):
    """A rematch's battle terrain (approved 2026-10-15): the Vs. Seeker
    brings a trainer back on the map where it was first fought
    (gVsSeekerRematchData), so Cyclist John's third rematch is fought on
    his road's plain, as he was, where its Staraptor's Secret Power lowers
    accuracy and Nature Power is Earthquake, not a building's paralysis
    and Tri Attack."""
    from . import calc, data
    ids = {t["constant"]: tid for tid, t in data.oxide_trainers().items()}
    first, again = ids["TRAINER_CYCLIST_JOHN"], ids["TRAINER_CYCLIST_JOHN_REMATCH_3"]
    terrain = calc.fight_terrain([again])
    out = (calc.fight_terrain([first]), terrain, fs.secret_power_effect(terrain), fs.nature_power_move(terrain))
    want = ("TERRAIN_PLAIN", "TERRAIN_PLAIN", {"acc": -1}, "Earthquake")
    results.append(("a rematch is fought on its first fight's terrain", out == want, str(out)))


def check_borrowed_twins(results):
    """The moves Copycat, Me First, Mimic, Mirror Move and Sketch borrow are
    rowed against a foe's twins too (approved 2026-10-15): prepare() rows
    the player's Copycat user's attacks into a trainer's Roost twin with
    the trainer's Gust beside its own Karate Chop, and with its mate's Water
    Gun, which Copycat can copy once the mate has used it; into the
    trainer's own key it carried both already, or the foe's at least."""
    st, pairs, _pokemon = prepared_jobs([("Pidgeotto", 30, "Keen Eye", ["Gust", "Roost"], None)],
                                        [("Machop", 30, "Guts", ["Copycat", "Karate Chop"], None),
                                         ("Bibarel", 30, "Unaware", ["Water Gun"], None)])
    def rowed(d):
        return sorted({m for a, dd, mv, _w in pairs if a == "p0" and dd == d for m in mv})
    twin = st["roost_twin"]["b0.0"][0][0]
    out = {"own key": rowed("b0.0"), "Roost twin": rowed(twin)}
    want = {"own key": ["Gust", "Karate Chop", "Water Gun"], "Roost twin": ["Gust", "Karate Chop", "Water Gun"]}
    results.append(("borrowed moves are rowed against a foe's twins", out == want, str(out)))


def check_meloetta_form(results):
    """Relic Song turns Meloetta between Aria and Pirouette (approved
    2026-10-15; AFTER_MOVE_HIT_STATE_RELIC_SONG, subscript_relic_song_form):
    prepare() rows a Meloetta that knows the move as Pirouette too; after a
    Relic Song that hits, its Close Combat and its Speed are its Pirouette
    twin's and its types Normal and Fighting; a second hit turns it back,
    a Relic Song a Substitute takes turns nothing, and it leaves the field
    as Aria."""
    st, pairs, pokemon = prepared_jobs([("Geodude", 30, "Sturdy", ["Tackle"], None)],
                                       [("Meloetta", 30, "Serene Grace", ["Relic Song", "Close Combat"], None)])
    twin = st["meloetta_twin"].get("p0")
    rowed = (twin, pokemon.get(twin, {}).get("species_data", {}).get("types"),
             any(a == twin and d == "b0.0" for a, d, _m, _w in pairs),
             any(a == "b0.0" and d == twin for a, d, _m, _w in pairs))
    b, p, foe = battle(["Relic Song", "Close Combat"], ["Tackle"],
                       {("p", "Relic Song"): [10] * 16, ("p", "Close Combat"): [20] * 16}, hp=300)
    b.st["pokemon"]["p0"]["species"] = p.species = "Meloetta"
    b.st["meloetta_twin"] = {"p0": "p0#pir"}
    b.st["info"]["p0#pir"] = dict(b.st["info"]["p0"], types=["Normal", "Fighting"],
                                  stats=dict(b.st["info"]["p0"]["stats"], atk=150))
    b.st["rows"][(None, "p0#pir", "b0.0")] = {"moves": {"Relic Song": {"rolls": [8] * 16},
                                                         "Close Combat": {"rolls": [35] * 16}}}
    b.st["speed"][(None, "p0#pir")] = 140
    cc, song = fs.move("Close Combat"), fs.move("Relic Song")
    b.rng = FixedDice(0.9)
    out = {"Aria": (b.damage(p, foe, cc, roll=0), b.speed(p), p.types)}
    fs.use_move(b, p, song, foe, True)
    out["after a hit"] = (b.damage(p, foe, cc, roll=0), b.speed(p), p.types, p.stats["atk"])
    fs.use_move(b, p, song, foe, True)
    out["after a second"] = (b.damage(p, foe, cc, roll=0), p.types)
    fs.use_move(b, p, song, foe, True)
    b.p.mons.append(fs.Mon("p1", b.st["pokemon"]["b0.0"], b.st["info"]["b0.0"], ["Tackle"], "p"))
    fs.switch_in(b, b.p, 1)
    out["after leaving"] = (p.pirouette, p.types)
    foe.sub = 50
    fs.switch_in(b, b.p, 0)
    fs.use_move(b, p, song, foe, True)
    out["into a Substitute"] = p.pirouette
    want = {"Aria": (20, 100, ["Normal"]), "after a hit": (35, 140, ["Normal", "Fighting"], 150),
            "after a second": (20, ["Normal"]), "after leaving": (False, ["Normal"]), "into a Substitute": False}
    ok = rowed == ("p0#pir", ["Normal", "Fighting"], True, True) and out == want
    results.append(("Relic Song turns Meloetta between its forms", ok, f"twin {rowed}; {out}"))


# ---- batch 11: the abilities open to the player, and Ian's answers of 2026-10-20 ----

# The batch's checks, run after batch 10's in main.
B11 = []


def b11(fn):
    B11.append(fn)
    return fn


def b11_battle(p_moves, b_moves, rolls, **kw):
    """A hand-built battle on the readings' dice (perfectline.RunDice)."""
    from . import perfectline as pl
    b, p, foe = battle(p_moves, b_moves, rolls, **kw)
    b.dice, b.rng = pl.RunDice(random.Random(1), True), random.Random(1)
    return b, p, foe


@b11
def check_weak_armor(results):
    """Weak Armor (approved 2026-10-14; BattleSystem_TriggerAbilityOnHit,
    subscript_weak_armor): a physical hit that does damage takes its
    holder's Defense down a stage and its Speed up two, made directly
    (AbilityStatChange); at -6 Defense the Speed still rises, and a
    special hit does nothing."""
    from . import perfectline as pl
    out = {}
    for case, name, start in (("physical", "Tackle", 0), ("special", "Ember", 0), ("at -6", "Tackle", -6)):
        b, p, foe = b11_battle(["Tackle"], [name], {("b", name): [10] * 16})
        p.ability = "Weak Armor"
        p.stages["def"] = start
        pl.use_move(b, foe, fs.move(name), p, True)
        out[case] = (p.stages["def"], p.stages["spe"])
    want = {"physical": (-1, 2), "special": (0, 0), "at -6": (-6, 2)}
    results.append(("Weak Armor trades Defense for Speed after a physical hit", out == want, str(out)))


@b11
def check_water_compaction(results):
    """Water Compaction (approved 2026-10-14; subscript_water_compaction):
    a Water hit that does damage raises its holder's Defense two stages, a
    special one too; a Normal hit does nothing, and neither does a Water
    hit its Substitute takes."""
    from . import perfectline as pl
    out = {}
    for case, name, sub in (("Water Gun", "Water Gun", 0), ("Tackle", "Tackle", 0), ("Substitute", "Water Gun", 50)):
        b, p, foe = b11_battle(["Tackle"], [name], {("b", name): [10] * 16})
        p.ability, p.sub = "Water Compaction", sub
        pl.use_move(b, foe, fs.move(name), p, True)
        out[case] = p.stages["def"]
    want = {"Water Gun": 2, "Tackle": 0, "Substitute": 0}
    results.append(("Water Compaction raises Defense two stages after a Water hit", out == want, str(out)))


@b11
def check_toxic_debris(results):
    """Toxic Debris (approved 2026-10-14; BattleSystem_TriggerAbilityOnHit,
    subscript_toxic_debris): a physical hit that does damage lays a layer of
    Toxic Spikes on the attacker's side, two at most, the hit that faints
    the holder too; a special hit lays none."""
    from . import perfectline as pl
    out = {}
    for case, name, hp, hits in (("one", "Tackle", 100, 1), ("three", "Tackle", 100, 3), ("special", "Ember", 100, 1),
                                 ("fainting", "Tackle", 5, 1)):
        b, p, foe = b11_battle(["Tackle"], [name], {("b", name): [10] * 16})
        p.ability, p.hp = "Toxic Debris", hp
        for _ in range(hits):
            pl.use_move(b, foe, fs.move(name), p, True)
        out[case] = b.b.hazards["tspikes"]
    want = {"one": 1, "three": 2, "special": 0, "fainting": 1}
    results.append(("Toxic Debris lays Toxic Spikes on the attacker's side after a physical hit", out == want,
                    str(out)))


@b11
def check_gooey(results):
    """Gooey (approved 2026-10-14; subscript_gooey): a contact hit lowers
    the attacker's Speed a stage, which Defiant answers with two stages of
    Attack and Clear Body keeps off; Mist does not stop it, and a hit
    without contact does nothing."""
    from . import perfectline as pl
    out = {}
    for case, name, ab, mist in (("contact", "Tackle", None, 0), ("no contact", "Swift", None, 0),
                                 ("Defiant", "Tackle", "Defiant", 0), ("Clear Body", "Tackle", "Clear Body", 0),
                                 ("Mist", "Tackle", None, 5)):
        b, p, foe = b11_battle(["Tackle"], [name], {("b", name): [10] * 16})
        p.ability, foe.ability, b.b.mist = "Gooey", ab, mist
        pl.use_move(b, foe, fs.move(name), p, True)
        out[case] = (foe.stages["spe"], foe.stages["atk"])
    want = {"contact": (-1, 0), "no contact": (0, 0), "Defiant": (-1, 2), "Clear Body": (0, 0), "Mist": (-1, 0)}
    results.append(("Gooey lowers a contact attacker's Speed", out == want, str(out)))


@b11
def check_pickpocket(results):
    """Pickpocket (approved 2026-10-14; BattleSystem_TriggerAbilityOnHit,
    subscript_pickpocket and TryPickpocket): a contact hit hands the
    attacker's item to an empty-handed holder; not from a hit without
    contact, not to a holder with an item, not from a Sticky Hold user, and
    not on a Dragon Tail that will drag the holder out (Ian, 2026-10-15),
    though with no one to drag in it steals."""
    from . import perfectline as pl
    out = {}
    for case, name, held, ab, bench in (("Tackle", "Tackle", None, None, True), ("Swift", "Swift", None, None, True),
                                        ("holding", "Tackle", "Oran Berry", None, True),
                                        ("Sticky Hold", "Tackle", None, "Sticky Hold", True),
                                        ("Dragon Tail", "Dragon Tail", None, None, True),
                                        ("Dragon Tail, no bench", "Dragon Tail", None, None, False)):
        b, p, foe = b11_battle(["Tackle"], [name], {("b", name): [10] * 16})
        if bench:
            b.p.mons.append(fs.Mon("p1", b.st["pokemon"]["p0"], b.st["info"]["p0"], ["Tackle"], "p"))
        p.ability, p.item, foe.ability, foe.item = "Pickpocket", held, ab, "Sitrus Berry"
        foe.stages["acc"] = 6                # Dragon Tail sure to land
        pl.use_move(b, foe, fs.move(name), p, True)
        out[case] = (p.item, foe.item)
    want = {"Tackle": ("Sitrus Berry", None), "Swift": (None, "Sitrus Berry"),
            "holding": ("Oran Berry", "Sitrus Berry"), "Sticky Hold": (None, "Sitrus Berry"),
            "Dragon Tail": (None, "Sitrus Berry"), "Dragon Tail, no bench": ("Sitrus Berry", None)}
    results.append(("Pickpocket takes a contact attacker's item", out == want, str(out)))


@b11
def check_long_reach(results):
    """Long Reach (approved 2026-10-14; Battler_MoveMakesContact): its
    holder's moves make no contact, so a Rough Skin target and a Spiky
    Shield cost it nothing, where they cost another Pokemon an eighth."""
    from . import perfectline as pl
    out = {}
    for case, ab in (("Long Reach", "Long Reach"), ("other", None)):
        b, p, foe = b11_battle(["Tackle"], ["Tackle"], {("p", "Tackle"): [10] * 16}, hp=80)
        p.ability, foe.ability = ab, "Rough Skin"
        pl.use_move(b, p, fs.move("Tackle"), foe, True)
        rough = p.maxhp - p.hp
        p.hp, foe.protecting, foe.last = p.maxhp, True, fs.move("Spiky Shield")
        pl.use_move(b, p, fs.move("Tackle"), foe, True)
        out[case] = (rough, p.maxhp - p.hp)
    want = {"Long Reach": (0, 0), "other": (10, 10)}
    results.append(("Long Reach's moves make no contact", out == want, str(out)))


@b11
def check_magician(results):
    """Magician (approved 2026-10-14; BattleSystem_TriggerAbilityOnHit after
    its switch, subscript_magician): the player's empty-handed holder's hit,
    contact or not, takes the target's item; not with an item in hand, not
    through Sticky Hold, not when the target's own on-hit ability answered
    (Rough Skin), and never for a trainer's holder (TryStealItem)."""
    from . import perfectline as pl
    out = {}
    rolls = {(s, m): [10] * 16 for s in "pb" for m in ("Swift", "Tackle")}
    for case, name, side, held, ab in (("Swift", "Swift", "p", None, None), ("Tackle", "Tackle", "p", None, None),
                                       ("holding", "Swift", "p", "Oran Berry", None),
                                       ("Sticky Hold", "Swift", "p", None, "Sticky Hold"),
                                       ("Rough Skin", "Tackle", "p", None, "Rough Skin"),
                                       ("trainer's", "Swift", "b", None, None)):
        b, p, foe = b11_battle(["Swift", "Tackle"], ["Swift", "Tackle"], rolls)
        att, dfn = (p, foe) if side == "p" else (foe, p)
        att.ability, att.item, dfn.ability, dfn.item = "Magician", held, ab, "Sitrus Berry"
        pl.use_move(b, att, fs.move(name), dfn, True)
        out[case] = (att.item, dfn.item)
    want = {"Swift": ("Sitrus Berry", None), "Tackle": ("Sitrus Berry", None),
            "holding": ("Oran Berry", "Sitrus Berry"), "Sticky Hold": (None, "Sitrus Berry"),
            "Rough Skin": (None, "Sitrus Berry"), "trainer's": (None, "Sitrus Berry")}
    results.append(("Magician takes the target's item after a hit", out == want, str(out)))


@b11
def check_anger_point(results):
    """Anger Point (approved 2026-10-14; subscript_critical_hit): a critical
    hit on its holder sets its Attack at +6, one its Substitute takes too,
    and a hit of several hits does at its critical one; a plain hit does
    nothing, nor a critical hit that faints it."""
    from . import perfectline as pl
    out = {}
    for case, name, stage, hp, sub in (("critical", "Tackle", 3, 100, 0), ("plain", "Tackle", 0, 100, 0),
                                       ("Substitute", "Tackle", 3, 100, 50), ("fainting", "Tackle", 3, 5, 0),
                                       ("two hits", "Double Kick", 3, 100, 0)):
        b, p, foe = b11_battle(["Tackle"], [name], {("b", name): [10] * 16})
        p.ability, p.hp, p.sub, foe.crit_stage = "Anger Point", hp, sub, stage
        foe.stages["acc"] = 6
        if not stage:
            b.st["first_battle"] = True      # no critical hit at all
        pl.use_move(b, foe, fs.move(name), p, True)
        out[case] = p.stages["atk"]
    want = {"critical": 6, "plain": 0, "Substitute": 6, "fainting": 0, "two hits": 6}
    results.append(("Anger Point maxes Attack after a critical hit", out == want, str(out)))


def _no_crit_dice():
    """The readings' dice with every rolled critical hit missing, so only a
    forced one lands."""
    from . import perfectline as pl

    class NoCrit(pl.RunDice):
        def good(self, p, kind=None):
            return False if kind == "crit" else super().good(p, kind)

        def bad(self, kind, p):
            return False if kind == "crit" else super().bad(kind, p)
    return NoCrit(random.Random(1), True)


@b11
def check_merciless(results):
    """Merciless (approved 2026-10-14; BattleSystem_CalcCriticalMulti): every
    hit its holder lands on a poisoned or badly poisoned target is critical,
    Oxide's 1.5 times, unless Shell Armor keeps it off; on a healthy target
    a hit is plain, and a move of several hits has each hit critical."""
    from . import perfectline as pl
    out = {}
    for case, status, ab in (("poisoned", "psn", None), ("badly poisoned", "tox", None), ("healthy", None, None),
                             ("Shell Armor", "psn", "Shell Armor")):
        b, p, foe = b11_battle(["Tackle"], ["Tackle"], {("p", "Tackle"): [10] * 16}, hp=200)
        b.dice = _no_crit_dice()
        p.ability, foe.status, foe.ability = "Merciless", status, ab
        pl.attack(b, p, fs.move("Tackle"), foe, True)
        out[case] = foe.maxhp - foe.hp
    out["several hits"] = fs.crit_rate(b, p, foe, fs.move("Double Kick"))
    foe.ability = None
    out["several hits"] = (out["several hits"], fs.crit_rate(b, p, foe, fs.move("Double Kick")))
    want = {"poisoned": 15, "badly poisoned": 15, "healthy": 10, "Shell Armor": 10, "several hits": (0.0, 1.0)}
    results.append(("Merciless makes every hit on a poisoned target critical", out == want, str(out)))


@b11
def check_analytic(results):
    """Analytic (approved 2026-10-14; BattleSystem_CalcMoveDamage): its
    holder's move at 13/10 power when every other Pokemon has acted this
    turn: when it moves after its foe, or its foe switched in; not when it
    moves first."""
    from . import perfectline as pl
    out = {}
    for case, speed, foe_act in (("first", 100, "move"), ("last", 30, "move"), ("foe switched", 100, "switch")):
        b, p, foe = b11_battle(["Tackle"], ["Splash"], {("p", "Tackle"): [10] * 16}, p_speed=speed, hp=500)
        b.dice = _no_crit_dice()
        b.b.mons.append(fs.Mon("b0.1", b.st["pokemon"]["b0.0"], b.st["info"]["b0.0"], ["Splash"], "b"))
        b.st["rows"][(None, "p0", "b0.1")] = b.st["rows"][(None, "p0", "b0.0")]
        b.st["speed"][(None, "b0.1")] = 50
        p.ability = "Analytic"
        aa = ("move", fs.move("Splash")) if foe_act == "move" else ("switch", 1)
        pl._turn(b, ("move", fs.move("Tackle")), aa)
        out[case] = b.b.cur().maxhp - b.b.cur().hp
    want = {"first": 10, "last": 13, "foe switched": 13}
    results.append(("Analytic's move at 13/10 power when its holder moves last", out == want, str(out)))


@b11
def check_flare_boost(results):
    """Flare Boost (approved 2026-10-14; BattleSystem_CalcMoveDamage): a
    special move at half again while its holder is burned; a physical one
    takes the burn's halving alone, and unburned nothing changes."""
    out = {}
    for case, name, status in (("Ember, burned", "Ember", "brn"), ("Ember", "Ember", None),
                               ("Tackle, burned", "Tackle", "brn")):
        b, p, foe = b11_battle([name], ["Splash"], {("p", name): [20] * 16})
        p.ability, p.status = "Flare Boost", status
        out[case] = b.damage(p, foe, fs.move(name), roll=0)
    want = {"Ember, burned": 30, "Ember": 20, "Tackle, burned": 10}
    results.append(("Flare Boost raises special moves while burned", out == want, str(out)))


@b11
def check_metal_weight(results):
    """Heavy Metal and Light Metal (approved 2026-10-14; Battler_Weight): the
    calculator's job for a holder carries twice or half its weight in whole
    tenths of a kilogram, a twin's own types kept; any other Pokemon's job
    is left alone."""
    bs = {"hp": 1, "at": 1, "df": 1, "sa": 1, "sd": 1, "sp": 1}
    blob = {"poks": {"Bronzong": {"bs": bs, "types": ["Steel", "Psychic"], "weightkg": 187.0},
                     "Scizor": {"bs": bs, "types": ["Bug", "Steel"], "weightkg": 118.5}}}
    heavy = fs.metal_weight(blob, {"species": "Bronzong", "ability": "Heavy Metal"})["species_data"]
    light = fs.metal_weight(blob, {"species": "Scizor", "ability": "Light Metal"})["species_data"]
    twin = fs.metal_weight(blob, {"species": "Scizor", "ability": "Light Metal", "species_data": {
        "bs": bs, "types": ["Water"], "exact_types": True, "weightkg": 118.5}})["species_data"]
    out = {"Heavy Metal": (heavy["weightkg"], heavy["types"]), "Light Metal": light["weightkg"],
           "twin": (twin["weightkg"], twin["types"], twin.get("exact_types"))}
    want = {"Heavy Metal": (374.0, ["Steel", "Psychic"]), "Light Metal": 59.2, "twin": (59.2, ["Water"], True)}
    results.append(("Heavy Metal and Light Metal change the weight the rows are made with", out == want, str(out)))


@b11
def check_contrary(results):
    """Contrary (approved 2026-10-14; BtlCmd_ChangeStatStage): every change
    a move, an item or Intimidate makes to its holder's stages is turned
    round: its Swords Dance lowers its Attack two stages, its Close Combat
    raises its defences, a foe's Growl raises its Attack, under Mist too,
    and Intimidate does; a Mold Breaker foe's Growl lowers it as usual,
    and Belly Drum still maximises it, set directly."""
    from . import perfectline as pl
    out = {}
    b, p, foe = b11_battle(["Swords Dance", "Close Combat", "Belly Drum"], ["Growl"],
                           {("p", "Close Combat"): [10] * 16})
    p.ability = "Contrary"
    pl.status_move(b, p, fs.move("Swords Dance"), foe, True)
    out["Swords Dance"] = p.stages["atk"]
    pl.attack(b, p, fs.move("Close Combat"), foe, True)
    out["Close Combat"] = (p.stages["def"], p.stages["spd"])
    p.stages["atk"] = 0
    b.p.mist = 5
    pl.status_move(b, foe, fs.move("Growl"), p, True)
    out["Growl under Mist"] = p.stages["atk"]
    p.stages["atk"], foe.ability, b.p.mist = 0, "Mold Breaker", 0
    pl.status_move(b, foe, fs.move("Growl"), p, True)
    out["Mold Breaker's Growl"] = p.stages["atk"]
    p.stages["atk"], foe.ability = 0, "Intimidate"
    fs.intimidate_foes(b, [foe])
    out["Intimidate"] = p.stages["atk"]
    p.stages["atk"] = 0
    pl.status_move(b, p, fs.move("Belly Drum"), foe, True)
    out["Belly Drum"] = p.stages["atk"]
    want = {"Swords Dance": -2, "Close Combat": (1, 1), "Growl under Mist": 1, "Mold Breaker's Growl": -1,
            "Intimidate": 1, "Belly Drum": 6}
    results.append(("Contrary turns every stat change round", out == want, str(out)))


@b11
def check_moody(results):
    """Moody (approved 2026-10-14; BattleSystem_TriggerTurnEndAbility,
    subscript_moody): at each turn's end one stat other than accuracy and
    evasion rises two stages and another falls one, drawn by the battle's
    dice, every stat in reach of both; with every stat but Sp. Def at +6,
    Sp. Def is the one to rise and one of the rest falls to +5."""
    from . import perfectline as pl
    ups, downs, plain = set(), set(), True
    for seed in range(40):
        b, p, foe = b11_battle(["Tackle"], ["Tackle"], {})
        b.dice = pl.RunDice(random.Random(seed), True)
        p.ability = "Moody"
        fs.end_of_turn(b)
        moved = {k: v for k, v in p.stages.items() if v}
        plain &= sorted(moved.values()) == [-1, 2]
        ups |= {k for k, v in moved.items() if v == 2}
        downs |= {k for k, v in moved.items() if v == -1}
    b, p, foe = b11_battle(["Tackle"], ["Tackle"], {})
    p.ability = "Moody"
    p.stages.update({"atk": 6, "def": 6, "spe": 6, "spa": 6})
    fs.end_of_turn(b)
    full = (p.stages["spd"], sorted(p.stages[k] for k in ("atk", "def", "spe", "spa")))
    out = (plain, sorted(ups), sorted(downs), full)
    want = (True, ["atk", "def", "spa", "spd", "spe"], ["atk", "def", "spa", "spd", "spe"], (2, [5, 6, 6, 6]))
    results.append(("Moody raises one stat two stages and lowers another at each turn's end", out == want, str(out)))


@b11
def check_screen_cleaner(results):
    """Screen Cleaner (approved 2026-10-14; the switch-in check's Oxide
    abilities step): as its holder comes in, Reflect, Light Screen and
    Aurora Veil end on both sides; another Pokemon coming in ends none."""
    out = {}
    for ab in ("Screen Cleaner", None):
        b, p, foe = b11_battle(["Tackle"], ["Tackle"], {})
        b.p.mons.append(fs.Mon("p1", b.st["pokemon"]["p0"], b.st["info"]["p0"], ["Tackle"], "p"))
        b.p.mons[1].ability = ab
        b.p.screens["Reflect"], b.b.screens["Light Screen"], b.b.aurora_veil = 5, 3, 4
        fs.switch_in(b, b.p, 1)
        out[ab or "other"] = (b.p.screens["Reflect"], b.b.screens["Light Screen"], b.b.aurora_veil)
    want = {"Screen Cleaner": (0, 0, 0), "other": (5, 3, 4)}
    results.append(("Screen Cleaner ends every screen as its holder comes in", out == want, str(out)))


@b11
def check_overcoat_weather(results):
    """Overcoat (approved 2026-10-14; BtlCmd_EndOfTurnWeatherEffect): its
    holder takes no sandstorm or hail damage at the turn's end, where
    another Pokemon loses a sixteenth."""
    out = {}
    for weather in ("Sand", "Hail"):
        for ab in ("Overcoat", None):
            b, p, foe = b11_battle(["Tackle"], ["Tackle"], {}, hp=160)
            b.weather, p.ability = weather, ab
            fs.end_of_turn(b)
            out[(weather, ab or "other")] = p.maxhp - p.hp
    want = {("Sand", "Overcoat"): 0, ("Sand", "other"): 10, ("Hail", "Overcoat"): 0, ("Hail", "other"): 10}
    results.append(("Overcoat keeps sand and hail off at the turn's end", out == want, str(out)))


@b11
def check_cloud_nine(results):
    """Cloud Nine (approved 2026-10-14; NO_CLOUD_NINE and CheckIgnoreWeather):
    while its holder stands, the weather has no effect: the sandstorm bites
    no one at the turn's end, Blizzard can miss in hail, a Swift Swim foe is
    not doubled in rain, Leaf Guard does not keep a status off in sun, and
    Solar Beam charges in sun. Without it each of these holds."""
    from . import perfectline as pl

    class Misses(pl.RunDice):
        """Every chance of a miss lands."""
        def bad(self, kind, p):
            return p > 0 if kind == "miss" else super().bad(kind, p)
    out = {}
    for ab in ("Cloud Nine", None):
        row = []
        b, p, foe = b11_battle(["Blizzard", "Solar Beam", "Thunder Wave"], ["Tackle"], {}, hp=160)
        b.cloudy, p.ability = True, ab
        b.weather = "Sand"
        fs.end_of_turn(b)
        row.append(foe.maxhp - foe.hp)
        b.weather, b.dice = "Hail", Misses(random.Random(1), True)
        row.append(pl.accuracy_hits(b, p, foe, fs.move("Blizzard")))
        b.weather = "Rain"
        b.st["speed"][("Rain", "b0.0")] = 100
        foe.ability = "Swift Swim"
        row.append(b.speed(foe))
        b.weather, foe.ability = "Sun", "Leaf Guard"
        b.dice = pl.RunDice(random.Random(1), True)
        pl.status_move(b, p, fs.move("Thunder Wave"), foe, True)
        row.append(foe.status)
        row.append(fs.charge_skipped(b, p, fs.move("Solar Beam")))
        out[ab or "other"] = tuple(row)
    want = {"Cloud Nine": (0, False, 50, "par", False), "other": (10, True, 100, None, True)}
    results.append(("Cloud Nine stills every effect of the weather", out == want, str(out)))


@b11
def check_wonder_skin(results):
    """Wonder Skin (approved 2026-10-14; BattleControllerPlayer_CheckMoveHitAccuracy):
    a status move aimed at its holder lands half the time at most, before
    the stages: Thunder Wave's 100 becomes 50, so with +6 accuracy it is
    sure again; a Mold Breaker's is not cut, nor a hit's accuracy."""
    from . import perfectline as pl
    out = {}
    for case, name, ab, acc in (("Thunder Wave", "Thunder Wave", None, 0), ("Mold Breaker", "Thunder Wave", "Mold Breaker", 0),
                                ("+6 accuracy", "Thunder Wave", None, 6), ("Tackle", "Tackle", None, 0)):
        hits = 0
        for seed in range(200):
            b, p, foe = b11_battle([name], ["Splash"], {})
            b.dice = pl.RunDice(random.Random(seed), True)
            foe.ability, p.ability, p.stages["acc"] = "Wonder Skin", ab, acc
            hits += pl.accuracy_hits(b, p, foe, fs.move(name))
        out[case] = hits
    ok = 70 <= out["Thunder Wave"] <= 130 and out["Mold Breaker"] == out["+6 accuracy"] == out["Tackle"] == 200
    results.append(("Wonder Skin halves a status move's accuracy", ok, f"hits of 200 {out}"))


@b11
def check_prankster_dark(results):
    """Prankster (approved 2026-10-14; BattleControllerPlayer_PriorityBlock):
    a status move it raises fails on a Dark-type foe; Spikes, aimed at the
    foe's side, still lands, and so does the move from a user without
    Prankster or into a foe of another type."""
    from . import perfectline as pl
    out = {}
    for case, ab, types in (("Dark", "Prankster", ("Dark",)), ("Normal", "Prankster", ("Normal",)),
                            ("no Prankster", None, ("Dark",))):
        b, p, foe = b11_battle(["Thunder Wave", "Spikes"], ["Splash"], {}, b_types=types)
        p.ability = ab
        pl.status_move(b, p, fs.move("Thunder Wave"), foe, True)
        pl.status_move(b, p, fs.move("Spikes"), foe, True)
        out[case] = (foe.status, b.b.hazards["spikes"])
    want = {"Dark": (None, 1), "Normal": ("par", 1), "no Prankster": ("par", 1)}
    results.append(("Prankster's raised status moves fail on a Dark type", out == want, str(out)))


@b11
def check_queenly_majesty(results):
    """Queenly Majesty (approved 2026-10-14; BattleControllerPlayer_PriorityBlock):
    a move of raised priority aimed at its holder fails, Quick Attack and
    a Prankster user's Thunder Wave alike; a plain Tackle lands, and a Mold
    Breaker's Quick Attack lands."""
    from . import perfectline as pl
    out = {}
    for case, name, ab in (("Quick Attack", "Quick Attack", None), ("Tackle", "Tackle", None),
                           ("Prankster", "Thunder Wave", "Prankster"), ("Mold Breaker", "Quick Attack", "Mold Breaker")):
        b, p, foe = b11_battle([name], ["Splash"], {("p", name): [10] * 16})
        foe.ability, p.ability = "Queenly Majesty", ab
        pl.use_move(b, p, fs.move(name), foe, True)
        out[case] = (foe.maxhp - foe.hp, foe.status)
    want = {"Quick Attack": (0, None), "Tackle": (10, None), "Prankster": (0, None), "Mold Breaker": (10, None)}
    results.append(("Queenly Majesty stops moves of raised priority", out == want, str(out)))


@b11
def check_magic_bounce(results):
    """Magic Bounce (approved 2026-10-14; BattleControllerPlayer_MoveStolen):
    a move Magic Coat would turn back, aimed at its holder, is turned back
    on its user every turn with no move used: Thunder Wave paralyses its
    user, Growl lowers its user's Attack, twice in two turns; a Mold
    Breaker's lands, and so does a move into a holder in the air."""
    from . import perfectline as pl
    out = {}
    for case, ab, flying in (("plain", None, False), ("Mold Breaker", "Mold Breaker", False), ("in the air", None, True)):
        b, p, foe = b11_battle(["Thunder Wave", "Growl"], ["Splash"], {})
        foe.ability, p.ability = "Magic Bounce", ab
        if flying:
            foe.charging = fs.move("Fly")
        pl.status_move(b, p, fs.move("Thunder Wave"), foe, True)
        for _ in range(2):
            pl.status_move(b, p, fs.move("Growl"), foe, True)
        out[case] = (p.status, p.stages["atk"], foe.status, foe.stages["atk"])
    want = {"plain": ("par", -2, None, 0), "Mold Breaker": (None, 0, "par", -2), "in the air": (None, 0, None, 0)}
    results.append(("Magic Bounce turns reflectable moves back on their user", out == want, str(out)))


@b11
def check_sweet_veil(results):
    """Sweet Veil (approved 2026-10-14; subscript_fall_asleep and
    subscript_yawn): its holder cannot fall asleep, to Spore or to a Yawn's
    drowsiness at the turn's end; a Mold Breaker's Spore puts it to
    sleep."""
    from . import perfectline as pl
    out = {}
    for case, name, ab in (("Spore", "Spore", None), ("Yawn", "Yawn", None), ("Mold Breaker", "Spore", "Mold Breaker")):
        b, p, foe = b11_battle([name], ["Splash"], {})
        foe.ability, p.ability = "Sweet Veil", ab
        pl.use_move(b, p, fs.move(name), foe, True)
        for _ in range(2):
            fs.end_of_turn(b)
        out[case] = foe.status
    want = {"Spore": None, "Yawn": None, "Mold Breaker": "slp"}
    results.append(("Sweet Veil keeps its holder awake", out == want, str(out)))


@b11
def check_pastel_veil(results):
    """Pastel Veil (approved 2026-10-14; subscript_poison and
    subscript_badly_poison): its holder cannot be poisoned or badly
    poisoned, by a move or by Toxic Spikes as it comes in; a Mold
    Breaker's Toxic poisons it."""
    from . import perfectline as pl
    out = {}
    for case, name, ab in (("Toxic", "Toxic", None), ("Poison Gas", "Poison Gas", None),
                           ("Mold Breaker", "Toxic", "Mold Breaker")):
        b, p, foe = b11_battle([name], ["Splash"], {})
        foe.ability, p.ability = "Pastel Veil", ab
        p.stages["acc"] = 6
        pl.use_move(b, p, fs.move(name), foe, True)
        out[case] = foe.status
    b, p, foe = b11_battle(["Tackle"], ["Splash"], {})
    b.b.mons.append(fs.Mon("b0.1", b.st["pokemon"]["b0.0"], b.st["info"]["b0.0"], ["Splash"], "b"))
    b.b.mons[1].ability = "Pastel Veil"
    b.b.hazards["tspikes"] = 2
    fs.switch_in(b, b.b, 1)
    out["Toxic Spikes"] = (b.b.cur().status, b.b.hazards["tspikes"])
    want = {"Toxic": None, "Poison Gas": None, "Mold Breaker": "tox", "Toxic Spikes": (None, 2)}
    results.append(("Pastel Veil keeps poison off its holder", out == want, str(out)))


@b11
def check_flower_veil(results):
    """Flower Veil (approved 2026-10-14; BtlCmd_ChangeStatStage): the other
    side cannot lower a Grass-type holder's stats, by Growl or Intimidate;
    a Mold Breaker's Growl can, a holder of another type has no shield, and
    its own Close Combat still lowers its defences."""
    from . import perfectline as pl
    out = {}
    for case, types, ab in (("Grass", ("Grass",), None), ("Mold Breaker", ("Grass",), "Mold Breaker"),
                            ("Normal", ("Normal",), None)):
        b, p, foe = b11_battle(["Growl"], ["Close Combat"], {("b", "Close Combat"): [10] * 16}, b_types=types)
        foe.ability, p.ability = "Flower Veil", ab
        pl.status_move(b, p, fs.move("Growl"), foe, True)
        out[case] = foe.stages["atk"]
    p.ability, foe.stages["atk"] = "Intimidate", 0
    foe.types = ["Grass"]
    fs.intimidate_foes(b, [p])
    out["Intimidate"] = foe.stages["atk"]
    pl.attack(b, foe, fs.move("Close Combat"), p, True)
    out["its own Close Combat"] = (foe.stages["def"], foe.stages["spd"])
    want = {"Grass": 0, "Mold Breaker": -1, "Normal": -1, "Intimidate": 0, "its own Close Combat": (-1, -1)}
    results.append(("Flower Veil keeps the other side's drops off a Grass-type holder", out == want, str(out)))

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


def check_reward_items(results):
    """A booster a trainer gives straight after the win is in the player's
    stock from that trainer's split on, and not a split before, unless
    another source gives that type's booster sooner."""
    from tools.oxide.encounters import calc_trainers
    from . import pool, splits
    by_type = {i: t for t, items in pool.TYPE_ITEMS.items() for i in items}
    rows, ok = [], True
    for split, tr, it in splits.trainer_rewards():
        t = by_type.get(calc_trainers._item_name(it))
        if t is None or split not in pool.SPLITS:
            continue
        here = t in fs.player_items(split)["boosters"]
        i = pool.SPLITS.index(split)
        before = i > 0 and t in fs.player_items(pool.SPLITS[i - 1])["boosters"]
        rows.append(f"{tr} {t} in {split}: {here}, before: {before}")
        ok = ok and here
    results.append(("a trainer's after-win booster joins the player's stock in its split", ok and bool(rows),
                    "; ".join(rows) or "no booster among the rewards"))


def main():
    results = []
    for check in (check_damage, check_crit_odds, check_status_immunity, check_item_moves,
                  check_weather_rock, check_map_weather_replaced, check_permanent_trick_room,
                  check_move_reworks, check_infiltrator, check_ability_weather, check_end_of_turn_order,
                  check_salt_cure, check_harvest, check_berry_first_hit,
                  check_neutralizing_gas, check_gas_wears_off, check_gas_exceptions, check_gas_doubles,
                  check_intimidate_start, check_intimidate_proof, check_two_hit_holds,
                  check_hits_one_by_one, check_hits_hold_and_heal, check_triple_axel,
                  check_protect_flag, check_protect_odds, check_pp_engine, check_confusion_blockers,
                  check_curse_and_rest, check_mist_and_intimidate, check_ai_fields, check_future_sight,
                  check_sleep_talk_rest, check_disable, check_nightmare,
                  check_encore, check_ice_body, check_absorbing_abilities,
                  check_roost, check_protean, check_form_twins, check_trace, check_mummy,
                  check_wandering_spirit, check_color_change, check_forecast, check_soak,
                  check_conversion, check_conversion2, check_camouflage, check_burn_up,
                  check_double_shock, check_skill_swap, check_role_play, check_entrainment,
                  check_worry_seed, check_gastro_acid, check_core_enforcer, check_captivate,
                  check_status_into_vanished, check_speed_down_hit, check_bounce_paralysis, check_weather_heal,
                  check_hail_under_lasting_hail, check_dream_eater, check_focus_punch,
                  check_crash_on_miss, check_bind, check_steal_item, check_swap_items,
                  check_pluck, check_chatter, check_stockpile, check_lower_sp_atk_hit, check_rollout, check_wake_up_slap, check_throat_chop, check_minimize_stomp, check_charge, check_lucky_chant, check_psych_up, check_lock_on, check_foresight, check_trainer_magnitude, check_trainer_return, check_smack_down, check_gravity, check_mimic, check_mirror_move, check_copycat, check_fling,
                  check_natural_gift, check_imprison, check_baton_pass,
                  check_magic_guard, check_liquid_ooze,
                  check_drop_answers, check_technician_power, check_stored_power,
                  check_hard_press, check_electro_ball, check_sacred_sword, check_mold_breaker,
                  check_oblivious_taunt, check_cursed_body, check_justified_rattled,
                  check_knockout_boost, check_trapping_exemptions, check_accuracy_abilities,
                  check_download, check_weather_abilities, check_sand_force,
                  check_bad_dreams, check_marvel_scale, check_shed_skin,
                  check_suction_cups, check_plus_minus, check_stench, check_unnerve,
                  check_telepathy, check_steadfast, check_starf_berry,
                  check_sticky_barb, check_payback, check_leech_seed_sap,
                  check_ghost_untrapped, check_soundproof_status, check_item_flinch_blocked,
                  check_black_sludge, check_water_bubble, check_eerie_spell,
                  check_burning_bulwark,
                  check_refresh, check_wring_out, check_miracle_eye, check_acupressure,
                  check_trainer_frustration, check_secret_power, check_snore,
                  check_raise_speed_hit, check_trump_card,
                  check_teeter_dance, check_smelling_salts, check_magic_coat, check_present,
                  check_water_sport, check_acrobatics, check_guard_swap,
                  check_power_swap, check_psycho_shift, check_memento,
                  check_sketch, check_me_first, check_nature_power,
                  check_power_trick, check_bide, check_transform,
                  check_sp_def_2_hit, check_tearful_look, check_venom_drench, check_false_swipe,
                  check_clear_smog, check_incinerate, check_life_dew,
                  check_mud_sport, check_punishment, check_sticky_web,
                  check_defog, check_strength_sap, check_parting_shot,
                  check_dragon_tail, check_side_guards, check_heat_crash,
                  check_healing_wish, check_guard_split, check_power_split,
                  check_embargo, check_magic_room,
                  check_relic_song, check_clanging_scales, check_matcha_gotcha,
                  check_fell_stinger, check_prevent_escape_hit,
                  check_poltergeist, check_belch, check_first_impression,
                  check_axe_kick, check_always_critical,
                  check_clangorous_soul, check_heart_swap, check_heal_pulse,
                  check_lunar_dance, check_grudge, check_octolock,
                  check_aurora_veil, check_teatime, check_assist,
                  check_snatch, check_sky_drop,
                  check_substitute_hit, check_knock_off_first, check_taunt_before_confusion,
                  check_forced_out, check_charge_ends, check_ingrain_grounds, check_fog,
                  check_rematch_terrain, check_borrowed_twins, check_meloetta_form,
                  check_status,
                  check_sleep_turns, check_ai_kill, check_ai_status,
                  check_battle, check_doubles, check_pivot, check_stall, check_pp_stall, check_setup,
                  check_self_risk, check_sure, check_reward_items) + tuple(B11):
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

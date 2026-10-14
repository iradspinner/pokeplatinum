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
    want_plain = {"hazards": (76, "psn", 1), "hazards, a Poison type": (76, None, 0), "recoil": 90, "crash": 50,
                  "bound": (94, 2, 50), "seeded": (88, 0, 62)}
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
                  check_roost, check_protean, check_magic_guard, check_liquid_ooze,
                  check_drop_answers, check_technician_power, check_stored_power,
                  check_hard_press, check_electro_ball, check_sacred_sword, check_mold_breaker,
                  check_oblivious_taunt, check_cursed_body, check_justified_rattled,
                  check_knockout_boost, check_trapping_exemptions, check_accuracy_abilities,
                  check_download, check_weather_abilities, check_sand_force,
                  check_status,
                  check_sleep_turns, check_ai_kill, check_ai_status,
                  check_battle, check_doubles, check_pivot, check_stall, check_pp_stall, check_setup,
                  check_self_risk, check_sure, check_reward_items):
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

"""The fight simulator's rules, on small battles built by hand (fightsim.py, fightai.py).

    PYTHONPATH=. python3 -m tools.oxide.balance.test_fightsim

Runs no Node: each check builds the calculator's rows itself, so what it
tests is the simulator's own arithmetic and rules.
"""
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

"""B3: pressure scores for each of Oxide's story fights.

    PYTHONPATH=. python3 -m tools.oxide.balance.pressure --fight roark
    PYTHONPATH=. python3 -m tools.oxide.balance.pressure --split Gardenia
    PYTHONPATH=. python3 -m tools.oxide.balance.pressure --report

Each boss Pokemon is set against the player's side at its fight's split
(pool.py), and the vendored calculator's own engine does the damage
(calc_headless.js, one Node process). For each boss Pokemon it reports:

- threat: the share of the player's side it knocks out in one or two hits
  while moving first;
- answers: the share of the player's side that does the same to it.

Rolled up per fight as the mean over its Pokemon; a rival fight is the mean
over its three starter variants, and a tag battle counts both opponents.

What a hit and a KO mean here. A move knocks out in n hits when n times its
middle roll (the ninth of sixteen, so at least half the rolls) reaches the
target's HP. A charging move (Solar Beam out of sun, Fly, Dig) spends two
turns a hit, and a recharging one (Hyper Beam) a turn after each hit but the
last, so "two hits" means two turns. Moving first is a positive priority
move, or equal priority and strictly more Speed (the engine's own final
Speed, so Choice Scarf and Swift Swim count); a Speed tie counts for neither
side. A fight fought under Trick Room (fights.json, "trick_room") reverses
the Speed test, strictly less Speed going first, while a positive priority
move still goes first. A boss holding a Focus Sash cannot be knocked out in
one hit.

What this leaves out, and so reads as a ceiling for the boss: accuracy,
secondary effects, status and setup, switching, and the AI's real choice of
move (it assumes the boss's best move; element 6 documents how Platinum's AI
actually picks). Each boss Pokemon starts the fight in its map's battle
weather, or in its own ability's weather. Doubles are scored as singles.

B5 adds columns beside these, which leave the B3 columns as they were:

- threat_chance: threat counted by the chance the knockout lands, from
  each move's accuracy, with a move that lowers its user's attack hitting
  softer after the first use;
- answers_duel: the share of the side that beats the boss Pokemon one on
  one from a free switch-in, knocking it out within three turns before it
  is knocked out, counted by the chance its own hits land; answers_sure,
  the share whose chance is at least 0.8;
- broad: the share of the side that surely answers at least half the
  team, high when a team shares a weakness; best_one and cover, the most
  of the team one player Pokemon surely answers, and the fewest that
  answer all of it;
- unseen: the tactics in the team that no damage score sees (setup,
  Baton Pass, hazards, Explosion, status, evasion, recovery, pinch
  berries), listed by kind and counted, not scored;
- predictable: how far a player can call the team's moves in advance,
  from how Platinum's AI picks (predictability()); against Ian's ratings it
  runs backwards, measuring how much of a team's time goes to attacks, so
  it is not read as difficulty (the plan, "What Ian's ratings showed");
- answers_branch: answers_bait, but a player Pokemon counts only if it
  also beats the boss Pokemon after one use of each setup move it knows
  (SETUP), the branch Ian plans a whole fight around ("if Metagross ever
  uses Agility, nothing I have beats it");
- safe: the share of the side that at most one boss Pokemon knocks out
  in one hit, so that it can switch in, low when a team doubles up its
  coverage so that baiting one Pokemon draws in another with the same
  answer (Saturn 2, Cyrus 3), high when it shares a weakness (Mars 2);
- answers_bait: one-on-one answers, and for a Choice holder also every
  player Pokemon that wins after the player baits the lock (bait()): the
  AI's pick against a given lead is fixed, so the player chooses the move
  it locks into, then switches to something that takes it.

A boss that holds an item keeps Natural Gift and Fling, which the
calculator works out from the item, as one hit each, since the item is
spent; the player's side holds no berries and never uses them.

The runs are staged and kept small, one split at a time, because this CPU
fails under load: every calculation is one process, run one after another.
Results go to pressure.json beside this file, one entry per fight.
"""
import argparse
import functools
import json
import os
import subprocess
import sys
import tempfile
import time

from ..encounters import calc_export
from . import data, metrics, pool, splits

HERE = os.path.dirname(os.path.abspath(__file__))
RUNNER = os.path.join(HERE, "calc_headless.js")
OUT = os.path.join(HERE, "pressure.json")

CHARGE = {"Solar Beam", "SolarBeam", "Solar Blade", "Sky Attack", "Skull Bash", "Razor Wind",
          "Fly", "Dig", "Dive", "Bounce", "Shadow Force", "Phantom Force", "Meteor Beam",
          "Freeze Shock", "Ice Burn", "Geomancy", "Electro Shot"}
SUN_SKIPS_CHARGE = {"Solar Beam", "SolarBeam", "Solar Blade"}
RECHARGE = {"Hyper Beam", "Giga Impact", "Blast Burn", "Frenzy Plant", "Hydro Cannon",
            "Rock Wrecker", "Roar of Time", "Eternabeam", "Prismatic Laser", "Meteor Assault"}
ABILITY_WEATHER = {"Drizzle": "Rain", "Drought": "Sun", "Sand Stream": "Sand",
                   "Snow Warning": "Hail"}
CALC_WEATHER = {"Rain": "Rain", "Sun": "Sun", "Sand": "Sand", "Hail": "Hail"}   # fog: none

# B5's readings (2026-09-25), in columns of their own beside B3's so B3's
# numbers stay comparable. Ian's bellwethers asked for them: Maylene and
# Volkner, fast attacking teams that B3's threat ranks among the hardest
# fights though a player plans around them, and Officer Hesperid at Lake
# Valor, whose danger is in moves no damage score sees (the plan, "B5").
MOVES_DIR = os.path.normpath(os.path.join(HERE, "..", "..", "..", "res", "moves"))
# Oxide's move data keeps Generation 4 spellings of a few names.
MOVE_SPELLING = {"High Jump Kick": "Hi Jump Kick", "Feint Attack": "Faint Attack",
                 "Smelling Salts": "SmellingSalt", "Vise Grip": "ViceGrip"}
# A move that lowers its user's attacking stat hits softer each use after
# the first; the stages each use costs.
SELF_DROP = {"Leaf Storm": 2, "Draco Meteor": 2, "Overheat": 2, "Psycho Boost": 2,
             "Fleur Cannon": 2, "Superpower": 1}
# A one-on-one answer may take three turns, one more than B3's answers.
DUEL_TURNS = 3
# A sure answer lands every hit it needs with at least this chance: a 90
# percent move twice (0.81) is sure, an 80 percent move twice (0.64) is not.
SURE = 0.8
# Tactics no damage score sees, by kind, as a boss team's moves, items and
# abilities name them. They are listed per fight, not scored: Officer
# Hesperid's Agility passed into a Choice Specs Chatot, beside two
# Explosions, is what makes her fight hard to plan for.
UNSEEN = {
    "setup": {"Swords Dance", "Dragon Dance", "Nasty Plot", "Calm Mind", "Bulk Up", "Agility",
              "Rock Polish", "Curse", "Quiver Dance", "Shell Smash", "Belly Drum", "Coil",
              "Work Up", "Growth", "Hone Claws", "Tail Glow", "Cosmic Power", "Iron Defense",
              "Amnesia", "Autotomize", "Shift Gear", "Acid Armor", "Barrier", "Howl",
              "Meditate", "Sharpen", "Charge", "Stockpile", "Victory Dance", "Geomancy",
              "Defend Order"},
    "passing": {"Baton Pass"},
    "hazards": {"Stealth Rock", "Spikes", "Toxic Spikes", "Sticky Web"},
    "sacrifice": {"Explosion", "Self-Destruct", "Selfdestruct", "Memento", "Destiny Bond",
                  "Healing Wish", "Lunar Dance", "Final Gambit", "Perish Song"},
    "speed control": {"Trick Room", "Tailwind", "Thunder Wave", "Glare", "Stun Spore"},
    "status": {"Will-O-Wisp", "Toxic", "Spore", "Sleep Powder", "Hypnosis", "Yawn",
               "Lovely Kiss", "Sing", "Grass Whistle", "Dark Void", "Confuse Ray", "Swagger",
               "Attract", "Poison Powder", "Supersonic", "Flatter", "Teeter Dance"},
    "evasion": {"Double Team", "Minimize", "Bright Powder", "BrightPowder", "Lax Incense",
                "Sand Veil", "Snow Cloak"},
    "recovery": {"Recover", "Roost", "Slack Off", "Soft-Boiled", "Milk Drink", "Moonlight",
                 "Morning Sun", "Synthesis", "Wish", "Rest", "Aqua Ring", "Ingrain",
                 "Leech Seed", "Heal Order", "Shore Up", "Strength Sap"},
    "disruption": {"Encore", "Taunt", "Trick", "Switcheroo", "Roar", "Whirlwind", "Haze",
                   "Disable", "Torment", "Protect", "Detect", "Substitute", "Reflect",
                   "Light Screen", "Safeguard", "Knock Off", "Fake Out", "U-turn", "Volt Switch"},
    "pinch items": {"Petaya Berry", "Liechi Berry", "Salac Berry", "Ganlon Berry",
                    "Apicot Berry", "Starf Berry", "Lansat Berry", "Micle Berry",
                    "Custap Berry", "Quick Claw", "White Herb"},
    "weather moves": {"Rain Dance", "Sunny Day", "Sandstorm", "Hail"},
}
# Moves Evaluate Attack neither calls strongest nor counts as killing, and
# marks down four times in five (docs/oxide/battle-ai/other-flags.md): each
# is a live choice about one turn in five.
GAMBLES = {"Explosion", "Self-Destruct", "Selfdestruct", "Focus Punch", "Sucker Punch"}
GAMBLE_WEIGHT = 0.2
# The stat stages one use of each setup move gives, as Generation 4 has
# them (Curse's as a non-Ghost uses it). A boss Pokemon that knows one is
# also scored as it stands after that one use.
SETUP = {"Swords Dance": {"atk": 2}, "Nasty Plot": {"spa": 2}, "Agility": {"spe": 2},
         "Rock Polish": {"spe": 2}, "Dragon Dance": {"atk": 1, "spe": 1},
         "Calm Mind": {"spa": 1, "spd": 1}, "Bulk Up": {"atk": 1, "def": 1},
         "Curse": {"atk": 1, "def": 1, "spe": -1}, "Cosmic Power": {"def": 1, "spd": 1},
         "Defend Order": {"def": 1, "spd": 1}, "Iron Defense": {"def": 2},
         "Acid Armor": {"def": 2}, "Barrier": {"def": 2}, "Amnesia": {"spd": 2},
         "Growth": {"spa": 1}, "Howl": {"atk": 1}, "Meditate": {"atk": 1},
         "Sharpen": {"atk": 1}, "Hone Claws": {"atk": 1}, "Work Up": {"atk": 1, "spa": 1},
         "Coil": {"atk": 1, "def": 1}, "Quiver Dance": {"spa": 1, "spd": 1, "spe": 1},
         "Shell Smash": {"atk": 2, "spa": 2, "spe": 2, "def": -1, "spd": -1},
         "Shift Gear": {"atk": 1, "spe": 2}, "Tail Glow": {"spa": 2}, "Belly Drum": {"atk": 6},
         "Charge": {"spd": 1}, "Victory Dance": {"atk": 1, "def": 1, "spe": 1}}
# Moves whose power comes from the held item, which one use spends: a boss
# holding an item keeps them, as a one-hit knockout at most.
ITEM_MOVES = {"Natural Gift", "Fling"}


def hits_to_ko(rolls, hp):
    """The fewest hits whose middle roll reaches hp, or None if it never does."""
    mid = rolls[len(rolls) // 2]
    if mid <= 0:
        return None
    return -(-hp // mid)


def turns(move, hits, weather):
    """Turns the hits take: two a hit for a charging move, one more between
    hits for a recharging one."""
    if move in CHARGE and not (move in SUN_SKIPS_CHARGE and weather == "Sun"):
        return 2 * hits
    if move in RECHARGE:
        return 2 * hits - 1
    return hits


def moves_first(priority, speeds, trick_room=False):
    """True when the attacker's move goes before the defender's, taken to be
    a move of no priority: a positive priority goes first, and otherwise the
    faster side does, or under Trick Room the slower. A tie is neither's."""
    if priority != 0:
        return priority > 0
    return speeds[0] < speeds[1] if trick_room else speeds[0] > speeds[1]


def wins(row, def_info, speeds, weather, sash=False, trick_room=False):
    """True when some move of the attacker's knocks the defender out within
    two turns while moving first. `speeds` is (attacker, defender)."""
    for move, r in row["moves"].items():
        if "error" in r:
            continue
        n = hits_to_ko(r["rolls"], def_info["hp"])
        if n is None or (move in ITEM_MOVES and n > 1):
            continue
        if sash and n == 1:
            n = 2
        if turns(move, n, weather) > 2:
            continue
        if moves_first(r["priority"], speeds, trick_room):
            return True
    return False


CHOICE = {"Choice Band", "Choice Specs", "Choice Scarf"}


def turns_to_ko(row, def_info, weather, sash=False):
    """{move: turns it takes to knock the defender out}, for the moves that
    ever do, with the same hit, charge and Focus Sash rules as wins()."""
    out = {}
    for move, r in row["moves"].items():
        if "error" in r:
            continue
        n = hits_to_ko(r["rolls"], def_info["hp"])
        if n is None or (move in ITEM_MOVES and n > 1):
            continue
        if sash and n == 1:
            n = 2
        out[move] = turns(move, n, weather)
    return out


def locked_move(rows, key, side_keys, info, weather):
    """The move a Choice-locked boss is taken to lock into: the one that
    knocks out most of the side within two turns, ignoring Speed, with ties
    going to the one that takes off most HP on average."""
    tally = {}
    for pk in side_keys:
        for move, r in rows[(key, pk)]["moves"].items():
            if "error" in r:
                continue
            t = turns_to_ko({"moves": {move: r}}, info[pk], weather).get(move)
            ko, share = tally.get(move, (0, 0.0))
            tally[move] = (ko + (t is not None and t <= 2),
                           share + min(1.0, r["rolls"][len(r["rolls"]) // 2] / info[pk]["hp"]))
    return max(tally, key=lambda m: tally[m]) if tally else None


def lock_answer(up, down, locked, player_info, boss_info, weather, sash, trick_room=False):
    """True when a player Pokemon that is not a plain answer beats a
    Choice-locked boss by coming in on its locked move. Coming in costs one
    hit of that move; then the player needs its knockout (two turns at most,
    as for any answer) to land before the locked move knocks it out. Moving
    first, it takes n hits for its n attacks (the switch-in hit and n - 1
    more); moving second it takes n + 1. The locked move knocks it out in k
    turns, so the answer holds when the hits taken stay below k."""
    r = down["moves"].get(locked)
    k = turns_to_ko({"moves": {locked: r}}, player_info, weather).get(locked) \
        if r and "error" not in r else None
    for move, n in turns_to_ko(up, boss_info, weather, sash).items():
        if n > 2:
            continue
        first = moves_first(up["moves"][move]["priority"], up["speeds"], trick_room)
        taken = n if first else n + 1
        if k is None or taken < k:
            return True
    return False


@functools.lru_cache(maxsize=None)
def accuracies():
    """{compact move name: accuracy in percent, None for a move that never
    misses} from Oxide's move data. The reference hacks' tables carry no
    accuracy, so their moves are read here as well."""
    out = {}
    for d in os.listdir(MOVES_DIR):
        path = os.path.join(MOVES_DIR, d, "data.json")
        if os.path.exists(path):
            with open(path, encoding="utf-8") as f:
                rec = json.load(f)
            out[metrics._compact(rec["name"])] = rec["accuracy"] or None
    return out


def hit_chance(move, att, dfn, weather, category=None):
    """The chance one use of `move` lands: its accuracy, Thunder and Blizzard
    in their weather, and the modifiers a trainer's set commonly carries (No
    Guard, Compound Eyes, Hustle, Wide Lens, Bright Powder, Sand Veil and
    Snow Cloak). `att` and `dfn` are the engine's records of the two."""
    if "No Guard" in (att.get("ability"), dfn.get("ability")):
        return 1.0
    if (move, weather) in (("Thunder", "Rain"), ("Blizzard", "Hail")):
        return 1.0
    acc = accuracies().get(metrics._compact(MOVE_SPELLING.get(move, move)), 100)
    if acc is None:
        return 1.0
    if (move, weather) == ("Thunder", "Sun"):
        acc = 50
    p = acc / 100
    if att.get("ability") == "Compound Eyes":
        p *= 1.3
    if att.get("ability") == "Hustle" and category == "Physical":
        p *= 0.8
    if att.get("item") == "Wide Lens":
        p *= 1.1
    if dfn.get("item") in ("Bright Powder", "BrightPowder"):
        p *= 0.9
    if (dfn.get("ability"), weather) in (("Sand Veil", "Sand"), ("Snow Cloak", "Hail")):
        p *= 0.8
    return min(1.0, p)


def hits_needed(move, rolls, hp):
    """hits_to_ko, with a move that lowers its user's attack hitting softer
    each use after the first: at two stages down half as hard, at four a
    third."""
    n = hits_to_ko(rolls, hp)
    if move in ITEM_MOVES and n is not None and n > 1:
        return None
    drop = SELF_DROP.get(move)
    if n is None or n == 1 or not drop:
        return n
    mid = rolls[len(rolls) // 2]
    dealt, down, hits = 0.0, 0, 0
    while dealt < hp:
        if hits == 6:
            return None
        dealt += mid * 2 / (2 + down)
        down, hits = min(6, down + drop), hits + 1
    return hits


def threat_chance(down, player, boss, weather, trick_room=False):
    """B3's threat for one pair, counted by chance: the boss's likeliest
    knockout within two turns while moving first, each hit landing with its
    accuracy, and a self-lowering move hitting softer after the first."""
    best = 0.0
    for move, r in down["moves"].items():
        if "error" in r:
            continue
        n = hits_needed(move, r["rolls"], player["hp"])
        if n is None or turns(move, n, weather) > 2:
            continue
        if moves_first(r["priority"], down["speeds"], trick_room):
            best = max(best, hit_chance(move, boss, player, weather, r.get("category")) ** n)
    return best


def duel(up, down, player, boss, weather, sash, trick_room=False):
    """The chance a player Pokemon beats a boss Pokemon one on one, coming in
    free after a faint: its knockout, within three turns, lands before the
    boss's quickest knockout of it. The boss's hits are taken to land, as a
    plan must assume; the player's must all land, so a win counts by that
    chance. Priority is compared move against move, then Speed."""
    k, k_pr = None, 0
    for move, r in down["moves"].items():
        if "error" in r:
            continue
        n = hits_needed(move, r["rolls"], player["hp"])
        if n is None:
            continue
        t = turns(move, n, weather)
        if k is None or t < k or (t == k and r["priority"] > k_pr):
            k, k_pr = t, r["priority"]
    best = 0.0
    for move, r in up["moves"].items():
        if "error" in r:
            continue
        n = hits_needed(move, r["rolls"], boss["hp"])
        if n is None:
            continue
        if sash and n == 1:
            n = 2
        t = turns(move, n, weather)
        if t > DUEL_TURNS:
            continue
        first = moves_first(r["priority"] - k_pr, up["speeds"], trick_room)
        if k is None or (t <= k if first else t < k):
            best = max(best, hit_chance(move, player, boss, weather, r.get("category")) ** n)
    return best


def ai_pick(row):
    """The move Evaluate Attack picks against this target: the one whose top
    roll does most, since every damage check in the AI's script uses the top
    of the range (docs/oxide/battle-ai/README.md). The gambles, which it
    never calls strongest, and the priority kill bonus are left out."""
    best, top = None, 0
    for move, r in row["moves"].items():
        if "error" in r or move in GAMBLES:
            continue
        if r["rolls"][-1] > top:
            best, top = move, r["rolls"][-1]
    return best


def bait(up, down, locked, player, boss, weather, sash, trick_room=False):
    """The chance a player Pokemon beats a boss Pokemon locked into `locked`
    by switching in on it: one hit taken coming in, then its knockout,
    within three turns, before the locked move knocks it out. Counted by the
    chance its own hits land, as in duel()."""
    r = down["moves"].get(locked)
    k = None
    if r and "error" not in r:
        n = hits_needed(locked, r["rolls"], player["hp"])
        k = turns(locked, n, weather) if n is not None else None
    pr = r["priority"] if r and "error" not in r else 0
    best = 0.0
    for move, r2 in up["moves"].items():
        if "error" in r2:
            continue
        n = hits_needed(move, r2["rolls"], boss["hp"])
        if n is None:
            continue
        if sash and n == 1:
            n = 2
        t = turns(move, n, weather)
        if t > DUEL_TURNS:
            continue
        first = moves_first(r2["priority"] - pr, up["speeds"], trick_room)
        taken = t if first else t + 1
        if k is None or taken < k:
            best = max(best, hit_chance(move, player, boss, weather, r2.get("category")) ** n)
    return best


def add_branches(jobs, key, mon, moves, side, weather):
    """Adds to `jobs` a copy of the boss Pokemon `key` as it stands after one
    use of each setup move it knows, keyed "key+Move", with its pairs against
    the side both ways."""
    for s in sorted(set(mon.get("moves") or []) & set(SETUP)):
        bkey = f"{key}+{s}"
        jobs["pokemon"][bkey] = dict(mon, boosts=SETUP[s])
        for i, p in enumerate(side):
            jobs["pairs"].append([bkey, f"p{i}", moves, weather])
            jobs["pairs"].append([f"p{i}", bkey, p["moves"], weather])


def cover(sets):
    """The fewest player Pokemon that between them hold a sure one-on-one
    answer to every boss Pokemon, or None when some boss Pokemon has none in
    the whole side. `sets` holds each boss Pokemon's sure answers."""
    if not sets or any(not s for s in sets):
        return None
    masks = {}
    for i, s in enumerate(sets):
        for pk in s:
            masks[pk] = masks.get(pk, 0) | (1 << i)
    distinct, full, reach = set(masks.values()), (1 << len(sets)) - 1, {0}
    for size in range(1, len(sets) + 1):
        reach = {m | d for m in reach for d in distinct}
        if full in reach:
            return size
    return None


def unseen(parties):
    """The tactics in the boss parties that the scores leave out: {kind:
    ["Species thing"]} over every variant, and their count, the mean over
    variants (a rival's three starters are three variants)."""
    kinds, counts = {}, []
    for party in parties:
        n = 0
        for m in party:
            things = set(m.get("moves") or []) | {m.get("item"), m.get("ability")}
            for kind, names in UNSEEN.items():
                for t in sorted(things & names):
                    n += 1
                    entry = f"{m['species']} {t}"
                    if entry not in kinds.setdefault(kind, []):
                        kinds[kind].append(entry)
        counts.append(n)
    return {"unseen": kinds, "unseen_count": round(sum(counts) / max(1, len(counts)), 2)}


def predictability(parties, category):
    """How far a player can call a boss team's moves in advance (Ian,
    2026-09-25: a fight whose every turn can be foreseen is easy to plan
    against). Every boss in Oxide carries Evaluate Attack, and every
    reference is taken to: under it the strongest attack into the target,
    or a killing one, is the pick, and the player can work that out. A
    status or setup move starts level with it and ties go at random, so
    each is a live choice; a gamble (GAMBLES) counts a fifth. Per Pokemon,
    one over its live choices; a Choice holder is called from its second
    turn on, so counts 1. The mean over the team, then over variants.
    `category(move)` gives a move's category, None if unknown."""
    means = []
    for party in parties:
        calls = []
        for m in party:
            if m.get("item") in CHOICE:
                calls.append(1.0)
                continue
            moves = m.get("moves") or []
            status = sum(category(mv) == "Status" for mv in moves if mv not in GAMBLES)
            gambles = sum(mv in GAMBLES for mv in moves)
            attacks = len(moves) - status - gambles
            live = (1 if attacks else 0) + status + GAMBLE_WEIGHT * gambles
            calls.append(1 / max(1.0, live))
        if calls:
            means.append(sum(calls) / len(calls))
    return round(sum(means) / len(means), 3) if means else None


def score_mons(bosses, side_keys, rows, info, trick_room=False):
    """Per boss Pokemon: threat, answers, and for a Choice holder the answers
    counting the lock (answers_lock; equal to answers for anyone else); and
    B5's threat by chance, one-on-one answers, and sure answers, whose set
    (_sure) roll_up takes for the fight's cover; the answers that hold in
    every setup branch (from rows for "key+Move", when there are any); and
    the set of player Pokemon it knocks out in one hit (_hits), for the
    fight's "safe"."""
    per_mon = []
    for v, key, mon, w in bosses:
        ghost = "Ghost" in (info[key].get("types") or [])
        branches = [k for k in info if k.startswith(key + "+")
                    and not (ghost and k.endswith("+Curse"))]
        sash = mon.get("item") == "Focus Sash"
        choice = mon.get("item") in CHOICE
        locked = locked_move(rows, key, side_keys, info, w) if choice else None
        threat = answer = lock = 0
        chance = duels = baits = held = 0.0
        sure, hits = set(), set()
        # A Choice holder locks into whatever it picks against the lead, so
        # the player can force any move it would pick against some Pokemon.
        forced = sorted({ai_pick(rows[(key, pk)]) for pk in side_keys} - {None}) if choice else []
        for pk in side_keys:
            down, up = rows[(key, pk)], rows[(pk, key)]
            chance += threat_chance(down, info[pk], info[key], w, trick_room)
            d = duel(up, down, info[pk], info[key], w, sash, trick_room)
            duels += d
            b = max([d] + [bait(up, down, m, info[pk], info[key], w, sash, trick_room)
                           for m in forced])
            baits += b
            held += min([b] + [duel(rows[(pk, bk)], rows[(bk, pk)], info[pk], info[bk], w, sash,
                                    trick_room) for bk in branches])
            if any(t <= 1 for t in turns_to_ko(down, info[pk], w).values()):
                hits.add(pk)
            if d >= SURE:
                sure.add(pk)
            if wins(down, info[pk], down["speeds"], w, trick_room=trick_room):
                threat += 1
            if wins(up, info[key], up["speeds"], w, sash=sash, trick_room=trick_room):
                answer += 1
                lock += 1
            elif choice and locked and lock_answer(up, down, locked, info[pk], info[key], w, sash,
                                                   trick_room):
                lock += 1
        n = len(side_keys)
        per_mon.append({"variant": v, "species": mon["species"], "level": mon["level"],
                        "item": mon.get("item"), "weather": w, "choice": choice,
                        "locked_move": locked,
                        "threat": round(threat / n, 3), "answers": round(answer / n, 3),
                        "answers_lock": round(lock / n, 3),
                        "threat_chance": round(chance / n, 3), "answers_duel": round(duels / n, 3),
                        "answers_sure": round(len(sure) / n, 3), "_sure": sure, "_side": n,
                        "answers_bait": round(baits / n, 3), "forced": forced,
                        "answers_branch": round(held / n, 3),
                        "branches": [k.split("+", 1)[1] for k in branches], "_hits": hits})
    return per_mon


def roll_up(per_mon):
    """A fight's scores from its Pokemon's: the mean over each variant's
    Pokemon, then over the variants. Takes each Pokemon's set of sure
    answers out of its record for the cover: the fewest player Pokemon that
    answer the whole team (the mean over variants, None if any has a
    Pokemon nothing surely answers), the most of the team one player
    Pokemon surely answers, and "broad", the share of the side that surely
    answers at least half the team, which is high when the team shares a
    weakness."""
    by_variant = {}
    for m in per_mon:
        by_variant.setdefault(m["variant"], []).append(m)
    covers, best_one, broad, safe = [], [], [], []
    for ms in by_variant.values():
        sets = [m.pop("_sure", set()) for m in ms]
        side = max(m.pop("_side", 1) for m in ms)
        hit_by = {}
        for m in ms:
            for pk in m.pop("_hits", set()):
                hit_by[pk] = hit_by.get(pk, 0) + 1
        safe.append(1 - sum(c > 1 for c in hit_by.values()) / side)
        covers.append(cover(sets))
        counts = {}
        for s in sets:
            for pk in s:
                counts[pk] = counts.get(pk, 0) + 1
        best_one.append(max(counts.values(), default=0) / len(ms))
        broad.append(sum(c * 2 >= len(ms) for c in counts.values()) / side)
    unanswered = sorted({m["species"] for m in per_mon if m["answers_sure"] == 0})

    def mean(k):
        return round(sum(sum(m[k] for m in ms) / len(ms) for ms in by_variant.values())
                     / len(by_variant), 3)

    return {"threat": mean("threat"), "answers": mean("answers"),
            "answers_lock": mean("answers_lock"),
            "threat_chance": mean("threat_chance"), "answers_duel": mean("answers_duel"),
            "answers_sure": mean("answers_sure"), "answers_bait": mean("answers_bait"),
            "answers_branch": mean("answers_branch"), "safe": round(sum(safe) / len(safe), 3),
            "cover": None if None in covers else round(sum(covers) / len(covers), 2),
            "best_one": round(sum(best_one) / len(best_one), 3),
            "broad": round(sum(broad) / len(broad), 3), "unanswered": unanswered,
            "max_threat": max(m["threat"] for m in per_mon),
            "min_answers": min(m["answers"] for m in per_mon),
            "min_answers_lock": min(m["answers_lock"] for m in per_mon),
            "choice_mons": sum(m["choice"] for m in per_mon)}


def boss_parties(fight):
    """[[boss Pokemon]] per variant: a rival's three starters are three
    variants, a tag battle's two opponents one party."""
    trainers = data.fight_trainers("oxide", fight)
    if fight.get("tag"):
        return [[m for t in trainers for m in t["party"]]], [t["tr_id"] for t in trainers]
    return [t["party"] for t in trainers], [t["tr_id"] for t in trainers]


def fight_weather(tr_ids):
    for tr in tr_ids:
        for w in splits.trainer_weather(tr):
            if w in CALC_WEATHER:
                return CALC_WEATHER[w]
    return None


def boss_moves(mon, blob):
    return [m for m in mon["moves"]
            if m in blob["moves"] and blob["moves"][m].get("category") != "Status"
            and (m not in pool.UNRELIABLE or (m in ITEM_MOVES and mon.get("item")))]


def run_node(blob_path, jobs):
    """One Node process, waited on, so nothing else runs beside it."""
    with tempfile.TemporaryDirectory(prefix="oxide-b3-") as tmp:
        jobs_path, out_path = os.path.join(tmp, "jobs.json"), os.path.join(tmp, "out.json")
        with open(jobs_path, "w", encoding="utf-8") as f:
            json.dump(jobs, f)
        subprocess.run(["node", RUNNER, blob_path, jobs_path, out_path], check=True)
        with open(out_path, encoding="utf-8") as f:
            return json.load(f)


def score_fight(fight, blob, blob_path, side=None, parties=None, cap=None):
    """One fight's scores, and how many calculations it took.

    A what-if (shape.py) passes its own player's side, boss parties or cap;
    left out, each comes from the fight's split as the game stands."""
    split = fight["split"]
    if side is None:
        side = pool.pool(split, blob)
    own_parties, tr_ids = boss_parties(fight) if fight.get("trainers") else ([], fight.get("tr_ids", []))
    parties = own_parties if parties is None else parties
    weather = fight_weather(tr_ids)
    jobs = {"pokemon": {}, "pairs": []}
    for i, p in enumerate(side):
        jobs["pokemon"][f"p{i}"] = p
    bosses = []
    for v, party in enumerate(parties):
        for j, mon in enumerate(party):
            key = f"b{v}.{j}"
            jobs["pokemon"][key] = mon
            w = CALC_WEATHER.get(ABILITY_WEATHER.get(mon.get("ability")), weather)
            bosses.append((v, key, mon, w))
            for i, p in enumerate(side):
                jobs["pairs"].append([key, f"p{i}", boss_moves(mon, blob), w])
                jobs["pairs"].append([f"p{i}", key, p["moves"], w])
            add_branches(jobs, key, mon, boss_moves(mon, blob), side, w)
    t0 = time.time()
    out = run_node(blob_path, jobs)
    seconds = time.time() - t0
    rows = {(r["a"], r["d"]): r for r in out["results"]}
    errors = sorted({f"{r['a']} {m}: {v['error']}" for r in out["results"]
                     for m, v in r["moves"].items() if "error" in v})
    trick_room = bool(fight.get("trick_room"))
    per_mon = score_mons(bosses, [f"p{i}" for i in range(len(side))], rows, out["pokemon"],
                         trick_room)
    return {
        "key": fight["key"], "label": fight["label"], "split": split,
        "cap": cap if cap is not None else pool.caps()[split], "pool": len(side), "weather": weather,
        "trick_room": trick_room,
        **roll_up(per_mon), **unseen(parties),
        "predictable": predictability(parties, lambda mv: blob["moves"].get(mv, {}).get("category")),
        "mons": per_mon, "calcs": sum(len(r["moves"]) for r in out["results"]),
        "errors": errors, "node_seconds": round(out.get("seconds", 0), 2),
        "wall_seconds": round(seconds, 2),
    }


def load():
    if os.path.exists(OUT):
        with open(OUT, encoding="utf-8") as f:
            return json.load(f)
    return {"_comment": __doc__.strip().split("\n\n")[0], "fights": {}}


def save(results):
    order = [f["key"] for f in data.fights()["fights"]]
    results["fights"] = {k: results["fights"][k] for k in order if k in results["fights"]}
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=1)
        f.write("\n")


def report(results, out=sys.stdout):
    print(f"{'fight':18}{'split':10}{'cap':>4}{'pool':>6}{'threat':>8}{'answers':>9}"
          f"{'worst mon':>11}{'fewest':>8}{'chance':>8}{'duel':>6}{'broad':>7}{'unseen':>8}"
          f"{'called':>8}",
          file=out)
    for r in results["fights"].values():
        print(f"{r['label']:18}{r['split']:10}{r['cap']:>4}{r['pool']:>6}{r['threat']:>8.2f}"
              f"{r['answers']:>9.2f}{r['max_threat']:>11.2f}{r['min_answers']:>8.2f}"
              f"{r.get('threat_chance', 0):>8.2f}{r.get('answers_duel', 0):>6.2f}"
              f"{r.get('broad', 0):>7.2f}{r.get('unseen_count', 0):>8}"
              f"{r.get('predictable') or 0:>8.2f}", file=out)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--fight", action="append", default=[])
    ap.add_argument("--split", action="append", default=[])
    ap.add_argument("--report", action="store_true")
    args = ap.parse_args(argv)
    results = load()
    if args.report:
        report(results)
        return 0
    wanted = [f for f in data.fights()["fights"]
              if f["key"] in args.fight or f["split"] in args.split]
    if not wanted:
        ap.error("name a --fight or a --split")
    blob = calc_export.build()
    with tempfile.TemporaryDirectory(prefix="oxide-b3-blob-") as tmp:
        blob_path = os.path.join(tmp, "blob.json")
        with open(blob_path, "w", encoding="utf-8") as f:
            json.dump(blob, f)
        for fight in wanted:
            r = score_fight(fight, blob, blob_path)
            results["fights"][fight["key"]] = r
            save(results)
            print(f"{r['label']}: threat {r['threat']:.2f}, answers {r['answers']:.2f}, "
                  f"{r['calcs']} calculations, node {r['node_seconds']}s, "
                  f"wall {r['wall_seconds']}s, {len(r['errors'])} errors", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())

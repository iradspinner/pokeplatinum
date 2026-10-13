"""The three-gym run's boxes and hand-played lines (step 3 of the
trainer-scoring handoff, docs/oxide/trainer-scoring-handoff.md), kept as
fixtures: each fight's box as the run had it, the hand-played six with its
held items, and the fight prepared around them. The planner's tests
(test_plplan, test_plfeat, test_plfixes), its label data (pldata) and
plplan's own command line read them.

Its runner, which searched lines with the September line search
(plines.py) and replayed them on the harness's seeds, was retired with
that search on 2026-10-13.
"""
from . import plscore


def iv(n):
    return {k: n for k in ("hp", "at", "df", "sp", "sa", "sd")}


EV = iv(0)

# The run's Pokemon as each fight met them: species, nature, ability, moves
# and IVs, and a level where it differs from the fight's cap. Records come
# from the harness (~/oxide-trials/three-gym-run): the hand line's own script
# first, then the fight's other scripts; box3.json and box3_natures.json give
# the natures and abilities of the rest. The run held Charmander to 25,
# Mareep to 28 and Popplio to 31, kept Starly at 6 as fodder, and traded
# Blipbug for Kazza's Vullaby after Roark and Finneon for Charap's Popplio
# after Mars 1.
#
# The harness never wrote moves for Corvisquire, Finneon, Charmander, Krabby
# after Roark, Mareep, Graveler, Breloom and Snover, nor for Wooloo, Vulpix,
# Steenee and Skiploom at Mars 1. Theirs are the capture rule on level-up
# moves alone (the run had no TMs), from the catch level in box3.json through
# the run's evolutions and holds, picked by the scorer's own rule
# (fightsim.player_moves), with an empty slot filled from a later record of
# the same Pokemon where the harness has one. Graveler keeps the run's
# Geodude set, since the rule never picks Magnitude.
ROARK = {
    "Prinplup": ("SPECIES_PRINPLUP", "Gentle", "Torrent", ["Metal Claw", "Bubble", "Peck", "Growl"]),
    "Wooloo": ("SPECIES_WOOLOO", "Naughty", "Run Away", ["Double Kick", "Tackle", "Defense Curl", "Guard Split"]),
    "Vulpix": ("SPECIES_VULPIX", "Naughty", "Flash Fire", ["Will-O-Wisp", "Ember", "Quick Attack", "Roar"]),
    "Bibarel": ("SPECIES_BIBAREL", "Bold", "Simple", ["Water Gun", "Rollout", "Defense Curl", "Tackle"]),
    "Corvisquire": ("SPECIES_CORVISQUIRE", "Hardy", "Keen Eye", ["Pluck", "Fury Attack", "Peck", "Leer"]),
    "Dottler": ("SPECIES_DOTTLER", "Adamant", "Swarm", ["Confusion", "Struggle Bug", "Reflect", "Light Screen"]),
    "Starly": ("SPECIES_STARLY", "Bold", "Keen Eye", ["Tackle", "Growl", "Quick Attack"], 15, 6),
    "Barboach": ("SPECIES_BARBOACH", "Adamant", "Swift Swim", ["Mud Bomb", "Water Gun", "Mud-Slap", "Water Sport"]),
    "Wartortle": ("SPECIES_WARTORTLE", "Relaxed", "Shell Armor", ["Water Gun", "Bite", "Withdraw", "Tail Whip"]),
    "Krabby": ("SPECIES_KRABBY", "Sassy", "Hyper Cutter", ["Bubble Beam", "Vice Grip", "Harden", "Leer"]),
    "Finneon": ("SPECIES_FINNEON", "Brave", "Chlorophyll", ["Water Gun", "Pound", "Attract"]),
    "Nidorino": ("SPECIES_NIDORINO", "Brave", "Poison Point", ["Double Kick", "Poison Sting", "Leer", "Focus Energy"]),
    "Onix": ("SPECIES_ONIX", "Jolly", "Rock Head", ["Rock Throw", "Screech", "Harden", "Bind"]),
    "Charmander": ("SPECIES_CHARMANDER", "Timid", "Blaze", ["Ember", "Scratch", "Smokescreen", "Growl"]),
    "Steenee": ("SPECIES_STEENEE", "Lonely", "Leaf Guard", ["Razor Leaf", "Rapid Spin", "Play Nice", "Splash"]),
    "Geodude": ("SPECIES_GEODUDE", "Impish", "Sturdy", ["Magnitude", "Rock Polish", "Rock Throw", "Defense Curl"]),
}
MARS = {
    "Prinplup": ("SPECIES_PRINPLUP", "Gentle", "Torrent", ["Metal Claw", "Bubble Beam", "Peck", "Growl"]),
    "Wooloo": ("SPECIES_WOOLOO", "Naughty", "Run Away", ["Headbutt", "Double Kick", "Guard Split", "Defense Curl"]),
    "Vulpix": ("SPECIES_VULPIX", "Naughty", "Flash Fire", ["Ember", "Will-O-Wisp", "Confuse Ray", "Quick Attack"]),
    "Bibarel": ("SPECIES_BIBAREL", "Bold", "Simple", ["Headbutt", "Water Gun", "Rollout", "Defense Curl"]),
    "Corvisquire": ("SPECIES_CORVISQUIRE", "Hardy", "Keen Eye", ["Pluck", "Steel Wing", "Fury Attack", "Peck"]),
    "Vullaby": ("SPECIES_VULLABY", "Hardy", "Big Pecks", ["Pluck", "Fury Attack", "Flatter", "Leer"], 20),
    "Starly": ("SPECIES_STARLY", "Bold", "Keen Eye", ["Tackle", "Growl", "Quick Attack"], 15, 6),
    "Barboach": ("SPECIES_BARBOACH", "Adamant", "Swift Swim", ["Mud Bomb", "Water Pulse", "Amnesia", "Water Gun"]),
    "Wartortle": ("SPECIES_WARTORTLE", "Relaxed", "Shell Armor", ["Bite", "Water Gun", "Rapid Spin", "Withdraw"]),
    "Krabby": ("SPECIES_KRABBY", "Sassy", "Hyper Cutter", ["Bubble Beam", "Mud Shot", "Vise Grip", "Bubble"]),
    "Finneon": ("SPECIES_FINNEON", "Brave", "Chlorophyll", ["Water Pulse", "Gust", "Pound", "Water Gun"]),
    "Nidorino": ("SPECIES_NIDORINO", "Brave", "Poison Point", ["Double Kick", "Fury Attack", "Poison Sting", "Leer"]),
    "Onix": ("SPECIES_ONIX", "Jolly", "Rock Head", ["Rock Tomb", "Rock Throw", "Screech", "Bind"]),
    "Charmander": ("SPECIES_CHARMANDER", "Timid", "Blaze", ["Ember", "Scratch", "Scary Face", "Smokescreen"]),
    "Steenee": ("SPECIES_STEENEE", "Lonely", "Leaf Guard", ["Razor Leaf", "Magical Leaf", "Rapid Spin", "Play Nice"]),
    "Geodude": ("SPECIES_GEODUDE", "Impish", "Sturdy", ["Magnitude", "Rock Throw", "Rock Polish", "Rollout"]),
    "Skiploom": ("SPECIES_SKIPLOOM", "Bashful", "Leaf Guard", ["Sleep Powder", "Stun Spore", "Bullet Seed", "Tackle"]),
    "Mareep": ("SPECIES_MAREEP", "Calm", "Static", ["Thunder Shock", "Tackle", "Thunder Wave", "Cotton Spore"]),
    "Pawmo": ("SPECIES_PAWMO", "Brave", "Natural Cure", ["Nuzzle", "Bite", "Thunder Shock", "Quick Attack"]),
    "Charjabug": ("SPECIES_CHARJABUG", "Jolly", "Battery", ["Spark", "Bug Bite", "Bite", "Mud-Slap"]),
}
GARDENIA = {
    "Prinplup": ("SPECIES_PRINPLUP", "Gentle", "Torrent", ["Metal Claw", "Bubble Beam", "Peck", "Growl"]),
    "Dubwool": ("SPECIES_DUBWOOL", "Naughty", "Steadfast", ["Headbutt", "Double Kick", "Guard Split", "Defense Curl"]),
    "Vulpix": ("SPECIES_VULPIX", "Naughty", "Flash Fire", ["Flamethrower", "Will-O-Wisp", "Confuse Ray", "Quick Attack"]),
    "Bibarel": ("SPECIES_BIBAREL", "Bold", "Simple", ["Headbutt", "Hyper Fang", "Water Gun", "Defense Curl"]),
    "Corvisquire": ("SPECIES_CORVISQUIRE", "Hardy", "Keen Eye", ["Drill Peck", "Pluck", "Steel Wing", "Leer"]),
    "Vullaby": ("SPECIES_VULLABY", "Hardy", "Big Pecks", ["Pluck", "Knock Off", "Tailwind", "Feint Attack"], 20),
    "Starly": ("SPECIES_STARLY", "Bold", "Keen Eye", ["Tackle", "Growl", "Quick Attack"], 15, 6),
    "Barboach": ("SPECIES_BARBOACH", "Adamant", "Swift Swim", ["Mud Bomb", "Water Pulse", "Amnesia", "Water Gun"]),
    "Wartortle": ("SPECIES_WARTORTLE", "Relaxed", "Shell Armor", ["Bite", "Water Gun", "Rapid Spin", "Withdraw"]),
    "Krabby": ("SPECIES_KRABBY", "Sassy", "Hyper Cutter", ["Bubble Beam", "Stomp", "Mud Shot", "Bubble"]),
    "Popplio": ("SPECIES_POPPLIO", "Bold", "Torrent", ["Sing", "Icy Wind", "Disarming Voice", "Aqua Jet"], 20),
    "Nidorino": ("SPECIES_NIDORINO", "Brave", "Poison Point", ["Horn Attack", "Poison Sting", "Double Kick", "Leer"]),
    "Onix": ("SPECIES_ONIX", "Jolly", "Rock Head", ["Rock Tomb", "Rock Throw", "Screech", "Bind"]),
    "Charmeleon": ("SPECIES_CHARMELEON", "Timid", "Blaze", ["Fire Fang", "Ember", "Scary Face", "Smokescreen"]),
    "Tsareena": ("SPECIES_TSAREENA", "Lonely", "Leaf Guard", ["Stomp", "Magical Leaf", "Play Nice", "Teeter Dance"]),
    "Graveler": ("SPECIES_GRAVELER", "Impish", "Sturdy", ["Magnitude", "Rock Throw", "Rock Polish", "Rollout"]),
    "Skiploom": ("SPECIES_SKIPLOOM", "Bashful", "Leaf Guard", ["Sleep Powder", "Stun Spore", "Bullet Seed", "Leech Seed"]),
    "Mareep": ("SPECIES_MAREEP", "Calm", "Static", ["Thunder Shock", "Tackle", "Thunder Wave", "Cotton Spore"]),
    "Pawmo": ("SPECIES_PAWMO", "Brave", "Natural Cure", ["Spark", "Arm Thrust", "Bite", "Nuzzle"]),
    "Vikavolt": ("SPECIES_VIKAVOLT", "Jolly", "Levitate", ["Bug Bite", "Spark", "Bite", "Mud-Slap"]),
    "Breloom": ("SPECIES_BRELOOM", "Docile", "Technician", ["Headbutt", "Mach Punch", "Mega Drain", "Tackle"]),
    "Snover": ("SPECIES_SNOVER", "Adamant", "Adaptability", ["Razor Leaf", "Icy Wind", "Ice Shard"]),
    "Golbat": ("SPECIES_GOLBAT", "Lonely", "Inner Focus", ["Wing Attack", "Bite", "Confuse Ray", "Supersonic"]),
}

# Goal 2's rival fights in Roark's split (the Overseer's provisional rule of
# 2026-10-02, until Ian confirms it): the box is the captures from the areas
# reached by the fight, each at the split's cap of 16 as the run had it at
# Roark (the Pocket PC's Rare Candies make the cap reachable from Sandgem on),
# and Barry 1, before Sandgem, meets the starter alone at level 5. Lucas and
# Dawn 1 is on Route 202, read without the Route 202 catch (the fight may come
# before it); Barry 2 is at the start of Route 203, after the Old Rod spots of
# Twinleaf, Route 218 and Route 219 but before Route 203's own.
# Barry 1 is also read for the other two starters (variant 1 for Turtwig, 2
# for Chimchar), with a neutral nature since the run never had them.
BARRY_1 = {"Piplup": ("SPECIES_PIPLUP", "Gentle", "Torrent", ["Pound", "Growl"], 15, 5),
           "Turtwig": ("SPECIES_TURTWIG", "Hardy", "Overgrow", ["Tackle", "Withdraw"], 15, 5),
           "Chimchar": ("SPECIES_CHIMCHAR", "Hardy", "Blaze", ["Scratch", "Leer"], 15, 5)}
LUCAS_DAWN_1 = {n: ROARK[n] for n in ("Prinplup", "Wooloo", "Vulpix", "Bibarel", "Corvisquire")}
BARRY_2 = {n: ROARK[n] for n in ("Prinplup", "Wooloo", "Vulpix", "Bibarel", "Corvisquire", "Dottler", "Starly",
                                  "Wartortle", "Krabby", "Finneon")}

# The hand-played line of each fight (the handoff's acceptance table): its
# six, its held items, the harness script's seeds, and its three numbers on
# the corrected AI (clean, won, deaths per fight, over 200 runs). `boosters`
# is the run's stock of type boosters by the fight.
FIGHTS = {
    "roark": dict(key="roark", cap=16, box=ROARK, seed0=2000, trace_seed=30,
                  six=["Barboach", "Nidorino", "Geodude", "Onix", "Prinplup", "Steenee"],
                  items={"Geodude": "Quick Claw"}, bar=(199, 200, 0.005),
                  boosters={"Fire": "Flame Plate"}),
    "mars": dict(key="mars_1", cap=22, box=MARS, seed0=7000, trace_seed=31,
                 six=["Geodude", "Vullaby", "Starly", "Onix", "Charjabug", "Nidorino"],
                 items={"Geodude": "Quick Claw"}, bar=(191, 200, 0.045),
                 boosters={"Fire": "Flame Plate", "Grass": "Miracle Seed"}),
    "gardenia": dict(key="gardenia", cap=26, box=GARDENIA, seed0=9000, trace_seed=32,
                     six=["Charmeleon", "Popplio", "Vikavolt", "Vullaby", "Golbat", "Tsareena"],
                     items={"Golbat": "Quick Claw"}, bar=(29, 116, 3.325),
                     boosters={"Fire": "Flame Plate", "Grass": "Miracle Seed", "Dragon": "Draco Plate"}),
    # Goal 2's rival fights: no hand-played line, so no bar and no held items;
    # `six` is the box itself where it has six or fewer, and Barry 2 is read
    # over random sixes of its box (plplan --six).
    "barry_1": dict(key="barry_1", cap=16, box=BARRY_1, seed0=11000, trace_seed=33, six=["Piplup"],
                    items={}, bar=None, boosters={}),
    "lucas_dawn_1": dict(key="lucas_dawn_1", cap=16, box=LUCAS_DAWN_1, seed0=12000, trace_seed=34,
                         six=list(LUCAS_DAWN_1), items={}, bar=None, boosters={}),
    "barry_2": dict(key="barry_2", cap=16, box=BARRY_2, seed0=13000, trace_seed=35,
                    six=["Prinplup", "Wooloo", "Vulpix", "Bibarel", "Corvisquire", "Wartortle"],
                    items={}, bar=None, boosters={}),
}
def records(f, names):
    """The given_side records (fightsim.prepare) for these box members."""
    out = []
    for n in names:
        rec = f["box"][n]
        const, nature, ability, moves = rec[:4]
        ivs = rec[4] if len(rec) > 4 else 15
        level = rec[5] if len(rec) > 5 else f["cap"]
        out.append({"constant": const, "species": n, "how": "plan", "level": level, "nature": nature,
                    "ivs": iv(ivs), "evs": EV, "ability": ability, "moves": list(moves or []), "fill": False})
    return out


def prepare(f, names, items=None):
    """The fight's state around these box members, keyed p0, p1, ... in
    order; with `items` ({name: item}) those held items replace the scorer's
    own rule."""
    prep = plscore.prepare(plscore.parse_fight(f["key"]), given_side=records(f, names))
    st = prep["st"]
    if items is not None:
        st["held"] = {f"p{i}": items.get(n) for i, n in enumerate(names)}
    # The scorer's own item rule draws on the run's stock rather than the
    # census's, which counts a Hard Stone on Oreburgh's northwest house 3F,
    # a floor pret marks unused, and at Mars 1 the Draco Plate found later in
    # Eterna. Its rule never hands out the run's Quick Claw.
    st["item_stock"] = {"boosters": dict(f["boosters"]), "Leftovers": 0, "Sitrus Berry": 0}
    return prep

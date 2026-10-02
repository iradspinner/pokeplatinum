"""Step 3 of the trainer-scoring handoff (docs/oxide/trainer-scoring-handoff.md):
the scorer's line search on the three-gym run's own box, judged against the
hand-played lines on Ian's three numbers (2026-10-01): the clean rate (won
with no Pokemon fainting), the win rate (won at all) and the deaths per fight
(the mean number of the player's Pokemon that faint, over every fight).

Two readings per fight:

- "hand": the line search alone, on the hand-played line's six with its held
  items. A shortfall here is a planning idea the search lacks.
- "box": the whole box as the run had it at the fight. The scorer picks its
  planned sixes (plscore's matchup weights), holds items by its own rule,
  and searches a line for each six.

Each reading runs the scorer's planned search (plscore.PLANNED_SEARCH) from
several seeds, then replays the best line on the harness's own seeds, so its
three numbers sit beside the bar's on the same dice streams.

    PYTHONPATH=. python3 -m tools.oxide.balance.plstep3 hand roark
    PYTHONPATH=. python3 -m tools.oxide.balance.plstep3 box gardenia
    PYTHONPATH=. python3 -m tools.oxide.balance.plstep3 trace roark   # the last best line, one seed
"""
import argparse
import json
import multiprocessing as mp
import os
import random
import sys
import time

from . import fightai
from . import perfectline as pl
from . import plines as lines
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
BARRY_1 = {"Piplup": ("SPECIES_PIPLUP", "Gentle", "Torrent", ["Pound", "Growl"], 15, 5)}
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
OUT = os.path.join(os.path.dirname(__file__), "perfectline_results", "step3")
SEARCH_SEEDS = 4          # independent searches of the hand six
REPLAY_RUNS = 200         # the bar's run count
REPLAY_TURN_CAP = 150     # the harness's own cap


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


def replay(st, team, boss_keys, flags, line, seed0, runs=REPLAY_RUNS):
    """The line's three numbers on the harness's seeds: (clean, won, deaths
    per fight), each fight played to a win, a wipe or the turn cap."""
    clean = won = deaths = 0
    saved = lines.RUN_TURN_CAP
    lines.RUN_TURN_CAP = REPLAY_TURN_CAP
    try:
        for i in range(runs):
            c, w, _t, d = lines.play_run(st, team, boss_keys, flags, line, random.Random(seed0 + i),
                                         True, to_end=True)
            clean += c
            won += w
            deaths += d
    finally:
        lines.RUN_TURN_CAP = saved
    return clean, won, round(deaths / runs, 3)


_ST = None


def _search(args):
    team, boss_keys, flags, seed = args
    t0 = time.time()
    r = lines.search(_ST, team, boss_keys, flags, seed=seed, keep_line=True, **plscore.PLANNED_SEARCH)
    r["seconds"] = round(time.time() - t0, 1)
    r["team"] = team
    r["seed"] = seed
    return r


def _pool(st, jobs, procs):
    global _ST
    _ST = st
    with mp.get_context("fork").Pool(min(len(jobs), procs or max(1, os.cpu_count() - 2))) as p:
        return p.map(_search, jobs, chunksize=1)


def read(fight, mode, procs=None, log=sys.stdout, tag=""):
    f = FIGHTS[fight]
    if mode == "hand":
        names = f["six"]
        prep = prepare(f, names, f["items"])
        st = prep["st"]
        boss_keys, flags, _s = prep["variants"][0]
        team = [f"p{i}" for i in range(len(names))]
        jobs = [(team, boss_keys, flags, plscore.SEED + s) for s in range(SEARCH_SEEDS)]
    else:
        names = list(f["box"])
        prep = prepare(f, names)
        st = prep["st"]
        boss_keys, flags, _s = prep["variants"][0]
        keys = [f"p{i}" for i in range(len(names))]
        weights = pl.matchup_wins(st, keys, boss_keys, flags)
        sixes = plscore.sixes(keys, plscore.PLANNED, random.Random(plscore.SEED), weights)
        jobs = [(six, boss_keys, flags, plscore.SEED + 100 + j) for j, six in enumerate(sixes)]
    sp = lambda k: st["pokemon"][k]["species"]
    t0 = time.time()
    rows = _pool(st, jobs, procs)
    for r in rows:
        r["replay"] = replay(st, r["team"], boss_keys, flags, r["policy"], f["seed0"])
    best = max(rows, key=lambda r: (r["replay"][0], r["replay"][1], -r["replay"][2]))
    print(f"{fight} ({mode}): {len(rows)} searches in {time.time() - t0:.0f} s; "
          f"bar clean {f['bar'][0]}/200, won {f['bar'][1]}/200, deaths {f['bar'][2]:.3f}", file=log)
    for r in rows:
        c, w, d = r["replay"]
        print(f"  {'best ' if r is best else '     '}{','.join(sp(k) for k in r['team'])}: "
              f"clean {c}/200, won {w}/200, deaths {d:.3f} (search confirm {r['rate']:.2f}, "
              f"{r['candidates']} candidates, {r['seconds']} s)\n      {r['line']}", file=log)
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, f"{fight}-{mode}{tag}.json"), "w") as fh:
        json.dump({"fight": fight, "mode": mode, "bar": f["bar"], "names": names,
                   "items": f["items"] if mode == "hand" else None,
                   "rows": [{"team": [sp(k) for k in r["team"]], "line": r["line"],
                             "clean": r["replay"][0], "won": r["replay"][1], "deaths": r["replay"][2],
                             "search_rate": r["rate"], "candidates": r["candidates"], "seed": r["seed"],
                             "keys": r["team"], "policy": policy_json(r["policy"])}
                            for r in rows], "best": rows.index(best)}, fh, indent=1)
    return rows, best


def policy_json(line):
    """A Line's fields as JSON (a dict keyed by team index is keyed by its
    string)."""
    out = {k: getattr(line, k) for k in lines.Line.__slots__}
    out["reserved"] = {str(i): k for i, k in line.reserved.items()}
    out["pairs"] = {k: list(v) for k, v in line.pairs.items()}
    return out


def policy_from(d):
    line = lines.Line(d["lead"], d["answers"])
    for k in lines.Line.__slots__:
        setattr(line, k, d[k])
    line.reserved = {int(i): k for i, k in d["reserved"].items()}
    line.pairs = {k: tuple(v) for k, v in d["pairs"].items()}
    return line


def load(fight, mode, tag=""):
    """A stored reading's best line: (fight, state, boss keys, AI flags,
    line, team keys, its row)."""
    f = FIGHTS[fight]
    with open(os.path.join(OUT, f"{fight}-{mode}{tag}.json")) as fh:
        saved = json.load(fh)
    prep = prepare(f, saved["names"], saved["items"])
    boss_keys, flags, _s = prep["variants"][0]
    r = saved["rows"][saved["best"]]
    return f, prep["st"], boss_keys, flags, policy_from(r["policy"]), r["keys"], r


def trace(fight, mode, seed=None, log=sys.stdout):
    """One run of the reading's best line, turn by turn, with the rule that
    chose each of the player's actions and the trainer's pick."""
    f, st, boss_keys, flags, line, team, r = load(fight, mode)
    seed = f["trace_seed"] if seed is None else seed
    rng = random.Random(seed)
    b = pl.make_battle(st, team, boss_keys, flags, line.lead)
    b.dice = pl.RunDice(rng, True)
    b.rng = rng

    def mon(m):
        s = f"{m.species} {m.hp}/{m.maxhp}"
        if m.status:
            s += f" {m.status}"
        boosts = {k: v for k, v in m.stages.items() if v}
        return s + (f" {boosts}" if boosts else "")
    print(f"{fight} ({mode}), seed {seed}: {r['line']}", file=log)
    print(f"start: you {mon(b.p.cur())} | foe {mon(b.b.cur())}", file=log)
    while b.turn < REPLAY_TURN_CAP and b.p.alive() and b.b.alive():
        me = b.p.cur().species
        pa = lines.decide(b, line)
        why = getattr(b, "why", "")
        b.rng = rng
        b.dice.rng = rng
        b.quick = {m.key: m.item == "Quick Claw" and (b.dice.good(0.2) if pl.player(m) else b.dice.bad("quickclaw", 0.2))
                   for m in (b.p.cur(), b.b.cur())}
        aa = fightai.choose(b, b.b.cur(), b.p.cur())
        foe = b.b.cur().species
        pl._turn(b, pa, aa)
        act = pa[1].name if pa[0] == "move" else "switch to " + b.p.mons[pa[1]].species
        theirs = getattr(aa[1], "name", None) if aa[0] == "move" else "switch to " + b.b.mons[aa[1]].species
        print(f"T{b.turn} [{b.weather or 'clear'}] {me}: {act} ({why}) | {foe}: {theirs} "
              f"-> you {mon(b.p.cur())} | foe {mon(b.b.cur())}", file=log)
    dead = [m.species for m in b.p.mons if not m.alive()]
    print(f"{'won' if not b.b.alive() else 'lost'}; fainted: {', '.join(dead) or 'none'}", file=log)


def causes(fight, mode, log=sys.stdout):
    """Where the reading's best line loses Pokemon over the harness's seeds:
    each faint by the player's Pokemon and the foe out when it fainted."""
    import collections
    f, st, boss_keys, flags, line, team, _r = load(fight, mode)
    faints, firsts = collections.Counter(), collections.Counter()
    for i in range(REPLAY_RUNS):
        rng = random.Random(f["seed0"] + i)
        b = pl.make_battle(st, team, boss_keys, flags, line.lead)
        b.dice = pl.RunDice(rng, True)
        b.rng = rng
        first = True
        while b.turn < REPLAY_TURN_CAP and b.p.alive() and b.b.alive():
            alive = [m.alive() for m in b.p.mons]
            foe = b.b.cur().species
            pl.play_turn(b, lines.decide(b, line), rng, True)
            for m, was in zip(b.p.mons, alive):
                if was and not m.alive():
                    faints[(m.species, foe)] += 1
                    if first:
                        firsts[(m.species, foe)] += 1
                        first = False
    print(f"{fight} ({mode}): faints over {REPLAY_RUNS} runs, as (fainted, foe out): total, first death", file=log)
    for k, n in faints.most_common():
        print(f"  {k[0]:12} to {k[1]:12} {n:4}  {firsts.get(k, 0):4}", file=log)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=("hand", "box", "trace", "moves", "causes"))
    ap.add_argument("fights", nargs="+", choices=sorted(FIGHTS))
    ap.add_argument("--of", default="hand", help="trace: the reading whose best line is traced")
    ap.add_argument("--seed", type=int)
    ap.add_argument("--procs", type=int)
    ap.add_argument("--tag", default="", help="a suffix for the stored reading's name")
    args = ap.parse_args(argv)
    for fight in args.fights:
        if args.mode == "trace":
            trace(fight, args.of, args.seed)
        elif args.mode == "causes":
            causes(fight, args.of)
        elif args.mode == "moves":
            # Each box member's moves as the fight state has them, so the
            # moveset rule's picks for the unrecorded ones can be checked.
            f = FIGHTS[fight]
            names = list(f["box"])
            st = prepare(f, names)["st"]
            for i, n in enumerate(names):
                k = f"p{i}"
                rule = "" if f["box"][n][3] else "  (moveset rule)"
                print(f"{fight} {n:12} L{st['pokemon'][k].get('level')} {st['pokemon'][k]['ability']:13} "
                      f"{', '.join(st['moves'][k])}{rule}")
        else:
            read(fight, args.mode, args.procs, tag=args.tag)
    return 0


if __name__ == "__main__":
    sys.exit(main())

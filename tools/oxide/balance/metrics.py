"""B2: the structural metrics, per story fight, for Oxide and every reference.

    PYTHONPATH=. python3 -m tools.oxide.balance.metrics              # every boss, every hack
    PYTHONPATH=. python3 -m tools.oxide.balance.metrics roark        # one fight in detail
    PYTHONPATH=. python3 -m tools.oxide.balance.metrics --order      # the B2 check's table
    PYTHONPATH=. python3 -m tools.oxide.balance.metrics --filler     # filler trainers per split

Every number is read from the hack's own data where the hack has it: its own
species stats and move table, else a shared fallback that the output counts.
The metrics are the plan's first group (docs/oxide/balance-plan.md, "What gets
measured"). They are cheap and structural: nothing here runs a damage roll.

Three choices worth knowing when reading the numbers:

- A rival fight lists one trainer per starter; its metrics are the mean over
  the three. A tag battle's two opponents are scored as one party.
- "Nature fit" is how the plan's "are natures chosen" is read from data,
  since no source says whether a nature was picked or rolled. A nature fits
  when it raises something and lowers neither the Pokemon's attacking stat
  nor its Speed, and it either raises one of those two or lowers the
  attacking stat it does not use. A rolled nature fits about one time in
  three (8 of the 25); a picked one nearly always does. A slow Pokemon that
  trades Speed for its attacking stat (Brave, Quiet) also fits, since that
  is a choice too; a whole Trick Room team would still read as unfit, and
  none of the story fights is one.
- Base stat totals are reported as they are. The plan's percentile of what
  the player can own by then needs the player's pool, which is B3.
"""
import functools
import json
import os
import statistics
import sys

from . import data

NFE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "nfe.json")
PLATINUM = ["oxide"] + [h for h in data.REFS if data.REFS[h]["game"] == "platinum"]
STATS = ("hp", "at", "df", "sa", "sd", "sp")

# Which generation's "not fully evolved" list a hack is read with, where it
# has no evolution data of its own. Oxide reads its own res/pokemon records.
NFE_GEN = {"vanilla": "gen4", "renegade": "gen4", "redux": "gen4", "redux_hc": "gen4",
           "kaizo": "gen4", "hardlove": "gen9", "null": "gen9", "unbound": "gen8",
           "run_and_bun": "gen8"}
# Species that gained their only evolution in Generation 9. A Generation 9
# hack counts them as unevolved only if its species list has the evolution.
LATE_EVOLUTIONS = {"Primeape": "Annihilape", "Dunsparce": "Dudunsparce",
                   "Girafarig": "Farigiraf", "Stantler": "Wyrdeer", "Ursaring": "Ursaluna",
                   "Bisharp": "Kingambit", "Duraludon": "Archaludon"}
# Spellings in a source that the shared species table spells otherwise.
SPECIES_ALIASES = {"Enamorus-T": "Enamorus-Therian", "Ho-oh": "Ho-Oh"}

NATURES = {
    "Hardy": (None, None), "Lonely": ("at", "df"), "Brave": ("at", "sp"),
    "Adamant": ("at", "sa"), "Naughty": ("at", "sd"), "Bold": ("df", "at"),
    "Docile": (None, None), "Relaxed": ("df", "sp"), "Impish": ("df", "sa"),
    "Lax": ("df", "sd"), "Timid": ("sp", "at"), "Hasty": ("sp", "df"),
    "Serious": (None, None), "Jolly": ("sp", "sa"), "Naive": ("sp", "sd"),
    "Modest": ("sa", "at"), "Mild": ("sa", "df"), "Quiet": ("sa", "sp"),
    "Bashful": (None, None), "Rash": ("sa", "sd"), "Calm": ("sd", "at"),
    "Gentle": ("sd", "df"), "Sassy": ("sd", "sp"), "Careful": ("sd", "sa"),
    "Quirky": (None, None),
}

# The move-quality groups, by name, the same for every hack. A hack rarely
# changes what one of these does, and names are the one thing every source
# shares. Priority also counts any damaging move whose own table gives it
# positive priority.
SETUP = {"Swords Dance", "Dragon Dance", "Nasty Plot", "Calm Mind", "Bulk Up", "Agility",
         "Rock Polish", "Quiver Dance", "Shell Smash", "Shift Gear", "Coil", "Curse",
         "Work Up", "Growth", "Howl", "Iron Defense", "Amnesia", "Cosmic Power",
         "Belly Drum", "Tail Glow", "Meditate", "Sharpen", "Acid Armor", "Barrier",
         "Hone Claws", "Cotton Guard", "Victory Dance", "Tidy Up", "Geomancy",
         "No Retreat", "Clangorous Soul", "Minimize", "Double Team", "Autotomize",
         "Stockpile", "Defend Order", "Charge", "Take Heart", "Filet Away"}
HAZARDS = {"Stealth Rock", "Spikes", "Toxic Spikes", "Sticky Web", "Stone Axe",
           "Ceaseless Edge"}
PRIORITY = {"Quick Attack", "Mach Punch", "Bullet Punch", "Ice Shard", "Aqua Jet",
            "Shadow Sneak", "Vacuum Wave", "Sucker Punch", "Extreme Speed", "ExtremeSpeed",
            "Fake Out", "Accelerock", "Jet Punch", "First Impression", "Water Shuriken",
            "Feint", "Grassy Glide", "Thunderclap", "Upper Hand"}
SPEED_CONTROL = {"Thunder Wave", "Glare", "Stun Spore", "Icy Wind", "Electroweb",
                 "Rock Tomb", "Bulldoze", "Mud Shot", "Low Sweep", "String Shot",
                 "Scary Face", "Cotton Spore", "Trick Room", "Tailwind", "Nuzzle",
                 "Bitter Malice", "Drum Beating", "Pounce", "Zap Cannon", "Sticky Web",
                 "Mud-Slap", "Bubble Beam", "BubbleBeam", "Constrict", "Bubble"}
RECOVERY = {"Recover", "Roost", "Soft-Boiled", "Softboiled", "Slack Off", "Milk Drink",
            "Moonlight", "Morning Sun", "Synthesis", "Wish", "Rest", "Heal Order",
            "Shore Up", "Strength Sap", "Leech Seed", "Ingrain", "Aqua Ring",
            "Pain Split", "Life Dew", "Swallow", "Lunar Blessing", "Jungle Healing"}
# Moves whose damage does not depend on type matchups, left out of coverage.
FIXED_DAMAGE = {"Seismic Toss", "Night Shade", "Dragon Rage", "Sonic Boom", "SonicBoom",
                "Super Fang", "Endeavor", "Psywave", "Counter", "Mirror Coat",
                "Metal Burst", "Bide", "Final Gambit", "Nature's Madness", "Ruination"}
# Damaging moves whose power is worked out in battle, which some tables store
# as 0 and which have no category in a table that lacks the column.
VARIABLE_POWER = {"Low Kick", "Grass Knot", "Gyro Ball", "Electro Ball", "Heavy Slam",
                  "Heat Crash", "Return", "Frustration", "Reversal", "Flail",
                  "Crush Grip", "Wring Out", "Punishment", "Magnitude", "Present",
                  "Trump Card", "Natural Gift", "Fling", "Beat Up", "Hidden Power"}

# Which defending types an attacking type hits for double damage, from
# Generation 6 on. Generation 4's list is the same without Fairy.
SUPER_EFFECTIVE = {
    "Fire": {"Grass", "Ice", "Bug", "Steel"}, "Water": {"Fire", "Ground", "Rock"},
    "Electric": {"Water", "Flying"}, "Grass": {"Water", "Ground", "Rock"},
    "Ice": {"Grass", "Ground", "Flying", "Dragon"},
    "Fighting": {"Normal", "Ice", "Rock", "Dark", "Steel"},
    "Poison": {"Grass", "Fairy"}, "Ground": {"Fire", "Electric", "Poison", "Rock", "Steel"},
    "Flying": {"Grass", "Fighting", "Bug"}, "Psychic": {"Fighting", "Poison"},
    "Bug": {"Grass", "Psychic", "Dark"}, "Rock": {"Fire", "Ice", "Flying", "Bug"},
    "Ghost": {"Psychic", "Ghost"}, "Dragon": {"Dragon"}, "Dark": {"Psychic", "Ghost"},
    "Steel": {"Ice", "Rock", "Fairy"}, "Fairy": {"Fighting", "Dragon", "Dark"},
    "Normal": set(),
}
HIDDEN_POWER_TYPES = ["Fighting", "Flying", "Poison", "Ground", "Rock", "Bug", "Ghost",
                      "Steel", "Fire", "Water", "Grass", "Electric", "Psychic", "Ice",
                      "Dragon", "Dark"]
AI_FLAGS = ["basic", "eval attack", "expert", "setup", "risky", "damage priority",
            "baton pass", "tag strategy", "check HP", "weather", "harassment"]

# The metrics the B2 check orders vanilla, Renegade and Kaizo on. Higher
# reads as harder for each of them. The rest are reported, not ordered:
# relative levels are about the curve rather than difficulty, and AI flags
# and doubles are too few distinct values to order.
ORDERED = ["party_size", "ace_level", "mean_level", "mean_iv", "nature_fit",
           "item_share", "evolved_share", "mean_bst", "setup", "hazards", "priority",
           "speed_control", "recovery", "coverage"]


# ---- species and moves, per hack --------------------------------------------

def _norm_stats(bs):
    return {k: bs[k] for k in STATS}


@functools.lru_cache(maxsize=None)
def _canon():
    from ..encounters import canon
    long = {"hp": "hp", "attack": "at", "defense": "df", "special_attack": "sa",
            "special_defense": "sd", "speed": "sp"}
    return {name: {"bs": {long[k]: v for k, v in rec["stats"].items()}, "types": rec["types"]}
            for name, rec in canon.table().items()}


@functools.lru_cache(maxsize=None)
def _oxide_tables():
    """Oxide's species, moves and type chart, as the calculator export builds
    them from res/ and the battle code, plus which species evolve."""
    from ..encounters import calc_export, canon, model, pokedex
    root = model.repo_root()
    species, evolves = {}, {}
    for sp in pokedex.species_list(root):
        rec, name = pokedex.load(root, sp), canon.showdown_name(sp)
        if rec is None or not name:
            continue
        species[name] = calc_export.species_entry(rec)
        evolves[name] = any(e["into"] and e["into"] != "SPECIES_NONE" and not e["form"]
                            for e in rec["evolutions"])
    for name, rec in calc_export.forms(root).items():
        species[name] = calc_export.species_entry(rec)
        evolves[name] = any(e["into"] and e["into"] != "SPECIES_NONE" and not e["form"]
                            for e in rec.get("evolutions") or [])
    moves = {}
    for rec in pokedex.moves(root).values():
        if rec["move"] == "MOVE_NONE" or rec["name"] in ("-", ""):
            continue
        known = calc_export.move_name(rec)
        moves[known or rec["name"]] = calc_export.move_entry(rec, bool(known))
    chart = pokedex.type_chart(root)
    types = sorted({calc_export.type_name(a) for a, _ in chart}
                   | {calc_export.type_name(d) for _, d in chart})
    types = [t for t in types if t in SUPER_EFFECTIVE]
    se = {t: set() for t in types}
    for (a, d), mult in chart.items():
        if mult >= 2 and calc_export.type_name(a) in se:
            se[calc_export.type_name(a)].add(calc_export.type_name(d))
    return species, moves, se, evolves


@functools.lru_cache(maxsize=None)
def species_table(hack):
    """{species: {"bs", "types"}} from the hack's own data, or {} where it has
    none (Unbound and Run & Bun, which fall back to the shared table)."""
    if hack == "oxide":
        return {k: {"bs": _norm_stats(v["bs"]), "types": v["types"]}
                for k, v in _oxide_tables()[0].items()}
    if hack in ("unbound", "run_and_bun"):
        return {}
    return {k: {"bs": _norm_stats(v["bs"]), "types": v.get("types")}
            for k, v in data.raw(hack)["poks"].items() if set(STATS) <= set(v.get("bs", {}))}


def _move(v):
    power = v.get("basePower", v.get("bp")) or 0
    return {"type": v.get("type"), "power": power, "category": v.get("category"),
            "priority": v.get("priority") or 0}


@functools.lru_cache(maxsize=None)
def move_table(hack):
    """{move: {"type", "power", "category", "priority"}} from the hack's own
    data, or {} where it has none."""
    if hack == "oxide":
        return {k: _move(v) for k, v in _oxide_tables()[1].items()}
    if hack in ("unbound", "run_and_bun"):
        return {}
    return {k: _move(v) for k, v in data.raw(hack)["moves"].items()}


# Where a move is missing from a hack's own table, these are asked in turn.
# Hardlove's table is the newest and carries the physical and special split.
MOVE_FALLBACK = ("hardlove", "null", "oxide")


def _compact(name):
    return "".join(ch for ch in name.lower() if ch.isalnum())


@functools.lru_cache(maxsize=None)
def _compact_index(hack):
    """A hack's moves keyed without spaces or punctuation, since Generation 4
    tables spell some names run together (SmokeScreen, ExtremeSpeed)."""
    return {_compact(k): v for k, v in move_table(hack).items()}


def lookup_move(hack, name):
    """(record, source hack) for a move, or (None, None)."""
    for source in (hack,) + MOVE_FALLBACK:
        rec = move_table(source).get(name) or _compact_index(source).get(_compact(name))
        if rec:
            if not rec["category"]:
                # Null's table has no category column; borrow one by name.
                for other in MOVE_FALLBACK:
                    cat = move_table(other).get(name, {}).get("category")
                    if cat:
                        rec = dict(rec, category=cat)
                        break
            return rec, source
    return None, None


def mon_stats(hack, mon):
    """(base stats, types, source) for a party member, or (None, None, None)."""
    if mon.get("base_stats"):
        return _norm_stats(mon["base_stats"]), mon.get("types"), hack
    name = SPECIES_ALIASES.get(mon["species"], mon["species"])
    for table, source in ((species_table(hack), hack), (_canon(), "canon")):
        rec = table.get(name) or table.get(mon["species"])
        if rec:
            return rec["bs"], rec["types"], source
    return None, None, None


@functools.lru_cache(maxsize=None)
def _nfe_lists():
    with open(NFE_FILE, encoding="utf-8") as f:
        return {k: set(v) for k, v in json.load(f).items()}


@functools.lru_cache(maxsize=None)
def _species_names(hack):
    if hack == "hardlove":
        return {m["species"] for t in data.ref_trainers(hack).values() for m in t["party"]} \
            | set(data.raw("hardlove")["poks"].get(k, {}).get("name", k)
                  for k in data.raw("hardlove")["poks"])
    return set(species_table(hack))


def is_evolved(hack, mon):
    """Whether a party member is fully evolved in its own game. A Mega is."""
    name = SPECIES_ALIASES.get(mon["species"], mon["species"])
    if mon.get("mega") or "-Mega" in name:
        return True
    if hack == "oxide":
        evolves = _oxide_tables()[3]
        if name in evolves:
            return not evolves[name]
    gen = NFE_GEN.get(hack, "gen9")
    if name not in _nfe_lists()[gen]:
        return True
    late = LATE_EVOLUTIONS.get(name)
    if late and gen == "gen9" and late not in _species_names(hack):
        return True
    return False


def se_table(hack):
    """{attacking type: defending types hit for double damage} for the hack."""
    if hack == "oxide":
        return _oxide_tables()[2]
    if data.REFS[hack]["game"] == "platinum":
        return {a: d - {"Fairy"} for a, d in SUPER_EFFECTIVE.items() if a != "Fairy"}
    return SUPER_EFFECTIVE


def hidden_power_type(mon):
    ivs = mon.get("ivs")
    if not ivs:
        return None
    bits = sum((ivs[k] & 1) << i for i, k in enumerate(("hp", "at", "df", "sp", "sa", "sd")))
    return HIDDEN_POWER_TYPES[bits * 15 // 63]


def damaging(rec, name):
    if rec is None:
        return name in VARIABLE_POWER
    if rec["category"] in ("Physical", "Special"):
        return True
    if rec["category"] == "Status":
        return False
    return rec["power"] > 0 or name in VARIABLE_POWER


def move_type(hack, mon, name, rec):
    if name.startswith("Hidden Power"):
        suffix = name[len("Hidden Power"):].strip()
        return suffix.title() if suffix else hidden_power_type(mon)
    return rec["type"] if rec else None


# ---- one party member, one trainer, one fight -------------------------------

SLOW = 60


def nature_fits(nature, used, speed):
    """Whether a nature reads as picked for this Pokemon (module docstring).
    A slow Pokemon (base Speed 60 or less) that trades Speed for its
    attacking stat, Brave or Quiet, counts as picked too: Renegade gives
    Brave to its Rhyperior-like Pokemon on purpose."""
    plus, minus = NATURES.get(nature, (None, None))
    if plus is None:
        return False
    unused = "sa" if used == "at" else "at"
    if minus == "sp" and plus == used and speed is not None and speed <= SLOW:
        return True
    if minus in (used, "sp"):
        return False
    return plus in (used, "sp") or minus == unused


def default_moves(hack, mon):
    """The moves a party member with none listed knows in battle: the last
    four it learns by level, the way the game fills them, from the hack's
    own learnsets. Vanilla's calculator file lists no moves for 487 of its
    1,873 sets (Barry 1 among the story fights) because the game fills them;
    a hack with no learnsets in its file gets nothing back."""
    if mon["moves"] or hack in ("oxide", "unbound", "run_and_bun", "hardlove"):
        return mon["moves"]
    from ..encounters import calc_trainers
    info = data.raw(hack)["poks"].get(mon["species"], {}).get("learnset_info") or {}
    learnset = sorted(info.get("learnset") or [], key=lambda e: e[0])
    return calc_trainers.default_moves(learnset, mon["level"])


def mon_metrics(hack, mon, unresolved):
    bs, types, source = mon_stats(hack, mon)
    if bs is None:
        unresolved["species"].add(mon["species"])
    mon = dict(mon, moves=default_moves(hack, mon))
    phys = spec = 0
    hits, groups = set(), {k: 0 for k in ("setup", "hazards", "priority", "speed_control", "recovery")}
    se = se_table(hack)
    for name in mon["moves"]:
        rec, _src = lookup_move(hack, name)
        if rec is None and not name.startswith("Hidden Power"):
            unresolved["moves"].add(name)
        hit = damaging(rec, name) or name.startswith("Hidden Power")
        if hit and rec:
            phys += rec["category"] == "Physical"
            spec += rec["category"] == "Special"
        if hit and name not in FIXED_DAMAGE:
            hits |= se.get(move_type(hack, mon, name, rec) or "", set())
        groups["setup"] += name in SETUP
        groups["hazards"] += name in HAZARDS
        groups["priority"] += name in PRIORITY or bool(hit and rec and rec["priority"] > 0)
        groups["speed_control"] += name in SPEED_CONTROL
        groups["recovery"] += name in RECOVERY
    if phys != spec:
        used = "at" if phys > spec else "sa"
    else:
        used = "at" if bs and bs["at"] >= bs["sa"] else "sa"
    ivs = mon.get("ivs")
    return {
        "level": mon["level"],
        "iv": statistics.mean(ivs[k] for k in STATS) if ivs else None,
        "ev": sum((mon.get("evs") or {}).values()),
        "nature_fit": nature_fits(mon.get("nature"), used, bs["sp"] if bs else None),
        "item": mon.get("item"),
        "evolved": is_evolved(hack, mon),
        "bst": sum(bs.values()) if bs else None,
        "stats_from": source,
        "hits": hits,
        **groups,
    }


def party_metrics(hack, party, trainers, unresolved):
    """The metrics of one party as the player meets it."""
    mons = [mon_metrics(hack, m, unresolved) for m in party]
    mean = lambda xs: statistics.mean(xs) if xs else None
    ivs = [m["iv"] for m in mons if m["iv"] is not None]
    bsts = [m["bst"] for m in mons if m["bst"] is not None]
    hits = set().union(*(m["hits"] for m in mons)) if mons else set()
    ai = trainers[0].get("ai")
    platinum = hack in PLATINUM
    return {
        "party_size": len(mons),
        "ace_level": max(m["level"] for m in mons),
        "mean_level": mean([m["level"] for m in mons]),
        "mean_iv": mean(ivs),
        "mean_ev": mean([m["ev"] for m in mons]),
        "nature_fit": mean([float(m["nature_fit"]) for m in mons]),
        "item_share": mean([float(bool(m["item"])) for m in mons]),
        "items": sorted({m["item"] for m in mons if m["item"]}),
        "evolved_share": mean([float(m["evolved"]) for m in mons]),
        "mean_bst": mean(bsts),
        "megas": sum(1 for m in party if m.get("mega") or "-Mega" in m["species"]),
        "ai_flags": bin(ai).count("1") if platinum and isinstance(ai, int) else None,
        "doubles": any(t.get("battle_type") == "Doubles" for t in trainers) or len(trainers) > 1,
        **{k: sum(m[k] for m in mons)
           for k in ("setup", "hazards", "priority", "speed_control", "recovery")},
        "coverage": len(hits),
    }


def _average(rows):
    """The mean of several variants' metrics (a rival's three starters)."""
    out = {}
    for k in rows[0]:
        vals = [r[k] for r in rows]
        if all(isinstance(v, (int, float)) and not isinstance(v, bool) for v in vals):
            out[k] = statistics.mean(vals)
        elif all(isinstance(v, bool) for v in vals):
            out[k] = any(vals)
        elif all(isinstance(v, list) for v in vals):
            out[k] = sorted(set().union(*vals))
        else:
            out[k] = next((v for v in vals if v is not None), None)
    return out


def fight_metrics(hack, fight, unresolved=None):
    """A story fight's metrics in one hack, or None if the hack has no
    counterpart for it."""
    unresolved = unresolved if unresolved is not None else {"species": set(), "moves": set()}
    trainers = data.fight_trainers(hack, fight)
    if not trainers:
        return None
    if fight.get("tag") or (len(trainers) > 1 and not fight["key"].startswith("barry")):
        # Tag battles, and Tate and Liza in the milestone hacks: one party.
        party = [m for t in trainers for m in t["party"]]
        out = party_metrics(hack, party, trainers, unresolved)
        out["doubles"] = True
    else:
        out = _average([party_metrics(hack, t["party"], [t], unresolved) for t in trainers])
    if hack == "oxide":
        from . import splits
        out["weather"] = sorted({w for t in fight["tr_ids"] for w in splits.trainer_weather(t)})
    return out


CLOSING = {"Roark": "roark", "Gardenia": "gardenia", "Fantina": "fantina",
           "Maylene": "maylene", "Wake": "wake", "Byron": "byron", "Candice": "candice",
           "HQ": "cyrus_2", "Galactic": "cyrus_3", "Volkner": "volkner", "League": "cynthia"}


@functools.lru_cache(maxsize=None)
def all_metrics():
    """{hack: {fight key: metrics}} for every hack and story fight, with the
    level relative to the split's cap and to the previous boss added. A
    split's cap is its closing boss's ace in the same hack."""
    out, unresolved = {}, {}
    for hack in ["oxide"] + list(data.REFS):
        miss = {"species": set(), "moves": set()}
        rows = {}
        for fight in data.fights()["fights"]:
            m = fight_metrics(hack, fight, miss)
            if m is not None:
                rows[fight["key"]] = m
        prev = None
        for fight in data.fights()["fights"]:
            m = rows.get(fight["key"])
            if m is None:
                continue
            cap = rows.get(CLOSING[fight["split"]], {}).get("ace_level")
            m["over_cap"] = m["ace_level"] - cap if cap is not None else None
            m["over_previous"] = m["ace_level"] - prev if prev is not None else None
            prev = m["ace_level"]
        out[hack] = rows
        unresolved[hack] = miss
    return out, unresolved


# ---- the B2 check -----------------------------------------------------------

def order_table(hacks=("vanilla", "renegade", "kaizo")):
    """For each ordered metric: each hack's mean over the story fights, and
    the share of fights in which the hacks come out in the given order (ties
    allowed). Only fights every hack in the list has are counted."""
    rows, _ = all_metrics()
    keys = [f["key"] for f in data.fights()["fights"] if all(f["key"] in rows[h] for h in hacks)]
    table = []
    for metric in ORDERED:
        vals = {h: [rows[h][k][metric] for k in keys] for h in hacks}
        if any(v is None for vs in vals.values() for v in vs):
            table.append((metric, None, None))
            continue
        means = {h: statistics.mean(vs) for h, vs in vals.items()}
        agree = sum(1 for i in range(len(keys))
                    if all(vals[a][i] <= vals[b][i] for a, b in zip(hacks, hacks[1:])))
        table.append((metric, means, agree / len(keys)))
    return keys, table


def in_order(means, hacks=("vanilla", "renegade", "kaizo")):
    """Means in order, each at or above the one before and the last above the first."""
    vals = [means[h] for h in hacks]
    return all(a <= b for a, b in zip(vals, vals[1:])) and vals[0] < vals[-1]


# ---- filler trainers per split ----------------------------------------------

# The hacks whose filler can be compared by id. Kaizo reuses most of its
# filler ids for other trainers, so its filler would need its own map.
FILLER_HACKS = ["oxide", "vanilla", "renegade", "redux", "redux_hc"]
PARTNER_STEMS = ("cheryl", "mira", "riley", "marley", "buck", "lucas", "dawn")


@functools.lru_cache(maxsize=None)
def _placed_filler():
    """{split: [tr_id]} for every first-run Oxide trainer that is not a story
    fight, a tag partner or a gym leader's rematch, by B1d's split map. The
    post-game split is not scored."""
    from . import splits
    story = {i for f in data.fights()["fights"] for i in f["tr_ids"]}
    out = {s: [] for s in data.fights()["splits"]}
    for tr_id, t in data.oxide_trainers().items():
        if tr_id in story or t["stem"].startswith(PARTNER_STEMS) or "rematch" in t["stem"]:
            continue
        split = splits.trainer_split(tr_id)
        if split in out:
            out[split].append(tr_id)
    return out


@functools.lru_cache(maxsize=None)
def late_visits():
    """[(split, tr_id)] for filler whose Oxide ace is above its split's cap.

    B1d gives a trainer the split of its map, and a map takes the split in
    which the player first reaches it. Part of a map can open later (Surf on
    Route 219, the bike on Route 207, Strength in Oreburgh Gate's basement),
    and a story revisit can add trainers (the grunts at Lake Verity). A
    trainer above the cap cannot belong to its split under hard caps, so
    these are left out of the filler numbers until B1e places them by what
    the player can reach. The cap is Ian's (fights.json), which since the
    Galactic split of 2026-09-25 can sit above the closing boss's ace."""
    caps = data.fights()["caps"]
    ox = data.oxide_trainers()
    out = []
    for split, ids in _placed_filler().items():
        cap = caps[split]
        out += [(split, i) for i in ids if max(m["level"] for m in ox[i]["party"]) > cap]
    return out


def filler_ids():
    """{split: [tr_id]} of the filler that is scored: placed, and not a late
    visit. The Platinum-based hacks keep Platinum's ids, so the same ids
    pick out their filler, subject to the name check in filler_summary."""
    late = {i for _s, i in late_visits()}
    return {s: [i for i in ids if i not in late] for s, ids in _placed_filler().items()}


def _base_name(name):
    """'Galactic Grunt44' -> 'Galactic Grunt': the calculator numbers repeats."""
    return (name or "").rstrip("0123456789").strip()


def filler_summary(hack):
    """({split: summary}, dropped) for a Platinum-based hack's filler. A
    reference's trainer is kept only when it has vanilla's name for the same
    id, since Redux and Kaizo reuse some ids for other trainers (Kaizo's 104
    is a level 100 Gambler where Platinum has a Swimmer). The worst fight is
    the highest ace against the split's cap, then the largest party, then
    the highest mean base stat total."""
    rows, _ = all_metrics()
    pool = data.oxide_trainers() if hack == "oxide" else data.ref_trainers(hack)
    vanilla = data.ref_trainers("vanilla")
    miss = {"species": set(), "moves": set()}
    out, dropped = {}, 0
    for split, ids in filler_ids().items():
        cap = rows[hack].get(CLOSING[split], {}).get("ace_level")
        ms = []
        for tr_id in ids:
            t = pool.get(tr_id)
            if not t or not t["party"]:
                continue
            if hack != "oxide" and _base_name(t["name"]) != _base_name(vanilla[tr_id]["name"]):
                dropped += 1
                continue
            m = party_metrics(hack, t["party"], [t], miss)
            m["name"], m["tr_id"] = t["name"], tr_id
            m["over_cap"] = m["ace_level"] - cap
            ms.append(m)
        mean = lambda k: statistics.mean(m[k] for m in ms if m[k] is not None)
        worst = max(ms, key=lambda m: (m["over_cap"], m["party_size"], m["mean_bst"] or 0))
        out[split] = {"trainers": len(ms), "doubles": sum(m["doubles"] for m in ms),
                      "pokemon": sum(m["party_size"] for m in ms),
                      **{k: mean(k) for k in ("party_size", "over_cap", "mean_iv", "nature_fit",
                                              "item_share", "evolved_share", "mean_bst")},
                      "worst": worst}
    return out, dropped


# ---- reports ----------------------------------------------------------------

def _fmt(v, width=6):
    if v is None:
        return f"{'-':>{width}}"
    if isinstance(v, bool):
        return f"{'yes' if v else 'no':>{width}}"
    if isinstance(v, float):
        return f"{v:>{width}.2f}" if abs(v) < 10 else f"{v:>{width}.1f}"
    return f"{v!s:>{width}}"


COLUMNS = [("party_size", "party"), ("ace_level", "ace"), ("over_cap", "vs cap"),
           ("over_previous", "vs prev"), ("mean_iv", "IV"), ("nature_fit", "nature"),
           ("item_share", "items"), ("evolved_share", "evolved"), ("mean_bst", "BST"),
           ("ai_flags", "AI"), ("setup", "setup"), ("hazards", "hazard"),
           ("priority", "prio"), ("speed_control", "speed"), ("recovery", "recov"),
           ("coverage", "cover"), ("doubles", "double")]


def report_all(out=sys.stdout):
    rows, unresolved = all_metrics()
    head = f"{'hack':12}" + "".join(f"{label:>8}" for _k, label in COLUMNS)
    for fight in data.fights()["fights"]:
        print(f"\n{fight['label']} ({fight['split']} split)", file=out)
        print(head, file=out)
        for hack in ["oxide"] + list(data.REFS):
            m = rows[hack].get(fight["key"])
            if m:
                print(f"{hack:12}" + "".join(_fmt(m[k], 8) for k, _l in COLUMNS), file=out)
    print("\nNot found in any table (left out of the numbers):", file=out)
    for hack, miss in unresolved.items():
        if miss["species"] or miss["moves"]:
            print(f"  {hack}: species {sorted(miss['species'])}, moves {sorted(miss['moves'])}",
                  file=out)


def report_fight(key, out=sys.stdout):
    fight = next(f for f in data.fights()["fights"] if f["key"] == key)
    rows, _ = all_metrics()
    for hack in ["oxide"] + list(data.REFS):
        m = rows[hack].get(key)
        if m:
            extra = f", weather {m['weather']}" if m.get("weather") else ""
            print(f"{hack:12} items {', '.join(m['items']) or 'none'}{extra}", file=out)


def report_order(out=sys.stdout):
    keys, table = order_table()
    print(f"{len(keys)} story fights; means, and the share of fights in order", file=out)
    print(f"{'metric':15}{'vanilla':>9}{'renegade':>9}{'kaizo':>9}{'oxide':>9}{'in order':>10}"
          f"{'fights':>8}", file=out)
    rows, _ = all_metrics()
    for metric, means, share in table:
        if means is None:
            print(f"{metric:15} (missing in some fight)", file=out)
            continue
        ox = statistics.mean(rows["oxide"][k][metric] for k in keys)
        print(f"{metric:15}" + "".join(_fmt(means[h], 9) for h in ("vanilla", "renegade", "kaizo"))
              + _fmt(ox, 9) + f"{'yes' if in_order(means) else 'NO':>10}{share:>8.0%}", file=out)


def report_filler(out=sys.stdout):
    ox = data.oxide_trainers()
    late = late_visits()
    print(f"Left out as later visits ({len(late)}): "
          + ", ".join(f"{ox[i]['stem']} ({s})" for s, i in late), file=out)
    print("Kaizo is left out: 252 of its filler ids hold another trainer than "
          "Platinum's, and some that keep the name are level 90 to 100.", file=out)
    for hack in FILLER_HACKS:
        summary, dropped = filler_summary(hack)
        print(f"\n{hack}" + (f", {dropped} ids holding another trainer left out" if dropped else ""),
              file=out)
        print(f"{'split':10}{'trainers':>9}{'party':>7}{'vs cap':>7}{'IV':>7}{'nature':>7}"
              f"{'items':>7}{'evolved':>8}{'BST':>7}  worst", file=out)
        for split, s in summary.items():
            w = s["worst"]
            print(f"{split:10}{s['trainers']:>9}" + "".join(
                _fmt(s[k], 7) for k in ("party_size", "over_cap", "mean_iv", "nature_fit",
                                        "item_share"))
                + _fmt(s["evolved_share"], 8) + _fmt(s["mean_bst"], 7)
                + f"  {w['name']} ({w['tr_id']}), {w['party_size']} at {w['ace_level']}", file=out)


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if not argv:
        report_all()
    elif argv[0] == "--order":
        report_order()
    elif argv[0] == "--filler":
        report_filler()
    else:
        report_fight(argv[0])
    return 0


if __name__ == "__main__":
    sys.exit(main())

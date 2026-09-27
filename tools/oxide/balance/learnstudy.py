"""The learnset study, part 1: when Platinum Kaizo gives each move, against
the move's real strength as Kaizo has it (docs/oxide/balance-plan.md, "The
learnset study").

    PYTHONPATH=. python3 -m tools.oxide.balance.learnstudy               # the report
    PYTHONPATH=. python3 -m tools.oxide.balance.learnstudy --line GIBLE  # one line's lists

It reads Kaizo's level-up lists as Ian gave them (docs/oxide/kaizo-learnsets.tsv),
Kaizo's moves as its own change list states them (docs/oxide/kaizo-move-changes.md)
and otherwise as its calculator file has them, and vanilla Platinum's lists and
evolutions from main. It writes nothing.

A move's strength is its expected damage per turn spent, in base power:
power, times the chance it lands, times the hits it averages, divided by the
turns it takes, less a share for recoil or fainting. Status moves have no
strength and are tallied apart, as are moves whose damage is fixed (Dragon
Rage, Seismic Toss) or returned (Counter, Bide).

A line is read along the path a player walks: each stage's moves from the
level it is reached, since an evolved stage's earlier moves need the Move
Relearner. A stage reached by stone, trade or friendship is taken as reached
at the encounter tool's stand-in level for that method.
"""
import argparse
import collections
import functools
import json
import os
import re
import statistics
import sys

from ..encounters import evolve, pokedex
from . import data, metrics

HERE = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.join(data.ROOT, "docs", "oxide")
LEARNSETS = os.path.join(DOCS, "kaizo-learnsets.tsv")
CHANGES = os.path.join(DOCS, "kaizo-move-changes.md")

# Each game's gym splits, closed by the leader's ace as its stored seats have
# it, and the League after them. Kaizo's Galactic fights sit above Volkner's
# level, so the splits follow the gyms.
GYMS = ["roark", "gardenia", "fantina", "maylene", "wake", "byron", "candice", "volkner"]
LEAGUE = ["aaron", "bertha", "flint", "lucian", "cynthia"]
SPLIT_NAMES = [g.title() for g in GYMS] + ["League"]

# Strength bands, in base power per turn.
WEAK, FAIR, STRONG, BIG = 50, 70, 85, 100

SETUP = {"Swords Dance", "Dragon Dance", "Nasty Plot", "Calm Mind", "Bulk Up", "Quiver Dance",
         "Shell Smash", "Agility", "Rock Polish", "Curse", "Growth", "Work Up", "Hone Claws",
         "Coil", "Shift Gear", "Cotton Guard", "Iron Defense", "Amnesia", "Tail Glow",
         "Belly Drum", "Cosmic Power", "Acid Armor", "Barrier", "Howl", "Meditate", "Sharpen",
         "Harden", "Withdraw", "Defense Curl", "Minimize", "Double Team", "Focus Energy"}
REACTIVE = {"Counter", "Mirror Coat", "Bide", "Metal Burst", "Comeuppance"}
# Fixed damage whatever the listed power; Sheer Cold and Psywave only when a
# game leaves them powerless (Kaizo gives Sheer Cold 70).
FIXED = {"Dragon Rage", "Sonic Boom", "Seismic Toss", "Night Shade", "Super Fang", "Endeavor",
         "Final Gambit", "Guillotine", "Horn Drill", "Fissure"}
FIXED_IF_POWERLESS = {"Sheer Cold", "Psywave"}
# Moves whose damage needs a condition the user rarely has: the share of
# their power they are counted at.
CONDITIONAL = {"Snore": 0.0, "Dream Eater": 0.3, "Focus Punch": 0.5, "Last Resort": 0.3,
               "Belch": 0.3, "Spit Up": 0.0, "Natural Gift": 0.5, "Fling": 0.5,
               "Trump Card": 0.5, "Present": 0.5}

# Effects that change a move's strength, by the decomp's names (Kaizo's
# calculator keeps Generation 4's numbering; Oxide's later effects are here
# too, for reading Oxide's own moves). Earthquake's effect, double damage on a
# digging target, is a plain hit: names are matched whole, never by a part.
# A charging turn out in the open, or a recharge, costs a turn. Fly, Dig, Dive,
# Bounce and Shadow Force spend theirs out of reach, trading it for an attack
# dodged, so they count as one turn.
OPEN_CHARGE = {"CHARGE_TURN_HIGH_CRIT", "CHARGE_TURN_HIGH_CRIT_FLINCH", "CHARGE_TURN_DEF_UP"}
TWO_TURNS = OPEN_CHARGE | {"SKIP_CHARGE_TURN_IN_SUN", "RECHARGE_AFTER"}
TWICE = {"HIT_TWICE", "POISON_MULTI_HIT"}
RISING_THREE = {"HIT_THREE_TIMES", "HIT_THREE_TIMES_INCREMENT_BASE_POWER_20"}
FLAT_THREE = {"HIT_THREE_TIMES_FIXED_POWER", "HIT_THREE_TIMES_ALWAYS_CRITICAL"}
RECOIL_THIRD = {"RECOIL_THIRD", "RECOIL_BURN_HIT", "RECOIL_PARALYZE_HIT"}

# Generation 4 spellings in Ian's lists and Kaizo's change list, against the
# modern ones its calculator file uses. Solar Beam and Kaizo's Solar-Beam (Skull
# Bash's slot) differ only by a hyphen, so names are never matched loosely
# where that would join two moves.
SPELLING = {"BubbleBeam": "Bubble Beam", "Faint Attack": "Feint Attack",
            "ThunderShock": "Thunder Shock", "Selfdestruct": "Self-Destruct",
            "SolarBeam": "Solar Beam", "ViceGrip": "Vise Grip", "Hi Jump Kick": "High Jump Kick",
            "SmellingSalt": "Smelling Salts", "SonicBoom": "Sonic Boom"}


def resolve(name, table):
    """The key `table` uses for a move named in Gen 4 or modern spelling, or None."""
    if not name:
        return None
    if name in table:
        return name
    if SPELLING.get(name) in table:
        return SPELLING[name]
    loose = [k for k in table if metrics._compact(k) == metrics._compact(name)]
    return loose[0] if len(loose) == 1 else None


# ---- the games' splits -----------------------------------------------------------

@functools.lru_cache(maxsize=None)
def splits(hack):
    """[(split, closing level)] for a reference hack, from its stored seats."""
    with open(os.path.join(HERE, "pressure_refs", f"{hack}.json"), encoding="utf-8") as f:
        seats = json.load(f)["fights"]
    out = [(g.title(), seats[g]["ace"]) for g in GYMS]
    out.append(("League", max(seats[k]["ace"] for k in LEAGUE if k in seats)))
    return out


def split_of(hack, level):
    for name, cap in splits(hack):
        if level <= cap:
            return name
    return "League"


def split_index(hack, level):
    return SPLIT_NAMES.index(split_of(hack, level))


# ---- Kaizo's moves ---------------------------------------------------------

def _split_note(text):
    """'Name (note (nested)): changes' -> (name, note, changes). The notes
    carry nested brackets ('Lowers SpAtk (Attack)'), so they are matched by
    depth rather than by pattern."""
    name_end = text.find(" (")
    colon = text.find(": ")
    if name_end < 0 or (0 <= colon < name_end):
        name, _, rest = text.partition(": ")
        return name.strip(), "", rest.strip()
    depth, i = 0, name_end + 1
    for i in range(name_end + 1, len(text)):
        depth += {"(": 1, ")": -1}.get(text[i], 0)
        if depth == 0:
            break
    note = text[name_end + 2:i]
    rest = text[i + 1:].lstrip(": ").strip()
    return text[:name_end].strip(), note, rest


@functools.lru_cache(maxsize=None)
def changes():
    """{Kaizo's name for the move: {"was", "note", "power", "accuracy", "type",
    "category", "priority", "chance"}} from Kaizo's change list, which the
    plan reads first. A renamed move ('Comet Punch -> Water Ball') is keyed by
    its new name, with the slot it took as "was"."""
    with open(CHANGES, encoding="utf-8") as f:
        text = f.read()
    block = text.split("```")[1]
    out = {}
    for line in block.strip().splitlines():
        head, note, rest = _split_note(line.strip())
        old, arrow, new = head.partition(" -> ")
        name = (new if arrow else old).strip()
        rec = {"was": old.strip() if arrow else None, "note": note}
        parts = [p.strip() for p in note.split(",")]
        if parts and parts[-1] in ("Physical", "Special", "Status"):
            rec["category"] = parts[-1]
        for item in (p.strip() for p in rest.split(",") if p.strip()):
            m = re.match(r"(\S+) (bp|acc|pp) -> (\S+) \2$", item)
            if m:
                key = {"bp": "power", "acc": "accuracy", "pp": "pp"}[m.group(2)]
                rec[key] = int(m.group(3))
                continue
            m = re.match(r"(\S+) type -> (\S+) type$", item)
            if m:
                rec["type"] = m.group(2)
                continue
            m = re.match(r"([+-]?\d+) priority$", item)
            if m:
                rec["priority"] = int(m.group(1))
                continue
            m = re.match(r"(\d+)% chance -> (\d+)% chance$", item)
            if m:
                rec["chance"] = int(m.group(2))
        out[name] = rec
    return out


@functools.lru_cache(maxsize=None)
def effect_names():
    """Generation 4's effect numbers, which Kaizo's calculator file keeps."""
    with open(os.path.join(data.ROOT, "generated", "move_battle_effects.txt"),
              encoding="utf-8") as f:
        return [l.strip().replace("BATTLE_EFFECT_", "") for l in f if l.strip()]


def _priority(calc, vanilla):
    """The calculator's priority where it is a real one (a reused slot can
    carry 255), else vanilla's, whose records may leave it out."""
    p = calc.get("priority")
    if isinstance(p, int) and -7 <= p <= 7:
        return p
    return vanilla.get("priority") or 0


@functools.lru_cache(maxsize=None)
def kaizo_moves():
    """{name: move} as Kaizo plays it, keyed by its calculator's spelling. The
    calculator file gives every move; where the change list states a value,
    the change list wins, and a move it touched keeps vanilla's priority
    unless it names one (the calculator's record for a reused slot can carry
    a placeholder: Constrict reads as a 255-power Psychic move at priority 255)."""
    calc = data.raw("kaizo")["moves"]
    vanilla = data.raw("vanilla")["moves"]
    names = effect_names()
    listed = {resolve(name, calc) or name: rec for name, rec in changes().items()}
    out, disagree = {}, []
    for name in set(calc) | set(listed):
        c = calc.get(name, {})
        ch = listed.get(name, {})
        was = ch.get("was")
        # Vanilla's record for the slot: the old move where Kaizo reused one.
        v = vanilla.get(resolve(was or name, vanilla) or "", {})
        e_id = c.get("e_id")
        out[name] = {
            "name": name,
            "type": ch.get("type") or c.get("type") or v.get("type"),
            "power": ch.get("power", c.get("basePower", v.get("basePower", 0))) or 0,
            "category": ch.get("category") or c.get("category") or v.get("category"),
            "accuracy": ch.get("accuracy", c.get("accuracy", v.get("accuracy", 100))),
            "priority": ch.get("priority", _priority(c, v)),
            "effect": names[e_id] if isinstance(e_id, int) and 0 <= e_id < len(names) else "",
            "note": ch.get("note", ""),
            "was": was,
        }
        if ch and c and (("power" in ch and ch["power"] != c.get("basePower"))
                         or ("type" in ch and ch["type"] != c.get("type"))):
            disagree.append(name)
    kaizo_moves.disagree = sorted(disagree)
    return out


def strength(move):
    """(kind, base power per turn) for a move given as {name, power, accuracy,
    category, effect, note}, by the rules in the module's doc. kind is
    "damage", "status", "fixed", "reactive" or "conditional"."""
    name, note, effect = move["name"], (move.get("note") or "").lower(), move.get("effect") or ""
    power = move["power"] or 0
    if name in REACTIVE:
        return "reactive", 0.0
    if name in FIXED or (name in FIXED_IF_POWERLESS and power <= 1):
        return "fixed", 0.0
    if move["category"] == "Status" or power <= 1:
        return "status", 0.0
    acc = move["accuracy"]
    hit = 1.0 if not acc or "always hits" in note else min(acc, 100) / 100
    if "up to 3 times" in note or effect in RISING_THREE:
        # Three hits, each ten stronger than the last and each able to miss.
        step = 20 if effect.endswith("POWER_20") else 10
        total = sum((power + step * i) * hit ** (i + 1) for i in range(3))
    elif effect in FLAT_THREE:
        total = power * hit * 3.0
    elif "2-5 times" in note or effect == "MULTI_HIT":
        total = power * hit * 3.0    # Generation 4's two to five hits average three
    elif "twice" in note or effect in TWICE:
        total = power * hit * 2.0
    else:
        total = power * hit
    # Kaizo's notes say where it made a charging or recharging move a plain
    # hit ("No Effect") or traded the recharge for recoil.
    plain = "no effect" in note or "recoil" in note
    turns = 2.0 if effect in TWO_TURNS and not plain else 1.0
    keep = 1.0
    if "1/2" in note or effect == "RECOIL_HALF":
        keep = 0.8
    elif "1/3" in note or effect in RECOIL_THIRD:
        keep = 0.85
    elif "1/4" in note or effect in ("RECOIL_QUARTER", "CRASH_ON_MISS"):
        keep = 0.9
    if effect in ("EXPLOSION", "HALVE_DEFENSE") or "explosion effect" in note:
        keep = 0.5          # Self-Destruct and Explosion: one use, then the user faints
    base = total / turns * keep
    if name in CONDITIONAL:
        return "conditional", base * CONDITIONAL[name]
    return "damage", base


def band(power):
    if power >= BIG:
        return "big"
    if power >= STRONG:
        return "strong"
    if power >= FAIR:
        return "fair"
    if power >= WEAK:
        return "weak"
    return "feeble"


# ---- Kaizo's lists and the lines ----------------------------------------------

@functools.lru_cache(maxsize=None)
def species_constants():
    """National number -> SPECIES_ constant, from the positional species list."""
    with open(os.path.join(data.ROOT, "generated", "species.txt"), encoding="utf-8") as f:
        names = [l.strip() for l in f if l.strip()]
    return {i: n for i, n in enumerate(names) if n.startswith("SPECIES_")}


@functools.lru_cache(maxsize=None)
def kaizo_lists():
    """{SPECIES_X: {"name", "types", "list": [(level, move)]}} for Kaizo's 493
    species, in Kaizo's order. Types are Kaizo's own, from its calculator,
    looked up by national number since the two spell some names apart."""
    by_num = {v.get("num"): v for v in data.raw("kaizo")["poks"].values()}
    consts = species_constants()
    out = {}
    with open(LEARNSETS, encoding="utf-8") as f:
        next(f)
        for row in f:
            cells = row.rstrip("\n").split("\t")
            if len(cells) < 2 or not cells[0].isdigit():
                continue
            num = int(cells[0])
            if not 1 <= num <= 493:
                continue
            moves = []
            for cell in cells[2:]:
                move, _, level = cell.rpartition("@")
                if move and level.isdigit():
                    moves.append((int(level), move))
            rec = by_num.get(num) or {}
            out[consts[num]] = {"name": cells[1].title(), "types": rec.get("types") or [],
                                "calc": rec.get("learnset_info", {}).get("learnset") or [],
                                "list": moves}
    return out


@functools.lru_cache(maxsize=None)
def vanilla_dex(species):
    return pokedex.load(data.ROOT, species, ref="main")


@functools.lru_cache(maxsize=None)
def _reached():
    """{species: (parent, level it is reached at)} by vanilla's evolutions, a
    stone, trade or friendship taken at the encounter tool's stand-in level."""
    out = {}
    for sp in kaizo_lists():
        for evo in (vanilla_dex(sp) or {}).get("evolutions", []):
            into = evo["into"]
            if into not in kaizo_lists() or evo["form"] or into in out:
                continue
            level = evo["level"] or evolve.PSEUDO.get("EVO_" + evo["method"],
                                                       evolve.DEFAULT_PSEUDO)
            out[into] = (sp, level)
    return out


def reached_at(species):
    return _reached().get(species, (None, 1))[1]


@functools.lru_cache(maxsize=None)
def lines():
    """[[base, stage 2, ...]] for every Generation 4 family, each branch its
    own line (Eevee's seven, Tyrogue's three)."""
    kids = collections.defaultdict(list)
    for into, (parent, _lv) in _reached().items():
        kids[parent].append(into)
    out = []

    def walk(path):
        if not kids.get(path[-1]):
            out.append(path)
        for into in kids.get(path[-1], []):
            walk(path + [into])
    for sp in kaizo_lists():
        if sp not in _reached():
            walk([sp])
    return out


def read(species, level, name, types, hack="kaizo"):
    """One list entry, read: its split, the move's kind, strength and band,
    and whether it is same-type."""
    moves = kaizo_moves()
    mv = moves.get(resolve(name, moves) or "")
    if mv is None:
        return {"species": species, "level": level, "move": name, "kind": "unknown"}
    kind, power = strength(mv)
    return {"species": species, "level": level, "split": split_of(hack, level), "move": name,
            "kind": kind, "power": round(power, 1),
            "band": band(power) if kind == "damage" else None,
            "type": mv["type"], "stab": mv["type"] in types, "setup": name in SETUP,
            "priority": mv["priority"]}


def entries(species):
    rec = kaizo_lists()[species]
    return [read(species, lv, name, rec["types"]) for lv, name in rec["list"]]


def path(line):
    """A line's moves as a player walking it meets them: each stage's from the
    level it is reached until the next stage is."""
    out = []
    for i, sp in enumerate(line):
        start = reached_at(sp) if i else 0
        stop = reached_at(line[i + 1]) if i + 1 < len(line) else 999
        out += [e for e in entries(sp) if start <= e["level"] < stop]
    return sorted(out, key=lambda e: e["level"])


# ---- the readings ------------------------------------------------------------

def curve():
    """Per Kaizo split: moves met along each line's path past level 1, their
    median strength, same-type and coverage apart, and the share that are
    status. A move shared by two lines of one family counts once."""
    rows = collections.defaultdict(lambda: {"stab": [], "cover": [], "status": 0, "all": 0})
    seen = set()
    for line in lines():
        for e in path(line):
            key = (e["species"], e["level"], e["move"])
            if e["kind"] == "unknown" or e["level"] <= 1 or key in seen:
                continue
            seen.add(key)
            r = rows[e["split"]]
            r["all"] += 1
            if e["kind"] == "damage":
                r["stab" if e["stab"] else "cover"].append(e["power"])
            elif e["kind"] == "status":
                r["status"] += 1
    return rows


def milestones(line):
    """Along a line's path: the level of the first same-type move of each band
    and of the first coverage move of fair strength or better."""
    got = {}
    for e in path(line):
        if e["kind"] != "damage":
            continue
        for name, floor in (("stab_fair", FAIR), ("stab_strong", STRONG), ("stab_big", BIG)):
            if e["stab"] and e["power"] >= floor and name not in got:
                got[name] = e["level"]
        if not e["stab"] and e["power"] >= FAIR and "cover_fair" not in got:
            got["cover_fair"] = e["level"]
    return got


def stage_shifts():
    """Moves a stage shares with the one before it: (earlier, later, move,
    level in each)."""
    out = []
    for line in lines():
        for a, b in zip(line, line[1:]):
            la = {m: l for l, m in kaizo_lists()[a]["list"] if l > 1}
            lb = {m: l for l, m in kaizo_lists()[b]["list"] if l > 1}
            out += [(a, b, m, la[m], lb[m]) for m in sorted(la.keys() & lb.keys())]
    return out


@functools.lru_cache(maxsize=None)
def _vanilla_names():
    return {rec["move"]: rec["name"] for rec in pokedex.vanilla_moves(data.ROOT).values()}


def against_vanilla():
    """Per species and move in both games' lists (a reused slot compared by the
    slot it took): (species, move, vanilla level, Kaizo level)."""
    slot = {name: rec["was"] for name, rec in changes().items() if rec["was"]}
    names = _vanilla_names()
    out = []
    for sp, rec in kaizo_lists().items():
        vlev = {}
        for lv, mv in (vanilla_dex(sp) or {}).get("learnset", []):
            vlev.setdefault(metrics._compact(names.get(mv, mv)), lv)
        for level, name in rec["list"]:
            key = metrics._compact(SPELLING.get(slot.get(name, name), slot.get(name, name)))
            alt = metrics._compact(slot.get(name, name))
            vl = vlev.get(key, vlev.get(alt))
            if vl is not None:
                out.append((sp, name, vl, level))
    return out


# ---- part 2: the rules tested ------------------------------------------------------

def family_of(line):
    return line[0]


def _fold(family, k):
    """A fixed fold for a family, so every run holds out the same lines."""
    return sum(ord(ch) for ch in family) % k


def _medians(train_lines):
    """What a training set says: each move's median split along the paths,
    and the curve's median strength per split, same-type and coverage apart."""
    per_move = collections.defaultdict(list)
    curve_rows = collections.defaultdict(lambda: {"stab": [], "cover": []})
    for line in train_lines:
        for e in path(line):
            if e["kind"] == "unknown" or e["level"] <= 1:
                continue
            per_move[e["move"]].append(SPLIT_NAMES.index(e["split"]))
            if e["kind"] == "damage":
                curve_rows[e["split"]]["stab" if e["stab"] else "cover"].append(e["power"])
    move_split = {m: statistics.median(v) for m, v in per_move.items()}
    med = {s: {k: statistics.median(v) if v else None for k, v in r.items()}
           for s, r in curve_rows.items()}
    everything = [i for v in per_move.values() for i in v]
    return move_split, med, statistics.median(everything)


def _by_curve(e, med, fallback):
    """The first split whose median move of the same kind is at least as
    strong as this one."""
    if e["kind"] != "damage":
        return fallback
    key = "stab" if e["stab"] else "cover"
    for i, s in enumerate(SPLIT_NAMES):
        m = med.get(s, {}).get(key)
        if m is not None and m >= e["power"]:
            return i
    return len(SPLIT_NAMES) - 1


def stage_key(line, species):
    """Where a species sits in its line: alone, first, middle or last."""
    if len(line) == 1:
        return "alone"
    i = line.index(species)
    return "first" if i == 0 else "last" if i == len(line) - 1 else "middle"


def _offsets(train, move_split):
    """How far Kaizo places a move from its usual split, by whether it is
    same-type and by the stage that learns it: the median, per group."""
    groups = collections.defaultdict(list)
    for line in train:
        for e in path(line):
            if e["kind"] == "unknown" or e["level"] <= 1 or e["move"] not in move_split:
                continue
            key = (e["kind"] == "damage" and e["stab"], stage_key(line, e["species"]))
            groups[key].append(SPLIT_NAMES.index(e["split"]) - move_split[e["move"]])
    return {k: statistics.median(v) for k, v in groups.items()}


def placement_test(k=5):
    """Each way of placing a move, fitted on four fifths of the families and
    scored on the fifth: the mean number of splits it misses Kaizo's by, and
    the share it places in Kaizo's split or one away."""
    scores = collections.defaultdict(list)
    names = _vanilla_names()
    for fold in range(k):
        train = [ln for ln in lines() if _fold(family_of(ln), k) != fold]
        test = [ln for ln in lines() if _fold(family_of(ln), k) == fold]
        move_split, med, overall = _medians(train)
        offsets = _offsets(train, move_split)
        # Each training move's strength, for placing a move as if unseen.
        power_of = {}
        for line in train:
            for e in path(line):
                if e["kind"] == "damage" and e["move"] in move_split:
                    power_of[e["move"]] = e["power"]
        for line in test:
            for e in path(line):
                if e["kind"] == "unknown" or e["level"] <= 1:
                    continue
                truth = SPLIT_NAMES.index(e["split"])
                curve_guess = _by_curve(e, med, overall)
                usual = move_split.get(e["move"], curve_guess)
                shift = offsets.get((e["kind"] == "damage" and e["stab"],
                                     stage_key(line, e["species"])), 0)
                guesses = {
                    "the strength curve alone": curve_guess,
                    "the move's usual split": move_split.get(e["move"], overall),
                    "the move's usual split, else the curve": usual,
                    "the same, shifted for same-type and stage":
                        min(len(SPLIT_NAMES) - 1, max(0, usual + shift)),
                }
                if e["kind"] == "damage":
                    # As if Kaizo had never used the move: the usual split of
                    # its other moves within ten points of this one's strength.
                    near = [move_split[m] for m, p in power_of.items()
                            if m != e["move"] and abs(p - e["power"]) <= 10]
                    guesses["an unseen move, by moves of like strength"] = (
                        statistics.median(near) if near else curve_guess)
                    guesses["an unseen move, by the curve"] = curve_guess
                    guesses["a known move's usual split, damaging moves only"] = usual
                van = {metrics._compact(names.get(mv, mv)): lv for lv, mv in
                       reversed((vanilla_dex(e["species"]) or {}).get("learnset", []))}
                slot = changes().get(e["move"], {}).get("was") or e["move"]
                vl = van.get(metrics._compact(SPELLING.get(slot, slot)))
                if vl is not None:
                    guesses["vanilla's split, where vanilla has the move"] = \
                        split_index("vanilla", vl)
                for name, g in guesses.items():
                    scores[name].append(abs(g - truth))
    return {name: {"n": len(v), "mean": sum(v) / len(v),
                   "exact": sum(x < 0.5 for x in v) / len(v),
                   "within_one": sum(x <= 1 for x in v) / len(v)}
            for name, v in scores.items()}


# ---- part 2: dead weight --------------------------------------------------------------

# The rule's four tests, each read off Kaizo's lists. A damaging move past its
# level-1 start is dead weight when it is weaker than FLOOR anywhere (Kaizo's
# lists hold Tackle-strength moves and weaker only as starting moves and Wrap);
# when it misses more than one time in ten on under 100 power (Kaizo raised
# nearly all such moves to full accuracy, and its lists keep only Mega Punch);
# or when it is at most HALF of what its split usually gives (Kaizo gives about
# one move in a hundred that weak). Snore, and moves that return damage at
# less than double, are dead weight whatever their power.
FLOOR = 40
RELIABLE = 90
HALF = 0.5
# Moves worth a slot for what they do besides damage.
UTILITY = {"U-turn", "Volt Switch", "Flip Turn", "Parting Shot", "Fake Out", "Pursuit",
           "Rapid Spin", "Knock Off", "Feint", "Thief", "Covet", "Dragon Tail", "Circle Throw",
           "Mortal Spin", "Clear Smog", "Seismic Toss", "Night Shade", "False Swipe"}
# Effect families that are worth a slot when they are certain: a stat drop or
# a status on the target (Mud-Slap, Icy Wind, Nuzzle).
SURE_EFFECTS = {"LOWER_SPEED_HIT", "LOWER_ACCURACY_HIT", "LOWER_ATTACK_HIT",
                "LOWER_SP_ATK_HIT", "LOWER_SP_DEF_HIT", "LOWER_DEFENSE_HIT", "PARALYZE_HIT",
                "BURN_HIT", "POISON_HIT", "CONFUSE_HIT", "FREEZE_HIT"}
# Returning damage below double, or working only in a state the user avoids.
NEVER = {"Bide", "Metal Burst", "Comeuppance", "Snore"}


@functools.lru_cache(maxsize=None)
def medians():
    """{split: {"stab": median, "cover": median}} of Kaizo's curve: what a
    split's ordinary new move is worth."""
    return {s: {k: statistics.median(v) if v else None
                for k, v in (("stab", r["stab"]), ("cover", r["cover"]))}
            for s, r in curve().items()}


def dead_weight(move, split, stab, first=False):
    """Why a level-up move is dead weight where it lands, or None. `move` is
    {name, power, accuracy, category, effect, chance, priority, note}; `first`
    marks a starting move, which the split's median does not judge."""
    name = move["name"]
    if name in NEVER:
        return "works only asleep, or returns less than double"
    kind, power = strength(move)
    if kind != "damage":
        return None
    note = (move.get("note") or "").lower()
    if move.get("effect") in OPEN_CHARGE and not ("no effect" in note or "recoil" in note):
        return "charges a turn in the open (Kaizo's lists keep no such move)"
    if (move.get("priority") or 0) > 0 or name in UTILITY:
        return None
    if move.get("effect") in SURE_EFFECTS and (move.get("chance") or 0) >= 100:
        return None
    if power < FLOOR:
        return f"strength {power:.0f}, under {FLOOR}"
    acc = move.get("accuracy")
    if acc and acc < RELIABLE and (move["power"] or 0) < 100 and "always hits" not in (
            move.get("note") or "").lower():
        return f"{acc}% accurate on {move['power']} power"
    if first:
        return None
    m = medians().get(split, {}).get("stab" if stab else "cover")
    if m and power <= m * HALF:
        return f"strength {power:.0f}, at most half of {split}'s usual {m:.0f}"
    return None


# Oxide's splits read against Kaizo's curve: the Galactic splits sit between
# Candice and Volkner, so they are read at Candice's.
OXIDE_TO_KAIZO = {"HQ": "Candice", "Galactic": "Candice"}


@functools.lru_cache(maxsize=None)
def oxide_splits():
    from . import pool
    return sorted(pool.caps().items(), key=lambda kv: kv[1])


def oxide_split(level):
    for name, cap in oxide_splits():
        if level <= cap:
            return name
    return "Post"


def oxide_move(rec, vanilla=None):
    """An Oxide move record as the study's rules read it."""
    r = vanilla or rec
    return {"name": rec["name"], "power": r.get("power") or 0, "accuracy": r.get("accuracy"),
            "category": (rec.get("class") or "").title(), "effect": rec.get("effect") or "",
            "chance": rec.get("effect_chance"), "priority": rec.get("priority") or 0, "note": ""}


def oxide_dead_weight():
    """Every Oxide level-up entry the rule flags: (species, level, move, split, why)."""
    moves = pokedex.moves(data.ROOT)
    with open(os.path.join(data.ROOT, "generated", "species.txt"), encoding="utf-8") as f:
        species = [l.strip() for l in f if l.strip().startswith("SPECIES_")]
    out = []
    for sp in species:
        try:
            rec = pokedex.load(data.ROOT, sp)
        except OSError:
            rec = None
        if not rec:
            continue
        types = {t.title() for t in rec["types"]}
        for level, mv in rec["learnset"]:
            m = moves.get(mv)
            if not m:
                continue
            split = oxide_split(level)
            if split == "Post":
                split = "League"
            ks = OXIDE_TO_KAIZO.get(split, split)
            why = dead_weight(oxide_move(m), ks, m["type"].title() in types, first=level <= 1)
            if why:
                out.append((sp, level, m["name"], split, why))
    return out


NAMED = ["Absorb", "Wrap", "Constrict", "Barrage", "Snore", "Rage", "Razor Wind", "Bide",
         "Comeuppance", "Octazooka", "Submission"]


def named_check():
    """Ian's named moves at Oxide's values, and Octazooka at vanilla's, each
    read against the curve in every split: the splits where the rule would
    let it stay."""
    moves = {m["name"]: m for m in pokedex.moves(data.ROOT).values()}
    van = {m["name"]: m for m in pokedex.vanilla_moves(data.ROOT).values()}
    out = {}
    for name in NAMED:
        m = moves.get(name)
        if not m:
            out[name] = "not in Oxide's moves"
            continue
        rec = oxide_move(m, van.get(name) if name == "Octazooka" else None)
        kept = ["level 1"] if not dead_weight(rec, "Roark", True, first=True) else []
        kept += sorted({s for s in SPLIT_NAMES for stab in (True, False)
                        if not dead_weight(rec, s, stab)}, key=SPLIT_NAMES.index)
        out[name] = kept
    return out


@functools.lru_cache(maxsize=None)
def _oxide_chances():
    """Each move's effect chance by name, from Oxide's data: Kaizo's calculator
    records carry none, and a sure stat drop is the same move in both."""
    return {metrics._compact(m["name"]): m["effect_chance"]
            for m in pokedex.moves(data.ROOT).values()}


def kaizo_dead_weight():
    """How often Kaizo's own lists give a move the rule calls dead weight,
    along the paths with Kaizo's move values: (entries, flagged at level 1,
    flagged later)."""
    moves = kaizo_moves()
    n, start, later = 0, collections.Counter(), collections.Counter()
    for line in lines():
        for e in path(line):
            if e["kind"] == "unknown":
                continue
            n += 1
            mv = moves[resolve(e["move"], moves)]
            chance = changes().get(e["move"], {}).get("chance")
            if chance is None:
                chance = _oxide_chances().get(metrics._compact(SPELLING.get(e["move"], e["move"])))
            first = e["level"] <= 1
            if dead_weight(dict(mv, chance=chance), e["split"], e["stab"], first=first):
                (start if first else later)[e["move"]] += 1
    return n, start, later


# ---- the report ------------------------------------------------------------------

def _q(values, q):
    values = sorted(values)
    return values[min(len(values) - 1, int(q * len(values)))] if values else None


def report(out=sys.stdout):
    ks = kaizo_lists()
    all_entries = [e for sp in ks for e in entries(sp)]
    unknown = collections.Counter(e["move"] for e in all_entries if e["kind"] == "unknown")
    print(f"Kaizo lists read: {len(ks)} species, {len(lines())} lines, "
          f"{len(all_entries)} entries; species without Kaizo types: "
          f"{[r['name'] for r in ks.values() if not r['types']] or 'none'}", file=out)
    print(f"moves not found in Kaizo's data: {dict(unknown) or 'none'}", file=out)
    print(f"change list and calculator disagree on (the list is used): "
          f"{', '.join(kaizo_moves.disagree) or 'none'}", file=out)
    # Ian's file is the source; the calculator's own lists are a cross-check.
    same = lambda a, b: [(l, metrics._compact(SPELLING.get(m, m))) for l, m in a] == \
        [(l, metrics._compact(m)) for l, m in b]
    differ = [r["name"] for r in ks.values() if not same(r["list"], r["calc"])]
    print(f"Ian's lists and the calculator's differ for {len(differ)} species: "
          f"{', '.join(differ[:10])}{' ...' if len(differ) > 10 else ''}", file=out)
    print("splits: Kaizo " + ", ".join(f"{s} {c}" for s, c in splits("kaizo"))
          + "; vanilla " + ", ".join(f"{s} {c}" for s, c in splits("vanilla")), file=out)

    print("\nThe curve: moves met along each line past level 1, per Kaizo split", file=out)
    print(f"{'split':10}{'moves':>7}{'status':>8}{'STAB n':>8}{'med':>6}{'q25':>6}{'q75':>6}"
          f"{'cover n':>9}{'med':>6}{'q25':>6}{'q75':>6}", file=out)
    rows = curve()
    fmt = lambda v, q: f"{_q(v, q):.0f}" if v else "-"
    for s in SPLIT_NAMES:
        r = rows.get(s)
        if not r:
            continue
        print(f"{s:10}{r['all']:>7}{r['status'] / r['all']:>8.2f}{len(r['stab']):>8}"
              f"{fmt(r['stab'], .5):>6}{fmt(r['stab'], .25):>6}{fmt(r['stab'], .75):>6}"
              f"{len(r['cover']):>9}{fmt(r['cover'], .5):>6}{fmt(r['cover'], .25):>6}"
              f"{fmt(r['cover'], .75):>6}", file=out)

    print("\nFirst moves along each line's path, by the Kaizo split they come in", file=out)
    hist = {k: collections.Counter() for k in ("stab_fair", "stab_strong", "stab_big",
                                              "cover_fair")}
    for line in lines():
        got = milestones(line)
        for k in hist:
            hist[k][split_of("kaizo", got[k]) if k in got else "never"] += 1
    cols = SPLIT_NAMES + ["never"]
    print(f"{'milestone':12}" + "".join(f"{s[:8]:>9}" for s in cols), file=out)
    for k, c in hist.items():
        print(f"{k:12}" + "".join(f"{c[s]:>9}" for s in cols), file=out)

    print("\nThe first strong same-type move against the stage the line is in", file=out)
    rel = collections.Counter()
    for line in lines():
        got = milestones(line)
        if "stab_strong" not in got:
            rel["never"] += 1
            continue
        lv = got["stab_strong"]
        stage = max(i for i, sp in enumerate(line) if (reached_at(sp) if i else 0) <= lv)
        rel[f"{len(line)}-stage line, stage {stage + 1}"] += 1
    for k in sorted(rel):
        print(f"  {k}: {rel[k]}", file=out)

    print("\nEvolved stages: level of a move both stages list, earlier stage against later",
          file=out)
    diffs = [lb - la for _a, _b, _m, la, lb in stage_shifts()]
    c = collections.Counter("same" if d == 0 else "later" if d > 0 else "earlier" for d in diffs)
    print(f"  {len(diffs)} shared moves: {dict(sorted(c.items()))}; median delay where later "
          f"{statistics.median([d for d in diffs if d > 0] or [0])} levels", file=out)

    print("\nKaizo against vanilla, the same species and move, in splits (each game's own)",
          file=out)
    by_split = collections.defaultdict(list)
    for _sp, _name, vl, kl in against_vanilla():
        by_split[split_of("kaizo", kl)].append(split_index("kaizo", kl)
                                              - split_index("vanilla", vl))
    for s in SPLIT_NAMES:
        d = by_split.get(s)
        if d:
            print(f"  {s:10}{len(d):>5} moves, median shift {statistics.median(d):+.0f} splits, "
                  f"{sum(x < 0 for x in d)} earlier, {sum(x > 0 for x in d)} later", file=out)

    print("\nLevel-1 moves of first stages", file=out)
    ones = [[e for e in entries(ln[0]) if e["level"] <= 1] for ln in lines()]
    counts = collections.Counter(len(o) for o in ones)
    print(f"  moves at level 1: {dict(sorted(counts.items()))}", file=out)
    bands = collections.Counter(e.get("band") or e["kind"] for o in ones for e in o)
    print(f"  their kinds and bands: {dict(sorted(bands.items()))}", file=out)

    print("\nSetup moves met along the lines, per Kaizo split", file=out)
    setup = collections.Counter(e["split"] for ln in lines() for e in path(ln)
                                if e.get("setup") and e["level"] > 1)
    print("  " + ", ".join(f"{s} {setup[s]}" for s in SPLIT_NAMES), file=out)

    names = collections.Counter(e["move"] for ln in lines() for e in path(ln)
                                if e.get("setup") and e["level"] > 1)
    print(f"  which: {dict(sorted(names.items()))}", file=out)

    last = [max((l for l, _m in r["list"]), default=0) for r in ks.values()]
    print(f"\nLast level-up move: median level {statistics.median(last)}, "
          f"{sum(l > splits('kaizo')[-2][1] for l in last)} species past Volkner", file=out)

    print("\nEach damaging move past level 1 against the best of its type already known",
          file=out)
    kinds = collections.Counter()
    downs = collections.Counter()
    for line in lines():
        best = {}
        for e in path(line):
            if e["kind"] != "damage":
                continue
            had = best.get(e["type"])
            if e["level"] > 1:
                if had is None:
                    kinds["new type"] += 1
                elif e["power"] > had * 1.1:
                    kinds["stronger"] += 1
                elif e["power"] >= had * 0.9:
                    kinds["about the same"] += 1
                else:
                    kinds["weaker"] += 1
                    downs[e["move"]] += 1
            best[e["type"]] = max(had or 0, e["power"])
    print(f"  {dict(sorted(kinds.items()))}", file=out)
    print(f"  the weaker ones most often: {downs.most_common(15)}", file=out)

    print("\nFeeble damaging moves (under 50 a turn) met past level 1, by Kaizo split", file=out)
    feeble = collections.Counter()
    which = collections.Counter()
    for line in lines():
        for e in path(line):
            if e["kind"] == "damage" and e["level"] > 1 and e["power"] < WEAK:
                feeble[e["split"]] += 1
                which[e["move"]] += 1
    print("  " + ", ".join(f"{s} {feeble[s]}" for s in SPLIT_NAMES), file=out)
    print(f"  most often: {which.most_common(15)}", file=out)

    print("\nWhat an evolved stage lists at the level it is reached", file=out)
    evo = collections.Counter()
    for sp in _reached():
        at = [e for e in entries(sp) if e["level"] == reached_at(sp)]
        evo["none" if not at else "status only" if all(e["kind"] != "damage" for e in at)
            else "damage " + max((e for e in at if e["kind"] == "damage"),
                                 key=lambda e: e["power"])["band"]] += 1
    print(f"  {dict(sorted(evo.items()))}", file=out)

    print("\nA line's strength against how soon it gets its first strong same-type move",
          file=out)
    by_num = {v.get("num"): v for v in data.raw("kaizo")["poks"].values()}
    consts = {v: k for k, v in species_constants().items()}
    pairs = []
    for line in lines():
        bst = sum(by_num[consts[line[-1]]]["bs"].values())
        got = milestones(line)
        pairs.append((bst, split_index("kaizo", got["stab_strong"])
                      if "stab_strong" in got else len(SPLIT_NAMES)))
    for lo, hi in ((0, 400), (400, 480), (480, 530), (530, 999)):
        grp = [s for b, s in pairs if lo <= b < hi]
        if grp:
            print(f"  final stage total {lo} to {hi - 1}: {len(grp)} lines, median split "
                  f"{SPLIT_NAMES[min(int(statistics.median(grp)), len(SPLIT_NAMES) - 1)]}"
                  f" ({statistics.median(grp):.1f})", file=out)


def rules_report(out=sys.stdout):
    """Part 2: the placement rules scored on held-out lines, and the dead-weight
    rule on Ian's named moves, on Kaizo's own lists and on Oxide's."""
    print("Placing a move in a split, fitted on four fifths of the families and scored on "
          "the fifth (moves past level 1 along the paths)", file=out)
    print(f"{'rule':46}{'moves':>7}{'mean miss':>11}{'exact':>7}{'within 1':>10}", file=out)
    for name, r in placement_test().items():
        print(f"{name:46}{r['n']:>7}{r['mean']:>11.2f}{r['exact']:>7.2f}{r['within_one']:>10.2f}",
              file=out)

    print("\nThe dead-weight rule on Ian's named moves (Oxide's values; Octazooka at "
          "vanilla's): where it would stay", file=out)
    for name, kept in named_check().items():
        print(f"  {name:12} {', '.join(kept) if kept else 'nowhere'}", file=out)

    n, start, later = kaizo_dead_weight()
    print(f"\nKaizo's own lists: {sum(start.values())} starting moves and "
          f"{sum(later.values())} later ones of {n} called dead weight", file=out)
    print(f"  starting: {start.most_common(10)}", file=out)
    print(f"  later: {later.most_common(10)}", file=out)

    flagged = oxide_dead_weight()
    by_move = collections.Counter(m for _s, _l, m, _sp, _w in flagged)
    reasons = collections.Counter(w.split(",")[0].split(" ")[0] if w[0].isalpha() else "acc"
                                  for *_x, w in flagged)
    print(f"\nOxide's lists now: {len(flagged)} entries called dead weight, "
          f"{len(by_move)} moves", file=out)
    print("  " + ", ".join(f"{m} {c}" for m, c in by_move.most_common(40)), file=out)
    named = [m for m in by_move if m in NAMED]
    print(f"  of Ian's named moves, in Oxide's lists and caught: {named}", file=out)


def show_line(name, out=sys.stdout):
    want = "SPECIES_" + name.upper()
    for line in lines():
        if want not in line:
            continue
        for sp in line:
            rec = kaizo_lists()[sp]
            print(f"\n{rec['name']} ({'/'.join(rec['types'])}), reached at "
                  f"{reached_at(sp) if sp in _reached() else 'the start'}", file=out)
            for e in entries(sp):
                if e["kind"] == "unknown":
                    print(f"  {e['level']:>3} {e['move']:16} not in Kaizo's data", file=out)
                    continue
                tag = "STAB" if e["stab"] and e["kind"] == "damage" else ""
                print(f"  {e['level']:>3} {e['split']:9} {e['move']:16} {e['kind']:11} "
                      f"{e['power']:>6} {e['band'] or '':7} {tag}", file=out)
        print("\nmilestones along the path:", milestones(line), file=out)
        return
    print(f"no line holds {want}", file=out)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--line", help="print one line's Kaizo lists, read")
    ap.add_argument("--rules", action="store_true", help="part 2: the rules tested")
    args = ap.parse_args(argv)
    if args.line:
        show_line(args.line)
    elif args.rules:
        rules_report()
    else:
        report()
    return 0


if __name__ == "__main__":
    sys.exit(main())

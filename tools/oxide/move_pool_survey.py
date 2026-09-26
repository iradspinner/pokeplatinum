#!/usr/bin/env python3
"""The move pool survey: every move a species can learn, and the cull candidates.

    PYTHONPATH=. python3 tools/oxide/move_pool_survey.py --csv docs/oxide/move-pool-survey.csv
    PYTHONPATH=. python3 tools/oxide/move_pool_survey.py --report
    PYTHONPATH=. python3 tools/oxide/move_pool_survey.py --appendix /tmp/appendix.md

Ian asked on 2026-09-27 for a survey of Oxide's learnable moves, to scope a cull
of useless, outclassed or niche moves from learnsets. It changes no game data.
It reads the tree as it stands: move records from res/moves/, learnsets from
every species' and form's data.json (level, TM, tutor and egg lists), the TM
items for what each machine teaches, docs/oxide/species-pick-list.csv for which
species the player can obtain, and res/trainers/data/ for who uses what.

A line is an evolution family (the encounter tool's `dex.lines`), and a line is
obtainable when any member is `native` or `new` in the pick-list. A move counts
for a line when any member learns it by any route.

`--csv` writes one row per learnable move, `--appendix` the same as the
Markdown table at the end of docs/oxide/move-pool-survey.md, and `--report`
prints the grouped candidate lists and what the recommended first cut costs,
which the survey's prose is written from. hg-engine's C was read by hand for
ENGINE_NOTES; nothing here needs the donor or base ROM.
"""
import argparse
import collections
import csv
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)

from tools.oxide.encounters import dex, pokedex            # noqa: E402
from tools.oxide.encounters.calc_trainers import default_moves, FORM_FOLDERS  # noqa: E402

# Ian's standing ruling (staples survey, 2026-09-26): the player never sets
# weather, so these leave every player learnset whatever the survey says.
WEATHER_EFFECTS = {"WEATHER_RAIN", "WEATHER_SUN", "WEATHER_SANDSTORM", "WEATHER_HAIL",
                   "WEATHER_SNOW"}

# Terrain is held for Ian's decision (element 4). Until it lands the four
# Terrain moves say "But nothing happened!" and Steel Roller is a plain
# 130-power hit; the moves that read terrain are in ENGINE_NOTES.
TERRAIN_SETTERS = {"MOVE_ELECTRIC_TERRAIN", "MOVE_GRASSY_TERRAIN", "MOVE_MISTY_TERRAIN",
                   "MOVE_PSYCHIC_TERRAIN"}


# Moves whose record says "plain hit" (effect 0) or names a Platinum effect,
# but whose real behaviour hg-engine carries in C keyed on the move id, so the
# converter's effect-by-effect audit never saw them; or which hg-engine never
# implemented at all. Read from hg-engine's src/ (2026-09-27) and Oxide's
# src/battle/, where none of these is named. None is seen in game.
ENGINE_NOTES = {
    "MOVE_MIND_BLOWN": "plain 150 hit; the user's loss of half its HP is missing",
    "MOVE_SCALE_SHOT": "hits two to five times; the Speed rise and Defense drop are missing",
    "MOVE_SPIKY_SHIELD": "a plain Protect; the damage to a contact attacker is missing",
    "MOVE_BANEFUL_BUNKER": "a plain Protect; the poison on contact is missing",
    "MOVE_SALT_CURE": "plain 40 hit; the damage every turn is missing (hg-engine lacks it too)",
    "MOVE_SKY_DROP": "plain 60 hit; the two-turn lift is missing",
    "MOVE_CORE_ENFORCER": "plain hit; the ability suppression is missing (hg-engine lacks it too)",
    "MOVE_BEAK_BLAST": "a priority -3 hit; the burn on contact while it heats up is missing",
    "MOVE_FLAME_BURST": "plain hit; the splash on the target's partner is missing (doubles only)",
    "MOVE_SHORE_UP": "heals more in sun, as Morning Sun does, instead of in sandstorm",
    "MOVE_TELEKINESIS": "status move running the plain-hit script: its effect never happens",
    "MOVE_MAGIC_ROOM": "status move running the plain-hit script: its effect never happens",
    "MOVE_ALLY_SWITCH": "status move running the plain-hit script: its effect never happens",
    "MOVE_TOPSY_TURVY": "status move running the plain-hit script: its effect never happens",
    "MOVE_FLOWER_SHIELD": "status move running the plain-hit script: its effect never happens",
    "MOVE_FAIRY_LOCK": "status move running the plain-hit script: its effect never happens",
    "MOVE_AROMATIC_MIST": "status move running the plain-hit script: its effect never happens",
    "MOVE_MAGNETIC_FLUX": "status move running the plain-hit script: its effect never happens",
    "MOVE_SPEED_SWAP": "status move running the plain-hit script: its effect never happens",
    "MOVE_TEATIME": "status move running the plain-hit script: its effect never happens",
    "MOVE_OCTOLOCK": "status move running the plain-hit script: its effect never happens",
    "MOVE_EXPANDING_FORCE": "plain 80 hit; its Psychic Terrain boost waits on terrain",
    "MOVE_GRASSY_GLIDE": "plain 55 hit; its priority in Grassy Terrain waits on terrain",
    "MOVE_TERRAIN_PULSE": "plain 50 Normal hit; its type and power change wait on terrain",
    "MOVE_NATURES_MADNESS": "halves HP; table power 0, where computed powers keep 1",
}

# Oxide's battle_lib.c lists that abilities read (Iron Fist, Sharpness,
# Punk Rock and Soundproof, Bulletproof). A move on one of these can matter to
# a line with the ability even when another move beats it on the numbers.
TAG_LISTS = {"sSoundMoves": "sound", "sBallAndBombMoves": "ball", "sSlicingMoves": "slicing",
             "sPunchingMoves": "punch"}

# Moves that only do something with a partner on the field. Oxide has double
# trainer battles, and wild doubles are coming with element 8, so these are
# not dead, but in a single battle each fails or has no target.
DOUBLES_ONLY = {
    "MOVE_HELPING_HAND": "boosts the partner's move",
    "MOVE_FOLLOW_ME": "draws attacks away from the partner",
    "MOVE_RAGE_POWDER": "draws attacks away from the partner",
    "MOVE_ALLY_SWITCH": "swaps places with the partner",
    "MOVE_AFTER_YOU": "makes the target move next; no use in singles",
    "MOVE_AROMATIC_MIST": "raises the partner's Sp. Def",
    "MOVE_COACHING": "raises the partner's Attack and Defense; fails alone",
    "MOVE_HEAL_PULSE": "heals a target; in singles only the foe",
    "MOVE_QUASH": "makes the target move last",
    "MOVE_DECORATE": "raises the partner's Attack and Sp. Atk",
    "MOVE_HOLD_HANDS": "does nothing even in doubles",
    "MOVE_INSTRUCT": "makes the partner repeat its move",
    "MOVE_SPOTLIGHT": "makes a foe the only target",
    "MOVE_WIDE_GUARD": "blocks spread moves, which in singles are rare",
    "MOVE_FLOWER_SHIELD": "raises Defense of every Grass type",
    "MOVE_ROTOTILLER": "raises attack stats of every grounded Grass type",
    "MOVE_MAGNETIC_FLUX": "raises Defense and Sp. Def of Plus and Minus holders",
    "MOVE_GEAR_UP": "raises Attack and Sp. Atk of Plus and Minus holders",
}

# Moves whose effect is nothing or next to nothing in a battle that matters.
DOES_NOTHING = {
    "MOVE_SPLASH": "does nothing",
    "MOVE_CELEBRATE": "does nothing",
    "MOVE_HOLD_HANDS": "does nothing",
    "MOVE_HAPPY_HOUR": "doubles prize money; no battle effect",
    "MOVE_TELEPORT": "flees a wild battle; fails against a trainer",
    "MOVE_ELECTRIC_TERRAIN": "stub: \"But nothing happened!\" until terrain exists",
    "MOVE_GRASSY_TERRAIN": "stub: \"But nothing happened!\" until terrain exists",
    "MOVE_MISTY_TERRAIN": "stub: \"But nothing happened!\" until terrain exists",
    "MOVE_PSYCHIC_TERRAIN": "stub: \"But nothing happened!\" until terrain exists",
}

# Effects a hit can carry without a cost to the user. A move with one of these
# can outclass a move that has no effect or the same effect at a lower chance.
CLEAN_EFFECTS = {
    "HIT", "HIGH_CRITICAL", "BYPASS_ACCURACY", "ALWAYS_CRITICAL", "SMACK_DOWN",
    "TRI_ATTACK", "THAW_AND_BURN_HIT", "INCINERATE", "REMOVE_HELD_ITEM",
    "STEAL_HELD_ITEM", "BADLY_POISON_HIT", "HIT_TWICE", "THUNDER", "BLIZZARD",
    "HURRICANE", "IGNORE_EVATION_REMOVE_DARK_IMMUNE", "PRIORITY_1",
} | {e for e in ("BURN_HIT", "FREEZE_HIT", "PARALYZE_HIT", "POISON_HIT", "FLINCH_HIT",
                 "CONFUSE_HIT", "LOWER_ATTACK_HIT", "LOWER_DEFENSE_HIT", "LOWER_SPEED_HIT",
                 "LOWER_SP_ATK_HIT", "LOWER_SP_DEF_HIT", "LOWER_SP_DEF_2_HIT",
                 "LOWER_ACCURACY_HIT", "RAISE_ATTACK_HIT", "RAISE_DEF_HIT",
                 "RAISE_DEF_2_HIT", "RAISE_SPEED_HIT", "RAISE_SP_ATK_HIT",
                 "RAISE_ALL_STATS_HIT", "FLINCH_BURN_HIT", "FLINCH_FREEZE_HIT",
                 "FLINCH_PARALYZE_HIT", "HIGH_CRITICAL_BURN_HIT", "HIGH_CRITICAL_POISON_HIT",
                 "RECOVER_HALF_DAMAGE_DEALT", "RECOVER_THREE_QUARTERS_DAMAGE_DEALT",
                 "SPEED_DOWN_HIT", "DOUBLE_DAMAGE_FLY_OR_BOUNCE", "DOUBLE_DAMAGE_DIG",
                 "DOUBLE_DAMAGE_DIVE", "DOUBLE_POWER_IF_TARGET_HIT")}


def species_records():
    """(species constant, form folder or None, data) for every species and form."""
    out = []
    for species in pokedex.species_list(ROOT):
        folder = pokedex.folder_of(species)
        with open(os.path.join(ROOT, "res", "pokemon", folder, "data.json"), encoding="utf-8") as f:
            out.append((species, None, json.load(f)))
        for p in sorted(glob.glob(os.path.join(ROOT, "res", "pokemon", folder, "forms", "*", "data.json"))):
            with open(p, encoding="utf-8") as f:
                out.append((species, os.path.basename(os.path.dirname(p)), json.load(f)))
    return out


def obtainable_lines():
    """Line ids with a member the pick-list marks native or new."""
    lines = dex.lines(ROOT)
    out = set()
    for row in dex.pick_list(ROOT):
        if row["status"] in ("native", "new") and row["constant"]:
            out.add(lines.get(row["constant"], row["constant"]))
    return out


def collect():
    """Everything the survey reads, in one dict."""
    moves = pokedex.moves(ROOT)
    machines = pokedex.machines(ROOT)
    machine_of = {m: k for k, m in machines.items()}
    tutors = {t["move"]: t["location"].replace("TUTOR_LOCATION_", "").replace("_", " ").title()
              for t in json.load(open(os.path.join(ROOT, "res", "pokemon", "move_tutors.json")))}
    lines = dex.lines(ROOT)
    obtainable = obtainable_lines()
    records = species_records()

    # move -> line -> set of routes; move -> line -> earliest level-up level
    routes = collections.defaultdict(lambda: collections.defaultdict(set))
    first_level = collections.defaultdict(dict)
    types_of_line = collections.defaultdict(set)
    level_sets = {}
    for species, form, data in records:
        line = lines.get(species, species)
        types_of_line[line] |= set(data.get("types") or [])
        learnset = data.get("learnset") or {}
        level_sets[(species, form)] = [tuple(e) for e in learnset.get("by_level") or []]
        for lv, mv in learnset.get("by_level") or []:
            routes[mv][line].add("level")
            if lv < first_level[mv].get(line, 999):
                first_level[mv][line] = lv
        for tm in learnset.get("by_tm") or []:
            if tm in machines:
                routes[machines[tm]][line].add("tm")
        for mv in learnset.get("by_tutor") or []:
            routes[mv][line].add("tutor")
        for mv in learnset.get("egg_moves") or []:
            routes[mv][line].add("egg")

    trainers = trainer_uses(level_sets)
    return {"moves": moves, "machine_of": machine_of, "tutors": tutors, "lines": lines,
            "obtainable": obtainable, "records": records, "routes": routes,
            "first_level": first_level, "types_of_line": types_of_line,
            "level_sets": level_sets, "trainers": trainers, "tags": move_tags(),
            "c_special": c_special()}


def trainer_uses(level_sets):
    """move -> {"default": [trainer stems], "hand": [trainer stems]}, counting only
    trainers some map in the game fields (the balance track's split resolver),
    plus the stems of trainers that field nothing, for the record."""
    from tools.oxide.balance import splits
    ids = splits._trainer_ids()
    out = collections.defaultdict(lambda: {"default": set(), "hand": set()})
    out["_default_sets"] = {}
    split_of = {}
    for path in sorted(glob.glob(os.path.join(ROOT, "res", "trainers", "data", "*.json"))):
        stem = os.path.basename(path)[:-5]
        if stem.startswith("dummy_"):
            continue
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        party = data.get("party") or []
        if not party:
            continue
        tr_id = ids.get("TRAINER_" + stem.upper())
        split = splits.trainer_split(tr_id) if tr_id is not None else None
        if not split:
            continue
        split_of[stem] = split
        has_moves = isinstance(party[0].get("moves"), list)
        for mon in party:
            if has_moves:
                for mv in mon.get("moves") or []:
                    if mv and mv != "MOVE_NONE":
                        out[mv]["hand"].add(stem)
            else:
                form = FORM_FOLDERS.get((mon["species"], mon.get("form") or 0))
                learnset = level_sets.get((mon["species"], form)) or level_sets.get((mon["species"], None)) or []
                got = default_moves(learnset, mon["level"])
                for mv in got:
                    out[mv]["default"].add(stem)
                out["_default_sets"].setdefault(stem, []).append(
                    (mon["species"], form, mon["level"], got))
    out["_split_of"] = split_of
    return out


def is_attack(rec):
    return rec["class"] != "STATUS"


def fixed_power(rec):
    return is_attack(rec) and (rec["power"] or 0) > 1


def acc(rec):
    """A never-miss move stores accuracy 0; rank it above 100."""
    return 101 if not rec["accuracy"] else rec["accuracy"]


def learners_of(d, move, only_obtainable=True):
    lines = d["routes"].get(move, {})
    return {l: r for l, r in lines.items() if not only_obtainable or l in d["obtainable"]}


def c_special():
    """Moves Oxide's battle C handles by name somewhere other than a plain list
    entry: their record may say "plain hit" while the C gives them a computed
    power, a different attacking stat or a condition. Such a move is never
    judged on its numbers alone. The trainer AI is left out, since it only
    scores moves. Pound is named only as the confusion self-hit."""
    out = set()
    for path in glob.glob(os.path.join(ROOT, "src", "battle", "*.c")):
        for line in open(path, encoding="utf-8"):
            if re.fullmatch(r"\s*MOVE_\w+,?\s*(//.*)?\n?", line):
                continue
            out.update(re.findall(r"\bMOVE_[A-Z0-9_]+\b", line))
    return out - {"MOVE_POUND"}


def move_tags():
    """{MOVE_X: set of tags} from the ability lists in battle_lib.c."""
    text = open(os.path.join(ROOT, "src", "battle", "battle_lib.c"), encoding="utf-8").read()
    out = collections.defaultdict(set)
    for name, tag in TAG_LISTS.items():
        body = re.search(r"\b%s\[\]\s*=\s*\{(.*?)\};" % name, text, re.S)
        for mv in re.findall(r"MOVE_\w+", body.group(1) if body else ""):
            out[mv].add(tag)
    return out


def engine_status(d, move):
    rec = d["moves"][move]
    if move in TERRAIN_SETTERS:
        return "stub: nothing happens (terrain held)"
    if move == "MOVE_STEEL_ROLLER":
        return "stub: plain 130 hit, should fail without terrain"
    if rec["stub"]:
        return "stub: plain hit" if is_attack(rec) else "stub: nothing happens"
    if move in ENGINE_NOTES:
        return "partial: " + ENGINE_NOTES[move]
    return "runs"


def humanise_effect(rec):
    e = rec["effect"]
    text = e.lower().replace("sp_atk", "sp. atk").replace("sp_def", "sp. def")
    text = text.replace("_", " ").replace("evation", "evasion").replace("supress", "suppress")
    if rec["effect_chance"] and rec["effect_chance"] not in (0, 100) and e != "HIT":
        text += f" ({rec['effect_chance']}%)"
    return "plain hit" if e == "HIT" else text


def beats(ra, rb, special=frozenset()):
    """True when attack B is at least as good as attack A on every count and
    better on one: same type and category, power, accuracy and priority no
    lower, an effect that costs the user nothing, and A's effect either none
    or B's own at no higher chance. A move whose effect the engine does not
    run (ENGINE_NOTES) is judged on what it does in Oxide, a plain hit."""
    if not (fixed_power(ra) and fixed_power(rb)):
        return False
    if ra["move"] in special or rb["move"] in special:
        return False
    if rb["type"] != ra["type"] or rb["class"] != ra["class"]:
        return False
    eff_a = "HIT" if ra["move"] in ENGINE_NOTES and ra["effect"] == "HIT" else ra["effect"]
    if rb["effect"] not in CLEAN_EFFECTS or rb["move"] in ENGINE_NOTES:
        return False
    if eff_a != "HIT" and not (eff_a == rb["effect"]
                               and (ra["effect_chance"] or 0) <= (rb["effect_chance"] or 0)):
        return False
    if rb["priority"] < ra["priority"] or rb["power"] < ra["power"] or acc(rb) < acc(ra):
        return False
    if (rb["power"], acc(rb)) == (ra["power"], acc(ra)) and rb["pp"] <= ra["pp"]:
        return False            # the same numbers: a near-duplicate, not outclassed
    return True


def outclassed(d):
    """For each attack A that some move beats, how many obtainable lines that
    learn A also learn a move that beats it, and how many get one by level-up
    no later than they get A. `strict` is every line."""
    moves = d["moves"]
    learnable = [m for m in d["routes"] if m in moves and learners_of(d, m)]
    tags = d["tags"]
    out = {}
    for a in learnable:
        ra = moves[a]
        betters = [b for b in learnable if b != a and beats(ra, moves[b], d["c_special"])]
        if not betters:
            continue
        la = learners_of(d, a)
        covered, in_time, who = 0, 0, collections.Counter()
        for line in la:
            have = [b for b in betters if line in d["routes"][b]]
            if not have:
                continue
            covered += 1
            who.update(have)
            a_lv = d["first_level"][a].get(line)
            if a_lv is not None and any(d["first_level"][b].get(line, 999) <= a_lv for b in have):
                in_time += 1
            elif a_lv is None:
                in_time += 1        # A is a TM, tutor or egg move there; B is already an option
        lost_tags = tags.get(a, set()) - set().union(*(tags.get(b, set()) for b in betters))
        out[a] = {"lines": len(la), "covered": covered, "in_time": in_time,
                  "strict": covered == len(la), "betters": [b for b, _ in who.most_common(3)],
                  "lost_tags": sorted(lost_tags)}
    return out


def near_duplicates(d):
    """Groups of attacks with one type, category and effect whose power and
    accuracy sit within ten of each other, and groups of status moves with
    the same effect."""
    moves = d["moves"]
    learnable = [m for m in d["routes"] if m in moves and learners_of(d, m)]
    groups = collections.defaultdict(list)
    for m in learnable:
        r = moves[m]
        if is_attack(r) and fixed_power(r):
            if m in d["c_special"]:
                continue        # its C makes it a different move from its record
            groups[("atk", r["type"], r["class"], r["effect"])].append(m)
        elif not is_attack(r):
            groups[("status", r["effect"])].append(m)
    out = []
    for key, ms in groups.items():
        if len(ms) < 2:
            continue
        if key[0] == "atk":
            ms = sorted(ms, key=lambda m: moves[m]["power"])
            # chain members whose power and accuracy are within ten of a neighbour
            cluster = [ms[0]]
            for m in ms[1:]:
                prev = moves[cluster[-1]]
                if abs(moves[m]["power"] - prev["power"]) <= 10 and abs(acc(moves[m]) - acc(prev)) <= 10:
                    cluster.append(m)
                else:
                    if len(cluster) > 1:
                        out.append((key, cluster))
                    cluster = [m]
            if len(cluster) > 1:
                out.append((key, cluster))
        else:
            out.append((key, sorted(ms)))
    return out


def early_attacks(d, line, cap, removed=frozenset()):
    """Attacks a line can know by level-up at or below `cap`. The first stage
    counts from level 1; a later stage's level-1 entries are its evolution and
    relearner moves, so they count only from the level it evolves at, which is
    approximated here as not at all."""
    members = [s for s, l in d["lines"].items() if l == line]
    base = set(dex.line_base(ROOT, line))
    got = set()
    for s in members:
        for lv, mv in d["level_sets"].get((s, None), []):
            if lv > cap or (s not in base and lv <= 1):
                continue
            rec = d["moves"].get(mv)
            if rec and is_attack(rec) and mv not in removed:
                got.add(mv)
    return got


def row(d, move):
    rec = d["moves"][move]
    obt = learners_of(d, move)
    every = learners_of(d, move, only_obtainable=False)
    by = collections.Counter(k for r in obt.values() for k in r)
    firsts = [d["first_level"][move][l] for l in obt if l in d["first_level"][move]]
    tr = d["trainers"].get(move, {"default": set(), "hand": set()})
    return {
        "move": move, "name": rec["name"], "type": rec["type"].title(),
        "category": rec["class"].title(), "power": rec["power"] if is_attack(rec) else "",
        "accuracy": rec["accuracy"] if rec["accuracy"] else "never misses",
        "pp": rec["pp"], "priority": rec["priority"], "effect": humanise_effect(rec),
        "engine": engine_status(d, move),
        "lines": len(obt), "by_level": by["level"], "by_tm": by["tm"],
        "by_tutor": by["tutor"], "by_egg": by["egg"],
        "unobtainable_lines": len(every) - len(obt),
        "earliest_level": min(firsts) if firsts else "",
        "tm": d["machine_of"].get(move, ""), "tutor": d["tutors"].get(move, ""),
        "trainer_default": len(tr["default"]), "trainer_hand": len(tr["hand"]),
    }


def engine_label(status):
    """The engine column, short, for the appendix table."""
    if "never happens" in status or "nothing happens" in status:
        return "no effect"
    if status.startswith("stub: plain 130"):
        return "stub, hits"
    if status.startswith("partial"):
        return "partial"
    return "runs"


def write_appendix(d, path):
    """The survey's appendix: one Markdown row per learnable move."""
    rows = [row(d, m) for m in sorted(d["routes"], key=lambda m: d["moves"][m]["name"]) if m in d["moves"]]
    head = ["Move", "Type", "Cat.", "Pow.", "Acc.", "PP", "Effect", "Engine", "Lines",
            "Lv", "TM", "Tutor", "Egg", "First lv", "Taught by", "Trainer defaults"]
    out = ["| " + " | ".join(head) + " |", "|" + "---|" * len(head)]
    for r in rows:
        acc_ = "always" if r["accuracy"] == "never misses" else r["accuracy"]
        teach = " ".join(x for x in (r["tm"], "tutor" if r["tutor"] else "") if x)
        cells = [r["name"], r["type"], r["category"][:4] + ".", r["power"], acc_, r["pp"],
                 r["effect"], engine_label(r["engine"]), r["lines"], r["by_level"] or "",
                 r["by_tm"] or "", r["by_tutor"] or "", r["by_egg"] or "", r["earliest_level"],
                 teach, r["trainer_default"] or ""]
        out.append("| " + " | ".join(str(c) for c in cells) + " |")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(out) + "\n")
    return rows


def write_csv(d, path):
    rows = [row(d, m) for m in sorted(d["routes"], key=lambda m: d["moves"][m]["name"]) if m in d["moves"]]
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    return rows


# The recommended first cut (docs/oxide/move-pool-survey.md). Every move here
# does nothing in Oxide today, and removing it costs no line an early attack, a
# level-1 move, a trainer's default set, a TM or a tutor. Splash and Teleport
# would leave lines with no level-1 move, so they wait on a replacement.
FIRST_CUT = {
    # dead: a status move whose record carries the plain-hit effect
    "MOVE_TELEKINESIS", "MOVE_MAGIC_ROOM", "MOVE_ALLY_SWITCH", "MOVE_TOPSY_TURVY",
    "MOVE_FLOWER_SHIELD", "MOVE_FAIRY_LOCK", "MOVE_AROMATIC_MIST", "MOVE_MAGNETIC_FLUX",
    "MOVE_SPEED_SWAP", "MOVE_TEATIME", "MOVE_OCTOLOCK",
    # outclassed, and plain hits in Oxide whatever their text says
    "MOVE_SKY_DROP", "MOVE_SALT_CURE",
}
# Cut as well if Ian leaves terrain out: the four setters say "But nothing
# happened!" and Steel Roller is a free 130-power hit.
TERRAIN_CUT = {"MOVE_ELECTRIC_TERRAIN", "MOVE_GRASSY_TERRAIN", "MOVE_MISTY_TERRAIN",
               "MOVE_PSYCHIC_TERRAIN", "MOVE_STEEL_ROLLER"}
CAPS = {"Roark": 16, "Gardenia": 26}


def cut_cost(d, cut):
    """What removing `cut` from every learnset costs: lines whose attacks by
    the first two caps drop below two or lose their last same-type attack,
    lines left with no level-1 move, trainer default sets that change, TMs
    and tutors left teaching a cut move, and one-line moves lost."""
    out = {"lines_hit": [], "no_level1": [], "trainers": [], "tms": [], "tutors": [],
           "signatures": [], "lines_touched": set()}
    for line in sorted(d["obtainable"]):
        for name, cap in CAPS.items():
            before = early_attacks(d, line, cap)
            after = early_attacks(d, line, cap, frozenset(cut))
            if before == after:
                continue
            types = d["types_of_line"][line]
            stab_before = {m for m in before if "TYPE_" + d["moves"][m]["type"] in types}
            stab_after = {m for m in after if "TYPE_" + d["moves"][m]["type"] in types}
            if len(after) < 2 or (stab_before and not stab_after):
                out["lines_hit"].append((line, name, sorted(before - after), len(after), len(stab_after)))
        for s in (m for m, l in d["lines"].items() if l == line):
            lv1 = [mv for lv, mv in d["level_sets"].get((s, None), []) if lv <= 1]
            if lv1 and all(mv in cut for mv in lv1) and s in dex.line_base(ROOT, line):
                out["no_level1"].append(s)
    for mv in sorted(cut):
        for l in learners_of(d, mv):
            out["lines_touched"].add(l)
        if d["machine_of"].get(mv):
            out["tms"].append((d["machine_of"][mv], mv))
        if mv in d["tutors"]:
            out["tutors"].append(mv)
        if len(learners_of(d, mv, only_obtainable=False)) == 1:
            out["signatures"].append(mv)
    for stem, mons in sorted(d["trainers"]["_default_sets"].items()):
        for species, form, level, got in mons:
            if d["lines"].get(species, species) not in d["obtainable"] or not set(got) & set(cut):
                continue
            learnset = d["level_sets"].get((species, form)) or d["level_sets"].get((species, None))
            now = default_moves([e for e in learnset if e[1] not in cut], level)
            out["trainers"].append((stem, d["trainers"]["_split_of"].get(stem), species, level,
                                    got, now))
    out["lines_touched"] = len(out["lines_touched"])
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--csv", help="write the per-move table here")
    ap.add_argument("--report", action="store_true", help="print the grouped lists as JSON")
    ap.add_argument("--appendix", help="write the survey's appendix table (Markdown) here")
    args = ap.parse_args(argv)
    d = collect()
    if args.appendix:
        write_appendix(d, args.appendix)
    if args.csv:
        rows = write_csv(d, args.csv)
        print(f"{len(rows)} learnable moves written to {args.csv}", file=sys.stderr)
    if args.report:
        json.dump(report(d), sys.stdout, indent=1, default=sorted)
        print()


def group(d, test):
    """{move name: obtainable lines} for the learnable moves passing `test`."""
    return {d["moves"][m]["name"]: len(learners_of(d, m))
            for m in sorted(d["routes"]) if m in d["moves"] and test(m)}


def report(d):
    """The numbers the survey's prose quotes."""
    moves = d["moves"]
    learnable = sorted(m for m in d["routes"] if m in moves)
    obt = {m for m in learnable if learners_of(d, m)}
    lines_all = set(d["lines"].values())
    trainers = d["trainers"]
    default_users = set(trainers["_default_sets"])
    return {
        "learnable": len(learnable),
        "learnable_by_obtainable": len(obt),
        "only_unobtainable": sorted(set(learnable) - obt),
        "obtainable_lines": len(d["obtainable"]),
        "lines": len(lines_all),
        "trainers_in_play": len(trainers["_split_of"]),
        "trainers_with_default_moves": len(default_users),
        "outclassed": outclassed(d),
        "near_duplicates": [(list(k), v) for k, v in near_duplicates(d)],
        "groups": {
            "weather": group(d, lambda m: moves[m]["effect"] in WEATHER_EFFECTS),
            "doubles_only": group(d, lambda m: m in DOUBLES_ONLY),
            "does_nothing": group(d, lambda m: m in DOES_NOTHING),
            "engine": group(d, lambda m: engine_status(d, m) != "runs"),
            "niche": group(d, lambda m: 0 < len(learners_of(d, m)) <= 2),
        },
        "first_cut": sorted(FIRST_CUT),
        "first_cut_cost": cut_cost(d, FIRST_CUT),
        "terrain_cut_cost": cut_cost(d, TERRAIN_CUT),
    }


if __name__ == "__main__":
    main()

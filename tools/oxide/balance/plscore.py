"""A fight prepared for the perfect-line scorer (out/design.md): its state,
its boss variants and the player's side, which plgoal3, plteam and the
planner's tests build every reading on.

A fight is a story key from tools/oxide/balance/fights.json or tr:<trainer
id>. A rival's variant is the one the box's starter meets. Importing this
module sets the simulator's player movesets to Ian's order (ian_moves).

Its September reader (read_fight, its report and command line), which
searched lines with plines.py and kept its readings in
perfectline_results/, was retired with that search on 2026-10-13; goal 3
(plgoal3.py) reads fights now.
"""
import json
import os

from . import calc, data, fightsim as fs, pool, required, splits
# Imported for what it sets up as it loads: it puts its own status, figure
# and effectiveness functions into fightsim and fightai, which every fight
# this module prepares is then read with.
from . import perfectline as pl  # noqa: F401
# Barry's starter beats the player's, so the rival variant a box meets is
# named by the player's starter (the data files are named that way too).
# Trainers the placements leave to their map's split although the player
# meets them later: Officer Somnu at Lake Verity is the return visit
# before Mars 2 (docs/oxide/pairwise-candidates.md, pair 23); the two
# Jubilife grunts of the tag battle beside Lucas or Dawn come only after
# Roark, since the Oreburgh Gym's win sets VAR_JUBILIFE_CITY_STATE to 3 and
# Jubilife's script starts the battle at 3 (Ian, 2026-10-04).
SPLIT_OVERRIDE = {420: "Candice", 414: "Gardenia", 415: "Gardenia"}
# A rival fight keeps one team for each starter the player can choose, in
# slots named by vanilla's starters: TRAINER_RIVAL_..._PIPLUP is met by a
# player who chose Piplup. Oxide's player chooses Scorbunny where vanilla's
# chose Chimchar, so the _CHIMCHAR slot is the Scorbunny player's (the
# OxiDex's Alpha tab reads it so too); a box that starts with Chimchar, as
# older boxes do, meets the same slot.
STARTER_VARIANT = {"SPECIES_TURTWIG": "TURTWIG", "SPECIES_SCORBUNNY": "CHIMCHAR", "SPECIES_CHIMCHAR": "CHIMCHAR",
                   "SPECIES_PIPLUP": "PIPLUP"}
SLOT_STARTER = {"TURTWIG": "SPECIES_TURTWIG", "CHIMCHAR": "SPECIES_SCORBUNNY", "PIPLUP": "SPECIES_PIPLUP"}
# Lucas and Dawn's teams are kept once for each starter too, in unnamed
# slots: the counterpart carries the starter weak to the player's, so a
# counterpart with the Piplup line is the Turtwig player's. The Dawn and
# Lucas versions of one slot hold the same team, for a male and a female
# player; the first listed (Dawn's) is taken.
COUNTERPART_STARTER = {"SPECIES_TURTWIG": ("Piplup", "Prinplup", "Empoleon"),
                       "SPECIES_SCORBUNNY": ("Turtwig", "Grotle", "Torterra"),
                       "SPECIES_PIPLUP": ("Chimchar", "Monferno", "Infernape")}


def slot_starter(t):
    """The player's starter this rival or counterpart team is met by, or None."""
    tag = t["constant"].rsplit("_", 1)[-1]
    if tag in SLOT_STARTER:
        return SLOT_STARTER[tag]
    names = {m["species"] for m in t["party"]}
    return next((sp for sp, line in COUNTERPART_STARTER.items() if names & set(line)), None)


# ---- Ian's movesets --------------------------------------------------------------------------------

def ian_moves(rec, can_names, tiers, types):
    """Four moves in Ian's order (2026-09-30): the strongest same-type
    attack, then the strongest attack of another type (a second same-type
    or coverage), then a third type, then the highest-tier status move the
    engine models (B or better), else a fourth attack."""
    damaging = [n for n in can_names if fs.move(n).damaging() and n not in pool.CONDITIONAL
                and fs.play_strength(n, types) > 0]
    ranked = sorted(damaging, key=lambda n: -fs.play_strength(n, types))
    attacks, seen = [], set()
    stab = [n for n in ranked if fs.move(n).type in types]
    if stab:
        attacks.append(stab[0])
        seen.add(fs.move(stab[0]).type)
    for n in ranked:
        if len(attacks) == 3:
            break
        if fs.move(n).type not in seen:
            attacks.append(n)
            seen.add(fs.move(n).type)
    status = [n for n in can_names if fs.move(n).cat == "Status" and fs.move(n).effect in fs.POLICY_STATUS
              and tiers.get(n, 0) >= fs.TIERS["B"]]
    status.sort(key=lambda n: -tiers.get(n, 0))
    if status:
        return attacks + status[:1]
    rest = [n for n in ranked if n not in attacks]
    return attacks + rest[:1]


fs.player_moves = ian_moves
fs.BOX_MODE = True


# ---- fights ----------------------------------------------------------------------------------------------

def parse_fight(name):
    if name.startswith("tr:"):
        return ("tr", int(name[3:]))
    return ("story", name)


def fight_label(f):
    kind, key = f
    if kind == "story":
        return next(x["label"] for x in data.fights()["fights"] if x["key"] == key)
    return data.oxide_trainers()[key]["name"]


def with_genders(t, tr=None):
    """A copy of a trainer's party with each member's gender as the game
    builds it (fightsim.trainer_gender), from the trainer's file in
    res/trainers/data (or `tr`, a trainer file read from elsewhere): its
    class, and each member's own gender and ability fields. The balance
    track's trainer data does not carry them."""
    if tr is None:
        path = os.path.join(data.ROOT, "res", "trainers", "data", t["stem"] + ".json")
        with open(path) as fh:
            tr = json.load(fh)
    out = []
    for j, m in enumerate(t["party"]):
        fm = tr["party"][m.get("sub_index", j)]
        out.append(dict(m, gender=fs.trainer_gender(fm["species"], tr["class"], fm.get("gender"),
                                                    fm.get("ability") or 0)))
    return out


def prepare(f, given_side=None):
    """The fight's state for the search: {"st", "flags", "variants": [(boss
    keys, flags, starter or None)], "split", "label"}, or None when the
    fight is a double battle."""
    kind, key = f
    if kind == "story":
        fight = next(x for x in data.fights()["fights"] if x["key"] == key)
        if fight.get("tag"):
            from . import pdoubles
            split = fight["split"]
            st = pdoubles.prepare_story(fight, fs.fight_cap(split, key))
            flat = [k for g in st["bosses"] for k in g]
            return {"st": st, "variants": [(flat, st["group_flags"][0], None)], "split": split,
                    "label": fight["label"], "key": key, "doubles": "tag"}
        trainers = data.fight_trainers("oxide", fight)
        parties = [with_genders(t) for t in trainers]
        weather = calc.fight_weather([t["tr_id"] for t in trainers])
        split = fight["split"]
        cap = fs.fight_cap(split, key)
        st = fs.prepare(split, parties, weather,
                        fs.trick_room_for([t["constant"] for t in trainers], fight.get("trick_room")), cap=cap,
                        given_side=given_side)
        variants = []
        for v, t in enumerate(trainers):
            starter = slot_starter(t) if len(trainers) > 1 else None
            variants.append((st["bosses"][v], t["ai"], starter))
        st["first_battle"] = any(t["constant"] in fs.FIRST_BATTLE for t in trainers)
        return {"st": st, "variants": variants, "split": split, "label": fight["label"], "key": key}
    t = data.oxide_trainers()[key]
    split = SPLIT_OVERRIDE.get(key) or (required.placements()[key]["split"] if key in required.placements()
                                        else splits.trainer_split(key))
    if t.get("battle_type") == "Doubles" and len(t["party"]) > 1:
        from . import pdoubles
        st = pdoubles.prepare_trainer(t, split, fs.fight_cap(split))
        return {"st": st, "variants": [(st["bosses"][0], t["ai"], None)], "split": split,
                "label": t["name"], "key": f"tr{key}", "doubles": "doubles"}
    st = fs.prepare(split, [with_genders(t)], calc.fight_weather([key]), fs.trick_room_for([t["constant"]]),
                    cap=fs.fight_cap(split), given_side=given_side)
    return {"st": st, "variants": [(st["bosses"][0], t["ai"], None)], "split": split,
            "label": t["name"], "key": f"tr{key}"}


# ---- teams from boxes -------------------------------------------------------------------------------------

def box_keys(st, box, rng):
    """The state's keys for a box's species, one of each species' regular
    abilities drawn at random; a stage the side lacks falls back to its
    pre-evolution in the side, else is left out."""
    by_species = {}
    for k in st["player"]:
        by_species.setdefault(st["pokemon"][k]["constant"], k)
    pre = pool.pre_evolutions()
    keys = []
    for sp in box:
        k = by_species.get(sp)
        if k is None:
            k = next((by_species[p] for p in pre.get(sp, []) if p in by_species), None)
        if k is None:
            continue
        keys.append(rng.choice(st["variants"].get(k, [k])))
    return keys


def sixes(keys, n, rng, weights=None):
    """n distinct sixes from the box's keys (all of them when the box has
    six or fewer): random, or with `weights` the first is the six with the
    highest weights and the rest are drawn leaning on them, as a player
    planning for the fight picks."""
    if len(keys) <= 6:
        return [list(keys)]
    out, seen = [], set()
    if weights:
        best = sorted(keys, key=lambda k: (-weights.get(k, 0), rng.random()))[:6]
        seen.add(tuple(sorted(best)))
        out.append(sorted(best))
    tries = 0
    while len(out) < n and tries < n * 20:
        tries += 1
        if weights:
            pick = sorted(keys, key=lambda k: -rng.random() ** (1 / (1 + 2 * weights.get(k, 0))))[:6]
        else:
            pick = rng.sample(keys, 6)
        team = tuple(sorted(pick))
        if team not in seen:
            seen.add(team)
            out.append(list(team))
    return out


def variant_for(prep, box):
    """The boss variant this box meets: a rival or counterpart by the box's
    starter (its first member), else the first."""
    vs = prep["variants"]
    if len(vs) == 1:
        return vs[0]
    starter = SLOT_STARTER.get(STARTER_VARIANT.get(box[0]), box[0])
    return next((v for v in vs if v[2] == starter), vs[0])

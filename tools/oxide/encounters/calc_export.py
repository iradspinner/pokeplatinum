"""The damage calculator's game data, generated from `res/` (M8 D5).

    PYTHONPATH=. python3 -m tools.oxide.encounters.calc_export            # what it cannot model
    PYTHONPATH=. python3 -m tools.oxide.encounters.calc_export --json     # the data blob itself

The vendored calculator (`calc/`) takes one JSON blob per game, in Showdown's
naming: species under `poks`, moves under `moves`, and optionally a type chart.
The hosted version fetches that blob from npoint.io; ours is built here from the
same files the game is built from, and served by `server.py` at
`/api/calc-data`, so it cannot drift from the game and needs no network.

Three things the calculator would otherwise get wrong for this fork:

1. **The type chart.** Generation 4's chart with Fairy added, Steel keeping its
   resistances to Ghost and Dark. No stock setting matches it, so it travels in
   the blob as `type_chart`, read out of the battle code by `pokedex.type_chart`.
2. **Oxide's own numbers.** 181 species differ from canon in stats and three in
   type, and every move's type, category, power and priority comes from its
   `data.json`, so Charm is Fairy and Attack Order is a 120-power hit here.
3. **What it cannot model.** The calculator keys every effect off Showdown's
   names. An ability or move Showdown has never heard of loads with its
   numbers but no logic, and an Oxide move whose effect is still a placeholder
   script is modelled with the effect the game does not yet have. `report()`
   lists both, so neither passes silently.

Learnsets are not exported: the calculator offers every move to every species
and has no way to limit a set to what a species learns.
"""
import argparse
import functools
import json
import os
import re
import sys

from . import calc_trainers
from . import canon
from . import model
from . import pokedex

TITLE = "Platinum Oxide"
NAMES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "calc_names.json")

STAT_KEYS = {"hp": "hp", "attack": "at", "defense": "df",
             "special_attack": "sa", "special_defense": "sd", "speed": "sp"}
# Curse is the one move of the Mystery type, which Showdown calls "???".
TYPE_NAMES = {"MYSTERY": "???"}
GENDERS = {"NO_GENDER": "N", "MALE_ONLY": "M", "FEMALE_ONLY": "F"}
# The hit count of an effect Showdown may not know, for a move it does not.
MULTIHIT = {"MULTI_HIT": [2, 5], "HIT_TWICE": 2, "POISON_MULTI_HIT": 2,
            "HIT_TWICE_AND_FLINCH": 2, "HIT_THREE_TIMES": 3,
            "HIT_THREE_TIMES_FIXED_POWER": 3,
            "HIT_THREE_TIMES_INCREMENT_BASE_POWER_20": 3,
            "HIT_THREE_TIMES_ALWAYS_CRITICAL": 3}


def clean(name):
    """The calculator's own id for a name: lowercase letters and digits only."""
    return re.sub(r"[^a-z0-9]", "", str(name).lower())


@functools.lru_cache(maxsize=1)
def calc_names():
    """{"abilities": {id: name}, "moves": {id: (name, type, category)},
    "items": {id: name}} the calculator knows, dumped from it by
    make_calc_names.js."""
    with open(NAMES, encoding="utf-8") as f:
        raw = json.load(f)
    return {"abilities": {clean(n): n for n in raw["abilities"]},
            "moves": {clean(n): (n, t, c) for n, (t, c) in raw["moves"].items()},
            "items": {clean(n): n for n in raw.get("items") or []}}


def type_name(t):
    return TYPE_NAMES.get(t, t.title())


def ability_name(constant):
    """SAND_VEIL -> Sand Veil, spelled as the calculator spells it, or None."""
    return calc_names()["abilities"].get(clean(constant))


# Names the cleaned id cannot match. Platinum's own four are Generation 4
# spellings Showdown later changed; the rest are the donor's moves shortened
# to fit the game's name box, all Z-moves but Collision Course. Each was
# checked by hand against its type, class and description (OriginSupernova's
# says Mew, which makes it Genesis Supernova). A closest-name match was tried
# first and put 7-Star Strike on Shadow Strike, so the list is explicit.
ALIASES = {
    "ViceGrip": "Vise Grip", "Hi Jump Kick": "High Jump Kick",
    "Faint Attack": "Feint Attack", "SmellingSalt": "Smelling Salts",
    "ColisionCourse": "Collision Course",
    "All-Out Pummel": "All-Out Pummeling",
    "Super Skystrike": "Supersonic Skystrike",
    "Continent Crush": "Continental Crush",
    "EndlessNitemare": "Never-Ending Nightmare",
    "Inferno Drive": "Inferno Overdrive",
    "Ultimate Drake": "Devastating Drake",
    "Black Eclipse": "Black Hole Eclipse",
    "Sinister Raid": "Sinister Arrow Raid",
    "Moonsault": "Malicious Moonsault",
    "Alolan Guardian": "Guardian of Alola",
    "7-Star Strike": "Soul-Stealing 7-Star Strike",
    "Sparksurfer": "Stoked Sparksurfer",
    "Pulver-Pancake": "Pulverizing Pancake",
    "OriginSupernova": "Genesis Supernova",
    "10,000,000 Bolt": "10,000,000 Volt Thunderbolt",
    "LightBurnSky": "Light That Burns the Sky",
    "Sunraze Smash": "Searing Sunraze Smash",
    "Moonraze Storm": "Menacing Moonraze Maelstrom",
    "Let\u2019s Snuggle": "Let's Snuggle Forever",
    "Stormshards": "Splintered Stormshards",
    "Soulblaze": "Clangorous Soulblaze",
}


def move_name(rec):
    """A move's name as the calculator spells it, or None. Matched on the
    cleaned id, which absorbs most spelling differences (DragonBreath is
    Dragon Breath, Sand-Attack is Sand Attack), then on ALIASES."""
    known = calc_names()["moves"]
    hit = known.get(clean(ALIASES.get(rec["name"], rec["name"])))
    return hit[0] if hit else None


# The alternate forms the game has, picked by hand, since the calculator knows
# every form of every species and most of those are not in Oxide. Picked:
# the twelve forms with a record of their own, whose numbers are Oxide's
# (Rotom's appliances are Electric/Fire and so on here, and Deoxys-Attack has
# Magic Guard); Castform's and Cherrim's weather forms; and Arceus under each
# plate but Fairy, since the game has no Pixie Plate. Left out: the forms that
# only change a sprite (Burmy's cloaks, the East Sea Shellos and Gastrodon, the
# Unown letters), whose numbers are the base species'.
FORM_RECORDS = {
    ("SPECIES_DEOXYS", "attack"): "Deoxys-Attack",
    ("SPECIES_DEOXYS", "defense"): "Deoxys-Defense",
    ("SPECIES_DEOXYS", "speed"): "Deoxys-Speed",
    ("SPECIES_WORMADAM", "sandy"): "Wormadam-Sandy",
    ("SPECIES_WORMADAM", "trash"): "Wormadam-Trash",
    ("SPECIES_GIRATINA", "origin"): "Giratina-Origin",
    ("SPECIES_SHAYMIN", "sky"): "Shaymin-Sky",
    ("SPECIES_ROTOM", "heat"): "Rotom-Heat",
    ("SPECIES_ROTOM", "wash"): "Rotom-Wash",
    ("SPECIES_ROTOM", "frost"): "Rotom-Frost",
    ("SPECIES_ROTOM", "fan"): "Rotom-Fan",
    ("SPECIES_ROTOM", "mow"): "Rotom-Mow",
}
# Forms with no record: the base species' numbers with another type, which is
# all a weather form or a plate changes. None keeps the base's types.
TYPE_FORMS = {
    "Castform-Sunny": ("SPECIES_CASTFORM", ["FIRE"]),
    "Castform-Rainy": ("SPECIES_CASTFORM", ["WATER"]),
    "Castform-Snowy": ("SPECIES_CASTFORM", ["ICE"]),
    "Cherrim-Sunshine": ("SPECIES_CHERRIM", None),
}
TYPE_FORMS.update({f"Arceus-{t.title()}": ("SPECIES_ARCEUS", [t]) for t in (
    "BUG", "DARK", "DRAGON", "ELECTRIC", "FIGHTING", "FIRE", "FLYING", "GHOST",
    "GRASS", "GROUND", "ICE", "POISON", "PSYCHIC", "ROCK", "STEEL", "WATER")})


def form_folders():
    """{Showdown name: (species, form folder)} for every picked form, which is
    where its sprites are. A weather form's folder is named for the weather
    (Cherrim's Sunshine is `sunny`), a plate form's for its type."""
    out = {name: key for key, name in FORM_RECORDS.items()}
    for name, (sp, _) in TYPE_FORMS.items():
        suffix = name.split("-", 1)[1].lower()
        out[name] = (sp, "sunny" if suffix == "sunshine" else suffix)
    return out


def form_folders_inverse():
    """{(species, form folder): Showdown name}, the other way round."""
    return {v: k for k, v in form_folders().items()}


def form_record(root, species, form):
    """A form's record as `species_entry` reads it: the base species, with the
    stats, types and abilities of the form's own data.json. Weight stays the
    base's, because the game keeps weight per species, not per form."""
    base = pokedex.load(root, species)
    folder = pokedex.folder_of(species)
    with open(os.path.join(root, "res", "pokemon", folder, "forms", form, "data.json"),
              encoding="utf-8") as f:
        raw = json.load(f)
    rec = dict(base)
    stats = raw.get("base_stats") or {}
    rec["stats"] = {k: stats.get(k, 0) for k in pokedex.STAT_KEYS}
    rec["types"] = list(dict.fromkeys(t.replace("TYPE_", "") for t in raw.get("types") or []))
    abilities = [a.replace("ABILITY_", "") for a in raw.get("abilities") or []]
    ordinary = [a for a in abilities[:2] if a not in ("NONE", "")]
    rec["abilities"] = list(dict.fromkeys(ordinary))
    rec["hidden_ability"] = None
    return rec


def forms(root=None):
    """{Showdown name: record} for every form the picker offers."""
    root = root or model.repo_root()
    out = {name: form_record(root, sp, form) for (sp, form), name in FORM_RECORDS.items()}
    for name, (sp, types) in TYPE_FORMS.items():
        rec = dict(pokedex.load(root, sp))
        if types:
            rec["types"] = types
        out[name] = rec
    return out


def species_entry(rec):
    stats = {STAT_KEYS[k]: v for k, v in rec["stats"].items()}
    abilities = {}
    for slot, a in zip(("0", "1"), rec["abilities"]):
        abilities[slot] = ability_name(a) or a.replace("_", " ").title()
    if rec["hidden_ability"]:
        a = rec["hidden_ability"]
        abilities["H"] = ability_name(a) or a.replace("_", " ").title()
    out = {"bs": stats, "types": [type_name(t) for t in rec["types"]],
           "abilities": abilities}
    # Stored as tenths of a pound; Grass Knot and Low Kick read kilograms.
    if rec.get("weight_pounds"):
        out["weightkg"] = round(rec["weight_pounds"] * 0.45359237, 1)
    gender = GENDERS.get(rec.get("gender_ratio"))
    if gender:
        out["gender"] = gender
    return out


def move_entry(rec, known):
    """One move's numbers. For a move the calculator knows, its own logic for
    what the move does stays and only the numbers are Oxide's. A power of 1 is
    the game's marker for a power worked out in code (Grass Knot, Gyro Ball,
    SonicBoom), which the calculator also works out, so it is left alone."""
    out = {"type": type_name(rec["type"]),
           "category": rec["class"].title(),
           "priority": rec["priority"] or 0,
           "e_id": rec["effect_id"]}
    if rec["power"] and rec["power"] != 1:
        out["basePower"] = rec["power"]
    elif not known:
        out["basePower"] = 0
    if not known:
        # Nothing to inherit, so the few things the formula reads come from
        # the move itself.
        hits = MULTIHIT.get(rec["effect"])
        if hits:
            out["multihit"] = hits
        if "MAKES_CONTACT" in rec["flags"]:
            out["makesContact"] = True
        if rec["effect_chance"]:
            out["secondaries"] = True
    return out


def build(root=None):
    """The whole blob, as the calculator's loader reads it."""
    root = root or model.repo_root()
    poks = {}
    for species in pokedex.species_list(root):
        rec = pokedex.load(root, species)
        name = canon.showdown_name(species)
        if rec is None or not name:
            continue
        poks[name] = species_entry(rec)
    for name, rec in forms(root).items():
        poks[name] = species_entry(rec)
    moves = {}
    for rec in pokedex.moves(root).values():
        if rec["move"] == "MOVE_NONE" or rec["name"] in ("-", ""):
            continue
        known = move_name(rec)
        moves[known or rec["name"]] = move_entry(rec, bool(known))
    chart = pokedex.type_chart(root)
    types = sorted({a for a, _ in chart} | {d for _, d in chart})
    type_chart = {type_name(a): {type_name(d): chart.get((a, d), 1.0) for d in types}
                  for a in types}
    type_chart["???"] = {}
    return {
        "title": TITLE,
        "poks": poks,
        "moves": moves,
        "custom_moves": {},
        # Every trainer's party, rebuilt the way the game builds it in
        # battle (calc_trainers.py), so a gym leader can be picked by name.
        "formatted_sets": calc_trainers.all_sets(root),
        "order": {},
        "type_chart": type_chart,
        # What the species picker offers: Oxide's species and the forms above,
        # rather than every species the calculator knows (a patch reads it).
        "picker": sorted(poks),
        "oxide_report": report(root),
    }


def report(root=None):
    """What the calculator cannot model, by name, so none of it is silent."""
    root = root or model.repo_root()
    abilities = set()
    for species in pokedex.species_list(root):
        rec = pokedex.load(root, species) or {}
        for a in rec.get("abilities", []) + [rec.get("hidden_ability")]:
            if a and not ability_name(a):
                abilities.add(a)
    unknown_moves, stubbed = [], []
    for rec in pokedex.moves(root).values():
        if rec["move"] == "MOVE_NONE" or rec["name"] in ("-", ""):
            continue
        if not move_name(rec):
            unknown_moves.append(rec["name"])
        elif rec["stub"]:
            stubbed.append(rec["name"])
    return {
        # Oxide abilities the calculator has no logic for at all.
        "unknown_abilities": sorted(abilities),
        # Moves it has never heard of: their power, type and category count,
        # and nothing else they do.
        "unknown_moves": sorted(unknown_moves),
        # Moves it knows whose effect in Oxide is still a placeholder script:
        # the numbers include an effect the game does not have yet.
        "placeholder_effects": sorted(stubbed),
    }


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--json", action="store_true", help="print the data blob")
    a = ap.parse_args(argv)
    if a.json:
        json.dump(build(), sys.stdout, ensure_ascii=False)
        print()
        return 0
    r = report()
    for key, title in (("unknown_abilities", "Abilities the calculator has no logic for"),
                       ("unknown_moves", "Moves the calculator has never heard of"),
                       ("placeholder_effects",
                        "Moves it models with an effect Oxide's script does not have yet")):
        print(f"{title}: {len(r[key])}")
        for name in r[key]:
            print(f"  {name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

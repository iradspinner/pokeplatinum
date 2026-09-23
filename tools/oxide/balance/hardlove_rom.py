"""Hardlove Gold's trainers, read from the donor ROM itself.

    PYTHONPATH=. python3 -m tools.oxide.balance.hardlove_rom 35

The calculator's Hardlove file (hardlove.js) predates Hardlove 0.6.9's
Clair and League: it holds vanilla HeartGold's sets there, where the ROM has
Clair at 77 and the League at 82. So Hardlove is read from ~/roms/hardlove.nds,
the same donor ROM the port reads, and the calculator file is only a
cross-check for the fights both cover.

hg-engine keeps HeartGold's two trainer archives: a/0/5/5 holds one 20-byte
header per trainer (data flags, class, party size, items, AI flags, battle
type), and a/0/5/6 the party. Each party member is laid out by the header's
flags, and every Hardlove trainer uses the same 36-byte layout (flags 0x7F):

    u8  IV scale        u8  ability slot and gender
    u16 level           u16 species, form in the top five bits
    u16 held item       u16 moves x4
    u16 ability         u16 ball
    u8  IVs x6          u8  EVs x6
    u8  nature          u8  shiny lock
    u16 ball seal

Names come from the ROM's own text banks and are then spelled the way the
calculator spells them, so a Hardlove set and a Renegade set can be compared
and later fed to the same damage engine.
"""
import functools
import json
import os
import re
import struct
import sys

from .. import donor
from . import data

MSGENC = os.path.join(data.ROOT, "build", "tools", "msgenc", "msgenc")
CHARMAP = os.path.join(data.ROOT, "tools", "msgenc", "charmap.txt")
NARC_TRDATA, NARC_TRPOKE = "a/0/5/5", "a/0/5/6"
BANK_SPECIES, BANK_MOVES, BANK_ITEMS = 237, 750, 222
BANK_TRAINER_NAMES, BANK_TRAINER_CLASSES = 729, 730

FLAG_MOVES, FLAG_ITEM, FLAG_ABILITY, FLAG_BALL = 0x01, 0x02, 0x04, 0x08
FLAG_IV_EV, FLAG_NATURE, FLAG_SHINY_LOCK, FLAG_EXTRA = 0x10, 0x20, 0x40, 0x80
STATS = ("hp", "at", "df", "sp", "sa", "sd")   # HeartGold's stat order
NATURES = ["Hardy", "Lonely", "Brave", "Adamant", "Naughty", "Bold", "Docile",
           "Relaxed", "Impish", "Lax", "Timid", "Hasty", "Serious", "Jolly",
           "Naive", "Modest", "Mild", "Quiet", "Bashful", "Rash", "Calm",
           "Gentle", "Sassy", "Careful", "Quirky"]


# The ROM's species names are capped at ten characters; these are the ones
# Hardlove's trainers use, spelled out in full.
TRUNCATED = {
    "Baraskewda": "Barraskewda", "Basclegion": "Basculegion", "Blacefalon": "Blacephalon",
    "Centskorch": "Centiskorch", "Corviknite": "Corviknight", "Corvsquire": "Corvisquire",
    "Crabomnabl": "Crabominable", "Dudunspars": "Dudunsparce", "Flechinder": "Fletchinder",
    "Kilowatrel": "Kilowattrel", "Mewscarada": "Meowscarada", "Poltegeist": "Polteageist",
    "Stonjorner": "Stonjourner", "Walkngwake": "Walking Wake",
}
# Every alternate form a Hardlove trainer uses, as (species, form number) to
# the calculator's suffix. Each was checked against the form's own record in
# the ROM (its types, and its stats where forms share types) on 2026-09-22.
FORM_SUFFIX = {
    ("Raticate", 1): "Alola", ("Raichu", 1): "Alola", ("Sandslash", 1): "Alola",
    ("Ninetales", 1): "Alola", ("Geodude", 1): "Alola", ("Golem", 1): "Alola",
    ("Muk", 1): "Alola", ("Exeggutor", 1): "Alola", ("Marowak", 1): "Alola",
    ("Arcanine", 1): "Hisui", ("Electrode", 1): "Hisui", ("Typhlosion", 1): "Hisui",
    ("Qwilfish", 1): "Hisui", ("Sneasel", 1): "Hisui", ("Samurott", 1): "Hisui",
    ("Lilligant", 1): "Hisui", ("Zoroark", 1): "Hisui", ("Braviary", 1): "Hisui",
    ("Goodra", 1): "Hisui", ("Avalugg", 1): "Hisui", ("Decidueye", 1): "Hisui",
    ("Rapidash", 1): "Galar", ("Farfetch’d", 1): "Galar", ("Weezing", 1): "Galar",
    ("Mr. Mime", 1): "Galar", ("Zapdos", 1): "Galar", ("Slowking", 1): "Galar",
    ("Corsola", 1): "Galar", ("Darmanitan", 1): "Galar", ("Yamask", 1): "Galar",
    ("Deoxys", 2): "Defense", ("Wormadam", 2): "Trash",
    ("Rotom", 1): "Heat", ("Rotom", 2): "Wash", ("Rotom", 3): "Frost",
    ("Rotom", 4): "Fan", ("Rotom", 5): "Mow",
    ("Landorus", 1): "Therian", ("Enamorus", 1): "Therian", ("Greninja", 2): "Ash",
    ("Floette", 5): "Eternal", ("Gourgeist", 1): "Small", ("Lycanroc", 1): "Midnight",
    ("Lycanroc", 2): "Dusk", ("Indeedee", 1): "F", ("Urshifu", 1): "Rapid-Strike",
}
# Forms with no record of their own in the ROM share the base record's stats;
# only their types differ, and these are those types.
FORM_TYPES = {
    ("Rotom", 1): ["Electric", "Fire"], ("Rotom", 2): ["Electric", "Water"],
    ("Rotom", 3): ["Electric", "Ice"], ("Rotom", 4): ["Electric", "Flying"],
    ("Rotom", 5): ["Electric", "Grass"], ("Wormadam", 2): ["Bug", "Steel"],
    ("Deoxys", 2): ["Psychic"],
}
# hg-engine's type numbering: Platinum's, with Fairy in the old Mystery slot.
TYPES = ["Normal", "Fighting", "Flying", "Poison", "Ground", "Rock", "Bug", "Ghost",
         "Steel", "Fairy", "Fire", "Water", "Grass", "Electric", "Psychic", "Ice",
         "Dragon", "Dark"]
MEGA_SUFFIXES = ("", " X", " Y", " Z")


def _key(name):
    return re.sub(r"[^a-z0-9]", "", name.lower())


@functools.lru_cache(maxsize=None)
def _rom():
    return donor.Donor()


@functools.lru_cache(maxsize=None)
def _bank(index):
    return [m if isinstance(m, str) or m is None else " ".join(m)
            for m in _rom().text_bank(index, MSGENC, CHARMAP)]


@functools.lru_cache(maxsize=None)
def _calc_spelling():
    """Calculator spellings of every species, move and item name that the
    Hardlove calculator file knows, by a punctuation-free key."""
    raw = data.raw("hardlove")
    names = {}
    # The species table is keyed by id ("farfetchd") and carries the display
    # name ("Farfetch'd") inside; the move table is keyed by display name.
    for rec in raw.get("poks", {}).values():
        if rec.get("name"):
            names.setdefault(_key(rec["name"]), rec["name"])
    for name in list(raw["formatted_sets"]) + list(raw.get("moves", {})):
        names.setdefault(_key(name), name)
    for sets in raw["formatted_sets"].values():
        for s in sets.values():
            if s.get("item"):
                names.setdefault(_key(s["item"]), s["item"])
    return names


def _spell(name):
    if not name:
        return None
    name = TRUNCATED.get(name, name)
    return _calc_spelling().get(_key(name), name.title() if name.isupper() else name)


def _mega_form(species, item):
    """The Mega form a Pokemon becomes with the stone it holds, or None.
    A stone is an item named for its holder ("Dragoninite" on Dragonite,
    "Raichunite Y" on Raichu); the suffix letter carries over to the form."""
    if not item or not species:
        return None
    for suffix in MEGA_SUFFIXES:
        stem = item[:-len(suffix)] if suffix and item.endswith(suffix) else item
        if suffix and not item.endswith(suffix):
            continue
        if stem.endswith("ite") and stem != "Eviolite" and _key(stem)[:4] == _key(species)[:4]:
            return f"{species}-Mega" + (f"-{suffix.strip()}" if suffix else "")
    return None


def _stats_and_types(species_id, base_name, form):
    """Base stats and types from the ROM's own records, which Hardlove has
    rebalanced, so the calculator's copies are not used here."""
    rom = _rom()
    forms = [i for i, _reverts in rom.forms_of(species_id)]
    record = rom.personal(forms[form - 1] if 0 < form <= len(forms) else species_id)
    hp, at, df, sp, sa, sd = record["base_stats"]
    types = [TYPES[t] for t in dict.fromkeys(record["types"])]
    return ({"hp": hp, "at": at, "df": df, "sp": sp, "sa": sa, "sd": sd},
            FORM_TYPES.get((base_name, form), types))


def _trainer_name(index):
    return (_bank(BANK_TRAINER_NAMES)[index] or "").replace("{TRNAME}", "").strip()


def _mon(record, flags):
    """One party member, decoded by the header's flags."""
    iv_scale, _slot, level, species_word = struct.unpack_from("<BBHH", record, 0)
    pos = 6
    item = moves = ability = ivs = evs = nature = None
    if flags & FLAG_ITEM:
        (item,) = struct.unpack_from("<H", record, pos); pos += 2
    if flags & FLAG_MOVES:
        moves = struct.unpack_from("<4H", record, pos); pos += 8
    if flags & FLAG_ABILITY:
        (ability,) = struct.unpack_from("<H", record, pos); pos += 2
    if flags & FLAG_BALL:
        pos += 2
    if flags & FLAG_IV_EV:
        ivs = record[pos:pos + 6]; evs = record[pos + 6:pos + 12]; pos += 12
    if flags & FLAG_NATURE:
        nature = record[pos]; pos += 1
    species, form = species_word & 0x7FF, species_word >> 11
    abilities = _bank(donor.TEXT_ABILITY_NAMES)
    base = _spell(_bank(BANK_SPECIES)[species])
    if form and (base, form) not in FORM_SUFFIX:
        raise KeyError(f"form {form} of {base} is not in FORM_SUFFIX; check its record and add it")
    name = f"{base}-{FORM_SUFFIX[(base, form)]}" if form else base
    held = _spell(_bank(BANK_ITEMS)[item]) if item else None
    base_stats, types = _stats_and_types(species, base, form) if species else (None, None)
    return {
        "species": name,
        "species_id": species, "form": form,
        "base_stats": base_stats, "types": types,
        "mega": _mega_form(name, held),
        "level": level,
        "item": held,
        # Hardlove adds abilities past the 319 names in its bank (484 is the
        # highest a trainer uses), so an unnamed one keeps its number.
        "ability": (_spell(abilities[ability]) if ability < len(abilities)
                    else f"Ability {ability}") if ability else None,
        "nature": NATURES[nature] if nature is not None and nature < 25 else None,
        "ivs": dict(zip(STATS, ivs)) if ivs is not None else
               {s: iv_scale * 31 // 255 for s in STATS},
        "evs": dict(zip(STATS, evs)) if evs is not None else None,
        "moves": [_spell(_bank(BANK_MOVES)[m]) for m in (moves or ()) if m],
        "sub_index": None,
    }


@functools.lru_cache(maxsize=None)
def trainers():
    """Every Hardlove trainer with a party, keyed by trainer id."""
    rom = _rom()
    headers, parties = rom.narc(NARC_TRDATA), rom.narc(NARC_TRPOKE)
    classes = _bank(BANK_TRAINER_CLASSES)
    out = {}
    for tr_id, header in enumerate(headers):
        flags, cls, _pad, count = struct.unpack_from("<BBBB", header, 0)
        (ai,) = struct.unpack_from("<I", header, 12)
        (battle_type,) = struct.unpack_from("<I", header, 16)
        if count == 0:
            continue
        party = parties[tr_id]
        size = len(party) // count
        # Two trainers use the extended layout (flags 0xFF), and one of them,
        # Silver's first Route 29 fight, pads its three Pokemon with three
        # level 0 records; a record with no level or species is not a Pokemon.
        mons = [m for m in (_mon(party[k * size:(k + 1) * size], flags) for k in range(count))
                if m["level"] and m["species_id"]]
        for k, m in enumerate(mons):
            m["sub_index"] = k
        out[tr_id] = {
            "hack": "hardlove", "tr_id": tr_id, "name": f"{classes[cls]} {_trainer_name(tr_id)}",
            "class_id": cls, "location": None,
            "battle_type": "Doubles" if battle_type else "Singles",
            "ai": ai, "party": mons}
    return out


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    for tr_id in (int(a) for a in argv or ["35"]):
        t = trainers()[tr_id]
        print(f"{tr_id} {t['name']} ({t['battle_type']})")
        for m in t["party"]:
            print(f"    {m['species']:14} {m['level']:>3} {str(m['item']):16} {str(m['ability']):14} "
                  f"{str(m['nature']):8} {', '.join(m['moves'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

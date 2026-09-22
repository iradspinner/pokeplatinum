"""Every trainer's party as the damage calculator's opponent sets.

    PYTHONPATH=. python3 -m tools.oxide.encounters.calc_trainers leader_roark

Read from `res/trainers/data/`, the same files the build packs, and rebuilt the
way `TrainerData_BuildParty` in `src/trainer_data.c` builds a party in battle,
because the parts a calculator needs most are not stored anywhere:

- **Nature.** A trainer's Pokemon has no stored nature. The game seeds its
  LCRNG with the IV scale plus the level plus the species plus the trainer's
  id, steps it once per trainer-class id, and puts the last value above a low
  byte to make the personality; the nature is that personality mod 25. The low
  byte is 136 for a male trainer class and 120 for a female one, unless the
  party entry asks for a gender or an ability slot, which this fork's
  `TrainerMon_PersonalityLowByte` then satisfies.
- **Ability.** Personality bit 0 picks the second ability when the species has
  one. It is the base species' pair even for a form, because
  `Pokemon_InitWith` sets the ability before the form is set.
- **Gender.** The low byte against the species' gender ratio.
- **IVs.** The IV scale times 31 over 255, the same in every stat. No EVs.
- **Moves**, when a trainer lists none: the level-up learnset walked in order
  up to the Pokemon's level, filling empty slots, skipping a move already
  known, and pushing out the oldest once all four are full.

Whether a party carries moves and items is decided by its first member, as
the packer (`trainerproc.c`) decides it.
"""
import functools
import json
import os
import re
import sys

from . import calc_export
from . import canon
from . import model
from . import pokedex

NATURES = ["Hardy", "Lonely", "Brave", "Adamant", "Naughty", "Bold", "Docile",
           "Relaxed", "Impish", "Lax", "Timid", "Hasty", "Serious", "Jolly",
           "Naive", "Modest", "Mild", "Quiet", "Bashful", "Rash", "Calm",
           "Gentle", "Sassy", "Careful", "Quirky"]
GENDER_RATIOS = {"MALE_ONLY": 0, "FEMALE_12_5": 31, "FEMALE_25": 63,
                 "FEMALE_50": 127, "FEMALE_75": 191, "FEMALE_87_5": 223,
                 "FEMALE_ONLY": 254, "NO_GENDER": 255}
LCRNG_MULTIPLIER, LCRNG_INCREMENT = 1103515245, 24691
LOW_BYTE_MALE_CLASS, LOW_BYTE_FEMALE_CLASS = 136, 120
MAX_IV, MAX_IV_SCALE = 31, 255
# Form numbers of the species whose forms have records (include/constants/forms.h).
FORM_FOLDERS = {
    ("SPECIES_DEOXYS", 1): "attack", ("SPECIES_DEOXYS", 2): "defense",
    ("SPECIES_DEOXYS", 3): "speed",
    ("SPECIES_WORMADAM", 1): "sandy", ("SPECIES_WORMADAM", 2): "trash",
    ("SPECIES_GIRATINA", 1): "origin", ("SPECIES_SHAYMIN", 1): "sky",
    ("SPECIES_ROTOM", 1): "heat", ("SPECIES_ROTOM", 2): "wash",
    ("SPECIES_ROTOM", 3): "frost", ("SPECIES_ROTOM", 4): "fan",
    ("SPECIES_ROTOM", 5): "mow",
}


def _lines(root, rel):
    with open(os.path.join(root, rel), encoding="utf-8") as f:
        return [l.strip() for l in f if l.strip()]


@functools.lru_cache(maxsize=2)
def _tables(root):
    trainers = _lines(root, "generated/trainers.txt")
    classes = _lines(root, "generated/trainer_classes.txt")
    genders = {}
    with open(os.path.join(root, "include", "data", "trainer_class_genders.h"),
              encoding="utf-8") as f:
        for cls, gender in re.findall(r"\[(TRAINER_CLASS_\w+)\]\s*=\s*(GENDER_\w+)", f.read()):
            genders[cls] = gender
    with open(os.path.join(root, "res", "text", "trainer_class_names.json"),
              encoding="utf-8") as f:
        names = [m.get("en_US", "") for m in json.load(f)["messages"]]
    flags = [f for f in _lines(root, "generated/ai_flags.txt")
             if f not in ("AI_FLAG_NONE", "AI_FLAG_ALL")]
    return {"ids": {t: i for i, t in enumerate(trainers)},
            "class_ids": {c: i for i, c in enumerate(classes)},
            "class_genders": genders, "class_names": names,
            "ai_bits": {f: 1 << i for i, f in enumerate(flags)}}


def personality(trainer_id, class_id, female_class, species_id, level, iv_scale,
                gender_ratio, want_gender=None, want_slot=0):
    """The personality `TrainerData_BuildParty` gives one party member."""
    rnd = (iv_scale + level + species_id + trainer_id) & 0xFFFFFFFF
    state = rnd
    for _ in range(class_id):
        state = (state * LCRNG_MULTIPLIER + LCRNG_INCREMENT) & 0xFFFFFFFF
        rnd = state >> 16
    low = low_byte(gender_ratio, want_gender, want_slot,
                   LOW_BYTE_FEMALE_CLASS if female_class else LOW_BYTE_MALE_CLASS)
    return ((rnd << 8) + low) & 0xFFFFFFFF


def _gender_byte(ratio, gender, offset):
    """`sub_02074128`: a low byte that makes a species the gender asked."""
    if ratio in (0, 254, 255):
        return offset
    return (25 * (ratio // 25 + 1) + offset) if gender == "male" else offset


def gender_of(ratio, pid):
    if ratio == 0:
        return "M"
    if ratio == 254:
        return "F"
    if ratio == 255:
        return "N"
    return "F" if ratio > (pid & 0xFF) else "M"


def low_byte(ratio, want_gender, want_slot, default):
    """`TrainerMon_PersonalityLowByte`, this fork's: honour a requested gender
    and ability slot (1 or 2) together, since both live in this byte."""
    if want_gender is None:
        if not want_slot:
            return default
        return (default & ~1) | (1 if want_slot == 2 else 0)
    candidate = _gender_byte(ratio, want_gender, 0) & 0xFF
    if not want_slot:
        return candidate
    bit = 1 if want_slot == 2 else 0
    if (candidate & 1) == bit:
        return candidate
    nudged = _gender_byte(ratio, want_gender, 1) & 0xFF
    want = "M" if want_gender == "male" else "F"
    return nudged if gender_of(ratio, nudged) == want else candidate


def default_moves(learnset, level):
    """`BoxPokemon_SetDefaultMoves`, move for move."""
    slots = []
    for lv, move in learnset:
        if lv > level:
            break
        if move in slots:
            continue
        if len(slots) < 4:
            slots.append(move)
        else:
            slots = slots[1:] + [move]
    return slots


def _raw_species(root, species, form_folder=None):
    folder = pokedex.folder_of(species)
    rel = ["res", "pokemon", folder] + (["forms", form_folder] if form_folder else []) + ["data.json"]
    with open(os.path.join(root, *rel), encoding="utf-8") as f:
        return json.load(f)


def _item_name(item):
    if not item or item == "ITEM_NONE":
        return None
    return calc_export.calc_names()["items"].get(calc_export.clean(item.replace("ITEM_", "")))


def trainer_name(root, data, stem):
    """What the trainer is called in the calculator: its class as the game
    prints it, then its name. The game's Pokemon Trainer class uses two glyphs
    for PKMN, written out here."""
    t = _tables(root)
    cls = t["class_names"][t["class_ids"][data["class"]]]
    cls = cls.replace("₧₦", "Pkmn")
    return f"{cls} {data['name']}".strip()


def build_trainer(root, stem, data=None):
    """One trainer as a list of calculator sets, in party order, plus what
    the calculator's set list needs to find them."""
    t = _tables(root)
    if data is None:
        with open(os.path.join(root, "res", "trainers", "data", stem + ".json"),
                  encoding="utf-8") as f:
            data = json.load(f)
    trainer_id = t["ids"]["TRAINER_" + stem.upper()]
    class_id = t["class_ids"][data["class"]]
    female = t["class_genders"].get(data["class"]) == "GENDER_FEMALE"
    moves_table = pokedex.moves(root)
    party = data.get("party") or []
    has_moves = bool(party) and isinstance(party[0].get("moves"), list)
    has_items = bool(party) and isinstance(party[0].get("item"), str)
    species_ids = t.setdefault("species_ids", {n: i for i, n in enumerate(
        _lines(root, "generated/species.txt"))})
    sets = []
    for i, m in enumerate(party):
        species = m["species"]
        form = m.get("form") or 0
        base = _raw_species(root, species)
        ratio = GENDER_RATIOS[base["gender_ratio"].replace("GENDER_RATIO_", "")]
        pid = personality(trainer_id, class_id, female, species_ids[species],
                          m["level"], m["iv_scale"], ratio,
                          want_gender=m.get("gender"), want_slot=m.get("ability") or 0)
        # The ability pair is the base species', whatever the form.
        a1, a2 = (base["abilities"] + ["ABILITY_NONE"])[:2]
        ability = a2 if a2 != "ABILITY_NONE" and pid & 1 else a1
        form_folder = FORM_FOLDERS.get((species, form))
        if has_moves:
            move_ids = [mv for mv in (m.get("moves") or []) if mv and mv != "MOVE_NONE"]
        else:
            source = _raw_species(root, species, form_folder) if form_folder else base
            learnset = [tuple(e) for e in (source.get("learnset") or {}).get("by_level") or []]
            move_ids = default_moves(learnset, m["level"])
        names = []
        for mv in move_ids:
            rec = moves_table.get(mv)
            names.append((calc_export.move_name(rec) or rec["name"]) if rec else mv)
        iv = m["iv_scale"] * MAX_IV // MAX_IV_SCALE
        name = calc_export.form_folders_inverse().get((species, form_folder)) if form_folder else None
        showdown = name or canon.showdown_name(species)
        entry = {
            "level": m["level"],
            "ivs": {k: iv for k in ("hp", "at", "df", "sa", "sd", "sp")},
            "evs": {k: 0 for k in ("hp", "at", "df", "sa", "sd", "sp")},
            "nature": NATURES[pid % 25],
            "ability": calc_export.ability_name(ability.replace("ABILITY_", ""))
                       or ability.replace("ABILITY_", "").replace("_", " ").title(),
            "moves": names,
            "gender": gender_of(ratio, pid),
            "tr_id": trainer_id,
            "sub_index": i,
            "ai": sum(t["ai_bits"].get(f, 0) for f in data.get("ai_flags") or []),
            "personality": pid,
        }
        item = _item_name(m.get("item")) if has_items else None
        if item:
            entry["item"] = item
        if data.get("double_battle"):
            entry["doubles"] = True
        sets.append((showdown, entry))
    return sets


def _stamp(root):
    """The newest modification time among everything the sets are built
    from: the trainers, the species and the moves."""
    newest = 0
    for rel in (("res", "trainers", "data"),):
        base = os.path.join(root, *rel)
        for f in os.listdir(base):
            newest = max(newest, os.stat(os.path.join(base, f)).st_mtime_ns)
    base = os.path.join(root, "res", "pokemon")
    for folder in os.listdir(base):
        path = os.path.join(base, folder, "data.json")
        if os.path.isfile(path):
            newest = max(newest, os.stat(path).st_mtime_ns)
    return newest


def all_sets(root=None):
    """Cached against the files it reads, since building every party takes
    over a second and the calculator asks on every load."""
    root = root or model.repo_root()
    return _all_sets(root, _stamp(root), id(pokedex.moves(root)))


@functools.lru_cache(maxsize=2)
def _all_sets(root, stamp, moves_version):
    """{species: {set name: set}}, the calculator's `formatted_sets`, for
    every trainer with a party.

    A set name is "Lvl <lowest level in the party> <class> <name>", the shape
    the calculator parses a trainer out of (`getTrainerName` wants "Lvl N"
    and no bracket inside). A class and name used twice (rematches, the
    rival's battles) gets the rest of its file name to tell them apart:
    "Leader Roark Rematch", "Pkmn Trainer Barry Canalave City Chimchar"."""
    base = os.path.join(root, "res", "trainers", "data")
    stems = sorted(f[:-5] for f in os.listdir(base) if f.endswith(".json"))
    loaded = {}
    for stem in stems:
        with open(os.path.join(base, stem + ".json"), encoding="utf-8") as f:
            data = json.load(f)
        if data.get("party") and not stem.startswith("dummy"):
            loaded[stem] = data
    names = {stem: trainer_name(root, d, stem) for stem, d in loaded.items()}
    counts = {}
    for n in names.values():
        counts[n] = counts.get(n, 0) + 1
    out = {}
    for stem, data in loaded.items():
        label = names[stem]
        if counts[label] > 1:
            words = set(re.findall(r"[a-z0-9]+", label.lower()))
            rest = stem.split("_")
            while rest and rest[0] in words:
                rest = rest[1:]
            if rest:
                label = f"{label} {' '.join(w.title() for w in rest)}"
        label = f"Lvl {min(m['level'] for m in data['party'])} {label}"
        seen = {}
        for species, entry in build_trainer(root, stem, data):
            # A second of one species in a party would take the first's key;
            # the calculator's own convention for that is a Slot suffix.
            seen[species] = seen.get(species, 0) + 1
            key = label if seen[species] == 1 else f"{label} Slot{seen[species]}"
            out.setdefault(species, {})[key] = entry
    return out


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    root = model.repo_root()
    for stem in argv or ["leader_roark"]:
        with open(os.path.join(root, "res", "trainers", "data", stem + ".json"),
                  encoding="utf-8") as f:
            data = json.load(f)
        print(trainer_name(root, data, stem))
        for species, e in build_trainer(root, stem, data):
            print(f"  {species:14} Lv{e['level']:<3} {e['nature']:8} {e['ability']:14} "
                  f"{e['gender']} IV{e['ivs']['hp']:<2} {e.get('item', '-'):16} "
                  f"{', '.join(e['moves'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

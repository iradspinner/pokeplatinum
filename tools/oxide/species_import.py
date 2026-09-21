"""Build the 159 new species' res/pokemon directories.

Driven by three sources, each authoritative for different fields; the split and
the evidence for it are in docs/oxide/donor-tables.md.

  docs/oxide/species-id-map.csv   which species, what id, which donor record
  New Pokedex.xlsx                base stats, types, both abilities, hidden ability
  the donor ROM                   everything else, including all the graphics

Imported by import_donor.py; not a command in its own right.
"""

import csv
import json
import os
import re
import shutil
import struct
import subprocess

import openpyxl

import donor

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SHEET = "/mnt/g/PokeROMs/Rokemon RomHack Creation Hub/New Pokedex.xlsx"
NITROGFX = os.path.join(ROOT, "build", "tools", "nitrogfx", "nitrogfx")
MSGENC = os.path.join(ROOT, "build", "tools", "msgenc", "msgenc")
CHARMAP = os.path.join(ROOT, "tools", "msgenc", "charmap.txt")

# Donor text banks that carry per-species strings, found by decoding every bank
# and looking for one 1476 long whose first entry reads "Bulbasaur".
BANK_NAME = 237
BANK_NAME_UPPER = 817
BANK_CATEGORY = 816
BANK_WEIGHT = 812
BANK_HEIGHT = 814

# The sheet and the donor's name bank disagree on spacing and hyphens for a few
# abilities: the sheet's "Compound Eyes", "Soul Heart" and "Water Compaction"
# are the donor's "CompoundEyes", "Soul-Heart" and "WaterCompaction". Names are
# matched with spaces, hyphens and apostrophes stripped, which covers all three
# without an alias list.

# Pokedex presentation that neither source has for a new species. The donor's
# dex tables stop at HeartGold's own count, so these are defaults, not data: the
# shape affects only the Pokedex's search-by-shape, the scales and positions only
# the size-comparison screen. Listed in the tracker as a thing to come back to.
DEFAULT_BODY_SHAPE = "SHAPE_BIPEDAL_TAILED"
DEFAULT_DEX_PLACEMENT = {
    "trainer_scale_f": 256, "pokemon_scale_f": 337,
    "trainer_scale_m": 256, "pokemon_scale_m": 337,
    "trainer_pos_f": 8, "pokemon_pos_f": 22,
    "trainer_pos_m": 8, "pokemon_pos_m": 22,
}
PLACEHOLDER_DEX_ENTRY = [
    "No Pokédex data is\n",
    "available for this\n",
    "Pokémon yet.",
]

# Evolutions the pick-list overrides, keyed by the species whose record holds
# them. Only the ones where the donor is wrong or unusable are here; everything
# else comes across as the donor has it. Source: the evolution table in
# docs/oxide/species-pick-list.md, and Q4 of phase4-engine-change-answers.md for
# the two alt-evolutions. Natives are not in this file; they are their own pass.
EVOLUTION_OVERRIDES = {
    # Primeape's donor trigger counts Rage Fist uses, which Generation 4 cannot
    # express at all, so the pick-list replaces it with a plain level 50.
    "SPECIES_CHARCADET": [("EVO_USE_ITEM", "ITEM_SUN_STONE", "SPECIES_ARMAROUGE"),
                          ("EVO_USE_ITEM", "ITEM_DUSK_STONE", "SPECIES_CERULEDGE")],
    "SPECIES_PAWMO": [("EVO_USE_ITEM", "ITEM_THUNDERSTONE", "SPECIES_PAWMOT")],
    "SPECIES_SINISTEA": [("EVO_USE_ITEM", "ITEM_DUSK_STONE", "SPECIES_POLTEAGEIST")],
    "SPECIES_POLTEAGEIST": [("EVO_USE_ITEM", "ITEM_DUSK_STONE", "SPECIES_SINISTCHA")],
    "SPECIES_YAMASK": [("EVO_LEVEL", 34, "SPECIES_COFAGRIGUS"),
                       ("EVO_LEVEL_WITH_HELD_ITEM_DAY", "ITEM_REAPER_CLOTH", "SPECIES_RUNERIGUS"),
                       ("EVO_LEVEL_WITH_HELD_ITEM_NIGHT", "ITEM_REAPER_CLOTH", "SPECIES_RUNERIGUS")],
    "SPECIES_GOOMY": [("EVO_LEVEL", 40, "SPECIES_SLIGGOO"),
                      ("EVO_LEVEL_WITH_HELD_ITEM_DAY", "ITEM_METAL_COAT", "SPECIES_HISUIAN_SLIGGOO"),
                      ("EVO_LEVEL_WITH_HELD_ITEM_NIGHT", "ITEM_METAL_COAT", "SPECIES_HISUIAN_SLIGGOO")],
    # The donor points Hisuian Sliggoo at 2804, past the end of its own table.
    "SPECIES_HISUIAN_SLIGGOO": [("EVO_LEVEL", 50, "SPECIES_HISUIAN_GOODRA")],
    "SPECIES_SLIGGOO": [("EVO_LEVEL", 50, "SPECIES_GOODRA")],
    # The donor's second branch is Hisuian Decidueye, which is not in the
    # pick-list, so the personality split collapses to a plain level 36.
    "SPECIES_DARTRIX": [("EVO_LEVEL", 36, "SPECIES_DECIDUEYE")],
    "SPECIES_GALARIAN_MR_MIME": [("EVO_LEVEL", 42, "SPECIES_MR_RIME")],
    "SPECIES_ZYGARDE_10": [("EVO_LEVEL", 50, "SPECIES_ZYGARDE_50")],
}


# ------------------------------------------------------------------ sources
def load_map():
    with open(os.path.join(ROOT, "docs", "oxide", "species-id-map.csv")) as f:
        return list(csv.DictReader(f))


def load_sheet():
    wb = openpyxl.load_workbook(SHEET, data_only=True, read_only=True)
    ws = wb["New Pokedex"]
    out = {}
    for row in ws.iter_rows(min_row=2, values_only=True):
        if isinstance(row[0], int):
            out[row[0]] = row
    return out


def sheet_number(value):
    """The sheet annotates some stats, "110 (+1)". The number is the stat."""
    m = re.match(r"\s*(\d+)", str(value))
    return int(m.group(1)) if m else None


def enum_list(name):
    path = os.path.join(ROOT, "generated", name + ".txt")
    return [l.strip().split(" =")[0] for l in open(path) if l.strip()]


# --------------------------------------------------------------- conversion
class Converter:
    def __init__(self, d):
        self.d = d
        self.notes = []
        self.map = load_map()
        self.sheet = load_sheet()
        self.types = enum_list("pokemon_types")
        self.colors = enum_list("pokemon_colors")
        self.egg_groups = enum_list("egg_groups")
        self.exp_rates = enum_list("exp_rates")
        self.moves = enum_list("moves")
        self.max_move = self.moves.index("MAX_MOVES") - 1
        self.evo_methods = enum_list("evolution_methods")
        self.items = enum_list("items")
        self.gender_ratios = {}
        for line in open(os.path.join(ROOT, "generated", "gender_ratios.txt")):
            if "=" in line:
                k, v = line.split("=")
                self.gender_ratios[int(v)] = k.strip()
        abilities = enum_list("abilities")
        names = d.text_bank(donor.TEXT_ABILITY_NAMES, MSGENC, CHARMAP)
        self.ability_by_name = {}
        for i, n in enumerate(names):
            self.ability_by_name.setdefault(self._normalize(n), i)
        self.abilities = abilities
        self.hidden = d.hidden_abilities()
        self.base_exp = d.base_exp()
        self.icon_pal = d.icon_palettes()
        self.names = d.text_bank(BANK_NAME, MSGENC, CHARMAP)
        self.upper = d.text_bank(BANK_NAME_UPPER, MSGENC, CHARMAP)
        self.categories = d.text_bank(BANK_CATEGORY, MSGENC, CHARMAP)
        self.weights = d.text_bank(BANK_WEIGHT, MSGENC, CHARMAP)
        self.heights = d.text_bank(BANK_HEIGHT, MSGENC, CHARMAP)
        # donor species id -> Oxide constant, for evolution targets
        self.target = {int(r["donor_index"]): r["constant"] for r in self.map}
        species = enum_list("species")
        for sid in range(1, 494):
            self.target[sid] = species[sid]

    @staticmethod
    def _normalize(s):
        s = str(s).strip().lower()
        return s.replace(" ", "").replace("-", "").replace("'", "").replace("’", "")

    def ability(self, value):
        if value is None or str(value).strip() in ("", "-", "None"):
            return "ABILITY_NONE"
        i = self.ability_by_name.get(self._normalize(value))
        if i is None:
            raise SystemExit("sheet ability %r is not in the donor's name bank" % value)
        return self.abilities[i]

    def gender_ratio(self, value, name):
        """Five donor records hold 190 where the enum has 191 (75% female): the
        Minccino and Gothita lines. Snap to the nearest named value and say so,
        rather than inventing an enum member for an off-by-one."""
        if value in self.gender_ratios:
            return self.gender_ratios[value]
        nearest = min(self.gender_ratios, key=lambda k: abs(k - value))
        self.notes.append("%s: gender ratio %d is not a named value, using %s (%d)"
                          % (name, value, self.gender_ratios[nearest], nearest))
        return self.gender_ratios[nearest]

    def type_name(self, sheet_value):
        return "TYPE_" + str(sheet_value).strip().upper()

    def learnset(self, donor_index):
        """Donor level-up moves, dropped to the ones Platinum has. Level 0 is
        hg-engine's evolution-move marker and becomes 1, the earliest Platinum
        can express."""
        out = []
        for level, move in self.d.learnset(donor_index):
            if move <= self.max_move:
                out.append([max(level, 1), self.moves[move]])
        return out

    # What the second element of an evolution entry means, which speciesproc
    # type-checks per method: nothing at all for some, a plain number for the
    # level ones, and an identifier out of a particular enum for the rest.
    EVO_PARAM_NONE = {
        "EVO_NONE", "EVO_LEVEL_HAPPINESS", "EVO_LEVEL_HAPPINESS_DAY",
        "EVO_LEVEL_HAPPINESS_NIGHT", "EVO_TRADE", "EVO_LEVEL_MAGNETIC_FIELD",
        "EVO_LEVEL_MOSS_ROCK", "EVO_LEVEL_ICE_ROCK",
    }
    EVO_PARAM_ITEM = {
        "EVO_TRADE_WITH_HELD_ITEM", "EVO_USE_ITEM", "EVO_USE_ITEM_MALE",
        "EVO_USE_ITEM_FEMALE", "EVO_LEVEL_WITH_HELD_ITEM_DAY",
        "EVO_LEVEL_WITH_HELD_ITEM_NIGHT",
    }
    EVO_PARAM_MOVE = {"EVO_LEVEL_KNOW_MOVE"}
    EVO_PARAM_SPECIES = {"EVO_LEVEL_SPECIES_IN_PARTY"}

    def evolutions(self, constant, donor_index):
        if constant in EVOLUTION_OVERRIDES:
            return [[m, p, t] if p is not None else [m, t]
                    for m, p, t in EVOLUTION_OVERRIDES[constant]]
        out = []
        for method, param, target in self.d.evolutions(donor_index):
            if method >= len(self.evo_methods) or target not in self.target:
                # a method Platinum does not have, or a target past the end of
                # the donor's own table; both are listed in donor-tables.md
                continue
            name = self.evo_methods[method]
            species = self.target[target]
            if name in self.EVO_PARAM_NONE:
                out.append([name, species])
            elif name in self.EVO_PARAM_ITEM:
                out.append([name, self.items[param], species])
            elif name in self.EVO_PARAM_MOVE:
                if param > self.max_move:
                    self.notes.append("%s: evolution by knowing move %d, which "
                                      "Platinum does not have; dropped" % (constant, param))
                    continue
                out.append([name, self.moves[param], species])
            elif name in self.EVO_PARAM_SPECIES:
                out.append([name, self.target[param], species])
            else:
                out.append([name, param, species])
        return out

    # ----------------------------------------------------------- data.json
    def data_json(self, row):
        """The res/pokemon/<species>/data.json for one new species."""
        sheet = self.sheet[int(row["dex_pos"])]
        dp = int(row["donor_index"])
        rec = self.d.personal(dp)
        st = [sheet_number(sheet[i]) for i in range(2, 8)]  # HP ATK DEF SPA SpDef SPE
        abilities = [self.ability(sheet[12]), self.ability(sheet[13]), self.ability(sheet[14])]
        # The twelve form records carry "???" here; they take the base species'.
        measure = FORM_BASE_SPECIES.get(row["constant"], dp)
        feet, inches = re.search(r"(\d+)\D+(\d+)", self.heights[measure]).groups()
        weight = float(re.search(r"([\d.]+)", self.weights[measure]).group(1))
        category = str(self.categories[dp])
        name = str(self.upper[dp])
        dex_lang = {
            "name": name,
            "category": category,
            "entry_text": list(PLACEHOLDER_DEX_ENTRY),
        }
        return {
            "base_stats": {
                "hp": st[0], "attack": st[1], "defense": st[2],
                "speed": st[5], "special_attack": st[3], "special_defense": st[4],
            },
            "types": [self.type_name(sheet[9]), self.type_name(sheet[10])],
            "catch_rate": rec["catch_rate"],
            "base_exp_reward": self.base_exp[dp],
            # Battling grants no EVs in Oxide and the donor zeroes these anyway.
            "ev_yields": {k: 0 for k in
                          ("hp", "attack", "defense", "speed",
                           "special_attack", "special_defense")},
            "held_items": {"common": "ITEM_NONE", "rare": "ITEM_NONE"},
            "gender_ratio": self.gender_ratio(rec["gender_ratio"], row["name"]),
            "hatch_cycles": rec["hatch_cycles"],
            "base_friendship": rec["base_friendship"],
            "exp_rate": self.exp_rates[rec["exp_rate"]],
            "egg_groups": [self.egg_groups[rec["egg_groups"][0]],
                           self.egg_groups[rec["egg_groups"][1]]],
            "abilities": abilities,
            "safari_flee_rate": rec["safari_flee_rate"],
            "body_color": self.colors[rec["body_color"]],
            "flip_sprite": rec["flip_sprite"],
            "icon_palette": self.icon_pal[dp],
            "learnset": {
                "by_level": self.learnset(dp),
                # Hardlove keeps TM compatibility somewhere this project has not
                # found, and the TM list itself is being redone in Phase 5, so
                # filling these in now would be work thrown away. Tracked there.
                "by_tm": [],
                "by_tutor": [],
                "egg_moves": [],
            },
            "evolutions": self.evolutions(row["constant"], dp),
            "offspring": row["constant"],  # fixed up once every species is read
            "footprint": {
                "has": False,
                "size": "FOOTPRINT_MEDIUM",
                "type": "FOOTPRINT_TYPE_NONE",
            },
            "pokedex_data": dict({
                "height_inches": int(feet) * 12 + int(inches),
                "weight_pounds": weight,
                "body_shape": DEFAULT_BODY_SHAPE,
            }, **DEFAULT_DEX_PLACEMENT, **{
                lang: dict(dex_lang) for lang in ("en", "fr", "de", "it", "es", "jp")
            }),
            "catching_show": {
                # Pal Park transfers a Generation 3 cartridge, so nothing new can
                # arrive that way and every new species is out of the Catching Show.
                "pal_park_land_area": "PAL_PARK_AREA_LAND_NONE",
                "pal_park_water_area": "PAL_PARK_AREA_WATER_NONE",
                "catching_points": 0,
                "rarity": 0,
                "unused": 0,
            },
        }


# --------------------------------------------------------------------- cries
# The donor keeps one wave archive per species, named WAVE_ARC_PV<species>, each
# holding a single IMA-ADPCM sample. Platinum's build wants a mono PCM16 wav at
# the sample rate the donor already uses, so this is a straight decode.
_IMA_INDEX = [-1, -1, -1, -1, 2, 4, 6, 8, -1, -1, -1, -1, 2, 4, 6, 8]
_IMA_STEP = [
    7, 8, 9, 10, 11, 12, 13, 14, 16, 17, 19, 21, 23, 25, 28, 31, 34, 37, 41, 45,
    50, 55, 60, 66, 73, 80, 88, 97, 107, 118, 130, 143, 157, 173, 190, 209, 230,
    253, 279, 307, 337, 371, 408, 449, 494, 544, 598, 658, 724, 796, 876, 963,
    1060, 1166, 1282, 1411, 1552, 1707, 1878, 2066, 2272, 2499, 2749, 3024,
    3327, 3660, 4026, 4428, 4871, 5358, 5894, 6484, 7132, 7845, 8630, 9493,
    10442, 11487, 12635, 13899, 15289, 16818, 18500, 20350, 22385, 24623, 27086,
    29794, 32767,
]


def decode_adpcm(data):
    """NDS IMA-ADPCM to signed 16-bit samples. The first four bytes are the
    starting predictor and step index; the rest is one sample per nibble, low
    nibble first."""
    predictor, index = struct.unpack("<hh", data[:4])
    out = bytearray()
    for byte in data[4:]:
        for nibble in (byte & 0x0F, byte >> 4):
            step = _IMA_STEP[index]
            diff = step >> 3
            if nibble & 1:
                diff += step >> 2
            if nibble & 2:
                diff += step >> 1
            if nibble & 4:
                diff += step
            predictor = predictor - diff if nibble & 8 else predictor + diff
            predictor = max(-32768, min(32767, predictor))
            index = max(0, min(88, index + _IMA_INDEX[nibble]))
            out += struct.pack("<h", predictor)
    return bytes(out)


def write_wav(path, samples, sample_rate):
    header = b"RIFF" + struct.pack("<I", 36 + len(samples)) + b"WAVEfmt "
    header += struct.pack("<IHHIIHH", 16, 1, 1, sample_rate, sample_rate * 2, 2, 16)
    header += b"data" + struct.pack("<I", len(samples))
    with open(path, "wb") as f:
        f.write(header + samples)


# CRLF, which is what every existing cry.txt in the repo has.
CRY_BANK_LINE = "0, Single, 0, 0, 60, 127, 127, 127, 127, 64\r\n"

# The twelve form and alt-evolution records the donor keeps as separate species
# are incomplete in two ways: nine have no wave archive of their own, and all
# twelve have "???" where their height and weight should be. Each borrows both
# from the species it is a form of, which is what the games do for a cry anyway.
# Values are donor species ids.
FORM_BASE_SPECIES = {
    "SPECIES_ALOLAN_NINETALES": 38,
    "SPECIES_GYARADOS_M": 130,
    "SPECIES_LOPUNNY_M": 428,
    "SPECIES_GALARIAN_RAPIDASH": 78,
    "SPECIES_GALARIAN_WEEZING": 110,
    "SPECIES_GALARIAN_MR_MIME": 122,
    "SPECIES_GALARIAN_ARTICUNO": 144,
    "SPECIES_GALARIAN_ZAPDOS": 145,
    "SPECIES_GALARIAN_MOLTRES": 146,
    "SPECIES_HISUIAN_SLIGGOO": 755,
    "SPECIES_HISUIAN_GOODRA": 756,
    "SPECIES_ZYGARDE_10": 768,
}

MESON_TEMPLATE = """species_data_files += files('data.json', 'sprite_data.json')

poke_icon_files += files('icon.png')

{pokegra}
pokefoot_files += files('footprint.png')
"""


def dirname_of(constant):
    return constant[len("SPECIES_"):].lower()


class Writer:
    def __init__(self, conv, dry_run, log):
        self.c = conv
        self.dry_run = dry_run
        self.log = log
        self.pokegra = conv.d.narc(donor.NARC_POKEGRA)
        self.icons = conv.d.narc(donor.NARC_ICONS)
        self.offsets = conv.d.narc(donor.NARC_SPRITE_OFFSETS)
        self.cries = self._cry_index()
        # The icon palette lives in the repo as a JASC .pal; nitrogfx needs it
        # as an NCLR to decode against, so build that once.
        self.icon_palette_nclr = os.path.join(ROOT, "build", "oxide_icon_shared.NCLR")
        if not dry_run:
            os.makedirs(os.path.dirname(self.icon_palette_nclr), exist_ok=True)
            subprocess.run([NITROGFX,
                            os.path.join(ROOT, "res", "pokemon", ".shared", "pl_poke_icon.pal"),
                            self.icon_palette_nclr, "-bitdepth", "4"], check=True)

    def _cry_index(self):
        import ndspy.soundArchive
        sdat = ndspy.soundArchive.SDAT(
            self.c.d.rom.files[self.c.d.names[donor.SDAT]])
        index = {}
        for i, entry in enumerate(sdat.waveArchives):
            name = entry[0] if isinstance(entry, tuple) else None
            if name and re.fullmatch(r"WAVE_ARC_PV\d+", name):
                index[int(name[len("WAVE_ARC_PV"):])] = entry[1]
        return index

    # The donor lays pl_pokegra out exactly as Platinum does: six members per
    # species, back-female, back-male, front-female, front-male, then the normal
    # and shiny palettes.
    def sprite(self, donor_index, slot):
        return self.pokegra[donor_index * 6 + slot]

    def write(self, row):
        out = os.path.join(ROOT, "res", "pokemon", dirname_of(row["constant"]))
        dp = int(row["donor_index"])
        data = self.c.data_json(row)
        if self.dry_run:
            self.log.append("would write %s" % os.path.relpath(out, ROOT))
            return data
        os.makedirs(out, exist_ok=True)

        # palettes first, because decoding a sprite needs one
        pal_paths = {}
        for slot, name in ((4, "normal"), (5, "shiny")):
            nclr = os.path.join(out, name + ".NCLR")
            with open(nclr, "wb") as f:
                f.write(self.sprite(dp, slot))
            subprocess.run([NITROGFX, nclr, os.path.join(out, name + ".pal")], check=True)
            pal_paths[name] = nclr

        ratio = data["gender_ratio"]
        wants = []
        if ratio != "GENDER_RATIO_FEMALE_ONLY":
            wants += [(1, "male_back"), (3, "male_front")]
        if ratio not in ("GENDER_RATIO_MALE_ONLY", "GENDER_RATIO_NO_GENDER"):
            wants += [(0, "female_back"), (2, "female_front")]
        for slot, name in wants:
            ncgr = os.path.join(out, name + ".NCGR")
            with open(ncgr, "wb") as f:
                f.write(self.sprite(dp, slot))
            subprocess.run([NITROGFX, ncgr, os.path.join(out, name + ".png"),
                            "-encodefronttoback", "-palette", pal_paths["normal"]], check=True)
            os.remove(ncgr)
        for p in pal_paths.values():
            os.remove(p)

        # Icon: the archive is seven shared members and then one per species.
        # Icons share one 256-colour palette split into sub-palettes, which is
        # what data.json's icon_palette selects, and nitrogfx counts those from
        # one. Four tiles wide gives Platinum's 32x64, two animation frames.
        icon_ncgr = os.path.join(out, "icon.NCGR")
        with open(icon_ncgr, "wb") as f:
            f.write(self.icons[7 + dp])
        subprocess.run([NITROGFX, icon_ncgr, os.path.join(out, "icon.png"),
                        "-palette", self.icon_palette_nclr,
                        "-palindex", str(data["icon_palette"] + 1),
                        "-width", "4"], check=True)
        os.remove(icon_ncgr)

        # footprint: the donor's are not where this project has found them, so
        # every new species carries a blank one and says so with "has": false.
        shutil.copy(os.path.join(ROOT, "res", "pokemon", "barboach", "footprint.png"),
                    os.path.join(out, "footprint.png"))

        # cry
        wave = self.cries.get(dp) or self.cries[FORM_BASE_SPECIES[row["constant"]]]
        sample = wave.waves[0]
        write_wav(os.path.join(out, "cry.wav"),
                  decode_adpcm(sample.data), sample.sampleRate)
        with open(os.path.join(out, "cry.txt"), "w", newline="") as f:
            f.write(CRY_BANK_LINE)

        # sprite_data.json: the y offsets are the donor's, four bytes per species
        # in the same order as the sprites. Everything else is a plain default;
        # the animation ids and shadow only affect how the sprite bobs.
        # A species with only one gender has an empty member where the other
        # gender's offset would be, exactly as Platinum does; fall back to the
        # gender it does have so sprite_data.json always has both keys.
        raw = [self.offsets[dp * 4 + i] for i in range(4)]
        y = [(m[0] if m else 0) for m in raw]
        if not raw[0]:
            y[0] = y[1]
        if not raw[1]:
            y[1] = y[0]
        if not raw[2]:
            y[2] = y[3]
        if not raw[3]:
            y[3] = y[2]
        with open(os.path.join(out, "sprite_data.json"), "w") as f:
            json.dump(sprite_data(y), f, indent=4)
            f.write("\n")

        lines = []
        for slot, name in sorted(wants):
            lines.append("pokegra_files += files('%s.png')" % name)
        with open(os.path.join(out, "meson.build"), "w") as f:
            f.write(MESON_TEMPLATE.format(pokegra="\n".join(lines) + "\n"))

        with open(os.path.join(out, "data.json"), "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
            f.write("\n")
        self.log.append("wrote %s" % os.path.relpath(out, ROOT))
        return data


def sprite_data(y_offsets):
    """y_offsets is [back_female, back_male, front_female, front_male]."""
    def frames(first, second):
        out = [{"sprite_frame": 0, "frame_delay": first, "x_shift": 0, "y_shift": 0},
               {"sprite_frame": 1, "frame_delay": second, "x_shift": 0, "y_shift": 0}]
        out += [{"sprite_frame": -1, "frame_delay": 0, "x_shift": 0, "y_shift": 0}
                for _ in range(8)]
        return out
    return {
        "front": {
            "y_offset": {"female": y_offsets[2], "male": y_offsets[3]},
            "addl_y_offset": 0,
            "animation": 7,
            "cry_delay": 13,
            "start_delay": 10,
            "frames": frames(10, 6),
        },
        "back": {
            "y_offset": {"female": y_offsets[0], "male": y_offsets[1]},
            "animation": 5,
            "cry_delay": 9,
            "start_delay": 11,
            "frames": frames(11, 15),
        },
        "shadow": {"x_offset": 0, "size": "SHADOW_SIZE_MEDIUM"},
    }


def fix_offspring(written, natives):
    """Platinum's `offspring` names what an egg from this species hatches into,
    so every member of a family points at its root. Walk the evolutions that
    were just written, plus the handful of new species that hang off a native,
    and carry the root down each chain."""
    source_of = {}
    for constant, data in written.items():
        for entry in data["evolutions"]:
            source_of[entry[-1]] = constant  # the target is always last
    for constant, native in natives.items():
        source_of[constant] = native

    def root(constant, seen=()):
        parent = source_of.get(constant)
        if parent is None or parent in seen:
            return constant
        if parent not in written:
            return parent  # a native: its own record already names the right root
        return root(parent, seen + (constant,))

    for constant, data in written.items():
        data["offspring"] = root(constant)


def insert_species_constants(constants, dry_run, log):
    """New species go into generated/species.txt immediately after
    SPECIES_ARCEUS, which pushes SPECIES_EGG and SPECIES_BAD_EGG up behind them
    and carries every count derived from the enum with it."""
    path = os.path.join(ROOT, "generated", "species.txt")
    lines = [l.rstrip("\n") for l in open(path)]
    if constants[0] in lines:
        log.append("generated/species.txt: already has them")
        return False
    at = lines.index("SPECIES_EGG")
    lines[at:at] = constants
    log.append("generated/species.txt: +%d constants before SPECIES_EGG" % len(constants))
    if not dry_run:
        with open(path, "w") as f:
            f.write("\n".join(lines) + "\n")
    return True

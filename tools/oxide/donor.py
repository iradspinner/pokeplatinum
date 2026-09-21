"""Read Hardlove Gold's data tables.

Hardlove is an hg-engine build, so its tables are hg-engine's layout rather than
vanilla HeartGold's. Three things moved out of the 44-byte species record and
into NARC a/0/2/8, which hg-engine uses as a scratch archive for data it added:
base experience, hidden abilities and icon palettes. This module knows where
each of those lives and hands them back as plain Python.

Nothing here writes to the repo. `import_donor.py` is the tool that does that;
this is the reader it sits on.

The donor ROM is pinned at ~/roms/hardlove.nds (a copy; the original lives in
the project folder on the G: drive and is never touched).
"""

import os
import struct
import subprocess
import json
import tempfile

import ndspy.rom
import ndspy.narc

DEFAULT_ROM = os.path.expanduser("~/roms/hardlove.nds")

# Where things live in the donor. Paths are the ROM's own, not DSPRE's names.
NARC_PERSONAL = "a/0/0/2"    # 1476 species records, 44 bytes each
NARC_LEARNSETS = "a/0/3/3"   # one blob, 34 fixed slots per species
NARC_EVOLUTIONS = "a/0/3/4"  # 1476 records, 9 slots of 6 bytes plus 2 padding
NARC_ADDON = "a/0/2/8"       # hg-engine's added data, members 7..13 below
NARC_TEXT = "a/0/2/7"        # 854 text banks

# Members of a/0/2/8. Identified by reading them, not from hg-engine's source;
# see docs/oxide/donor-tables.md for the evidence behind each one.
ADDON_HIDDEN_ABILITIES = 7   # u16 per species
ADDON_BASE_EXP = 8           # u16 per species
ADDON_ICON_PALETTES = 9      # u8 per species
ADDON_UNIDENTIFIED = 10      # u16 per species, only 26 non-zero; see the doc
ADDON_FORM_DATA = 11         # 32 u16 per species, the personal indices of its forms
ADDON_FORM_TO_SPECIES = 12   # u16 per form record, the species it belongs to
ADDON_FORM_REVERSION = 13    # u16 per form record, small values, see the doc

# Text banks. Ability ids line up with Platinum's for 0..123.
TEXT_ABILITY_NAMES = 720
TEXT_ABILITY_NAMES_UPPER = 721
TEXT_ABILITY_DESCRIPTIONS = 722

NUM_DONOR_SPECIES = 1476     # includes the 400 form records at 1076..1475
FIRST_FORM_RECORD = 1076
LEARNSET_SLOTS = 34          # fixed-width, unused slots are (0xFFFF, 0)
EVOLUTION_SLOTS = 9

# Hardlove types are Platinum's numbering with one exception: hg-engine gave
# Fairy the dead TYPE_MYSTERY slot, 9. Oxide put Fairy on the end at 18, so
# every type read out of the donor goes through this.
DONOR_TYPE_FAIRY = 9


class Donor:
    def __init__(self, path=DEFAULT_ROM):
        self.rom = ndspy.rom.NintendoDSRom.fromFile(path)
        self.names = _walk(self.rom.filenames)
        self._cache = {}

    def narc(self, path):
        if path not in self._cache:
            self._cache[path] = ndspy.narc.NARC(self.rom.files[self.names[path]]).files
        return self._cache[path]

    # -------------------------------------------------------------- species
    def personal(self, index):
        """One species record, decoded. hg-engine widened both abilities to u16
        and emptied base exp and the TM masks, so this is not Platinum's layout
        even though it is still 44 bytes."""
        b = self.narc(NARC_PERSONAL)[index]
        return {
            "base_stats": struct.unpack("<6B", b[0:6]),   # hp atk def spe spa spd
            "types": (b[6], b[7]),
            "catch_rate": b[8],
            # b[9] is base exp in vanilla; hg-engine zeroes it except on the
            # form records and keeps the real table in a/0/2/8 member 8.
            "ev_yields": struct.unpack("<H", b[10:12])[0],
            "held_items": struct.unpack("<2H", b[12:16]),
            "gender_ratio": b[16],
            "hatch_cycles": b[17],
            "base_friendship": b[18],
            "exp_rate": b[19],
            "egg_groups": (b[20], b[21]),
            "abilities": (struct.unpack("<H", b[22:24])[0],
                          struct.unpack("<H", b[26:28])[0]),
            "safari_flee_rate": b[24],
            "body_color": b[25] & 0x7F,
            "flip_sprite": bool(b[25] >> 7),
        }

    def _addon_u16(self, member):
        b = self.narc(NARC_ADDON)[member]
        return struct.unpack("<%dH" % (len(b) // 2), b)

    def hidden_abilities(self):
        return self._addon_u16(ADDON_HIDDEN_ABILITIES)

    def base_exp(self):
        return self._addon_u16(ADDON_BASE_EXP)

    def icon_palettes(self):
        return self.narc(NARC_ADDON)[ADDON_ICON_PALETTES]

    def forms_of(self, species):
        """The personal indices of one species' alternate forms. The high bit
        marks a form that reverts after battle (mega, gigantamax); Oxide has
        none of those, so callers generally want the unflagged ones."""
        b = self.narc(NARC_ADDON)[ADDON_FORM_DATA]
        stride = 32
        start = species * stride
        if (start + stride) * 2 > len(b):
            return []
        row = struct.unpack("<%dH" % stride, b[start * 2:(start + stride) * 2])
        return [(v & 0x7FFF, bool(v & 0x8000)) for v in row if v]

    # ------------------------------------------------------------ learnsets
    def learnset(self, index):
        """[(level, move)] for one species. The archive is one flat blob of
        fixed-width records, 34 slots each, padded with (0xFFFF, 0)."""
        b = self.narc(NARC_LEARNSETS)[0]
        rec = LEARNSET_SLOTS * 4
        chunk = b[index * rec:(index + 1) * rec]
        out = []
        for i in range(LEARNSET_SLOTS):
            move, level = struct.unpack("<2H", chunk[i * 4:i * 4 + 4])
            if move == 0xFFFF:
                break
            out.append((level, move))
        return out

    # ----------------------------------------------------------- evolutions
    def evolutions(self, index):
        """[(method, param, target)] for one species, empty slots dropped.
        Targets are donor species ids and some of them dangle: Hardlove's table
        was built against a newer hg-engine whose species list is longer."""
        b = self.narc(NARC_EVOLUTIONS)[index]
        out = []
        for i in range(EVOLUTION_SLOTS):
            method, param, target = struct.unpack("<3H", b[i * 6:i * 6 + 6])
            if method or target:
                out.append((method, param, target))
        return out

    # ----------------------------------------------------------------- text
    def text_bank(self, index, msgenc, charmap):
        """Decode one text bank with the repo's own msgenc. Returns the list of
        messages; each is a string, or a list of lines for a multi-line one."""
        data = self.narc(NARC_TEXT)[index]
        with tempfile.TemporaryDirectory() as tmp:
            binpath = os.path.join(tmp, "bank.bin")
            jsonpath = os.path.join(tmp, "bank.json")
            with open(binpath, "wb") as f:
                f.write(data)
            subprocess.run([msgenc, "-d", "--json", "-c", charmap, jsonpath, binpath],
                           check=True, capture_output=True)
            with open(jsonpath, encoding="utf-8") as f:
                msgs = json.load(f)["messages"]
        return [m.get("en_US") for m in msgs]


def _walk(folder, prefix=""):
    out = {}
    for i, name in enumerate(folder.files):
        out[prefix + name] = folder.firstID + i
    for folder_name, sub in folder.folders:
        out.update(_walk(sub, prefix + folder_name + "/"))
    return out

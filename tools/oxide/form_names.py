#!/usr/bin/env python3
"""The in-game names of the twelve form species, kept in one place.

The form species (Alolan Ninetales, the Galarian forms, the two megas and the
rest) are species of their own, with their own entries in the species name
bank, and nothing at runtime turns one back into its base. Hardlove's name
bank has "-----" in those slots, so a wild catch, a trainer's Pokemon and an
evolution into one were all named "-----". Ian chose short distinct names on
2026-09-28.

To change a spelling, edit FORM_NAMES and run this script: it writes the
name into every language of the species' pokedex_data, where the build reads
it. `--check` reports any file that disagrees with the table and exits 1.
species_import.py takes its form names from here too, so a re-import cannot
bring the dashes back.

A name must fit the 10-character name slot (MON_NAME_LEN). Every capital,
digit and the hyphen are 6 pixels wide in the game's fonts, so 10 of them
come to 60 pixels, the same as vanilla's widest names (WIGGLYTUFF); anything
that fits the slot fits the summary, the battle HP box and the dex list.
The same Latin name goes in all six languages, as the new species do.
"""
import os
import sys

import jsonstyle

FORM_NAMES = {
    "SPECIES_ALOLAN_NINETALES": "A-NINETALS",
    "SPECIES_GALARIAN_WEEZING": "G-WEEZING",
    "SPECIES_GALARIAN_RAPIDASH": "G-RAPIDASH",
    "SPECIES_GALARIAN_MR_MIME": "G-MR. MIME",
    "SPECIES_GALARIAN_ARTICUNO": "G-ARTICUNO",
    "SPECIES_GALARIAN_ZAPDOS": "G-ZAPDOS",
    "SPECIES_GALARIAN_MOLTRES": "G-MOLTRES",
    "SPECIES_GYARADOS_M": "M-GYARADOS",
    "SPECIES_LOPUNNY_M": "M-LOPUNNY",
    "SPECIES_HISUIAN_SLIGGOO": "H-SLIGGOO",
    "SPECIES_HISUIAN_GOODRA": "H-GOODRA",
    "SPECIES_ZYGARDE_10": "ZYGARDE-10",
}

LANGUAGES = ("en", "fr", "de", "it", "es", "jp")
MON_NAME_LEN = 10
# Characters every one of these names may use; each is in the text encoder's
# charmap and already appears in a vanilla species name.
ALLOWED = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-. ")

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", ".."))


def data_path(constant):
    folder = constant[len("SPECIES_"):].lower()
    return os.path.join(ROOT, "res", "pokemon", folder, "data.json")


def problems_with_names():
    """Names that would not fit the slot or the font."""
    out = []
    for constant, name in FORM_NAMES.items():
        if len(name) > MON_NAME_LEN:
            out.append("%s: %r is %d characters, over %d" % (constant, name, len(name), MON_NAME_LEN))
        bad = sorted(set(name) - ALLOWED)
        if bad:
            out.append("%s: %r uses %s" % (constant, name, "".join(bad)))
    return out


def run(check):
    problems = problems_with_names()
    if problems:
        print("\n".join(problems))
        return 1
    stale = []
    for constant, name in FORM_NAMES.items():
        path = data_path(constant)
        text = open(path, encoding="utf-8").read()
        new = text
        for lang in LANGUAGES:
            key = ["pokedex_data", lang, "name"]
            if jsonstyle.get_value(new, key) != name:
                new = jsonstyle.replace_value(new, key, name)
        if new != text:
            stale.append(os.path.relpath(path, ROOT))
            if not check:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(new)
    if check:
        for p in stale:
            print("form name differs from form_names.py: " + p)
        return 1 if stale else 0
    for p in stale:
        print("wrote " + p)
    if not stale:
        print("nothing to do")
    return 0


if __name__ == "__main__":
    sys.exit(run("--check" in sys.argv[1:]))

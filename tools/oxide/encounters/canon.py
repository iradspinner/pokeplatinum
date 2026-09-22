"""What a species is *supposed* to be, and what a damage calculator calls it.

Two jobs that turn out to be one. The dex wants to say how far Oxide's numbers
have moved from the real ones, which for the 159 ported species is not a
question `main` can answer: Annihilape is simply absent from vanilla Platinum,
so comparing against it says "new" and stops. And D5 has to hand the calculator
species under Showdown's spellings. Both need the same map from our constants
to canonical names, so it lives here once.

The canonical table is `canon.json`, dumped from the vendored calculator's own
Generation 9 data by `make_canon.js`. That makes it the right baseline twice
over: it is what a species really has in its home generation, and it is exactly
what the calculator will believe when it is fed ours.

`showdown_name()` is mostly a rule with a short list of exceptions, and the rule
is checked rather than trusted: `unmatched()` returns every species in the tree
that does not land on a canonical entry, and the test suite requires that list
to hold only what is deliberately absent.
"""
import functools
import json
import os
import unicodedata

CANON = os.path.join(os.path.dirname(os.path.abspath(__file__)), "canon.json")

# Regional forms are a prefix here and a suffix there.
REGIONS = {"ALOLAN": "Alola", "GALARIAN": "Galar", "HISUIAN": "Hisui",
           "PALDEAN": "Paldea"}

# Names no rule produces: punctuation, particles, and the forms whose suffix
# is a number or a percentage.
EXCEPTIONS = {
    "SPECIES_NIDORAN_F": "Nidoran-F",
    "SPECIES_NIDORAN_M": "Nidoran-M",
    "SPECIES_FARFETCHD": "Farfetch\u2019d",
    "SPECIES_SIRFETCHD": "Sirfetch\u2019d",
    "SPECIES_HO_OH": "Ho-Oh",
    "SPECIES_MR_MIME": "Mr. Mime",
    "SPECIES_MR_RIME": "Mr. Rime",
    "SPECIES_MIME_JR": "Mime Jr.",
    "SPECIES_PORYGON_Z": "Porygon-Z",
    "SPECIES_PORYGON2": "Porygon2",
    "SPECIES_TYPE_NULL": "Type: Null",
    "SPECIES_JANGMO_O": "Jangmo-o",
    "SPECIES_HAKAMO_O": "Hakamo-o",
    "SPECIES_KOMMO_O": "Kommo-o",
    "SPECIES_FLABEBE": "Flabébé",
    "SPECIES_ZYGARDE_10": "Zygarde-10%",
    "SPECIES_ZYGARDE_50": "Zygarde",
    "SPECIES_GALARIAN_MR_MIME": "Mr. Mime-Galar",
    "SPECIES_GALARIAN_ARTICUNO": "Articuno-Galar",
    "SPECIES_GALARIAN_ZAPDOS": "Zapdos-Galar",
    "SPECIES_GALARIAN_MOLTRES": "Moltres-Galar",
}


@functools.lru_cache(maxsize=1)
def table():
    """{showdown name: {stats, types, weightkg, abilities}} for Generation 9.

    Keys are normalised, because upstream writes Flabébé with combining
    accents and we write it precomposed: identical on screen, unequal in
    Python."""
    with open(CANON, encoding="utf-8") as f:
        raw = json.load(f)
    return {unicodedata.normalize("NFC", k): v for k, v in raw.items()}


def showdown_name(species):
    """Our constant as the calculator spells it."""
    if species in EXCEPTIONS:
        return EXCEPTIONS[species]
    body = species.replace("SPECIES_", "")
    for prefix, suffix in REGIONS.items():
        if body.startswith(prefix + "_"):
            return _title(body[len(prefix) + 1:]) + "-" + suffix
    if body.endswith("_M") and len(body) > 2:
        return _title(body[:-2]) + "-Mega"
    return _title(body)


def _title(body):
    return " ".join(part.capitalize() for part in body.split("_"))


def canon_of(species):
    """The canonical record for a species, or None when it has no counterpart."""
    return table().get(unicodedata.normalize("NFC", showdown_name(species)))


def delta(species, record):
    """How far a species has been moved from its canonical self.

    None when there is nothing to compare against, otherwise only the fields
    that differ. Types are compared as sets, because the order of a dual type
    is not something either side is careful about."""
    was = canon_of(species)
    if was is None:
        return None
    out = {}
    stats = {k: record["stats"][k] - was["stats"][k] for k in record["stats"]
             if record["stats"].get(k) != was["stats"].get(k)}
    if stats:
        out["stats"] = stats
        out["bst"] = sum(stats.values())
    mine = {t.title() for t in record["types"]}
    theirs = set(was["types"])
    if mine != theirs:
        out["types"] = {"was": sorted(theirs), "now": sorted(mine)}
    out["name"] = showdown_name(species)
    return out


def unmatched(species_list):
    """Every species that does not land on a canonical entry. The rule is only
    worth having if this stays empty but for what is deliberately absent."""
    return [s for s in species_list if canon_of(s) is None]

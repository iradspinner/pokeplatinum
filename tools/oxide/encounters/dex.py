"""Species names and evolution lines, read from res/pokemon/.

Two things the encounter tool needs that the encounter files do not carry.

*Names.* `include/generated/species.h` is a build artefact and absent from a
clean tree, so the constants are derived from the directory listing. All 329
species used across the encounter files are covered by the 496 found there.

*Lines.* The dupes clause works on evolution families, not on species: a
Starly caught on Route 201 also dupes out Staravia and Staraptor wherever they
appear. Each species' `data.json` carries its `evolutions`, so the families
are the connected components of that graph -- which also handles branching
(Eevee) and convergent lines without any special casing.
"""
import json
import os

# SPECIES_MR_MIME is not "Mr Mime" and SPECIES_NIDORAN_F is not "Nidoran F".
# Only these need help; everything else title-cases.
SPECIAL_NAMES = {
    "SPECIES_HO_OH": "Ho-Oh",
    "SPECIES_MIME_JR": "Mime Jr.",
    "SPECIES_MR_MIME": "Mr. Mime",
    "SPECIES_NIDORAN_F": "Nidoran♀",
    "SPECIES_NIDORAN_M": "Nidoran♂",
    "SPECIES_PORYGON_Z": "Porygon-Z",
    "SPECIES_FARFETCHD": "Farfetch'd",
    "SPECIES_PORYGON2": "Porygon2",
}

_CACHE = {}


def display_name(species):
    """SPECIES_GLALIE -> Glalie. The page never shows a raw constant."""
    if species in SPECIAL_NAMES:
        return SPECIAL_NAMES[species]
    return " ".join(w.capitalize()
                    for w in species.replace("SPECIES_", "").split("_"))


def _pokemon_dir(root):
    return os.path.join(root, "res", "pokemon")


def species_universe(root):
    path = _pokemon_dir(root)
    return sorted("SPECIES_" + d.upper() for d in os.listdir(path)
                  if not d.startswith(".")          # res/pokemon/.shared
                  and os.path.isdir(os.path.join(path, d)))


def _build_lines(root):
    """{species: line_id} over the evolution graph's connected components."""
    known = set(species_universe(root))
    parent = {s: s for s in known}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[max(ra, rb)] = min(ra, rb)   # lowest name is the line id

    for species in known:
        folder = species.replace("SPECIES_", "").lower()
        data = os.path.join(_pokemon_dir(root), folder, "data.json")
        try:
            with open(data, encoding="utf-8") as f:
                evos = json.load(f).get("evolutions") or []
        except (FileNotFoundError, ValueError):
            continue
        for evo in evos:
            # Entries vary in arity, so the target is found by looking for the
            # SPECIES_ element rather than by position:
            #   ["EVO_LEVEL", 14, "SPECIES_STARAVIA"]
            #   ["EVO_LEVEL_MOSS_ROCK", "SPECIES_LEAFEON"]
            #   ["EVO_USE_ITEM", "ITEM_THUNDERSTONE", "SPECIES_JOLTEON"]
            # Assuming index 2 silently drops the two-element forms, which is
            # four of Eevee's seven.
            if not isinstance(evo, list):
                continue
            for field in evo:
                if (isinstance(field, str) and field.startswith("SPECIES_")
                        and field in known):
                    union(species, field)
    return {s: find(s) for s in known}


def lines(root):
    if "lines" not in _CACHE:
        _CACHE["lines"] = _build_lines(root)
    return _CACHE["lines"]


def line_of(root, species):
    return lines(root).get(species, species)


def members_of_line(root, line_id):
    return sorted(s for s, l in lines(root).items() if l == line_id)


def expand_caught(root, caught):
    """Every species duped out by what has been caught.

    Catching one member of a family dupes out the whole family, so this is
    what the odds are actually conditioned on.
    """
    table = lines(root)
    caught_lines = {table.get(s, s) for s in caught}
    return {s for s, l in table.items() if l in caught_lines}

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


def _normalise(name):
    """The pick-list writes 'Nidoran F', 'Mr. Mime', "Farfetch'd"; the tree
    writes SPECIES_NIDORAN_F, SPECIES_MR_MIME, SPECIES_FARFETCHD. Both sides
    collapse to the same key here, so the reverse mapping never needs a
    hand-written exception table beyond SPECIAL_NAMES."""
    if name.startswith("SPECIES_"):
        name = name[len("SPECIES_"):]
    out = name.upper()
    for ch in ("'", ".", "%", ":"):
        out = out.replace(ch, "")
    out = out.replace("♀", " F").replace("♂", " M")
    return "_".join(out.replace("-", " ").split())


def constant_of(root, name):
    """'Starly' -> SPECIES_STARLY, or None when nothing in the tree matches.

    The reverse of display_name. A pick-list row whose species has not been
    ported yet (the 159 `new` rows) has no constant and comes back None,
    which is the signal the audit and coverage commands key off.
    """
    if "constants" not in _CACHE:
        _CACHE["constants"] = {_normalise(s): s for s in species_universe(root)}
        for const, shown in SPECIAL_NAMES.items():
            _CACHE["constants"].setdefault(_normalise(shown), const)
    return _CACHE["constants"].get(_normalise(name))


PICK_LIST = ("docs", "oxide", "species-pick-list.csv")


def pick_list(root):
    """The species pick-list, one dict per row, with `constant` resolved
    against the tree (None for rows the tree does not have yet) and `tier`
    present whether or not the CSV has the column yet."""
    import csv
    rows = []
    with open(os.path.join(root, *PICK_LIST), encoding="utf-8", newline="") as f:
        for r in csv.DictReader(f):
            r = dict(r)
            r["constant"] = constant_of(root, r["name"])
            r.setdefault("tier", "")
            rows.append(r)
    return rows


def _build_lines(root):
    """{species: line_id} over the evolution graph's connected components.
    Also records the directed edges, which line_base needs."""
    known = set(species_universe(root))
    parent = {s: s for s in known}
    evolves_into = {s: set() for s in known}
    evo_levels = {}

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
            # The level for a level-up method (EVO_LEVEL and its variants,
            # whose first int is the level); None for a stone, a trade or
            # friendship, which no level cap gates.
            method = evo[0] if evo and isinstance(evo[0], str) else ""
            ints = [x for x in evo if isinstance(x, int) and not isinstance(x, bool)]
            level = ints[0] if method.startswith("EVO_LEVEL") and ints else None
            for field in evo:
                if (isinstance(field, str) and field.startswith("SPECIES_")
                        and field in known):
                    union(species, field)
                    evolves_into[species].add(field)
                    evo_levels.setdefault(species, []).append((field, level))
    _CACHE["evolves_into"] = evolves_into
    _CACHE["evo_levels"] = evo_levels
    return {s: find(s) for s in known}


def final_by_level(root, species):
    """The lowest level at which `species` stands fully evolved by level-up
    alone: 0 for a final stage, the last level-up level along the cheapest
    all-level-up path otherwise, or None when every path needs a stone, a
    trade or friendship. Ian's cap rule (2026-09-21): a line whose final
    stage comes by level-up under a split's cap belongs in or before that
    split."""
    lines(root)
    levels = _CACHE.get("evo_levels") or {}

    def walk(s, seen):
        # A mega or regional form is listed as an "evolution" of its base
        # (SPECIES_GYARADOS -> SPECIES_GYARADOS_M); it is not a stage.
        targets = [(t, lv) for t, lv in (levels.get(s) or [])
                   if not t.startswith(s + "_")]
        if not targets:
            return 0
        best = None
        for t, lv in targets:
            if lv is None or t in seen:
                continue
            rest = walk(t, seen | {t})
            if rest is None:
                continue
            cand = max(lv, rest)
            if best is None or cand < best:
                best = cand
        return best
    return walk(species, {species})


def lines(root):
    if "lines" not in _CACHE:
        _CACHE["lines"] = _build_lines(root)
    return _CACHE["lines"]


def line_base(root, line_id):
    """The first stage(s) of a line: members nothing in the line evolves
    into. Usually one species; a line with two roots (none in Platinum's
    data, but the graph allows it) returns both, sorted."""
    lines(root)
    members = members_of_line(root, line_id)
    evolved = set()
    for s in members:
        evolved |= _CACHE["evolves_into"].get(s, set())
    roots = [s for s in members if s not in evolved]
    return roots or members[:1]


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

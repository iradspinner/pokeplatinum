"""The team builder's three move lists (build plan item 28), kept apart as
Ian asked:

1. **Oxide's own**: what the Pokemon can know in Oxide at its level, read
   from res/pokemon/ on every request, because the learnset cloud job keeps
   rewriting the level-up lists. Level-up moves at or below the level (an
   earlier stage's too, credited to it), then TM and HM, tutor and egg
   moves (the egg moves of the line's first stage).
2. **Generation IV legal**: Pokemon Showdown's sources marked 4 (Diamond,
   Pearl, Platinum, HeartGold and SoulSilver). Empty for a species added
   later.
3. **Latest-generation legal**: the newest generation the species appears
   in; Generation 8 for one Scarlet and Violet cut.

Lists 2 and 3 come from canon_learnsets.json, which make_learnsets.js
writes from the Showdown package (canon_src/README.md has its provenance);
both follow Showdown's own evolution chains, since they are about canon. A
move Oxide does not have is listed with move None, to be seen and not
picked.
"""
import functools
import json
import os
import re

from . import calc_export
from . import calc_trainers
from . import canon
from . import dex
from . import pokedex

HERE = os.path.dirname(os.path.abspath(__file__))
CANON = os.path.join(HERE, "canon_learnsets.json")
HOW = {"M": "TM", "T": "Tutor", "E": "Egg", "S": "Event", "R": "Form", "D": "Dream World"}


def to_id(name):
    return re.sub(r"[^a-z0-9]", "", str(name).lower())


@functools.lru_cache(maxsize=1)
def canon_lists():
    with open(CANON, encoding="utf-8") as f:
        return json.load(f)


# Moves Oxide still calls by their Generation IV names, which Showdown has
# since renamed: Showdown's id to Oxide's.
RENAMED = {"feintattack": "faintattack", "highjumpkick": "hijumpkick",
           "smellingsalts": "smellingsalt", "visegrip": "vicegrip"}


def move_ids(root):
    """{Showdown move id: MOVE_X} for every move Oxide has. A Z-move's
    special twin (named "... (Special)" by the calculator) is left out."""
    out = {}
    for const, rec in pokedex.moves(root).items():
        name = rec.get("name") or ""
        if name and "(Special)" not in name:
            out.setdefault(to_id(name), const)
    for new, old in RENAMED.items():
        if old in out:
            out.setdefault(new, out[old])
    return out


def showdown_id(root, species, form=0):
    folder = calc_trainers.FORM_FOLDERS.get((species, form or 0))
    name = calc_export.form_folders_inverse().get((species, folder)) if folder else None
    return to_id(name or canon.showdown_name(species))


# A level-0 learnset entry is an evolution move (2026-09-28): taught the moment
# a Pokemon evolves into the species, at any level, and offered by the Move
# Relearner, so it is on a trainer's legal palette. It reads as this, and
# sorts first.
ON_EVOLVING = "On evolving"


def _how(code):
    if code == "L0":
        return ON_EVOLVING
    return "Level " + code[1:] if code.startswith("L") else HOW.get(code, code)


def _entry(root, const, name, how, source=None):
    rec = pokedex.moves(root).get(const) if const else None
    return {"move": const, "name": (rec or {}).get("name") or name, "how": how,
            "from": source, "type": (rec or {}).get("type"),
            "power": (rec or {}).get("power"), "class": (rec or {}).get("class")}


def _level_key(e):
    if e["how"].startswith(ON_EVOLVING):
        return (0, -1, e["name"])
    m = re.match(r"Level (\d+)", e["how"])
    return (0, int(m.group(1)), e["name"]) if m else (1, 0, e["name"])


def canon_list(root, species, form, which):
    """List 2 ("gen4") or 3 ("latest") for one species: (entries, gen, games)."""
    table = canon_lists()
    rec = table.get(showdown_id(root, species, form)) or table.get(showdown_id(root, species))
    if not rec:
        return [], None, None
    ids, names = move_ids(root), table.get("_moves", {})
    raw = rec["gen4"] if which == "gen4" else rec["latest"]["moves"]
    out = []
    for item in raw:
        move, codes = item[0], item[1]
        source = item[2] if len(item) > 2 else None
        how = ", ".join(_how(c) for c in codes.split(","))
        out.append(_entry(root, ids.get(move), names.get(move, move), how,
                          names.get(source) or (source.title() if source else None)))
    out.sort(key=_level_key)
    if which == "gen4":
        return out, 4, "Diamond, Pearl, Platinum, HeartGold and SoulSilver"
    return out, rec["latest"]["gen"], rec["latest"]["games"]


def _record(root, species, form):
    folder = calc_trainers.FORM_FOLDERS.get((species, form or 0))
    return calc_trainers._raw_species(root, species, folder)


def earlier_stages(root, species):
    """Oxide's own earlier stages of `species`, nearest first."""
    dex.lines(root)
    into = dex._CACHE.get("evolves_into") or {}
    out, cur = [], species
    while True:
        parents = sorted(s for s, t in into.items() if cur in t and not cur.startswith(s + "_"))
        if not parents or parents[0] in out:
            return out
        out.append(parents[0])
        cur = parents[0]


def oxide_list(root, species, form, level):
    """List 1: what the Pokemon can know in Oxide at `level`."""
    machines = pokedex.machines(root)
    seen, out = set(), []

    def add(const, how, source=None):
        if const and const != "MOVE_NONE" and (const, source) not in seen:
            seen.add((const, source))
            out.append(_entry(root, const, const, how, source))

    learnset = _record(root, species, form).get("learnset") or {}
    own = {}
    for lv, move in learnset.get("by_level") or []:
        if lv <= level:
            own.setdefault(move, []).append(lv)
    for move, lvs in own.items():
        # A move learned on evolving and at a level too reads as both in its
        # one entry ("On evolving, level 20"), and sorts with the evolution moves.
        rest = ", ".join(str(x) for x in sorted(set(x for x in lvs if x)))
        if 0 in lvs:
            add(move, ON_EVOLVING + (", level " + rest if rest else ""))
        else:
            add(move, "Level " + rest)
    for stage in earlier_stages(root, species):
        stage_ls = (calc_trainers._raw_species(root, stage).get("learnset") or {})
        for lv, move in stage_ls.get("by_level") or []:
            if lv <= level and move not in own:
                add(move, ON_EVOLVING if lv == 0 else f"Level {lv}", dex.display_name(stage))
    for tm in learnset.get("by_tm") or []:
        add(machines.get(tm), tm.replace("TM", "TM ").replace("HM", "HM "))
    for move in learnset.get("by_tutor") or []:
        add(move, "Tutor")
    first = (earlier_stages(root, species) or [species])[-1]
    first_ls = (calc_trainers._raw_species(root, first).get("learnset") or {}) \
        if first != species else learnset
    for move in first_ls.get("egg_moves") or []:
        add(move, "Egg", dex.display_name(first) if first != species else None)
    out.sort(key=_level_key)
    return out


def lists(root, species, form=0, level=100):
    """The three lists for one team member, each apart."""
    gen4, _, gen4_games = canon_list(root, species, form, "gen4")
    latest, gen, games = canon_list(root, species, form, "latest")
    return {"species": species, "form": form or 0, "level": level,
            "oxide": oxide_list(root, species, form, level),
            "gen4": {"gen": 4, "games": gen4_games, "moves": gen4},
            "latest": {"gen": gen, "games": games, "moves": latest}}

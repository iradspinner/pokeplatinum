"""The trainer team builder's model (build plan item 28, Ian, 2026-09-27).

Every trainer is one file under res/trainers/data/, which the packer
(tools/dataproc/src/trainerproc.c) turns into the game's trainer archives.
This module reads those files for the Trainers tab: a list of every trainer
with its split and level cap, and one trainer's team as the game builds it
in battle (nature, ability, gender and default moves come from
calc_trainers, which follows TrainerData_BuildParty).

The split is the balance track's placement, read without building any party
so the whole list costs about three seconds once: a story fight's split from
fights.json, else the split B6 places the trainer in, else the maps that
field it. It is the order teamscore.resolve uses, and test_trainers holds
the two to the same answer. A trainer with no split (the dummies, and the
slots no map fields) has no cap and no score.
"""
import functools
import json
import os

from . import calc_trainers
from . import dex
from . import model
from . import pokedex

DATA = ("res", "trainers", "data")
# enum TrainerMonAbility: 0 either ordinary slot by personality, 1 and 2 that
# slot, 3 the hidden ability (1832a346c).
ABILITY_CHOICES = {0: "either, by personality", 1: "slot 1", 2: "slot 2", 3: "hidden"}


def path_of(root, stem):
    return os.path.join(root, *DATA, stem + ".json")


def stems(root):
    return sorted(f[:-5] for f in os.listdir(os.path.join(root, *DATA)) if f.endswith(".json"))


def load(root, stem):
    """The trainer's file as JSON. A stem is a file name, never a path."""
    if not stem or "/" in stem or "\\" in stem or stem.startswith("."):
        raise KeyError(stem)
    with open(path_of(root, stem), encoding="utf-8") as f:
        return json.load(f)


def _stamp(root):
    """Changes whenever a trainer file does, so the list is rebuilt after a save."""
    base = os.path.join(root, *DATA)
    return max(os.stat(os.path.join(base, f)).st_mtime_ns for f in os.listdir(base))


@functools.lru_cache(maxsize=1)
def split_map(root):
    """{stem: split or None}, placed as teamscore.resolve places a fight."""
    from ..balance import b6, data as bdata, splits as bsplits
    ids = calc_trainers._tables(root)["ids"]
    story = {}
    for fight in bdata.fights()["fights"]:
        for tr in fight["tr_ids"]:
            story.setdefault(tr, fight["split"])
    placed = b6.placements()
    out = {}
    for stem in stems(root):
        tr = ids.get("TRAINER_" + stem.upper())
        if tr is None:
            out[stem] = None
            continue
        out[stem] = story.get(tr) or (placed.get(tr) or {}).get("split") \
            or bsplits.trainer_split(tr)
    return out


@functools.lru_cache(maxsize=1)
def caps():
    """{split: level cap}, the balance track's, which its tests hold to the engine's."""
    from ..balance import pool
    return dict(pool.caps())


def split_order():
    from ..balance import pool
    return list(pool.SPLITS)


def summary(root=None):
    """One row per trainer for the list, rebuilt when a trainer file changes."""
    root = root or model.repo_root()
    return _summary(root, _stamp(root))


@functools.lru_cache(maxsize=2)
def _summary(root, stamp):
    places, cap = split_map(root), caps()
    rows = []
    for stem in stems(root):
        data = load(root, stem)
        party = data.get("party") or []
        split = places.get(stem)
        rows.append({
            "stem": stem, "name": data.get("name", ""), "label": calc_trainers.trainer_name(root, data, stem),
            "class": data.get("class"), "split": split, "cap": cap.get(split),
            "double": bool(data.get("double_battle")),
            "party": [{"species": m["species"], "level": m["level"]} for m in party],
            "top": max((m["level"] for m in party), default=0),
        })
    return rows


def _ability_options(root, species, form):
    """The names a party member's ability value can give, from the record the
    game reads: the form's own where it has one (f801cc160)."""
    folder = calc_trainers.FORM_FOLDERS.get((species, form or 0))
    record = calc_trainers._raw_species(root, species, folder)
    a1, a2, hidden = (record["abilities"] + ["ABILITY_NONE"] * 3)[:3]
    tidy = lambda a: None if a == "ABILITY_NONE" else a.replace("ABILITY_", "")
    return {"1": tidy(a1), "2": tidy(a2), "hidden": tidy(hidden)}


def detail(root, stem, data=None):
    """One trainer's team, as the file has it and as the game builds it.
    `data` is an unsaved edit of the file, shown the same way."""
    data = data if data is not None else load(root, stem)
    moves = pokedex.moves(root)
    built = calc_trainers.build_trainer(root, stem, data)
    party = data.get("party") or []
    split = split_map(root).get(stem)
    members = []
    for m, (showdown, s) in zip(party, built):
        rec = pokedex.load(root, m["species"]) or {}
        file_moves = m.get("moves")
        members.append({
            "file": m,
            "name": dex.display_name(m["species"]),
            "folder": rec.get("folder"),
            "types": rec.get("types") or [],
            "stats": rec.get("stats") or {},
            "abilities": _ability_options(root, m["species"], m.get("form")),
            "iv": m["iv_scale"] * calc_trainers.MAX_IV // calc_trainers.MAX_IV_SCALE,
            "built": {"nature": s["nature"], "ability": s["ability"], "gender": s["gender"],
                      "moves": s["moves"], "item": s.get("item"),
                      "default_moves": not isinstance(file_moves, list)},
            "move_names": [(moves.get(mv) or {}).get("name", mv)
                           for mv in (file_moves or []) if mv and mv != "MOVE_NONE"],
            "calc_name": showdown,
        })
    return {
        "stem": stem, "label": calc_trainers.trainer_name(root, data, stem),
        "name": data.get("name", ""), "class": data.get("class"),
        "ai_flags": data.get("ai_flags") or [], "double_battle": bool(data.get("double_battle")),
        "items": data.get("items") or [], "split": split, "cap": caps().get(split),
        "members": members,
        "all_ai_flags": ai_flags(root, data.get("ai_flags") or []),
        "ability_choices": ABILITY_CHOICES,
    }


def ai_flags(root, chosen=()):
    """The AI flags in bit order: every named one, and an unused bit only
    when this trainer sets it, since nothing reads those."""
    bits = calc_trainers._tables(root)["ai_bits"]
    return [f for f in sorted(bits, key=bits.get)
            if not f.startswith("AI_FLAG_UNUSED") or f in chosen]

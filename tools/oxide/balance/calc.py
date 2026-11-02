"""The damage calculator, run headless: the runner every fight reading uses.

The fight simulator (fightsim.prepare) asks the vendored calculator's own
engine for every matchup's sixteen damage rolls and both Speeds, through
calc_headless.js in one Node process (one a batch, in turn, for a job too
big for one: run_node). This module holds what it needs to do
that: the calculator's data (the encounter tool's calc_export, built once a
process and written to a file the runner reads), the runner itself with the
Eviolite rule the engine follows, and a fight's map weather in the
calculator's names.

These lived in pressure.py and teamscore.py, the first scoring system, until
that system was retired on 2026-10-13; they moved here unchanged.
"""
import functools
import json
import os
import re
import subprocess
import tempfile

from ..encounters import calc_export
from . import data, splits

HERE = os.path.dirname(os.path.abspath(__file__))
RUNNER = os.path.join(HERE, "calc_headless.js")

# The weathers the calculator models, by the census's names for them; fog
# has no effect on damage, so it maps to none.
CALC_WEATHER = {"Rain": "Rain", "Sun": "Sun", "Sand": "Sand", "Hail": "Hail"}


@functools.lru_cache(maxsize=None)
def blob():
    """The calculator's data (species, moves, type chart), as the encounter
    tool's server hands it to the calculator's page; built once a process.

    The engine's effect decides whether a move's hits are always critical:
    every move whose effect is not one of calc_export.ALWAYS_CRIT_EFFECTS
    comes marked as not (willCrit false), so Zippy Zap, which the
    calculator knows as Let's Go's always critical move, is the plain hit
    of Oxide's effect script 316. Until 2026-10-20 Zippy Zap's rows were
    critical hits (Ian approved the fix); since the same day the export
    marks them, for the OxiDex's calculator page as for the runner, where
    this function did it for the runner alone."""
    return calc_export.build()


@functools.lru_cache(maxsize=None)
def blob_path():
    """The blob on disk, for the Node runner; kept for the process."""
    fd, path = tempfile.mkstemp(prefix="oxide-teamscore-", suffix=".json")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(blob(), f)
    return path


def fight_weather(tr_ids):
    """The calculator's weather for a fight: the first weather the census
    finds on any of its trainers' maps that the calculator models, or None."""
    for tr in tr_ids:
        for w in splits.trainer_weather(tr):
            if w in CALC_WEATHER:
                return CALC_WEATHER[w]
    return None


def fight_fog(tr_ids):
    """Whether a fight starts in deep fog: a map that battles one of its
    trainers has the overworld fog (splits.BATTLE_WEATHER's "Fog", which
    subscript_overworld_fog turns into FIELD_CONDITION_DEEP_FOG). The
    calculator has no fog, as fog changes no damage, so the battle keeps it
    apart from the rows' weather (fightsim.fog_cut)."""
    return any("Fog" in splits.trainer_weather(tr) for tr in tr_ids)


# The battle terrain each map backdrop gives (field_battle_data_transfer.c,
# sTerrainForBackground). The engine first reads the tile the player stands
# on (CalcTerrain: ice, tall grass, sand, snow, mud, a cave floor, water),
# which the simulator does not know, so a fight's terrain is its backdrop's.
TERRAIN_OF_BACKGROUND = {
    "BACKGROUND_PLAIN": "TERRAIN_PLAIN", "BACKGROUND_WATER": "TERRAIN_WATER", "BACKGROUND_CITY": "TERRAIN_BUILDING",
    "BACKGROUND_FOREST": "TERRAIN_GRASS", "BACKGROUND_MOUNTAIN": "TERRAIN_MOUNTAIN", "BACKGROUND_SNOW": "TERRAIN_SNOW",
    "BACKGROUND_INDOORS_1": "TERRAIN_BUILDING", "BACKGROUND_INDOORS_2": "TERRAIN_BUILDING",
    "BACKGROUND_INDOORS_3": "TERRAIN_BUILDING", "BACKGROUND_CAVE_1": "TERRAIN_CAVE", "BACKGROUND_CAVE_2": "TERRAIN_CAVE",
    "BACKGROUND_CAVE_3": "TERRAIN_CAVE", "BACKGROUND_AARON": "TERRAIN_AARON", "BACKGROUND_BERTHA": "TERRAIN_BERTHA",
    "BACKGROUND_FLINT": "TERRAIN_FLINT", "BACKGROUND_LUCIAN": "TERRAIN_LUCIAN", "BACKGROUND_CYNTHIA": "TERRAIN_CYNTHIA",
    "BACKGROUND_DISTORTION_WORLD": "TERRAIN_DISTORTION_WORLD",
}


@functools.lru_cache(maxsize=None)
def rematch_originals():
    """{a rematch's trainer id: the trainer it rematches}, from the Vs.
    Seeker's table (gVsSeekerRematchData in src/overlay005/vs_seeker.c),
    whose each row names a trainer and then its rematches, all fought by
    the same trainer on the map where the first was."""
    path = os.path.join(data.ROOT, "src", "overlay005", "vs_seeker.c")
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    body = text[text.index("gVsSeekerRematchData[]"):]
    body = body[:body.index("};")]
    out = {}
    for line in body.split("\n"):
        names = re.findall(r"\b(TRAINER_[A-Z0-9_]+)\b", line)
        ids = [splits._trainer_id(n) for n in names]
        if len(ids) > 1 and ids[0] is not None:
            for tr in ids[1:]:
                if tr is not None and tr != ids[0]:
                    out[tr] = ids[0]
    return out


def fight_terrain(tr_ids):
    """The battle terrain of a fight (BattleSystem_GetTerrain, which
    Camouflage, Secret Power and Nature Power read): the backdrop's of the
    first map, by name, that battles one of its trainers, a rematch's on
    the maps of the trainer it rematches (rematch_originals), or None,
    which the battle reads as a building's. Until 2026-10-15 a rematch
    named no map and read as a building (Ian approved the fix)."""
    heads = splits.headers()
    maps = splits.trainer_maps()
    for tr in tr_ids:
        found = maps.get(tr) or maps.get(rematch_originals().get(tr), ())
        for h in sorted(found):
            bg = heads.get(h, {}).get("battleBG")
            if bg in TERRAIN_OF_BACKGROUND:
                return TERRAIN_OF_BACKGROUND[bg]
    return None


@functools.lru_cache(maxsize=None)
def can_evolve():
    """{calculator name: whether the species can still evolve}, from Oxide's
    own evolution records. The engine gives the Eviolite to a species whose
    first evolution slot is in use (Species_CanEvolve, battle_lib.c); the
    calculator's Generation 4 mechanics ask its Generation 4 species table
    instead, which has no species added later (Naclstack's line), so the
    runner is told the engine's answer for each holder."""
    from ..encounters import pokedex
    from . import plteam
    out = {}
    for sp in pokedex.species_list(data.ROOT):
        raw = pokedex._read(data.ROOT, f"res/pokemon/{pokedex.folder_of(sp)}/data.json") or {}
        name = plteam.species_name(sp)
        out[name] = out.get(name, False) or bool(raw.get("evolutions"))
    return out


# The most move rows one Node process is given. The runner returns its whole
# answer as one JSON string, and V8 caps a string at about 536 million
# characters; each move's row (its sixteen rolls, priority and category)
# takes about 135 of them, so a job past about 4 million moves died with
# "Invalid string length", and the rows it held before writing ran its
# heap out first (Ace Trainer Alyssa's blind draw in Byron's split, 7.2
# million moves, 2026-11-02). 400,000 moves write about 54 MB.
BATCH_MOVES = 400_000


def batches(pairs, budget):
    """The pairs in order, cut into runs of at most `budget` moves each (a
    pair counts its moves, and one more for its row), a pair never split."""
    out, run, used = [], [], 0
    for pair in pairs:
        cost = 1 + len(pair[2])
        if run and used + cost > budget:
            out.append(run)
            run, used = [], 0
        run.append(pair)
        used += cost
    if run or not out:
        out.append(run)
    return out


def run_node(blob_path, jobs):
    """Node processes one after another, each waited on, so nothing else runs
    beside them: one for a job of up to BATCH_MOVES moves, and for a bigger
    job one for each batch of its pairs, joined into the answer one process
    would have given. Each batch is sent every Pokemon, so each runner sets
    up its engine as the one would (the Eviolite's and exact types' tables);
    the calculator copies a Pokemon before each matchup, so no row depends
    on the rows run before it in the same process. The results keep the
    pairs' order and the Pokemon their first appearance's."""
    # Each Eviolite holder carries whether its species can still evolve, by
    # the engine's rule (can_evolve), for the runner's Generation 4 table.
    pokemon = jobs.get("pokemon") or {}
    if any(p.get("item") == "Eviolite" for p in pokemon.values()):
        evolves = can_evolve()
        jobs = dict(jobs, pokemon={
            k: dict(p, can_evolve=evolves[p["species"]])
            if p.get("item") == "Eviolite" and p.get("species") in evolves else p
            for k, p in pokemon.items()})
    runs = batches(jobs.get("pairs") or [], BATCH_MOVES)
    if len(runs) == 1:
        return _run_once(blob_path, jobs)
    out = {"pokemon": {}, "results": [], "seconds": 0.0}
    for run in runs:
        part = _run_once(blob_path, dict(jobs, pairs=run))
        out["results"].extend(part["results"])
        for k, info in part["pokemon"].items():
            out["pokemon"].setdefault(k, info)
        out["seconds"] += part.get("seconds", 0.0)
    return out


def _run_once(blob_path, jobs):
    """One Node process on one job, waited on."""
    with tempfile.TemporaryDirectory(prefix="oxide-b3-") as tmp:
        jobs_path, out_path = os.path.join(tmp, "jobs.json"), os.path.join(tmp, "out.json")
        with open(jobs_path, "w", encoding="utf-8") as f:
            json.dump(jobs, f)
        subprocess.run(["node", RUNNER, blob_path, jobs_path, out_path], check=True)
        with open(out_path, encoding="utf-8") as f:
            return json.load(f)

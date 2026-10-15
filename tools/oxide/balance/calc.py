"""The damage calculator, run headless: the runner every fight reading uses.

The fight simulator (fightsim.prepare) asks the vendored calculator's own
engine for every matchup's sixteen damage rolls and both Speeds, through
calc_headless.js in one Node process. This module holds what it needs to do
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
    tool's server hands it to the calculator's page; built once a process."""
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


def fight_terrain(tr_ids):
    """The battle terrain of a fight (BattleSystem_GetTerrain, which
    Camouflage reads): the backdrop's of the first map, by name, that
    battles one of its trainers, or None."""
    heads = splits.headers()
    for tr in tr_ids:
        for h in sorted(splits.trainer_maps().get(tr, ())):
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


def run_node(blob_path, jobs):
    """One Node process, waited on, so nothing else runs beside it."""
    # Each Eviolite holder carries whether its species can still evolve, by
    # the engine's rule (can_evolve), for the runner's Generation 4 table.
    pokemon = jobs.get("pokemon") or {}
    if any(p.get("item") == "Eviolite" for p in pokemon.values()):
        evolves = can_evolve()
        jobs = dict(jobs, pokemon={
            k: dict(p, can_evolve=evolves[p["species"]])
            if p.get("item") == "Eviolite" and p.get("species") in evolves else p
            for k, p in pokemon.items()})
    with tempfile.TemporaryDirectory(prefix="oxide-b3-") as tmp:
        jobs_path, out_path = os.path.join(tmp, "jobs.json"), os.path.join(tmp, "out.json")
        with open(jobs_path, "w", encoding="utf-8") as f:
            json.dump(jobs, f)
        subprocess.run(["node", RUNNER, blob_path, jobs_path, out_path], check=True)
        with open(out_path, encoding="utf-8") as f:
            return json.load(f)

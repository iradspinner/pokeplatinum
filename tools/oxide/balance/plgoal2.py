"""Goal 2's readings (the handoff's order of work, step 2): the team search on
goal 2's boxes for the fights through Fantina that have no hand-played line,
Barry 2 at 11, Jupiter 1 at 27, Lucas and Dawn 2 at 30 and Fantina at 33.
Roark, Mars 1 and Gardenia were read on the hand run's boxes by the team
search's test (plteam_test). These fights pass when Ian has read the
winner's line and reasoning and accepts it.

Each box is goal 2's (~/oxide-trials/three-gym-run/goal2-boxes.json, built
from the choices Ian accepted), every member at the fight's cap with its
whole move pool rebuilt by the capture rule from the species and level it
was caught at, through the run's holds and evolutions. The trainer's team is
the one a Piplup player meets. The items are the type boosters the run can
have picked up by each fight (fightsim's item rule hands them out):

    Barry 2       none; the Flame Plate is in Oreburgh Mine, and the Hard
                  Stone the split's list shows sits in an unused map
    Jupiter 1     the hand run's three (Flame Plate, Miracle Seed, Draco
                  Plate), with Eterna Forest's Silver Powder and the Old
                  Chateau's Dread Plate, both open with Cut after Gardenia
    Lucas, Dawn 2 those, with Route 206's Poison Barb
    Fantina       those, with Amity Square's Spooky Plate in Hearthome

Results go to ~/oxide-trials/scorer-stage2/team/<fight>/ (log.txt,
result.json, and line.txt, the winner's fight turn by turn).

    PYTHONPATH=. tools/oxide/capped python3 -m tools.oxide.balance.plgoal2 barry_2 jupiter_1 ...
"""
import json
import os
import sys

from . import plteam

BOXES = os.path.expanduser("~/oxide-trials/three-gym-run/goal2-boxes.json")
# The run's evolution holds (goal2_boxes.HOLD): each delayed for a move.
HOLDS = {"SPECIES_MAREEP": 28, "SPECIES_POPPLIO": 31, "SPECIES_CHARMANDER": 25, "SPECIES_GRUBBIN": 21}
EARLY = {"Fire": "Flame Plate", "Grass": "Miracle Seed", "Dragon": "Draco Plate",
         "Bug": "Silver Powder", "Dark": "Dread Plate"}
# fight: (story key, the variant a Piplup player meets, the boosters by then).
# Barry 2's files are named by the player's starter (TRAINER_RIVAL_ROUTE_203_
# PIPLUP is the first); Route 207's script gives a player whose starter is
# neither Turtwig nor the fire starter trainer 794 or 801, the second and
# fifth of fights.json's list, the same team (Monferno's).
FIGHTS = {
    "barry_2": ("barry_2", 0, {}),
    "jupiter_1": ("jupiter_1", 0, dict(EARLY)),
    "lucas_dawn_2": ("lucas_dawn_2", 1, dict(EARLY, Poison="Poison Barb")),
    "fantina": ("fantina", 0, dict(EARLY, Poison="Poison Barb", Ghost="Spooky Plate")),
}


def box(fight):
    """Goal 2's box at this fight as the team search reads it: each member
    with its whole move pool from its catch. The rebuilt member must be the
    species goal 2's table shows, or the box is not the one Ian accepted."""
    with open(BOXES) as fh:
        recs = json.load(fh)[fight]
    out = []
    for r in recs:
        final, pool_ = plteam.move_pool(r["base"], r["caught_level"], r["level"], HOLDS,
                                        magnetic=fight != "barry_2")
        if final != r["constant"]:
            raise ValueError(f"{fight}: {r['caught']} rebuilds as {final}, goal 2's box has {r['constant']}")
        out.append(plteam.record(final, r["level"], r["nature"], r["ability"], r["ivs"], pool_))
    return out


def run(fight, procs=10):
    key, variant, boosters = FIGHTS[fight]
    stock = {"boosters": boosters, "Leftovers": 0, "Sitrus Berry": 0}
    return plteam.search(fight, key, box(fight), stock, os.path.join(plteam.ROOT, "team", fight),
                         variant=variant, procs=procs)


if __name__ == "__main__":
    for name in sys.argv[1:] or list(FIGHTS):
        run(name)

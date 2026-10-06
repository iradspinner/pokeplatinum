"""The team search's first test (the Overseer's, Ian's go of 2026-10-02): the
search on the hand run's own boxes at Roark (cap 16), Mars 1 at its new soft
cap of 19, and Gardenia (cap 26). Does it find our hand-played sixes, or
sixes that read as well by Ian's order (wins first, then faints)? A miss at
Mars 1, which our six wins by a PP stall, would show the screen undervaluing
stall plans.

Each fight's box is the run's box at that fight (plstep3's ROARK, MARS and
GARDENIA records: natures, abilities, levels), each member with its whole
move pool by the capture rule from its catch level (box3.json) through the
run's holds and evolutions. Results and a log go to
~/oxide-trials/scorer-stage2/team/<fight>/.

    PYTHONPATH=. tools/oxide/capped python3 -m tools.oxide.balance.plteam_test roark mars gardenia
"""
import json
import os
import sys

from . import plteam, plstep3

RUN = os.path.expanduser("~/oxide-trials/three-gym-run")
HOLDS = {"SPECIES_CHARMANDER": 25, "SPECIES_GRUBBIN": 21, "SPECIES_MAREEP": 28, "SPECIES_POPPLIO": 31}
# The two trades come in at the level of the Pokemon given (about the cap of
# the split they were made in), and the honey tree's Grubbin at 13.
EXTRA = {"SPECIES_VULLABY": 16, "SPECIES_POPPLIO": 20, "SPECIES_GRUBBIN": 13}
# fight: (story key, cap, box records, the bar's six with its moves, the bar's numbers)
TESTS = {
    "roark": ("roark", 16, plstep3.ROARK, plstep3.FIGHTS["roark"]["six"], "98.5% clean, 100% won, 0.015 faints"),
    "mars": ("mars_1", 19, plstep3.MARS, ["Geodude", "Vullaby", "Starly", "Onix", "Grubbin", "Nidorino"],
             "67.1% clean, 99.8% won, 0.423 faints (our line adjusted to 19)"),
    "gardenia": ("gardenia", 26, plstep3.GARDENIA, plstep3.FIGHTS["gardenia"]["six"],
                 "15.1% clean, 59.9% won, 3.212 faints"),
}


def caught_levels():
    """{caught species: level} from the rolled box, with the trades and the
    honey tree."""
    out = {}
    for _where, sp, lvl in json.load(open(os.path.join(RUN, "box3.json"))):
        out[sp] = int(str(lvl).split("-")[-1])
    out.update(EXTRA)
    return out


def family(sp):
    seen, todo = {sp}, [sp]
    while todo:
        cur = todo.pop()
        for e in plteam.mon_data(cur).get("evolutions") or []:
            if str(e[-1]).startswith("SPECIES_") and e[-1] not in seen:
                seen.add(e[-1])
                todo.append(e[-1])
    return seen


def box(records, cap):
    """The box's members as the team search reads them, at the cap: each
    from its catch through the run's holds and evolutions, with its whole
    move pool."""
    caught = caught_levels()
    out = []
    for name, rec in records.items():
        const, nature, ability = rec[0], rec[1], rec[2]
        ivs = rec[4] if len(rec) > 4 else 15
        level = rec[5] if len(rec) > 5 else cap
        if name == "Charjabug" and cap < 20:
            const = "SPECIES_GRUBBIN"
        base = next(sp for sp in caught if const in family(sp))
        final, pool_ = plteam.move_pool(base, caught[base], level, HOLDS, magnetic=cap >= 26)
        out.append(plteam.record(final, level, nature, ability, ivs, pool_))
    return out


def run(fight, procs=10):
    """The search on the hand run's box at this fight, our six read beside
    its finalists (plteam.search)."""
    key, cap, records, bar_six, bar = TESTS[fight]
    f = plstep3.FIGHTS[fight]
    stock = {"boosters": dict(f["boosters"]), "Leftovers": 0, "Sitrus Berry": 0}
    return plteam.search(fight, key, box(records, cap), stock, os.path.join(plteam.ROOT, "team", fight),
                         ours=bar_six, bar=bar, procs=procs)


if __name__ == "__main__":
    for fight in sys.argv[1:] or list(TESTS):
        run(fight)

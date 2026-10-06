"""Stage 2's position features (plfeat.py): their sizes, that a position
always gives the same numbers, that the copy of a position gives what the
original does, and that the active Pokemon's matchup row moves with its
stat stages.

    PYTHONPATH=. python3 -m tools.oxide.balance.test_plfeat
"""
import random
import sys

from . import fightsim as fs
from . import perfectline as pl
from . import plfeat
from . import plplan
from . import plstep3

RESULTS = []


def check(name, ok, detail=""):
    RESULTS.append(ok)
    print(f"  {'ok  ' if ok else 'FAIL'}  {name:70} {detail}")


def main():
    print("position features")
    f = plstep3.FIGHTS["roark"]
    prep = plstep3.prepare(f, f["six"], f["items"])
    st = prep["st"]
    bk, flags, _ = prep["variants"][0]
    team = [f"p{i}" for i in range(6)]
    fight = plfeat.Fight(st, team, bk)
    b = pl.make_battle(st, team, bk, flags, 2)
    x, i = plfeat.features(b, fight)
    check("the arrays have the declared sizes", x.shape == (plfeat.FLOATS,) and i.shape == (plfeat.IDS,),
          (x.shape, i.shape))
    x2, i2 = plfeat.features(plplan.clone(b), fight)
    check("a copy of a position gives the same numbers", (x == x2).all() and (i == i2).all())
    rng = random.Random(3)
    b.dice, b.rng = pl.RunDice(rng), rng
    same = True
    while b.turn < 12 and b.p.alive() and b.b.alive():
        a1, _ = plfeat.features(b, fight)
        a2, _ = plfeat.features(b, fight)
        same = same and (a1 == a2).all()
        pl.play_turn(b, plplan.plain(b), rng)
    check("each position along a fight gives the same numbers twice", same)
    c = pl.make_battle(st, team, bk, flags, 2)
    base, _ = plfeat.features(c, fight)
    c.p.cur().stages["atk"] = 2
    up, _ = plfeat.features(c, fight)
    start = plfeat.FIELD_FLOATS + plfeat.SLOTS * plfeat.MON_FLOATS
    check("+2 Attack raises the active Pokemon's damage share on the trainer's active one",
          up[start] > base[start], (float(base[start]), float(up[start])))
    ids_ok = int(i.max()) < plfeat.NAME_IDS and int(i.min()) >= 0
    check("every id is inside its table", ids_ok, (int(i.min()), int(i.max())))
    print(f"\n{sum(RESULTS)}/{len(RESULTS)} passed")
    return 0 if all(RESULTS) else 1


if __name__ == "__main__":
    sys.exit(main())

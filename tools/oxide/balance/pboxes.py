"""A random nuzlocke box by the fight's split (out/design.md, "What the
reading is").

The OxiDex's box simulator (tools/oxide/encounters/simulate.py) knows the
capture areas of a run to a split, every way each can be caught, the dupes
clause and the stage a catch reaches by the cap; it plays those areas for
the best box. Ian's step 1 wants a random box, so this draws one: at each
area a random option among those open by the split, a species rolled by
that option's own odds under the dupes clause, a random starter, no
repel manipulation and no trade that costs a Pokemon.

    PYTHONPATH=~/pokeplatinum python3 boxes.py Roark 3      # three boxes
"""
import functools
import random
import sys

from ..encounters import simulate as sim


@functools.lru_cache(maxsize=None)
def context(split):
    return sim.context(split)


def random_box(split, rng):
    """[species constant] of one run's box by the split's end, each at the
    stage it reaches by the cap, the starter first."""
    ctx = context(split)
    rank, values = ctx["rank"], ctx["values"]
    box = sim.Box(ctx["root"], values)
    starter = rng.choice(ctx["starter_src"]["pool"])
    where = ctx["starter_src"].get("capture_area") or "Route 201"
    box.add(starter, where)
    drawn = set()
    for area in ctx["areas"]:
        if area["name"] == where:
            continue
        opts = [o for o in area["options"]
                if rank.get(o.split, 99) <= rank[split] and o.repel is None and not o.requires]
        if not opts:
            continue
        opt = rng.choice(opts)
        sp = sim._roll(opt, box, rng, drawn)
        if sp is None:
            continue
        if opt.kind == "legendary":
            drawn.add(sp)
        box.add(sp, area["name"])
    return [values.stage(m["species"]) for m in box.members]


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    split = argv[0] if argv else "Roark"
    n = int(argv[1]) if len(argv) > 1 else 1
    from tools.oxide.encounters import dex
    for i in range(n):
        box = random_box(split, random.Random(i))
        print(f"box {i}: {len(box)} Pokemon: " + ", ".join(dex.display_name(sp) for sp in box))
    return 0


if __name__ == "__main__":
    sys.exit(main())

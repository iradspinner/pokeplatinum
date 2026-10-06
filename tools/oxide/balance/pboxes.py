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


def planned_box(split, seed=0):
    """[species constant] of the box the encounter tool expects by the
    split's end: the simulator's best-play run (each area's best option,
    the dupes clause, no deaths), at the stage each reaches by the cap."""
    ctx = context(split)
    r = sim.run(split, seed=seed, ctx=ctx)
    return [m["stage"] for m in r["box"] if m.get("alive", True)]


def save_box(path, split):
    """[species constant] of the living Pokemon in a real save (the
    OxiDex's save reader; the graveyard boxes are left out, as the
    simulator's start_from_save reads them), at the stage each reaches by
    the split's cap."""
    from ..encounters import model, savefile
    ctx = context(split)
    save = savefile.read(path)
    start = sim.start_from_save(save, model.load_encounters(), split)
    return [ctx["values"].stage(m["species"]) for m in start["members"] if m.get("alive", True)]


IV_ORDER = ("hp", "at", "df", "sp", "sa", "sd")     # Platinum's order in the save
_SAVE_BOX = {}    # {split: [constant]}: the save box the fight was rebuilt around


def save_records(path, split, lift=False):
    """The living Pokemon of a real save as the fight setup takes them
    (fightsim.prepare's given_side): the graveyard boxes left out, as the
    simulator's start_from_save reads them. As saved (lift False), each keeps
    its level, nature, IVs, ability and real moves. Lifted to the split's cap
    (lift True), each is the stage it reaches by then, keeps its real moves,
    and has its empty slots filled by the moveset rule."""
    import collections
    from ..encounters import canon, model, savefile
    from . import pool
    ctx = context(split)
    save = savefile.read(path)
    start = sim.start_from_save(save, model.load_encounters(), split)
    dead = collections.Counter(m["species"] for m in start["members"] if not m.get("alive", True))
    cap = pool.caps()[split]
    out = []
    for m in save["party"] + save["boxes"]:
        if m.get("is_egg"):
            continue
        sp = m["species"]
        if dead[sp] > 0:
            dead[sp] -= 1
            continue
        const = ctx["values"].stage(sp) if lift else sp
        out.append({"constant": const, "species": canon.showdown_name(const), "how": "save",
                    "level": cap if lift else m["level"],
                    "nature": m.get("stat_nature") or m["nature"],
                    "ivs": dict(zip(IV_ORDER, m.get("stat_ivs") or m["ivs"])),
                    "evs": dict(zip(IV_ORDER, m["evs"])),
                    "ability": None if lift else m["ability"],
                    "moves": list(m["moves"]), "fill": lift})
    return out


def box_from(source, split, rng):
    """One box by its source: "random" (a random run), "planned" (the
    simulator's best-play run) or "save:<path>" (a real save)."""
    if source == "planned":
        return planned_box(split)
    if source.startswith(("save:", "savecap:")):
        return _SAVE_BOX.get(split) or save_box(source.split(":", 1)[1], split)
    return random_box(split, rng)


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

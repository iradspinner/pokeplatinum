"""The evolution stone census (Ian, 2026-09-27), for the item pass.

    PYTHONPATH=. python3 -m tools.oxide.balance.stones

Ian sees stones as a strong scarcity lever, and competition for a scarce
stone is intended: a player with two claimants and one stone has to
choose. So the census lists, per stone, every place the player can get one
and from which split, and every line that wants one and from which split
the player can own it. It changes nothing.

Where a stone can come from: item balls and hidden items (splits.items),
NPC gifts (splits.gifts), marts and the Game Corner's prize counter
(splits.marts), and the Underground's digs. A dig draws a treasure by
weight, with one set of weights before the National Dex and another after
(src/underground/mining.c); Oxide means to give the National Dex from the
start (element 8), so both are shown, as each stone's share of all the
weight. The Underground opens with the Explorer Kit.

Who wants one: every species whose evolution record names the stone,
whether used on it or held while it levels (the Oval Stone), with the
first split the player can own that species (pool.species_by_split).
"""
import collections
import json
import os
import re
import sys

from . import data, pool, splits

STONES = ("ITEM_FIRE_STONE", "ITEM_WATER_STONE", "ITEM_THUNDERSTONE", "ITEM_LEAF_STONE",
          "ITEM_MOON_STONE", "ITEM_SUN_STONE", "ITEM_SHINY_STONE", "ITEM_DUSK_STONE",
          "ITEM_DAWN_STONE", "ITEM_OVAL_STONE", "ITEM_ICE_STONE")
_DIG = re.compile(r"\.itemID = MINING_TREASURE_(\w+), \.oddTIDWeight = (\d+), "
                  r"\.evenTIDWeight = (\d+), \.oddTIDNatDexWeight = (\d+), "
                  r"\.evenTIDNatDexWeight = (\d+)")


def dig_weights():
    """{treasure name: (odd, even, odd with the National Dex, even with it)}."""
    with open(os.path.join(data.ROOT, "src", "underground", "mining.c"), encoding="utf-8") as f:
        text = f.read()
    return {name: tuple(int(x) for x in w) for name, *w in _DIG.findall(text)}


def dig_shares():
    """{item constant: (share without the National Dex, share with it)},
    each the mean of the odd and even trainer-id weights over all the
    weight of that kind."""
    weights = dig_weights()
    totals = [sum(w[i] for w in weights.values()) for i in range(4)]
    out = {}
    for name, w in weights.items():
        before = (w[0] / totals[0] + w[1] / totals[1]) / 2
        after = (w[2] / totals[2] + w[3] / totals[3]) / 2
        out[f"ITEM_{name}".replace("THUNDER_STONE", "THUNDERSTONE")] = (before, after)
    return out


def underground_split():
    """The split the Explorer Kit is first given in."""
    got = [s for s, _m, item in splits.gifts() if item == "ITEM_EXPLORER_KIT"]
    return min(got, key=pool.split_index) if got else None


def sources():
    """{stone: [(split, where, how)]}, earliest first."""
    out = collections.defaultdict(list)
    for split, header, item, how in splits.items():
        if item in STONES:
            out[item].append((split, header, how))
    for split, header, item in splits.gifts():
        if item in STONES:
            out[item].append((split, header, "gift"))
    for split, table, item in splits.marts():
        if item in STONES:
            out[item].append((split, table, "Game Corner" if table == "GameCornerPrizes" else "mart"))
    for item in out:
        out[item].sort(key=lambda r: (pool.split_index(r[0]), r[1]))
    return out


def claimants():
    """{stone: [(species, target, first split the species can be owned)]}."""
    first = {}
    for split in pool.SPLITS:
        for sp in pool.species_by_split()[split]:
            first.setdefault(sp, split)
    out = collections.defaultdict(list)
    base = os.path.join(data.ROOT, "res", "pokemon")
    for folder in sorted(os.listdir(base)):
        path = os.path.join(base, folder, "data.json")
        if not os.path.exists(path):
            continue
        with open(path, encoding="utf-8") as f:
            evos = json.load(f).get("evolutions") or []
        species = f"SPECIES_{folder.upper()}"
        for evo in evos:
            if not isinstance(evo, list):
                continue
            target = next((x for x in evo if isinstance(x, str) and x.startswith("SPECIES_")), None)
            for x in evo:
                if x in STONES and target:
                    out[x].append((species, target, first.get(species)))
    return out


def main(argv=None):
    src, want, shares = sources(), claimants(), dig_shares()
    dig = underground_split()
    for stone in STONES:
        if not src.get(stone) and not want.get(stone) and stone not in shares:
            continue
        print(f"{stone.replace('ITEM_', '').replace('_', ' ').title()}")
        for split, where, how in src.get(stone, []):
            print(f"    {str(split):10} {how:12} {where}")
        if stone in shares:
            before, after = shares[stone]
            print(f"    {str(dig):10} {'dig':12} {before:.1%} of digs, {after:.1%} with the "
                  f"National Dex")
        for species, target, split in sorted(want.get(stone, []),
                                             key=lambda r: (pool.split_index(r[2]), r[0])):
            print(f"      wanted by {species.replace('SPECIES_', '').title()} for "
                  f"{target.replace('SPECIES_', '').title()}, owned from {split or 'never'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

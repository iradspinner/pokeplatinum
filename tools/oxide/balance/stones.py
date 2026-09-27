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


# A gift the split map places by its map but the script gates on a story
# flag, with the split the flag is first set in. Route 207's woman gives all
# nine stones at once, once the player has travelled with Mira through
# Wayward Cave (FLAG_TRAVELED_WITH_MIRA), which the bike opens in Fantina's
# split.
GIFT_GATES = {"ROUTE_207": ("Fantina", "all nine at once, after travelling with Mira")}


def underground_split():
    """The split the Explorer Kit is first given in."""
    got = [s for s, _m, item in splits.gifts() if item == "ITEM_EXPLORER_KIT"]
    return min(got, key=pool.split_index) if got else None


def hidden_items():
    """[(split, maps, item)], one per hidden item. A hidden item on the
    border of two maps is listed in both maps' events under one script,
    and so one flag: it is one item, found from whichever map the player
    reaches first (Route 211 west's Moon Stone is Eterna City's)."""
    flags = dict(splits._FLAG.findall(splits._read("build", "generated", "vars_flags.h")))
    start = int(flags["HIDDEN_ITEM_FLAGS_START"])
    hidden = {int(flags[flag]) - start: item for item, flag in
              splits._HIDDEN.findall(splits._read("include", "data", "field", "hidden_items.h"))}
    by_script = {}
    for header, fields in splits.headers().items():
        events = fields.get("eventsArchiveID")
        path = os.path.join(data.ROOT, "res", "field", "events", f"{events}.json") if events else None
        if not path or not os.path.exists(path):
            continue
        with open(path, encoding="utf-8") as f:
            ev = json.load(f)
        split = splits.map_split(header)[0]
        for bg in ev.get("bg_events", []):
            script = bg.get("script")
            if bg.get("type") == splits.BG_HIDDEN_ITEM and isinstance(script, int):
                row = by_script.setdefault(script, [None, [], hidden.get(script - splits.HIDDEN_ITEM_SCRIPT)])
                row[1].append(header)
                if split in pool.SPLITS and (row[0] is None
                                             or pool.split_index(split) < pool.split_index(row[0])):
                    row[0] = split
    return [(s, sorted(set(maps)), item) for s, maps, item in by_script.values()]


def sources():
    """{stone: [(split, where, how)]}, earliest first, each item once."""
    out = collections.defaultdict(list)
    for split, header, item, how in splits.items():
        if item in STONES and how != "hidden":
            out[item].append((split, header, how))
    for split, maps, item in hidden_items():
        if item in STONES:
            out[item].append((split, " and ".join(maps), "hidden"))
    for split, header, item in splits.gifts():
        if item in STONES:
            gate = GIFT_GATES.get(header)
            out[item].append((gate[0], f"{header} ({gate[1]})", "gift") if gate
                             else (split, header, "gift"))
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


# Ian's rulings on the census (2026-09-27): the Underground closes (the
# player is never given the Explorer Kit), and both bulk stone sets go,
# Route 207's nine and Galactic HQ B2F's.
REMOVED = {("ROUTE_207", "gift"), ("GALACTIC_HQ_B2F", "ball")}
_TREASURE = re.compile(r"\[(\d+)\] = (ITEM_\w+),")


def underground_items():
    """Every item the Underground hands out: its digs, and its treasure
    vendors, which sell from the same list (src/underground.c)."""
    with open(os.path.join(data.ROOT, "src", "underground.c"), encoding="utf-8") as f:
        text = f.read()
    body = text[text.index("sMiningItems"):]
    body = body[:body.index("};")]
    return [item for _i, item in _TREASURE.findall(body)]


def elsewhere():
    """{item: [(split, where, how)]} for each Underground item, from every
    source but the Underground and the two bulk stone sets Ian removed."""
    wanted = set(underground_items())
    out = {item: [] for item in underground_items()}
    rows = ([(s, h, it, how) for s, h, it, how in splits.items() if how != "hidden"]
            + [(s, " and ".join(maps), it, "hidden") for s, maps, it in hidden_items()]
            + [(s, h, it, "gift") for s, h, it in splits.gifts()]
            + [(s, t, it, "Game Corner" if t == "GameCornerPrizes" else "mart")
               for s, t, it in splits.marts()])
    for split, where, item, how in rows:
        if item in wanted and not (item in STONES and (where, how) in REMOVED):
            out[item].append((split, where, how))
    for item in out:
        out[item].sort(key=lambda r: (pool.split_index(r[0]), r[1]))
    return out


def report_underground(items=()):
    """One line per Underground item, or every source of each item named."""
    for item, rows in elsewhere().items():
        name = item.replace("ITEM_", "").replace("_", " ").title()
        if items:
            if item in items:
                print(name)
                for split, where, how in rows:
                    print(f"    {str(split):10} {how:12} {where}")
            continue
        if not rows:
            print(f"{name:14} only in the Underground")
            continue
        first = rows[0]
        print(f"{name:14} {len(rows):>2} elsewhere, first {first[0]} ({first[2]}, {first[1]})")


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    if "--underground" in argv:
        report_underground([a for a in argv if a.startswith("ITEM_")])
        return 0
    src, want, shares = sources(), claimants(), dig_shares()
    dig = underground_split()
    for stone in STONES:
        if not src.get(stone) and not want.get(stone) and stone not in shares:
            continue
        kept = [r for r in src.get(stone, []) if r[0] in pool.SPLITS
                and not any(r[1].startswith(m) and r[2] == how for m, how in REMOVED)]
        print(f"{stone.replace('ITEM_', '').replace('_', ' ').title()}: {len(kept)} before the "
              f"League once the Underground and the bulk sets are gone")
        for split, where, how in src.get(stone, []):
            print(f"    {str(split):10} {how:12} {where}")
        if stone in shares and any(shares[stone]):
            before, after = shares[stone]
            print(f"    {str(dig):10} {'dig':12} {before:.1%} of digs, {after:.1%} with the "
                  f"National Dex, with no limit")
        for species, target, split in sorted(want.get(stone, []),
                                             key=lambda r: (pool.split_index(r[2]), r[0])):
            print(f"      wanted by {species.replace('SPECIES_', '').title()} for "
                  f"{target.replace('SPECIES_', '').title()}, owned from {split or 'never'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

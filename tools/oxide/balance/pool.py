"""B3: the player's side at each split.

    PYTHONPATH=. python3 -m tools.oxide.balance.pool [split]

For each split, every species the player can own by its end, each at the
split's cap with average IVs (15), no EVs (Oxide gives none from battling)
and a neutral nature, holding the best attacking item the player can have by
then and knowing every damaging move it can know by then. That is the plan's
"player's side": what a nuzlocke could bring, not what one run does bring.

Where each piece comes from:

- Species. The encounter tables, each counted from its own split (the
  encounter design's), for land, the day and night slots, and water, which
  also waits for the rod or for Surf. Honey trees count from Gardenia's
  split, where the first Honey is. The scripted sources are
  docs/oxide/pokemon-sources.csv (starters, gifts, trades, statics, fossils,
  roamers), each at its location's split, and left out when its level is
  above that split's cap. Swarms, the Poke Radar, the GBA slots and the
  Trophy Garden dailies are never used (Ian, 2026-09-21), so they are not
  sources. Then every evolution reachable at the cap, by the encounter
  tool's own rule (evolve.py): a level, or its judged level for a stone,
  trade or friendship.
- Moves. The level-up moves of the species and of every earlier stage at or
  below the cap, the TMs and HMs the player has by then (B1d's item map),
  and the tutors whose house is reachable by then. Egg moves are left out.
- The item. The strongest general damage item the split offers, among the
  Choice items, Life Orb, Expert Belt, the type boosters and plates, and
  Muscle Band and Wise Glasses (best_item says how it picks).
- The ability is the species' first.

The caps are the closing bosses' aces in the tree, as B2 reads them
(Maylene 39, the League 78).
"""
import collections
import csv
import functools
import json
import os
import sys

from ..encounters import calc_export, calc_trainers, canon, evolve, model, pokedex, progression
from . import data, splits

SPLITS = [s for s in splits.SPLITS if s != "Post"]   # post-game has no cap
AVERAGE_IV = 15
CLOSING = {"Roark": "roark", "Gardenia": "gardenia", "Fantina": "fantina",
           "Maylene": "maylene", "Wake": "wake", "Byron": "byron",
           "Candice": "candice", "Volkner": "volkner", "League": "cynthia"}
LAND_KEYS = ("land_encounters", "day", "night")
HONEY_SPLIT = "Gardenia"
SOURCES = os.path.join(data.ROOT, "docs", "oxide", "pokemon-sources.csv")
TUTOR_MAPS = {"TUTOR_LOCATION_ROUTE_212": "ROUTE_212_HOUSE",
              "TUTOR_LOCATION_SNOWPOINT_CITY": "SNOWPOINT_CITY_EAST_HOUSE",
              "TUTOR_LOCATION_SURVIVAL_AREA": "SURVIVAL_AREA_NORTH_HOUSE"}

# Held items that raise damage, by calculator name. A type booster and its
# plate do the same in Generation 4, so either counts.
TYPE_ITEMS = {
    "Normal": ["Silk Scarf"], "Fighting": ["Black Belt", "Fist Plate"],
    "Flying": ["Sharp Beak", "Sky Plate"], "Poison": ["Poison Barb", "Toxic Plate"],
    "Ground": ["Soft Sand", "Earth Plate"], "Rock": ["Hard Stone", "Stone Plate", "Rock Incense"],
    "Bug": ["Silver Powder", "Insect Plate"], "Ghost": ["Spell Tag", "Spooky Plate"],
    "Steel": ["Metal Coat", "Iron Plate"], "Fire": ["Charcoal", "Flame Plate"],
    "Water": ["Mystic Water", "Splash Plate", "Sea Incense", "Wave Incense"],
    "Grass": ["Miracle Seed", "Meadow Plate", "Rose Incense"],
    "Electric": ["Magnet", "Zap Plate"], "Psychic": ["Twisted Spoon", "Mind Plate", "Odd Incense"],
    "Ice": ["Never-Melt Ice", "Icicle Plate"], "Dragon": ["Dragon Fang", "Draco Plate"],
    "Dark": ["Black Glasses", "Dread Plate"],
}


def split_index(split):
    return SPLITS.index(split) if split in SPLITS else len(SPLITS)


def later(*names):
    """The latest of some splits, or None if any is unknown."""
    if any(n not in SPLITS for n in names):
        return None
    return max(names, key=split_index)


@functools.lru_cache(maxsize=None)
def caps():
    """{split: cap}: each split's closing boss's ace in the tree."""
    by_key = {f["key"]: f for f in data.fights()["fights"]}
    out = {}
    for split, key in CLOSING.items():
        parties = [t["party"] for t in data.fight_trainers("oxide", by_key[key])]
        out[split] = max(m["level"] for p in parties for m in p)
    return out


@functools.lru_cache(maxsize=None)
def _location_splits():
    """{location name: its earliest split} over every map with that name."""
    out = {}
    for header in splits.headers():
        name, split = splits.location_name(header), splits.map_split(header)[0]
        if name and split in SPLITS:
            if name not in out or split_index(split) < split_index(out[name]):
                out[name] = split
    return out


@functools.lru_cache(maxsize=None)
def caught():
    """{species constant: (split, how)}: the first split each species can be
    caught or received in, before any evolution."""
    sidecar = model.load_sidecar() or {}
    area_split = progression.split_of(sidecar)
    entries = sidecar.get("areas") or {}
    first = {}

    def offer(species, split, how):
        if split not in SPLITS:
            return
        if species not in first or split_index(split) < split_index(first[species][0]):
            first[species] = (split, how)

    for area in model.load_all():
        split = area_split.get(area.name)
        if not split:
            continue
        ref = area.reference_species()
        for key in LAND_KEYS:
            for sp in ref.get(key) or []:
                offer(sp, split, "wild")
        water = (entries.get(area.name) or {}).get("water_split") or split
        for kind in ("surf", "old_rod", "good_rod", "super_rod"):
            arrives = later(water, progression.rod_split(sidecar, kind))
            for sp in ref.get(kind + "_encounters") or []:
                offer(sp, arrives, kind)
    for key, vals in model.honey_tree_species().items():
        for sp in vals:
            offer(sp, HONEY_SPLIT, "honey")
    locs = _location_splits()
    cap = caps()
    with open(SOURCES, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            split = locs.get(row["location"])
            level = int(row["level"]) if row["level"].isdigit() else 0
            if split and cap.get(split) and level <= cap[split]:
                offer(row["species"], split, row["method"])
    return first


@functools.lru_cache(maxsize=None)
def pre_evolutions():
    """{species: [its earlier stages]}, from every species' evolutions."""
    parent = {}
    for sp in pokedex.species_list(data.ROOT):
        for _need, target in evolve.evolutions(data.ROOT, sp):
            parent.setdefault(target, sp)
    out = {}
    for sp in pokedex.species_list(data.ROOT):
        chain, cur = [], parent.get(sp)
        while cur and cur not in chain and cur != sp:
            chain.append(cur)
            cur = parent.get(cur)
        out[sp] = chain
    return out


@functools.lru_cache(maxsize=None)
def species_by_split():
    """{split: {species constant: how}}: everything owned by each split's end,
    evolutions reached at its cap included."""
    first = caught()
    cap = caps()
    out = {}
    for split in SPLITS:
        have = {sp: how for sp, (s, how) in first.items() if split_index(s) <= split_index(split)}
        todo = list(have)
        while todo:
            sp = todo.pop()
            for need, target in evolve.evolutions(data.ROOT, sp):
                if need <= cap[split] and target not in have:
                    have[target] = "evolved"
                    todo.append(target)
        out[split] = have
    return out


@functools.lru_cache(maxsize=None)
def _items_first():
    """{item constant: the first split the player can hold it in}."""
    first = {}
    rows = ([(s, it) for s, _m, it, _how in splits.items()]
            + [(s, it) for s, _m, it in splits.gifts()]
            + [(s, it) for s, _t, it in splits.marts()])
    for split, item in rows:
        if item and split in SPLITS:
            if item not in first or split_index(split) < split_index(first[item]):
                first[item] = split
    return first


@functools.lru_cache(maxsize=None)
def items_by_split():
    """{split: {calculator item name}} held by the end of each split."""
    first = _items_first()
    out = {}
    for split in SPLITS:
        names = {calc_trainers._item_name(it) for it, s in first.items()
                 if split_index(s) <= split_index(split)}
        out[split] = {n for n in names if n}
    return out


@functools.lru_cache(maxsize=None)
def _tutor_splits():
    """{move constant: the first split one of its tutors is reachable in}."""
    with open(os.path.join(data.ROOT, "res", "pokemon", "move_tutors.json"), encoding="utf-8") as f:
        rows = json.load(f)
    out = {}
    for row in rows:
        split = splits.map_split(TUTOR_MAPS[row["location"]])[0]
        if split in SPLITS and (row["move"] not in out
                                or split_index(split) < split_index(out[row["move"]])):
            out[row["move"]] = split
    return out


@functools.lru_cache(maxsize=None)
def _move_names():
    """{MOVE_ constant: the name the calculator's data uses}."""
    out = {}
    for rec in pokedex.moves(data.ROOT).values():
        if rec["move"] != "MOVE_NONE" and rec["name"] not in ("-", ""):
            out[rec["move"]] = calc_export.move_name(rec) or rec["name"]
    return out


def moves_at(species, split):
    """Every move constant the species can know by the end of the split."""
    cap = caps()[split]
    tms = {m: s for m, s in ((it.replace("ITEM_", ""), s) for it, s in _items_first().items())
           if m.startswith(("TM", "HM"))}
    machines = pokedex.machines(data.ROOT)
    tutors = _tutor_splits()
    out = set()
    for stage in [species] + pre_evolutions().get(species, []):
        rec = pokedex.load(data.ROOT, stage)
        if rec is None:
            continue
        out |= {mv for lvl, mv in rec["learnset"] if lvl <= cap}
    rec = pokedex.load(data.ROOT, species)
    if rec:
        for machine in rec["by_tm"]:
            if machine in tms and split_index(tms[machine]) <= split_index(split) and machine in machines:
                out.add(machines[machine])
        for mv in rec["by_tutor"]:
            if mv in tutors and split_index(tutors[mv]) <= split_index(split):
                out.add(mv)
    return out


def best_item(stats, move_types, items):
    """The one held item that raises this Pokemon's damage most, of those
    the split offers: a Choice item for its stronger attacking side (x1.5),
    else Life Orb (x1.3), else a booster for its best STAB type or Expert
    Belt (x1.2), else Muscle Band or Wise Glasses (x1.1). `move_types` is
    [(type, category, power)] of its damaging moves, strongest first."""
    physical = stats["at"] >= stats["sa"]
    choice = "Choice Band" if physical else "Choice Specs"
    if choice in items:
        return choice
    if "Life Orb" in items:
        return "Life Orb"
    for t, _cat, _bp in move_types:
        for it in TYPE_ITEMS.get(t, []):
            if it in items:
                return it
    if "Expert Belt" in items:
        return "Expert Belt"
    small = "Muscle Band" if physical else "Wise Glasses"
    return small if small in items else None


# Moves whose listed damage cannot be relied on in a straight exchange: they
# need a status, a hit taken or a berry first, work only on the first turn,
# or do something other than damage. Left out on both sides.
UNRELIABLE = {"Dream Eater", "Focus Punch", "Fake Out", "First Impression", "Snore",
              "Last Resort", "Belch", "Synchronoise", "Spit Up", "Natural Gift", "Fling",
              "Future Sight", "Doom Desire", "Counter", "Mirror Coat", "Metal Burst",
              "Bide", "Endeavor", "Final Gambit", "Present", "Beat Up", "Sky Drop",
              "Shell Trap", "Upper Hand", "Spite", "Magnitude",
              "Sheer Cold", "Fissure", "Guillotine", "Horn Drill"}
# Hidden Power's type and power come from the IVs, and the pool's are all 15,
# which would make every one a 70-power Dark move; a real one is a lottery.
PLAYER_ONLY_EXCLUDED = {"Hidden Power"}
# Moves that knock the user out. A boss's Explosion still ends a nuzlocke
# Pokemon, so it counts against the player; the player's is no answer.
SACRIFICE = {"Explosion", "Self-Destruct", "Selfdestruct", "Memento", "Misty Explosion"}
CONDITIONAL = UNRELIABLE | SACRIFICE | PLAYER_ONLY_EXCLUDED


def damaging_moves(names, blob, keep=2):
    """The damaging moves worth trying, strongest two per type and category
    (plus any whose power the calculator works out, such as Low Kick), from
    a list of calculator move names. Fewer candidates keep the run short;
    the third-strongest move of one type never beats the first."""
    by_kind = collections.defaultdict(list)
    variable = []
    for n in names:
        rec = blob["moves"].get(n)
        if not rec or rec.get("category") == "Status" or n in CONDITIONAL:
            continue
        bp = rec.get("basePower", rec.get("bp")) or 0
        if bp <= 1:
            variable.append(n)
        else:
            by_kind[(rec["type"], rec["category"])].append((bp, n))
    out = []
    for kind, rows in by_kind.items():
        out += [n for _bp, n in sorted(rows, reverse=True)[:keep]]
    return sorted(out) + sorted(variable)


def pool(split, blob):
    """[{species, name, level, ability, item, nature, ivs, evs, moves, how}]."""
    cap = caps()[split]
    items = items_by_split()[split]
    names = _move_names()
    out = []
    for sp, how in sorted(species_by_split()[split].items()):
        name = canon.showdown_name(sp)
        if not name or name not in blob["poks"]:
            continue
        rec = pokedex.load(data.ROOT, sp)
        moves = damaging_moves(sorted({names[m] for m in moves_at(sp, split) if m in names}), blob)
        stats = blob["poks"][name]["bs"]
        kinds = sorted(((blob["moves"][m]["type"], blob["moves"][m]["category"],
                         blob["moves"][m].get("basePower") or 0) for m in moves),
                       key=lambda k: -k[2] * (1.5 if k[0] in blob["poks"][name]["types"] else 1))
        abilities = blob["poks"][name].get("abilities") or {}
        iv = {k: AVERAGE_IV for k in ("hp", "at", "df", "sa", "sd", "sp")}
        out.append({
            "species": name, "constant": sp, "how": how, "level": cap,
            "ability": abilities.get("0"), "item": best_item(stats, kinds, items),
            "nature": "Hardy", "ivs": iv, "evs": {k: 0 for k in iv}, "moves": moves,
        })
    return out


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    blob = calc_export.build()
    for split in (argv or SPLITS):
        p = pool(split, blob)
        by_how = collections.Counter(m["how"] for m in p)
        print(f"{split:9} cap {caps()[split]:>2}: {len(p)} species "
              f"({', '.join(f'{n} {h}' for h, n in by_how.most_common())}); "
              f"items {len(items_by_split()[split])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

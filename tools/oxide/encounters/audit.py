"""The leak audit and the availability coverage. Authoring plan Step 0.

Two questions the authoring pass keeps asking, answered from the tree:

  * **audit**: where does every species reference live, and is it on the
    pick-list? A reference to an off-list species anywhere the game can
    roll one -- a land slot, a rod, a swarm, the radar, a dual-slot list, a
    honey tree, the marsh binoculars, the garden's daily visitor -- is a
    leak: a species the list calls unobtainable, obtainable. Scripts that
    hand over or battle a species are listed too, but reported rather than
    counted, since they are outside the encounter track (decision 8).

  * **coverage**: for every evolution line on the pick-list, where can the
    player get it? A wild *home* (decision 3: a live land table where the
    line's first stage holds at least 10% of the merged share), cameos,
    water, the other keys, a gift script, an in-game trade, or nothing.
    This is R12's input made visible, and Step 2's availability plan is
    written from it.

Pure data in, dicts out; the CLI formats.
"""
import collections
import glob
import os
import re

from . import analysis as A
from . import dex
from . import model

# Script commands that put a species in the player's hands or in front of
# them. Cries, previews and dex flags name species too and are not leaks.
GIVE_COMMANDS = ("GivePokemon", "GiveEgg", "GivePokemonWithMoves")
BATTLE_COMMANDS = ("StartWildBattle", "StartLegendaryBattle",
                   "StartGiratinaOriginBattle", "StartFatefulEncounter")
SCRIPT_COMMANDS = GIVE_COMMANDS + BATTLE_COMMANDS
_SCRIPT_RE = re.compile(r"^\s*(" + "|".join(SCRIPT_COMMANDS) + r")\s+(SPECIES_[A-Z0-9_]+)")

GIFTS_CSV = os.path.join("docs", "oxide", "pokemon-gifts.csv")
TRADES_DIR = os.path.join("res", "npc_trades")

# Scripts that hand over a species chosen at runtime, which the grep cannot
# see: the starter on Route 201 (GivePokemon 32768 is a variable) and the
# Mining Museum's fossil revival (VAR_REVIVED_POKEMON_SPECIES). Decision 3
# counts both as acquisition paths.
SCRIPTED = {
    "SPECIES_TURTWIG": "starter, route_201",
    "SPECIES_CHIMCHAR": "starter, route_201",
    "SPECIES_PIPLUP": "starter, route_201",
    "SPECIES_OMANYTE": "fossil, mining_museum",
    "SPECIES_KABUTO": "fossil, mining_museum",
    "SPECIES_AERODACTYL": "fossil, mining_museum",
    "SPECIES_LILEEP": "fossil, mining_museum",
    "SPECIES_ANORITH": "fossil, mining_museum",
    "SPECIES_CRANIDOS": "fossil, mining_museum",
    "SPECIES_SHIELDON": "fossil, mining_museum",
    # Platinum's roamers are released by an event and then walk the routes;
    # no script names them. Mesprit after Valor Cavern, Cresselia from
    # Fullmoon Island, the three birds from Oak in Eterna after the League.
    "SPECIES_MESPRIT": "roamer, valor_cavern",
    "SPECIES_CRESSELIA": "roamer, fullmoon_island",
    "SPECIES_ARTICUNO": "roamer, eterna_city (Oak, post-League)",
    "SPECIES_ZAPDOS": "roamer, eterna_city (Oak, post-League)",
    "SPECIES_MOLTRES": "roamer, eterna_city (Oak, post-League)",
    # and Phione is bred from the Manaphy egg the mansion's office gives
    "SPECIES_PHIONE": "bred from Manaphy, pokemon_day_care",
}

HOME_SHARE = 0.10


def on_list(root):
    """{constant: pick-list row} for every row the tree can resolve. Rows
    marked `cut` are off the list by definition; `new` rows have no
    constant yet and cannot be referenced, so they cannot leak."""
    out = {}
    for row in dex.pick_list(root):
        if row["status"] == "cut" or not row["constant"]:
            continue
        out[row["constant"]] = row
    return out


# -- audit ------------------------------------------------------------------


def references(ref=None):
    """[{file, key, index, species, live}] for every species reference in
    every encounter file, in file order."""
    rows = []
    for a in model.load_all(ref):
        for key, vals in a.reference_species().items():
            for i, sp in enumerate(vals):
                rows.append({"file": a.name, "key": key, "index": i,
                             "species": sp, "live": a.land_active})
    return rows


def script_references(root):
    """[{script, line, command, species}] for the commands in SCRIPT_COMMANDS
    whose species operand is a constant. Operands that are variables (the
    starter, the revived fossil) are decided at runtime and are not listed."""
    rows = []
    for path in sorted(glob.glob(os.path.join(root, "res", "field", "scripts", "*.s"))):
        with open(path, encoding="utf-8", errors="replace") as f:
            for n, line in enumerate(f, 1):
                m = _SCRIPT_RE.match(line)
                if m:
                    rows.append({"script": os.path.basename(path)[:-2],
                                 "line": n, "command": m.group(1),
                                 "species": m.group(2)})
    return rows


def audit(ref=None):
    root = model.repo_root()
    listed = on_list(root)
    rows = references(ref)
    for r in rows:
        r["on_list"] = r["species"] in listed
    scripts = script_references(root)
    for r in scripts:
        r["on_list"] = r["species"] in listed

    by_key = collections.OrderedDict()
    for r in rows:
        d = by_key.setdefault(r["key"], {"refs": 0, "off": 0, "off_species": set()})
        d["refs"] += 1
        if not r["on_list"]:
            d["off"] += 1
            d["off_species"].add(r["species"])
    for d in by_key.values():
        d["off_species"] = len(d["off_species"])

    files = {r["file"] for r in rows}
    leaking_files = {r["file"] for r in rows if not r["on_list"]}
    all_species = {r["species"] for r in rows}
    live_land = [r for r in rows if r["key"] == "land_encounters" and r["live"]]
    live_land_species = {r["species"] for r in live_land}
    natives = set(listed)
    return {
        "rows": rows,
        "scripts": scripts,
        "summary": {
            "files": len(files),
            "files_with_leak": len(leaking_files),
            "references": len(rows),
            "off_list_references": sum(1 for r in rows if not r["on_list"]),
            "distinct_species": len(all_species),
            "distinct_off_list": len(all_species - natives),
            "live_land_slots": len(live_land),
            "live_land_slots_off_list": sum(1 for r in live_land if not r["on_list"]),
            "natives": len(natives),
            "natives_in_no_live_land_table": len(natives - live_land_species),
            "natives_in_no_source": len(natives - all_species),
            "by_key": by_key,
            "script_references": len(scripts),
            "script_off_list": sum(1 for r in scripts if not r["on_list"]),
        },
    }


# -- coverage ---------------------------------------------------------------


def gifts(root):
    """[{map, command, species}] from pokemon-gifts.csv, the survey of every
    GivePokemon / GiveEgg the base ROM's scripts reach."""
    import csv
    path = os.path.join(root, GIFTS_CSV)
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8", newline="") as f:
        return [{"map": r["map"], "command": r["command"], "species": r["species"]}
                for r in csv.DictReader(f) if r.get("species", "").startswith("SPECIES_")]


def trades(root):
    """[{name, species, wants}] from res/npc_trades: what the NPC hands over
    and what it asks for."""
    import json
    out = []
    for path in sorted(glob.glob(os.path.join(root, TRADES_DIR, "*.json"))):
        with open(path, encoding="utf-8") as f:
            d = json.load(f)
        out.append({"name": os.path.basename(path)[:-5], "species": d["species"],
                    "wants": d.get("requestedSpecies")})
    return out


def acquisition_costs(areas, wanted):
    """{species: (cost, area, kind, lead_level)}: the cheapest place to meet
    each wanted species, over every live table kind and every repel rung.

    Cost is expected encounters to the first one that is the species: the
    reciprocal of its share of the surviving pool at the best rung (design
    doc 2.4, with an empty party: nothing duped out yet). Water slots hold a
    level range, so their rungs admit fractions of a slot; analysis.pool
    handles that.
    """
    best = {}
    for a in areas:
        for kind in a.kinds_present():
            slots = a.kind_slots(kind)
            rates = A.TABLE_KINDS[kind][2]
            for lead, pool in A.distinct_rungs(slots, rates):
                for sp, share in pool.items():
                    if sp in wanted and share > 0:
                        cost = 1.0 / share
                        if sp not in best or cost < best[sp][0]:
                            best[sp] = (cost, a.name, kind, lead)
    return best


def availability(ref=None):
    """R12's input: one row per native line on the pick-list with its tier,
    whether it has a scripted source, and its cheapest wild acquisition.
    Returns None when the pick-list has no `tier` column yet, which is the
    signal for the rule to report itself skipped."""
    root = model.repo_root()
    if not any(r.get("tier") for r in dex.pick_list(root)):
        return None
    cov = coverage(ref)
    areas = [a for a in model.load_all(ref) if a.land_active]
    wanted = {sp for line in cov["lines"] for sp in line["base"]}
    costs = acquisition_costs(areas, wanted)
    out = []
    for line in cov["lines"]:
        cheapest = min((costs[sp] for sp in line["base"] if sp in costs),
                       default=None)
        # A honey-tree placement is a source the cost model cannot price (a
        # tree is slathered, waited on, and rolled by rarity tier), so it is
        # carried as its own flag; the plan uses the rare tier for the grass
        # starters and R12 accepts it.
        honey = sorted({key for _, key, _ in line["other"]
                        if key in model.HONEY_TREE_KEYS})
        out.append({
            "name": line["name"], "line": line["line"], "tier": line["tier"],
            "non_wild": bool(line["gifts"] or line["trades"] or line["static"]
                             or line["scripted"]),
            "honey": honey,
            "cost": cheapest[0] if cheapest else None,
            "where": cheapest[1:] if cheapest else None,
        })
    return out


def coverage(ref=None):
    root = model.repo_root()
    listed = on_list(root)
    line_of = dex.lines(root)
    rows = dex.pick_list(root)

    # Group the natives by evolution line. A line's members on the list are
    # what the player is promised; its base stage is what a wild home holds.
    by_line = collections.OrderedDict()
    for row in rows:
        c = row["constant"]
        if row["status"] == "cut" or not c:
            continue
        by_line.setdefault(line_of.get(c, c), []).append(row)

    areas = [a for a in model.load_all(ref) if a.land_active]
    land_share = {}      # (area, species) -> merged land share
    other = collections.defaultdict(list)   # species -> [(area, key)]
    for a in areas:
        for sp, share in A.merged(a.slots).items():
            land_share[(a.name, sp)] = share
        for key, vals in a.reference_species().items():
            if key == "land_encounters":
                continue
            for sp in set(vals):
                other[sp].append((a.name, key))
    for name, reader in ((model.HONEY_TREE, model.honey_tree_species),
                         (model.GREAT_MARSH_LOOKOUT, model.great_marsh_lookout_species)):
        for key, vals in reader(ref).items():
            for sp in set(vals):
                other[sp].append((name, key))
    gift_rows, trade_rows = gifts(root), trades(root)
    static_rows = [r for r in script_references(root) if r["command"] in BATTLE_COMMANDS]
    water_keys = {k for k, (key, _, _) in A.TABLE_KINDS.items() if k != "land"}
    water_json = {A.TABLE_KINDS[k][0] for k in water_keys}

    out = []
    for line_id, members in by_line.items():
        consts = [m["constant"] for m in members]
        bases = dex.line_base(root, line_id)
        home, cameo = [], []
        for (area, sp), share in land_share.items():
            if sp in bases and share >= HOME_SHARE:
                home.append((area, round(share, 3)))
            elif sp in consts or sp in bases:
                cameo.append((area, sp, round(share, 3)))
        water, extra = [], []
        for sp in consts:
            for area, key in other.get(sp, []):
                (water if key in water_json else extra).append((area, key, sp))
        g = [(r["map"], r["command"], r["species"]) for r in gift_rows if r["species"] in consts]
        t = [(r["name"], r["species"]) for r in trade_rows if r["species"] in consts]
        st = [(r["script"], r["command"], r["species"]) for r in static_rows
              if r["species"] in consts]
        sc = [(SCRIPTED[sp], sp) for sp in consts if sp in SCRIPTED]
        if home:
            status = "home"
        elif g or t or st or sc:
            status = "non-wild"
        elif water:
            status = "water-only"
        elif cameo:
            status = "cameo-only"
        elif extra:
            status = "other-only"
        else:
            status = "none"
        tier = next((m["tier"] for m in members if m.get("tier")), "")
        out.append({
            "line": line_id, "name": dex.display_name(bases[0]),
            "base": bases, "members": consts, "tier": tier, "status": status,
            "home": sorted(home, key=lambda r: -r[1]),
            "cameo": sorted(cameo), "water": sorted(set(water)),
            "other": sorted(set(extra)), "gifts": sorted(set(g)), "trades": sorted(set(t)),
            "static": sorted(set(st)), "scripted": sorted(set(sc)),
        })
    new = [{"line": None, "name": r["name"], "base": [], "members": [],
            "tier": r.get("tier", ""), "status": "new", "home": [], "cameo": [],
            "water": [], "other": [], "gifts": [], "trades": [], "static": [],
            "scripted": []}
           for r in rows if r["status"] == "new"]
    counts = collections.Counter(r["status"] for r in out)
    return {
        "lines": out,
        "new": new,
        "summary": {
            "native_lines": len(out),
            "new_species": len(new),
            # rows the tree cannot resolve: 159 before Phase 4 element 3, 0 after
            "not_in_tree": sum(1 for r in rows if r["status"] != "cut" and not r["constant"]),
            "by_status": dict(counts),
            "with_wild_home": counts.get("home", 0),
            "with_non_wild_source_only": counts.get("non-wild", 0),
            "with_nothing": counts.get("none", 0),
        },
    }

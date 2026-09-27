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
import json
import os
import re

from . import analysis as A
from . import dex
from . import model

# Script commands that put a species in the player's hands or in front of
# them. Cries, previews and dex flags name species too and are not leaks.
GIVE_COMMANDS = ("GivePokemon", "GiveEgg", "GivePokemonWithMoves",
                 # Platinum Oxide: a gift with a chosen nature, IVs and shininess
                 "GiveDesignedPokemon")
BATTLE_COMMANDS = ("StartWildBattle", "StartLegendaryBattle",
                   "StartGiratinaOriginBattle", "StartFatefulEncounter")
SCRIPT_COMMANDS = GIVE_COMMANDS + BATTLE_COMMANDS
_SCRIPT_RE = re.compile(r"^\s*(" + "|".join(SCRIPT_COMMANDS) + r")\s+(SPECIES_[A-Z0-9_]+)")

GIFTS_CSV = os.path.join("docs", "oxide", "pokemon-gifts.csv")
TRADES_DIR = os.path.join("res", "npc_trades")

# Scripts that hand over a species chosen at runtime, which the grep cannot
# see: the starter (GivePokemon 32768 is a variable; its three choices are
# read from scripted.json, see starters()) and the Mining Museum's fossil
# revival (VAR_REVIVED_POKEMON_SPECIES). Decision 3 counts both as
# acquisition paths.
SCRIPTED = {
    "SPECIES_OMANYTE": "fossil, mining_museum",
    "SPECIES_KABUTO": "fossil, mining_museum",
    "SPECIES_AERODACTYL": "fossil, mining_museum",
    "SPECIES_LILEEP": "fossil, mining_museum",
    "SPECIES_ANORITH": "fossil, mining_museum",
    "SPECIES_CRANIDOS": "fossil, mining_museum",
    "SPECIES_SHIELDON": "fossil, mining_museum",
    # Platinum's roamers are released by an event and then walk the routes;
    # no script names them. Cresselia from Fullmoon Island, the three birds
    # from Oak in Eterna after the League. Mesprit's roamer, released at
    # Verity Cavern, is the legendary pool's roamer draw, which Ian turned off
    # on 2026-09-27; Mesprit waits in that third, held back (empty_thirds).
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


# Script sources that the script itself makes unreachable, which a scan of
# commands cannot tell: (script, species) with Ian's reason. The sources
# catalogue (tools/oxide/pokemon_sources.py) honours this list too.
UNREACHABLE_SCRIPT_SOURCES = {
    ("scripts_stark_mountain_room_3", "SPECIES_HEATRAN"):
        "Stark Mountain's last room is empty (Ian, 2026-09-27); the script "
        "jumps past the line that would unhide Heatran",
    ("scripts_valor_cavern", "SPECIES_AZELF"):
        "Valor Cavern holds no legendary (Ian, 2026-09-27); its transition "
        "script sets FLAG_HIDE_VALOR_CAVERN_AZELF on every load, so the lab "
        "and the Hall of Fame clearing the flag never bring Azelf back",
}


def script_references(root):
    """[{script, line, command, species}] for the commands in SCRIPT_COMMANDS
    whose species operand is a constant. Operands that are variables (the
    starter, the revived fossil) are decided at runtime and are not listed,
    and neither is a source in UNREACHABLE_SCRIPT_SOURCES."""
    rows = []
    for path in sorted(glob.glob(os.path.join(root, "res", "field", "scripts", "*.s"))):
        with open(path, encoding="utf-8", errors="replace") as f:
            in_kit = False
            for n, line in enumerate(f, 1):
                # The test kit's #ifdef OXIDE_TESTKIT blocks are never in the ROM
                # of record (docs/oxide/test-kit.md), so their gifts and battles
                # are not sources; skipped by line so the numbers stay right.
                if line.startswith("#ifdef OXIDE_TESTKIT"):
                    in_kit = True
                if in_kit:
                    in_kit = not line.startswith("#endif")
                    continue
                m = _SCRIPT_RE.match(line)
                if m and (os.path.basename(path)[:-2], m.group(2)) in UNREACHABLE_SCRIPT_SOURCES:
                    continue
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
    """[{map, command, species}] for every gift the tree's scripts make with
    a constant species. Until 2026-09-27 this read pokemon-gifts.csv, the
    base ROM's survey of 2026-09-20, which knew nothing of Oxide's own gifts
    (the Veilstone Elekid, the Day Care Floette) and still listed the gift
    clowns Ian retired."""
    return [{"map": r["script"].replace("scripts_", "", 1), "command": r["command"],
             "species": r["species"]}
            for r in script_references(root) if r["command"] in GIVE_COMMANDS]


# The legendary pool's draws (main-scripts, 2026-09-27): the new-game script
# rolls each place's species into a variable, and the static battle and the
# roamer read the variable, so the species are named only by these SetVars.
# Acuity Cavern's own script also sets a fallback for an old save, which is
# not a draw, so only the new-game script is read.
_DRAW_RE = re.compile(r"^\s*SetVar\s+(VAR_LEGENDARY_POOL_[A-Z_]+),\s*(SPECIES_[A-Z0-9_]+)")
DRAW_SCRIPT = os.path.join("res", "field", "scripts", "scripts_init_new_game.s")


def pool_draws(root):
    """[{script, line, command, species}] for the pool draws' species. A draw
    for a third the plan holds back (the roamer's since 2026-09-27) is left
    out: the script may still roll it, but nothing releases what it rolls."""
    path = os.path.join(root, DRAW_SCRIPT)
    if not os.path.exists(path):
        return []
    held = empty_thirds(pool_block(root))
    rows = []
    with open(path, encoding="utf-8", errors="replace") as f:
        for n, line in enumerate(f, 1):
            m = _DRAW_RE.match(line)
            key = m and m.group(1)[len("VAR_LEGENDARY_POOL_"):-len("_SPECIES")].lower()
            if m and key not in held:
                rows.append({"script": "scripts_init_new_game", "line": n,
                             "command": "LegendaryPoolDraw " + m.group(1),
                             "species": m.group(2)})
    return rows


# Hidden abilities handed out by script (element 8). A script sets
# FLAG_NEXT_MON_HIDDEN_ABILITY just before a gift, an egg or a scripted wild
# battle, and the next of these commands the player meets takes the flag,
# wherever it is; GiveHiddenAbility switches a party Pokemon over directly.
# The takers are the commands whose C code asks for the flag: the two gift
# functions, GiveEgg, and every battle through CreateWildMon_Scripted.
HIDDEN_FLAG = "FLAG_NEXT_MON_HIDDEN_ABILITY"
HIDDEN_TAKERS = ("GivePokemon", "GiveDesignedPokemon", "GiveEgg") + BATTLE_COMMANDS \
    + ("TestKitStartWildBattle",)
_GIFT_TAKERS = ("GivePokemon", "GiveDesignedPokemon")
_LABEL_RE = re.compile(r"^([A-Za-z_]\w*):")
_JUMP_RE = re.compile(r"^\s*(GoTo\w*|Call\w*|End|Return)\b")
_COMMAND_RE = re.compile(r"^\s*([A-Za-z_]\w*)\s*([^,\s]*)")
_SETVAR_RE = re.compile(r"^\s*SetVar\s+(\w+),\s*(SPECIES_[A-Z0-9_]+)")


def hidden_grants_in(text, script, draws=None):
    """[{script, line, command, species}] for each hidden ability one script's
    text hands out. `species` lists what the command can give: a constant, a
    SetVar earlier in the same label, or a legendary pool variable's draws
    (`draws`, {variable: [species]}); empty when the lint cannot tell. A flag
    set with no taker before the script jumps, ends or reaches a new label is
    a row with command None, since the next gift anywhere would take it."""
    draws = draws or {}
    # Comments go, keeping the line count, so prose in a /* */ block that
    # starts with "Call" or "End" is not read as a jump.
    text = re.sub(r"/\*.*?\*/", lambda m: "\n" * m.group(0).count("\n"), text, flags=re.S)
    rows = []
    pending, setvars, last_gift, in_kit = None, {}, [], False

    def unclaimed():
        rows.append({"script": script, "line": pending, "command": None, "species": []})

    for n, line in enumerate(text.split("\n"), 1):
        # The test kit is never in the ROM of record (script_references).
        if line.startswith("#ifdef OXIDE_TESTKIT"):
            in_kit = True
        if in_kit:
            in_kit = not line.startswith("#endif")
            continue
        line = line.split("//")[0]
        if _LABEL_RE.match(line) or _JUMP_RE.match(line):
            if pending:
                unclaimed()
            pending, setvars, last_gift = None, {}, []
            continue
        m = _SETVAR_RE.match(line)
        if m:
            setvars[m.group(1)] = m.group(2)
        m = _COMMAND_RE.match(line)
        if not m:
            continue
        command, operand = m.groups()
        if command == "SetFlag" and operand == HIDDEN_FLAG:
            pending = pending or n
        elif command == "ClearFlag" and operand == HIDDEN_FLAG:
            pending = None
        elif command in HIDDEN_TAKERS:
            if operand.startswith("SPECIES_"):
                species = [operand]
            elif operand in setvars:
                species = [setvars[operand]]
            else:
                species = list(draws.get(operand) or [])
            if pending:
                rows.append({"script": script, "line": n, "command": command,
                             "species": species})
                pending = None
            if command in _GIFT_TAKERS:
                last_gift = species
        elif command == "GiveHiddenAbility":
            # Its party slot is a variable; the Pokemon is taken to be the
            # gift just made in the same label, which is how a gift script
            # would use it.
            rows.append({"script": script, "line": n, "command": command,
                         "species": list(last_gift)})
    if pending:
        unclaimed()
    return rows


def hidden_ability_grants(root):
    """hidden_grants_in over every field script, each row with `stages`:
    [(stage, its hidden ability)] for the species and everything it can
    evolve into, since the hidden slot stays through evolution."""
    from . import pokedex      # here, not at the top: only this reader needs it
    draws = {}
    for r in pool_draws(root):
        draws.setdefault(r["command"].split()[-1], []).append(r["species"])
    rows = []
    for path in sorted(glob.glob(os.path.join(root, "res", "field", "scripts", "*.s"))):
        with open(path, encoding="utf-8", errors="replace") as f:
            text = f.read()
        if HIDDEN_FLAG not in text and "GiveHiddenAbility" not in text:
            continue
        rows += hidden_grants_in(text, os.path.basename(path)[:-2], draws)
    for r in rows:
        stages = []
        for sp in r["species"]:
            for stage in dex.later_stages(root, sp):
                rec = pokedex.load(root, stage) or {}
                stages.append((stage, rec.get("hidden_ability")))
        r["stages"] = stages
    return rows


def starters(root):
    """{species: label} for what scripted.json's live sources hand over when
    the script picks at runtime: the starter choice, Riley's random egg and
    the like, with their pools resolved from the scripts by scripted.load.
    Sources the simulator leaves out (an empty cavern, a battle that is not
    a legal catch, a trade of a cut line) are not counted."""
    from . import scripted     # here, not at the top: scripted imports availability, which imports audit
    out = {}
    for s in scripted.load(root):
        if not s.get("simulate", True):
            continue
        for sp in s.get("pool") or []:
            out.setdefault(sp, f"{s['kind']}, {s['id']}")
    return out


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


def _land_layers(area):
    """[(label, slots)] for a land table as each time of day meets it: the
    base slots in the morning, and by day and at night the same slots with 2
    and 3 replaced by that time's list, at those slots' levels."""
    base = area.kind_slots("land")
    out = [("land", base)]
    for layer in ("day", "night"):
        swap = area.data.get(layer) or []
        if len(swap) != len(model.DAY_NIGHT_SLOTS):
            continue
        slots = list(base)
        for sp, s in zip(swap, model.DAY_NIGHT_SLOTS):
            slots[s] = (sp, base[s][1], base[s][2])
        if slots != base:
            out.append((f"land by {layer}" if layer == "day" else "land at night", slots))
    return out


def acquisition_costs(areas, wanted):
    """{species: (cost, area, kind, lead_level)}: the cheapest place to meet
    each wanted species, over every live table kind, time of day and repel
    rung.

    Cost is expected encounters to the first one that is the species: the
    reciprocal of its share of the surviving pool at the best rung (design
    doc 2.4, with an empty party: nothing duped out yet). Water slots hold a
    level range, so their rungs admit fractions of a slot; analysis.pool
    handles that. Until 2026-09-27 this read only the morning's land slots
    and only areas with live grass, so a line met by day or at night, or only
    by rod in an area with no grass (Snowpoint's harbour), read as absent.
    """
    best = {}
    for a in areas:
        for kind in a.kinds_present():
            if kind == "land" and not a.land_active:
                continue                # grass the game never rolls
            rates = A.TABLE_KINDS[kind][2]
            variants = _land_layers(a) if kind == "land" else [(kind, a.kind_slots(kind))]
            for label, slots in variants:
                for lead, pool in A.distinct_rungs(slots, rates):
                    for sp, share in pool.items():
                        if sp in wanted and share > 0:
                            cost = 1.0 / share
                            if sp not in best or cost < best[sp][0]:
                                best[sp] = (cost, a.name, label, lead)
    return best


def pool_block(root):
    """The availability plan's legendary pool block, or {} without one."""
    path = os.path.join(root, "docs", "oxide", "encounters", "availability-plan.json")
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f).get("pool") or {}
    except (FileNotFoundError, ValueError):
        return {}


def empty_thirds(pool):
    """The thirds of the legendary pool drawn nowhere: the reserve, and the
    third of any place the pool lists as empty (Valor Cavern, and the roamer
    since 2026-09-27). A third is matched by its name in the empty list, as
    the balance track's obtainable() matches it, so the two cannot disagree."""
    empty = " ".join(pool.get("empty") or []).lower()
    return {k for k in (pool.get("thirds") or {}) if k == "reserve" or k.lower() in empty}


def held_back(root):
    """{species: why} for the legendaries Ian keeps out of reach on purpose,
    from the availability plan's pool block: the pool's reserve, and the
    third of any place the pool marks empty (Valor Cavern since 2026-09-27);
    and {species: text} for the post-League proposals, which are sourced on
    paper while their scripts wait. R12 reports these as warnings with the
    reason, so an error is a line nobody has decided about."""
    path = os.path.join(root, "docs", "oxide", "encounters", "availability-plan.json")
    try:
        with open(path, encoding="utf-8") as f:
            plan = json.load(f)
    except (FileNotFoundError, ValueError):
        return {}, {}
    pool = plan.get("pool") or {}
    until = pool.get("empty_until") or "Ian rules otherwise"
    held = {}
    for key, species in (pool.get("thirds") or {}).items():
        if key == "reserve":
            why = "in the legendary pool's reserve, drawn nowhere"
        else:
            place = next((e for e in pool.get("empty") or [] if key.lower() in e.lower()), None)
            if not place:
                continue
            why = f"in the pool third of {place}, which holds no legendary until {until}"
        for sp in species:
            held.setdefault(sp, why)
    proposals = {sp: text for sp, text in (plan.get("proposals") or {}).items()
                 if not sp.startswith("_")}
    return held, proposals


def availability(ref=None):
    """R12's input: one row per native line on the pick-list with its tier,
    whether it has a scripted source, and its cheapest wild acquisition.
    Returns None when the pick-list has no `tier` column yet, which is the
    signal for the rule to report itself skipped."""
    root = model.repo_root()
    if not any(r.get("tier") for r in dex.pick_list(root)):
        return None
    cov = coverage(ref)
    # Every live table, a rods-only area's water included, and every stage
    # of a line: catching a Pikachu is the Pichu line under the dupes clause,
    # and the babies stand as their next stage from level 10.
    areas = list(model.load_all(ref))
    members = {line["line"]: dex.members_of_line(root, line["line"]) or list(line["base"])
               for line in cov["lines"]}
    wanted = {sp for stages in members.values() for sp in stages}
    costs = acquisition_costs(areas, wanted)
    held, proposals = held_back(root)
    out = []
    for line in cov["lines"]:
        stages = members[line["line"]]
        cheapest = min(((*costs[sp], sp) for sp in members[line["line"]] if sp in costs),
                       default=None)
        # A honey-tree placement is a source the cost model cannot price (a
        # tree is slathered, waited on, and rolled by rarity tier), so it is
        # carried as its own flag, which R12 accepts.
        honey = sorted({key for _, key, _ in line["other"]
                        if key in (*model.HONEY_TREE_KEYS, "rare")})
        out.append({
            "name": line["name"], "line": line["line"], "tier": line["tier"],
            "non_wild": bool(line["gifts"] or line["trades"] or line["static"]
                             or line["scripted"]),
            "honey": honey,
            "cost": cheapest[0] if cheapest else None,
            "where": cheapest[1:4] if cheapest else None,
            # The stage met, when it is not the line's first (Pikachu for Pichu).
            "met_as": dex.display_name(cheapest[4])
                      if cheapest and cheapest[4] not in line["base"] else None,
            "held": next((held[sp] for sp in stages if sp in held), None),
            "proposal": next((proposals[sp] for sp in stages if sp in proposals), None),
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
    for name, reader in ((model.HONEY_TREE, lambda r: model.honey_tree_species(r, badges=None)),
                         (model.GREAT_MARSH_LOOKOUT, model.great_marsh_lookout_species)):
        for key, vals in reader(ref).items():
            for sp in set(vals):
                other[sp].append((name, key))
    gift_rows, trade_rows = gifts(root), trades(root)
    static_rows = ([r for r in script_references(root) if r["command"] in BATTLE_COMMANDS]
                   + pool_draws(root))
    runtime = dict(SCRIPTED, **starters(root))
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
        sc = [(runtime[sp], sp) for sp in consts if sp in runtime]
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

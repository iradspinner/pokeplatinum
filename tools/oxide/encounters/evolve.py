"""Put every wild slot at the stage its level deserves.

Ian's rule, 2026-09-21: a wild Pokemon should already be evolved if its level is
high enough to have evolved, and where a line branches the table picks a side.
An Elekid at Sendoff Spring is an Electivire; Treecko and Snivy on Route 208 are
a Grovyle and a Servine.

Three things decide what a slot holds.

**The level comes from the written table**, so this runs after `apply`, and a
species is judged by the lowest level it appears at in that area: a slot that
spans 22 to 26 is judged as 22, so nothing evolves before the whole slot has.

**A line that grows up on its own grows up at its own level.** When a stage has
any level-up evolution, the stone and trade routes out of it are ignored;
otherwise Snorunt would be a Froslass at the stone's judged level and never
reach Glalie at 42.

**A method with no level of its own gets a judged one**, in PSEUDO below. These
are the numbers to argue with: a stone at 30, friendship at 20, a trade at 38,
which is what makes Electabuzz an Electivire late on and not before.

An evolution into a species the pick-list does not carry is refused, and so is
one whose stage is already in the same table, because a table cannot hold the
same species twice.
"""
import json
import os

from . import audit
from . import model

# Methods that have no level of their own, and the level each is judged at.
PSEUDO = {
    "EVO_FRIENDSHIP": 20, "EVO_FRIENDSHIP_DAY": 20, "EVO_FRIENDSHIP_NIGHT": 20,
    "EVO_USE_ITEM": 30, "EVO_USE_ITEM_MALE": 30, "EVO_USE_ITEM_FEMALE": 30,
    "EVO_STONE": 30, "EVO_STONE_MALE": 30, "EVO_STONE_FEMALE": 30,
    "EVO_TRADE": 38, "EVO_TRADE_ITEM": 38, "EVO_OTHER_PARTY_MON": 38,
    "EVO_LEVEL_DARK_IN_PARTY": 38,
    "EVO_LEVEL_MOSS_ROCK": 30, "EVO_LEVEL_ICE_ROCK": 30, "EVO_LEVEL_RAIN": 30,
    "EVO_HAS_MOVE": 32, "EVO_HAS_MOVE_TYPE": 32,
}
DEFAULT_PSEUDO = 32

# Where a line splits into two stages that are both available at the same level,
# the one the tables use. Judgement, not data; an unruled branch stays put.
BRANCH = {
    "SPECIES_CHARCADET": "SPECIES_CERULEDGE",
    "SPECIES_GOOMY": "SPECIES_SLIGGOO",
    "SPECIES_KIRLIA": "SPECIES_GARDEVOIR",
    "SPECIES_SCYTHER": "SPECIES_SCIZOR",
    "SPECIES_SNORUNT": "SPECIES_GLALIE",
    "SPECIES_YAMASK": "SPECIES_COFAGRIGUS",
    "SPECIES_WURMPLE": "SPECIES_SILCOON",
    "SPECIES_CLAMPERL": "SPECIES_GOREBYSS",
    "SPECIES_BURMY": "SPECIES_WORMADAM",
    "SPECIES_NINCADA": "SPECIES_NINJASK",
    "SPECIES_TYROGUE": "SPECIES_HITMONLEE",
    "SPECIES_EEVEE": "SPECIES_VAPOREON",
    "SPECIES_POLIWHIRL": "SPECIES_POLIWRATH",
    "SPECIES_SLOWPOKE": "SPECIES_SLOWBRO",
    "SPECIES_EXEGGCUTE": "SPECIES_EXEGGUTOR",
    "SPECIES_APPLIN": "SPECIES_FLAPPLE",
    "SPECIES_TOXEL": "SPECIES_TOXTRICITY",
    "SPECIES_MIME_JR": "SPECIES_MR_MIME",
    "SPECIES_GLOOM": "SPECIES_VILEPLUME",
}
WATER_KINDS = ("surf", "old_rod", "good_rod", "super_rod")
PLAN = os.path.join("docs", "oxide", "encounters", "availability-plan.json")


def evolutions(root, species):
    """[(level it is reachable at, target)] out of one stage."""
    folder = species.replace("SPECIES_", "").lower()
    path = os.path.join(root, "res", "pokemon", folder, "data.json")
    try:
        with open(path, encoding="utf-8") as f:
            evos = json.load(f).get("evolutions") or []
    except (FileNotFoundError, ValueError):
        return []
    out = []
    for evo in evos:
        if not isinstance(evo, list) or not evo:
            continue
        method = evo[0] if isinstance(evo[0], str) else ""
        ints = [x for x in evo if isinstance(x, int) and not isinstance(x, bool)]
        target = next((x for x in evo
                       if isinstance(x, str) and x.startswith("SPECIES_")), None)
        # A mega or a regional form is listed as an evolution of its base
        # (SPECIES_GYARADOS -> SPECIES_GYARADOS_M); it is not a stage.
        if target is None or target.startswith(species + "_"):
            continue
        if method.startswith("EVO_LEVEL") and ints:
            out.append((ints[0], target, True))
        else:
            out.append((PSEUDO.get(method, DEFAULT_PSEUDO), target, False))
    if any(by_level for _, _, by_level in out):
        out = [e for e in out if e[2]]
    return [(need, target) for need, target, _ in out]


def stage_at(root, species, level, on_list, seen=None):
    """The stage of `species`'s line that an encounter of `level` should hold."""
    seen = seen or {species}
    ready = sorted({t for need, t in evolutions(root, species)
                    if level >= need and t not in seen and t in on_list})
    if not ready:
        return species
    if len(ready) > 1:
        pick = BRANCH.get(species)
        if pick not in ready:
            return species          # no ruling: leave it rather than guess
        chosen = pick
    else:
        chosen = ready[0]
    return stage_at(root, chosen, level, on_list, seen | {chosen})


def lowest_levels(area):
    """{species: the lowest level this area shows it at}."""
    out = {}

    def note(species, level):
        if species not in out or level < out[species]:
            out[species] = level
    # A water-only area keeps a land array at rate 0, which the sidecar has no
    # cast for and nothing ever meets; judging it would ask for a change that
    # cannot be written.
    land = area.slots if (area.has_land and area.land_active) else []
    for species, level in land:
        note(species, level)
    levels = [level for _, level in land]
    for key in ("day", "night"):
        for i, species in enumerate(area.data.get(key) or []):
            if i + 1 < len(levels):
                note(species, levels[i + 1])
    for kind in WATER_KINDS:
        for row in area.data.get(kind + "_encounters") or []:
            # A water slot is a range; judge it by its floor, so nothing evolves
            # until the whole slot has.
            if row.get("species"):
                note(row["species"], row.get("level_min", 0))
    return out


def plan_changes(ref=None):
    """[(area, from, to, level)] and the ones a duplicate stage blocks."""
    root = model.repo_root()
    on_list = audit.on_list(root)
    entries = (model.load_sidecar() or {}).get("areas") or {}
    moves, blocked = [], []
    for area in model.load_all(ref):
        entry = entries.get(area.name) or {}
        present = set(entry.get("cast") or []) | set(entry.get("day") or []) \
            | set(entry.get("night") or [])
        for kind in WATER_KINDS:
            present |= set((entry.get(kind) or {}).get("cast") or [])
        for species, level in sorted(lowest_levels(area).items()):
            new = stage_at(root, species, level, on_list)
            if new == species:
                continue
            (blocked if new in present else moves).append(
                (area.name, species, new, level))
    return moves, blocked


def apply(moves):
    """Rewrite the sidecar's casts and the plan's species lists."""
    sidecar = model.load_sidecar()
    entries = sidecar["areas"]
    with open(PLAN, encoding="utf-8") as f:
        plan = json.load(f)
    by_area = {}
    for area, old, new, _ in moves:
        by_area.setdefault(area, {})[old] = new
    for area, mapping in by_area.items():
        entry = entries.get(area)
        if not entry:
            continue
        for key in ("cast", "day", "night"):
            if entry.get(key):
                entry[key] = [mapping.get(x, x) for x in entry[key]]
        for kind in WATER_KINDS:
            if (entry.get(kind) or {}).get("cast"):
                entry[kind]["cast"] = [mapping.get(x, x) for x in entry[kind]["cast"]]
        spec = plan["areas"].get(area)
        if spec:
            for key in ("home", "cameo", "tail"):
                if spec.get(key):
                    spec[key] = [mapping.get(x, x) for x in spec[key]]
    model.save_sidecar(sidecar)
    with open(PLAN, "w", encoding="utf-8", newline="\n") as f:
        f.write(_dump(plan) + "\n")
    return len(by_area)


def _dump(obj, indent=0):
    """The plan file's own shape: one key a line, scalar lists kept inline."""
    pad = "  " * indent
    if isinstance(obj, dict):
        if not obj:
            return "{}"
        items = [f"{pad}  {json.dumps(k, ensure_ascii=False)}: {_dump(v, indent + 1)}"
                 for k, v in obj.items()]
        return "{\n" + ",\n".join(items) + f"\n{pad}}}"
    if isinstance(obj, list):
        if all(not isinstance(x, (dict, list)) for x in obj):
            return json.dumps(obj, ensure_ascii=False)
        items = [f"{pad}  {_dump(v, indent + 1)}" for v in obj]
        return "[\n" + ",\n".join(items) + f"\n{pad}]"
    return json.dumps(obj, ensure_ascii=False)

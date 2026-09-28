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
are the numbers to argue with: a stone or a place (the Moss Rock, the Ice Rock,
Mt. Coronet's field) at 30, and a held item, a known move or a partner in the
party at 32. Oxide has no friendship or trade evolution left (Ian, 2026-09-27,
and element 8's trade strip), so neither has a number.

An evolution into a species the pick-list does not carry is refused, and so is
one whose stage is already in the same table, because a table cannot hold the
same species twice.
"""
import json
import os

from . import audit
from . import dex
from . import model

# Methods that have no level of their own, and the level each is judged at,
# under the names res/pokemon uses. Until 2026-09-27 this table was keyed by
# other names (EVO_FRIENDSHIP, EVO_TRADE_ITEM and the like), so every method
# but the stones fell through to DEFAULT_PSEUDO; the values below are the ones
# the tables were built against, so renaming them moved nothing.
PSEUDO = {
    "EVO_USE_ITEM": 30, "EVO_USE_ITEM_MALE": 30, "EVO_USE_ITEM_FEMALE": 30,
    "EVO_LEVEL_MOSS_ROCK": 30, "EVO_LEVEL_ICE_ROCK": 30,
    "EVO_LEVEL_MAGNETIC_FIELD": 32,
    "EVO_LEVEL_WITH_HELD_ITEM_DAY": 32, "EVO_LEVEL_WITH_HELD_ITEM_NIGHT": 32,
    "EVO_LEVEL_KNOW_MOVE": 32, "EVO_LEVEL_SPECIES_IN_PARTY": 32,
    # Feebas's Beauty of 170 is a condition, not a level (dex.NOT_A_LEVEL);
    # until 2026-09-27 it read as Milotic reached at level 170.
    "EVO_LEVEL_BEAUTY": 32,
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


# Evolutions the Pokemon decides, not the player: by its personality
# (Wurmple), its sex (Burmy, Combee) or its Attack against its Defense
# (Tyrogue). A nuzlocke meets one of each per place, so the Box sim takes the
# worse outcome of these (the Overseer's correction, 2026-09-28).
FIXED_BY_THE_POKEMON = ("EVO_LEVEL_PID_LOW", "EVO_LEVEL_PID_HIGH", "EVO_LEVEL_FEMALE",
                        "EVO_LEVEL_MALE", "EVO_LEVEL_ATK_LT_DEF", "EVO_LEVEL_ATK_GT_DEF",
                        "EVO_LEVEL_ATK_EQ_DEF")
# Not a stage of the caught Pokemon: Shedinja is a second Pokemon that
# appears beside the Ninjask a Nincada becomes.
NOT_A_STAGE = ("EVO_LEVEL_SHEDINJA",)


def routes(root, species):
    """[(target, level or None, item or None, fixed)] out of one stage, for
    the Box sim (Ian, 2026-09-28): a level evolution with its level, and an
    evolution by a stone either sex can use with its item, whose first split
    the balance track's census gives. A stone is kept beside a level
    evolution (Koffing's Moon Stone beside Weezing at 35), where
    `evolutions`, which the tables use, drops it. Any other method keeps its
    judged level, as `evolutions` gives it, and a stone for one sex
    (Froslass's Dawn Stone) is judged so too, since the sim cannot know a
    Pokemon's sex. `fixed` marks an evolution the Pokemon decides
    (FIXED_BY_THE_POKEMON) rather than the player."""
    folder = species.replace("SPECIES_", "").lower()
    path = os.path.join(root, "res", "pokemon", folder, "data.json")
    try:
        with open(path, encoding="utf-8") as f:
            evos = json.load(f).get("evolutions") or []
    except (FileNotFoundError, ValueError):
        return []
    by_level, stones, judged = [], [], []
    for evo in evos:
        if not isinstance(evo, list) or not evo:
            continue
        method = evo[0] if isinstance(evo[0], str) else ""
        ints = [x for x in evo if isinstance(x, int) and not isinstance(x, bool)]
        target = next((x for x in reversed(evo)
                       if isinstance(x, str) and x.startswith("SPECIES_")), None)
        if target is None or target.startswith(species + "_") or method in NOT_A_STAGE:
            continue
        items = [x for x in evo if isinstance(x, str) and x.startswith("ITEM_")]
        level = dex.evo_level(method, ints)
        fixed = method in FIXED_BY_THE_POKEMON
        if level is not None:
            by_level.append((target, level, None, fixed))
        elif method == "EVO_USE_ITEM" and items:
            stones.append((target, None, items[0], False))
        else:
            judged.append((target, PSEUDO.get(method, DEFAULT_PSEUDO), None, fixed))
    # As in `evolutions`, a judged route yields to a level route out of the
    # same stage (Snorunt grows into Glalie; its Dawn Stone is for females).
    return by_level + stones + ([] if by_level else judged)


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
        # The result is the last species named; one before it is a partner
        # (EVO_LEVEL_SPECIES_IN_PARTY: Mantyke with a Remoraid in the party).
        target = next((x for x in reversed(evo)
                       if isinstance(x, str) and x.startswith("SPECIES_")), None)
        # A mega or a regional form is listed as an evolution of its base
        # (SPECIES_GYARADOS -> SPECIES_GYARADOS_M); it is not a stage.
        if target is None or target.startswith(species + "_"):
            continue
        level = dex.evo_level(method, ints)
        if level is not None:
            out.append((level, target, True))
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

"""The box simulator: one nuzlocke run up to a chosen split, played to make
the box worth as much as it can (Ian, 2026-09-26).

    PYTHONPATH=. python3 -m tools.oxide.encounters.simulate --split Wake \\
        --deaths 3 --starter SPECIES_PIPLUP --seed 7
    PYTHONPATH=. python3 -m tools.oxide.encounters.simulate --areas Gardenia

The first form plays one run and prints it area by area; the second prints
what every capture area is worth to an empty box by each of its options,
which is the per-area analysis Ian wanted kept in code rather than in the
tool. The tool's Simulator tab calls `run` through the server.

The rules are Ian's:

- one encounter per capture area (location name), the dupes clause over
  whole families, and dead Pokemon still count for dupes;
- any table in an area may be chosen: grass by time of day, surf and the
  rods once they arrive, the honey tree, and any scripted source there;
- a repel manipulation picks the lead level and so the rung of a grass
  table; before Gardenia's split only one is allowed in the whole run;
- gifts, trades, statics and eggs count as `scripted.json` places them;
  an egg is a capture of its own;
- deaths hit a random living Pokemon at a random point of the run;
- the Great Marsh dailies are left out, the Battle Zone is open in its
  planned split, and planned areas count as if built.

The player is played greedily and adaptively: at each area, with the box as
it stands, it takes the option whose expected gain to the box is highest,
waits for a later option (surf, a rod, the honey tree) when that is worth
more and still arrives in time, and spends the one early repel where it
gains the most among the Roark-split areas still to come. When luck or a
death pushes the box off the expected line, every later choice is made
against the box it actually has.

A random scripted pool is treated like a table under the dupes clause (a
member the player already has does not count), which reads the gift
scripts' yes-or-no as a chance to decline and ask again.
"""
import argparse
import collections
import functools
import json
import os
import random
import sys

from . import analysis as A
from . import audit
from . import dex
from . import evolve
from . import locations
from . import model
from . import pokedex
from . import progression
from . import scripted

VALUES = os.path.join("docs", "oxide", "encounters", "values.json")
TIER_SCORE = {"S": 100, "A": 80, "B": 60, "C": 40, "D": 20}
PICK_SCORE = {"gate": 100, "preferred": 90, "starter-adjacent": 55, "filler": 50}
# The value mix: how much of a Pokemon's worth is raw stats, how much the
# nuzlocke rating of its line, and how much the pick-list tier.
W_BST, W_TIER, W_PICK = 0.45, 0.40, 0.15
# Ian's super-wanted lines (values.json, `wanted`) are worth this much more to
# him than their stats say, so best play goes after them the way he would.
WANTED_BONUS = 10.0
BST_FLOOR, BST_CEIL = 250, 600
# Ian: "I'd rather have 10 decent Pokemon than only 6 great ones", so the
# best six add a small bonus on top of the sum of everything alive.
TOP_SIX_WEIGHT = 0.25
# A later option is waited for only when it beats the best one now by this.
DEFER_MARGIN = 1.05
HONEY_FROM = scripted.HONEY_FROM  # Honey is sold in Floaroma, Gardenia's split
HONEY_SLOTS = (0.40, 0.20, 0.20, 0.10, 0.05, 0.05)
WATER_KINDS = ("surf", "old_rod", "good_rod", "super_rod")
KIND_WORDS = {"land": "grass", "surf": "surf", "old_rod": "Old Rod",
              "good_rod": "Good Rod", "super_rod": "Super Rod"}


# -- value ---------------------------------------------------------------------


class Values:
    """What a Pokemon is worth to a box at a given split: the stage its line
    reaches by that split's level cap, scored on BST, the line's nuzlocke
    rating and its pick-list tier, 0 to 100."""

    def __init__(self, root, split, sidecar):
        self.root = root
        self.cap = (progression.cap_of(sidecar, split)
                    or progression.DEFAULT_CAPS.get(split) or 100)
        with open(os.path.join(root, VALUES), encoding="utf-8") as f:
            data = json.load(f)
        self.rating = data["lines"]
        self.wanted = {dex.line_of(root, sp) for sp in data.get("wanted") or []
                       if os.path.isdir(os.path.join(root, "res", "pokemon", pokedex.folder_of(sp)))}
        self.on_list = audit.on_list(root)
        # Lines a trade for a wanted Pokemon asks for (Mindy's Snover for
        # Suicune): Ian would catch one with the trade in mind, so it counts
        # as wanted until then. `run` fills this from scripted.json.
        self.plan_lines = set()
        self.pick_tier = {}
        for row in dex.pick_list(root):
            if row.get("constant"):
                self.pick_tier[dex.line_of(root, row["constant"])] = row.get("tier") or ""
        # A stone evolution is reachable from the split the stone is first in
        # reach, by the balance track's census (read only), counted as
        # reachable rather than budgeted (Ian, 2026-09-28).
        self.split = split
        self.split_idx = progression.split_index(sidecar)
        try:
            from ..balance import pool as bpool
            self.stone_first = bpool.evolution_items_first()
        except Exception:
            self.stone_first = {}

    def _ready(self, level, item):
        if item is None:
            return level <= self.cap
        first = self.stone_first.get(item)
        return first is not None and self.split_idx.get(first, 99) <= self.split_idx.get(self.split, 99)

    @functools.lru_cache(maxsize=None)
    def stage(self, species):
        """The best stage a Pokemon caught as `species` reaches by this split:
        by level under the cap, by a stone once the stone is in reach (both
        Koffing's routes, Weezing at 35 and Galarian Weezing by Moon Stone),
        taking the one worth more where two are ready."""
        return self._stage(species, frozenset([species]))

    def _stage(self, species, seen):
        routes = [r for r in evolve.routes(self.root, species)
                  if r[0] not in seen and r[0] in self.on_list]
        worth = lambda st: (self.worth(st), st)
        # The player's routes (a stone, a held item, a level): the best stage
        # any ready one leads to.
        chosen = sorted({t for t, level, item, fixed in routes if not fixed and self._ready(level, item)})
        options = [self._stage(t, seen | {t}) for t in chosen]
        # The Pokemon's own (personality, sex, stats): it takes one of them,
        # and the sim assumes the worse, counting one not yet reachable as
        # staying put (a male Combee is a Combee until 50).
        fixed = [(t, level, item) for t, level, item, f in routes if f]
        if fixed:
            outcomes = [self._stage(t, seen | {t}) if self._ready(level, item) else species
                        for t, level, item in fixed]
            options.append(min(outcomes, key=worth))
        return max(options, key=worth) if options else species

    @functools.lru_cache(maxsize=None)
    def worth(self, stage):
        """What a Pokemon at this stage is worth, 0 to 100."""
        try:
            bst = pokedex.load(self.root, stage)["bst"]
        except Exception:
            bst = BST_FLOOR
        line = dex.line_of(self.root, stage)
        # A family's regional branch (Galarian Weezing in Koffing's) carries its
        # own rating, and is measured against its own final form; a family
        # with none is one branch, rated by its line id as before.
        branch = dex.branch_of(self.root, stage)
        members = [m for m in dex.members_of_line(self.root, line)
                   if dex.branch_of(self.root, m) == branch
                   and os.path.isdir(os.path.join(self.root, "res", "pokemon", pokedex.folder_of(m)))]
        key = min(members) if members else line
        bst_score = 100 * min(1.0, max(0.0, (bst - BST_FLOOR) / (BST_CEIL - BST_FLOOR)))
        tier = TIER_SCORE.get(self.rating.get(key, self.rating.get(line)), 40)
        # A line's rating is for its final form; a stage short of it by the
        # cap is worth that share of it, measured by BST.
        final = max((pokedex.load(self.root, m)["bst"] for m in members), default=bst)
        tier *= min(1.0, bst / final) if final else 1.0
        pick = PICK_SCORE.get(self.pick_tier.get(line), 40)
        return round(W_BST * bst_score + W_TIER * tier + W_PICK * pick, 1)

    @functools.lru_cache(maxsize=None)
    def of(self, species):
        return self.worth(self.stage(species))

    def pref(self, species):
        """What the player chases: the value, plus Ian's bonus for a
        super-wanted line. Choices use this; reports and the scarcity rule
        use `of`, the Pokemon's own worth."""
        line = dex.line_of(self.root, species)
        bonus = WANTED_BONUS if line in self.wanted or line in self.plan_lines else 0.0
        return self.of(species) + bonus


def box_value(values):
    """The box's worth: everything alive, plus a small bonus for the best
    six."""
    alive = sorted(values, reverse=True)
    return sum(alive) + TOP_SIX_WEIGHT * sum(alive[:6])


def gain(value, alive_values):
    """What adding a Pokemon worth `value` does to a box's worth."""
    return box_value(alive_values + [value]) - box_value(alive_values)


# -- the world -----------------------------------------------------------------


# requires: for a trade, the species it asks for; the player hands over a
# living member of that line, which leaves the box.
Option = collections.namedtuple("Option", "label kind split shares repel requires",
                                defaults=(None,))
# shares: {species: weight}; a scripted "choice" pool is marked by kind
# "choice" and a legendary draw by kind "legendary".


def _table_options(area, entry, sidecar, rank, target):
    """Every way to catch something from one encounter file, as Options."""
    out = []
    split = entry.get("split")
    if area.land_active and split:
        base = area.kind_slots("land")
        tables = [("morning", base)]
        for layer in ("day", "night"):
            swap = area.data.get(layer) or []
            if len(swap) == 2:
                t = list(base)
                for i, sp in enumerate(swap):
                    _, lo, hi = t[2 + i]
                    t[2 + i] = (sp, lo, hi)
                tables.append((layer, t))
        # A pool reached two ways (a rung above the day and night slots is
        # the same at every hour) is one choice, listed once.
        seen = []
        for layer, t in tables:
            whole = A.merged(t)
            if whole not in seen:
                seen.append(whole)
                out.append(Option(f"grass, {layer}", "land", split, whole, None))
            for level, pool in A.distinct_rungs(t)[1:]:
                if pool in seen:
                    continue
                seen.append(pool)
                out.append(Option(f"grass, {layer}, repel with a level {level} lead",
                                  "land", split, pool, level))
    water_from = entry.get("water_split") or split
    for kind in WATER_KINDS:
        slots = area.kind_slots(kind) if kind in area.kinds_present() else []
        if not slots or not water_from:
            continue
        arrives = max((water_from, progression.rod_split(sidecar, kind) or water_from),
                      key=lambda s: rank.get(s, 99))
        out.append(Option(KIND_WORDS[kind], kind, arrives,
                          A.merged(slots, A.TABLE_KINDS[kind][2]), None))
    return [o for o in out if rank.get(o.split, 99) <= rank[target]]


def _honey_option(split, rank, tables):
    split = max((split, HONEY_FROM), key=lambda s: rank.get(s, 99))
    table = scripted.honey_table_for(split, rank, tables)
    shares = {}
    for tier, weight in (("common", 0.70), ("uncommon", 0.20)):
        for sp, p in zip(table[tier], HONEY_SLOTS):
            shares[sp] = shares.get(sp, 0.0) + weight * p
    return Option(f"honey tree ({table['badges']} badge table)", "honey", split,
                  shares, None)


def _source_option(src):
    kind = {"choice": "choice", "legendary_pool": "legendary"}.get(src["pick"], "scripted")
    shares = {sp: 1.0 / len(src["pool"]) for sp in src["pool"]}
    return Option(src["label"], kind, src["split"], shares, None, src.get("requires"))


def world(target, root=None):
    """The capture areas of a run up to `target`, in play order: each a dict
    with its name, first split, order and options."""
    root = root or model.repo_root()
    sidecar = model.load_sidecar() or {}
    entries = sidecar.get("areas") or {}
    rank = progression.split_index(sidecar)
    where = locations.location_of(root)
    stems_of = collections.defaultdict(list)
    for area in model.load_all():
        name = where.get(area.name)
        e = entries.get(area.name) or {}
        if not name or e.get("no_capture") or area.name.startswith("encounters_unknown_"):
            continue
        stems_of[name].append((area, e))

    areas = {}

    def place(name):
        return areas.setdefault(name, {"name": name, "options": [], "order": None,
                                       "split": None, "sources": []})

    def note_time(a, split, order):
        if split is None:
            return
        if a["split"] is None or (rank.get(split, 99), order or 0) < \
                (rank.get(a["split"], 99), a["order"] or 0):
            a["split"], a["order"] = split, order

    for name, members in stems_of.items():
        a = place(name)
        for area, e in members:
            opts = _table_options(area, e, sidecar, rank, target)
            # Tables of one place that are the same (Lake Verity and its
            # drained twin) offer the same choice once.
            opts = [o for o in opts if not any(p.shares == o.shares and p.split == o.split
                                               for p in a["options"])]
            a["options"] += opts
            for o in opts:
                note_time(a, o.split, e.get("order"))
    honey_tables = model.honey_tree_tables()
    trees = scripted.honey_tree_locations(root)
    for src in scripted.load(root):
        if not src.get("simulate", True) or src["kind"] == "starter":
            continue
        if rank.get(src["split"], 99) > rank[target]:
            continue
        name = src.get("capture_area") or src["label"]
        a = place(name)
        a["options"].append(_source_option(src))
        a["sources"].append(src["id"])
        note_time(a, src["split"], src.get("order"))
    # A tree is reached when its place is, whatever the target: the place's
    # earliest split over all its tables, not only the ones in reach.
    home = {}
    for name, members in stems_of.items():
        splits = [s for _, e in members for s in (e.get("split"), e.get("water_split")) if s]
        if splits:
            home[name] = min(splits, key=lambda s: rank.get(s, 99))
    for name, n in trees.items():
        a = areas.get(name) or place(name)
        reached = home.get(name) or a["split"] or HONEY_FROM
        opt = _honey_option(reached, rank, honey_tables)
        if rank.get(opt.split, 99) <= rank[target]:
            a["options"].append(opt)
            note_time(a, opt.split, a["order"])
    out = [a for a in areas.values() if a["options"] and a["split"]]
    out.sort(key=lambda a: (rank.get(a["split"], 99), a["order"] if a["order"] is not None else 1e9,
                            a["name"]))
    return out


# -- one run -------------------------------------------------------------------


class Box:
    def __init__(self, root, values):
        self.root = root
        self.values = values
        self.members = []          # [{species, area, alive, value, traded}]
        self.lines = set()         # every line caught, dead or alive

    def owns(self, species):
        return dex.line_of(self.root, species) in self.lines

    def alive_values(self):
        return [m["value"] for m in self.members if m["alive"]]

    def alive_prefs(self):
        return [self.values.pref(m["species"]) for m in self.members if m["alive"]]

    def payment(self, requires):
        """The least valuable living member a trade asking for `requires`
        could take, or None."""
        line = dex.line_of(self.root, requires)
        can = [m for m in self.members if m["alive"] and dex.line_of(self.root, m["species"]) == line]
        return min(can, key=lambda m: m["value"]) if can else None

    def add(self, species, area):
        v = self.values.of(species)
        self.members.append({"species": species, "area": area, "alive": True, "value": v,
                             "traded": False})
        self.lines.add(dex.line_of(self.root, species))
        return v


def _live(shares, box, drawn=()):
    """The option's odds under the dupes clause: owned families and already
    drawn legendaries drop out, the rest renormalise."""
    kept = {sp: s for sp, s in shares.items() if not box.owns(sp) and sp not in drawn}
    total = sum(kept.values())
    return {sp: s / total for sp, s in kept.items()} if total else {}


def expected_gain(option, box, drawn=()):
    alive = box.alive_prefs()
    live = _live(option.shares, box, drawn)
    if not live:
        return 0.0
    if option.requires:
        pay = box.payment(option.requires)
        if pay is None:
            return 0.0
        rest = list(alive)
        rest.remove(box.values.pref(pay["species"]))
        # A member caught with this trade in mind (Ian's Snover for Suicune)
        # was the trade's price from the start, so handing it over costs
        # nothing further; any other member is a real loss to the box.
        base = rest if dex.line_of(box.root, pay["species"]) in box.values.plan_lines else alive
        return sum(p * (box_value(rest + [box.values.pref(sp)]) - box_value(base))
                   for sp, p in live.items())
    if option.kind == "choice":
        return max(gain(box.values.pref(sp), alive) for sp in live)
    return sum(p * gain(box.values.pref(sp), alive) for sp, p in live.items())


def _roll(option, box, rng, drawn=()):
    live = _live(option.shares, box, drawn)
    if not live:
        return None
    if option.kind == "choice":
        return max(live, key=box.values.pref)
    r, acc = rng.random(), 0.0
    for sp, p in sorted(live.items()):
        acc += p
        if r <= acc:
            return sp
    return sorted(live)[-1]


def context(target, root=None):
    """What every run to `target` shares: the sidecar, the split order, the
    values and the capture areas. `confidence` builds it once for all its
    runs; `run` builds its own when given none."""
    root = root or model.repo_root()
    sidecar = model.load_sidecar() or {}
    rank = progression.split_index(sidecar)
    if target not in rank:
        raise ValueError(f"no such split: {target}")
    values = Values(root, target, sidecar)
    values.plan_lines = {dex.line_of(root, src["requires"]) for src in scripted.load(root)
                         if src.get("requires") and src.get("simulate", True)
                         and any(dex.line_of(root, sp) in values.wanted for sp in src["pool"])}
    return {"root": root, "target": target, "sidecar": sidecar, "rank": rank, "values": values,
            "areas": world(target, root),
            "starter_src": next(s for s in scripted.load(root) if s["kind"] == "starter")}


def can_give(area):
    """Every species an area's options can give, for the Box sim's lock list."""
    return sorted({sp for o in area["options"] for sp in o.shares})


def start_from_save(save, encounters, target, root=None, ctx=None):
    """The state a real save leaves a run in (Ian's request 2): {"members":
    [{species, area, alive}], "used": {area names}, "split", "unmatched"}.

    Every Pokemon in the party and the boxes spends the capture of the place
    it was met, or of its egg's source for an egg or a hatched Pokemon. A met
    location names a place, and the sim's areas are places, so the two match
    by name; a place the sim splits in several (Mt. Coronet's captures) is
    matched to the one whose tables give that Pokemon. The graveyard is the
    run of boxes at the end that fills backwards (Ian, 2026-09-27): the last
    box, and the one before it while the one after is full; a Pokemon there
    is dead. The tool's own Caught list (`encounters`, area file to species)
    marks the places whose encounter left nothing in the save, a Pokemon that
    fled or fainted. The run resumes in the save's level-cap split."""
    ctx = ctx or context(target, root)
    root = ctx["root"]
    by_name = {a["name"]: a for a in ctx["areas"]}
    counts = collections.Counter(m["box"] for m in save.get("boxes") or [])
    grave, b = set(), save.get("box_count") or 0
    while b >= 1:
        grave.add(b)
        if counts[b] < 30:
            break
        b -= 1
    members, used, unmatched = [], set(), []
    # The game's place names use a typographic apostrophe (Rowan’s Briefcase)
    # where the tool's use a plain one.
    norm = lambda name: (name or "").replace("’", "'")
    by_name = {norm(k): v for k, v in by_name.items()}
    starter_place = ctx["starter_src"].get("capture_area") or "Route 201"

    def area_for(place, species):
        place = norm(place)
        if place in by_name:
            return by_name[place]["name"]
        family = dex.line_of(root, species)
        near = [a for a in ctx["areas"] if a["name"].startswith(place) and a["name"] not in used]
        for a in near:
            if any(dex.line_of(root, sp) == family for sp in can_give(a)):
                return a["name"]
        return near[0]["name"] if near else None

    for mon in (save.get("party") or []) + (save.get("boxes") or []):
        if not mon.get("species", "").startswith("SPECIES_"):
            continue
        place = mon.get("egg_location") or mon.get("met_location") or ""
        # The starter's place is its own met location, not a sim area.
        name = starter_place if norm(place) == norm(starter_place) else area_for(place, mon["species"])
        if name:
            used.add(name)
        elif place:
            unmatched.append(f"{mon['name']} from {place}")
        members.append({"species": mon["species"], "area": name or place,
                        "alive": mon.get("box") not in grave, "slot": mon["slot"]})
    where = locations.location_of(root)
    by_key = scripted.by_key()
    for key in encounters or {}:
        src = by_key.get(key)
        name = (src.get("capture_area") or src.get("label")) if src else where.get(key)
        if name in by_name:
            used.add(name)
    split = ((save.get("progress") or {}).get("split") or {}).get("name")
    return {"members": members, "used": used, "split": split if split in ctx["rank"] else None,
            "unmatched": unmatched, "graveyard": sorted(grave)}


def run(target, deaths=0, starter=None, seed=None, root=None, locks=None, start=None, ctx=None):
    """Play one run to the end of `target`. Returns the log, the box and its
    worth, as plain data for the tool and the command line.

    `locks` is {area: species, or "" to leave it unused}: the player's own
    picks (Ian's request 1), taken as they are, never waited on, with every
    other area played for the best box around them. `start` is the state a
    save leaves (`start_from_save`, request 2): its Pokemon already in the box
    and its places spent, the run resuming in its split, where a place left
    behind unused is still open with what the player has now. Every area's
    entry says what the area could give, the decision made there and its
    margin, the lead of the best option over the next, for `confidence`."""
    ctx = ctx or context(target, root)
    root, rank, values = ctx["root"], ctx["rank"], ctx["values"]
    locks = locks or {}
    rng = random.Random(seed)
    box = Box(root, values)
    areas = list(ctx["areas"])
    log = []
    if start:
        for m in start["members"]:
            box.add(m["species"], m["area"])
            box.members[-1]["alive"] = m["alive"]
            log.append({"area": m["area"], "split": start["split"] or "Roark",
                        "choice": "in your save" + ("" if m["alive"] else ", dead"),
                        "species": m["species"], "value": box.members[-1]["value"],
                        "from_save": True, "options": []})
        areas = [a for a in areas if a["name"] not in start["used"]]
        now_rank = rank.get(start["split"], 0)
        areas = [a if rank.get(a["split"], 99) >= now_rank else dict(a, split=start["split"])
                 for a in areas]
        repel_used = now_rank > 0
    else:
        starter = starter or rng.choice(ctx["starter_src"]["pool"])
        # The starter spends the capture of the place scripted.json names for
        # it. That was Route 201 until the starter got a met location of its
        # own, Rowan's Briefcase (Ian, 2026-09-27), which leaves Route 201's
        # table a capture from the first step.
        where = ctx["starter_src"].get("capture_area") or "Route 201"
        log.append({"area": where, "split": "Roark", "choice": "the starter",
                    "species": starter, "value": box.add(starter, where), "options": []})
        areas = [a for a in areas if a["name"] != where]
        repel_used = False

    # Deaths land between captures, at random points of the run.
    n = len(areas)
    death_at = collections.Counter(rng.randrange(n + 1) for _ in range(max(0, deaths)))
    roark = [a for a in areas if a["split"] == "Roark"]
    drawn = set()
    pending = list(areas)
    step = 0

    def kill(k, when):
        for _ in range(k):
            alive = [m for m in box.members if m["alive"]]
            if not alive:
                return
            m = rng.choice(alive)
            m["alive"] = False
            log.append({"death": m["species"], "caught_at": m["area"], "when": when})

    def usable(opt, now_split):
        if opt.repel is not None and rank.get(opt.split, 99) == 0 and repel_used:
            return False
        return rank.get(opt.split, 99) <= rank.get(now_split, 99)

    def repel_gain(a):
        # What the one early repel would add at this area, with the box as
        # it stands: the best repel option's gain over the best without.
        plain = max((expected_gain(o, box, drawn) for o in a["options"]
                     if o.repel is None and o.split == "Roark"), default=0.0)
        rep = max((expected_gain(o, box, drawn) for o in a["options"]
                   if o.repel is not None and o.split == "Roark"), default=0.0)
        return rep - plain

    def margin(best, other):
        return round((best - other) / best, 3) if best > 0 else 0.0

    while pending:
        a = pending.pop(0)
        kill(death_at.pop(step, 0), f"before {a['name']}")
        step += 1
        now = a["split"]
        gives = can_give(a)
        if a["name"] in locks:
            sp = locks[a["name"]]
            entry = {"area": a["name"], "split": now, "locked": True, "can_give": gives,
                     "options": [], "decision": "your pick"}
            if not sp:
                entry.update(choice=None, species=None, value=None, note="left unused, your pick")
            else:
                entry.update(choice="your pick", species=sp, value=box.add(sp, a["name"]))
            log.append(entry)
            continue
        opts = [o for o in a["options"] if usable(o, now)]
        # The early repel goes where it gains most among the Roark areas
        # still to come, judged again at each one.
        if now == "Roark" and not repel_used:
            here = repel_gain(a)
            rest = [repel_gain(b) for b in roark if b in pending]
            if rest and here < max(rest):
                opts = [o for o in opts if o.repel is None]
        scored = sorted(((expected_gain(o, box, drawn), o) for o in opts),
                        key=lambda t: -t[0])
        later = [o for o in a["options"] if rank.get(o.split, 99) > rank.get(now, 99)
                 and not (o.repel is not None and rank.get(o.split, 99) == 0)]
        best_later = max(((expected_gain(o, box, drawn), o) for o in later),
                         key=lambda t: t[0], default=(0.0, None))
        best_now = scored[0] if scored else (0.0, None)
        if best_later[1] is not None and best_later[0] > best_now[0] * DEFER_MARGIN:
            # Wait for the later table: come back to this place when it opens.
            opt = best_later[1]
            back = dict(a, split=opt.split, options=a["options"])
            at = next((i for i, b in enumerate(pending)
                       if rank.get(b["split"], 99) > rank.get(opt.split, 99)), len(pending))
            pending.insert(at, back)
            log.append({"area": a["name"], "split": now, "wait": opt.label,
                        "until": opt.split, "decision": f"wait for the {opt.label}",
                        "margin": margin(best_later[0], best_now[0])})
            continue
        ev, opt = best_now
        second = scored[1][0] if len(scored) > 1 else 0.0
        entry = {"area": a["name"], "split": now, "can_give": gives,
                 "options": [{"label": o.label, "gain": round(g, 1)} for g, o in scored[:4]]}
        if opt is None or ev <= 0:
            entry.update(choice=None, species=None, value=None, decision="nothing new",
                         margin=0.0, note="nothing here the box does not already have")
            log.append(entry)
            continue
        entry.update(decision=opt.label, margin=margin(ev, max(second, best_later[0])))
        sp = _roll(opt, box, rng, drawn)
        if opt.kind == "legendary":
            drawn.add(sp)
        if opt.repel is not None and rank.get(opt.split, 99) == 0:
            repel_used = True
        if opt.requires:
            pay = box.payment(opt.requires)
            pay["alive"], pay["traded"] = False, True
            entry["traded_away"] = dex.display_name(pay["species"])
        entry.update(choice=opt.label, species=sp, value=box.add(sp, a["name"]),
                     expected=round(ev, 1))
        log.append(entry)
    kill(death_at.pop(step, 0), "at the end of the split")
    for k in list(death_at):
        kill(death_at.pop(k), "at the end of the split")

    alive = box.alive_values()
    name = lambda sp: {"value": sp, "label": dex.display_name(sp)}
    return {
        "split": target, "cap": values.cap, "deaths": deaths, "seed": seed,
        "starter": starter, "locks": locks,
        "log": [dict(e, label=dex.display_name(e["species"]),
                     can_give=[name(sp) for sp in e.get("can_give", [])])
                if e.get("species")
                else dict(e, label=dex.display_name(e["death"])) if e.get("death")
                else dict(e, can_give=[name(sp) for sp in e.get("can_give", [])]) for e in log],
        "box": [dict(m, label=dex.display_name(m["species"]),
                     stage=values.stage(m["species"]),
                     stage_label=dex.display_name(values.stage(m["species"])))
                for m in sorted(box.members, key=lambda m: -m["value"])],
        "alive": len(alive),
        "dead": sum(1 for m in box.members if not m["alive"] and not m["traded"]),
        "worth": round(box_value(alive), 1),
        "sum_alive": round(sum(alive), 1),
        "top_six": round(sum(sorted(alive, reverse=True)[:6]), 1),
    }


def confidence(target, deaths=0, starter=None, locks=None, start=None, runs=40, areas=10,
               seed=0, root=None):
    """How sure the sim is of its calls at the next `areas` places not yet
    decided (Ian's request 3). It plays `runs` runs from the same state with
    different luck and, for each place, reports the call most runs make there
    (catch with an option, or wait for a later table), the share of runs that
    make it, and the mean margin of that call over the next best. The first
    place's margin is exact, since the box it meets is known; later places
    depend on earlier luck, which the share measures."""
    ctx = context(target, root)
    order, tally, margins = [], {}, {}
    for i in range(runs):
        out = run(target, deaths, starter, seed * 1000 + i, root, locks, start, ctx)
        seen = set()
        for e in out["log"]:
            name = e.get("area")
            if not name or e.get("from_save") or e.get("locked") or e.get("death") \
                    or name in seen or "decision" not in e:
                continue
            seen.add(name)
            if name not in tally:
                order.append(name)
                tally[name] = collections.Counter()
                margins[name] = collections.defaultdict(list)
            tally[name][e["decision"]] += 1
            margins[name][e["decision"]].append(e.get("margin") or 0.0)
    rows = []
    for name in order[:areas]:
        total = sum(tally[name].values())
        calls = tally[name].most_common()
        top, n = calls[0]
        rows.append({"area": name, "decision": top, "share": round(n / total, 2),
                     "margin": round(sum(margins[name][top]) / len(margins[name][top]), 2),
                     "others": [{"decision": d, "share": round(k / total, 2)} for d, k in calls[1:4]],
                     "runs": total})
    return {"split": target, "runs": runs, "areas": rows}


# -- the per-area analysis ------------------------------------------------------


def area_values(target, root=None):
    """Every capture area up to `target`, each option's expected worth to an
    empty box at that split, best first. The design aid Ian asked to keep
    in code: it shows where the prizes cluster and which areas are flat."""
    root = root or model.repo_root()
    sidecar = model.load_sidecar() or {}
    values = Values(root, target, sidecar)
    box = Box(root, values)
    rows = []
    for a in world(target, root):
        scored = sorted(((expected_gain(o, box), o) for o in a["options"]),
                        key=lambda t: -t[0])
        rows.append({"area": a["name"], "split": a["split"],
                     "options": [(o.label, o.split, round(g, 1)) for g, o in scored]})
    return rows


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("--split", default="League")
    p.add_argument("--deaths", type=int, default=0)
    p.add_argument("--starter")
    p.add_argument("--seed", type=int)
    p.add_argument("--areas", metavar="SPLIT",
                   help="print every area's options by worth to an empty box")
    args = p.parse_args(argv)
    if args.areas:
        for r in area_values(args.areas):
            best = r["options"][0]
            print(f"{r['split']:9} {r['area']:28} {best[2]:6.1f}  {best[0]}")
            for label, split, g in r["options"][1:4]:
                print(f"{'':38} {g:6.1f}  {label} ({split})")
        return 0
    out = run(args.split, args.deaths, args.starter, args.seed)
    for e in out["log"]:
        if e.get("death"):
            print(f"  died: {e['label']} (from {e['caught_at']}), {e['when']}")
        elif e.get("wait"):
            print(f"{e['split']:9} {e['area']:28} waits for {e['wait']} ({e['until']})")
        elif e.get("species"):
            print(f"{e['split']:9} {e['area']:28} {e['label']:14} {e['value']:5.1f}  {e['choice']}")
        else:
            print(f"{e['split']:9} {e['area']:28} nothing new")
    print(f"\n{out['alive']} alive, {out['dead']} dead; worth {out['worth']} "
          f"(sum {out['sum_alive']}, best six {out['top_six']})")
    return 0


if __name__ == "__main__":
    sys.exit(main())

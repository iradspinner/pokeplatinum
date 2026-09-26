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
BST_FLOOR, BST_CEIL = 250, 600
# Ian: "I'd rather have 10 decent Pokemon than only 6 great ones", so the
# best six add a small bonus on top of the sum of everything alive.
TOP_SIX_WEIGHT = 0.25
# A later option is waited for only when it beats the best one now by this.
DEFER_MARGIN = 1.05
HONEY_FROM = "Gardenia"          # Honey is sold in Floaroma, Gardenia's split
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
            self.rating = json.load(f)["lines"]
        self.on_list = audit.on_list(root)
        self.pick_tier = {}
        for row in dex.pick_list(root):
            if row.get("constant"):
                self.pick_tier[dex.line_of(root, row["constant"])] = row.get("tier") or ""

    @functools.lru_cache(maxsize=None)
    def stage(self, species):
        return evolve.stage_at(self.root, species, self.cap, self.on_list)

    @functools.lru_cache(maxsize=None)
    def of(self, species):
        stage = self.stage(species)
        try:
            bst = pokedex.load(self.root, stage)["bst"]
        except Exception:
            bst = BST_FLOOR
        line = dex.line_of(self.root, species)
        bst_score = 100 * min(1.0, max(0.0, (bst - BST_FLOOR) / (BST_CEIL - BST_FLOOR)))
        tier = TIER_SCORE.get(self.rating.get(line), 40)
        # A line's rating is for its final form; a stage short of it by the
        # cap is worth that share of it, measured by BST.
        final = max((pokedex.load(self.root, m)["bst"]
                     for m in dex.members_of_line(self.root, line)
                     if os.path.isdir(os.path.join(self.root, "res", "pokemon",
                                                   pokedex.folder_of(m)))),
                    default=bst)
        tier *= min(1.0, bst / final) if final else 1.0
        pick = PICK_SCORE.get(self.pick_tier.get(line), 40)
        return round(W_BST * bst_score + W_TIER * tier + W_PICK * pick, 1)


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
    alive = box.alive_values()
    live = _live(option.shares, box, drawn)
    if not live:
        return 0.0
    if option.requires:
        pay = box.payment(option.requires)
        if pay is None:
            return 0.0
        rest = list(alive)
        rest.remove(pay["value"])
        return sum(p * (box_value(rest + [box.values.of(sp)]) - box_value(alive))
                   for sp, p in live.items())
    if option.kind == "choice":
        return max(gain(box.values.of(sp), alive) for sp in live)
    return sum(p * gain(box.values.of(sp), alive) for sp, p in live.items())


def _roll(option, box, rng, drawn=()):
    live = _live(option.shares, box, drawn)
    if not live:
        return None
    if option.kind == "choice":
        return max(live, key=box.values.of)
    r, acc = rng.random(), 0.0
    for sp, p in sorted(live.items()):
        acc += p
        if r <= acc:
            return sp
    return sorted(live)[-1]


def run(target, deaths=0, starter=None, seed=None, root=None):
    """Play one run to the end of `target`. Returns the log, the box and its
    worth, as plain data for the tool and the command line."""
    root = root or model.repo_root()
    sidecar = model.load_sidecar() or {}
    rank = progression.split_index(sidecar)
    if target not in rank:
        raise ValueError(f"no such split: {target}")
    rng = random.Random(seed)
    values = Values(root, target, sidecar)
    box = Box(root, values)
    areas = world(target, root)
    starters = next(s["pool"] for s in scripted.load(root) if s["kind"] == "starter")
    starter = starter or rng.choice(starters)
    log = [{"area": "Route 201", "split": "Roark", "choice": "the starter",
            "species": starter, "value": box.add(starter, "Route 201"), "options": []}]
    # The starter is Route 201's capture (scripted-sources.md).
    areas = [a for a in areas if a["name"] != "Route 201"]

    # Deaths land between captures, at random points of the run.
    n = len(areas)
    death_at = collections.Counter(rng.randrange(n + 1) for _ in range(max(0, deaths)))
    repel_used = False
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

    while pending:
        a = pending.pop(0)
        kill(death_at.pop(step, 0), f"before {a['name']}")
        step += 1
        now = a["split"]
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
                        "until": opt.split})
            continue
        ev, opt = best_now
        entry = {"area": a["name"], "split": now,
                 "options": [{"label": o.label, "gain": round(g, 1)} for g, o in scored[:4]]}
        if opt is None or ev <= 0:
            entry.update(choice=None, species=None, value=None,
                         note="nothing here the box does not already have")
            log.append(entry)
            continue
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
    return {
        "split": target, "cap": values.cap, "deaths": deaths, "seed": seed,
        "starter": starter,
        "log": [dict(e, label=dex.display_name(e["species"])) if e.get("species")
                else dict(e, label=dex.display_name(e["death"])) if e.get("death")
                else e for e in log],
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

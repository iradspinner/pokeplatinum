"""The scripted captures and the honey trees, as the area list and the box
simulator see them.

`docs/oxide/encounters/scripted.json` names every scripted capture (the
starter, gifts, trades, statics, fossils, eggs) with its capture area, split
and play order; the species and levels come from the sources catalogue that
`tools/oxide/pokemon_sources.py` writes, so a gift edited in its script shows
here on the next regeneration without anyone copying it across. The honey
trees are read from the engine's own list of tree maps and from the honey
tables.

Read-only, like `locations.py`.
"""
import csv
import functools
import json
import os
import re

from . import availability
from . import locations
from . import model

SCRIPTED = os.path.join("docs", "oxide", "encounters", "scripted.json")
HONEY_TREE_C = os.path.join("src", "overlay005", "honey_tree.c")
HEADERS = os.path.join("include", "data", "map_headers.h")
KINDS = ("starter", "gift", "trade", "static", "fossil", "egg")
PICKS = ("random", "choice", "legendary_pool")
KEY_PREFIX = "scripted:"
HONEY_PREFIX = "honey:"


def _catalogue(root):
    path = os.path.join(root, availability.SOURCES)
    with open(path, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def _legendary_pool(root, key):
    """The third of the legendary pool one lake cavern draws from."""
    plan = availability.load_plan()
    return list(((plan.get("pool") or {}).get("thirds") or {}).get(key) or [])


def load(root=None):
    """Every scripted source, resolved: the file's entry plus `pool` (the
    species it can give, in the catalogue's order), `level`, `key` (what
    the caught file stores it under), `shares_table` (whether a wild table
    has the same location name) and `order` (its own, or its location's
    first table's). Raises ValueError on a source that matches nothing."""
    root = root or model.repo_root()
    with open(os.path.join(root, SCRIPTED), encoding="utf-8") as f:
        spec = json.load(f)
    rows = _catalogue(root)
    wild = locations.by_location(root)
    sidecar = (model.load_sidecar() or {}).get("areas") or {}
    out = []
    for src in spec["sources"]:
        s = dict(src)
        if s["kind"] not in KINDS or s["pick"] not in PICKS:
            raise ValueError(f"{s['id']}: unknown kind or pick")
        if s["pick"] == "legendary_pool":
            s["pool"] = _legendary_pool(root, s["pool_key"])
        elif not s.get("pool"):
            want = s["from"]
            hits = [r for r in rows if r["map_or_file"] == want["file"]
                    and ("level" not in want or r["level"] == want["level"])]
            if not hits:
                raise ValueError(f"{s['id']}: nothing in the sources catalogue "
                                 f"matches {want}")
            s["pool"] = list(dict.fromkeys(r["species"] for r in hits))
            if "level" not in s:
                levels = {r["level"] for r in hits}
                s["level"] = int(levels.pop()) if len(levels) == 1 and \
                    next(iter(levels)).isdigit() else None
        s["key"] = KEY_PREFIX + s["id"]
        area = s.get("capture_area")
        stems = wild.get(area) or []
        s["shares_table"] = bool(stems)
        if s.get("order") is None:
            orders = [sidecar.get(st, {}).get("order") for st in stems]
            orders = [o for o in orders if o is not None]
            s["order"] = min(orders) if orders else None
        s.setdefault("simulate", True)
        s.setdefault("planned", False)
        out.append(s)
    return out


def by_key(root=None):
    return {s["key"]: s for s in load(root)}


# -- the honey trees ---------------------------------------------------------


@functools.lru_cache(maxsize=None)
def _header_labels(root):
    """{map header: label id} for every header."""
    with open(os.path.join(root, HEADERS), encoding="utf-8") as f:
        text = f.read()
    out = {}
    for header, body in re.findall(r"\[(MAP_HEADER_\w+)\] = \{(.*?)\n    \},", text, re.S):
        label = re.search(r"\.mapLabelTextID = (\w+)", body)
        if label:
            out[header] = label.group(1)
    return out


def honey_tree_maps(root=None):
    """The map headers with a honey tree, in the engine's tree order."""
    root = root or model.repo_root()
    with open(os.path.join(root, HONEY_TREE_C), encoding="utf-8") as f:
        text = f.read()
    block = re.search(r"sHoneyTreeMapHeaderIDs\[[^\]]*\]\s*=\s*\{(.*?)\};", text, re.S)
    return re.findall(r"MAP_HEADER_\w+", block.group(1))


def honey_tree_locations(root=None):
    """{location name: number of trees there}, in tree order."""
    root = root or model.repo_root()
    labels = _header_labels(root)
    names = locations.label_names(root)
    out = {}
    for header in honey_tree_maps(root):
        name = names.get(labels.get(header), header)
        out[name] = out.get(name, 0) + 1
    return out


def honey_tree_stems(root=None):
    """{encounter file: number of trees on its maps}: the tables that stand
    where a tree does. The capture is the location's, but the tree is shown
    on the table whose map it is on, not on every floor of the Lost Tower."""
    root = root or model.repo_root()
    trees = honey_tree_maps(root)
    out = {}
    placed = set()
    for stem, uses in locations.header_uses(root).items():
        n = sum(trees.count(header) for header, _ in uses)
        if n:
            out[stem] = n
            placed.update(h for h, _ in uses if h in trees)
    # A tree on a map with no table of its own (the clearing outside Eterna
    # Forest) belongs to its location's first table in play order. One at a
    # place with no table at all (Floaroma Meadow) is shown with that
    # place's gift instead.
    labels = _header_labels(root)
    names = locations.label_names(root)
    wild = locations.by_location(root)
    sidecar = (model.load_sidecar() or {}).get("areas") or {}
    for header in trees:
        if header in placed:
            continue
        stems = wild.get(names.get(labels.get(header)))
        if stems:
            first = min(stems, key=lambda st: sidecar.get(st, {}).get("order") or 1e9)
            out[first] = out.get(first, 0) + 1
    return out


def honey_table_for(split, split_rank, tables=None):
    """The honey table a tree shaken in `split` reads: the one for the
    badges the player holds then. A split is named for the gym that ends it,
    so the player holds as many badges as there are gym splits before it;
    HQ and Galactic sit between Candice and Volkner without a gym of their
    own, so both read the seven-badge table."""
    tables = tables if tables is not None else model.honey_tree_tables()
    gyms = ("Roark", "Gardenia", "Fantina", "Maylene", "Wake", "Byron",
            "Candice", "Volkner", "League")
    rank = split_rank.get(split)
    if rank is None:
        return None
    badges = sum(1 for g in gyms[:8] if split_rank.get(g, 99) < rank)
    return tables[max(badges, 1) - 1]

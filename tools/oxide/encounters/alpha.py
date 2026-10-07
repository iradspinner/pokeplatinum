"""The alpha checklist (alpha readiness step 17; Ian, 2026-10-06): every zone
of the game in walking order, split by split, with what the player meets
there, for Ian to work through in the alpha run.

    PYTHONPATH=. python3 -m tools.oxide.encounters.alpha [--split Roark]

Ian's words: "when I get to Route 202, I should fight x mandatory trainers,
y optional trainers with z rewards, x hidden items, etc." A zone is a place
name as the game shows it on the map popup (every room of a town or a cave
counts under its name), and it appears once in each split it has something
in. Everything is read from the tree when the page loads, so the page
follows the later steps (the reward placements, the combed teams) with no
hand edits:

  trainers     the story bosses (tools/oxide/balance/fights.json) and every
               ordinary trainer the balance census places, with its role,
               reward and gauntlet section (docs/oxide/trainer-roles.tsv);
               each one's team from res/trainers/data, its split as the
               Trainers tab places it
  pickups      item balls and hidden items, with the split the census's
               reach opens each in and the field move that opens it
  gifts        items an NPC script gives
  rewards      the reward table's placements (docs/oxide/reward-placements.tsv):
               a trainer's reward on its row, a ball or gift matched to the
               place it replaces, the shop and Game Corner TMs with their
               badge counts
  wild         the zone's encounter tables and scripted captures
  checks       the in-game checklist's items that belong to the zone

The two TSVs are the balance track's. Until `balance-tm-pass` lands they
exist only there, so they are read from that branch; once on `oxide`, the
working tree's copy wins and the fallback goes unused. Read-only: nothing
here writes the tree.
"""
import argparse
import collections
import csv
import functools
import io
import json
import os
import re
import subprocess

from . import dex, locations, model, scripted, trainers
from ..balance import splits as bsplits

SPLITS = list(bsplits.SPLITS)
TABLES = {"roles": "docs/oxide/trainer-roles.tsv",
          "rewards": "docs/oxide/reward-placements.tsv",
          "tms": "docs/oxide/tm-list.tsv"}
FALLBACK_REF = "origin/balance-tm-pass"
CHECKLIST = os.path.join("docs", "oxide", "ingame-checklist.md")
CHECK_ZONES = os.path.join("docs", "oxide", "encounters", "alpha-check-zones.json")
FIGHTS = os.path.join("tools", "oxide", "balance", "fights.json")
HIDDEN_ITEM_SCRIPT = 8000

# Places the encounter sidecar gives no walking position, since they hold no
# wild table: each follows the place named, in that order where several
# follow one. A test fails on any zone with content and no position.
ZONE_AFTER = {
    "Trainers’ School": "Jubilife City",
    "Oreburgh City": "Oreburgh Gate",
    "Floaroma Meadow": "Floaroma Town",
    "Flower Shop": "Floaroma Town",
    "T.G. Eterna Bldg": "Eterna City",
    "Cycle Shop": "Eterna City",
    "Hearthome City": "Route 208",
    "Café": "Route 210",
    "Pokémon Day Care": "Solaceon Town",
    "Veilstone City": "Route 215",
    "Veilstone Store": "Veilstone City",
    "Game Corner": "Veilstone City",
    "Galactic HQ": "Veilstone City",
    "Pokémon Mansion": "Route 212",
    "Grand Lake": "Valor Lakefront",
    "Restaurant": "Valor Lakefront",
    "Valor Cavern": "Lake Valor",
    "Ironworks Hall": "Fuego Ironworks",
    "Fight Area": "Snowpoint City",
    "Survival Area": "Route 225",
    "Spear Pillar": "Mt. Coronet",
    "Distortion World": "Spear Pillar",
    "Battleground": "Route 225",
    "Battle Park": "Fight Area",
    "Fullmoon Island": "Canalave City",
    "Mining Museum": "Oreburgh City",
    "Acuity Cavern": "Lake Acuity",
    "Iron Ruins": "Iron Island",
    "Iceberg Ruins": "Route 217",
    "Rock Peak Ruins": "Route 228",
}


# ---- sources -------------------------------------------------------------

def _tsv_text(root, rel):
    """(text, where): the working tree's copy, else the fallback branch's,
    else None."""
    path = os.path.join(root, rel)
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            return f.read(), "working tree"
    try:
        return model._read(rel, ref=FALLBACK_REF), FALLBACK_REF
    except subprocess.CalledProcessError:
        return None, None


@functools.lru_cache(maxsize=None)
def tables(root):
    """{name: (rows, where)} for the three balance tables, comment lines
    dropped. A table found nowhere is ([], None)."""
    out = {}
    for name, rel in TABLES.items():
        text, where = _tsv_text(root, rel)
        rows = list(csv.DictReader(io.StringIO("".join(
            l for l in (text or "").splitlines(True) if not l.startswith("#"))), delimiter="\t"))
        out[name] = (rows, where)
    return out


def _bare(header):
    return header[len("MAP_HEADER_"):] if header and header.startswith("MAP_HEADER_") else header


def zone_of(header):
    """The place name the game shows for a map header (with or without its
    prefix), or None."""
    try:
        return bsplits.location_name(_bare(header))
    except KeyError:
        return None


@functools.lru_cache(maxsize=None)
def _trainer_ids(root):
    from . import calc_trainers
    return calc_trainers._tables(root)["ids"]


def _stem(constant):
    return constant[len("TRAINER_"):].lower()


def _earliest_map(maps):
    return min(maps, key=lambda h: (SPLITS.index(bsplits.map_split(h)[0])
                                    if bsplits.map_split(h)[0] in SPLITS else len(SPLITS), h))


def trainer_map(root, constant):
    """The map a trainer is fought on: its sight trainer's or the script
    that battles it, the earliest by split; else a map whose script names
    it; else None."""
    tr = _trainer_ids(root).get(constant)
    if tr is None:
        return None
    for maps in (bsplits.trainer_maps().get(tr), bsplits.trainer_mentions().get(tr)):
        if maps:
            return "MAP_HEADER_" + _earliest_map(maps)
    return None


def team(root, constant):
    """[{species, label, level, item}] as the trainer's file has it."""
    try:
        data = trainers.load(root, _stem(constant))
    except (KeyError, FileNotFoundError):
        return []
    out = []
    for m in data.get("party") or []:
        sp = m.get("species")
        out.append({"species": sp, "label": dex.display_name(sp) if sp else "?",
                    "level": m.get("level"), "item": m.get("item")})
    return out


def _trainer_name(root, constant):
    try:
        data = trainers.load(root, _stem(constant))
    except (KeyError, FileNotFoundError):
        return constant
    cls = (data.get("class") or "").replace("TRAINER_CLASS_", "").replace("_", " ").title()
    name = data.get("name") or ""
    return f"{cls} {name}".strip() or constant


# ---- the in-game checklist ------------------------------------------------

_ITEM = re.compile(r"^- \[( |x)\] (.*?)(?=^- \[|^#|\Z)", re.M | re.S)
_TITLE = re.compile(r"\*\*(.+?)\*\*")


LIVE = "**(live)**"


def checklist_items(root):
    """[{key, title, done, live, section, text}] for every box in the
    checklist. An item's key is its bold title, else its first eight words
    ("(live)", which marks a check an agent reads over the GDB stub, is not a
    title), so a wording change later in the item keeps its mapping; a key
    met twice gets its count after it."""
    with open(os.path.join(root, CHECKLIST), encoding="utf-8") as f:
        text = f.read()
    out, section, seen = [], "", collections.Counter()
    nxt = re.compile(r"^(- \[|#)", re.M)
    for m in re.finditer(r"^## (.+)$|^- \[( |x)\] ", text, re.M):
        if m.group(1):
            section = m.group(1).strip()
            continue
        end = nxt.search(text, m.end())
        body = " ".join(text[m.end(): end.start() if end else len(text)].split())
        live = body.startswith(LIVE)
        if live:
            body = body[len(LIVE):].strip()
        title = _TITLE.match(body)
        key = title.group(1).strip() if title else " ".join(body.split()[:8])
        seen[key] += 1
        if seen[key] > 1:
            key = f"{key} ({seen[key]})"
        out.append({"key": key, "done": m.group(2) == "x", "live": live,
                    "section": section, "text": body})
    return out


@functools.lru_cache(maxsize=None)
def _check_overrides(root):
    path = os.path.join(root, CHECK_ZONES)
    if not os.path.exists(path):
        return {}
    with open(path, encoding="utf-8") as f:
        return {k: v for k, v in json.load(f)["overrides"].items() if not k.startswith("_")}


ANYWHERE = ("anywhere", None)


def check_names(first_split, trainer_places):
    """{a name a checklist item may use: (zone, split)}: every zone's own
    name and a town's or city's bare name ("Sandgem") at the zone's first
    split, and every trainer's and boss's name ("Camper Zackary",
    "Volkner") at the trainer's own zone and split."""
    out = {}
    for z, s in first_split.items():
        out[z] = (z, s)
        for tail in (" Town", " City"):
            if z.endswith(tail):
                out.setdefault(z[: -len(tail)], (z, s))
    for name, place in trainer_places.items():
        out.setdefault(name, place)
    return out


def check_zone(item, names, overrides, first_split):
    """(zone, split) for a checklist item: the override file's (a zone, or
    "zone|split" for a later visit), else the place of the first name the
    item's text uses (the longer name wins at one place, so "Route 210" is
    not read as "Route 21"), else ANYWHERE."""
    if item["key"] in overrides:
        zone, _bar, split = overrides[item["key"]].partition("|")
        return (zone, split or first_split.get(zone)) if zone != "anywhere" else ANYWHERE
    text = item["text"]
    best = None
    for n in sorted(names, key=len, reverse=True):
        i = re.search(r"(?<![\w])" + re.escape(n) + r"(?![\w])", text)
        if i and (best is None or i.start() < best[0]):
            best = (i.start(), n)
    return names[best[1]] if best else ANYWHERE


# ---- building the page ----------------------------------------------------

def _wild(root):
    """[(split, zone, row)] for every encounter table a header uses, under
    its land split, or its water split when it has no grass."""
    sc = (model.load_sidecar() or {}).get("areas") or {}
    names = locations.label_names(root)
    out = []
    for a in model.load_all():
        uses = locations.header_uses(root).get(a.name)
        if not uses:
            continue
        e = sc.get(a.name) or {}
        split = e.get("split") if a.land_active else (e.get("water_split") or e.get("split"))
        if split not in SPLITS:
            continue
        zone = names.get(uses[0][1], uses[0][1])
        species = []
        for k in ("land", *[k for k in a.kinds_present() if k != "land"]):
            for sp, *_ in (a.kind_slots(k) if k != "land" or a.land_active else []):
                if sp not in species:
                    species.append(sp)
        out.append((split, zone, {"area": a.name, "label": _area_label(a.name),
                                  "kinds": a.kinds_present() if not a.land_active
                                  else ["land"] + [k for k in a.kinds_present() if k != "land"],
                                  "species": [dex.display_name(s) for s in species]}))
    return out


@functools.lru_cache(maxsize=None)
def _script_headers():
    """{script file stem: the first map header that runs it}."""
    out = {}
    for h, fields in sorted(bsplits.headers().items()):
        stem = fields.get("scriptsArchiveID")
        if stem:
            out.setdefault(stem, h)
    return out


def scripted_zone(s):
    """Where a scripted capture is handed over: the zone of the map whose
    script gives it (Cynthia's egg is Eterna City's, though it counts where
    it hatches), else its capture area, else its label."""
    stem = ((s.get("from") or {}).get("file") or "")
    header = _script_headers().get(stem[:-2] if stem.endswith(".s") else stem)
    return (zone_of(header) if header else None) or s.get("capture_area") or s.get("label")


def _area_label(name):
    from . import server
    return server._area_label(name)


def build(root=None):
    """The whole checklist: {"splits": [{split, cap, zones: [...]}],
    "sources": {...}, "unplaced": [...]}. Each zone holds trainers,
    gauntlets, pickups, gifts, shop, wild, scripted and checks."""
    root = root or model.repo_root()
    tabs = tables(root)
    roles, roles_from = tabs["roles"]
    rewards, rewards_from = tabs["rewards"]
    caps = trainers.caps()
    smap = trainers.split_map(root)
    zones = collections.defaultdict(lambda: collections.defaultdict(list))   # (split, zone) -> kind -> rows
    unplaced = []

    def put(split, zone, kind, row):
        if split not in SPLITS or not zone:
            unplaced.append({"kind": kind, "split": split, "zone": zone, "row": row})
            return
        zones[(split, zone)][kind].append(row)

    # Trainer rewards from the reward table, by trainer.
    reward_of = collections.defaultdict(list)
    for r in rewards:
        if r.get("kind") == "trainer" and r.get("trainer_id"):
            reward_of[r["trainer_id"]].append({"item": r["reward"], "copies": int(r.get("copies") or 1)})

    # The story bosses, one row a fight; a rival fight's three starter
    # variants are one row, each variant's team kept.
    with open(os.path.join(root, FIGHTS), encoding="utf-8") as f:
        fights = json.load(f)["fights"]
    boss_constants = set()
    for fight in fights:
        consts = [c for c in fight["trainers"] if c in _trainer_ids(root)]
        boss_constants.update(consts)
        if not consts:
            continue
        header = next((h for h in (trainer_map(root, c) for c in consts) if h), None)
        put(fight["split"], zone_of(header), "trainers", {
            "key": fight["key"], "name": fight["label"], "kind": "boss", "required": True,
            "constants": consts, "map": header, "tag": bool(fight.get("tag")),
            "teams": [{"constant": c, "team": team(root, c)} for c in consts],
            "rewards": [x for c in consts for x in reward_of.get(c, [])], "rated": True})

    # Every ordinary trainer the census places.
    for r in roles:
        c = r["trainer_id"]
        if c in boss_constants:
            continue
        header = r.get("map") or trainer_map(root, c)
        split = r.get("split") or smap.get(_stem(c))
        role = r.get("role") or "none"
        # A trainer the table plans and the main track has yet to create
        # (step 10's Game Corner challenger) has no file and no team yet.
        planned = not os.path.exists(trainers.path_of(root, _stem(c)))
        name = r.get("trainer") or ""
        if planned or not name or name.startswith("new"):
            name = c[len("TRAINER_"):].replace("_", " ").title() if planned else _trainer_name(root, c)
        put(split, zone_of(header), "trainers", {
            "key": c, "name": name, "planned": planned,
            "kind": "gauntlet" if role == "gauntlet" else "trainer",
            "required": r.get("required") == "yes", "constants": [c], "map": header,
            "section": r.get("section") or None, "role": role,
            "teams": [{"constant": c, "team": team(root, c)}],
            "rewards": reward_of.get(c, []), "rated": role == "gauntlet",
            "reading": r.get("reading") or None})

    # Balls and hidden items, each with its pickup flag.
    flags = bsplits.flag_values()
    for key, (row, maps) in bsplits.pickups().items():
        split, header, item, how, needs = row
        if how == "hidden":
            flag = flags["HIDDEN_ITEM_FLAGS_START"] + key - HIDDEN_ITEM_SCRIPT
            flag_name = None
        else:
            flag_name = key if isinstance(key, str) else None
            flag = flags.get(flag_name) if flag_name else None
        put(split, zone_of(header), "pickups", {
            "item": item, "how": how, "needs": needs, "map": "MAP_HEADER_" + header,
            "flag": flag, "flag_name": flag_name, "placed": None})

    # Items NPC scripts give.
    for split, header, item in bsplits.gifts():
        put(split, zone_of(header), "gifts", {"item": item, "map": "MAP_HEADER_" + header, "placed": None})

    # The reward table: balls and gifts matched to the place they replace
    # (or, once step 10 has placed them, to the place that holds them),
    # shop and Game Corner TMs listed with their badge counts.
    for r in rewards:
        kind = r.get("kind")
        if kind == "trainer":
            continue
        zone, split = zone_of(r.get("map")), r.get("split")
        reward = {"item": r["reward"], "copies": int(r.get("copies") or 1),
                  "badges": int(r["badges"]) if (r.get("badges") or "").isdigit() else None,
                  "replaces": r.get("replaces") or None, "note": r.get("note") or ""}
        if kind in ("mart", "prize"):
            put(split, zone, "shop", dict(reward, kind=kind))
            continue
        bucket = "pickups" if kind == "ball" else "gifts"
        rows = [x for z in [zones.get((s, zone)) for s in SPLITS] if z for x in z[bucket]
                if x["map"] == r.get("map") and x["placed"] is None]
        hit = next((x for x in rows if x["item"] == r["reward"]), None) \
            or next((x for x in rows if x["item"] == r.get("replaces")), None)
        if hit:
            hit["placed"] = reward
        else:
            put(split, zone, bucket, {"item": None, "how": kind, "needs": None, "map": r.get("map"),
                                      "flag": None, "flag_name": None, "placed": reward})

    for split, zone, row in _wild(root):
        put(split, zone, "wild", row)
    for s in scripted.load(root):
        put(s.get("split"), scripted_zone(s), "scripted", {
            "label": s["label"], "kind": s["kind"], "pool": [dex.display_name(x) for x in s["pool"]],
            "level": s.get("level"), "planned": bool(s.get("planned"))})

    # The checklist's items, by zone; "anywhere" sits before the first split.
    first_split = {}
    for s, z in sorted(zones, key=lambda k: SPLITS.index(k[0])):
        first_split.setdefault(z, s)
    trainer_places = {}
    for (s, z), kinds in sorted(zones.items(), key=lambda kv: SPLITS.index(kv[0][0])):
        for t in kinds.get("trainers", []):
            trainer_places.setdefault(t["name"], (z, s))
    names = check_names(first_split, trainer_places)
    overrides = _check_overrides(root)
    anywhere = []
    for item in checklist_items(root):
        z, s = check_zone(item, names, overrides, first_split)
        item = dict(item, zone=z, split=s)
        if (s, z) not in zones:
            anywhere.append(item)
            continue
        zones[(s, z)]["checks"].append(item)

    order = zone_order(root)
    out = []
    for split in SPLITS:
        zs = [z for s, z in zones if s == split]
        zs.sort(key=lambda z: (order.get(z, 1e9), z))
        out.append({"split": split, "cap": caps.get(split),
                    "zones": [dict(_zone_view(z, zones[(split, z)]), order=order.get(z)) for z in zs]})
    return {"splits": out, "anywhere": anywhere, "unplaced": unplaced,
            "sources": {"roles": roles_from, "rewards": rewards_from}}


def _zone_view(zone, kinds):
    trainers_ = kinds.get("trainers", [])
    return {
        "zone": zone,
        "trainers": [t for t in trainers_ if t["kind"] != "gauntlet"],
        "gauntlets": _sections(t for t in trainers_ if t["kind"] == "gauntlet"),
        "pickups": kinds.get("pickups", []),
        "gifts": kinds.get("gifts", []),
        "shop": kinds.get("shop", []),
        "wild": kinds.get("wild", []),
        "scripted": kinds.get("scripted", []),
        "checks": kinds.get("checks", []),
        "counts": counts(kinds),
    }


def _sections(rows):
    by = collections.OrderedDict()
    for t in rows:
        by.setdefault(t.get("section") or "?", []).append(t)
    return [{"section": k, "trainers": v} for k, v in by.items()]


def counts(kinds):
    """What a zone's header line says: the numbers Ian checks off."""
    tr = kinds.get("trainers", [])
    pk = kinds.get("pickups", [])
    return {
        "mandatory": sum(1 for t in tr if t["required"] and t["kind"] != "gauntlet"),
        "optional": sum(1 for t in tr if not t["required"] and t["kind"] != "gauntlet"),
        "rewards": sum(1 for t in tr if t["rewards"]),
        "gauntlet": sum(1 for t in tr if t["kind"] == "gauntlet"),
        "balls": sum(1 for p in pk if p["how"] == "ball"),
        "hidden": sum(1 for p in pk if p["how"] == "hidden"),
        "gifts": len(kinds.get("gifts", [])),
        "shop": len(kinds.get("shop", [])),
        "wild": len(kinds.get("wild", [])),
        "checks": len(kinds.get("checks", [])),
    }


@functools.lru_cache(maxsize=None)
def zone_order(root):
    """{zone: position}: the earliest sidecar order among the zone's tables,
    and for a place with no table, just after the place ZONE_AFTER names."""
    sc = (model.load_sidecar() or {}).get("areas") or {}
    names = locations.label_names(root)
    out = {}
    for stem, uses in locations.header_uses(root).items():
        o = (sc.get(stem) or {}).get("order")
        if o is None:
            continue
        for _h, lab in uses:
            z = names.get(lab, lab)
            out[z] = min(out.get(z, o), o)
    pending = dict(ZONE_AFTER)
    for _ in range(len(pending) + 1):
        for z, after in list(pending.items()):
            if after in out:
                n = sum(1 for x, a in ZONE_AFTER.items() if a == after and x in out and x != after)
                out[z] = out[after] + 0.01 * (n + 1)
                del pending[z]
    return out


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("--split")
    args = p.parse_args(argv)
    data = build()
    for s in data["splits"]:
        if args.split and s["split"] != args.split:
            continue
        print(f"== {s['split']} (cap {s['cap']})")
        for z in s["zones"]:
            c = z["counts"]
            print(f"  {z['zone']:24} {c['mandatory']} mandatory, {c['optional']} optional "
                  f"({c['rewards']} rewards), {c['gauntlet']} gauntlet, {c['balls']} balls, "
                  f"{c['hidden']} hidden, {c['gifts']} gifts, {c['shop']} shop, "
                  f"{c['wild']} tables, {c['checks']} checks")
    print(f"unplaced: {len(data['unplaced'])}; anywhere checks: {len(data['anywhere'])}; "
          f"sources {data['sources']}")


if __name__ == "__main__":
    main()

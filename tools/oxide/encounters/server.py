"""A local editor for the encounter tables.

    PYTHONPATH=. python3 -m tools.oxide.encounters.server
    then open http://localhost:8765

Binds 127.0.0.1 only. Python stdlib, no dependencies, no build step, no CDN:
this has to still start in two years.

Why a server rather than a browser artifact: a sandboxed page cannot hold or
write repo files, and the File System Access API needs a secure non-sandboxed
context. Running next to the repo removes all of that, and every edit lands
through model.py, so the style-preservation guarantee is the same one the CLI
has.

Every number the page shows comes from analysis.py, lint.py or dex.py through
these endpoints. There is no second implementation of the maths in
JavaScript, so the page and the CLI cannot disagree.
"""
import argparse
import errno
import functools
import http.server
import json
import os
import re
import socketserver
import sys
import urllib.parse
import zlib

from . import analysis as A
from . import canon
from . import dex
from . import lint
from . import locations
from . import model
from . import pokedex
from . import progression

HOST, PORT = "127.0.0.1", 8765
UI = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ui")

from .model import load_encounters, save_encounters  # noqa: E402
from . import planner  # noqa: E402

KIND_LABELS = {"land": "Grass", "surf": "Surf", "old_rod": "Old rod",
               "good_rod": "Good rod", "super_rod": "Super rod"}


def species_universe():
    return dex.species_universe(model.repo_root())


# The twenty-five unknown_533 to unknown_557 files are post-game rooms nothing
# in Oxide uses yet, and Ian asked for them out of the tool until something
# does (2026-09-22). They are parked here, in the browser tool only: the files,
# the CLI, the linter and the availability plan still see them. Parked areas
# leave the area list, the header's game metrics and the dex's cross-links.
def parked(area_name):
    return area_name.startswith("encounters_unknown_")


class State:
    """Loaded per request; the files are the state, so nothing is cached
    across writes."""

    def __init__(self, ref=None):
        self.ref = ref
        self.root = model.repo_root()
        self.sidecar = model.load_sidecar()
        self.entries = (self.sidecar or {}).get("areas") or {}
        self.thresholds = lint.thresholds_from(self.sidecar)
        # {split: position}, so the page can group areas by the game's
        # progression: Roark first, Post last.
        self.split_rank = progression.split_index(self.sidecar)
        self.encounters = load_encounters()          # {area: species}
        self.caught = set(self.encounters.values())
        # The dupes clause works on families: a Starly caught on Route 201
        # also dupes out Staravia and Staraptor wherever they appear. owner_of
        # remembers where, so a duped-out row can say "Starly, Route 201".
        self.owned = dex.expand_caught(self.root, self.caught)
        self.owner_of = {}
        for area, sp in self.encounters.items():
            for member in dex.members_of_line(self.root, dex.line_of(self.root, sp)):
                self.owner_of[member] = (area, sp)

    def areas(self):
        # Every area with a table of any kind: a water-only area (Twinleaf
        # Town, Route 219) is a capture area by its rods and surf even though
        # its grass rate is zero.
        return [a for a in model.load_all(self.ref)
                if (a.land_active or a.kinds_present()) and not parked(a.name)]

    def entry(self, name):
        return self.entries.get(name) or {}

    def payload(self, areas):
        return [(a.name, a.slots, self.entry(a.name) or {"band": a.band},
                 a.data) for a in areas]


# How an area's file name reads as a place: each word capitalised, floors in
# capitals (1F, B2F), and the few words the game spells its own way.
_LABEL_WORDS = {"mt": "Mt.", "pokemon": "Pok\u00e9mon", "and": "and",
                "deadend": "Dead End"}


def _area_label(name):
    words = name.replace("encounters_", "").split("_")
    return " ".join(_LABEL_WORDS.get(w) or
                    (w.upper() if re.fullmatch(r"b?\d+f", w) else w.capitalize())
                    for w in words)


def _species_view(species, st, area=None):
    owner = st.owner_of.get(species)
    here = owner is not None and owner[0] == area
    return {
        "species": species, "label": dex.display_name(species),
        "caught": here,                       # the encounter for this area
        "duped": owner is not None and not here,
        "caught_at": _area_label(owner[0]) if owner else None,
        "via": dex.display_name(owner[1]) if owner and owner[1] != species else None,
    }


def area_row(a, st, findings_by_area):
    e = st.entry(a.name)
    f = findings_by_area.get(a.name, [])
    kinds = a.kinds_present()
    # The row's numbers come from the grass when it is live, else from the
    # area's first table of any kind (a water-only area).
    main = "land" if a.land_active or not kinds else kinds[0]
    main_slots = a.kind_slots(main) if main != "land" else [(s, lv, lv) for s, lv in a.slots]
    main_rates = A.TABLE_KINDS[main][2]
    m = A.table_metrics(main_slots, main_rates)
    c = A.caught_metrics(main_slots, st.owned, main_rates)
    levels = [lv for _, lo, hi in main_slots for lv in (lo, hi)]

    # "Does this area still owe me anything" has to count every table kind,
    # not just the grass, or a route whose only remaining species is in its
    # surf table reads as finished.
    all_species, live_all = set(), set()
    for k in kinds:
        for sp, _, _ in a.kind_slots(k):
            all_species.add(sp)
            if sp not in st.owned:
                live_all.add(sp)

    return {
        "area": a.name,
        "label": _area_label(a.name),
        "encounter": st.encounters.get(a.name),
        "encounter_label": dex.display_name(st.encounters[a.name])
                           if a.name in st.encounters else None,
        "band": e.get("band") or a.band,
        "archetype": e.get("archetype"),
        "intent": e.get("intent", ""),
        # Ian's capture rule: one capture per location name, so the name and
        # the gym split are what a row is worth, not the file it came from.
        "location": locations.location(a.name),
        "split": e.get("split"),
        "split_rank": st.split_rank.get(e.get("split")),
        "order": e.get("order"),
        "no_capture": bool(e.get("no_capture")),
        "species": m["n_species"],
        "hhi": m["hhi"],
        "top": m["top_share"],
        "uplift": m["uplift_on_rarest"],
        "rungs": m["rung_count"],
        "land_rate": a.data.get("land_rate"),
        "level_min": min(levels), "level_max": max(levels),
        "level_med": A.median(levels),
        "kinds": kinds,
        "species_total": len(all_species),
        "live_total": len(live_all),
        "live_species": c["live_species"],
        "target_label": dex.display_name(c["target"]) if c["target"] else None,
        "best_share": c["best_share"],
        "best_level": c["best_level"],
        "holds": sorted({dex.display_name(s) for s in all_species}),
        "errors": sum(1 for x in f if x.severity == "error"),
        "warns": sum(1 for x in f if x.severity == "warn"),
    }


def area_detail(a, st, kind="land"):
    if kind not in A.TABLE_KINDS:
        kind = "land"
    # A water-only area opens on a designed table (one its sidecar entry
    # holds a cast for) if it has one, else its first table, rather than on
    # empty grass.
    if kind == "land" and not a.land_active and a.kinds_present():
        present = a.kinds_present()
        designed = [k for k in present if isinstance(st.entry(a.name).get(k), dict)]
        kind = (designed or present)[0]
    slots = a.kind_slots(kind)
    _, _, rates = A.TABLE_KINDS[kind]
    e = st.entry(a.name)

    if not slots:
        return {"area": a.name, "kind": kind, "empty": True,
                "kinds": a.kinds_present(), "label": _area_label(a.name)}

    odds = A.slot_odds(slots, st.owned, rates)
    m = A.table_metrics(slots, rates)
    c = A.caught_metrics(slots, st.owned, rates)

    def merged_view(table):
        # One line per species with its share on paper and its real odds
        # (the share among what is still uncaught), most common first.
        merged = A.merged(table, rates)
        cond = A.conditional(merged, st.owned)
        return [dict(_species_view(s, st, a.name), share=v, cond=cond.get(s, 0.0))
                for s, v in sorted(merged.items(), key=lambda kv: -kv[1])]

    # Every water table in brief, so the page can show all four under the one
    # being edited: each slot's species, rate, levels and real odds.
    water = []
    for k in a.kinds_present():
        if k == "land":
            continue
        k_slots = a.kind_slots(k)
        _, _, k_rates = A.TABLE_KINDS[k]
        k_odds = A.slot_odds(k_slots, st.owned, k_rates)
        water.append({
            "kind": k, "label": KIND_LABELS[k], "rate": a.kind_rate(k),
            "slots": [dict(_species_view(sp, st, a.name), rate=k_rates[i],
                           level_min=lo, level_max=hi, odds=k_odds[i])
                      for i, (sp, lo, hi) in enumerate(k_slots)],
        })

    # Day and night put their own two species in slots 2 and 3 and leave the
    # rest alone, so each gets its own list; the page shows the one for the
    # time of day being viewed rather than the morning table's at all hours.
    merged_layers = {}
    if kind == "land":
        for layer in ("day", "night"):
            swap_in = a.data.get(layer) or []
            if len(swap_in) == 2:
                table = list(slots)
                for i, sp in enumerate(swap_in):
                    _, lo, hi = table[2 + i]
                    table[2 + i] = (sp, lo, hi)
                merged_layers[layer] = merged_view(table)

    rung_rows = []
    for level, p in A.distinct_rungs(slots, rates):
        cond = A.conditional(p, st.owned)
        rung_rows.append({
            "level": level,
            "throughput": A.throughput(p, st.owned),
            "pool": [dict(_species_view(s, st, a.name), share=v, cond=cond.get(s))
                     for s, v in sorted(p.items(), key=lambda kv: -kv[1])],
        })

    # lint is calibrated on land tables, so it only runs on them
    findings = (lint.lint_table(a.name, a.slots, e or {"band": a.band},
                                st.thresholds, data=a.data)
                if kind == "land" else [])

    return {
        "area": a.name,
        "label": _area_label(a.name),
        "encounter": st.encounters.get(a.name),
        "encounter_label": dex.display_name(st.encounters[a.name])
                           if a.name in st.encounters else None,
        "kind": kind,
        "kinds": a.kinds_present(),
        "kind_labels": KIND_LABELS,
        "band": e.get("band") or a.band,
        "archetype": e.get("archetype"),
        "intent": e.get("intent", ""),
        "location": locations.location(a.name),
        "split": e.get("split"),
        "no_capture": bool(e.get("no_capture")),
        "rate": a.kind_rate(kind),
        "ranged": kind != "land",
        "slots": [dict(_species_view(sp, st, a.name), slot=i, rate=rates[i],
                       level_min=lo, level_max=hi, odds=odds[i])
                  for i, ((sp, lo, hi)) in enumerate(slots)],
        "day": a.data.get("day"), "night": a.data.get("night"),
        "day_labels": [dex.display_name(s) for s in (a.data.get("day") or [])],
        "night_labels": [dex.display_name(s)
                         for s in (a.data.get("night") or [])],
        "merged": merged_view(slots),
        "merged_layers": merged_layers,
        "water": water,
        "rungs": rung_rows,
        "metrics": m,
        "caught_metrics": c,
        "rarest_label": dex.display_name(m["rarest_species"])
                        if m["rarest_species"] else None,
        "best_uplift_label": dex.display_name(m["best_uplift_species"])
                             if m["best_uplift_species"] else None,
        "findings": [f._asdict() for f in findings],
    }


@functools.lru_cache(maxsize=1)
def _captures():
    # Parked areas leave the dex's "where it is met" as well as the area list.
    out = {}
    for species, rows in pokedex.captures().items():
        kept = [r for r in rows if not parked(r["area"])]
        if kept:
            out[species] = kept
    return out


def _transparent_background(data):
    """Make palette entry 0 transparent before serving a sprite.

    The sprites carry no alpha: the colour the game treats as transparent is
    simply the first palette entry, so a browser draws every sprite inside a
    beige box. A tRNS chunk saying entry 0 is clear is the same statement the
    game makes when it draws one, and it is four bytes of header around a byte
    array, so the file is otherwise untouched."""
    if b"tRNS" in data or b"PLTE" not in data:
        return data
    at = data.find(b"PLTE")
    length = int.from_bytes(data[at - 4:at], "big")
    end = at + 4 + length + 4                    # past PLTE's own checksum
    payload = b"tRNS" + bytes([0] + [255] * (length // 3 - 1))
    chunk = (len(payload) - 4).to_bytes(4, "big") + payload \
        + zlib.crc32(payload).to_bytes(4, "big")
    return data[:end] + chunk + data[end:]


def dex_list():
    """Every species in the tree, as one row each: what the list view needs and
    nothing it does not, because there are 652 of them."""
    root = model.repo_root()
    caught = _captures()
    rows = []
    for species in pokedex.species_list(root):
        rec = pokedex.load(root, species)
        if rec is None:
            continue
        d = pokedex.delta(root, species)
        rows.append({
            "species": species,
            "folder": rec["folder"],
            "name": rec["name"],
            "types": rec["types"],
            "bst": rec["bst"],
            "stats": rec["stats"],
            "new": bool(d and d.get("new")),
            "changed": bool(d and not d.get("new")),
            "bst_delta": (d or {}).get("bst"),
            # Against the species' real self, which is the only comparison the
            # ported ones have: vanilla Platinum has never heard of them.
            "canon_delta": (canon.delta(species, rec) or {}).get("bst"),
            "appearances": len(caught.get(species) or []),
        })
    return {"rows": rows, "count": len(rows)}


def dex_detail(species):
    """One species, with what changed from vanilla, where it is met, and what
    every type does to it."""
    root = model.repo_root()
    species = species.upper()
    if not species.startswith("SPECIES_"):
        species = "SPECIES_" + species
    rec = pokedex.load(root, species)
    if rec is None:
        return {"error": "no such species"}
    chart = pokedex.type_chart(root)
    matchups = {}
    for attacking in sorted({a for a, _ in chart}):
        mult = pokedex.effectiveness(chart, attacking, rec["types"])
        if mult != 1.0:
            matchups[attacking] = mult
    out = dict(rec)
    out["delta"] = pokedex.delta(root, species)
    out["vanilla"] = pokedex.load(root, species, "main")
    out["canon"] = canon.delta(species, rec)
    out["canon_name"] = canon.showdown_name(species)
    out["sprites"] = pokedex.sprites(root, species)
    out["captures"] = _captures().get(species) or []
    out["matchups"] = matchups
    moves = pokedex.moves(root)
    out["learnset"] = []
    for lv, mv in rec["learnset"]:
        m = moves.get(mv) or {}
        out["learnset"].append({
            "level": lv, "move": mv,
            "label": m.get("name") or dex.display_name(mv),
            "type": m.get("type"), "class": m.get("class"),
            "power": m.get("power"), "accuracy": m.get("accuracy"),
            "pp": m.get("pp"),
        })
    # The other three ways a species learns a move, as names and types only:
    # the page lists them compactly and each opens its move.
    by_machine = pokedex.machines(root)
    brief = lambda mv, **kw: dict(kw, move=mv, type=(moves.get(mv) or {}).get("type"),
                                  label=(moves.get(mv) or {}).get("name")
                                  or dex.display_name(mv))
    out["machine_moves"] = [brief(by_machine[t], machine=t) for t in rec["by_tm"]
                            if t in by_machine]
    out["tutor_moves"] = [brief(mv) for mv in rec["by_tutor"]]
    out["egg_moves"] = [brief(mv) for mv in rec["egg_moves"]]
    # A mega is entered twice, once under the day method and once under the
    # night one, which is how the tree holds an alt-evolution. That is one
    # forme, not two evolutions.
    seen, evolutions = set(), []
    for evo in rec["evolutions"]:
        if evo["into"] in seen:
            continue
        seen.add(evo["into"])
        into = pokedex.load(root, evo["into"]) if evo["into"] else None
        evo = dict(evo, label=into["name"] if into else None,
                   folder=into["folder"] if into else None)
        evolutions.append(evo)
    out["evolutions"] = [e for e in evolutions if not e["form"]]
    out["formes"] = [e for e in evolutions if e["form"]]
    # The captures index is per species, not per line: after the evolution pass
    # a table that used to hold Litten holds Torracat, so the page has to be able
    # to say where the rest of the line is met.
    caps = _captures()
    line_id = None
    try:
        line_id = dex.line_of(root, species)
    except Exception:
        line_id = None
    members = dex.members_of_line(root, line_id) if line_id else []
    out["line"] = []
    for member in members:
        rec_m = pokedex.load(root, member)
        if rec_m is None:
            continue
        out["line"].append({
            "species": member,
            "label": rec_m["name"],
            "folder": rec_m["folder"],
            "appearances": len(caps.get(member) or []),
            "evolutions": rec_m["evolutions"],
            "bst": rec_m["bst"],
            "mega_of": rec_m["mega_of"],
        })
    # A mega shares its base's line but is not a stage of it, so it belongs with
    # the formes rather than in the chain.
    out["line"] = [m for m in out["line"] if not m["mega_of"]]
    out["line"] = _in_stage_order(out["line"])
    return out


def _in_stage_order(line):
    """The line from its first stage out, each member marked with its stage.

    Members come from the line index sorted by name, which read Incineroar,
    Litten, Torracat. Walk the evolutions instead, from the member nothing
    evolves into; a branch (Eevee's eight) is siblings at one stage, in the
    order the game lists them."""
    by_species = {m["species"]: m for m in line}
    into = {m["species"]: [e["into"] for e in m["evolutions"]
                           if not e["form"] and e["into"] in by_species]
            for m in line}
    evolved = {t for targets in into.values() for t in targets}
    frontier = [m["species"] for m in line if m["species"] not in evolved]
    stage, seen, out = 0, set(), []
    while frontier:
        nxt = []
        for sp in frontier:
            if sp in seen:
                continue
            seen.add(sp)
            out.append(dict(by_species[sp], stage=stage))
            nxt.extend(into[sp])
        frontier, stage = nxt, stage + 1
    # Anything the walk cannot reach still shows, after the rest.
    out.extend(dict(m, stage=stage) for m in line if m["species"] not in seen)
    return out


def _move_name(move):
    move = move.upper()
    return move if move.startswith("MOVE_") else "MOVE_" + move


def move_list():
    """Every move in the tree, one row each, with what changed from vanilla and
    how many species learn it."""
    root = model.repo_root()
    moves = pokedex.moves(root)
    vanilla = pokedex.vanilla_moves(root)
    learnt = pokedex.learners(root)
    rows = []
    for move, rec in sorted(moves.items(), key=lambda kv: kv[1]["id"] or 0):
        if move == "MOVE_NONE":
            continue
        d = pokedex.move_delta(rec, vanilla.get(move))
        rows.append({
            "move": move, "id": rec["id"], "name": rec["name"],
            "type": rec["type"], "class": rec["class"], "power": rec["power"],
            "accuracy": rec["accuracy"], "pp": rec["pp"],
            "priority": rec["priority"], "effect": rec["effect"],
            "stub": rec["stub"],
            "new": bool(d and d.get("new")),
            "changed": bool(d and not d.get("new")),
            "learners": len({r["species"] for r in learnt.get(move) or []}),
        })
    return {"rows": rows, "count": len(rows)}


def move_detail(move):
    """One move, with what changed from vanilla and every species that learns
    it: how, at what level, and the earliest split a player can meet it wild,
    which is the question an author asks of a move."""
    root = model.repo_root()
    move = _move_name(move)
    rec = pokedex.moves(root).get(move)
    if rec is None:
        return {"error": "no such move"}
    was = pokedex.vanilla_moves(root).get(move)
    split_rank = progression.split_index(model.load_sidecar())
    caps = _captures()
    out = dict(rec)
    out["delta"] = pokedex.move_delta(rec, was)
    out["vanilla"] = was
    out["machine"] = next((m for m, mv in pokedex.machines(root).items()
                           if mv == move), None)
    learners = []
    for row in pokedex.learners(root).get(move) or []:
        sp = pokedex.load(root, row["species"])
        met = caps.get(row["species"]) or []
        splits = sorted({c["split"] for c in met if c.get("split")},
                        key=lambda s: split_rank.get(s, 99))
        learners.append(dict(row, label=sp["name"], folder=sp["folder"],
                             types=sp["types"], appearances=len(met),
                             first_split=splits[0] if splits else None))
    # Grouped by how, then by level for level-up, then by how early a player
    # can have the species at all, so the top of each group is the answer to
    # "who is the first thing that can use this".
    how = {h: i for i, h in enumerate(pokedex.LEARN_KINDS)}
    learners.sort(key=lambda r: (how[r["how"]], r["level"] or 0,
                                 split_rank.get(r["first_split"], 99),
                                 r["label"]))
    out["learners"] = learners
    return out


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=UI, **kw)

    def log_message(self, fmt, *args):
        pass

    def end_headers(self):
        # Everything here is read from disk per request, so a cached copy is
        # only ever a way to be shown yesterday's tool. That is not theoretical:
        # a stale page is indistinguishable from a view that was never built.
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def _send(self, obj, code=200):
        body = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _sprite(self, folder, kind):
        """A species' sprite straight out of res/. The PNGs are indexed colour
        with their own palette, so a browser draws them as they are; a front or
        back sheet is two frames side by side, which the page crops."""
        kind = kind.replace(".png", "")
        if kind not in pokedex.SPRITES or "/" in folder or ".." in folder:
            return self._send({"error": "no such sprite"}, 404)
        path = os.path.join(model.repo_root(), "res", "pokemon", folder,
                            kind + ".png")
        try:
            with open(path, "rb") as f:
                body = _transparent_background(f.read())
        except OSError:
            return self._send({"error": "no such sprite"}, 404)
        self.send_response(200)
        self.send_header("Content-Type", "image/png")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _body(self):
        n = int(self.headers.get("Content-Length") or 0)
        return json.loads(self.rfile.read(n) or b"{}")

    def do_GET(self):
        url = urllib.parse.urlparse(self.path)
        q = urllib.parse.parse_qs(url.query)
        ref = (q.get("ref") or [None])[0] or None
        kind = (q.get("kind") or ["land"])[0]
        parts = [p for p in url.path.split("/") if p]

        if not parts or parts[0] != "api":
            return super().do_GET()
        # /api alone, or /api/area, /api/move or /api/sprite without the name
        # they need, is an unknown endpoint like any other, not a crash.
        if len(parts) < 2 or (parts[1] in ("area", "move", "sprite") and len(parts) < 3):
            return self._send({"error": "unknown endpoint"}, 404)
        try:
            st = State(ref)
            if parts[1] == "areas":
                areas = st.areas()
                findings = lint.lint_all(st.payload(areas), st.sidecar)
                by_area = {}
                for f in findings:
                    by_area.setdefault(f.target, []).append(f)
                g = A.game_metrics(
                    [a.slots for a in areas],
                    [st.entry(a.name).get("band") or a.band for a in areas])
                return self._send({
                    "ref": ref or "working tree",
                    "root": model.repo_root(),
                    "rows": [area_row(a, st, by_area) for a in areas],
                    "game": g,
                    "game_findings": [f._asdict() for f in findings
                                      if f.scope == "game"],
                    "thresholds": st.thresholds,
                    "kind_labels": KIND_LABELS,
                })
            if parts[1] == "area":
                return self._send(
                    area_detail(model.load_area(parts[2], ref), st, kind))
            if parts[1] == "species":
                rows = [{"value": s, "label": dex.display_name(s)}
                        for s in species_universe()]
                rows.sort(key=lambda r: r["label"])
                return self._send({"species": rows})
            if parts[1] == "plan":
                area = (q.get("area") or [None])[0]
                species = (q.get("species") or [None])[0]
                if not area or not species:
                    return self._send({"error": "plan needs area and species"},
                                      400)
                areas, line_of, members_of = planner.plan_inputs()
                if not any(a["name"] == area for a in areas):
                    return self._send({"error": "no such area"}, 404)
                out = planner.plan(area, species, kind, areas, st.owned,
                                   line_of, members_of)
                out["lines"] = planner.describe(out, dex.display_name,
                                                _area_label, KIND_LABELS)
                return self._send(out)

            if parts[1] == "dex":
                return self._send(dex_list() if len(parts) < 3
                                  else dex_detail(parts[2]))
            if parts[1] == "moves":
                return self._send(move_list())
            if parts[1] == "move":
                out = move_detail(parts[2])
                return self._send(out, 404 if "error" in out else 200)
            if parts[1] == "sprite":
                return self._sprite(parts[2], parts[3] if len(parts) > 3 else "icon")
            if parts[1] == "caught":
                return self._send({
                    "encounters": st.encounters,
                    "caught": sorted(st.caught),
                    "owned": sorted(st.owned),
                })
        except FileNotFoundError:
            return self._send({"error": "no such area"}, 404)
        except Exception as exc:
            return self._send({"error": f"{type(exc).__name__}: {exc}"}, 500)
        return self._send({"error": "unknown endpoint"}, 404)

    def do_POST(self):
        url = urllib.parse.urlparse(self.path)
        parts = [p for p in url.path.split("/") if p]
        try:
            body = self._body()

            # Caught state is global: ticking a species here changes the odds
            # on every other table too, which is the point of the dupes
            # clause. Stored once, server side, rather than per page.
            if len(parts) >= 2 and parts[0] == "api" and parts[1] == "caught":
                enc = load_encounters()
                if body.get("clear") and "area" not in body:
                    enc = {}
                else:
                    area = body.get("area")
                    if not area:
                        return self._send({"error": "which area?"}, 400)
                    model.load_area(area)          # 404s if it does not exist
                    if body.get("clear") or body.get("caught") is False:
                        if body.get("species") in (None, enc.get(area)):
                            enc.pop(area, None)
                    else:
                        sp = body.get("species")
                        if sp not in set(species_universe()):
                            return self._send(
                                {"error": f"no such species: {sp}"}, 400)
                        enc[area] = sp             # one encounter per area
                save_encounters(enc)
                st = State(None)
                return self._send({"encounters": st.encounters,
                                   "caught": sorted(st.caught),
                                   "owned": sorted(st.owned)})

            if len(parts) >= 3 and parts[0] == "api" and parts[1] == "area":
                name = parts[2]
                what = parts[3] if len(parts) > 3 else "slot"
                kind = body.get("kind", "land")
                a = model.load_area(name)
                before = a.text

                # The page's combobox is a suggestion, not a constraint, so a
                # typo would otherwise write a species that does not exist and
                # break the next build. Refuse it here.
                sp = body.get("species")
                if sp is not None and sp not in set(species_universe()):
                    return self._send({"error": f"no such species: {sp}"}, 400)
                for key in ("level", "level_min", "level_max"):
                    v = body.get(key)
                    if v is not None and not 1 <= int(v) <= 100:
                        return self._send(
                            {"error": f"{key} {v} out of range 1-100"}, 400)

                if what == "slot":
                    if kind == "land":
                        a.set_slot(int(body["slot"]), species=sp,
                                   level=body.get("level"))
                    else:
                        a.set_water_slot(kind, int(body["slot"]), species=sp,
                                         level_min=body.get("level_min"),
                                         level_max=body.get("level_max"))
                elif what == "time":
                    a.set_time_slot(body["layer"], int(body["index"]), sp)
                elif what == "rate":
                    a.set_land_rate(int(body["land_rate"]))
                else:
                    return self._send({"error": f"unknown write {what}"}, 404)

                changed = a.text != before
                if changed:
                    a.save()
                st = State(None)
                out = area_detail(model.load_area(name), st, kind)
                out["changed"] = changed
                return self._send(out)
        except (KeyError, ValueError, IndexError) as exc:
            return self._send({"error": f"bad request: {exc}"}, 400)
        except RuntimeError as exc:
            return self._send({"error": str(exc)}, 403)
        except Exception as exc:
            return self._send({"error": f"{type(exc).__name__}: {exc}"}, 500)
        return self._send({"error": "unknown endpoint"}, 404)


class Server(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    # There is a copy of this tool in every checkout and worktree, and they all
    # want the same port. Running two at once is the point of the flag: one on
    # the branch being written, one on what is merged.
    ap.add_argument("--port", type=int, default=PORT,
                    help=f"default {PORT}; use another to run a second checkout")
    a = ap.parse_args(argv)

    os.chdir(model.repo_root())
    try:
        httpd = Server((HOST, a.port), Handler)
    except OSError as exc:
        if exc.errno != errno.EADDRINUSE:
            raise
        print(f"port {a.port} is already taken, most likely by another copy of "
              f"this tool.\nEither stop that one, or start this one on another "
              f"port:\n    PYTHONPATH=. python3 -m tools.oxide.encounters.server "
              f"--port {a.port + 1}")
        return 1
    with httpd:
        print(f"encounter tool on http://{HOST}:{a.port}")
        print(f"editing {model.ENC_DIR} in {model.repo_root()}")
        print("ctrl-c to stop")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nstopped")
    return 0


if __name__ == "__main__":
    sys.exit(main())

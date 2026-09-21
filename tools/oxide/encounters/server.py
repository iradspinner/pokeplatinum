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
import http.server
import json
import os
import socketserver
import urllib.parse

from . import analysis as A
from . import dex
from . import lint
from . import locations
from . import model

HOST, PORT = "127.0.0.1", 8765
UI = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ui")

from .model import load_encounters, save_encounters  # noqa: E402
from . import planner  # noqa: E402

KIND_LABELS = {"land": "Grass", "surf": "Surf", "old_rod": "Old rod",
               "good_rod": "Good rod", "super_rod": "Super rod"}


def species_universe():
    return dex.species_universe(model.repo_root())


class State:
    """Loaded per request; the files are the state, so nothing is cached
    across writes."""

    def __init__(self, ref=None):
        self.ref = ref
        self.root = model.repo_root()
        self.sidecar = model.load_sidecar()
        self.entries = (self.sidecar or {}).get("areas") or {}
        self.thresholds = lint.thresholds_from(self.sidecar)
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
        return [a for a in model.load_all(self.ref) if a.land_active]

    def entry(self, name):
        return self.entries.get(name) or {}

    def payload(self, areas):
        return [(a.name, a.slots, self.entry(a.name) or {"band": a.band},
                 a.data) for a in areas]


def _area_label(name):
    return name.replace("encounters_", "").replace("_", " ")


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
    m = A.table_metrics(a.slots)
    c = A.caught_metrics(a.slots, st.owned)
    e = st.entry(a.name)
    f = findings_by_area.get(a.name, [])
    levels = a.levels
    kinds = a.kinds_present()

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
    slots = a.kind_slots(kind)
    _, _, rates = A.TABLE_KINDS[kind]
    e = st.entry(a.name)

    if not slots:
        return {"area": a.name, "kind": kind, "empty": True,
                "kinds": a.kinds_present(), "label": _area_label(a.name)}

    odds = A.slot_odds(slots, st.owned, rates)
    m = A.table_metrics(slots, rates)
    c = A.caught_metrics(slots, st.owned, rates)
    merged = A.merged(slots, rates)
    cond_merged = A.conditional(merged, st.owned)

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
        "merged": [dict(_species_view(s, st, a.name), share=v,
                        cond=cond_merged.get(s, 0.0))
                   for s, v in sorted(merged.items(), key=lambda kv: -kv[1])],
        "rungs": rung_rows,
        "metrics": m,
        "caught_metrics": c,
        "rarest_label": dex.display_name(m["rarest_species"])
                        if m["rarest_species"] else None,
        "best_uplift_label": dex.display_name(m["best_uplift_species"])
                             if m["best_uplift_species"] else None,
        "findings": [f._asdict() for f in findings],
    }


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=UI, **kw)

    def log_message(self, fmt, *args):
        pass

    def _send(self, obj, code=200):
        body = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
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


def main():
    os.chdir(model.repo_root())
    with Server((HOST, PORT), Handler) as httpd:
        print(f"encounter tool on http://{HOST}:{PORT}")
        print(f"editing {model.ENC_DIR} in {model.repo_root()}")
        print("ctrl-c to stop")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nstopped")


if __name__ == "__main__":
    main()

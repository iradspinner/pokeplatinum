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

Every number the UI shows comes from analysis.py or lint.py through these
endpoints. There is no second implementation of the maths in JavaScript, so
the page and the CLI cannot disagree.
"""
import http.server
import json
import os
import socketserver
import urllib.parse

from . import analysis as A
from . import lint
from . import model

HOST, PORT = "127.0.0.1", 8765
UI = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ui")

# Per-playthrough state, not design intent, so it is gitignored rather than
# living in the sidecar. What Ian has caught changes which tables are worth
# walking; it is not a statement about how the tables should be built.
CAUGHT_FILE = os.path.join("docs", "oxide", "encounters", "caught.json")

# SPECIES_MR_MIME is not "Mr Mime" and SPECIES_NIDORAN_F is not "Nidoran F".
# Only these six plus farfetchd need help; everything else title-cases.
SPECIAL_NAMES = {
    "SPECIES_HO_OH": "Ho-Oh",
    "SPECIES_MIME_JR": "Mime Jr.",
    "SPECIES_MR_MIME": "Mr. Mime",
    "SPECIES_NIDORAN_F": "Nidoran♀",
    "SPECIES_NIDORAN_M": "Nidoran♂",
    "SPECIES_PORYGON_Z": "Porygon-Z",
    "SPECIES_FARFETCHD": "Farfetch'd",
    "SPECIES_PORYGON2": "Porygon2",
}


def display_name(species):
    """SPECIES_GLALIE -> Glalie. The page never shows a raw constant."""
    if species in SPECIAL_NAMES:
        return SPECIAL_NAMES[species]
    stem = species.replace("SPECIES_", "")
    return " ".join(w.capitalize() for w in stem.split("_"))


def load_caught():
    path = os.path.join(model.repo_root(), CAUGHT_FILE)
    try:
        with open(path, encoding="utf-8") as f:
            return set(json.load(f).get("caught") or [])
    except (FileNotFoundError, ValueError):
        return set()


def save_caught(caught):
    path = os.path.join(model.repo_root(), CAUGHT_FILE)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump({"caught": sorted(caught)}, f, indent=2)
        f.write("\n")


def species_universe():
    """SPECIES_* constants, derived from res/pokemon/. include/generated is a
    build artefact and is not present in a clean tree, and the directory names
    round-trip exactly: all 329 species used across the encounter files are
    covered by the 502 derived here."""
    root = os.path.join(model.repo_root(), "res", "pokemon")
    return sorted("SPECIES_" + d.upper() for d in os.listdir(root)
                  if not d.startswith(".")          # res/pokemon/.shared
                  and os.path.isdir(os.path.join(root, d)))


class State:
    """Loaded once per request batch; the files are the state, so nothing is
    cached across writes."""

    def __init__(self, ref=None):
        self.ref = ref
        self.sidecar = model.load_sidecar()
        self.entries = (self.sidecar or {}).get("areas") or {}
        self.thresholds = lint.thresholds_from(self.sidecar)
        self.caught = load_caught()

    def areas(self):
        return [a for a in model.load_all(self.ref) if a.land_active]

    def entry(self, name):
        return self.entries.get(name) or {}

    def payload(self, areas):
        return [(a.name, a.slots,
                 self.entry(a.name) or {"band": a.band}, a.data)
                for a in areas]


def area_row(a, st, findings_by_area):
    m = A.table_metrics(a.slots)
    c = A.caught_metrics(a.slots, st.caught)
    e = st.entry(a.name)
    f = findings_by_area.get(a.name, [])
    levels = a.levels
    return {
        "area": a.name,
        "band": e.get("band") or a.band,
        "archetype": e.get("archetype"),
        "intent": e.get("intent", ""),
        "species": m["n_species"],
        "hhi": m["hhi"],
        "top": m["top_share"],
        "uplift": m["uplift_on_rarest"],
        "best_uplift": m["best_uplift"],
        "rungs": m["rung_count"],
        "land_rate": a.data.get("land_rate"),
        # play order, approximated by encounter level until a real
        # progression order exists in the sidecar
        "level_min": min(levels),
        "level_max": max(levels),
        "level_med": A.median(levels),
        # what is still worth catching here, given what is already caught
        "live_species": c["live_species"],
        "target": c["target"],
        "target_label": display_name(c["target"]) if c["target"] else None,
        "best_share": c["best_share"],
        "best_level": c["best_level"],
        # powers the "/gible" filter: "which routes hold Gible?" is the
        # question the dupe-out cascade is asked in
        "holds": sorted({display_name(s) for s, _ in a.slots}),
        "errors": sum(1 for x in f if x.severity == "error"),
        "warns": sum(1 for x in f if x.severity == "warn"),
    }


def area_detail(a, st):
    m = A.table_metrics(a.slots)
    e = st.entry(a.name)
    findings = lint.lint_table(a.name, a.slots, e or {"band": a.band},
                               st.thresholds, data=a.data)
    rungs = []
    for level, pool in A.distinct_rungs(a.slots):
        cond = A.conditional(pool, st.caught)
        rungs.append({
            "level": level,
            "throughput": A.throughput(pool, st.caught),
            "pool": [{"species": s, "label": display_name(s), "share": v,
                      "caught": s in st.caught, "cond": cond.get(s)}
                     for s, v in sorted(pool.items(), key=lambda kv: -kv[1])],
        })
    merged = A.merged(a.slots)
    return {
        "area": a.name,
        "band": e.get("band") or a.band,
        "archetype": e.get("archetype"),
        "intent": e.get("intent", ""),
        "land_rate": a.data.get("land_rate"),
        "slots": [{"slot": i, "rate": A.LAND_RATES[i], "species": s,
                   "label": display_name(s), "level": lv,
                   "caught": s in st.caught}
                  for i, (s, lv) in enumerate(a.slots)],
        "day": a.data.get("day"), "night": a.data.get("night"),
        "day_labels": [display_name(s) for s in (a.data.get("day") or [])],
        "night_labels": [display_name(s) for s in (a.data.get("night") or [])],
        "merged": [{"species": s, "label": display_name(s), "share": v,
                    "caught": s in st.caught}
                   for s, v in sorted(merged.items(), key=lambda kv: -kv[1])],
        "rungs": rungs,
        "metrics": m,
        "caught_metrics": A.caught_metrics(a.slots, st.caught),
        "rarest_label": display_name(m["rarest_species"])
                        if m["rarest_species"] else None,
        "best_uplift_label": display_name(m["best_uplift_species"])
                             if m["best_uplift_species"] else None,
        "findings": [f._asdict() for f in findings],
    }


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=UI, **kw)

    def log_message(self, fmt, *args):
        pass  # the page polls; the default logger is pure noise

    # -- helpers ---------------------------------------------------------

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

    # -- routes ----------------------------------------------------------

    def do_GET(self):
        url = urllib.parse.urlparse(self.path)
        q = urllib.parse.parse_qs(url.query)
        ref = (q.get("ref") or [None])[0] or None
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
                game = [f._asdict() for f in findings if f.scope == "game"]
                g = A.game_metrics([a.slots for a in areas],
                                   [st.entry(a.name).get("band") or a.band
                                    for a in areas])
                return self._send({
                    "ref": ref or "working tree",
                    "rows": [area_row(a, st, by_area) for a in areas],
                    "game": g,
                    "game_findings": game,
                    "thresholds": st.thresholds,
                })

            if parts[1] == "area":
                a = model.load_area(parts[2], ref)
                return self._send(area_detail(a, st))

            if parts[1] == "species":
                # the whole pokedex, sorted by display name, for the combobox
                rows = [{"value": s, "label": display_name(s)}
                        for s in species_universe()]
                rows.sort(key=lambda r: r["label"])
                return self._send({"species": rows})

            if parts[1] == "caught":
                return self._send({"caught": sorted(st.caught)})

        except FileNotFoundError:
            return self._send({"error": "no such area"}, 404)
        except Exception as exc:  # surface it in the page, not just the log
            return self._send({"error": f"{type(exc).__name__}: {exc}"}, 500)
        return self._send({"error": "unknown endpoint"}, 404)

    def do_POST(self):
        url = urllib.parse.urlparse(self.path)
        parts = [p for p in url.path.split("/") if p]
        try:
            body = self._body()

            # Caught state is global: ticking a species here changes the odds
            # on every other table too, which is the whole point of the dupes
            # clause. It is stored once, server side, rather than per page.
            if len(parts) >= 2 and parts[0] == "api" and parts[1] == "caught":
                caught = load_caught()
                if "clear" in body:
                    caught = set()
                else:
                    sp = body.get("species")
                    if sp not in set(species_universe()):
                        return self._send({"error": f"no such species: {sp}"},
                                          400)
                    caught.add(sp) if body.get("caught") else caught.discard(sp)
                save_caught(caught)
                return self._send({"caught": sorted(caught)})

            if len(parts) >= 3 and parts[0] == "api" and parts[1] == "area":
                name = parts[2]
                what = parts[3] if len(parts) > 3 else "slot"
                a = model.load_area(name)
                before = a.text

                # The datalist in the page is a suggestion, not a constraint,
                # so a typo would otherwise write a species that does not
                # exist and break the next build. Refuse it here instead.
                sp = body.get("species")
                if sp is not None and sp not in set(species_universe()):
                    return self._send(
                        {"error": f"no such species: {sp}"}, 400)

                if what == "slot":
                    lvl = body.get("level")
                    if lvl is not None and not 1 <= int(lvl) <= 100:
                        return self._send(
                            {"error": f"level {lvl} out of range 1-100"}, 400)
                    a.set_slot(int(body["slot"]), species=sp, level=lvl)
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
                out = area_detail(model.load_area(name), st)
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

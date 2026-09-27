"""Incremental rescores: recompute only the scores whose inputs changed.

    PYTHONPATH=. python3 -m tools.oxide.balance.rescore             # recompute what changed
    PYTHONPATH=. python3 -m tools.oxide.balance.rescore --verify    # recompute the unverified
    PYTHONPATH=. python3 -m tools.oxide.balance.rescore --status    # count, compute nothing
    PYTHONPATH=. python3 -m tools.oxide.balance.rescore --seed      # adopt stored scores

Ian's ruling of 2026-09-27: a full rescore costs about 45 minutes a run on
this CPU, and two runs must agree, even when a change touches a few fights.
So every stored score (a story fight in pressure.json, Hesperid's in
calibrate.json, a reference seat in pressure_refs/, a cell of shape.json's
grid, and B6's ordinary trainers and per-fight levers in b6.json) carries a
fingerprint of everything that decides it, and a verified mark.

The fingerprint is a hash of: the exact job file the calculator runs (the
player's side, the boss Pokemon, their moves, weather); what the scorer
takes besides (the parties as the trainer data holds them, Trick Room, the
cap, a reference's move categories); the slices of the calculator's data
the job reads (the title, the type chart, and the species and move records
it names); the accuracies of its moves; the damage calculator's files the
headless runner loads (engine_files) and Node's version; and the scorer's
code with docstrings left out, so a change to the scoring rules rescores
everything and a change to its wording does not. The game's own C, battle
scripts and AI are not read by any score, so merging them stales nothing.
Every score is worked out from its own fight alone, and every roll-up is
made at report time from the stored scores, so nothing else can move one.

A rescore recomputes each score whose fingerprint differs from its inputs
now, or that has none, and stores it unverified. --verify recomputes each
unverified score and marks it verified when the two agree exactly, timing
aside, which keeps the rule that two runs agree while this CPU can return
wrong answers. test_b3 checks that every fingerprint matches its inputs
and that nothing is left unverified. --seed adopts scores computed before
fingerprints existed: it stamps each with its inputs' fingerprint,
unverified, so the next --verify recomputes all of them once. --restamp
moves each score that is current under the previous definition to this
one, keeping its verified mark; it has been used twice, when the engine
part narrowed from the whole vendored folder to engine_files, and when
species records' hidden-ability slot left the hash (_species_record).

Every calculation runs in one Node process at a time.
"""
import argparse
import ast
import collections
import functools
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
import time

from ..encounters import calc_export
from . import b6, calibrate, data, metrics, pool, pressure, refpressure, shape

HERE = os.path.dirname(os.path.abspath(__file__))
CALC_DIR = os.path.normpath(os.path.join(HERE, "..", "encounters", "calc"))
TIMING = {"node_seconds", "wall_seconds", "seconds"}
MARKS = {"fingerprint", "verified"}
KINDS = ("pressure", "calibrate", "ref", "shape", "b6", "b6lever")


# ---- what decides a score ----------------------------------------------------

def _top_names(node):
    """The names a top-level statement defines."""
    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
        return {node.name}
    if isinstance(node, ast.Assign):
        return {t.id for t in node.targets if isinstance(t, ast.Name)}
    return set()


def _code_hash(path, skip=frozenset()):
    """The module's code as Python parses it, docstrings left out, and any
    top-level function or constant named in `skip` too."""
    with open(path, encoding="utf-8") as f:
        tree = ast.parse(f.read())
    tree.body = [n for n in tree.body if not (_top_names(n) and _top_names(n) <= skip)]
    for node in ast.walk(tree):
        body = getattr(node, "body", None)
        if (isinstance(node, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
                and body and isinstance(body[0], ast.Expr)
                and isinstance(body[0].value, ast.Constant) and isinstance(body[0].value.value, str)):
            node.body = body[1:] or [ast.Pass()]
    return hashlib.sha256(ast.dump(tree).encode()).hexdigest()


# What b6.py holds besides its scoring: the report, the fight scale, the
# draft scorer, the new-content and dead-weight counts, and their constants.
# None of it decides a stored score, so editing it stales nothing. Kept
# here, not in b6.py, so that listing it never changed b6.py's own hash.
B6_REPORT_ONLY = frozenset({
    "BANDS", "FAR", "CARRIES", "MIN_FIGHTS", "HYPER", "TOO_HARD", "DEAD_MOVES",
    "DEAD_ABILITIES", "DRAFT_IV", "story_scores", "scale_line", "on_scale", "band",
    "_main_list", "new_content", "obtainable", "dead_weight", "_fmt", "lever_table",
    "species_table", "hyper_offense", "fully_evolved", "_changes", "report",
    "_constants_by_name", "_fill", "_draft_party", "score_draft", "main"})


_SCRIPT = re.compile(r'<script[^>]*src="\./(calc/[^"?]+)')


def engine_files():
    """The files the headless runner reads, as calc_headless.js finds them:
    itself, the page, every ./calc/ script the page loads (a commented-out
    line skipped), and initialize.js, whose helpers it lifts. Nothing else
    in the vendored folder (its notes, other data) can move a score."""
    with open(os.path.join(CALC_DIR, "index.html"), encoding="utf-8") as f:
        scripts = [m.group(1) for line in f if not line.strip().startswith("<!--")
                   for m in [_SCRIPT.search(line)] if m]
    paths = [os.path.join(HERE, "calc_headless.js"), os.path.join(CALC_DIR, "index.html"),
             os.path.join(CALC_DIR, "js", "initialize.js")]
    paths += [os.path.join(CALC_DIR, s) for s in dict.fromkeys(scripts)]
    return paths


def _hash_files(paths):
    h = hashlib.sha256()
    for p in paths:
        h.update(os.path.relpath(p, HERE).encode())
        with open(p, "rb") as f:
            h.update(f.read())
    node = subprocess.run(["node", "--version"], capture_output=True, text=True, check=True).stdout
    h.update(node.strip().encode())
    return h.hexdigest()


@functools.lru_cache(maxsize=None)
def engine_hash():
    """The engine the runner loads, and Node's version."""
    return _hash_files(engine_files())


@functools.lru_cache(maxsize=None)
def scorer_hash(kind, previous=False):
    """The code a kind of score is worked out by: pressure.py for all, and
    the module that reduces or builds it for the others; for B6, b6.py
    less its report (B6_REPORT_ONLY), or all of it for `previous`."""
    mods = {"pressure": ["pressure.py"], "calibrate": ["pressure.py"],
            "ref": ["pressure.py", "refpressure.py"], "shape": ["pressure.py", "shape.py"],
            "b6": ["pressure.py", "b6.py"], "b6lever": ["pressure.py", "b6.py"]}[kind]
    return hashlib.sha256("".join(
        _code_hash(os.path.join(HERE, m),
                   B6_REPORT_ONLY if m == "b6.py" and not previous else frozenset())
        for m in mods).encode()).hexdigest()


def _names(o, species, moves):
    """Every species and move named by a Pokemon record anywhere in o: the
    job's, and those in what a scorer takes besides (a party's status
    moves, a lever's new move, a side at another cap)."""
    if isinstance(o, dict):
        if isinstance(o.get("species"), str) and isinstance(o.get("moves"), list):
            species.add(o["species"])
            moves.update(m for m in o["moves"] if isinstance(m, str))
        for v in o.values():
            _names(v, species, moves)
    elif isinstance(o, (list, tuple)):
        for v in o:
            _names(v, species, moves)


def _species_record(rec):
    """A species' calculator record as the fingerprint reads it: without
    its hidden ability ("H"). No score can reach that slot: every scored
    Pokemon is given an ability (the side its first, a trainer's set its
    own), and the engine falls back to slot "0" when one is missing. The
    natives' hidden abilities (2026-09-27) added "H" to 451 records and so
    changed every score's hash while changing no score."""
    if not isinstance(rec, dict) or not isinstance(rec.get("abilities"), dict):
        return rec
    return dict(rec, abilities={k: v for k, v in rec["abilities"].items() if k != "H"})


def fingerprint(kind, jobs, ctx, blob, previous=False):
    """The hash of everything that decides one score (the module's doc).
    `previous` hashes by the definition this one replaced, for --restamp:
    B6's scorer hashed as the whole of b6.py (scorer_hash)."""
    species, moves = set(), set()
    _names(jobs["pokemon"], species, moves)
    _names(ctx, species, moves)
    for _a, _d, ms, _w in jobs["pairs"]:
        moves.update(ms)
    acc = pressure.accuracies()
    payload = {
        "jobs": jobs, "ctx": ctx,
        "blob": {"title": blob["title"], "type_chart": blob["type_chart"],
                 "poks": {s: _species_record(blob["poks"].get(s)) for s in sorted(species)},
                 "moves": {m: blob["moves"].get(m) for m in sorted(moves)}},
        "accuracy": {m: acc.get(metrics._compact(pressure.MOVE_SPELLING.get(m, m)))
                     for m in sorted(moves)},
        "engine": engine_hash(), "scorer": scorer_hash(kind, previous),
    }
    text = json.dumps(payload, sort_keys=True, default=sorted)
    return hashlib.sha256(text.encode()).hexdigest()[:20]


# ---- every stored score, as a unit -------------------------------------------

class Unit:
    """One stored score: where it lives, how to build its job, and how to
    turn the calculator's answer into the stored record. `finish(out, ctx,
    seconds)` makes the record from one Node run of the job; a unit whose
    record takes more than one run (B6's levers) passes `compute(built,
    blob_path)` instead."""

    def __init__(self, kind, name, build, finish, get, put, compute=None):
        self.kind, self.name = kind, name
        self._build, self._finish, self._get, self._put = build, finish, get, put
        self._compute = compute
        self._built = None

    def built(self):
        if self._built is None:
            self._built = self._build()
        return self._built

    def stored(self):
        return self._get()

    def compute(self, blob_path):
        if self._compute is not None:
            return self._compute(self.built(), blob_path)
        jobs, ctx, _fp_ctx = self.built()
        t0 = time.time()
        out = pressure.run_node(blob_path, jobs)
        return self._finish(out, ctx, time.time() - t0)

    def store(self, record):
        self._put(record)


class Files:
    """The four result files, loaded once and saved when changed."""

    def __init__(self):
        self.pressure = pressure.load()
        self.calibrate = calibrate.load()
        self.refs = {h: refpressure.load(h) for h in refpressure.HACKS}
        self.shape = shape.load()
        self.b6 = b6.load()
        self.dirty = set()

    def save(self):
        if "pressure" in self.dirty:
            pressure.save(self.pressure)
        if "calibrate" in self.dirty:
            calibrate.save(self.calibrate)
        for h in refpressure.HACKS:
            if f"ref {h}" in self.dirty:
                refpressure.save(h, self.refs[h])
        if "shape" in self.dirty:
            shape.save(self.shape)
        if "b6" in self.dirty:
            b6.save(self.b6)
        self.dirty.clear()


class Sides:
    """The player's side per split and cap, built once each."""

    def __init__(self, blob):
        self.blob, self.cache = blob, {}

    def at(self, split, cap=None):
        caps = pool.caps()
        cap = caps[split] if cap is None else cap
        if (split, cap) not in self.cache:
            self.cache[(split, cap)] = (pool.pool(split, self.blob) if cap == caps[split]
                                        else shape.side_at(split, cap, self.blob))
        return self.cache[(split, cap)]


def _fight_ctx(ctx):
    """What a story fight's score takes besides its job file."""
    return {k: ctx[k] for k in ("key", "label", "split", "cap", "pool", "weather", "trick_room",
                                "parties")}


def units(blob, files, sides, kinds=KINDS):
    """Every stored score, in the order the tools write them."""
    out = []
    fights = data.fights()["fights"]
    if "pressure" in kinds:
        for fight in fights:
            def build(fight=fight):
                jobs, ctx = pressure.fight_jobs(fight, blob, side=sides.at(fight["split"]))
                return jobs, ctx, _fight_ctx(ctx)

            def put(r, key=fight["key"]):
                files.pressure["fights"][key] = r
                files.dirty.add("pressure")
            out.append(Unit("pressure", fight["key"], build,
                            lambda o, c, s: pressure.score_jobs(o, c, blob, s),
                            lambda key=fight["key"]: files.pressure["fights"].get(key), put))
    if "calibrate" in kinds:
        by_constant = {t["constant"]: t for t in data.oxide_trainers().values()}
        for constant, split, key, label in calibrate.EXTRA:
            t = by_constant[constant]
            fight = {"key": key, "label": label, "split": split, "tr_ids": [t["tr_id"]]}

            def build(fight=fight, t=t):
                jobs, ctx = pressure.fight_jobs(fight, blob, side=sides.at(fight["split"]),
                                                parties=[t["party"]])
                return jobs, ctx, _fight_ctx(ctx)

            def put(r, key=key):
                files.calibrate["fights"][key] = r
                files.dirty.add("calibrate")
            out.append(Unit("calibrate", key, build,
                            lambda o, c, s: pressure.score_jobs(o, c, blob, s),
                            lambda key=key: files.calibrate["fights"].get(key), put))
    if "ref" in kinds:
        for hack in refpressure.HACKS:
            for fight in fights:
                if not refpressure.parties(hack, fight):
                    continue

                def build(hack=hack, fight=fight):
                    built = refpressure.ref_jobs(hack, fight, blob, side=sides.at(fight["split"]))
                    if built is None:
                        return None
                    jobs, ctx = built
                    return jobs, ctx, {k: ctx[k] for k in ("hack", "key", "label", "split", "cap",
                                                           "pool", "ps", "categories", "trainers")}

                def put(r, hack=hack, key=fight["key"]):
                    files.refs[hack]["fights"][key] = r
                    files.dirty.add(f"ref {hack}")
                out.append(Unit("ref", f"{hack} {fight['key']}", build,
                                lambda o, c, s: refpressure.score_ref_jobs(o, c, s),
                                lambda hack=hack, key=fight["key"]:
                                    files.refs[hack]["fights"].get(key), put))
    if "shape" in kinds:
        out += shape_units(blob, files, sides)
    if "b6" in kinds or "b6lever" in kinds:
        out += b6_units(blob, files, sides, kinds)
    return out


def b6_units(blob, files, sides, kinds):
    """B6's ordinary trainers ("b6") and each story fight's levers
    ("b6lever"), stored in b6.json."""
    out = []
    res = files.b6
    if "b6" in kinds:
        for tr in sorted(b6.placements()):
            def build(tr=tr):
                fight, parties = b6.trainer_fight(tr)
                jobs, ctx = pressure.fight_jobs(fight, blob, side=sides.at(fight["split"]),
                                                parties=parties)
                return jobs, ctx, dict(_fight_ctx(ctx), placement=b6.placements()[tr])

            def put(r, tr=tr):
                res.setdefault("trainers", {})[str(tr)] = r
                files.dirty.add("b6")
            out.append(Unit("b6", f"trainer {tr}", build,
                            lambda o, c, s, tr=tr: b6.trainer_record(
                                pressure.score_jobs(o, c, blob, s), tr),
                            lambda tr=tr: res.get("trainers", {}).get(str(tr)), put))
    if "b6lever" in kinds:
        caps = pool.caps()
        for fight, parties in b6.boss_fights():
            def build(fight=fight, parties=parties):
                split = fight["split"]
                side = sides.at(split)
                jobs, ctx = pressure.fight_jobs(fight, blob, side=side, parties=parties)
                capped = {str(d): sides.at(split, caps[split] + d)
                          for d in (-b6.CAP_STEP, b6.CAP_STEP)}
                inputs = b6.lever_inputs(fight, side, capped, blob)
                fp = dict(_fight_ctx(ctx), levers=b6._fp_view(inputs))
                return jobs, dict(ctx, inputs=dict(inputs, side=side)), fp

            def compute(built, blob_path, fight=fight, parties=parties):
                jobs, ctx, _fp = built
                return b6.lever_record(fight, parties, jobs, ctx, ctx["inputs"], blob, blob_path)

            def put(r, key=fight["key"]):
                res.setdefault("fights", {})[key] = r
                files.dirty.add("b6")
            out.append(Unit("b6lever", f"levers {fight['key']}", build, None,
                            lambda key=fight["key"]: res.get("fights", {}).get(key), put,
                            compute=compute))
    return out


def _shape_reduce(r, extra=None):
    kept = {k: r[k] for k in shape.SCORE_KEYS}
    kept.update(extra or {})
    return kept


def shape_units(blob, files, sides):
    """The grid's cells, as shape.run_bosses and run_filler write them."""
    out = []
    caps = data.fights()["caps"]
    res = files.shape

    def cell(kind_path, fight, parties, side_split, cap, extra=None):
        def build():
            side = sides.at(side_split, cap)
            jobs, ctx = pressure.fight_jobs(fight, blob, side=side, parties=parties, cap=cap)
            return jobs, ctx, dict(_fight_ctx(ctx), extra=extra)

        def finish(o, c, s):
            return _shape_reduce(pressure.score_jobs(o, c, blob, s), extra)

        def get():
            node = res
            for k in kind_path:
                node = node.get(k) if isinstance(node, dict) else None
                if node is None:
                    return None
            return node

        def put(r):
            node = res
            for k in kind_path[:-1]:
                node = node.setdefault(k, {})
            node[kind_path[-1]] = r
            files.dirty.add("shape")
        return Unit("shape", "/".join(kind_path), build, finish, get, put)

    groups = [(g, key) + shape._fight_parties(key) for g, keys in shape.GROUPS.items()
              for key in keys]
    zfight, zparties = shape._zone_boss_fight()
    groups.append(("zone", zfight["key"], zfight, zparties))
    for group, key, fight, parties in groups:
        cap = shape.REFERENCE_CAP[group]
        for delta in shape.DELTAS:
            out.append(cell(("bosses", group, key, str(delta)), fight,
                            shape.shifted(parties, cap, delta), shape.SIDE_OF[group], cap))
    for split, ids in shape._reference_filler().items():
        for tr in ids:
            fight, parties = shape._filler_fight(tr, split)
            extra = {"ace_below_cap": caps[split] - max(m["level"] for m in parties[0])}
            out.append(cell(("filler", split, str(tr)), fight, parties, split, caps[split], extra))
    zcap = shape.REFERENCE_CAP["zone"]
    for tr in shape._zone_filler():
        fight, parties = shape._filler_fight(tr, "Galactic")
        for delta in shape.FILLER_DELTAS:
            out.append(cell(("filler", f"zone {delta}", str(tr)), fight,
                            shape.shifted(parties, zcap, delta), shape.SIDE_OF["zone"], zcap))
    return out


# ---- the runs ----------------------------------------------------------------

def _strip(o):
    if isinstance(o, dict):
        return {k: _strip(v) for k, v in o.items() if k not in TIMING and k not in MARKS}
    if isinstance(o, list):
        return [_strip(v) for v in o]
    return o


def _plain(record):
    """A record as JSON would give it back, so a fresh result compares with
    a stored one (tuples become lists, and so on)."""
    return json.loads(json.dumps(record))


def _one(u, mode, blob, blob_path, files):
    """What one unit comes to under `mode`: a count's label, and whether a
    recomputed score disagreed with the stored one."""
    built = u.built()
    if built is None:
        return None, False
    jobs, _ctx, fp_ctx = built
    fp = fingerprint(u.kind, jobs, fp_ctx, blob)
    old = u.stored()
    current = old is not None and old.get("fingerprint") == fp
    if mode == "status":
        return ("missing" if old is None else "stale" if not current
                else "verified" if old.get("verified") else "unverified"), False
    if mode == "seed":
        if old is None or "fingerprint" in old:
            return "left as it was", False
        u.store(dict(old, fingerprint=fp, verified=False))
        return "seeded", False
    if mode == "restamp":
        # A score current under the previous definition is current under
        # this one, which reads a subset of the same inputs; it keeps its
        # verified mark.
        if current or old is None:
            return "left as it was", False
        if old.get("fingerprint") != fingerprint(u.kind, jobs, fp_ctx, blob, previous=True):
            return "stale either way", False
        u.store(dict(old, fingerprint=fp))
        return "restamped", False
    if mode == "rescore":
        if current:
            return "reused", False
        u.store(dict(_plain(u.compute(blob_path)), fingerprint=fp, verified=False))
        files.save()
        return "recomputed", False
    if not current or old.get("verified"):
        return ("stale" if not current else "already verified"), False
    r = _plain(u.compute(blob_path))
    if _strip(r) != _strip(old):
        return "disagreed", True
    u.store(dict(old, verified=True))
    files.save()
    return "verified", False


def run(mode, kinds=KINDS, names=None, out=sys.stdout):
    """mode: "rescore", "verify", "status" or "seed". Prints and returns
    the counts, which say how many scores a run recomputed and how many it
    reused."""
    blob = calc_export.build()
    files, sides = Files(), Sides(blob)
    counts = collections.Counter()
    mismatched = []
    with tempfile.TemporaryDirectory(prefix="oxide-rescore-") as tmp:
        blob_path = os.path.join(tmp, "blob.json")
        with open(blob_path, "w", encoding="utf-8") as f:
            json.dump(blob, f)
        for u in units(blob, files, sides, kinds):
            if names and u.name not in names:
                continue
            try:
                label, disagreed = _one(u, mode, blob, blob_path, files)
            finally:
                u._built = None      # a built job is large; keep one at a time
            if label is None:
                continue
            counts[f"{u.kind} {label}"] += 1
            if disagreed:
                mismatched.append(u.name)
            if label in ("recomputed", "verified", "disagreed"):
                print(f"{mode} {u.kind} {u.name}: {label}", flush=True)
        files.save()
    for k in sorted(counts):
        print(f"{k}: {counts[k]}", file=out)
    if mismatched:
        print(f"disagreed, left unverified: {', '.join(mismatched)}", file=out)
    return counts


def check(blob=None, kinds=KINDS):
    """[(unit name, problem)] for every stored score of `kinds` whose
    fingerprint does not match its inputs or that is not verified. test_b3
    reads it for the scores before B6, test_b6 for B6's."""
    blob = calc_export.build() if blob is None else blob
    files, sides = Files(), Sides(blob)
    problems = []
    for u in units(blob, files, sides, kinds):
        label, _disagreed = _one(u, "status", blob, None, files)
        u._built = None
        if label not in (None, "verified"):
            problems.append((u.name, label))
    return problems


def main(argv=None):
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--verify", action="store_true")
    g.add_argument("--status", action="store_true")
    g.add_argument("--seed", action="store_true")
    g.add_argument("--restamp", action="store_true",
                   help="move scores current under the first engine definition to the narrower one")
    ap.add_argument("--kind", action="append", choices=KINDS, default=[])
    ap.add_argument("--name", action="append", default=[],
                    help="one score, as the run prints it (a fight key, 'kaizo roark', ...)")
    args = ap.parse_args(argv)
    mode = ("verify" if args.verify else "status" if args.status else "seed" if args.seed
            else "restamp" if args.restamp else "rescore")
    run(mode, tuple(args.kind) or KINDS, set(args.name) or None)
    return 0


if __name__ == "__main__":
    sys.exit(main())

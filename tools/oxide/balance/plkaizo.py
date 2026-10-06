"""Platinum Kaizo's trainer teams read by the perfect-line scorer, for Ian's
blind study of how Kaizo builds its teams (the Oxide Overseer, 2026-09-30:
rewrite the study's scores from the new scorer).

    PYTHONPATH=. python3 -m tools.oxide.balance.plkaizo              # read what is not yet read
    PYTHONPATH=. python3 -m tools.oxide.balance.plkaizo --table T.md # the table from the readings

The fights are the ninety kaizoteams.py chose (every boss, and about six
other trainers a split spread by difficulty), read back from the old
scores.md so the two versions compare fight for fight. Each is read twice,
as plrescore reads Oxide's own: a boss blind and planned, any other fight
blind only.

1. Against Kaizo's own player. A box is one run's catches: a starter, then
   one Pokemon drawn from each Kaizo wild area open by the split (an
   encounter placed by its level as the learnset study places it, behind
   its rod or Surf, in an area reachable by then; see GATE),
   each evolved as far as Kaizo's evolutions allow by Kaizo's cap, at the
   cap, and a species caught twice kept once. Its four moves are chosen by
   fightsim's moveset rule from Kaizo's level-up lists by Ian's capture
   rule (no TMs, tutors or egg moves); a Pokemon left with no usable move
   is left out. The teams fight at Kaizo's levels.
2. Against Oxide's player: Oxide's random boxes at the matching split and
   cap, as Oxide's own fights are read, with each Kaizo Pokemon kept at its
   distance under the cap.

Trainer Pokemon keep all four of their moves, status included, and their
held items; species, move and ability data are Oxide's where Kaizo's
differ. A Kaizo ability Oxide's species cannot have becomes its first,
except a weather ability, which is kept so the team keeps its weather.
Typed Hidden Power is Hidden Power at 60 power of its type. Kaizo's AI
flags map bit for bit onto the game's (their names are the editor's); a
trainer the split sheets supply without flags gets Basic, Evaluate Attack
and Expert, the flags almost every Kaizo trainer has. A multi battle's two
trainers are one double battle with their teams interleaved, the player
alone; Barry's three starter variants are met in turn by the boxes.
"""
import argparse
import collections
import functools
import json
import multiprocessing as mp
import os
import random
import re
import sys
import time

from . import fightsim as fs, kaizoteams as K, learnwild, perfectline as pl, plscore as S, pool
from . import pboxes as boxes

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(S.RESULTS, "kaizo.json")
OLD_TABLE = os.path.expanduser("~/oxide-trials/kaizo-teams/scores.md")
FLAG_BITS = {"Prioritize Effectiveness": 0, "Evaluate Attacks": 1, "Expert": 2, "Prioritize Status": 3,
             "Risky Attacks": 4, "Prioritize Damage": 5, "Partner": 6, "Double Battle": 7,
             "Prioritize Healing": 8, "Utilize Weather": 9, "Harassment": 10}
DEFAULT_FLAGS = 0b111


# ---- the fights --------------------------------------------------------------

def old_rows():
    """[(home split title, label)] in the old table's order."""
    out = []
    for line in open(OLD_TABLE, encoding="utf-8"):
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) != 8 or not re.match(r"^\w[\w ]* \(\w+\)$", cells[0]) or cells[0].startswith("Kaizo"):
            continue
        out.append((cells[0].split(" (")[0], cells[1].rsplit(" (", 1)[0]))
    return out


@functools.lru_cache(maxsize=None)
def chosen():
    """[(fight, [trainer records])] for the old table's fights."""
    trainers = K.load_trainers()
    caps = K.kaizo_caps(trainers)
    fs_ = K.fights(trainers, caps)
    by = {(K.TITLE[f["home"]], f["label"]): f for f in fs_}
    rec = {(t["ksplit"], t["trainer"]): t for t in reversed(trainers)}
    out = []
    for key in old_rows():
        f = by[key]
        out.append((f, [rec[(f["ksplit"], n)] for n in f["names"]]))
    return out, caps


def flags_of(members):
    given = [fl for u in members for fl in (u.get("ai_flags") or [])]
    if not given:
        return DEFAULT_FLAGS
    return sum(1 << FLAG_BITS[n] for n in set(given) if n in FLAG_BITS)


def trainer_mon(m, level, notes):
    """One Kaizo trainer Pokemon as fightsim reads a party member, or None."""
    blob = K._blob()
    name = K.species_name(m["species"])
    if not name:
        notes["species"].add(m["species"])
        return None
    have = (blob["poks"][name].get("abilities") or {})
    kab = m.get("ability") or have.get("0")
    ability = kab if kab in have.values() or kab in fs.ABILITY_WEATHER else have.get("0")
    if ability != kab:
        notes["abilities"].add(f"{name} {kab}")
    elif kab not in have.values():
        notes["weather_kept"].add(f"{name} {kab}")
    moves, move_data = [], {}
    for mv in m.get("moves") or []:
        if not mv:
            continue
        n, d = K.move_name(mv)
        if not n:
            notes["moves"].add(mv)
            continue
        if d:
            # Typed Hidden Power: the plain move, its type set for the calculator.
            n = "Hidden Power"
            move_data[n] = d
        if n not in moves:
            moves.append(n)
    iv = (m.get("difficulty") if isinstance(m.get("difficulty"), int) else 255) * 31 // 255
    return {"species": name, "level": level, "item": (m.get("item") or "").replace("’", "'") or None,
            "ability": ability, "nature": m.get("nature") or "Hardy", "ivs": {k: iv for k in K.STATS},
            "evs": {k: 0 for k in K.STATS}, "moves": moves, "move_data": move_data}


def parties(f, members, level_of, notes):
    """(parties, doubles): Barry's variants as separate parties; a multi
    battle's two teams interleaved into one."""
    if f["variants"]:
        teams = [u["team"] for u in members]
    elif len(members) > 1:
        a, b = members[0]["team"], members[1]["team"]
        teams = [[m for pair in zip(a, b) for m in pair] + a[len(b):] + b[len(a):]]
    else:
        teams = [members[0]["team"]]
    out = []
    for team in teams:
        built = [trainer_mon(m, level_of(m["level"]), notes) for m in team]
        out.append([x for x in built if x])
    doubles = f["battle"] in ("Double", "Multi") and max(len(p) for p in out) > 1
    return out, doubles


# ---- Kaizo's player -------------------------------------------------------------

# The Kaizo split from which each way of meeting a Pokemon is open: the Old
# Rod from Jubilife, the Good Rod from Route 209 and Surf after Wake's badge
# (vanilla Platinum's order, this track's reading), and the Super Rod on
# Route 222 in Volkner's split (Ian, 2026-09-30).
GATE = {"old_rod": "roark", "good_rod": "fantina", "surf": "byron", "super_rod": "volkner"}
LAND = ("land", "day", "night")


def _at(e, galactic_maps):
    """The Kaizo split index an encounter's level places it in: the
    learnset study's gym split, with a League-level area among the Galactic
    split's own maps placed there."""
    s = e["split"]
    if s == "League":
        name = e["area"].strip().lower()
        return K.KAIZO_ORDER.index("galactic" if name in galactic_maps else "elite-four")
    return K.KAIZO_ORDER.index(s.lower())


@functools.lru_cache(maxsize=None)
def kaizo_areas(ksplit):
    """{area: [(species, catch level)]} open to Kaizo's player by the split.
    An encounter is open when its level's split has come (the learnset
    study's placement), its rod or Surf is in hand, and its area is
    reachable: from its grass's earliest split, or from Surf when the area
    has no grass."""
    galactic_maps = set()
    with open(os.path.join(K.TEAMS_DIR, "galactic-split.json"), encoding="utf-8") as fh:
        for t in json.load(fh):
            galactic_maps.add(re.split(r"\s*\(", t.get("location") or "")[0].strip().lower())
    enc = learnwild.kaizo_encounters()
    reach = {}
    for e in enc:
        if e["kind"] in LAND:
            reach[e["area"]] = min(reach.get(e["area"], 99), _at(e, galactic_maps))
    now = K.KAIZO_ORDER.index(ksplit)
    out = collections.defaultdict(set)
    for e in enc:
        gate = K.KAIZO_ORDER.index(GATE.get(e["kind"], "roark"))
        area = reach.get(e["area"], K.KAIZO_ORDER.index(GATE["surf"]))
        if max(_at(e, galactic_maps), gate, area) <= now:
            out[e["area"]].add((e["species"], e["lo"]))
    return {a: sorted(v) for a, v in sorted(out.items())}


def final_stage(sp, level, cap, rng):
    """The stage a catch reaches by the cap, a branch drawn at random."""
    while True:
        kids = [(max(need, level + 1), c) for need, c in K._children().get(sp, [])
                if max(need, level + 1) <= cap]
        if not kids:
            return sp
        level, sp = rng.choice(sorted(kids))


def kaizo_box(ksplit, cap, rng):
    box = [final_stage(rng.choice(K.STARTERS), K.STARTER_LEVEL, cap, rng)]
    for area, opts in kaizo_areas(ksplit).items():
        opts = [o for o in opts if o[1] <= cap]
        if opts:
            sp, lv = rng.choice(opts)
            box.append(final_stage(sp, lv, cap, rng))
    return list(dict.fromkeys(box))


@functools.lru_cache(maxsize=None)
def kaizo_records(ksplit, cap):
    """The side records for every species Kaizo's player can have by the
    split: at the cap, average IVs, either regular ability, and four moves
    by fightsim's rule from what Kaizo's lists teach by the capture rule."""
    blob = K._blob()
    moves_of = collections.defaultdict(set)
    catches = {(sp, K.STARTER_LEVEL) for sp in K.STARTERS}
    catches |= {c for opts in kaizo_areas(ksplit).values() for c in opts}
    for sp, level in sorted(catches):
        if level > cap:
            continue
        start = set(K.calc_trainers.default_moves(K._klist(sp), level))
        start |= {mv for lv, mv in K._klist(sp) if level < lv <= cap}
        todo = [(sp, level, start)]
        while todo:
            stage, now, known = todo.pop()
            moves_of[stage] |= known
            for need, child in K._children().get(stage, []):
                at = max(need, now + 1)
                if at > cap:
                    continue
                todo.append((child, at, known | {mv for lv, mv in K._klist(child)
                                                 if max(at, 2) <= lv <= cap}))
    tiers = fs.status_tiers()
    out = []
    for sp in sorted(moves_of):
        name = K.canon.showdown_name(sp)
        if not name or name not in blob["poks"]:
            continue
        names = sorted({n for n, d in (K.move_name(mv) for mv in moves_of[sp]) if n and not d})
        rec = {"species": name, "constant": sp, "how": "kaizo", "level": cap, "ability": None,
               "item": None, "nature": "Hardy", "ivs": {k: pool.AVERAGE_IV for k in K.STATS},
               "evs": {k: 0 for k in K.STATS}}
        rec["moves"] = fs.player_moves(rec, names, tiers, blob["poks"][name].get("types") or [])
        # A Pokemon with no move the scorer can use (Kaizo's Abra, which
        # evolves at 45 and knows only Teleport) never fights; the box
        # leaves it out.
        if rec["moves"]:
            out.append(rec)
    return out


# ---- reading -------------------------------------------------------------------

def prepare(f, members, which, caps):
    """(prep, box_fn, notes) for one fight against one side."""
    notes = {k: set() for k in ("species", "moves", "abilities", "weather_kept")}
    kcap, ocap = caps[f["home"]], pool.caps()[f["oxide"]]
    if which == "kaizo":
        level_of = lambda lv: lv
        split, cap, side = f["oxide"], kcap, kaizo_records(f["home"], kcap)
        box_fn = lambda rng: kaizo_box(f["home"], kcap, rng)
    else:
        level_of = lambda lv: K.oxide_level(lv, kcap, ocap)
        split, cap, side = f["oxide"], ocap, None
        box_fn = lambda rng: boxes.box_from("random", f["oxide"], rng)
    ps, doubles = parties(f, members, level_of, notes)
    flags = flags_of(members)
    st = fs.prepare(split, ps, f["weather"], f["trick_room"], cap=cap, doubles=doubles, given_side=side)
    prep = {"st": st, "split": split, "label": f["label"], "key": f["key"],
            "variants": [(keys, flags, None) for keys in st["bosses"]]}
    if doubles:
        st["battle"] = "doubles"
        st["group_flags"] = [flags]
        prep["doubles"] = "doubles"
    return prep, box_fn, notes


def read(prep, box_fn, boss, seed=S.SEED, procs=None):
    """plscore.read_fight's steps with this fight's own boxes; a rival's
    variants are met by the boxes in turn."""
    st = prep["st"]
    rng = random.Random(seed)
    planned = S.PLANNED if boss else 0
    jobs, sizes = [], []
    for bi in range(S.BOXES):
        box = box_fn(random.Random(seed * 100 + bi))
        keys = S.box_keys(st, box, rng)
        sizes.append(len(keys))
        boss_keys, flags, _s = prep["variants"][bi % len(prep["variants"])]
        for j, team in enumerate(S.sixes(keys, S.BLIND, rng)):
            jobs.append((team, boss_keys, flags, f"blind:{bi}", pl.BUDGET, False, seed + 1000 * bi + j))
        weights = pl.matchup_wins(st, keys, boss_keys, flags, pl.BUDGET)
        for j, team in enumerate(S.sixes(keys, planned, rng, weights)):
            jobs.append((team, boss_keys, flags, f"planned:{bi}", pl.BUDGET, False,
                         seed + 1000 * bi + 100 + j))
    t0 = time.time()
    with mp.get_context("fork").Pool(procs or max(1, os.cpu_count() - 2), initializer=S._init,
                                     initargs=(prep,)) as p:
        rows = p.map(S._job, jobs, chunksize=1)
    out = S.summarise(rows)
    out.update(seconds=round(time.time() - t0, 1), box_sizes=[min(sizes), max(sizes)])
    # Through JSON, as plrescore stores a reading.
    return json.loads(json.dumps(out))


def load():
    if os.path.exists(OUT):
        with open(OUT, encoding="utf-8") as fh:
            return json.load(fh)
    return {"fights": {}}


def save(store):
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT + ".tmp", "w", encoding="utf-8") as fh:
        json.dump(store, fh, indent=1, sort_keys=True)
        fh.write("\n")
    os.replace(OUT + ".tmp", OUT)


def run(only=None, procs=None):
    store = load()
    fights, caps = chosen()
    store["caps"] = caps
    store["oxide_caps"] = {f["oxide"]: pool.caps()[f["oxide"]] for f, _m in fights}
    for f, members in fights:
        if only and f["key"] not in only:
            continue
        r = store["fights"].setdefault(f["key"], {k: f[k] for k in (
            "key", "label", "names", "ids", "ksplit", "home", "oxide", "kind", "superboss", "variants",
            "battle", "size", "top", "weather", "trick_room", "notes", "from_sheet")})
        r["flags"] = flags_of(members)
        r["flags_given"] = any(u.get("ai_flags") for u in members)
        for which in ("kaizo", "oxide"):
            if "vs_" + which in r:
                continue
            prep, box_fn, notes = prepare(f, members, which, caps)
            r["vs_" + which] = read(prep, box_fn, f["kind"] == "boss", procs=procs)
            r["left_out"] = {k: sorted(v) for k, v in notes.items() if v and k not in ("abilities", "weather_kept")}
            r["abilities_swapped"] = sorted(notes["abilities"])
            r["weather_kept"] = sorted(notes["weather_kept"])
            print(f"{f['label'][:40]:40} vs {which:5} blind {r['vs_' + which]['blind_rate']:.2f} "
                  f"planned {r['vs_' + which]['planned_rate']:.2f} ({r['vs_' + which]['seconds']} s)",
                  flush=True)
            save(store)
    return store


# ---- the table -------------------------------------------------------------------

def judged(r, which):
    """(clean rate, deaths, wipe) as the fight is judged: a boss by its
    planned line, any other fight blind."""
    v = r["vs_" + which]
    k = "planned" if r["kind"] == "boss" else "blind"
    return v[f"{k}_rate"], v[f"{k}_deaths"], v[f"{k}_wipe"]


def note(r):
    """The old table's note, plus the flags a sheet trainer was given."""
    text = K.note(dict(r, weather_kept=r.get("weather_kept", []), left_out=r.get("left_out", {})))
    if not r.get("flags_given"):
        text += ("; " if text else "") + "no AI flags given, read with Basic, Evaluate Attack and Expert"
    return text


def table(store):
    lines = ["| Kaizo split (Oxide's) | Trainer (id) | Kind | Battle | Team | Read | "
             "Kaizo's pool: clean, deaths, wipe | Oxide's pool: clean, deaths, wipe | Note |",
             "|---|---|---|---|---|---|---|---|---|"]
    fights, _caps = chosen()
    for f, _m in fights:
        r = store["fights"].get(f["key"])
        if not r or "vs_oxide" not in r:
            continue
        ids = ", ".join(str(i) for i in r["ids"] if i is not None) or "none"
        cells = []
        for which in ("kaizo", "oxide"):
            c, d, w = judged(r, which)
            cells.append(f"{c:.2f}, {d:.2f}, {w:.2f}")
        lines.append(f"| {K.TITLE[r['home']]} ({r['oxide']}) | {r['label']} ({ids}) | {r['kind']} | "
                     f"{r['battle']} | {r['size']}, top {r['top']} | "
                     f"{'planned' if r['kind'] == 'boss' else 'blind'} | {cells[0]} | {cells[1]} | {note(r)} |")
    return "\n".join(lines) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", nargs="*")
    ap.add_argument("--procs", type=int)
    ap.add_argument("--table")
    a = ap.parse_args(argv)
    if a.table:
        with open(a.table, "w", encoding="utf-8") as fh:
            fh.write(table(load()))
        return 0
    run(set(a.only) if a.only else None, a.procs)
    return 0


if __name__ == "__main__":
    sys.exit(main())

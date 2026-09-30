"""Platinum Kaizo's trainer teams scored two ways, for Ian's blind study of
how Kaizo builds its teams (the Oxide Overseer, 2026-09-29).

    PYTHONPATH=. python3 -m tools.oxide.balance.kaizoteams TABLE.md RESULTS.json [--workers 16]

The teams are ~/oxide-trials/kaizo-teams/kaizo-trainers/<split>-split.json,
which the Overseer built from Kaizo's trainer tables (371 of 436 trainers;
the other 65 are read from the split sheets and carry a "note"). Nothing is
written into that folder: the study that reads it is blind to Oxide's rules.

Which fights. Every boss (the gym leaders, each of Barry's fights with its
three starter variants as one fight, every Commander and Cyrus, the Elite
Four, the Champion and the two optional superbosses), and about six other
trainers a split. The six are chosen from every non-boss fight placed in
the split by the team scorer's instant estimate against Oxide's side: the
10th, 30th, 50th, 70th and 90th percentile and the hardest, with an Ace
Trainer added where the split has one and none was picked. The player's
tag partners are left out; a multi battle's two trainers are one fight,
scored as one party, as the reference scorer does.

Two scores each, both by the same machinery as Oxide's own fights
(pressure.py's matchups, B6's safe switch-ins on Ian's scale):

1. Against Kaizo's own player: every species Kaizo's wild tables give by
   the split (the learnset study's reading, each area in the split of its
   median level), and the three starters, evolved as Kaizo's evolutions
   allow by Kaizo's cap, knowing their moves from Kaizo's level-up lists by
   Ian's capture rule (the four at capture, then each stage's level-ups to
   the cap). No TMs, no held items: Kaizo's placements of both are not in
   the data this track holds. The teams fight at Kaizo's own levels.
2. Against Oxide's player: pool.pool at the matching Oxide split and its
   cap, unchanged. Each Kaizo team is carried onto that split by keeping
   every Pokemon's distance under the cap (a Kaizo Pokemon three levels
   under Kaizo's cap fights three under Oxide's), so the score reads the
   team, not Kaizo's level curve.

Species stats and types, abilities and move data are Oxide's wherever
Kaizo's differ (the Overseer's instruction), counted in the results. A
Kaizo ability Oxide's species cannot have becomes its first ability, but a
Kaizo weather ability keeps its weather for that Pokemon, since a trainer's
weather is part of its team. Typed Hidden Power is the later games' fixed
60-power move of its type, as the reference scorer reads it. A species or
move Oxide lacks is left out and listed per fight.
"""
import argparse
import collections
import concurrent.futures
import difflib
import functools
import json
import os
import re
import sys

from ..encounters import calc_export, calc_trainers, canon
from . import b6, data, learngen, learnstudy as ls, learnwild, metrics, pool, pressure, teamscore

TEAMS_DIR = os.path.expanduser("~/oxide-trials/kaizo-teams/kaizo-trainers")
# Kaizo's own order of its splits, as its documentation lists the sheets:
# Volkner's gym comes before the Galactic HQ there.
KAIZO_ORDER = ["roark", "gardenia", "fantina", "maylene", "wake", "byron", "candice",
               "volkner", "galactic", "elite-four"]
TITLE = {"roark": "Roark", "gardenia": "Gardenia", "fantina": "Fantina", "maylene": "Maylene",
         "wake": "Wake", "byron": "Byron", "candice": "Candice", "volkner": "Volkner",
         "galactic": "Galactic", "elite-four": "League"}
# The Oxide split each Kaizo split is scored in, by place. Kaizo's Galactic
# split is Veilstone's warehouse and the Galactic HQ, which close Oxide's HQ
# split. Kaizo's Elite Four split holds Route 223, Victory Road and Barry's
# last fight, which are Oxide's Barry split, and then the League.
OXIDE_OF = {"roark": "Roark", "gardenia": "Gardenia", "fantina": "Fantina",
            "maylene": "Maylene", "wake": "Wake", "byron": "Byron", "candice": "Candice",
            "volkner": "Volkner", "galactic": "HQ", "elite-four": "Barry"}
LEAGUE_NAMES = ("Elite Four", "Champion")
BOSS = re.compile(r"^(Leader|LEADER|Commander|Elite Four|Champion|Barry #)|SUPERBOSS")
PARTNER = re.compile(r"TAG PARTNER|\(PARTNER\)|Tag Partner", re.I)
PAIRED = re.compile(r"(?:MULTI BATTLE|TAG BATTLE)\s+with\s+([^,)]+)", re.I)
WEATHER_WORDS = [(re.compile(r"\brain\b", re.I), "Rain"), (re.compile(r"\bhail\b", re.I), "Hail"),
                 (re.compile(r"\bsun\b", re.I), "Sun"), (re.compile(r"sandstorm", re.I), "Sand")]
STARTERS = ["SPECIES_TURTWIG", "SPECIES_CHIMCHAR", "SPECIES_PIPLUP"]
STARTER_LEVEL = 5
HIDDEN_POWER_BP = 60
QUANTILES = (0.1, 0.3, 0.5, 0.7, 0.9)
STATS = ("hp", "at", "df", "sa", "sd", "sp")


# ---- the teams --------------------------------------------------------------

def load_trainers():
    """[trainer] in Kaizo's walking order, each tagged with its split file."""
    out = []
    for split in KAIZO_ORDER:
        with open(os.path.join(TEAMS_DIR, f"{split}-split.json"), encoding="utf-8") as f:
            for pos, t in enumerate(json.load(f)):
                out.append(dict(t, ksplit=split, pos=pos))
    return out


def ace(t):
    return max((m["level"] for m in t["team"]), default=0)


def kaizo_caps(trainers):
    """{Kaizo split: its level cap}: the gym splits close at their leader's
    ace (the learnset study's stored seats), the Galactic split at the
    highest level among its bosses, and the League at 100."""
    caps = {s.lower(): c for s, c in ls.splits("kaizo") if s != "League"}
    caps["galactic"] = max(ace(t) for t in trainers
                           if t["ksplit"] == "galactic" and BOSS.search(t["trainer"]))
    caps["elite-four"] = 100
    return caps


def weather_of(t):
    """(field weather, trick room, notes) from the trainer's and its map's
    labels in the split sheets."""
    text = f"{t.get('location') or ''} {t['trainer']}"
    weather = next((w for rx, w in WEATHER_WORDS if rx.search(text)), None)
    notes = []
    if re.search(r"gravity", text, re.I):
        notes.append("Gravity, not modelled")
    if re.search(r"\bfog\b", text, re.I):
        notes.append("fog, not modelled")
    return weather, bool(re.search(r"trick room", text, re.I)), notes


def _last_word(name):
    base = re.split(r"\s*\(", name)[0]
    return re.sub(r"^(Galactic|Galacticf|GalacticF|Cyclist|CyclistF)", "", base.split()[-1]).lower()


def fights(trainers, caps):
    """[fight]: each trainer the player fights, a multi battle's two
    trainers as one fight and Barry's three starter variants as one."""
    used, out = set(), []
    by_split = collections.defaultdict(list)
    for t in trainers:
        by_split[t["ksplit"]].append(t)
    for split in KAIZO_ORDER:
        ts = by_split[split]
        for t in ts:
            key = (split, t["pos"])
            if key in used or PARTNER.search(t["trainer"]) or not t["team"]:
                continue
            members = [t]
            m = re.match(r"Barry #(\d+)", t["trainer"])
            if m:
                members = [u for u in ts if u["trainer"].startswith(f"Barry #{m.group(1)} ")]
            else:
                p = PAIRED.search(t["trainer"])
                if p:
                    want = _last_word(p.group(1).strip())
                    cands = [u for u in ts if (split, u["pos"]) not in used and u is not t
                             and u["team"] and PAIRED.search(u["trainer"])]
                    scored = sorted(cands, key=lambda u: (-difflib.SequenceMatcher(
                        None, want, _last_word(u["trainer"])).ratio(), abs(u["pos"] - t["pos"])))
                    if scored and difflib.SequenceMatcher(
                            None, want, _last_word(scored[0]["trainer"])).ratio() >= 0.75:
                        members = [t, scored[0]]
            for u in members:
                used.add((split, u["pos"]))
            out.append(make_fight(members, split, caps, variants=bool(m)))
    return out


def make_fight(members, split, caps, variants):
    t = members[0]
    top = max(ace(u) for u in members)
    names = [u["trainer"] for u in members]
    boss = any(BOSS.search(n) for n in names)
    kind = "boss" if boss else "Ace" if any(n.startswith("Ace Trainer") for n in names) \
        else "ordinary"
    # A trainer above its split's cap is fought later: it moves to the first
    # Kaizo split whose cap covers its ace, as B6 places Oxide's late visits.
    home = split
    if top > caps[split]:
        later = [s for s in KAIZO_ORDER[KAIZO_ORDER.index(split):] if caps[s] >= top]
        home = later[0] if later else KAIZO_ORDER[-1]
    oxide = OXIDE_OF[home]
    if home == "elite-four" and any(n.startswith(LEAGUE_NAMES) for n in names):
        oxide = "League"
    weather, trick_room, notes = weather_of(t)
    if not boss and any(re.search(r"gauntlet", f"{u.get('location') or ''} {u['trainer']}", re.I)
                        for u in members):
        notes.append("in a Kaizo gauntlet")
    if any(n.startswith("Leader Fantina ?") for n in names):
        notes.append("a second Fantina fight inside her gym")
    parties =[u["team"] for u in members] if variants else [[m for u in members for m in u["team"]]]
    battle = "Multi" if len(members) > 1 and not variants else (t.get("battle") or "from sheet")
    label = names[0].split(" (")[0] if variants else " and ".join(n.split(" (")[0] for n in names)
    label = " ".join(label.split()).rstrip(" -*")
    ids = [u["id"] for u in members]
    return {"key": f"{split}:{members[0]['pos']}", "label": label, "names": names, "ids": ids,
            "ksplit": split, "home": home, "oxide": oxide, "kind": kind,
            "superboss": any("SUPERBOSS" in n for n in names), "variants": variants,
            "battle": battle.replace(" Battle", ""), "size": max(len(p) for p in parties),
            "top": top, "weather": weather, "trick_room": trick_room, "notes": notes,
            "from_sheet": any(u.get("note") for u in members), "parties": parties}


# ---- names ------------------------------------------------------------------

@functools.lru_cache(maxsize=None)
def _blob():
    return calc_export.build()


@functools.lru_cache(maxsize=None)
def _compact_species():
    return {metrics._compact(k): k for k in _blob()["poks"]}


def species_name(name):
    """Kaizo's species name as the calculator's, or None."""
    poks = _blob()["poks"]
    n = name.replace("♂", "-M").replace("♀", "-F").replace("’", "'").strip()
    for cand in (n, re.split(r"\s*-\s*", n)[0]):
        if cand in poks:
            return cand
        k = _compact_species().get(metrics._compact(cand))
        if k:
            return k
    return None


def move_name(name):
    """(calculator name, move data) for a Kaizo move, or (None, None)."""
    m = re.match(r"^HP (\w+)$", name)
    if m:
        n = f"Hidden Power {m.group(1).title()}"
        return n, {"type": m.group(1).title(), "category": "Special",
                   "basePower": HIDDEN_POWER_BP, "priority": 0}
    r = ls.resolve(name, _blob()["moves"])
    return (r, None) if r else (None, None)


# ---- the boss side ----------------------------------------------------------

def boss_mon(m, level, notes):
    """The job record for one Kaizo trainer Pokemon at `level`, or None."""
    blob = _blob()
    name = species_name(m["species"])
    if not name:
        notes["species"].add(m["species"])
        return None
    rec = blob["poks"][name]
    have = rec.get("abilities") or {}
    ability = m.get("ability") or have.get("0")
    kaizo_ability = ability
    if ability not in have.values():
        notes["abilities"].add(f"{name} {ability}")
        ability = have.get("0")
    moves, move_data, every = [], {}, []
    for mv in m.get("moves") or []:
        if not mv:
            continue
        n, d = move_name(mv)
        if not n:
            notes["moves"].add(mv)
            continue
        every.append(n)
        if d:
            move_data[n] = d
            moves.append(n)
            continue
        r = blob["moves"][n]
        if r.get("category") == "Status":
            continue
        if n in pool.UNRELIABLE and not (n in pressure.ITEM_MOVES and m.get("item")):
            continue
        moves.append(n)
    iv = (m.get("difficulty") if isinstance(m.get("difficulty"), int) else 255) * 31 // 255
    item = (m.get("item") or "").replace("’", "'") or None
    job = {"species": name, "level": level, "item": item, "ability": ability,
           "nature": m.get("nature") or "Hardy", "ivs": {k: iv for k in STATS},
           "evs": {k: 0 for k in STATS}, "moves": moves, "move_data": move_data}
    weather = pressure.CALC_WEATHER.get(pressure.ABILITY_WEATHER.get(kaizo_ability))
    return job, every, kaizo_ability, weather


# ---- Kaizo's player ---------------------------------------------------------

@functools.lru_cache(maxsize=None)
def _children():
    out = collections.defaultdict(list)
    for child, (parent, level) in learngen.kaizo_reached().items():
        out[parent].append((level, child))
    return out


def _klist(sp):
    return sorted((ls.kaizo_lists().get(sp) or {}).get("list") or [])


@functools.lru_cache(maxsize=None)
def kaizo_catches(ksplit):
    """[(species constant, catch level)] Kaizo's player can make by the end
    of a Kaizo split. The learnset study places each wild area in the split
    of its median level; its splits are the gyms and the League, so the
    Galactic split, which comes after Volkner's in Kaizo, takes Volkner's
    and earlier areas and the League-level areas whose names appear among
    the Galactic split's own maps."""
    order = [s.title() for s in KAIZO_ORDER[:-2]] + ["League"]
    galactic_maps = set()
    with open(os.path.join(TEAMS_DIR, "galactic-split.json"), encoding="utf-8") as f:
        for t in json.load(f):
            galactic_maps.add(re.split(r"\s*\(", t.get("location") or "")[0].strip().lower())
    out = set((sp, STARTER_LEVEL) for sp in STARTERS)
    for e in learnwild.kaizo_encounters():
        s = e["split"]
        if ksplit == "galactic":
            ok = order.index(s) <= order.index("Volkner") or \
                (s == "League" and e["area"].strip().lower() in galactic_maps)
        elif ksplit == "elite-four":
            ok = True
        else:
            ok = order.index(s) <= order.index(TITLE[ksplit])
        if ok:
            out.add((e["species"], e["lo"]))
    return sorted(out)


BOX_RUNS = 300
BOX_SEED = 20260930


def _area_ok(ksplit, split, area, galactic_maps):
    """Whether a wild area placed in Kaizo split `split` is reached by the
    end of `ksplit`, by kaizo_catches' rule."""
    order = [s.title() for s in KAIZO_ORDER[:-2]] + ["League"]
    if ksplit == "galactic":
        return order.index(split) <= order.index("Volkner") or \
            (split == "League" and area.strip().lower() in galactic_maps)
    if ksplit == "elite-four":
        return True
    return order.index(split) <= order.index(TITLE[ksplit])


def _family(sp):
    parent = {child: p for child, (p, _lv) in learngen.kaizo_reached().items()}
    while sp in parent:
        sp = parent[sp]
    return sp


def _stage_at(sp, level, cap):
    """The last stage a Pokemon caught at `level` reaches by the cap along
    its first level evolution at each step."""
    now = level
    while True:
        nxt = sorted((max(need, now + 1), child) for need, child in _children().get(sp, [])
                     if max(need, now + 1) <= cap)
        if not nxt:
            return sp
        now, sp = nxt[0]


@functools.lru_cache(maxsize=None)
def kaizo_box_shares(ksplit, cap, runs=BOX_RUNS):
    """{stage: share}: a realistic Kaizo box at the end of `ksplit`, the
    counterpart of pool.box_shares for Oxide (2026-09-30). Each area
    reached gives its first encounter, drawn by its land table's slot rates
    (its Surf table's when it has no land table), under the dupes clause
    over families; the starters take turns. Each catch counts as the last
    stage it reaches by the cap."""
    import random
    from . import kaizo_docs
    docs = kaizo_docs.load()
    galactic_maps = set()
    with open(os.path.join(TEAMS_DIR, "galactic-split.json"), encoding="utf-8") as f:
        for t in json.load(f):
            galactic_maps.add(re.split(r"\s*\(", t.get("location") or "")[0].strip().lower())
    tables = {}
    for t in docs["field"].values():
        slots = [(r, learngen.kaizo_constant(sp), lv) for r, sp, lv in t["slots"] if sp]
        if t["rate"] and slots:
            split = ls.split_of("kaizo", sorted(lv for _r, _s, lv in slots)[len(slots) // 2])
            if _area_ok(ksplit, split, t["area"], galactic_maps):
                tables.setdefault(t["area"], slots)
    for t in docs["water"].values():
        slots = [(r, learngen.kaizo_constant(sp), lo) for r, sp, lo, _hi in t["surf"] if sp]
        if t["area"] in tables or not slots or not t["rates"].get("surf"):
            continue
        split = ls.split_of("kaizo", sorted(lv for _r, _s, lv in slots)[len(slots) // 2])
        if _area_ok(ksplit, split, t["area"], galactic_maps):
            tables[t["area"]] = slots
    rng = random.Random(BOX_SEED)
    counts = collections.Counter()
    for run_i in range(runs):
        box = [(STARTERS[run_i % len(STARTERS)], STARTER_LEVEL)]
        owned = {_family(box[0][0])}
        for area in sorted(tables):
            open_slots = [s for s in tables[area] if _family(s[1]) not in owned and s[2] <= cap]
            if not open_slots:
                continue
            r = rng.random() * sum(x[0] for x in open_slots)
            for rate, sp, lv in open_slots:
                r -= rate
                if r <= 0:
                    break
            box.append((sp, lv))
            owned.add(_family(sp))
        counts.update({_stage_at(sp, lv, cap) for sp, lv in box})
    return {sp: c / runs for sp, c in counts.items()}


def kaizo_side(ksplit, cap):
    """The player's side from Kaizo's own game: [{species, level, ability,
    item, nature, ivs, evs, moves}] like pool.pool's, and what was left out."""
    blob = _blob()
    moves_of = collections.defaultdict(set)
    for sp, level in kaizo_catches(ksplit):
        if level > cap:
            continue
        start = set(calc_trainers.default_moves(_klist(sp), level))
        start |= {mv for lv, mv in _klist(sp) if level < lv <= cap}
        todo = [(sp, level, start)]
        while todo:
            stage, now, known = todo.pop()
            moves_of[stage] |= known
            for need, child in _children().get(stage, []):
                at = max(need, now + 1)
                if at > cap:
                    continue
                todo.append((child, at, known | {mv for lv, mv in _klist(child)
                                                 if max(at, 2) <= lv <= cap}))
    side, missing, dropped = [], set(), collections.Counter()
    shares = kaizo_box_shares(ksplit, cap)
    for sp in sorted(moves_of):
        name = canon.showdown_name(sp)
        if not shares.get(sp):
            continue
        if not name or name not in blob["poks"]:
            missing.add(sp)
            continue
        names = []
        for mv in sorted(moves_of[sp]):
            n, d = move_name(mv)
            if not n or d:
                dropped[mv] += 1
                continue
            names.append(n)
        abilities = blob["poks"][name].get("abilities") or {}
        side.append({"species": name, "constant": sp, "how": "kaizo", "level": cap,
                     "ability": abilities.get("0"), "item": None, "nature": "Hardy",
                     "ivs": {k: pool.AVERAGE_IV for k in STATS}, "evs": {k: 0 for k in STATS},
                     # Four level-up moves: Kaizo's TM placements are not in
                     # this data, so nothing is taught.
                     "moves": pool.choose_four(name, set(names), set(), blob),
                     "box_share": round(shares[sp], 4)})
    return side, sorted(missing), dict(dropped)


# ---- scoring ----------------------------------------------------------------

def fight_jobs(fight, side, level_of):
    """(jobs, ctx) for one fight against one side, with each boss Pokemon's
    level given by level_of(its Kaizo level)."""
    notes = {k: set() for k in ("species", "moves", "abilities")}
    jobs = {"pokemon": {f"p{i}": p for i, p in enumerate(side)}, "pairs": []}
    bosses, shown, weather_kept = [], [], set()
    for v, party in enumerate(fight["parties"]):
        team = []
        for j, m in enumerate(party):
            built = boss_mon(m, level_of(m["level"]), notes)
            if built is None:
                continue
            job, every, kaizo_ability, own_weather = built
            key = f"b{v}.{j}"
            jobs["pokemon"][key] = job
            w = own_weather or fight["weather"]
            if own_weather and kaizo_ability != job["ability"]:
                weather_kept.add(f"{job['species']} {kaizo_ability}")
            bosses.append((v, key, job, w))
            team.append({"species": job["species"], "level": job["level"], "item": job["item"],
                         "ability": kaizo_ability, "moves": every})
            for i, p in enumerate(side):
                jobs["pairs"].append([key, f"p{i}", job["moves"], w])
                jobs["pairs"].append([f"p{i}", key, p["moves"], w])
            pressure.add_branches(jobs, key, dict(job, moves=every), job["moves"], side, w)
        shown.append(team)
    ctx = {"bosses": bosses, "side": len(side), "weights": pool.side_weights(side),
           "trick_room": fight["trick_room"],
           "parties": shown, "notes": {k: sorted(v) for k, v in notes.items()},
           "weather_kept": sorted(weather_kept)}
    return jobs, ctx


def score(jobs, ctx, out):
    """A fight's readings from the calculator's answer to its jobs."""
    rows = {(r["a"], r["d"]): r for r in out["results"]}
    per_mon = pressure.score_mons(ctx["bosses"], [f"p{i}" for i in range(ctx["side"])], rows,
                                  out["pokemon"], ctx["trick_room"], ctx.get("weights"))
    r = pressure.roll_up([dict(m) for m in per_mon])
    line = b6.scale_line()
    tactics = pressure.unseen(ctx["parties"])
    return {"safe": r["safe"], "scale": round(b6.on_scale(r["safe"], line), 2),
            "threat_chance": r["threat_chance"], "answers_bait": r["answers_bait"],
            "side": ctx["side"], "unseen_count": tactics["unseen_count"],
            "errors": sorted({f"{x['a']} {mv}: {v['error']}" for x in out["results"]
                              for mv, v in x["moves"].items() if "error" in v})[:5]}


def estimate(fight, oxide_cap, kcap):
    """The team scorer's instant estimate against Oxide's side, for choosing
    the spread: the teams at their Oxide levels, calibrated as teamscore
    calibrates it, on Ian's scale."""
    notes = {k: set() for k in ("species", "moves", "abilities")}
    parties = []
    for party in fight["parties"]:
        team = []
        for m in party:
            built = boss_mon(m, oxide_level(m["level"], kcap, oxide_cap), notes)
            if built:
                team.append(built[0])
        parties.append(team)
    safe, _t, _a, _rows = teamscore.raw_estimate(parties, fight["oxide"], fight["trick_room"])
    fit = teamscore._fit()
    safe = min(1.0, max(0.0, fit["alpha"] + fit["beta"] * safe)) if fit else safe
    return round(b6.on_scale(safe, b6.scale_line()), 2)


def oxide_level(level, kcap, ocap):
    """A Kaizo level carried onto Oxide's split: the same distance under the cap."""
    return max(1, min(ocap, ocap - (kcap - level)))


def choose(fs, caps):
    """Every boss, and about six other fights per split spread from easy to
    hard by the estimate, with an Ace Trainer where the split has one."""
    ocaps = pool.caps()
    chosen = [f for f in fs if f["kind"] == "boss"]
    for split in KAIZO_ORDER:
        rest = [f for f in fs if f["home"] == split and f["kind"] != "boss"]
        if not rest:
            continue
        for f in rest:
            f["estimate"] = estimate(f, ocaps[f["oxide"]], caps[f["home"]])
        rest.sort(key=lambda f: (f["estimate"], f["key"]))
        n = len(rest)
        picks = [rest[min(n - 1, int(q * n))] for q in QUANTILES] + [rest[-1]]
        aces = [f for f in rest if f["kind"] == "Ace"]
        if aces and not any(f["kind"] == "Ace" for f in picks):
            mid = rest[n // 2]["estimate"]
            picks.append(min(aces, key=lambda f: (abs(f["estimate"] - mid), f["key"])))
        seen = set()
        for f in picks:
            if f["key"] not in seen:
                seen.add(f["key"])
                chosen.append(f)
    order = {s: i for i, s in enumerate(KAIZO_ORDER)}
    return sorted(chosen, key=lambda f: (order[f["home"]], f["kind"] != "boss",
                                         f.get("estimate", 0), f["key"]))


def run(workers=16):
    trainers = load_trainers()
    caps = kaizo_caps(trainers)
    ocaps = pool.caps()
    blob = _blob()
    fs = fights(trainers, caps)
    chosen = choose(fs, caps)
    sides, side_notes = {}, {}
    for f in chosen:
        if f["home"] not in sides:
            s, missing, dropped = kaizo_side(f["home"], caps[f["home"]])
            sides[f["home"]] = s
            side_notes[f["home"]] = {"size": len(s), "cap": caps[f["home"]],
                                     "species_missing": missing, "moves_dropped": dropped}
        if f["oxide"] not in sides:
            sides[f["oxide"]] = pool.pool(f["oxide"], blob)
    blob_path = teamscore._blob_path()
    work = []
    for f in chosen:
        kcap, ocap = caps[f["home"]], ocaps[f["oxide"]]
        work.append((f, "kaizo", fight_jobs(f, sides[f["home"]], lambda lv: lv)))
        work.append((f, "oxide", fight_jobs(f, sides[f["oxide"]],
                                            lambda lv, k=kcap, o=ocap: oxide_level(lv, k, o))))
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as ex:
        outs = list(ex.map(lambda w: pressure.run_node(blob_path, w[2][0]), work))
    results = collections.OrderedDict()
    for (f, which, (jobs, ctx)), out in zip(work, outs):
        r = results.setdefault(f["key"], {k: f[k] for k in (
            "key", "label", "names", "ids", "ksplit", "home", "oxide", "kind", "superboss",
            "variants", "battle", "size", "top", "weather", "trick_room", "notes", "from_sheet")})
        r["estimate"] = f.get("estimate")
        r["kaizo_cap"], r["oxide_cap"] = caps[f["home"]], ocaps[f["oxide"]]
        r["vs_" + which] = score(jobs, ctx, out)
        r["left_out"] = {k: v for k, v in ctx["notes"].items() if v and k != "abilities"}
        r["abilities_swapped"] = ctx["notes"]["abilities"]
        r["weather_kept"] = ctx["weather_kept"]
    return {"caps": caps, "oxide_caps": {s: ocaps[s] for s in sorted({f["oxide"] for f in chosen})},
            "sides": {s: side_notes[s] for s in side_notes},
            "oxide_sides": {s: len(sides[s]) for s in sorted({f["oxide"] for f in chosen})},
            "fights_found": len(fs), "counts": substitutions(chosen),
            "fights": list(results.values())}


def substitutions(chosen):
    """How much of the scored teams Oxide's data changes: Pokemon whose
    species Kaizo gives other stats or types, and moves Kaizo plays with
    another type, power or category."""
    blob = _blob()
    kpoks = data.raw("kaizo")["poks"]
    kmoves = ls.kaizo_moves()
    mons = stats = 0
    move_uses = moved = retyped = 0
    changed_species, changed_moves, retyped_moves = set(), set(), set()
    for f in chosen:
        for party in f["parties"]:
            for m in party:
                name = species_name(m["species"])
                if not name:
                    continue
                mons += 1
                k = kpoks.get(name) or kpoks.get(m["species"])
                o = blob["poks"][name]
                if k and (metrics._norm_stats(k.get("bs") or {}) != metrics._norm_stats(o["bs"])
                          or sorted(t for t in k.get("types") or [] if t)
                          != sorted(t for t in o.get("types") or [] if t)):
                    stats += 1
                    changed_species.add(name)
                for mv in m.get("moves") or []:
                    n, d = move_name(mv) if mv else (None, None)
                    if not n or d:
                        continue
                    move_uses += 1
                    km = kmoves.get(ls.resolve(mv, kmoves) or mv)
                    om = blob["moves"][n]
                    if not km:
                        continue
                    # A change of type or category changes what the move is;
                    # a change of power alone is mostly the later games'
                    # numbers, which Oxide follows and Kaizo, a Generation 4
                    # hack, does not. Powers of 1 or less are fixed damage.
                    kp, op = km["power"] or 0, om.get("basePower") or 0
                    if km["type"] != om.get("type") or km["category"] != om.get("category"):
                        retyped += 1
                        retyped_moves.add(n)
                    elif kp > 1 and op > 1 and kp != op:
                        moved += 1
                        changed_moves.add(n)
    return {"pokemon": mons, "pokemon_species_differ": stats, "species_differ": sorted(changed_species),
            "move_uses": move_uses, "move_uses_type_or_category_differ": retyped,
            "moves_type_or_category_differ": sorted(retyped_moves),
            "move_uses_power_differs": moved, "moves_power_differs": sorted(changed_moves)}


# ---- the table --------------------------------------------------------------

def note(r):
    bits = []
    if r["weather"]:
        bits.append(f"weather: {r['weather']}")
    if r["trick_room"]:
        bits.append("Trick Room")
    bits += r["notes"]
    if r["weather_kept"]:
        bits.append("own weather: " + ", ".join(r["weather_kept"]))
    if r["variants"]:
        bits.append("three starter variants, averaged")
    if r["superboss"]:
        bits.append("optional superboss")
    if r["home"] != r["ksplit"]:
        bits.append(f"fought late, from {TITLE[r['ksplit']]}'s split")
    if r["from_sheet"]:
        bits.append("team from the split sheet")
    left = sorted(set(r["left_out"].get("species", [])) | set(r["left_out"].get("moves", [])))
    if left:
        bits.append("left out: " + ", ".join(left))
    return "; ".join(bits)


def table(res):
    lines = ["| Kaizo split (Oxide's) | Trainer (id) | Kind | Battle | Team | Against Kaizo's pool | "
             "Against Oxide's pool | Note |", "|---|---|---|---|---|---|---|---|"]
    for r in res["fights"]:
        ids = ", ".join(str(i) for i in r["ids"] if i is not None) or "none"
        lines.append(
            f"| {TITLE[r['home']]} ({r['oxide']}) | {r['label']} ({ids}) | {r['kind']} | "
            f"{r['battle']} | {r['size']}, top {r['top']} | {r['vs_kaizo']['scale']:.1f} | "
            f"{r['vs_oxide']['scale']:.1f} | {note(r)} |")
    return "\n".join(lines) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("table")
    ap.add_argument("results")
    ap.add_argument("--workers", type=int, default=16)
    a = ap.parse_args(argv)
    res = run(a.workers)
    with open(a.results, "w", encoding="utf-8") as f:
        json.dump(res, f, indent=1, sort_keys=True)
        f.write("\n")
    with open(a.table, "w", encoding="utf-8") as f:
        f.write(table(res))
    return 0


if __name__ == "__main__":
    sys.exit(main())

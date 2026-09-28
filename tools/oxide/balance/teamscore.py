"""A trainer team's place on Ian's fight scale, for the encounter tool's team builder.

    PYTHONPATH=. python3 -m tools.oxide.balance.teamscore leader_roark           # estimate
    PYTHONPATH=. python3 -m tools.oxide.balance.teamscore leader_roark --score   # full score
    PYTHONPATH=. python3 -m tools.oxide.balance.teamscore --fit                  # calibrate

Ian's team builder (2026-09-27) edits a trainer's team, saves it to
res/trainers/data/, and shows two numbers. The encounter tool's server
calls the two entry points here, each with the trainer's file stem and,
for unsaved edits, the trainer's JSON as the builder holds it:

- estimate(stem, data): instant, pure Python, for every edit. Each boss
  Pokemon is set against the player's side for its split with the
  Generation 4 damage formula at the middle roll, without the engine:
  base stats, level, IVs, nature, move power, type, the attack item
  (Choice Band or Specs, Life Orb, a type booster, Expert Belt) and Choice
  Scarf's Speed, and no ability, weather or critical hit. From that come
  the same three readings the plan uses: safe switch-ins (the share of the
  side at most one boss Pokemon knocks out in one hit), threat (the share
  a boss Pokemon knocks out in two hits while moving first) and answers
  (the share that does that to it). Safe switch-ins then go through the
  line fitted to the full scorer (--fit, teamscore.json), and onto Ian's
  fight scale by the plan's line.
- score(stem, data): the full scorer, one Node process, the number the
  plan gives: pressure.score_fight's readings for the trainer's fight, its
  place on Ian's fight scale, and for a story fight the same seat in each
  reference hack, from their stored scores.

The fight is the trainer's story fight when it has one (with this team in
its place; a rival's other starters and a tag partner as stored), else the
ordinary trainer's own fight in the split B6 places it in. In place of a
stem, both entry points take a pair key from pairs.py (two stems joined by
"+"), with unsaved edits as {stem: JSON}: a double against two trainers at
once, scored as one fight against both teams (Ian, 2026-09-28). Its weather is
its map's, and a trainer in the engine's permanent Trick Room table fights
under it. Nothing is stored: a saved team stales its fight's scores in the
usual way, and rescore.py recomputes them.
"""
import argparse
import functools
import json
import math
import os
import re
import sys
import tempfile
import time

from ..encounters import calc_export, calc_trainers
from . import b6, data, pool, pressure, refpressure, splits

HERE = os.path.dirname(os.path.abspath(__file__))
FIT = os.path.join(HERE, "teamscore.json")
BATTLE_LIB = os.path.join(data.ROOT, "src", "battle", "battle_lib.c")

# The natures, as (raised stat, lowered stat); the five neutral ones raise
# and lower the same stat.
NATURES = {
    "Hardy": ("at", "at"), "Lonely": ("at", "df"), "Brave": ("at", "sp"),
    "Adamant": ("at", "sa"), "Naughty": ("at", "sd"), "Bold": ("df", "at"),
    "Docile": ("df", "df"), "Relaxed": ("df", "sp"), "Impish": ("df", "sa"),
    "Lax": ("df", "sd"), "Timid": ("sp", "at"), "Hasty": ("sp", "df"),
    "Serious": ("sp", "sp"), "Jolly": ("sp", "sa"), "Naive": ("sp", "sd"),
    "Modest": ("sa", "at"), "Mild": ("sa", "df"), "Quiet": ("sa", "sp"),
    "Bashful": ("sa", "sa"), "Rash": ("sa", "sd"), "Calm": ("sd", "at"),
    "Gentle": ("sd", "df"), "Sassy": ("sd", "sp"), "Careful": ("sd", "sa"),
    "Quirky": ("sd", "sd")}
# The middle of the sixteen damage rolls (85 to 100 percent), the one
# pressure.py reads.
MID_ROLL = 0.93
TYPE_BOOST = {item: t for t, items in pool.TYPE_ITEMS.items() for item in items}


# ---- inputs, built once per process --------------------------------------------

@functools.lru_cache(maxsize=None)
def _blob():
    return calc_export.build()


@functools.lru_cache(maxsize=None)
def _blob_path():
    """The blob on disk, for the Node runner; kept for the process."""
    fd, path = tempfile.mkstemp(prefix="oxide-teamscore-", suffix=".json")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(_blob(), f)
    return path


@functools.lru_cache(maxsize=None)
def side(split):
    return pool.pool(split, _blob())


@functools.lru_cache(maxsize=None)
def room_trainers(table):
    """Trainer constants in one of the engine's permanent room tables."""
    with open(BATTLE_LIB, encoding="utf-8") as f:
        text = f.read()
    body = text[text.index(table + "[]"):]
    body = body[:body.index("};")]
    return set(re.findall(r"TRAINER_\w+", body)) - {"TRAINER_NONE"}


def party_of(stem, data_json=None):
    """(tr_id, [boss Pokemon]) for a trainer, from its file or `data_json`."""
    if data_json is None:
        with open(os.path.join(data.ROOT, "res", "trainers", "data", f"{stem}.json"),
                  encoding="utf-8") as f:
            data_json = json.load(f)
    sets = calc_trainers.build_trainer(data.ROOT, stem, data_json)
    if not sets:
        raise ValueError(f"{stem}: no party")
    return sets[0][1]["tr_id"], [data._mon(sp, s) for sp, s in sets]


@functools.lru_cache(maxsize=None)
def _pairs():
    from . import pairs
    return {p["key"]: p for p in pairs.pairs()}


def resolve_pair(key, edits=None):
    """The fight a double against two trainers at once is scored in (Ian,
    2026-09-28): one fight against both teams, as the story tag battles
    are, both parties counted as one. `key` is the pair finder's (two
    stems joined by "+"), and `edits` is {stem: the trainer's JSON as the
    builder holds it} for either or both sides. A pair that is a story
    fight (Mars and Jupiter, Flint and Volkner) is scored as that fight.
    The player's partner, where the game gives one, is not on the player's
    side yet, as for the story tag battles; the scorer has no model of two
    Pokemon on the field at once either."""
    entry = _pairs().get(key)
    if entry is None:
        raise ValueError(f"{key}: no such pair (tools/oxide/balance/pairs.py)")
    edits = edits or {}
    ids, teams = [], []
    for st in entry["stems"]:
        tr_id, party = party_of(st, edits.get(st))
        ids.append(tr_id)
        teams.append(party)
    trainers = data.oxide_trainers()
    if entry["story"]:
        fight = next(f for f in data.fights()["fights"] if f["key"] == entry["story"])
        by_id = dict(zip(ids, teams))
        fteams = [by_id.get(t, trainers[t]["party"]) for t in fight["tr_ids"]]
        parties = [[m for team in fteams for m in team]] if fight.get("tag") else fteams
        return {"fight": dict(fight, trainers=None), "parties": parties, "split": fight["split"],
                "weather": pressure.fight_weather(fight["tr_ids"]), "story": fight["key"], "pair": entry}
    split = entry["split"]
    if split not in pool.SPLITS:
        raise ValueError(f"{key}: not placed in a split with a cap")
    constants = {trainers[i]["constant"] for i in ids}
    fight = {"key": f"pair:{key}", "label": key, "split": split, "tr_ids": ids, "tag": True,
             "trick_room": bool(constants & room_trainers("sPermanentTrickRoomTrainers"))}
    return {"fight": fight, "parties": [[m for team in teams for m in team]], "split": split,
            "weather": pressure.fight_weather(ids), "story": None, "pair": entry}


def resolve(stem, data_json=None):
    """The fight the trainer's team is scored in: {fight, parties, split,
    weather, story}. A pair key (two stems joined by "+") names a double
    against two trainers at once, and its `data_json` is {stem: JSON} for
    either side (resolve_pair)."""
    if "+" in stem:
        return resolve_pair(stem, data_json)
    tr_id, party = party_of(stem, data_json)
    trainers = data.oxide_trainers()
    constant = "TRAINER_" + stem.upper()
    for fight in data.fights()["fights"]:
        if tr_id not in fight["tr_ids"]:
            continue
        teams = [party if t == tr_id else trainers[t]["party"] for t in fight["tr_ids"]]
        parties = [[m for team in teams for m in team]] if fight.get("tag") else teams
        return {"fight": dict(fight, trainers=None), "parties": parties, "split": fight["split"],
                "weather": pressure.fight_weather(fight["tr_ids"]), "story": fight["key"]}
    placed = b6.placements().get(tr_id)
    split = placed["split"] if placed else splits.trainer_split(tr_id)
    if split not in pool.SPLITS:
        raise ValueError(f"{stem}: not placed in a split with a cap")
    fight = {"key": f"tr{tr_id}", "label": stem, "split": split, "tr_ids": [tr_id],
             "trick_room": constant in room_trainers("sPermanentTrickRoomTrainers")}
    return {"fight": fight, "parties": [party], "split": split,
            "weather": pressure.fight_weather([tr_id]), "story": None}


# ---- the estimate ------------------------------------------------------------

def _stats(mon):
    """Generation 4 stats from base stats, level, IVs, EVs and nature."""
    rec = _blob()["poks"][mon["species"]]
    bs, level = rec["bs"], mon["level"]
    ivs, evs = mon.get("ivs") or {}, mon.get("evs") or {}
    up, down = NATURES.get(mon.get("nature") or "Hardy", ("at", "at"))
    out = {}
    for k in ("hp", "at", "df", "sa", "sd", "sp"):
        core = (2 * bs[k] + ivs.get(k, 31) + evs.get(k, 0) // 4) * level // 100
        if k == "hp":
            out[k] = core + level + 10
        else:
            mult = 1.1 if k == up and up != down else 0.9 if k == down and up != down else 1.0
            out[k] = math.floor((core + 5) * mult)
    if mon.get("item") == "Choice Scarf":
        out["sp"] = math.floor(out["sp"] * 1.5)
    return out, rec["types"]


def _prepare(mon, moves):
    stats, types = _stats(mon)
    usable = []
    for name in moves:
        rec = _blob()["moves"].get(name)
        if not rec or rec.get("category") not in ("Physical", "Special"):
            continue
        power = rec.get("basePower", rec.get("bp")) or 0
        if power > 1:
            usable.append((name, rec["type"], rec["category"], power, rec.get("priority", 0)))
    return {"mon": mon, "stats": stats, "types": types, "moves": usable}


def _damage(att, dfn, move):
    """One hit at the middle roll, by the Generation 4 formula."""
    _name, mtype, category, power, _pr = move
    chart = _blob()["type_chart"]
    eff = 1.0
    for t in dfn["types"]:
        eff *= chart.get(mtype, {}).get(t, 1.0)
    if eff == 0:
        return 0
    item = att["mon"].get("item")
    a_key, d_key = ("at", "df") if category == "Physical" else ("sa", "sd")
    attack = att["stats"][a_key]
    if (item, category) in (("Choice Band", "Physical"), ("Choice Specs", "Special")):
        attack = math.floor(attack * 1.5)
    if TYPE_BOOST.get(item) == mtype:
        power = math.floor(power * 1.2)
    level = att["mon"]["level"]
    base = (2 * level // 5 + 2) * power * attack // max(1, dfn["stats"][d_key]) // 50 + 2
    dmg = base * (1.5 if mtype in att["types"] else 1.0) * eff * MID_ROLL
    if item == "Life Orb":
        dmg *= 1.3
    if item == "Expert Belt" and eff > 1:
        dmg *= 1.2
    return dmg


def _hits(att, dfn):
    """(fewest hits to knock out, that move's priority), or (None, 0)."""
    best, pr = None, 0
    for move in att["moves"]:
        d = _damage(att, dfn, move)
        if d <= 0:
            continue
        n = math.ceil(dfn["stats"]["hp"] / d)
        if best is None or n < best or (n == best and move[4] > pr):
            best, pr = n, move[4]
    return best, pr


def _first(a, b, pr, trick_room):
    if pr:
        return pr > 0
    return a["stats"]["sp"] < b["stats"]["sp"] if trick_room else a["stats"]["sp"] > b["stats"]["sp"]


def raw_estimate(parties, split, trick_room=False):
    """(safe, threat, answers, per-Pokemon rows) by the estimate's rules."""
    blob = _blob()
    players = [_prepare(p, p["moves"]) for p in side(split)]
    safes, threats, answers, rows = [], [], [], []
    for party in parties:
        hit_count = [0] * len(players)
        for mon in party:
            if mon["species"] not in blob["poks"]:
                continue
            boss = _prepare(mon, pressure.boss_moves(mon, blob))
            t = a = 0
            for i, pl in enumerate(players):
                n, pr = _hits(boss, pl)
                if n == 1:
                    hit_count[i] += 1
                if n is not None and n <= 2 and _first(boss, pl, pr, trick_room):
                    t += 1
                m, pr2 = _hits(pl, boss)
                if m is not None and m <= 2 and _first(pl, boss, pr2, trick_room):
                    a += 1
            k = len(players)
            rows.append({"species": mon["species"], "level": mon["level"],
                         "threat": round(t / k, 3), "answers": round(a / k, 3)})
            threats.append(t / k)
            answers.append(a / k)
        safes.append(1 - sum(c > 1 for c in hit_count) / len(players))
    mean = lambda v: sum(v) / len(v) if v else 0.0
    return mean(safes), mean(threats), mean(answers), rows


def _fit():
    if os.path.exists(FIT):
        with open(FIT, encoding="utf-8") as f:
            return json.load(f)
    return None


def estimate(stem, data_json=None):
    """The instant estimate for a trainer's team (the module's doc)."""
    t0 = time.time()
    fx = resolve(stem, data_json)
    safe, threat, answers, rows = raw_estimate(fx["parties"], fx["split"],
                                               bool(fx["fight"].get("trick_room")))
    fit = _fit()
    calibrated = fit["alpha"] + fit["beta"] * safe if fit else safe
    calibrated = min(1.0, max(0.0, calibrated))
    line = b6.scale_line()
    rating = b6.on_scale(calibrated, line)
    return {"kind": "estimate", "split": fx["split"], "cap": pool.caps()[fx["split"]],
            "story": fx["story"], "weather": fx["weather"],
            "trick_room": bool(fx["fight"].get("trick_room")),
            "safe_raw": round(safe, 3), "safe": round(calibrated, 3), "threat": round(threat, 3),
            "answers": round(answers, 3), "scale": round(rating, 1), "band": b6.band(rating),
            "fit": {k: fit[k] for k in ("r2", "mean_error", "n", "story_mean_error",
                                        "story_max_error", "story_n") if k in fit} if fit else None,
            "mons": rows, "seconds": round(time.time() - t0, 2)}


# ---- the full score ------------------------------------------------------------

def score(stem, data_json=None):
    """The full scorer's reading for a trainer's team (the module's doc)."""
    t0 = time.time()
    fx = resolve(stem, data_json)
    blob, split = _blob(), fx["split"]
    jobs, ctx = pressure.fight_jobs(fx["fight"], blob, side=side(split), parties=fx["parties"],
                                    weather=fx["weather"])
    out = pressure.run_node(_blob_path(), jobs)
    r = pressure.score_jobs(out, ctx, blob, time.time() - t0)
    line = b6.scale_line()
    rating = b6.on_scale(r["safe"], line)
    refs = {}
    if fx["story"]:
        for hack in refpressure.HACKS:
            seat = refpressure.load(hack)["fights"].get(fx["story"])
            if seat:
                refs[hack] = {"safe": seat["safe"],
                              "scale": round(b6.on_scale(seat["safe"], line), 1)}
    return {"kind": "score", "split": split, "cap": r["cap"], "story": fx["story"],
            "weather": r["weather"], "trick_room": r["trick_room"],
            **{k: r[k] for k in ("safe", "threat", "threat_chance", "answers", "answers_bait",
                                 "unseen_count", "unseen")},
            "scale": round(rating, 1), "band": b6.band(rating), "references": refs,
            "mons": [{k: m[k] for k in ("species", "level", "item", "threat_chance",
                                        "answers_bait")} for m in r["mons"]],
            "errors": r["errors"], "seconds": round(time.time() - t0, 2)}


# ---- calibration -------------------------------------------------------------

def fit_estimate():
    """Fits the full scorer's safe switch-ins to the estimate's, over every
    stored story fight and ordinary trainer, and saves the line. The error
    is given twice: over everything, where hundreds of easy trainers near
    full safety pull it down, and over the story fights alone, which is the
    figure to trust for a boss."""
    xs, ys = [], []
    stories = pressure.load()["fights"]
    for fight in data.fights()["fights"]:
        r = stories.get(fight["key"])
        if not r:
            continue
        parties, _ids = pressure.boss_parties(fight)
        xs.append(raw_estimate(parties, fight["split"], bool(fight.get("trick_room")))[0])
        ys.append(r["safe"])
    n_story = len(xs)
    trainers = data.oxide_trainers()
    for tr, r in b6.load().get("trainers", {}).items():
        xs.append(raw_estimate([trainers[int(tr)]["party"]], r["split"])[0])
        ys.append(r["safe"])
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs)
    beta = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sxx if sxx else 1.0
    alpha = my - beta * mx
    pred = [alpha + beta * x for x in xs]
    ss = sum((y - p) ** 2 for y, p in zip(ys, pred))
    st = sum((y - my) ** 2 for y in ys)
    # Errors in points of Ian's scale, with the estimate clamped as estimate() clamps it.
    line = b6.scale_line()
    errs = [abs(line[1] * (y - min(1.0, max(0.0, p)))) for y, p in zip(ys, pred)]
    out = {"alpha": round(alpha, 4), "beta": round(beta, 4), "r2": round(1 - ss / st, 3),
           "mean_error": round(sum(errs) / n, 2), "n": n,
           "story_mean_error": round(sum(errs[:n_story]) / n_story, 2),
           "story_max_error": round(max(errs[:n_story]), 1), "story_n": n_story,
           "_comment": "The estimate's safe switch-ins against the full scorer's; the errors "
                       "are in points of Ian's fight scale, and the story ones are the figure "
                       "to trust for a boss. teamscore.py --fit writes it."}
    with open(FIT, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1, sort_keys=True)
        f.write("\n")
    return out


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("stem", nargs="?")
    ap.add_argument("--score", action="store_true")
    ap.add_argument("--fit", action="store_true")
    args = ap.parse_args(argv)
    if args.fit:
        print(json.dumps(fit_estimate(), indent=1))
        return 0
    if not args.stem:
        ap.error("name a trainer's file stem, a pair key (two stems joined by +), or --fit")
    print(json.dumps((score if args.score else estimate)(args.stem), indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())

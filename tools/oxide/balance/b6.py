"""B6: the audit, aimed at Ian's four goals of 2026-09-26.

    PYTHONPATH=. python3 -m tools.oxide.balance.rescore --kind b6 --kind b6lever --kind b6pair
    PYTHONPATH=. python3 -m tools.oxide.balance.rescore --kind b6 --kind b6lever --kind b6pair --verify
    PYTHONPATH=. python3 -m tools.oxide.balance.b6 --report

Ian's goals (the plan, "The target"): curb the hyper-offense; more fights in
the middle of his fight scale (3 to 6 or 7) and fewer at the bottom (0 to
2); bring in the added Pokemon, moves and abilities; and a pass over
everything so that nothing is comically untuned or unfun. B6 reads Oxide
against each with pressure.py's scores, and judges no matchup differently.
Its scores are stored in b6.json as rescore.py's units, so they are
recomputed only when their inputs change, and verified by a second run.

- The fight scale. Every fight is placed on Ian's fight scale from its safe
  switch-ins, by the line fitted to his ratings of fifteen single battles
  (scale_line). The story fights and Hesperid's come from pressure.json and
  calibrate.json; every ordinary trainer is scored here the same way
  (the "b6" units), in the split the player first meets it in
  (placements). The line cannot read below about 2: a party whose Pokemon
  never double up on a knockout leaves every switch-in safe, and a party of
  one always does. So the bottom band is ordered by threat instead.
- Each double against two trainers at once (the "b6pair" units), scored as
  one fight against both teams (Ian, 2026-09-28). The roll-up counts a pair
  the player cannot split once, in place of its two trainers.
- Each story fight's levers (the "b6lever" units). The fight is scored as
  it stands, then again under each change, rerunning only the matchups a
  change touches. On the boss side: one Pokemon out, one Pokemon's item
  off, one move gone, each alone, which says which single change moves the
  fight most and so what the trainer pass has to work with; and which
  pairs of boss Pokemon knock out the same player Pokemon in one hit,
  which is what pulls safe switch-ins down. On the player's side: a TM or
  HM one split earlier, a damage item one split earlier, the player's
  Choice items gone (Ian, 2026-09-26: nearly gone from the game), the
  split's cap two levels either way, and the fight's map weather gone. A
  species' stats reach a fight only through that species, so each species
  is read by what it answers across the story fights instead.
- New content: how much of the player's side and of the trainers' parties
  is species, moves and abilities vanilla Platinum lacks.
"""
import argparse
import collections
import csv
import functools
import json
import os
import subprocess
import sys
import tempfile

from ..encounters import calc_export, calc_trainers, canon, evolve, pokedex
from . import calibrate, data, metrics, pool, pressure, required

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "b6.json")
SPLITS = pool.SPLITS

# The readings kept for every scored trainer, and the ones a change is judged by.
KEEP = ("threat", "threat_chance", "answers", "answers_duel", "answers_bait", "answers_branch",
        "safe", "cover", "best_one", "broad", "unseen_count", "predictable", "pool", "cap")
LEVER_READ = ("threat_chance", "answers_duel", "answers_bait", "safe", "cover")
# Ian's fight scale, split into his goal's bands: the bottom (0 to 2), the
# middle he wants more of (3 to 6 or 7), and the peak.
BANDS = (("0 to 2", 2.5), ("3 to 7", 7.5), ("8 to 10", float("inf")))
# The player's damage items best_item weighs.
DAMAGE_ITEMS = ({"Choice Band", "Choice Specs", "Life Orb", "Expert Belt", "Muscle Band",
                 "Wise Glasses"} | {i for v in pool.TYPE_ITEMS.values() for i in v})
PLAYER_CHOICE = {"Choice Band", "Choice Specs", "Choice Scarf"}
CAP_STEP = 2
# A lever that moves the fights it touches, on the mean, by this share of
# the side in answers or safe switch-ins is flagged as far; one that moves
# nothing is flagged as none.
FAR = 0.05
# A species that surely answers this share of the boss Pokemon it meets,
# over at least MIN_FIGHTS story fights, is flagged as carrying the game.
# Half is common at the cap with a species' best moves and item (over a
# hundred species reach it), so the flag is for the few far above that.
CARRIES = 0.85
MIN_FIGHTS = 5


def load():
    if os.path.exists(OUT):
        with open(OUT, encoding="utf-8") as f:
            return json.load(f)
    return {"_comment": __doc__.strip().split("\n\n")[0], "trainers": {}, "fights": {}}


def save(results):
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=1, sort_keys=True)
        f.write("\n")


# ---- the fight scale ---------------------------------------------------------

def story_scores():
    """Oxide's story fights and Hesperid's two, keyed as scored."""
    return {**pressure.load()["fights"], **calibrate.load()["fights"]}


def scale_line(fights=None):
    """(a, b) with Ian's fight rating read as a + b * safe switch-ins, the
    least-squares line over his ratings of the fifteen single battles
    (calibrate.IAN_RATINGS less the Spear Pillar tag battle, which the tool
    scores as singles without the player's partner)."""
    fights = story_scores() if fights is None else fights
    keys = [k for k in calibrate.IAN_RATINGS if k != "mars_jupiter"]
    xs = [fights[k]["safe"] for k in keys]
    ys = [calibrate.IAN_RATINGS[k] for k in keys]
    mx, my = sum(xs) / len(xs), sum(ys) / len(ys)
    b = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs)
    return my - b * mx, b


def on_scale(safe, line):
    return line[0] + line[1] * safe


def band(rating):
    return next(name for name, top in BANDS if rating < top)


# ---- every ordinary trainer --------------------------------------------------

@functools.lru_cache(maxsize=None)
def placements():
    """{tr_id: {"split", "how", "late"}} for every first-run ordinary
    trainer (metrics._placed_filler: no story fight, tag partner or
    rematch). The split is the one the player first meets it in on the story
    path (B1e) where the model reaches it, else its map's (B1d); a trainer
    whose ace is over that split's cap moves to the first split whose cap
    covers it ("late"), as B1e found the late visits do. "how" is B1e's
    verdict, required or avoidable, or why the model leaves it out."""
    first = required.first_crossings()
    _rows, left = required.report()
    reason = {c: r for _h, r, ts in left for c in ts}
    never = set(required.never_reached())
    caps = pool.caps()
    ox = data.oxide_trainers()
    out = {}
    for split, ids in metrics._placed_filler().items():
        for tr in ids:
            t = ox[tr]
            if not t["party"]:
                continue
            c = t["constant"]
            if c in first:
                s, _header, how = first[c]
            else:
                s = split
                how = reason.get(c) or ("behind a field move" if c in never else "not on a crossing")
            if s not in caps:
                continue
            ace = max(m["level"] for m in t["party"])
            late = False
            if ace > caps[s]:
                later = [x for x in SPLITS[pool.split_index(s):] if caps[x] >= ace]
                if not later:
                    continue
                s, late = later[0], True
            out[tr] = {"split": s, "how": how, "late": late}
    return out


def trainer_fight(tr):
    """The fight record and party for one ordinary trainer, at its placement."""
    t = data.oxide_trainers()[tr]
    p = placements()[tr]
    return {"key": f"tr{tr}", "label": t["name"], "split": p["split"], "tr_ids": [tr]}, [t["party"]]


def trainer_record(r, tr):
    """What b6.json keeps of an ordinary trainer's scores."""
    t = data.oxide_trainers()[tr]
    return {**{k: r[k] for k in KEEP}, **placements()[tr], "name": t["name"],
            "constant": t["constant"], "battle_type": t["battle_type"],
            "size": len(t["party"]), "ace": max(m["level"] for m in t["party"]),
            "unseen": r["unseen"], "errors": r["errors"],
            "mons": [{k: m[k] for k in ("species", "level", "item", "threat_chance",
                                       "answers_bait")} for m in r["mons"]]}


# ---- doubles against two trainers at once ------------------------------------

@functools.lru_cache(maxsize=None)
def scored_pairs():
    """{key: pair} for every double against two trainers at once scored as a
    fight of its own (Ian, 2026-09-28: one fight against both teams, both
    parties counted as one, as teamscore.resolve_pair builds it): the pair
    finder's two-trainer doubles outside the story fights, in a split with a
    cap. A story pair (Mars and Jupiter) is scored as its story fight. Each
    trainer keeps its own score too, which the team builder shows."""
    from . import pairs
    return {p["key"]: p for p in pairs.pairs()
            if len(p["stems"]) == 2 and not p["story"] and p["split"] in SPLITS}


def pair_record(r, pair):
    """What b6.json keeps of a pair's score. `how` is B1e's verdict as for
    a trainer, required when either trainer is; `kind` is how the pair
    finder found the double, and `each_alone` whether the player can meet
    the two one at a time."""
    ox = data.oxide_trainers()
    by_constant = {t["constant"]: tr for tr, t in ox.items()}
    constants = ["TRAINER_" + st.upper() for st in pair["stems"]]
    verdicts = [(placements().get(by_constant.get(c)) or {}).get("how") for c in constants]
    return {**{k: r[k] for k in KEEP}, "split": pair["split"],
            "how": "required" if "required" in verdicts else next((v for v in verdicts if v), None),
            "kind": pair["how"], "each_alone": bool(pair.get("each_alone")),
            "partner": pair["partner"], "constants": constants,
            "name": " and ".join(ox[by_constant[c]]["name"] for c in constants),
            "size": len(r["mons"]), "ace": max(m["level"] for m in r["mons"]),
            "unseen": r["unseen"], "errors": r["errors"],
            "mons": [{k: m[k] for k in ("species", "level", "item", "threat_chance",
                                       "answers_bait")} for m in r["mons"]]}


def ordinary_fights(results):
    """The ordinary fights the report rolls up: each double against two
    trainers the player cannot split counted once, as its pair, in place of
    its two trainers; every other trainer on its own. A pair whose trainers
    can each be met alone counts as its two singles, the way a player who
    sees it coming would take it."""
    pairs_ = results.get("pairs", {})
    joined = {c for p in pairs_.values() if not p["each_alone"] for c in p["constants"]}
    return [r for r in results.get("trainers", {}).values() if r["constant"] not in joined] \
        + [p for p in pairs_.values() if not p["each_alone"]]


# ---- one boss fight's matchups, kept for its levers --------------------------

def boss_fights():
    """[(fight, parties)] for the story fights and Hesperid's two."""
    out = []
    for fight in data.fights()["fights"]:
        out.append((fight, pressure.boss_parties(fight)[0]))
    by_constant = {t["constant"]: t for t in data.oxide_trainers().values()}
    for constant, split, key, label in calibrate.EXTRA:
        t = by_constant[constant]
        out.append(({"key": key, "label": label, "split": split, "tr_ids": [t["tr_id"]]},
                    [t["party"]]))
    return out


def run_state(jobs, ctx, side, blob_path):
    """Every matchup of one fight's job, run and kept."""
    out = pressure.run_node(blob_path, jobs)
    return {"bosses": ctx["bosses"], "side": side, "side_keys": [f"p{i}" for i in range(len(side))],
            "rows": {(r["a"], r["d"]): r for r in out["results"]}, "info": out["pokemon"],
            "trick_room": ctx["trick_room"], "pokemon": jobs["pokemon"],
            "weights": pool.side_weights(side)}


def score_all(st, rows=None, info=None, bosses=None):
    """score_mons over the fight, with the matchups given or the fight's own."""
    return pressure.score_mons(st["bosses"] if bosses is None else bosses, st["side_keys"],
                               st["rows"] if rows is None else rows,
                               st["info"] if info is None else info, st["trick_room"],
                               st.get("weights"))


def roll(per_mon):
    """The fight's readings from per-Pokemon records, leaving them intact."""
    return pressure.roll_up([dict(m) for m in per_mon])


def _boss_keys(st, key):
    """A boss Pokemon's key and its setup branches' keys."""
    return [k for k in st["info"] if k == key or k.startswith(key + "+")]


def rerun(st, blob_path, pairs, pokemon, merge=False):
    """New rows and info with the given pairs rerun in one Node process:
    each new row replaces the old one, or with merge=True adds its moves to
    it. st is left as it was."""
    if not pairs:
        return st["rows"], st["info"]
    out = pressure.run_node(blob_path, {"pokemon": pokemon, "pairs": pairs})
    rows, info = dict(st["rows"]), dict(st["info"])
    for r in out["results"]:
        k = (r["a"], r["d"])
        if merge and k in rows:
            rows[k] = dict(rows[k], moves={**rows[k]["moves"], **r["moves"]})
        else:
            rows[k] = r
    info.update(out["pokemon"])
    return rows, info


def _player_pairs(st, changed):
    """Pairs and Pokemon for rerunning player Pokemon `changed`
    ({pk: (record, moves to run)}) into every boss key, branches included,
    each in the weather its base pair used."""
    pokemon = dict(st["pokemon"])
    pairs = []
    boss_keys = [k for k in st["info"] if k.startswith("b")]
    for pk, (rec, moves) in changed.items():
        pokemon[pk] = rec
        for bk in boss_keys:
            base = st["rows"].get((pk, bk))
            if base is not None:
                pairs.append([pk, bk, moves, base["weather"]])
    return pairs, pokemon


def _delta(base, r):
    return {k: (round(r[k] - base[k], 3) if r.get(k) is not None and base.get(k) is not None
                else None) for k in LEVER_READ}


# ---- the player's levers -----------------------------------------------------

def _kinds(p, blob):
    """[(type, category, power)] of a player Pokemon's moves, strongest
    first, as pool.pool orders them for best_item."""
    types = blob["poks"][p["species"]]["types"]
    return sorted(((blob["moves"][m]["type"], blob["moves"][m]["category"],
                    blob["moves"][m].get("basePower") or 0) for m in p["moves"]),
                  key=lambda k: -k[2] * (1.5 if k[0] in types else 1))


def tm_levers(blob):
    """{split: [(label, machine, move name)]}: each TM or HM whose first
    split is later than Roark's, listed under the split before, where it
    would land one split earlier."""
    firsts = pool._items_first()
    machines = pokedex.machines(data.ROOT)
    names = pool._move_names()
    out = collections.defaultdict(list)
    for item, split in sorted(firsts.items()):
        m = item.replace("ITEM_", "")
        if not m.startswith(("TM", "HM")) or m not in machines or split not in SPLITS:
            continue
        i = pool.split_index(split)
        name = names.get(machines[m])
        if i == 0 or not name or name not in blob["moves"]:
            continue
        out[SPLITS[i - 1]].append((f"{m} {name} from {split} to {SPLITS[i - 1]}", m, name))
    return out


def item_levers():
    """{split: [(label, item)]}: each damage item whose first split is later
    than Roark's, under the split before."""
    first = {}
    for const, split in sorted(pool._items_first().items()):
        name = calc_trainers._item_name(const)
        if name in DAMAGE_ITEMS and split in SPLITS:
            if name not in first or pool.split_index(split) < pool.split_index(first[name]):
                first[name] = split
    out = collections.defaultdict(list)
    for name, split in sorted(first.items()):
        i = pool.split_index(split)
        if i:
            out[SPLITS[i - 1]].append((f"{name} from {split} to {SPLITS[i - 1]}", name))
    return out


def tm_learners(side, machine, name, blob):
    """{pk: (record, [name])} for the player Pokemon that would know the
    machine's move, as pool.choose_four would pick it, and {pk: moves it
    would drop to make room}."""
    changed, dropped = {}, {}
    for i, p in enumerate(side):
        rec = pokedex.load(data.ROOT, p["constant"])
        if not rec or machine not in rec["by_tm"] or name in p["moves"]:
            continue
        # The side's four stay candidates beside the machine's move, which
        # goes in only if it earns a slot.
        moves = pool.choose_four(p["species"], set(p["moves"]), {name}, blob)
        if name not in moves:
            continue
        changed[f"p{i}"] = (dict(p, moves=moves), [name])
        dropped[f"p{i}"] = set(p["moves"]) - set(moves)
    return changed, dropped


def item_holders(side, items, blob):
    """{pk: (record, moves)} for the player Pokemon whose best item changes
    when the split offers `items`."""
    changed = {}
    for i, p in enumerate(side):
        best = pool.best_item(blob["poks"][p["species"]]["bs"], _kinds(p, blob), items)
        if best != p["item"]:
            changed[f"p{i}"] = (dict(p, item=best), p["moves"])
    return changed


def lever_inputs(fight, side, capped, blob):
    """What one fight's player levers read, beyond its own job file: each
    lever's changed player Pokemon, and the sides at the other caps. The
    fingerprint takes all of it."""
    split = fight["split"]
    items = pool.items_by_split()[split]
    tms = [(label, m, name, tm_learners(side, m, name, blob))
           for label, m, name in tm_levers(blob).get(split, [])]
    its = [(label, item, item_holders(side, items | {item}, blob))
           for label, item in item_levers().get(split, [])]
    return {"tms": tms, "items": its,
            "no_choice": item_holders(side, items - PLAYER_CHOICE, blob), "capped": capped}


def _fp_view(inputs):
    """lever_inputs as plain data for a fingerprint."""
    return {"tms": [(label, m, name, {pk: rec for pk, (rec, _mv) in ch.items()},
                     {pk: sorted(d) for pk, d in dr.items()})
                    for label, m, name, (ch, dr) in inputs["tms"]],
            "items": [(label, item, {pk: rec for pk, (rec, _mv) in ch.items()})
                      for label, item, ch in inputs["items"]],
            "no_choice": {pk: rec for pk, (rec, _mv) in inputs["no_choice"].items()},
            "capped": inputs["capped"]}


# ---- species -----------------------------------------------------------------

def species_rows(st, per_mon):
    """Per player species in one fight: the boss Pokemon it faces and surely
    answers, whether it alone answers one, and in how many variants it is a
    safe switch-in."""
    by_variant = collections.defaultdict(list)
    for b, m in zip(st["bosses"], per_mon):
        by_variant[m["variant"]].append(m)
    out = {}
    for i, p in enumerate(st["side"]):
        pk = f"p{i}"
        a = {"faced": 0, "answered": 0, "alone": 0, "safe_in": 0, "variants": 0}
        for ms in by_variant.values():
            a["variants"] += 1
            if sum(pk in m["_hits"] for m in ms) <= 1:
                a["safe_in"] += 1
            for m in ms:
                a["faced"] += 1
                if pk in m["_sure"]:
                    a["answered"] += 1
                    a["alone"] += len(m["_sure"]) == 1
        out[p["constant"]] = a
    return out


def safe_overlaps(per_mon):
    """Which boss Pokemon double up on a one-hit knockout: [(pair of
    species, the player Pokemon both knock out in one hit)], per variant,
    largest first. These pull safe switch-ins down."""
    pairs = collections.Counter()
    by_variant = collections.defaultdict(list)
    for m in per_mon:
        by_variant[m["variant"]].append(m)
    for ms in by_variant.values():
        for i in range(len(ms)):
            for j in range(i + 1, len(ms)):
                n = len(ms[i]["_hits"] & ms[j]["_hits"])
                if n:
                    pairs[f"{ms[i]['species']} and {ms[j]['species']}"] += n
    return pairs.most_common(6)


# ---- one fight's lever record --------------------------------------------------

def breakdown(st, base_mons, base, blob, blob_path):
    """Each single change to the boss side and its effect: one Pokemon out,
    one Pokemon's item off, one move gone. Only the changed Pokemon's record
    is worked out again. [(label, delta)]."""
    out = []
    per_variant = collections.Counter(b[0] for b in st["bosses"])
    for j, (v, key, mon, w) in enumerate(st["bosses"]):
        who = f"{mon['species']} ({key})"
        if per_variant[v] > 1:
            out.append((f"{who} out", _delta(base, roll(base_mons[:j] + base_mons[j + 1:]))))
        for move in pressure.boss_moves(mon, blob):
            rows = dict(st["rows"])
            for bk in _boss_keys(st, key):
                for pk in st["side_keys"]:
                    row = rows.get((bk, pk))
                    if row and move in row["moves"]:
                        rows[(bk, pk)] = dict(row, moves={m: x for m, x in row["moves"].items()
                                                          if m != move})
            one = score_all(st, rows=rows, bosses=[st["bosses"][j]])[0]
            out.append((f"{who} without {move}",
                        _delta(base, roll(base_mons[:j] + [one] + base_mons[j + 1:]))))
        if mon.get("item"):
            bare = dict(mon, item=None)
            pokemon = dict(st["pokemon"])
            pairs = []
            moves = pressure.boss_moves(bare, blob)
            for bk in _boss_keys(st, key):
                pokemon[bk] = bare if bk == key else dict(bare, boosts=st["pokemon"][bk].get("boosts"))
                for i, p in enumerate(st["side"]):
                    pairs.append([bk, f"p{i}", moves, w])
                    pairs.append([f"p{i}", bk, p["moves"], w])
            rows, info = rerun(st, blob_path, pairs, pokemon)
            one = score_all(st, rows=rows, info=info, bosses=[(v, key, bare, w)])[0]
            out.append((f"{who} without its {mon['item']}",
                        _delta(base, roll(base_mons[:j] + [one] + base_mons[j + 1:]))))
    return out


def lever_record(fight, parties, jobs, ctx, inputs, blob, blob_path):
    """One story fight scored as it stands and under every change."""
    side = inputs["side"]
    st = run_state(jobs, ctx, side, blob_path)
    base_mons = score_all(st)
    base = roll(base_mons)
    levers = {}

    def record(label, kind, per_mon, touched):
        levers[label] = {"kind": kind, "touched": touched,
                         "delta": _delta(base, roll(per_mon)) if per_mon else None}

    for label, _m, _name, (changed, dropped) in inputs["tms"]:
        per_mon = None
        if changed:
            pairs, pokemon = _player_pairs(st, changed)
            rows, info = rerun(st, blob_path, pairs, pokemon, merge=True)
            for pk, gone in dropped.items():
                if gone:
                    for bk in [k for k in st["info"] if k.startswith("b")]:
                        if (pk, bk) in rows:
                            rows[(pk, bk)] = dict(rows[(pk, bk)], moves={
                                m: x for m, x in rows[(pk, bk)]["moves"].items() if m not in gone})
            per_mon = score_all(st, rows=rows, info=info)
        record(label, "TM one split earlier", per_mon, len(changed))
    for label, _item, changed in inputs["items"] + [("the player's Choice items gone", None,
                                                     inputs["no_choice"])]:
        per_mon = None
        if changed:
            pairs, pokemon = _player_pairs(st, changed)
            rows, info = rerun(st, blob_path, pairs, pokemon)
            per_mon = score_all(st, rows=rows, info=info)
        record(label, "item" if _item is None else "item one split earlier", per_mon, len(changed))
    if ctx["weather"]:
        jobs2, ctx2 = pressure.fight_jobs(fight, blob, side=side, parties=parties, weather=None)
        st2 = run_state(jobs2, ctx2, side, blob_path)
        record(f"{fight['label']}'s {ctx['weather']} gone", "weather", score_all(st2), len(side))
    for d, cside in inputs["capped"].items():
        jobs2, ctx2 = pressure.fight_jobs(fight, blob, side=cside, parties=parties)
        st2 = run_state(jobs2, ctx2, cside, blob_path)
        record(f"{fight['split']}'s cap {int(d):+d}", "cap", score_all(st2), len(cside))
    return {"label": fight["label"], "split": fight["split"],
            "base": {k: base[k] for k in LEVER_READ}, "levers": levers,
            "overlaps": safe_overlaps(base_mons),
            "mons": [{"key": b[1], "species": m["species"], "item": m["item"],
                      "threat_chance": m["threat_chance"], "answers_bait": m["answers_bait"],
                      "one_hit": len(m["_hits"]), "sure": len(m["_sure"])}
                     for b, m in zip(st["bosses"], base_mons)],
            "changes": breakdown(st, base_mons, base, blob, blob_path),
            "species": species_rows(st, base_mons)}


# ---- new content (goal 3) ----------------------------------------------------

def _main_list(name):
    out = subprocess.run(["git", "show", f"main:generated/{name}.txt"], cwd=data.ROOT,
                         capture_output=True, text=True, check=True).stdout
    return {line.strip() for line in out.splitlines() if line.strip()}


def new_content(blob):
    """{split: counts of species, moves and abilities vanilla Platinum lacks,
    on the player's side and on the trainers the player meets there}."""
    vanilla_species = {canon.showdown_name(s) for s in _main_list("species")}
    names = pool._move_names()
    vanilla_moves = {names[m] for m in _main_list("moves") if m in names}
    vanilla_abilities = {calc_export.ability_name(a.replace("ABILITY_", ""))
                         for a in _main_list("abilities")}
    ox = data.oxide_trainers()
    mons_by_split = collections.defaultdict(list)
    for fight, parties in boss_fights():
        mons_by_split[fight["split"]] += [m for p in parties for m in p]
    for tr, p in placements().items():
        mons_by_split[p["split"]] += ox[tr]["party"]
    out = {}
    for split in SPLITS:
        side = pool.pool(split, blob)
        mons = mons_by_split[split]
        moves = [mv for m in mons for mv in m.get("moves") or []]
        out[split] = {
            "side": len(side),
            "side_new_species": sum(p["species"] not in vanilla_species for p in side),
            "side_with_new_move": sum(any(mv not in vanilla_moves for mv in p["moves"])
                                      for p in side),
            "foe_mons": len(mons),
            "foe_new_species": sum(m["species"] not in vanilla_species for m in mons),
            "foe_moves": len(moves),
            "foe_new_moves": sum(mv not in vanilla_moves for mv in moves),
            "foe_new_abilities": sum(bool(m.get("ability")) and m["ability"] not in vanilla_abilities
                                     for m in mons)}
    return out


# ---- dead weight (goal 4) ----------------------------------------------------

# Ian's rulings of 2026-09-27. Terrain is not ported: the four Terrain moves
# say "But nothing happened!" and the four Surge abilities and Seed Sower do
# nothing, so the passes take them out of everything the player can get
# (the moves that only read terrain, Ice Spinner, Terrain Pulse and the
# rest, are plain hits and stay). The move-pool survey cuts eight more from
# every learnset, and Splash and Teleport, whose species get a real move;
# Steel Roller stays, its effect to be written.
DEAD_MOVES = {"MOVE_ELECTRIC_TERRAIN", "MOVE_GRASSY_TERRAIN", "MOVE_MISTY_TERRAIN",
              "MOVE_PSYCHIC_TERRAIN", "MOVE_TELEKINESIS", "MOVE_ALLY_SWITCH",
              "MOVE_TOPSY_TURVY", "MOVE_FLOWER_SHIELD", "MOVE_FAIRY_LOCK", "MOVE_AROMATIC_MIST",
              "MOVE_MAGNETIC_FLUX", "MOVE_SPEED_SWAP", "MOVE_SPLASH", "MOVE_TELEPORT"}
DEAD_ABILITIES = {"ELECTRIC_SURGE", "GRASSY_SURGE", "MISTY_SURGE", "PSYCHIC_SURGE", "SEED_SOWER"}


def obtainable():
    """Every species the player can come to own at all: the player's side at
    the League; every scripted source, whatever its level (the side leaves
    out one above its location's cap, such as a roamer); and the drawn
    thirds of the legendary pool (availability-plan.json: not the reserve,
    and not a third whose cavern is kept empty); with what each evolves
    into."""
    out = set(pool.species_by_split()[SPLITS[-1]])
    with open(pool.SOURCES, encoding="utf-8") as f:
        out |= {row["species"] for row in csv.DictReader(f)}
    path = os.path.join(data.ROOT, "docs", "oxide", "encounters", "availability-plan.json")
    with open(path, encoding="utf-8") as f:
        drawn = json.load(f).get("pool", {})
    empty = " ".join(drawn.get("empty") or []).lower()
    for third, species in (drawn.get("thirds") or {}).items():
        if third != "reserve" and third not in empty:
            out |= set(species)
    todo = list(out)
    while todo:
        for _need, target in evolve.evolutions(data.ROOT, todo.pop()):
            if target not in out:
                out.add(target)
                todo.append(target)
    return out


def dead_weight():
    """{"species": [(constant, obtainable, [what is dead])], "tms": [(machine,
    move)], "tutors": [(location, move)]}: everything that carries a move
    or ability Ian's terrain ruling left doing nothing."""
    owned = obtainable()
    machines = pokedex.machines(data.ROOT)
    rows = []
    with open(os.path.join(data.ROOT, "generated", "species.txt"), encoding="utf-8") as f:
        species = [line.strip() for line in f if line.strip().startswith("SPECIES_")]
    for sp in species:
        try:
            rec = pokedex.load(data.ROOT, sp)
        except OSError:
            rec = None
        if not rec:
            continue
        dead = [f"ability {a}" for a in rec["abilities"] if a in DEAD_ABILITIES]
        if rec.get("hidden_ability") in DEAD_ABILITIES:
            dead.append(f"hidden ability {rec['hidden_ability']}")
        dead += [f"level {lvl} {mv}" for lvl, mv in rec["learnset"] if mv in DEAD_MOVES]
        dead += [f"{m} {machines[m]}" for m in rec["by_tm"] if machines.get(m) in DEAD_MOVES]
        dead += [f"tutor {mv}" for mv in rec["by_tutor"] if mv in DEAD_MOVES]
        dead += [f"egg {mv}" for mv in rec["egg_moves"] if mv in DEAD_MOVES]
        if dead:
            rows.append((sp, sp in owned, dead))
    with open(os.path.join(data.ROOT, "res", "pokemon", "move_tutors.json"), encoding="utf-8") as f:
        tutors = [(r["location"], r["move"]) for r in json.load(f) if r["move"] in DEAD_MOVES]
    return {"species": rows, "tms": sorted((m, mv) for m, mv in machines.items() if mv in DEAD_MOVES),
            "tutors": tutors}


# ---- report ------------------------------------------------------------------

def _fmt(v, w=6, d=2):
    return f"{v:>{w}.{d}f}" if isinstance(v, (int, float)) else f"{'':>{w}}"


def lever_table(results):
    """[(size, label, kind, mean answers_bait change, mean safe change,
    fights touched)] over the story fights, largest first."""
    by_label = collections.defaultdict(list)
    kinds = {}
    for rec in results.get("fights", {}).values():
        for label, lv in rec["levers"].items():
            kinds[label] = lv["kind"]
            by_label[label].append(lv["delta"])
    rows = []
    for label, ds in by_label.items():
        ds = [d for d in ds if d]
        if not ds:
            rows.append((0.0, label, kinds[label], None, None, 0))
            continue
        ab = sum(d["answers_bait"] for d in ds) / len(ds)
        sf = sum(d["safe"] for d in ds) / len(ds)
        rows.append((abs(ab) + abs(sf), label, kinds[label], ab, sf, len(ds)))
    return sorted(rows, key=lambda r: -r[0])


def species_table(results):
    """{constant: totals over the story fights}."""
    tot = {}
    for rec in results.get("fights", {}).values():
        for sp, a in rec["species"].items():
            t = tot.setdefault(sp, {"fights": 0, "faced": 0, "answered": 0, "alone": 0,
                                    "safe_in": 0, "variants": 0})
            t["fights"] += 1
            for k in ("faced", "answered", "alone", "safe_in", "variants"):
                t[k] += a[k]
    return tot


# Goal 1's test for a fight whose difficulty is all damage: it threatens at
# least Renegade's gym mean (0.54, "What B3b and B5 found") by chance, shows
# few tactics, and spends most of its turns on moves a player can call.
HYPER = {"threat_chance": 0.55, "tactics": 4, "called": 0.65}
# The fights Ian named as perhaps too hard (2026-09-26).
TOO_HARD = ("flint", "byron")


def hyper_offense(r):
    return (r["threat_chance"] >= HYPER["threat_chance"] and r["unseen_count"] <= HYPER["tactics"]
            and (r.get("predictable") or 0) >= HYPER["called"])


def fully_evolved(constant):
    return not evolve.evolutions(data.ROOT, constant)


def _changes(rec, key, n=3, sign=1):
    """The n boss-side changes that move `key` most in the direction `sign`."""
    rows = [(lab, d) for lab, d in rec["changes"] if d.get(key) is not None]
    return sorted(rows, key=lambda c: -sign * c[1][key])[:n]


def _tr_ids(constants):
    by_constant = {t["constant"]: tr for tr, t in data.oxide_trainers().items()}
    return [by_constant[c] for c in constants if c in by_constant]


def report(results, content=None, out=sys.stdout):
    line = scale_line()
    say = functools.partial(print, file=out)
    say(f"Ian's fight scale from safe switch-ins: {line[0]:.1f} {line[1]:+.1f} x safe "
        f"(the bottom band, 0 to 2, is safe {(2.5 - line[0]) / line[1]:.2f} or more)")
    story = story_scores()
    fights = results.get("fights", {})

    say(f"\nGoal 2, the story fights on the scale ({len(story)}):")
    say(f"{'fight':22}{'split':10}{'safe':>6}{'scale':>7}{'chance':>8}{'bait':>6}"
        f"{'tactics':>9}{'called':>8}  band, marks")
    for k, r in story.items():
        rating = on_scale(r["safe"], line)
        marks = [band(rating)] + (["hyper-offense"] if hyper_offense(r) else []) \
            + (["Ian: perhaps too hard"] if k in TOO_HARD else [])
        say(f"{r['label'][:21]:22}{r['split']:10}{_fmt(r['safe'])}{_fmt(rating, 7, 1)}"
            f"{_fmt(r['threat_chance'], 8)}{_fmt(r['answers_bait'])}{_fmt(r['unseen_count'], 9, 1)}"
            f"{_fmt(r.get('predictable'), 8)}  {', '.join(marks)}")

    trainers = results.get("trainers", {})
    if trainers:
        rolled = ordinary_fights(results)
        pairs_ = results.get("pairs", {})
        together = [p for p in pairs_.values() if not p["each_alone"]]
        say(f"\nGoal 2, ordinary fights by band (all placed / required on the story path); "
            f"{len(together)} doubles against two trainers count once each, in place of their "
            f"{2 * len(together)} trainers, and {len(pairs_) - len(together)} that can be split "
            f"count as singles:")
        say(f"{'split':10}" + "".join(f"{n:>14}" for n, _t in BANDS) + f"{'mean threat':>14}")
        for split in SPLITS:
            rs = [r for r in rolled if r["split"] == split]
            cells = []
            for name, _top in BANDS:
                a = sum(band(on_scale(r["safe"], line)) == name for r in rs)
                q = sum(band(on_scale(r["safe"], line)) == name for r in rs if r["how"] == "required")
                cells.append(f"{a:>8} / {q:<3}")
            mean = sum(r["threat_chance"] for r in rs) / len(rs) if rs else None
            say(f"{split:10}" + "".join(f"{c:>14}" for c in cells) + _fmt(mean, 14))
        req = [r for r in rolled if r["how"] == "required"]
        say(f"Required ordinary fights in the middle band or above: "
            f"{sum(band(on_scale(r['safe'], line)) != BANDS[0][0] for r in req)} of {len(req)}")
        by_size = collections.defaultdict(list)
        for r in rolled:
            by_size[min(r["size"], 4)].append(r)
        say("By party size (4 means four or more, a pair's two parties together): " + "; ".join(
            f"{s}: {len(rs)} fights, {sum(band(on_scale(r['safe'], line)) == BANDS[0][0] for r in rs)}"
            f" at the bottom" for s, rs in sorted(by_size.items())))
        if pairs_:
            say("Doubles against two trainers, each as one fight (scale; each trainer alone):")
            for key, p in sorted(pairs_.items(), key=lambda kv: (pool.split_index(kv[1]["split"]), kv[0])):
                alone = [trainers.get(str(t)) for t in _tr_ids(p["constants"])]
                singles = ", ".join(f"{on_scale(a['safe'], line):.1f}" for a in alone if a)
                say(f"  {p['split']:9}{on_scale(p['safe'], line):5.1f}  ({singles})  {p['name']}"
                    + ("  (can be split)" if p["each_alone"] else ""))

    if fights:
        say("\nGoal 1, hyper-offense: the fights whose difficulty is damage, and the boss-side "
            "changes that cut their threat most (with what each does to safe switch-ins):")
        for k, r in story.items():
            if not hyper_offense(r) or k not in fights:
                continue
            rec = fights[k]
            top = max(rec["mons"], key=lambda m: m["threat_chance"])
            say(f"{r['label']}: threat {r['threat_chance']:.2f}, most from {top['species']} "
                f"({top['threat_chance']:.2f}, {top['item']})")
            for lab, d in _changes(rec, "threat_chance", sign=-1):
                say(f"    {lab}: threat {d['threat_chance']:+.3f}, safe {d['safe']:+.3f}")

        say("\nFlint and Byron, what makes them hard: the pairs that double up on one-hit "
            "knockouts, and the changes that give back the most safe switch-ins:")
        for k in TOO_HARD:
            if k not in fights:
                continue
            rec = fights[k]
            say(f"{rec['label']}: safe {rec['base']['safe']:.2f}; overlaps "
                + ", ".join(f"{p} ({n})" for p, n in rec["overlaps"][:4]))
            say("    fewest answers: " + ", ".join(
                f"{m['species']} {m['answers_bait']:.2f}"
                for m in sorted(rec["mons"], key=lambda m: m["answers_bait"])[:3]))
            for lab, d in _changes(rec, "safe", sign=1):
                say(f"    {lab}: safe {d['safe']:+.3f}, threat {d['threat_chance']:+.3f}")

        rows = lever_table(results)
        say("\nGoal 4, the player's levers, mean change over the story fights each touches "
            "(answers baiting counted, safe switch-ins, fights):")
        for size, label, _kind, ab, sf, n in rows:
            flag = "FAR" if size >= FAR else ("none" if size == 0 else "")
            say(f"  {label[:56]:57}{_fmt(ab, 7, 3)}{_fmt(sf, 7, 3)}{n:>4}  {flag}")

        tot = species_table(results)
        shares = sorted(t["answered"] / t["faced"] for sp, t in tot.items()
                        if t["fights"] >= MIN_FIGHTS and t["faced"] and fully_evolved(sp))
        carriers = sorted((sp for sp, t in tot.items() if t["fights"] >= MIN_FIGHTS
                           and t["answered"] >= CARRIES * t["faced"]),
                          key=lambda sp: -tot[sp]["answered"] / tot[sp]["faced"])
        say(f"\nGoal 4, the share of boss Pokemon a species surely answers, over the story "
            f"fights it meets ({MIN_FIGHTS} or more): a fully evolved species' median is "
            f"{shares[len(shares) // 2]:.2f}; {CARRIES} or more: " + (", ".join(
                f"{canon.showdown_name(sp)} {tot[sp]['answered'] / tot[sp]['faced']:.2f}"
                for sp in carriers) or "none"))
        alone = sorted((sp for sp, t in tot.items() if t["alone"]), key=lambda sp: -tot[sp]["alone"])
        say("Species that are the only sure answer to some boss Pokemon: " + ", ".join(
            f"{canon.showdown_name(sp)} {tot[sp]['alone']}" for sp in alone[:20]))
        idle = sorted(sp for sp, t in tot.items() if t["fights"] >= MIN_FIGHTS
                      and not t["answered"] and fully_evolved(sp))
        say(f"Fully evolved species that surely answer nothing in {MIN_FIGHTS} or more story "
            f"fights ({len(idle)}): " + ", ".join(canon.showdown_name(sp) for sp in idle))

    dead = dead_weight()
    say("\nGoal 4, what Ian's rulings of 2026-09-27 cut (terrain, the move survey): "
        f"{len(dead['tms'])} TMs and {len(dead['tutors'])} tutor moves teach a dead move; "
        f"{sum(o for _s, o, _d in dead['species'])} obtainable species carry one:")
    for sp, owned, things in dead["species"]:
        say(f"  {canon.showdown_name(sp):18}{'obtainable' if owned else 'not obtainable':16}"
            f"{', '.join(things)}")
    if content:
        say("\nGoal 3, what vanilla Platinum lacks, per split: on the player's side, new species "
            "and species with a new move; on the trainers there, new species, moves, abilities:")
        for split, c in content.items():
            say(f"  {split:10} side {c['side_new_species']:>3} / {c['side_with_new_move']:>3} of "
                f"{c['side']:>3}; trainers {c['foe_new_species']:>3} of {c['foe_mons']:>3} Pokemon, "
                f"{c['foe_new_moves']:>3} of {c['foe_moves']:>4} moves, "
                f"{c['foe_new_abilities']:>3} abilities")


# What a species-only draft is filled in with until Ian sets the rest: IVs
# as Oxide's bosses carry them (B2 read a mean of 28.7), a neutral nature,
# no item.
DRAFT_IV = 30


@functools.lru_cache(maxsize=None)
def _constants_by_name():
    return {canon.showdown_name(sp): sp for sp in pokedex.species_list(data.ROOT)}


def _fill(m, level):
    """A draft entry made whole. A bare species name, or an entry missing a
    field, takes the level given, the moves the game itself gives a
    Pokemon of that level (its last four by level-up), its first ability,
    IVs of DRAFT_IV, a neutral nature and no item."""
    m = {"species": m} if isinstance(m, str) else dict(m)
    m.setdefault("level", level)
    rec = pokedex.load(data.ROOT, _constants_by_name()[m["species"]])
    if not m.get("moves"):
        names = pool._move_names()
        m["moves"] = [names.get(mv, mv) for mv in
                      calc_trainers.default_moves(sorted(rec["learnset"], key=lambda e: e[0]),
                                                  m["level"])]
        m["_filled"] = True
    if not m.get("ability"):
        m["ability"] = calc_export.ability_name(rec["abilities"][0])
    m.setdefault("nature", "Hardy")
    m.setdefault("item", None)
    m["ivs"] = {k: (m.get("ivs") or {}).get(k, DRAFT_IV) for k in metrics.STATS}
    m["evs"] = {k: (m.get("evs") or {}).get(k, 0) for k in metrics.STATS}
    return m


def _draft_party(what, level):
    """A drafted team: a trainer constant already in the tree, or a JSON
    file holding a list of party members in the trainer data's shape
    (species, level, item, ability, nature, ivs, evs, moves), any of which
    may be a bare species name or leave fields out (_fill)."""
    if what.startswith("TRAINER_"):
        t = next(t for t in data.oxide_trainers().values() if t["constant"] == what)
        return t["name"], t["party"], [t["tr_id"]]
    with open(what, encoding="utf-8") as f:
        party = [_fill(m, level) for m in json.load(f)]
    return os.path.basename(what), party, []


def score_draft(what, split, weather=None, trick_room=False, level=None, out=sys.stdout):
    """One drafted team (Ian's Frontier Brains, 2026-09-27) scored as a
    story fight in `split`, and placed on his fight scale. A trainer in the
    tree fights in its map's weather, a drafted file in `weather` (Rain,
    Sun, Sand or Hail) or in none; `trick_room` fights it under a permanent
    Trick Room, as Saturn 2's and Thorton's are. A draft's missing levels
    are `level`, else the split's cap. Nothing is stored; a draft that
    becomes a trainer is scored with the rest."""
    say = functools.partial(print, file=out)
    label, party, tr_ids = _draft_party(what, level or pool.caps()[split])
    blob = calc_export.build()
    side = pool.pool(split, blob)
    fight = {"key": "draft", "label": label, "split": split, "tr_ids": tr_ids,
             "trick_room": trick_room}
    with tempfile.TemporaryDirectory(prefix="oxide-b6-draft-") as tmp:
        path = os.path.join(tmp, "blob.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(blob, f)
        jobs, ctx = pressure.fight_jobs(fight, blob, side=side, parties=[party],
                                        weather="map" if tr_ids else weather)
        st = run_state(jobs, ctx, side, path)
    per_mon = score_all(st)
    r = roll(per_mon)
    line = scale_line()
    rating = on_scale(r["safe"], line)
    tactics = pressure.unseen([party])
    say(f"{label} in {split}'s split (cap {pool.caps()[split]}, {len(side)} species on the "
        f"side, weather {ctx['weather'] or 'none'}{', under Trick Room' if trick_room else ''}):")
    filled = [m["species"] for m in party if m.get("_filled")]
    if filled:
        say(f"  provisional: {', '.join(filled)} fight with the game's default moves for "
            f"their level, IVs {DRAFT_IV}, a neutral nature and no item, until Ian sets them")
    say(f"  safe switch-ins {r['safe']:.2f}, so about {rating:.1f} on Ian's fight scale "
        f"({band(rating)}); threat by chance {r['threat_chance']:.2f}, answers baiting counted "
        f"{r['answers_bait']:.2f}, tactics {tactics['unseen_count']}")
    for m in per_mon:
        say(f"  {m['species']:14}{m['level']:>4} {str(m['item']):16} threat {m['threat_chance']:.2f}"
            f", answers {m['answers_bait']:.2f}, knocks out {len(m['_hits'])} in one hit")
    overlaps = safe_overlaps(per_mon)
    if overlaps:
        say("  doubled-up knockouts: " + ", ".join(f"{p} ({n})" for p, n in overlaps))
    for kind, things in tactics["unseen"].items():
        say(f"  {kind}: {', '.join(things)}")


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--draft", help="a trainer constant, or a JSON file of a drafted party")
    ap.add_argument("--split", help="the split a --draft is fought in")
    ap.add_argument("--weather", choices=sorted(pressure.CALC_WEATHER),
                    help="the map weather a drafted file is fought in")
    ap.add_argument("--trick-room", action="store_true",
                    help="fight the draft under a permanent Trick Room")
    ap.add_argument("--level", type=int, help="the level of draft members that give none")
    ap.add_argument("--content", action="store_true",
                    help="also count the new species, moves and abilities (about half a minute)")
    args = ap.parse_args(argv)
    if args.draft:
        if args.split not in SPLITS:
            ap.error(f"--draft needs --split, one of {', '.join(SPLITS)}")
        score_draft(args.draft, args.split, args.weather, args.trick_room, args.level)
        return 0
    report(load(), new_content(calc_export.build()) if args.content else None)
    return 0


if __name__ == "__main__":
    sys.exit(main())

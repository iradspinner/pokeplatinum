"""The TM pass, a draft for Ian (2026-09-28). It writes no game data.

    PYTHONPATH=. python3 -m tools.oxide.balance.tmpass     # docs/oxide/tm-pass.md and its TSVs

Ian's rulings: TMs are single-use again, and each placement gives a set
number of copies (strong TMs one, utility two or three, weak ones given by a
single optional trainer); egg move lists are only the trainers' legal
palette; his first-pass removals leave the TM list (not the level-up
lists); about 100 TMs with the cut line shown; Toxic, Will-O-Wisp and
other reliable status moves may return as single copies, shown as a group;
the six HMs become single-use TMs once field moves work on the badge alone
(element 8), with Surf and Waterfall strong and a buff proposed for each of
the others.

Parts, each in the report:
- reach: the census's (splits.item_reach), which waits for each field
  move and the bike where a map needs them (the census had placed Lake
  Verity's TM38 in Roark's split).
- the set: today's TMs less the removals, and the later games' TM and tutor
  moves that qualify, ranked by how many lines without a niche they give a
  role (niche-check.tsv, the proposal's reading), then by lines reached and
  worth; the cut line at about 100.
- compatibility: who learns each, from today's lists and every later game's
  TM, tutor and level-up lists (hg-engine), less what the rules forbid.
- placement: each TM in one of today's TM places, by the split the reach
  gives it, with copies; a strong TM no earlier than the first split each
  flagged or over-bar line it reaches has a good move of that type (capped
  at Byron's, where the flags stop looking); a weak TM behind one optional
  trainer on the easier side of its split.
- tutors the same way, and the egg lists as the trainers' palette.
"""
import argparse
import collections
import csv
import json
import os
import statistics
import sys

from ..encounters import pokedex
from . import b6, data, learngen as g, laterlearn as ll, learnplan as lp, pool, splits

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(data.ROOT, "docs", "oxide")
TARGET = 100
BELOW_LINE = 15
# Ian's first-pass removals (2026-09-28): TM-only; the level-up lists keep them.
REMOVED = {"Protect", "Double Team", "Rain Dance", "Sandstorm", "Sunny Day", "Hail", "Thief", "Snatch",
           "Skill Swap", "Toxic", "Focus Punch", "Substitute", "Dream Eater", "Swords Dance", "Embargo",
           "Will-O-Wisp", "Flash"}
HM_REMOVED = {"Cut", "Rock Smash"}
# He relaxes these (2026-09-28): reliable status may return as single copies.
RELAXED_NAMED = {"Toxic", "Will-O-Wisp"}
STATUS_EFFECTS = {"STATUS_PARALYZE", "STATUS_SLEEP", "STATUS_BURN", "STATUS_POISON",
                  "STATUS_BADLY_POISON", "STATUS_SLEEP_NEXT_TURN"}
# Attacks whose power the battle works out, read at a stand-in: Return and
# Frustration at full friendship, Hidden Power's fixed 60, a weight or speed
# move at a middling 70. Fling and Natural Gift hang on a held item and
# stay out.
STAND_IN = {"POWER_BASED_ON_FRIENDSHIP": 102, "POWER_BASED_ON_LOW_FRIENDSHIP": 102,
            "RANDOM_POWER_BASED_ON_IVS": 60, "POWER_BASED_ON_LOW_SPEED": 70,
            "INCREASE_POWER_WITH_WEIGHT": 70}
ITEM_BOUND = {"FLING", "NATURAL_GIFT"}
KEEP_UTILITY = {"False Swipe"}      # the nuzlocke's catching tool
OHKO = {"Sheer Cold", "Fissure", "Horn Drill", "Guillotine"}
HAZARDS = {"Stealth Rock", "Spikes", "Toxic Spikes", "Sticky Web"}
PIVOTS = {"U-turn", "Volt Switch", "Flip Turn", "Parting Shot"}


# ---- reach -----------------------------------------------------------------------------

def item_places():
    """[{split, map_split, map, item, how, needs}] for every item ball and
    hidden item, from the census's reach (splits.item_reach): the split the
    way to it first opens, and the move that opened it ("foot" for none,
    "unreached" where nothing does)."""
    return [{"split": split, "map_split": splits.map_split(header)[0], "map": header, "item": item,
             "how": how, "needs": needs, "x": "", "z": ""}
            for split, header, item, how, needs in splits.item_reach()]


# ---- candidates, compatibility and worth ------------------------------------------------

def hg_key(species):
    """hg-engine's key for an Oxide species (learnplan.hg_key)."""
    return lp.hg_key(species)


def later_learns(species):
    """{MOVE_X} the species learns in any later game by TM, tutor or level-up."""
    out = set()
    for gkey, _name in ll.GAMES:
        rec = ll.game(gkey).get(hg_key(species)) or ll.game(gkey).get(species)
        if not rec:
            continue
        for kind in ("MachineMoves", "TutorMoves", "LevelMoves"):
            for e in rec.get(kind) or []:
                out.add(ll.oxide_move(e["Move"] if isinstance(e, dict) else e))
    return out


def later_moves_by(kind):
    """{MOVE_X} any later game gives any species by that kind (MachineMoves, TutorMoves)."""
    out = set()
    for gkey, _name in ll.GAMES:
        for rec in ll.game(gkey).values():
            for e in (rec or {}).get(kind) or []:
                out.add(ll.oxide_move(e["Move"] if isinstance(e, dict) else e))
    return out


def is_attack(c):
    return lp.M()[c]["class"] != "STATUS"


def eff(c):
    """An attack's effective power, a computed one's at its stand-in."""
    m = lp.M()[c]
    return STAND_IN.get(m.get("effect"), lp.effective_power(c))


def qualifies(c):
    """(bool, why not): a move a TM or a tutor may teach."""
    m = lp.M().get(c)
    if not m:
        return False, "not in Oxide"
    nm = lp.name(c)
    if not ll.placeable(c):
        return False, "the engine does not run it in full"
    if c in g.WEATHER_MOVES or c in lp.NEEDS_WEATHER:
        return False, "weather"
    if c in b6.DEAD_MOVES or c in ll._doubles_only():
        return False, "the move pool's cut, or a partner move"
    if nm in OHKO:
        return False, "knocks out in one hit"
    if c in lp.SELF_KO:
        return False, "the user faints, which in a nuzlocke is a death"
    if m.get("effect") in ITEM_BOUND:
        return False, "hangs on a held item"
    if nm in HAZARDS | PIVOTS | KEEP_UTILITY:
        return True, ""
    if is_attack(c):
        return (eff(c) >= 50, "under 50 by effective power")
    return ((lp.rank(c) or 0) >= 3, "a status move rated under B")


def relaxed_group():
    """Toxic, Will-O-Wisp and every status move that inflicts a major status
    reliably (90% or more, or never missing), for Ian to take or leave."""
    out = []
    for c, m in lp.M().items():
        if m["class"] != "STATUS" or not ll.placeable(c):
            continue
        acc = m.get("accuracy") or 0
        if lp.name(c) in RELAXED_NAMED or (m.get("effect") in STATUS_EFFECTS and (acc == 0 or acc >= 90)):
            if lines_reached(c) < RELAXED_MIN_LINES:
                # A TM one line or none can learn is no real option.
                RELAXED_TOO_FEW.append((c, lines_reached(c)))
                continue
            out.append(c)
    return sorted(out, key=lp.name)


RELAXED_MIN_LINES = 2
RELAXED_TOO_FEW = []


def tier(c):
    nm = lp.name(c)
    if nm in KEEP_UTILITY:
        return "utility"
    if is_attack(c):
        e = eff(c)
        if e >= 90:
            return "strong"
        return "utility" if e >= 65 or nm in PIVOTS else "weak"
    r = lp.rank(c) or 0
    if r >= 5:
        return "strong"
    return "utility" if r >= 4 or nm in HAZARDS else "weak"


def three_copy_candidate(c):
    return lp.name(c) in HAZARDS | PIVOTS


_COMPAT = {}


def compat_table():
    """{species: {MOVE_X}} a species may learn from a machine or a tutor: its
    TM and tutor lists today, and every later game's TM, tutor and level-up
    lists for it."""
    if not _COMPAT:
        machines = pokedex.machines(data.ROOT)
        for s in pokedex.species_list(data.ROOT):
            rec = pokedex.load(data.ROOT, s) or {}
            have = {machines[m] for m in rec.get("by_tm") or [] if m in machines}
            have |= set(rec.get("by_tutor") or [])
            have |= later_learns(s)
            _COMPAT[s] = have
    return _COMPAT


def compatible(c):
    return sorted(s for s, moves in compat_table().items() if c in moves)


_NICHELESS = set()


def nicheless():
    """Stages the niche check finds with no niche on the proposal, held past
    their first split."""
    if not _NICHELESS:
        path = os.path.join(OUT, "niche-check.tsv")
        for r in csv.DictReader(open(path, encoding="utf-8"), delimiter="\t"):
            if r["reading"] == "proposal" and not r["niche"] and not r["passing"]:
                _NICHELESS.add(r["species"])
    return _NICHELESS


def lines_reached(c):
    ob = g._obtainable()
    return len({lp.line_of(s)[0] for s in compatible(c) if s in ob})


def niche_lift(c):
    """How many lines with a stage the niche check finds no niche for would
    learn it as a role: an attack of 65 or more, or a status move rated A or
    better."""
    if not ((is_attack(c) and eff(c) >= 65) or (lp.rank(c) or 0) >= 4):
        return 0
    return len({lp.line_of(s)[0] for s in compatible(c) if s in nicheless()})


def worth(c):
    return eff(c) if is_attack(c) else (lp.rank(c) or 0) * 25


def near_duplicate(c, chosen):
    """Whether a move already in the set does the same job: the same type and
    category, within 15 by effective power, learnt by at least seven in ten
    of the lines that would learn this one."""
    if not is_attack(c):
        return None
    mine = {lp.line_of(s)[0] for s in compatible(c) if s in g._obtainable()}
    for d in chosen:
        if d == c or not is_attack(d) or lp.M()[d]["type"] != lp.M()[c]["type"] \
                or lp.M()[d]["class"] != lp.M()[c]["class"] or abs(eff(d) - eff(c)) > 15:
            continue
        theirs = {lp.line_of(s)[0] for s in compatible(d) if s in g._obtainable()}
        if mine and len(mine & theirs) >= 0.7 * len(mine):
            return d
    return None


def _by_name():
    return {lp.name(c): c for c in lp.M()}


def build_set():
    """(kept, dropped, chosen, below the line, relaxed group, HMs)."""
    machines = pokedex.machines(data.ROOT)
    current = {k: c for k, c in machines.items() if k.startswith("TM")}
    hms = {k: c for k, c in machines.items() if k.startswith("HM")}
    kept, dropped = [], []
    for k, c in sorted(current.items()):
        if lp.name(c) in REMOVED:
            dropped.append((k, c, "Ian's removal"))
            continue
        ok, why = qualifies(c)
        if not ok:
            dropped.append((k, c, why))
            continue
        kept.append((k, c))
    relaxed = relaxed_group()
    have = {c for _k, c in kept} | set(hms.values()) | set(relaxed)
    names = _by_name()
    later_tm = [names[r["move"]] for r in csv.DictReader(
        open(os.path.join(OUT, "later-moves-tm.tsv"), encoding="utf-8"), delimiter="\t") if r["move"] in names]
    cands = (later_moves_by("MachineMoves") | later_moves_by("TutorMoves") | set(later_tm)) - have
    ranked = []
    for c in sorted(cands):
        ok, _why = qualifies(c)
        if not ok or lp.name(c) in REMOVED or lp.name(c) in HM_REMOVED:
            continue
        reached = lines_reached(c)
        if reached < 3:
            continue
        ranked.append((c, niche_lift(c), reached, worth(c)))
    ranked.sort(key=lambda x: (-x[1], -x[2], -x[3], lp.name(x[0])))
    room = max(0, TARGET - len(kept))
    chosen, below, dupes = [], [], []
    in_set = [c for _k, c in kept]
    for x in ranked:
        d = near_duplicate(x[0], in_set)
        if d:
            dupes.append((x[0], d))
            continue
        (chosen if len(chosen) < room else below).append(x)
        if len(chosen) <= room:
            in_set.append(x[0])
    NEAR_DUPES[:] = dupes
    return kept, dropped, chosen, below[:BELOW_LINE], relaxed, hms


NEAR_DUPES = []


# ---- placement ---------------------------------------------------------------------------

def allowed_split(c, proposal):
    """The earliest split a strong TM may be placed in: no earlier than the
    split in which each flagged or over-bar line it reaches has a good move
    of that type on the proposal, capped at Byron's, where the flags stop
    looking; for a strong status move, Byron's when it reaches such a line.
    Also the lines it reaches early (none of that type by then)."""
    early, splits_ = [], []
    ob = g._obtainable()
    kind, _p = lp.strength(c)
    for s in compatible(c):
        if s not in ob or not lp.strong_stage(s):
            continue
        if kind == "damage":
            if not lp.good_attack(c, lp._types(s)):
                continue
            first = lp.first_good_of_type(s, lp.M()[c]["type"], proposal.get(s) or lp._now(s))
            split = lp._split_of(first) if first else None
        else:
            split = None
        if split is None or split not in pool.SPLITS or pool.split_index(split) > pool.split_index("Byron"):
            early.append(s)
            split = "Byron"
        splits_.append(split)
    return (max(splits_, key=pool.split_index) if splits_ else pool.SPLITS[0]), sorted(early)


def optional_trainers():
    """{split: [(scale, tr_id, stem)]} of the optional trainers on the easier
    side of their split (at or under its median on Ian's fight scale)."""
    stored = json.load(open(os.path.join(HERE, "b6.json"), encoding="utf-8"))["trainers"]
    line = b6.scale_line()
    ox = data.oxide_trainers()
    rows = collections.defaultdict(list)
    for tr, p in b6.placements().items():
        t = stored.get(str(tr))
        if p["how"] != "avoidable" or not t:
            continue
        rows[p["split"]].append((round(b6.on_scale(t["safe"], line), 1), tr,
                                 ox[tr]["constant"].removeprefix("TRAINER_").lower()))
    out = {}
    for split, rs in rows.items():
        mid = statistics.median(r[0] for r in rs)
        out[split] = sorted(r for r in rs if r[0] <= mid)
    return out


def natural_split(c):
    """For a weak TM with no place today: the median first split of the
    obtainable stages that learn it."""
    firsts = sorted(pool.split_index(s) for s in (lp._owned_from(x) for x in compatible(c)
                                                    if x in g._obtainable()) if s)
    return pool.SPLITS[firsts[len(firsts) // 2]] if firsts else pool.SPLITS[1]


def place(kept, chosen, relaxed, places, proposal):
    """[row] placing every TM of the set: its tier, copies, where, from which
    split, and the lines a strong one reaches early."""
    tm_slots = [p for p in places if (p["item"] or "").startswith(("ITEM_TM", "ITEM_HM"))]
    tm_slots += [{"split": s, "map_split": s, "map": m, "item": it, "how": "gift", "needs": "foot",
                  "x": "", "z": ""} for s, m, it in splits.gifts() if (it or "").startswith("ITEM_TM")]
    machines = pokedex.machines(data.ROOT)
    move_of = {"ITEM_" + k: c for k, c in machines.items()}
    by_move = collections.defaultdict(list)
    for sl in tm_slots:
        by_move[move_of.get(sl["item"])].append(sl)
    set_moves = list(dict.fromkeys([c for _k, c in kept] + [x[0] for x in chosen] + list(relaxed)))
    free = [sl for c, sls in by_move.items() if c not in set_moves for sl in sls]
    free.sort(key=lambda sl: (pool.split_index(sl["split"]) if sl["split"] in pool.SPLITS else 99, sl["map"]))
    rows = []
    trainers = optional_trainers()
    used = set()
    for c in set_moves:
        t = "strong" if c in relaxed else tier(c)
        allowed, early = allowed_split(c, proposal) if t == "strong" else (pool.SPLITS[0], [])
        own = sorted(by_move.get(c, []), key=lambda sl: pool.split_index(sl["split"])
                     if sl["split"] in pool.SPLITS else 99)
        row = {"move": c, "tier": t, "copies": {"strong": 1, "utility": 2, "weak": 1}[t],
               "three": t == "utility" and three_copy_candidate(c), "allowed": allowed, "early": early,
               "relaxed": c in relaxed, "place": None, "split": None, "note": ""}
        if t == "weak":
            target = own[0]["split"] if own and own[0]["split"] in pool.SPLITS else natural_split(c)
            order = sorted(pool.SPLITS, key=lambda s: (abs(pool.split_index(s) - pool.split_index(target)),
                                                      pool.split_index(s)))
            pick = next(((s, tr) for s in order for tr in trainers.get(s, []) if tr[1] not in used), None)
            if pick:
                used.add(pick[1][1])
                row.update(place=f"defeating {pick[1][2]} (scale {pick[1][0]})", split=pick[0])
            else:
                row["note"] = "no optional trainer fits"
            rows.append(row)
            continue
        ok_own = [sl for sl in own if sl["split"] in pool.SPLITS
                  and pool.split_index(sl["split"]) >= pool.split_index(allowed)]
        if ok_own:
            sl = ok_own[0]
            row.update(place=f"{sl['map']} ({sl['how']})", split=sl["split"])
        else:
            if own:
                row["note"] = f"its place today, in {own[0]['split']}, is before {allowed}"
            sl = next((x for x in free if x["split"] in pool.SPLITS
                       and pool.split_index(x["split"]) >= pool.split_index(allowed)), None)
            if sl:
                free.remove(sl)
                row.update(place=f"{sl['map']} ({sl['how']}, today {sl['item']})", split=sl["split"])
            else:
                row["note"] = (row["note"] + "; " if row["note"] else "") + "no free place from that split"
        rows.append(row)
    return rows


# ---- the HMs, tutors and egg lists ---------------------------------------------------------

def hm_rows(hms):
    """The six HMs as future single-use TMs (element 8), with a buff proposed
    for the poor ones and Rock Smash as an early TM."""
    out = []
    for k, c in sorted(hms.items()):
        m = lp.M()[c]
        nm = lp.name(c)
        now = f"{m.get('power') or '-'} power, {m.get('accuracy') or 'never misses'} accuracy, {m.get('effect')}"
        if nm in HM_REMOVED:
            continue
        if nm in ("Surf", "Waterfall"):
            out.append((k, nm, "strong", now, "as it is (Ian: strong)"))
        elif nm == "Fly":
            out.append((k, nm, "utility", now, "accuracy 95 to 100: a two-turn move that can still miss "
                                              "is poor; this makes it the reliable Flying hit"))
        elif nm == "Strength":
            out.append((k, nm, "utility", now, "power 80 to 90: a clean Normal hit between Body Slam "
                                              "and Double-Edge, with no recoil"))
        elif nm == "Defog":
            out.append((k, nm, "utility", now, "clear hazards on both sides as the later games do, if "
                                              "Oxide's does not yet; it then answers the trainers' "
                                              "hazards, a niche nothing else fills"))
        elif nm == "Rock Climb":
            out.append((k, nm, "utility", now, "accuracy 85 to 95: its 20% confusion makes it a Normal "
                                              "option worth a slot once it seldom misses"))
        else:
            out.append((k, nm, tier(c), now, "as it is"))
    smash = _by_name().get("Rock Smash")
    if smash:
        m = lp.M()[smash]
        out.append(("HM06", "Rock Smash", "weak", f"{m.get('power')} power, {m.get('accuracy')} accuracy, "
                    f"{m.get('effect')}", "an early TM in Roark's split as it is: Fighting coverage "
                                          "against Roark's Rock types, with its Defense drop"))
    return out


def tutor_rows(set_moves):
    """(kept, dropped, additions ranked): today's tutors less what does not
    qualify, and the later games' tutor moves not in the TM set."""
    cur = json.load(open(os.path.join(data.ROOT, "res", "pokemon", "move_tutors.json"), encoding="utf-8"))
    where = pool._tutor_splits()
    kept, dropped = [], []
    for t in cur:
        c = t["move"]
        ok, why = qualifies(c)
        if lp.name(c) in REMOVED:
            ok, why = False, "Ian's removal"
        (kept if ok else dropped).append((c, t["location"], where.get(c), t, why))
    have = {c for c, *_ in kept} | set(set_moves)
    ranked = []
    for c in sorted(later_moves_by("TutorMoves") - have):
        ok, _why = qualifies(c)
        if not ok or lp.name(c) in REMOVED:
            continue
        reached = lines_reached(c)
        if reached >= 3:
            ranked.append((c, niche_lift(c), reached, worth(c)))
    ranked.sort(key=lambda x: (-x[1], -x[2], -x[3], lp.name(x[0])))
    return kept, dropped, ranked


def egg_lists():
    """{species: [MOVE_X]}: the latest later game's egg moves, less what the
    engine does not run or the weather ruling forbids; the trainers' legal
    palette only, never the player's."""
    out = {}
    for s in pokedex.species_list(data.ROOT):
        for gkey, _name in reversed(ll.GAMES):
            rec = ll.game(gkey).get(hg_key(s)) or ll.game(gkey).get(s)
            if rec and rec.get("EggMoves"):
                moves = [ll.oxide_move(e["Move"] if isinstance(e, dict) else e) for e in rec["EggMoves"]]
                out[s] = [c for c in moves if c in lp.M() and ll.placeable(c) and c not in g.WEATHER_MOVES]
                break
    return out


# ---- the report ---------------------------------------------------------------------------

def run(log=sys.stdout):
    proposal = ll.proposal_lists()
    lp.PROPOSED.clear()
    lp.PROPOSED.update(proposal)
    places = item_places()
    print(f"  reach: {len(places)} items read", file=log, flush=True)
    kept, dropped, chosen, below, relaxed, hms = build_set()
    print(f"  set: {len(kept)} kept, {len(chosen)} new, {len(relaxed)} in the reliable-status group", file=log,
          flush=True)
    rows = place(kept, chosen, relaxed, places, proposal)
    tut_kept, tut_dropped, tut_ranked = tutor_rows([r["move"] for r in rows])
    eggs = egg_lists()
    return {"places": places, "kept": kept, "dropped": dropped, "chosen": chosen, "below": below,
            "relaxed": relaxed, "hms": hm_rows(hms), "rows": rows, "tut_kept": tut_kept,
            "tut_dropped": tut_dropped, "tut_ranked": tut_ranked, "eggs": eggs}


def _sp(s):
    return lp._sp(s)


def write(res, log=sys.stdout):
    nm = lp.name
    with open(os.path.join(OUT, "tm-pass-set.tsv"), "w", encoding="utf-8") as f:
        f.write("move\tstatus\ttier\tcopies\tthree_copy_candidate\tlines\tniche_lift\tworth\tsplit\tplace\t"
                "no_earlier_than\treaches_early\tnote\n")
        by_move = {r["move"]: r for r in res["rows"]}
        status = {c: "kept" for _k, c in res["kept"]}
        status.update({x[0]: "new" for x in res["chosen"]})
        status.update({c: "reliable-status group" for c in res["relaxed"]})
        for c, r in sorted(by_move.items(), key=lambda kv: nm(kv[0])):
            f.write(f"{nm(c)}\t{status.get(c)}\t{r['tier']}\t{r['copies']}\t{'yes' if r['three'] else ''}\t"
                    f"{lines_reached(c)}\t{niche_lift(c)}\t{worth(c):.0f}\t{r['split'] or ''}\t{r['place'] or ''}\t"
                    f"{r['allowed'] if r['tier'] == 'strong' else ''}\t{', '.join(_sp(s) for s in r['early'])}\t"
                    f"{r['note']}\n")
        for c, lift, reached, w in res["below"]:
            f.write(f"{nm(c)}\tbelow the line\t{tier(c)}\t\t\t{reached}\t{lift}\t{w:.0f}\t\t\t\t\t\n")
    with open(os.path.join(OUT, "tm-pass-compat.tsv"), "w", encoding="utf-8") as f:
        f.write("move\tspecies\n")
        for r in res["rows"]:
            f.write(f"{nm(r['move'])}\t{' '.join(s[8:].lower() for s in compatible(r['move']))}\n")
    with open(os.path.join(OUT, "tm-pass-reach.tsv"), "w", encoding="utf-8") as f:
        f.write("map\titem\thow\tx\tz\tmap_split\tneeds\tsplit\n")
        for p in res["places"]:
            if p["needs"] != "foot":
                f.write(f"{p['map']}\t{p['item']}\t{p['how']}\t{p['x']}\t{p['z']}\t{p['map_split']}\t"
                        f"{p['needs']}\t{p['split']}\n")
    with open(os.path.join(OUT, "tm-pass-eggs.tsv"), "w", encoding="utf-8") as f:
        f.write("species\tegg_moves\n")
        for s, moves in sorted(res["eggs"].items()):
            f.write(f"{s}\t{', '.join(nm(c) for c in moves)}\n")
    with open(os.path.join(OUT, "tm-pass.md"), "w", encoding="utf-8") as out:
        _write_md(out, res)
    print("wrote docs/oxide/tm-pass.md and its TSVs", file=log)


def _write_md(out, res):
    p = lambda *a: print(*a, file=out)
    nm = lp.name
    rows = res["rows"]
    p("# The TM pass, a draft\n")
    p("Written by `tmpass.py` for Ian's rulings of 2026-09-28, rerun on learnset v3 on 2026-09-30. "
      "It writes no game data. "
      "TMs are single-use again and each placement gives a set number of copies: strong TMs one, "
      "utility two (three where Ian picks), weak ones given by a single optional trainer. Egg lists "
      "are only the trainers' palette. The TSVs beside this file hold the detail: the set "
      "(`tm-pass-set.tsv`), who learns each (`tm-pass-compat.tsv`), the items the reach fix moves "
      "(`tm-pass-reach.tsv`) and the egg lists (`tm-pass-eggs.tsv`).\n")
    moved = [x for x in res["places"] if x["needs"] != "foot"]
    by_need = collections.Counter(x["needs"] for x in moved)
    p("## Reach\n")
    p(f"The census reaches {len(res['places']) - len(moved)} item balls and hidden items on foot; "
      f"{len(moved)} wait for a field move or the bike and count from the split it first works in ("
      + ", ".join(f"{n} {k}" for k, n in by_need.most_common()) + "), listed in the TSV. "
      "The TMs among them:\n")
    tms = [x for x in moved if (x["item"] or "").startswith(("ITEM_TM", "ITEM_HM"))]
    p("| Map | Item | Needs | Split then | Split now |\n|---|---|---|---|---|")
    for x in tms:
        p(f"| {x['map'].removeprefix('MAP_HEADER_')} | {x['item'].removeprefix('ITEM_')} | {x['needs']} | "
          f"{x['map_split']} | {x['split']} |")
    kept, chosen = res["kept"], res["chosen"]
    p("\n## The set\n")
    in_group = [c for _k, c in kept if c in res["relaxed"]]
    p(f"{len(kept)} of today's 92 TMs stay"
      + (f" ({', '.join(nm(c) for c in in_group)} among them, in the reliable-status group)" if in_group else "")
      + f"; {len(res['dropped'])} go (Ian's removals, and cuts proposed for Ian where a move no "
      f"longer qualifies). {len(chosen)} new ones come from the later games' TM and tutor moves, ranked by "
      f"how many lines with a stage that has no niche they would give a role, then by lines reached, "
      f"then by worth. The line falls at {len(kept) + len(chosen)} TMs; the {len(res['below'])} after it "
      f"are shown so Ian can move it. The six HMs are below, and the reliable-status group apart.\n")
    # Ian's own removals say so; every other cut is a proposal for him.
    ian = "Ian's removal"
    leave = lambda why: why if why == ian else "proposed for Ian: " + why
    p("Leaving: " + ", ".join(f"{k} {nm(c)} ({leave(why)})" for k, c, why in res["dropped"]) + ".\n")
    p("| New TM | Tier | Lines | Lines without a niche it helps | Worth |\n|---|---|---|---|---|")
    for c, lift, reached, w in chosen:
        p(f"| {nm(c)} | {tier(c)} | {reached} | {lift} | {w:.0f} |")
    p("\nBelow the line: " + ", ".join(f"{nm(c)} ({reached} lines, {lift})" for c, lift, reached, _w
                                       in res["below"]) + ".")
    p("\n## Strong TMs and the lines they reach early\n")
    p("A strong TM goes no earlier than the split in which each flagged or over-bar line it reaches "
      "has a good move of that type, capped at Byron's, where the flags stop looking. Lines it still "
      "reaches with no move of that type by then:\n")
    p("| TM | Placed | No earlier than | Reaches early |\n|---|---|---|---|")
    for r in sorted((r for r in rows if r["tier"] == "strong" and not r["relaxed"]), key=lambda r: nm(r["move"])):
        p(f"| {nm(r['move'])} | {r['split'] or '-'} | {r['allowed']} | "
          f"{', '.join(_sp(s) for s in r['early'][:8]) + (' and more' if len(r['early']) > 8 else '') or 'none'} |")
    p("\n## The reliable-status group, for Ian to take or leave\n")
    p("Toxic, Will-O-Wisp and each status move that inflicts a major status at 90% or more, or never "
      "misses, as strong-tier TMs of one copy each:\n")
    p("| TM | Lines | Placed |\n|---|---|---|")
    for r in (r for r in rows if r["relaxed"]):
        p(f"| {nm(r['move'])} | {lines_reached(r['move'])} | {r['split'] or '-'}: {r['place'] or r['note']} |")
    if RELAXED_TOO_FEW:
        p("\nLeft out of the group as no real option, since at most one line could learn it: "
          + ", ".join(f"{nm(c)} ({n} line{'s' if n != 1 else ''})" for c, n in sorted(RELAXED_TOO_FEW, key=lambda x: nm(x[0])))
          + ".")
    p("\n## Placement and copies\n")
    counts = collections.Counter(r["tier"] for r in rows)
    p(f"Strong {counts['strong']}, utility {counts['utility']}, weak {counts['weak']}. Candidates for a "
      f"third copy are marked; Ian picks. Weak TMs go behind an optional trainer on the easier side of "
      f"its split, named below; marts keep selling what they sell now.\n")
    p("| TM | Tier | Copies | Split | Where |\n|---|---|---|---|---|")
    for r in sorted(rows, key=lambda r: (pool.split_index(r["split"]) if r["split"] in pool.SPLITS else 99,
                                         nm(r["move"]))):
        copies = f"{r['copies']}{' (3?)' if r['three'] else ''}"
        p(f"| {nm(r['move'])} | {r['tier']} | {copies} | {r['split'] or '-'} | "
          f"{r['place'] or r['note']}{'; ' + r['note'] if r['place'] and r['note'] else ''} |")
    p("\n## The HMs\n")
    p("The six HMs become single-use TMs once field moves work on the badge alone (element 8), tiered "
      "like any TM. Ian's view is that apart from Surf and Waterfall they are poor moves, so each other "
      "one gets a proposed buff, which would change trainers' copies of the move too; Rock Smash, no "
      "longer an HM, is proposed as an early TM:\n")
    p("| HM | Move | Tier | Today | Proposal |\n|---|---|---|---|---|")
    for k, move, t, now, prop in res["hms"]:
        p(f"| {k} | {move} | {t} | {now} | {prop} |")
    p("\n## Tutors\n")
    p(f"{len(res['tut_kept'])} of today's {len(res['tut_kept']) + len(res['tut_dropped'])} tutor moves "
      f"stay; leaving: " + ", ".join(f"{nm(c)} ({why})" for c, _l, _s, _t, why in res["tut_dropped"])
      + ". The later games' tutor moves not in the TM set, ranked the same way (the first 15):\n")
    p("| Move | Tier | Lines | Lines without a niche it helps |\n|---|---|---|---|")
    for c, lift, reached, _w in res["tut_ranked"][:15]:
        p(f"| {nm(c)} | {tier(c)} | {reached} | {lift} |")
    from . import stones
    p("\n## Stone contests\n")
    p("Ian's scarce-stone ruling accepts two lines wanting one stone. The branches he has ruled in "
      "(2026-09-28: Vulpix to Alolan Ninetales by an Ice Stone, Koffing and Ponyta to their Galarian "
      "forms by a Moon Stone) add claimants, counted here with the census's places for each stone, "
      "less the two bulk sets Ian removed (Route 207's nine, Galactic HQ B2F's):\n")
    claim, src = stones.claimants(), stones.sources()
    for stone in ("ITEM_MOON_STONE", "ITEM_ICE_STONE"):
        places = [x for x in src.get(stone, []) if not any(x[1].startswith(m) and x[2] == h
                                                            for m, h in stones.REMOVED)]
        who = sorted(claim.get(stone, []), key=lambda x: (pool.split_index(x[2]) if x[2] else 99, x[0]))
        p(f"**{stone.removeprefix('ITEM_').replace('_', ' ').title()}**: {len(places)} places "
          f"({', '.join(f'{sp} {w} ({h})' for sp, w, h in places) or 'none yet; the item pass places it'}); "
          f"{len(who)} claimants: " + ", ".join(f"{_sp(a)} to {_sp(b)} ({sp or 'not owned on the story path'})"
                                                for a, b, sp in who) + ".\n")
    p("The Ice Stone (item 492, priced 2100 like the other stones) is placed nowhere yet, and its "
      "place is the census's call: one copy on Route 217, the snow route in Candice's split, so a "
      "Vulpix owner meets it where the Ice types live, well after Alolan Ninetales can be caught wild "
      "in Gardenia's split; the item pass picks the exact spot.\n")
    p(f"\n## Egg lists, the trainers' palette\n")
    p(f"{len(res['eggs'])} species get the latest later game's egg moves, less what the engine does not "
      f"run and the weather ruling forbids (`tm-pass-eggs.tsv`). They are for trainer design only: a "
      f"nuzlocke has no breeding, the gift eggs are scripted without egg moves, and the relearner never "
      f"offers them.")


def main(argv=None):
    argparse.ArgumentParser(description=__doc__.split("\n")[0]).parse_args(argv)
    write(run())


if __name__ == "__main__":
    main()

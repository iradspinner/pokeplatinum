"""Goal 3: every boss, rival, named Galactic fight and Ace Trainer of the
game read once, on the trainer files of the commit that lands alpha
readiness step 12 (step 15; docs/oxide/trainer-scoring-handoff.md, "Goal
3's reading").

Run it from an extracted copy of that commit, so that every file the
scorer reads (trainers, learnsets, encounters, items) is that commit's:

    git archive -o goal3.tar <commit>; mkdir <dir>; tar -x -C <dir> -f goal3.tar
    cd <dir> && PYTHONPATH=. tools/oxide/capped python3 -m tools.oxide.balance.plgoal3 --run <commit>

and afterwards, from the scoring worktree, put the pooled readings in the
difficulty store and write the summary:

    PYTHONPATH=. python3 -m tools.oxide.balance.plgoal3 --run <commit> --store

The fights: goal 3's single battles, as goal3_fights lists them (its kept
rows and those dropped only as doubles, as goal3.csv has them), less the
tag battles, which wait for the doubles planner: 39 bosses and 41 Ace
Trainers. The milestone reading before alpha 1 reads the bosses only (Ian,
2026-10-07, under his rule that each change is judged for its effect on
difficulty), so --kinds defaults to them.

The boxes (Ian's answer 3 of 2026-09-30, a spread of rolled boxes): three
random runs of the encounter simulator, seeds 1 to 3 (Ian cut five to three
for this milestone, 2026-10-07), every catch alive. Each seed is one run
through the whole game (Ian, 2026-10-15), so a catch is the same Pokemon
at every fight: each capture area is rolled once, at the run's first
visit, among the options open then (Ian's choice: nobody waits for Surf or
a rod), which keeps the box sizes the per-split rolls had. Box k's starter
is the starter list's k-th (Turtwig, Scorbunny, Piplup), so every rival
team is met by one box. A fight that closes its split (and each Elite Four
fight) takes the run's catches by the split's end; any other takes only
the catches made before it in walking order (the encounter sidecar's
order, which the OxiDex's Alpha tab follows) and every catch made from an
earlier split's options. Each member is the stage it reaches by the
fight's level, with its whole move pool from its catch, a Hardy nature,
IVs of 15, its first ability, and a gender rolled once from a fixed seed.

Held-back versions (Ian, 2026-10-15 and 2026-10-21): a boss's box also
offers each pre-evolution held back wherever that reaches, by the fight, a
move sooner than its evolution does or one its evolution never gets, of
any kind, the Pokemon and the move deciding and no power threshold
(plteam.holds_open; only a Starly held back, never a caught Staravia, has
Brave Bird by Maylene's split; a Fletchling held to 25 has Will-O-Wisp at
Gardenia), and the team search weighs both, never taking two versions of
one catch. So that a
hold's cost counts, a held-back version is offered only if no earlier
fight of the seed used the catch in a form the hold rules out (rule A),
and once a reading uses one, the seed's later fights see the line as the
hold left it (rule B). What each reading chose is kept in its box's
result.json ("chosen"), and the next fight's box is built from the chosen
of every earlier fight of the same seed, so each seed's fights read in
play order (play_order, run_all); the seeds still run side by side. A
hold rule A leaves out is listed in the result ("ruled_out") and the
summary, not modelled, since testing it means reading that earlier fight
again. Where the reading's chosen six uses a held-back version, the box
is read a second time with none on offer, and the result keeps both
readings ("without_holds", Ian, 2026-10-15: to measure what holds change;
narrowed on 2026-10-21 from wherever the screen's top sixes held one). An Ace Trainer's blind reading is offered no holds
and chooses no six, so it records nothing for later fights.

The planned-box sample (Ian, 2026-10-15): with --planned, Mars 1,
Gardenia, Maylene and Wake are also read on a fourth box, the Box sim's
planning player's (its best catches and its encounter waits, planned to
each fight's own split as pboxes.planned_box plans it), under the same
rules, its fights in play order like a seed's; the summary reports it
beside the random boxes and the store leaves it out.

The levels (Ian, 2026-10-07): a fight that closes its split at the split's
cap, the Elite Four at their aces, every other boss at its own ace's level
(the interim soft caps of 2026-10-02, extended to the later mini-bosses),
and an Ace Trainer at the soft cap in force where it stands: the ace of
the next boss or tag battle of its split not yet beaten, else the split's
cap. Never above the split's cap.

The items: what the run holds by the end of the fight's split
(fightsim.player_items): type boosters, Leftovers and Sitrus Berries.
Element 7's held items are never given to the player's six (Ian,
2026-10-07: no held-item try for this reading), so late bosses read
slightly hard.

The readings: a boss by the team search on each box (plteam.search), then
its winner's standard reading (75 fights at real odds and 25 very unlucky,
by the play-out planner at budget 64), the boxes pooled. One pair of
networks serves each boss (Ian's yes, 2026-10-07): its first box labels
and trains them, and its other boxes reuse them, skipping both; the race
they steer is a shortlist, and the play-out check and the loop decide on
each box. An Ace Trainer is read blind (plstudy.blind), its 75 and 25
fights shared among the boxes. Each boss's reading also reports how its
six uses Sticky Web and, where it carries the move, whether the wins lean
on it (web_report; Ian, 2026-10-15). Each box's result goes to
~/oxide-trials/goal3/<run>/ as it finishes, so a run stopped midway
resumes where it stopped. Jobs run fight by fight in play order, each
fight's boxes side by side once its first box is done (its networks), so
a run stopped early has read the early game on every box.
"""
import argparse
import collections
import datetime
import functools
import json
import os
import random
import subprocess
import sys
import time

from . import plthreads  # noqa: F401  (one numpy thread per process, before anything loads numpy)
from ..encounters import alpha, model as encounter_model
from . import data, fightsim as fs, pboxes, pldifficulty, plniche, plscore, plstudy, plteam, pool

# The reading runs from an extracted copy of a commit, which is not a git
# checkout. The encounter tool finds its tree by asking git, which fails
# there, and run from inside another checkout quietly reads that one
# instead. Point it at the tree this module was loaded from.
encounter_model.repo_root = lambda: data.ROOT

OUT = os.path.expanduser("~/oxide-trials/goal3")
SEEDS = (1, 2, 3)
# The planned-box sample (Ian, 2026-10-15): a fourth box, the Box sim's
# planning player's, read once on these fights beside the random boxes.
PLANNED = "planned"
PLANNED_FIGHTS = ("mars_1", "gardenia", "maylene", "wake")
# An Ace Trainer's fights on each box, real and very unlucky: about 75 and
# 25 over the boxes.
BLIND = (75 // len(SEEDS), 25 // len(SEEDS))
ACE = "Ace Trainers"
# The fights that close a split, and the Elite Four, each at its split's
# cap or its own ace (fightsim.fight_cap).
CLOSES = set(pool.CLOSING.values()) | set(fs.ELITE_FOUR_CAPS)

Catch = collections.namedtuple("Catch", "species split place area")


# ---- the fights -------------------------------------------------------------------------------------------

@functools.lru_cache(maxsize=None)
def all_rows():
    """[{name, kind, split, ids, story, slug, single}] for every row goal3.csv
    lists, in goal3_fights' order: its kept rows and those dropped only as
    doubles. A row is single unless it is a tag battle or a double."""
    sys.path.insert(0, plniche.GOAL3)
    import goal3_fights as g3
    rows = []
    g3.write = lambda rs, left: rows.extend(rs)
    g3.main()
    story = {tuple(sorted(f["tr_ids"])): f for f in data.fights()["fights"]}
    ox = data.oxide_trainers()
    out = []
    for r in rows:
        if r.drop and set(r.drop) - {"double"}:
            continue
        flags = " ".join(r.flags)
        multi = ("tag battle", "double against two trainers", "sight lines cross", "double battle")
        f = story.get(tuple(sorted(r.ids)))
        out.append({"name": r.name, "kind": r.kind, "split": f["split"] if f else r.split, "ids": list(r.ids),
                    "story": f["key"] if f else None, "slug": f["key"] if f else ox[r.ids[0]]["stem"],
                    "single": not any(m in flags for m in multi)})
    return out


def fights():
    """Goal 3's single battles: what this driver reads."""
    return [f for f in all_rows() if f["single"]]


def trainers_of(f):
    """The trainer records of a row, in the order its variants come."""
    if f["story"]:
        fight = next(x for x in data.fights()["fights"] if x["key"] == f["story"])
        return data.fight_trainers("oxide", fight)
    ox = data.oxide_trainers()
    return [dict(ox[i], tr_id=i) for i in f["ids"]]


def met(f, starter):
    """(fight key, variant index, trainer record): the team a run with this
    starter meets (plscore.variant_for's rule, read from the files)."""
    ts = trainers_of(f)
    want = plscore.SLOT_STARTER.get(plscore.STARTER_VARIANT.get(starter), starter)
    v = next((i for i, t in enumerate(ts) if len(ts) > 1 and plscore.slot_starter(t) == want), 0)
    if f["story"]:
        return f["story"], v, ts[v]
    return f"tr:{ts[v]['tr_id']}", 0, ts[v]


def ace(trainers):
    return max(m["level"] for t in trainers for m in t["party"])


def closes(f):
    return f["story"] in CLOSES


# ---- where a fight stands, and its level --------------------------------------------------------------------

@functools.lru_cache(maxsize=None)
def zone_order():
    return alpha.zone_order(data.ROOT)


START = float("-inf")       # a fight met as its split opens: only earlier splits' catches come before it


@functools.lru_cache(maxsize=None)
def own_areas(split):
    """[(order, name)] of the areas first reached in this split."""
    return [(area_place(a), a["name"]) for a in pboxes.context(split)["areas"]
            if a["split"] == split and area_place(a) is not None]


@functools.lru_cache(maxsize=None)
def place(slug):
    """A row's place in walking order, the earliest of its trainers': the
    order of the zone its trainer's map lies in, when that falls among its
    split's own areas. A zone first reached in an earlier split (Mars 2 at
    Lake Verity, the officers on Mt. Coronet) is being revisited: the fight
    takes its split's own area of that zone's name where there is one (Mt.
    Coronet Peak), else the split's start (START). None where no map is
    known."""
    f = next(x for x in all_rows() if x["slug"] == slug)
    own = own_areas(f["split"])
    lo, hi = (min(o for o, _n in own), max(o for o, _n in own)) if own else (None, None)
    zo, at, known = zone_order(), [], False
    for t in trainers_of(f):
        h = alpha.trainer_map(data.ROOT, t["constant"])
        z = alpha.zone_of(h) if h else None
        if z not in zo:
            continue
        known = True
        if own and lo <= zo[z] <= hi:
            at.append(zo[z])
            continue
        same = [o for o, n in own if n.startswith(z)]
        at.append(min(same) if same else START)
    return min(at) if at else (START if known else None)


def area_place(area):
    if area.get("order") is not None:
        return area["order"]
    return zone_order().get(area["name"].split(" (")[0])


def level(f, trainer):
    """The level the player's box stands at for this fight (the module's
    rule)."""
    split = f["split"]
    cap = pool.caps()[split]
    if closes(f):
        return fs.fight_cap(split, f["story"])
    if f["kind"] != ACE:
        return min(ace([trainer]), cap)
    # An Ace Trainer: the soft cap in force where it stands. A player's
    # level never falls along the walk, so the cap is never below a boss of
    # the split already beaten, nor below the split before's cap.
    at = place(f["slug"])
    bosses = [(place(r["slug"]), r) for r in all_rows()
              if r["kind"] != ACE and r["split"] == split and not closes(r)]
    bosses = [(p, r) for p, r in bosses if p is not None and at is not None]
    i = pool.SPLITS.index(split)
    floor = max([pool.caps()[pool.SPLITS[i - 1]]] if i else [0])
    floor = max([floor] + [ace(trainers_of(r)) for p, r in bosses if p < at])
    ahead = [(p, r) for p, r in bosses if p >= at]
    if not ahead:
        return cap
    _p, nxt = min(ahead, key=lambda pr: pr[0])
    return min(max(ace(trainers_of(nxt)), floor), cap)


@functools.lru_cache(maxsize=None)
def play_order():
    """[slug] of goal 3's fights in the order a run meets them, the order
    each seed's fights are read in (box's rules A and B). The story fights
    come in fights.json's order, the story path; every other fight (the
    officers, the Stark Mountain commanders, the Ace Trainers) comes before
    the first story fight of its split at or past its place, a closing fight
    counting as its split's end, so an officer met where a commander is
    (Somnu at Valley Windworks, Moira in the Eterna building) comes first,
    as the officers guard the way. A place cannot order a story fight met in
    a revisited zone, which takes its split's start (Lucas and Dawn 2's box
    lacks the catches Jupiter 1's has from their split, yet it comes after
    Jupiter 1), so the story path orders those."""
    rows = fights()
    story = {x["key"]: i for i, x in enumerate(data.fights()["fights"])}
    seq = sorted((f for f in rows if f["story"]), key=lambda f: story[f["story"]])

    def at(f):
        p = place(f["slug"])
        return float("inf") if p is None else p

    def mark(f):
        return float("inf") if closes(f) else at(f)

    for f in sorted((f for f in rows if not f["story"]), key=lambda f: (pool.split_index(f["split"]), at(f))):
        i = pool.split_index(f["split"])
        j = next((n for n, s in enumerate(seq) if s["story"] and pool.split_index(s["split"]) == i
                  and mark(s) >= at(f)), None)
        if j is None:
            j = max([n + 1 for n, s in enumerate(seq) if pool.split_index(s["split"]) <= i] or [0])
        seq.insert(j, f)
    return tuple(f["slug"] for f in seq)


# ---- the boxes ----------------------------------------------------------------------------------------------

# A run is rolled over every capture area of the game, the last split's.
LAST = "League"


@functools.lru_cache(maxsize=None)
def run_of(seed):
    """[Catch] of box seed's one run through the whole game, the starter
    first (Ian, 2026-10-15: each box seed is one run, so a catch is the same
    Pokemon at every fight; until then each split rolled its own box, and
    Gardenia's and Maylene's seed 1 agreed on 17 of 25 areas' catches).
    Each capture area, in the simulator's walking order, is rolled once at
    the run's first visit, among the options open then (Ian's choice:
    nobody waits for Surf or a rod): the options of the earliest split any
    of its options opens in, with no repel manipulation and no trade that
    costs a Pokemon, a species drawn by the option's own odds under the
    dupes clause. Box k's starter is the starter list's k-th. This keeps
    the box sizes the per-split rolls had, where one roll among all of an
    area's options left the early boxes a third smaller (test_plgoal3 holds
    the sizes)."""
    ctx = pboxes.context(LAST)
    rank, values = ctx["rank"], ctx["values"]
    rng = random.Random(seed)
    box = pboxes.sim.Box(ctx["root"], values)
    starters = ctx["starter_src"]["pool"]
    rng.choice(starters)        # drawn as plniche.roll draws it, so the rolls after it are the seed's own
    starter = starters[(seed - 1) % len(starters)]
    where = ctx["starter_src"].get("capture_area") or "Route 201"
    box.add(starter, where)
    caught = [Catch(starter, None, None, where)]
    drawn = set()
    for area in ctx["areas"]:
        if area["name"] == where:
            continue
        opts = [o for o in area["options"] if o.repel is None and not o.requires]
        if not opts:
            continue
        first = min(rank.get(o.split, 99) for o in opts)
        opt = rng.choice([o for o in opts if rank.get(o.split, 99) == first])
        sp = pboxes.roll(area, opt, box, rng, drawn)
        if sp is None:
            continue
        if opt.kind == "legendary":
            drawn.add(sp)
        box.add(sp, area["name"])
        caught.append(Catch(sp, opt.split, area_place(area), area["name"]))
    return tuple(caught)


@functools.lru_cache(maxsize=None)
def roll(split, seed):
    """[Catch] of box seed's run by the split's end: its catches from options
    open by then, the starter first. Every fight of the seed draws on the
    one run (run_of); the planned box (PLANNED) on the planning player's
    run to the split's end (planned)."""
    if seed == PLANNED:
        return planned(split)
    rank = pboxes.context(LAST)["rank"]
    return tuple(c for c in run_of(seed) if c.split is None or rank.get(c.split, 99) <= rank[split])


@functools.lru_cache(maxsize=None)
def planned(split):
    """[Catch] of the Box sim's planning player's run to the split's end
    (pboxes.planned_run: each area's best option and its waits for a later
    table, the dupes clause, no deaths), the planned-box sample's box. It is
    planned to the fight's own split, as pboxes.planned_box plans it: one
    plan to the League waits for Super Rods until Candice's split at three
    of Roark's areas, which would leave them out of every box before then.
    So two splits' plans can catch differently, and rule B carries a hold
    only where the same area gave the same Pokemon. A catch the planner waited for is made
    at the end of the later table's split in the simulator's walk, so it has
    no place there: cut takes it only from that split's closing fight on."""
    by_name = {a["name"]: a for a in pboxes.context(split)["areas"]}
    return tuple(Catch(sp, s, None if s is None or waited else area_place(by_name[name]), name)
                 for sp, s, name, waited in pboxes.planned_run(split))


def cut(caught, f):
    """The catches a run has made by this fight (the module's rule)."""
    at = place(f["slug"])
    if closes(f) or at is None:
        return list(caught)
    rank = pboxes.context(f["split"])["rank"]
    return [c for i, c in enumerate(caught)
            if i == 0 or rank[c.split] < rank[f["split"]] or (c.place is not None and c.place <= at)]


@functools.lru_cache(maxsize=None)
def place_starts():
    """{place evolution method: (split, order)}: where the walk first
    reaches one of the engine's maps for it (pool.place_maps: the magnetic
    field from Mt. Coronet 1F South, the Moss Rock in Eterna Forest, the Ice
    Rock on Route 217)."""
    from . import splits
    zo, out = zone_order(), {}
    for method, headers in pool.place_maps().items():
        at = []
        for h in headers:
            s, z = splits.map_split(h)[0], alpha.zone_of(h)
            if s in pool.SPLITS and z in zo:
                at.append((pool.split_index(s), zo[z], s))
        if at:
            _i, order, s = min(at)
            out[method] = (s, order)
    return out


def places(f):
    """The place evolutions the run has reached by this fight."""
    at, here = place(f["slug"]), pool.split_index(f["split"])
    return {m for m, (s, order) in place_starts().items()
            if here > pool.split_index(s)
            or (here == pool.split_index(s) and (closes(f) or (at is not None and at >= order)))}


def box(caught, f, lvl, seed, hist=None, holds=True):
    """The box's members as the fight reads them, at this level, and the
    holds rule A leaves out: {"records": [record], "ruled_out": [hold]}.
    Each member has a gender rolled once at its catch, which a gendered
    evolution follows, and a coin that settles any choice among evolutions
    (Wurmple's, Eevee's).

    Each catch comes once as its line stands: evolved on time, or as the
    hold its last use in this seed left it (rule B, Ian, 2026-10-15: once a
    reading uses a held-back version, the seed's later fights see the line
    as the hold left it). `hist` is history's {area: [use]}. With `holds`,
    a catch also comes held back wherever that reaches a move sooner than
    its evolution does, or one its evolution never gets (plteam.holds_open,
    any kind of move, Ian, 2026-10-21), unless an earlier
    fight of the seed used the catch in a form the hold rules out (rule A,
    the same day): at that fight's level the hold would have made it a
    different stage, or one that evolved at another level. A hold rule A
    leaves out is listed in "ruled_out", not modelled, since testing it
    means reading that earlier fight again; it is left off the list where
    an offered hold brings the same moves. Of the held versions that bring
    the same moves (Starly held to 37 and Staravia to 43 both bring Brave
    Bird by Wake), the one held the fewest levels is kept.

    Every record carries its catch (its area; versions of one catch share
    it, and plteam's search never takes two in one six), its holds, whether
    it is a held-back version offered beside the line as it stands ("held"),
    the moves its hold brings ("gained") and of those the moves the hold is
    for, learned at the hold's level ("hold_for", which the play-off puts
    in first), and its path of evolutions at this level ("path", what rule
    A compares)."""
    hist = hist or {}
    blob = fs.calc.blob()["poks"]
    reached = sorted(places(f))
    recs, ruled = [], []
    for c in caught:
        caught_level = 5 if c.split is None else plniche.catch_level(c.species, c.split)
        tag = f"goal 3 / box {seed} / {c.area}"
        gender = fs.rolled_gender(c.species, tag)
        coin = random.Random(f"evolution / {tag}").randrange(1 << 16)

        def path(hold, at=lvl, where=reached):
            return [list(p) for p in plteam.chain(c.species, min(caught_level, at), at, hold, places=where,
                                                  gender=gender, coin=coin)]

        def member(hold, held, gained=()):
            final, pool_ = plteam.move_pool(c.species, min(caught_level, lvl), lvl, hold, places=reached,
                                            gender=gender, coin=coin)
            name = plteam.species_name(final)
            ability = (blob.get(name) or {}).get("abilities", {}).get("0")
            return plteam.record(final, lvl, "Hardy", ability, 15, pool_, label=plteam.hold_label(name, hold),
                                 gender=gender, line=plniche.line_of(c.species), caught=c.species,
                                 caught_level=caught_level, area=c.area, catch=c.area, hold=dict(hold),
                                 held=held, gained=list(gained), hold_for=plteam.hold_moves(base, hold, gained),
                                 path=path(hold))

        uses = [u for u in hist.get(c.area, []) if u["caught"] == c.species]
        base = dict(uses[-1]["hold"]) if uses else {}
        recs.append(member(base, False))
        if not holds:
            continue
        offered, out = [], []
        for hold, gained, wait in plteam.holds_open(c.species, min(caught_level, lvl), lvl, base, places=reached,
                                                    gender=gender, coin=coin):
            if any(set(g) >= set(gained) for g in offered):
                continue            # an offered hold held no longer brings these moves already
            against = next((u for u in uses if path(hold, u["level"], u["places"]) != u["path"]), None)
            if against is None:
                offered.append(gained)
                recs.append(member(hold, True, gained))
            elif not any(set(o["gained"]) >= set(gained) for o in out):
                stage = plteam.species_name(path(hold)[-1][0])
                out.append({"area": c.area, "label": plteam.hold_label(stage, hold), "hold": hold,
                            "gained": gained, "used_at": against["fight"], "used_as": against["label"]})
        ruled += [o for o in out if not any(set(g) >= set(o["gained"]) for g in offered)]
    return {"records": recs, "ruled_out": ruled}


def records(caught, f, lvl, seed):
    """The box's members evolved on time, no hold offered or carried."""
    return box(caught, f, lvl, seed, holds=False)["records"]


def history(run, seed, slug):
    """({area: [use]}, [slug]): what the readings of this seed's fights
    before this one chose, in play order (each box's result.json keeps its
    "chosen", the uses that rules A and B read), and the fights they came
    from. A fight not yet read is not among them, which is why a seed's
    fights are read in play order (run_all)."""
    order = play_order()
    out, src = {}, []
    for s in order[:order.index(slug)]:
        path = os.path.join(box_dir(run, s, seed), "result.json")
        if not os.path.exists(path):
            continue
        with open(path) as fh:
            chosen = json.load(fh).get("chosen")
        if chosen is None:
            continue
        src.append(s)
        for u in chosen:
            out.setdefault(u["area"], []).append(u)
    return out, src


def uses(st, team, f, lvl):
    """What a reading chose, for the seed's later fights (history): each
    member of its six with its catch, the holds it carries, its stage and
    its path of evolutions at the fight's level and places."""
    out = []
    for k in team:
        r = st["pokemon"][k]
        out.append({"fight": f["slug"], "area": r["area"], "caught": r["caught"], "species": r["constant"],
                    "label": r["label"], "hold": r.get("hold") or {}, "held": bool(r.get("held")), "level": lvl,
                    "places": sorted(places(f)), "path": r["path"]})
    return out


# ---- one fight on one box -----------------------------------------------------------------------------------

def box_dir(run, slug, seed):
    return os.path.join(OUT, run, slug, f"box{seed}")


def first_box_model(run, slug, seed):
    """The networks the boss's first box trained, for a later box to reuse;
    None on the first box, or where the first box has no result yet (the
    later box then labels and trains its own, as the first would)."""
    if seed == SEEDS[0]:
        return None
    path = os.path.join(box_dir(run, slug, SEEDS[0]), "result.json")
    if not os.path.exists(path):
        return None
    with open(path) as fh:
        return json.load(fh).get("model")


def fight_state(key, recs, stock, v, slug):
    """(st, keys, boss_keys, flags): the fight against this box, every member
    with its whole move pool, and the run's items by then."""
    prep = plscore.prepare(plscore.parse_fight(key), given_side=recs)
    if prep.get("doubles"):
        raise SystemExit(f"{slug}: a double battle, which goal 3 leaves to the doubles planner")
    st = prep["st"]
    st["item_stock"] = dict(stock)
    boss_keys, flags, _s = prep["variants"][v]
    return st, [f"p{i}" for i in range(len(recs))], boss_keys, flags


def setup(run, slug, seed):
    """Everything one fight on one box reads before its search: the fight,
    the seed's run by it, the team it meets, its level, the box (with this
    seed's history: box's rules A and B) and the run's items."""
    f = next(x for x in fights() if x["slug"] == slug)
    whole = roll(f["split"], seed)
    caught = cut(whole, f)
    key, v, trainer = met(f, whole[0].species)
    lvl = level(f, trainer)
    hist, hist_from = history(run, seed, slug)
    # An Ace Trainer's blind reading chooses no six, so it is offered no
    # holds (it still sees each line as the seed's holds left it).
    built = box(caught, f, lvl, seed, hist, holds=f["kind"] != ACE)
    return dict(f=f, whole=whole, caught=caught, key=key, v=v, trainer=trainer, lvl=lvl, hist_from=hist_from,
                built=built, stock=fs.player_items(f["split"]))


def read_box(run, slug, seed, procs):
    """One fight on one box: the team search and its winner's reading for a
    boss, the blind reading for an Ace Trainer; its result.json, whose
    "chosen" (the boss's six, uses) the seed's later fights are built from."""
    out_dir = box_dir(run, slug, seed)
    path = os.path.join(out_dir, "result.json")
    if os.path.exists(path):
        with open(path) as fh:
            return json.load(fh)
    os.makedirs(out_dir, exist_ok=True)
    t0 = time.time()
    s = setup(run, slug, seed)
    f, whole, key, v, trainer, lvl, stock = s["f"], s["whole"], s["key"], s["v"], s["trainer"], s["lvl"], s["stock"]
    split, recs = f["split"], s["built"]["records"]
    st, keys, boss_keys, flags = fight_state(key, recs, stock, v, slug)
    result = {"fight": f["name"], "slug": slug, "kind": f["kind"], "split": split, "seed": seed, "run": run,
              "starter": whole[0].species, "trainer": trainer["constant"], "key": key, "level": lvl,
              "place": place(slug), "box": [f"{r['label']} ({r['area']})" for r in recs],
              "left_out": len(whole) - len(s["caught"]), "items": stock,
              "foes": [f"{st['pokemon'][k]['species']} {st['pokemon'][k]['level']}" for k in boss_keys],
              "offered": [r["label"] for r in recs if r["held"]], "ruled_out": s["built"]["ruled_out"],
              "history_from": s["hist_from"]}
    if f["kind"] == ACE:
        real, unlucky, faints_to, fainted = plstudy.blind(
            st, keys, boss_keys, flags, real=BLIND[0], unlucky=BLIND[1], procs=procs, seed=11 + 100 * seed,
            cap=lvl, split=split, leave_out=[trainer["tr_id"]])
        result.update(how="blind", real=real, unlucky=unlucky, faints_to=faints_to, fainted=fainted, chosen=[])
    else:
        model = first_box_model(run, slug, seed)
        summary = plteam.search(f"g3-{run}-{slug}-b{seed}", key, recs, stock, os.path.join(out_dir, "search"),
                                procs=procs, prepared=(st, keys, boss_keys, flags), model=model)
        result.update(model=summary.get("model"), reused=model is not None)
        win = summary["winner_keys"]
        tallies = []
        real, unlucky, rows = plteam.full_reading(st, boss_keys, flags, win, {}, procs=procs, tallies=tallies)
        result.update(how="search", winner=summary["winner"],
                      moves={st["pokemon"][k]["species"]: st["moves"][k] for k in win},
                      items={st["pokemon"][k]["species"]: it for k, it in fs.assign_items(st, win).items() if it},
                      real=real, unlucky=unlucky, faints_to=plteam.losing_enemies(rows),
                      fainted=plstudy.fainted(rows), chosen=uses(st, win, f, lvl),
                      held_used=[st["pokemon"][k]["label"] for k in win if st["pokemon"][k]["held"]])
        result["sticky_web"] = web_report(st, boss_keys, flags, win, tallies, recs, real, procs)
        # The play-off's record, and the held versions it put in a finalist
        # (Ian's option 1, 2026-10-21).
        result["playoff"] = summary.get("playoff") or []
        result["playoff_won"] = sorted({n for p in result["playoff"] for n in p.get("kept", [])
                                        if n not in p["six"] and n in set(result["offered"])})
        offered = set(result["offered"])
        result["held_in_screen"] = sorted({n for six in summary["screen"] for n in six} & offered)
        # Paired only where the chosen six uses a held version (Ian,
        # 2026-10-21; until then wherever the screen's top sixes held one,
        # which from Barry 3 on was nearly every box).
        if result["held_used"]:
            result["without_holds"] = without_holds(run, slug, seed, s, summary.get("model"), procs, out_dir)
    result["minutes"] = round((time.time() - t0) / 60, 1)
    with open(path + ".part", "w") as fh:
        json.dump(result, fh, indent=1)
    os.replace(path + ".part", path)
    r, u = result["real"], result["unlucky"]
    pair = result.get("without_holds")
    print(f"{f['name']} box {seed} ({result['how']}, level {lvl}): real {r['won']:.0%} won, {r['faints']:.2f} "
          f"faints, {r['clean']:.0%} clean; very unlucky {u['won']:.0%}, {u['faints']:.2f}"
          + (f"; without holds {pair['real']['won']:.0%} won, {pair['real']['faints']:.2f} faints" if pair else "")
          + f"; {result['minutes']} minutes", flush=True)
    return result


WEB = "Sticky Web"


def web_report(st, boss_keys, flags, win, tallies, recs, real, procs, check=25):
    """How the reading's six uses Sticky Web (Ian, 2026-10-15: keep an eye
    out in case it becomes an omnipresent strategy for the scorer): the
    members whose four moves carry it, and for each of the reading's two
    tallies (real odds, very unlucky) the fights it was laid in and the
    wins with it laid and without. Where the six carries it, the six is
    read again on `check` fights at real odds by the same play-out planner,
    each carrier's web swapped for its strongest other attack from its move
    pool (by fightsim.play_strength), and "leans" says whether the win rate
    fell more than plteam.WIN_TOL below the reading's without it."""
    team = tuple(win)
    carriers = [k for k in win if WEB in st["moves"][k]]
    out = {"carried_by": [plteam.member_name(st["pokemon"][k]) for k in carriers]}
    if not carriers:
        return out
    for luck, t in zip(("real", "unlucky"), tallies):
        rows, chose = t.rows[team], t.chose.get(team, [])
        laid = [WEB in c for c in chose]
        out[luck] = {"fights": len(rows), "laid": sum(laid),
                     "won_laid": sum(1 for r, lay in zip(rows, laid) if lay and r[0]),
                     "won_not_laid": sum(1 for r, lay in zip(rows, laid) if not lay and r[0])}
    kept, swapped = {k: (st["moves"][k], st["pokemon"][k]) for k in carriers}, {}
    try:
        for k in carriers:
            pool_ = recs[int(k[1:])]["moves"]           # the record's whole move pool
            types = (fs.calc.blob()["poks"].get(st["pokemon"][k]["species"]) or {}).get("types") or []
            spare = sorted((n for n in pool_ if n not in st["moves"][k] and fs.move(n).damaging()
                            and fs.play_strength(n, types) > 0), key=lambda n: -fs.play_strength(n, types))
            new = [n for n in st["moves"][k] if n != WEB] + spare[:1]
            swapped[plteam.member_name(st["pokemon"][k])] = spare[0] if spare else None
            st["moves"][k] = new
            st["pokemon"][k] = dict(st["pokemon"][k], moves=new)
        t = plteam.read(st, boss_keys, flags, [list(win)], check, {}, procs=procs, seed0=4243)
    finally:
        for k, (mv, rec) in kept.items():
            st["moves"][k], st["pokemon"][k] = mv, rec
    out["without"] = dict(t.numbers(team), swapped=swapped)
    out["leans"] = out["without"]["won"] < real["won"] - plteam.WIN_TOL
    return out


def without_holds(run, slug, seed, s, model, procs, out_dir):
    """The paired reading (Ian, 2026-10-15): where the reading's chosen six
    uses a held-back version (the trigger Ian narrowed on 2026-10-21), the
    same box is read again with none on offer, each line as it stands (the
    holds rule B carries stay), by the same search and reading, so that the
    reading reports what the holds change. The search reuses the networks of the box's own
    search. Its winner chooses nothing for later fights: the reading with
    the holds on offer is the box's reading."""
    t0 = time.time()
    base = [r for r in s["built"]["records"] if not r["held"]]
    st, keys, boss_keys, flags = fight_state(s["key"], base, s["stock"], s["v"], slug)
    summary = plteam.search(f"g3-{run}-{slug}-b{seed}-without-holds", s["key"], base, s["stock"],
                            os.path.join(out_dir, "search-without-holds"), procs=procs,
                            prepared=(st, keys, boss_keys, flags), model=model)
    win = summary["winner_keys"]
    real, unlucky, rows = plteam.full_reading(st, boss_keys, flags, win, {}, procs=procs)
    return {"winner": summary["winner"], "moves": {st["pokemon"][k]["species"]: st["moves"][k] for k in win},
            "real": real, "unlucky": unlucky, "faints_to": plteam.losing_enemies(rows),
            "minutes": round((time.time() - t0) / 60, 1)}


# ---- the run ------------------------------------------------------------------------------------------------

def jobs(only=None, kinds=("boss", "ace"), seeds=SEEDS, planned_sample=False):
    """(slug, seed) in run order: the fights in play order, each with its
    boxes side by side; with `planned_sample`, the planned box (PLANNED) of
    each sample fight (PLANNED_FIGHTS) among them as one more box, which
    reads in play order like a seed."""
    by = {f["slug"]: f for f in fights()}
    picked = [s for s in play_order() if (not only or s in only)
              and ("ace" if by[s]["kind"] == ACE else "boss") in kinds]
    return [(slug, s) for slug in picked
            for s in tuple(seeds) + ((PLANNED,) if planned_sample and slug in PLANNED_FIGHTS else ())]


def waits_on(job, todo):
    """The jobs of `todo` this one must wait for: every earlier boss of its
    seed in play order, whose chosen six its box is built from (box's rules
    A and B; an Ace Trainer chooses none), and for a boss's later box its
    first box, whose networks it reuses (first_box_model)."""
    slug, s = job
    rank = {x: i for i, x in enumerate(play_order())}
    kind = {f["slug"]: f["kind"] for f in fights()}
    out = [(x, ss) for x, ss in todo if ss == s and rank[x] < rank[slug] and kind[x] != ACE]
    if s != SEEDS[0] and kind[slug] != ACE and (slug, SEEDS[0]) in todo:
        out.append((slug, SEEDS[0]))
    return out


def run_all(run, todo, parallel, procs):
    """The jobs not yet done, `parallel` at a time, each in its own process
    (a team search forks its own workers, which a pool's workers may not),
    so one job's network training on the GPU overlaps another's play-outs.
    A seed's fights read in play order: a job starts once every job it
    waits on is done (waits_on), so the seeds run side by side, a boss's
    later boxes a step behind its first. A job left waiting on one that
    failed cannot be read and is left for the next run; a failed first box
    only costs its later boxes their reuse of its networks."""
    def done(job):
        return os.path.exists(os.path.join(box_dir(run, *job), "result.json"))

    pending = [j for j in todo if not done(j)]
    print(f"goal 3, run {run}: {len(todo) - len(pending)} of {len(todo)} boxes done; {len(pending)} to go",
          flush=True)
    running, failed = [], set()
    while pending or running:
        for job in list(pending):
            if len(running) >= parallel:
                break
            deps = waits_on(job, todo)
            first = (job[0], SEEDS[0])
            if any(d in failed and d != first for d in deps):
                pending.remove(job)
                failed.add(job)
                print(f"LEFT {job[0]} box {job[1]}: an earlier fight of its box failed", flush=True)
                continue
            if not all(done(d) or (d == first and d in failed) for d in deps):
                continue
            pending.remove(job)
            slug, s = job
            os.makedirs(box_dir(run, slug, s), exist_ok=True)
            log = open(os.path.join(box_dir(run, slug, s), "log.txt"), "a")
            cmd = [sys.executable, "-m", "tools.oxide.balance.plgoal3", "--run", run, "--one", slug, str(s),
                   "--procs", str(procs)]
            running.append((slug, s, subprocess.Popen(cmd, cwd=data.ROOT, stdout=log, stderr=subprocess.STDOUT,
                                                      env=dict(os.environ, PYTHONPATH=".")), log))
        if not running:
            if pending:
                print(f"stopped: {len(pending)} boxes wait on boxes outside this run", flush=True)
            break
        time.sleep(5)
        for item in list(running):
            slug, s, proc, log = item
            if proc.poll() is None:
                continue
            running.remove(item)
            log.close()
            path = os.path.join(box_dir(run, slug, s), "result.json")
            if proc.returncode == 0 and os.path.exists(path):
                with open(path) as fh:
                    r = json.load(fh)
                print(f"done {slug} box {s}: real {r['real']['won']:.0%} won, {r['real']['faints']:.2f} faints; "
                      f"{r['minutes']} minutes", flush=True)
            else:
                failed.add((slug, s))
                print(f"FAILED {slug} box {s} (exit {proc.returncode}); its log.txt says why", flush=True)


# ---- pooling, the store and the summary ---------------------------------------------------------------------

def results(run, seeds=SEEDS):
    """{slug: [box results]} of a run, in fight order: the random boxes',
    which the store pools (the planned box's are planned_results')."""
    out = {}
    for f in fights():
        rs = []
        for s in seeds:
            path = os.path.join(box_dir(run, f["slug"], s), "result.json")
            if os.path.exists(path):
                with open(path) as fh:
                    rs.append(json.load(fh))
        if rs:
            out[f["slug"]] = rs
    return out


def planned_results(run):
    """{slug: the planned box's result} of a run's planned-box sample."""
    return {slug: rs[0] for slug, rs in results(run, (PLANNED,)).items()}


def planned_table(run, by_slug):
    """The summary's table of the planned-box sample (Ian, 2026-10-15): each
    sample fight read on the planning player's box beside its random boxes
    pooled, which the sample stays out of."""
    plan, res = planned_results(run), results(run)
    if not plan:
        return []
    out = ["", "The planned-box sample: the Box sim's planning player's box (its best catches and its encounter "
               "waits), beside the random boxes pooled.", "",
           "| Fight | Planned box: members | Won | Faints | Clean | Random boxes: won | Faints |", "|---|---|---|---|---|---|---|"]
    for slug, r in plan.items():
        rand = pool_side([x["real"] for x in res[slug]]) if res.get(slug) else None
        out.append(f"| {by_slug[slug]['name']} | {len(r['box'])} | {r['real']['won']:.0%} | {r['real']['faints']:.2f} | "
                   f"{r['real']['clean']:.0%} | " + (f"{rand['won']:.0%} | {rand['faints']:.2f} |" if rand
                                                     else "not read | |"))
    return out


def pool_side(sides):
    """Three numbers pooled over several readings, weighted by their fights."""
    n = sum(s["fights"] for s in sides)
    return {"won": round(sum(s["won"] * s["fights"] for s in sides) / n, 4),
            "clean": round(sum(s["clean"] * s["fights"] for s in sides) / n, 4),
            "faints": round(sum(s["faints"] * s["fights"] for s in sides) / n, 4), "fights": n}


def store_key(f, trainer):
    """The store's key: the trainer constant, or the story fight's key when
    it has several (pldifficulty)."""
    return f["story"] if f["story"] and len(trainers_of(f)) > 1 else trainer


def store(run, commit, path=pldifficulty.PATH):
    """Each fight's pooled reading into the difficulty store: one per team
    the boxes met (a rival's teams by the boxes' starters)."""
    today = datetime.date.today().isoformat()
    by_slug = {f["slug"]: f for f in fights()}
    n = 0
    for slug, rs in results(run).items():
        f = by_slug[slug]
        for trainer in dict.fromkeys(r["trainer"] for r in rs):
            mine = [r for r in rs if r["trainer"] == trainer]
            real = pool_side([r["real"] for r in mine])
            how = "the team search's winner on each" if f["kind"] != ACE else "blind on each"
            label = f["name"] if len(mine) == len(rs) else f"{f['name']}, the team {trainer} fields"
            pldifficulty.put(store_key(f, trainer), dict(
                real, label=label, team="oxide", trainer=trainer, date=today, stale=None,
                unlucky=pool_side([r["unlucky"] for r in mine]),
                source=f"goal 3 on {commit}: {len(mine)} rolled box{'es' if len(mine) > 1 else ''} "
                       f"(seeds {', '.join(str(r['seed']) for r in mine)}), {how}"), path)
            n += 1
    problems = pldifficulty.problems(pldifficulty.load(path))
    print(f"{n} readings put in {path}; the store's problems: {problems or 'none'}")
    return problems


def box_notes(r):
    """A box's lines on its holds for the summary: the held-back versions it
    offered, those its winner took, and those rule A left out, with the
    earlier fight whose six rules each out."""
    out = []
    if r.get("offered"):
        out.append(f"  - held back on offer: {', '.join(r['offered'])}")
    if r.get("held_used"):
        out.append(f"  - the winner took held back: {', '.join(r['held_used'])}")
    if r.get("playoff_won"):
        out.append(f"  - the play-off put in a finalist: {', '.join(r['playoff_won'])}")
    for h in r.get("ruled_out") or []:
        out.append(f"  - not offered, not modelled: {h['label']} for {', '.join(h['gained'])}, since "
                   f"{by_slug_name(h['used_at'])} used it as {h['used_as']}")
    pair = r.get("without_holds")
    if pair:
        out.append(f"  - read again without them: {', '.join(pair['winner'])}; {pair['real']['won']:.0%} won, "
                   f"{pair['real']['faints']:.2f} faints")
    return out


def web_lines(rs):
    """A fight's lines on Sticky Web for the summary (Ian, 2026-10-15): each
    box whose winner carries it, the fights it was laid in, and the win rate
    with it and with it swapped out, which says whether the wins lean on it."""
    out = []
    for r in rs:
        w = r.get("sticky_web") or {}
        if not w.get("carried_by"):
            continue
        real, no = w["real"], w["without"]
        swap = ", ".join(f"{mv or 'nothing'} on {who}" for who, mv in no["swapped"].items())
        box = "the planned box" if r["seed"] == PLANNED else f"box {r['seed']}"
        out.append(f"- Sticky Web in {box}'s six ({', '.join(w['carried_by'])}): laid in {real['laid']} "
                   f"of {real['fights']} fights at real odds, {real['won_laid']} of them won; {r['real']['won']:.0%} "
                   f"won with it, {no['won']:.0%} with {swap} in its place, so the wins "
                   f"{'lean' if w['leans'] else 'do not lean'} on it")
    return out


def web_total(res):
    """The summary's line on Sticky Web over the whole run."""
    rs = [r for v in res.values() for r in v if r.get("how") == "search"]
    carry = [r for r in rs if (r.get("sticky_web") or {}).get("carried_by")]
    lean = [r for r in carry if r["sticky_web"]["leans"]]
    return ["", f"Sticky Web: carried by the winners of {len(carry)} of {len(rs)} boss boxes read; their wins "
                f"lean on it in {len(lean)}."]


def paired_table(res, by_slug):
    """The summary's table of the paired readings (Ian, 2026-10-15): each box
    whose chosen six uses a held-back version, read with the holds on offer
    and again without, both numbers side by side."""
    rows = [(by_slug[slug], r) for slug, rs in res.items() for r in rs if r.get("without_holds")]
    if not rows:
        return []
    out = ["", "Paired readings: the boxes whose chosen six uses a held-back version, read again with none on "
               "offer.", "",
           "| Fight | Box | With holds: won, faints | Without: won, faints | Held back in the chosen six |",
           "|---|---|---|---|---|"]
    for f, r in rows:
        a, b = r["real"], r["without_holds"]["real"]
        out.append(f"| {f['name']} | {r['seed']} | {a['won']:.0%}, {a['faints']:.2f} | {b['won']:.0%}, "
                   f"{b['faints']:.2f} | {', '.join(r['held_used'])} |")
    return out


def by_slug_name(slug):
    return next((f["name"] for f in fights() if f["slug"] == slug), slug)


def species_of(name):
    """A member's species from its name in a result ("Staraptor (Starly held
    to 37)" is a Staraptor)."""
    return name.split(" (")[0]


def summary(run, commit):
    """The run's readings as Markdown: each fight's pooled numbers and
    difficulty, its boxes' winners, the lines every box's winner took, and
    the held-back versions each box offered, its winner took and rule A
    left out (listed, not modelled)."""
    by_slug = {f["slug"]: f for f in fights()}
    lines = [f"# Goal 3's readings, run {run} on {commit}", "",
             "| Fight | Split | Level | Boxes | Won | Faints | Clean | Difficulty | Very unlucky won |",
             "|---|---|---|---|---|---|---|---|---|"]
    detail = []
    plan = planned_results(run)
    for slug, rs in results(run).items():
        f = by_slug[slug]
        real, unl = pool_side([r["real"] for r in rs]), pool_side([r["unlucky"] for r in rs])
        lvls = sorted({r["level"] for r in rs})
        lines.append(f"| {f['name']} | {f['split']} | {', '.join(map(str, lvls))} | {len(rs)} | {real['won']:.0%} | "
                     f"{real['faints']:.2f} | {real['clean']:.0%} | {pldifficulty.difficulty(real):.2f} | "
                     f"{unl['won']:.0%} |")
        if f["kind"] != ACE:
            detail.append(f"## {f['name']}")
            # The planned box's line comes beside the random boxes', outside
            # their pooled numbers.
            for r in rs + ([plan[slug]] if slug in plan else []):
                detail.append(f"- {'the planned box' if r['seed'] == PLANNED else 'box ' + str(r['seed'])} "
                              f"({r['starter']}, {len(r['box'])} members, {r['trainer']}): "
                              f"{', '.join(r['winner'])}; {r['real']['won']:.0%} won, "
                              f"{r['real']['faints']:.2f} faints")
                detail += box_notes(r)
            every = set.intersection(*({species_of(n) for n in r["winner"]} for r in rs)) if len(rs) > 1 else set()
            if every:
                detail.append(f"- every box's winner took {', '.join(sorted(every))}")
            detail += web_lines(rs + ([plan[slug]] if slug in plan else []))
            detail.append("")
    every_box = {slug: rs + ([plan[slug]] if slug in plan else []) for slug, rs in results(run).items()}
    lines += web_total(every_box)
    lines += paired_table(every_box, by_slug)
    lines += planned_table(run, by_slug)
    text = "\n".join(lines + [""] + detail)
    with open(os.path.join(OUT, run, "summary.md"), "w") as fh:
        fh.write(text + "\n")
    return text


def dry(run, slug, seed, screen=False):
    """One box as its reading would build it, read from the run's earlier
    results, with nothing read: its members, the held-back versions on
    offer, the holds rule A leaves out and the fights its history came
    from; with `screen`, the matchup screen's top sixes too. A few seconds,
    a minute or so with the screen."""
    s = setup(run, slug, seed)
    recs = s["built"]["records"]
    print(f"{s['f']['name']} box {seed} at level {s['lvl']}, {len(s['caught'])} catches, history from "
          f"{', '.join(s['hist_from']) or 'no earlier reading'}")
    for r in recs:
        print(f"  {'held back ' if r['held'] else ''}{r['label']} ({r['area']}): {', '.join(r['moves'])}")
    for h in s["built"]["ruled_out"]:
        print(f"  not offered, not modelled: {h['label']} for {', '.join(h['gained'])}, since {h['used_at']} "
              f"used it as {h['used_as']}")
    if not screen:
        return
    st, keys, boss_keys, _flags = fight_state(s["key"], recs, s["stock"], s["v"], slug)
    sixes, scores, _M, _moves = plteam.screen(st, keys, boss_keys)
    held = {k for k in keys if st["pokemon"][k]["held"]}
    for six, score in zip(sixes, scores):
        print(f"  {score:6.2f}  " + ", ".join(plteam.member_name(st["pokemon"][k]) for k in six))
    inside = sorted({plteam.member_name(st["pokemon"][k]) for six in sixes for k in six if k in held})
    print(f"held-back versions in the screen's top sixes: {', '.join(inside) or 'none'}"
          + ("; the box is read again without them if its chosen six takes one" if inside else ""))


def seed_of(text):
    """A box seed from the command line: a number, or planned."""
    return PLANNED if text == PLANNED else int(text)


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("--run", required=True, help="the run's name: the commit read")
    p.add_argument("--only", help="slugs, comma-separated (story keys or trainer file stems)")
    p.add_argument("--kinds", default="boss", help="boss, ace, or both comma-separated (this milestone: boss)")
    p.add_argument("--boxes", default=",".join(map(str, SEEDS)), help="box seeds, comma-separated")
    p.add_argument("--parallel", type=int, default=2)
    p.add_argument("--procs", type=int, default=14, help="workers for each job")
    p.add_argument("--planned", action="store_true",
                   help="also read the planned-box sample: the planning player's box on " + ", ".join(PLANNED_FIGHTS))
    p.add_argument("--one", nargs=2, metavar=("SLUG", "SEED"),
                   help="read one box (what each job runs); SEED a box seed, or planned for the planned box")
    p.add_argument("--box", nargs=2, metavar=("SLUG", "SEED"),
                   help="print one box as its reading would build it, from the run's earlier results, and read "
                        "nothing")
    p.add_argument("--screen", action="store_true", help="with --box, also run the matchup screen on it")
    p.add_argument("--list", action="store_true", help="print the fights in play order with their levels and places")
    p.add_argument("--store", action="store_true", help="pool the run's readings into the difficulty store")
    p.add_argument("--commit", help="the commit read, for the store's source (default: the run's name)")
    a = p.parse_args(argv)
    if a.one:
        read_box(a.run, a.one[0], seed_of(a.one[1]), a.procs)
    elif a.box:
        dry(a.run, a.box[0], seed_of(a.box[1]), a.screen)
    elif a.list:
        by = {f["slug"]: f for f in fights()}
        for slug in play_order():
            f = by[slug]
            _k, _v, t = met(f, roll(f["split"], 1)[0].species)
            print(f"{f['name']:44} {f['kind'][:12]:12} {f['split']:9} level {level(f, t):3}  "
                  f"place {place(f['slug'])}  {f['slug']}")
    elif a.store:
        store(a.run, a.commit or a.run)
        print(summary(a.run, a.commit or a.run))
    else:
        seeds = tuple(int(s) for s in a.boxes.split(","))
        todo = jobs(set(a.only.split(",")) if a.only else None, tuple(a.kinds.split(",")), seeds, a.planned)
        run_all(a.run, todo, a.parallel, a.procs)


if __name__ == "__main__":
    main()

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
random runs of the encounter simulator for each split, seeds 1 to 3 (Ian
cut five to three for this milestone, 2026-10-07), every catch alive. Box
k's starter is the starter list's k-th (Turtwig, Scorbunny, Piplup), so
every rival team is met by one box; the rest of the run is the seed's own
rolls, the same for every fight of a split. A fight that closes its split (and each Elite Four
fight) takes the box as it stands at the split's end; any other takes
only the catches made before it in walking order (the encounter sidecar's
order, which the OxiDex's Alpha tab follows) and every catch made from an
earlier split's options. Each member is the stage it reaches by the
fight's level, with its whole move pool from its catch, a Hardy nature,
IVs of 15, its first ability, and a gender rolled once from a fixed seed.

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
fights shared among the boxes. Each box's result goes to ~/oxide-trials/goal3/<run>/
as it finishes, so a run stopped midway resumes where it stopped. Jobs run
box by box (every fight's first box, then every fight's second), so a run
stopped early still orders the whole game, on fewer boxes.
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

from ..encounters import alpha
from . import data, fightsim as fs, pboxes, pldifficulty, plniche, plscore, plstudy, plteam, pool

OUT = os.path.expanduser("~/oxide-trials/goal3")
SEEDS = (1, 2, 3)
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


# ---- the boxes ----------------------------------------------------------------------------------------------

@functools.lru_cache(maxsize=None)
def roll(split, seed):
    """[Catch] of one random run's box by the split's end, the starter
    first: plniche.roll's run, with box seed's starter set in turn."""
    ctx = pboxes.context(split)
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
        opts = [o for o in area["options"]
                if rank.get(o.split, 99) <= rank[split] and o.repel is None and not o.requires]
        if not opts:
            continue
        opt = rng.choice(opts)
        sp = pboxes.sim._roll(opt, box, rng, drawn)
        if sp is None:
            continue
        if opt.kind == "legendary":
            drawn.add(sp)
        box.add(sp, area["name"])
        caught.append(Catch(sp, opt.split, area_place(area), area["name"]))
    return tuple(caught)


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


def records(caught, f, lvl, seed):
    """The box's members as the fight reads them, at this level: each with
    a gender rolled once at its catch, which a gendered evolution follows,
    and a coin that settles any choice among evolutions (Wurmple's, Eevee's)."""
    blob = fs.teamscore._blob()["poks"]
    reached = places(f)
    out = []
    for c in caught:
        caught_level = 5 if c.split is None else plniche.catch_level(c.species, c.split)
        tag = f"goal 3 / box {seed} / {c.area}"
        gender = fs.rolled_gender(c.species, tag)
        coin = random.Random(f"evolution / {tag}").randrange(1 << 16)
        final, pool_ = plteam.move_pool(c.species, min(caught_level, lvl), lvl, places=reached, gender=gender,
                                        coin=coin)
        name = plteam.species_name(final)
        ability = (blob.get(name) or {}).get("abilities", {}).get("0")
        out.append(plteam.record(final, lvl, "Hardy", ability, 15, pool_, gender=gender,
                                 line=plniche.line_of(c.species), caught=c.species, caught_level=caught_level,
                                 area=c.area))
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


def read_box(run, slug, seed, procs):
    """One fight on one box: the team search and its winner's reading for a
    boss, the blind reading for an Ace Trainer; its result.json."""
    f = next(x for x in fights() if x["slug"] == slug)
    out_dir = box_dir(run, slug, seed)
    path = os.path.join(out_dir, "result.json")
    if os.path.exists(path):
        with open(path) as fh:
            return json.load(fh)
    os.makedirs(out_dir, exist_ok=True)
    t0 = time.time()
    split = f["split"]
    whole = roll(split, seed)
    caught = cut(whole, f)
    key, v, trainer = met(f, whole[0].species)
    lvl = level(f, trainer)
    recs = records(caught, f, lvl, seed)
    stock = fs.player_items(split)
    prep = plscore.prepare(plscore.parse_fight(key), given_side=recs)
    if prep.get("doubles"):
        raise SystemExit(f"{slug}: a double battle, which goal 3 leaves to the doubles planner")
    st = prep["st"]
    st["item_stock"] = dict(stock)
    keys = [f"p{i}" for i in range(len(recs))]
    boss_keys, flags, _s = prep["variants"][v]
    result = {"fight": f["name"], "slug": slug, "kind": f["kind"], "split": split, "seed": seed, "run": run,
              "starter": whole[0].species, "trainer": trainer["constant"], "key": key, "level": lvl,
              "place": place(slug), "box": [f"{r['species']} ({r['area']})" for r in recs],
              "left_out": len(whole) - len(caught), "items": stock,
              "foes": [f"{st['pokemon'][k]['species']} {st['pokemon'][k]['level']}" for k in boss_keys]}
    if f["kind"] == ACE:
        real, unlucky, faints_to, fainted = plstudy.blind(
            st, keys, boss_keys, flags, real=BLIND[0], unlucky=BLIND[1], procs=procs, seed=11 + 100 * seed,
            cap=lvl, split=split, leave_out=[trainer["tr_id"]])
        result.update(how="blind", real=real, unlucky=unlucky, faints_to=faints_to, fainted=fainted)
    else:
        model = first_box_model(run, slug, seed)
        summary = plteam.search(f"g3-{run}-{slug}-b{seed}", key, recs, stock, os.path.join(out_dir, "search"),
                                procs=procs, prepared=(st, keys, boss_keys, flags), model=model)
        result.update(model=summary.get("model"), reused=model is not None)
        win = summary["winner_keys"]
        real, unlucky, rows = plteam.full_reading(st, boss_keys, flags, win, {}, procs=procs)
        result.update(how="search", winner=summary["winner"],
                      moves={st["pokemon"][k]["species"]: st["moves"][k] for k in win},
                      items={st["pokemon"][k]["species"]: it for k, it in fs.assign_items(st, win).items() if it},
                      real=real, unlucky=unlucky, faints_to=plteam.losing_enemies(rows),
                      fainted=plstudy.fainted(rows))
    result["minutes"] = round((time.time() - t0) / 60, 1)
    with open(path + ".part", "w") as fh:
        json.dump(result, fh, indent=1)
    os.replace(path + ".part", path)
    r, u = result["real"], result["unlucky"]
    print(f"{f['name']} box {seed} ({result['how']}, level {lvl}): real {r['won']:.0%} won, {r['faints']:.2f} "
          f"faints, {r['clean']:.0%} clean; very unlucky {u['won']:.0%}, {u['faints']:.2f}; "
          f"{result['minutes']} minutes", flush=True)
    return result


# ---- the run ------------------------------------------------------------------------------------------------

def jobs(only=None, kinds=("boss", "ace"), seeds=SEEDS):
    """(slug, seed) in run order: every fight's first box, then every
    fight's second, and so on."""
    picked = [f for f in fights() if (not only or f["slug"] in only)
              and ("ace" if f["kind"] == ACE else "boss") in kinds]
    return [(f["slug"], s) for s in seeds for f in picked]


def run_all(run, todo, parallel, procs):
    """The jobs not yet done, `parallel` at a time, each in its own process
    (a team search forks its own workers, which a pool's workers may not),
    so one job's network training on the GPU overlaps another's play-outs."""
    pending = [(slug, s) for slug, s in todo if not os.path.exists(os.path.join(box_dir(run, slug, s),
                                                                                "result.json"))]
    print(f"goal 3, run {run}: {len(todo) - len(pending)} of {len(todo)} boxes done; {len(pending)} to go",
          flush=True)
    running = []
    while pending or running:
        while pending and len(running) < parallel:
            slug, s = pending.pop(0)
            os.makedirs(box_dir(run, slug, s), exist_ok=True)
            log = open(os.path.join(box_dir(run, slug, s), "log.txt"), "a")
            cmd = [sys.executable, "-m", "tools.oxide.balance.plgoal3", "--run", run, "--one", slug, str(s),
                   "--procs", str(procs)]
            running.append((slug, s, subprocess.Popen(cmd, cwd=data.ROOT, stdout=log, stderr=subprocess.STDOUT,
                                                      env=dict(os.environ, PYTHONPATH=".")), log))
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
                print(f"FAILED {slug} box {s} (exit {proc.returncode}); its log.txt says why", flush=True)


# ---- pooling, the store and the summary ---------------------------------------------------------------------

def results(run):
    """{slug: [box results]} of a run, in fight order."""
    out = {}
    for f in fights():
        rs = []
        for s in SEEDS:
            path = os.path.join(box_dir(run, f["slug"], s), "result.json")
            if os.path.exists(path):
                with open(path) as fh:
                    rs.append(json.load(fh))
        if rs:
            out[f["slug"]] = rs
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


def summary(run, commit):
    """The run's readings as Markdown: each fight's pooled numbers and
    difficulty, its boxes' winners, and the lines every box's winner took."""
    by_slug = {f["slug"]: f for f in fights()}
    lines = [f"# Goal 3's readings, run {run} on {commit}", "",
             "| Fight | Split | Level | Boxes | Won | Faints | Clean | Difficulty | Very unlucky won |",
             "|---|---|---|---|---|---|---|---|---|"]
    detail = []
    for slug, rs in results(run).items():
        f = by_slug[slug]
        real, unl = pool_side([r["real"] for r in rs]), pool_side([r["unlucky"] for r in rs])
        lvls = sorted({r["level"] for r in rs})
        lines.append(f"| {f['name']} | {f['split']} | {', '.join(map(str, lvls))} | {len(rs)} | {real['won']:.0%} | "
                     f"{real['faints']:.2f} | {real['clean']:.0%} | {pldifficulty.difficulty(real):.2f} | "
                     f"{unl['won']:.0%} |")
        if f["kind"] != ACE:
            detail.append(f"## {f['name']}")
            for r in rs:
                detail.append(f"- box {r['seed']} ({r['starter']}, {len(r['box'])} members, {r['trainer']}): "
                              f"{', '.join(r['winner'])}; {r['real']['won']:.0%} won, "
                              f"{r['real']['faints']:.2f} faints")
            every = set.intersection(*(set(r["winner"]) for r in rs)) if len(rs) > 1 else set()
            if every:
                detail.append(f"- every box's winner took {', '.join(sorted(every))}")
            detail.append("")
    text = "\n".join(lines + [""] + detail)
    with open(os.path.join(OUT, run, "summary.md"), "w") as fh:
        fh.write(text + "\n")
    return text


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("--run", required=True, help="the run's name: the commit read")
    p.add_argument("--only", help="slugs, comma-separated (story keys or trainer file stems)")
    p.add_argument("--kinds", default="boss", help="boss, ace, or both comma-separated (this milestone: boss)")
    p.add_argument("--boxes", default=",".join(map(str, SEEDS)), help="box seeds, comma-separated")
    p.add_argument("--parallel", type=int, default=2)
    p.add_argument("--procs", type=int, default=14, help="workers for each job")
    p.add_argument("--one", nargs=2, metavar=("SLUG", "SEED"), help="read one box (what each job runs)")
    p.add_argument("--list", action="store_true", help="print the fights with their levels and places")
    p.add_argument("--store", action="store_true", help="pool the run's readings into the difficulty store")
    p.add_argument("--commit", help="the commit read, for the store's source (default: the run's name)")
    a = p.parse_args(argv)
    if a.one:
        read_box(a.run, a.one[0], int(a.one[1]), a.procs)
    elif a.list:
        for f in fights():
            _k, _v, t = met(f, roll(f["split"], 1)[0].species)
            print(f"{f['name']:44} {f['kind'][:12]:12} {f['split']:9} level {level(f, t):3}  "
                  f"place {place(f['slug'])}  {f['slug']}")
    elif a.store:
        store(a.run, a.commit or a.run)
        print(summary(a.run, a.commit or a.run))
    else:
        seeds = tuple(int(s) for s in a.boxes.split(","))
        todo = jobs(set(a.only.split(",")) if a.only else None, tuple(a.kinds.split(",")), seeds)
        run_all(a.run, todo, a.parallel, a.procs)


if __name__ == "__main__":
    main()

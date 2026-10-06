"""Learnset checks 2 and 3 (docs/oxide/learnset-checks.md), by the team
search's matchup screen alone, with no simulated fights.

For every boss fight of goal 3's list (its kept rows, Ace Trainers and the
doubles the screen cannot read left out), on three rolled boxes of the
fight's split, the screen scores every six of the box (plteam.screen):

- Check 2, a niche: for each line, how many bosses of the split it is first
  caught in, or the next, put it in one of the screen's top five sixes (the
  ones the team search labels first), with its top-20 count beside it; and,
  apart, how often the line was in the box but cut before the screen (a box
  over 30 members keeps the 30 with the best summed margins against that
  boss, since the screen cannot score the hundreds of millions of sixes of
  a late box) and how often it was screened but in no top six. The lines no
  boss takes are leads, not verdicts, and the support-like ones among them
  are marked: the screen ranks by damage margins, where walls, stallers and
  support lines score low.
- Check 3, move use: how often each move is among the four the screen picks
  for a member of a top-five six, over every screen; the moves never picked
  though some screened member knew them, and the most picked.

A box comes from the encounter tool's random run to the split (pboxes,
three fixed seeds), each member as caught, at the level its catch comes at
in the split it was caught in (pool.catches), raised to the fight's cap with
its level evolutions and its whole move pool (the last four at capture and
the level-ups by the cap, plteam.move_pool), a neutral nature, IVs of 15
and its first ability. A rival's team is the one the box's starter meets.
Only the level-up lists differ between the two readings: oxide's from the
tree, and learnset v3's from a file named by OXIDE_LEARNSETS
(plteam.mon_data).

    PYTHONPATH=. tools/oxide/capped python3 -m tools.oxide.balance.plniche OUT_DIR V3_JSON
"""
import collections
import json
import multiprocessing as mp
import os
import random
import sys
import time

import numpy as np

from . import data, fightsim as fs, pboxes, plscore, plteam, pool

SEEDS = (1, 2, 3)
CUT = 30            # the most members a screen enumerates the sixes of
TOP = 5             # the top sixes a line counts in (the search labels these)
GOAL3 = os.path.expanduser("~/oxide-trials/scorer-stage2")


# ---- the fights ---------------------------------------------------------------------------------

def boss_fights():
    """[(label, split, ids or story key)] for goal 3's kept rows, Ace
    Trainers left out, from goal3_fights' own list."""
    sys.path.insert(0, GOAL3)
    import goal3_fights as g3
    rows = []
    g3.write = lambda rs, left: rows.extend(rs)
    g3.main()
    by_ids = {tuple(sorted(f["tr_ids"])): f["key"] for f in data.fights()["fights"]}
    out = []
    for r in rows:
        if r.drop or r.kind == "Ace Trainers":
            continue
        story = by_ids.get(tuple(sorted(r.ids)))
        out.append({"label": r.name, "split": r.split, "story": story, "ids": list(r.ids), "kind": r.kind})
    return out


def fight_for(f, starter):
    """The fight key a box with this starter meets: a story fight by its key
    (plscore picks the rival's variant), else the trainer whose constant
    names this starter, else the row's first."""
    if f["story"]:
        return f["story"]
    tag = plscore.STARTER_VARIANT.get(starter)
    ox = data.oxide_trainers()
    pick = next((i for i in f["ids"] if tag and ox[i]["constant"].endswith("_" + tag)), f["ids"][0])
    return f"tr:{pick}"


# ---- the boxes ----------------------------------------------------------------------------------

def line_of(sp):
    pre = pool.pre_evolutions().get(sp) or []
    return pre[-1] if pre else sp


def catch_level(sp, split):
    """The level a catch of this species comes at in this split: the highest
    of its places there, else its lowest anywhere, else 5 (a gift)."""
    here = [lv for s, lv, _how in pool.catches().get(sp, []) if s == split]
    if here:
        return max(here)
    anywhere = [lv for _s, lv, _how in pool.catches().get(sp, [])]
    return min(anywhere) if anywhere else 5


def roll(split, seed):
    """[(species as caught, the split it was caught in)] of one random run's
    box by the split's end (pboxes.random_box, keeping how each came), the
    starter first."""
    ctx = pboxes.context(split)
    rank, values = ctx["rank"], ctx["values"]
    rng = random.Random(seed)
    box = pboxes.sim.Box(ctx["root"], values)
    starter = rng.choice(ctx["starter_src"]["pool"])
    where = ctx["starter_src"].get("capture_area") or "Route 201"
    box.add(starter, where)
    caught = [(starter, None)]
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
        caught.append((sp, opt.split))
    return caught


def records(caught, cap):
    """The box's members as the screen reads them, at the cap."""
    blob = fs.teamscore._blob()["poks"]
    out = []
    for sp, split in caught:
        level = 5 if split is None else catch_level(sp, split)
        # Mt. Coronet's magnetic field is reached in Gardenia's split, as the
        # three-gym run's boxes have it (plteam_test: from the cap of 26).
        final, pool_ = plteam.move_pool(sp, min(level, cap), cap, magnetic=cap >= 26)
        name = plteam.species_name(final)
        ability = (blob.get(name) or {}).get("abilities", {}).get("0")
        out.append(plteam.record(final, cap, "Hardy", ability, 15, pool_, line=line_of(sp), caught=sp,
                                 caught_level=level))
    return out


# ---- one screen ---------------------------------------------------------------------------------

def _screen_job(job):
    """One fight on one box: what the cut and the screen did with each member."""
    label, key, recs = job["label"], job["key"], job["records"]
    try:
        prep = plscore.prepare(plscore.parse_fight(key), given_side=recs)
    except Exception as e:                                   # noqa: BLE001
        return dict(job, records=None, error=f"{type(e).__name__}: {e}")
    if prep.get("doubles"):
        return dict(job, records=None, error="a double battle")
    st = prep["st"]
    keys = [f"p{i}" for i in range(len(recs))]
    boss_keys, _flags, _s = plscore.variant_for(prep, [job["starter"]])
    cut = []
    if len(keys) > CUT:
        mine, theirs, speed = plteam.matchups(st, keys, boss_keys)
        moves = {k: plteam.pick_moves(st, k, boss_keys, mine) for k in keys}
        M = np.clip(plteam.margins(st, keys, boss_keys, moves, mine, theirs, speed), -3, 3)
        order = sorted(range(len(keys)), key=lambda i: -M[i].sum())
        cut = [keys[i] for i in order[CUT:]]
        keys = [keys[i] for i in sorted(order[:CUT])]
    sixes, _scores, _M, moves = plteam.screen(st, keys, boss_keys, top=20)
    lines = {f"p{i}": r["line"] for i, r in enumerate(recs)}
    top5 = {k for s in sixes[:TOP] for k in s}
    top20 = {k for s in sixes for k in s}
    members = []
    for i, r in enumerate(recs):
        k = f"p{i}"
        members.append({"line": r["line"], "species": r["species"], "constant": r["constant"], "pool": r["moves"],
                        "fate": "cut" if k in cut else "top" if k in top5 else "top20" if k in top20 else "out",
                        "picked": moves.get(k) if k in top5 else None, "best": bool(sixes) and k in sixes[0]})
    return {"label": label, "key": key, "split": job["split"], "seed": job["seed"], "learnsets": job["learnsets"],
            "members": members, "top": [[st["pokemon"][k]["species"] for k in s] for s in sixes[:TOP]],
            "foes": [st["pokemon"][e]["species"] for e in boss_keys]}


# ---- the two checks -----------------------------------------------------------------------------

def first_splits():
    """{line: the split it is first caught in}, over every stage's catches."""
    out = {}
    for sp, entries in pool.catches().items():
        line = line_of(sp)
        for s, _lv, _how in entries:
            if line not in out or pool.SPLITS.index(s) < pool.SPLITS.index(out[line]):
                out[line] = s
    return out


def support_like(finals):
    """Whether a line reads as support: in the whole level-up list of the
    stages the boxes reached, at least as many status moves as attacks. (Its
    pool at an early cap says too little: every early list is mostly
    Growl and Leer.)"""
    names = plteam.move_names()
    status = attacks = 0
    for sp in finals:
        for _lvl, const in plteam.mon_data(sp)["learnset"]["by_level"]:
            name = names.get(const)
            if name is None:
                continue
            if fs.move(name).cat == "Status":
                status += 1
            elif fs.play_strength(name, []) > 0:
                attacks += 1
    return status >= attacks


def niche(screens):
    """Check 2 for one learnset: per line, its window's bosses and screens."""
    first = first_splits()
    window = {line: {s, pool.SPLITS[min(pool.SPLITS.index(s) + 1, len(pool.SPLITS) - 1)]}
              for line, s in first.items()}
    per = collections.defaultdict(lambda: {"bosses_met": set(), "bosses_taking": set(), "bosses_top20": set(),
                                           "bosses_best": set(), "screens_in_box": 0, "cut": 0, "out": 0,
                                           "top20": 0, "top": 0, "pools": []})
    for sc in screens:
        for m in sc["members"]:
            line = m["line"]
            if sc["split"] not in window.get(line, ()):
                continue
            d = per[line]
            d["bosses_met"].add(sc["label"])
            d["screens_in_box"] += 1
            d[m["fate"]] += 1
            if m["fate"] == "top":
                d["bosses_taking"].add(sc["label"])
            if m["fate"] in ("top", "top20"):
                d["bosses_top20"].add(sc["label"])
            if m.get("best"):
                d["bosses_best"].add(sc["label"])
            if m["constant"] not in d["pools"]:
                d["pools"].append(m["constant"])
    bosses = collections.defaultdict(set)
    for sc in screens:
        bosses[sc["split"]].add(sc["label"])
    out = {}
    for line, d in per.items():
        in_window = set().union(*(bosses[s] for s in window[line]))
        out[line] = {"name": plteam.species_name(line), "first_split": first[line],
                     "bosses_in_window": len(in_window), "bosses_met": len(d["bosses_met"]),
                     "bosses_taking": len(d["bosses_taking"]), "bosses_top20": len(d["bosses_top20"]),
                     "bosses_best": len(d["bosses_best"]),
                     "screens_in_box": d["screens_in_box"], "cut": d["cut"], "screened_not_top": d["out"] + d["top20"],
                     "top": d["top"], "support_like": support_like(d["pools"])}
    return out


def move_use(screens):
    """Check 3 for one learnset: each move's picks for a top-six member, how
    often a screened member knew it, and how often it came beside a stronger
    attack of its own type in the same pool (the screen picks one attack a
    type, so such a move is outclassed there rather than dead)."""
    picked, known, top_known, outclassed = (collections.Counter() for _ in range(4))
    strength = {}

    def power(name):
        if name not in strength:
            strength[name] = fs.play_strength(name, [])
        return strength[name]
    for sc in screens:
        for m in sc["members"]:
            if m["fate"] == "cut":
                continue
            for name in m["pool"]:
                known[name] += 1
                if m["fate"] == "top":
                    top_known[name] += 1
                mv = fs.move(name)
                if power(name) > 0 and any(o != name and fs.move(o).type == mv.type and power(o) > power(name)
                                           for o in m["pool"]):
                    outclassed[name] += 1
            for name in m["picked"] or []:
                picked[name] += 1
    return {name: {"picked": picked[name], "known_by_screened": known[name], "known_by_top": top_known[name],
                   "outclassed": outclassed[name]}
            for name in known}


# ---- the run ------------------------------------------------------------------------------------

def jobs_for(learnsets, fights):
    jobs = []
    for f in fights:
        for seed in SEEDS:
            caught = roll(f["split"], seed)
            starter = caught[0][0]
            key = fight_for(f, starter)
            kind, k = plscore.parse_fight(key)
            cap = fs.fight_cap(f["split"], k if kind == "story" else None)
            jobs.append({"label": f["label"], "key": key, "split": f["split"], "seed": seed, "starter": starter,
                         "learnsets": learnsets, "records": records(caught, cap)})
    return jobs


def run(out_dir, v3_path, procs=24):
    os.makedirs(out_dir, exist_ok=True)
    t0 = time.time()
    fights = [f for f in boss_fights() if f["split"]]
    result = {"fights": [f["label"] for f in fights], "seeds": list(SEEDS), "cut": CUT, "top": TOP}
    for name, path in (("oxide", None), ("v3", v3_path)):
        if path:
            os.environ["OXIDE_LEARNSETS"] = path
        else:
            os.environ.pop("OXIDE_LEARNSETS", None)
        plteam._OTHER.clear()
        jobs = jobs_for(name, fights)
        with mp.get_context("fork").Pool(procs) as p:
            screens = list(p.imap_unordered(_screen_job, jobs, chunksize=1))
        errors = [(s["label"], s["error"]) for s in screens if s.get("error")]
        good = [s for s in screens if not s.get("error")]
        result[name] = {"screens": len(good), "errors": errors, "niche": niche(good), "moves": move_use(good),
                        "coverage": coverage(good)}
        with open(os.path.join(out_dir, f"screens-{name}.json"), "w") as fh:
            json.dump(good, fh)
        print(f"{name}: {len(good)} screens, {len(errors)} not read, {time.time() - t0:.0f} s", flush=True)
    with open(os.path.join(out_dir, "checks-2-3.json"), "w") as fh:
        json.dump(result, fh, indent=1)
    return result


def coverage(screens):
    """{split: (mean box size, mean members in a top six, mean members cut)}:
    how much of a box the top sixes take, which says how much "taken" means
    there (a small early box's five top sixes hold most of it)."""
    by = collections.defaultdict(list)
    for sc in screens:
        fates = [m["fate"] for m in sc["members"]]
        by[sc["split"]].append((len(fates), fates.count("top"), fates.count("cut")))
    return {s: tuple(round(sum(x[i] for x in v) / len(v), 1) for i in range(3)) for s, v in by.items()}


def summary(result, out_dir):
    """The short Markdown summary beside the JSON."""
    L = ["# Learnset checks 2 and 3: the screen's baseline", "",
         f"The team search's matchup screen (no simulated fights) on {len(result['fights'])} boss fights "
         f"(goal 3's kept rows, Ace Trainers and doubles left out), {len(result['seeds'])} rolled boxes each, "
         f"once with oxide's level-up lists and once with learnset v3's (its proposal's lists, "
         "`docs/oxide/learnset-proposal.tsv` on `balance-learngen-v2`, since that branch never wrote them into "
         f"the species files). A box over {result['cut']} members is cut to the {result['cut']} with the best "
         f"summed margins against that boss first; a line counts as taken when it is in one of the screen's top "
         f"{result['top']} sixes, and \"best\" counts the bosses whose single best six holds it. `plniche.py` holds "
         "the method; `checks-2-3.json` every number.", ""]
    for name in ("oxide", "v3"):
        r = result[name]
        L += [f"Screens read with {name}'s lists: {r['screens']}; not read: {len(r['errors'])}"
              + (f" ({'; '.join(f'{a}: {b}' for a, b in r['errors'][:5])})" if r["errors"] else "") + ".", ""]
    cov = result["oxide"]["coverage"]
    L += ["How much of a box the top five sixes hold, with oxide's lists (a small early box's top sixes hold "
          "most of it, so \"taken\" means little there and \"best\" says more):", "",
          "| Split | Box | In a top six | Cut |", "|---|---|---|---|"]
    L += [f"| {s} | {cov[s][0]} | {cov[s][1]} | {cov[s][2]} |" for s in pool.SPLITS if s in cov]
    L += ["", "## Check 2, a niche", "",
          "A line's window is the split it is first caught in and the next. \"Taken\" counts the window's bosses "
          "that put it in a top six on some box; \"met\" the window's bosses that had it in a box at all. \"Cut\" "
          "and \"screened, not top\" count screens: the cut dropped it before the screen, or the screen read it "
          "and left it out. The two failures mean different things: the cut ranks by summed damage margins, "
          "where walls, stallers and support lines score low.", ""]
    for name in ("oxide", "v3"):
        n = result[name]["niche"]
        never = sorted((d for d in n.values() if d["bosses_met"] and not d["bosses_taking"]),
                       key=lambda d: (-d["bosses_met"], d["name"]))
        every = sorted((d for d in n.values() if d["bosses_met"] >= 3 and d["bosses_taking"] == d["bosses_met"]),
                       key=lambda d: (-d["bosses_best"], -d["bosses_met"], d["name"]))
        L += [f"### {name}: {len(n)} lines met a boss in their window; {len(never)} taken by none, "
              f"{len(every)} by every boss that met them (three or more)", "",
              "Taken by no boss: leads, not verdicts. A star marks a support-like line (at least as many status "
              "moves as attacks in its whole level-up list), which the screen undervalues.", "",
              "| Line | First split | Bosses met | Cut | Screened, not top | Top 20 bosses |",
              "|---|---|---|---|---|---|"]
        for d in never:
            L.append(f"| {d['name']}{' *' if d['support_like'] else ''} | {d['first_split']} | {d['bosses_met']} "
                     f"of {d['bosses_in_window']} | {d['cut']} | {d['screened_not_top']} | {d['bosses_top20']} |")
        L += ["", "Taken by every boss that met them, with the bosses whose best six holds it:", "",
              "| Line | First split | Bosses taking | Best six |", "|---|---|---|---|"]
        for d in every:
            L.append(f"| {d['name']} | {d['first_split']} | {d['bosses_taking']} of {d['bosses_met']} met "
                     f"| {d['bosses_best']} |")
        L.append("")
    L += ["## Check 3, move use", "",
          "Picks count the four moves the screen gives each member of a top six, over every screen; \"known\" "
          "counts the screened members whose pool had the move. The screen takes one attack of each type, so a "
          "move \"outclassed\" in a pool (beside a stronger attack of its own type) is passed over there rather "
          "than dead; a never-picked move known mostly where it is outclassed says the pools give it nothing to "
          "do, not that the move is bad.", ""]
    for name in ("oxide", "v3"):
        mv = result[name]["moves"]
        top = sorted(mv.items(), key=lambda kv: -kv[1]["picked"])[:20]
        dead = sorted(((k, d) for k, d in mv.items() if not d["picked"]), key=lambda kv: -kv[1]["known_by_screened"])
        L += [f"### {name}: {len(mv)} moves known by a screened member; {len(dead)} never picked", "",
              "Most picked:", "", "| Move | Picks | Known by a top-six member | Known by a screened member |",
              "|---|---|---|---|"]
        L += [f"| {k} | {d['picked']} | {d['known_by_top']} | {d['known_by_screened']} |" for k, d in top]
        L += ["", "Never picked, most known first (the first 40):", "",
              "| Move | Known by a screened member | Of those, outclassed |", "|---|---|---|"]
        L += [f"| {k} | {d['known_by_screened']} | {d['outclassed']} |" for k, d in dead[:40]]
        L.append("")
    o, v = result["oxide"]["niche"], result["v3"]["niche"]
    diff = [line for line in sorted(set(o) | set(v), key=lambda x: (o.get(x) or v.get(x))["name"])
            if (o.get(line, {}).get("bosses_taking"), o.get(line, {}).get("bosses_best"))
            != (v.get(line, {}).get("bosses_taking"), v.get(line, {}).get("bosses_best"))]
    never = {name: sum(1 for d in result[name]["moves"].values() if not d["picked"]) for name in ("oxide", "v3")}
    L += ["## oxide against v3", "",
          f"v3 changes what the screen does for {len(diff)} of the lines met: their bosses taking and best six, "
          f"oxide then v3. Never-picked moves: {never['oxide']} with oxide's lists, {never['v3']} with v3's.", "",
          "| Line | First split | Bosses met | Taking | Best six |", "|---|---|---|---|---|"]
    for line in diff:
        a, b = o.get(line, {}), v.get(line, {})
        L.append(f"| {(a or b)['name']} | {(a or b)['first_split']} | {(a or b)['bosses_met']} "
                 f"| {a.get('bosses_taking', '-')} then {b.get('bosses_taking', '-')} "
                 f"| {a.get('bosses_best', '-')} then {b.get('bosses_best', '-')} |")
    L.append("")
    with open(os.path.join(out_dir, "checks-2-3.md"), "w") as fh:
        fh.write("\n".join(L))


if __name__ == "__main__":
    res = run(sys.argv[1], sys.argv[2], procs=int(os.environ.get("NICHE_PROCS", 24)))
    summary(res, sys.argv[1])

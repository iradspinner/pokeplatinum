"""The Kaizo team study's worked examples, read by the scorer (the Overseer's
request of 2026-10-03; the study's notes in
~/oxide-trials/kaizo-teams/out/examples.md). Each example is a trainer file
outside res/ (out/examples/<stem>.json), the trainer's own file with only
its party changed; it is built by the build's own party builder
(calc_trainers), genders from the file, and never copied into res/.

How each is read, by Ian's rules (bosses with a planned six, ordinary
trainers blind from a realistic box; every reading 75 fights at real odds
and 25 very unlucky, by the play-out planner at budget 64):

- blind (taylor, catherine, grunt): each fight draws a six at random from
  the box the run would have there, every member with four fixed moves by
  the scorer's rule over its whole pool, as goal 2's records are made: the
  player brings what it carries, not a six chosen for this trainer.
- section (the grunt's gauntlet): the four grunts of the Eterna building's
  1F and 2F in a row, the example first and the other three as res/ has
  them, one random six from the box carrying its HP, status, PP and items
  from fight to fight with no healing (plplan.CARRY).
- search (gardenia, maylene): the team search (plteam.search) and Ian's
  standard reading of its winner.

The boxes: Taylor (Route 204 north, before Mars 1) the hand run's box at
Roark raised to the interim cap of 19; Catherine goal 2's Fantina box at
33; the grunt goal 2's Jupiter 1 box at 27; Gardenia the hand run's box at
26; Maylene goal 2's Fantina box with every member raised to 38, level
evolutions taken, no new captures (a real box at 38 would be stronger).

    PYTHONPATH=. tools/oxide/capped python3 -m tools.oxide.balance.plstudy taylor catherine grunt section
"""
import json
import os
import random
import sys
import time

from ..encounters import calc_trainers
from . import data, fightsim as fs, plgoal2, plplan, plscore, plstep3, plteam, plteam_test

EXAMPLES = os.path.expanduser("~/oxide-trials/kaizo-teams/out/examples")
OUT = os.path.join(plteam.ROOT, "study")
RES = os.path.join(data.ROOT, "res", "trainers", "data")
SECTION = ["galactic_grunt_team_galactic_eterna_building_1f_1", "galactic_grunt_team_galactic_eterna_building_1f_2",
           "galactic_grunt_team_galactic_eterna_building_2f_1", "galactic_grunt_team_galactic_eterna_building_2f_2"]


NOTES = []      # what the readings did that the files alone would not


def trainer_party(path):
    """(party, AI flags) for a trainer file: the build's party builder, and
    each member's gender as the game gives it. The packer (trainerproc.c)
    gives a party items only when its first member's "item" is a string; a
    file whose first member has null while another holds an item would lose
    every item in the built game, so it is read with "ITEM_NONE" there, as
    the study means it, and the reading says so."""
    with open(path) as fh:
        tr = json.load(fh)
    stem = os.path.basename(path)[:-len(".json")]
    party = tr.get("party") or []
    if party and not isinstance(party[0].get("item"), str) and any(m.get("item") for m in party):
        tr = dict(tr, party=[dict(party[0], item="ITEM_NONE")] + party[1:])
        NOTES.append(f"{stem}: its first member's item is null, so the built game would drop every item; "
                     "read with ITEM_NONE there, as the study means it")
    sets = calc_trainers.build_trainer(data.ROOT, stem, tr)
    t = {"stem": stem, "party": [data._mon(sp, s) for sp, s in sets]}
    return plscore.with_genders(t, tr), sets[0][1].get("ai")


def prepare(paths, split, cap, recs, stock):
    """(st, box keys, [(boss keys, flags)] per trainer) for these trainer
    files against this box."""
    parties = [trainer_party(p) for p in paths]
    st = fs.prepare(split, [p for p, _f in parties], None, cap=cap, given_side=recs)
    st["item_stock"] = dict(stock)
    keys = [f"p{i}" for i in range(len(recs))]
    return st, keys, [(st["bosses"][i], f) for i, (_p, f) in enumerate(parties)]


def fixed(recs):
    """Each member with four moves by the scorer's rule over its whole pool
    (fightsim.player_moves), the empty slots filled with its latest moves,
    as goal 2's records are made."""
    tiers, blob = fs.status_tiers(), fs.teamscore._blob()
    out = []
    for r in recs:
        cand = list(r["moves"])
        mv = fs.player_moves({}, cand, tiers, blob["poks"].get(r["species"], {}).get("types") or [])
        for m in reversed(cand):
            if len(mv) >= 4:
                break
            if m not in mv:
                mv.append(m)
        out.append(dict(r, moves=mv))
    return out


def goal2_records(fight):
    """Goal 2's box at this fight, with its records' own moves and genders."""
    with open(plgoal2.BOXES) as fh:
        recs = json.load(fh)[fight]
    return [plteam.record(r["constant"], r["level"], r["nature"], r["ability"], r["ivs"], r["moves"],
                          gender=r["gender"]) for r in recs]


def raised(fight, level):
    """Goal 2's box at this fight with every member raised to `level`, its
    level evolutions taken (the run's holds kept), with whole move pools."""
    with open(plgoal2.BOXES) as fh:
        recs = json.load(fh)[fight]
    out = []
    for r in recs:
        final, pool_ = plteam.move_pool(r["base"], r["caught_level"], level, plgoal2.HOLDS, magnetic=True)
        out.append(plteam.record(final, level, r["nature"], r["ability"], r["ivs"], pool_, gender=r["gender"]))
    return out


def stock(boosters):
    return {"boosters": dict(boosters), "Leftovers": 0, "Sitrus Berry": 0}


# example: (trainer file, split, cap, box records, stock, kind)
def examples():
    roark, gardenia = plstep3.FIGHTS["roark"], plstep3.FIGHTS["gardenia"]
    path = lambda stem: os.path.join(EXAMPLES, stem + ".json")    # noqa: E731
    return {
        "taylor": (path("aroma_lady_taylor"), "Gardenia", 19,
                   lambda: fixed(plteam_test.box(plstep3.ROARK, 19)), stock(roark["boosters"]), "blind"),
        "catherine": (path("ace_trainer_catherine"), "Fantina", 33,
                      lambda: goal2_records("fantina"), stock(plgoal2.FIGHTS["fantina"][2]), "blind"),
        "grunt": (path(SECTION[0]), "Fantina", 27,
                  lambda: goal2_records("jupiter_1"), stock(plgoal2.FIGHTS["jupiter_1"][2]), "blind"),
        "section": (None, "Fantina", 27,
                    lambda: goal2_records("jupiter_1"), stock(plgoal2.FIGHTS["jupiter_1"][2]), "section"),
        "gardenia": (path("leader_gardenia"), "Gardenia", 26,
                     lambda: plteam_test.box(plstep3.GARDENIA, 26), stock(gardenia["boosters"]), "search"),
        "maylene": (path("leader_maylene"), "Maylene", 38,
                    lambda: raised("fantina", 38), stock(plgoal2.FIGHTS["fantina"][2]), "search"),
    }


def pooled(tally):
    """A tally's three numbers over every fight it holds, whatever six."""
    rows = [r for rs in tally.rows.values() for r in rs]
    n = max(1, len(rows))
    return {"fights": len(rows), "won": sum(r[0] for r in rows) / n, "faints": sum(r[1] for r in rows) / n,
            "clean": sum(r[2] for r in rows) / n}


def draw(rng, keys, n):
    """n different sixes drawn at random from the box."""
    out = []
    while len(out) < n:
        s = tuple(sorted(rng.sample(keys, min(6, len(keys))), key=keys.index))
        if s not in out:
            out.append(s)
    return out


def blind(st, keys, boss_keys, flags, real=75, unlucky=25, procs=None, seed=11):
    """The blind reading: each fight with its own random six."""
    rng = random.Random(seed)
    a = plteam.read(st, boss_keys, flags, draw(rng, keys, real), 1, {}, "real", seed0=seed, procs=procs)
    b = plteam.read(st, boss_keys, flags, draw(rng, keys, unlucky), 1, {}, "unlucky", seed0=seed + 1, procs=procs)
    rows = [r for rs in a.rows.values() for r in rs]
    return pooled(a), pooled(b), plteam.losing_enemies(rows)


_JOB = {}


def _section_job(args):
    """One run through the section: the same six from fight to fight, its
    state carried, stopping at a loss."""
    six, seed, luck = args
    j = _JOB
    plplan.CARRY = None
    faints, won, r = [], True, None
    try:
        for v, (boss_keys, flags) in enumerate(j["fights"]):
            lead, _vals = plplan.Planner(0).lead(j["st"], list(six), boss_keys, flags)
            r = plplan.play(j["st"], list(six), boss_keys, flags, lead, seed * 10 + v, {}, luck)
            faints += [tuple(x) for x in r["faints"]]
            plplan.CARRY = r["carry"]
            if not r["won"]:
                won = False
                break
    finally:
        plplan.CARRY = None
    deaths = sum(1 for c in r["carry"] if c[0] <= 0)
    return won, deaths, won and deaths == 0, faints


def section(st, keys, fights, real=75, unlucky=25, procs=None, seed=13):
    """The gauntlet section read blind: each run one random six through
    every fight in a row."""
    _JOB.update(st=st, fights=fights)
    rng = random.Random(seed)
    out = {}
    for luck, n, s0 in (("real", real, seed), ("unlucky", unlucky, seed + 1)):
        jobs = [(six, s0 * 1000 + i, luck) for i, six in enumerate(draw(rng, keys, n))]
        with plplan.fork_pool(procs or plplan.pool_size()) as pool_:
            rows = list(pool_.imap_unordered(_section_job, jobs, chunksize=1))
        out[luck] = {"fights": len(rows), "won": sum(r[0] for r in rows) / len(rows),
                     "faints": sum(r[1] for r in rows) / len(rows), "clean": sum(r[2] for r in rows) / len(rows)}
        if luck == "real":
            out["faints_to"] = plteam.losing_enemies([(w, d, c, f) for w, d, c, f in rows])
    return out


def run(name, procs=12):
    path, split, cap, box_fn, stk, kind = examples()[name]
    os.makedirs(OUT, exist_ok=True)
    t0 = time.time()
    recs = box_fn()
    result = {"example": name, "split": split, "cap": cap, "kind": kind, "box": [r["species"] for r in recs]}
    if kind == "section":
        paths = [os.path.join(EXAMPLES, SECTION[0] + ".json")] + [os.path.join(RES, s + ".json") for s in SECTION[1:]]
        st, keys, fights = prepare(paths, split, cap, recs, stk)
        result["trainers"] = [[st["pokemon"][k]["species"] + f" {st['pokemon'][k]['level']}" for k in bk]
                              for bk, _f in fights]
        out = section(st, keys, fights, procs=procs)
        result.update(real=out["real"], unlucky=out["unlucky"], faints_to=out["faints_to"])
    else:
        st, keys, fights = prepare([path], split, cap, recs, stk)
        boss_keys, flags = fights[0]
        result["trainer"] = [st["pokemon"][k]["species"] + f" {st['pokemon'][k]['level']}" for k in boss_keys]
        if kind == "blind":
            real, unlucky, faints_to = blind(st, keys, boss_keys, flags, procs=procs)
        else:
            out_dir = os.path.join(OUT, name)
            summary = plteam.search(f"study_{name}", None, recs, stk, out_dir, procs=procs,
                                    prepared=(st, keys, boss_keys, flags))
            names = {k: st["pokemon"][k]["species"] for k in keys}
            by_name = {v: k for k, v in names.items()}
            win = [by_name[n] for n in summary["winner"]]
            real, unlucky, rows = plteam.full_reading(st, boss_keys, flags, win, {}, procs=procs)
            faints_to = plteam.losing_enemies(rows)
            result["winner"] = summary["winner"]
        result.update(real=real, unlucky=unlucky, faints_to=faints_to)
    result["notes"] = sorted(set(NOTES))
    result["minutes"] = round((time.time() - t0) / 60, 1)
    with open(os.path.join(OUT, name + ".json"), "w") as fh:
        json.dump(result, fh, indent=1)
    r, u = result["real"], result["unlucky"]
    print(f"{name} ({kind}, {split} at {cap}): real {r['won']:.0%} won, {r['faints']:.2f} faints, "
          f"{r['clean']:.0%} clean; very unlucky {u['won']:.0%}, {u['faints']:.2f}, {u['clean']:.0%}; "
          f"faints to {result['faints_to'][:4]}; {result['minutes']} minutes", flush=True)
    return result


if __name__ == "__main__":
    for example in sys.argv[1:]:
        run(example)

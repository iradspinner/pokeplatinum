"""The blind and gauntlet readings the scorer uses, from the Kaizo team
study's worked examples (the Overseer's request of 2026-10-03).

- blind: each fight draws a six at random from the stronger half of the box
  the run would have there, never a member held below the cap
  (plteam.blind_pool, Ian, 2026-10-04), every member with its own fixed
  moves: the player brings what it carries, not a six chosen for this
  trainer. Goal 3 reads its ordinary trainers this way (plgoal3).
- section: a gauntlet section's trainers in a row, one random six from the
  box's stronger half carrying its HP, status, PP and items from fight to
  fight with no healing (plplan.CARRY).

prepare() builds a fight from trainer files, the way the examples were
read; test_plfixes reads with it. The worked examples themselves, their
command line and the Kaizo anchor (which rested on plgoal2.py, plkaizo.py
and kaizoteams.py) were retired with those modules on 2026-10-13; their
readings are in ~/oxide-trials/scorer-stage2/study.
"""
import collections
import json
import os
import random

from ..encounters import calc_trainers
from . import calc, data, fightsim as fs, plplan, plscore, plteam

RES = os.path.join(data.ROOT, "res", "trainers", "data")


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
    files against this box. The field starts in the map weather of the
    trainers the files rebuild, matched by file name, as a story fight's
    does (the comb's Roark was read with no sand until 2026-10-06), and in
    the game's permanent Trick Room when one of them is on its list."""
    parties = [trainer_party(p) for p in paths]
    stems = [os.path.basename(p)[:-len(".json")] for p in paths]
    weather = calc.fight_weather(trainer_ids(stems))
    trick_room = fs.trick_room_for(["TRAINER_" + s.upper() for s in stems])
    st = fs.prepare(split, [p for p, _f in parties], weather, trick_room, cap=cap, given_side=recs,
                    terrain=calc.fight_terrain(trainer_ids(stems)))
    st["item_stock"] = dict(stock)
    keys = [f"p{i}" for i in range(len(recs))]
    return st, keys, [(st["bosses"][i], f) for i, (_p, f) in enumerate(parties)]


def fixed(recs):
    """Each member with four moves by the scorer's rule over its whole pool
    (fightsim.player_moves), the empty slots filled with its latest moves,
    as goal 2's records are made."""
    tiers, blob = fs.status_tiers(), fs.calc.blob()
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


def stock(boosters):
    return {"boosters": dict(boosters), "Leftovers": 0, "Sitrus Berry": 0}


def pooled(tally):
    """A tally's three numbers over every fight it holds, whatever six."""
    rows = [r for rs in tally.rows.values() for r in rs]
    n = max(1, len(rows))
    return {"fights": len(rows), "won": sum(r[0] for r in rows) / n, "faints": sum(r[1] for r in rows) / n,
            "clean": sum(r[2] for r in rows) / n}


def draw(rng, keys, n):
    """n sixes drawn at random from the pool, one for each fight, each
    draw on its own: a small pool repeats a six, as a player can. (Drawing
    n different sixes looped forever once the stronger half of a box left
    fewer than n of them: eight members make 28.)"""
    return [tuple(sorted(rng.sample(keys, min(6, len(keys))), key=keys.index)) for _ in range(n)]


def read_drawn(st, boss_keys, flags, sixes, luck, seed0, procs):
    """The drawn sixes read one fight per draw: a six drawn k times is read
    on k fights in one call, so that its fights take different seeds
    (plteam.read seeds a six by its members and the fights it has had)."""
    counts = collections.Counter(sixes)
    tally = None
    for k in sorted(set(counts.values())):
        tally = plteam.read(st, boss_keys, flags, [s for s, c in counts.items() if c == k], k, {}, luck,
                            seed0=seed0, procs=procs, tally=tally)
    return tally


def blind(st, keys, boss_keys, flags, real=75, unlucky=25, procs=None, seed=11, cap=None, split=None,
          leave_out=()):
    """The blind reading: each fight with its own random six from the box's
    stronger half, never a member held below the cap (plteam.blind_pool,
    Ian, 2026-10-04)."""
    rng = random.Random(seed)
    keys = plteam.blind_pool(st, keys, split, cap, leave_out)
    a = read_drawn(st, boss_keys, flags, draw(rng, keys, real), "real", seed, procs)
    b = read_drawn(st, boss_keys, flags, draw(rng, keys, unlucky), "unlucky", seed + 1, procs)
    rows = [r for rs in a.rows.values() for r in rs]
    return pooled(a), pooled(b), plteam.losing_enemies(rows), fainted(rows)


def fainted(rows):
    """Which of the player's Pokemon fainted, most first, over a reading's
    rows' (fainted, enemy out) pairs."""
    tally = {}
    for _w, _d, _c, faints in rows:
        for mine, _foe in faints:
            tally[mine] = tally.get(mine, 0) + 1
    return sorted(tally.items(), key=lambda kv: -kv[1])


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


def section(st, keys, fights, real=75, unlucky=25, procs=None, seed=13, cap=None, split=None,
            leave_out=()):
    """The gauntlet section read blind: each run one random six from the
    box's stronger half (as blind's) through every fight in a row."""
    _JOB.update(st=st, fights=fights)
    rng = random.Random(seed)
    keys = plteam.blind_pool(st, keys, split, cap, leave_out)
    out = {}
    for luck, n, s0 in (("real", real, seed), ("unlucky", unlucky, seed + 1)):
        jobs = [(six, s0 * 1000 + i, luck) for i, six in enumerate(draw(rng, keys, n))]
        with plplan.fork_pool(procs or plplan.pool_size()) as pool_:
            rows = list(pool_.imap_unordered(_section_job, jobs, chunksize=1))
        out[luck] = {"fights": len(rows), "won": sum(r[0] for r in rows) / len(rows),
                     "faints": sum(r[1] for r in rows) / len(rows), "clean": sum(r[2] for r in rows) / len(rows)}
        if luck == "real":
            out["faints_to"] = plteam.losing_enemies([(w, d, c, f) for w, d, c, f in rows])
            out["fainted"] = fainted(rows)
    return out


def trainer_ids(stems):
    """The res/ trainer ids of these file stems (an example keeps the stem
    of the trainer it rebuilds), to keep them out of the blind draw's panel."""
    by_stem = {t["stem"]: k for k, t in data.oxide_trainers().items()}
    return [by_stem[s] for s in stems if s in by_stem]

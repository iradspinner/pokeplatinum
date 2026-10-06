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
  the stronger half of the box the run would have there, never a member
  held below the cap (plteam.blind_pool, Ian, 2026-10-04), every member
  with its own fixed moves: the player brings what it carries, not a six
  chosen for this trainer.
- section (the grunt's gauntlet): the four grunts of the Eterna building's
  1F and 2F in a row, the example first and the other three as res/ has
  them, one random six from the box's stronger half carrying its HP,
  status, PP and items from fight to fight with no healing (plplan.CARRY).
- search (gardenia, maylene): the team search (plteam.search) and Ian's
  standard reading of its winner.

The boxes: Taylor (Route 204 north, before Mars 1) the hand run's box at
Roark raised to the interim cap of 19; Catherine goal 2's Fantina box at
33; the grunt goal 2's Jupiter 1 box at 27; Gardenia the hand run's box at
26; Maylene goal 2's Fantina box with every member raised to 38, level
evolutions taken, no new captures (a real box at 38 would be stronger).

    PYTHONPATH=. tools/oxide/capped python3 -m tools.oxide.balance.plstudy taylor catherine grunt section
"""
import collections
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


# ---- the Kaizo anchor (Ian's yes, 2026-10-03): Kaizo's bosses of its first
# three splits on goal 2's boxes, a 10/10 reading in the scorer's numbers.
# Kaizo's Mars is a double, which the team search cannot read, so it is left
# out. Levels move from Kaizo's cap to the cap in force here as the Kaizo
# reader moves them (kaizoteams.oxide_level); Kaizo's own weathers stay.
# Kaizo's data gives no genders, so its Pokemon read as genderless, which
# only Attract and Cute Charm notice (none of the six uses either).

def kaizo_prepare(label, variant, split, cap, recs, stk, by_ace=False):
    """(st, box keys, [(boss keys, flags)]) for one of Kaizo's bosses."""
    from . import kaizoteams as K, plkaizo as P
    tr = K.load_trainers()
    caps = K.kaizo_caps(tr)
    rec = {(t["ksplit"], t["trainer"]): t for t in reversed(tr)}
    f = next(x for x in K.fights(tr, caps) if x["label"] == label and x.get("kind") == "boss")
    members = [rec[(f["ksplit"], n)] for n in f["names"]]
    notes = {k: set() for k in ("species", "moves", "abilities", "weather_kept")}
    # A mini-boss (by_ace) maps its own ace to the cap in force, which is
    # Oxide's interim cap at that fight's ace; Kaizo has no interim caps, so
    # its split cap would leave Barry 2 and Jupiter far under the box.
    kcap = max(m["level"] for m in members[variant]["team"]) if by_ace else caps[f["home"]]
    ps, _doubles = P.parties(f, members, lambda lv: K.oxide_level(lv, kcap, cap), notes)
    st = fs.prepare(split, [ps[variant]], f["weather"], f["trick_room"], cap=cap, given_side=recs)
    st["item_stock"] = dict(stk)
    for k, v in notes.items():
        if v:
            NOTES.append(f"Kaizo {label}: {k} {sorted(v)}")
    keys = [f"p{i}" for i in range(len(recs))]
    return st, keys, [(st["bosses"][0], P.flags_of(members))]


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
        # The Kaizo anchor: (Kaizo's label, its variant a Piplup player meets).
        "kaizo_barry_2": (("Barry #2", 1, True), "Roark", 11, lambda: plgoal2.box("barry_2"), stock({}), "kaizo"),
        "kaizo_roark": (("Leader Roark", 0), "Roark", 16,
                        lambda: plteam_test.box(plstep3.ROARK, 16), stock(roark["boosters"]), "kaizo"),
        "kaizo_gardenia": (("Leader Gardenia", 0), "Gardenia", 26,
                           lambda: plteam_test.box(plstep3.GARDENIA, 26), stock(gardenia["boosters"]), "kaizo"),
        "kaizo_jupiter": (("Commander Jupiter", 0, True), "Fantina", 27,
                          lambda: plgoal2.box("jupiter_1"), stock(plgoal2.FIGHTS["jupiter_1"][2]), "kaizo"),
        "kaizo_fantina_gym": (("Leader Fantina ?", 0), "Fantina", 33,
                              lambda: plgoal2.box("fantina"), stock(plgoal2.FIGHTS["fantina"][2]), "kaizo"),
        "kaizo_fantina": (("Leader Fantina", 0), "Fantina", 33,
                          lambda: plgoal2.box("fantina"), stock(plgoal2.FIGHTS["fantina"][2]), "kaizo"),
    } | comb_roark(roark)


# The study's comb of Roark's split (the Overseer, 2026-10-06), read from
# out/comb/ as the examples are. Ordinary trainers blind at the cap in force
# when met: 11 before Barry 2, on goal 2's Barry 2 box with its own moves,
# and 16 from Route 203 on, on the hand run's Roark box with the scorer's
# moves. Roark at 16 and Barry 2 at 11 (a Piplup player's file) by the team
# search on the boxes goal 2 and the Kaizo anchor read them on. The Jubilife
# tag pair, a double in Gardenia's split, waits for doubles.
COMB = os.path.expanduser("~/oxide-trials/kaizo-teams/out/comb")
COMB_BEFORE_BARRY_2 = ["youngster_tristan", "youngster_logan", "lass_natalie", "school_kid_harrison",
                       "school_kid_christine"]
COMB_AT_16 = ["youngster_michael", "lass_madeline", "lass_kaitlin", "youngster_dallas", "youngster_sebastian",
              "camper_curtis", "picnicker_diana", "worker_colin", "worker_mason", "youngster_jonathon",
              "youngster_darius"]


def comb_roark(roark):
    path = lambda stem: os.path.join(COMB, stem + ".json")    # noqa: E731
    out = {f"comb_{s}": (path(s), "Roark", 11, lambda: goal2_records("barry_2"), stock({}), "blind")
           for s in COMB_BEFORE_BARRY_2}
    out |= {f"comb_{s}": (path(s), "Roark", 16, lambda: fixed(plteam_test.box(plstep3.ROARK, 16)),
                          stock(roark["boosters"]), "blind") for s in COMB_AT_16}
    out["comb_leader_roark"] = (path("leader_roark"), "Roark", 16, lambda: plteam_test.box(plstep3.ROARK, 16),
                                stock(roark["boosters"]), "search")
    out["comb_rival_route_203_piplup"] = (path("rival_route_203_piplup"), "Roark", 11,
                                          lambda: plgoal2.box("barry_2"), stock({}), "search")
    return out


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


def run(name, procs=12, without=()):
    path, split, cap, box_fn, stk, kind = examples()[name]
    os.makedirs(OUT, exist_ok=True)
    t0 = time.time()
    # `without`: members left out of the box (as a variant reading, saved
    # under its own name), such as the run's level-6 Starly.
    recs = [r for r in box_fn() if r["species"] not in without]
    result = {"example": name, "split": split, "cap": cap, "kind": kind, "box": [r["species"] for r in recs]}
    if kind == "section":
        paths = [os.path.join(EXAMPLES, SECTION[0] + ".json")] + [os.path.join(RES, s + ".json") for s in SECTION[1:]]
        st, keys, fights = prepare(paths, split, cap, recs, stk)
        result["trainers"] = [[st["pokemon"][k]["species"] + f" {st['pokemon'][k]['level']}" for k in bk]
                              for bk, _f in fights]
        out = section(st, keys, fights, procs=procs, cap=cap, split=split, leave_out=trainer_ids(SECTION))
        result.update(real=out["real"], unlucky=out["unlucky"], faints_to=out["faints_to"], fainted=out["fainted"])
    else:
        st, keys, fights = (kaizo_prepare(*path[:2], split, cap, recs, stk, *path[2:]) if kind == "kaizo"
                            else prepare([path], split, cap, recs, stk))
        boss_keys, flags = fights[0]
        result["trainer"] = [st["pokemon"][k]["species"] + f" {st['pokemon'][k]['level']}" for k in boss_keys]
        if kind == "blind":
            real, unlucky, faints_to, result["fainted"] = blind(
                st, keys, boss_keys, flags, procs=procs, cap=cap, split=split,
                leave_out=trainer_ids([os.path.basename(path)[:-5]]))
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
    if without:
        name = f"{name}-without-{'-'.join(without)}"
        result["example"], result["without"] = name, list(without)
    with open(os.path.join(OUT, name + ".json"), "w") as fh:
        json.dump(result, fh, indent=1)
    r, u = result["real"], result["unlucky"]
    print(f"{name} ({kind}, {split} at {cap}): real {r['won']:.0%} won, {r['faints']:.2f} faints, "
          f"{r['clean']:.0%} clean; very unlucky {u['won']:.0%}, {u['faints']:.2f}, {u['clean']:.0%}; "
          f"faints to {result['faints_to'][:4]}; {result['minutes']} minutes", flush=True)
    return result


if __name__ == "__main__":
    for example in sys.argv[1:]:
        # "taylor:Starly" reads Taylor with Starly left out of the box.
        example, _sep, left = example.partition(":")
        run(example, procs=int(os.environ.get("STUDY_PROCS", 12)), without=tuple(x for x in left.split(",") if x))

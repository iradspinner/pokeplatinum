"""The team search: a boss's six and moves chosen by the scorer itself (Ian,
2026-10-02; the plan in docs/oxide/trainer-scoring-handoff.md, "The team
search: plan and costs").

1. Screen, with no simulated fights. Every box member's whole move pool is
   prepared against the boss, so the damage calculator's rows give each
   member's expected damage on each enemy and back, with speed. Each member
   gets four moves picked against this fight, and every six is scored by how
   well it answers every enemy (a member that needs fewer hits to knock an
   enemy out than the enemy needs for it, with who moves first), with the
   least overlap. The top sixes, kept apart from one another, go on.
2. Labels. The play-out planner labels the screen's top sixes (a tenth of a
   round, budget 64; the spread round from the network's own play helped
   once and hurt twice, at Gardenia and at Mars 1 at 19, so it is left out),
   and two networks train from scratch on everything but this fight's old
   labels plus these.
3. Race, on the network planner, by Ian's member ratings: sixes are drawn by
   member weights, each read on a few fights, and the weights move toward
   the members of the best sixes (the cross-entropy method); then the best
   full sixes race by halving, which settles pairs that work only together.
4. Finalists: two or three sixes, 75 fights at real odds and 25 very unlucky.
5. Diagnosis: the play-out planner reads the winner on 25 fights. If the
   network falls short of it on the same six, the gap is training: more
   labels on that six, and read again. If the gap stays, the network is not
   trusted for this fight: the play-out planner reads the top three on 25
   fights each and the best of them in full.

A six's score in the race is Ian's order made one number: its win share
first, its faints second (a win outweighs any number of faints the race can
see, since each fight's faints count a tenth of a win).

    PYTHONPATH=. python3 -m tools.oxide.balance.plteam_test   # the first test
"""
import itertools
import json
import math
import os
import random
import subprocess
import zlib

from . import plthreads  # noqa: F401  (one numpy thread per process, before numpy loads)
import numpy as np  # noqa: E402

from . import fightsim as fs, pldata, plfeat, plplan, plscore, pool  # noqa: E402

ROOT = os.path.expanduser("~/oxide-trials/scorer-stage2")
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
MOVES = None


def move_names():
    global MOVES
    if MOVES is None:
        MOVES = pool._move_names()
    return MOVES


# ---- a box member's moves -------------------------------------------------------------------------

def mon_data(sp):
    with open(os.path.join(REPO, "res/pokemon", sp[len("SPECIES_"):].lower(), "data.json")) as fh:
        return json.load(fh)


def species_name(sp):
    blob = fs.teamscore._blob()
    n = sp[len("SPECIES_"):].replace("_", " ").title().replace(" ", "-")
    return n if n in blob["poks"] else n.replace("-", "")


def chain(sp, caught, cap, holds=None, magnetic=False):
    """[(species, from level)] as a member levels from `caught` to `cap`:
    level evolutions (each delayed to its hold, if any), evolving by knowing
    a move once the move is learned, and by a magnetic field where the run
    has reached one; stones, trades and friendship are not taken."""
    holds = holds or {}
    path, cur, lvl = [(sp, caught)], sp, caught
    while True:
        nxt = None
        known = {mv for l, mv in mon_data(cur)["learnset"]["by_level"] if l <= cap}
        for e in mon_data(cur).get("evolutions") or []:
            kind, target = e[0], e[-1]
            if kind == "EVO_LEVEL" and isinstance(e[1], int):
                at = max(e[1], holds.get(cur, 0), lvl)
                if at <= cap:
                    nxt = (target, at)
            elif kind == "EVO_LEVEL_KNOW_MOVE" and e[1] in known:
                at = max(lvl, next(l for l, mv in mon_data(cur)["learnset"]["by_level"] if mv == e[1]))
                if at <= cap:
                    nxt = (target, at)
            elif kind == "EVO_LEVEL_MAGNETIC_FIELD" and magnetic:
                nxt = (target, lvl)
        if not nxt:
            return path
        cur, lvl = nxt
        path.append(nxt)


def move_pool(sp, caught, cap, holds=None, magnetic=False, known=None):
    """(final species, its move pool as the calculator names them): the
    capture rule's moves, the last four by the catch level (or `known`, the
    moves a record already has), and every level-up move learned after it up
    to the cap, along its evolutions."""
    names = move_names()
    path = chain(sp, caught, cap, holds, magnetic)
    by_name = {v: k for k, v in names.items()}
    first = ([by_name[m] for m in known if m in by_name] if known is not None else
             [mv for l, mv in mon_data(sp)["learnset"]["by_level"] if l <= caught][-4:])
    later = []
    for k, (s, frm) in enumerate(path):
        to = path[k + 1][1] if k + 1 < len(path) else cap
        later += [mv for l, mv in mon_data(s)["learnset"]["by_level"] if caught < l <= cap and frm <= l <= to]
    return path[-1][0], [names[m] for m in dict.fromkeys(first + later) if m in names]


def record(sp, level, nature, ability, ivs, moves, label=None):
    iv = {k: ivs for k in ("hp", "at", "df", "sp", "sa", "sd")}
    return {"constant": sp, "species": species_name(sp), "how": "plan", "level": level, "nature": nature,
            "ivs": iv, "evs": {k: 0 for k in iv}, "ability": ability, "moves": list(moves), "fill": False,
            "label": label or species_name(sp)}


# ---- 1. the screen ---------------------------------------------------------------------------------------

def prepare(fight_key, records, item_stock):
    """The fight against the whole box, every member with its whole pool:
    (st, the members' keys, the boss variant's (keys, flags))."""
    prep = plscore.prepare(plscore.parse_fight(fight_key), given_side=records)
    st = prep["st"]
    st["item_stock"] = dict(item_stock)
    keys = [f"p{i}" for i in range(len(records))]
    boss_keys, flags, _s = prep["variants"][0]
    return st, keys, boss_keys, flags


def matchups(st, keys, boss_keys):
    """For the fight's first weather: each member's expected share of each
    enemy's HP a turn by each of its moves, each enemy's best share of each
    member's HP, and speeds."""
    w = sorted({x for x, _a, _d in st["rows"]}, key=str)[0]

    def row(a, t):
        return st["rows"].get((w, a, t)) or st["rows"].get((None, a, t))

    def expected(k, e, name, mv):
        if name == "Magnitude":
            # Its power is rolled on use, so its rows are one per power, under
            # twin keys (fightsim.prepare); the expectation weighs them by odds.
            return sum(pct / 100 * plfeat._expected((row(f"{k}#m{p}", e) or {}).get("moves", {}).get(name), mv)
                       for p, pct in fs.MAGNITUDE_POWERS.items())
        return plfeat._expected((row(k, e) or {}).get("moves", {}).get(name), mv)

    mine = {}       # (member, move): [share of each enemy's HP]
    for k in keys:
        for name in st["moves"][k]:
            mv = fs.move(name)
            if not mv.damaging():
                continue
            mine[(k, name)] = [expected(k, e, name, mv) / st["info"][e]["hp"] for e in boss_keys]
    theirs = {}     # (enemy, member): best share of the member's HP
    for e in boss_keys:
        for k in keys:
            r = row(e, k)
            best = 0.0
            for name in st["moves"][e]:
                mv = fs.move(name)
                if mv.damaging() and r:
                    best = max(best, plfeat._expected(r["moves"].get(name), mv))
            theirs[(e, k)] = best / st["info"][k]["hp"]
    speed = {k: st["speed"].get((w, k)) or st["speed"].get((None, k)) or 1 for k in keys + list(boss_keys)}
    return mine, theirs, speed


def pick_moves(st, k, boss_keys, mine):
    """A member's four moves against this fight: up to three attacks of
    different types chosen for coverage (each adds the most to its best hit
    on every enemy), then the scorer's status rule (the best policy status
    move of tier A, else attacks, else status moves of tier B), as
    fightsim.player_moves fills a set."""
    attacks = [(n, s) for (kk, n), s in mine.items() if kk == k]
    chosen, types, best = [], set(), [0.0] * len(boss_keys)
    while len(chosen) < 3:
        gain, pick = 0.0, None
        for n, s in attacks:
            if n in chosen or fs.move(n).type in types:
                continue
            g = sum(max(0.0, min(1.0, x) - b) for x, b in zip(s, best))
            if g > gain:
                gain, pick = g, (n, s)
        if pick is None:
            break
        chosen.append(pick[0])
        types.add(fs.move(pick[0]).type)
        best = [max(b, min(1.0, x)) for b, x in zip(best, pick[1])]
    tiers = fs.status_tiers()
    # Every status move it has, best tier first: Ian's tiers rate Screech,
    # Play Nice and Leer low, yet our lines won Roark and Mars 1 with them,
    # so a spare slot takes a status move before a weaker attack of a type
    # already chosen (a move that does nothing in a position is never
    # offered by the planner, so a useless one costs nothing).
    status = sorted([n for n in st["moves"][k] if fs.move(n).cat == "Status" and n not in IDLE],
                    key=lambda n: -tiers.get(n, 0))
    out = chosen + [n for n in status[:1] if tiers.get(n, 0) >= fs.TIERS["A"]]
    rest = sorted((n for n, _s in attacks if n not in out), key=lambda n: -sum(mine[(k, n)]))
    new_type, seen = [], set(types)
    for n in rest:                       # the best attack of each type not yet covered
        if fs.move(n).type not in seen:
            new_type.append(n)
            seen.add(fs.move(n).type)
    same_type = [n for n in rest if n not in new_type]
    for n in new_type + status + same_type + [n for n in st["moves"][k] if n not in out]:
        if len(out) >= 4:
            break
        if n not in out:
            out.append(n)
    return out[:4]


# Status moves that do nothing in these fights (field effects and the like),
# filled only when nothing else is left.
IDLE = {"Mud Sport", "Water Sport", "Splash", "Teleport", "Celebrate", "Hold Hands", "Copycat", "Follow Me",
        "Helping Hand", "Ally Switch", "Magic Room", "Wonder Room"}


def margins(st, keys, boss_keys, moves, mine, theirs, speed):
    """For each member and enemy, how far the member wins their one-on-one:
    the hits the enemy needs to knock the member out less the hits the
    member needs, half a hit more for moving first and half a hit less for
    moving second. Positive means the member answers the enemy."""
    out = np.zeros((len(keys), len(boss_keys)))
    for i, k in enumerate(keys):
        for j, e in enumerate(boss_keys):
            share = max([mine[(k, n)][j] for n in moves[k] if (k, n) in mine] or [0.0])
            hits = math.ceil(1.0 / share) if share > 0.01 else 99
            taken = math.ceil(1.0 / theirs[(e, k)]) if theirs[(e, k)] > 0.01 else 99
            out[i, j] = min(taken - hits + (0.5 if speed[k] > speed[e] else -0.5), 3.0)
    return out


def score_sixes(M, size=6, depth=0.3, hole=2.0):
    """Every six of the box scored at once: per enemy, its best answer's
    margin and a little for a second answer, less a penalty for each enemy
    no member answers. [(score, member indices)], best first."""
    n = M.shape[0]
    combos = np.array(list(itertools.combinations(range(n), min(size, n))))
    out = []
    for lo in range(0, len(combos), 50000):
        c = combos[lo:lo + 50000]
        m = M[c]                                     # sixes x members x enemies
        top = np.sort(m, axis=1)
        best, second = top[:, -1, :], top[:, -2, :] if m.shape[1] > 1 else np.zeros_like(top[:, -1, :])
        s = (np.clip(best, -3, 3) + depth * np.clip(second, 0, 3)).sum(1) - hole * (best <= 0).sum(1)
        out += list(zip(s.tolist(), [tuple(x) for x in c.tolist()]))
    out.sort(key=lambda t: -t[0])
    return out


def screen(st, keys, boss_keys, top=20, apart=2):
    """The screen: each member's moves for this fight (set into the state,
    so every later fight uses them) and the top sixes, each differing from
    every one kept before it in at least `apart` members. Returns (sixes as
    key lists, their scores, the margin table, each member's moves)."""
    mine, theirs, speed = matchups(st, keys, boss_keys)
    moves = {k: pick_moves(st, k, boss_keys, mine) for k in keys}
    for k in keys:
        st["moves"][k] = moves[k]
        st["pokemon"][k] = dict(st["pokemon"][k], moves=moves[k])
    M = margins(st, keys, boss_keys, moves, mine, theirs, speed)
    kept = []
    for s, idx in score_sixes(M):
        if all(len(set(idx) - set(j)) >= apart for _s, j in kept):
            kept.append((s, idx))
        if len(kept) >= top:
            break
    return [[keys[i] for i in idx] for _s, idx in kept], [s for s, _i in kept], M, moves


# ---- 2. labels and networks --------------------------------------------------------------------------------

_JOB = {}


def _label_job(args):
    team, positions, seed, out_dir, name = args
    j = _JOB
    return pldata.distill(j["st"], team, j["boss_keys"], j["flags"], positions, seed, out_dir,
                          {"fight": name, "six": [j["st"]["pokemon"][k]["species"] for k in team]})


def label(st, sixes, boss_keys, flags, name, out_dir, positions=4500, budget=64, procs=None, seed=1):
    """The play-out planner's labels on these sixes (a job each), at the
    given budget: a tenth of a round over ten sixes by default."""
    _JOB.update(st=st, boss_keys=boss_keys, flags=flags)
    pldata.LABEL_BUDGET = budget
    jobs = [(six, positions, seed * 1000 + i, out_dir, name) for i, six in enumerate(sixes)]
    with plplan.fork_pool(procs or min(len(jobs), plplan.pool_size())) as pool_:
        return list(pool_.imap_unordered(_label_job, jobs, chunksize=1))


def without(fight_names, out):
    """A folder of links to every labelled shard so far except these fights'
    (their old labels would have seen other teams of the same fight)."""
    os.makedirs(out, exist_ok=True)
    for folder in ("data-gen", "data-gen-held", "data-d1", "data-d2", "data-d3"):
        for p in __import__("glob").glob(os.path.join(ROOT, folder, "*.json")):
            with open(p) as fh:
                if json.load(fh)["fight"] in fight_names:
                    continue
            for ext in (".json", ".npz"):
                t = os.path.join(out, f"{folder}-{os.path.basename(p)[:-5]}{ext}")
                if not os.path.exists(t):
                    os.symlink(p[:-5] + ext, t)
    return out


def train(name, data_dirs, seeds=(1, 2)):
    """Networks from scratch on these folders, one per seed, under the
    memory cap; their average's name."""
    for s in seeds:
        subprocess.run([os.path.join(REPO, "tools/oxide/capped"), "--max", "22G",
                        os.path.expanduser("~/venvs/oxide-ml/bin/python"), "-m", "tools.oxide.balance.plnet",
                        "--name", f"{name}-s{s}", "--data", *data_dirs, "--held-out", "0", "--epochs", "10",
                        "--lr", "1e-3", "--seed", str(s)],
                       cwd=REPO, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                       env=dict(os.environ, PYTHONPATH="."))
    return "+".join(f"{name}-s{s}" for s in seeds)


# ---- 3 and 4. the race and the finalists ---------------------------------------------------------------------

_LEADS = {}


def _fight_job(args):
    team, seed, cfg, luck = args
    j = _JOB
    lk = (tuple(team), json.dumps(cfg, sort_keys=True))
    if lk not in _LEADS:
        _LEADS[lk] = plplan.Planner(0, **cfg).lead(j["st"], list(team), j["boss_keys"], j["flags"])[0]
    r = plplan.play(j["st"], list(team), j["boss_keys"], j["flags"], _LEADS[lk], seed, cfg, luck)
    return tuple(team), r["won"], r["deaths"], r["clean"], [tuple(x) for x in r["faints"]], r["seconds"]


class Tally:
    """Every fight read for each six, and the race's score from them."""

    def __init__(self):
        self.rows = {}

    def add(self, team, won, deaths, clean, faints):
        self.rows.setdefault(tuple(team), []).append((won, deaths, clean, faints))

    def score(self, team):
        r = self.rows.get(tuple(team), [])
        if not r:
            return -1.0
        return sum(w for w, *_ in r) / len(r) - 0.1 * sum(d for _w, d, *_ in r) / len(r)

    def numbers(self, team):
        r = self.rows.get(tuple(team), [])
        n = max(1, len(r))
        return {"fights": len(r), "won": sum(w for w, *_ in r) / n, "faints": sum(d for _w, d, *_ in r) / n,
                "clean": sum(c for _w, _d, c, _f in r) / n}


def read(st, boss_keys, flags, teams, fights, cfg, luck="real", seed0=0, procs=None, tally=None):
    """Each team read on `fights` more fights; the tally."""
    _JOB.update(st=st, boss_keys=boss_keys, flags=flags)
    tally = tally or Tally()
    jobs = []
    for t in teams:
        # Each team's seeds follow from its members (a checksum, the same in
        # every process) and the fights it has had, so a reading repeats.
        start = seed0 * 1_000_003 + zlib.crc32(",".join(t).encode()) + len(tally.rows.get(tuple(t), []))
        jobs += [(tuple(t), start + i, cfg, luck) for i in range(fights)]
    with plplan.fork_pool(procs or plplan.pool_size()) as pool_:
        for team, won, deaths, clean, faints, _s in pool_.imap_unordered(_fight_job, jobs, chunksize=1):
            tally.add(team, won, deaths, clean, faints)
    return tally


def race(st, keys, boss_keys, flags, screened, cfg, rounds=5, per_round=16, fights=4, elite=4, rate=0.3,
         log=print, seed=1):
    """Ian's member ratings, then halving: (finalists best first, the tally,
    the members' final weights). Weights start from how often each member is
    in the screen's sixes; each round draws `per_round` sixes by weight
    (the screen's best always among the first round's), reads each on
    `fights` fights, and moves the weights toward the members of the
    `elite` best sixes so far."""
    rng = random.Random(seed)
    counts = {k: 1.0 + sum(k in s for s in screened) for k in keys}
    w = {k: c / sum(counts.values()) for k, c in counts.items()}
    tally = Tally()
    for r in range(rounds):
        teams = [tuple(s) for s in screened[:per_round // 2]] if r == 0 else []
        while len(teams) < per_round:
            pool_ = list(keys)
            six = []
            for _ in range(6):
                pick = rng.choices(pool_, weights=[w[k] for k in pool_])[0]
                six.append(pick)
                pool_.remove(pick)
            t = tuple(sorted(six, key=keys.index))
            if t not in teams:
                teams.append(t)
        read(st, boss_keys, flags, teams, fights, cfg, seed0=seed * 7919 + r, tally=tally)
        best = sorted(tally.rows, key=lambda t: -tally.score(t))[:elite]
        share = {k: sum(k in t for t in best) / elite for k in keys}
        w = {k: (1 - rate) * w[k] + rate * (share[k] + 0.01) for k in keys}
        log(f"  race round {r + 1}: best {[st['pokemon'][k]['species'] for k in best[0]]} "
            f"score {tally.score(best[0]):.2f}; heaviest {sorted(w, key=lambda k: -w[k])[:6]}")
    cands = sorted(tally.rows, key=lambda t: -tally.score(t))[:5]
    for fights_more, keep in ((8, 3), (16, 3)):
        read(st, boss_keys, flags, cands, fights_more, cfg, seed0=seed * 104729, tally=tally)
        cands = sorted(cands, key=lambda t: -tally.score(t))[:keep]
    return cands, tally, w


def full_reading(st, boss_keys, flags, team, cfg, real=75, unlucky=25, procs=None, seed=9):
    """The reading Ian rules: 75 fights at real odds and 25 very unlucky."""
    a = read(st, boss_keys, flags, [team], real, cfg, "real", seed0=seed * 31337, procs=procs)
    b = read(st, boss_keys, flags, [team], unlucky, cfg, "unlucky", seed0=seed * 31337 + 1, procs=procs)
    return a.numbers(team), b.numbers(team), a.rows[tuple(team)]


def losing_enemies(rows):
    """Which enemy Pokemon a reading's faints fell to, most first, from its
    rows' (fainted, enemy out) pairs."""
    tally = {}
    for _w, _d, _c, faints in rows:
        for _mine, foe in faints:
            tally[foe] = tally.get(foe, 0) + 1
    return sorted(tally.items(), key=lambda kv: -kv[1])


def ian_order(n):
    """A reading's place in Ian's order: wins first, then fewer faints."""
    return (round(n["won"], 3), -n["faints"])

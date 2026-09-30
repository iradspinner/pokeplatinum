"""Gauntlets: trainers fought in a row with no healing between them (Ian,
2026-09-27; balance plan, "Attrition lives in gauntlets").

    PYTHONPATH=. python3 -m tools.oxide.balance.gauntlet                    # the sections
    PYTHONPATH=. python3 -m tools.oxide.balance.gauntlet --first-reading    # the first proposal's

Two readings live here. The second, on Ian's rulings of 2026-09-27, is the
one the proposal uses: sections of 2 to 5 trainers, fights played out turn
by turn with rolls, misses, critical hits and the cost of swapping in, and
the survivors healed between fights while the dead stay dead (its own
section below). The first, described next, is kept for comparison: Ian
judged it too kind, since one team must answer several different fights.

The Pocket PC heals anywhere except in a gauntlet, so every other fight is
scored from a healed party and a gauntlet needs its own reading: how much a
party has left after it. The fight scores cannot give that, since they ask
whether the player has answers, not what the answers cost.

The reading sends random parties of six from the split's player side (the
plan's side: every species the player can own by the split's end, at its
cap) through the gauntlet's trainers in order, their Pokemon one at a time.
In each duel both sides deal their hardest hit every turn (the middle roll,
a charging or recharging move at half a turn), from the HP each has left,
and the one that moves first strikes first. Each boss Pokemon is met by the
member that beats it losing the least HP. When no member can win, the one
that hurts the boss most falls to it, which a nuzlocke counts as a death,
and the next steps in against what the boss has left. Nothing heals between
trainers.

A party clears the gauntlet cleanly when no member faints. The share of
parties that do is set beside the same share for the split's story fights,
each read the same way from a healed party, so a gauntlet can be sized to
sit where Ian wants it against his rated fights.

Left out, as the fight scores leave them out: misses, critical hits,
status, switching costs, the player's items (a bag's Potions soften every
gauntlet), and the boss's AI choosing anything but its hardest hit. Random
parties are weaker than a player's chosen six, so the shares compare
gauntlets and fights with one another, not with a run.
"""
import argparse
import collections
import json
import os
import random
import statistics
import sys

from ..encounters import calc_trainers
from . import b6, data, pressure, splits, teamscore

PARTIES = 1000
SIZE = 6
SEED = 20260927

# The candidate gauntlets: one-way areas, their maps in walking order, the
# split they are fought in, and the story fights that close them.
CANDIDATES = {
    "galactic_eterna": {
        "label": "Team Galactic's Eterna building", "split": "Fantina",
        "maps": ["TEAM_GALACTIC_ETERNA_BUILDING_1F", "TEAM_GALACTIC_ETERNA_BUILDING_2F",
                 "TEAM_GALACTIC_ETERNA_BUILDING_3F"], "bosses": ["jupiter_1"]},
    "wayward_cave": {
        "label": "Wayward Cave", "split": "Fantina", "maps": ["WAYWARD_CAVE_1F"], "bosses": []},
    "lost_tower": {
        "label": "The Lost Tower", "split": "Maylene",
        "maps": ["ROUTE_209_LOST_TOWER_2F", "ROUTE_209_LOST_TOWER_3F", "ROUTE_209_LOST_TOWER_4F"],
        "bosses": []},
    "iron_island": {
        "label": "Iron Island", "split": "Byron",
        "maps": ["IRON_ISLAND_B1F_LEFT_ROOM", "IRON_ISLAND_B1F_RIGHT_ROOM",
                 "IRON_ISLAND_B2F_LEFT_ROOM", "IRON_ISLAND_B2F_RIGHT_ROOM"], "bosses": []},
    "galactic_hq": {
        "label": "The Galactic HQ", "split": "HQ",
        "maps": ["GALACTIC_HQ_1F", "GALACTIC_HQ_2F", "GALACTIC_HQ_3F", "GALACTIC_HQ_B2F"],
        "bosses": ["cyrus_2", "saturn_2"]},
    "mt_coronet": {
        "label": "The Mt. Coronet climb", "split": "Galactic",
        "maps": ["MT_CORONET_1F_TUNNEL_ROOM", "MT_CORONET_3F", "MT_CORONET_4F_ROOMS_1_AND_2",
                 "MT_CORONET_5F", "MT_CORONET_6F"], "bosses": ["mars_jupiter", "cyrus_3"]},
    "stark_mountain": {
        "label": "Stark Mountain", "split": "Galactic",
        "maps": ["STARK_MOUNTAIN_OUTSIDE", "STARK_MOUNTAIN_ROOM_1", "STARK_MOUNTAIN_ROOM_2"],
        "bosses": []},
    "victory_road": {
        "label": "Victory Road", "split": "Barry",
        "maps": ["VICTORY_ROAD_1F", "VICTORY_ROAD_2F", "VICTORY_ROAD_B1F"], "bosses": []},
    # Ian designed the level 71 Lucas and Dawn fight (one slot per starter,
    # 779 to 784) for the start of Victory Road; its script is the
    # Battleground's until the trainer pass moves it. Read with the first slot.
    "victory_road_rival": {
        "label": "Victory Road, opened by the level 71 Lucas and Dawn fight", "split": "Barry",
        "first": [779],
        "maps": ["VICTORY_ROAD_1F", "VICTORY_ROAD_2F", "VICTORY_ROAD_B1F"], "bosses": []},
}


def trainers(name):
    """A candidate's ordinary trainers in walking order: map by map, each
    map's in id order. Only first-run trainers B6 places are taken, so a
    post-game room (Victory Road's back) stays out."""
    spec = CANDIDATES[name]
    placed = b6.placements()
    by_map = collections.defaultdict(list)
    for tr, maps in splits.trainer_maps().items():
        for h in maps:
            if h in spec["maps"] and tr in placed:
                by_map[h].append(tr)
    return spec.get("first", []) + [tr for h in spec["maps"] for tr in sorted(by_map[h])]


def _story(key):
    return next(f for f in data.fights()["fights"] if f["key"] == key)


def _team(tr):
    """A trainer's party by id. The balance data leaves out every dummy_
    slot, and Ian's Lucas and Dawn fights live in some (779 to 802), so a
    slot it lacks is read from its own file."""
    ox = data.oxide_trainers()
    if tr in ox:
        return ox[tr]["party"]
    with open(os.path.join(data.ROOT, "generated", "trainers.txt"), encoding="utf-8") as f:
        stem = [l.strip() for l in f][tr].replace("TRAINER_", "").lower()
    with open(os.path.join(data.ROOT, "res", "trainers", "data", f"{stem}.json"),
              encoding="utf-8") as f:
        raw = json.load(f)
    return [data._mon(sp, s) for sp, s in calc_trainers.build_trainer(data.ROOT, stem, raw)]


def parties(tr_ids, boss_keys=()):
    """The gauntlet's teams in order, each a list of Pokemon, with its
    closing story fights' parties after the ordinary trainers'."""
    teams = [(f"trainer {tr}", _team(tr)) for tr in tr_ids]
    for key in boss_keys:
        for p in pressure.boss_parties(_story(key))[0]:
            teams.append((key, p))
    return teams


def run(split, teams, trick_room=False):
    """Every matchup of the split's side against every Pokemon of `teams`,
    in one Node run: b6's state, with the boss keys in team order."""
    blob, side = teamscore._blob(), teamscore.side(split)
    all_mons = [m for _label, team in teams for m in team]
    fight = {"key": "gauntlet", "label": "gauntlet", "split": split, "tr_ids": [],
             "trick_room": trick_room}
    jobs, ctx = pressure.fight_jobs(fight, blob, side=side, parties=[all_mons], weather=None)
    return b6.run_state(jobs, ctx, side, teamscore._blob_path())


def _per_turn(row, weather):
    """An attacker's hardest middle roll a turn against one defender, and its
    priority: a charging or recharging move counts at half. Fling and Natural
    Gift are left out, being one use each."""
    per, pr = 0.0, 0
    for move, r in row["moves"].items():
        if "error" in r or move in pressure.ITEM_MOVES:
            continue
        mid = r["rolls"][len(r["rolls"]) // 2]
        if pressure.turns(move, 1, weather) > 1 or move in pressure.RECHARGE:
            mid /= 2
        if mid > per:
            per, pr = mid, r["priority"]
    return per, pr


def rates(st):
    """{(member key, boss key): (share of the boss's HP the member takes a
    turn, share of the member's HP the boss takes a turn, whether the
    member moves first)}."""
    out = {}
    tr = st["trick_room"]
    for _v, bk, _mon, w in st["bosses"]:
        for pk in st["side_keys"]:
            up, down = st["rows"][(pk, bk)], st["rows"][(bk, pk)]
            dealt, pr = _per_turn(up, w)
            taken, bpr = _per_turn(down, w)
            out[(pk, bk)] = (dealt / st["info"][bk]["hp"], taken / st["info"][pk]["hp"],
                             pressure.moves_first(pr - bpr, up["speeds"], tr))
    return out


def duel(rate, member_hp, boss_hp):
    """One member against one boss Pokemon, each from what it has left:
    (member wins, member's HP after, boss's HP after)."""
    dealt, taken, first = rate
    if dealt <= 0:
        return False, 0.0, boss_hp
    to_win = -(-boss_hp // dealt) if boss_hp > 0 else 0
    to_lose = -(-member_hp // taken) if taken > 0 else float("inf")
    if to_win < to_lose or (first and to_win == to_lose):
        hits_taken = to_win - 1 if first else to_win
        return True, member_hp - hits_taken * taken, 0.0
    # The member falls, having hit the boss each turn it moved before then.
    hits_dealt = to_lose if first else to_lose - 1
    return False, 0.0, max(0.0, boss_hp - hits_dealt * dealt)


def simulate(rate, side_keys, boss_keys, n=PARTIES, seed=SEED):
    """Random parties through the bosses in order: {"clean", "wiped",
    "faints" (median), "hp_used" (median, in whole members)}. Each boss
    Pokemon is met by the member that beats it losing the least HP; when
    none can, the member that hurts it most falls to it and the next steps
    in against what is left."""
    rng = random.Random(seed)
    clean = wiped = 0
    faints_all, used_all = [], []
    for _ in range(n):
        party = rng.sample(side_keys, min(SIZE, len(side_keys)))
        hp = {p: 1.0 for p in party}
        faints = 0
        for bk in boss_keys:
            boss = 1.0
            while boss > 0 and any(v > 0 for v in hp.values()):
                outcomes = [(p, duel(rate[(p, bk)], hp[p], boss)) for p in party if hp[p] > 0]
                wins = [(hp[p] - left, p) for p, (won, left, _b) in outcomes if won]
                if wins:
                    lost, p = min(wins)
                    hp[p] -= lost
                    boss = 0.0
                    break
                p, (_won, _left, after) = min(outcomes, key=lambda o: o[1][2])
                hp[p], boss = 0.0, after
                faints += 1
            if not any(v > 0 for v in hp.values()):
                break
        clean += faints == 0
        wiped += not any(v > 0 for v in hp.values())
        faints_all.append(faints)
        used_all.append(sum(1.0 - max(v, 0.0) for v in hp.values()))
    return {"clean": clean / n, "wiped": wiped / n, "faints": statistics.median(faints_all),
            "hp_used": round(statistics.median(used_all), 2)}


def boss_keys(st):
    """The gauntlet's Pokemon keys in order, setup branches left out."""
    return [bk for _v, bk, _m, _w in st["bosses"]]


def strong_third(st):
    """The third of the side with the highest stat totals at the cap: closer
    to the six a player picks than the whole side, which runs from first
    stages to legendaries."""
    total = lambda pk: sum(st["info"][pk]["stats"].values())
    keys = sorted(st["side_keys"], key=total, reverse=True)
    return keys[:max(SIZE, len(keys) // 3)]


def both(st, rate, keys):
    """The reading for random parties from the whole side and from its
    strong third."""
    return {"random": simulate(rate, st["side_keys"], keys),
            "strong": simulate(rate, strong_third(st), keys)}


def reading(name, prefix=None):
    """A candidate read whole and, trainer by trainer, as the first k of its
    teams: [(teams so far, label of the last, Pokemon so far, result)]."""
    spec = CANDIDATES[name]
    teams = parties(trainers(name), spec["bosses"])
    st = run(spec["split"], teams)
    rate = rates(st)
    keys = boss_keys(st)
    out, count = [], 0
    for i, (label, team) in enumerate(teams):
        count += len(team)
        if prefix is None or i + 1 in prefix or i + 1 == len(teams):
            out.append((i + 1, label, count, both(st, rate, keys[:count])))
    return out


def anchors(split):
    """The split's story fights, each read the same way from a healed party."""
    out = {}
    for fight in data.fights()["fights"]:
        if fight["split"] != split:
            continue
        teams = [(fight["key"], p) for p in pressure.boss_parties(fight)[0]]
        st = run(split, teams, bool(fight.get("trick_room")))
        out[fight["key"]] = both(st, rates(st), boss_keys(st))
    return out


def _fmt(r):
    """Both readings on one line: clean clears, then the median HP the party
    used, in whole members, for random and for strong parties."""
    a, b = r["random"], r["strong"]
    return (f"random clean {a['clean']:.2f}, HP used {a['hp_used']:g}; "
            f"strong clean {b['clean']:.2f}, HP used {b['hp_used']:g}, "
            f"median faints {b['faints']:g}")


# ---- the second reading, on Ian's rulings (2026-09-27) ---------------------------------
#
# A gauntlet is 2 to 5 mandatory trainers on the easier side of average, bosses
# outside it, and the bag may heal between its fights: the danger is deaths
# snowballing. Ian judged the first reading too kind, because one team must
# answer several different fights. So this one plays each trainer's fight
# out: the six stay together through the section; a member keeps the field
# from one boss Pokemon to the next unless another answers it better, and
# swapping in at a fight's start costs the incoming member a hit (after a
# faint, and between boss Pokemon, the game's Shift mode lets the player
# swap free); every hit rolls its damage and its accuracy, and one in
# sixteen is critical, twice as hard. After each trainer the survivors heal
# to full, as the bag allows, and a member that fell stays fallen.

# Each section: its label, its maps in walking order, which half of a map
# (0 or 1, None for all of it), and the trainers left out of it. Mt.
# Coronet's officers are left out: Hesperid is a fight Ian rated as a boss,
# and Moira and Argo read well above the split's average; Somnu, at it,
# joins the floors below.
SECTIONS = {
    "galactic_eterna": [
        ("1F and 2F", ["TEAM_GALACTIC_ETERNA_BUILDING_1F", "TEAM_GALACTIC_ETERNA_BUILDING_2F"],
         None, ()),
        ("3F", ["TEAM_GALACTIC_ETERNA_BUILDING_3F"], None, ())],
    "galactic_hq": [
        ("1F", ["GALACTIC_HQ_1F"], None, ()), ("2F", ["GALACTIC_HQ_2F"], None, ()),
        ("3F", ["GALACTIC_HQ_3F"], None, ()), ("B2F", ["GALACTIC_HQ_B2F"], None, ())],
    "mt_coronet": [
        ("1F's tunnel", ["MT_CORONET_1F_TUNNEL_ROOM"], None, ()),
        ("3F, 4F and Somnu on 5F", ["MT_CORONET_3F", "MT_CORONET_4F_ROOMS_1_AND_2",
                                     "MT_CORONET_5F"], None, (520, 526, 834))],
    "victory_road": [
        ("1F, the half nearer the entrance", ["VICTORY_ROAD_1F"], 0, ()),
        ("1F, the far half", ["VICTORY_ROAD_1F"], 1, ()),
        ("2F", ["VICTORY_ROAD_2F"], None, ()), ("B1F", ["VICTORY_ROAD_B1F"], None, ())],
}
CRIT = 1 / 16
MAX_TURNS = 30


def _positions(header):
    """{trainer id: its z on the map}, from the map's events."""
    events = splits.headers()[header].get("eventsArchiveID")
    path = os.path.join(data.ROOT, "res", "field", "events", f"{events}.json")
    ids = {t["constant"]: tr for tr, t in data.oxide_trainers().items()}
    out = {}
    if events and os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            for o in json.load(f).get("object_events", []):
                tr = ids.get(str(o.get("script", "")))
                if tr is not None:
                    out[tr] = o.get("z", 0)
    return out


def section_trainers(area, section):
    """A section's trainers in walking order. A map split in two halves is
    ordered from its entrance, taken as the larger z, as on Victory Road 1F."""
    _label, maps, half, leave_out = section
    placed = b6.placements()
    out = []
    for h in maps:
        on_map = [tr for tr, ms in splits.trainer_maps().items()
                  if h in ms and tr in placed and tr not in leave_out]
        pos = _positions(h)
        on_map.sort(key=lambda tr: (-pos.get(tr, 0), tr))
        if half is not None:
            k = (len(on_map) + 1) // 2
            on_map = on_map[:k] if half == 0 else on_map[k:]
        out += on_map
    return out


def _accuracy(move):
    a = pressure.accuracies().get(metrics_compact(pressure.MOVE_SPELLING.get(move, move)), 100)
    return 1.0 if a is None else min(a, 100) / 100


def metrics_compact(name):
    from . import metrics
    return metrics._compact(name)


def _choice(row, weather):
    """The move with the most expected damage a turn: (move, rolls, priority,
    accuracy, turns a hit takes), or None."""
    best = None
    for move, r in row["moves"].items():
        if "error" in r or move in pressure.ITEM_MOVES or not r["rolls"]:
            continue
        mid = r["rolls"][len(r["rolls"]) // 2]
        if mid <= 0:
            continue
        acc = _accuracy(move)
        slow = 2 if pressure.turns(move, 1, weather) > 1 or move in pressure.RECHARGE else 1
        value = mid * acc / slow
        if best is None or value > best[0]:
            best = (value, move, r["rolls"], r["priority"], acc, slow)
    return best[1:] if best else None


def _hit(choice, rng):
    """One use of a move: its damage, 0 on a miss."""
    _move, rolls, _pr, acc, _slow = choice
    if rng.random() >= acc:
        return 0
    return rng.choice(rolls) * (2 if rng.random() < CRIT else 1)


def _first(up, a, b, trick_room, rng):
    pa, pb = (a[2] if a else 0), (b[2] if b else 0)
    if pa != pb:
        return pa > pb
    sa, sb = up["speeds"]
    if sa == sb:
        return rng.random() < 0.5
    return sa < sb if trick_room else sa > sb


def fight(st, pk, bk, hp, boss_hp, rng):
    """A member against a boss Pokemon, turn by turn from what each has
    left: (member's HP, boss's HP) after one falls, or after MAX_TURNS."""
    up, down = st["rows"][(pk, bk)], st["rows"][(bk, pk)]
    w = next(w for _v, k, _m, w in st["bosses"] if k == bk)
    a, b = _choice(up, w), _choice(down, w)
    if a is None and b is None:
        return hp, boss_hp
    first = _first(up, a, b, st["trick_room"], rng)
    for turn in range(MAX_TURNS):
        for side in (("p", "b") if first else ("b", "p")):
            if hp <= 0 or boss_hp <= 0:
                return max(hp, 0), max(boss_hp, 0)
            ch = a if side == "p" else b
            if ch is None or turn % ch[4]:
                continue
            if side == "p":
                boss_hp -= _hit(ch, rng)
            else:
                hp -= _hit(ch, rng)
    return max(hp, 0), max(boss_hp, 0)


def _pick(st, rate, alive, hp, bk, boss_share):
    """The member a player sends at a boss Pokemon, by the first reading's
    even-handed duel: the one that wins losing the least share of its HP,
    else the one that leaves the boss the least."""
    best_win, best_lose = None, None
    for pk in alive:
        share = hp[pk] / st["info"][pk]["hp"]
        won, left, after = duel(rate[(pk, bk)], share, boss_share)
        if won:
            if best_win is None or share - left < best_win[0]:
                best_win = (share - left, pk)
        elif best_lose is None or after < best_lose[0]:
            best_lose = (after, pk)
    return (best_win or best_lose)[1]


def draw(rng, keys, weights, k):
    """k of `keys` without replacement, each as likely as its box share
    (weights; all equal when there are none): a party a realistic box would
    field, not one of every species (2026-09-30)."""
    w = weights or {}
    ranked = sorted(keys, key=lambda pk: rng.random() ** (1.0 / max(w.get(pk, 1.0), 1e-9)),
                    reverse=True)
    return ranked[:min(k, len(ranked))]


def run_section(st, team_sizes, pool_keys, n=PARTIES, seed=SEED):
    """Parties of six through a section's trainers in order: {"clean" (the
    share with no death), "deaths" (the mean), "wiped"}."""
    rng = random.Random(seed)
    rate = rates(st)
    keys = boss_keys(st)
    fights, i = [], 0
    for size in team_sizes:
        fights.append(keys[i:i + size])
        i += size
    clean = wiped = 0
    deaths_all = []
    for _ in range(n):
        party = draw(rng, pool_keys, st.get("weights"), SIZE)
        full = {pk: st["info"][pk]["hp"] for pk in party}
        hp = dict(full)
        deaths = 0
        for boss_mons in fights:
            active = next((pk for pk in party if hp[pk] > 0), None)
            opening = True
            for bk in boss_mons:
                boss_hp = st["info"][bk]["hp"]
                while boss_hp > 0:
                    alive = [pk for pk in party if hp[pk] > 0]
                    if not alive:
                        break
                    pk = _pick(st, rate, alive, hp, bk, boss_hp / st["info"][bk]["hp"])
                    if opening and pk != active:
                        # Swapping in against the fight's first Pokemon costs a hit.
                        b = _choice(st["rows"][(bk, pk)], None)
                        if b:
                            hp[pk] -= _hit(b, rng)
                        if hp[pk] <= 0:
                            hp[pk] = 0
                            deaths += 1
                            continue
                    opening = False
                    active = pk
                    hp[pk], boss_hp = fight(st, pk, bk, hp[pk], boss_hp, rng)
                    if hp[pk] <= 0:
                        deaths += 1
                    elif boss_hp > 0:
                        break          # a stalemate: nobody can finish it
            for pk in party:
                if hp[pk] > 0:
                    hp[pk] = full[pk]    # the bag heals the survivors between fights
        clean += deaths == 0
        wiped += all(hp[pk] <= 0 for pk in party)
        deaths_all.append(deaths)
    return {"clean": clean / n, "deaths": round(statistics.mean(deaths_all), 2),
            "wiped": wiped / n}


def section_reading(area, section):
    split = CANDIDATES[area]["split"]
    trs = section_trainers(area, section)
    teams = [(f"trainer {tr}", _team(tr)) for tr in trs]
    st = run(split, teams)
    return trs, run_section(st, [len(t) for _l, t in teams], strong_third(st))


def fight_reading(fight):
    """A story fight read the same way, from a healed party. A tag fight's
    trainers are one battle; a fight with a team per starter (Barry's, Lucas
    and Dawn's) is read team by team and the readings averaged."""
    ps = pressure.boss_parties(fight)[0]
    groups = [[p for p in ps]] if fight.get("tag") else [[p] for p in ps]
    reads = []
    for group in groups:
        teams = [(fight["key"], p) for p in group]
        st = run(fight["split"], teams, bool(fight.get("trick_room")))
        reads.append(run_section(st, [sum(len(t) for _l, t in teams)], strong_third(st)))
    return {k: round(statistics.mean(r[k] for r in reads), 2) for k in ("clean", "deaths", "wiped")}


def split_average(split):
    """The mean of the split's ordinary trainers on Ian's scale (B6)."""
    line = b6.scale_line()
    res = b6.load().get("trainers", {})
    vals = [b6.on_scale(r["safe"], line) for tr, r in res.items() if r.get("split") == split]
    return statistics.mean(vals) if vals else None


def section_report(out=sys.stdout):
    line = b6.scale_line()
    res = b6.load().get("trainers", {})
    ox = data.oxide_trainers()
    for area, sections in SECTIONS.items():
        spec = CANDIDATES[area]
        avg = split_average(spec["split"])
        print(f"\n{spec['label']} ({spec['split']}'s split; its ordinary trainers average "
              f"{avg:.1f} on Ian's scale)", file=out)
        for section in sections:
            trs, r = section_reading(area, section)
            scale = {tr: b6.on_scale(res[str(tr)]["safe"], line) for tr in trs if str(tr) in res}
            above = [f"{ox[tr]['name']} {tr} ({s:.1f})" for tr, s in scale.items() if s > avg + 0.5]
            print(f"  {section[0]:34} {len(trs)} trainers, {sum(len(ox[t]['party']) for t in trs)} "
                  f"Pokemon, each {min(scale.values()):.1f} to {max(scale.values()):.1f}: clean "
                  f"{r['clean']:.2f}, deaths {r['deaths']:.2f} a run"
                  f"{'; above the average: ' + ', '.join(above) if above else ''}", file=out)
        for fight in data.fights()["fights"]:
            if fight["split"] == spec["split"]:
                r = fight_reading(fight)
                print(f"  story fight {fight['key']:22} clean {r['clean']:.2f}, "
                      f"deaths {r['deaths']:.2f}", file=out)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("name", nargs="?", choices=sorted(CANDIDATES))
    ap.add_argument("--first-reading", action="store_true",
                    help="the first reading, with no healing and the average hit")
    args = ap.parse_args(argv)
    if not args.first_reading:
        section_report()
        return 0
    names = [args.name] if args.name else list(CANDIDATES)
    seen_splits = set()
    for name in names:
        spec = CANDIDATES[name]
        rows = reading(name, prefix=None if args.name else {4, 6, 8, 10, 12})
        print(f"\n{spec['label']} ({spec['split']}'s split, {len(trainers(name))} trainers"
              f"{', then ' + ' and '.join(spec['bosses']) if spec['bosses'] else ''})")
        for k, label, count, r in rows:
            print(f"  first {k:>2} teams ({count:>2} Pokemon, to {label}): {_fmt(r)}")
        if spec["split"] not in seen_splits:
            seen_splits.add(spec["split"])
            for key, r in anchors(spec["split"]).items():
                print(f"  story fight {key}, from a healed party: {_fmt(r)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

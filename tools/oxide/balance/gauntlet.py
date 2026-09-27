"""Gauntlets: trainers fought in a row with no healing between them (Ian,
2026-09-27; balance plan, "Attrition lives in gauntlets").

    PYTHONPATH=. python3 -m tools.oxide.balance.gauntlet                 # every candidate
    PYTHONPATH=. python3 -m tools.oxide.balance.gauntlet galactic_hq     # one, trainer by trainer

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
        "label": "Victory Road", "split": "League",
        "maps": ["VICTORY_ROAD_1F", "VICTORY_ROAD_2F", "VICTORY_ROAD_B1F"], "bosses": []},
    # Ian designed the level 71 Lucas and Dawn fight (one slot per starter,
    # 779 to 784) for the start of Victory Road; its script is the
    # Battleground's until the trainer pass moves it. Read with the first slot.
    "victory_road_rival": {
        "label": "Victory Road, opened by the level 71 Lucas and Dawn fight", "split": "League",
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


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("name", nargs="?", choices=sorted(CANDIDATES))
    args = ap.parse_args(argv)
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

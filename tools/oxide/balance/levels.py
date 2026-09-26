"""B4: the level curve, the natural level per split against its cap.

    PYTHONPATH=. python3 -m tools.oxide.balance.levels            # the report
    PYTHONPATH=. python3 -m tools.oxide.balance.levels --team 4   # a smaller team

The natural level is where a team ends a split having beaten its trainers
and nothing else: no wild battles, no grinding. Experience is the game's
own formula (battle_script.c, BtlCmd_CalcExpGain and the get-exp task): a
fainted Pokemon gives its species' base experience times its level over 7,
divided among the Pokemon that fought it, and a trainer battle adds half
again. The team shares all of it evenly, which is what rotating a nuzlocke
team does on average. At a hard cap the extra is lost, as Oxide's
script-driven caps will do, so each split starts from the level the last
one ended on, not from where the experience alone would have taken it.

Two curves bracket what a player gets:

- the floor: the story fights plus the trainers B1e says cannot be walked
  around on the story path;
- the ceiling: every trainer B1d places in the split, less the late visits
  that belong to a later one.

Gyms with moving parts and multi-floor dungeons are not in B1e's model, so
their trainers count only toward the ceiling; the floor is a floor.

Renegade Platinum keeps Platinum's trainer ids, so its trainers are read
through the same placement and scored the same way. It has no hard caps,
so its curve is read uncapped against the caps Oxide took from its bosses.

Oxide means the player to "candy to the cap": Rare Candies, chained, close
whatever gap the trainers leave. Ian ruled on 2026-09-25 that the portable
PC (the base ROM's Vs. Seeker item, still to be ported) gives infinite Rare
Candies, so the gap never blocks a player. The candy budget below measures
how much of each cap the trainers give for free and how much the candies
have to cover, which is what the placement pass changes when it makes more
ordinary trainers unavoidable.

The splits and their caps come from fights.json, so a change to the split
structure changes the curve without touching this file.
"""
import argparse
import collections
import functools
import json
import os
import sys

from ..encounters import canon, pokedex
from . import data, metrics, required

START_LEVEL = 5           # the starter
TRAINER_BONUS = (150, 100)
GROWTH = ("EXP_RATE_MEDIUM_SLOW", "EXP_RATE_MEDIUM_FAST")


def exp_at(rate, n):
    """Total experience at level n for a growth rate (Generation 4's tables)."""
    if n <= 1:
        return 0
    if rate == "EXP_RATE_MEDIUM_FAST":
        return n ** 3
    if rate == "EXP_RATE_MEDIUM_SLOW":
        return 6 * n ** 3 // 5 - 15 * n ** 2 + 100 * n - 140
    if rate == "EXP_RATE_FAST":
        return 4 * n ** 3 // 5
    if rate == "EXP_RATE_SLOW":
        return 5 * n ** 3 // 4
    raise KeyError(rate)


def level_for(rate, exp):
    """The level a total of experience reaches, up to 100."""
    n = 1
    while n < 100 and exp_at(rate, n + 1) <= exp:
        n += 1
    return n


@functools.lru_cache(maxsize=None)
def species_exp():
    """{calculator name: base experience} for every species in the tree. A
    form without its own entry uses its base species' (Rotom-Wash, Rotom)."""
    out = {}
    for species in pokedex.species_list(data.ROOT):
        name = canon.showdown_name(species)
        path = os.path.join(data.ROOT, "res", "pokemon", pokedex.folder_of(species), "data.json")
        if not name or not os.path.exists(path):
            continue
        with open(path, encoding="utf-8") as f:
            out[name] = json.load(f)["base_exp_reward"]
    return out


def _key(name):
    """Names compared without punctuation or case, since the hacks' data
    spell some differently (Farfetch'd with a straight or a curly quote)."""
    return "".join(c for c in name.lower() if c.isalnum())


@functools.lru_cache(maxsize=None)
def _by_key():
    return {_key(n): v for n, v in species_exp().items()}


def base_exp(name):
    table = _by_key()
    for candidate in (name, name.split("-")[0]):
        if _key(candidate) in table:
            return table[_key(candidate)]
    raise KeyError(f"no base experience for {name}")


def foe_exp(mon):
    """Experience one fainted Pokemon gives the one Pokemon that fought it."""
    exp = base_exp(mon["species"]) * mon["level"] // 7
    return exp * TRAINER_BONUS[0] // TRAINER_BONUS[1]


def trainer_exp(trainer):
    return sum(foe_exp(m) for m in trainer["party"])


def _fight_trainers(hack, fight):
    """One rival variant (they share levels) and both halves of a tag."""
    ts = data.fight_trainers(hack, fight)
    return ts if fight.get("tag") else ts[:1]


def splits():
    """The splits in play order, from fights.json."""
    return list(data.fights()["splits"])


@functools.lru_cache(maxsize=None)
def trainer_sets():
    """{split: {"story": [tr_id], "required": [tr_id], "placed": [tr_id]}}.
    A story fight's trainers count in its split and nowhere else."""
    story = collections.defaultdict(list)
    story_ids = set()
    for fight in data.fights()["fights"]:
        ids = [t["tr_id"] for t in _fight_trainers("oxide", fight)]
        story[fight["split"]] += ids
        story_ids |= set(fight["tr_ids"])
    ids = required.trainer_ids()
    req = collections.defaultdict(list)
    for const, (split, _header, verdict) in required.first_crossings().items():
        tr_id = ids.get(const)
        if verdict == "required" and tr_id is not None and tr_id not in story_ids:
            req[split].append(tr_id)
    placed = {s: [i for i in v if i not in story_ids] for s, v in metrics.filler_ids().items()}
    return {s: {"story": story.get(s, []), "required": sorted(set(req.get(s, []))),
                "placed": placed.get(s, [])} for s in splits()}


def split_exp(hack, kind):
    """{split: experience} for a hack, where kind is "floor" (story and
    required) or "ceiling" (story and every placed trainer)."""
    pool = data.oxide_trainers() if hack == "oxide" else data.ref_trainers(hack)
    by_key = {f["key"]: f for f in data.fights()["fights"]}
    out = {}
    for split, sets in trainer_sets().items():
        exp = 0
        for fight in (f for f in data.fights()["fights"] if f["split"] == split):
            exp += sum(trainer_exp(t) for t in _fight_trainers(hack, by_key[fight["key"]]))
        extra = sets["required"] if kind == "floor" else sets["placed"]
        exp += sum(trainer_exp(pool[i]) for i in extra if i in pool)
        out[split] = exp
    return out


def curve(hack, kind, team=6, rate="EXP_RATE_MEDIUM_SLOW", capped=True):
    """[(split, cap, experience in the split, level at its end, experience
    lost to the cap)] for a team of `team` sharing evenly."""
    caps = data.fights()["caps"]
    exp = exp_at(rate, START_LEVEL)
    rows = []
    for split, gained in split_exp(hack, kind).items():
        exp += gained / team
        level = level_for(rate, exp)
        lost = 0
        if capped and level >= caps[split]:
            lost = exp - exp_at(rate, caps[split])
            exp = exp_at(rate, caps[split])
            level = caps[split]
        rows.append((split, caps[split], gained, level, lost * team))
    return rows


@functools.lru_cache(maxsize=None)
def candy_supply():
    """{split: Rare Candies the split offers}: item balls, hidden items, NPC
    gifts and shops (B1d). A shop that sells them would make the supply
    unlimited, so it is reported apart."""
    from . import splits as placement
    out = collections.Counter()
    shops = set()
    for split, _h, item, _how in placement.items():
        if item == "ITEM_RARE_CANDY":
            out[split] += 1
    for split, _h, item in placement.gifts():
        if item == "ITEM_RARE_CANDY":
            out[split] += 1
    for split, table, item in placement.marts():
        if item == "ITEM_RARE_CANDY":
            shops.add((split, table))
    return {s: out.get(s, 0) for s in splits()}, sorted(shops)


def candy_budget(kind, team=6, rate="EXP_RATE_MEDIUM_SLOW"):
    """[(split, cap, level trainers alone reach, candies to close the gap,
    candies offered, running balance)] for "candy to the cap": the team
    enters each split at the last split's cap, as Oxide means it to, and
    tops up with Rare Candies, one level each."""
    caps = data.fights()["caps"]
    supply, _shops = candy_supply()
    start, balance, rows = START_LEVEL, 0, []
    for split, gained in split_exp("oxide", kind).items():
        exp = exp_at(rate, start) + gained / team
        reached = min(level_for(rate, exp), caps[split])
        needed = team * (caps[split] - reached)
        balance += supply[split] - needed
        rows.append((split, caps[split], reached, needed, supply[split], balance))
        start = caps[split]
    return rows


def report(team=6, out=sys.stdout):
    caps = data.fights()["caps"]
    series = {}
    for rate in GROWTH:
        short = "slow" if rate.endswith("SLOW") else "fast"
        for kind in ("floor", "ceiling"):
            series[f"oxide {kind} {short}"] = curve("oxide", kind, team, rate)
    series["renegade ceiling slow, uncapped"] = curve("renegade", "ceiling", team,
                                                     "EXP_RATE_MEDIUM_SLOW", capped=False)
    print(f"team of {team}; levels at each split's end", file=out)
    print(f"{'split':9}{'cap':>4}" + "".join(f"{k:>34}" for k in series), file=out)
    for i, split in enumerate(splits()):
        cells = "".join(f"{series[k][i][3]:>34}" for k in series)
        print(f"{split:9}{caps[split]:>4}{cells}", file=out)
    supply, shops = candy_supply()
    print(f"\nRare Candies to reach each cap, team of {team}, entering each split at the"
          f" last cap (medium slow); the portable PC's are unlimited, so 'offered' counts"
          f" only the ones placed in the world"
          f"{'; shops selling them: ' + str(shops) if shops else ''}", file=out)
    print(f"{'split':9}{'cap':>4}{'floor reach':>12}{'needed':>8}{'ceiling reach':>14}{'needed':>8}"
          f"{'offered':>8}{'balance (ceiling)':>18}", file=out)
    floor, ceiling = candy_budget("floor", team), candy_budget("ceiling", team)
    for f, c in zip(floor, ceiling):
        print(f"{f[0]:9}{f[1]:>4}{f[2]:>12}{f[3]:>8}{c[2]:>14}{c[3]:>8}{c[4]:>8}{c[5]:>18}", file=out)
    return series


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--team", type=int, default=6)
    args = ap.parse_args(argv)
    report(args.team)
    return 0


if __name__ == "__main__":
    sys.exit(main())

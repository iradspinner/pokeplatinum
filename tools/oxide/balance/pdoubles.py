"""Double and tag battles for the perfect-line scorer (the prototype
README's step 2), a first version.

The perfect-line turn code plays one Pokemon a side, so a double battle is
played by fightsim's own four-actor battle (run_doubles: targeting, spread
moves, a tag battle's two opponents and Barry beside the player). A line
here is the order the six are sent out in: the lead pair first, then the
rest, which fightsim's doubles player follows when it replaces a knocked-out
Pokemon. The search screens every lead pair and a few orders of the rest,
confirms the best, and reports its clean-win rate, mean deaths and wipe
chance, as plines.search does for singles.

The dice are fightsim's own, at the game's odds on both sides; the luck
budget of the singles lines (every status chance against the player, one
critical hit) is not applied in doubles yet, and a reading says so
("dice": "game odds").
"""
import itertools
import random

from . import data, fightsim as fs, pressure


def prepare_story(fight, cap):
    """The fightsim state of a tag story fight, set for doubles: each
    opponent fills its own slot and Barry's partner teams stand beside the
    player, as fightsim.story reads it."""
    ox = data.oxide_trainers()
    trainers = data.fight_trainers("oxide", fight)
    parties = [t["party"] for t in trainers]
    weather = pressure.fight_weather([t["tr_id"] for t in trainers])
    partners = [ox[p]["party"] for p in fight.get("partner_ids", []) if p in ox]
    st = fs.prepare(fight["split"], parties, weather, bool(fight.get("trick_room")), cap=cap,
                    partners=partners, doubles=True)
    st["battle"] = "tag"
    st["group_flags"] = [t["ai"] for t in trainers]
    st["partner_flags"] = ox[fight["partner_ids"][0]]["ai"] if fight.get("partner_ids") else 0
    return st


def prepare_trainer(t, split, cap):
    """The fightsim state of one trainer's double battle."""
    st = fs.prepare(split, [t["party"]], pressure.fight_weather([t["tr_id"]]), cap=cap, doubles=True)
    st["battle"] = "doubles"
    st["group_flags"] = [t["ai"]]
    return st


def play(st, order, rng):
    """One double battle with the six sent out in this order: (clean win,
    won, Pokemon lost)."""
    if st["battle"] == "tag":
        partner = rng.choice(st["partners"]) if st.get("partners") else ()
        lost, won = fs.run_doubles(st, order, st["bosses"], rng, st["group_flags"], partner_keys=partner,
                                   partner_flags=st.get("partner_flags", 0), trick_room=st["trick_room"])
    else:
        lost, won = fs.run_doubles(st, order, [st["bosses"][0]], rng, st["group_flags"],
                                   trick_room=st["trick_room"])
    return won and lost == 0, won, lost


def stats(st, order, runs, rng):
    clean = deaths = wipes = 0
    for _ in range(runs):
        c, won, lost = play(st, order, rng)
        clean += c
        deaths += lost
        wipes += not won and lost == len(order)
    return clean / runs, deaths / runs, wipes / runs


def orders(team, rng, rest_orders):
    """Every lead pair, each with the rest in a few orders."""
    for pair in itertools.combinations(team, 2):
        rest = [k for k in team if k not in pair]
        seen = set()
        for _ in range(rest_orders):
            r = rest[:]
            rng.shuffle(r)
            if tuple(r) in seen:
                continue
            seen.add(tuple(r))
            yield list(pair) + r


def search(st, team, seed=0, screen_runs=20, keep=3, confirm_runs=200, rest_orders=2, **_ignored):
    """The best order's readings for this six: {"rate", "deaths", "wipe",
    "line", "candidates", "runs", "converged", "dice"}."""
    rng = random.Random(seed)
    scored = []
    for i, order in enumerate(orders(team, rng, rest_orders)):
        r, d, _w = stats(st, order, screen_runs, random.Random(seed * 7919 + i))
        scored.append((r, -d, i, order))
    scored.sort(key=lambda x: (-x[0], -x[1], x[2]))
    best = None
    for r, _nd, i, order in scored[:keep]:
        rate, deaths, wipe = stats(st, order, confirm_runs, random.Random(seed * 104729 + i))
        if best is None or (rate, -deaths) > (best[0], -best[1]):
            best = (rate, deaths, wipe, order)
    rate, deaths, wipe, order = best
    names = [st["pokemon"][k]["species"] for k in order]
    return {"rate": round(rate, 3), "deaths": round(deaths, 3), "wipe": round(wipe, 3),
            "line": f"lead {names[0]} and {names[1]}, then {', '.join(names[2:])}",
            "candidates": len(scored), "converged": True, "dice": "game odds",
            "screen": {len(scored): max(x[0] for x in scored)},
            "runs": len(scored) * screen_runs + min(keep, len(scored)) * confirm_runs}

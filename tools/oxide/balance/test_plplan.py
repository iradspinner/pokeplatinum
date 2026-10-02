"""The planner's pieces (plplan.py): the trainer's exact choice odds against
the AI's own sampled picks, the battle copy, the keyed dice, and a turn's
exact outcomes against the turn sampled at real odds.

    PYTHONPATH=. python3 -m tools.oxide.balance.test_plplan
"""
import collections
import random
import sys

from . import fightai
from . import fightsim as fs
from . import perfectline as pl
from . import plplan
from . import plstep3

RESULTS = []


def check(name, ok, detail=""):
    RESULTS.append(ok)
    print(f"  {'ok  ' if ok else 'FAIL'}  {name:70} {detail}")


def fight_state(fight):
    f = plstep3.FIGHTS[fight]
    prep = plstep3.prepare(f, f["six"], f["items"])
    bk, flags, _s = prep["variants"][0]
    return prep["st"], [f"p{i}" for i in range(6)], bk, flags, f["six"]


def states():
    """(label, battle) at points of the three gyms where the AI's pick is
    uncertain: each foe against several of the hand six, some hurt."""
    out = []
    for fight in ("roark", "mars", "gardenia"):
        st, team, bk, flags, names = fight_state(fight)
        for lead in range(6):
            for foe in range(len(bk)):
                b = pl.make_battle(st, team, bk, flags, lead)
                if foe:
                    b.b.mons[0].hp = 0
                    fs.switch_in(b, b.b, foe)
                if (lead + foe) % 3 == 1:
                    b.p.cur().hp = max(1, b.p.cur().hp * 2 // 5)
                if (lead + foe) % 4 == 2:
                    b.b.cur().hp = max(1, b.b.cur().hp // 2)
                b.turn = 1 if (lead + foe) % 2 else 0
                out.append((f"{fight}: {b.b.cur().species} on {names[lead]}", b))
    return out


def sampled(b, n, seed):
    counts = collections.Counter()
    for i in range(n):
        c = plplan.clone(b)
        c.quick = {}
        c.rng = random.Random(seed * 100003 + i)
        a = fightai.choose(c, c.b.cur(), c.p.cur())
        counts[(a[0], a[1].name if a[0] == "move" else a[1])] += 1
    return {k: v / n for k, v in counts.items()}


def exact_odds():
    """Over many states, the exact odds sit within sampling error of the
    AI's own frequencies (four standard errors), and every pick the AI made
    has odds above zero."""
    n = 3000
    worst, bad, tried = 0.0, [], 0
    for label, b in states():
        c = plplan.clone(b)
        c.quick = {}
        dist = plplan.ai_distribution(c)
        exact = {(a[0], a[1].name if a[0] == "move" else a[1]): p for a, p in dist}
        freq = sampled(b, n, len(label))
        tried += 1
        if abs(sum(exact.values()) - 1) > 1e-9:
            bad.append((label, "odds do not sum to 1"))
        for k in set(exact) | set(freq):
            p, f = exact.get(k, 0.0), freq.get(k, 0.0)
            se = max((p * (1 - p) / n) ** 0.5, 1 / n)
            z = abs(p - f) / se
            worst = max(worst, z)
            if z > 4 or (f > 0 and p == 0):
                bad.append((label, k, round(p, 3), round(f, 3)))
    check("the exact odds match the AI's sampled picks", not bad,
          f"{tried} states, worst gap {worst:.1f} standard errors; {bad[:3]}")


def store_fingerprints():
    """The fingerprint cache gives back what was put under a key, misses a
    key it never saw, and stays within its cap."""
    s = plplan.Store(3)
    keys = [(i, ("a", i), None) for i in range(5)]
    for k in keys[:3]:
        s.put(k, k[0])
    hits = [s.get(k) for k in keys[:3]]
    miss = s.get(keys[4])
    s.put(keys[3], 3)
    check("the cache returns its entries, misses unknown keys and keeps its cap",
          hits == [0, 1, 2] and miss is None and len(s.d) <= 3, (hits, miss, len(s.d)))


def pick_odds_rules():
    """Ties split evenly, and a sure higher score always wins."""
    d = plplan.pick_odds([{100: 1.0}, {100: 1.0}, {90: 1.0}])
    check("two slots tied at the top split the pick", abs(d[0] - 0.5) < 1e-12 and d[2] == 0, d)
    d = plplan.pick_odds([{100: 0.5, 101: 0.5}, {100: 1.0}])
    check("a slot that scores higher half the time and ties otherwise", abs(d[0] - 0.75) < 1e-12, d)


def clone_is_separate():
    st, team, bk, flags, _n = fight_state("roark")
    b = pl.make_battle(st, team, bk, flags, 0)
    b.p.cur().last = b.p.cur().moves[0]
    c = plplan.clone(b)
    fightai.record_last_move(c.p.cur())
    c.p.cur().hp -= 5
    c.b.cur().stages["atk"] = -1
    check("a copy's changes leave the original alone",
          b.p.cur().shown == [] and b.p.cur().hp == b.p.cur().maxhp and b.b.cur().stages["atk"] == 0,
          (b.p.cur().shown, c.p.cur().shown))


def turn_odds():
    """The exact enumeration of a turn agrees with the turn sampled at real
    odds: its outcomes' probabilities sum to one, and the chance that the
    target faints matches the sampled frequency (four standard errors).
    Steenee's Razor Leaf on Lileep, and Lileep's Rock Tomb on Steenee while
    Steenee Splashes, each at the first HP where the knockout is uncertain."""
    st, team, bk, flags, names = fight_state("roark")
    s_i = names.index("Steenee")

    def start():
        b = pl.make_battle(st, team, bk, flags, s_i)
        b.b.mons[0].hp = 0
        fs.switch_in(b, b.b, 2)
        b.quick = {}
        return b

    def move(mon, name):
        return "move", next(m for m in mon.moves if m.name == name)

    cases = []
    for side, mine, theirs in (("b", "Razor Leaf", "Ingrain"), ("p", "Splash", "Rock Tomb")):
        for hp in range(2, 40):
            b = start()
            target = b.b.cur() if side == "b" else b.p.cur()
            target.hp = hp
            pa, aa = move(b.p.cur(), mine), move(b.b.cur(), theirs)
            outs = plplan.turn_outcomes(b, pa, aa, 1)
            dead = sum(p for c, p in outs if not (c.b.mons[2] if side == "b" else c.p.mons[s_i]).alive())
            if 0.05 < dead < 0.95:
                cases.append((side, hp, b, pa, aa, outs, dead))
                break
    for side, hp, b, pa, aa, outs, dead in cases:
        total = sum(p for _c, p in outs)
        n, hits = 4000, 0
        for i in range(n):
            c = plplan.clone(b)
            rng = random.Random(i)
            c.dice, c.rng = pl.RunDice(rng, luck="real"), rng
            pl._turn(c, pa, aa)
            hits += not (c.b.mons[2] if side == "b" else c.p.mons[s_i]).alive()
        z = abs(dead - hits / n) / max((dead * (1 - dead) / n) ** 0.5, 1 / n)
        who = "Lileep" if side == "b" else "Steenee"
        check(f"{who} at {hp} HP: the turn's outcomes sum to one and its faint chance matches",
              abs(total - 1) < 1e-9 and z < 4,
              f"{len(outs)} outcomes; exact {dead:.3f}, sampled {hits / n:.3f}")
    check("both uncertain knockouts were found", len(cases) == 2, [c[:2] for c in cases])


def keyed_dice_share_luck():
    """Two copies on the same key draw the same numbers on the same turn."""
    st, team, bk, flags, _n = fight_state("roark")
    b = pl.make_battle(st, team, bk, flags, 0)
    c1, c2 = plplan.clone(b), plplan.clone(b)
    r1, r2 = plplan.KeyedRandom(5, c1), plplan.KeyedRandom(5, c2)
    a = [r1.random() for _ in range(3)]
    bb = [r2.random() for _ in range(3)]
    c1.turn += 1
    nxt = r1.random()
    check("keyed dice repeat on the same key and turn, and move on with the turn",
          a == bb and nxt != a[0], (a[0], bb[0], nxt))


def main():
    print("the planner's pieces")
    pick_odds_rules()
    store_fingerprints()
    clone_is_separate()
    keyed_dice_share_luck()
    turn_odds()
    exact_odds()
    print(f"\n{sum(RESULTS)}/{len(RESULTS)} passed")
    return 0 if all(RESULTS) else 1


if __name__ == "__main__":
    sys.exit(main())

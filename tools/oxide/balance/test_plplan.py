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
            q = min(max(p, 0.0), 1.0)      # a sum of odds can land a rounding hair above 1
            se = max((q * (1 - q) / n) ** 0.5, 1 / n)
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
    Steenee's Razor Leaf on Lileep while Lileep uses Mega Drain, and Lileep's
    Ancient Power on Steenee while Steenee Splashes, each at the first HP
    where the knockout is uncertain. Lileep is found in Roark's team by
    species, so a reordered team (his redesign of 2026-10-12 moved it from
    third to second, and Acid became Mega Drain) does not break the test."""
    st, team, bk, flags, names = fight_state("roark")
    s_i = names.index("Steenee")
    l_i = next(i for i, m in enumerate(pl.make_battle(st, team, bk, flags, s_i).b.mons)
               if m.species == "Lileep")

    def start():
        b = pl.make_battle(st, team, bk, flags, s_i)
        b.b.mons[0].hp = 0
        fs.switch_in(b, b.b, l_i)
        b.quick = {}
        return b

    def move(mon, name):
        return "move", next(m for m in mon.moves if m.name == name)

    cases = []
    for side, mine, theirs in (("b", "Razor Leaf", "Mega Drain"), ("p", "Splash", "Ancient Power")):
        for hp in range(2, 40):
            b = start()
            target = b.b.cur() if side == "b" else b.p.cur()
            target.hp = hp
            pa, aa = move(b.p.cur(), mine), move(b.b.cur(), theirs)
            outs = plplan.turn_outcomes(b, pa, aa, 1)
            dead = sum(p for c, p in outs if not (c.b.mons[l_i] if side == "b" else c.p.mons[s_i]).alive())
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
            hits += not (c.b.mons[l_i] if side == "b" else c.p.mons[s_i]).alive()
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


def future_sight_through_planner():
    """A waiting Future Sight (approved 2026-10-13) rides through the
    planner: its copy of a battle carries the hit, every outcome of the turn
    it comes due on has it landed, and positions that differ only in a
    waiting hit are never merged as one."""
    st, team, bk, flags, names = fight_state("roark")
    b = pl.make_battle(st, team, bk, flags, names.index("Steenee"))
    b.quick = {}
    foe = b.b.cur()
    due = (1, 12, "Future Sight", "p", 0)
    b.b.future, b.b.future_sight = (due, None), True
    c = plplan.clone(b)
    copied = c.b.future == b.b.future and c.b.future_sight
    pa = ("move", next(m for m in b.p.cur().moves if m.name == "Splash"))
    aa = ("move", next(m for m in foe.moves if m.cat == "Status" and m.range != "SINGLE_TARGET")
          if any(m.cat == "Status" and m.range != "SINGLE_TARGET" for m in foe.moves) else foe.moves[0])
    outs = plplan.turn_outcomes(b, pa, aa, 1)
    landed = all(o.b.future == (None, None) and not o.b.future_sight for o, _p in outs)
    hp = sorted({o.b.mons[b.b.active].hp for o, _p in outs})
    later = plplan.clone(b)
    later.b.future = ((2,) + due[1:], None)
    merged = plplan.merge_key(later) == plplan.merge_key(b)
    check("a waiting Future Sight rides through the planner's copies and turns",
          copied and landed and not merged and outs and max(hp) <= foe.maxhp - 12,
          f"copied {copied}; landed in every outcome {landed}; the target's HP after the turn {hp} of "
          f"{foe.maxhp}; merged with a later one {merged}")


def disabled_left_out():
    """A disabled move (approved 2026-10-13) is left out of the planner's
    options, its plain policy's attack and its last resort, as the engine
    keeps it out of the choice."""
    st, team, bk, flags, names = fight_state("roark")
    b = pl.make_battle(st, team, bk, flags, names.index("Barboach"))
    me = b.p.cur()
    best = plplan.strongest(b)[1].name
    me.disabled, me.disabled_turns = best, 3
    opts = [a[1].name for a in plplan.options(b) if a[0] == "move"]
    after = plplan.strongest(b)[1].name
    plain = plplan.plain(b)
    check("a disabled move is out of the planner's options and its plain attack",
          best not in opts and after != best and not (plain[0] == "move" and plain[1].name == best),
          f"the strongest {best}, then {after}; options {opts}; plain {plain[0]} "
          f"{plain[1].name if plain[0] == 'move' else plain[1]}")


def encore_leaves_one_move():
    """Under Encore (approved 2026-10-14) the planner's options are the
    Encore move and the switches; its plain policy's pick comes out as the
    Encore move when used."""
    st, team, bk, flags, names = fight_state("roark")
    b = pl.make_battle(st, team, bk, flags, names.index("Barboach"))
    me = b.p.cur()
    me.encore, me.encore_turns = "Mud-Slap", 3
    opts = [a for a in plplan.options(b)]
    moves = [a[1].name for a in opts if a[0] == "move"]
    switches = sum(1 for a in opts if a[0] == "switch")
    used = fs.encored_move(me, plplan.strongest(b)[1]).name
    check("under Encore the planner chooses the Encore move or a switch",
          moves == ["Mud-Slap"] and switches == 5 and used == "Mud-Slap",
          f"moves {moves}; switches {switches}; the plain pick used as {used}")


def offered(b):
    """The names of the moves plplan.options offers at b."""
    return sorted(a[1].name for a in plplan.options(b) if a[0] == "move")


def options_by_rule():
    """The options drop only a move that would fail or do nothing by the
    battle's own rules (approved 2026-10-15; plplan.would_fail), on the
    calculator's real rows: Knock Off on a target holding nothing, Healing
    Wish with a hurt Pokemon to send in, Dragon Dance at +6 Attack with
    Speed to raise, and Copycat on the first turn against a target that
    knows a faster move are offered, though the trainer's AI's Basic check
    scores each at -10 or below; Healing Wish with no one to mend, Copycat
    with nothing it could copy and Thunder Wave on a Ground type are not;
    Me First is offered while the target may use a hit after it."""
    from .test_fightai import battle
    out = {}
    b = battle([("Machop", 30, "Guts", ["Tackle"])], [("Absol", 30, "Pressure", ["Knock Off", "Thunder Wave"])])
    b.b.cur().item = None
    out["Knock Off, no item"] = offered(b)
    for hurt in (True, False):
        b = battle([("Machop", 30, "Guts", ["Tackle"])],
                   [("Togekiss", 30, "Serene Grace", ["Healing Wish", "Air Slash"]),
                    ("Bibarel", 30, "Unaware", ["Tackle"])])
        if hurt:
            b.p.mons[1].hp //= 2
        out["Healing Wish, " + ("a hurt mate" if hurt else "all well")] = offered(b)
    b = battle([("Machop", 30, "Guts", ["Tackle"])], [("Gyarados", 30, "Intimidate", ["Dragon Dance", "Waterfall"])])
    b.p.cur().stages["atk"] = 6
    out["Dragon Dance at +6 Attack"] = offered(b)
    for case, foe_moves, last in (("nothing to copy", ["Tackle"], None), ("a faster foe move", ["Extreme Speed"], None),
                                  ("a last move", ["Tackle"], "Tackle")):
        b = battle([("Machop", 20, "Guts", foe_moves)], [("Ninjask", 40, "Infiltrator", ["Copycat", "Me First"])])
        b.last_move = fs.move(last) if last else None
        out["Copycat, " + case] = offered(b)
    b = battle([("Diglett", 30, "Sand Veil", ["Tackle"])], [("Pikachu", 30, "Static", ["Thunder Wave", "Quick Attack"])])
    out["Thunder Wave on a Ground type"] = offered(b)
    want = {"Knock Off, no item": ["Knock Off", "Thunder Wave"],
            "Healing Wish, a hurt mate": ["Air Slash", "Healing Wish"], "Healing Wish, all well": ["Air Slash"],
            "Dragon Dance at +6 Attack": ["Dragon Dance", "Waterfall"],
            "Copycat, nothing to copy": ["Me First"], "Copycat, a faster foe move": ["Copycat", "Me First"],
            "Copycat, a last move": ["Copycat", "Me First"], "Thunder Wave on a Ground type": ["Quick Attack"]}
    check("the options drop only moves the battle's rules would fail", out == want,
          "; ".join(f"{k} {v}" for k, v in out.items()))


def idle_moves_picked():
    """Mud Sport and Magic Room are off the team search's idle list
    (approved 2026-10-15; plteam.IDLE), as their effects run: on real rows
    a Pikachu with four Electric moves and Mud Sport takes Mud Sport as its
    status move against a trainer's Bibarel, in place of its fourth
    Electric move, where it took it only when nothing else was left;
    Splash stays idle."""
    from . import plteam
    from .test_fightai import _prepared
    boss = (("Bibarel", 20, "Unaware", ("Tackle",), None),)
    out = {}
    for extra in ("Mud Sport", "Splash"):
        player = (("Pikachu", 20, "Static", ("Thunder Shock", "Spark", "Nuzzle", "Thunderbolt", extra), None),)
        st = _prepared(boss, player, "Roark", None)
        mine, _theirs, _speed = plteam.matchups(st, ["p0"], st["bosses"][0])
        out[extra] = extra in plteam.pick_moves(st, "p0", st["bosses"][0], mine)
    check("Mud Sport is no longer an idle move for the team search", out == {"Mud Sport": True, "Splash": False},
          f"picked {out}")


def keys_hold_new_states():
    """The planner's merge key holds every battle state the batches added
    (approved 2026-10-15): two positions of Roark's fight that differ only
    by Lucky Chant or Sticky Web on a side, Gravity's or Magic Room's turns,
    Copycat's last move or deep fog no longer merge; the search's shape key
    tells Aurora Veil apart, the trainer's AI's key Aurora Veil too, and a
    Belch user's keys whether it has eaten a Berry."""
    st, team, bk, flags, _names = fight_state("roark")
    base = pl.make_battle(st, team, bk, flags, 0)
    changes = {"Lucky Chant": lambda c: setattr(c.p, "lucky_chant", 3),
               "Sticky Web": lambda c: setattr(c.b, "web", 1),
               "Gravity": lambda c: setattr(c, "gravity", 3),
               "Magic Room": lambda c: setattr(c, "magic_room", 3),
               "Copycat's last move": lambda c: setattr(c, "last_move", fs.move("Tackle")),
               "deep fog": lambda c: setattr(c, "fog", True)}
    out = {}
    for name, change in changes.items():
        c = plplan.clone(base)
        change(c)
        out[name] = plplan.merge_key(c) != plplan.merge_key(base)
    c = plplan.clone(base)
    c.p.aurora_veil = 3
    out["Aurora Veil, shape"] = pl.shape_key(c) != pl.shape_key(base)
    out["Aurora Veil, AI"] = pl.ai_key(c) != pl.ai_key(base)
    c = plplan.clone(base)
    m = c.p.cur()
    m.belch = True
    plain = pl.mon_key(m)
    m.ate_berry = True
    out["a Belch user's Berry"] = pl.mon_key(m) != plain
    check("the planner's keys hold the states the batches added", all(out.values()), str(out))


def main():
    print("the planner's pieces")
    pick_odds_rules()
    store_fingerprints()
    clone_is_separate()
    keyed_dice_share_luck()
    turn_odds()
    exact_odds()
    future_sight_through_planner()
    disabled_left_out()
    encore_leaves_one_move()
    options_by_rule()
    idle_moves_picked()
    keys_hold_new_states()
    print(f"\n{sum(RESULTS)}/{len(RESULTS)} passed")
    return 0 if all(RESULTS) else 1


if __name__ == "__main__":
    sys.exit(main())

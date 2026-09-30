"""The mechanics the Roark fight showed missing from the perfect-line
simulator, each checked on that fight (the Overseer, 2026-09-30).

    PYTHONPATH=. python3 -m tools.oxide.balance.test_plfixes
"""
import random

from . import fightai, plscore, perfectline as pl, fightsim as fs

IV = {k: 15 for k in ("hp", "at", "df", "sp", "sa", "sd")}
EV = {k: 0 for k in IV}
TEAM = [("SPECIES_BARBOACH", "Barboach", "Lonely", "Swift Swim", ["Mud Bomb", "Water Gun", "Mud-Slap"]),
        ("SPECIES_NACLI", "Nacli", "Impish", "Sturdy", ["Mud Shot", "Rock Throw", "Harden", "Headbutt"]),
        ("SPECIES_GRUBBIN", "Grubbin", "Relaxed", "Swarm", ["Bug Bite", "Bite", "Mud-Slap"])]


def battle(seed=1):
    recs = [{"constant": c, "species": s, "how": "test", "level": 16, "nature": n, "ivs": IV, "evs": EV,
             "ability": a, "moves": mv, "fill": False} for c, s, n, a, mv in TEAM]
    prep = plscore.prepare(plscore.parse_fight("roark"), given_side=recs)
    boss_keys, flags, _ = prep["variants"][0]
    b = pl.make_battle(prep["st"], ["p0", "p1", "p2"], boss_keys, flags, 0)
    for m in b.p.mons:
        m.item = None
    rng = random.Random(seed)
    b.dice = pl.RunDice(rng, True)
    b.rng = rng
    return b


def mv(mon, name):
    return next(m for m in mon.moves if m.name == name)


def boss(b, species):
    i = next(i for i, m in enumerate(b.b.mons) if m.species == species)
    fs.switch_in(b, b.b, i)
    return b.b.cur()


def main():
    results = []

    # Block traps its target until Nosepass leaves; a trapped Pokemon cannot
    # switch; the AI does not Block a target already trapped.
    b = battle()
    nose, barb = b.b.cur(), b.p.cur()
    pl.status_move(b, nose, mv(nose, "Block"), barb, True)
    trapped = barb.trapped_by == nose.key and not fs.can_switch(barb)
    try:
        pl._turn(b, ("switch", 1), ("move", mv(nose, "Rock Throw")))
        refused = False
    except ValueError:
        refused = True
    rescore = fightai.basic(b, nose, barb, mv(nose, "Block"), 1)
    boss(b, "Geodude")
    freed = barb.trapped_by is None
    results.append(("Block traps until its user leaves, and a second Block scores -10",
                    trapped and refused and rescore == -10 and freed,
                    f"trapped {trapped}, switch refused {refused}, Block {rescore}, freed {freed}"))

    # Apicot Berry: +1 Special Defense at a quarter HP, eaten.
    b = battle()
    nose = b.b.cur()
    fs.hurt(b, nose, nose.hp - nose.maxhp // 4)
    results.append(("Apicot Berry raises Special Defense at a quarter HP and is eaten",
                    nose.stages["spd"] == 1 and nose.item is None, f"spd {nose.stages['spd']}, item {nose.item}"))

    # Sitrus fires on the hit that takes it to half, not at the end of the turn.
    b = battle()
    cran = boss(b, "Cranidos")
    before = cran.hp
    fs.hurt(b, cran, cran.hp - cran.maxhp // 2 + 1)
    low = cran.maxhp // 2 - 1
    results.append(("Sitrus Berry heals a quarter as soon as the holder falls to half",
                    cran.item is None and cran.hp == low + cran.maxhp // 4,
                    f"{before} -> {cran.hp}, item {cran.item}"))

    # Mold Breaker ignores Sturdy: Cranidos can knock out a full-HP Sturdy Nacli.
    b = battle()
    cran = boss(b, "Cranidos")
    fs.switch_in(b, b.p, 1)
    nacli = b.p.cur()
    cran.stages["atk"] = 6
    rock = mv(cran, "Rock Throw")
    for _ in range(20):
        if not nacli.alive():
            break
        nacli.hp = nacli.maxhp
        pl.attack(b, cran, rock, nacli, True)
    results.append(("Mold Breaker's hit ignores Sturdy", not nacli.alive(), f"Nacli {nacli.hp}/{nacli.maxhp}"))

    # Pursuit doubles against a Pokemon switching out, and hits before the switch.
    b = battle(3)
    cran = boss(b, "Cranidos")
    barb = b.p.cur()
    pl._turn(b, ("switch", 1), ("move", mv(cran, "Pursuit")))
    hit_out = barb.hp < barb.maxhp and b.p.cur().species == "Nacli" and b.p.cur().hp == b.p.cur().maxhp - int(
        b.p.cur().maxhp * b.st["rock_eff"].get(b.p.cur().key, 1) / 8) * bool(b.p.hazards["rocks"])
    plain = battle(3)
    c2 = boss(plain, "Cranidos")
    pl.attack(plain, c2, mv(c2, "Pursuit"), plain.p.cur(), True)
    doubled = (barb.maxhp - barb.hp) > (plain.p.cur().maxhp - plain.p.cur().hp)
    results.append(("Pursuit hits the Pokemon switching out, harder than a plain Pursuit",
                    hit_out and doubled, f"switching {barb.maxhp - barb.hp}, plain {plain.p.cur().maxhp - plain.p.cur().hp}"))

    # Big Root: Mega Drain restores 30% more.
    b = battle()
    lil = boss(b, "Lileep")
    fs.switch_in(b, b.p, 1)
    lil.hp = 10
    pl.attack(b, lil, mv(lil, "Mega Drain"), b.p.cur(), True)
    dealt = b.p.cur().maxhp - b.p.cur().hp
    results.append(("Big Root raises Mega Drain's heal by 30%", lil.hp == min(lil.maxhp, 10 + int((dealt // 2) * 1.3)),
                    f"dealt {dealt}, Lileep 10 -> {lil.hp}"))

    # Ingrain: roots the user (no switching, no second Ingrain) and heals a
    # sixteenth a turn, 30% more with Big Root.
    b = battle()
    lil = boss(b, "Lileep")
    pl.status_move(b, lil, mv(lil, "Ingrain"), b.p.cur(), True)
    lil.hp = 20
    fs.end_of_turn(b)
    gain = lil.hp - 20
    results.append(("Ingrain roots Lileep and heals a sixteenth, a third more with Big Root",
                    not fs.can_switch(lil) and fightai.basic(b, lil, b.p.cur(), mv(lil, "Ingrain"), 1) == -10
                    and gain == int((lil.maxhp // 16) * 1.3),
                    f"healed {gain} of {lil.maxhp}"))

    # Bug Bite eats the target's Sitrus Berry: the user heals, the berry is gone.
    b = battle()
    cran = boss(b, "Cranidos")
    fs.switch_in(b, b.p, 2)
    grub = b.p.cur()
    grub.hp = 10
    pl.attack(b, grub, mv(grub, "Bug Bite"), cran, True)
    results.append(("Bug Bite eats Cranidos's Sitrus Berry", cran.item is None and grub.hp == 10 + grub.maxhp // 4,
                    f"Grubbin 10 -> {grub.hp}, Cranidos item {cran.item}"))

    width = max(len(r[0]) for r in results)
    for name, ok, note in results:
        print(f"  {'ok  ' if ok else 'FAIL'}  {name:{width}}  {note}")
    passed = sum(1 for r in results if r[1])
    print(f"\n{passed}/{len(results)} passed")
    return 0 if passed == len(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())

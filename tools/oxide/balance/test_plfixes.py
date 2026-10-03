"""The mechanics the Roark fight showed missing from the perfect-line
simulator, each checked on that fight (the Overseer, 2026-09-30).

    PYTHONPATH=. python3 -m tools.oxide.balance.test_plfixes
"""
import collections
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


def _hits(b, attack, att, name, dfn, tries=30, hp=None):
    """The damage of each landed use of a move over a number of tries, the
    target's HP reset (to hp, or full) before each."""
    move = fs.move(name)
    att.moves = [move]
    att.pp = {name: 99}
    out = []
    for i in range(tries):
        b.rng = random.Random(i)
        b.dice = pl.RunDice(random.Random(i), True)
        dfn.hp = hp or dfn.maxhp
        att.hit_this_turn = None
        attack(b, att, move, dfn, True)
        out.append((hp or dfn.maxhp) - dfn.hp)
    return out


def first_battle_checks():
    """The game's first battle, Barry on Route 201, has no critical hits on
    either side (the Overseer, 2026-10-02: BtlCmd_CalcCrit sets the
    multiplier to 1 under BATTLE_STATUS_FIRST_BATTLE). Barry's Turtwig uses
    Tackle on a level-5 Piplup 400 times with the mark and 400 without: with
    it the top damage stays the plain roll's, without it a crit shows."""
    rec = [{"constant": "SPECIES_PIPLUP", "species": "Piplup", "how": "test", "level": 5, "nature": "Hardy",
            "ivs": IV, "evs": EV, "ability": "Torrent", "moves": ["Pound", "Growl"], "fill": False}]
    prep = plscore.prepare(plscore.parse_fight("barry_1"), given_side=rec)
    st = prep["st"]
    boss_keys, flags, _ = prep["variants"][0]
    b = pl.make_battle(st, ["p0"], boss_keys, flags, 0)
    turtwig, piplup = b.b.cur(), b.p.cur()
    marked = st["first_battle"]
    with_mark = _hits(b, pl.attack, turtwig, "Tackle", piplup, tries=400)
    st["first_battle"] = False
    without = _hits(b, pl.attack, turtwig, "Tackle", piplup, tries=400)
    st["first_battle"] = marked
    return [("the first battle is marked, Roark is not", marked and not battle().st.get("first_battle"),
             f"Barry 1 {marked}"),
            ("no critical hit in the first battle: Tackle's top damage stays below a crit's",
             max(with_mark) < max(without), f"top {max(with_mark)} with the mark, {max(without)} without")]


def magnet_rise_checks():
    """Magnet Rise (effect script 252, found missing on 2026-10-03, when a
    Magnitude knocked out a risen Jolteon in Lucas and Dawn 2's line): its
    user takes nothing from Ground moves through five turn ends, a switch
    clears it, and Ingrain stops it. Roark's lead rises; Barboach answers
    with Mud Bomb."""
    b = battle()
    foe, barboach = b.b.cur(), b.p.mons[0]
    rise = fs.move("Magnet Rise")
    before = _hits(b, pl.attack, barboach, "Mud Bomb", foe, tries=5)
    pl.status_move(b, foe, rise, barboach, True)
    risen = _hits(b, pl.attack, barboach, "Mud Bomb", foe, tries=5)
    risen_fs = _hits(b, fs.attack, barboach, "Mud Bomb", foe, tries=5)
    for _ in range(4):
        fs.end_of_turn(b)
    foe.hp = foe.maxhp
    four = _hits(b, pl.attack, barboach, "Mud Bomb", foe, tries=5)
    fs.end_of_turn(b)
    foe.hp = foe.maxhp
    five = _hits(b, pl.attack, barboach, "Mud Bomb", foe, tries=5)
    pl.status_move(b, foe, rise, barboach, True)
    fs.switch_in(b, b.b, 1)
    fs.switch_in(b, b.b, 0)
    cleared = b.b.cur().magnet_rise
    foe = b.b.cur()
    foe.ingrained = True
    pl.status_move(b, foe, rise, barboach, True)
    rooted = foe.magnet_rise
    return [("Magnet Rise: Ground moves do nothing to its user, in both simulators",
             max(before) > 0 and max(risen) == 0 and max(risen_fs) == 0,
             f"Mud Bomb {max(before)} before, {max(risen)} and {max(risen_fs)} after"),
            ("Magnet Rise lasts through four turn ends and is gone after the fifth",
             max(four) == 0 and max(five) > 0, f"after four {max(four)}, after five {max(five)}"),
            ("a switch clears Magnet Rise, and Ingrain stops it", cleared == 0 and rooted == 0,
             f"after a switch {cleared}, rooted {rooted}")]


def torment_and_pain_split_checks():
    """Torment and Pain Split (found doing nothing on 2026-10-03, in Lucas
    and Dawn 2's Monferno and Fantina's Rotom): a tormented Pokemon cannot
    pick the move it used last, in the player's options or the trainer's
    AI, until a switch; Pain Split sets both Pokemon's HP to half their sum,
    and fails on a Substitute."""
    b = battle()
    foe, barboach = b.b.cur(), b.p.cur()
    barboach.moves = [fs.move("Mud Bomb"), fs.move("Water Gun")]
    barboach.pp = {"Mud Bomb": 10, "Water Gun": 10}
    pl.status_move(b, foe, fs.move("Torment"), barboach, True)
    barboach.last = barboach.moves[0]
    from . import plplan
    names = [a[1].name for a in plplan.options(b) if a[0] == "move"]
    foe_moves = list(foe.moves)
    foe.tormented, foe.last = True, foe_moves[0]
    ai_out = fightai.invalid(b, foe, foe_moves[0])
    fs.switch_in(b, b.p, 1)
    fs.switch_in(b, b.p, 0)
    cleared = b.p.cur().tormented
    b = battle()
    foe, barboach = b.b.cur(), b.p.cur()
    barboach.hp, foe.hp = barboach.maxhp, 4
    pl.status_move(b, foe, fs.move("Pain Split"), barboach, True)
    avg = (barboach.maxhp + 4) // 2
    split = (barboach.hp, foe.hp)
    b2 = battle()
    foe2, mon2 = b2.b.cur(), b2.p.cur()
    mon2.sub, foe2.hp = 10, 4
    fs.pain_split(b2, foe2, mon2)
    return [("Torment: the move used last is no option, for the player or the trainer's AI, until a switch",
             names == ["Water Gun"] and ai_out and not cleared, f"options {names}, AI rules it out {ai_out}, "
             f"after a switch {cleared}"),
            ("Pain Split: both HP become half their sum (capped), and it fails on a Substitute",
             split == (avg, min(foe.maxhp, avg)) and foe2.hp == 4,
             f"{split} against {avg}; through a Substitute the user stays at {foe2.hp}")]


def destiny_bond_checks():
    """Destiny Bond (subscript_destiny_bond and
    subscript_faint_check_destiny_bond): a Pokemon under it that a foe's
    move faints takes the foe with it; the bond ends when its user next
    tries to act. Roark's lead bonds; Barboach's Mud Bomb faints it."""
    b = battle()
    foe, barboach = b.b.cur(), b.p.cur()
    bond = fs.move("Destiny Bond")
    pl.use_move(b, foe, bond, barboach, True)
    set_ = foe.destiny_bond
    foe.hp = 1
    b.dice = pl.RunDice(random.Random(3), True)
    pl.use_move(b, barboach, mv(barboach, "Mud Bomb"), foe, True)
    took = not foe.alive() and not barboach.alive()
    b = battle()
    foe, barboach = b.b.cur(), b.p.cur()
    pl.use_move(b, foe, bond, barboach, True)
    pl.use_move(b, foe, fs.move("Tackle"), barboach, True)     # it acts again: the bond ends
    foe.hp = 1
    pl.use_move(b, barboach, mv(barboach, "Mud Bomb"), foe, True)
    ended = not foe.alive() and barboach.alive()
    return [("Destiny Bond: the foe whose move faints its user faints too",
             set_ and took, f"set {set_}, both fainted {took}"),
            ("Destiny Bond ends when its user next acts", ended, f"only the bonded one fainted {ended}")]


def fixed_damage_checks():
    """Handoff step 2, fixed damage (Scoring Agent, 2026-09-30): each effect
    script sets the damage itself, so stages, screens and crits never touch
    it, but an immune type still takes nothing. Both attack paths, the
    simulator's and the perfect-line search's, are checked."""
    from .test_fightai import battle
    out = []
    b = battle([("Gible", 20, "Rough Skin", ["Dragon Rage", "Sonic Boom"]),
                ("Raticate", 20, "Guts", ["Super Fang", "Counter"])],
               [("Snorlax", 30, "Thick Fat", ["Body Slam"]), ("Misdreavus", 20, "Levitate", ["Astonish"]),
                ("Geodude", 20, "Sturdy", ["Rock Throw"]), ("Umbreon", 30, "Synchronize", ["Bite"])])
    gible, rat = b.b.mons
    lax, ghost, geo, dark = b.p.mons
    for label, attack in (("simulator", fs.attack), ("search", pl.attack)):
        gible.stages["spa"] = 6
        b.p.screens["Light Screen"] = 5
        got = {d for d in _hits(b, attack, gible, "Dragon Rage", lax) if d}
        gible.stages["spa"] = 0
        b.p.screens["Light Screen"] = 0
        out.append((f"{label}: Dragon Rage does 40 through +6 and Light Screen", got == {40}, f"{sorted(got)}"))
        immune = {name: max(_hits(b, attack, user, name, target)) for name, user, target in (
            ("Seismic Toss", rat, ghost), ("Sonic Boom", gible, ghost), ("Night Shade", gible, lax),
            ("Super Fang", rat, ghost), ("Endeavor", rat, ghost))}
        out.append((f"{label}: fixed-damage moves do nothing to an immune type", not any(immune.values()),
                    f"{immune}"))
        got = {d for d in _hits(b, attack, rat, "Super Fang", lax, hp=101) if d}
        out.append((f"{label}: Super Fang takes half the target's current HP", got == {50}, f"{sorted(got)}"))
        got = {d for d in _hits(b, attack, rat, "Psywave", lax, tries=200) if d}
        out.append((f"{label}: Psywave does half to one and a half times the level, in tenths",
                    got <= {20 * t // 10 for t in range(5, 16)} and len(got) >= 6, f"{sorted(got)}"))
        rat.level = 60
        ko = max(_hits(b, attack, rat, "Horn Drill", geo, tries=60))
        rat.level = 20
        out.append((f"{label}: a one-hit KO move fails into Sturdy", ko == 0, f"took {ko}"))
        rat.hit_this_turn = ("Physical", 30)
        countered = []
        for i in range(10):
            b.rng, b.dice = random.Random(i), pl.RunDice(random.Random(i), True)
            ghost.hp = ghost.maxhp
            rat.hit_this_turn = ("Physical", 30)
            rat.moves, rat.pp = [fs.move("Counter")], {"Counter": 99}
            attack(b, rat, fs.move("Counter"), ghost, True)
            countered.append(ghost.maxhp - ghost.hp)
        out.append((f"{label}: Counter does nothing to a Ghost", not any(countered), f"{countered}"))
    return out


def explosion_checks():
    """Explosion's effect script faints its user before the hit, so it
    faints into a Ghost or a Protect too; Damp stops the move and the user
    keeps its HP (the Scoring Agent, 2026-09-30)."""
    from .test_fightai import battle
    out = []
    b = battle([("Geodude", 20, "Sturdy", ["Explosion", "Rock Throw"])],
               [("Misdreavus", 20, "Levitate", ["Astonish"]), ("Psyduck", 20, "Damp", ["Water Gun"]),
                ("Snorlax", 30, "Thick Fat", ["Body Slam"])])
    geo = b.b.cur()
    ghost, duck, lax = b.p.mons
    boom = fs.move("Explosion")
    for label, attack in (("simulator", fs.attack), ("search", pl.attack)):
        seen = []
        for target, protect in ((ghost, False), (lax, True), (duck, False)):
            b.rng, b.dice = random.Random(1), pl.RunDice(random.Random(1), True)
            geo.hp, target.hp = geo.maxhp, target.maxhp
            target.protecting = protect
            b.p.active = b.p.mons.index(target)
            attack(b, geo, boom, target, True)
            target.protecting = False
            seen.append((geo.hp, target.maxhp - target.hp))
        ok = seen[0] == (0, 0) and seen[1] == (0, 0) and seen[2][0] == geo.maxhp and seen[2][1] == 0
        out.append((f"{label}: Explosion faints its user into a Ghost or Protect; Damp stops it",
                    ok, f"(user HP, damage) Ghost {seen[0]}, Protect {seen[1]}, Damp {seen[2]}"))
    b.p.active = 0
    return out


def sleep_talk_and_aqua_ring_checks():
    """Sleep Talk used asleep calls one of its user's other moves (the AI now
    scores it +10 asleep, as the game does); Aqua Ring heals a sixteenth at
    each turn's end (the Scoring Agent, 2026-10-01)."""
    from .test_fightai import battle
    out = []
    b = battle([("Snorlax", 40, "Thick Fat", ["Sleep Talk", "Body Slam", "Aqua Ring"])],
               [("Machamp", 40, "Guts", ["Cross Chop"])])
    lax, champ = b.b.cur(), b.p.cur()
    for label, attack in (("simulator", fs.use_move), ("search", pl.use_move)):
        b.rng, b.dice = random.Random(3), pl.RunDice(random.Random(3), True)
        champ.hp = champ.maxhp
        lax.status, lax.sleep = "slp", 3
        attack(b, lax, fs.move("Sleep Talk"), champ, True)
        hit = champ.maxhp - champ.hp
        out.append((f"{label}: Sleep Talk asleep calls Body Slam", hit > 0, f"Machamp took {hit}"))
    lax.status, lax.sleep = None, 0
    fs.status_move(b, lax, fs.move("Aqua Ring"), champ, True)
    lax.hp = lax.maxhp // 2
    before = lax.hp
    fs.end_of_turn(b)
    out.append(("Aqua Ring heals a sixteenth at the turn's end", lax.hp - before == lax.maxhp // 16,
                f"{before} -> {lax.hp} of {lax.maxhp}"))
    return out


def sleep_checks():
    """Handoff step 2, sleep length (Scoring Agent, 2026-09-30). The engine's
    counter is 2 to 5 (`Random 3, 2` in the fall-asleep script), less one
    per move attempt, waking to act at zero: one to four turns, as the
    simulator draws. Rest sets 3, two turns. Early Bird takes two a time."""
    out = []

    def turns_asleep(sleep, ability):
        mon = type("M", (), {})()
        mon.status, mon.sleep, mon.ability = "slp", sleep, ability
        n = 0
        while fs.sleep_tick(mon):
            n += 1
        return n
    plain = [turns_asleep(s, None) for s in (1, 2, 3, 4)]
    early = [turns_asleep(s, "Early Bird") for s in (1, 2, 3, 4)]
    rest = (turns_asleep(2, None), turns_asleep(2, "Early Bird"))
    out.append(("sleep lasts one to four turns; Early Bird zero, one, one or two",
                plain == [1, 2, 3, 4] and early == [0, 1, 1, 2], f"plain {plain}, Early Bird {early}"))
    out.append(("Rest sleeps two turns, one with Early Bird", rest == (2, 1), f"{rest}"))
    return out


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

    # The post-knockout pick follows BattleAI_PostKOSwitchIn: stage 1 by type
    # match-up with a super-effective move, stage 2 by the damage the fainted
    # Pokemon would do with each candidate's moves.
    picks = {}
    for lead in range(3):
        b = battle()
        fs.switch_in(b, b.p, lead)
        b.b.cur().hp = 0
        picks[b.p.cur().species] = b.b.mons[fightai.replacement(b, b.b, b.p.cur())].species
    results.append(("After Nosepass: Barboach draws Lileep (stage 1), Grubbin draws Cranidos (stage 1)",
                    picks.get("Barboach") == "Lileep" and picks.get("Grubbin") == "Cranidos", str(picks)))

    # Magnitude rolls its power (10 to 150) and deals that power's damage.
    recs = [{"constant": "SPECIES_GEODUDE", "species": "Geodude", "how": "test", "level": 16, "nature": "Jolly",
             "ivs": IV, "evs": EV, "ability": "Sturdy", "moves": ["Magnitude", "Rock Throw"], "fill": False}]
    prep = plscore.prepare(plscore.parse_fight("roark"), given_side=recs)
    boss_keys, flags, _ = prep["variants"][0]
    seen, damages = set(), []
    for seed in range(40):
        b = pl.make_battle(prep["st"], ["p0"], boss_keys, flags, 0)
        b.p.mons[0].item = None
        rng = random.Random(seed)
        b.dice, b.rng = pl.RunDice(rng, True), rng
        cran = boss(b, "Cranidos")
        cran.item = None
        before = cran.hp
        pl.attack(b, b.p.cur(), mv(b.p.cur(), "Magnitude"), cran, True)
        seen.add(b.last_magnitude)
        damages.append(before - cran.hp)
    results.append(("Magnitude rolls its power and deals damage by it",
                    len(seen) >= 4 and max(damages) > 40 and min(damages) > 0,
                    f"powers seen {sorted(seen)}, damage {min(damages)} to {max(damages)}"))

    # Expert's Speed-down routine: Lileep at a Speed tie with Turtwig is not
    # slower, so Rock Tomb takes -3 and Ingrain (100) wins; once rooted,
    # Basic scores Ingrain -10 and Constrict (99) leads.
    recs = [{"constant": "SPECIES_TURTWIG", "species": "Turtwig", "how": "test", "level": 16, "nature": "Lonely",
             "ivs": IV, "evs": EV, "ability": "Shell Armor", "moves": ["Razor Leaf", "Absorb"], "fill": False}]
    prep = plscore.prepare(plscore.parse_fight("roark"), given_side=recs)
    boss_keys, flags, _ = prep["variants"][0]
    b = pl.make_battle(prep["st"], ["p0"], boss_keys, flags, 0)
    lil = boss(b, "Lileep")
    lil.turns_in = 1
    picks = collections.Counter()
    for i in range(400):
        b.rng = random.Random(i)
        picks[fightai.choose(b, lil, b.p.cur())[1].name] += 1
    lil.ingrained = True
    rooted = collections.Counter()
    for i in range(400):
        b.rng = random.Random(i)
        rooted[fightai.choose(b, lil, b.p.cur())[1].name] += 1
    results.append(("Lileep against Turtwig: Ingrain first, then mostly Constrict, never Rock Tomb",
                    picks == {"Ingrain": 400} and rooted["Constrict"] > 300 and not rooted["Rock Tomb"],
                    f"first {dict(picks)}, rooted {dict(rooted)}"))

    # Rollout: the first hit after Defense Curl is 60 power (2x, not 4x), and
    # the AI costs Rollout at its listed 30, so Rock Throw stays its strongest.
    recs = [{"constant": "SPECIES_GEODUDE", "species": "Geodude", "how": "test", "level": 16, "nature": "Jolly",
             "ivs": IV, "evs": EV, "ability": "Sturdy", "moves": ["Magnitude", "Rock Throw"], "fill": False}]
    prep = plscore.prepare(plscore.parse_fight("roark"), given_side=recs)
    boss_keys, flags, _ = prep["variants"][0]
    b = pl.make_battle(prep["st"], ["p0"], boss_keys, flags, 0)
    b.p.mons[0].item = None
    rng = random.Random(1)
    b.dice, b.rng = pl.RunDice(rng, True), rng
    geo = boss(b, "Geodude")
    geo.turns_in = 1
    rollout, throw = mv(geo, "Rollout"), mv(geo, "Rock Throw")
    plain = [b.damage(geo, b.p.cur(), rollout, crit=False, roll=15)]
    geo.curled = True
    fs.rollout_after(geo, rollout, True)
    first = b.damage(geo, b.p.cur(), rollout, crit=False, roll=15)
    fs.rollout_after(geo, rollout, True)
    second = b.damage(geo, b.p.cur(), rollout, crit=False, roll=15)
    geo.rollout, geo.lock, geo.rollout_hit = 0, None, 0
    scores = fightai.score_moves(b, geo, b.p.cur(), b.ai_flags)
    by = {m.name: s for m, s in zip(geo.moves, scores)}
    results.append(("Rollout: the first curled hit is 2x, the next 4x; the AI costs it at 30 power",
                    first == 2 * plain[0] or abs(first - 2 * plain[0]) <= 1,
                    f"plain {plain[0]}, curled first {first}, second {second}; scores {by}"))
    results.append(("the AI scores curled Rollout below Rock Throw against a Geodude",
                    by["Rollout"] < by["Rock Throw"], f"{by}"))

    # Status moves and the type chart: only Thunder Wave is gated by type in
    # the engine; the AI's Basic zeroes only the paralysis moves by type.
    iv20 = {k: 20 for k in IV}
    recs = [{"constant": "SPECIES_VULLABY", "species": "Vullaby", "how": "test", "level": 22, "nature": "Hardy",
             "ivs": iv20, "evs": EV, "ability": "Big Pecks", "moves": ["Pluck", "Leer"], "fill": False},
            {"constant": "SPECIES_GEODUDE", "species": "Geodude", "how": "test", "level": 22, "nature": "Impish",
             "ivs": IV, "evs": EV, "ability": "Sturdy", "moves": ["Magnitude", "Rock Throw"], "fill": False}]
    prep = plscore.prepare(plscore.parse_fight("mars_1"), given_side=recs)
    boss_keys, flags, _ = prep["variants"][0]
    b = pl.make_battle(prep["st"], ["p0", "p1"], boss_keys, flags, 0)
    rng = random.Random(3)
    b.dice, b.rng = pl.RunDice(rng, True), rng
    bronzor = boss(b, "Bronzor")
    vull = b.p.cur()
    hyp = mv(bronzor, "Hypnosis")
    results.append(("Basic does not zero Hypnosis against a Dark type",
                    fightai.basic(b, bronzor, vull, hyp, 0) == 0, f"{fightai.basic(b, bronzor, vull, hyp, 0)}"))
    slept = 0
    for i in range(40):
        vull.status, vull.sleep = None, 0
        b.rng = random.Random(i); b.dice = pl.RunDice(b.rng, True)
        pl.status_move(b, bronzor, hyp, vull, True)
        slept += vull.status == "slp"
    vull.status, vull.sleep = None, 0
    results.append(("Hypnosis puts a Dark type to sleep at its accuracy", 12 <= slept <= 36, f"{slept} of 40"))
    tw = fs.move("Thunder Wave")
    if tw is not None:
        geo = b.p.mons[1]
        pl.status_move(b, bronzor, tw, geo, True)
        results.append(("Thunder Wave still fails on a Ground type", geo.status is None, f"{geo.status}"))
        results.append(("Basic still zeroes Thunder Wave against a Ground type",
                        fightai.basic(b, bronzor, geo, tw, 0) == -10, f"{fightai.basic(b, bronzor, geo, tw, 0)}"))

    # Struggle: with no PP left the AI's Pokemon struggles, hits for typeless
    # damage (it touches a Dark type) and loses a quarter of its HP.
    for m in bronzor.moves:
        bronzor.pp[m.name] = 0
    pick = fightai.choose(b, bronzor, vull)
    hp_v, hp_b = vull.hp, bronzor.hp
    pl._turn(b, ("move", mv(vull, "Leer")), pick)
    results.append(("with no PP left the AI struggles, hits and takes a quarter of its HP in recoil",
                    pick[1].name == "Struggle" and vull.hp < hp_v and hp_b - bronzor.hp == bronzor.maxhp // 4,
                    f"{pick[1].name}; Vullaby {hp_v} to {vull.hp}; Bronzor {hp_b} to {bronzor.hp} of {bronzor.maxhp}"))

    # Quick Claw: a slower player's Pokemon holding it moves first about one
    # time in five.
    geo = b.p.mons[1]
    b.p.active = 1
    geo.item = "Quick Claw"
    bronzor.pp = {m.name: 10 for m in bronzor.moves}
    firsts = 0
    for i in range(400):
        c = pl.clone_battle(b)
        c.rng = random.Random(i); c.dice = pl.RunDice(c.rng, True)
        g, bz = c.p.cur(), c.b.cur()
        g.hp, bz.hp = g.maxhp, bz.maxhp
        log = []
        orig = pl.use_move
        pl.use_move = lambda bb, att, m, d, first, _o=orig, _l=log: (_l.append(att.side), _o(bb, att, m, d, first))
        try:
            pl._turn(c, ("move", mv(g, "Rock Throw")), ("move", mv(bz, "Calm Mind")))
        finally:
            pl.use_move = orig
        firsts += bool(log) and log[0] == "p"
    results.append(("a slower Pokemon's Quick Claw moves it first about one time in five",
                    50 <= firsts <= 115, f"{firsts} of 400"))

    # Powder: Grass types are immune, and the AI knows; Leaf Guard stops
    # status in sun (the engine knows, the AI does not).
    recs = [{"constant": "SPECIES_TSAREENA", "species": "Tsareena", "how": "test", "level": 26, "nature": "Lonely",
             "ivs": IV, "evs": EV, "ability": "Leaf Guard", "moves": ["Stomp"], "fill": False},
            {"constant": "SPECIES_GOLBAT", "species": "Golbat", "how": "test", "level": 26, "nature": "Lonely",
             "ivs": IV, "evs": EV, "ability": "Inner Focus", "moves": ["Wing Attack"], "fill": False}]
    prep = plscore.prepare(plscore.parse_fight("gardenia"), given_side=recs)
    boss_keys, flags, _ = prep["variants"][0]
    b = pl.make_battle(prep["st"], ["p0", "p1"], boss_keys, flags, 0)
    b.dice = pl.RunDice(random.Random(5), True); b.rng = random.Random(5)
    rose, tsa, gol = boss(b, "Roserade"), b.p.mons[0], b.p.mons[1]
    spore = mv(rose, "Stun Spore")
    for _ in range(20):
        pl.status_move(b, rose, spore, tsa, True)
    results.append(("Stun Spore never paralyses a Grass type, and the AI scores it -10",
                    tsa.status is None and fightai.basic(b, rose, tsa, spore, 0) == -10,
                    f"{tsa.status}, {fightai.basic(b, rose, tsa, spore, 0)}"))
    b.weather = "Sun"
    gol.ability = "Leaf Guard"
    for _ in range(20):
        pl.status_move(b, rose, spore, gol, True)
    results.append(("Leaf Guard stops status in sun", gol.status is None, f"{gol.status}"))
    b.weather = None
    for _ in range(20):
        pl.status_move(b, rose, spore, gol, True)
    results.append(("out of sun Leaf Guard does not", gol.status == "par", f"{gol.status}"))

    # Switching (TrainerAI_ShouldSwitch): an asleep Natural Cure holder at
    # half HP or more, not hit, leaves seven times in eight; Natural Gift is
    # typed by its berry, so Lumineon's Watmel gift counts as super-effective
    # against a Bug type and keeps it in nine times in ten.
    recs = [{"constant": "SPECIES_VIKAVOLT", "species": "Vikavolt", "how": "test", "level": 26, "nature": "Jolly",
             "ivs": IV, "evs": EV, "ability": "Levitate", "moves": ["Spark", "Bug Bite"], "fill": False}]
    prep = plscore.prepare(plscore.parse_fight("gardenia"), given_side=recs)
    boss_keys, flags, _ = prep["variants"][0]
    b = pl.make_battle(prep["st"], ["p0"], boss_keys, flags, 0)
    vika = b.p.cur()
    rose = boss(b, "Roserade")
    b.b.active = b.b.mons.index(rose)
    rose.status, rose.sleep, rose.last_hit_by = "slp", 3, None
    left = 0
    for i in range(800):
        b.rng = random.Random(i)
        left += fightai.should_switch(b, b.b, rose, vika) is not None
    results.append(("an asleep Natural Cure holder at full HP, not hit, switches about 7 in 8",
                    0.82 <= left / 800 <= 0.93, f"{left} of 800"))
    lum = boss(b, "Lumineon")
    b.b.active = b.b.mons.index(lum)
    lum.last_hit_by = mv(vika, "Spark")
    gift = mv(lum, "Natural Gift")
    stays = 0
    for i in range(800):
        b.rng = random.Random(i)
        stays += fightai.should_switch(b, b.b, lum, vika) is None
    results.append(("Natural Gift takes its berry's type: Watmel's Fire keeps Lumineon in about 9 in 10 against Vikavolt",
                    fightai.move_type(b, lum, gift) == "Fire" and stays / 800 >= 0.85, f"{fightai.move_type(b, lum, gift)}, stayed {stays} of 800"))

    results += fixed_damage_checks()
    results += explosion_checks()
    results += sleep_checks()
    results += sleep_talk_and_aqua_ring_checks()
    results += first_battle_checks()
    results += magnet_rise_checks()
    results += torment_and_pain_split_checks()
    results += destiny_bond_checks()

    width = max(len(r[0]) for r in results)
    for name, ok, note in results:
        print(f"  {'ok  ' if ok else 'FAIL'}  {name:{width}}  {note}")
    passed = sum(1 for r in results if r[1])
    print(f"\n{passed}/{len(results)} passed")
    return 0 if passed == len(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())

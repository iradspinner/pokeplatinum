"""The mechanics the Roark fight showed missing from the perfect-line
simulator, each checked on that fight (the Overseer, 2026-09-30).

    PYTHONPATH=. python3 -m tools.oxide.balance.test_plfixes
"""
import collections
import os
import random

from . import fightai, plscore, perfectline as pl, fightsim as fs

IV = {k: 15 for k in ("hp", "at", "df", "sp", "sa", "sd")}
EV = {k: 0 for k in IV}
TEAM = [("SPECIES_BARBOACH", "Barboach", "Lonely", "Swift Swim", ["Mud Bomb", "Water Gun", "Mud-Slap"]),
        ("SPECIES_NACLI", "Nacli", "Impish", "Sturdy", ["Mud Shot", "Rock Throw", "Harden", "Headbutt"]),
        ("SPECIES_GRUBBIN", "Grubbin", "Relaxed", "Swarm", ["Bug Bite", "Bite", "Mud-Slap"])]


def battle(seed=1, team=TEAM):
    recs = [{"constant": c, "species": s, "how": "test", "level": 16, "nature": n, "ivs": IV, "evs": EV,
             "ability": a, "moves": mv, "fill": False} for c, s, n, a, mv in team]
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


def gender_checks():
    """Genders, Attract and the contact abilities (Ian, 2026-10-03): a
    trainer's Pokemon get the gender their file gives (Jupiter 1's Delcatty
    is female); Attract works only across genders, not on Oblivious; love
    stops about half the moves and ends when its object leaves; Cute Charm
    and Static take about 3 contact hits in 10, Rough Skin an eighth."""
    prep = plscore.prepare(plscore.parse_fight("jupiter_1"), given_side=[])
    st = prep["st"]
    delcatty = next(k for k in prep["variants"][0][0] if st["pokemon"][k]["species"] == "Delcatty")
    file_gender = st["pokemon"][delcatty]["gender"]
    b = battle()
    foe, barboach = b.b.cur(), b.p.cur()
    attract = fs.move("Attract")
    foe.gender, barboach.gender = "F", "F"
    pl.status_move(b, foe, attract, barboach, True)
    same = barboach.infatuated
    barboach.gender = None
    pl.status_move(b, foe, attract, barboach, True)
    genderless = barboach.infatuated
    barboach.gender, barboach.ability = "M", "Oblivious"
    pl.status_move(b, foe, attract, barboach, True)
    oblivious = barboach.infatuated
    barboach.ability = "Swift Swim"
    pl.status_move(b, foe, attract, barboach, True)
    took = barboach.infatuated == foe.key
    stopped = 0
    for i in range(400):
        b.dice = pl.RunDice(random.Random(i), True)
        barboach.last = None
        before = foe.hp = foe.maxhp
        pl.use_move(b, barboach, mv(barboach, "Water Gun"), foe, True)
        stopped += foe.hp == before
    fs.switch_in(b, b.b, 1)
    ended = barboach.infatuated
    # Cute Charm and Static on contact, Rough Skin's eighth.
    b = battle()
    foe, grubbin = b.b.cur(), b.p.mons[2]
    fs.switch_in(b, b.p, 2)
    foe.gender, grubbin.gender = "F", "M"
    counts = {}
    for ability in ("Cute Charm", "Static"):
        foe.ability, n = ability, 0
        for i in range(400):
            b.dice = pl.RunDice(random.Random(i), True)
            grubbin.infatuated, grubbin.status, foe.hp = None, None, foe.maxhp
            pl.use_move(b, grubbin, mv(grubbin, "Bite"), foe, True)
            n += bool(grubbin.infatuated) if ability == "Cute Charm" else grubbin.status == "par"
        counts[ability] = n
    foe.ability, grubbin.hp, foe.hp = "Rough Skin", grubbin.maxhp, foe.maxhp
    pl.use_move(b, grubbin, mv(grubbin, "Bite"), foe, True)
    rough = grubbin.maxhp - grubbin.hp
    return [("a trainer's Pokemon has the gender its file gives (Jupiter 1's Delcatty is female)",
             file_gender == "F", f"Delcatty {file_gender}"),
            ("Attract: not between equal genders, not on a genderless or Oblivious target, yes across",
             not same and not genderless and not oblivious and took,
             f"same {same}, genderless {genderless}, Oblivious {oblivious}, across {took}"),
            ("love stops about half the moves, and ends when its object switches out",
             150 <= stopped <= 250 and ended is None, f"{stopped} of 400 stopped, after the switch {ended}"),
            ("Cute Charm and Static take about 3 contact hits in 10; Rough Skin takes an eighth",
             all(80 <= c <= 160 for c in counts.values()) and rough == max(1, grubbin.maxhp // 8),
             f"{counts}, Rough Skin {rough} of {grubbin.maxhp}")]


def wish_spite_recycle_checks():
    """Wish, Spite and Recycle (2026-10-03): Wish heals its side's Pokemon by
    half its maximum HP at the second turn's end; Spite takes 4 PP from the
    target's last move; Recycle brings back the item its user used up."""
    b = battle()
    foe, barboach = b.b.cur(), b.p.cur()
    foe.hp = 10
    pl.status_move(b, foe, fs.move("Wish"), barboach, True)
    fs.end_of_turn(b)
    after_one = foe.hp
    fs.end_of_turn(b)
    after_two = foe.hp
    barboach.last, barboach.pp["Mud Bomb"] = mv(barboach, "Mud Bomb"), 10
    b.dice = pl.RunDice(random.Random(1), True)
    pl.status_move(b, foe, fs.move("Spite"), barboach, True)
    spited = barboach.pp["Mud Bomb"]
    foe.item = "Sitrus Berry"
    foe.hp = foe.maxhp // 2 - 1
    fs.berry_check(foe)
    eaten = foe.item
    pl.status_move(b, foe, fs.move("Recycle"), barboach, True)
    back = foe.item
    return [("Wish heals half the maximum HP at the second turn's end",
             after_one == 10 and after_two == min(foe.maxhp, 10 + foe.maxhp // 2),
             f"10 then {after_one} then {after_two} of {foe.maxhp}"),
            ("Spite takes 4 PP; Recycle brings back a used-up berry",
             spited == 6 and eaten is None and back == "Sitrus Berry", f"PP {spited}, berry {eaten} then {back}")]


def held_state_checks():
    """The held items, abilities and move effects the calculator's rows
    cannot know (2026-10-03), each as the decomp has it."""
    out = []
    b = battle()
    foe, barboach = b.b.cur(), b.p.cur()
    gun = fs.move("Water Gun")

    def dmg(att, dfn, mv):
        return pl.damage_of(b, att, dfn, mv, False, True)

    # A pinch ability at a third of its HP; a resist berry's halving, then gone.
    barboach.ability = "Torrent"
    full = dmg(barboach, foe, gun)
    barboach.hp = barboach.maxhp // 3
    pinch = dmg(barboach, foe, gun)
    barboach.hp = barboach.maxhp
    holder = next((m for m in b.b.mons if fs._row_item(b, m) == "Passho Berry"), None)
    berry = None
    if holder is not None:
        fs.switch_in(b, b.b, b.b.mons.index(holder))
        first = dmg(barboach, holder, gun)
        fs.after_hit(b, barboach, holder, gun, first)
        second = dmg(barboach, holder, gun)
        berry = (holder.item, round(second / max(1, first), 2))
    out.append(("a pinch ability's 1.5 at a third of HP; a resist berry halves one hit and is eaten",
                1.4 <= pinch / full <= 1.6 and berry is not None and berry[0] is None and 1.8 <= berry[1] <= 2.2,
                f"Torrent {full} then {pinch}; Passho Berry {berry}"))
    # Status berries, Berry Juice, White Herb, a Toxic Orb, Shell Bell.
    b = battle()
    foe, barboach = b.b.cur(), b.p.cur()
    barboach.item = "Pecha Berry"
    b.status_src = None
    pl.give_status(b, barboach, "psn")
    pecha = (barboach.status, barboach.item)
    barboach.item, barboach.hp = "Berry Juice", barboach.maxhp // 2
    fs.berry_check(barboach)
    juice = barboach.hp - barboach.maxhp // 2
    barboach.item = "White Herb"
    fs.change_stages(barboach, {"def": -1})
    herb = (barboach.stages["def"], barboach.item)
    barboach.item, barboach.status = "Toxic Orb", None
    fs.end_of_turn(b)
    orb = barboach.status
    barboach.item, barboach.hp = "Shell Bell", barboach.maxhp // 2
    fs.after_hit(b, barboach, foe, gun, 40)
    bell = barboach.hp - barboach.maxhp // 2
    out.append(("Pecha cures at once, Berry Juice heals 20, White Herb undoes a drop, Toxic Orb, Shell Bell",
                pecha == (None, None) and juice == 20 and herb == (0, None) and orb == "tox" and bell == 5,
                f"Pecha {pecha}, Juice +{juice}, Herb {herb}, Orb {orb}, Bell +{bell}"))
    # Aftermath, Unburden, Truant, Natural Cure, Regenerator, Speed Boost, Poison Heal.
    b = battle()
    foe, barboach = b.b.cur(), b.p.cur()
    grubbin = b.p.mons[2]
    fs.switch_in(b, b.p, 2)
    foe.ability, foe.hp = "Aftermath", 1
    b.dice = pl.RunDice(random.Random(2), True)
    pl.use_move(b, grubbin, mv(grubbin, "Bite"), foe, True)
    after = grubbin.maxhp - grubbin.hp if not foe.alive() else None
    foe2 = b.b.mons[1]
    foe2.ability, foe2.item, foe2.had_item = "Unburden", "Sitrus Berry", True
    s1 = b.speed(foe2)
    fs.consume(foe2)
    s2 = b.speed(foe2)
    grubbin.ability, grubbin.loafing = "Truant", False
    acted = []
    for _ in range(3):
        before = foe2.hp = foe2.maxhp
        pl.use_move(b, grubbin, mv(grubbin, "Bite"), foe2, True)
        acted.append(foe2.hp < before)
    fs.switch_in(b, b.p, 0)
    barboach.ability, barboach.status = "Natural Cure", "par"
    nacli = b.p.mons[1]
    nacli.ability, nacli.hp = "Regenerator", nacli.maxhp // 3
    fs.switch_in(b, b.p, 1)         # Barboach leaves: Natural Cure
    fs.switch_in(b, b.p, 0)         # Nacli leaves: Regenerator
    cured, regen = barboach.status, nacli.hp
    barboach.ability, barboach.turns_in, barboach.stages["spe"] = "Speed Boost", 1, 0
    barboach.ability, barboach.status = "Poison Heal", "psn"
    barboach.hp = barboach.maxhp // 2
    fs.end_of_turn(b)
    healed = barboach.hp - barboach.maxhp // 2
    barboach.ability, barboach.status, barboach.turns_in = "Speed Boost", None, 1
    fs.end_of_turn(b)
    boosted = barboach.stages["spe"]
    out.append(("Aftermath, Unburden, Truant, Natural Cure, Regenerator, Poison Heal, Speed Boost",
                after == grubbin.maxhp // 4 and s2 == 2 * s1 and acted == [True, False, True]
                and cured is None and regen == nacli.maxhp // 3 + nacli.maxhp // 3 and healed == barboach.maxhp // 8
                and boosted == 1,
                f"Aftermath {after}, speed {s1} then {s2}, Truant {acted}, cured {cured}, Regenerator {regen}, "
                f"Poison Heal +{healed}, Speed Boost {boosted}"))
    # Inner Focus, Synchronize, Magnet Pull, Unaware, Super Luck's stage.
    b = battle()
    foe, barboach = b.b.cur(), b.p.cur()
    barboach.ability = "Inner Focus"
    b.dice = pl.RunDice(random.Random(3), True)
    foe.moves, foe.pp = [fs.move("Fake Out")], {"Fake Out": 10}
    pl.use_move(b, foe, foe.moves[0], barboach, True)
    focus = barboach.flinch
    barboach.ability, barboach.status, foe.status = "Synchronize", None, None
    b.status_src = foe
    pl.give_status(b, barboach, "par")
    synced = foe.status
    foe.ability = "Magnet Pull"
    barboach.types = ["Steel"]
    from . import plplan
    trapped = not any(a[0] == "switch" for a in plplan.options(b))
    barboach.types = ["Water", "Ground"]
    foe.ability = "Unaware"
    plain_hit = dmg(barboach, foe, gun)
    barboach.stages["spa"] = 2
    unaware_hit = dmg(barboach, foe, gun)
    barboach.stages["spa"] = 0
    out.append(("Inner Focus, Synchronize, Magnet Pull, Unaware",
                not focus and synced == "par" and trapped and unaware_hit == plain_hit,
                f"flinched {focus}, synced {synced}, trapped {trapped}, Unaware {plain_hit} then {unaware_hit}"))
    # Flail and Water Spout by HP, Rage, Last Resort, Hurricane in rain, Custap. Dig is a one-turn hit
    # since the move reworks (2026-10-06), so nothing goes underground: its old check, Earthquake
    # reaching a digger, is now that Dig never charges (Gust into Fly keeps the reach rules' check).
    m = fs.Mon.__new__(fs.Mon)
    m.hp, m.maxhp = 1, 64
    low = fs.flail_power(m)
    m.hp = 64
    high = fs.flail_power(m)
    b = battle()
    foe, barboach = b.b.cur(), b.p.cur()
    foe.raging = True
    fs.after_hit(b, barboach, foe, gun, 10)
    rage = foe.stages["atk"]
    barboach.moves = [fs.move("Last Resort"), fs.move("Water Gun")]
    barboach.pp = {"Last Resort": 5, "Water Gun": 10}
    early = fs.commit_move(barboach, barboach.moves[0])
    fs.commit_move(barboach, barboach.moves[1])
    later = fs.commit_move(barboach, barboach.moves[0])
    b.weather = "Rain"
    rain = all(pl.accuracy_hits(b, barboach, foe, fs.move("Hurricane")) for _ in range(20))
    b.weather = None
    dig = fs.move("Dig")
    one_turn = dig.effect not in fs.TWO_TURN and dig.effect not in fs.INVULNERABLE
    foe.item, foe.hp = "Custap Berry", foe.maxhp // 4
    custap = fs.custap_fires(foe)
    out.append(("Flail by HP, Rage, Last Resort, Hurricane in rain, Dig in one turn, Custap at a quarter",
                low == 200 and high == 20 and rage == 1 and early and not later and rain and one_turn and custap,
                f"Flail {low}/{high}, Rage +{rage}, Last Resort fails {early} then {later}, rain {rain}, "
                f"Dig's effect {dig.effect}, Custap {custap}"))
    return out


def blind_pool_checks():
    """The blind draw's pool (Ian, 2026-10-04): the stronger half of the
    members at the cap, by their margins against the split's trainers, six
    at least; a member held below the cap never in it. Read on the hand
    run's box at 19, which keeps a level-6 Starly, in Gardenia's split."""
    from . import plstep3, plteam, plteam_test
    recs = plteam_test.box(plstep3.ROARK, 19)
    st = fs.prepare("Gardenia", [], None, cap=19, given_side=recs)
    keys = [f"p{i}" for i in range(len(recs))]
    pool_ = plteam.blind_pool(st, keys, "Gardenia", 19)
    ready = [k for k in keys if st["pokemon"][k]["level"] >= 19]
    power = plteam.split_strength(st, ready, "Gardenia", 19)
    dropped = [k for k in ready if k not in pool_]
    below = [st["pokemon"][k]["species"] for k in keys if k not in ready]
    ok = (len(pool_) == max(6, (len(ready) + 1) // 2) and not set(pool_) - set(ready)
          and min(power[k] for k in pool_) >= max(power[k] for k in dropped) and below)
    # 75 fights from eight members, which make only 28 different sixes.
    from . import plstudy
    drawn = plstudy.draw(random.Random(1), pool_, 75)
    ok = ok and len(drawn) == 75 and all(len(s) == 6 and set(s) <= set(pool_) for s in drawn)
    return [("the blind pool is the stronger half at the cap, never one held below it; 75 draws from it",
             ok, f"keeps {len(pool_)} of {len(keys)}; below the cap and out: {', '.join(below)}; "
                 f"{len(set(drawn))} different sixes in 75 draws")]


def map_weather_checks():
    """The study and blind readings start in the trainers' map weather, as
    a story fight does: Roark's file and Youngster Darius's (Oreburgh's gym,
    permanent sand) in sand, Youngster Tristan's (Route 203) in none. The
    comb read all three with no weather until 2026-10-06."""
    from . import plstep3, plstudy, plteam_test
    recs = plstudy.fixed(plteam_test.box(plstep3.ROARK, 16))
    got = {}
    for stem in ("leader_roark", "youngster_darius", "youngster_tristan"):
        st, _k, _f = plstudy.prepare([os.path.join(plstudy.RES, stem + ".json")], "Roark", 16, recs,
                                     plstudy.stock({}))
        got[stem] = st.get("base_weather")
    story = plscore.prepare(plscore.parse_fight("roark"))["st"].get("base_weather")
    ok = got == {"leader_roark": "Sand", "youngster_darius": "Sand", "youngster_tristan": None} and story == "Sand"
    return [("study and blind readings start in the map's weather, as the story fight does", ok,
             f"{got}; the story fight's Roark {story}")]


def rework_checks():
    """The move reworks (Ian, 2026-10-06; the engine on cloud/main-move-reworks),
    each on the planner's own attack in a one-against-one battle whose rows
    are set (test_fightsim.battle), so every number is exact. The target has
    Battle Armor so that no crit muddies a damage figure."""
    from . import plplan
    from .test_fightsim import battle as duel
    out = []

    def fresh(pm, bm=("Tackle",), roll=30, seed=1, hp=100, b_types=("Normal",)):
        rolls = {("p", m): [roll] * 16 for m in pm}
        rolls.update({("b", m): [roll] * 16 for m in bm})
        b, p, foe = duel(list(pm), list(bm), rolls, hp=hp, seed=seed, b_types=b_types)
        b.dice = pl.RunDice(random.Random(seed), True)
        b.rng = b.dice.rng
        foe.ability = "Battle Armor"
        return b, p, foe

    def use(name, seed=1, **kw):
        b, p, foe = fresh([name], seed=seed, **kw)
        pl.use_move(b, p, fs.move(name), foe, True)
        return b, p, foe

    # Hyper Beam, Giga Impact, Rock Wrecker, Roar of Time: half the damage
    # as recoil, no recharge; Rock Head takes no recoil.
    beams = []
    for name in ("Hyper Beam", "Giga Impact", "Rock Wrecker", "Roar of Time"):
        b, p, foe = use(name, roll=40)
        beams.append((name, 100 - foe.hp, 100 - p.hp, p.recharge))
    b, p, foe = fresh(["Hyper Beam"], roll=40)
    p.ability = "Rock Head"
    pl.use_move(b, p, fs.move("Hyper Beam"), foe, True)
    out.append(("Hyper Beam and its kin: half recoil, no recharge; none with Rock Head",
                all(x[1:] == (40, 20, False) for x in beams) and p.hp == 100,
                f"{beams}; Rock Head HP {p.hp}"))

    # The starter ultimates and the one-turn moves: accuracy, recoil and
    # status over 600 uses each.
    def tally(name, n=600, roll=30):
        hit = recoil_ok = status = confused = locked = charging = 0
        frac = fs.RECOIL.get(fs.move(name).effect, 0)
        for s in range(n):
            b, p, foe = use(name, seed=s, roll=roll)
            dealt = 100 - foe.hp
            if dealt:
                hit += 1
                recoil_ok += (100 - p.hp) == (max(1, int(dealt * frac)) if frac else 0)
                status += foe.status is not None
                confused += bool(foe.confused)
            locked += p.lock is not None
            charging += p.charging is not None
        return {"hit": hit / n, "recoil": recoil_ok == hit, "status": status / max(1, hit),
                "confused": confused / max(1, hit), "locked": locked, "charging": charging}
    want = {"Blast Burn": (0.95, "status", 0.30), "Frenzy Plant": (0.95, "status", 0.20),
            "Hydro Cannon": (0.95, "status", 0.0), "Sky Attack": (1.0, "status", 0.20),
            "Dig": (1.0, "status", 0.0), "Dive": (1.0, "status", 0.0),
            "Thrash": (1.0, "status", 0.20), "Outrage": (1.0, "status", 0.0),
            "Petal Dance": (1.0, "confused", 0.20), "Uproar": (1.0, "confused", 0.20),
            "Raging Fury": (1.0, "confused", 0.20)}
    got = {name: tally(name) for name in want}
    bad = [name for name, (acc, kind, rate) in want.items()
           if abs(got[name]["hit"] - acc) > 0.04 or not got[name]["recoil"]
           or abs(got[name][kind] - rate) > 0.06 or got[name]["locked"] or got[name]["charging"]]
    out.append(("starter ultimates, Sky Attack, Dig, Dive and the rampage moves in one turn, at their odds",
                not bad, "; ".join(f"{n} hit {g['hit']:.2f} {want[n][1]} {g[want[n][1]]:.2f}"
                                   + ("" if g["recoil"] else " recoil wrong") for n, g in got.items())
                + (f"; off: {bad}" if bad else "")))

    # Two to five hits on 35/35/15/15: a row of three hits at 10 each.
    def spread(item=None, ability=None, n=4000):
        counts = collections.Counter()
        for s in range(n):
            b, p, foe = fresh(["Bullet Seed"], seed=s, roll=30, hp=200)
            p.item, p.ability = item, ability or p.ability
            if ability == "Skill Link":
                b.st["rows"][(None, "p0", "b0.0")]["moves"]["Bullet Seed"]["rolls"] = [50] * 16
            pl.attack(b, p, fs.move("Bullet Seed"), foe, True)
            counts[(200 - foe.hp) // 10] += 1
        return {h: round(c / n, 3) for h, c in sorted(counts.items())}
    plain, link, dice = spread(), spread(ability="Skill Link"), spread(item="Loaded Dice")
    ok = (all(abs(plain.get(h, 0) - w / 100) < 0.025 for h, w in fs.MULTI_HIT_ODDS) and link == {5: 1.0}
          and set(dice) == {4, 5} and abs(dice[4] - 0.5) < 0.03)
    # The planner's dice enumerate the count at its odds.
    b, p, foe = fresh(["Bullet Seed"])
    b.dice = plplan.EnumDice((), random.Random(0))
    pl.rolled_hits(b, p, foe, fs.move("Bullet Seed"), False)
    enum = b.dice.events[0] if b.dice.events else None
    out.append(("two to five hit moves roll 35/35/15/15; Skill Link 5, Loaded Dice 4 or 5; the planner enumerates",
                ok and enum == (0.35, 0.35, 0.15, 0.15),
                f"hits {plain}; Skill Link {link}; Loaded Dice {dice}; enumerated {enum}"))

    # A Focus Sash holds one hit, not a two to five hit move's total.
    b, p, foe = fresh(["Bullet Seed"], roll=150)
    foe.item = "Focus Sash"
    pl.attack(b, p, fs.move("Bullet Seed"), foe, True)
    b2, p2, foe2 = fresh(["Tackle"], roll=150)
    foe2.item = "Focus Sash"
    pl.attack(b2, p2, fs.move("Tackle"), foe2, True)
    out.append(("a Focus Sash holds a single hit but not a multi-hit move", foe.hp == 0 and foe2.hp == 1,
                f"Bullet Seed leaves {foe.hp}, Tackle {foe2.hp}"))

    # Fury Cutter: three hits at 30, 40 and 50 on a row of one hit at 30.
    b, p, foe = fresh(["Fury Cutter"], roll=30, hp=200)
    pl.attack(b, p, fs.move("Fury Cutter"), foe, True)
    cutter = 200 - foe.hp
    expected = fs.expected_hit_scale(fs.move("Fury Cutter"))
    out.append(("Fury Cutter hits three times rising by 10; Spite has 5 PP",
                cutter == 120 and abs(expected - 4.0) < 1e-9 and fs.move("Spite").pp == 5,
                f"dealt {cutter} on a 30 row; expected scale {expected:.2f}; Spite {fs.move('Spite').pp} PP"))

    # Upper Hand: only against a chosen priority move, before it acts; it flinches.
    def upper(chosen, first=True, ability=None):
        b, p, foe = fresh(["Upper Hand"], roll=20)
        foe.chosen = fs.move(chosen) if chosen else None
        foe.ability = ability or foe.ability
        pl.attack(b, p, fs.move("Upper Hand"), foe, first)
        return 100 - foe.hp, foe.flinch
    ups = {"Quick Attack": upper("Quick Attack"), "Tackle": upper("Tackle"),
           "Quick Attack, second": upper("Quick Attack", first=False),
           "Prankster Thunder Wave": upper("Thunder Wave", ability="Prankster"),
           "Thunder Wave": upper("Thunder Wave")}
    out.append(("Upper Hand lands only on a chosen priority move, and flinches",
                ups == {"Quick Attack": (20, True), "Tackle": (0, False), "Quick Attack, second": (0, False),
                        "Prankster Thunder Wave": (20, True), "Thunder Wave": (0, False)}, str(ups)))

    # Shell Trap: only after a physical hit on its user this turn.
    traps = {}
    for label, hit in (("none", None), ("physical", ("Physical", 10)), ("special", ("Special", 10))):
        b, p, foe = fresh(["Shell Trap"], roll=25)
        p.hit_this_turn = hit
        pl.attack(b, p, fs.move("Shell Trap"), foe, True)
        traps[label] = 100 - foe.hp
    out.append(("Shell Trap strikes only after a physical hit on its user", traps == {"none": 0, "physical": 25,
                                                                                     "special": 0}, str(traps)))

    # Burning Jealousy: a burn only on a target whose stats rose this turn,
    # none through Sheer Force; the flag clears at the turn's end.
    def jealous(raised, ability=None):
        b, p, foe = fresh(["Burning Jealousy"], roll=10)
        p.ability = ability or p.ability
        if raised:
            fs.change_stages(foe, {"atk": 1})
        pl.attack(b, p, fs.move("Burning Jealousy"), foe, True)
        return foe.status
    b, p, foe = fresh(["Tackle"])
    fs.change_stages(foe, {"spe": 1})
    raised = foe.stat_raised
    fs.end_of_turn(b)
    out.append(("Burning Jealousy burns only a target whose stats rose this turn",
                (jealous(False), jealous(True), jealous(True, "Sheer Force"), raised, foe.stat_raised)
                == (None, "brn", None, True, False),
                f"plain {jealous(False)}, raised {jealous(True)}, Sheer Force {jealous(True, 'Sheer Force')}; "
                f"flag {raised} then {foe.stat_raised}"))

    # Sheer Force strips the new effects' secondaries and keeps the recoil.
    sf = {}
    for name, kind in (("Raging Fury", "confused"), ("Thrash", "status")):
        landed = recoil = 0
        for s in range(300):
            b, p, foe = fresh([name], seed=s, roll=30)
            p.ability = "Sheer Force"
            pl.attack(b, p, fs.move(name), foe, True)
            landed += bool(foe.confused) if kind == "confused" else foe.status is not None
            recoil += p.hp == 90
        sf[name] = (landed, recoil)
    b, p, foe = fresh(["Upper Hand"], roll=20)
    p.ability, foe.chosen = "Sheer Force", fs.move("Quick Attack")
    pl.attack(b, p, fs.move("Upper Hand"), foe, True)
    out.append(("Sheer Force strips Raging Fury's, Thrash's and Upper Hand's secondaries, keeping the recoil",
                sf == {"Raging Fury": (0, 300), "Thrash": (0, 300)} and not foe.flinch
                and {"RECOIL_CONFUSE_HIT", "UPPER_HAND", "BURN_HIT_IF_STATS_ROSE"} <= fs.sheer_force_effects(),
                f"{sf}; Upper Hand flinch {foe.flinch}"))

    # Reckless: the game raises every effect it lists by 1.2; on a row the
    # simulator adds it only where the calculator does not (Hyper Beam, until
    # the calculator reads the game's list), never where it does (Brave Bird),
    # and never without Reckless.
    reck = {}
    for name, ability in (("Hyper Beam", "Reckless"), ("Brave Bird", "Reckless"), ("Hyper Beam", "Intimidate")):
        b, p, foe = fresh([name], roll=40, hp=200)
        p.ability = ability
        pl.attack(b, p, fs.move(name), foe, True)
        reck[f"{name} {ability}"] = 200 - foe.hp
    beam = 40 if "Hyper Beam" in fs.calc_reckless() else 48
    want_effects = {"RECOIL_HALF", "RECOIL_BURN_HIT", "RECOIL_PARALYZE_HIT", "RECOIL_CONFUSE_HIT", "RECOIL_THIRD",
                    "RECOIL_QUARTER", "CRASH_ON_MISS"}
    out.append(("Reckless: the simulator adds 1.2 where the calculator's row lacks it, and only there",
                reck == {"Hyper Beam Reckless": beam, "Brave Bird Reckless": 40, "Hyper Beam Intimidate": 40}
                and want_effects <= fs.reckless_effects(),
                f"{reck}; the calculator boosts {len(fs.calc_reckless())} moves itself; "
                f"effects {sorted(fs.reckless_effects())}"))

    # Priority as the engine reckons it: Prankster on a status move, Gale
    # Wings on a Flying move at full HP.
    b, p, foe = fresh(["Tackle"])
    p.ability = "Prankster"
    prank = fs.move_priority(p, fs.move("Thunder Wave"))
    p.ability = "Gale Wings"
    gale = fs.move_priority(p, fs.move("Brave Bird"))
    p.hp -= 1
    gale_hurt = fs.move_priority(p, fs.move("Brave Bird"))
    out.append(("Prankster and Gale Wings raise priority as Battler_MovePriority does",
                (prank, gale, gale_hurt) == (1, 1, 0), f"Prankster Thunder Wave {prank}, Gale Wings {gale}, "
                                                       f"hurt {gale_hurt}"))
    return out


def sheer_force_life_orb_checks():
    """Ian, 2026-10-07: a Sheer Force user holding a Life Orb takes no Life
    Orb recoil on a move Sheer Force boosts (Battler_SheerForceActive: an
    effect it strips, or a move that keeps its effect under it), and keeps
    both boosts. On the planner's attack with set rows, then on the
    calculator: one level 100 Nidoking's Flamethrower into a Snorlax with
    Sheer Force and a Life Orb, each alone, and neither (1.3, 1.3 and 1.69,
    within rounding)."""
    from . import pressure, teamscore
    from .test_fightsim import battle as duel
    out = []

    def lost(name, ability, item="Life Orb"):
        b, p, foe = duel([name], ["Tackle"], {("p", name): [20] * 16}, hp=100)
        b.dice = pl.RunDice(random.Random(1), True)
        b.rng = b.dice.rng
        foe.ability = "Battle Armor"
        p.ability, p.item = ability, item
        pl.attack(b, p, fs.move(name), foe, True)
        return 100 - p.hp
    got = {"Flamethrower, Sheer Force": lost("Flamethrower", "Sheer Force"),
           "Ceaseless Edge, Sheer Force": lost("Ceaseless Edge", "Sheer Force"),
           "Spirit Shackle, Sheer Force": lost("Spirit Shackle", "Sheer Force"),
           "Tackle, Sheer Force": lost("Tackle", "Sheer Force"),
           "Flamethrower, Blaze": lost("Flamethrower", "Blaze")}
    sf = types_ns(ability="Sheer Force")
    strips = {n: fs.sheer_force_strips(sf, fs.move(n)) for n in ("Flamethrower", "Spirit Shackle", "Ceaseless Edge")}
    out.append(("Sheer Force with a Life Orb: no recoil on a move it boosts, recoil on one it does not",
                got == {"Flamethrower, Sheer Force": 0, "Ceaseless Edge, Sheer Force": 0,
                        "Spirit Shackle, Sheer Force": 0, "Tackle, Sheer Force": 10, "Flamethrower, Blaze": 10}
                and strips == {"Flamethrower": True, "Spirit Shackle": False, "Ceaseless Edge": False},
                f"HP lost {got}; strips {strips}"))

    ivs = {k: 31 for k in ("hp", "at", "df", "sp", "sa", "sd")}
    mon = {"species": "Nidoking", "level": 100, "nature": "Modest", "ivs": ivs, "evs": dict.fromkeys(ivs, 0)}
    pk = {"both": dict(mon, ability="Sheer Force", item="Life Orb"), "sf": dict(mon, ability="Sheer Force", item=""),
          "lo": dict(mon, ability="Poison Point", item="Life Orb"), "none": dict(mon, ability="Poison Point", item=""),
          # Immunity, not Thick Fat, so the Fire hit is large enough that rounding stays under 1%.
          "t": dict(mon, species="Snorlax", level=50, nature="Hardy", ability="Immunity", item="")}
    jobs = {"pokemon": pk, "pairs": [[k, "t", ["Flamethrower"], None] for k in ("both", "sf", "lo", "none")]}
    rows = {r["a"]: r["moves"]["Flamethrower"]["rolls"][-1]
            for r in pressure.run_node(teamscore._blob_path(), jobs)["results"]}
    ratio = {k: round(rows[k] / rows["none"], 3) for k in ("both", "sf", "lo")}
    out.append(("the calculator's row gives Sheer Force's 1.3 and the Life Orb's 1.3 together",
                abs(ratio["sf"] - 1.3) < 0.03 and abs(ratio["lo"] - 1.3) < 0.03 and abs(ratio["both"] - 1.69) < 0.05,
                f"Flamethrower {rows}; ratios to neither {ratio}"))
    return out


def infiltrator_checks():
    """An Infiltrator attacker's move passes another Pokemon's Substitute
    (BattleSystem_InfiltratorPasses, on main-engine-cleanups): its hit
    strikes the Pokemon behind it, and its added effects, status moves and
    stat drops land through it. A status from anything but a move (an
    ability, an item, Toxic Spikes), the holder's own Substitute, Transform
    and Sky Drop still meet it. On the planner's attack with set rows."""
    from .test_fightsim import battle as duel

    def setup(moves, ability):
        b, p, foe = duel(moves, ["Tackle"], {("p", m): [20] * 16 for m in moves}, hp=100)
        b.dice = pl.RunDice(random.Random(1), True)
        b.rng = b.dice.rng
        foe.ability, foe.sub, p.ability = "Battle Armor", 25, ability
        return b, p, foe
    got = {}
    for ability in ("Infiltrator", "Run Away"):
        b, p, foe = setup(["Tackle"], ability)
        pl.attack(b, p, fs.move("Tackle"), foe, True)
        hit = (100 - foe.hp, foe.sub)
        b, p, foe = setup(["Nuzzle"], ability)
        pl.attack(b, p, fs.move("Nuzzle"), foe, True)
        nuzzle = foe.status
        b, p, foe = setup(["Spore"], ability)
        pl.status_move(b, p, fs.move("Spore"), foe, True)
        spore = foe.status
        b, p, foe = setup(["Growl"], ability)
        pl.status_move(b, p, fs.move("Growl"), foe, True)
        got[ability] = (hit, nuzzle, spore, foe.stages["atk"])
    b, p, foe = setup(["Tackle"], "Infiltrator")
    plain = fs.give_status(b, foe, "psn")          # not from a move: an ability's, an item's, a hazard's
    p.sub = 10
    held = (fs.sub_blocks(p, p, fs.move("Tackle")), fs.sub_blocks(p, foe, fs.move("Transform")),
            fs.sub_blocks(p, foe, fs.move("Sky Drop")))
    ok = (got == {"Infiltrator": ((20, 25), "par", "slp", -1), "Run Away": ((0, 5), None, None, 0)}
          and plain is False and held == (True, True, True))
    return [("Infiltrator passes a Substitute with a move's hit, effects and status moves, and only then", ok,
             f"{got}; a status not from a move {plain}; own Substitute, Transform, Sky Drop held {held}")]


def charge_and_heal_block_checks():
    """Meteor Beam and Electro Shot charge with a Sp. Atk rise; a Power Herb
    skips the charge and still raises it, and Electro Shot skips in rain
    unless Cloud Nine is out; Skull Bash's Power Herb raises Defense
    (effect scripts 145, 324, 325). Heal Block and Psychic Noise block healing
    for five turns: healing moves fail and cannot be chosen, draining and
    Leech Seed heal nothing, Leftovers still heals (subscript_heal_block_start,
    Move_HealBlocked, the drain and Leech Seed subscripts). Draining Kiss
    heals three quarters. On the planner's routines with set rows."""
    from . import fightai
    from .test_fightsim import battle as duel
    out = []

    def fresh(pm, bm=("Tackle",), roll=20, hp=100):
        rolls = {("p", m): [roll] * 16 for m in pm}
        rolls.update({("b", m): [roll] * 16 for m in bm})
        b, p, foe = duel(list(pm), list(bm), rolls, hp=hp)
        b.dice = pl.RunDice(random.Random(1), True)
        b.rng = b.dice.rng
        foe.ability = "Battle Armor"
        return b, p, foe

    def charge(name, item=None, weather=None, foe_ability=None):
        b, p, foe = fresh([name])
        p.item, b.weather = item, weather
        if foe_ability:
            foe.ability = foe_ability
        pl.use_move(b, p, fs.move(name), foe, True)
        first = (100 - foe.hp, p.charging is not None, p.stages["spa"], p.stages["def"], p.item)
        if p.charging is not None:
            pl.use_move(b, p, fs.move(name), foe, True)
        return first, 100 - foe.hp
    got = {"Meteor Beam": charge("Meteor Beam"), "Meteor Beam, Power Herb": charge("Meteor Beam", "Power Herb"),
           "Electro Shot, rain": charge("Electro Shot", weather="Rain"),
           "Electro Shot, rain, Cloud Nine": charge("Electro Shot", weather="Rain", foe_ability="Cloud Nine"),
           "Skull Bash, Power Herb": charge("Skull Bash", "Power Herb")}
    # The Sp. Atk rise lands before the hit, so a 20 row deals 30.
    want = {"Meteor Beam": ((0, True, 1, 0, None), 30), "Meteor Beam, Power Herb": ((30, False, 1, 0, None), 30),
            "Electro Shot, rain": ((30, False, 1, 0, None), 30),
            "Electro Shot, rain, Cloud Nine": ((0, True, 1, 0, None), 30),
            "Skull Bash, Power Herb": ((20, False, 0, 1, None), 20)}
    out.append(("Meteor Beam and Electro Shot charge with a Sp. Atk rise, as the engine runs them", got == want,
                str(got)))

    # Heal Block from Psychic Noise, on the foe; then what it stops and what it does not.
    b, p, foe = fresh(["Psychic Noise"], ["Recover", "Giga Drain"], hp=100)
    pl.attack(b, p, fs.move("Psychic Noise"), foe, True)
    blocked = foe.heal_block
    foe.hp = 50
    pl.use_move(b, foe, fs.move("Recover"), p, True)
    recover = foe.hp
    chosen = fightai.invalid(b, foe, fs.move("Recover"))
    pl.attack(b, foe, fs.move("Giga Drain"), p, True)
    drain = foe.hp
    foe.item, foe.seeded, p.seeded = "Leftovers", False, True
    p.hp = 100
    for _ in range(5):
        fs.end_of_turn(b)
    after = (foe.hp, foe.heal_block)
    fs.end_of_turn(b)                                # the block is over: Leech Seed heals again
    sixth = foe.hp
    b2, p2, foe2 = fresh(["Heal Block"])
    foe2.sub = 25
    pl.status_move(b2, p2, fs.move("Heal Block"), foe2, True)
    on_sub = foe2.heal_block
    b3, p3, foe3 = fresh(["Draining Kiss"], roll=40)
    p3.hp = 50
    pl.attack(b3, p3, fs.move("Draining Kiss"), foe3, True)
    # Five turns' ends: Leftovers heals each one; Leech Seed's heal from the seeded
    # player's Pokemon is blocked on all five, since that Pokemon's turn end runs
    # before the blocked one counts down: the engine runs each Pokemon's turn end
    # in speed order (monSpeedOrder), and the seeded one is the faster here. (The
    # simulator runs the player's side first whatever the speeds.) On the sixth
    # Leech Seed heals again.
    ok = (blocked == 5 and recover == 50 and chosen and drain == 50 and after == (50 + 5 * (100 // 16), 0)
          and sixth == after[0] + 100 // 16 + 100 // 8 and on_sub == 0 and p3.hp == 80)
    out.append(("Heal Block and Psychic Noise block healing moves, draining and Leech Seed for five turns, "
                "not Leftovers; Draining Kiss heals three quarters", ok,
                f"blocked {blocked}; Recover leaves {recover}, refused by the AI {chosen}; Giga Drain leaves {drain}; "
                f"after five turns {after}, the sixth {sixth}; on a Substitute {on_sub}; "
                f"Draining Kiss heals to {p3.hp}"))
    return out


def end_order_enumeration_checks():
    """The planner's dice enumerate a speed tie at the turn's end at even
    odds (fightsim.end_order's coin), so a tied finish is weighed both ways."""
    from . import plplan
    from .test_fightsim import battle as duel
    b, p, foe = duel(["Tackle"], ["Tackle"], {}, p_speed=80, b_speed=80)
    b.dice = plplan.EnumDice((), random.Random(0))
    fs.end_order(b)
    tie = b.dice.events[0] if b.dice.events else None
    b2, p2, foe2 = duel(["Tackle"], ["Tackle"], {}, p_speed=100, b_speed=50)
    b2.dice = plplan.EnumDice((), random.Random(0))
    order = [m.side for m in fs.end_order(b2)]
    return [("the planner enumerates a speed tie at the turn's end; no tie, no coin",
             tie == (0.5, 0.5) and order == ["p", "b"] and not b2.dice.events,
             f"tie events {tie}; untied order {order}, events {b2.dice.events}")]


def types_ns(**kw):
    import types
    return types.SimpleNamespace(**kw)


def reckless_calc_checks():
    """Every move on an effect the game raises for Reckless deals 1.2 times
    as much with Reckless, the calculator's own boost and the simulator's
    (fs.reckless_fix) together: re-measured on the calculator, one level 100
    Staraptor with Reckless against the same with Intimidate. Catches the
    day the calculator learns a move's recoil, which would double the boost."""
    import types
    from . import pressure, teamscore
    by_name = fs._by_calc_name()[0]
    moves = sorted(n for n, r in by_name.items() if (r.get("effect") or "") in fs.reckless_effects() and r.get("power"))
    ivs = {k: 31 for k in ("hp", "at", "df", "sp", "sa", "sd")}
    mon = {"species": "Staraptor", "level": 100, "nature": "Hardy", "ivs": ivs, "evs": dict.fromkeys(ivs, 0), "item": ""}
    jobs = {"pokemon": {"r": dict(mon, ability="Reckless"), "i": dict(mon, ability="Intimidate"),
                        "t": dict(mon, species="Snorlax", level=50, ability="Thick Fat")},
            "pairs": [["r", "t", moves, None], ["i", "t", moves, None]]}
    rows = {r["a"]: r["moves"] for r in pressure.run_node(teamscore._blob_path(), jobs)["results"]}
    reckless = types.SimpleNamespace(ability="Reckless")
    off, small = [], []
    for n in moves:
        a, p = rows["r"].get(n, {}), rows["i"].get(n, {})
        if not a.get("rolls") or not p.get("rolls") or p["rolls"][-1] < 60:
            small.append(n)
            continue
        ratio = a["rolls"][-1] / p["rolls"][-1] * fs.reckless_fix(reckless, fs.move(n))
        if abs(ratio - 1.2) > 0.03:
            off.append(f"{n} {ratio:.3f}")
    return [("Reckless: the calculator's boost and the simulator's come to 1.2 on every move it raises",
             not off and len(moves) - len(small) >= 20,
             f"{len(moves) - len(small)} moves measured; off {off}; too small to measure {small}")]


def trick_room_checks():
    """Saturn 2 opens in the game's permanent Trick Room on every path, from
    the game's own list (battle_lib.c, sPermanentTrickRoomTrainers): the
    story fight, and the study's reader on his own file (which started clear
    until 2026-10-06). In the planner's battle the room stays through a
    Trick Room and ten turns' ends; Roark's file opens with none."""
    from . import plstep3, plstudy, plteam_test
    listed = fs.permanent_trick_room()
    recs = plstudy.fixed(plteam_test.box(plstep3.ROARK, 16))
    prep = plscore.prepare(plscore.parse_fight("saturn_2"), given_side=recs)
    boss_keys, flags, _ = prep["variants"][0]
    b = pl.make_battle(prep["st"], ["p0", "p1", "p2"], boss_keys, flags, 0)
    start = b.trick_room
    pl.status_move(b, b.p.cur(), fs.move("Trick Room"), b.b.cur(), True)
    for _ in range(10):
        fs.end_of_turn(b)
    study = {}
    for stem in ("commander_saturn_galactic_hq", "leader_roark"):
        st, _k, _f = plstudy.prepare([os.path.join(plstudy.RES, stem + ".json")], "HQ", 60, recs, plstudy.stock({}))
        study[stem] = st["trick_room"]
    ok = (listed == {"TRAINER_COMMANDER_SATURN_GALACTIC_HQ"} and prep["st"]["trick_room"] and start == 999
          and b.trick_room == 999 and study == {"commander_saturn_galactic_hq": True, "leader_roark": False})
    return [("Saturn 2 opens in the game's permanent Trick Room on the story and study paths", ok,
             f"list {sorted(listed)}; story {prep['st']['trick_room']}, battle {start} then {b.trick_room}; "
             f"study {study}")]


# The Kaizo study's worked examples brought these moves (2026-10-03).
STUDY_TEAM = [("SPECIES_BARBOACH", "Barboach", "Lonely", "Swift Swim", ["Hex", "Venoshock", "Assurance", "Mortal Spin"]),
              ("SPECIES_NACLI", "Nacli", "Impish", "Sturdy", ["Rapid Spin", "Toxic", "Rock Throw", "Gyro Ball"]),
              ("SPECIES_GRUBBIN", "Grubbin", "Relaxed", "Swarm", ["Bug Bite", "Bite", "Mud-Slap"])]


def study_effect_checks():
    """The effects the study's worked examples use that the simulator lacked
    (2026-10-03), each as the decomp has it: Hex, Venoshock and Assurance
    double by the target's state; Mortal Spin poisons and clears; Rapid Spin
    clears and raises Speed; Corrosion poisons Poison and Steel types with a
    move; Poison Touch poisons on contact; Thunder and kin reach a flier."""
    out = []
    b = battle(team=STUDY_TEAM)
    foe, barboach = b.b.cur(), b.p.cur()
    hex_ = mv(barboach, "Hex")

    def hp_lost(status, n=40):
        """Hex's average damage into the foe, its status as given."""
        lost = []
        for i in range(n):
            b.dice = pl.RunDice(random.Random(100 + i), True)
            foe.hp, foe.status, foe.sub = foe.maxhp, status, 0
            pl.attack(b, barboach, hex_, foe, True)
            lost.append(foe.maxhp - foe.hp)
        return sum(lost) / n
    plain, burnt = hp_lost(None), hp_lost("brn")
    foe.status = None
    venom = (fs.doubled(barboach, foe, mv(barboach, "Venoshock")),)
    foe.status = "psn"
    venom += (fs.doubled(barboach, foe, mv(barboach, "Venoshock")),)
    foe.status = "par"
    venom += (fs.doubled(barboach, foe, mv(barboach, "Venoshock")),)
    foe.status = None
    out.append(("Hex doubles on a status; Venoshock on poison only",
                plain > 0 and 1.8 <= burnt / plain <= 2.2 and venom == (False, True, False),
                f"Hex {plain:.1f} then {burnt:.1f} burnt; Venoshock clean/psn/par {venom}"))
    # Assurance: HP lost while the turn runs counts; at a replacement after
    # the turn's end it does not.
    assurance = mv(barboach, "Assurance")
    foe.hit_this_turn, foe.hurt_this_turn = None, False      # Hex's hits above were this turn's
    b.mid_turn = True
    fresh = fs.doubled(barboach, foe, assurance)
    fs.hurt(b, foe, 1)
    hurt = fs.doubled(barboach, foe, assurance)
    fs.end_of_turn(b)
    cleared = fs.doubled(barboach, foe, assurance)
    fs.hurt(b, foe, 1)               # mid_turn is off: a replacement's hazard damage
    replaced = fs.doubled(barboach, foe, assurance)
    foe.hit_this_turn = ("Physical", 5)
    struck = fs.doubled(barboach, foe, assurance)
    foe.hit_this_turn = None
    out.append(("Assurance doubles after HP lost this turn, not after a replacement's hazards",
                not fresh and hurt and not cleared and not replaced and struck,
                f"fresh {fresh}, hurt {hurt}, next turn {cleared}, replacement {replaced}, hit {struck}"))
    # Mortal Spin: poisons, and frees its user and side; Corrosion reaches a
    # Poison type with it and a Steel type with Toxic.
    b = battle(team=STUDY_TEAM)
    foe, barboach = b.b.cur(), b.p.cur()
    spin = mv(barboach, "Mortal Spin")
    b.p.hazards = {"rocks": 1, "spikes": 2, "tspikes": 1}
    barboach.bound, barboach.seeded = 3, True
    b.dice = pl.RunDice(random.Random(5), True)
    foe.hp = foe.maxhp
    pl.use_move(b, barboach, spin, foe, True)
    mortal = (foe.status, dict(b.p.hazards), barboach.bound, barboach.seeded, barboach.stages["spe"])
    corroded = []
    for ability in (None, "Corrosion"):
        foe.status, foe.types, barboach.ability = None, ["Poison"], ability
        foe.hp = foe.maxhp
        pl.use_move(b, barboach, spin, foe, True)
        corroded.append(foe.status)
    nacli = b.p.mons[1]
    fs.switch_in(b, b.p, 1)
    for ability in (None, "Corrosion"):
        foe.status, foe.types, nacli.ability = None, ["Steel"], ability
        pl.use_move(b, nacli, mv(nacli, "Toxic"), foe, True)
        corroded.append(foe.status)
    out.append(("Mortal Spin poisons and clears; Corrosion poisons Poison and Steel types",
                mortal == ("psn", {"rocks": 0, "spikes": 0, "tspikes": 0}, 0, False, 0)
                and corroded[0] is None and corroded[1] == "psn" and corroded[2] is None and corroded[3] == "tox",
                f"Mortal Spin {mortal}; Corrosion {corroded}"))
    # Rapid Spin: clears and raises Speed.
    foe.types = ["Rock", "Ground"]
    nacli.ability = "Sturdy"
    b.p.hazards = {"rocks": 1, "spikes": 0, "tspikes": 2}
    nacli.bound, nacli.seeded = 2, True
    foe.hp = foe.maxhp
    pl.use_move(b, nacli, mv(nacli, "Rapid Spin"), foe, True)
    rapid = (dict(b.p.hazards), nacli.bound, nacli.seeded, nacli.stages["spe"])
    out.append(("Rapid Spin clears its side and raises Speed a stage",
                rapid == ({"rocks": 0, "spikes": 0, "tspikes": 0}, 0, False, 1), f"Rapid Spin {rapid}"))
    # Gyro Ball: its power by the turn's Speeds, so a slowed user hits harder.
    gyro = mv(nacli, "Gyro Ball")
    nacli.stages["spe"] = 0
    level = pl.damage_of(b, nacli, foe, gyro, False, True)
    nacli.stages["spe"] = -2
    slowed = pl.damage_of(b, nacli, foe, gyro, False, True)
    want = fs.gyro_power(b.speed(foe), b.speed(nacli)) / fs.gyro_power(b.speed(foe), b.row_speed(nacli))
    nacli.stages["spe"] = 0
    out.append(("Gyro Ball's power follows the turn's Speeds",
                level and slowed > level and abs(slowed / level - want) < 0.1,
                f"Gyro Ball {level} then {slowed} slowed (power ratio {want:.2f})"))
    # Poison Touch: on contact when the defender's ability did nothing; not
    # through Rough Skin acting, nor on a Poison type.
    yes = (lambda kind, p, victim: True)                                   # noqa: E731
    first = (lambda kind, n: 0)                                            # noqa: E731
    b = battle(team=STUDY_TEAM)
    foe, grubbin = b.b.cur(), b.p.mons[2]
    fs.switch_in(b, b.p, 2)
    bite = mv(grubbin, "Bite")
    touched = []
    for ability, types in ((None, ["Rock"]), ("Rough Skin", ["Rock"]), (None, ["Poison"])):
        foe.status, foe.ability, foe.types = None, ability, types
        grubbin.ability, grubbin.hp = "Poison Touch", grubbin.maxhp
        fs.contact_ability(b, grubbin, foe, bite, 10, yes, first)
        touched.append(foe.status)
    out.append(("Poison Touch poisons on contact, not when Rough Skin acts or on a Poison type",
                touched == ["psn", None, None], f"Poison Touch {touched}"))
    # A Pokemon in the air: Gust doubles, Thunder and Sky Uppercut reach it,
    # Earthquake and Thousand Arrows do not.
    foe.charging = fs.move("Fly")
    air = {n: fs.reach_mult(fs.move(n), foe) for n in ("Gust", "Thunder", "Sky Uppercut", "Earthquake",
                                                         "Thousand Arrows")}
    foe.charging = None
    out.append(("Gust doubles into Fly; Thunder and Sky Uppercut reach it; Earthquake and Thousand Arrows do not",
                air == {"Gust": 2, "Thunder": 1, "Sky Uppercut": 1, "Earthquake": 0, "Thousand Arrows": 0},
                f"{air}"))
    # Sleep Talk picks through the battle's dice, so a play-out's replays of
    # a turn agree; the enumeration of a sleeping talker's turn completes.
    from . import plplan
    b = battle()
    foe, barboach = b.b.cur(), b.p.cur()
    talk = fs.move("Sleep Talk")
    own = list(foe.moves)
    foe.moves = [talk] + own
    foe.pp = {m.name: 10 for m in foe.moves}
    second = [m for m in own if m.effect not in fs.SLEEP_TALK_SKIPS and m.effect not in fs.TWO_TURN][1]
    foe.status, foe.sleep = "slp", 3

    class Second:
        def choice(self, kind, n):
            return 1
    b.dice = Second()
    picked = fs.sleep_talk_pick(b, foe)
    outcomes = plplan.turn_outcomes(b, ("move", mv(barboach, "Mud-Slap")), ("move", talk), 7)
    total = sum(p for _c, p in outcomes)
    out += blind_pool_checks()
    out += map_weather_checks()
    out += trick_room_checks()
    out += rework_checks()
    out += reckless_calc_checks()
    out += sheer_force_life_orb_checks()
    out += infiltrator_checks()
    out += charge_and_heal_block_checks()
    out += end_order_enumeration_checks()
    out.append(("Sleep Talk picks through the dice; a sleeping talker's turn enumerates",
                picked is second and len(outcomes) > 1 and abs(total - 1) < 1e-9,
                f"picked {picked.name}, {len(outcomes)} outcomes"))
    return out


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

    # The very unlucky stress test (Ian, 2026-10-06): Quick Claw and Focus
    # Band roll against the player, the trainer's firing if either of two
    # rolls does and the player's only if both do. The player's claw above
    # then fires about one time in twenty-five; the trainer's Focus Band
    # saves a Bronzor at 1 HP about 19 times in 100 hits, against 10 at
    # real odds. Each seed is played with and without the band, so a miss
    # (Rock Throw is 90 percent) never counts as a save.
    stressed = 0
    for i in range(400):
        c = pl.clone_battle(b)
        c.rng = random.Random(i); c.dice = pl.RunDice(c.rng, True, luck="unlucky")
        g, bz = c.p.cur(), c.b.cur()
        g.hp, bz.hp = g.maxhp, bz.maxhp
        log = []
        orig = pl.use_move
        pl.use_move = lambda bb, att, m, d, first, _o=orig, _l=log: (_l.append(att.side), _o(bb, att, m, d, first))
        try:
            pl._turn(c, ("move", mv(g, "Rock Throw")), ("move", mv(bz, "Calm Mind")))
        finally:
            pl.use_move = orig
        stressed += bool(log) and log[0] == "p"
    saves = {}
    for luck in ("real", "unlucky"):
        saves[luck] = 0
        for i in range(1000):
            alive = []
            for band in ("Focus Band", None):
                c = pl.clone_battle(b)
                c.rng = random.Random(i); c.dice = pl.RunDice(c.rng, True, luck=luck)
                g, bz = c.p.cur(), c.b.cur()
                bz.item, bz.hp = band, 1
                pl.attack(c, g, mv(g, "Rock Throw"), bz, True)
                alive.append(bz.hp > 0)
            saves[luck] += alive[0] and not alive[1]
    dice = {}
    for side in ("bad", "good"):
        for kind, p in (("quickclaw", 0.2), ("focusband", 0.1)):
            d = pl.RunDice(random.Random(7), True, luck="unlucky")
            roll = (lambda: d.bad(kind, p)) if side == "bad" else (lambda: d.good(p, kind))
            dice[f"{side} {kind}"] = round(sum(roll() for _ in range(20000)) / 20000, 3)
    want = {"bad quickclaw": 0.36, "bad focusband": 0.19, "good quickclaw": 0.04, "good focusband": 0.01}
    results.append(("the stress test rolls Quick Claw and Focus Band against the player",
                    stressed <= 35 and 55 <= saves["real"] <= 130 and 130 <= saves["unlucky"] <= 220
                    and all(abs(dice[k] - v) < 0.015 for k, v in want.items()),
                    f"player's claw first {stressed} of 400; band saves {saves['real']} real, "
                    f"{saves['unlucky']} unlucky of 1000; dice {dice}"))

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
    results += gender_checks()
    results += wish_spite_recycle_checks()
    results += held_state_checks()
    results += study_effect_checks()

    width = max(len(r[0]) for r in results)
    for name, ok, note in results:
        print(f"  {'ok  ' if ok else 'FAIL'}  {name:{width}}  {note}")
    passed = sum(1 for r in results if r[1])
    print(f"\n{passed}/{len(results)} passed")
    return 0 if passed == len(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())

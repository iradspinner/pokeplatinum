"""The mechanics the Roark fight showed missing from the perfect-line
simulator, each checked on that fight (the Overseer, 2026-09-30).

    PYTHONPATH=. python3 -m tools.oxide.balance.test_plfixes

The checks use Roark's team as it stood before his redesign of 2026-10-12
(Nosepass and Geodude with Block, Lileep with Acid, Larvitar, Cranidos),
saved in test_plfixes_roark.json, and Gardenia's as it stood before Ian's
six of 2026-10-13 (Breloom with Stun Spore, Ludicolo, a Natural Cure
Roserade), saved in test_plfixes_gardenia.json, so a later team for either
leaves them standing.
"""
import collections
import functools
import json
import math
import os
import random

from . import data, fightai, plscore, perfectline as pl, fightsim as fs

# The scorer reads a trainer's team through data.oxide_trainers() and its
# genders and abilities through plscore.with_genders(); both are pointed at
# the saved team here, before anything reads them.
_HERE = os.path.dirname(os.path.abspath(__file__))


def _fixture(name):
    with open(os.path.join(_HERE, name), encoding="utf-8") as fh:
        return json.load(fh)


# Each saved team, by its trainer file's stem. The names are written out so
# the gate's scope tool sees which files this test reads.
PINNED = {"leader_roark": _fixture("test_plfixes_roark.json"),
          "leader_gardenia": _fixture("test_plfixes_gardenia.json")}
ROARK = PINNED["leader_roark"]
_live_trainers = data.oxide_trainers
_live_genders = plscore.with_genders


@functools.lru_cache(maxsize=None)
def _pinned_trainers(root=data.ROOT):
    out = dict(_live_trainers(root))
    for stem, team in PINNED.items():
        party = data.calc_trainers.build_trainer(root, stem, team)
        tr_id = party[0][1]["tr_id"]
        out[tr_id] = dict(out[tr_id], ai=party[0][1].get("ai"), party=[data._mon(sp, s) for sp, s in party])
    return out


def _pinned_genders(t, tr=None):
    if tr is None and t.get("stem") in PINNED:
        tr = PINNED[t["stem"]]
    return _live_genders(t, tr)


data.oxide_trainers = _pinned_trainers
plscore.with_genders = _pinned_genders

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
    foe.item = None         # step 12's Nosepass holds Leftovers, which would heal it too
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

    # A Focus Sash holds a single hit from full HP, and every hit of a two
    # to five hit move after the first (focusItemActivated lasts the move;
    # the engine's rule, approved 2026-10-14, where until then the move's
    # total broke the Sash).
    b, p, foe = fresh(["Bullet Seed"], roll=150)
    foe.item = "Focus Sash"
    pl.attack(b, p, fs.move("Bullet Seed"), foe, True)
    b2, p2, foe2 = fresh(["Tackle"], roll=150)
    foe2.item = "Focus Sash"
    pl.attack(b2, p2, fs.move("Tackle"), foe2, True)
    out.append(("a Focus Sash holds a single hit, and every hit of a multi-hit move from full HP",
                (foe.hp, foe.item, foe2.hp, foe2.item) == (1, None, 1, None),
                f"Bullet Seed leaves {foe.hp} ({foe.item}), Tackle {foe2.hp} ({foe2.item})"))

    # The rising moves, Fury Cutter 10, 20, 30 and Triple Kick 20, 30, 40
    # (Ian, 2026-10-12): the calculator's row adds up all three hits, and
    # each hit after the first checks accuracy (Triple Kick's 90%).
    b, p, foe = fresh(["Fury Cutter"], roll=60, hp=200)
    pl.attack(b, p, fs.move("Fury Cutter"), foe, True)
    cutter = 200 - foe.hp
    kicks = set()
    for seed in range(1, 40):
        b, p, foe = fresh(["Triple Kick"], roll=90, hp=200, seed=seed)
        pl.attack(b, p, fs.move("Triple Kick"), foe, True)
        kicks.add(200 - foe.hp)
    fc_scale = fs.expected_hit_scale(fs.move("Fury Cutter"))
    tk_scale = fs.expected_hit_scale(fs.move("Triple Kick"))
    out.append(("Fury Cutter and Triple Kick: three rising hits on a row of all three; Spite has 5 PP",
                cutter == 60 and kicks <= {0, 20, 50, 90} and 90 in kicks and 50 in kicks
                and abs(fc_scale - 1.0) < 1e-9 and abs(tk_scale - (20 + 30 * 0.9 + 40 * 0.81) / 90) < 1e-9
                and fs.move("Spite").pp == 5,
                f"Fury Cutter dealt {cutter} on a 60 row; Triple Kick dealt {sorted(kicks)} on a 90 row; "
                f"expected scales {fc_scale:.3f} and {tk_scale:.3f}; Spite {fs.move('Spite').pp} PP"))

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
    from . import calc
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
            for r in calc.run_node(calc.blob_path(), jobs)["results"]}
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
    from . import calc
    by_name = fs._by_calc_name()[0]
    moves = sorted(n for n, r in by_name.items() if (r.get("effect") or "") in fs.reckless_effects() and r.get("power"))
    ivs = {k: 31 for k in ("hp", "at", "df", "sp", "sa", "sd")}
    mon = {"species": "Staraptor", "level": 100, "nature": "Hardy", "ivs": ivs, "evs": dict.fromkeys(ivs, 0), "item": ""}
    jobs = {"pokemon": {"r": dict(mon, ability="Reckless"), "i": dict(mon, ability="Intimidate"),
                        "t": dict(mon, species="Snorlax", level=50, ability="Thick Fat")},
            "pairs": [["r", "t", moves, None], ["i", "t", moves, None]]}
    rows = {r["a"]: r["moves"] for r in calc.run_node(calc.blob_path(), jobs)["results"]}
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


def neutralizing_gas_checks():
    """Neutralizing Gas (the simulator's support approved by Ian,
    2026-10-13) on the calculator's own rows and in the readings' battle.
    prepare() rows each Pokemon that can meet a holder on an ability-blank
    twin, so a Levitate Bronzor's twin takes the holder's Earthquake where
    Bronzor reads 0, and a Huge Power Azumarill's twin hits the holder half
    as hard. In perfectline's battle the gas sends them to those rows while
    the holder is in, and when it leaves at the start of a turn, Mightyena's
    Intimidate goes off again on the Pokemon that replaces it."""
    zero = dict.fromkeys(("hp", "at", "df", "sa", "sd", "sp"), 0)

    def foe(species, ability, moves):
        return {"species": species, "level": 30, "item": None, "ability": ability, "nature": "Hardy",
                "ivs": dict.fromkeys(zero, 31), "evs": dict(zero), "moves": moves, "sub_index": 0, "mega": None}

    def rec(species, ability, moves):
        return {"constant": "SPECIES_" + species.upper(), "species": species, "how": "plan", "level": 30,
                "nature": "Hardy", "ivs": dict(IV), "evs": dict(zero), "ability": ability, "moves": moves,
                "fill": False, "label": species}
    party = [foe("Weezing-Galar", "Neutralizing Gas", ["Earthquake", "Sludge Bomb"]),
             foe("Skuntank", "Aftermath", ["Earthquake", "Crunch"])]
    recs = [rec("Bronzor", "Levitate", ["Confusion", "Tackle"]), rec("Azumarill", "Huge Power", ["Aqua Tail"]),
            rec("Mightyena", "Intimidate", ["Bite"])]
    st = fs.prepare("Fantina", [party], None, cap=30, given_side=recs)
    st["held"] = {}          # no boosters, so a hit reads its row as it stands
    rows = st["rows"]

    def top(a, d, move):
        return max(rows[(None, a, d)]["moves"][move]["rolls"])
    quake = (top("b0.0", "p0", "Earthquake"), top("b0.0", "p0#ng", "Earthquake"))
    tail = (top("p1", "b0.0", "Aqua Tail"), top("p1#ng", "b0.0", "Aqua Tail"))
    twins = (st["gas"], st["gas_twin"].get("p0"), st["gas_twin"].get("p1"), st["gas_twin"].get("p2"))
    out = [("prepare rows a twin with its ability blank for each Pokemon that can meet the gas", twins ==
            (True, "p0#ng", "p1#ng", "p2#ng") and quake[0] == 0 and quake[1] > 0
            and 1.8 <= tail[0] / tail[1] <= 2.2,
            f"twins {twins}; Earthquake on Bronzor and its twin {quake}; Aqua Tail from Azumarill and its twin {tail}")]
    b = pl.make_battle(st, ["p0", "p1", "p2"], st["bosses"][0], 7, 0)
    bronzor, weezing = b.p.cur(), b.b.cur()
    under = (bronzor.ability, pl.damage_of(b, weezing, bronzor, fs.move("Earthquake"), False, True))
    copied = pl.clone_battle(b).gas_flag
    b2 = pl.make_battle(st, ["p1", "p0", "p2"], st["bosses"][0], 7, 0)
    hp_hit = pl.damage_of(b2, b2.p.cur(), b2.b.cur(), fs.move("Aqua Tail"), False, True)
    b3 = pl.make_battle(st, ["p2", "p0", "p1"], st["bosses"][0], 7, 0)
    dog = b3.p.cur()
    before = (dog.ability, b3.b.cur().stages["atk"])
    pl._turn(b3, ("move", fs.move("Bite")), ("switch", 1))
    after = (dog.ability, b3.b.cur().species, b3.b.cur().stages["atk"])
    fs.switch_in(b, b.b, 1)
    left = (bronzor.ability, pl.damage_of(b, b.b.cur(), bronzor, fs.move("Earthquake"), False, True))
    ok = (under[0] is None and under[1] and copied and hp_hit == tail[1] and before == (None, 0)
          and after == ("Intimidate", "Skuntank", -1) and left == ("Levitate", 0))
    out.append(("the readings' battle: the twins' rows while the holder is in, the real ones after; "
                "Intimidate again on the replacement", ok,
                f"Bronzor under the gas (ability, Earthquake) {under}, the copy keeps the gas {copied}; "
                f"Azumarill's Aqua Tail {hp_hit}; Mightyena before {before}, after the holder left {after}; "
                f"Bronzor after (ability, Skuntank's Earthquake) {left}"))
    return out


def unburden_checks():
    """Unburden counted once (Ian approved the fix, 2026-10-13). The engine
    doubles its holder's Speed only once the item it came in with is gone
    (BattleSystem_CompareBattlerSpeed reads canUnburden and an empty hand).
    The calculator's page counts every ability as active, so its Speed for
    an Unburden Pokemon came doubled from the first turn, and the battle
    doubled it again once the item went: Jupiter 1's Pelipper read 92, then
    184, where the game gives 46, then 92. On the calculator's real rows an
    Unburden Pelipper holding its Sitrus Berry is now as fast as a Pressure
    twin, twice as fast once the berry is eaten, and the player's Unburden
    Pelipper, which comes in holding nothing, is never doubled."""
    from .test_fightai import battle
    b = battle([("Pelipper", 26, "Unburden", ["Water Pulse"], "Sitrus Berry"),
                ("Pelipper", 26, "Pressure", ["Water Pulse"], "Sitrus Berry")],
               [("Pelipper", 26, "Unburden", ["Water Pulse"])])
    holder, twin, mine = b.b.mons[0], b.b.mons[1], b.p.cur()
    plain = b.speed(twin)
    held = b.speed(holder)
    fs.consume(holder)
    eaten = b.speed(holder)
    empty = b.speed(mine)
    ok = held == plain and eaten == 2 * plain and empty == plain
    return [("Unburden doubles Speed once, after the item is gone, on the calculator's rows", ok,
             f"Pressure twin {plain}; Unburden holding its berry {held}, after eating it {eaten}; "
             f"the player's empty-handed Unburden {empty}")]


def intimidate_once_checks():
    """Intimidate counted once (Ian approved the fix, 2026-10-13). The
    engine takes one Attack stage off each foe on the field as the holder
    comes in (the switch-in check's Intimidate step), and from no Pokemon
    that comes in later. The calculator's page counts every ability as
    active, so its rows already took a stage off every physical hit into an
    Intimidate Pokemon, from any attacker at any time, and the battle took a
    second on entry: Mars 1's Torracat met Machop's Karate Chop at about
    4/9 of its damage where one stage leaves 2/3. The rows now leave
    Intimidate off, and the battle's stage is its only effect. The battle's
    start is mended with it: the leads come in before their Intimidate
    goes off, so a trainer lead's Intimidate lands on the player's lead,
    which the player's own switch-in used to wipe."""
    from .test_fightai import battle
    tor = [("Torracat", 18, "Blaze", ["Double Kick"]), ("Torracat", 18, "Intimidate", ["Double Kick"])]
    chops = [("Machop", 20, "Guts", ["Karate Chop"]), ("Machop", 20, "Guts", ["Karate Chop"])]
    b = battle(tor, chops)
    blaze, scary = b.b.mons
    machop, second = b.p.mons
    kc = fs.move("Karate Chop")
    rows = (b.rolls(machop, scary, kc)[-1], b.rolls(machop, blaze, kc)[-1])
    plain = pl.damage_of(b, machop, blaze, kc, False, True)
    fs.switch_in(b, b.b, 1)              # the Intimidate Torracat comes in mid-battle
    into = (machop.stages["atk"], pl.damage_of(b, machop, scary, kc, False, True))
    fs.switch_in(b, b.p, 1)              # a Machop sent in after it keeps its Attack
    late = (second.stages["atk"], pl.damage_of(b, second, scary, kc, False, True))
    lead = battle(list(reversed(tor)), chops)
    led = lead.p.cur().stages["atk"]
    dogs = [("Mightyena", 20, "Intimidate", ["Bite"]), ("Mightyena", 20, "Quick Feet", ["Bite"])]
    mine = battle(tor, dogs)
    dk = fs.move("Double Kick")
    theirs = (mine.b.cur().stages["atk"], mine.rolls(mine.b.cur(), mine.p.mons[0], dk)[-1],
              mine.rolls(mine.b.cur(), mine.p.mons[1], dk)[-1])
    one_stage = int(plain * 2 / 3)
    ok = (rows[0] == rows[1] and into[0] == -1 and abs(into[1] - one_stage) <= 1 and late == (0, plain)
          and led == -1 and theirs[0] == -1 and theirs[1] == theirs[2])
    return [("Intimidate takes one stage, once, on entry; the rows leave it off", ok,
             f"Karate Chop's top row into Intimidate and Blaze Torracat {rows}; plain {plain}; "
             f"after Intimidate came in (stage, damage) {into}, one stage is {one_stage}; "
             f"a Machop sent in later {late}; a trainer lead's Intimidate on the player's lead {led}; "
             f"the player's Intimidate lead: the trainer's stage, Double Kick's top row into it and its twin {theirs}")]


def two_hit_checks():
    """Two-hit moves against Sturdy on the calculator's real rows and the
    readings' attack (approved 2026-10-13). The calculator caps a row's
    first hit into a full-HP Sturdy holder at its HP less one, and the
    readings then held the two hits as one, so Machop's Double Kick never
    finished a Sturdy Geodude. Now the first hit meets Sturdy and the
    second finishes it whenever the two come to its HP, a single Karate
    Chop is still held at 1 HP, and a Rock Head Geodude holding a Focus Sash
    keeps 1 HP against the pair, as the engine's Sash does, and loses it."""
    from .test_fightai import battle
    b = battle([("Geodude", 12, "Sturdy", ["Tackle"]), ("Geodude", 12, "Rock Head", ["Tackle"], "Focus Sash")],
               [("Machop", 20, "Guts", ["Double Kick", "Karate Chop"])])
    sturdy, sash = b.b.mons
    machop = b.p.cur()
    counts = collections.Counter()
    for seed in range(40):
        b.dice, b.rng = pl.RunDice(random.Random(seed), True), random.Random(seed)
        for target, name in ((sturdy, "Double Kick"), (sturdy, "Karate Chop"), (sash, "Double Kick")):
            target.hp, target.item = target.maxhp, b.st["pokemon"][target.key].get("item")
            pl.attack(b, machop, fs.move(name), target, True)
            counts[(target.ability, name, "fainted" if not target.alive() else f"{target.hp} HP",
                    target.item)] += 1
    rows = (max(b.rolls(machop, sturdy, fs.move("Double Kick"))), sturdy.maxhp)
    want = {("Sturdy", "Double Kick", "fainted", None): 40, ("Sturdy", "Karate Chop", "1 HP", None): 40,
            ("Rock Head", "Double Kick", "1 HP", None): 40}
    return [("a two-hit move breaks Sturdy on the calculator's rows; a Focus Sash still holds", dict(counts) == want,
             f"Double Kick's top row and Geodude's HP {rows}; over 40 tries each {dict(counts)}")]


def protect_checks():
    """Protect on the readings' path, on the calculator's real rows
    (approved 2026-10-14). Croagunk uses Detect in a turn the player
    switches Gengar out for Machop: the switch comes first, so no battler
    acts after the Detect, which fails (BtlCmd_TryProtection) and leaves
    the run at 0, where it worked and ran on to 1. A protecting Croagunk
    still takes Gengar's Phantom Force, which has no MOVE_FLAG_CAN_PROTECT,
    and its protection ends (subscript_feint), where Protect stopped it. A
    Detect at a run of 4 works one time in eight on the readings' dice, and
    the planner's dice offer it at exactly those odds (it was a
    sixteenth)."""
    from . import plplan
    from .test_fightai import battle
    b = battle([("Croagunk", 22, "Dry Skin", ["Detect", "Poison Jab"])],
               [("Gengar", 26, "Cursed Body", ["Phantom Force", "Shadow Ball"]), ("Machop", 26, "Guts", ["Low Kick"])])
    foe, gengar = b.b.cur(), b.p.cur()
    rng = random.Random(1)
    b.dice, b.rng = pl.RunDice(rng, True), rng
    pl._turn(b, ("switch", 1), ("move", fs.move("Detect")))
    slower = (foe.protecting, foe.protect_run, b.p.cur().species)
    fs.switch_in(b, b.p, 0)
    foe.hp, foe.protecting = foe.maxhp, True
    pl.attack(b, gengar, fs.move("Phantom Force"), foe, True)
    phantom = (foe.maxhp - foe.hp > 0, foe.protecting)
    works = 0
    for s in range(4000):
        b.dice, b.rng = pl.RunDice(random.Random(s), True), random.Random(s)
        foe.protecting, foe.protect_run = False, 4
        pl.status_move(b, foe, fs.move("Detect"), gengar, True)
        works += foe.protecting
    foe.protecting, foe.protect_run = False, 4
    b.dice = plplan.EnumDice((), random.Random(0))
    pl.status_move(b, foe, fs.move("Detect"), gengar, True)
    offered = b.dice.events
    ok = slower == (False, 0, "Machop") and phantom == (True, False) and 0.105 <= works / 4000 <= 0.145 \
        and offered == [(0.875, 0.125)]
    return [("Protect on the readings' path: it fails acting last, Phantom Force passes it, its run floors at "
             "an eighth", ok,
             f"Detect as the player switches (protecting, run, in) {slower}; Phantom Force into Detect "
             f"(hit, still protecting) "
             f"{phantom}; Detect at run 4 worked {works / 4000:.3f}; planner's event {offered}")]


def confusion_checks():
    """Confusion on the readings' path, on the calculator's real rows
    (approved 2026-10-14): a Machop's Dynamic Punch confuses an Oblivious
    Slowpoke holding a Lum Berry, which cures it at once and is used up (it
    waited for the turn's end), and leaves an Own Tempo Slowpoke unconfused
    (it confused it); a Lumineon's Swagger into the player's side under
    Safeguard raises the Attack and confuses nothing (it confused)."""
    from .test_fightai import battle
    b = battle([("Slowpoke", 16, "Oblivious", ["Tackle"], "Lum Berry"), ("Slowpoke", 16, "Own Tempo", ["Tackle"]),
                ("Lumineon", 16, "Swift Swim", ["Swagger"])],
               [("Machop", 16, "Guts", ["Dynamic Punch"])])
    lum, slowpoke, lumineon = b.b.mons
    machop = b.p.cur()
    machop.stages["acc"] = 6                     # Dynamic Punch's 50% always lands
    out = []
    for target in (lum, slowpoke):
        b.dice, b.rng = pl.RunDice(random.Random(1), True), random.Random(1)
        target.hp = target.maxhp
        pl.attack(b, machop, fs.move("Dynamic Punch"), target, True)
        out.append((target.ability, target.alive(), bool(target.confused), target.item))
    machop.stages["acc"] = 0
    b.p.safeguard = 5
    lumineon.stages["acc"] = 6
    pl.status_move(b, lumineon, fs.move("Swagger"), machop, True)
    out.append(("Machop under Safeguard", bool(machop.confused), machop.stages["atk"]))
    want = [("Oblivious", True, False, None), ("Own Tempo", True, False, None), ("Machop under Safeguard", False, 2)]
    return [("the readings' confusion meets a Lum Berry at once, Own Tempo on a hit, and Safeguard", out == want,
             f"(standing, confused, item; or confused, Attack stage) {out}")]


def curse_rest_checks():
    """The Ghost Curse and Rest on the readings' path, on the calculator's
    real rows (approved 2026-10-14): a Haunter's Curse into a Machop behind
    a Substitute fails and costs Haunter nothing (it cut half and cursed
    through the Substitute), and into a Machop already cursed fails the same;
    an Insomnia Hoothoot's Rest at half HP fails and names Insomnia (it slept
    and healed)."""
    from .test_fightai import battle
    b = battle([("Haunter", 25, "Levitate", ["Curse"]), ("Hoothoot", 25, "Insomnia", ["Rest"])],
               [("Machop", 25, "Guts", ["Karate Chop"])])
    haunter, hoothoot = b.b.mons
    machop = b.p.cur()
    b.dice, b.rng = pl.RunDice(random.Random(1), True), random.Random(1)
    machop.sub = machop.maxhp // 4
    pl.status_move(b, haunter, fs.move("Curse"), machop, True)
    behind = (haunter.maxhp - haunter.hp, machop.cursed)
    machop.sub, machop.cursed = 0, True
    pl.status_move(b, haunter, fs.move("Curse"), machop, True)
    again = haunter.maxhp - haunter.hp
    fs.switch_in(b, b.b, 1)
    hoothoot.hp = hoothoot.maxhp // 2
    pl.status_move(b, hoothoot, fs.move("Rest"), machop, True)
    rest = (hoothoot.hp == hoothoot.maxhp, hoothoot.status, hoothoot.revealed)
    return [("the readings' Ghost Curse fails behind a Substitute and on a cursed target; Insomnia stops Rest",
             behind == (0, False) and again == 0 and rest == (False, None, "Insomnia"),
             f"behind a Substitute (Haunter's HP lost, cursed) {behind}; already cursed, HP lost {again}; "
             f"Insomnia's Rest (healed, status, named) {rest}")]


def mist_intimidate_checks():
    """Mist and Intimidate on the readings' path, on the calculator's real
    rows (approved 2026-10-14): a Lombre's Mist keeps a Granbull's
    Intimidate and a Glameow's Growl off its Attack (both cut it), the
    trainer's AI then scores a second Mist -8, where it scored 0, and once
    Mist is gone a Substitute keeps Intimidate off (it cut it)."""
    from .test_fightai import battle
    b = battle([("Glameow", 25, "Limber", ["Growl"]), ("Granbull", 25, "Intimidate", ["Bite"])],
               [("Lombre", 25, "Swift Swim", ["Mist", "Water Gun"])])
    glameow, granbull = b.b.mons
    lombre = b.p.cur()
    b.dice, b.rng = pl.RunDice(random.Random(1), True), random.Random(1)
    pl.status_move(b, lombre, fs.move("Mist"), glameow, True)
    pl.status_move(b, glameow, fs.move("Growl"), lombre, True)
    fs.switch_in(b, b.b, 1)
    misted = (lombre.stages["atk"], getattr(b.p, "mist", 0))
    score = fightai.basic(b, lombre, granbull, fs.move("Mist"), None)
    b.p.mist, lombre.stages["atk"] = 0, 0
    fs.switch_in(b, b.b, 0)
    lombre.sub = lombre.maxhp // 4
    fs.switch_in(b, b.b, 1)
    behind = lombre.stages["atk"]
    return [("the readings' Mist stops Growl and Intimidate, the AI reads it, and a Substitute stops Intimidate",
             misted == (0, 5) and score == -8 and behind == 0,
             f"under Mist (Attack, turns) {misted}; a second Mist scores {score}; behind a Substitute {behind}")]


def ai_field_checks():
    """The trainer's AI on the readings' path reads what the battle now sets
    (approved 2026-10-14), on the calculator's real rows: a Munchlax whose
    Lum Berry has cured a poison is offered Recycle by the planner's exact
    odds of its AI (it was never offered, as the AI read an item nothing
    set), and a Machop's Bug Bite that eats the Munchlax's Sitrus Berry
    leaves the Machop marked as having eaten a Berry, which Belch needs."""
    from . import plplan
    from .test_fightai import battle
    b = battle([("Munchlax", 20, "Pickup", ["Recycle", "Tackle"], "Lum Berry")],
               [("Machop", 20, "Guts", ["Karate Chop", "Bug Bite"])])
    munchlax, machop = b.b.cur(), b.p.cur()
    b.dice, b.rng = pl.RunDice(random.Random(1), True), random.Random(1)
    b.quick = {}
    plplan.reset()
    before = dict((a[1].name, round(p, 3)) for a, p in plplan.ai_distribution(b))
    fs.give_status(b, munchlax, "tox")
    plplan.reset()
    after = dict((a[1].name, round(p, 3)) for a, p in plplan.ai_distribution(b))
    munchlax.item, munchlax.hp = "Sitrus Berry", munchlax.maxhp
    pl.attack(b, machop, fs.move("Bug Bite"), munchlax, True)
    bitten = (munchlax.item, getattr(machop, "ate_berry", False))
    ok = before.get("Recycle", 0) == 0 and after.get("Recycle", 0) > 0.5 and bitten == (None, True)
    return [("the readings' AI offers Recycle once an item is used up; Bug Bite marks its user as having eaten",
             ok, f"Recycle's odds before {before.get('Recycle', 0)}, after the Lum Berry {after.get('Recycle', 0)}; "
                 f"after Bug Bite (Munchlax's item, Machop ate) {bitten}")]


def pp_checks():
    """PP on the readings' path, on the calculator's real rows (approved
    2026-10-14): a Staravia's Fly costs one PP over its two turns, the
    strike's turn already paid (it cost two), and its Quick Attack into a
    Pressure Dusclops costs two (it cost one)."""
    from .test_fightai import battle
    b = battle([("Geodude", 30, "Rock Head", ["Tackle"]), ("Dusclops", 30, "Pressure", ["Night Shade"])],
               [("Staravia", 30, "Reckless", ["Fly", "Quick Attack"])])
    geodude, dusclops = b.b.mons
    star = b.p.cur()
    b.dice, b.rng = pl.RunDice(random.Random(1), True), random.Random(1)
    pl.use_move(b, star, fs.move("Fly"), geodude, True)
    pl.use_move(b, star, star.charging, geodude, True)
    fly = 15 - star.pp["Fly"]
    fs.switch_in(b, b.b, 1)
    pl.use_move(b, star, fs.move("Quick Attack"), dusclops, True)
    quick = fs.move("Quick Attack").pp - star.pp["Quick Attack"]
    return [("the readings charge PP once a choice, and Pressure adds one", (fly, quick, star.charging) == (1, 2, None),
             f"Fly over its two turns {fly}; Quick Attack into Pressure {quick}")]


def hit_by_hit_checks():
    """A move of several hits on the readings' path lands hit by hit
    (perfectline.multi_hit, fightsim.land_hits; approved 2026-10-14). On
    hand rows: Skill Link Bullet Seed at a critical stage of +2 rolls a
    critical hit a hit, its totals spreading from 50 to 75 in steps of 5
    (one roll gave 50 or 75); a Focus Band rolls at every hit, saving its
    holder from five hits of 30 about 34 times in a hundred (one roll at the
    lethal total, 10); and the planner's dice take the number of critical
    hits as one event at the binomial odds. On the calculator's real rows,
    a Skill Link Minccino's Tail Slap into a Rough Skin Gible costs it five
    eighths of its 70 HP, 40, where one chance took 8."""
    from . import plplan
    from .test_fightai import battle
    from .test_fightsim import battle as duel

    def fresh(row, seed=1, item=None, stage=0, hp=400):
        b, p, foe = duel(["Bullet Seed"], ["Tackle"], {("p", "Bullet Seed"): [row] * 16}, hp=hp, seed=seed)
        b.dice = pl.RunDice(random.Random(seed), True)
        b.rng = b.dice.rng
        p.ability, p.crit_stage, foe.item = "Skill Link", stage, item
        if not stage:
            foe.ability = "Battle Armor"
        return b, p, foe
    totals = collections.Counter()
    for s in range(400):
        b, p, foe = fresh(50, seed=s, stage=2)
        pl.attack(b, p, fs.move("Bullet Seed"), foe, True)
        totals[400 - foe.hp] += 1
    band = 0
    for s in range(2000):
        b, p, foe = fresh(150, seed=s, item="Focus Band", hp=100)
        pl.attack(b, p, fs.move("Bullet Seed"), foe, True)
        band += foe.hp == 1
    b, p, foe = fresh(50, stage=1)
    b.dice = plplan.EnumDice((), random.Random(0))
    pl.attack(b, p, fs.move("Bullet Seed"), foe, True)
    binom = tuple(round(math.comb(5, k) * (1 / 8) ** k * (7 / 8) ** (5 - k), 12) for k in range(6))
    enumerated = [tuple(round(x, 12) for x in ev) for ev in b.dice.events]

    b = battle([("Gible", 25, "Rough Skin", ["Tackle"])], [("Minccino", 25, "Skill Link", ["Tail Slap"])])
    gible, minccino = b.b.cur(), b.p.cur()
    lost = set()
    for seed in range(20):
        b.dice, b.rng = pl.RunDice(random.Random(seed), True), random.Random(seed)
        gible.hp, minccino.hp = gible.maxhp, minccino.maxhp
        pl.use_move(b, minccino, fs.move("Tail Slap"), gible, True)
        if gible.hp < gible.maxhp:
            lost.add(minccino.maxhp - minccino.hp)
    ok = (set(totals) <= {50, 55, 60, 65, 70, 75} and len(totals) >= 5 and 0.30 <= band / 2000 <= 0.39
          and binom in enumerated and lost == {5 * (minccino.maxhp // 8)})
    return [("the readings land a move of several hits hit by hit: a critical hit, the Focus Band and Rough Skin "
             "per hit", ok,
             f"Bullet Seed totals {dict(sorted(totals.items()))}; Focus Band held {band / 2000:.3f}; planner's "
             f"critical-hit event {binom in enumerated}; Minccino ({minccino.maxhp} HP) lost {sorted(lost)} "
             f"to Gible's Rough Skin")]


def future_sight_checks():
    """Future Sight on the calculator's real rows and the readings' battle
    (approved 2026-10-13). The calculator rows the two moves with no type
    chart and no STAB: Kadabra's Doom Desire (140, Steel) and Future Sight
    (120, Psychic) on a Fighting Machop stand at about 140 to 120, though
    Psychic hits Machop twice over and is Kadabra's own type, and a Dark
    Murkrow takes Future Sight in full. In the readings' battle the hit on
    Machop waits: nothing at once, then the stored damage at the end of the
    second turn after, on the Murkrow that has come in; meanwhile the
    trainer's AI scores a second one -12, as Basic_CheckFutureSight reads
    the side's mark, and a copy of the battle, as the planner and the
    search make, carries the waiting hit."""
    from .test_fightai import battle
    b = battle([("Kadabra", 30, "Synchronize", ["Future Sight", "Doom Desire"])],
               [("Machop", 30, "Guts", ["Karate Chop"]), ("Murkrow", 30, "Insomnia", ["Peck"])])
    kad, machop, murkrow = b.b.cur(), b.p.mons[0], b.p.mons[1]
    fsight, desire = fs.move("Future Sight"), fs.move("Doom Desire")
    ratio = max(b.rolls(kad, machop, desire)) / max(b.rolls(kad, machop, fsight))
    dark = max(b.rolls(kad, murkrow, fsight))
    b.dice, b.rng = pl.RunDice(random.Random(4), True), random.Random(4)
    pl.use_move(b, kad, fsight, machop, True)
    at_once = machop.maxhp - machop.hp
    waiting = getattr(b.p, "future", (None,))[0]
    ai = fightai.basic(b, kad, machop, fsight)
    copied = waiting is not None and pl.clone_battle(b).p.future == b.p.future
    hp = []
    for turn in range(3):
        if turn == 1:
            fs.switch_in(b, b.p, 1)          # the Dark Murkrow stands in the slot when it lands
        fs.end_of_turn(b)
        hp.append(murkrow.hp)
    dmg = waiting[1] if waiting else None
    ok = (1.12 <= ratio <= 1.22 and dark > 0 and at_once == 0 and waiting is not None and ai == -12 and copied
          and hp == [murkrow.maxhp, murkrow.maxhp, murkrow.maxhp - dmg])
    return [("Future Sight: a typeless row, and in the readings' battle it lands two turns on", ok,
             f"Doom Desire over Future Sight on Machop {ratio:.3f}; Future Sight's top row on Murkrow {dark}; "
             f"at once {at_once}; waiting {waiting}; the AI's Basic {ai}; the copy carries it {copied}; "
             f"Murkrow's HP after each turn's end {hp} of {murkrow.maxhp}")]


def disable_and_nightmare_checks():
    """Disable and Nightmare on the calculator's real rows and the readings'
    battle (approved 2026-10-13): after a Geodude's Tackle, Drowzee's Disable
    keeps it out of the player's options and makes a Tackle chosen before it
    fail, and the trainer's AI scores a second Disable -8; Gastly's
    Nightmare on the sleeping Geodude takes a quarter of its HP at the
    turn's end."""
    from .test_fightai import battle
    b = battle([("Drowzee", 20, "Insomnia", ["Disable", "Pound"]), ("Gastly", 20, "Levitate", ["Nightmare", "Lick"])],
               [("Geodude", 20, "Sturdy", ["Tackle", "Rock Throw"])])
    drowzee, gastly = b.b.mons
    geo = b.p.cur()
    b.dice, b.rng = pl.RunDice(random.Random(2), True), random.Random(2)
    pl.use_move(b, geo, fs.move("Tackle"), drowzee, True)
    pl.use_move(b, drowzee, fs.move("Disable"), geo, True)
    options = sorted(a[1].name for a in pl.player_actions(b) if a[0] == "move")
    before = drowzee.hp
    pl.use_move(b, geo, fs.move("Tackle"), drowzee, True)
    blocked = before - drowzee.hp
    second = fightai.basic(b, drowzee, geo, fs.move("Disable"))
    fs.switch_in(b, b.b, 1)
    geo.status, geo.sleep = "slp", 3
    pl.use_move(b, gastly, fs.move("Nightmare"), geo, True)
    hp = geo.hp
    fs.end_of_turn(b)
    lost = hp - geo.hp
    ok = options == ["Rock Throw"] and blocked == 0 and second == -8 and lost == max(1, geo.maxhp // 4)
    return [("the readings' battle: Disable keeps the move out of the player's options, Nightmare bites", ok,
             f"the player's moves after Disable {options}; Tackle dealt {blocked}; a second Disable {second}; "
             f"Nightmare took {lost} of {geo.maxhp} at the turn's end")]


def pivot_checks():
    """U-turn after a knockout or a Substitute's hit (approved 2026-10-14;
    subscript_attack_then_switch_out runs on any hit). On the calculator's
    real rows, in the readings' turn: Liepard's U-turn that knocks Machop
    out still takes Liepard out (Golbat in), as does one that only breaks a
    Substitute, and one that leaves Machop standing; with the player's side
    beaten, or nothing on the trainer's bench, Liepard stays."""
    from .test_fightai import battle
    foes = [("Liepard", 22, "Limber", ["U-turn"]), ("Golbat", 22, "Inner Focus", ["Bite"])]
    mine = [("Machop", 20, "Guts", ["Karate Chop"]), ("Geodude", 20, "Rock Head", ["Tackle"])]
    got = {}
    for label, hp, sub in (("knocked out", 1, 0), ("behind a Substitute", None, 30), ("hit", None, 0)):
        b = battle(foes, mine)
        b.dice, b.rng = pl.RunDice(random.Random(1), True), random.Random(1)
        machop = b.p.cur()
        machop.hp = hp or machop.hp
        machop.sub = sub
        uturn = fs.move("U-turn")
        pl._turn(b, ("move", fs.move("Karate Chop")), ("move", uturn))
        got[label] = b.b.cur().species
    b = battle(foes, mine[:1])
    b.dice, b.rng = pl.RunDice(random.Random(1), True), random.Random(1)
    b.p.cur().hp = 1
    pl._turn(b, ("move", fs.move("Karate Chop")), ("move", fs.move("U-turn")))
    got["the player beaten"] = b.b.cur().species
    b = battle(foes[:1], mine)
    b.dice, b.rng = pl.RunDice(random.Random(1), True), random.Random(1)
    b.p.cur().hp = 1
    pl._turn(b, ("move", fs.move("Karate Chop")), ("move", fs.move("U-turn")))
    got["no bench"] = b.b.cur().species
    want = {"knocked out": "Golbat", "behind a Substitute": "Golbat", "hit": "Golbat",
            "the player beaten": "Liepard", "no bench": "Liepard"}
    return [("U-turn switches its user out after a knockout or a Substitute's hit, as the engine does",
             got == want, f"the trainer's Pokemon after the turn {got}")]


def ice_body_checks():
    """Ice Body on the calculator's real rows (approved 2026-10-14): in a
    fight held in hail, Moira's Galarian Mr. Mime at half HP gets a
    sixteenth of its HP back at the turn's end, through fightsim's turn's
    end, which the readings share; a Pressure twin gets nothing."""
    from .test_fightai import battle
    b = battle([("Mr. Mime-Galar", 26, "Ice Body", ["Freeze-Dry"]), ("Mr. Mime-Galar", 26, "Pressure", ["Freeze-Dry"])],
               [("Machop", 26, "Guts", ["Karate Chop"])], weather="Hail")
    body, twin = b.b.mons
    body.hp, twin.hp = body.maxhp // 2, twin.maxhp // 2
    before = (body.hp, twin.hp)
    fs.end_of_turn(b)
    fs.switch_in(b, b.b, 1)
    fs.end_of_turn(b)
    gained = (body.hp - before[0], twin.hp - before[1])
    ok = b.weather == "Hail" and gained == (body.maxhp // 16, 0)
    return [("Ice Body heals a sixteenth in hail on the real rows", ok,
             f"weather {b.weather}; gained at the turn's end (Ice Body, Pressure) {gained} of {body.maxhp}")]


def readings_damage_checks():
    """The readings' damage (perfectline.damage_of) takes fightsim's own two
    corrections (approved 2026-10-14), as the engine's damage has them
    (battle_lib.c, BattleSystem_CalcMoveDamage): Reflect halves neither
    Brick Break, which breaks it, nor an Infiltrator's hit, nor a critical
    hit; and the calculator rows a Flash Fire attacker as always lit, so
    its Fire move counts two thirds until a Fire hit has lit it. Rows of 30,
    on a hand-built battle."""
    from .test_fightsim import battle as hand
    rows = {("p", "Brick Break"): [30] * 16, ("p", "Tackle"): [30] * 16, ("p", "Ember"): [30] * 16}
    b, p, foe = hand(["Brick Break", "Tackle", "Ember"], ["Tackle"], rows)
    b.b.screens["Reflect"] = 5

    def both(name, crit=False):
        mv = fs.move(name)
        return pl.damage_of(b, p, foe, mv, crit, False), b.damage(p, foe, mv, crit=crit, roll=0)
    got = {"Brick Break into Reflect": both("Brick Break"), "Tackle into Reflect": both("Tackle"),
           "a critical Tackle into Reflect": both("Tackle", True)}
    p.ability = "Infiltrator"
    got["an Infiltrator's Tackle into Reflect"] = both("Tackle")
    p.ability = "Flash Fire"
    got["an unlit Flash Fire's Ember"] = both("Ember")
    p.flash_fire = True
    got["a lit Flash Fire's Ember"] = both("Ember")
    want = {"Brick Break into Reflect": (30, 30), "Tackle into Reflect": (15, 15),
            "a critical Tackle into Reflect": (45, 45), "an Infiltrator's Tackle into Reflect": (30, 30),
            "an unlit Flash Fire's Ember": (20, 20), "a lit Flash Fire's Ember": (30, 30)}
    return [("the readings' damage passes a screen as fightsim's does, and Flash Fire counts only when lit",
             got == want, f"(readings, fightsim) {got}")]


def absorbing_ability_checks():
    """The absorbing abilities on the calculator's real rows, in the
    readings' battle (approved 2026-10-14): a Volt Absorb Lanturn at half HP
    takes a Pikachu's Thunderbolt whole and gets a quarter of its HP back,
    and Roark's Storm Drain Lileep takes a Barboach's Water Gun and rises a
    stage of Sp. Atk (Roark's readings move with this)."""
    from .test_fightai import battle
    b = battle([("Lanturn", 26, "Volt Absorb", ["Discharge"]), ("Lileep", 16, "Storm Drain", ["Mega Drain"])],
               [("Pikachu", 26, "Static", ["Thunderbolt"]), ("Barboach", 16, "Oblivious", ["Water Gun"])])
    lanturn, lileep = b.b.mons
    pika, barb = b.p.mons
    b.dice, b.rng = pl.RunDice(random.Random(1), True), random.Random(1)
    lanturn.hp = lanturn.maxhp // 2
    before = lanturn.hp
    pl.use_move(b, pika, fs.move("Thunderbolt"), lanturn, True)
    healed = lanturn.hp - before
    fs.switch_in(b, b.b, 1)
    fs.switch_in(b, b.p, 1)
    pl.use_move(b, barb, fs.move("Water Gun"), lileep, True)
    rise = (lileep.hp == lileep.maxhp, lileep.stages["spa"])
    ok = healed == lanturn.maxhp // 4 and rise == (True, 1)
    return [("the readings' battle: Volt Absorb heals a quarter, Storm Drain raises Sp. Atk", ok,
             f"Lanturn healed {healed} of {lanturn.maxhp}; Lileep after Water Gun (full HP, Sp. Atk stage) {rise}")]


def roost_checks():
    """Roost on the calculator's real rows (approved 2026-10-14): prepare
    rows a Water and Flying Pelipper's twin typed Water alone, so once it
    has roosted a Diglett's Earthquake reaches it and a Pikachu's
    Thunderbolt hits it twice over rather than four times, in the readings'
    damage, until the turn's end."""
    from .test_fightai import battle
    b = battle([("Pelipper", 26, "Keen Eye", ["Roost", "Water Pulse"])],
               [("Diglett", 26, "Sand Veil", ["Earthquake"]), ("Pikachu", 26, "Static", ["Thunderbolt"])])
    pel = b.b.cur()
    dig, pika = b.p.mons
    quake, bolt = fs.move("Earthquake"), fs.move("Thunderbolt")
    twins = b.st["roost_twin"].get(pel.key)
    before = (pl.damage_of(b, dig, pel, quake, False, True), pl.damage_of(b, pika, pel, bolt, False, True))
    b.dice, b.rng = pl.RunDice(random.Random(1), True), random.Random(1)
    pel.hp = pel.maxhp // 2
    pl.use_move(b, pel, fs.move("Roost"), dig, True)
    during = (pel.roosting, pl.damage_of(b, dig, pel, quake, False, True), pl.damage_of(b, pika, pel, bolt, False, True))
    fs.end_of_turn(b)
    after = (pel.roosting, pl.damage_of(b, dig, pel, quake, False, True))
    ok = (twins and twins[0][1] == ["Water"] and before[0] == 0 and during[0] is True and during[1] > 0
          and abs(during[2] * 2 - before[1]) <= 2 and after == (False, 0))
    return [("Roost: the twin without Flying meets the foe's moves while Pelipper roosts", ok,
             f"twins {twins}; before (Earthquake, Thunderbolt) {before}; while roosting (roosting, Earthquake, "
             f"Thunderbolt) {during}; the next turn {after}")]


def protean_checks():
    """Protean on the calculator's real rows and the readings' move
    (approved 2026-10-14): prepare rows a twin of Mars 1's Floragato for
    each type its moves could make it; after its Play Rough it is a Fairy
    type, so the next Play Rough has STAB, about half again its old row,
    and Machop's Karate Chop meets a Fairy, half what it did on Grass."""
    from .test_fightai import battle
    b = battle([("Floragato", 20, "Protean", ["Play Rough", "Seed Bomb"])], [("Machop", 20, "Guts", ["Karate Chop"])])
    flora, machop = b.b.cur(), b.p.cur()
    rough, chop = fs.move("Play Rough"), fs.move("Karate Chop")
    twins = sorted((b.st.get("protean_twin") or {}).get(flora.key, {}))
    before = (pl.damage_of(b, flora, machop, rough, False, True), pl.damage_of(b, machop, flora, chop, False, True))
    b.dice, b.rng = pl.RunDice(random.Random(1), True), random.Random(1)
    machop.hp = machop.maxhp * 10
    pl.use_move(b, flora, rough, machop, True)
    after = (list(flora.types), pl.damage_of(b, flora, machop, rough, False, True),
             pl.damage_of(b, machop, flora, chop, False, True))
    ok = (twins == ["Fairy"] and after[0] == ["Fairy"] and 1.4 <= after[1] / max(1, before[0]) <= 1.6
          and abs(after[2] * 2 - before[1]) <= 2)
    return [("Protean: Floragato becomes a Fairy type, with STAB for Play Rough, on its twin's rows", ok,
             f"twins {twins}; before (Play Rough, Karate Chop) {before}; after (types, Play Rough, Karate Chop) {after}")]


def magic_guard_checks():
    """Magic Guard in the readings' battle on the calculator's real rows
    (approved 2026-10-14): a Magic Guard Clefable (Gardenia's boxes field a
    Magic Guard Alolan Ninetales the same way) now comes in over Stealth Rock
    and takes Gardenia's Cherrim's Leech Seed at no cost, where a Cute Charm
    Clefable loses an eighth to each; the seeding Cherrim heals nothing off
    the first."""
    from .test_fightai import battle
    b = battle([("Cherrim", 24, "Flower Gift", ["Leech Seed", "Petal Blizzard"])],
               [("Clefable", 25, "Magic Guard", ["Moonblast"]), ("Clefable", 25, "Cute Charm", ["Moonblast"]),
                ("Barboach", 25, "Oblivious", ["Water Gun"])])
    cherrim = b.b.cur()
    guard, plain, _barb = b.p.mons
    fs.switch_in(b, b.p, 2)
    b.p.hazards["rocks"] = 1
    out = {}
    for i, mon in ((0, guard), (1, plain)):
        b.dice, b.rng = pl.RunDice(random.Random(1), True), random.Random(1)
        fs.switch_in(b, b.p, i)
        entered = mon.maxhp - mon.hp
        cherrim.hp = cherrim.maxhp // 2
        pl.use_move(b, cherrim, fs.move("Leech Seed"), mon, True)
        before, healer = mon.hp, cherrim.hp
        fs.end_of_turn(b)
        out[mon.ability] = (entered, before - mon.hp, cherrim.hp - healer, mon.maxhp)
    ok = out["Magic Guard"][:3] == (0, 0, 0) and out["Cute Charm"][0] > 0 and out["Cute Charm"][1] == out["Cute Charm"][3] // 8
    return [("Magic Guard: a Clefable takes no Stealth Rock and no Leech Seed on the real rows", ok,
             f"(HP lost coming in, HP lost to the seed, Cherrim's heal, maximum HP) {out}")]


def liquid_ooze_checks():
    """Liquid Ooze on the calculator's real rows in the readings' battle
    (approved 2026-10-14): the Tentacool in Roark's and Gardenia's boxes
    can carry it, and then Gardenia's Roserade loses to its Giga Drain what
    it would have healed, and her Cherrim to its Leech Seed, where a Clear
    Body Tentacool heals them both."""
    from .test_fightai import battle
    b = battle([("Roserade", 26, "Natural Cure", ["Giga Drain"]), ("Cherrim", 24, "Flower Gift", ["Leech Seed"])],
               [("Tentacool", 26, "Liquid Ooze", ["Bubble Beam"]), ("Tentacool", 26, "Clear Body", ["Bubble Beam"])])
    rose, cherrim = b.b.mons
    out = {}
    for i, cool in enumerate(b.p.mons):
        fs.switch_in(b, b.p, i)
        fs.switch_in(b, b.b, 0)
        b.dice, b.rng = pl.RunDice(random.Random(1), True), random.Random(1)
        rose.hp, cool.hp = rose.maxhp // 2, cool.maxhp
        pl.use_move(b, rose, fs.move("Giga Drain"), cool, True)
        drained = (cool.maxhp - cool.hp, rose.hp - rose.maxhp // 2)
        fs.switch_in(b, b.b, 1)
        cherrim.hp = cherrim.maxhp // 2
        pl.use_move(b, cherrim, fs.move("Leech Seed"), cool, True)
        fs.end_of_turn(b)
        out[cool.ability] = drained + (cherrim.hp - cherrim.maxhp // 2,)
    ooze, plain = out["Liquid Ooze"], out["Clear Body"]
    ok = ooze[1] == -(ooze[0] // 2) and ooze[2] < 0 and plain[1] == plain[0] // 2 and plain[2] > 0
    return [("Liquid Ooze: Roserade's Giga Drain and Cherrim's Leech Seed hurt them on the real rows", ok,
             f"(Giga Drain's damage, Roserade's HP change, Cherrim's HP change at the turn's end) {out}")]


def drop_answer_checks():
    """The answers to Intimidate on the calculator's real rows (approved
    2026-10-14): a player's Intimidate Staravia leading against Mars 2's
    kind of Defiant Primeape leaves it at +1 Attack, so its Close Combat on
    the Staravia hits half again as hard as at no stage; against a Mirror
    Armor Corviknight it is Staravia's own Attack that falls."""
    from .test_fightai import battle
    out = {}
    for foe in (("Primeape", 30, "Defiant", ["Close Combat"]), ("Corviknight", 30, "Mirror Armor", ["Brave Bird"])):
        b = battle([foe], [("Staravia", 30, "Intimidate", ["Wing Attack"])])
        u, t = b.b.cur(), b.p.cur()
        mv = u.moves[0]
        now = pl.damage_of(b, u, t, mv, False, True)
        stages = (u.stages["atk"], t.stages["atk"])
        u.stages["atk"] = 0
        out[u.ability] = stages + (now, pl.damage_of(b, u, t, mv, False, True))
    ok = (out["Defiant"][:2] == (1, 0) and out["Mirror Armor"][:2] == (0, -1)
          and abs(out["Defiant"][2] - out["Defiant"][3] * 1.5) <= 2)
    return [("Defiant and Mirror Armor answer a lead's Intimidate on the real rows", ok,
             f"(the foe's Attack stage, Staravia's, the foe's top hit now, at no stage) {out}")]


def technician_power_checks():
    """Technician on the calculator's real rows (approved 2026-10-14): the
    calculator rows a Technician Breloom's Reversal at full HP's 20 power
    with Technician's half, half again a Poison Heal Breloom's; near 1 HP
    Reversal hits at 200 power, past Technician's reach, so the two now hit
    alike in the readings' damage, where the Technician one hit half again
    as hard. Pursuit into a switching target doubles to 80 the same way."""
    from .test_fightai import battle
    b = battle([("Breloom", 30, "Technician", ["Reversal", "Pursuit"]), ("Breloom", 30, "Poison Heal", ["Reversal", "Pursuit"])],
               [("Snorlax", 30, "Thick Fat", ["Body Slam"])])
    tech, plain = b.b.mons
    lax = b.p.cur()
    rev, pur = fs.move("Reversal"), fs.move("Pursuit")
    full = (pl.damage_of(b, tech, lax, rev, False, True), pl.damage_of(b, plain, lax, rev, False, True))
    tech.hp = plain.hp = 1
    low = (pl.damage_of(b, tech, lax, rev, False, True), pl.damage_of(b, plain, lax, rev, False, True))
    pursuit = []
    for mon in (tech, plain):
        b.dice, b.rng = pl.RunDice(random.Random(1), True), random.Random(1)
        mon.pursuing = True
        lax.hp = lax.maxhp
        pl.attack(b, mon, pur, lax, True)
        mon.pursuing = False
        pursuit.append(lax.maxhp - lax.hp)
    ok = (abs(full[0] - full[1] * 1.5) <= 2 and abs(low[0] - low[1]) <= 2
          and abs(pursuit[0] - pursuit[1]) <= 2 and pursuit[1] > 0)
    return [("Technician comes off Reversal near 1 HP and off a doubled Pursuit on the real rows", ok,
             f"Reversal (Technician, Poison Heal) at full HP {full}, at 1 HP {low}; Pursuit into a switch {pursuit}")]


def stored_power_checks():
    """Stored Power on the calculator's real rows (approved 2026-10-14): an
    Espeon's at +2 Sp. Atk and +1 Speed has 80 power, four times its row's
    20, and the +2 Sp. Atk doubles it again, so it hits eight times as hard
    as at no stage in the readings' damage, where it hit twice as hard."""
    from .test_fightai import battle
    b = battle([("Espeon", 40, "Synchronize", ["Stored Power"])], [("Snorlax", 40, "Thick Fat", ["Body Slam"])])
    esp, lax = b.b.cur(), b.p.cur()
    sp = fs.move("Stored Power")
    plain = pl.damage_of(b, esp, lax, sp, False, True)
    esp.stages["spa"], esp.stages["spe"] = 2, 1
    boosted = pl.damage_of(b, esp, lax, sp, False, True)
    ok = abs(boosted - plain * 8) <= 8
    return [("Stored Power at +2 Sp. Atk and +1 Speed hits eight times as hard on the real rows", ok,
             f"Espeon's top roll at no stage {plain}, at +2 Sp. Atk and +1 Speed {boosted}")]


def hard_press_checks():
    """Hard Press on the calculator's real rows (approved 2026-10-14): a
    Magnezone's into a Snorlax at a quarter of its HP has 25 power, a
    quarter of its full-HP row's 100, in the readings' damage, where it hit
    as at full HP."""
    from .test_fightai import battle
    b = battle([("Magnezone", 40, "Sturdy", ["Hard Press"])], [("Snorlax", 40, "Thick Fat", ["Body Slam"])])
    mag, lax = b.b.cur(), b.p.cur()
    hp = fs.move("Hard Press")
    full = pl.damage_of(b, mag, lax, hp, False, True)
    lax.hp = lax.maxhp // 4
    quarter = pl.damage_of(b, mag, lax, hp, False, True)
    ok = abs(quarter - full / 4) <= 2
    return [("Hard Press into a target at a quarter of its HP has a quarter the power on the real rows", ok,
             f"Magnezone's top roll at full HP {full}, at a quarter {quarter}")]


def electro_ball_checks():
    """Electro Ball on the calculator's real rows (approved 2026-10-14): a
    Jolteon's into a Snorlax, Speeds 121 against 41 at the start, has 80
    power; once the Jolteon is at +2 Speed and the Snorlax paralysed it has
    150, so it hits 15/8 as hard in the readings' damage, where it kept the
    opening 80."""
    from .test_fightai import battle
    b = battle([("Jolteon", 40, "Volt Absorb", ["Electro Ball"])], [("Snorlax", 40, "Thick Fat", ["Body Slam"])])
    jol, lax = b.b.cur(), b.p.cur()
    eb = fs.move("Electro Ball")
    opening = pl.damage_of(b, jol, lax, eb, False, True)
    lax.status, jol.stages["spe"] = "par", 2
    later = pl.damage_of(b, jol, lax, eb, False, True)
    ok = abs(later - opening * 150 / 80) <= 2
    return [("Electro Ball's power follows the Speeds as they stand on the real rows", ok,
             f"Jolteon's top roll at the opening Speeds {opening}, at +2 Speed on a paralysed Snorlax {later}")]


def sacred_sword_checks():
    """Sacred Sword on the calculator's real rows in the readings' damage
    (approved 2026-10-14): a Gallade's against a Snorlax at +2 Defense and
    at -2 hits as at no stage, where it hit half and twice as hard; its
    Close Combat still meets the stages."""
    from .test_fightai import battle
    b = battle([("Gallade", 40, "Justified", ["Sacred Sword", "Close Combat"])], [("Snorlax", 40, "Thick Fat", ["Body Slam"])])
    gal, lax = b.b.cur(), b.p.cur()
    ss, cc = fs.move("Sacred Sword"), fs.move("Close Combat")
    out = {}
    for st in (0, 2, -2):
        lax.stages["def"] = st
        out[st] = (pl.damage_of(b, gal, lax, ss, False, True), pl.damage_of(b, gal, lax, cc, False, True))
    ok = out[2][0] == out[0][0] == out[-2][0] and out[2][1] < out[0][1] < out[-2][1]
    return [("Sacred Sword ignores the target's Defense stages on the real rows", ok,
             f"(Sacred Sword, Close Combat) at the target's Defense stage 0, +2, -2: {out}")]


def mold_breaker_checks():
    """Mold Breaker on the calculator's real rows in the readings' battle
    (approved 2026-10-14): Roark's Mold Breaker Cranidos's Rock Slide now
    flinches an Inner Focus Zubat, which every one of his boxes holds, and
    can land a critical hit on a Shell Armor Turtwig (box 1's six takes
    one); a Rock Head Cranidos does neither."""
    from .test_fightai import battle
    out = {}
    for ab in ("Mold Breaker", "Rock Head"):
        b = battle([("Cranidos", 16, ab, ["Rock Slide"])],
                   [("Zubat", 16, "Inner Focus", ["Bite"]), ("Turtwig", 16, "Shell Armor", ["Tackle"])])
        cran = b.b.cur()
        zubat, turtwig = b.p.mons
        flinched = 0
        for seed in range(200):
            b.dice, b.rng = pl.RunDice(random.Random(seed), True), random.Random(seed)
            zubat.hp, zubat.flinch = zubat.maxhp * 10, False     # it outlasts the hit, so a flinch can show
            pl.attack(b, cran, fs.move("Rock Slide"), zubat, True)
            flinched += zubat.flinch
        out[ab] = (flinched, fs.crit_rate(b, cran, turtwig, fs.move("Rock Slide")) > 0)
    ok = out["Mold Breaker"][0] > 30 and out["Mold Breaker"][1] and out["Rock Head"] == (0, False)
    return [("Mold Breaker: Cranidos flinches an Inner Focus Zubat and crits a Shell Armor Turtwig", ok,
             f"(flinches in 200 Rock Slides, can land a critical hit on Turtwig) {out}")]


def oblivious_taunt_checks():
    """Oblivious against Taunt in the readings' battle (approved 2026-10-14):
    a trainer's Taunt fails on the player's Oblivious Slowpoke and lands on
    an Own Tempo one."""
    from .test_fightai import battle
    b = battle([("Murkrow", 20, "Insomnia", ["Taunt"])],
               [("Slowpoke", 20, "Oblivious", ["Water Pulse"]), ("Slowpoke", 20, "Own Tempo", ["Water Pulse"])])
    crow = b.b.cur()
    out = {}
    for i, poke in enumerate(b.p.mons):
        fs.switch_in(b, b.p, i)
        b.dice, b.rng = pl.RunDice(random.Random(1), True), random.Random(1)
        pl.use_move(b, crow, fs.move("Taunt"), poke, True)
        out[poke.ability] = poke.taunt
    ok = out["Oblivious"] == 0 and out["Own Tempo"] >= 3
    return [("Oblivious keeps a trainer's Taunt off a Slowpoke in the readings' battle", ok, f"Taunt's turns {out}")]


def cursed_body_checks():
    """Cursed Body in the readings' battle (approved 2026-10-14): Fantina's
    and Candice's Cursed Body holders disable the player's move about three
    times in ten; here a Jellicent's against a Pikachu's Thunderbolt over 300
    hits, through the battle's dice."""
    from .test_fightai import battle
    b = battle([("Jellicent", 30, "Cursed Body", ["Hex"])], [("Pikachu", 30, "Static", ["Thunderbolt", "Quick Attack"])])
    jelly, pika = b.b.cur(), b.p.cur()
    bolt = fs.move("Thunderbolt")
    disabled = 0
    for seed in range(300):
        b.dice, b.rng = pl.RunDice(random.Random(seed), True), random.Random(seed)
        jelly.hp, pika.disabled, pika.disabled_turns = jelly.maxhp, None, 0
        pika.pp["Thunderbolt"] = 10
        pl.use_move(b, pika, bolt, jelly, True)
        disabled += pika.disabled == "Thunderbolt"
    ok = 60 <= disabled <= 120
    return [("Cursed Body disables the player's move about three times in ten", ok, f"disabled in {disabled} of 300 hits")]


def justified_checks():
    """Justified in the readings' battle (approved 2026-10-14): Lucian's
    Justified Gallade gains a stage of Attack from a player's Bite, and its
    Close Combat then hits half again as hard; a Steadfast one gains none."""
    from .test_fightai import battle
    out = {}
    for ab in ("Justified", "Steadfast"):
        b = battle([("Gallade", 40, ab, ["Close Combat"])], [("Houndour", 40, "Flash Fire", ["Bite"])])
        gal, dog = b.b.cur(), b.p.cur()
        b.dice, b.rng = pl.RunDice(random.Random(1), True), random.Random(1)
        before = pl.damage_of(b, gal, dog, fs.move("Close Combat"), False, True)
        pl.use_move(b, dog, fs.move("Bite"), gal, True)
        out[ab] = (gal.stages["atk"], before, pl.damage_of(b, gal, dog, fs.move("Close Combat"), False, True))
    ok = out["Justified"][0] == 1 and out["Steadfast"][0] == 0 and abs(out["Justified"][2] - out["Justified"][1] * 1.5) <= 2
    return [("Justified: a Bite raises Gallade's Attack in the readings' battle", ok,
             f"(Attack stage, Close Combat's top roll before, after) {out}")]


def moxie_checks():
    """Moxie in the readings' battle (approved 2026-10-14): Cyrus 1's kind of
    Moxie Honchkrow knocks out a weakened Pikachu with Brave Bird and rises
    a stage of Attack; an Insomnia one does not."""
    from .test_fightai import battle
    out = {}
    for ab in ("Moxie", "Insomnia"):
        b = battle([("Honchkrow", 40, ab, ["Brave Bird"])], [("Pikachu", 40, "Static", ["Thunderbolt"])])
        crow, pika = b.b.cur(), b.p.cur()
        b.dice, b.rng = pl.RunDice(random.Random(1), True), random.Random(1)
        pika.hp = 1
        pl.use_move(b, crow, fs.move("Brave Bird"), pika, True)
        out[ab] = (pika.alive(), crow.stages["atk"])
    ok = out["Moxie"] == (False, 1) and out["Insomnia"] == (False, 0)
    return [("Moxie: Honchkrow rises on a knockout in the readings' battle", ok, f"(Pikachu standing, Attack stage) {out}")]


def trapping_checks():
    """Shadow Tag in the readings' choices (approved 2026-10-14): against
    Saturn's kind of Shadow Tag Gothitelle the player's Machop may not
    switch, while a Ghost Gastly and a Machop holding a Shed Shell are each
    offered their switches."""
    from .test_fightai import battle
    out = {}
    for label, lead, item in (("Machop", ("Machop", 40, "Guts", ["Karate Chop"]), None),
                              ("Gastly", ("Gastly", 40, "Levitate", ["Lick"]), None),
                              ("Machop, a Shed Shell", ("Machop", 40, "Guts", ["Karate Chop"]), "Shed Shell")):
        b = battle([("Gothitelle", 40, "Shadow Tag", ["Psychic"])], [lead, ("Snorlax", 40, "Thick Fat", ["Body Slam"])])
        b.p.cur().item = item
        out[label] = any(a[0] == "switch" for a in pl.player_actions(b))
    ok = out == {"Machop": False, "Gastly": True, "Machop, a Shed Shell": True}
    return [("Shadow Tag holds a Machop but not a Ghost or a Shed Shell holder in the readings' choices", ok,
             f"switches offered {out}")]


def accuracy_ability_checks():
    """No Guard and Keen Eye in the readings' accuracy (approved 2026-10-14):
    Maylene's rematch's kind of No Guard Machamp lands every Dynamic Punch,
    and the player's No Guard Machop every one into a Guts Machamp; a Keen
    Eye Starly's Tackle ignores a +6 evasion that leaves a Reckless one at
    about a third, over 300 uses each."""
    from .test_fightai import battle
    b = battle([("Machamp", 40, "No Guard", ["Dynamic Punch"]), ("Machamp", 40, "Guts", ["Dynamic Punch"])],
               [("Machop", 40, "No Guard", ["Dynamic Punch"]), ("Starly", 40, "Keen Eye", ["Tackle"]),
                ("Starly", 40, "Reckless", ["Tackle"])])
    guard, guts = b.b.mons
    chop, keen, reckless = b.p.mons
    dp, tackle = fs.move("Dynamic Punch"), fs.move("Tackle")

    def lands(att, dfn, mv, eva=0):
        dfn.stages["eva"] = eva
        n = 0
        for seed in range(300):
            b.dice = pl.RunDice(random.Random(seed), True)
            n += pl.accuracy_hits(b, att, dfn, mv)
        dfn.stages["eva"] = 0
        return n
    got = {"No Guard Machamp's Dynamic Punch": lands(guard, chop, dp),
           "No Guard Machop's Dynamic Punch": lands(chop, guts, dp),
           "Keen Eye Tackle into +6": lands(keen, guts, tackle, eva=6),
           "Reckless Tackle into +6": lands(reckless, guts, tackle, eva=6)}
    ok = (got["No Guard Machamp's Dynamic Punch"] == got["No Guard Machop's Dynamic Punch"] == 300
          and got["Keen Eye Tackle into +6"] == 300 and got["Reckless Tackle into +6"] < 150)
    return [("No Guard and Keen Eye in the readings' accuracy", ok, f"landed of 300 {got}")]


def download_checks():
    """Download on the calculator's real rows (approved 2026-10-14): the
    Cynthia rematch's kind of Download Porygon-Z, leading against a
    Geodude (Defense far above its Sp. Def), comes in at +1 Sp. Atk, a real
    stage, and its rows now read as a Pressure twin's at no stage, where
    they carried the boost themselves and no stage showed."""
    from .test_fightai import battle
    out = {}
    for ab in ("Download", "Pressure"):
        b = battle([("Porygon-Z", 40, ab, ["Tri Attack"])], [("Geodude", 40, "Sturdy", ["Tackle"])])
        pz, geo = b.b.cur(), b.p.cur()
        stage = pz.stages["spa"]
        pz.stages["spa"] = 0
        out[ab] = (stage, pl.damage_of(b, pz, geo, fs.move("Tri Attack"), False, True))
    ok = out["Download"][0] == 1 and out["Pressure"][0] == 0 and out["Download"][1] == out["Pressure"][1]
    return [("Download: Porygon-Z leads at +1 Sp. Atk against a Geodude, its rows without the boost", ok,
             f"(Sp. Atk stage on entry, Tri Attack's top roll at no stage) {out}")]


def weather_ability_checks():
    """The weather's turn-end abilities on the real rows' battle (approved
    2026-10-14): in a fight held in rain, a Rain Dish Lombre (in Roark's and
    Gardenia's boxes) gets a sixteenth back at the turn's end and a
    paralysed Hydration Vaporeon is cured; in a sandstorm a Sand Force
    Shellos, a Water type the sand would bite, takes no damage. (Every Sand
    Rush holder in Oxide is a Ground type, which the sand spares anyway.)"""
    from .test_fightai import battle
    b = battle([("Geodude", 20, "Sturdy", ["Tackle"])],
               [("Lombre", 20, "Rain Dish", ["Water Gun"]), ("Vaporeon", 20, "Hydration", ["Water Gun"])], weather="Rain")
    lombre, vap = b.p.mons
    lombre.hp = lombre.maxhp // 2
    before = lombre.hp
    fs.end_of_turn(b)
    healed = lombre.hp - before
    fs.switch_in(b, b.p, 1)
    vap.status = "par"
    fs.end_of_turn(b)
    cured = vap.status is None
    s = battle([("Shellos", 20, "Sand Force", ["Mud-Slap"])], [("Geodude", 20, "Sturdy", ["Tackle"])], weather="Sand")
    shellos = s.b.cur()
    fs.end_of_turn(s)
    spared = shellos.hp == shellos.maxhp
    ok = b.weather == "Rain" and healed == lombre.maxhp // 16 and cured and s.weather == "Sand" and spared
    return [("Rain Dish heals, Hydration cures, Sand Force is spared the sand on the real rows", ok,
             f"Lombre healed {healed} of {lombre.maxhp}; Vaporeon cured {cured}; Shellos at full HP after the sand {spared}")]


def sand_force_checks():
    """Sand Force on the calculator's real rows (approved 2026-10-14): in a
    sandstorm a Sand Force Probopass's Power Gem hits 13/10 as hard as a
    Sturdy one's in the readings' damage, where the two read alike."""
    from .test_fightai import battle
    b = battle([("Probopass", 40, "Sand Force", ["Power Gem"]), ("Probopass", 40, "Sturdy", ["Power Gem"])],
               [("Pikachu", 40, "Static", ["Thunderbolt"])], weather="Sand")
    force, sturdy = b.b.mons
    pika = b.p.cur()
    gem = fs.move("Power Gem")
    got = (pl.damage_of(b, force, pika, gem, False, True), pl.damage_of(b, sturdy, pika, gem, False, True))
    ok = b.weather == "Sand" and abs(got[0] - got[1] * 1.3) <= 2
    return [("Sand Force: Power Gem at 13/10 in sand on the real rows", ok, f"(Sand Force, Sturdy) top rolls {got}")]


def bad_dreams_checks():
    """Bad Dreams in the readings' battle (approved 2026-10-14): Somnu's
    Mt. Coronet Darkrai's Dark Void puts a Machop to sleep, and at the
    turn's end it loses an eighth of its HP."""
    from .test_fightai import battle
    b = battle([("Darkrai", 40, "Bad Dreams", ["Dark Void"])], [("Machop", 40, "Guts", ["Karate Chop"])])
    dark, chop = b.b.cur(), b.p.cur()
    b.dice, b.rng = pl.RunDice(random.Random(1), True), random.Random(1)
    chop.status, chop.sleep = "slp", 3
    before = chop.hp
    fs.end_of_turn(b)
    lost = before - chop.hp
    ok = lost == chop.maxhp // 8 and dark.revealed == "Bad Dreams"
    return [("Bad Dreams: a sleeping Machop loses an eighth at the turn's end", ok,
             f"lost {lost} of {chop.maxhp}; Darkrai's ability named {dark.revealed}")]


def marvel_scale_checks():
    """Marvel Scale on the calculator's real rows (approved 2026-10-14):
    Cynthia's Milotic, once burned or paralysed, takes two thirds of a
    Machamp's Cross Chop in the readings' damage, where it took it whole."""
    from .test_fightai import battle
    b = battle([("Milotic", 40, "Marvel Scale", ["Scald"])], [("Machamp", 40, "Guts", ["Cross Chop"])])
    milo, champ = b.b.cur(), b.p.cur()
    chop = fs.move("Cross Chop")
    plain = pl.damage_of(b, champ, milo, chop, False, True)
    milo.status = "par"
    scaled = pl.damage_of(b, champ, milo, chop, False, True)
    ok = abs(scaled - plain * 2 / 3) <= 2
    return [("Marvel Scale: a paralysed Milotic takes two thirds of a Cross Chop on the real rows", ok,
             f"Cross Chop's top roll with no status {plain}, paralysed {scaled}")]


def shed_skin_checks():
    """Shed Skin through the readings' dice (approved 2026-10-14): a
    trainer's Shed Skin Gabite, burned, is cured about one turn end in three
    on a run's real odds, and the planner's dice offer the cure as an event
    at those odds."""
    from .test_fightai import battle
    from . import plplan
    b = battle([("Gabite", 30, "Shed Skin", ["Dragon Claw"])], [("Machop", 30, "Guts", ["Karate Chop"])])
    gab = b.b.cur()
    cured = 0
    for seed in range(300):
        b.dice, b.rng = pl.RunDice(random.Random(seed), True), random.Random(seed)
        gab.status, gab.hp = "brn", gab.maxhp
        fs.end_of_turn(b)
        cured += gab.status is None
    gab.status = "brn"
    d = plplan.EnumDice((), random.Random(0))
    b.dice = d
    fs.end_of_turn(b)
    offered = any(abs(probs[1] - 1 / 3) < 1e-9 for probs in d.events if len(probs) == 2)
    ok = 70 <= cured <= 130 and offered
    return [("Shed Skin cures about a third of the time on the readings' dice", ok,
             f"cured {cured} of 300; offered to the planner at a third {offered}")]


def suction_cups_checks():
    """Suction Cups in the readings' battle (approved 2026-10-14): the
    player's Roar leaves a trainer's Suction Cups Octillery in, and drags a
    Sniper one out for its partner."""
    from .test_fightai import battle
    out = {}
    for ab in ("Suction Cups", "Sniper"):
        b = battle([("Octillery", 30, ab, ["Octazooka"]), ("Geodude", 30, "Sturdy", ["Tackle"])],
                   [("Houndour", 30, "Flash Fire", ["Roar"])])
        b.dice, b.rng = pl.RunDice(random.Random(1), True), random.Random(1)
        pl.use_move(b, b.p.cur(), fs.move("Roar"), b.b.cur(), True)
        out[ab] = b.b.cur().species
    ok = out == {"Suction Cups": "Octillery", "Sniper": "Geodude"}
    return [("Suction Cups keeps Octillery in against the player's Roar", ok, f"the trainer's Pokemon after Roar {out}")]


def plus_minus_checks():
    """Plus on the calculator's real rows (approved 2026-10-14): prepare now
    rows a Plus Plusle without its boost, so in a single battle its
    Thunderbolt reads as a Lightning Rod Plusle's, where it read half again
    as hard."""
    from .test_fightai import battle
    b = battle([("Plusle", 30, "Plus", ["Thunderbolt"]), ("Plusle", 30, "Lightning Rod", ["Thunderbolt"])],
               [("Snorlax", 30, "Thick Fat", ["Body Slam"])])
    plus, rod = b.b.mons
    lax = b.p.cur()
    bolt = fs.move("Thunderbolt")
    got = (pl.damage_of(b, plus, lax, bolt, False, True), pl.damage_of(b, rod, lax, bolt, False, True))
    ok = got[0] == got[1]
    return [("Plus: a lone Plusle's Thunderbolt reads as a Lightning Rod one's on the real rows", ok,
             f"(Plus, Lightning Rod) top rolls {got}")]


def stench_checks():
    """Stench in the readings' battle (approved 2026-10-14): a Stench
    Weezing moving first flinches a Snorlax with Sludge Bomb about one time
    in ten over 400 hits, a Levitate one never."""
    from .test_fightai import battle
    out = {}
    for ab in ("Stench", "Levitate"):
        b = battle([("Weezing", 40, ab, ["Sludge Bomb"])], [("Snorlax", 40, "Thick Fat", ["Body Slam"])])
        wee, lax = b.b.cur(), b.p.cur()
        n = 0
        for seed in range(400):
            b.dice, b.rng = pl.RunDice(random.Random(seed), True), random.Random(seed)
            lax.hp, lax.flinch, lax.status = lax.maxhp, False, None
            pl.attack(b, wee, fs.move("Sludge Bomb"), lax, True)
            n += lax.flinch
        out[ab] = n
    ok = 20 <= out["Stench"] <= 65 and out["Levitate"] == 0
    return [("Stench: Weezing's Sludge Bomb flinches about one time in ten", ok, f"flinched of 400 {out}")]


def unnerve_checks():
    """Unnerve on the calculator's real rows (approved 2026-10-14): the
    player's Sitrus Berry, which the scorer hands out, does not fire under
    a trainer's Unnerve Tyranitar, and the player's Unnerve Corvisquire (in
    Roark's and Gardenia's boxes) keeps Roark's kind of Passho Berry
    Sandshrew from halving its Water hit, so a Water Gun lands at the row's
    whole worth."""
    from .test_fightai import battle
    b = battle([("Tyranitar", 40, "Unnerve", ["Crunch"])], [("Machamp", 40, "Guts", ["Cross Chop"], "Sitrus Berry")])
    champ = b.p.cur()
    b.dice, b.rng = pl.RunDice(random.Random(1), True), random.Random(1)
    fs.hurt(b, champ, champ.hp - champ.maxhp // 2 + 1)
    kept = champ.item == "Sitrus Berry" and champ.hp < champ.maxhp // 2
    c = battle([("Sandshrew", 16, "Sand Veil", ["Rock Slide"], "Passho Berry")],
               [("Corvisquire", 16, "Unnerve", ["Water Gun"]), ("Corvisquire", 16, "Keen Eye", ["Water Gun"])])
    shrew = c.b.cur()
    unnerve, keen = c.p.mons
    gun = fs.move("Water Gun")
    # Unnerve works while its holder is on the field, whoever attacks, so
    # each Corvisquire is read with itself sent in.
    c.p.active = 1
    halved = pl.damage_of(c, keen, shrew, gun, False, False)
    c.p.active = 0
    whole = pl.damage_of(c, unnerve, shrew, gun, False, False)
    ok = kept and abs(whole - halved * 2) <= 2
    return [("Unnerve keeps a Sitrus Berry uneaten and a Passho Berry from halving, on the real rows", ok,
             f"Machamp kept its Sitrus Berry below half HP {kept}; Water Gun's bottom roll into the Passho "
             f"Sandshrew from a Keen Eye Corvisquire {halved}, from an Unnerve one {whole}")]


def steadfast_checks():
    """Steadfast in the readings' battle (approved 2026-10-14): the player's
    Steadfast Dubwool (box 3 of Gardenia's reading takes one) flinched by a
    Fake Out rises a stage of Speed; a Fluffy one does not."""
    from .test_fightai import battle
    out = {}
    for ab in ("Steadfast", "Fluffy"):
        b = battle([("Ambipom", 30, "Technician", ["Fake Out"])], [("Dubwool", 30, ab, ["Double Kick"])])
        pom, wool = b.b.cur(), b.p.cur()
        b.dice, b.rng = pl.RunDice(random.Random(1), True), random.Random(1)
        pl.use_move(b, pom, fs.move("Fake Out"), wool, True)
        flinched = wool.flinch
        pl.use_move(b, wool, fs.move("Double Kick"), pom, False)
        out[ab] = (flinched, wool.stages["spe"])
    ok = out == {"Steadfast": (True, 1), "Fluffy": (True, 0)}
    return [("Steadfast: a flinched Dubwool rises a stage of Speed in the readings' battle", ok,
             f"(flinched, Speed stage) {out}")]


def starf_berry_checks():
    """The Starf Berry through the readings' dice (approved 2026-10-14):
    Hesperid's kind of Starf Berry holder, hit to a quarter of its HP, eats
    it and raises one stat two stages, and the planner's dice offer the
    five stats as one event at even odds."""
    from .test_fightai import battle
    from . import plplan
    b = battle([("Slaking", 40, "Truant", ["Giga Impact"], "Starf Berry")], [("Machamp", 40, "Guts", ["Cross Chop"])])
    lax = b.b.cur()
    b.dice, b.rng = pl.RunDice(random.Random(1), True), random.Random(1)
    fs.hurt(b, lax, lax.hp - lax.maxhp // 4)
    rose = {k: v for k, v in lax.stages.items() if v}
    lax.item, lax.stages = "Starf Berry", dict.fromkeys(fs.STAGE_KEYS, 0)
    lax.hp = lax.maxhp
    d = plplan.EnumDice((), random.Random(0))
    b.dice = d
    fs.hurt(b, lax, lax.hp - lax.maxhp // 4)
    offered = any(len(probs) == 5 and all(abs(q - 0.2) < 1e-9 for q in probs) for probs in d.events)
    ok = len(rose) == 1 and list(rose.values()) == [2] and offered
    return [("the Starf Berry fires at a quarter HP on the readings' dice", ok,
             f"raised {rose}; offered to the planner as five even outcomes {offered}")]


def sticky_barb_checks():
    """The Sticky Barb in the readings' battle (approved 2026-10-14): a
    trainer's barb passes to the player's empty-handed Machop on its Karate
    Chop, and at the turn's end it is the Machop that loses an eighth."""
    from .test_fightai import battle
    b = battle([("Ferrothorn", 30, "Iron Barbs", ["Leech Seed"], "Sticky Barb")], [("Machop", 30, "Guts", ["Karate Chop"])])
    ferro, chop = b.b.cur(), b.p.cur()
    b.dice, b.rng = pl.RunDice(random.Random(1), True), random.Random(1)
    pl.use_move(b, chop, fs.move("Karate Chop"), ferro, True)
    moved = (chop.item, ferro.item)
    before = chop.hp
    fs.end_of_turn(b)
    lost = before - chop.hp
    ok = moved == ("Sticky Barb", None) and lost == chop.maxhp // 8
    return [("the Sticky Barb passes to a contact attacker and hurts it at the turn's end", ok,
             f"(Machop's item, Ferrothorn's) {moved}; Machop lost {lost} of {chop.maxhp} at the turn's end")]


def rivalry_checks():
    """Rivalry on the calculator's real rows (approved 2026-10-14): prepare
    gives the calculator each Pokemon's gender, so a male Rivalry Luxray's
    Spark hits a male Bibarel a quarter harder and a female one a quarter
    softer (5/3 between them), where both read the same quarter harder; a
    Pressure Luxray hits the two alike."""
    def rec(sp, lv, ab, mv, gender):
        return {"species": sp, "level": lv, "ability": ab, "item": None, "nature": "Hardy", "ivs": IV, "evs": EV,
                "moves": mv, "gender": gender}
    bosses = [rec("Luxray", 30, "Rivalry", ["Spark"], "male"), rec("Luxray", 30, "Pressure", ["Spark"], "male")]
    side = [dict(rec("Bibarel", 30, "Simple", ["Tackle"], g), constant="SPECIES_BIBAREL", how="test", fill=False)
            for g in ("male", "female")]
    st = fs.prepare("Roark", [bosses], None, given_side=side)
    b = pl.make_battle(st, ["p0", "p1"], st["bosses"][0], 7, 0)
    rival, plain = b.b.mons
    male, female = b.p.mons
    spark = fs.move("Spark")
    got = {lux.ability: (pl.damage_of(b, lux, male, spark, False, True), pl.damage_of(b, lux, female, spark, False, True))
           for lux in (rival, plain)}
    r = got["Rivalry"]
    ok = (male.gender, female.gender) == ("M", "F") and abs(r[0] / r[1] - 5 / 3) < 0.08 and got["Pressure"][0] == got["Pressure"][1]
    return [("Rivalry reads the two Pokemon's genders on the real rows", ok,
             f"Spark's top roll into the male and the female Bibarel {got}")]


def payback_checks():
    """Payback on the calculator's real rows (approved 2026-10-14): a slow
    Machamp's Payback into a faster Jolteon, which the calculator rows at
    twice its power, reads at its table power, as its Bite of the same 60
    does (to the calculator's rounding), and doubles once when it moves
    second; it read at twice the Bite, and four times once doubled."""
    from .test_fightai import battle
    b = battle([("Jolteon", 40, "Volt Absorb", ["Thunderbolt"])], [("Machamp", 40, "Guts", ["Payback", "Bite"])])
    jolt, champ = b.b.cur(), b.p.cur()
    pay, bite = fs.move("Payback"), fs.move("Bite")
    rows = (pl.damage_of(b, champ, jolt, pay, False, True), pl.damage_of(b, champ, jolt, bite, False, True))
    second = []
    for first in (True, False):
        b.dice, b.rng = pl.RunDice(random.Random(1), True), random.Random(1)
        jolt.hp = jolt.maxhp
        b.st["first_battle"] = True
        pl.attack(b, champ, pay, jolt, first)
        second.append(jolt.maxhp - jolt.hp)
    b.st["first_battle"] = False
    slower = b.row_speed(champ) <= b.row_speed(jolt)
    # The halved row and a row made at 60 differ only by the calculator's
    # rounding, a point or two.
    ok = slower and abs(rows[0] - rows[1]) <= 2 and abs(second[1] - 2 * second[0]) <= 2
    return [("Payback reads at its table power on the real rows and doubles once", ok,
             f"slower in the rows {slower}; top rolls (Payback, Bite) {rows}; dealt moving first, second {second}")]


def leech_seed_sap_checks():
    """Leech Seed in the readings' battle (approved 2026-10-14): Gardenia's
    kind of Leech Seed Cherrim, at low HP, gets back only the 3 HP a
    seeded Machop had left; with the Cherrim fainted the seeded Machop
    loses nothing at the turn's end."""
    from .test_fightai import battle
    out = {}
    for case in ("low", "seeder down"):
        b = battle([("Cherrim", 24, "Flower Gift", ["Leech Seed"])], [("Machop", 24, "Guts", ["Karate Chop"])])
        cherrim, chop = b.b.cur(), b.p.cur()
        b.dice, b.rng = pl.RunDice(random.Random(1), True), random.Random(1)
        chop.seeded = True
        cherrim.hp = 10
        if case == "low":
            chop.hp = 3
        else:
            cherrim.hp = 0
        before = (chop.hp, cherrim.hp)
        fs.end_of_turn(b)
        out[case] = (before, (chop.hp, cherrim.hp))
    ok = out["low"][1] == (0, 13) and out["seeder down"][1] == out["seeder down"][0]
    return [("Leech Seed gives back what it saps and saps nothing with its seeder down, in the readings", ok,
             f"(Machop's HP, Cherrim's) before and after {out}")]


def ghost_untrapped_checks():
    """A Ghost type under Mean Look in the readings' choices (approved
    2026-10-14): a trainer's Gengar's Mean Look holds the player's Machop
    in, while a Haunter is still offered its switch."""
    from .test_fightai import battle
    out = {}
    for lead in (("Machop", 40, "Guts", ["Karate Chop"]), ("Haunter", 40, "Levitate", ["Lick"])):
        b = battle([("Gengar", 40, "Cursed Body", ["Mean Look"])], [lead, ("Snorlax", 40, "Thick Fat", ["Body Slam"])])
        b.dice, b.rng = pl.RunDice(random.Random(1), True), random.Random(1)
        pl.use_move(b, b.b.cur(), fs.move("Mean Look"), b.p.cur(), True)
        out[lead[0]] = (b.p.cur().trapped_by is not None, any(a[0] == "switch" for a in pl.player_actions(b)))
    ok = out == {"Machop": (True, False), "Haunter": (True, True)}
    return [("a Ghost type under Mean Look is still offered its switch in the readings", ok,
             f"(Mean Look landed, a switch offered) {out}")]


def soundproof_status_checks():
    """Soundproof in the readings' battle (approved 2026-10-14): a trainer's
    Sing never sleeps the player's Soundproof Snover over 200 uses, while a
    Snow Warning one sleeps about as often as Sing lands."""
    from .test_fightai import battle
    out = {}
    for ab in ("Soundproof", "Snow Warning"):
        slept = 0
        for seed in range(200):
            b = battle([("Jigglypuff", 30, "Cute Charm", ["Sing"])], [("Snover", 30, ab, ["Powder Snow"])])
            b.dice, b.rng = pl.RunDice(random.Random(seed), True), random.Random(seed)
            pl.use_move(b, b.b.cur(), fs.move("Sing"), b.p.cur(), True)
            slept += b.p.cur().status == "slp"
        out[ab] = slept
    ok = out["Soundproof"] == 0 and 70 <= out["Snow Warning"] <= 150
    return [("Soundproof stops Sing in the readings", ok, f"slept of 200 {out}")]


def item_flinch_blocked_checks():
    """Shield Dust against a King's Rock in the readings' battle (approved
    2026-10-14): Cyrus's kind of King's Rock holder, moving first, never
    flinches the player's Shield Dust Dustox over 400 hits, and flinches a
    Compound Eyes one about one time in ten."""
    from .test_fightai import battle
    out = {}
    for ab in ("Shield Dust", "Compound Eyes"):
        b = battle([("Machamp", 40, "Guts", ["Cross Chop"], "King's Rock")], [("Dustox", 40, ab, ["Gust"])])
        champ, dust = b.b.cur(), b.p.cur()
        n = 0
        for seed in range(400):
            b.dice, b.rng = pl.RunDice(random.Random(seed), True), random.Random(seed)
            dust.hp, dust.flinch = dust.maxhp, False
            pl.attack(b, champ, fs.move("Cross Chop"), dust, True)
            n += bool(dust.flinch)
        out[ab] = n
    ok = out["Shield Dust"] == 0 and 20 <= out["Compound Eyes"] <= 65
    return [("Shield Dust stops a King's Rock's flinch in the readings", ok, f"flinched of 400 {out}")]


def black_sludge_checks():
    """Black Sludge in the readings' battle (approved 2026-10-14): on a
    trainer's Machamp it takes an eighth at the turn's end; on a Muk it gives
    a sixteenth back."""
    from .test_fightai import battle
    out = {}
    for sp, ab in (("Machamp", "Guts"), ("Muk", "Stench")):
        b = battle([(sp, 40, ab, ["Body Slam"], "Black Sludge")], [("Snorlax", 40, "Thick Fat", ["Body Slam"])])
        m = b.b.cur()
        b.dice, b.rng = pl.RunDice(random.Random(1), True), random.Random(1)
        m.hp = m.maxhp // 2
        before = m.hp
        fs.end_of_turn(b)
        out[sp] = (m.hp - before, m.maxhp)
    ok = out["Machamp"][0] == -(out["Machamp"][1] // 8) and out["Muk"][0] == out["Muk"][1] // 16
    return [("Black Sludge hurts a Machamp and heals a Muk in the readings", ok, f"(HP change, maximum HP) {out}")]


def water_bubble_checks():
    """Water Bubble in the readings' battle (approved 2026-10-14): a
    trainer's sure Will-O-Wisp never burns the player's Water Bubble
    Araquanid, and burns a Water Absorb one."""
    from .test_fightai import battle
    out = {}
    for ab in ("Water Bubble", "Water Absorb"):
        b = battle([("Ninetales", 30, "Flash Fire", ["Will-O-Wisp"])], [("Araquanid", 30, ab, ["Bubble Beam"])])
        b.dice, b.rng = pl.RunDice(random.Random(1), True), random.Random(1)
        b.b.cur().stages["acc"] = 6
        pl.use_move(b, b.b.cur(), fs.move("Will-O-Wisp"), b.p.cur(), True)
        out[ab] = b.p.cur().status
    ok = out == {"Water Bubble": None, "Water Absorb": "brn"}
    return [("Water Bubble keeps a Will-O-Wisp's burn off in the readings", ok, f"status after Will-O-Wisp {out}")]


def eerie_spell_checks():
    """Eerie Spell in the readings' battle (Oxide's engine since 2026-10-14):
    the player's Eerie Spell takes 3 PP from the Thunderbolt a trainer's
    Jolteon has just used, and none after the Jolteon has switched in."""
    from .test_fightai import battle
    out = {}
    for case in ("after its Thunderbolt", "just in"):
        b = battle([("Jolteon", 40, "Volt Absorb", ["Thunderbolt"])], [("Slowking", 40, "Oblivious", ["Eerie Spell"])])
        jolt, king = b.b.cur(), b.p.cur()
        b.dice, b.rng = pl.RunDice(random.Random(1), True), random.Random(1)
        if case == "after its Thunderbolt":
            pl.use_move(b, jolt, fs.move("Thunderbolt"), king, True)
        before = jolt.pp["Thunderbolt"]
        b.st["first_battle"] = True
        pl.use_move(b, king, fs.move("Eerie Spell"), jolt, False)
        b.st["first_battle"] = False
        out[case] = (before, jolt.pp["Thunderbolt"])
    ok = out["after its Thunderbolt"][0] - out["after its Thunderbolt"][1] == 3 and out["just in"][0] == out["just in"][1]
    return [("Eerie Spell drains the last move's PP in the readings", ok, f"Thunderbolt's PP before and after {out}")]


def burning_bulwark_checks():
    """Burning Bulwark in the readings' battle (Oxide's engine since
    2026-10-14): a trainer's Burning Bulwark, used first in the turn, stops
    the player's Karate Chop and burns the Machop; a Water Veil attacker is
    stopped and not burned."""
    from .test_fightai import battle
    out = {}
    for ab in ("Guts", "Water Veil"):
        b = battle([("Scovillain", 40, "Chlorophyll", ["Burning Bulwark"])], [("Machop", 40, ab, ["Karate Chop"])])
        sco, chop = b.b.cur(), b.p.cur()
        b.dice, b.rng = pl.RunDice(random.Random(1), True), random.Random(1)
        pl.use_move(b, sco, fs.move("Burning Bulwark"), chop, True)
        pl.use_move(b, chop, fs.move("Karate Chop"), sco, False)
        out[ab] = (sco.hp == sco.maxhp, chop.status)
    ok = out == {"Guts": (True, "brn"), "Water Veil": (True, None)}
    return [("Burning Bulwark burns a contact attacker in the readings", ok,
             f"(Scovillain untouched, the Machop's status) {out}")]


def trace_checks():
    """Trace on the calculator's real rows and the readings' battle
    (approved 2026-10-14): prepare rows Moira 1's Kirlia on a twin for the
    one foe's ability that changes its rows (Bronzor's Levitate; Diglett's
    Arena Trap changes none), and nothing more; leading against Bronzor it
    traces Levitate, so Diglett's Earthquake misses it where it hit before.
    A Synchronize Kirlia gets no twin and still takes the Earthquake."""
    from .test_fightai import battle
    foes = [("Bronzor", 26, "Levitate", ["Confusion"]), ("Diglett", 26, "Arena Trap", ["Earthquake"])]
    quake = fs.move("Earthquake")
    out = {}
    for ability in ("Trace", "Synchronize"):
        b = battle([("Kirlia", 26, ability, ["Psychic", "Magical Leaf"])], foes)
        kirlia = b.b.cur()
        twins = sorted(((b.st.get("form_twin") or {}).get(kirlia.key) or {}).get("twins", {}), key=repr)
        out[ability] = (kirlia.ability, b.p.mons[0].revealed, twins,
                        pl.damage_of(b, b.p.mons[1], kirlia, quake, False, True))
    t, s = out["Trace"], out["Synchronize"]
    ok = (t[0] == "Levitate" and t[1] == "Levitate" and t[2] == [(None, "Levitate")] and t[3] == 0
          and s[0] == "Synchronize" and s[2] == [] and s[3] > 0)
    return [("Trace: Moira 1's Kirlia copies Levitate on its twin's rows, and Earthquake misses it", ok,
             f"(its ability, Bronzor's named, its twins, Diglett's Earthquake) with Trace {t}; with Synchronize {s}")]


def mummy_checks():
    """Mummy on the calculator's real rows and the readings' move (approved
    2026-10-14): prepare rows a Huge Power Azumarill on its ability-blank
    twin, as it can take Mummy from Argo 1's drafted Cofagrigus; its first
    Aqua Tail into Cofagrigus gives it Mummy, and its next hits half as
    hard."""
    from .test_fightai import battle
    b = battle([("Cofagrigus", 40, "Mummy", ["Will-O-Wisp", "Hex"])], [("Azumarill", 40, "Huge Power", ["Aqua Tail"])])
    cof, azu = b.b.cur(), b.p.cur()
    tail = fs.move("Aqua Tail")
    twins = sorted(((b.st.get("form_twin") or {}).get(azu.key) or {}).get("twins", {}), key=repr)
    before = pl.damage_of(b, azu, cof, tail, False, True)
    b.dice, b.rng = pl.RunDice(random.Random(1), True), random.Random(1)
    cof.hp = cof.maxhp * 10
    pl.use_move(b, azu, tail, cof, True)
    after = (azu.ability, azu.revealed, pl.damage_of(b, azu, cof, tail, False, True))
    ok = twins == [(None, None)] and after[:2] == ("Mummy", "Mummy") and 1.8 <= before / max(1, after[2]) <= 2.2
    return [("Mummy: Azumarill's Aqua Tail into Cofagrigus takes its Huge Power away", ok,
             f"Azumarill's twins {twins}; Aqua Tail before {before}; after (its ability, named, Aqua Tail) {after}")]


def wandering_spirit_checks():
    """Wandering Spirit on the calculator's real rows and the readings' move
    (approved 2026-10-14): a Huge Power Azumarill's Aqua Tail into a
    Runerigus swaps their abilities, so Azumarill's next Aqua Tail hits
    half as hard and Runerigus's Shadow Claw twice as hard, each on the
    twin prepare made for the swap."""
    from .test_fightai import battle
    b = battle([("Runerigus", 40, "Wandering Spirit", ["Shadow Claw"])], [("Azumarill", 40, "Huge Power", ["Aqua Tail"])])
    run, azu = b.b.cur(), b.p.cur()
    tail, claw = fs.move("Aqua Tail"), fs.move("Shadow Claw")
    before = (pl.damage_of(b, azu, run, tail, False, True), pl.damage_of(b, run, azu, claw, False, True))
    b.dice, b.rng = pl.RunDice(random.Random(1), True), random.Random(1)
    run.hp = run.maxhp * 10
    pl.use_move(b, azu, tail, run, True)
    after = (azu.ability, run.ability, pl.damage_of(b, azu, run, tail, False, True),
             pl.damage_of(b, run, azu, claw, False, True))
    ok = (after[:2] == ("Wandering Spirit", "Huge Power") and 1.8 <= before[0] / max(1, after[2]) <= 2.2
          and 1.8 <= after[3] / max(1, before[1]) <= 2.2)
    return [("Wandering Spirit: Azumarill and Runerigus swap Huge Power on their twins' rows", ok,
             f"before (Aqua Tail, Shadow Claw) {before}; after (Azumarill's ability, Runerigus's, Aqua Tail, "
             f"Shadow Claw) {after}")]


def color_change_checks():
    """Color Change on the calculator's real rows and the readings' move
    (approved 2026-10-14): prepare rows Artist William's Kecleon on a twin of
    each type its foes' moves hit with (Water and Electric here); after a
    Squirtle's Water Gun it is a Water type, so a Pikachu's Thunderbolt hits
    it twice as hard as before."""
    from .test_fightai import battle
    b = battle([("Kecleon", 32, "Color Change", ["Slash", "Shadow Claw"])],
               [("Squirtle", 32, "Torrent", ["Water Gun"]), ("Pikachu", 32, "Static", ["Thunderbolt"])])
    kec = b.b.cur()
    squirtle, pika = b.p.mons
    bolt = fs.move("Thunderbolt")
    twins = sorted(((b.st.get("form_twin") or {}).get(kec.key) or {}).get("twins", {}), key=repr)
    before = pl.damage_of(b, pika, kec, bolt, False, True)
    b.dice, b.rng = pl.RunDice(random.Random(1), True), random.Random(1)
    kec.hp = kec.maxhp * 10
    pl.use_move(b, squirtle, fs.move("Water Gun"), kec, True)
    after = (list(kec.types), pl.damage_of(b, pika, kec, bolt, False, True))
    ok = (twins == [(("Electric",), None), (("Water",), None)] and after[0] == ["Water"]
          and abs(after[1] - 2 * before) <= 2)
    return [("Color Change: Kecleon turns Water after Water Gun, and Thunderbolt doubles on its twin's rows", ok,
             f"twins {twins}; Thunderbolt before {before}; after Water Gun (types, Thunderbolt) {after}")]


def forecast_checks():
    """Forecast in the readings' battle (approved 2026-10-14): Camper
    Zackary's Castform leading in a sunny fight is a Fire type from the
    battle's start, as its rows already had it, so a Vulpix's Will-O-Wisp
    cannot burn it; after a Rain Dance it is a Water type."""
    from .test_fightai import battle
    b = battle([("Castform", 24, "Forecast", ["Water Pulse", "Ember"])],
               [("Vulpix", 24, "Flash Fire", ["Will-O-Wisp", "Rain Dance"])], weather="Sun")
    cast, vulpix = b.b.cur(), b.p.cur()
    b.dice, b.rng = pl.RunDice(random.Random(1), True), random.Random(1)
    start = list(cast.types)
    vulpix.stages["acc"] = 6
    pl.use_move(b, vulpix, fs.move("Will-O-Wisp"), cast, True)
    burned = cast.status
    pl.use_move(b, vulpix, fs.move("Rain Dance"), cast, True)
    rain = (b.weather, list(cast.types))
    ok = start == ["Fire"] and burned is None and rain == ("Rain", ["Water"])
    return [("Forecast: Castform is Fire in sun, unburnt by Will-O-Wisp, and Water after Rain Dance", ok,
             f"types at the start {start}; status after Will-O-Wisp {burned}; after Rain Dance (weather, types) {rain}")]


def soak_checks():
    """Soak on the calculator's real rows and the readings' move (approved
    2026-10-14): prepare rows a Geodude on a pure Water twin, as a Staryu's
    Soak can make it one; after the Soak, Staryu's Thunderbolt hits it where
    its Ground type took nothing, and Staryu's Water Gun lands at half
    power where it landed four times over."""
    from .test_fightai import battle
    b = battle([("Geodude", 30, "Rock Head", ["Rock Throw"])],
               [("Staryu", 30, "Illuminate", ["Soak", "Thunderbolt", "Water Gun"])])
    geo, star = b.b.cur(), b.p.cur()
    bolt, gun = fs.move("Thunderbolt"), fs.move("Water Gun")
    twins = sorted(((b.st.get("form_twin") or {}).get(geo.key) or {}).get("twins", {}), key=repr)
    before = (pl.damage_of(b, star, geo, bolt, False, True), pl.damage_of(b, star, geo, gun, False, True))
    b.dice, b.rng = pl.RunDice(random.Random(1), True), random.Random(1)
    pl.use_move(b, star, fs.move("Soak"), geo, True)
    after = (list(geo.types), pl.damage_of(b, star, geo, bolt, False, True), pl.damage_of(b, star, geo, gun, False, True))
    ok = (twins == [(("Water",), None)] and before[0] == 0 and after[0] == ["Water"] and after[1] > 0
          and abs(after[2] * 8 - before[1]) <= 12)
    return [("Soak: a Geodude made pure Water meets Thunderbolt and Water Gun on its Water twin", ok,
             f"twins {twins}; before (Thunderbolt, Water Gun) {before}; after Soak (types, Thunderbolt, Water Gun) {after}")]


def conversion_checks():
    """Conversion on the calculator's real rows and the readings' move
    (approved 2026-10-14): prepare rows Scientist Travon's Porygon on a
    Psychic and a Bug twin, the types of its Psybeam and Signal Beam; after
    its Conversion, whichever it took, a Machop's Karate Chop lands at a
    quarter of what it did on Porygon's Normal type."""
    from .test_fightai import battle
    b = battle([("Porygon", 24, "Analytic", ["Psybeam", "Signal Beam", "Conversion", "Recover"])],
               [("Machop", 24, "Guts", ["Karate Chop"])])
    pory, machop = b.b.cur(), b.p.cur()
    chop = fs.move("Karate Chop")
    twins = sorted(((b.st.get("form_twin") or {}).get(pory.key) or {}).get("twins", {}), key=repr)
    before = pl.damage_of(b, machop, pory, chop, False, True)
    b.dice, b.rng = pl.RunDice(random.Random(1), True), random.Random(1)
    pl.use_move(b, pory, fs.move("Conversion"), machop, True)
    after = (list(pory.types), pl.damage_of(b, machop, pory, chop, False, True))
    ok = (twins == [(("Bug",), None), (("Psychic",), None)] and after[0] in (["Bug"], ["Psychic"])
          and abs(after[1] * 4 - before) <= 6)
    return [("Conversion: Porygon takes one of its moves' types, and Karate Chop quarters on its twin", ok,
             f"twins {twins}; Karate Chop before {before}; after Conversion (types, Karate Chop) {after}")]


def conversion2_checks():
    """Conversion 2 on the calculator's real rows and the readings' move
    (approved 2026-10-14): prepare rows a Porygon2 on a twin of each type
    that resists a Machop's Karate Chop; after a Karate Chop and its
    Conversion 2 it is one of them, and the next Karate Chop lands at half
    or less of what it did."""
    from .test_fightai import battle
    b = battle([("Porygon2", 30, "Download", ["Conversion 2", "Tri Attack"])], [("Machop", 30, "Guts", ["Karate Chop"])])
    pory, machop = b.b.cur(), b.p.cur()
    chop = fs.move("Karate Chop")
    twins = sorted(t[0][0] for t in ((b.st.get("form_twin") or {}).get(pory.key) or {}).get("twins", {}))
    before = pl.damage_of(b, machop, pory, chop, False, True)
    b.dice, b.rng = pl.RunDice(random.Random(1), True), random.Random(1)
    pory.hp = pory.maxhp * 10
    pl.use_move(b, machop, chop, pory, True)
    pl.use_move(b, pory, fs.move("Conversion 2"), machop, False)
    after = (list(pory.types), pl.damage_of(b, machop, pory, chop, False, True))
    resist = ["Bug", "Fairy", "Flying", "Ghost", "Poison", "Psychic"]
    ok = twins == resist and after[0][0] in resist and after[1] * 2 <= before
    return [("Conversion 2: Porygon2 takes a type that resists Karate Chop, on its twin's rows", ok,
             f"twins {twins}; Karate Chop before {before}; after (types, Karate Chop) {after}")]


def camouflage_checks():
    """Camouflage on the calculator's real rows and the readings' move
    (approved 2026-10-14): a fight's terrain comes from its trainer's map's
    backdrop (Roark's gym a building, Spear Pillar a mountain, Route 202
    plain ground), and prepare rows a Camouflage user on its twin of that
    terrain's type; on Route 202's ground, a Staryu's Camouflage makes it a
    Ground type, so a Pikachu's Thunderbolt then reads 0."""
    by = {t["constant"]: t["tr_id"] for t in data.oxide_trainers().values()}
    terrains = tuple(calc_terrain([by[c]]) for c in ("TRAINER_LEADER_ROARK", "TRAINER_COMMANDER_MARS_SPEAR_PILLAR",
                                                   "TRAINER_YOUNGSTER_TRISTAN"))

    def rec(sp, ab, mv):
        return {"species": sp, "level": 30, "ability": ab, "item": None, "nature": "Hardy", "ivs": IV, "evs": EV,
                "moves": mv}
    side = [dict(rec("Staryu", "Illuminate", ["Camouflage", "Water Gun"]), constant="SPECIES_STARYU", how="test",
                 fill=False)]
    st = fs.prepare("Gardenia", [[rec("Pikachu", "Static", ["Thunderbolt"])]], None, given_side=side,
                    terrain=terrains[2])
    b = pl.make_battle(st, ["p0"], st["bosses"][0], 7, 0)
    star, pika = b.p.cur(), b.b.cur()
    bolt = fs.move("Thunderbolt")
    twins = sorted(((st.get("form_twin") or {}).get(star.key) or {}).get("twins", {}), key=repr)
    before = pl.damage_of(b, pika, star, bolt, False, True)
    b.dice, b.rng = pl.RunDice(random.Random(1), True), random.Random(1)
    pl.use_move(b, star, fs.move("Camouflage"), pika, True)
    after = (list(star.types), pl.damage_of(b, pika, star, bolt, False, True))
    ok = (terrains == ("TERRAIN_BUILDING", "TERRAIN_MOUNTAIN", "TERRAIN_PLAIN") and twins == [(("Ground",), None)]
          and before > 0 and after == (["Ground"], 0))
    return [("Camouflage: Staryu takes Route 202's Ground type, and Thunderbolt then misses it", ok,
             f"terrains (Roark, Spear Pillar, Route 202) {terrains}; twins {twins}; Thunderbolt before {before}; "
             f"after Camouflage (types, Thunderbolt) {after}")]


def burn_up_checks():
    """Burn Up on the calculator's real rows and the readings' move
    (approved 2026-10-14): prepare rows a Ponyta on its typeless twins, as
    its Burn Up can leave it with no type; after one Burn Up into a
    Squirtle, the Squirtle's Water Gun lands at half what it did on the Fire
    type, and a second Burn Up fails."""
    from .test_fightai import battle
    b = battle([("Squirtle", 30, "Torrent", ["Water Gun"])], [("Ponyta", 30, "Run Away", ["Burn Up"])])
    squirtle, pony = b.b.cur(), b.p.cur()
    gun = fs.move("Water Gun")
    twins = sorted(((b.st.get("form_twin") or {}).get(pony.key) or {}).get("twins", {}), key=repr)
    before = pl.damage_of(b, squirtle, pony, gun, False, True)
    b.dice, b.rng = pl.RunDice(random.Random(1), True), random.Random(1)
    squirtle.hp = squirtle.maxhp * 10
    pl.use_move(b, pony, fs.move("Burn Up"), squirtle, True)
    first = squirtle.maxhp * 10 - squirtle.hp
    pl.use_move(b, pony, fs.move("Burn Up"), squirtle, True)
    second = squirtle.maxhp * 10 - squirtle.hp - first
    after = (list(pony.types), pl.damage_of(b, squirtle, pony, gun, False, True))
    ok = (twins == [(("???",), None)] and first > 0 and second == 0 and after[0] == ["???"]
          and after[1] is not None and abs(after[1] * 2 - before) <= 3)
    return [("Burn Up: Ponyta loses its Fire type, then Water Gun halves and a second Burn Up fails", ok,
             f"twins {twins}; Water Gun before {before}; the two Burn Ups' damage ({first}, {second}); "
             f"after (types, Water Gun) {after}")]


def double_shock_checks():
    """Double Shock on the calculator's real rows and the readings' move
    (approved 2026-10-14): prepare rows a Pawmot on a Fighting twin, its Volt
    Absorb kept, as its Double Shock can leave it Fighting alone; after one
    into a Squirtle, the Squirtle's Earthquake lands at half what it did on
    the Electric type, and a second Double Shock fails."""
    from .test_fightai import battle
    b = battle([("Squirtle", 40, "Torrent", ["Earthquake"])], [("Pawmot", 40, "Volt Absorb", ["Double Shock"])])
    squirtle, paw = b.b.cur(), b.p.cur()
    quake = fs.move("Earthquake")
    twins = sorted(((b.st.get("form_twin") or {}).get(paw.key) or {}).get("twins", {}), key=repr)
    before = pl.damage_of(b, squirtle, paw, quake, False, True)
    b.dice, b.rng = pl.RunDice(random.Random(1), True), random.Random(1)
    squirtle.hp = squirtle.maxhp * 10
    pl.use_move(b, paw, fs.move("Double Shock"), squirtle, True)
    first = squirtle.maxhp * 10 - squirtle.hp
    pl.use_move(b, paw, fs.move("Double Shock"), squirtle, True)
    second = squirtle.maxhp * 10 - squirtle.hp - first
    after = (list(paw.types), pl.damage_of(b, squirtle, paw, quake, False, True))
    ok = (twins == [(("Fighting",), "Volt Absorb")] and first > 0 and second == 0 and after[0] == ["Fighting"]
          and after[1] is not None and abs(after[1] * 2 - before) <= 3)
    return [("Double Shock: Pawmot loses its Electric type, so Earthquake halves and a second fails", ok,
             f"twins {twins}; Earthquake before {before}; the two Double Shocks' damage ({first}, {second}); "
             f"after (types, Earthquake) {after}")]


def skill_swap_checks():
    """Skill Swap on the calculator's real rows and the readings' move
    (approved 2026-10-14): prepare rows a Sylveon on a Levitate twin and a
    trainer's Bronzor on an ability-blank one, as a swap between them can
    make; after Sylveon's Skill Swap its Earthquake reaches Bronzor, where
    it took nothing, and the Bronzor's Earthquake no longer reaches it."""
    from .test_fightai import battle
    b = battle([("Bronzor", 30, "Levitate", ["Earthquake"])], [("Sylveon", 30, "Cute Charm", ["Skill Swap", "Earthquake"])])
    bronzor, syl = b.b.cur(), b.p.cur()
    quake = fs.move("Earthquake")
    twins = {m.species: sorted(((b.st.get("form_twin") or {}).get(m.key) or {}).get("twins", {}), key=repr)
             for m in (bronzor, syl)}
    before = (pl.damage_of(b, syl, bronzor, quake, False, True), pl.damage_of(b, bronzor, syl, quake, False, True))
    b.dice, b.rng = pl.RunDice(random.Random(1), True), random.Random(1)
    pl.use_move(b, syl, fs.move("Skill Swap"), bronzor, True)
    after = (syl.ability, bronzor.ability, pl.damage_of(b, syl, bronzor, quake, False, True),
             pl.damage_of(b, bronzor, syl, quake, False, True))
    ok = (twins == {"Bronzor": [(None, None)], "Sylveon": [(None, "Levitate")]} and before[0] == 0 and before[1] > 0
          and after[:2] == ("Levitate", "Cute Charm") and after[2] > 0 and after[3] == 0)
    return [("Skill Swap: Sylveon takes Bronzor's Levitate, on both twins' rows", ok,
             f"twins {twins}; Earthquake before (Sylveon's, Bronzor's) {before}; after (Sylveon's ability, "
             f"Bronzor's, the two Earthquakes) {after}")]


def role_play_checks():
    """Role Play on the calculator's real rows and the readings' move
    (approved 2026-10-14): prepare rows a trainer's Soundproof Mr. Mime on a
    twin for each foe's ability it could copy whose rows differ from its own
    (a Bronzor's Levitate, and a Diglett's Arena Trap, which would leave it
    without Soundproof); after its Role Play on Bronzor, the Diglett's
    Earthquake takes nothing from it, where it hit."""
    from .test_fightai import battle
    b = battle([("Mr. Mime", 30, "Soundproof", ["Role Play", "Psychic"])],
               [("Bronzor", 30, "Levitate", ["Confusion"]), ("Diglett", 30, "Arena Trap", ["Earthquake"])])
    mime = b.b.cur()
    bronzor, dig = b.p.mons
    quake = fs.move("Earthquake")
    twins = sorted(((b.st.get("form_twin") or {}).get(mime.key) or {}).get("twins", {}), key=repr)
    before = pl.damage_of(b, dig, mime, quake, False, True)
    b.dice, b.rng = pl.RunDice(random.Random(1), True), random.Random(1)
    pl.use_move(b, mime, fs.move("Role Play"), bronzor, True)
    after = (mime.ability, pl.damage_of(b, dig, mime, quake, False, True))
    ok = twins == [(None, "Levitate"), (None, None)] and before > 0 and after == ("Levitate", 0)
    return [("Role Play: Mr. Mime copies Bronzor's Levitate, and Earthquake misses it on its twin", ok,
             f"twins {twins}; Earthquake before {before}; after Role Play (its ability, Earthquake) {after}")]


def entrainment_checks():
    """Entrainment on the calculator's real rows and the readings' move
    (approved 2026-10-14): prepare rows a trainer's Bronzor on its
    ability-blank twin, as a Swarm Leavanny's Entrainment can give it Swarm,
    which changes no row; after the Entrainment the Leavanny's Earthquake
    reaches the Bronzor, which its Levitate had kept off."""
    from .test_fightai import battle
    b = battle([("Bronzor", 30, "Levitate", ["Confusion"])], [("Leavanny", 30, "Swarm", ["Entrainment", "Earthquake"])])
    bronzor, lea = b.b.cur(), b.p.cur()
    quake = fs.move("Earthquake")
    twins = sorted(((b.st.get("form_twin") or {}).get(bronzor.key) or {}).get("twins", {}), key=repr)
    before = pl.damage_of(b, lea, bronzor, quake, False, True)
    b.dice, b.rng = pl.RunDice(random.Random(1), True), random.Random(1)
    pl.use_move(b, lea, fs.move("Entrainment"), bronzor, True)
    after = (bronzor.ability, pl.damage_of(b, lea, bronzor, quake, False, True))
    ok = twins == [(None, None)] and before == 0 and after[0] == "Swarm" and after[1] > 0
    return [("Entrainment: a Bronzor given Swarm loses Levitate on its twin's rows", ok,
             f"twins {twins}; Earthquake before {before}; after Entrainment (its ability, Earthquake) {after}")]


def worry_seed_checks():
    """Worry Seed on the calculator's real rows and the readings' move
    (approved 2026-10-14): prepare rows a Levitate Bronzor on its
    ability-blank twin, as Lady Melissa's Cherrim's Worry Seed can give it
    Insomnia; after it, the Cherrim's Earthquake reaches the Bronzor, and
    a sleeping Bronzor wakes."""
    from .test_fightai import battle
    b = battle([("Cherrim", 30, "Flower Gift", ["Worry Seed", "Earthquake"])], [("Bronzor", 30, "Levitate", ["Confusion"])])
    cherrim, bronzor = b.b.cur(), b.p.cur()
    quake = fs.move("Earthquake")
    twins = sorted(((b.st.get("form_twin") or {}).get(bronzor.key) or {}).get("twins", {}), key=repr)
    before = pl.damage_of(b, cherrim, bronzor, quake, False, True)
    b.dice, b.rng = pl.RunDice(random.Random(1), True), random.Random(1)
    bronzor.status, bronzor.sleep = "slp", 3
    pl.use_move(b, cherrim, fs.move("Worry Seed"), bronzor, True)
    after = (bronzor.ability, bronzor.status, pl.damage_of(b, cherrim, bronzor, quake, False, True))
    ok = twins == [(None, None)] and before == 0 and after[:2] == ("Insomnia", None) and after[2] > 0
    return [("Worry Seed: a Bronzor given Insomnia wakes and loses Levitate on its twin's rows", ok,
             f"twins {twins}; Earthquake before {before}; after Worry Seed (its ability, status, Earthquake) {after}")]


def gastro_acid_checks():
    """Gastro Acid on the calculator's real rows and the readings' move
    (approved 2026-10-14): prepare rows a Levitate Bronzor on its
    ability-blank twin, as Pkmn Ranger Ashlee's Arbok's Gastro Acid can
    suppress it; after it, the Arbok's Earthquake reaches the Bronzor."""
    from .test_fightai import battle
    b = battle([("Arbok", 30, "Intimidate", ["Gastro Acid", "Earthquake"])], [("Bronzor", 30, "Levitate", ["Confusion"])])
    arbok, bronzor = b.b.cur(), b.p.cur()
    quake = fs.move("Earthquake")
    twins = sorted(((b.st.get("form_twin") or {}).get(bronzor.key) or {}).get("twins", {}), key=repr)
    before = pl.damage_of(b, arbok, bronzor, quake, False, True)
    b.dice, b.rng = pl.RunDice(random.Random(1), True), random.Random(1)
    pl.use_move(b, arbok, fs.move("Gastro Acid"), bronzor, True)
    after = (bronzor.ability, getattr(bronzor, "suppressed", False), pl.damage_of(b, arbok, bronzor, quake, False, True))
    ok = twins == [(None, None)] and before == 0 and after[:2] == (None, True) and after[2] > 0
    return [("Gastro Acid: a suppressed Bronzor loses Levitate on its twin's rows", ok,
             f"twins {twins}; Earthquake before {before}; after Gastro Acid (ability, suppressed, Earthquake) {after}")]


def core_enforcer_checks():
    """Core Enforcer on the calculator's real rows and the readings' move
    (approved 2026-10-14): prepare rows a Levitate Bronzor on its
    ability-blank twin, as a Kingdra's Core Enforcer can suppress it; once
    the Bronzor has moved, the Kingdra's Core Enforcer takes its Levitate,
    and the Kingdra's Earthquake then reaches it."""
    from .test_fightai import battle
    b = battle([("Kingdra", 50, "Sniper", ["Core Enforcer", "Earthquake"])], [("Bronzor", 50, "Levitate", ["Confusion"])])
    king, bronzor = b.b.cur(), b.p.cur()
    quake = fs.move("Earthquake")
    twins = sorted(((b.st.get("form_twin") or {}).get(bronzor.key) or {}).get("twins", {}), key=repr)
    before = pl.damage_of(b, king, bronzor, quake, False, True)
    b.dice, b.rng = pl.RunDice(random.Random(1), True), random.Random(1)
    bronzor.hp = bronzor.maxhp * 10
    pl.use_move(b, bronzor, fs.move("Confusion"), king, True)
    pl.use_move(b, king, fs.move("Core Enforcer"), bronzor, False)
    after = (bronzor.ability, pl.damage_of(b, king, bronzor, quake, False, True))
    ok = twins == [(None, None)] and before == 0 and after[0] is None and after[1] > 0
    return [("Core Enforcer: a Bronzor that has moved loses Levitate on its twin's rows", ok,
             f"twins {twins}; Earthquake before {before}; after Core Enforcer (its ability, Earthquake) {after}")]


def captivate_checks():
    """Captivate in the readings' battle, on the genders prepare gives the
    battle (approved 2026-10-14): a female trainer's Persian's Captivate
    takes two stages of Sp. Atk off a male Bibarel and none off a female
    one."""
    def rec(sp, ab, mv, gender):
        return {"species": sp, "level": 30, "ability": ab, "item": None, "nature": "Hardy", "ivs": IV, "evs": EV,
                "moves": mv, "gender": gender}
    side = [dict(rec("Bibarel", "Simple", ["Tackle"], g), constant="SPECIES_BIBAREL", how="test", fill=False)
            for g in ("male", "female")]
    st = fs.prepare("Roark", [[rec("Persian", "Limber", ["Captivate"], "female")]], None, given_side=side)
    out = {}
    for i, label in ((0, "male"), (1, "female")):
        b = pl.make_battle(st, ["p0", "p1"], st["bosses"][0], 7, i)
        b.dice, b.rng = pl.RunDice(random.Random(1), True), random.Random(1)
        persian, bib = b.b.cur(), b.p.cur()
        bib.ability = None          # Simple would double the drop
        pl.use_move(b, persian, fs.move("Captivate"), bib, True)
        out[label] = (persian.gender, bib.gender, bib.stages["spa"])
    ok = out == {"male": ("F", "M", -2), "female": ("F", "F", 0)}
    return [("Captivate: a female Persian's lowers a male Bibarel's Sp. Atk and leaves a female's", ok,
             f"(Persian's gender, Bibarel's, its Sp. Atk stage) {out}")]


def vanished_status_checks():
    """A status move into a target on its hidden turn, in the readings'
    battle on the calculator's real rows (approved 2026-10-14): a trainer's
    Staraptor takes Fly's first turn, and a Raichu's Thunder Wave aimed at it
    then misses; the same Thunder Wave paralyses it once Fly has landed."""
    from .test_fightai import battle
    b = battle([("Staraptor", 30, "Reckless", ["Fly"])], [("Raichu", 40, "Lightning Rod", ["Thunder Wave"])])
    b.dice, b.rng = pl.RunDice(random.Random(1), True), random.Random(1)
    star, rai = b.b.cur(), b.p.cur()
    pl.use_move(b, star, fs.move("Fly"), rai, True)
    up = star.charging is not None
    pl.use_move(b, rai, fs.move("Thunder Wave"), star, False)
    missed = star.status
    pl.use_move(b, star, star.charging, rai, True)
    landed_fly = star.charging is None and rai.hp < rai.maxhp
    pl.use_move(b, rai, fs.move("Thunder Wave"), star, False)
    got = (up, missed, landed_fly, star.status)
    return [("the readings' Thunder Wave misses a Staraptor in the air and paralyses it after", got ==
             (True, None, True, "par"), f"(in the air, its status after, Fly landed, its status then) {got}")]


def speed_down_hit_checks():
    """Hammer Arm in the readings' battle on the calculator's real rows
    (approved 2026-10-14): a trainer's Hariyama hits a Staraptor with it,
    and the Hariyama's own Speed falls a stage while the Staraptor's stays."""
    from .test_fightai import battle
    b = battle([("Hariyama", 40, "Thick Fat", ["Hammer Arm"])], [("Staraptor", 40, "Reckless", ["Tackle"])])
    b.dice, b.rng = pl.RunDice(random.Random(1), True), random.Random(1)
    har, star = b.b.cur(), b.p.cur()
    pl.use_move(b, har, fs.move("Hammer Arm"), star, True)
    got = (star.hp < star.maxhp, har.stages["spe"], star.stages["spe"])
    return [("the readings' Hammer Arm lowers its user's Speed, not its target's", got == (True, -1, 0),
             f"(hit, Hariyama's Speed stage, Staraptor's) {got}")]


def bounce_paralysis_checks():
    """Bounce in the readings' battle on the calculator's real rows
    (approved 2026-10-14): a trainer's Lopunny takes Bounce's first turn and
    comes down on a Bibarel, 300 times on the game's odds; about 30% of the
    hits paralyse it (the window is 20% to 40%)."""
    from .test_fightai import battle
    b0 = battle([("Lopunny", 40, "Limber", ["Bounce"])], [("Bibarel", 40, "Unaware", ["Tackle"])])
    landed = par = 0
    for seed in range(300):
        b = pl.clone_battle(b0)
        b.dice, b.rng = pl.RunDice(random.Random(seed), True), random.Random(seed)
        lop, bib = b.b.cur(), b.p.cur()
        pl.use_move(b, lop, fs.move("Bounce"), bib, True)
        pl.use_move(b, lop, lop.charging or fs.move("Bounce"), bib, True)
        if bib.hp < bib.maxhp:
            landed += 1
            par += bib.status == "par"
    share = par / landed if landed else 0
    return [("the readings' Bounce paralyses at about its 30% chance", 0.2 <= share <= 0.4,
             f"{par} paralysed of {landed} hits that landed ({share:.0%})")]


def weather_heal_checks():
    """Synthesis and Shore Up in the readings' battle on the calculator's
    real rows (approved 2026-10-14): the player's Cherrim at 1 HP under sun
    restores two thirds of its HP against a trainer's Damp Golduck and half
    against a Cloud Nine one (the player never holds Cloud Nine); its Shore
    Up in a sandstorm restores two thirds."""
    from .test_fightai import battle
    out = {}
    for label, ability, move, weather in (("Damp, sun", "Damp", "Synthesis", "Sun"),
                                          ("Cloud Nine, sun", "Cloud Nine", "Synthesis", "Sun"),
                                          ("Damp, sand", "Damp", "Shore Up", "Sand")):
        b = battle([("Golduck", 40, ability, ["Tackle"])], [("Cherrim", 40, "Flower Gift", ["Synthesis", "Shore Up"])])
        b.dice, b.rng = pl.RunDice(random.Random(1), True), random.Random(1)
        b.weather, b.weather_turns = weather, 0
        duck, che = b.b.cur(), b.p.cur()
        che.hp = 1
        pl.use_move(b, che, fs.move(move), duck, True)
        out[label] = (duck.ability, che.hp - 1, che.maxhp)
    want = {"Damp, sun": 20 / 30, "Cloud Nine, sun": 1 / 2, "Damp, sand": 20 / 30}
    ok = all(got == int(m * want[k] + 1e-9) for k, (_a, got, m) in out.items())
    return [("the readings' Synthesis halves under Cloud Nine; Shore Up restores two thirds in sand", ok,
             f"(Golduck's ability, HP restored, maximum HP) {out}")]


def hail_checks():
    """Hail in the readings' battle on the calculator's real rows (approved
    2026-10-14): a trainer's Abomasnow with Snow Warning brings a lasting
    hail in; its Glaceon partner's Hail then makes it a five-turn hail,
    and after five turn ends the hail is gone."""
    from .test_fightai import battle
    b = battle([("Abomasnow", 50, "Snow Warning", ["Ice Shard"]), ("Glaceon", 50, "Snow Cloak", ["Hail"])],
               [("Bibarel", 50, "Unaware", ["Tackle"])])
    b.dice, b.rng = pl.RunDice(random.Random(1), True), random.Random(1)
    lasting = (b.weather, b.weather_turns)
    fs.switch_in(b, b.b, 1)
    gla, bib = b.b.cur(), b.p.cur()
    pl.use_move(b, gla, fs.move("Hail"), bib, True)
    after = (b.weather, b.weather_turns)
    for _ in range(5):
        fs.end_of_turn(b)
    got = (lasting, after, b.weather)
    return [("the readings' Hail turns Snow Warning's lasting hail into five turns", got ==
             (("Hail", 0), ("Hail", 5), None), f"(weather on entry, after Hail, after five turn ends) {got}")]


def dream_eater_checks():
    """Dream Eater in the readings' battle on the calculator's real rows
    (approved 2026-10-14): a trainer's Hypno's Dream Eater leaves an awake
    Bibarel and itself as they were, and on the Bibarel asleep it hits and
    takes back half the damage."""
    from .test_fightai import battle
    out = {}
    for label, status in (("awake", None), ("asleep", "slp")):
        b = battle([("Hypno", 40, "Insomnia", ["Dream Eater"])], [("Bibarel", 40, "Unaware", ["Tackle"])])
        b.dice, b.rng = pl.RunDice(random.Random(1), True), random.Random(1)
        hyp, bib = b.b.cur(), b.p.cur()
        bib.status, bib.sleep = status, 3 if status else 0
        hyp.hp = hyp.maxhp // 2
        before = hyp.hp
        pl.use_move(b, hyp, fs.move("Dream Eater"), bib, True)
        dealt = bib.maxhp - bib.hp
        out[label] = (dealt, hyp.hp - before)
    ok = out["awake"] == (0, 0) and out["asleep"][0] > 0 and out["asleep"][1] == out["asleep"][0] // 2
    return [("the readings' Dream Eater misses an awake target and drains a sleeping one", ok,
             f"(damage dealt, HP taken back) {out}")]


def focus_punch_checks():
    """Focus Punch in the readings' battle on the calculator's real rows
    (approved 2026-10-14): a whole turn in which a trainer's faster
    Staraptor hits the player's Machamp with Quick Attack, and the Machamp's
    Focus Punch then fails; in a turn when the Staraptor uses Growl it
    lands."""
    from .test_fightai import battle
    out = {}
    for label, foe_move in (("hit first", "Quick Attack"), ("not hit", "Growl")):
        b = battle([("Staraptor", 40, "Reckless", ["Quick Attack", "Growl"])],
                   [("Machamp", 40, "Guts", ["Focus Punch"])])
        b.dice, b.rng = pl.RunDice(random.Random(1), True), random.Random(1)
        star, champ = b.b.cur(), b.p.cur()
        pl._turn(b, ("move", fs.move("Focus Punch")), ("move", fs.move(foe_move)))
        out[label] = (champ.hp < champ.maxhp, star.hp < star.maxhp)
    ok = out == {"hit first": (True, False), "not hit": (False, True)}
    return [("the readings' Focus Punch fails after a hit and lands without one", ok,
             f"(Machamp hit, Staraptor hit) {out}")]


def crash_checks():
    """High Jump Kick in the readings' battle on the calculator's real rows
    (approved 2026-10-14): a trainer's Hitmonlee kicks into the player's
    Protect or into a Pokemon in the air, and crashes for half the damage
    its hit would have done (between half its row's lowest roll and half
    its highest with a critical hit), at most half the target's maximum HP:
    a Togekiss resists the hit, so the crash is half of it, while a Bibarel
    takes enough that half its maximum HP caps the crash."""
    from .test_fightai import battle
    out = {}
    for species, ability, how in (("Togekiss", "Hustle", "into Protect"), ("Togekiss", "Hustle", "into Fly"),
                                  ("Bibarel", "Unaware", "into Protect")):
        b = battle([("Hitmonlee", 40, "Limber", ["High Jump Kick"])], [(species, 40, ability, ["Protect", "Fly"])])
        b.dice, b.rng = pl.RunDice(random.Random(1), True), random.Random(1)
        lee, mon = b.b.cur(), b.p.cur()
        if how == "into Protect":
            mon.protecting = True
        else:
            mon.charging = fs.move("Fly")
        hjk = fs.move("High Jump Kick")
        lo = pl.damage_of(b, lee, mon, hjk, False, top=False)
        hi = pl.damage_of(b, lee, mon, hjk, True, top=True)
        pl.use_move(b, lee, hjk, mon, True)
        lost = lee.maxhp - lee.hp
        out[f"{species} {how}"] = (lost, min(lo // 2, mon.maxhp // 2), min(hi // 2, mon.maxhp // 2),
                                   mon.hp == mon.maxhp)
    ok = all(a <= lost <= c and d and lost > 0 for lost, a, c, d in out.values()) \
        and out["Togekiss into Protect"][2] < b.p.cur().maxhp // 2
    return [("the readings' High Jump Kick crashes for half its hit into Protect or Fly", ok,
             f"(HP lost, lowest allowed, highest allowed, target untouched) {out}")]


def bind_checks():
    """Sand Tomb in the readings' battle on the calculator's real rows
    (approved 2026-10-14): a trainer's Hippowdon binds the player's Bibarel
    on the battle's dice; each turn's end then costs it an eighth of its
    maximum HP while the count lasts, and the bind ends when the Hippowdon
    switches out."""
    from .test_fightai import battle
    b = battle([("Hippowdon", 40, "Sand Stream", ["Sand Tomb"]), ("Gastrodon", 40, "Sticky Hold", ["Tackle"])],
               [("Bibarel", 40, "Unaware", ["Tackle"])])
    b.dice, b.rng = pl.RunDice(random.Random(1), True), random.Random(1)
    b.weather, b.weather_turns = None, 0
    hip, bib = b.b.cur(), b.p.cur()
    pl.use_move(b, hip, fs.move("Sand Tomb"), bib, True)
    count = bib.bound
    hp = bib.hp
    fs.end_of_turn(b)
    lost = hp - bib.hp
    fs.switch_in(b, b.b, 1)
    got = (3 <= count <= 6, lost == bib.maxhp // 8, bib.bound, fs.trapped(b, bib))
    return [("the readings' Sand Tomb takes an eighth a turn and ends with its binder", got == (True, True, 0, False),
             f"(count {count} in 3 to 6, an eighth lost ({lost} of {bib.maxhp}), count after the binder left, "
             f"trapped) {got}")]


def steal_item_checks():
    """Thief in the readings' battle on the calculator's real rows
    (approved 2026-10-14): the player's empty-handed Frogadier takes a
    trainer's Breloom's Coba Berry, and a Frogadier holding a Mystic Water
    takes nothing. A trainer's Honchkrow's Thief leaves the player's
    Leftovers where they are."""
    from .test_fightai import battle
    out = {}
    for label, item in (("empty-handed", None), ("holding Mystic Water", "Mystic Water")):
        b = battle([("Breloom", 30, "Technician", ["Mach Punch"], "Coba Berry")],
                   [("Frogadier", 30, "Torrent", ["Thief", "Aerial Ace"])])
        b.dice, b.rng = pl.RunDice(random.Random(1), True), random.Random(1)
        bre, frog = b.b.cur(), b.p.cur()
        bre.item, frog.item = "Coba Berry", item
        pl.use_move(b, frog, fs.move("Thief"), bre, True)
        out[label] = (frog.item, bre.item)
    b = battle([("Honchkrow", 40, "Insomnia", ["Thief"])], [("Bibarel", 40, "Unaware", ["Tackle"], "Leftovers")])
    b.dice, b.rng = pl.RunDice(random.Random(1), True), random.Random(1)
    honch, bib = b.b.cur(), b.p.cur()
    pl.use_move(b, honch, fs.move("Thief"), bib, True)
    out["a trainer's Thief"] = (honch.item, bib.item, bib.hp < bib.maxhp)
    ok = out == {"empty-handed": ("Coba Berry", None), "holding Mystic Water": ("Mystic Water", "Coba Berry"),
                 "a trainer's Thief": (None, "Leftovers", True)}
    return [("the readings' Thief steals for the player's empty-handed Pokemon only", ok,
             f"(thief's item, target's item[, hit]) {out}")]


def swap_items_checks():
    """Trick in the readings' battle on the calculator's real rows
    (approved 2026-10-14): the player's Alakazam's Trick gives its Charcoal
    to a trainer's Rotom and takes the Rotom's Leftovers, which then heal
    the Alakazam at the turn's end; the Rotom's own Trick on the Alakazam
    swaps nothing."""
    from .test_fightai import battle
    b = battle([("Rotom", 40, "Levitate", ["Trick", "Thunderbolt"], "Leftovers")],
               [("Alakazam", 40, "Synchronize", ["Trick", "Psychic"], "Charcoal")])
    b.dice, b.rng = pl.RunDice(random.Random(1), True), random.Random(1)
    rot, zam = b.b.cur(), b.p.cur()
    rot.item = "Leftovers"
    pl.use_move(b, rot, fs.move("Trick"), zam, True)
    after_trainer = (zam.item, rot.item)
    pl.use_move(b, zam, fs.move("Trick"), rot, False)
    after_player = (zam.item, rot.item)
    zam.hp = zam.maxhp // 2
    hp = zam.hp
    fs.end_of_turn(b)
    got = (after_trainer, after_player, zam.hp - hp)
    ok = got == (("Charcoal", "Leftovers"), ("Leftovers", "Charcoal"), zam.maxhp // 16)
    return [("the readings' Trick swaps for the player and not for the trainer", ok,
             f"(items after the Rotom's Trick, after the Alakazam's, HP the Leftovers gave back) {got}")]


def pluck_checks():
    """Pluck in the readings' battle on the calculator's real rows (approved
    2026-10-14): the player's poisoned Staravia plucks a trainer's
    Roserade's Lum Berry and is cured; a trainer's Gastrodon's Sticky Hold
    keeps its Sitrus Berry from the same Pluck."""
    from .test_fightai import battle
    out = {}
    for label, boss in (("Lum Berry", ("Roserade", 30, "Natural Cure", ["Tackle"], "Lum Berry")),
                        ("Sticky Hold", ("Gastrodon", 30, "Sticky Hold", ["Tackle"], "Sitrus Berry"))):
        b = battle([boss], [("Staravia", 30, "Intimidate", ["Pluck"])])
        b.dice, b.rng = pl.RunDice(random.Random(1), True), random.Random(1)
        foe, star = b.b.cur(), b.p.cur()
        foe.item = boss[4]
        star.status = "psn"
        pl.use_move(b, star, fs.move("Pluck"), foe, True)
        out[label] = (star.status, foe.item, foe.hp < foe.maxhp)
    ok = out == {"Lum Berry": (None, None, True), "Sticky Hold": ("psn", "Sitrus Berry", True)}
    return [("the readings' Pluck takes a Lum Berry's cure and meets Sticky Hold", ok,
             f"(Staravia's status, the target's item, hit) {out}")]


def chatter_checks():
    """Chatter in the readings' battle on the calculator's real rows
    (approved 2026-10-14): a trainer's Chatot's Chatter confuses the
    player's Bibarel about once in 100 hits; 3000 hits on the game's odds
    confuse it between 15 and 50 times."""
    from .test_fightai import battle
    b0 = battle([("Chatot", 40, "Keen Eye", ["Chatter"])], [("Bibarel", 40, "Unaware", ["Tackle"])])
    confused = hits = 0
    for seed in range(3000):
        b = pl.clone_battle(b0)
        b.dice, b.rng = pl.RunDice(random.Random(seed), True), random.Random(seed)
        chat, bib = b.b.cur(), b.p.cur()
        pl.use_move(b, chat, fs.move("Chatter"), bib, True)
        hits += bib.hp < bib.maxhp
        confused += bool(bib.confused)
    return [("the readings' Chatter confuses about 1 time in 100", 15 <= confused <= 50 and hits > 2900,
             f"{confused} confused in {hits} hits")]


def stockpile_checks():
    """Stockpile and Spit Up in the readings' battle on the calculator's
    real rows (approved 2026-10-14): a trainer's Swalot stockpiles twice and
    its Spit Up then deals the top roll of its 200-power row, above the top
    of its 100-power one, and gives its two Defense and Sp. Def stages back;
    its Swallow after one Stockpile restores a quarter of its HP."""
    from .test_fightai import battle
    b = battle([("Swalot", 40, "Gluttony", ["Stockpile", "Spit Up", "Swallow"])], [("Bibarel", 40, "Unaware", ["Tackle"])])
    b.dice, b.rng = pl.RunDice(random.Random(1), True), random.Random(1)
    swa, bib = b.b.cur(), b.p.cur()
    top = {p: b.st["rows"][(None, f"{swa.key}#su{p}", bib.key)]["moves"]["Spit Up"]["rolls"][-1] for p in (100, 200)}
    for _ in range(2):
        pl.use_move(b, swa, fs.move("Stockpile"), bib, True)
    stored = (swa.stockpile, swa.stages["def"], swa.stages["spd"])
    b.dice.one_crit = False
    b.dice.rng = random.Random(3)            # no critical hit on this seed
    pl.use_move(b, swa, fs.move("Spit Up"), bib, True)
    dealt = bib.maxhp - bib.hp
    after = (swa.stockpile, swa.stages["def"], swa.stages["spd"])
    pl.use_move(b, swa, fs.move("Stockpile"), bib, True)
    swa.hp = 1
    pl.use_move(b, swa, fs.move("Swallow"), bib, True)
    healed = swa.hp - 1
    ok = (stored == (2, 2, 2) and dealt in (top[200], int(top[200] * 1.5)) and top[200] > top[100]
          and after == (0, 0, 0) and healed == swa.maxhp // 4)
    return [("the readings' Spit Up hits at its stockpiles' power; Swallow restores by them", ok,
             f"stored {stored}, Spit Up dealt {dealt} (tops {top}), after {after}, Swallow restored {healed} "
             f"of {swa.maxhp}")]


def lower_sp_atk_checks():
    """Snarl in the readings' battle on the calculator's real rows (approved
    2026-10-14): a trainer's Poochyena's Snarl hits the player's Bibarel and
    lowers its Sp. Atk a stage, as effect script 71 does every time."""
    from .test_fightai import battle
    b = battle([("Poochyena", 20, "Run Away", ["Snarl"])], [("Bibarel", 20, "Unaware", ["Tackle"])])
    b.dice, b.rng = pl.RunDice(random.Random(1), True), random.Random(1)
    poo, bib = b.b.cur(), b.p.cur()
    pl.use_move(b, poo, fs.move("Snarl"), bib, True)
    ok = bib.hp < bib.maxhp and bib.stages["spa"] == -1
    return [("the readings' Snarl lowers its target's Sp. Atk", ok,
             f"Bibarel {bib.hp}/{bib.maxhp}, Sp. Atk stage {bib.stages['spa']}")]


def rollout_checks():
    """Rollout in the readings' battle on the calculator's real rows
    (approved 2026-10-14): a trainer's Geodude rolls five times in a row,
    held in through every turn's end, each hit a place further along (1 to
    16 times), and is then free, its next Rollout starting again at once;
    a turn it is fully paralysed ends the run, and the next starts again."""
    from .test_fightai import battle

    class Sure(pl.RunDice):
        """Run dice where the trainer never misses and is fully paralysed
        only while `stop` is set."""
        stop = False

        def good(self, p, kind=None):
            return kind == "paralysis" and self.stop
    b = battle([("Geodude", 20, "Rock Head", ["Rollout"])], [("Bibarel", 20, "Unaware", ["Leer"])])
    b.dice, b.rng = Sure(random.Random(1), True), random.Random(1)
    geo, bib = b.b.cur(), b.p.cur()
    bib.hp = bib.maxhp = 100000
    roll, leer = fs.move("Rollout"), fs.move("Leer")
    seen = []
    for turn in range(9):
        b.dice.stop = turn == 7
        geo.status = "par" if turn == 7 else None
        forced = geo.lock is not None
        pl._turn(b, ("move", leer), ("move", geo.lock[0] if forced else roll))
        seen.append((forced, "par" if turn == 7 else geo.rollout_hit, geo.lock is not None))
    want = [(False, 0, True), (True, 1, True), (True, 2, True), (True, 3, True), (True, 4, False),
            (False, 0, True), (True, 1, True), (True, "par", False), (False, 0, True)]
    return [("the readings' Rollout runs five uses, then starts again; a paralysis ends the run", seen == want,
             f"(forced, place in the run, locked after) per turn {seen}")]


def wake_up_slap_checks():
    """Wake-Up Slap in the readings' battle on the calculator's real rows
    (approved 2026-10-14): a trainer's Hariyama slaps the player's sleeping
    Bibarel at twice the row's power and wakes it, and its next slap hits at
    the row's own power."""
    from .test_fightai import battle
    b = battle([("Hariyama", 30, "Thick Fat", ["Wake-Up Slap"])], [("Bibarel", 30, "Unaware", ["Tackle"])])
    b.dice, b.rng = pl.RunDice(random.Random(1), True), random.Random(1)
    b.dice.one_crit = False
    har, bib = b.b.cur(), b.p.cur()
    rolls = b.st["rows"][(None, har.key, bib.key)]["moves"]["Wake-Up Slap"]["rolls"]
    bib.hp = bib.maxhp = 100000
    bib.status, bib.sleep = "slp", 3
    slap = fs.move("Wake-Up Slap")
    pl.use_move(b, har, slap, bib, True)
    first, woke = bib.maxhp - bib.hp, bib.status is None
    before = bib.hp
    pl.use_move(b, har, slap, bib, True)
    second = before - bib.hp
    ok = woke and 2 * rolls[0] <= first <= 3 * rolls[-1] and rolls[0] <= second <= 1.5 * rolls[-1] and first > second
    return [("the readings' Wake-Up Slap doubles on a sleeper and wakes it", ok,
             f"first slap {first}, woke {woke}, second {second}, row {rolls[0]} to {rolls[-1]}")]


def throat_chop_checks():
    """Throat Chop in the readings' battle on the calculator's real rows
    (approved 2026-10-14): a trainer's Zangoose chops the player's Loudred,
    whose Hyper Voice then leaves its options and fails if tried, until the
    second turn's end has passed."""
    from .test_fightai import battle
    b = battle([("Zangoose", 30, "Immunity", ["Throat Chop"])], [("Loudred", 30, "Soundproof", ["Hyper Voice", "Stomp"])])
    b.dice, b.rng = pl.RunDice(random.Random(1), True), random.Random(1)
    zan, lou = b.b.cur(), b.p.cur()
    lou.hp = lou.maxhp = 100000
    pl.use_move(b, zan, fs.move("Throat Chop"), lou, True)
    held = getattr(lou, "throat_chop", 0)

    def offered():
        return sorted(a[1].name for a in pl.player_actions(b) if a[0] == "move")
    first = offered()
    before = zan.hp
    pl.use_move(b, lou, fs.move("Hyper Voice"), zan, False)
    failed = zan.hp == before
    fs.end_of_turn(b)
    second = offered()
    fs.end_of_turn(b)
    third = offered()
    ok = held == 2 and first == ["Stomp"] and failed and second == ["Stomp"] and third == ["Hyper Voice", "Stomp"]
    return [("the readings' Throat Chop holds the target's sound moves through the next turn", ok,
             f"count {held}; offered {first}, then {second}, then {third}; Hyper Voice failed {failed}")]


def minimize_checks():
    """Minimize and Stomp in the readings' battle on the calculator's real
    rows (approved 2026-10-14): a trainer's Grimer minimizes, and the
    player's Ponyta's Stomp then hits it at twice its row."""
    from .test_fightai import battle

    class Steady(pl.RunDice):
        """Run dice with no luck either way: no miss, critical hit or proc."""
        def bad(self, kind, p):
            return False

        def good(self, p, kind=None):
            return False
    b = battle([("Grimer", 25, "Stench", ["Minimize"])], [("Ponyta", 25, "Run Away", ["Stomp"])])
    b.dice, b.rng = Steady(random.Random(1), True), random.Random(1)
    gri, pon = b.b.cur(), b.p.cur()
    rolls = b.st["rows"][(None, pon.key, gri.key)]["moves"]["Stomp"]["rolls"]
    gri.hp = gri.maxhp = 100000
    pl.use_move(b, gri, fs.move("Minimize"), pon, True)
    pl.use_move(b, pon, fs.move("Stomp"), gri, False)
    dealt = gri.maxhp - gri.hp
    ok = getattr(gri, "minimized", False) and gri.stages["eva"] == 2 and 2 * rolls[0] - 1 <= dealt <= 2 * rolls[-1]
    return [("the readings' Stomp doubles on a Minimize user", ok,
             f"evasion {gri.stages['eva']}, marked {getattr(gri, 'minimized', None)}, Stomp dealt {dealt}, "
             f"row {rolls[0]} to {rolls[-1]}")]


def charge_checks():
    """Charge in the readings' battle on the calculator's real rows
    (approved 2026-10-14): a trainer's Pikachu charges, and its Thunder
    Shock then hits the player's Bibarel at twice its row, as the trainer's
    AI also reckons it."""
    from .test_fightai import battle

    class Steady(pl.RunDice):
        def bad(self, kind, p):
            return False

        def good(self, p, kind=None):
            return False
    b = battle([("Pikachu", 25, "Static", ["Charge", "Thunder Shock"])], [("Bibarel", 25, "Unaware", ["Tackle"])])
    b.dice, b.rng = Steady(random.Random(1), True), random.Random(1)
    pik, bib = b.b.cur(), b.p.cur()
    rolls = b.st["rows"][(None, pik.key, bib.key)]["moves"]["Thunder Shock"]["rolls"]
    bib.hp = bib.maxhp = 100000
    shock = fs.move("Thunder Shock")
    before_ai = fightai.figure(b, pik, bib, shock)
    pl.use_move(b, pik, fs.move("Charge"), bib, True)
    after_ai = fightai.figure(b, pik, bib, shock)
    pl.use_move(b, pik, shock, bib, True)
    dealt = bib.maxhp - bib.hp
    ok = pik.stages["spd"] == 1 and 2 * rolls[0] - 1 <= dealt <= 2 * rolls[-1] and after_ai >= 2 * before_ai - 1
    return [("the readings' Charge doubles the next Electric hit, in the AI's figure too", ok,
             f"Sp. Def {pik.stages['spd']}, Thunder Shock dealt {dealt} (row {rolls[0]} to {rolls[-1]}), "
             f"AI figure {before_ai} then {after_ai}")]


def lucky_chant_checks():
    """Lucky Chant in the readings' battle on the calculator's real rows
    (approved 2026-10-14): the player's Bibarel, set to land a critical hit
    every time, lands one on a trainer's Clefairy until the Clefairy's
    Lucky Chant goes up, and none after."""
    from .test_fightai import battle
    b = battle([("Clefairy", 25, "Cute Charm", ["Lucky Chant"])], [("Bibarel", 25, "Unaware", ["Tackle"])])
    b.dice, b.rng = pl.RunDice(random.Random(1), True), random.Random(1)
    cle, bib = b.b.cur(), b.p.cur()
    rolls = b.st["rows"][(None, bib.key, cle.key)]["moves"]["Tackle"]["rolls"]
    cle.hp = cle.maxhp = 100000
    bib.crit_stage = 3                    # a critical hit on every roll (Oxide's rate at +3)
    tackle = fs.move("Tackle")
    pl.use_move(b, bib, tackle, cle, True)
    before = cle.maxhp - cle.hp
    pl.use_move(b, cle, fs.move("Lucky Chant"), bib, False)
    pl.use_move(b, bib, tackle, cle, True)
    after = cle.maxhp - cle.hp - before
    ok = before >= int(1.5 * rolls[0]) and after <= rolls[-1] and getattr(b.b, "lucky_chant", 0) == 5
    return [("the readings' Lucky Chant keeps critical hits off its side", ok,
             f"Tackle dealt {before} before the chant and {after} after (row {rolls[0]} to {rolls[-1]})")]


def psych_up_checks():
    """Psych Up in the readings' battle on the calculator's real rows
    (approved 2026-10-14): a trainer's Spoink copies the player's Bibarel's
    Swords Dance, and its stages then weigh in its damage."""
    from .test_fightai import battle
    b = battle([("Spoink", 25, "Thick Fat", ["Psych Up", "Zen Headbutt"])], [("Bibarel", 25, "Unaware", ["Swords Dance"])])
    b.dice, b.rng = pl.RunDice(random.Random(1), True), random.Random(1)
    spo, bib = b.b.cur(), b.p.cur()
    pl.use_move(b, bib, fs.move("Swords Dance"), spo, True)
    pl.use_move(b, spo, fs.move("Psych Up"), bib, False)
    plain = pl.damage_of(b, spo, bib, fs.move("Zen Headbutt"), False, True)
    ok = spo.stages["atk"] == 2 and bib.stages["atk"] == 2
    return [("the readings' Psych Up copies the target's stages", ok,
             f"Spoink's Attack stage {spo.stages['atk']}, Bibarel's {bib.stages['atk']}, Zen Headbutt's top {plain}")]


def lock_on_checks():
    """Lock-On in the readings' battle on the calculator's real rows
    (approved 2026-10-14): a trainer's Magnemite locks on to the player's
    Bibarel at +6 evasion, and its Zap Cannon then hits on dice where it
    would miss; when the Magnemite is switched out the hold ends."""
    from .test_fightai import battle

    class Unlucky(pl.RunDice):
        """Run dice that give the player every piece of luck: the trainer
        misses whenever accuracy is rolled."""
        def good(self, p, kind=None):
            return True
    b = battle([("Magnemite", 25, "Sturdy", ["Lock-On", "Zap Cannon"]), ("Geodude", 25, "Sturdy", ["Tackle"])],
               [("Bibarel", 25, "Unaware", ["Tackle"])])
    b.dice, b.rng = Unlucky(random.Random(1), True), random.Random(1)
    mag, bib = b.b.cur(), b.p.cur()
    bib.hp = bib.maxhp = 100000
    bib.stages["eva"] = 6
    zap = fs.move("Zap Cannon")
    pl.use_move(b, mag, zap, bib, True)
    missed = bib.hp == bib.maxhp
    pl.use_move(b, mag, fs.move("Lock-On"), bib, True)
    held = (getattr(bib, "locked_on", 0), getattr(bib, "lock_on_by", None) == mag.key)
    pl.use_move(b, mag, zap, bib, True)
    hit = bib.hp < bib.maxhp
    fs.switch_in(b, b.b, 1)
    ended = getattr(bib, "locked_on", 0)
    ok = missed and held == (2, True) and hit and ended == 0
    return [("the readings' Lock-On lands the next Zap Cannon, and ends with its user", ok,
             f"missed before {missed}, hold {held}, hit after {hit}, hold after the switch {ended}")]


def foresight_checks():
    """Foresight in the readings' battle on the calculator's real rows
    (approved 2026-10-14): a trainer's Machoke's Karate Chop cannot touch
    the player's Misdreavus until its Foresight lands, and then hits from
    the Misdreavus's twin's row without Ghost."""
    from .test_fightai import battle
    b = battle([("Machoke", 30, "Guts", ["Foresight", "Karate Chop"])], [("Misdreavus", 30, "Levitate", ["Astonish"])])
    b.dice, b.rng = pl.RunDice(random.Random(1), True), random.Random(1)
    mac, mis = b.b.cur(), b.p.cur()
    mis.hp = mis.maxhp = 100000
    chop = fs.move("Karate Chop")
    pl.use_move(b, mac, chop, mis, True)
    before = mis.maxhp - mis.hp
    pl.use_move(b, mac, fs.move("Foresight"), mis, True)
    pl.use_move(b, mac, chop, mis, True)
    after = mis.maxhp - mis.hp - before
    twin = (b.st.get("foresight_twin") or {}).get(mis.key)
    ok = before == 0 and after > 0 and twin is not None
    return [("the readings' Foresight lets a Fighting move hit a Ghost", ok,
             f"Karate Chop dealt {before} before and {after} after; the twin {twin}")]


def trainer_magnitude_checks():
    """A trainer's Magnitude in the readings' battle on the calculator's
    real rows (approved 2026-10-14): a Graveler's Magnitude on the player's
    Machop hits on every use, at the power the battle's dice roll, where
    before it found no row and dealt nothing."""
    from .test_fightai import battle
    b = battle([("Graveler", 30, "Sturdy", ["Magnitude"])], [("Machop", 30, "Guts", ["Karate Chop"])])
    b.dice, b.rng = pl.RunDice(random.Random(1), True), random.Random(1)
    gra, mac = b.b.cur(), b.p.cur()
    mac.hp = mac.maxhp = 10 ** 7
    hits, powers = 0, set()
    for _ in range(200):
        before = mac.hp
        pl.use_move(b, gra, fs.move("Magnitude"), mac, True)
        hits += mac.hp < before
        powers.add(getattr(b, "last_magnitude", None))
    ok = hits >= 180 and powers == set(fs.MAGNITUDE_POWERS)
    return [("the readings' trainer Magnitude hits at its rolled power", ok,
             f"{hits} of 200 uses hit; powers rolled {sorted(p for p in powers if p)}")]


def trainer_return_checks():
    """A trainer's Return on the calculator's real rows (approved
    2026-10-14): a trainer's Pidgeot, at its base friendship of 70, hits the
    player's Bibarel with Return at 28 power, about a third of its Body
    Slam's 85, and the trainer's AI's figure reads the same row."""
    from .test_fightai import battle
    b = battle([("Pidgeot", 30, "Keen Eye", ["Return", "Body Slam"])], [("Bibarel", 30, "Simple", ["Tackle"])])
    pid, bib = b.b.cur(), b.p.cur()
    row = b.st["rows"][(None, pid.key, bib.key)]["moves"]
    ret, slam = row["Return"]["rolls"][-1], row["Body Slam"]["rolls"][-1]
    ai = fightai.figure(b, pid, bib, fs.move("Return"))
    ok = 0.25 < ret / slam < 0.42 and abs(ai - ret) <= 1
    return [("a trainer's Return hits at its friendship's power", ok,
             f"Return's top {ret} against Body Slam's {slam} ({ret / slam:.2f}); the AI's figure {ai}")]


def smack_down_checks():
    """Smack Down in the readings' battle on the calculator's real rows
    (approved 2026-10-14): the player's Nacli's Mud Shot cannot touch a
    trainer's Starly until its Smack Down brings the Starly down, and then
    hits from the Starly's twin's row without Flying; the trainer's AI
    reads the grounding in its type check too."""
    from .test_fightai import battle
    b = battle([("Starly", 25, "Keen Eye", ["Quick Attack"])], [("Nacli", 25, "Purifying Salt", ["Smack Down", "Mud Shot"])])
    b.dice, b.rng = pl.RunDice(random.Random(1), True), random.Random(1)
    sta, nac = b.b.cur(), b.p.cur()
    sta.hp = sta.maxhp = 100000
    shot = fs.move("Mud Shot")
    pl.use_move(b, nac, shot, sta, True)
    before = sta.maxhp - sta.hp
    ai_before = fightai.script_eff(b, nac, sta, shot)
    pl.use_move(b, nac, fs.move("Smack Down"), sta, True)
    mid = sta.maxhp - sta.hp
    pl.use_move(b, nac, shot, sta, True)
    after = sta.maxhp - sta.hp - mid
    ai_after = fightai.script_eff(b, nac, sta, shot)
    ok = before == 0 and getattr(sta, "smacked", False) and after > 0 and ai_before == 0 and ai_after > 0
    return [("the readings' Smack Down lets Ground moves hit a flier", ok,
             f"Mud Shot dealt {before} before and {after} after; the AI's effectiveness {ai_before} then {ai_after}")]


def gravity_checks():
    """Gravity in the readings' battle on the calculator's real rows
    (approved 2026-10-14): a trainer's Clefairy's Mud-Slap cannot touch the
    player's Starly until its Gravity is up, and then hits from the
    Starly's twin's row without Flying; under it the Starly's Fly leaves
    its options, and the trainer's AI reads the grounding in its type
    check."""
    from .test_fightai import battle
    b = battle([("Clefairy", 25, "Cute Charm", ["Gravity", "Mud-Slap"])], [("Starly", 25, "Keen Eye", ["Fly", "Quick Attack"])])
    b.dice, b.rng = pl.RunDice(random.Random(1), True), random.Random(1)
    cle, sta = b.b.cur(), b.p.cur()
    sta.hp = sta.maxhp = 100000
    slap = fs.move("Mud-Slap")
    pl.use_move(b, cle, slap, sta, True)
    before = sta.maxhp - sta.hp
    offered_before = sorted(a[1].name for a in pl.player_actions(b) if a[0] == "move")
    pl.use_move(b, cle, fs.move("Gravity"), sta, True)
    mid = sta.maxhp - sta.hp
    pl.use_move(b, cle, slap, sta, True)
    after = sta.maxhp - sta.hp - mid
    offered = sorted(a[1].name for a in pl.player_actions(b) if a[0] == "move")
    ai = fightai.script_eff(b, cle, sta, slap)
    ok = (before == 0 and getattr(b, "gravity", 0) == 5 and after > 0 and "Fly" in offered_before
          and "Fly" not in offered and ai > 0)
    return [("the readings' Gravity lets Ground moves hit a flier and bars Fly", ok,
             f"Mud-Slap dealt {before} before and {after} after; offered {offered_before} then {offered}; "
             f"the AI's effectiveness {ai}")]


def mimic_checks():
    """Mimic in the readings' battle on the calculator's real rows (approved
    2026-10-14): after the player's Bibarel uses Body Slam, a trainer's Mr.
    Mime's Mimic copies it, and its Body Slam then hits from the Mr. Mime's
    own row, which carries its foes' moves; the trainer's AI may choose it."""
    from .test_fightai import battle
    b = battle([("Mr. Mime", 30, "Soundproof", ["Mimic", "Confusion"])], [("Bibarel", 30, "Simple", ["Body Slam"])])
    b.dice, b.rng = pl.RunDice(random.Random(1), True), random.Random(1)
    mime, bib = b.b.cur(), b.p.cur()
    bib.hp = bib.maxhp = 100000
    pl.use_move(b, bib, fs.move("Body Slam"), mime, True)
    pl.use_move(b, mime, fs.move("Mimic"), bib, False)
    names = [m.name for m in mime.moves]
    slam = next((m for m in mime.moves if m.name == "Body Slam"), None)
    dealt = 0
    if slam is not None:
        pl.use_move(b, mime, slam, bib, True)
        dealt = bib.maxhp - bib.hp
    open_to_ai = slam is not None and not fightai.invalid(b, mime, slam)
    ok = names == ["Body Slam", "Confusion"] and dealt > 0 and mime.pp.get("Body Slam") == 4 and open_to_ai
    return [("the readings' Mimic copies the target's move and uses it", ok,
             f"moves {names}, Body Slam dealt {dealt}, its PP {mime.pp.get('Body Slam')}, open to the AI {open_to_ai}")]


def mirror_move_checks():
    """Mirror Move in the readings' battle on the calculator's real rows
    (approved 2026-10-14): a trainer's Pidgeot's Mirror Move turns the
    player's Bibarel's Body Slam back on it, from the Pidgeot's own row,
    which carries its foes' moves."""
    from .test_fightai import battle
    b = battle([("Pidgeot", 30, "Keen Eye", ["Mirror Move", "Wing Attack"])], [("Bibarel", 30, "Simple", ["Body Slam"])])
    b.dice, b.rng = pl.RunDice(random.Random(1), True), random.Random(1)
    pid, bib = b.b.cur(), b.p.cur()
    bib.hp = bib.maxhp = 100000
    pid.hp = pid.maxhp = 100000
    pl.use_move(b, bib, fs.move("Body Slam"), pid, True)
    pl.use_move(b, pid, fs.move("Mirror Move"), bib, False)
    dealt = bib.maxhp - bib.hp
    row = b.st["rows"][(None, pid.key, bib.key)]["moves"].get("Body Slam", {}).get("rolls")
    ok = row is not None and dealt > 0 and row[0] <= dealt <= int(1.5 * row[-1]) + 1
    return [("the readings' Mirror Move turns the foe's move back on it", ok,
             f"Mirror Move dealt {dealt}; the Pidgeot's Body Slam row {row and (row[0], row[-1])}")]


def copycat_checks():
    """Copycat in the readings' battle on the calculator's real rows
    (approved 2026-10-14): after the player's Bibarel uses Body Slam, a
    trainer's Clefable's Copycat uses it on the Bibarel from the Clefable's
    own row, which carries its foes' moves."""
    from .test_fightai import battle
    b = battle([("Clefable", 30, "Magic Guard", ["Copycat", "Moonblast"])], [("Bibarel", 30, "Simple", ["Body Slam"])])
    b.dice, b.rng = pl.RunDice(random.Random(1), True), random.Random(1)
    cle, bib = b.b.cur(), b.p.cur()
    bib.hp = bib.maxhp = 100000
    cle.hp = cle.maxhp = 100000
    pl.use_move(b, bib, fs.move("Body Slam"), cle, True)
    pl.use_move(b, cle, fs.move("Copycat"), bib, False)
    dealt = bib.maxhp - bib.hp
    row = b.st["rows"][(None, cle.key, bib.key)]["moves"].get("Body Slam", {}).get("rolls")
    ok = b.st.get("copycat") and row is not None and dealt > 0 and row[0] <= dealt <= int(1.5 * row[-1]) + 1
    return [("the readings' Copycat uses the battle's last move", ok,
             f"Copycat dealt {dealt}; the Clefable's Body Slam row {row and (row[0], row[-1])}")]


def fling_checks():
    """Fling in the readings' battle on the calculator's real rows (approved
    2026-10-14): the player's Bibarel throws its Hard Stone (handed to the
    player by Roark's split) at a trainer's Machop from its twin's row at
    100 power, where its own item-free row read nothing; the Machop throws
    a Sitrus Berry, which the Bibarel eats, healing a quarter of its HP."""
    from .test_fightai import battle
    b = battle([("Machop", 30, "Guts", ["Fling"], "Sitrus Berry")], [("Bibarel", 30, "Simple", ["Fling"], "Hard Stone")])
    b.dice, b.rng = pl.RunDice(random.Random(1), True), random.Random(1)
    b.dice.one_crit = False
    mac, bib = b.b.cur(), b.p.cur()
    mac.hp = mac.maxhp = 100000
    pl.use_move(b, bib, fs.move("Fling"), mac, True)
    thrown = (mac.maxhp - mac.hp, bib.item)
    bib.hp = bib.maxhp // 2
    before = bib.hp
    pl.use_move(b, mac, fs.move("Fling"), bib, True)
    row = b.st["rows"][(None, mac.key, bib.key)]["moves"]["Fling"]["rolls"]
    net = bib.hp - before
    healed = fs.engine_divide(bib.maxhp * 25, 100)
    ok = thrown[0] > 0 and thrown[1] is None and healed - int(1.5 * row[-1]) - 1 <= net <= healed - row[0] + 1
    return [("the readings' Fling throws the player's item at its power, and a thrown Berry is eaten", ok,
             f"Hard Stone dealt {thrown[0]}; the Sitrus Berry's hit and heal came to {net} (heal {healed}, row "
             f"{row[0]} to {row[-1]})")]


def natural_gift_checks():
    """Natural Gift in the readings' battle on the calculator's real rows
    (approved 2026-10-14): the player's Donphan holding a Sitrus Berry hits
    a trainer's Roserade with a Psychic Natural Gift from its twin's row and
    spends the Berry."""
    from .test_fightai import battle
    b = battle([("Roserade", 30, "Natural Cure", ["Tackle"])], [("Donphan", 30, "Sturdy", ["Natural Gift"], "Sitrus Berry")])
    b.dice, b.rng = pl.RunDice(random.Random(1), True), random.Random(1)
    ros, don = b.b.cur(), b.p.cur()
    row = b.st["rows"].get((None, f"{don.key}#ng", ros.key), {}).get("moves", {}).get("Natural Gift", {})
    pl.use_move(b, don, fs.move("Natural Gift"), ros, True)
    got = (bool(row.get("rolls")), ros.hp < ros.maxhp, don.item)
    return [("the readings' Natural Gift hits for the player's Sitrus Berry holder", got == (True, True, None),
             f"(twin row, hit, Donphan's item after) {got}")]


def imprison_checks():
    """Imprison in the readings' battle on the calculator's real rows
    (approved 2026-10-14): Mars's Bronzor imprisons against the player's
    Kadabra, which shares Confusion with it; Confusion then drops out of the
    player's options and the trainer's Basic scores a second Imprison -10."""
    from .test_fightai import battle
    b = battle([("Bronzor", 30, "Levitate", ["Imprison", "Confusion", "Hypnosis", "Confuse Ray"])],
               [("Kadabra", 30, "Synchronize", ["Confusion", "Shadow Ball"])])
    b.dice, b.rng = pl.RunDice(random.Random(1), True), random.Random(1)
    bron, kad = b.b.cur(), b.p.cur()
    before = sorted(a[1].name for a in pl.player_actions(b) if a[0] == "move")
    pl.use_move(b, bron, fs.move("Imprison"), kad, True)
    after = sorted(a[1].name for a in pl.player_actions(b) if a[0] == "move")
    again = fightai.basic(b, bron, kad, fs.move("Imprison"), 0)
    got = (before, after, again)
    return [("the readings' Imprison takes the shared Confusion from the player's options", got ==
             (["Confusion", "Shadow Ball"], ["Shadow Ball"], -10), f"(options before, after, a second Imprison) {got}")]


def baton_pass_checks():
    """Baton Pass in a whole turn of the readings' battle on the
    calculator's real rows (approved 2026-10-14): a trainer's Ninjask at +2
    Speed and +1 Attack Baton Passes, the trainer's AI sends in its Scizor
    with both stages, and the player's Staraptor's Close Combat, moving
    after, hits the Scizor rather than the Ninjask."""
    from .test_fightai import battle
    b = battle([("Ninjask", 40, "Speed Boost", ["Baton Pass"]), ("Scizor", 40, "Technician", ["Bullet Punch"])],
               [("Staraptor", 40, "Reckless", ["Close Combat"])])
    b.dice, b.rng = pl.RunDice(random.Random(1), True), random.Random(1)
    nin = b.b.cur()
    nin.stages.update(spe=2, atk=1)
    pl._turn(b, ("move", fs.move("Close Combat")), ("move", fs.move("Baton Pass")))
    new = b.b.cur()
    got = (new.species, new.stages["spe"], new.stages["atk"], new.hp < new.maxhp, nin.hp == nin.maxhp)
    return [("the readings' Baton Pass sends in the replacement with the stages", got ==
             ("Scizor", 2 + (new.ability == "Speed Boost"), 1, True, True),
             f"(newcomer, Speed stage, Attack stage, newcomer hit, Ninjask untouched) {got}")]


def row_neutral_checks():
    """The abilities a changed-ability twin need not carry (fightsim.ROW_NEUTRAL)
    on the calculator's real rows (2026-10-14): a Pokemon with each of them,
    every one that some species has, reads exactly the rows and Speed of the
    same Pokemon with the stand-in, both ways, over single-hit moves of
    every kind (physical and special, contact and not, a sound move, a punch,
    Fire, Water, Grass, Bug, Ground and Electric) at full HP, no status and
    no stages. So a change between them, or to or from the stand-in, needs
    no twin. And a fight with a Mummy holder twins only the holder's foes
    with a contact move, not its partners."""
    blob = fs.calc.blob()
    have = {a for p in blob["poks"].values() for a in (p.get("abilities") or {}).values() if a}
    neutral = sorted(fs.ROW_NEUTRAL & have)
    moves = ["Flamethrower", "Surf", "Energy Ball", "X-Scissor", "Earthquake", "Thunder Punch", "Hyper Voice",
             "Body Slam", "Aqua Jet"]

    def rec(ab, i):
        return {"constant": "SPECIES_SNORLAX", "species": "Snorlax", "how": "test", "level": 30, "nature": "Hardy",
                "ivs": IV, "evs": EV, "ability": ab, "moves": moves, "fill": False, "label": f"Snorlax {i}"}
    side = [rec(fs.WEATHER_STAND_IN, 0)] + [rec(ab, i + 1) for i, ab in enumerate(neutral)]
    foe = {"species": "Machamp", "level": 30, "ability": "No Guard", "item": None, "nature": "Hardy", "ivs": IV,
           "evs": EV, "moves": moves}
    st = fs.prepare("Fantina", [[foe]], None, given_side=side)
    rows, speed = st["rows"], st["speed"]

    def rolls(a, d):
        return {m: tuple(r.get("rolls") or ()) for m, r in rows[(None, a, d)]["moves"].items()}
    differ = [ab for i, ab in enumerate(neutral, 1)
              if rolls(f"p{i}", "b0.0") != rolls("p0", "b0.0") or rolls("b0.0", f"p{i}") != rolls("b0.0", "p0")
              or speed[(None, f"p{i}")] != speed[(None, "p0")]]
    from .test_fightai import battle
    b = battle([("Cofagrigus", 40, "Mummy", ["Hex"]), ("Hitmonchan", 40, "Iron Fist", ["Mach Punch"])],
               [("Azumarill", 40, "Huge Power", ["Aqua Tail"])])
    twinned = sorted(b.st.get("form_twin") or {})
    ok = len(neutral) >= 25 and differ == [] and twinned == ["p0"]
    return [("the abilities twins need not carry change no row, and Mummy twins only its holder's contact foes", ok,
             f"{len(neutral)} abilities checked, differing {differ}; twinned in a Mummy fight {twinned}")]


def calc_terrain(tr_ids):
    from . import calc
    return getattr(calc, "fight_terrain", lambda _ids: None)(tr_ids)


def sleep_talk_and_aqua_ring_checks():
    """Sleep Talk used asleep calls one of its user's other moves (the AI now
    scores it +10 asleep, as the game does), and one that calls Rest does
    nothing, as Rest fails on a sleeping user (2026-10-13); Aqua Ring heals a
    sixteenth at each turn's end (the Scoring Agent, 2026-10-01)."""
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
    # Rest fails on a sleeping user (approved 2026-10-13), so in the
    # readings' battle a Sleep Talk that calls it leaves Snorlax's HP alone.
    b = battle([("Snorlax", 40, "Thick Fat", ["Sleep Talk", "Rest"])], [("Machop", 40, "Guts", ["Cross Chop"])])
    lax, champ = b.b.cur(), b.p.cur()
    seen = set()
    for seed in range(20):
        b.rng, b.dice = random.Random(seed), pl.RunDice(random.Random(seed), True)
        lax.hp, lax.status, lax.sleep = lax.maxhp // 2, "slp", 3
        pl.use_move(b, lax, fs.move("Sleep Talk"), champ, True)
        seen.add((lax.hp == lax.maxhp // 2, lax.sleep))
    out.append(("search: a Sleep Talk that calls Rest leaves the sleeper's HP and sleep running down",
                seen == {(True, 2)}, f"(HP unchanged, sleep left) {sorted(seen)}"))
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


def refresh_checks():
    """Refresh in the readings' battle on the calculator's real rows
    (approved 2026-10-14): a trainer's paralysed Altaria's Refresh cures
    its paralysis, and its sleeping Swablu on the bench sleeps on, where
    before the Swablu woke too."""
    from .test_fightai import battle
    b = battle([("Altaria", 40, "Natural Cure", ["Refresh", "Peck"]), ("Swablu", 40, "Natural Cure", ["Peck"])],
               [("Bibarel", 40, "Simple", ["Tackle"])])
    b.dice, b.rng = pl.RunDice(random.Random(1), True), random.Random(1)
    alt, swa, bib = b.b.mons[0], b.b.mons[1], b.p.cur()
    alt.status, swa.status, swa.sleep = "par", "slp", 3
    pl.status_move(b, alt, fs.move("Refresh"), bib, True)
    ok = alt.status is None and swa.status == "slp"
    return [("the readings' Refresh cures only its user", ok, f"Altaria {alt.status}, Swablu {swa.status}")]


def wring_out_checks():
    """Wring Out in the readings' battle on the calculator's real rows
    (approved 2026-10-14): a trainer's Tentacruel's Wring Out on the
    player's Bibarel at half HP hits about half as hard as at full HP (61
    power against 121), where before it hit alike at both."""
    from .test_fightai import battle
    b = battle([("Tentacruel", 40, "Clear Body", ["Wring Out"])], [("Bibarel", 40, "Simple", ["Tackle"])])
    ten, bib = b.b.cur(), b.p.cur()
    mv = fs.move("Wring Out")
    full = b.damage(ten, bib, mv, roll=15)
    bib.hp = bib.maxhp // 2
    half = b.damage(ten, bib, mv, roll=15)
    ok = full > 0 and 0.45 < half / full < 0.55
    return [("the readings' Wring Out hits by its target's HP left", ok, f"full HP {full}, half HP {half}")]


def miracle_eye_checks():
    """Miracle Eye in the readings' battle on the calculator's real rows
    (approved 2026-10-14): a trainer's Kadabra's Psybeam cannot touch the
    player's Poochyena until its Miracle Eye lands, and then hits from the
    Poochyena's twin's row without Dark."""
    from .test_fightai import battle
    b = battle([("Kadabra", 30, "Synchronize", ["Miracle Eye", "Psybeam"])], [("Poochyena", 30, "Run Away", ["Bite"])])
    b.dice, b.rng = pl.RunDice(random.Random(1), True), random.Random(1)
    kad, poo = b.b.cur(), b.p.cur()
    poo.hp = poo.maxhp = 100000
    beam = fs.move("Psybeam")
    pl.use_move(b, kad, beam, poo, True)
    before = poo.maxhp - poo.hp
    pl.use_move(b, kad, fs.move("Miracle Eye"), poo, True)
    pl.use_move(b, kad, beam, poo, True)
    after = poo.maxhp - poo.hp - before
    twin = (b.st.get("miracle_twin") or {}).get(poo.key)
    ok = before == 0 and after > 0 and twin is not None
    return [("the readings' Miracle Eye lets a Psychic move hit a Dark type", ok,
             f"Psybeam dealt {before} before and {after} after; the twin {twin}")]


def acupressure_checks():
    """Acupressure in the readings' battle on the calculator's real rows
    (approved 2026-10-14): each use of a trainer's Dodrio's Acupressure
    raises one of its seven stats by two stages, drawn by the battle's
    dice, and over forty uses from a fresh start every stat is drawn."""
    from .test_fightai import battle
    b = battle([("Dodrio", 30, "Early Bird", ["Acupressure", "Peck"])], [("Bibarel", 30, "Simple", ["Tackle"])])
    b.dice, b.rng = pl.RunDice(random.Random(1), True), random.Random(1)
    dod, bib = b.b.cur(), b.p.cur()
    drawn, each = set(), True
    for _ in range(40):
        dod.stages = dict.fromkeys(fs.STAGE_KEYS, 0)
        pl.status_move(b, dod, fs.move("Acupressure"), bib, True)
        up = {k: v for k, v in dod.stages.items() if v}
        each = each and len(up) == 1 and set(up.values()) == {2}
        drawn |= set(up)
    ok = each and drawn == set(fs.STAGE_KEYS)
    return [("the readings' Acupressure raises one stat by two", ok, f"each use one stat by two {each}; drawn {sorted(drawn)}")]


def trainer_frustration_checks():
    """A trainer's Frustration on the calculator's real rows (approved
    2026-10-14): a trainer's Raticate, at its base friendship of 70, hits
    the player's Bibarel with Frustration at 74 power, under its Body
    Slam's 85, where the calculator's zero-friendship 102 hit harder; and
    the trainer's AI's figure reads the same row."""
    from .test_fightai import battle
    b = battle([("Raticate", 30, "Guts", ["Frustration", "Body Slam"])], [("Bibarel", 30, "Simple", ["Tackle"])])
    rat, bib = b.b.cur(), b.p.cur()
    row = b.st["rows"][(None, rat.key, bib.key)]["moves"]
    fru, slam = row["Frustration"]["rolls"][-1], row["Body Slam"]["rolls"][-1]
    ai = fightai.figure(b, rat, bib, fs.move("Frustration"))
    ok = 0.78 < fru / slam < 0.96 and abs(ai - fru) <= 1
    return [("a trainer's Frustration hits at its friendship's power", ok,
             f"Frustration's top {fru} against Body Slam's {slam} ({fru / slam:.2f}); the AI's figure {ai}")]


def secret_power_checks():
    """Secret Power in the readings' battle on the calculator's real rows
    (approved 2026-10-14): on plain ground (trainer 1's Route 202) a
    trainer's Zigzagoon's Secret Power lowers the player's Bibarel's
    accuracy about three times in ten, and in a building it paralyses."""
    from .test_fightai import battle
    out = {}
    for terrain in ("TERRAIN_PLAIN", "TERRAIN_BUILDING"):
        b = battle([("Zigzagoon", 20, "Pickup", ["Secret Power"])], [("Bibarel", 20, "Unaware", ["Tackle"])])
        b.st = dict(b.st, terrain=terrain)
        b.dice, b.rng = pl.RunDice(random.Random(1), True), random.Random(1)
        zig, bib = b.b.cur(), b.p.cur()
        bib.hp = bib.maxhp = 100000
        n = 0
        for _ in range(100):
            bib.stages["acc"], bib.status = 0, None
            pl.attack(b, zig, fs.move("Secret Power"), bib, True)
            n += bib.stages["acc"] == -1 if terrain == "TERRAIN_PLAIN" else bib.status == "par"
        out[terrain] = n
    ok = all(15 <= n <= 45 for n in out.values())
    return [("the readings' Secret Power adds its terrain's effect", ok, f"of 100 hits, effects landed {out}")]


def snore_checks():
    """Snore in the readings' battle on the calculator's real rows (approved
    2026-10-14): a trainer's sleeping Whiscash's Snore hits the player's
    Bibarel and flinches it about three times in ten, and an awake one's
    Snore fails."""
    from .test_fightai import battle
    b = battle([("Whiscash", 30, "Oblivious", ["Snore"])], [("Bibarel", 30, "Unaware", ["Tackle"])])
    b.dice, b.rng = pl.RunDice(random.Random(1), True), random.Random(1)
    whi, bib = b.b.cur(), b.p.cur()
    bib.hp = bib.maxhp = 100000
    flinches = 0
    for _ in range(100):
        whi.status, whi.sleep, bib.flinch = "slp", 3, False
        pl.attack(b, whi, fs.move("Snore"), bib, True)
        flinches += bib.flinch
    asleep = bib.maxhp - bib.hp
    whi.status, whi.sleep = None, 0
    before = bib.hp
    pl.attack(b, whi, fs.move("Snore"), bib, True)
    ok = asleep > 0 and 15 <= flinches <= 45 and bib.hp == before
    return [("the readings' Snore flinches asleep and fails awake", ok,
             f"100 sleeping Snores dealt {asleep}, flinched {flinches}; awake it dealt {before - bib.hp}")]


def raise_speed_hit_checks():
    """Trailblaze in the readings' battle on the calculator's real rows
    (approved 2026-10-14): a trainer's Pikachu's Trailblaze on the player's
    Bibarel raises its Speed a stage each hit, three hits three stages."""
    from .test_fightai import battle
    b = battle([("Pikachu", 30, "Static", ["Trailblaze"])], [("Bibarel", 30, "Unaware", ["Tackle"])])
    b.dice, b.rng = pl.RunDice(random.Random(1), True), random.Random(1)
    pik, bib = b.b.cur(), b.p.cur()
    bib.hp = bib.maxhp = 100000
    for _ in range(3):
        pl.attack(b, pik, fs.move("Trailblaze"), bib, True)
    ok = bib.hp < bib.maxhp and pik.stages["spe"] == 3
    return [("the readings' Trailblaze raises its user's Speed", ok, f"Speed stage {pik.stages['spe']} after three hits")]


def trump_card_checks():
    """Trump Card in the readings' battle on the calculator's real rows
    (approved 2026-10-14): a trainer's Minun's five Trump Cards on the
    player's Bibarel hit harder as its PP runs down, the last at five times
    the first (200 power against 40)."""
    from .test_fightai import battle
    b = battle([("Minun", 40, "Minus", ["Trump Card"])], [("Bibarel", 40, "Unaware", ["Tackle"])])
    b.dice, b.rng = pl.RunDice(random.Random(1), True), random.Random(1)
    minun, bib = b.b.cur(), b.p.cur()
    bib.hp = bib.maxhp = 100000
    dealt = []
    for _ in range(5):
        before = bib.hp
        pl.use_move(b, minun, fs.move("Trump Card"), bib, True)
        dealt.append(before - bib.hp)
    ok = all(x < y for x, y in zip(dealt, dealt[1:])) and 4 <= dealt[-1] / dealt[0] <= 6
    return [("the readings' Trump Card rises as its PP runs down", ok, f"damage by use {dealt}")]


def teeter_dance_checks():
    """Teeter Dance in the readings' battle on the calculator's real rows
    (approved 2026-10-14): a trainer's Spinda's Teeter Dance confuses the
    player's Bibarel, where before it did nothing."""
    from .test_fightai import battle
    b = battle([("Spinda", 30, "Tangled Feet", ["Teeter Dance"])], [("Bibarel", 30, "Unaware", ["Tackle"])])
    b.dice, b.rng = pl.RunDice(random.Random(1), True), random.Random(1)
    spi, bib = b.b.cur(), b.p.cur()
    pl.status_move(b, spi, fs.move("Teeter Dance"), bib, True)
    return [("the readings' Teeter Dance confuses its target", bool(bib.confused), f"Bibarel confused {bib.confused}")]


def smelling_salts_checks():
    """Smelling Salts in the readings' battle on the calculator's real rows
    (approved 2026-10-14): a trainer's Makuhita's Smelling Salts on the
    player's paralysed Bibarel hits twice as hard as on a healthy one, and
    cures the paralysis."""
    from .test_fightai import battle

    class Top(pl.RunDice):
        """Run dice that roll the top damage, never miss and never crit."""
        def roll(self, top):
            return 15

        def bad(self, kind, p):
            return False

        def good(self, p, kind=None):
            return False
    b = battle([("Makuhita", 30, "Thick Fat", ["Smelling Salts"])], [("Bibarel", 30, "Unaware", ["Tackle"])])
    b.dice, b.rng = Top(random.Random(1), True), random.Random(1)
    mak, bib = b.b.cur(), b.p.cur()
    bib.hp = bib.maxhp = 100000
    mv = fs.move("Smelling Salts")
    pl.attack(b, mak, mv, bib, True)
    plain = bib.maxhp - bib.hp
    bib.status, bib.hp = "par", bib.maxhp
    pl.attack(b, mak, mv, bib, True)
    salted = bib.maxhp - bib.hp
    ok = plain > 0 and salted == 2 * plain and bib.status is None
    return [("the readings' Smelling Salts doubles on paralysis and cures it", ok,
             f"healthy {plain}, paralysed {salted}, the status after {bib.status}")]


def magic_coat_checks():
    """Magic Coat in the readings' battle on the calculator's real rows
    (approved 2026-10-14): a trainer's Spoink's Magic Coat turns the
    player's Thunder Wave back, paralysing the player's Bibarel; a
    trainer's Spoink that has not used it is paralysed."""
    from .test_fightai import battle
    out = {}
    for coat in (True, False):
        b = battle([("Spoink", 30, "Thick Fat", ["Magic Coat", "Psybeam"])], [("Bibarel", 30, "Unaware", ["Thunder Wave"])])
        b.dice, b.rng = pl.RunDice(random.Random(1), True), random.Random(1)
        spo, bib = b.b.cur(), b.p.cur()
        if coat:
            pl.status_move(b, spo, fs.move("Magic Coat"), bib, True)
        pl.status_move(b, bib, fs.move("Thunder Wave"), spo, False)
        out["coat" if coat else "no coat"] = (bib.status, spo.status)
    ok = out == {"coat": ("par", None), "no coat": (None, "par")}
    return [("the readings' Magic Coat turns a status move back", ok, f"(Bibarel, Spoink) {out}")]


def present_checks():
    """Present in the readings' battle on the calculator's real rows
    (approved 2026-10-14): of 300 uses of a trainer's Delibird's Present on
    the player's Bibarel, about a fifth heal it a quarter and the rest hit
    at three tiers of damage, where before the move found no row and did
    nothing."""
    from .test_fightai import battle

    class Sure(pl.RunDice):
        """Run dice where the trainer never misses or lands a critical hit."""
        def good(self, p, kind=None):
            return False
    b = battle([("Delibird", 30, "Hustle", ["Present"])], [("Bibarel", 30, "Unaware", ["Tackle"])])
    b.dice, b.rng = Sure(random.Random(1), True), random.Random(1)
    deli, bib = b.b.cur(), b.p.cur()
    bib.maxhp = 100000
    heals, tiers = 0, set()
    for _ in range(300):
        bib.hp = bib.maxhp // 2
        pl.attack(b, deli, fs.move("Present"), bib, True)
        if bib.hp > bib.maxhp // 2:
            heals += 1
        elif bib.hp < bib.maxhp // 2:
            tiers.add((bib.maxhp // 2 - bib.hp) // 10)
    ok = 40 <= heals <= 85 and len(tiers) >= 3
    return [("the readings' Present hits at its rolled power or heals", ok,
             f"{heals} heals in 300; damage bands seen {sorted(tiers)}")]


def water_sport_checks():
    """Water Sport in the readings' battle on the calculator's real rows
    (approved 2026-10-14): after a trainer's Budew's Water Sport the
    player's Charmander's Ember hits it half as hard, and so does the
    trainer's AI's figure of a Fire move."""
    from .test_fightai import battle
    b = battle([("Budew", 26, "Natural Cure", ["Water Sport", "Absorb"])], [("Charmander", 26, "Blaze", ["Ember"])])
    b.dice, b.rng = pl.RunDice(random.Random(1), True), random.Random(1)
    bud, cha = b.b.cur(), b.p.cur()
    ember = fs.move("Ember")
    before = b.damage(cha, bud, ember, roll=15)
    pl.status_move(b, bud, fs.move("Water Sport"), cha, True)
    after = b.damage(cha, bud, ember, roll=15)
    ok = before > 0 and abs(after - before / 2) <= 1 and bud.water_sport
    return [("the readings' Water Sport halves Fire moves", ok, f"Ember's top roll {before} before, {after} after")]


def acrobatics_checks():
    """Acrobatics in the readings' battle on the calculator's real rows
    (approved 2026-10-14): a trainer's Emolga with no item hits the
    player's Bibarel twice as hard as one holding an Oran Berry."""
    from .test_fightai import battle

    class Top(pl.RunDice):
        """Run dice that roll the top damage, never miss and never crit."""
        def roll(self, top):
            return 15

        def bad(self, kind, p):
            return False

        def good(self, p, kind=None):
            return False
    out = {}
    for item in (None, "Oran Berry"):
        b = battle([("Emolga", 28, "Static", ["Acrobatics"])], [("Bibarel", 28, "Unaware", ["Tackle"])])
        b.dice, b.rng = Top(random.Random(1), True), random.Random(1)
        emo, bib = b.b.cur(), b.p.cur()
        emo.item = item
        bib.hp = bib.maxhp = 100000
        pl.attack(b, emo, fs.move("Acrobatics"), bib, True)
        out[item] = bib.maxhp - bib.hp
    ok = out["Oran Berry"] > 0 and out[None] == 2 * out["Oran Berry"]
    return [("the readings' Acrobatics doubles without an item", ok, str(out))]


def guard_swap_checks():
    """Guard Swap in the readings' battle on the calculator's real rows
    (approved 2026-10-14): a trainer's Xatu takes the player's Bibarel's
    two Defense stages from its Defense Curls and gives back its own
    none."""
    from .test_fightai import battle
    b = battle([("Xatu", 40, "Synchronize", ["Guard Swap", "Psychic"])], [("Bibarel", 40, "Unaware", ["Defense Curl"])])
    b.dice, b.rng = pl.RunDice(random.Random(1), True), random.Random(1)
    xatu, bib = b.b.cur(), b.p.cur()
    bib.stages["def"] = 2
    pl.status_move(b, xatu, fs.move("Guard Swap"), bib, True)
    ok = xatu.stages["def"] == 2 and bib.stages["def"] == 0
    return [("the readings' Guard Swap swaps the defensive stages", ok,
             f"Xatu's Defense stage {xatu.stages['def']}, Bibarel's {bib.stages['def']}")]


def power_swap_checks():
    """Power Swap in the readings' battle on the calculator's real rows
    (approved 2026-10-14): a trainer's Xatu takes the player's Bibarel's
    +2 Attack and gives it its own -1."""
    from .test_fightai import battle
    b = battle([("Xatu", 40, "Synchronize", ["Power Swap", "Psychic"])], [("Bibarel", 40, "Unaware", ["Swords Dance"])])
    b.dice, b.rng = pl.RunDice(random.Random(1), True), random.Random(1)
    xatu, bib = b.b.cur(), b.p.cur()
    bib.stages["atk"], xatu.stages["atk"] = 2, -1
    pl.status_move(b, xatu, fs.move("Power Swap"), bib, True)
    ok = xatu.stages["atk"] == 2 and bib.stages["atk"] == -1
    return [("the readings' Power Swap swaps the attacking stages", ok,
             f"Xatu's Attack stage {xatu.stages['atk']}, Bibarel's {bib.stages['atk']}")]


def psycho_shift_checks():
    """Psycho Shift in the readings' battle on the calculator's real rows
    (approved 2026-10-14): a trainer's burned Noctowl's Psycho Shift burns
    the player's Bibarel and cures the Noctowl."""
    from .test_fightai import battle
    b = battle([("Noctowl", 40, "Insomnia", ["Psycho Shift", "Extrasensory"])], [("Bibarel", 40, "Unaware", ["Tackle"])])
    b.dice, b.rng = pl.RunDice(random.Random(1), True), random.Random(1)
    noc, bib = b.b.cur(), b.p.cur()
    noc.status = "brn"
    pl.status_move(b, noc, fs.move("Psycho Shift"), bib, True)
    ok = noc.status is None and bib.status == "brn"
    return [("the readings' Psycho Shift hands its user's status on", ok, f"Noctowl {noc.status}, Bibarel {bib.status}")]


def memento_checks():
    """Memento in the readings' battle on the calculator's real rows
    (approved 2026-10-14): a trainer's Jumpluff's Memento into the player's
    Bibarel behind a Substitute faints the Jumpluff and lowers nothing,
    and into a protecting Bibarel still faints it."""
    from .test_fightai import battle
    out = {}
    for setup in ("sub", "protect"):
        b = battle([("Jumpluff", 40, "Chlorophyll", ["Memento"])], [("Bibarel", 40, "Unaware", ["Substitute", "Protect"])])
        b.dice, b.rng = pl.RunDice(random.Random(1), True), random.Random(1)
        jum, bib = b.b.cur(), b.p.cur()
        bib.sub = bib.maxhp // 4 if setup == "sub" else 0
        bib.protecting = setup == "protect"
        pl.status_move(b, jum, fs.move("Memento"), bib, True)
        out[setup] = (jum.hp, bib.stages["atk"], bib.stages["spa"])
    ok = out == {"sub": (0, 0, 0), "protect": (0, 0, 0)}
    return [("the readings' Memento faints its user and meets a Substitute", ok,
             f"(Jumpluff's HP, Bibarel's Attack and Sp. Atk) {out}")]


def sketch_checks():
    """Sketch in the readings' battle on the calculator's real rows (approved
    2026-10-14): a trainer's Smeargle sketches the player's Bibarel's Body
    Slam, hits with it from its own row, keeps it after leaving, and the
    trainer's AI can figure it."""
    from .test_fightai import battle
    b = battle([("Smeargle", 30, "Own Tempo", ["Sketch"])], [("Bibarel", 30, "Unaware", ["Body Slam"])])
    b.dice, b.rng = pl.RunDice(random.Random(1), True), random.Random(1)
    sme, bib = b.b.cur(), b.p.cur()
    bib.hp = bib.maxhp = 100000
    pl.use_move(b, bib, fs.move("Body Slam"), sme, False)
    sme.hp = sme.maxhp
    pl.use_move(b, sme, fs.move("Sketch"), bib, False)
    slam = next((m for m in sme.moves if m.name == "Body Slam"), None)
    dealt = 0
    if slam is not None:
        before = bib.hp
        pl.use_move(b, sme, slam, bib, True)
        dealt = before - bib.hp
    figure = fightai.figure(b, sme, bib, slam) if slam is not None else None
    sme.reset_volatile()
    ok = slam is not None and dealt > 0 and bool(figure) and any(m.name == "Body Slam" for m in sme.moves)
    return [("the readings' Sketch takes the target's last move for good", ok,
             f"Smeargle's moves {[m.name for m in sme.moves]}; Body Slam dealt {dealt}, the AI's figure {figure}")]


def me_first_checks():
    """Me First in the readings' battle on the calculator's real rows
    (approved 2026-10-14): a trainer's Furret moving first takes the
    player's Bibarel's chosen Body Slam and hits with it at half again
    what its own Body Slam row gives."""
    from .test_fightai import battle

    class Top(pl.RunDice):
        """Run dice that roll the top damage, never miss and never crit."""
        def roll(self, top):
            return 15

        def bad(self, kind, p):
            return False

        def good(self, p, kind=None):
            return False
    b = battle([("Furret", 40, "Keen Eye", ["Me First"])], [("Bibarel", 40, "Unaware", ["Body Slam"])])
    b.dice, b.rng = Top(random.Random(1), True), random.Random(1)
    fur, bib = b.b.cur(), b.p.cur()
    bib.hp = bib.maxhp = 100000
    bib.chosen = fs.move("Body Slam")
    pl.use_move(b, fur, fs.move("Me First"), bib, True)
    taken = bib.maxhp - bib.hp
    bib.hp = bib.maxhp
    pl.attack(b, fur, fs.move("Body Slam"), bib, True)
    plain = bib.maxhp - bib.hp
    ok = plain > 0 and abs(taken - plain * 1.5) <= 1
    return [("the readings' Me First takes the target's chosen hit at half again", ok,
             f"Me First's Body Slam {taken}, a plain one {plain}")]


def nature_power_checks():
    """Nature Power in the readings' battle on the calculator's real rows
    (approved 2026-10-14): where the fight names no terrain, a trainer's
    Ludicolo's Nature Power turns into Tri Attack and hits the player's
    Bibarel from its own row, where before it did nothing."""
    from .test_fightai import battle
    b = battle([("Ludicolo", 40, "Swift Swim", ["Nature Power"])], [("Bibarel", 40, "Unaware", ["Tackle"])])
    b.dice, b.rng = pl.RunDice(random.Random(1), True), random.Random(1)
    lud, bib = b.b.cur(), b.p.cur()
    bib.hp = bib.maxhp = 100000
    rowed = "Tri Attack" in b.st["rows"][(None, lud.key, bib.key)]["moves"]
    pl.use_move(b, lud, fs.move("Nature Power"), bib, True)
    ok = rowed and bib.hp < bib.maxhp
    return [("the readings' Nature Power uses its terrain's move", ok,
             f"Tri Attack rowed {rowed}; it dealt {bib.maxhp - bib.hp}")]


def power_trick_checks():
    """Power Trick in the readings' battle on the calculator's real rows
    (approved 2026-10-14): once the player's Shuckle swaps its feeble
    Attack for its great Defense, its Rollout hits a trainer's Geodude far
    harder and the Geodude's Tackle hurts it far more."""
    from .test_fightai import battle
    b = battle([("Geodude", 30, "Sturdy", ["Tackle"])], [("Shuckle", 30, "Sturdy", ["Power Trick", "Rollout"])])
    b.dice, b.rng = pl.RunDice(random.Random(1), True), random.Random(1)
    geo, shu = b.b.cur(), b.p.cur()
    roll, tackle = fs.move("Rollout"), fs.move("Tackle")
    before = (b.damage(shu, geo, roll, roll=15), b.damage(geo, shu, tackle, roll=15))
    pl.status_move(b, shu, fs.move("Power Trick"), geo, True)
    after = (b.damage(shu, geo, roll, roll=15), b.damage(geo, shu, tackle, roll=15))
    ok = after[0] > 2 * before[0] and after[1] > 2 * before[1]
    return [("the readings' Power Trick swaps its user's Attack and Defense", ok,
             f"(Rollout, Tackle into it) before {before}, after {after}")]


def bide_checks():
    """Bide in the readings' battle on the calculator's real rows (approved
    2026-10-14): a trainer's Miltank's Bide stores the two Tackles the
    player's Bibarel lands and gives back twice their HP, where before it
    did nothing."""
    from .test_fightai import battle

    class Sure(pl.RunDice):
        """Run dice where nobody misses or lands a critical hit."""
        def bad(self, kind, p):
            return False

        def good(self, p, kind=None):
            return False
    b = battle([("Miltank", 30, "Thick Fat", ["Bide"])], [("Bibarel", 30, "Unaware", ["Tackle"])])
    b.dice, b.rng = Sure(random.Random(1), True), random.Random(1)
    mil, bib = b.b.cur(), b.p.cur()
    mil.hp = mil.maxhp = bib.hp = bib.maxhp = 100000
    bide, tackle = fs.move("Bide"), fs.move("Tackle")
    taken = 0
    for turn in range(3):
        pl.use_move(b, mil, mil.lock[0] if mil.lock else bide, bib, True)
        if turn < 2:
            before = mil.hp
            pl.use_move(b, bib, tackle, mil, False)
            taken += before - mil.hp
    given = bib.maxhp - bib.hp
    ok = taken > 0 and given == 2 * taken
    return [("the readings' Bide gives back twice what it stored", ok, f"stored {taken}, gave back {given}")]


def transform_checks():
    """Transform in the readings' battle on the calculator's real rows
    (approved 2026-10-14, the cheap part): a trainer's Ditto turns into
    the player's Bibarel, its moves at 5 PP, its types and ability, and its
    copied Growl lowers the Bibarel's Attack, where before Transform did
    nothing."""
    from .test_fightai import battle
    b = battle([("Ditto", 30, "Limber", ["Transform"])], [("Bibarel", 30, "Unaware", ["Growl", "Tackle"])])
    b.dice, b.rng = pl.RunDice(random.Random(1), True), random.Random(1)
    dit, bib = b.b.cur(), b.p.cur()
    pl.use_move(b, dit, fs.move("Transform"), bib, True)
    copied = ([m.name for m in dit.moves], dict(dit.pp), dit.types == bib.types, dit.ability)
    growl = next((m for m in dit.moves if m.name == "Growl"), None)
    if growl is not None:
        pl.use_move(b, dit, growl, bib, True)
    ok = copied == (["Growl", "Tackle"], {"Growl": 5, "Tackle": 5}, True, "Unaware") and bib.stages["atk"] == -1
    return [("the readings' Transform copies its target", ok, f"{copied}; Bibarel's Attack stage {bib.stages['atk']}")]


class Sure7(pl.RunDice):
    """Run dice for batch 7's checks: the top damage roll, no miss and no
    critical hit for either side, and only a certain chance lands."""
    def roll(self, top):
        return 15

    def bad(self, kind, p):
        return False

    def good(self, p, kind=None):
        return p >= 1


def b7_battle(boss, player):
    """A battle on the calculator's real rows with batch 7's sure dice."""
    from .test_fightai import battle
    b = battle(boss, player)
    b.dice, b.rng = Sure7(random.Random(1), True), random.Random(1)
    return b, b.b.cur(), b.p.cur()


def sp_def_2_checks():
    """Acid Spray in the readings' battle on the calculator's real rows
    (approved 2026-10-14): the player's Croagunk's hit lowers a trainer's
    Geodude's Sp. Def two stages."""
    b, geo, cro = b7_battle([("Geodude", 30, "Sturdy", ["Tackle"])], [("Croagunk", 30, "Dry Skin", ["Acid Spray"])])
    hp = geo.hp
    pl.attack(b, cro, fs.move("Acid Spray"), geo, True)
    ok = geo.hp < hp and geo.stages["spd"] == -2
    return [("the readings' Acid Spray lowers Sp. Def two stages", ok, f"Geodude's HP {hp} to {geo.hp}, Sp. Def stage {geo.stages['spd']}")]


def tearful_look_checks():
    """Noble Roar in the readings' battle on the calculator's real rows
    (approved 2026-10-14): the player's Bibarel lowers a trainer's
    Geodude's Attack and Sp. Atk a stage each."""
    b, geo, bib = b7_battle([("Geodude", 30, "Sturdy", ["Tackle"])], [("Bibarel", 30, "Unaware", ["Noble Roar"])])
    pl.status_move(b, bib, fs.move("Noble Roar"), geo, True)
    ok = (geo.stages["atk"], geo.stages["spa"]) == (-1, -1)
    return [("the readings' Noble Roar lowers Attack and Sp. Atk", ok, f"Geodude's stages {geo.stages['atk']}, {geo.stages['spa']}")]


def venom_drench_checks():
    """Venom Drench in the readings' battle on the calculator's real rows
    (approved 2026-10-14): the player's Bibarel lowers a poisoned trainer's
    Geodude's Attack, Sp. Atk and Speed, and leaves a healthy one alone."""
    out = {}
    for status in (None, "psn"):
        b, geo, bib = b7_battle([("Geodude", 30, "Sturdy", ["Tackle"])], [("Bibarel", 30, "Unaware", ["Venom Drench"])])
        geo.status = status
        pl.status_move(b, bib, fs.move("Venom Drench"), geo, True)
        out[status] = (geo.stages["atk"], geo.stages["spa"], geo.stages["spe"])
    ok = out == {None: (0, 0, 0), "psn": (-1, -1, -1)}
    return [("the readings' Venom Drench lowers a poisoned target's stats", ok, str(out))]


def false_swipe_checks():
    """False Swipe in the readings' battle on the calculator's real rows
    (approved 2026-10-14): the player's Bibarel's hit leaves a trainer's
    Geodude at 3 HP on 1 HP, where a Tackle knocks it out."""
    out = {}
    for name in ("False Swipe", "Tackle"):
        b, geo, bib = b7_battle([("Geodude", 30, "Sturdy", ["Tackle"])], [("Bibarel", 30, "Unaware", [name])])
        geo.hp = 3
        pl.attack(b, bib, fs.move(name), geo, True)
        out[name] = geo.hp
    ok = out == {"False Swipe": 1, "Tackle": 0}
    return [("the readings' False Swipe leaves its target 1 HP", ok, f"HP left {out}")]


def clear_smog_checks():
    """Clear Smog in the readings' battle on the calculator's real rows
    (approved 2026-10-14): the player's Budew's hit puts a trainer's
    Geodude's +2 Defense and +1 Attack back to 0."""
    b, geo, bud = b7_battle([("Geodude", 30, "Sturdy", ["Tackle"])], [("Budew", 30, "Natural Cure", ["Clear Smog"])])
    geo.stages.update({"def": 2, "atk": 1})
    hp = geo.hp
    pl.attack(b, bud, fs.move("Clear Smog"), geo, True)
    ok = geo.hp < hp and geo.stages["def"] == 0 and geo.stages["atk"] == 0
    return [("the readings' Clear Smog resets its target's stages", ok, f"HP {hp} to {geo.hp}, stages {geo.stages}")]


def incinerate_checks():
    """Incinerate in the readings' battle on the calculator's real rows
    (approved 2026-10-14): the player's Charmander's hit takes a trainer's
    Bibarel below half, and its Sitrus Berry burns before it can eat it."""
    b, bib, cha = b7_battle([("Bibarel", 30, "Unaware", ["Tackle"], "Sitrus Berry")],
                            [("Charmander", 30, "Blaze", ["Incinerate"])])
    bib.item = "Sitrus Berry"
    bib.hp = bib.maxhp // 2 + 2
    hp = bib.hp
    pl.attack(b, cha, fs.move("Incinerate"), bib, True)
    ok = bib.item is None and not bib.ate_berry and bib.hp < hp and bib.hp <= bib.maxhp // 2
    return [("the readings' Incinerate burns its target's Berry before it is eaten", ok,
             f"Bibarel's HP {hp} to {bib.hp} of {bib.maxhp}, item {bib.item}, ate a Berry {bib.ate_berry}")]


def life_dew_checks():
    """Life Dew in the readings' battle on the calculator's real rows
    (approved 2026-10-14): the player's Bibarel at half HP gets back a
    quarter of its maximum, rounded up."""
    b, geo, bib = b7_battle([("Geodude", 30, "Sturdy", ["Tackle"])], [("Bibarel", 30, "Unaware", ["Life Dew"])])
    bib.hp = bib.maxhp // 2
    hp = bib.hp
    pl.status_move(b, bib, fs.move("Life Dew"), geo, True)
    ok = bib.hp == hp + (bib.maxhp + 3) // 4
    return [("the readings' Life Dew heals a quarter", ok, f"Bibarel's HP {hp} to {bib.hp} of {bib.maxhp}")]


def mud_sport_checks():
    """Mud Sport in the readings' battle on the calculator's real rows
    (approved 2026-10-14): after a trainer's Bibarel's Mud Sport the
    player's Pikachu's Thunder Shock hits it half as hard."""
    b, bib, pik = b7_battle([("Bibarel", 26, "Unaware", ["Mud Sport", "Tackle"])],
                            [("Pikachu", 26, "Static", ["Thunder Shock"])])
    shock = fs.move("Thunder Shock")
    before = b.damage(pik, bib, shock, roll=15)
    pl.status_move(b, bib, fs.move("Mud Sport"), pik, True)
    after = b.damage(pik, bib, shock, roll=15)
    ok = before > 0 and abs(after - before / 2) <= 1 and bib.mud_sport
    return [("the readings' Mud Sport halves Electric moves", ok, f"Thunder Shock's top roll {before} before, {after} after")]


def punishment_checks():
    """Punishment in the readings' battle on the calculator's real rows
    (approved 2026-10-14): the player's Sneasel hits a trainer's Geodude
    at +2 Defense at 100 power, five thirds of its plain 60, against a
    Defense twice as high, so at five sixths of its plain hit."""
    b, geo, sne = b7_battle([("Geodude", 30, "Sturdy", ["Defense Curl"])], [("Sneasel", 30, "Inner Focus", ["Punishment"])])
    pun = fs.move("Punishment")
    plain = pl.damage_of(b, sne, geo, pun, False, True)
    geo.stages["def"] = 2
    raised = pl.damage_of(b, sne, geo, pun, False, True)
    want = int(plain * (100 / 60) / 2)
    ok = plain > 0 and abs(raised - want) <= 1
    return [("the readings' Punishment grows with the target's raised stages", ok,
             f"top roll {plain} plain, {raised} at +2 Defense (about {want} wanted)")]


def sticky_web_checks():
    """Sticky Web in the readings' battle on the calculator's real rows
    (approved 2026-10-14): the player's Swadloon lays a web on the trainer's
    side, which costs the trainer's Bibarel a stage of Speed as it comes in
    and spares its Starly; the planner is offered the move once, not twice."""
    b, geo, swa = b7_battle([("Geodude", 30, "Sturdy", ["Tackle"]), ("Bibarel", 30, "Unaware", ["Tackle"]),
                             ("Starly", 30, "Keen Eye", ["Tackle"])], [("Swadloon", 30, "Chlorophyll", ["Sticky Web"])])
    web = fs.move("Sticky Web")
    offered = [("move", web) in pl.player_actions(b)]
    pl.status_move(b, swa, web, geo, True)
    offered.append(("move", web) in pl.player_actions(b))
    fs.switch_in(b, b.b, 1)
    bib = b.b.cur().stages["spe"]
    fs.switch_in(b, b.b, 2)
    sta = b.b.cur().stages["spe"]
    ok = b.b.web == 1 and bib == -1 and sta == 0 and offered == [True, False]
    return [("the readings' Sticky Web slows a grounded newcomer", ok,
             f"web {b.b.web}; Bibarel's Speed stage {bib}, Starly's {sta}; offered {offered}")]


def defog_checks():
    """Defog in the readings' battle on the calculator's real rows (approved
    2026-10-14): the player's Corviknight lowers a trainer's Geodude's
    evasion, takes down its side's Reflect and blows the Stealth Rock off
    the player's own side."""
    b, geo, cor = b7_battle([("Geodude", 30, "Sturdy", ["Tackle"])], [("Corviknight", 30, "Pressure", ["Defog"])])
    b.b.screens["Reflect"], b.p.hazards["rocks"] = 5, 1
    pl.status_move(b, cor, fs.move("Defog"), geo, True)
    ok = geo.stages["eva"] == -1 and b.b.screens["Reflect"] == 0 and b.p.hazards["rocks"] == 0
    return [("the readings' Defog clears screens and hazards", ok,
             f"Geodude's evasion {geo.stages['eva']}, its Reflect {b.b.screens['Reflect']}, the player's rocks {b.p.hazards['rocks']}")]


def strength_sap_checks():
    """Strength Sap in the readings' battle on the calculator's real rows
    (approved 2026-10-14): the player's Dolliv at low HP heals by a
    trainer's Geodude's Attack stat and lowers it a stage."""
    b, geo, dol = b7_battle([("Geodude", 30, "Sturdy", ["Tackle"])], [("Dolliv", 30, "Early Bird", ["Strength Sap"])])
    dol.hp = 1
    pl.status_move(b, dol, fs.move("Strength Sap"), geo, True)
    want = min(dol.maxhp, 1 + geo.stats["atk"])
    ok = dol.hp == want and geo.stages["atk"] == -1
    return [("the readings' Strength Sap heals by the target's Attack", ok,
             f"Dolliv's HP 1 to {dol.hp} (Geodude's Attack {geo.stats['atk']}), Geodude's Attack stage {geo.stages['atk']}")]


def parting_shot_checks():
    """Parting Shot in a whole turn of the readings' battle on the
    calculator's real rows (approved 2026-10-14): the player's Bibarel
    lowers a trainer's Geodude's Attack and Sp. Atk and switches out, and
    the Geodude's Tackle, moving after, hits the Pokemon sent in."""
    b, geo, bib = b7_battle([("Geodude", 30, "Sturdy", ["Tackle"])],
                            [("Bibarel", 30, "Unaware", ["Parting Shot"]), ("Staravia", 30, "Intimidate", ["Peck"])])
    bib.hp = bib.maxhp
    geo_speed, bib_speed = b.speed(geo), b.speed(bib)
    pl._turn(b, ("move", fs.move("Parting Shot")), ("move", fs.move("Tackle")))
    new = b.p.cur()
    got = (new.species, geo.stages["atk"], geo.stages["spa"], bib.hp == bib.maxhp, new.hp < new.maxhp)
    ok = got[0] == "Staravia" and got[2] == -1 and got[1] <= -1 and got[3] and (got[4] or geo_speed > bib_speed)
    return [("the readings' Parting Shot drops both stats and switches its user out", ok,
             f"(on the field, Geodude's Attack and Sp. Atk stages, Bibarel untouched, newcomer hit) {got}")]


def dragon_tail_checks():
    """Dragon Tail in the readings' battle on the calculator's real rows
    (approved 2026-10-14): the player's Gible's hit drags a trainer's
    Geodude out for its Bibarel, which meets the Stealth Rock on its side.
    The whole move runs (use_move), as the drag comes after the hit's
    aftermath since 2026-10-15 (dragon_tail_order_checks)."""
    b, geo, gib = b7_battle([("Geodude", 30, "Sturdy", ["Tackle"]), ("Bibarel", 30, "Unaware", ["Tackle"])],
                            [("Gible", 30, "Sand Veil", ["Dragon Tail"])])
    b.b.hazards["rocks"] = 1
    hp = geo.hp
    pl.use_move(b, gib, fs.move("Dragon Tail"), geo, True)
    new = b.b.cur()
    ok = geo.hp < hp and new.species == "Bibarel" and new.hp < new.maxhp
    return [("the readings' Dragon Tail drags its target out", ok,
             f"Geodude's HP {hp} to {geo.hp}; now in {new.species} at {new.hp} of {new.maxhp}")]


def dragon_tail_order_checks():
    """Dragon Tail's drag after the hit's aftermath in the readings' battle
    on the calculator's real rows (approved 2026-10-15, following the
    engine's fix 6809a5c4e): the player's Gible hits a trainer's Rough Skin
    Sharpedo, loses an eighth of its HP to the Sharpedo's Rough Skin, and
    then drags it out for the Bibarel; a Gible with less than that eighth
    left falls to the Rough Skin and drags nothing."""
    out = {}
    for low in (False, True):
        b, sha, gib = b7_battle([("Sharpedo", 30, "Rough Skin", ["Tackle"]), ("Bibarel", 30, "Unaware", ["Tackle"])],
                                [("Gible", 30, "Sand Veil", ["Dragon Tail"])])
        if low:
            gib.hp = 3
        pl.use_move(b, gib, fs.move("Dragon Tail"), sha, True)
        out["low" if low else "full"] = (b.b.cur().species, gib.maxhp - gib.hp if not low else gib.hp)
    want = {"full": ("Bibarel", gib.maxhp // 8), "low": ("Sharpedo", 0)}
    return [("the readings' Dragon Tail drags after the target's Rough Skin answers", out == want,
             f"(now in, HP the Gible lost or has left) {out}, want {want}")]


def knock_off_first_checks():
    """Knock Off and Bug Bite before the target's Berry, and a trainer's
    item gone from its rows, in the readings' battle on the calculator's
    real rows (approved 2026-10-15): a trainer's Machop holding a Sitrus
    Berry, hit to 2 HP by the player's Knock Off, keeps 2 HP and loses the
    Berry; hit so by the player's Bug Bite from a Vespiquen at half HP, the
    Vespiquen eats it and heals. A trainer's Machop holding a Black Belt
    hits the player's Pokemon less with its Karate Chop once Knock Off has
    taken the Belt, by its item twin's row."""
    out = {}
    for name, user in (("Knock Off", "Absol"), ("Bug Bite", "Vespiquen")):
        b, mach, att = b8_battle([("Machop", 30, "Guts", ["Tackle"], "Sitrus Berry")],
                                 [(user, 30, "Pressure", [name])])
        mach.item = "Sitrus Berry"
        dmg = pl.damage_of(b, att, mach, fs.move(name), False, True, roll=15)
        mach.hp = dmg + 2
        att.hp = att.maxhp // 2
        mine = att.hp
        pl.attack(b, att, fs.move(name), mach, True)
        out[name] = (mach.hp, mach.item, att.hp - mine)
        if name == "Bug Bite":
            gain = att.maxhp // 4
    b, mach, absol = b8_battle([("Machop", 30, "Guts", ["Karate Chop"], "Black Belt")],
                               [("Absol", 30, "Pressure", ["Knock Off"])])
    belted = b.damage(mach, absol, fs.move("Karate Chop"), roll=15)
    pl.attack(b, absol, fs.move("Knock Off"), mach, True)
    bare = b.damage(mach, absol, fs.move("Karate Chop"), roll=15)
    ok = (out["Knock Off"] == (2, None, 0) and out["Bug Bite"] == (2, None, gain) and mach.item is None
          and bare < belted)
    return [("the readings' Knock Off and Bug Bite act before the Berry, and the trainer's rows lose the item", ok,
             f"(Machop's HP, its item, the user's heal) {out}; Karate Chop with the Belt {belted}, after Knock Off {bare}")]


class Confused10(Sure7):
    """Batch 10's dice for confusion: as Sure7, and the player's confusion
    check always hurts it."""
    def bad(self, kind, p):
        return kind == "confusion"


def taunt_before_confusion_checks():
    """Taunt before confusion in the readings' battle on the calculator's
    real rows (approved 2026-10-15): the player's taunted, confused
    Machop's Bulk Up fails at once, with no self-hit and its confusion's
    count kept; an untaunted one hurts itself."""
    out = {}
    for taunted in (True, False):
        b, geo, mach = b8_battle([("Geodude", 30, "Sturdy", ["Tackle"])], [("Machop", 30, "Guts", ["Bulk Up"])],
                                 Confused10)
        mach.confused = 3
        if taunted:
            mach.taunt = 3
        pl.use_move(b, mach, fs.move("Bulk Up"), geo, True)
        out["taunted" if taunted else "not taunted"] = (mach.hp < mach.maxhp, mach.confused, mach.stages["atk"])
    ok = out == {"taunted": (False, 3, 0), "not taunted": (True, 2, 0)}
    return [("the readings' Taunt stops a status move before confusion", ok, f"(hurt, confusion left, Attack) {out}")]


def forced_out_checks():
    """A Pokemon forced out before it acts, in a whole turn of the readings'
    battle on the calculator's real rows (approved 2026-10-15): the
    player's faster Pidgeotto's Whirlwind drags a trainer's Machop out, and
    the Machop's own Whirlwind, of the same priority, never comes, so the
    Pidgeotto stays in."""
    b, mach, pid = b8_battle([("Machop", 30, "Guts", ["Whirlwind"]), ("Geodude", 30, "Sturdy", ["Tackle"])],
                             [("Pidgeotto", 30, "Keen Eye", ["Whirlwind"]), ("Bibarel", 30, "Unaware", ["Tackle"])])
    pl._turn(b, ("move", fs.move("Whirlwind")), ("move", fs.move("Whirlwind")))
    got = (b.p.cur().species, b.b.cur().species)
    return [("the readings' Pokemon dragged out before its turn does not act", got == ("Pidgeotto", "Geodude"),
             f"(the player's in, the trainer's in) {got}")]


def charge_ends_checks():
    """A charge that ends on a turn its user cannot act, in the readings'
    battle on the calculator's real rows (approved 2026-10-15): the
    player's Pidgeotto takes to the air with Fly, flinches on its striking
    turn and comes down without striking, so a trainer's Machop's Tackle
    then hits it; asleep in the air it comes down too."""
    out = {}
    for case in ("flinched", "asleep"):
        b, mach, pid = b8_battle([("Machop", 30, "Guts", ["Tackle"])], [("Pidgeotto", 30, "Keen Eye", ["Fly"])])
        fly = fs.move("Fly")
        pl.use_move(b, pid, fly, mach, True)
        up = pid.charging is not None
        hp = mach.hp
        if case == "flinched":
            pid.flinch = True
            pl.use_move(b, pid, fly, mach, True)
        else:
            pl.give_status(b, pid, "slp")
        mine = pid.hp
        pl.attack(b, mach, fs.move("Tackle"), pid, False)
        out[case] = (up, pid.charging is None, mach.hp == hp, pid.hp < mine)
    ok = out == {"flinched": (True, True, True, True), "asleep": (True, True, True, True)}
    return [("the readings' charge ends on a turn its user cannot act", ok,
             f"(charged, charge ended, no strike, then hit) {out}")]


def ingrain_grounds_checks():
    """Ingrain's grounding in the readings' battle on the calculator's real
    rows (approved 2026-10-15): a trainer's Levitate Bronzor is out of the
    player's Gible's Earthquake's reach, and the trainer's AI reads the
    move as doing nothing to it, until the Bronzor uses Ingrain; then the
    Earthquake hits it and the AI reads the hit."""
    b, bron, gib = b8_battle([("Bronzor", 30, "Levitate", ["Ingrain"])], [("Gible", 30, "Sand Veil", ["Earthquake"])])
    eq = fs.move("Earthquake")
    before = (b.damage(gib, bron, eq, ai_view=True), fightai.script_eff(b, gib, bron, eq) == fightai.IMMUNE)
    pl.status_move(b, bron, fs.move("Ingrain"), gib, True)
    after = (b.damage(gib, bron, eq, ai_view=True), fightai.script_eff(b, gib, bron, eq) == fightai.IMMUNE)
    ok = before == (0, True) and after[0] > 0 and not after[1]
    return [("the readings' Ingrain grounds a Levitate holder", ok,
             f"(Earthquake's top roll, the AI reads it immune) before {before}, after {after}")]


class Probe10(Sure7):
    """Batch 10's dice for accuracy: as Sure7, and each miss chance the
    player's moves meet is recorded."""
    def __init__(self, rng, one_crit=True, luck=None):
        super().__init__(rng, one_crit, luck)
        self.misses = []

    def bad(self, kind, p):
        if kind == "miss":
            self.misses.append(round(p, 6))
        return False


def fog_checks():
    """Deep fog in the readings' battle on the calculator's real rows
    (approved 2026-10-15): a battle made from a fight prepared in fog
    starts in it; there the player's Machop's Karate Chop, of 100
    accuracy, misses four times in ten, where it never misses in clear
    air, and a trainer's Golduck's Cloud Nine lifts the cut."""
    out = {}
    for case in ("clear", "fog", "Cloud Nine"):
        boss = [("Golduck" if case == "Cloud Nine" else "Geodude", 30, "Cloud Nine" if case == "Cloud Nine" else "Sturdy",
                 ["Tackle"])]
        b, foe, mach = b8_battle(boss, [("Machop", 30, "Guts", ["Karate Chop"])], Probe10)
        if case != "clear":
            fogged = pl.make_battle(dict(b.st, fog=True), ["p0"], b.st["bosses"][0], 7, 0)
            b.fog = fogged.fog
        landed = pl.accuracy_hits(b, mach, foe, fs.move("Karate Chop"))
        out[case] = (landed, b.dice.misses)
    ok = out == {"clear": (True, []), "fog": (True, [0.4]), "Cloud Nine": (True, [])}
    return [("the readings' deep fog cuts accuracy to six tenths", ok, f"(landed, miss chances met) {out}")]


def rematch_terrain_checks():
    """A rematch's terrain in a fight prepared on the calculator's real rows
    (approved 2026-10-15): Guitarist Tony's rematch is fought on his road's
    plain, as he was, so its Ludicolo's Nature Power is Earthquake, rowed
    against the player's Machop, where a building's Tri Attack was. The
    rematch is prepared as fightsim.trainer prepares a trainer, in the
    first fight's split, as the scorer places no rematch."""
    from . import calc, data, splits
    ids = {t["constant"]: tid for tid, t in data.oxide_trainers().items()}
    tid = ids["TRAINER_GUITARIST_TONY_REMATCH"]
    t = data.oxide_trainers()[tid]
    split = splits.trainer_split(ids["TRAINER_GUITARIST_TONY"])
    recs = [{"constant": "SPECIES_MACHOP", "species": "Machop", "how": "test", "level": 40, "nature": "Hardy",
             "ivs": IV, "evs": EV, "ability": "Guts", "moves": ["Karate Chop"], "fill": False}]
    st = fs.prepare(split, [plscore.with_genders(t)], calc.fight_weather([tid]), cap=fs.fight_cap(split),
                    given_side=recs, terrain=calc.fight_terrain([tid]))
    lud = next(k for k in st["bosses"][0] if st["pokemon"][k]["species"] == "Ludicolo")
    row = st["rows"].get((None, lud, "p0")) or {}
    got = (st.get("terrain"), fs.nature_power_move(st.get("terrain")), "Earthquake" in (row.get("moves") or {}))
    return [("the readings' rematch is fought on its first fight's terrain", got == ("TERRAIN_PLAIN", "Earthquake", True),
             f"(terrain, Nature Power's move, Earthquake rowed for the Ludicolo) {got}")]


def borrowed_twin_checks():
    """A borrowed move into a changed foe in the readings' battle on the
    calculator's real rows (approved 2026-10-15): once the player's Machop
    has Soaked a trainer's Pidgeotto, its Copycat of the Pidgeotto's Razor
    Leaf and its Me First of the Razor Leaf the Pidgeotto has chosen both
    hit the Water type it now is, super effectively, read from its twin's
    row, where before they read its Normal and Flying row, which resists
    Grass, at a quarter of that."""
    out = {}
    for name in ("Copycat", "Me First"):
        b, pid, mach = b8_battle([("Pidgeotto", 30, "Keen Eye", ["Razor Leaf"])],
                                 [("Machop", 30, "Guts", ["Copycat", "Me First", "Soak"])])
        leaf = fs.move("Razor Leaf")
        old = b.st["rows"][(None, "p0", pid.key)]["moves"]["Razor Leaf"]["rolls"][-1]
        pl.status_move(b, mach, fs.move("Soak"), pid, True)
        b.last_move, pid.chosen = leaf, leaf
        hp = pid.hp
        pl.use_move(b, mach, fs.move(name), pid, True)
        out[name] = (pid.types, hp - pid.hp, old)
    ok = all(t == ["Water"] and dealt >= 3 * old for t, dealt, old in out.values())
    return [("the readings' Copycat and Me First hit a Soaked foe on its twin's row", ok,
             f"(the Pidgeotto's types, HP taken, the old row's top roll) {out}")]


def meloetta_form_checks():
    """Meloetta's forms in the readings' battle on the calculator's real
    rows (approved 2026-10-15): the player's Meloetta's Relic Song on a
    trainer's Snorlax turns it into Pirouette, Normal and Fighting, faster
    and with its Close Combat harder than as Aria; a second Relic Song
    turns it back."""
    b, snor, mel = b8_battle([("Snorlax", 40, "Thick Fat", ["Tackle"])],
                             [("Meloetta", 40, "Serene Grace", ["Relic Song", "Close Combat"])])
    cc, song = fs.move("Close Combat"), fs.move("Relic Song")
    snor.hp = snor.maxhp = 10 ** 6       # it stands through the hits
    aria = (b.damage(mel, snor, cc, ai_view=True), b.speed(mel), list(mel.types))
    pl.use_move(b, mel, song, snor, True)
    pir = (b.damage(mel, snor, cc, ai_view=True), b.speed(mel), list(mel.types))
    pl.use_move(b, mel, song, snor, True)
    back = (b.damage(mel, snor, cc, ai_view=True), b.speed(mel), list(mel.types))
    ok = (pir[2] == ["Normal", "Fighting"] and pir[0] > aria[0] and pir[1] > aria[1] and back == aria)
    return [("the readings' Relic Song turns Meloetta between its forms", ok,
             f"(Close Combat's top roll, Speed, types) Aria {aria}, Pirouette {pir}, back {back}")]


def options_rule_checks():
    """The planner's options in Roark's fight on the calculator's real rows
    (approved 2026-10-15; plplan.would_fail): with Roark's Pokemon in front
    holding nothing, the player's Knock Off is offered, as it still hits;
    with a hurt Pokemon on the bench, Healing Wish is offered; with nobody
    hurt, it is not. The trainer's AI's Basic check scores both -10 or
    below, which ruled them out before."""
    from . import plplan
    team = [("SPECIES_ABSOL", "Absol", "Hardy", "Pressure", ["Knock Off", "Bite"]),
            ("SPECIES_TOGEKISS", "Togekiss", "Hardy", "Serene Grace", ["Healing Wish", "Air Slash"]),
            ("SPECIES_BIBAREL", "Bibarel", "Hardy", "Unaware", ["Tackle"])]
    out = {}
    b = battle(team=team)
    b.b.cur().item = None
    out["Knock Off"] = sorted(a[1].name for a in plplan.options(b) if a[0] == "move")
    for hurt in (True, False):
        b = battle(team=team)
        fs.switch_in(b, b.p, 1)
        if hurt:
            b.p.mons[2].hp //= 2
        out["Healing Wish, " + ("hurt" if hurt else "well")] = sorted(
            a[1].name for a in plplan.options(b) if a[0] == "move")
    want = {"Knock Off": ["Bite", "Knock Off"], "Healing Wish, hurt": ["Air Slash", "Healing Wish"],
            "Healing Wish, well": ["Air Slash"]}
    return [("the planner's options drop only moves that would fail", out == want, f"offered {out}")]


def idle_list_checks():
    """Magic Room off the team search's idle list on Roark's real rows
    (approved 2026-10-15; plteam.IDLE): a box Pikachu with four Electric
    moves and Magic Room takes Magic Room as its status move against
    Roark's team, where it took it only when nothing else was left."""
    from . import plteam
    recs = [{"constant": "SPECIES_PIKACHU", "species": "Pikachu", "how": "test", "level": 16, "nature": "Hardy",
             "ivs": IV, "evs": EV, "ability": "Static",
             "moves": ["Thunder Shock", "Spark", "Nuzzle", "Thunderbolt", "Magic Room"], "fill": False}]
    prep = plscore.prepare(plscore.parse_fight("roark"), given_side=recs)
    st, boss = prep["st"], list(prep["variants"][0][0])
    mine, _theirs, _speed = plteam.matchups(st, ["p0"], boss)
    got = plteam.pick_moves(st, "p0", boss, mine)
    return [("the team search picks Magic Room, no longer idle", "Magic Room" in got, f"picked {got}")]


def merge_key_checks():
    """The planner's merge key on Roark's real rows (approved 2026-10-15):
    a turn that lays Sticky Web on Roark's side, or one that starts Lucky
    Chant on the player's, leads to a position the key tells apart from the
    same position without it, so the two are not merged."""
    from . import plplan
    b = battle()
    out = {}
    for name, side, attr in (("Sticky Web", "b", "web"), ("Lucky Chant", "p", "lucky_chant")):
        c = plplan.clone(b)
        setattr(getattr(c, side), attr, 1 if attr == "web" else 5)
        out[name] = plplan.merge_key(c) != plplan.merge_key(b)
    return [("the planner's merge key tells Sticky Web and Lucky Chant apart", all(out.values()), str(out))]


# ---- batch 11: the abilities open to the player, and Ian's answers of 2026-10-20 ----

# The batch's checks, run after batch 10's in main.
B11 = []


def b11(fn):
    B11.append(fn)
    return fn


@b11
def weak_armor_checks():
    """Weak Armor on the calculator's real rows (approved 2026-10-14): a
    trainer's Houndour's Bite takes the player's Polteageist's Defense down
    a stage and its Speed up two, so it outruns where it did not, and the
    Houndour's Bite then hits harder; its Ember changes nothing."""
    out = {}
    for name in ("Bite", "Ember"):
        b, hound, pol = b8_battle([("Houndour", 30, "Flash Fire", ["Bite", "Ember"])],
                                  [("Polteageist", 30, "Weak Armor", ["Shadow Ball"])])
        pol.hp = pol.maxhp = 10 ** 6          # it stands through the hits
        speed, bite = b.speed(pol), b.damage(hound, pol, fs.move("Bite"), roll=15)
        pl.use_move(b, hound, fs.move(name), pol, True)
        out[name] = (pol.stages["def"], pol.stages["spe"], b.speed(pol) > speed,
                     b.damage(hound, pol, fs.move("Bite"), roll=15) > bite)
    ok = out == {"Bite": (-1, 2, True, True), "Ember": (0, 0, False, False)}
    return [("the readings' Weak Armor trades Defense for Speed after a physical hit", ok,
             f"(Defense, Speed stage, faster, Bite harder) {out}")]


@b11
def water_compaction_checks():
    """Water Compaction on the calculator's real rows (approved 2026-10-14):
    a trainer's Buizel's Aqua Jet raises the player's Sandygast's Defense
    two stages, so the next Aqua Jet does less; its Quick Attack does
    nothing to it (a Ghost type)."""
    out = {}
    for name in ("Aqua Jet", "Quick Attack"):
        b, bui, sandy = b8_battle([("Buizel", 30, "Swift Swim", ["Aqua Jet", "Quick Attack"])],
                                  [("Sandygast", 30, "Water Compaction", ["Shadow Ball"])])
        sandy.hp = sandy.maxhp = 10 ** 6
        jet = b.damage(bui, sandy, fs.move("Aqua Jet"), roll=15)
        pl.use_move(b, bui, fs.move(name), sandy, True)
        out[name] = (sandy.stages["def"], b.damage(bui, sandy, fs.move("Aqua Jet"), roll=15) < jet)
    ok = out == {"Aqua Jet": (2, True), "Quick Attack": (0, False)}
    return [("the readings' Water Compaction raises Defense after a Water hit", ok,
             f"(Defense stage, Aqua Jet softer) {out}")]


@b11
def toxic_debris_checks():
    """Toxic Debris on the calculator's real rows (approved 2026-10-14): a
    trainer's Machop's Karate Chop on the player's Glimmora lays Toxic
    Spikes on the trainer's side, so its Geodude coming in is poisoned;
    after a Water Gun from its Lotad nothing is laid."""
    out = {}
    for name, user in (("Karate Chop", "Machop"), ("Water Gun", "Lotad")):
        b, foe, glim = b8_battle([(user, 30, "Swift Swim", [name]), ("Geodude", 30, "Sturdy", ["Tackle"])],
                                 [("Glimmora", 30, "Toxic Debris", ["Power Gem"])])
        glim.hp = glim.maxhp = 10 ** 6
        pl.use_move(b, foe, fs.move(name), glim, True)
        fs.switch_in(b, b.b, 1)
        out[name] = (b.b.hazards["tspikes"], b.b.cur().status)
    ok = out == {"Karate Chop": (1, "psn"), "Water Gun": (0, None)}
    return [("the readings' Toxic Debris lays Toxic Spikes after a physical hit", ok,
             f"(layers on the trainer's side, the Geodude's status) {out}")]


@b11
def gooey_checks():
    """Gooey on the calculator's real rows (approved 2026-10-14): a
    trainer's Machop's Karate Chop on the player's Goomy costs the Machop a
    stage of Speed, so a Machop that outran it no longer does; its Swift
    costs nothing."""
    out = {}
    for name in ("Karate Chop", "Swift"):
        b, mach, goomy = b8_battle([("Machop", 30, "Guts", ["Karate Chop", "Swift"])],
                                   [("Goomy", 30, "Gooey", ["Water Gun"])])
        goomy.hp = goomy.maxhp = 10 ** 6
        mach.stages["spe"] = 1               # a Machop that outruns the Goomy
        before = b.faster(mach, goomy)
        pl.use_move(b, mach, fs.move(name), goomy, True)
        out[name] = (mach.stages["spe"], before, b.speed(mach) > b.speed(goomy))
    ok = out["Karate Chop"][0] == 0 and out["Swift"][0] == 1 and out["Swift"][2]
    return [("the readings' Gooey slows a contact attacker", ok, f"(Speed stage, faster before, faster after) {out}")]


@b11
def pickpocket_checks():
    """Pickpocket on the calculator's real rows (approved 2026-10-14): a
    trainer's Machop holding a Black Belt Karate Chops the player's
    Weavile, which takes the Belt, and the Machop's next Karate Chop does
    less, by its item twin's row."""
    b, mach, wea = b8_battle([("Machop", 30, "Guts", ["Karate Chop"], "Black Belt")],
                             [("Weavile", 30, "Pickpocket", ["Ice Shard"])])
    wea.hp = wea.maxhp = 10 ** 6
    belted = b.damage(mach, wea, fs.move("Karate Chop"), roll=15)
    pl.use_move(b, mach, fs.move("Karate Chop"), wea, True)
    bare = b.damage(mach, wea, fs.move("Karate Chop"), roll=15)
    ok = wea.item == "Black Belt" and mach.item is None and bare < belted
    return [("the readings' Pickpocket takes a contact attacker's item", ok,
             f"Weavile holds {wea.item}, Machop {mach.item}; Karate Chop with the Belt {belted}, after {bare}")]


@b11
def long_reach_checks():
    """Long Reach on the calculator's real rows (approved 2026-10-14): the
    player's Decidueye's Leaf Blade into a trainer's Gible with Rough Skin
    costs it nothing; an Overgrow Decidueye loses an eighth."""
    out = {}
    for ab in ("Long Reach", "Overgrow"):
        b, gible, dec = b8_battle([("Gible", 30, "Rough Skin", ["Tackle"])], [("Decidueye", 30, ab, ["Leaf Blade"])])
        gible.hp = gible.maxhp = 10 ** 6
        pl.use_move(b, dec, fs.move("Leaf Blade"), gible, True)
        out[ab] = (dec.maxhp - dec.hp, dec.maxhp // 8)
    ok = out["Long Reach"][0] == 0 and out["Overgrow"][0] == out["Overgrow"][1]
    return [("the readings' Long Reach makes no contact", ok, f"(HP lost, an eighth) {out}")]


@b11
def magician_checks():
    """Magician on the calculator's real rows (approved 2026-10-14): the
    player's Delphox's Ember takes a trainer's Machop's Black Belt, and the
    Machop's Karate Chop then does less, by its item twin's row."""
    b, mach, delph = b8_battle([("Machop", 30, "Guts", ["Karate Chop"], "Black Belt")],
                               [("Delphox", 30, "Magician", ["Ember"])])
    mach.hp = mach.maxhp = 10 ** 6
    belted = b.damage(mach, delph, fs.move("Karate Chop"), roll=15)
    pl.use_move(b, delph, fs.move("Ember"), mach, True)
    bare = b.damage(mach, delph, fs.move("Karate Chop"), roll=15)
    ok = delph.item == "Black Belt" and mach.item is None and bare < belted
    return [("the readings' Magician takes the target's item", ok,
             f"Delphox holds {delph.item}, Machop {mach.item}; Karate Chop with the Belt {belted}, after {bare}")]


class Crit11(Sure7):
    """Batch 11's dice for critical hits: as Sure7, and the trainer's
    critical hit always lands (bad luck for the player)."""
    def bad(self, kind, p):
        return kind == "crit" and p > 0


@b11
def anger_point_checks():
    """Anger Point on the calculator's real rows (approved 2026-10-14): a
    trainer's Machop's critical Karate Chop sets the player's Mankey's
    Attack at +6, and its own Karate Chop then hits far harder; a plain
    hit (Sure7's dice) changes nothing."""
    out = {}
    for dice in (Crit11, Sure7):
        b, mach, mank = b8_battle([("Machop", 30, "Guts", ["Karate Chop"])],
                                  [("Mankey", 30, "Anger Point", ["Karate Chop"])], dice)
        mach.hp = mach.maxhp = mank.hp = mank.maxhp = 10 ** 6
        before = b.damage(mank, mach, fs.move("Karate Chop"), roll=15)
        pl.use_move(b, mach, fs.move("Karate Chop"), mank, True)
        out[dice.__name__] = (mank.stages["atk"], b.damage(mank, mach, fs.move("Karate Chop"), roll=15) / before)
    ok = out["Crit11"][0] == 6 and out["Crit11"][1] > 3.5 and out["Sure7"] == (0, 1.0)
    return [("the readings' Anger Point maxes Attack after a critical hit", ok, f"(Attack stage, damage ratio) {out}")]


@b11
def merciless_checks():
    """Merciless on the calculator's real rows (approved 2026-10-14): the
    player's Toxapex's Liquidation lands critical, half again, on a
    poisoned trainer's Machop, and plain on a healthy one (Sure7's dice
    roll no critical hit)."""
    out = {}
    for status in ("psn", None):
        b, mach, pex = b8_battle([("Machop", 30, "Guts", ["Karate Chop"])],
                                 [("Toxapex", 30, "Merciless", ["Liquidation"])])
        mach.hp = mach.maxhp = 10 ** 6
        mach.status = status
        pl.attack(b, pex, fs.move("Liquidation"), mach, True)
        out[status] = mach.maxhp - mach.hp
    plain = pl.damage_of(b, pex, mach, fs.move("Liquidation"), False, True)
    ok = out[None] == plain and out["psn"] == pl.damage_of(b, pex, mach, fs.move("Liquidation"), True, True) > plain
    return [("the readings' Merciless lands critical on a poisoned target", ok, f"(HP taken by status) {out}, plain {plain}")]


@b11
def analytic_checks():
    """Analytic on the calculator's real rows (approved 2026-10-14): the
    player's Magnezone's Flash Cannon in a turn against a faster trainer's
    Jolteon lands at 13/10 of its plain damage; against a slower Snorlax,
    with Magnezone moving first, it lands plain."""
    out = {}
    for foe in ("Jolteon", "Snorlax"):
        b, f, mag = b8_battle([(foe, 30, "Volt Absorb" if foe == "Jolteon" else "Thick Fat", ["Growl"])],
                              [("Magnezone", 30, "Analytic", ["Flash Cannon"])])
        f.hp = f.maxhp = mag.hp = mag.maxhp = 10 ** 6
        plain = pl.damage_of(b, mag, f, fs.move("Flash Cannon"), False, True)
        pl._turn(b, ("move", fs.move("Flash Cannon")), ("move", fs.move("Growl")))
        out[foe] = (f.maxhp - f.hp, plain)
    ok = out["Snorlax"][0] == out["Snorlax"][1] and out["Jolteon"][0] > out["Jolteon"][1] * 1.2
    return [("the readings' Analytic strengthens a move made last", ok, f"(HP taken, plain damage) {out}")]


@b11
def flare_boost_checks():
    """Flare Boost on the calculator's real rows (approved 2026-10-14): the
    player's burned Drifblim's Shadow Ball into a trainer's Machop does
    half again what an unburned one's does."""
    b, mach, drif = b8_battle([("Machop", 30, "Guts", ["Karate Chop"])],
                              [("Drifblim", 30, "Flare Boost", ["Shadow Ball"])])
    plain = pl.damage_of(b, drif, mach, fs.move("Shadow Ball"), False, True)
    drif.status = "brn"
    burned = pl.damage_of(b, drif, mach, fs.move("Shadow Ball"), False, True)
    ok = abs(burned - plain * 1.5) <= 1
    return [("the readings' Flare Boost raises special moves while burned", ok,
             f"Shadow Ball's top roll {plain} unburned, {burned} burned")]


@b11
def metal_weight_checks():
    """Heavy Metal and Light Metal on the calculator's real rows (approved
    2026-10-14): a trainer's Machop's Low Kick into the player's Heavy
    Metal Bronzong (187 kg, doubled past 200) hits at 120 power where a
    Levitate one takes 100, and into a Light Metal Scizor (118.5 kg,
    halved under 60) at 80 where a Technician one takes 100."""
    out = {}
    for sp, abs_ in (("Bronzong", ("Heavy Metal", "Levitate")), ("Scizor", ("Light Metal", "Technician"))):
        tops = []
        for ab in abs_:
            b, mach, mon = b8_battle([("Machop", 30, "Guts", ["Low Kick"])], [(sp, 30, ab, ["Tackle"])])
            tops.append(b.rolls(mach, mon, fs.move("Low Kick"))[-1])
        out[sp] = (tops[0], tops[1], round(tops[0] / tops[1], 2))
    ok = 1.15 <= out["Bronzong"][2] <= 1.25 and 0.75 <= out["Scizor"][2] <= 0.85
    return [("the readings' Heavy Metal and Light Metal change Low Kick's power", ok,
             f"(the holder's top roll, the other's, ratio) {out}")]


@b11
def contrary_checks():
    """Contrary on the calculator's real rows (approved 2026-10-14): the
    player's Serperior's Leaf Storm raises its Sp. Atk two stages, so a
    second Leaf Storm into a trainer's Machop hits harder than the first,
    and the Machop's Leer raises its Defense."""
    b, mach, serp = b8_battle([("Machop", 30, "Guts", ["Leer"])], [("Serperior", 30, "Contrary", ["Leaf Storm"])])
    mach.hp = mach.maxhp = 10 ** 6
    storm = fs.move("Leaf Storm")
    first = pl.damage_of(b, serp, mach, storm, False, True)
    pl.attack(b, serp, storm, mach, True)
    second = pl.damage_of(b, serp, mach, storm, False, True)
    pl.status_move(b, mach, fs.move("Leer"), serp, True)
    ok = serp.stages["spa"] == 2 and second > first * 1.8 and serp.stages["def"] == 1
    return [("the readings' Contrary turns Leaf Storm's drop and Leer's into rises", ok,
             f"Sp. Atk {serp.stages['spa']}, Defense {serp.stages['def']}; Leaf Storm {first} then {second}")]


@b11
def moody_checks():
    """Moody on the calculator's real rows (approved 2026-10-14): over a
    turn in which a trainer's Machop and the player's Bibarel trade
    Tackles, the Bibarel ends with one stat two stages up and another one
    down, and the planner's enumerating dice split the turn's end into its
    twenty draws (five to rise, four to fall)."""
    from . import plplan
    b, mach, bib = b8_battle([("Machop", 30, "Guts", ["Tackle"])], [("Bibarel", 30, "Moody", ["Tackle"])])
    mach.hp = mach.maxhp = bib.hp = bib.maxhp = 10 ** 6
    pl._turn(b, ("move", fs.move("Tackle")), ("move", fs.move("Tackle")))
    moved = sorted(v for v in bib.stages.values() if v)
    b2, mach2, bib2 = b8_battle([("Machop", 30, "Guts", ["Tackle"])], [("Bibarel", 30, "Moody", ["Tackle"])])
    mach2.hp = mach2.maxhp = bib2.hp = bib2.maxhp = 10 ** 6
    d = plplan.EnumDice((), random.Random(1))
    b2.dice, b2.rng = d, d.rng
    fs.end_of_turn(b2)
    sizes = [len(e) for e in d.events]
    ok = moved == [-1, 2] and sizes[-2:] == [5, 4]
    return [("the readings' Moody raises one stat and lowers another at the turn's end", ok,
             f"the Bibarel's moved stages {moved}; the planner's last two draws {sizes[-2:]}")]


@b11
def screen_cleaner_checks():
    """Screen Cleaner on the calculator's real rows (approved 2026-10-14):
    the player's Jynx given Screen Cleaner coming in ends a trainer's
    Reflect, so its Ice Punch into the trainer's Machop does what it does
    with no screen up."""
    b, mach, first = b8_battle([("Machop", 30, "Guts", ["Reflect"])],
                               [("Bibarel", 30, "Simple", ["Tackle"]), ("Jynx", 30, "Screen Cleaner", ["Ice Punch"])])
    mach.hp = mach.maxhp = 10 ** 6
    rime = b.p.mons[1]
    clear = pl.damage_of(b, rime, mach, fs.move("Ice Punch"), False, True)
    pl.status_move(b, mach, fs.move("Reflect"), first, True)
    screened = pl.damage_of(b, rime, mach, fs.move("Ice Punch"), False, True)
    fs.switch_in(b, b.p, 1)
    after = pl.damage_of(b, rime, mach, fs.move("Ice Punch"), False, True)
    ok = screened < clear and after == clear and b.b.screens["Reflect"] == 0
    return [("the readings' Screen Cleaner ends a trainer's Reflect", ok,
             f"Ice Punch's top roll {clear} clear, {screened} under Reflect, {after} after Jynx came in")]


@b11
def overcoat_weather_checks():
    """Overcoat on the calculator's real rows (approved 2026-10-14): in a
    trainer's sandstorm (its Hippowdon's Sand Stream) the player's
    Shellder with Overcoat keeps its HP at the turn's end, where a Shell
    Armor one loses a sixteenth."""
    out = {}
    for ab in ("Overcoat", "Shell Armor"):
        b, hippo, shell = b8_battle([("Hippowdon", 30, "Sand Stream", ["Tackle"])], [("Shellder", 30, ab, ["Tackle"])])
        b.weather = "Sand"
        fs.end_of_turn(b)
        out[ab] = (shell.maxhp - shell.hp, shell.maxhp // 16)
    ok = out["Overcoat"][0] == 0 and out["Shell Armor"][0] == out["Shell Armor"][1] > 0
    return [("the readings' Overcoat keeps the sandstorm off", ok, f"(HP lost, a sixteenth) {out}")]


@b11
def cloud_nine_checks():
    """Cloud Nine on the calculator's real rows (approved 2026-10-14): with a
    trainer's Golduck given Cloud Nine on the field, the player's Swift
    Swim Lotad is not doubled in its Rain Dance's rain, and a sandstorm
    bites neither; with a Damp Golduck the Lotad is doubled and both are
    bitten."""
    out = {}
    for ab in ("Cloud Nine", "Damp"):
        b, duck, lotad = b8_battle([("Golduck", 30, ab, ["Rain Dance"])], [("Lotad", 30, "Swift Swim", ["Tackle"])])
        dry = b.speed(lotad)
        b.weather = "Rain"
        wet = b.speed(lotad)
        b.weather = "Sand"
        fs.end_of_turn(b)
        out[ab] = (wet / dry, duck.maxhp - duck.hp, lotad.maxhp - lotad.hp)
    ok = out["Cloud Nine"] == (1.0, 0, 0) and out["Damp"][0] == 2.0 and out["Damp"][1] > 0 and out["Damp"][2] > 0
    return [("the readings' Cloud Nine stills the weather", ok, f"(rain Speed over dry, HP lost to sand by each) {out}")]


class Misses11(Sure7):
    """Batch 11's dice for accuracy: as Sure7, and every chance of the
    player's move missing lands."""
    def bad(self, kind, p):
        return kind == "miss" and p > 0


@b11
def wonder_skin_checks():
    """Wonder Skin on the calculator's real rows (approved 2026-10-14): the
    player's Pikachu's Thunder Wave can miss a trainer's Skitty with Wonder
    Skin, where it cannot miss a Cute Charm one."""
    out = {}
    for ab in ("Wonder Skin", "Cute Charm"):
        b, sk, pika = b8_battle([("Skitty", 30, ab, ["Tackle"])], [("Pikachu", 30, "Static", ["Thunder Wave"])],
                                Misses11)
        pl.status_move(b, pika, fs.move("Thunder Wave"), sk, True)
        out[ab] = sk.status
    ok = out == {"Wonder Skin": None, "Cute Charm": "par"}
    return [("the readings' Wonder Skin lets Thunder Wave miss", ok, f"the Skitty's status {out}")]


@b11
def prankster_dark_checks():
    """Prankster on the calculator's real rows (approved 2026-10-14): the
    player's Klefki's Thunder Wave fails on a trainer's Poochyena, a Dark
    type, and paralyses a Machop."""
    out = {}
    for foe in ("Poochyena", "Machop"):
        b, f, kle = b8_battle([(foe, 30, "Run Away" if foe == "Poochyena" else "Guts", ["Tackle"])],
                              [("Klefki", 30, "Prankster", ["Thunder Wave"])])
        pl.status_move(b, kle, fs.move("Thunder Wave"), f, True)
        out[foe] = f.status
    ok = out == {"Poochyena": None, "Machop": "par"}
    return [("the readings' Prankster status moves fail on a Dark type", ok, f"the foe's status {out}")]


@b11
def queenly_majesty_checks():
    """Queenly Majesty on the calculator's real rows (approved 2026-10-14):
    the player's Buizel's Aqua Jet does nothing to a trainer's Tsareena
    with Queenly Majesty, where it hits a Leaf Guard one, and its Water
    Gun hits both."""
    out = {}
    for ab in ("Queenly Majesty", "Leaf Guard"):
        b, ts, bui = b8_battle([("Tsareena", 30, ab, ["Tackle"])], [("Buizel", 30, "Swift Swim", ["Aqua Jet", "Water Gun"])])
        ts.hp = ts.maxhp = 10 ** 6
        pl.use_move(b, bui, fs.move("Aqua Jet"), ts, True)
        jet = ts.maxhp - ts.hp
        pl.use_move(b, bui, fs.move("Water Gun"), ts, True)
        out[ab] = (jet, ts.maxhp - ts.hp - jet)
    ok = out["Queenly Majesty"][0] == 0 and out["Leaf Guard"][0] > 0 and out["Queenly Majesty"][1] > 0
    return [("the readings' Queenly Majesty stops Aqua Jet", ok, f"(Aqua Jet's damage, Water Gun's) {out}")]


@b11
def magic_bounce_checks():
    """Magic Bounce on the calculator's real rows (approved 2026-10-14): a
    trainer's Machop's Leer on the player's Espeon with Magic Bounce lowers
    the Machop's own Defense; on a Synchronize Espeon it lowers the
    Espeon's."""
    out = {}
    for ab in ("Magic Bounce", "Synchronize"):
        b, mach, esp = b8_battle([("Machop", 30, "Guts", ["Leer"])], [("Espeon", 30, ab, ["Confusion"])])
        pl.status_move(b, mach, fs.move("Leer"), esp, True)
        out[ab] = (mach.stages["def"], esp.stages["def"])
    ok = out == {"Magic Bounce": (-1, 0), "Synchronize": (0, -1)}
    return [("the readings' Magic Bounce turns Leer back", ok, f"(the Machop's Defense, the Espeon's) {out}")]


@b11
def sweet_veil_checks():
    """Sweet Veil on the calculator's real rows (approved 2026-10-14): a
    trainer's Smoochum's Sing does not put the player's Sweet Veil Tsareena
    to sleep, and puts an Oblivious one to sleep."""
    out = {}
    for ab in ("Sweet Veil", "Oblivious"):
        b, smo, ts = b8_battle([("Smoochum", 30, "Forewarn", ["Sing"])], [("Tsareena", 30, ab, ["Tackle"])])
        b.dice = Lucky8(random.Random(1), True)
        pl.status_move(b, smo, fs.move("Sing"), ts, True)
        out[ab] = ts.status
    ok = out == {"Sweet Veil": None, "Oblivious": "slp"}
    return [("the readings' Sweet Veil keeps its holder awake", ok, f"the Tsareena's status {out}")]


@b11
def pastel_veil_checks():
    """Pastel Veil on the calculator's real rows (approved 2026-10-14): a
    trainer's Grimer's Toxic does not poison the player's Pastel Veil
    Ponyta, and badly poisons a Run Away one."""
    out = {}
    for ab in ("Pastel Veil", "Run Away"):
        b, gri, pony = b8_battle([("Grimer", 30, "Stench", ["Toxic"])], [("Ponyta", 30, ab, ["Tackle"])])
        b.dice = Lucky8(random.Random(1), True)
        pl.status_move(b, gri, fs.move("Toxic"), pony, True)
        out[ab] = pony.status
    ok = out == {"Pastel Veil": None, "Run Away": "tox"}
    return [("the readings' Pastel Veil keeps poison off its holder", ok, f"the Ponyta's status {out}")]


@b11
def flower_veil_checks():
    """Flower Veil on the calculator's real rows (approved 2026-10-14): a
    trainer's Machop's Leer leaves the Defense of the player's Grass-type
    Turtwig given Flower Veil as it was, and lowers an Overgrow one's; a
    Floette, no Grass type, has no shield."""
    out = {}
    for sp, ab in (("Turtwig", "Flower Veil"), ("Turtwig", "Overgrow"), ("Floette", "Flower Veil")):
        b, mach, mon = b8_battle([("Machop", 30, "Guts", ["Leer"])], [(sp, 30, ab, ["Tackle"])])
        pl.status_move(b, mach, fs.move("Leer"), mon, True)
        out[(sp, ab)] = mon.stages["def"]
    ok = out == {("Turtwig", "Flower Veil"): 0, ("Turtwig", "Overgrow"): -1, ("Floette", "Flower Veil"): -1}
    return [("the readings' Flower Veil shields a Grass-type holder's stats", ok, f"Defense after Leer {out}")]


@b11
def pluck_through_substitute_checks():
    """Bug Bite through a Substitute on the calculator's real rows (Ian's
    answer of 2026-10-20): the player's Vespiquen at half HP eats the Sitrus
    Berry of a trainer's Machop behind a Substitute that takes the hit, and
    heals a quarter."""
    b, mach, ves = b8_battle([("Machop", 30, "Guts", ["Tackle"], "Sitrus Berry")],
                             [("Vespiquen", 30, "Pressure", ["Bug Bite"])])
    mach.item, mach.sub = "Sitrus Berry", 10 ** 6
    ves.hp = ves.maxhp // 2
    hp = ves.hp
    pl.attack(b, ves, fs.move("Bug Bite"), mach, True)
    ok = mach.item is None and mach.hp == mach.maxhp and ves.hp - hp == ves.maxhp // 4
    return [("the readings' Bug Bite eats the Berry through a Substitute", ok,
             f"Machop's item {mach.item}, HP {mach.hp}/{mach.maxhp}; Vespiquen healed {ves.hp - hp}")]


@b11
def belly_drum_at_six_checks():
    """Belly Drum at +6 on the calculator's real rows (Ian's answer of
    2026-10-20): the player's Snorlax with its Attack at +6 already keeps
    its HP when it uses Belly Drum against a trainer's Machop; from 0 it
    pays half."""
    out = {}
    for start in (6, 0):
        b, mach, snor = b8_battle([("Machop", 30, "Guts", ["Tackle"])], [("Snorlax", 30, "Thick Fat", ["Belly Drum"])])
        snor.stages["atk"] = start
        pl.use_move(b, snor, fs.move("Belly Drum"), mach, True)
        out[start] = (snor.maxhp - snor.hp, snor.stages["atk"])
    ok = out[6] == (0, 6) and out[0][0] == snor.maxhp // 2 and out[0][1] == 6
    return [("the readings' Belly Drum at +6 costs nothing", ok, f"(HP paid, Attack stage) from +6 and from 0 {out}")]


@b11
def held_state_key_checks():
    """The planner's merge key on the calculator's real rows (approved 2026-10-20):
    after a turn in which the player's Slaking (Truant) and a trainer's
    Geodude both act, the position is told apart from the same position
    with the Slaking's loafing turn spent, and a Geodude that has used
    Defense Curl from one that has not."""
    from . import plplan
    b, geo, slak = b8_battle([("Geodude", 30, "Sturdy", ["Defense Curl", "Tackle"])], [("Slaking", 30, "Truant", ["Tackle"])])
    geo.hp = geo.maxhp = slak.hp = slak.maxhp = 10 ** 6
    pl._turn(b, ("move", fs.move("Tackle")), ("move", fs.move("Defense Curl")))
    out = {}
    for name, mon, attr in (("Truant", slak, "loafing"), ("Defense Curl", geo, "curled")):
        c = plplan.clone(b)
        m = c.p.cur() if mon is slak else c.b.cur()
        setattr(m, attr, not getattr(m, attr))
        out[name] = (getattr(mon, attr), plplan.merge_key(c) != plplan.merge_key(b))
    ok = out == {"Truant": (True, True), "Defense Curl": (True, True)}
    return [("the readings' merge key tells Truant's turn and Defense Curl apart", ok, f"(the state set, told apart) {out}")]


@b11
def copycat_idle_checks():
    """Copycat off the team search's idle list on Roark's real rows (Ian's
    answer of 2026-10-20; plteam.IDLE): a box Pikachu with four Electric
    moves and Copycat takes it as its status move against Roark's team.
    Water Sport, also off the list that day, is idle against Roark, whose
    team has no Fire hit (Ian's answer of the same day; sports_idle_checks)."""
    from . import plteam
    out = {}
    for extra in ("Copycat", "Water Sport"):
        recs = [{"constant": "SPECIES_PIKACHU", "species": "Pikachu", "how": "test", "level": 16, "nature": "Hardy",
                 "ivs": IV, "evs": EV, "ability": "Static",
                 "moves": ["Thunder Shock", "Spark", "Nuzzle", "Thunderbolt", extra], "fill": False}]
        prep = plscore.prepare(plscore.parse_fight("roark"), given_side=recs)
        st, boss = prep["st"], list(prep["variants"][0][0])
        mine, _theirs, _speed = plteam.matchups(st, ["p0"], boss)
        out[extra] = extra in plteam.pick_moves(st, "p0", boss, mine)
    return [("the team search picks Copycat, and Water Sport not against Roark", out == {"Copycat": True,
             "Water Sport": False}, f"picked {out}")]


@b11
def borrowed_power_row_checks():
    """A borrowed Magnitude, Present or Heat Crash on the calculator's real
    rows (Ian's answer of 2026-10-20): the player's Togekiss's Copycat of a
    trainer's Magnitude, Present or Heat Crash hits a Machop, from the power
    rows prepare() now gives a Pokemon that can borrow the move, where it
    found no row and dealt nothing."""
    out = {}
    for foe, name in (("Diglett", "Magnitude"), ("Delibird", "Present"), ("Torkoal", "Heat Crash")):
        b, f, tog = b8_battle([(foe, 30, "Sturdy", [name]), ("Machop", 30, "Guts", ["Tackle"])],
                              [("Togekiss", 30, "Hustle", ["Copycat"])])
        fs.switch_in(b, b.b, 1)
        mach = b.b.cur()
        mach.hp = mach.maxhp = 10 ** 6
        b.last_move = fs.move(name)
        dealt = 0
        for seed in range(8):            # Present's gift heals at times; any hit counts
            b.dice = Sure7(random.Random(seed), True)
            before = mach.hp
            pl.use_move(b, tog, fs.move("Copycat"), mach, True)
            dealt = max(dealt, before - mach.hp)
            b.last_move = fs.move(name)
        out[name] = dealt
    ok = all(v > 0 for v in out.values())
    return [("the readings' borrowed Magnitude, Present and Heat Crash deal damage", ok, f"the most a Copycat dealt {out}")]


def side_guard_checks():
    """Quick Guard in a whole turn of the readings' battle on the
    calculator's real rows (approved 2026-10-14): the player's Bibarel's
    Quick Guard, at +3, goes up before a trainer's Starly's Quick Attack and
    stops it, where a Tackle would have landed."""
    out = {}
    for foe_move in ("Quick Attack", "Tackle"):
        b, sta, bib = b7_battle([("Starly", 30, "Keen Eye", [foe_move])], [("Bibarel", 30, "Unaware", ["Quick Guard"])])
        pl._turn(b, ("move", fs.move("Quick Guard")), ("move", fs.move(foe_move)))
        out[foe_move] = bib.hp == bib.maxhp
    ok = out == {"Quick Attack": True, "Tackle": False}
    return [("the readings' Quick Guard stops a priority move", ok, f"Bibarel untouched {out}")]


def heat_crash_checks():
    """Heat Crash in the readings' battle on the calculator's real rows
    (approved 2026-10-14): the player's Torkoal's Heat Crash hits a
    trainer's light Starly at 120 power and its heavy Onix at 40, and the
    team search's rating of it reads the same rows."""
    from . import plteam
    b, sta, tor = b7_battle([("Starly", 30, "Keen Eye", ["Tackle"]), ("Onix", 30, "Sturdy", ["Tackle"])],
                            [("Torkoal", 30, "White Smoke", ["Heat Crash"])])
    onix = b.b.mons[1]
    hc = fs.move("Heat Crash")
    powers = (b.st["heat_crash"].get((tor.key, sta.key)), b.st["heat_crash"].get((tor.key, onix.key)))
    hits = (pl.damage_of(b, tor, sta, hc, False, True), pl.damage_of(b, tor, onix, hc, False, True))
    mine, _theirs, _speed = plteam.matchups(b.st, [tor.key], [sta.key, onix.key])
    rated = mine.get((tor.key, "Heat Crash"))
    hp = sta.hp
    pl.attack(b, tor, hc, sta, True)
    ok = powers == (120, 40) and all(h and h > 0 for h in hits) and sta.hp < hp and rated and rated[0] > 0
    return [("the readings' Heat Crash hits at its weight power", ok,
             f"powers {powers}, top rolls {hits}, Starly's HP {hp} to {sta.hp}, team search's shares {rated}")]


def healing_wish_checks():
    """Healing Wish in a whole turn of the readings' battle on the
    calculator's real rows (approved 2026-10-14): the player's Bibarel
    faints to it, its poisoned Staravia at half HP comes in at once and is
    healed and cured, and the trainer's Geodude's Tackle, moving after,
    hits the Staravia."""
    b, geo, bib = b7_battle([("Geodude", 20, "Sturdy", ["Tackle"])],
                            [("Bibarel", 40, "Unaware", ["Healing Wish"]), ("Staravia", 40, "Intimidate", ["Peck"])])
    sta = b.p.mons[1]
    sta.hp, sta.status = sta.maxhp // 2, "psn"
    pl._turn(b, ("move", fs.move("Healing Wish")), ("move", fs.move("Tackle")))
    got = (bib.hp, b.p.cur().species, sta.status, sta.hp > sta.maxhp // 2, sta.hp < sta.maxhp)
    ok = got == (0, "Staravia", None, True, True)
    return [("the readings' Healing Wish heals its replacement", ok,
             f"(Bibarel's HP, on the field, Staravia's status, healed past half, hit after) {got}")]


def guard_split_checks():
    """Guard Split in the readings' battle on the calculator's real rows
    (approved 2026-10-14): the player's Dubwool and a trainer's Onix share
    their Defense, and the Onix's Tackle into the Dubwool and the Dubwool's
    into the Onix change by the Defenses' ratios."""
    b, geo, dub = b7_battle([("Onix", 30, "Sturdy", ["Tackle"])], [("Dubwool", 30, "Fluffy", ["Guard Split", "Tackle"])])
    tackle = fs.move("Tackle")
    before = (pl.damage_of(b, dub, geo, tackle, False, True), pl.damage_of(b, geo, dub, tackle, False, True))
    gd, dd = geo.stats["def"], dub.stats["def"]
    pl.status_move(b, dub, fs.move("Guard Split"), geo, True)
    avg = (gd + dd) // 2
    after = (pl.damage_of(b, dub, geo, tackle, False, True), pl.damage_of(b, geo, dub, tackle, False, True))
    want = (int(before[0] * gd / avg), int(before[1] * dd / avg))
    ok = fs.raw_stat(geo, "def") == fs.raw_stat(dub, "def") == avg and all(abs(x - y) <= 1 for x, y in zip(after, want))
    return [("the readings' Guard Split shares the Defenses", ok,
             f"Defenses {gd} and {dd} to {avg}; top rolls {before} to {after} (about {want} wanted)")]


def power_split_checks():
    """Power Split in the readings' battle on the calculator's real rows
    (approved 2026-10-14): the player's Bibarel and a trainer's Machoke
    share their Attack, and each one's Tackle into the other changes by the
    Attacks' ratios."""
    b, mac, bib = b7_battle([("Machoke", 30, "Guts", ["Tackle"])], [("Bibarel", 30, "Unaware", ["Power Split", "Tackle"])])
    tackle = fs.move("Tackle")
    before = (pl.damage_of(b, bib, mac, tackle, False, True), pl.damage_of(b, mac, bib, tackle, False, True))
    ma, ba = mac.stats["atk"], bib.stats["atk"]
    pl.status_move(b, bib, fs.move("Power Split"), mac, True)
    avg = (ma + ba) // 2
    after = (pl.damage_of(b, bib, mac, tackle, False, True), pl.damage_of(b, mac, bib, tackle, False, True))
    want = (int(before[0] * avg / ba), int(before[1] * avg / ma))
    ok = fs.raw_stat(mac, "atk") == fs.raw_stat(bib, "atk") == avg and ma != ba \
        and all(abs(x - y) <= 1 for x, y in zip(after, want))
    return [("the readings' Power Split shares the Attacks", ok,
             f"Attacks {ma} and {ba} to {avg}; top rolls {before} to {after} (about {want} wanted)")]


def embargo_checks():
    """Embargo in the readings' battle on the calculator's real rows
    (approved 2026-10-14): a trainer's Geodude under the player's Embargo
    keeps its Sitrus Berry when a hit takes it below half, where without
    Embargo it eats it."""
    out = {}
    for embargoed in (False, True):
        b, geo, bib = b7_battle([("Geodude", 30, "Sturdy", ["Tackle"], "Sitrus Berry")],
                                [("Bibarel", 30, "Unaware", ["Embargo", "Tackle"])])
        geo.item = "Sitrus Berry"
        if embargoed:
            pl.status_move(b, bib, fs.move("Embargo"), geo, True)
        geo.hp = geo.maxhp // 2 + 1
        pl.attack(b, bib, fs.move("Tackle"), geo, True)
        out[embargoed] = (geo.item, geo.item_off, geo.hp <= geo.maxhp // 2)
    ok = out == {False: (None, None, False), True: (None, "Sitrus Berry", True)}
    return [("the readings' Embargo keeps a Berry from working", ok, f"(item, held back, below half) {out}")]


def magic_room_checks():
    """Magic Room in the readings' battle on the calculator's real rows
    (approved 2026-10-14): while it runs the player's Charmander's Charcoal
    adds nothing to its Ember, and the trainer's Bibarel's Sitrus Berry
    stays uneaten below half."""
    b, bib, cha = b7_battle([("Bibarel", 30, "Unaware", ["Tackle"], "Sitrus Berry")],
                            [("Charmander", 30, "Blaze", ["Magic Room", "Ember"])])
    cha.item, bib.item = "Charcoal", "Sitrus Berry"
    ember = fs.move("Ember")
    boosted = pl.damage_of(b, cha, bib, ember, False, True)
    pl.status_move(b, cha, fs.move("Magic Room"), bib, True)
    plain = pl.damage_of(b, cha, bib, ember, False, True)
    bib.hp = bib.maxhp // 2 + 1
    pl.attack(b, cha, ember, bib, True)
    ok = plain < boosted and bib.item_off == "Sitrus Berry" and bib.hp <= bib.maxhp // 2 and b.magic_room == 5
    return [("the readings' Magic Room holds every item back", ok,
             f"Ember's top roll {boosted} with Charcoal, {plain} in the room; Bibarel's Berry held back {bib.item_off}")]


class Lucky8(Sure7):
    """Batch 8's dice: as Sure7 (the top roll, no miss, no critical hit),
    and every added effect at a chance lands, the player's own moves'
    (good) and the trainer's on the player (lands_on_player)."""
    def good(self, p, kind=None):
        return p >= 1 or (p > 0 and kind not in (None, "crit"))

    def lands_on_player(self, kind, p):
        return p > 0


def b8_battle(boss, player, dice=Sure7):
    """A battle on the calculator's real rows with batch 8's dice."""
    from .test_fightai import battle
    b = battle(boss, player)
    b.dice, b.rng = dice(random.Random(1), True), random.Random(1)
    return b, b.b.cur(), b.p.cur()


def relic_song_checks():
    """Relic Song in the readings' battle on the calculator's real rows
    (approved 2026-10-14): the player's Meloetta's hit puts a trainer's
    Geodude to sleep when its chance lands, and a Tackle does not."""
    out = {}
    for name in ("Relic Song", "Tackle"):
        b, geo, mel = b8_battle([("Geodude", 30, "Sturdy", ["Tackle"])], [("Meloetta", 30, "Serene Grace", [name])],
                                Lucky8)
        pl.attack(b, mel, fs.move(name), geo, True)
        out[name] = (geo.status, geo.hp < geo.maxhp)
    ok = out == {"Relic Song": ("slp", True), "Tackle": (None, True)}
    return [("the readings' Relic Song puts its target to sleep", ok, f"(status, hit) {out}")]


def clanging_scales_checks():
    """Clanging Scales in the readings' battle on the calculator's real
    rows (approved 2026-10-14): the player's Bibarel's hit on a trainer's
    Geodude lowers the Bibarel's own Defense a stage."""
    b, geo, bib = b8_battle([("Geodude", 30, "Sturdy", ["Tackle"])], [("Bibarel", 30, "Unaware", ["Clanging Scales"])])
    hp = geo.hp
    pl.attack(b, bib, fs.move("Clanging Scales"), geo, True)
    ok = geo.hp < hp and bib.stages["def"] == -1
    return [("the readings' Clanging Scales lowers its user's Defense", ok,
             f"Geodude's HP {hp} to {geo.hp}, Bibarel's Defense stage {bib.stages['def']}")]

def matcha_gotcha_checks():
    """Matcha Gotcha in the readings' battle on the calculator's real rows
    (approved 2026-10-14): the player's Bibarel at half HP hits a trainer's
    Geodude, which Sturdy holds at 1 HP, drains half of what it took, and
    burns it when the chance lands."""
    b, geo, bib = b8_battle([("Geodude", 30, "Sturdy", ["Tackle"])], [("Bibarel", 30, "Unaware", ["Matcha Gotcha"])],
                            Lucky8)
    bib.hp = bib.maxhp // 2
    hp, mine = geo.hp, bib.hp
    pl.attack(b, bib, fs.move("Matcha Gotcha"), geo, True)
    ok = geo.hp == 1 and bib.hp == mine + (hp - 1) // 2 and geo.status == "brn"
    return [("the readings' Matcha Gotcha drains and burns", ok,
             f"Geodude's HP {hp} to {geo.hp}, its status {geo.status}; Bibarel's HP {mine} to {bib.hp}")]

def fell_stinger_checks():
    """Fell Stinger in the readings' battle on the calculator's real rows
    (approved 2026-10-14): the player's Bibarel's hit knocks out a trainer's
    Geodude at 1 HP and its Attack rises three stages; at full HP Sturdy
    holds the Geodude and the Attack stays."""
    out = {}
    for low in (True, False):
        b, geo, bib = b8_battle([("Geodude", 30, "Sturdy", ["Tackle"])], [("Bibarel", 30, "Unaware", ["Fell Stinger"])])
        if low:
            geo.hp = 1
        pl.attack(b, bib, fs.move("Fell Stinger"), geo, True)
        out[low] = (geo.alive(), bib.stages["atk"])
    ok = out == {True: (False, 3), False: (True, 0)}
    return [("the readings' Fell Stinger raises Attack on a knockout", ok, f"(Geodude standing, Bibarel's Attack) {out}")]

def prevent_escape_hit_checks():
    """Anchor Shot in the readings' battle on the calculator's real rows
    (approved 2026-10-14): the player's Bibarel's hit leaves a trainer's
    Geodude held, so it cannot switch, and a Tackle does not."""
    out = {}
    for name in ("Anchor Shot", "Tackle"):
        b, geo, bib = b8_battle([("Geodude", 30, "Sturdy", ["Tackle"]), ("Onix", 30, "Sturdy", ["Tackle"])],
                                [("Bibarel", 30, "Unaware", [name])])
        pl.attack(b, bib, fs.move(name), geo, True)
        out[name] = (geo.hp < geo.maxhp, geo.trapped_by == bib.key, fs.trapped(b, geo))
    ok = out == {"Anchor Shot": (True, True, True), "Tackle": (True, False, False)}
    return [("the readings' Anchor Shot traps its target", ok, f"(hit, held by Bibarel, trapped) {out}")]

def poltergeist_checks():
    """Poltergeist in the readings' battle on the calculator's real rows
    (approved 2026-10-14): the player's Bibarel's Poltergeist hits a
    trainer's Geodude holding an Oran Berry and fails on one holding
    nothing."""
    out = {}
    for item in ("Oran Berry", None):
        b, geo, bib = b8_battle([("Geodude", 30, "Sturdy", ["Tackle"])], [("Bibarel", 30, "Unaware", ["Poltergeist"])])
        geo.item = item
        hp = geo.hp
        pl.attack(b, bib, fs.move("Poltergeist"), geo, True)
        out[item] = hp - geo.hp
    ok = out["Oran Berry"] > 0 and out[None] == 0
    return [("the readings' Poltergeist fails on a target with no item", ok, f"HP taken {out}")]

def belch_checks():
    """Belch in the readings' battle on the calculator's real rows
    (approved 2026-10-14): the player's Bibarel's Belch takes nothing from
    a trainer's Geodude before the Bibarel has eaten its Oran Berry, and
    hits once it has."""
    out = {}
    for eaten in (False, True):
        b, geo, bib = b8_battle([("Geodude", 30, "Sturdy", ["Tackle"])], [("Bibarel", 30, "Unaware", ["Belch"])])
        bib.item = "Oran Berry"
        if eaten:
            bib.hp = bib.maxhp // 2 - 1
            fs.berry_check(bib, b)       # the Bibarel eats its Berry at half HP
        hp = geo.hp
        pl.attack(b, bib, fs.move("Belch"), geo, True)
        out[eaten] = (bib.item, hp - geo.hp)
    ok = out[False] == ("Oran Berry", 0) and out[True][0] is None and out[True][1] > 0
    return [("the readings' Belch fails before a Berry is eaten", ok, f"(Bibarel's item, HP taken) {out}")]

def first_impression_checks():
    """First Impression in the readings' battle on the calculator's real
    rows (approved 2026-10-14): the player's Bibarel's hits a trainer's
    Geodude on its first turn out and takes nothing on a later one."""
    out = {}
    for turns in (0, 1):
        b, geo, bib = b8_battle([("Geodude", 30, "Sturdy", ["Tackle"])], [("Bibarel", 30, "Unaware", ["First Impression"])])
        bib.turns_in = turns
        hp = geo.hp
        pl.attack(b, bib, fs.move("First Impression"), geo, True)
        out[turns] = hp - geo.hp
    ok = out[0] > 0 and out[1] == 0
    return [("the readings' First Impression fails after the first turn", ok, f"HP taken by turns out {out}")]

def axe_kick_checks():
    """Axe Kick in the readings' battle on the calculator's real rows
    (approved 2026-10-14): the player's Bibarel's hit confuses a trainer's
    Bibarel when its chance lands, and its miss costs the player's half the
    hit's damage, as the planner's dice would have the hit land."""
    b, foe, bib = b8_battle([("Bibarel", 30, "Simple", ["Tackle"])], [("Bibarel", 30, "Unaware", ["Axe Kick"])], Lucky8)
    pl.attack(b, bib, fs.move("Axe Kick"), foe, True)
    confused = bool(foe.confused)

    class Miss(Lucky8):
        def bad(self, kind, p):
            return kind == "miss"
    b2, foe2, bib2 = b8_battle([("Bibarel", 30, "Simple", ["Tackle"])], [("Bibarel", 30, "Unaware", ["Axe Kick"])], Miss)
    hit = pl.damage_of(b2, bib2, foe2, fs.move("Axe Kick"), False, True)
    hp = bib2.hp
    pl.attack(b2, bib2, fs.move("Axe Kick"), foe2, True)
    crash = (hp - bib2.hp, foe2.hp == foe2.maxhp)
    ok = confused and crash == (min(hit // 2, foe2.maxhp // 2), True)
    return [("the readings' Axe Kick confuses and crashes on a miss", ok,
             f"confused {confused}; crash (HP lost, target untouched) {crash}, the hit's top roll {hit}")]

def always_critical_checks():
    """Frost Breath in the readings' battle on the calculator's real rows
    (approved 2026-10-14): the player's Glalie's hit on a trainer's
    Bibarel is its row's critical hit, behind a Light Screen and into +1
    Sp. Def alike, two thirds of it under the trainer's Lucky Chant, and
    the trainer's AI reckons the move without the critical hit."""
    out = {}
    for case in ("plain", "light screen", "+1 Sp. Def", "lucky chant"):
        b, bib, gla = b8_battle([("Bibarel", 30, "Simple", ["Frost Breath"])], [("Glalie", 30, "Inner Focus", ["Frost Breath"])])
        if case == "light screen":
            b.b.screens["Light Screen"] = 5
        if case == "+1 Sp. Def":
            bib.stages["spd"] = 1
        if case == "lucky chant":
            b.b.lucky_chant = 5
        top = b.rolls(gla, bib, fs.move("Frost Breath"))[-1]
        hp = bib.hp
        pl.attack(b, gla, fs.move("Frost Breath"), bib, True)
        out[case] = (hp - bib.hp, top)
    est = (b.damage(bib, gla, fs.move("Frost Breath"), ai_view=True), b.rolls(bib, gla, fs.move("Frost Breath"))[-1])
    ok = (all(d == t for d, t in (out["plain"], out["light screen"], out["+1 Sp. Def"]))
          and out["lucky chant"][0] == int(out["lucky chant"][1] / 1.5) and est[0] == int(est[1] / 1.5))
    return [("the readings' Frost Breath is its row's critical hit", ok, f"(HP taken, row's top roll) {out}; AI's estimate {est}")]

def clangorous_soul_checks():
    """Clangorous Soul in the readings' battle on the calculator's real
    rows (approved 2026-10-14): the player's Bibarel gives a third of its
    maximum HP for a stage of all five stats."""
    b, geo, bib = b8_battle([("Geodude", 30, "Sturdy", ["Tackle"])], [("Bibarel", 30, "Unaware", ["Clangorous Soul"])])
    pl.status_move(b, bib, fs.move("Clangorous Soul"), geo, True)
    got = (bib.maxhp - bib.hp, tuple(bib.stages[k] for k in ("atk", "def", "spa", "spd", "spe")))
    ok = got == (bib.maxhp // 3, (1, 1, 1, 1, 1))
    return [("the readings' Clangorous Soul raises all five stats", ok, f"(HP lost, stages) {got} of {bib.maxhp}")]

def heart_swap_checks():
    """Heart Swap in the readings' battle on the calculator's real rows
    (approved 2026-10-14): the player's Bibarel takes a trainer's Geodude's
    +2 Defense and +1 Speed and hands it its own -1 Attack."""
    b, geo, bib = b8_battle([("Geodude", 30, "Sturdy", ["Tackle"])], [("Bibarel", 30, "Unaware", ["Heart Swap"])])
    geo.stages.update({"def": 2, "spe": 1})
    bib.stages["atk"] = -1
    pl.status_move(b, bib, fs.move("Heart Swap"), geo, True)
    got = ((bib.stages["def"], bib.stages["spe"], bib.stages["atk"]), (geo.stages["def"], geo.stages["spe"], geo.stages["atk"]))
    ok = got == ((2, 1, 0), (0, 0, -1))
    return [("the readings' Heart Swap exchanges the stages", ok, f"(Bibarel's, Geodude's) Defense, Speed, Attack {got}")]

def heal_pulse_checks():
    """Heal Pulse in the readings' battle on the calculator's real rows
    (approved 2026-10-14): in a single battle the player's Bibarel's Heal
    Pulse gives a trainer's Geodude at 1 HP half its HP back."""
    b, geo, bib = b8_battle([("Geodude", 30, "Sturdy", ["Tackle"])], [("Bibarel", 30, "Unaware", ["Heal Pulse"])])
    geo.hp = 1
    pl.status_move(b, bib, fs.move("Heal Pulse"), geo, True)
    ok = geo.hp == 1 + (geo.maxhp + 1) // 2
    return [("the readings' Heal Pulse heals its target", ok, f"Geodude's HP 1 to {geo.hp} of {geo.maxhp}")]

def lunar_dance_checks():
    """Lunar Dance in a whole turn of the readings' battle on the
    calculator's real rows (approved 2026-10-14): the player's Bibarel
    faints to it, its burned Staravia at half HP with one PP of Peck left
    comes in at once and is healed, cured and given its PP back, and the
    trainer's Geodude's Tackle, moving after, hits the Staravia."""
    b, geo, bib = b8_battle([("Geodude", 20, "Sturdy", ["Tackle"])],
                            [("Bibarel", 40, "Unaware", ["Lunar Dance"]), ("Staravia", 40, "Intimidate", ["Peck"])])
    sta = b.p.mons[1]
    sta.hp, sta.status, sta.pp = sta.maxhp // 2, "brn", {"Peck": 1}
    pl._turn(b, ("move", fs.move("Lunar Dance")), ("move", fs.move("Tackle")))
    got = (bib.hp, b.p.cur().species, sta.status, sta.pp["Peck"], sta.hp > sta.maxhp // 2, sta.hp < sta.maxhp)
    ok = got == (0, "Staravia", None, fs.move("Peck").pp, True, True)
    return [("the readings' Lunar Dance restores its replacement", ok,
             f"(Bibarel's HP, on the field, Staravia's status, Peck's PP, healed past half, hit after) {got}")]

def grudge_checks():
    """Grudge in a whole turn of the readings' battle on the calculator's
    real rows (approved 2026-10-14): the player's Bibarel at 1 HP uses
    Grudge before a trainer's Geodude's Tackle knocks it out, and the
    Tackle loses all its PP."""
    b, geo, bib = b8_battle([("Geodude", 30, "Sturdy", ["Tackle"])],
                            [("Bibarel", 30, "Unaware", ["Grudge"]), ("Staravia", 30, "Intimidate", ["Peck"])])
    bib.hp = 1
    pl._turn(b, ("move", fs.move("Grudge")), ("move", fs.move("Tackle")))
    ok = not bib.alive() and geo.pp["Tackle"] == 0
    return [("the readings' Grudge empties the knockout move's PP", ok,
             f"Bibarel standing {bib.alive()}, the Geodude's Tackle PP {geo.pp['Tackle']}")]

def octolock_checks():
    """Octolock in a whole turn of the readings' battle on the calculator's
    real rows (approved 2026-10-14): the player's Bibarel's Octolock holds
    a trainer's Geodude, which cannot switch, and at the turn's end it
    loses a stage of Defense and of Sp. Def."""
    b, geo, bib = b8_battle([("Geodude", 30, "Sturdy", ["Tackle"]), ("Onix", 30, "Sturdy", ["Tackle"])],
                            [("Bibarel", 30, "Unaware", ["Octolock"])])
    pl._turn(b, ("move", fs.move("Octolock")), ("move", fs.move("Tackle")))
    got = (fs.trapped(b, geo), geo.stages["def"], geo.stages["spd"])
    return [("the readings' Octolock holds its target and lowers its Defenses", got == (True, -1, -1),
             f"(trapped, Defense, Sp. Def) {got}")]

def aurora_veil_checks():
    """Aurora Veil in the readings' battle on the calculator's real rows
    (approved 2026-10-14): in hail the player's Glalie veils its side, and
    a trainer's Geodude's Tackle and Mud-Slap into it are halved; out of
    hail it fails."""
    out = {}
    for weather in (None, "Hail"):
        b, geo, gla = b8_battle([("Geodude", 30, "Sturdy", ["Tackle", "Mud-Slap"])], [("Glalie", 30, "Inner Focus", ["Aurora Veil"])])
        b.weather = weather
        before = [pl.damage_of(b, geo, gla, fs.move(m), False, True) for m in ("Tackle", "Mud-Slap")]
        pl.status_move(b, gla, fs.move("Aurora Veil"), geo, True)
        after = [pl.damage_of(b, geo, gla, fs.move(m), False, True) for m in ("Tackle", "Mud-Slap")]
        out[weather] = (b.p.aurora_veil, before, after)
    ok = (out[None][0] == 0 and out[None][1] == out[None][2] and out["Hail"][0] == 5
          and all(a == max(1, int(x * 0.5)) or abs(a - x / 2) <= 1 for x, a in zip(out["Hail"][1], out["Hail"][2])))
    return [("the readings' Aurora Veil halves both kinds of hit in hail", ok, f"(veil, before, after) {out}")]

def teatime_checks():
    """Teatime in the readings' battle on the calculator's real rows
    (approved 2026-10-14): the player's Bibarel at full HP eats its Oran
    Berry for nothing and a trainer's Geodude its Liechi Berry, which
    raises its Attack, both Berries counting as eaten."""
    b, geo, bib = b8_battle([("Geodude", 30, "Sturdy", ["Tackle"])], [("Bibarel", 30, "Unaware", ["Teatime"])])
    bib.item, geo.item = "Oran Berry", "Liechi Berry"
    pl.status_move(b, bib, fs.move("Teatime"), geo, True)
    got = (bib.item, bib.ate_berry, geo.item, geo.ate_berry, geo.stages["atk"])
    return [("the readings' Teatime feeds both their Berries", got == (None, True, None, True, 1),
             f"(Bibarel's item, eaten, Geodude's item, eaten, its Attack) {got}")]

def assist_checks():
    """Assist in the readings' battle on the calculator's real rows
    (approved 2026-10-14): the player's Bibarel's Assist uses its Staravia's
    move, Quick Attack or Peck as the battle's dice pick, into a trainer's
    Geodude, as the Bibarel's own."""
    out = []
    for pick in (0, 1):
        b, geo, bib = b8_battle([("Geodude", 30, "Sturdy", ["Tackle"])],
                                [("Bibarel", 30, "Unaware", ["Assist"]), ("Staravia", 30, "Intimidate", ["Quick Attack", "Peck"])])
        b.dice.choice = lambda kind, n, pick=pick: pick if kind == "assist" else 0
        hp = geo.hp
        pl.use_move(b, bib, fs.move("Assist"), geo, True)
        out.append((hp - geo.hp, bib.last.name if bib.last else None))
    ok = out[0][0] > 0 and out[1][0] > 0 and out[0][0] != out[1][0]
    return [("the readings' Assist uses a party member's move", ok, f"(HP taken, last move) for each pick {out}")]

def snatch_checks():
    """Snatch in a whole turn of the readings' battle on the calculator's
    real rows (approved 2026-10-14): the player's Liepard's Snatch takes a
    trainer's Geodude's Swords Dance, so the Liepard's Attack rises two
    stages and the Geodude's stays."""
    b, geo, lie = b8_battle([("Geodude", 30, "Sturdy", ["Swords Dance"])], [("Liepard", 30, "Limber", ["Snatch"])])
    pl._turn(b, ("move", fs.move("Snatch")), ("move", fs.move("Swords Dance")))
    got = (lie.stages["atk"], geo.stages["atk"], geo.pp["Swords Dance"] < fs.move("Swords Dance").pp)
    return [("the readings' Snatch takes the trainer's Swords Dance", got == (2, 0, True),
             f"(Liepard's Attack, Geodude's Attack, the Geodude paid) {got}")]

def sky_drop_checks():
    """Sky Drop in two whole turns of the readings' battle on the
    calculator's real rows (approved 2026-10-14): the player's Bibarel lifts
    a trainer's Geodude, whose Tackle that turn does nothing and which
    cannot switch; the next turn it drops the Geodude for the hit, and the
    Geodude, let go, then hits back."""
    b, geo, bib = b8_battle([("Geodude", 30, "Sturdy", ["Tackle"]), ("Onix", 30, "Sturdy", ["Tackle"])],
                            [("Bibarel", 30, "Unaware", ["Sky Drop"])])
    pl._turn(b, ("move", fs.move("Sky Drop")), ("move", fs.move("Tackle")))
    first = (geo.hp == geo.maxhp, bib.hp == bib.maxhp, fs.trapped(b, geo))
    pl._turn(b, ("move", fs.move("Sky Drop")), ("move", fs.move("Tackle")))
    second = (geo.hp < geo.maxhp, bib.hp < bib.maxhp, fs.trapped(b, geo))
    ok = first == (True, True, True) and second == (True, True, False)
    return [("the readings' Sky Drop lifts and then drops its target", ok,
             f"turn 1 (Geodude untouched, Bibarel untouched, Geodude held) {first}; turn 2 (both hit, held) {second}")]


# ---- batch 10: the follow-ups Ian approved on 2026-10-15 ----

def substitute_hit_checks():
    """A hit that breaks a Substitute in the readings' battle on the
    calculator's real rows (approved 2026-10-15): the player's Pikachu's
    Nuzzle paralyses a trainer's Machop with no Substitute, and through a
    1 HP Substitute it breaks leaves the Machop untouched and unparalysed
    (SELF_TURN_FLAG_SUBSTITUTE_HIT lasts the move)."""
    out = {}
    for sub in (0, 1):
        b, mach, pika = b8_battle([("Machop", 30, "Guts", ["Tackle"])], [("Pikachu", 30, "Static", ["Nuzzle"])],
                                  Lucky8)
        mach.sub = sub
        pl.attack(b, pika, fs.move("Nuzzle"), mach, True)
        out[sub] = (mach.status, mach.sub, mach.hp == mach.maxhp)
    ok = out == {0: ("par", 0, False), 1: (None, 0, True)}
    return [("the readings' hit that breaks a Substitute gives no added effect", ok,
             f"(status, Substitute left, full HP) by Substitute {out}")]


# ---- batch 12: the abilities and moves out of everyone's reach, and Ian's answers of 2026-10-20 ----

# The batch's checks, run after batch 11's in main.
B12 = []


def b12(fn):
    B12.append(fn)
    return fn


@b12
def sports_idle_checks():
    """Water Sport idle against a team with no damaging Fire move (Ian's
    answer of 2026-10-20; plteam.idle_sports), on Roark's real rows: batch
    11 found the team search giving Water Sport to the Barboach and the
    Goldeen of all three of Roark's goal 3 boxes in place of Mud-Slap and
    Aqua Jet; with the pools of box 1's two, each now takes the attack."""
    from . import plteam
    pools = {"Barboach": ("SPECIES_BARBOACH", "Swift Swim", ["Mud-Slap", "Icy Wind", "Water Sport", "Water Gun", "Mud Bomb"]),
             "Goldeen": ("SPECIES_GOLDEEN", "Swift Swim", ["Peck", "Water Sport", "Aqua Jet", "Scald", "Horn Attack"])}
    recs = [{"constant": c, "species": sp, "how": "test", "level": 16, "nature": "Hardy", "ivs": IV, "evs": EV,
             "ability": ab, "moves": mv, "fill": False} for sp, (c, ab, mv) in pools.items()]
    prep = plscore.prepare(plscore.parse_fight("roark"), given_side=recs)
    st, boss = prep["st"], list(prep["variants"][0][0])
    mine, _theirs, _speed = plteam.matchups(st, ["p0", "p1"], boss)
    out = {sp: plteam.pick_moves(st, k, boss, mine) for sp, k in zip(pools, ("p0", "p1"))}
    ok = ("Water Sport" not in out["Barboach"] + out["Goldeen"] and "Mud-Slap" in out["Barboach"]
          and "Aqua Jet" in out["Goldeen"])
    return [("the team search leaves Water Sport idle against Roark, who has no Fire hit", ok, f"fours {out}")]


@b12
def metal_mold_breaker_checks():
    """A Mold Breaker's Low Kick into a Heavy Metal target on the
    calculator's real rows (Ian's answer of 2026-10-20; Battler_Weight): a
    trainer's Cranidos with Mold Breaker hits the player's Bronzor, 60.5 kg
    and 121 with Heavy Metal, at 80 power, as into a Bronzor with Levitate,
    where one with Rock Head hits it at Heavy Metal's 100."""
    out = {}
    for ab, own in (("Mold Breaker", "Heavy Metal"), ("Mold Breaker", "Levitate"), ("Rock Head", "Heavy Metal")):
        b, cran, bronzor = b8_battle([("Cranidos", 30, ab, ["Low Kick"])], [("Bronzor", 30, own, ["Tackle"])])
        out[(ab, own)] = b.rolls(cran, bronzor, fs.move("Low Kick"))[-1]
    ok = (out[("Mold Breaker", "Heavy Metal")] == out[("Mold Breaker", "Levitate")]
          < out[("Rock Head", "Heavy Metal")])
    return [("the readings' Mold Breaker Low Kick reads a Heavy Metal target's own weight", ok,
             f"top roll by (attacker, target) {out}")]


@b12
def berserk_checks():
    """Berserk on the calculator's real rows (approved 2026-10-14): a
    trainer's Machop's Pound takes the player's Bibarel, given Berserk,
    from above half its HP to half or less, which raises its Sp. Atk a
    stage, so its Water Pulse hits harder; a hit that leaves it above half
    does not."""
    out = {}
    for case in ("past half", "above half"):
        b, mach, bib = b8_battle([("Machop", 30, "Guts", ["Pound"])],
                                 [("Bibarel", 30, "Berserk", ["Water Pulse"])])
        before = pl.damage_of(b, bib, mach, fs.move("Water Pulse"), False, True)
        hit = pl.damage_of(b, mach, bib, fs.move("Pound"), False, True)
        bib.hp = bib.maxhp // 2 + hit if case == "past half" else bib.maxhp
        pl.use_move(b, mach, fs.move("Pound"), bib, True)
        out[case] = (bib.stages["spa"], pl.damage_of(b, bib, mach, fs.move("Water Pulse"), False, True) > before)
    ok = out == {"past half": (1, True), "above half": (0, False)}
    return [("the readings' Berserk raises Sp. Atk as a hit takes it to half", ok, f"(Sp. Atk stage, harder) {out}")]


@b12
def multiscale_checks():
    """Multiscale on the calculator's real rows (approved 2026-10-14): a
    trainer's Machop's Karate Chop does half as much to the player's
    Dragonite at full HP as one HP below it, and a Mold Breaker Pancham's
    Karate Chop does the full damage at full HP."""
    b, mach, dra = b8_battle([("Machop", 30, "Guts", ["Karate Chop"])], [("Dragonite", 30, "Multiscale", ["Tackle"])])
    full = pl.damage_of(b, mach, dra, fs.move("Karate Chop"), False, True)
    dra.hp -= 1
    hurt = pl.damage_of(b, mach, dra, fs.move("Karate Chop"), False, True)
    b, pan, dra = b8_battle([("Pancham", 30, "Mold Breaker", ["Karate Chop"])],
                            [("Dragonite", 30, "Multiscale", ["Tackle"])])
    mold_full = pl.damage_of(b, pan, dra, fs.move("Karate Chop"), False, True)
    dra.hp -= 1
    mold_hurt = pl.damage_of(b, pan, dra, fs.move("Karate Chop"), False, True)
    ok = abs(full - hurt / 2) <= 1 and mold_full == mold_hurt
    return [("the readings' Multiscale halves a hit at full HP", ok,
             f"Machop's top roll {full} at full HP, {hurt} below; Pancham's {mold_full} and {mold_hurt}")]


@b12
def soul_heart_checks():
    """Soul Heart on the calculator's real rows (approved 2026-10-14): the
    player's Magearna's Flash Cannon knocks out a trainer's Machop, which
    raises its Sp. Atk a stage as the move ends, so its hit on the
    trainer's next Pokemon is harder."""
    b, mach, mag = b8_battle([("Machop", 30, "Guts", ["Karate Chop"]), ("Geodude", 30, "Sturdy", ["Tackle"])],
                             [("Magearna", 30, "Soul Heart", ["Flash Cannon"])])
    geo = b.b.mons[1]
    before = pl.damage_of(b, mag, geo, fs.move("Flash Cannon"), False, True)
    mach.hp = 1
    pl.use_move(b, mag, fs.move("Flash Cannon"), mach, True)
    after = pl.damage_of(b, mag, geo, fs.move("Flash Cannon"), False, True)
    ok = not mach.alive() and mag.stages["spa"] == 1 and after > before
    return [("the readings' Soul Heart raises Sp. Atk as a foe faints", ok,
             f"Sp. Atk stage {mag.stages['spa']}, Flash Cannon's top roll on Geodude {before} then {after}")]


@b12
def toxic_boost_checks():
    """Toxic Boost on the calculator's real rows (approved 2026-10-14): the
    player's poisoned Zangoose's Slash into a trainer's Machop does half
    again what a healthy one's does."""
    b, mach, zan = b8_battle([("Machop", 30, "Guts", ["Karate Chop"])], [("Zangoose", 30, "Toxic Boost", ["Slash"])])
    plain = pl.damage_of(b, zan, mach, fs.move("Slash"), False, True)
    zan.status = "psn"
    poisoned = pl.damage_of(b, zan, mach, fs.move("Slash"), False, True)
    ok = abs(poisoned - plain * 1.5) <= 1
    return [("the readings' Toxic Boost raises physical moves while poisoned", ok,
             f"Slash's top roll {plain} healthy, {poisoned} poisoned")]


@b12
def sticky_hold_knock_off_checks():
    """Knock Off into Sticky Hold on the calculator's real rows (approved
    2026-10-14): the player's Machop's Knock Off leaves a trainer's Sticky
    Hold Grimer its Black Sludge, and takes a Stench Grimer's."""
    out = {}
    for ab in ("Sticky Hold", "Stench"):
        b, gri, mach = b8_battle([("Grimer", 30, ab, ["Pound"], "Black Sludge")], [("Machop", 30, "Guts", ["Knock Off"])])
        pl.use_move(b, mach, fs.move("Knock Off"), gri, True)
        out[ab] = gri.item
    ok = out == {"Sticky Hold": "Black Sludge", "Stench": None}
    return [("the readings' Knock Off leaves a Sticky Hold holder its item", ok, f"item after {out}")]


def main():
    results = []

    # Block traps its target until Nosepass leaves; a trapped Pokemon cannot
    # switch; the AI does not Block a target already trapped.
    b = battle()
    nose, barb = b.b.cur(), b.p.cur()
    pl.status_move(b, nose, mv(nose, "Block"), barb, True)
    trapped = barb.trapped_by == nose.key and not fs.can_switch(barb)
    try:
        pl._turn(b, ("switch", 1), ("move", mv(nose, "Rock Tomb")))
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
    nose.item = "Apicot Berry"      # step 12's Nosepass holds Leftovers
    fs.hurt(b, nose, nose.hp - nose.maxhp // 4)
    results.append(("Apicot Berry raises Special Defense at a quarter HP and is eaten",
                    nose.stages["spd"] == 1 and nose.item is None, f"spd {nose.stages['spd']}, item {nose.item}"))

    # Sitrus fires on the hit that takes it to half, not at the end of the turn.
    b = battle()
    cran = boss(b, "Cranidos")
    cran.item = "Sitrus Berry"      # step 12's Cranidos holds a Lum Berry
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
    # Step 12's Cranidos has Rock Head: the check sets the ability it tests.
    cran.ability = "Mold Breaker"
    rock = mv(cran, "Rock Slide")
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

    # Big Root: a draining move (step 12's Lileep has Giga Drain) restores 30% more.
    b = battle()
    lil = boss(b, "Lileep")
    fs.switch_in(b, b.p, 1)
    lil.hp = 10
    pl.attack(b, lil, mv(lil, "Giga Drain"), b.p.cur(), True)
    dealt = b.p.cur().maxhp - b.p.cur().hp
    results.append(("Big Root raises a drain's heal by 30%", lil.hp == min(lil.maxhp, 10 + int((dealt // 2) * 1.3)),
                    f"dealt {dealt}, Lileep 10 -> {lil.hp}"))

    # Ingrain: roots the user (no switching, no second Ingrain) and heals a
    # sixteenth a turn, 30% more with Big Root. Step 12's Lileep has no
    # Ingrain, so the check gives it one.
    b = battle()
    lil = boss(b, "Lileep")
    lil.moves = list(lil.moves) + [fs.move("Ingrain")]
    lil.pp["Ingrain"] = 10
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
    cran.item = "Sitrus Berry"      # step 12's Cranidos holds a Lum Berry
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
    # The moves Roark's Lileep had before step 12, which this check is built on.
    lil.moves = [fs.move(n) for n in ("Mega Drain", "Rock Tomb", "Constrict", "Ingrain")]
    lil.pp = {m.name: 10 for m in lil.moves}
    # ...and the Speed tie it rests on (step 12's Lileep is a point slower),
    # set where the battle reads Speed, for this battle only.
    row_speed, turtwig = b.row_speed, b.p.cur()
    b.row_speed = lambda mon: row_speed(turtwig) if mon is lil else row_speed(mon)
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
    # With step 12's Calm Lileep, Constrict now ties Ingrain on the first
    # turn, so the check asks only what the two rules give: never Rock Tomb
    # at a Speed tie, and never Ingrain once rooted.
    results.append(("Lileep against Turtwig at a Speed tie: never Rock Tomb; rooted, never Ingrain, mostly Constrict",
                    picks["Ingrain"] > 0 and not picks["Rock Tomb"] and rooted["Constrict"] > 300
                    and not rooted["Rock Tomb"] and not rooted["Ingrain"],
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
            pl._turn(c, ("move", mv(g, "Rock Throw")), ("move", mv(bz, "Confuse Ray")))
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
            pl._turn(c, ("move", mv(g, "Rock Throw")), ("move", mv(bz, "Confuse Ray")))
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
    brel, tsa, gol = boss(b, "Breloom"), b.p.mons[0], b.p.mons[1]
    spore = mv(brel, "Stun Spore")
    for _ in range(20):
        pl.status_move(b, brel, spore, tsa, True)
    results.append(("Stun Spore never paralyses a Grass type, and the AI scores it -10",
                    tsa.status is None and fightai.basic(b, brel, tsa, spore, 0) == -10,
                    f"{tsa.status}, {fightai.basic(b, brel, tsa, spore, 0)}"))
    b.weather = "Sun"
    gol.ability = "Leaf Guard"
    for _ in range(20):
        pl.status_move(b, brel, spore, gol, True)
    results.append(("Leaf Guard stops status in sun", gol.status is None, f"{gol.status}"))
    b.weather = None
    for _ in range(20):
        pl.status_move(b, brel, spore, gol, True)
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
    # Step 12's Gardenia has no Lumineon, so her Ludicolo carries the gift
    # and its Watmel Berry here (Spark is neutral on it, where it hit
    # Lumineon hard, so the stay half asks less than it did).
    lum = boss(b, "Ludicolo")
    b.b.active = b.b.mons.index(lum)
    lum.item = "Watmel Berry"
    lum.moves = list(lum.moves) + [fs.move("Natural Gift")]
    lum.pp["Natural Gift"] = 10
    lum.last_hit_by = mv(vika, "Spark")
    gift = mv(lum, "Natural Gift")
    stays = 0
    for i in range(800):
        b.rng = random.Random(i)
        stays += fightai.should_switch(b, b.b, lum, vika) is None
    results.append(("Natural Gift takes its berry's type: Watmel's Fire keeps Ludicolo in about 9 in 10 against Vikavolt",
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
    results += neutralizing_gas_checks()
    results += unburden_checks()
    results += intimidate_once_checks()
    results += two_hit_checks()
    results += hit_by_hit_checks()
    results += protect_checks()
    results += pp_checks()
    results += confusion_checks()
    results += curse_rest_checks()
    results += mist_intimidate_checks()
    results += ai_field_checks()
    results += future_sight_checks()
    results += disable_and_nightmare_checks()
    results += pivot_checks()
    results += ice_body_checks()
    results += readings_damage_checks()
    results += absorbing_ability_checks()
    results += roost_checks()
    results += protean_checks()
    results += magic_guard_checks()
    results += liquid_ooze_checks()
    results += drop_answer_checks()
    results += technician_power_checks()
    results += stored_power_checks()
    results += hard_press_checks()
    results += electro_ball_checks()
    results += sacred_sword_checks()
    results += mold_breaker_checks()
    results += oblivious_taunt_checks()
    results += cursed_body_checks()
    results += justified_checks()
    results += moxie_checks()
    results += trapping_checks()
    results += accuracy_ability_checks()
    results += download_checks()
    results += weather_ability_checks()
    results += sand_force_checks()
    results += bad_dreams_checks()
    results += marvel_scale_checks()
    results += shed_skin_checks()
    results += suction_cups_checks()
    results += plus_minus_checks()
    results += stench_checks()
    results += unnerve_checks()
    results += steadfast_checks()
    results += starf_berry_checks()
    results += sticky_barb_checks()
    results += rivalry_checks()
    results += payback_checks()
    results += leech_seed_sap_checks()
    results += ghost_untrapped_checks()
    results += soundproof_status_checks()
    results += item_flinch_blocked_checks()
    results += black_sludge_checks()
    results += water_bubble_checks()
    results += eerie_spell_checks()
    results += burning_bulwark_checks()
    results += trace_checks()
    results += mummy_checks()
    results += wandering_spirit_checks()
    results += color_change_checks()
    results += forecast_checks()
    results += soak_checks()
    results += conversion_checks()
    results += conversion2_checks()
    results += camouflage_checks()
    results += burn_up_checks()
    results += double_shock_checks()
    results += skill_swap_checks()
    results += role_play_checks()
    results += entrainment_checks()
    results += worry_seed_checks()
    results += gastro_acid_checks()
    results += core_enforcer_checks()
    results += captivate_checks()
    results += vanished_status_checks()
    results += speed_down_hit_checks()
    results += bounce_paralysis_checks()
    results += weather_heal_checks()
    results += hail_checks()
    results += dream_eater_checks()
    results += focus_punch_checks()
    results += crash_checks()
    results += bind_checks()
    results += steal_item_checks()
    results += swap_items_checks()
    results += pluck_checks()
    results += chatter_checks()
    results += stockpile_checks()
    results += natural_gift_checks()
    results += lower_sp_atk_checks()
    results += rollout_checks()
    results += wake_up_slap_checks()
    results += throat_chop_checks()
    results += minimize_checks()
    results += charge_checks()
    results += lucky_chant_checks()
    results += psych_up_checks()
    results += lock_on_checks()
    results += foresight_checks()
    results += trainer_magnitude_checks()
    results += trainer_return_checks()
    results += smack_down_checks()
    results += gravity_checks()
    results += mimic_checks()
    results += mirror_move_checks()
    results += copycat_checks()
    results += fling_checks()
    results += imprison_checks()
    results += baton_pass_checks()
    results += row_neutral_checks()
    results += refresh_checks()
    results += wring_out_checks()
    results += miracle_eye_checks()
    results += acupressure_checks()
    results += trainer_frustration_checks()
    results += secret_power_checks()
    results += snore_checks()
    results += raise_speed_hit_checks()
    results += trump_card_checks()
    results += teeter_dance_checks()
    results += smelling_salts_checks()
    results += magic_coat_checks()
    results += present_checks()
    results += water_sport_checks()
    results += acrobatics_checks()
    results += guard_swap_checks()
    results += power_swap_checks()
    results += psycho_shift_checks()
    results += memento_checks()
    results += sketch_checks()
    results += me_first_checks()
    results += nature_power_checks()
    results += power_trick_checks()
    results += bide_checks()
    results += transform_checks()
    results += sp_def_2_checks()
    results += tearful_look_checks()
    results += venom_drench_checks()
    results += false_swipe_checks()
    results += clear_smog_checks()
    results += incinerate_checks()
    results += life_dew_checks()
    results += mud_sport_checks()
    results += punishment_checks()
    results += sticky_web_checks()
    results += defog_checks()
    results += strength_sap_checks()
    results += parting_shot_checks()
    results += dragon_tail_checks()
    results += side_guard_checks()
    results += heat_crash_checks()
    results += healing_wish_checks()
    results += guard_split_checks()
    results += power_split_checks()
    results += embargo_checks()
    results += magic_room_checks()
    results += relic_song_checks()
    results += clanging_scales_checks()
    results += matcha_gotcha_checks()
    results += fell_stinger_checks()
    results += prevent_escape_hit_checks()
    results += poltergeist_checks()
    results += belch_checks()
    results += first_impression_checks()
    results += axe_kick_checks()
    results += always_critical_checks()
    results += clangorous_soul_checks()
    results += heart_swap_checks()
    results += heal_pulse_checks()
    results += lunar_dance_checks()
    results += grudge_checks()
    results += octolock_checks()
    results += aurora_veil_checks()
    results += teatime_checks()
    results += assist_checks()
    results += snatch_checks()
    results += sky_drop_checks()
    results += substitute_hit_checks()
    results += dragon_tail_order_checks()
    results += knock_off_first_checks()
    results += taunt_before_confusion_checks()
    results += forced_out_checks()
    results += charge_ends_checks()
    results += ingrain_grounds_checks()
    results += fog_checks()
    results += rematch_terrain_checks()
    results += borrowed_twin_checks()
    results += meloetta_form_checks()
    results += options_rule_checks()
    results += idle_list_checks()
    results += merge_key_checks()
    for fn in B11:
        results += fn()
    for fn in B12:
        results += fn()

    width = max(len(r[0]) for r in results)
    for name, ok, note in results:
        print(f"  {'ok  ' if ok else 'FAIL'}  {name:{width}}  {note}")
    passed = sum(1 for r in results if r[1])
    print(f"\n{passed}/{len(results)} passed")
    return 0 if passed == len(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())

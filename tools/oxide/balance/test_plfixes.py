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

    width = max(len(r[0]) for r in results)
    for name, ok, note in results:
        print(f"  {'ok  ' if ok else 'FAIL'}  {name:{width}}  {note}")
    passed = sum(1 for r in results if r[1])
    print(f"\n{passed}/{len(results)} passed")
    return 0 if passed == len(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())

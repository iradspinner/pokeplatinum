"""The fight simulator's trainer AI, routine by routine, against the game's
own AI at HEAD (src/battle/trainer_ai/script.s and trainer_ai.c): the
Scoring Agent's audit of 2026-09-30.

Each check builds a small battle with the Pokemon and moves the routine
needs, sets the state it reads, and calls the routine directly with the
dice fixed: PASS makes every chance(b, p) succeed, FAIL makes every one
fail, so both branches of a random check are pinned.

    PYTHONPATH=. python3 -m tools.oxide.balance.test_fightai
"""
import functools
import random
import sys

from . import fightai as ai, fightsim as fs, perfectline as pl

IV = {k: 31 for k in ("hp", "at", "df", "sp", "sa", "sd")}
EV = {k: 0 for k in IV}


class Dice:
    """A stand-in for the battle's random source that always returns one
    value: 0.0 passes every chance check, 0.9999 fails every one."""

    def __init__(self, value):
        self.value = value

    def random(self):
        return self.value

    def choice(self, seq):
        return seq[0]


PASS, FAIL = 0.0, 0.9999


@functools.lru_cache(maxsize=None)
def _prepared(boss, player, split, weather):
    """The calculator's rows for one pair of parties, made once: each party
    is a tuple of (species, level, ability, moves, item)."""
    boss_recs = [{"species": sp, "level": lv, "ability": ab, "item": it, "nature": "Hardy",
                  "ivs": IV, "evs": EV, "moves": list(mv)} for sp, lv, ab, mv, it in boss]
    player_recs = [{"constant": "SPECIES_" + sp.upper().replace(" ", "_").replace("-", "_"),
                    "species": sp, "how": "test", "level": lv, "nature": "Hardy", "ivs": IV,
                    "evs": EV, "ability": ab, "moves": list(mv), "fill": False}
                   for sp, lv, ab, mv, _it in player]
    return fs.prepare(split, [boss_recs], weather, given_side=player_recs)


def battle(boss, player, split="Roark", weather=None, flags=7, dice=PASS):
    """A fresh battle with each side's first Pokemon in. boss and player are
    lists of (species, level, ability, [moves]) or with a fifth item."""
    def norm(party):
        return tuple((p[0], p[1], p[2], tuple(p[3]), p[4] if len(p) > 4 else None) for p in party)
    st = _prepared(norm(boss), norm(player), split, weather)
    b = pl.make_battle(st, [f"p{i}" for i in range(len(player))], st["bosses"][0], flags, 0)
    for m in b.p.mons:
        m.item = next((p[4] for p in player if p[0] == m.species and len(p) > 4), None)
    b.rng = Dice(dice)
    return b


def mv(mon, name):
    return next(m for m in mon.moves if m.name == name)


def roll(b, dice):
    """Fix the battle's dice to PASS or FAIL."""
    b.rng = Dice(dice)
    return b


def checks():
    """[(label, ok, note)] for every routine."""
    out = []
    for fn in CHECKS:
        try:
            out += fn()
        except Exception as exc:          # a check that cannot run is a failure, named
            out.append((fn.__name__, False, f"{type(exc).__name__}: {exc}"))
    return out


CHECKS = []


def check(fn):
    CHECKS.append(fn)
    return fn


@check
def fixture():
    b = battle([("Geodude", 16, "Sturdy", ["Rock Throw", "Defense Curl"])],
               [("Barboach", 16, "Oblivious", ["Mud Bomb", "Water Gun"])])
    u, t = b.b.cur(), b.p.cur()
    f = ai.figure(b, u, t, mv(u, "Rock Throw"))
    return [("the fixture builds a battle the AI can read", u.species == "Geodude" and f is not None and f > 0,
             f"{u} vs {t}, Rock Throw {f}")]


# ---- Expert, routine by routine ------------------------------------------------------------------

class Seq(Dice):
    """Dice that return a given sequence, then repeat its last value: for
    the rows where all-pass and all-fail cannot tell two readings apart."""

    def __init__(self, values):
        self.values = list(values)

    def random(self):
        return self.values.pop(0) if len(self.values) > 1 else self.values[0]


EX_BOSS = [("Snorlax", 40, "Thick Fat", ["Body Slam", "Crunch", "Earthquake", "Fire Punch"]),
           ("Gengar", 40, "Levitate", ["Shadow Ball", "Sludge Bomb", "Thunderbolt", "Focus Blast"])]
EX_PLAYER = [("Machamp", 40, "Guts", ["Cross Chop", "Rock Slide"]),
             ("Blissey", 40, "Natural Cure", ["Seismic Toss"])]


def hp(m, pct):
    """Set m's HP so that frac() reads pct, as AICmd_IfHPPercent* would."""
    m.hp = max(1, pct * m.maxhp // 100) if pct else 0
    while 100 * m.hp // m.maxhp < pct:
        m.hp += 1


def speeds(b, user, foe):
    """Fix the two Speeds the AI compares (user: the trainer's Pokemon)."""
    b.speed = lambda m: user if m.side == "b" else foe


def moves(m, *names):
    m.moves = [fs.move(n) for n in names]
    m.pp = {x.name: x.pp for x in m.moves}


def ex(move, setup=None, dice=PASS):
    """Expert's score for Snorlax's move against Machamp, after setup(b, u,
    t); Snorlax moves first unless setup says otherwise."""
    b = battle(EX_BOSS, EX_PLAYER)
    u, t = b.b.cur(), b.p.cur()
    moves(u, move, "Body Slam")
    speeds(b, 100, 50)
    if setup:
        setup(b, u, t)
    b.rng = dice if isinstance(dice, Dice) else Dice(dice)
    return ai.expert(b, u, t, fs.move(move))


def _t(**kw):
    """A setup that sets fields on the user (u_*), the target (t_*) or the
    battle (b_*), HP by percent (u_hp, t_hp), stages (u_atk and so on),
    speed (slower=True or tie=True), and the target's last and shown moves."""
    def setup(b, u, t):
        for k, v in kw.items():
            who, _, field = k.partition("_")
            mon = {"u": u, "t": t}.get(who)
            if k == "slower":
                speeds(b, 50, 100)
            elif k == "tie":
                speeds(b, 80, 80)
            elif k == "weather":
                b.weather = v
            elif k == "trick_room":
                b.trick_room = v
            elif who == "b":
                setattr(b, field, v)
            elif field == "hp":
                hp(mon, v)
            elif field in fs.STAGE_KEYS:
                mon.stages[field] = v
            elif field == "last":
                mon.last = fs.move(v) if v else None
            elif field == "shown":
                mon.shown = [fs.move(n) for n in v]
            elif field == "moves":
                moves(mon, *v)
            else:
                setattr(mon, field, v)
    return setup


def _last_pokemon(b):
    for m in b.b.mons[1:]:
        m.hp = 0


# (label, move, setup, score with every chance passing, score with every one failing)
EXPERT_ROWS = [
    ("StatusSleep, with Dream Eater", "Hypnosis", _t(u_moves=("Hypnosis", "Dream Eater")), 1, 0),
    ("DrainMove, Draining Kiss into a Fire type", "Draining Kiss", _t(t_types=["Fire"]), -3, 0),
    ("Explosion, faster at full HP, foe evasion +4", "Explosion", _t(t_eva=4), -5, -1),
    ("Explosion, slower at 25%", "Explosion", _t(slower=True, u_hp=25), 2, 0),
    ("DreamEater, sleeping foe", "Dream Eater", _t(t_status="slp"), 3, 0),
    ("DreamEater, Dark foe", "Dream Eater", _t(t_types=["Dark"]), -1, -1),
    ("MirrorMove, foe's last Thunder Wave", "Mirror Move", _t(t_last="Thunder Wave"), 2, 0),
    ("MirrorMove, foe's last Tackle", "Mirror Move", _t(t_last="Tackle"), -1, 0),
    ("StatusAttackUp, Swords Dance at full HP", "Swords Dance", None, 2, 0),
    ("StatusAttackUp, Hone Claws at full HP", "Hone Claws", None, 2, 0),
    ("StatusAttackUp, Work Up at 60%", "Work Up", _t(u_hp=60), -2, 0),
    ("StatusDefenseUp, Iron Defense at 60%, foe's last Flamethrower", "Iron Defense",
     _t(u_hp=60, t_last="Flamethrower"), -2, -2),
    ("StatusDefenseUp, Coil at full HP", "Coil", None, 2, 0),
    ("StatusSpeedUp, Agility slower", "Agility", _t(slower=True), 3, 0),
    ("StatusSpeedUp, Autotomize faster", "Autotomize", None, -3, -3),
    ("StatusSpAttackUp, Nasty Plot at 60%", "Nasty Plot", _t(u_hp=60), -2, 0),
    ("StatusSpDefenseUp, Calm Mind at 60%, foe's last Tackle", "Calm Mind", _t(u_hp=60, t_last="Tackle"), -2, -2),
    ("StatusSpDefenseUp, Take Heart at full HP", "Take Heart", None, 2, 0),
    ("(none) Stockpile has no Expert routine", "Stockpile", None, 0, 0),
    ("StatusEvasionUp, at 45% rooted, foe badly poisoned and cursed", "Double Team",
     _t(u_hp=45, u_eva=1, u_ingrained=True, t_status="tox", t_cursed=True), 6, 0),
    ("BypassAccuracyMove, foe evasion +5", "Aerial Ace", _t(t_eva=5), 2, 1),
    ("StatusAttackDown, Growl, foe's last Flamethrower", "Growl", _t(t_last="Flamethrower"), -2, 0),
    ("StatusAttackDown, Charm at 80%, foe at 60% and Attack -1", "Charm", _t(u_hp=80, t_hp=60, t_atk=-1), -4, -4),
    ("StatusAttackDown, Noble Roar, foe's last Flamethrower", "Noble Roar", _t(t_last="Flamethrower"), -2, 0),
    ("StatusDefenseDown, Screech at 60%", "Screech", _t(u_hp=60), -2, 0),
    ("StatusDefenseDown, Tickle at 60%", "Tickle", _t(u_hp=60), -2, 0),
    ("SpeedDownOnHit, Icy Wind slower into a Grass type", "Icy Wind", _t(slower=True, t_types=["Grass"]), 2, 0),
    ("SpeedDownOnHit, Icy Wind into a Water type", "Icy Wind", _t(slower=True, t_types=["Water"]), 0, 0),
    ("SpeedDownOnHit, Bubble Beam is not named", "Bubble Beam", _t(slower=True), 0, 0),
    ("SpeedDownOnHit, Rock Tomb on a speed tie counts as not slower", "Rock Tomb", _t(tie=True, t_types=["Normal"]), -3, -3),
    ("StatusSpeedDown, Scary Face slower", "Scary Face", _t(slower=True), 2, 0),
    ("StatusSpAttackDown, Eerie Impulse, foe has not moved", "Eerie Impulse", None, -2, 0),
    ("StatusAccuracyDown, Sand Attack, foe badly poisoned", "Sand Attack", _t(t_status="tox"), 2, 0),
    ("StatusAccuracyDown, at 60%, foe accuracy -1", "Sand Attack", _t(u_hp=60, t_acc=-1), -3, 0),
    ("StatusEvasionDown, Sweet Scent at 60%", "Sweet Scent", _t(u_hp=60), -2, 0),
    ("Haze, foe Attack +3", "Haze", _t(t_atk=3), 3, 0),
    ("Haze, nothing raised", "Haze", None, -1, 0),
    ("ClearSmog, foe Sp. Atk +3", "Clear Smog", _t(t_spa=3), 3, 0),
    ("Bide, at 80%", "Bide", _t(u_hp=80), -2, -2),
    ("ForceSwitch, Roar, foe in for four turns", "Roar", _t(t_turns_in=4), 4, 0),
    ("ForceSwitch, Dragon Tail with nothing to gain", "Dragon Tail", None, -3, -3),
    ("Conversion, at 80% after the first turn", "Conversion", _t(u_hp=80, b_turn=2), -4, -2),
    ("Synthesis, slower at 50% in rain", "Synthesis", _t(slower=True, u_hp=50, weather="Rain"), 0, -2),
    ("Synthesis, Shore Up skips the weather", "Shore Up", _t(slower=True, u_hp=50, weather="Sand"), 2, 0),
    ("Recovery, faster at 50% (the faster heal)", "Recover", _t(u_hp=50), -8, -8),
    ("Recovery, Strength Sap slower at 50%", "Strength Sap", _t(slower=True, u_hp=50), 2, 0),
    ("ToxicLeechSeed, both at 40%, with Protect", "Toxic",
     _t(u_hp=40, t_hp=40, u_moves=("Toxic", "Tackle", "Protect")), -4, 0),
    ("LightScreen, foe's last Flamethrower", "Light Screen", _t(t_last="Flamethrower"), 2, 0),
    ("Reflect, foe has not moved (move 0 is physical)", "Reflect", None, 2, 0),
    ("AuroraVeil, foe's last Flamethrower", "Aurora Veil", _t(t_last="Flamethrower"), 2, 0),
    ("Rest, faster at 45%", "Rest", _t(u_hp=45), -3, 0),
    ("Rest, slower at 50%", "Rest", _t(slower=True, u_hp=50), 3, 0),
    ("OHKOMove", "Sheer Cold", None, 1, 0),
    ("SuperFang, foe at 50%", "Super Fang", _t(t_hp=50), -1, -1),
    ("BindingMove, Mean Look on a cursed foe", "Mean Look", _t(t_cursed=True), 1, 0),
    ("HighCritical, Slash, neutral", "Slash", _t(t_types=["Water"]), 1, 0),
    ("HighCritical, Drill Run into Levitate reads as immune", "Drill Run", _t(t_ability="Levitate"), 0, 0),
    ("HighCritical, Frost Breath into a Grass type", "Frost Breath", _t(t_types=["Grass"]), 1, 0),
    ("SpeedUpOnHit, Esper Wing faster (not the high-critical routine)", "Esper Wing", None, 0, 0),
    ("Swagger with Psych Up, foe Attack +0, first turn", "Swagger", _t(u_moves=("Swagger", "Psych Up")), -5, -5),
    ("Swagger with Psych Up, foe Attack -3, first turn", "Swagger",
     _t(u_moves=("Swagger", "Psych Up"), t_atk=-3), 5, 5),
    ("Swagger alone, foe at 40%", "Swagger", _t(t_hp=40), -1, -1),
    ("Flatter, foe at full HP", "Flatter", None, 1, 0),
    ("StatusConfuse, foe at 25%", "Confuse Ray", _t(t_hp=25), -3, -2),
    ("StatusPoison, user at 40%", "Poison Powder", _t(u_hp=40), -1, -1),
    ("StatusParalyze, slower", "Thunder Wave", _t(slower=True), 3, 0),
    ("StatusParalyze, faster at 60%", "Thunder Wave", _t(u_hp=60), -1, -1),
    ("VitalThrow, faster at 50%", "Vital Throw", _t(u_hp=50), -1, 0),
    ("Substitute, Focus Punch, 60%, foe's last Confuse Ray, foe unconfused", "Substitute",
     _t(u_hp=60, u_moves=("Substitute", "Focus Punch"), t_last="Confuse Ray"), 0, 0),
    ("Substitute, foe's last Leech Seed, foe unseeded", "Substitute", _t(t_last="Leech Seed"), 1, 0),
    # Hyper Beam and Giga Impact lost their recharge in the move reworks
    # (2026-10-06); Prismatic Laser and Eternabeam keep it.
    ("RechargeTurn, Prismatic Laser with Truant", "Prismatic Laser", _t(u_ability="Truant", u_hp=50), 1, 0),
    ("RechargeTurn, Eternabeam faster at 50%", "Eternabeam", _t(u_hp=50), -1, -1),
    ("RecoilMove, Raging Fury with Rock Head", "Raging Fury", _t(u_ability="Rock Head", t_types=["Normal"]), 1, 1),
    ("ShellTrap, foe's last Tackle", "Shell Trap", _t(t_last="Tackle", t_types=["Normal"]), 0, 0),
    ("ShellTrap, foe yet to move", "Shell Trap", _t(t_types=["Normal"]), 0, 0),
    ("ShellTrap, foe's last Flamethrower", "Shell Trap", _t(t_last="Flamethrower", t_types=["Normal"]), -2, -2),
    ("ShellTrap, into a Water type", "Shell Trap", _t(t_last="Flamethrower", t_types=["Water"]), -1, -1),
    ("Disable, foe's last Tackle", "Disable", _t(t_last="Tackle"), 1, 1),
    ("Counter, foe's last Tackle", "Counter", _t(t_last="Tackle"), 1, 0),
    ("Counter, foe's last Flamethrower", "Counter", _t(t_last="Flamethrower"), -1, -1),
    ("Counter, a Psychic foe that has not moved", "Counter", _t(t_types=["Psychic"]), 4, 0),
    ("Counter, knowing Mirror Coat, at 40%", "Counter", _t(u_hp=40, u_moves=("Counter", "Mirror Coat")), 3, 0),
    ("MirrorCoat, knowing Counter", "Mirror Coat", _t(u_moves=("Mirror Coat", "Counter")), 4, 0),
    ("MirrorCoat, a Water foe that has not moved", "Mirror Coat", _t(t_types=["Water"]), 0, 0),
    ("MirrorCoat, at 25%, foe's last Tackle", "Mirror Coat", _t(u_hp=25, t_last="Tackle"), -3, -1),
    ("Encore, foe's last Swords Dance", "Encore", _t(t_last="Swords Dance"), 3, 0),
    ("Encore, foe's last Tackle", "Encore", _t(t_last="Tackle"), -2, -2),
    ("PainSplit, faster at 30%, foe at 90%", "Pain Split", _t(u_hp=30, t_hp=90), 1, 1),
    ("Nightmare, Snore", "Snore", None, 2, 2),
    ("LockOn", "Lock-On", None, 2, 0),
    ("SleepTalk, asleep", "Sleep Talk", _t(u_status="slp"), 10, 10),
    ("SleepTalk, awake", "Sleep Talk", None, -5, -5),
    ("DestinyBond, faster at 25%", "Destiny Bond", _t(u_hp=25), 3, -1),
    ("DestinyBond, slower at 25%", "Destiny Bond", _t(slower=True, u_hp=25), -1, -1),
    ("Reversal, Flail faster at 5%", "Flail", _t(u_hp=5), 2, 1),
    ("Reversal, slower at 50%", "Reversal", _t(slower=True, u_hp=50), 0, 0),
    ("HealBell, nobody statused", "Heal Bell", None, -5, -5),
    ("Thief, the foe's item not named", "Thief", None, -2, -2),
    ("Curse, Defense +0", "Curse", None, 3, 0),
    ("Curse, with Gyro Ball, Defense +1", "Curse", _t(u_def=1, u_moves=("Curse", "Gyro Ball")), 3, 0),
    ("Curse, a Ghost user at 60%", "Curse", _t(u_types=["Ghost"], u_hp=60), -1, -1),
    ("Protect, nothing", "Protect", None, 1, 0),
    ("Protect, user under Perish Song", "Protect", _t(u_perish=2), -2, -2),
    ("Protect, foe seen using Recover", "Protect", _t(t_shown=["Recover"]), -2, -2),
    ("Protect, foe badly poisoned, run of one", "Protect", _t(t_status="tox", u_protect_run=1), -1, 1),
    ("Spikes, with Roar", "Spikes", _t(u_moves=("Spikes", "Roar")), 2, 0),
    ("Spikes, Sticky Web", "Sticky Web", None, 1, 0),
    ("ToxicSpikes, with Whirlwind", "Toxic Spikes", _t(u_moves=("Toxic Spikes", "Whirlwind")), 2, 0),
    ("StealthRock, with Dragon Tail (not Roar)", "Stealth Rock", _t(u_moves=("Stealth Rock", "Dragon Tail")), 1, 0),
    ("Foresight, a Ghost foe", "Foresight", _t(t_types=["Ghost"]), 2, 0),
    ("Foresight, nothing", "Foresight", None, -2, -2),
    ("Endure, at 20%", "Endure", _t(u_hp=20), 1, 0),
    ("Endure, at 2%", "Endure", _t(u_hp=2), -1, -1),
    ("BatonPass, Attack +3, faster at 50%", "Baton Pass", _t(u_atk=3, u_hp=50), 2, 0),
    ("BatonPass, nothing raised", "Baton Pass", None, -2, -2),
    ("Pursuit, first turn, foe shown U-turn", "Pursuit", _t(u_turns_in=0, t_shown=["U-turn"]), 2, 0),
    ("RainDance, Swift Swim slower", "Rain Dance", _t(slower=True, u_ability="Swift Swim"), 1, 1),
    ("RainDance, Swift Swim on a speed tie (faster half the time)", "Rain Dance",
     _t(tie=True, u_ability="Swift Swim"), 0, 1),
    ("RainDance, Rain Dish in clear weather", "Rain Dance", _t(u_ability="Rain Dish"), 1, 1),
    ("SunnyDay, Flower Gift in clear weather", "Sunny Day", _t(u_ability="Flower Gift"), 1, 1),
    ("SunnyDay, Leaf Guard paralysed", "Sunny Day", _t(u_ability="Leaf Guard", u_status="par"), 0, 0),
    ("BellyDrum, at 89%", "Belly Drum", _t(u_hp=89), -2, -2),
    ("PsychUp, foe Attack +3", "Psych Up", _t(t_atk=3), 1, 1),
    ("ChargeTurnNoInvuln, Solar Beam in sun", "Solar Beam", _t(weather="Sun"), 2, 2),
    ("ChargeTurnNoInvuln, Solar Beam into a Fire type", "Solar Beam", _t(t_types=["Fire"]), -2, -2),
    ("ChargeTurnNoInvuln, at 38%", "Solar Beam", _t(u_hp=38), -1, -1),
    ("Thunder, Hurricane in sun", "Hurricane", _t(weather="Sun", t_types=["Normal"]), -3, 0),
    ("RainStorm, Bleakwind Storm in sun", "Bleakwind Storm", _t(weather="Sun", t_types=["Normal"]), 0, 0),
    # Dig and Dive became one-turn hits in the move reworks (2026-10-06);
    # Bounce and Fly keep the routine.
    ("ChargeTurnWithInvuln, Bounce faster", "Bounce", _t(t_types=["Normal"]), 1, 0),
    ("ChargeTurnWithInvuln, Bounce slower", "Bounce", _t(slower=True, t_types=["Normal"]), 0, 0),
    ("ChargeTurnWithInvuln, Bounce into a Rock type", "Bounce", _t(t_types=["Rock"]), -1, -1),
    ("ChargeTurnWithInvuln, Fly with a Power Herb", "Fly", _t(u_item="Power Herb"), 2, 2),
    ("FakeOut, First Impression", "First Impression", None, 2, 2),
    ("SpitUp, two Stockpiles", "Spit Up", _t(u_stockpile=2), 2, 0),
    ("Hail, in rain with Blizzard and Ice Body", "Hail",
     _t(weather="Rain", u_ability="Ice Body", u_moves=("Hail", "Blizzard")), 5, 5),
    ("Facade, burned", "Facade", _t(u_status="brn"), 1, 1),
    ("FocusPunch, behind a Substitute", "Focus Punch", _t(u_sub=20, t_types=["Normal"]), 5, 5),
    ("FocusPunch, second turn out", "Focus Punch", _t(u_turns_in=1, t_types=["Normal"]), 1, 0),
    ("SmellingSalts, paralysed foe", "Smelling Salts", _t(t_status="par"), 1, 1),
    ("Trick, holding a Choice Scarf", "Trick", _t(u_item="Choice Scarf"), 5, 5),
    ("Trick, holding Leftovers", "Trick", _t(u_item="Leftovers"), -3, -3),
    ("ChangeUserAbility, Role Play for Speed Boost", "Role Play", _t(t_ability="Speed Boost"), 2, 0),
    ("Ingrain changes nothing", "Ingrain", None, 0, 0),
    ("Superpower, faster at full HP", "Superpower", _t(t_types=["Normal"]), -1, -1),
    ("Superpower, faster at 35%", "Superpower", _t(u_hp=35, t_types=["Normal"]), 0, 0),
    ("Superpower, Attack -1, slower at 70%", "Superpower",
     _t(u_atk=-1, slower=True, u_hp=70, t_types=["Normal"]), -1, -1),
    ("MagicCoat, second turn, foe at full HP", "Magic Coat", _t(u_turns_in=1), -1, 0),
    ("Recycle, a Lum Berry to bring back", "Recycle", _t(u_recycle="Lum Berry"), 1, 0),
    ("Revenge, Avalanche, healthy foe", "Avalanche", None, 2, -2),
    ("BrickBreak, Reflect up", "Brick Break", lambda b, u, t: b.p.screens.update(Reflect=5), 1, 1),
    ("KnockOff, second turn out", "Knock Off", _t(u_turns_in=1), 1, 0),
    ("Endeavor, faster at 40%", "Endeavor", _t(u_hp=40), 1, 1),
    ("Endeavor, faster at 41%", "Endeavor", _t(u_hp=41), -1, -1),
    ("WaterSpout, Eruption faster at 50%", "Eruption", _t(u_hp=50, t_types=["Normal"]), -1, -1),
    ("Imprison, second turn", "Imprison", _t(u_turns_in=1), 2, 0),
    ("Refresh, foe at 49%", "Refresh", _t(t_hp=49), -1, -1),
    ("Snatch, first turn", "Snatch", _t(u_turns_in=0), 2, 0),
    ("MudSport, an Electric foe", "Mud Sport", _t(t_types=["Electric"]), 1, 1),
    ("Overheat, faster at 60%", "Overheat", _t(u_hp=60, t_types=["Normal"]), -1, -1),
    ("CloseCombat, slower at 81%", "Close Combat", _t(slower=True, u_hp=81, t_types=["Normal"]), 0, 0),
    ("DragonDance, slower at 40%", "Dragon Dance", _t(slower=True, u_hp=40), 1, 0),
    ("DragonDance, slower at 40%, the coin failing and the next roll passing", "Dragon Dance",
     _t(slower=True, u_hp=40), Seq([0.9999, 0.0]), 0),
    ("DragonDance, Quiver Dance slower", "Quiver Dance", _t(slower=True), 1, 0),
    ("Gravity, a Flying foe", "Gravity", _t(t_types=["Flying"]), 1, 0),
    ("MiracleEye, a Dark foe", "Miracle Eye", _t(t_types=["Dark"]), 2, 0),
    ("WakeUpSlap, sleeping foe", "Wake-Up Slap", _t(t_status="slp", t_types=["Normal"]), 1, 1),
    ("HammerArm, slower", "Hammer Arm", _t(slower=True, t_types=["Normal"]), 1, 1),
    ("GyroBall changes nothing", "Gyro Ball", None, 0, 0),
    ("Brine, foe at 50%", "Brine", _t(t_hp=50, t_types=["Normal"]), 2, 1),
    ("Feint, foe seen using Protect, run 3", "Feint", _t(t_shown=["Protect"], t_protect_run=3), -2, -2),
    ("Pluck, Bug Bite on the first turn", "Bug Bite", _t(u_turns_in=0, t_types=["Normal"]), 2, 0),
    ("Tailwind, faster at full HP", "Tailwind", None, -1, 0),
    ("Tailwind, slower at 50%", "Tailwind", _t(slower=True, u_hp=50), 1, 0),
    ("Tailwind, a tie at full HP", "Tailwind", _t(tie=True), -1, 0),
    ("Acupressure, at 50%", "Acupressure", _t(u_hp=50), -1, -1),
    ("MetalBurst, foe asleep", "Metal Burst", _t(t_status="slp"), -1, -1),
    ("Payback, slower at full HP", "Payback", _t(slower=True, t_types=["Normal"]), 1, 0),
    ("Payback, slower at 29%", "Payback", _t(slower=True, u_hp=29, t_types=["Normal"]), 0, 0),
    ("Assurance, slower", "Assurance", _t(slower=True, t_types=["Normal"]), 1, 0),
    ("Embargo", "Embargo", None, 1, 0),
    ("Fling, holding nothing", "Fling", _t(u_item=None, t_types=["Normal"]), -2, -2),
    ("PsychoShift, healthy user", "Psycho Shift", None, -10, -10),
    ("TrumpCard, one PP left", "Trump Card", _t(u_pp={"Trump Card": 1}, t_types=["Normal"]), 3, 3),
    ("HealBlock, foe seen using Recover", "Heal Block", _t(t_shown=["Recover"]), 1, 0),
    ("WringOut, foe at full HP, faster", "Wring Out", _t(t_types=["Normal"]), 3, 2),
    ("PowerTrick, at 30%", "Power Trick", _t(u_hp=30), -2, -2),
    ("GastroAcid, foe at 25%", "Gastro Acid", _t(t_hp=25), -2, 0),
    ("LuckyChant, at 69%", "Lucky Chant", _t(u_hp=69), -1, -1),
    ("MeFirst, slower", "Me First", _t(slower=True), -2, -2),
    ("Copycat, faster, foe's last Thunder Wave", "Copycat", _t(t_last="Thunder Wave"), 2, 0),
    ("PowerSwap, foe +4 Attack and Sp. Atk", "Power Swap", _t(t_atk=4, t_spa=4), 5, 0),
    ("Punishment, foe stages summing to 7", "Punishment", _t(t_atk=4, t_spa=3, t_types=["Normal"]), 4, 0),
    ("LastResort, the other moves used", "Last Resort", _t(u_last_resort_count=1, t_types=["Normal"]), 1, 1),
    ("WorrySeed, foe seen using Rest", "Worry Seed", _t(t_shown=["Rest"]), 3, 1),
    ("SuckerPunch, into a Fighting type", "Sucker Punch", None, -1, -1),
    ("HeartSwap, foe +2 Attack", "Heart Swap", _t(t_atk=2), 1, 1),
    ("AquaRing, at 30%", "Aqua Ring", _t(u_hp=30), 1, 0),
    ("MagnetRise, a Ground foe seen using Earthquake", "Magnet Rise",
     _t(t_types=["Ground"], t_shown=["Earthquake"]), 2, 2),
    ("Defog, at 60% with nothing anywhere", "Defog", _t(u_hp=60), -2, 0),
    ("TrickRoom, slower", "Trick Room", _t(slower=True), 3, 0),
    ("TrickRoom, a last Pokemon at 30%", "Trick Room",
     lambda b, u, t: (speeds(b, 50, 100), hp(u, 30), _last_pokemon(b)), 0, 0),
    ("Blizzard, into a Water type", "Blizzard", _t(t_types=["Water"]), -3, 0),
    ("Captivate, foe's last Tackle", "Captivate", _t(t_last="Tackle"), -1, 0),
    ("RecoilMove, Brave Bird into a Steel type with Rock Head", "Brave Bird",
     _t(t_types=["Steel"], u_ability="Rock Head"), 0, 0),
    ("RecoilMove, neutral with Rock Head", "Brave Bird", _t(t_types=["Normal"], u_ability="Rock Head"), 1, 1),
    ("HealingWish, faster at full HP", "Healing Wish", None, -5, 0),
    ("Hex, a burned Normal foe (immune)", "Hex", _t(t_status="brn", t_types=["Normal"]), -1, -1),
    ("Venoshock, a poisoned foe", "Venoshock", _t(t_status="psn", t_types=["Normal"]), 1, 1),
    ("Acrobatics, holding nothing", "Acrobatics", _t(t_types=["Normal"]), 1, 1),
    ("BoltBeak, a speed tie", "Bolt Beak", _t(tie=True, t_types=["Normal"]), 1, 0),
    ("RapidSpin, Stealth Rock on its side, slower", "Rapid Spin",
     lambda b, u, t: (speeds(b, 50, 100), b.b.hazards.update(rocks=1)), 3, 2),
    ("RapidSpin, into a Ghost type", "Rapid Spin", _t(t_types=["Ghost"]), -1, -1),
    ("SpeedUpOnHit, Flame Charge slower", "Flame Charge", _t(slower=True, t_types=["Normal"]), 1, 0),
    ("SpeedUpOnHit, under Trick Room", "Flame Charge", _t(slower=True, trick_room=5, t_types=["Normal"]), 0, 0),
    ("MortalSpin, seeded", "Mortal Spin", _t(u_seeded=True, t_types=["Normal"]), 2, 2),
    ("PartingShot, a bench that hits harder, faster, foe at full HP", "Parting Shot",
     _t(u_moves=("Parting Shot",)), 3, 1),
    ("PartingShot, the last Pokemon, as Growl", "Parting Shot",
     lambda b, u, t: (_last_pokemon(b), setattr(t, "last", fs.move("Flamethrower"))), -2, 0),
    ("UTurn, faster, foe at full HP, the bench hits harder", "U-turn",
     _t(t_types=["Normal"], u_moves=("U-turn",)), 3, 1),
    ("UTurn, with a super-effective attack", "U-turn",
     _t(t_types=["Normal"], u_moves=("U-turn", "Close Combat")), 1, 1),
    ("UTurn, slower, foe at 20%", "U-turn", _t(slower=True, t_hp=20, t_types=["Normal"], u_moves=("U-turn",)), 2, 0),
    ("UTurn, into a Steel type", "U-turn", _t(t_types=["Steel"]), -1, -1),
]


@check
def expert_routines():
    out = []
    for label, move, setup, want_pass, want_fail in EXPERT_ROWS:
        if isinstance(want_pass, Dice):
            # A row pinned by a dice sequence: one reading, want_fail its score.
            got = ex(move, setup, want_pass)
            out.append((f"Expert_{label}", got == want_fail, f"{got} (want {want_fail})"))
            continue
        got = (ex(move, setup, PASS), ex(move, setup, FAIL))
        out.append((f"Expert_{label}", got == (want_pass, want_fail),
                    f"pass {got[0]}, fail {got[1]} (want {want_pass}, {want_fail})"))
    return out


@check
def expert_dispatch():
    """Every label Expert_Main routes to has a routine, and none is left over."""
    routes = ai.expert_routes()
    missing = sorted({lab for lab in routes.values() if lab not in ai.EXPERT_ROUTINES})
    unused = sorted(set(ai.EXPERT_ROUTINES) - set(routes.values()))
    return [("Expert_Main's table: every label has a routine", not missing and not unused and len(routes) >= 237,
             f"{len(routes)} effects, missing {missing}, unused {unused}")]


@check
def no_calc_list():
    """The effects the AI gives no damage figure are the game's own list
    (trainer_ai.c, sNoDamageCalcMoveEffects), which the move reworks changed
    by taking half recoil off it (2026-10-06)."""
    import os
    import re
    path = os.path.join(fs.data.ROOT, "src", "battle", "trainer_ai", "trainer_ai.c")
    with open(path, encoding="utf-8") as fh:
        body = re.search(r"sNoDamageCalcMoveEffects\[\] = \{(.*?)\};", fh.read(), re.S).group(1)
    game = set(re.findall(r"BATTLE_EFFECT_(\w+)", body))
    return [("sNoDamageCalcMoveEffects matches the AI's list", game == ai.NO_CALC,
             f"{len(game)} in the game; only in the game {sorted(game - ai.NO_CALC)}, "
             f"only here {sorted(ai.NO_CALC - game)}")]


# ---- the smaller flags, switching, the post-knockout pick ----------------------------------------

def fl(bit, move, setup=None, dice=PASS):
    """One flag's change to Snorlax's move against Machamp."""
    b = battle(EX_BOSS, EX_PLAYER)
    u, t = b.b.cur(), b.p.cur()
    moves(u, move, "Body Slam")
    speeds(b, 100, 50)
    if setup:
        setup(b, u, t)
    b.rng = dice if isinstance(dice, Dice) else Dice(dice)
    mvo = fs.move(move)
    return ai.flag_score(bit, b, u, t, mvo, ai.figure(b, u, t, mvo), None)


FLAG_ROWS = [
    # (label, bit, move, setup, every chance passing, every chance failing)
    ("SetupFirstTurn, Charge is not in the table", ai.SETUP_FIRST, "Charge", None, 0, 0),
    ("SetupFirstTurn, Magnet Rise on turn 0", ai.SETUP_FIRST, "Magnet Rise", None, 2, 0),
    ("SetupFirstTurn, Swords Dance on turn 1", ai.SETUP_FIRST, "Swords Dance", _t(b_turn=1), 0, 0),
    ("Risky, Magnitude is not in the table", ai.RISKY, "Magnitude", None, 0, 0),
    ("Risky, Gyro Ball", ai.RISKY, "Gyro Ball", None, 2, 0),
    ("Risky, Explosion", ai.RISKY, "Explosion", None, 2, 0),
    ("Harassment, Teeter Dance", ai.HARASS, "Teeter Dance", None, 2, 0),
    ("Harassment, Spite", ai.HARASS, "Spite", None, 2, 0),
    ("Harassment, Toxic is not in the table", ai.HARASS, "Toxic", None, 0, 0),
    ("Weather, Sunny Day on turn 0", ai.WEATHER, "Sunny Day", None, 5, 5),
    ("Weather, Sunny Day with the sun up", ai.WEATHER, "Sunny Day", _t(weather="Sun"), 0, 0),
    ("Weather, Rain Dance in sun", ai.WEATHER, "Rain Dance", _t(weather="Sun"), 5, 5),
    ("Weather, Rain Dance on turn 1", ai.WEATHER, "Rain Dance", _t(b_turn=1), 0, 0),
    ("CheckHP, Explosion at 50%, foe at full HP", ai.CHECK_HP, "Explosion", _t(u_hp=50), -2, 0),
    ("CheckHP, Explosion at full HP, foe at 20%", ai.CHECK_HP, "Explosion", _t(t_hp=20), -4, 0),
    ("CheckHP, Explosion at 30%", ai.CHECK_HP, "Explosion", _t(u_hp=30), 0, 0),
    ("CheckHP, Explosion at 31%", ai.CHECK_HP, "Explosion", _t(u_hp=31), -2, 0),
    ("CheckHP, Hypnosis, foe at 50%", ai.CHECK_HP, "Hypnosis", _t(t_hp=50), 0, 0),
    ("CheckHP, Agility, foe at 50%", ai.CHECK_HP, "Agility", _t(t_hp=50), -2, 0),
    ("CheckHP, Reflect at 50%", ai.CHECK_HP, "Reflect", _t(u_hp=50), 0, 0),
    ("CheckHP, Water Spout at 20%", ai.CHECK_HP, "Water Spout", _t(u_hp=20), -2, 0),
    ("BatonPass flag, Swords Dance on turn 0, knowing Baton Pass", ai.BATON, "Swords Dance",
     _t(u_moves=("Swords Dance", "Baton Pass")), 5, 5),
    ("BatonPass flag, Swords Dance on turn 2 at 50%", ai.BATON, "Swords Dance",
     _t(u_moves=("Swords Dance", "Baton Pass"), b_turn=2, u_hp=50), -10, -10),
    ("BatonPass flag, Protect after its own Protect", ai.BATON, "Protect",
     _t(u_moves=("Protect", "Baton Pass"), b_turn=2, u_last="Protect"), -2, -2),
    ("BatonPass flag, Protect after an attack", ai.BATON, "Protect",
     _t(u_moves=("Protect", "Baton Pass"), b_turn=2, u_last="X-Scissor"), 2, 2),
    ("BatonPass flag, Baton Pass at Attack +2", ai.BATON, "Baton Pass", _t(u_atk=2, b_turn=2), 2, 2),
    ("BatonPass flag, Baton Pass on turn 0", ai.BATON, "Baton Pass", None, -2, -2),
    ("BatonPass flag, Heal Order without Baton Pass, turn 2 at 50%", ai.BATON, "Heal Order",
     _t(b_turn=2, u_hp=50), -7, 0),
    ("BatonPass flag, an attack with a comparison", ai.BATON, "Body Slam", None, 0, 0),
    ("BatonPass flag, no bench", ai.BATON, "Swords Dance", lambda b, u, t: _last_pokemon(b), 0, 0),
    # The other flags' routing (Ian, 2026-10-07; other-flags-new-moves.md): each
    # new move as its nearest Platinum effect, and the doc's judgment calls.
    ("SetupFirstTurn, Hone Claws on turn 0, as Meditate", ai.SETUP_FIRST, "Hone Claws", None, 2, 0),
    ("SetupFirstTurn, Aurora Veil on turn 0, as Reflect", ai.SETUP_FIRST, "Aurora Veil", None, 2, 0),
    ("SetupFirstTurn, Venom Drench is left out (it fails on turn 0)", ai.SETUP_FIRST, "Venom Drench", None, 0, 0),
    ("SetupFirstTurn, Quiver Dance is left out, as Dragon Dance", ai.SETUP_FIRST, "Quiver Dance", None, 0, 0),
    ("Risky, Final Gambit, as Explosion", ai.RISKY, "Final Gambit", None, 2, 0),
    ("Risky, Flower Trick is left out (no gamble)", ai.RISKY, "Flower Trick", None, 0, 0),
    ("Harassment, Sticky Web, as Spikes", ai.HARASS, "Sticky Web", None, 2, 0),
    ("Harassment, Magic Room, as Embargo", ai.HARASS, "Magic Room", None, 2, 0),
    ("CheckHP, Hone Claws at 50%, as Meditate", ai.CHECK_HP, "Hone Claws", _t(u_hp=50), -2, 0),
    ("CheckHP, Strength Sap at full HP, as Recover", ai.CHECK_HP, "Strength Sap", None, -2, 0),
    ("CheckHP, Final Gambit, foe at 20% (the target-low table only)", ai.CHECK_HP, "Final Gambit",
     _t(t_hp=20), -2, 0),
    ("CheckHP, Final Gambit at 50% is left out", ai.CHECK_HP, "Final Gambit", _t(u_hp=50), 0, 0),
    ("BatonPass flag, Quiver Dance on turn 0, knowing Baton Pass, as Dragon Dance", ai.BATON, "Quiver Dance",
     _t(u_moves=("Quiver Dance", "Baton Pass")), 5, 5),
]


@check
def flag_routines():
    out = []
    for label, bit, move, setup, wp, wf in FLAG_ROWS:
        got = (fl(bit, move, setup, PASS), fl(bit, move, setup, FAIL))
        out.append((label, got == (wp, wf), f"pass {got[0]}, fail {got[1]} (want {wp}, {wf})"))
    return out


SW_BOSS = [("Pikachu", 40, "Static", ["Thunderbolt", "Thunder Shock"]),
           ("Gyarados", 40, "Intimidate", ["Waterfall", "Ice Fang"]),
           ("Gengar", 40, "Levitate", ["Shadow Ball", "Sludge Bomb"]),
           ("Bronzong", 40, "Levitate", ["Shadow Ball", "Gyro Ball"])]
SW_PLAYER = [("Dugtrio", 40, "Arena Trap", ["Earthquake", "Night Slash"]),
             ("Gliscor", 40, "Hyper Cutter", ["Earthquake", "X-Scissor"]),
             ("Skarmory", 40, "Keen Eye", ["Drill Peck", "Steel Wing"]),
             ("Alakazam", 40, "Inner Focus", ["Psychic", "Earthquake"])]


def sw(setup, dice=PASS):
    """The switch decision for the trainer's lead against the player's lead,
    after setup(b, u, t)."""
    b = battle(SW_BOSS, SW_PLAYER)
    u, t = b.b.cur(), b.p.cur()
    setup(b, u, t)
    b.rng = dice if isinstance(dice, Dice) else Dice(dice)
    return ai.should_switch(b, b.b, b.b.cur(), b.p.cur())


def _to(b, side, species):
    side.active = next(i for i, m in enumerate(side.mons) if m.species == species)


@check
def switching():
    out = []

    def lead(boss=None, player=None):
        def setup(b, u, t):
            if boss:
                _to(b, b.b, boss)
            if player:
                _to(b, b.p, player)
        return setup
    # Arena Trap holds the AI's Pikachu, whose Electric attacks cannot touch Dugtrio.
    got = (sw(lead(), PASS), sw(lead(), FAIL))
    out.append(("ShouldSwitch: a foe's Arena Trap keeps the AI in", got == (None, None), f"{got}"))

    def gliscor(b, u, t):
        _to(b, b.p, "Gliscor")
    got = (sw(gliscor, PASS), sw(gliscor, FAIL))
    out.append(("ShouldSwitch: two attacks with no effect, a bench Ice Fang comes in",
                got == (1, None), f"{got} (want 1 passing, None failing)"))

    def ghost_trapped(b, u, t):
        _to(b, b.b, "Gengar")
        b.b.cur().trapped_by = t.key
        b.b.cur().perish = 1
    got = (sw(ghost_trapped, PASS), sw(ghost_trapped, FAIL))
    out.append(("ShouldSwitch: a Ghost is never held, so Perish Song moves it",
                got[0] is not None and got[1] is not None, f"{got}"))

    def boosted(b, u, t):
        _to(b, b.p, "Alakazam")
        u.stages.update(atk=3, acc=1)
        u.last_hit_by = fs.move("Earthquake")
    got = sw(boosted, PASS)
    out.append(("ShouldSwitch: four stages up, accuracy counted, keeps it in", got is None, f"{got}"))

    # Choice lock: the switch rules still run.
    b = battle(SW_BOSS, SW_PLAYER)
    _to(b, b.p, "Alakazam")
    u = b.b.cur()
    u.choice, u.perish = "Thunderbolt", 1
    b.rng = Dice(FAIL)
    got = ai.choose(b, u, b.p.cur())
    out.append(("PickCommand: a Choice-locked Pokemon still switches under Perish Song",
                got[0] == "switch", f"{got}"))

    # The flags: Ground on Skarmory reads super effective and immune; Levitate.
    b = battle(SW_BOSS, SW_PLAYER)
    flags = (ai.type_flags(b, "Ground", ["Steel", "Flying"]), ai.type_flags(b, "Electric", ["Ground", "Flying"]),
             ai.type_flags(b, "Ground", ["Flying", "Bug"]), ai.type_flags(b, "Normal", ["Rock", "Ghost"]),
             ai.type_flags(b, "Fire", ["Water", "Grass"]))
    want = ((True, True, False), (True, True, False), (True, False, True), (True, False, False),
            (False, False, False))
    out.append(("Effectiveness flags meet types in the chart's order (bug 10, kept)", flags == want, f"{flags}"))
    dug = b.p.cur()
    bronzong = next(m for m in b.b.mons if m.species == "Bronzong")
    eq = fs.move("Earthquake")
    out.append(("Levitate: Earthquake on Bronzong is neither super effective (active) nor anything but immune (bench)",
                not ai.active_flags(b, dug, eq, bronzong)[1] and ai.bench_flags(b, dug.ability, "Ground", bronzong)[0],
                f"active {ai.active_flags(b, dug, eq, bronzong)}, bench {ai.bench_flags(b, dug.ability, 'Ground', bronzong)}"))
    return out


@check
def post_ko_pick():
    out = []
    # Stage 1 never takes a candidate whose type score is 0. Against the
    # player's Gengar, Kangaskhan (Normal, 0) has a super-effective Pursuit,
    # which stage 1 used to take; Steelix (above 0) has no super-effective
    # move, so the engine goes to stage 2, where Iron Tail outscores Pursuit.
    b = battle([("Gengar", 40, "Levitate", ["Shadow Ball"]), ("Kangaskhan", 40, "Early Bird", ["Pursuit"]),
                ("Steelix", 40, "Sturdy", ["Iron Tail"])],
               [("Gengar", 40, "Levitate", ["Shadow Ball"])])
    b.rng = Dice(PASS)
    got = b.b.mons[ai.replacement(b, b.b, b.p.cur())].species
    out.append(("PostKOSwitchIn stage 1: a type score of 0 is never taken", got == "Steelix", f"picked {got}"))
    # A status move costs 2 (3 with the same-type bonus), 0 into an immunity.
    b = battle([("Gengar", 40, "Levitate", ["Shadow Ball"]), ("Snorlax", 40, "Thick Fat", ["Growl", "Body Slam"])],
               [("Machamp", 40, "Guts", ["Cross Chop"])])
    gengar, lax, champ = b.b.mons[0], b.b.mons[1], b.p.cur()
    growl = fs.move("Growl")
    out.append(("PostKOSwitchIn stage 2: a status move scores 2, 0 into an immunity",
                ai._ko_score(b, gengar, lax, champ, growl) == 2 and ai._ko_score(b, lax, lax, champ, growl) == 3,
                f"{ai._ko_score(b, gengar, lax, champ, growl)}, as Snorlax {ai._ko_score(b, lax, lax, champ, growl)}"))
    return out


@check
def hit_record_and_turns():
    out = []
    b = battle(EX_BOSS, EX_PLAYER)
    lax, champ = b.b.cur(), b.p.cur()
    b.rng = Dice(0.5)
    fs.use_move(b, champ, fs.move("Thunder Wave"), lax, True)
    tw = lax.last_hit_by
    fs.use_move(b, champ, fs.move("Swords Dance"), lax, True)
    sd = lax.last_hit_by
    champ.status = "par"
    b.rng = Dice(0.0)             # fully paralysed
    fs.use_move(b, champ, fs.move("Cross Chop"), lax, True)
    cleared = lax.last_hit_by
    out.append(("Hit record: a status move records, a self-move leaves it, a turn unable to act clears it",
                tw is not None and tw.name == "Thunder Wave" and sd is tw and cleared is None,
                f"{tw}, {sd}, {cleared}"))
    # A Pokemon switched in during a turn reads its first turn at the next.
    b = battle(EX_BOSS, EX_PLAYER)
    b.mid_turn = True
    fs.switch_in(b, b.p, 1)
    fs.end_of_turn(b)
    first = b.p.cur().turns_in
    fs.end_of_turn(b)
    lead = b.b.cur().turns_in
    out.append(("Turn count: a mid-turn switch-in reads 0 the next turn; a lead 2 at its third",
                first == 0 and lead == 2, f"{first}, {lead}"))
    # The AI knows a Quick Claw fired: its Pokemon reads itself slower.
    b = battle(EX_BOSS, EX_PLAYER)
    lax, champ = b.b.cur(), b.p.cur()
    speeds(b, 100, 50)
    champ.item = "Quick Claw"
    before = ai.slower(b, lax, champ)
    b.quick = {champ.key: True}
    after = ai.slower(b, lax, champ)
    out.append(("Speed: the player's Quick Claw that fires this turn makes the AI read itself slower",
                not before and after, f"{before}, {after}"))
    return out


# ---- Basic, Evaluate Attack, the figure and what the AI knows -------------------------------------

A_BOSS = [("Kangaskhan", 40, "Scrappy", ["Body Slam", "Hidden Power", "Low Kick", "Magnitude"]),
          ("Starmie", 40, "Natural Cure", ["Surf", "Thunder Wave"]),
          ("Arcanine", 40, "Intimidate", ["Flamethrower", "Roar"]),
          ("Gengar", 40, "Levitate", ["Shadow Ball", "Hypnosis"]),
          ("Absol", 40, "Super Luck", ["Sucker Punch", "Night Slash", "Quick Attack", "Feint"]),
          ("Venusaur", 40, "Overgrow", ["Sleep Powder", "Energy Ball"]),
          ("Golem", 40, "Rock Head", ["Explosion", "Rock Slide"]),
          ("Breloom", 40, "Effect Spore", ["Bullet Seed", "Seed Bomb"]),
          ("Raichu", 40, "Static", ["Thunderbolt", "Thunder Wave"], "Expert Belt"),
          ("Lucario", 40, "Inner Focus", ["Aura Sphere", "Vacuum Wave"], "Life Orb"),
          ("Rampardos", 40, "Mold Breaker", ["Rock Slide", "Head Smash"])]
A_PLAYER = [("Quagsire", 40, "Unaware", ["Surf"]), ("Houndoom", 40, "Flash Fire", ["Crunch"]),
            ("Hoothoot", 40, "Tinted Lens", ["Peck"]), ("Gengar", 40, "Levitate", ["Shadow Ball"]),
            ("Exploud", 40, "Scrappy", ["Hyper Voice"]), ("Jangmo-o", 40, "Soundproof", ["Dragon Tail"]),
            ("Bronzong", 40, "Heatproof", ["Gyro Ball"]), ("Zigzagoon", 40, "Gluttony", ["Tackle"]),
            ("Psyduck", 40, "Swift Swim", ["Water Gun"]), ("Tsareena", 40, "Leaf Guard", ["Trop Kick"]),
            ("Goodra", 40, "Hydration", ["Dragon Pulse"]), ("Slowpoke", 40, "Own Tempo", ["Water Gun"]),
            ("Starly", 10, "Keen Eye", ["Tackle"]), ("Machop", 40, "Guts", ["Karate Chop"]),
            ("Gallade", 40, "Steadfast", ["Psycho Cut"]), ("Fletchling", 40, "Big Pecks", ["Peck"]),
            ("Beldum", 40, "Clear Body", ["Take Down"]), ("Torkoal", 40, "Shell Armor", ["Ember"]),
            ("Octillery", 40, "Sniper", ["Octazooka"]), ("Clefable", 40, "Magic Guard", ["Moonblast"]),
            ("Snorlax", 40, "Thick Fat", ["Body Slam"]), ("Shedinja", 40, "Wonder Guard", ["Shadow Sneak"]),
            ("Lickitung", 40, "Oblivious", ["Lick"]), ("Glameow", 40, "Limber", ["Scratch"]),
            ("Wailord", 40, "Pressure", ["Water Gun"]), ("Muk", 40, "Stench", ["Sludge"]),
            ("Dewgong", 40, "Thick Fat", ["Aurora Beam"]), ("Hoppip", 40, "Chlorophyll", ["Tackle"]),
            ("Sealeo", 40, "Ice Body", ["Water Gun"]), ("Gyarados", 70, "Intimidate", ["Waterfall"]),
            ("Geodude", 10, "Sturdy", ["Tackle"]), ("Lanturn", 40, "Volt Absorb", ["Spark"]),
            ("Ninjask", 40, "Speed Boost", ["Scratch"]), ("Yanma", 40, "Compound Eyes", ["Tackle"]),
            ("Bidoof", 40, "Simple", ["Tackle"])]


def ab(boss_sp, player_sp, move, setup=None, dice=PASS, fn="basic"):
    """Basic's (or Evaluate Attack's) score for the trainer's boss_sp using
    move against the player's player_sp, after setup(b, u, t); the trainer's
    Pokemon moves first unless setup says otherwise."""
    b = battle(A_BOSS, A_PLAYER)
    _to(b, b.b, boss_sp)
    _to(b, b.p, player_sp)
    u, t = b.b.cur(), b.p.cur()
    if all(m.name != move for m in u.moves):
        moves(u, move, *[m.name for m in u.moves])
    speeds(b, 100, 50)
    if setup:
        setup(b, u, t)
    b.rng = dice if isinstance(dice, Dice) else Dice(dice)
    mvo = fs.move(move)
    f = ai.figure(b, u, t, mvo)
    if fn == "basic":
        return ai.basic(b, u, t, mvo, f)
    figs = [ai.figure(b, u, t, m) for m in u.moves]
    best = max((x for x in figs if x is not None), default=None)
    return ai.evaluate_attack(b, u, t, mvo, f, best)


def _alone(b, u, t):
    """Each side down to its active Pokemon."""
    for side in (b.b, b.p):
        for i, m in enumerate(side.mons):
            if i != side.active:
                m.hp = 0


# (label, trainer's Pokemon, player's Pokemon, move, setup, every chance passing, every one failing).
# The AI guesses a player's ability between its species' two slots: the
# first on a passing coin, the second on a failing one.
BASIC_ROWS = [
    ("CheckForImmunity: Scrappy's Body Slam into a Ghost", "Kangaskhan", "Gengar", "Body Slam", None, 0, 0),
    ("CheckForImmunity: Hidden Power at odd IVs is Dark, into a Ghost", "Kangaskhan", "Gengar", "Hidden Power",
     None, 0, 0),
    ("CheckForImmunity: Magnitude into a real Levitate", "Kangaskhan", "Gengar", "Magnitude", None, -10, -10),
    ("absorbing checks: Surf into Quagsire (Water Absorb or Unaware)", "Starmie", "Quagsire", "Surf", None, -12, 0),
    ("absorbing checks: Flamethrower into Houndoom (Early Bird or Flash Fire)", "Arcanine", "Houndoom",
     "Flamethrower", None, 0, -12),
    ("CheckMagnitude: into Bronzong (Levitate or Heatproof, real Heatproof)", "Kangaskhan", "Bronzong",
     "Magnitude", None, -12, 0),
    ("CheckSoundproof: Screech into Exploud (Scrappy or Soundproof)", "Kangaskhan", "Exploud", "Screech", None, 0, -10),
    ("CheckBulletproof: Shadow Ball into Jangmo-o (Bulletproof or Soundproof)", "Gengar", "Jangmo-o",
     "Shadow Ball", None, -10, 0),
    ("CheckQueenlyMajesty: Sucker Punch into Tsareena (Leaf Guard or Queenly Majesty)", "Absol", "Tsareena",
     "Sucker Punch", None, 0, -10),
    ("CheckPowderImmunity and SapSipper: Sleep Powder into Goodra (Sap Sipper or Hydration)", "Venusaur", "Goodra",
     "Sleep Powder", None, -10, 0),
    ("CheckRest: Leaf Guard in sun at half HP", "Gengar", "Zigzagoon", "Rest",
     _t(u_ability="Leaf Guard", weather="Sun", u_hp=50), -10, -10),
    ("CheckUpperHand: no priority move shown", "Kangaskhan", "Zigzagoon", "Upper Hand", None, -10, -10),
    ("CheckUpperHand: Quick Attack shown", "Kangaskhan", "Zigzagoon", "Upper Hand",
     _t(t_shown=("Quick Attack",)), 0, 0),
    ("CheckUpperHand: a Prankster's Thunder Wave shown", "Kangaskhan", "Zigzagoon", "Upper Hand",
     _t(t_shown=("Thunder Wave",), t_ability="Prankster"), 0, 0),
    ("CheckUpperHand: Thunder Wave shown, no Prankster", "Kangaskhan", "Zigzagoon", "Upper Hand",
     _t(t_shown=("Thunder Wave",), t_ability="Run Away"), -10, -10),
    ("CheckTaunt: into Slowpoke (Oblivious or Own Tempo)", "Gengar", "Slowpoke", "Taunt", None, -10, 0),
    ("CheckTaunt: into a taunted Zigzagoon (Basic never checks it)", "Gengar", "Zigzagoon", "Taunt", _t(t_taunt=3), 0, 0),
    ("CheckCannotSleep: Hypnosis into Hoothoot (Insomnia or Tinted Lens)", "Gengar", "Hoothoot", "Hypnosis",
     None, -10, 0),
    ("CheckCannotSleep: Hypnosis once Tinted Lens is named", "Gengar", "Hoothoot", "Hypnosis",
     _t(t_revealed="Tinted Lens"), 0, 0),
    ("CheckCannotSleep: Hypnosis into a Substitute (Basic never looks)", "Gengar", "Zigzagoon", "Hypnosis",
     _t(t_sub=10), 0, 0),
    ("CheckCannotSleep: Yawn into a drowsy target", "Gengar", "Zigzagoon", "Yawn", _t(t_yawn=1), 0, 0),
    ("CheckCannotExplode: each side on its last Pokemon", "Golem", "Zigzagoon", "Explosion", _alone, -1, -1),
    ("CheckCannotExplode: into Psyduck (Damp or Swift Swim)", "Golem", "Psyduck", "Explosion", None, -10, 0),
    ("CheckDreamEater: an awake target", "Gengar", "Zigzagoon", "Dream Eater", None, -8, -8),
    ("CheckBellyDrum: at 50%", "Gengar", "Zigzagoon", "Belly Drum", _t(u_hp=50), -10, -10),
    ("CheckHighStatStage: Swords Dance at +6", "Gengar", "Zigzagoon", "Swords Dance", _t(u_atk=6), -10, -10),
    ("CheckHighStatStage: Agility under Trick Room", "Gengar", "Zigzagoon", "Agility", _t(trick_room=5), -10, -10),
    ("CheckHighStatStage: Charge has no stage check", "Gengar", "Zigzagoon", "Charge", _t(u_spd=6), 0, 0),
    ("CheckHighStatStage_Evasion: Double Team into Starly (Keen Eye)", "Gengar", "Starly", "Double Team",
     None, -10, -10),
    ("CheckHighStatStage_Evasion: Double Team into Machop (Guts or No Guard)", "Gengar", "Machop", "Double Team",
     None, 0, -10),
    ("CheckLowStatStage_Attack: Growl into Gallade (Hyper Cutter or Steadfast)", "Gengar", "Gallade", "Growl",
     None, -10, 0),
    ("CheckLowStatStage_Defense: Screech into Fletchling (Big Pecks)", "Gengar", "Fletchling", "Screech",
     None, -10, -10),
    ("CheckLowStatStage_Speed: Scary Face under Trick Room", "Gengar", "Zigzagoon", "Scary Face",
     _t(trick_room=5), -10, -10),
    ("CheckLowStatStage_Speed: Scary Face into Ninjask (Speed Boost, read with no coin)", "Gengar", "Ninjask",
     "Scary Face", None, -10, -10),
    ("CheckLowStatStage_Speed: Scary Face into Yanma (Speed Boost unknown until named)", "Gengar", "Yanma",
     "Scary Face", None, 0, 0),
    ("CheckLowStatStage_Accuracy: Sand Attack into Starly (Keen Eye)", "Gengar", "Starly", "Sand Attack",
     None, -10, -10),
    ("CheckClearBodyEffect: Leer into Beldum", "Gengar", "Beldum", "Leer", None, -10, -10),
    ("CheckClearBodyEffect: Leer into Torkoal (White Smoke or Shell Armor)", "Gengar", "Torkoal", "Leer", None, -10, 0),
    ("CheckStatStageImbalance: Psych Up with nothing raised", "Gengar", "Zigzagoon", "Psych Up", None, -10, -10),
    ("CheckCanForceSwitch: Roar into Octillery (Suction Cups or Sniper)", "Arcanine", "Octillery", "Roar",
     None, -10, 0),
    ("CheckCanRecoverHP: Recover at full HP", "Gengar", "Zigzagoon", "Recover", None, -8, -8),
    ("CheckCannotPoison: Toxic into Clefable (Magic Guard)", "Gengar", "Clefable", "Toxic", None, -10, -10),
    ("CheckCannotPoison: Toxic into Snorlax (Immunity or Thick Fat)", "Gengar", "Snorlax", "Toxic", None, -10, 0),
    ("CheckAlreadyUnderLightScreen", "Gengar", "Zigzagoon", "Light Screen",
     lambda b, u, t: b.b.screens.update({"Light Screen": 5}), -8, -8),
    ("CheckOHKOWouldFail: Sheer Cold into a higher level", "Gengar", "Zigzagoon", "Sheer Cold", _t(u_level=30),
     -10, -10),
    ("CheckNonStandardDamage: Hyper Beam into Shedinja", "Kangaskhan", "Shedinja", "Hyper Beam", None, -10, -10),
    ("CheckNonStandardDamage: Night Shade into Shedinja (super effective)", "Gengar", "Shedinja", "Night Shade",
     None, 0, 0),
    ("CheckCannotConfuse: Confuse Ray into Lickitung (Own Tempo or Oblivious)", "Gengar", "Lickitung",
     "Confuse Ray", None, -10, 0),
    ("CheckCannotConfuse: Swagger into Safeguard", "Gengar", "Zigzagoon", "Swagger",
     lambda b, u, t: setattr(b.p, "safeguard", 5), -10, -10),
    ("Safeguard: an Infiltrator's Toxic passes it", "Gengar", "Zigzagoon", "Toxic",
     lambda b, u, t: (setattr(b.p, "safeguard", 5), setattr(u, "ability", "Infiltrator")), 0, 0),
    ("CheckCannotParalyze: Stun Spore into Glameow (Limber)", "Venusaur", "Glameow", "Stun Spore", None, -10, -10),
    ("CheckCannotParalyze: Thunder Wave into a Substitute", "Starmie", "Zigzagoon", "Thunder Wave", _t(t_sub=10), 0, 0),
    ("CheckCannotLeechSeed: into Clefable (Magic Guard)", "Venusaur", "Clefable", "Leech Seed", None, -10, -10),
    ("CheckAttackerAsleep: Sleep Talk awake", "Gengar", "Zigzagoon", "Sleep Talk", None, -8, -8),
    ("CheckMeanLook: Block into a Ghost", "Kangaskhan", "Gengar", "Block", None, -10, -10),
    ("CheckCurse: a Ghost's Curse into a cursed target", "Gengar", "Zigzagoon", "Curse", _t(t_cursed=True), -10, -10),
    ("CheckPerishSong: only the user has a count", "Gengar", "Zigzagoon", "Perish Song", _t(u_perish=2), 0, 0),
    ("CheckCannotAttract: into Slowpoke (Oblivious or Own Tempo)", "Gengar", "Slowpoke", "Attract", None, -10, 0),
    ("CheckMemento: the last Pokemon", "Gengar", "Zigzagoon", "Memento", _alone, -10, -10),
    ("CheckRainDance: into a paralysed Dewgong (Thick Fat or Hydration)", "Starmie", "Dewgong", "Rain Dance",
     _t(t_status="par"), 0, -8),
    ("CheckSunnyDay: into Hoppip (Chlorophyll or Leaf Guard)", "Arcanine", "Hoppip", "Sunny Day", None, 0, -10),
    ("CheckCanSpitUpOrSwallow: Swallow into a Ghost", "Gengar", "Gengar", "Swallow", _t(u_stockpile=1), -10, -10),
    ("CheckHail: into Sealeo (Ice Body)", "Gengar", "Sealeo", "Hail", None, -8, -8),
    ("CheckCannotBurn: Will-O-Wisp into Wailord (Pressure or Water Veil)", "Gengar", "Wailord", "Will-O-Wisp",
     None, 0, -10),
    ("CheckHelpingHand: a single battle", "Gengar", "Zigzagoon", "Helping Hand", None, -10, -10),
    ("CheckCanRemoveItem: Knock Off into Muk with Leftovers (Stench or Sticky Hold)", "Absol", "Muk", "Knock Off",
     _t(t_item="Leftovers"), 0, -10),
    ("CheckCanRemoveItem: Knock Off into no item", "Absol", "Zigzagoon", "Knock Off", None, -10, -10),
    ("CheckTickle: Defense at -6", "Gengar", "Zigzagoon", "Tickle", _t(t_def=-6), -8, -8),
    ("CheckDragonDance: Speed +6 under Trick Room", "Gengar", "Zigzagoon", "Dragon Dance",
     _t(u_spe=6, trick_room=5), -10, -10),
    ("CheckShiftGear: Attack +6", "Gengar", "Zigzagoon", "Shift Gear", _t(u_atk=6), -10, -10),
    ("CheckHealingWish: a full and healthy bench", "Gengar", "Zigzagoon", "Healing Wish", None, -30, -30),
    ("CheckNaturalGift: no item", "Gengar", "Zigzagoon", "Natural Gift", None, -10, -10),
    ("CheckFling: no item", "Gengar", "Zigzagoon", "Fling", None, -10, -10),
    ("CheckFling: a Flame Orb into a burned target", "Gengar", "Zigzagoon", "Fling",
     _t(u_item="Flame Orb", t_status="brn"), 3, 3),
    ("CheckCopycat: turn 0, faster", "Gengar", "Zigzagoon", "Copycat", None, -10, -10),
    ("CheckCopycat: turn 1", "Gengar", "Zigzagoon", "Copycat", _t(b_turn=1), 0, 0),
    ("CheckAquaRing: already up", "Gengar", "Zigzagoon", "Aqua Ring", _t(u_aqua_ring=True), -10, -10),
    ("CheckCanRefreshStatus: no status", "Gengar", "Zigzagoon", "Refresh", None, -10, -10),
    ("CheckFirstTurnInBattle: Fake Out on the second turn out", "Kangaskhan", "Zigzagoon", "Fake Out",
     _t(u_turns_in=1), -10, -10),
]


EVAL_ROWS = [
    ("EvalAttack_MaybeDeprioritize: Sucker Punch (no comparison)", "Absol", "Zigzagoon", "Sucker Punch", None, -2, 0),
    ("EvalAttack_MaybeDeprioritize: Explosion (no comparison)", "Golem", "Zigzagoon", "Explosion", None, -2, 0),
    ("EvalAttack_MaybeDeprioritize: Final Gambit, as Explosion (2026-10-07)", "Kangaskhan", "Zigzagoon",
     "Final Gambit", None, -2, 0),
    ("EvalAttack_ApplyKillBonuses: Quick Attack (PRIORITY_1) knocks out", "Absol", "Starly", "Quick Attack",
     None, 6, 6),
    ("EvalAttack_ApplyKillBonuses: Feint knocks out (+4: the effect, not the priority)", "Absol", "Starly", "Feint",
     None, 4, 4),
    ("EvalAttack_CheckQuadEffective: Thunder Wave into Gyarados", "Starmie", "Gyarados", "Thunder Wave", None, 2, 0),
    ("EvalAttack_CheckQuadEffective: an Expert Belt reads no bucket", "Raichu", "Gyarados", "Thunderbolt", None, 0, 0),
    ("AI_SturdySurvives: a full-HP Sturdy target survives", "Golem", "Geodude", "Rock Slide", None, 0, 0),
    ("AI_SturdySurvives: Mold Breaker gets past Sturdy", "Rampardos", "Geodude", "Rock Slide", None, 4, 4),
]


@check
def basic_routines():
    out = []
    for label, bsp, psp, move, setup, wp, wf in BASIC_ROWS:
        got = (ab(bsp, psp, move, setup, PASS), ab(bsp, psp, move, setup, FAIL))
        out.append((f"Basic_{label}", got == (wp, wf), f"pass {got[0]}, fail {got[1]} (want {wp}, {wf})"))
    for label, bsp, psp, move, setup, wp, wf in EVAL_ROWS:
        got = (ab(bsp, psp, move, setup, PASS, "eval"), ab(bsp, psp, move, setup, FAIL, "eval"))
        out.append((label, got == (wp, wf), f"pass {got[0]}, fail {got[1]} (want {wp}, {wf})"))
    return out


@check
def damage_figure_and_engine():
    out = []
    b = battle(A_BOSS, A_PLAYER)
    _to(b, b.p, "Bidoof")
    t = b.p.cur()
    _to(b, b.b, "Breloom")
    bre = b.b.cur()
    # A move of several hits on its expected hits (TrainerAI_ExpectedHitsDamage,
    # 2026-10-07): the row adds three hits; the AI takes one and counts 3.1.
    one, row = ai.figure(b, bre, t, fs.move("Bullet Seed")), b.damage(bre, t, fs.move("Bullet Seed"), ai_view=True)
    out.append(("figure: a two to five hit move on 3.1 hits (the row adds three)",
                one == (row // 3) * 31 // 10, f"{one} of {row}"))
    plain = ai.expected_hits(bre, fs.move("Bullet Seed"), 100)
    bre.ability = "Skill Link"
    link = ai.expected_hits(bre, fs.move("Bullet Seed"), 100)
    cutter = ai.expected_hits(bre, fs.move("Fury Cutter"), 100)
    kick = ai.expected_hits(bre, fs.move("Triple Kick"), 100)
    out.append(("expected hits: 3.1, Skill Link 5, Fury Cutter 30+40+50 over 30, Triple Kick's row as it is; "
                "Bone Rush at 100%", (plain, link, cutter, kick, fs.move("Bone Rush").acc) == (310, 500, 400, 100, 100),
                f"{plain}, {link}, {cutter}, {kick}; Bone Rush {fs.move('Bone Rush').acc}%"))
    _to(b, b.b, "Lucario")
    luc = b.b.cur()
    lo, raw = ai.figure(b, luc, t, fs.move("Aura Sphere")), b.damage(luc, t, fs.move("Aura Sphere"), ai_view=True)
    out.append(("figure: Life Orb is not in the AI's estimate", lo == raw * 4096 // 5324, f"{lo} of {raw}"))
    _to(b, b.b, "Kangaskhan")
    kan = b.b.cur()
    lk = ai.figure(b, kan, t, fs.move("Low Kick"))
    out.append(("figure: Low Kick (listed at power 1) gets a figure", lk is not None and lk > 0, f"{lk}"))
    out.append(("move type: Hidden Power at odd IVs is Dark", ai.move_type(b, kan, fs.move("Hidden Power")) == "Dark",
                ai.move_type(b, kan, fs.move("Hidden Power"))))
    _to(b, b.b, "Raichu")
    _to(b, b.p, "Lanturn")
    rai, lan = b.b.cur(), b.p.cur()
    tb = ai.figure(b, rai, lan, fs.move("Thunderbolt"))
    out.append(("figure: the estimate ignores Volt Absorb (the ability-blank twin row)",
                tb is not None and tb > 0 and b.damage(rai, lan, fs.move("Thunderbolt"), ai_view=True) == 0, f"{tb}"))
    # The score engine: a Choice lock rules out the other moves only while
    # the item is held; a slot with no PP scores 0.
    _to(b, b.b, "Starmie")
    star = b.b.cur()
    star.choice, star.item = "Surf", None
    free = ai.invalid(b, star, fs.move("Thunder Wave"))
    star.item = "Choice Specs"
    held = ai.invalid(b, star, fs.move("Thunder Wave"))
    star.choice = star.item = None
    star.pp["Surf"] = 0
    b.rng = Dice(PASS)
    sc = ai.score_moves(b, star, b.p.cur(), 1)
    out.append(("TrainerAI_Init: a Choice lock holds only with the item; no PP scores 0",
                not free and held and sc[0] == 0, f"{free}, {held}, {sc}"))
    # What the AI learns: Intimidate names itself as it comes in; a hit an
    # ability takes names it; Sturdy holding names it.
    b = battle(A_BOSS, A_PLAYER)
    _to(b, b.b, "Arcanine")
    b.mid_turn = False
    fs.switch_in(b, b.p, next(i for i, m in enumerate(b.p.mons) if m.species == "Gyarados"))
    gy = b.p.cur()
    named = gy.revealed
    fs.switch_in(b, b.p, next(i for i, m in enumerate(b.p.mons) if m.species == "Houndoom"))
    hd = b.p.cur()
    b.rng = random.Random(1)
    fs.attack(b, b.b.cur(), fs.move("Flamethrower"), hd, True)
    out.append(("Revealed abilities: Intimidate on entry, forgotten on leaving; Flash Fire on taking a Fire move",
                named == "Intimidate" and gy.revealed is None and hd.revealed == "Flash Fire",
                f"{named}, {gy.revealed}, {hd.revealed}"))
    return out


@check
def cache_key():
    """perfectline caches the AI's picks by what it reads: states the AI
    tells apart must not share a key."""
    b = battle(EX_BOSS, EX_PLAYER)
    u, t = b.b.cur(), b.p.cur()
    keys = []
    for turns, pct in ((2, 70), (4, 70), (2, 69)):
        t.turns_in = turns
        hp(u, pct)
        keys.append(pl.ai_key(b))
    t.shown = [fs.move("Recover")]
    keys.append(pl.ai_key(b))
    return [("perfectline's AI cache key tells turns in, HP thresholds and seen moves apart",
             len(set(keys)) == 4, f"{len(set(keys))} distinct of 4")]


def doubles(dice=PASS):
    """The Expert fixture as a double battle: Snorlax beside Gengar against
    Machamp beside Blissey."""
    b = battle(EX_BOSS, EX_PLAYER)
    b.doubles = True
    b.b.active2, b.p.active2 = 1, 1
    b.rng = Dice(dice)
    return b, b.b.mons[0], b.b.mons[1], b.p.mons[0], b.p.mons[1]


def _as(mon, types=None, ability=None, hp_pct=None):
    if types is not None:
        mon.types = list(types)
    if ability is not None:
        mon.ability = ability
    if hp_pct is not None:
        hp(mon, hp_pct)
    return mon


@check
def tag_strategy_routines():
    out = []
    # A single battle: Follow Me with no partner for good scores -10.
    b = battle(EX_BOSS, EX_PLAYER)
    b.rng = Dice(PASS)
    lax = b.b.cur()
    got = ai.tag_strategy(b, lax, b.p.cur(), fs.move("Follow Me"), None)
    out.append(("TagStrategy_FollowMe: a single battle", got == -10, f"{got}"))
    rows = []
    b, lax, gen, champ, bliss = doubles()
    rows.append(("TagStrategy_Earthquake: beside a Rock/Bug partner", ai._tag_quake(lax, _as(gen, ["Rock", "Bug"], "Swift Swim")), -10))
    rows.append(("TagStrategy_Earthquake: beside a Levitate partner", ai._tag_quake(lax, _as(gen, ["Ghost", "Poison"], "Levitate")), 2))
    rows.append(("TagStrategy_Explosion: beside a Ghost partner", ai._tag_boom(lax, _as(gen, ["Ghost"], "Levitate")), 0))
    rows.append(("TagStrategy_Explosion: beside a Grass/Dark partner", ai._tag_boom(lax, _as(gen, ["Grass", "Dark"], "Chlorophyll")), -10))
    rows.append(("TagStrategy_CheckElectricMove: Discharge beside a Water/Ground partner",
                 ai._tag_electric(b, lax, champ, fs.move("Discharge"), _as(gen, ["Water", "Ground"], "Damp")), 3))
    rows.append(("TagStrategy_CheckWaterMove: Surf beside a Water/Ground partner",
                 ai._tag_water(b, lax, champ, fs.move("Surf"), _as(gen, ["Water", "Ground"], "Damp")), -10))
    rows.append(("TagStrategy_CheckFireMove: Lava Plume beside a Bug/Rock partner",
                 ai._tag_fire(lax, fs.move("Lava Plume"), _as(gen, ["Bug", "Rock"], "Sturdy")), -10))
    lax.flash_fire = True
    rows.append(("TagStrategy_CheckFireMove: a lit Flash Fire's Flamethrower",
                 ai._tag_fire(lax, fs.move("Flamethrower"), gen), 1))
    lax.flash_fire = False
    rows.append(("TagStrategy_Sandstorm: beside a Rock partner",
                 ai._tag_weather(b, _as(lax, ["Normal"], "Thick Fat"), "Sandstorm") if _as(gen, ["Bug", "Rock"]) else 0, 2))
    # The partner pass: Flamethrower at a Flash Fire partner, unlit then lit.
    _as(gen, ["Fire"], "Flash Fire")
    unlit = ai.tag_partner(b, lax, gen, fs.move("Flamethrower"))
    gen.flash_fire = True
    lit = ai.tag_partner(b, lax, gen, fs.move("Flamethrower"))
    gen.flash_fire = False
    rows.append(("TagStrategy_Partner: Flamethrower at an unlit Flash Fire partner", unlit, 3))
    rows.append(("TagStrategy_Partner: the same once it is lit", lit, -30))
    for label, got, want in rows:
        out.append((label, got == want, f"{got} (want {want})"))
    # Helping Hand on a partner above half HP: +2 at 75%, else -1.
    got = []
    for dice in (PASS, FAIL):
        b, lax, gen, champ, bliss = doubles(dice)
        hp(gen, 60)
        got.append(ai.tag_partner(b, lax, gen, fs.move("Helping Hand")))
    out.append(("TagStrategy_Partner: Helping Hand on a partner at 60%", got == [2, -1], f"{got}"))
    # The damage step: Gengar's Thunderbolt into a target typed Grass (half),
    # not a knockout, not the strongest of the pair, the other foe standing.
    got = []
    for dice in (PASS, FAIL):
        b, lax, gen, champ, bliss = doubles(dice)
        champ.types = ["Grass"]
        got.append(ai.tag_strategy(b, gen, champ, fs.move("Thunderbolt"), lax))
    out.append(("TagStrategy_Main: a resisted move loses 1 at 75% while the other foe stands",
                got == [-1, 0], f"{got}"))
    return out


def main():
    results = checks()
    width = max(len(label) for label, _, _ in results)
    failed = 0
    for label, ok, note in results:
        failed += not ok
        print(f"  {'ok  ' if ok else 'FAIL'}  {label:{width}}  {note}")
    print(f"\n{len(results) - failed}/{len(results)} passed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())

"""The perfect-line search (out/design.md).

A fight is an AND-OR game: the player must have some action (OR) that
survives every adversary choice (AND), where the adversary plays the
trainer, from what its AI could pick, and the dice, within the luck budget.
The mechanics, the damage rows and the trainer AI are fightsim's and
fightai's, imported from the repo and used as they are; only the turn's
chance points are replaced here with adversary choices, so that a turn is a
deterministic function of (player action, trainer action, luck script).

    PYTHONPATH=~/pokeplatinum python3 perfectline.py    # a self-check on Roark

Nothing here writes to the repo. fightsim's `give_status` is replaced in
memory, because its end-of-turn and switch-in code call it by name for
Yawn and Toxic Spikes, and the search needs sleep's length to be the
adversary's rather than a die.
"""
import collections
import random
import time
import zlib

from . import fightsim as fs, fightai

# Oxide's critical hits (src/battle/battle_lib.c sCriticalStageRates and
# battle_script.c ApplyCriticalMul, not fightsim's Platinum values): 1 in 24
# at neutral, 1 in 8 at +1, 1 in 2 at +2, certain from +3; 1.5 times damage,
# 2.25 with Sniper.
CRIT_RATE = {0: 1 / 24, 1: 1 / 8, 2: 1 / 2, 3: 1.0, 4: 1.0}
CRIT_MUL = 1.5
# The luck budget: the adversary may pick any run of bad luck at least this
# likely. One critical hit's worth (design.md, question 1).
BUDGET = 1 / 24
# The trainer's AI is sampled this many times at a state. Its most frequent
# pick is the adversary's for free; any other pick is bad luck for the
# player at its sampled frequency, spent from the same budget as a crit
# (question 7). A pick seen fewer than AI_MIN times is not offered.
AI_SAMPLES = 32
AI_MIN = 2
# A line longer than this is no line; a search past this many states, or
# this many seconds, is undecided.
TURN_CAP = 60
NODE_CAP = 15000
TIME_CAP = 12.0
# Bad luck strikes at the first opportunity of a matchup (design.md, "The
# search"): a kind of event passed over once, while these two Pokemon
# face each other, is not offered again until one of them leaves. Without
# this the adversary chooses the timing of every event and a winning
# strategy has to be verified against every timing.
FIRST_CHANCE = True
# Sleep and confusion last their longest on the player and shortest on the
# trainer (questions 5 and 6); the counters are fightsim's own units.
SLEEP_ON = {"p": 4, "b": 1}
CONFUSION_ON = {"p": 5, "b": 2}
TAUNT_ON = {"p": 5, "b": 3}
BIND_ON = {"p": 5, "b": 2}
OUTRAGE_TURNS = {"p": 2, "b": 3}

FREE = 1.0


class Luck:
    """The dice of one turn, as a script. Each chance point asks for an
    event with the cost of each option (option 0 is the default, no bad
    luck, at no cost); the script answers the first events and the rest
    take the default. `events` records what was asked, so the enumerator
    can branch on it afterwards; `declined` the kinds passed over, which
    stay passed over for the rest of the matchup (FIRST_CHANCE)."""
    __slots__ = ("script", "events", "spent", "declined")

    def __init__(self, script, spent, declined=frozenset()):
        self.script = script
        self.events = []
        self.spent = spent
        self.declined = set(declined)

    def event(self, kind, costs):
        i = len(self.events)
        self.events.append((kind, tuple(costs)))
        opt = self.script[i] if i < len(self.script) else 0
        if opt:
            self.spent *= costs[opt]
        else:
            self.declined.add(kind)
        return opt

    def bad(self, kind, p):
        """Whether the bad thing with probability p happens."""
        if p <= 0:
            return False
        if p >= 1:
            return True
        return self.event(kind, (FREE, p)) == 1

    def choice(self, kind, n):
        """The adversary's free pick among n options."""
        if n <= 1:
            return 0
        return self.event(kind, (FREE,) * n)


class SearchDice:
    """The adversary's dice for the strict search: every chance point is
    a Luck event, and every certainty goes the trainer's way."""
    def __init__(self, luck):
        self.luck = luck
        self.mode = "search"

    def bad(self, kind, p):
        return self.luck.bad(kind, p)

    def good(self, p):
        return False

    def roll(self, top):
        return 15 if top else 0

    def sleep(self, side):
        return SLEEP_ON[side]

    def confusion(self, side):
        return CONFUSION_ON[side]

    def taunt(self, side):
        return TAUNT_ON[side]

    def bind(self, side):
        return BIND_ON[side]

    def outrage(self, side):
        return OUTRAGE_TURNS[side]

    def thaws(self, mon):
        return not player(mon)

    def tie_player_first(self):
        return False

    def choice(self, kind, n):
        return self.luck.choice(kind, n)

    def confusion_roll(self):
        return 100


class RunDice:
    """Real dice for a random run, under Ian's rules of 2026-09-30: a
    secondary status against the player always lands (the turn code never
    asks the dice for it), and at most one critical hit lands on the
    player in a fight. Everything else rolls at the game's odds."""
    def __init__(self, rng, one_crit=True):
        self.rng = rng
        self.mode = "run"
        self.one_crit = one_crit
        self.crit_used = False

    def bad(self, kind, p):
        if kind == "crit" and self.one_crit and self.crit_used:
            return False
        hit = self.rng.random() < p
        if hit and kind == "crit":
            self.crit_used = True
        return hit

    def good(self, p):
        return self.rng.random() < p

    def roll(self, top):
        return self.rng.randrange(16)

    def sleep(self, side):
        return self.rng.randint(1, 4)

    def confusion(self, side):
        return self.rng.randint(2, 5)

    def taunt(self, side):
        return self.rng.randint(3, 5)

    def bind(self, side):
        return self.rng.randint(2, 5)

    def outrage(self, side):
        return self.rng.randint(2, 3)

    def thaws(self, mon):
        return self.rng.random() < 0.2

    def tie_player_first(self):
        return self.rng.random() < 0.5

    def choice(self, kind, n):
        return self.rng.randrange(n)

    def confusion_roll(self):
        return self.rng.randint(85, 100)


def player(mon):
    return mon.side == "p"


def damage_of(b, att, dfn, mv, crit, top, roll=None):
    """fightsim's damage arithmetic with Oxide's critical hit: the top roll
    (top) or the bottom one, or roll index `roll`, stages (a crit ignores
    the ones that would weaken it), burn, Guts, the player's booster,
    screens, 1.5x on a crit."""
    rolls = b.rolls(att, dfn, mv)
    if not rolls:
        return None
    base = rolls[min(roll, len(rolls) - 1)] if roll is not None else (rolls[-1] if top else rolls[0])
    if base <= 0:
        return 0
    a_st, d_st = ("atk", "def") if mv.cat == "Physical" else ("spa", "spd")
    a, d = att.stages[a_st], dfn.stages[d_st]
    if crit:
        a, d = max(a, 0), min(d, 0)
    mult = fs.stage_mult(a) / fs.stage_mult(d)
    if mv.cat == "Physical" and att.status == "brn" and att.ability != "Guts":
        mult *= 0.5
    if att.ability == "Guts" and att.status:
        mult *= 1.5
    if att.side == "p" and fs.BOOSTER_TYPE.get(att.item) == mv.type:
        mult *= 1.2
    side = b.p if dfn.side == "p" else b.b
    screen = "Reflect" if mv.cat == "Physical" else "Light Screen"
    if side.screens[screen] and not crit:
        mult *= 0.5
    if crit:
        mult *= CRIT_MUL * (1.5 if att.ability == "Sniper" else 1.0)
    mult *= fs.rollout_mult(att, mv)
    return max(1, int(base * mult))


# ---- the turn, with the dice replaced ---------------------------------------------------------

_FS_GIVE_STATUS = fs.give_status


def give_status(b, target, status):
    # A battle fightsim plays with its own dice (pdoubles' double battles)
    # keeps fightsim's sleep roll.
    if not hasattr(b, "dice"):
        return _FS_GIVE_STATUS(b, target, status)
    if not fs.can_status(b, target, status) or fs.leaf_guarded(b, target):
        return False
    target.status = status
    if status == "slp":
        target.sleep = b.dice.sleep(target.side)
    if status == "tox":
        target.toxic = 0
    return True


fs.give_status = give_status   # Yawn and Toxic Spikes inside fightsim reach this one


def accuracy_hits(b, att, dfn, mv):
    """The trainer's moves hit; the player's may miss, at the budget."""
    if mv.acc == 0 or mv.effect == "BYPASS_ACCURACY":
        return True
    acc = mv.acc
    if mv.effect == "THUNDER":
        acc = 100 if b.weather == "Rain" else 50 if b.weather == "Sun" else acc
    if mv.effect == "BLIZZARD" and b.weather == "Hail":
        return True
    s = max(-6, min(6, att.stages["acc"] - dfn.stages["eva"]))
    acc = acc * ((3 + s) / 3 if s >= 0 else 3 / (3 - s))
    if att.ability == "Compound Eyes":
        acc *= 1.3
    if att.ability == "Hustle" and mv.cat == "Physical":
        acc *= 0.8
    if dfn.item in ("Bright Powder", "BrightPowder", "Lax Incense"):
        acc *= 0.9
    if dfn.ability in ("Sand Veil",) and b.weather == "Sand":
        acc *= 0.8
    if dfn.ability in ("Snow Cloak",) and b.weather == "Hail":
        acc *= 0.8
    if acc >= 100:
        return True
    if player(att):
        return not b.dice.bad("miss", 1 - acc / 100)
    return not b.dice.good(1 - acc / 100)      # the trainer's miss is the player's luck


def use_move(b, att, mv, dfn, first):
    if not att.alive():
        return
    if att.recharge:
        att.recharge = False
        return
    if att.status == "frz":
        # In the search the trainer thaws at once and the player stays
        # frozen (question 9); in a run both thaw at 1 in 5 a turn.
        if mv.effect == "THAW_AND_BURN_HIT" or b.dice.thaws(att):
            att.status = None
        else:
            return
    if att.status == "slp":
        if att.sleep > 0:
            att.sleep -= 1
            if mv.effect not in ("DAMAGE_WHILE_ASLEEP", "USE_RANDOM_LEARNED_MOVE_SLEEP"):
                return
        else:
            att.status = None
    if att.flinch:
        att.flinch = False
        return
    if att.confused:
        att.confused -= 1
        if att.confused and (b.dice.bad("confusion", 0.5) if player(att) else b.dice.good(0.5)):
            fs.hurt(b, att, confusion_damage(att, b.dice.confusion_roll()))
            return
    if att.status == "par" and (b.dice.bad("paralysis", 0.25) if player(att) else b.dice.good(0.25)):
        return
    if att.taunt and mv.cat == "Status":
        return
    att.pp[mv.name] = att.pp.get(mv.name, 1) - 1
    if mv.effect not in ("PROTECT", "SURVIVE_WITH_1_HP"):
        att.protect_run = 0
    att.last = mv
    att.last_hit_by = None
    if att.item and att.item.startswith("Choice") and not att.choice:
        att.choice = mv.name
    if mv.effect in fs.TWO_TURN and att.charging is None:
        if mv.effect in ("SOLAR_BEAM", "SKIP_CHARGE_TURN_IN_SUN") and b.weather == "Sun":
            pass
        elif att.item == "Power Herb":
            att.item = None
        else:
            att.charging = mv
            if mv.effect == "CHARGE_TURN_DEF_UP":
                fs.change_stages(att, {"def": 1})
            return
    att.charging = None
    if mv.cat == "Status":
        status_move(b, att, mv, dfn, first)
        return
    attack(b, att, mv, dfn, first)


def struggle_damage(att, dfn, roll):
    """Struggle: 50 power, physical, typeless, no modifiers, at the roll."""
    a = att.stats.get("atk", 50) * fs.stage_mult(att.stages["atk"])
    d = dfn.stats.get("def", 50) * fs.stage_mult(dfn.stages["def"])
    base = ((2 * att.level // 5 + 2) * 50 * a / d) // 50 + 2
    return int(base * roll / 100)


def confusion_damage(mon, roll):
    """A self-hit: a 40-power typeless physical hit at the given roll."""
    a = mon.stats.get("atk", 50) * fs.stage_mult(mon.stages["atk"])
    d = mon.stats.get("def", 50) * fs.stage_mult(mon.stages["def"])
    base = ((2 * mon.level // 5 + 2) * 40 * a / d) // 50 + 2
    return int(base * roll / 100)


def attack(b, att, mv, dfn, first):
    if not dfn.alive():
        return
    if dfn.charging is not None and dfn.charging.effect in fs.INVULNERABLE:
        return
    if dfn.protecting and mv.effect not in ("REMOVE_PROTECT",):
        return
    if mv.effect == "HIT_FIRST_IF_TARGET_ATTACKING":
        nxt = getattr(dfn, "chosen", None)
        if not first or nxt is None or nxt.cat == "Status":
            return
    if mv.effect == "ALWAYS_FLINCH_FIRST_TURN_ONLY" and att.turns_in > 1:
        return
    # Natural Gift and Fling spend the held item, and fail without one;
    # fightsim keeps the item and fires them every turn.
    if mv.name in ("Natural Gift", "Fling"):
        if not att.item or (mv.name == "Natural Gift" and "Berry" not in att.item):
            return
        att.item = None
    if not accuracy_hits(b, att, dfn, mv):
        if mv.effect == "CRASH_ON_MISS":
            fs.hurt(b, att, att.maxhp // 2)
        fs.rollout_after(att, mv, False)
        return
    fs.rollout_after(att, mv, True)
    trainer = not player(att)
    dmg = None
    if mv.effect == "ONE_HIT_KO":
        if att.level < dfn.level:
            return
        p_ohko = (30 + att.level - dfn.level) / 100
        if not (b.dice.bad("ohko", p_ohko) if trainer else b.dice.good(p_ohko)):
            return
        dmg = dfn.hp
    elif mv.effect == "HALVE_HP":
        dmg = max(1, dfn.hp // 2)
    elif mv.effect == "LEVEL_DAMAGE_FLAT":
        dmg = att.level
    elif mv.effect == "SET_HP_EQUAL_TO_USER":
        dmg = max(0, dfn.hp - att.hp)
    elif mv.effect in ("COUNTER", "MIRROR_COAT", "METAL_BURST"):
        hit = att.hit_this_turn
        want = {"COUNTER": "Physical", "MIRROR_COAT": "Special"}.get(mv.effect)
        if not hit or (want and hit[0] != want):
            return
        dmg = int(hit[1] * (1.5 if mv.effect == "METAL_BURST" else 2))
    elif mv.effect == "STRUGGLE":
        # Struggle skips the type chart and every modifier (battle_lib.c
        # returns early for MOVE_STRUGGLE): a 50-power physical hit on stats
        # and stages, at the roll.
        roll = 85 + (b.dice.roll(trainer) if b.dice.mode == "run" else (15 if trainer else 0))
        dmg = struggle_damage(att, dfn, roll)
    if dmg is None:
        crit = False
        if dfn.ability not in ("Battle Armor", "Shell Armor"):
            stage = att.crit_stage + (1 if mv.effect.startswith("HIGH_CRITICAL") or
                                      mv.effect.startswith("CHARGE_TURN_HIGH_CRIT") else 0)
            if att.item in ("Scope Lens", "Razor Claw"):
                stage += 1
            rate = CRIT_RATE[min(stage, 4)]
            crit = b.dice.bad("crit", rate) if trainer else b.dice.good(rate)
        key = att.key
        if mv.name == "Magnitude":
            # The power is rolled first, at the game's odds for either side
            # in a run (the player's own luck, question 1 of design.md), and
            # its row is that power's (fightsim.prepare adds them).
            powers = list(fs.MAGNITUDE_POWERS)
            weights = [fs.MAGNITUDE_POWERS[p] for p in powers]
            rng = getattr(b, "rng", None)
            p = rng.choices(powers, weights)[0] if rng is not None else 70
            att.key = f"{key}#m{p}"
            b.last_magnitude = p
        try:
            dmg = damage_of(b, att, dfn, mv, crit, top=trainer,
                            roll=b.dice.roll(trainer) if b.dice.mode == "run" else None)
        finally:
            att.key = key
        if dmg is None:
            return
        if mv.effect == "DOUBLE_POWER_IF_MOVING_SECOND" and not first:
            dmg *= 2
        if mv.effect == "HIT_BEFORE_SWITCH" and getattr(att, "pursuing", False):
            dmg *= 2
        if mv.effect == "DOUBLE_POWER_WHEN_STATUSED" and att.status:
            dmg *= 2
        if mv.effect == "DOUBLE_POWER_IF_HIT" and att.hit_this_turn:
            dmg *= 2
        if mv.effect == "DOUBLE_POWER_WHEN_BELOW_HALF" and dfn.hp * 2 <= dfn.maxhp:
            dmg *= 2
        if mv.effect == "DOUBLE_POWER_HEAL_SLEEP" and dfn.status == "slp":
            dmg *= 2
    if dmg <= 0:
        return
    if dfn.sub:
        dfn.sub = max(0, dfn.sub - dmg)
        dealt = 0
    else:
        full = dfn.hp == dfn.maxhp
        sturdy = dfn.ability == "Sturdy" and att.ability != "Mold Breaker"
        if dmg >= dfn.hp and full and (dfn.item == "Focus Sash" or sturdy):
            dmg = dfn.hp - 1
            if dfn.item == "Focus Sash" and not sturdy:
                dfn.item = None
        if dmg >= dfn.hp and getattr(dfn, "enduring", False):
            dmg = dfn.hp - 1
        # The trainer's Focus Band is an item proc, in the budget (question 8).
        if dmg >= dfn.hp and dfn.item == "Focus Band" and \
                (b.dice.bad("focusband", 0.1) if not player(dfn) else b.dice.good(0.1)):
            dmg = dfn.hp - 1
        dealt = min(dmg, dfn.hp)
        dfn.hp -= dealt
        fs.berry_check(dfn)
        dfn.hit_this_turn = (mv.cat, dealt)
        dfn.last_hit_by = mv
        if dfn.status == "frz" and mv.type == "Fire":
            dfn.status = None
    e = mv.effect
    if e == "STRUGGLE" and att.ability != "Magic Guard":
        # subscript_struggle: the user loses a quarter of its maximum HP.
        fs.hurt(b, att, max(1, att.maxhp // 4))
    if e in fs.RECOIL and att.ability != "Rock Head":
        fs.hurt(b, att, max(1, int(dealt * fs.RECOIL[e])))
    if e in ("RECOVER_HALF_DAMAGE_DEALT", "RECOVER_DAMAGE_SLEEP"):
        # Big Root raises what a draining move restores by 30%.
        gain = dealt // 2
        fs.heal(att, int(gain * 1.3) if att.item == "Big Root" else gain)
    if e in ("EAT_BERRY",) and dfn.item and "Berry" in dfn.item:
        # Bug Bite and Pluck eat the target's berry and take its effect.
        berry, dfn.item = dfn.item, None
        if berry == "Sitrus Berry":
            fs.heal(att, att.maxhp // 4)
        elif berry == "Oran Berry":
            fs.heal(att, 10)
        elif berry in fs.PINCH_BERRIES:
            fs.change_stages(att, {fs.PINCH_BERRIES[berry]: 1})
    if e == "RECHARGE_AFTER":
        att.recharge = True
    if e in fs.SELF_KO:
        att.hp = 0
    if e == "CONTINUE_AND_CONFUSE_SELF":
        if att.lock is None:
            att.lock = (mv, b.dice.outrage(att.side))
    if att.item == "Life Orb" and dealt and att.ability != "Magic Guard":
        fs.hurt(b, att, att.maxhp // 10)
    if e == "REMOVE_SCREENS":
        side = b.p if player(dfn) else b.b
        side.screens = dict.fromkeys(side.screens, 0)
    def secondary(kind, p):
        """A secondary effect that is luck: against the player at its
        chance from the budget, for the player at its chance as luck."""
        return b.dice.bad(kind, p) if trainer else b.dice.good(p)
    if e in fs.HIT_SELF_STAGES:
        ch, certain = fs.HIT_SELF_STAGES[e]
        if certain or secondary("statup", (mv.chance or 10) / 100):
            fs.change_stages(att, ch)
    if not dfn.alive() or dfn.sub:
        return
    chance = mv.chance or 0
    if dfn.ability == "Shield Dust":
        chance = 0
    if att.ability == "Serene Grace":
        chance = min(100, chance * 2)
    # A secondary status on the player always lands (Ian, 2026-09-30); the
    # player's own lands at its chance in a run and never in the search.
    if e in fs.HIT_STATUS and chance and (trainer or b.dice.good(chance / 100)):
        give_status(b, dfn, fs.HIT_STATUS[e])
    if e == "TRI_ATTACK" and chance and (trainer or b.dice.good(chance / 100)):
        order = ("frz", "par", "brn")
        if b.dice.mode == "run":
            order = (order[b.dice.choice("tri", 3)],)
        for st in order:
            if give_status(b, dfn, st):
                break
    # A flinch and a stat change are not status conditions: they are luck,
    # at the move's chance (design.md, question 10).
    if e in fs.FLINCH_HIT and first and chance and secondary("flinch", chance / 100):
        dfn.flinch = True
    if e == "ALWAYS_FLINCH_FIRST_TURN_ONLY" and first:
        dfn.flinch = True
    # King's Rock and Razor Fang are item procs, in the budget (question 8).
    if first and att.item in ("King's Rock", "Razor Fang") and not dfn.flinch \
            and secondary("kingsrock", 0.1):
        dfn.flinch = True
    if e == "CONFUSE_HIT" and chance and not dfn.confused and (trainer or b.dice.good(chance / 100)):
        dfn.confused = b.dice.confusion(dfn.side)
    if e in fs.HIT_FOE_STAGES and chance and dfn.ability not in ("Clear Body", "White Smoke") \
            and secondary("statdrop", chance / 100):
        fs.change_stages(dfn, fs.HIT_FOE_STAGES[e])
    if e == "SWITCH_HIT":
        att.u_turn = True
    if e in ("BIND_HIT", "WHIRLPOOL") and not dfn.bound:
        dfn.bound = b.dice.bind(dfn.side)
    if e in ("REMOVE_HELD_ITEM", "STEAL_HELD_ITEM"):
        dfn.item = None


def status_move(b, att, mv, dfn, first):
    e = mv.effect
    foe_side = b.p if player(dfn) else b.b
    own_side = b.p if player(att) else b.b
    targets_foe = mv.range not in ("USER", "USER_SIDE", "ALLY", "FIELD", "USER_OR_ALLY")
    if targets_foe and dfn.alive():
        if dfn.protecting:
            return
        # Only Thunder Wave among the status moves meets the type chart
        # (BattleControllerPlayer_CheckTypeChart): it fails on a Ground type,
        # while Hypnosis sleeps a Dark type and Will-O-Wisp burns a Normal one.
        if mv.name == "Thunder Wave" and fs.effectiveness(b.st["chart"], mv.type, dfn.types) == 0:
            return
        # Grass types and Overcoat are immune to powder and spore moves.
        if fs.powder_immune(dfn, mv):
            return
        if not accuracy_hits(b, att, dfn, mv):
            return
    if e in fs.STATUS_OF:
        if dfn.sub:
            return
        give_status(b, dfn, fs.STATUS_OF[e])
    elif e == "STATUS_CONFUSE":
        if not dfn.sub and not dfn.confused and dfn.ability != "Own Tempo":
            dfn.confused = b.dice.confusion(dfn.side)
    elif e in ("ATK_UP_2_STATUS_CONFUSION", "SP_ATK_UP_CAUSE_CONFUSION"):
        if not dfn.sub:
            fs.change_stages(dfn, {"atk": 2} if e.startswith("ATK") else {"spa": 1})
            if not dfn.confused and dfn.ability != "Own Tempo":
                dfn.confused = b.dice.confusion(dfn.side)
    elif e == "STATUS_SLEEP_NEXT_TURN":
        if not dfn.status and not dfn.yawn and not dfn.sub:
            dfn.yawn = 2
    elif e == "PREVENT_ESCAPE":
        if dfn.trapped_by is None and not dfn.sub:
            dfn.trapped_by = att.key
    elif e == "GROUND_TRAP_USER_CONTINUOUS_HEAL":
        att.ingrained = True
    elif e == "STATUS_LEECH_SEED":
        if "Grass" not in dfn.types and not dfn.sub:
            dfn.seeded = True
    elif e in fs.SELF_STAGES:
        fs.change_stages(att, fs.SELF_STAGES[e])
        if e == "DEF_UP_DOUBLE_ROLLOUT_POWER":
            att.curled = True
    elif e in fs.FOE_STAGES:
        if not dfn.sub and dfn.ability not in ("Clear Body", "White Smoke"):
            fs.change_stages(dfn, fs.FOE_STAGES[e])
    elif e == "CURSE":
        if "Ghost" in att.types:
            fs.hurt(b, att, att.maxhp // 2)
            dfn.cursed = True
        else:
            fs.change_stages(att, {"atk": 1, "def": 1, "spe": -1})
    elif e == "MAX_ATK_LOSE_HALF_MAX_HP":
        if att.hp > att.maxhp // 2:
            fs.hurt(b, att, att.maxhp // 2)
            att.stages["atk"] = 6
    elif e == "CRIT_UP_2":
        att.crit_stage = 2
    elif e in fs.HEAL_HALF:
        fs.heal(att, att.maxhp // 2)
    elif e == "HEAL_HALF_MORE_IN_SUN":
        frac = 2 / 3 if b.weather == "Sun" else 1 / 4 if b.weather else 1 / 2
        fs.heal(att, int(att.maxhp * frac))
    elif e == "REST":
        if att.hp < att.maxhp:
            att.hp, att.status, att.sleep, att.toxic = att.maxhp, "slp", 2, 0
    elif e == "SWALLOW":
        fs.heal(att, att.maxhp // 4)
    elif e == "SET_LIGHT_SCREEN":
        if not own_side.screens["Light Screen"]:
            own_side.screens["Light Screen"] = 8 if att.item == "Light Clay" else 5
    elif e == "SET_REFLECT":
        if not own_side.screens["Reflect"]:
            own_side.screens["Reflect"] = 8 if att.item == "Light Clay" else 5
    elif e in fs.WEATHER_OF:
        if b.weather != fs.WEATHER_OF[e]:
            rock = {"Sun": "Heat Rock", "Rain": "Damp Rock", "Sand": "Smooth Rock", "Hail": "Icy Rock"}
            b.weather = fs.WEATHER_OF[e]
            b.weather_turns = 8 if att.item == rock.get(b.weather) else 5
    elif e == "TRICK_ROOM":
        if b.trick_room < 999:               # a permanent room (Saturn 2) cannot be ended
            b.trick_room = 0 if b.trick_room else 5
    elif e == "DOUBLE_SPEED_3_TURNS":
        if not own_side.tailwind:
            own_side.tailwind = 3
    elif e == "STEALTH_ROCK":
        foe_side.hazards["rocks"] = 1
    elif e == "SET_SPIKES":
        foe_side.hazards["spikes"] = min(3, foe_side.hazards["spikes"] + 1)
    elif e == "TOXIC_SPIKES":
        foe_side.hazards["tspikes"] = min(2, foe_side.hazards["tspikes"] + 1)
    elif e == "PROTECT" or e == "SURVIVE_WITH_1_HP":
        # A first Protect works. A repeat works at 1/2^run: for the player
        # its failing is bad luck, for the trainer its working is.
        p_work = 1 / (2 ** att.protect_run)
        if att.protect_run == 0:
            works = True
        elif player(att):
            works = not b.dice.bad("protectfail", 1 - p_work)
        else:
            works = b.dice.bad("protectworks", p_work)
        if works:
            att.protecting = e == "PROTECT"
            att.enduring = e == "SURVIVE_WITH_1_HP"
            att.protect_run += 1
        else:
            att.protect_run = 0
    elif e == "SET_SUBSTITUTE":
        if not att.sub and att.hp > att.maxhp // 4:
            fs.hurt(b, att, att.maxhp // 4)
            att.sub = att.maxhp // 4
    elif e == "RESET_STAT_CHANGES":
        for m in (att, dfn):
            m.stages = dict.fromkeys(fs.STAGE_KEYS, 0)
    elif e in ("HEAL_STATUS", "CURE_PARTY_STATUS"):
        for m in own_side.mons:
            m.status = None
    elif e == "PREVENT_STATUS":
        own_side.safeguard = 5
    elif e == "TAUNT":
        if not dfn.taunt:
            dfn.taunt = b.dice.taunt(dfn.side)
    elif e == "FORCE_SWITCH":
        bench = foe_side.bench()
        if bench and not getattr(dfn, "ingrained", False):
            nxt = bench[b.dice.choice("roar", len(bench))]
            fs.switch_in(b, foe_side, foe_side.mons.index(nxt))
    elif e == "FAINT_AND_ATK_SP_ATK_DOWN_2":
        att.hp = 0
        fs.change_stages(dfn, {"atk": -2, "spa": -2})
    elif e == "PASS_STATS_AND_STATUS":
        att.baton = True
    elif e == "ALL_FAINT_3_TURNS":
        for m in (b.p.on_field() + b.b.on_field()):
            if m.alive() and not m.perish and m.ability != "Soundproof":
                m.perish = 4


# ---- state copies and keys -----------------------------------------------------------------------

def clone_mon(m):
    c = fs.Mon.__new__(fs.Mon)
    c.__dict__.update(m.__dict__)
    c.stages = dict(m.stages)
    c.pp = dict(m.pp)
    return c


def clone_side(s):
    c = fs.Side.__new__(fs.Side)
    c.mons = [clone_mon(m) for m in s.mons]
    c.name, c.active, c.active2 = s.name, s.active, s.active2
    c.screens = dict(s.screens)
    c.tailwind, c.safeguard = s.tailwind, s.safeguard
    c.hazards = dict(s.hazards)
    return c


def clone_battle(b):
    c = fs.Battle.__new__(fs.Battle)
    c.st = b.st
    c.rng = None
    c.p, c.b = clone_side(b.p), clone_side(b.b)
    c.weather, c.weather_turns = b.weather, b.weather_turns
    c.trick_room, c.turn, c.ai_flags = b.trick_room, b.turn, b.ai_flags
    c.log = []
    c.luck_spent = b.luck_spent
    c.declined = getattr(b, "declined", frozenset())
    return c


def _name(x):
    return None if x is None else x.name


def mon_key(m):
    return (m.hp, m.status, m.sleep, m.toxic, tuple(m.stages.values()), m.confused, m.flinch,
            m.seeded, m.yawn, m.protect_run, m.sub, _name(m.charging), m.recharge,
            (m.lock[0].name, m.lock[1]) if m.lock else None, m.choice, m.taunt,
            None if m.last is None else m.last.cat, min(m.turns_in, 2), _name(m.last_hit_by),
            m.crit_stage, m.bound, m.cursed, m.perish, m.item, tuple(sorted(m.pp.items())),
            m.enduring, m.protecting, m.ability)


def side_key(s):
    return (s.active, tuple(mon_key(m) for m in s.mons), tuple(s.screens.values()), s.tailwind,
            tuple(s.hazards.values()), s.safeguard)


def state_key(b):
    return (side_key(b.p), side_key(b.b), b.weather, b.weather_turns, b.trick_room,
            round(b.luck_spent, 6), getattr(b, "declined", frozenset()))


def shape_key(b):
    """The state without its HP totals and luck: what `vector` leaves out."""
    def side(sd):
        return (sd.active, tuple(mon_key(m)[1:] for m in sd.mons), tuple(sd.screens.values()),
                sd.tailwind, tuple(sd.hazards.values()), sd.safeguard)
    return (side(b.p), side(b.b), b.weather, b.weather_turns, b.trick_room,
            getattr(b, "declined", frozenset()))


def vector(b):
    """(the player's HPs, the trainer's HPs, luck spent): the parts of a
    state that order it. A state is worse for the player than another of
    the same shape when its player HPs are no higher, its trainer HPs no
    lower, and the adversary has no less budget left (spent no lower)."""
    return (tuple(m.hp for m in b.p.mons), tuple(m.hp for m in b.b.mons), round(b.luck_spent, 6))


def worse_or_equal(v, w):
    """Whether state v is worse for the player than w, or the same."""
    return (all(a <= c for a, c in zip(v[0], w[0])) and all(a >= c for a, c in zip(v[1], w[1]))
            and v[2] >= w[2] - 1e-9)


# ---- the adversary's and the player's options ----------------------------------------------------

def ai_key(b):
    """What the trainer's AI reads at a state: its own active Pokemon whole,
    the player's active one by the HP bands the scoring uses and by which of
    the trainer's moves would knock it out, who is alive on each bench, the
    field, and whether it is the first turn."""
    u, t = b.b.cur(), b.p.cur()
    kills = tuple((fightai.figure(b, u, t, m) or 0) >= t.hp for m in u.moves)
    tk = mon_key(t)
    tk = (_band(t.frac()), kills) + tk[1:]
    uk = mon_key(u)
    uk = (_band(u.frac()), u.hp == u.maxhp) + uk[1:]
    return (uk, tk, tuple(m.alive() for m in b.p.mons), tuple(m.alive() for m in b.b.mons),
            b.p.active, b.b.active, tuple(b.p.screens.values()), tuple(b.b.screens.values()),
            b.p.tailwind, b.b.tailwind, tuple(b.p.hazards.values()), tuple(b.b.hazards.values()),
            b.p.safeguard, b.b.safeguard, b.weather, b.trick_room > 0, b.turn == 0, b.ai_flags)


_AI_CACHE = {}


def _band(frac):
    """The HP bands the AI's scoring reads."""
    return (frac >= 100, frac >= 90, frac > 80, frac > 70, frac >= 60, frac > 50, frac >= 40,
            frac > 30, frac > 25)


_figure = fightai.figure


def figure(b, u, t, mv):
    """The AI's damage figure, with Natural Gift and Fling worth nothing
    once the item is spent (the calculator's row still has the power)."""
    if mv.name in ("Natural Gift", "Fling") and (not u.item or (mv.name == "Natural Gift" and "Berry" not in u.item)):
        return 0
    return _figure(b, u, t, mv)


fightai.figure = figure

_EFF = {}
_effectiveness = fs.effectiveness


def effectiveness(blob_or_chart, atk_type, def_types):
    """fightsim's type-chart lookup, memoised; the chart is one object."""
    k = (id(blob_or_chart), atk_type, tuple(def_types))
    v = _EFF.get(k)
    if v is None:
        v = _effectiveness(blob_or_chart, atk_type, def_types)
        _EFF[k] = v
    return v


fs.effectiveness = effectiveness


def ai_actions(b, key=None):
    """The trainer's actions at this state with their sampled frequencies,
    most frequent first: [(('move', Move) or ('switch', index), frequency)].
    Cached by what the AI reads."""
    u, t = b.b.cur(), b.p.cur()
    k = ai_key(b)
    got = _AI_CACHE.get(k)
    if got is None:
        rng = random.Random(zlib.crc32(repr(k).encode()))
        b.rng = rng
        counts = collections.Counter()
        for _s in range(AI_SAMPLES):
            a = fightai.choose(b, u, t)
            counts[(a[0], a[1].name if a[0] == "move" else a[1])] += 1
        b.rng = None
        got = [(kk, c / AI_SAMPLES) for kk, c in counts.most_common() if c >= AI_MIN]
        _AI_CACHE[k] = got
    out = []
    for (kind, what), f in got:
        if kind == "move":
            out.append((("move", next(m for m in u.moves if m.name == what)), f))
        else:
            out.append((("switch", what), f))
    return out


def dmg_low(b, att, dfn, mv):
    """The player's bottom roll, stages and screens applied."""
    r = b.rolls(att, dfn, mv)
    if not r:
        return 0
    return b.damage(att, dfn, mv, roll=0) or 0


def dmg_top(b, att, dfn, mv):
    """The trainer's top roll, no critical hit."""
    r = b.rolls(att, dfn, mv)
    if not r:
        return 0
    return b.damage(att, dfn, mv, roll=len(r) - 1) or 0


def player_actions(b):
    """The player's options: moves with PP that would do something, and
    switches to a living bench member. The search orders them."""
    me, foe = b.p.cur(), b.b.cur()
    if me.lock:
        return [("move", me.lock[0])]
    if me.charging is not None:
        return [("move", me.charging)]
    if me.recharge:
        return [("move", me.moves[0])]
    out = []
    for mv in me.moves:
        if me.pp.get(mv.name, 1) <= 0 or (me.taunt and mv.cat == "Status"):
            continue
        if me.choice and mv.name != me.choice:
            continue
        if mv.effect in fs.SELF_KO or mv.effect == "FAINT_AND_ATK_SP_ATK_DOWN_2":
            continue
        f = fightai.figure(b, me, foe, mv)
        if fightai.basic(b, me, foe, mv, f) <= -8:
            continue           # a move that would do nothing here
        out.append(("move", mv))
    if not me.bound:
        for i, m in enumerate(b.p.mons):
            if i != b.p.active and m.alive():
                out.append(("switch", i))
    return out


def evaluate(b):
    """How the fight stands for the player, for ordering only: HP and
    Pokemon on each side, the player's statuses against it, and the luck
    the adversary has already spent for it."""
    if player_lost(b):
        return -100.0
    p = sum(m.hp / m.maxhp for m in b.p.mons) + 0.25 * sum(1 for m in b.p.mons if m.alive())
    f = sum(m.hp / m.maxhp for m in b.b.mons if m.alive()) + 0.5 * sum(1 for m in b.b.mons if m.alive())
    pen = sum(0.3 for m in b.p.mons if m.status in ("slp", "frz")) \
        + sum(0.15 for m in b.p.mons if m.status in ("par", "brn", "tox", "psn"))
    return p - f - pen + 0.2 * (1 - b.luck_spent)


def exchange(b, budget):
    """The plain exchange between the two active Pokemon from here, as a
    player reads it: turns the player needs at its bottom rolls, turns the
    foe needs at its top rolls with a critical hit if the budget still
    allows one, and who moves first (a tie goes to the foe)."""
    me, foe = b.p.cur(), b.b.cur()
    mine = max((dmg_low(b, me, foe, mv) for mv in me.moves
                if mv.damaging() and me.pp.get(mv.name, 1) > 0 and mv.effect not in fs.SELF_KO
                and (not me.choice or mv.name == me.choice)), default=0)
    theirs = [(dmg_top(b, foe, me, mv), damage_of(b, foe, me, mv, True, True) or 0)
              for mv in foe.moves if mv.damaging() and foe.pp.get(mv.name, 1) > 0]
    plain = max((t[0] for t in theirs), default=0)
    crit = max((t[1] for t in theirs), default=0)
    if b.luck_spent * CRIT_RATE[0] < budget - 1e-12:
        crit = plain
    t_me = -(-foe.hp // mine) if mine > 0 else 99
    if plain <= 0:
        t_foe = 99
    else:
        left = me.hp - crit
        t_foe = 1 if left <= 0 else 1 + -(-left // plain)
    sm, sf = b.speed(me), b.speed(foe)
    if b.trick_room:
        sm, sf = -sm, -sf
    first = sm > sf
    win = t_me < t_foe or (t_me == t_foe and first)
    return win, t_me, t_foe


def ordering_score(b, budget, before):
    """The number the player's actions are ordered by, read on the worst
    turn each leads to: a knockout counts most, then winning the exchange
    in front of it, then how quickly, then the HP picture. `before` is the
    parent's count of standing foes."""
    if player_lost(b):
        return -100.0
    if not b.b.alive():
        return 100.0
    win, t_me, _t_foe = exchange(b, budget)
    kos = before - len(b.b.alive())
    return 12.0 * kos + (6.0 if win else 0.0) - 0.5 * min(t_me, 20) + evaluate(b)


# ---- one turn ---------------------------------------------------------------------------------------

def _turn(c, pa, aa):
    """The turn's body on a battle whose dice are set: switches, the two
    moves in order, the end of the turn, a knockout's replacement."""
    b_active_p, b_active_b = c.p.active, c.b.active
    if pa[0] == "switch" and not fs.can_switch(c.p.cur()):
        raise ValueError(f"{c.p.cur().species} is trapped and cannot switch")
    # Pursuit hits a Pokemon that is switching out before it leaves, at
    # double power, and is then spent for the turn.
    if pa[0] == "switch" and aa[0] == "move" and aa[1].effect == "HIT_BEFORE_SWITCH" and c.b.cur().alive():
        c.b.cur().pursuing = True
        use_move(c, c.b.cur(), aa[1], c.p.cur(), True)
        c.b.cur().pursuing = False
        aa = ("none", None)
        if not c.p.cur().alive():
            pa = ("none", None)
    if aa[0] == "switch" and pa[0] == "move" and pa[1].effect == "HIT_BEFORE_SWITCH" and c.p.cur().alive():
        c.p.cur().pursuing = True
        use_move(c, c.p.cur(), pa[1], c.b.cur(), True)
        c.p.cur().pursuing = False
        pa = ("none", None)
    if pa[0] == "switch":
        fs.switch_in(c, c.p, pa[1])
    if aa[0] == "switch":
        fs.switch_in(c, c.b, aa[1])
    me, foe = c.p.cur(), c.b.cur()
    order = []
    if pa[0] == "move":
        order.append((me, pa[1]))
    if aa[0] == "move":
        order.append((foe, aa[1]))
    for mon, mv in order:
        mon.chosen = mv
    if len(order) == 2:
        (a, ma), (d, md) = order
        if ma.pri != md.pri:
            order.sort(key=lambda o: -o[1].pri)
        else:
            sa, sd = c.speed(a), c.speed(d)
            if c.trick_room:
                sa, sd = -sa, -sd
            if sa < sd or (sa == sd and not c.dice.tie_player_first()):
                # The player is slower: its Quick Claw (one in five) keeps it
                # first. Before this the check sat after this branch and could
                # never fire.
                if not (me.item == "Quick Claw" and c.dice.good(0.2)):
                    order.reverse()
            elif foe.item == "Quick Claw" and c.dice.bad("quickclaw", 0.2):
                order.reverse()
    for i, (mon, mv) in enumerate(order):
        target = fs.foe_of(c, mon)
        first = i == 0 and len(order) == 2
        use_move(c, mon, mv, target, first)
        if getattr(mon, "u_turn", False):
            mon.u_turn = False
            side = c.p if player(mon) else c.b
            if side.bench():
                if side is c.p:
                    idx = fs.player_replacement(c)
                else:
                    idx = fightai.replacement(c, side, fs.foe_of(c, mon))
                if idx is not None and idx != side.active:
                    fs.switch_in(c, side, idx)
    fs.end_of_turn(c)
    for mon in (c.p.cur(), c.b.cur()):
        if mon.lock:
            mv, left = mon.lock
            mon.lock = (mv, left - 1) if left > 1 else None
            if left <= 1 and not mon.confused and mv.effect == "CONTINUE_AND_CONFUSE_SELF":
                mon.confused = c.dice.confusion(mon.side)
    if c.b.alive() and not c.b.cur().alive():
        idx = fightai.replacement(c, c.b, c.p.cur())
        if idx is not None:
            fs.switch_in(c, c.b, idx)
    # A run played past a death (plines' mean deaths and wipe chance) needs
    # the player's knocked-out Pokemon replaced too; before any death this
    # never fires, so a clean result is unchanged.
    if c.p.alive() and not c.p.cur().alive():
        idx = fs.player_replacement(c)
        if idx is None or not c.p.mons[idx].alive():
            idx = next(i for i, m in enumerate(c.p.mons) if m.alive())
        fs.switch_in(c, c.p, idx)
    # The matchup changed (a switch on either side, or a knockout): every
    # kind of bad luck is on offer again.
    return (c.p.active == b_active_p and c.b.active == b_active_b
            and c.p.cur().alive() and c.b.cur().alive() and pa[0] != "switch" and aa[0] != "switch")


def step(b, pa, aas, script):
    """The turn after the player's choice under one luck script, whose
    first event is the trainer's pick among `aas` (the most frequent free,
    the others at their frequency): a new battle."""
    c = clone_battle(b)
    c.luck = Luck(script, b.luck_spent, c.declined if FIRST_CHANCE else frozenset())
    c.dice = SearchDice(c.luck)
    aa = aas[c.luck.event("ai", (FREE,) + tuple(f for _a, f in aas[1:]))][0]
    same = _turn(c, pa, aa)
    c.luck_spent = c.luck.spent
    c.declined = frozenset(c.luck.declined) if same else frozenset()
    return c


def play_turn(b, pa, rng, one_crit=True):
    """One turn of a random run, in place: the trainer's AI picks with real
    dice, and so does everything else (RunDice)."""
    b.rng = rng
    b.dice = RunDice(rng, one_crit) if not isinstance(getattr(b, "dice", None), RunDice) else b.dice
    b.dice.rng = rng
    aa = fightai.choose(b, b.b.cur(), b.p.cur())
    _turn(b, pa, aa)
    return b


def outcomes(b, pa, aas, budget):
    """Every child of the player's choice under the allowed runs of bad
    luck, the trainer's pick included: the turn with the free pick and no
    bad luck, then one more for each event whose flip still fits the
    budget, recursively."""
    stack = [()]
    out = []
    while stack:
        script = stack.pop()
        child = step(b, pa, aas, script)
        out.append(child)
        spent = b.luck_spent
        declined = set(getattr(b, "declined", ())) if FIRST_CHANCE else set()
        for i, (kind, costs) in enumerate(child.luck.events):
            chosen = script[i] if i < len(script) else 0
            if i >= len(script) and kind not in declined:
                for opt in range(1, len(costs)):
                    if spent * costs[opt] >= budget - 1e-12:
                        stack.append(script + (0,) * (i - len(script)) + (opt,))
            if chosen:
                spent *= costs[chosen]
            else:
                declined.add(kind)
    return out


def player_lost(b):
    return any(not m.alive() for m in b.p.mons)


def danger(b):
    return min(m.hp / m.maxhp for m in b.p.mons)


# ---- the search ----------------------------------------------------------------------------------------

# The search widens by discrepancies (limited discrepancy search): a pass
# with d discrepancies may leave the greedy first choice at most d times
# along a line, on the lead or on any turn. The passes run d = 0, 1, 2, ...
# and share their memos, so an easy fight is decided by the greedy line
# alone and a hard one spends its node budget on the lines nearest to it,
# which is where a player looks too.
MAX_DISC = 8


class Search:
    def __init__(self, budget=BUDGET, node_cap=NODE_CAP, time_cap=TIME_CAP):
        self.budget = budget
        self.node_cap = node_cap
        self.time_cap = time_cap
        self.win = collections.defaultdict(list)    # shape: [vector] known to win
        self.fail = collections.defaultdict(list)   # shape: [(vector, disc)] known to fail
        self.acts = {}           # state key: (the trainer's actions, the player's)
        self.nodes = 0
        self.capped = False
        self.t0 = time.time()

    def known_win(self, shape, v):
        """A stored win from a state worse than or equal to this one."""
        return any(worse_or_equal(w, v) for w in self.win.get(shape, ()))

    def known_fail(self, shape, v, disc):
        """A stored failure, at no fewer discrepancies, from a state better
        than or equal to this one."""
        return any(d >= disc and worse_or_equal(v, w) for w, d in self.fail.get(shape, ()))

    def note_win(self, shape, v):
        rows = self.win[shape]
        rows[:] = [w for w in rows if not worse_or_equal(v, w)]   # keep only the worst wins
        rows.append(v)
        self.fail[shape] = [(w, d) for w, d in self.fail.get(shape, ()) if w != v]

    def note_fail(self, shape, v, disc):
        self.fail[shape].append((v, disc))

    def options(self, b, key):
        """The trainer's actions and the player's, the player's ordered by
        the worst turn each leads to (a one-turn lookahead), with the ones
        that lose a Pokemon outright left out. Cached by state."""
        got = self.acts.get(key)
        if got is None:
            aas = ai_actions(b, key)
            ranked = []
            for pa in player_actions(b):
                kids = outcomes(b, pa, aas, self.budget)
                before = len(b.b.alive())
                worst = min((ordering_score(k, self.budget, before) for k in kids), default=-100.0)
                if worst > -100.0:
                    ranked.append((worst, pa))
            ranked.sort(key=lambda x: -x[0])
            got = (aas, [pa for _w, pa in ranked])
            self.acts[key] = got
        return got

    def solve(self, b, depth, disc):
        """True when a perfect line exists from here within `disc`
        discrepancies, False when none does, None when the search gave up."""
        if player_lost(b):
            return False
        if not b.b.alive():
            return True
        if depth >= TURN_CAP:
            return False
        shape, v = shape_key(b), vector(b)
        if self.known_win(shape, v):
            return True
        if self.known_fail(shape, v, disc):
            return False
        if self.capped or self.nodes >= self.node_cap or time.time() - self.t0 > self.time_cap:
            self.capped = True
            return None
        self.nodes += 1
        self.note_fail(shape, v, disc)        # a state that returns to itself is no line
        key = state_key(b)
        aas, pas = self.options(b, key)
        for i, pa in enumerate(pas):
            cost = 0 if i == 0 else 1
            if cost > disc:
                break
            kids = outcomes(b, pa, aas, self.budget)
            kids.sort(key=evaluate)           # the worst turn first
            ok = True
            for kid in kids:
                r = self.solve(kid, depth + 1, disc - cost)
                if r is None:
                    return None
                if not r:
                    ok = False
                    break
            if ok:
                self.note_win(shape, v)
                return True
        return False

    def trace(self, b, depth=0):
        """The found line under no bad luck, for reading: one row a turn."""
        rows = []
        def winning(k):
            return (not k.b.alive() and not player_lost(k)) or \
                (not player_lost(k) and self.known_win(shape_key(k), vector(k)))
        while not player_lost(b) and b.b.alive() and depth < TURN_CAP:
            if not self.known_win(shape_key(b), vector(b)):
                break
            aas, pas = self.options(b, state_key(b))
            chosen = None
            for pa in pas:
                if all(winning(k) for k in outcomes(b, pa, aas, self.budget)):
                    chosen = pa
                    break
            if chosen is None:
                break
            aa = aas[0][0]
            me, foe = b.p.cur(), b.b.cur()
            what = "switch->" + b.p.mons[chosen[1]].species if chosen[0] == "switch" else chosen[1].name
            theirs = "switch" if aa[0] == "switch" else aa[1].name
            others = ", ".join(f"{a[1].name if a[0] == 'move' else 'switch'} {f:.0%}" for a, f in aas[1:])
            rows.append(f"t{depth + 1:>2} {me.species} {me.hp}/{me.maxhp}{' ' + me.status if me.status else ''}"
                        f" {what:24}| {foe.species} {foe.hp}/{foe.maxhp} {theirs}"
                        f"{' (or ' + others + ')' if others else ''}")
            b = step(b, chosen, aas, ())
            depth += 1
        return rows


# ---- building a battle ---------------------------------------------------------------------------------

def make_battle(st, team, boss_keys, flags, lead):
    pm = [fs.Mon(k, st["pokemon"][k], st["info"][k], st["moves"][k], "p") for k in team]
    held = fs.assign_items(st, team) if "split" in st else {}
    for m in pm:
        m.item = held.get(m.key)
    bm = [fs.Mon(k, st["pokemon"][k], st["info"][k], st["moves"][k], "b") for k in boss_keys]
    b = fs.Battle(st, fs.Side(pm, "p"), fs.Side(bm, "b"), None, weather=st.get("base_weather"),
                  trick_room=st.get("trick_room", False), ai_flags=flags)
    b.luck_spent = 1.0
    b.luck = Luck((), 1.0)
    b.dice = SearchDice(b.luck)
    b.declined = frozenset()
    b.p.active = lead
    for side in (b.b, b.p):
        fs.switch_in(b, side, side.active)
    b.luck_spent = b.luck.spent
    return b


def lead_order(st, team, boss_keys, flags, budget=BUDGET):
    """Leads to try, best first: the one that wins its exchange against
    the trainer's lead by the widest margin of turns."""
    scored = []
    for i in range(len(team)):
        b = make_battle(st, team, boss_keys, flags, i)
        if player_lost(b):
            continue
        win, t_me, t_foe = exchange(b, budget)
        scored.append(((1 if win else 0), t_foe - t_me, -t_me, i))
    scored.sort(reverse=True)
    return [i for *_k, i in scored] or list(range(len(team)))


def matchup_wins(st, keys, boss_keys, flags, budget=BUDGET):
    """{key: how many of the trainer's Pokemon it beats one on one from
    full HP, by the exchange reading}: what a planned six is seeded on."""
    out = {}
    for k in keys:
        n = 0
        for j in range(len(boss_keys)):
            order = boss_keys[j:] + boss_keys[:j]
            b = make_battle(st, [k], order, flags, 0)
            if not player_lost(b) and exchange(b, budget)[0]:
                n += 1
        out[k] = n
    return out


def perfect(st, team, boss_keys, flags, budget=BUDGET, node_cap=NODE_CAP, time_cap=TIME_CAP,
            want_trace=False, max_disc=MAX_DISC):
    """Whether this six has a perfect line against this party: {"found":
    True/False/None, "nodes", "seconds", "lead", "disc", "trace"}. found is
    None when the search gave up before deciding."""
    s = Search(budget, node_cap, time_cap)
    leads = lead_order(st, team, boss_keys, flags, budget)
    found, lead_used, trace, disc_used = False, None, None, None
    for disc in range(max_disc + 1):
        for j, lead in enumerate(leads):
            cost = 0 if j == 0 else 1
            if cost > disc:
                break
            b = make_battle(st, team, boss_keys, flags, lead)
            r = s.solve(b, 0, disc - cost)
            if r is None:
                found = None
                break
            if r:
                found, lead_used, disc_used = True, lead, disc
                if want_trace:
                    trace = s.trace(make_battle(st, team, boss_keys, flags, lead))
                break
        if found or found is None:
            break
    return {"found": found, "nodes": s.nodes, "seconds": round(time.time() - s.t0, 2),
            "lead": lead_used, "disc": disc_used, "trace": trace}


# ---- a self-check ---------------------------------------------------------------------------------------

def _selfcheck():
    from tools.oxide.balance import data
    fs.BOX_MODE = True
    fight = next(f for f in data.fights()["fights"] if f["key"] == "roark")
    trainers = data.fight_trainers("oxide", fight)
    st = fs.prepare("Roark", [t["party"] for t in trainers], None, cap=16)
    rng = random.Random(3)
    keys = [k for k in st["player"]]
    for trial in range(4):
        team = fs.draw(st, fs.sample_team(st, rng), rng)
        r = perfect(st, team, st["bosses"][0], trainers[0]["ai"], want_trace=True)
        print([st["pokemon"][k]["species"] for k in team], r["found"], r["nodes"], r["seconds"])
        if r["trace"]:
            print("\n".join("   " + row for row in r["trace"]))


if __name__ == "__main__":
    _selfcheck()

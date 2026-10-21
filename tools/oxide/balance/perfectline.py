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
BIND_ON = {"p": 6, "b": 3}
OUTRAGE_TURNS = {"p": 2, "b": 3}

FREE = 1.0

# How a random run's dice fall (Ian, 2026-10-02). "real": the game's own odds
# for everything, crits at 1 in 24 with no cap, which is how fights are
# measured. "unlucky": the stress test, a very unlucky fight, where every
# status and crit check, the trainer's and the player's alike, rolls twice and
# keeps the result worse for the player (STRESS names them; damage rolls and
# accuracy stay at the game's odds). Quick Claw and Focus Band roll the same
# way (Ian, 2026-10-06): the trainer's fire if either roll does, the player's
# only if both do. "budget": Ian's earlier luck budget of
# 2026-09-30 (a secondary status against the player always lands, at most one
# crit lands on the player), kept so the old bar can be re-measured.
LUCK = "real"
STRESS = frozenset({"crit", "status", "confusehit", "flinch", "statdrop", "statup", "kingsrock", "love",
                    "paralysis", "confusion", "thaw", "quickclaw", "focusband"})


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

    def good(self, p, kind=None):
        return False

    def lands_on_player(self, kind, p):
        return True

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
    """Real dice for a random run, as LUCK (or `luck`) sets them: the game's
    odds, the stress test's doubled checks, or the old luck budget, where
    `one_crit` caps the crits on the player at one. `bad` is a chance that
    hurts the player, `good` one that helps it; `kind` names the check."""
    def __init__(self, rng, one_crit=True, luck=None):
        self.rng = rng
        self.mode = "run"
        self.luck = luck or LUCK
        self.one_crit = one_crit and self.luck == "budget"
        self.crit_used = False

    def bad(self, kind, p):
        if kind == "crit" and self.one_crit and self.crit_used:
            return False
        hit = self.rng.random() < p
        if not hit and self.luck == "unlucky" and kind in STRESS:
            hit = self.rng.random() < p          # either of two rolls lands
        if hit and kind == "crit":
            self.crit_used = True
        return hit

    def good(self, p, kind=None):
        hit = self.rng.random() < p
        if hit and self.luck == "unlucky" and kind in STRESS:
            hit = self.rng.random() < p          # both rolls must land
        return hit

    def lands_on_player(self, kind, p):
        """A secondary effect of the trainer's move on the player: always
        under the old budget, else at its chance."""
        return True if self.luck == "budget" else self.bad(kind, p)

    def roll(self, top):
        return self.rng.randrange(16)

    def pick_weighted(self, items, weights):
        return self.rng.choices(items, weights)[0]

    def sleep(self, side):
        return self.rng.randint(1, 4)

    def confusion(self, side):
        return self.rng.randint(2, 5)

    def taunt(self, side):
        return self.rng.randint(3, 5)

    def bind(self, side):
        return self.rng.randint(3, 6)            # subscript_bind_start's Random 3, 3

    def outrage(self, side):
        return self.rng.randint(2, 3)

    def thaws(self, mon):
        return self.good(0.2, "thaw") if player(mon) else self.bad("thaw", 0.2)

    def tie_player_first(self):
        return self.rng.random() < 0.5

    def choice(self, kind, n):
        return self.rng.randrange(n)

    def confusion_roll(self):
        return self.rng.randint(85, 100)


def player(mon):
    return mon.side == "p"


def damage_of(b, att, dfn, mv, crit, top, roll=None, share=None):
    """fightsim's damage arithmetic with Oxide's critical hit: the top roll
    (top) or the bottom one, or roll index `roll`, stages (a crit ignores
    the ones that would weaken it), burn, Guts, Flash Fire's boost only once
    lit, the player's booster, screens (passed by a crit, Brick Break's kind
    and an Infiltrator), 1.5x on a crit. With share, (weight, whole), one
    hit of a move whose row adds up several (fightsim.hit_weights)."""
    rolls = b.rolls(att, dfn, mv)
    if not rolls:
        return None
    base = rolls[min(roll, len(rolls) - 1)] if roll is not None else (rolls[-1] if top else rolls[0])
    if base <= 0:
        return 0
    if share is not None:
        base = base * share[0] / share[1]
    a_st, d_st = ("atk", "def") if mv.cat == "Physical" else ("spa", "spd")
    a, d = att.stages[a_st], dfn.stages[d_st]
    if dfn.ability == "Unaware" and att.ability != "Mold Breaker":
        a = 0                    # Unaware ignores the attacker's stages
    if att.ability == "Unaware" or mv.const in fs.IGNORE_TARGET_STAGES:
        d = 0                    # and, on its own attack, the target's, as Sacred Sword's kind does
    if crit:
        a, d = max(a, 0), min(d, 0)
    mult = fs.stage_mult(a) / fs.stage_mult(d) * fs.state_mult(b, att, dfn, mv)
    if mv.cat == "Physical" and att.status == "brn" and att.ability != "Guts":
        mult *= 0.5
    if att.ability == "Guts" and att.status:
        mult *= 1.5
    if att.ability == "Flash Fire" and mv.type == "Fire" and not att.flash_fire:
        mult *= 2 / 3        # the calculator's row has Flash Fire always lit (fightsim's Battle.damage)
    elif att.gas_stash == "Flash Fire" and att.flash_fire and mv.type == "Fire":
        mult *= 1.5          # lit, it burns on under the gas (BATTLEMON_FLASH_FIRE); the twin's row lacks it
    if att.side == "p" and fs.BOOSTER_TYPE.get(att.item) == mv.type:
        mult *= 1.2
    side = b.p if dfn.side == "p" else b.b
    screen = "Reflect" if mv.cat == "Physical" else "Light Screen"
    # A screen halves neither a critical hit, nor Brick Break's kind, which
    # breaks it, nor an Infiltrator's hit (battle_lib.c, BattleSystem_CalcMoveDamage),
    # as fightsim's Battle.damage has it.
    if (side.screens[screen] or side.aurora_veil) and not crit and mv.effect != "REMOVE_SCREENS" \
            and att.ability != "Infiltrator":
        # Aurora Veil halves both kinds, once with a screen (fightsim.aurora_veil);
        # a double battle's screen takes a third, as Battle.damage has it.
        mult *= 2 / 3 if b.doubles else 0.5
    if b.spread:
        mult *= 0.75             # a double battle's move that hits more than one (fightsim.Battle.spread)
    if mv.sure:
        mult *= fs.row_crit_mult(att, dfn, crit)    # the row's own critical hit (fightsim.row_crit_mult)
    elif crit:
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
        if target.alive() and not target.status and not fs.status_ability_ignored(b, target) \
                and (target.ability in fs.STATUS_ABILITIES.get(status, ()) or fs.leaf_guarded(b, target)):
            fs.reveal(target)
        return False
    target.status = status
    if status == "slp":
        target.sleep = b.dice.sleep(target.side)
    if status == "tox":
        target.toxic = 0
    fs.charge_ends(target, status)   # asleep or frozen, its charge is over (fightsim.charge_ends)
    fs.synchronize(b, target, status)
    fs.cure_berry(target, b)
    return True


fs.give_status = give_status   # Yawn and Toxic Spikes inside fightsim reach this one


def accuracy_hits(b, att, dfn, mv, first=True, later=False):
    """Whether the move lands, a miss bad luck for its user's side.
    `first`: whether the target has yet to move this turn (the Zoom Lens).
    `later`: a later hit of a rising move's or Population Bomb's, whose
    check skips the hit overrides, No Guard and Lock-On (fightsim.RISING,
    fightsim.TEN_HITS)."""
    if mv.acc == 0 or mv.effect == "BYPASS_ACCURACY" or (
            not later and (fs.no_guard(att, dfn, mv) or (dfn.rare and fs.lands_sure(att, dfn, mv)))):
        return True
    acc = mv.acc
    if dfn.ability == "Wonder Skin" and mv.cat == "Status":
        acc = fs.wonder_skin(att, dfn, acc)      # half at most, before the stages (fightsim.wonder_skin)
    weather = fs.weather_now(b)          # none while Cloud Nine or Air Lock is out (NO_CLOUD_NINE)
    if weather == "Rain" and mv.effect in fs.RAIN_SURE:
        return True          # never a miss in the rain, past every stage (fightsim.RAIN_SURE)
    if mv.effect in ("THUNDER", "HURRICANE") and weather == "Sun":
        acc = 50             # Oxide: Hurricane as Thunder in the sun
    if mv.effect == "BLIZZARD" and weather == "Hail":
        return True
    # The stages, with Unaware, Keen Eye and Sacred Sword's kind, Tangled
    # Feet and the Zoom Lens (fightsim.accuracy_scale).
    acc *= fs.accuracy_scale(att, dfn, mv, first)
    if att.ability == "Compound Eyes":
        acc *= 1.3
    if att.item == "Wide Lens":
        acc *= 1.1
    if att.ability == "Hustle" and mv.cat == "Physical":
        acc *= 0.8
    if dfn.item in ("Bright Powder", "BrightPowder", "Lax Incense"):
        acc *= 0.9
    if dfn.ability in ("Sand Veil",) and weather == "Sand" and not fs.mold(att, dfn):
        acc *= 0.8
    if dfn.ability in ("Snow Cloak",) and weather == "Hail" and not fs.mold(att, dfn):
        acc *= 0.8               # Mold Breaker gets past both (Battler_IgnorableAbility)
    if b.fog:
        acc *= fs.fog_cut(b)     # deep fog's six tenths (fightsim.fog_cut)
    if b.gravity:
        acc = acc * 10 / 6       # Gravity's ten sixths, last (fightsim.gravity_start)
    if acc >= 100:
        return True
    if player(att):
        return not b.dice.bad("miss", 1 - acc / 100)
    return not b.dice.good(1 - acc / 100)      # the trainer's miss is the player's luck


fs.DICE_ACCURACY = accuracy_hits   # a landing Future Sight checks its accuracy on these dice


def use_move(b, att, mv, dfn, first, targets=None):
    """One move, then the switch-in check that ends it, where a Neutralizing
    Gas whose holder fell wears off (fightsim.use_move). `targets`: in a
    double battle, the Pokemon a damaging move hits, each in turn
    (fightsim.run_doubles); None in a single battle, where dfn is the one."""
    _use_move(b, att, mv, dfn, first, targets)
    if att.me_first:
        att.me_first = False             # Me First's half again lasts the move it took (fightsim.me_first_move)
    if b.st.get("gas"):
        fs.gas_update(b)
    fs.move_end(b)          # a waiting Trace (fightsim.move_end)


def _use_move(b, att, mv, dfn, first, targets=None):
    if not att.alive():
        return
    att.acted_turn = b.turn          # its action this turn has begun (fightsim._use_move)
    mv = fs.encored_move(att, mv)        # the Encore move, whatever was chosen (fightsim.encored_move)
    att.conversion2_src = (att.last_hit_by, att.last_hit_type) if att.last_hit_by is not None else None
    att.last_hit_by = None           # cleared with its own action, after Conversion 2 has read it (fightsim.use_move)
    att.destiny_bond = False         # and its Destiny Bond with it
    b.status_src = att               # a status this move gives comes from att (Synchronize)
    if att.rare:
        if att.grudge:
            att.grudge = False       # and its Grudge (fightsim.grudge)
        if att.sky_holder is not None and fs.sky_held(b, att):
            return fs.could_not_act(b, att, mv, dfn, targets)     # held in the air by Sky Drop (fightsim.sky_held)
    if att.recharge:
        att.recharge = False
        return fs.could_not_act(b, att, mv, dfn, targets)
    if fs.loafs(att):
        return fs.could_not_act(b, att, mv, dfn, targets)
    if att.status == "frz":
        # In the search the trainer thaws at once and the player stays
        # frozen (question 9); in a run both thaw at 1 in 5 a turn.
        if mv.effect == "THAW_AND_BURN_HIT" or b.dice.thaws(att):
            att.status = None
        else:
            return fs.could_not_act(b, att, mv, dfn, targets)
    if att.status == "slp":
        if fs.sleep_tick(att):
            if mv.effect not in ("DAMAGE_WHILE_ASLEEP", "USE_RANDOM_LEARNED_MOVE_SLEEP"):
                return fs.could_not_act(b, att, mv, dfn, targets)
    if att.flinch:
        fs.flinched(att)                 # Steadfast answers it
        return fs.could_not_act(b, att, mv, dfn, targets)
    if att.disabled is not None and mv.name == att.disabled:
        att.choice = None                # subscript_move_is_disabled lets go of a Choice item's lock
        return fs.could_not_act(b, att, mv, dfn, targets)
    # Taunt, Imprison, Gravity, Heal Block and Throat Chop, in the engine's
    # order, before confusion, paralysis and love (fightsim._use_move).
    if att.taunt and mv.cat == "Status":
        return fs.could_not_act(b, att, mv, dfn, targets)
    if mv.name in att.sealed:
        att.choice = None                # a foe's Imprison, as Disable (fightsim.disabled_out)
        return fs.could_not_act(b, att, mv, dfn, targets)
    if ((att.rare or b.gravity) and fs.move_barred(b, att, mv)) or fs.move_heal_blocked(att, mv):
        return fs.could_not_act(b, att, mv, dfn, targets)     # Gravity's, Heal Block's or Throat Chop's (fightsim.move_barred)
    if att.confused:
        att.confused -= 1
        if att.confused and (b.dice.bad("confusion", 0.5) if player(att) else b.dice.good(0.5, "confusion")):
            fs.hurt(b, att, confusion_damage(att, b.dice.confusion_roll()))
            return fs.could_not_act(b, att, mv, dfn, targets)
    if att.status == "par" and (b.dice.bad("paralysis", 0.25) if player(att) else b.dice.good(0.25, "paralysis")):
        return fs.could_not_act(b, att, mv, dfn, targets)
    if att.infatuated and (b.dice.bad("love", 0.5) if player(att) else b.dice.good(0.5, "love")):
        return fs.could_not_act(b, att, mv, dfn, targets)     # immobilized by love (CHECK_STATUS_STATE_ATTRACT)
    if fs.tormented_out(att, mv):
        return fs.could_not_act(b, att, mv, dfn, targets)
    fs.mark_hit(b, mv, dfn, True, targets)
    prev = fs.note_move(b, mv)           # the move before this one, for Copycat (fightsim.note_move)
    fs.spend_pp(b, att, mv, dfn, targets)     # once a choice, and Pressure's (fightsim.spend_pp)
    paid = mv                        # the slot that paid, whatever it calls (fightsim.grudge)
    if mv.effect not in ("PROTECT", "SURVIVE_WITH_1_HP") and mv.const not in fs.KEEPS_PROTECT_RUN:
        att.protect_run = 0
    att.last = mv
    if att.item and att.item.startswith("Choice") and not att.choice:
        att.choice = mv.name
    fs.protean(b, att, mv)               # Protean retypes its user before the move runs
    if fs.commit_move(att, mv):
        return                       # Last Resort before every other move was used
    if mv.effect in fs.CALLERS:
        # Mirror Move's and Copycat's copy, or Assist's pick on the battle's
        # dice, run as its own (fightsim.called_move).
        mv = fs.called_move(b, att, mv, prev, lambda kind, n: b.dice.choice(kind, n))
        if mv is None:
            return
        fs.mark_hit(b, mv, dfn, True, targets)
    if mv.effect == "USE_MOVE_FIRST":
        mv = fs.me_first_move(att, dfn, first)    # the target's chosen hit, at half again (fightsim.me_first_move)
        if mv is None:
            return
        fs.mark_hit(b, mv, dfn, True, targets)
    if mv.effect == "NATURE_POWER":
        mv = fs.move(fs.nature_power_move(b.st.get("terrain")))     # its terrain's move (fightsim.nature_power_move)
        fs.mark_hit(b, mv, dfn, True, targets)
    if mv.effect in ("FLY", "BOUNCE") and att.smacked:
        return                       # brought down by Smack Down, it cannot fly (fightsim.smack_down)
    if mv.effect == "SKY_DROP" and not b.doubles and not fs.sky_drop(b, att, mv, dfn):
        return                       # Sky Drop's lift, or a drop that fails (fightsim.sky_drop)
    if mv.effect in fs.TWO_TURN and att.charging is None and not fs.charge_skipped(b, att, mv):
        att.charging = mv
        fs.change_stages(att, fs.CHARGE_STAGES.get(mv.effect, {}))   # Skull Bash, Meteor Beam, Electro Shot
        return
    att.charging = None
    if mv.effect == "USE_RANDOM_LEARNED_MOVE_SLEEP":
        mv = fs.sleep_talk_pick(b, att) if att.status == "slp" else None
        if mv is None:
            return
    if mv.cat == "Status":
        thief = fs.snatched(b, att, mv) if b.snatching and mv.snatch else None
        if thief is not None:
            status_move(b, thief, mv, att, first)     # a waiting Snatch user takes it (fightsim.snatched)
            return
        if targets is not None:
            # A double battle's status move aimed at both foes, or at every
            # other Pokemon (Growl, Sweet Scent, Teeter Dance): it runs on
            # each in turn, each through its own checks, as the engine's
            # BattleControllerPlayer_LoopSpreadMoves sends the move back
            # through BATTLE_CONTROL_BEFORE_MOVE for each.
            for t in targets:
                status_move(b, att, mv, t, t not in b.moved)
            return
        status_move(b, att, mv, dfn, first)
        return
    if targets is not None:
        _spread_attack(b, att, mv, targets, paid)
        return
    before = dfn.hp
    if att.ability == "Analytic" and fs.moves_last(b, first):
        # Its foe has acted this turn or switched in, every other Pokemon's
        # action done (Battler_MovedThisTurn): 13/10 power (fightsim.ability_power).
        b.analytic = att
        try:
            attack(b, att, mv, dfn, first)
        finally:
            b.analytic = None
    else:
        attack(b, att, mv, dfn, first)
    # A contact ability's chance hurts the player when the player's Pokemon
    # takes it, and helps it when the trainer's does (fightsim.hit_aftermath:
    # a move of several hits has had it hit by hit).
    fs.hit_aftermath(b, att, dfn, mv,
                     lambda kind, p, victim: b.dice.bad(kind, p) if player(victim) else b.dice.good(p, kind),
                     lambda kind, n: b.dice.choice(kind, n))
    if b.blown is att:
        fs.mind_blown_cost(b, att)       # half its HP as the move ends, hit or miss (fightsim.mind_blown_cost)
    fs.destiny_bond(att, dfn)
    if dfn.grudge:
        fs.grudge(att, dfn, paid, mv)        # the knockout's move loses its PP (fightsim.grudge)
    fs.knockout_boost(att, dfn, before)      # Moxie and Beast Boost
    if mv.const == "MOVE_RELIC_SONG":
        fs.relic_song(b, att, mv, b.last_dealt > 0)     # Meloetta's form (fightsim.relic_song)


def _spread_attack(b, att, mv, targets, paid):
    """A damaging move in a double battle (fightsim.run_doubles), on each
    Pokemon it hits in turn, as fightsim._use_move's own loop ran it until
    2026-10-21: a move that hits more than one is at three quarters on each
    (Battle.spread, read by damage_of); each target's hit and its contact
    ability's answer, then Mind Blown's cost once, then each target's
    Destiny Bond, Grudge and Moxie, and Relic Song's form once a use.
    `first` for each is whether that target has yet to act this turn.
    Magnitude's power is rolled once for the whole use (BtlCmd_CalcMagnitudePower
    keeps battleCtx->magnitude until the move ends), held in
    Battle.spread_magnitude meanwhile."""
    b.spread = len(targets) > 1
    before = {id(t): t.hp for t in targets}
    try:
        for t in targets:
            attack(b, att, mv, t, t not in b.moved)
            fs.hit_aftermath(b, att, t, mv,
                             lambda kind, p, victim: b.dice.bad(kind, p) if player(victim) else b.dice.good(p, kind),
                             lambda kind, n: b.dice.choice(kind, n))
    finally:
        b.spread = False
        b.spread_magnitude = None
    if b.blown is att:
        fs.mind_blown_cost(b, att)       # once, after every target (fightsim.mind_blown_cost)
    for t in targets:
        fs.destiny_bond(att, t)
        if t.grudge:
            fs.grudge(att, t, paid, mv)
        fs.knockout_boost(att, t, before[id(t)])
    if mv.const == "MOVE_RELIC_SONG":
        fs.relic_song(b, att, mv, any(t.hp < before[id(t)] for t in targets))    # once a use, whatever it hit


def struggle_damage(att, dfn, roll, room=False):
    """Struggle: 50 power, physical, typeless, no modifiers, at the roll;
    under Wonder Room (`room`) it meets the target's Sp. Def with its
    Defense stages (fightsim.room_mult)."""
    a = att.stats.get("atk", 50) * fs.stage_mult(att.stages["atk"])
    d = dfn.stats.get("spd" if room else "def", 50) * fs.stage_mult(dfn.stages["def"])
    base = ((2 * att.level // 5 + 2) * 50 * a / d) // 50 + 2
    return int(base * roll / 100)


def confusion_damage(mon, roll):
    """A self-hit: a 40-power typeless physical hit at the given roll."""
    a = mon.stats.get("atk", 50) * fs.stage_mult(mon.stages["atk"])
    d = mon.stats.get("def", 50) * fs.stage_mult(mon.stages["def"])
    base = ((2 * mon.level // 5 + 2) * 40 * a / d) // 50 + 2
    return int(base * roll / 100)


def rolled_hits(b, att, dfn, mv, trainer, first=True):
    """The hits this use makes: a two to five hit move's count
    (fs.multi_hit_odds), rolled by a run's dice and enumerated at its odds by
    the planner's; a rising move's hits (Fury Cutter, Triple Kick, Triple
    Axel) until its first miss, each later hit checking accuracy again unless
    a Loaded Dice skips the check, and skipping the hit overrides, so No
    Guard and Lock-On land only the first (fightsim.RISING); Population
    Bomb's up to ten the same way (fightsim.TEN_HITS); two for the two-hit
    moves and three for
    the three-hit ones (fightsim.THREE_HITS). In the strict
    search the trainer gets its most hits and the player its fewest."""
    odds = fs.multi_hit_odds(att, mv)
    if odds:
        counts, weights = [h for h, _w in odds], [w for _h, w in odds]
        if len(counts) == 1:
            return counts[0]
        pick = getattr(b.dice, "pick_weighted", None)
        if pick is None:
            return max(counts) if trainer else min(counts)
        return pick(counts, weights)
    if mv.effect in fs.RISING:
        hits = 1
        while hits < fs.RISING_COUNT and (att.item == "Loaded Dice"
                                          or accuracy_hits(b, att, dfn, mv, first, later=True)):
            hits += 1
        return hits
    if mv.effect == fs.TEN_HITS:
        # Population Bomb's ten, until the first miss of a later check that
        # skips the hit overrides (fightsim.TEN_HITS); a Loaded Dice's are
        # its odds above.
        hits = 1
        while hits < 10 and accuracy_hits(b, att, dfn, mv, first, later=True):
            hits += 1
        return hits
    return 2 if mv.effect in fs.TWO_HITS else 3 if mv.effect in fs.THREE_HITS else 1


def crit_hits(b, att, dfn, mv, hits, trainer):
    """Each hit's critical hit for a move of several hits, as the engine's
    CalcCrit runs once a hit (fightsim.crit_rate). Dice that enumerate a
    turn (the planner's, crit_count) take the number of critical hits at its
    binomial odds as one event, the first that many hits landing critical,
    so a turn splits n + 1 ways rather than 2 to the n; any other dice roll
    every hit, the stress test's doubled check included."""
    rate = fs.crit_rate(b, att, dfn, mv)
    if rate <= 0:
        return [False] * hits
    count = getattr(b.dice, "crit_count", None)
    if count is not None:
        k = count(hits, rate)
        return [i < k for i in range(hits)]
    return [b.dice.bad("crit", rate) if trainer else b.dice.good(rate, "crit") for _ in range(hits)]


def multi_hit(b, att, mv, dfn, first, hits, trainer):
    """A move of several hits landed hit by hit (fightsim.land_hits) on the
    battle's dice: each hit's critical hit (crit_hits), and its damage roll,
    each hit's own in a run, as the engine rolls one a hit, but one shared by
    every hit when the dice enumerate a turn (the planner's), whose rolls are
    grouped by the whole move's damage. None when the move has no row or
    deals nothing (the single-hit zero branch's work done); else the HP
    taken from dfn."""
    rolls = b.rolls(att, dfn, mv)
    if not rolls:
        return None
    if rolls[-1] <= 0:
        if dfn.ability in fs.ZEROING and fs.effectiveness(b.st["chart"], mv.type, dfn.types) > 0:
            fs.reveal(dfn)
            if dfn.ability == "Flash Fire" and mv.type == "Fire":
                dfn.flash_fire = True
            fs.absorb(b, att, dfn, mv)
        return None
    crits = crit_hits(b, att, dfn, mv, hits, trainer)
    weights, whole = fs.hit_weights(att, mv, hits)
    reckless = fs.reckless_fix(att, mv)

    def one(i, crit, roll):
        d = damage_of(b, att, dfn, mv, crit, top=trainer, roll=roll, share=(weights[i], whole)) or 0
        return d if reckless == 1.0 else int(d * reckless)

    shared = None
    if b.dice.mode == "run":
        grouped = getattr(b.dice, "roll_grouped", None)
        if grouped:
            # The whole move's damage at a roll, for grouping alone: a resist
            # berry held now halves the first hit only.
            berry = fs.resist_berry(b, dfn, mv)
            held = fs.berry_works(b, dfn, berry)
            shared = grouped(lambda r: sum(one(i, crits[i], r) * (2 if held and i else 1) for i in range(hits)),
                             dfn.hp)

    def hit_damage(i, crit):
        roll = None
        if b.dice.mode == "run":
            roll = shared if shared is not None else b.dice.roll(trainer)
        return one(i, crit, roll)

    b.hits_landed = True
    dealt = fs.land_hits(b, att, dfn, mv, first, hits, hit_damage, crits,
                         lambda kind, p, victim: b.dice.bad(kind, p) if player(victim) else b.dice.good(p, kind),
                         lambda kind, n: b.dice.choice(kind, n))
    b.last_dealt = dealt
    return dealt


def beat_up(b, att, mv, dfn, first, trainer):
    """Beat Up's hits (fightsim.beat_up_hits) on the battle's dice: each
    hit's critical hit as crit_hits rolls them, and its damage roll, each
    hit's own in a run but one shared by every hit when the dice enumerate
    a turn (the planner's), grouped by the whole move's damage; the
    trainer's top roll and the player's lowest in the strict search."""
    shared = None
    if b.dice.mode == "run":
        grouped = getattr(b.dice, "roll_grouped", None)
        if grouped:
            members = fs.beat_up_party(b, att)
            shared = grouped(lambda r: sum(fs.beat_up_damage(b, att, m, dfn, mv, False, r) for m in members), dfn.hp)

    def roll_of(i, crit):
        if b.dice.mode != "run":
            return 15 if trainer else 0
        return shared if shared is not None else b.dice.roll(trainer)

    return fs.beat_up_hits(b, att, mv, dfn, first, lambda n, rate: crit_hits(b, att, dfn, mv, n, trainer), roll_of,
                           lambda kind, p, victim: b.dice.bad(kind, p) if player(victim) else b.dice.good(p, kind),
                           lambda kind, n: b.dice.choice(kind, n))


def crash(b, att, dfn, mv):
    """A Jump Kick, High Jump Kick or Supercell Slam that failed to hit, on
    an accuracy miss, a Protect or a target in the air: its user loses half
    the damage the hit would have done, at most half the target's maximum
    HP (fightsim.crash_loss). The hit's critical hit and damage roll come
    from the battle's dice the other way about from a hit's: a crit or a
    high roll is bad luck for the player when its own Pokemon crashes, and
    good luck when the trainer's does."""
    if mv.effect not in fs.CRASH or att.ability == "Magic Guard":
        return                   # Jump Kick's kind and Axe Kick (fightsim.CRASH)
    mine = player(att)
    rate = fs.crit_rate(b, att, dfn, mv)
    crit = rate > 0 and (b.dice.bad("crit", rate) if mine else b.dice.good(rate, "crit"))
    roll = None
    if b.dice.mode == "run":
        grouped = getattr(b.dice, "roll_grouped", None)
        roll = grouped(lambda r: fs.crash_loss(att, dfn, damage_of(b, att, dfn, mv, crit, top=mine, roll=r) or 0),
                       att.hp) if grouped else b.dice.roll(not mine)
    fs.hurt(b, att, fs.crash_loss(att, dfn, damage_of(b, att, dfn, mv, crit, top=mine, roll=roll) or 0))


def attack(b, att, mv, dfn, first):
    b.last_dealt = 0                     # the HP this move took, for the contact abilities
    b.hits_landed = False                # a move of several hits that land_hits landed
    b.sub_hit = False                    # a Substitute it has hit (fightsim.Battle.sub_hit)
    if mv.effect == "BIDE" and not fs.bide_releases(att, mv):
        return                           # Bide starts, stores, or has nothing to give back (fightsim.bide_releases)
    if not dfn.alive():
        fs.rollout_break(att, mv)        # no target: a Rollout run ends (fightsim.rollout_break)
        return
    if fs.loses_type_fails(att, mv):
        return                           # Burn Up or Double Shock without its type (fightsim.lose_type)
    if fs.dream_eater_fails(att, dfn, mv) or fs.lost_focus(att, mv) or (mv.effect == "DAMAGE_WHILE_ASLEEP"
                                                                       and fs.snore_fails(att, mv)):
        return                           # Dream Eater awake or behind a Substitute; Focus Punch once hit; Snore awake
    if mv.effect in fs.FAILS_BEFORE and fs.fails_before(att, dfn, mv):
        return                           # Poltergeist, Belch and First Impression's own failures (fightsim.fails_before)
    spit = fs.spit_up_key(att) if mv.effect == "SPIT_UP" else None
    if mv.effect == "SPIT_UP" and spit is None:
        return                           # Spit Up with nothing stored (fightsim.spit_up_key)
    if att is not dfn and att.side == dfn.side and dfn.ability == "Telepathy" and mv.power and not fs.mold(att, dfn):
        fs.reveal(dfn)
        return                           # a partner's damaging move into Telepathy (fightsim.attack), a double battle's
    if mv.effect == "MIND_BLOWN" and not fs.mind_blown(b, att):
        return                           # a Damp Pokemon stops it, and nothing is paid (fightsim.mind_blown)
    if mv.effect in fs.SELF_KO and not fs.explode_first(b, att):
        return
    if mv.effect == fs.FUTURE_SIGHT:
        # Future Sight and Doom Desire (fightsim.foresee): the damage is
        # worked out now, with no critical hit, its roll made now by the
        # battle's dice, and lands at the turn's end two turns on.
        top = not player(att)
        roll = None
        if b.dice.mode == "run":
            grouped = getattr(b.dice, "roll_grouped", None)
            roll = grouped(lambda r: damage_of(b, att, dfn, mv, False, top, roll=r) or 0, dfn.hp) \
                if grouped else b.dice.roll(top)
        dmg = damage_of(b, att, dfn, mv, False, top, roll=roll)
        if dmg is not None:
            fs.foresee(b, att, mv, dfn, dmg)
        return
    if dfn.charging is not None and dfn.charging.effect in fs.INVULNERABLE and not fs.reaches(mv, dfn) \
            and not fs.lands_sure(att, dfn, mv):
        crash(b, att, dfn, mv)
        fs.rollout_break(att, mv)
        return                   # No Guard reaches it there (fightsim.no_guard)
    if fs.protected(b, att, mv, dfn):
        crash(b, att, dfn, mv)
        fs.rollout_break(att, mv)
        return                   # only a move Protect can stop (fightsim.protected)
    if mv.effect == "REMOVE_PROTECT" and not dfn.protecting:
        return                   # Feint and Hyperspace Hole fail on a target not protecting (BtlCmd_TryFeint)
    if fs.lifted(dfn, mv):
        return
    if mv.effect == "HIT_FIRST_IF_TARGET_ATTACKING":
        nxt = getattr(dfn, "chosen", None)
        if not first or nxt is None or nxt.cat == "Status":
            return
    if fs.move_fails_first(att, mv, dfn, first):       # Upper Hand and Shell Trap
        return
    if mv.effect == "ALWAYS_FLINCH_FIRST_TURN_ONLY" and att.turns_in > 0:
        return
    # Natural Gift and Fling spend the held item, and fail without one;
    # fightsim keeps the item and fires them every turn.
    gift = None
    if mv.name in ("Natural Gift", "Fling"):
        if not att.item or (mv.name == "Natural Gift" and "Berry" not in att.item):
            return
        if mv.name == "Fling" and not fs.item_fling(att.item)[0]:
            return                       # an item with no fling power cannot be thrown (TryFling)
        gift = att.item
        fs.consume(att, eaten=False)     # spent, not eaten (Belch)
        fs.mark_unheld(b, att)           # a trainer's flung item gone from its rows (fightsim.mark_unheld)
    if gift is not None and mv.name == "Fling":
        b.flung = gift                   # its effect after the hit (fightsim.fling_effect)
    if not accuracy_hits(b, att, dfn, mv, first):
        crash(b, att, dfn, mv)               # Magic Guard spares it (fightsim.crash_loss)
        fs.rollout_after(att, mv, False)
        return
    if mv.effect == "POLLEN_PUFF" and dfn.side == att.side and dfn is not att:
        fs.pollen_puff_heal(dfn)             # on its user's ally, a heal in place of the hit (fightsim.pollen_puff_heal)
        return
    if dfn.ability == "Queenly Majesty" and fs.majesty_blocked(att, dfn, mv):
        return                               # a raised move into Queenly Majesty (fightsim.majesty_blocked)
    fs.rollout_after(att, mv, True)
    trainer = not player(att)
    if mv.effect == "BEAT_UP":
        dealt = beat_up(b, att, mv, dfn, first, trainer)
        _after_attack(b, att, mv, dfn, first, dealt, trainer, hit_by_hit=True)
        return
    hits = rolled_hits(b, att, dfn, mv, trainer, first)
    if mv.effect in fs.HIT_BY_HIT:
        dealt = multi_hit(b, att, mv, dfn, first, hits, trainer)
        if dealt is not None:
            _after_attack(b, att, mv, dfn, first, dealt, trainer, hit_by_hit=True)
        return
    present = fs.present_roll(b) if mv.effect == "RANDOM_POWER_MAYBE_HEAL" else None
    if present == 0:
        fs.present_heal(dfn)             # Present's gift instead of a hit (fightsim.present_heal)
        return
    # Fixed damage (fightsim.fixed_damage). Psywave's roll goes the
    # trainer's way in the search, as a damage roll does, and rolls in a run.
    tenths = 10
    if mv.effect == "RANDOM_DAMAGE_1_TO_150_LEVEL":
        tenths = b.dice.rng.randint(5, 15) if b.dice.mode == "run" else (15 if trainer else 5)
    dmg = fs.fixed_damage(b, att, dfn, mv, tenths)
    if mv.effect == "ONE_HIT_KO":
        if fs.ohko_blocked(b, att, dfn, mv):
            return
        p_ohko = (30 + att.level - dfn.level) / 100
        if not (b.dice.bad("ohko", p_ohko) if trainer else b.dice.good(p_ohko)):
            return
        dmg = dfn.hp
    elif mv.effect in ("COUNTER", "MIRROR_COAT", "METAL_BURST"):
        hit = att.hit_this_turn
        want = {"COUNTER": "Physical", "MIRROR_COAT": "Special"}.get(mv.effect)
        if not hit or (want and hit[0] != want) or fs.effectiveness(b.st["chart"], mv.type, fs.chart_types(dfn, mv)) == 0:
            return
        dmg = int(hit[1] * (1.5 if mv.effect == "METAL_BURST" else 2))
    elif mv.effect == "STRUGGLE":
        # Struggle skips the type chart and every modifier (battle_lib.c
        # returns early for MOVE_STRUGGLE): a 50-power physical hit on stats
        # and stages, at the roll.
        roll = 85 + (b.dice.roll(trainer) if b.dice.mode == "run" else (15 if trainer else 0))
        dmg = struggle_damage(att, dfn, roll, b.wonder_room)
    crit = False
    if dmg is None:
        # The first battle (Barry on Route 201) has no critical hits on either
        # side: BtlCmd_CalcCrit sets the multiplier to 1 under
        # BATTLE_STATUS_FIRST_BATTLE (src/battle/battle_script.c).
        if not fs.crit_proof(att, dfn, b) and not b.st.get("first_battle"):     # the armour, unless Mold Breaker; Lucky Chant
            stage = att.crit_stage + (att.ability == "Super Luck") + (1 if mv.effect.startswith("HIGH_CRITICAL") or
                                      mv.effect.startswith("CHARGE_TURN_HIGH_CRIT") else 0)
            if att.item in ("Scope Lens", "Razor Claw"):
                stage += 1
            rate = CRIT_RATE[min(stage, 4)]
            if mv.sure or fs.merciless(att, dfn) or fs.focused(att):
                crit = True          # Frost Breath's kind, Merciless on poison and Laser Focus, forced (fightsim.sure_crit)
            else:
                crit = b.dice.bad("crit", rate) if trainer else b.dice.good(rate, "crit")
        key = att.key
        if mv.name == "Magnitude":
            # The power is rolled first, at the game's odds for either side
            # in a run (the player's own luck, question 1 of design.md), and
            # its row is that power's (fightsim.prepare adds them).
            powers = list(fs.MAGNITUDE_POWERS)
            weights = [fs.MAGNITUDE_POWERS[p] for p in powers]
            rng = getattr(b, "rng", None)
            pick = getattr(b.dice, "pick_weighted", None)
            p = b.spread_magnitude
            if p is None:
                p = pick(powers, weights) if pick else (rng.choices(powers, weights)[0] if rng is not None else 70)
                if b.doubles:
                    b.spread_magnitude = p   # one roll for every target of the use (_spread_attack)
            att.key = f"{key}#m{p}"
            b.last_magnitude = p
        if present is not None:
            att.key = f"{key}#pr{present}"   # Present's row at its rolled power (fightsim.present_roll)
        if spit is not None:
            att.key = spit                   # Spit Up's row for the power it spends
        elif mv.name == "Natural Gift" and player(att):
            att.key = fs.natural_gift_key(key, gift)     # the player's, rowed with its Berry
        elif mv.name == "Fling" and player(att):
            att.key = fs.fling_key(key, gift)            # the player's, rowed at its item's fling power
        try:
            roll = None
            if spit is not None:
                roll = 15                    # CalcMaxDamage: Spit Up's top roll, no variance
            elif b.dice.mode == "run":
                # Dice that enumerate a turn's outcomes (plplan) take the
                # damage of every roll, so rolls that land alike count as one.
                grouped = getattr(b.dice, "roll_grouped", None)
                roll = grouped(lambda r: fs.berry_first_hit(b, dfn, mv, fs.use_damage(
                    att, mv, damage_of(b, att, dfn, mv, crit, top=trainer, roll=r) or 0, hits), hits), dfn.hp) \
                    if grouped else b.dice.roll(trainer)
            dmg = damage_of(b, att, dfn, mv, crit, top=trainer, roll=roll)
        finally:
            att.key = key
        if dmg is None:
            return
        dmg = fs.use_damage(att, mv, dmg, hits)
        # A resist berry halves only the first hit (fightsim.berry_first_hit).
        dmg = fs.berry_first_hit(b, dfn, mv, dmg, hits)
        if mv.effect == "DOUBLE_POWER_IF_MOVING_SECOND" and not first:
            # Payback doubles once the target has acted (fs.state_mult has
            # taken the calculator's own doubling off its row).
            dmg = int(dmg * fs.doubled_power(att, mv))
        if mv.effect == "HIT_BEFORE_SWITCH" and getattr(att, "pursuing", False):
            dmg = int(dmg * fs.doubled_power(att, mv))     # BtlCmd_TryPursuit's POWER_MULTI 20
        if mv.effect == "DOUBLE_POWER_IF_FASTER" and fs.beak_doubles(b, dfn, first):
            dmg = int(dmg * fs.doubled_power(att, mv))     # Bolt Beak and Fishious Rend (fightsim.beak_doubles)
        if mv.effect == "FICKLE_BEAM" and fs.fickle_doubles(b):
            dmg = int(dmg * fs.doubled_power(att, mv))     # three times in ten (fightsim.fickle_doubles)
        # A doubled power meets Technician after it is doubled (fs.doubled_power).
        if mv.effect == "DOUBLE_POWER_WHEN_STATUSED" and att.status:
            dmg = int(dmg * fs.doubled_power(att, mv))
        if mv.effect == "DOUBLE_POWER_IF_HIT" and att.hit_this_turn:
            dmg = int(dmg * fs.doubled_power(att, mv))
        if mv.effect == "DOUBLE_POWER_WHEN_BELOW_HALF" and dfn.hp * 2 <= dfn.maxhp:
            dmg = int(dmg * fs.doubled_power(att, mv))
        if mv.effect == "DOUBLE_POWER_HEAL_SLEEP" and fs.slap_doubles(att, dfn, mv):
            dmg = int(dmg * fs.doubled_power(att, mv))     # Wake-Up Slap, no Substitute in the way
        if fs.doubled(att, dfn, mv):
            dmg = int(dmg * fs.doubled_power(att, mv))
    if dmg <= 0:
        fs.rollout_break(att, mv)    # an immunity ends a Rollout run (fightsim.rollout_break)
        if dfn.ability in fs.ZEROING and fs.effectiveness(b.st["chart"], mv.type, dfn.types) > 0:
            fs.reveal(dfn)           # an absorbing ability, Levitate or Wonder Guard took it
            if dfn.ability == "Flash Fire" and mv.type == "Fire":
                dfn.flash_fire = True
            fs.absorb(b, att, dfn, mv)   # and a heal or a stage for the ones that give one
        return
    if fs.sub_blocks(att, dfn, mv):
        dfn.sub = max(0, dfn.sub - dmg)
        dealt = 0
        b.sub_hit = True         # broken or not, nothing of the hit reaches the Pokemon behind it
        if mv.effect == "EAT_BERRY":
            # but Bug Bite and Pluck eat its Berry through the Substitute
            # (as fightsim.attack has it)
            fs.pluck(b, att, dfn, lambda kind, n: b.dice.choice(kind, n))
    else:
        if mv.effect == "LEAVE_WITH_1_HP" and dmg >= dfn.hp:
            dmg = dfn.hp - 1     # False Swipe and Hold Back leave 1 HP, before Sturdy and the Sash
        # Focus Sash and Sturdy hold one hit from full HP; a move of several
        # hits lands them one at a time (multi_hit) and never comes here.
        full = dfn.hp == dfn.maxhp and hits < 2
        sturdy = dfn.ability == "Sturdy" and att.ability != "Mold Breaker"
        if dmg >= dfn.hp and full and (dfn.item == "Focus Sash" or sturdy):
            if sturdy:
                fs.reveal(dfn)
            dmg = dfn.hp - 1
            if dfn.item == "Focus Sash" and not sturdy:
                fs.consume(dfn)
        if dmg >= dfn.hp and getattr(dfn, "enduring", False):
            dmg = dfn.hp - 1
        # The trainer's Focus Band is an item proc, in the budget (question 8).
        if dmg >= dfn.hp and dfn.item == "Focus Band" and \
                (b.dice.bad("focusband", 0.1) if not player(dfn) else b.dice.good(0.1, "focusband")):
            dmg = dfn.hp - 1
        dealt = min(dmg, dfn.hp)
        dfn.hp -= dealt
        b.last_dealt, b.hit_left = dealt, dfn.hp     # the HP before any Berry answers (fightsim.Battle.hit_left)
        if mv.effect == "INCINERATE" and dfn.alive():
            fs.incinerate(b, dfn, mv)    # its Berry burned before the target can eat it (fightsim.incinerate)
        elif mv.effect in fs.TAKES_FIRST and dealt > 0:
            # Knock Off's and Bug Bite's effect before the target's own Berry
            # can act (fightsim.take_first).
            fs.take_first(b, att, dfn, mv, lambda kind, n: b.dice.choice(kind, n))
        fs.berry_check(dfn, b)
        dfn.hit_this_turn = (mv.cat, dealt)
        if dfn.bide:
            fs.bide_store(dfn, dealt)        # a Bide user stores what it took (fightsim.bide_store)
        if dfn.status == "frz" and mv.type == "Fire":
            dfn.status = None
    if crit:
        fs.anger_point(dfn)              # the hit's first answer, a Substitute's too (fightsim.anger_point)
    _after_attack(b, att, mv, dfn, first, dealt, trainer)


def _after_attack(b, att, mv, dfn, first, dealt, trainer, hit_by_hit=False):
    """A damaging move's own effects once its hits have landed, dealt the
    HP they took from dfn: recoil, draining, the Life Orb and the added
    effects. A move of several hits (hit_by_hit) has rolled its King's
    Rock and its own added effect hit by hit already (fightsim.land_hits)."""
    e = mv.effect
    if e in fs.BREAKS_PROTECT:
        dfn.protecting = False   # subscript_feint: the hit ends the target's protection
    if e == "STRUGGLE" and att.ability != "Magic Guard":
        # subscript_struggle: the user loses a quarter of its maximum HP.
        fs.hurt(b, att, max(1, att.maxhp // 4))
    if e in fs.RECOIL and att.ability not in fs.RECOIL_PROOF:     # Rock Head and Magic Guard
        fs.hurt(b, att, max(1, int(dealt * fs.RECOIL[e])))
    if e in fs.ANY_HIT:
        fs.any_hit(b, att, dfn, mv)      # Chloroblast's cost, Freezy Frost's reset, screens, hazards (fightsim.any_hit)
    if e in fs.DRAIN:
        # Big Root raises what a draining move restores by 30%; Heal Block on
        # the user stops the heal, not the damage, and the target's Liquid
        # Ooze turns it into damage (fightsim.drain).
        gain = int(dealt * fs.DRAIN[e])
        fs.drain(b, att, dfn, int(gain * 1.3) if att.item == "Big Root" else gain)
    if e == "RECHARGE_AFTER":
        att.recharge = True
    if e in fs.SELF_KO or e == "FINAL_GAMBIT":
        att.hp = 0
    if e == "CONTINUE_AND_CONFUSE_SELF":
        if att.lock is None:
            att.lock = (mv, b.dice.outrage(att.side))
    if att.item == "Life Orb" and dealt and att.ability != "Magic Guard" and not fs.sheer_force_active(att, mv):
        fs.hurt(b, att, att.maxhp // 10)
    if e == "REMOVE_SCREENS":
        side = b.p if player(dfn) else b.b
        side.screens = dict.fromkeys(side.screens, 0)
        if side.aurora_veil:
            side.aurora_veil = 0         # Aurora Veil breaks with the screens (fightsim.aurora_veil)
    def secondary(kind, p):
        """A secondary effect at its chance: bad luck against the player,
        good luck for it."""
        return b.dice.bad(kind, p) if trainer else b.dice.good(p, kind)
    # Sheer Force strips the secondary effect of the effects the game lists
    # (fs.sheer_force_effects); a recoil stays, and the calculator's row
    # already carries its 1.3x.
    stripped = fs.sheer_force_strips(att, mv)
    if e in fs.HIT_SELF_STAGES and not (stripped and not fs.HIT_SELF_STAGES[e][1]):
        ch, certain = fs.HIT_SELF_STAGES[e]
        # Its chance, doubled for Serene Grace (fightsim.self_raise_chance).
        if certain or secondary("statup", min(100, fs.self_raise_chance(att, mv)) / 100):
            fs.change_stages(att, ch)
    if e in ("REMOVE_HAZARDS_AND_BINDING", "MORTAL_SPIN"):
        fs.spin(b, att, dfn, e)
    if e == "CURE_PARTY_STATUS_HIT":
        fs.sparkly_swirl(b, att)         # its party's status cured after any hit (fightsim.sparkly_swirl)
    if e in fs.LOSES_TYPE:
        fs.lose_type(att, fs.LOSES_TYPE[e])     # Burn Up and Double Shock, a Substitute's hit too (fightsim.lose_type)
    if e == "SWITCH_HIT":
        att.u_turn = True        # after a knockout and a Substitute's hit too (fightsim.attack)
    if e == "STEAL_HELD_ITEM" and dealt > 0:
        fs.steal_item(att, dfn)  # the player's Thief and Covet only (fightsim.steal_item)
        fs.mark_unheld(b, dfn)   # a trainer's stolen item gone from its rows (fightsim.mark_unheld)
    if e in fs.LATE_HIT:
        fs.late_hit(b, att, dfn, mv, stripped, dealt)     # Fell Stinger's knockout, Anchor Shot's trap (fightsim.late_hit)
    # A hit on a Substitute, the one that broke it included, gives the
    # Pokemon behind it nothing (fightsim._after_attack, b.sub_hit).
    if not dfn.alive() or b.sub_hit or fs.sub_blocks(att, dfn, mv):
        return
    if e == "PREVENT_ESCAPE_BOTH_HIT":
        fs.jaw_lock(att, dfn)    # Jaw Lock holds both, each by the other (fightsim.jaw_lock)
    if e == "LEECH_SEED_HIT":
        fs.sappy_seed(dfn)       # Sappy Seed seeds a target left standing (fightsim.sappy_seed)
    if e == "CLEAR_SMOG":
        fs.clear_smog(dfn)       # every stage of the target back to 0 (fightsim.clear_smog)
    if e == "DOUBLE_POWER_HEAL_SLEEP":
        fs.slap_wakes(dfn, mv)   # Wake-Up Slap's doubled hit wakes its target (fightsim.slap_wakes)
    if e == "DOUBLE_POWER_AND_CURE_PARALYSIS":
        fs.salts_cure(dfn, mv)   # Smelling Salts' doubled hit cures its target (fightsim.salts_cure)
    if e == "FLING" and b.flung:
        fs.fling_effect(b, att, dfn, mv, b.flung, first, lambda kind, n: b.dice.choice(kind, n))
    if e == "THROAT_CHOP":
        fs.throat_chop(att, dfn, stripped)     # its hold on the target's sound moves (fightsim.throat_chop)
    if e == "SMACK_DOWN":
        fs.smack_down(b, att, dfn)       # down until it leaves (fightsim.smack_down)
    if e == "SALT_CURE":
        dfn.salted = True        # as fightsim: salted once the hit lands, chance-free
    if e == "CORE_ENFORCER" and getattr(dfn, "acted_turn", None) == b.turn:
        fs.suppress(b, dfn)      # Core Enforcer on a target that has moved this turn (fightsim._after_attack)
    if e == "DECREASE_LAST_MOVE_PP_HIT" and dealt > 0:
        fs.spite(dfn, 3)         # Eerie Spell drains 3 PP after its hit, chance-free (fightsim._after_attack)
    chance = mv.chance or 0
    if (dfn.ability == "Shield Dust" and not fs.mold(att, dfn)) or stripped:
        chance = 0               # Shield Dust, unless Mold Breaker gets past it
    if att.ability == "Serene Grace":
        chance = min(100, chance * 2)
    # A secondary status lands at its chance (Ian, 2026-10-02); under the
    # old luck budget, and in the strict search, one on the player always
    # lands, and the player's own never does in the search.
    def status_lands(kind):
        return b.dice.lands_on_player(kind, chance / 100) if trainer else b.dice.good(chance / 100, kind)
    if e in fs.HIT_STATUS and chance and status_lands("status"):
        fs.give_status_by_move(b, att, dfn, mv, fs.HIT_STATUS[e])
    if e in fs.STATUS_PICK and chance and status_lands("status"):
        # Dire Claw's one status of three, drawn evenly (fightsim.STATUS_PICK)
        fs.give_status_by_move(b, att, dfn, mv, fs.STATUS_PICK[e][b.dice.choice("status pick", 3)])
    # Burning Jealousy burns only a target one of whose stats rose this turn.
    if e == "BURN_HIT_IF_STATS_ROSE" and getattr(dfn, "stat_raised", False) and chance and status_lands("status"):
        fs.give_status_by_move(b, att, dfn, mv, "brn")
    if e == "TRI_ATTACK" and chance and status_lands("status"):
        order = ("frz", "par", "brn")
        if b.dice.mode == "run":
            order = (order[b.dice.choice("tri", 3)],)
        for st in order:
            if fs.give_status_by_move(b, att, dfn, mv, st):
                break
    if e == "SECRET_POWER" and chance:
        # Its battle terrain's added effect (fightsim.secret_power_effect): a
        # stage down and a flinch are luck, a status lands as the others do.
        what = fs.secret_power_effect(b.st.get("terrain"))
        if isinstance(what, dict):
            if secondary("statdrop", chance / 100):
                fs.lower_stats(b, att, dfn, what)
        elif what == "flinch":
            if first and secondary("flinch", chance / 100):
                dfn.flinch = True
        elif status_lands("status"):
            fs.give_status_by_move(b, att, dfn, mv, what)
    # A flinch and a stat change are not status conditions: they are luck,
    # at the move's chance (design.md, question 10).
    if e in fs.FLINCH_HIT and first and chance and secondary("flinch", chance / 100):
        dfn.flinch = True
    if e == "ALWAYS_FLINCH_FIRST_TURN_ONLY" and first and not stripped:
        dfn.flinch = True
    # King's Rock and Razor Fang are item procs, in the budget (question 8);
    # Stench counts as one (fightsim.flinch_item).
    if first and fs.flinch_item(att) and not dfn.flinch and not hit_by_hit \
            and not fs.item_flinch_blocked(att, dfn) and secondary("kingsrock", 0.1):
        dfn.flinch = True
    if dfn.ability == "Inner Focus" and not fs.mold(att, dfn):
        dfn.flinch = False       # Inner Focus: it never flinches, unless Mold Breaker gets past it
    if e in fs.CONFUSE_HITS and chance \
            and not fs.confusion_blocked(b, att, dfn, hit=True) and status_lands("confusehit"):
        dfn.confused = b.dice.confusion(dfn.side)
        fs.confusion_berry(dfn, b)          # a Lum Berry cures it at once
    if e == "CHATTER" and fs.chatter_confuses(att, dfn, stripped) and not fs.confusion_blocked(b, att, dfn, hit=True) \
            and (b.dice.lands_on_player("confusehit", fs.CHATTER_ODDS) if trainer
                 else b.dice.good(fs.CHATTER_ODDS, "confusehit")):
        dfn.confused = b.dice.confusion(dfn.side)     # a Chatot's Chatter, 1 in 100 (fightsim.CHATTER_ODDS)
        fs.confusion_berry(dfn, b)
    if e in fs.HIT_FOE_STAGES and chance and secondary("statdrop", chance / 100):
        fs.lower_stats(b, att, dfn, fs.HIT_FOE_STAGES[e])     # Mirror Armor, the blockers, Defiant
    if e == "HIT_AND_PREVENT_HEALING" and not stripped:     # Psychic Noise; Shield Dust does not stop it
        fs.start_heal_block(att, dfn, mv)
    if e in ("BIND_HIT", "WHIRLPOOL") and not dfn.bound:
        # The count, 3 to 6 on the battle's dice and 6 with a Grip Claw, and
        # the binder, whose leaving ends it (fightsim.Mon.bound).
        dfn.bound, dfn.bound_by = 6 if att.item == "Grip Claw" else b.dice.bind(dfn.side), att.key


def status_move(b, att, mv, dfn, first):
    e = mv.effect
    if (dfn.magic_coat or dfn.ability == "Magic Bounce") and fs.bounces(b, att, mv, dfn):
        b.reflecting = True              # Magic Coat or Magic Bounce turns it back on its user (fightsim.bounces)
        try:
            status_move(b, dfn, mv, att, first)
        finally:
            b.reflecting = False
        return
    if e == "RESTORE_HP_EVERY_TURN":
        att.aqua_ring = True             # Aqua Ring (fightsim heals it at the turn's end)
        return
    if e == "GIVE_GROUND_IMMUNITY":
        fs.magnet_rise(att)              # Magnet Rise (fightsim counts it down at the turn's end)
        return
    if e == "KO_MON_THAT_DEFEATED_USER":
        att.destiny_bond = True          # Destiny Bond (fs.destiny_bond after each attack)
        return
    foe_side = b.p if player(dfn) else b.b
    own_side = b.p if player(att) else b.b
    targets_foe = mv.range not in ("USER", "USER_SIDE", "ALLY", "FIELD", "USER_OR_ALLY")
    if e == "FAINT_AND_ATK_SP_ATK_DOWN_2" and not fs.memento_faints(att, dfn):
        return                           # Memento faints its user before its checks, or with no target does nothing
    if targets_foe and dfn.alive():
        if fs.protected(b, att, mv, dfn):
            return
        if fs.status_out_of_reach(att, dfn, mv):
            return               # a target on its hidden turn of Fly and the like (fightsim.status_out_of_reach)
        # Only Thunder Wave among the status moves meets the type chart
        # (BattleControllerPlayer_CheckTypeChart): it fails on a Ground type,
        # while Hypnosis sleeps a Dark type and Will-O-Wisp burns a Normal one.
        if mv.name == "Thunder Wave" and fs.effectiveness(b.st["chart"], mv.type, dfn.types) == 0:
            return
        # Grass types and Overcoat are immune to powder and spore moves.
        if fs.powder_immune(dfn, mv, att):
            return
        if not accuracy_hits(b, att, dfn, mv, first):
            return
        if fs.absorb(b, att, dfn, mv):
            return               # a status move of the ability's type is taken whole (fightsim.absorb)
        if fs.soundproofed(att, dfn, mv):
            return               # Sing, Growl or Roar into Soundproof (fightsim.soundproofed)
        if dfn.ability == "Queenly Majesty" and fs.majesty_blocked(att, dfn, mv):
            return               # a raised move into Queenly Majesty (fightsim.majesty_blocked)
        if att.ability == "Prankster" and fs.prankster_blocked(att, dfn, mv):
            return               # a raised status move into a Dark type (fightsim.prankster_blocked)
    if e in fs.STATUS_OF:
        if fs.sub_blocks(att, dfn, mv):
            return
        fs.give_status_by_move(b, att, dfn, mv, fs.STATUS_OF[e])
    elif e in ("STATUS_CONFUSE", "CONFUSE_ALL"):
        # Teeter Dance's one target in a single battle is the foe (fightsim.teeter_dance_others).
        if not fs.sub_blocks(att, dfn, mv) and not fs.confusion_blocked(b, att, dfn):
            dfn.confused = b.dice.confusion(dfn.side)
            fs.confusion_berry(dfn, b)
    elif e in ("ATK_UP_2_STATUS_CONFUSION", "SP_ATK_UP_CAUSE_CONFUSION"):
        if not fs.sub_blocks(att, dfn, mv):
            fs.change_stages(dfn, {"atk": 2} if e.startswith("ATK") else {"spa": 1})
            if not fs.confusion_blocked(b, att, dfn):
                dfn.confused = b.dice.confusion(dfn.side)
                fs.confusion_berry(dfn, b)
    elif e == "STATUS_SLEEP_NEXT_TURN":
        if not dfn.status and not dfn.yawn and not fs.sub_blocks(att, dfn, mv):
            dfn.yawn = 2
    elif e == "PREVENT_ESCAPE":
        if dfn.trapped_by is None and not fs.sub_blocks(att, dfn, mv):
            dfn.trapped_by = att.key
    elif e == "GROUND_TRAP_USER_CONTINUOUS_HEAL":
        # Rooted, and so held to the ground: under the rare flag, its rows
        # meet Ground moves on its twin without Flying or Levitate
        # (fightsim.grounded, Battle.row).
        att.ingrained = att.rare = True
    elif e == "STATUS_LEECH_SEED":
        if "Grass" not in dfn.types and not fs.sub_blocks(att, dfn, mv):
            dfn.seeded = True
    elif e == "PREVENT_HEALING":                             # Heal Block
        fs.start_heal_block(att, dfn, mv)
    elif e == "STOCKPILE":
        fs.stockpile(att)                # its count, up to three (fightsim.stockpile)
    elif e in fs.SELF_STAGES:
        if e == "TAKE_HEART":
            fs.take_heart(att)           # the two stages, then its status cured (fightsim.take_heart)
        else:
            fs.change_stages(att, fs.SELF_STAGES[e])
        if e == "DEF_UP_DOUBLE_ROLLOUT_POWER":
            att.curled = True
        if e == "EVA_UP_2_MINIMIZE":
            att.minimized = att.rare = True     # Minimize's mark, which Stomp doubles on (fightsim.doubled)
        if e == "SP_DEF_UP_DOUBLE_ELECTRIC_POWER":
            att.charged, att.rare = 2, True     # Charge, two turn ends (fightsim.state_mult doubles its Electric moves)
    elif e == "SP_ATK_DOWN_2_OPPOSITE_GENDER":
        if fs.captivates(att, dfn) and not fs.sub_blocks(att, dfn, mv):
            fs.lower_stats(b, att, dfn, fs.FOE_STAGES[e])     # Captivate, only across the genders (fightsim.captivates)
    elif e in fs.FOE_STAGES:
        if not fs.sub_blocks(att, dfn, mv):
            fs.lower_stats(b, att, dfn, fs.FOE_STAGES[e])     # stat by stat (fightsim.lower_stats)
    elif e == "SPICY_EXTRACT":
        fs.spicy_extract(b, att, dfn, mv)    # Attack up two, then Defense down two (fightsim.spicy_extract)
    elif e == "VENOM_DRENCH":
        if dfn.status in ("psn", "tox") and not fs.sub_blocks(att, dfn, mv):
            fs.lower_stats(b, att, dfn, fs.VENOM_DRENCH_STAGES)     # a poisoned target's three stats
    elif e == "PARTING_SHOT":
        fs.parting_shot(b, att, dfn, mv)     # both drops, then out as after U-turn (fightsim.parting_shot)
    elif e == "FAINT_AND_FULL_HEAL_NEXT_MON":
        fs.healing_wish(b, att)          # its user faints; the turn heals the one sent in (fightsim.wish_comes_true)
    elif e == "FAINT_FULL_RESTORE_NEXT_MON":
        fs.healing_wish(b, att, lunar=True)     # Lunar Dance: as Healing Wish, the PP restored too
    elif e == "GUARD_SPLIT":
        fs.share_stats(b, att, dfn, mv, ("def", "spd"))     # the two Defenses averaged (fightsim.share_stats)
    elif e == "POWER_SPLIT":
        fs.share_stats(b, att, dfn, mv, ("atk", "spa"))     # the two Attacks averaged (fightsim.share_stats)
    elif e == "PREVENT_ITEM_USE":
        fs.embargo(b, att, dfn, mv)      # five turns with its item held back (fightsim.embargo)
    elif e == "MAGIC_ROOM":
        fs.magic_room(b)                 # five turns with every item held back (fightsim.magic_room)
    elif e == "WONDER_ROOM":
        fs.wonder_room(b)                # five turns with the Defenses traded (fightsim.wonder_room)
    elif e == "CURSE":
        if "Ghost" in att.types:
            fs.ghost_curse(b, att, dfn, mv)      # it fails, at no cost, through a Substitute or on a cursed target
        else:
            fs.change_stages(att, {"atk": 1, "def": 1, "spe": -1})
    elif e == "MAX_ATK_LOSE_HALF_MAX_HP":
        # subscript_belly_drum fails, at no cost, with Attack at +6 already or
        # half its HP or less; else half its HP goes and Attack is set at +6
        # directly. Until 2026-10-20 a Belly Drum at +6 still cost half its
        # HP (Ian approved the fix on 2026-10-20).
        if att.stages["atk"] < 6 and att.hp > att.maxhp // 2:
            fs.hurt(b, att, att.maxhp // 2)
            att.stages["atk"] = 6
    elif e == "RAISE_ALL_STATS_LOSE_THIRD_MAX_HP":
        fs.clangorous_soul(b, att)       # a third of its HP for all five stats (fightsim.clangorous_soul)
    elif e == "ATK_SP_ATK_SPEED_UP_2_LOSE_HALF_MAX_HP":
        fs.fillet_away(b, att)           # half its HP for Attack, Sp. Atk and Speed (fightsim.fillet_away)
    elif e == "AUTOTOMIZE":
        fs.autotomize(att)               # two stages of Speed and 100 kg lighter (fightsim.autotomize)
    elif e == "LASER_FOCUS":
        fs.laser_focus(att)              # its next turn's hits critical (fightsim.laser_focus)
    elif e == "LUNAR_BLESSING":
        fs.lunar_blessing(b, att)        # a quarter back and its status cured (fightsim.lunar_blessing)
    elif e == "REMOVE_ALL_PP_ON_DEFEAT":
        att.grudge = att.rare = True     # Grudge, until its user next acts (fightsim.grudge)
    elif e == "OCTOLOCK":
        fs.octolock(att, dfn, mv)        # held, and a stage of each Defense at each turn's end (fightsim.octolock)
    elif e == "SET_AURORA_VEIL":
        fs.aurora_veil(b, att)           # five turns of both screens' halving, in hail (fightsim.aurora_veil)
    elif e == "TEATIME":
        fs.teatime(b, lambda kind, n: b.dice.choice(kind, n))     # every Berry on the field eaten (fightsim.teatime)
    elif e == "STEAL_STATUS_MOVE":
        fs.snatch(b, att, first)         # it waits to take the foe's next move Snatch may take (fightsim.snatched)
    elif e == "CRIT_UP_2":
        att.crit_stage = 2
    elif e in fs.HEAL_HALF:
        if e == "HEAL_HALF_REMOVE_FLYING_TYPE" and att.hp < att.maxhp:
            att.roosting = True          # Roost, as fightsim.status_move
        fs.heal(att, att.maxhp // 2)
    elif e == "HEAL_HALF_MORE_IN_SUN":
        fs.heal(att, fs.weather_heal(b, att, mv))     # Shore Up's sand, Cloud Nine (fightsim.weather_heal)
    elif e == "LIFE_DEW":
        fs.life_dew(att, b)              # a quarter back, rounded up, its ally's too, not under Heal Block (fightsim.life_dew)
    elif e == "STRENGTH_SAP":
        fs.strength_sap(b, att, dfn, mv)     # the target's Attack back as HP, then a stage off it (fightsim.strength_sap)
    elif e == "REST":
        # As fightsim's: Rest fails on the abilities that keep its user awake
        # (fightsim.rest_blocked), on a sleeping user, which is how a Sleep
        # Talk reaches it, and at full HP (subscript_rest).
        if not fs.rest_blocked(b, att) and att.hp < att.maxhp and att.status != "slp":
            att.hp, att.status, att.sleep, att.toxic = att.maxhp, "slp", 2, 0
            fs.cure_berry(att, b)       # a Chesto or Lum Berry wakes it at once
    elif e == "SWALLOW":
        fs.swallow(att)                  # by the stockpiles spent (fightsim.swallow)
    elif e == "SET_LIGHT_SCREEN":
        if not own_side.screens["Light Screen"]:
            own_side.screens["Light Screen"] = 8 if att.item == "Light Clay" else 5
    elif e == "SET_REFLECT":
        if not own_side.screens["Reflect"]:
            own_side.screens["Reflect"] = 8 if att.item == "Light Clay" else 5
    elif e in fs.WEATHER_OF:
        if not fs.weather_move_fails(b, e):          # Hail under a lasting hail (fightsim.weather_move_fails)
            rock = {"Sun": "Heat Rock", "Rain": "Damp Rock", "Sand": "Smooth Rock", "Hail": "Icy Rock"}
            b.weather = fs.WEATHER_OF[e]
            b.weather_turns = 8 if att.item == rock.get(b.weather) else 5
            if b.fog:
                b.fog = False                        # every weather flag cleared first, deep fog's too
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
    elif e == "STICKY_WEB":
        fs.lay_web(b, att)               # a web across the field (fightsim.lay_web, caught in fightsim.switch_in)
    elif e == "REMOVE_HAZARDS_SCREENS_EVA_DOWN":
        fs.defog(b, att, dfn, mv)        # evasion down, screens, hazards and fog cleared (fightsim.defog)
    elif e == "PROTECT_USER_SIDE":
        fs.side_guard(b, att, mv, first)     # Wide Guard and its kind guard the side this turn (fightsim.side_guard)
    elif e == "PROTECT" or e == "SURVIVE_WITH_1_HP":
        # BtlCmd_TryProtection: it fails when no battler acts after its user
        # (fightsim.moves_last). Otherwise a first one works, and a repeat at
        # fightsim.protect_odds, an eighth at worst: for the player its
        # failing is bad luck, for the trainer its working is.
        p_work = fs.protect_odds(att)
        if fs.moves_last(b, first):
            works = False
        elif att.protect_run == 0:
            works = True
        elif player(att):
            works = not b.dice.bad("protectfail", 1 - p_work)
        else:
            works = b.dice.bad("protectworks", p_work)
        if works:
            att.protecting = e == "PROTECT"
            att.enduring = e == "SURVIVE_WITH_1_HP"
            att.protect_run = min(att.protect_run + 1, fs.PROTECT_RUN_CAP)
        else:
            att.protect_run = 0
    elif e == "SET_SUBSTITUTE":
        if not att.sub and att.hp > att.maxhp // 4:
            fs.hurt(b, att, att.maxhp // 4)
            att.sub = att.maxhp // 4
    elif e == "RESET_STAT_CHANGES":
        fs.reset_all_stats(b)            # Haze: every stage on the field and Focus Energy (fightsim.reset_all_stats)
    elif e == "HEAL_STATUS":
        fs.refresh(att)                  # Refresh cures its user's own poison, burn or paralysis
    elif e == "SWAP_ATK_DEF":
        fs.power_trick(att)              # Attack and Defense swapped, its rows from its twin (fightsim.power_trick)
    elif e == "TRANSFER_STATUS":
        fs.psycho_shift(b, att, dfn, mv)     # Psycho Shift hands its user's status on (fightsim.psycho_shift)
    elif e == "SWAP_DEF_SP_DEF_STAT_CHANGES":
        fs.swap_stages(att, dfn, ("def", "spd"))      # Guard Swap (fightsim.swap_stages)
    elif e == "SWAP_ATK_SP_ATK_STAT_CHANGES":
        fs.swap_stages(att, dfn, ("atk", "spa"))      # Power Swap (fightsim.swap_stages)
    elif e == "SWAP_STAT_CHANGES":
        fs.heart_swap(att, dfn)          # every stage and Focus Energy exchanged (fightsim.heart_swap)
    elif e == "HEAL_TARGET":
        fs.heal_pulse(att, dfn, mv)      # half the target's HP back, the foe's in a single battle (fightsim.heal_pulse)
    elif e == "BOOST_ALLY_POWER_BY_50_PERCENT":
        fs.helping_hand(b, att)          # the partner's power by half this turn, a double battle's (fightsim.helping_hand)
    elif e == "MAKE_GLOBAL_TARGET":
        fs.follow_me(b, att, mv)         # Follow Me, Rage Powder, Spotlight: the center of attention (fightsim.follow_me)
    elif e == "AFTER_YOU":
        fs.after_you(b, att, dfn)        # its target acts next, in a double battle (fightsim.after_you)
    elif e == "COACHING":
        fs.coaching(b, att, dfn)         # its ally's Attack and Defense, in a double battle (fightsim.coaching)
    elif e == "HALVE_FIRE_DAMAGE":
        fs.water_sport(att)              # Fire moves at half power while it stands (fightsim.sport_half)
    elif e == "HALVE_ELECTRIC_DAMAGE":
        fs.mud_sport(att)                # Electric moves at half power while it stands (fightsim.sport_half)
    elif e == "APPLY_MAGIC_COAT":
        att.magic_coat = not fs.moves_last(b, first)  # this turn's coat, unless no battler acts after it
    elif e == "RANDOM_STAT_UP_2":
        fs.acupressure(att, lambda n: b.dice.choice("acupressure", n))     # two stages of a stat drawn evenly
    elif e == "CURE_PARTY_STATUS":
        fs.party_cure(b, att, mv)        # Heal Bell spares Soundproof, both end Nightmare (fightsim.party_cure)
    elif e == "PREVENT_STATUS":
        own_side.safeguard = 5
    elif e == "PREVENT_STAT_REDUCTION":
        fs.mist(own_side)                # Mist, five turns (fightsim.mist)
    elif e == "PREVENT_CRITS":
        fs.lucky_chant(own_side)         # Lucky Chant, five turns (fightsim.lucky_chant)
    elif e == "COPY_STAT_CHANGES":
        fs.psych_up(att, dfn)            # Psych Up takes the target's stages and Focus Energy
    elif e == "NEXT_ATTACK_ALWAYS_HITS":
        fs.lock_on(att, dfn)             # Lock-On and Mind Reader (fightsim.lock_on, read by fightsim.lands_sure)
    elif e == "FORESIGHT":
        fs.foresee_target(dfn)           # Foresight and Odor Sleuth (fightsim.foresee_target)
    elif e == "IGNORE_EVATION_REMOVE_DARK_IMMUNE":
        fs.miracle_eye(dfn)              # Miracle Eye (fightsim.miracle_eye)
    elif e == "GRAVITY":
        fs.gravity_start(b)              # five turns of Gravity (fightsim.gravity_start)
    elif e == "COPY_MOVE_FOR_BATTLE":
        fs.mimic(att, dfn)               # Mimic takes the target's last move (fightsim.mimic)
    elif e == "LEARN_MOVE_PERMANENT":
        fs.sketch(att, dfn, mv)          # Sketch takes the target's last move for good (fightsim.sketch)
    elif e == "TRANSFORM":
        fs.transform(b, att, dfn)        # a copy of the target but for its HP (fightsim.transform)
    elif e == "TAUNT":
        if not dfn.taunt and not fs.taunt_blocked(att, dfn):     # Oblivious, unless Mold Breaker
            dfn.taunt = b.dice.taunt(dfn.side)
    elif e == "TORMENT":
        dfn.tormented = True             # subscript_torment_start: fails if already tormented
    elif e == "DISABLE":
        # fightsim.disable, its 3 to 6 turns from the battle's dice; it fails
        # on a target in the air or underground (subscript_disable_start).
        if not (dfn.charging is not None and dfn.charging.effect in fs.INVULNERABLE):
            fs.disable(dfn, lambda: 3 + b.dice.choice("disable", 4))
    elif e == "STATUS_NIGHTMARE":
        fs.nightmare(att, dfn, mv)
    elif e == "ENCORE":
        fs.encore(dfn, lambda: 3 + b.dice.choice("encore", 5))     # fightsim.encore, 3 to 7 turns
    elif e == "INFATUATE":
        fs.infatuate(att, dfn, att.ability == "Mold Breaker")
    elif e == "HEAL_IN_3_TURNS":
        fs.wish(own_side)
    elif e == "DECREASE_LAST_MOVE_PP":
        fs.spite(dfn)
    elif e == "RECYCLE":
        fs.recycle(att)
    elif e == "AVERAGE_HP":
        fs.pain_split(b, att, dfn)
    elif e == "FORCE_SWITCH":
        if b.doubles:
            # A double battle's draw, from the target's own trainer's party
            # into the target's slot (fightsim.drag_pick). Until 2026-10-21
            # the one drawn took the first slot, whichever it hit (Ian
            # approved the fix on 2026-10-20).
            if dfn.alive() and not fs.anchored(att, dfn) and not getattr(dfn, "ingrained", False):
                idx = fs.drag_pick(b, dfn, lambda kind, n: b.dice.choice(kind, n))
                if idx is not None:
                    fs.switch_in(b, foe_side, idx, slot=fs.slot_of(foe_side, dfn))
            return
        bench = foe_side.bench()
        if bench and not fs.anchored(att, dfn) and not getattr(dfn, "ingrained", False):     # Suction Cups
            nxt = bench[b.dice.choice("roar", len(bench))]
            fs.switch_in(b, foe_side, foe_side.mons.index(nxt))
    elif e == "FAINT_AND_ATK_SP_ATK_DOWN_2":
        fs.memento_drops(b, att, dfn, mv)    # no drops through a Substitute, the blockers met (fightsim.memento_drops)
    elif e == "PASS_STATS_AND_STATUS":
        att.baton = True
    elif e == "SWITCH_HELD_ITEMS":
        fs.swap_items(att, dfn, mv)      # the player's Trick and Switcheroo only (fightsim.swap_items)
        fs.mark_unheld(b, att, dfn)      # a trainer's item swapped away from its rows (fightsim.mark_unheld)
    elif e == "MAKE_SHARED_MOVES_UNUSEABLE":
        fs.imprison(b, att)              # the foes' shared moves sealed while it stays (fightsim.imprison)
    elif e in fs.FORM_MOVES:
        # The status moves that change a type or an ability (fightsim.FORM_MOVES),
        # a choice among several on the battle's dice.
        fs.FORM_MOVES[e](b, att, mv, dfn, lambda kind, n: b.dice.choice(kind, n))
    elif e == "ALL_FAINT_3_TURNS":
        for m in (b.p.on_field() + b.b.on_field()):
            if m.alive() and not m.perish and (m.ability != "Soundproof" or fs.mold(att, m)):
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
    c.tailwind, c.safeguard, c.wish = s.tailwind, s.safeguard, getattr(s, "wish", 0)
    c.mist = getattr(s, "mist", 0)
    if s.lucky_chant:
        c.lucky_chant = s.lucky_chant    # left on the class while 0 (fightsim.Side)
    if s.aurora_veil:
        c.aurora_veil = s.aurora_veil    # Aurora Veil, left on the class while 0 (fightsim.Side)
    if s.web:
        c.web = s.web                    # Sticky Web, left on the class while 0 (fightsim.Side)
    if s.guard is not None:
        c.guard = s.guard                # this turn's side guard (fightsim.side_guard)
    c.hazards = dict(s.hazards)
    c.future, c.future_sight = s.future, s.future_sight        # a waiting Future Sight (tuples, shared safely)
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
    c.gas_flag = getattr(b, "gas_flag", False)       # a Neutralizing Gas noted on the field
    if b.gravity:
        c.gravity = b.gravity        # left on the class while 0 (fightsim.Battle)
    if b.last_move is not None:
        c.last_move = b.last_move    # Copycat's move (fightsim.note_move)
    if b.sporty:
        c.sporty = True              # a Water Sport user in the fight (fightsim.Battle.sporty)
    if b.guarded:
        c.guarded = True             # a side guard up this turn (fightsim.side_guard)
    if b.split:
        c.split = True               # stats averaged in this battle (fightsim.share_stats)
    if b.magic_room:
        c.magic_room = b.magic_room  # Magic Room's turns (fightsim.magic_room)
    if b.wonder_room:
        c.wonder_room = b.wonder_room    # Wonder Room's turns (fightsim.wonder_room)
    if b.snatching:
        c.snatching = True           # a Snatch waits this turn (fightsim.snatch)
    if b.unheld:
        c.unheld = True              # a Pokemon reads its item twin (fightsim.mark_unheld)
    if b.fog:
        c.fog = True                 # deep fog on the field (fightsim.fog_cut)
    if b.cloudy:
        c.cloudy = True              # a Cloud Nine or Air Lock holder in the fight (fightsim.weather_now)
    return c


def _name(x):
    return None if x is None else x.name


def _form(m):
    """A type or ability the battle changed (fightsim.set_types, set_ability,
    suppress, Forecast): its types, whether its ability is suppressed, and
    the ability its record holds. Empty while nothing has changed, so the
    keys of a fight without these changes stay as they were."""
    if not (getattr(m, "retyped", False) or getattr(m, "ability_was", None) is not None
            or getattr(m, "suppressed", False)):
        return ()
    return ("form", tuple(m.types), m.suppressed, fs.raw_ability(m))


def mon_key(m):
    key = (m.hp, m.status, m.sleep, m.toxic, tuple(m.stages.values()), m.confused, m.flinch,
           m.seeded, m.yawn, m.protect_run, m.sub, _name(m.charging), m.recharge,
           (m.lock[0].name, m.lock[1]) if m.lock else None, m.choice, m.taunt,
           None if m.last is None else m.last.cat, min(m.turns_in, 2), _name(m.last_hit_by),
           m.crit_stage, m.bound, m.cursed, m.perish, m.item or ("knocked off" if m.knocked_off else None),
           tuple(sorted(m.pp.items())),
           m.enduring, m.protecting, m.ability, m.magnet_rise, _name(m.last) if m.tormented else None,
           m.destiny_bond, m.infatuated, m.recycle, getattr(m, "heal_block", 0), getattr(m, "salted", False),
           getattr(m, "disabled", None), getattr(m, "disabled_turns", 0), getattr(m, "nightmare", False),
           getattr(m, "encore", None), getattr(m, "encore_turns", 0),
           getattr(m, "protean_type", None), getattr(m, "protean_used", False),
           # Last Resort works, and the AI rates it, by the moves used since it came in.
           getattr(m, "last_resort_count", 0) if getattr(m, "last_resort", False) else None)
    if m.stockpile:
        key += ("stockpile", m.stockpile, m.stockpile_def, m.stockpile_spd)
    if m.belch:
        key += ("ate", m.ate_berry)      # Belch fails until its user has eaten a Berry (fightsim.fails_before)
    if (m.ingrained or m.aqua_ring or m.trapped_by is not None or m.flash_fire or m.rollout or m.curled
            or m.raging or m.loafing):
        # The states batch 10 found the keys without (Ian approved adding
        # them on 2026-10-20): Ingrain's and Aqua Ring's heals, the Pokemon a
        # Block or Mean Look holds it for, a lit Flash Fire, Rollout's count,
        # Defense Curl's doubling, Rage's rise and a Truant's turn to loaf.
        # Kept out of the key while none is set, so a fight without them
        # keys as before; every key reads them here (side_key and
        # state_key, shape_key, ai_key and the planner's merge_key).
        key += ("held", m.ingrained, m.aqua_ring, m.trapped_by, m.flash_fire, m.rollout, m.curled, m.raging,
                m.loafing)
    if m.imprisoning or m.imprisoned:
        key += ("imprison", m.imprisoning, m.imprisoned, m.sealed)
    if m.rare:
        # The rarer states one of this stay's moves set (fightsim.Mon.rare).
        key += ("rare", m.throat_chop, m.minimized, m.charged, m.locked_on, m.lock_on_by, m.foresight, m.smacked, m.miracle_eye, m.water_sport, m.mud_sport, m.power_trick, m.bide, m.bide_damage,
                m.transform_key, tuple(sorted(m.split.items())) if m.split else None, m.embargo, m.roomed, m.item_off,
                m.grudge, m.octolocked, m.sky_holder, m.pirouette, m.lightened, m.laser_focus,
                tuple(x.name for x in m.moves) if m.mimicked is not None else None,
                None if m.mirror is None else m.mirror.name)
    return key + _form(m) if m.formed else key


def side_key(s):
    key = (s.active, tuple(mon_key(m) for m in s.mons), tuple(s.screens.values()), s.tailwind,
           tuple(s.hazards.values()), s.safeguard, getattr(s, "wish", 0), s.future, s.future_sight,
           getattr(s, "mist", 0))
    # Lucky Chant's turns and Sticky Web, kept out of the key while there
    # are none, so the keys of a fight without them stay as they were.
    if s.lucky_chant or s.web:
        key += (("lucky chant", s.lucky_chant, "web", s.web),)
    if s.aurora_veil:
        key += (("aurora veil", s.aurora_veil),)     # kept out of the key while there is none
    return key


def _field_extra(b):
    """The field's states most fights never have, kept out of the keys
    while they are not there: Gravity's turns, in a fight with Copycat
    the battle's last move, Magic Room's and Wonder Room's turns and deep
    fog (each checked by the keys before calling)."""
    out = (("gravity", b.gravity),) if b.gravity else ()
    if b.last_move is not None:
        out += (("last move", b.last_move.name),)
    if b.magic_room:
        out += (("magic room", b.magic_room),)
    if b.wonder_room:
        out += (("wonder room", b.wonder_room),)
    if b.fog:
        out += (("fog",),)
    return out


def state_key(b):
    key = (side_key(b.p), side_key(b.b), b.weather, b.weather_turns, b.trick_room,
           round(b.luck_spent, 6), getattr(b, "declined", frozenset()))
    rare = b.gravity or b.last_move is not None or b.magic_room or b.fog or b.wonder_room
    return key + _field_extra(b) if rare else key


def shape_key(b):
    """The state without its HP totals and luck: what `vector` leaves out."""
    def side(sd):
        key = (sd.active, tuple(mon_key(m)[1:] for m in sd.mons), tuple(sd.screens.values()),
               sd.tailwind, tuple(sd.hazards.values()), sd.safeguard, getattr(sd, "wish", 0),
               sd.future, sd.future_sight, getattr(sd, "mist", 0))
        if sd.lucky_chant or sd.web:
            key += (("lucky chant", sd.lucky_chant, "web", sd.web),)
        if sd.aurora_veil:
            key += (("aurora veil", sd.aurora_veil),)     # as side_key keeps it, since 2026-10-15
        return key
    key = (side(b.p), side(b.b), b.weather, b.weather_turns, b.trick_room, getattr(b, "declined", frozenset()))
    rare = b.gravity or b.last_move is not None or b.magic_room or b.fog or b.wonder_room
    return key + _field_extra(b) if rare else key


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

def _ai_mon(m):
    """What fightai reads of one Pokemon beyond mon_key: who it is, its last
    move by name (Mirror Move, Encore, Copycat and Baton Pass read the move),
    its turns in up to the four Roar reads, the moves the AI has seen it
    use, the ability a message has named, trapping and rooting, the type
    the last hit was recorded with, the Custap pinch, and for a Belch user
    whether it has eaten a Berry."""
    return (m.key, None if m.last is None else m.last.name, max(-1, min(m.turns_in, 4)),
            tuple(x.name for x in m.shown), m.revealed, m.trapped_by is not None, m.ingrained,
            m.last_hit_type, m.hp <= m.maxhp // 4, m.hp <= m.maxhp // 2, m.aqua_ring, m.flash_fire,
            getattr(m, "ate_berry", False) if getattr(m, "belch", False) else None)


def ai_key(b):
    """What the trainer's AI reads at a state: its own active Pokemon whole,
    the player's active one by every HP threshold the AI tests and by which
    of the trainer's moves would knock it out, the Pokemon on each side and
    the trainer's bench by HP and status, the field, the turn's Quick Claw
    roll, and whether it is the battle's first turn."""
    u, t = b.b.cur(), b.p.cur()
    kills = tuple((fightai.figure(b, u, t, m) or 0) >= t.hp for m in u.moves)
    tk = mon_key(t)
    tk = (_band(t.frac()), kills, t.hp == t.maxhp) + tk[1:] + _ai_mon(t)
    uk = mon_key(u)
    uk = (_band(u.frac()), u.hp == u.maxhp, u.hp >= u.maxhp // 2) + uk[1:] + _ai_mon(u)
    bench = tuple((m.key, m.alive(), m.hp == m.maxhp, m.status) for m in b.b.mons)
    quick = tuple(sorted((getattr(b, "quick", None) or {}).items()))
    return (uk, tk, bench, tuple((m.key, m.alive(), m.status) for m in b.p.mons),
            b.p.active, b.b.active, tuple(b.p.screens.values()), tuple(b.b.screens.values()),
            b.p.tailwind, b.b.tailwind, tuple(b.p.hazards.values()), tuple(b.b.hazards.values()),
            b.p.safeguard, b.b.safeguard, b.weather, b.trick_room > 0, b.turn == 0, b.ai_flags, quick,
            b.p.future_sight, b.b.future_sight, getattr(b.p, "mist", 0) > 0, getattr(b.b, "mist", 0) > 0) \
        + (_ai_field(b) if b.gravity or b.p.lucky_chant or b.b.lucky_chant or b.p.web or b.b.web or b.fog
           or b.p.aurora_veil or b.b.aurora_veil or b.wonder_room else ())


def _ai_field(b):
    """The field states the later batches add that the trainer's AI reads,
    kept out of its key while none is there: Lucky Chant on either side
    (Basic_CheckLuckyChant), Gravity (Basic_CheckGravity, the barred
    moves, the type check), Sticky Web on either side (Basic_CheckStickyWeb,
    Basic_CheckDefog, Expert_Defog, Expert_RapidSpin), deep fog
    (Basic_CheckDefog) and, since 2026-10-15, Aurora Veil on either side
    (Basic_CheckAuroraVeil, Expert_AuroraVeil, Expert_Defog), which batch 8
    gave the battle and this key had left out; and since 2026-10-20 Wonder
    Room, whose swap the AI's damage estimate reads (TrainerAI_CalcDamage
    passes the field's conditions)."""
    if not (b.p.lucky_chant or b.b.lucky_chant or b.gravity or b.p.web or b.b.web or b.fog
            or b.p.aurora_veil or b.b.aurora_veil or b.wonder_room):
        return ()
    return (("field", b.p.lucky_chant > 0, b.b.lucky_chant > 0, b.gravity > 0, b.p.web, b.b.web)
            + (("fog",) if b.fog else ())
            + (("aurora veil", b.p.aurora_veil > 0, b.b.aurora_veil > 0) if b.p.aurora_veil or b.b.aurora_veil
               else ())
            + (("wonder room",) if b.wonder_room else ()),)


_AI_CACHE = {}
_AI_CACHE_ST = None


def _band(frac):
    """Every HP threshold fightai reads, with both > and >= (frac is a whole
    number, so frac > x is frac >= x + 1)."""
    return tuple(frac >= x for x in _BANDS)


_BANDS = sorted({y for x in (4, 8, 20, 25, 26, 30, 33, 34, 35, 38, 40, 50, 51, 60, 70, 75, 80, 85, 90, 100)
                 for y in (x, x + 1)})


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
    # One fight's picks are no use in another: the cache holds one fight's
    # prepared state at a time (an id can be reused once a state is freed).
    global _AI_CACHE_ST
    if _AI_CACHE_ST is not b.st:
        _AI_CACHE.clear()
        _AI_CACHE_ST = b.st
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
    # The filter borrows the trainer AI's Basic; its few rolls (a speed tie)
    # get fixed dice here, so the search stays deterministic.
    saved, b.rng = b.rng, b.rng if getattr(b, "rng", None) is not None else random.Random(0)
    try:
        for mv in me.moves:
            if me.pp.get(mv.name, 1) <= 0 or (me.taunt and mv.cat == "Status") or fs.tormented_out(me, mv) \
                    or fs.move_heal_blocked(me, mv) or fs.disabled_out(me, mv) \
                    or ((me.rare or b.gravity) and fs.move_barred(b, me, mv)):
                continue
            if me.choice and mv.name != me.choice:
                continue
            if me.encore is not None and mv.name != me.encore:
                continue                 # Encore leaves the one move to choose
            if mv.effect in fs.SELF_KO or mv.effect == "FAINT_AND_ATK_SP_ATK_DOWN_2":
                continue
            f = fightai.figure(b, me, foe, mv)
            if fightai.basic(b, me, foe, mv, f) <= -8:
                continue           # a move that would do nothing here
            out.append(("move", mv))
    finally:
        b.rng = saved
    if not fs.trapped(b, me):            # a bind, Block, Ingrain, a trapping ability; a Shed Shell frees it
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
    c.mid_turn = True
    quick = getattr(c, "quick", None)
    c.quick = None
    if pa[0] == "switch" and (not fs.can_switch(c.p.cur()) or fs.ability_trapped(c, c.p.cur())):
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
        c.p.cur().switched_turn = c.turn     # it came in by its side's choice (fightsim.beak_doubles)
    if aa[0] == "switch":
        fs.switch_in(c, c.b, aa[1])
        c.b.cur().switched_turn = c.turn
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
        # Priority as the engine reckons it (Prankster, Gale Wings).
        if fs.move_priority(a, ma) != fs.move_priority(d, md):
            order.sort(key=lambda o: -fs.move_priority(o[0], o[1]))
        else:
            sa, sd = c.speed(a), c.speed(d)
            if c.trick_room:
                sa, sd = -sa, -sd
            if quick is not None:
                # A run: each Quick Claw was rolled before the trainer chose
                # (speedRand, which the AI's speed reading also sees); one
                # that fired puts its holder first, two cancel.
                qp, qf = quick.get(me.key, False), quick.get(foe.key, False)
                if qf and not qp:
                    order.reverse()
                elif qp == qf and (sa < sd or (sa == sd and not c.dice.tie_player_first())):
                    order.reverse()
                for mon in (me, foe):
                    if quick.get(mon.key) and mon.item == "Custap Berry":
                        fs.consume(mon)          # a Custap Berry that fired is eaten
            elif sa < sd or (sa == sd and not c.dice.tie_player_first()):
                # The player is slower: its Quick Claw (one in five) keeps it
                # first. Before this the check sat after this branch and could
                # never fire.
                if not (me.item == "Quick Claw" and c.dice.good(0.2, "quickclaw")):
                    order.reverse()
            elif foe.item == "Quick Claw" and c.dice.bad("quickclaw", 0.2):
                order.reverse()
    for i, (mon, mv) in enumerate(order):
        if i and fs.forced_out(c, mon):
            continue                     # dragged out before its turn, it does not act (fightsim.forced_out)
        target = fs.foe_of(c, mon)
        first = i == 0 and len(order) == 2
        use_move(c, mon, mv, target, first)
        if mon.wished:
            # Healing Wish: its replacement now, picked as a knockout's is.
            fs.wish_comes_true(c, mon, lambda side: fs.player_replacement(c) if side is c.p
                               else fightai.replacement(c, side, fs.foe_of(c, mon)))
        if getattr(mon, "u_turn", False) or getattr(mon, "baton", False):
            # subscript_attack_then_switch_out: no switch once the target's
            # side has nothing left (CheckBlackOut), with no one to send in
            # (TryReplaceFaintedMon), or when the user fell on the way (Rough
            # Skin, Destiny Bond). The replacement comes now, before a fainted
            # target's own at the turn's end, picked against the slot as it
            # stands, as BattleAI_PostKOSwitchIn reads it. Baton Pass
            # (subscript_baton_pass) switches the same way, through the same
            # party list, and hands the replacement its state (fightsim.baton_pass).
            passing = mon.baton
            mon.u_turn = mon.baton = False
            side = c.p if player(mon) else c.b
            if mon.alive() and (c.b if player(mon) else c.p).alive() and side.bench():
                if side is c.p:
                    idx = fs.player_replacement(c)
                else:
                    idx = fightai.replacement(c, side, fs.foe_of(c, mon))
                if idx is not None and idx != side.active:
                    (fs.baton_pass if passing else fs.switch_in)(c, side, idx)
    fs.end_of_turn(c)
    for mon in (c.p.cur(), c.b.cur()):
        if fs.rollout_lock_ticks(mon):       # a Rollout counts its own uses (fightsim.rollout_lock_ticks)
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
    # Quick Claw is rolled before anyone chooses, and the trainer's AI reads
    # the roll (BattleSystem_CompareBattlerSpeed sees speedRand).
    b.quick = {m.key: fs.custap_fires(m, b) or (m.item == "Quick Claw" and (b.dice.good(0.2, "quickclaw") if player(m) else b.dice.bad("quickclaw", 0.2)))
               for m in (b.p.cur(), b.b.cur())}
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
    # Held items by the scorer's own rule, unless the state names them (a
    # hand-played line's items, plstep3).
    held = st["held"] if "held" in st else fs.assign_items(st, team) if "split" in st else {}
    for m in pm:
        fs.hold(st, m, held.get(m.key))      # a Plate types its Judgment (fightsim.hold)
    bm = [fs.Mon(k, st["pokemon"][k], st["info"][k], st["moves"][k], "b") for k in boss_keys]
    b = fs.Battle(st, fs.Side(pm, "p"), fs.Side(bm, "b"), None, weather=st.get("base_weather"),
                  trick_room=st.get("trick_room", False), ai_flags=flags)
    b.luck_spent = 1.0
    b.luck = Luck((), 1.0)
    b.dice = SearchDice(b.luck)
    b.declined = frozenset()
    b.p.active = lead
    fs.open_battle(b)            # both leads in, then their Intimidate
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

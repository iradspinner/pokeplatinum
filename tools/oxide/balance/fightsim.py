"""The scoring rebuild's fight simulator (Ian's approval, 2026-09-27).

    PYTHONPATH=. python3 -m tools.oxide.balance.fightsim roark        # one story fight
    PYTHONPATH=. python3 -m tools.oxide.balance.fightsim --trainer 525 # one trainer

The headline score was a damage race blind to status and setup, so it read
the Galactic HQ B2F grunt above Officer Somnu's sleep team. This plays each
fight out turn by turn, many times, and records how many of the player's
Pokemon faint.

Each run draws a fresh six from the strongest third of the split's player
side (pool.py, at the cap), as the gauntlet's reading does, each with four
moves: its three strongest attacks of different types and its best status
move by Ian's tier list (docs/oxide/status-move-tiers.md), else a fourth
attack. The trainer's team is its own, moves and items included.

Damage comes from the calculator the scores use, run once per fight for
every attacker, target and move at neutral stages in each weather the
fight can have. The rest is applied here, as Generation 4 has it: stat
stages, burn halving physical damage, Reflect and Light Screen, critical
hits (1 in 16, doubled, ignoring the stages that would weaken them), the
roll, accuracy with accuracy and evasion stages. Status is Generation 4's:
sleep for one to four turns, paralysis quartering Speed and a quarter of
turns lost, burn and poison an eighth a turn, Toxic rising by sixteenths,
freezing thawed one turn in five, confusion for one to four turns with a
half chance of a 40-power hit on itself, flinching.

The trainer chooses as the game's AI does (docs/oxide/battle-ai, condensed
in fightai.py): its own flags score each move, with the switch rules and the
post-faint pick. The player follows a fixed policy: the best answer leads;
each turn it attacks with the move that finishes the foe soonest, uses a
status move when it turns the exchange, sets up while the foe needs three
or more hits to faint it, and switches to a bench member that wins the
exchange when the active one loses it, judging each switch-in on the move
the foe aimed at the Pokemon it replaces and going in through a pivot that
takes that move easily when nothing else can. It stalls out the foe's
screens, Tailwind, a move's Trick Room or weather, and a threat with few PP
left, by trading places between Pokemon that take little. After a faint it
sends in the best answer.

A fight's reading is the mean number of the player's Pokemon lost, the
chance of losing three or more, and the chance of a wipe.
"""
import collections
import csv
import functools
import json
import math
import os
import random
import re
import statistics
import sys
import tempfile

from ..encounters import calc_export
from . import b6, data, pool, pressure, teamscore

RUNS = 200
MAX_TURNS = 80
# Oxide's critical hits, the Generation 7 odds and multiplier
# (src/battle/battle_lib.c sCriticalStageRates, battle_script.c
# ApplyCriticalMul), not Platinum's 1 in 16 and double damage.
CRIT_RATE = {0: 1 / 24, 1: 1 / 8, 2: 1 / 2, 3: 1.0, 4: 1.0}
CRIT_MUL = 1.5
# The rock that stretches each weather a move sets from five turns to eight.
WEATHER_ROCK = {"Sun": "Heat Rock", "Rain": "Damp Rock", "Sand": "Smooth Rock", "Hail": "Icy Rock"}
STAGE_KEYS = ("atk", "def", "spa", "spd", "spe", "acc", "eva")
TIERS = {"SSS": 6, "S": 5, "A": 4, "B": 3, "C": 2, "D": 1, "F": 0}

# ---- moves ---------------------------------------------------------------------------------


@functools.lru_cache(maxsize=None)
def _by_calc_name():
    """{calculator move name: Oxide's move record}."""
    names = pool._move_names()
    recs = pokedex_moves()
    out = {}
    for const, calc in names.items():
        if const in recs:
            out[calc] = recs[const]
    # A few trainer files spell a move the older way; the compact name finds it.
    compact = {re.sub(r"[^a-z0-9]", "", r["name"].lower()): r for r in recs.values()}
    return out, compact


@functools.lru_cache(maxsize=None)
def pokedex_moves():
    from ..encounters import pokedex
    return pokedex.moves(data.ROOT)


class Move:
    """One move as the simulator reads it."""
    __slots__ = ("name", "type", "cat", "power", "acc", "pri", "effect", "chance", "range",
                 "contact", "sound", "pp", "const", "reflectable")

    def __init__(self, name):
        by, compact = _by_calc_name()
        rec = by.get(name) or compact.get(re.sub(r"[^a-z0-9]", "", name.lower())) or {}
        self.name = name
        self.const = rec.get("move")
        self.type = (rec.get("type") or "NORMAL").title()
        self.cat = {"PHYSICAL": "Physical", "SPECIAL": "Special"}.get(rec.get("class"), "Status")
        self.power = rec.get("power") or 0
        self.acc = rec.get("accuracy") or 0          # 0: never misses
        self.pri = rec.get("priority") or 0
        self.effect = rec.get("effect") or ("HIT" if self.power else "DO_NOTHING")
        self.chance = rec.get("effect_chance") or 0
        self.range = rec.get("range") or "SINGLE_TARGET"
        flags = rec.get("flags") or []
        self.contact = "MAKES_CONTACT" in flags
        self.sound = "SOUND" in " ".join(flags)
        self.reflectable = any("MAGIC_COAT" in f for f in flags)
        self.pp = rec.get("pp") or 10

    def damaging(self):
        return self.cat != "Status"

    def __repr__(self):
        return f"Move({self.name})"


@functools.lru_cache(maxsize=None)
def move(name):
    return Move(name)


# What each effect does beyond its damage. A status move whose effect is not
# here does nothing; a damaging one is a plain hit. fightsim_report counts
# the effects met that are not here.
STATUS_OF = {"STATUS_SLEEP": "slp", "STATUS_PARALYZE": "par", "STATUS_BURN": "brn",
             "STATUS_POISON": "psn", "STATUS_BADLY_POISON": "tox"}
HIT_STATUS = {"BURN_HIT": "brn", "PARALYZE_HIT": "par", "FREEZE_HIT": "frz", "POISON_HIT": "psn",
              "BADLY_POISON_HIT": "tox", "THAW_AND_BURN_HIT": "brn", "HIGH_CRITICAL_POISON_HIT": "psn",
              "HIGH_CRITICAL_BURN_HIT": "brn", "RECOIL_BURN_HIT": "brn", "RECOIL_PARALYZE_HIT": "par",
              "FLINCH_BURN_HIT": "brn", "FLINCH_PARALYZE_HIT": "par", "FLINCH_FREEZE_HIT": "frz",
              "BLIZZARD": "frz", "THUNDER": "par"}
FLINCH_HIT = {"FLINCH_HIT", "FLINCH_BURN_HIT", "FLINCH_PARALYZE_HIT", "FLINCH_FREEZE_HIT",
              "FLINCH_MINIMIZE_DOUBLE_HIT", "FLINCH_DOUBLE_DAMAGE_FLY_OR_BOUNCE"}
# Stat changes: (on whom, {stat: stages}); a hit's change comes with its chance.
SELF_STAGES = {
    "ATK_UP": {"atk": 1}, "ATK_UP_2": {"atk": 2}, "DEF_UP": {"def": 1}, "DEF_UP_2": {"def": 2},
    "SPEED_UP_2": {"spe": 2}, "SP_ATK_UP": {"spa": 1}, "SP_ATK_UP_2": {"spa": 2},
    "SP_DEF_UP_2": {"spd": 2}, "SP_ATK_SP_DEF_UP": {"spa": 1, "spd": 1},
    "ATK_SPD_UP": {"atk": 1, "spe": 1}, "ATK_DEF_UP": {"atk": 1, "def": 1},
    "DEF_SPD_UP": {"def": 1, "spd": 1}, "EVA_UP": {"eva": 1}, "EVA_UP_2_MINIMIZE": {"eva": 2},
    "DEF_UP_DOUBLE_ROLLOUT_POWER": {"def": 1}, "SP_DEF_UP_DOUBLE_ELECTRIC_POWER": {"spd": 1},
    "STOCKPILE": {"def": 1, "spd": 1}, "CHARGE_TURN_DEF_UP": {"def": 1},
    # Oxide's newer setup moves, under the effect names its table gives them.
    "SP_ATK_SP_DEF_SPEED_UP": {"spa": 1, "spd": 1, "spe": 1},
    "ATK_SP_ATK_SPEED_UP_2_DEF_SP_DEF_DOWN": {"atk": 2, "spa": 2, "spe": 2, "def": -1, "spd": -1},
    "ATK_DEF_ACC_UP": {"atk": 1, "def": 1, "acc": 1}, "SPEED_UP_2_ATK_UP": {"spe": 2, "atk": 1},
    "ATK_SP_ATK_UP": {"atk": 1, "spa": 1}, "ATK_ACC_UP": {"atk": 1, "acc": 1}, "DEF_UP_3": {"def": 3},
    "ATK_DEF_SPEED_UP": {"atk": 1, "def": 1, "spe": 1}, "TAKE_HEART": {"spa": 1, "spd": 1},
    "SHELL_SMASH": {"atk": 2, "spa": 2, "spe": 2, "def": -1, "spd": -1},
    "QUIVER_DANCE": {"spa": 1, "spd": 1, "spe": 1}, "COIL": {"atk": 1, "def": 1, "acc": 1},
    "SHIFT_GEAR": {"atk": 1, "spe": 2}, "HONE_CLAWS": {"atk": 1, "acc": 1},
    "WORK_UP": {"atk": 1, "spa": 1}, "GROWTH": {"atk": 1, "spa": 1},
}
FOE_STAGES = {
    "ATK_DOWN": {"atk": -1}, "ATK_DOWN_2": {"atk": -2}, "DEF_DOWN": {"def": -1},
    "DEF_DOWN_2": {"def": -2}, "SPEED_DOWN": {"spe": -1}, "SPEED_DOWN_2": {"spe": -2},
    "SP_DEF_DOWN_2": {"spd": -2}, "ACC_DOWN": {"acc": -1}, "EVA_DOWN": {"eva": -1},
    "ATK_DEF_DOWN": {"atk": -1, "def": -1}, "SP_ATK_DOWN_2_OPPOSITE_GENDER": {"spa": -2},
}
HIT_FOE_STAGES = {
    "LOWER_SP_DEF_HIT": {"spd": -1}, "LOWER_DEFENSE_HIT": {"def": -1},
    "LOWER_SPEED_HIT": {"spe": -1}, "LOWER_ACCURACY_HIT": {"acc": -1},
    "LOWER_ATTACK_HIT": {"atk": -1}, "SPEED_DOWN_HIT": {"spe": -1},
}
HIT_SELF_STAGES = {  # (stages, certain)
    "DEF_SPD_DOWN_HIT": ({"def": -1, "spd": -1}, True),
    "LOWER_OWN_ATK_AND_DEF": ({"atk": -1, "def": -1}, True),
    "USER_SP_ATK_DOWN_2": ({"spa": -2}, True),
    "RAISE_ATTACK_HIT": ({"atk": 1}, False), "RAISE_SP_ATK_HIT": ({"spa": 1}, False),
    "RAISE_DEF_HIT": ({"def": 1}, False),
    "RAISE_ALL_STATS_HIT": ({"atk": 1, "def": 1, "spa": 1, "spd": 1, "spe": 1}, False),
}
RECOIL = {"RECOIL_THIRD": 1 / 3, "RECOIL_QUARTER": 1 / 4, "RECOIL_HALF": 1 / 2,
          "RECOIL_BURN_HIT": 1 / 3, "RECOIL_PARALYZE_HIT": 1 / 3}
HEAL_HALF = {"RESTORE_HALF_HP", "HEAL_HALF_REMOVE_FLYING_TYPE"}
TWO_TURN = {"FLY", "DIG", "DIVE", "BOUNCE", "SHADOW_FORCE", "CHARGE_TURN_HIGH_CRIT", "CHARGE_TURN_HIGH_CRIT_FLINCH",
            "CHARGE_TURN_DEF_UP", "SOLAR_BEAM", "SKIP_CHARGE_TURN_IN_SUN"}
INVULNERABLE = {"FLY", "DIG", "DIVE", "BOUNCE", "SHADOW_FORCE"}
SELF_KO = {"HALVE_DEFENSE", "EXPLOSION", "FAINT_AND_ATK_SP_ATK_DOWN_2"}
WEATHER_OF = {"WEATHER_RAIN": "Rain", "WEATHER_SUN": "Sun", "WEATHER_SANDSTORM": "Sand",
              "WEATHER_HAIL": "Hail"}
ABILITY_WEATHER = {"Drizzle": "Rain", "Drought": "Sun", "Sand Stream": "Sand", "Snow Warning": "Hail"}
# The abilities no obtainable Pokemon keeps in a regular slot (Ian, 2026-09-26),
# and the stand-in the player's side takes when both its regular slots held one.
NO_WEATHER_ABILITY = set(ABILITY_WEATHER) | {"Cloud Nine", "Air Lock"}
WEATHER_STAND_IN = "Pressure"


# ---- the Pokemon and the field -----------------------------------------------------------

class Mon:
    """One Pokemon in a battle."""

    def __init__(self, key, rec, info, moves, side):
        self.key, self.side = key, side
        self.species = rec.get("species")
        self.level = rec.get("level") or 50
        self.maxhp = info["hp"]
        self.hp = self.maxhp
        self.stats = info["stats"]
        self.types = [t.title() for t in info.get("types") or []]
        self.ability = info.get("ability") or rec.get("ability")
        self.item = info.get("item") or rec.get("item")
        self.moves = [move(m) for m in moves][:4]
        self.pp = {m.name: m.pp for m in self.moves}
        self.ivs = rec.get("ivs") or {}
        self.status, self.sleep, self.toxic = None, 0, 0
        self.reset_volatile()

    def reset_volatile(self):
        self.stages = dict.fromkeys(STAGE_KEYS, 0)
        self.rollout = 0
        self.curled = False
        self.confused = 0
        self.flinch = False
        self.seeded = False
        self.yawn = 0
        self.protect_run = 0
        self.protecting = False
        self.sub = 0
        self.charging = None
        self.recharge = False
        # Block and Mean Look: this Pokemon cannot switch while the Pokemon
        # that trapped it (trapped_by, its key) stays in. Ingrain roots the
        # user: it cannot switch, and heals at the end of each turn.
        self.trapped_by = None
        self.ingrained = False
        self.lock = None                 # (move, turns) for Outrage and kin
        self.choice = None
        self.taunt = 0
        self.last = None
        self.turns_in = 0
        self.hit_this_turn = None        # (category, damage) of the last hit taken this turn
        self.last_hit_by = None          # the move last aimed at it since it last acted
        self.last_hit_type = None        # that move's type as the battle recorded it (Weather Ball)
        self.crit_stage = 0
        self.bound = 0
        self.enduring = False
        self.cursed = False
        self.u_turn = False
        self.baton = False
        self.chosen = None
        self.perish = 0                  # Perish Song's count; switching out clears it
        # The moves the trainer's AI has seen this Pokemon use since it came
        # in (AI_CONTEXT.battlerMoves; fightai.choose records them).
        self.shown = []
        # The ability a battle message has named (AI_CONTEXT.battlerAbilities,
        # BattleAI_SetAbility); the trainer's AI guesses until then.
        self.revealed = None
        self.flash_fire = False          # lit by a Fire move it took

    def alive(self):
        return self.hp > 0

    def frac(self):
        return 100 * self.hp // self.maxhp if self.maxhp else 0

    def __repr__(self):
        return f"{self.species}({self.hp}/{self.maxhp})"


class Side:
    """One side's Pokemon. In a double battle `active2` is the second slot's
    index, and each Pokemon's `owner` says whose party it is (the player's,
    a partner's, or one of two opposing trainers'), so a fainted slot is
    refilled from its own trainer's party."""

    def __init__(self, mons, name):
        self.mons, self.name = mons, name
        self.active = 0
        self.active2 = None
        self.screens = {"Reflect": 0, "Light Screen": 0}
        self.tailwind = 0
        self.hazards = {"rocks": 0, "spikes": 0, "tspikes": 0}
        self.safeguard = 0

    def cur(self):
        return self.mons[self.active]

    def on_field(self):
        idx = [self.active] + ([self.active2] if self.active2 is not None else [])
        return [self.mons[i] for i in idx]

    def bench(self, owner=None):
        return [m for i, m in enumerate(self.mons) if i not in (self.active, self.active2)
                and m.alive() and (owner is None or getattr(m, "owner", None) == owner)]

    def alive(self):
        return [m for m in self.mons if m.alive()]


class Battle:
    """One battle's state and rules, with the damage rows it reads."""

    def __init__(self, st, player, boss, rng, weather=None, trick_room=False, ai_flags=0):
        self.st, self.rng = st, rng
        self.p, self.b = player, boss
        self.weather = weather
        self.weather_turns = 0 if weather else 0     # 0 with weather set: permanent
        self.trick_room = 999 if trick_room else 0
        self.turn = 0
        self.ai_flags = ai_flags
        self.log = []

    # -- reading the calculator's rows

    def row(self, att, dfn):
        w = self.weather if (self.weather, att.key, dfn.key) in self.st["rows"] else None
        return self.st["rows"].get((w, att.key, dfn.key))

    def rolls(self, att, dfn, mv):
        r = self.row(att, dfn)
        if not r:
            return None
        got = r["moves"].get(mv.name)
        if not got or "error" in got:
            return None
        return got["rolls"]

    def speed(self, mon):
        """Speed as BattleSystem_CompareBattlerSpeed works it, in whole
        numbers: the calculator's figure (weather abilities and items in
        it) at the Speed stage (sStatStageBoosts, truncated), then Quick
        Feet's 1.5 with a status or else paralysis's quarter, then Tailwind."""
        s = int(self.st["speed"].get((self.weather, mon.key)) or self.st["speed"].get((None, mon.key)) or 1)
        st = mon.stages["spe"]
        s = s * (10 + 5 * st) // 10 if st >= 0 else s * 10 // (10 - 5 * st)
        if mon.ability == "Quick Feet" and mon.status:
            s = s * 15 // 10
        elif mon.status == "par":
            s //= 4
        side = self.p if mon.side == "p" else self.b
        if side.tailwind:
            s *= 2
        return s

    def faster(self, a, b):
        """Whether a moves before b at equal priority; ties at random."""
        sa, sb = self.speed(a), self.speed(b)
        if self.trick_room:
            sa, sb = -sa, -sb
        if sa == sb:
            return self.rng.random() < 0.5
        return sa > sb

    # -- damage

    def damage(self, att, dfn, mv, crit=None, roll=None, ai_view=False):
        """One use's damage, or None when the calculator has no figure. With
        ai_view: the top roll, no critical hit, as the AI reckons it."""
        rolls = self.rolls(att, dfn, mv)
        if rolls is None:
            return None
        base = rolls[-1] if ai_view else (rolls[roll] if roll is not None else self.rng.choice(rolls))
        if base <= 0:
            return 0
        a_st, d_st = ("atk", "def") if mv.cat == "Physical" else ("spa", "spd")
        a, d = att.stages[a_st], dfn.stages[d_st]
        if crit:
            a, d = max(a, 0), min(d, 0)
        mult = stage_mult(a) / stage_mult(d)
        if mv.cat == "Physical" and att.status == "brn" and att.ability != "Guts":
            mult *= 0.5
        if att.ability == "Guts" and att.status:
            mult *= 1.5
        if att.ability == "Flash Fire" and mv.type == "Fire" and not att.flash_fire:
            mult *= 2 / 3        # the calculator's row has Flash Fire always lit
        if att.side == "p" and BOOSTER_TYPE.get(att.item) == mv.type:
            mult *= 1.2          # the player's rows are item-free; a booster adds its fifth here
        side = self.p if dfn.side == "p" else self.b
        screen = "Reflect" if mv.cat == "Physical" else "Light Screen"
        if side.screens[screen] and not crit and mv.effect != "REMOVE_SCREENS" and att.ability != "Infiltrator":
            mult *= 2 / 3 if getattr(self, "doubles", False) else 0.5
        if getattr(self, "spread", False):
            mult *= 0.75
        if crit:
            mult *= CRIT_MUL * (1.5 if att.ability == "Sniper" else 1.0)
        if not ai_view:
            # TrainerAI_CalcDamage has no Rollout case: the AI costs it at
            # its listed power, with no Defense Curl and no run count.
            mult *= rollout_mult(att, mv)
        return max(1, int(base * mult))

    def accuracy_hits(self, att, dfn, mv):
        if mv.acc == 0 or mv.effect == "BYPASS_ACCURACY":
            return True
        acc = mv.acc
        if mv.effect == "THUNDER":
            acc = 100 if self.weather == "Rain" else 50 if self.weather == "Sun" else acc
        if mv.effect == "BLIZZARD" and self.weather == "Hail":
            return True
        s = max(-6, min(6, att.stages["acc"] - dfn.stages["eva"]))
        acc = acc * ((3 + s) / 3 if s >= 0 else 3 / (3 - s))
        if att.ability == "Compound Eyes":
            acc *= 1.3
        if att.ability == "Hustle" and mv.cat == "Physical":
            acc *= 0.8
        return self.rng.random() * 100 < acc


def stage_mult(s):
    return (2 + s) / 2 if s >= 0 else 2 / (2 - s)


# ---- the rules of a turn --------------------------------------------------------------------

def can_status(b, target, status):
    if target.status or not target.alive() or target.sub:
        return False
    side = b.p if target.side == "p" else b.b
    if side.safeguard:
        return False
    t = set(target.types)
    if status in ("psn", "tox") and t & {"Poison", "Steel"}:
        return False
    if status == "brn" and "Fire" in t:
        return False
    if status == "frz" and "Ice" in t:
        return False
    if status == "par" and "Electric" in t:
        return False
    return target.ability not in STATUS_ABILITIES.get(status, set())


STATUS_ABILITIES = {"slp": {"Insomnia", "Vital Spirit"}, "par": {"Limber"}, "brn": {"Water Veil"},
                    "psn": {"Immunity"}, "tox": {"Immunity"}, "frz": {"Magma Armor"}}
# The abilities announced as their holder comes in (each message tags the
# ability, so BattleAI_SetAbility records it).
ENTRY_ANNOUNCED = {"Intimidate", "Pressure", "Mold Breaker", "Drizzle", "Drought", "Sand Stream",
                   "Snow Warning", "Download", "Trace", "Anticipation", "Forewarn", "Frisk", "Slow Start",
                   "Unnerve", "Neutralizing Gas"}


# The abilities that turn a hit to nothing, and so are named when they do.
ZEROING = {"Volt Absorb", "Water Absorb", "Flash Fire", "Motor Drive", "Dry Skin", "Lightning Rod",
           "Storm Drain", "Sap Sipper", "Levitate", "Wonder Guard", "Soundproof", "Bulletproof"}


# The abilities that take a move whole, which the AI's damage estimate does
# not see (fightai.figure costs the move on an ability-blank twin).
AI_BLIND_ABSORBS = {"Volt Absorb", "Water Absorb", "Flash Fire", "Motor Drive", "Dry Skin", "Lightning Rod",
                    "Storm Drain", "Sap Sipper", "Soundproof", "Bulletproof"}


def reveal(mon):
    """A battle message has named mon's ability (BattleAI_SetAbility): the
    trainer's AI reads it from now on, until mon leaves the field. The
    simulator names it where the engine would for what the simulator
    models: an entry announcement, a hit the ability turns to nothing, Sturdy
    holding, a status or a stat drop the ability stops."""
    mon.revealed = mon.ability


def stat_drop_blocked(b, mon, changes):
    """Whether mon's ability stops a drop the foe inflicts (Clear Body and
    White Smoke stop any; Hyper Cutter Attack, Keen Eye accuracy, Big Pecks
    Defense); the ability that stops it is named."""
    falls = {k for k, v in changes.items() if v < 0}
    if not falls:
        return False
    ab = mon.ability
    if ab in ("Clear Body", "White Smoke") or (ab == "Hyper Cutter" and falls <= {"atk"}) \
            or (ab == "Keen Eye" and falls <= {"acc"}) or (ab == "Big Pecks" and falls <= {"def"}):
        reveal(mon)
        return True
    return False


# The powder and spore moves (battle_lib.c, sPowderMoves): Grass types and
# Overcoat are immune to them in Oxide (Generation 6).
POWDER = {"Cotton Spore", "Poison Powder", "Sleep Powder", "Stun Spore", "Spore", "Powder",
          "Rage Powder", "Magic Powder"}


def powder_immune(target, mv):
    return mv.name in POWDER and ("Grass" in target.types or target.ability == "Overcoat")


def leaf_guarded(b, target):
    """Leaf Guard keeps every major status off its holder in sun. The engine
    knows it; the AI does not, so this is not part of can_status."""
    return target.ability == "Leaf Guard" and b.weather == "Sun"


def give_status(b, target, status):
    if not can_status(b, target, status) or leaf_guarded(b, target):
        if target.alive() and not target.status and (target.ability in STATUS_ABILITIES.get(status, ())
                                                     or leaf_guarded(b, target)):
            reveal(target)
        return False
    target.status = status
    if status == "slp":
        target.sleep = b.rng.randint(1, 4)
    if status == "tox":
        target.toxic = 0
    return True


def change_stages(mon, changes):
    # Simple doubles every change to its own stages.
    mult = 2 if getattr(mon, "ability", None) == "Simple" else 1
    for k, v in changes.items():
        mon.stages[k] = max(-6, min(6, mon.stages[k] + v * mult))


ROLLOUT = "DOUBLE_POWER_EACH_TURN_LOCK_INTO"   # Rollout and Ice Ball


def rollout_mult(att, mv):
    """Rollout and Ice Ball double each hit in a row, five at most, and
    twice again after Defense Curl."""
    if mv.effect != ROLLOUT:
        return 1
    # The hit's place in the run, taken before rollout_after moved the count
    # on: the first hit is 1x, then 2x, 4x...; Defense Curl doubles each.
    return 2 ** getattr(att, "rollout_hit", 0) * (2 if getattr(att, "curled", False) else 1)


def rollout_after(att, mv, hit):
    """The lock after a use: the next hit in a row, or the run broken by a
    miss or its fifth hit."""
    if mv.effect != ROLLOUT:
        return
    att.rollout_hit = getattr(att, "rollout", 0) if hit else 0
    att.rollout = getattr(att, "rollout", 0) + 1 if hit else 0
    if not hit or att.rollout >= 5:
        att.rollout = 0
        att.lock = None
    else:
        att.lock = (mv, 5 - att.rollout)


# Magnitude's powers and their chances in percent (Generation 4, Magnitude 4
# to 10). The decomp names its effect BATTLE_EFFECT_PSYWAVE, as pret's vanilla
# data does; Psywave itself is RANDOM_DAMAGE_1_TO_150_LEVEL.
MAGNITUDE_POWERS = {10: 5, 30: 10, 50: 20, 70: 30, 90: 20, 110: 10, 150: 5}

# The moves whose effect script sets the damage itself (res/battle/scripts/
# effects): stat stages, screens, burn, items and critical hits never touch
# the figure, but the type chart still runs, so an immune target takes
# nothing (ApplyTypeMultiplier flags MOVE_STATUS_INEFFECTIVE even with
# SYSCTL_IGNORE_TYPE_CHECKS set): Seismic Toss misses a Ghost, Night Shade a
# Normal type, Dragon Rage a Fairy.
FIXED_DAMAGE = {"40_DAMAGE_FLAT", "20_DAMAGE_FLAT", "LEVEL_DAMAGE_FLAT", "RANDOM_DAMAGE_1_TO_150_LEVEL",
                "HALVE_HP", "QUARTER_HP", "SET_HP_EQUAL_TO_USER", "FINAL_GAMBIT"}


def fixed_damage(b, att, dfn, mv, tenths=10):
    """A fixed-damage move's damage, 0 when it fails or the target's type is
    immune, or None for any other move. tenths is Psywave's roll, 5 to 15
    (`Random 10, 5`, then level times the roll over ten, at least 1)."""
    if mv.effect not in FIXED_DAMAGE:
        return None
    if effectiveness(b.st["chart"], mv.type, dfn.types) == 0:
        return 0
    e = mv.effect
    if e == "40_DAMAGE_FLAT":
        return 40
    if e == "20_DAMAGE_FLAT":
        return 20
    if e == "LEVEL_DAMAGE_FLAT":
        return att.level
    if e == "RANDOM_DAMAGE_1_TO_150_LEVEL":
        return max(1, att.level * tenths // 10)
    if e == "HALVE_HP":
        return max(1, dfn.hp // 2)                 # BattleSystem_Divide keeps at least 1
    if e == "QUARTER_HP":
        return 3 * max(1, dfn.hp // 4)            # three quarters of the target's HP, as its script has it
    if e == "SET_HP_EQUAL_TO_USER":
        return max(0, dfn.hp - att.hp)            # fails when the target has no more HP than the user
    return att.hp                                 # Final Gambit; attack() faints the user


def ohko_blocked(b, att, dfn, mv):
    """A one-hit KO move fails on a type it cannot hit, a higher-level
    target, or Sturdy unless the user has Mold Breaker (BtlCmd_TryOHKOMove)."""
    return (effectiveness(b.st["chart"], mv.type, dfn.types) == 0 or att.level < dfn.level
            or (dfn.ability == "Sturdy" and att.ability != "Mold Breaker"))


def hurt(b, mon, amount):
    """HP lost to anything but a move's hit."""
    if amount <= 0 or not mon.alive():
        return
    mon.hp = max(0, mon.hp - amount)
    berry_check(mon)


# A pinch berry raises a stat by one stage once its holder is at a quarter of
# its HP or less; Sitrus heals a quarter and Oran 10 once at half or less. In
# Generation 4 each fires as soon as the HP drops, not at the end of the turn.
PINCH_BERRIES = {"Apicot Berry": "spd", "Liechi Berry": "atk", "Ganlon Berry": "def",
                 "Salac Berry": "spe", "Petaya Berry": "spa"}


def berry_check(mon):
    if not mon.alive() or not mon.item:
        return
    if mon.item in PINCH_BERRIES and mon.hp * 4 <= mon.maxhp:
        change_stages(mon, {PINCH_BERRIES[mon.item]: 1})
        mon.item = None
    elif mon.item == "Sitrus Berry" and mon.hp * 2 <= mon.maxhp:
        heal(mon, mon.maxhp // 4)
        mon.item = None
    elif mon.item == "Oran Berry" and mon.hp * 2 <= mon.maxhp:
        heal(mon, 10)
        mon.item = None


def can_switch(mon):
    """False while Block, Mean Look or its own Ingrain holds it in."""
    return mon.trapped_by is None and not mon.ingrained


def heal(mon, amount):
    mon.hp = min(mon.maxhp, mon.hp + max(0, amount))


def foe_of(b, mon):
    """The foe it faces: in a double battle the first standing one."""
    side = b.b if mon.side == "p" else b.p
    return next((m for m in side.on_field() if m.alive()), side.cur())


# The ranges whose defender is the user itself (BattleSystem_Defender): a
# move of these never marks a foe as hit.
OWN_RANGES = {"USER", "USER_SIDE", "SINGLE_TARGET_SPECIAL", "FIELD", "ALL", "ALLY", "USER_OR_ALLY"}


def mark_hit(b, mv, dfn, shown, targets=None):
    """BattleControllerPlayer_UpdateFlagsWhenHit: once the attack message
    shows, the move is the last to hit its defender, a status move or a
    miss included; a user that could not move clears its defender's record
    instead. The switch rules read this record."""
    if mv.range in OWN_RANGES or dfn is None:
        return
    for d in targets or [dfn]:
        d.last_hit_by = mv if shown else None
        d.last_hit_type = ({"Sun": "Fire", "Rain": "Water", "Hail": "Ice", "Sand": "Rock"}.get(b.weather, mv.type)
                           if shown and mv.name == "Weather Ball" else mv.type if shown else None)


def could_not_act(b, att, mv, dfn, targets=None):
    """A turn the Pokemon could not act (recharging, frozen, asleep,
    flinched, hurt by its confusion, fully paralysed, or a status move
    stopped by Taunt). The engine never marks such a move as succeeded, so
    it records no previous move (movePrevByBattler is MOVE_NONE, which the
    AI reads as move 0) and the Protect run breaks
    (BattleControllerPlayer_UpdateMoveBuffers); its target's last-hit
    record is cleared."""
    att.last = None
    att.protect_run = 0
    mark_hit(b, mv, dfn, False, targets)


def sleep_tick(att):
    """One move attempt while asleep (the sleep check in
    battle_controller_player.c). The engine's counter is att.sleep + 1, set
    to 2 to 5 by the fall-asleep script and to 3 by Rest; each attempt takes
    one off, two with Early Bird, and the Pokemon wakes and acts once it
    reaches zero. True while it stays asleep."""
    drop = 2 if att.ability == "Early Bird" else 1
    if att.sleep >= drop:
        att.sleep -= drop
        return True
    att.sleep = 0
    att.status = None
    return False


def use_move(b, att, mv, dfn, first, targets=None):
    """One move, from its user's turn check to its last effect. `first`:
    whether the target has not moved yet this turn."""
    if not att.alive():
        return
    # Its own record clears with its action, whatever happens
    # (BattleControllerPlayer_ClearFlags).
    att.last_hit_by = None
    # The user's own state first.
    if att.recharge:
        att.recharge = False
        return could_not_act(b, att, mv, dfn, targets)
    if att.status == "frz":
        if b.rng.random() < 0.2 or mv.effect == "THAW_AND_BURN_HIT":
            att.status = None
        else:
            return could_not_act(b, att, mv, dfn, targets)
    if att.status == "slp":
        # The counter is the turns it cannot move (one to four); when it has
        # run out the Pokemon wakes and acts the same turn, as in Generation 4.
        if sleep_tick(att):
            if mv.effect not in ("DAMAGE_WHILE_ASLEEP", "USE_RANDOM_LEARNED_MOVE_SLEEP"):
                return could_not_act(b, att, mv, dfn, targets)
    if att.flinch:
        att.flinch = False
        return could_not_act(b, att, mv, dfn, targets)
    if att.confused:
        att.confused -= 1
        if att.confused and b.rng.random() < 0.5:
            hurt(b, att, confusion_damage(att, b.rng))
            return could_not_act(b, att, mv, dfn, targets)
    if att.status == "par" and b.rng.random() < 0.25:
        return could_not_act(b, att, mv, dfn, targets)
    if att.taunt and mv.cat == "Status":
        return could_not_act(b, att, mv, dfn, targets)
    mark_hit(b, mv, dfn, True, targets)
    att.pp[mv.name] = att.pp.get(mv.name, 1) - 1
    if mv.effect not in ("PROTECT", "SURVIVE_WITH_1_HP"):
        att.protect_run = 0
    att.last = mv
    if att.item and att.item.startswith("Choice") and not att.choice:
        att.choice = mv.name
    # Charging moves: the first turn only charges (Fly and Dig vanish).
    if mv.effect in TWO_TURN and att.charging is None:
        if mv.effect in ("SOLAR_BEAM", "SKIP_CHARGE_TURN_IN_SUN") and b.weather == "Sun":
            pass
        elif att.item == "Power Herb":
            att.item = None
        else:
            att.charging = mv
            if mv.effect == "CHARGE_TURN_DEF_UP":
                change_stages(att, {"def": 1})
            return
    att.charging = None
    if mv.cat == "Status":
        status_move(b, att, mv, dfn, first)
        return
    if targets is None:
        attack(b, att, mv, dfn, first)
        return
    # A double battle: a spread move hits each target at three quarters.
    b.spread = len(targets) > 1
    for t in targets:
        attack(b, att, mv, t, t not in b.moved)
    b.spread = False


def confusion_damage(mon, rng):
    """A 40-power typeless physical hit on itself, Generation 4's formula."""
    a = mon.stats.get("atk", 50) * stage_mult(mon.stages["atk"])
    d = mon.stats.get("def", 50) * stage_mult(mon.stages["def"])
    base = ((2 * mon.level // 5 + 2) * 40 * a / d) // 50 + 2
    return int(base * rng.randint(85, 100) / 100)


def explode_first(b, att):
    """Explosion and Self-Destruct (effect script 7) set their user's HP to
    0 before the hit is worked out, so the user faints even when the move
    then misses or meets Protect, an immune type or a Pokemon in the air. A
    Damp Pokemon anywhere on the field stops the move first, and its user
    keeps its HP, unless the user has Mold Breaker. False when Damp stopped
    it."""
    if att.ability != "Mold Breaker" and any(
            m.ability == "Damp" and m.alive() for m in b.p.on_field() + b.b.on_field()):
        return False
    att.hp = 0
    return True


def attack(b, att, mv, dfn, first):
    if not dfn.alive():
        return
    if mv.effect in SELF_KO and not explode_first(b, att):
        return
    if dfn.charging is not None and dfn.charging.effect in INVULNERABLE:
        return
    if dfn.protecting and mv.effect not in ("REMOVE_PROTECT",):
        return
    if mv.effect == "HIT_FIRST_IF_TARGET_ATTACKING":        # Sucker Punch
        nxt = getattr(dfn, "chosen", None)
        if not first or nxt is None or nxt.cat == "Status":
            return
    if mv.effect == "ALWAYS_FLINCH_FIRST_TURN_ONLY" and att.turns_in > 0:
        return
    # Natural Gift and Fling spend the held item, and fail without one (a
    # Natural Gift needs a berry).
    if mv.name in ("Natural Gift", "Fling"):
        if not att.item or (mv.name == "Natural Gift" and "Berry" not in att.item):
            return
        att.item = None
    if not b.accuracy_hits(att, dfn, mv):
        if mv.effect == "CRASH_ON_MISS":
            hurt(b, att, att.maxhp // 2)
        rollout_after(att, mv, False)
        return
    rollout_after(att, mv, True)
    # Fixed-damage moves.
    dmg = fixed_damage(b, att, dfn, mv, b.rng.randint(5, 15) if mv.effect == "RANDOM_DAMAGE_1_TO_150_LEVEL" else 10)
    if mv.effect == "ONE_HIT_KO":
        if ohko_blocked(b, att, dfn, mv) or b.rng.random() * 100 >= 30 + att.level - dfn.level:
            return
        dmg = dfn.hp
    elif mv.effect in ("COUNTER", "MIRROR_COAT", "METAL_BURST"):
        hit = att.hit_this_turn
        want = {"COUNTER": "Physical", "MIRROR_COAT": "Special"}.get(mv.effect)
        if not hit or (want and hit[0] != want) or effectiveness(b.st["chart"], mv.type, dfn.types) == 0:
            return
        dmg = int(hit[1] * (1.5 if mv.effect == "METAL_BURST" else 2))
    if dmg is None:
        stage = att.crit_stage + (1 if mv.effect.startswith("HIGH_CRITICAL") or
                                  mv.effect.startswith("CHARGE_TURN_HIGH_CRIT") else 0)
        crit = b.rng.random() < CRIT_RATE[min(stage, 4)] and dfn.ability not in ("Battle Armor", "Shell Armor")
        dmg = b.damage(att, dfn, mv, crit=crit)
        if dmg is None:
            return
        if mv.effect == "DOUBLE_POWER_IF_MOVING_SECOND" and not first:
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
        if dfn.ability in ZEROING and effectiveness(b.st["chart"], mv.type, dfn.types) > 0:
            reveal(dfn)              # an absorbing ability, Levitate or Wonder Guard took it
            if dfn.ability == "Flash Fire" and mv.type == "Fire":
                dfn.flash_fire = True
        return
    # The hit lands: Substitute, Focus Sash and Sturdy, then the damage.
    if dfn.sub:
        dfn.sub = max(0, dfn.sub - dmg)
        dealt = 0
    else:
        full = dfn.hp == dfn.maxhp
        if dmg >= dfn.hp and full and (dfn.item == "Focus Sash" or dfn.ability == "Sturdy"):
            if dfn.ability == "Sturdy":
                reveal(dfn)
            dmg = dfn.hp - 1
            if dfn.item == "Focus Sash":
                dfn.item = None
        if dmg >= dfn.hp and getattr(dfn, "enduring", False):
            dmg = dfn.hp - 1
        dealt = min(dmg, dfn.hp)
        dfn.hp -= dealt
        dfn.hit_this_turn = (mv.cat, dealt)
        if dfn.status == "frz" and mv.type == "Fire":
            dfn.status = None
    # The move's own effects.
    e = mv.effect
    if e in RECOIL and att.ability != "Rock Head":
        hurt(b, att, max(1, int(dealt * RECOIL[e])))
    if e in ("RECOVER_HALF_DAMAGE_DEALT", "RECOVER_DAMAGE_SLEEP"):
        heal(att, dealt // 2)
    if e == "RECHARGE_AFTER":
        att.recharge = True
    if e in SELF_KO or e == "FINAL_GAMBIT":
        att.hp = 0
    if e == "CONTINUE_AND_CONFUSE_SELF":
        if att.lock is None:
            att.lock = (mv, b.rng.randint(2, 3))
    if att.item == "Life Orb" and dealt and att.ability != "Magic Guard":
        hurt(b, att, att.maxhp // 10)
    if e == "REMOVE_SCREENS":
        side = b.p if dfn.side == "p" else b.b
        side.screens = dict.fromkeys(side.screens, 0)
    if e in HIT_SELF_STAGES:
        ch, certain = HIT_SELF_STAGES[e]
        if certain or b.rng.random() * 100 < (mv.chance or 10):
            change_stages(att, ch)
    if not dfn.alive() or dfn.sub:
        return
    chance = mv.chance or 0
    if dfn.ability == "Shield Dust":
        chance = 0
    if att.ability == "Serene Grace":
        chance *= 2
    if e in HIT_STATUS and b.rng.random() * 100 < chance:
        give_status(b, dfn, HIT_STATUS[e])
    if e == "TRI_ATTACK" and b.rng.random() * 100 < chance:
        give_status(b, dfn, b.rng.choice(["brn", "par", "frz"]))
    if e in FLINCH_HIT and first and b.rng.random() * 100 < chance:
        dfn.flinch = True
    if e == "ALWAYS_FLINCH_FIRST_TURN_ONLY" and first:
        dfn.flinch = True
    if e == "CONFUSE_HIT" and b.rng.random() * 100 < chance and not dfn.confused:
        dfn.confused = b.rng.randint(2, 5)
    if e in HIT_FOE_STAGES and b.rng.random() * 100 < chance and not stat_drop_blocked(b, dfn, HIT_FOE_STAGES[e]):
        change_stages(dfn, HIT_FOE_STAGES[e])
    if e == "SWITCH_HIT":
        att.u_turn = True
    if e in ("BIND_HIT", "WHIRLPOOL") and not dfn.bound:
        dfn.bound = b.rng.randint(2, 5)
    if e in ("REMOVE_HELD_ITEM", "STEAL_HELD_ITEM"):
        dfn.item = None


def status_move(b, att, mv, dfn, first):
    e = mv.effect
    foe_side = b.p if dfn.side == "p" else b.b
    own_side = b.p if att.side == "p" else b.b
    targets_foe = mv.range not in ("USER", "USER_SIDE", "ALLY", "FIELD", "USER_OR_ALLY")
    if targets_foe and dfn.alive():
        if dfn.protecting:
            return
        # The engine runs the type chart only for moves with power, and for
        # Thunder Wave (BattleControllerPlayer_CheckTypeChart), so Thunder
        # Wave fails on a Ground type while Hypnosis still sleeps a Dark one.
        if mv.name == "Thunder Wave" and effectiveness(b.st["chart"], mv.type, dfn.types) == 0:
            return
        if powder_immune(dfn, mv):
            return
        if not b.accuracy_hits(att, dfn, mv):
            return
    if e in STATUS_OF:
        if dfn.sub:
            return
        give_status(b, dfn, STATUS_OF[e])
    elif e == "STATUS_CONFUSE":
        if not dfn.sub and not dfn.confused and dfn.ability != "Own Tempo":
            dfn.confused = b.rng.randint(2, 5)
    elif e in ("ATK_UP_2_STATUS_CONFUSION", "SP_ATK_UP_CAUSE_CONFUSION"):
        if not dfn.sub:
            change_stages(dfn, {"atk": 2} if e.startswith("ATK") else {"spa": 1})
            if not dfn.confused and dfn.ability != "Own Tempo":
                dfn.confused = b.rng.randint(2, 5)
    elif e == "STATUS_SLEEP_NEXT_TURN":
        if not dfn.status and not dfn.yawn and not dfn.sub:
            dfn.yawn = 2
    elif e == "STATUS_LEECH_SEED":
        if "Grass" not in dfn.types and not dfn.sub:
            dfn.seeded = True
    elif e in SELF_STAGES:
        change_stages(att, SELF_STAGES[e])
        if e == "DEF_UP_DOUBLE_ROLLOUT_POWER":
            att.curled = True
    elif e in FOE_STAGES:
        if not dfn.sub and not stat_drop_blocked(b, dfn, FOE_STAGES[e]):
            change_stages(dfn, FOE_STAGES[e])
    elif e == "CURSE":
        if "Ghost" in att.types:
            hurt(b, att, att.maxhp // 2)
            dfn.cursed = True
        else:
            change_stages(att, {"atk": 1, "def": 1, "spe": -1})
    elif e == "MAX_ATK_LOSE_HALF_MAX_HP":
        if att.hp > att.maxhp // 2:
            hurt(b, att, att.maxhp // 2)
            att.stages["atk"] = 6
    elif e == "CRIT_UP_2":
        att.crit_stage = 2
    elif e in HEAL_HALF:
        heal(att, att.maxhp // 2)
    elif e == "HEAL_HALF_MORE_IN_SUN":
        frac = 2 / 3 if b.weather == "Sun" else 1 / 4 if b.weather else 1 / 2
        heal(att, int(att.maxhp * frac))
    elif e == "REST":
        if att.hp < att.maxhp:
            att.hp, att.status, att.sleep, att.toxic = att.maxhp, "slp", 2, 0
    elif e == "SWALLOW":
        heal(att, att.maxhp // 4)
    elif e == "SET_LIGHT_SCREEN":
        if not own_side.screens["Light Screen"]:
            own_side.screens["Light Screen"] = 8 if att.item == "Light Clay" else 5
    elif e == "SET_REFLECT":
        if not own_side.screens["Reflect"]:
            own_side.screens["Reflect"] = 8 if att.item == "Light Clay" else 5
    elif e in WEATHER_OF:
        if b.weather != WEATHER_OF[e]:
            b.weather = WEATHER_OF[e]
            b.weather_turns = 8 if att.item == WEATHER_ROCK.get(b.weather) else 5
    elif e == "TRICK_ROOM":
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
        if b.rng.random() < 1 / (2 ** att.protect_run):
            att.protecting = e == "PROTECT"
            att.enduring = e == "SURVIVE_WITH_1_HP"
            att.protect_run += 1
        else:
            att.protect_run = 0
    elif e == "SET_SUBSTITUTE":
        if not att.sub and att.hp > att.maxhp // 4:
            hurt(b, att, att.maxhp // 4)
            att.sub = att.maxhp // 4
    elif e == "RESET_STAT_CHANGES":
        for m in (att, dfn):
            m.stages = dict.fromkeys(STAGE_KEYS, 0)
    elif e in ("HEAL_STATUS", "CURE_PARTY_STATUS"):
        for m in own_side.mons:
            m.status = None
    elif e == "PREVENT_STATUS":
        own_side.safeguard = 5
    elif e == "TAUNT":
        if not dfn.taunt:
            dfn.taunt = b.rng.randint(3, 5)
    elif e == "FORCE_SWITCH":
        bench = foe_side.bench()
        if bench and not getattr(dfn, "ingrained", False):
            nxt = b.rng.choice(bench)
            switch_in(b, foe_side, foe_side.mons.index(nxt))
    elif e == "FAINT_AND_ATK_SP_ATK_DOWN_2":
        att.hp = 0
        change_stages(dfn, {"atk": -2, "spa": -2})
    elif e == "PASS_STATS_AND_STATUS":
        att.baton = True
    elif e == "ALL_FAINT_3_TURNS":
        # Perish Song: every Pokemon on the field faints at the end of the
        # third turn after this one unless it switches out first.
        for m in (b.p.on_field() + b.b.on_field()):
            if m.alive() and not m.perish and m.ability != "Soundproof":
                m.perish = 4
    elif e == "HIT_IN_3_TURNS":
        pass


def switch_in(b, side, index, slot=0):
    """A Pokemon comes in to a slot: volatile state resets, hazards bite."""
    leaving = side.cur() if slot == 0 else (side.mons[side.active2] if side.active2 is not None else None)
    if leaving is not None:
        for foe in (b.b if side is b.p else b.p).mons:
            if foe.trapped_by == leaving.key:
                foe.trapped_by = None
    if slot == 0:
        side.cur().reset_volatile()
        side.active = index
    else:
        if side.active2 is not None:
            side.mons[side.active2].reset_volatile()
        side.active2 = index
    new = side.mons[index]
    new.reset_volatile()
    # The engine sets fakeOutTurnNumber to the turn count plus one when a
    # Pokemon comes in, and counts its turns from the first decision after:
    # one switched in during a turn reads 0 at the next turn, as does a
    # faint replacement sent in after the end of the turn.
    new.turns_in = -1 if getattr(b, "mid_turn", False) else 0
    new.toxic = 0                # Toxic's count starts again on a switch
    if side.hazards["rocks"]:
        eff = b.st["rock_eff"].get(new.key, 1)
        hurt(b, new, int(new.maxhp * eff / 8))
    grounded = "Flying" not in new.types and new.ability != "Levitate"
    if grounded and side.hazards["spikes"]:
        hurt(b, new, new.maxhp * {1: 1, 2: 1.5, 3: 2}[side.hazards["spikes"]] // 8)
    if grounded and side.hazards["tspikes"]:
        if "Poison" in new.types:
            side.hazards["tspikes"] = 0
        else:
            give_status(b, new, "psn" if side.hazards["tspikes"] == 1 else "tox")
    weather = ABILITY_WEATHER.get(new.ability)
    if weather:
        b.weather, b.weather_turns = weather, 0
    if new.ability in ENTRY_ANNOUNCED:
        reveal(new)
    if new.ability == "Intimidate":
        for foe in (b.b if side is b.p else b.p).on_field():
            if foe.alive() and not stat_drop_blocked(b, foe, {"atk": -1}):
                change_stages(foe, {"atk": -1})


def end_of_turn(b):
    _end_of_turn(b)
    b.mid_turn = False


def _end_of_turn(b):
    for side in (b.p, b.b):
        for m in side.on_field():
            _end_of_turn_mon(b, side, m)
        side.screens = {k: max(0, v - 1) for k, v in side.screens.items()}
        side.tailwind = max(0, side.tailwind - 1)
        side.safeguard = max(0, side.safeguard - 1)
    if b.weather_turns:
        b.weather_turns -= 1
        if b.weather_turns == 0:
            b.weather = b.st.get("base_weather")
    if 0 < b.trick_room < 999:
        b.trick_room -= 1
    b.turn += 1


def _end_of_turn_mon(b, side, m):
    if m.alive():
        if b.weather in ("Sand", "Hail"):
            safe = {"Sand": {"Rock", "Ground", "Steel"}, "Hail": {"Ice"}}[b.weather]
            shield = {"Sand": "Sand Veil", "Hail": "Snow Cloak"}[b.weather]
            if not set(m.types) & safe and m.ability not in (shield, "Magic Guard"):
                hurt(b, m, m.maxhp // 16)
        if m.item == "Leftovers" or (m.item == "Black Sludge" and "Poison" in m.types):
            heal(m, m.maxhp // 16)
        if m.status in ("brn", "psn") and m.ability != "Magic Guard":
            hurt(b, m, m.maxhp // 8)
        if m.status == "tox" and m.ability != "Magic Guard":
            m.toxic += 1
            hurt(b, m, m.maxhp * m.toxic // 16)
        if m.seeded:
            foe = foe_of(b, m)
            amount = m.maxhp // 8
            hurt(b, m, amount)
            if foe.alive():
                heal(foe, amount)
        if m.bound:
            m.bound -= 1
            hurt(b, m, m.maxhp // 16)
        if m.yawn:
            m.yawn -= 1
            if m.yawn == 0:
                give_status(b, m, "slp")
        if m.ingrained and m.alive() and m.hp < m.maxhp:
            gain = m.maxhp // 16
            heal(m, int(gain * 1.3) if m.item == "Big Root" else gain)
        if m.item == "Sitrus Berry" and 0 < m.hp <= m.maxhp // 2:
            heal(m, m.maxhp // 4)
            m.item = None
        if m.item == "Lum Berry" and (m.status or m.confused):
            m.status, m.confused, m.item = None, 0, None
        if m.taunt:
            m.taunt -= 1
        if m.cursed and m.ability != "Magic Guard":
            hurt(b, m, m.maxhp // 4)
        if m.perish:
            m.perish -= 1
            if m.perish == 0:
                m.hp = 0
        m.protecting = False
        m.enduring = False
        m.flinch = False        # a flinch lasts only the turn it is dealt
        m.hit_this_turn = None
        m.turns_in += 1


# ---- the player's policy -----------------------------------------------------------------------

def exp_damage(b, att, dfn, mv):
    """A move's expected damage a turn, for the player's reckoning: the
    middle roll with stages, burn and screens, times accuracy, a two-turn
    move at half."""
    r = b.rolls(att, dfn, mv)
    if r is None:
        return 0.0
    d = b.damage(att, dfn, mv, roll=len(r) // 2) or 0
    acc = 1.0 if mv.acc == 0 else min(1.0, mv.acc / 100)
    if mv.effect in TWO_TURN or mv.effect == "RECHARGE_AFTER":
        d /= 2
    if mv.effect in SELF_KO or mv.effect in ("HIT_FIRST_IF_TARGET_ATTACKING",
                                            "ALWAYS_FLINCH_FIRST_TURN_ONLY", "HIT_IN_3_TURNS"):
        return 0.0
    return d * acc


def best_attack(b, att, dfn):
    usable = [m for m in att.moves if m.damaging() and att.pp.get(m.name, 1) > 0
              and (not att.choice or m.name == att.choice)]
    if not usable:
        return None, 0.0
    return max(((m, exp_damage(b, att, dfn, m)) for m in usable), key=lambda x: x[1])


def exchange(b, me, foe):
    """(turns I need, turns it needs, I move first): the plain exchange."""
    _m, mine = best_attack(b, me, foe)
    _f, theirs = best_attack(b, foe, me)
    t_me = math.ceil(foe.hp / mine) if mine > 0 else 99
    t_foe = math.ceil(me.hp / theirs) if theirs > 0 else 99
    return t_me, t_foe, b.speed(me) > b.speed(foe) if not b.trick_room else b.speed(me) < b.speed(foe)


def wins(t_me, t_foe, first):
    return t_me < t_foe or (t_me == t_foe and first)


def moves_first(b, a, c):
    """Whether a outspeeds c as things stand, Trick Room included."""
    return b.speed(a) < b.speed(c) if b.trick_room else b.speed(a) > b.speed(c)


def after_entry(b, m, foe, hit):
    """For m coming in and taking `hit` on the way: (wins its exchange,
    turns it needs, share of its HP left), or None when the hit faints it."""
    left = m.hp - hit
    if left <= 0:
        return None
    _m, mine = best_attack(b, m, foe)
    _f, theirs = best_attack(b, foe, m)
    tm = math.ceil(foe.hp / mine) if mine > 0 else 99
    tf = math.ceil(left / theirs) if theirs > 0 else 99
    return wins(tm, tf, moves_first(b, m, foe)), tm, left / m.maxhp


def entry_hit(b, foe, m, mv):
    """What m takes coming in on the move the foe chose for the Pokemon it replaces."""
    return exp_damage(b, foe, m, mv) if mv is not None else 0.0


# The player's switching (the Overseer's rules, 2026-09-27). The foe picks
# its move against the Pokemon in front of it, so whatever comes in takes
# that move: a switch-in is judged on it, and a Pokemon that takes it easily
# can carry a teammate in behind it (a pivot). Switches in one battle are
# capped so two answers cannot trade places for ever.
SWITCH_CAP = 14
# Stalling: while the foe's side has a timed effect that turns the exchange
# (screens, Tailwind, a move's Trick Room or weather), or its one threat is
# nearly out of PP, the player trades places between Pokemon that each take
# at most STALL_HIT of their HP from what is aimed at them, for at most
# STALL_CAP turns in a battle.
STALL_HIT = 0.2
STALL_CAP = 12
PP_STALL_MAX = 4


def cleared(b):
    """The field with the foe side's timed effects run out, to compare the
    exchange with; a context that puts everything back."""
    class _Cleared:
        def __enter__(self):
            self.saved = (dict(b.b.screens), b.b.tailwind, b.trick_room, b.weather, b.weather_turns)
            b.b.screens = dict.fromkeys(b.b.screens, 0)
            b.b.tailwind = 0
            if b.trick_room < 999:
                b.trick_room = 0
            if b.weather_turns:
                b.weather, b.weather_turns = b.st.get("base_weather"), 0
            return b

        def __exit__(self, *exc):
            b.b.screens, b.b.tailwind, b.trick_room, b.weather, b.weather_turns = self.saved
    return _Cleared()


def timed_edge(b, me, foe):
    """Turns left on the foe side's timed effects when they turn this
    exchange against the player, else 0."""
    left = max([v for v in b.b.screens.values()] + [b.b.tailwind,
               b.trick_room if b.trick_room < 999 else 0, b.weather_turns])
    if left < 2:
        return 0
    now = exchange(b, me, foe)
    with cleared(b):
        then = exchange(b, me, foe)
    if (wins(*then) and not wins(*now)) or then[0] * 1.5 <= now[0]:
        return left
    return 0


def pp_threat(b, me, foe, pred):
    """The foe's move to drain when it is the one thing beating `me` and
    has few uses left, else None."""
    if pred is None or foe.pp.get(pred.name, 0) > PP_STALL_MAX or foe.pp.get(pred.name, 0) <= 0:
        return None
    t_me, t_foe, first = exchange(b, me, foe)
    if wins(t_me, t_foe, first):
        return None
    others = [exp_damage(b, foe, me, m) for m in foe.moves if m.damaging() and m.name != pred.name
              and foe.pp.get(m.name, 1) > 0]
    theirs = max(others, default=0.0)
    t_foe2 = math.ceil(me.hp / theirs) if theirs > 0 else 99
    return pred if wins(t_me, t_foe2, first) else None


def stall_switch(b, me, foe, pred):
    """A bench Pokemon to trade places with while stalling: it takes at most
    STALL_HIT from the move aimed at `me`, and `me`, coming back, takes at
    most that from what the foe would aim at it. None when there is none."""
    best = None
    for i, m in enumerate(b.p.mons):
        if i == b.p.active or not m.alive() or m.hp * 2 < m.maxhp:
            continue
        hit = entry_hit(b, foe, m, pred)
        back_mv = best_attack(b, foe, m)[0]
        back = entry_hit(b, foe, me, back_mv)
        if hit <= STALL_HIT * m.maxhp and back <= STALL_HIT * me.maxhp and back < me.hp:
            key = hit / m.maxhp + back / me.maxhp
            if best is None or key < best[0]:
                best = (key, i)
    return best[1] if best else None


def pick_switch(b, me, foe, pred):
    """The bench Pokemon to bring in, straight or through a pivot: (index,
    pivot). Straight: it takes `pred` and still wins its exchange. Through a
    pivot C: C takes `pred` for at most a quarter of its HP, and the one
    after it wins, having taken what the foe aims at C."""
    best = None
    for i, m in enumerate(b.p.mons):
        if i == b.p.active or not m.alive():
            continue
        got = after_entry(b, m, foe, entry_hit(b, foe, m, pred))
        if got and got[0]:
            key = (got[1], -got[2])
            if best is None or key < best[0]:
                best = (key, i)
    if best:
        return best[1], False
    for c, pivot in enumerate(b.p.mons):
        if c == b.p.active or not pivot.alive():
            continue
        hit = entry_hit(b, foe, pivot, pred)
        if hit > pivot.maxhp / 4 or hit >= pivot.hp:
            continue
        aimed = best_attack(b, foe, pivot)[0]
        for i, m in enumerate(b.p.mons):
            if i in (b.p.active, c) or not m.alive():
                continue
            got = after_entry(b, m, foe, entry_hit(b, foe, m, aimed))
            if got and got[0]:
                key = (got[1], -got[2])
                if best is None or key < best[0]:
                    best = (key, c)
    return (best[1], True) if best else (None, False)


# Setup when safe (the Overseer, 2026-09-27): a boost is worth its turn when
# the foe needs three or more hits to faint the user after it, up to +2 in
# the attacking stat against a last Pokemon and +4 with more to come; Speed
# counts when the user is slower; a defence boost when the foe's best hits
# that side.
SETUP_CAP = {1: 2}
SETUP_CAP_MORE = 4


def setup_worth(b, me, foe, mv, t_me, safe_turns, first):
    e = mv.effect
    foes_left = len(b.b.alive())
    cap = SETUP_CAP.get(foes_left, SETUP_CAP_MORE)
    best = best_attack(b, me, foe)[0]
    att_stat = "atk" if (best or mv).cat == "Physical" else "spa"
    if e == "MAX_ATK_LOSE_HALF_MAX_HP":
        _f, theirs = best_attack(b, foe, me)
        after = (me.hp - me.maxhp // 2)
        return (att_stat == "atk" and me.stages["atk"] < 2 and after > 0
                and (math.ceil(after / theirs) if theirs > 0 else 99) >= 3
                and (t_me >= 2 or foes_left >= 2))
    ch = SELF_STAGES.get(e) or ({"atk": 1, "def": 1, "spe": -1} if e == "CURSE" and "Ghost" not in me.types else None)
    if not ch or safe_turns < 3 or (t_me < 2 and foes_left < 2):
        return False
    if ch.get(att_stat, 0) > 0 and me.stages[att_stat] < cap:
        return True
    if ch.get("spe", 0) > 0 and not first and me.stages["spe"] < 2:
        return True
    fm = best_attack(b, foe, me)[0]
    guard = "def" if fm and fm.cat == "Physical" else "spd"
    return ch.get(guard, 0) > 0 and me.stages[guard] < 2 and t_me >= 3


def player_choice(b):
    """('move', Move) or ('switch', index)."""
    choice = _player_choice(b)
    if choice[0] == "switch":
        b.p_switches = getattr(b, "p_switches", 0) + 1
    return choice


def _player_choice(b):
    side, me, foe = b.p, b.p.cur(), b.b.cur()
    if me.lock:
        return "move", me.lock[0]
    if me.charging is not None:
        return "move", me.charging
    t_me, t_foe, first = exchange(b, me, foe)
    pred = best_attack(b, foe, me)[0]      # the move the player expects on `me`
    can_switch = getattr(b, "p_switches", 0) < SWITCH_CAP and side.bench()
    # Perish Song about to take it: out it goes, to the best answer left.
    if me.perish and me.perish <= 2 and side.bench():
        idx = player_replacement(b)
        if idx is not None and idx != side.active:
            return "switch", idx
    finishing = t_me == 1 and first
    # Stalling: run out the foe's timed effects or its threat's PP.
    if can_switch and not finishing and getattr(b, "stalled", 0) < STALL_CAP:
        if timed_edge(b, me, foe) or pp_threat(b, me, foe, pred):
            idx = stall_switch(b, me, foe, pred)
            if idx is not None:
                b.stalled = getattr(b, "stalled", 0) + 1
                return "switch", idx
    # Switch when this one loses the exchange and a bench member wins it,
    # straight or through a pivot.
    if can_switch and not wins(t_me, t_foe, first) and not finishing:
        idx, _pivot = pick_switch(b, me, foe, pred)
        if idx is not None:
            return "switch", idx
    # A status or setup move when it turns the exchange: it costs a turn.
    safe_turns = t_foe - (0 if first else 1)
    for mv in me.moves:
        if mv.cat != "Status" or me.pp.get(mv.name, 1) <= 0 or me.taunt:
            continue
        e = mv.effect
        if e in STATUS_OF and can_status(b, foe, STATUS_OF[e]) and safe_turns >= 2:
            st = STATUS_OF[e]
            acc = 1.0 if mv.acc == 0 else mv.acc / 100
            if st == "slp" and acc >= 0.7 and t_me >= 2:
                return "move", mv
            if st == "par" and not first and b.speed(foe) // 4 < b.speed(me) and t_me >= 2:
                return "move", mv
            if st == "brn":
                fm, _d = best_attack(b, foe, me)
                if fm and fm.cat == "Physical" and t_me >= 2:
                    return "move", mv
            if st == "tox" and t_me >= 4:
                return "move", mv
        if (e in SELF_STAGES or e in ("MAX_ATK_LOSE_HALF_MAX_HP", "CURSE")) \
                and setup_worth(b, me, foe, mv, t_me, safe_turns, first):
            return "move", mv
        if e in HEAL_HALF and me.hp * 2 < me.maxhp and safe_turns >= 2:
            return "move", mv
    mv, _d = safe_attack(b, me, foe)
    if mv is None:
        mv = next((m for m in me.moves if me.pp.get(m.name, 1) > 0), me.moves[0])
    # A move that finishes the foe this turn goes first when one exists.
    for m in me.moves:
        if m.damaging() and (not me.choice or m.name == me.choice) and not self_risk(b, me, foe, m):
            r = b.rolls(me, foe, m)
            if r and b.damage(me, foe, m, roll=0) >= foe.hp and (m.pri > 0 or first) \
                    and (m.acc == 0 or m.acc >= 90):
                return "move", m
    return "move", mv


def self_risk(b, me, foe, mv):
    """Whether the move could faint its user: recoil from its top roll (up
    to the foe's HP), or the crash of a miss. A nuzlocke player does not
    trade a Pokemon for a hit when another move will do."""
    if mv.effect in RECOIL and me.ability != "Rock Head":
        r = b.rolls(me, foe, mv)
        top = b.damage(me, foe, mv, roll=len(r) - 1) if r else 0
        return int(min(top or 0, foe.hp) * RECOIL[mv.effect]) >= me.hp
    if mv.effect == "CRASH_ON_MISS" and mv.acc and mv.acc < 100:
        return me.maxhp // 2 >= me.hp
    return False


def safe_attack(b, me, foe):
    """The player's best attack, leaving out any that could faint the user
    while one that cannot still does damage."""
    usable = [m for m in me.moves if m.damaging() and me.pp.get(m.name, 1) > 0
              and (not me.choice or m.name == me.choice)]
    safe = [m for m in usable if not self_risk(b, me, foe, m)]
    pick = safe if any(exp_damage(b, me, foe, m) > 0 for m in safe) else usable
    if not pick:
        return None, 0.0
    return max(((m, exp_damage(b, me, foe, m)) for m in pick), key=lambda x: x[1])


def player_replacement(b):
    """After a faint: the member that wins the exchange best, else the one
    that hurts the foe most."""
    side, foe = b.p, b.b.cur()
    best = None
    for i, m in enumerate(side.mons):
        if not m.alive():
            continue
        t_me, t_foe, first = exchange(b, m, foe)
        key = (0 if wins(t_me, t_foe, first) else 1, t_me, -m.hp)
        if best is None or key < best[0]:
            best = (key, i)
    return best[1] if best else None


# ---- one battle ---------------------------------------------------------------------------------

def run_battle(st, player_keys, boss_keys, rng, flags, trick_room=False):
    """One battle: (the player's Pokemon lost, whether the player won)."""
    pm = [Mon(k, st["pokemon"][k], st["info"][k], st["moves"][k], "p") for k in player_keys]
    held = assign_items(st, player_keys) if "split" in st else {}
    for m in pm:
        m.item = held.get(m.key)
    bm = [Mon(k, st["pokemon"][k], st["info"][k], st["moves"][k], "b") for k in boss_keys]
    b = Battle(st, Side(pm, "p"), Side(bm, "b"), rng, weather=st.get("base_weather"),
               trick_room=trick_room, ai_flags=flags)
    b.p.active = player_replacement(b) or 0
    for side in (b.b, b.p):
        switch_in(b, side, side.active)
    while b.turn < MAX_TURNS:
        if not b.p.alive() or not b.b.alive():
            break
        pa = player_choice(b)
        ba = fightai.choose(b, b.b.cur(), b.p.cur())
        b.mid_turn = True
        me, foe = b.p.cur(), b.b.cur()
        # Switches first.
        if pa[0] == "switch":
            switch_in(b, b.p, pa[1])
        if ba[0] == "switch":
            switch_in(b, b.b, ba[1])
        me, foe = b.p.cur(), b.b.cur()
        order = []
        if pa[0] == "move":
            order.append((me, pa[1], foe))
        if ba[0] == "move":
            order.append((foe, ba[1], me))
        for mon, mv, _t in order:
            mon.chosen = mv
        if len(order) == 2:
            (a, ma, _), (c, mc, _) = order
            if ma.pri != mc.pri:
                order.sort(key=lambda o: -o[1].pri)
            elif not b.faster(a, c):
                order.reverse()
        for i, (mon, mv, _t) in enumerate(order):
            target = foe_of(b, mon)
            first = i == 0 and len(order) == 2
            use_move(b, mon, mv, target, first)
            if getattr(mon, "u_turn", False):
                mon.u_turn = False
                side = b.p if mon.side == "p" else b.b
                if side.bench():
                    idx = player_replacement(b) if side is b.p else fightai.replacement(b, side, foe_of(b, mon))
                    if idx is not None and idx != side.active:
                        switch_in(b, side, idx)
        end_of_turn(b)
        for mon in (b.p.cur(), b.b.cur()):
            if mon.lock:
                mv, left = mon.lock
                mon.lock = (mv, left - 1) if left > 1 else None
                if left <= 1 and not mon.confused and mv.effect == "CONTINUE_AND_CONFUSE_SELF":
                    mon.confused = rng.randint(2, 5)
        # Faints are replaced.
        if b.b.alive() and not b.b.cur().alive():
            idx = fightai.replacement(b, b.b, b.p.cur())
            if idx is not None:
                switch_in(b, b.b, idx)
        if b.p.alive() and not b.p.cur().alive():
            idx = player_replacement(b)
            if idx is not None:
                switch_in(b, b.p, idx)
    lost = sum(1 for m in pm if not m.alive())
    b.hp_lost = 1 - sum(m.hp for m in pm) / sum(m.maxhp for m in pm)
    run_battle.hp_lost = b.hp_lost
    return lost, bool(b.p.alive()) and not b.b.alive()


# ---- a double battle ------------------------------------------------------------------------------

SPREAD = {"ADJACENT_OPPONENTS", "ALL_ADJACENT"}


def foes_of(b, mon):
    return [m for m in (b.b if mon.side == "p" else b.p).on_field() if m.alive()]


def ally_of(b, mon):
    side = b.p if mon.side == "p" else b.b
    return next((m for m in side.on_field() if m is not mon and m.alive()), None)


def targets_of(b, att, mv, chosen):
    """Who a move hits in a double battle: both foes, everyone beside the
    user, a random foe, or the one chosen (the other foe when it is down)."""
    foes = foes_of(b, att)
    if mv.range == "ADJACENT_OPPONENTS":
        return foes
    if mv.range == "ALL_ADJACENT":
        ally = ally_of(b, att)
        return foes + ([ally] if ally else [])
    if mv.range == "RANDOM_OPPONENT":
        return [b.rng.choice(foes)] if foes else []
    if chosen is not None and chosen in foes:
        return [chosen]
    if chosen is not None and (chosen is att or chosen is ally_of(b, att)):
        return [chosen]                  # the AI aimed it at its partner or at itself
    return foes[:1]


def player_choice_doubles(b, me):
    """('move', Move, target) for a player-controlled slot: the move and
    target worth the most, counted as the share of the foes' HP it takes
    (three quarters each for a spread move), a knockout worth half a foe
    more, and HP taken from the ally counted against it. A status move is
    used on the foe it helps most against, by the singles rules."""
    if me.lock:
        return "move", me.lock[0], None
    if me.charging is not None:
        return "move", me.charging, None
    foes = foes_of(b, me)
    ally = ally_of(b, me)
    best = None
    for mv in me.moves:
        if me.pp.get(mv.name, 1) <= 0 or (me.choice and mv.name != me.choice) or (me.taunt and mv.cat == "Status"):
            continue
        if not mv.damaging():
            for f in foes:
                e = mv.effect
                if e in STATUS_OF and can_status(b, f, STATUS_OF[e]) and (mv.acc == 0 or mv.acc >= 70):
                    value = {"slp": 0.9, "par": 0.5 if b.speed(f) > b.speed(me) else 0.2,
                             "brn": 0.6 if any(m.cat == "Physical" for m in f.moves) else 0.1,
                             "tox": 0.4, "psn": 0.2}[STATUS_OF[e]]
                    if best is None or value > best[0]:
                        best = (value, mv, f)
            continue
        choices = [None] if mv.range in SPREAD or mv.range == "RANDOM_OPPONENT" else foes
        for f in choices:
            tl = targets_of(b, me, mv, f)
            scale = 0.75 if len(tl) > 1 else 1.0
            value = 0.0
            for t in tl:
                d = exp_damage(b, me, t, mv) * scale
                share = min(1.0, d / t.hp) if t.hp else 0
                if t is ally:
                    value -= 1.5 * share
                else:
                    value += share + (0.5 if d >= t.hp else 0)
            if best is None or value > best[0]:
                best = (value, mv, f)
    if best is None:
        mv = next((m for m in me.moves if me.pp.get(m.name, 1) > 0), me.moves[0])
        return "move", mv, foes[0] if foes else None
    return "move", best[1], best[2]


def player_replacement_doubles(b, side, owner):
    """A fainted player slot's replacement: the bench member that takes the
    largest share of the foes' HP against what they take of its own."""
    foes = foes_of(b, side.mons[side.active] if side.mons[side.active].alive() else side.mons[0])
    if not foes:
        foes = [m for m in b.b.alive()][:2]
    best = None
    for i, m in enumerate(side.mons):
        if i in (side.active, side.active2) or not m.alive() or getattr(m, "owner", None) != owner:
            continue
        mine = sum(min(1.0, best_attack(b, m, f)[1] / f.hp) for f in foes if f.hp)
        theirs = sum(min(1.0, best_attack(b, f, m)[1] / m.hp) for f in foes if m.hp)
        key = mine - theirs
        if best is None or key > best[0]:
            best = (key, i)
    return best[1] if best else None


def run_doubles(st, player_keys, boss_groups, rng, boss_flags, partner_keys=(), partner_flags=0,
                trick_room=False):
    """One double battle: (the player's Pokemon lost, whether the player won).
    boss_groups is one party (a doubles trainer fills both slots) or two
    (a tag battle, each opponent filling its own slot); partner_keys is a
    partner's party (Barry), driven by its own flags beside the player."""
    pm = [Mon(k, st["pokemon"][k], st["info"][k], st["moves"][k], "p") for k in player_keys]
    held = assign_items(st, player_keys) if "split" in st else {}
    for m in pm:
        m.item = held.get(m.key)
    for m in pm:
        m.owner = "player"
    part = [Mon(k, st["pokemon"][k], st["info"][k], st["moves"][k], "p") for k in partner_keys]
    for m in part:
        m.owner = "partner"
    bm = []
    for g, keys in enumerate(boss_groups):
        for k in keys:
            m = Mon(k, st["pokemon"][k], st["info"][k], st["moves"][k], "b")
            m.owner = g
            bm.append(m)
    b = Battle(st, Side(pm + part, "p"), Side(bm, "b"), rng, weather=st.get("base_weather"),
               trick_room=trick_room, ai_flags=boss_flags[0])
    b.doubles, b.moved = True, set()
    flags_of = {g: boss_flags[min(g, len(boss_flags) - 1)] for g in range(len(boss_groups))}
    flags_of["partner"] = partner_flags
    # The leads.
    b.b.active = 0
    b.b.active2 = len(boss_groups[0]) if len(boss_groups) == 2 else (1 if len(bm) > 1 else None)
    b.p.active = 0
    b.p.active2 = len(pm) if part else (1 if len(pm) > 1 else None)
    for side in (b.b, b.p):
        switch_in(b, side, side.active)
        if side.active2 is not None:
            switch_in(b, side, side.active2, slot=1)

    def flags_for(mon):
        return flags_of.get(mon.owner, boss_flags[0])

    while b.turn < MAX_TURNS and b.p.alive() and b.b.alive():
        b.moved = set()
        acts = []
        for mon in b.p.on_field() + b.b.on_field():
            if not mon.alive():
                continue
            if mon.side == "p" and mon.owner == "player":
                acts.append((mon,) + player_choice_doubles(b, mon)[1:])
            else:
                old = b.ai_flags
                b.ai_flags = flags_for(mon)
                a = fightai.choose_doubles(b, mon)
                b.ai_flags = old
                acts.append((mon, a[1], a[2]))
        for mon, mv, _t in acts:
            mon.chosen = mv
        b.mid_turn = True
        keyed = [(-mv.pri, -b.speed(mon) if not b.trick_room else b.speed(mon), rng.random(), mon, mv, t)
                 for mon, mv, t in acts]
        for *_k, mon, mv, t in sorted(keyed, key=lambda x: x[:3]):
            if not mon.alive():
                continue
            if t is not None and not t.alive():
                t = None
            tl = targets_of(b, mon, mv, t)
            first = bool(tl) and tl[0] not in b.moved
            use_move(b, mon, mv, tl[0] if tl else foe_of(b, mon), first,
                     targets=tl if mv.damaging() else None)
            b.moved.add(mon)
        end_of_turn(b)
        for mon in b.p.on_field() + b.b.on_field():
            if mon.lock:
                mv, left = mon.lock
                mon.lock = (mv, left - 1) if left > 1 else None
                if left <= 1 and not mon.confused and mv.effect == "CONTINUE_AND_CONFUSE_SELF":
                    mon.confused = rng.randint(2, 5)
        # Refill fainted slots from each slot's own party.
        for side in (b.p, b.b):
            for slot, idx in ((0, side.active), (1, side.active2)):
                if idx is None or side.mons[idx].alive():
                    continue
                owner = side.mons[idx].owner
                if side is b.p and owner == "player":
                    nxt = player_replacement_doubles(b, side, owner)
                else:
                    foes = foes_of(b, side.mons[idx])
                    nxt = fightai.replacement(b, side, foes[0] if foes else side.mons[idx], owner=owner)
                if nxt is not None and not side.mons[nxt].alive():
                    nxt = None
                if nxt is not None:
                    switch_in(b, side, nxt, slot=slot)
    lost = sum(1 for m in pm if not m.alive())
    b.hp_lost = 1 - sum(m.hp for m in pm) / sum(m.maxhp for m in pm)
    run_battle.hp_lost = b.hp_lost
    return lost, bool(b.p.alive()) and not b.b.alive()


# ---- preparing a fight ------------------------------------------------------------------------

# A move's downside in play (Ian, 2026-09-27; as learnplan weighs it): the
# strength model already takes recoil and a recharge turn off.
DOWNSIDE = {"UPROAR": 0.5, "CONTINUE_AND_CONFUSE_SELF": 0.6, "USER_SP_ATK_DOWN_2": 0.8,
            "LOWER_OWN_ATK_AND_DEF": 0.85, "DEF_SPD_DOWN_HIT": 0.9, "SPEED_DOWN_HIT": 0.95}
# The status and setup moves the player's policy knows how to use.
POLICY_STATUS = set(STATUS_OF) | set(SELF_STAGES) | HEAL_HALF | {"MAX_ATK_LOSE_HALF_MAX_HP", "CURSE"} \
    | {"SET_REFLECT", "SET_LIGHT_SCREEN", "STEALTH_ROCK", "SET_SPIKES", "TOXIC_SPIKES"}   # screens and hazards, which the lines use


def play_strength(name, types):
    """A move's worth a turn to the player: the strength model (accuracy,
    hits, recoil, a recharge turn) with its downside, same-type at 1.5.
    Charge moves count nothing: the player sets no weather and has no Power
    Herb to fire them in one turn."""
    from . import learnstudy as ls
    mv = move(name)
    if not mv.damaging() or mv.const is None or mv.effect in TWO_TURN or mv.effect in SELF_KO:
        return 0.0
    kind, p = ls.strength(ls.oxide_move(pokedex_moves()[mv.const]))
    if kind != "damage":
        return 0.0
    return p * DOWNSIDE.get(mv.effect, 1.0) * (1.5 if mv.type in types else 1.0)


def player_moves(rec, can_names, tiers, types):
    """Four moves for a side Pokemon from what it can have by the split
    (the capture rule, TMs and tutors): its three attacks worth most in
    play, of different types, and its best status move by Ian's tiers (A
    or better) among those the policy uses, else a fourth attack."""
    damaging = [n for n in can_names if move(n).damaging() and n not in pool.CONDITIONAL
                and play_strength(n, types) > 0]
    ranked = sorted(damaging, key=lambda n: -play_strength(n, types))
    attacks, seen = [], set()
    for n in ranked:
        if move(n).type not in seen:
            attacks.append(n)
            seen.add(move(n).type)
        if len(attacks) == 3:
            break
    status = [n for n in can_names if move(n).cat == "Status" and move(n).effect in POLICY_STATUS
              and tiers.get(n, 0) >= TIERS["B"]]
    status.sort(key=lambda n: -tiers.get(n, 0))
    moves = attacks + [n for n in status[:1] if tiers.get(n, 0) >= TIERS["A"]]
    # Every slot is filled, as a player fills them (the Roark read,
    # 2026-09-30): a Pokemon with fewer than three attack types takes its
    # next best status moves (B or better), then attacks of a type it has.
    rest = [n for n in ranked if n not in attacks]
    for n in [s for s in status if s not in moves] + rest:
        if len(moves) >= 4:
            break
        moves.append(n)
    return moves


# The player's items (Ian, 2026-09-27): never a Life Orb or a Choice item.
# The best offensive items are the type boosters (1.2 times), one of each
# type, where the census finds one by the split; Leftovers and Sitrus
# Berries as the census counts them.
BOOSTER_TYPE = {it: t for t, items in pool.TYPE_ITEMS.items() for it in items}


@functools.lru_cache(maxsize=None)
def player_items(split):
    """{"boosters": {type: item}, "Leftovers": copies, "Sitrus Berry": copies}
    by the split's end: field items and gifts once each, mart items without
    limit."""
    from ..encounters import calc_trainers
    from . import splits as sp
    order = pool.SPLITS

    def upto(s):
        return s in order and order.index(s) <= order.index(split)
    name = calc_trainers._item_name
    finds = collections.Counter()
    for s, _m, it, _how in sp.items():
        if upto(s):
            finds[name(it)] += 1
    for s, _m, it in sp.gifts():
        if upto(s):
            finds[name(it)] += 1
    marts = {name(it) for s, _t, it in sp.marts() if upto(s)}
    boosters = {}
    for t, items in pool.TYPE_ITEMS.items():
        have = [i for i in items if finds.get(i) or i in marts]
        if have:
            boosters[t] = have[0]
    count = lambda i: 99 if i in marts else finds.get(i, 0)
    return {"boosters": boosters, "Leftovers": count("Leftovers"), "Sitrus Berry": count("Sitrus Berry")}


def assign_items(st, team):
    """{key: item} for a team: a booster for a member's main same-type
    attack when that type's booster is in reach and not yet given, else
    Leftovers, else a Sitrus Berry, while copies last; strongest first."""
    stock = player_items(st["split"])
    boosters = dict(stock["boosters"])
    left = {"Leftovers": stock["Leftovers"], "Sitrus Berry": stock["Sitrus Berry"]}
    out = {}
    order = sorted(team, key=lambda k: -sum(st["info"][k]["stats"].values()))
    for k in order:
        types = [t.title() for t in st["info"][k].get("types") or []]
        # Its same-type attacks, best first: the first whose booster is free.
        stab = sorted((m for m in st["moves"][k] if move(m).damaging() and move(m).type in types),
                      key=lambda m: -play_strength(m, types))
        t = next((move(m).type for m in stab if move(m).type in boosters), None)
        if t is not None:
            out[k] = boosters.pop(t)
        elif left["Leftovers"] > 0:
            out[k] = "Leftovers"
            left["Leftovers"] -= 1
        elif left["Sitrus Berry"] > 0:
            out[k] = "Sitrus Berry"
            left["Sitrus Berry"] -= 1
        else:
            out[k] = None
    return out


def _power(name, rec, blob):
    m = blob["moves"].get(name, {})
    bp = m.get("basePower") or m.get("bp") or 0
    return bp * (1.5 if m.get("type") in (blob["poks"].get(rec["species"], {}).get("types") or []) else 1)


# Ian does not rate these (2026-09-27): the instant-death moves and every
# entry hazard but Toxic Spikes and Sticky Web. Dark Void keeps Generation
# 4's accuracy in Oxide, so it reads as A rather than the list's D.
UNRATED = {"Revival Blessing", "Destiny Bond", "Memento", "Healing Wish", "Lunar Dance",
           "Stealth Rock", "Spikes"}
TIER_READINGS = {"Dark Void": "A"}


@functools.lru_cache(maxsize=None)
def status_tiers():
    """{calculator move name: tier rank} from Ian's list
    (docs/oxide/status-move-tiers.md), the unrated moves left out."""
    path = os.path.join(data.ROOT, "docs", "oxide", "status-move-tiers.md")
    by_compact = {re.sub(r"[^a-z0-9]", "", m["name"].lower()): c for c, m in pokedex_moves().items()}
    names = pool._move_names()
    out = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            m = re.match(r"\|\s*(SSS|S|A|B|C|D|F|Useless)\s*\|(.*)\|\s*$", line)
            if not m:
                continue
            for n in (x.strip() for x in m.group(2).split(",")):
                c = by_compact.get(re.sub(r"[^a-z0-9]", "", n.lower()))
                if c in names and n not in UNRATED:
                    out[names[c]] = TIERS.get(TIER_READINGS.get(n, m.group(1)), 0)
    return out


# The League split in two (Ian, 2026-09-27): every fight up to the Elite Four
# is played at the "Barry split" cap of 71, and each Elite Four fight at its
# own ace's level, since Ian levels only to the next fight's ace.
BARRY_SPLIT_CAP = 71
ELITE_FOUR_CAPS = {"aaron": 72, "bertha": 73, "flint": 74, "lucian": 75, "cynthia": 78}


def fight_cap(split, key=None):
    if split != "League":
        return pool.caps()[split]
    return ELITE_FOUR_CAPS.get(key, BARRY_SPLIT_CAP)


def side_at(split, cap, blob):
    """The split's player side with its Pokemon at `cap` rather than the
    split's own: the caps read while the side is built are the split's
    with this one in its place."""
    original = pool.caps
    own = cap == original()[split]
    if not own:
        # species_by_split caches its reading of the caps: read afresh.
        pool.caps = lambda: dict(original(), **{split: cap})
        pool.species_by_split.cache_clear()
    try:
        side = pool.pool(split, blob)
        return side, {p["constant"]: pool.moves_at(p["constant"], split) for p in side}
    finally:
        if not own:
            pool.caps = original
            pool.species_by_split.cache_clear()


# What a run is sure to have (the Overseer, 2026-09-27): the starter (one,
# the player's pick), the gifts and eggs every run is handed, the trades that
# ask for nothing, and the static battles. A giver who hands over one of
# several at random (Riley's egg, the clowns) makes no one species sure.
SURE_HOW = ("starter", "gift", "egg gift", "static battle", "in-game trade")


@functools.lru_cache(maxsize=None)
def sure_catches():
    """{species constant: (split, how)} for the sure Pokemon, each in the
    first split it is had in."""
    locs = pool._location_splits()
    groups = collections.defaultdict(list)
    with open(pool.SOURCES, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["method"] in SURE_HOW:
                groups[(row["location"], row["map_or_file"], row["method"])].append(row)
    rolled = pool.catches()
    out = {}
    for (loc, _file, how), rows in groups.items():
        split = locs.get(loc)
        if not split or (len(rows) > 1 and how != "starter"):
            continue
        if "at random" in rows[0]["conditions"]:
            continue            # the Veilstone clown lists only the roll that is a Pokemon
        if how == "in-game trade" and "trade away SPECIES_NONE" not in rows[0]["conditions"]:
            continue
        for r in rows:
            sp = r["species"]
            # Only what the pool counts by the split's cap (a level-70 static is not).
            if any(h == how and s == split for s, _lv, h in rolled.get(sp, [])):
                if sp not in out or pool.split_index(split) < pool.split_index(out[sp][0]):
                    out[sp] = (split, how)
    return out


def family(species):
    """The first stage of a species' line."""
    return (pool.pre_evolutions().get(species) or [species])[-1]


def prepare(split, parties, weather=None, trick_room=False, cap=None, partners=(), doubles=False,
            given_side=None):
    """Everything a fight's battles read: the strong third of the side, the
    trainer's Pokemon, a partner's teams (keys q0.0 and on), and the
    calculator's rows for every pair in every weather the fight can have;
    in a double battle also each ally's spread moves on its ally."""
    blob = teamscore._blob()
    cap = cap or pool.caps()[split]
    side, can = side_at(split, cap, blob)
    # The strong third by stat total at the cap, as the gauntlet takes it.
    totals = {}
    for p in side:
        bs = blob["poks"].get(p["species"], {}).get("bs") or {}
        totals[p["species"]] = sum(bs.values())
    third = sorted(side, key=lambda p: -totals.get(p["species"], 0))[:max(6, len(side) // 3)]
    # Beside it, what every run has by the split, as far as it evolves.
    owned = {p["constant"] for p in side}
    sure = [sp for sp, (s, _how) in sure_catches().items()
            if pool.split_index(s) <= pool.split_index(split)]
    for p in side:
        c = p["constant"]
        from_sure = any(c == sp or sp in pool.pre_evolutions().get(c, []) for sp in sure)
        last = not any(t in owned for _n, _i, t in pool.evolutions(c))
        if from_sure and last and p not in third:
            third.append(p)
    if BOX_MODE:
        third = side          # a box can hold anything the split's side has
    if given_side is not None:
        # A real save's Pokemon (pboxes.save_records): each keeps its level,
        # nature, IVs, ability and, where the record carries them, its moves.
        third = list(given_side)
    tiers = status_tiers()
    names = pool._move_names()
    pokemon, moves, variants = {}, {}, {}
    for i, p in enumerate(third):
        poks = blob["poks"].get(p["species"], {})
        types = poks.get("types") or []
        can_names = sorted({names[c] for c in can.get(p["constant"], ()) if c in names})
        mv = player_moves(p, can_names, tiers, types)
        if p.get("moves") and given_side is not None:
            # The save's own moves, and with "fill" (a Pokemon lifted to the
            # cap) its empty slots from the moveset rule.
            real = [m for m in p["moves"] if m]
            mv = real + ([m for m in mv if m not in real][:4 - len(real)] if p.get("fill") else [])
        # A caught Pokemon has either regular ability, never the hidden one,
        # and never one that sets or cancels weather (Ian, 2026-09-26: the
        # player never controls weather). A species whose regular slots hold
        # only such abilities takes a stand-in with no effect here or in the
        # calculator, until the ability pass gives it a real one.
        abilities = poks.get("abilities") or {}
        regular = [a for a in dict.fromkeys((abilities.get("0"), abilities.get("1")))
                   if a and a not in NO_WEATHER_ABILITY]
        if given_side is not None and p.get("ability") and p["ability"] not in NO_WEATHER_ABILITY:
            regular = [p["ability"]]
        # Rows without the player's item: items are handed out per team and
        # applied here (assign_items, Battle.damage).
        pokemon[f"p{i}"] = dict(p, moves=mv, item=None, ability=regular[0] if regular else WEATHER_STAND_IN)
        moves[f"p{i}"] = mv
        variants[f"p{i}"] = [f"p{i}"]
        if len(regular) > 1:
            pokemon[f"p{i}~1"] = dict(pokemon[f"p{i}"], ability=regular[1])
            moves[f"p{i}~1"] = mv
            variants[f"p{i}"].append(f"p{i}~1")
    boss_keys = []
    for v, party in enumerate(parties):
        keys = []
        for j, mon in enumerate(party):
            k = f"b{v}.{j}"
            pokemon[k] = mon
            moves[k] = list(mon["moves"])
            keys.append(k)
        boss_keys.append(keys)
    partner_keys = []
    for v, party in enumerate(partners):
        keys = []
        for j, mon in enumerate(party):
            k = f"q{v}.{j}"
            pokemon[k] = mon
            moves[k] = list(mon["moves"])
            keys.append(k)
        partner_keys.append(keys)
    # The weathers the fight can have: its own, its Pokemon's abilities', and
    # every weather move on either side.
    weathers = {pressure.CALC_WEATHER.get(weather, weather) if weather else None}
    for k, mv in moves.items():
        ab = pokemon[k].get("ability")
        if ab in ABILITY_WEATHER:
            weathers.add(ABILITY_WEATHER[ab])
        for name in mv:
            e = move(name).effect
            if e in WEATHER_OF:
                weathers.add(WEATHER_OF[e])
    pairs = []
    pkeys = [k for k in pokemon if k.startswith("p")]
    bkeys = [k for k in pokemon if k.startswith("b")]
    qkeys = [k for k in pokemon if k.startswith("q")]

    def hits(k):
        return [m for m in moves[k] if move(m).damaging()]

    # A trainer's rows carry every damaging move of its own party, not only
    # its own: the post-knockout pick (fightai.replacement, stage 2) costs a
    # candidate's moves as if the Pokemon that just fainted used them, as
    # BattleAI_PostKOSwitchIn does. Extra moves in a row change nothing
    # else, since every lookup is by the move's name.
    def party_hits(k):
        prefix = k.split(".")[0] + "."
        out = []
        for other in moves:
            if other.startswith(prefix):
                out += [m for m in hits(other) if m not in out]
        return out

    def spread(k):
        return [m for m in moves[k] if move(m).damaging() and move(m).range == "ALL_ADJACENT"]
    for w in weathers:
        for a in pkeys + qkeys:
            for d in bkeys:
                pairs.append([a, d, hits(a), w])
                pairs.append([d, a, party_hits(d), w])
        if doubles or partners:
            # An ally's spread move on its ally: the player's and a
            # partner's Pokemon on each other, the trainers' on each other.
            for group in ((pkeys + qkeys), bkeys):
                for a in group:
                    if spread(a):
                        pairs += [[a, d, spread(a), w] for d in group if d != a]
    # Magnitude's power is rolled when it is used (MAGNITUDE_POWERS), so the
    # calculator is asked once per power level, each as its own attacker key
    # ("<key>#m<power>") carrying that power, against every foe it can meet.
    for k in list(pkeys) + list(qkeys):
        if "Magnitude" in moves.get(k, ()):
            for p in MAGNITUDE_POWERS:
                dk = f"{k}#m{p}"
                pokemon[dk] = dict(pokemon[k], move_data={"Magnitude": {
                    "type": "Ground", "category": "Physical", "basePower": p}})
                for w in weathers:
                    for d in bkeys:
                        pairs.append([dk, d, ["Magnitude"], w])
    # The trainer's AI costs a move with BattleSystem_CalcMoveDamage, which
    # knows nothing of the abilities that take a move whole; the calculator's
    # row for such a Pokemon reads 0. So each player Pokemon with one gets a
    # twin with the ability blank, rowed against every trainer Pokemon, for
    # fightai.figure's estimate (Basic refuses the move by its guess at the
    # ability instead).
    ai_twin = {}
    for k in list(pkeys):
        if pokemon[k].get("ability") in AI_BLIND_ABSORBS:
            twin = f"{k}#ai"
            pokemon[twin] = dict(pokemon[k], ability=WEATHER_STAND_IN)
            ai_twin[k] = twin
            for w in weathers:
                for d in bkeys:
                    pairs.append([d, twin, party_hits(d), w])
    out = pressure.run_node(teamscore._blob_path(), {"pokemon": pokemon, "pairs": pairs})
    rows, speed = {}, {}
    for r in out["results"]:
        rows[(r["weather"], r["a"], r["d"])] = r
        speed[(r["weather"], r["a"])] = r["speeds"][0]
        speed[(r["weather"], r["d"])] = r["speeds"][1]
    info = out["pokemon"]
    rock = {k: effectiveness(blob, "Rock", inf.get("types") or []) for k, inf in info.items()}
    # A team holds one Pokemon of each family, and one starter.
    starters = {family(sp) for sp, (_s, how) in sure_catches().items() if how == "starter"}
    group = {}
    for k in variants:
        fam = family(pokemon[k]["constant"])
        group[k] = "starter" if fam in starters else fam
    return {"pokemon": pokemon, "moves": moves, "info": info, "rows": rows, "speed": speed,
            "player": list(variants), "variants": variants, "group": group,
            "bosses": boss_keys, "partners": partner_keys,
            "base_weather": pressure.CALC_WEATHER.get(weather, weather) if weather else None,
            "rock_eff": rock, "trick_room": trick_room, "chart": blob["type_chart"], "split": split,
            "ai_twin": ai_twin}


def effectiveness(blob_or_chart, atk_type, def_types):
    """The type chart's multiplier of an attacking type on a set of types."""
    chart = blob_or_chart.get("type_chart", blob_or_chart)
    out = 1.0
    for t in def_types:
        out *= (chart.get(atk_type) or {}).get(t.title(), 1.0)
    return out


# The planned team (Ian, 2026-09-27): the player prepares for the fight.
# CANDIDATES sixes from the strong third and the sure Pokemon each play
# PRE_RUNS battles; the FINALISTS losing fewest play FINAL_RUNS more, and the
# best of those, by Pokemon lost and then battles won, is the team. One stage
# alone picks lucky teams: ten battles cannot tell a good six from a
# fortunate one. Three candidates in four are drawn at random; the fourth is
# drawn toward the Pokemon that beat most of the trainer's one on one.
CANDIDATES = 80
PRE_RUNS = 10
FINALISTS = 8
FINAL_RUNS = 40


# Ordinary doubles trainers are played as doubles; Ian judged his pairs as
# singles, so the fit turns this off.
PLAY_DOUBLES = True


def variants(st):
    """A tag fight's two opponents are one battle; a rival's starters are
    one battle each."""
    return 1 if st.get("battle") == "tag" else len(st["bosses"])


def battle(st, team, v, rng, flags):
    """One battle of the fight's kind: (Pokemon lost, won)."""
    kind = st.get("battle")
    if kind == "tag":
        partner = rng.choice(st["partners"]) if st.get("partners") else ()
        return run_doubles(st, team, st["bosses"], rng, st["group_flags"], partner_keys=partner,
                           partner_flags=st.get("partner_flags", 0), trick_room=st["trick_room"])
    if kind == "doubles" and PLAY_DOUBLES:
        return run_doubles(st, team, [st["bosses"][v]], rng, [flags], trick_room=st["trick_room"])
    return run_battle(st, team, st["bosses"][v], rng, flags, st["trick_room"])


def _trial(st, team, v, flags, rng, n):
    """(Pokemon lost, battles lost, share of HP lost), each a mean: a team
    that loses nothing is judged by the HP it spends."""
    lost = won = hp = 0
    for _r in range(n):
        l, w = battle(st, team, v, rng, flags)
        lost += l
        won += w
        hp += run_battle.hp_lost
    return lost / n, -won / n, hp / n


def draw(st, keys, rng):
    """The Pokemon for these species, each with one of its regular
    abilities at random, as a catch would have it."""
    return [rng.choice(st.get("variants", {}).get(k, [k])) for k in keys]


def sample_team(st, rng, weights=None):
    """Six of the player's Pokemon, one per family and one starter at most;
    with weights, the heavier ones more likely."""
    keys = list(st["player"])
    if weights:
        keys.sort(key=lambda k: -rng.random() ** (1 / weights.get(k, 1.0)))
    else:
        rng.shuffle(keys)
    team, groups = [], set()
    for k in keys:
        g = st.get("group", {}).get(k, k)
        if g not in groups:
            team.append(k)
            groups.add(g)
        if len(team) == 6:
            break
    return team


def matchups(st, v):
    """{player key: the trainer's Pokemon it beats one on one at full HP,
    plus a half}, the weight a drawn candidate leans on."""
    rng = random.Random(0)
    boss = st["bosses"][v] if st.get("battle") != "tag" else [k for g in st["bosses"] for k in g]
    pm = [Mon(k, st["pokemon"][k], st["info"][k], st["moves"][k], "p") for k in st["player"]]
    bm = [Mon(k, st["pokemon"][k], st["info"][k], st["moves"][k], "b") for k in boss]
    b = Battle(st, Side(pm, "p"), Side(bm, "b"), rng, weather=st.get("base_weather"),
               trick_room=st.get("trick_room"))
    return {m.key: 0.5 + sum(1 for f in bm if wins(*exchange(b, m, f))) for m in pm}


def plan_team(st, v, flags, rng):
    """The six a player prepared for this fight brings."""
    first = []
    weights = matchups(st, v)
    for c in range(CANDIDATES):
        team = draw(st, sample_team(st, rng, weights if c % 4 == 3 else None), rng)
        first.append((_trial(st, team, v, flags, rng, PRE_RUNS), team))
    first.sort(key=lambda x: x[0])
    final = [(_trial(st, team, v, flags, rng, FINAL_RUNS), team) for _k, team in first[:FINALISTS]]
    return min(final, key=lambda x: x[0])[1]


# A realistic box (the Overseer's suggestion, 2026-09-27): what one run's
# route gives by the split, one catch per capture area, from which the
# planned six is chosen. BOXES boxes per fight, the reading's battles
# shared among them.
BOXES = 8


@functools.lru_cache(maxsize=None)
def _capture_areas():
    """[(split, [species by slot])] for every wild table the game rolls,
    and [(split, species, how)] for the scripted catches (one starter)."""
    from . import learnwild
    areas = collections.defaultdict(list)
    for e in learnwild.oxide_encounters():
        areas[(e["area"], e["split"])].append(e["species"])
    scripted = []
    for sp, rows in pool.catches().items():
        for split, _lv, how in rows:
            if how not in ("wild", "surf", "old_rod", "good_rod", "super_rod"):
                scripted.append((split, sp, how))
    return [(s, spp) for (_a, s), spp in areas.items()], scripted


def _final_stage(species, split, rng):
    """As far as the species evolves by the split's cap, a branch at random."""
    seen = {species}
    while True:
        nxt = [t for need, item, t in pool.evolutions(species)
               if t not in seen and pool.reachable(need, item, split)]
        if not nxt:
            return species
        species = rng.choice(nxt)
        seen.add(species)


def random_box(split, rng):
    """One run's catches by the split's end: a catch per wild area reached,
    the starter, and the scripted gifts, trades, fossils and honey trees."""
    order = pool.SPLITS
    areas, scripted = _capture_areas()
    box = []
    for s, spp in areas:
        if s in order and order.index(s) <= order.index(split):
            box.append(_final_stage(rng.choice(spp), split, rng))
    starters = [sp for s, sp, how in scripted if how == "starter"]
    if starters:
        box.append(_final_stage(rng.choice(starters), split, rng))
    for s, sp, how in scripted:
        if how != "starter" and s in order and order.index(s) <= order.index(split) and how != "roamer":
            box.append(_final_stage(sp, split, rng))
    return box


def read_boxed(st, flags_by_party, runs=RUNS, seed=20260927):
    """As read_fight, with each planned six chosen from a realistic box."""
    rng = random.Random(seed)
    by_species = collections.defaultdict(list)
    for k in st["player"]:
        by_species[st["pokemon"][k]["constant"]].append(k)
    reads = []
    for v in range(variants(st)):
        lost_all, hp_all, wins_ = [], [], 0
        for _b in range(BOXES):
            box = [by_species[sp][0] for sp in random_box(st["split"], rng) if by_species.get(sp)]
            if len(box) < 6:
                box = box + rng.sample(st["player"], 6 - len(box))
            sub = dict(st, player=sorted(set(box)))
            team = plan_team(sub, v, flags_by_party[v], rng)
            for _ in range(max(1, runs // BOXES)):
                lost, won = battle(st, team, v, rng, flags_by_party[v])
                lost_all.append(lost)
                hp_all.append(run_battle.hp_lost)
                wins_ += won
        n = len(lost_all)
        reads.append({"losses": statistics.mean(lost_all),
                      "three_plus": sum(1 for x in lost_all if x >= 3) / n,
                      "wipe": sum(1 for x in lost_all if x >= 6) / n,
                      "won": wins_ / n, "hp_lost": statistics.mean(hp_all)})
    return {k: round(statistics.mean(r[k] for r in reads), 3) for k in reads[0]}


def read_fight(st, flags_by_party, runs=RUNS, seed=20260927):
    if BOX_MODE:
        return read_boxed(st, flags_by_party, runs, seed)
    return read_planned(st, flags_by_party, runs, seed)


BOX_MODE = False


def read_planned(st, flags_by_party, runs=RUNS, seed=20260927):
    """Each variant's planned team, then its battles: {"losses",
    "three_plus", "wipe", "won", "teams"}, the variants averaged (a rival
    with a team per starter is met with the one the player's starter
    brings, and the player plans for that one)."""
    rng = random.Random(seed)
    reads, teams = [], []
    for v in range(variants(st)):
        team = plan_team(st, v, flags_by_party[v], rng)
        teams.append([st["pokemon"][k]["species"] for k in team])
        lost_all, hp_all, wins_ = [], [], 0
        for _ in range(runs):
            lost, won = battle(st, team, v, rng, flags_by_party[v])
            lost_all.append(lost)
            hp_all.append(run_battle.hp_lost)
            wins_ += won
        n = len(lost_all)
        reads.append({"losses": statistics.mean(lost_all),
                      "three_plus": sum(1 for x in lost_all if x >= 3) / n,
                      "wipe": sum(1 for x in lost_all if x >= 6) / n,
                      "won": wins_ / n,
                      "hp_lost": statistics.mean(hp_all)})
    out = {k: round(statistics.mean(r[k] for r in reads), 3) for k in reads[0]}
    out["teams"] = teams
    return out


def story(key, runs=RUNS):
    """A story fight's reading. A tag fight is a double battle: each
    opponent fills its own slot from its own party, and Barry fights beside
    the player with one of his partner teams, drawn each battle."""
    fight = next(f for f in data.fights()["fights"] if f["key"] == key)
    ox = data.oxide_trainers()
    trainers = data.fight_trainers("oxide", fight)
    tr_ids = [t["tr_id"] for t in trainers]
    parties = [t["party"] for t in trainers]
    weather = pressure.fight_weather(tr_ids)
    cap = fight_cap(fight["split"], key)
    if fight.get("tag"):
        partners = [ox[p]["party"] for p in fight.get("partner_ids", []) if p in ox]
        st = prepare(fight["split"], parties, weather, bool(fight.get("trick_room")), cap=cap,
                     partners=partners, doubles=True)
        st["battle"] = "tag"
        st["group_flags"] = [t["ai"] for t in trainers]
        st["partner_flags"] = ox[fight["partner_ids"][0]]["ai"] if fight.get("partner_ids") else 0
        return read_fight(st, [st["group_flags"][0]], runs)
    st = prepare(fight["split"], parties, weather, bool(fight.get("trick_room")), cap=cap)
    return read_fight(st, [t["ai"] for t in trainers], runs)


def trainer(tr_id, runs=RUNS, split=None):
    """An ordinary trainer's reading, in the split B6 places it in; a
    doubles trainer plays as doubles unless PLAY_DOUBLES is off."""
    t = data.oxide_trainers()[tr_id]
    split = split or b6.placements()[tr_id]["split"]
    doubles = t.get("battle_type") == "Doubles" and PLAY_DOUBLES and len(t["party"]) > 1
    st = prepare(split, [t["party"]], pressure.fight_weather([tr_id]), cap=fight_cap(split),
                 doubles=doubles)
    if doubles:
        st["battle"] = "doubles"
    return read_fight(st, [t["ai"]], runs)


def split_reading(split, runs=RUNS, out=sys.stdout):
    """Every story fight and placed trainer of a split, timed."""
    import time
    t0 = time.time()
    rows = []
    for f in data.fights()["fights"]:
        if f["split"] == split:
            r = story(f["key"], runs)
            rows.append((f["label"], r))
            print(f"  {f['label']:28} {r}", file=out, flush=True)
    for tr, p in sorted(b6.placements().items()):
        if p["split"] == split:
            r = trainer(tr, runs)
            rows.append((data.oxide_trainers()[tr]["name"], r))
            print(f"  {data.oxide_trainers()[tr]['name']:28} {r}", file=out, flush=True)
    print(f"{split}: {len(rows)} fights in {time.time() - t0:.0f} s", file=out)
    return rows


def main(argv=None):
    import argparse
    # Run as a script this file is __main__, a second copy that fightai does
    # not see; the work goes through the package's copy.
    from . import fightsim as mod
    ap = argparse.ArgumentParser()
    ap.add_argument("fight", nargs="*")
    ap.add_argument("--trainer", type=int, nargs="*", default=[])
    ap.add_argument("--runs", type=int, default=RUNS)
    ap.add_argument("--split", help="read every fight of one split, timed")
    args = ap.parse_args(argv)
    if args.split:
        mod.split_reading(args.split, args.runs)
    for key in args.fight:
        print(key, mod.story(key, args.runs))
    for tr in args.trainer:
        print(tr, data.oxide_trainers()[tr]["name"], mod.trainer(tr, args.runs))
    return 0


# fightai reads this module's effect tables when it is imported, so it comes last.
from . import fightai  # noqa: E402

if __name__ == "__main__":
    sys.exit(main())

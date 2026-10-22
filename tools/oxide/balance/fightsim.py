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
import glob
import json
import math
import os
import random
import re
import statistics
import sys
import tempfile

from ..encounters import calc_export
from . import calc, data, pool, required

RUNS = 200
MAX_TURNS = 80
# Oxide's critical hits, the Generation 7 odds and multiplier
# (src/battle/battle_lib.c sCriticalStageRates, battle_script.c
# ApplyCriticalMul), not Platinum's 1 in 16 and double damage.
CRIT_RATE = {0: 1 / 24, 1: 1 / 8, 2: 1 / 2, 3: 1.0, 4: 1.0}
# The trainers of the game's first battle, which the Route 201 script starts
# with StartFirstBattle (Encounter_NewVsFirstBattle sets
# BATTLE_STATUS_FIRST_BATTLE): no critical hits on either side in it. A
# prepared fight against one carries st["first_battle"].
FIRST_BATTLE = frozenset({"TRAINER_RIVAL_ROUTE_201_PIPLUP", "TRAINER_RIVAL_ROUTE_201_TURTWIG",
                          "TRAINER_RIVAL_ROUTE_201_CHIMCHAR"})
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
                 "contact", "sound", "pp", "const", "reflectable", "protect", "mirror", "snatch", "sure")

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
        self.protect = "CAN_PROTECT" in flags        # MOVE_FLAG_CAN_PROTECT: Protect stops it
        self.mirror = "CAN_MIRROR_MOVE" in flags     # MOVE_FLAG_CAN_MIRROR_MOVE: Mirror Move can copy it
        self.snatch = "CAN_SNATCH" in flags          # MOVE_FLAG_CAN_SNATCH: Snatch can take it
        # Frost Breath's kind and Surging Strikes: its row is a critical hit (row_crit_mult)
        self.sure = self.effect in ("ALWAYS_CRITICAL", "HIT_THREE_TIMES_ALWAYS_CRITICAL")
        self.pp = rec.get("pp") or 10

    def damaging(self):
        return self.cat != "Status"

    def __repr__(self):
        return f"Move({self.name})"


@functools.lru_cache(maxsize=None)
def move(name):
    return Move(name)


# The type boosters, by the type whose moves each raises by a fifth (its
# effectParam of 20 in sTypeBoostingItems, BattleSystem_CalcMoveDamage):
# pool.TYPE_ITEMS' list, and Fairy's two, which element 7 added, the Fairy
# Feather (HOLD_EFFECT_STRENGTHEN_FAIRY) and the Pixie Plate
# (HOLD_EFFECT_ARCEUS_FAIRY). pool.TYPE_ITEMS has no Fairy entry, and until
# 2026-10-21 the census of the player's items (player_items) and the
# battle's fifth (BOOSTER_TYPE) read it alone, so no Fairy booster reached
# a six and a Fairy Feather raised nothing (Ian approved the fix on
# 2026-10-20). Each type's classic booster comes before its Plate, the
# order the census takes them in.
TYPE_BOOSTERS = dict(pool.TYPE_ITEMS, Fairy=["Fairy Feather", "Pixie Plate"])

# The Plates whose type Judgment takes (effect script 268 sets the move's
# type by the holder's HOLD_EFFECT_ARCEUS_*): the sixteen of Platinum, and
# the Pixie Plate, which element 7 added and the script has made Fairy since
# bb4b3021b (2026-10-20). Until then the script left a Pixie Plate's
# Judgment Normal, and so did the simulator; it follows the fix (Ian
# approved it on 2026-10-20).
JUDGMENT_TYPE = {item: t for t, items in TYPE_BOOSTERS.items() for item in items if item.endswith(" Plate")}


@functools.lru_cache(maxsize=None)
def judgment_move(mv, item):
    """Judgment as its holder of `item`, a Plate, uses it: the same move at
    the Plate's type (JUDGMENT_TYPE), as the battle types it, for the
    simulator's own type reads (an immunity's reveal, Flash Fire, a thaw,
    the resist Berries, Color Change) and the trainer's AI's, which types
    it by the Plate too (TrainerAI_MoveType); the calculator's row has the
    Plate's type already. Until 2026-10-20 those reads took it as Normal
    (Ian approved the fix)."""
    c = Move(mv.name)
    c.type = JUDGMENT_TYPE[item]
    return c


# What each effect does beyond its damage. A status move whose effect is not
# here does nothing; a damaging one is a plain hit. fightsim_report counts
# the effects met that are not here.
STATUS_OF = {"STATUS_SLEEP": "slp", "STATUS_PARALYZE": "par", "STATUS_BURN": "brn",
             "STATUS_POISON": "psn", "STATUS_BADLY_POISON": "tox"}
HIT_STATUS = {"BURN_HIT": "brn", "PARALYZE_HIT": "par", "FREEZE_HIT": "frz", "POISON_HIT": "psn",
              "BADLY_POISON_HIT": "tox", "THAW_AND_BURN_HIT": "brn", "HIGH_CRITICAL_POISON_HIT": "psn",
              "HIGH_CRITICAL_BURN_HIT": "brn", "RECOIL_BURN_HIT": "brn", "RECOIL_PARALYZE_HIT": "par",
              "FLINCH_BURN_HIT": "brn", "FLINCH_PARALYZE_HIT": "par", "FLINCH_FREEZE_HIT": "frz",
              "BLIZZARD": "frz", "THUNDER": "par",
              # Bounce's hit (effect script 263) paralyses at the move's
              # chance, as Thunderbolt's does; until 2026-10-15 it never did
              # (Ian approved the fix).
              "BOUNCE": "par",
              # Infernal Parade and Barb Barrage (effect scripts 321, 322).
              "BURN_HIT_DOUBLE_POWER_ON_STATUS": "brn", "POISON_HIT_DOUBLE_POWER_ON_POISONED": "psn",
              # Relic Song and Wicked Torque (effect script 301): sleep at the
              # move's chance (10) through the sleep subscript, as a hit's
              # status; Sheer Force leaves it (not on sSheerForceEffects).
              # Until 2026-10-15 neither ever slept (Ian approved the fix).
              # Relic Song's turn of Meloetta between its forms is relic_song's.
              "SLEEP_HIT": "slp",
              # Ice Burn and Freeze Shock's hit, once charged (TWO_TURN): a burn
              # or a paralysis at the move's chance (30), as an indirect effect
              # (MOVE_SUBSCRIPT_PTR_BURN, _PARALYZE), which Sheer Force leaves.
              "CHARGE_TURN_BURN_HIT": "brn", "CHARGE_TURN_PARALYZE_HIT": "par",
              # Matcha Gotcha (effect script 348, subscript_burn_and_drain_health):
              # a burn at the move's chance (20) on a target left standing,
              # and the drain of DRAIN below either way. Until 2026-10-15 it
              # was a plain hit (Ian approved the fix).
              "RECOVER_HALF_DAMAGE_DEALT_BURN_HIT": "brn",
              # Sandsear Storm (effect script 358): a burn at the move's
              # chance (30) on each target, an indirect effect Sheer Force
              # strips (sSheerForceEffects); it never misses in the rain
              # (RAIN_SURE). Until 2026-10-20 it never burned (Ian approved
              # the fix).
              "SANDSEAR_STORM": "brn",
              # Wildbolt Storm (effect script 357): a paralysis at the move's
              # chance (30), as Sandsear Storm's burn, which Sheer Force
              # strips. Until 2026-10-20 it never paralysed (Ian approved
              # the fix).
              "WILDBOLT_STORM": "par"}
# Dire Claw (effect script 350): Random 2, 0 picks sleep, poison or
# paralysis evenly, and only that one is tried at the move's chance (30),
# through its own subscript and checks, so a target immune to the one
# picked takes none. Sheer Force leaves it (not on sSheerForceEffects).
# Until 2026-10-20 it never gave a status (Ian approved the fix).
STATUS_PICK = {"SLEEP_POISON_PARALYZE_HIT": ("slp", "psn", "par")}
FLINCH_HIT = {"FLINCH_HIT", "FLINCH_BURN_HIT", "FLINCH_PARALYZE_HIT", "FLINCH_FREEZE_HIT",
              "FLINCH_MINIMIZE_DOUBLE_HIT", "FLINCH_DOUBLE_DAMAGE_FLY_OR_BOUNCE",
              "UPPER_HAND",                       # at its 100%, as Fake Out's target flinches
              # Snore (effect script 92) flinches at its 30%, set before its
              # damage; until 2026-10-15 it never did (Ian approved the fix).
              "DAMAGE_WHILE_ASLEEP"}
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
    # Geomancy's second turn (effect script 318, despite the effect's name):
    # Sp. Atk, Sp. Def and Speed two stages each, through the stat-stage
    # subscript, its charge turn in TWO_TURN.
    "CHARGE_TURN_ATK_SP_ATK_SPEED_UP_2": {"spa": 2, "spd": 2, "spe": 2},
}
FOE_STAGES = {
    "ATK_DOWN": {"atk": -1}, "ATK_DOWN_2": {"atk": -2}, "DEF_DOWN": {"def": -1},
    "DEF_DOWN_2": {"def": -2}, "SPEED_DOWN": {"spe": -1}, "SPEED_DOWN_2": {"spe": -2},
    "SP_DEF_DOWN_2": {"spd": -2}, "ACC_DOWN": {"acc": -1}, "EVA_DOWN": {"eva": -1},
    "ATK_DEF_DOWN": {"atk": -1, "def": -1}, "SP_ATK_DOWN_2_OPPOSITE_GENDER": {"spa": -2},
    # Noble Roar and Tearful Look (effect script 362,
    # subscript_atk_sp_atk_down): Attack and Sp. Atk a stage each, one stat
    # at a time, as Tickle's are; a Substitute stops both. Until 2026-10-15
    # they did nothing (Ian approved the fix).
    "TEARFUL_LOOK": {"atk": -1, "spa": -1},
}
# Venom Drench (effect script 361, subscript_atk_sp_atk_speed_down): Attack,
# Sp. Atk and Speed a stage each, only on a poisoned or badly poisoned
# target; the script fails on any other.
VENOM_DRENCH_STAGES = {"atk": -1, "spa": -1, "spe": -1}
HIT_FOE_STAGES = {
    "LOWER_SP_DEF_HIT": {"spd": -1}, "LOWER_DEFENSE_HIT": {"def": -1},
    "LOWER_SPEED_HIT": {"spe": -1}, "LOWER_ACCURACY_HIT": {"acc": -1},
    "LOWER_ATTACK_HIT": {"atk": -1},
    # Snarl, Struggle Bug, Mystical Fire, Skitter Smack and Spirit Break
    # (always), Mist Ball (half the time) and Moonblast (one time in ten):
    # effect script 71 lowers the target's Sp. Atk a stage at the move's
    # chance. Until 2026-10-15 the hit landed and the drop never came (Ian
    # approved the fix).
    "LOWER_SP_ATK_HIT": {"spa": -1},
    # Acid Spray and Lumina Crash (always) and Seed Flare (four times in
    # ten): effect script 271 lowers the target's Sp. Def two stages at the
    # move's chance, which Sheer Force strips (sSheerForceEffects). Until
    # 2026-10-15 the hit landed and the drop never came (Ian approved the
    # fix).
    "LOWER_SP_DEF_2_HIT": {"spd": -2},
    # Bleakwind Storm (effect script 356): each target's Speed falls a stage
    # at the move's chance (30), an indirect effect Sheer Force strips; it
    # never misses in the rain (BattleControllerPlayer_CheckMoveHitOverrides,
    # unless Cloud Nine or Air Lock is out: RAIN_SURE). Until 2026-10-20
    # the hit landed with neither (Ian approved the fix).
    "BLEAKWIND_STORM": {"spe": -1},
}
HIT_SELF_STAGES = {  # (stages, certain)
    "DEF_SPD_DOWN_HIT": ({"def": -1, "spd": -1}, True),
    # Hammer Arm and Ice Hammer (effect script 218): the user's own Speed
    # falls a stage on any hit (ON_HIT, TO_ATTACKER), a Substitute's or a
    # knockout's too, and Sheer Force leaves it, as the effect is not on
    # sSheerForceEffects. Until 2026-10-15 it was a drop on the target at the
    # move's chance (Ian approved the fix).
    "SPEED_DOWN_HIT": ({"spe": -1}, True),
    "LOWER_OWN_ATK_AND_DEF": ({"atk": -1, "def": -1}, True),
    "USER_SP_ATK_DOWN_2": ({"spa": -2}, True),
    "RAISE_ATTACK_HIT": ({"atk": 1}, False), "RAISE_SP_ATK_HIT": ({"spa": 1}, False),
    "RAISE_DEF_HIT": ({"def": 1}, False),
    "RAISE_ALL_STATS_HIT": ({"atk": 1, "def": 1, "spa": 1, "spd": 1, "spe": 1}, False),
    # Flame Charge, Trailblaze and Aqua Step (effect script 285): the user's
    # Speed rises a stage at the move's chance (100), as Metal Claw's Attack
    # does, so a knockout's or a Substitute's hit raises it too and Sheer
    # Force strips it (sSheerForceEffects). Until 2026-10-15 the Speed never
    # rose (Ian approved the fix).
    "RAISE_SPEED_HIT": ({"spe": 1}, False),
    # Clanging Scales (effect script 342, subscript_user_def_down_hit): the
    # user's own Defense falls a stage on any hit (ON_HIT, TO_ATTACKER), a
    # Substitute's or a knockout's too, and Sheer Force leaves it, as the
    # effect is not on sSheerForceEffects. Until 2026-10-15 the Defense never
    # fell (Ian approved the fix).
    "USER_DEF_DOWN_HIT": ({"def": -1}, True),
    # Esper Wing (effect script 368): the user's Speed rises a stage at the
    # move's chance (100), an indirect effect on the user, so a knockout's
    # or a Substitute's hit raises it too; Sheer Force leaves it, as the
    # effect is not on sSheerForceEffects. Its critical stage comes from the
    # effect's name (HIGH_CRITICAL). Until 2026-10-20 the Speed never rose
    # (Ian approved the fix).
    "HIGH_CRITICAL_RAISE_SPEED_HIT": ({"spe": 1}, False),
    # Diamond Storm (effect script 317): the user's Defense rises two stages
    # at the move's chance (50), an indirect effect on the user, so a
    # knockout's or a Substitute's hit raises it too; Sheer Force leaves it,
    # as the effect is not on sSheerForceEffects. Until 2026-10-20 the
    # Defense never rose (Ian approved the fix).
    "RAISE_DEF_2_HIT": ({"def": 2}, False),
    # Zippy Zap (effect script 316): the user's evasion rises a stage at the
    # move's chance (100), an indirect effect on the user, so a knockout's
    # or a Substitute's hit raises it too; Sheer Force leaves it. Its rows
    # are plain hits (calc_export.move_entry). Until 2026-10-20 the evasion
    # never rose and every hit was critical (Ian approved the fix).
    "RAISE_EVA_HIT": ({"eva": 1}, False),
    # Hyperspace Fury (effect script 343, subscript_hyperspace_fury, ON_HIT
    # on its user): its target's protection ends (BREAKS_PROTECT) and the
    # user's own Defense falls a stage, a knockout's or a Substitute's hit
    # too. Until 2026-10-20 the Defense never fell (Ian approved the fix).
    "USER_DEF_DOWN_HIT_REMOVE_PROTECT": ({"def": -1}, True),
    # V-create (effect script 291, subscript_user_def_sp_def_speed_down_hit,
    # ON_HIT on its user): its Speed, Defense and Sp. Def fall a stage each,
    # a knockout's or a Substitute's hit too. Until 2026-10-20 none fell
    # (Ian approved the fix).
    "USER_DEF_SP_DEF_SPEED_DOWN_HIT": ({"spe": -1, "def": -1, "spd": -1}, True),
    # Spin Out (effect script 355, ON_HIT on its user): its Speed falls two
    # stages, a knockout's or a Substitute's hit too. Until 2026-10-20 it
    # never fell (Ian approved the fix).
    "USER_SPEED_DOWN_2_HIT": ({"spe": -2}, True),
}


def self_raise_chance(att, mv):
    """The percent chance of a hit's raise of its own user's stats (the
    HIT_SELF_STAGES that are not certain): the move's chance, doubled for
    a Serene Grace user, as BattleSystem_TriggerSecondaryEffect doubles
    every indirect effect's chance whichever Pokemon it lands on. Until
    2026-10-20 Serene Grace left these alone, so a Togetic's Ancient Power
    raised its stats one time in ten, not two (Ian approved the fix)."""
    chance = mv.chance or 10
    return chance * 2 if att.ability == "Serene Grace" else chance


RECOIL = {"RECOIL_THIRD": 1 / 3, "RECOIL_QUARTER": 1 / 4, "RECOIL_HALF": 1 / 2,
          "RECOIL_BURN_HIT": 1 / 3, "RECOIL_PARALYZE_HIT": 1 / 3,
          "RECOIL_CONFUSE_HIT": 1 / 3}           # Raging Fury (effect 417)
# The abilities that spare their holder a hit's recoil: subscript_recoil_1_2,
# _1_3 and _1_4 each stop at Rock Head and then at Magic Guard (Magic Guard
# added 2026-10-14, Ian approved the fix).
RECOIL_PROOF = frozenset({"Rock Head", "Magic Guard"})
# The move reworks (Ian, 2026-10-06; effects 416 to 420). A two to five hit
# move rolls its hits on Generation 5's spread (BtlCmd_SetMultiHit): five with
# Skill Link, and a Loaded Dice turns a roll of two or three into four or
# five, which leaves four and five at even odds.
MULTI_HIT_ODDS = ((2, 35), (3, 35), (4, 15), (5, 15))
# Fury Cutter and Triple Kick: three hits rising by 10 from the listed power,
# each checking accuracy and the move stopping at the first miss
# (effect_script_0416). The calculator's row is all three hits added up
# (its Oxide profile, since 2026-10-07). Its SetMultiHit flags,
# SYSCTL_TRIPLE_KICK, skip the hit overrides on every hit after the first
# (SYSCTL_SKIP_ACCURACY_OVERRIDES in BattleControllerPlayer_TryMove), so
# No Guard and Lock-On land only the first, and the later ones roll their
# accuracy (accuracy_hits' `later`), as Population Bomb's do (TEN_HITS).
# Until 2026-10-20 No Guard and Lock-On landed all three (Ian approved the
# fix).
RISING_HITS = "HIT_THREE_TIMES_RISING_10"
RISING_COUNT = 3
# Triple Axel (effect script 298) hits the same way at 20, 40 and 60, with
# the same flags: its script adds 20 to a power that starts at 0 for every
# move, so its row too is all three hits added up (the calculator's Oxide
# profile).
AXEL_HITS = "HIT_THREE_TIMES_INCREMENT_BASE_POWER_20"
RISING = frozenset({RISING_HITS, AXEL_HITS})


def rising_powers(mv):
    """The powers of a rising move's three hits: Fury Cutter and Triple Kick
    from the listed power up by 10 a hit, Triple Axel 20, 40 and 60."""
    if mv.effect == AXEL_HITS:
        return [20, 40, 60]
    p = max(1, mv.power)
    return [p + 10 * i for i in range(RISING_COUNT)]
HEAL_HALF = {"RESTORE_HALF_HP", "HEAL_HALF_REMOVE_FLYING_TYPE"}
# The share of its damage a draining move restores: half (Giga Drain, Dream
# Eater, Horn Leech), three quarters (Draining Kiss, Oblivion Wing).
DRAIN = {"RECOVER_HALF_DAMAGE_DEALT": 1 / 2, "RECOVER_DAMAGE_SLEEP": 1 / 2,
         "RECOVER_THREE_QUARTERS_DAMAGE_DEALT": 3 / 4,
         # Matcha Gotcha: subscript_burn_and_drain_health ends in the half
         # drain, a knockout's too (its burn is in HIT_STATUS).
         "RECOVER_HALF_DAMAGE_DEALT_BURN_HIT": 1 / 2}
TWO_TURN = {"FLY", "DIG", "DIVE", "BOUNCE", "SHADOW_FORCE", "CHARGE_TURN_HIGH_CRIT", "CHARGE_TURN_HIGH_CRIT_FLINCH",
            "CHARGE_TURN_DEF_UP", "SOLAR_BEAM", "SKIP_CHARGE_TURN_IN_SUN",
            "CHARGE_TURN_SP_ATK_UP", "CHARGE_TURN_SP_ATK_UP_RAIN_SKIPS",  # Meteor Beam, Electro Shot
            # Geomancy (effect script 318): a turn absorbing power, or none
            # with a Power Herb, and then two stages each of Sp. Atk, Sp. Def
            # and Speed (SELF_STAGES). Until 2026-10-20 it did nothing (Ian
            # approved the fix).
            "CHARGE_TURN_ATK_SP_ATK_SPEED_UP_2",
            # Ice Burn and Freeze Shock (effect scripts 364 and 363): a turn
            # charging, or none with a Power Herb, then the hit and its burn
            # or paralysis (HIT_STATUS). Until 2026-10-20 each hit every turn
            # with no status (Ian approved the fix).
            "CHARGE_TURN_BURN_HIT", "CHARGE_TURN_PARALYZE_HIT"}
INVULNERABLE = {"FLY", "DIG", "DIVE", "BOUNCE", "SHADOW_FORCE"}
SELF_KO = {"HALVE_DEFENSE", "EXPLOSION", "FAINT_AND_ATK_SP_ATK_DOWN_2"}
FUTURE_SIGHT = "HIT_IN_3_TURNS"                 # Future Sight and Doom Desire
WEATHER_OF = {"WEATHER_RAIN": "Rain", "WEATHER_SUN": "Sun", "WEATHER_SANDSTORM": "Sand",
              "WEATHER_HAIL": "Hail"}
ABILITY_WEATHER = {"Drizzle": "Rain", "Drought": "Sun", "Sand Stream": "Sand", "Snow Warning": "Hail"}
# The abilities no obtainable Pokemon keeps in a regular slot (Ian, 2026-09-26),
# and the stand-in the player's side takes when both its regular slots held one.
NO_WEATHER_ABILITY = set(ABILITY_WEATHER) | {"Cloud Nine", "Air Lock"}
WEATHER_STAND_IN = "Pressure"
# The abilities Neutralizing Gas leaves on (BattleSystem_NeutralizingGasSuppresses):
# another holder's gas, and those Generation 9 marks as impossible to suppress.
GAS_PROOF = {"Neutralizing Gas", "Multitype", "Zen Mode", "Stance Change", "Shields Down", "Schooling",
             "Disguise", "Battle Bond", "Power Construct", "Comatose", "RKS System", "Gulp Missile",
             "Ice Face", "As One (Glastrier)", "As One (Spectrier)", "Zero to Hero", "Tera Shift"}
# The abilities the battle applies itself as it runs, which prepare() asks
# the calculator to leave off its rows and Speeds (its page counts every
# ability as active from the start). Unburden: the engine doubles its
# holder's Speed only once the item it came in with is gone
# (BattleSystem_CompareBattlerSpeed reads canUnburden and an empty hand),
# which Battle.speed does, where the calculator doubled it from the first turn.
# Intimidate: the engine takes one Attack stage off each foe on the field as
# its holder comes in, and none off a foe that comes in later
# (intimidate_foes), where the calculator took a stage off every physical
# hit into the holder, at any time and on top of the battle's own stage.
# Download: the engine raises one stat a stage as its holder comes in, from
# the foes then on the field (download), where the calculator raised the
# stat in each row by that row's defender. Plus and Minus: the engine
# raises a special move only beside a partner with either (plus_minus), where
# the calculator raised it in every row.
CALC_ABILITY_OFF = frozenset({"Unburden", "Intimidate", "Download", "Plus", "Minus"})


# ---- genders (Ian, 2026-10-03) -------------------------------------------------------------

@functools.lru_cache(maxsize=None)
def _ratio_values():
    out = {}
    with open(os.path.join(data.ROOT, "generated", "gender_ratios.txt")) as fh:
        for line in fh:
            name, _eq, val = line.partition("=")
            if val.strip():
                out[name.strip()] = int(val)
    return out


@functools.lru_cache(maxsize=None)
def gender_ratio(constant):
    """A species' gender ratio byte: 0 male only, 254 female only, 255
    genderless, otherwise a personality whose low byte is below it is
    female (SpeciesData_GetGenderOf)."""
    path = os.path.join(data.ROOT, "res", "pokemon", constant[len("SPECIES_"):].lower(), "data.json")
    with open(path) as fh:
        return _ratio_values()[json.load(fh)["gender_ratio"]]


def gender_from_byte(ratio, byte):
    """The gender a personality's low byte gives a species: "M", "F", or None
    for a genderless one."""
    if ratio == 255:
        return None
    if ratio == 254:
        return "F"
    if ratio == 0:
        return "M"
    return "F" if ratio > byte else "M"


def rolled_gender(constant, seed):
    """A box member's gender, rolled once from a fixed seed by its species'
    ratio, as the box's natures were rolled (Ian, 2026-10-03)."""
    return gender_from_byte(gender_ratio(constant), random.Random(f"gender / {seed}").randrange(256))


@functools.lru_cache(maxsize=None)
def class_genders():
    """{trainer class: "M" or "F"} from the game's own table
    (include/data/trainer_class_genders.h)."""
    out = {}
    with open(os.path.join(data.ROOT, "include", "data", "trainer_class_genders.h")) as fh:
        for line in fh:
            m = re.match(r"\s*\[(TRAINER_CLASS_\w+)\]\s*=\s*GENDER_(MALE|FEMALE)", line)
            if m:
                out[m.group(1)] = "M" if m.group(2) == "MALE" else "F"
    return out


def trainer_gender(constant, trainer_class, gender, ability):
    """A trainer's Pokemon's gender as TrainerData_BuildParty makes it: a
    gender the trainer file names is kept (sub_02074128); otherwise the
    personality's low byte is 120 for a female trainer class and 136 for a
    male one, its lowest bit set by an ability-slot request, and compared
    with the species' ratio (TrainerMon_PersonalityLowByte)."""
    ratio = gender_ratio(constant)
    if gender in ("male", "female"):
        return gender_from_byte(ratio, 255 if gender == "male" else 0)
    low = 120 if class_genders().get(trainer_class) == "F" else 136
    if ability == 1:
        low &= ~1
    elif ability == 2:
        low |= 1
    return gender_from_byte(ratio, low)


def _gender_of(rec):
    """A record's gender: as it names it ("M", "F", "male", "female", or None
    for a genderless species), else rolled once from the record itself."""
    if "gender" in rec:
        return {"male": "M", "female": "F", "M": "M", "F": "F"}.get(rec["gender"])
    if rec.get("constant"):
        return rolled_gender(rec["constant"], f"{rec['constant']} / {rec.get('label') or rec.get('species')}")
    return None


# ---- the Pokemon and the field -----------------------------------------------------------

class Mon:
    """One Pokemon in a battle."""

    # While Neutralizing Gas has its ability off, the ability waits here and
    # `ability` reads None (gas_update); None while the gas leaves it alone.
    gas_stash = None
    # Whether the battle has changed its types or ability (set_types,
    # set_ability, suppress, forecast), so the reads that follow such a
    # change (form_key, the search's keys) need look no further otherwise.
    formed = False
    # Whether Knock Off took its item (knockedOffItemsMask, kept by party
    # slot through switching): its slot can neither steal an item with
    # Thief or Covet nor swap one with Trick.
    knocked_off = False
    # Stockpile's count, up to three (moveEffectsData.stockpileCount), and
    # the Defense and Sp. Def stages it raised (stockpileDefBoosts and
    # stockpileSpDefBoosts), which Spit Up and Swallow give back; left on the
    # class while 0, and cleared when it leaves.
    stockpile = 0
    stockpile_def = 0
    stockpile_spd = 0
    # Imprison: whether this Pokemon imprisons (MOVE_EFFECT_IMPRISON), whether
    # a foe's Imprison has been tried on it (MOVE_EFFECT_IMPRISONED, which
    # the trainer's AI reads), and the moves a standing imprisoner's
    # Imprison seals for it (Move_Imprisoned); all cleared when it leaves.
    imprisoning = False
    imprisoned = False
    sealed = frozenset()
    # Whether this stay has set one of the rarer states below (Minimize's
    # mark, Charge, Lock-On's hold, Foresight, Smack Down, Mirror Move's
    # record, Mimic's copy, Throat Chop's hold), so the search's keys, the
    # rows' twins and the turn's end need look at them only then; cleared
    # with them when it leaves.
    rare = False
    # A player's Pokemon that knows Judgment and holds a Plate: the key of
    # its twin rowed with Judgment at the Plate's type (hold, plate_key),
    # which Battle.row reads for Judgment; left on the class while None.
    plated = None
    # A player's Arceus with Multitype holding a Plate (hold): the Plate's
    # type, as a one-item tuple, which is its type for the whole battle
    # (Battler_MonType); its rows are its twin's of that form (form_key,
    # through the battle's form_twin), kept through switching since its
    # party record keeps the Plate. Left on the class while None, and so
    # for a trainer's, whose record is in its Plate's form already
    # (plate_form).
    plate_types = None
    # Minimize's mark (MOVE_EFFECT_MINIMIZE), which Stomp and Steamroller
    # double on; cleared when it leaves.
    minimized = False
    # Smack Down's mark (MOVE_EFFECT_SMACKED_DOWN): brought to the ground
    # until it leaves, its Levitate off and its Flying type no shield
    # against Ground moves (grounded).
    smacked = False
    # Foresight and Odor Sleuth (VOLATILE_CONDITION_FORESIGHT): its raised
    # evasion stops counting, and Normal and Fighting moves meet its Ghost
    # type; cleared when it leaves.
    foresight = False
    # Miracle Eye (MOVE_EFFECT_MIRACLE_EYE): its raised evasion stops
    # counting, and Psychic moves meet its Dark type; cleared when it leaves.
    miracle_eye = False
    # Water Sport (MOVE_EFFECT_WATER_SPORT): while it stands on the field
    # every Fire move's power is halved (sport_half); cleared when it
    # leaves, and handed on by Baton Pass.
    water_sport = False
    # Mud Sport (MOVE_EFFECT_MUD_SPORT): while it stands on the field every
    # Electric move's power is halved (sport_half); cleared when it leaves,
    # and handed on by Baton Pass.
    mud_sport = False
    # Lock-On and Mind Reader: on the Pokemon held, the turns left
    # (MOVE_EFFECT_LOCK_ON, 2 when used) and the holder's key
    # (lockOnTarget); cleared when it leaves.
    locked_on = 0
    lock_on_by = None
    # Charge's turns (MOVE_EFFECT_CHARGE with chargedTurns): 2 when used, one
    # off at each turn's end, its Electric moves at twice the power while
    # it runs; cleared when it leaves.
    charged = 0
    # Mirror Move: the last move with MOVE_FLAG_CAN_MIRROR_MOVE whose attack
    # message showed with this Pokemon its target (moveCopied), kept only
    # for a Pokemon that knows Mirror Move (mirror_user); cleared when it or
    # a foe comes in.
    mirror = None
    mirror_user = False
    # Mimic: the move list and Mimic's PP as they stood before it copied a
    # move into its slot (mimickedMoveSlot), brought back as it leaves;
    # None while it has copied nothing.
    mimicked = None
    # Magic Coat's turn flag (turnFlags.magicCoat): the first move with
    # MOVE_FLAG_CAN_MAGIC_COAT aimed at it this turn is turned back on its
    # user (coat_bounces); gone with the turn.
    magic_coat = False
    # Power Trick (MOVE_EFFECT_POWER_TRICK): its Attack and Defense stats
    # have changed places, so its rows come from its twin with the two
    # swapped (trick_key); a second use puts them back. Cleared when it
    # leaves, and handed on by Baton Pass.
    power_trick = False
    # Bide (VOLATILE_CONDITION_BIDE): the uses of storing it has left (2 as
    # it starts), and the HP the moves aimed at it have taken meanwhile
    # (storedDamage); cleared when it leaves.
    bide = 0
    bide_damage = 0
    # Transform (VOLATILE_CONDITION_TRANSFORM): whether it has turned into a
    # copy of another Pokemon, that Pokemon's key, whose rows its hits read
    # where prepare() has them (Battle.row), and its own moves and PP as they
    # stood, which come back as it leaves; cleared when it leaves.
    transformed = False
    transform_key = None
    transformed_from = None
    # Me First: the move it took is running at half again its damage
    # (moveEffectsData.meFirst); cleared as that move ends (use_move).
    me_first = False
    # Embargo's turns left on it (moveEffectsData.embargoTurns, which the
    # trainer's AI reads); while they run its held item does not work
    # (Battler_HeldItem), and waits in item_off (lock_item); cleared when it
    # leaves, and handed on by Baton Pass.
    embargo = 0
    # A held item that does not work for now, under Embargo or Magic Room
    # (lock_item): the item waits here, and `item` reads None, so every item
    # effect stops; the moves that take, swap or burn the item itself reach
    # it here (raw_item_op). None while its item works.
    item_off = None
    # Whether Magic Room has caught it on the field (roomed until the room
    # ends or it leaves).
    roomed = False
    # Guard Split and Power Split (subscript_guard_split, _power_split): the
    # raw stats the battle has averaged, {stat: value}, in place of its own
    # (raw_stat), until it leaves; None while nothing has been averaged.
    split = None
    # Healing Wish: its user has fainted to it and the turn now sends in and
    # heals its replacement (wish_comes_true); cleared as that is done.
    wished = False
    # Throat Chop's hold on its target's sound moves (OXIDE_MON_THROAT_CHOP):
    # 2 when the hit lands, one off at each turn's end, so it lasts the rest
    # of this turn and all of the next; cleared when it leaves.
    throat_chop = 0
    # Grudge (MOVE_EFFECT_GRUDGE): set by the move until its user next tries
    # to act or leaves, under the rare flag (grudge).
    grudge = False
    # Snatch (TurnFlags.snatching): it waits this turn to take the next move
    # Snatch may take (snatched); a turn flag, cleared with the turn.
    snatching = False
    # Sky Drop (OXIDE_MON_FLAG_SKY_DROP_HELD): the key of the Sky Drop user
    # holding it in the air, or None; it does nothing and cannot switch
    # while held (sky_held). Under the rare flag.
    sky_holder = None
    # Octolock (OXIDE_MON_FLAG_OCTOLOCKED): held as Mean Look holds it, and
    # a stage of Defense and Sp. Def lost at each turn's end, under the rare
    # flag (octolock).
    octolocked = False
    # Whether it holds anything but the item its rows were made with since
    # a move took, swapped or spent its item, so its rows come from its item
    # twin (mark_unheld, Battle.row); kept through switching, as the item's
    # loss is. Only a trainer's Pokemon has a twin.
    unheld = False
    # Meloetta's Pirouette form, which a Relic Song that hit turns it into
    # and out of (relic_song): its rows and Speed are its Pirouette twin's,
    # its types and stats that form's, and its Aria types and stats wait in
    # `aria`; under the rare flag, and back to Aria as it leaves.
    pirouette = False
    aria = None
    # Autotomize (ReduceWeight): how many times this stay has taken 100 kg
    # off its weight, which comes back from its species as it next comes
    # in; under the rare flag (autotomize, weight_now).
    lightened = 0
    # The turn this Pokemon came in by its side's own choice to switch, for
    # Bolt Beak and Fishious Rend (beak_doubles); set by the turn as it
    # switches, None before.
    switched_turn = None
    # Laser Focus (MOVE_EFFECT_LASER_FOCUS): its count, 2 when used, one
    # off at each turn's end, so its next turn's moves land critical while
    # it stands at 1 or more (laser_focus); under the rare flag, cleared as
    # it leaves.
    laser_focus = 0
    # Soul Heart (soul_heart): how many other Pokemon of the battle were
    # down when it was last looked at, set as it comes in, so each later
    # faint counts once; kept only in a fight with a Soul Heart holder
    # (st["soul_heart"]).
    soul_seen = 0
    # Helping Hand (turnFlags.helpingHand): its partner's Helping Hand has
    # raised its moves' power by half for the rest of the turn
    # (helping_hand); a turn flag, cleared as the next double-battle turn
    # starts. Left on the class while False.
    helped = False
    # Every Pokemon made by __init__ sets these in its own record (here and
    # in reset_volatile). The same values stand on the class as well, so the
    # search's keys (perfectline.mon_key, _ai_mon) can read them directly
    # rather than through getattr with a default, which costs more; a read
    # gives the value getattr's default gave on a record without them.
    heal_block = 0
    salted = False
    disabled = None
    disabled_turns = 0
    nightmare = False
    encore = None
    encore_turns = 0
    protean_type = None
    protean_used = False
    last_resort = False
    last_resort_count = 0
    ate_berry = False
    belch = False
    # Likewise for the trainer's AI, which reads these for every move it
    # scores (fightai.ability_of, check_ability, invalid).
    suppressed = False
    revealed = None
    tormented = False

    def __init__(self, key, rec, info, moves, side):
        self.key, self.side = key, side
        self.species = rec.get("species")
        self.level = rec.get("level") or 50
        self.maxhp = info["hp"]
        self.hp = self.maxhp
        self.stats = info["stats"]
        self.types = [t.title() for t in info.get("types") or []]
        self.base_types = list(self.types)          # its own types, which a switch brings back (Protean)
        self.ability = info.get("ability") or rec.get("ability")
        self.item = info.get("item") or rec.get("item")
        self.moves = [move(m) for m in moves][:4]
        if self.item in JUDGMENT_TYPE:
            # Judgment hits with its Plate's type (effect script 268), which
            # every type read of the battle and of the trainer's AI then
            # sees (judgment_move).
            self.moves = [judgment_move(m, self.item) if m.effect == "JUDGEMENT" else m for m in self.moves]
        self.pp = {m.name: m.pp for m in self.moves}
        # Whether it knows a move whose rule reads its own history, for the
        # keys that must tell such histories apart (perfectline.mon_key and
        # _ai_mon): Last Resort reads the moves used since it came in, Belch
        # whether it has eaten a Berry this battle.
        self.last_resort = any(m.effect == "FAIL_IF_NOT_USED_ALL_OTHER_MOVES" for m in self.moves)
        self.belch = any(m.const == "MOVE_BELCH" for m in self.moves)
        if any(m.effect == "COPY_MOVE" for m in self.moves):
            self.mirror_user = True      # its record of the moves aimed at it counts (mirror)
        # A Berry it ate this battle (berryEatenMask, kept by party slot, so
        # through switching), which Belch needs and the trainer's AI reads.
        self.ate_berry = False
        self.ivs = rec.get("ivs") or {}
        self.gender = _gender_of(rec)    # "M", "F" or None (genderless): Attract, Cute Charm
        self.recycle = None              # the item it last used up, for Recycle
        self.status, self.sleep, self.toxic = None, 0, 0
        self.reset_volatile()

    def reset_volatile(self):
        self.stages = dict.fromkeys(STAGE_KEYS, 0)
        if self.stockpile:
            self.stockpile = self.stockpile_def = self.stockpile_spd = 0
        if self.imprisoning or self.imprisoned or self.sealed:
            self.imprisoning, self.imprisoned, self.sealed = False, False, frozenset()
        if self.rare:
            # oxideFlags (Throat Chop) are cleared as it leaves, and so are
            # moveEffectsMask (Minimize, Charge, Lock-On, Smack Down),
            # statusVolatile (Foresight) and moveCopied (Mirror Move); a Baton
            # Pass hands on the Lock-On hold alone (baton_state).
            self.throat_chop = self.charged = self.locked_on = 0
            self.minimized = self.foresight = self.smacked = self.miracle_eye = self.water_sport = False
            self.mud_sport = False
            self.power_trick = False
            self.split = None            # the battle's averaged stats go as it leaves
            if self.item_off is not None:
                self.item, self.item_off = self.item_off, None     # its party record holds the item
            self.embargo, self.roomed = 0, False
            self.bide = self.bide_damage = 0
            if self.transformed_from is not None:
                # The party record keeps its own moves and their PP
                # (BattleMon_CopyToParty skips a transformed Pokemon's), so
                # they come back; its types and ability come back below.
                self.moves, self.pp = self.transformed_from
            self.transformed, self.transform_key, self.transformed_from = False, None, None
            self.lock_on_by = self.mirror = None
            if self.mimicked is not None:
                # The party record still holds Mimic, with the PP its use left
                # it (BattleMon_CopyToParty skips a mimicked slot), so it comes
                # back.
                moves, pp = self.mimicked
                self.pp = {k: v for k, v in self.pp.items() if any(m.name == k for m in moves)}
                self.pp["Mimic"] = pp
                self.moves, self.mimicked = moves, None
            self.grudge = False          # Grudge goes with moveEffectsMask
            self.octolocked = False      # and Octolock with oxideFlags
            self.sky_holder = None       # and a Sky Drop's hold
            self.lightened = 0           # and its weight comes back from its species (autotomize)
            self.laser_focus = 0         # and Laser Focus goes with moveEffectsMask
            if self.pirouette:
                # Meloetta leaves the field as Aria (TryRestoreStatusOnSwitch
                # writes the form back to its party record).
                self.types, self.stats = self.aria
                self.pirouette, self.aria = False, None
            self.rare = False
        self.stat_raised = False         # a stage rose this turn (Burning Jealousy)
        self.heal_block = 0              # Heal Block's turns left
        self.rollout = 0
        self.curled = False
        self.confused = 0
        self.flinch = False
        self.seeded = False
        self.salted = False           # Salt Cure: loses HP at each turn's end until it leaves
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
        # Disable: the move it cannot choose or use, and the turn ends left
        # on the count (moveEffectsData.disabledMove and disabledTurns).
        self.disabled = None
        self.disabled_turns = 0
        self.nightmare = False           # Nightmare: a quarter of its HP each turn's end while it sleeps
        # Encore: the move it is locked into, and the turn ends left on the
        # count (moveEffectsData.encoredMove and encoredTurns).
        self.encore = None
        self.encore_turns = 0
        self.roosting = False            # Roost: its Flying type meets no move until the turn ends
        # Protean and Libero: once a stay on the field the user takes its
        # move's type alone; the type it took, and whether it has.
        # Leaving the field brings back the types Protean took away, and any
        # other type or ability the battle changed (set_types, set_ability,
        # suppress), as the engine reloads both from the party record when a
        # Pokemon comes back in (BattleSystem_InitBattleMon).
        if getattr(self, "protean_type", None) is not None or getattr(self, "retyped", False):
            self.types = list(self.base_types)
        self.protean_type = None
        self.protean_used = False
        self.retyped = False             # its types are the battle's, not its own
        # The types its rows must now be read with (form_key), when a move or
        # an ability other than Protean and Forecast changed them; None for
        # its own rows.
        self.row_types = None
        if getattr(self, "suppressed", False):
            self.ability = self.suppress_stash
        # Gastro Acid and Core Enforcer: its ability reads as none until it
        # leaves (MOVE_EFFECT_ABILITY_SUPPRESSED), and waits here meanwhile.
        self.suppressed, self.suppress_stash = False, None
        if getattr(self, "ability_was", None) is not None:
            self.ability = self.ability_was[0]
        # The ability it came in with, kept as a one-item tuple once the
        # battle has written another (set_ability); None while unchanged.
        self.ability_was = None
        self.traced = False              # Trace has gone off this stay (traceAnnounced)
        self.camouflaged = False         # Camouflage has retyped it (MOVE_EFFECT_CAMOUFLAGE)
        self.formed = False
        if self.plate_types is not None:
            # A player's Arceus keeps its Plate's form through switching
            # (Battler_MonType reads the held Plate at every read), so its
            # rows stay its twin's of that form (hold).
            self.row_types, self.formed = self.plate_types, True
        self.last = None
        self.turns_in = 0
        self.hit_this_turn = None        # (category, damage) of the last hit taken this turn
        self.hurt_this_turn = False      # HP lost to anything but a hit this turn (Assurance)
        self.last_hit_by = None          # the move last aimed at it since it last acted
        self.last_hit_type = None        # that move's type as the battle recorded it (Weather Ball)
        self.crit_stage = 0
        # A binding move's count (VOLATILE_CONDITION_BIND): set to 3 to 6, 6
        # with a Grip Claw (subscript_bind_start's Random 3, 3), it falls by
        # one each turn's end, which costs HP while it stays above 0; and the
        # binder's key (bindTarget), whose leaving frees it.
        self.bound = 0
        self.bound_by = None
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
        self.aqua_ring = False           # a sixteenth back at each turn's end
        self.magnet_rise = 0             # Magnet Rise's turns left: Ground moves fail on it
        self.tormented = False           # Torment: it cannot pick the move it used last
        self.destiny_bond = False        # Destiny Bond: a foe whose move faints it faints too
        self.infatuated = None           # the key of the Pokemon it is in love with (Attract, Cute Charm)
        self.raging = False              # its last move was Rage: a hit raises its Attack
        self.loafing = False             # Truant: it loafs on its next turn
        self.had_item = bool(getattr(self, "item", None))   # Unburden: it came in holding an item
        self.used_moves = frozenset()    # Last Resort: the moves used since it came in
        self.last_resort_count = 0       # how many of them, Last Resort aside (moveEffectsData.lastResortCount)

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

    # Lucky Chant's turns left (SIDE_CONDITION_LUCKY_CHANT): no critical hit
    # lands on the side while it runs; left on the class while 0.
    lucky_chant = 0
    # Aurora Veil's turns left (SIDE_CONDITION_AURORA_VEIL, auroraVeilTurns):
    # physical and special hits on the side are halved as by Reflect and
    # Light Screen, not stacking with them; left on the class while 0.
    aurora_veil = 0
    # Sticky Web on the side (SIDE_CONDITION_STICKY_WEB), 1 while laid: each
    # grounded Pokemon that comes in loses a stage of Speed (web_catch);
    # Rapid Spin, Mortal Spin and Defog clear it; left on the class while 0.
    web = 0
    # The side guard one of the side's Pokemon raised this turn
    # (TurnFlags.sideGuard): Wide Guard's, Quick Guard's, Mat Block's or
    # Crafty Shield's move constant, read by protected (guard_stops); gone
    # with the turn, and left on the class while there is none.
    guard = None
    # Follow Me, Rage Powder or Spotlight this turn (sideConditions.followMe
    # and followMeUser, a battler slot): the slot, 0 or 1, whose Pokemon
    # draws the other side's single-target moves (follow_me, targets_of);
    # cleared as the next double-battle turn starts, and left on the class
    # while None.
    follow_me = None
    # Set by __init__ on every side; on the class too, so the search's keys
    # and copies read them directly (perfectline.side_key, clone_side).
    wish = 0
    mist = 0

    def __init__(self, mons, name):
        self.mons, self.name = mons, name
        self.active = 0
        self.active2 = None
        self.screens = {"Reflect": 0, "Light Screen": 0}
        self.tailwind = 0
        self.hazards = {"rocks": 0, "spikes": 0, "tspikes": 0}
        self.safeguard = 0
        self.mist = 0                    # Mist's turns left (sideConditions.mistTurns)
        self.wish = 0                    # Wish's turn ends left: it heals at the second
        # Future Sight and Doom Desire waiting on each of the side's two slots
        # (fieldConditions.futureSight*): (turn ends left, damage, move, the
        # user's side, the user's slot), or None; and the side's
        # SIDE_CONDITION_FUTURE_SIGHT, which the trainer's AI reads.
        self.future = (None, None)
        self.future_sight = False

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

    # Gravity's turns left (FIELD_CONDITION_GRAVITY): every Pokemon held to
    # the ground, accuracy up by ten sixths, the airborne moves barred; left
    # on the class while 0.
    gravity = 0
    # The last move any Pokemon used whose attack message showed (movePrev),
    # which Copycat uses; kept only in a fight with a Copycat user
    # (st["copycat"]), and None after a turn some Pokemon could not act.
    last_move = None
    # The item a Fling has just thrown, for its effect after the hit.
    flung = None
    # A move Magic Coat is turning back is running (coat_bounces), so it is
    # not turned again.
    reflecting = False
    # Whether a Pokemon waits with Snatch this turn (Mon.snatching), so the
    # status moves look for one only then; cleared with the turn.
    snatching = False
    # Magic Room's turns left (magicRoomTurns): no held item on the field
    # works while they run (lock_item); left on the class while 0.
    magic_room = 0
    # Wonder Room's turns left (FIELD_CONDITION_WONDER_ROOM): every
    # Pokemon's Defense and Sp. Def trade places in the damage (room_mult);
    # left on the class while 0.
    wonder_room = 0
    # Whether Guard Split or Power Split has averaged a stat in this battle
    # (Mon.split), so the damage reads split_mult only then; kept by its
    # copies.
    split = False
    # Whether a side guard is up this turn (Side.guard), so protected looks
    # for one only then; left on the class while none is.
    guarded = False
    # Whether a Pokemon in this fight knows Water Sport or Mud Sport
    # (st["water_sport"], st["mud_sport"]), so the damage reads sport_half
    # only then; set as the battle is made and kept by its copies.
    sporty = False
    # Whether the move being worked out has hit a Substitute, one it broke
    # included (SELF_TURN_FLAG_SUBSTITUTE_HIT, which lasts the move): its
    # added effects then reach nothing behind it (attack, _after_attack).
    # Set again at each attack, so a copy made between moves needs none.
    sub_hit = False
    # Whether a Pokemon in this battle reads its item twin (Mon.unheld), so
    # the rows look for one only then; kept by the battle's copies.
    unheld = False
    # Deep fog on the field (FIELD_CONDITION_DEEP_FOG), from a battle on a
    # foggy map (st["fog"]): every move's accuracy at six tenths unless
    # Cloud Nine or Air Lock is out (fog_cut); a weather that starts, by a
    # move or an ability, clears it, and so does Defog. Left on the class
    # while there is none.
    fog = False
    # Whether a Pokemon in this fight has Cloud Nine or Air Lock, a twin's
    # included (st["cloud_nine"]), so the reads of the weather that look for
    # one (weather_now, row_speed) look only then; kept by the battle's
    # copies.
    cloudy = False
    # The Analytic holder whose move is running while every other Pokemon
    # on the field has acted this turn (Battler_MovedThisTurn for each):
    # its power is 13/10 (ability_power). Set by _use_move around the
    # attack, None otherwise.
    analytic = None
    # The Mind Blown user whose effect script ran in the move being worked
    # out (SELF_TURN_FLAG_MIND_BLOWN), which pays its half as the move ends
    # (mind_blown_cost); None otherwise.
    blown = None
    # The HP the last hit to land left its target with, set as the hit takes
    # it and before any Berry answers it, so the target's on-hit ability
    # reads the HP the engine's does (Berserk, hit_ability).
    hit_left = None
    # A double battle (run_doubles sets it); left on the class while False.
    doubles = False
    # Whether the move being worked out landed its hits one at a time
    # (land_hits), which attack() sets for every move; False on the class,
    # as a read with no move worked out yet found it (hit_aftermath).
    hits_landed = False
    # Whether a Helping Hand has helped a Pokemon this turn (Mon.helped), so
    # the next turn clears the flag only then.
    helping = False
    # Whether a side has a center of attention this turn (Side.follow_me),
    # so targets_of looks for one, and the next turn clears it, only then.
    following = False
    # A double battle's order of moves for the turn, [(Pokemon, move,
    # target)], and the place of the one acting now (run_doubles), which
    # After You changes; None outside a double battle's turn.
    queue = None
    queue_pos = -1
    # How many of the battle's Pokemon were down when Soul Heart last looked,
    # in a double battle (soul_heart); left on the class while 0.
    soul_down = 0
    # A double battle's damaging move is hitting more than one target, so
    # each hit is at three quarters (Battle.damage, perfectline.damage_of);
    # set around the move by the spread loop.
    spread = False
    # Magnitude's power for the use being worked out, in a double battle,
    # where one roll serves every target (BtlCmd_CalcMagnitudePower keeps
    # battleCtx->magnitude until the move ends); None between moves.
    spread_magnitude = None

    def __init__(self, st, player, boss, rng, weather=None, trick_room=False, ai_flags=0):
        self.st, self.rng = st, rng
        self.p, self.b = player, boss
        self.weather = weather
        self.weather_turns = 0 if weather else 0     # 0 with weather set: permanent
        self.trick_room = 999 if trick_room else 0
        if st.get("water_sport") or st.get("mud_sport"):
            self.sporty = True
        if st.get("fog"):
            self.fog = True
        if st.get("cloud_nine"):
            self.cloudy = True
        self.turn = 0
        self.ai_flags = ai_flags
        self.log = []

    # -- reading the calculator's rows

    def row(self, att, dfn, mv=None):
        # A Pokemon whose ability the gas has off reads its ability-blank twin's rows.
        ak = att.key if att.gas_stash is None else gas_key(self, att)
        if att.plated is not None and mv is not None and mv.effect == "JUDGEMENT":
            ak = att.plated      # the player's Judgment at its Plate's type (hold)
        dk = dfn.key if dfn.gas_stash is None else gas_key(self, dfn)
        if att.protean_type:
            ak = protean_key(self, att) or ak     # a Protean user's twin of its new type
        if dfn.protean_type:
            dk = protean_key(self, dfn) or dk
        if dfn.roosting and mv is not None and "Flying" in dfn.types:
            dk = roost_key(self, dfn, mv) or dk     # a roosting target meets the move on its twin without Flying
        if dfn.rare:
            if dfn.pirouette:
                dk = pirouette_key(self, dfn) or dk     # Meloetta as Pirouette (relic_song)
            if dfn.power_trick:
                dk = trick_key(self, dfn) or dk
            if mv is not None:
                # An identified Ghost's twin without Ghost; a grounded flier's
                # without Flying or Levitate; a Miracle Eye target's without Dark.
                dk = (foresight_key(self, dfn, mv, att) or ground_key(self, dfn, mv, att)
                      or miracle_key(self, dfn, mv, att) or dk)
        elif self.gravity and mv is not None:
            dk = ground_key(self, dfn, mv, att) or dk     # Gravity grounds a flier that nothing else marks
        rows = self.st["rows"]
        if att.rare:
            if att.pirouette:
                ak = pirouette_key(self, att) or ak     # Meloetta as Pirouette (relic_song)
            if att.power_trick:
                ak = trick_key(self, att) or ak   # a Power Trick user's twin with Attack and Defense swapped
            if att.transformed:
                # A transformed Pokemon hits as the one it copied where prepare()
                # has rowed that one against this target (transform).
                tk = att.transform_key
                if (self.weather, tk, dk) in rows or (None, tk, dk) in rows:
                    ak = tk
        if att.ability == "Mold Breaker" and dfn.ability in METALS:
            dk = metal_raw_key(self, att, dfn, mv, ak) or dk     # the target's own weight (metal_raw_key)
        # A type or ability another move or ability changed (form_key) reads
        # the changed Pokemon's twin: the pair of twins when both are
        # changed, else the one change against the other's rows, as far as
        # prepare() rowed them.
        fa = form_key(self, att, mv) if att.formed else None
        fd = form_key(self, dfn, mv, defending=True) if dfn.formed else None
        if fa or fd:
            for a, d in ((fa or ak, fd or dk), (fa or ak, dk), (ak, fd or dk)):
                w = self.weather if (self.weather, a, d) in rows else None
                got = rows.get((w, a, d))
                if got is not None:
                    return got
        if self.unheld and (att.unheld or dfn.unheld):
            # A trainer's Pokemon whose item the battle took reads its item
            # twin (mark_unheld), where nothing else has changed its key; a
            # pair prepare() did not row with the twin keeps its own rows.
            # Its Fling reads its own rows, made with its own item: the item
            # is spent before the hit (Fling's script), but its damage is
            # worked out from the item still held (RemoveItem comes after
            # CalcDamage). An item the player's Trick gave it flings at its
            # own item's power, as Ian accepted on 2026-10-15. Until
            # 2026-10-21 it read the twin, which holds nothing, so the Fling
            # dealt nothing (Ian approved the fix on 2026-10-21).
            ua = item_key(self, att) if att.unheld and ak == att.key and not flinging(mv) else None
            ud = item_key(self, dfn) if dfn.unheld and dk == dfn.key else None
            if ua or ud:
                a, d = ua or ak, ud or dk
                w = self.weather if (self.weather, a, d) in rows else None
                got = rows.get((w, a, d))
                if got is not None:
                    return got
        w = self.weather if (self.weather, ak, dk) in rows else None
        return rows.get((w, ak, dk))

    def rolls(self, att, dfn, mv):
        r = self.row(att, dfn, mv)
        if not r:
            return None
        got = r["moves"].get(mv.name)
        if not got or "error" in got:
            # Heat Crash has no row of its own (the calculator gives it no
            # power), only its power rows (heat_crash_rolls); looked for
            # only on this path, which other moves never reach.
            return self.heat_crash_rolls(att, dfn, mv) if mv.name == "Heat Crash" else None
        return got["rolls"]

    def heat_crash_rolls(self, att, dfn, mv):
        """Heat Crash's rolls from the row prepare() made at the power the two
        Pokemon's weights give it ("<key>#hc<power>", weight_power), or None
        where it made none (a twin's rows, a fight without the move)."""
        power = (self.st.get("heat_crash") or {}).get((att.key, dfn.key))
        if power is None:
            return None
        key = att.key
        att.key = f"{key}#hc{power}"
        try:
            r = self.row(att, dfn, mv)
        finally:
            att.key = key
        got = r["moves"].get(mv.name) if r else None
        return got["rolls"] if got and "error" not in got else None

    def speed(self, mon):
        """Speed as BattleSystem_CompareBattlerSpeed works it, in whole
        numbers: the calculator's figure (weather abilities and items in
        it) at the Speed stage (sStatStageBoosts, truncated), then Quick
        Feet's 1.5 with a status or else paralysis's quarter, then Tailwind."""
        s = self.row_speed(mon)
        st = mon.stages["spe"]
        s = s * (10 + 5 * st) // 10 if st >= 0 else s * 10 // (10 - 5 * st)
        if mon.ability == "Quick Feet" and mon.status:
            s = s * 15 // 10
        elif mon.status == "par":
            s //= 4
        if mon.ability == "Unburden" and mon.had_item and not (mon.item or mon.item_off):
            s *= 2               # canUnburden, set as it came in holding an item
        side = self.p if mon.side == "p" else self.b
        if side.tailwind:
            s *= 2
        return s

    def row_speed(self, mon):
        """The calculator's Speed for this Pokemon in this weather, as its
        damage rows have it: no stages, no status. Under Neutralizing Gas its
        ability-blank twin's, so Swift Swim and the like stop counting, and
        after a changed ability its twin's (form_key), so a traced Swift Swim
        starts counting."""
        speed = self.st["speed"]
        key = mon.key if mon.gas_stash is None else gas_key(self, mon)
        if mon.rare and mon.transformed and ((self.weather, mon.transform_key) in speed
                                             or (None, mon.transform_key) in speed):
            key = mon.transform_key      # a transformed Pokemon has its copy's Speed (transform)
        if mon.rare and mon.pirouette:
            twin = pirouette_key(self, mon)
            if twin and ((self.weather, twin) in speed or (None, twin) in speed):
                key = twin               # Meloetta as Pirouette has its twin's Speed (relic_song)
        twin = form_key(self, mon) if mon.formed else None
        if twin and ((self.weather, twin) in speed or (None, twin) in speed):
            key = twin
        if self.unheld and mon.unheld and key == mon.key:
            # its item twin's Speed, a Choice Scarf gone (mark_unheld)
            twin = item_key(self, mon)
            if twin and ((self.weather, twin) in speed or (None, twin) in speed):
                key = twin
        weather = self.weather
        if self.cloudy and weather is not None and weather_ignored(self):
            # Swift Swim, Chlorophyll and Sand Rush do not count while Cloud
            # Nine or Air Lock is out (BattleSystem_CompareBattlerSpeed's
            # NO_CLOUD_NINE): the Speed with no weather, the calculator's
            # own figure where no row has it.
            return int(speed.get((None, key)) or (self.st["info"].get(key) or {}).get("speed") or 1)
        return int(speed.get((weather, key)) or speed.get((None, key)) or 1)

    def faster(self, a, b):
        """Whether a moves before b at equal priority; ties at random."""
        sa, sb = self.speed(a), self.speed(b)
        if self.trick_room:
            sa, sb = -sa, -sb
        if sa == sb:
            return self.rng.random() < 0.5
        return sa > sb

    # -- damage

    def damage(self, att, dfn, mv, crit=None, roll=None, ai_view=False, share=None):
        """One use's damage, or None when the calculator has no figure. With
        ai_view: the top roll, no critical hit, as the AI reckons it. With
        share, (weight, whole), one hit of a move whose row adds up several
        (hit_weights)."""
        rolls = self.rolls(att, dfn, mv)
        if rolls is None:
            return None
        sure = mv.sure
        if sure:
            # The move's own critical hit unless told (sure_crit); none in
            # the AI's estimate, which passes criticalMul 1 (TrainerAI_CalcDamage).
            crit = False if ai_view else (sure_crit(self, att, dfn) if crit is None else crit)
        base = rolls[-1] if ai_view else (rolls[roll] if roll is not None else self.rng.choice(rolls))
        if base <= 0:
            return 0
        if share is not None:
            base = base * share[0] / share[1]
        a_st, d_st = ("atk", "def") if mv.cat == "Physical" else ("spa", "spd")
        a, d = att.stages[a_st], dfn.stages[d_st]
        if dfn.ability == "Unaware" and att.ability != "Mold Breaker":
            a = 0                # Unaware ignores the attacker's stages
        if att.ability == "Unaware" or mv.const in IGNORE_TARGET_STAGES:
            d = 0                # and, on its own attack, the target's, as Sacred Sword's kind does
        if crit:
            a, d = max(a, 0), min(d, 0)
        mult = stage_mult(a) / stage_mult(d) * state_mult(self, att, dfn, mv)
        if mv.cat == "Physical" and att.status == "brn" and att.ability != "Guts":
            mult *= 0.5
        if att.ability == "Guts" and att.status:
            mult *= 1.5
        if att.ability == "Flash Fire" and mv.type == "Fire" and not att.flash_fire:
            mult *= 2 / 3        # the calculator's row has Flash Fire always lit
        elif att.gas_stash == "Flash Fire" and att.flash_fire and mv.type == "Fire":
            mult *= 1.5          # lit, it burns on under the gas (BATTLEMON_FLASH_FIRE); the twin's row lacks it
        if att.side == "p" and booster_fifth(self, att, mv):
            # The player's rows are item-free; a booster adds its fifth here.
            # booster_fifth is False for any Pokemon not on the player's
            # side, so the side is looked at first and the call made only
            # for the player's, as this runs for every damage figure.
            mult *= 1.2
        side = self.p if dfn.side == "p" else self.b
        screen = "Reflect" if mv.cat == "Physical" else "Light Screen"
        if (side.screens[screen] or side.aurora_veil) and not crit and mv.effect != "REMOVE_SCREENS" \
                and att.ability != "Infiltrator":     # Aurora Veil halves both, once with a screen
            mult *= 2 / 3 if self.doubles else 0.5
        if self.spread:
            mult *= 0.75
        if sure:
            mult *= row_crit_mult(att, dfn, crit)     # the row's own critical hit (row_crit_mult)
        elif crit:
            mult *= CRIT_MUL * (1.5 if att.ability == "Sniper" else 1.0)
        if not ai_view and mv.effect == ROLLOUT:
            # TrainerAI_CalcDamage has no Rollout case: the AI costs it at
            # its listed power, with no Defense Curl and no run count. Any
            # other move's factor is 1 (rollout_mult), so it is applied only
            # for Rollout and Ice Ball.
            mult *= rollout_mult(att, mv)
        return max(1, int(base * mult))

    def accuracy_hits(self, att, dfn, mv, first=True, later=False):
        """Whether the move lands (BattleControllerPlayer_CheckMoveHitAccuracy
        and the hit overrides). `first`: whether the target has yet to move
        this turn, for the Zoom Lens. `later`: a later hit of a rising
        move's or Population Bomb's, whose check skips the overrides, No
        Guard and Lock-On among them (RISING, TEN_HITS)."""
        if mv.acc == 0 or mv.effect == "BYPASS_ACCURACY" or (
                not later and (no_guard(att, dfn, mv) or (dfn.rare and lands_sure(att, dfn, mv)))):
            return True
        acc = mv.acc
        if dfn.ability == "Wonder Skin" and mv.cat == "Status":
            acc = wonder_skin(att, dfn, acc)
        weather = weather_now(self)          # none under Cloud Nine or Air Lock
        if weather == "Rain" and mv.effect in RAIN_SURE:
            return True      # never a miss in the rain, past every stage (RAIN_SURE)
        if mv.effect in ("THUNDER", "HURRICANE") and weather == "Sun":
            acc = 50         # Oxide: Hurricane as Thunder in the sun
        if mv.effect == "BLIZZARD" and weather == "Hail":
            return True
        acc *= accuracy_scale(att, dfn, mv, first)
        if att.ability == "Compound Eyes":
            acc *= 1.3
        if att.item == "Wide Lens":
            acc *= 1.1
        if self.fog:
            acc *= fog_cut(self)         # deep fog's six tenths (fog_cut)
        if att.ability == "Hustle" and mv.cat == "Physical":
            acc *= 0.8
        if self.gravity:
            acc = acc * 10 / 6           # Gravity's ten sixths, after everything else
        return self.rng.random() * 100 < acc


# The moves that never miss in the rain: BattleControllerPlayer_CheckMoveHitOverrides
# clears the miss the accuracy roll made, unless Cloud Nine or Air Lock is
# out, so no stage, item or ability that cuts accuracy can make them miss
# there. Thunder, Hurricane and the three Hisuian storms. Until 2026-10-20
# Thunder and Hurricane were set at 100 in the rain and then met the stages,
# so a lowered accuracy or a raised evasion could still make them miss, and
# Wildbolt Storm and Sandsear Storm met the rain as any weather (Ian approved
# the fix on 2026-10-20; Bleakwind Storm's came in on 2026-10-20 too).
RAIN_SURE = frozenset({"THUNDER", "HURRICANE", "BLEAKWIND_STORM", "WILDBOLT_STORM", "SANDSEAR_STORM"})


def wonder_skin(att, dfn, acc):
    """A status move's accuracy against a Wonder Skin holder
    (BattleControllerPlayer_CheckMoveHitAccuracy, before the stages): 50 at
    most, unless att's Mold Breaker gets past it; a move that cannot miss
    never comes here. Until 2026-10-20 it did nothing (Ian approved the
    fix)."""
    return min(acc, 50) if not mold(att, dfn) else acc


def stage_mult(s):
    return (2 + s) / 2 if s >= 0 else 2 / (2 - s)


def no_guard(att, dfn, mv):
    """No Guard on either side lands every move but a one-hit KO move, whose
    check is its own (BattleControllerPlayer_CheckMoveHitOverrides skips
    the accuracy roll's miss, and the semi-invulnerable test after it, for
    a move without SYSCTL_NONSTANDARD_ACC_CHECK). Until 2026-10-14 accuracy
    was rolled as usual both ways (Ian approved the fix)."""
    return (att.ability == "No Guard" or dfn.ability == "No Guard") and mv.effect != "ONE_HIT_KO"


IDENTIFIED_TYPES = frozenset({"Normal", "Fighting"})


def identified(dfn, mv_type):
    """Whether Foresight or Odor Sleuth lets a move of this type meet dfn's
    Ghost type: BattleSystem_ApplyTypeChart stops at the chart's 0xFE mark
    for an identified target, which leaves out the Ghost type's immunities
    to Normal and Fighting moves."""
    return dfn.foresight and mv_type in IDENTIFIED_TYPES and "Ghost" in dfn.types


def chart_types(dfn, mv):
    """dfn's types as the type chart reads them against mv: without Ghost
    for a Normal or Fighting move into an identified target, so it meets
    the Pokemon's other type alone (none for a pure Ghost)."""
    if identified(dfn, mv.type):
        return [t for t in dfn.types if t != "Ghost"]
    if eyed(dfn, mv.type):
        return [t for t in dfn.types if t != "Dark"]
    return dfn.types


def foresee_target(dfn):
    """Foresight and Odor Sleuth (effect script 113, subscript_foresight):
    the target is identified until it leaves, through a Substitute too, and
    a second use changes nothing. Its raised evasion stops counting against
    any attacker (MON_IS_IDENTIFIED in BattleControllerPlayer_CheckMoveHitAccuracy,
    lowered evasion still counting), and Normal and Fighting moves hit its
    Ghost type (identified), read from its twin without Ghost (prepare's
    foresight_twin). Until 2026-10-15 the moves did nothing (Ian approved
    the fix)."""
    dfn.foresight = dfn.rare = True


def foresight_key(b, mon, mv, att):
    """The key of the rows an identified Ghost meets a Normal or Fighting
    move on (prepare's foresight_twin), or None."""
    if not identified(mon, move_type_used(att.ability, mv, att.ivs, att.item, weather_now(b))):
        return None
    return (b.st.get("foresight_twin") or {}).get(mon.key)


def eyed(dfn, mv_type):
    """Whether Miracle Eye lets a move of this type meet dfn's Dark type:
    BasicTypeMulApplies skips the chart's Psychic-into-Dark immunity for a
    target with MOVE_EFFECT_MIRACLE_EYE, and only that entry."""
    return dfn.miracle_eye and mv_type == "Psychic" and "Dark" in dfn.types


def miracle_eye(dfn):
    """Miracle Eye (effect script 216, subscript_miracle_eye): the target is
    marked until it leaves (MOVE_EFFECT_MIRACLE_EYE, not handed on by Baton
    Pass), through a Substitute too, as the subscript has no Substitute
    check; a second use changes nothing. Its raised evasion stops counting
    against any attacker (MON_IS_IDENTIFIED in
    BattleControllerPlayer_CheckMoveHitAccuracy, lowered evasion still
    counting), and Psychic moves hit its Dark type (eyed), read from its
    twin without Dark (prepare's miracle_twin). Until 2026-10-15 the move
    did nothing (Ian approved the fix)."""
    dfn.miracle_eye = dfn.rare = True


def miracle_key(b, mon, mv, att):
    """The key of the rows a Miracle Eye target of the Dark type meets a
    Psychic move on (prepare's miracle_twin), or None."""
    if not mon.miracle_eye or not eyed(mon, move_type_used(att.ability, mv, att.ivs, att.item, weather_now(b))):
        return None
    return (b.st.get("miracle_twin") or {}).get(mon.key)


def grounded(b, mon):
    """Whether mon is held to the ground against Ground moves: Smack Down's
    mark on it, its own Ingrain's roots, or Gravity in force.
    BattleSystem_ApplyTypeChart then skips the Flying type's immunity to
    Ground moves (BasicTypeMulApplies) and Battler_Ability reads no
    Levitate, so a Ground move meets its other type alone, read from its
    twin (prepare's ground_twin). Ingrain's part did nothing until
    2026-10-15 (Ian approved the fix)."""
    return mon.smacked or mon.ingrained or bool(getattr(b, "gravity", 0))


def gravity_start(b):
    """Gravity (effect script 215, subscript_gravity_start): it fails while
    one is in force; otherwise five turns, ended at the fifth turn's end
    (FIELD_COND_CHECK_STATE_GRAVITY), and every Pokemon on the field in the
    air on Fly's or Bounce's hidden turn is brought down, out of the move,
    and every one under Magnet Rise loses it. While it lasts every Pokemon
    is grounded (grounded), accuracy rises by ten sixths
    (BattleControllerPlayer_CheckMoveHitAccuracy), Fly, Bounce, Jump Kick,
    High Jump Kick, Splash and Magnet Rise can be neither chosen nor used
    (Move_FailsInHighGravity, move_barred), Spikes and Toxic Spikes reach a
    Flying or Levitate newcomer, Arena Trap holds every foe, and Grav Apple
    hits half as hard again. Until 2026-10-15 Gravity did nothing (Ian
    approved the fix)."""
    if b.gravity:
        return
    b.gravity = 5
    for m in b.p.on_field() + b.b.on_field():
        if not m.alive():
            continue
        m.magnet_rise = 0
        if m.charging is not None and m.charging.effect in ("FLY", "BOUNCE"):
            m.charging = None            # UnlockMoveChoice and ToggleVanish: brought out of the air


def ground_key(b, mon, mv, att):
    """The key of the rows a grounded Flying or Levitate Pokemon meets a
    Ground move on (prepare's ground_twin), or None."""
    if not grounded(b, mon) or move_type_used(att.ability, mv, att.ivs, att.item, weather_now(b)) != "Ground":
        return None
    return (b.st.get("ground_twin") or {}).get(mon.key)


def smack_down(b, att, dfn):
    """Smack Down's hit (effect script 406, subscript_smack_down, ON_HIT):
    on a target left standing, with no Substitute in the way, not already
    down and with no Gravity in force, a Pokemon on the hidden turn of Fly
    or Bounce is pulled out of it, and one under Magnet Rise loses it; it,
    and a Flying type or a Levitate holder, is then down until it leaves
    (Ingrain and an Iron Ball hold a Pokemon down already). Down, its Fly,
    Bounce and Magnet Rise fail (effect scripts 155, 263 and 252), Arena
    Trap holds it, and Ground moves hit it (grounded). Until 2026-10-15 the
    hit grounded nothing (Ian approved the fix)."""
    if dfn.smacked or getattr(b, "gravity", 0):
        return
    if dfn.charging is not None and dfn.charging.effect in ("FLY", "BOUNCE"):
        dfn.charging = None              # UnlockMoveChoice and ToggleVanish: out of the air
    elif dfn.ingrained or dfn.item == "Iron Ball":
        return
    elif dfn.magnet_rise:
        dfn.magnet_rise = 0
    elif "Flying" not in dfn.types and dfn.ability != "Levitate":
        return
    dfn.smacked = dfn.rare = True


def locked_onto(att, dfn):
    """Whether att's Lock-On or Mind Reader holds dfn (MON_IS_LOCKED_ONTO:
    the target's MOVE_EFFECT_LOCK_ON count runs and names att)."""
    return bool(dfn.locked_on) and dfn.lock_on_by == att.key


def lands_sure(att, dfn, mv):
    """BattleControllerPlayer_CheckMoveHitOverrides' first override: with
    No Guard on either side, or the user's Lock-On on the target, the move
    hits whatever its accuracy and the stages, and reaches a target on the
    hidden turn of Fly and the like, a one-hit KO move apart, whose check is
    its own. Lock-On's part did nothing until 2026-10-15 (Ian approved the
    fix)."""
    return no_guard(att, dfn, mv) or (dfn.rare and locked_onto(att, dfn) and mv.effect != "ONE_HIT_KO")


def lock_on(att, dfn):
    """Lock-On and Mind Reader (effect script 94, subscript_lock_on): on a
    target with no Substitute (an Infiltrator passes it) the user's moves
    land for the rest of this turn and all of the next (the target's count
    set to 2, one off at each turn's end, MON_COND_CHECK_STATE_LOCK_ON).
    The hold ends when either leaves, but a Baton Pass carries it on: the
    target's to its replacement (MOVE_EFFECT_BATON_PASSED), the user's to
    its own, its count started again (battle_lib.c 2196). Protect stops the
    move, and a target on its hidden turn makes it fail."""
    if not sub_blocks(att, dfn):
        dfn.locked_on, dfn.lock_on_by, dfn.rare = 2, att.key, True


def accuracy_scale(att, dfn, mv, first=True):
    """The accuracy check's stage factor and the abilities and item beside it
    that both battles share (BattleControllerPlayer_CheckMoveHitAccuracy):
    an Unaware target (unless Mold Breaker gets past it) ignores the
    attacker's accuracy stages; an Unaware, Keen Eye or Illuminate attacker,
    and Sacred Sword's kind, ignore the target's evasion stages; a confused
    Tangled Feet target halves the accuracy (Mold Breaker gets past it); a
    Zoom Lens adds a fifth against a target that has already moved this turn
    (not `first`). Until 2026-10-14 every stage counted and neither Tangled
    Feet nor the Zoom Lens did anything (Ian approved the fix)."""
    acc_st = 0 if dfn.ability == "Unaware" and not mold(att, dfn) else att.stages["acc"]
    ignore_eva = mv.const in IGNORE_TARGET_STAGES or att.ability in ("Unaware", "Keen Eye", "Illuminate")
    eva = dfn.stages["eva"]
    if eva > 0 and (dfn.foresight or dfn.miracle_eye):
        eva = 0                  # an identified target's raised evasion stops counting (foresee_target, miracle_eye)
    s = max(-6, min(6, acc_st - (0 if ignore_eva else eva)))
    scale = (3 + s) / 3 if s >= 0 else 3 / (3 - s)
    if dfn.ability == "Tangled Feet" and dfn.confused and not mold(att, dfn):
        scale *= 0.5
    if att.item == "Zoom Lens" and not first:
        scale *= 1.2
    return scale


# The moves that ignore their target's stat stages, raised or lowered, its
# defensive ones in the damage (BattleSystem_CalcMoveDamage) and its evasion
# in the accuracy check (BattleControllerPlayer_CheckMoveHitAccuracy), as an
# Unaware attacker does. Until 2026-10-14 the readings and fightsim's own
# damage weakened them by the target's stages (Ian approved the fix).
IGNORE_TARGET_STAGES = frozenset({"MOVE_SACRED_SWORD", "MOVE_DARKEST_LARIAT", "MOVE_CHIP_AWAY"})


# ---- the rules of a turn --------------------------------------------------------------------

def mold(att, dfn):
    """Battler_IgnorableAbility: att's Mold Breaker gets past dfn's ability
    wherever the engine asks that function, unless dfn holds an Ability
    Shield (Oxide, element 7). Until 2026-10-14 the simulator honoured it
    for Sturdy, Unaware, Damp, Own Tempo, Oblivious and the absorbing
    abilities alone (Ian approved the fix)."""
    return att is not None and att is not dfn and att.ability == "Mold Breaker" and dfn.item != "Ability Shield"


def status_ability_ignored(b, target):
    """Whether the status about to be given comes from a Mold Breaker's move,
    which the status subscripts' ability checks let through
    (CheckIgnorableAbility on every path but Toxic Spikes'). b.status_src is
    the move's user while a move runs, and the ability's holder, no one, or
    the foe for an ability's, a hazard's or Synchronize's status."""
    return mold(getattr(b, "status_src", None), target)


def can_status(b, target, status):
    # A Substitute stops a status unless a move's own effect passes it
    # (give_status_by_move, for an Infiltrator attacker).
    if target.status or not target.alive() or (target.sub and getattr(b, "passing_sub", None) is not target):
        return False
    side = b.p if target.side == "p" else b.b
    if side.safeguard and getattr(b, "passing_safeguard", None) is not target:
        return False
    t = set(target.types)
    # Oxide's Corrosion: a poison its holder gives with a move, as a status
    # move or a hit's effect, reaches Poison and Steel types (subscript_poison).
    # status_src is the move's user then, and never a Corrosion holder for
    # an ability's poison, a hazard's or an Orb's.
    src = getattr(b, "status_src", None)
    if status in ("psn", "tox") and t & {"Poison", "Steel"} and not (src is not None and src.ability == "Corrosion"):
        return False
    if status == "brn" and "Fire" in t:
        return False
    if status == "frz" and "Ice" in t:
        return False
    if status == "par" and "Electric" in t:
        return False
    if b.doubles and status in PARTNER_STATUS_VEIL and veil_partner(b, target, status) is not None:
        return False
    if status_ability_ignored(b, target):
        return True              # a Mold Breaker's move passes the abilities below
    if target.ability == "Purifying Salt":
        return False             # Oxide: Purifying Salt allows no status at all
    return target.ability not in STATUS_ABILITIES.get(status, set())


# Oxide's Water Bubble keeps burns off as Water Veil does (subscript_burn,
# Ability_ForbidsStatus); until 2026-10-14 the simulator let them through
# (Ian approved the fix). Oxide's Sweet Veil keeps sleep off its holder as
# Insomnia does (subscript_fall_asleep and subscript_yawn, past a Mold
# Breaker's move; in a double battle its partner too, through
# PARTNER_STATUS_VEIL since 2026-10-21); until 2026-10-20 it did nothing in
# the battle (Ian approved the fix). Oxide's Pastel Veil keeps poison and
# bad poison off its holder as Immunity does (subscript_poison,
# subscript_badly_poison, Toxic Spikes' included; its partner's in a double
# battle through PARTNER_STATUS_VEIL since 2026-10-21); until 2026-10-20 the
# poison landed, and only its cure ran (Ian approved the fix).
STATUS_ABILITIES = {"slp": {"Insomnia", "Vital Spirit", "Sweet Veil"}, "par": {"Limber"},
                    "brn": {"Water Veil", "Water Bubble"},
                    "psn": {"Immunity", "Pastel Veil"}, "tox": {"Immunity", "Pastel Veil"}, "frz": {"Magma Armor"}}
# The abilities that keep a status off their holder's partner too, in a
# double battle (can_status).
PARTNER_STATUS_VEIL = {"slp": "Sweet Veil", "psn": "Pastel Veil", "tox": "Pastel Veil"}
# The abilities announced as their holder comes in (each message tags the
# ability, so BattleAI_SetAbility records it).
ENTRY_ANNOUNCED = {"Intimidate", "Pressure", "Mold Breaker", "Drizzle", "Drought", "Sand Stream",
                   "Snow Warning", "Download", "Trace", "Anticipation", "Forewarn", "Frisk", "Slow Start",
                   "Unnerve", "Neutralizing Gas"}


# The abilities that turn a hit to nothing, and so are named when they do.
ZEROING = {"Volt Absorb", "Water Absorb", "Flash Fire", "Motor Drive", "Dry Skin", "Lightning Rod",
           "Storm Drain", "Sap Sipper", "Levitate", "Wonder Guard", "Soundproof", "Bulletproof"}


# The abilities that take a move of one type whole and give their holder
# something for it (BattleSystem_TriggerImmunityAbility): a quarter of its
# maximum HP back, or a stage of one stat.
ABSORB_HEAL = {"Volt Absorb": "Electric", "Water Absorb": "Water", "Dry Skin": "Water"}
ABSORB_STAGE = {"Lightning Rod": ("Electric", "spa"), "Storm Drain": ("Water", "spa"),
                "Sap Sipper": ("Grass", "atk"), "Motor Drive": ("Electric", "spe")}


def absorb(b, att, dfn, mv):
    """Whether dfn's ability takes this move whole, as
    BattleSystem_TriggerImmunityAbility does for a move of its type from
    another Pokemon, damaging or not, unless the user has Mold Breaker; if
    so its holder gets its due: a quarter of its maximum HP
    (subscript_ability_restores_hp, nothing at full HP) or a stage of its
    stat, raised directly so Simple does not double it
    (subscript_absorb_and_*_up_1_stage, nothing at +6). The ability is
    named either way."""
    ab = dfn.ability
    kind = ABSORB_HEAL.get(ab) or (ABSORB_STAGE[ab][0] if ab in ABSORB_STAGE else None)
    if kind is None or kind != mv.type or att is dfn or att.ability == "Mold Breaker":
        return False
    reveal(dfn)
    if ab in ABSORB_HEAL:
        if dfn.hp < dfn.maxhp:
            heal(dfn, max(1, dfn.maxhp // 4))
    else:
        stat = ABSORB_STAGE[ab][1]
        if dfn.stages[stat] < 6:
            dfn.stages[stat] += 1
            dfn.stat_raised = True
    return True


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


# ---- Neutralizing Gas (the simulator's support approved by Ian, 2026-10-13) --------------------------------

# The natures with their raised and lowered stats (pokemon_nature.c's
# table), by the stat keys the records use; a neutral one has neither.
NATURES = {"Hardy": (None, None), "Lonely": ("at", "df"), "Brave": ("at", "sp"), "Adamant": ("at", "sa"),
           "Naughty": ("at", "sd"), "Bold": ("df", "at"), "Docile": (None, None), "Relaxed": ("df", "sp"),
           "Impish": ("df", "sa"), "Lax": ("df", "sd"), "Timid": ("sp", "at"), "Hasty": ("sp", "df"),
           "Serious": (None, None), "Jolly": ("sp", "sa"), "Naive": ("sp", "sd"), "Modest": ("sa", "at"),
           "Mild": ("sa", "df"), "Quiet": ("sa", "sp"), "Bashful": (None, None), "Rash": ("sa", "sd"),
           "Calm": ("sd", "at"), "Gentle": ("sd", "df"), "Sassy": ("sd", "sp"), "Careful": ("sd", "sa"),
           "Quirky": (None, None)}


def swapped_nature(nature):
    """The nature whose effects on Attack and Defense are this one's swapped
    (Adamant's raised Attack becomes Impish's raised Defense), so a twin
    built with it has the two final stats exchanged; a neutral one, or one
    the table lacks, stays."""
    plus, minus = NATURES.get(nature or "Hardy", (None, None))
    if plus is None:
        return nature
    flip = {"at": "df", "df": "at"}
    want = (flip.get(plus, plus), flip.get(minus, minus))
    return next((n for n, pm in NATURES.items() if pm == want), nature)


def power_trick(att):
    """Power Trick and Power Shift (effect script 238,
    subscript_user_swap_atk_and_def): the user's Attack and Defense stats
    change places, its stages staying, and the mark turns over
    (MOVE_EFFECT_POWER_TRICK is XORed), so a second use puts them back; its
    rows then come from its twin built with the two swapped (prepare's
    trick_twin, trick_key). The trainer's AI's Basic check reads the mark.
    Until 2026-10-15 the stats stayed (Ian approved the fix)."""
    att.power_trick = not att.power_trick
    if att.power_trick:
        att.rare = True


def trick_key(b, mon):
    """The key of a Power Trick user's twin with its Attack and Defense
    swapped (prepare's trick_twin), or None (a Baton Pass's receiver has
    none, and reads its own rows)."""
    return (b.st.get("trick_twin") or {}).get(mon.key)


def protean_key(b, mon):
    """The key of the rows of a Pokemon its Protean has retyped: its twin
    of that one type (prepare's protean_twin), or None without one."""
    return ((b.st.get("protean_twin") or {}).get(mon.key) or {}).get(mon.protean_type)


def protean(b, mon, mv):
    """Protean and Libero (BEFORE_MOVE_STATE_PROTEAN): once a stay on the
    field, the first move, Struggle aside, whose type its user is not wholly
    already makes the user that type alone, so the move takes STAB and the
    user meets moves as that type, until it leaves the field. The rows
    follow through its twin of that type (protean_key) and the type checks
    through mon.types; the message names the ability."""
    if mon.ability not in ("Protean", "Libero") or mon.protean_used or mv.effect == "STRUGGLE":
        return
    t = ({"Sun": "Fire", "Rain": "Water", "Hail": "Ice", "Sand": "Rock"}.get(b.weather, mv.type)
         if mv.name == "Weather Ball" else mv.type)
    if set(mon.types) == {t}:
        return
    mon.protean_used, mon.protean_type, mon.types = True, t, [t]
    reveal(mon)


def roost_key(b, mon, mv):
    """The key of the rows a roosting Pokemon meets this move on (prepare's
    roost_twin): its twin typed without Flying; for a pure Flying one,
    whichever of its Normal and Grass twins this move's type hits neutrally,
    as a type the chart cannot read would be hit. None for a Pokemon with
    no twin."""
    twins = (b.st.get("roost_twin") or {}).get(mon.key)
    if not twins:
        return None
    for key, types in twins:
        if len(twins) == 1 or effectiveness(b.st["chart"], mv.type, types) == 1:
            return key
    return twins[0][0]


# ---- types and abilities the battle changes (batch 3 of the fixes Ian approved on 2026-10-14) ----
#
# A move or an ability can rewrite a Pokemon's types (Soak, Color Change,
# Conversion, Burn Up) or its ability (Trace, Mummy, Skill Swap, Worry
# Seed) in the middle of a battle, or turn its ability off (Gastro Acid),
# and the change lasts until the Pokemon leaves the field, since the engine
# reloads both from the party record as it comes back in
# (BattleSystem_InitBattleMon). The calculator's rows are made once per
# fight with each Pokemon's own types and ability. So prepare() makes a
# twin of each Pokemon for each change its fight can produce, as the moves
# and abilities on both sides decide (FORM_CHANGES), and rows it both ways
# against every foe it can face; the battle reads a changed Pokemon's rows
# from its twin (form_key). A fight with none of these moves and abilities
# gets no twin. A change of ability needs a twin only when the old or the
# new ability changes the calculator's rows (row_ability), so most
# abilities share one twin, or need none.

# The calculator's files a Generation 4 row runs through: gen4.js, what it
# calls, and Oxide's profile.
CALC_ROW_FILES = ("mechanics/gen4.js", "mechanics/util.js", "mechanics/romhacks/helpers.js",
                  "mechanics/romhacks/index.js", "mechanics/romhacks/profiles/platinum-oxide.js",
                  "mechanics/romhacks/profiles/platinum-oxide-data.js", "move.js", "pokemon.js", "stats.js",
                  "field.js", "items.js")
# The abilities the calculator reads that never change one of the
# simulator's rows, which are made at full HP, with no status, stat stage,
# screen or Intimidate (CALC_ABILITY_OFF) and with one hit's effects at a
# time, so a twin need not carry them: those it reads only between a
# multi-hit move's hits (checkMultihitBoost: Mummy and Wandering Spirit
# hand the attacker their ability, Gooey, Weak Armor, Water Compaction and
# Seed Sower answer a hit), which the battle runs hit by hit itself where it
# runs them at all; Intimidate's blockers and answers (checkIntimidate:
# Clear Body, White Smoke, Hyper Cutter, Inner Focus, Own Tempo, Oblivious,
# Mirror Armor, Defiant, Competitive, Guard Dog); those of stat stages
# (Simple, Contrary, Unaware) and of screens (Infiltrator); those of a
# status (Guts, Marvel Scale, Quick Feet, Merciless) or of a third of HP
# (Blaze, Torrent, Overgrow, Swarm), which the battle applies itself as it
# runs; and Protean and Libero, which only the later generations' STAB
# reads (getStabMod), where the battle retypes the holder itself. A check in
# test_plfixes holds the calculator to it.
ROW_NEUTRAL = frozenset({
    "Mummy", "Wandering Spirit", "Lingering Aroma", "Gooey", "Weak Armor", "Water Compaction", "Seed Sower",
    "Clear Body", "White Smoke", "Hyper Cutter", "Full Metal Body", "Strong Body", "Inner Focus", "Own Tempo",
    "Oblivious", "Mirror Armor", "Defiant", "Competitive", "Guard Dog", "Simple", "Contrary", "Unaware",
    "Infiltrator", "Guts", "Marvel Scale", "Quick Feet", "Merciless", "Blaze", "Torrent", "Overgrow", "Swarm",
    "Protean", "Libero"})


@functools.lru_cache(maxsize=None)
def row_abilities():
    """The abilities that can change a calculator row: each ability that a
    file the Generation 4 row runs through spells out, a superset that costs
    at most a twin too many, less those prepare() keeps off the rows
    (CALC_ABILITY_OFF) and ROW_NEUTRAL."""
    names = set()
    for p in calc.blob()["poks"].values():
        names.update(a for a in (p.get("abilities") or {}).values() if a)
    base = os.path.join(data.ROOT, "tools", "oxide", "encounters", "calc", "calc")
    found = set()
    for rel in CALC_ROW_FILES:
        with open(os.path.join(base, rel), encoding="utf-8") as fh:
            found.update(re.findall(r"""['"]([A-Z][A-Za-z' -]+)['"]""", fh.read()))
    return frozenset(found & names) - CALC_ABILITY_OFF - ROW_NEUTRAL


def row_ability(ability):
    """The ability as a calculator row reads it: itself when it can change a
    row, else None, which a twin makes with the stand-in."""
    return ability if ability in row_abilities() else None


# What each ability refuses (battle_lib.c's sAbilityChangeFlags, Oxide's
# table after hg-engine's AbilityFlags; Ability_ChangeFails): "trace", Trace
# cannot copy it; "copy", Role Play cannot copy it; "swap", Skill Swap and
# Wandering Spirit cannot take it; "suppress", it cannot be suppressed or
# replaced (Gastro Acid, Core Enforcer, Worry Seed, Mummy, Role Play's user,
# Entrainment's target); "entrain", Entrainment cannot pass it on. Every
# other ability refuses nothing.
_ALL_CHANGES = frozenset({"trace", "copy", "swap", "suppress", "entrain"})
_NO_COPYING = frozenset({"trace", "copy", "entrain"})
_NO_TAKING = frozenset({"trace", "copy", "swap", "entrain"})
ABILITY_REFUSES = {
    "Wonder Guard": frozenset({"copy", "swap", "entrain"}), "Trace": _NO_COPYING, "Forecast": _NO_COPYING,
    "Multitype": _ALL_CHANGES, "Flower Gift": _NO_COPYING, "Illusion": _NO_TAKING, "Imposter": _NO_COPYING,
    "Zen Mode": _ALL_CHANGES, "Stance Change": _ALL_CHANGES, "Shields Down": _ALL_CHANGES,
    "Schooling": _ALL_CHANGES, "Disguise": _ALL_CHANGES, "Battle Bond": _ALL_CHANGES,
    "Power Construct": _ALL_CHANGES, "Comatose": _ALL_CHANGES, "Receiver": _NO_COPYING,
    "Power of Alchemy": _NO_COPYING, "RKS System": _ALL_CHANGES, "Gulp Missile": frozenset({"suppress"}),
    "Ice Face": _ALL_CHANGES, "Neutralizing Gas": _NO_TAKING, "Hunger Switch": _NO_TAKING,
    "As One (Glastrier)": _ALL_CHANGES, "As One (Spectrier)": _ALL_CHANGES, "Zero to Hero": _ALL_CHANGES,
    "Commander": _NO_TAKING, "Protosynthesis": _NO_TAKING, "Quark Drive": _NO_TAKING,
    "Embody Aspect (Teal)": _NO_TAKING, "Embody Aspect (Hearthflame)": _NO_TAKING,
    "Embody Aspect (Wellspring)": _NO_TAKING, "Embody Aspect (Cornerstone)": _NO_TAKING,
    "Tera Shift": _ALL_CHANGES, "Tera Shell": _NO_TAKING, "Teraform Zero": _NO_TAKING,
    "Poison Puppeteer": _NO_TAKING,
}


def refuses(ability, change):
    """Ability_ChangeFails: whether this ability refuses this kind of change."""
    return change in ABILITY_REFUSES.get(ability, ())


def raw_ability(mon):
    """The ability the battle's record holds (BATTLEMON_ABILITY), which the
    moves and abilities that change one read and write: under Neutralizing
    Gas or Gastro Acid, the one they have off."""
    if mon.gas_stash is not None:
        return mon.gas_stash
    if getattr(mon, "suppressed", False):
        return mon.suppress_stash
    return mon.ability


# The abilities that cure their holder's status or confusion at once
# (BattleSystem_RecoverStatusByAbility, run as each move ends and in the
# switch-in check), and what each cures. It matters only to a Pokemon that
# gains one while it has the status, which a changed ability can do.
ABILITY_CURES = {"Immunity": ("psn", "tox"), "Pastel Veil": ("psn", "tox"), "Limber": ("par",),
                 "Insomnia": ("slp",), "Vital Spirit": ("slp",), "Water Veil": ("brn",),
                 "Water Bubble": ("brn",), "Magma Armor": ("frz",),
                 "Purifying Salt": ("psn", "tox", "par", "slp", "brn", "frz")}


def ability_cures(mon):
    """BattleSystem_RecoverStatusByAbility for mon as its ability now reads:
    the status, confusion or love its ability forbids is cured, the message
    naming the ability."""
    if mon.status and mon.status in ABILITY_CURES.get(mon.ability, ()):
        mon.status, mon.sleep, mon.toxic = None, 0, 0
        reveal(mon)
    if mon.ability == "Own Tempo" and mon.confused:
        mon.confused = 0
        reveal(mon)
    if mon.ability == "Oblivious" and mon.infatuated:
        mon.infatuated = None
        reveal(mon)


def set_ability(b, mon, new, acted=True):
    """A script writes mon's ability (UpdateMonData on BATTLEMON_ABILITY,
    which also tells the trainer's AI, BattleAI_SetAbility), for as long as
    mon stays in: under Neutralizing Gas or Gastro Acid the new ability waits
    where the old one did. A Pokemon given Truant loafs on its next turn
    (the scripts set its parity from the turn count), so on this turn only
    if it has acted already (`acted`). Then its new ability may cure a status
    (ability_cures)."""
    if getattr(mon, "ability_was", None) is None:
        mon.ability_was = (raw_ability(mon),)
    if mon.gas_stash is not None:
        mon.gas_stash = new
    elif getattr(mon, "suppressed", False):
        mon.suppress_stash = new
    else:
        mon.ability = new
    mon.formed = True
    mon.revealed = new
    if new == "Truant":
        mon.loafing = acted
    ability_cures(mon)


def set_types(mon, types):
    """A move or an ability rewrites mon's types (BATTLEMON_TYPE_1 and _2)
    until it leaves: the battle's type checks read them at once, and its rows
    come from its twin of those types (form_key). "???" is the type a pure
    Fire Burn Up or pure Electric Double Shock user is left with, which no
    move's type meets."""
    mon.types = list(types)
    mon.retyped = mon.formed = True
    mon.row_types = tuple(types)


def suppress(b, mon):
    """Gastro Acid's and Core Enforcer's effect on mon (MOVE_EFFECT_ABILITY_SUPPRESSED):
    its ability reads as none until it leaves (Battler_Ability), its rows
    and Speed then its ability-blank twin's (form_key). It fails on an
    ability already suppressed, on one that refuses (refuses "suppress"),
    and on an Ability Shield's holder. Whether it took. Neutralizing Gas
    stops with its holder's (BattleSystem_NeutralizingGasActive), which the
    move's end then finds (gas_update)."""
    raw = raw_ability(mon)
    if getattr(mon, "suppressed", False) or refuses(raw, "suppress") or mon.item == "Ability Shield":
        return False
    mon.suppressed, mon.suppress_stash = True, raw
    mon.ability, mon.gas_stash = None, None
    mon.formed = True
    return True


def form_key(b, mon, mv=None, defending=False):
    """The key of the rows mon meets now that a move or an ability other than
    Protean has changed its types or its ability (prepare's form_twin): its
    twin of those types and that ability as the rows read it (row_ability),
    else its twin of the changed types alone, else of the changed ability
    alone. A Pokemon left with no type ("???") has a Normal and a Grass twin,
    as Roost's pure Flying one has: as the target, the one this move's type
    hits neutrally, which is how a typeless Pokemon is hit; as the attacker,
    the one of another type than the move's, so it takes no STAB. None
    while nothing has changed, or with no twin for the change."""
    if mon.row_types is None and mon.ability_was is None and not mon.suppressed:
        return None
    own = (b.st.get("form_twin") or {}).get(mon.key)
    if not own:
        return None
    ab = row_ability(mon.ability)
    for sig in ((mon.row_types, ab), (mon.row_types, own["ability"]), (None, ab)):
        if sig == (None, own["ability"]):
            return mon.key
        got = own["twins"].get(sig)
        if got is None:
            continue
        if isinstance(got, str):
            return got
        if mv is None:
            return got[0][0]
        for key, types in got:
            if (effectiveness(b.st["chart"], mv.type, types) == 1) if defending else mv.type not in types:
                return key
        return got[0][0]
    return None


# Each kind of change a fight can produce: a function of the fight's
# Pokemon (FormFight) that yields (key, types, ability) for each change the
# Pokemon of that key can undergo, types None where they stay its own and
# ability the one it is left with; a change that changes two Pokemon at once
# (Skill Swap, Wandering Spirit) yields its partner's as a fourth item, so
# the two twins are rowed against each other. The fixes add their own
# (form_change).
FORM_CHANGES = []


def form_change(fn):
    FORM_CHANGES.append(fn)
    return fn


class FormFight:
    """What FORM_CHANGES read of a fight being prepared: its Pokemon by key,
    their moves, sides, foes, types and abilities, its weathers and the type
    its terrain gives Camouflage."""

    def __init__(self, pokemon, moves, blob, pkeys, qkeys, bkeys, weathers, camouflage):
        self.pokemon, self.move_names, self.blob = pokemon, moves, blob
        self.pkeys, self.qkeys, self.bkeys = list(pkeys), list(qkeys), list(bkeys)
        self.weathers, self.camouflage = weathers, camouflage

    def keys(self):
        return self.pkeys + self.qkeys + self.bkeys

    def foes(self, k):
        """The keys k can face: the trainer's for the player's and a
        partner's Pokemon, theirs for the trainer's."""
        return self.bkeys if k[0] in "pq" else self.pkeys + self.qkeys

    def allies(self, k):
        """The other Pokemon of k's side (a variant of k, the same Pokemon
        with its other ability, left out)."""
        side = self.bkeys if k[0] == "b" else self.pkeys + self.qkeys
        return [g for g in side if g.split("~")[0] != k.split("~")[0]]

    def ability(self, k):
        return self.pokemon[k].get("ability")

    def types(self, k):
        own = self.pokemon[k].get("species_data") or self.blob["poks"].get(self.pokemon[k]["species"]) or {}
        return [t for t in (own.get("types") or []) if t]

    def moves(self, k):
        return [move(m) for m in self.move_names.get(k, ())]

    def contact(self, k):
        """Whether k has a damaging move that makes contact (makes_contact:
        none for a Long Reach holder)."""
        return self.ability(k) != "Long Reach" and any(mv.contact and mv.damaging() for mv in self.moves(k))

    def hit_types(self, k):
        """The types k's damaging moves can hit with: Weather Ball in each of
        the fight's weathers, Hidden Power and Natural Gift as the Pokemon's
        IVs and item make them, and Normalize, Pixilate and Liquid Voice as
        they turn a move (move_type_used)."""
        rec, out = self.pokemon[k], set()
        for mv in self.moves(k):
            if not mv.damaging():
                continue
            if mv.name == "Weather Ball" and rec.get("ability") != "Normalize":
                out |= {WEATHER_BALL_TYPE.get(w, "Normal") for w in self.weathers}
            else:
                out.add(move_type_used(rec.get("ability"), mv, rec.get("ivs"), rec.get("item"), None))
        return out


# Weather Ball's type in each weather (BattleSystem_CalcMoveType).
WEATHER_BALL_TYPE = {"Sun": "Fire", "Rain": "Water", "Hail": "Ice", "Sand": "Rock"}
# The Normal moves Pixilate leaves alone (battle_lib.c, sMovesKeepTheirType).
KEEP_TYPE = frozenset({"MOVE_HIDDEN_POWER", "MOVE_WEATHER_BALL", "MOVE_NATURAL_GIFT", "MOVE_JUDGMENT",
                       "MOVE_TECHNO_BLAST", "MOVE_MULTI_ATTACK", "MOVE_TERRAIN_PULSE", "MOVE_STRUGGLE"})


def move_type_used(ability, mv, ivs, item, weather):
    """The type a move hits with as the battle records it (battleCtx->moveType,
    which Color Change reads): Normalize makes every move Normal; Weather Ball
    the weather's; Hidden Power the IVs'; Natural Gift the Berry's; Pixilate
    a Normal move with power Fairy and Liquid Voice a sound move Water
    (BattleSystem_SetMoveTypeByAbility); every other move its own type."""
    if ability == "Normalize":
        return "Normal"
    if mv.name == "Weather Ball":
        return WEATHER_BALL_TYPE.get(weather, "Normal")
    if mv.effect == "RANDOM_POWER_BASED_ON_IVS":
        return fightai.hidden_power_type(ivs) or mv.type
    if mv.name == "Natural Gift":
        return (fightai._gift_type(item) if item else None) or mv.type
    if ability == "Pixilate" and mv.type == "Normal" and mv.power and mv.const not in KEEP_TYPE:
        return "Fairy"
    if ability == "Liquid Voice" and mv.const in fightai.SOUND_MOVES:
        return "Water"
    return mv.type


def form_twins(ff, pairs, hits_of, spread, whole_field, gas_twin):
    """The twins for every change FORM_CHANGES finds in the fight ff:
    {key: {"ability": its own ability as rows read it, "twins": {(types,
    ability): twin key, or ((key, types), ...) for no type}}}. Each twin is
    the Pokemon's record with that ability (row_ability's, or the stand-in)
    and, for changed types, species_data with exactly those types (its own
    stats and weight kept, as Roost's twins have them); twins of one
    Pokemon's two variants are shared, since only the ability differs, and
    an ability-blank one is Neutralizing Gas's twin where that exists. Each
    twin is rowed both ways in every weather against every foe, a player's
    Magnitude at each power included, in a double battle against its
    allies' spread moves, and against the twin of a change's partner. Two
    changes made apart from each other on both sides at once read the one
    change against the other's own rows (Battle.row). The rows are appended
    to `pairs`."""
    def sig_of(types, ability):
        return (tuple(types) if types else None, row_ability(ability))
    want, links = collections.defaultdict(set), set()
    for fn in FORM_CHANGES:
        for item in fn(ff):
            k, sig = item[0], sig_of(item[1], item[2])
            if sig != (None, row_ability(ff.ability(k))):
                want[k].add(sig)
            if len(item) > 3:
                f, fsig = item[3][0], sig_of(item[3][1], item[3][2])
                if fsig != (None, row_ability(ff.ability(f))):
                    want[f].add(fsig)
                links.add(((k, sig), (f, fsig)))
    out, made, named = {}, {}, {}
    for k in sorted(want):
        root = k.split("~")[0]
        rec = ff.pokemon[k]
        own = dict(rec.get("species_data") or ff.blob["poks"].get(rec["species"]) or {})
        entry = {"ability": row_ability(ff.ability(k)), "twins": {}}
        for types, ab in sorted(want[k], key=repr):
            choices = ([("Normal",), ("Grass",)] if types == ("???",) else [types])
            got = []
            for tt in choices:
                name = f"{root}#fm{'/'.join(tt) if tt else ''}@{ab or ''}"
                if tt is None and ab is None and gas_twin.get(k):
                    name = gas_twin[k]
                if name not in ff.pokemon:
                    twin = dict(rec, ability=ab or WEATHER_STAND_IN)
                    if tt:
                        data_ = {"bs": dict(own.get("bs") or {}), "types": list(tt), "exact_types": True}
                        if own.get("weightkg") is not None:
                            data_["weightkg"] = own["weightkg"]
                        twin["species_data"] = data_
                    ff.pokemon[name] = twin
                made.setdefault(k, [])
                if name not in made[k]:
                    made[k].append(name)
                got.append((name, list(tt) if tt else None))
            entry["twins"][(types, ab)] = got[0][0] if len(got) == 1 else tuple(got)
            named[(k, (types, ab))] = [n for n, _t in got]
        out[k] = entry
    seen = {(a, d, w) for a, d, _m, w in pairs}

    def add(a, d, mv, w):
        if mv and (a, d, w) not in seen:
            seen.add((a, d, w))
            pairs.append([a, d, mv, w])
    for k in sorted(made):
        for t in made[k]:
            for w in ff.weathers:
                for d in ff.foes(k):
                    add(t, d, hits_of(k), w)
                    add(d, t, hits_of(d), w)
                    if "Magnitude" in ff.move_names.get(d, ()):     # a trainer's power keys too, since 2026-10-15
                        for p in MAGNITUDE_POWERS:
                            add(f"{d}#m{p}", t, ["Magnitude"], w)
                if whole_field:
                    for a in ff.allies(k):
                        add(a, t, spread(a), w)
                        add(t, a, spread(k), w)
    for (k, sig), (f, fsig) in sorted(links, key=repr):
        for t in named.get((k, sig), []):
            for u in named.get((f, fsig), []):
                for w in ff.weathers:
                    add(t, u, hits_of(k), w)
                    add(u, t, hits_of(f), w)
    return out


def gas_on(b):
    """BattleSystem_NeutralizingGasActive: a holder with HP on the field. The
    engine works it out afresh at every read, so the gas starts and stops
    with its holder's arrival, fainting or leaving."""
    return any(m.ability == "Neutralizing Gas" and m.alive() for m in b.p.on_field() + b.b.on_field())


def gas_key(b, mon):
    """The calculator's key for mon's rows and Speed while the gas has its
    ability off: its ability-blank twin (prepare's st["gas_twin"]), or its own
    key where the twin would read the same."""
    return (b.st.get("gas_twin") or {}).get(mon.key, mon.key)


def gas_update(b, check=True):
    """Neutralizing Gas as the battle stands now. While a holder with HP is
    on the field every other battler's ability reads as none (Battler_Ability):
    it waits in gas_stash, save an Ability Shield holder's and the GAS_PROOF
    ones. Once no holder is, each comes back. With `check`, the switch-in
    check's gas step follows (SWITCH_IN_CHECK_STATE_NEUTRALIZING_GAS): a gas
    on the field is noted (FIELD_CONDITION_NEUTRALIZING_GAS), and once a
    noted gas has gone every battler on the field sets off its entry
    abilities again, fastest first, as the engine resets their announcements.
    Returns whether that happened. The engine runs the check when a move
    ends (BattleControllerPlayer_MoveEnd) and when a Pokemon comes in, so a
    holder knocked out by a move takes its re-announced Intimidate into an
    empty slot, while one that leaves or falls at the turn's end has it land
    on the Pokemon that replaces it."""
    on = gas_on(b)
    for m in b.p.on_field() + b.b.on_field():
        if on:
            if m.gas_stash is None and m.ability and m.ability not in GAS_PROOF and m.item != "Ability Shield":
                m.gas_stash, m.ability = m.ability, None
        elif m.gas_stash is not None:
            m.ability, m.gas_stash = m.gas_stash, None
    if not check:
        return False
    if on:
        b.gas_flag = True
        return False
    if getattr(b, "gas_flag", False):
        b.gas_flag = False
        mons = [m for m in b.p.on_field() + b.b.on_field() if m.alive()]
        entry_abilities(b, sorted(mons, key=b.speed, reverse=not b.trick_room))
        return True
    return False


def trace(b):
    """The switch-in check's Trace step (SWITCH_IN_CHECK_STATE_TRACE), over
    every Pokemon on the field, fastest first: a Trace holder that has not
    traced since it came in (traceAnnounced), standing and holding no
    Griseous Orb, copies the ability of a foe on the field that stands and
    whose ability does not refuse Trace (ChooseTraceTarget, which in a
    double battle picks between two such foes at random); the message names
    both abilities (subscript_trace). With no such foe it waits, and the
    check, which runs again as every move ends and each Pokemon comes in,
    tries again then. The holders that traced, in that order. Until
    2026-10-14 Trace was only announced (Ian approved the fix)."""
    out = []
    field = [m for m in b.p.on_field() + b.b.on_field() if m.alive()]
    if not any(m.ability == "Trace" and not m.traced for m in field):
        return out
    for m in sorted(field, key=b.speed, reverse=not b.trick_room):
        if m.ability != "Trace" or m.traced or m.item == "Griseous Orb" or not m.alive():
            continue
        foes = [f for f in (b.b if m.side == "p" else b.p).on_field()
                if f.alive() and not refuses(raw_ability(f), "trace")]
        if not foes:
            continue
        target = foes[1] if len(foes) > 1 and coin(b, "trace") else foes[0]
        m.traced = True
        set_ability(b, m, raw_ability(target), acted=getattr(m, "acted_turn", None) == b.turn)
        target.revealed = raw_ability(target)
        out.append(m)
    return out


@form_change
def _traced(ff):
    """Trace: its holder can copy the ability of any foe it faces that does
    not refuse Trace."""
    for k in ff.keys():
        if ff.ability(k) == "Trace":
            for f in ff.foes(k):
                if not refuses(ff.ability(f), "trace"):
                    yield k, None, ff.ability(f)


def entry_abilities(b, mons, intimidate=True, trace_now=True):
    """The switch-in check's ability steps for these Pokemon, each step over
    all of them in the order given (monSpeedOrder): Trace over the whole
    field first (trace), whose holders then join the steps after it with the
    ability they copied; the weather abilities, the announcement the
    trainer's AI reads (BattleAI_SetAbility), Intimidate, then Download. The
    battle's leads leave Trace, Intimidate and Download to open_battle
    (trace_now and intimidate False), as those read the foes on the field."""
    if trace_now:
        mons = list(mons) + [m for m in trace(b) if m not in mons]
    for new in mons:
        weather = ABILITY_WEATHER.get(new.ability)
        if weather:
            b.weather, b.weather_turns = weather, 0
            if b.fog:
                b.fog = False        # the ability's subscript clears every weather, deep fog too
    for new in mons:
        if new.ability in ENTRY_ANNOUNCED:
            reveal(new)
    if intimidate:
        intimidate_foes(b, mons)
        for new in mons:
            download(b, new)
    for new in mons:
        if new.ability == "Screen Cleaner" and new.alive():
            screen_cleaner(b, new)       # Oxide's abilities' step, after Download
        elif new.ability == "Hospitality" and new.alive() and b.doubles:
            hospitality(b, new)
        elif new.ability == "Pastel Veil" and new.alive() and b.doubles:
            ally = ally_of(b, new)
            if ally is not None and ally.status in ("psn", "tox"):
                # BattleSystem_TriggerEffectOnSwitch's Oxide abilities,
                # subscript_pastel_veil: a poisoned partner is cured as the
                # holder comes in. Until 2026-10-21 it was not (Ian approved
                # the double-battle part batch 11 left on 2026-10-14).
                ally.status, ally.toxic = None, 0
                reveal(new)
    forecast(b)                          # the check's form step comes after these


def hospitality(b, mon):
    """Hospitality (BattleSystem_TriggerEffectOnSwitch's Oxide abilities,
    subscript_hospitality): as its holder comes in, in a double battle, its
    standing partner below full HP gets back a quarter of its maximum HP
    (BattleSystem_Divide). In a single battle it has no partner. Until
    2026-10-21 it did nothing (Ian approved the double-battle part batch 11
    left on 2026-10-14)."""
    ally = ally_of(b, mon)
    if ally is not None and ally.hp < ally.maxhp:
        heal(ally, engine_divide(ally.maxhp, 4))
        reveal(mon)


def screen_cleaner(b, mon):
    """Screen Cleaner (SWITCH_IN_CHECK_STATE_OXIDE_ABILITIES, once as its
    holder comes in): Reflect, Light Screen and Aurora Veil end on both
    sides; with none up it says nothing. Until 2026-10-20 it did nothing
    (Ian approved the fix)."""
    sides = (b.p, b.b)
    if any(any(sd.screens.values()) or sd.aurora_veil for sd in sides):
        for sd in sides:
            sd.screens = dict.fromkeys(sd.screens, 0)
            if sd.aurora_veil:
                sd.aurora_veil = 0
        reveal(mon)


def download(b, mon):
    """Download's step of the switch-in check (SWITCH_IN_CHECK_STATE_DOWNLOAD),
    once a stay on the field: the foes on the field with HP and no
    Substitute have their Defense and their Sp. Def added up, each at its
    stage (sStatStageBoosts); a Defense total no lower raises its holder's
    Sp. Atk a stage, a lower one its Attack, through the stat-stage subscript
    (so Simple doubles it); with no such foe, nothing. prepare() keeps it
    out of the calculator's rows (CALC_ABILITY_OFF), which picked the stat
    again for each defender and never made it a stage Haze or a switch
    clears. Until 2026-10-14 the battle only announced it (Ian approved the
    fix)."""
    if mon.ability != "Download" or not mon.alive():
        return
    foes = [f for f in (b.b if mon.side == "p" else b.p).on_field() if f.alive() and not f.sub]
    if not foes:
        return
    defense = sum(int(f.stats.get("def", 0) * stage_mult(f.stages["def"])) for f in foes)
    sp_def = sum(int(f.stats.get("spd", 0) * stage_mult(f.stages["spd"])) for f in foes)
    if defense + sp_def:
        change_stages(mon, {"spa" if defense >= sp_def else "atk": 1})


def intimidate_foes(b, mons):
    """Intimidate's step of the switch-in check for these Pokemon, in the
    order given: one Attack stage off each foe on the field, through what any
    drop from the other side meets (lower_stats: the blockers, Mirror Armor,
    Defiant and Competitive). This stage is Intimidate's only effect, since
    prepare() keeps it out of the calculator's rows (CALC_ABILITY_OFF). Then
    a Rattled foe gains a stage of Speed, whether or not its Attack fell
    (subscript_intimidate, Generation 8's rule), raised directly, so Simple
    does not double it (AbilityStatChange). Until 2026-10-14 Mirror Armor,
    Defiant, Competitive and Rattled did nothing here (Ian approved the
    fix)."""
    for new in mons:
        if new.ability == "Intimidate":
            for foe in (b.b if new.side == "p" else b.p).on_field():
                # subscript_intimidate passes over a foe behind a Substitute.
                if foe.alive() and not foe.sub:
                    lower_stats(b, new, foe, {"atk": -1}, intimidate=True)
                    if foe.ability == "Rattled" and foe.alive():
                        raise_own(foe, "spe", 1)


# The abilities Oxide's engine lets stop Intimidate beside those that stop
# any lowering of Attack (BtlCmd_ChangeStatStage, Generation 8's rule):
# Inner Focus, Own Tempo, Oblivious and Scrappy. The game's other answers to
# Intimidate (Mirror Armor, Defiant, Competitive, Rattled) meet it in
# lower_stats and intimidate_foes.
INTIMIDATE_PROOF = frozenset({"Inner Focus", "Own Tempo", "Oblivious", "Scrappy"})
# Defiant and Competitive answer each stat another side lowers with two
# stages of this one (BtlCmd_TryDefiant).
DEFIANT_STAT = {"Defiant": "atk", "Competitive": "spa"}


def raise_own(mon, stat, stages):
    """A stat an ability raises on its own holder (AbilityStatChange, or
    TryDefiant's direct raise): the stages straight on, so Simple does not
    double them, nothing at +6 or with no HP; the message names the
    ability. Whether it rose."""
    if not mon.alive() or mon.stages[stat] >= 6:
        return False
    mon.stages[stat] = min(6, mon.stages[stat] + stages)
    mon.stat_raised = True
    reveal(mon)
    return True


def ability_stages(holder, mon, stat, stages):
    """A stat an ability changes (AbilityStatChange, which Weak Armor, Water
    Compaction, Gooey, Moody and the other abilities' subscripts call): mon's
    stage moves by `stages`, held within -6 and +6, made directly, so Simple
    does not double it, Contrary does not turn it, and Mist and Mirror Armor
    do not stop it. Nothing happens to a Pokemon with no HP or a stage
    already at the limit, and a drop that another Pokemon's ability makes is
    kept off by Clear Body, White Smoke or a Clear Amulet, in silence. The
    message names the holder's ability. Whether the stage moved."""
    if not mon.alive():
        return False
    now = max(-6, min(6, mon.stages[stat] + stages))
    if now == mon.stages[stat]:
        return False
    if stages < 0 and mon is not holder and (mon.ability in ("Clear Body", "White Smoke")
                                             or mon.item == "Clear Amulet"):
        return False
    mon.stages[stat] = now
    if stages > 0:
        mon.stat_raised = True
    reveal(holder)
    return True


def lower_stats(b, src, mon, changes, intimidate=False):
    """src's move or ability lowering mon's stats from the other side, one
    stat at a time in the order given, as each of the subscripts' calls to
    BtlCmd_ChangeStatStage takes one. Mirror Armor (unless src has Mold
    Breaker) turns a drop back on src while src stands, which then takes it
    as its own: no blocker of its own side checked and no Defiant. Otherwise
    the drop meets stat_drop_blocked, does nothing at -6, and once it lands
    (Simple doubling it) a Defiant or Competitive holder answers with two
    stages of Attack or Sp. Atk (TryDefiant, once a stat). The stats that
    fell. Until 2026-10-14 a change of several stats was blocked or let
    through whole, so Hyper Cutter stopped Tickle's Defense drop with its
    Attack one, and Mirror Armor and Defiant did nothing (Ian approved the
    fix)."""
    fell = []
    for stat, v in changes.items():
        if v >= 0:
            change_stages(mon, {stat: v})
            continue
        if mon.ability == "Contrary" and not mold(src, mon):
            # Contrary turns the drop into a rise before anything that
            # stops a drop is asked (BtlCmd_ChangeStatStage), so Mist, the
            # blockers and Mirror Armor play no part and Defiant has none
            # to answer.
            change_stages(mon, {stat: v})
            continue
        if (src is not None and src is not mon and src.side != mon.side and src.alive()
                and mon.ability == "Mirror Armor" and src.ability != "Mold Breaker"):
            if src.stages[stat] > -6:
                change_stages(src, {stat: v}, simple=False)
            continue
        if stat_drop_blocked(b, mon, {stat: v}, src=src, intimidate=intimidate) or mon.stages[stat] <= -6:
            continue
        change_stages(mon, {stat: v}, simple=not mold(src, mon))     # Mold Breaker gets past Simple too
        fell.append(stat)
        if src is not None and src.side != mon.side and mon.ability in DEFIANT_STAT:
            raise_own(mon, DEFIANT_STAT[mon.ability], 2)
    return fell


def open_battle(b):
    """The battle's start (BATTLE_CONTROL_SHOW_BATTLE_MON): every lead comes
    in first, and only then does the switch-in check run over all of them,
    fastest first (BattleSystem_TriggerEffectOnSwitch by monSpeedOrder), so
    each side's Intimidate lands on the other side's leads. Sending the leads
    in one after another, as the battles did until 2026-10-13, let the
    player's lead's own switch-in reset the stage a trainer lead's Intimidate
    had just taken off it. The weather and the announcements go off as each
    lead comes in, as before: only a trainer lead has a weather ability, and
    in a double battle the trainers' leads keep the order they had."""
    leads = []
    for side in (b.b, b.p):
        switch_in(b, side, side.active, lead=True)
        leads.append(side.mons[side.active])
        if side.active2 is not None:
            switch_in(b, side, side.active2, slot=1, lead=True)
            leads.append(side.mons[side.active2])
    ordered = sorted(leads, key=b.speed, reverse=not b.trick_room)
    # Trace first, once every lead is in; a traced weather ability then sets
    # its weather before the leads' Intimidate and Download go off.
    entry_abilities(b, trace(b), intimidate=False, trace_now=False)
    intimidate_foes(b, ordered)
    for lead in ordered:
        download(b, lead)                # after Intimidate, as the switch-in check runs them
    forecast(b)


def stat_drop_blocked(b, mon, changes, src=None, intimidate=False):
    """Whether a drop from the other side is stopped, in BtlCmd_ChangeStatStage's
    order: Mist on mon's side, which an Infiltrator `src` passes; a Clear
    Amulet (Oxide, element 7); then mon's ability, named as it stops it:
    Clear Body and White Smoke any drop, with `intimidate` Inner Focus, Own
    Tempo, Oblivious and Scrappy, Hyper Cutter an Attack drop, Keen Eye an
    accuracy drop, Big Pecks a Defense drop. Mist and the Amulet were
    added on 2026-10-14 (Ian approved the fix)."""
    falls = {k for k, v in changes.items() if v < 0}
    if not falls:
        return False
    side = b.p if mon.side == "p" else b.b
    if getattr(side, "mist", 0) and (src is None or src.ability != "Infiltrator"):
        return True
    if mon.ability == "Flower Veil" and "Grass" in mon.types and not mold(src, mon):
        # Oxide's Flower Veil keeps the other side from lowering a Grass-type
        # holder's stats, after Mist; its message names no ability. Until
        # 2026-10-20 it did nothing (Ian approved the fix).
        return True
    if b.doubles and "Grass" in mon.types:
        # And a Grass-type partner's, in a double battle (PartnerHasFlowerVeil:
        # a standing partner, unless a Mold Breaker gets past it). Until
        # 2026-10-21 the partner had no shield (Ian approved the
        # double-battle part batch 11 left on 2026-10-14).
        ally = ally_of(b, mon)
        if ally is not None and ally.ability == "Flower Veil" and not mold(src, ally):
            return True
    if mon.item == "Clear Amulet":
        return True
    # A Mold Breaker src gets past the abilities (AbilityBlocksSpecificStatReduction
    # and the Clear Body test ask Battler_IgnorableAbility).
    ab = None if mold(src, mon) else mon.ability
    if ab in ("Clear Body", "White Smoke") or (intimidate and ab in INTIMIDATE_PROOF) \
            or (ab == "Hyper Cutter" and falls <= {"atk"}) \
            or (ab == "Keen Eye" and falls <= {"acc"}) or (ab == "Big Pecks" and falls <= {"def"}):
        reveal(mon)
        return True
    return False


def take_heart(att):
    """Take Heart (effect script 367, subscript_take_heart, a direct effect
    on its user): a stage each of Sp. Atk and Sp. Def, unless both are at +6
    already, and then, whether they rose or not, the user's status is cured
    (MON_CONDITION_NONE, with a sleep's turns and Toxic's count). Until
    2026-10-20 the stages rose and the status stayed (Ian approved the
    fix)."""
    if not (att.stages["spa"] == 6 and att.stages["spd"] == 6):
        change_stages(att, SELF_STAGES["TAKE_HEART"])
    if att.status:
        att.status, att.sleep, att.toxic = None, 0, 0


def spicy_extract(b, att, dfn, mv):
    """Spicy Extract (effect script 302, subscript_spicy_extract, a direct
    effect on a target left standing): its Attack rises two stages, then
    its Defense falls two, each through BtlCmd_ChangeStatStage, which works
    out Simple and Contrary first (a Mold Breaker user gets past both).
    Only a fall meets the blockers: a rise passes a Substitute and Mist,
    while the fall stops at a Substitute (an Infiltrator's passes,
    sub_blocks) and meets Mirror Armor, Mist, Flower Veil, the Clear Amulet,
    Clear Body, Big Pecks and Defiant as any drop does (lower_stats). Under
    Contrary the two swap: the Attack falls, past those same checks, and
    the Defense rises. Until 2026-10-20 the move did nothing (Ian approved
    the fix)."""
    if not dfn.alive():
        return
    sub = sub_blocks(att, dfn, mv)
    if dfn.ability == "Contrary" and not mold(att, dfn):
        if not sub and dfn.stages["atk"] > -6 and not stat_drop_blocked(b, dfn, {"atk": -2}, src=att):
            change_stages(dfn, {"atk": 2})       # Contrary's fall (CHANGE_MULT)
        change_stages(dfn, {"def": -2})          # and its rise
        return
    change_stages(dfn, {"atk": 2}, simple=not mold(att, dfn))
    if not sub:
        lower_stats(b, att, dfn, {"def": -2})


def mist(side):
    """Mist (BtlCmd_TryMist): five turns in which the other side's moves and
    abilities cannot lower the stats of this side's Pokemon
    (stat_drop_blocked), counted down at each turn's end; it fails while
    one runs. Until 2026-10-14 the move did nothing (Ian approved the fix)."""
    if not side.mist:
        side.mist = 5


# The powder and spore moves (battle_lib.c, sPowderMoves): Grass types and
# Overcoat are immune to them in Oxide (Generation 6).
POWDER = {"Cotton Spore", "Poison Powder", "Sleep Powder", "Stun Spore", "Spore", "Powder",
          "Rage Powder", "Magic Powder"}


def powder_immune(target, mv, att=None):
    """A Grass type meets no powder or spore move, and Overcoat none unless
    att has Mold Breaker (BattleSystem_TriggerImmunityAbility asks
    Battler_IgnorableAbility; the Grass type's immunity is the type's)."""
    return mv.name in POWDER and ("Grass" in target.types or (target.ability == "Overcoat" and not mold(att, target)))


def leaf_guarded(b, target):
    """Leaf Guard keeps every major status off its holder in sun, unless a
    Mold Breaker's move gives it. The engine knows it; the AI does not, so
    this is not part of can_status."""
    return (target.ability == "Leaf Guard" and b.weather == "Sun" and not status_ability_ignored(b, target)
            and not weather_ignored(b))


def veil_partner(b, target, status):
    """The standing partner whose Sweet Veil or Pastel Veil keeps this status
    off target in a double battle (the status subscripts' CHECK_HAVE_ON_SIDE),
    unless a Mold Breaker's move gets past the partner's ability
    (CheckIgnorableAbility; Toxic Spikes' check is not ignorable, and its
    status has no source), or None. Until 2026-10-21 neither shielded the
    partner (Ian approved the double-battle parts batch 11 left on
    2026-10-14)."""
    ally = ally_of(b, target)
    if ally is not None and ally.ability == PARTNER_STATUS_VEIL.get(status) \
            and not mold(getattr(b, "status_src", None), ally):
        return ally
    return None


def give_status(b, target, status):
    if not can_status(b, target, status) or leaf_guarded(b, target):
        if target.alive() and not target.status and not status_ability_ignored(b, target) \
                and (target.ability in STATUS_ABILITIES.get(status, ()) or leaf_guarded(b, target)):
            reveal(target)
        elif b.doubles and target.alive() and not target.status:
            veil = veil_partner(b, target, status)
            if veil is not None:
                reveal(veil)         # the message names the partner's veil
        return False
    target.status = status
    if status == "slp":
        target.sleep = b.rng.randint(1, 4)
    if status == "tox":
        target.toxic = 0
    charge_ends(target, status)      # asleep or frozen, its charge is over
    synchronize(b, target, status)
    cure_berry(target, b)
    return True


# How BtlCmd_ChangeStatStage scales a change by its target's ability:
# Simple doubles it (Generation 5), and Contrary turns it round, from any
# source, a rise into a fall and a fall into a rise.
CHANGE_MULT = {"Simple": 2, "Contrary": -1}


def change_stages(mon, changes, simple=True):
    # Simple doubles every change to its own stages and Contrary turns it
    # round (CHANGE_MULT), as BtlCmd_ChangeStatStage makes a move's, an
    # item's and Intimidate's changes; a drop Mirror Armor turns back keeps
    # the size it had, and one a Mold Breaker makes meets neither (simple
    # False). Contrary did nothing until 2026-10-20 (Ian approved the fix).
    mult = CHANGE_MULT.get(getattr(mon, "ability", None), 1) if simple else 1
    for k, v in changes.items():
        before = mon.stages[k]
        mon.stages[k] = max(-6, min(6, mon.stages[k] + v * mult))
        if mon.stages[k] > before:
            # A stage that rose this turn (TurnFlags.statRaised), which
            # Burning Jealousy reads; cleared at the turn's end and on a
            # switch-in.
            mon.stat_raised = True
    # A White Herb puts every lowered stage back to 0, once.
    if getattr(mon, "item", None) == "White Herb" and any(s < 0 for s in mon.stages.values()):
        mon.stages = {k: max(0, s) for k, s in mon.stages.items()}
        consume(mon)


ROLLOUT = "DOUBLE_POWER_EACH_TURN_LOCK_INTO"   # Rollout and Ice Ball
# The effects that hit exactly twice (SetMultiHit 2 in effect scripts 44, 77
# and 296): Double Kick, Dual Wingbeat and the other HIT_TWICE moves,
# Twineedle and Double Iron Bash.
TWO_HITS = frozenset({"HIT_TWICE", "POISON_MULTI_HIT", "HIT_TWICE_AND_FLINCH"})
# The moves of three hits at their listed power, one accuracy check for
# the three (SetMultiHit 3, SYSCTL_MULTI_HIT_MOVE): Triple Dive (effect
# script 299) and Surging Strikes (366), whose calculator rows add up the
# three, Surging Strikes' each critical (Move.sure: BattleSystem_CalcCrit
# makes every one of its hits critical, unless Battle Armor, Shell Armor or
# Lucky Chant keeps it off). Until 2026-10-20 each landed as one hit holding
# the row's three (Ian approved the fixes).
THREE_HITS = frozenset({"HIT_THREE_TIMES_FIXED_POWER", "HIT_THREE_TIMES_ALWAYS_CRITICAL"})
# Population Bomb (effect script 297): SetMultiHit 10 with Triple Kick's
# flags, so up to ten hits at the listed power, each after the first
# checking accuracy again but skipping the hit overrides
# (SYSCTL_SKIP_ACCURACY_OVERRIDES: No Guard and Lock-On do not land it),
# the move stopping at the first miss; a Loaded Dice makes it four to ten
# hits evenly (10 - Random % 7) with no later checks (BtlCmd_SetMultiHit),
# and Skill Link changes nothing. The calculator's row adds up two hits,
# ten with Skill Link or a Grip Claw (row_hits). Until 2026-10-20 it landed
# as one hit holding the row's two (Ian approved the fix).
TEN_HITS = "UP_TO_10_HITS"
TEN_LOADED = tuple((h, 1) for h in range(4, 11))
# Every effect whose hits the engine lands one at a time and the calculator's
# row adds up (SetMultiHit in effect scripts 29, 44, 77, 296, 297, 298, 299
# and 416): the two to five hit moves, the two-hit and three-hit moves, the
# three rising ones and Population Bomb; Beat Up lands its own
# (beat_up_hits).
HIT_BY_HIT = frozenset({"MULTI_HIT", "HIT_TWICE", "POISON_MULTI_HIT", "HIT_TWICE_AND_FLINCH",
                        "HIT_THREE_TIMES_RISING_10", "HIT_THREE_TIMES_INCREMENT_BASE_POWER_20",
                        TEN_HITS}) | THREE_HITS
# The secondary effect each of the two-hit kin rolls once a hit (effect
# scripts 77 and 296 set it for every hit): Twineedle's poison and Double
# Iron Bash's flinch, at the move's chance.
HIT_BY_HIT_EFFECT = {"POISON_MULTI_HIT": "psn", "HIT_TWICE_AND_FLINCH": "flinch"}


def flinch_item(att):
    """Whether att's hits carry King's Rock's one in ten to flinch
    (BattleControllerPlayer_CheckExtraFlinch): a King's Rock or Razor Fang,
    or Stench, which counts as a King's Rock when its holder has none and
    does not add to one (Generation 5). Stench did nothing until 2026-10-14
    (Ian approved the fix)."""
    return att.item in ("King's Rock", "Razor Fang") or att.ability == "Stench"


def item_flinch_blocked(att, dfn):
    """Whether dfn shrugs off the flinch of att's King's Rock, Razor Fang or
    Stench (subscript_flinch_mon, whose side effect is then indirect):
    Shield Dust, which Mold Breaker gets past, or a Covert Cloak. Until
    2026-10-14 both let it through (Ian approved the fix)."""
    return (dfn.ability == "Shield Dust" and not mold(att, dfn)) or dfn.item == "Covert Cloak"


def hit_weights(att, mv, hits):
    """Each landed hit's share of the calculator's row, as whole-number
    weights, and the row's whole weight: the row adds up row_hits equal hits
    for a two to five hit move, two for the two-hit moves, and a rising
    move's three hits at their powers."""
    if mv.effect in RISING:
        powers = rising_powers(mv)
        return powers[:hits], sum(powers)
    total = row_hits(att, mv) if mv.effect in ("MULTI_HIT", TEN_HITS) or mv.effect in THREE_HITS else 2
    return [1] * hits, total


def land_hits(b, att, dfn, mv, first, hits, hit_damage, crits, chance, pick):
    """A move of several hits landed as the engine's multi-hit loop lands it
    (BattleControllerPlayer_LoopMultiHit): the move's script runs again for
    each hit, so each has its own damage and critical hit (hit_damage(i,
    crit) works the i-th hit out as it comes, crits[i] its critical hit),
    and each takes its own HP update and after-effects before the next. The
    loop stops once a Pokemon has fainted, the target or the attacker (to
    Rough Skin), or once the attacker is asleep (Effect Spore).

    Each hit's HP update (BattleControllerPlayer_UpdateHP): a Substitute
    takes the hit, and once it breaks the next hits land on the Pokemon
    behind it; but after any hit on it this move, no later hit sets off an
    on-hit ability or an added effect (SELF_TURN_FLAG_SUBSTITUTE_HIT lasts
    the move). Sturdy holds a hit taken at full HP, so only the first. A
    Focus Sash is armed by a hit taken at full HP, and a Focus Band's one in
    ten is rolled at every hit; either, once armed, holds that hit and every
    later one at 1 HP (focusItemActivated, a self turn flag cleared only when
    the move is over), and the Sash is used up at the move's end if it held
    one (subscript_move_followup_message). Endure holds every hit.

    Then, hit by hit: the resist berry that halved the hit is used up, the
    two-hit kin's added effect rolls, Rage rises, the target's on-hit ability
    answers a contact hit (contact_ability, `chance` and `pick` the battle's
    dice), King's Rock rolls, the target's berry is checked, and a Fire hit
    thaws it. Until 2026-10-14 the move landed as one hit, with one critical
    roll, one contact chance and one Sash or Band check (Ian approved the
    fix). Returns the HP the hits took from dfn, its Substitute's aside."""
    sturdy = dfn.ability == "Sturdy" and att.ability != "Mold Breaker"
    armed = held = sub_hit = False
    stripped = sheer_force_strips(att, mv)
    added = HIT_BY_HIT_EFFECT.get(mv.effect)
    total = 0
    for i in range(hits):
        if i and (not dfn.alive() or not att.alive() or att.status == "slp"):
            break
        dmg = hit_damage(i, crits[i])
        if sub_blocks(att, dfn, mv):
            dfn.sub = max(0, dfn.sub - dmg)
            sub_hit = b.sub_hit = True   # and the move's own effects after the hits (_after_attack)
            if crits[i]:
                anger_point(dfn)         # the hit's critical message comes all the same
            continue
        enduring = getattr(dfn, "enduring", False)
        on_sturdy = False
        if not enduring:
            if sturdy and dfn.hp == dfn.maxhp:
                on_sturdy = True
            else:
                if dfn.item == "Focus Band" and not armed and band_holds(b, dfn):
                    armed = True
                if dfn.item == "Focus Sash" and dfn.hp == dfn.maxhp:
                    armed = True
        if dmg >= dfn.hp and (enduring or on_sturdy or armed):
            dmg = dfn.hp - 1
            if on_sturdy:
                reveal(dfn)
            elif not enduring:
                held = True
        dealt = min(dmg, dfn.hp)
        dfn.hp -= dealt
        b.hit_left = dfn.hp
        total += dealt
        if crits[i]:
            anger_point(dfn)             # the hit's first answer (MULTI_HIT_CRITICAL)
        dfn.hit_this_turn = (mv.cat, dealt)
        if dfn.bide:
            bide_store(dfn, dealt)       # a Bide user stores what it took
        if dealt <= 0:
            continue
        berry = resist_berry(b, dfn, mv)
        if berry_works(b, dfn, berry):
            consume(dfn)
        if added and not sub_hit and dfn.alive() and not stripped and (dfn.ability != "Shield Dust" or mold(att, dfn)):
            p = min(100, (mv.chance or 0) * (2 if att.ability == "Serene Grace" else 1)) / 100
            if added == "psn" and chance("status", p, dfn):
                give_status_by_move(b, att, dfn, mv, "psn")
            elif added == "flinch" and first and chance("flinch", p, dfn):
                dfn.flinch = True
        if dfn.raging and dfn.alive():
            change_stages(dfn, {"atk": 1})
        if not sub_hit:
            contact_ability(b, att, dfn, mv, dealt, chance, pick)
            if first and flinch_item(att) and not dfn.flinch and dfn.alive() \
                    and not item_flinch_blocked(att, dfn) and chance("kingsrock", 0.1, dfn):
                dfn.flinch = True
        berry_check(dfn, b)
        if dfn.status == "frz" and mv.type == "Fire":
            dfn.status = None
    if held and dfn.item == "Focus Sash":
        consume(dfn)
    return total


def anger_point(mon):
    """Anger Point (subscript_critical_hit, run as the critical hit's message
    is, the hit's first answer): a critical hit on a standing holder, one
    its Substitute took included, sets its Attack at +6 directly, so
    Contrary and Simple play no part, unless it is there already. Until
    2026-10-20 it did nothing (Ian approved the fix)."""
    if mon.ability == "Anger Point" and mon.alive() and mon.stages["atk"] < 6:
        mon.stages["atk"] = 6
        mon.stat_raised = True
        reveal(mon)


def rollout_mult(att, mv):
    """Rollout and Ice Ball double each hit in a row, five at most, and
    twice again after Defense Curl."""
    if mv.effect != ROLLOUT:
        return 1
    # The hit's place in the run, taken before rollout_after moved the count
    # on: the first hit is 1x, then 2x, 4x...; Defense Curl doubles each.
    # BtlCmd_CalcRolloutPower sets the power, so Technician is judged on it.
    times = 2 ** getattr(att, "rollout_hit", 0) * (2 if getattr(att, "curled", False) else 1)
    return power_ratio(att, mv.power, mv.power * times) if mv.power > 1 else times


def rollout_after(att, mv, hit):
    """The lock after a use: the next hit in a row, or the run broken by a
    miss or its fifth hit. BtlCmd_CalcRolloutPower locks the user in for
    five uses, counting each use down itself, so the lock (move, uses left)
    is never counted down at a turn's end (rollout_lock_ticks)."""
    if mv.effect != ROLLOUT:
        return
    att.rollout_hit = getattr(att, "rollout", 0) if hit else 0
    att.rollout = getattr(att, "rollout", 0) + 1 if hit else 0
    if not hit or att.rollout >= 5:
        att.rollout = 0
        att.lock = None
    else:
        att.lock = (mv, 5 - att.rollout)


def rollout_break(att, mv=None):
    """A run of Rollout or Ice Ball broken before it hit (mv the move tried,
    or None for a turn its user could not act on): every subscript that
    stops a move unlocks its user (Battler_UnlockMoveChoice, which sets
    rolloutCount to 0), whether the move missed, met Protect, an immunity or
    a target out of reach or gone (subscript_missed, subscript_no_target),
    or the user was asleep, frozen, flinched, paralysed, hurt by its
    confusion, in love, loafing, recharging or held by Disable or Imprison.
    So the next Rollout starts again at its listed power. Until 2026-10-15
    such a turn left the run going (Ian approved the fix)."""
    if mv is not None and mv.effect != ROLLOUT:
        return
    if getattr(att, "rollout", 0) or (att.lock is not None and att.lock[0].effect == ROLLOUT):
        att.rollout = 0
        att.lock = None


def rollout_lock_ticks(mon):
    """Whether a turn's end counts this Pokemon's move lock down: never a
    Rollout's, whose uses count themselves (rollout_after). Until 2026-10-15
    the turn's end took one off it too, so the lock ran out after the
    fourth hit and left the count standing, and a later Rollout opened at
    sixteen times its power (Ian approved the fix)."""
    return mon.lock is not None and mon.lock[0].effect != ROLLOUT


# Magnitude's powers and their chances in percent (Generation 4, Magnitude 4
# to 10). The decomp names its effect BATTLE_EFFECT_PSYWAVE, as pret's vanilla
# data does; Psywave itself is RANDOM_DAMAGE_1_TO_150_LEVEL.
MAGNITUDE_POWERS = {10: 5, 30: 10, 50: 20, 70: 30, 90: 20, 110: 10, 150: 5}
# Present's outcomes by BtlCmd_Present's roll of 256 (the random number's
# low byte against 255 times 40, 70 and 80 over 100): 40 power below 102,
# 80 below 178, 120 below 204, and from 204 on the gift (0 here), a quarter
# of the target's maximum HP back.
PRESENT_ODDS = {40: 102, 80: 76, 120: 26, 0: 52}
# Spit Up's power by the stockpiles it spends (effect script 161: 100 each).
SPIT_UP_POWERS = (100, 200, 300)


@functools.lru_cache(maxsize=None)
def _base_friendship():
    """{compact species name: base friendship}, from each species' own
    record under res/pokemon (its folder's name, letters and digits only)."""
    out = {}
    root = os.path.join(data.ROOT, "res", "pokemon")
    for folder in os.listdir(root):
        path = os.path.join(root, folder, "data.json")
        if os.path.isfile(path):
            with open(path, encoding="utf-8") as fh:
                out[re.sub(r"[^a-z0-9]", "", folder.lower())] = json.load(fh).get("base_friendship")
    return out


def weight_power(blob, att, dfn):
    """Heavy Slam's and Heat Crash's power from the two Pokemon's records
    (BtlCmd_CalcHeavySlamPower): the target's weight over the user's, each
    in tenths of a kilogram through Battler_Weight (Heavy Metal doubles a
    weight, Light Metal halves it, the target's read past by a Mold Breaker,
    and never below 0.1 kg), 120 power at a fifth or less, 100 at a
    quarter, 80 at a third, 60 at a half, else 40."""
    def weight(rec, own):
        poks = blob["poks"].get(rec.get("species")) or {}
        w = int(round((poks.get("weightkg") or 0) * 10))
        ab = rec.get("ability")
        if own or att.get("ability") != "Mold Breaker":
            if ab == "Heavy Metal":
                w *= 2
            elif ab == "Light Metal":
                w //= 2
        return max(1, w)
    ratio = weight(dfn, False) * 10000 // weight(att, True)
    return 120 if ratio <= 2000 else 100 if ratio <= 2500 else 80 if ratio <= 3334 else 60 if ratio <= 5000 else 40


METALS = ("Heavy Metal", "Light Metal")
# The moves whose rows read the target's weight from its job: Low Kick and
# Grass Knot (BtlCmd_CalcWeightBasedPower) and Heavy Slam (the calculator
# works its power out; Heat Crash has power rows of its own, weight_power).
WEIGHT_MOVES = frozenset({"Low Kick", "Grass Knot", "Heavy Slam"})


def metal_weight(blob, rec):
    """The calculator's job for a Heavy Metal or Light Metal holder, its own
    or a twin's (Battler_Weight): its species record, its own where it has
    one (a twin's types and stats), at twice its weight or half of it, in
    whole tenths of a kilogram and never below 0.1 kg, so the rows' Low
    Kick, Grass Knot and Heavy Slam read the weight the engine does, on
    either side of the move. A Mold Breaker attacker gets past a target's
    in the engine, which the rows do not follow. Until 2026-10-20 both
    abilities did nothing in the rows (Ian approved the fix)."""
    poks = blob["poks"].get(rec.get("species")) or {}
    own = dict(rec.get("species_data") or {})
    if not own:
        if not poks.get("bs"):
            return rec
        own = {"bs": dict(poks["bs"]), "types": [t for t in poks.get("types") or [] if t]}
    kg = own.get("weightkg", poks.get("weightkg"))
    if kg is None:
        return rec
    w = int(round(kg * 10))
    w = w * 2 if rec.get("ability") == "Heavy Metal" else w // 2
    own["weightkg"] = max(1, w) / 10
    return dict(rec, species_data=own)


def metal_raw_key(b, att, dfn, mv, ak):
    """The twin of a Heavy Metal or Light Metal target at its own weight
    ("<key>#mw", prepare's metal_raw) for a Mold Breaker attacker's Low
    Kick, Grass Knot or Heavy Slam, which reads past the target's ability
    (Battler_Weight); None where there is no such row. Battle.row asks only
    for a Mold Breaker attacker and a target with one of the two."""
    t = (b.st.get("metal_raw") or {}).get(dfn.key) if mv is not None and mv.name in WEIGHT_MOVES else None
    if t is None:
        return None
    rows = b.st["rows"]
    return t if (b.weather, ak, t) in rows or (None, ak, t) in rows else None


def power_row_keys(name, knows, takes):
    """The keys whose rows need a move's power rows (Magnitude's, Present's
    or Heat Crash's, made per power since each power is set as the move
    runs): those that know the move (knows, each key's moves) and those
    that can borrow it (takes, each borrower's moves it may take: prepare's
    all_hits for a Pokemon with Copycat, Me First, Mimic, Mirror Move or
    Sketch), in knows' order."""
    return [k for k in knows if name in knows[k] or name in takes.get(k, ())]


# A trainer's power keys, each rowed with its one move at one power
# (prepare): Magnitude's "<key>#m<power>", Present's "#pr", Heat Crash's
# "#hc" and Spit Up's "#su".
POWER_KEY = re.compile(r"#(m|pr|hc|su)\d+$")
POWER_MOVES = {"m": "Magnitude", "pr": "Present", "hc": "Heat Crash", "su": "Spit Up"}


def carried_moves(key, all_hits):
    """The damaging moves the rows of a trainer's key carry, for a new
    twin rowed against it: a power key's one move, else its Pokemon's
    (all_hits of the key it twins: its party's, and what it can borrow)."""
    m = POWER_KEY.search(key)
    return [POWER_MOVES[m.group(1)]] if m else all_hits(key.split("#")[0])


def friendship_power(species):
    """Return's power for a trainer's Pokemon (effect script 121: friendship
    times 10 over 25). TrainerData_BuildParty never sets friendship, so a
    trainer's Pokemon has its species' base friendship (Pokemon_InitWith):
    70 for most, so 28 power; a power of 0 (Buneary's 0) falls back to the
    move's listed 1 (BattleSystem_CalcMoveDamage takes the listed power for
    an input of 0). The trainer's AI reckons it the same way
    (TrainerAI_CalcDamage's MOVE_RETURN case). Until 2026-10-15 every row
    gave Return the calculator's full-friendship 102 (Ian approved the
    fix)."""
    table = _base_friendship()
    name = re.sub(r"[^a-z0-9]", "", (species or "").lower())
    base = table.get(name)
    if base is None:
        base = table.get(re.sub(r"[^a-z0-9]", "", (species or "").split("-")[0].lower()), 70)
    return max(1, (base or 0) * 10 // 25)


def frustration_power(species):
    """Frustration's power for a trainer's Pokemon (effect script 123: 255
    less friendship, times 10 over 25), at its species' base friendship as
    for Return (friendship_power): 74 for most, 102 for Buneary's 0, 46 for
    Lopunny's 140; a power of 0 falls back to the listed 1. The trainer's
    AI reckons it the same way (TrainerAI_CalcDamage's MOVE_FRUSTRATION
    case). Until 2026-10-15 every row gave Frustration the calculator's
    zero-friendship 102 (Ian approved the fix)."""
    table = _base_friendship()
    name = re.sub(r"[^a-z0-9]", "", (species or "").lower())
    base = table.get(name)
    if base is None:
        base = table.get(re.sub(r"[^a-z0-9]", "", (species or "").split("-")[0].lower()), 70)
    return max(1, (255 - (base or 0)) * 10 // 25)


@functools.lru_cache(maxsize=None)
def _forbidden_moves():
    """The engine's sCannotMetronomeMoves (battle_lib.c), split at its
    FORBIDDEN_BY_MIMIC_DELIM: (the moves Mimic may not copy, the moves
    Metronome and Copycat may not call), as MOVE_ constants."""
    with open(os.path.join(data.ROOT, "src", "battle", "battle_lib.c"), encoding="utf-8") as fh:
        body = re.search(r"sCannotMetronomeMoves\[\] = \{(.*?)\};", fh.read(), re.S).group(1)
    head, _sep, tail = body.partition("FORBIDDEN_BY_MIMIC_DELIM")
    mimic = frozenset(re.findall(r"\b(MOVE_\w+)", head))
    return mimic, mimic | frozenset(re.findall(r"\b(MOVE_\w+)", tail))


# The status moves that use another move as their own, run in place of
# the move chosen (called_move): Mirror Move, Copycat and Assist.
CALLERS = frozenset({"COPY_MOVE", "USE_LAST_USED_MOVE", "USE_RANDOM_ALLY_MOVE"})
# Move_IsInvoker: the moves that call another, which Copycat will not copy.
INVOKERS = frozenset({"MOVE_SLEEP_TALK", "MOVE_COPYCAT", "MOVE_ASSIST", "MOVE_ME_FIRST", "MOVE_MIRROR_MOVE",
                      "MOVE_METRONOME"})


def note_move(b, mv):
    """The battle's last move used (movePrev, set when the attack message
    shows and cleared when it does not), for Copycat: it is set to mv, and
    the move it held before is given back for this move's Copycat (None in
    a fight with no Copycat user, which keeps no record)."""
    if not b.st.get("copycat"):
        return None
    prev, b.last_move = b.last_move, mv
    return prev


def metronome_callable(b, att, mv):
    """Move_CanBeMetronomed, which Copycat and Metronome both ask: not a
    move Gravity bars for the user, not one Heal Block bars, and not one of
    the engine's sCannotMetronomeMoves."""
    return (not (getattr(b, "gravity", 0) and mv.const in fightai.GRAVITY_FAILS)
            and not move_heal_blocked(att, mv) and mv.const not in _forbidden_moves()[1])


def called_move(b, att, mv, prev=None, pick=None):
    """The move a calling move uses in its place, or None when it fails.
    Mirror Move (effect script 9, BtlCmd_SetMirrorMove): the last move with
    MOVE_FLAG_CAN_MIRROR_MOVE aimed at its user since it, or a foe, came in
    (moveCopied), unless that move's effect is one Encore may not hold
    (Move_CanBeEncored, NO_ENCORE). Copycat (effect script 242,
    BtlCmd_TryCopycat): the last move any Pokemon used before it (prev, the
    battle's movePrev), unless there is none, it calls another move
    (Move_IsInvoker) or Metronome could not call it (metronome_callable).
    The called move runs as the user's own, spending no PP of its own, on
    the foe in front (BattleSystem_Defender); the user's last move stays the
    calling move (movePrevByBattler is moveTemp). Until 2026-10-15 both did
    nothing (Ian approved the fix).

    Assist (effect script 180, BtlCmd_TryAssist): one of the moves its
    user's party members know, every member but the user, a fainted one
    too, picked at random among all of them, a move two members know
    counting twice (pick(kind, n), the battle's dice), never one that calls
    another (Move_IsInvoker) or one Metronome could not call
    (metronome_callable); with none it fails. Until 2026-10-15 it did
    nothing (Ian approved the fix)."""
    if mv.effect == "USE_RANDOM_ALLY_MOVE":
        side = b.p if att.side == "p" else b.b
        pool = [m for mate in side.mons if mate is not att for m in mate.moves
                if m.const not in INVOKERS and metronome_callable(b, att, m)]
        if not pool:
            return None
        return pool[pick("assist", len(pool))] if pick is not None and len(pool) > 1 else pool[0]
    if mv.effect == "COPY_MOVE":
        got = att.mirror
        return got if got is not None and got.effect not in NO_ENCORE else None
    if mv.effect == "USE_LAST_USED_MOVE":
        if prev is None or prev.const in INVOKERS or not metronome_callable(b, att, prev):
            return None
        return prev
    return None


def mimic(att, dfn):
    """Mimic (effect script 82, subscript_mimic, BtlCmd_TryMimic): the
    target's last move (movePrevByBattler) takes the place of the user's
    first Mimic until the user leaves, with 5 PP or the move's own if it has
    fewer. It fails with no last move, on a move Mimic may not copy (the
    engine's list up to FORBIDDEN_BY_MIMIC_DELIM), on one the user knows
    already, and through a Substitute unless an Infiltrator passes it. The
    copy is a new move list, never the old one changed, since the search's
    copies of a Pokemon share it. Until 2026-10-15 Mimic did nothing (Ian
    approved the fix)."""
    last = dfn.last
    if last is None or last.const in _forbidden_moves()[0] or sub_blocks(att, dfn):
        return
    if any(m.name == last.name for m in att.moves):
        return
    j = next((i for i, m in enumerate(att.moves) if m.effect == "COPY_MOVE_FOR_BATTLE"), None)
    if j is None:
        return
    att.mimicked, att.rare = (att.moves, att.pp.get(att.moves[j].name, 0)), True
    moves = list(att.moves)
    moves[j] = last
    att.pp = {k: v for k, v in att.pp.items() if k != att.moves[j].name}
    att.pp[last.name] = min(5, last.pp)
    att.moves = moves


# The effects Me First may not take (sCannotMeFirstMoves, compared by
# effect): Counter's, Mirror Coat's, Thief's and Covet's, Focus Punch's and
# Chatter's.
ME_FIRST_REFUSES = frozenset({"COUNTER", "MIRROR_COAT", "STEAL_HELD_ITEM", "HIT_LAST_WHIFF_IF_HIT", "CHATTER"})


def me_first_move(att, dfn, first):
    """Me First (effect script 241, BtlCmd_TryMeFirst): the move its target
    has chosen this turn (its Encore move while one holds it), used at once
    as the user's own at half again its damage (the meFirst flag, read
    after the critical hit in BattleSystem_CalcMoveDamage's caller), or
    None when it fails: the target has acted already, struggles, chose a
    move with no power, or one of the effects the engine bars
    (ME_FIRST_REFUSES). The move spends no PP of its own; prepare() rows a
    Me First user with its foes' damaging moves (BORROWS). Until
    2026-10-15 Me First did nothing (Ian approved the fix)."""
    nxt = dfn.chosen
    if dfn.encore is not None:
        nxt = next((m for m in dfn.moves if m.name == dfn.encore), nxt)
    if (not first or nxt is None or not dfn.alive() or nxt.effect == "STRUGGLE" or nxt.power <= 0
            or nxt.effect in ME_FIRST_REFUSES):
        return None
    att.me_first = att.rare = True
    return nxt


# The moves Sketch may not take (BtlCmd_TrySketch), beside none at all.
SKETCH_REFUSES = frozenset({"MOVE_STRUGGLE", "MOVE_SKETCH", "MOVE_CHATTER"})


def sketch(att, dfn, mv):
    """Sketch (effect script 95, subscript_sketch, BtlCmd_TrySketch): the
    target's last move since it came in (moveSketched, set when its attack
    message shows) takes the place of the user's first Sketch for good,
    with the move's full PP, and stays through switching (the party record
    is written, BattleController_EmitUpdatePartyMon). It fails through a
    Substitute an Infiltrator does not pass, on a transformed user, on no
    last move, Struggle, Sketch or Chatter, and on a move the user knows
    already. The copy is a new move list, never the old one changed, since
    the search's copies of a Pokemon share it; prepare() rows a Sketch user
    with its foes' damaging moves (BORROWS). Until 2026-10-15 Sketch did
    nothing (Ian approved the fix)."""
    last = dfn.last
    if (last is None or last.const in SKETCH_REFUSES or getattr(att, "transformed", False)
            or sub_blocks(att, dfn, mv)):
        return
    if any(m.name == last.name for m in att.moves if m.effect != "LEARN_MOVE_PERMANENT"):
        return
    j = next((i for i, m in enumerate(att.moves) if m.effect == "LEARN_MOVE_PERMANENT"), None)
    if j is None:
        return
    old = att.moves[j]
    moves = list(att.moves)
    moves[j] = last
    att.pp = {k: v for k, v in att.pp.items() if k != old.name}
    att.pp[last.name] = last.pp
    att.moves = moves


def present_roll(b):
    """Present's outcome for this use (effect script 122, BtlCmd_Present): a
    power of 40, 80 or 120, or 0 for the gift, at PRESENT_ODDS, on the
    battle's dice (a run's draw, the planner's weighted event); where no
    dice can weigh it, the likeliest, 40, as Magnitude takes its likeliest
    there. Its power's row is the "<key>#pr<power>" one prepare() adds."""
    outcomes, weights = list(PRESENT_ODDS), list(PRESENT_ODDS.values())
    pick = getattr(getattr(b, "dice", None), "pick_weighted", None)
    if pick is not None:
        return pick(outcomes, weights)
    rng = getattr(b, "rng", None)
    return rng.choices(outcomes, weights)[0] if rng is not None and hasattr(rng, "choices") else 40


def present_heal(dfn):
    """Present's gift (subscript_present_heal, after the accuracy check and
    past the type chart, SYSCTL_IGNORE_IMMUNITIES): the target gets back a
    quarter of its maximum HP (BattleSystem_Divide, at least 1), nothing
    under Heal Block (the subscript's message) or at full HP (subscript_recover_hp's
    NO_MORE_WORK). Until 2026-10-15 Present found no row and did nothing
    (Ian approved the fix)."""
    if dfn.alive() and not dfn.heal_block and dfn.hp < dfn.maxhp:
        heal(dfn, max(1, dfn.maxhp // 4))


def stockpile(mon):
    """Stockpile (effect script 160, subscript_stockpile): it fails at three;
    each use adds one and raises Defense and Sp. Def a stage each through the
    stat-stage subscript (so Simple doubles them), counting a stage only when
    it rose (one at +6 does not). Until 2026-10-15 there was no count: it
    raised both every time and never failed (Ian approved the fix)."""
    if mon.stockpile >= 3:
        return
    mon.stockpile += 1
    if mon.stages["def"] < 6:
        change_stages(mon, {"def": 1})
        mon.stockpile_def += 1
    if mon.stages["spd"] < 6:
        change_stages(mon, {"spd": 1})
        mon.stockpile_spd += 1


def spend_stockpile(mon):
    """Spit Up and Swallow (effect scripts 161 and 162) spend every
    stockpile at once, before their hit or heal is tried, and take back one
    stage of Defense and of Sp. Def for each that Stockpile raised, no lower
    than -6 (OPCODE_SUB_TO_ZERO on the stored stage). The count spent."""
    n = mon.stockpile
    mon.stages["def"] = max(-6, mon.stages["def"] - mon.stockpile_def)
    mon.stages["spd"] = max(-6, mon.stages["spd"] - mon.stockpile_spd)
    mon.stockpile = mon.stockpile_def = mon.stockpile_spd = 0
    return n


def swallow(att):
    """Swallow (effect script 162): with no stockpile it fails; otherwise
    it spends them all (spend_stockpile) and restores a quarter of its
    user's maximum HP for one, half for two and all of it for three
    (BattleSystem_Divide by 1 << (3 - count)). Until 2026-10-15 it restored
    a quarter whatever was stored, and spent nothing (Ian approved the
    fix)."""
    if att.stockpile:
        heal(att, engine_divide(att.maxhp, 1 << (3 - spend_stockpile(att))))


def natural_gift_key(key, berry):
    """The row the player's Natural Gift is read from: its twin holding the
    Berry it spends ("<key>#ng", which prepare adds for the Sitrus Berry, the
    one Berry the player is handed), since the player's own rows are made
    with no item and the calculator types and powers Natural Gift by the
    Berry (CalcNaturalGiftParams: a Sitrus Berry's is Psychic at 60). Any
    other Berry has no twin, and its Natural Gift no row. Until 2026-10-15
    the player's Natural Gift never dealt damage (Ian approved the fix)."""
    return f"{key}#ng" if berry == "Sitrus Berry" else key


def spit_up_key(att):
    """Spit Up with no stockpile fails before anything else ("failed to spit
    up a thing"); otherwise it spends them (spend_stockpile) and hits at 100
    power for each, from the calculator's row for that power ("<key>#su<power>",
    which prepare adds), at its top roll (CalcMaxDamage has no variance).
    None when it fails. Until 2026-10-15 it hit at its listed power of 1."""
    if not att.stockpile:
        return None
    return f"{att.key}#su{100 * spend_stockpile(att)}"

# The moves whose effect script sets the damage itself (res/battle/scripts/
# effects): stat stages, screens, burn, items and critical hits never touch
# the figure, but the type chart still runs, so an immune target takes
# nothing (ApplyTypeMultiplier flags MOVE_STATUS_INEFFECTIVE even with
# SYSCTL_IGNORE_TYPE_CHECKS set): Seismic Toss misses a Ghost, Night Shade a
# Normal type, Dragon Rage a Fairy.
FIXED_DAMAGE = {"40_DAMAGE_FLAT", "20_DAMAGE_FLAT", "LEVEL_DAMAGE_FLAT", "RANDOM_DAMAGE_1_TO_150_LEVEL",
                "HALVE_HP", "QUARTER_HP", "SET_HP_EQUAL_TO_USER", "FINAL_GAMBIT"}


def bide_ends(att):
    """A Bide ends (Battler_UnlockMoveChoice clears VOLATILE_CONDITION_BIDE
    with the lock), its stored HP gone."""
    att.bide = att.bide_damage = 0
    if att.lock is not None and att.lock[0].effect == "BIDE":
        att.lock = None


def bide_releases(att, mv):
    """Bide (effect script 26, subscript_bide_start, the status check's
    CHECK_STATUS_STATE_BIDE and subscript_bide_end): its first use locks its
    user in for two more turns (a lock its turn's end counts down, so no
    PP is paid then) and starts storing from 0; the second stores on; the
    third, once the storing has run out, gives back twice the HP the moves
    aimed at it took meanwhile (bide_store), as fixed damage past the type
    chart (its range is its user's, so BattleControllerPlayer_CheckTypeChart
    leaves it alone), at its foe; with nothing stored it fails. A turn its
    user cannot act ends it (could_not_act), as the subscripts that stop a
    move unlock it; a sleeping user's Bide, which the engine holds until it
    wakes, ends too. Whether this use hits, the damage in att.bide_release.
    Until 2026-10-15 Bide did nothing (Ian approved the fix)."""
    if not att.bide:
        att.bide, att.bide_damage, att.rare = 2, 0, True
        att.lock = (mv, 3)
        return False
    att.bide -= 1
    if att.bide:
        return False                 # storing energy
    stored = att.bide_damage
    bide_ends(att)
    att.bide_release = 2 * stored
    return stored > 0


def bide_store(dfn, dealt):
    """A move's hit on a Bide user adds the HP it took to the store
    (storedDamage, in BattleControllerPlayer_UpdateHP); a Substitute's hit
    adds nothing."""
    if dfn.bide:
        dfn.bide_damage += dealt


def fixed_damage(b, att, dfn, mv, tenths=10):
    """A fixed-damage move's damage, 0 when it fails or the target's type is
    immune, or None for any other move. tenths is Psywave's roll, 5 to 15
    (`Random 10, 5`, then level times the roll over ten, at least 1)."""
    if mv.effect == "BIDE":
        return att.bide_release      # twice what it stored, past the type chart (bide_releases)
    if mv.effect not in FIXED_DAMAGE:
        return None
    if effectiveness(b.st["chart"], mv.type, chart_types(dfn, mv)) == 0:
        return 0                 # Seismic Toss hits an identified Ghost (chart_types)
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


def slot_of(side, mon):
    """The slot mon stands in on its side: 0, or 1 in a double battle."""
    return 1 if side.active2 is not None and side.mons[side.active2] is mon else 0


def foresee(b, att, mv, dfn, dmg):
    """Future Sight and Doom Desire as they are used (effect script 148,
    BtlCmd_TryFutureSight). The damage is worked out now, the roll made now,
    with no type chart and no critical hit (BattleSystem_CalcMoveDamage, as
    the calculator's rows for these two moves already have it), and kept on
    the target's slot for the turn's end at which the count, three now, has
    run down to 0 (future_sight_ends). The move fails while one waits on that
    slot. Whether it was set."""
    side = b.p if dfn.side == "p" else b.b
    slot = slot_of(side, dfn)
    if side.future[slot] is not None:
        return False
    own = b.p if att.side == "p" else b.b
    pending = list(side.future)
    pending[slot] = (3, dmg, mv.name, att.side, slot_of(own, att))
    side.future, side.future_sight = tuple(pending), True
    return True


# The accuracy check a Future Sight makes as it lands, when the battle plays
# with dice: perfectline's, which it sets here (fightsim cannot import it).
DICE_ACCURACY = None


def future_sight_ends(b, order):
    """The first step of the turn's side conditions
    (SIDE_COND_CHECK_STATE_FUTURE_SIGHT), over the battlers in end order:
    each Future Sight waiting on a slot counts down, and on reaching 0 lands
    on whoever then stands there, if it has HP; the side's condition clears
    only as one lands. The hit checks accuracy for the Pokemon now in its
    user's slot, misses a target in the air or underground, goes to a
    Substitute, and is held by Sturdy or a Focus Sash at full HP or by a
    Focus Band (subscript_future_sight_damage's CheckHoldOnWith1HP); no type
    chart, no Endure; Rage rises. False once the battle is over."""
    visits = []
    for m in order:
        side = b.p if m.side == "p" else b.b
        visits.append((side, slot_of(side, m), m))
    for side in (b.p, b.b):
        for slot in (0, 1):
            if side.future[slot] is not None and not any(s is side and k == slot for s, k, _m in visits):
                visits.append((side, slot, None))          # an empty slot in a double battle
    for side, slot, m in visits:
        pending = side.future[slot]
        if pending is None:
            continue
        turns, dmg, name, user_side, user_slot = pending
        future = list(side.future)
        future[slot] = (turns - 1,) + pending[1:] if turns > 1 else None
        side.future = tuple(future)
        if turns > 1 or m is None or not m.alive():
            continue
        side.future_sight = False
        users = b.p if user_side == "p" else b.b
        user = users.mons[users.active] if user_slot == 0 else (
            users.mons[users.active2] if users.active2 is not None else None)
        mv = move(name)
        if m.charging is not None and m.charging.effect in INVULNERABLE:
            continue
        if user is not None:
            dice = getattr(b, "dice", None)
            if not (DICE_ACCURACY(b, user, m, mv) if dice is not None and DICE_ACCURACY else
                    b.accuracy_hits(user, m, mv)):
                continue
        if m.sub:
            m.sub = max(0, m.sub - dmg)
            continue
        if m.hp == m.maxhp and m.ability == "Sturdy":
            if dmg >= m.hp:
                reveal(m)
                dmg = m.hp - 1
        elif dmg >= m.hp and m.item == "Focus Sash" and m.hp == m.maxhp:
            dmg = m.hp - 1
            consume(m)
        elif dmg >= m.hp and m.item == "Focus Band" and band_holds(b, m):
            dmg = m.hp - 1
        hurt(b, m, dmg)
        if getattr(m, "raging", False) and m.alive():
            change_stages(m, {"atk": 1})
        if battle_over(b):
            return False
    return True


def band_holds(b, mon):
    """A Focus Band's one in ten, through the battle's dice when it has them
    (bad luck for the player when the trainer's band holds)."""
    dice = getattr(b, "dice", None)
    if dice is None:
        return b.rng.random() < 0.1
    return dice.bad("focusband", 0.1) if mon.side == "b" else dice.good(0.1, "focusband")


def ohko_blocked(b, att, dfn, mv):
    """A one-hit KO move fails on a type it cannot hit, a higher-level
    target, or Sturdy unless the user has Mold Breaker (BtlCmd_TryOHKOMove)."""
    return (effectiveness(b.st["chart"], mv.type, dfn.types) == 0 or att.level < dfn.level
            or (dfn.ability == "Sturdy" and att.ability != "Mold Breaker"))


def engine_divide(value, divisor):
    """BattleSystem_Divide on a whole number of HP: the quotient rounded
    down, but never 0 from a value that is not 0."""
    return 0 if value == 0 else max(1, value // divisor)


def life_dew(att, b=None):
    """Life Dew (effect script 383, subscript_life_dew): it fails under Heal
    Block, which the script checks itself (the move is not on
    sMovesAffectedByHealBlock, so it can be chosen); otherwise its user gets
    back a quarter of its maximum HP, rounded up, unless its HP is full, and
    in a double battle so does its standing ally, the ally's own Heal Block
    unread. Until 2026-10-15 it did nothing (Ian approved the fix); until
    2026-10-21 the ally got nothing (Ian approved the double-battle part
    batch 7 left on 2026-10-14)."""
    if heal_blocked(att):
        return
    heal(att, (att.maxhp + 3) // 4)
    ally = ally_of(b, att) if b is not None and b.doubles else None
    if ally is not None:
        heal(ally, (ally.maxhp + 3) // 4)


def coaching(b, att, dfn):
    """Coaching (effect script 381, subscript_coaching): its target is the
    user's ally (RANGE_ALLY), whose Attack and Defense rise a stage each
    through the stat-stage subscript (change_stages: Simple and Contrary
    count); with no ally the target is the user and the move fails, as it
    does on a fainted ally. So it does nothing in a single battle. Until
    2026-10-21 it did nothing in a double battle either (Ian approved the
    double-battle part batch 8 left on 2026-10-14)."""
    if not b.doubles or dfn is att or dfn.side != att.side or not dfn.alive():
        return
    change_stages(dfn, {"atk": 1, "def": 1})


def strength_sap(b, att, dfn, mv):
    """Strength Sap (effect script 378, subscript_strength_sap): it fails on
    a target whose Attack is at -6; otherwise the heal is the target's
    Attack stat at its stage, taken before the drop (BtlCmd_CalcStrengthSap,
    Battler_AttackAfterStage, in whole numbers; a Power Trick holder's
    Attack is its Defense), then the target's Attack falls a stage, which a
    Substitute, Mist and the blocking abilities stop without stopping the
    heal; a Big Root adds 30 per cent, and into Liquid Ooze the heal is
    damage instead, which Magic Guard turns away. Heal Block does not stop
    it (subscript_recover_hp has no check, and the move is not on
    sMovesAffectedByHealBlock). Until 2026-10-15 it did nothing (Ian
    approved the fix)."""
    stage = dfn.stages["atk"]
    if stage <= -6:
        return
    attack = raw_stat(dfn, "def" if dfn.power_trick else "atk")
    gain = attack * (2 + stage) // 2 if stage >= 0 else attack * 2 // (2 - stage)
    if not sub_blocks(att, dfn, mv):
        lower_stats(b, att, dfn, {"atk": -1})
    if att.item == "Big Root":
        gain = gain * 130 // 100
    if dfn.ability == "Liquid Ooze":
        reveal(dfn)
        if att.ability != "Magic Guard":
            hurt(b, att, gain)
    else:
        heal(att, gain)


def weather_heal(b, att, mv):
    """The HP Moonlight, Morning Sun, Synthesis and Shore Up restore
    (effect script 132, BtlCmd_WeatherHPRecovery): half with no weather, or
    with Cloud Nine or Air Lock on the field; two thirds in sun and a quarter
    in any other weather. Shore Up instead restores two thirds in a
    sandstorm and half otherwise. Until 2026-10-15 Cloud Nine and Air Lock
    were ignored and Shore Up took the sun rule (Ian approved the fix)."""
    weather = None if weather_ignored(b) else b.weather
    if mv.const == "MOVE_SHORE_UP":
        return engine_divide(att.maxhp * 20, 30) if weather == "Sand" else att.maxhp // 2
    if weather is None:
        return att.maxhp // 2
    if weather == "Sun":
        return engine_divide(att.maxhp * 20, 30)
    return engine_divide(att.maxhp, 4)


def hurt(b, mon, amount):
    """HP lost to anything but a move's hit."""
    if amount <= 0 or not mon.alive():
        return
    mon.hp = max(0, mon.hp - amount)
    # Assurance's mask (subscript_update_hp): set by HP lost while the turn
    # runs, and cleared with the turn flags only after a knockout's
    # replacement has come in, so hazards on that replacement do not count.
    if getattr(b, "mid_turn", False):
        mon.hurt_this_turn = True
    berry_check(mon, b)
    if not mon.hp and mon.ability == "Neutralizing Gas" and b.st.get("gas"):
        gas_update(b, check=False)       # the gas goes with its holder's last HP


# A pinch berry raises a stat by one stage once its holder is at a quarter of
# its HP or less; Sitrus heals a quarter and Oran 10 once at half or less. In
# Generation 4 each fires as soon as the HP drops, not at the end of the turn.
PINCH_BERRIES = {"Apicot Berry": "spd", "Liechi Berry": "atk", "Ganlon Berry": "def",
                 "Salac Berry": "spe", "Petaya Berry": "spa"}


def unnerved(b, mon):
    """Whether mon cannot eat the Berry it holds (BerryBlockedByUnnerve): a
    foe with Unnerve stands on the field. That stops every Berry the engine
    eats from its holder's hand, the pinch and healing ones, the cure ones,
    a resist Berry's halving and the Custap Berry; Natural Gift, Bug Bite,
    Pluck and Harvest are not eating. b None (a check made with no battle)
    has no foe. Until 2026-10-14 Unnerve did nothing (Ian approved the
    fix)."""
    if b is None or not mon.item or not mon.item.endswith("Berry"):
        return False
    foes = (b.b if mon.side == "p" else b.p).on_field()
    return any(f.alive() and f.ability == "Unnerve" for f in foes)


def berry_works(b, mon, berry):
    """Whether mon still holds this resist Berry and may eat it."""
    return bool(berry) and mon.item == berry and not unnerved(b, mon)


def berry_check(mon, b=None):
    # An item none of the branches below eats leaves nothing to do, so
    # Unnerve, which needs a look at the foes, is looked for only after.
    if not mon.alive() or not mon.item or mon.item not in BERRY_CHECK_ITEMS or unnerved(b, mon):
        return
    # Gluttony eats a pinch berry at half its HP, not a quarter.
    if mon.item in PINCH_BERRIES and mon.hp * (2 if mon.ability == "Gluttony" else 4) <= mon.maxhp:
        change_stages(mon, {PINCH_BERRIES[mon.item]: 1})
        consume(mon)
    elif mon.item == "Starf Berry" and mon.hp * (2 if mon.ability == "Gluttony" else 4) <= mon.maxhp:
        # HOLD_EFFECT_PINCH_RANDOM_UP: at a quarter of its HP (half with
        # Gluttony) one of the five stats other than accuracy and evasion
        # that can still rise, drawn at random, rises two stages through the
        # stat-stage subscript (so Simple doubles it); with none that can,
        # the Berry stays uneaten. Until 2026-10-14 it did nothing (Ian
        # approved the fix).
        room = [s for s in ("atk", "def", "spa", "spd", "spe") if item_can_raise(mon, s)]
        if room:
            dice = getattr(b, "dice", None) if b is not None else None
            pick = (dice.choice("starf", len(room)) if dice is not None
                    else b.rng.randrange(len(room)) if b is not None and getattr(b, "rng", None) is not None else 0)
            change_stages(mon, {room[pick]: 2})
            consume(mon)
    elif mon.item == "Sitrus Berry" and mon.hp * 2 <= mon.maxhp:
        heal(mon, mon.maxhp // 4)
        consume(mon)
    elif mon.item in ("Oran Berry", "Berry Juice") and mon.hp * 2 <= mon.maxhp:
        heal(mon, 10 if mon.item == "Oran Berry" else 20)
        consume(mon)


# The items berry_check eats, each in one of its branches.
BERRY_CHECK_ITEMS = frozenset(PINCH_BERRIES) | {"Starf Berry", "Sitrus Berry", "Oran Berry", "Berry Juice"}


def item_can_raise(mon, stat):
    """Whether an item's raise would change mon's stat (Battler_ItemCanRaiseStat):
    one below +6, or for a Contrary holder, which the raise lowers
    (change_stages), one above -6."""
    return mon.stages[stat] > -6 if mon.ability == "Contrary" else mon.stages[stat] < 6


def binding_band(b, mon):
    """Whether the Pokemon that bound mon stands on the field holding a
    Binding Band (HOLD_EFFECT_BINDING_BAND, read at each turn's end)."""
    foes = (b.b if mon.side == "p" else b.p).on_field()
    return any(f.key == getattr(mon, "bound_by", None) and f.item == "Binding Band" for f in foes)


def untrappable(mon):
    """Whether nothing can trap mon (Battler_IsTrapped returns at once): it
    holds a Shed Shell (HOLD_EFFECT_SWITCH), or it is a Ghost type, by
    Oxide's Generation 6 rule, which frees it from a bind, Block, Mean Look
    and its own Ingrain as well as the trapping abilities. Both came in on
    2026-10-14, the Ghost type's freedom from the moves after the gaps list
    (Ian approved the fixes)."""
    return mon.item == "Shed Shell" or "Ghost" in mon.types


def can_switch(mon):
    """False while Block, Mean Look or its own Ingrain holds it in, unless
    nothing can trap it (untrappable)."""
    if untrappable(mon):
        return True
    return mon.trapped_by is None and not mon.ingrained


def trapped(b, mon):
    """Whether mon cannot switch out (Battler_IsTrapped, the party menu's
    test): held in the air by Sky Drop, whatever its type or item
    (sky_held); a bind, Block, Mean Look or its own Ingrain (can_switch), or
    a foe's trapping ability (ability_trapped); never a Shed Shell holder or
    a Ghost type (untrappable)."""
    if mon.sky_holder is not None and sky_held(b, mon):
        return True
    if untrappable(mon):
        return False
    return bool(mon.bound) or not can_switch(mon) or ability_trapped(b, mon)


def sky_held(b, mon):
    """Whether a Sky Drop holds mon in the air (Battler_SkyDropHeld): while
    it and its holder both stand and the holder is still on the field,
    charging its Sky Drop; once any of that has stopped the hold ends here."""
    if mon.alive():
        foes = b.b if mon.side == "p" else b.p
        for f in foes.on_field():
            if f.key == mon.sky_holder and f.alive() and f.charging is not None and f.charging.effect == "SKY_DROP":
                return True
    mon.sky_holder = None
    return False


def sky_drop(b, att, mv, dfn):
    """Sky Drop (effect script 414, TrySkyDrop, Generation 6's rule in
    Oxide's engine), in a single battle; True when its hit is to land now.
    The first turn lifts the target with its user, failing on a target
    fainted, out of reach, protecting, behind a Substitute, already held or
    of 200 kg or more, under Gravity, or for a user Smack Down has brought
    down; the PP is paid then, as a charging move's is. While held the
    target does nothing and cannot switch (sky_held), and if the user stops
    before its drop, by fainting or a turn it cannot act, the target lands.
    The second turn drops the target: the move fails on one no longer held,
    does nothing to a Flying type, and otherwise hits. Until 2026-10-15 it
    hit on the turn it was used, nobody was held, and Flying types took it
    (Ian approved the fix). In a double battle it fails on an ally too
    (TrySkyDrop), and while the hold lasts the user and the target are in
    the air for every other Pokemon (sky_airborne), and the user's drop
    goes to the Pokemon it holds (run_doubles); until 2026-10-21 it was a
    plain hit there (Ian approved the double-battle part batch 8 left on
    2026-10-14)."""
    if att.charging is None:
        weight = (calc.blob()["poks"].get(dfn.species) or {}).get("weightkg") or 0
        if (not dfn.alive() or dfn is att or (dfn.charging is not None and dfn.charging.effect in INVULNERABLE)
                or dfn.protecting or dfn.sub or dfn.sky_holder is not None or weight >= 200
                or getattr(b, "gravity", 0) or att.smacked or dfn.side == att.side
                or (b.doubles and sky_airborne(b, dfn))):
            return False
        att.charging = mv
        dfn.sky_holder, dfn.rare = att.key, True
        return False
    att.charging = None
    if dfn.sky_holder != att.key:
        return False
    dfn.sky_holder = None
    return "Flying" not in dfn.types


def sky_airborne(b, mon):
    """Whether, in a double battle, mon is up in the air with a Sky Drop:
    its user charging it, or a Pokemon it holds (sky_held). TrySkyDrop and
    the lift's script give both MOVE_EFFECT_AIRBORNE, as Fly gives its user,
    so every other Pokemon's move meets them as it meets a Pokemon in the
    air (sky_out_of_reach); a single battle has no other Pokemon to aim at
    them."""
    if mon.charging is not None and mon.charging.effect == "SKY_DROP":
        return True
    return mon.sky_holder is not None and sky_held(b, mon)


def sky_out_of_reach(b, att, dfn, mv):
    """Whether att's move cannot reach dfn up in the air with a Sky Drop
    (sky_airborne), as BattleControllerPlayer_CheckMoveHitOverrides misses a
    MOVE_EFFECT_AIRBORNE target: unless the move reaches the air (HIT_IN_AIR:
    Gust, Twister, Thunder, Hurricane, Sky Uppercut, Smack Down) or No Guard
    or Lock-On lands it (lands_sure)."""
    if not sky_airborne(b, dfn):
        return False
    return not air_reach(mv) and not lands_sure(att, dfn, mv)


def air_reach(mv):
    """How a move strikes a Pokemon in the air: HIT_IN_AIR's 2 or 1, or 0;
    Thousand Arrows shares Smack Down's effect but does not reach the air
    (Oxide), as reach_mult has it."""
    return HIT_IN_AIR.get(mv.effect, 0) if mv.name != "Thousand Arrows" else 0


def heal(mon, amount):
    mon.hp = min(mon.maxhp, mon.hp + max(0, amount))


def drain(b, att, dfn, gain):
    """What a drain gives att off dfn, a draining move's hit or Leech Seed's
    sap (subscript_drain_half_damage_dealt, _three_quarters, the Dream Eater
    and Leech Seed subscripts): `gain` HP back, unless dfn has Liquid Ooze,
    which the engine checks first, before Heal Block, and which turns the
    heal into that much damage to att, unless att has Magic Guard (then the
    message names both abilities). Heal Block on att stops only the heal.
    Until 2026-10-14 Liquid Ooze did nothing (Ian approved the fix)."""
    if gain <= 0:
        return
    if dfn.ability == "Liquid Ooze":
        if att.ability == "Magic Guard":
            reveal(att)
            reveal(dfn)
        else:
            hurt(b, att, gain)
        return
    if not heal_blocked(att):
        heal(att, gain)


def forced_out(b, mon):
    """Whether mon, in a single battle's order of moves, has left the field
    before its turn came: forced out by a faster Roar or Whirlwind of the
    same priority, or a Dragon Tail or Circle Throw, it does not act (its
    party slot's action goes with it), and the Pokemon dragged in has no
    action of its own this turn. Until 2026-10-15 it used its move from
    the bench (Ian approved the fix)."""
    return mon is not (b.p if mon.side == "p" else b.b).cur()


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
        if d.mirror_user and shown and mv.mirror:
            d.mirror, d.rare = mv, True     # BattleControllerPlayer_UpdateFlagsWhenHit's moveCopied
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
    if att.charging is not None:
        # The subscript that stopped it unlocked its user
        # (Battler_UnlockMoveChoice clears MOVE_LOCKED and the hidden turn),
        # so a charge ends: a Fly or Solar Beam user that flinches or is
        # fully paralysed on its striking turn must charge again, and a
        # Sky Drop user stopped in the air lets its target go. Sleep and
        # freeze end the charge as they come (charge_ends). Until 2026-10-15
        # only Sky Drop's ended (Ian approved the fix).
        att.charging = None
    if att.bide:
        bide_ends(att)               # the subscript that stopped it unlocked its user, its Bide with it
    if b.st.get("copycat"):
        b.last_move = None           # no attack message: movePrev is MOVE_NONE
    if att.rollout or att.lock is not None:
        rollout_break(att)           # the subscript that stopped it unlocked its user (rollout_break)
    mark_hit(b, mv, dfn, False, targets)


def charge_ends(mon, status):
    """Falling asleep or being frozen unlocks a Pokemon at once
    (subscript_fall_asleep and subscript_freeze run UnlockMoveChoice; a
    sleeping Pokemon still locked is unlocked again at the turn's start),
    so a charge it was holding ends there: a Fly user put to sleep comes
    down and can be hit, and must charge again once it wakes."""
    if mon.charging is not None and status in ("slp", "frz"):
        mon.charging = None


def flinched(att):
    """A flinch stops att's move (subscript_flinched): Steadfast then raises
    its Speed a stage through the stat-stage subscript, the message naming
    the ability. Steadfast did nothing until 2026-10-14 (Ian approved the
    fix)."""
    att.flinch = False
    if att.ability == "Steadfast" and att.stages["spe"] < 6:
        change_stages(att, {"spe": 1})
        reveal(att)


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


# The ranges whose PP cost counts every Pressure holder standing on the other
# side, and those that count none (BattleControllerPlayer_DecrementPP's switch);
# any other range counts its target's own Pressure.
PRESSURE_ALL = frozenset({"ALL_ADJACENT", "FIELD", "ADJACENT_OPPONENTS", "OPPONENT_SIDE"})
PRESSURE_NONE = frozenset({"USER_SIDE", "USER", "USER_OR_ALLY", "ALLY"})
# The ranges whose defender is the user itself or no one at the PP step, so
# a single target's Pressure never counts for them.
PRESSURE_NO_TARGET = frozenset({"SINGLE_TARGET_SPECIAL", "ALL"})


def pp_cost(b, att, mv, dfn, targets=None):
    """The PP a move costs as it is used (BattleControllerPlayer_DecrementPP):
    one, and one more for each Pressure holder it meets on the other side
    (Oxide counts only the opponents', the later games' rule): every one
    standing for a move of the whole side or field and for Imprison and
    Snatch, none for a move of the user's own side, its target's own for any
    other. A Spikes or Toxic Spikes that fails at its last layer skips the
    Pressure (BtlCmd_TrySpikes and TryToxicSpikes set skipPressureCheck).
    Until 2026-10-14 every move cost one (Ian approved the fix)."""
    if mv.effect == "SET_SPIKES" or mv.effect == "TOXIC_SPIKES":
        side = b.b if att.side == "p" else b.p
        if side.hazards["spikes" if mv.effect == "SET_SPIKES" else "tspikes"] >= (3 if mv.effect == "SET_SPIKES" else 2):
            return 1
    if mv.name in ("Imprison", "Snatch") or mv.range in PRESSURE_ALL:
        # Only this case counts every standing foe, so only it lists them.
        foes = [m for m in (b.b if att.side == "p" else b.p).on_field() if m.alive()]
        return 1 + sum(m.ability == "Pressure" for m in foes)
    if mv.range in PRESSURE_NONE or mv.range in PRESSURE_NO_TARGET:
        return 1
    hit = targets if targets else [dfn]
    return 1 + sum(1 for t in hit if t is not None and t is not att and t.side != att.side
                   and t.ability == "Pressure")


def paid_already(att, mv):
    """Whether this turn's move costs no PP: a battler held in a charge or a
    Rollout cannot choose its command, and the engine marks its turn as paid
    (Battler_CanPickCommand false, so ppDecremented is set as commands are
    chosen), so the strike of a charging move and every locked Rollout or Ice
    Ball after the first cost nothing (Ian approved the fix of 2026-10-14)."""
    if att.charging is not None:
        return True
    return att.lock is not None and att.lock[0].name == mv.name


def spend_pp(b, att, mv, dfn, targets=None):
    """The PP step of a move: nothing on a turn already paid (paid_already),
    else pp_cost, never below 0 (the engine sets 0 when the cost is more
    than what is left)."""
    if paid_already(att, mv):
        return
    cost = pp_cost(b, att, mv, dfn, targets)
    left = att.pp.get(mv.name, 1)
    att.pp[mv.name] = left - 1 if cost == 1 else max(0, left - cost)


def use_move(b, att, mv, dfn, first, targets=None):
    """One move, from its user's turn check to its last effect, and then the
    switch-in check that ends every action (BattleControllerPlayer_MoveEnd),
    where a Neutralizing Gas whose holder fell during the move wears off.
    `first`: whether the target has not moved yet this turn."""
    _use_move(b, att, mv, dfn, first, targets)
    if att.me_first:
        att.me_first = False     # Me First's half again lasts the move it took
    if b.st.get("gas"):
        gas_update(b)
    move_end(b)


def move_end(b):
    """The rest of the switch-in check that ends every move
    (BattleControllerPlayer_MoveEnd), beyond Neutralizing Gas's step: a Trace
    holder still waiting for a foe it can copy traces now (trace), and its
    new ability's entry steps follow; then Castform takes the weather's form
    (forecast). A move's knockouts come first, each faint subscript's Soul
    Heart with them (soul_heart)."""
    if b.st.get("soul_heart"):
        soul_heart(b)
    # The Pokemon on the field, listed once for Trace's look and for
    # Forecast, since this runs after every move; listed again for Forecast
    # only if a Trace went off, as its entry steps follow.
    field = b.p.on_field() + b.b.on_field()
    for m in field:
        if m.ability == "Trace" and not m.traced:
            traced = trace(b)
            if traced:
                entry_abilities(b, traced, trace_now=False)
                field = None
            break
    forecast(b, field)


def fainted_others(b, mon):
    """How many Pokemon of the battle but mon are down."""
    return sum(1 for side in (b.p, b.b) for m in side.mons if m is not mon and not m.alive())


def soul_heart(b):
    """Soul Heart (BtlCmd_TrySoulHeart, run from subscript_faint_mon): each
    time another Pokemon faints, a standing holder on the field gains a
    stage of Sp. Atk through the stat-stage subscript (change_stages, so
    Simple doubles it and Contrary turns it), nothing at +6; the message
    names the ability. The faint subscripts run as a move ends, as the
    hazards finish with a newcomer and as the turn ends, so it is looked at
    there; each Pokemon on the field keeps the count of the others down
    (Mon.soul_seen), so each faint counts once and one that gains the
    ability later counts only the faints after. Until 2026-10-20 it did
    nothing (Ian approved the fix). In a double battle each faint raises the first
    holder in speed order that is up and below +6 (BtlCmd_TrySoulHeart over
    monSpeedOrder, end_order here), so of two holders only the faster
    gains, the slower when the faster is at +6; the faints are counted for
    the battle (Battle.soul_down), so a holder that comes in counts only
    those after. Until 2026-10-21 every holder gained (Ian approved the
    double-battle part batch 12 left on 2026-10-20)."""
    if b.doubles:
        down = sum(1 for side in (b.p, b.b) for m in side.mons if not m.alive())
        new, b.soul_down = down - b.soul_down, down
        holders = [m for m in end_order(b) if m.alive() and m.ability == "Soul Heart"] if new > 0 else ()
        for _ in range(new):
            m = next((m for m in holders if m.stages["spa"] < 6), None)
            if m is None:
                break
            change_stages(m, {"spa": 1})
            reveal(m)
        return
    for m in b.p.on_field() + b.b.on_field():
        if not m.alive():
            continue
        down = fainted_others(b, m)
        if m.ability == "Soul Heart":
            for _ in range(down - m.soul_seen):
                if m.stages["spa"] < 6:
                    change_stages(m, {"spa": 1})
                    reveal(m)
        m.soul_seen = down


# Castform's type in each weather (BattleSystem_TriggerFormChange).
FORECAST_TYPE = {"Sun": "Fire", "Rain": "Water", "Hail": "Ice"}


def forecast(b, field=None):
    """Castform's form check (BattleSystem_TriggerFormChange, in the
    switch-in check and after every move): a Castform standing with Forecast
    takes the weather's type alone, Fire in sun, Water in rain, Ice in hail,
    and Normal in any other weather or none, or with Cloud Nine or Air Lock
    on the field, whenever it is not of that type already. The battle's type
    checks (a burn, a freeze, the hail, the trainer's AI) read it at once;
    its rows need no twin, since the calculator types it by each row's
    weather (checkForecast). A Castform that has lost Forecast keeps the form
    it has, and leaving brings its own type back. Until 2026-10-14 it stayed
    Normal in every weather (Ian approved the fix)."""
    for m in b.p.on_field() + b.b.on_field() if field is None else field:     # field: move_end's list
        if m.species != "Castform" or not m.alive() or m.ability != "Forecast":
            continue
        want = "Normal" if weather_ignored(b) else FORECAST_TYPE.get(b.weather, "Normal")
        if want not in m.types:
            m.types, m.retyped, m.formed = [want], True, True


def _use_move(b, att, mv, dfn, first, targets=None):
    if not att.alive():
        return
    att.acted_turn = b.turn      # its action this turn has begun (a Truant given later this turn: set_ability)
    mv = encored_move(att, mv)
    # Its own record clears with its action, whatever happens
    # (BattleControllerPlayer_ClearFlags), and so does its Destiny Bond. The
    # record as it stood is what this action's Conversion 2 reads.
    att.conversion2_src = (att.last_hit_by, att.last_hit_type) if att.last_hit_by is not None else None
    att.last_hit_by = None
    att.destiny_bond = False
    b.status_src = att           # a status this move gives comes from att (Synchronize)
    if att.rare:
        # Grudge and a Sky Drop's hold come with the rare flag: its Grudge
        # ends as its action begins (CHECK_STATUS_START), and held in the
        # air by Sky Drop it does nothing (sky_held).
        if att.grudge:
            att.grudge = False
        if att.sky_holder is not None and sky_held(b, att):
            return could_not_act(b, att, mv, dfn, targets)
    # The user's own state first.
    if att.recharge:
        att.recharge = False
        return could_not_act(b, att, mv, dfn, targets)
    if loafs(att):
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
        flinched(att)                # Steadfast answers it
        return could_not_act(b, att, mv, dfn, targets)
    if att.disabled is not None and mv.name == att.disabled:
        att.choice = None            # subscript_move_is_disabled lets go of a Choice item's lock
        return could_not_act(b, att, mv, dfn, targets)
    # Taunt, Imprison, Gravity, Heal Block and Throat Chop are checked in the
    # engine's order (CHECK_STATUS_STATE_TAUNT to _THROAT_CHOP), all before
    # confusion, paralysis and love, so a taunted Pokemon's status move
    # fails before its confusion can make it hurt itself, and with its
    # confusion's count kept. Until 2026-10-15 Taunt and Heal Block came
    # after love (Ian approved the fix).
    if att.taunt and mv.cat == "Status":
        return could_not_act(b, att, mv, dfn, targets)
    if mv.name in att.sealed:
        att.choice = None            # a foe's Imprison lets go of it too (disabled_out)
        return could_not_act(b, att, mv, dfn, targets)
    if ((att.rare or b.gravity) and move_barred(b, att, mv)) or move_heal_blocked(att, mv):
        return could_not_act(b, att, mv, dfn, targets)     # Gravity's, Heal Block's or Throat Chop's (move_barred)
    if att.confused:
        att.confused -= 1
        if att.confused and b.rng.random() < 0.5:
            hurt(b, att, confusion_damage(att, b.rng))
            return could_not_act(b, att, mv, dfn, targets)
    if att.status == "par" and b.rng.random() < 0.25:
        return could_not_act(b, att, mv, dfn, targets)
    if att.infatuated and b.rng.random() < 0.5:
        return could_not_act(b, att, mv, dfn, targets)     # immobilized by love (CHECK_STATUS_STATE_ATTRACT)
    if tormented_out(att, mv):
        return could_not_act(b, att, mv, dfn, targets)
    mark_hit(b, mv, dfn, True, targets)
    prev = note_move(b, mv)      # the move before this one, for Copycat
    spend_pp(b, att, mv, dfn, targets)
    paid = mv                    # the move in the slot that paid, whatever it calls (Grudge's ATTACKER_MOVE_SLOT)
    if mv.effect not in ("PROTECT", "SURVIVE_WITH_1_HP") and mv.const not in KEEPS_PROTECT_RUN:
        att.protect_run = 0
    att.last = mv
    if att.item and att.item.startswith("Choice") and not att.choice:
        att.choice = mv.name
    protean(b, att, mv)
    if commit_move(att, mv):
        return                   # Last Resort before every other move was used
    if mv.effect in CALLERS:
        mv = called_move(b, att, mv, prev, lambda kind, n: b.rng.randrange(n))
        if mv is None:
            return               # nothing to call: it fails
        mark_hit(b, mv, dfn, True, targets)     # the called move is the last to hit its target (moveHit)
    if mv.effect == "USE_MOVE_FIRST":
        mv = me_first_move(att, dfn, first)     # the target's chosen hit, at half again (me_first_move)
        if mv is None:
            return
        mark_hit(b, mv, dfn, True, targets)
    if mv.effect == "NATURE_POWER":
        mv = move(nature_power_move(b.st.get("terrain")))     # its terrain's move, as its own
        mark_hit(b, mv, dfn, True, targets)
    if mv.effect in ("FLY", "BOUNCE") and att.smacked:
        return                   # brought down, it cannot take to the air (effect scripts 155 and 263)
    if mv.effect == "SKY_DROP" and not getattr(b, "doubles", False) and not sky_drop(b, att, mv, dfn):
        return                   # Sky Drop's lift, or a drop that fails (sky_drop)
    # Charging moves: the first turn only charges (Fly and Dig vanish).
    if mv.effect in TWO_TURN and att.charging is None and not charge_skipped(b, att, mv):
        att.charging = mv
        change_stages(att, CHARGE_STAGES.get(mv.effect, {}))     # Skull Bash, Meteor Beam, Electro Shot
        return
    att.charging = None
    if mv.effect == "USE_RANDOM_LEARNED_MOVE_SLEEP":
        # Sleep Talk works only asleep, and then uses one of its other moves.
        mv = sleep_talk_pick(b, att) if att.status == "slp" else None
        if mv is None:
            return
    if mv.cat == "Status":
        thief = snatched(b, att, mv) if b.snatching and mv.snatch else None
        if thief is not None:
            status_move(b, thief, mv, att, first)     # the move is the Snatch user's (snatched)
            return
        status_move(b, att, mv, dfn, first)
        return
    chance = lambda kind, p, victim: b.rng.random() < p      # noqa: E731
    pick = lambda kind, n: b.rng.randrange(n)               # noqa: E731
    if targets is None:
        before = dfn.hp
        if att.ability == "Analytic" and moves_last(b, first):
            # Its foe has acted this turn, or switched in.
            b.analytic = att
            try:
                attack(b, att, mv, dfn, first)
            finally:
                b.analytic = None
        else:
            attack(b, att, mv, dfn, first)
        hit_aftermath(b, att, dfn, mv, chance, pick)
        if b.blown is att:
            mind_blown_cost(b, att)
        destiny_bond(att, dfn)
        if dfn.grudge:
            grudge(att, dfn, paid, mv)
        knockout_boost(att, dfn, before)
        if mv.const == "MOVE_RELIC_SONG":
            relic_song(b, att, mv, b.last_dealt > 0)     # Meloetta's form (relic_song)
        return
    # A double battle: a spread move hits each target at three quarters.
    b.spread = len(targets) > 1
    before = {id(t): t.hp for t in targets}
    for t in targets:
        attack(b, att, mv, t, t not in b.moved)
        hit_aftermath(b, att, t, mv, chance, pick)
    b.spread = False
    if b.blown is att:
        mind_blown_cost(b, att)          # once, after every target (mind_blown_cost)
    for t in targets:
        destiny_bond(att, t)
        if t.grudge:
            grudge(att, t, paid, mv)
        knockout_boost(att, t, before[id(t)])
    if mv.const == "MOVE_RELIC_SONG":
        relic_song(b, att, mv, any(t.hp < before[id(t)] for t in targets))    # once a use, whatever it hit


def confusion_damage(mon, rng):
    """A 40-power typeless physical hit on itself, Generation 4's formula."""
    a = mon.stats.get("atk", 50) * stage_mult(mon.stages["atk"])
    d = mon.stats.get("def", 50) * stage_mult(mon.stages["def"])
    base = ((2 * mon.level // 5 + 2) * 40 * a / d) // 50 + 2
    return int(base * rng.randint(85, 100) / 100)


def mind_blown(b, att):
    """Mind Blown's effect script (408): a Damp Pokemon anywhere on the
    field, its user included, stops the move before it starts, unless the
    user has Mold Breaker, and nothing is paid (False); else the script
    marks its user (SELF_TURN_FLAG_MIND_BLOWN, Battle.blown), which then
    pays as the move ends, whether it hit, missed or met Protect or an
    immunity (mind_blown_cost). A move with no target never runs its
    script, so attack() comes here only with one."""
    if att.ability != "Mold Breaker" and any(
            m.ability == "Damp" and m.alive() for m in b.p.on_field() + b.b.on_field()):
        return False
    b.blown = att
    return True


def mind_blown_cost(b, att):
    """Mind Blown's cost (BattleControllerPlayer_FaintAfterSelfdestruct,
    subscript_recoil_half_max_hp): once the move is over, once whatever its
    targets, a user still standing loses half its maximum HP, rounded up;
    Magic Guard spares it and Rock Head does not, as it is a cost rather
    than recoil. Until 2026-10-20 the move cost nothing (Ian approved the
    fix)."""
    b.blown = None
    if att.alive() and att.ability != "Magic Guard":
        hurt(b, att, (att.maxhp + 1) // 2)


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
    if att.ability == "Neutralizing Gas" and b.st.get("gas"):
        gas_update(b, check=False)       # a holder's gas is gone before its blast lands, so the target's ability counts
    return True


def attack(b, att, mv, dfn, first):
    b.last_dealt = 0                     # the HP this move took, for the contact abilities
    b.hits_landed = False                # a move of several hits that land_hits landed
    b.sub_hit = False                    # a Substitute it has hit (Battle.sub_hit)
    if mv.effect == "BIDE" and not bide_releases(att, mv):
        return                   # Bide starts, stores, or has nothing to give back (bide_releases)
    if not dfn.alive():
        rollout_break(att, mv)           # no target (subscript_no_target)
        return
    if loses_type_fails(att, mv):
        return                           # Burn Up or Double Shock without its type (lose_type)
    if dream_eater_fails(att, dfn, mv) or lost_focus(att, mv) or (mv.effect == "DAMAGE_WHILE_ASLEEP"
                                                                 and snore_fails(att, mv)):
        return
    if mv.effect in FAILS_BEFORE and fails_before(att, dfn, mv):
        return                           # Poltergeist, Belch and First Impression's own failures (fails_before)
    spit = spit_up_key(att) if mv.effect == "SPIT_UP" else None
    if mv.effect == "SPIT_UP" and spit is None:
        return
    # Telepathy: its holder takes no damaging move from its partner
    # (BattleControllerPlayer_PriorityBlock, which Mold Breaker gets past),
    # a spread move's in a double battle; the message names the ability.
    # Until 2026-10-14 the partner's spread moves hit it (Ian approved the fix).
    if att is not dfn and att.side == dfn.side and dfn.ability == "Telepathy" and mv.power and not mold(att, dfn):
        reveal(dfn)
        return
    if mv.effect == "MIND_BLOWN" and not mind_blown(b, att):
        return                   # a Damp Pokemon stops it, and nothing is paid (mind_blown)
    if mv.effect in SELF_KO and not explode_first(b, att):
        return
    if mv.effect == FUTURE_SIGHT:
        # Future Sight and Doom Desire strike later (foresee). As used they
        # pass Protect, the air and the ground and every immunity, and roll
        # no accuracy (effect script 148 sets SYSCTL_NONSTANDARD_ACC_CHECK).
        dmg = b.damage(att, dfn, mv, crit=False)
        if dmg is not None:
            foresee(b, att, mv, dfn, dmg)
        return
    if dfn.charging is not None and dfn.charging.effect in INVULNERABLE and not reaches(mv, dfn) \
            and not lands_sure(att, dfn, mv):
        _crash(b, att, dfn, mv)
        rollout_break(att, mv)
        return                   # No Guard reaches it there (no_guard)
    if protected(b, att, mv, dfn):
        _crash(b, att, dfn, mv)
        rollout_break(att, mv)
        return
    if mv.effect == "REMOVE_PROTECT" and not dfn.protecting:
        return                   # Feint and Hyperspace Hole fail on a target not protecting (BtlCmd_TryFeint)
    if lifted(dfn, mv):
        return
    if mv.effect == "HIT_FIRST_IF_TARGET_ATTACKING":        # Sucker Punch
        nxt = getattr(dfn, "chosen", None)
        if not first or nxt is None or nxt.cat == "Status":
            return
    if move_fails_first(att, mv, dfn, first):
        return
    if mv.effect == "ALWAYS_FLINCH_FIRST_TURN_ONLY" and att.turns_in > 0:
        return
    # Natural Gift and Fling spend the held item, and fail without one (a
    # Natural Gift needs a berry).
    gift = None
    if mv.name in ("Natural Gift", "Fling"):
        if not att.item or (mv.name == "Natural Gift" and "Berry" not in att.item):
            return
        if mv.name == "Fling" and not item_fling(att.item)[0]:
            return               # an item with no fling power cannot be thrown (TryFling)
        gift = att.item
        consume(att, eaten=False)
        mark_unheld(b, att)          # a trainer's flung item gone from its rows too (item twin)
    if gift is not None and mv.name == "Fling":
        b.flung = gift               # its effect after the hit (fling_effect)
    if not b.accuracy_hits(att, dfn, mv, first):
        _crash(b, att, dfn, mv)          # Magic Guard spares it (crash_loss)
        rollout_after(att, mv, False)
        return
    if dfn.ability == "Queenly Majesty" and majesty_blocked(att, dfn, mv):
        return                           # a raised move into Queenly Majesty (majesty_blocked)
    rollout_after(att, mv, True)
    # The hits this use makes: a two to five hit move's roll, or Fury
    # Cutter's run until a miss (a Loaded Dice skips the later checks).
    hits = 1
    odds = multi_hit_odds(att, mv)
    if odds:
        hits = b.rng.choices([h for h, _w in odds], [w for _h, w in odds])[0]
    elif mv.effect in RISING:
        # A later hit's check skips the hit overrides, No Guard and Lock-On (RISING)
        while hits < RISING_COUNT and (att.item == "Loaded Dice" or b.accuracy_hits(att, dfn, mv, first, later=True)):
            hits += 1
    elif mv.effect == TEN_HITS:
        # Population Bomb's later checks skip the hit overrides (TEN_HITS)
        while hits < 10 and b.accuracy_hits(att, dfn, mv, first, later=True):
            hits += 1
    elif mv.effect in TWO_HITS:
        hits = 2
    elif mv.effect in THREE_HITS:
        hits = 3
    if mv.effect == "BEAT_UP":
        # Each eligible party member's own hit, on this battle's dice (beat_up_hits).
        dealt = beat_up_hits(b, att, mv, dfn, first, lambda n, rate: [b.rng.random() < rate for _ in range(n)],
                             lambda i, crit: b.rng.randrange(16),
                             lambda kind, p, victim: b.rng.random() < p, lambda kind, n: b.rng.randrange(n))
        return _after_attack(b, att, mv, dfn, first, dealt)
    if mv.effect in HIT_BY_HIT:
        dealt = _attack_hits(b, att, mv, dfn, first, hits)
        if dealt is None:
            return
        return _after_attack(b, att, mv, dfn, first, dealt)
    present = present_roll(b) if mv.effect == "RANDOM_POWER_MAYBE_HEAL" else None
    if present == 0:
        present_heal(dfn)                # Present's gift instead of a hit (present_heal)
        return
    # Fixed-damage moves.
    dmg = fixed_damage(b, att, dfn, mv, b.rng.randint(5, 15) if mv.effect == "RANDOM_DAMAGE_1_TO_150_LEVEL" else 10)
    if mv.effect == "ONE_HIT_KO":
        if ohko_blocked(b, att, dfn, mv) or b.rng.random() * 100 >= 30 + att.level - dfn.level:
            return
        dmg = dfn.hp
    elif mv.effect in ("COUNTER", "MIRROR_COAT", "METAL_BURST"):
        hit = att.hit_this_turn
        want = {"COUNTER": "Physical", "MIRROR_COAT": "Special"}.get(mv.effect)
        if not hit or (want and hit[0] != want) or effectiveness(b.st["chart"], mv.type, chart_types(dfn, mv)) == 0:
            return
        dmg = int(hit[1] * (1.5 if mv.effect == "METAL_BURST" else 2))
    crit = False
    if dmg is None:
        stage = att.crit_stage + (att.ability == "Super Luck") + (1 if mv.effect.startswith("HIGH_CRITICAL") or
                                  mv.effect.startswith("CHARGE_TURN_HIGH_CRIT") else 0)
        crit = ((mv.sure or merciless(att, dfn) or focused(att) or b.rng.random() < CRIT_RATE[min(stage, 4)])
                and not crit_proof(att, dfn, b) and not b.st.get("first_battle"))
        if spit is not None:
            key, att.key = att.key, spit
            try:
                dmg = b.damage(att, dfn, mv, crit=crit, roll=15)     # Spit Up's row, its top roll
            finally:
                att.key = key
        elif mv.name == "Natural Gift" and att.side == "p":
            key, att.key = att.key, natural_gift_key(att.key, gift)
            try:
                dmg = b.damage(att, dfn, mv, crit=crit)
            finally:
                att.key = key
        elif mv.name == "Fling" and att.side == "p":
            key, att.key = att.key, fling_key(att.key, gift)
            try:
                dmg = b.damage(att, dfn, mv, crit=crit)
            finally:
                att.key = key
        elif present is not None:
            key, att.key = att.key, f"{att.key}#pr{present}"
            try:
                dmg = b.damage(att, dfn, mv, crit=crit)     # Present's row at its rolled power
            finally:
                att.key = key
        else:
            dmg = b.damage(att, dfn, mv, crit=crit)
        if dmg is None:
            return
        dmg = use_damage(att, mv, dmg, hits)
        dmg = berry_first_hit(b, dfn, mv, dmg, hits)
        if mv.effect == "DOUBLE_POWER_IF_MOVING_SECOND" and not first:
            # BtlCmd_CalcPaybackPower: twice the power once the target has
            # acted this turn (moved, switched or used an item).
            dmg = int(dmg * doubled_power(att, mv))
        if mv.effect == "DOUBLE_POWER_IF_FASTER" and beak_doubles(b, dfn, first):
            dmg = int(dmg * doubled_power(att, mv))     # Bolt Beak and Fishious Rend (beak_doubles)
        if mv.effect == "FICKLE_BEAM" and fickle_doubles(b):
            dmg = int(dmg * doubled_power(att, mv))     # three times in ten (fickle_doubles)
        # A doubled power meets Technician after it is doubled (doubled_power).
        if mv.effect == "DOUBLE_POWER_WHEN_STATUSED" and att.status:
            dmg = int(dmg * doubled_power(att, mv))
        if mv.effect == "DOUBLE_POWER_IF_HIT" and att.hit_this_turn:
            dmg = int(dmg * doubled_power(att, mv))
        if mv.effect == "DOUBLE_POWER_WHEN_BELOW_HALF" and dfn.hp * 2 <= dfn.maxhp:
            dmg = int(dmg * doubled_power(att, mv))
        if mv.effect == "DOUBLE_POWER_HEAL_SLEEP" and slap_doubles(att, dfn, mv):
            dmg = int(dmg * doubled_power(att, mv))     # Wake-Up Slap, no Substitute in the way
        if doubled(att, dfn, mv):
            dmg = int(dmg * doubled_power(att, mv))
    if dmg <= 0:
        rollout_break(att, mv)       # an immunity stops the run (subscript_missed)
        if dfn.ability in ZEROING and effectiveness(b.st["chart"], mv.type, dfn.types) > 0:
            reveal(dfn)              # an absorbing ability, Levitate or Wonder Guard took it
            if dfn.ability == "Flash Fire" and mv.type == "Fire":
                dfn.flash_fire = True
            absorb(b, att, dfn, mv)  # and a heal or a stage for the ones that give one
        return
    # The hit lands: Substitute, Focus Sash and Sturdy, then the damage.
    if sub_blocks(att, dfn, mv):
        dfn.sub = max(0, dfn.sub - dmg)
        dealt = 0
        b.sub_hit = True         # broken or not, nothing of the hit reaches the Pokemon behind it
        if mv.effect == "EAT_BERRY":
            # Bug Bite and Pluck eat the Berry of the Pokemon behind it all
            # the same: their effect script's indirect effect
            # (MOVE_SUBSCRIPT_PTR_PLUCK, subscript_pluck and TryPluck) asks
            # nothing of a Substitute. Until 2026-10-20 the Substitute kept
            # the Berry (Ian approved the fix on 2026-10-20).
            pluck(b, att, dfn, lambda kind, n: b.rng.randrange(n))
    else:
        if mv.effect == "LEAVE_WITH_1_HP" and dmg >= dfn.hp:
            # False Swipe and Hold Back (effect script 101): a hit that would
            # knock its target out leaves it at 1 HP, and one at 1 HP deals
            # nothing (battle_controller_player.c, after the Substitute and
            # before Sturdy and the Focus items, so neither is spent). Until
            # 2026-10-15 they could knock out (Ian approved the fix).
            dmg = dfn.hp - 1
        # Focus Sash and Sturdy hold one hit from full HP; a move of several
        # hits lands them one at a time (land_hits) and never comes here.
        full = dfn.hp == dfn.maxhp and hits < 2
        if dmg >= dfn.hp and full and (dfn.item == "Focus Sash" or dfn.ability == "Sturdy"):
            if dfn.ability == "Sturdy":
                reveal(dfn)
            dmg = dfn.hp - 1
            if dfn.item == "Focus Sash":
                consume(dfn)
        if dmg >= dfn.hp and getattr(dfn, "enduring", False):
            dmg = dfn.hp - 1
        dealt = min(dmg, dfn.hp)
        dfn.hp -= dealt
        b.last_dealt, b.hit_left = dealt, dfn.hp
        if mv.effect in TAKES_FIRST and dealt > 0:
            take_first(b, att, dfn, mv, lambda kind, n: b.rng.randrange(n))     # Knock Off's and Bug Bite's (take_first)
        dfn.hit_this_turn = (mv.cat, dealt)
        if dfn.bide:
            bide_store(dfn, dealt)       # a Bide user stores what it took
        if dfn.status == "frz" and mv.type == "Fire":
            dfn.status = None
    if crit:
        anger_point(dfn)
    _after_attack(b, att, mv, dfn, first, dealt)


def crash_loss(att, dfn, damage):
    """The HP a Jump Kick, High Jump Kick or Supercell Slam that failed to
    hit costs its user (subscript_crash_on_miss, called from every path of
    subscript_missed): half the damage its hit would have done to the
    target, type chart and same-type bonus in, which the effect script
    worked out before the checks (so nothing against a type that is immune),
    at most half the target's maximum HP; nothing for a Magic Guard holder.
    Until 2026-10-15 a miss cost half the user's own maximum HP, and a
    Protect or a target in the air cost nothing (Ian approved the fix)."""
    if att.ability == "Magic Guard" or not damage:
        return 0
    return min(engine_divide(damage, 2), engine_divide(dfn.maxhp, 2))


# The effects whose miss crashes (SYSCTL_CRASH_DAMAGE, set by effect
# scripts 45 and 293): Jump Kick's kind, and Axe Kick, whose crash
# subscript_missed runs as it runs theirs. Until 2026-10-15 Axe Kick never
# crashed (Ian approved the fix).
CRASH = frozenset({"CRASH_ON_MISS", "CONFUSE_HIT_CRASH_ON_MISS"})
# The hits that confuse at their chance (subscript_confuse as a hit's
# indirect effect): Confusion's kind, Hurricane, Raging Fury, and Axe Kick
# (effect script 293), whose 30 per cent never ran until 2026-10-15 (Ian
# approved the fix).
CONFUSE_HITS = frozenset({"CONFUSE_HIT", "HURRICANE", "RECOIL_CONFUSE_HIT", "CONFUSE_HIT_CRASH_ON_MISS"})


def _crash(b, att, dfn, mv):
    """fightsim's own battle: a crash move that failed to hit, its damage
    rolled with a critical hit at its odds (crash_loss)."""
    if mv.effect not in CRASH or att.ability == "Magic Guard":
        return
    crit = b.rng.random() < crit_rate(b, att, dfn, mv)
    hurt(b, att, crash_loss(att, dfn, b.damage(att, dfn, mv, crit=crit) or 0))


# Chatter's chance to confuse (effect script 267, BtlCmd_CheckChatterActivation):
# a roll of 0 to 99 no higher than the user's recorded cry's figure confuses,
# and that figure is 0 with no recording, as every trainer's Chatot has and as
# the simulator takes the player's, so 1 in 100 (a loud recording makes it 10
# or 30, so 11 or 31 in 100).
CHATTER_ODDS = 0.01


def chatter_confuses(att, dfn, stripped):
    """Whether this Chatter may confuse at CHATTER_ODDS: only a Chatot's, and
    not under Sheer Force (CHATTER is on sSheerForceEffects) or into Shield
    Dust (subscript_confuse checks it for a hit's effect; Mold Breaker gets
    past it). The confusion's own blockers follow (confusion_blocked). Until
    2026-10-15 Chatter never confused (Ian approved the fix)."""
    return (att.species == "Chatot" and not stripped
            and not (dfn.ability == "Shield Dust" and not mold(att, dfn)))


def clear_smog(dfn):
    """Clear Smog's hit (effect script 390, subscript_clear_smog, run on the
    hit): a target still standing and not behind a Substitute has every
    stat stage put back to 0; a chance-free effect, so Shield Dust and Sheer
    Force (not on sSheerForceEffects) leave it alone. Until 2026-10-15 it
    was a plain hit (Ian approved the fix)."""
    dfn.stages = dict.fromkeys(STAGE_KEYS, 0)


def drag_out(b, att, dfn, pick):
    """Dragon Tail and Circle Throw (effect script 395's hit, then
    subscript_force_switch_hit from the after-move effects, once the
    target's ability and held items have answered; hit_aftermath): unless
    the target fainted, the user fell (to Rough Skin, say), the hit met a
    Substitute, the target has Suction Cups (which a Mold Breaker passes) or
    Ingrain roots it, the target is dragged out for a party member drawn at
    random (BtlCmd_TryDragonTail), which meets the hazards as it comes in;
    with no one left to send in, nothing happens. The hit has done its
    damage, so none of these fails the move. Until 2026-10-15 the target
    stayed in (Ian approved the fix). In a double battle the one drawn
    comes from the target's own trainer's party into the target's slot
    (drag_pick); until 2026-10-21 the target stayed in there (Ian approved
    the double-battle part of batch 7 on 2026-10-14)."""
    if not att.alive() or not dfn.alive() or getattr(dfn, "ingrained", False) \
            or (dfn.ability == "Suction Cups" and not mold(att, dfn)):
        return
    side = b.p if dfn.side == "p" else b.b
    if b.doubles:
        idx = drag_pick(b, dfn, pick)
        if idx is not None:
            switch_in(b, side, idx, slot=slot_of(side, dfn))
        return
    bench = side.bench()
    if bench:
        switch_in(b, side, side.mons.index(bench[pick("roar", len(bench))]))


def drag_pick(b, dfn, pick):
    """The party index BattleScript_PickDraggedOutMon draws to come in for
    dfn in a double battle, or None. The party is dfn's own trainer's (a
    tag battle's two trainers, or the player and a partner, each have their
    own; one trainer's double battle has one), and the move fails unless it
    has more Pokemon standing, those on the field included, than the
    slots it fills, two for one trainer's pair and one each in a tag or
    partner battle: a pair whose other slot has fainted with one Pokemon
    waiting fails. The one drawn is any of that party standing off the
    field, at even odds (pick(kind, n)). Roar's and Whirlwind's level check
    (BattleSystem_CanWhirlwind, whirlwind_odds) comes before the draw, in
    the double battles as in the single ones (perfectline.whirlwind_passes);
    until 2026-10-21 neither had it."""
    side = b.p if dfn.side == "p" else b.b
    owner = getattr(dfn, "owner", None)
    mine = [m for m in side.mons if getattr(m, "owner", None) == owner]
    field = side.on_field()
    slots = sum(1 for m in field if getattr(m, "owner", None) == owner)
    if sum(m.alive() for m in mine) <= slots:
        return None
    cands = [m for m in mine if m.alive() and m not in field]
    if not cands:
        return None
    return side.mons.index(cands[pick("roar", len(cands))])


@functools.lru_cache(maxsize=None)
def whirlwind_odds(user_level, target_level):
    """The chance Roar or Whirlwind passes its level check in a trainer
    battle (BattleScript_PickDraggedOutMon with checkLevel, once its target
    has someone to send in, asks BattleSystem_CanWhirlwind): always when the
    user is of the target's level or higher; otherwise a random byte r
    passes when ((r * (user's level + target's level)) >> 8) + 1 is above a
    quarter of the target's level, rounded down. Dragon Tail and Circle
    Throw skip the check (BtlCmd_TryDragonTail)."""
    if user_level >= target_level:
        return 1.0
    return sum(((r * (user_level + target_level)) >> 8) + 1 > target_level // 4 for r in range(256)) / 256


def drag_coming(b, att, dfn, mv):
    """Whether this hit of Dragon Tail or Circle Throw will drag dfn out once
    its ability and items have answered it (the engine's HitWillDragTarget,
    which Pickpocket asks): hit_aftermath's and drag_out's own conditions,
    read before the drag runs."""
    if mv.effect != "FORCE_SWITCH_HIT" or getattr(b, "last_dealt", 0) <= 0 or b.sub_hit:
        return False
    if not att.alive() or not dfn.alive() or getattr(dfn, "ingrained", False) \
            or (dfn.ability == "Suction Cups" and not mold(att, dfn)):
        return False
    if b.doubles:
        return drag_pick(b, dfn, lambda kind, n: 0) is not None
    return bool((b.p if dfn.side == "p" else b.b).bench())


@functools.lru_cache(maxsize=None)
def incinerable():
    """The Berries Incinerate burns (subscript_incinerate's range, Cheri to
    Rowap in generated/items.txt), by the names the battle gives items; the
    Roseli Berry, which Oxide added after Rowap, is not among them."""
    with open(os.path.join(data.ROOT, "generated", "items.txt"), encoding="utf-8") as fh:
        consts = [x.strip() for x in fh if x.strip()]
    lo, hi = consts.index("ITEM_CHERI_BERRY"), consts.index("ITEM_ROWAP_BERRY")
    return frozenset(" ".join(w.title() for w in c[len("ITEM_"):].split("_")) for c in consts[lo:hi + 1])


def incinerate(b, dfn, mv):
    """Incinerate's hit (effect script 372, subscript_incinerate, run on the
    hit): a target still standing and not behind a Substitute loses a Berry
    it holds, burned up rather than used, so Recycle cannot bring it back
    and it counts as no Berry eaten. The added effect comes before the
    defender's held item is checked (AFTER_MOVE_EFFECT_DEFENDER_ITEM), so a
    Sitrus Berry the hit brought into range burns before it is eaten; a
    resist Berry that halved the hit was used up in the damage, so after_hit
    takes it as used. Until 2026-10-15 it was a plain hit and the target ate
    its Berry later (Ian approved the fix)."""
    if dfn.item_off is not None:
        return raw_item_op((dfn,), lambda: incinerate(b, dfn, mv))
    if dfn.item in incinerable() and resist_berry(b, dfn, mv) != dfn.item:
        dfn.item = None


def slap_doubles(att, dfn, mv):
    """Wake-Up Slap (effect script 217) doubles its power (POWER_MULTI 20)
    on a sleeping target with no Substitute in the way (CheckSubstitute
    skips both the doubling and the wake-up, Infiltrator passing it), and
    only then sets its wake-up subscript. Until 2026-10-15 it doubled into
    a Substitute too (Ian approved the fix)."""
    return mv.effect == "DOUBLE_POWER_HEAL_SLEEP" and dfn.status == "slp" and not sub_blocks(att, dfn, mv)


def slap_wakes(dfn, mv):
    """Wake-Up Slap's doubled hit wakes its target once it has landed and
    left the target standing (subscript_heal_target_sleep, ON_HIT, which
    skips a target at 0 HP); a chance-free effect, so Shield Dust and Sheer
    Force leave it alone. Until 2026-10-15 the target slept on, and every
    later Wake-Up Slap doubled too (Ian approved the fix)."""
    if mv.effect == "DOUBLE_POWER_HEAL_SLEEP" and dfn.alive() and dfn.status == "slp":
        dfn.status, dfn.sleep = None, 0


def salts_cure(dfn, mv):
    """Smelling Salts' doubled hit cures its target's paralysis once it has
    landed and left the target standing (subscript_heal_target_paralysis,
    ON_HIT, which skips a target at 0 HP); chance-free, so Shield Dust and
    Sheer Force leave it alone. Until 2026-10-15 the target stayed
    paralysed (Ian approved the fix)."""
    if mv.effect == "DOUBLE_POWER_AND_CURE_PARALYSIS" and dfn.alive() and dfn.status == "par":
        dfn.status = None


def dream_eater_fails(att, dfn, mv):
    """Dream Eater (effect script 8) "wasn't affected" by a target that is
    not asleep, or one behind a Substitute an Infiltrator does not pass
    (CheckSubstitute), before its accuracy or the target's Protect is
    checked; a Comatose target is not asleep to it, as the script reads only
    the sleep status. Until 2026-10-15 it hit an awake target and drained
    half (Ian approved the fix)."""
    return mv.effect == "RECOVER_DAMAGE_SLEEP" and (dfn.status != "slp" or sub_blocks(att, dfn, mv))


# The moves whose own effect script can fail them before their accuracy,
# a Protect or the target's reach is checked, each looked at once by effect
# (fails_before).
FAILS_BEFORE = frozenset({"POLTERGEIST", "BELCH", "FIRST_TURN_ONLY"})


def fails_before(att, dfn, mv):
    """Whether mv, one of FAILS_BEFORE, fails in its effect script before
    it is aimed. Poltergeist (effect script 345): against a target that
    holds no item (BATTLEMON_HELD_ITEM, the item itself, so one that
    Embargo or Magic Room holds back still counts). Belch (effect script
    396, TryBelch): until its user has eaten a Berry this battle
    (Battler_HasEatenBerry, kept for its party slot, so a switch keeps it:
    Mon.ate_berry, which consume and pluck set). First Impression (effect
    script 373): after its user's first turn out, as Fake Out's script
    reads it (fakeOutTurnNumber against the turn count, turns_in here),
    before a Protect is checked, so a Spiky Shield it would meet costs
    nothing. Until 2026-10-15 all three hit every time (Ian approved the
    fixes)."""
    e = mv.effect
    if e == "POLTERGEIST":
        return dfn.item is None and dfn.item_off is None
    if e == "BELCH":
        return not att.ate_berry
    if e == "FIRST_TURN_ONLY":
        return att.turns_in > 0
    return False


def snore_fails(att, mv):
    """Snore (effect script 92) fails when its user is awake, before its
    accuracy is checked, as the script reads the sleep status first; a
    sleeper that wakes this turn is awake by then. Until 2026-10-15 an
    awake Snore hit (Ian approved the fix)."""
    return mv.effect == "DAMAGE_WHILE_ASLEEP" and att.status != "slp"


def lost_focus(att, mv):
    """Focus Punch (effect script 170) "lost its focus and couldn't move"
    when a physical or special hit has taken HP from its user earlier this
    turn (the turn's damage masks, which a hit on its Substitute leaves
    alone), before its accuracy is checked; its PP is spent. Until
    2026-10-15 it always landed (Ian approved the fix)."""
    return mv.effect == "HIT_LAST_WHIFF_IF_HIT" and bool(att.hit_this_turn)


def crit_proof(att, dfn, b=None):
    """Battle Armor and Shell Armor keep critical hits off their holder
    unless att's Mold Breaker gets past them (BtlCmd_CalcCrit asks
    Battler_IgnorableAbility), and so does a Lucky Chant on its side, given
    the battle b (BattleSystem_CalcCriticalMulti reads the defender's
    SIDE_CONDITION_LUCKY_CHANT; until 2026-10-15 nothing did, Ian approved
    the fix)."""
    if b is not None and (b.p if dfn.side == "p" else b.b).lucky_chant:
        return True
    return dfn.ability in ("Battle Armor", "Shell Armor") and not mold(att, dfn)


# Flower Trick, Frost Breath, Storm Throw and Wicked Blow (effect script
# 282, Move.sure): BattleSystem_CalcCriticalMulti makes every hit critical,
# unless crit_proof or the first battle keeps it off (sure_crit).


def sure_crit(b, att, dfn):
    """Whether an always-critical move's hit lands critical: always, unless
    Battle Armor or Shell Armor (past Mold Breaker) or a Lucky Chant keeps
    it off (crit_proof), or it is the first battle (BtlCmd_CalcCrit)."""
    return not crit_proof(att, dfn, b) and not b.st.get("first_battle")


def row_crit_mult(att, dfn, crit):
    """What an always-critical move's damage takes on its row, which the
    calculator makes critical (its profile's alwaysCrit list, at Oxide's
    1.5, 2.25 for a Sniper) unless the target's Battle Armor or Shell Armor
    holds, which Mold Breaker clears there: nothing more when the hit is
    critical and its row is, the multiplier when the row is not, and the
    multiplier taken out of a row that is when the hit is not (a Lucky
    Chant, the first battle, the trainer's AI's estimate). Until 2026-10-15
    the row's critical hit stood with every stage and screen read as for a
    plain hit, and a further one in 24 critical hit came on top (Ian
    approved the fix)."""
    f = CRIT_MUL * (1.5 if att.ability == "Sniper" else 1.0)
    row = not (dfn.ability in ("Battle Armor", "Shell Armor") and att.ability != "Mold Breaker")
    if crit:
        return 1.0 if row else f
    return 1 / f if row else 1.0


def psych_up(att, dfn):
    """Psych Up (effect script 143, BtlCmd_CopyStatStages): the user takes
    every one of the target's stat stages, accuracy and evasion included,
    and its Focus Energy (VOLATILE_CONDITION_FOCUS_ENERGY is added to the
    user's own, never taken away); a stage the copy raises counts as one
    raised this turn (Oxide's Burning Jealousy flag). No Substitute or
    Protect stops it. Until 2026-10-15 it did nothing (Ian approved the
    fix)."""
    if any(dfn.stages[k] > att.stages[k] for k in STAGE_KEYS):
        att.stat_raised = True
    att.stages = dict(dfn.stages)
    att.crit_stage = max(att.crit_stage, dfn.crit_stage)


def lucky_chant(side):
    """Lucky Chant (effect script 240): five turns on its user's side, ended
    at the fifth turn's end (FIELD_COND_CHECK_STATE_LUCKY_CHANT); it fails
    while one runs."""
    if not side.lucky_chant:
        side.lucky_chant = 5


def lunar_blessing(b, att):
    """Lunar Blessing and Jungle Healing (effect script 415,
    subscript_lunar_blessing): the move fails when its user, and in a
    double battle its partner on the field, have full HP and no status;
    otherwise each of them below full HP regains a quarter of its maximum
    HP, rounded up, and each with a status is cured of it and of
    Nightmare. Heal Block stops it before it runs (move_heal_blocked).
    Until 2026-10-20 it did nothing (Ian approved the fix)."""
    mons = [att]
    ally = ally_of(b, att) if getattr(b, "doubles", False) else None
    if ally is not None:
        mons.append(ally)
    if all(m.hp == m.maxhp and not m.status for m in mons):
        return
    for m in mons:
        if m.hp < m.maxhp:
            heal(m, (m.maxhp + 3) // 4)
        if m.status:
            m.status, m.nightmare = None, False


def laser_focus(att):
    """Laser Focus (effect script 399, subscript_laser_focus): its user's
    count is set to 2 (MOVE_EFFECT_LASER_FOCUS_1), one off at each turn's
    end (MON_COND_CHECK_STATE_LOCK_ON, as Lock-On's), so every hit it
    makes on the next turn is critical (focused) unless crit_proof or the
    first battle keeps it off; gone as it leaves, and not handed on by
    Baton Pass (MOVE_EFFECT_BATON_PASSED leaves it out). Until 2026-10-20
    it did nothing (Ian approved the fix)."""
    att.laser_focus, att.rare = 2, True


def focused(att):
    """Whether Laser Focus makes att's hits critical now (laser_focus)."""
    return att.rare and att.laser_focus > 0


def merciless(att, dfn):
    """Merciless (BattleSystem_CalcCriticalMulti): every hit its holder lands
    on a poisoned or badly poisoned target is critical, unless crit_proof or
    the first battle keeps it off, as for an always-critical move. Until
    2026-10-20 it did nothing (Ian approved the fix)."""
    return att.ability == "Merciless" and dfn.status in ("psn", "tox")


def crit_rate(b, att, dfn, mv):
    """The chance a hit of mv lands critical: Oxide's rate at the attacker's
    stage, 0 against Battle Armor or Shell Armor (unless Mold Breaker), on
    a side under Lucky Chant and in the first battle (BtlCmd_CalcCrit)."""
    if crit_proof(att, dfn, b) or b.st.get("first_battle"):
        return 0.0
    if mv.sure or merciless(att, dfn) or focused(att):
        return 1.0                       # forced (sure_crit, merciless, laser_focus)
    stage = att.crit_stage + (att.ability == "Super Luck") + (1 if mv.effect.startswith("HIGH_CRITICAL") or
                                                               mv.effect.startswith("CHARGE_TURN_HIGH_CRIT") else 0)
    if att.item in ("Scope Lens", "Razor Claw"):
        stage += 1
    return CRIT_RATE[min(stage, 4)]


def _attack_hits(b, att, mv, dfn, first, hits):
    """fightsim's own landing of a move of several hits (land_hits), on its
    own dice: each hit rolls its critical hit and its damage roll. None when
    the move has no row or deals nothing (an immunity or an ability that
    takes it whole, handled as a single hit's would be); else the HP taken."""
    rolls = b.rolls(att, dfn, mv)
    if rolls is None:
        return None
    if rolls[-1] <= 0:
        if dfn.ability in ZEROING and effectiveness(b.st["chart"], mv.type, dfn.types) > 0:
            reveal(dfn)
            if dfn.ability == "Flash Fire" and mv.type == "Fire":
                dfn.flash_fire = True
            absorb(b, att, dfn, mv)
        return None
    rate = crit_rate(b, att, dfn, mv)
    crits = [b.rng.random() < rate for _ in range(hits)]
    weights, whole = hit_weights(att, mv, hits)

    def hit_damage(i, crit):
        d = b.damage(att, dfn, mv, crit=crit, share=(weights[i], whole)) or 0
        return int(d * reckless_fix(att, mv)) if reckless_fix(att, mv) != 1.0 else d

    b.hits_landed = True
    dealt = land_hits(b, att, dfn, mv, first, hits, hit_damage, crits,
                      lambda kind, p, victim: b.rng.random() < p, lambda kind, n: b.rng.randrange(n))
    b.last_dealt = dealt
    return dealt


def beat_up_party(b, att):
    """The members whose hits Beat Up lands, in party order (BtlCmd_BeatUp,
    BeatUpEligibleMon): its user, whatever its state, and every other
    member of its party with HP and no status."""
    side = b.p if att.side == "p" else b.b
    return [m for m in side.mons if m is att or (m.alive() and not m.status)]


def base_stat(b, mon, stat):
    """A Pokemon's species' base stat ("at", "df" and so on), as
    SpeciesData_GetFormValue gives it: its record's own species data
    where it has one (a twin's form), else its species'."""
    rec = b.st["pokemon"].get(mon.key) or {}
    bs = (rec.get("species_data") or {}).get("bs") or (calc.blob()["poks"].get(rec.get("species") or mon.species)
                                                       or {}).get("bs") or {}
    return bs.get(stat) or 1


def beat_up_damage(b, att, member, dfn, mv, crit, roll):
    """One member's Beat Up hit (BtlCmd_BeatUp): its species' base Attack
    times the move's power times its level's factor (level times 2 over
    5, plus 2), over the target's species' base Defense, over 50, plus 2,
    in whole numbers; a critical hit's multiplier (ApplyCriticalMul: 3/2,
    a Sniper user's 9/4); then the damage roll, roll 0 to 15 for 85 to 100
    percent (BattleSystem_CalcDamageVariance), at least 1. It skips the
    damage routine and the type chart (SYSCTL_IGNORE_IMMUNITIES), so no
    same-type bonus, type, stage, item or ability reaches it."""
    dmg = (base_stat(b, member, "at") * mv.power * (member.level * 2 // 5 + 2)
           // base_stat(b, dfn, "df") // 50 + 2)
    if crit:
        dmg = dmg * 9 // 4 if att.ability == "Sniper" else dmg * 3 // 2
    if att.helped:
        dmg = dmg * 15 // 10     # its partner's Helping Hand, before the roll (helping_hand)
    return max(1, dmg * (85 + roll) // 100)


def beat_up_hits(b, att, mv, dfn, first, crits_of, roll_of, chance, pick):
    """Beat Up (effect script 154, BtlCmd_BeatUp): one hit for each member
    beat_up_party gives, in party order, each with its own critical hit
    (CalcCrit runs again each hit: crits_of(hits, rate)) and damage roll
    (roll_of(i, crit)), landed hit by hit as a move of several hits is
    (land_hits): a Substitute takes them, Sturdy and a Focus Sash hold
    the first at full HP, and the loop stops once a Pokemon faints. It
    meets no type chart, so a Ghost type is hit, Wonder Guard does
    nothing and no resist Berry halves it. The HP taken from dfn. Until
    2026-10-20 it was one hit from its user's row (Ian approved the fix)."""
    members = beat_up_party(b, att)
    crits = crits_of(len(members), crit_rate(b, att, dfn, mv))

    def hit_damage(i, crit):
        return beat_up_damage(b, att, members[i], dfn, mv, crit, roll_of(i, crit))

    b.hits_landed = True
    dealt = land_hits(b, att, dfn, mv, first, len(members), hit_damage, crits, chance, pick)
    b.last_dealt = dealt
    return dealt


def _after_attack(b, att, mv, dfn, first, dealt):
    """A damaging move's own effects once its hits have landed, dealt the
    HP they took from dfn: recoil, draining, the Life Orb and the added
    effects (a move of several hits rolls its own hit by hit in land_hits,
    and has none here)."""
    e = mv.effect
    if e in BREAKS_PROTECT:
        dfn.protecting = False
    if e in RECOIL and att.ability not in RECOIL_PROOF:
        hurt(b, att, max(1, int(dealt * RECOIL[e])))
    if e in ANY_HIT:
        any_hit(b, att, dfn, mv)         # Chloroblast's cost, Freezy Frost's reset, screens, hazards (any_hit)
    # Draining (subscript_drain_half_damage_dealt, _three_quarters): Heal Block
    # on the user stops the heal, not the damage, and Liquid Ooze turns it
    # into damage (drain).
    if e in DRAIN:
        drain(b, att, dfn, int(dealt * DRAIN[e]))
    if e == "RECHARGE_AFTER":
        att.recharge = True
    if e in SELF_KO or e == "FINAL_GAMBIT":
        att.hp = 0
    if e == "CONTINUE_AND_CONFUSE_SELF":
        if att.lock is None:
            att.lock = (mv, b.rng.randint(2, 3))
    if att.item == "Life Orb" and dealt and att.ability != "Magic Guard" and not sheer_force_active(att, mv):
        hurt(b, att, att.maxhp // 10)
    if e == "REMOVE_SCREENS":
        side = b.p if dfn.side == "p" else b.b
        side.screens = dict.fromkeys(side.screens, 0)
        if side.aurora_veil:
            side.aurora_veil = 0         # BtlCmd_TryBreakScreens breaks Aurora Veil too
    stripped = sheer_force_strips(att, mv)
    if e in HIT_SELF_STAGES and not (stripped and not HIT_SELF_STAGES[e][1]):
        ch, certain = HIT_SELF_STAGES[e]
        if certain or b.rng.random() * 100 < self_raise_chance(att, mv):
            change_stages(att, ch)
    if e in ("REMOVE_HAZARDS_AND_BINDING", "MORTAL_SPIN"):
        spin(b, att, dfn, e)
    if e == "CURE_PARTY_STATUS_HIT":
        sparkly_swirl(b, att)            # after any hit, a Substitute's or a knockout's too (sparkly_swirl)
    if e in LOSES_TYPE:
        lose_type(att, LOSES_TYPE[e])    # Burn Up and Double Shock: after the hit, a Substitute's too
    if e == "SWITCH_HIT":
        # U-turn, Volt Switch and Flip Turn switch their user out after any
        # hit, a knockout or a hit on a Substitute too (effect script 228's
        # subscript_attack_then_switch_out runs ON_HIT); the turn does it.
        att.u_turn = True
    if e == "STEAL_HELD_ITEM" and dealt > 0:
        steal_item(att, dfn)             # a knockout too (MOVE_SIDE_EFFECT_CHECK_SUBSTITUTE)
        mark_unheld(b, dfn)              # a trainer's stolen item gone from its rows (item twin)
    if e in LATE_HIT:
        late_hit(b, att, dfn, mv, stripped, dealt)     # Fell Stinger's knockout, Anchor Shot's trap (late_hit)
    # A hit on a Substitute, even the one that broke it, sets off nothing in
    # the Pokemon behind it: the added effects ask CheckSubstitute or
    # Battler_SubstituteWasHit, which read SELF_TURN_FLAG_SUBSTITUTE_HIT for
    # the rest of the move (b.sub_hit). Until 2026-10-15 the hit that broke
    # one gave its added effect to the Pokemon behind it (Ian approved the
    # fix).
    if not dfn.alive() or b.sub_hit or sub_blocks(att, dfn, mv):
        return
    if e == "PREVENT_ESCAPE_BOTH_HIT":
        jaw_lock(att, dfn)           # both held, each by the other (jaw_lock)
    if e == "LEECH_SEED_HIT":
        sappy_seed(dfn)              # a target left standing, no Substitute in the way (sappy_seed)
    if e == "CLEAR_SMOG":
        clear_smog(dfn)              # every stage of a target the hit itself reached back to 0
    if e == "INCINERATE":
        incinerate(b, dfn, mv)       # a Berry the target holds is burned up (incinerate)
    if e == "DOUBLE_POWER_HEAL_SLEEP":
        slap_wakes(dfn, mv)          # Wake-Up Slap's doubled hit wakes its target (slap_wakes)
    if e == "DOUBLE_POWER_AND_CURE_PARALYSIS":
        salts_cure(dfn, mv)          # Smelling Salts' doubled hit cures its target (salts_cure)
    if e == "FLING" and b.flung:
        fling_effect(b, att, dfn, mv, b.flung, first, lambda kind, n: b.rng.randrange(n))
    if e == "THROAT_CHOP":
        throat_chop(att, dfn, stripped)
    if e == "SMACK_DOWN":
        smack_down(b, att, dfn)
    if e == "SALT_CURE":
        # subscript_salt_cure: the target is salted once the hit lands,
        # until it leaves the field; a chance-free effect, so Shield Dust
        # and Sheer Force (sSheerForceEffects) leave it alone.
        dfn.salted = True
    if e == "CORE_ENFORCER" and getattr(dfn, "acted_turn", None) == b.turn:
        # Core Enforcer (effect script 413, subscript_core_enforcer): once
        # the hit is in, a standing target with no Substitute that has moved
        # this turn loses its ability until it leaves, as Gastro Acid takes
        # it (suppress). Until 2026-10-14 it was a plain hit (Ian approved
        # the fix).
        suppress(b, dfn)
    if e == "DECREASE_LAST_MOVE_PP_HIT" and dealt > 0:
        # Eerie Spell (effect script 421, subscript_reduce_target_pp_hit,
        # Oxide's engine since 2026-10-14): once its hit has landed on the
        # target itself, not on a Substitute, the target's last move loses 3
        # PP by Spite's own command. A chance-free effect, so Shield Dust, a
        # Covert Cloak and Sheer Force leave it alone.
        spite(dfn, 3)
    chance = mv.chance or 0
    if (dfn.ability == "Shield Dust" and not mold(att, dfn)) or stripped:
        chance = 0               # Shield Dust, unless Mold Breaker gets past it
    if att.ability == "Serene Grace":
        chance *= 2
    if e in HIT_STATUS and b.rng.random() * 100 < chance:
        give_status_by_move(b, att, dfn, mv, HIT_STATUS[e])
    if e in STATUS_PICK and b.rng.random() * 100 < chance:
        give_status_by_move(b, att, dfn, mv, b.rng.choice(STATUS_PICK[e]))     # Dire Claw's pick of three
    if e == "BURN_HIT_IF_STATS_ROSE" and getattr(dfn, "stat_raised", False) and b.rng.random() * 100 < chance:
        give_status_by_move(b, att, dfn, mv, "brn")
    if e == "TRI_ATTACK" and b.rng.random() * 100 < chance:
        give_status_by_move(b, att, dfn, mv, b.rng.choice(["brn", "par", "frz"]))
    if e == "SECRET_POWER" and b.rng.random() * 100 < chance:
        what = secret_power_effect(b.st.get("terrain"))     # its terrain's stage, status or flinch
        if isinstance(what, dict):
            lower_stats(b, att, dfn, what)
        elif what == "flinch":
            dfn.flinch = dfn.flinch or first
        else:
            give_status_by_move(b, att, dfn, mv, what)
    if e in FLINCH_HIT and first and b.rng.random() * 100 < chance:
        dfn.flinch = True
    if e == "ALWAYS_FLINCH_FIRST_TURN_ONLY" and first and not stripped:
        dfn.flinch = True
    if dfn.ability == "Inner Focus" and not mold(att, dfn):
        dfn.flinch = False       # Inner Focus: it never flinches, unless Mold Breaker gets past it
    if e in CONFUSE_HITS and b.rng.random() * 100 < chance \
            and not confusion_blocked(b, att, dfn, hit=True):
        dfn.confused = b.rng.randint(2, 5)
        confusion_berry(dfn, b)
    if e == "CHATTER" and chatter_confuses(att, dfn, stripped) and b.rng.random() < CHATTER_ODDS \
            and not confusion_blocked(b, att, dfn, hit=True):
        dfn.confused = b.rng.randint(2, 5)
        confusion_berry(dfn, b)
    if e in HIT_FOE_STAGES and b.rng.random() * 100 < chance:
        lower_stats(b, att, dfn, HIT_FOE_STAGES[e])
    if e == "HIT_AND_PREVENT_HEALING" and not stripped:     # Psychic Noise; Shield Dust does not stop it
        start_heal_block(att, dfn, mv)
    if e in ("BIND_HIT", "WHIRLPOOL") and not dfn.bound:
        dfn.bound, dfn.bound_by = 6 if att.item == "Grip Claw" else b.rng.randint(3, 6), att.key


# The moves Sleep Talk never calls (Gen 4's list, by effect).
SLEEP_TALK_SKIPS = {"USE_RANDOM_LEARNED_MOVE_SLEEP", "HIT_LAST_WHIFF_IF_HIT", "BIDE", "UPROAR", "COPY_MOVE",
                    "CALL_RANDOM_MOVE", "USE_MOVE_FIRST", "USE_LAST_USED_MOVE", "MIMIC", "SKETCH"}


def sleep_talk_pick(b, att):
    """Sleep Talk: one of its user's other moves at random, never a move
    that needs a charge turn or one on Gen 4's list; with no dice (the strict
    search) the first such move. None when there is none. A battle playing
    with dice picks through them, as every other chance in its turn does:
    the play-outs replay a turn's chances by script, and a pick from the
    battle's own generator differed between replays (it broke Kaizo
    Fantina's labels, whose Spiritomb sleeps and talks)."""
    picks = [m for m in att.moves if m.effect not in SLEEP_TALK_SKIPS and m.effect not in TWO_TURN
             and not disabled_out(att, m)]
    if not picks:
        return None
    dice = getattr(b, "dice", None)
    if dice is not None:
        return picks[dice.choice("sleeptalk", len(picks))]
    rng = getattr(b, "rng", None)
    return rng.choice(picks) if rng is not None else picks[0]


def ghost_curse(b, att, dfn, mv):
    """A Ghost type's Curse (effect script 109, subscript_curse_ghost): it
    fails, costing nothing, on a target with no HP, out of reach in the air
    or underground, behind a Substitute (an Infiltrator's Curse passes it),
    or already cursed; else its user cuts half its maximum HP and curses the
    target, which loses a quarter of its own at each turn's end. Until
    2026-10-14 it cut the HP and cursed in every case (Ian approved the
    fix). Whether it took."""
    if not dfn.alive() or dfn.cursed or sub_blocks(att, dfn, mv) \
            or (dfn.charging is not None and dfn.charging.effect in INVULNERABLE):
        return False
    hurt(b, att, att.maxhp // 2)
    dfn.cursed = True
    return True


# The abilities that keep their own holder from Rest (subscript_rest); Sweet
# Veil keeps its partner awake too, and Leaf Guard only in sun.
REST_PROOF = frozenset({"Insomnia", "Vital Spirit", "Purifying Salt", "Sweet Veil"})


def rest_blocked(b, att):
    """Whether subscript_rest keeps att awake before anything else is
    checked: Insomnia, Vital Spirit or Oxide's Purifying Salt; a Sweet Veil
    of its own or, in a double battle, its partner's; or Leaf Guard in sun
    that Cloud Nine and Air Lock leave alone (CheckIgnoreWeather). The
    message names the ability ("stayed awake because of its"). Until
    2026-10-14 only full HP and sleep stopped Rest (Ian approved the fix)."""
    holder = att if att.ability in REST_PROOF else None
    if holder is None and getattr(b, "doubles", False):
        ally = ally_of(b, att)
        holder = ally if ally is not None and ally.ability == "Sweet Veil" else None
    if holder is None and att.ability == "Leaf Guard" and b.weather == "Sun" and not weather_ignored(b):
        holder = att
    if holder is None:
        return False
    reveal(holder)
    return True


def taunt_blocked(att, dfn):
    """Whether Oblivious keeps Taunt off dfn (subscript_taunt_start's
    CheckIgnorableAbility, Generation 6's rule), unless att has Mold
    Breaker; the message names the ability. Until 2026-10-14 an Oblivious
    target was taunted (Ian approved the fix)."""
    if dfn.ability == "Oblivious" and not mold(att, dfn):
        reveal(dfn)
        return True
    return False


def throat_chopped(mon, mv):
    """Whether Throat Chop's hold keeps mon from this move: a sound move of
    the engine's sSoundMoves or sSelfAimedSoundMoves (fightai.SOUND_MOVES)
    while its count runs (Move_ThroatChopped)."""
    return bool(mon.throat_chop) and mv.const in fightai.SOUND_MOVES


def move_barred(b, mon, mv):
    """Whether a move of this batch's holds can be neither chosen
    (BattleSystem_CheckInvalidMoves, which the player's menu and the
    trainer's AI both read) nor used (the status checks before a move):
    a sound move under Throat Chop, and an airborne move under Gravity
    (Move_FailsInHighGravity's list, fightai.GRAVITY_FAILS)."""
    return throat_chopped(mon, mv) or (bool(getattr(b, "gravity", 0)) and mv.const in fightai.GRAVITY_FAILS)


def throat_chop(att, dfn, stripped):
    """Throat Chop's hit (effect script 401, subscript_throat_chop, ON_HIT):
    once it has landed on a target left standing, with no Substitute in the
    way, no Shield Dust (Mold Breaker gets past it) and no Covert Cloak, the
    target's count starts at 2, unless one is running; Sheer Force strips
    it (sSheerForceEffects). Until 2026-10-15 the hit set nothing, so the
    target kept its sound moves (Ian approved the fix)."""
    if stripped or dfn.throat_chop or dfn.item == "Covert Cloak":
        return
    if dfn.ability == "Shield Dust" and not mold(att, dfn):
        return
    dfn.throat_chop, dfn.rare = 2, True


def majesty_blocked(att, dfn, mv):
    """A move of raised priority (move_priority: Prankster's and Gale Wings'
    raises count) aimed at a foe with Queenly Majesty fails, unless a Mold
    Breaker gets past it (BattleControllerPlayer_PriorityBlock, after the
    immunity abilities; in a double battle the holder's partner is shielded
    too, majesty_partner_blocked). The message names the ability. Until
    2026-10-20 the move landed (Ian approved the fix)."""
    if dfn is att or dfn.side == att.side or mold(att, dfn) or move_priority(att, mv) <= 0:
        return False
    reveal(dfn)
    return True


def majesty_partner_blocked(b, att, dfn, mv):
    """Queenly Majesty on the target's standing partner, in a double battle
    (BattleControllerPlayer_PriorityBlock, after the target's own): a move
    of raised priority aimed at a foe fails if that foe's partner has it,
    unless a Mold Breaker gets past it; the message names the ability.
    Until 2026-10-21 only the target's own shielded it (Ian approved the
    double-battle part batch 11 left on 2026-10-14)."""
    if dfn is att or dfn.side == att.side or move_priority(att, mv) <= 0:
        return False
    ally = ally_of(b, dfn)
    if ally is None or ally.ability != "Queenly Majesty" or mold(att, ally):
        return False
    reveal(ally)
    return True


def prankster_blocked(att, dfn, mv):
    """A status move Prankster raised, aimed at a Dark-type foe, fails
    (BattleControllerPlayer_PriorityBlock, after the immunity abilities),
    unless it aims at the foe's side (Spikes and the like); the AI's
    Basic_CheckPrankster already kept such moves from being chosen. Until
    2026-10-20 the move landed (Ian approved the fix)."""
    return (dfn is not att and dfn.side != att.side and mv.cat == "Status" and mv.range != "OPPONENT_SIDE"
            and move_priority(att, mv) > mv.pri and "Dark" in dfn.types)


def soundproofed(att, dfn, mv):
    """Whether Soundproof stops att's sound move at dfn
    (BattleSystem_TriggerImmunityAbility over sSoundMoves, which
    fightai.BASIC_SOUND copies; Mold Breaker gets past it); the message
    names the ability. The calculator's rows already stop the damaging ones;
    this is for the status ones (Growl, Roar, Sing, Supersonic, Screech,
    Metal Sound, Grass Whistle, Confide, Noble Roar and Parting Shot), which
    went through until 2026-10-14 (Ian approved the fix)."""
    if (att is not dfn and mv.const in fightai.BASIC_SOUND and dfn.ability == "Soundproof"
            and not mold(att, dfn)):
        reveal(dfn)
        return True
    return False


def anchored(att, dfn):
    """Whether Suction Cups keeps dfn in against Roar or Whirlwind
    (subscript_force_target_to_switch_or_flee's CheckIgnorableAbility, so a
    Mold Breaker user gets past it); the message names the ability. Until
    2026-10-14 Roar dragged it out (Ian approved the fix)."""
    if dfn.ability == "Suction Cups" and not mold(att, dfn):
        reveal(dfn)
        return True
    return False


def magnet_rise(att):
    """Magnet Rise (effect script 252): five turns in which Ground moves fail
    on its user, counted down at each turn's end and cleared by a switch. It
    fails while one is running, on a Levitate user, on one rooted by
    Ingrain, and on one Smack Down brought down (Oxide's effect script 252;
    the mark is kept since 2026-10-15)."""
    if not att.magnet_rise and att.ability != "Levitate" and not att.ingrained and not att.smacked:
        att.magnet_rise = 5


def tormented_out(mon, mv):
    """Whether Torment rules this move out: a tormented Pokemon cannot pick
    the move it used last (BattleSystem_CheckInvalidMoves'
    CHECK_INVALID_TORMENTED), which a switch or a turn it could not act
    clears."""
    return mon.tormented and mon.last is not None and mon.last.name == mv.name


def disabled_out(mon, mv):
    """Whether Disable or a foe's Imprison rules this move out: it cannot be
    chosen (BattleSystem_CheckInvalidMoves' CHECK_INVALID_DISABLED and
    CHECK_INVALID_IMPRISONED), Sleep Talk cannot call it (BtlCmd_TrySleepTalk
    asks every check but PP), and it fails if it was chosen before the
    Disable or the Imprison came (CHECK_STATUS_STATE_DISABLE and
    CHECK_STATUS_STATE_IMPRISON, both before confusion, both letting go of a
    Choice item's lock)."""
    return (mon.disabled is not None and mv.name == mon.disabled) or mv.name in mon.sealed


def imprison(b, att):
    """Imprison (effect script 192, BtlCmd_TryImprison): the foes on the
    field are marked as tried (imprisoned) whatever happens; the move then
    fails if its user imprisons already or shares no move with a foe on the
    field. Otherwise, until the user leaves, every foe on the field, and
    each that comes in while it stays, cannot choose or use a move the user
    knows (sealed, read by disabled_out). Until 2026-10-15 it did nothing
    (Ian approved the fix)."""
    foes = (b.b if att.side == "p" else b.p).on_field()
    for f in foes:
        f.imprisoned = True
    mine = frozenset(m.name for m in att.moves)
    if att.imprisoning or not any(m.name in mine for f in foes for m in f.moves):
        return
    att.imprisoning = True
    for f in foes:
        f.sealed = f.sealed | mine


def seal_newcomer(b, side, new):
    """A Pokemon coming in while a foe imprisons is sealed out of that foe's
    moves (Move_Imprisoned reads the imprisoner's moves, whoever faces it)."""
    for f in (b.b if side is b.p else b.p).on_field():
        if f.imprisoning:
            new.sealed = new.sealed | frozenset(m.name for m in f.moves)


def disable(dfn, turns):
    """Disable (effect script 86, BtlCmd_TryDisable): the target's last move
    is disabled for the count turns() gives (3 to 6, Random % 4 + 3), drawn
    only when it takes. It fails while one of the target's moves is disabled,
    before the target has used a move, when that move is not one it knows,
    and when it has no PP left; a Substitute does not stop it. Whether it
    took."""
    last = dfn.last
    if dfn.disabled is not None or last is None or not any(m.name == last.name for m in dfn.moves) \
            or dfn.pp.get(last.name, 0) <= 0:
        return False
    dfn.disabled, dfn.disabled_turns = last.name, turns()
    return True


# The moves Encore cannot lock a Pokemon into (sCannotEncoreMoves, matched by
# effect): Transform, Mimic, Sketch, Mirror Move, Encore and Struggle.
NO_ENCORE = frozenset({"TRANSFORM", "COPY_MOVE_FOR_BATTLE", "LEARN_MOVE_PERMANENT", "COPY_MOVE", "ENCORE",
                       "STRUGGLE"})


def encore(dfn, turns):
    """Encore (effect script 90, BtlCmd_TryEncore): the target is locked into
    its last move for the count turns() gives (3 to 7, Random % 5 + 3),
    drawn only when it takes. It fails while the target is under one, before
    it has used a move, and when that move is not one it knows, is one
    Encore cannot lock or has no PP left; a Substitute does not stop it.
    Whether it took."""
    last = dfn.last
    if dfn.encore is not None or last is None or last.effect in NO_ENCORE \
            or not any(m.name == last.name for m in dfn.moves) or dfn.pp.get(last.name, 0) <= 0:
        return False
    dfn.encore, dfn.encore_turns = last.name, turns()
    return True


def encored_move(mon, mv):
    """The move an encored Pokemon uses whatever it chose
    (BattleControllerPlayer_FightCommand takes the Encore move first, so one
    encored after it chose this turn uses the Encore move too); mv itself
    otherwise, and for Struggle, which comes first."""
    if mon.encore is None or mv.name == mon.encore or mv.effect == "STRUGGLE":
        return mv
    return next((m for m in mon.moves if m.name == mon.encore), mv)


def nightmare(att, dfn, mv):
    """Nightmare (effect script 107, subscript_nightmare_start): only on a
    sleeping target that is not in one already and has no Substitute in the
    way (an Infiltrator's passes)."""
    if dfn.status == "slp" and not dfn.nightmare and not sub_blocks(att, dfn, mv):
        dfn.nightmare = True


# The stats Acupressure may raise, in BtlCmd_BoostRandomStatBy2's order
# (BATTLE_STAT_ATTACK to BATTLE_STAT_EVASION).
ACUPRESSURE_STATS = ("atk", "def", "spe", "spa", "spd", "acc", "eva")


def acupressure(att, pick):
    """Acupressure (effect script 226, BtlCmd_BoostRandomStatBy2) on its user,
    the one target its range allows in a single battle: it fails behind
    the user's own Substitute (the script's CheckSubstitute on its
    target), and otherwise raises by two stages one of the stats not at
    +6 yet, drawn evenly (pick(n) on the battle's dice), failing when all
    seven are there; Simple doubles the two, as for any raise. Until
    2026-10-15 nothing rose (Ian approved the fix)."""
    if att.sub:
        return
    room = [k for k in ACUPRESSURE_STATS if att.stages[k] < 6]
    if room:
        change_stages(att, {room[pick(len(room)) if len(room) > 1 else 0]: 2})


def coat_bounces(b, att, mv, dfn):
    """Magic Coat (effect script 183, TrySetMagicCoat, and
    BattleControllerPlayer_MoveStolen before the move's own checks): a move
    with MOVE_FLAG_CAN_MAGIC_COAT aimed at a foe that used Magic Coat this
    turn is turned back on its user, once, the flag spent; the move turned
    back is not turned again. A move whose defender is its own user, or
    that aims at its own side or the field, is not aimed at the coat.
    Whether this move is turned back. Until 2026-10-15 Magic Coat did
    nothing (Ian approved the fix)."""
    if (not mv.reflectable or b.reflecting or dfn is att or dfn.side == att.side or not dfn.alive()
            or mv.range in OWN_RANGES or mv.range in ("USER_SIDE", "FIELD", "ALLY", "USER_OR_ALLY")):
        return False
    dfn.magic_coat = False
    return True


def bounces(b, att, mv, dfn):
    """Whether a move is turned back on its user (BattleControllerPlayer_MoveStolen):
    by Magic Coat used this turn (coat_bounces), or else by Magic Bounce,
    every turn and with no move, unless a Mold Breaker gets past it or its
    holder is out of reach in the air or underground; the message names
    the ability. Pressure on the bounce is not followed. Until 2026-10-20
    Magic Bounce did nothing (Ian approved the fix)."""
    coat = dfn.magic_coat
    if not coat and (mold(att, dfn) or (dfn.charging is not None and dfn.charging.effect in INVULNERABLE)):
        return False
    if not coat_bounces(b, att, mv, dfn):
        return False
    if not coat:
        reveal(dfn)                      # Magic Bounce's own message
    return True


def teeter_dance_others(b, att, mv, dfn, first):
    """Teeter Dance (effect script 199, the confusion subscript on each
    target) in a double battle, where its range (ALL_ADJACENT) reaches every
    other Pokemon on the field, the user's ally too: status_move confuses
    the target it was given, and this the rest, each through its own
    Protect, hidden turn and accuracy check, a Substitute, Own Tempo,
    Safeguard and a confusion already there, as the engine's spread loop
    runs the move on each in turn. In a single battle its one target is the
    foe. Until 2026-10-15 Teeter Dance confused nobody (Ian approved the
    fix)."""
    if not getattr(b, "doubles", False):
        return
    ally = ally_of(b, att)
    for m in foes_of(b, att) + ([ally] if ally else []):
        if m is dfn or not m.alive():
            continue
        if protected(b, att, mv, m) or status_out_of_reach(att, m, mv) or not b.accuracy_hits(att, m, mv, first):
            continue
        if not sub_blocks(att, m, mv) and not confusion_blocked(b, att, m):
            m.confused = b.rng.randint(2, 5)
            confusion_berry(m, b)


def water_sport(att):
    """Water Sport (effect script 210): its user is marked
    (MOVE_EFFECT_WATER_SPORT) until it leaves, failing when it is already;
    while any Pokemon on the field has the mark, every Fire move's power
    is halved (sport_half). Until 2026-10-15 it did nothing (Ian approved
    the fix)."""
    if not att.water_sport:
        att.water_sport = att.rare = True


def mud_sport(att):
    """Mud Sport (effect script 201): its user is marked
    (MOVE_EFFECT_MUD_SPORT) until it leaves, failing when it is already;
    while any Pokemon on the field has the mark, every Electric move's power
    is halved (sport_half). Until 2026-10-15 it did nothing (Ian approved
    the fix)."""
    if not att.mud_sport:
        att.mud_sport = att.rare = True


def sport_half(b, att, dfn, mv):
    """The factor Water Sport puts on a Fire move, and Mud Sport on an
    Electric one (BattleSystem_CalcMoveDamage: the power halved, in whole
    numbers, after Technician, while BattleSystem_AnyBattlersWithMoveEffect
    finds the mark on any battler: in a single battle the two Pokemon on the
    field are the hit's own); the trainer's AI's figure meets it too, as the
    engine's estimate runs the same routine. Looked at only in a fight where
    a Pokemon knows one of the moves (Battle.sporty)."""
    kind = move_type_used(att.ability, mv, att.ivs, att.item, weather_now(b))
    if kind == "Fire":
        mark = "water_sport"
    elif kind == "Electric":
        mark = "mud_sport"
    else:
        return 1.0
    if getattr(b, "doubles", False):
        on = any(getattr(m, mark) and m.alive() for m in b.p.on_field() + b.b.on_field())
    else:
        on = (getattr(att, mark) and att.alive()) or (getattr(dfn, mark) and dfn.alive())
    if not on:
        return 1.0
    p = technician(att, mv.power) if mv.power > 1 else 2
    return (p // 2) / p


def swap_stages(att, dfn, stats):
    """Guard Swap and Power Swap (effect scripts 244 and 243,
    subscript_exchange_def_and_spdef_stages and
    subscript_exchange_atk_and_spatk_stages): the user's and the target's
    stages of the two stats change places, a Substitute in the way or not,
    as the subscripts have no Substitute check. Until 2026-10-15 no stage
    moved (Ian approved the fix)."""
    for k in stats:
        att.stages[k], dfn.stages[k] = dfn.stages[k], att.stages[k]


def snatch(b, att, first):
    """Snatch (effect script 195, TrySnatch): it fails when no battler acts
    after its user this turn (moves_last); otherwise its user waits for the
    rest of the turn to take the next move Snatch may take (snatched)."""
    if not moves_last(b, first):
        att.snatching = b.snatching = True


def snatched(b, att, mv):
    """The Pokemon that takes att's status move mv, one Snatch may take
    (MOVE_FLAG_CAN_SNATCH), or None (BattleControllerPlayer_MoveStolen): the
    first Pokemon on the field in speed order that waits with Snatch, whose
    wait it ends. It then uses the move as its own, aimed at att, att having
    paid for it (subscript_snatch), and pays one PP more of its Snatch when
    att has Pressure (BattleSystem_DecPPForPressure). Until 2026-10-15
    Snatch did nothing (Ian approved the fix)."""
    waiting = sorted((m for m in b.p.on_field() + b.b.on_field() if m is not att and m.snatching),
                     key=lambda m: -b.speed(m))
    if not waiting:
        return None
    thief = waiting[0]
    thief.snatching = False
    if att.ability == "Pressure" and thief.pp.get("Snatch", 0) > 0:
        thief.pp["Snatch"] -= 1
    return thief


def teatime(b, pick):
    """Teatime (effect script 412, subscript_teatime, TryTeatime): it fails
    when no Pokemon on the field holds a Berry; otherwise each one that
    does, in speed order, eats its own Berry at once, whether or not it
    would set itself off, as Pluck eats one (BattleSystem_PluckBerry with
    the eater standing as the attacker), a Berry with nothing to give being
    eaten all the same. The Berry is its holder's own for Belch and Recycle
    (consume), and it is read past Embargo and Magic Room, which the command
    does not ask (raw_item_op). Until 2026-10-15 Teatime did nothing (Ian
    approved the fix)."""
    eaters = [m for m in b.p.on_field() + b.b.on_field()
              if m.alive() and (m.item or m.item_off or "").endswith("Berry")]
    for m in sorted(eaters, key=lambda m: -b.speed(m)):
        def eat(m=m):
            berry = m.item
            consume(m)
            eat_berry(m, berry, pick)
        if m.item_off is not None:
            raw_item_op((m,), eat)
        else:
            eat()


def aurora_veil(b, att):
    """Aurora Veil (effect script 377, subscript_aurora_veil, TryAuroraVeil):
    it fails with the veil up on its user's side already, or unless the
    weather is hail that no Cloud Nine or Air Lock voids; otherwise the side
    is veiled for five turns, eight with a Light Clay, and while it lasts
    physical and special hits on the side are halved, once with Reflect or
    Light Screen (BattleSystem_CalcMoveDamage), a critical hit, Brick
    Break's kind and an Infiltrator passing it. It runs down after Light
    Screen, and Brick Break's kind and Defog clear it. Until 2026-10-15 it
    did nothing (Ian approved the fix)."""
    side = b.p if att.side == "p" else b.b
    if side.aurora_veil or b.weather != "Hail" or weather_ignored(b):
        return
    side.aurora_veil = 8 if att.item == "Light Clay" else 5


def octolock(att, dfn, mv):
    """Octolock (effect script 410, subscript_octolock), once Protect and
    the accuracy check have let it through: it fails on a target already
    octolocked or behind a Substitute an Infiltrator does not pass;
    otherwise the target is held as Mean Look holds it, by its user until
    the user leaves (trapped_by, so a Ghost type may still switch), and
    marked, so it loses a stage of Defense and one of Sp. Def at each
    turn's end (octolock_turn). A Baton Pass hands both on, from either
    side (baton_state, switch_in). Until 2026-10-15 it did nothing (Ian
    approved the fix)."""
    if dfn.octolocked or sub_blocks(att, dfn, mv):
        return
    dfn.trapped_by = att.key
    dfn.octolocked = dfn.rare = True


def octolock_turn(b, side, m):
    """An octolocked Pokemon's turn's end (MON_COND_CHECK_STATE_OCTOLOCK,
    after binding, subscript_octolock_turn): a stage of Defense and then
    one of Sp. Def lost, its Octolock user standing as the attacker, so the
    blockers, Mist, Simple, Defiant and Mirror Armor act as on a move's
    drops (lower_stats)."""
    foes = b.b if side is b.p else b.p
    src = next((f for f in foes.on_field() if f.key == m.trapped_by), None)
    lower_stats(b, src, m, {"def": -1, "spd": -1})


def heal_pulse(att, dfn, mv):
    """Heal Pulse (effect script 379, subscript_heal_pulse): it fails on a
    target under Heal Block or behind a Substitute an Infiltrator does not
    pass; otherwise the target gets back half its maximum HP, rounded up,
    or three quarters with its user's Mega Launcher, nothing at full HP
    (subscript_recover_hp). In a single battle its target is the foe; in a
    double battle the one it is aimed at, an ally too (run_doubles). Until
    2026-10-15 it did nothing (Ian approved the fix)."""
    if dfn.heal_block or sub_blocks(att, dfn, mv):
        return
    heal(dfn, 3 * ((dfn.maxhp + 3) // 4) if att.ability == "Mega Launcher" else (dfn.maxhp + 1) // 2)


def heart_swap(att, dfn):
    """Heart Swap (effect script 250, subscript_exchange_all_stat_stages):
    the user and its target exchange all seven stat stages, accuracy and
    evasion with them, and each takes the other's Focus Energy
    (VOLATILE_CONDITION_FOCUS_ENERGY, crit_stage here), a Substitute in the
    way or not, as the subscript has no Substitute check. Until 2026-10-15
    no stage moved (Ian approved the fix)."""
    swap_stages(att, dfn, STAGE_KEYS)
    att.crit_stage, dfn.crit_stage = dfn.crit_stage, att.crit_stage


def psycho_shift(b, att, dfn, mv):
    """Psycho Shift (effect script 234, CheckCanShareStatus and
    subscript_give_target_own_status): it fails when its user has no
    status, the target has one, or a Substitute an Infiltrator does not
    pass is in the way; otherwise it gives the target the user's sleep,
    poison, burn, paralysis or bad poison through the status's own
    subscript, which its types, abilities and Safeguard may refuse
    (give_status_by_move, a fresh sleep count or toxic count), and only
    once the target has it is the user cured. Until 2026-10-15 the status
    stayed with the user (Ian approved the fix)."""
    if not att.status or dfn.status or sub_blocks(att, dfn, mv):
        return
    if give_status_by_move(b, att, dfn, mv, att.status):
        att.status, att.sleep, att.toxic = None, 0, 0


def memento_faints(att, dfn):
    """Memento (effect script 168): with a target to aim at, its user
    faints as the script starts (BATTLEMON_CUR_HP set to 0), before the
    accuracy check or the target's Protect, so a miss or a Protect still
    costs it; with none (BattleControllerPlayer_HasNoTarget, before the
    script) nothing happens. Whether the user fainted. Until 2026-10-15 a
    miss, a Protect or a target on its hidden turn spared it, and a
    Memento with no target fainted it (Ian approved the fix)."""
    if not dfn.alive():
        return False
    att.hp = 0
    return True


def memento_drops(b, att, dfn, mv):
    """Memento's drops once it lands (subscript_memento): none through a
    Substitute; otherwise Attack and Sp. Atk two stages each through the
    stat-down subscript, which Clear Body, White Smoke, Hyper Cutter and
    Mist meet as any drop does (lower_stats). Until 2026-10-15 both drops
    passed a Substitute and every blocker (Ian approved the fix)."""
    if not sub_blocks(att, dfn, mv):
        lower_stats(b, att, dfn, {"atk": -2, "spa": -2})


def transform(b, att, dfn):
    """Transform (effect script 57, subscript_transform_into_target,
    BtlCmd_Transform): it fails on a target that is hidden on a two-turn
    move's turn or transformed already; otherwise its user becomes a copy of
    the target in all but HP, level, status and item: its moves with 5 PP
    each (fewer for a move that has fewer), its stat stages, types and
    ability (Oxide's copy runs through the ability), and its Attack,
    Defense, Speed, Sp. Atk and Sp. Def; its Disable and Last Resort count
    clear. The battle reads the copy's types and ability (set_types,
    set_ability) and its Speed, and its hits read the copied Pokemon's rows
    where prepare() has them against the target (in a double battle a
    spread move's rows on its own side); every other hit, and every hit
    into it, keeps the user's own rows, as the copy's rows against its own
    side are not made (reported to Ian with their cost). Leaving brings its
    own moves, types and ability back. Until 2026-10-15 Transform did
    nothing (Ian approved the part of the fix that is cheap)."""
    if dfn is att or not dfn.alive() or dfn.transformed or (
            dfn.charging is not None and dfn.charging.effect in INVULNERABLE):
        return
    if att.transformed_from is None:
        att.transformed_from = (att.moves, att.pp)
    att.transformed, att.transform_key, att.rare = True, dfn.key, True
    att.moves = list(dfn.moves)
    att.pp = {m.name: min(5, m.pp) for m in att.moves}
    att.stages = dict(dfn.stages)
    att.disabled, att.disabled_turns, att.last_resort_count = None, 0, 0
    set_types(att, list(dfn.types))
    set_ability(b, att, dfn.ability)


def refresh(att):
    """Refresh (effect script 193, subscript_recover_psn_prz_brn): its user's
    own poison, bad poison, burn or paralysis is cured
    (MON_CONDITION_FACADE_BOOST, the whole status word cleared, the toxic
    count with it), and on sleep, freeze or no status it fails; nobody else
    is touched. Until 2026-10-15 it shared Heal Bell's branch and cured the
    user's whole side, sleep and freeze included (Ian approved the fix)."""
    if att.status in ("psn", "tox", "brn", "par"):
        att.status, att.toxic = None, 0


def consume(mon, eaten=True):
    """A held item used up (BtlCmd_RemoveItem): gone, and kept for Recycle.
    The engine keeps one per battle position, so a Pokemon could recycle
    what the one before it used; here each Pokemon keeps its own. A Berry
    used up is eaten (BattleScript_RecordBerryEaten, for Belch), unless
    Natural Gift or Fling spent it (eaten False)."""
    if eaten and mon.item and mon.item.endswith("Berry"):
        mon.ate_berry = True
    mon.recycle, mon.item = mon.item, None
    if mon.plate_types is not None:
        unplate(mon)             # a player's Arceus that flung its Plate is Normal again


def lock_item(mon):
    """Its held item stops working for now, under Embargo or Magic Room
    (Battler_HeldItem reads none): it waits in item_off and `item` reads
    None, so every item effect stops with it."""
    if mon.item:
        mon.item_off, mon.item = mon.item, None
        mon.rare = True


def unlock_item(mon):
    """Its held item works again, once neither Embargo nor Magic Room holds it."""
    if mon.item_off is not None and not mon.embargo and not mon.roomed:
        mon.item, mon.item_off = mon.item_off, None


def raw_item_op(mons, fn):
    """Run fn, a move that takes, swaps or burns a held item itself, with the
    items Embargo or Magic Room hold back in hand, as those moves read the
    held item past them (BATTLEMON_HELD_ITEM); afterwards an item that
    still does not work waits again."""
    for m in mons:
        if m.item_off is not None:
            m.item, m.item_off = m.item_off, None
    try:
        return fn()
    finally:
        for m in mons:
            if m.embargo or m.roomed:
                lock_item(m)


def embargo(b, att, dfn, mv):
    """Embargo (effect script 232, subscript_embargo_start): it fails on a
    target behind a Substitute, already under Embargo, with Multitype or
    holding a Griseous Orb; otherwise for five turns the target's held item
    does not work (lock_item), counted down at each turn's end
    (MON_COND_CHECK_STATE_EMBARGO). The script also fails when the target's
    Quick Claw or Custap Berry went off this turn, which is not followed.
    The calculator's rows keep a trainer's item's own damage and Speed (a
    Life Orb's, a booster's, a Choice item's, an Assault Vest's), which would
    need item-free twin rows. Until 2026-10-15 the move did nothing (Ian
    approved the fix)."""
    if dfn.embargo or sub_blocks(att, dfn, mv) or dfn.ability == "Multitype" \
            or (dfn.item or dfn.item_off) == "Griseous Orb":
        return
    dfn.embargo, dfn.rare = 5, True
    lock_item(dfn)


def magic_room(b):
    """Magic Room (effect script 411): five turns in which no held item works
    (lock_item on every Pokemon on the field, and on each that comes in),
    counted down after Trick Room at each turn's end
    (SIDE_COND_CHECK_STATE_MAGIC_ROOM); used while one runs, it ends it. The
    calculator's rows keep a trainer's item's own damage and Speed, as for
    Embargo. Until 2026-10-15 the move did nothing (Ian approved the fix)."""
    if b.magic_room:
        magic_room_ends(b)
        return
    b.magic_room = 5
    for m in b.p.on_field() + b.b.on_field():
        m.roomed = m.rare = True
        lock_item(m)


def wonder_room(b):
    """Wonder Room (effect script 407): five turns in which every Pokemon's
    Defense and Sp. Def trade places in the damage (room_mult), counted down
    straight after Trick Room at each turn's end
    (SIDE_COND_CHECK_STATE_WONDER_ROOM); used while one runs, it ends it. A
    boss's permanent room would make it fail, but the engine's list of them
    (sPermanentWonderRoomTrainers) is empty. Until 2026-10-20 the move did
    nothing (Ian approved the fix)."""
    b.wonder_room = 0 if b.wonder_room else 5


def room_mult(att, dfn, mv):
    """Wonder Room's swap on a hit (BattleSystem_CalcMoveDamage under
    FIELD_CONDITION_WONDER_ROOM, which the trainer's AI's estimate reads
    too): only the stats trade, so a physical hit, or Psyshock's kind,
    meets the target's Sp. Def with its Defense stages and modifiers, and a
    special hit its Defense with the Sp. Def ones; Body Press, which hits
    with its user's Defense, takes its user's Sp. Def the same way. The
    rows are made outside the room, so the hit is scaled by the stats'
    ratio, as split_mult scales Guard Split's (stats it averaged read as
    averaged): the damage formula's whole-number steps and its added 2 are
    not followed, so a hit can differ from the engine's by a point or a few
    per cent."""
    d = "def" if mv.cat == "Physical" or mv.const in AGAINST_DEFENSE else "spd"
    other = "spd" if d == "def" else "def"
    mult = max(1, raw_stat(dfn, d)) / max(1, raw_stat(dfn, other))
    if mv.const == "MOVE_BODY_PRESS":
        mult *= max(1, raw_stat(att, "spd")) / max(1, raw_stat(att, "def"))
    return mult


def magic_room_ends(b):
    b.magic_room = 0
    for m in b.p.on_field() + b.b.on_field():
        if m.roomed:
            m.roomed = False
            unlock_item(m)


def knock_off(att, dfn):
    """Knock Off's hit (subscript_knock_off, BtlCmd_TryKnockOff): the
    target's item is gone, and its party slot is marked (knocked_off),
    unless the target has Multitype (its record's, BATTLEMON_ABILITY, so
    gas or Gastro Acid does not hide it) or holds a Griseous Orb, or its
    Sticky Hold keeps the item, which a Mold Breaker attacker gets past,
    the message naming the ability. A Quick Claw or Custap Berry that
    went off this turn also keeps it in the engine (BATTLEMON_QUICK_CLAW,
    BATTLEMON_CUSTAP_BERRY), which is not followed. Until 2026-10-20
    Sticky Hold, Multitype and the Orb kept nothing (Ian approved the
    fix)."""
    if dfn.item_off is not None:
        return raw_item_op((dfn,), lambda: knock_off(att, dfn))
    if not dfn.item or raw_ability(dfn) == "Multitype" or dfn.item == "Griseous Orb":
        return
    if dfn.ability == "Sticky Hold" and not mold(att, dfn):
        reveal(dfn)
        return
    dfn.item, dfn.knocked_off = None, True


def steal_item(att, dfn):
    """Thief and Covet (effect script 105, BtlCmd_TryStealItem), once their
    hit has struck the target itself, not its Substitute, a knockout
    included. An AI trainer's never takes anything outside the Battle
    Frontier, so its Thief is a plain hit. The player's takes the target's
    item when it holds none itself, unless its own item was knocked off
    this battle, either has Multitype, the target holds a Griseous Orb or
    the target's Sticky Hold keeps it (named; Mold Breaker gets past it).
    Until 2026-10-15 either side's Thief removed the target's item, as
    Knock Off does, and the thief never gained it (Ian approved the fix)."""
    if att.item_off is not None or dfn.item_off is not None:
        return raw_item_op((att, dfn), lambda: steal_item(att, dfn))
    if att.side != "p" or att.item or not dfn.item or att.knocked_off or dfn.knocked_off:
        return
    if "Multitype" in (att.ability, dfn.ability) or dfn.item == "Griseous Orb":
        return
    if dfn.ability == "Sticky Hold" and not mold(att, dfn):
        reveal(dfn)
        return
    att.item, dfn.item = dfn.item, None


def swap_items(att, dfn, mv):
    """Trick and Switcheroo (effect script 177, subscript_exchange_items and
    BtlCmd_TrySwapItems) once the move has reached its target: an AI
    trainer's always fails outside the Battle Frontier. The player's swaps
    the two Pokemon's items unless the target's Substitute stands in the
    way, either has Multitype or holds a Griseous Orb, either slot's item
    was knocked off this battle, neither holds anything, or the target's
    Sticky Hold keeps its item (named; Mold Breaker gets past it). Until
    2026-10-15 nobody's Trick did anything (Ian approved the fix)."""
    if att.item_off is not None or dfn.item_off is not None:
        return raw_item_op((att, dfn), lambda: swap_items(att, dfn, mv))
    if att.side != "p" or sub_blocks(att, dfn, mv):
        return
    if "Multitype" in (att.ability, dfn.ability) or "Griseous Orb" in (att.item, dfn.item):
        return
    if att.knocked_off or dfn.knocked_off or not (att.item or dfn.item):
        return
    if dfn.ability == "Sticky Hold" and not mold(att, dfn):
        reveal(dfn)
        return
    att.item, dfn.item = dfn.item, att.item


def pluck(b, att, dfn, pick):
    """Bug Bite and Pluck (effect script 224, subscript_pluck, BtlCmd_TryPluck
    and BattleSystem_PluckBerry) once their hit has landed, on the target or
    on its Substitute, a knockout included: the user eats the target's Berry
    and takes its
    effect (eat_berry). The target's Sticky Hold keeps it (named; Mold
    Breaker gets past it); any other item stays where it is. The Berry is
    gone from the target and kept for its Recycle (RemoveItem), and the user
    has eaten a Berry (BattleScript_RecordBerryEaten, for Belch); a Klutz
    user eats it for nothing. Until 2026-10-15 only a Sitrus, an Oran or a
    pinch Berry did anything, and Sticky Hold was ignored (Ian approved the
    fix)."""
    if dfn.item_off is not None:
        return raw_item_op((dfn,), lambda: pluck(b, att, dfn, pick))
    berry = dfn.item
    if not berry or not berry.endswith("Berry"):
        return
    if dfn.ability == "Sticky Hold" and not mold(att, dfn):
        reveal(dfn)
        return
    consume(dfn, eaten=False)
    att.ate_berry = True
    if att.ability != "Klutz":
        eat_berry(att, berry, pick)


@functools.lru_cache(maxsize=None)
def _item_fling():
    """{compact item name: (fling power, fling effect)} from Oxide's item
    data (res/items/data, flingPower and flingEffect)."""
    out = {}
    for path in glob.glob(os.path.join(data.ROOT, "res", "items", "data", "*.json")):
        with open(path, encoding="utf-8") as fh:
            rec = json.load(fh)
        out[re.sub(r"[^a-z0-9]", "", (rec.get("name") or "").lower())] = (
            rec.get("flingPower") or 0, (rec.get("flingEffect") or "FLING_EFFECT_NONE")[len("FLING_EFFECT_"):])
    return out


def item_fling(item):
    """(fling power, fling effect) of a held item; (0, "NONE") for none."""
    return _item_fling().get(re.sub(r"[^a-z0-9]", "", (item or "").lower()), (0, "NONE"))


FLING_STATUS = {"BURN": "brn", "POISON": "psn", "BADLY_POISON": "tox", "PARALYZE": "par"}


def fling_effect(b, att, dfn, mv, item, first, pick):
    """Fling's thrown item on its target (BattleSystem_FlingItem's fling
    scripts, run by subscript_fling on the hit when the target stands and
    no Substitute is in the way): a Berry's effect as if the target ate it
    (eat_berry), the Orbs', the Poison Barb's and the Light Ball's status,
    King's Rock's and Razor Fang's flinch on a target yet to move, the
    White Herb's lowered stages put back, the Mental Herb's cure of love;
    any other item does nothing more. Until 2026-10-15 no fling effect ran
    (Ian approved the fix)."""
    effect = item_fling(item)[1]
    if item.endswith("Berry"):
        eat_berry(dfn, item, pick)
    elif effect in FLING_STATUS:
        give_status_by_move(b, att, dfn, mv, FLING_STATUS[effect])
    elif effect == "FLINCH":
        if first:
            dfn.flinch = True
    elif effect == "STATDOWN_RESTORE":
        dfn.stages = {k: max(0, v) for k, v in dfn.stages.items()}
    elif effect == "HEAL_INFATUATION":
        dfn.infatuated = None


def fling_key(key, item):
    """The row the player's Fling is read from: its twin holding the thrown
    item ("<key>#fl<item>", which prepare adds for each item the player is
    handed), since the player's own rows are made with no item and the
    calculator powers Fling by the item it holds, as the engine does, a
    plate's or another booster's own boost included (RemoveItem comes after
    CalcDamage)."""
    return f"{key}#fl{re.sub(r'[^a-z0-9]', '', (item or '').lower())}"


def eat_berry(mon, berry, pick):
    """A Berry's effect on the Pokemon that eats another's (PluckBerry's
    pluck effects, from the item data): an Oran Berry 10 HP and a Sitrus
    Berry a quarter; a cure Berry its status, a Persim Berry confusion and a
    Lum Berry both; a pinch Berry its stat a stage and a Starf Berry a
    stat chosen at random two, whatever the HP; a Lansat Berry Focus
    Energy's critical rate; a Leppa Berry 10 PP to the move missing most.
    The resist Berries and the rest have no effect when eaten so."""
    if berry == "Oran Berry":
        heal(mon, 10)
    elif berry == "Sitrus Berry":
        heal(mon, engine_divide(mon.maxhp * 25, 100))
    elif berry == "Lum Berry":
        mon.status, mon.sleep, mon.toxic, mon.confused = None, 0, 0, 0
    elif berry == "Persim Berry":
        mon.confused = 0
    elif berry in CURE_BERRY:
        if mon.status in CURE_BERRY[berry]:
            mon.status, mon.sleep, mon.toxic = None, 0, 0
    elif berry in PINCH_BERRIES:
        if item_can_raise(mon, PINCH_BERRIES[berry]):
            change_stages(mon, {PINCH_BERRIES[berry]: 1})
    elif berry == "Starf Berry":
        room = [s for s in ("atk", "def", "spa", "spd", "spe") if item_can_raise(mon, s)]
        if room:
            change_stages(mon, {room[pick("starf", len(room))]: 2})
    elif berry == "Lansat Berry":
        mon.crit_stage = max(mon.crit_stage, 2)
    elif berry == "Leppa Berry":
        gaps = [(m.pp - mon.pp.get(m.name, m.pp), m.name) for m in mon.moves]
        gap, name = max(gaps, default=(0, None))
        if gap > 0:
            mon.pp[name] += min(10, gap)


def recycle(att):
    """Recycle (effect script 184, BtlCmd_TryRecycle): the item its user
    last used up comes back, if it now holds nothing."""
    if not att.item and att.recycle:
        att.item, att.recycle = att.recycle, None


# The last moves Spite's command finds no slot for (Battler_SlotForMove
# returns LEARNED_MOVES_MAX): Mimic and Sketch, which have become other
# moves, and Struggle, which is no learned move.
SPITE_NO_SLOT = frozenset({"Mimic", "Sketch", "Struggle"})


def spite(dfn, amount=4):
    """Spite (BtlCmd_TrySpite): the target's last move loses 4 PP, or what
    it has left; it fails before the target has moved since it came in, when
    its last turn was lost (could_not_act clears `last`), with that move at
    0, or for a last move in SPITE_NO_SLOT. Eerie Spell's hit runs the same
    command for 3 (Oxide's engine since 2026-10-14)."""
    last = dfn.last
    if last is not None and last.name not in SPITE_NO_SLOT and dfn.pp.get(last.name, 0) > 0:
        dfn.pp[last.name] -= min(amount, dfn.pp[last.name])


def wish(side):
    """Wish: its side's slot is healed at the second turn's end by half the
    maximum HP of whoever then stands there (FIELD_COND_CHECK_STATE_WISH);
    it fails while one is pending."""
    if not side.wish:
        side.wish = 2


def pain_split(b, att, dfn):
    """Pain Split (subscript_pain_split): both Pokemon's HP become half
    their sum, each capped at its maximum (a berry fires on the drop as on
    any other); it fails on a Substitute."""
    if sub_blocks(att, dfn):
        return
    avg = (att.hp + dfn.hp) // 2
    for m in (att, dfn):
        if avg < m.hp:
            hurt(b, m, m.hp - avg)
        else:
            heal(m, avg - m.hp)


def infatuate(src, target, mold=False):
    """Attract or Cute Charm on target, in love with src (subscript_infatuate,
    BtlCmd_TryAttract): it fails on Oblivious (unless src has Mold Breaker),
    on one already in love, and unless the two are of opposite genders.
    Whether it took."""
    if target.ability == "Oblivious" and not mold:
        return False
    if target.infatuated or not src.gender or not target.gender or src.gender == target.gender:
        return False
    target.infatuated = src.key
    return True


# The abilities that strike back at a contact move (battle_lib's on-hit
# ability switch), each at three in ten but Rough Skin.
CONTACT_STATUS = {"Static": "par", "Poison Point": "psn", "Flame Body": "brn"}
# Every ability _struck_back has a branch for; any other returns False at once.
STRUCK_BACK = frozenset(CONTACT_STATUS) | {"Mummy", "Wandering Spirit", "Aftermath", "Rough Skin", "Iron Barbs",
                                           "Cute Charm", "Gooey", "Pickpocket", "Effect Spore"}


def contact_ability(b, att, dfn, mv, dealt, chance, pick):
    """The defender's ability after a move hurt it, as battle_lib's on-hit
    switch has them (BattleSystem_TriggerAbilityOnHit): only when the move did
    damage (not to a Substitute). Those any damaging hit sets off come first
    (hit_ability: Cursed Body); then, for a contact move whose user still
    stands, Static, Poison Point, Flame Body, Effect Spore and Cute Charm at
    3 in 10, a status only on an attacker with none, and Rough Skin and
    Oxide's Iron Barbs an eighth of the attacker's HP. When none of those
    acted, Oxide's Poison Touch poisons the target 3 times in 10, after a
    contact move, and Magician takes its item (battle_lib, after the
    switch). Contact is Battler_MoveMakesContact's (makes_contact).
    `chance(kind, p, victim)` and `pick(kind, n)` are the battle's dice."""
    if dealt <= 0:
        return
    contact = makes_contact(att, mv)
    acted = bool(dfn.ability and hit_ability(b, att, dfn, mv, chance, dealt))
    if not acted and contact:
        acted = bool(att.alive() and dfn.ability and _struck_back(b, att, dfn, chance, pick, mv))
        if not acted and att.ability == "Poison Touch" and dfn.alive() and not dfn.status \
                and chance("status", 0.3, dfn):
            acted = True
            b.status_src = att
            if give_status(b, dfn, "psn"):
                reveal(att)
    if not acted and att.ability == "Magician":
        magician(b, att, dfn)
    if contact:
        sticky_barb(att, dfn)


def magician(b, att, dfn):
    """Magician (BattleSystem_TriggerAbilityOnHit after its switch,
    subscript_magician): when the target's own on-hit ability did nothing,
    a damaging move that did damage, by a standing user holding nothing, to
    a target holding an item, takes the item by Thief's checks
    (TryStealItem, steal_item): never for a trainer's Pokemon outside the
    Battle Frontier, and Sticky Hold keeps it in silence. A trainer's
    Pokemon robbed of its item reads its item twin (mark_unheld). Until
    2026-10-20 it did nothing (Ian approved the fix)."""
    if not att.alive() or att is dfn or att.item or att.item_off is not None \
            or not (dfn.item or dfn.item_off is not None):
        return
    if dfn.ability == "Sticky Hold" and not mold(att, dfn):
        return
    steal_item(att, dfn)
    mark_unheld(b, dfn)


def makes_contact(att, mv):
    """Whether att's move makes contact (Battler_MoveMakesContact): a move
    with the contact flag, unless its user has Long Reach, which every
    contact answer asks (the on-hit abilities, Sticky Barb, Spiky Shield
    and its kin, Mummy and Wandering Spirit). Until 2026-10-20 Long Reach
    did nothing (Ian approved the fix)."""
    return mv.contact and att.ability != "Long Reach"


def sticky_barb(att, dfn):
    """A contact hit on a Sticky Barb's holder hands the barb to an attacker
    that stands and holds nothing (BattleSystem_TriggerHeldItemOnHit's
    HOLD_EFFECT_DMG_USER_CONTACT_XFR; Knock Off, which takes the item
    first, leaves nothing to hand). Until 2026-10-14 the barb did nothing
    (Ian approved the fix)."""
    if dfn.item == "Sticky Barb" and att.alive() and not att.item and att is not dfn:
        att.item, dfn.item = dfn.item, None


# The abilities a hit of these types raises a stat of (subscript_justified,
# subscript_rattled, by CurrentMoveType).
HIT_RAISE = {"Justified": ({"Dark"}, "atk"), "Rattled": ({"Bug", "Ghost", "Dark"}, "spe")}
# Every ability hit_ability has a branch for; any other returns False at once.
HIT_ABILITIES = frozenset(HIT_RAISE) | {"Weak Armor", "Water Compaction", "Toxic Debris", "Berserk",
                                        "Cursed Body", "Color Change"}


def hit_type(b, mv):
    """The type a move hits with as the battle records it: Weather Ball's
    from the weather, every other move's its own."""
    if mv.name == "Weather Ball":
        return {"Sun": "Fire", "Rain": "Water", "Hail": "Ice", "Sand": "Rock"}.get(weather_now(b), mv.type)
    return mv.type


def hit_ability(b, att, dfn, mv, chance, dealt=0):
    """The defender's on-hit abilities that any damaging hit sets off,
    contact or not (BattleSystem_TriggerAbilityOnHit's switch); whether one
    acted. Cursed Body: three times in ten the attacker's move, if it has
    power, is one of its moves with PP left after the use and no move of
    its is disabled already, is disabled for three turn ends after this
    one's (disabledTurns 3, Disable's own count), its holder fainted or
    not. Justified gains a stage of Attack from a Dark hit, and Rattled one
    of Speed from a Bug, Ghost or Dark one, while their holder stands, each
    raised directly (raise_own). Until 2026-10-14 none of the three did
    anything (Ian approved the fix)."""
    a = dfn.ability
    if a not in HIT_ABILITIES:
        return False                 # none of the branches below names it
    if a in HIT_RAISE:
        types, stat = HIT_RAISE[a]
        return dfn.alive() and hit_type(b, mv) in types and raise_own(dfn, stat, 1)
    if a == "Weak Armor":
        # subscript_weak_armor: a physical hit that did damage to its holder,
        # still standing, takes its Defense down a stage and then its Speed
        # up two (ability_stages), the Speed rising though the Defense is at
        # -6 already. Until 2026-10-20 it did nothing (Ian approved the fix).
        if not dfn.alive() or mv.cat != "Physical":
            return False
        ability_stages(dfn, dfn, "def", -1)
        ability_stages(dfn, dfn, "spe", 2)
        return True
    if a == "Water Compaction":
        # subscript_water_compaction: a Water hit that did damage, by the
        # type the battle records it with (Normalize's Normal, Weather
        # Ball's, Liquid Voice's Water: move_type_used), raises its holder's
        # Defense two stages while it stands. Until 2026-10-20 it did
        # nothing (Ian approved the fix).
        if not dfn.alive() or move_type_used(att.ability, mv, att.ivs, att.item or att.recycle,
                                             weather_now(b)) != "Water":
            return False
        ability_stages(dfn, dfn, "def", 2)
        return True
    if a == "Toxic Debris":
        # A physical hit that did damage lays a layer of Toxic Spikes on its
        # holder's other side, two at most, whether or not the holder still
        # stands (BattleSystem_TriggerAbilityOnHit, subscript_toxic_debris).
        # Until 2026-10-20 it did nothing (Ian approved the fix).
        side = b.b if dfn.side == "p" else b.p
        if mv.cat != "Physical" or side.hazards["tspikes"] >= 2:
            return False
        side.hazards["tspikes"] += 1
        reveal(dfn)
        return True
    if a == "Berserk":
        # BattleSystem_TriggerAbilityOnHit, subscript_berserk: a hit that
        # did damage and took its standing holder from above half its
        # maximum HP to half or less, by HP read before any Berry answers
        # the hit (Battle.hit_left), and not one Sheer Force boosted, raises
        # its Sp. Atk a stage by AbilityStatChange (ability_stages); the
        # ability has answered even at +6. Until 2026-10-20 it did nothing
        # (Ian approved the fix).
        left = b.hit_left if b.hit_left is not None else dfn.hp
        half = dfn.maxhp // 2
        if not dealt or not left or left > half or left + dealt <= half or sheer_force_active(att, mv):
            return False
        ability_stages(dfn, dfn, "spa", 1)
        return True
    if a == "Cursed Body":
        if (att.alive() and att is not dfn and att.disabled is None and mv.power
                and any(m.name == mv.name for m in att.moves) and att.pp.get(mv.name, 0) > 0
                and chance("cursedbody", 0.3, att)):
            att.disabled, att.disabled_turns = mv.name, 3
            return True
        return False
    if a == "Color Change":
        return color_change(b, att, dfn, mv)
    return False


def color_change(b, att, dfn, mv):
    """Color Change (BattleSystem_TriggerAbilityOnHit, subscript_color_change):
    a move with power that did damage to its holder, Struggle aside and not
    one Sheer Force boosts, makes the holder that move's type alone while it
    stands and is not of that type already, the type as the battle records
    it (move_type_used: Weather Ball's weather's, Hidden Power's and Natural
    Gift's own, a Normalize, Pixilate or Liquid Voice user's); the message
    names the ability. Its rows then come from its twin of that type
    (form_key) until it leaves. Whether it acted. Until 2026-10-14 Color
    Change did nothing (Ian approved the fix)."""
    t = move_type_used(att.ability, mv, att.ivs, att.item or att.recycle, weather_now(b))
    if (not dfn.alive() or not mv.power or mv.effect == "STRUGGLE" or sheer_force_active(att, mv)
            or t in dfn.types):
        return False
    set_types(dfn, [t])
    reveal(dfn)
    return True


@form_change
def _color_changed(ff):
    """Color Change: its holder can become the type of any damaging move its
    foes can hit it with (FormFight.hit_types) but its own."""
    for k in ff.keys():
        if ff.ability(k) == "Color Change":
            own = set(ff.types(k))
            for t in sorted({t for f in ff.foes(k) for t in ff.hit_types(f)} - own):
                yield k, [t], ff.ability(k)


def mummy(b, att, dfn):
    """Mummy (BattleSystem_TriggerAbilityOnHit, subscript_mummy): a contact
    move that hurt its holder, standing or not, passes Mummy to the attacker
    while it stands, unless its ability is Mummy already, refuses to be
    replaced, or is kept by an Ability Shield; the message names the
    attacker's new ability. Its rows are then its ability-blank twin's
    (form_key), so Levitate, Huge Power and the like are gone with the old
    ability. Whether it acted. Until 2026-10-14 Mummy did nothing (Ian
    approved the fix)."""
    raw = raw_ability(att)
    if not att.alive() or att is dfn or raw == "Mummy" or refuses(raw, "suppress") or att.item == "Ability Shield":
        return False
    set_ability(b, att, "Mummy")
    return True


@form_change
def _mummified(ff):
    """Mummy: any foe of a holder with a contact move and an ability Mummy
    can replace may take Mummy. The holder's partner that takes it in turn,
    from a foe that has, keeps its own rows: a second step, left out to keep
    the preparation from growing with every contact move in the box."""
    for h in ff.keys():
        if ff.ability(h) != "Mummy":
            continue
        for k in ff.foes(h):
            ab = ff.ability(k)
            if (ab != "Mummy" and not refuses(ab, "suppress") and ff.pokemon[k].get("item") != "Ability Shield"
                    and ff.contact(k)):
                yield k, None, "Mummy"


def wandering_spirit(b, att, dfn):
    """Wandering Spirit (BattleSystem_TriggerAbilityOnHit,
    subscript_wandering_spirit): a contact move that hurt its holder swaps
    the holder's ability with the attacker's while the attacker stands,
    unless the attacker's is Wandering Spirit already or refuses a swap, or
    either holds an Ability Shield; both are named, and a Truant either gains
    loafs on its next turn. Each then reads its twin for its new ability
    (form_key). Whether it acted. Until 2026-10-14 Wandering Spirit did
    nothing (Ian approved the fix)."""
    raw, own = raw_ability(att), raw_ability(dfn)
    if (not att.alive() or att is dfn or raw == "Wandering Spirit" or refuses(raw, "swap")
            or "Ability Shield" in (att.item, dfn.item)):
        return False
    set_ability(b, att, own)
    set_ability(b, dfn, raw, acted=getattr(dfn, "acted_turn", None) == b.turn)
    return True


@form_change
def _spirit_swapped(ff):
    """Wandering Spirit: its holder can take the ability of any foe with a
    contact move whose ability a swap can take, and that foe takes Wandering
    Spirit."""
    for k in ff.keys():
        if ff.ability(k) != "Wandering Spirit" or ff.pokemon[k].get("item") == "Ability Shield":
            continue
        for f in ff.foes(k):
            ab = ff.ability(f)
            if (ab != "Wandering Spirit" and not refuses(ab, "swap") and ff.contact(f)
                    and ff.pokemon[f].get("item") != "Ability Shield"):
                yield k, None, ab, (f, None, "Wandering Spirit")


def pickpocket(b, att, dfn, mv):
    """Pickpocket (BattleSystem_TriggerAbilityOnHit, subscript_pickpocket):
    a contact move that did damage to its standing holder, which holds
    nothing, from a user that holds an item, not one Sheer Force boosted,
    and not a Dragon Tail or Circle Throw about to drag the holder out
    (drag_coming, Ian's ruling of 2026-10-15). TryPickpocket then lets the
    item go to the holder unless the holder's own item was knocked off this
    battle, either has Multitype, the item is a Griseous Orb or the user
    has Sticky Hold; the message names neither ability. Unlike Thief a
    trainer's holder takes the item too. A trainer's Pokemon that loses
    its item reads its item twin (mark_unheld). Whether the ability ran.
    Until 2026-10-20 it did nothing (Ian approved the fix)."""
    if att.item_off is not None or dfn.item_off is not None:
        return raw_item_op((att, dfn), lambda: pickpocket(b, att, dfn, mv))
    if (not dfn.alive() or dfn.item or not att.item or att is dfn or sheer_force_active(att, mv)
            or drag_coming(b, att, dfn, mv)):
        return False
    if not (dfn.knocked_off or "Multitype" in (att.ability, dfn.ability) or att.item == "Griseous Orb"
            or att.ability == "Sticky Hold"):
        dfn.item, att.item = att.item, None
        mark_unheld(b, att)
    return True


def _struck_back(b, att, dfn, chance, pick, mv):
    """The defender's on-hit ability that a contact move of att's, mv, sets
    off; whether it acted."""
    a = dfn.ability
    b.status_src = dfn           # a status the ability gives comes from dfn (Synchronize)
    if a not in STRUCK_BACK:
        return False                 # none of the branches below names it
    if a == "Mummy":
        return mummy(b, att, dfn)
    if a == "Wandering Spirit":
        return wandering_spirit(b, att, dfn)
    if a == "Aftermath":
        # A contact move that fainted it costs its user a quarter of its
        # HP, unless Magic Guard or a Damp Pokemon on the field stops it.
        if not dfn.alive() and att.ability != "Magic Guard" and not any(
                m.ability == "Damp" and m.alive() for m in b.p.on_field() + b.b.on_field()):
            reveal(dfn)
            hurt(b, att, max(1, att.maxhp // 4))
            return True
        return False
    if a in ("Rough Skin", "Iron Barbs"):
        if att.ability != "Magic Guard":
            reveal(dfn)
            hurt(b, att, max(1, att.maxhp // 8))
            return True
        return False
    if a == "Cute Charm":
        if not att.infatuated and chance("status", 0.3, att):
            if infatuate(dfn, att):
                reveal(dfn)
            return True
        return False
    if a == "Gooey":
        # subscript_gooey: a contact move that did damage lowers its user's
        # Speed a stage while it is above -6, by ability_stages (Clear Body,
        # White Smoke and a Clear Amulet keep it; Mist and Mirror Armor do
        # not), and TryDefiant answers the drop. Until 2026-10-20 it did
        # nothing (Ian approved the fix).
        if att.stages["spe"] <= -6:
            return False
        if ability_stages(dfn, att, "spe", -1) and att.ability in DEFIANT_STAT:
            raise_own(att, DEFIANT_STAT[att.ability], 2)
        return True
    if a == "Pickpocket":
        return pickpocket(b, att, dfn, mv)
    if att.status:
        return False
    if a == "Effect Spore":
        # Oxide: its spores are a powder, which misses Grass types, Overcoat
        # and Safety Goggles.
        if "Grass" in att.types or att.ability == "Overcoat" or att.item == "Safety Goggles":
            return False
        if chance("status", 0.3, att):
            status = ("psn", "par", "slp")[pick("spore", 3)]
            if give_status(b, att, status):
                reveal(dfn)
            return True
        return False
    if a in CONTACT_STATUS and chance("status", 0.3, att):
        if give_status(b, att, CONTACT_STATUS[a]):
            reveal(dfn)
        return True
    return False


# ---- held items and abilities the calculator's rows cannot know (2026-10-03) ---------------------
# The rows are made once per fight, at full HP, with each Pokemon's starting
# item; these change a fight's state as it runs, as the decomp has them.

PINCH_ABILITY = {"Overgrow": "Grass", "Blaze": "Fire", "Torrent": "Water", "Swarm": "Bug"}
RESIST_BERRY = {"Occa Berry": "Fire", "Passho Berry": "Water", "Wacan Berry": "Electric", "Rindo Berry": "Grass",
                "Yache Berry": "Ice", "Chople Berry": "Fighting", "Kebia Berry": "Poison", "Shuca Berry": "Ground",
                "Coba Berry": "Flying", "Payapa Berry": "Psychic", "Tanga Berry": "Bug", "Charti Berry": "Rock",
                "Kasib Berry": "Ghost", "Haban Berry": "Dragon", "Colbur Berry": "Dark", "Babiri Berry": "Steel",
                "Chilan Berry": "Normal"}
CURE_BERRY = {"Pecha Berry": ("psn", "tox"), "Cheri Berry": ("par",), "Chesto Berry": ("slp",),
              "Rawst Berry": ("brn",), "Aspear Berry": ("frz",),
              "Lum Berry": ("psn", "tox", "par", "slp", "brn", "frz")}
FLAIL_POWER = ((1, 200), (5, 150), (12, 100), (21, 80), (42, 40), (64, 20))


def flail_power(mon):
    """Flail and Reversal's power (BtlCmd_CalcFlailPower): the HP bar's
    pixels out of 64 against sHPPixelsToFlailPower."""
    px = mon.hp * 64 // mon.maxhp
    if px == 0 and mon.hp > 0:
        px = 1
    return next(p for top, p in FLAIL_POWER if px <= top)


def _row_item(b, mon):
    """The item mon's calculator rows were made with (the player's rows are
    item-free). A key with no "#" is its own record's, so it is split only
    when it has one."""
    k = mon.key
    return (b.st["pokemon"].get(k.split("#")[0] if "#" in k else k) or {}).get("item")


# ---- a trainer's held item gone from its rows (batch 10, approved 2026-10-15) ----
#
# A trainer's rows are made with its held item, so a Charcoal, a Life Orb,
# a Choice item, an Expert Belt or an Eviolite stays in them. Once the
# battle takes the item away (the player's Knock Off, Thief, Covet, Trick or
# Switcheroo, or the trainer's own Fling), the engine reads no item
# (Battler_HeldItemEffect), so prepare() rows such a Pokemon a second time
# with no item (its item twin, "<key>#ni"), both ways against every foe,
# and the battle reads the twin while the Pokemon lacks the item its rows
# were made with (Mon.unheld, set by mark_unheld). A fight where nothing can
# take a trainer's item gets no twin.

# The items the calculator's files name that never change a row the
# simulator makes: White Herb and Clear Amulet answer only Intimidate and
# stat drops, and the rows carry neither (CALC_ABILITY_OFF, no stages).
ROW_NEUTRAL_ITEMS = frozenset({"White Herb", "Clear Amulet"})
# The moves of a foe that take a trainer's item away, and the trainer's own
# move that spends it.
TAKES_ITEM = frozenset({"REMOVE_HELD_ITEM", "STEAL_HELD_ITEM", "SWITCH_HELD_ITEMS"})
# The abilities that take a foe's item (pickpocket, magician), for the same
# twins.
TAKING_ABILITIES = frozenset({"Pickpocket", "Magician"})


def _compact(name):
    return re.sub(r"[^a-z0-9]", "", name.lower())


@functools.lru_cache(maxsize=None)
def row_items():
    """The held items a calculator row can read, compacted (Generation 4's
    "DeepSeaTooth" and Oxide's "Deep Sea Tooth" alike): every item a file
    the Generation 4 row runs through asks for by name (hasItem, or an item
    compared by name), and the type boosters of getItemBoostType; a
    superset that costs at most a twin too many."""
    base = os.path.join(data.ROOT, "tools", "oxide", "encounters", "calc", "calc")
    found = set()
    for rel in CALC_ROW_FILES:
        with open(os.path.join(base, rel), encoding="utf-8") as fh:
            text = fh.read()
        for args in re.findall(r"hasItem\(([^)]*)\)", text):
            found.update(re.findall(r"""['"]([^'"]+)['"]""", args))
        found.update(re.findall(r"""item(?:\.name)? === ['"]([^'"]+)['"]""", text))
        if "function getItemBoostType" in text:
            body = text[text.index("function getItemBoostType"):text.index("exports.getItemBoostType")]
            found.update(re.findall(r"case '([^']+)'", body))
    return frozenset(_compact(n) for n in found)


def row_item(item):
    """Whether a trainer's rows read this held item, so its loss needs the
    item twin: one row_items names, a Berry apart (a resist Berry's halving
    the battle undoes itself, berry_works; no other Berry changes a row) and
    the ROW_NEUTRAL_ITEMS."""
    return bool(item) and not item.endswith("Berry") and item not in ROW_NEUTRAL_ITEMS \
        and _compact(item) in row_items()


def item_key(b, mon):
    """The key of mon's item twin (prepare's item_twin), or None."""
    return (b.st.get("item_twin") or {}).get(mon.key)


def flinging(mv):
    """Whether mv is Fling, whose hit a trainer's Pokemon reads from its own
    rows, made with its own item, even once the throw has spent the item
    (Battle.row): a Fling with nothing to throw fails before its hit."""
    return mv is not None and mv.name == "Fling"


def mark_unheld(b, *mons):
    """After a move took, swapped or spent a held item: each of mons that
    has an item twin reads it while it holds anything but the item its rows
    were made with (Mon.unheld), and the battle notes that one may
    (Battle.unheld), so Battle.row looks no further otherwise."""
    twins = b.st.get("item_twin")
    if not twins:
        return
    for m in mons:
        if m.key in twins:
            m.unheld = m.item != b.st["pokemon"][m.key].get("item")
            if m.unheld:
                b.unheld = True
                if m.ability == "Multitype" and m.item not in JUDGMENT_TYPE:
                    unplate(m)   # an Arceus whose Plate is gone is Normal, its twin too (plate_form)


# ---- Meloetta's two forms (batch 10, approved 2026-10-15) ----

@functools.lru_cache(maxsize=None)
def pirouette_data():
    """Meloetta's Pirouette form as prepare()'s species_data, from its
    record (res/pokemon/meloetta/forms/pirouette): its base stats and its
    types, exactly. The calculator's species table knows only Aria."""
    path = os.path.join(data.ROOT, "res", "pokemon", "meloetta", "forms", "pirouette", "data.json")
    with open(path, encoding="utf-8") as fh:
        raw = json.load(fh)
    bs = raw["base_stats"]
    return {"bs": {"hp": bs["hp"], "at": bs["attack"], "df": bs["defense"], "sa": bs["special_attack"],
                   "sd": bs["special_defense"], "sp": bs["speed"]},
            "types": [t[len("TYPE_"):].title() for t in raw["types"]], "exact_types": True}


def pirouette_key(b, mon):
    """The key of a Meloetta's Pirouette twin (prepare's meloetta_twin), or None."""
    return (b.st.get("meloetta_twin") or {}).get(mon.key)


def relic_song(b, att, mv, hit):
    """Relic Song's turn of Meloetta between Aria and Pirouette, once a use
    of it has hit (BattleControllerPlayer_TriggerAfterMoveHitEffects'
    AFTER_MOVE_HIT_STATE_RELIC_SONG, under SYSCTL_MOVE_HIT, which a hit on
    a target itself sets and a Substitute's does not; `hit`): a Meloetta
    still standing and not transformed takes the other form, its types and
    stats from the form's record (subscript_relic_song_form recalculates
    them), its rows and Speed from its Pirouette twin (pirouette_key);
    both forms' ability is Serene Grace. It goes back to Aria as it leaves
    (Mon.reset_volatile). Until 2026-10-15 it kept its starting form (Ian
    approved the fix)."""
    if not hit or att.species != "Meloetta" or not att.alive() or att.transformed:
        return
    twin = pirouette_key(b, att)
    if twin is None:
        return
    if att.pirouette:
        att.types, att.stats = att.aria
        att.pirouette, att.aria = False, None
        return
    info = b.st["info"][twin]
    att.aria = (att.types, att.stats)
    att.types, att.stats = [t.title() for t in info.get("types") or []], info["stats"]
    att.pirouette = att.rare = True


# Knock Off and Bug Bite (effect scripts 188 and 224): their own effect is
# an on-hit side effect (ONE_HIT_TRIGGER_SECONDARY), which runs before the
# target's held item is checked (AFTER_MOVE_EFFECT_DEFENDER_ITEM), so a
# Sitrus Berry or a pinch Berry is knocked off or eaten by the user before
# its holder can eat it.
TAKES_FIRST = frozenset({"REMOVE_HELD_ITEM", "EAT_BERRY"})


def take_first(b, att, dfn, mv, pick):
    """Knock Off's and Bug Bite's effect once their hit has struck the target
    itself, before the target's own Berry can act (berry_check comes
    after): a resist Berry that halved the hit has been eaten already (the
    hit's update of HP runs subscript_type_resist_berry), so neither move
    finds it; then Bug Bite and Pluck eat the target's Berry (pluck), a
    knockout included, and Knock Off takes the item of a target left
    standing (knock_off), whose item twin it reads from then on
    (mark_unheld). Until 2026-10-15 the target ate its Berry first, and a
    trainer's knocked-off item went on boosting its rows (Ian approved the
    fixes)."""
    berry = resist_berry(b, dfn, mv)
    if berry_works(b, dfn, berry):
        consume(dfn)
    if mv.effect == "EAT_BERRY":
        pluck(b, att, dfn, pick)
    elif dfn.alive():
        knock_off(att, dfn)
        mark_unheld(b, dfn)


def resist_berry(b, dfn, mv):
    """The resist berry dfn's rows halve this move by, if any: one of the
    move's type, against a super-effective hit (any Normal move for the
    Chilan Berry)."""
    if mv.cat == "Status" or mv.effect in (FUTURE_SIGHT, "BEAT_UP"):
        return None                  # Future Sight and Beat Up never meet the type chart, nor a resist berry
    berry = _row_item(b, dfn)        # looked up only for a move that can meet one
    if RESIST_BERRY.get(berry) != mv.type:
        return None
    if berry != "Chilan Berry" and effectiveness(b.st["chart"], mv.type, chart_types(dfn, mv)) <= 1:
        return None
    return berry


def berry_first_hit(b, dfn, mv, dmg, hits):
    """A move that hits more than once loses only its first hit to a resist
    berry. The battle script that halves a hit also uses the berry up
    (subscript_type_resist_berry.s, run from each hit's update of HP), so
    every later hit lands in full; the calculator's row halves them all, so
    each hit after the first gets its half back. `hits` is the hits this use
    rolled; a Double Kick-style move always hits twice. Until 2026-10-13 the
    simulator halved every hit, and Golbat's Dual Wingbeat left a Coba
    Berry Breloom at a tenth of its HP where the game knocks it out (Ian
    approved the fix)."""
    berry = resist_berry(b, dfn, mv)
    if not berry_works(b, dfn, berry):
        return dmg
    if mv.effect == "HIT_TWICE":
        powers = [1, 1]
    elif mv.effect == "MULTI_HIT":
        powers = [1] * hits
    elif mv.effect in RISING:
        powers = rising_powers(mv)[:hits]
    else:
        return dmg
    if len(powers) < 2:
        return dmg
    # The row is every hit at half; the game is the first at half and the
    # rest whole, which is the row times 2 less the first hit's share.
    return int(dmg * (2 - powers[0] / sum(powers)))


# The moves that reach a Pokemon in the air from Fly or Bounce (their effect
# scripts set SYSCTL_HIT_DURING_FLY), with their power there: Gust and
# Twister double (scripts 149 and 146); Thunder, Sky Uppercut, Hurricane and
# Smack Down hit at their power (152, 207, 341, 406). Smack Down's grounding,
# which also ends the Fly, is not simulated.
HIT_IN_AIR = {"DOUBLE_DAMAGE_FLY_OR_BOUNCE": 2, "FLINCH_DOUBLE_DAMAGE_FLY_OR_BOUNCE": 2,
              "THUNDER": 1, "HIT_FLY": 1, "HURRICANE": 1, "SMACK_DOWN": 1}


def reach_mult(mv, dfn):
    """How a move strikes a Pokemon on a two-turn move's hidden turn: 0 when
    it cannot; Earthquake and Magnitude underground, and Surf and Whirlpool
    underwater, at double damage; the moves of HIT_IN_AIR in the air. Thousand
    Arrows shares Smack Down's effect but does not reach the air (Oxide)."""
    c = dfn.charging
    if c is None:
        return 0
    if c.effect == "DIG" and (mv.effect == "DOUBLE_DAMAGE_DIG" or mv.name == "Magnitude"):
        return 2
    if c.effect == "DIVE" and mv.effect in ("DOUBLE_DAMAGE_DIVE", "WHIRLPOOL"):
        return 2
    if c.effect in ("FLY", "BOUNCE") and mv.effect in HIT_IN_AIR and mv.name != "Thousand Arrows":
        return HIT_IN_AIR[mv.effect]
    return 0


def reaches(mv, dfn):
    """Whether a move strikes a Pokemon mid-Dig, mid-Dive or in the air."""
    return reach_mult(mv, dfn) > 0


def doubled(att, dfn, mv):
    """A move whose effect script doubles its power by the target's state as
    the hit lands, which the rows (made with no status) cannot know and the
    trainer's AI does not reckon in its damage (it scores these through
    Expert_Hex and kin): Hex and Infernal Parade on a target with a status
    or Comatose (effect scripts 287 and 321); Venoshock and Barb Barrage on a
    poisoned one (280, 322); Assurance on one that lost HP earlier this turn
    (231, the turn flag subscript_update_hp sets)."""
    e = mv.effect
    if e in ("DOUBLE_DAMAGE_ON_STATUS", "BURN_HIT_DOUBLE_POWER_ON_STATUS"):
        return bool(dfn.status) or dfn.ability == "Comatose"
    if e in ("DOUBLE_POWER_ON_POISONED", "POISON_HIT_DOUBLE_POWER_ON_POISONED"):
        return dfn.status in ("psn", "tox")
    if e == "DOUBLE_POWER_IF_TARGET_HIT":
        return bool(dfn.hit_this_turn) or dfn.hurt_this_turn
    if e == "DOUBLE_DAMAGE_WITHOUT_ITEM":
        # Acrobatics (effect script 289): POWER_MULTI 20 when its user holds
        # no item, an eaten, flung or knocked-off one included; the rows never
        # double it. Until 2026-10-15 it never doubled (Ian approved the fix).
        return not (att.item or att.item_off)     # an item held under Embargo or Magic Room still counts
    if e == "DOUBLE_POWER_AND_CURE_PARALYSIS":
        # Smelling Salts (effect script 171) on a paralysed target with no
        # Substitute in the way (CheckSubstitute skips the doubling and the
        # cure, an Infiltrator passing it). Until 2026-10-15 it never
        # doubled (Ian approved the fix).
        return dfn.status == "par" and not sub_blocks(att, dfn, mv)
    if e == "FLINCH_MINIMIZE_DOUBLE_HIT":
        # Stomp and Steamroller (effect script 150) on a target that has used
        # Minimize since it came in (MOVE_EFFECT_MINIMIZE, set by
        # subscript_minimize). Until 2026-10-15 nothing kept the mark, so
        # they never doubled (Ian approved the fix).
        return dfn.minimized
    return False


def spin(b, att, dfn, e):
    """Rapid Spin and Mortal Spin on a hit (BtlCmd_RapidSpin): the user is
    freed from a binding move and from Leech Seed, and every hazard on its
    own side is cleared. Oxide's Rapid Spin then raises its user's Speed a
    stage (subscript_rapid_spin); Mortal Spin first poisons its target
    (subscript_mortal_spin) as a secondary effect, which a Substitute,
    Shield Dust and Covert Cloak stop."""
    if (e == "MORTAL_SPIN" and dfn.alive() and not sub_blocks(att, dfn)
            and (dfn.ability != "Shield Dust" or mold(att, dfn)) and dfn.item != "Covert Cloak"):
        give_status_by_move(b, att, dfn, None, "psn")
    att.bound = 0
    att.seeded = False
    side = b.p if att.side == "p" else b.b
    side.hazards = dict.fromkeys(side.hazards, 0)
    if side.web:
        side.web = 0                 # Oxide's Rapid Spin and Mortal Spin clear Sticky Web too (BtlCmd_RapidSpin)
    if e == "REMOVE_HAZARDS_AND_BINDING" and att.alive():
        change_stages(att, {"spe": 1})


def party_cure(b, att, mv):
    """Heal Bell and Aromatherapy (effect script 102, subscript_heal_bell):
    TryPartyStatusRefresh cures the user and, in a double battle, its
    partner on the field, each losing Nightmare with its status, and
    BtlIOCmd_RefreshPartyStatus cures every Pokemon of the user's own
    party. Heal Bell, a sound, spares a Soundproof Pokemon: the user's own
    Soundproof always, a partner's and a party member's unless the user
    has Mold Breaker (the partner's through Battler_IgnorableAbility, the
    party's because the message passes a Mold Breaker user's ability as
    none). Aromatherapy cures them all. The cure clears the status as
    sparkly_swirl does. Until 2026-10-20 both cured every Pokemon on the
    side and left Nightmare (Ian approved the fix on 2026-10-20)."""
    side = b.p if att.side == "p" else b.b
    field = side.on_field()
    bell = mv.const == "MOVE_HEAL_BELL"
    owner = getattr(att, "owner", None)
    for m in side.mons:
        if m not in field and getattr(m, "owner", None) != owner:
            continue
        if bell and m.ability == "Soundproof" and (m is att or att.ability != "Mold Breaker"):
            continue
        m.status = None
        if m in field:
            m.nightmare = False


def sparkly_swirl(b, att):
    """Sparkly Swirl (effect script 314): once its hit lands, a Substitute's
    or a knockout's too (an indirect effect run ON_HIT, which Sheer Force
    does not strip), subscript_heal_bell's TryPartyStatusRefresh runs as for
    any move but Heal Bell: its user's status and Nightmare are gone, and so
    are those of its partner on the field, and every Pokemon in its party is
    cured (BtlIOCmd_RefreshPartyStatus), Soundproof or not. Until 2026-10-20
    it was a plain hit (Ian approved the fix)."""
    side = b.p if att.side == "p" else b.b
    field = side.on_field()
    for m in side.mons:
        if m in field or getattr(m, "owner", None) == getattr(att, "owner", None):
            m.status = None
    for m in field:
        m.nightmare = False


# Fickle Beam's roll (effect script 349): Random 9, 0 gives 0 to 9, and
# above 6 the power doubles, so three times in ten.
FICKLE_ODDS = {True: 3, False: 7}


def fickle_doubles(b):
    """Whether this Fickle Beam goes all out at twice its power (effect
    script 349's POWER_MULTI 20), on the battle's dice: a run's draw or the
    planner's weighted event; where no dice can weigh it, the likelier,
    not. Until 2026-10-20 it never doubled (Ian approved the fix)."""
    pick = getattr(getattr(b, "dice", None), "pick_weighted", None)
    if pick is not None:
        return pick(list(FICKLE_ODDS), list(FICKLE_ODDS.values()))
    rng = getattr(b, "rng", None)
    return rng.random() < 0.3 if rng is not None else False


def beak_doubles(b, dfn, first):
    """Whether Bolt Beak and Fishious Rend double their power
    (BtlCmd_CalcBoltBeakPower, effect script 382): while the target's
    action this turn is still to come (`first`), or when its side chose
    this turn to switch it in, which the engine counts as not having acted
    (Generation 8's rule; Mon.switched_turn). The rows are made at the
    listed power, which the trainer's AI reckons with too. Until 2026-10-20
    they never doubled (Ian approved the fix)."""
    return first or dfn.switched_turn == b.turn


def sappy_seed(dfn):
    """Sappy Seed (effect script 310): its hit's indirect effect
    (MOVE_SIDE_EFFECT_CHECK_HP) runs subscript_leech_seed_start on a target
    left standing: nothing behind a Substitute, one hit this move included
    (CheckSubstitute, past an Infiltrator), on a Grass type or on one
    seeded already; else the target is seeded, as by Leech Seed. Neither
    Sheer Force nor Shield Dust stops it. Until 2026-10-20 it was a plain
    hit (Ian approved the fix)."""
    if "Grass" not in dfn.types:
        dfn.seeded = True


def fainted_party(b, mon):
    """How many of mon's party have fainted (Last Respects' count in
    BattleScript_ComputedMovePower: the party members, eggs aside, at 0 HP):
    its side's Pokemon of its own trainer, as a tag battle keeps each
    trainer's party apart (Mon.owner)."""
    side = b.p if mon.side == "p" else b.b
    owner = getattr(mon, "owner", None)
    return sum(1 for m in side.mons if not m.alive() and getattr(m, "owner", None) == owner)


def technician(att, power):
    """A move's power after Technician, which BattleSystem_CalcMoveDamage
    applies once the power is worked out and its multipliers are in (a
    doubling's POWER_MULTI, Flail's and Gyro Ball's figures): half again for
    a power of 60 or less, in whole numbers."""
    return power * 15 // 10 if att.ability == "Technician" and power <= 60 else power


def power_ratio(att, row, now):
    """How a hit at power `now` compares with its row, made at power `row`:
    now over row, with Technician judged at each, so its half again comes off
    a power that has passed 60 and goes on one that has fallen to 60. Until
    2026-10-14 a row's Technician stayed whatever the power became, so a
    Technician holder's Flail read at 300 near 1 HP where the engine gives
    200 (Ian approved the fix)."""
    return technician(att, now) / technician(att, row) if row > 0 else 1.0


def doubled_power(att, mv):
    """What a doubling of a move's power (the effect scripts' POWER_MULTI of
    20, or Assurance's doubled power) gives its hit: two, or less for a
    Technician holder whose row already had Technician's half and whose
    doubled power is past 60."""
    return power_ratio(att, mv.power, 2 * mv.power) if mv.power > 1 else 2


# The special moves that hit the target's Defense (BattleSystem_CalcMoveDamage).
AGAINST_DEFENSE = frozenset({"MOVE_PSYSHOCK", "MOVE_PSYSTRIKE", "MOVE_SECRET_SWORD"})


PLUS_MINUS = ("Plus", "Minus")


def plus_minus(b, att, mv):
    """Plus and Minus (BattleSystem_CalcMoveDamage, Generation 5's rule): half
    again to the holder's Sp. Atk for a special move while a partner on its
    side also has Plus or Minus, so never in a single battle. prepare()
    keeps both out of the calculator's rows (CALC_ABILITY_OFF), which raised
    every special move of a holder alone. Until 2026-10-14 the rows' boost
    stood in every battle (Ian approved the fix)."""
    if att.ability not in PLUS_MINUS or mv.cat != "Special" or not getattr(b, "doubles", False):
        return 1.0
    ally = ally_of(b, att)
    return 1.5 if ally is not None and ally.ability in ("Plus", "Minus") else 1.0


def partner_power(b, att, dfn, mv):
    """The partner abilities' factors on a double battle's hit
    (BattleSystem_CalcMoveDamage): Battery, on the attacker's standing
    partner, raises a special move's power by 13/10 after Technician (the
    holder's own moves only beside a second holder: the count of holders on
    its side must pass its own); Friend Guard, on the target's standing
    partner, cuts the damage to three quarters, unless the attacker's Mold
    Breaker gets past it. The calculator's rows have neither. Until
    2026-10-21 neither did anything (Ian approved the double-battle parts
    batch 11 left on 2026-10-14)."""
    m = 1.0
    if mv.cat == "Special":
        ally = ally_of(b, att)
        if ally is not None and ally.ability == "Battery":
            m *= 1.3
    guard = ally_of(b, dfn)
    if guard is not None and guard.ability == "Friend Guard" and not mold(att, guard):
        m *= 0.75
    return m


def marvel_scale(att, dfn, mv):
    """Marvel Scale's half again to its holder's Defense while it has a
    status (BattleSystem_CalcMoveDamage, which Mold Breaker gets past), for
    a hit on Defense: a physical one, or Psyshock's kind. The calculator's
    rows are made with no status, so they never carry it. The factor on the
    hit; until 2026-10-14 it was never applied (Ian approved the fix)."""
    if dfn.ability == "Marvel Scale" and dfn.status and not mold(att, dfn) \
            and (mv.cat == "Physical" or mv.const in AGAINST_DEFENSE):
        return 2 / 3
    return 1.0


# The moves whose power reads weights (weight_move_power), which an
# Autotomize changes as the fight runs.
WEIGHT_EFFECTS = frozenset({"INCREASE_POWER_WITH_WEIGHT", "HEAVY_SLAM"})
# The effects and the moves whose power state_mult sets from the battle's
# state, each looked for once.
STATE_POWER_EFFECTS = frozenset({"INCREASE_POWER_WITH_LESS_HP", "DECREASE_POWER_WITH_LESS_USER_HP",
                                 "POWER_BASED_ON_LOW_SPEED", "HIGHER_POWER_WHEN_LOW_PP",
                                 "INCREASE_POWER_WITH_MORE_HP", "INCREASE_POWER_WITH_MORE_STAT_UP"})
STATE_POWER_MOVES = frozenset({"MOVE_PAYBACK", "MOVE_STORED_POWER", "MOVE_POWER_TRIP", "MOVE_ELECTRO_BALL",
                               "MOVE_HARD_PRESS", "MOVE_LAST_RESPECTS"})


def state_mult(b, att, dfn, mv):
    """What a hit's row lacks as the fight runs: a pinch ability's 1.5 at a
    third of its HP or less; a resist berry gone (the row still halves the
    hit, so this doubles it back); Flail's power by HP (the row has full
    HP's 20); Water Spout's by HP (the row has full HP's 150); Gyro Ball's
    by the Speeds; a doubling for a Pokemon in the air, underground or
    underwater. Each power is judged for Technician (power_ratio)."""
    m = 1.0
    if PINCH_ABILITY.get(att.ability) == mv.type and att.hp * 3 <= att.maxhp:
        m *= 1.5
    if dfn.ability == "Marvel Scale":
        m *= marvel_scale(att, dfn, mv)      # 1 for any other ability, so looked at only for this one
    if dfn.ability == "Multiscale" and dfn.hp == dfn.maxhp and not mold(att, dfn):
        # BattleSystem_CalcMoveDamage halves the damage a Multiscale holder
        # takes at full HP, unless a Mold Breaker gets past it; the
        # calculator's Generation 4 path has no Multiscale. Each hit of a
        # move of several reads the HP it meets. Until 2026-10-20 it did
        # nothing (Ian approved the fix).
        m *= 0.5
    if att.ability in PLUS_MINUS:
        m *= plus_minus(b, att, mv)          # 1 for any other ability
    if b.doubles:
        m *= partner_power(b, att, dfn, mv)      # Battery's 13/10 and Friend Guard's three quarters
    berry = resist_berry(b, dfn, mv)
    if berry and not berry_works(b, dfn, berry):
        m *= 2               # the row's halving gone with the Berry, or held off by Unnerve
    # The powers the battle's state sets, by effect and by move, each
    # behind one look (STATE_POWER_EFFECTS, STATE_POWER_MOVES), as a move
    # has one effect and is one move.
    e = mv.effect
    if e in STATE_POWER_EFFECTS:
        if e == "INCREASE_POWER_WITH_LESS_HP":
            m *= power_ratio(att, 20, flail_power(att))
        elif e == "DECREASE_POWER_WITH_LESS_USER_HP":
            m *= power_ratio(att, 150, max(1, 150 * att.hp // att.maxhp))
        elif e == "POWER_BASED_ON_LOW_SPEED":
            # Gyro Ball: the row has its power at both Pokemon's starting Speeds;
            # the game takes the turn's, stages and paralysis in them, and so
            # does the trainer's AI (TrainerAI_CalcDamage's MOVE_GYRO_BALL case).
            m *= power_ratio(att, gyro_power(b.row_speed(dfn), b.row_speed(att)),
                             gyro_power(b.speed(dfn), b.speed(att)))
        elif e == "HIGHER_POWER_WHEN_LOW_PP":
            # Trump Card: the row has the calculator's full-PP 40 (Oxide's
            # profile); the power rises as the PP runs down (trump_card_power).
            # The trainer's AI gives it no figure (its listed power is 1). Until
            # 2026-10-15 every use hit at 40 (Ian approved the fix).
            m *= power_ratio(att, 40, trump_card_power(b, att, mv))
        elif e == "INCREASE_POWER_WITH_MORE_HP":
            # Crush Grip and Wring Out (effect script 237, BtlCmd_CalcWringOutPower):
            # 1 plus 120 times the target's HP over its maximum, in whole numbers;
            # the row is made at full HP's 121. The trainer's AI gives them no
            # figure (their listed power is 1). Until 2026-10-15 they hit at 121
            # whatever the target's HP (Ian approved the fix).
            m *= power_ratio(att, 121, 1 + 120 * dfn.hp // dfn.maxhp)
        elif e == "INCREASE_POWER_WITH_MORE_STAT_UP":
            # Punishment (effect script 245, BtlCmd_CalcPunishmentPower): 60
            # and 20 more for each stage the target has raised, accuracy and
            # evasion included, up to 200; the row is made at 60, with none
            # raised. Until 2026-10-15 it hit at 60 whatever the target's
            # stages (Ian approved the fix).
            m *= power_ratio(att, 60, min(200, 60 + 20 * sum(s for s in dfn.stages.values() if s > 0)))
    if (att.ability == "Sand Force" and b.weather == "Sand" and not weather_ignored(b)
            and mv.type in ("Ground", "Rock", "Steel")):
        # BattleSystem_CalcMoveDamage: Ground, Rock and Steel moves at 13/10
        # power in a sandstorm that Cloud Nine and Air Lock leave alone; the
        # calculator's Generation 4 path has no Sand Force. Until 2026-10-14
        # it did nothing (Ian approved the fix).
        m *= 1.3
    c = mv.const
    if c in STATE_POWER_MOVES:
        if c == "MOVE_PAYBACK":
            if b.row_speed(att) <= b.row_speed(dfn):
                # The calculator rows Payback at twice its power for a user no
                # faster than its target (gen4.js: turnOrder 'last'), and the battle
                # then doubles it again when the target has acted first. The engine
                # doubles it once, on the turn's own order (BtlCmd_CalcPaybackPower),
                # and the trainer's AI reckons it at its table power. So the row goes
                # back to that power here, Technician judged at each, and attack()
                # doubles it as the turn runs. Until 2026-10-14 a slower Payback user
                # hit at four times the power (Ian approved the fix).
                m *= power_ratio(att, 2 * mv.power, mv.power)
        elif c in ("MOVE_STORED_POWER", "MOVE_POWER_TRIP"):
            # BattleScript_ComputedMovePower: 20, and 20 more for each stage its
            # user has raised a stat, accuracy and evasion included; the row is
            # made with none raised. The trainer's AI reckons it the same way
            # (TrainerAI_ComputedMovePower). Until 2026-10-14 it hit at 20 power
            # whatever the stages (Ian approved the fix).
            m *= power_ratio(att, 20, 20 + 20 * sum(s for s in att.stages.values() if s > 0))
        elif c == "MOVE_ELECTRO_BALL":
            # The engine reads the Speeds the turn order was worked out from, its
            # stages, paralysis, Tailwind and items in them, as Gyro Ball does;
            # the row has its power at the two Pokemon's starting Speeds. Until
            # 2026-10-14 it kept the opening Speeds' power the whole fight (Ian
            # approved the fix).
            m *= power_ratio(att, electro_power(b.row_speed(att), b.row_speed(dfn)),
                             electro_power(b.speed(att), b.speed(dfn)))
        elif c == "MOVE_HARD_PRESS":
            # BattleScript_ComputedMovePower: up to 100 by the share of its HP
            # the target has left, at least 1; the row is made at full HP. Until
            # 2026-10-14 it hit at full power whatever the target's HP (Ian
            # approved the fix).
            m *= power_ratio(att, 100, max(1, 100 * dfn.hp // dfn.maxhp))
        elif c == "MOVE_LAST_RESPECTS":
            # BattleScript_ComputedMovePower: 50, and 50 more for each Pokemon
            # of its user's party that has fainted (fainted_party); the row is
            # made at 50. The trainer's AI reckons it the same way
            # (TrainerAI_ComputedMovePower). Until 2026-10-20 it hit at 50
            # whatever had fainted (Ian approved the fix on 2026-10-20).
            m *= power_ratio(att, 50, 50 + 50 * fainted_party(b, att))
    if (att.rare or dfn.rare) and (att.lightened or dfn.lightened) and mv.effect in WEIGHT_EFFECTS:
        # An Autotomize on either side: the power at the weights now, over
        # the rows' at the species' own (weight_move_power).
        m *= power_ratio(att, weight_move_power(b, att, dfn, mv, False), weight_move_power(b, att, dfn, mv, True))
    if att.ability in POWER_ABILITIES:
        m *= ability_power(b, att, mv)       # Analytic's 13/10, Flare Boost's half again (ability_power)
    if b.sporty:
        m *= sport_half(b, att, dfn, mv)     # Water Sport on the field halves a Fire move's power
    if b.split:
        m *= split_mult(att, dfn, mv)        # stats Guard Split or Power Split averaged (split_mult)
    if b.wonder_room:
        m *= room_mult(att, dfn, mv)         # the Defenses traded under Wonder Room (room_mult)
    if b.gravity and c == "MOVE_GRAV_APPLE":
        # BattleScript_ComputedMovePower: half as strong again while Gravity
        # is in force (since 2026-10-15, when Gravity began to run).
        m *= power_ratio(att, mv.power, mv.power * 15 // 10)
    if att.rare:
        if att.charged and move_type_used(att.ability, mv, att.ivs, att.item, weather_now(b)) == "Electric":
            # Charge: BattleSystem_CalcMoveDamage doubles an Electric move's
            # power while MOVE_EFFECT_CHARGE stands, after POWER_MULTI and
            # before Technician; the trainer's AI reckons it the same way.
            # Until 2026-10-15 Charge only raised Sp. Def (Ian approved the
            # fix).
            m *= power_ratio(att, mv.power, 2 * mv.power) if mv.power > 1 else 2
        if att.me_first:
            m *= 1.5             # a move Me First took, at half again its damage (me_first_move)
    if att.helped:
        # Helping Hand: BattleSystem_CalcMoveDamage raises the power by half
        # (15/10) after a doubling and before Technician (helping_hand).
        m *= power_ratio(att, mv.power, mv.power * 15 // 10) if mv.power > 1 else 1.5
    reach = reach_mult(mv, dfn) if dfn.charging is not None else 0     # 0 for a target not mid-move
    if not reach and b.doubles and (dfn.rare or dfn.charging is not None) and sky_airborne(b, dfn):
        reach = air_reach(mv)    # Gust and Twister double on a Sky Drop's pair in the air, as on a flier
    if reach > 1:
        # The effect scripts double the power (POWER_MULTI 20) before
        # Technician is judged; Magnitude, whose power is rolled, doubles.
        m *= power_ratio(att, mv.power, reach * mv.power) if mv.power > 1 else reach
    return m


# The abilities whose power the battle's state sets (ability_power).
POWER_ABILITIES = frozenset({"Analytic", "Flare Boost", "Toxic Boost"})


def ability_power(b, att, mv):
    """A power multiplier BattleSystem_CalcMoveDamage gives by an ability and
    the battle's state, after Technician, which the rows lack. Analytic:
    13/10 when every other Pokemon on the field has acted this turn, as
    the battle notes while such a holder's move runs (Battle.analytic,
    set by _use_move), Future Sight and Doom Desire apart, whose damage is
    worked out as they are used. Flare Boost: half again for a special
    move while its holder is burned. Until 2026-10-20 neither did anything
    (Ian approved the fix). Toxic Boost: half again for a physical move
    while its holder is poisoned or badly poisoned; until 2026-10-20 it did
    nothing either (Ian approved the fix)."""
    if att.ability == "Analytic":
        return 1.3 if b.analytic is att and mv.effect != FUTURE_SIGHT else 1.0
    if att.ability == "Flare Boost":
        return 1.5 if att.status == "brn" and mv.cat == "Special" else 1.0
    if att.ability == "Toxic Boost":
        return 1.5 if att.status in ("psn", "tox") and mv.cat == "Physical" else 1.0
    return 1.0


# Trump Card's power by the PP its slot has left once the use is paid
# (sCurrentPPScaledPower): 200 at none left, then 80, 60, 50, and 40 from
# four on.
TRUMP_CARD_POWER = (200, 80, 60, 50, 40)


def trump_card_power(b, att, mv):
    """Trump Card's power for this use (effect script 235,
    BtlCmd_CalcTrumpCardPower, which reads its slot's PP after the use has
    paid). Inside its user's action this turn the PP is paid already; a
    figure made before it, as a planner's, counts the one PP the use will
    take."""
    left = att.pp.get(mv.name, mv.pp)
    if getattr(att, "acted_turn", None) != b.turn:
        left -= 1
    return TRUMP_CARD_POWER[max(0, min(left, 4))]


# Electro Ball's power by how many whole times over the target's Speed is
# its user's (sElectroBallPower).
ELECTRO_BALL_POWER = (40, 60, 80, 120, 150)


def electro_power(user_speed, target_speed):
    """Electro Ball's power (BattleScript_ComputedMovePower): the user's
    Speed over the target's, in whole times, picks 40, 60, 80, 120 or 150,
    a target with no Speed giving 40."""
    ratio = user_speed // target_speed if target_speed else 0
    return ELECTRO_BALL_POWER[min(ratio, len(ELECTRO_BALL_POWER) - 1)]


def gyro_power(target_speed, user_speed):
    """Gyro Ball's power (BtlCmd_CalcGyroBallPower): 1 + 25 times the
    target's Speed over the user's, at most 150."""
    return min(150, 1 + 25 * target_speed // max(1, user_speed))


def after_hit(b, att, dfn, mv, dealt):
    """After a damaging hit (dealt > 0): a resist berry that halved it is
    used up; Rage raises its user's Attack when hit; Shell Bell gives back
    an eighth of the damage dealt. A move of several hits does the first two
    hit by hit (land_hits), so after it only shell_bell runs."""
    if dealt <= 0:
        return
    berry = resist_berry(b, dfn, mv)
    if berry_works(b, dfn, berry):
        consume(dfn)
    if dfn.raging and dfn.alive():
        change_stages(dfn, {"atk": 1})
    shell_bell(att, dealt)


def shell_bell(att, dealt):
    """Shell Bell gives back an eighth of the damage the whole move dealt,
    once it is over (shellBellDamageDealt adds up every hit)."""
    if dealt > 0 and att.item == "Shell Bell" and att.alive():
        heal(att, max(1, dealt // 8))


def hit_aftermath(b, att, dfn, mv, chance, pick):
    """What follows a damaging move's hit on dfn: after_hit and the target's
    on-hit ability for a move of one hit, then Dragon Tail's drag
    (drag_out); for one of several, whose hits land_hits took one at a time
    with their own aftermath, only the Shell Bell on their total."""
    if b.hits_landed:
        shell_bell(att, b.last_dealt)
        return
    after_hit(b, att, dfn, mv, b.last_dealt)
    contact_ability(b, att, dfn, mv, b.last_dealt, chance, pick)
    if mv.effect == "FORCE_SWITCH_HIT" and b.last_dealt > 0 and not b.sub_hit:
        # Dragon Tail and Circle Throw drag their target out once its own
        # ability and held items have answered the hit (the engine's
        # AFTER_MOVE_EFFECT_FORCE_SWITCH_HIT since 6809a5c4e, run after
        # TRIGGER_ITEMS_ON_HIT and before the Red Card and the Eject Button,
        # which the simulator does not hold). Until 2026-10-15 the drag came
        # first and the Pokemon dragged in answered (Ian approved the fix).
        drag_out(b, att, dfn, pick)


def confusion_blocked(b, att, dfn, hit=False):
    """Whether subscript_confuse keeps att's move from confusing dfn: Own
    Tempo, which a Mold Breaker attacker ignores (its message names it,
    though not for a hit's added confusion); a confusion already running;
    Safeguard on dfn's side, which an Infiltrator attacker passes
    (CheckSafeguard); and for a hit (`hit`) a Covert Cloak, as Shield Dust,
    which zeroes every added effect's chance, does. A Substitute has stopped
    the move before this. Until 2026-10-14 only Own Tempo stopped it, and
    not for a hit (Ian approved the fix)."""
    if dfn.ability == "Own Tempo" and att.ability != "Mold Breaker":
        if not hit:
            reveal(dfn)
        return True
    if dfn.confused:
        return True
    if hit and dfn.item == "Covert Cloak":
        return True
    side = b.p if dfn.side == "p" else b.b
    return bool(side.safeguard) and att.ability != "Infiltrator"


def confusion_berry(mon, b=None):
    """A Lum or Persim Berry cures confusion the moment it sets in, after
    the move (BattleSystem_TriggerHeldItemOnStatus), and is used up; the
    turn's end, which waited for it until 2026-10-14, is too late for a
    holder that moves after. Unnerve holds it (unnerved)."""
    if mon.confused and mon.item in ("Lum Berry", "Persim Berry") and not unnerved(b, mon):
        mon.confused = 0
        consume(mon)


def cure_berry(mon, b=None):
    """A status-curing berry (or Lum) cures the status it was just given,
    and is used up; Unnerve holds it (unnerved)."""
    if mon.status and mon.status in CURE_BERRY.get(mon.item, ()) and not unnerved(b, mon):
        mon.status, mon.sleep, mon.toxic = None, 0, 0
        consume(mon)


def synchronize(b, target, status):
    """Synchronize (subscript_poison, _badly_poison, _paralyze, _burn):
    a foe that gave its holder poison, bad poison (Oxide passes it on as
    bad poison), paralysis or a burn gets the same."""
    src = getattr(b, "status_src", None)
    if (target.ability == "Synchronize" and status in ("psn", "tox", "par", "brn") and src is not None
            and src.side != target.side and src.alive() and not src.status):
        b.status_src = None
        try:
            give_status(b, src, status)
        finally:
            b.status_src = src


def ability_trapped(b, mon):
    """Held in by the foe's ability (Battler_IsTrapped): Magnet Pull holds a
    Steel type, Shadow Tag anything without it, Arena Trap anything grounded:
    not a Flying type, a Levitate holder, an Air Balloon's or one under
    Magnet Rise, unless an Iron Ball brings it down. A Ghost type and a Shed
    Shell holder are never held (Oxide, Generation 6's rule). Until
    2026-10-14 the Ghost type, the Shed Shell and the Air Balloon were not
    exempt (Ian approved the fix)."""
    if "Ghost" in mon.types or mon.item == "Shed Shell":
        return False
    foe = foe_of(b, mon)
    if not foe.alive():
        return False
    if foe.ability == "Magnet Pull":
        return "Steel" in mon.types
    if foe.ability == "Shadow Tag":
        return mon.ability != "Shadow Tag"
    if foe.ability == "Arena Trap":
        if mon.item == "Iron Ball" or b.gravity:
            return True          # under Gravity, or an Iron Ball, it holds every foe
        return ((("Flying" not in mon.types and mon.ability != "Levitate") or mon.smacked) and not mon.magnet_rise
                and mon.item != "Air Balloon")     # a Pokemon Smack Down brought down is held (Oxide)
    return False


def commit_move(att, mv):
    """A move its user has committed to (its PP spent): Rage marks it to
    rise when hit, until it uses another move; Last Resort's record of the
    moves used since it came in; Truant loafs on its next turn. Whether
    Last Resort fails: until every other move it knows has been used since
    it came in."""
    att.raging = mv.effect == "RAISE_ATK_WHEN_HIT"
    fails = False
    if mv.effect == "FAIL_IF_NOT_USED_ALL_OTHER_MOVES":
        # The other moves are gathered only for Last Resort, the one move
        # whose use reads them.
        others = {m.name for m in att.moves if m.name != mv.name}
        fails = not others or not others <= att.used_moves
    # BattleSystem_UpdateLastResort's count, which the trainer's AI reads
    # (Expert_LastResort): each move other than Last Resort the first time it
    # is used since its user came in, four at most.
    if mv.effect != "FAIL_IF_NOT_USED_ALL_OTHER_MOVES" and mv.name not in att.used_moves and att.last_resort_count < 4:
        att.last_resort_count += 1
    if mv.name not in att.used_moves:
        att.used_moves = att.used_moves | {mv.name}    # a move already in the record leaves it as it is
    if att.ability == "Truant":
        att.loafing = True
    return fails


def loafs(att):
    """Truant: a turn after one it acted on, it loafs (BattleSystem_
    IsTruant's turn parity, reset as it comes in)."""
    if att.ability == "Truant" and att.loafing:
        att.loafing = False
        return True
    return False


def move_priority(mon, mv):
    """A move's priority as the engine reckons it for its user
    (Battler_MovePriority): one more for Prankster on a status move, and for
    Gale Wings on a Flying move at full HP."""
    pri = mv.pri
    if mon.ability == "Prankster" and mv.cat == "Status":
        pri += 1
    if mon.ability == "Gale Wings" and mv.type == "Flying" and mon.hp == mon.maxhp:
        pri += 1
    return pri


def sub_blocks(att, dfn, mv=None):
    """Whether dfn's Substitute stands between att's move and dfn: its hit,
    its status move and the move's own added effects. An Infiltrator
    attacker passes another Pokemon's Substitute with any move but Transform
    and Sky Drop (BattleSystem_InfiltratorPasses, on main-engine-cleanups);
    a Pokemon's own Substitute is never passed, and an ability's, an item's
    or Toxic Spikes' effect never passes (give_status_by_move)."""
    if not dfn.sub:
        return False
    passes = (att is not dfn and att.ability == "Infiltrator"
              and (mv is None or mv.name not in ("Transform", "Sky Drop")))
    return not passes


# The stage a charging move raises, on its charge turn or when its charge is
# skipped (effect scripts 145, 324 and 325, and their Power Herb and rain
# subscripts, which raise it too): Skull Bash's Defense, Meteor Beam's and
# Electro Shot's Sp. Atk.
CHARGE_STAGES = {"CHARGE_TURN_DEF_UP": {"def": 1}, "CHARGE_TURN_SP_ATK_UP": {"spa": 1},
                 "CHARGE_TURN_SP_ATK_UP_RAIN_SKIPS": {"spa": 1}}


def weather_ignored(b):
    """Cloud Nine or Air Lock on the field (CheckIgnoreWeather)."""
    return any(m.alive() and m.ability in ("Cloud Nine", "Air Lock") for m in b.p.on_field() + b.b.on_field())


def weather_now(b):
    """The weather as its effects read it: none while Cloud Nine or Air Lock
    is out (NO_CLOUD_NINE), in a fight with either (Battle.cloudy)."""
    return None if b.cloudy and b.weather is not None and weather_ignored(b) else b.weather


def fog_cut(b):
    """Deep fog's cut to a move's accuracy (BattleControllerPlayer_CheckMoveHitAccuracy,
    under FIELD_CONDITION_DEEP_FOG and NO_CLOUD_NINE): six tenths, after the
    stages, Compound Eyes, Sand Veil and Snow Cloak and before Hustle,
    Tangled Feet and the items; nothing while Cloud Nine or Air Lock is out.
    A fight on a foggy map starts in it (subscript_overworld_fog). Until
    2026-10-15 the fog cut nothing, and no fight carried it (Ian approved
    the fix)."""
    return 1.0 if weather_ignored(b) else 0.6


def charge_skipped(b, att, mv):
    """Whether a two-turn move strikes at once: SolarBeam in sun; Electro
    Shot in rain unless Cloud Nine or Air Lock is out, raising Sp. Atk
    (subscript_sp_atk_up_rain_skip); else a Power Herb, spent, raising the
    move's charge stage (subscript_power_herb_skull_bash and _meteor_beam)."""
    if mv.effect in ("SOLAR_BEAM", "SKIP_CHARGE_TURN_IN_SUN") and b.weather == "Sun" and not weather_ignored(b):
        return True
    if mv.effect == "CHARGE_TURN_SP_ATK_UP_RAIN_SKIPS" and b.weather == "Rain" and not weather_ignored(b):
        change_stages(att, CHARGE_STAGES[mv.effect])
        return True
    if att.item == "Power Herb":
        consume(att)
        change_stages(att, CHARGE_STAGES.get(mv.effect, {}))
        return True
    return False


@functools.lru_cache(maxsize=None)
def heal_blocked_moves():
    """The moves Heal Block stops (battle_lib.c, sMovesAffectedByHealBlock):
    they cannot be chosen and fail if used (Move_HealBlocked)."""
    with open(os.path.join(data.ROOT, "src", "battle", "battle_lib.c"), encoding="utf-8") as fh:
        body = re.search(r"sMovesAffectedByHealBlock\[\] = \{(.*?)\};", fh.read(), re.S).group(1)
    return frozenset(re.findall(r"MOVE_\w+", body))


def heal_blocked(mon):
    """Whether Heal Block runs on mon (moveEffectsData.healBlockTurns): its
    healing moves, its draining, Leech Seed's heal for it, Wish's, Ingrain's
    and Aqua Ring's all fail; held items and abilities still heal."""
    return getattr(mon, "heal_block", 0) > 0


def move_heal_blocked(mon, mv):
    return heal_blocked(mon) and mv.const in heal_blocked_moves()


def start_heal_block(att, dfn, mv):
    """Heal Block, and Psychic Noise's added effect (subscript_heal_block_start):
    five turns, failing on a Substitute (an Infiltrator's passes) or on a
    Pokemon already blocked."""
    if dfn.alive() and not heal_blocked(dfn) and not sub_blocks(att, dfn, mv):
        dfn.heal_block = 5


def give_status_by_move(b, att, dfn, mv, status):
    """give_status for a status that att's move gives dfn, the one path on
    which an Infiltrator passes dfn's Substitute (can_status reads
    b.passing_sub, set only here and only for the call)."""
    b.passing_sub = dfn if dfn.sub and not sub_blocks(att, dfn, mv) else None
    # An Infiltrator's move passes Safeguard too (CheckSafeguard,
    # BattleSystem_InfiltratorPassesEffect), read by can_status.
    b.passing_safeguard = dfn if att is not dfn and att.ability == "Infiltrator" else None
    try:
        return give_status(b, dfn, status)
    finally:
        b.passing_sub = b.passing_safeguard = None


def move_fails_first(att, mv, dfn, first):
    """The reworked moves that fail before they hit (effects 418 and 419).
    Upper Hand needs its target to have chosen a move of raised priority and
    not to have acted yet (TryUpperHand); Shell Trap, moving last, needs a
    physical move to have hit its user this turn (a Substitute's hit does
    not count, as the physical damage mask leaves it out)."""
    if mv.effect == "UPPER_HAND":
        nxt = getattr(dfn, "chosen", None)
        return not first or nxt is None or move_priority(dfn, nxt) <= 0
    if mv.effect == "SHELL_TRAP":
        hit = att.hit_this_turn
        return not hit or hit[0] != "Physical" or not hit[1]
    return False


@functools.lru_cache(maxsize=None)
def reckless_effects():
    """The effects whose power Reckless raises by 1.2 in the game: every
    effect script that sets BTLVAR_POWER_MULTI to 12 for ABILITY_RECKLESS
    (battle_lib.c applies it as power * 12 / 10), named by its number in
    generated/move_battle_effects.txt. Since the move reworks these include
    Hyper Beam's kin, the starter ultimates, Sky Attack, Thrash, Outrage and
    Raging Fury."""
    with open(os.path.join(data.ROOT, "generated", "move_battle_effects.txt"), encoding="utf-8") as fh:
        names = [line.strip()[len("BATTLE_EFFECT_"):] for line in fh if line.strip()]
    out = set()
    scripts = os.path.join(data.ROOT, "res", "battle", "scripts", "effects")
    for fn in os.listdir(scripts):
        m = re.fullmatch(r"effect_script_(\d+)\.s", fn)
        if m and int(m.group(1)) < len(names):
            with open(os.path.join(scripts, fn), encoding="utf-8") as fh:
                if "ABILITY_RECKLESS" in fh.read():
                    out.add(names[int(m.group(1))])
    return frozenset(out)


# The moves whose Reckless boost an OxiDex calculator without the game's own
# list gives anyway (upstream's data marks them as recoil or crash moves),
# measured 2026-10-07 by costing each move on a Reckless effect for one
# Staraptor with Reckless and with Intimidate.
CALC_RECKLESS = frozenset({
    "Axe Kick", "Brave Bird", "Double-Edge", "Flare Blitz", "Head Charge", "Head Smash", "High Jump Kick",
    "Jump Kick", "Light of Ruin", "Submission", "Supercell Slam", "Take Down", "Volt Tackle", "Wave Crash",
    "Wild Charge", "Wood Hammer"})
CALC_DATA = os.path.join("tools", "oxide", "encounters", "calc", "calc", "mechanics", "romhacks", "profiles",
                         "platinum-oxide-data.js")


@functools.lru_cache(maxsize=None)
def calc_reckless():
    """The moves the calculator's rows already boost for Reckless. Since the
    encounter track's c5aed2a7bf (2026-10-07) the calculator's Platinum Oxide
    profile reads a "reckless" list that make_calc_mechanics writes from the
    game's own effect scripts, and boosts exactly those; before it, upstream's
    recoil and crash moves (CALC_RECKLESS). Read from the tree either way, so
    the simulator adds the 1.2 only where the calculator does not, whichever
    lands first (test_plfixes re-measures it)."""
    try:
        with open(os.path.join(data.ROOT, CALC_DATA), encoding="utf-8") as fh:
            m = re.search(r'"reckless":\s*\[(.*?)\]', fh.read(), re.S)
    except OSError:
        m = None
    return frozenset(re.findall(r'"([^"]+)"', m.group(1))) if m else CALC_RECKLESS


def reckless_fix(att, mv):
    """The 1.2 Reckless gives a move the calculator's row leaves unboosted."""
    if att.ability == "Reckless" and mv.effect in reckless_effects() and mv.name not in calc_reckless():
        return 1.2
    return 1.0


def use_damage(att, mv, dmg, hits):
    """A row's damage as this use deals it: its hits (scale_hits) and the
    Reckless boost the calculator misses (reckless_fix)."""
    dmg = scale_hits(att, mv, dmg, hits)
    fix = reckless_fix(att, mv)
    return dmg if fix == 1.0 else int(dmg * fix)


def scale_hits(att, mv, dmg, hits):
    """A row's damage for the hits this use rolled: a two to five hit move's
    row counts row_hits hits, a rising move's all three."""
    if mv.effect in RISING:
        return int(dmg * rising_scale(mv, hits))
    rh = row_hits(att, mv)
    if mv.effect == "MULTI_HIT" and hits != rh:
        return dmg * hits // rh
    return dmg


def multi_hit_odds(att, mv):
    """[(hits, weight)] for a two to five hit move, and for a Loaded Dice
    holder's Population Bomb (TEN_LOADED); else None."""
    if mv.effect != "MULTI_HIT":
        return TEN_LOADED if mv.effect == TEN_HITS and att.item == "Loaded Dice" else None
    if att.ability == "Skill Link":
        return ((5, 1),)
    if att.item == "Loaded Dice":
        return ((4, 1), (5, 1))
    return MULTI_HIT_ODDS


def row_hits(att, mv):
    """The hits a calculator row adds up for this move (calc_headless.js
    rolls(), move.js): a two to five hit move at its lowest plus one, or its
    most with Skill Link or a Grip Claw; Double Kick's kind at two
    (TWO_HITS, Twineedle and Double Iron Bash with it); Triple Dive's at
    three (THREE_HITS); else one. The trainer's AI divides its row by this
    to get one hit, as the game's estimate starts, then counts the move's
    hits (fightai.expected_hits). Until 2026-10-21 Twineedle and Double
    Iron Bash counted one here, though their rows add up two, so the AI
    rated Twineedle on both its hits where the game rated one; nothing
    else read the count for them (hit_weights gives them two)."""
    if mv.effect == "MULTI_HIT":
        return 5 if att.ability == "Skill Link" or att.item == "Grip Claw" else 3
    if mv.effect in THREE_HITS:
        return 3             # Triple Dive's kind (calc's multihit 3)
    if mv.effect == TEN_HITS:
        # Population Bomb (calc's multihit [1, 10]): two, ten for Skill Link
        # or a Grip Claw, which the engine's hits do not follow (TEN_HITS)
        return 10 if att.ability == "Skill Link" or att.item == "Grip Claw" else 2
    return 2 if mv.effect in TWO_HITS else 1


def rising_scale(mv, hits):
    """A rising move's damage over `hits` hits, as a share of its row, which
    adds up all three (rising_powers). Until 2026-10-12 this read the row as
    the first hit alone, so once the calculator began adding the three
    (2026-10-07) Fury Cutter dealt about four times its damage (Ian approved
    the fix)."""
    powers = rising_powers(mv)
    return sum(powers[:hits]) / sum(powers)


def expected_hit_scale(mv, att=None):
    """A move's expected damage as a multiple of its calculator row, for the
    reckonings that read rows (exp_damage, plfeat._expected), before the
    first hit's accuracy: a rising move's later hits each need accuracy
    again, and its row adds all three (Triple Axel's too since 2026-10-14).
    A two to five hit move's row counts three hits, close to its expected
    3.1, so it is left as it is. Population Bomb's ten hits each need the
    accuracy after the first, seven on average with a Loaded Dice, over
    the row's two, or ten for a Skill Link or Grip Claw holder (`att`, an
    object with its ability and item, or None for neither)."""
    if mv.effect == TEN_HITS:
        acc = 1.0 if mv.acc == 0 else min(1.0, mv.acc / 100)
        hits = 7.0 if getattr(att, "item", None) == "Loaded Dice" else sum(acc ** i for i in range(10))
        return hits / (row_hits(att, mv) if att is not None else 2)
    if mv.effect not in RISING:
        return 1.0
    acc = 1.0 if mv.acc == 0 else min(1.0, mv.acc / 100)
    powers = rising_powers(mv)
    return sum(p * acc ** i for i, p in enumerate(powers)) / sum(powers)


@functools.lru_cache(maxsize=None)
def sheer_force_effects():
    """The effects whose secondary effect Sheer Force strips (and whose
    power it raises, which the calculator's own copy of this list does),
    read from the game's list (battle_lib.c, sSheerForceEffects); a recoil
    stays. Names as Move.effect gives them."""
    with open(os.path.join(data.ROOT, "src", "battle", "battle_lib.c"), encoding="utf-8") as fh:
        body = re.search(r"sSheerForceEffects\[\] = \{(.*?)\};", fh.read(), re.S).group(1)
    return frozenset(re.findall(r"BATTLE_EFFECT_(\w+)", body))


@functools.lru_cache(maxsize=None)
def sheer_force_keep_moves():
    """The moves Sheer Force strengthens that keep their effect, as in
    hg-engine (battle_lib.c, sSheerForceKeepEffectMoves): MOVE_ constants."""
    with open(os.path.join(data.ROOT, "src", "battle", "battle_lib.c"), encoding="utf-8") as fh:
        body = re.search(r"sSheerForceKeepEffectMoves\[\] = \{(.*?)\};", fh.read(), re.S).group(1)
    return frozenset(re.findall(r"MOVE_\w+", body))


def sheer_force_strips(att, mv):
    """Whether this hit's secondary effect is stripped by its user's Sheer
    Force (Battler_SheerForceStrips): an effect on the game's list, unless
    the move keeps its effect."""
    return (att.ability == "Sheer Force" and mv.const not in sheer_force_keep_moves()
            and mv.effect in sheer_force_effects())


def sheer_force_active(att, mv):
    """Whether Sheer Force boosts this hit (Battler_SheerForceActive): it
    strips the effect, or the move keeps its effect under Sheer Force. While
    it is active a Life Orb takes no recoil (Ian, 2026-10-07)."""
    return sheer_force_strips(att, mv) or (att.ability == "Sheer Force" and mv.const in sheer_force_keep_moves())


@functools.lru_cache(maxsize=None)
def permanent_trick_room():
    """The trainers whose battles open in a Trick Room that lasts the whole
    fight, read from the game's own list (battle_lib.c,
    sPermanentTrickRoomTrainers), so a reading follows the tree it runs in."""
    with open(os.path.join(data.ROOT, "src", "battle", "battle_lib.c"), encoding="utf-8") as fh:
        body = re.search(r"sPermanentTrickRoomTrainers\[\] = \{(.*?)\};", fh.read(), re.S).group(1)
    return frozenset(c for c in re.findall(r"TRAINER_\w+", body) if c != "TRAINER_NONE")


def trick_room_for(constants, flag=False):
    """Whether a fight against these trainers (their TRAINER_ constants)
    opens in the permanent room: one of them is on the game's list, or the
    fight's own trick_room flag in fights.json is set."""
    return bool(flag) or any(c in permanent_trick_room() for c in constants)


def custap_fires(mon, b=None):
    """A Custap Berry puts its holder first in its priority bracket, like a
    Quick Claw that always fires, at a quarter of its HP or less (half with
    Gluttony), once (HOLD_EFFECT_PINCH_PRIORITY), unless Unnerve holds it
    (BattleSystem_CompareBattlerSpeed asks BerryBlockedByUnnerve)."""
    return (mon.item == "Custap Berry" and mon.alive()
            and mon.hp * (2 if mon.ability == "Gluttony" else 4) <= mon.maxhp and not unnerved(b, mon))


def knockout_boost(att, dfn, before):
    """Moxie and Beast Boost after a move (BtlCmd_TryBeastBoost, run from
    subscript_faint_check_destiny_bond once Destiny Bond has had its turn):
    when att's move took HP from dfn and fainted it (`before`, its HP as the
    move began) and att still stands, Moxie raises att's Attack a stage and
    Beast Boost its highest stat, Attack, Defense, Sp. Atk, Sp. Def then
    Speed winning a tie, by the stats without stages; nothing at +6.
    Until 2026-10-14 neither did anything (Ian approved the fix)."""
    if att.ability not in ("Moxie", "Beast Boost") or att is dfn or not att.alive():
        return
    if dfn.alive() or before <= 0:
        return
    if att.ability == "Moxie":
        stat = "atk"
    else:
        order = ("atk", "def", "spa", "spd", "spe")
        stat = max(order, key=lambda s: (att.stats.get(s, 0), -order.index(s)))
    if att.stages[stat] < 6:
        change_stages(att, {stat: 1})
        reveal(att)


# The hits whose own effect waits for the hit to be in and reads how it
# left its target, each looked at once by effect (late_hit).
LATE_HIT = frozenset({"FELL_STINGER", "PREVENT_ESCAPE_HIT"})


def late_hit(b, att, dfn, mv, stripped, dealt):
    """A hit's own effect once it is in, for the effects in LATE_HIT, run
    before the knockout and Substitute checks that end the others; dealt is
    the HP the hit took from dfn itself, 0 when its Substitute took it.

    Fell Stinger (effect script 388, subscript_fell_stinger, ON_HIT): when
    its hit leaves the target with no HP, its user's Attack rises three
    stages through the stat subscript; a Substitute's hit leaves the target
    standing.

    Anchor Shot, Spirit Shackle and Thousand Waves (effect script 351,
    subscript_prevent_escape_hit, ON_HIT): a target left standing that
    nothing holds yet is held as Mean Look holds it, until the user leaves
    (trapped_by). CheckSubstitute stops it for a hit that met a Substitute,
    one it broke too (SELF_TURN_FLAG_SUBSTITUTE_HIT), so only a hit on the
    target itself traps. Shield Dust does not stop it; Sheer Force strips
    Thousand Waves' and leaves the other two theirs (sSheerForceEffects,
    sSheerForceKeepEffectMoves). A Ghost type held so can still switch
    (untrappable).

    Until 2026-10-15 both were plain hits (Ian approved the fixes)."""
    e = mv.effect
    if e == "FELL_STINGER":
        if not dfn.alive():
            change_stages(att, {"atk": 3})
    elif e == "PREVENT_ESCAPE_HIT":
        if not stripped and dealt > 0 and dfn.alive() and dfn.trapped_by is None:
            dfn.trapped_by = att.key


# The hits whose own effect runs ON_HIT on any hit, a knockout's or a
# Substitute's included, each looked at once by effect (any_hit).
ANY_HIT = frozenset({"RECOIL_HALF_MAX_HP", "RESET_STAT_CHANGES_HIT", "SET_LIGHT_SCREEN_HIT", "SET_REFLECT_HIT",
                     "STEALTH_ROCK_HIT", "SET_SPIKES_HIT"})
# The screen each screen-raising hit puts up on its user's side (any_hit).
HIT_SCREENS = {"SET_LIGHT_SCREEN_HIT": "Light Screen", "SET_REFLECT_HIT": "Reflect"}


def any_hit(b, att, dfn, mv):
    """A hit's own effect for the effects in ANY_HIT, once the hit is in,
    before the knockout and Substitute checks that end the others.

    Chloroblast (effect script 403, subscript_recoil_half_max_hp, ON_HIT
    on its user): the user loses half its maximum HP, rounded up; Magic
    Guard spares it and Rock Head does not, as it is a cost rather than
    recoil from the damage. Its script's Reckless 1.2 is in the row (the
    calculator's Oxide profile). Until 2026-10-20 it cost nothing (Ian
    approved the fix).

    Freezy Frost (effect script 313, subscript_reset_all_stat_stages,
    ON_HIT with no Pokemon of its own): Haze's command resets every
    Pokemon on the field (reset_all_stats). Until 2026-10-20 every stage
    stayed (Ian approved the fix).

    Glitzy Glow and Baddy Bad (effect scripts 311 and 312,
    subscript_light_screen and subscript_reflect, ON_HIT): the screen goes
    up on the user's side for five turns, eight with a Light Clay, as the
    status moves raise it (BtlCmd_TryLightScreen, BtlCmd_TryReflect); one
    already up stays as it is, and the move, which has done its damage, has
    not failed. Until 2026-10-20 no screen went up (Ian approved the
    fixes).

    Stone Axe and Ceaseless Edge (effect scripts 353 and 354,
    subscript_set_stealth_rock and subscript_set_spikes, ON_HIT): Stealth
    Rock goes down on the target's side unless it is there already, and a
    layer of Spikes, up to three (BtlCmd_TrySpikes). Both moves keep the
    effect under Sheer Force, which strengthens them
    (sSheerForceKeepEffectMoves; the calculator's row has the 1.3). Until
    2026-10-20 neither laid anything (Ian approved the fixes)."""
    e = mv.effect
    if e == "RECOIL_HALF_MAX_HP":
        if att.ability != "Magic Guard":
            hurt(b, att, (att.maxhp + 1) // 2)
    elif e == "RESET_STAT_CHANGES_HIT":
        reset_all_stats(b)
    elif e in HIT_SCREENS:
        side = b.p if att.side == "p" else b.b
        if not side.screens[HIT_SCREENS[e]]:
            side.screens[HIT_SCREENS[e]] = 8 if att.item == "Light Clay" else 5
    elif e == "STEALTH_ROCK_HIT":
        (b.p if dfn.side == "p" else b.b).hazards["rocks"] = 1
    elif e == "SET_SPIKES_HIT":
        side = b.p if dfn.side == "p" else b.b
        side.hazards["spikes"] = min(3, side.hazards["spikes"] + 1)


def reset_all_stats(b):
    """BtlCmd_ResetAllStatChanges: every Pokemon on the field, on both
    sides, back to no stat stages, and its Focus Energy gone (crit_stage,
    VOLATILE_CONDITION_FOCUS_ENERGY here). Haze (effect script 25) and
    Freezy Frost's hit (313) run it through subscript_reset_all_stat_stages.
    Until 2026-10-20 Haze reset only its user and its target, the two
    Pokemon of a single battle but not the four of a double, and left
    Focus Energy (Ian approved the fix)."""
    for m in b.p.on_field() + b.b.on_field():
        m.stages = dict.fromkeys(STAGE_KEYS, 0)
        m.crit_stage = 0


def jaw_lock(att, dfn):
    """Jaw Lock (effect script 352, subscript_jaw_lock, ON_HIT): once its
    hit is in, the target and the user each hold the other as Mean Look
    holds, until one of them leaves (trapped_by). The callers come here only
    for a target left standing with no Substitute in the way, the one the
    hit broke included (CheckSubstitute reads SELF_TURN_FLAG_SUBSTITUTE_HIT).
    A Pokemon already held keeps its first holder: when the user is held
    already only the target is held, and when the target is, only the user.
    A chance-free effect off sSheerForceEffects, so Shield Dust and Sheer
    Force leave it alone; a Ghost type or a Shed Shell holder held so can
    still switch (untrappable). Until 2026-10-20 it was a plain hit (Ian
    approved the fix)."""
    if att.trapped_by is not None:
        if dfn.trapped_by is None:
            dfn.trapped_by = att.key
    elif dfn.trapped_by is not None:
        att.trapped_by = dfn.key
    else:
        att.trapped_by, dfn.trapped_by = dfn.key, att.key


def grudge(att, dfn, paid, mv):
    """After a move, for a target under Grudge (effect script 194 sets
    MOVE_EFFECT_GRUDGE; BtlCmd_TryGrudge, run from
    subscript_faint_check_destiny_bond and U-turn's subscript): if the move
    knocked it out and its user still stands on the other side, the move in
    the user's slot that paid for this one (paid, the slot's move whatever
    it called) loses all its PP, unless the move was Struggle. The mark is
    set until its user next tries to act or leaves. Until 2026-10-15
    Grudge did nothing (Ian approved the fix)."""
    if not dfn.alive() and att.alive() and att.side != dfn.side and mv.effect != "STRUGGLE":
        att.pp[paid.name] = 0


def destiny_bond(att, dfn):
    """After a move: if it fainted a Pokemon under Destiny Bond and its user
    still stands on the other side, the user faints too
    (subscript_faint_check_destiny_bond). The bond is set by the move
    (subscript_destiny_bond) and cleared when its user next tries to act
    (BattleControllerPlayer_CheckStatusDisruption) or switches out."""
    if dfn.destiny_bond and not dfn.alive() and att.alive() and att.side != dfn.side:
        att.hp = 0


# The effects whose hit ends its target's protection for the rest of the turn
# (subscript_feint, run on the hit): Feint and Hyperspace Hole, the strike of
# Shadow Force and Phantom Force, and Hyperspace Fury.
BREAKS_PROTECT = frozenset({"REMOVE_PROTECT", "SHADOW_FORCE", "USER_DEF_DOWN_HIT_REMOVE_PROTECT"})
# Protect's run of successes counts no higher than this (sProtectSuccessRate's
# last row): a fourth Protect in a row, and every one after, works one time
# in eight.
PROTECT_RUN_CAP = 3
# The side guards that keep Protect's run going and add to it, as Protect
# and Endure do (Move_KeepsProtectRun); Mat Block and Crafty Shield neither
# keep it nor add to it.
KEEPS_PROTECT_RUN = frozenset({"MOVE_WIDE_GUARD", "MOVE_QUICK_GUARD"})


def protected(b, att, mv, dfn):
    """Whether dfn's Protect stops att's move, as
    BattleControllerPlayer_CheckMoveHitOverrides decides: only a move flagged
    MOVE_FLAG_CAN_PROTECT, so Feint, Shadow Force, Phantom Force, Future
    Sight, Curse, the hazards and the rest pass it. A stopped move lets go
    of its user's lock (Battler_UnlockMoveChoice ends a Rollout's run); a
    contact move stopped by Spiky Shield costs its user an eighth of its
    maximum HP unless it has Magic Guard, one stopped by Baneful Bunker
    poisons a user with no status, and one stopped by Burning Bulwark burns
    it (subscript_missed, since 2026-10-14 for Burning Bulwark: the burn
    subscript stops it at a Fire type, a user behind its own Substitute or
    under Safeguard, and Water Veil, Water Bubble, Purifying Salt and Leaf
    Guard in sun, which give_status reads; the burned user is the attacker
    there, so a Mold Breaker never gets past those). Oxide's other
    protecting moves (King's Shield, Obstruct, Silk Trap) only protect.
    Until 2026-10-14 Protect stopped every move but Feint (Ian approved the
    fix)."""
    if not dfn.protecting or not mv.protect:
        return b.guarded and mv.protect and guard_stops(b, att, mv, dfn)
    rollout_after(att, mv, False)
    guard = dfn.last.name if dfn.last is not None else None
    if makes_contact(att, mv) and att.alive():
        if guard == "Spiky Shield" and att.ability != "Magic Guard":
            hurt(b, att, max(1, att.maxhp // 8))
        elif guard == "Baneful Bunker" and not att.status:
            b.status_src = dfn
            give_status(b, att, "psn")
        elif guard == "Burning Bulwark" and not att.status:
            b.status_src = dfn               # Synchronize passes it back, as in the engine
            give_status(b, att, "brn")
    return True


def side_guard(b, att, mv, first):
    """Wide Guard, Quick Guard, Mat Block and Crafty Shield (effect script
    371, BtlCmd_TryProtection's side guard): it fails when no battler acts
    after its user (moves_last), and Mat Block on any turn but its user's
    first out, as Fake Out's test has it; otherwise it never rolls against
    Protect's run and guards its user's side for the rest of the turn
    (guard_stops). A failure ends the run; Wide Guard and Quick Guard add to
    it. Until 2026-10-15 the four did nothing (Ian approved the fix)."""
    if moves_last(b, first) or (mv.const == "MOVE_MAT_BLOCK" and att.turns_in > 0):
        att.protect_run = 0
        return
    side = b.p if att.side == "p" else b.b
    side.guard = mv.const
    b.guarded = True
    if mv.const in KEEPS_PROTECT_RUN:
        att.protect_run = min(att.protect_run + 1, PROTECT_RUN_CAP)


def guard_stops(b, att, mv, dfn):
    """Whether a side guard on dfn's side stops att's move, which can be
    protected against (BattleControllerPlayer_SideGuardAgainst): Wide Guard
    a move that hits more than one target (by its range, so in a single
    battle too), Quick Guard a move of raised priority (Prankster and Gale
    Wings counting), Mat Block a damaging move, Crafty Shield a status move
    aimed at someone other than its user. A stopped move lets go of its
    user's lock, as Protect's does; the guard's side takes nothing from it.
    In a double battle the side's guard covers both its Pokemon, as the
    engine's check reads the defender's and its partner's."""
    g = (b.p if dfn.side == "p" else b.b).guard
    if g is None:
        return False
    if g == "MOVE_WIDE_GUARD":
        stop = mv.range in SPREAD
    elif g == "MOVE_QUICK_GUARD":
        stop = move_priority(att, mv) > 0
    elif g == "MOVE_MAT_BLOCK":
        stop = mv.cat != "Status"
    else:
        stop = mv.cat == "Status" and att is not dfn
    if stop:
        rollout_after(att, mv, False)
    return stop


def moves_last(b, first):
    """Whether no battler acts after this one this turn (BtlCmd_TryProtection's
    waitingBattlers of 1): a double battle marks it as each acts
    (run_doubles), and in a single battle it is the move whose target has
    already moved, or that has no move against it."""
    last = getattr(b, "moving_last", None)
    return (not first) if last is None else last


def protect_odds(att):
    """The chance a Protect, Detect or Endure works after att's run of
    successes (sProtectSuccessRate): certain, then a half, a quarter and an
    eighth, which stays the floor."""
    return 1 / (2 ** min(att.protect_run, PROTECT_RUN_CAP))


def out_of_reach(att, dfn, mv):
    """Whether dfn is in the air, underground or underwater where mv cannot
    reach it (MOVE_STATUS_SEMI_INVULNERABLE), as a hit's check has it."""
    return (dfn.charging is not None and dfn.charging.effect in INVULNERABLE and not reaches(mv, dfn)
            and not lands_sure(att, dfn, mv))


# The status moves whose effect scripts set every SYSCTL_HIT_DURING flag, so
# that they reach a target on its hidden turn: Memento (effect script 168).
# Helping Hand's script (176) sets them too, but it aims at an ally, whom the
# check below never reaches.
REACHES_VANISHED = frozenset({"FAINT_AND_ATK_SP_ATK_DOWN_2"})


def status_out_of_reach(att, dfn, mv):
    """BattleControllerPlayer_CheckMoveHitOverrides for a status move: one
    aimed at a foe misses it on the hidden turn of Fly, Bounce, Shadow Force
    or Phantom Force (MOVE_STATUS_SEMI_INVULNERABLE), unless No Guard is on
    either side (out_of_reach) or its script reaches there (REACHES_VANISHED).
    A move whose defender is its own user (OWN_RANGES) never meets the check,
    and one aimed at the foe's side (Spikes, Stealth Rock) passes it. Dig and
    Dive are one-turn hits in Oxide's move data (the move reworks), so no
    Pokemon is ever underground or underwater. Until 2026-10-14 every status
    move reached a hidden target (Ian approved the fix)."""
    return (mv.range not in OWN_RANGES and mv.range != "OPPONENT_SIDE" and mv.effect not in REACHES_VANISHED
            and out_of_reach(att, dfn, mv))


# The status moves that change a type or an ability: each effect's function
# of (battle, user, move, target, pick), pick(kind, n) the battle's dice for
# a choice among n; both battles' status_move run them.
FORM_MOVES = {}


def form_move(effect):
    def add(fn):
        FORM_MOVES[effect] = fn
        return fn
    return add


@form_move("CHANGE_TO_WATER_TYPE")
def soak(b, att, mv, dfn, pick):
    """Soak (effect script 284, subscript_change_target_to_water_type): its
    target becomes pure Water until it leaves, unless the move cannot reach
    it, a Substitute stands in front of it, its ability is Multitype, or it
    is pure Water already. Its rows then come from its Water twin (form_key).
    Until 2026-10-14 Soak did nothing (Ian approved the fix)."""
    if out_of_reach(att, dfn, mv) or sub_blocks(att, dfn, mv) or dfn.ability == "Multitype" or dfn.types == ["Water"]:
        return False
    set_types(dfn, ["Water"])
    return True


@form_change
def _soaked(ff):
    """Soak: any foe of a Soak user but a pure Water one or a Multitype one
    may be made pure Water."""
    for k in ff.keys():
        if any(m.effect == "CHANGE_TO_WATER_TYPE" for m in ff.moves(k)):
            for f in ff.foes(k):
                if ff.types(f) != ["Water"] and ff.ability(f) != "Multitype":
                    yield f, ["Water"], ff.ability(f)


def conversion_type(mv, types):
    """The type Conversion reads for one of its user's moves (BtlCmd_TryConversion):
    its own, but Curse's Mystery type counts as Ghost for a Ghost type and
    Normal for any other."""
    if mv.type == "Mystery":
        return "Ghost" if "Ghost" in types else "Normal"
    return mv.type


@form_move("CONVERSION")
def conversion(b, att, mv, dfn, pick):
    """Conversion (subscript_conversion, BtlCmd_TryConversion): its user
    takes the type of one of its moves, Conversion aside, that it is not of
    already, each such move as likely as the next; it fails on Multitype or
    with no such move. Its rows then come from its twin of that type
    (form_key). Until 2026-10-14 Conversion did nothing (Ian approved the
    fix)."""
    if att.ability == "Multitype":
        return False
    options = [t for t in (conversion_type(m, att.types) for m in att.moves if m.effect != "CONVERSION")
               if t not in att.types]
    if not options:
        return False
    set_types(att, [options[pick("conversion", len(options)) if len(options) > 1 else 0]])
    return True


@form_change
def _converted(ff):
    """Conversion: its user may take the type of any of its other moves but
    its own types."""
    for k in ff.keys():
        mvs = ff.moves(k)
        if ff.ability(k) != "Multitype" and any(m.effect == "CONVERSION" for m in mvs):
            own = ff.types(k)
            for t in sorted({conversion_type(m, own) for m in mvs if m.effect != "CONVERSION"} - set(own)):
                yield k, [t], ff.ability(k)


@form_move("CONVERSION2")
def conversion2(b, att, mv, dfn, pick):
    """Conversion 2 (subscript_conversion_2, BtlCmd_TryConversion2): its
    user takes, alone, a type that resists or is immune to the type of the
    last move aimed at it since it last acted (conversion2Move, which a
    move at its own side or the field leaves unset), one it is not of
    already, each as likely as the next (a random entry of the type chart's
    table). It fails on Multitype, with no such move, or with no such type.
    Its rows then come from its twin of that type (form_key). Until
    2026-10-14 Conversion 2 did nothing (Ian approved the fix)."""
    src = getattr(att, "conversion2_src", None)
    if att.ability == "Multitype" or src is None or src[0].range == "OPPONENT_SIDE":
        return False
    hit_by = src[1] or src[0].type
    options = sorted(d for d, m in (b.st["chart"].get(hit_by) or {}).items() if m < 1 and d not in att.types)
    if not options:
        return False
    set_types(att, [options[pick("conversion2", len(options)) if len(options) > 1 else 0]])
    return True


@form_change
def _converted2(ff):
    """Conversion 2: its user may take any type that resists a move its foes
    can aim at it, its own types aside."""
    chart = ff.blob["type_chart"]
    for k in ff.keys():
        if ff.ability(k) == "Multitype" or not any(m.effect == "CONVERSION2" for m in ff.moves(k)):
            continue
        aimed = set()
        for f in ff.foes(k):
            aimed |= ff.hit_types(f)
            aimed |= {m.type for m in ff.moves(f) if not m.damaging() and m.range not in OWN_RANGES | {"OPPONENT_SIDE"}}
        own = set(ff.types(k))
        for t in sorted(aimed):
            for d, m in sorted((chart.get(t) or {}).items()):
                if m < 1 and d not in own:
                    yield k, [d], ff.ability(k)


@form_move("SWITCH_ABILITIES")
def skill_swap(b, att, mv, dfn, pick):
    """Skill Swap (effect script 191, subscript_exchange_abilities): the user
    and its standing target swap abilities, both named, unless the move
    cannot reach the target, either ability refuses a swap
    (Ability_ChangeFails) or is kept by an Ability Shield, either holds a
    Griseous Orb, or neither has an ability; a Substitute does not stop it.
    A Truant either gains loafs on its next turn (set_ability). Each then
    reads its twin for its new ability (form_key). Until 2026-10-14 Skill
    Swap did nothing (Ian approved the fix)."""
    a, d = raw_ability(att), raw_ability(dfn)
    if (not dfn.alive() or out_of_reach(att, dfn, mv) or refuses(a, "swap") or refuses(d, "swap")
            or {"Ability Shield", "Griseous Orb"} & {att.item, dfn.item} or (a is None and d is None)):
        return False
    set_ability(b, att, d)
    set_ability(b, dfn, a, acted=getattr(dfn, "acted_turn", None) == b.turn)
    return True


@form_change
def _skill_swapped(ff):
    """Skill Swap: its user may take the ability of any foe a swap reaches,
    and that foe the user's."""
    keep = {"Ability Shield", "Griseous Orb"}
    for k in ff.keys():
        a = ff.ability(k)
        if (not any(m.effect == "SWITCH_ABILITIES" for m in ff.moves(k)) or refuses(a, "swap")
                or ff.pokemon[k].get("item") in keep):
            continue
        for f in ff.foes(k):
            d = ff.ability(f)
            if refuses(d, "swap") or ff.pokemon[f].get("item") in keep or (a is None and d is None):
                continue
            yield k, None, d, (f, None, a)


@form_move("COPY_ABILITY")
def role_play(b, att, mv, dfn, pick):
    """Role Play (effect script 178, subscript_copy_ability): the user takes
    its standing target's ability, both named, unless the user's ability is
    Multitype or cannot be replaced, it holds a Griseous Orb or an Ability
    Shield, the move cannot reach the target, or the target's ability
    refuses to be copied or is none (BtlCmd_CheckAbilityChange's copy kind);
    a Substitute does not stop it, nor the target's own Ability Shield. A
    Truant it takes makes it loaf on its next turn (set_ability). Its rows
    then come from its twin for that ability (form_key). Until 2026-10-14
    Role Play did nothing (Ian approved the fix)."""
    a, d = raw_ability(att), raw_ability(dfn)
    if (att.ability == "Multitype" or att.item in ("Griseous Orb", "Ability Shield") or not dfn.alive()
            or out_of_reach(att, dfn, mv) or refuses(d, "copy") or refuses(a, "suppress") or d is None):
        return False
    set_ability(b, att, d)
    dfn.revealed = d
    return True


@form_change
def _role_played(ff):
    """Role Play: its user may take the ability of any foe whose ability can
    be copied."""
    for k in ff.keys():
        a = ff.ability(k)
        if (not any(m.effect == "COPY_ABILITY" for m in ff.moves(k)) or a == "Multitype" or refuses(a, "suppress")
                or ff.pokemon[k].get("item") in ("Griseous Orb", "Ability Shield")):
            continue
        for f in ff.foes(k):
            d = ff.ability(f)
            if d and not refuses(d, "copy"):
                yield k, None, d


@form_move("ENTRAINMENT")
def entrainment(b, att, mv, dfn, pick):
    """Entrainment (effect script 384, subscript_entrainment): once the move
    lands, its standing target takes the user's ability, named, unless the
    move cannot reach it, a Substitute stands in front of it, the user's
    ability refuses to be passed on, the target's cannot be replaced, is
    Truant or is the user's already (BtlCmd_CheckAbilityChange's entrainment
    kind), or the target holds an Ability Shield. A target given Truant
    loafs on its next turn (set_ability). Its rows then come from its twin
    for that ability (form_key). Until 2026-10-14 Entrainment did nothing
    (Ian approved the fix)."""
    a, d = raw_ability(att), raw_ability(dfn)
    if (not dfn.alive() or out_of_reach(att, dfn, mv) or sub_blocks(att, dfn, mv) or refuses(a, "entrain")
            or refuses(d, "suppress") or d in ("Truant", a) or dfn.item == "Ability Shield"):
        return False
    set_ability(b, dfn, a, acted=getattr(dfn, "acted_turn", None) == b.turn)
    return True


@form_change
def _entrained(ff):
    """Entrainment: any foe of its user whose ability can be replaced may
    take the user's."""
    for k in ff.keys():
        a = ff.ability(k)
        if not any(m.effect == "ENTRAINMENT" for m in ff.moves(k)) or refuses(a, "entrain"):
            continue
        for f in ff.foes(k):
            d = ff.ability(f)
            if not refuses(d, "suppress") and d not in ("Truant", a) and ff.pokemon[f].get("item") != "Ability Shield":
                yield f, None, a


@form_move("SET_ABILITY_TO_INSOMNIA")
def worry_seed(b, att, mv, dfn, pick):
    """Worry Seed (effect script 247, subscript_give_target_insomnia): once
    the move lands, its standing target's ability becomes Insomnia, named,
    unless the move cannot reach it, a Substitute stands in front of it,
    its ability cannot be replaced or is Truant (BtlCmd_CheckAbilityChange's
    overwrite kind), or it holds an Ability Shield or a Griseous Orb. A
    sleeping target wakes as the move ends (RecoverStatusByAbility), and no
    sleep reaches it after. Its rows then come from its twin for Insomnia,
    which changes no row (form_key). Until 2026-10-14 Worry Seed did nothing
    (Ian approved the fix)."""
    d = raw_ability(dfn)
    if (not dfn.alive() or out_of_reach(att, dfn, mv) or sub_blocks(att, dfn, mv) or refuses(d, "suppress")
            or d == "Truant" or dfn.item in ("Ability Shield", "Griseous Orb")):
        return False
    set_ability(b, dfn, "Insomnia")
    return True


@form_change
def _worried(ff):
    """Worry Seed: any foe of its user whose ability can be replaced may
    take Insomnia."""
    for k in ff.keys():
        if not any(m.effect == "SET_ABILITY_TO_INSOMNIA" for m in ff.moves(k)):
            continue
        for f in ff.foes(k):
            d = ff.ability(f)
            if (not refuses(d, "suppress") and d != "Truant"
                    and ff.pokemon[f].get("item") not in ("Ability Shield", "Griseous Orb")):
                yield f, None, "Insomnia"


@form_move("SUPRESS_ABILITY")
def gastro_acid(b, att, mv, dfn, pick):
    """Gastro Acid (effect script 239, subscript_suppress_target_ability):
    once the move lands on its standing target, with no Substitute in front
    of it and not in the air or underground, the target's ability reads as
    none until it leaves (suppress), unless it is suppressed already, its
    ability cannot be suppressed, or it holds an Ability Shield. Nothing
    names the ability. A Neutralizing Gas holder's gas stops with it, as the
    move's end then finds (gas_update). Its rows then come from its
    ability-blank twin (form_key). Until 2026-10-14 Gastro Acid did nothing
    (Ian approved the fix)."""
    if not dfn.alive() or out_of_reach(att, dfn, mv) or sub_blocks(att, dfn, mv):
        return False
    return suppress(b, dfn)


@form_change
def _suppressed(ff):
    """Gastro Acid and Core Enforcer: any foe of their user whose ability can
    be suppressed may lose it."""
    for k in ff.keys():
        if not any(m.effect in SUPPRESSES for m in ff.moves(k)):
            continue
        for f in ff.foes(k):
            if not refuses(ff.ability(f), "suppress") and ff.pokemon[f].get("item") != "Ability Shield":
                yield f, None, None


# The moves that suppress their target's ability: Gastro Acid and Core
# Enforcer.
SUPPRESSES = frozenset({"SUPRESS_ABILITY", "CORE_ENFORCER"})


# The type Camouflage gives on each battle terrain (data/terrain/to_type.h,
# sTerrainCamouflageType); every terrain after the bridge's (the Elite
# Four's rooms, the Distortion World) counts as the special one, Normal.
CAMOUFLAGE_TYPE = {"TERRAIN_PLAIN": "Ground", "TERRAIN_SAND": "Ground", "TERRAIN_GRASS": "Grass",
                   "TERRAIN_PUDDLE": "Grass", "TERRAIN_MOUNTAIN": "Rock", "TERRAIN_CAVE": "Rock",
                   "TERRAIN_SNOW": "Ice", "TERRAIN_WATER": "Water", "TERRAIN_ICE": "Ice",
                   "TERRAIN_BUILDING": "Normal", "TERRAIN_GREAT_MARSH": "Ground", "TERRAIN_BRIDGE": "Flying"}


# The added effect Secret Power takes from its battle terrain (effect
# script 197, BtlCmd_GetTerrainSecondaryEffect, data/terrain/
# to_secondary_effect.h): a stage down on the target, a status, or a
# flinch; every terrain after the bridge's counts as the special one,
# paralysis.
SECRET_POWER_EFFECT = {"TERRAIN_PLAIN": {"acc": -1}, "TERRAIN_SAND": {"acc": -1}, "TERRAIN_GRASS": "slp",
                       "TERRAIN_PUDDLE": "slp", "TERRAIN_MOUNTAIN": "flinch", "TERRAIN_CAVE": "flinch",
                       "TERRAIN_SNOW": "frz", "TERRAIN_WATER": {"atk": -1}, "TERRAIN_ICE": "frz",
                       "TERRAIN_BUILDING": "par", "TERRAIN_GREAT_MARSH": {"spe": -1},
                       "TERRAIN_BRIDGE": {"eva": -1}}


def secret_power_effect(terrain):
    """Secret Power's added effect on this battle terrain (st["terrain"],
    calc.fight_terrain), a building's paralysis where the fight names none,
    as Camouflage takes a building's type there. Until 2026-10-15 the hit
    had no added effect (Ian approved the fix)."""
    return SECRET_POWER_EFFECT.get(terrain or "TERRAIN_BUILDING", "par")


# The move Nature Power turns into on each battle terrain (effect script
# 173, BtlCmd_GetTerrainMove, data/terrain/to_move.h); every terrain after
# the bridge's counts as the special one, Tri Attack.
NATURE_POWER_MOVE = {"TERRAIN_PLAIN": "Earthquake", "TERRAIN_SAND": "Earthquake", "TERRAIN_GRASS": "Seed Bomb",
                     "TERRAIN_PUDDLE": "Seed Bomb", "TERRAIN_MOUNTAIN": "Rock Slide", "TERRAIN_CAVE": "Rock Slide",
                     "TERRAIN_SNOW": "Blizzard", "TERRAIN_WATER": "Hydro Pump", "TERRAIN_ICE": "Ice Beam",
                     "TERRAIN_BUILDING": "Tri Attack", "TERRAIN_GREAT_MARSH": "Mud Bomb",
                     "TERRAIN_BRIDGE": "Air Slash"}


def nature_power_move(terrain):
    """The move Nature Power uses on this battle terrain (st["terrain"],
    calc.fight_terrain), as its user's own, spending no PP of its own (the
    script's GoToMoveScript); a building's Tri Attack where the fight names
    none, as Camouflage and Secret Power take a building's there. prepare()
    rows a Nature Power user with it. Until 2026-10-15 Nature Power did
    nothing (Ian approved the fix)."""
    return NATURE_POWER_MOVE.get(terrain or "TERRAIN_BUILDING", "Tri Attack")


def camouflage_type(terrain):
    """Camouflage's type on this battle terrain (calc.fight_terrain), a
    building's Normal where the fight names none."""
    return CAMOUFLAGE_TYPE.get(terrain or "TERRAIN_BUILDING", "Normal")


@form_move("CAMOUFLAGE")
def camouflage(b, att, mv, dfn, pick):
    """Camouflage (effect script 213, BtlCmd_TryCamouflage): its user takes,
    alone, the type its battle terrain gives (st["camouflage"], from the map's
    backdrop), and is marked so (MOVE_EFFECT_CAMOUFLAGE, which the trainer's
    AI reads); it fails on Multitype or when the user is of that type
    already. Its rows then come from its twin of that type (form_key). Until
    2026-10-14 Camouflage did nothing (Ian approved the fix)."""
    t = b.st.get("camouflage") or "Normal"
    if att.ability == "Multitype" or t in att.types:
        return False
    set_types(att, [t])
    att.camouflaged = True
    return True


@form_change
def _camouflaged(ff):
    """Camouflage: its user may take its terrain's type, unless it has it."""
    for k in ff.keys():
        mvs = ff.moves(k)
        if (ff.ability(k) != "Multitype" and any(m.effect == "CAMOUFLAGE" for m in mvs)
                and ff.camouflage not in ff.types(k)):
            yield k, [ff.camouflage], ff.ability(k)


# The hits that take their user's own type away once they land, and fail
# without it: Burn Up's Fire and Double Shock's Electric (effect scripts 393
# and 394).
LOSES_TYPE = {"REMOVE_USER_FIRE_TYPE_HIT": "Fire", "REMOVE_USER_ELECTRIC_TYPE_HIT": "Electric"}


def loses_type_fails(att, mv):
    """Whether Burn Up or Double Shock fails at once, its user not of the
    type it spends (the effect script's first check, before anything else is
    worked out), so Double Shock lands once a stay."""
    return mv.effect in LOSES_TYPE and LOSES_TYPE[mv.effect] not in att.types


def lose_type(mon, t):
    """subscript_remove_user_fire_type and _electric_type: once the move has
    hit, a Substitute included, its user loses the type t until it leaves; a
    dual type keeps its other type alone, and a user that had no other is
    left with none ("???", which no move's type meets). Its rows then come
    from its twin without t (form_key). Until 2026-10-14 neither move ever
    failed and its user kept its type (Ian approved the fix)."""
    rest = [x for x in mon.types if x != t]
    set_types(mon, rest or ["???"])


@form_change
def _types_spent(ff):
    """Burn Up and Double Shock: their user, if it has the type, may lose
    it."""
    for k in ff.keys():
        own = ff.types(k)
        for t in {LOSES_TYPE[m.effect] for m in ff.moves(k) if m.effect in LOSES_TYPE}:
            if t in own:
                yield k, [x for x in own if x != t] or ["???"], ff.ability(k)


def captivates(att, dfn):
    """Captivate's own checks (effect script 265) before its two stages of
    Sp. Atk: a target's Oblivious makes it ineffective, the message naming
    the ability, unless the user's Mold Breaker gets past it; a genderless
    user or target, or two of one gender, make it fail. Whether the drop may
    land. Until 2026-10-14 it landed whatever the genders (Ian approved the
    fix)."""
    if dfn.ability == "Oblivious" and not mold(att, dfn):
        reveal(dfn)
        return False
    return bool(att.gender and dfn.gender and att.gender != dfn.gender)


def lifted(dfn, mv):
    """Whether Magnet Rise makes this Ground move fail on dfn (the type
    check's MOVE_STATUS_MAGNET_RISE): not on a Pokemon rooted by Ingrain or
    holding an Iron Ball, and never for Thousand Arrows."""
    return (mv.type == "Ground" and dfn.magnet_rise and not dfn.ingrained and dfn.item != "Iron Ball"
            and mv.name != "Thousand Arrows")


def weather_move_fails(b, e):
    """Whether a weather move fails: Rain Dance, Sunny Day and Sandstorm
    under any weather of their own kind, an ability's or a fight's lasting
    one included (effect scripts 136, 137 and 115 test FIELD_CONDITION_RAINING
    and the rest, which take both kinds), and Hail only under a move's hail
    (effect script 164 tests FIELD_CONDITION_HAILING_TEMP alone, as vanilla
    Platinum's does), so under a Snow Warning's lasting hail it starts five
    turns of its own, after which the hail ends. Until 2026-10-15 Hail failed
    under any hail (Ian approved the fix)."""
    return b.weather == WEATHER_OF[e] and (e != "WEATHER_HAIL" or b.weather_turns > 0)


def status_move(b, att, mv, dfn, first):
    e = mv.effect
    if (dfn.magic_coat or dfn.ability == "Magic Bounce") and bounces(b, att, mv, dfn):
        b.reflecting = True              # Magic Coat or Magic Bounce turns it back on its user (bounces)
        try:
            status_move(b, dfn, mv, att, first)
        finally:
            b.reflecting = False
        return
    if e == "RESTORE_HP_EVERY_TURN":
        att.aqua_ring = True             # Aqua Ring
        return
    if e == "GIVE_GROUND_IMMUNITY":
        magnet_rise(att)
        return
    if e == "KO_MON_THAT_DEFEATED_USER":
        att.destiny_bond = True
        return
    foe_side = b.p if dfn.side == "p" else b.b
    own_side = b.p if att.side == "p" else b.b
    targets_foe = mv.range not in ("USER", "USER_SIDE", "ALLY", "FIELD", "USER_OR_ALLY")
    if e == "CONFUSE_ALL":
        teeter_dance_others(b, att, mv, dfn, first)     # Teeter Dance's other targets in a double battle
    if e == "FAINT_AND_ATK_SP_ATK_DOWN_2" and not memento_faints(att, dfn):
        return                           # Memento with no target: nothing happens
    if targets_foe and dfn.alive():
        if protected(b, att, mv, dfn):
            return
        if status_out_of_reach(att, dfn, mv):
            return               # a target on its hidden turn of Fly and the like (status_out_of_reach)
        # The engine runs the type chart only for moves with power, and for
        # Thunder Wave (BattleControllerPlayer_CheckTypeChart), so Thunder
        # Wave fails on a Ground type while Hypnosis still sleeps a Dark one.
        if mv.name == "Thunder Wave" and effectiveness(b.st["chart"], mv.type, dfn.types) == 0:
            return
        if powder_immune(dfn, mv, att):
            return
        if not b.accuracy_hits(att, dfn, mv, first):
            return
        if absorb(b, att, dfn, mv):
            return               # Thunder Wave into Volt Absorb, Spore into Sap Sipper: taken whole
        if soundproofed(att, dfn, mv):
            return               # Sing, Growl or Roar into Soundproof
        if dfn.ability == "Queenly Majesty" and majesty_blocked(att, dfn, mv):
            return               # a raised move into Queenly Majesty (majesty_blocked)
        if att.ability == "Prankster" and prankster_blocked(att, dfn, mv):
            return               # a raised status move into a Dark type (prankster_blocked)
    if e in STATUS_OF:
        if sub_blocks(att, dfn, mv):
            return
        give_status_by_move(b, att, dfn, mv, STATUS_OF[e])
    elif e in ("STATUS_CONFUSE", "CONFUSE_ALL"):
        if not sub_blocks(att, dfn, mv) and not confusion_blocked(b, att, dfn):
            dfn.confused = b.rng.randint(2, 5)
            confusion_berry(dfn, b)
    elif e in ("ATK_UP_2_STATUS_CONFUSION", "SP_ATK_UP_CAUSE_CONFUSION"):
        if not sub_blocks(att, dfn, mv):
            change_stages(dfn, {"atk": 2} if e.startswith("ATK") else {"spa": 1})
            if not confusion_blocked(b, att, dfn):
                dfn.confused = b.rng.randint(2, 5)
                confusion_berry(dfn, b)
    elif e == "STATUS_SLEEP_NEXT_TURN":
        if not dfn.status and not dfn.yawn and not sub_blocks(att, dfn, mv):
            dfn.yawn = 2
    elif e == "STATUS_LEECH_SEED":
        if "Grass" not in dfn.types and not sub_blocks(att, dfn, mv):
            dfn.seeded = True
    elif e == "PREVENT_HEALING":                             # Heal Block
        start_heal_block(att, dfn, mv)
    elif e == "STOCKPILE":
        stockpile(att)
    elif e in SELF_STAGES:
        if e == "TAKE_HEART":
            take_heart(att)              # the two stages, then its status cured (take_heart)
        else:
            change_stages(att, SELF_STAGES[e])
        if e == "DEF_UP_DOUBLE_ROLLOUT_POWER":
            att.curled = True
        if e == "EVA_UP_2_MINIMIZE":
            att.minimized = att.rare = True     # subscript_minimize marks its user before the stages, even at +6
        if e == "SP_DEF_UP_DOUBLE_ELECTRIC_POWER":
            att.charged, att.rare = 2, True     # subscript_charge: chargedTurns 2, set before its Sp. Def stage
    elif e == "SP_ATK_DOWN_2_OPPOSITE_GENDER":
        if captivates(att, dfn) and not sub_blocks(att, dfn, mv):
            lower_stats(b, att, dfn, FOE_STAGES[e])     # Captivate, only across the genders
    elif e in FOE_STAGES:
        if not sub_blocks(att, dfn, mv):
            lower_stats(b, att, dfn, FOE_STAGES[e])
    elif e == "SPICY_EXTRACT":
        spicy_extract(b, att, dfn, mv)
    elif e == "VENOM_DRENCH":
        # Only a poisoned target's stats fall (effect script 361); until
        # 2026-10-15 the move did nothing (Ian approved the fix).
        if dfn.status in ("psn", "tox") and not sub_blocks(att, dfn, mv):
            lower_stats(b, att, dfn, VENOM_DRENCH_STAGES)
    elif e == "PARTING_SHOT":
        parting_shot(b, att, dfn, mv)
    elif e == "FAINT_AND_FULL_HEAL_NEXT_MON":
        healing_wish(b, att)
    elif e == "FAINT_FULL_RESTORE_NEXT_MON":
        healing_wish(b, att, lunar=True)
    elif e == "GUARD_SPLIT":
        share_stats(b, att, dfn, mv, ("def", "spd"))
    elif e == "POWER_SPLIT":
        share_stats(b, att, dfn, mv, ("atk", "spa"))
    elif e == "PREVENT_ITEM_USE":
        embargo(b, att, dfn, mv)
    elif e == "MAGIC_ROOM":
        magic_room(b)
    elif e == "WONDER_ROOM":
        wonder_room(b)
    elif e == "CURSE":
        if "Ghost" in att.types:
            ghost_curse(b, att, dfn, mv)
        else:
            change_stages(att, {"atk": 1, "def": 1, "spe": -1})
    elif e == "MAX_ATK_LOSE_HALF_MAX_HP":
        # subscript_belly_drum fails, at no cost, with Attack at +6 already or
        # half its HP or less; else half its HP goes and Attack is set at +6
        # directly. Until 2026-10-20 a Belly Drum at +6 still cost half its
        # HP (Ian approved the fix on 2026-10-20).
        if att.stages["atk"] < 6 and att.hp > att.maxhp // 2:
            hurt(b, att, att.maxhp // 2)
            att.stages["atk"] = 6
    elif e == "RAISE_ALL_STATS_LOSE_THIRD_MAX_HP":
        clangorous_soul(b, att)
    elif e == "ATK_SP_ATK_SPEED_UP_2_LOSE_HALF_MAX_HP":
        fillet_away(b, att)
    elif e == "AUTOTOMIZE":
        autotomize(att)
    elif e == "LASER_FOCUS":
        laser_focus(att)
    elif e == "LUNAR_BLESSING":
        lunar_blessing(b, att)
    elif e == "REMOVE_ALL_PP_ON_DEFEAT":
        att.grudge = att.rare = True     # Grudge, until its user next acts (grudge)
    elif e == "OCTOLOCK":
        octolock(att, dfn, mv)
    elif e == "SET_AURORA_VEIL":
        aurora_veil(b, att)
    elif e == "TEATIME":
        teatime(b, lambda kind, n: b.rng.randrange(n))
    elif e == "STEAL_STATUS_MOVE":
        snatch(b, att, first)
    elif e == "CRIT_UP_2":
        att.crit_stage = 2
    elif e in HEAL_HALF:
        # Roost (effect script 214, subscript_roost) fails at full HP, as the
        # other half heals do, and otherwise also roosts its user until the
        # turn ends (TURN_FLAG_ROOSTING).
        if e == "HEAL_HALF_REMOVE_FLYING_TYPE" and att.hp < att.maxhp:
            att.roosting = True
        heal(att, att.maxhp // 2)
    elif e == "HEAL_HALF_MORE_IN_SUN":
        heal(att, weather_heal(b, att, mv))
    elif e == "LIFE_DEW":
        life_dew(att, b)
    elif e == "STRENGTH_SAP":
        strength_sap(b, att, dfn, mv)
    elif e == "REST":
        # subscript_rest fails on the abilities that keep its user awake
        # (rest_blocked), on a Pokemon already asleep ("is already asleep!"),
        # so a Sleep Talk that calls Rest does nothing, and at full HP.
        if not rest_blocked(b, att) and att.hp < att.maxhp and att.status != "slp":
            att.hp, att.status, att.sleep, att.toxic = att.maxhp, "slp", 2, 0
            cure_berry(att, b)          # a Chesto or Lum Berry wakes it at once
    elif e == "SWALLOW":
        swallow(att)
    elif e == "SET_LIGHT_SCREEN":
        if not own_side.screens["Light Screen"]:
            own_side.screens["Light Screen"] = 8 if att.item == "Light Clay" else 5
    elif e == "SET_REFLECT":
        if not own_side.screens["Reflect"]:
            own_side.screens["Reflect"] = 8 if att.item == "Light Clay" else 5
    elif e in WEATHER_OF:
        if not weather_move_fails(b, e):
            b.weather = WEATHER_OF[e]
            b.weather_turns = 8 if att.item == WEATHER_ROCK.get(b.weather) else 5
            if b.fog:
                b.fog = False        # the move clears every weather flag first, deep fog's too
    elif e == "TRICK_ROOM":
        if b.trick_room < 999:               # a permanent room makes the move fail
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
        lay_web(b, att)
    elif e == "REMOVE_HAZARDS_SCREENS_EVA_DOWN":
        defog(b, att, dfn, mv)
    elif e == "PROTECT_USER_SIDE":
        side_guard(b, att, mv, first)
    elif e == "PROTECT" or e == "SURVIVE_WITH_1_HP":
        # BtlCmd_TryProtection: it fails when no battler acts after its user,
        # and otherwise works at protect_odds; a failure ends the run.
        if not moves_last(b, first) and b.rng.random() < protect_odds(att):
            att.protecting = e == "PROTECT"
            att.enduring = e == "SURVIVE_WITH_1_HP"
            att.protect_run = min(att.protect_run + 1, PROTECT_RUN_CAP)
        else:
            att.protect_run = 0
    elif e == "SET_SUBSTITUTE":
        if not att.sub and att.hp > att.maxhp // 4:
            hurt(b, att, att.maxhp // 4)
            att.sub = att.maxhp // 4
    elif e == "RESET_STAT_CHANGES":
        # Haze (effect script 25, subscript_reset_all_stat_stages): every
        # Pokemon on the field, its Focus Energy too (reset_all_stats).
        reset_all_stats(b)
    elif e == "HEAL_STATUS":
        refresh(att)
    elif e == "SWAP_ATK_DEF":
        power_trick(att)
    elif e == "TRANSFER_STATUS":
        psycho_shift(b, att, dfn, mv)
    elif e == "SWAP_DEF_SP_DEF_STAT_CHANGES":
        swap_stages(att, dfn, ("def", "spd"))     # Guard Swap
    elif e == "SWAP_ATK_SP_ATK_STAT_CHANGES":
        swap_stages(att, dfn, ("atk", "spa"))     # Power Swap
    elif e == "SWAP_STAT_CHANGES":
        heart_swap(att, dfn)
    elif e == "HEAL_TARGET":
        heal_pulse(att, dfn, mv)
    elif e == "HALVE_FIRE_DAMAGE":
        water_sport(att)
    elif e == "HALVE_ELECTRIC_DAMAGE":
        mud_sport(att)
    elif e == "APPLY_MAGIC_COAT":
        att.magic_coat = not moves_last(b, first)     # it fails when no battler acts after its user
    elif e == "RANDOM_STAT_UP_2":
        acupressure(att, b.rng.randrange)
    elif e == "CURE_PARTY_STATUS":
        party_cure(b, att, mv)           # Heal Bell spares Soundproof, both end Nightmare (party_cure)
    elif e == "PREVENT_STATUS":
        own_side.safeguard = 5
    elif e == "PREVENT_STAT_REDUCTION":
        mist(own_side)
    elif e == "PREVENT_CRITS":
        lucky_chant(own_side)
    elif e == "COPY_STAT_CHANGES":
        psych_up(att, dfn)
    elif e == "NEXT_ATTACK_ALWAYS_HITS":
        lock_on(att, dfn)
    elif e == "FORESIGHT":
        foresee_target(dfn)
    elif e == "IGNORE_EVATION_REMOVE_DARK_IMMUNE":
        miracle_eye(dfn)
    elif e == "GRAVITY":
        gravity_start(b)
    elif e == "COPY_MOVE_FOR_BATTLE":
        mimic(att, dfn)
    elif e == "LEARN_MOVE_PERMANENT":
        sketch(att, dfn, mv)
    elif e == "TRANSFORM":
        transform(b, att, dfn)
    elif e == "TAUNT":
        if not dfn.taunt and not taunt_blocked(att, dfn):
            dfn.taunt = b.rng.randint(3, 5)
    elif e == "TORMENT":
        dfn.tormented = True             # subscript_torment_start: fails if already tormented
    elif e == "DISABLE":
        # subscript_disable_start fails on a target in the air or underground.
        if not (dfn.charging is not None and dfn.charging.effect in INVULNERABLE):
            disable(dfn, lambda: b.rng.randint(3, 6))
    elif e == "STATUS_NIGHTMARE":
        nightmare(att, dfn, mv)
    elif e == "ENCORE":
        encore(dfn, lambda: b.rng.randint(3, 7))
    elif e == "INFATUATE":
        infatuate(att, dfn, att.ability == "Mold Breaker")
    elif e == "HEAL_IN_3_TURNS":
        wish(own_side)
    elif e == "DECREASE_LAST_MOVE_PP":
        spite(dfn)
    elif e == "RECYCLE":
        recycle(att)
    elif e == "AVERAGE_HP":
        pain_split(b, att, dfn)
    elif e == "FORCE_SWITCH":
        bench = foe_side.bench()
        if bench and not anchored(att, dfn) and not getattr(dfn, "ingrained", False) \
                and (att.level >= dfn.level or b.rng.random() < whirlwind_odds(att.level, dfn.level)):
            nxt = b.rng.choice(bench)
            switch_in(b, foe_side, foe_side.mons.index(nxt))
    elif e == "FAINT_AND_ATK_SP_ATK_DOWN_2":
        memento_drops(b, att, dfn, mv)
    elif e == "PASS_STATS_AND_STATUS":
        att.baton = True
    elif e == "SWITCH_HELD_ITEMS":
        swap_items(att, dfn, mv)
        mark_unheld(b, att, dfn)         # a trainer's item swapped away from its rows (item twin)
    elif e == "MAKE_SHARED_MOVES_UNUSEABLE":
        imprison(b, att)
    elif e in FORM_MOVES:
        # The status moves that change a type or an ability (FORM_MOVES).
        FORM_MOVES[e](b, att, mv, dfn, lambda kind, n: b.rng.randrange(n))
    elif e == "ALL_FAINT_3_TURNS":
        # Perish Song: every Pokemon on the field faints at the end of the
        # third turn after this one unless it switches out first.
        for m in (b.p.on_field() + b.b.on_field()):
            if m.alive() and not m.perish and (m.ability != "Soundproof" or mold(att, m)):
                m.perish = 4
    elif e == "HIT_IN_3_TURNS":
        pass


def raw_stat(mon, stat):
    """A Pokemon's raw stat as the battle has it: the calculator's, unless
    Guard Split or Power Split has averaged it (Mon.split)."""
    got = mon.split.get(stat) if mon.split else None
    return got if got is not None else mon.stats.get(stat, 1)


def share_stats(b, att, dfn, mv, stats):
    """Guard Split (effect script 278, subscript_guard_split) and Power
    Split (279, subscript_power_split): a Substitute stops it; otherwise
    each of the stats named, Defense and Sp. Def or Attack and Sp. Atk, is
    the two Pokemon's raw values added and halved, in whole numbers, for
    both, until each leaves. The calculator's rows keep the stats they were
    made with, so split_mult scales each hit by the stats' ratio."""
    if sub_blocks(att, dfn, mv):
        return
    for stat in stats:
        avg = (raw_stat(att, stat) + raw_stat(dfn, stat)) // 2
        for m in (att, dfn):
            m.split = dict(m.split or {}, **{stat: avg})
    att.rare = dfn.rare = True
    b.split = True


def split_mult(att, dfn, mv):
    """The factor stats Guard Split or Power Split averaged put on a hit:
    the attacker's Attack or Sp. Atk now over its row's, the target's
    Defense or Sp. Def in its row over now (Psyshock's kind against
    Defense). The damage formula's whole-number steps and its added 2 are
    not followed, so a hit can differ from the engine's by a point or a few
    per cent; exact rows for the new stats would need twins rowed for each
    pair that splits."""
    if not (att.split or dfn.split):
        return 1.0
    a, d = ("atk", "def") if mv.cat == "Physical" else ("spa", "spd")
    if mv.const in AGAINST_DEFENSE:
        d = "def"
    mult = 1.0
    if att.split and a in att.split:
        mult *= att.split[a] / max(1, att.stats.get(a, 1))
    if dfn.split and d in dfn.split:
        mult *= max(1, dfn.stats.get(d, 1)) / max(1, dfn.split[d])
    return mult


# The five stats Clangorous Soul raises (subscript_boost_all_stats).
ALL_FIVE = ("atk", "def", "spa", "spd", "spe")


def clangorous_soul(b, att):
    """Clangorous Soul (effect script 346,
    subscript_raise_all_stats_lose_third_max_hp): it fails with all five
    stats at +6, or with its user at a third of its maximum HP or less;
    otherwise the user loses that third, as Belly Drum's half is lost, and
    its Attack, Defense, Speed, Sp. Atk and Sp. Def rise a stage each
    (subscript_boost_all_stats). Until 2026-10-15 it did nothing (Ian
    approved the fix)."""
    third = att.maxhp // 3
    if all(att.stages[k] >= 6 for k in ALL_FIVE) or att.hp <= third:
        return
    hurt(b, att, third)
    change_stages(att, dict.fromkeys(ALL_FIVE, 1))


def fillet_away(b, att):
    """Fillet Away (effect script 303,
    subscript_atk_sp_atk_speed_up_2_lose_half_max_hp): it fails with
    Attack, Sp. Atk and Speed all at +6, or with its user at half its
    maximum HP or less (BattleSystem_Divide's half); otherwise the user
    loses that half, as Belly Drum's is lost (hurt, which checks a pinch
    Berry), and the three rise two stages each through the stat-stage
    subscript (change_stages). Until 2026-10-20 it did nothing (Ian
    approved the fix)."""
    half = engine_divide(att.maxhp, 2)
    if all(att.stages[k] >= 6 for k in ("atk", "spa", "spe")) or att.hp <= half:
        return
    hurt(b, att, half)
    change_stages(att, {"atk": 2, "spa": 2, "spe": 2})


def autotomize(att):
    """Autotomize (effect script 281, subscript_autotomize): it fails with
    its user's Speed at +6; otherwise the Speed rises two stages through
    the stat-stage subscript (change_stages) and ReduceWeight takes 100 kg
    off the user's weight, to 0.1 kg at least, until it leaves
    (Mon.lightened, which Low Kick, Grass Knot, Heavy Slam and Heat Crash
    read through weight_now). Until 2026-10-20 it did nothing (Ian
    approved the fix)."""
    if att.stages["spe"] >= 6:
        return
    change_stages(att, {"spe": 2})
    att.lightened += 1
    att.rare = True


# The weight moves' powers by the target's weight in tenths of a kilogram
# (sWeightToPower): the first bound the weight does not pass, else 120.
WEIGHT_TO_POWER = ((100, 20), (250, 40), (500, 60), (1000, 80), (2000, 100))


def weight_now(b, att, mon, lightened):
    """mon's weight in tenths of a kilogram as Battler_Weight(att, mon)
    reads it: its species' weight, less 100 kg for each Autotomize when
    `lightened` (ReduceWeight, to 1 at least), then doubled by Heavy Metal
    or halved by Light Metal unless att's Mold Breaker gets past mon's,
    and never below 1."""
    rec = b.st["pokemon"].get(mon.key) or {}
    poks = calc.blob()["poks"].get(rec.get("species") or mon.species) or {}
    w = int(round((poks.get("weightkg") or 0) * 10))
    for _ in range(mon.lightened if lightened else 0):
        w = w - 1000 if w > 1000 else 1
    if mon is att or not mold(att, mon):
        if mon.ability == "Heavy Metal":
            w *= 2
        elif mon.ability == "Light Metal":
            w //= 2
    return max(1, w)


def weight_move_power(b, att, dfn, mv, lightened):
    """A weight move's power: Low Kick's and Grass Knot's by the target's
    weight (BtlCmd_CalcWeightBasedPower), Heavy Slam's and Heat Crash's by
    the target's share of the user's (BtlCmd_CalcHeavySlamPower), with
    the weights now (`lightened`) or as the rows have them."""
    if mv.effect == "HEAVY_SLAM":
        ratio = weight_now(b, att, dfn, lightened) * 10000 // weight_now(b, att, att, lightened)
        return 120 if ratio <= 2000 else 100 if ratio <= 2500 else 80 if ratio <= 3334 else 60 if ratio <= 5000 else 40
    w = weight_now(b, att, dfn, lightened)
    return next((p for bound, p in WEIGHT_TO_POWER if bound >= w), 120)


def healing_wish(b, att, lunar=False):
    """Healing Wish (effect script 220, subscript_healing_wish) and, with
    lunar, Lunar Dance (effect script 270, subscript_lunar_dance): it fails
    when no party member can come in (TryReplaceFaintedMon); otherwise its
    user faints, and the turn sends in its replacement at once
    (wish_comes_true). Until 2026-10-15 both did nothing (Ian approved the
    fixes). In a double battle the party is the user's own trainer's
    (BattleSystem_AnyReplacementMons keeps a tag battle's apart), and the
    one sent in takes the user's slot; until 2026-10-21 both did nothing
    there (Ian approved the double-battle parts of batches 7 and 8 on
    2026-10-14)."""
    side = b.p if att.side == "p" else b.b
    if not side.bench(owner=getattr(att, "owner", None) if b.doubles else None):
        return
    att.hp = 0
    att.wished = "lunar" if lunar else True


def wish_comes_true(b, mon, choose, slot=0, owner=None):
    """Healing Wish's and Lunar Dance's replacement (their subscripts,
    straight after the move): the party member choose(side) picks comes in
    and meets the hazards, and one left standing gets its HP back in full
    and its status cured, and after Lunar Dance every move's PP too; one the
    hazards knock out is replaced in turn, the wish waiting for the next.
    In a double battle the one sent in takes the user's slot (`slot`), from
    its own trainer's party (`owner`)."""
    lunar = mon.wished == "lunar"
    mon.wished = False
    side = b.p if mon.side == "p" else b.b
    while side.bench(owner):
        idx = choose(side)
        if idx is None or not side.mons[idx].alive():
            return
        switch_in(b, side, idx, slot=slot)
        new = side.mons[idx]
        if new.alive():
            new.hp, new.status, new.sleep, new.toxic = new.maxhp, None, 0, 0
            if lunar:
                new.pp = {m.name: m.pp for m in new.moves}     # BATTLEMON_MAX_PP_1 to 4 into CUR_PP
            return


def parting_shot(b, att, dfn, mv):
    """Parting Shot (effect script 389, subscript_parting_shot): it fails on
    a target behind a Substitute, and does nothing more on one whose Attack
    and Sp. Atk are both at -6; otherwise the target's Attack and Sp. Atk
    fall a stage each, as Tickle's do (Mist and the blocking abilities stop
    each drop, not what follows), and its user then switches out through the
    party list, passing nothing on, when it has someone to send in: the
    turn switches it as after U-turn (u_turn). Until 2026-10-15 the move did
    nothing (Ian approved the fix)."""
    if sub_blocks(att, dfn, mv) or (dfn.stages["atk"] <= -6 and dfn.stages["spa"] <= -6):
        return
    lower_stats(b, att, dfn, {"atk": -1, "spa": -1})
    att.u_turn = True


def defog(b, att, dfn, mv):
    """Defog (effect script 258, subscript_defog, Oxide's Generation 6
    version): the target's evasion falls a stage, which a Substitute, Mist
    and the blocking abilities stop as for any drop (lower_stats); then,
    whatever became of the drop, the target's side loses Reflect, Light
    Screen, Mist and Safeguard, both sides lose Spikes, Toxic Spikes,
    Stealth Rock and Sticky Web, and a battle in deep fog (Ian, 2026-09-26:
    Defog still clears fog) is clear of it. Until 2026-10-15 it did nothing
    (Ian approved the fix)."""
    if not sub_blocks(att, dfn, mv):
        lower_stats(b, att, dfn, {"eva": -1})
    side = b.p if dfn.side == "p" else b.b
    side.screens = dict.fromkeys(side.screens, 0)
    if side.aurora_veil:
        side.aurora_veil = 0             # subscript_defog clears Aurora Veil after the screens
    side.mist = side.safeguard = 0
    for s in (b.p, b.b):
        s.hazards = dict.fromkeys(s.hazards, 0)
        if s.web:
            s.web = 0
    if b.fog:
        b.fog = False                # FIELD_CONDITION_DEEP_FOG cleared


def lay_web(b, att):
    """Sticky Web (effect script 326, BtlCmd_TryStickyWeb): a web on the
    side across from its user, failing while one is laid. Until 2026-10-15
    the move did nothing (Ian approved the fix)."""
    side = b.b if att.side == "p" else b.p
    if not side.web:
        side.web = 1


def web_grounded(b, mon):
    """Whether a newcomer meets Sticky Web (Battler_IsGrounded): not a Flying
    type, a Levitate holder or an Air Balloon's, unless an Iron Ball or
    Gravity holds it down; a newcomer has no Magnet Rise or Smack Down yet."""
    return (("Flying" not in mon.types and mon.ability != "Levitate" and mon.item != "Air Balloon")
            or mon.item == "Iron Ball" or bool(b.gravity))


def web_catch(mon):
    """A grounded newcomer caught in Sticky Web (BtlCmd_CheckStickyWeb): Clear
    Body and White Smoke keep its Speed, Contrary raises it a stage instead,
    a Clear Amulet keeps it, and at -6 nothing happens; otherwise it falls a
    stage, made directly, so Simple does not double it and Mist and Magic
    Guard do not stop it, and Defiant or Competitive answers the drop, as
    the other side laid the web."""
    ab = mon.ability
    if ab in ("Clear Body", "White Smoke"):
        reveal(mon)
        return
    if ab == "Contrary":
        if mon.stages["spe"] < 6:
            mon.stages["spe"] += 1
            mon.stat_raised = True
        return
    if mon.item == "Clear Amulet" or mon.stages["spe"] <= -6:
        return
    change_stages(mon, {"spe": -1}, simple=False)
    if ab in DEFIANT_STAT:
        raise_own(mon, DEFIANT_STAT[ab], 2)


def baton_state(mon):
    """What Baton Pass hands its replacement (BattleSystem_InitBattleMon
    under SYSCTL_BATON_PASS): the stat stages; of the volatile conditions
    Focus Energy's critical rate, being held by Mean Look or Block,
    confusion, a Ghost's Curse and the Substitute with its HP
    (VOLATILE_CONDITION_BATON_PASSED); and of the move effects Leech Seed,
    Perish Song's count, Ingrain, Aqua Ring, a suppressed ability (Gastro
    Acid), Heal Block's, Magnet Rise's and Embargo's turns, Lock-On's hold,
    Water Sport, Mud Sport and Power Trick (MOVE_EFFECT_BATON_PASSED).
    Everything else (Taunt, Encore, Disable, Torment, Yawn, a bind, love,
    Salt Cure, Stockpile, Imprison) stays behind."""
    return {"stages": dict(mon.stages), "crit_stage": mon.crit_stage, "trapped_by": mon.trapped_by,
            "octolocked": mon.octolocked,
            "confused": mon.confused, "cursed": mon.cursed, "sub": mon.sub, "seeded": mon.seeded,
            "perish": mon.perish, "ingrained": mon.ingrained, "aqua_ring": mon.aqua_ring,
            "heal_block": mon.heal_block, "magnet_rise": mon.magnet_rise,
            "locked_on": mon.locked_on, "lock_on_by": mon.lock_on_by, "water_sport": mon.water_sport,
            "mud_sport": mon.mud_sport, "power_trick": mon.power_trick, "embargo": mon.embargo,
            "rare": bool(mon.locked_on or mon.water_sport or mon.mud_sport or mon.power_trick or mon.embargo
                         or mon.octolocked or mon.ingrained),     # Ingrain's grounding (grounded)
            "suppressed": getattr(mon, "suppressed", False)}


def baton_pass(b, side, index, slot=0):
    """Baton Pass's switch (effect script 127, subscript_baton_pass): its
    user leaves, as any switch does (Natural Cure and Regenerator on the
    way out), and the replacement comes in carrying baton_state, before the
    hazards and its own entry abilities; a foe that the user's Mean Look or
    Block held stays held by the replacement, and the user's binds and
    love end (BattleSystem_InitBattleMon). Until 2026-10-15 Baton Pass did
    nothing and its user stayed in (Ian approved the fix). `slot`: the
    user's slot, 1 for a double battle's second."""
    leaving = side.mons[side.active2] if slot == 1 else side.cur()
    switch_in(b, side, index, slot=slot, passed=baton_state(leaving))


def switch_in(b, side, index, slot=0, lead=False, passed=None):
    """A Pokemon comes in to a slot: volatile state resets, hazards bite.
    A lead at the battle's start (`lead`) leaves its Intimidate to
    open_battle, which runs it once every lead is in. `passed`: what a Baton
    Pass hands the newcomer (baton_state)."""
    leaving = side.cur() if slot == 0 else (side.mons[side.active2] if side.active2 is not None else None)
    b.status_src = None          # hazards give their status from no foe
    gas = b.st.get("gas")
    if gas:
        gas_update(b, check=False)
    if leaving is not None and leaving.alive() and leaving is not side.mons[index]:
        # As it leaves: Natural Cure cures its status, and Oxide's
        # Regenerator gives back a third of its HP (BtlCmd_TryRestoreStatusOnSwitch).
        # Neutralizing Gas on the field stops both: the ability reads None.
        if leaving.ability == "Natural Cure":
            leaving.status, leaving.sleep, leaving.toxic = None, 0, 0
        if leaving.ability == "Regenerator":
            heal(leaving, leaving.maxhp // 3)
    if leaving is not None:
        for foe in (b.b if side is b.p else b.p).mons:
            if foe.trapped_by == leaving.key:
                # A Baton Pass keeps a foe held by its user (the Mean Look
                # clearing is skipped under SYSCTL_BATON_PASS), an
                # Octolock's with it; otherwise its Octolock ends too.
                foe.trapped_by = None if passed is None else side.mons[index].key
                if passed is None and foe.octolocked:
                    foe.octolocked = False
            if leaving.imprisoning and foe.sealed:
                foe.sealed = frozenset()     # the Imprison ends with its user (moveEffectsMask cleared)
            if foe.bound and getattr(foe, "bound_by", None) == leaving.key:
                # The bind ends when its binder leaves, by a switch or a
                # knockout's replacement (BattleSystem_InitBattleMon clears
                # the binds bindTarget names); until 2026-10-15 it outlasted
                # the binder (Ian approved the fix).
                foe.bound, foe.bound_by = 0, None
            if foe.infatuated == leaving.key:
                foe.infatuated = None    # love ends when its object leaves (battle_lib's switch-out)
            if foe.mirror is not None:
                foe.mirror = None        # a battler coming in clears its foes' moveCopied
            if foe.locked_on and foe.lock_on_by == leaving.key:
                # The user's Lock-On ends as it leaves, or passes with a Baton
                # Pass to its replacement, its count started again.
                foe.locked_on, foe.lock_on_by = (0, None) if passed is None else (2, side.mons[index].key)
        if leaving.gas_stash is not None and leaving is not side.mons[index]:
            leaving.ability, leaving.gas_stash = leaving.gas_stash, None   # its party record keeps its ability
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
    seal_newcomer(b, side, new)
    if b.st.get("soul_heart"):
        new.soul_seen = fainted_others(b, new)     # Soul Heart counts the faints from here on (soul_heart)
    if passed is not None:
        suppressed = passed.pop("suppressed")
        for k, v in passed.items():
            setattr(new, k, v)
        if suppressed:
            suppress(b, new)         # Gastro Acid's suppression goes with the baton
    if b.magic_room or new.embargo:
        new.roomed = bool(b.magic_room)
        lock_item(new)               # no held item works for it under Magic Room or a passed Embargo
    if gas:
        # The gas reads live: a newcomer under it meets the hazards with its
        # ability off, and a holder's arrival or departure turns the others'
        # off or on at once.
        gas_update(b, check=False)
    # subscript_hazards_check sends a Magic Guard holder straight past Toxic
    # Spikes, Spikes and Stealth Rock (to Sticky Web, laid since 2026-10-15,
    # which still catches it), so it takes no hazard damage and no poison, and a Poison type
    # holding it does not soak up the Toxic Spikes either. Until 2026-10-14
    # every hazard reached it (Ian approved the fix).
    guarded = new.ability == "Magic Guard"
    if side.hazards["rocks"] and not guarded:
        # An Arceus with Multitype meets the rocks as the type its Plate gives
        # it, or as Normal without one (Battler_MonType), where rock_eff has
        # its record's types (a player's record holds no item).
        eff = effectiveness(b.st["chart"], "Rock", new.types) if new.ability == "Multitype" \
            else b.st["rock_eff"].get(new.key, 1)
        hurt(b, new, int(new.maxhp * eff / 8))
    # Gravity holds a Flying or Levitate newcomer down for the Spikes
    # (subscript_hazards_check).
    grounded = ("Flying" not in new.types and new.ability != "Levitate" or bool(b.gravity)) and not guarded
    if grounded and side.hazards["spikes"]:
        hurt(b, new, new.maxhp * {1: 1, 2: 1.5, 3: 2}[side.hazards["spikes"]] // 8)
    if grounded and side.hazards["tspikes"]:
        if "Poison" in new.types:
            side.hazards["tspikes"] = 0
        else:
            give_status(b, new, "psn" if side.hazards["tspikes"] == 1 else "tox")
    if side.web and new.alive() and web_grounded(b, new):
        web_catch(new)               # Sticky Web last, past Magic Guard (subscript_hazards_check)
    if b.st.get("soul_heart"):
        soul_heart(b)                # a newcomer the hazards knocked out (soul_heart)
    if gas and gas_update(b):
        return                   # the gas wore off: the whole field's entry abilities went off, the newcomer's with them
    entry_abilities(b, [new], intimidate=not lead, trace_now=not lead)


def end_of_turn(b):
    _end_of_turn(b)
    if b.st.get("soul_heart"):
        soul_heart(b)                # the turn's end's knockouts (soul_heart)
    b.mid_turn = False
    if b.st.get("gas"):
        # A holder that fell at the turn's end takes its gas with it now; the
        # announcements it owes wait for its replacement's switch-in check.
        gas_update(b, check=False)


def battle_over(b):
    """A side has no Pokemon left: the engine checks it between every step
    of the turn's end (BattleControllerPlayer_CheckBattleOver), so the first
    side to run out loses, whatever would have come after."""
    return not b.p.alive() or not b.b.alive()


def helps(b, mon, kind, p):
    """A chance at p that helps mon, through the battle's dice when it has
    them, so the planner enumerates it and a trainer's luck is the player's
    bad luck, else through its own rng."""
    dice = getattr(b, "dice", None)
    if dice is None:
        return b.rng.random() < p
    return dice.bad(kind, p) if mon.side == "b" else dice.good(p, kind)


def coin(b, kind="tie"):
    """A fair coin through the battle's dice (so the planner enumerates it),
    or its own rng for a battle fightsim plays alone."""
    dice = getattr(b, "dice", None)
    return dice.choice(kind, 2) == 1 if dice is not None else b.rng.random() < 0.5


def pick_one(b, kind, n):
    """One of n outcomes, at even odds, through the battle's dice (so the
    planner enumerates it), or its own rng for a battle fightsim plays
    alone."""
    if n <= 1:
        return 0
    dice = getattr(b, "dice", None)
    return dice.choice(kind, n) if dice is not None else b.rng.randrange(n)


# The five stats Moody draws from, in the engine's order (BATTLE_STAT_ATTACK
# to BATTLE_STAT_SP_DEFENSE).
MOODY_STATS = ("atk", "def", "spe", "spa", "spd")


def healer(b, m):
    """Healer (BattleSystem_TriggerTurnEndAbility, subscript_healer): at each
    turn's end, in a double battle, three times in ten its standing
    partner's status is cured, and Nightmare with it; the message names the
    ability. In a single battle it has no partner. Until 2026-10-21 it did
    nothing (Ian approved the double-battle part batch 11 left on
    2026-10-14)."""
    ally = ally_of(b, m)
    if m.alive() and ally is not None and ally.status and helps(b, ally, "healer", 0.3):
        ally.status, ally.sleep, ally.toxic, ally.nightmare = None, 0, 0, False
        reveal(m)


def moody(b, m):
    """Moody (BattleSystem_TriggerTurnEndAbility, subscript_moody): at each
    turn's end one of the five stats other than accuracy and evasion that
    is below +6, drawn at random, rises two stages, and then one of the
    other four above -6, drawn at random, falls one, each made by
    ability_stages, so Simple and Contrary play no part; with no stat to
    draw, that change is left out. Until 2026-10-20 it did nothing (Ian
    approved the fix)."""
    room = [s for s in MOODY_STATS if m.stages[s] < 6]
    up = room[pick_one(b, "moody", len(room))] if room else None
    room = [s for s in MOODY_STATS if s != up and m.stages[s] > -6]
    down = room[pick_one(b, "moody", len(room))] if room else None
    if up is not None:
        ability_stages(m, m, up, 2)
    if down is not None:
        ability_stages(m, m, down, -1)


SLOW_ITEMS = ("Lagging Tail", "Full Incense")


def slow_after(m1, m2, s1, s2, tie):
    """Lagging Tail and Full Incense, then Stall, in a comparison of two
    Pokemon in one priority bracket that no Quick Claw or Custap Berry has
    settled (BattleSystem_CompareBattlerSpeed, HOLD_EFFECT_PRIORITY_DOWN and
    ABILITY_STALL): None when neither holds such an item and neither has
    Stall, so Speed decides; else whether m1 goes after m2. A holder goes
    after one without, and of two holders the slower goes first (s1 and s2
    their Speeds, Trick Room or not), tie() deciding equal Speeds. Each item
    is checked before Stall, so a Lagging Tail holder goes after a Stall
    Pokemon."""
    l1, l2 = m1.item in SLOW_ITEMS, m2.item in SLOW_ITEMS
    if not (l1 or l2):
        l1, l2 = m1.ability == "Stall", m2.ability == "Stall"
        if not (l1 or l2):
            return None
    if l1 != l2:
        return l1
    return s1 > s2 or (s1 == s2 and tie())


def end_order(b):
    """The Pokemon on the field in the order the engine runs the turn's end:
    BattleSystem_SortMonSpeedOrder, re-run once the moves are done
    (battle_controller_player.c 907), an exchange sort from battler 0 (the
    player's first slot, then the trainer's, then the second slots) on
    BattleSystem_CompareBattlerSpeed with ignoreQuickClaw (battle_lib.c 1207
    to 1470). A fainted Pokemon goes after a standing one; then a Quick Claw
    that fired this turn, or a Custap Berry in its pinch, goes first; a
    Lagging Tail or Full Incense, then Stall, goes last; then Speed, the
    slower first under Trick Room; a tie swaps on a coin flip."""
    order = []
    for pair in zip(b.p.on_field() + [None], b.b.on_field() + [None]):
        order += [m for m in pair if m is not None]
    quick = getattr(b, "quick", None) or {}

    def after(m1, m2):
        """Whether m1 goes after m2 (the comparison's nonzero result)."""
        if not m1.alive() or not m2.alive():
            return not m1.alive() and m2.alive()
        q1, q2 = quick.get(m1.key) or custap_fires(m1, b), quick.get(m2.key) or custap_fires(m2, b)
        s1, s2 = b.speed(m1), b.speed(m2)
        if q1 != q2:
            return q2
        if q1 and q2:
            return s1 < s2 or (s1 == s2 and coin(b))
        lag1, lag2 = m1.item in ("Lagging Tail", "Full Incense"), m2.item in ("Lagging Tail", "Full Incense")
        if lag1 or lag2:
            return (lag1 and not lag2) or (lag1 and lag2 and (s1 > s2 or (s1 == s2 and coin(b))))
        st1, st2 = m1.ability == "Stall", m2.ability == "Stall"
        if st1 or st2:
            return (st1 and not st2) or (st1 and st2 and (s1 > s2 or (s1 == s2 and coin(b))))
        if b.trick_room:
            return s1 > s2 or (s1 == s2 and coin(b))
        return s1 < s2 or (s1 == s2 and coin(b))

    for j in range(len(order) - 1):
        for k in range(j + 1, len(order)):
            if after(order[j], order[k]):
                order[j], order[k] = order[k], order[j]
    return order


def _end_of_turn(b):
    """The turn's end in the engine's three stages, each over the Pokemon in
    end_order, stopping the moment a side has no Pokemon left (battle_over).
    Field conditions (BattleControllerPlayer_CheckFieldConditions): the
    sides' screens, Tailwind and Safeguard count down, Wish lands, then a
    move's weather counts down (ending before it acts on its last turn) and
    sand and hail strike each Pokemon, Ice Body healing in hail instead
    (subscript_weather_continues, by GetMonBySpeedOrder). Each Pokemon's own conditions (_end_of_turn_mon).
    Side conditions: Future Sight (future_sight_ends), Perish Song, then
    Trick Room's count."""
    b.status_src = None          # no foe gives what the turn's end gives
    order = end_order(b)
    for side in (b.p, b.b):
        side.screens = {k: max(0, v - 1) for k, v in side.screens.items()}
        if side.aurora_veil:
            side.aurora_veil -= 1        # FIELD_COND_CHECK_STATE_AURORA_VEIL, after Light Screen
        side.tailwind = max(0, side.tailwind - 1)
        side.safeguard = max(0, side.safeguard - 1)
        side.mist = max(0, getattr(side, "mist", 0) - 1)
        if side.lucky_chant:
            side.lucky_chant -= 1        # FIELD_COND_CHECK_STATE_LUCKY_CHANT
    for m in order:
        side = b.p if m.side == "p" else b.b
        if side.wish and m is side.cur():
            side.wish -= 1
            if side.wish == 0 and m.alive() and not heal_blocked(m):
                heal(m, m.maxhp // 2)
    if b.gravity:
        b.gravity -= 1               # FIELD_COND_CHECK_STATE_GRAVITY
    if b.weather_turns:
        b.weather_turns -= 1
        if b.weather_turns == 0:
            # A weather move cleared the map's weather when it began
            # (effect_script_0136 and its siblings clear every weather
            # flag), and only the move's own flag clears now, so the
            # field is left clear rather than returning to the map's.
            b.weather = None
    if b.weather in ("Sand", "Hail") and not weather_ignored(b):
        # BtlCmd_EndOfTurnWeatherEffect acts only under NO_CLOUD_NINE: with
        # Cloud Nine or Air Lock out no Pokemon is bitten, nor healed by Ice
        # Body (until 2026-10-20 the bite came all the same, Ian approved
        # the fix).
        safe = {"Sand": {"Rock", "Ground", "Steel"}, "Hail": {"Ice"}}[b.weather]
        # The abilities the weather's bite passes over (BtlCmd_EndOfTurnWeatherEffect):
        # Sand Veil, and Oxide's Sand Rush and Sand Force, in sand; Snow
        # Cloak in hail; Oxide's Overcoat in both. Sand Rush and Sand Force
        # were bitten until 2026-10-14, Overcoat until 2026-10-20 (Ian
        # approved the fixes).
        shield = {"Sand": ("Sand Veil", "Sand Rush", "Sand Force", "Overcoat"),
                  "Hail": ("Snow Cloak", "Overcoat")}[b.weather]
        for m in order:
            if b.weather == "Hail" and m.ability == "Ice Body":
                # BtlCmd_EndOfTurnWeatherEffect: Ice Body heals a sixteenth in
                # hail in place of the hail's bite, below full HP, unless
                # Cloud Nine or Air Lock is out.
                if m.alive() and m.hp < m.maxhp and not weather_ignored(b):
                    heal(m, max(1, m.maxhp // 16))
                continue
            if m.alive() and not set(m.types) & safe and m.ability not in shield and m.ability != "Magic Guard":
                hurt(b, m, m.maxhp // 16)
                if battle_over(b):
                    return
    if b.weather in ("Rain", "Sun") and not weather_ignored(b):
        # BtlCmd_EndOfTurnWeatherEffect, a Pokemon at a time in speed order:
        # Dry Skin gets an eighth of maximum HP back in rain, below full HP,
        # and loses an eighth in sun; Rain Dish a sixteenth back in rain,
        # below full HP; Hydration cures its status in rain; Solar Power
        # loses an eighth in sun. The heals and the loss name the ability, and
        # Hydration's cure does. Rain Dish, Hydration and Solar Power did
        # nothing until 2026-10-14 (Ian approved the fix).
        for m in order:
            if not m.alive():
                continue
            if m.ability == "Dry Skin":
                if b.weather == "Rain":
                    if m.hp < m.maxhp:
                        heal(m, max(1, m.maxhp // 8))
                else:
                    hurt(b, m, max(1, m.maxhp // 8))
                    if battle_over(b):
                        return
            elif b.weather == "Rain" and m.ability == "Rain Dish" and m.hp < m.maxhp:
                heal(m, max(1, m.maxhp // 16))
                reveal(m)
            elif b.weather == "Rain" and m.ability == "Hydration" and m.status:
                m.status, m.sleep, m.toxic = None, 0, 0
                reveal(m)
            elif b.weather == "Sun" and m.ability == "Solar Power":
                hurt(b, m, max(1, m.maxhp // 8))
                reveal(m)
                if battle_over(b):
                    return
    for m in order:
        side = b.p if m.side == "p" else b.b
        if not _end_of_turn_mon(b, side, m):
            return
    if not future_sight_ends(b, order):
        return
    for m in order:
        if m.alive() and m.perish:
            m.perish -= 1
            if m.perish == 0:
                m.hp = 0
                if battle_over(b):
                    return
    if 0 < b.trick_room < 999:
        b.trick_room -= 1
    if b.wonder_room:
        b.wonder_room -= 1          # SIDE_COND_CHECK_STATE_WONDER_ROOM, after Trick Room
    if b.magic_room:
        b.magic_room -= 1           # SIDE_COND_CHECK_STATE_MAGIC_ROOM, after Trick Room
        if not b.magic_room:
            magic_room_ends(b)
    if b.guarded:
        b.p.guard = b.b.guard = None     # the side guards are turn flags too
        b.guarded = False
    if b.snatching:
        for m in b.p.mons + b.b.mons:
            m.snatching = False          # no Snatch waits past the turn, one dragged out too (a turn flag)
        b.snatching = False
    for m in order:
        m.roosting = False          # a turn flag, gone with the turn
        if m.magic_coat:
            m.magic_coat = False    # Magic Coat's turn flag too
        if m.alive():
            m.protecting = False
            m.enduring = False
            m.flinch = False        # a flinch lasts only the turn it is dealt
            m.hit_this_turn = None
            m.hurt_this_turn = False
            m.stat_raised = False
            m.turns_in += 1
    b.turn += 1


def _end_of_turn_mon(b, side, m):
    """One Pokemon's own conditions, in the engine's order
    (MON_COND_CHECK_STATE_*, battle_controller_player.c 1308 to 1335):
    Ingrain, Aqua Ring, its ability, its berry, Leftovers, Leech Seed, poison
    and burn, Nightmare, Curse, binding, the counts (Disable, Encore, Taunt,
    Magnet Rise, Heal Block), Yawn, then the Orbs. False once the battle is
    over."""
    if not m.alive():
        return True
    if m.ingrained and m.hp < m.maxhp and not heal_blocked(m):
        gain = m.maxhp // 16
        heal(m, int(gain * 1.3) if m.item == "Big Root" else gain)
    if m.aqua_ring and not heal_blocked(m):
        heal(m, m.maxhp // 16)
    # Speed Boost (BattleSystem_TriggerTurnEndAbility): +1 Speed at each
    # turn's end but the one it came in on.
    if m.ability == "Speed Boost" and m.turns_in > 0:
        change_stages(m, {"spe": 1})
    elif m.ability == "Moody":
        moody(b, m)
    # Shed Skin (the same step): a status is cured one time in three
    # (Oxide's Generation 5 odds), the message naming the ability. Until
    # 2026-10-14 it did nothing (Ian approved the fix).
    if m.ability == "Shed Skin" and m.status and helps(b, m, "shedskin", 1 / 3):
        m.status, m.sleep, m.toxic = None, 0, 0
        reveal(m)
    if m.ability == "Healer" and b.doubles:
        healer(b, m)
    # Harvest (the same function, battle_lib.c 4225): a berry it used up,
    # Natural Gift's included, grows back while it holds nothing, every turn
    # in sun that Cloud Nine and Air Lock leave alone, and on a coin flip
    # otherwise. Added with Ian's approval (2026-10-13) for Gardenia's
    # Exeggutor; the berry checks just below can then use it this same turn.
    if m.ability == "Harvest" and not m.item and m.recycle and m.recycle.endswith("Berry"):
        if (b.weather == "Sun" and not weather_ignored(b)) or coin(b, "harvest"):
            m.item, m.recycle = m.recycle, None
    if m.item == "Sitrus Berry" and 0 < m.hp <= m.maxhp // 2 and not unnerved(b, m):
        heal(m, m.maxhp // 4)
        consume(m)
    if m.item == "Lum Berry" and (m.status or m.confused) and not unnerved(b, m):
        m.status, m.confused = None, 0
        consume(m)
    if m.item == "Leftovers" or (m.item == "Black Sludge" and "Poison" in m.types):
        heal(m, m.maxhp // 16)
    elif m.item == "Black Sludge" and m.ability != "Magic Guard":
        # HOLD_EFFECT_HP_RESTORE_PSN_TYPE: a holder that is not a Poison type
        # loses an eighth of its maximum HP instead, unless it has Magic
        # Guard. Until 2026-10-14 the Black Sludge did nothing to it (Ian
        # approved the fix).
        hurt(b, m, max(1, m.maxhp // 8))
        if battle_over(b):
            return False
    # MON_COND_CHECK_STATE_LEECH_SEED skips a Magic Guard holder whole: no
    # HP sapped and none given (added 2026-10-14, Ian approved the fix).
    if m.seeded and m.ability != "Magic Guard":
        # The step also needs a standing Pokemon in the seeder's slot, so the
        # turn its seeder faints nothing is sapped; and the seeder is given
        # what the sap took (subscript_leech_seed_effect reads BTLVAR_HIT_DAMAGE),
        # never more than the HP the seeded Pokemon had left. Until 2026-10-14
        # the sap ran with the seeder down and always gave a full eighth (Ian
        # approved the fix).
        foe = foe_of(b, m)
        if foe.alive():
            amount = m.maxhp // 8
            sapped = min(amount, m.hp)
            hurt(b, m, amount)
            # Leech Seed heals no blocked seeder, and a Liquid Ooze holder's
            # sap hurts the seeder instead (drain).
            drain(b, foe, m, sapped)
            if battle_over(b):
                return False
    if m.alive():
        if m.status in ("psn", "tox") and m.ability == "Poison Heal":
            heal(m, m.maxhp // 8)        # Poison Heal: poison heals it an eighth instead
        elif m.status in ("brn", "psn") and m.ability != "Magic Guard":
            # Heatproof halves a burn's bite.
            hurt(b, m, m.maxhp // (16 if m.status == "brn" and m.ability == "Heatproof" else 8))
        elif m.status == "tox" and m.ability != "Magic Guard":
            m.toxic += 1
            hurt(b, m, m.maxhp * m.toxic // 16)
        if battle_over(b):
            return False
    # Nightmare (MON_COND_CHECK_STATE_NIGHTMARE, between the burn and Curse):
    # a quarter of its maximum HP while it sleeps, none with Magic Guard;
    # once it is awake the nightmare ends.
    if m.alive() and m.nightmare:
        if m.status != "slp":
            m.nightmare = False
        elif m.ability != "Magic Guard":
            hurt(b, m, max(1, m.maxhp // 4))
            if battle_over(b):
                return False
    if m.alive() and m.cursed and m.ability != "Magic Guard":
        hurt(b, m, m.maxhp // 4)
        if battle_over(b):
            return False
    if m.alive() and m.bound:
        # MON_COND_CHECK_STATE_BIND: the count falls, and while it stays
        # above 0 the bound Pokemon loses an eighth of its maximum HP, a
        # sixth when its binder holds a Binding Band (Oxide's later-games
        # figures); at 0 the bind ends with no damage. subscript_bind_effect
        # hurts no Magic Guard holder, though its count still runs down
        # (added 2026-10-14). Until 2026-10-15 it took Platinum's sixteenth on
        # each of 2 to 5 turns and freed the Pokemon a turn early (Ian
        # approved the fix).
        m.bound -= 1
        if m.bound and m.ability != "Magic Guard":
            hurt(b, m, engine_divide(m.maxhp, 6 if binding_band(b, m) else 8))
        if battle_over(b):
            return False
    if m.octolocked and m.alive():
        octolock_turn(b, side, m)
    # Salt Cure (MON_COND_CHECK_STATE_SALT_CURE, after binding): an eighth
    # of maximum HP, a quarter for a Water or Steel type; Magic Guard is spared.
    if m.alive() and getattr(m, "salted", False) and m.ability != "Magic Guard":
        hurt(b, m, m.maxhp // (4 if set(m.types) & {"Water", "Steel"} else 8))
        if battle_over(b):
            return False
    # Bad Dreams (MON_COND_CHECK_STATE_BAD_DREAMS, after Salt Cure): a
    # sleeping Pokemon without Magic Guard loses an eighth of its maximum HP
    # for each foe with Bad Dreams standing on the field; the message names
    # the holder's ability. Until 2026-10-14 it did nothing (Ian approved
    # the fix).
    if m.alive() and m.status == "slp" and m.ability != "Magic Guard":
        for foe in (b.b if m.side == "p" else b.p).on_field():
            if m.alive() and foe.alive() and foe.ability == "Bad Dreams":
                reveal(foe)
                hurt(b, m, max(1, m.maxhp // 8))
                if battle_over(b):
                    return False
    # Disable's count (MON_COND_CHECK_STATE_DISABLE, before Taunt's): it
    # runs down a turn's end at a time, and the move is free again at the
    # turn's end after it reached 0, or at once if the Pokemon no longer
    # knows it. Three to six turns after the Disable's own, then.
    if m.disabled is not None:
        if m.disabled_turns and any(x.name == m.disabled for x in m.moves):
            m.disabled_turns -= 1
        else:
            m.disabled, m.disabled_turns = None, 0
    # Encore's count (MON_COND_CHECK_STATE_ENCORE, after Disable's): it runs
    # down in the same way, and ends at once if the move is no longer known
    # or has no PP left.
    if m.encore is not None:
        if m.encore_turns and any(x.name == m.encore for x in m.moves) and m.pp.get(m.encore, 0) > 0:
            m.encore_turns -= 1
        else:
            m.encore, m.encore_turns = None, 0
    if m.rare:
        if m.locked_on:
            m.locked_on -= 1         # MON_COND_CHECK_STATE_LOCK_ON
            if not m.locked_on:
                m.lock_on_by = None
        if m.throat_chop:
            m.throat_chop -= 1       # MON_COND_CHECK_STATE_LOCK_ON lowers Throat Chop's count, silently
        if m.laser_focus:
            m.laser_focus -= 1       # and Laser Focus's (laser_focus)
        if m.charged:
            m.charged -= 1           # MON_COND_CHECK_STATE_CHARGE: at 0 the mark is gone
    if m.taunt:
        m.taunt -= 1
    if m.magnet_rise:
        m.magnet_rise -= 1           # MON_COND_CHECK_STATE_MAGNET_RISE counts it down
    if getattr(m, "heal_block", 0):
        m.heal_block -= 1           # Heal Block counts down at the turn's end
    if m.rare and m.embargo:
        m.embargo -= 1              # MON_COND_CHECK_STATE_EMBARGO: its item works again at 0
        if not m.embargo:
            unlock_item(m)
    if m.alive() and m.yawn:
        m.yawn -= 1
        if m.yawn == 0:
            give_status(b, m, "slp")
    # A Sticky Barb takes an eighth of its holder's maximum HP, unless it has
    # Magic Guard (BattleSystem_TriggerDetrimentalHeldItem, the last step,
    # with the Orbs).
    if m.alive() and m.item == "Sticky Barb" and m.ability != "Magic Guard":
        hurt(b, m, max(1, m.maxhp // 8))
        if battle_over(b):
            return False
    # Toxic Orb and Flame Orb give their holder their status
    # (BattleSystem_TriggerDetrimentalHeldItem, the last step).
    if m.alive() and m.item in ("Toxic Orb", "Flame Orb") and not m.status:
        b.status_src = None
        give_status(b, m, "tox" if m.item == "Toxic Orb" else "brn")
    return True


# ---- the player's policy -----------------------------------------------------------------------

def exp_damage(b, att, dfn, mv):
    """A move's expected damage a turn, for the player's reckoning: the
    middle roll with stages, burn and screens, times accuracy, a two-turn
    move at half."""
    r = b.rolls(att, dfn, mv)
    if r is None:
        return 0.0
    d = (b.damage(att, dfn, mv, roll=len(r) // 2) or 0) * expected_hit_scale(mv, att) * reckless_fix(att, mv)
    acc = 1.0 if mv.acc == 0 else min(1.0, mv.acc / 100)
    if mv.effect in TWO_TURN or mv.effect == "RECHARGE_AFTER":
        d /= 2
    if mv.effect in SELF_KO or mv.effect in ("HIT_FIRST_IF_TARGET_ATTACKING",
                                            "ALWAYS_FLINCH_FIRST_TURN_ONLY", "HIT_IN_3_TURNS"):
        return 0.0
    return d * acc


def best_attack(b, att, dfn):
    usable = [m for m in att.moves if m.damaging() and att.pp.get(m.name, 1) > 0
              and (not att.choice or m.name == att.choice) and not disabled_out(att, m)]
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
                b.weather, b.weather_turns = None, 0
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
    if me.encore is not None:
        return "move", encored_move(me, me.moves[0])      # Encore leaves it one move
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
        if mv.cat != "Status" or me.pp.get(mv.name, 1) <= 0 or me.taunt or disabled_out(me, mv):
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
    trade a Pokemon for a hit when another move will do. Rock Head and
    Magic Guard spare it the recoil, and Magic Guard the crash, as the
    battle does."""
    if mv.effect in RECOIL and me.ability not in RECOIL_PROOF:
        r = b.rolls(me, foe, mv)
        top = b.damage(me, foe, mv, roll=len(r) - 1) if r else 0
        return int(min(top or 0, foe.hp) * RECOIL[mv.effect]) >= me.hp
    if mv.effect in CRASH and mv.acc and mv.acc < 100 and me.ability != "Magic Guard":
        return me.maxhp // 2 >= me.hp
    return False


def safe_attack(b, me, foe):
    """The player's best attack, leaving out any that could faint the user
    while one that cannot still does damage."""
    usable = [m for m in me.moves if m.damaging() and me.pp.get(m.name, 1) > 0
              and (not me.choice or m.name == me.choice) and not tormented_out(me, m)
              and not disabled_out(me, m) and not ((me.rare or b.gravity) and move_barred(b, me, m))]
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
        hold(st, m, held.get(m.key))
    bm = [Mon(k, st["pokemon"][k], st["info"][k], st["moves"][k], "b") for k in boss_keys]
    b = Battle(st, Side(pm, "p"), Side(bm, "b"), rng, weather=st.get("base_weather"),
               trick_room=trick_room, ai_flags=flags)
    b.p.active = player_replacement(b) or 0
    open_battle(b)
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
            b.p.cur().switched_turn = b.turn     # it came in by its side's choice (beak_doubles)
        if ba[0] == "switch":
            switch_in(b, b.b, ba[1])
            b.b.cur().switched_turn = b.turn
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
            if move_priority(a, ma) != move_priority(c, mc):
                order.sort(key=lambda o: -move_priority(o[0], o[1]))
            elif not b.faster(a, c):
                order.reverse()
        for i, (mon, mv, _t) in enumerate(order):
            if i and forced_out(b, mon):
                continue                 # dragged out before its turn (forced_out)
            target = foe_of(b, mon)
            first = i == 0 and len(order) == 2
            use_move(b, mon, mv, target, first)
            if mon.wished:
                wish_comes_true(b, mon, lambda side: player_replacement(b) if side is b.p
                                else fightai.replacement(b, side, foe_of(b, mon)))
            if getattr(mon, "u_turn", False) or getattr(mon, "baton", False):
                passing = mon.baton
                mon.u_turn = mon.baton = False   # as perfectline._turn: no switch for a fallen user or a beaten side
                side = b.p if mon.side == "p" else b.b
                if mon.alive() and (b.b if mon.side == "p" else b.p).alive() and side.bench():
                    idx = player_replacement(b) if side is b.p else fightai.replacement(b, side, foe_of(b, mon))
                    if idx is not None and idx != side.active:
                        (baton_pass if passing else switch_in)(b, side, idx)
        end_of_turn(b)
        for mon in (b.p.cur(), b.b.cur()):
            if rollout_lock_ticks(mon):
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


def pollen_puff_heal(att, dfn):
    """Pollen Puff aimed at its user's ally (effect script 380's IfSameSide
    branch, subscript_pollen_puff_heal): once the move has met the ally's
    Protect, hidden turn and accuracy as a hit would, the ally gets back half
    its maximum HP, rounded up, in place of any damage; nothing at full HP
    (subscript_recover_hp), and Heal Block on the ally does not stop it. A
    Telepathy ally takes nothing, as from any partner's move with power
    (perfectline.attack), and a Bulletproof ally nothing either, as Pollen
    Puff is on sBallAndBombMoves and the immunity abilities' check
    (BattleSystem_TriggerImmunityAbility) runs past the script's
    SYSCTL_IGNORE_IMMUNITIES, unless the user's Mold Breaker gets past it.
    Until 2026-10-21 a double battle's Pollen Puff hit its user's ally (Ian
    approved the double-battle part batch 7 left on 2026-10-14)."""
    if dfn.ability == "Bulletproof" and not mold(att, dfn):
        reveal(dfn)
        return
    if dfn.alive() and dfn.hp < dfn.maxhp:
        heal(dfn, (dfn.maxhp + 1) // 2)


def after_you(b, att, dfn):
    """After You (effect script 305, subscript_handle_after_you,
    ChangeExecutionOrderPriority): in a double battle its target, yet to act
    this turn, acts next, straight after the user, the Pokemon in between
    each one place later (the turn's order, Battle.queue); it fails on a
    target that has acted or is not in the order. In a single battle its
    target, the foe, is next already or has acted, so it changes nothing.
    Until 2026-10-21 it did nothing in a double battle (Ian approved the
    double-battle part batch 7 left on 2026-10-14)."""
    queue = b.queue
    if not b.doubles or queue is None:
        return
    pos = next((i for i, a in enumerate(queue) if a[0] is dfn), None)
    if pos is None or pos <= b.queue_pos or dfn in b.moved:
        return
    queue.insert(b.queue_pos + 1, queue.pop(pos))


def follow_me(b, att, mv):
    """Follow Me, Rage Powder and Spotlight (effect script 172,
    BtlCmd_FollowMe): in a double battle the user's slot becomes its side's
    center of attention for the rest of the turn, so the other side's
    single-target moves and its random-target ones go to the Pokemon in it
    while that one stands (center, read by targets_of as BattleSystem_Defender
    reads sideConditions.followMe). Oxide's Spotlight runs Follow Me's script
    too, so it is its user, not its target, that draws the moves; its target
    can stop it by protecting. In a single battle it changes nothing. Until
    2026-10-21 it did nothing in a double battle (Ian approved the fix on
    2026-10-14 with the gaps list's MAKE_GLOBAL_TARGET row)."""
    if not b.doubles:
        return
    side = b.p if att.side == "p" else b.b
    side.follow_me = slot_of(side, att)
    b.following = True


def center(b, att):
    """The Pokemon at the center of attention on att's other side (follow_me),
    standing in the slot its Follow Me was used from, or None."""
    side = b.b if att.side == "p" else b.p
    if side.follow_me is None:
        return None
    idx = side.active2 if side.follow_me == 1 else side.active
    mon = side.mons[idx] if idx is not None else None
    return mon if mon is not None and mon.alive() else None


def targets_of(b, att, mv, chosen, randomize=False):
    """Who a move hits in a double battle: both foes, everyone beside the
    user, a random foe, or the one chosen (the other foe when it is down).
    `randomize`: the target is drawn as a random foe's, as BattleSystem_Defender
    draws a Struggle's (FightCommand's randomizeTarget). A center of
    attention on the other side (follow_me) draws a single-target or
    random-target move, as BattleSystem_Defender sends them to
    sideConditions.followMeUser."""
    foes = foes_of(b, att)
    if mv.range == "ADJACENT_OPPONENTS":
        return foes
    if mv.range == "ALL_ADJACENT":
        ally = ally_of(b, att)
        return foes + ([ally] if ally else [])
    if b.following and (mv.range in ("RANDOM_OPPONENT", "SINGLE_TARGET", "SINGLE_TARGET_ME_FIRST") or randomize):
        mon = center(b, att)
        if mon is not None:
            return [mon]
    if mv.range == "RANDOM_OPPONENT" or randomize:
        return [foes[pick_one(b, "target", len(foes))]] if foes else []
    if mv.range == "ALLY":
        # Helping Hand's and Coaching's target is the user's partner whatever
        # was chosen (BattleSystem_Defender), the user itself with none.
        ally = ally_of(b, att)
        return [ally] if ally is not None else [att]
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
        if me.pp.get(mv.name, 1) <= 0 or (me.choice and mv.name != me.choice) or (me.taunt and mv.cat == "Status") \
                or move_heal_blocked(me, mv) or disabled_out(me, mv) or ((me.rare or b.gravity) and move_barred(b, me, mv)):
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


def helping_hand(b, att):
    """Helping Hand (effect script 176, BtlCmd_TryHelpingHand): in a double
    battle its user's partner, standing and yet to act this turn, has the
    power of its moves raised by half for the rest of the turn (Mon.helped,
    read by state_mult and beat_up_damage, as BattleSystem_CalcMoveDamage,
    BtlCmd_BeatUp and Future Sight's damage read turnFlags.helpingHand). It
    fails in a single battle, on a partner that has acted, fainted or is
    helped already, and for a user its partner has helped. Until 2026-10-21
    it did nothing in a double battle (Ian approved the fix on 2026-10-14
    with the gaps list's BOOST_ALLY_POWER_BY_50_PERCENT row)."""
    if not b.doubles:
        return
    ally = ally_of(b, att)
    if ally is None or ally in b.moved or att.helped or ally.helped:
        return
    ally.helped = True
    b.helping = True


def doubles_replacement(b, side, mon):
    """The party index that comes into mon's slot mid-turn in a double
    battle, from mon's own trainer's party (BattleSystem_AnyReplacementMons:
    a tag battle keeps each trainer's apart), picked as a knockout's is: by
    the player's doubles rule for the player's own Pokemon, else by the
    trainer's AI (BattleAI_PostKOSwitchIn, fightai.replacement). None when
    no one waits on the bench."""
    if not side.bench(owner=mon.owner):
        return None
    if side is b.p and mon.owner == "player":
        idx = player_replacement_doubles(b, side, mon.owner)
    else:
        foes = foes_of(b, mon)
        idx = fightai.replacement(b, side, foes[0] if foes else mon, owner=mon.owner)
    if idx is None or not side.mons[idx].alive() or side.mons[idx] in side.on_field():
        return None
    return idx


def doubles_switch_out(b, mon):
    """U-turn's, Volt Switch's, Flip Turn's and Parting Shot's switch, and
    Baton Pass's, in a double battle (subscript_attack_then_switch_out,
    subscript_parting_shot, subscript_baton_pass), straight after the move:
    no switch once the target's side has nothing left (CheckBlackOut), with
    no one of the user's own party to send in (TryReplaceFaintedMon), or
    when the user fell on the way; otherwise the replacement
    (doubles_replacement) comes into the user's slot, carrying Baton Pass's
    state for a Baton Pass (baton_pass). It does not act this turn. Until
    2026-10-21 the user stayed in (Ian approved the double-battle part of
    batch 10 on 2026-10-15, and of Parting Shot with batch 7's on 2026-10-14)."""
    passing = mon.baton
    mon.u_turn = mon.baton = False
    side = b.p if mon.side == "p" else b.b
    if not mon.alive() or not (b.b if mon.side == "p" else b.p).alive():
        return
    idx = doubles_replacement(b, side, mon)
    if idx is None:
        return
    slot = slot_of(side, mon)
    if passing:
        baton_pass(b, side, idx, slot=slot)
    else:
        switch_in(b, side, idx, slot=slot)


def struggles(b, mon):
    """Whether mon can only Struggle this turn in a double battle: it can
    choose (Battler_CanPickCommand: not locked into a move, charging or
    recharging) and every move it knows is ruled out
    (BattleSystem_CheckInvalidMoves, fightai.invalid: no PP, Disable,
    Torment, Taunt, Imprison, Gravity, Heal Block, Belch, Throat Chop, an
    Assault Vest, Encore, a Choice lock), so the command input gives it
    Struggle (BattleSystem_CheckStruggling), the player's side as the
    trainer's. Until 2026-10-21 neither side ever struggled in a double
    battle: a Pokemon out of PP used a move it could not (Ian approved the
    double battles' path on 2026-10-14)."""
    if mon.lock or mon.charging is not None or mon.recharge:
        return False
    return all(fightai.invalid(b, mon, m) for m in mon.moves)


def doubles_quick(b):
    """Each Pokemon's Quick Claw for the turn, rolled before anyone chooses,
    as in the single battles (perfectline.play_turn): the engine reads
    speedRand, drawn for every battler before the turn (BattleContext_InitCounters,
    then each turn's PRE_MOVE_ACTION_STATE_SPEED_RNG), against the claw's one
    in five, and the trainer's AI reads it too (fightai._first_item). The
    player's side rolls as its luck, the trainer's as the player's bad luck,
    alike at the game's odds."""
    b.quick = {m.key: m.item == "Quick Claw" and (b.dice.good(0.2, "quickclaw") if m.side == "p"
                                                  else b.dice.bad("quickclaw", 0.2))
               for m in b.p.on_field() + b.b.on_field() if m.alive()}
    b.custap = set()


def doubles_order(b, acts):
    """The turn's moves in a double battle in the engine's order
    (BattleControllerPlayer_CalcTurnOrder): an exchange sort over the four
    on BattleSystem_CompareBattlerSpeed, so the higher priority goes first
    (move_priority: Prankster and Gale Wings count); within a priority a
    Quick Claw that fired this turn (doubles_quick) or a Custap Berry in its
    pinch (custap_fires, a quarter of its HP, half with Gluttony, unless
    Unnerve holds it) puts its holder first, and two such holders go by
    Speed; then Speed, the slower first under Trick Room; a tie swaps on a
    coin. A Custap Berry so found is eaten as its holder acts, whatever its
    move's priority (CompareBattlerSpeed sets moveEffectsData.custapBerry,
    which subscript_check_quick_claw reads), and is noted in b.custap. acts
    is [(Pokemon, move, target)], returned in order. Until 2026-10-21 the
    double battles went by priority and Speed alone, so neither item did
    anything (Ian approved the double battles' path on 2026-10-14). Where
    neither has fired, a Lagging Tail or Full Incense, then Stall, puts its
    holder last in the bracket (slow_after); until 2026-10-21 neither
    battle's order had them (Ian approved the fix on 2026-10-21)."""
    quick = {}
    for mon, _mv, _t in acts:
        q = bool(b.quick.get(mon.key))
        if custap_fires(mon, b):
            q = True
            b.custap.add(mon.key)
        quick[mon.key] = q

    def after(x, y):
        """Whether x goes after y: CompareBattlerSpeed's nonzero result."""
        px, py = move_priority(x[0], x[1]), move_priority(y[0], y[1])
        if px != py:
            return px < py
        sx, sy = b.speed(x[0]), b.speed(y[0])
        qx, qy = quick[x[0].key], quick[y[0].key]
        if qx != qy:
            return qy
        if not qx:
            # Lagging Tail and Full Incense, then Stall, once neither
            # Pokemon's Quick Claw or Custap Berry has fired (slow_after).
            slow = slow_after(x[0], y[0], sx, sy, lambda: b.rng.random() < 0.5)
            if slow is not None:
                return slow
        if b.trick_room and not (qx and qy):
            return sx > sy or (sx == sy and b.rng.random() < 0.5)
        return sx < sy or (sx == sy and b.rng.random() < 0.5)

    order = list(acts)
    for i in range(len(order) - 1):
        for j in range(i + 1, len(order)):
            if after(order[i], order[j]):
                order[i], order[j] = order[j], order[i]
    return order


def run_doubles(st, player_keys, boss_groups, rng, boss_flags, partner_keys=(), partner_flags=0,
                trick_room=False):
    """One double battle: (the player's Pokemon lost, whether the player won).
    boss_groups is one party (a doubles trainer fills both slots) or two
    (a tag battle, each opponent filling its own slot); partner_keys is a
    partner's party (Barry), driven by its own flags beside the player.

    Every move is played through perfectline's use_move, attack and
    status_move, on perfectline's dice at the game's odds (RunDice, "real"),
    as the singles readings play them, so each branch they hold runs here
    too: the Berries on a hit, Mean Look and Ingrain, Scope Lens, King's
    Rock, Focus Band, Big Root, Struggle, Magnitude's rolled power and the
    rest. Until 2026-10-21 the double battles ran fightsim's own attack and
    status_move, which lacked them (Ian approved the double battles' path on
    2026-10-14 with the gaps list, simulator-gaps.md's "Double battles")."""
    from . import perfectline as pl      # imported here: perfectline imports this module
    pm = [Mon(k, st["pokemon"][k], st["info"][k], st["moves"][k], "p") for k in player_keys]
    held = assign_items(st, player_keys) if "split" in st else {}
    for m in pm:
        hold(st, m, held.get(m.key))
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
    b.dice = pl.RunDice(rng, luck="real")    # the game's odds on both sides, as pdoubles reports ("dice")
    flags_of = {g: boss_flags[min(g, len(boss_flags) - 1)] for g in range(len(boss_groups))}
    flags_of["partner"] = partner_flags
    # The leads.
    b.b.active = 0
    b.b.active2 = len(boss_groups[0]) if len(boss_groups) == 2 else (1 if len(bm) > 1 else None)
    b.p.active = 0
    b.p.active2 = len(pm) if part else (1 if len(pm) > 1 else None)
    open_battle(b)

    def flags_for(mon):
        return flags_of.get(mon.owner, boss_flags[0])

    while b.turn < MAX_TURNS and b.p.alive() and b.b.alive():
        b.moved = set()
        if b.helping:
            for m in b.p.mons + b.b.mons:
                m.helped = False         # last turn's Helping Hand (a turn flag)
            b.helping = False
        if b.following:
            b.p.follow_me = b.b.follow_me = None     # last turn's center of attention
            b.following = False
        doubles_quick(b)
        acts = []
        for mon in b.p.on_field() + b.b.on_field():
            if not mon.alive():
                continue
            if struggles(b, mon):
                acts.append((mon, move("Struggle"), None))
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
        # The turn's order, held on the battle so that After You can move a
        # Pokemon up in it as the turn runs (after_you).
        b.queue = doubles_order(b, acts)
        b.queue_pos = -1
        while b.queue_pos + 1 < len(b.queue):
            b.queue_pos += 1
            i = b.queue_pos
            ordered = b.queue
            mon, mv, t = ordered[i]
            if not mon.alive() or mon not in (b.p if mon.side == "p" else b.b).on_field():
                continue                 # fainted, or dragged out before its turn (forced_out)
            if mon.key in b.custap:
                consume(mon)             # its Custap Berry, eaten as it acts (subscript_check_quick_claw)
            if t is not None and not t.alive():
                t = None
            if mv.effect == "SKY_DROP" and mon.charging is not None:
                # Sky Drop's drop, aimed at the Pokemon its user holds (the
                # target it lifted, which BattleSystem_Defender keeps).
                t = next((m for m in foes_of(b, mon) if m.sky_holder == mon.key), t)
            tl = targets_of(b, mon, mv, t, randomize=mv.effect == "STRUGGLE")
            first = bool(tl) and tl[0] not in b.moved
            # No standing battler acts after this one (moves_last, for Protect).
            b.moving_last = not any(later[0].alive() for later in ordered[i + 1:])
            # A damaging move goes to each Pokemon it hits, and so does a status
            # move aimed at both foes or every other Pokemon (SPREAD).
            pl.use_move(b, mon, mv, tl[0] if tl else foe_of(b, mon), first,
                        targets=tl if mv.damaging() or (mv.range in SPREAD and tl) else None)
            b.moved.add(mon)
            if mon.wished:
                # Healing Wish and Lunar Dance: the user's replacement now,
                # into its slot (wish_comes_true).
                side = b.p if mon.side == "p" else b.b
                wish_comes_true(b, mon, lambda sd, mon=mon: doubles_replacement(b, sd, mon),
                                slot=slot_of(side, mon), owner=mon.owner)
            if mon.u_turn or mon.baton:
                doubles_switch_out(b, mon)
        b.moving_last = None
        b.queue = None
        end_of_turn(b)
        for mon in b.p.on_field() + b.b.on_field():
            if rollout_lock_ticks(mon):
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
#
# The Pixie Plate, which element 7 added, raises Fairy moves as the engine's
# other Plates raise theirs (sTypeBoostingItems in battle_lib.c, by
# HOLD_EFFECT_ARCEUS_FAIRY), so a player's Pokemon holding one gets the
# fifth too. Until 2026-10-20 its Fairy moves got nothing (Ian approved the
# fix). The Fairy Feather (HOLD_EFFECT_STRENGTHEN_FAIRY) does the same, and
# both are in the census (TYPE_BOOSTERS), which hands out one booster of
# each type: the Fairy Feather from Fantina's split, Camper Anthony's
# reward, and still the Feather once Volkner's split adds Beauty Nicola's
# Pixie Plate, as each type's classic booster comes before its Plate. So a
# Fairy type's Fairy attack takes it as any other type's same-type attack
# takes its booster (assign_items). Until 2026-10-21 neither reached a six,
# and a Fairy Feather held gave nothing (Ian approved the fix on
# 2026-10-20).
BOOSTER_TYPE = {it: t for t, items in TYPE_BOOSTERS.items() for it in items}

# The abilities and moves whose type the battle sets as the move is used
# (move_type_used), so a booster's fifth goes by that type and not by the
# move's own; any other move keeps its own type, which is read at no cost.
RETYPING_ABILITIES = frozenset({"Normalize", "Pixilate", "Liquid Voice"})
RETYPED_MOVES = frozenset({"Weather Ball", "Hidden Power", "Natural Gift"})


def booster_fifth(b, att, mv):
    """Whether the battle adds a type booster's fifth to att's move
    (sTypeBoostingItems, BattleSystem_CalcMoveDamage): only for the player's
    own Pokemon, whose rows are made with no item (prepare, assign_items). A
    tag battle's partner beside the player (keys q0.0 and on) is rowed from
    its trainer's record, its item in the row already, so its fifth is not
    added again. Until 2026-10-21 a partner's booster counted twice (Ian
    approved the fix on 2026-10-20 after batch 14; Barry's partner teams
    hold no item today, so nothing read differently).

    The booster matches the type the move hits with, which
    BattleScript_CalcMoveDamage hands the damage (battleCtx->moveType, or
    Normal for a Normalize user): a Pixilate user's Normal move is Fairy and
    takes the Fairy Feather, Weather Ball takes the booster of its weather's
    type, Hidden Power that of its IVs' type, and a Liquid Voice user's
    sound move Mystic Water (move_type_used). Until 2026-10-21 the check
    read the move's own type, so a Pixilate Sylveon's Swift took nothing
    from its Fairy Feather (Ian approved the fix on 2026-10-21)."""
    if att.side != "p" or att.key[0] == "q":
        return False
    t = BOOSTER_TYPE.get(att.item)
    if t is None:
        return False
    if att.ability in RETYPING_ABILITIES or mv.name in RETYPED_MOVES:
        return move_type_used(att.ability, mv, att.ivs, att.item, weather_now(b)) == t
    return mv.type == t


def plate_key(key, item):
    """The twin a player's Pokemon reads Judgment from while it holds this
    Plate ("<key>#jd<type>", which prepare adds for every Pokemon of the
    player's that knows Judgment), or None for an item that is no Plate."""
    t = JUDGMENT_TYPE.get(item)
    return f"{key}#jd{t}" if t else None


def hold(st, mon, item):
    """A player's Pokemon handed its item as a battle starts (assign_items,
    or a state's own items), its rows made with none. A Plate makes its
    Judgment the Plate's type (effect script 268), for the battle's and the
    trainer's AI's type reads (judgment_move, as Mon gives a trainer's from
    its own record) and for its damage, which it reads from its twin rowed
    at that type (plate_key, Battle.row); the Plate's fifth comes on top
    (BOOSTER_TYPE). Without one Judgment is Normal again. Until 2026-10-20
    a player's Judgment hit as Normal whatever it held (Ian approved the
    fix).

    An Arceus with Multitype is of its Plate's type for every read, not
    Judgment's alone (Battler_MonType), so one handed a Plate takes that
    type for the battle's and the AI's type reads, and every row of its
    from its twin in that form, which for such an Arceus is rowed for every
    move both ways and named in st["form_twin"] (prepare): the battle reads
    it through form_key as it reads a type batch 3's machinery changed,
    kept through switching (Mon.plate_types), its Judgment that twin's too.
    Until 2026-10-21 it stayed Normal everywhere but in its Judgment's
    damage (Ian approved the fix on 2026-10-20)."""
    mon.item = item
    if mon.ability == "Multitype" and mon.species == "Arceus":
        t = JUDGMENT_TYPE.get(item)
        twins = ((st.get("form_twin") or {}).get(mon.key) or {}).get("twins") or {}
        if t and twins.get(((t,), row_ability(mon.ability))):
            mon.moves = [judgment_move(m, item) if m.effect == "JUDGEMENT" else m for m in mon.moves]
            mon.types, mon.base_types = [t], [t]
            mon.plate_types = mon.row_types = (t,)
            mon.formed, mon.plated = True, None
            return
        if mon.plate_types is not None:
            unplate(mon)
    if item not in JUDGMENT_TYPE and mon.plated is None:
        return
    if not any(m.effect == "JUDGEMENT" for m in mon.moves):
        return
    mon.moves = [(judgment_move(m, item) if item in JUDGMENT_TYPE else move(m.name))
                 if m.effect == "JUDGEMENT" else m for m in mon.moves]
    twin = plate_key(mon.key, item)
    mon.plated = twin if twin in st.get("pokemon", ()) else None


def unplate(mon):
    """An Arceus with Multitype left without its Plate, which only its own
    Fling takes from it (Multitype stops Knock Off, Thief, Covet, Trick and
    Pickpocket): Normal again for every read (Battler_MonType's default),
    its rows its own Normal form's, a trainer's its item twin's
    (mark_unheld), and its Judgment Normal."""
    if mon.plate_types is not None:
        mon.plate_types = mon.row_types = None
        mon.formed = False
    mon.types, mon.base_types = ["Normal"], ["Normal"]
    mon.moves = [move(m.name) if m.effect == "JUDGEMENT" else m for m in mon.moves]
    mon.plated = None


def plate_form(rec, poks):
    """A trainer's or a partner's Pokemon as its rows are made: an Arceus
    with Multitype holding a Plate in that Plate's form ("Arceus-Fire" and
    the rest, calc_export's TYPE_FORMS, with Arceus's numbers), since
    Battler_MonType makes it of the Plate's type for every read of the
    battle, and only its own Fling takes the Plate away; any other record
    as it is. Until 2026-10-21 such an Arceus was Normal in every row but
    its Judgment's (Ian approved the fix on 2026-10-20)."""
    t = JUDGMENT_TYPE.get(rec.get("item"))
    if t and rec.get("species") == "Arceus" and rec.get("ability") == "Multitype" and f"Arceus-{t}" in poks:
        return dict(rec, species=f"Arceus-{t}")
    return rec


@functools.lru_cache(maxsize=None)
def player_items(split):
    """{"boosters": {type: item}, "Leftovers": copies, "Sitrus Berry": copies}
    by the split's end: field items, gifts and the items a trainer gives
    straight after the win (step 10's rewards) once each, mart items
    without limit."""
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
    for s, _t, it in sp.trainer_rewards():
        if upto(s):
            finds[name(it)] += 1
    marts ={name(it) for s, _t, it in sp.marts() if upto(s)}
    boosters = {}
    for t, items in TYPE_BOOSTERS.items():       # Fairy's two among them since 2026-10-21
        have = [i for i in items if finds.get(i) or i in marts]
        if have:
            boosters[t] = have[0]
    count = lambda i: 99 if i in marts else finds.get(i, 0)
    return {"boosters": boosters, "Leftovers": count("Leftovers"), "Sitrus Berry": count("Sitrus Berry")}


def assign_items(st, team):
    """{key: item} for a team: a booster for a member's main same-type
    attack when that type's booster is in reach and not yet given, else
    Leftovers, else a Sitrus Berry, while copies last; strongest first. A
    state may name its own stock (st["item_stock"], in player_items' form),
    as a real run's items (plstep3)."""
    stock = st.get("item_stock") or player_items(st["split"])
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


# The status moves that use a foe's move as their user's own, whose users'
# rows carry the foes' damaging moves (prepare's borrowed): Mimic, Mirror
# Move, Copycat, Sketch and Me First.
BORROWS = frozenset({"COPY_MOVE_FOR_BATTLE", "COPY_MOVE", "USE_LAST_USED_MOVE", "LEARN_MOVE_PERMANENT",
                     "USE_MOVE_FIRST"})


def prepare(split, parties, weather=None, trick_room=False, cap=None, partners=(), doubles=False,
            given_side=None, terrain=None, fog=False):
    """Everything a fight's battles read: the strong third of the side, the
    trainer's Pokemon, a partner's teams (keys q0.0 and on), and the
    calculator's rows for every pair in every weather the fight can have;
    in a double battle also each ally's spread moves on its ally. `terrain`
    is the fight's battle terrain (calc.fight_terrain), for Camouflage;
    `fog` whether it is fought in deep fog (calc.fight_fog)."""
    blob = calc.blob()
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
    def friendly(mon):
        """A trainer's Pokemon with Return, Pika Papow or Veevee Volley,
        rowed at its own friendship's power (friendship_power) rather than
        the calculator's full-friendship 102, or with Frustration, rowed at
        its friendship's power (frustration_power) rather than the
        calculator's zero-friendship 102; any other record as it is."""
        own = {}
        for name in mon.get("moves") or ():
            mv = move(name)
            power = {"POWER_BASED_ON_FRIENDSHIP": friendship_power,
                     "POWER_BASED_ON_LOW_FRIENDSHIP": frustration_power}.get(mv.effect)
            if power is not None:
                own[name] = {"type": mv.type, "category": mv.cat, "basePower": power(mon.get("species")),
                             "flags": {"contact": 1} if mv.contact else {}}
        if not own:
            return mon
        return dict(mon, move_data=dict(mon.get("move_data") or {}, **own))

    # A trainer's or a partner's Arceus holding a Plate is rowed in that
    # Plate's form (plate_form), its rows, twins and types the form's.
    boss_keys = []
    for v, party in enumerate(parties):
        keys = []
        for j, mon in enumerate(party):
            k = f"b{v}.{j}"
            pokemon[k] = plate_form(friendly(mon), blob["poks"])
            moves[k] = list(mon["moves"])
            keys.append(k)
        boss_keys.append(keys)
    partner_keys = []
    for v, party in enumerate(partners):
        keys = []
        for j, mon in enumerate(party):
            k = f"q{v}.{j}"
            pokemon[k] = plate_form(mon, blob["poks"])
            moves[k] = list(mon["moves"])
            keys.append(k)
        partner_keys.append(keys)
    # The weathers the fight can have: its own, its Pokemon's abilities', and
    # every weather move on either side.
    weathers = {calc.CALC_WEATHER.get(weather, weather) if weather else None}
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

    # A Pokemon with Mimic can use what it copies from a foe as its own
    # (mimic), so its rows carry every damaging move its foes know, beside
    # its own; every lookup is by the move's name, so the extra moves
    # change nothing else.
    # A Nature Power user's rows carry the move its terrain turns it into
    # (nature_power_move) the same way.
    borrowed = {}
    for k in pkeys + qkeys + bkeys:
        extra = []
        if any(move(m).effect in BORROWS for m in moves[k]):
            foes = pkeys + qkeys if k in bkeys else bkeys
            extra += [m for d in foes for m in hits(d)]
        if any(move(m).effect == "NATURE_POWER" for m in moves[k]):
            extra.append(nature_power_move(terrain))
        if k not in bkeys and any(move(m).effect == "USE_RANDOM_ALLY_MOVE" for m in moves[k]):
            # Assist uses its party's moves (called_move): the player's or a
            # partner's user carries its party mates' damaging moves, as a
            # trainer's rows carry its party's already (party_hits).
            mates = pkeys if k in pkeys else qkeys
            extra += [m for d in mates if d != k for m in hits(d)]
        if k not in bkeys and any(move(m).effect == "USE_LAST_USED_MOVE" for m in moves[k]):
            # Copycat copies the last move any Pokemon used (note_move), the
            # move a Pokemon of its own side used before it came in among
            # them, so the player's or a partner's user carries its own
            # side's damaging moves too, as a trainer's rows carry its
            # party's (party_hits). Until 2026-10-15 such a copy found no
            # row and dealt nothing (Ian approved the fix).
            extra += [m for d in pkeys + qkeys if d.split("~")[0] != k.split("~")[0] for m in hits(d)]
        if extra:
            borrowed[k] = list(dict.fromkeys(extra))

    def with_borrowed(k, mvs):
        return mvs + [m for m in borrowed.get(k, ()) if m not in mvs] if k in borrowed else mvs

    # Every damaging move a Pokemon's rows carry: its own, a trainer's
    # party's (party_hits), and the moves it can borrow (with_borrowed), so
    # a move Copycat, Me First, Mimic, Mirror Move or Sketch takes is rowed
    # against a foe's twins (and from the user's own twins) as against its
    # own keys. Until 2026-10-15 the twins were rowed with a Pokemon's own
    # moves alone, so a borrowed move into a Soaked, Roosting or gassed foe
    # found no row and dealt nothing (Ian approved the fix).
    def all_hits(k):
        return with_borrowed(k, party_hits(k) if k in bkeys else hits(k))
    for w in weathers:
        for a in pkeys + qkeys:
            for d in bkeys:
                pairs.append([a, d, with_borrowed(a, hits(a)), w])
                pairs.append([d, a, with_borrowed(d, party_hits(d)), w])
        if doubles or partners:
            # An ally's spread move on its ally: the player's and a
            # partner's Pokemon on each other, the trainers' on each other.
            for group in ((pkeys + qkeys), bkeys):
                for a in group:
                    if spread(a):
                        pairs += [[a, d, spread(a), w] for d in group if d != a]
    # Magnitude's power is rolled when it is used (MAGNITUDE_POWERS), so the
    # calculator is asked once per power level, each as its own attacker key
    # ("<key>#m<power>") carrying that power, against every foe it can meet,
    # on either side. Until 2026-10-15 only the player's and a partner's
    # Pokemon had these keys, so a trainer's Magnitude found no row and
    # never dealt damage (Ian approved the fix). A Pokemon that can borrow
    # the move (Copycat, Me First, Mimic, Mirror Move, Sketch) gets them too,
    # as it does Present's and Heat Crash's (power_row_keys); until
    # 2026-10-20 a borrowed one dealt nothing (Ian approved the fix).
    takes = {k: all_hits(k) for k in list(pkeys) + list(qkeys) + list(bkeys)
             if any(move(m).effect in BORROWS for m in moves[k])}
    knows = {k: moves.get(k, ()) for k in list(pkeys) + list(qkeys) + list(bkeys)}
    for k in power_row_keys("Magnitude", knows, takes):
        foes = pkeys + qkeys if k in bkeys else bkeys
        for p in MAGNITUDE_POWERS:
            dk = f"{k}#m{p}"
            pokemon[dk] = dict(pokemon[k], move_data={"Magnitude": {
                "type": "Ground", "category": "Physical", "basePower": p}})
            for w in weathers:
                for d in foes:
                    pairs.append([dk, d, ["Magnitude"], w])
    # Present's power is rolled when it is used (present_roll), so the
    # calculator is asked once per power, each as its own attacker key
    # ("<key>#pr<power>") carrying that power, against every foe it can
    # meet, on either side; the calculator gives Present itself no row.
    for k in power_row_keys("Present", knows, takes):
        foes = pkeys + qkeys if k in bkeys else bkeys
        for p in PRESENT_ODDS:
            if p:
                dk = f"{k}#pr{p}"
                pokemon[dk] = dict(pokemon[k], move_data={"Present": {
                    "type": "Normal", "category": "Physical", "basePower": p}})
                for w in weathers:
                    for d in foes:
                        pairs.append([dk, d, ["Present"], w])
    # Heat Crash's power is set by the two Pokemon's weights (weight_power), as
    # Heavy Slam's is, which the calculator works out for Heavy Slam alone:
    # it gives Heat Crash no power, so no row ("damage is not a number").
    # So each Heat Crash user is asked once per power its foes' weights give
    # it, each as its own attacker key ("<key>#hc<power>") against the foes
    # that give that power, on either side (Battle.heat_crash_rolls). Until
    # 2026-10-15 Heat Crash never dealt damage (Ian approved the fix).
    heat_crash = {}
    for k in power_row_keys("Heat Crash", knows, takes):
        for d in (pkeys + qkeys if k in bkeys else bkeys):
            power = weight_power(blob, pokemon[k], pokemon[d])
            heat_crash[(k, d)] = power
            dk = f"{k}#hc{power}"
            pokemon.setdefault(dk, dict(pokemon[k], move_data={"Heat Crash": {
                "type": "Fire", "category": "Physical", "basePower": power}}))
            for w in weathers:
                pairs.append([dk, d, ["Heat Crash"], w])
    # Spit Up's power is 100 for each stockpile it spends (spit_up_key), so the
    # calculator is asked once per count, each as its own attacker key
    # ("<key>#su<power>") carrying that power, against every foe it can meet,
    # on either side (the trainer's Spit Up users are most of them).
    for k in list(pkeys) + list(qkeys) + list(bkeys):
        if "Spit Up" in moves.get(k, ()):
            foes = pkeys + qkeys if k in bkeys else bkeys
            for power in SPIT_UP_POWERS:
                dk = f"{k}#su{power}"
                pokemon[dk] = dict(pokemon[k], move_data={"Spit Up": {
                    "type": "Normal", "category": "Special", "basePower": power}})
                for w in weathers:
                    for d in foes:
                        pairs.append([dk, d, ["Spit Up"], w])
    # The player's Fling, rowed holding each item the player is handed by
    # the split (player_items: the type boosters, Leftovers, the Sitrus
    # Berry), each as its own attacker key ("<key>#fl<item>"), since its own
    # rows carry no item and the calculator powers Fling by the item held
    # (fling_key).
    flingers = [k for k in list(pkeys) + list(qkeys) if "Fling" in moves.get(k, ())]
    held = player_items(split) if flingers else {"boosters": {}}
    flung = [i for i in list(held["boosters"].values()) + [i for i in ("Leftovers", "Sitrus Berry") if held.get(i)]
             if item_fling(i)[0]]
    for k in flingers:
        for item in flung:
            dk = fling_key(k, item)
            pokemon[dk] = dict(pokemon[k], item=item)
            for w in weathers:
                for d in bkeys:
                    pairs.append([dk, d, ["Fling"], w])
    # The player's Natural Gift, rowed holding the Sitrus Berry its rows lack
    # (natural_gift_key), against every trainer Pokemon.
    for k in list(pkeys):
        if "Natural Gift" in moves.get(k, ()):
            dk = f"{k}#ng"
            pokemon[dk] = dict(pokemon[k], item="Sitrus Berry")
            for w in weathers:
                for d in bkeys:
                    pairs.append([dk, d, ["Natural Gift"], w])
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
    # Neutralizing Gas: while a holder stands on the field every other
    # battler's ability is off (Battler_Ability), which the calculator's
    # Generation 4 engine does not know. So each Pokemon that can meet a
    # holder gets a twin with its ability blank (the stand-in, as for the
    # AI's twin), rowed both ways against each holder it can face; in a
    # double battle the gas reaches the whole field, so there every pair a
    # battle can read is rowed again with each side's twins. A variant
    # ("p0~1") shares its Pokemon's twin, since only the ability differs.
    holders = [k for k in pkeys + qkeys + bkeys if pokemon[k].get("ability") == "Neutralizing Gas"]
    gas_twin = {}
    if holders:
        ours = pkeys + qkeys

        def gassed(k):
            ab = pokemon[k].get("ability")
            return bool(ab) and ab not in GAS_PROOF and ab != WEATHER_STAND_IN \
                and pokemon[k].get("item") != "Ability Shield"

        def twin(k):
            if not gassed(k):
                return k
            t = k.split("~")[0] + "#ng"
            if t not in pokemon:
                pokemon[t] = dict(pokemon[k], ability=WEATHER_STAND_IN)
            gas_twin[k] = t
            return t

        def hits_of(k):
            return all_hits(k)
        seen = set()

        def row_twice(a, d, w):
            # a and d are base keys; the twins stand in where the gas reaches.
            ta, td = twin(a), twin(d)
            if (ta, td) == (a, d):
                return
            for x, y, mv in ((ta, td, hits_of(a)), (td, ta, hits_of(d))):
                if (x, y, w) not in seen and mv:
                    seen.add((x, y, w))
                    pairs.append([x, y, mv, w])
        whole_field = doubles or bool(partners)
        for w in weathers:
            for a in ours:
                for d in bkeys:
                    if whole_field or (a in holders) != (d in holders):
                        row_twice(a, d, w)
            if whole_field:
                for group in (ours, bkeys):
                    for a in group:
                        if spread(a):
                            for d in group:
                                ta, td = twin(a), twin(d)
                                if d != a and (ta, td) != (a, d) and (ta, td, w) not in seen:
                                    seen.add((ta, td, w))
                                    pairs.append([ta, td, spread(a), w])
        # Magnitude's power keys, for a twin that can meet the gas, on either
        # side (a trainer's since 2026-10-15).
        for k in ours + bkeys:
            if "Magnitude" in moves.get(k, ()) and twin(k) != k:
                held = bkeys if k not in bkeys else ours
                for p in MAGNITUDE_POWERS:
                    dk, tdk = f"{k}#m{p}", f"{twin(k)}#m{p}"
                    pokemon.setdefault(tdk, dict(pokemon[dk], ability=WEATHER_STAND_IN))
                    gas_twin[dk] = tdk
                    for w in weathers:
                        for d in held:
                            if (whole_field or d in holders or k in holders) and (tdk, twin(d), w) not in seen:
                                seen.add((tdk, twin(d), w))
                                pairs.append([tdk, twin(d), ["Magnitude"], w])
    # Roost: while its user roosts, its Flying type meets no move until the
    # turn ends (BasicTypeMulApplies skips the chart's rows for a roosting
    # defender's Flying type), which the calculator cannot know. So each
    # Roost user with the Flying type gets a twin with its types less Flying
    # (species_data with exact types, its own stats and weight kept, which
    # the runner builds on an alias of its species, as the calculator's
    # species table would otherwise keep a second type), rowed for every
    # foe's moves into it, a player's Magnitude at each power included. A pure
    # Flying Pokemon is left with no type the chart reads, which the
    # calculator cannot be given; its Normal and Grass twins between them hit
    # every move type neutrally (roost_key picks).
    roost_twin = {}
    for k in pkeys + qkeys + bkeys:
        if not any(move(m).effect == "HEAL_HALF_REMOVE_FLYING_TYPE" for m in moves[k]):
            continue
        poks = blob["poks"].get(pokemon[k]["species"]) or {}
        types = [t for t in (poks.get("types") or []) if t]
        if "Flying" not in types or not poks.get("bs"):
            continue
        rest = [t for t in types if t != "Flying"]
        foes = pkeys + qkeys if k.startswith("b") else bkeys
        for i, tt in enumerate([rest] if rest else [["Normal"], ["Grass"]]):
            t = f"{k}#roost{i}"
            own = {"bs": dict(poks["bs"]), "types": tt, "exact_types": True}
            if poks.get("weightkg") is not None:
                own["weightkg"] = poks["weightkg"]
            pokemon[t] = dict(pokemon[k], species_data=own)
            roost_twin.setdefault(k, []).append((t, tt))
            for w in weathers:
                for d in foes:
                    got = all_hits(d)
                    if got:
                        pairs.append([d, t, got, w])
                    if "Magnitude" in moves.get(d, ()):     # a trainer's power keys too, since 2026-10-15
                        for p in MAGNITUDE_POWERS:
                            pairs.append([f"{d}#m{p}", t, ["Magnitude"], w])
    # Foresight and Odor Sleuth let Normal and Fighting moves meet an
    # identified target's Ghost type (identified), which the calculator's
    # rows cannot know. So each Ghost type whose foes can identify it gets a
    # twin typed without Ghost (species_data with exact types, its own stats
    # and weight kept, as Roost's twins are; a pure Ghost's twin is Water,
    # which Normal and Fighting moves both hit neutrally), rowed for every
    # foe's Normal and Fighting moves into it (all of a Normalize holder's).
    foresight_twin = {}
    for k in pkeys + qkeys + bkeys:
        foes = pkeys + qkeys if k.startswith("b") else bkeys
        if not any(move(m).effect == "FORESIGHT" for d in foes for m in moves[d]):
            continue
        poks = blob["poks"].get(pokemon[k]["species"]) or {}
        types = [t for t in (poks.get("types") or []) if t]
        if "Ghost" not in types or not poks.get("bs"):
            continue
        t = f"{k}#fs"
        own = {"bs": dict(poks["bs"]), "types": [x for x in types if x != "Ghost"] or ["Water"], "exact_types": True}
        if poks.get("weightkg") is not None:
            own["weightkg"] = poks["weightkg"]
        pokemon[t] = dict(pokemon[k], species_data=own)
        foresight_twin[k] = t
        for w in weathers:
            for d in foes:
                got = [m for m in (all_hits(d))
                       if move(m).type in IDENTIFIED_TYPES or pokemon[d].get("ability") == "Normalize"]
                if got:
                    pairs.append([d, t, got, w])
    # Power Trick and Power Shift swap their user's Attack and Defense stats
    # (power_trick), which the calculator's rows cannot know. So each user
    # gets a twin built with the two swapped: its base stats, IVs and EVs
    # for the two exchanged, and the nature whose effect on them is its
    # own's swapped (swapped_nature), so its final Attack and Defense are
    # each other's; its types, ability, item and the rest kept. The twin is
    # rowed both ways against every foe.
    trick_twin = {}
    for k in pkeys + qkeys + bkeys:
        if not any(move(m).effect == "SWAP_ATK_DEF" for m in moves[k]):
            continue
        poks = blob["poks"].get(pokemon[k]["species"]) or {}
        if not poks.get("bs"):
            continue

        def swap(d):
            d = dict(d or {})
            if "at" in d or "df" in d:
                d["at"], d["df"] = d.get("df"), d.get("at")
            return d
        t = f"{k}#trick"
        own = {"bs": swap(poks["bs"]), "types": [x for x in (poks.get("types") or []) if x]}
        if poks.get("weightkg") is not None:
            own["weightkg"] = poks["weightkg"]
        rec = dict(pokemon[k], species_data=own, nature=swapped_nature(pokemon[k].get("nature")))
        for part in ("ivs", "evs"):
            if pokemon[k].get(part):
                rec[part] = swap(pokemon[k][part])
        pokemon[t] = rec
        trick_twin[k] = t
        foes = pkeys + qkeys if k in bkeys else bkeys
        mine = all_hits(k)
        for w in weathers:
            for d in foes:
                if mine:
                    pairs.append([t, d, mine, w])
                got = all_hits(d)
                if got:
                    pairs.append([d, t, got, w])
    # Miracle Eye lets Psychic moves meet a marked target's Dark type
    # (eyed), which the calculator's rows cannot know. So each Dark type
    # whose foes can use it gets a twin typed without Dark (a pure Dark's
    # twin is Water, which Psychic moves hit neutrally), made as Foresight's
    # twins are, and rowed for every foe's Psychic moves into it, and the
    # moves whose type the battle sets (KEEP_TYPE: Hidden Power and kin).
    miracle_twin = {}
    for k in pkeys + qkeys + bkeys:
        foes = pkeys + qkeys if k.startswith("b") else bkeys
        if not any(move(m).effect == "IGNORE_EVATION_REMOVE_DARK_IMMUNE" for d in foes for m in moves[d]):
            continue
        poks = blob["poks"].get(pokemon[k]["species"]) or {}
        types = [t for t in (poks.get("types") or []) if t]
        if "Dark" not in types or not poks.get("bs"):
            continue
        t = f"{k}#me"
        own = {"bs": dict(poks["bs"]), "types": [x for x in types if x != "Dark"] or ["Water"], "exact_types": True}
        if poks.get("weightkg") is not None:
            own["weightkg"] = poks["weightkg"]
        pokemon[t] = dict(pokemon[k], species_data=own)
        miracle_twin[k] = t
        for w in weathers:
            for d in foes:
                got = [m for m in (all_hits(d))
                       if move(m).type == "Psychic" or move(m).const in KEEP_TYPE]
                if got:
                    pairs.append([d, t, got, w])
    # Smack Down holds a Flying type or a Levitate holder to the ground
    # (grounded), which the calculator's rows cannot know: they read its
    # Ground immunity. So each such Pokemon whose foes can bring it down
    # gets a twin typed without Flying (Normal for a pure Flying one, which
    # Ground moves hit neutrally), with Levitate blanked to the stand-in and
    # an Air Balloon taken off, made as Roost's twins are, and rowed for
    # every foe's Ground moves into it, Magnitude at each power included.
    ground_twin = {}
    gravity = any(move(m).effect == "GRAVITY" for d in moves for m in moves[d])
    for k in pkeys + qkeys + bkeys:
        foes = pkeys + qkeys if k.startswith("b") else bkeys
        # Its own Ingrain grounds it too (grounded), since 2026-10-15.
        if not gravity and not any(move(m).effect == "SMACK_DOWN" for d in foes for m in moves[d]) \
                and not any(move(m).effect == "GROUND_TRAP_USER_CONTINUOUS_HEAL" for m in moves[k]):
            continue
        poks = blob["poks"].get(pokemon[k]["species"]) or {}
        types = [t for t in (poks.get("types") or []) if t]
        levitate = pokemon[k].get("ability") == "Levitate"
        if not ("Flying" in types or levitate) or not poks.get("bs"):
            continue
        t = f"{k}#gd"
        own = {"bs": dict(poks["bs"]), "types": [x for x in types if x != "Flying"] or ["Normal"], "exact_types": True}
        if poks.get("weightkg") is not None:
            own["weightkg"] = poks["weightkg"]
        pokemon[t] = dict(pokemon[k], species_data=own,
                          ability=WEATHER_STAND_IN if levitate else pokemon[k].get("ability"),
                          item=None if pokemon[k].get("item") == "Air Balloon" else pokemon[k].get("item"))
        ground_twin[k] = t
        for w in weathers:
            for d in foes:
                got = [m for m in (all_hits(d)) if move(m).type == "Ground"]
                if got:
                    pairs.append([d, t, got, w])
                if "Magnitude" in moves.get(d, ()):
                    for p in MAGNITUDE_POWERS:
                        pairs.append([f"{d}#m{p}", t, ["Magnitude"], w])
    # Protean and Libero retype their holder to its first move's type
    # (protean), which the calculator's Generation 4 rows cannot know: they
    # give the holder no STAB for it and meet moves on its own types. So
    # each holder gets a twin per type its moves could make it (species_data
    # with that one type, exactly, as Roost's twins have it; its own stats and
    # weight kept), rowed both ways against every foe.
    protean_twin = {}
    for k in pkeys + qkeys + bkeys:
        if pokemon[k].get("ability") not in ("Protean", "Libero"):
            continue
        poks = blob["poks"].get(pokemon[k]["species"]) or {}
        own_types = {t for t in (poks.get("types") or []) if t}
        if not poks.get("bs"):
            continue
        foes = pkeys + qkeys if k.startswith("b") else bkeys
        mine = all_hits(k)
        for kind in sorted({move(m).type for m in moves[k] if move(m).effect != "STRUGGLE"}):
            if own_types == {kind}:
                continue
            t = f"{k}#pt{kind}"
            own = {"bs": dict(poks["bs"]), "types": [kind], "exact_types": True}
            if poks.get("weightkg") is not None:
                own["weightkg"] = poks["weightkg"]
            pokemon[t] = dict(pokemon[k], species_data=own)
            protean_twin.setdefault(k, {})[kind] = t
            for w in weathers:
                for d in foes:
                    if mine:
                        pairs.append([t, d, mine, w])
                    got = all_hits(d)
                    if got:
                        pairs.append([d, t, got, w])
    # A trainer's held item that the fight can take away (the player's or a
    # partner's Knock Off, Thief, Covet, Trick or Switcheroo, Pickpocket or
    # Magician, or the Pokemon's own Fling) and that its rows read (row_item): a twin with
    # no item ("<key>#ni"), rowed both ways in every weather against every
    # foe, which the battle reads once the item is gone (mark_unheld).
    item_twin = {}
    takers = any(move(m).effect in TAKES_ITEM for k in pkeys + qkeys for m in moves[k]) \
        or any(pokemon[k].get("ability") in TAKING_ABILITIES for k in pkeys + qkeys)
    for k in bkeys:
        if not row_item(pokemon[k].get("item")):
            continue
        if not takers and not any(move(m).effect == "FLING" for m in moves[k]):
            continue
        t = f"{k}#ni"
        pokemon[t] = dict(pokemon[k], item=None)
        if pokemon[k].get("ability") == "Multitype" and pokemon[k]["species"].startswith("Arceus-"):
            pokemon[t]["species"] = "Arceus"     # its Plate flung, an Arceus is Normal again (plate_form)
        item_twin[k] = t
        for w in weathers:
            for d in pkeys + qkeys:
                got = with_borrowed(k, party_hits(k))
                if got:
                    pairs.append([t, d, got, w])
                got = with_borrowed(d, hits(d))
                if got:
                    pairs.append([d, t, got, w])
    # Meloetta's Pirouette form, which Relic Song turns it into and out of
    # (relic_song): each Meloetta that knows the move gets a twin of that
    # form ("<key>#pir": its base stats and types from the form's record,
    # pirouette_data, its weight kept), rowed both ways in every weather
    # against every foe.
    meloetta_twin = {}
    for k in pkeys + qkeys + bkeys:
        if pokemon[k].get("species") != "Meloetta" or "Relic Song" not in moves[k]:
            continue
        own = dict(pirouette_data())
        weight = (blob["poks"].get("Meloetta") or {}).get("weightkg")
        if weight is not None:
            own["weightkg"] = weight
        t = f"{k}#pir"
        pokemon[t] = dict(pokemon[k], species_data=own)
        meloetta_twin[k] = t
        for w in weathers:
            for d in (pkeys + qkeys if k in bkeys else bkeys):
                for a, dd, mvs in ((t, d, all_hits(k)), (d, t, all_hits(d))):
                    if mvs:
                        pairs.append([a, dd, mvs, w])
    # The types and abilities other moves and abilities can change
    # (FORM_CHANGES): a twin for each change the fight can produce, rowed
    # both ways against every foe (form_twins). None in a fight without them.
    camo = camouflage_type(terrain)
    form_twin = form_twins(FormFight(pokemon, moves, blob, pkeys, qkeys, bkeys, weathers, camo), pairs,
                           all_hits, spread,
                           doubles or bool(partners), gas_twin)
    # A Mold Breaker attacker reads a Heavy Metal or Light Metal target's
    # own weight (Battler_Weight asks Battler_IgnorableAbility), where the
    # target's rows carry the weight its ability gives it (metal_weight). So
    # each such target of a Mold Breaker foe that knows Low Kick, Grass Knot
    # or Heavy Slam gets a twin at its own weight ("<key>#mw"), rowed for
    # those moves alone, which Battle.row reads for them (metal_raw_key).
    # Heat Crash's power rows have the target's own weight already
    # (weight_power). Until 2026-10-20 a Mold Breaker's weight move read the
    # changed weight (Ian approved the fix).
    metal_raw = {}
    for d in pkeys + qkeys + bkeys:
        if pokemon[d].get("ability") not in METALS:
            continue
        for a in (pkeys + qkeys if d in bkeys else bkeys):
            mvs = [m for m in all_hits(a) if m in WEIGHT_MOVES] if pokemon[a].get("ability") == "Mold Breaker" else []
            if mvs:
                t = metal_raw.setdefault(d, f"{d}#mw")
                pokemon.setdefault(t, dict(pokemon[d]))
                for w in weathers:
                    pairs.append([a, t, mvs, w])
    # The player's Judgment takes its held Plate's type (effect script 268),
    # and a Multitype Arceus holding it is of that type too (Battler_MonType),
    # where the player's rows are made with no item and read it as a Normal
    # move from a Normal Pokemon. So each of the player's Pokemon that knows
    # Judgment gets a twin per Plate type ("<key>#jd<type>", plate_key), its
    # Judgment of that type and an Arceus in that type's form ("Arceus-Fire"
    # and the rest, calc_export's), still holding nothing, rowed for
    # Judgment against every trainer's key and twin; the battle reads it
    # while the Pokemon holds that Plate (hold) and adds the Plate's fifth
    # (BOOSTER_TYPE). None in a fight without the move, which only the
    # Arceus of after the League knows.
    #
    # An Arceus with Multitype is of its Plate's type for every read, not
    # for Judgment's alone (Battler_MonType). So each of the player's Arceus
    # with Multitype has these twins whether or not it knows Judgment, and
    # each in its form is rowed for every move both ways: its moves against
    # every trainer's key and twin, theirs against it (a power key with its
    # one move, carried_moves), in every weather, and in a double battle its
    # allies' spread moves on it and its on them. Each is named in form_twin
    # as its type's change ((type,), its ability as rows read it), which
    # hold sets while it holds that Plate, so the battle reads it through
    # form_key as it reads a type batch 3's machinery changed. Until
    # 2026-10-21 such an Arceus was Normal in every row but its Judgment's
    # (Ian approved the fix on 2026-10-20). None in a fight without one.
    judging = [k for k in pkeys if "Judgment" in moves[k]]
    multitype = [k for k in pkeys if pokemon[k].get("species") == "Arceus" and pokemon[k].get("ability") == "Multitype"]
    if judging or multitype:
        jm = move("Judgment")
        targets = [d for d in pokemon if d.startswith("b")]
        for k in dict.fromkeys(judging + multitype):
            for t in sorted(set(JUDGMENT_TYPE.values())):
                tk = f"{k}#jd{t}"
                pokemon[tk] = dict(pokemon[k], move_data=dict(pokemon[k].get("move_data") or {}, Judgment={
                    "type": t, "category": jm.cat, "basePower": jm.power}))
                formed = k in multitype and f"Arceus-{t}" in blob["poks"]
                if formed:
                    pokemon[tk]["species"] = f"Arceus-{t}"
                if not formed:
                    for w in weathers:
                        for d in targets:
                            pairs.append([tk, d, ["Judgment"], w])
                    continue
                ab = row_ability(pokemon[k].get("ability"))
                form_twin.setdefault(k, {"ability": ab, "twins": {}})["twins"][((t,), ab)] = tk
                mine = all_hits(k)
                for w in weathers:
                    for d in targets:
                        got = carried_moves(d, all_hits)
                        if mine and not POWER_KEY.search(d):
                            pairs.append([tk, d, mine, w])
                        if got:
                            pairs.append([d, tk, got, w])
                    if doubles or partners:
                        for a in pkeys + qkeys:
                            if a.split("~")[0] != k.split("~")[0]:
                                if spread(a):
                                    pairs.append([a, tk, spread(a), w])
                                if spread(k):
                                    pairs.append([tk, a, spread(k), w])
    # The calculator is told to leave off the abilities the battle applies
    # itself as it runs (CALC_ABILITY_OFF), so their effect is counted once,
    # and each Pokemon's gender as the battle has it (calc_gender: "M", "F",
    # or "N" for none), which Rivalry reads (BattleSystem_CalcMoveDamage: a
    # quarter more against its own gender, a quarter less against the
    # other, nothing against a genderless one). Until 2026-10-14 it was told
    # no gender, took every Pokemon as male, and gave a Rivalry holder its
    # quarter more against every male and female foe alike (Ian approved the
    # fix).
    jobs = {}
    for k, p in pokemon.items():
        job = dict(p, ability_on=False) if p.get("ability") in CALC_ABILITY_OFF else dict(p)
        job["calc_gender"] = _gender_of(p) or "N"
        if p.get("ability") in METALS and not k.endswith("#mw"):
            # the weight Heavy Metal or Light Metal gives it; a Mold
            # Breaker's twin of it keeps its own (metal_raw)
            job = metal_weight(blob, job)
        jobs[k] = job
    out = calc.run_node(calc.blob_path(), {"pokemon": jobs, "pairs": pairs})
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
            "base_weather": calc.CALC_WEATHER.get(weather, weather) if weather else None,
            "rock_eff": rock, "trick_room": trick_room, "chart": blob["type_chart"], "split": split,
            "ai_twin": ai_twin, "gas": bool(holders), "gas_twin": gas_twin, "roost_twin": roost_twin,
            "foresight_twin": foresight_twin, "ground_twin": ground_twin, "miracle_twin": miracle_twin,
            "trick_twin": trick_twin, "item_twin": item_twin, "meloetta_twin": meloetta_twin,
            "cloud_nine": any(p.get("ability") in ("Cloud Nine", "Air Lock") for p in pokemon.values()),
            "copycat": any(move(m).effect == "USE_LAST_USED_MOVE" for mv in moves.values() for m in mv),
            "water_sport": any(move(m).effect == "HALVE_FIRE_DAMAGE" for mv in moves.values() for m in mv),
            "mud_sport": any(move(m).effect == "HALVE_ELECTRIC_DAMAGE" for mv in moves.values() for m in mv),
            "heat_crash": heat_crash, "metal_raw": metal_raw,
            "soul_heart": any(p.get("ability") == "Soul Heart" for p in pokemon.values()),
            "protean_twin": protean_twin, "form_twin": form_twin, "camouflage": camo, "terrain": terrain,
            "fog": bool(fog)}


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
    areas = collections.defaultdict(list)
    for e in pool.wild_encounters():
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
    weather = calc.fight_weather(tr_ids)
    cap = fight_cap(fight["split"], key)
    if fight.get("tag"):
        partners = [ox[p]["party"] for p in fight.get("partner_ids", []) if p in ox]
        st = prepare(fight["split"], parties, weather,
                     trick_room_for([t["constant"] for t in trainers], fight.get("trick_room")), cap=cap,
                     partners=partners, doubles=True, terrain=calc.fight_terrain(tr_ids), fog=calc.fight_fog(tr_ids))
        st["battle"] = "tag"
        st["group_flags"] = [t["ai"] for t in trainers]
        st["partner_flags"] = ox[fight["partner_ids"][0]]["ai"] if fight.get("partner_ids") else 0
        return read_fight(st, [st["group_flags"][0]], runs)
    st = prepare(fight["split"], parties, weather,
                 trick_room_for([t["constant"] for t in trainers], fight.get("trick_room")), cap=cap,
                 terrain=calc.fight_terrain(tr_ids), fog=calc.fight_fog(tr_ids))
    return read_fight(st, [t["ai"] for t in trainers], runs)


def trainer(tr_id, runs=RUNS, split=None):
    """An ordinary trainer's reading, in the split the census places it in
    (required.placements); a doubles trainer plays as doubles unless
    PLAY_DOUBLES is off."""
    t = data.oxide_trainers()[tr_id]
    split = split or required.placements()[tr_id]["split"]
    doubles = t.get("battle_type") == "Doubles" and PLAY_DOUBLES and len(t["party"]) > 1
    st = prepare(split, [t["party"]], calc.fight_weather([tr_id]), trick_room_for([t["constant"]]),
                 cap=fight_cap(split), doubles=doubles, terrain=calc.fight_terrain([tr_id]),
                 fog=calc.fight_fog([tr_id]))
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
    for tr, p in sorted(required.placements().items()):
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

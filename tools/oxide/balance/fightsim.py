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
                 "contact", "sound", "pp", "const", "reflectable", "protect")

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
              "BLIZZARD": "frz", "THUNDER": "par",
              # Infernal Parade and Barb Barrage (effect scripts 321, 322).
              "BURN_HIT_DOUBLE_POWER_ON_STATUS": "brn", "POISON_HIT_DOUBLE_POWER_ON_POISONED": "psn"}
FLINCH_HIT = {"FLINCH_HIT", "FLINCH_BURN_HIT", "FLINCH_PARALYZE_HIT", "FLINCH_FREEZE_HIT",
              "FLINCH_MINIMIZE_DOUBLE_HIT", "FLINCH_DOUBLE_DAMAGE_FLY_OR_BOUNCE",
              "UPPER_HAND"}                       # at its 100%, as Fake Out's target flinches
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
# (its Oxide profile, since 2026-10-07).
RISING_HITS = "HIT_THREE_TIMES_RISING_10"
RISING_COUNT = 3
# Triple Axel (effect script 298) hits the same way at 20, 40 and 60: its
# script adds 20 to a power that starts at 0 for every move, so its row
# too is all three hits added up (the calculator's Oxide profile).
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
         "RECOVER_THREE_QUARTERS_DAMAGE_DEALT": 3 / 4}
TWO_TURN = {"FLY", "DIG", "DIVE", "BOUNCE", "SHADOW_FORCE", "CHARGE_TURN_HIGH_CRIT", "CHARGE_TURN_HIGH_CRIT_FLINCH",
            "CHARGE_TURN_DEF_UP", "SOLAR_BEAM", "SKIP_CHARGE_TURN_IN_SUN",
            "CHARGE_TURN_SP_ATK_UP", "CHARGE_TURN_SP_ATK_UP_RAIN_SKIPS"}  # Meteor Beam, Electro Shot
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
CALC_ABILITY_OFF = frozenset({"Unburden", "Intimidate"})


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
        self.pp = {m.name: m.pp for m in self.moves}
        # Whether it knows a move whose rule reads its own history, for the
        # keys that must tell such histories apart (perfectline.mon_key and
        # _ai_mon): Last Resort reads the moves used since it came in, Belch
        # whether it has eaten a Berry this battle.
        self.last_resort = any(m.effect == "FAIL_IF_NOT_USED_ALL_OTHER_MOVES" for m in self.moves)
        self.belch = any(m.const == "MOVE_BELCH" for m in self.moves)
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
        # Leaving the field brings back the types Protean took away.
        if getattr(self, "protean_type", None) is not None:
            self.types = list(self.base_types)
        self.protean_type = None
        self.protean_used = False
        self.last = None
        self.turns_in = 0
        self.hit_this_turn = None        # (category, damage) of the last hit taken this turn
        self.hurt_this_turn = False      # HP lost to anything but a hit this turn (Assurance)
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

    def row(self, att, dfn, mv=None):
        # A Pokemon whose ability the gas has off reads its ability-blank twin's rows.
        ak = att.key if att.gas_stash is None else gas_key(self, att)
        dk = dfn.key if dfn.gas_stash is None else gas_key(self, dfn)
        if att.protean_type:
            ak = protean_key(self, att) or ak     # a Protean user's twin of its new type
        if dfn.protean_type:
            dk = protean_key(self, dfn) or dk
        if dfn.roosting and mv is not None:
            dk = roost_key(self, dfn, mv) or dk     # a roosting target meets the move on its twin without Flying
        w = self.weather if (self.weather, ak, dk) in self.st["rows"] else None
        return self.st["rows"].get((w, ak, dk))

    def rolls(self, att, dfn, mv):
        r = self.row(att, dfn, mv)
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
        s = self.row_speed(mon)
        st = mon.stages["spe"]
        s = s * (10 + 5 * st) // 10 if st >= 0 else s * 10 // (10 - 5 * st)
        if mon.ability == "Quick Feet" and mon.status:
            s = s * 15 // 10
        elif mon.status == "par":
            s //= 4
        if mon.ability == "Unburden" and mon.had_item and not mon.item:
            s *= 2               # canUnburden, set as it came in holding an item
        side = self.p if mon.side == "p" else self.b
        if side.tailwind:
            s *= 2
        return s

    def row_speed(self, mon):
        """The calculator's Speed for this Pokemon in this weather, as its
        damage rows have it: no stages, no status. Under Neutralizing Gas its
        ability-blank twin's, so Swift Swim and the like stop counting."""
        key = mon.key if mon.gas_stash is None else gas_key(self, mon)
        return int(self.st["speed"].get((self.weather, key)) or self.st["speed"].get((None, key)) or 1)

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
        if mv.effect in ("THUNDER", "HURRICANE"):           # Oxide: Hurricane as Thunder in weather
            acc = 100 if self.weather == "Rain" else 50 if self.weather == "Sun" else acc
        if mv.effect == "BLIZZARD" and self.weather == "Hail":
            return True
        eva = 0 if mv.const in IGNORE_TARGET_STAGES else dfn.stages["eva"]
        s = max(-6, min(6, att.stages["acc"] - eva))
        acc = acc * ((3 + s) / 3 if s >= 0 else 3 / (3 - s))
        if att.ability == "Compound Eyes":
            acc *= 1.3
        if att.item == "Wide Lens":
            acc *= 1.1
        if att.ability == "Hustle" and mv.cat == "Physical":
            acc *= 0.8
        return self.rng.random() * 100 < acc


def stage_mult(s):
    return (2 + s) / 2 if s >= 0 else 2 / (2 - s)


# The moves that ignore their target's stat stages, raised or lowered, its
# defensive ones in the damage (BattleSystem_CalcMoveDamage) and its evasion
# in the accuracy check (BattleControllerPlayer_CheckMoveHitAccuracy), as an
# Unaware attacker does. Until 2026-10-14 the readings and fightsim's own
# damage weakened them by the target's stages (Ian approved the fix).
IGNORE_TARGET_STAGES = frozenset({"MOVE_SACRED_SWORD", "MOVE_DARKEST_LARIAT", "MOVE_CHIP_AWAY"})


# ---- the rules of a turn --------------------------------------------------------------------

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
    if target.ability == "Purifying Salt":
        return False             # Oxide: Purifying Salt allows no status at all
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


def entry_abilities(b, mons, intimidate=True):
    """The switch-in check's ability steps for these Pokemon, each step over
    all of them in the order given (monSpeedOrder): the weather abilities, the
    announcement the trainer's AI reads (BattleAI_SetAbility), Intimidate.
    The battle's leads leave Intimidate to open_battle (intimidate False)."""
    for new in mons:
        weather = ABILITY_WEATHER.get(new.ability)
        if weather:
            b.weather, b.weather_turns = weather, 0
    for new in mons:
        if new.ability in ENTRY_ANNOUNCED:
            reveal(new)
    if intimidate:
        intimidate_foes(b, mons)


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
        if (src is not None and src is not mon and src.side != mon.side and src.alive()
                and mon.ability == "Mirror Armor" and src.ability != "Mold Breaker"):
            if src.stages[stat] > -6:
                change_stages(src, {stat: v}, simple=False)
            continue
        if stat_drop_blocked(b, mon, {stat: v}, src=src, intimidate=intimidate) or mon.stages[stat] <= -6:
            continue
        change_stages(mon, {stat: v})
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
    intimidate_foes(b, sorted(leads, key=b.speed, reverse=not b.trick_room))


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
    if mon.item == "Clear Amulet":
        return True
    ab = mon.ability
    if ab in ("Clear Body", "White Smoke") or (intimidate and ab in INTIMIDATE_PROOF) \
            or (ab == "Hyper Cutter" and falls <= {"atk"}) \
            or (ab == "Keen Eye" and falls <= {"acc"}) or (ab == "Big Pecks" and falls <= {"def"}):
        reveal(mon)
        return True
    return False


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
    synchronize(b, target, status)
    cure_berry(target)
    return True


def change_stages(mon, changes, simple=True):
    # Simple doubles every change to its own stages; a drop Mirror Armor
    # turns back keeps the size it had (simple False).
    mult = 2 if simple and getattr(mon, "ability", None) == "Simple" else 1
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
# Every effect whose hits the engine lands one at a time and the calculator's
# row adds up (SetMultiHit in effect scripts 29, 44, 77, 296, 298 and 416):
# the two to five hit moves, the two-hit moves and the three rising ones.
# Triple Dive, Surging Strikes, Population Bomb and Beat Up are left out, as
# neither side can have them today.
HIT_BY_HIT = frozenset({"MULTI_HIT", "HIT_TWICE", "POISON_MULTI_HIT", "HIT_TWICE_AND_FLINCH",
                        "HIT_THREE_TIMES_RISING_10", "HIT_THREE_TIMES_INCREMENT_BASE_POWER_20"})
# The secondary effect each of the two-hit kin rolls once a hit (effect
# scripts 77 and 296 set it for every hit): Twineedle's poison and Double
# Iron Bash's flinch, at the move's chance.
HIT_BY_HIT_EFFECT = {"POISON_MULTI_HIT": "psn", "HIT_TWICE_AND_FLINCH": "flinch"}


def hit_weights(att, mv, hits):
    """Each landed hit's share of the calculator's row, as whole-number
    weights, and the row's whole weight: the row adds up row_hits equal hits
    for a two to five hit move, two for the two-hit moves, and a rising
    move's three hits at their powers."""
    if mv.effect in RISING:
        powers = rising_powers(mv)
        return powers[:hits], sum(powers)
    total = row_hits(att, mv) if mv.effect == "MULTI_HIT" else 2
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
            sub_hit = True
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
        total += dealt
        dfn.hit_this_turn = (mv.cat, dealt)
        if dealt <= 0:
            continue
        berry = resist_berry(b, dfn, mv)
        if berry and dfn.item == berry:
            consume(dfn)
        if added and not sub_hit and dfn.alive() and not stripped and dfn.ability != "Shield Dust":
            p = min(100, (mv.chance or 0) * (2 if att.ability == "Serene Grace" else 1)) / 100
            if added == "psn" and chance("status", p, dfn):
                give_status_by_move(b, att, dfn, mv, "psn")
            elif added == "flinch" and first and chance("flinch", p, dfn):
                dfn.flinch = True
        if dfn.raging and dfn.alive():
            change_stages(dfn, {"atk": 1})
        if not sub_hit:
            contact_ability(b, att, dfn, mv, dealt, chance, pick)
            if first and att.item in ("King's Rock", "Razor Fang") and not dfn.flinch and dfn.alive() \
                    and chance("kingsrock", 0.1, dfn):
                dfn.flinch = True
        berry_check(dfn)
        if dfn.status == "frz" and mv.type == "Fire":
            dfn.status = None
    if held and dfn.item == "Focus Sash":
        consume(dfn)
    return total


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
    berry_check(mon)
    if not mon.hp and mon.ability == "Neutralizing Gas" and b.st.get("gas"):
        gas_update(b, check=False)       # the gas goes with its holder's last HP


# A pinch berry raises a stat by one stage once its holder is at a quarter of
# its HP or less; Sitrus heals a quarter and Oran 10 once at half or less. In
# Generation 4 each fires as soon as the HP drops, not at the end of the turn.
PINCH_BERRIES = {"Apicot Berry": "spd", "Liechi Berry": "atk", "Ganlon Berry": "def",
                 "Salac Berry": "spe", "Petaya Berry": "spa"}


def berry_check(mon):
    if not mon.alive() or not mon.item:
        return
    # Gluttony eats a pinch berry at half its HP, not a quarter.
    if mon.item in PINCH_BERRIES and mon.hp * (2 if mon.ability == "Gluttony" else 4) <= mon.maxhp:
        change_stages(mon, {PINCH_BERRIES[mon.item]: 1})
        consume(mon)
    elif mon.item == "Sitrus Berry" and mon.hp * 2 <= mon.maxhp:
        heal(mon, mon.maxhp // 4)
        consume(mon)
    elif mon.item in ("Oran Berry", "Berry Juice") and mon.hp * 2 <= mon.maxhp:
        heal(mon, 10 if mon.item == "Oran Berry" else 20)
        consume(mon)


def can_switch(mon):
    """False while Block, Mean Look or its own Ingrain holds it in."""
    return mon.trapped_by is None and not mon.ingrained


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
    foes = [m for m in (b.b if att.side == "p" else b.p).on_field() if m.alive()]
    if mv.effect == "SET_SPIKES" or mv.effect == "TOXIC_SPIKES":
        side = b.b if att.side == "p" else b.p
        if side.hazards["spikes" if mv.effect == "SET_SPIKES" else "tspikes"] >= (3 if mv.effect == "SET_SPIKES" else 2):
            return 1
    if mv.name in ("Imprison", "Snatch") or mv.range in PRESSURE_ALL:
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
    if b.st.get("gas"):
        gas_update(b)


def _use_move(b, att, mv, dfn, first, targets=None):
    if not att.alive():
        return
    mv = encored_move(att, mv)
    # Its own record clears with its action, whatever happens
    # (BattleControllerPlayer_ClearFlags), and so does its Destiny Bond.
    att.last_hit_by = None
    att.destiny_bond = False
    b.status_src = att           # a status this move gives comes from att (Synchronize)
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
        att.flinch = False
        return could_not_act(b, att, mv, dfn, targets)
    if disabled_out(att, mv):
        att.choice = None            # subscript_move_is_disabled lets go of a Choice item's lock
        return could_not_act(b, att, mv, dfn, targets)
    if att.confused:
        att.confused -= 1
        if att.confused and b.rng.random() < 0.5:
            hurt(b, att, confusion_damage(att, b.rng))
            return could_not_act(b, att, mv, dfn, targets)
    if att.status == "par" and b.rng.random() < 0.25:
        return could_not_act(b, att, mv, dfn, targets)
    if att.infatuated and b.rng.random() < 0.5:
        return could_not_act(b, att, mv, dfn, targets)     # immobilized by love (CHECK_STATUS_STATE_ATTRACT)
    if (att.taunt and mv.cat == "Status") or tormented_out(att, mv) or move_heal_blocked(att, mv):
        return could_not_act(b, att, mv, dfn, targets)
    mark_hit(b, mv, dfn, True, targets)
    spend_pp(b, att, mv, dfn, targets)
    if mv.effect not in ("PROTECT", "SURVIVE_WITH_1_HP"):
        att.protect_run = 0
    att.last = mv
    if att.item and att.item.startswith("Choice") and not att.choice:
        att.choice = mv.name
    protean(b, att, mv)
    if commit_move(att, mv):
        return                   # Last Resort before every other move was used
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
        status_move(b, att, mv, dfn, first)
        return
    chance = lambda kind, p, victim: b.rng.random() < p      # noqa: E731
    pick = lambda kind, n: b.rng.randrange(n)               # noqa: E731
    if targets is None:
        attack(b, att, mv, dfn, first)
        hit_aftermath(b, att, dfn, mv, chance, pick)
        destiny_bond(att, dfn)
        return
    # A double battle: a spread move hits each target at three quarters.
    b.spread = len(targets) > 1
    for t in targets:
        attack(b, att, mv, t, t not in b.moved)
        hit_aftermath(b, att, t, mv, chance, pick)
    b.spread = False
    for t in targets:
        destiny_bond(att, t)


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
    if att.ability == "Neutralizing Gas" and b.st.get("gas"):
        gas_update(b, check=False)       # a holder's gas is gone before its blast lands, so the target's ability counts
    return True


def attack(b, att, mv, dfn, first):
    b.last_dealt = 0                     # the HP this move took, for the contact abilities
    b.hits_landed = False                # a move of several hits that land_hits landed
    if not dfn.alive():
        return
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
    if dfn.charging is not None and dfn.charging.effect in INVULNERABLE and not reaches(mv, dfn):
        return
    if protected(b, att, mv, dfn):
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
    if mv.name in ("Natural Gift", "Fling"):
        if not att.item or (mv.name == "Natural Gift" and "Berry" not in att.item):
            return
        consume(att, eaten=False)
    if not b.accuracy_hits(att, dfn, mv):
        # subscript_crash_on_miss spares a Magic Guard user (added 2026-10-14,
        # Ian approved the fix).
        if mv.effect == "CRASH_ON_MISS" and att.ability != "Magic Guard":
            hurt(b, att, att.maxhp // 2)
        rollout_after(att, mv, False)
        return
    rollout_after(att, mv, True)
    # The hits this use makes: a two to five hit move's roll, or Fury
    # Cutter's run until a miss (a Loaded Dice skips the later checks).
    hits = 1
    odds = multi_hit_odds(att, mv)
    if odds:
        hits = b.rng.choices([h for h, _w in odds], [w for _h, w in odds])[0]
    elif mv.effect in RISING:
        while hits < RISING_COUNT and (att.item == "Loaded Dice" or b.accuracy_hits(att, dfn, mv)):
            hits += 1
    elif mv.effect in TWO_HITS:
        hits = 2
    if mv.effect in HIT_BY_HIT:
        dealt = _attack_hits(b, att, mv, dfn, first, hits)
        if dealt is None:
            return
        return _after_attack(b, att, mv, dfn, first, dealt)
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
        stage = att.crit_stage + (att.ability == "Super Luck") + (1 if mv.effect.startswith("HIGH_CRITICAL") or
                                  mv.effect.startswith("CHARGE_TURN_HIGH_CRIT") else 0)
        crit = (b.rng.random() < CRIT_RATE[min(stage, 4)] and dfn.ability not in ("Battle Armor", "Shell Armor")
                and not b.st.get("first_battle"))
        dmg = b.damage(att, dfn, mv, crit=crit)
        if dmg is None:
            return
        dmg = use_damage(att, mv, dmg, hits)
        dmg = berry_first_hit(b, dfn, mv, dmg, hits)
        if mv.effect == "DOUBLE_POWER_IF_MOVING_SECOND" and not first:
            dmg *= 2
        # A doubled power meets Technician after it is doubled (doubled_power).
        if mv.effect == "DOUBLE_POWER_WHEN_STATUSED" and att.status:
            dmg = int(dmg * doubled_power(att, mv))
        if mv.effect == "DOUBLE_POWER_IF_HIT" and att.hit_this_turn:
            dmg = int(dmg * doubled_power(att, mv))
        if mv.effect == "DOUBLE_POWER_WHEN_BELOW_HALF" and dfn.hp * 2 <= dfn.maxhp:
            dmg = int(dmg * doubled_power(att, mv))
        if mv.effect == "DOUBLE_POWER_HEAL_SLEEP" and dfn.status == "slp":
            dmg = int(dmg * doubled_power(att, mv))
        if doubled(att, dfn, mv):
            dmg = int(dmg * doubled_power(att, mv))
    if dmg <= 0:
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
    else:
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
        b.last_dealt = dealt
        dfn.hit_this_turn = (mv.cat, dealt)
        if dfn.status == "frz" and mv.type == "Fire":
            dfn.status = None
    _after_attack(b, att, mv, dfn, first, dealt)


def crit_rate(b, att, dfn, mv):
    """The chance a hit of mv lands critical: Oxide's rate at the attacker's
    stage, 0 against Battle Armor or Shell Armor and in the first battle
    (BtlCmd_CalcCrit)."""
    if dfn.ability in ("Battle Armor", "Shell Armor") or b.st.get("first_battle"):
        return 0.0
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
    stripped = sheer_force_strips(att, mv)
    if e in HIT_SELF_STAGES and not (stripped and not HIT_SELF_STAGES[e][1]):
        ch, certain = HIT_SELF_STAGES[e]
        if certain or b.rng.random() * 100 < (mv.chance or 10):
            change_stages(att, ch)
    if e in ("REMOVE_HAZARDS_AND_BINDING", "MORTAL_SPIN"):
        spin(b, att, dfn, e)
    if e == "SWITCH_HIT":
        # U-turn, Volt Switch and Flip Turn switch their user out after any
        # hit, a knockout or a hit on a Substitute too (effect script 228's
        # subscript_attack_then_switch_out runs ON_HIT); the turn does it.
        att.u_turn = True
    if not dfn.alive() or sub_blocks(att, dfn, mv):
        return
    if e == "SALT_CURE":
        # subscript_salt_cure: the target is salted once the hit lands,
        # until it leaves the field; a chance-free effect, so Shield Dust
        # and Sheer Force (sSheerForceEffects) leave it alone.
        dfn.salted = True
    chance = mv.chance or 0
    if dfn.ability == "Shield Dust" or stripped:
        chance = 0
    if att.ability == "Serene Grace":
        chance *= 2
    if e in HIT_STATUS and b.rng.random() * 100 < chance:
        give_status_by_move(b, att, dfn, mv, HIT_STATUS[e])
    if e == "BURN_HIT_IF_STATS_ROSE" and getattr(dfn, "stat_raised", False) and b.rng.random() * 100 < chance:
        give_status_by_move(b, att, dfn, mv, "brn")
    if e == "TRI_ATTACK" and b.rng.random() * 100 < chance:
        give_status_by_move(b, att, dfn, mv, b.rng.choice(["brn", "par", "frz"]))
    if e in FLINCH_HIT and first and b.rng.random() * 100 < chance:
        dfn.flinch = True
    if e == "ALWAYS_FLINCH_FIRST_TURN_ONLY" and first and not stripped:
        dfn.flinch = True
    if dfn.ability == "Inner Focus":
        dfn.flinch = False       # Inner Focus: it never flinches
    if e in ("CONFUSE_HIT", "HURRICANE", "RECOIL_CONFUSE_HIT") and b.rng.random() * 100 < chance \
            and not confusion_blocked(b, att, dfn, hit=True):
        dfn.confused = b.rng.randint(2, 5)
        confusion_berry(dfn)
    if e in HIT_FOE_STAGES and b.rng.random() * 100 < chance:
        lower_stats(b, att, dfn, HIT_FOE_STAGES[e])
    if e == "HIT_AND_PREVENT_HEALING" and not stripped:     # Psychic Noise; Shield Dust does not stop it
        start_heal_block(att, dfn, mv)
    if e in ("BIND_HIT", "WHIRLPOOL") and not dfn.bound:
        dfn.bound = b.rng.randint(2, 5)
    if e in ("REMOVE_HELD_ITEM", "STEAL_HELD_ITEM"):
        dfn.item = None


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


def magnet_rise(att):
    """Magnet Rise (effect script 252): five turns in which Ground moves fail
    on its user, counted down at each turn's end and cleared by a switch. It
    fails while one is running, on a Levitate user, and on one rooted by
    Ingrain (Oxide adds Smack Down, which the simulator does not model)."""
    if not att.magnet_rise and att.ability != "Levitate" and not att.ingrained:
        att.magnet_rise = 5


def tormented_out(mon, mv):
    """Whether Torment rules this move out: a tormented Pokemon cannot pick
    the move it used last (BattleSystem_CheckInvalidMoves'
    CHECK_INVALID_TORMENTED), which a switch or a turn it could not act
    clears."""
    return mon.tormented and mon.last is not None and mon.last.name == mv.name


def disabled_out(mon, mv):
    """Whether Disable rules this move out: it cannot be chosen
    (BattleSystem_CheckInvalidMoves' CHECK_INVALID_DISABLED), Sleep Talk
    cannot call it (BtlCmd_TrySleepTalk asks the same check), and it fails
    if it was chosen before the Disable came (CHECK_STATUS_STATE_DISABLE)."""
    return mon.disabled is not None and mv.name == mon.disabled


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


def consume(mon, eaten=True):
    """A held item used up (BtlCmd_RemoveItem): gone, and kept for Recycle.
    The engine keeps one per battle position, so a Pokemon could recycle
    what the one before it used; here each Pokemon keeps its own. A Berry
    used up is eaten (BattleScript_RecordBerryEaten, for Belch), unless
    Natural Gift or Fling spent it (eaten False)."""
    if eaten and mon.item and mon.item.endswith("Berry"):
        mon.ate_berry = True
    mon.recycle, mon.item = mon.item, None


def recycle(att):
    """Recycle (effect script 184, BtlCmd_TryRecycle): the item its user
    last used up comes back, if it now holds nothing."""
    if not att.item and att.recycle:
        att.item, att.recycle = att.recycle, None


def spite(dfn):
    """Spite (BtlCmd_TrySpite): the target's last move loses 4 PP, or what
    it has left; it fails before the target has moved or with that move at 0."""
    last = dfn.last
    if last is not None and dfn.pp.get(last.name, 0) > 0:
        dfn.pp[last.name] -= min(4, dfn.pp[last.name])


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


def contact_ability(b, att, dfn, mv, dealt, chance, pick):
    """The defender's ability after a contact move hurt it (Static, Poison
    Point, Flame Body, Effect Spore, Cute Charm at 3 in 10; Rough Skin and
    Oxide's Iron Barbs an eighth of the attacker's HP), as battle_lib's
    on-hit switch has them: only when the move did damage (not to a
    Substitute) and its user still stands, a status only on an attacker with
    none. When none of those acted, Oxide's Poison Touch poisons the target
    3 times in 10 (battle_lib, after the switch). `chance(kind, p, victim)`
    and `pick(kind, n)` are the battle's dice."""
    if not mv.contact or dealt <= 0:
        return
    if att.alive() and dfn.ability and _struck_back(b, att, dfn, chance, pick):
        return
    if att.ability == "Poison Touch" and dfn.alive() and not dfn.status and chance("status", 0.3, dfn):
        b.status_src = att
        if give_status(b, dfn, "psn"):
            reveal(att)


def _struck_back(b, att, dfn, chance, pick):
    """The defender's on-hit ability; whether it acted."""
    a = dfn.ability
    b.status_src = dfn           # a status the ability gives comes from dfn (Synchronize)
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
    item-free)."""
    return (b.st["pokemon"].get(mon.key.split("#")[0]) or {}).get("item")


def resist_berry(b, dfn, mv):
    """The resist berry dfn's rows halve this move by, if any: one of the
    move's type, against a super-effective hit (any Normal move for the
    Chilan Berry)."""
    berry = _row_item(b, dfn)
    if mv.cat == "Status" or mv.effect == FUTURE_SIGHT or RESIST_BERRY.get(berry) != mv.type:
        return None                  # Future Sight never meets the type chart, nor a resist berry
    if berry != "Chilan Berry" and effectiveness(b.st["chart"], mv.type, dfn.types) <= 1:
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
    if not berry or dfn.item != berry:
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
    return False


def spin(b, att, dfn, e):
    """Rapid Spin and Mortal Spin on a hit (BtlCmd_RapidSpin): the user is
    freed from a binding move and from Leech Seed, and every hazard on its
    own side is cleared. Oxide's Rapid Spin then raises its user's Speed a
    stage (subscript_rapid_spin); Mortal Spin first poisons its target
    (subscript_mortal_spin) as a secondary effect, which a Substitute,
    Shield Dust and Covert Cloak stop."""
    if (e == "MORTAL_SPIN" and dfn.alive() and not sub_blocks(att, dfn) and dfn.ability != "Shield Dust"
            and dfn.item != "Covert Cloak"):
        give_status_by_move(b, att, dfn, None, "psn")
    att.bound = 0
    att.seeded = False
    side = b.p if att.side == "p" else b.b
    side.hazards = dict.fromkeys(side.hazards, 0)
    if e == "REMOVE_HAZARDS_AND_BINDING" and att.alive():
        change_stages(att, {"spe": 1})


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
    berry = resist_berry(b, dfn, mv)
    if berry and dfn.item != berry:
        m *= 2
    if mv.effect == "INCREASE_POWER_WITH_LESS_HP":
        m *= power_ratio(att, 20, flail_power(att))
    if mv.effect == "DECREASE_POWER_WITH_LESS_USER_HP":
        m *= power_ratio(att, 150, max(1, 150 * att.hp // att.maxhp))
    if mv.effect == "POWER_BASED_ON_LOW_SPEED":
        # Gyro Ball: the row has its power at both Pokemon's starting Speeds;
        # the game takes the turn's, stages and paralysis in them, and so
        # does the trainer's AI (TrainerAI_CalcDamage's MOVE_GYRO_BALL case).
        m *= power_ratio(att, gyro_power(b.row_speed(dfn), b.row_speed(att)), gyro_power(b.speed(dfn), b.speed(att)))
    if mv.const in ("MOVE_STORED_POWER", "MOVE_POWER_TRIP"):
        # BattleScript_ComputedMovePower: 20, and 20 more for each stage its
        # user has raised a stat, accuracy and evasion included; the row is
        # made with none raised. The trainer's AI reckons it the same way
        # (TrainerAI_ComputedMovePower). Until 2026-10-14 it hit at 20 power
        # whatever the stages (Ian approved the fix).
        m *= power_ratio(att, 20, 20 + 20 * sum(s for s in att.stages.values() if s > 0))
    if mv.const == "MOVE_ELECTRO_BALL":
        # The engine reads the Speeds the turn order was worked out from, its
        # stages, paralysis, Tailwind and items in them, as Gyro Ball does;
        # the row has its power at the two Pokemon's starting Speeds. Until
        # 2026-10-14 it kept the opening Speeds' power the whole fight (Ian
        # approved the fix).
        m *= power_ratio(att, electro_power(b.row_speed(att), b.row_speed(dfn)),
                         electro_power(b.speed(att), b.speed(dfn)))
    if mv.const == "MOVE_HARD_PRESS":
        # BattleScript_ComputedMovePower: up to 100 by the share of its HP
        # the target has left, at least 1; the row is made at full HP. Until
        # 2026-10-14 it hit at full power whatever the target's HP (Ian
        # approved the fix).
        m *= power_ratio(att, 100, max(1, 100 * dfn.hp // dfn.maxhp))
    reach = reach_mult(mv, dfn)
    if reach > 1:
        # The effect scripts double the power (POWER_MULTI 20) before
        # Technician is judged; Magnitude, whose power is rolled, doubles.
        m *= power_ratio(att, mv.power, reach * mv.power) if mv.power > 1 else reach
    return m


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
    if berry and dfn.item == berry:
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
    on-hit ability for a move of one hit; for one of several, whose hits
    land_hits took one at a time with their own aftermath, only the Shell
    Bell on their total."""
    if getattr(b, "hits_landed", False):
        shell_bell(att, b.last_dealt)
        return
    after_hit(b, att, dfn, mv, b.last_dealt)
    contact_ability(b, att, dfn, mv, b.last_dealt, chance, pick)


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


def confusion_berry(mon):
    """A Lum or Persim Berry cures confusion the moment it sets in, after
    the move (BattleSystem_TriggerHeldItemOnStatus), and is used up; the
    turn's end, which waited for it until 2026-10-14, is too late for a
    holder that moves after."""
    if mon.confused and mon.item in ("Lum Berry", "Persim Berry"):
        mon.confused = 0
        consume(mon)


def cure_berry(mon):
    """A status-curing berry (or Lum) cures the status it was just given,
    and is used up."""
    if mon.status and mon.status in CURE_BERRY.get(mon.item, ()):
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
    """Held in by the foe's ability: Magnet Pull holds a Steel type, Shadow
    Tag anything without it, Arena Trap anything grounded."""
    foe = foe_of(b, mon)
    if not foe.alive():
        return False
    if foe.ability == "Magnet Pull":
        return "Steel" in mon.types
    if foe.ability == "Shadow Tag":
        return mon.ability != "Shadow Tag"
    if foe.ability == "Arena Trap":
        return "Flying" not in mon.types and mon.ability != "Levitate" and not mon.magnet_rise
    return False


def commit_move(att, mv):
    """A move its user has committed to (its PP spent): Rage marks it to
    rise when hit, until it uses another move; Last Resort's record of the
    moves used since it came in; Truant loafs on its next turn. Whether
    Last Resort fails: until every other move it knows has been used since
    it came in."""
    att.raging = mv.effect == "RAISE_ATK_WHEN_HIT"
    others = {m.name for m in att.moves if m.name != mv.name}
    fails = mv.effect == "FAIL_IF_NOT_USED_ALL_OTHER_MOVES" and (not others or not others <= att.used_moves)
    # BattleSystem_UpdateLastResort's count, which the trainer's AI reads
    # (Expert_LastResort): each move other than Last Resort the first time it
    # is used since its user came in, four at most.
    if mv.effect != "FAIL_IF_NOT_USED_ALL_OTHER_MOVES" and mv.name not in att.used_moves and att.last_resort_count < 4:
        att.last_resort_count += 1
    att.used_moves = att.used_moves | {mv.name}
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


def charge_skipped(b, att, mv):
    """Whether a two-turn move strikes at once: SolarBeam in sun; Electro
    Shot in rain unless Cloud Nine or Air Lock is out, raising Sp. Atk
    (subscript_sp_atk_up_rain_skip); else a Power Herb, spent, raising the
    move's charge stage (subscript_power_herb_skull_bash and _meteor_beam)."""
    if mv.effect in ("SOLAR_BEAM", "SKIP_CHARGE_TURN_IN_SUN") and b.weather == "Sun":
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
    """[(hits, weight)] for a two to five hit move, else None."""
    if mv.effect != "MULTI_HIT":
        return None
    if att.ability == "Skill Link":
        return ((5, 1),)
    if att.item == "Loaded Dice":
        return ((4, 1), (5, 1))
    return MULTI_HIT_ODDS


def row_hits(att, mv):
    """The hits a calculator row adds up for this move (calc_headless.js
    rolls(), move.js): a two to five hit move at its lowest plus one, or its
    most with Skill Link or a Grip Claw; Double Kick's kind at two; else one."""
    if mv.effect == "MULTI_HIT":
        return 5 if att.ability == "Skill Link" or att.item == "Grip Claw" else 3
    return 2 if mv.effect == "HIT_TWICE" else 1


def rising_scale(mv, hits):
    """A rising move's damage over `hits` hits, as a share of its row, which
    adds up all three (rising_powers). Until 2026-10-12 this read the row as
    the first hit alone, so once the calculator began adding the three
    (2026-10-07) Fury Cutter dealt about four times its damage (Ian approved
    the fix)."""
    powers = rising_powers(mv)
    return sum(powers[:hits]) / sum(powers)


def expected_hit_scale(mv):
    """A move's expected damage as a multiple of its calculator row, for the
    reckonings that read rows (exp_damage, plfeat._expected), before the
    first hit's accuracy: a rising move's later hits each need accuracy
    again, and its row adds all three (Triple Axel's too since 2026-10-14).
    A two to five hit move's row counts three hits, close to its expected
    3.1, so it is left as it is."""
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


def custap_fires(mon):
    """A Custap Berry puts its holder first in its priority bracket, like a
    Quick Claw that always fires, at a quarter of its HP or less (half with
    Gluttony), once (HOLD_EFFECT_PINCH_PRIORITY)."""
    return (mon.item == "Custap Berry" and mon.alive()
            and mon.hp * (2 if mon.ability == "Gluttony" else 4) <= mon.maxhp)


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


def protected(b, att, mv, dfn):
    """Whether dfn's Protect stops att's move, as
    BattleControllerPlayer_CheckMoveHitOverrides decides: only a move flagged
    MOVE_FLAG_CAN_PROTECT, so Feint, Shadow Force, Phantom Force, Future
    Sight, Curse, the hazards and the rest pass it. A stopped move lets go
    of its user's lock (Battler_UnlockMoveChoice ends a Rollout's run); a
    contact move stopped by Spiky Shield costs its user an eighth of its
    maximum HP unless it has Magic Guard, and one stopped by Baneful Bunker
    poisons a user with no status (subscript_missed). Oxide's other
    protecting moves (King's Shield, Obstruct, Silk Trap, Burning Bulwark)
    only protect. Until 2026-10-14 Protect stopped every move but Feint
    (Ian approved the fix)."""
    if not dfn.protecting or not mv.protect:
        return False
    rollout_after(att, mv, False)
    guard = dfn.last.name if dfn.last is not None else None
    if mv.contact and att.alive():
        if guard == "Spiky Shield" and att.ability != "Magic Guard":
            hurt(b, att, max(1, att.maxhp // 8))
        elif guard == "Baneful Bunker" and not att.status:
            b.status_src = dfn
            give_status(b, att, "psn")
    return True


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


def lifted(dfn, mv):
    """Whether Magnet Rise makes this Ground move fail on dfn (the type
    check's MOVE_STATUS_MAGNET_RISE): not on a Pokemon rooted by Ingrain or
    holding an Iron Ball, and never for Thousand Arrows."""
    return (mv.type == "Ground" and dfn.magnet_rise and not dfn.ingrained and dfn.item != "Iron Ball"
            and mv.name != "Thousand Arrows")


def status_move(b, att, mv, dfn, first):
    e = mv.effect
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
    if targets_foe and dfn.alive():
        if protected(b, att, mv, dfn):
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
        if absorb(b, att, dfn, mv):
            return               # Thunder Wave into Volt Absorb, Spore into Sap Sipper: taken whole
    if e in STATUS_OF:
        if sub_blocks(att, dfn, mv):
            return
        give_status_by_move(b, att, dfn, mv, STATUS_OF[e])
    elif e == "STATUS_CONFUSE":
        if not sub_blocks(att, dfn, mv) and not confusion_blocked(b, att, dfn):
            dfn.confused = b.rng.randint(2, 5)
            confusion_berry(dfn)
    elif e in ("ATK_UP_2_STATUS_CONFUSION", "SP_ATK_UP_CAUSE_CONFUSION"):
        if not sub_blocks(att, dfn, mv):
            change_stages(dfn, {"atk": 2} if e.startswith("ATK") else {"spa": 1})
            if not confusion_blocked(b, att, dfn):
                dfn.confused = b.rng.randint(2, 5)
                confusion_berry(dfn)
    elif e == "STATUS_SLEEP_NEXT_TURN":
        if not dfn.status and not dfn.yawn and not sub_blocks(att, dfn, mv):
            dfn.yawn = 2
    elif e == "STATUS_LEECH_SEED":
        if "Grass" not in dfn.types and not sub_blocks(att, dfn, mv):
            dfn.seeded = True
    elif e == "PREVENT_HEALING":                             # Heal Block
        start_heal_block(att, dfn, mv)
    elif e in SELF_STAGES:
        change_stages(att, SELF_STAGES[e])
        if e == "DEF_UP_DOUBLE_ROLLOUT_POWER":
            att.curled = True
    elif e in FOE_STAGES:
        if not sub_blocks(att, dfn, mv):
            lower_stats(b, att, dfn, FOE_STAGES[e])
    elif e == "CURSE":
        if "Ghost" in att.types:
            ghost_curse(b, att, dfn, mv)
        else:
            change_stages(att, {"atk": 1, "def": 1, "spe": -1})
    elif e == "MAX_ATK_LOSE_HALF_MAX_HP":
        if att.hp > att.maxhp // 2:
            hurt(b, att, att.maxhp // 2)
            att.stages["atk"] = 6
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
        frac = 2 / 3 if b.weather == "Sun" else 1 / 4 if b.weather else 1 / 2
        heal(att, int(att.maxhp * frac))
    elif e == "REST":
        # subscript_rest fails on the abilities that keep its user awake
        # (rest_blocked), on a Pokemon already asleep ("is already asleep!"),
        # so a Sleep Talk that calls Rest does nothing, and at full HP.
        if not rest_blocked(b, att) and att.hp < att.maxhp and att.status != "slp":
            att.hp, att.status, att.sleep, att.toxic = att.maxhp, "slp", 2, 0
            cure_berry(att)          # a Chesto or Lum Berry wakes it at once
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
        for m in (att, dfn):
            m.stages = dict.fromkeys(STAGE_KEYS, 0)
    elif e in ("HEAL_STATUS", "CURE_PARTY_STATUS"):
        for m in own_side.mons:
            m.status = None
    elif e == "PREVENT_STATUS":
        own_side.safeguard = 5
    elif e == "PREVENT_STAT_REDUCTION":
        mist(own_side)
    elif e == "TAUNT":
        if not dfn.taunt:
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


def switch_in(b, side, index, slot=0, lead=False):
    """A Pokemon comes in to a slot: volatile state resets, hazards bite.
    A lead at the battle's start (`lead`) leaves its Intimidate to
    open_battle, which runs it once every lead is in."""
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
                foe.trapped_by = None
            if foe.infatuated == leaving.key:
                foe.infatuated = None    # love ends when its object leaves (battle_lib's switch-out)
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
    if gas:
        # The gas reads live: a newcomer under it meets the hazards with its
        # ability off, and a holder's arrival or departure turns the others'
        # off or on at once.
        gas_update(b, check=False)
    # subscript_hazards_check sends a Magic Guard holder straight past Toxic
    # Spikes, Spikes and Stealth Rock (to Sticky Web, which the simulator does
    # not lay), so it takes no hazard damage and no poison, and a Poison type
    # holding it does not soak up the Toxic Spikes either. Until 2026-10-14
    # every hazard reached it (Ian approved the fix).
    guarded = new.ability == "Magic Guard"
    if side.hazards["rocks"] and not guarded:
        eff = b.st["rock_eff"].get(new.key, 1)
        hurt(b, new, int(new.maxhp * eff / 8))
    grounded = "Flying" not in new.types and new.ability != "Levitate" and not guarded
    if grounded and side.hazards["spikes"]:
        hurt(b, new, new.maxhp * {1: 1, 2: 1.5, 3: 2}[side.hazards["spikes"]] // 8)
    if grounded and side.hazards["tspikes"]:
        if "Poison" in new.types:
            side.hazards["tspikes"] = 0
        else:
            give_status(b, new, "psn" if side.hazards["tspikes"] == 1 else "tox")
    if gas and gas_update(b):
        return                   # the gas wore off: the whole field's entry abilities went off, the newcomer's with them
    entry_abilities(b, [new], intimidate=not lead)


def end_of_turn(b):
    _end_of_turn(b)
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


def coin(b, kind="tie"):
    """A fair coin through the battle's dice (so the planner enumerates it),
    or its own rng for a battle fightsim plays alone."""
    dice = getattr(b, "dice", None)
    return dice.choice(kind, 2) == 1 if dice is not None else b.rng.random() < 0.5


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
        q1, q2 = quick.get(m1.key) or custap_fires(m1), quick.get(m2.key) or custap_fires(m2)
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
        side.tailwind = max(0, side.tailwind - 1)
        side.safeguard = max(0, side.safeguard - 1)
        side.mist = max(0, getattr(side, "mist", 0) - 1)
    for m in order:
        side = b.p if m.side == "p" else b.b
        if side.wish and m is side.cur():
            side.wish -= 1
            if side.wish == 0 and m.alive() and not heal_blocked(m):
                heal(m, m.maxhp // 2)
    if b.weather_turns:
        b.weather_turns -= 1
        if b.weather_turns == 0:
            # A weather move cleared the map's weather when it began
            # (effect_script_0136 and its siblings clear every weather
            # flag), and only the move's own flag clears now, so the
            # field is left clear rather than returning to the map's.
            b.weather = None
    if b.weather in ("Sand", "Hail"):
        safe = {"Sand": {"Rock", "Ground", "Steel"}, "Hail": {"Ice"}}[b.weather]
        shield = {"Sand": "Sand Veil", "Hail": "Snow Cloak"}[b.weather]
        for m in order:
            if b.weather == "Hail" and m.ability == "Ice Body":
                # BtlCmd_EndOfTurnWeatherEffect: Ice Body heals a sixteenth in
                # hail in place of the hail's bite, below full HP, unless
                # Cloud Nine or Air Lock is out.
                if m.alive() and m.hp < m.maxhp and not weather_ignored(b):
                    heal(m, max(1, m.maxhp // 16))
                continue
            if m.alive() and not set(m.types) & safe and m.ability not in (shield, "Magic Guard"):
                hurt(b, m, m.maxhp // 16)
                if battle_over(b):
                    return
    if b.weather in ("Rain", "Sun") and not weather_ignored(b):
        # Dry Skin (BtlCmd_EndOfTurnWeatherEffect): an eighth of maximum HP
        # back in rain, below full HP, and an eighth lost in sun.
        for m in order:
            if m.alive() and m.ability == "Dry Skin":
                if b.weather == "Rain":
                    if m.hp < m.maxhp:
                        heal(m, max(1, m.maxhp // 8))
                else:
                    hurt(b, m, max(1, m.maxhp // 8))
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
    for m in order:
        m.roosting = False          # a turn flag, gone with the turn
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
    # Harvest (the same function, battle_lib.c 4225): a berry it used up,
    # Natural Gift's included, grows back while it holds nothing, every turn
    # in sun that Cloud Nine and Air Lock leave alone, and on a coin flip
    # otherwise. Added with Ian's approval (2026-10-13) for Gardenia's
    # Exeggutor; the berry checks just below can then use it this same turn.
    if m.ability == "Harvest" and not m.item and m.recycle and m.recycle.endswith("Berry"):
        if (b.weather == "Sun" and not weather_ignored(b)) or coin(b, "harvest"):
            m.item, m.recycle = m.recycle, None
    if m.item == "Sitrus Berry" and 0 < m.hp <= m.maxhp // 2:
        heal(m, m.maxhp // 4)
        consume(m)
    if m.item == "Lum Berry" and (m.status or m.confused):
        m.status, m.confused = None, 0
        consume(m)
    if m.item == "Leftovers" or (m.item == "Black Sludge" and "Poison" in m.types):
        heal(m, m.maxhp // 16)
    # MON_COND_CHECK_STATE_LEECH_SEED skips a Magic Guard holder whole: no
    # HP sapped and none given (added 2026-10-14, Ian approved the fix).
    if m.seeded and m.ability != "Magic Guard":
        foe = foe_of(b, m)
        amount = m.maxhp // 8
        hurt(b, m, amount)
        if foe.alive():
            # Leech Seed heals no blocked seeder, and a Liquid Ooze holder's
            # sap hurts the seeder instead (drain).
            drain(b, foe, m, amount)
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
        m.bound -= 1
        # subscript_bind_effect hurts no Magic Guard holder, though its count
        # still runs down (added 2026-10-14, Ian approved the fix).
        if m.ability != "Magic Guard":
            hurt(b, m, m.maxhp // 16)
        if battle_over(b):
            return False
    # Salt Cure (MON_COND_CHECK_STATE_SALT_CURE, after binding): an eighth
    # of maximum HP, a quarter for a Water or Steel type; Magic Guard is spared.
    if m.alive() and getattr(m, "salted", False) and m.ability != "Magic Guard":
        hurt(b, m, m.maxhp // (4 if set(m.types) & {"Water", "Steel"} else 8))
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
    if m.taunt:
        m.taunt -= 1
    if m.magnet_rise:
        m.magnet_rise -= 1           # MON_COND_CHECK_STATE_MAGNET_RISE counts it down
    if getattr(m, "heal_block", 0):
        m.heal_block -= 1           # Heal Block counts down at the turn's end
    if m.alive() and m.yawn:
        m.yawn -= 1
        if m.yawn == 0:
            give_status(b, m, "slp")
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
    d = (b.damage(att, dfn, mv, roll=len(r) // 2) or 0) * expected_hit_scale(mv) * reckless_fix(att, mv)
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
    if mv.effect == "CRASH_ON_MISS" and mv.acc and mv.acc < 100 and me.ability != "Magic Guard":
        return me.maxhp // 2 >= me.hp
    return False


def safe_attack(b, me, foe):
    """The player's best attack, leaving out any that could faint the user
    while one that cannot still does damage."""
    usable = [m for m in me.moves if m.damaging() and me.pp.get(m.name, 1) > 0
              and (not me.choice or m.name == me.choice) and not tormented_out(me, m)
              and not disabled_out(me, m)]
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
            if move_priority(a, ma) != move_priority(c, mc):
                order.sort(key=lambda o: -move_priority(o[0], o[1]))
            elif not b.faster(a, c):
                order.reverse()
        for i, (mon, mv, _t) in enumerate(order):
            target = foe_of(b, mon)
            first = i == 0 and len(order) == 2
            use_move(b, mon, mv, target, first)
            if getattr(mon, "u_turn", False):
                mon.u_turn = False       # as perfectline._turn: no switch for a fallen user or a beaten side
                side = b.p if mon.side == "p" else b.b
                if mon.alive() and (b.b if mon.side == "p" else b.p).alive() and side.bench():
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
        if me.pp.get(mv.name, 1) <= 0 or (me.choice and mv.name != me.choice) or (me.taunt and mv.cat == "Status") \
                or move_heal_blocked(me, mv) or disabled_out(me, mv):
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
    open_battle(b)

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
        keyed = [(-move_priority(mon, mv), -b.speed(mon) if not b.trick_room else b.speed(mon), rng.random(),
                  mon, mv, t)
                 for mon, mv, t in acts]
        ordered = sorted(keyed, key=lambda x: x[:3])
        for i, (*_k, mon, mv, t) in enumerate(ordered):
            if not mon.alive():
                continue
            if t is not None and not t.alive():
                t = None
            tl = targets_of(b, mon, mv, t)
            first = bool(tl) and tl[0] not in b.moved
            # No standing battler acts after this one (moves_last, for Protect).
            b.moving_last = not any(later[3].alive() for later in ordered[i + 1:])
            use_move(b, mon, mv, tl[0] if tl else foe_of(b, mon), first,
                     targets=tl if mv.damaging() else None)
            b.moved.add(mon)
        b.moving_last = None
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
    for t, items in pool.TYPE_ITEMS.items():
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


def prepare(split, parties, weather=None, trick_room=False, cap=None, partners=(), doubles=False,
            given_side=None):
    """Everything a fight's battles read: the strong third of the side, the
    trainer's Pokemon, a partner's teams (keys q0.0 and on), and the
    calculator's rows for every pair in every weather the fight can have;
    in a double battle also each ally's spread moves on its ally."""
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
            return party_hits(k) if k in bkeys else hits(k)
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
        # Magnitude's power keys, for a twin that can meet the gas.
        for k in ours:
            if "Magnitude" in moves.get(k, ()) and twin(k) != k:
                for p in MAGNITUDE_POWERS:
                    dk, tdk = f"{k}#m{p}", f"{twin(k)}#m{p}"
                    pokemon.setdefault(tdk, dict(pokemon[dk], ability=WEATHER_STAND_IN))
                    gas_twin[dk] = tdk
                    for w in weathers:
                        for d in bkeys:
                            if (whole_field or d in holders) and (tdk, twin(d), w) not in seen:
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
                    got = party_hits(d) if d in bkeys else hits(d)
                    if got:
                        pairs.append([d, t, got, w])
                    if "Magnitude" in moves.get(d, ()) and not d.startswith("b"):
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
        mine = party_hits(k) if k in bkeys else hits(k)
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
                    got = party_hits(d) if d in bkeys else hits(d)
                    if got:
                        pairs.append([d, t, got, w])
    # The calculator is told to leave off the abilities the battle applies
    # itself as it runs (CALC_ABILITY_OFF), so their effect is counted once.
    jobs = {k: dict(p, ability_on=False) if p.get("ability") in CALC_ABILITY_OFF else p
            for k, p in pokemon.items()}
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
            "protean_twin": protean_twin}


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
                     partners=partners, doubles=True)
        st["battle"] = "tag"
        st["group_flags"] = [t["ai"] for t in trainers]
        st["partner_flags"] = ox[fight["partner_ids"][0]]["ai"] if fight.get("partner_ids") else 0
        return read_fight(st, [st["group_flags"][0]], runs)
    st = prepare(fight["split"], parties, weather,
                 trick_room_for([t["constant"] for t in trainers], fight.get("trick_room")), cap=cap)
    return read_fight(st, [t["ai"] for t in trainers], runs)


def trainer(tr_id, runs=RUNS, split=None):
    """An ordinary trainer's reading, in the split the census places it in
    (required.placements); a doubles trainer plays as doubles unless
    PLAY_DOUBLES is off."""
    t = data.oxide_trainers()[tr_id]
    split = split or required.placements()[tr_id]["split"]
    doubles = t.get("battle_type") == "Doubles" and PLAY_DOUBLES and len(t["party"]) > 1
    st = prepare(split, [t["party"]], calc.fight_weather([tr_id]), trick_room_for([t["constant"]]),
                 cap=fight_cap(split), doubles=doubles)
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

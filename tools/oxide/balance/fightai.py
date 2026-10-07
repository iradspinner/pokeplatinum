"""The trainer AI for the fight simulator, from docs/oxide/battle-ai (condensed
2026-09-27): each of the trainer's flags scores its moves from 100, the
highest wins with ties at random, and before that the switch rules decide
whether it switches instead. Singles only for now.

What is modelled, flag by flag, is the rules that decide how a fight plays:
Basic's refusals (immunity, a status on a statused target, a stat at its
limit, a screen or weather already up, healing at full HP, a last Pokemon's
Explosion), Evaluate Attack whole, Expert's routines for status, stat
moves, healing, screens, weather, Trick Room, Tailwind, Protect,
Substitute, hazards, Roar, Explosion and the common conditional attacks,
Setup First Turn, Risky, Prioritize Extremes, Check HP by its bands,
Weather and Harassment. The AI reads its damage at the top roll with no
critical hit. Rules for moves Oxide's trainers rarely carry are left out;
fightsim's report counts the effects it meets without a rule.
"""
import copy
import functools
import json
import os
import re

from . import data, fightsim as fs

BASIC, EVAL, EXPERT, SETUP_FIRST, RISKY, EXTREMES, BATON, TAG, CHECK_HP, WEATHER, HARASS = range(11)

# ---- Audit A (2026-09-30): the score engine, the damage figure, what the AI
# knows of its target, Basic and Evaluate Attack, as script.s and
# trainer_ai.c have them at HEAD. Paste into tools/oxide/balance/fightai.py:
# it replaces NO_CALC, has_comparison, figure, score_moves, choose, basic and
# evaluate_attack, and adds the helpers they call. Fields the simulator does
# not keep yet are read with getattr and a default that leaves the check off.

# sNoDamageCalcMoveEffects (trainer_ai.c 31 to 46): no figure, whatever the power.
# Half recoil (Head Smash's, now Hyper Beam's and its kin's) left the list
# with the move reworks (Ian, 2026-10-06): it is costed as an ordinary attack.
NO_CALC = {"HALVE_DEFENSE", "RECOVER_DAMAGE_SLEEP", "CHARGE_TURN_HIGH_CRIT",
           "CHARGE_TURN_HIGH_CRIT_FLINCH", "RECHARGE_AFTER", "CHARGE_TURN_DEF_UP",
           "SKIP_CHARGE_TURN_IN_SUN", "SPIT_UP", "HIT_LAST_WHIFF_IF_HIT", "LOWER_OWN_ATK_AND_DEF",
           "DECREASE_POWER_WITH_LESS_USER_HP", "HIT_FIRST_IF_TARGET_ATTACKING"}
# sAltPowerMoveEffects (48 to 61): a figure although the listed power is 1.
ALT_POWER = {"RANDOM_POWER_BASED_ON_IVS", "POWER_BASED_ON_LOW_SPEED", "NATURAL_GIFT", "JUDGEMENT",
             "40_DAMAGE_FLAT", "LEVEL_DAMAGE_FLAT", "RANDOM_DAMAGE_1_TO_150_LEVEL",
             "POWER_BASED_ON_FRIENDSHIP", "POWER_BASED_ON_LOW_FRIENDSHIP", "20_DAMAGE_FLAT",
             "INCREASE_POWER_WITH_WEIGHT"}
# sComputedPowerHits (Oxide, 67 to 71): listed at power 1, given a figure.
COMPUTED_POWER_HITS = {"MOVE_ELECTRO_BALL", "MOVE_HARD_PRESS"}
# The engine estimates one hit (BattleSystem_CalcMoveDamage), where the
# calculator's row adds up several (fightsim.row_hits); since the move
# reworks it then rates the move on its expected hits (expected_hits).
# The pinch abilities BattleSystem_CalcMoveDamage applies at a third of HP or
# less; the calculator's rows are made at full HP.
# Hidden Power's types in IV order (TrainerAI_MoveType, the Mystery type skipped).
TRAP_ABILITIES = ("Shadow Tag", "Magnet Pull", "Arena Trap")
NOT_AT_FOE = ("USER", "USER_SIDE", "FIELD", "ALLY", "USER_OR_ALLY")
# Basic_CheckSoundproof's list (script.s 139 to 170).
BASIC_SOUND = {"MOVE_GROWL", "MOVE_ROAR", "MOVE_SING", "MOVE_SUPERSONIC", "MOVE_SCREECH",
               "MOVE_SNORE", "MOVE_UPROAR", "MOVE_METAL_SOUND", "MOVE_GRASS_WHISTLE",
               "MOVE_HYPER_VOICE", "MOVE_BUG_BUZZ", "MOVE_CHATTER", "MOVE_ALLURING_VOICE",
               "MOVE_BOOMBURST", "MOVE_CLANGING_SCALES", "MOVE_CONFIDE", "MOVE_DISARMING_VOICE",
               "MOVE_ECHOED_VOICE", "MOVE_EERIE_SPELL", "MOVE_NOBLE_ROAR", "MOVE_OVERDRIVE",
               "MOVE_PARTING_SHOT", "MOVE_PSYCHIC_NOISE", "MOVE_RELIC_SONG", "MOVE_ROUND",
               "MOVE_SNARL", "MOVE_SPARKLING_ARIA", "MOVE_TORCH_SONG"}
# The engine's sSoundMoves, which Throat Chop reads (battle_lib.c).
SOUND_MOVES = BASIC_SOUND | {"MOVE_HEAL_BELL", "MOVE_HOWL", "MOVE_PERISH_SONG", "MOVE_CLANGOROUS_SOUL"}
# Basic_CheckBulletproof's list (176 to 203), the engine's sBallAndBombMoves.
BALL_AND_BOMB = {"MOVE_ACID_SPRAY", "MOVE_AURA_SPHERE", "MOVE_BARRAGE", "MOVE_BEAK_BLAST",
                 "MOVE_BULLET_SEED", "MOVE_EGG_BOMB", "MOVE_ELECTRO_BALL", "MOVE_ENERGY_BALL",
                 "MOVE_FOCUS_BLAST", "MOVE_GYRO_BALL", "MOVE_ICE_BALL", "MOVE_MAGNET_BOMB",
                 "MOVE_MIST_BALL", "MOVE_MUD_BOMB", "MOVE_OCTAZOOKA", "MOVE_POLLEN_PUFF",
                 "MOVE_PYRO_BALL", "MOVE_ROCK_BLAST", "MOVE_ROCK_WRECKER", "MOVE_SEARING_SHOT",
                 "MOVE_SEED_BOMB", "MOVE_SHADOW_BALL", "MOVE_SLUDGE_BOMB", "MOVE_SYRUP_BOMB",
                 "MOVE_WEATHER_BALL", "MOVE_ZAP_CANNON"}
# Basic_ScoreMoveEffect (236 to 249): the powders less Rage Powder, and the
# Grass status moves aimed at the foe that are not powders.
BASIC_POWDERS = {"MOVE_COTTON_SPORE", "MOVE_POISON_POWDER", "MOVE_SLEEP_POWDER", "MOVE_STUN_SPORE",
                 "MOVE_SPORE", "MOVE_POWDER", "MOVE_MAGIC_POWDER"}
GRASS_STATUS = {"MOVE_LEECH_SEED", "MOVE_GRASS_WHISTLE", "MOVE_WORRY_SEED"}
# The abilities Basic_CheckForImmunity reads through the guess, by the type
# each takes (82 to 93).
ABSORBS_TYPE = {"Volt Absorb": "Electric", "Motor Drive": "Electric", "Lightning Rod": "Electric",
                "Water Absorb": "Water", "Storm Drain": "Water", "Dry Skin": "Water",
                "Flash Fire": "Fire", "Sap Sipper": "Grass", "Levitate": "Ground"}
# Effects whose charge turn MoveIsOnDamagingTurn excludes, so Wonder Guard
# does not flag them while the AI chooses (battle_lib.c 9431 to 9456).
CHARGE_TURN = {"BIDE", "CHARGE_TURN_HIGH_CRIT", "CHARGE_TURN_HIGH_CRIT_FLINCH",
               "CHARGE_TURN_DEF_UP", "SKIP_CHARGE_TURN_IN_SUN", "FLY", "DIVE", "DIG", "BOUNCE",
               "SHADOW_FORCE", "CHARGE_TURN_SP_ATK_UP", "CHARGE_TURN_SP_ATK_UP_RAIN_SKIPS",
               "CHARGE_TURN_PARALYZE_HIT", "CHARGE_TURN_BURN_HIT",
               "CHARGE_TURN_ATK_SP_ATK_SPEED_UP_2", "SKY_DROP"}
# Move_FailsInHighGravity and Move_HealBlocked (battle_lib.c 3757 to 3816).
GRAVITY_FAILS = {"MOVE_FLY", "MOVE_BOUNCE", "MOVE_JUMP_KICK", "MOVE_HI_JUMP_KICK", "MOVE_SPLASH",
                 "MOVE_MAGNET_RISE"}
HEAL_BLOCKED = {"MOVE_RECOVER", "MOVE_SOFTBOILED", "MOVE_REST", "MOVE_MILK_DRINK",
                "MOVE_MORNING_SUN", "MOVE_SYNTHESIS", "MOVE_MOONLIGHT", "MOVE_SWALLOW",
                "MOVE_HEAL_ORDER", "MOVE_SLACK_OFF", "MOVE_ROOST", "MOVE_LUNAR_DANCE",
                "MOVE_HEALING_WISH", "MOVE_WISH", "MOVE_LUNAR_BLESSING", "MOVE_JUNGLE_HEALING"}
# Basic's raising handlers: (the stat at +6 that scores -10, the stats at
# +6 that score -8, refused under Trick Room).
RAISES = {
    "ATK_UP": ("atk", (), False), "ATK_UP_2": ("atk", (), False),
    "DEF_UP": ("def", (), False), "DEF_UP_2": ("def", (), False), "DEF_UP_3": ("def", (), False),
    "DEF_UP_DOUBLE_ROLLOUT_POWER": ("def", (), False),
    "SPEED_UP": ("spe", (), True), "SPEED_UP_2": ("spe", (), True), "AUTOTOMIZE": ("spe", (), True),
    "SP_ATK_UP": ("spa", (), False), "SP_ATK_UP_2": ("spa", (), False),
    "SP_DEF_UP": ("spd", (), False), "SP_DEF_UP_2": ("spd", (), False),
    "DEF_SPD_UP": ("def", ("spd",), False), "ATK_DEF_UP": ("atk", ("def",), False),
    "SP_ATK_SP_DEF_UP": ("spa", ("spd",), False), "ATK_SPD_UP": ("atk", ("spe",), True),
    "ATK_ACC_UP": ("atk", ("acc",), False), "SP_ATK_SP_DEF_SPEED_UP": ("spa", ("spd", "spe"), True),
    "ATK_DEF_ACC_UP": ("atk", ("def", "acc"), False), "SPEED_UP_2_ATK_UP": ("atk", ("spe",), True),
    "ATK_SP_ATK_SPEED_UP_2_DEF_SP_DEF_DOWN": ("atk", ("spa", "spe"), True),
    "ATK_SP_ATK_UP": ("atk", ("spa",), False),
    "ATK_SP_ATK_SPEED_UP_2_LOSE_HALF_MAX_HP": ("atk", ("spa", "spe"), True),
    "CHARGE_TURN_ATK_SP_ATK_SPEED_UP_2": ("spa", ("spd", "spe"), True),
    "ATK_DEF_SPEED_UP": ("atk", ("def", "spe"), True),
    "RAISE_ALL_STATS_LOSE_THIRD_MAX_HP": ("atk", ("def", "spe", "spa", "spd"), False),
}
# Basic's lowering handlers by the stage each reads (the two harsh accuracy
# and evasion drops go to each other's handler, as vanilla sends them).
LOWERS = {"ATK_DOWN": "atk", "ATK_DOWN_2": "atk", "DEF_DOWN": "def", "DEF_DOWN_2": "def",
          "SPEED_DOWN": "spe", "SPEED_DOWN_2": "spe", "SP_ATK_DOWN": "spa", "SP_ATK_DOWN_2": "spa",
          "SP_DEF_DOWN": "spd", "SP_DEF_DOWN_2": "spd", "ACC_DOWN": "acc", "EVA_DOWN": "eva",
          "EVA_DOWN_2": "acc", "ACC_DOWN_2": "eva"}
# The effects Basic_CheckNonStandardDamageOrChargeTurn takes (870 to 882).
NONSTANDARD = {"BIDE", "CHARGE_TURN_HIGH_CRIT", "HALVE_HP", "40_DAMAGE_FLAT", "RECHARGE_AFTER",
               "LEVEL_DAMAGE_FLAT", "RANDOM_DAMAGE_1_TO_150_LEVEL", "COUNTER",
               "INCREASE_POWER_WITH_LESS_HP", "POWER_BASED_ON_FRIENDSHIP", "RANDOM_POWER_MAYBE_HEAL",
               "POWER_BASED_ON_LOW_FRIENDSHIP", "20_DAMAGE_FLAT", "RANDOM_POWER_BASED_ON_IVS",
               "MIRROR_COAT", "CHARGE_TURN_DEF_UP", "HIT_LAST_WHIFF_IF_HIT", "LOWER_OWN_ATK_AND_DEF",
               "SET_HP_EQUAL_TO_USER", "INCREASE_POWER_WITH_WEIGHT", "POWER_BASED_ON_LOW_SPEED",
               "HIGHER_POWER_WHEN_LOW_PP", "INCREASE_POWER_WITH_MORE_HP",
               "INCREASE_POWER_WITH_MORE_STAT_UP"}
# Status effects element 4 added whose effect is not written yet (442 to 456).
UNWRITTEN = {"ADD_THIRD_TYPE_GHOST", "ADD_THIRD_TYPE_GRASS", "APPLY_TERRAINS",
             "CHANGE_TO_PSYCHIC_TYPE", "DECORATE", "ION_DELUGE", "POWDER", "QUASH",
             "SET_ABILITY_TO_SIMPLE", "SHED_TAIL", "STUFF_CHEEKS", "TIDY_UP", "TOXIC_THREAD",
             "WEATHER_SNOW"}


# ---- what the AI knows of its target

_REGULAR = {}


def _regular_abilities(mon):
    """SPECIES_DATA_ABILITY_1 and _2 of the Pokemon's species; the
    calculator's blob is made from the same species data. Kept per species,
    since the blob does not change."""
    got = _REGULAR.get(mon.species)
    if got is None:
        ab = (fs.teamscore._blob()["poks"].get(mon.species) or {}).get("abilities") or {}
        got = _REGULAR[mon.species] = (ab.get("0"), ab.get("1"))
    return got


def ability_of(b, u, mon):
    """AICmd_LoadBattlerAbility as the AI's Pokemon u reads mon (trainer_ai.c
    1217 to 1260): no ability under Gastro Acid; its own side's real ability;
    for a foe, the ability a battle message has named (mon.revealed), else the
    real one if it traps, else a fresh coin between its species' two regular
    slots. Each call is its own flip, as each command is."""
    if getattr(mon, "suppressed", False):
        return None
    # Its own side reads the real ability; so does the player, whose plan
    # knows the trainer's Pokemon (the guess is the trainer AI's alone).
    if mon.side == u.side or u.side == "p":
        return mon.ability
    if getattr(mon, "revealed", None):
        return mon.revealed
    if mon.ability in TRAP_ABILITIES:
        return mon.ability
    a1, a2 = _regular_abilities(mon)
    if a1 and a2:
        return a1 if chance(b, 50) else a2
    return a1 or a2


def check_ability(b, u, mon, name):
    """AICmd_CheckBattlerAbility (1262 to 1317): "have", "not" or "unknown".
    An unannounced foe whose species has two slots is unknown when either is
    the ability asked about, and read as its first slot otherwise. No flip."""
    if getattr(mon, "suppressed", False):
        ab = None
    elif mon.side == u.side or u.side == "p":
        ab = mon.ability
    elif getattr(mon, "revealed", None):
        ab = mon.revealed
    elif mon.ability in TRAP_ABILITIES:
        ab = mon.ability
    else:
        a1, a2 = _regular_abilities(mon)
        ab = (None if name in (a1, a2) else a1) if a1 and a2 else (a1 or a2)
    if ab is None:
        return "unknown"
    return "have" if ab == name else "not"


def mold(u, mon):
    """AICmd_IfMoldBreakerIgnores and Battler_IgnorableAbility: u's Mold
    Breaker gets past mon's ability unless mon holds an Ability Shield."""
    return u.ability == "Mold Breaker" and mon.item != "Ability Shield"


def script_type(b, u, mv):
    """LoadTypeFrom LOAD_MOVE_TYPE (AI_ScriptMoveType, 974 to 981): Weather
    Ball's type from the weather, every other move its listed type."""
    return move_type(b, u, mv) if mv.const == "MOVE_WEATHER_BALL" else mv.type


# ---- the damage figure

def has_comparison(mv):
    """AICmd_FlagMoveDamageScore's gate (1058 to 1113): an alternative-power
    effect, a computed-power hit, or listed power above 1 outside the
    no-calc table."""
    return (mv.effect in ALT_POWER or mv.const in COMPUTED_POWER_HITS
            or (mv.power > 1 and mv.effect not in NO_CALC))


def expected_hits(u, mv, d):
    """TrainerAI_ExpectedHitsDamage (the move reworks, Ian's answer of
    2026-10-07): one hit's estimate at the listed power to the whole move's.
    A two to five hit move counts 3.1 hits, or 5 under Skill Link (a Loaded
    Dice is not seen, as the AI sees no held item there); Fury Cutter its
    power plus 10 and 20 more over its power. Triple Kick (10, 20, 30) and
    Triple Axel (20, 40, 60) the game rates by their three hits' sum over
    the listed power, which is what the calculator's row already adds up
    (gen4.js), so their row stands as it is."""
    p = mv.power
    if p <= 0:
        return d
    if mv.effect == "MULTI_HIT":
        return d * 5 if u.ability == "Skill Link" else d * 31 // 10
    if mv.effect == fs.RISING_HITS:
        return d * (p * 3 + 10 + 20) // p
    return d


def figure(b, u, t, mv):
    """TrainerAI_CalcDamage at the top roll (3249 to 3528): no critical
    hit, no Life Orb, a move of several hits on its expected hits
    (expected_hits); 0 for an immunity the type chart flags; None without a
    comparison. Fixed damage is set directly."""
    if not has_comparison(mv):
        return None
    if script_eff(b, u, t, mv) == 0:
        return 0
    fixed = {"LEVEL_DAMAGE_FLAT": u.level, "40_DAMAGE_FLAT": 40, "20_DAMAGE_FLAT": 20}
    if mv.effect in fixed:
        return fixed[mv.effect]
    if mv.effect == "RANDOM_DAMAGE_1_TO_150_LEVEL":
        r = b.rng.random() if getattr(b, "rng", None) is not None else 0.5
        return u.level * (5 + int(r * 11)) // 10    # drawn again each time
    d = b.damage(u, t, mv, ai_view=True)
    if d == 0 and t.side == "p":
        d = _unabsorbed(b, u, t, mv)
    if d is None:
        return None          # no row: no comparison, rather than an immunity
    d //= fs.row_hits(u, mv)        # one hit, as the engine's estimate starts
    if u.item == "Life Orb":
        d = d * 4096 // 5324                       # the calculator's 1.3, taken back off
    if PINCH.get(u.ability) == mv.type and u.hp <= u.maxhp // 3:
        d = d * 3 // 2                             # the row is made at full HP
    return expected_hits(u, mv, d)


def _unabsorbed(b, u, t, mv):
    """The estimate leaves out the abilities that take a move whole (Flash
    Fire, Volt Absorb, Water Absorb, Motor Drive, Dry Skin, Lightning Rod,
    Storm Drain, Sap Sipper, Soundproof, Bulletproof), which the calculator's
    row reads as 0. Cost the move on the Pokemon's ability-blank twin, once
    prepare() makes one (st["ai_twin"]), else on the same Pokemon with its
    other regular ability; with neither, 0 stands."""
    base = t.key.split("~")[0]
    twins = [b.st.get("ai_twin", {}).get(t.key)] + list(b.st.get("variants", {}).get(base, ()))
    for k in twins:
        if k and k != t.key:
            alt = copy.copy(t)
            alt.key = k
            d = b.damage(u, alt, mv, ai_view=True)
            if d:
                return d
    return 0


# Who moves first, as the AI reads it: BattleSystem_CompareBattlerSpeed,
# which every IfSpeedCompareEqualTo calls with ignoreQuickClaw TRUE. That
# flag only stops the call recording the item's effect: a Quick Claw that
# fires this turn (speedRand, rolled before the AI chooses and read again by
# the turn order) and a Custap Berry in its pinch still put their holder
# first, then Lagging Tail and Full Incense, and Stall, put theirs last; then
# Trick Room, then Speed. Both moves count as priority 0. A speed tie reads
# as FASTER or TIE on a coin flip, never SLOWER.
LAGGING = ("Lagging Tail", "Full Incense")


def _first_item(b, mon, foe):
    """mon's Quick Claw fired this turn (b.quick, set by the turn before the
    AI picks), or its Custap Berry is in its pinch (a quarter HP, half with
    Gluttony; Unnerve on the foe holds it)."""
    if mon.item == "Quick Claw":
        return bool((getattr(b, "quick", None) or {}).get(mon.key))
    if mon.item == "Custap Berry" and foe.ability != "Unnerve":
        return mon.hp <= mon.maxhp // (2 if mon.ability == "Gluttony" else 4)
    return False


def speed_order(b, u, t, coin=True):
    """"slower", "faster" or "tie" for u against t. Without the coin a tie
    reads "tie", for the SLOWER tests, which a tie never meets."""
    su, st_ = b.speed(u), b.speed(t)

    def even(swap=False):
        lo, hi = (st_, su) if swap else (su, st_)
        if lo < hi:
            return "slower"
        if lo == hi:
            return "faster" if coin and chance(b, 50) else "tie"
        return "faster"
    qu, qt = _first_item(b, u, t), _first_item(b, t, u)
    if qu or qt:
        return even() if qu and qt else ("faster" if qu else "slower")
    lu, lt = u.item in LAGGING, t.item in LAGGING
    if lu or lt:
        return even(True) if lu and lt else ("slower" if lu else "faster")
    xu, xt = u.ability == "Stall", t.ability == "Stall"
    if xu or xt:
        return even(True) if xu and xt else ("slower" if xu else "faster")
    return even(bool(b.trick_room))


def slower(b, u, t):
    """IfSpeedCompareEqualTo COMPARE_SPEED_SLOWER."""
    return speed_order(b, u, t, coin=False) == "slower"


def faster(b, u, t):
    """IfSpeedCompareEqualTo COMPARE_SPEED_FASTER: a tie half the time."""
    return speed_order(b, u, t) == "faster"


def chance(b, p):
    return b.rng.random() * 100 < p


def eff(b, mv, t):
    return fs.effectiveness(b.st["chart"], mv.type, t.types)


@functools.lru_cache(maxsize=None)
def _gift_type(item):
    """A berry's Natural Gift type, from its item data."""
    path = os.path.join(data.ROOT, "res", "items", "data", item.lower().replace(" ", "_") + ".json")
    try:
        with open(path, encoding="utf-8") as f:
            ty = json.load(f).get("naturalGiftType")
    except OSError:
        return None
    return ty[len("TYPE_"):].title() if ty else None


def move_type(b, mon, mv):
    """The type a move really has in battle (TrainerAI_MoveType,
    Move_CalcVariableType): Weather Ball by the weather, Natural Gift by the
    berry held; the switching checks read these."""
    if mv.name == "Weather Ball" and b.weather:
        return {"Sun": "Fire", "Rain": "Water", "Hail": "Ice", "Sand": "Rock"}.get(b.weather, mv.type)
    if mv.name == "Natural Gift":
        if mon.item and "Berry" in mon.item:
            return _gift_type(mon.item) or mv.type
    if mv.effect == "RANDOM_POWER_BASED_ON_IVS":
        return hidden_power_type(getattr(mon, "ivs", None)) or mv.type
    return mv.type


HIDDEN_POWER_TYPES = ("Fighting", "Flying", "Poison", "Ground", "Rock", "Bug", "Ghost", "Steel", "Fire",
                      "Water", "Grass", "Electric", "Psychic", "Ice", "Dragon", "Dark")


def hidden_power_type(ivs):
    """Hidden Power's type from the IVs' low bits (Move_CalcVariableType): a
    trainer's IVs are all one value, so all even gives Fighting and all odd
    Dark."""
    if not ivs:
        return None
    bits = sum((ivs.get(k, 0) & 1) << n for n, k in enumerate(("hp", "at", "df", "sp", "sa", "sd")))
    return HIDDEN_POWER_TYPES[bits * 15 // 63]


def eff_of(b, mon, mv, t):
    return fs.effectiveness(b.st["chart"], move_type(b, mon, mv), t.types)


def invalid(b, u, mv):
    """BattleSystem_CheckInvalidMoves(CHECK_INVALID_ALL) for one of u's moves
    (battle_lib.c 2394 to 2485)."""
    if u.pp.get(mv.name, 1) <= 0:
        return True
    if mv.name == getattr(u, "disabled", None):
        return True
    if getattr(u, "tormented", False) and u.last is not None and u.last.name == mv.name:
        return True
    if u.taunt and mv.power == 0:
        return True
    if mv.name in getattr(u, "sealed", ()):                   # the foe's Imprison
        return True
    if getattr(b, "gravity", 0) and mv.const in GRAVITY_FAILS:
        return True
    if getattr(u, "heal_block", 0) and mv.const in HEAL_BLOCKED:
        return True
    if mv.const == "MOVE_BELCH" and not getattr(u, "ate_berry", False):
        return True
    if getattr(u, "throat_chop", 0) and mv.const in SOUND_MOVES:
        return True
    if u.item == "Assault Vest" and mv.cat == "Status" and mv.const != "MOVE_ME_FIRST":
        return True
    enc = getattr(u, "encore", None)
    if enc is not None and mv.name != enc:
        return True
    if u.choice and (u.item or "").startswith("Choice") and mv.name != u.choice \
            and any(m.name == u.choice for m in u.moves):
        return True
    return False


def score_moves(b, u, t, flags):
    """[score] for u's four slots (TrainerAI_Init, TrainerAI_EvalMoves): 100,
    or 0 for a move CheckInvalidMoves rules out, which the routines still
    score; a slot with no PP is 0 under every flag. Each flag's total is
    floored at 0, and past 127 the signed byte wraps and is floored to 0."""
    figs = [figure(b, u, t, m) for m in u.moves]
    best = max((f for f in figs if f is not None), default=None)
    return [score_slot(b, u, t, i, figs, best, flags) for i in range(len(u.moves))]


def score_slot(b, u, t, i, figs, best, flags):
    """One slot's score in score_moves, given every slot's damage figure and
    the best of them. A slot's rolls are its own, so the planner (plplan)
    can enumerate them slot by slot."""
    mv = u.moves[i]
    if u.pp.get(mv.name, 1) <= 0:
        return 0
    s = 0 if invalid(b, u, mv) else 100
    for bit in range(11):
        if flags >> bit & 1:
            s += flag_score(bit, b, u, t, mv, figs[i], best)
            s = 0 if s < 0 or s > 127 else s
    return s


def flag_score(bit, b, u, t, mv, f, best):
    if bit == BASIC:
        return basic(b, u, t, mv, f)
    if bit == EVAL:
        return evaluate_attack(b, u, t, mv, f, best)
    if bit == EXPERT:
        return expert(b, u, t, mv, f)
    if bit == SETUP_FIRST:
        # SetupFirstTurn_Main: the battle's first turn (LoadTurnCount is
        # totalTurns), a move in its table, +2 at 68.75%.
        return 2 if b.turn == 0 and mv.effect in script_table("SetupFirstTurn_SetupEffects") \
            and chance(b, 68.75) else 0
    if bit == RISKY:
        return 2 if mv.effect in script_table("Risky_RiskyEffects") and chance(b, 50) else 0
    if bit == EXTREMES:
        return 2 if f is None and chance(b, 60.9) else 0
    if bit == CHECK_HP:
        return check_hp(b, u, t, mv)
    if bit == WEATHER:
        w = fs.WEATHER_OF.get(mv.effect)
        return 5 if b.turn == 0 and w and b.weather != w else 0
    if bit == BATON:
        return baton_pass(b, u, t, mv, f)
    if bit == TAG:
        return tag_strategy(b, u, t, mv, fs.ally_of(b, u))
    if bit == HARASS:
        return 2 if mv.effect in script_table("Harrassment_Effects") and chance(b, 50) else 0
    return 0


# ---- Basic

def basic(b, u, t, mv, f=None):
    """Basic_Main (script.s 52 to 467) and every handler it reaches."""
    r = _basic_entry(b, u, t, mv)
    if r is not None:
        return r
    return _basic_effect(b, u, t, mv)


def _basic_entry(b, u, t, mv):
    """Basic_Main to Basic_CheckQueenlyMajesty_Priority (52 to 234): the
    score to end on, or None to go on to Basic_ScoreMoveEffect."""
    e40 = script_eff(b, u, t, mv)
    if mv.const in ("MOVE_FISSURE", "MOVE_HORN_DRILL") or has_comparison(mv) or mv.power > 0:
        # Basic_CheckForImmunity and the absorbing abilities (73 to 128).
        if e40 == 0:
            return -10
        if not mold(u, t):
            ab = ability_of(b, u, t)
            if ABSORBS_TYPE.get(ab) == script_type(b, u, mv) or (ab == "Wonder Guard" and e40 not in (80, 160)):
                return -12
    # Basic_CheckSoundproof (134 to 170): with Mold Breaker and a Soundproof
    # guess the script jumps to Basic_ScoreMoveEffect, past the next four.
    if ability_of(b, u, t) == "Soundproof":
        if mold(u, t):
            return None
        if mv.const in BASIC_SOUND:
            return -10
    # Basic_CheckBulletproof (172 to 203).
    if ability_of(b, u, t) == "Bulletproof" and not mold(u, t) and mv.const in BALL_AND_BOMB:
        return -10
    # Basic_CheckPrankster (205 to 208), IfPranksterBlockedByDark.
    if (u.ability == "Prankster" and mv.cat == "Status" and mv.range not in NOT_AT_FOE
            and mv.range != "OPPONENT_SIDE" and "Dark" in t.types):
        return -10
    # Basic_CheckMagicBounce (210 to 217).
    if (check_ability(b, u, t, "Magic Bounce") == "have" and not mold(u, t)
            and getattr(mv, "reflectable", False) and mv.range not in NOT_AT_FOE):
        return -10
    # Basic_CheckQueenlyMajesty (219 to 234): a move of raised priority at the foe.
    pri = mv.pri + (1 if u.ability == "Prankster" and mv.cat == "Status" else 0)
    if pri > 0 and mv.range not in NOT_AT_FOE and not mold(u, t) \
            and ability_of(b, u, t) == "Queenly Majesty":
        return -10
    return None


def _clear_body(b, u, t):
    """Basic_CheckClearBodyEffect and Basic_CheckFlowerVeil (722 to 752), the
    tail of every lowering handler."""
    ab = ability_of(b, u, t)
    if ab in ("Clear Body", "White Smoke") or (ab == "Mirror Armor" and not mold(u, t)):
        return -10
    if "Grass" in t.types and not mold(u, t) and ability_of(b, u, t) == "Flower Veil":
        return -10
    return 0


def _basic_effect(b, u, t, mv):
    """Basic_ScoreMoveEffect and the effect dispatch (236 to 467) with the
    handler each effect reaches; an effect not listed scores 0."""
    e, c = mv.effect, mv.const
    foe = b.p if t.side == "p" else b.b
    own = b.p if u.side == "p" else b.b
    hu = u.frac()
    guard = bool(foe.safeguard) and u.ability != "Infiltrator"       # Basic_Safeguard*, 908 to 931

    # Basic_CheckPowderImmunity (519 to 529), falling into Basic_CheckSapSipper (531 to 539).
    if c in BASIC_POWDERS or c in GRASS_STATUS:
        if c in BASIC_POWDERS and "Grass" in t.types:
            return -10
        if not mold(u, t):
            if c in BASIC_POWDERS and ability_of(b, u, t) == "Overcoat":
                return -10
            if script_type(b, u, mv) == "Grass" and ability_of(b, u, t) == "Sap Sipper":
                return -10

    if e in ("STATUS_SLEEP", "STATUS_SLEEP_NEXT_TURN"):            # Basic_CheckCannotSleep
        if t.status or guard or ability_of(b, u, t) in ("Insomnia", "Vital Spirit"):
            return -10
        return -10 if not mold(u, t) and ability_of(b, u, t) in ("Purifying Salt", "Sweet Veil") else 0
    if e == "HALVE_DEFENSE":                                        # Basic_CheckCannotExplode
        if script_eff(b, u, t, mv) == 0:
            return -10
        if not mold(u, t) and ability_of(b, u, t) == "Damp":
            return -10
        if not own.bench():                                         # Basic_CheckLastMon
            return -10 if foe.bench() else -1
        return 0
    if e == "MIND_BLOWN":
        return -10 if not mold(u, t) and ability_of(b, u, t) == "Damp" else 0
    if e == "RECOVER_DAMAGE_SLEEP":                                 # Basic_CheckDreamEater
        if t.status != "slp":
            return -8
        return -10 if script_eff(b, u, t, mv) == 0 else 0
    if e == "MAX_ATK_LOSE_HALF_MAX_HP":                             # Basic_CheckBellyDrum
        return -10 if hu < 51 or u.stages["atk"] >= 6 else 0
    if e in RAISES:
        first, rest, room = RAISES[e]
        if room and b.trick_room:
            return -10
        if (e == "ATK_SP_ATK_SPEED_UP_2_LOSE_HALF_MAX_HP" and hu < 51) or \
                (e == "RAISE_ALL_STATS_LOSE_THIRD_MAX_HP" and hu < 34):
            return -10
        if u.stages[first] >= 6:
            return -10
        return -8 if any(u.stages[k] >= 6 for k in rest) else 0
    if e in ("ACC_UP", "ACC_UP_2", "EVA_UP", "EVA_UP_2", "EVA_UP_2_MINIMIZE"):
        k = "acc" if e.startswith("ACC") else "eva"
        blocks = ("No Guard",) if k == "acc" else ("No Guard", "Keen Eye", "Illuminate")
        if ability_of(b, u, t) in blocks or u.ability == "No Guard":
            return -10
        return -10 if u.stages[k] >= 6 else 0
    if e == "TAKE_HEART":                                           # Basic_CheckTakeHeart
        if u.status:
            return 0
        return -10 if u.stages["spa"] >= 6 else (-8 if u.stages["spd"] >= 6 else 0)
    if e in LOWERS:                                                 # Basic_CheckLowStatStage_*
        k = LOWERS[e]
        if k == "spe" and b.trick_room:
            return -10
        if t.stages[k] <= -6:
            return -10
        if k == "atk" and ability_of(b, u, t) == "Hyper Cutter":
            return -10
        if k == "def" and ability_of(b, u, t) == "Big Pecks":
            return -10
        if k == "spe" and check_ability(b, u, t, "Speed Boost") == "have":
            return -10
        if k == "acc" and (u.ability == "No Guard"
                           or ability_of(b, u, t) in ("Keen Eye", "Illuminate", "No Guard")):
            return -10
        if k == "eva" and (u.ability in ("No Guard", "Keen Eye", "Illuminate")
                           or ability_of(b, u, t) == "No Guard"):
            return -10
        return _clear_body(b, u, t)
    if e in ("RESET_STAT_CHANGES", "COPY_STAT_CHANGES", "SWAP_STAT_CHANGES"):
        worse = any(v < 0 for v in u.stages.values()) or any(v > 0 for v in t.stages.values())
        return 0 if worse else -10                                  # Basic_CheckStatStageImbalance
    if e == "FORCE_SWITCH":                                         # Basic_CheckCanForceSwitch
        if not foe.bench():
            return -10
        return -10 if not mold(u, t) and ability_of(b, u, t) == "Suction Cups" else 0
    if e in ("RESTORE_HALF_HP", "HEAL_HALF_MORE_IN_SUN", "HEAL_HALF_REMOVE_FLYING_TYPE",
             "LIFE_DEW", "UNUSED_133", "UNUSED_134", "UNUSED_157"):  # Basic_CheckCanRecoverHP
        return -8 if hu == 100 else 0
    if e == "LUNAR_BLESSING":
        return 0 if u.status else (-8 if hu == 100 else 0)
    if e in ("STATUS_POISON", "STATUS_BADLY_POISON"):              # Basic_CheckCannotPoison
        if {"Steel", "Poison"} & set(t.types):
            return -10
        ab = ability_of(b, u, t)
        if ab in ("Immunity", "Magic Guard", "Poison Heal") or (ab == "Leaf Guard" and b.weather == "Sun"):
            return -10
        if ability_of(b, u, t) == "Hydration" and b.weather == "Rain":
            return -10
        if t.status or guard:
            return -10
        return -10 if not mold(u, t) and ability_of(b, u, t) in ("Purifying Salt", "Pastel Veil") else 0
    if e == "SET_LIGHT_SCREEN":
        return -8 if own.screens["Light Screen"] else 0
    if e == "SET_REFLECT":
        return -8 if own.screens["Reflect"] else 0
    if e == "PREVENT_STAT_REDUCTION":                               # Mist
        return -8 if getattr(own, "mist", 0) else 0
    if e == "PREVENT_STATUS":                                       # Safeguard
        return -8 if own.safeguard else 0
    if e == "ONE_HIT_KO":                                           # Basic_CheckOHKOWouldFail
        if script_eff(b, u, t, mv) == 0:
            return -10
        if not mold(u, t) and ability_of(b, u, t) == "Sturdy":
            return -10
        return -10 if u.level < t.level else 0
    if e in NONSTANDARD or e == "PSYWAVE":
        # Basic_CheckMagnitude (Magnitude's effect is PSYWAVE): its Mold
        # Breaker test reads a stale value and never fires (vanilla B5).
        if e == "PSYWAVE" and ability_of(b, u, t) == "Levitate":
            return -10
        e40 = script_eff(b, u, t, mv)                                # Basic_CheckNonStandardDamageOrChargeTurn
        if e40 == 0:
            return -10
        if ability_of(b, u, t) == "Wonder Guard" and not mold(u, t) and e40 not in (80, 160):
            return -10
        return 0
    if e == "CRIT_UP_2":                                            # Basic_CheckAlreadyPumpedUp
        return -10 if u.crit_stage else 0
    if e in ("STATUS_CONFUSE", "ATK_UP_2_STATUS_CONFUSION", "SP_ATK_UP_CAUSE_CONFUSION"):
        if t.confused:                                              # Basic_CheckCannotConfuse
            return -5
        return -10 if ability_of(b, u, t) == "Own Tempo" or guard else 0
    if e == "STATUS_PARALYZE":                                      # Basic_CheckCannotParalyze
        if script_eff(b, u, t, mv) == 0 or "Electric" in t.types or ability_of(b, u, t) == "Limber":
            return -10
        if not mold(u, t):
            if ability_of(b, u, t) == "Purifying Salt":
                return -10
            if c == "MOVE_THUNDER_WAVE" and \
                    ability_of(b, u, t) in ("Motor Drive", "Volt Absorb", "Lightning Rod"):
                return -10
        return -10 if t.status or guard else 0
    if e == "SET_SUBSTITUTE":                                       # Basic_CheckCannotSubstitute
        return -8 if u.sub else (-10 if hu < 26 else 0)
    if e == "STATUS_LEECH_SEED":                                    # Basic_CheckCannotLeechSeed
        if t.seeded or "Grass" in t.types:
            return -10
        return -10 if ability_of(b, u, t) == "Magic Guard" else 0
    if e == "DISABLE":
        return -8 if getattr(t, "disabled", None) else 0
    if e == "ENCORE":
        return -8 if getattr(t, "encore", None) else 0
    if e in ("DAMAGE_WHILE_ASLEEP", "USE_RANDOM_LEARNED_MOVE_SLEEP"):  # Basic_CheckAttackerAsleep
        return -8 if u.status != "slp" else 0
    if e == "NEXT_ATTACK_ALWAYS_HITS":                              # Basic_CheckLockOn
        if getattr(t, "locked_on", 0) or u.ability == "No Guard":
            return -10
        return -10 if ability_of(b, u, t) == "No Guard" else 0
    if e == "PREVENT_ESCAPE":                                       # Basic_CheckMeanLook
        return -10 if t.trapped_by is not None or "Ghost" in t.types else 0
    if e == "STATUS_NIGHTMARE":                                     # Basic_CheckNightmare
        if getattr(t, "nightmare", False):
            return -10
        if t.status != "slp":
            return -8
        return -10 if ability_of(b, u, t) == "Magic Guard" else 0
    if e == "CURSE":                                                # Basic_CheckCurse
        if "Ghost" in u.types:
            return -10 if t.cursed or ability_of(b, u, t) == "Magic Guard" else 0
        return -10 if u.stages["atk"] >= 6 else (-8 if u.stages["def"] >= 6 else 0)
    if e == "SET_SPIKES":                                           # Basic_CheckSpikes
        return -10 if foe.hazards["spikes"] >= 3 or not foe.bench() else 0
    if e == "FORESIGHT":
        return -10 if getattr(t, "foresight", False) else 0
    if e == "ALL_FAINT_3_TURNS":                                    # Basic_CheckPerishSong
        return -10 if t.perish else 0
    if e == "WEATHER_SANDSTORM":
        return -8 if b.weather == "Sand" else 0
    if e == "INFATUATE":                                            # Basic_CheckCannotAttract
        if getattr(t, "infatuated", False) or ability_of(b, u, t) == "Oblivious":
            return -10
        ug, tg = getattr(u, "gender", None), getattr(t, "gender", None)
        if ug is None or tg is None:
            return 0                                                # genders not kept yet
        return 0 if {ug, tg} == {"M", "F"} else -10
    if e == "FAINT_AND_ATK_SP_ATK_DOWN_2":                          # Basic_CheckMemento
        if not mold(u, t) and ability_of(b, u, t) in ("Clear Body", "White Smoke"):
            return -10
        if t.stages["atk"] <= -6:
            return -10
        if t.stages["spa"] <= -6:
            return -8
        return -10 if not own.bench() else 0
    if e == "PASS_STATS_AND_STATUS":                                # Basic_CheckBatonPass
        return -10 if not own.bench() else 0
    if e == "WEATHER_RAIN":                                         # Basic_CheckRainDance
        if u.ability not in ("Swift Swim", "Hydration") and ability_of(b, u, t) == "Hydration" and t.status:
            return -8
        return -8 if b.weather == "Rain" else 0
    if e == "WEATHER_SUN":                                          # Basic_CheckSunnyDay
        if u.ability not in ("Flower Gift", "Leaf Guard", "Solar Power") and \
                ability_of(b, u, t) == "Leaf Guard" and not t.status:
            return -10
        return -8 if b.weather == "Sun" else 0
    if e == "HIT_IN_3_TURNS":                                       # Basic_CheckFutureSight
        return -12 if getattr(foe, "future_sight", 0) or getattr(own, "future_sight", 0) else 0
    if e == "FLEE_FROM_WILD_BATTLE":                                # Teleport
        return -10
    if e in ("ALWAYS_FLINCH_FIRST_TURN_ONLY", "FIRST_TURN_ONLY"):   # Basic_CheckFirstTurnInBattle
        return 0 if u.turns_in <= 0 else -10
    if e == "STOCKPILE":                                            # Basic_CheckMaxStockpile
        return -10 if getattr(u, "stockpile", 0) == 3 else 0
    if e in ("SPIT_UP", "SWALLOW"):                                 # Basic_CheckCanSpitUpOrSwallow
        if script_eff(b, u, t, mv) == 0 or getattr(u, "stockpile", 0) == 0:
            return -10
        return -8 if e == "SWALLOW" and hu == 100 else 0
    if e == "WEATHER_HAIL":                                         # Basic_CheckHail
        if b.weather == "Hail":
            return -8
        if ability_of(b, u, t) != "Ice Body":
            return 0
        return 0 if u.ability == "Ice Body" else -8
    if e == "TORMENT":
        return -10 if getattr(t, "tormented", False) else 0
    if e == "STATUS_BURN":                                          # Basic_CheckCannotBurn
        if ability_of(b, u, t) in ("Water Veil", "Magic Guard") or t.status or "Fire" in t.types or guard:
            return -10
        return -10 if not mold(u, t) and ability_of(b, u, t) in ("Purifying Salt", "Water Bubble") else 0
    if e == "BOOST_ALLY_POWER_BY_50_PERCENT":                       # Basic_CheckHelpingHand
        return 0 if getattr(b, "doubles", False) else -10
    if e in ("SWITCH_HELD_ITEMS", "REMOVE_HELD_ITEM"):              # Basic_CheckCanRemoveItem
        return -10 if ability_of(b, u, t) == "Sticky Hold" or not t.item else 0
    if e == "GROUND_TRAP_USER_CONTINUOUS_HEAL":                     # Basic_CheckAlreadyIngrained
        return -10 if u.ingrained else 0
    if e == "RECYCLE":
        return -10 if not getattr(u, "recycle_item", None) else 0
    if e == "MAKE_SHARED_MOVES_UNUSEABLE":                          # Basic_CheckCanImprison
        return -10 if getattr(u, "imprisoning", False) or getattr(t, "sealed", ()) else 0
    if e == "HEAL_STATUS":                                          # Basic_CheckCanRefreshStatus
        return 0 if u.status in ("brn", "psn", "tox", "par") else -10
    if e == "HALVE_ELECTRIC_DAMAGE":                                # Mud Sport
        return -10 if getattr(u, "mud_sport", False) else 0
    if e == "HALVE_FIRE_DAMAGE":                                    # Water Sport
        return -10 if getattr(u, "water_sport", False) else 0
    if e == "ATK_DEF_DOWN":                                         # Basic_CheckTickle
        if not mold(u, t) and ability_of(b, u, t) in ("Clear Body", "White Smoke"):
            return -10
        return -10 if t.stages["atk"] <= -6 else (-8 if t.stages["def"] <= -6 else 0)
    if e == "CAMOUFLAGE":
        return -10 if getattr(u, "camouflaged", False) else 0
    if e == "GRAVITY":
        return -10 if getattr(b, "gravity", 0) else 0
    if e == "IGNORE_EVATION_REMOVE_DARK_IMMUNE":                    # Miracle Eye
        return -10 if getattr(t, "miracle_eye", False) else 0
    if e in ("FAINT_AND_FULL_HEAL_NEXT_MON", "FAINT_FULL_RESTORE_NEXT_MON"):
        # Basic_CheckHealingWish and Basic_CheckLunarDance: -20, a further -10
        # on the last Pokemon or with nothing to mend (a fainted or on-field
        # party member counts as wounded, vanilla B7).
        if not own.bench():
            return -30
        others = [m for m in own.mons if m is not u]
        useful = any(m.status for m in own.bench()) or any(m.hp < m.maxhp for m in others)
        if e == "FAINT_FULL_RESTORE_NEXT_MON":
            useful = useful or any(m.pp.get(x.name, x.pp) < x.pp for m in others for x in m.moves)
        return -20 if useful else -30
    if e == "NATURAL_GIFT":                                         # Basic_CheckNaturalGift
        if not (u.item and _gift_type(u.item)):
            return -10
        return -10 if script_eff(b, u, t, mv) == 0 else 0
    if e == "DOUBLE_SPEED_3_TURNS":                                 # Basic_CheckTailwind
        return -10 if b.trick_room or own.tailwind else 0
    if e == "RANDOM_STAT_UP_2":                                     # Basic_CheckAcupressure
        return -10 if any(v >= 6 for v in u.stages.values()) else 0
    if e == "METAL_BURST":                                          # Basic_CheckMetalBurst
        if script_eff(b, u, t, mv) == 0 or ability_of(b, u, t) == "Stall" \
                or getattr(t, "known_item", None) == "Shiny Stone":
            return -10
        if u.ability == "Stall" or u.item == "Shiny Stone":
            return 0
        return -10 if speed_order(b, u, t) == "faster" else 0
    if e == "PREVENT_ITEM_USE":                                     # Basic_CheckEmbargo
        return -10 if getattr(t, "embargo", 0) else 0
    if e == "FLING":
        return _basic_fling(b, u, t, mv)
    if e == "TRANSFER_STATUS":
        return _basic_psycho_shift(b, u, t)
    if e == "PREVENT_HEALING":                                      # Basic_CheckHealBlock
        return -10 if getattr(t, "heal_block", 0) else 0
    if e == "SWAP_ATK_DEF":                                         # Basic_CheckPowerTrick
        return -10 if getattr(u, "power_trick", False) else 0
    if e == "SUPRESS_ABILITY":                                      # Basic_CheckGastroAcid
        if getattr(t, "suppressed", False):
            return -10
        return -10 if ability_of(b, u, t) in ("Multitype", "Truant", "Slow Start", "Stench",
                                              "Run Away", "Pickup", "Honey Gather") else 0
    if e == "PREVENT_CRITS":                                        # Basic_CheckLuckyChant
        return -10 if getattr(own, "lucky_chant", 0) else 0
    if e == "USE_LAST_USED_MOVE":                                   # Basic_CheckCopycat
        return -10 if b.turn == 0 and speed_order(b, u, t) == "faster" else 0
    if e == "SWAP_ATK_SP_ATK_STAT_CHANGES":                         # Basic_CheckPowerSwap
        return -10 if t.stages["atk"] - u.stages["atk"] < 1 and t.stages["spa"] - u.stages["spa"] < 1 else 0
    if e == "SWAP_DEF_SP_DEF_STAT_CHANGES":                         # Basic_CheckGuardSwap
        return -10 if t.stages["def"] - u.stages["def"] < 1 and t.stages["spd"] - u.stages["spd"] < 1 else 0
    if e == "FAIL_IF_NOT_USED_ALL_OTHER_MOVES":                     # Basic_CheckLastResort
        others = [m.name for m in u.moves if m.name != mv.name]
        used = getattr(u, "used_moves", set())
        return 0 if others and all(n in used for n in others) else -10
    if e == "SET_ABILITY_TO_INSOMNIA":                              # Basic_CheckWorrySeed
        if ability_of(b, u, t) in ("Truant", "Insomnia", "Vital Spirit", "Multitype"):
            return -10
        seen = {m.name for m in shown(t)}
        return -10 if t.status == "slp" and not seen & {"Sleep Talk", "Snore"} else 0
    if e == "TOXIC_SPIKES":                                         # Basic_CheckToxicSpikes
        return -10 if foe.hazards["tspikes"] >= 2 or not foe.bench() else 0
    if e == "RESTORE_HP_EVERY_TURN":                                # Basic_CheckAquaRing
        return -10 if getattr(u, "aqua_ring", False) else 0
    if e == "GIVE_GROUND_IMMUNITY":                                 # Basic_CheckMagnetRise
        return -10 if getattr(u, "magnet_rise", 0) or u.ability == "Levitate" or "Flying" in u.types else 0
    if e == "REMOVE_HAZARDS_SCREENS_EVA_DOWN":
        return _basic_defog(b, u, t, own, foe)
    if e == "TRICK_ROOM":                                           # Basic_CheckTrickRoom
        if getattr(b, "trick_room_perm", b.trick_room >= 999):
            return -10
        return -10 if speed_order(b, u, t) != "slower" else 0
    if e == "WONDER_ROOM":                                          # Basic_CheckWonderRoom
        return -10 if getattr(b, "wonder_room_perm", False) else 0
    if e == "SP_ATK_DOWN_2_OPPOSITE_GENDER":                        # Basic_CheckCaptivate
        if not mold(u, t) and ability_of(b, u, t) in ("Oblivious", "Clear Body", "White Smoke"):
            return -10
        ug, tg = getattr(u, "gender", None), getattr(t, "gender", None)
        if ug is not None and tg is not None and {ug, tg} != {"M", "F"}:
            return -10
        return -10 if t.stages["spa"] <= -6 else 0
    if e == "STEALTH_ROCK":                                         # Basic_CheckStealthRock
        return -10 if foe.hazards["rocks"] or not foe.bench() else 0
    if e == "POLTERGEIST":
        return -10 if not t.item else 0
    if e == "STICKY_WEB":
        return -10 if getattr(foe, "sticky_web", False) or not foe.bench() else 0
    if e == "SET_AURORA_VEIL":
        if getattr(own, "aurora_veil", 0):
            return -8
        return -10 if b.weather != "Hail" else 0
    if e == "UPPER_HAND":                                           # Basic_CheckUpperHand
        # IfBattlerKnowsPriorityMove on the target: the AI reads only the
        # moves it has seen the player's Pokemon use.
        return 0 if any(fs.move_priority(t, m) > 0 for m in shown(t)) else -10
    if e == "STRENGTH_SAP":
        return -10 if t.stages["atk"] <= -6 else 0
    if e == "PARTING_SHOT":
        return -10 if t.stages["atk"] <= -6 and t.stages["spa"] <= -6 else 0
    if (e == "HIT" and mv.power == 0) or e in UNWRITTEN:            # Basic_CheckUnwrittenStatusMove
        return -10
    if e == "REST":                                                 # Basic_CheckRest
        if hu == 100:
            return -8
        if u.ability in ("Insomnia", "Vital Spirit", "Purifying Salt", "Sweet Veil") or \
                (u.ability == "Leaf Guard" and b.weather == "Sun"):
            return -10
        return -10 if u.ability != "Soundproof" and getattr(b, "uproar", 0) else 0
    if e == "TAUNT":                                                # Basic_CheckTaunt
        return -10 if not mold(u, t) and ability_of(b, u, t) == "Oblivious" else 0
    return 0


def _basic_fling(b, u, t, mv):
    """Basic_CheckFling (1602 to 1702)."""
    if script_eff(b, u, t, mv) == 0:
        return -10
    rec = _item(u.item) if u.item else {}
    if (rec.get("flingPower") or 0) < 10 or u.ability == "Multitype":
        return -10
    hold = rec.get("holdEffect")
    foe_guard = (b.p if t.side == "p" else b.b).safeguard
    own_guard = (b.p if u.side == "p" else b.b).safeguard
    if hold in ("HOLD_EFFECT_PSN_USER", "HOLD_EFFECT_STRENGTHEN_POISON"):
        if not (foe_guard or t.status or u.ability == "Poison Heal" or {"Poison", "Steel"} & set(t.types)
                or ability_of(b, u, t) in ("Immunity", "Poison Heal", "Magic Guard")):
            return 0
        if own_guard or u.status or {"Poison", "Steel"} & set(u.types) or \
                u.ability in ("Klutz", "Immunity", "Poison Heal", "Magic Guard", "Guts"):
            return -5
        return 3
    if hold == "HOLD_EFFECT_BRN_USER":
        if not (foe_guard or t.status or "Fire" in t.types
                or ability_of(b, u, t) in ("Magic Guard", "Water Veil")):
            return 0
        if own_guard or u.status or "Fire" in u.types or \
                u.ability in ("Klutz", "Magic Guard", "Water Veil", "Guts"):
            return -5
        return 3
    if hold == "HOLD_EFFECT_PIKA_SPATK_UP":
        return -5 if foe_guard or t.status or ability_of(b, u, t) == "Limber" else 0
    return 0


def _basic_psycho_shift(b, u, t):
    """Basic_CheckCanPsychoShift (1704 to 1754)."""
    if not u.status or t.status or (b.p if t.side == "p" else b.b).safeguard:
        return -10
    if u.status in ("psn", "tox"):
        if u.ability == "Poison Heal" or {"Poison", "Steel"} & set(t.types):
            return -10
        return -10 if ability_of(b, u, t) in ("Immunity", "Poison Heal", "Magic Guard") else 0
    if u.status == "brn":
        if "Fire" in t.types:
            return -10
        return -10 if ability_of(b, u, t) in ("Magic Guard", "Water Veil") else 0
    if u.status == "par":
        return -10 if ability_of(b, u, t) == "Limber" else 0
    return 0


def _basic_defog(b, u, t, own, foe):
    """Basic_CheckDefog (1879 to 1911): refused only at -6 evasion with
    nothing to clear on either side."""
    if t.stages["eva"] > -6 or foe.screens["Light Screen"] or foe.screens["Reflect"] \
            or getattr(foe, "aurora_veil", 0) or any(own.hazards.values()) \
            or getattr(own, "sticky_web", False) or b.weather == "Fog":
        return 0
    if not foe.bench():
        return -10
    return 0 if any(foe.hazards.values()) or getattr(foe, "sticky_web", False) else -10


# ---- Evaluate Attack

def evaluate_attack(b, u, t, mv, f, best):
    """EvalAttack_Main (script.s 7155 to 7217)."""
    if f is not None:
        # IfCurrentMoveKills USE_MAX_DAMAGE after AI_SturdySurvives: Sturdy
        # at full HP leaves its holder on 1 HP unless Mold Breaker ignores it.
        dmg = f
        if t.hp == t.maxhp and dmg >= t.hp and t.ability == "Sturdy" and not mold(u, t):
            dmg = t.hp - 1
        if t.hp <= dmg:                                             # EvalAttack_ApplyKillBonuses
            if mv.effect == "HALVE_DEFENSE":
                return 0
            if mv.effect in ("HIT_LAST_WHIFF_IF_HIT", "HIT_FIRST_IF_TARGET_ATTACKING", "HIT_IN_3_TURNS"):
                return 4 if chance(b, 33.6) else 0                  # IfRandomLessThan 170 skips it
            return 6 if mv.effect == "PRIORITY_1" else 4            # the effect, not the priority
        if best is not None and f < best:                           # AI_NOT_HIGHEST_DAMAGE
            return -1
    s = 0
    # EvalAttack_MaybeDeprioritize: a move with no comparison reaches it too.
    if mv.effect in ("HALVE_DEFENSE", "HIT_LAST_WHIFF_IF_HIT", "HIT_FIRST_IF_TARGET_ATTACKING") \
            and chance(b, 80.1):                                    # IfRandomLessThan 51 skips it
        s -= 2
    # EvalAttack_CheckQuadEffective, status moves included (vanilla O12).
    if script_eff(b, u, t, mv) == 160 and chance(b, 68.75):          # IfRandomLessThan 80 skips it
        s += 2
    return s


# ---- the Expert flag ----------------------------------------------------------------------------
#
# Expert_Main (script.s) is a jump table from a move's battle effect to a
# routine; the table is read from the script itself (expert_routes), so an
# effect Oxide routes later reaches its routine here with no edit, and a
# label with no routine below fails test_fightai. Each routine is the
# script's, by its label, from the Scoring Agent's audit of 2026-09-30
# (docs/oxide/trainer-scoring-handoff.md): every threshold, roll and early
# end as the script has it at HEAD, vanilla bugs Ian kept included.
#
# A chance(b, p) below is always the probability that the score changes:
# `IfRandomLessThan N, skip` before an add is chance(b, (256 - N) / 2.56).

# The values AICmd_IfMoveEffectivenessEquals compares (include/constants/battle.h).
IMMUNE, QUARTER, HALF, DOUBLE, QUADRUPLE = 0, 10, 20, 80, 160


def script_eff(b, u, t, mv):
    """The number AICmd_IfMoveEffectivenessEquals compares for u's move into
    t: BattleSystem_ApplyTypeChart from a base of 40 at the move's battle
    type (STAB, the chart type by type, Filter and Solid Rock, Expert Belt,
    Tinted Lens), with plain STAB's 1.5 divided back out at the four exact
    values, and any immunity flag (the chart, Levitate, Magnet Rise, an Air
    Balloon, Wonder Guard) reading 0. Scrappy and Foresight get Normal and
    Fighting past a Ghost; an Iron Ball, Thousand Arrows or Gravity grounds
    a Flying type; Freeze-Dry hits Water. A neutral STAB hit (60), or one
    Filter or Tinted Lens scaled, matches none of the five, as in the game."""
    ty = "Normal" if u.ability == "Normalize" else move_type(b, u, mv)
    grounded = t.item == "Iron Ball" or mv.const == "MOVE_THOUSAND_ARROWS"
    if ty == "Ground" and not grounded and (
            (t.ability == "Levitate" and not mold(u, t)) or getattr(t, "magnet_rise", 0)
            or t.item == "Air Balloon"):
        return IMMUNE
    d = 40
    if ty in u.types:
        d = d * 2 if u.ability == "Adaptability" else d * 15 // 10
    steps = 0
    for typ in dict.fromkeys(t.types):
        m = fs.effectiveness(b.st["chart"], ty, [typ])
        if mv.const == "MOVE_FREEZE_DRY" and typ == "Water":
            m = 2.0
        if m == 0 and typ == "Ghost" and ty in ("Normal", "Fighting") and (
                u.ability == "Scrappy" or getattr(t, "foresight", False)):
            continue
        if m == 0 and typ == "Flying" and ty == "Ground" and (grounded or getattr(b, "gravity", 0)):
            continue
        if m == 0:
            return IMMUNE
        d = max(1, d * int(m * 10) // 10)
        steps += 1 if m > 1 else -1 if m < 1 else 0
    if mv.power and t.ability == "Wonder Guard" and not mold(u, t) and steps <= 0 \
            and mv.effect not in CHARGE_TURN:
        return IMMUNE
    if mv.power:
        if steps > 0 and t.ability in ("Filter", "Solid Rock", "Prism Armor") and not mold(u, t):
            d = d * 3 // 4
        if steps > 0 and u.item == "Expert Belt":
            d = d * 120 // 100
        if steps < 0 and u.ability == "Tinted Lens":
            d *= 2
    return {120: DOUBLE, 240: QUADRUPLE, 30: HALF, 15: QUARTER}.get(d, d)


# The move 0 the engine records after a turn its Pokemon could not act
# (res/moves/none: power 0, physical, effect HIT); `last` is None then.
def _prev_power(t):
    return 0 if t.last is None else t.last.power


def _prev_class(t):
    """LoadDefenderLastUsedMoveClass: no move reads as physical (move 0)."""
    return "Physical" if t.last is None else t.last.cat


def _prev_effect(t):
    return "HIT" if t.last is None else t.last.effect


def shown(mon):
    """The moves the AI has seen this Pokemon use since it came in
    (AI_CONTEXT.battlerMoves, filled by TrainerAI_RecordLastMove from each
    move that passed its before-move checks; cleared on switch-in)."""
    return getattr(mon, "shown", ())


def _knows(mon, *consts):
    """IfMoveKnown on the user: any of its four moves by move id."""
    return any(m.const in consts for m in mon.moves)


@functools.lru_cache(maxsize=None)
def _item(item):
    """An item's record from res/items/data, or {} for none."""
    if not item:
        return {}
    stem = "".join(c for c in item.lower() if c.isalnum() or c == " ").replace(" ", "_")
    path = os.path.join(data.ROOT, "res", "items", "data", stem + ".json")
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except OSError:
        return {}


def _hold(item):
    """An item's hold effect without its HOLD_EFFECT_ prefix, or None."""
    he = _item(item).get("holdEffect")
    return he[len("HOLD_EFFECT_"):] if he else None


def _side(b, mon):
    return b.p if mon.side == "p" else b.b


def _best_figure(b, u, t):
    """TrainerAI_CalcAllDamage at the top roll: u's strongest figure on t."""
    return max((figure(b, u, t, m) or 0 for m in u.moves), default=0)


def _bench_outdamages(b, side, u, t):
    """IfPartyMemberDealsMoreDamage USE_MAX_DAMAGE: a benched Pokemon's
    attack, costed as if u used it (u's stats, level, types and stages:
    expert-2.md bug 10, which Ian kept), beats u's own best on t. A trainer's
    rows carry its whole party's attacks (fightsim.prepare, party_hits)."""
    mine = _best_figure(b, u, t)
    return any((figure(b, u, t, m) or 0) > mine for mon in side.bench() for m in mon.moves)


def _self_hit_beats(b, u, t):
    """IfBattlerDealsMoreDamage AI_BATTLER_DEFENDER (expert-2.md bug 6): t's
    last move, costed as t hitting itself, beats u's best on t. The
    calculator has no row of a Pokemon on itself, so this reads False."""
    if t.last is None:
        return False
    rolls = b.rolls(t, t, t.last)
    return bool(rolls) and rolls[-1] > _best_figure(b, u, t)


def _infatuated(mon):
    return getattr(mon, "infatuated", False)


class _Ctx:
    """What the Expert routines read, worked out once per move scored."""
    __slots__ = ("b", "u", "t", "mv", "e", "hu", "ht", "slow", "val", "res", "own", "foe")

    def __init__(self, b, u, t, mv):
        self.b, self.u, self.t, self.mv, self.e = b, u, t, mv, mv.effect
        self.hu, self.ht = u.frac(), t.frac()
        self.slow = slower(b, u, t)
        self.val = script_eff(b, u, t, mv) if mv.damaging() else None
        # "If the opponent resists or is immune to the move": the three
        # IfMoveEffectivenessEquals tests for 0, 10 and 20.
        self.res = self.val in (IMMUNE, QUARTER, HALF)
        self.own, self.foe = _side(b, u), _side(b, t)

    def roll(self, p):
        return chance(self.b, p)

    def faster(self):
        return faster(self.b, self.u, self.t)


# -- the routines, in script order -----------------------------------------------------------------

def x_status_sleep(c):
    """Expert_StatusSleep: +1 at 50% when the user knows Dream Eater or
    Nightmare (by effect, PP or not)."""
    if any(m.effect in ("RECOVER_DAMAGE_SLEEP", "STATUS_NIGHTMARE") for m in c.u.moves) and c.roll(50):
        return 1
    return 0


def x_drain_move(c):
    """Expert_DrainMove: -3 at 80.5% into a target that resists or is immune."""
    return -3 if c.res and c.roll(80.5) else 0


def x_explosion(c):
    """Expert_Explosion (Explosion, Self-Destruct, Memento): -1 against
    raised evasion, -1 more at 50% at +4; then by the user's HP and speed."""
    s = 0
    if c.t.stages["eva"] >= 1:
        s -= 1
        if c.t.stages["eva"] >= 4 and c.roll(50):
            s -= 1
    if c.hu >= 80 and not c.slow:
        return s - (3 if c.roll(80.5) else 0)
    if c.hu > 50:
        return s - (1 if c.roll(80.5) else 0)
    if c.roll(50):
        s += 1
    if c.hu <= 30 and c.roll(80.5):
        s += 1
    return s


def x_dream_eater(c):
    """Expert_DreamEater: -1 into a resist; +3 at 80.1% on a sleeping target."""
    if c.res:
        return -1
    return 3 if c.t.status == "slp" and c.roll(80.1) else 0


MIRROR_MOVE_TABLE = {
    "MOVE_SLEEP_POWDER", "MOVE_LOVELY_KISS", "MOVE_SPORE", "MOVE_HYPNOSIS", "MOVE_SING",
    "MOVE_GRASS_WHISTLE", "MOVE_SHADOW_PUNCH", "MOVE_SAND_ATTACK", "MOVE_SMOKE_SCREEN", "MOVE_TOXIC",
    "MOVE_GUILLOTINE", "MOVE_HORN_DRILL", "MOVE_FISSURE", "MOVE_SHEER_COLD", "MOVE_CROSS_CHOP",
    "MOVE_AEROBLAST", "MOVE_CONFUSE_RAY", "MOVE_SWEET_KISS", "MOVE_SCREECH", "MOVE_COTTON_SPORE",
    "MOVE_SCARY_FACE", "MOVE_FAKE_TEARS", "MOVE_METAL_SOUND", "MOVE_THUNDER_WAVE", "MOVE_GLARE",
    "MOVE_POISON_POWDER", "MOVE_SHADOW_BALL", "MOVE_DYNAMIC_PUNCH", "MOVE_HYPER_BEAM",
    "MOVE_EXTREME_SPEED", "MOVE_THIEF", "MOVE_COVET", "MOVE_ATTRACT", "MOVE_SWAGGER", "MOVE_TORMENT",
    "MOVE_FLATTER", "MOVE_TRICK", "MOVE_SUPERPOWER", "MOVE_SKILL_SWAP", "MOVE_PSYCHO_SHIFT",
    "MOVE_POWER_SWAP", "MOVE_GUARD_SWAP", "MOVE_SUCKER_PUNCH", "MOVE_HEART_SWAP", "MOVE_SWITCHEROO",
    "MOVE_CAPTIVATE", "MOVE_DARK_VOID"}


def x_mirror_move(c):
    """Expert_MirrorMove: copying a listed move when moving first, +2 at
    50%; a move not on the list, -1 at 68.75%."""
    listed = c.t.last is not None and c.t.last.const in MIRROR_MOVE_TABLE
    if listed:
        return 2 if not c.slow and c.roll(50) else 0
    return -1 if c.roll(68.75) else 0


def _raise_attack(c, k, low_band):
    """Expert_StatusAttackUp and Expert_StatusSpAttackUp: a stage already at
    +3, -1 at 60.9%; otherwise at full HP +2 at 50%. Above 70% HP nothing
    more; below 40%, -2; between, -2 at low_band."""
    s = 0
    if c.u.stages[k] >= 3:
        if c.roll(60.9):
            s -= 1
    elif c.hu == 100 and c.roll(50):
        s += 2
    if c.hu > 70:
        return s
    if c.hu < 40:
        return s - 2
    return s - (2 if c.roll(low_band) else 0)


def x_status_attack_up(c):
    return _raise_attack(c, "atk", 84.4)


def x_status_sp_attack_up(c):
    return _raise_attack(c, "spa", 72.7)


def _raise_defence(c, k, cls):
    """Expert_StatusDefenseUp and Expert_StatusSpDefenseUp: the raise is
    worth less the more hurt the user is, and when the foe's last move
    was not of the class it guards against (by power, then class)."""
    s = 0
    if c.u.stages[k] >= 3:
        if c.roll(60.9):
            s -= 1
    elif c.hu == 100 and c.roll(50):
        s += 2
    if c.hu >= 70 and c.roll(78.1):
        return s
    if c.hu < 40:
        return s - 2
    if _prev_power(c.t) == 0:
        return s - (2 if c.roll(76.6) else 0)
    if _prev_class(c.t) != cls:
        return s - 2
    return s - (2 if c.roll(58.6) else 0)


def x_status_defense_up(c):
    return _raise_defence(c, "def", "Physical")


def x_status_sp_defense_up(c):
    return _raise_defence(c, "spd", "Special")


def x_status_speed_up(c):
    """Expert_StatusSpeedUp: not slower, -3; slower, +3 at 72.7%."""
    if not c.slow:
        return -3
    return 3 if c.roll(72.7) else 0


def x_status_accuracy_up(c):
    """Expert_StatusAccuracyUp: -2 at 80.5% at +3 accuracy; -2 at 70% HP or less."""
    s = -2 if c.u.stages["acc"] >= 3 and c.roll(80.5) else 0
    return s - (2 if c.hu <= 70 else 0)


def x_status_evasion_up(c):
    """Expert_StatusEvasionUp: Double Team and Minimize, worth more while
    the foe wears down and the user heals."""
    u, t = c.u, c.t
    s = 0
    if c.hu >= 90 and c.roll(60.9):
        s += 3
    if u.stages["eva"] >= 3 and c.roll(50):
        s -= 1
    # Toxic on the foe: one roll above half HP, two at half or less.
    if t.status == "tox" and (c.hu > 50 or c.roll(68.75)) and c.roll(80.5):
        s += 3
    if t.seeded and c.roll(72.7):
        s += 3
    if (u.ingrained or getattr(u, "aqua_ring", False)) and c.roll(50):
        s += 2
    if t.cursed and c.roll(72.7):
        s += 3
    if c.hu > 70 or u.stages["eva"] == 0:
        return s
    if c.hu < 40 or c.ht < 40:
        return s - 2
    return s - (2 if c.roll(72.7) else 0)


def x_bypass_accuracy_move(c):
    """Expert_BypassAccuracyMove: a move that cannot miss is worth more
    against raised evasion or lowered accuracy."""
    t, u = c.t, c.u
    if t.stages["eva"] >= 5 or u.stages["acc"] <= -5:
        return 1 + (1 if c.roll(60.9) else 0)
    if t.stages["eva"] >= 3 or u.stages["acc"] <= -3:
        return 1 if c.roll(60.9) else 0
    return 0


def _lower_attack(c, k, cls):
    """Expert_StatusAttackDown and Expert_StatusSpAttackDown (Growl and its
    kin, Noble Roar, Venom Drench; Confide, Eerie Impulse; Parting Shot
    with nobody to switch to): less for a stage already moved and a foe at
    70% HP or less; then -2 at 50% when the foe's last move was of the
    other class (no move reads as physical)."""
    s = 0
    if c.t.stages[k] != 0:
        s -= 1
        if c.hu <= 90:
            s -= 1
        if c.t.stages[k] <= -3 and c.roll(80.5):
            s -= 2
    if c.ht <= 70:
        s -= 2
    if _prev_class(c.t) == cls and c.roll(50):
        s -= 2
    return s


def x_status_attack_down(c):
    return _lower_attack(c, "atk", "Special")


def x_status_sp_attack_down(c):
    return _lower_attack(c, "spa", "Physical")


def _lower_defence(c, k):
    """Expert_StatusDefenseDown, Expert_StatusSpDefenseDown and
    Expert_StatusEvasionDown: one roll, -2 at 80.5%, when the user is below
    70% HP or else the foe's stage is at -3 or lower; -2 against a foe at
    70% HP or less."""
    s = -2 if (c.hu < 70 or c.t.stages[k] <= -3) and c.roll(80.5) else 0
    return s - (2 if c.ht <= 70 else 0)


def x_status_defense_down(c):
    return _lower_defence(c, "def")


def x_status_sp_defense_down(c):
    return _lower_defence(c, "spd")


def x_status_evasion_down(c):
    return _lower_defence(c, "eva")


# The Speed-lowering attacks Expert_SpeedDownOnHit names by move id.
SPEED_DOWN_NAMED = {"MOVE_ICY_WIND", "MOVE_ROCK_TOMB", "MOVE_MUD_SHOT", "MOVE_LOW_SWEEP", "MOVE_BULLDOZE",
                    "MOVE_ELECTROWEB", "MOVE_GLACIATE", "MOVE_DRUM_BEATING", "MOVE_POUNCE"}


def x_speed_down_on_hit(c):
    """Expert_SpeedDownOnHit: nothing into a resist; the named attacks go on
    to Expert_StatusSpeedDown, any other gets nothing."""
    if c.res or c.mv.const not in SPEED_DOWN_NAMED:
        return 0
    return x_status_speed_down(c)


def x_status_speed_down(c):
    """Expert_StatusSpeedDown: a user that is not slower (a tie counts as
    not slower), -3; a slower one, +2 at 72.7%."""
    if not c.slow:
        return -3
    return 2 if c.roll(72.7) else 0


def x_status_accuracy_down(c):
    """Expert_StatusAccuracyDown: Sand Attack and its kin."""
    u, t = c.u, c.t
    s = 0
    if (c.hu < 70 or c.ht <= 70) and c.roll(60.9):
        s -= 1
    if u.stages["acc"] <= -2 and c.roll(68.75):       # the user's own accuracy (expert-1.md bug 8)
        s -= 2
    if t.status == "tox" and c.roll(72.7):
        s += 2
    if t.seeded and c.roll(72.7):
        s += 2
    if (u.ingrained or getattr(u, "aqua_ring", False)) and c.roll(50):
        s += 1
    if t.cursed and c.roll(72.7):
        s += 2
    if c.hu > 70 or t.stages["acc"] == 0:
        return s
    if c.hu < 40 or c.ht < 40:
        return s - 2
    return s - (2 if c.roll(72.7) else 0)


FOUR = ("atk", "def", "spa", "spd")


def x_haze(c):
    """Expert_Haze: -3 at 80.5% when the user has stages to lose; +3 at
    80.5% when the foe has stages to lose, else -1 at 80.5%."""
    u, t = c.u, c.t
    s = 0
    if any(u.stages[k] >= 3 for k in FOUR + ("eva",)) or any(t.stages[k] <= -3 for k in FOUR + ("acc",)):
        if c.roll(80.5):
            s -= 3
    if any(t.stages[k] >= 3 for k in FOUR + ("eva",)) or any(u.stages[k] <= -3 for k in FOUR + ("acc",)):
        if c.roll(80.5):
            s += 3
    elif c.roll(80.5):
        s -= 1
    return s


def x_clear_smog(c):
    """Expert_ClearSmog (Oxide): the foe's half of Haze, without the -1."""
    t = c.t
    s = 0
    if any(t.stages[k] <= -3 for k in FOUR + ("acc",)) and c.roll(80.5):
        s -= 3
    if any(t.stages[k] >= 3 for k in FOUR + ("eva",)) and c.roll(80.5):
        s += 3
    return s


def x_bide(c):
    """Expert_Bide: -2 at 90% HP or less."""
    return -2 if c.hu <= 90 else 0


def x_force_switch(c):
    """Expert_ForceSwitch (Roar, Whirlwind, Dragon Tail, Circle Throw): a
    foe in for more than three turns, +2 at 75% and +2 at 50%; else hazards
    on its side or a foe stage at +3, +2 at 50%; else -3."""
    t, foe = c.t, c.foe
    if t.turns_in > 3:
        return (2 if c.roll(75) else 0) + (2 if c.roll(50) else 0)
    if any(foe.hazards.values()) or any(t.stages[k] >= 3 for k in FOUR + ("eva",)):
        return 2 if c.roll(50) else 0
    return -3


def x_conversion(c):
    """Expert_Conversion: -2 at 90% HP or less; -2 at 78.1% after the first turn."""
    s = -2 if c.hu <= 90 else 0
    return s - (2 if c.b.turn != 0 and c.roll(78.1) else 0)


def x_synthesis(c):
    """Expert_Synthesis: -2 in rain, sand or hail, then Expert_Recovery.
    Shore Up goes straight to Recovery by move id."""
    s = 0
    if c.mv.const != "MOVE_SHORE_UP" and c.b.weather in ("Rain", "Sand", "Hail"):
        s -= 2
    return s + x_recovery(c)


def x_recovery(c):
    """Expert_Recovery: at full HP -3; a user that is not slower -8 (the
    faster heal, kept as vanilla has it, expert-1.md bug 4); at 70% or
    more -3 at 88.3%; else +2 at 92.2%, at 56.2% once the foe has shown
    Snatch."""
    if c.hu == 100:
        return -3
    if not c.slow:
        return -8
    if c.hu >= 70 and c.roll(88.3):
        return -3
    snatch = any(m.effect == "STEAL_STATUS_MOVE" for m in shown(c.t))
    return 2 if (not snatch or c.roll(60.9)) and c.roll(92.2) else 0


def x_toxic_leech_seed(c):
    """Expert_ToxicLeechSeed: with an attack of its own, -3 at 80.5% for a
    user at half HP or less and again for a foe at half or less; +2 at
    76.6% when the user knows Protect."""
    s = 0
    has_power = any(m.power > 0 for m in c.u.moves)
    if has_power and c.hu <= 50 and c.roll(80.5):
        s -= 3
    if has_power and c.ht <= 50 and c.roll(80.5):
        s -= 3
    if any(m.effect in ("PROTECT", "SP_DEF_UP") for m in c.u.moves) and c.roll(76.6):
        s += 2
    return s


def _screen(c, hit):
    """Expert_LightScreen, Expert_Reflect and Expert_AuroraVeil: -2 below
    50% HP; +1 at 50% at 90% or more; +1 at 75% when the foe's last move
    was of the class the screen stops."""
    if c.hu < 50:
        return -2
    s = 1 if c.hu >= 90 and c.roll(50) else 0
    return s + (1 if hit and c.roll(75) else 0)


def x_light_screen(c):
    return _screen(c, c.t.last is not None and c.t.last.cat == "Special")


def x_reflect(c):
    return _screen(c, _prev_class(c.t) == "Physical")


def x_aurora_veil(c):
    return _screen(c, c.t.last is None or c.t.last.cat != "Status")


def x_rest(c):
    """Expert_Rest: by speed and HP, then +3 at 96.1% (77.3% once the foe
    has shown Snatch)."""
    hu = c.hu
    if not c.slow:
        if hu == 100:
            return -8
        if hu > 50:
            return -3
        if hu >= 40 and c.roll(72.7):
            return -3
    else:
        if hu > 70:
            return -3
        if hu >= 60 and c.roll(80.5):
            return -3
    snatch = any(m.effect == "STEAL_STATUS_MOVE" for m in shown(c.t))
    return 3 if (not snatch or c.roll(80.5)) and c.roll(96.1) else 0


def x_ohko_move(c):
    """Expert_OHKOMove: +1 at 25%."""
    return 1 if c.roll(25) else 0


def x_super_fang(c):
    """Expert_SuperFang: -1 against a foe at half HP or less."""
    return -1 if c.ht <= 50 else 0


def x_binding_move(c):
    """Expert_BindingMove: +1 at 50% on a foe that a trap keeps under Toxic,
    Curse, Perish Song or infatuation."""
    t = c.t
    if (t.status == "tox" or t.cursed or t.perish or _infatuated(t)) and c.roll(50):
        return 1
    return 0


def x_high_critical(c):
    """Expert_HighCritical: nothing into a resist; super-effective, +1 at
    50%; otherwise (neutral, or a number matching nothing) +1 at 25%."""
    if c.res:
        return 0
    if c.val in (DOUBLE, QUADRUPLE):
        return 1 if c.roll(50) else 0
    return 1 if c.roll(50) and c.roll(50) else 0


def x_swagger(c):
    """Expert_Swagger: with Psych Up (by move id), -5 unless the foe's
    Attack is at -3 or lower, then +3, +2 more on the battle's first turn
    (expert-1.md bug 9); otherwise as Flatter."""
    if _knows(c.u, "MOVE_PSYCH_UP"):
        if c.t.stages["atk"] >= -2:
            return -5
        return 3 + (2 if c.b.turn == 0 else 0)
    return x_flatter(c)


def x_flatter(c):
    """Expert_Flatter: +1 at 50%, then Expert_StatusConfuse."""
    return (1 if c.roll(50) else 0) + x_status_confuse(c)


def x_status_confuse(c):
    """Expert_StatusConfuse: above 70% foe HP nothing; then -1 at 50%, -1 at
    50% HP or less, -1 more at 30% or less."""
    if c.ht > 70:
        return 0
    s = -1 if c.roll(50) else 0
    if c.ht <= 50:
        s -= 1
    if c.ht <= 30:
        s -= 1
    return s


def x_status_poison(c):
    """Expert_StatusPoison: -1 for a user below 50% HP or a foe at 50% or less."""
    return -1 if c.hu < 50 or c.ht <= 50 else 0


def x_status_paralyze(c):
    """Expert_StatusParalyze: slower, +3 at 92.2%; not slower at 70% HP or less, -1."""
    if c.slow:
        return 3 if c.roll(92.2) else 0
    return -1 if c.hu <= 70 else 0


def x_vital_throw(c):
    """Expert_VitalThrow: slower or above 60% HP, nothing; below 40%, -1 at
    80.5%; between, -1 at 29.7% then 80.5%."""
    if c.slow or c.hu > 60:
        return 0
    if c.hu < 40:
        return -1 if c.roll(80.5) else 0
    return -1 if c.roll(29.7) and c.roll(80.5) else 0


def x_substitute(c):
    """Expert_Substitute: +1 at 62.5% with Focus Punch; -1 at 60.9% per HP
    band below 91%; moving first, +1 at 60.9% when the foe's last move was
    one a Substitute blocks and the foe is free of its condition."""
    u, t = c.u, c.t
    s = 1 if _knows(u, "MOVE_FOCUS_PUNCH") and c.roll(62.5) else 0
    rolls = 0 if c.hu > 90 else 1 if c.hu > 70 else 2 if c.hu > 50 else 3
    for _ in range(rolls):
        if c.roll(60.9):
            s -= 1
    if not c.slow:
        le = _prev_effect(t)
        if ((le in fs.STATUS_OF and not t.status) or (le == "STATUS_CONFUSE" and not t.confused)
                or (le == "STATUS_LEECH_SEED" and not t.seeded)) and c.roll(60.9):
            s += 1
    return s


def x_recharge_turn(c):
    """Expert_RechargeTurn: -1 into a resist; Truant, +1 at 68.75%;
    otherwise -1 when slower at 60% HP or more, or not slower above 40%."""
    if c.res:
        return -1
    if c.u.ability == "Truant":
        return 1 if c.roll(68.75) else 0
    if (c.slow and c.hu >= 60) or (not c.slow and c.hu > 40):
        return -1
    return 0


def x_disable(c):
    """Expert_Disable: moving first, -1 at 60.9% after a status move (or
    none), +1 after an attack."""
    if c.slow:
        return 0
    if _prev_power(c.t) == 0:
        return -1 if c.roll(60.9) else 0
    return 1


COUNTER_PHYSICAL_TYPES = {"Normal", "Fighting", "Flying", "Poison", "Ground", "Rock", "Bug", "Ghost", "Steel"}
MIRROR_COAT_SPECIAL_TYPES = {"Fire", "Water", "Grass", "Electric", "Psychic", "Ice", "Dragon", "Dark"}


def _counter_shape(c, other, cls, types_ok):
    """Expert_Counter and Expert_MirrorCoat: -1 against a foe asleep,
    infatuated or confused; -1 at 96.1% at 30% HP or less and -1 at 60.9%
    at half or less; knowing the other move, +4 at 60.9%; a taunted foe,
    +1 at 60.9%; then by the foe's last move: none or a status move, +4 at
    49% when its types fit the pre-split list (bug 10); the other class,
    -1; this class, +1 at 60.9%."""
    t = c.t
    if t.status == "slp" or t.confused or _infatuated(t):
        return -1
    s = 0
    if c.hu <= 30 and c.roll(96.1):
        s -= 1
    if c.hu <= 50 and c.roll(60.9):
        s -= 1
    if _knows(c.u, other):
        return s + (4 if c.roll(60.9) else 0)
    if t.taunt and c.roll(60.9):
        s += 1
    if _prev_power(t) == 0:
        if types_ok(set(t.types)) and c.roll(80.5) and c.roll(60.9):
            s += 4
        return s
    if t.last.cat != cls:
        return s - 1
    return s + (1 if c.roll(60.9) else 0)


def x_counter(c):
    return _counter_shape(c, "MOVE_MIRROR_COAT", "Physical", lambda ts: not ts & COUNTER_PHYSICAL_TYPES)


def x_mirror_coat(c):
    return _counter_shape(c, "MOVE_COUNTER", "Special", lambda ts: not ts & MIRROR_COAT_SPECIAL_TYPES)


ENCORE_EFFECTS = {
    "RECOVER_DAMAGE_SLEEP", "ATK_UP", "DEF_UP", "SPEED_UP", "SP_ATK_UP", "RESET_STAT_CHANGES",
    "FORCE_SWITCH", "CONVERSION", "STATUS_BADLY_POISON", "SET_LIGHT_SCREEN", "REST", "HALVE_HP",
    "SP_DEF_UP_2", "STATUS_CONFUSE", "STATUS_POISON", "STATUS_PARALYZE", "STATUS_LEECH_SEED",
    "DO_NOTHING", "ATK_UP_2", "ENCORE", "CONVERSION2", "NEXT_ATTACK_ALWAYS_HITS", "CURE_PARTY_STATUS",
    "PREVENT_ESCAPE", "STATUS_NIGHTMARE", "PROTECT", "SWITCH_ABILITIES", "FORESIGHT",
    "ALL_FAINT_3_TURNS", "WEATHER_SANDSTORM", "SURVIVE_WITH_1_HP", "ATK_UP_2_STATUS_CONFUSION",
    "INFATUATE", "PREVENT_STATUS", "WEATHER_RAIN", "WEATHER_SUN", "MAX_ATK_LOSE_HALF_MAX_HP",
    "COPY_STAT_CHANGES", "HIT_IN_3_TURNS", "ALWAYS_FLINCH_FIRST_TURN_ONLY", "STOCKPILE", "SPIT_UP",
    "SWALLOW", "WEATHER_HAIL", "TORMENT", "STATUS_BURN", "MAKE_GLOBAL_TARGET",
    "SP_DEF_UP_DOUBLE_ELECTRIC_POWER", "SWITCH_HELD_ITEMS", "COPY_ABILITY",
    "GROUND_TRAP_USER_CONTINUOUS_HEAL", "RECYCLE", "REMOVE_HELD_ITEM", "MAKE_SHARED_MOVES_UNUSEABLE",
    "HEAL_STATUS", "REMOVE_ALL_PP_ON_DEFEAT", "CONFUSE_ALL", "HALVE_ELECTRIC_DAMAGE",
    "HALVE_FIRE_DAMAGE", "ATK_SPD_UP", "CAMOUFLAGE", "GRAVITY", "IGNORE_EVATION_REMOVE_DARK_IMMUNE",
    "FAINT_AND_FULL_HEAL_NEXT_MON", "NATURAL_GIFT", "REMOVE_PROTECT", "DOUBLE_SPEED_3_TURNS",
    "RANDOM_STAT_UP_2", "FLING", "TRANSFER_STATUS", "PREVENT_HEALING", "SWAP_ATK_DEF",
    "SUPRESS_ABILITY", "PREVENT_CRITS", "SWAP_ATK_SP_ATK_STAT_CHANGES", "SWAP_DEF_SP_DEF_STAT_CHANGES",
    "SET_ABILITY_TO_INSOMNIA", "SWAP_STAT_CHANGES", "RESTORE_HP_EVERY_TURN", "GIVE_GROUND_IMMUNITY",
    "TRICK_ROOM"}


def x_encore(c):
    """Expert_Encore: a disabled foe, +3 at 88.3%; slower, or the foe's last
    move not worth locking in (the 82-effect list), -2; else +3 at 88.3%."""
    if getattr(c.t, "disabled", 0):
        return 3 if c.roll(88.3) else 0
    if c.slow or _prev_effect(c.t) not in ENCORE_EFFECTS:
        return -2
    return 3 if c.roll(88.3) else 0


def x_pain_split(c):
    """Expert_PainSplit: a foe below 80%, -1; else -1 above 60% HP when
    slower (40% when not), +1 at or below it."""
    if c.ht < 80:
        return -1
    return -1 if c.hu > (60 if c.slow else 40) else 1


def x_nightmare(c):
    """Expert_Nightmare (Snore's route): +2."""
    return 2


def x_lock_on(c):
    """Expert_LockOn: +2 at 50%."""
    return 2 if c.roll(50) else 0


def x_sleep_talk(c):
    """Expert_SleepTalk: asleep +10; awake -5."""
    return 10 if c.u.status == "slp" else -5


def x_destiny_bond(c):
    """Expert_DestinyBond: -1; moving first and hurt, back up by HP band."""
    s = -1
    if c.slow or c.hu > 70:
        return s
    if c.roll(50):
        s += 1
    if c.hu > 50:
        return s
    if c.roll(50):
        s += 1
    if c.hu > 30:
        return s
    return s + (2 if c.roll(60.9) else 0)


def x_reversal(c):
    """Expert_Reversal (Flail, Reversal): by HP band and speed."""
    s = 0
    if not c.slow:
        if c.hu > 33:
            return -1
        if c.hu > 20:
            return 0
        if c.hu < 8:
            s += 1
    else:
        if c.hu > 60:
            return -1
        if c.hu > 40:
            return 0
    return s + (1 if c.roll(60.9) else 0)


def x_heal_bell(c):
    """Expert_HealBell: -5 unless the user or a benched party member has a status."""
    if c.u.status or any(m.status for m in c.own.bench()):
        return 0
    return -5


# Expert_Thief_EncouragedItemEffects, as the script lists them.
THIEF_EFFECTS = {"SLP_RESTORE", "STATUS_RESTORE", "HP_RESTORE", "ACC_REDUCE", "HP_RESTORE_GRADUAL",
                 "PIKA_SPATK_UP", "CUBONE_ATK_UP", "WEAKEN_SE_FIRE", "WEAKEN_SE_WATER", "WEAKEN_SE_ELECTRIC",
                 "WEAKEN_SE_GRASS", "WEAKEN_SE_ICE", "WEAKEN_SE_FIGHT", "WEAKEN_SE_POISON", "WEAKEN_SE_GROUND",
                 "WEAKEN_SE_FLYING", "WEAKEN_SE_PSYCHIC", "WEAKEN_SE_BUG", "WEAKEN_SE_ROCK", "WEAKEN_SE_GHOST",
                 "WEAKEN_SE_DRAGON", "WEAKEN_SE_DARK", "WEAKEN_SE_STEEL", "WEAKEN_NORMAL", "WEAKEN_SE_FAIRY",
                 "HP_RESTORE_PSN_TYPE"}


def x_thief(c):
    """Expert_Thief (Thief, Covet): the foe's item, as the battle has named
    it (AI_CONTEXT.battlerHeldItems), on the script's list, +1 at 80.5%;
    anything else, an unnamed item included, -2."""
    item = c.t.item if getattr(c.t, "item_known", False) else None
    if _hold(item) not in THIEF_EFFECTS:
        return -2
    return 1 if c.roll(80.5) else 0


def x_curse(c):
    """Expert_Curse: a Ghost user, -1 at 80% HP or less; otherwise up to +3
    by its Defense stage, surer with Gyro Ball or Trick Room."""
    u = c.u
    if "Ghost" in u.types:
        return 0 if c.hu > 80 else -1
    if u.stages["def"] >= 4:
        return 0
    s = 0
    if _knows(u, "MOVE_GYRO_BALL", "MOVE_TRICK_ROOM"):
        if c.roll(87.5):                 # the 12.5% that fails skips the coin flip too
            s += 1
            if c.roll(50):
                s += 1
    elif c.roll(50):
        s += 1
    if u.stages["def"] >= 2:
        return s
    if c.roll(50):
        s += 1
    if u.stages["def"] >= 1:
        return s
    return s + (1 if c.roll(50) else 0)


def x_protect(c):
    """Expert_Protect: -2 at 50% once the foe has shown Feint or Shadow
    Force; a run of two or more, -2; the user wearing down (or the foe seen
    healing), -2; the foe wearing down, +2, else +2 at 33.2%; then -1 at
    50%, and -1 and -1 at 50% when the last move kept a run going."""
    u, t = c.u, c.t
    seen = shown(t)
    s = 0
    if any(m.const in ("MOVE_FEINT", "MOVE_SHADOW_FORCE") for m in seen) and c.roll(50):
        s -= 2
    if u.protect_run > 1:
        return s - 2
    if (u.status == "tox" or u.cursed or u.perish or _infatuated(u) or u.seeded or u.yawn
            or any(m.effect in ("RESTORE_HALF_HP", "DEF_UP_DOUBLE_ROLLOUT_POWER") for m in seen)):
        return s if getattr(u, "locked_on", False) else s - 2
    if (t.status == "tox" or t.cursed or t.perish or _infatuated(t) or t.seeded or t.yawn
            or getattr(c.b, "doubles", False) or getattr(u, "locked_on", False)):
        s += 2
    elif c.roll(33.2):
        s += 2
    if c.roll(50):
        s -= 1
    if u.protect_run:
        s -= 1
        if c.roll(50):
            s -= 1
    return s


def x_hazards(c):
    """Expert_Spikes, Expert_ToxicSpikes and Expert_StealthRock (Sticky Web
    too): +1 at 50%, then +1 at 75% when the user knows Roar or Whirlwind."""
    if not c.roll(50):
        return 0
    return 1 + (1 if _knows(c.u, "MOVE_ROAR", "MOVE_WHIRLWIND") and c.roll(75) else 0)


def x_foresight(c):
    """Expert_Foresight (with the battle_edits fix): a Ghost foe, +2 at
    47.3%; a foe at +3 evasion, +2 at 68.75%; otherwise -2."""
    if "Ghost" in c.t.types:
        return 2 if c.roll(68.75) and c.roll(68.75) else 0
    if c.t.stages["eva"] >= 3:
        return 2 if c.roll(68.75) else 0
    return -2


def x_endure(c):
    """Expert_Endure: 4% to 34% HP, +1 at 72.7%; otherwise -1."""
    if 4 <= c.hu < 35:
        return 1 if c.roll(72.7) else 0
    return -1


def x_baton_pass(c):
    """Expert_BatonPass: a stage at +3 or more is worth passing once the
    user is hurt (+2 at 68.75%); a best stage of +2, -2 unless hurt; nothing
    above +1, -2."""
    top = max(c.u.stages[k] for k in FOUR + ("eva",))
    if top >= 3:
        if c.hu > (70 if c.slow else 60):
            return 0
        return 2 if c.roll(68.75) else 0
    if top == 2:
        if (c.hu < 70) if c.slow else (c.hu <= 60):
            return 0
        return -2
    return -2


def x_pursuit(c):
    """Expert_Pursuit: +1 at 50% on the user's first turn in, otherwise +1
    at 50% against a Ghost or Psychic foe; then +1 at 50% if the foe has
    shown U-turn (by move id)."""
    s = 0
    if c.u.turns_in == 0:
        if c.roll(50):
            s += 1
    elif ("Ghost" in c.t.types or "Psychic" in c.t.types) and c.roll(50):
        s += 1
    if any(m.const == "MOVE_U_TURN" for m in shown(c.t)) and c.roll(50):
        s += 1
    return s


def x_rain_dance(c):
    """Expert_RainDance: a Swift Swim user not moving first (a tie half the
    time), +1; below 40% HP, -1; another weather up, +1; Rain Dish, or
    Hydration with a status, +1."""
    u = c.u
    if u.ability == "Swift Swim" and not c.faster():
        return 1
    if c.hu < 40:
        return -1
    if c.b.weather in ("Hail", "Sun", "Sand"):
        return 1
    if u.ability == "Rain Dish" or (u.ability == "Hydration" and u.status):
        return 1
    return 0


def x_sunny_day(c):
    """Expert_SunnyDay: below 40% HP, -1; another weather up, +1; Flower
    Gift, or Leaf Guard without a status (the battle_edits fix), +1."""
    u = c.u
    if c.hu < 40:
        return -1
    if c.b.weather in ("Hail", "Rain", "Sand"):
        return 1
    if u.ability == "Flower Gift" or (u.ability == "Leaf Guard" and not u.status):
        return 1
    return 0


def x_belly_drum(c):
    """Expert_BellyDrum: -2 below 90% HP."""
    return -2 if c.hu < 90 else 0


def x_psych_up(c):
    """Expert_PsychUp: only a foe stage at +3 is worth copying; then +1 if
    any of the user's four main stats is at +0 or lower, else +2 if its
    evasion is, else -2 at 80.5%."""
    u, t = c.u, c.t
    if not any(t.stages[k] >= 3 for k in FOUR + ("eva",)):
        return -2
    if any(u.stages[k] <= 0 for k in FOUR):
        return 1
    if u.stages["eva"] <= 0:
        return 2
    return -2 if c.roll(80.5) else 0


def x_charge_turn_no_invuln(c):
    """Expert_ChargeTurnNoInvuln (Solar Beam, Sky Attack, Skull Bash, Razor
    Wind, Freeze Shock, Ice Burn): each row ends the routine."""
    if c.res:
        return -2
    if c.e == "SKIP_CHARGE_TURN_IN_SUN" and c.b.weather == "Sun":
        return 2
    if c.u.item == "Power Herb":
        return 2
    if any(m.effect == "PROTECT" for m in shown(c.t)):
        return -2
    return -1 if c.hu <= 38 else 0


def x_thunder(c):
    """Expert_Thunder (Thunder, Hurricane): -3 at 80.5% into a resist or in
    sun, and stop; +1 in rain."""
    if c.res or c.b.weather == "Sun":
        return -3 if c.roll(80.5) else 0
    return 1 if c.b.weather == "Rain" else 0


def x_rain_storm(c):
    """Expert_RainStorm (the Hisuian storms, sure in rain, unhurt by sun)."""
    if c.res:
        return -3 if c.roll(80.5) else 0
    return 1 if c.b.weather == "Rain" else 0


def x_blizzard(c):
    """Expert_Blizzard: -3 at 80.5% into a resist; +1 in hail."""
    if c.res:
        return -3 if c.roll(80.5) else 0
    return 1 if c.b.weather == "Hail" else 0


def _in_the_air(c, shadow_force):
    """Expert_ChargeTurnWithInvuln and Expert_ShadowForce: Fly's group
    first takes a Power Herb (+2) and a foe seen using Protect (-1); then a
    resist, -1 (the battle_edits fix); Shadow Force with a Power Herb, +1;
    then the first of these rows that applies gives +1 at 68.75%: the foe
    under Toxic, Curse or Leech Seed, sand for a user it cannot hurt, hail
    for an Ice user, and a user that is not slower."""
    u, t = c.u, c.t
    if not shadow_force:
        if u.item == "Power Herb":
            return 2
        if any(m.effect == "PROTECT" for m in shown(t)):
            return -1
    if c.res:
        return -1
    if shadow_force and u.item == "Power Herb":
        return 1
    if t.status == "tox" or t.cursed or t.seeded:
        return 1 if c.roll(68.75) else 0
    if c.b.weather == "Sand" and set(u.types) & {"Ground", "Rock", "Steel"}:
        return 1 if c.roll(68.75) else 0
    if c.b.weather == "Hail" and "Ice" in u.types:
        return 1 if c.roll(68.75) else 0
    if c.slow or _prev_effect(t) == "NEXT_ATTACK_ALWAYS_HITS":
        return 0
    return 1 if c.roll(68.75) else 0


def x_charge_turn_with_invuln(c):
    return _in_the_air(c, False)


def x_shadow_force(c):
    return _in_the_air(c, True)


def x_fake_out(c):
    """Expert_FakeOut (Fake Out, First Impression): +2."""
    return 2


def x_spit_up(c):
    """Expert_SpitUp: with two Stockpiles or more, +2 at 68.75%."""
    return 2 if getattr(c.u, "stockpile", 0) >= 2 and c.roll(68.75) else 0


def x_hail(c):
    """Expert_Hail: -1 below 40% HP; with another weather up, +1, +2 more
    when the user knows Blizzard, +2 more with Ice Body."""
    if c.hu < 40:
        return -1
    if c.b.weather not in ("Sun", "Rain", "Sand"):
        return 0
    return 1 + (2 if _knows(c.u, "MOVE_BLIZZARD") else 0) + (2 if c.u.ability == "Ice Body" else 0)


def x_facade(c):
    """Expert_Facade (with the battle_edits fix): +1 when the user is
    poisoned, burned or paralysed."""
    return 1 if c.u.status in ("psn", "tox", "brn", "par") else 0


def x_focus_punch(c):
    """Expert_FocusPunch: each row ends the routine."""
    t = c.t
    if c.res:
        return -1
    if c.u.sub:
        return 5
    if t.status == "slp":
        return 1
    if t.confused or _infatuated(t):
        return 1 if c.roll(60.9) else 0
    if c.u.turns_in == 0:
        return 0
    return 1 if c.roll(21.9) else 0


def x_smelling_salts(c):
    """Expert_SmellingSalts: +1 against a paralysed foe."""
    return 1 if c.t.status == "par" else 0


TRICK_DISRUPTIVE = {"CHOICE_ATK", "CHOICE_SPATK", "CHOICE_SPEED", "SPEED_DOWN_GROUNDED", "PRIORITY_DOWN",
                    "DMG_USER_CONTACT_XFR", "LVLUP_ATK_EV_UP", "LVLUP_DEF_EV_UP", "LVLUP_SPATK_EV_UP",
                    "LVLUP_SPDEF_EV_UP", "LVLUP_SPEED_EV_UP", "LVLUP_HP_EV_UP"}   # Macho Brace left out (bug 13)
TRICK_BAD = TRICK_DISRUPTIVE | {"EVS_UP_SPEED_DOWN", "PSN_USER", "BRN_USER", "HP_RESTORE_PSN_TYPE"}
FLAVOUR = {"HP_RESTORE_SPICY", "HP_RESTORE_DRY", "HP_RESTORE_SWEET", "HP_RESTORE_BITTER", "HP_RESTORE_SOUR"}


def x_trick(c):
    """Expert_Trick (Trick, Switcheroo), by the user's own item's hold
    effect against the foe's item as the AI has seen it named (expert-2.md
    bugs 11, 12 and 13 kept)."""
    u, t = c.u, c.t
    mine = _hold(u.item)
    theirs = _hold(t.item if getattr(t, "item_known", False) else None)

    def poison_proof(m, side):
        return bool(m.status or side.safeguard or {"Steel", "Poison"} & set(m.types)
                    or m.ability in ("Immunity", "Magic Guard", "Poison Heal"))

    def burn_proof(m, side):
        return bool(m.status or side.safeguard or "Fire" in m.types or m.ability in ("Water Veil", "Magic Guard"))
    if mine in TRICK_DISRUPTIVE:
        return -3 if theirs in TRICK_BAD else 5
    if mine == "PSN_USER":
        if theirs in TRICK_BAD:
            return -3
        if not poison_proof(t, c.foe):
            return 5
        return -3 if poison_proof(u, c.own) or u.ability == "Klutz" else 5
    if mine == "BRN_USER":
        if theirs in TRICK_BAD:
            return -3
        if not burn_proof(t, c.foe):
            return 5
        if u.ability in ("Water Veil", "Magic Guard"):
            return -3
        if u.ability == "Klutz":
            return -5                      # bug 12, as the game has it
        return -3 if burn_proof(u, c.own) else 5
    if mine == "HP_RESTORE_PSN_TYPE":
        if theirs in TRICK_BAD:
            return -3
        if "Poison" in t.types:
            return -3 if "Poison" in u.types or u.ability in ("Magic Guard", "Klutz") else 5
        if t.ability == "Magic Guard":     # bug 11: the Toxic Orb checks
            return -3 if poison_proof(u, c.own) or u.ability == "Klutz" else 5
        return 5
    if mine in FLAVOUR:
        if theirs in TRICK_BAD or theirs in FLAVOUR:
            return -3
        return 2 if c.roll(80.5) else 0
    return -3


ROLE_PLAY_WANTED = {"Speed Boost", "Battle Armor", "Sand Veil", "Static", "Flash Fire", "Wonder Guard",
                    "Effect Spore", "Swift Swim", "Huge Power", "Rain Dish", "Cute Charm", "Shed Skin",
                    "Marvel Scale", "Pure Power", "Chlorophyll", "Shield Dust", "Adaptability",
                    "Magic Guard", "Mold Breaker", "Super Luck", "Unaware", "Tinted Lens", "Filter",
                    "Solid Rock", "Reckless"}


def x_change_user_ability(c):
    """Expert_ChangeUserAbility (Role Play, Skill Swap): -1 when the user's
    ability is already wanted or the foe's is not; else +2 at 80.5%."""
    if c.u.ability in ROLE_PLAY_WANTED or c.t.ability not in ROLE_PLAY_WANTED:
        return -1
    return 2 if c.roll(80.5) else 0


def x_nothing(c):
    """A routine that changes nothing (Expert_Ingrain, Expert_GyroBall)."""
    return 0


def x_superpower(c):
    """Expert_Superpower: a single -1 into a resist, with the user's Attack
    lowered, when slower at 60% HP or more, or not slower above 40%."""
    if c.res or c.u.stages["atk"] < 0:
        return -1
    if (c.slow and c.hu >= 60) or (not c.slow and c.hu > 40):
        return -1
    return 0


def x_magic_coat(c):
    """Expert_MagicCoat."""
    s = -1 if c.ht <= 30 and c.roll(60.9) else 0
    if c.u.turns_in == 0:
        return s + (1 if c.roll(41.4) else 0)
    return s - (1 if c.roll(88.3) else 0)


def x_recycle(c):
    """Expert_Recycle: +1 at 80.5% with a Chesto, Lum or Starf Berry to bring back, else -2."""
    if getattr(c.u, "recycle", None) not in ("Chesto Berry", "Lum Berry", "Starf Berry"):
        return -2
    return 1 if c.roll(80.5) else 0


def x_revenge(c):
    """Expert_Revenge (Avalanche, Revenge): -2 into a foe asleep, infatuated
    or confused; otherwise +2 at 29.7% and -2 the rest of the time."""
    t = c.t
    if t.status == "slp" or t.confused or _infatuated(t):
        return -2
    return 2 if c.roll(29.7) else -2


def x_brick_break(c):
    """Expert_BrickBreak: +1 with Reflect or Light Screen on the foe's side."""
    return 1 if c.foe.screens["Reflect"] or c.foe.screens["Light Screen"] else 0


def x_knock_off(c):
    """Expert_KnockOff: after the user's first turn out, against a foe at
    30% HP or more, +1 at 29.7%."""
    if c.ht < 30 or c.u.turns_in == 0:
        return 0
    return 1 if c.roll(29.7) else 0


def x_endeavor(c):
    """Expert_Endeavor: a foe below 70%, -1; else -1 above 50% HP when
    slower (40% when not), +1 at or below it."""
    if c.ht < 70:
        return -1
    return -1 if c.hu > (50 if c.slow else 40) else 1


def x_water_spout(c):
    """Expert_WaterSpout (with the battle_edits fix, the user's HP): -1 into
    a resist, or at 70% HP or less when slower (50% when not)."""
    if c.res:
        return -1
    return -1 if c.hu <= (70 if c.slow else 50) else 0


def x_imprison(c):
    """Expert_Imprison: after the first turn out, +2 at 60.9%."""
    return 2 if c.u.turns_in > 0 and c.roll(60.9) else 0


def x_refresh(c):
    """Expert_Refresh: -1 against a foe below 50% HP (the script reads the foe)."""
    return -1 if c.ht < 50 else 0


def x_snatch(c):
    """Expert_Snatch."""
    if c.u.turns_in == 0:
        return 2 if c.roll(41.4) else 0
    if not c.roll(88.3):
        return 0
    if c.slow:
        if c.ht > 25:
            return -2 if c.roll(88.3) else 0
        if any(m.effect in ("RESTORE_HALF_HP", "DEF_UP_DOUBLE_ROLLOUT_POWER") for m in shown(c.t)):
            return 2 if c.roll(41.4) else 0
        if c.roll(10.2):
            return 1
        return -2 if c.roll(88.3) else 0
    if c.hu != 100 or c.ht < 70 or c.roll(76.6):
        return -2 if c.roll(88.3) else 0
    return 0


def _sport(c, ty):
    """Expert_MudSport and Expert_WaterSport: -1 below 50% HP; +1 against a
    foe of the type it weakens, -1 against any other."""
    if c.hu < 50:
        return -1
    return 1 if ty in c.t.types else -1


def x_mud_sport(c):
    return _sport(c, "Electric")


def x_water_sport(c):
    return _sport(c, "Fire")


def x_self_drop(c):
    """Expert_Overheat and Expert_CloseCombat: -1 into a resist, when slower
    at 80% HP or less, or when not slower at 60% or less."""
    if c.res:
        return -1
    return -1 if (c.slow and c.hu <= 80) or (not c.slow and c.hu <= 60) else 0


def x_dragon_dance(c):
    """Expert_DragonDance and the new setup moves routed to it: a slower
    user, +1 at 50%, and stop either way; one that is not slower, -1 at
    72.7% at half HP or less."""
    if c.slow:
        return 1 if c.roll(50) else 0
    return -1 if c.hu <= 50 and c.roll(72.7) else 0


def x_gravity(c):
    """Expert_Gravity (Gravity, Smack Down, Thousand Arrows): +1 at 75%
    against a foe in the air; a grounded one at 60% HP or more, +1 at 37.5%."""
    t = c.t
    airborne = t.ability == "Levitate" or getattr(t, "magnet_rise", 0) or "Flying" in t.types
    if not airborne and (c.hu < 60 or not c.roll(50)):
        return 0
    return 1 if c.roll(75) else 0


def x_miracle_eye(c):
    """Expert_MiracleEye: a Dark foe, +2 at 47.3%; +3 evasion, +2 at 68.75%; else -2."""
    if "Dark" in c.t.types:
        return 2 if c.roll(68.75) and c.roll(68.75) else 0
    if c.t.stages["eva"] >= 3:
        return 2 if c.roll(68.75) else 0
    return -2


def x_wake_up_slap(c):
    """Expert_WakeUpSlap: -1 into a resist; +1 on a sleeping foe."""
    if c.res:
        return -1
    return 1 if c.t.status == "slp" else 0


def x_hammer_arm(c):
    """Expert_HammerArm: -1 into a resist; +1 when slower."""
    if c.res:
        return -1
    return 1 if c.slow else 0


def x_brine(c):
    """Expert_Brine: -1 into a resist; a foe at half HP or less, +1, and +1 more at 50%."""
    if c.res:
        return -1
    if c.ht > 50:
        return 0
    return 2 if c.roll(50) else 1


def x_feint(c):
    """Expert_Feint (a Protect run of exactly 2 falls to the run-0 row,
    expert-2.md bug 9)."""
    u, t = c.u, c.t
    if not any(m.effect == "PROTECT" for m in shown(t)) and not c.roll(25):
        return 0
    s = 0
    worn = u.status == "tox" or u.cursed or u.perish or _infatuated(u) or u.seeded or u.yawn
    healing = c.ht != 100 and _hold(t.item if getattr(t, "item_known", False) else None) in (
        "HP_RESTORE_GRADUAL", "HP_RESTORE_PSN_TYPE")
    if (worn or healing) and c.roll(50):
        s += 1
    run = t.protect_run
    if run == 1:
        return s + (1 if c.roll(25) else 0)
    if run > 2:
        return s - 2
    return s + (1 if c.roll(50) else 0)


def x_pluck(c):
    """Expert_Pluck (Bug Bite, Pluck, Incinerate): -1 into a resist; +1 at
    75% on the user's first turn out; +1 at 50%."""
    if c.res:
        return -1
    s = 1 if c.u.turns_in == 0 and c.roll(75) else 0
    return s + (1 if c.roll(50) else 0)


def x_tailwind(c):
    """Expert_Tailwind: a quarter of the time nothing; then a user that
    moves first (a tie half the time) -1, at 30% HP or less -1, above 75%
    +1, else +1 at 75%."""
    if not c.roll(75):
        return 0
    if c.faster() or c.hu <= 30:
        return -1
    return 1 if c.hu > 75 or c.roll(75) else 0


def x_acupressure(c):
    """Expert_Acupressure."""
    if c.hu < 51:
        return -1
    if c.hu > 90 or c.roll(50):
        return 1 if c.roll(75) else 0
    return 0


def x_metal_burst(c):
    """Expert_MetalBurst."""
    t = c.t
    if t.status == "slp" or t.confused or _infatuated(t) or any(
            m.effect in ("DOUBLE_POWER_IF_HIT", "HIT_LAST_WHIFF_IF_HIT", "PRIORITY_NEG_1_BYPASS_ACCURACY")
            for m in shown(t)):
        return -1
    s = 0
    if c.hu <= 30 and c.roll(96.1):
        s -= 1
    if c.hu <= 50 and c.roll(60.9):
        s -= 1
    if c.roll(25):
        s += 1
    if t.taunt:
        if _prev_power(t) != 0 and c.roll(60.9):
            s += 1
        if c.roll(60.9):
            s += 1
    return s


def _u_turn(c, check_resist):
    """Expert_UTurn, and Expert_PartingShot without the resist check. With
    nobody to switch to, nothing (Parting Shot is then scored as Growl,
    before this is reached)."""
    if check_resist and c.res:
        return -1
    if not c.own.bench():
        return 0
    s = 0
    # A super-effective attack of its own makes switching out worse (by type
    # and power, as AI_HasSuperEffectiveMove reads it: attacks only).
    if _se_moves(c.b, c.u, c.t) and c.roll(75):
        s -= 2
    # Nobody on the bench hits harder: -2 at 75% and stop.
    if not _bench_outdamages(c.b, c.own, c.u, c.t) and c.roll(75):
        return s - 2
    if c.ht > 70:
        if c.roll(75):
            s += 1
        if c.roll(50):
            s += 1
    elif c.ht > 30:
        if c.roll(50):
            s += 1
    elif c.roll(50) and c.roll(50):
        s += 1
    if c.faster() or c.roll(50):
        s += 1
    return s


def x_u_turn(c):
    return _u_turn(c, True)


def x_parting_shot(c):
    if not c.own.bench():
        return x_status_attack_down(c)
    return _u_turn(c, False)


def x_payback(c):
    """Expert_Payback: -1 into a resist; moving first (a tie half the time)
    or below 30% HP, nothing; else +1 at 75%."""
    if c.res:
        return -1
    if c.faster() or c.hu < 30:
        return 0
    return 1 if c.roll(75) else 0


def x_assurance(c):
    """Expert_Assurance (the Jaboca and Rowap row never matches, expert-2.md bug 4)."""
    if c.res:
        return -1
    if c.faster():
        return 0
    if c.u.ability == "Rough Skin" or c.roll(50):
        return 1 if c.roll(50) else 0
    return 0


def x_embargo(c):
    """Expert_Embargo (Embargo, Magic Room): +1 at 50%."""
    return 1 if c.roll(50) else 0


def x_fling(c):
    """Expert_Fling, by the held item's Fling power."""
    if c.res:
        keeps = ("SOMETIMES_FLINCH", "STRENGTHEN_POISON", "PSN_USER", "BRN_USER", "PIKA_SPATK_UP")
        return 0 if _hold(c.u.item) in keeps else -1
    p = _item(c.u.item).get("flingPower", 0) or 0
    if p < 30:
        return -2
    if p > 90:
        s = 0
        if c.val in (DOUBLE, QUADRUPLE):
            s += 4
        elif c.roll(50):
            s += 1
        return s + (1 if c.roll(75) else 0)
    if p > 60:
        return 1 if c.roll(75) else 0
    return -1 if c.roll(50) else 0


def x_psycho_shift(c):
    """Expert_PsychoShift: -10 without a status to pass; +1 at 50% on a foe at 30% HP or more."""
    if not c.u.status:
        return -10
    return 1 if c.roll(50) and c.ht >= 30 else 0


def x_trump_card(c):
    """Expert_TrumpCard: by the move's PP left, then the foe's Pressure and accuracy stages."""
    if c.res:
        return -1
    pp = c.u.pp.get(c.mv.name, 0)
    if pp == 1:
        return 3
    if pp == 2:
        return 1 + (1 if c.roll(60.9) else 0)
    if pp == 3:
        return 1 if c.roll(60.9) else 0
    s = 1 if c.t.ability == "Pressure" and c.roll(88.3) else 0
    if c.t.stages["eva"] >= 5 or c.u.stages["acc"] <= -5:
        return s + 1 + (1 if c.roll(60.9) else 0)
    if c.t.stages["eva"] >= 3 or c.u.stages["acc"] <= -3:
        return s + (1 if c.roll(60.9) else 0)
    return s


HEAL_BLOCK_SEEN = {"RECOVER_DAMAGE_SLEEP", "RESTORE_HALF_HP", "HEAL_HALF_REMOVE_FLYING_TYPE", "UNUSED_157",
                   "HEAL_HALF_MORE_IN_SUN", "REST", "SWALLOW", "RECOVER_HALF_DAMAGE_DEALT",
                   "GROUND_TRAP_USER_CONTINUOUS_HEAL", "RESTORE_HP_EVERY_TURN", "STATUS_LEECH_SEED",
                   "FAINT_AND_FULL_HEAL_NEXT_MON", "FAINT_FULL_RESTORE_NEXT_MON"}


def x_heal_block(c):
    """Expert_HealBlock: a foe seen healing (or the user seeded, the foe
    rooted or ringed), else at 37.5%: +1 at 90.2%."""
    t = c.t
    if (any(m.effect in HEAL_BLOCK_SEEN for m in shown(t)) or c.u.seeded or t.ingrained
            or getattr(t, "aqua_ring", False) or c.roll(37.5)):
        return 1 if c.roll(90.2) else 0
    return 0


def x_wring_out(c):
    """Expert_WringOut (Wring Out, Crush Grip)."""
    if c.res or c.ht < 50:
        return -1
    s = 0
    if c.ht == 100:
        s += 1 if c.slow else 2
    elif c.ht <= 85:
        return 0
    return s + (1 if c.roll(90.2) else 0)


def x_power_trick(c):
    """Expert_PowerTrick (Power Trick, Power Shift)."""
    if c.hu > 90:
        return 1 if c.roll(62.5) else 0
    if c.hu > 60:
        return 1 if c.roll(50) else 0
    if c.hu > 30:
        return 1 if c.roll(35.9) else 0
    return -2


def x_gastro_acid(c):
    """Expert_GastroAcid."""
    if not c.roll(75):
        return 0
    s = 1
    if c.ht > 70:
        return s
    if c.roll(50):
        s -= 1
    if c.ht > 50:
        return s
    s -= 1
    return s if c.ht > 30 else s - 1


def x_lucky_chant(c):
    """Expert_LuckyChant: -1 below 70% HP; +1 when the foe has shown a
    high-critical attack, else at 25%."""
    if c.hu < 70:
        return -1
    crit = ("HIGH_CRITICAL", "HIGH_CRITICAL_BURN_HIT", "HIGH_CRITICAL_POISON_HIT")
    return 1 if any(m.effect in crit for m in shown(c.t)) or c.roll(25) else 0


def x_me_first(c):
    """Expert_MeFirst."""
    if c.slow:
        return -2
    s = 1 if _self_hit_beats(c.b, c.u, c.t) and c.roll(87.5) else 0
    if c.t.last is not None and c.t.last.cat == "Status":
        return s + (1 if c.roll(75) else 0)
    if c.roll(50):
        s += 1 + (1 if c.roll(75) else 0)
    return s


def x_copycat(c):
    """Expert_Copycat (the table is Mirror Move's)."""
    beats = _self_hit_beats(c.b, c.u, c.t)
    liked = c.t.last is not None and c.t.last.const in MIRROR_MOVE_TABLE
    if not c.slow:
        if beats:
            return 2 if c.roll(87.5) else 0
        if liked:
            return 2 if c.roll(50) else 0
    if beats or liked:
        return 0
    return -1 if c.roll(68.75) else 0


def _swap_ladder(c, d1, d2):
    """Expert_PowerSwap's and Expert_GuardSwap's ladder (expert-2.md bug 5
    kept): the two stage differences pick a top rung; each rung down to +1
    is a 50% try, stopping at the first won."""
    if d1 > 3:
        top = 5 if d2 > 3 else 4 if d2 > 1 else 3 if d2 == 0 else 0
    elif d1 > 1:
        top = 4 if d2 > 3 else 3 if d2 > 1 else 2 if d2 == 0 else 0
    elif d1 > 0:
        top = 3 if d2 > 3 else 2 if d2 > 1 else 1 if d2 == 0 else 0
    elif d1 == 0:
        top = 3 if d2 > 3 else 2 if d2 > 1 else 1 if d2 > 0 else 0
    else:
        top = 0
    for n in range(top, 0, -1):
        if c.roll(50):
            return n
    return 0


def x_power_swap(c):
    return _swap_ladder(c, c.t.stages["atk"] - c.u.stages["atk"], c.t.stages["spa"] - c.u.stages["spa"])


def x_guard_swap(c):
    return _swap_ladder(c, c.t.stages["def"] - c.u.stages["def"], c.t.stages["spd"] - c.u.stages["spd"])


def x_punishment(c):
    """Expert_Punishment (the vanilla fix: the first rung won ends it)."""
    if c.res:
        return 0
    up = sum(v for v in c.t.stages.values() if v > 0)
    top = 4 if up > 6 else 3 if up > 5 else 2 if up > 4 else 1 if up > 2 else 0
    for n in range(top, 0, -1):
        if c.roll(50):
            return n
    return 0


def x_last_resort(c):
    """Expert_LastResort: -1 into a resist; +1 once every other move has been used."""
    if c.res:
        return -1
    n = len(c.u.moves)
    return 1 if n > 1 and getattr(c.u, "last_resort_count", 0) >= n - 1 else 0


def x_worry_seed(c):
    """Expert_WorrySeed (Worry Seed, Entrainment)."""
    s = 1 if any(m.const == "MOVE_REST" for m in shown(c.t)) else 0
    if c.hu >= 50 and c.roll(50):
        s += 1
    return s + (1 if c.roll(75) else 0)


def x_sucker_punch(c):
    """Expert_SuckerPunch (Sucker Punch, Thunderclap): -1 into a resist; +1 at 75%."""
    if c.res:
        return -1
    return 1 if c.roll(75) else 0


def x_shell_trap(c):
    """Expert_ShellTrap (the move reworks, 2026-10-06): -1 into a resist or
    an immunity; else -2 unless the target's last move was physical (before
    it has moved, its last move reads as physical)."""
    if c.res:
        return -1
    return 0 if _prev_class(c.t) == "Physical" else -2


def x_heart_swap(c):
    """Expert_HeartSwap (Focus Energy is the simulator's crit_stage)."""
    u, t = c.u, c.t
    if not (any(t.stages[k] >= 2 for k in FOUR + ("eva",)) or t.crit_stage):
        return -2
    if any(u.stages[k] <= 0 for k in FOUR):
        return 1
    if u.stages["eva"] <= 0:
        return 2
    if not u.crit_stage:
        return 1
    return -2 if c.roll(80.5) else 0


def x_aqua_ring(c):
    """Expert_AquaRing: at 30% HP or more, +1 at 50%."""
    return 1 if c.hu >= 30 and c.roll(50) else 0


def x_magnet_rise(c):
    """Expert_MagnetRise: at half HP or more, +1 once the foe has shown a
    Ground attack, and +1 against a Ground foe, else at 50%."""
    if c.hu < 50:
        return 0
    s = 1 if any(m.const in ("MOVE_EARTHQUAKE", "MOVE_EARTH_POWER", "MOVE_FISSURE") for m in shown(c.t)) else 0
    return s + (1 if "Ground" in c.t.types or c.roll(50) else 0)


def x_defog(c):
    """Expert_Defog (with the exit expert-2.md's table misses)."""
    own, foe = c.own, c.foe
    s = 0
    if own.bench() and (any(own.hazards.values()) or getattr(own, "web", 0)):
        s += 2
    foe_haz = any(foe.hazards.values()) or getattr(foe, "web", 0)
    last_roll = False
    if foe.screens["Light Screen"] or foe.screens["Reflect"] or getattr(foe, "veil", 0):
        if c.hu <= 30 and not own.bench():
            last_roll = True
        else:
            s += 1
            if not foe.bench():
                return s
            if foe_haz and c.roll(50):
                s -= 1
    elif foe_haz:
        s -= 2
    if (last_roll or c.hu < 70 or c.t.stages["eva"] <= -3) and c.roll(80.5):
        s -= 2
    if c.ht <= 70:
        s -= 2
    return s


def x_trick_room(c):
    """Expert_TrickRoom: nothing in a double battle or for a last Pokemon at
    30% HP or less; slower, +3 at 75%; not slower, -1."""
    if getattr(c.b, "doubles", False) or (c.hu <= 30 and not c.own.bench()):
        return 0
    if not c.slow:
        return -1
    return 3 if c.roll(75) else 0


def x_captivate(c):
    """Expert_Captivate: Attack Down's rows on Sp. Atk, then -1 at 75% when
    the foe's last move was physical (or none)."""
    t = c.t
    s = 0
    if t.stages["spa"] != 0:
        s -= 1
        if c.hu <= 90:
            s -= 1
        if t.stages["spa"] <= -3 and c.roll(80.5):
            s -= 2
    if c.ht <= 70:
        s -= 2
    if _prev_class(t) == "Physical" and c.roll(75):
        s -= 1
    return s


def x_recoil_move(c):
    """Expert_RecoilMove: nothing into a resist; +1 with Rock Head or Magic Guard."""
    if c.res:
        return 0
    return 1 if c.u.ability in ("Rock Head", "Magic Guard") else 0


def x_healing_wish(c):
    """Expert_HealingWish (Healing Wish, Lunar Dance)."""
    if c.hu >= 80 and not c.slow:
        return -5 if c.roll(25) else 0
    if c.hu > 50:
        return -1 if c.roll(80.5) else 0
    s = 0
    if c.roll(25):
        s += 1
        if not _se_moves(c.b, c.u, c.t) and c.roll(25):
            s += 1
        if _bench_outdamages(c.b, c.own, c.u, c.t) and c.roll(50):
            s += 1
    if c.hu <= 30 and c.roll(50):
        s += 1
    return s


def x_doubled(c):
    """Expert_Hex, Expert_Venoshock, Expert_Acrobatics and Expert_BoltBeak:
    -1 into a resist; +1 when the power doubles (Bolt Beak: moving first, a
    tie half the time)."""
    if c.res:
        return -1
    e = c.e
    if e in ("DOUBLE_DAMAGE_ON_STATUS", "BURN_HIT_DOUBLE_POWER_ON_STATUS"):
        return 1 if c.t.status or c.t.ability == "Comatose" else 0
    if e in ("DOUBLE_POWER_ON_POISONED", "POISON_HIT_DOUBLE_POWER_ON_POISONED"):
        return 1 if c.t.status in ("psn", "tox") else 0
    if e == "DOUBLE_DAMAGE_WITHOUT_ITEM":
        return 1 if not c.u.item else 0
    return 1 if c.faster() else 0


def _speed_up_on_hit(c):
    """Expert_SpeedUpOnHit: -1 into a resist; under Trick Room, at +6 Speed
    or moving first, nothing; else +1 at 50%."""
    if c.res:
        return -1
    if c.b.trick_room or c.u.stages["spe"] >= 6 or c.faster():
        return 0
    return 1 if c.roll(50) else 0


def _spin_clears(c):
    """Rapid Spin's and Mortal Spin's clearing: +2 when the user is bound or
    seeded, or its side has a hazard with a party member left to come in."""
    own = c.own
    if c.u.bound or c.u.seeded or (own.bench() and (any(own.hazards.values()) or getattr(own, "web", 0))):
        return 2
    return 0


def x_rapid_spin(c):
    """Expert_RapidSpin: into an immune foe nothing is cleared, -1; else the
    clearing, then Expert_SpeedUpOnHit."""
    if c.val == IMMUNE:
        return -1
    return _spin_clears(c) + _speed_up_on_hit(c)


def x_speed_up_on_hit(c):
    return _speed_up_on_hit(c)


def x_mortal_spin(c):
    """Expert_MortalSpin: Rapid Spin's clearing without the Speed raise."""
    if c.val == IMMUNE:
        return -1
    return _spin_clears(c)


# Each Expert_Main label, by its routine above.
EXPERT_ROUTINES = {
    "Expert_StatusSleep": x_status_sleep, "Expert_DrainMove": x_drain_move,
    "Expert_Explosion": x_explosion, "Expert_DreamEater": x_dream_eater,
    "Expert_MirrorMove": x_mirror_move, "Expert_StatusAttackUp": x_status_attack_up,
    "Expert_StatusDefenseUp": x_status_defense_up, "Expert_StatusSpeedUp": x_status_speed_up,
    "Expert_StatusSpAttackUp": x_status_sp_attack_up, "Expert_StatusSpDefenseUp": x_status_sp_defense_up,
    "Expert_StatusAccuracyUp": x_status_accuracy_up, "Expert_StatusEvasionUp": x_status_evasion_up,
    "Expert_BypassAccuracyMove": x_bypass_accuracy_move, "Expert_StatusAttackDown": x_status_attack_down,
    "Expert_StatusDefenseDown": x_status_defense_down, "Expert_StatusSpeedDown": x_status_speed_down,
    "Expert_StatusSpAttackDown": x_status_sp_attack_down,
    "Expert_StatusSpDefenseDown": x_status_sp_defense_down,
    "Expert_StatusAccuracyDown": x_status_accuracy_down, "Expert_StatusEvasionDown": x_status_evasion_down,
    "Expert_Haze": x_haze, "Expert_ClearSmog": x_clear_smog, "Expert_Bide": x_bide,
    "Expert_ForceSwitch": x_force_switch, "Expert_Conversion": x_conversion,
    "Expert_Synthesis": x_synthesis, "Expert_Recovery": x_recovery,
    "Expert_ToxicLeechSeed": x_toxic_leech_seed, "Expert_LightScreen": x_light_screen,
    "Expert_Reflect": x_reflect, "Expert_AuroraVeil": x_aurora_veil, "Expert_Rest": x_rest,
    "Expert_OHKOMove": x_ohko_move, "Expert_SuperFang": x_super_fang,
    "Expert_BindingMove": x_binding_move, "Expert_HighCritical": x_high_critical,
    "Expert_Swagger": x_swagger, "Expert_Flatter": x_flatter, "Expert_StatusConfuse": x_status_confuse,
    "Expert_StatusPoison": x_status_poison, "Expert_StatusParalyze": x_status_paralyze,
    "Expert_SpeedDownOnHit": x_speed_down_on_hit, "Expert_VitalThrow": x_vital_throw,
    "Expert_Substitute": x_substitute, "Expert_RechargeTurn": x_recharge_turn,
    "Expert_Disable": x_disable, "Expert_Counter": x_counter, "Expert_Encore": x_encore,
    "Expert_PainSplit": x_pain_split, "Expert_Nightmare": x_nightmare, "Expert_LockOn": x_lock_on,
    "Expert_SleepTalk": x_sleep_talk, "Expert_DestinyBond": x_destiny_bond,
    "Expert_Reversal": x_reversal, "Expert_HealBell": x_heal_bell, "Expert_Thief": x_thief,
    "Expert_Curse": x_curse, "Expert_Protect": x_protect, "Expert_Spikes": x_hazards,
    "Expert_ToxicSpikes": x_hazards, "Expert_StealthRock": x_hazards,
    "Expert_Foresight": x_foresight, "Expert_Endure": x_endure, "Expert_BatonPass": x_baton_pass,
    "Expert_Pursuit": x_pursuit, "Expert_RainDance": x_rain_dance, "Expert_SunnyDay": x_sunny_day,
    "Expert_BellyDrum": x_belly_drum, "Expert_PsychUp": x_psych_up, "Expert_MirrorCoat": x_mirror_coat,
    "Expert_ChargeTurnNoInvuln": x_charge_turn_no_invuln, "Expert_Thunder": x_thunder,
    "Expert_RainStorm": x_rain_storm, "Expert_Blizzard": x_blizzard,
    "Expert_ChargeTurnWithInvuln": x_charge_turn_with_invuln, "Expert_ShadowForce": x_shadow_force,
    "Expert_FakeOut": x_fake_out, "Expert_SpitUp": x_spit_up, "Expert_Hail": x_hail,
    "Expert_Facade": x_facade, "Expert_FocusPunch": x_focus_punch,
    "Expert_SmellingSalts": x_smelling_salts, "Expert_Trick": x_trick,
    "Expert_ChangeUserAbility": x_change_user_ability, "Expert_Ingrain": x_nothing,
    "Expert_GyroBall": x_nothing, "Expert_Superpower": x_superpower, "Expert_MagicCoat": x_magic_coat,
    "Expert_Recycle": x_recycle, "Expert_Revenge": x_revenge, "Expert_BrickBreak": x_brick_break,
    "Expert_KnockOff": x_knock_off, "Expert_Endeavor": x_endeavor, "Expert_WaterSpout": x_water_spout,
    "Expert_Imprison": x_imprison, "Expert_Refresh": x_refresh, "Expert_Snatch": x_snatch,
    "Expert_MudSport": x_mud_sport, "Expert_WaterSport": x_water_sport, "Expert_Overheat": x_self_drop,
    "Expert_CloseCombat": x_self_drop, "Expert_DragonDance": x_dragon_dance, "Expert_Gravity": x_gravity,
    "Expert_MiracleEye": x_miracle_eye, "Expert_WakeUpSlap": x_wake_up_slap,
    "Expert_HammerArm": x_hammer_arm, "Expert_HealingWish": x_healing_wish, "Expert_Brine": x_brine,
    "Expert_Feint": x_feint, "Expert_Pluck": x_pluck, "Expert_Tailwind": x_tailwind,
    "Expert_Acupressure": x_acupressure, "Expert_MetalBurst": x_metal_burst, "Expert_UTurn": x_u_turn,
    "Expert_PartingShot": x_parting_shot, "Expert_Payback": x_payback, "Expert_Assurance": x_assurance,
    "Expert_Embargo": x_embargo, "Expert_Fling": x_fling, "Expert_PsychoShift": x_psycho_shift,
    "Expert_TrumpCard": x_trump_card, "Expert_HealBlock": x_heal_block, "Expert_WringOut": x_wring_out,
    "Expert_PowerTrick": x_power_trick, "Expert_GastroAcid": x_gastro_acid,
    "Expert_LuckyChant": x_lucky_chant, "Expert_MeFirst": x_me_first, "Expert_Copycat": x_copycat,
    "Expert_PowerSwap": x_power_swap, "Expert_GuardSwap": x_guard_swap,
    "Expert_Punishment": x_punishment, "Expert_LastResort": x_last_resort,
    "Expert_WorrySeed": x_worry_seed, "Expert_SuckerPunch": x_sucker_punch, "Expert_ShellTrap": x_shell_trap,
    "Expert_HeartSwap": x_heart_swap, "Expert_AquaRing": x_aqua_ring, "Expert_MagnetRise": x_magnet_rise,
    "Expert_Defog": x_defog, "Expert_TrickRoom": x_trick_room, "Expert_Captivate": x_captivate,
    "Expert_RecoilMove": x_recoil_move, "Expert_Hex": x_doubled, "Expert_Venoshock": x_doubled,
    "Expert_Acrobatics": x_doubled, "Expert_BoltBeak": x_doubled,
    "Expert_RapidSpin": x_rapid_spin, "Expert_SpeedUpOnHit": x_speed_up_on_hit,
    "Expert_MortalSpin": x_mortal_spin}


@functools.lru_cache(maxsize=None)
def _script_lines():
    path = os.path.join(data.ROOT, "src", "battle", "trainer_ai", "script.s")
    with open(path, encoding="utf-8") as f:
        return tuple(f.read().splitlines())


@functools.lru_cache(maxsize=None)
def script_table(label):
    """The battle effects a TableEntry list in script.s names, by its
    label, so the flags read the script's own lists."""
    lines = _script_lines()
    out = set()
    for line in lines[lines.index(label + ":") + 1:]:
        st = line.strip()
        if not st or st.startswith("//"):
            continue
        if not st.startswith("TableEntry") or "TABLE_END" in st:
            break
        m = re.match(r"TableEntry BATTLE_EFFECT_(\w+)", st)
        if m:
            out.add(m.group(1))
    return frozenset(out)


@functools.lru_cache(maxsize=None)
def expert_routes():
    """{effect: label} from Expert_Main's jump table in script.s, first
    match winning, as the script runs it."""
    lines = _script_lines()
    start = lines.index("Expert_Main:")
    routes = {}
    for line in lines[start + 1:]:
        s = line.strip()
        if s.startswith("PopOrEnd"):
            break
        m = re.match(r"IfCurrentMoveEffectEqualTo BATTLE_EFFECT_(\w+), (\w+)", s)
        if m:
            routes.setdefault(m.group(1), m.group(2))
    return routes


def expert(b, u, t, mv, f=None):
    """The Expert flag's change to one move's score: its routine by
    Expert_Main's table, or nothing for an effect the table leaves out."""
    label = expert_routes().get(mv.effect)
    if label is None:
        return 0
    return EXPERT_ROUTINES[label](_Ctx(b, u, t, mv))


def check_hp(b, u, t, mv):
    """CheckHP_Main: one table by the user's HP band (above 70%, 31% to 70%,
    30% or less) and one by the target's (the band above 70% is an empty
    table); a move in either takes -2 at 80.5%."""
    e = mv.effect
    hu, ht = u.frac(), t.frac()
    s = 0
    mine = ("CheckHP_DiscourageAtHighHP" if hu > 70 else "CheckHP_DiscourageAtMediumHP" if hu > 30
            else "CheckHP_DiscourageAtLowHP")
    if e in script_table(mine) and chance(b, 80.5):
        s -= 2
    theirs = ("CheckHP_Target_DiscourageAtHighHP" if ht > 70 else "CheckHP_Target_DiscourageAtMediumHP"
              if ht > 30 else "CheckHP_Target_DiscourageAtLowHP")
    if e in script_table(theirs) and chance(b, 80.5):
        s -= 2
    return s


# BatonPass_EvalMove names these by move id.
BATON_BOOSTS = {"MOVE_SWORDS_DANCE", "MOVE_DRAGON_DANCE", "MOVE_CALM_MIND", "MOVE_NASTY_PLOT"}


def baton_pass(b, u, t, mv, f):
    """BatonPass_Main: moves without a damage comparison, while a party
    member is left to pass to. Without Baton Pass it still runs 68.75% of
    the time. The four named boosts, and any other move after +3 at 92.2%
    (it falls through, vanilla), take +5 on the battle's first turn, -10
    below 60% HP, else +1; Protect, -2 after the user's own Protect or
    Detect, else +2; Baton Pass, -2 on the first turn, else up to +3 by
    the first of Attack and Sp. Atk raised."""
    if not _side(b, u).bench() or f is not None:
        return 0
    if not any(m.effect == "PASS_STATS_AND_STATUS" for m in u.moves) and not chance(b, 68.75):
        return 0
    s = 0
    if mv.const in BATON_BOOSTS:
        pass
    elif mv.effect == "PROTECT":
        return -2 if u.last is not None and u.last.const in ("MOVE_PROTECT", "MOVE_DETECT") else 2
    elif mv.const == "MOVE_BATON_PASS":
        if b.turn == 0:
            return -2
        for k in ("atk", "spa"):
            if u.stages[k] >= 1:
                return min(u.stages[k], 3)
        return 0
    else:
        if not chance(b, 92.2):
            return 0
        s = 3
    if b.turn == 0:
        return s + 5
    if u.frac() < 60:
        return s - 10
    return s + 1


def record_last_move(t):
    """TrainerAI_RecordLastMove, run before every decision: the target's
    previous move joins the moves the AI has seen it use (four at most;
    none after a turn it could not act)."""
    if t.last is not None and t.last not in t.shown and len(t.shown) < 4:
        t.shown.append(t.last)


def choose(b, u, t):
    """('move', Move) or ('switch', index), in the engine's order: a locked
    Pokemon picks nothing (Battler_CanPickCommand); the target's last move
    joins the moves the AI has seen; TrainerAI_PickCommand asks the switch
    rules; the command input gives Struggle when every move is ruled out and
    the Encore move under Encore; then the scores, the highest winning and
    ties at random. A Choice lock rules the other moves out (invalid)."""
    forced = forced_choice(u)
    if forced is not None:
        return forced
    record_last_move(t)
    sw = should_switch(b, _side(b, u), u, t)
    if sw is not None:
        return "switch", sw
    fixed = fixed_move(b, u)
    if fixed is not None:
        return fixed
    scores = score_moves(b, u, t, b.ai_flags)
    top = max(scores)
    picks = [i for i, sc in enumerate(scores) if sc == top]
    return "move", u.moves[b.rng.choice(picks)]


def forced_choice(u):
    """The action a locked, charging or recharging Pokemon takes without a
    choice (Battler_CanPickCommand), else None."""
    if u.lock:
        return "move", u.lock[0]
    if u.charging is not None:
        return "move", u.charging
    if u.recharge:
        return "move", u.moves[0]
    return None


def fixed_move(b, u):
    """Struggle when every move is ruled out, the Encore move under Encore;
    None when the scores decide."""
    if all(invalid(b, u, m) for m in u.moves):
        return "move", fs.move("Struggle")
    enc = getattr(u, "encore", None)
    if enc is not None:
        return "move", next(m for m in u.moves if m.name == enc)
    return None


def skip_odds(n):
    """The percent chance that `IfRandomLessThan n` does not jump."""
    return (256 - n) * 100 / 256


def ally_slot(b, u):
    """The Pokemon in u's partner slot, standing or not; None in a single
    battle. The weather rows and the partner's Lightning Rod and Storm Drain
    checks read the slot without asking whether it stands."""
    side = _side(b, u)
    if side.active2 is None:
        return None
    idx = side.active2 if side.mons[side.active] is u else side.active
    return side.mons[idx]


def other_foe(b, u, t):
    """The target's partner on the field, or None when that slot stands empty."""
    return next((x for x in fs.foes_of(b, u) if x is not t), None) if getattr(b, "doubles", False) else None


def ai_sees(b, u, mon, name):
    """AICmd_CheckBattlerAbility answering "have"."""
    return check_ability(b, u, mon, name) == "have"


# ---- Tag Strategy ----------------------------------------------------------------------------------
#
# TagStrategy_Main for a move aimed at a foe: the damage step, then the
# first special case that fits (script.s, TagStrategy_Main through
# TagStrategy_CheckFireMove); TagStrategy_Partner for a move aimed at the
# AI's own partner. The flag runs in every trainer double battle (forced on)
# and in the single battles of the trainers whose files carry it.

TAG_FLAT = {"ONE_HIT_KO", "40_DAMAGE_FLAT", "LEVEL_DAMAGE_FLAT", "RANDOM_DAMAGE_1_TO_150_LEVEL", "20_DAMAGE_FLAT"}
QUAKES = {"Earthquake", "Magnitude", "Bulldoze"}
BOOMS = {"Explosion", "Self-Destruct"}
NEW_SPREAD = {"Brutal Swing", "Boomburst", "Sludge Wave", "Petal Blizzard", "Synchronoise", "Misty Explosion"}
NOT_PORTED = {"Skill Swap", "Future Sight", "Doom Desire", "Gravity", "Trick Room"}


def tag_strategy(b, u, t, mv, ally):
    """TagStrategy_Main for a move aimed at a foe. The damage step: a
    resisted move that does not knock out loses 1 (2 for a quarter) at 75%
    while the target's partner stands; the strongest move of the AI's two
    Pokemon on this target (a fainted partner's moves still count) +1 at 50%
    (80.5% for the priority-one effect); otherwise, or when that roll fails,
    a twice effective move +1 at 60.9% and a four times one +1 at 75%. The
    flat-damage effects skip the effectiveness parts."""
    s = 0
    f = figure(b, u, t, mv)
    if f is not None:
        flat = mv.effect in TAG_FLAT
        if not flat:
            m = script_eff(b, u, t, mv)
            kills = f >= t.hp and not (t.hp == t.maxhp and t.ability == "Sturdy" and not mold(u, t))
            tp = other_foe(b, u, t)
            if m in (HALF, QUARTER) and not kills and tp is not None and tp.frac() > 0 and chance(b, 75):
                s -= 1 if m == HALF else 2
        mate = ally_slot(b, u)
        mine = [figure(b, u, t, x) or 0 for x in u.moves]
        theirs = [figure(b, mate, t, x) or 0 for x in mate.moves] if mate is not None else []
        if f >= max(mine + theirs) and chance(b, skip_odds(50) if mv.effect == "PRIORITY_1" else 50):
            s += 1
        elif not flat:
            m = script_eff(b, u, t, mv)
            if m == DOUBLE and chance(b, skip_odds(100)):
                s += 1
            elif m == QUADRUPLE and chance(b, 75):
                s += 1
    return s + tag_special(b, u, t, mv, ally)


def tag_special(b, u, t, mv, ally):
    """TagStrategy_CheckSpecialScoring: the first case that fits, by move
    id, then by listed type (Weather Ball by its weather), then Helping Hand."""
    n = mv.name
    if n in QUAKES:
        return _tag_quake(u, ally)
    if n in BOOMS:
        return _tag_boom(u, ally)
    if n in NEW_SPREAD:
        return _tag_spread(b, u, mv, ally)
    if n in NOT_PORTED:
        return 0          # no trainer in a double battle carries these (2026-09-30)
    if n in ("Rain Dance", "Sunny Day", "Hail", "Sandstorm"):
        return _tag_weather(b, u, n)
    if n == "Follow Me":
        return _tag_follow_me(b, u, ally)
    ty = move_type(b, u, mv) if n == "Weather Ball" else mv.type
    if ty == "Electric":
        return _tag_electric(b, u, t, mv, ally)
    if ty == "Fire":
        return _tag_fire(u, mv, ally)
    if ty == "Water":
        return _tag_water(b, u, t, mv, ally)
    # TagStrategy_PartnerKnowsHelpingHand: a damaging move with a comparison,
    # flat damage aside, beside a standing Helping Hand user.
    if ally is not None and any(x.name == "Helping Hand" for x in ally.moves) \
            and mv.effect not in TAG_FLAT and figure(b, u, t, mv) is not None:
        return 1
    return 0


def _tag_quake(u, ally):
    """TagStrategy_Earthquake (Earthquake, Magnitude, Bulldoze)."""
    if ally is None:
        return 0
    if getattr(ally, "magnet_rise", 0):
        return 2
    if not mold(u, ally) and ally.ability in ("Levitate", "Telepathy"):
        return 2
    tys = set(ally.types)
    if "Flying" in tys:
        return 2
    if tys & {"Fire", "Electric", "Poison", "Rock"}:
        return -10
    return -3 if "Steel" not in tys or tys & {"Bug", "Grass"} else -10


def _tag_boom(u, ally):
    """TagStrategy_Explosion."""
    if ally is None or "Ghost" in ally.types:
        return 0
    if not mold(u, ally) and ally.ability == "Telepathy":
        return 0
    return -3 if set(ally.types) & {"Rock", "Steel"} else -10


def _tag_spread(b, u, mv, ally):
    """TagStrategy_SpreadMove (the new spread moves)."""
    if ally is None:
        return 0
    boom = mv.name == "Misty Explosion"
    if not mold(u, ally):
        if ally.ability == "Telepathy" or (mv.name == "Boomburst" and ally.ability == "Soundproof"):
            return 0 if boom else 2
        if mv.name == "Petal Blizzard" and ally.ability == "Sap Sipper":
            return 3
    m = script_eff(b, u, ally, mv)
    if m == IMMUNE:
        return 0 if boom else 2
    if m in (DOUBLE, QUADRUPLE):
        return -10
    if m in (HALF, QUARTER):
        return -3
    return -10 if boom else -3


def _sun_part(b, x):
    a = x.ability
    if a == "Leaf Guard":
        return 2 if not x.status and x.frac() >= 30 else 0
    if a == "Flower Gift":
        return 2
    if a == "Dry Skin":
        return -2
    if a == "Solar Power":
        # The +1 at half HP or more runs on into the 50% -2 (bug O5, vanilla).
        return (1 if x.frac() >= 50 else 0) - (2 if chance(b, 50) else 0)
    return 0


def _tag_weather(b, u, name):
    """TagStrategy_RainDance, SunnyDay, Hail and Sandstorm: the rows for the
    user and whoever is in its partner slot."""
    total = 0
    for x in (u, ally_slot(b, u)):
        if x is None:
            continue
        if name == "Rain Dance":
            total += 2 if x.ability == "Dry Skin" or (x.ability == "Hydration" and x.status) else 0
        elif name == "Sunny Day":
            total += _sun_part(b, x)
        elif name == "Hail":
            blizzard = any(m.name == "Blizzard" for m in x.moves) and (x is u or x.alive())
            total += 2 if x.ability in ("Ice Body", "Snow Cloak") or blizzard else 0
        else:
            total += 2 if x.ability == "Sand Veil" or "Rock" in x.types else 0
    return total


def _tag_follow_me(b, u, ally):
    """TagStrategy_FollowMe: -10 with no partner for good; otherwise by the
    user's and the partner's HP bands, at 75%."""
    if ally is None:
        return -10
    hu, ha = u.frac(), ally.frac()
    if hu <= 30:
        return -5 if chance(b, 75) else 0
    band = 0 if ha > 90 else 1 if ha > 50 else 2 if ha > 30 else 3
    row = (-1, 1, 2, 3) if hu > 90 else (-2, -1, 1, 2) if hu > 50 else (-2, -2, 1, 2)
    return row[band] if chance(b, 75) else 0


def can_draw_in(u, mv):
    """IfMoveCanBeDrawnIn: a single target or random foe, no Normalize, no Mold Breaker."""
    return mv.range in ("SINGLE_TARGET", "RANDOM_OPPONENT") and u.ability not in ("Normalize", "Mold Breaker")


def _tag_electric(b, u, t, mv, ally):
    """TagStrategy_CheckElectricMove."""
    if mv.name in ("Discharge", "Parabolic Charge"):
        if ally is None:
            return 0
        if not mold(u, ally) and ally.ability in ("Motor Drive", "Volt Absorb", "Lightning Rod", "Telepathy"):
            return 3
        tys = set(ally.types)
        if "Ground" in tys:
            return 3
        return -10 if tys & {"Water", "Flying"} else -3
    if not can_draw_in(u, mv):
        return 0
    tp = other_foe(b, u, t)
    if tp is not None and ai_sees(b, u, tp, "Lightning Rod"):
        return -10
    mate = ally_slot(b, u)
    return -10 if mate is not None and mate.ability == "Lightning Rod" else 0


def _tag_water(b, u, t, mv, ally):
    """TagStrategy_CheckWaterMove."""
    if mv.name in ("Surf", "Sparkling Aria"):
        if ally is None:
            return 0
        if mv.name == "Sparkling Aria" and not mold(u, ally) and ally.ability == "Soundproof":
            return 2
        if not mold(u, ally):
            if ally.ability in ("Dry Skin", "Water Absorb", "Storm Drain"):
                return 3
            if ally.ability == "Telepathy":
                return 2
        tys = set(ally.types)
        if tys & {"Ground", "Fire"}:
            return -10
        return -3 if "Rock" not in tys or tys & {"Water", "Grass", "Dragon"} else -10
    if not can_draw_in(u, mv):
        return 0
    tp = other_foe(b, u, t)
    if tp is not None and ai_sees(b, u, tp, "Storm Drain"):
        return -10
    mate = ally_slot(b, u)
    return -10 if mate is not None and mate.ability == "Storm Drain" else 0


def _tag_fire(u, mv, ally):
    """TagStrategy_CheckFireMove."""
    s = 1 if getattr(u, "flash_fire", False) else 0
    if mv.name not in ("Lava Plume", "Searing Shot", "Mind Blown") or ally is None:
        return s
    if not mold(u, ally):
        if ally.ability == "Dry Skin":
            return s - 3
        if ally.ability == "Flash Fire":
            return s + 3
        if ally.ability == "Telepathy":
            return s + 2
    return s - 10 if set(ally.types) & {"Grass", "Steel", "Ice", "Bug"} else s - 3


def _absorb_ladder(b, x):
    h = x.frac()
    if h == 100:
        return -10
    if h > 90:
        return 0
    return 3 if chance(b, 25 if h > 75 else 50 if h > 50 else 75) else 0


def _raise_rule(b, x, stat):
    """Motor Drive, Lightning Rod, Storm Drain and Sap Sipper: 62.5% no
    change, else -30 at +6 and +3 below."""
    if chance(b, 62.5):
        return 0
    return -30 if x.stages[stat] >= 6 else 3


def _p_electric(b, x):
    if x.ability == "Motor Drive":
        return _raise_rule(b, x, "spe")
    if x.ability == "Volt Absorb":
        return _absorb_ladder(b, x)
    if x.ability == "Lightning Rod":
        return _raise_rule(b, x, "spa")
    return -30


def _p_water(b, x):
    if x.ability in ("Water Absorb", "Dry Skin"):
        return _absorb_ladder(b, x)
    return _raise_rule(b, x, "spa") if x.ability == "Storm Drain" else -30


def _p_grass(b, x):
    return _raise_rule(b, x, "atk") if x.ability == "Sap Sipper" else -30


def _p_fire(x):
    return 3 if x.ability == "Flash Fire" and not getattr(x, "flash_fire", False) else -30


def tag_partner(b, u, ally, mv):
    """TagStrategy_Partner: a move aimed at the AI's own partner. Only
    whether the result keeps the score at 100 or more matters to the driver."""
    if ally is None:
        return -30
    ty = move_type(b, u, mv) if mv.name == "Weather Ball" else mv.type
    if mv.damaging() and has_comparison(mv):
        rule = {"Fire": lambda: _p_fire(ally), "Electric": lambda: _p_electric(b, ally),
                "Water": lambda: _p_water(b, ally), "Grass": lambda: _p_grass(b, ally)}.get(ty)
        return rule() if rule else -30
    if ty == "Grass":
        return _p_grass(b, ally)
    n = mv.name
    if n == "Will-O-Wisp":
        if ally.ability == "Flash Fire":
            return _p_fire(ally)
        ok = (ally.ability == "Guts" and not ally.status and "Fire" not in ally.types
              and ally.item not in ("Flame Orb", "Toxic Orb") and ally.frac() >= 81)
        return 5 if ok else -30
    if n == "Thunder Wave":
        if "Ground" in ally.types or ally.ability not in ("Motor Drive", "Volt Absorb", "Lightning Rod"):
            return -30
        return _p_electric(b, ally)
    if mv.effect in ("STATUS_BADLY_POISON", "STATUS_POISON"):
        ok = ally.ability == "Poison Heal" and not ally.status and ally.item != "Toxic Orb" and ally.frac() <= 91
        return 5 if ok else -30
    if n == "Helping Hand":
        if ally.frac() == 0:
            return -30
        others = fs.foes_of(b, u) + [u]
        if ally.frac() > 50 or all(b.speed(ally) > b.speed(x) for x in others):
            return 2 if chance(b, 75) else -1
        return 0
    if n == "Swagger":
        if ally.item not in ("Persim Berry", "Lum Berry"):
            return -30
        return 0 if ally.stages["atk"] >= 2 else 3
    if n == "Gastro Acid":
        return 5 if ally.ability in ("Truant", "Slow Start") else -30
    if n == "Acupressure":
        if any(v >= 6 for v in ally.stages.values()):
            return -30
        if ally.frac() < 51:
            return -1
        if ally.frac() <= 90 and chance(b, 50):
            return 0
        return 2 if chance(b, skip_odds(80)) else 0
    return -30        # Skill Swap's partner rules are not ported; no double battle carries it


def partner_scores(b, u, ally, flags):
    """The partner pass: every routine but Tag Strategy and Check HP stops at
    once on the partner, and Check HP runs the partner rules again."""
    out = []
    for mv in u.moves:
        if u.pp.get(mv.name, 1) <= 0:
            out.append(0)
            continue
        s = 0 if invalid(b, u, mv) else 100
        for bit in (TAG, CHECK_HP):
            if flags >> bit & 1:
                s += tag_partner(b, u, ally, mv)
                s = 0 if s < 0 or s > 127 else s
        out.append(s)
    return out


def choose_doubles(b, u):
    """('move', Move, target): TrainerAI_MainDoubles. Each other standing
    battler is scored as the target in turn, the AI's partner included, with
    Tag Strategy forced on; each target keeps its best move (ties at
    random); a partner whose best is below 100 is dropped; the target with
    the highest best wins (ties at random); a move for the user or its ally
    aimed at the foe's side, and a non-Ghost Curse, turn on the user."""
    if u.lock:
        return "move", u.lock[0], None
    if u.charging is not None:
        return "move", u.charging, None
    if u.recharge:
        return "move", u.moves[0], None
    flags = b.ai_flags | 1 << TAG
    ally = fs.ally_of(b, u)
    per_target = []
    for t in fs.foes_of(b, u) + ([ally] if ally is not None else []):
        if t is not ally:
            record_last_move(t)
        scores = partner_scores(b, u, ally, flags) if t is ally else score_moves(b, u, t, flags)
        top = max(scores)
        if t is ally and top < 100:
            continue
        i = b.rng.choice([k for k, sc in enumerate(scores) if sc == top])
        per_target.append((top, u.moves[i], t))
    if not per_target:
        return "move", u.moves[0], None
    top = max(x[0] for x in per_target)
    _s, mv, t = b.rng.choice([x for x in per_target if x[0] == top])
    if (mv.range == "USER_OR_ALLY" and t.side == "p") or (mv.effect == "CURSE" and "Ghost" not in u.types):
        t = u
    return "move", mv, t


# ---- switching and the post-knockout pick ------------------------------------------------------
#
# These read the engine's effectiveness flags rather than a type product
# (the Scoring Agent's audit, 2026-09-30). BattleSystem_ApplyTypeChart (the
# active Pokemon's moves) and BattleSystem_CalcEffectiveness (the bench, the
# post-knockout pick) walk the type chart entry by entry and keep "super
# effective" and "not very effective" as flags each later entry toggles, so
# an immunity met first does not stop a later weakness from setting "super
# effective" (switching-and-items.md bug 10, vanilla, kept): Earthquake reads
# super effective on Skarmory, Thunderbolt on Gliscor, Poison moves on a
# Steel or Fairy type.

# The order the chart meets a defender's types in, for the attacking types
# whose immunity is not their last entry (battle_lib.c, sTypeMatchupMultipliers).
CHART_ORDER = {
    "Electric": ("Water", "Electric", "Grass", "Ground", "Flying", "Dragon"),
    "Poison": ("Grass", "Poison", "Ground", "Rock", "Ghost", "Steel", "Fairy"),
    "Ground": ("Fire", "Electric", "Grass", "Poison", "Flying", "Bug", "Rock", "Steel"),
    "Psychic": ("Fighting", "Poison", "Psychic", "Dark", "Steel"),
    "Ghost": ("Normal", "Psychic", "Dark", "Steel", "Ghost"),
}


_FLAGS = {}
_CHARTS = {}


def type_flags(b, mtype, types, scrappy=False):
    """(no effect, super effective, not very effective) as the engine's
    flags read for a move of this type into these types; kept by the chart,
    the move's type, the target's types and Scrappy, all it depends on."""
    chart = b.st["chart"]
    _CHARTS[id(chart)] = chart          # held, so its id is never reused
    k = (id(chart), mtype, tuple(types), scrappy)
    got = _FLAGS.get(k)
    if got is None:
        got = _FLAGS[k] = _type_flags(b, mtype, types, scrappy)
    return got


def _type_flags(b, mtype, types, scrappy=False):
    def mul(ty):
        # Scrappy stops the chart before Normal and Fighting meet Ghost.
        if scrappy and ty == "Ghost" and mtype in ("Normal", "Fighting"):
            return 1.0
        return fs.effectiveness(b.st["chart"], mtype, [ty])
    order = CHART_ORDER.get(mtype)
    tys = list(dict.fromkeys(t.title() for t in types))
    if order:
        tys.sort(key=lambda ty: order.index(ty) if ty in order else len(order))
    else:
        tys.sort(key=lambda ty: mul(ty) == 0)     # every other immunity is the last entry met
    ine = se = nve = False
    for ty in tys:
        m = mul(ty)
        if m == 0:
            ine, se, nve = True, False, False
        elif m < 1:
            se, nve = (False, nve) if se else (False, True)
        elif m > 1:
            se, nve = (se, False) if nve else (True, False)
    return ine, se, nve


def active_flags(b, u, mv, foe):
    """BattleSystem_ApplyTypeChart's flags for the active Pokemon's move: a
    move of power 0 never sets "super" or "not very", Levitate sets a flag
    of its own (neither "no effect" nor super effective), and an Air Balloon
    makes a Ground move "no effect"."""
    ty = "Normal" if u.ability == "Normalize" else move_type(b, u, mv)
    if ty == "Ground" and mv.name != "Thousand Arrows":
        if foe.ability == "Levitate" and not mold(u, foe):
            return False, False, False
        if foe.item == "Air Balloon":
            return True, False, False
    ine, se, nve = type_flags(b, ty, foe.types, u.ability == "Scrappy")
    return (ine, se, nve) if mv.power else (ine, False, False)


def bench_flags(b, att_ability, mtype, foe):
    """BattleSystem_CalcEffectiveness's flags: power is not read, so status
    moves count (bug 9, kept); Levitate is "no effect" to a Ground move;
    Wonder Guard makes anything not super effective "no effect"."""
    if att_ability == "Normalize":
        mtype = "Normal"
    mold = att_ability == "Mold Breaker"
    if mtype == "Ground" and foe.ability == "Levitate" and not mold:
        return True, False, False
    ine, se, nve = type_flags(b, mtype, foe.types, att_ability == "Scrappy")
    if foe.ability == "Wonder Guard" and not mold and not se:
        ine = True
    return ine, se, nve


def _se_moves(b, mon, t):
    """The active Pokemon's moves AI_HasSuperEffectiveMove counts (attacks
    only, by ApplyTypeChart's flag)."""
    return [m for m in mon.moves if active_flags(b, mon, m, t)[1]]


def _any_se_moves(b, mon, t):
    """A Pokemon's moves CalcEffectiveness marks super effective on t, status
    moves included: the bench checks and the post-knockout pick read these."""
    return [m for m in mon.moves if bench_flags(b, mon.ability, move_type(b, mon, m), t)[1]]


# The abilities that take a type's moves, as AI_AbilityAbsorbsType has them
# (Oxide adds Storm Drain, Dry Skin, Lightning Rod, Motor Drive, Sap Sipper).
ABSORBS = {"Fire": {"Flash Fire"}, "Water": {"Water Absorb", "Storm Drain", "Dry Skin"},
           "Electric": {"Volt Absorb", "Lightning Rod", "Motor Drive"}, "Grass": {"Sap Sipper"}}


def _hit_type(mon, hit):
    """The type of the move that last hit mon, as the absorber rule reads it:
    its listed type, except Weather Ball, which reads the type the battle
    recorded when it hit (moveHitType)."""
    if hit.name == "Weather Ball":
        return getattr(mon, "last_hit_type", None) or hit.type
    return hit.type


def ai_trapped(b, u, t):
    """The trap test at the top of TrainerAI_ShouldSwitch: a Ghost is never
    held; otherwise a bind, Mean Look or Block, its own Ingrain, a foe's
    Shadow Tag or Arena Trap (the AI exempts no Flying or Levitate user),
    or another battler's Magnet Pull on a Steel user."""
    if "Ghost" in u.types:
        return False
    if u.trapped_by is not None or u.bound or u.ingrained:
        return True
    foes = fs.foes_of(b, u) if getattr(b, "doubles", False) else [t]
    if any(f.ability in ("Shadow Tag", "Arena Trap") for f in foes):
        return True
    near = foes + ([fs.ally_of(b, u)] if getattr(b, "doubles", False) and fs.ally_of(b, u) else [])
    return "Steel" in u.types and any(m.ability == "Magnet Pull" for m in near)


def _party_counter(b, side, bench, t, hit, want, p):
    """AI_HasPartyMemberWithSuperEffectiveMove: a bench Pokemon the last hit
    cannot touch (want "ine") or that resists it (want "nve"), read with the
    hitter's ability and type for the move, with a roll of p per move of any
    kind super effective on the hitter."""
    if hit is None or not hit.power:
        return None
    htype = move_type(b, t, hit)
    for i in bench:
        mon = side.mons[i]
        ine, _se, nve = bench_flags(b, t.ability, htype, mon)
        if ine if want == "ine" else nve:
            for _m in _any_se_moves(b, mon, t):
                if chance(b, p):
                    return i
    return None


def should_switch(b, side, u, t):
    """TrainerAI_ShouldSwitch, rule by rule; in singles each party check
    reads the one foe as both defenders, so it rolls twice."""
    if ai_trapped(b, u, t):
        return None
    bench = [i for i, m in enumerate(side.mons) if i != side.active and m.alive()]
    if not bench:
        return None
    # AI_PerishSongKO
    if u.perish == 1:
        return replacement(b, side, t)
    # AI_CannotDamageWonderGuard: no super-effective attack on a Wonder Guard foe.
    if t.ability == "Wonder Guard" and not _se_moves(b, u, t):
        for i in bench:
            for _m in _any_se_moves(b, side.mons[i], t):
                if chance(b, 66.7):
                    return i
    # AI_OnlyIneffectiveMoves: two or more attacks, every one with no effect.
    dmg = [m for m in u.moves if m.power]
    if len(dmg) >= 2 and all(active_flags(b, u, m, t)[0] for m in dmg):
        for i in bench:
            mon = side.mons[i]
            for m in mon.moves:
                if m.power and bench_flags(b, mon.ability, move_type(b, mon, m), t)[1]:
                    for _ in range(2):
                        if chance(b, 66.7):
                            return i
        for i in bench:
            mon = side.mons[i]
            for m in mon.moves:
                if m.power and bench_flags(b, mon.ability, move_type(b, mon, m), t) == (False, False, False):
                    for _ in range(2):
                        if chance(b, 50):
                            return i
    hit = u.last_hit_by
    # AI_HasAbsorbAbilityInParty: a super-effective attack of its own keeps it
    # in two times in three; otherwise a bench member that takes the type of
    # the attack that hit it comes in, one time in two.
    if not (_se_moves(b, u, t) and chance(b, 66.7)) and hit is not None and hit.power:
        htype = _hit_type(u, hit)
        if u.ability not in ABSORBS.get(htype, ()):
            for i in bench:
                if side.mons[i].ability in ABSORBS.get(htype, ()) and chance(b, 50):
                    return i
    # AI_IsAsleepWithNaturalCure, at half HP or more.
    if u.status == "slp" and u.ability == "Natural Cure" and u.hp >= u.maxhp // 2:
        if hit is None and chance(b, 50):
            return replacement(b, side, t)
        if (hit is None or not hit.power) and chance(b, 50):
            return replacement(b, side, t)
        for want in ("ine", "nve"):
            i = _party_counter(b, side, bench, t, hit, want, 100)
            if i is not None:
                return i
        if chance(b, 50):
            return replacement(b, side, t)
    # AI_HasSuperEffectiveMove: each super-effective attack keeps it in nine
    # times in ten; AI_IsHeavilyStatBoosted (four or more stages up, accuracy
    # and evasion counted) keeps it in.
    for _m in _se_moves(b, u, t):
        if chance(b, 90):
            return None
    if sum(v for v in u.stages.values() if v > 0) >= 4:
        return None
    # AI_HasPartyMemberWithSuperEffectiveMove: immune, one in two per move;
    # resisting, one in three per move.
    for want, p in (("ine", 50), ("nve", 100 / 3)):
        i = _party_counter(b, side, bench, t, hit, want, p)
        if i is not None:
            return i
    return None


PINCH = {"Overgrow": "Grass", "Blaze": "Fire", "Torrent": "Water", "Swarm": "Bug"}


def _ko_score(b, fainted, cand, target, m):
    """One move's stage 2 score in BattleAI_PostKOSwitchIn: the move costed by
    BattleSystem_CalcMoveDamage as the fainted Pokemon would use it (its
    stats and stages, the target's stages and screens, its HP of 0, so a
    pinch ability counts; no same-type bonus or type yet), cut to a byte;
    then ApplyTypeChart (the fainted Pokemon's same-type bonus, the chart,
    Filter, Solid Rock, Expert Belt, Tinted Lens), cut to a byte again; 0
    into an immunity. A status move costs 2 (no class branch, CalcMoveDamage
    returns its closing + 2). The calculator's top roll includes the
    same-type bonus and the type, so they are divided back out of it."""
    ty = move_type(b, cand, m)
    if ty == "Ground" and m.name != "Thousand Arrows" and (
            (target.ability == "Levitate" and not mold(fainted, target)) or target.item == "Air Balloon"):
        return 0
    ine, se, nve = type_flags(b, ty, target.types, fainted.ability == "Scrappy")
    if ine:
        return 0
    if m.power and target.ability == "Wonder Guard" and not mold(fainted, target) and not se:
        return 0
    stab = (2 if fainted.ability == "Adaptability" else 1.5) if ty in fainted.types else 1
    eff = fs.effectiveness(b.st["chart"], ty, target.types)
    if m.cat == "Status":
        d = 2
    else:
        top = b.damage(fainted, target, m, ai_view=True)
        if not top:
            d = 0
        else:
            d = int(top / (stab * eff) + 0.5)
            if PINCH.get(fainted.ability) == ty:
                d = d * 3 // 2
    d %= 256
    if ty in fainted.types:
        d = d * 2 if fainted.ability == "Adaptability" else d * 15 // 10
    for x in dict.fromkeys(target.types):
        mx = fs.effectiveness(b.st["chart"], ty, [x])
        if d:
            d = max(1, d * int(mx * 10) // 10)
    if m.power and se and target.ability in ("Filter", "Solid Rock", "Prism Armor") \
            and not mold(fainted, target):
        d = d * 3 // 4
    if m.power and se and fainted.item == "Expert Belt":
        d = d * 120 // 100
    if m.power and nve and fainted.ability == "Tinted Lens":
        d *= 2
    return d % 256


def replacement(b, side, target, owner=None):
    """BattleAI_PostKOSwitchIn, as the engine runs it. Stage 1: the candidate
    whose two types (one type counted twice) score highest against the
    target (40 times the chart each, summed into a byte; a score of 0 is
    never taken), with a move of any kind super effective on it, in party
    order on ties; one without such a move is set aside and the next tried.
    Stage 2: the candidate whose moves score highest by _ko_score, ties by
    party order. The score is never reset (bug 16): a power-1 move or an
    empty slot compares the last figure again, before stage 2's first
    figure the last one stage 1 computed. With nothing above 0, the first
    living candidate. In a tag battle only the fainted Pokemon's own
    trainer's party can refill its slot."""
    def mine(m):
        return owner is None or getattr(m, "owner", None) == owner
    cands = [i for i, m in enumerate(side.mons)
             if i not in (side.active, side.active2) and m.alive() and mine(m)]
    if not cands and owner is None:
        cands = [i for i, m in enumerate(side.mons) if m.alive()]
    if not cands:
        return None

    def type_score(m):
        tys = m.types if len(m.types) == 2 else m.types * 2
        return sum(int(40 * fs.effectiveness(b.st["chart"], ty, target.types)) for ty in tys) % 256
    score = 0                      # the engine's one u8, carried from stage to stage
    set_aside = set()
    while True:
        best, picked = 0, None
        for i in cands:
            if i in set_aside:
                continue
            score = type_score(side.mons[i])
            if best < score:
                best, picked = score, i
        if picked is None:
            break
        if _any_se_moves(b, side.mons[picked], target):
            return picked
        set_aside.add(picked)
    fainted = side.mons[side.active]
    best, picked = 0, None
    for i in cands:
        moves = side.mons[i].moves
        for j in range(4):
            m = moves[j] if j < len(moves) else None
            if m is not None and m.power != 1:
                score = _ko_score(b, fainted, side.mons[i], target, m)
            if best < score:
                best, picked = score, i
    return picked if picked is not None else cands[0]

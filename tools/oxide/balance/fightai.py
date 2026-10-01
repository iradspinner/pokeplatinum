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
import functools
import json
import os
import re

from . import data, fightsim as fs

BASIC, EVAL, EXPERT, SETUP_FIRST, RISKY, EXTREMES, BATON, TAG, CHECK_HP, WEATHER, HARASS = range(11)

# Effects that have no damage figure for the AI (1.3 of the spec).
NO_CALC = {"HALVE_DEFENSE", "EXPLOSION", "RECOVER_DAMAGE_SLEEP", "CHARGE_TURN_HIGH_CRIT",
           "CHARGE_TURN_HIGH_CRIT_FLINCH", "RECHARGE_AFTER", "CHARGE_TURN_DEF_UP", "SOLAR_BEAM",
           "SKIP_CHARGE_TURN_IN_SUN", "SPIT_UP", "HIT_LAST_WHIFF_IF_HIT", "LOWER_OWN_ATK_AND_DEF",
           "DECREASE_POWER_WITH_LESS_USER_HP", "HIT_FIRST_IF_TARGET_ATTACKING", "RECOIL_HALF",
           "ONE_HIT_KO", "COUNTER", "MIRROR_COAT", "METAL_BURST", "INCREASE_POWER_WITH_LESS_HP"}
SETUP_FIRST_LIST = (set(fs.SELF_STAGES) | set(fs.FOE_STAGES) | {"SET_LIGHT_SCREEN", "SET_REFLECT",
                    "STATUS_CONFUSE", "STATUS_POISON", "STATUS_PARALYZE", "STATUS_BURN",
                    "SET_SUBSTITUTE", "STATUS_LEECH_SEED", "CURSE", "ATK_UP_2_STATUS_CONFUSION",
                    "SP_ATK_UP_CAUSE_CONFUSION", "STATUS_SLEEP_NEXT_TURN", "DOUBLE_SPEED_3_TURNS",
                    "CRIT_UP_2"}) - {"ATK_SPD_UP"}
RISKY_LIST = {"STATUS_SLEEP", "HALVE_DEFENSE", "EXPLOSION", "ONE_HIT_KO", "HIGH_CRITICAL",
              "STATUS_CONFUSE", "CALL_RANDOM_MOVE", "PSYWAVE", "COUNTER", "KO_MON_THAT_DEFEATED_USER",
              "ATK_UP_2_STATUS_CONFUSION", "INFATUATE", "RAISE_ALL_STATS_HIT",
              "MAX_ATK_LOSE_HALF_MAX_HP", "MIRROR_COAT", "HIT_LAST_WHIFF_IF_HIT", "DOUBLE_POWER_IF_HIT",
              "HIT_FIRST_IF_TARGET_ATTACKING", "DOUBLE_POWER_IF_MOVING_SECOND", "METAL_BURST"}
HARASS_LIST = {"STATUS_SLEEP", "ATK_DOWN", "DEF_DOWN", "ACC_DOWN", "EVA_DOWN", "ATK_DOWN_2",
               "DEF_DOWN_2", "SPEED_DOWN_2", "SP_DEF_DOWN_2", "STATUS_CONFUSE", "STATUS_POISON",
               "STATUS_PARALYZE", "STATUS_LEECH_SEED", "ENCORE", "SET_SPIKES",
               "ATK_UP_2_STATUS_CONFUSION", "INFATUATE", "TORMENT", "STATUS_BURN",
               "STATUS_SLEEP_NEXT_TURN", "REMOVE_HELD_ITEM", "TOXIC_SPIKES",
               "SP_ATK_UP_CAUSE_CONFUSION", "ATK_DEF_DOWN", "SP_ATK_DOWN_2_OPPOSITE_GENDER"}


def has_comparison(mv):
    return mv.damaging() and mv.effect not in NO_CALC and (mv.power > 1 or mv.effect == "LEVEL_DAMAGE_FLAT")


def figure(b, u, t, mv):
    """The AI's damage figure: the top roll, no critical hit, stages and
    screens applied; 0 for an immunity, None without a comparison."""
    if not has_comparison(mv):
        return None
    if mv.effect == "LEVEL_DAMAGE_FLAT":
        return u.level if fs.effectiveness(b.st["chart"], mv.type, t.types) else 0
    d = b.damage(u, t, mv, ai_view=True)
    return 0 if d is None else d


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
        return bool(getattr(b, "quick", {}).get(mon.key))
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
    return mv.type


def eff_of(b, mon, mv, t):
    return fs.effectiveness(b.st["chart"], move_type(b, mon, mv), t.types)


def score_moves(b, u, t, flags):
    """[score] for u's four slots."""
    figs = [figure(b, u, t, m) for m in u.moves]
    best = max((f for f in figs if f is not None), default=None)
    out = []
    for i, mv in enumerate(u.moves):
        s = 100
        invalid = u.pp.get(mv.name, 1) <= 0 or (u.taunt and mv.cat == "Status") or \
            (u.choice and mv.name != u.choice)
        if invalid:
            s = 0
        f = figs[i]
        for bit in range(11):
            if not flags >> bit & 1:
                continue
            s += flag_score(bit, b, u, t, mv, f, best)
            s = 0 if s < 0 else s
            if s > 127:
                s = 0                      # the signed byte wraps
        if u.pp.get(mv.name, 1) <= 0:
            s = -1                         # no PP: never picked
        out.append(s)
    return out


def flag_score(bit, b, u, t, mv, f, best):
    if bit == BASIC:
        return basic(b, u, t, mv, f)
    if bit == EVAL:
        return evaluate_attack(b, u, t, mv, f, best)
    if bit == EXPERT:
        return expert(b, u, t, mv, f)
    if bit == SETUP_FIRST:
        return 2 if b.turn == 0 and mv.effect in SETUP_FIRST_LIST and chance(b, 68.75) else 0
    if bit == RISKY:
        return 2 if mv.effect in RISKY_LIST and chance(b, 50) else 0
    if bit == EXTREMES:
        return 2 if f is None and chance(b, 60.9) else 0
    if bit == CHECK_HP:
        return check_hp(b, u, t, mv)
    if bit == WEATHER:
        w = fs.WEATHER_OF.get(mv.effect)
        return 5 if b.turn == 0 and w and b.weather != w else 0
    if bit == HARASS:
        return 2 if mv.effect in HARASS_LIST and chance(b, 50) else 0
    return 0


def basic(b, u, t, mv, f):
    e = mv.effect
    foe_side = b.p if t.side == "p" else b.b
    own_side = b.p if u.side == "p" else b.b
    if mv.damaging() and f == 0:
        return -10
    if mv.damaging() and eff(b, mv, t) == 0:
        return -10
    # Basic_CheckPowderImmunity (Oxide): a powder move at a Grass type or an
    # Overcoat holder scores -10; Rage Powder is aimed at its user.
    if mv.name in fs.POWDER and mv.name != "Rage Powder" and fs.powder_immune(t, mv):
        return -10
    if e in fs.STATUS_OF:
        # Status moves skip Basic's immunity check (basic.md, lines 62 to 68);
        # of the status handlers only Basic_CheckCannotParalyze asks the type
        # chart (Thunder Wave on Ground, Glare on Ghost). So Hypnosis keeps its
        # score against a Dark type.
        immune = e == "STATUS_PARALYZE" and eff(b, mv, t) == 0
        return -10 if not fs.can_status(b, t, fs.STATUS_OF[e]) or immune else 0
    if e == "STATUS_SLEEP_NEXT_TURN":
        return -10 if t.status or t.yawn or not fs.can_status(b, t, "slp") else 0
    if e in ("STATUS_CONFUSE", "ATK_UP_2_STATUS_CONFUSION", "SP_ATK_UP_CAUSE_CONFUSION"):
        return -5 if t.confused else (-10 if t.ability == "Own Tempo" else 0)
    if e == "STATUS_LEECH_SEED":
        return -10 if t.seeded or "Grass" in t.types else 0
    # Basic_CheckMeanLook and Basic_CheckAlreadyIngrained
    # (docs/oxide/battle-ai/basic.md): a second trap, a second rooting.
    if e == "PREVENT_ESCAPE":
        return -10 if t.trapped_by is not None else 0
    if e == "GROUND_TRAP_USER_CONTINUOUS_HEAL":
        return -10 if u.ingrained else 0
    if e in fs.SELF_STAGES:
        ch = fs.SELF_STAGES[e]
        stats = [k for k, v in ch.items() if v > 0]
        if stats and u.stages[stats[0]] >= 6:
            return -10
        if len(stats) > 1 and u.stages[stats[1]] >= 6:
            return -8
        if "spe" in stats and b.trick_room:
            return -10
        return 0
    if e in fs.FOE_STAGES:
        k = next(iter(fs.FOE_STAGES[e]))
        if t.stages[k] <= -6:
            return -10
        if t.ability in ("Clear Body", "White Smoke") or (k == "atk" and t.ability == "Hyper Cutter"):
            return -10
        return 0
    if e == "MAX_ATK_LOSE_HALF_MAX_HP":
        return -10 if u.frac() <= 50 or u.stages["atk"] >= 6 else 0
    if e == "CURSE" and "Ghost" not in u.types:
        return -10 if u.stages["atk"] >= 6 else (-8 if u.stages["def"] >= 6 else 0)
    if e == "CRIT_UP_2":
        return -10 if u.crit_stage else 0
    if e in ("SET_LIGHT_SCREEN", "SET_REFLECT"):
        key = "Light Screen" if e == "SET_LIGHT_SCREEN" else "Reflect"
        return -8 if own_side.screens[key] else 0
    if e == "PREVENT_STATUS":
        return -8 if own_side.safeguard else 0
    if e == "DOUBLE_SPEED_3_TURNS":
        return -10 if own_side.tailwind or b.trick_room else 0
    if e == "TRICK_ROOM":
        return -10 if not slower(b, u, t) else 0
    if e == "SET_SUBSTITUTE":
        return -8 if u.sub else (-10 if u.frac() <= 25 else 0)
    if e in fs.WEATHER_OF:
        return -8 if b.weather == fs.WEATHER_OF[e] else 0
    if e == "SET_SPIKES":
        return -10 if foe_side.hazards["spikes"] >= 3 or not foe_side.bench() else 0
    if e == "TOXIC_SPIKES":
        return -10 if foe_side.hazards["tspikes"] >= 2 or not foe_side.bench() else 0
    if e == "STEALTH_ROCK":
        return -10 if foe_side.hazards["rocks"] or not foe_side.bench() else 0
    if e in fs.HEAL_HALF or e == "HEAL_HALF_MORE_IN_SUN":
        return -8 if u.hp == u.maxhp else 0
    if e == "REST":
        return -8 if u.hp == u.maxhp else (-10 if u.ability in ("Insomnia", "Vital Spirit") else 0)
    if e == "RECOVER_DAMAGE_SLEEP":
        return -8 if t.status != "slp" else 0
    if e in fs.SELF_KO and mv.damaging():
        if eff(b, mv, t) == 0:
            return -10
        if not own_side.bench() and foe_side.bench():
            return -10
        return 0
    if e == "FORCE_SWITCH":
        return -10 if not foe_side.bench() else 0
    if e == "ALWAYS_FLINCH_FIRST_TURN_ONLY":
        return -10 if u.turns_in > 0 else 0
    if e == "HIT_IN_3_TURNS":
        return -12 if getattr(t, "future", 0) else 0
    if e == "RESET_STAT_CHANGES":
        worse = any(v < 0 for v in u.stages.values()) or any(v > 0 for v in t.stages.values())
        return 0 if worse else -10
    if e == "TAUNT":
        return -10 if t.taunt else 0
    if e == "ALL_FAINT_3_TURNS":
        return -10 if t.perish or u.perish else 0
    if e in ("PASS_STATS_AND_STATUS",):
        return -10 if not own_side.bench() else 0
    if e == "PROTECT":
        return 0
    return 0


def evaluate_attack(b, u, t, mv, f, best):
    if f is None:
        # Moves without a comparison skip straight to the last row.
        return 2 if eff(b, mv, t) >= 4 and chance(b, 68.75) else 0
    kills = f >= t.hp and not (t.hp == t.maxhp and t.ability == "Sturdy")
    if kills:
        if mv.effect == "PRIORITY_1" or (mv.pri > 0 and mv.effect not in (
                "ALWAYS_FLINCH_FIRST_TURN_ONLY", "HIT_FIRST_IF_TARGET_ATTACKING")):
            return 6
        if mv.effect == "HIT_IN_3_TURNS":
            return 4 if chance(b, 33.6) else 0
        return 4
    if best is not None and f < best:
        return -1
    s = 0
    if mv.effect in fs.SELF_KO or mv.effect in ("HIT_LAST_WHIFF_IF_HIT", "HIT_FIRST_IF_TARGET_ATTACKING"):
        s -= 2 if chance(b, 80.1) else 0
    if eff(b, mv, t) >= 4 and chance(b, 68.75):
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
MOLD_BREAKER = ("Mold Breaker", "Teravolt", "Turboblaze")


def script_eff(b, u, t, mv):
    """The number AICmd_IfMoveEffectivenessEquals compares for u's move into
    t: BattleSystem_ApplyTypeChart from a base of 40 (STAB, the chart type by
    type, Filter and Solid Rock, Expert Belt, Tinted Lens), with plain STAB's
    1.5 divided back out at the four exact values, and any immunity flag
    (the type chart, Levitate, an Air Balloon, Wonder Guard) reading 0. A
    neutral STAB hit (60), or one Filter or Tinted Lens scaled, matches none
    of the five, as in the game."""
    breaker = u.ability in MOLD_BREAKER
    ty = "Normal" if u.ability == "Normalize" else move_type(b, u, mv)
    if ty == "Ground" and mv.name != "Thousand Arrows" and (
            (t.ability == "Levitate" and not breaker) or t.item == "Air Balloon"):
        return IMMUNE
    d = 40
    if ty in u.types:
        d = d * 2 if u.ability == "Adaptability" else d * 15 // 10
    steps = 0
    for typ in dict.fromkeys(t.types):
        m = fs.effectiveness(b.st["chart"], ty, [typ])
        if m == 0 and typ == "Ghost" and ty in ("Normal", "Fighting") and u.ability == "Scrappy":
            continue
        if m == 0:
            return IMMUNE
        d = max(1, d * int(m * 10) // 10)
        steps += 1 if m > 1 else -1 if m < 1 else 0
    if t.ability == "Wonder Guard" and not breaker and steps <= 0:
        return IMMUNE
    if steps > 0 and t.ability in ("Filter", "Solid Rock", "Prism Armor") and not breaker:
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
    "Expert_WorrySeed": x_worry_seed, "Expert_SuckerPunch": x_sucker_punch,
    "Expert_HeartSwap": x_heart_swap, "Expert_AquaRing": x_aqua_ring, "Expert_MagnetRise": x_magnet_rise,
    "Expert_Defog": x_defog, "Expert_TrickRoom": x_trick_room, "Expert_Captivate": x_captivate,
    "Expert_RecoilMove": x_recoil_move, "Expert_Hex": x_doubled, "Expert_Venoshock": x_doubled,
    "Expert_Acrobatics": x_doubled, "Expert_BoltBeak": x_doubled,
    "Expert_RapidSpin": x_rapid_spin, "Expert_SpeedUpOnHit": x_speed_up_on_hit,
    "Expert_MortalSpin": x_mortal_spin}


@functools.lru_cache(maxsize=None)
def expert_routes():
    """{effect: label} from Expert_Main's jump table in script.s, first
    match winning, as the script runs it."""
    path = os.path.join(data.ROOT, "src", "battle", "trainer_ai", "script.s")
    with open(path, encoding="utf-8") as f:
        lines = f.read().splitlines()
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


CHECK_HIGH = {"HALVE_DEFENSE", "EXPLOSION", "RESTORE_HALF_HP", "HEAL_HALF_REMOVE_FLYING_TYPE",
              "HEAL_HALF_MORE_IN_SUN", "REST", "SURVIVE_WITH_1_HP", "KO_MON_THAT_DEFEATED_USER",
              "INCREASE_POWER_WITH_LESS_HP"}
CHECK_LOW = set(fs.SELF_STAGES) | {"SET_LIGHT_SCREEN", "SET_REFLECT", "CRIT_UP_2",
                                   "MAX_ATK_LOSE_HALF_MAX_HP", "PREVENT_STAT_REDUCTION"}
CHECK_FOE_LOW = set(fs.STATUS_OF) | set(fs.FOE_STAGES) | {"STATUS_CONFUSE", "STATUS_LEECH_SEED",
                                                          "STATUS_SLEEP_NEXT_TURN"}


def check_hp(b, u, t, mv):
    s = 0
    e = mv.effect
    hu, ht = u.frac(), t.frac()
    if (hu > 70 and e in CHECK_HIGH) or (hu <= 70 and e in CHECK_LOW):
        s -= 2 if chance(b, 80.5) else 0
    if ht <= 70 and e in CHECK_FOE_LOW:
        s -= 2 if chance(b, 80.5) else 0
    return s


def record_last_move(t):
    """TrainerAI_RecordLastMove, run before every decision: the target's
    previous move joins the moves the AI has seen it use (four at most;
    none after a turn it could not act)."""
    if t.last is not None and t.last not in t.shown and len(t.shown) < 4:
        t.shown.append(t.last)


def choose(b, u, t):
    """('move', Move) or ('switch', index) for the trainer's active Pokemon."""
    if u.lock:
        return "move", u.lock[0]
    if u.charging is not None:
        return "move", u.charging
    if u.recharge:
        return "move", u.moves[0]
    record_last_move(t)
    if u.choice:
        locked = next((m for m in u.moves if m.name == u.choice), None)
        if locked is not None and u.pp.get(locked.name, 1) > 0:
            return "move", locked
    # With no PP left in any move the engine substitutes Struggle
    # (battle_lib.c, the MOVE_STRUGGLE fallback in the turn order code).
    if all(u.pp.get(m.name, 1) <= 0 for m in u.moves):
        return "move", fs.move("Struggle")
    side = b.p if u.side == "p" else b.b
    sw = should_switch(b, side, u, t)
    if sw is not None:
        return "switch", sw
    scores = score_moves(b, u, t, b.ai_flags)
    top = max(scores)
    picks = [i for i, s in enumerate(scores) if s == top]
    return "move", u.moves[b.rng.choice(picks)]


def tag_strategy(b, u, t, mv, ally):
    """Tag Strategy toward a foe, lightly (section 4 of the spec): a spread
    move that hurts the ally is marked down, Explosion beside a living ally
    most of all, and a strongest or super-effective hit a little up."""
    s = 0
    if ally is not None:
        if mv.range == "ALL_ADJACENT" and mv.damaging():
            e = eff(b, mv, ally)
            if e == 0 or (mv.type == "Ground" and (ally.ability == "Levitate" or "Flying" in ally.types)):
                s += 2
            elif e >= 2:
                s -= 10
            else:
                s -= 3
        if mv.effect in fs.SELF_KO and mv.damaging():
            s += 0 if "Ghost" in ally.types else (-3 if set(ally.types) & {"Rock", "Steel"} else -10)
    f = figure(b, u, t, mv)
    if f:
        mine = [figure(b, u, t, m) or 0 for m in u.moves]
        theirs = [figure(b, ally, t, m) or 0 for m in ally.moves] if ally else []
        if f >= max(mine + theirs):
            s += 1 if chance(b, 80.5 if mv.pri > 0 else 50) else 0
        elif eff(b, mv, t) >= 2 and chance(b, 60.9):
            s += 1
    return s


def choose_doubles(b, u):
    """('move', Move, target): each foe scored as the target in turn, the
    best move for each kept, and the target whose best scores highest."""
    if u.lock:
        return "move", u.lock[0], None
    if u.charging is not None:
        return "move", u.charging, None
    if u.recharge:
        return "move", u.moves[0], None
    foes = fs.foes_of(b, u)
    ally = fs.ally_of(b, u)
    best = []
    for t in foes:
        record_last_move(t)
        scores = score_moves(b, u, t, b.ai_flags)
        for i, mv in enumerate(u.moves):
            s = scores[i] + (tag_strategy(b, u, t, mv, ally) if scores[i] > 0 else 0)
            best.append((s, b.rng.random(), mv, t))
    if not best:
        return "move", u.moves[0], None
    s, _r, mv, t = max(best, key=lambda x: (x[0], x[1]))
    return "move", mv, t


def _se_moves(b, mon, t):
    return [m for m in mon.moves if m.damaging() and eff_of(b, mon, m, t) >= 2]


# The abilities that take a type's moves, as AI_AbilityAbsorbsType has them
# (Oxide adds Storm Drain, Dry Skin, Lightning Rod, Motor Drive, Sap Sipper).
ABSORBS = {"Fire": {"Flash Fire"}, "Water": {"Water Absorb", "Storm Drain", "Dry Skin"},
           "Electric": {"Volt Absorb", "Lightning Rod", "Motor Drive"}, "Grass": {"Sap Sipper"}}


def _any_se_moves(b, mon, t):
    """Every move, status moves too, whose type hits t super-effectively:
    BattleSystem_CalcEffectiveness, which the party checks use, sets the flag
    whatever the move's power."""
    return [m for m in mon.moves if eff_of(b, mon, m, t) >= 2]


def _hit_type(b, mv):
    """The type the last move that hit had (moveHitType): Weather Ball's
    comes from the weather."""
    if mv.name == "Weather Ball" and b.weather:
        return {"Sun": "Fire", "Rain": "Water", "Hail": "Ice", "Sand": "Rock"}.get(b.weather, mv.type)
    return mv.type


def should_switch(b, side, u, t):
    """TrainerAI_ShouldSwitch (trainer_ai.c), rule by rule; in singles each
    party check reads the one foe as both defenders, so it rolls twice."""
    if not fs.can_switch(u):
        return None          # trapped by Block or Mean Look, or rooted by Ingrain
    bench = [i for i, m in enumerate(side.mons) if i != side.active and m.alive()]
    if not bench or u.bound:
        return None
    # AI_PerishSongKO
    if u.perish == 1:
        return replacement(b, side, t)
    # AI_CannotDamageWonderGuard: no super-effective attack on a Wonder Guard foe.
    if t.ability == "Wonder Guard" and not _se_moves(b, u, t):
        for i in bench:
            for m in _any_se_moves(b, side.mons[i], t):
                if chance(b, 66.7):
                    return i
    # AI_OnlyIneffectiveMoves: two or more attacks, every one immune.
    dmg = [m for m in u.moves if m.damaging()]
    if len(dmg) >= 2 and all(eff_of(b, u, m, t) == 0 for m in dmg):
        for i in bench:
            for m in side.mons[i].moves:
                if m.damaging() and eff_of(b, side.mons[i], m, t) >= 2:
                    for _ in range(2):
                        if chance(b, 66.7):
                            return i
        for i in bench:
            for m in side.mons[i].moves:
                if m.damaging() and eff_of(b, side.mons[i], m, t) == 1:
                    for _ in range(2):
                        if chance(b, 50):
                            return i
    hit = u.last_hit_by
    # AI_HasAbsorbAbilityInParty: a super-effective attack of its own keeps it
    # in two times in three; otherwise a bench member that takes the type of
    # the attack that hit it comes in, one time in two.
    if not (_se_moves(b, u, t) and chance(b, 66.7)) and hit is not None and hit.damaging():
        htype = _hit_type(b, hit)
        if u.ability not in ABSORBS.get(htype, ()):
            for i in bench:
                if side.mons[i].ability in ABSORBS.get(htype, ()) and chance(b, 50):
                    return i
    # AI_IsAsleepWithNaturalCure, at half HP or more.
    if u.status == "slp" and u.ability == "Natural Cure" and u.hp >= u.maxhp // 2:
        if hit is None and chance(b, 50):
            return replacement(b, side, t)
        if (hit is None or not hit.damaging()) and chance(b, 50):
            return replacement(b, side, t)
        if hit is not None and hit.damaging():
            for want in (0, "res"):
                for i in bench:
                    m = side.mons[i]
                    e = fs.effectiveness(b.st["chart"], _hit_type(b, hit), m.types)
                    if (e == 0 if want == 0 else 0 < e < 1) and _any_se_moves(b, m, t):
                        return i
        if chance(b, 50):
            return replacement(b, side, t)
    # AI_HasSuperEffectiveMove: each super-effective attack keeps it in nine
    # times in ten; four or more boosts keep it in.
    for m in _se_moves(b, u, t):
        if chance(b, 90):
            return None
    if sum(v for k, v in u.stages.items() if v > 0 and k != "acc") >= 4:
        return None
    # AI_HasPartyMemberWithSuperEffectiveMove: a bench member immune to (one
    # in two per move) or resisting (one in three per move) the attack that
    # hit it, with a super-effective move of any kind at the foe.
    if hit is not None and hit.damaging():
        for want, p in ((0, 50), ("res", 33.3)):
            for i in bench:
                m = side.mons[i]
                e = fs.effectiveness(b.st["chart"], _hit_type(b, hit), m.types)
                if e == 0 if want == 0 else 0 < e < 1:
                    for _mv in _any_se_moves(b, m, t):
                        if chance(b, p):
                            return i
    return None


def replacement(b, side, target, owner=None):
    """The post-faint pick: by type match-up first (the candidate's types
    against the target's), taken only with a super-effective move; else by
    the damage its moves would do. In a tag battle only the fainted
    Pokemon's own trainer's party can refill its slot."""
    def mine(m):
        return owner is None or getattr(m, "owner", None) == owner
    cands = [i for i, m in enumerate(side.mons)
             if i not in (side.active, side.active2) and m.alive() and mine(m)]
    if not cands and owner is None:
        cands = [i for i, m in enumerate(side.mons) if m.alive()]
    if not cands:
        return None
    chart = b.st["chart"]

    def type_score(m):
        tys = m.types if len(m.types) == 2 else m.types * 2
        total = 0
        for ty in tys:
            total += int(40 * fs.effectiveness(chart, ty, target.types))
        return total % 256
    for i in sorted(cands, key=lambda i: (-type_score(side.mons[i]), i)):
        if _se_moves(b, side.mons[i], target) or any(
                m.cat == "Status" and eff(b, m, target) >= 2 for m in side.mons[i].moves):
            return i
    # Stage 2 (BattleAI_PostKOSwitchIn, battle_lib.c): each candidate's
    # moves are costed as if the Pokemon that just fainted used them, at
    # its stats, types and ability, by the top roll without a critical hit;
    # a move listed at power 1 (variable power: Low Kick, Magnitude) is
    # skipped, an immune target scores 0, and the score is a u8, so a figure
    # past 255 wraps. The highest wins, ties by party order.
    fainted = side.mons[side.active]
    row = b.row(fainted, target)
    best, best_score = cands[0], 0
    for i in sorted(cands):
        for m in side.mons[i].moves:
            if not m.damaging() or m.power == 1:
                continue
            got = (row or {}).get("moves", {}).get(m.name) if row else None
            score = (got["rolls"][-1] if got and got.get("rolls") else 0)
            if eff(b, m, target) == 0:
                score = 0
            score %= 256
            if score > best_score:
                best, best_score = i, score
    return best

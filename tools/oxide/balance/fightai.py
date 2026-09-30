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

from . import data, fightsim as fs

BASIC, EVAL, EXPERT, SETUP_FIRST, RISKY, EXTREMES, BATON, TAG, CHECK_HP, WEATHER, HARASS = range(11)

# Effects that have no damage figure for the AI (1.3 of the spec).
NO_CALC = {"HALVE_DEFENSE", "EXPLOSION", "RECOVER_DAMAGE_SLEEP", "CHARGE_TURN_HIGH_CRIT",
           "CHARGE_TURN_HIGH_CRIT_FLINCH", "RECHARGE_AFTER", "CHARGE_TURN_DEF_UP", "SOLAR_BEAM",
           "SKIP_CHARGE_TURN_IN_SUN", "SPIT_UP", "HIT_LAST_WHIFF_IF_HIT", "LOWER_OWN_ATK_AND_DEF",
           "DECREASE_POWER_WITH_LESS_USER_HP", "HIT_FIRST_IF_TARGET_ATTACKING", "RECOIL_HALF",
           "ONE_HIT_KO", "COUNTER", "MIRROR_COAT", "METAL_BURST", "INCREASE_POWER_WITH_LESS_HP"}
ATK_UP = {"ATK_UP", "ATK_UP_2", "HONE_CLAWS", "WORK_UP", "GROWTH"}
SPA_UP = {"SP_ATK_UP", "SP_ATK_UP_2"}
# Defense Curl (DEF_UP_DOUBLE_ROLLOUT_POWER) has no Expert routine in the game:
# StatusDefenseUp takes DEF_UP, DEF_UP_2 and ATK_DEF_UP (expert-1.md, dispatch).
DEF_UP = {"DEF_UP", "DEF_UP_2", "ATK_DEF_UP", "COIL"}
SPD_UP = {"SP_ATK_SP_DEF_UP", "SP_DEF_UP_2", "DEF_SPD_UP", "STOCKPILE"}
DANCE = {"ATK_SPD_UP", "QUIVER_DANCE", "SHIFT_GEAR", "SHELL_SMASH"}
SLEEP = {"STATUS_SLEEP"}
PARA = {"STATUS_PARALYZE"}
TOXIC_SEED = {"STATUS_BADLY_POISON", "STATUS_LEECH_SEED"}
CONFUSE = {"STATUS_CONFUSE"}
HEAL = {"RESTORE_HALF_HP", "HEAL_HALF_REMOVE_FLYING_TYPE", "SWALLOW"}
PROTECTS = {"PROTECT"}
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


# The Speed-lowering attacks SpeedDownOnHit names by move id (expert-1.md).
SPEED_DOWN_NAMED = {"Icy Wind", "Rock Tomb", "Mud Shot", "Bulldoze", "Electroweb", "Low Sweep",
                    "Glaciate", "Drum Beating", "Pounce"}


def slower(b, u, t):
    su, st_ = b.speed(u), b.speed(t)
    if b.trick_room:
        return su > st_
    return su < st_


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


def _last_class(t):
    lm = t.last
    return None if lm is None else ("status" if lm.cat == "Status" else lm.cat)


def expert(b, u, t, mv, f):
    e = mv.effect
    hu, ht = u.frac(), t.frac()
    slow = slower(b, u, t)
    res = eff(b, mv, t) < 1 and mv.damaging()
    s = 0
    if e in SLEEP:
        if any(m.effect in ("RECOVER_DAMAGE_SLEEP", "STATUS_NIGHTMARE") for m in u.moves) and chance(b, 50):
            s += 1
    elif e == "RECOVER_DAMAGE_SLEEP":
        if res:
            return -1
        if t.status == "slp" and chance(b, 80.1):
            s += 3
    elif e == "STATUS_POISON":
        if hu < 50 or ht <= 50:
            s -= 1
    elif e in TOXIC_SEED:
        has_power = any(m.power > 0 for m in u.moves)
        if has_power and hu <= 50 and chance(b, 80.5):
            s -= 3
        if has_power and ht <= 50 and chance(b, 80.5):
            s -= 3
        if any(m.effect == "PROTECT" for m in u.moves) and chance(b, 76.6):
            s += 2
    elif e in PARA:
        if slow and chance(b, 92.2):
            s += 3
        elif not slow and hu <= 70:
            s -= 1
    elif e in ("LOWER_SPEED_HIT", "SPEED_DOWN", "SPEED_DOWN_2"):
        # SpeedDownOnHit (2338 to 2351) and StatusSpeedDown (2353 to 2366),
        # expert-1.md: an attack the foe resists or is immune to scores
        # nothing; only the attacks named by move id (Icy Wind, Rock Tomb,
        # Mud Shot, and Oxide's six since 2026-09-27) and the Speed-lowering
        # status moves go on to Speed Down, where a user that is not slower
        # (a tie counts as not slower) takes -3 and a slower one +2 at 72.7%.
        if e == "LOWER_SPEED_HIT" and (res or eff(b, mv, t) == 0 or mv.name not in SPEED_DOWN_NAMED):
            return s
        if not slow:
            s -= 3
        elif chance(b, 72.7):
            s += 2
    elif e == "HIT_BEFORE_SWITCH":
        # Pursuit (3706 to 3735): +1 at 50% on the user's first turn in,
        # otherwise +1 at 50% against a Ghost or Psychic foe; then +1 at 50%
        # if the foe has shown U-turn.
        if u.turns_in == 0:
            if chance(b, 50):
                s += 1
        elif ("Ghost" in t.types or "Psychic" in t.types) and chance(b, 50):
            s += 1
        if any(m.name == "U-turn" for m in getattr(t, "shown", ())) and chance(b, 50):
            s += 1
    elif e in CONFUSE or e in ("ATK_UP_2_STATUS_CONFUSION", "SP_ATK_UP_CAUSE_CONFUSION"):
        if e != "STATUS_CONFUSE" and chance(b, 50):
            s += 1
        if ht > 70:
            return s
        if chance(b, 50):
            s -= 1
        if ht <= 50:
            s -= 1
        if ht <= 30:
            s -= 1
    elif e in ATK_UP or e in SPA_UP:
        k = "atk" if e in ATK_UP else "spa"
        if u.stages[k] >= 3:
            if chance(b, 60.9):
                s -= 1
        elif hu == 100 and chance(b, 50):
            s += 2
        if hu > 70:
            return s
        if hu < 40:
            s -= 2
        elif chance(b, 84.4 if k == "atk" else 72.7):
            s -= 2
    elif e in DEF_UP or e in SPD_UP:
        k, cls = ("def", "Physical") if e in DEF_UP else ("spd", "Special")
        if u.stages[k] >= 3:
            if chance(b, 60.9):
                s -= 1
        elif hu == 100 and chance(b, 50):
            s += 2
        if hu >= 70 and chance(b, 78.1):
            return s
        last = _last_class(t)
        if hu < 40:
            s -= 2
        elif last in (None, "status") and chance(b, 76.6):
            s -= 2
        elif last and last != cls and last != "status":
            s -= 2
        elif last == cls and chance(b, 58.6):
            s -= 2
    elif e == "SPEED_UP_2":
        if not slow:
            s -= 3
        elif chance(b, 72.7):
            s += 3
    elif e in DANCE:
        if slow and chance(b, 50):
            return 1
        if hu <= 50 and chance(b, 72.7):
            s -= 1
    elif e in ("EVA_UP", "EVA_UP_2_MINIMIZE"):
        if hu >= 90 and chance(b, 60.9):
            s += 3
        if u.stages["eva"] >= 3 and chance(b, 50):
            s -= 1
        if t.status == "tox" and chance(b, 80.5):
            s += 3
        if t.seeded and chance(b, 72.7):
            s += 3
        if hu <= 70 and u.stages["eva"] != 0:
            s -= 2 if (hu < 40 or ht < 40) else (2 if chance(b, 72.7) else 0)
    elif e == "MAX_ATK_LOSE_HALF_MAX_HP":
        if hu < 90:
            s -= 2
    elif e in HEAL or e == "HEAL_HALF_MORE_IN_SUN":
        if e == "HEAL_HALF_MORE_IN_SUN" and b.weather in ("Rain", "Sand", "Hail"):
            s -= 2
        if hu == 100:
            return s - 3
        if not slow:
            return s - 8
        if hu >= 70 and chance(b, 88.3):
            return s - 3
        if chance(b, 92.2):
            s += 2
    elif e == "REST":
        if not slow:
            if hu == 100:
                return -8
            if hu > 50:
                return -3
            if hu >= 40 and chance(b, 72.7):
                return -3
        else:
            if hu > 70:
                return -3
            if hu >= 60 and chance(b, 80.5):
                return -3
        if chance(b, 96.1):
            s += 3
    elif e in ("SET_LIGHT_SCREEN", "SET_REFLECT"):
        cls = "Special" if e == "SET_LIGHT_SCREEN" else "Physical"
        if hu < 50:
            return -2
        if hu >= 90 and chance(b, 50):
            s += 1
        last = _last_class(t)
        if (last == cls or (cls == "Physical" and last is None)) and chance(b, 75):
            s += 1
    elif e in ("WEATHER_RAIN", "WEATHER_SUN"):
        if hu < 40:
            return -1
        if b.weather and b.weather != fs.WEATHER_OF[e]:
            return 1
    elif e == "WEATHER_HAIL":
        if hu < 40:
            return -1
        if b.weather in ("Sun", "Rain", "Sand"):
            s += 1
    elif e == "TRICK_ROOM":
        if slow and chance(b, 75):
            s += 3
        elif not slow:
            s -= 1
    elif e == "DOUBLE_SPEED_3_TURNS":
        if chance(b, 25):
            return 0
        if not slow and b.speed(u) != b.speed(t):
            s -= 1
        if hu <= 30:
            s -= 1
        elif hu > 75:
            s += 1
        elif chance(b, 75):
            s += 1
    elif e == "PROTECT":
        if u.protect_run > 1:
            return -2
        if u.status == "tox" or u.seeded or u.cursed or u.yawn:
            return -2
        if t.status == "tox" or t.seeded or t.cursed or t.yawn:
            s += 2
        elif chance(b, 33.2):
            s += 2
        if chance(b, 50):
            s -= 1
        if u.protect_run == 1:
            s -= 1
            if chance(b, 50):
                s -= 1
    elif e == "SET_SUBSTITUTE":
        rolls = 1 if 71 <= hu <= 90 else 2 if 51 <= hu <= 70 else 3 if hu <= 50 else 0
        for _ in range(rolls):
            if chance(b, 60.9):
                s -= 1
        lm = t.last
        if not slow and lm is not None and lm.effect in fs.STATUS_OF and not t.status and chance(b, 60.9):
            s += 1
    elif e == "SET_SPIKES":
        if not chance(b, 50):
            return 0
        s += 1
        if any(m.effect == "FORCE_SWITCH" for m in u.moves) and chance(b, 75):
            s += 1
    elif e in ("TOXIC_SPIKES", "STEALTH_ROCK"):
        if chance(b, 50):
            return 0
        s += 1
        if any(m.effect == "FORCE_SWITCH" for m in u.moves) and chance(b, 75):
            s += 1
    elif e == "FORCE_SWITCH":
        foe_side = b.p if t.side == "p" else b.b
        if t.turns_in > 3:
            s += 2 if chance(b, 75) else 0
            s += 2 if chance(b, 50) else 0
        elif any(foe_side.hazards.values()) or any(t.stages[k] >= 3 for k in ("atk", "def", "spa", "spd", "eva")):
            s += 2 if chance(b, 50) else 0
        else:
            s -= 3
    elif e in fs.SELF_KO:
        if t.stages["eva"] >= 1:
            s -= 1
        if hu >= 80 and not slow:
            if chance(b, 80.5):
                return s - 3
        elif hu > 50:
            s -= 1 if chance(b, 80.5) else 0
        else:
            s += 1 if chance(b, 50) else 0
            if hu <= 30 and chance(b, 80.5):
                s += 1
    elif e == "RECOVER_HALF_DAMAGE_DEALT":
        if res and chance(b, 80.5):
            s -= 3
    elif e.startswith("HIGH_CRITICAL"):
        if res:
            return 0
        if eff(b, mv, t) >= 2:
            s += 1 if chance(b, 50) else 0
        elif chance(b, 25):
            s += 1
    elif e == "RECHARGE_AFTER":
        if res:
            return -1
        if (slow and hu >= 60) or (not slow and hu > 40):
            s -= 1
    elif e in ("THUNDER", "BLIZZARD"):
        if res or (e == "THUNDER" and b.weather == "Sun"):
            if chance(b, 80.5):
                s -= 3
        elif (e == "THUNDER" and b.weather == "Rain") or (e == "BLIZZARD" and b.weather == "Hail"):
            s += 1
    elif e == "ALWAYS_FLINCH_FIRST_TURN_ONLY":
        s += 2
    elif e == "DOUBLE_POWER_WHEN_STATUSED":
        if u.status in ("psn", "tox", "brn", "par"):
            s += 1
    elif e in ("LOWER_OWN_ATK_AND_DEF", "USER_SP_ATK_DOWN_2", "DEF_SPD_DOWN_HIT"):
        if res:
            return -1
        if e == "LOWER_OWN_ATK_AND_DEF" and u.stages["atk"] <= -1:
            s -= 1
        if (slow and hu <= 80 and e != "LOWER_OWN_ATK_AND_DEF") or (slow and hu >= 60 and e == "LOWER_OWN_ATK_AND_DEF"):
            s -= 1
        elif not slow and hu <= 60:
            s -= 1
    elif e in fs.RECOIL:
        if res and chance(b, 80.5):
            s -= 3
        elif u.ability in ("Rock Head", "Magic Guard"):
            s += 1
    elif e == "HIT_FIRST_IF_TARGET_ATTACKING":
        if res:
            return -1
        if chance(b, 75):
            s += 1
    elif e == "DOUBLE_POWER_IF_MOVING_SECOND":
        if res:
            return -1
        if slow and hu >= 30 and chance(b, 75):
            s += 1
    elif e in fs.FOE_STAGES:
        k = next(iter(fs.FOE_STAGES[e]))
        if k in ("atk", "spa"):
            if t.stages[k] != 0:
                s -= 1
                if hu <= 90:
                    s -= 1
                if t.stages[k] <= -3 and chance(b, 80.5):
                    s -= 2
            if ht <= 70:
                s -= 2
        elif k == "spe":
            if not slow:
                s -= 3
            elif chance(b, 72.7):
                s += 2
        else:
            if hu < 70 and chance(b, 80.5):
                s -= 2
            elif t.stages[k] <= -3 and chance(b, 80.5):
                s -= 2
            if ht <= 70:
                s -= 2
    elif e == "SWITCH_HIT":
        own = b.p if u.side == "p" else b.b
        if res:
            return -1
        if not own.bench():
            return 0
        if ht > 70:
            s += (1 if chance(b, 75) else 0) + (1 if chance(b, 50) else 0)
        elif ht > 30:
            s += 1 if chance(b, 50) else 0
        if not slow:
            s += 1
    return s


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


def choose(b, u, t):
    """('move', Move) or ('switch', index) for the trainer's active Pokemon."""
    if u.lock:
        return "move", u.lock[0]
    if u.charging is not None:
        return "move", u.charging
    if u.recharge:
        return "move", u.moves[0]
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

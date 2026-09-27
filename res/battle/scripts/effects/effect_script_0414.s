#include "macros/btlcmd.inc"


// Oxide: Sky Drop, on the model of Fly. hg-engine leaves it a TODO; this is
// Generation 6's rule. The first turn lifts the target into the air with the
// user (TrySkyDrop, subscript_sky_drop_lift); the target can then do nothing
// and cannot switch out (Battler_SkyDropHeld). The second turn drops it:
// both land, and the drop hits, except a Flying type, which it does not
// affect. If the user stops in between, the target lands
// (Battler_ReleaseSkyDropTargets), and a target no longer held on the second
// turn makes the move fail.
_000:
    CompareMonDataToValue OPCODE_FLAG_SET, BTLSCR_ATTACKER, BATTLEMON_VOLATILE_STATUS, VOLATILE_CONDITION_MOVE_LOCKED, _drop
    TrySkyDrop _end
    UpdateMonData OPCODE_FLAG_ON, BTLSCR_ATTACKER, BATTLEMON_MOVE_EFFECTS_MASK, MOVE_EFFECT_AIRBORNE
    // {0} took {1} into the sky!
    BufferMessage BattleStrings_Text_PokemonTookPokemonIntoTheSky_AllyAlly, TAG_NICKNAME_NICKNAME, BTLSCR_ATTACKER, BTLSCR_DEFENDER
    UpdateVar OPCODE_SET, BTLVAR_SIDE_EFFECT_FLAGS_DIRECT, MOVE_SIDE_EFFECT_TO_ATTACKER|MOVE_SUBSCRIPT_PTR_SKY_DROP_LIFT
    UpdateVar OPCODE_FLAG_ON, BTLVAR_BATTLE_CTX_STATUS, SYSCTL_SKIP_ATTACK_MESSAGE|SYSCTL_CHECK_LOOP_ONLY_ONCE|SYSCTL_FIRST_OF_MULTI_TURN
    End 

_drop:
    CompareMonDataToValue OPCODE_FLAG_NOT, BTLSCR_DEFENDER, BATTLEMON_OXIDE_FLAGS, OXIDE_MON_FLAG_SKY_DROP_HELD, _lost
    UpdateMonData OPCODE_FLAG_OFF, BTLSCR_DEFENDER, BATTLEMON_OXIDE_FLAGS, OXIDE_MON_FLAG_SKY_DROP_HELD|OXIDE_MON_SKY_DROP_HOLDER
    UpdateMonData OPCODE_FLAG_OFF, BTLSCR_DEFENDER, BATTLEMON_MOVE_EFFECTS_MASK, MOVE_EFFECT_AIRBORNE
    UpdateMonData OPCODE_FLAG_OFF, BTLSCR_DEFENDER, BATTLEMON_MOVE_EFFECTS_TEMP, MOVE_EFFECT_AIRBORNE
    ToggleVanish BTLSCR_DEFENDER, FALSE
    Wait 
    CompareMonDataToValue OPCODE_EQU, BTLSCR_DEFENDER, BATTLEMON_TYPE_1, TYPE_FLYING, _flying
    CompareMonDataToValue OPCODE_EQU, BTLSCR_DEFENDER, BATTLEMON_TYPE_2, TYPE_FLYING, _flying
    CalcCrit 
    CalcDamage 
    GoTo _land

_flying:
    UpdateVar OPCODE_FLAG_ON, BTLVAR_MOVE_STATUS_FLAGS, MOVE_STATUS_INEFFECTIVE
    GoTo _land

_lost:
    UpdateVar OPCODE_FLAG_ON, BTLVAR_MOVE_STATUS_FLAGS, MOVE_STATUS_FAILED

_land:
    UpdateMonData OPCODE_FLAG_OFF, BTLSCR_ATTACKER, BATTLEMON_MOVE_EFFECTS_MASK, MOVE_EFFECT_SEMI_INVULNERABLE
    Call BATTLE_SUBSCRIPT_CHARGE_MOVE_CLEANUP

_end:
    End 

#include "macros/btlcmd.inc"


// Oxide: Strength Sap restores the user's HP by the target's Attack, stat
// stage included, then lowers that Attack a stage. It fails when the Attack
// is already at its lowest. Big Root adds to the heal and Liquid Ooze turns
// it into damage, as for the draining moves.
_000:
    CompareMonDataToValue OPCODE_EQU, BTLSCR_DEFENDER, BATTLEMON_ATTACK_STAGE, 0, _fail
    Call BATTLE_SUBSCRIPT_ATTACK_MESSAGE_AND_ANIMATION
    CalcStrengthSap
    UpdateVar OPCODE_SET, BTLVAR_SIDE_EFFECT_PARAM, MOVE_SUBSCRIPT_PTR_ATTACK_DOWN_1_STAGE
    Call BATTLE_SUBSCRIPT_UPDATE_STAT_STAGE
    CheckItemHoldEffect CHECK_NOT_HAVE, BTLSCR_ATTACKER, HOLD_EFFECT_LEECH_BOOST, _heal
    GetItemEffectParam BTLSCR_ATTACKER, BTLVAR_CALC_TEMP
    UpdateVar OPCODE_ADD, BTLVAR_CALC_TEMP, 100
    UpdateVarFromVar OPCODE_MUL, BTLVAR_HP_CALC_TEMP, BTLVAR_CALC_TEMP
    UpdateVar OPCODE_DIV, BTLVAR_HP_CALC_TEMP, 100

_heal:
    UpdateVarFromVar OPCODE_SET, BTLVAR_MSG_BATTLER_TEMP, BTLVAR_ATTACKER
    CheckAbility CHECK_HAVE, BTLSCR_DEFENDER, ABILITY_LIQUID_OOZE, _ooze
    Call BATTLE_SUBSCRIPT_RECOVER_HP
    End

_ooze:
    CheckAbility CHECK_HAVE, BTLSCR_ATTACKER, ABILITY_MAGIC_GUARD, _end
    UpdateVar OPCODE_MUL, BTLVAR_HP_CALC_TEMP, -1
    UpdateVar OPCODE_FLAG_ON, BTLVAR_BATTLE_CTX_STATUS, SYSCTL_SKIP_SPRITE_BLINK
    Call BATTLE_SUBSCRIPT_UPDATE_HP
    // It sucked up the liquid ooze!
    PrintMessage BattleStrings_Text_ItSuckedUpTheLiquidOoze, TAG_NONE
    Wait
    WaitButtonABTime 30

_end:
    End

_fail:
    UpdateVar OPCODE_FLAG_ON, BTLVAR_MOVE_STATUS_FLAGS, MOVE_STATUS_FAILED
    End

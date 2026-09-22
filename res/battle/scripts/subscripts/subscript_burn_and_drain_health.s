#include "macros/btlcmd.inc"


Start:
    CompareVarToValue OPCODE_EQU, BTLVAR_DEFENDER, BATTLER_NONE, NoBurn
    CompareMonDataToValue OPCODE_EQU, BTLSCR_DEFENDER, BATTLEMON_CUR_HP, 0, NoBurn
    UpdateVarFromVar OPCODE_SET, BTLVAR_SIDE_EFFECT_MON, BTLVAR_DEFENDER
    CheckEffectActivation NoBurn
    Call BATTLE_SUBSCRIPT_BURN
NoBurn:
    Call BATTLE_SUBSCRIPT_DRAIN_HALF_DAMAGE_DEALT
    End

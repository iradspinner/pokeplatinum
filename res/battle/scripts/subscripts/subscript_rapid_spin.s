#include "macros/btlcmd.inc"


_000:
    RapidSpin 
    // Oxide: Rapid Spin also raises its user's Speed by one stage
    // (Generation 8; hg-engine gives it the effect as a secondary one).
    CompareMonDataToValue OPCODE_EQU, BTLSCR_ATTACKER, BATTLEMON_CUR_HP, 0, _end
    UpdateVarFromVar OPCODE_SET, BTLVAR_SIDE_EFFECT_MON, BTLVAR_ATTACKER
    UpdateVar OPCODE_SET, BTLVAR_SIDE_EFFECT_PARAM, MOVE_SUBSCRIPT_PTR_SPEED_UP_1_STAGE
    Call BATTLE_SUBSCRIPT_UPDATE_STAT_STAGE

_end:
    End 

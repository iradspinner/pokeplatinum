#include "macros/btlcmd.inc"


_000:
    CompareVarToValue OPCODE_FLAG_SET, BTLVAR_BATTLE_CTX_STATUS, SYSCTL_MULTI_HIT_SKIP_MESSAGE, _011
    // Hit {0} time(s)!
    PrintMessage BattleStrings_Text_HitXTimes, TAG_NUMBER, BTLSCR_MSG_TEMP
    Wait 
    WaitButtonABTime 30

_011:
    // Oxide: once Scale Shot's last hit is in, its user's Defense falls and
    // its Speed rises, one stage each, as hg-engine does after the move
    // (ServerDoPostMoveEffects). A miss never gets here, so it changes
    // nothing, and a user knocked out by the hits is left alone. Each stat
    // is tried on its own, so a Defense already at -6 still lets the Speed
    // rise; hg-engine skips both when either is at its limit.
    CompareVarToValue OPCODE_NEQ, BTLVAR_CURRENT_MOVE, MOVE_SCALE_SHOT, _end
    CompareMonDataToValue OPCODE_EQU, BTLSCR_ATTACKER, BATTLEMON_CUR_HP, 0, _end
    UpdateVarFromVar OPCODE_SET, BTLVAR_SIDE_EFFECT_MON, BTLVAR_ATTACKER
    UpdateVar OPCODE_SET, BTLVAR_SIDE_EFFECT_TYPE, SIDE_EFFECT_TYPE_INDIRECT
    UpdateVar OPCODE_FLAG_ON, BTLVAR_BATTLE_CTX_STATUS_2, SYSCTL_STAT_STAGE_CHANGE_SHOWN
    UpdateVar OPCODE_SET, BTLVAR_SIDE_EFFECT_PARAM, MOVE_SUBSCRIPT_PTR_DEFENSE_DOWN_1_STAGE
    Call BATTLE_SUBSCRIPT_UPDATE_STAT_STAGE
    UpdateVar OPCODE_SET, BTLVAR_SIDE_EFFECT_PARAM, MOVE_SUBSCRIPT_PTR_SPEED_UP_1_STAGE
    Call BATTLE_SUBSCRIPT_UPDATE_STAT_STAGE
    UpdateVar OPCODE_FLAG_OFF, BTLVAR_BATTLE_CTX_STATUS_2, SYSCTL_UPDATE_STAT_STAGES
    UpdateVar OPCODE_FLAG_OFF, BTLVAR_BATTLE_CTX_STATUS_2, SYSCTL_STAT_STAGE_CHANGE_SHOWN

_end:
    End

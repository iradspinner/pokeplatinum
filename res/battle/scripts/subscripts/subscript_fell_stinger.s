#include "macros/btlcmd.inc"


// Oxide: Fell Stinger raises its user's Attack three stages when the hit
// knocks the target out. A hit's side effect runs before fainting is
// processed, so the target's HP is already final here.
_000:
    CompareMonDataToValue OPCODE_NEQ, BTLSCR_DEFENDER, BATTLEMON_CUR_HP, 0, _end
    UpdateVar OPCODE_SET, BTLVAR_SIDE_EFFECT_PARAM, MOVE_SUBSCRIPT_PTR_ATTACK_UP_3_STAGES
    Call BATTLE_SUBSCRIPT_UPDATE_STAT_STAGE

_end:
    End

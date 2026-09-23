#include "macros/btlcmd.inc"


// Coaching targets the user's ally. With no ally, Platinum makes the user the
// target of an ally move, so the move fails here rather than coaching itself,
// and it fails against an ally that has fainted, as hg-engine's C has it.
_000:
    CompareVarToVar OPCODE_EQU, BTLVAR_ATTACKER, BTLVAR_DEFENDER, _fail
    CompareMonDataToValue OPCODE_EQU, BTLSCR_DEFENDER, BATTLEMON_CUR_HP, 0, _fail
    UpdateVar OPCODE_SET, BTLVAR_SIDE_EFFECT_FLAGS_DIRECT, MOVE_SIDE_EFFECT_TO_DEFENDER|MOVE_SUBSCRIPT_PTR_COACHING
    End

_fail:
    UpdateVar OPCODE_FLAG_ON, BTLVAR_MOVE_STATUS_FLAGS, MOVE_STATUS_FAILED
    End

#include "macros/btlcmd.inc"


// Oxide: Pollen Puff used on an ally restores half its maximum HP, rounded up,
// instead of damaging it. hg-engine's version also sets a flag with a
// comparison opcode where an update belongs; the effect script already sets
// what the heal needs, as Present's does.
_000:
    PrintAttackMessage
    Wait
    UpdateMonDataFromVar OPCODE_GET, BTLSCR_DEFENDER, BATTLEMON_MAX_HP, BTLVAR_HP_CALC_TEMP
    UpdateVar OPCODE_ADD, BTLVAR_HP_CALC_TEMP, 1
    DivideVarByValue BTLVAR_HP_CALC_TEMP, 2
    UpdateVarFromVar OPCODE_SET, BTLVAR_MSG_BATTLER_TEMP, BTLVAR_DEFENDER
    Call BATTLE_SUBSCRIPT_RECOVER_HP
    End

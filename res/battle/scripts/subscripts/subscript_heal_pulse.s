#include "macros/btlcmd.inc"


// Oxide: Heal Pulse restores half the target's maximum HP, or three quarters
// with Mega Launcher, rounded up as hg-engine's own divide does it; adding
// before dividing does the same for Platinum's, which truncates.
_000:
    // A substitute blocks it, as it does Pain Split.
    CheckSubstitute BTLSCR_DEFENDER, _blocked
    PrintAttackMessage
    Wait
    UpdateMonDataFromVar OPCODE_GET, BTLSCR_DEFENDER, BATTLEMON_MAX_HP, BTLVAR_HP_CALC_TEMP
    CheckAbility CHECK_HAVE, BTLSCR_ATTACKER, ABILITY_MEGALAUNCHER, _threeQuarters
    UpdateVar OPCODE_ADD, BTLVAR_HP_CALC_TEMP, 1
    DivideVarByValue BTLVAR_HP_CALC_TEMP, 2
    GoTo _heal

_threeQuarters:
    UpdateVar OPCODE_ADD, BTLVAR_HP_CALC_TEMP, 3
    DivideVarByValue BTLVAR_HP_CALC_TEMP, 4
    UpdateVar OPCODE_MUL, BTLVAR_HP_CALC_TEMP, 3

_heal:
    UpdateVarFromVar OPCODE_SET, BTLVAR_MSG_BATTLER_TEMP, BTLVAR_DEFENDER
    Call BATTLE_SUBSCRIPT_RECOVER_HP
    End

_blocked:
    UpdateVar OPCODE_FLAG_ON, BTLVAR_MOVE_STATUS_FLAGS, MOVE_STATUS_FAILED
    End

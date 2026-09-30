#include "macros/btlcmd.inc"


// Oxide: Lunar Blessing and Jungle Healing, which hg-engine left as plain
// hits of no power. Each restores a quarter of the maximum HP of its user
// and, in a double battle, its ally, and cures their status
// (subscript_lunar_blessing). Heal Block stops both before this runs
// (sMovesAffectedByHealBlock). The move fails when neither battler has HP to
// restore or a status to cure.
_000:
    CompareMonDataToValue OPCODE_FLAG_SET, BTLSCR_ATTACKER, BATTLEMON_STATUS, MON_CONDITION_ANY, _work
    UpdateMonDataFromVar OPCODE_GET, BTLSCR_ATTACKER, BATTLEMON_MAX_HP, BTLVAR_HP_CALC_TEMP
    CompareMonDataToVar OPCODE_NEQ, BTLSCR_ATTACKER, BATTLEMON_CUR_HP, BTLVAR_HP_CALC_TEMP, _work
    CompareVarToValue OPCODE_FLAG_NOT, BTLVAR_BATTLE_TYPE, BATTLE_TYPE_DOUBLES, _fail
    CompareMonDataToValue OPCODE_EQU, BTLSCR_ATTACKER_PARTNER, BATTLEMON_CUR_HP, 0, _fail
    CompareMonDataToValue OPCODE_FLAG_SET, BTLSCR_ATTACKER_PARTNER, BATTLEMON_STATUS, MON_CONDITION_ANY, _work
    UpdateMonDataFromVar OPCODE_GET, BTLSCR_ATTACKER_PARTNER, BATTLEMON_MAX_HP, BTLVAR_HP_CALC_TEMP
    CompareMonDataToVar OPCODE_NEQ, BTLSCR_ATTACKER_PARTNER, BATTLEMON_CUR_HP, BTLVAR_HP_CALC_TEMP, _work

_fail:
    UpdateVar OPCODE_FLAG_ON, BTLVAR_MOVE_STATUS_FLAGS, MOVE_STATUS_FAILED
    End

_work:
    PrintAttackMessage
    UpdateVarFromVar OPCODE_SET, BTLVAR_MSG_BATTLER_TEMP, BTLVAR_ATTACKER
    UpdateVar OPCODE_SET, BTLVAR_SIDE_EFFECT_FLAGS_DIRECT, MOVE_SIDE_EFFECT_TO_ATTACKER|MOVE_SUBSCRIPT_PTR_LUNAR_BLESSING
    End

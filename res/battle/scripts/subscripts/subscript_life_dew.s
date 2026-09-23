#include "macros/btlcmd.inc"


// Oxide: Life Dew restores a quarter of the maximum HP, rounded up, to its user
// and, in a double battle, to its ally; a battler already at full HP is
// skipped. hg-engine heals the ally from C. Platinum's two battlers on one
// side have ids that differ by 2, so the ally is the user's id with that bit
// flipped, and no new command is needed.
_000:
    PlayMoveAnimation BTLSCR_ATTACKER
    Wait
    UpdateVarFromVar OPCODE_SET, BTLVAR_MSG_BATTLER_TEMP, BTLVAR_ATTACKER
    UpdateMonDataFromVar OPCODE_GET, BTLSCR_MSG_BATTLER_TEMP, BATTLEMON_MAX_HP, BTLVAR_HP_CALC_TEMP
    CompareMonDataToVar OPCODE_EQU, BTLSCR_MSG_BATTLER_TEMP, BATTLEMON_CUR_HP, BTLVAR_HP_CALC_TEMP, _ally
    UpdateVar OPCODE_ADD, BTLVAR_HP_CALC_TEMP, 3
    DivideVarByValue BTLVAR_HP_CALC_TEMP, 4
    UpdateVar OPCODE_FLAG_ON, BTLVAR_BATTLE_CTX_STATUS, SYSCTL_SKIP_SPRITE_BLINK
    Call BATTLE_SUBSCRIPT_UPDATE_HP
    // {0} regained health!
    PrintMessage BattleStrings_Text_PokemonRegainedHealth_Ally, TAG_NICKNAME, BTLSCR_MSG_BATTLER_TEMP
    Wait
    WaitButtonABTime 30

_ally:
    CompareVarToValue OPCODE_FLAG_NOT, BTLVAR_BATTLE_TYPE, BATTLE_TYPE_DOUBLES, _end
    CompareMonDataToValue OPCODE_EQU, BTLSCR_ATTACKER_PARTNER, BATTLEMON_CUR_HP, 0, _end
    UpdateVarFromVar OPCODE_SET, BTLVAR_MSG_BATTLER_TEMP, BTLVAR_ATTACKER
    UpdateVar OPCODE_BITWISE_XOR, BTLVAR_MSG_BATTLER_TEMP, 2
    UpdateMonDataFromVar OPCODE_GET, BTLSCR_MSG_BATTLER_TEMP, BATTLEMON_MAX_HP, BTLVAR_HP_CALC_TEMP
    CompareMonDataToVar OPCODE_EQU, BTLSCR_MSG_BATTLER_TEMP, BATTLEMON_CUR_HP, BTLVAR_HP_CALC_TEMP, _end
    UpdateVar OPCODE_ADD, BTLVAR_HP_CALC_TEMP, 3
    DivideVarByValue BTLVAR_HP_CALC_TEMP, 4
    UpdateVar OPCODE_FLAG_ON, BTLVAR_BATTLE_CTX_STATUS, SYSCTL_SKIP_SPRITE_BLINK
    Call BATTLE_SUBSCRIPT_UPDATE_HP
    // {0} regained health!
    PrintMessage BattleStrings_Text_PokemonRegainedHealth_Ally, TAG_NICKNAME, BTLSCR_MSG_BATTLER_TEMP
    Wait
    WaitButtonABTime 30

_end:
    End

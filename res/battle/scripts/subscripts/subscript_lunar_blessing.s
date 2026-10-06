#include "macros/btlcmd.inc"


// Oxide: Lunar Blessing and Jungle Healing restore a quarter of the maximum
// HP, rounded up, and cure the status of the user and, in a double battle,
// its ally, as Life Dew heals (subscript_life_dew): the ally is the user's id
// with bit 1 flipped. A battler at full HP skips the healing, and one with no
// status skips the cure.
_000:
    PlayMoveAnimation BTLSCR_ATTACKER
    Wait
    UpdateVarFromVar OPCODE_SET, BTLVAR_MSG_BATTLER_TEMP, BTLVAR_ATTACKER
    UpdateMonDataFromVar OPCODE_GET, BTLSCR_MSG_BATTLER_TEMP, BATTLEMON_MAX_HP, BTLVAR_HP_CALC_TEMP
    CompareMonDataToVar OPCODE_EQU, BTLSCR_MSG_BATTLER_TEMP, BATTLEMON_CUR_HP, BTLVAR_HP_CALC_TEMP, _userCure
    UpdateVar OPCODE_ADD, BTLVAR_HP_CALC_TEMP, 3
    DivideVarByValue BTLVAR_HP_CALC_TEMP, 4
    UpdateVar OPCODE_FLAG_ON, BTLVAR_BATTLE_CTX_STATUS, SYSCTL_SKIP_SPRITE_BLINK
    Call BATTLE_SUBSCRIPT_UPDATE_HP
    // {0} regained health!
    PrintMessage BattleStrings_Text_PokemonRegainedHealth_Ally, TAG_NICKNAME, BTLSCR_MSG_BATTLER_TEMP
    Wait
    WaitButtonABTime 30

_userCure:
    CompareMonDataToValue OPCODE_FLAG_NOT, BTLSCR_MSG_BATTLER_TEMP, BATTLEMON_STATUS, MON_CONDITION_ANY, _ally
    UpdateMonData OPCODE_SET, BTLSCR_MSG_BATTLER_TEMP, BATTLEMON_STATUS, MON_CONDITION_NONE
    UpdateMonData OPCODE_FLAG_OFF, BTLSCR_MSG_BATTLER_TEMP, BATTLEMON_VOLATILE_STATUS, VOLATILE_CONDITION_NIGHTMARE
    // {0}’s status returned to normal!
    PrintMessage BattleStrings_Text_PokemonsStatusReturnedToNormal_Ally, TAG_NICKNAME, BTLSCR_MSG_BATTLER_TEMP
    Wait
    SetHealthBoxStatusIcon BTLSCR_MSG_BATTLER_TEMP, BATTLE_ANIMATION_NONE
    WaitButtonABTime 30

_ally:
    CompareVarToValue OPCODE_FLAG_NOT, BTLVAR_BATTLE_TYPE, BATTLE_TYPE_DOUBLES, _end
    CompareMonDataToValue OPCODE_EQU, BTLSCR_ATTACKER_PARTNER, BATTLEMON_CUR_HP, 0, _end
    UpdateVarFromVar OPCODE_SET, BTLVAR_MSG_BATTLER_TEMP, BTLVAR_ATTACKER
    UpdateVar OPCODE_BITWISE_XOR, BTLVAR_MSG_BATTLER_TEMP, 2
    UpdateMonDataFromVar OPCODE_GET, BTLSCR_MSG_BATTLER_TEMP, BATTLEMON_MAX_HP, BTLVAR_HP_CALC_TEMP
    CompareMonDataToVar OPCODE_EQU, BTLSCR_MSG_BATTLER_TEMP, BATTLEMON_CUR_HP, BTLVAR_HP_CALC_TEMP, _allyCure
    UpdateVar OPCODE_ADD, BTLVAR_HP_CALC_TEMP, 3
    DivideVarByValue BTLVAR_HP_CALC_TEMP, 4
    UpdateVar OPCODE_FLAG_ON, BTLVAR_BATTLE_CTX_STATUS, SYSCTL_SKIP_SPRITE_BLINK
    Call BATTLE_SUBSCRIPT_UPDATE_HP
    // {0} regained health!
    PrintMessage BattleStrings_Text_PokemonRegainedHealth_Ally, TAG_NICKNAME, BTLSCR_MSG_BATTLER_TEMP
    Wait
    WaitButtonABTime 30

_allyCure:
    CompareMonDataToValue OPCODE_FLAG_NOT, BTLSCR_MSG_BATTLER_TEMP, BATTLEMON_STATUS, MON_CONDITION_ANY, _end
    UpdateMonData OPCODE_SET, BTLSCR_MSG_BATTLER_TEMP, BATTLEMON_STATUS, MON_CONDITION_NONE
    UpdateMonData OPCODE_FLAG_OFF, BTLSCR_MSG_BATTLER_TEMP, BATTLEMON_VOLATILE_STATUS, VOLATILE_CONDITION_NIGHTMARE
    // {0}’s status returned to normal!
    PrintMessage BattleStrings_Text_PokemonsStatusReturnedToNormal_Ally, TAG_NICKNAME, BTLSCR_MSG_BATTLER_TEMP
    Wait
    SetHealthBoxStatusIcon BTLSCR_MSG_BATTLER_TEMP, BATTLE_ANIMATION_NONE
    WaitButtonABTime 30

_end:
    End

#include "macros/btlcmd.inc"


// Oxide, element 7: the Weakness Policy, used up to raise its holder's Attack
// and Sp. Atk two stages each when a supereffective move hits it (hg-engine's
// subscript 344). A stat already at +6 is passed over. With Contrary,
// BTLVAR_CALC_TEMP is set and both fall two stages instead, a stat already at
// -6 passed over, as hg-engine's stat change does for a Contrary holder.
_000:
    PlayBattleAnimation BTLSCR_MSG_TEMP, BATTLE_ANIMATION_HELD_ITEM
    Wait
    WaitButtonABTime 15
    CompareVarToValue OPCODE_NEQ, BTLVAR_CALC_TEMP, 0, _contrary
    CompareMonDataToValue OPCODE_EQU, BTLSCR_MSG_TEMP, BATTLEMON_ATTACK_STAGE, 12, _spatk
    UpdateMonData OPCODE_ADD, BTLSCR_MSG_TEMP, BATTLEMON_ATTACK_STAGE, 2
    CompareMonDataToValue OPCODE_LTE, BTLSCR_MSG_TEMP, BATTLEMON_ATTACK_STAGE, 12, _atk_msg
    UpdateMonData OPCODE_SET, BTLSCR_MSG_TEMP, BATTLEMON_ATTACK_STAGE, 12

_atk_msg:
    PlayBattleAnimation BTLSCR_MSG_TEMP, BATTLE_ANIMATION_STAT_BOOST
    Wait
    UpdateVar OPCODE_SET, BTLVAR_MSG_TEMP, BATTLE_STAT_ATTACK
    // The {1} sharply raised {0}’s {2}!
    PrintMessage BattleStrings_Text_TheItemSharplyRaisedPokemonsStat_Ally, TAG_NICKNAME_ITEM_STAT, BTLSCR_MSG_TEMP, BTLSCR_MSG_TEMP, BTLSCR_MSG_TEMP
    Wait
    WaitButtonABTime 30

_spatk:
    CompareMonDataToValue OPCODE_EQU, BTLSCR_MSG_TEMP, BATTLEMON_SP_ATTACK_STAGE, 12, _end
    UpdateMonData OPCODE_ADD, BTLSCR_MSG_TEMP, BATTLEMON_SP_ATTACK_STAGE, 2
    CompareMonDataToValue OPCODE_LTE, BTLSCR_MSG_TEMP, BATTLEMON_SP_ATTACK_STAGE, 12, _spatk_msg
    UpdateMonData OPCODE_SET, BTLSCR_MSG_TEMP, BATTLEMON_SP_ATTACK_STAGE, 12

_spatk_msg:
    PlayBattleAnimation BTLSCR_MSG_TEMP, BATTLE_ANIMATION_STAT_BOOST
    Wait
    UpdateVar OPCODE_SET, BTLVAR_MSG_TEMP, BATTLE_STAT_SP_ATTACK
    // The {1} sharply raised {0}’s {2}!
    PrintMessage BattleStrings_Text_TheItemSharplyRaisedPokemonsStat_Ally, TAG_NICKNAME_ITEM_STAT, BTLSCR_MSG_TEMP, BTLSCR_MSG_TEMP, BTLSCR_MSG_TEMP
    Wait
    WaitButtonABTime 30
    GoTo _end

_contrary:
    CompareMonDataToValue OPCODE_EQU, BTLSCR_MSG_TEMP, BATTLEMON_ATTACK_STAGE, 0, _contrary_spatk
    UpdateMonData OPCODE_SUB_TO_ZERO, BTLSCR_MSG_TEMP, BATTLEMON_ATTACK_STAGE, 2
    PlayBattleAnimation BTLSCR_MSG_TEMP, BATTLE_ANIMATION_STAT_DROP
    Wait
    UpdateVar OPCODE_SET, BTLVAR_MSG_TEMP, BATTLE_STAT_ATTACK
    // {0}’s {1} harshly fell!
    PrintMessage BattleStrings_Text_PokemonsStatHarshlyFell_Ally, TAG_NICKNAME_STAT, BTLSCR_MSG_TEMP, BTLSCR_MSG_TEMP
    Wait
    WaitButtonABTime 30

_contrary_spatk:
    CompareMonDataToValue OPCODE_EQU, BTLSCR_MSG_TEMP, BATTLEMON_SP_ATTACK_STAGE, 0, _end
    UpdateMonData OPCODE_SUB_TO_ZERO, BTLSCR_MSG_TEMP, BATTLEMON_SP_ATTACK_STAGE, 2
    PlayBattleAnimation BTLSCR_MSG_TEMP, BATTLE_ANIMATION_STAT_DROP
    Wait
    UpdateVar OPCODE_SET, BTLVAR_MSG_TEMP, BATTLE_STAT_SP_ATTACK
    // {0}’s {1} harshly fell!
    PrintMessage BattleStrings_Text_PokemonsStatHarshlyFell_Ally, TAG_NICKNAME_STAT, BTLSCR_MSG_TEMP, BTLSCR_MSG_TEMP
    Wait
    WaitButtonABTime 30

_end:
    RemoveItem BTLSCR_MSG_TEMP
    End

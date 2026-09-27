#include "macros/btlcmd.inc"


// Oxide, element 7: the Weakness Policy, used up to raise its holder's Attack
// and Sp. Atk two stages each when a supereffective move hits it (hg-engine's
// subscript 344). A stat already at +6 is passed over.
_000:
    PlayBattleAnimation BTLSCR_MSG_TEMP, BATTLE_ANIMATION_HELD_ITEM
    Wait
    WaitButtonABTime 15
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

_end:
    RemoveItem BTLSCR_MSG_TEMP
    End

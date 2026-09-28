#include "macros/btlcmd.inc"


// Oxide, element 7: the Absorb Bulb and the Cell Battery, used up to raise
// their holder's stat one stage when a move of their type hits it.
// BTLVAR_MSG_TEMP holds the stat, BTLSCR_MSG_TEMP the holder; the pattern of
// subscript_held_item_sharply_raise_stat.
_000:
    PlayBattleAnimation BTLSCR_MSG_TEMP, BATTLE_ANIMATION_HELD_ITEM
    Wait
    WaitButtonABTime 15
    PlayBattleAnimation BTLSCR_MSG_TEMP, BATTLE_ANIMATION_STAT_BOOST
    Wait
    // The {1} raised {0}’s {2}!
    PrintMessage BattleStrings_Text_TheItemRaisedPokemonsStat_Ally, TAG_NICKNAME_ITEM_STAT, BTLSCR_MSG_TEMP, BTLSCR_MSG_TEMP, BTLSCR_MSG_TEMP
    Wait
    WaitButtonABTime 30
    UpdateVar OPCODE_SET, BTLVAR_SCRIPT_TEMP, BATTLEMON_HP_STAGE
    UpdateVarFromVar OPCODE_ADD, BTLVAR_SCRIPT_TEMP, BTLVAR_MSG_TEMP
    UpdateMonData OPCODE_ADD, BTLSCR_MSG_TEMP, BATTLEMON_TEMP, 1
    CompareMonDataToValue OPCODE_LTE, BTLSCR_MSG_TEMP, BATTLEMON_TEMP, 12, _end
    UpdateMonData OPCODE_SET, BTLSCR_MSG_TEMP, BATTLEMON_TEMP, 12

_end:
    RemoveItem BTLSCR_MSG_TEMP
    End

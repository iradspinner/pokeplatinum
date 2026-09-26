#include "macros/btlcmd.inc"


// Oxide: Harvest. The Berry is in BTLVAR_MSG_ITEM_TEMP.
_000:
    UpdateMonDataFromVar OPCODE_SET, BTLSCR_MSG_BATTLER_TEMP, BATTLEMON_HELD_ITEM, BTLVAR_MSG_ITEM_TEMP
    // {0} harvested one {1}!
    PrintMessage BattleStrings_Text_PokemonHarvestedOneItem_Ally, TAG_NICKNAME_ITEM, BTLSCR_MSG_BATTLER_TEMP, BTLSCR_MSG_TEMP
    Wait 
    WaitButtonABTime 30
    End 

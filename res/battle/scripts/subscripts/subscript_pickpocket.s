#include "macros/btlcmd.inc"


// Oxide: Pickpocket. After a contact move its holder, the defender, takes the
// attacker's item, with Thief's message; TryPickpocket makes the checks.
_000:
    TryPickpocket _end
    // {0} stole {1}’s {2}!
    PrintMessage BattleStrings_Text_PokemonStolePokemonsItem_AllyAlly, TAG_NICKNAME_NICKNAME_ITEM, BTLSCR_DEFENDER, BTLSCR_ATTACKER, BTLSCR_ATTACKER
    Wait 
    WaitButtonABTime 30
    UpdateMonDataFromVar OPCODE_GET, BTLSCR_ATTACKER, BATTLEMON_HELD_ITEM, BTLVAR_SCRIPT_TEMP
    UpdateMonDataFromVar OPCODE_SET, BTLSCR_DEFENDER, BATTLEMON_HELD_ITEM, BTLVAR_SCRIPT_TEMP
    UpdateMonData OPCODE_SET, BTLSCR_ATTACKER, BATTLEMON_HELD_ITEM, ITEM_NONE

_end:
    End 

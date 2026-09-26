#include "macros/btlcmd.inc"


// Oxide: Magician takes the target's item after a damaging move, with Thief's
// checks (TryStealItem) and message; Sticky Hold keeps the item silently.
_000:
    TryStealItem _end, _end
    // {0} stole {1}’s {2}!
    PrintMessage BattleStrings_Text_PokemonStolePokemonsItem_AllyAlly, TAG_NICKNAME_NICKNAME_ITEM, BTLSCR_ATTACKER, BTLSCR_DEFENDER, BTLSCR_DEFENDER
    Wait 
    WaitButtonABTime 30
    UpdateMonDataFromVar OPCODE_GET, BTLSCR_DEFENDER, BATTLEMON_HELD_ITEM, BTLVAR_SCRIPT_TEMP
    UpdateMonDataFromVar OPCODE_SET, BTLSCR_ATTACKER, BATTLEMON_HELD_ITEM, BTLVAR_SCRIPT_TEMP
    UpdateMonData OPCODE_SET, BTLSCR_DEFENDER, BATTLEMON_HELD_ITEM, ITEM_NONE

_end:
    End 

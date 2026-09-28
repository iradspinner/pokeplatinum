#include "macros/btlcmd.inc"


// Oxide, element 7: an Air Balloon bursts when its holder is hit by a
// damaging move (hg-engine's subscript 337).
_000:
    // {0}’s {1} popped!
    PrintMessage BattleStrings_Text_PokemonsItemPopped_Ally, TAG_NICKNAME_ITEM, BTLSCR_DEFENDER, BTLSCR_DEFENDER
    Wait
    WaitButtonABTime 30
    RemoveItem BTLSCR_DEFENDER
    End

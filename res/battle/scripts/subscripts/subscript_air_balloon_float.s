#include "macros/btlcmd.inc"


// Oxide, element 7: a battler holding an Air Balloon says so when it comes
// in (hg-engine's subscript 338).
_000:
    // {0} floats in the air with its {1}!
    PrintMessage BattleStrings_Text_PokemonFloatsInTheAirWithItsItem_Ally, TAG_NICKNAME_ITEM, BTLSCR_MSG_TEMP, BTLSCR_MSG_TEMP
    Wait
    WaitButtonABTime 30
    End

#include "macros/btlcmd.inc"


// Oxide: Unnerve's switch-in message, for the holder's other side.
_000:
    // The foe’s team is too nervous to eat Berries!
    PrintMessage BattleStrings_Text_TheFoesTeamIsTooNervousToEatBerries, TAG_NONE_SIDE_CONSCIOUS, BTLSCR_MSG_BATTLER_TEMP
    Wait 
    WaitButtonABTime 30
    End 

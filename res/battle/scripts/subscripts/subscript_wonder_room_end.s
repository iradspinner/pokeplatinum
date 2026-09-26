#include "macros/btlcmd.inc"


// Oxide: Wonder Room's five turns are over (BattleControllerPlayer_CheckSideConditions).
_000:
    // Wonder Room wore off, and the Defense and Sp. Def stats returned to normal!
    PrintGlobalMessage BattleStrings_Text_WonderRoomWoreOffAndTheDefenseAndSpDefStatsReturnedToNormal, TAG_NONE
    Wait 
    WaitButtonABTime 30
    End 

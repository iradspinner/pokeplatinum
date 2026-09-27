#include "macros/btlcmd.inc"


// Oxide: Magic Room's five turns are over (BattleControllerPlayer_CheckSideConditions).
_000:
    // Magic Room wore off, and held items' effects returned to normal!
    PrintGlobalMessage BattleStrings_Text_MagicRoomWoreOffAndHeldItemsEffectsReturnedToNormal, TAG_NONE
    Wait 
    WaitButtonABTime 30
    End 

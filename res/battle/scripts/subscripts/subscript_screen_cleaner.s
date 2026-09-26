#include "macros/btlcmd.inc"


// Oxide: Screen Cleaner. BattleSystem_TriggerEffectOnSwitch has already
// ended the screens; this only says so.
_000:
    // All screens on the field were cleansed!
    PrintMessage BattleStrings_Text_AllScreensOnTheFieldWereCleansed, TAG_NONE
    Wait 
    WaitButtonABTime 30
    End 

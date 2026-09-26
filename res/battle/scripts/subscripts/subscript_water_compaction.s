#include "macros/btlcmd.inc"


// Oxide: Water Compaction. A Water-type hit raises its holder's Defense by two
// stages.
_000:
    AbilityStatChange BTLSCR_DEFENDER, BTLSCR_DEFENDER, BATTLE_STAT_DEFENSE, 2, _end
    PlayBattleAnimationFromVar BTLSCR_MSG_BATTLER_TEMP, BTLVAR_SCRIPT_TEMP
    Wait 
    PrintBufferedMessage 
    Wait 
    WaitButtonABTime 30

_end:
    End 

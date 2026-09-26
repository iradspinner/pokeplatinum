#include "macros/btlcmd.inc"


// Oxide: Rattled. A Bug, Ghost or Dark hit raises its holder's Speed by one
// stage.
_000:
    AbilityStatChange BTLSCR_DEFENDER, BTLSCR_DEFENDER, BATTLE_STAT_SPEED, 1, _end
    PlayBattleAnimationFromVar BTLSCR_MSG_BATTLER_TEMP, BTLVAR_SCRIPT_TEMP
    Wait 
    PrintBufferedMessage 
    Wait 
    WaitButtonABTime 30

_end:
    End 

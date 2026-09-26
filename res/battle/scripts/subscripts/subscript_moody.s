#include "macros/btlcmd.inc"


// Oxide: Moody. At the end of each turn the stat in BTLVAR_CALC_TEMP rises two
// stages and the one in BTLVAR_MSG_TEMP falls one; BattleSystem_TriggerTurnEndAbility
// draws both.
_000:
    AbilityStatChangeFromVar BTLSCR_MSG_BATTLER_TEMP, BTLSCR_MSG_BATTLER_TEMP, BTLVAR_CALC_TEMP, 2, _lower
    PlayBattleAnimationFromVar BTLSCR_MSG_BATTLER_TEMP, BTLVAR_SCRIPT_TEMP
    Wait 
    PrintBufferedMessage 
    Wait 
    WaitButtonABTime 30

_lower:
    AbilityStatChangeFromVar BTLSCR_MSG_BATTLER_TEMP, BTLSCR_MSG_BATTLER_TEMP, BTLVAR_MSG_TEMP, -1, _end
    PlayBattleAnimationFromVar BTLSCR_MSG_BATTLER_TEMP, BTLVAR_SCRIPT_TEMP
    Wait 
    PrintBufferedMessage 
    Wait 
    WaitButtonABTime 30

_end:
    End 

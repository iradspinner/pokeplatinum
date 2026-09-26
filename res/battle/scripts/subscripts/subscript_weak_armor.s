#include "macros/btlcmd.inc"


// Oxide: Weak Armor. A physical hit lowers its holder's Defense by one stage
// and raises its Speed by two (the later games' amount).
_000:
    AbilityStatChange BTLSCR_DEFENDER, BTLSCR_DEFENDER, BATTLE_STAT_DEFENSE, -1, _speed
    PlayBattleAnimationFromVar BTLSCR_MSG_BATTLER_TEMP, BTLVAR_SCRIPT_TEMP
    Wait 
    PrintBufferedMessage 
    Wait 
    WaitButtonABTime 30

_speed:
    AbilityStatChange BTLSCR_DEFENDER, BTLSCR_DEFENDER, BATTLE_STAT_SPEED, 2, _end
    PlayBattleAnimationFromVar BTLSCR_MSG_BATTLER_TEMP, BTLVAR_SCRIPT_TEMP
    Wait 
    PrintBufferedMessage 
    Wait 
    WaitButtonABTime 30

_end:
    End 

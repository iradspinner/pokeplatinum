#include "macros/btlcmd.inc"


// Oxide: Gooey. A contact move lowers the attacker's Speed by one stage,
// which Defiant and Competitive answer.
_000:
    AbilityStatChange BTLSCR_DEFENDER, BTLSCR_ATTACKER, BATTLE_STAT_SPEED, -1, _end
    PlayBattleAnimationFromVar BTLSCR_MSG_BATTLER_TEMP, BTLVAR_SCRIPT_TEMP
    Wait 
    PrintBufferedMessage 
    Wait 
    WaitButtonABTime 30
    TryDefiant _end
    PlayBattleAnimation BTLSCR_SIDE_EFFECT_MON, BATTLE_ANIMATION_STAT_BOOST
    Wait 
    PrintBufferedMessage 
    Wait 
    WaitButtonABTime 30

_end:
    End 

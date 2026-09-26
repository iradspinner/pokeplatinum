#include "macros/btlcmd.inc"


// Oxide: Berserk. A hit that takes its holder below half its HP raises its
// Sp. Atk by one stage.
_000:
    AbilityStatChange BTLSCR_DEFENDER, BTLSCR_DEFENDER, BATTLE_STAT_SP_ATTACK, 1, _end
    PlayBattleAnimationFromVar BTLSCR_MSG_BATTLER_TEMP, BTLVAR_SCRIPT_TEMP
    Wait 
    PrintBufferedMessage 
    Wait 
    WaitButtonABTime 30

_end:
    End 

#include "macros/btlcmd.inc"


// Oxide: Sky Drop's first turn, after TrySkyDrop has lifted the target: as a
// Fly user's charge turn (subscript_vanish_on_charge_turn), with the target
// vanishing into the air along with the user.
_000:
    PlayMoveAnimation BTLSCR_ATTACKER
    Wait 
    PrintBufferedMessage 
    Wait 
    WaitButtonABTime 30
    LockMoveChoice BTLSCR_SIDE_EFFECT_MON
    ToggleVanish BTLSCR_SIDE_EFFECT_MON, TRUE
    ToggleVanish BTLSCR_DEFENDER, TRUE
    Wait 
    End 

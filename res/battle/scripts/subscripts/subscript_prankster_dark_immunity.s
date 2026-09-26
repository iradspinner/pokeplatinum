#include "macros/btlcmd.inc"


// Oxide: a Dark-type target is not affected by a status move Prankster raised.
_000:
    PrintAttackMessage
    Wait
    WaitButtonABTime 30
    // It doesn’t affect {0}...
    PrintMessage BattleStrings_Text_ItDoesntAffectPokemon_Ally, TAG_NICKNAME, BTLSCR_DEFENDER
    Wait
    WaitButtonABTime 30
    End

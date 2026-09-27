#include "macros/btlcmd.inc"


// Oxide: a Beak Blast user heats its beak at the start of the turn, as a Focus
// Punch user tightens its focus (BattleControllerPlayer_CheckPreMoveActions).
_000:
    // {0} started heating up its beak!
    PrintMessage BattleStrings_Text_PokemonStartedHeatingUpItsBeak_Ally, TAG_NICKNAME, BTLSCR_MSG_TEMP
    Wait 
    WaitButtonABTime 30
    End 

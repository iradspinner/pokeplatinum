#include "macros/btlcmd.inc"


// Oxide: a sound move chosen before Throat Chop landed fails when its turn
// comes, with Heal Block's message and Throat Chop named in it.
_000:
    UpdateVar OPCODE_SET, BTLVAR_MSG_MOVE_TEMP, MOVE_THROAT_CHOP
    // {0} can’t use {2} because of {1}!
    PrintMessage BattleStrings_Text_PokemonCantUseMoveBecauseOfMove_Ally, TAG_NICKNAME_MOVE_MOVE, BTLSCR_ATTACKER, BTLSCR_MSG_TEMP, BTLSCR_ATTACKER
    Wait
    WaitButtonABTime 30
    End

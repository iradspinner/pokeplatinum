#include "macros/btlcmd.inc"


// Oxide: Cursed Body. BattleSystem_TriggerAbilityOnHit has already disabled
// the attacker's move; this only says so, with Disable's message.
_000:
    // {0}’s {1} was disabled!
    PrintMessage BattleStrings_Text_PokemonsMoveWasDisabled_Ally, TAG_NICKNAME_MOVE, BTLSCR_ATTACKER, BTLSCR_MSG_TEMP
    Wait 
    WaitButtonABTime 30
    End 

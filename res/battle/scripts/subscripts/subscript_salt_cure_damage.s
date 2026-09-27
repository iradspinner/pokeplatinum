#include "macros/btlcmd.inc"


// Oxide: a salted battler loses an eighth of its maximum HP at the end of
// each turn, a quarter if it is a Water or Steel type; the controller sets
// the amount and skips a Magic Guard holder, as for Bad Dreams.
_000:
    // {0} is hurt by Salt Cure!
    PrintMessage BattleStrings_Text_PokemonIsHurtBySaltCure_Ally, TAG_NICKNAME, BTLSCR_MSG_TEMP
    Wait 
    WaitButtonABTime 30
    UpdateVar OPCODE_FLAG_ON, BTLVAR_BATTLE_CTX_STATUS, SYSCTL_SKIP_SPRITE_BLINK
    GoToSubscript BATTLE_SUBSCRIPT_UPDATE_HP

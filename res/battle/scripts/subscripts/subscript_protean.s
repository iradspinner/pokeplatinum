#include "macros/btlcmd.inc"


// Oxide: Protean and Libero give their holder its move's type, which
// BTLVAR_MSG_TEMP holds, with Color Change's message.
_000:
    UpdateMonDataFromVar OPCODE_SET, BTLSCR_ATTACKER, BATTLEMON_TYPE_1, BTLVAR_MSG_TEMP
    UpdateMonDataFromVar OPCODE_SET, BTLSCR_ATTACKER, BATTLEMON_TYPE_2, BTLVAR_MSG_TEMP
    // {0}’s {1} made it the {2} type!
    PrintMessage BattleStrings_Text_PokemonsAbilityMadeItType_Ally, TAG_NICKNAME_ABILITY_TYPE, BTLSCR_ATTACKER, BTLSCR_ATTACKER, BTLSCR_MSG_TEMP
    Wait 
    WaitButtonABTime 30
    End 

#include "macros/btlcmd.inc"


// Oxide: Magic Bounce. Magic Coat's subscript with the holder's own message;
// MagicCoat turns the move back on its user.
_000:
    PrintAttackMessage 
    Wait 
    WaitButtonABTime 15
    // {0} bounced the {1} back!
    PrintMessage BattleStrings_Text_PokemonBouncedTheMoveBack_Ally, TAG_NICKNAME_MOVE, BTLSCR_DEFENDER, BTLSCR_ATTACKER
    Wait 
    WaitButtonABTime 30
    MagicCoat 
    UpdateVar OPCODE_FLAG_OFF, BTLVAR_BATTLE_CTX_STATUS, SYSCTL_PLAYED_MOVE_ANIMATION
    End 

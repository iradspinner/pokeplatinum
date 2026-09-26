#include "macros/btlcmd.inc"


// Oxide: Queenly Majesty stops a move of raised priority aimed at its holder
// or its partner, with Damp's message; abilityMon is the holder.
_000:
    PrintAttackMessage
    Wait
    WaitButtonABTime 30
    // {0}’s {1} prevents {2} from using {3}!
    PrintMessage BattleStrings_Text_PokemonsAbilityPreventsPokemonFromUsingMove_AllyAlly, TAG_NICKNAME_ABILITY_NICKNAME_MOVE, BTLSCR_ABILITY_MON, BTLSCR_ABILITY_MON, BTLSCR_ATTACKER, BTLSCR_ATTACKER
    Wait
    WaitButtonABTime 30
    End

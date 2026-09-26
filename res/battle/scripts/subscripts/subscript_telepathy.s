#include "macros/btlcmd.inc"


// Oxide: Telepathy keeps its holder safe from its partner's damaging moves.
_000:
    PrintAttackMessage 
    Wait 
    WaitButtonABTime 30
    // {0} avoids attacks by its ally Pokémon!
    PrintMessage BattleStrings_Text_PokemonAvoidsAttacksByItsAllyPokemon_Ally, TAG_NICKNAME, BTLSCR_DEFENDER
    Wait 
    WaitButtonABTime 30
    End 

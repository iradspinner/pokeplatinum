#include "macros/btlcmd.inc"


// Oxide: the switch-in message of Dark Aura, Fairy Aura or Aura Break, which
// BattleSystem_TriggerEffectOnSwitch leaves in BTLVAR_MSG_TEMP.
_000:
    CompareVarToValue OPCODE_EQU, BTLVAR_MSG_TEMP, ABILITY_FAIRY_AURA, _fairy
    CompareVarToValue OPCODE_EQU, BTLVAR_MSG_TEMP, ABILITY_AURA_BREAK, _break
    // {0} is radiating a dark aura!
    PrintMessage BattleStrings_Text_PokemonIsRadiatingADarkAura_Ally, TAG_NICKNAME, BTLSCR_MSG_BATTLER_TEMP
    GoTo _end

_fairy:
    // {0} is radiating a fairy aura!
    PrintMessage BattleStrings_Text_PokemonIsRadiatingAFairyAura_Ally, TAG_NICKNAME, BTLSCR_MSG_BATTLER_TEMP
    GoTo _end

_break:
    // {0} reversed all other Pokémon’s auras!
    PrintMessage BattleStrings_Text_PokemonReversedAllOtherPokemonsAuras_Ally, TAG_NICKNAME, BTLSCR_MSG_BATTLER_TEMP

_end:
    Wait 
    WaitButtonABTime 30
    End 

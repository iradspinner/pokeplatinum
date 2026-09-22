#include "macros/btlcmd.inc"


// Oxide: Double Shock takes the Electric type away from its user after it hits,
// the move itself having failed already if the user did not have it. A dual
// type keeps its other type, which Platinum writes as that type twice; a user
// that was Electric and nothing else is left with the ??? type until it
// switches out, since a battler's types are reloaded when it comes back in.
_000:
    // {0} used up all its electricity!
    PrintMessage BattleStrings_Text_PokemonUsedUpAllItsElectricity_Ally, TAG_NICKNAME, BTLSCR_ATTACKER
    Wait
    WaitButtonABTime 30
    CompareMonDataToValue OPCODE_NEQ, BTLSCR_ATTACKER, BATTLEMON_TYPE_1, TYPE_ELECTRIC, _second
    CompareMonDataToValue OPCODE_EQU, BTLSCR_ATTACKER, BATTLEMON_TYPE_2, TYPE_ELECTRIC, _both
    UpdateMonDataFromVar OPCODE_GET, BTLSCR_ATTACKER, BATTLEMON_TYPE_2, BTLVAR_CALC_TEMP
    UpdateMonDataFromVar OPCODE_SET, BTLSCR_ATTACKER, BATTLEMON_TYPE_1, BTLVAR_CALC_TEMP
    End

_second:
    CompareMonDataToValue OPCODE_NEQ, BTLSCR_ATTACKER, BATTLEMON_TYPE_2, TYPE_ELECTRIC, _end
    UpdateMonDataFromVar OPCODE_GET, BTLSCR_ATTACKER, BATTLEMON_TYPE_1, BTLVAR_CALC_TEMP
    UpdateMonDataFromVar OPCODE_SET, BTLSCR_ATTACKER, BATTLEMON_TYPE_2, BTLVAR_CALC_TEMP
    End

_both:
    UpdateMonData OPCODE_SET, BTLSCR_ATTACKER, BATTLEMON_TYPE_1, TYPE_MYSTERY
    UpdateMonData OPCODE_SET, BTLSCR_ATTACKER, BATTLEMON_TYPE_2, TYPE_MYSTERY

_end:
    End

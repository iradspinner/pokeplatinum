#include "macros/btlcmd.inc"


// Oxide: Jaw Lock traps both its user and the target after it hits. hg-engine
// runs its subscript from C after the move; this is that logic as a hit's
// side effect, ending quietly rather than failing the move when there is
// nothing to do. A battler already trapped keeps its first trapper.
_000:
    CompareMonDataToValue OPCODE_EQU, BTLSCR_DEFENDER, BATTLEMON_CUR_HP, 0, _end
    CheckSubstitute BTLSCR_DEFENDER, _end
    CompareMonDataToValue OPCODE_FLAG_SET, BTLSCR_ATTACKER, BATTLEMON_VOLATILE_STATUS, VOLATILE_CONDITION_MEAN_LOOK, _trapDefender
    CompareMonDataToValue OPCODE_FLAG_SET, BTLSCR_DEFENDER, BATTLEMON_VOLATILE_STATUS, VOLATILE_CONDITION_MEAN_LOOK, _trapAttacker
    UpdateMonData OPCODE_FLAG_ON, BTLSCR_ATTACKER, BATTLEMON_VOLATILE_STATUS, VOLATILE_CONDITION_MEAN_LOOK
    UpdateMonData OPCODE_FLAG_ON, BTLSCR_DEFENDER, BATTLEMON_VOLATILE_STATUS, VOLATILE_CONDITION_MEAN_LOOK
    UpdateMonDataFromVar OPCODE_FLAG_ON, BTLSCR_ATTACKER, BATTLEMON_MEAN_LOOK_TARGET, BTLVAR_DEFENDER
    UpdateMonDataFromVar OPCODE_FLAG_ON, BTLSCR_DEFENDER, BATTLEMON_MEAN_LOOK_TARGET, BTLVAR_ATTACKER
    // Neither Pokémon can run away!
    PrintMessage BattleStrings_Text_NeitherPokemonCanRunAway, TAG_NONE
    Wait
    WaitButtonABTime 30
    End

_trapDefender:
    CompareMonDataToValue OPCODE_FLAG_SET, BTLSCR_DEFENDER, BATTLEMON_VOLATILE_STATUS, VOLATILE_CONDITION_MEAN_LOOK, _end
    UpdateMonData OPCODE_FLAG_ON, BTLSCR_DEFENDER, BATTLEMON_VOLATILE_STATUS, VOLATILE_CONDITION_MEAN_LOOK
    UpdateMonDataFromVar OPCODE_FLAG_ON, BTLSCR_DEFENDER, BATTLEMON_MEAN_LOOK_TARGET, BTLVAR_ATTACKER
    // {0} can no longer escape!
    PrintMessage BattleStrings_Text_PokemonCanNoLongerEscape_Ally, TAG_NICKNAME, BTLSCR_DEFENDER
    Wait
    WaitButtonABTime 30
    End

_trapAttacker:
    UpdateMonData OPCODE_FLAG_ON, BTLSCR_ATTACKER, BATTLEMON_VOLATILE_STATUS, VOLATILE_CONDITION_MEAN_LOOK
    UpdateMonDataFromVar OPCODE_FLAG_ON, BTLSCR_ATTACKER, BATTLEMON_MEAN_LOOK_TARGET, BTLVAR_DEFENDER
    // {0} can no longer escape!
    PrintMessage BattleStrings_Text_PokemonCanNoLongerEscape_Ally, TAG_NICKNAME, BTLSCR_ATTACKER
    Wait
    WaitButtonABTime 30

_end:
    End

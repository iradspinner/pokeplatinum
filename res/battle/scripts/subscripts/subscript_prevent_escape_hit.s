#include "macros/btlcmd.inc"


// Oxide: Thousand Waves, Spirit Shackle and Anchor Shot trap the target after
// they hit. Mean Look's own subscript cannot be reused, because it plays the
// move again and fails the move when the target is already trapped; here that
// case, a fainted target and a substitute all end quietly.
_000:
    CompareMonDataToValue OPCODE_EQU, BTLSCR_DEFENDER, BATTLEMON_CUR_HP, 0, _end
    CompareMonDataToValue OPCODE_FLAG_SET, BTLSCR_DEFENDER, BATTLEMON_VOLATILE_STATUS, VOLATILE_CONDITION_MEAN_LOOK, _end
    CheckSubstitute BTLSCR_DEFENDER, _end
    UpdateMonData OPCODE_FLAG_ON, BTLSCR_DEFENDER, BATTLEMON_VOLATILE_STATUS, VOLATILE_CONDITION_MEAN_LOOK
    UpdateMonDataFromVar OPCODE_FLAG_ON, BTLSCR_DEFENDER, BATTLEMON_MEAN_LOOK_TARGET, BTLVAR_ATTACKER
    // {0} can no longer escape!
    PrintMessage BattleStrings_Text_PokemonCanNoLongerEscape_Ally, TAG_NICKNAME, BTLSCR_DEFENDER
    Wait
    WaitButtonABTime 30

_end:
    End

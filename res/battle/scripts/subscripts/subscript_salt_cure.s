#include "macros/btlcmd.inc"


// Oxide: Salt Cure salts the target once it has hit, until the target leaves
// the field; the end of turn check then takes its HP
// (BattleControllerPlayer_CheckMonConditions). Nothing happens if the target
// fainted, is behind a substitute or is already salted.
_000:
    CompareMonDataToValue OPCODE_EQU, BTLSCR_DEFENDER, BATTLEMON_CUR_HP, 0, _end
    CheckSubstitute BTLSCR_DEFENDER, _end
    CompareMonDataToValue OPCODE_FLAG_SET, BTLSCR_DEFENDER, BATTLEMON_OXIDE_FLAGS, OXIDE_MON_FLAG_SALT_CURED, _end
    UpdateMonData OPCODE_FLAG_ON, BTLSCR_DEFENDER, BATTLEMON_OXIDE_FLAGS, OXIDE_MON_FLAG_SALT_CURED
    // {0} is being salt cured!
    PrintMessage BattleStrings_Text_PokemonIsBeingSaltCured_Ally, TAG_NICKNAME, BTLSCR_DEFENDER
    Wait
    WaitButtonABTime 30

_end:
    End

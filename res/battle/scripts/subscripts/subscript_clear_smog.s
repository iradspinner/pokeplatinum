#include "macros/btlcmd.inc"


// Oxide: Clear Smog resets the target's stat stages after it hits, unless the
// target fainted or the hit landed on a substitute. hg-engine does this with a
// command of its own and then prints Haze's line, as this does.
_000:
    CompareMonDataToValue OPCODE_EQU, BTLSCR_DEFENDER, BATTLEMON_CUR_HP, 0, _end
    CheckSubstitute BTLSCR_DEFENDER, _end
    UpdateMonData OPCODE_SET, BTLSCR_DEFENDER, BATTLEMON_ATTACK_STAGE, 6
    UpdateMonData OPCODE_SET, BTLSCR_DEFENDER, BATTLEMON_DEFENSE_STAGE, 6
    UpdateMonData OPCODE_SET, BTLSCR_DEFENDER, BATTLEMON_SPEED_STAGE, 6
    UpdateMonData OPCODE_SET, BTLSCR_DEFENDER, BATTLEMON_SP_ATTACK_STAGE, 6
    UpdateMonData OPCODE_SET, BTLSCR_DEFENDER, BATTLEMON_SP_DEFENSE_STAGE, 6
    UpdateMonData OPCODE_SET, BTLSCR_DEFENDER, BATTLEMON_ACCURACY_STAGE, 6
    UpdateMonData OPCODE_SET, BTLSCR_DEFENDER, BATTLEMON_EVASION_STAGE, 6
    // All stat changes were eliminated!
    PrintMessage BattleStrings_Text_AllStatChangesWereEliminated, TAG_NONE
    Wait
    WaitButtonABTime 30

_end:
    End

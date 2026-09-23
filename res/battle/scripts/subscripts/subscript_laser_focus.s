#include "macros/btlcmd.inc"


// Oxide: Laser Focus makes its user's move on the next turn a critical hit.
// hg-engine's subscript, with the user's Laser Focus countdown set to 2 (the
// high bit) in place of hg-engine's move-condition flag. It runs down at the
// end of each turn, as Lock-On's does.
_000:
    PrintAttackMessage
    Wait
    PlayMoveAnimation BTLSCR_ATTACKER
    Wait
    UpdateMonData OPCODE_FLAG_OFF, BTLSCR_ATTACKER, BATTLEMON_MOVE_EFFECTS_MASK, MOVE_EFFECT_LASER_FOCUS
    UpdateMonData OPCODE_FLAG_ON, BTLSCR_ATTACKER, BATTLEMON_MOVE_EFFECTS_MASK, MOVE_EFFECT_LASER_FOCUS_1
    // {0} concentrated intensely!
    PrintMessage BattleStrings_Text_PokemonConcentratedIntensely_Ally, TAG_NICKNAME, BTLSCR_ATTACKER
    Wait
    WaitButtonABTime 30
    End

#include "macros/btlcmd.inc"


// Oxide: Fury Cutter as Kaizo has it (the move reworks, Ian, 2026-10-06).
// Three hits, the first at the move's listed power and each later one 10
// more (30, 40, 50 at Fury Cutter's 30). Each hit checks accuracy and the
// move stops at the first miss, as Triple Kick does. The power is kept in
// the move's power variable, which starts at 0 for every move and lasts
// across its hits.
_000:
    SetMultiHit 3, SYSCTL_TRIPLE_KICK
    UpdateVar OPCODE_SET, BTLVAR_AFTER_MOVE_MESSAGE_TYPE, AFTER_MOVE_MESSAGE_MULTI_HIT
    CompareVarToValue OPCODE_EQU, BTLVAR_MOVE_POWER, 0, _first
    UpdateVar OPCODE_ADD, BTLVAR_MOVE_POWER, 10
    GoTo _hit

_first:
    GetCurrentMoveData MOVEATTRIBUTE_POWER
    UpdateVarFromVar OPCODE_SET, BTLVAR_MOVE_POWER, BTLVAR_CALC_TEMP

_hit:
    CalcCrit
    CalcDamage
    End

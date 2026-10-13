#include "macros/btlcmd.inc"


// Oxide: three hits rising by 10, Fury Cutter's since the move reworks (Ian,
// 2026-10-06) and Triple Kick's since 2026-10-12. The first hit is at the
// move's listed power and each later one 10 more: Fury Cutter 10, 20, 30;
// Triple Kick 20, 30, 40 (Ian, 2026-10-12). Each hit checks accuracy and
// the move stops at the first miss, as Triple Kick always has. The power is kept in
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

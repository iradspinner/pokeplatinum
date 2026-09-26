#include "macros/btlcmd.inc"


// Oxide: Belch, a plain hit once its user has eaten a Berry this battle.
// hg-engine fails it before the move in C; TryBelch does the same here, the
// way Fake Out's script fails after the first turn.
_000:
    TryBelch _failed
    CalcCrit
    CalcDamage
    End

_failed:
    UpdateVar OPCODE_FLAG_ON, BTLVAR_MOVE_STATUS_FLAGS, MOVE_STATUS_FAILED
    End

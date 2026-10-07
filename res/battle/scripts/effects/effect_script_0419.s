#include "macros/btlcmd.inc"


// Oxide: Shell Trap (the move reworks, Ian, 2026-10-06). It moves last, at
// -3, and strikes only if a physical move has hit its user this turn: the
// user's physical damage mask, which Counter reads too, holds a bit for each
// battler whose physical move did it damage this turn (not a Substitute's).
// Otherwise it fails.
_000:
    CompareVarToValue OPCODE_EQU, BTLVAR_ATTACKER_PHYSICAL_DAMAGE_MASK, 0, _fail
    CalcCrit
    CalcDamage
    End

_fail:
    UpdateVar OPCODE_FLAG_ON, BTLVAR_MOVE_STATUS_FLAGS, MOVE_STATUS_FAILED
    End

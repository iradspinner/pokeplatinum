#include "macros/btlcmd.inc"


// Oxide: Upper Hand (the move reworks, Ian, 2026-10-06). It fails unless its
// target has yet to act this turn and has chosen a move of raised priority
// (TryUpperHand); when it lands, the target flinches, at the move's 100%
// chance, as Fake Out's target does.
_000:
    TryUpperHand _fail
    UpdateVar OPCODE_SET, BTLVAR_SIDE_EFFECT_FLAGS_INDIRECT, MOVE_SIDE_EFFECT_TO_DEFENDER|MOVE_SUBSCRIPT_PTR_FLINCH
    CalcCrit
    CalcDamage
    End

_fail:
    UpdateVar OPCODE_FLAG_ON, BTLVAR_MOVE_STATUS_FLAGS, MOVE_STATUS_FAILED
    End

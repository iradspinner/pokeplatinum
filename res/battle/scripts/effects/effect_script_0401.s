#include "macros/btlcmd.inc"


// Oxide: Throat Chop. A plain hit that, once it has hit, keeps the target
// from using sound moves for the rest of this turn and all of the next
// (subscript_throat_chop), as in Generation 7 on.
_000:
    UpdateVar OPCODE_SET, BTLVAR_SIDE_EFFECT_FLAGS_INDIRECT, MOVE_SIDE_EFFECT_ON_HIT|MOVE_SIDE_EFFECT_TO_DEFENDER|MOVE_SUBSCRIPT_PTR_THROAT_CHOP
    CalcCrit
    CalcDamage
    End

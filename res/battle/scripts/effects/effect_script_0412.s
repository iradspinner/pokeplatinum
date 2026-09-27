#include "macros/btlcmd.inc"


// Oxide: Teatime, which feeds every battler its own Berry (subscript_teatime).
_000:
    UpdateVar OPCODE_SET, BTLVAR_SIDE_EFFECT_FLAGS_DIRECT, MOVE_SIDE_EFFECT_ON_HIT|MOVE_SIDE_EFFECT_TO_ATTACKER|MOVE_SUBSCRIPT_PTR_TEATIME
    End

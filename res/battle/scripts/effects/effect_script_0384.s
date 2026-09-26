#include "macros/btlcmd.inc"


// Oxide: Entrainment, as hg-engine's effect 384, with Worry Seed's flags.
_000:
    UpdateVar OPCODE_SET, BTLVAR_SIDE_EFFECT_FLAGS_DIRECT, MOVE_SIDE_EFFECT_ON_HIT|MOVE_SIDE_EFFECT_TO_DEFENDER|MOVE_SUBSCRIPT_PTR_ENTRAINMENT
    End 

#include "macros/btlcmd.inc"


// Oxide: Core Enforcer. A plain hit that then suppresses the ability of a
// target that has already moved this turn (subscript_core_enforcer).
_000:
    UpdateVar OPCODE_SET, BTLVAR_SIDE_EFFECT_FLAGS_INDIRECT, MOVE_SIDE_EFFECT_ON_HIT|MOVE_SIDE_EFFECT_TO_DEFENDER|MOVE_SUBSCRIPT_PTR_CORE_ENFORCER
    CalcCrit
    CalcDamage
    End

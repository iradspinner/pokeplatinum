#include "macros/btlcmd.inc"


// Oxide: Smack Down hits a Pokemon in the air from Fly or Bounce, and Thousand
// Arrows, which shares the effect, does not. Both then ground the target.
_000:
    CompareVarToValue OPCODE_EQU, BTLVAR_CURRENT_MOVE, MOVE_THOUSAND_ARROWS, _hit
    UpdateVar OPCODE_FLAG_ON, BTLVAR_BATTLE_CTX_STATUS, SYSCTL_HIT_DURING_FLY

_hit:
    UpdateVar OPCODE_SET, BTLVAR_SIDE_EFFECT_FLAGS_INDIRECT, MOVE_SIDE_EFFECT_ON_HIT|MOVE_SIDE_EFFECT_TO_DEFENDER|MOVE_SUBSCRIPT_PTR_SMACK_DOWN
    CalcCrit
    CalcDamage
    End

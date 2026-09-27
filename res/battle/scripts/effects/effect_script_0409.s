#include "macros/btlcmd.inc"


// Oxide: Salt Cure. A plain hit that salts the target (subscript_salt_cure),
// which then loses HP at the end of every turn until it leaves the field, as
// in Generation 9; hg-engine has no code for it.
_000:
    UpdateVar OPCODE_SET, BTLVAR_SIDE_EFFECT_FLAGS_INDIRECT, MOVE_SIDE_EFFECT_ON_HIT|MOVE_SIDE_EFFECT_TO_DEFENDER|MOVE_SUBSCRIPT_PTR_SALT_CURE
    CalcCrit
    CalcDamage
    End

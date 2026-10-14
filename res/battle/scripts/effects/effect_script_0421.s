#include "macros/btlcmd.inc"


// Oxide: Eerie Spell (Ian, 2026-10-14). A plain hit that then takes 3 PP
// from the target's last used move (subscript_reduce_target_pp_hit), as in
// the later games. The drain runs only when the target still stands and its
// Substitute did not take the hit, since in Oxide a sound move meets a
// Substitute.
_000:
    UpdateVar OPCODE_SET, BTLVAR_SIDE_EFFECT_FLAGS_INDIRECT, MOVE_SIDE_EFFECT_CHECK_HP_AND_SUBSTITUTE|MOVE_SIDE_EFFECT_TO_DEFENDER|MOVE_SUBSCRIPT_PTR_REDUCE_TARGET_PP_HIT
    CalcCrit
    CalcDamage
    End

#include "macros/btlcmd.inc"


// Oxide: Raging Fury's after effect (the move reworks, Ian, 2026-10-06), on
// the pattern of Volt Tackle's: the user takes a third of the damage as
// recoil, then the target is confused if the move's chance came up.
_000:
    Call BATTLE_SUBSCRIPT_RECOIL_1_3
    CompareVarToValue OPCODE_FLAG_NOT, BTLVAR_BATTLE_CTX_STATUS, SYSCTL_APPLY_SECONDARY_EFFECT, _008
    Call BATTLE_SUBSCRIPT_CONFUSE

_008:
    End

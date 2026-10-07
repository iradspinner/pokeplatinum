#include "macros/btlcmd.inc"


// Oxide: Raging Fury in one turn (the move reworks, Ian, 2026-10-06): a hit
// that costs the user a third of the damage it deals and may confuse the
// target, on the pattern of Volt Tackle's effect (262), Reckless included.
_000:
    CheckAbility CHECK_NOT_HAVE, BTLSCR_ATTACKER, ABILITY_RECKLESS, _008
    UpdateVar OPCODE_SET, BTLVAR_POWER_MULTI, 12

_008:
    UpdateVar OPCODE_SET, BTLVAR_SIDE_EFFECT_FLAGS_INDIRECT, MOVE_SIDE_EFFECT_PROBABILISTIC|MOVE_SIDE_EFFECT_TO_DEFENDER|MOVE_SUBSCRIPT_PTR_RECOIL_1_3_CHANCE_TO_CONFUSE
    CalcCrit
    CalcDamage
    End

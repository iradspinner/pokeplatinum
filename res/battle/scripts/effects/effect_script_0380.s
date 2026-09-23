#include "macros/btlcmd.inc"


// Pollen Puff damages a foe and heals an ally. hg-engine tells the two apart
// with a command of its own; Platinum's IfSameSide does the same. The heal
// path is set up the way Present's is.
_000:
    IfSameSide BTLSCR_ATTACKER, BTLSCR_DEFENDER, _heal
    CalcCrit
    CalcDamage
    End

_heal:
    UpdateVarFromVar OPCODE_SET, BTLVAR_MSG_BATTLER_TEMP, BTLVAR_DEFENDER
    UpdateVar OPCODE_SET, BTLVAR_SIDE_EFFECT_FLAGS_DIRECT, MOVE_SIDE_EFFECT_ON_HIT|MOVE_SUBSCRIPT_PTR_POLLEN_PUFF_HEAL
    UpdateVar OPCODE_FLAG_ON, BTLVAR_BATTLE_CTX_STATUS, SYSCTL_IGNORE_IMMUNITIES
    UpdateVar OPCODE_SET, BTLVAR_MOVE_EFFECT_CHANCE, 1
    End

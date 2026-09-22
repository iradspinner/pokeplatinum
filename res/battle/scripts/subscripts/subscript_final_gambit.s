#include "macros/btlcmd.inc"


// Oxide: Final Gambit's user faints once the move has hit, the way
// Explosion's does: it sets the user's self-destructed bit and its HP to 0,
// and the controller faints it after the move. As a hit's side effect this
// does not run when the move misses or has no effect, so the user survives
// those, which is the later generations' rule.
_000:
    UpdateVar OPCODE_SET, BTLVAR_CALC_TEMP, 0x10000000
    UpdateVarFromVar OPCODE_LEFT_SHIFT, BTLVAR_CALC_TEMP, BTLVAR_ATTACKER
    UpdateVarFromVar OPCODE_FLAG_ON, BTLVAR_BATTLE_CTX_STATUS, BTLVAR_CALC_TEMP
    UpdateMonData OPCODE_SET, BTLSCR_ATTACKER, BATTLEMON_CUR_HP, 0
    UpdateVar OPCODE_SET, BTLVAR_HP_CALC_TEMP, 32767
    UpdateHealthBar BTLSCR_ATTACKER
    Wait
    End

#include "macros/btlcmd.inc"


_000:
    SetMultiHit 10, SYSCTL_TRIPLE_KICK
    UpdateVar OPCODE_SET, BTLVAR_AFTER_MOVE_MESSAGE_TYPE, AFTER_MOVE_MESSAGE_MULTI_HIT
    CalcCrit
    CalcDamage
    End

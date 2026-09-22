#include "macros/btlcmd.inc"


_000:
    CompareMonDataToValue OPCODE_EQU, BTLSCR_ATTACKER, BATTLEMON_HELD_ITEM, ITEM_NONE, _011
    UpdateVar OPCODE_SET, BTLVAR_POWER_MULTI, 10
    GoTo _015
_011:
    UpdateVar OPCODE_SET, BTLVAR_POWER_MULTI, 20
_015:
    CalcCrit
    CalcDamage
    End

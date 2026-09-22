#include "macros/btlcmd.inc"


_000:
    CompareMonDataToVar OPCODE_NEQ, BTLSCR_ATTACKER, BATTLEMON_FAKE_OUT_TURN_NUMBER, BTLVAR_TOTAL_TURNS, _fail
    CalcCrit
    CalcDamage
    End

_fail:
    UpdateVar OPCODE_FLAG_ON, BTLVAR_MOVE_STATUS_FLAGS, MOVE_STATUS_FAILED
    End

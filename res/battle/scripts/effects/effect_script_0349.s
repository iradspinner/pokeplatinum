#include "macros/btlcmd.inc"


_000:
    Random 9, 0
    CompareVarToValue OPCODE_GT, BTLVAR_CALC_TEMP, 6, _020
    UpdateVar OPCODE_SET, BTLVAR_POWER_MULTI, 10
    GoTo _024
_020:
    UpdateVar OPCODE_SET, BTLVAR_POWER_MULTI, 20
    // {0} is going all out for this attack!
    PrintMessage BattleStrings_Text_PokemonIsGoingAllOutForThisAttack_Ally, TAG_NICKNAME, BTLSCR_ATTACKER
    Wait
    WaitButtonABTime 30
_024:
    CalcCrit
    CalcDamage
    End

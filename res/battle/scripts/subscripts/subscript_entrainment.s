#include "macros/btlcmd.inc"


_000:
    UpdateMonDataFromVar OPCODE_GET, BTLSCR_ATTACKER, BATTLEMON_ABILITY, BTLVAR_CALC_TEMP
    UpdateMonDataFromVar OPCODE_SET, BTLSCR_DEFENDER, BATTLEMON_ABILITY, BTLVAR_CALC_TEMP
    // {0} acquired {1}!
    PrintMessage BattleStrings_Text_PokemonAcquiredAbility_Ally, TAG_NICKNAME_ABILITY, BTLSCR_DEFENDER, BTLSCR_DEFENDER
    Wait
    WaitButtonABTime 30
    End

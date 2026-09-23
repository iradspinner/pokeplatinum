#include "macros/btlcmd.inc"


_000:
    CompareMonDataToValue OPCODE_EQU, BTLSCR_DEFENDER, BATTLEMON_HELD_ITEM, ITEM_NONE, _017
    PrintAttackMessage
    Wait
    WaitButtonABTime 30
    // {0} is about to be attacked by its {1}!
    PrintMessage BattleStrings_Text_PokemonIsAboutToBeAttackedByItsItem_Ally, TAG_NICKNAME_ITEM, BTLSCR_DEFENDER, BTLSCR_DEFENDER
    Wait
    WaitButtonABTime 30
    CalcCrit
    CalcDamage
    End
_017:
    UpdateVar OPCODE_FLAG_ON, BTLVAR_MOVE_STATUS_FLAGS, MOVE_STATUS_FAILED
    End

#include "macros/btlcmd.inc"


_000:
    PrintAttackMessage
    Wait
    WaitButtonABTime 30
    ChangeExecutionOrderPriority BTLSCR_DEFENDER, EXECUTION_ORDER_AFTER_YOU, _018
    PlayMoveAnimation BTLSCR_ATTACKER
    Wait
    // {0} took the kind offer!
    PrintMessage BattleStrings_Text_PokemonTookTheKindOffer_Ally, TAG_NICKNAME, BTLSCR_DEFENDER
    Wait
    WaitButtonABTime 30
    End
_018:
    UpdateVar OPCODE_FLAG_ON, BTLVAR_MOVE_STATUS_FLAGS, MOVE_STATUS_FAILED
    End

#include "macros/btlcmd.inc"


// Oxide, element 7: Safety Goggles keep a powder or spore move off their
// holder (hg-engine's subscript 382).
_000:
    PrintAttackMessage
    Wait
    WaitButtonABTime 30
    UpdateVar OPCODE_FLAG_ON, BTLVAR_MOVE_STATUS_FLAGS, MOVE_STATUS_FAILED
    // {0} is protected by its {1}!
    PrintMessage BattleStrings_Text_PokemonIsProtectedByItsItem_Ally, TAG_NICKNAME_ITEM, BTLSCR_DEFENDER, BTLSCR_DEFENDER
    Wait
    WaitButtonABTime 30
    End

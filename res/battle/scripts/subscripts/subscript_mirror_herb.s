#include "macros/btlcmd.inc"


// Oxide, element 7: the Mirror Herb has copied a foe's stat rises
// (BattleSystem_TriggerMirrorHerb has already made them) and is used up.
// BTLVAR_CALC_TEMP is set when its holder's Contrary made them falls.
_000:
    PlayBattleAnimation BTLSCR_MSG_TEMP, BATTLE_ANIMATION_HELD_ITEM
    Wait
    WaitButtonABTime 15
    CompareVarToValue OPCODE_NEQ, BTLVAR_CALC_TEMP, 0, _contrary
    PlayBattleAnimation BTLSCR_MSG_TEMP, BATTLE_ANIMATION_STAT_BOOST
    Wait
    GoTo _message

_contrary:
    PlayBattleAnimation BTLSCR_MSG_TEMP, BATTLE_ANIMATION_STAT_DROP
    Wait

_message:
    // {0}’s {1} copied its foe’s stat changes!
    PrintMessage BattleStrings_Text_PokemonsItemCopiedItsFoesStatChanges_Ally, TAG_NICKNAME_ITEM, BTLSCR_MSG_TEMP, BTLSCR_MSG_TEMP
    Wait
    WaitButtonABTime 30
    RemoveItem BTLSCR_MSG_TEMP
    End

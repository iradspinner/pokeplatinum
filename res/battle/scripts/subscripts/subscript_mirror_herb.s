#include "macros/btlcmd.inc"


// Oxide, element 7: the Mirror Herb has copied a foe's stat rises
// (BattleSystem_TriggerMirrorHerb has already made them) and is used up.
_000:
    PlayBattleAnimation BTLSCR_MSG_TEMP, BATTLE_ANIMATION_HELD_ITEM
    Wait
    WaitButtonABTime 15
    PlayBattleAnimation BTLSCR_MSG_TEMP, BATTLE_ANIMATION_STAT_BOOST
    Wait
    // {0}’s {1} copied its foe’s stat changes!
    PrintMessage BattleStrings_Text_PokemonsItemCopiedItsFoesStatChanges_Ally, TAG_NICKNAME_ITEM, BTLSCR_MSG_TEMP, BTLSCR_MSG_TEMP
    Wait
    WaitButtonABTime 30
    RemoveItem BTLSCR_MSG_TEMP
    End

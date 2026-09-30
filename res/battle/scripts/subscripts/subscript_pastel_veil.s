#include "macros/btlcmd.inc"

// Oxide: Pastel Veil. The holder, BTLSCR_MSG_BATTLER_TEMP, has come in beside
// a poisoned partner, BTLSCR_SIDE_EFFECT_MON, which is cured.
_000:
    // {0} was cured of its poisoning!
    PrintMessage BattleStrings_Text_PokemonWasCuredOfItsPoisoning_Ally, TAG_NICKNAME, BTLSCR_SIDE_EFFECT_MON
    Wait
    SetHealthBoxStatusIcon BTLSCR_SIDE_EFFECT_MON, BATTLE_ANIMATION_NONE
    WaitButtonABTime 30
    UpdateMonData OPCODE_SET, BTLSCR_SIDE_EFFECT_MON, BATTLEMON_STATUS, MON_CONDITION_NONE
    End

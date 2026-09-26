#include "macros/btlcmd.inc"


// Oxide: a boss fight opens in a Wonder Room that lasts the whole battle
// (BattleSystem_TriggerEffectOnSwitch), with the move's animation and its
// own message, as subscript_overworld_trick_room opens a Trick Room.
_000:
    UpdateVar OPCODE_SET, BTLVAR_MSG_MOVE_TEMP, MOVE_WONDER_ROOM
    PlayMoveAnimation BTLSCR_MSG_TEMP
    Wait 
    UpdateVar OPCODE_SET, BTLVAR_MOVE_EFFECT_CHANCE, 0
    UpdateVar OPCODE_FLAG_OFF, BTLVAR_BATTLE_CTX_STATUS, SYSCTL_PLAYED_MOVE_ANIMATION
    // It created a bizarre area in which the Defense and Sp. Def stats are swapped!
    PrintMessage BattleStrings_Text_ItCreatedABizarreAreaInWhichTheDefenseAndSpDefStatsAreSwapped, TAG_NONE
    Wait 
    WaitButtonABTime 30
    UpdateVar OPCODE_FLAG_ON, BTLVAR_FIELD_CONDITIONS, FIELD_CONDITION_WONDER_ROOM_INIT
    End 

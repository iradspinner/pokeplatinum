#include "macros/btlcmd.inc"


// Oxide: Wonder Room. For five turns every battler's Defense and Sp. Def
// trade places in the damage calculation (BattleSystem_CalcMoveDamage), as in
// Generation 5 on. Used while the room is up, it ends the room, as Trick Room
// does; under a boss fight's permanent room it fails.
_000:
    CompareVarToValue OPCODE_FLAG_SET, BTLVAR_FIELD_CONDITIONS, FIELD_CONDITION_WONDER_ROOM_PERM, _failed
    CompareVarToValue OPCODE_FLAG_SET, BTLVAR_FIELD_CONDITIONS, FIELD_CONDITION_WONDER_ROOM, _end
    UpdateVar OPCODE_FLAG_ON, BTLVAR_FIELD_CONDITIONS, FIELD_CONDITION_WONDER_ROOM_INIT
    // It created a bizarre area in which the Defense and Sp. Def stats are swapped!
    BufferMessage BattleStrings_Text_ItCreatedABizarreAreaInWhichTheDefenseAndSpDefStatsAreSwapped, TAG_NONE
    GoTo _show

_end:
    UpdateVar OPCODE_FLAG_OFF, BTLVAR_FIELD_CONDITIONS, FIELD_CONDITION_WONDER_ROOM
    // Wonder Room wore off, and the Defense and Sp. Def stats returned to normal!
    BufferMessage BattleStrings_Text_WonderRoomWoreOffAndTheDefenseAndSpDefStatsReturnedToNormal, TAG_NONE

_show:
    UpdateVar OPCODE_SET, BTLVAR_SIDE_EFFECT_FLAGS_INDIRECT, MOVE_SIDE_EFFECT_ON_HIT|MOVE_SUBSCRIPT_PTR_PRINT_MESSAGE_AND_PLAY_ANIMATION
    End 

_failed:
    UpdateVar OPCODE_FLAG_ON, BTLVAR_MOVE_STATUS_FLAGS, MOVE_STATUS_FAILED
    End 

#include "macros/btlcmd.inc"


// Oxide: Magic Room. For five turns no held item works (Battler_HeldItem), as
// in hg-engine's script and the later games. Used while the room is up, it
// ends the room, as Trick Room does.
_000:
    CompareVarToValue OPCODE_NEQ, BTLVAR_MAGIC_ROOM_TURNS, 0, _end
    UpdateVar OPCODE_SET, BTLVAR_MAGIC_ROOM_TURNS, 5
    // It created a bizarre area in which Pokémon's held items lose their effects!
    BufferMessage BattleStrings_Text_ItCreatedABizarreAreaInWhichPokemonsHeldItemsLoseTheirEffects, TAG_NONE
    GoTo _show

_end:
    UpdateVar OPCODE_SET, BTLVAR_MAGIC_ROOM_TURNS, 0
    // Magic Room wore off, and held items' effects returned to normal!
    BufferMessage BattleStrings_Text_MagicRoomWoreOffAndHeldItemsEffectsReturnedToNormal, TAG_NONE

_show:
    UpdateVar OPCODE_SET, BTLVAR_SIDE_EFFECT_FLAGS_INDIRECT, MOVE_SIDE_EFFECT_ON_HIT|MOVE_SUBSCRIPT_PTR_PRINT_MESSAGE_AND_PLAY_ANIMATION
    End 

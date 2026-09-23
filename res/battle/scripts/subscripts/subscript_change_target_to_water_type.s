#include "macros/btlcmd.inc"


// Oxide: Soak makes the target pure Water. It fails against a substitute,
// against Arceus's Multitype and against a target that is pure Water
// already, the later games' rules; hg-engine's command only sets the type.
_000:
    CheckSubstitute BTLSCR_DEFENDER, _fail
    CheckAbility CHECK_HAVE, BTLSCR_DEFENDER, ABILITY_MULTITYPE, _fail
    CompareMonDataToValue OPCODE_NEQ, BTLSCR_DEFENDER, BATTLEMON_TYPE_1, TYPE_WATER, _soak
    CompareMonDataToValue OPCODE_EQU, BTLSCR_DEFENDER, BATTLEMON_TYPE_2, TYPE_WATER, _fail

_soak:
    Call BATTLE_SUBSCRIPT_ATTACK_MESSAGE_AND_ANIMATION
    UpdateMonData OPCODE_SET, BTLSCR_DEFENDER, BATTLEMON_TYPE_1, TYPE_WATER
    UpdateMonData OPCODE_SET, BTLSCR_DEFENDER, BATTLEMON_TYPE_2, TYPE_WATER
    // {0} transformed into the Water type!
    PrintMessage BattleStrings_Text_PokemonTransformedIntoTheWaterType_Ally, TAG_NICKNAME, BTLSCR_DEFENDER
    Wait
    WaitButtonABTime 30
    End

_fail:
    UpdateVar OPCODE_FLAG_ON, BTLVAR_MOVE_STATUS_FLAGS, MOVE_STATUS_FAILED
    End

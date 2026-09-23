#include "macros/btlcmd.inc"


// Oxide: Smack Down and Thousand Arrows ground the target after they hit,
// until it leaves the field. Built from Gravity's start subscript, which
// brings a Pokemon down the same ways: a Magnet Rise user loses it, and one in
// the air from Fly or Bounce is pulled out of the move. Nothing happens if the
// target fainted, is behind a substitute or is already on the ground, which
// Gravity, Ingrain, an Iron Ball or an earlier Smack Down all mean.
_000:
    CompareMonDataToValue OPCODE_EQU, BTLSCR_DEFENDER, BATTLEMON_CUR_HP, 0, _end
    CheckSubstitute BTLSCR_DEFENDER, _end
    CompareMonDataToValue OPCODE_FLAG_SET, BTLSCR_DEFENDER, BATTLEMON_MOVE_EFFECTS_MASK, MOVE_EFFECT_SMACKED_DOWN, _end
    CompareVarToValue OPCODE_FLAG_SET, BTLVAR_FIELD_CONDITIONS, FIELD_CONDITION_GRAVITY, _end
    CompareMonDataToValue OPCODE_FLAG_SET, BTLSCR_DEFENDER, BATTLEMON_MOVE_EFFECTS_MASK, MOVE_EFFECT_AIRBORNE, _fly
    CompareMonDataToValue OPCODE_FLAG_SET, BTLSCR_DEFENDER, BATTLEMON_MOVE_EFFECTS_MASK, MOVE_EFFECT_INGRAIN, _end
    CheckItemHoldEffect CHECK_HAVE, BTLSCR_DEFENDER, HOLD_EFFECT_SPEED_DOWN_GROUNDED, _end
    CompareMonDataToValue OPCODE_NEQ, BTLSCR_DEFENDER, BATTLEMON_MAGNET_RISE_TURNS, 0, _magnet_rise
    CompareMonDataToValue OPCODE_EQU, BTLSCR_DEFENDER, BATTLEMON_TYPE_1, TYPE_FLYING, _ground
    CompareMonDataToValue OPCODE_EQU, BTLSCR_DEFENDER, BATTLEMON_TYPE_2, TYPE_FLYING, _ground
    CheckAbility CHECK_HAVE, BTLSCR_DEFENDER, ABILITY_LEVITATE, _ground
    End

_magnet_rise:
    UpdateMonData OPCODE_SET, BTLSCR_DEFENDER, BATTLEMON_MAGNET_RISE_TURNS, 0
    GoTo _ground

_fly:
    UnlockMoveChoice BTLSCR_DEFENDER
    ToggleVanish BTLSCR_DEFENDER, FALSE
    Wait

_ground:
    UpdateMonData OPCODE_FLAG_ON, BTLSCR_DEFENDER, BATTLEMON_MOVE_EFFECTS_MASK, MOVE_EFFECT_SMACKED_DOWN
    // {0} fell straight down!
    PrintMessage BattleStrings_Text_PokemonFellStraightDown_Ally, TAG_NICKNAME, BTLSCR_DEFENDER
    Wait
    WaitButtonABTime 30

_end:
    End

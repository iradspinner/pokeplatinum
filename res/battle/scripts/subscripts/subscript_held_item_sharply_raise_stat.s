#include "macros/btlcmd.inc"


// The Starf Berry: two stages of a random stat. Oxide: the rise goes through
// ChangeStatStage as the other stat Berries' does, so Simple doubles it and
// Contrary turns it into a drop (Ian, 2026-09-28), where Platinum added the
// stages here directly. MOVE_SUBSCRIPT_PTR_RECOIL_1_3 sits just before the
// two-stage rises, as QUARTER_RECOIL does before the one-stage ones.
_000:
    PlayBattleAnimation BTLSCR_MSG_TEMP, BATTLE_ANIMATION_HELD_ITEM
    Wait
    WaitButtonABTime 15
    UpdateVar OPCODE_SET, BTLVAR_SIDE_EFFECT_PARAM, MOVE_SUBSCRIPT_PTR_RECOIL_1_3
    UpdateVarFromVar OPCODE_ADD, BTLVAR_SIDE_EFFECT_PARAM, BTLVAR_MSG_TEMP
    UpdateVar OPCODE_SET, BTLVAR_SIDE_EFFECT_TYPE, SIDE_EFFECT_TYPE_HELD_ITEM
    UpdateVarFromVar OPCODE_SET, BTLVAR_SIDE_EFFECT_MON, BTLVAR_MSG_BATTLER_TEMP
    Call BATTLE_SUBSCRIPT_UPDATE_STAT_STAGE
    Call BATTLE_SUBSCRIPT_PLUCK_CHECK
    End

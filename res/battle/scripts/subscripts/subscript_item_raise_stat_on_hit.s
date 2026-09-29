#include "macros/btlcmd.inc"


// Oxide, element 7: the Absorb Bulb and the Cell Battery, used up to raise
// their holder's stat one stage when a move of their type hits it.
// BTLVAR_MSG_TEMP holds the stat, BTLSCR_MSG_TEMP the holder. The rise goes
// through ChangeStatStage as subscript_held_item_raise_stat's does, so Simple
// and Contrary apply to it (Ian, 2026-09-28).
_000:
    PlayBattleAnimation BTLSCR_MSG_TEMP, BATTLE_ANIMATION_HELD_ITEM
    Wait
    WaitButtonABTime 15
    UpdateVar OPCODE_SET, BTLVAR_SIDE_EFFECT_PARAM, MOVE_SUBSCRIPT_PTR_QUARTER_RECOIL
    UpdateVarFromVar OPCODE_ADD, BTLVAR_SIDE_EFFECT_PARAM, BTLVAR_MSG_TEMP
    UpdateVar OPCODE_SET, BTLVAR_SIDE_EFFECT_TYPE, SIDE_EFFECT_TYPE_HELD_ITEM
    UpdateVarFromVar OPCODE_SET, BTLVAR_SIDE_EFFECT_MON, BTLVAR_MSG_BATTLER_TEMP
    Call BATTLE_SUBSCRIPT_UPDATE_STAT_STAGE
    RemoveItem BTLSCR_MSG_TEMP
    End

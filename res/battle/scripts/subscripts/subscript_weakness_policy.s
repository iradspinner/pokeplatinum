#include "macros/btlcmd.inc"


// Oxide, element 7: the Weakness Policy, used up to raise its holder's Attack
// and Sp. Atk two stages each when a supereffective move hits it (hg-engine's
// subscript 344). Each rise goes through ChangeStatStage as a held item's, so
// Simple doubles it and Contrary turns it into a drop, as in hg-engine and
// the later games (Ian, 2026-09-28); a stat already at its limit is passed
// over in silence.
_000:
    PlayBattleAnimation BTLSCR_MSG_TEMP, BATTLE_ANIMATION_HELD_ITEM
    Wait
    WaitButtonABTime 15
    UpdateVar OPCODE_SET, BTLVAR_SIDE_EFFECT_TYPE, SIDE_EFFECT_TYPE_HELD_ITEM
    UpdateVarFromVar OPCODE_SET, BTLVAR_SIDE_EFFECT_MON, BTLVAR_MSG_BATTLER_TEMP
    UpdateVar OPCODE_SET, BTLVAR_SIDE_EFFECT_PARAM, MOVE_SUBSCRIPT_PTR_ATTACK_UP_2_STAGES
    Call BATTLE_SUBSCRIPT_UPDATE_STAT_STAGE
    UpdateVar OPCODE_SET, BTLVAR_SIDE_EFFECT_PARAM, MOVE_SUBSCRIPT_PTR_SP_ATTACK_UP_2_STAGES
    Call BATTLE_SUBSCRIPT_UPDATE_STAT_STAGE
    RemoveItem BTLSCR_MSG_TEMP
    End

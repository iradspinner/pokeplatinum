#include "macros/btlanimcmd.inc"

// Oxide: Freeze Shock charges on its first turn and acts on its second. The move's
// effect chance is even on the charge turn and set to 1 for the second by
// Platinum's charge cleanup, which is how Sky Attack and Solar Beam tell the
// two turns apart. The charge is a glow on the user; the second turn is
// Ice Beam's animation, as before.
L_0:
    LoadParticleResource 0, ice_beam_spa
    JumpIfEffectChanceOdd L_charge, L_strike
    End

L_charge:
    Func_FadeBg FADE_BG_TYPE_BASE, 1, 0, 8, BATTLE_COLOR_LIGHT_BLUE
    WaitForAnimTasks
    PlaySoundEffectL SEQ_SE_DP_SHUSHU_sseq
    Func_FadeBattlerSprite BATTLE_ANIM_ATTACKER, 0, 2, BATTLE_COLOR_LIGHT_CYAN, 10, 0
    WaitForAnimTasks
    UnloadParticleSystem 0
    Func_FadeBg FADE_BG_TYPE_BASE, 1, 8, 0, BATTLE_COLOR_LIGHT_BLUE
    WaitForAnimTasks
    End

L_strike:
    Func_FadeBg FADE_BG_TYPE_BASE, 1, 0, 8, BATTLE_COLOR_LIGHT_BLUE
    WaitForAnimTasks
    CreateEmitter 0, 1, EMITTER_CB_GENERIC
    SetExtraParams 0, 2, 6, 1, 0, 0
    PlayMovingSoundEffectAtkDef SEQ_SE_DP_025_sseq, BATTLE_SOUND_PAN_LEFT, BATTLE_SOUND_PAN_RIGHT, 4, 2
    Delay 15
    CreateEmitter 0, 2, EMITTER_CB_SET_POS_TO_DEFENDER
    CreateEmitter 0, 0, EMITTER_CB_SET_POS_TO_DEFENDER
    Func_Shake 1, 0, 1, 2, BATTLE_ANIM_BATTLER_SPRITE_DEFENDER
    WaitForAllEmitters
    UnloadParticleSystem 0
    Func_FadeBg FADE_BG_TYPE_BASE, 1, 8, 0, BATTLE_COLOR_LIGHT_BLUE
    WaitForAnimTasks
    End

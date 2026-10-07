#include "macros/btlanimcmd.inc"

// Oxide: Dig strikes in one turn since the move reworks (Ian, 2026-10-06),
// so only the strike is played, without the rise from underground that
// followed the old turn spent digging.
L_0:
    LoadParticleResource 0, dig_spa
    LoadParticleResource 1, pound_spa
    CreateEmitter 0, 0, EMITTER_CB_GENERIC
    SetExtraParams 0, 1, 5, 0, 0, 0
    SetExtraParams 1, 0, -688, 0
    CreateEmitter 0, 3, EMITTER_CB_GENERIC
    SetExtraParams 0, 1, 5, 0, 0, 0
    SetExtraParams 1, 0, -688, 0
    PlaySoundEffectL SEQ_SE_DP_W091_sseq
    Delay 2
    CreateEmitter 0, 1, EMITTER_CB_GENERIC
    SetExtraParams 0, 1, 5, 0, 0, 0
    SetExtraParams 1, 0, -688, 0
    CreateEmitter 0, 3, EMITTER_CB_GENERIC
    SetExtraParams 0, 1, 5, 0, 0, 0
    SetExtraParams 1, 0, -688, 0
    PlaySoundEffectL SEQ_SE_DP_W091_sseq
    Delay 2
    CreateEmitter 0, 2, EMITTER_CB_GENERIC
    SetExtraParams 0, 1, 5, 0, 0, 0
    SetExtraParams 1, 0, -688, 0
    CreateEmitter 0, 3, EMITTER_CB_GENERIC
    SetExtraParams 0, 1, 5, 0, 0, 0
    SetExtraParams 1, 0, -688, 0
    PlaySoundEffectL SEQ_SE_DP_W091_sseq
    Delay 5
    PlaySoundEffectR SEQ_SE_DP_030_sseq
    CreateEmitter 1, 1, EMITTER_CB_SET_POS_TO_DEFENDER
    CreateEmitter 1, 0, EMITTER_CB_SET_POS_TO_DEFENDER
    Func_Shake 1, 0, 1, 2, BATTLE_ANIM_BATTLER_SPRITE_DEFENDER
    WaitForAnimTasks
    Func_HideBattler BATTLE_ANIM_ATTACKER, FALSE
    WaitForAllEmitters
    UnloadParticleSystem 0
    UnloadParticleSystem 1
    End

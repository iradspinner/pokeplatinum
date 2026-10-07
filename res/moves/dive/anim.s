#include "macros/btlanimcmd.inc"

// Oxide: Dive strikes in one turn since the move reworks (Ian, 2026-10-06),
// so only the strike is played.
L_0:
    LoadParticleResource 0, dive_spa
    PlayLoopedSoundEffectR SEQ_SE_DP_W291_sseq, 3, 4
    CreateEmitter 0, 1, EMITTER_CB_GENERIC
    SetExtraParams 0, 2, 5, 0, 0, 0
    SetExtraParams 1, 0, -3440, 0
    CreateEmitter 0, 0, EMITTER_CB_GENERIC
    SetExtraParams 0, 2, 5, 0, 0, 0
    SetExtraParams 1, 0, -3440, 0
    CreateEmitter 0, 2, EMITTER_CB_GENERIC
    SetExtraParams 0, 2, 5, 0, 0, 0
    SetExtraParams 1, 0, -3440, 0
    Func_Shake 2, 0, 1, 2, BATTLE_ANIM_BATTLER_SPRITE_DEFENDER
    Delay 15
    Func_HideBattler BATTLE_ANIM_ATTACKER, FALSE
    WaitForAllEmitters
    UnloadParticleSystem 0
    End

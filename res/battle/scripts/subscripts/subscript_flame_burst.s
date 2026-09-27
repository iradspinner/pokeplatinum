#include "macros/btlcmd.inc"


// Oxide: Flame Burst's burst hits the target's partner for a sixteenth of
// its maximum HP (BattleControllerPlayer_TriggerAfterMoveHitEffects sets the
// battler and the amount), as hg-engine's subscript does.
_000:
    PlayMoveHitSound BTLSCR_MSG_TEMP
    FlickerMon BTLSCR_MSG_TEMP
    Wait 
    // The bursting flame hit {0}!
    PrintMessage BattleStrings_Text_TheBurstingFlameHitPokemon_Ally, TAG_NICKNAME, BTLSCR_MSG_TEMP
    Wait 
    WaitButtonABTime 30
    UpdateVar OPCODE_FLAG_ON, BTLVAR_BATTLE_CTX_STATUS, SYSCTL_SKIP_SPRITE_BLINK
    Call BATTLE_SUBSCRIPT_UPDATE_HP
    End 

#include "macros/btlcmd.inc"


// Oxide: Toxic Debris. BattleSystem_TriggerAbilityOnHit has already laid a
// layer of Toxic Spikes on its holder's other side; this only says so.
_000:
    // Poison spikes were scattered all around your team’s feet!
    PrintMessage BattleStrings_Text_PoisonSpikesWereScatteredAllAroundYourTeamsFeet, TAG_NONE_SIDE_CONSCIOUS, BTLSCR_DEFENDER_ENEMY
    Wait 
    WaitButtonABTime 30
    End 

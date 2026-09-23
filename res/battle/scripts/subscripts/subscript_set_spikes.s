#include "macros/btlcmd.inc"


// Oxide: Ceaseless Edge lays a layer of Spikes on the target's side after it
// hits, with Spikes' own check and message. As for Stone Axe, hg-engine's
// hazard queue is left out.
_000:
    TrySpikes _end
    // Spikes were scattered all around your team’s feet!
    PrintMessage BattleStrings_Text_SpikesWereScatteredAllAroundYourTeamsFeet, TAG_NONE_SIDE_CONSCIOUS, BTLSCR_ATTACKER_ENEMY
    Wait
    WaitButtonABTime 30

_end:
    End

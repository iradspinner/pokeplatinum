#include "macros/btlcmd.inc"


// Oxide: Neutralizing Gas's switch-in message. The suppression itself is
// worked out in Battler_Ability.
_000:
    // Neutralizing gas filled the area!
    PrintMessage BattleStrings_Text_NeutralizingGasFilledTheArea, TAG_NONE
    Wait 
    WaitButtonABTime 30
    End 

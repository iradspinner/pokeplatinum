#include "macros/btlcmd.inc"


// Oxide: the gas is gone, its last holder having fainted, left the field or
// been hit by Gastro Acid. The switch-in abilities it held back announce
// themselves after this, from BattleSystem_TriggerEffectOnSwitch.
_000:
    // The effects of the neutralizing gas wore off!
    PrintMessage BattleStrings_Text_TheEffectsOfTheNeutralizingGasWoreOff, TAG_NONE
    Wait 
    WaitButtonABTime 30
    End 

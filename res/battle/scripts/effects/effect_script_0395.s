#include "macros/btlcmd.inc"


// Oxide: Dragon Tail and Circle Throw. The drag is not set here as a side
// effect: the side-effect state runs before the target's ability answers
// the hit, so the Pokemon dragged in answered in its place.
// BattleControllerPlayer_AfterMoveEffects runs subscript_force_switch_hit
// once the target's ability and held items have answered.
_000:
    CalcCrit
    CalcDamage
    End

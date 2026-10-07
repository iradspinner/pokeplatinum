#include "macros/btlcmd.inc"


// Oxide: Burning Jealousy (the move reworks, Ian, 2026-10-06). It burns only
// a target one of whose stats rose this turn (the target's statRaised turn
// flag), at the move's 100% chance; otherwise it is a plain hit. A move that
// hits both foes runs this once for each, so each is judged alone.
_000:
    IfTurnFlag BTLSCR_DEFENDER, TURN_FLAG_STAT_RAISED, FALSE, _hit
    UpdateVar OPCODE_SET, BTLVAR_SIDE_EFFECT_FLAGS_INDIRECT, MOVE_SIDE_EFFECT_TO_DEFENDER|MOVE_SUBSCRIPT_PTR_BURN

_hit:
    CalcCrit
    CalcDamage
    End

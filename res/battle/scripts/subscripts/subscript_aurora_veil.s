#include "macros/btlcmd.inc"


// Oxide: Aurora Veil, in the shape of Reflect's subscript. hg-engine's own
// runs its failure checks before the move, in C Platinum does not have, so
// TryAuroraVeil makes them and jumps on failure as TryReflect does.
_000:
    TryAuroraVeil _end
    Call BATTLE_SUBSCRIPT_ANIMATION_PREPARED_MESSAGE

_end:
    End

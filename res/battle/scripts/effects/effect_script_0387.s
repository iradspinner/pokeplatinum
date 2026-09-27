#include "macros/btlcmd.inc"


// Steel Roller. hg-engine hits and then ends the terrain in C, and fails
// before the hit when there is none. Oxide has no terrain (Ian, 2026-09-27),
// so the move is kept as a plain hit that never fails: with nothing to end,
// ending the terrain after the hit is nothing to do.
_000:
    CalcCrit
    CalcDamage
    End

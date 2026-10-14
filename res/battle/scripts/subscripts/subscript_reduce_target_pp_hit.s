#include "macros/btlcmd.inc"


// Oxide: Eerie Spell's drain, once its hit has landed (effect_script_0421).
// Spite's own command finds the target's last used move and takes its PP:
// 3 here where Spite takes 4, never below 0, and the copy of a Transform or
// Mimic loses the PP, as with Spite. A target with no last move (it has not
// moved since it came in, or could not move last turn), or whose last move
// has no PP left or is no longer among its moves (Mimic, Sketch), loses
// nothing, and nothing is printed, since the hit itself worked.
_000:
    TrySpite _end
    // It reduced the PP of {0}’s {1} by {2}!
    PrintMessage BattleStrings_Text_ItReducedThePPOfPokemonsMoveByX_Ally, TAG_NICKNAME_MOVE_NUMBER, BTLSCR_DEFENDER, BTLSCR_MSG_TEMP, BTLSCR_MSG_TEMP
    Wait
    WaitButtonABTime 30

_end:
    End

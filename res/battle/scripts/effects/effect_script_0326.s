#include "macros/btlcmd.inc"


// Oxide: Sticky Web, laid as Spikes are. hg-engine's script, without its
// hazard queue, which Oxide leaves out as it does for Stone Axe.
_000:
    TryStickyWeb _failed
    // A sticky web has been laid out on the ground on your side!
    BufferMessage BattleStrings_Text_AStickyWebHasBeenLaidOutOnYourSide, TAG_NONE_SIDE_CONSCIOUS, BTLSCR_ATTACKER_ENEMY
    UpdateVar OPCODE_SET, BTLVAR_SIDE_EFFECT_FLAGS_INDIRECT, MOVE_SIDE_EFFECT_ON_HIT|MOVE_SUBSCRIPT_PTR_PRINT_MESSAGE_AND_PLAY_ANIMATION
    End

_failed:
    UpdateVar OPCODE_FLAG_ON, BTLVAR_MOVE_STATUS_FLAGS, MOVE_STATUS_FAILED
    End

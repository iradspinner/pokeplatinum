#include "macros/btlcmd.inc"


// Oxide: Teatime. Every battler on the field that holds a Berry eats it at
// once, in speed order, whether or not it would trigger by itself, as a
// Berry that Pluck steals does; hg-engine has no code for it. It fails when
// no battler holds a Berry. TryTeatime reads each Berry as Pluck's command
// does; the subscript it names enacts the Berry and takes it away, and a
// Berry with nothing to enact is taken away here.
_000:
    TryTeatime TEATIME_CHECK, _fail
    Call BATTLE_SUBSCRIPT_ATTACK_MESSAGE_AND_ANIMATION
    // It's teatime! Everyone dug in to their Berries!
    PrintMessage BattleStrings_Text_ItsTeatimeEveryoneDugInToTheirBerries, TAG_NONE
    Wait 
    WaitButtonABTime 30

_next:
    TryTeatime TEATIME_NEXT, _end
    CompareVarToValue OPCODE_EQU, BTLVAR_SCRIPT_TEMP, 0, _no_effect
    CallFromVar BTLVAR_SCRIPT_TEMP
    GoTo _next

_no_effect:
    RemoveItem BTLSCR_MSG_TEMP
    GoTo _next

_fail:
    PrintAttackMessage 
    Wait 
    WaitButtonABTime 30
    Call BATTLE_SUBSCRIPT_BUT_IT_FAILED
    UpdateVar OPCODE_FLAG_ON, BTLVAR_MOVE_STATUS_FLAGS, MOVE_STATUS_NO_MORE_WORK

_end:
    End 

#include "macros/scrcmd.inc"


@ Platinum Oxide: the base ROM's Battleground has no init script at all. Its
@ first byte is the terminator, and FieldSystem_GetFixedInitScriptID and
@ FieldSystem_GetFrameTableInitScriptID both stop there and return 0xffff, so
@ nothing runs on transition or on frame any more. Vanilla ran script 4 on
@ transition and consulted a frame table on VAR_BATTLEGROUND_STATE.
@
@ The base ROM's member is 54 bytes: the terminator followed by 53 bytes of the
@ old table, which DSPRE left in place rather than truncating. Those bytes are
@ unreachable, so they are not reproduced here and this file builds to 4 bytes
@ instead. That is the one place the Battleground's init script deliberately
@ differs from the base ROM.

    InitScriptEntryEnd

    InitScriptEnd

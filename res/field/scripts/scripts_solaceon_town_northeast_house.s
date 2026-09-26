#include "macros/scrcmd.inc"
#include "res/text/bank/solaceon_town_northeast_house.h"


    ScriptEntry SolaceonTownNortheastHouse_PokemonBreederF
    ScriptEntry SolaceonTownNortheastHouse_Cowgirl
    ScriptEntryEnd

@ Oxide: the gift clown that stood here is gone (Ian, 2026-09-27; the encounter track's
@ clown-replacements.md): its object, its script entry and its lines, with the
@ orphaned pick-menu names. Where the town had no other capture, new grass
@ outside takes its place.

SolaceonTownNortheastHouse_PokemonBreederF:
    PlaySE SE_CONFIRM_sseq_3
    LockAll
    FacePlayer
    GetFirstNonEggInParty VAR_RESULT
    GetPartyMonNature VAR_0x8004, VAR_RESULT
    BufferNatureName 0, VAR_0x8004
    Message SolaceonTownNortheastHouse_Text_YourPokemonHasThisNature
    WaitButton
    CloseMessage
    ReleaseAll
    End

SolaceonTownNortheastHouse_Cowgirl:
    NPCMessage SolaceonTownNortheastHouse_Text_ThisAreaHadManyPokemon
    End


    .balign 4, 0

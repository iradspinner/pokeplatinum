#include "macros/scrcmd.inc"
#include "res/text/bank/solaceon_town_northeast_house.h"


    ScriptEntry SolaceonTownNortheastHouse_PokemonBreederF
    ScriptEntry SolaceonTownNortheastHouse_Cowgirl
    ScriptEntry SolaceonTownNortheastHouse_Clown
    ScriptEntryEnd

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

SolaceonTownNortheastHouse_Clown:
    PlaySE SE_CONFIRM_sseq_3
    LockAll
    FacePlayer
    Message SolaceonTownNortheastHouse_Text_WouldYouLikeOneOfThesePokemon
    ShowYesNoMenu VAR_0x800C
    GoToIfEq VAR_0x800C, 0, SolaceonTownNortheastHouse_PickAGift
    GoToIfEq VAR_0x800C, 1, SolaceonTownNortheastHouse_Declined
    GoTo SolaceonTownNortheastHouse_Declined

SolaceonTownNortheastHouse_PickAGift:
    GetRandom VAR_0x800C, 3
    GoToIfEq VAR_0x800C, 0, SolaceonTownNortheastHouse_GiveNatu
    GoToIfEq VAR_0x800C, 1, SolaceonTownNortheastHouse_GiveTrapinch
    GoToIfEq VAR_0x800C, 2, SolaceonTownNortheastHouse_GiveClamperl
    End

SolaceonTownNortheastHouse_Declined:
    Message SolaceonTownNortheastHouse_Text_SeeYa
    WaitButton
    CloseMessage
    ReleaseAll
    End

SolaceonTownNortheastHouse_GiveNatu:
    CloseMessage
    GetPartyCount VAR_0x800C
    GoToIfEq VAR_0x800C, 6, SolaceonTownNortheastHouse_PartyIsFull
    PlayFanfare SEQ_FANFA4_sseq
    WaitFanfare
    GivePokemon SPECIES_LUNATONE, 30, 0, VAR_0x800C
    Message SolaceonTownNortheastHouse_Text_SeeYa
    CloseMessage
    ReleaseAll
    End

SolaceonTownNortheastHouse_GiveTrapinch:
    CloseMessage
    GetPartyCount VAR_0x800C
    GoToIfEq VAR_0x800C, 6, SolaceonTownNortheastHouse_PartyIsFull
    PlayFanfare SEQ_FANFA4_sseq
    WaitFanfare
    GivePokemon SPECIES_TRAPINCH, 30, 0, VAR_0x800C
    Message SolaceonTownNortheastHouse_Text_SeeYa
    CloseMessage
    ReleaseAll
    End

SolaceonTownNortheastHouse_GiveClamperl:
    CloseMessage
    GetPartyCount VAR_0x800C
    GoToIfEq VAR_0x800C, 6, SolaceonTownNortheastHouse_PartyIsFull
    PlayFanfare SEQ_FANFA4_sseq
    WaitFanfare
    GivePokemon SPECIES_SOLROCK, 30, 0, VAR_0x800C
    Message SolaceonTownNortheastHouse_Text_SeeYa
    CloseMessage
    ReleaseAll
    End

SolaceonTownNortheastHouse_PartyIsFull:
    Message SolaceonTownNortheastHouse_Text_YourPartyIsFull
    WaitButton
    CloseMessage
    ReleaseAll
    End

    .balign 4, 0

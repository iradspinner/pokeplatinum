#include "macros/scrcmd.inc"
#include "res/text/bank/floaroma_meadow_house.h"


    ScriptEntry FloaromaMeadowHouse_Hiker
    ScriptEntry FloaromaMeadowHouse_NinjaBoy
    ScriptEntry FloaromaMeadowHouse_Clown
    ScriptEntryEnd

FloaromaMeadowHouse_Hiker:
    NPCMessage FloaromaMeadowHouse_Text_FlowersInTheFieldsAreSpecial
    End

FloaromaMeadowHouse_NinjaBoy:
    NPCMessage FloaromaMeadowHouse_Text_RustlingTreeOftenRarePokemon
    End

FloaromaMeadowHouse_Clown:
    PlaySE SE_CONFIRM_sseq_3
    LockAll
    FacePlayer
    Message FloaromaMeadowHouse_Text_WouldYouLikeOneOfThesePokemon
    ShowYesNoMenu VAR_0x800C
    GoToIfEq VAR_0x800C, 0, FloaromaMeadowHouse_PickAGift
    GoToIfEq VAR_0x800C, 1, FloaromaMeadowHouse_Declined
    GoTo FloaromaMeadowHouse_Declined

FloaromaMeadowHouse_GiveCombee:
    CloseMessage
    GetPartyCount VAR_0x800C
    GoToIfEq VAR_0x800C, 6, FloaromaMeadowHouse_PartyIsFull
    PlayFanfare SEQ_FANFA4_sseq
    WaitFanfare
    GivePokemon SPECIES_COMBEE, 18, 0, VAR_0x800C
    Message FloaromaMeadowHouse_Text_SeeYa
    CloseMessage
    ReleaseAll
    End

FloaromaMeadowHouse_GiveCherubi:
    CloseMessage
    GetPartyCount VAR_0x800C
    GoToIfEq VAR_0x800C, 6, FloaromaMeadowHouse_PartyIsFull
    PlayFanfare SEQ_FANFA4_sseq
    WaitFanfare
    GivePokemon SPECIES_CHERUBI, 18, 0, VAR_0x800C
    Message FloaromaMeadowHouse_Text_SeeYa
    CloseMessage
    ReleaseAll
    End

FloaromaMeadowHouse_GivePachirisu:
    CloseMessage
    GetPartyCount VAR_0x800C
    GoToIfEq VAR_0x800C, 6, FloaromaMeadowHouse_PartyIsFull
    PlayFanfare SEQ_FANFA4_sseq
    WaitFanfare
    GivePokemon SPECIES_PACHIRISU, 18, 0, VAR_0x800C
    Message FloaromaMeadowHouse_Text_SeeYa
    CloseMessage
    ReleaseAll
    End

FloaromaMeadowHouse_Declined:
    Message FloaromaMeadowHouse_Text_SeeYa
    WaitButton
    CloseMessage
    ReleaseAll
    End

FloaromaMeadowHouse_PartyIsFull:
    Message FloaromaMeadowHouse_Text_YourPartyIsFull
    WaitButton
    CloseMessage
    ReleaseAll
    End

FloaromaMeadowHouse_PickAGift:
    GetRandom VAR_0x800C, 3
    GoToIfEq VAR_0x800C, 0, FloaromaMeadowHouse_GiveCombee
    GoToIfEq VAR_0x800C, 1, FloaromaMeadowHouse_GiveCherubi
    GoToIfEq VAR_0x800C, 2, FloaromaMeadowHouse_GivePachirisu
    End

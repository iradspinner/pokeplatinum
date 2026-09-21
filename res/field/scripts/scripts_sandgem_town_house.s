#include "macros/scrcmd.inc"
#include "res/text/bank/sandgem_town_house.h"


    ScriptEntry SandgemTownHouse_BreederM
    ScriptEntry SandgemTownHouse_BreederF
    ScriptEntry SandgemTownHouse_Clown
    ScriptEntryEnd

SandgemTownHouse_BreederM:
    NPCMessage SandgemTownHouse_Text_GrowStrongerFromBattling
    End

SandgemTownHouse_BreederF:
    NPCMessage SandgemTownHouse_Text_GoodTrainerTakesCare
    End

SandgemTownHouse_Clown:
    PlaySE SE_CONFIRM_sseq_3
    LockAll
    FacePlayer
    GoToIfSet FLAG_RECEIVED_SANDGEM_TOWN_HOUSE_GIFT, SandgemTownHouse_Declined
    Message SandgemTownHouse_Text_WouldYouLikeOneOfThesePokemon
    ShowYesNoMenu VAR_RESULT
    GoToIfEq VAR_RESULT, MENU_NO, SandgemTownHouse_Declined
    GetRandom VAR_0x800C, 3
    SetVarFromVar VAR_0x8008, VAR_0x800C
    GoToIfEq VAR_0x8008, 0, SandgemTownHouse_GivePichu
    GoToIfEq VAR_0x8008, 1, SandgemTownHouse_GiveGrubbin
    GoToIfEq VAR_0x8008, 2, SandgemTownHouse_GiveFletchling
    GoTo SandgemTownHouse_Declined

SandgemTownHouse_GivePichu:
    CloseMessage
    GetPartyCount VAR_0x800C
    GoToIfEq VAR_0x800C, 6, SandgemTownHouse_PartyIsFull
    PlayFanfare SEQ_FANFA4_sseq
    WaitFanfare
    GivePokemon SPECIES_PICHU, 5, 0, VAR_0x800C
    SetFlag FLAG_RECEIVED_SANDGEM_TOWN_HOUSE_GIFT
    Message SandgemTownHouse_Text_SeeYa
    CloseMessage
    ReleaseAll
    End

SandgemTownHouse_GiveGrubbin:
    CloseMessage
    GetPartyCount VAR_0x800C
    GoToIfEq VAR_0x800C, 6, SandgemTownHouse_PartyIsFull
    PlayFanfare SEQ_FANFA4_sseq
    WaitFanfare
    GivePokemon SPECIES_GRUBBIN, 5, 0, VAR_0x800C
    SetFlag FLAG_RECEIVED_SANDGEM_TOWN_HOUSE_GIFT
    Message SandgemTownHouse_Text_SeeYa
    CloseMessage
    ReleaseAll
    End

SandgemTownHouse_GiveFletchling:
    CloseMessage
    GetPartyCount VAR_0x800C
    GoToIfEq VAR_0x800C, 6, SandgemTownHouse_PartyIsFull
    PlayFanfare SEQ_FANFA4_sseq
    WaitFanfare
    GivePokemon SPECIES_FLETCHLING, 5, 0, VAR_0x800C
    SetFlag FLAG_RECEIVED_SANDGEM_TOWN_HOUSE_GIFT
    Message SandgemTownHouse_Text_SeeYa
    CloseMessage
    ReleaseAll
    End

SandgemTownHouse_Declined:
    Message SandgemTownHouse_Text_SeeYa
    WaitButton
    CloseMessage
    ReleaseAll
    End

SandgemTownHouse_PartyIsFull:
    Message SandgemTownHouse_Text_YourPartyIsFull
    WaitButton
    CloseMessage
    ReleaseAll
    End

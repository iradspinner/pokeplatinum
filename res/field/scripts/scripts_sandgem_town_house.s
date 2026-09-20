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
    Message SandgemTownHouse_Text_WouldYouLikeOneOfThesePokemon
    InitLocalTextListMenu 1, 1, 0, VAR_0x800C, 1
    AddListMenuEntry SandgemTownHouse_Text_Venonat, 0
    AddListMenuEntry SandgemTownHouse_Text_Ekans, 1
    AddListMenuEntry SandgemTownHouse_Text_Gulpin, 2
    ShowListMenu
    SetVarFromVar VAR_0x8008, VAR_0x800C
    GoToIfEq VAR_0x8008, 0, SandgemTownHouse_GiveVenonat
    GoToIfEq VAR_0x8008, 1, SandgemTownHouse_GiveEkans
    GoToIfEq VAR_0x8008, 2, SandgemTownHouse_GiveGulpin
    GoTo SandgemTownHouse_Declined

SandgemTownHouse_GiveVenonat:
    CloseMessage
    GetPartyCount VAR_0x800C
    GoToIfEq VAR_0x800C, 6, SandgemTownHouse_PartyIsFull
    PlayFanfare SEQ_FANFA4_sseq
    WaitFanfare
    GivePokemon SPECIES_VENONAT, 5, 0, VAR_0x800C
    Message SandgemTownHouse_Text_SeeYa
    CloseMessage
    ReleaseAll
    End

SandgemTownHouse_GiveEkans:
    CloseMessage
    GetPartyCount VAR_0x800C
    GoToIfEq VAR_0x800C, 6, SandgemTownHouse_PartyIsFull
    PlayFanfare SEQ_FANFA4_sseq
    WaitFanfare
    GivePokemon SPECIES_EKANS, 5, 0, VAR_0x800C
    Message SandgemTownHouse_Text_SeeYa
    CloseMessage
    ReleaseAll
    End

SandgemTownHouse_GiveGulpin:
    CloseMessage
    GetPartyCount VAR_0x800C
    GoToIfEq VAR_0x800C, 6, SandgemTownHouse_PartyIsFull
    PlayFanfare SEQ_FANFA4_sseq
    WaitFanfare
    GivePokemon SPECIES_GULPIN, 5, 0, VAR_0x800C
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

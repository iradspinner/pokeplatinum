#include "macros/scrcmd.inc"
#include "res/text/bank/oreburgh_city_middle_house.h"


    ScriptEntry OreburghCityMiddleHouse_SchoolKidF
    ScriptEntry OreburghCityMiddleHouse_Hiker
    ScriptEntry OreburghCityMiddleHouse_Clown
    ScriptEntryEnd

OreburghCityMiddleHouse_SchoolKidF:
    NPCMessage OreburghCityMiddleHouse_Text_RoarkUsesRockTypePokemon
    End

OreburghCityMiddleHouse_Hiker:
    NPCMessage OreburghCityMiddleHouse_Text_RoarkIsOurTownsGymLeader
    End

OreburghCityMiddleHouse_Clown:
    PlaySE SE_CONFIRM_sseq_3
    LockAll
    FacePlayer
    Message OreburghCityMiddleHouse_Text_WouldYouLikeAGiftPokemon
    ShowYesNoMenu VAR_0x800C
    GoToIfEq VAR_0x800C, 0, OreburghCityMiddleHouse_PickAGift
    GoToIfEq VAR_0x800C, 1, OreburghCityMiddleHouse_Declined
    GoTo OreburghCityMiddleHouse_Declined

OreburghCityMiddleHouse_PickAGift:
    GetRandom VAR_0x800C, 3
    GoToIfEq VAR_0x800C, 0, OreburghCityMiddleHouse_GiveOddish
    GoToIfEq VAR_0x800C, 1, OreburghCityMiddleHouse_GiveBellsprout
    GoToIfEq VAR_0x800C, 2, OreburghCityMiddleHouse_GiveCacnea
    End

OreburghCityMiddleHouse_Declined:
    Message OreburghCityMiddleHouse_Text_SeeYa
    WaitButton
    CloseMessage
    ReleaseAll
    End

OreburghCityMiddleHouse_GiveOddish:
    CloseMessage
    GetPartyCount VAR_0x800C
    GoToIfEq VAR_0x800C, 6, OreburghCityMiddleHouse_PartyIsFull
    PlayFanfare SEQ_FANFA4_sseq
    WaitFanfare
    GivePokemon SPECIES_ODDISH, 15, 0, VAR_0x800C
    Message OreburghCityMiddleHouse_Text_SeeYa
    CloseMessage
    ReleaseAll
    End

OreburghCityMiddleHouse_GiveBellsprout:
    CloseMessage
    GetPartyCount VAR_0x800C
    GoToIfEq VAR_0x800C, 6, OreburghCityMiddleHouse_PartyIsFull
    PlayFanfare SEQ_FANFA4_sseq
    WaitFanfare
    GivePokemon SPECIES_BELLSPROUT, 15, 0, VAR_0x800C
    Message OreburghCityMiddleHouse_Text_SeeYa
    CloseMessage
    ReleaseAll
    End

OreburghCityMiddleHouse_GiveCacnea:
    CloseMessage
    GetPartyCount VAR_0x800C
    GoToIfEq VAR_0x800C, 6, OreburghCityMiddleHouse_PartyIsFull
    PlayFanfare SEQ_FANFA4_sseq
    WaitFanfare
    GivePokemon SPECIES_CACNEA, 15, 0, VAR_0x800C
    Message OreburghCityMiddleHouse_Text_SeeYa
    CloseMessage
    ReleaseAll
    End

OreburghCityMiddleHouse_PartyIsFull:
    Message OreburghCityMiddleHouse_Text_YourPartyIsFull
    WaitButton
    CloseMessage
    ReleaseAll
    End

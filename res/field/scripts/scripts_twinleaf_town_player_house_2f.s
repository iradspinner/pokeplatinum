#include "macros/scrcmd.inc"
#include "res/text/bank/twinleaf_town_player_house_2f.h"
#include "res/field/events/events_twinleaf_town_player_house_2f.h"


    ScriptEntry TwinleafTownPlayerHouse2F_Wii
    ScriptEntry TwinleafTownPlayerHouse2F_PC
    ScriptEntry TwinleafTownPlayerHouse2F_OnFrame_ConcludeSpecialProgram
    ScriptEntry TwinleafTownPlayerHouse2F_ScrollingSignpost
    ScriptEntry TwinleafTownPlayerHouse2F_OnTransition
    ScriptEntry TwinleafTownPlayerHouse2F_TV
    ScriptEntry TwinleafTownPlayerHouse2F_CoordEvent_RivalNorth
    ScriptEntry TwinleafTownPlayerHouse2F_CoordEvent_RivalWest
    ScriptEntry TwinleafTownPlayerHouse2F_CoordEvent_RivalEast
    ScriptEntry TwinleafTownPlayerHouse2F_CoordEvent_RivalSouth
#ifdef OXIDE_TESTKIT
    ScriptEntry TestKit_Helper
#endif
    ScriptEntryEnd

TwinleafTownPlayerHouse2F_OnTransition:
    GoToIfEq VAR_PLAYER_HOUSE_SPECIAL_PROGRAM_STATE, 0, TwinleafTownPlayerHouse2F_SetVolumeForTV
    End

TwinleafTownPlayerHouse2F_SetVolumeForTV:
    SetInitialVolumeForSequence SEQ_TV_HOUSOU_sseq, 50
    End

TwinleafTownPlayerHouse2F_OnFrame_ConcludeSpecialProgram:
    LockAll
    SetVar VAR_PLAYER_HOUSE_SPECIAL_PROGRAM_STATE, 1
    Message TwinleafTownPlayerHouse2F_Text_ConcludesSpecialProgram
    PlayFanfare SEQ_TV_END_sseq
    Message TwinleafTownPlayerHouse2F_Text_SeeYouNextWeek
    WaitFanfare
    CloseMessage
    PlayDefaultMusic
    ReleaseAll
    End

TwinleafTownPlayerHouse2F_Wii:
    EventMessage TwinleafTownPlayerHouse2F_Text_ItsAWii
    End

TwinleafTownPlayerHouse2F_PC:
    PlaySE SE_CONFIRM_sseq_3
    LockAll
    BufferPlayerName 0
    Message TwinleafTownPlayerHouse2F_Text_PCPokemonBasics
    WaitButton
    CloseMessage
    ReleaseAll
    End

TwinleafTownPlayerHouse2F_ScrollingSignpost:
    ShowScrollingSign TwinleafTownPlayerHouse2F_Text_XButtonOpensMenu
    End

TwinleafTownPlayerHouse2F_TV:
    EventMessage TwinleafTownPlayerHouse2F_Text_MomBoughtTVAsGift
    End

TwinleafTownPlayerHouse2F_CoordEvent_RivalNorth:
    SetVar VAR_MAP_LOCAL_0x00, 0
    GoTo TwinleafTownPlayerHouse2F_Rival
    End

TwinleafTownPlayerHouse2F_CoordEvent_RivalWest:
    SetVar VAR_MAP_LOCAL_0x00, 1
    GoTo TwinleafTownPlayerHouse2F_Rival
    End

TwinleafTownPlayerHouse2F_CoordEvent_RivalEast:
    SetVar VAR_MAP_LOCAL_0x00, 2
    GoTo TwinleafTownPlayerHouse2F_Rival
    End

TwinleafTownPlayerHouse2F_CoordEvent_RivalSouth:
    SetVar VAR_MAP_LOCAL_0x00, 3
    GoTo TwinleafTownPlayerHouse2F_Rival
    End

TwinleafTownPlayerHouse2F_Rival:
    LockAll
    ClearFlag FLAG_HIDE_TWINLEAF_TOWN_PLAYER_HOUSE_2F_RIVAL
    AddObject LOCALID_RIVAL
    ApplyMovement LOCALID_RIVAL, TwinleafTownPlayerHouse2F_Movement_RivalEnterRoom
    WaitMovement
    Common_SetRivalBGM
    BufferRivalName 0
    Message TwinleafTownPlayerHouse2F_Text_ThereYouAre
    CloseMessage
    CallIfEq VAR_MAP_LOCAL_0x00, 0, TwinleafTownPlayerHouse2F_RivalApproachPlayerNorth
    CallIfEq VAR_MAP_LOCAL_0x00, 1, TwinleafTownPlayerHouse2F_RivalApproachPlayerWest
    CallIfEq VAR_MAP_LOCAL_0x00, 2, TwinleafTownPlayerHouse2F_RivalApproachPlayerEast
    CallIfEq VAR_MAP_LOCAL_0x00, 3, TwinleafTownPlayerHouse2F_RivalApproachPlayerSouth
    BufferPlayerName 1
    Message TwinleafTownPlayerHouse2F_Text_ProfRowanWouldGivePokemon
    CloseMessage
    ApplyMovement LOCALID_RIVAL, TwinleafTownPlayerHouse2F_Movement_RivalExclamationMark
    WaitMovement
    CallIfEq VAR_MAP_LOCAL_0x00, 0, TwinleafTownPlayerHouse2F_RivalApproachPCNorth
    CallIfEq VAR_MAP_LOCAL_0x00, 1, TwinleafTownPlayerHouse2F_RivalApproachPCWest
    CallIfEq VAR_MAP_LOCAL_0x00, 2, TwinleafTownPlayerHouse2F_RivalApproachPCEast
    CallIfEq VAR_MAP_LOCAL_0x00, 3, TwinleafTownPlayerHouse2F_RivalApproachPCSouth
    Message TwinleafTownPlayerHouse2F_Text_IsThisANewPC
    CloseMessage
    CallIfEq VAR_MAP_LOCAL_0x00, 0, TwinleafTownPlayerHouse2F_RivalTurnBackNorth
    CallIfEq VAR_MAP_LOCAL_0x00, 1, TwinleafTownPlayerHouse2F_RivalTurnBackWest
    CallIfEq VAR_MAP_LOCAL_0x00, 2, TwinleafTownPlayerHouse2F_RivalTurnBackEast
    CallIfEq VAR_MAP_LOCAL_0x00, 3, TwinleafTownPlayerHouse2F_RivalTurnBackSouth
    BufferRivalName 0
    Message TwinleafTownPlayerHouse2F_Text_WhereWasI
    CloseMessage
    CallIfEq VAR_MAP_LOCAL_0x00, 0, TwinleafTownPlayerHouse2F_RivalWalkBackToPlayerNorth
    CallIfEq VAR_MAP_LOCAL_0x00, 1, TwinleafTownPlayerHouse2F_RivalWalkBackToPlayerWest
    CallIfEq VAR_MAP_LOCAL_0x00, 2, TwinleafTownPlayerHouse2F_RivalWalkBackToPlayerEast
    CallIfEq VAR_MAP_LOCAL_0x00, 3, TwinleafTownPlayerHouse2F_RivalWalkBackToPlayerSouth
    BufferPlayerName 1
    Message TwinleafTownPlayerHouse2F_Text_SeeProfRowanAndGetPokemon
    CloseMessage
    CallIfEq VAR_MAP_LOCAL_0x00, 0, TwinleafTownPlayerHouse2F_RivalLeaveNorth
    CallIfEq VAR_MAP_LOCAL_0x00, 1, TwinleafTownPlayerHouse2F_RivalLeaveWest
    CallIfEq VAR_MAP_LOCAL_0x00, 2, TwinleafTownPlayerHouse2F_RivalLeaveEast
    CallIfEq VAR_MAP_LOCAL_0x00, 3, TwinleafTownPlayerHouse2F_RivalLeaveSouth
    PlaySE SEQ_SE_DP_KAIDAN2_sseq
    RemoveObject LOCALID_RIVAL
    Common_FadeToDefaultMusic2
    WaitSE SEQ_SE_DP_KAIDAN2_sseq
    SetFlag FLAG_HIDE_TWINLEAF_TOWN_PLAYER_HOUSE_2F_RIVAL
    SetVar VAR_PLAYER_HOUSE_RIVAL_STATE, 1
    ReleaseAll
    End

TwinleafTownPlayerHouse2F_RivalApproachPlayerNorth:
    ApplyMovement LOCALID_PLAYER, TwinleafTownPlayerHouse2F_Movement_PlayerFaceRivalLongDelay
    ApplyMovement LOCALID_RIVAL, TwinleafTownPlayerHouse2F_Movement_RivalApproachPlayerNorth
    WaitMovement
    Return

TwinleafTownPlayerHouse2F_RivalApproachPlayerWest:
    ApplyMovement LOCALID_PLAYER, TwinleafTownPlayerHouse2F_Movement_PlayerFaceRivalShortDelay
    ApplyMovement LOCALID_RIVAL, TwinleafTownPlayerHouse2F_Movement_RivalApproachPlayerWest
    WaitMovement
    Return

TwinleafTownPlayerHouse2F_RivalApproachPlayerEast:
    ApplyMovement LOCALID_RIVAL, TwinleafTownPlayerHouse2F_Movement_RivalApproachPlayerEast
    WaitMovement
    Return

TwinleafTownPlayerHouse2F_RivalApproachPlayerSouth:
    ApplyMovement LOCALID_PLAYER, TwinleafTownPlayerHouse2F_Movement_PlayerFaceRivalShortDelay
    ApplyMovement LOCALID_RIVAL, TwinleafTownPlayerHouse2F_Movement_RivalApproachPlayerSouth
    WaitMovement
    Return

TwinleafTownPlayerHouse2F_RivalApproachPCNorth:
    ApplyMovement LOCALID_PLAYER, TwinleafTownPlayerHouse2F_Movement_PlayerWatchRivalApproachPCNorth
    ApplyMovement LOCALID_RIVAL, TwinleafTownPlayerHouse2F_Movement_RivalApproachPCNorth
    WaitMovement
    Return

TwinleafTownPlayerHouse2F_RivalApproachPCWest:
    ApplyMovement LOCALID_PLAYER, TwinleafTownPlayerHouse2F_Movement_PlayerWatchRivalApproachPCWest
    ApplyMovement LOCALID_RIVAL, TwinleafTownPlayerHouse2F_Movement_RivalApproachPCWest
    WaitMovement
    Return

TwinleafTownPlayerHouse2F_RivalApproachPCEast:
    ApplyMovement LOCALID_PLAYER, TwinleafTownPlayerHouse2F_Movement_PlayerWatchRivalApproachPCEast
    ApplyMovement LOCALID_RIVAL, TwinleafTownPlayerHouse2F_Movement_RivalApproachPCEast
    WaitMovement
    Return

TwinleafTownPlayerHouse2F_RivalApproachPCSouth:
    ApplyMovement LOCALID_PLAYER, TwinleafTownPlayerHouse2F_Movement_PlayerWatchRivalApproachPCSouth
    ApplyMovement LOCALID_RIVAL, TwinleafTownPlayerHouse2F_Movement_RivalApproachPCSouth
    WaitMovement
    Return

TwinleafTownPlayerHouse2F_RivalTurnBackNorth:
    ApplyMovement LOCALID_RIVAL, TwinleafTownPlayerHouse2F_Movement_RivalTurnBackNorth
    WaitMovement
    Return

TwinleafTownPlayerHouse2F_RivalTurnBackWest:
    ApplyMovement LOCALID_RIVAL, TwinleafTownPlayerHouse2F_Movement_RivalTurnBackWest
    WaitMovement
    Return

TwinleafTownPlayerHouse2F_RivalTurnBackEast:
    ApplyMovement LOCALID_RIVAL, TwinleafTownPlayerHouse2F_Movement_RivalTurnBackEast
    WaitMovement
    Return

TwinleafTownPlayerHouse2F_RivalTurnBackSouth:
    ApplyMovement LOCALID_RIVAL, TwinleafTownPlayerHouse2F_Movement_RivalTurnBackSouth
    WaitMovement
    Return

TwinleafTownPlayerHouse2F_RivalWalkBackToPlayerNorth:
    ApplyMovement LOCALID_RIVAL, TwinleafTownPlayerHouse2F_Movement_RivalWalkBackToPlayerNorth
    WaitMovement
    Return

TwinleafTownPlayerHouse2F_RivalWalkBackToPlayerWest:
    ApplyMovement LOCALID_RIVAL, TwinleafTownPlayerHouse2F_Movement_RivalWalkBackToPlayerWest
    WaitMovement
    Return

TwinleafTownPlayerHouse2F_RivalWalkBackToPlayerEast:
    ApplyMovement LOCALID_RIVAL, TwinleafTownPlayerHouse2F_Movement_RivalWalkBackToPlayerEast
    WaitMovement
    Return

TwinleafTownPlayerHouse2F_RivalWalkBackToPlayerSouth:
    ApplyMovement LOCALID_RIVAL, TwinleafTownPlayerHouse2F_Movement_RivalWalkBackToPlayerSouth
    WaitMovement
    Return

TwinleafTownPlayerHouse2F_RivalLeaveNorth:
    ApplyMovement LOCALID_PLAYER, TwinleafTownPlayerHouse2F_Movement_PlayerWatchRivalLeave
    ApplyMovement LOCALID_RIVAL, TwinleafTownPlayerHouse2F_Movement_RivalLeaveNorth
    WaitMovement
    Return

TwinleafTownPlayerHouse2F_RivalLeaveWest:
    ApplyMovement LOCALID_PLAYER, TwinleafTownPlayerHouse2F_Movement_PlayerWatchRivalLeave
    ApplyMovement LOCALID_RIVAL, TwinleafTownPlayerHouse2F_Movement_RivalLeaveWest
    WaitMovement
    Return

TwinleafTownPlayerHouse2F_RivalLeaveEast:
    ApplyMovement LOCALID_PLAYER, TwinleafTownPlayerHouse2F_Movement_PlayerWatchRivalLeave
    ApplyMovement LOCALID_RIVAL, TwinleafTownPlayerHouse2F_Movement_RivalLeaveEast
    WaitMovement
    Return

TwinleafTownPlayerHouse2F_RivalLeaveSouth:
    ApplyMovement LOCALID_PLAYER, TwinleafTownPlayerHouse2F_Movement_PlayerWatchRivalLeave
    ApplyMovement LOCALID_RIVAL, TwinleafTownPlayerHouse2F_Movement_RivalLeaveSouth
    WaitMovement
    Return

    .balign 4, 0
TwinleafTownPlayerHouse2F_Movement_RivalEnterRoom:
    WalkFastWest 2
    EmoteExclamationMark
    Delay8
    EndMovement

    .balign 4, 0
TwinleafTownPlayerHouse2F_Movement_RivalApproachPlayerNorth:
    WalkFastWest
    WalkFastSouth
    WalkFastWest 2
    EndMovement

    .balign 4, 0
TwinleafTownPlayerHouse2F_Movement_RivalApproachPlayerWest:
    WalkFastWest
    WalkFastSouth 2
    WalkFastWest 3
    EndMovement

    .balign 4, 0
TwinleafTownPlayerHouse2F_Movement_RivalApproachPlayerEast:
    WalkFastSouth 2
    WalkFastWest 2
    EndMovement

    .balign 4, 0
TwinleafTownPlayerHouse2F_Movement_RivalApproachPlayerSouth:
    WalkFastWest
    WalkFastSouth 3
    WalkFastWest 2
    EndMovement

    .balign 4, 0
TwinleafTownPlayerHouse2F_Movement_RivalExclamationMark:
    EmoteExclamationMark
    Delay8
    EndMovement

    .balign 4, 0
TwinleafTownPlayerHouse2F_Movement_RivalApproachPCNorth:
    WalkFastSouth
    WalkFastWest 4
    WalkFastNorth
    EndMovement

    .balign 4, 0
TwinleafTownPlayerHouse2F_Movement_RivalApproachPCWest:
    WalkFastNorth
    WalkFastWest 3
    WalkOnSpotFastNorth
    EndMovement

    .balign 4, 0
TwinleafTownPlayerHouse2F_Movement_RivalApproachPCEast:
    WalkFastNorth
    WalkFastWest 5
    WalkOnSpotFastNorth
    EndMovement

    .balign 4, 0
TwinleafTownPlayerHouse2F_Movement_RivalApproachPCSouth:
    WalkFastNorth
    WalkFastWest 4
    WalkFastNorth
    EndMovement

    .balign 4, 0
TwinleafTownPlayerHouse2F_Movement_RivalTurnBackNorth:
    WalkOnSpotNormalEast
    EndMovement

    .balign 4, 0
TwinleafTownPlayerHouse2F_Movement_RivalTurnBackWest:
    WalkOnSpotNormalEast
    EndMovement

    .balign 4, 0
TwinleafTownPlayerHouse2F_Movement_RivalTurnBackEast:
    WalkOnSpotNormalEast
    EndMovement

    .balign 4, 0
TwinleafTownPlayerHouse2F_Movement_RivalTurnBackSouth:
    WalkOnSpotNormalEast
    EndMovement

    .balign 4, 0
TwinleafTownPlayerHouse2F_Movement_RivalWalkBackToPlayerNorth:
    WalkFastEast 2
    EndMovement

    .balign 4, 0
TwinleafTownPlayerHouse2F_Movement_RivalWalkBackToPlayerWest:
    WalkFastEast
    WalkFastSouth
    WalkOnSpotFastEast
    EndMovement

    .balign 4, 0
TwinleafTownPlayerHouse2F_Movement_RivalWalkBackToPlayerEast:
    WalkFastEast
    WalkFastSouth
    WalkFastEast 2
    EndMovement

    .balign 4, 0
TwinleafTownPlayerHouse2F_Movement_RivalWalkBackToPlayerSouth:
    WalkFastEast
    WalkFastSouth 2
    WalkFastEast
    EndMovement

    .balign 4, 0
TwinleafTownPlayerHouse2F_Movement_RivalLeaveNorth:
    WalkFastSouth
    WalkFastEast 3
    WalkFastNorth 2
    WalkFastEast 4
    EndMovement

    .balign 4, 0
TwinleafTownPlayerHouse2F_Movement_RivalLeaveWest:
    WalkFastNorth
    WalkFastEast 4
    WalkFastNorth
    WalkFastEast 3
    EndMovement

    .balign 4, 0
TwinleafTownPlayerHouse2F_Movement_RivalLeaveEast:
    WalkFastNorth
    WalkFastEast 2
    WalkFastNorth
    WalkFastEast 3
    EndMovement

    .balign 4, 0
TwinleafTownPlayerHouse2F_Movement_RivalLeaveSouth:
    WalkFastNorth
    WalkFastEast 3
    WalkFastNorth 2
    WalkFastEast 3
    EndMovement

    .balign 4, 0
TwinleafTownPlayerHouse2F_Movement_PlayerFaceRivalLongDelay:
    Delay8
    Delay4
    WalkOnSpotNormalEast
    EndMovement

    .balign 4, 0
TwinleafTownPlayerHouse2F_Movement_PlayerFaceRivalShortDelay:
    Delay8 2
    WalkOnSpotNormalEast
    EndMovement

    .balign 4, 0
TwinleafTownPlayerHouse2F_Movement_PlayerWatchRivalApproachPCNorth:
    Delay8 2
    WalkOnSpotFastWest
    EndMovement

    .balign 4, 0
TwinleafTownPlayerHouse2F_Movement_PlayerWatchRivalApproachPCWest:
    Delay8
    WalkOnSpotNormalWest
    EndMovement

    .balign 4, 0
TwinleafTownPlayerHouse2F_Movement_PlayerWatchRivalApproachPCEast:
    Delay8
    WalkOnSpotNormalWest
    EndMovement

    .balign 4, 0
TwinleafTownPlayerHouse2F_Movement_PlayerWatchRivalApproachPCSouth:
    Delay8
    WalkOnSpotNormalWest
    EndMovement

    .balign 4, 0
TwinleafTownPlayerHouse2F_Movement_PlayerWatchRivalLeave:
    Delay8 2
    WalkOnSpotNormalEast
    EndMovement

#ifdef OXIDE_TESTKIT
/* Platinum Oxide test kit: built only by `make testkit` (docs/oxide/test-kit.md),
   so none of this is in a normal ROM. The NPC in the bedroom's bottom-left
   corner hands out what the emulator checks in the tracker's "Waiting on Ian"
   list need. Its object event and text are appended from res/testkit/.

   Each new batch of battle effect scripts adds a move set: four moves that use
   the batch's effects, given on a Mew by TestKit_GiveMew. Add a menu entry, its
   text in res/testkit/, and a block like TestKit_MoveSet1. */
    .balign 4, 0
TestKit_Helper:
    PlaySE SE_CONFIRM_sseq_3
    LockAll
    FacePlayer
    Message TestKit_Text_WhatDoYouNeed
    InitLocalTextListMenu 1, 1, 0, VAR_0x8004
    AddListMenuEntry TestKit_Text_MenuRareCandies, 0
    AddListMenuEntry TestKit_Text_MenuForms, 1
    AddListMenuEntry TestKit_Text_MenuEevee, 2
    AddListMenuEntry TestKit_Text_MenuKlefki, 3
    AddListMenuEntry TestKit_Text_MenuFairy, 4
    AddListMenuEntry TestKit_Text_MenuMoveSets, 5
    AddListMenuEntry TestKit_Text_MenuWildChansey, 6
    AddListMenuEntry TestKit_Text_MenuWildShuckle, 9
    AddListMenuEntry TestKit_Text_MenuWildLugia, 10
    AddListMenuEntry TestKit_Text_MenuWildSkarmory, 11
    AddListMenuEntry TestKit_Text_MenuWarp, 7
    AddListMenuEntry TestKit_Text_MenuNothing, 8
    ShowListMenu
    GoToIfEq VAR_0x8004, 0, TestKit_RareCandies
    GoToIfEq VAR_0x8004, 1, TestKit_Forms
    GoToIfEq VAR_0x8004, 2, TestKit_Eevee
    GoToIfEq VAR_0x8004, 3, TestKit_Klefki
    GoToIfEq VAR_0x8004, 4, TestKit_Fairy
    GoToIfEq VAR_0x8004, 5, TestKit_MoveSets
    GoToIfEq VAR_0x8004, 6, TestKit_WildChansey
    GoToIfEq VAR_0x8004, 7, TestKit_Warp
    GoToIfEq VAR_0x8004, 9, TestKit_WildShuckle
    GoToIfEq VAR_0x8004, 10, TestKit_WildLugia
    GoToIfEq VAR_0x8004, 11, TestKit_WildSkarmory
    GoTo TestKit_Close

TestKit_RareCandies:
    AddItem ITEM_RARE_CANDY, 99, VAR_RESULT
    Message TestKit_Text_RareCandies
    GoTo TestKit_WaitAndClose

/* The party count before a gift is the slot the gift lands in. */
TestKit_Forms:
    GetPartyCount VAR_0x8005
    GoToIfGe VAR_0x8005, 5, TestKit_PartyFull
    GivePokemon SPECIES_ROTOM, 30, ITEM_NONE, VAR_RESULT
    TestKitSetPartyMonForm VAR_0x8005, 2    /* ROTOM_FORM_WASH */
    AddVar VAR_0x8005, 1
    GivePokemon SPECIES_GIRATINA, 50, ITEM_GRISEOUS_ORB, VAR_RESULT
    TestKitSetPartyMonForm VAR_0x8005, 1    /* GIRATINA_FORM_ORIGIN */
    Message TestKit_Text_Forms
    GoTo TestKit_WaitAndClose

/* Sylveon's method is a level-up while knowing Charm, so Eevee gets Charm in
   its first slot and one Rare Candy should evolve it. */
TestKit_Eevee:
    GetPartyCount VAR_0x8005
    GoToIfGe VAR_0x8005, 6, TestKit_PartyFull
    GivePokemon SPECIES_EEVEE, 20, ITEM_NONE, VAR_RESULT
    ResetPartyMonMoveSlot_Unused VAR_0x8005, 0, MOVE_CHARM
    Message TestKit_Text_Eevee
    GoTo TestKit_WaitAndClose

/* Klefki learns Fairy Wind (move 587) at Lv. 6, which the old packed learnset
   format could not hold, so one Rare Candy tests the widened format. */
TestKit_Klefki:
    GetPartyCount VAR_0x8005
    GoToIfGe VAR_0x8005, 6, TestKit_PartyFull
    GivePokemon SPECIES_KLEFKI, 5, ITEM_NONE, VAR_RESULT
    Message TestKit_Text_Klefki
    GoTo TestKit_WaitAndClose

TestKit_Fairy:
    GetPartyCount VAR_0x8005
    GoToIfGe VAR_0x8005, 6, TestKit_PartyFull
    GivePokemon SPECIES_GIBLE, 20, ITEM_NONE, VAR_RESULT
    ResetPartyMonMoveSlot_Unused VAR_0x8005, 0, MOVE_DRAGON_CLAW
    Message TestKit_Text_Fairy
    WaitButton
    CloseMessage
    StartWildBattle SPECIES_CLEFAIRY, 10
    GoTo TestKit_AfterBattle

TestKit_WildChansey:
    Message TestKit_Text_WildChansey
    WaitButton
    CloseMessage
    StartWildBattle SPECIES_CHANSEY, 50
    GoTo TestKit_AfterBattle

/* Chansey's Defense is so low that a physical hit ends the battle before an
   extra effect shows (Sappy Seed, Axe Kick's confusion, Double Iron Bash's
   flinch), so Shuckle is the physical target. It is also slower than Mew. */
TestKit_WildShuckle:
    Message TestKit_Text_WildShuckle
    WaitButton
    CloseMessage
    StartWildBattle SPECIES_SHUCKLE, 50
    GoTo TestKit_AfterBattle

/* At Lv. 2 Lugia knows only Whirlwind, so it uses it every turn: the attacker
   for the Roar and Whirlwind Ingrain fix (set 25). */
TestKit_WildLugia:
    Message TestKit_Text_WildLugia
    WaitButton
    CloseMessage
    StartWildBattle SPECIES_LUGIA, 2
    GoTo TestKit_AfterBattle

/* A Flying Pokemon bulky enough to take Smack Down and Thousand Arrows and
   still be there to show it was grounded (set 26). */
TestKit_WildSkarmory:
    Message TestKit_Text_WildSkarmory
    WaitButton
    CloseMessage
    StartWildBattle SPECIES_SKARMORY, 50
    GoTo TestKit_AfterBattle

TestKit_AfterBattle:
    CheckWonBattle VAR_RESULT
    GoToIfEq VAR_RESULT, FALSE, TestKit_LostBattle
    ReleaseAll
    End

TestKit_LostBattle:
    BlackOutFromBattle
    ReleaseAll
    End

TestKit_MoveSets:
    GetPartyCount VAR_0x8005
    GoToIfGe VAR_0x8005, 6, TestKit_PartyFull
    Message TestKit_Text_WhichSet
    InitLocalTextListMenu 1, 1, 0, VAR_0x8004
    AddListMenuEntry TestKit_Text_MenuSet1, 0
    AddListMenuEntry TestKit_Text_MenuSet2, 1
    AddListMenuEntry TestKit_Text_MenuSet3, 2
    AddListMenuEntry TestKit_Text_MenuSet4, 3
    AddListMenuEntry TestKit_Text_MenuSet5, 4
    AddListMenuEntry TestKit_Text_MenuSet6, 5
    AddListMenuEntry TestKit_Text_MenuSet7, 6
    AddListMenuEntry TestKit_Text_MenuSet8, 7
    AddListMenuEntry TestKit_Text_MenuSet9, 8
    AddListMenuEntry TestKit_Text_MenuSet10, 9
    AddListMenuEntry TestKit_Text_MenuSet11, 10
    AddListMenuEntry TestKit_Text_MenuSet12, 11
    AddListMenuEntry TestKit_Text_MenuSet13, 12
    AddListMenuEntry TestKit_Text_MenuSet14, 13
    AddListMenuEntry TestKit_Text_MenuSet15, 14
    AddListMenuEntry TestKit_Text_MenuSet16, 15
    AddListMenuEntry TestKit_Text_MenuSet17, 16
    AddListMenuEntry TestKit_Text_MenuSet18, 17
    AddListMenuEntry TestKit_Text_MenuSet19, 18
    AddListMenuEntry TestKit_Text_MenuSet20, 19
    AddListMenuEntry TestKit_Text_MenuSet21, 20
    AddListMenuEntry TestKit_Text_MenuSet22, 21
    AddListMenuEntry TestKit_Text_MenuSet23, 22
    AddListMenuEntry TestKit_Text_MenuSet24, 23
    AddListMenuEntry TestKit_Text_MenuSet25, 24
    AddListMenuEntry TestKit_Text_MenuSet26, 25
    ShowListMenu
    GoToIfEq VAR_0x8004, 0, TestKit_MoveSet1
    GoToIfEq VAR_0x8004, 1, TestKit_MoveSet2
    GoToIfEq VAR_0x8004, 2, TestKit_MoveSet3
    GoToIfEq VAR_0x8004, 3, TestKit_MoveSet4
    GoToIfEq VAR_0x8004, 4, TestKit_MoveSet5
    GoToIfEq VAR_0x8004, 5, TestKit_MoveSet6
    GoToIfEq VAR_0x8004, 6, TestKit_MoveSet7
    GoToIfEq VAR_0x8004, 7, TestKit_MoveSet8
    GoToIfEq VAR_0x8004, 8, TestKit_MoveSet9
    GoToIfEq VAR_0x8004, 9, TestKit_MoveSet10
    GoToIfEq VAR_0x8004, 10, TestKit_MoveSet11
    GoToIfEq VAR_0x8004, 11, TestKit_MoveSet12
    GoToIfEq VAR_0x8004, 12, TestKit_MoveSet13
    GoToIfEq VAR_0x8004, 13, TestKit_MoveSet14
    GoToIfEq VAR_0x8004, 14, TestKit_MoveSet15
    GoToIfEq VAR_0x8004, 15, TestKit_MoveSet16
    GoToIfEq VAR_0x8004, 16, TestKit_MoveSet17
    GoToIfEq VAR_0x8004, 17, TestKit_MoveSet18
    GoToIfEq VAR_0x8004, 18, TestKit_MoveSet19
    GoToIfEq VAR_0x8004, 19, TestKit_MoveSet20
    GoToIfEq VAR_0x8004, 20, TestKit_MoveSet21
    GoToIfEq VAR_0x8004, 21, TestKit_MoveSet22
    GoToIfEq VAR_0x8004, 22, TestKit_MoveSet23
    GoToIfEq VAR_0x8004, 23, TestKit_MoveSet24
    GoToIfEq VAR_0x8004, 24, TestKit_MoveSet25
    GoToIfEq VAR_0x8004, 25, TestKit_MoveSet26
    GoTo TestKit_Close

/* Sets 1 to 4: the first batch of effect scripts (388331c51). */
TestKit_MoveSet1:
    SetVar VAR_0x8006, MOVE_POPULATION_BOMB
    SetVar VAR_0x8007, MOVE_TRIPLE_DIVE
    SetVar VAR_0x8008, MOVE_SAPPY_SEED
    SetVar VAR_0x8009, MOVE_ZIPPY_ZAP
    GoTo TestKit_GiveMew

TestKit_MoveSet2:
    SetVar VAR_0x8006, MOVE_GLITZY_GLOW
    SetVar VAR_0x8007, MOVE_BADDY_BAD
    SetVar VAR_0x8008, MOVE_FREEZY_FROST
    SetVar VAR_0x8009, MOVE_SPARKLY_SWIRL
    GoTo TestKit_GiveMew

/* Toxic first, since Infernal Parade and Barb Barrage double on a status. */
TestKit_MoveSet3:
    SetVar VAR_0x8006, MOVE_TOXIC
    SetVar VAR_0x8007, MOVE_INFERNAL_PARADE
    SetVar VAR_0x8008, MOVE_BARB_BARRAGE
    SetVar VAR_0x8009, MOVE_PSYCHIC_NOISE
    GoTo TestKit_GiveMew

TestKit_MoveSet4:
    SetVar VAR_0x8006, MOVE_DIRE_CLAW
    SetVar VAR_0x8007, MOVE_SPIN_OUT
    SetVar VAR_0x8008, MOVE_ALOLAN_GUARDIAN
    SetVar VAR_0x8009, MOVE_ESPER_WING
    GoTo TestKit_GiveMew

/* Sets 5 to 7: the second batch (2f84be2ef). Hex and Venoshock want a status
   on the target first; Acrobatics doubles because the Mew holds nothing. */
TestKit_MoveSet5:
    SetVar VAR_0x8006, MOVE_TOXIC
    SetVar VAR_0x8007, MOVE_VENOSHOCK
    SetVar VAR_0x8008, MOVE_HEX
    SetVar VAR_0x8009, MOVE_ACROBATICS
    GoTo TestKit_GiveMew

TestKit_MoveSet6:
    SetVar VAR_0x8006, MOVE_FLAME_CHARGE
    SetVar VAR_0x8007, MOVE_AXE_KICK
    SetVar VAR_0x8008, MOVE_DOUBLE_IRON_BASH
    SetVar VAR_0x8009, MOVE_TRIPLE_AXEL
    GoTo TestKit_GiveMew

/* Set 7 carries Spin Out so Bolt Beak can be compared: first while Mew moves
   first (double power), then after two Spin Outs, when Chansey outspeeds it.
   Flower Trick, which it replaced, passed in Ian's first run. */
TestKit_MoveSet7:
    SetVar VAR_0x8006, MOVE_RELIC_SONG
    SetVar VAR_0x8007, MOVE_SURGING_STRIKES
    SetVar VAR_0x8008, MOVE_SPIN_OUT
    SetVar VAR_0x8009, MOVE_BOLT_BEAK
    GoTo TestKit_GiveMew

/* Sets 8 and 9: the third batch (5d1d1a970). The storms never miss in rain,
   and Hurricane drops to 50 accuracy in sun. */
TestKit_MoveSet8:
    SetVar VAR_0x8006, MOVE_RAIN_DANCE
    SetVar VAR_0x8007, MOVE_HURRICANE
    SetVar VAR_0x8008, MOVE_WILDBOLT_STORM
    SetVar VAR_0x8009, MOVE_BLEAKWIND_STORM
    GoTo TestKit_GiveMew

TestKit_MoveSet9:
    SetVar VAR_0x8006, MOVE_SUNNY_DAY
    SetVar VAR_0x8007, MOVE_SANDSEAR_STORM
    SetVar VAR_0x8008, MOVE_DIAMOND_STORM
    SetVar VAR_0x8009, MOVE_FIRST_IMPRESSION
    GoTo TestKit_GiveMew

/* Sets 10 to 17: the four batches after 5d1d1a970, up to c4d800e11. */
TestKit_MoveSet10:
    SetVar VAR_0x8006, MOVE_HONE_CLAWS
    SetVar VAR_0x8007, MOVE_QUIVER_DANCE
    SetVar VAR_0x8008, MOVE_COIL
    SetVar VAR_0x8009, MOVE_SHIFT_GEAR
    GoTo TestKit_GiveMew

TestKit_MoveSet11:
    SetVar VAR_0x8006, MOVE_SHELL_SMASH
    SetVar VAR_0x8007, MOVE_WORK_UP
    SetVar VAR_0x8008, MOVE_VICTORY_DANCE
    SetVar VAR_0x8009, MOVE_COTTON_GUARD
    GoTo TestKit_GiveMew

TestKit_MoveSet12:
    SetVar VAR_0x8006, MOVE_FILLET_AWAY
    SetVar VAR_0x8007, MOVE_CLANGOROUS_SOUL
    SetVar VAR_0x8008, MOVE_GEOMANCY
    SetVar VAR_0x8009, MOVE_TAKE_HEART
    GoTo TestKit_GiveMew

TestKit_MoveSet13:
    SetVar VAR_0x8006, MOVE_V_CREATE
    SetVar VAR_0x8007, MOVE_CLANGING_SCALES
    SetVar VAR_0x8008, MOVE_HYPERSPACE_FURY
    SetVar VAR_0x8009, MOVE_SPICY_EXTRACT
    GoTo TestKit_GiveMew

/* Poltergeist fails against a target holding nothing, which is correct. */
TestKit_MoveSet14:
    SetVar VAR_0x8006, MOVE_POLTERGEIST
    SetVar VAR_0x8007, MOVE_FICKLE_BEAM
    SetVar VAR_0x8008, MOVE_MATCHA_GOTCHA
    SetVar VAR_0x8009, MOVE_ANCHOR_SHOT
    GoTo TestKit_GiveMew

TestKit_MoveSet15:
    SetVar VAR_0x8006, MOVE_JAW_LOCK
    SetVar VAR_0x8007, MOVE_STONE_AXE
    SetVar VAR_0x8008, MOVE_CEASELESS_EDGE
    SetVar VAR_0x8009, MOVE_MORTAL_SPIN
    GoTo TestKit_GiveMew

/* Double Shock needs an Electric user, so set 16 is on Electivire. */
TestKit_MoveSet16:
    SetVar VAR_0x8006, MOVE_FREEZE_SHOCK
    SetVar VAR_0x8007, MOVE_ICE_BURN
    SetVar VAR_0x8008, MOVE_FELL_STINGER
    SetVar VAR_0x8009, MOVE_DOUBLE_SHOCK
    SetVar VAR_0x800A, SPECIES_ELECTIVIRE
    GoTo TestKit_GivePokemonWithMoves

/* Burn Up needs a Fire user, so set 17 is on Magmortar. */
TestKit_MoveSet17:
    SetVar VAR_0x8006, MOVE_BURN_UP
    SetVar VAR_0x8007, MOVE_CLEAR_SMOG
    SetVar VAR_0x8008, MOVE_FINAL_GAMBIT
    SetVar VAR_0x8009, MOVE_CHLOROBLAST
    SetVar VAR_0x800A, SPECIES_MAGMORTAR
    GoTo TestKit_GivePokemonWithMoves

/* Sets 18 to 22: batches 9664a529a and a32b5ab7d. Coaching and Pollen Puff's
   ally heal need a double battle, which the kit cannot start, so Coaching is
   here only to show it fails in a single battle. */
TestKit_MoveSet18:
    SetVar VAR_0x8006, MOVE_DRAINING_KISS
    SetVar VAR_0x8007, MOVE_OBLIVION_WING
    SetVar VAR_0x8008, MOVE_NOBLE_ROAR
    SetVar VAR_0x8009, MOVE_TEARFUL_LOOK
    GoTo TestKit_GiveMew

/* Venom Drench only works on a poisoned target, so Toxic comes first. */
TestKit_MoveSet19:
    SetVar VAR_0x8006, MOVE_TOXIC
    SetVar VAR_0x8007, MOVE_VENOM_DRENCH
    SetVar VAR_0x8008, MOVE_HEAL_PULSE
    SetVar VAR_0x8009, MOVE_LIFE_DEW
    GoTo TestKit_GiveMew

TestKit_MoveSet20:
    SetVar VAR_0x8006, MOVE_POLLEN_PUFF
    SetVar VAR_0x8007, MOVE_STRENGTH_SAP
    SetVar VAR_0x8008, MOVE_GUARD_SPLIT
    SetVar VAR_0x8009, MOVE_POWER_SPLIT
    GoTo TestKit_GiveMew

/* Soak makes the target pure Water, so Thunderbolt should then hit it for
   double damage. Incinerate burns a held berry only if the target has one. */
TestKit_MoveSet21:
    SetVar VAR_0x8006, MOVE_SOAK
    SetVar VAR_0x8007, MOVE_THUNDERBOLT
    SetVar VAR_0x8008, MOVE_INCINERATE
    SetVar VAR_0x8009, MOVE_COACHING
    GoTo TestKit_GiveMew

/* Heavy Slam and Heat Crash grow with the user's weight against the target's,
   so they go on Metagross (550 kg); Autotomize lightens it, weakening both.
   Swords Dance is a two-stage rise, to check it still says "sharply". */
TestKit_MoveSet22:
    SetVar VAR_0x8006, MOVE_HEAVY_SLAM
    SetVar VAR_0x8007, MOVE_HEAT_CRASH
    SetVar VAR_0x8008, MOVE_AUTOTOMIZE
    SetVar VAR_0x8009, MOVE_SWORDS_DANCE
    SetVar VAR_0x800A, SPECIES_METAGROSS
    GoTo TestKit_GivePokemonWithMoves

/* Dragon Tail and Circle Throw hit, then drag the target out: against a wild
   Pokemon no higher in level than Mew they end the battle. Parting Shot lowers
   the target's Attack and Special Attack, then switches Mew out if there is
   another Pokemon to send in. Roar is here because its code was reshaped to
   share with Dragon Tail and should behave exactly as before. */
TestKit_MoveSet23:
    SetVar VAR_0x8006, MOVE_DRAGON_TAIL
    SetVar VAR_0x8007, MOVE_CIRCLE_THROW
    SetVar VAR_0x8008, MOVE_PARTING_SHOT
    SetVar VAR_0x8009, MOVE_ROAR
    GoTo TestKit_GiveMew

/* Laser Focus makes Mew's move on the next turn a critical hit, and only that
   turn's. Tackle shows it against Shuckle: a critical hit the turn after Laser
   Focus, then ordinary odds the turn after that. Lock-On and Zap Cannon are here
   because Laser Focus counts down beside Lock-On at the end of each turn, so
   Zap Cannon on the turn after Lock-On should still never miss. */
TestKit_MoveSet24:
    SetVar VAR_0x8006, MOVE_LASER_FOCUS
    SetVar VAR_0x8007, MOVE_TACKLE
    SetVar VAR_0x8008, MOVE_LOCK_ON
    SetVar VAR_0x8009, MOVE_ZAP_CANNON
    GoTo TestKit_GiveMew

/* Set 25, against the wild Lugia: Ingrain on the first turn, so its Whirlwind
   fails as it always did, then Aqua Ring. Vanilla let the next Whirlwind end
   the battle once a second effect was up; with the fix Mew stays anchored. */
TestKit_MoveSet25:
    SetVar VAR_0x8006, MOVE_INGRAIN
    SetVar VAR_0x8007, MOVE_AQUA_RING
    SetVar VAR_0x8008, MOVE_SPLASH
    SetVar VAR_0x8009, MOVE_RECOVER
    GoTo TestKit_GiveMew

/* Set 26, against the wild Skarmory: Earthquake does nothing to it until
   Smack Down or Thousand Arrows has brought it down. Thousand Arrows hits it
   anyway, as a Ground move against Steel alone. */
TestKit_MoveSet26:
    SetVar VAR_0x8006, MOVE_SMACK_DOWN
    SetVar VAR_0x8007, MOVE_EARTHQUAKE
    SetVar VAR_0x8008, MOVE_THOUSAND_ARROWS
    SetVar VAR_0x8009, MOVE_RECOVER
    GoTo TestKit_GiveMew

/* Gives a Lv. 50 Pokemon of species VAR_0x800A (Mew from TestKit_GiveMew) in
   slot VAR_0x8005, holding the four moves in VAR_0x8006 to VAR_0x8009, and
   names them. */
TestKit_GiveMew:
    SetVar VAR_0x800A, SPECIES_MEW
TestKit_GivePokemonWithMoves:
    GivePokemon VAR_0x800A, 50, ITEM_NONE, VAR_RESULT
    ResetPartyMonMoveSlot_Unused VAR_0x8005, 0, VAR_0x8006
    ResetPartyMonMoveSlot_Unused VAR_0x8005, 1, VAR_0x8007
    ResetPartyMonMoveSlot_Unused VAR_0x8005, 2, VAR_0x8008
    ResetPartyMonMoveSlot_Unused VAR_0x8005, 3, VAR_0x8009
    BufferMoveName 0, VAR_0x8006
    BufferMoveName 1, VAR_0x8007
    BufferMoveName 2, VAR_0x8008
    BufferMoveName 3, VAR_0x8009
    Message TestKit_Text_MoveSet
    GoTo TestKit_WaitAndClose

/* Towns land on their fly points (src/spawn_locations.c); the Pokemon Center
   lands in front of the counter, where a whiteout does. */
TestKit_Warp:
    Message TestKit_Text_WhereTo
    InitLocalTextListMenu 1, 1, 0, VAR_0x8004
    AddListMenuEntry TestKit_Text_MenuTwinleaf, 0
    AddListMenuEntry TestKit_Text_MenuSandgem, 1
    AddListMenuEntry TestKit_Text_MenuSandgemCenter, 2
    AddListMenuEntry TestKit_Text_MenuJubilife, 3
    AddListMenuEntry TestKit_Text_MenuPastoria, 4
    AddListMenuEntry TestKit_Text_MenuVeilstone, 5
    ShowListMenu
    GoToIfEq VAR_0x8004, 0, TestKit_WarpTwinleaf
    GoToIfEq VAR_0x8004, 1, TestKit_WarpSandgem
    GoToIfEq VAR_0x8004, 2, TestKit_WarpSandgemCenter
    GoToIfEq VAR_0x8004, 3, TestKit_WarpJubilife
    GoToIfEq VAR_0x8004, 4, TestKit_WarpPastoria
    GoToIfEq VAR_0x8004, 5, TestKit_WarpVeilstone
    GoTo TestKit_Close

TestKit_WarpTwinleaf:
    CloseMessage
    Warp MAP_HEADER_TWINLEAF_TOWN, 0x74, 0x376, DIR_SOUTH
    ReleaseAll
    End

TestKit_WarpSandgem:
    CloseMessage
    Warp MAP_HEADER_SANDGEM_TOWN, 0xB1, 0x34B, DIR_SOUTH
    ReleaseAll
    End

TestKit_WarpSandgemCenter:
    CloseMessage
    Warp MAP_HEADER_SANDGEM_TOWN_POKECENTER_1F, 0x8, 0x6, DIR_NORTH
    ReleaseAll
    End

TestKit_WarpJubilife:
    CloseMessage
    Warp MAP_HEADER_JUBILIFE_CITY, 0xB4, 0x309, DIR_SOUTH
    ReleaseAll
    End

TestKit_WarpPastoria:
    CloseMessage
    Warp MAP_HEADER_PASTORIA_CITY, 0x258, 0x330, DIR_SOUTH
    ReleaseAll
    End

TestKit_WarpVeilstone:
    CloseMessage
    Warp MAP_HEADER_VEILSTONE_CITY, 0x2CD, 0x264, DIR_SOUTH
    ReleaseAll
    End

TestKit_PartyFull:
    Message TestKit_Text_PartyFull
    GoTo TestKit_WaitAndClose

TestKit_WaitAndClose:
    WaitButton
TestKit_Close:
    CloseMessage
    ReleaseAll
    End
#endif

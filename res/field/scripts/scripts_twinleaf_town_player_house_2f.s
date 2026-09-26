#include "macros/scrcmd.inc"
#include "res/text/bank/twinleaf_town_player_house_2f.h"
#include "res/field/events/events_twinleaf_town_player_house_2f.h"
#ifdef OXIDE_TESTKIT
#include "generated/abilities.h"
#endif


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
    SetVar VAR_0x800B, ABILITY_NONE
    SetVar VAR_0x8000, SPECIES_NONE
    SetVar VAR_0x8003, MOVE_NONE
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
    AddListMenuEntry TestKit_Text_MenuWildHorsea, 12
    AddListMenuEntry TestKit_Text_MenuWildGlameow, 13
    AddListMenuEntry TestKit_Text_MenuAbilities, 14
    AddListMenuEntry TestKit_Text_MenuStaples, 15
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
    GoToIfEq VAR_0x8004, 12, TestKit_WildHorsea
    GoToIfEq VAR_0x8004, 13, TestKit_WildGlameow
    GoToIfEq VAR_0x8004, 14, TestKit_Abilities
    GoToIfEq VAR_0x8004, 15, TestKit_Staples
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

/* At Lv. 1 Horsea knows only Bubble, which hits every foe, and Glameow only
   Fake Out, which has raised priority: attackers for Wide Guard and Quick
   Guard (set 30). */
TestKit_WildHorsea:
    Message TestKit_Text_WildHorsea
    WaitButton
    CloseMessage
    StartWildBattle SPECIES_HORSEA, 1
    GoTo TestKit_AfterBattle

TestKit_WildGlameow:
    Message TestKit_Text_WildGlameow
    WaitButton
    CloseMessage
    StartWildBattle SPECIES_GLAMEOW, 1
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
    AddListMenuEntry TestKit_Text_MenuSet27, 26
    AddListMenuEntry TestKit_Text_MenuSet28, 27
    AddListMenuEntry TestKit_Text_MenuSet29, 28
    AddListMenuEntry TestKit_Text_MenuSet30, 29
    AddListMenuEntry TestKit_Text_MenuSet31, 30
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
    GoToIfEq VAR_0x8004, 26, TestKit_MoveSet27
    GoToIfEq VAR_0x8004, 27, TestKit_MoveSet28
    GoToIfEq VAR_0x8004, 28, TestKit_MoveSet29
    GoToIfEq VAR_0x8004, 29, TestKit_MoveSet30
    GoToIfEq VAR_0x8004, 30, TestKit_MoveSet31
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

/* Set 27: Sticky Web is laid, fails a second time, and Defog clears it along
   with Spikes and Stealth Rock. Its switch-in Speed drop needs a Pokemon to
   switch in on the webbed side, which a wild battle never has. */
TestKit_MoveSet27:
    SetVar VAR_0x8006, MOVE_STICKY_WEB
    SetVar VAR_0x8007, MOVE_SPIKES
    SetVar VAR_0x8008, MOVE_STEALTH_ROCK
    SetVar VAR_0x8009, MOVE_DEFOG
    GoTo TestKit_GiveMew

/* Set 28: After You on the wild Shuckle, which is slower than Mew, takes the
   kind offer; once Trick Room is up Shuckle moves first, so After You fails.
   Moving an ally's turn needs a double battle, which the kit does not have. */
TestKit_MoveSet28:
    SetVar VAR_0x8006, MOVE_AFTER_YOU
    SetVar VAR_0x8007, MOVE_TRICK_ROOM
    SetVar VAR_0x8008, MOVE_TACKLE
    SetVar VAR_0x8009, MOVE_RECOVER
    GoTo TestKit_GiveMew

/* Set 29: Aurora Veil fails without hail, goes up under Hail, fails a second
   time while up, and wears off after five turns. */
TestKit_MoveSet29:
    SetVar VAR_0x8006, MOVE_AURORA_VEIL
    SetVar VAR_0x8007, MOVE_HAIL
    SetVar VAR_0x8008, MOVE_RECOVER
    SetVar VAR_0x8009, MOVE_SPLASH
    GoTo TestKit_GiveMew

/* Set 30: the four side guards, each against the foe it should stop: Wide
   Guard against the wild Horsea's Bubble, Quick Guard against the wild
   Glameow's Fake Out, Mat Block against the wild Skarmory on the first turn
   only, and Crafty Shield against the wild Lugia's Whirlwind. */
TestKit_MoveSet30:
    SetVar VAR_0x8006, MOVE_WIDE_GUARD
    SetVar VAR_0x8007, MOVE_QUICK_GUARD
    SetVar VAR_0x8008, MOVE_MAT_BLOCK
    SetVar VAR_0x8009, MOVE_CRAFTY_SHIELD
    GoTo TestKit_GiveMew

/* Set 31: Belch is refused at the move menu until Mew has eaten a Berry.
   Give Mew the Sitrus Berry this puts in the bag; Belly Drum halves its HP,
   the Berry heals it, and Belch can then be chosen, even after switching
   out and back. */
TestKit_MoveSet31:
    AddItem ITEM_SITRUS_BERRY, 1, VAR_RESULT
    SetVar VAR_0x8006, MOVE_BELCH
    SetVar VAR_0x8007, MOVE_BELLY_DRUM
    SetVar VAR_0x8008, MOVE_RECOVER
    SetVar VAR_0x8009, MOVE_SPLASH
    GoTo TestKit_GiveMew

/* As TestKit_GivePokemonWithMoves, holding the item in VAR_0x8004 (free once
   a menu has been answered), for an entry that needs a held item. */
TestKit_GivePokemonWithItem:
    GivePokemon VAR_0x800A, 50, VAR_0x8004, VAR_RESULT
    GoTo TestKit_GivePokemonSetMoves

/* Gives a Lv. 50 Pokemon of species VAR_0x800A (Mew from TestKit_GiveMew) in
   slot VAR_0x8005, holding the four moves in VAR_0x8006 to VAR_0x8009, and
   names them. */
TestKit_GiveMew:
    SetVar VAR_0x800A, SPECIES_MEW
TestKit_GivePokemonWithMoves:
    GivePokemon VAR_0x800A, 50, ITEM_NONE, VAR_RESULT
TestKit_GivePokemonSetMoves:
    ResetPartyMonMoveSlot_Unused VAR_0x8005, 0, VAR_0x8006
    ResetPartyMonMoveSlot_Unused VAR_0x8005, 1, VAR_0x8007
    ResetPartyMonMoveSlot_Unused VAR_0x8005, 2, VAR_0x8008
    ResetPartyMonMoveSlot_Unused VAR_0x8005, 3, VAR_0x8009
    CallIfNe VAR_0x800B, ABILITY_NONE, TestKit_SetAbility
    BufferMoveName 0, VAR_0x8006
    BufferMoveName 1, VAR_0x8007
    BufferMoveName 2, VAR_0x8008
    BufferMoveName 3, VAR_0x8009
    Message TestKit_Text_MoveSet
    GoToIfNe VAR_0x8000, SPECIES_NONE, TestKit_AbilityFoe
    GoTo TestKit_WaitAndClose

/* An ability entry that names a foe fights it straight after the gift: a wild
   Lv. 50 VAR_0x8000 with the ability VAR_0x8001 and, unless VAR_0x8002 is
   MOVE_NONE, that one move (with VAR_0x8003 as a second, if set) in place of
   its own. The new Pokemon is
   not in the lead, so switch it in on the first turn. */
TestKit_AbilityFoe:
    WaitButton
    CloseMessage
    TestKitStartWildBattle VAR_0x8000, 50, VAR_0x8001, VAR_0x8002, VAR_0x8003, MOVE_NONE, MOVE_NONE
    GoTo TestKit_AfterBattle

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

TestKit_SetAbility:
    TestKitSetPartyMonAbility VAR_0x8005, VAR_0x800B
    Return

/* Element 5: one entry per new ability, each a Lv. 50 Pokemon that carries it,
   given with the ability set whatever its personality rolls, and four moves
   that show it. docs/oxide/test-kit.md says what to look for. Add an entry
   with a menu line, its text in res/testkit/, and a block like the others. */
TestKit_Abilities:
    GetPartyCount VAR_0x8005
    GoToIfGe VAR_0x8005, 6, TestKit_PartyFull
    Message TestKit_Text_WhichAbility
    InitLocalTextListMenu 1, 1, 0, VAR_0x8004
    AddListMenuEntry TestKit_Text_MenuAbilityBeastBoost, 0
    AddListMenuEntry TestKit_Text_MenuAbilitySoulHeart, 1
    AddListMenuEntry TestKit_Text_MenuAbilitySapSipper, 2
    AddListMenuEntry TestKit_Text_MenuAbilityBulletproof, 3
    AddListMenuEntry TestKit_Text_MenuAbilityOvercoat, 4
    AddListMenuEntry TestKit_Text_MenuAbilityPurifyingSalt, 5
    AddListMenuEntry TestKit_Text_MenuAbilityCorrosion, 6
    AddListMenuEntry TestKit_Text_MenuAbilityCompetitive, 7
    AddListMenuEntry TestKit_Text_MenuAbilityDefiant, 8
    AddListMenuEntry TestKit_Text_MenuAbilityBigPecks, 9
    AddListMenuEntry TestKit_Text_MenuAbilityFlowerVeil, 10
    AddListMenuEntry TestKit_Text_MenuAbilityContrary, 11
    AddListMenuEntry TestKit_Text_MenuAbilityMirrorArmor, 12
    AddListMenuEntry TestKit_Text_MenuAbilityPrankster, 13
    AddListMenuEntry TestKit_Text_MenuAbilityGaleWings, 14
    AddListMenuEntry TestKit_Text_MenuAbilityQueenlyMajesty, 15
    AddListMenuEntry TestKit_Text_MenuAbilityIronBarbs, 16
    AddListMenuEntry TestKit_Text_MenuAbilityWeakArmor, 17
    AddListMenuEntry TestKit_Text_MenuAbilityCursedBody, 18
    AddListMenuEntry TestKit_Text_MenuAbilityWaterCompaction, 19
    AddListMenuEntry TestKit_Text_MenuAbilityToxicDebris, 20
    AddListMenuEntry TestKit_Text_MenuAbilityBerserk, 21
    AddListMenuEntry TestKit_Text_MenuAbilityGooey, 22
    AddListMenuEntry TestKit_Text_MenuAbilityMummy, 23
    AddListMenuEntry TestKit_Text_MenuAbilityWanderingSpirit, 24
    AddListMenuEntry TestKit_Text_MenuAbilityEntrainment, 25
    AddListMenuEntry TestKit_Text_MenuAbilityAbilityList, 26
    AddListMenuEntry TestKit_Text_MenuAbilityMore, 27
    ShowListMenu
    GoToIfEq VAR_0x8004, 0, TestKit_AbilityBeastBoost
    GoToIfEq VAR_0x8004, 1, TestKit_AbilitySoulHeart
    GoToIfEq VAR_0x8004, 2, TestKit_AbilitySapSipper
    GoToIfEq VAR_0x8004, 3, TestKit_AbilityBulletproof
    GoToIfEq VAR_0x8004, 4, TestKit_AbilityOvercoat
    GoToIfEq VAR_0x8004, 5, TestKit_AbilityPurifyingSalt
    GoToIfEq VAR_0x8004, 6, TestKit_AbilityCorrosion
    GoToIfEq VAR_0x8004, 7, TestKit_AbilityCompetitive
    GoToIfEq VAR_0x8004, 8, TestKit_AbilityDefiant
    GoToIfEq VAR_0x8004, 9, TestKit_AbilityBigPecks
    GoToIfEq VAR_0x8004, 10, TestKit_AbilityFlowerVeil
    GoToIfEq VAR_0x8004, 11, TestKit_AbilityContrary
    GoToIfEq VAR_0x8004, 12, TestKit_AbilityMirrorArmor
    GoToIfEq VAR_0x8004, 13, TestKit_AbilityPrankster
    GoToIfEq VAR_0x8004, 14, TestKit_AbilityGaleWings
    GoToIfEq VAR_0x8004, 15, TestKit_AbilityQueenlyMajesty
    GoToIfEq VAR_0x8004, 16, TestKit_AbilityIronBarbs
    GoToIfEq VAR_0x8004, 17, TestKit_AbilityWeakArmor
    GoToIfEq VAR_0x8004, 18, TestKit_AbilityCursedBody
    GoToIfEq VAR_0x8004, 19, TestKit_AbilityWaterCompaction
    GoToIfEq VAR_0x8004, 20, TestKit_AbilityToxicDebris
    GoToIfEq VAR_0x8004, 21, TestKit_AbilityBerserk
    GoToIfEq VAR_0x8004, 22, TestKit_AbilityGooey
    GoToIfEq VAR_0x8004, 23, TestKit_AbilityMummy
    GoToIfEq VAR_0x8004, 24, TestKit_AbilityWanderingSpirit
    GoToIfEq VAR_0x8004, 25, TestKit_AbilityEntrainment
    GoToIfEq VAR_0x8004, 26, TestKit_AbilityAbilityList
    GoToIfEq VAR_0x8004, 27, TestKit_Abilities2
    GoTo TestKit_Close

/* The field menu holds 28 entries, so the abilities go on over a second page. */
TestKit_Abilities2:
    Message TestKit_Text_WhichAbility
    InitLocalTextListMenu 1, 1, 0, VAR_0x8004
    AddListMenuEntry TestKit_Text_MenuAbilityFluffy, 0
    AddListMenuEntry TestKit_Text_MenuAbilityIceScales, 1
    AddListMenuEntry TestKit_Text_MenuAbilityWaterBubble, 2
    AddListMenuEntry TestKit_Text_MenuAbilityMerciless, 3
    AddListMenuEntry TestKit_Text_MenuAbilityLongReach, 4
    AddListMenuEntry TestKit_Text_MenuAbilityPixilate, 5
    AddListMenuEntry TestKit_Text_MenuAbilityLiquidVoice, 6
    AddListMenuEntry TestKit_Text_MenuAbilitySheerForce, 7
    AddListMenuEntry TestKit_Text_MenuAbilityAuras, 8
    AddListMenuEntry TestKit_Text_MenuAbilityAuraBreak, 9
    AddListMenuEntry TestKit_Text_MenuAbilityUnnerve, 10
    AddListMenuEntry TestKit_Text_MenuAbilityScreenCleaner, 11
    AddListMenuEntry TestKit_Text_MenuAbilityRegenerator, 12
    AddListMenuEntry TestKit_Text_MenuAbilityPastelVeil, 13
    AddListMenuEntry TestKit_Text_MenuAbilitySweetVeil, 14
    AddListMenuEntry TestKit_Text_MenuAbilityHarvest, 15
    AddListMenuEntry TestKit_Text_MenuAbilityProtean, 16
    AddListMenuEntry TestKit_Text_MenuAbilityLibero, 17
    AddListMenuEntry TestKit_Text_MenuAbilityInfiltrator, 18
    AddListMenuEntry TestKit_Text_MenuAbilityNeutralizingGas, 19
    ShowListMenu
    GoToIfEq VAR_0x8004, 0, TestKit_AbilityFluffy
    GoToIfEq VAR_0x8004, 1, TestKit_AbilityIceScales
    GoToIfEq VAR_0x8004, 2, TestKit_AbilityWaterBubble
    GoToIfEq VAR_0x8004, 3, TestKit_AbilityMerciless
    GoToIfEq VAR_0x8004, 4, TestKit_AbilityLongReach
    GoToIfEq VAR_0x8004, 5, TestKit_AbilityPixilate
    GoToIfEq VAR_0x8004, 6, TestKit_AbilityLiquidVoice
    GoToIfEq VAR_0x8004, 7, TestKit_AbilitySheerForce
    GoToIfEq VAR_0x8004, 8, TestKit_AbilityAuras
    GoToIfEq VAR_0x8004, 9, TestKit_AbilityAuraBreak
    GoToIfEq VAR_0x8004, 10, TestKit_AbilityUnnerve
    GoToIfEq VAR_0x8004, 11, TestKit_AbilityScreenCleaner
    GoToIfEq VAR_0x8004, 12, TestKit_AbilityRegenerator
    GoToIfEq VAR_0x8004, 13, TestKit_AbilityPastelVeil
    GoToIfEq VAR_0x8004, 14, TestKit_AbilitySweetVeil
    GoToIfEq VAR_0x8004, 15, TestKit_AbilityHarvest
    GoToIfEq VAR_0x8004, 16, TestKit_AbilityProtean
    GoToIfEq VAR_0x8004, 17, TestKit_AbilityLibero
    GoToIfEq VAR_0x8004, 18, TestKit_AbilityInfiltrator
    GoToIfEq VAR_0x8004, 19, TestKit_AbilityNeutralizingGas
    GoTo TestKit_Close

/* Beast Boost: Kartana's highest stat is Attack, so knocking out any wild
   Pokemon raises its Attack one stage, right after the faint message. */
TestKit_AbilityBeastBoost:
    SetVar VAR_0x800A, SPECIES_KARTANA
    SetVar VAR_0x800B, ABILITY_BEAST_BOOST
    SetVar VAR_0x8006, MOVE_LEAF_BLADE
    SetVar VAR_0x8007, MOVE_SACRED_SWORD
    SetVar VAR_0x8008, MOVE_SWORDS_DANCE
    SetVar VAR_0x8009, MOVE_NIGHT_SLASH
    GoTo TestKit_GivePokemonWithMoves

/* Soul Heart: when any other Pokemon faints, Magearna's Sp. Atk rises one
   stage, right after the faint message. */
TestKit_AbilitySoulHeart:
    SetVar VAR_0x800A, SPECIES_MAGEARNA
    SetVar VAR_0x800B, ABILITY_SOUL_HEART
    SetVar VAR_0x8006, MOVE_FLEUR_CANNON
    SetVar VAR_0x8007, MOVE_FLASH_CANNON
    SetVar VAR_0x8008, MOVE_DAZZLING_GLEAM
    SetVar VAR_0x8009, MOVE_CALM_MIND
    GoTo TestKit_GivePokemonWithMoves

/* Sap Sipper: a wild Bellsprout that knows only Vine Whip. Goodra takes no
   damage and its Attack rises instead, until it is at +6. */
TestKit_AbilitySapSipper:
    SetVar VAR_0x800A, SPECIES_GOODRA
    SetVar VAR_0x800B, ABILITY_SAP_SIPPER
    SetVar VAR_0x8006, MOVE_DRAGON_PULSE
    SetVar VAR_0x8007, MOVE_SLUDGE_BOMB
    SetVar VAR_0x8008, MOVE_THUNDERBOLT
    SetVar VAR_0x8009, MOVE_REST
    SetVar VAR_0x8000, SPECIES_BELLSPROUT
    SetVar VAR_0x8001, ABILITY_NONE
    SetVar VAR_0x8002, MOVE_VINE_WHIP
    GoTo TestKit_GivePokemonWithMoves

/* Bulletproof: a wild Chansey that knows only Egg Bomb, which Kommo-o's
   Bulletproof blocks every time. */
TestKit_AbilityBulletproof:
    SetVar VAR_0x800A, SPECIES_KOMMO_O
    SetVar VAR_0x800B, ABILITY_BULLETPROOF
    SetVar VAR_0x8006, MOVE_CLANGING_SCALES
    SetVar VAR_0x8007, MOVE_DRAGON_DANCE
    SetVar VAR_0x8008, MOVE_CLOSE_COMBAT
    SetVar VAR_0x8009, MOVE_IRON_DEFENSE
    SetVar VAR_0x8000, SPECIES_CHANSEY
    SetVar VAR_0x8001, ABILITY_NONE
    SetVar VAR_0x8002, MOVE_EGG_BOMB
    GoTo TestKit_GivePokemonWithMoves

/* Overcoat: a wild Paras that knows only Spore, which Overcoat blocks; once
   Mandibuzz sets up Sandstorm, Paras takes the sand damage and Mandibuzz
   does not. */
TestKit_AbilityOvercoat:
    SetVar VAR_0x800A, SPECIES_MANDIBUZZ
    SetVar VAR_0x800B, ABILITY_OVERCOAT
    SetVar VAR_0x8006, MOVE_SANDSTORM
    SetVar VAR_0x8007, MOVE_ROOST
    SetVar VAR_0x8008, MOVE_FOUL_PLAY
    SetVar VAR_0x8009, MOVE_TOXIC
    SetVar VAR_0x8000, SPECIES_PARAS
    SetVar VAR_0x8001, ABILITY_NONE
    SetVar VAR_0x8002, MOVE_SPORE
    GoTo TestKit_GivePokemonWithMoves

/* Purifying Salt: a wild Gengar that knows only Will-O-Wisp, which fails
   against Garganacl; Garganacl's own Rest fails too, since it cannot fall
   asleep. */
TestKit_AbilityPurifyingSalt:
    SetVar VAR_0x800A, SPECIES_GARGANACL
    SetVar VAR_0x800B, ABILITY_PURIFYING_SALT
    SetVar VAR_0x8006, MOVE_REST
    SetVar VAR_0x8007, MOVE_SALT_CURE
    SetVar VAR_0x8008, MOVE_STEALTH_ROCK
    SetVar VAR_0x8009, MOVE_RECOVER
    SetVar VAR_0x8000, SPECIES_GENGAR
    SetVar VAR_0x8001, ABILITY_NONE
    SetVar VAR_0x8002, MOVE_WILL_O_WISP
    GoTo TestKit_GivePokemonWithMoves

/* Corrosion: a wild Skarmory, a Steel type, which Salazzle's Toxic and
   Poison Gas poison all the same. */
TestKit_AbilityCorrosion:
    SetVar VAR_0x800A, SPECIES_SALAZZLE
    SetVar VAR_0x800B, ABILITY_CORROSION
    SetVar VAR_0x8006, MOVE_TOXIC
    SetVar VAR_0x8007, MOVE_POISON_GAS
    SetVar VAR_0x8008, MOVE_FLAMETHROWER
    SetVar VAR_0x8009, MOVE_SLUDGE_BOMB
    SetVar VAR_0x8000, SPECIES_SKARMORY
    SetVar VAR_0x8001, ABILITY_NONE
    SetVar VAR_0x8002, MOVE_NONE
    GoTo TestKit_GivePokemonWithMoves

/* Competitive: a wild Chansey that knows only Growl. Each Growl lowers
   Gothitelle's Attack and then raises its Sp. Atk two stages. */
TestKit_AbilityCompetitive:
    SetVar VAR_0x800A, SPECIES_GOTHITELLE
    SetVar VAR_0x800B, ABILITY_COMPETITIVE
    SetVar VAR_0x8006, MOVE_PSYCHIC
    SetVar VAR_0x8007, MOVE_CALM_MIND
    SetVar VAR_0x8008, MOVE_THUNDERBOLT
    SetVar VAR_0x8009, MOVE_THUNDER_WAVE
    SetVar VAR_0x8000, SPECIES_CHANSEY
    SetVar VAR_0x8001, ABILITY_NONE
    SetVar VAR_0x8002, MOVE_GROWL
    GoTo TestKit_GivePokemonWithMoves

/* Defiant: a wild Chansey that knows only Tail Whip. Each Tail Whip lowers
   Galarian Zapdos's Defense and then raises its Attack two stages. */
TestKit_AbilityDefiant:
    SetVar VAR_0x800A, SPECIES_GALARIAN_ZAPDOS
    SetVar VAR_0x800B, ABILITY_DEFIANT
    SetVar VAR_0x8006, MOVE_THUNDEROUS_KICK
    SetVar VAR_0x8007, MOVE_BRAVE_BIRD
    SetVar VAR_0x8008, MOVE_BULK_UP
    SetVar VAR_0x8009, MOVE_CLOSE_COMBAT
    SetVar VAR_0x8000, SPECIES_CHANSEY
    SetVar VAR_0x8001, ABILITY_NONE
    SetVar VAR_0x8002, MOVE_TAIL_WHIP
    GoTo TestKit_GivePokemonWithMoves

/* Big Pecks: a wild Chansey that knows only Tail Whip, which cannot lower
   Mandibuzz's Defense. */
TestKit_AbilityBigPecks:
    SetVar VAR_0x800A, SPECIES_MANDIBUZZ
    SetVar VAR_0x800B, ABILITY_BIG_PECKS
    SetVar VAR_0x8006, MOVE_FOUL_PLAY
    SetVar VAR_0x8007, MOVE_ROOST
    SetVar VAR_0x8008, MOVE_TOXIC
    SetVar VAR_0x8009, MOVE_BRAVE_BIRD
    SetVar VAR_0x8000, SPECIES_CHANSEY
    SetVar VAR_0x8001, ABILITY_NONE
    SetVar VAR_0x8002, MOVE_TAIL_WHIP
    GoTo TestKit_GivePokemonWithMoves

/* Flower Veil guards Grass types, and none of its three carriers is one, so
   the kit gives it to Tsareena. A wild Chansey that knows only Growl cannot
   lower Tsareena's Attack. */
TestKit_AbilityFlowerVeil:
    SetVar VAR_0x800A, SPECIES_TSAREENA
    SetVar VAR_0x800B, ABILITY_FLOWER_VEIL
    SetVar VAR_0x8006, MOVE_TROP_KICK
    SetVar VAR_0x8007, MOVE_POWER_WHIP
    SetVar VAR_0x8008, MOVE_KNOCK_OFF
    SetVar VAR_0x8009, MOVE_TRAILBLAZE
    SetVar VAR_0x8000, SPECIES_CHANSEY
    SetVar VAR_0x8001, ABILITY_NONE
    SetVar VAR_0x8002, MOVE_GROWL
    GoTo TestKit_GivePokemonWithMoves

/* Contrary: Serperior's Leaf Storm raises its Sp. Atk two stages instead of
   lowering it, and Coil lowers its stats instead of raising them. */
TestKit_AbilityContrary:
    SetVar VAR_0x800A, SPECIES_SERPERIOR
    SetVar VAR_0x800B, ABILITY_CONTRARY
    SetVar VAR_0x8006, MOVE_LEAF_STORM
    SetVar VAR_0x8007, MOVE_GIGA_DRAIN
    SetVar VAR_0x8008, MOVE_COIL
    SetVar VAR_0x8009, MOVE_GLARE
    GoTo TestKit_GivePokemonWithMoves

/* Mirror Armor: a wild Chansey that knows only Growl. Each Growl lowers
   Chansey's own Attack instead of Corviknight's. */
TestKit_AbilityMirrorArmor:
    SetVar VAR_0x800A, SPECIES_CORVIKNIGHT
    SetVar VAR_0x800B, ABILITY_MIRROR_ARMOR
    SetVar VAR_0x8006, MOVE_IRON_DEFENSE
    SetVar VAR_0x8007, MOVE_BODY_PRESS
    SetVar VAR_0x8008, MOVE_ROOST
    SetVar VAR_0x8009, MOVE_IRON_HEAD
    SetVar VAR_0x8000, SPECIES_CHANSEY
    SetVar VAR_0x8001, ABILITY_NONE
    SetVar VAR_0x8002, MOVE_GROWL
    GoTo TestKit_GivePokemonWithMoves

/* Prankster: a wild Weavile, faster than Klefki and a Dark type. Klefki's
   status moves go first; Thunder Wave and Swagger do not affect Weavile,
   while Spikes, aimed at its side, still works. */
TestKit_AbilityPrankster:
    SetVar VAR_0x800A, SPECIES_KLEFKI
    SetVar VAR_0x800B, ABILITY_PRANKSTER
    SetVar VAR_0x8006, MOVE_THUNDER_WAVE
    SetVar VAR_0x8007, MOVE_SPIKES
    SetVar VAR_0x8008, MOVE_SWAGGER
    SetVar VAR_0x8009, MOVE_FOUL_PLAY
    SetVar VAR_0x8000, SPECIES_WEAVILE
    SetVar VAR_0x8001, ABILITY_NONE
    SetVar VAR_0x8002, MOVE_NONE
    GoTo TestKit_GivePokemonWithMoves

/* Gale Wings: a wild Jolteon, faster than Talonflame. At full HP Brave Bird
   goes first; once Talonflame has taken damage it does not. */
TestKit_AbilityGaleWings:
    SetVar VAR_0x800A, SPECIES_TALONFLAME
    SetVar VAR_0x800B, ABILITY_GALE_WINGS
    SetVar VAR_0x8006, MOVE_BRAVE_BIRD
    SetVar VAR_0x8007, MOVE_FLARE_BLITZ
    SetVar VAR_0x8008, MOVE_ROOST
    SetVar VAR_0x8009, MOVE_SWORDS_DANCE
    SetVar VAR_0x8000, SPECIES_JOLTEON
    SetVar VAR_0x8001, ABILITY_NONE
    SetVar VAR_0x8002, MOVE_NONE
    GoTo TestKit_GivePokemonWithMoves

/* Queenly Majesty: a wild Rattata that knows only Quick Attack, which
   Tsareena's Queenly Majesty stops every time. */
TestKit_AbilityQueenlyMajesty:
    SetVar VAR_0x800A, SPECIES_TSAREENA
    SetVar VAR_0x800B, ABILITY_QUEENLY_MAJESTY
    SetVar VAR_0x8006, MOVE_TROP_KICK
    SetVar VAR_0x8007, MOVE_POWER_WHIP
    SetVar VAR_0x8008, MOVE_KNOCK_OFF
    SetVar VAR_0x8009, MOVE_TRAILBLAZE
    SetVar VAR_0x8000, SPECIES_RATTATA
    SetVar VAR_0x8001, ABILITY_NONE
    SetVar VAR_0x8002, MOVE_QUICK_ATTACK
    GoTo TestKit_GivePokemonWithMoves

/* Iron Barbs: a wild Rattata that knows only Tackle, which hurts it by an
   eighth of its HP each time it touches Ferrothorn. */
TestKit_AbilityIronBarbs:
    SetVar VAR_0x800A, SPECIES_FERROTHORN
    SetVar VAR_0x800B, ABILITY_IRON_BARBS
    SetVar VAR_0x8006, MOVE_IRON_DEFENSE
    SetVar VAR_0x8007, MOVE_LEECH_SEED
    SetVar VAR_0x8008, MOVE_GYRO_BALL
    SetVar VAR_0x8009, MOVE_SPIKES
    SetVar VAR_0x8000, SPECIES_RATTATA
    SetVar VAR_0x8001, ABILITY_NONE
    SetVar VAR_0x8002, MOVE_TACKLE
    GoTo TestKit_GivePokemonWithMoves

/* Weak Armor: a wild Rattata that knows only Tackle; each physical hit
   lowers Crustle's Defense and sharply raises its Speed. */
TestKit_AbilityWeakArmor:
    SetVar VAR_0x800A, SPECIES_CRUSTLE
    SetVar VAR_0x800B, ABILITY_WEAK_ARMOR
    SetVar VAR_0x8006, MOVE_SHELL_SMASH
    SetVar VAR_0x8007, MOVE_ROCK_SLIDE
    SetVar VAR_0x8008, MOVE_X_SCISSOR
    SetVar VAR_0x8009, MOVE_STEALTH_ROCK
    SetVar VAR_0x8000, SPECIES_RATTATA
    SetVar VAR_0x8001, ABILITY_NONE
    SetVar VAR_0x8002, MOVE_TACKLE
    GoTo TestKit_GivePokemonWithMoves

/* Cursed Body: a wild Rattata that knows only Tackle; about one hit in three
   disables Tackle, and Rattata then has to Struggle. */
TestKit_AbilityCursedBody:
    SetVar VAR_0x800A, SPECIES_JELLICENT
    SetVar VAR_0x800B, ABILITY_CURSED_BODY
    SetVar VAR_0x8006, MOVE_SCALD
    SetVar VAR_0x8007, MOVE_RECOVER
    SetVar VAR_0x8008, MOVE_WILL_O_WISP
    SetVar VAR_0x8009, MOVE_SHADOW_BALL
    SetVar VAR_0x8000, SPECIES_RATTATA
    SetVar VAR_0x8001, ABILITY_NONE
    SetVar VAR_0x8002, MOVE_TACKLE
    GoTo TestKit_GivePokemonWithMoves

/* Water Compaction: a wild Psyduck that knows only Water Gun, each hit of
   which sharply raises Palossand's Defense. */
TestKit_AbilityWaterCompaction:
    SetVar VAR_0x800A, SPECIES_PALOSSAND
    SetVar VAR_0x800B, ABILITY_WATERCOMPACTION
    SetVar VAR_0x8006, MOVE_SHORE_UP
    SetVar VAR_0x8007, MOVE_SHADOW_BALL
    SetVar VAR_0x8008, MOVE_EARTH_POWER
    SetVar VAR_0x8009, MOVE_IRON_DEFENSE
    SetVar VAR_0x8000, SPECIES_PSYDUCK
    SetVar VAR_0x8001, ABILITY_NONE
    SetVar VAR_0x8002, MOVE_WATER_GUN
    GoTo TestKit_GivePokemonWithMoves

/* Toxic Debris: a wild Rattata that knows only Tackle; each physical hit
   lays Toxic Spikes on the wild side, up to two layers. */
TestKit_AbilityToxicDebris:
    SetVar VAR_0x800A, SPECIES_GLIMMORA
    SetVar VAR_0x800B, ABILITY_TOXIC_DEBRIS
    SetVar VAR_0x8006, MOVE_POWER_GEM
    SetVar VAR_0x8007, MOVE_SLUDGE_WAVE
    SetVar VAR_0x8008, MOVE_MORTAL_SPIN
    SetVar VAR_0x8009, MOVE_EARTH_POWER
    SetVar VAR_0x8000, SPECIES_RATTATA
    SetVar VAR_0x8001, ABILITY_NONE
    SetVar VAR_0x8002, MOVE_TACKLE
    GoTo TestKit_GivePokemonWithMoves

/* Berserk: a wild Rhydon that knows only Rock Slide, strong enough to take
   Moltres below half its HP in a hit or two. */
TestKit_AbilityBerserk:
    SetVar VAR_0x800A, SPECIES_GALARIAN_MOLTRES
    SetVar VAR_0x800B, ABILITY_BERSERK
    SetVar VAR_0x8006, MOVE_FIERY_WRATH
    SetVar VAR_0x8007, MOVE_NASTY_PLOT
    SetVar VAR_0x8008, MOVE_AIR_SLASH
    SetVar VAR_0x8009, MOVE_ROOST
    SetVar VAR_0x8000, SPECIES_RHYDON
    SetVar VAR_0x8001, ABILITY_NONE
    SetVar VAR_0x8002, MOVE_ROCK_SLIDE
    GoTo TestKit_GivePokemonWithMoves

/* Gooey: a wild Rattata that knows only Tackle, whose Speed falls each time
   it touches Goodra. */
TestKit_AbilityGooey:
    SetVar VAR_0x800A, SPECIES_GOODRA
    SetVar VAR_0x800B, ABILITY_GOOEY
    SetVar VAR_0x8006, MOVE_DRAGON_PULSE
    SetVar VAR_0x8007, MOVE_SLUDGE_BOMB
    SetVar VAR_0x8008, MOVE_THUNDERBOLT
    SetVar VAR_0x8009, MOVE_REST
    SetVar VAR_0x8000, SPECIES_RATTATA
    SetVar VAR_0x8001, ABILITY_NONE
    SetVar VAR_0x8002, MOVE_TACKLE
    GoTo TestKit_GivePokemonWithMoves

/* Mummy: a wild Rattata that knows only Tackle, which takes Mummy the first
   time it touches Cofagrigus. */
TestKit_AbilityMummy:
    SetVar VAR_0x800A, SPECIES_COFAGRIGUS
    SetVar VAR_0x800B, ABILITY_MUMMY
    SetVar VAR_0x8006, MOVE_SHADOW_BALL
    SetVar VAR_0x8007, MOVE_WILL_O_WISP
    SetVar VAR_0x8008, MOVE_PROTECT
    SetVar VAR_0x8009, MOVE_NASTY_PLOT
    SetVar VAR_0x8000, SPECIES_RATTATA
    SetVar VAR_0x8001, ABILITY_NONE
    SetVar VAR_0x8002, MOVE_TACKLE
    GoTo TestKit_GivePokemonWithMoves

/* Wandering Spirit: a wild Rattata with Guts that knows only Tackle; the
   first Tackle swaps their abilities, and after it Runerigus has Guts, so
   later Tackles do nothing. */
TestKit_AbilityWanderingSpirit:
    SetVar VAR_0x800A, SPECIES_RUNERIGUS
    SetVar VAR_0x800B, ABILITY_WANDERING_SPIRIT
    SetVar VAR_0x8006, MOVE_EARTHQUAKE
    SetVar VAR_0x8007, MOVE_SHADOW_CLAW
    SetVar VAR_0x8008, MOVE_PROTECT
    SetVar VAR_0x8009, MOVE_STEALTH_ROCK
    SetVar VAR_0x8000, SPECIES_RATTATA
    SetVar VAR_0x8001, ABILITY_NONE
    SetVar VAR_0x8002, MOVE_TACKLE
    GoTo TestKit_GivePokemonWithMoves

/* Entrainment: a wild Rattata with Guts; Entrainment gives it Leavanny's
   Swarm, and the other three show the ability moves still working. */
TestKit_AbilityEntrainment:
    SetVar VAR_0x800A, SPECIES_LEAVANNY
    SetVar VAR_0x800B, ABILITY_SWARM
    SetVar VAR_0x8006, MOVE_ENTRAINMENT
    SetVar VAR_0x8007, MOVE_SKILL_SWAP
    SetVar VAR_0x8008, MOVE_ROLE_PLAY
    SetVar VAR_0x8009, MOVE_WORRY_SEED
    SetVar VAR_0x8000, SPECIES_RATTATA
    SetVar VAR_0x8001, ABILITY_NONE
    SetVar VAR_0x8002, MOVE_TACKLE
    GoTo TestKit_GivePokemonWithMoves

/* Ability list: a wild Rattata given Disguise, one of the abilities on the
   new list; all four moves fail against it. */
TestKit_AbilityAbilityList:
    SetVar VAR_0x800A, SPECIES_LEAVANNY
    SetVar VAR_0x800B, ABILITY_SWARM
    SetVar VAR_0x8006, MOVE_ENTRAINMENT
    SetVar VAR_0x8007, MOVE_SKILL_SWAP
    SetVar VAR_0x8008, MOVE_ROLE_PLAY
    SetVar VAR_0x8009, MOVE_GASTRO_ACID
    SetVar VAR_0x8000, SPECIES_RATTATA
    SetVar VAR_0x8001, ABILITY_DISGUISE
    SetVar VAR_0x8002, MOVE_TACKLE
    GoTo TestKit_GivePokemonWithMoves

/* Fluffy: a wild Eevee that knows Tackle and Ember; Fluffy halves the
   contact Tackle and doubles the Fire-type Ember, so Ember hits around twice
   as hard as Tackle, where without Fluffy it would hit about half as hard. */
TestKit_AbilityFluffy:
    SetVar VAR_0x800A, SPECIES_DUBWOOL
    SetVar VAR_0x800B, ABILITY_FLUFFY
    SetVar VAR_0x8006, MOVE_COTTON_GUARD
    SetVar VAR_0x8007, MOVE_BODY_PRESS
    SetVar VAR_0x8008, MOVE_WILD_CHARGE
    SetVar VAR_0x8009, MOVE_SWORDS_DANCE
    SetVar VAR_0x8000, SPECIES_EEVEE
    SetVar VAR_0x8001, ABILITY_NONE
    SetVar VAR_0x8002, MOVE_TACKLE
    SetVar VAR_0x8003, MOVE_EMBER
    GoTo TestKit_GivePokemonWithMoves

/* Ice Scales: a wild Porygon that knows Tackle and Swift; Ice Scales halves
   the special Swift, which then does less than Tackle, where without it
   Swift would do more. */
TestKit_AbilityIceScales:
    SetVar VAR_0x800A, SPECIES_FROSMOTH
    SetVar VAR_0x800B, ABILITY_ICE_SCALES
    SetVar VAR_0x8006, MOVE_QUIVER_DANCE
    SetVar VAR_0x8007, MOVE_ICE_BEAM
    SetVar VAR_0x8008, MOVE_BUG_BUZZ
    SetVar VAR_0x8009, MOVE_GIGA_DRAIN
    SetVar VAR_0x8000, SPECIES_PORYGON
    SetVar VAR_0x8001, ABILITY_NONE
    SetVar VAR_0x8002, MOVE_TACKLE
    SetVar VAR_0x8003, MOVE_SWIFT
    GoTo TestKit_GivePokemonWithMoves

/* Water Bubble: a wild Gengar that knows only Will-O-Wisp, which Water
   Bubble stops as Water Veil does. */
TestKit_AbilityWaterBubble:
    SetVar VAR_0x800A, SPECIES_ARAQUANID
    SetVar VAR_0x800B, ABILITY_WATER_BUBBLE
    SetVar VAR_0x8006, MOVE_LIQUIDATION
    SetVar VAR_0x8007, MOVE_LEECH_LIFE
    SetVar VAR_0x8008, MOVE_PROTECT
    SetVar VAR_0x8009, MOVE_MIRROR_COAT
    SetVar VAR_0x8000, SPECIES_GENGAR
    SetVar VAR_0x8001, ABILITY_NONE
    SetVar VAR_0x8002, MOVE_WILL_O_WISP
    GoTo TestKit_GivePokemonWithMoves

/* Merciless: a wild Rattata that knows only Growl; once Toxic has poisoned
   it, every Scald is a critical hit. */
TestKit_AbilityMerciless:
    SetVar VAR_0x800A, SPECIES_TOXAPEX
    SetVar VAR_0x800B, ABILITY_MERCILESS
    SetVar VAR_0x8006, MOVE_TOXIC
    SetVar VAR_0x8007, MOVE_SCALD
    SetVar VAR_0x8008, MOVE_RECOVER
    SetVar VAR_0x8009, MOVE_PROTECT
    SetVar VAR_0x8000, SPECIES_RATTATA
    SetVar VAR_0x8001, ABILITY_NONE
    SetVar VAR_0x8002, MOVE_GROWL
    GoTo TestKit_GivePokemonWithMoves

/* Long Reach: a wild Ferrothorn with Iron Barbs that knows only Iron
   Defense; Leaf Blade makes no contact, so Iron Barbs never hurts Decidueye. */
TestKit_AbilityLongReach:
    SetVar VAR_0x800A, SPECIES_DECIDUEYE
    SetVar VAR_0x800B, ABILITY_LONG_REACH
    SetVar VAR_0x8006, MOVE_LEAF_BLADE
    SetVar VAR_0x8007, MOVE_SHADOW_SNEAK
    SetVar VAR_0x8008, MOVE_SWORDS_DANCE
    SetVar VAR_0x8009, MOVE_ROOST
    SetVar VAR_0x8000, SPECIES_FERROTHORN
    SetVar VAR_0x8001, ABILITY_IRON_BARBS
    SetVar VAR_0x8002, MOVE_IRON_DEFENSE
    GoTo TestKit_GivePokemonWithMoves

/* Pixilate: a wild Misdreavus, a Ghost type, that knows only Growl; Hyper
   Voice and Quick Attack turn Fairy and hit it, where a Normal move would
   not affect it. */
TestKit_AbilityPixilate:
    SetVar VAR_0x800A, SPECIES_SYLVEON
    SetVar VAR_0x800B, ABILITY_PIXILATE
    SetVar VAR_0x8006, MOVE_HYPER_VOICE
    SetVar VAR_0x8007, MOVE_QUICK_ATTACK
    SetVar VAR_0x8008, MOVE_CALM_MIND
    SetVar VAR_0x8009, MOVE_WISH
    SetVar VAR_0x8000, SPECIES_MISDREAVUS
    SetVar VAR_0x8001, ABILITY_NONE
    SetVar VAR_0x8002, MOVE_GROWL
    GoTo TestKit_GivePokemonWithMoves

/* Liquid Voice: a wild Vaporeon with Water Absorb that knows only Growl;
   Hyper Voice turns Water, so Water Absorb takes it and restores Vaporeon's
   HP. */
TestKit_AbilityLiquidVoice:
    SetVar VAR_0x800A, SPECIES_PRIMARINA
    SetVar VAR_0x800B, ABILITY_LIQUID_VOICE
    SetVar VAR_0x8006, MOVE_HYPER_VOICE
    SetVar VAR_0x8007, MOVE_MOONBLAST
    SetVar VAR_0x8008, MOVE_CALM_MIND
    SetVar VAR_0x8009, MOVE_SPARKLING_ARIA
    SetVar VAR_0x8000, SPECIES_VAPOREON
    SetVar VAR_0x8001, ABILITY_WATER_ABSORB
    SetVar VAR_0x8002, MOVE_GROWL
    GoTo TestKit_GivePokemonWithMoves

/* Sheer Force: a wild Chansey that knows only Growl; Flame Charge never
   raises Toucannon's Speed, since Sheer Force strips that for more power. */
TestKit_AbilitySheerForce:
    SetVar VAR_0x800A, SPECIES_TOUCANNON
    SetVar VAR_0x800B, ABILITY_SHEER_FORCE
    SetVar VAR_0x8006, MOVE_FLAME_CHARGE
    SetVar VAR_0x8007, MOVE_BRAVE_BIRD
    SetVar VAR_0x8008, MOVE_BULLET_SEED
    SetVar VAR_0x8009, MOVE_ROOST
    SetVar VAR_0x8000, SPECIES_CHANSEY
    SetVar VAR_0x8001, ABILITY_NONE
    SetVar VAR_0x8002, MOVE_GROWL
    GoTo TestKit_GivePokemonWithMoves

/* Auras: a wild Yveltal with Dark Aura that knows only Dark Pulse; both
   announce their auras, Yveltal as the battle starts and Xerneas as it comes
   in. */
TestKit_AbilityAuras:
    SetVar VAR_0x800A, SPECIES_XERNEAS
    SetVar VAR_0x800B, ABILITY_FAIRY_AURA
    SetVar VAR_0x8006, MOVE_MOONBLAST
    SetVar VAR_0x8007, MOVE_GEOMANCY
    SetVar VAR_0x8008, MOVE_PSYSHOCK
    SetVar VAR_0x8009, MOVE_FOCUS_BLAST
    SetVar VAR_0x8000, SPECIES_YVELTAL
    SetVar VAR_0x8001, ABILITY_DARK_AURA
    SetVar VAR_0x8002, MOVE_DARK_PULSE
    GoTo TestKit_GivePokemonWithMoves

/* Aura Break: a wild Yveltal with Dark Aura that knows only Dark Pulse;
   Zygarde announces Aura Break as it comes in. */
TestKit_AbilityAuraBreak:
    SetVar VAR_0x800A, SPECIES_ZYGARDE_50
    SetVar VAR_0x800B, ABILITY_AURA_BREAK
    SetVar VAR_0x8006, MOVE_THOUSAND_ARROWS
    SetVar VAR_0x8007, MOVE_DRAGON_DANCE
    SetVar VAR_0x8008, MOVE_COIL
    SetVar VAR_0x8009, MOVE_REST
    SetVar VAR_0x8000, SPECIES_YVELTAL
    SetVar VAR_0x8001, ABILITY_DARK_AURA
    SetVar VAR_0x8002, MOVE_DARK_PULSE
    GoTo TestKit_GivePokemonWithMoves

/* Unnerve: any foe; Galvantula announces Unnerve as it comes in. */
TestKit_AbilityUnnerve:
    SetVar VAR_0x800A, SPECIES_GALVANTULA
    SetVar VAR_0x800B, ABILITY_UNNERVE
    SetVar VAR_0x8006, MOVE_THUNDER
    SetVar VAR_0x8007, MOVE_BUG_BUZZ
    SetVar VAR_0x8008, MOVE_ENERGY_BALL
    SetVar VAR_0x8009, MOVE_STICKY_WEB
    SetVar VAR_0x8000, SPECIES_RATTATA
    SetVar VAR_0x8001, ABILITY_NONE
    SetVar VAR_0x8002, MOVE_GROWL
    GoTo TestKit_GivePokemonWithMoves

/* Screen Cleaner: a wild Chansey that knows Reflect and Light Screen; once a
   screen is up, switch Mr. Rime in and it ends them. */
TestKit_AbilityScreenCleaner:
    SetVar VAR_0x800A, SPECIES_MR_RIME
    SetVar VAR_0x800B, ABILITY_SCREEN_CLEANER
    SetVar VAR_0x8006, MOVE_FREEZE_DRY
    SetVar VAR_0x8007, MOVE_PSYCHIC
    SetVar VAR_0x8008, MOVE_RAPID_SPIN
    SetVar VAR_0x8009, MOVE_SLACK_OFF
    SetVar VAR_0x8000, SPECIES_CHANSEY
    SetVar VAR_0x8001, ABILITY_NONE
    SetVar VAR_0x8002, MOVE_REFLECT
    SetVar VAR_0x8003, MOVE_LIGHT_SCREEN
    GoTo TestKit_GivePokemonWithMoves

/* Regenerator: a wild Rattata that knows only Tackle; switch the hurt
   Toxapex out and back, and it has a third of its HP back. */
TestKit_AbilityRegenerator:
    SetVar VAR_0x800A, SPECIES_TOXAPEX
    SetVar VAR_0x800B, ABILITY_REGENERATOR
    SetVar VAR_0x8006, MOVE_SCALD
    SetVar VAR_0x8007, MOVE_TOXIC
    SetVar VAR_0x8008, MOVE_HAZE
    SetVar VAR_0x8009, MOVE_RECOVER
    SetVar VAR_0x8000, SPECIES_RATTATA
    SetVar VAR_0x8001, ABILITY_NONE
    SetVar VAR_0x8002, MOVE_TACKLE
    GoTo TestKit_GivePokemonWithMoves

/* Pastel Veil: a wild Grimer that knows only Toxic, which Pastel Veil stops. */
TestKit_AbilityPastelVeil:
    SetVar VAR_0x800A, SPECIES_GALARIAN_RAPIDASH
    SetVar VAR_0x800B, ABILITY_PASTEL_VEIL
    SetVar VAR_0x8006, MOVE_PLAY_ROUGH
    SetVar VAR_0x8007, MOVE_HIGH_HORSEPOWER
    SetVar VAR_0x8008, MOVE_MORNING_SUN
    SetVar VAR_0x8009, MOVE_QUICK_ATTACK
    SetVar VAR_0x8000, SPECIES_GRIMER
    SetVar VAR_0x8001, ABILITY_NONE
    SetVar VAR_0x8002, MOVE_TOXIC
    GoTo TestKit_GivePokemonWithMoves

/* Sweet Veil: a wild Jigglypuff that knows only Sing, which Sweet Veil keeps
   from putting Tsareena to sleep. */
TestKit_AbilitySweetVeil:
    SetVar VAR_0x800A, SPECIES_TSAREENA
    SetVar VAR_0x800B, ABILITY_SWEET_VEIL
    SetVar VAR_0x8006, MOVE_TROP_KICK
    SetVar VAR_0x8007, MOVE_POWER_WHIP
    SetVar VAR_0x8008, MOVE_TRIPLE_AXEL
    SetVar VAR_0x8009, MOVE_QUICK_ATTACK
    SetVar VAR_0x8000, SPECIES_JIGGLYPUFF
    SetVar VAR_0x8001, ABILITY_NONE
    SetVar VAR_0x8002, MOVE_SING
    GoTo TestKit_GivePokemonWithMoves

/* Harvest: holding a Sitrus Berry; Substitute twice takes Arboliva below
   half its HP, it eats the Berry, and Harvest then grows it back half the
   time at the end of a turn. */
TestKit_AbilityHarvest:
    SetVar VAR_0x800A, SPECIES_ARBOLIVA
    SetVar VAR_0x800B, ABILITY_HARVEST
    SetVar VAR_0x8006, MOVE_SUBSTITUTE
    SetVar VAR_0x8007, MOVE_HYPER_VOICE
    SetVar VAR_0x8008, MOVE_LEECH_SEED
    SetVar VAR_0x8009, MOVE_PROTECT
    SetVar VAR_0x8000, SPECIES_RATTATA
    SetVar VAR_0x8001, ABILITY_NONE
    SetVar VAR_0x8002, MOVE_GROWL
    SetVar VAR_0x8004, ITEM_SITRUS_BERRY
    GoTo TestKit_GivePokemonWithItem

/* Protean: any foe; Greninja's first move gives it that move's type, and no
   later one does until it switches out and back in. */
TestKit_AbilityProtean:
    SetVar VAR_0x800A, SPECIES_GRENINJA
    SetVar VAR_0x800B, ABILITY_PROTEAN
    SetVar VAR_0x8006, MOVE_SURF
    SetVar VAR_0x8007, MOVE_DARK_PULSE
    SetVar VAR_0x8008, MOVE_ICE_BEAM
    SetVar VAR_0x8009, MOVE_U_TURN
    SetVar VAR_0x8000, SPECIES_RATTATA
    SetVar VAR_0x8001, ABILITY_NONE
    SetVar VAR_0x8002, MOVE_GROWL
    GoTo TestKit_GivePokemonWithMoves

/* Libero: as Protean, for Cinderace. */
TestKit_AbilityLibero:
    SetVar VAR_0x800A, SPECIES_CINDERACE
    SetVar VAR_0x800B, ABILITY_LIBERO
    SetVar VAR_0x8006, MOVE_PYRO_BALL
    SetVar VAR_0x8007, MOVE_COURT_CHANGE
    SetVar VAR_0x8008, MOVE_SUCKER_PUNCH
    SetVar VAR_0x8009, MOVE_U_TURN
    SetVar VAR_0x8000, SPECIES_RATTATA
    SetVar VAR_0x8001, ABILITY_NONE
    SetVar VAR_0x8002, MOVE_GROWL
    GoTo TestKit_GivePokemonWithMoves

/* Infiltrator: a wild Chansey that knows only Mist; Fake Tears still lowers
   its Sp. Def through the Mist. */
TestKit_AbilityInfiltrator:
    SetVar VAR_0x800A, SPECIES_CHANDELURE
    SetVar VAR_0x800B, ABILITY_INFILTRATOR
    SetVar VAR_0x8006, MOVE_SHADOW_BALL
    SetVar VAR_0x8007, MOVE_FLAMETHROWER
    SetVar VAR_0x8008, MOVE_FAKE_TEARS
    SetVar VAR_0x8009, MOVE_ENERGY_BALL
    SetVar VAR_0x8000, SPECIES_CHANSEY
    SetVar VAR_0x8001, ABILITY_NONE
    SetVar VAR_0x8002, MOVE_MIST
    GoTo TestKit_GivePokemonWithMoves

/* Neutralizing Gas: a wild Chansey given Pressure that knows only Growl.
   Pressure announces itself and doubles the PP Weezing's moves cost, so it
   shows the gas arriving, the suppression, and the gas leaving, after which
   Pressure announces itself again. */
TestKit_AbilityNeutralizingGas:
    SetVar VAR_0x800A, SPECIES_GALARIAN_WEEZING
    SetVar VAR_0x800B, ABILITY_NEUTRALIZING_GAS
    SetVar VAR_0x8006, MOVE_SLUDGE_BOMB
    SetVar VAR_0x8007, MOVE_STRANGE_STEAM
    SetVar VAR_0x8008, MOVE_WILL_O_WISP
    SetVar VAR_0x8009, MOVE_PROTECT
    SetVar VAR_0x8000, SPECIES_CHANSEY
    SetVar VAR_0x8001, ABILITY_PRESSURE
    SetVar VAR_0x8002, MOVE_GROWL
    GoTo TestKit_GivePokemonWithMoves

/* The staples survey's engine rulings (Ian, 2026-09-26): the later games'
   rules for native abilities, type immunities, critical hits, Defog and Rapid
   Spin. Each entry is built as an ability entry is, with a foe where it needs
   one. */
TestKit_Staples:
    Message TestKit_Text_WhichRule
    InitLocalTextListMenu 1, 1, 0, VAR_0x8004
    AddListMenuEntry TestKit_Text_MenuStapleSturdy, 0
    AddListMenuEntry TestKit_Text_MenuStapleLightningRod, 1
    AddListMenuEntry TestKit_Text_MenuStapleStormDrain, 2
    AddListMenuEntry TestKit_Text_MenuStapleIntimidate, 3
    AddListMenuEntry TestKit_Text_MenuStapleOblivious, 4
    AddListMenuEntry TestKit_Text_MenuStapleIlluminate, 5
    AddListMenuEntry TestKit_Text_MenuStapleSynchronize, 6
    ShowListMenu
    GoToIfEq VAR_0x8004, 0, TestKit_StapleSturdy
    GoToIfEq VAR_0x8004, 1, TestKit_StapleLightningRod
    GoToIfEq VAR_0x8004, 2, TestKit_StapleStormDrain
    GoToIfEq VAR_0x8004, 3, TestKit_StapleIntimidate
    GoToIfEq VAR_0x8004, 4, TestKit_StapleOblivious
    GoToIfEq VAR_0x8004, 5, TestKit_StapleIlluminate
    GoToIfEq VAR_0x8004, 6, TestKit_StapleSynchronize
    GoTo TestKit_Close

/* Sturdy: a Geodude given Sturdy, against a wild Vaporeon that knows only
   Surf, which does four times damage to it. Rest takes Geodude back to full
   HP, so Sturdy holds again. */
TestKit_StapleSturdy:
    SetVar VAR_0x800A, SPECIES_GEODUDE
    SetVar VAR_0x800B, ABILITY_STURDY
    SetVar VAR_0x8006, MOVE_REST
    SetVar VAR_0x8007, MOVE_ROCK_SLIDE
    SetVar VAR_0x8008, MOVE_DEFENSE_CURL
    SetVar VAR_0x8009, MOVE_MAGNITUDE
    SetVar VAR_0x8000, SPECIES_VAPOREON
    SetVar VAR_0x8001, ABILITY_NONE
    SetVar VAR_0x8002, MOVE_SURF
    GoTo TestKit_GivePokemonWithMoves

/* Lightning Rod: a Raichu given Lightning Rod, against a wild Jolteon that
   knows only Thunderbolt. */
TestKit_StapleLightningRod:
    SetVar VAR_0x800A, SPECIES_RAICHU
    SetVar VAR_0x800B, ABILITY_LIGHTNING_ROD
    SetVar VAR_0x8006, MOVE_THUNDERBOLT
    SetVar VAR_0x8007, MOVE_NASTY_PLOT
    SetVar VAR_0x8008, MOVE_SURF
    SetVar VAR_0x8009, MOVE_FOCUS_BLAST
    SetVar VAR_0x8000, SPECIES_JOLTEON
    SetVar VAR_0x8001, ABILITY_NONE
    SetVar VAR_0x8002, MOVE_THUNDERBOLT
    GoTo TestKit_GivePokemonWithMoves

/* Storm Drain: a Gastrodon given Storm Drain, against a wild Vaporeon that
   knows only Surf. */
TestKit_StapleStormDrain:
    SetVar VAR_0x800A, SPECIES_GASTRODON
    SetVar VAR_0x800B, ABILITY_STORM_DRAIN
    SetVar VAR_0x8006, MOVE_EARTH_POWER
    SetVar VAR_0x8007, MOVE_ICE_BEAM
    SetVar VAR_0x8008, MOVE_RECOVER
    SetVar VAR_0x8009, MOVE_TOXIC
    SetVar VAR_0x8000, SPECIES_VAPOREON
    SetVar VAR_0x8001, ABILITY_NONE
    SetVar VAR_0x8002, MOVE_SURF
    GoTo TestKit_GivePokemonWithMoves

/* Intimidate blocked: a Staraptor with Intimidate, against a wild Lucario
   given Inner Focus that knows only Splash. */
TestKit_StapleIntimidate:
    SetVar VAR_0x800A, SPECIES_STARAPTOR
    SetVar VAR_0x800B, ABILITY_INTIMIDATE
    SetVar VAR_0x8006, MOVE_BRAVE_BIRD
    SetVar VAR_0x8007, MOVE_CLOSE_COMBAT
    SetVar VAR_0x8008, MOVE_ROOST
    SetVar VAR_0x8009, MOVE_U_TURN
    SetVar VAR_0x8000, SPECIES_LUCARIO
    SetVar VAR_0x8001, ABILITY_INNER_FOCUS
    SetVar VAR_0x8002, MOVE_SPLASH
    GoTo TestKit_GivePokemonWithMoves

/* Oblivious and Taunt: a Weavile with Taunt, against a wild Slowbro given
   Oblivious that knows only Growl. */
TestKit_StapleOblivious:
    SetVar VAR_0x800A, SPECIES_WEAVILE
    SetVar VAR_0x800B, ABILITY_NONE
    SetVar VAR_0x8006, MOVE_TAUNT
    SetVar VAR_0x8007, MOVE_NIGHT_SLASH
    SetVar VAR_0x8008, MOVE_ICE_SHARD
    SetVar VAR_0x8009, MOVE_SWORDS_DANCE
    SetVar VAR_0x8000, SPECIES_SLOWBRO
    SetVar VAR_0x8001, ABILITY_OBLIVIOUS
    SetVar VAR_0x8002, MOVE_GROWL
    GoTo TestKit_GivePokemonWithMoves

/* Keen Eye and Illuminate: a Starmie given Illuminate, against a wild
   Chansey that knows Double Team and Sand Attack. Keen Eye works the same
   way. */
TestKit_StapleIlluminate:
    SetVar VAR_0x800A, SPECIES_STARMIE
    SetVar VAR_0x800B, ABILITY_ILLUMINATE
    SetVar VAR_0x8006, MOVE_SURF
    SetVar VAR_0x8007, MOVE_THUNDERBOLT
    SetVar VAR_0x8008, MOVE_ICE_BEAM
    SetVar VAR_0x8009, MOVE_RECOVER
    SetVar VAR_0x8000, SPECIES_CHANSEY
    SetVar VAR_0x8001, ABILITY_NONE
    SetVar VAR_0x8002, MOVE_DOUBLE_TEAM
    SetVar VAR_0x8003, MOVE_SAND_ATTACK
    GoTo TestKit_GivePokemonWithMoves

/* Synchronize: an Espeon given Synchronize, against a wild Chansey that
   knows only Toxic. */
TestKit_StapleSynchronize:
    SetVar VAR_0x800A, SPECIES_ESPEON
    SetVar VAR_0x800B, ABILITY_SYNCHRONIZE
    SetVar VAR_0x8006, MOVE_PSYCHIC
    SetVar VAR_0x8007, MOVE_CALM_MIND
    SetVar VAR_0x8008, MOVE_MORNING_SUN
    SetVar VAR_0x8009, MOVE_PROTECT
    SetVar VAR_0x8000, SPECIES_CHANSEY
    SetVar VAR_0x8001, ABILITY_NONE
    SetVar VAR_0x8002, MOVE_TOXIC
    GoTo TestKit_GivePokemonWithMoves

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

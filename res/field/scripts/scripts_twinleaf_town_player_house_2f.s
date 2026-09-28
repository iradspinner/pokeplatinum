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
    AddListMenuEntry TestKit_Text_MenuLevelCaps, 16
    AddListMenuEntry TestKit_Text_MenuSpriteHeights, 17
    AddListMenuEntry TestKit_Text_MenuItems, 18
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
    GoToIfEq VAR_0x8004, 16, TestKit_LevelCaps
    GoToIfEq VAR_0x8004, 17, TestKit_SpriteHeights
    GoToIfEq VAR_0x8004, 18, TestKit_Items
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
   its first slot and one Rare Candy should evolve it. It is Lv. 15, below a
   new game's level cap of 16, so the candy is not refused. */
TestKit_Eevee:
    GetPartyCount VAR_0x8005
    GoToIfGe VAR_0x8005, 6, TestKit_PartyFull
    GivePokemon SPECIES_EEVEE, 15, ITEM_NONE, VAR_RESULT
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

/* Four new species in turn, to see them seated on the field: Wooloo,
   Rookidee and Fletchling stand on their shadows, and Sinistea hovers just
   above its own. Lv. 5, so any lead can run. */
TestKit_SpriteHeights:
    Message TestKit_Text_SpriteHeights
    WaitButton
    CloseMessage
    StartWildBattle SPECIES_WOOLOO, 5
    CheckWonBattle VAR_RESULT
    GoToIfEq VAR_RESULT, FALSE, TestKit_LostBattle
    StartWildBattle SPECIES_SINISTEA, 5
    CheckWonBattle VAR_RESULT
    GoToIfEq VAR_RESULT, FALSE, TestKit_LostBattle
    StartWildBattle SPECIES_ROOKIDEE, 5
    CheckWonBattle VAR_RESULT
    GoToIfEq VAR_RESULT, FALSE, TestKit_LostBattle
    StartWildBattle SPECIES_FLETCHLING, 5
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
    AddListMenuEntry TestKit_Text_MenuSetMore, 27
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
    GoToIfEq VAR_0x8004, 27, TestKit_MoveSets2
    GoTo TestKit_Close

/* The field menu holds 28 entries (FIELD_MENU_ENTRIES_MAX), so the sets go on
   over a second page, as the abilities do. */
TestKit_MoveSets2:
    Message TestKit_Text_WhichSet
    InitLocalTextListMenu 1, 1, 0, VAR_0x8004
    AddListMenuEntry TestKit_Text_MenuSet28, 0
    AddListMenuEntry TestKit_Text_MenuSet29, 1
    AddListMenuEntry TestKit_Text_MenuSet30, 2
    AddListMenuEntry TestKit_Text_MenuSet31, 3
    AddListMenuEntry TestKit_Text_MenuSet32, 4
    AddListMenuEntry TestKit_Text_MenuSet33, 5
    AddListMenuEntry TestKit_Text_MenuSet34, 6
    AddListMenuEntry TestKit_Text_MenuSet35, 7
    AddListMenuEntry TestKit_Text_MenuSet36, 8
    AddListMenuEntry TestKit_Text_MenuSet37, 9
    AddListMenuEntry TestKit_Text_MenuSet38, 10
    AddListMenuEntry TestKit_Text_MenuSet39, 11
    AddListMenuEntry TestKit_Text_MenuSet40, 12
    AddListMenuEntry TestKit_Text_MenuSet41, 13
    AddListMenuEntry TestKit_Text_MenuSet42, 14
    AddListMenuEntry TestKit_Text_MenuSet43, 15
    AddListMenuEntry TestKit_Text_MenuSet44, 16
    AddListMenuEntry TestKit_Text_MenuSet45, 17
    AddListMenuEntry TestKit_Text_MenuSet46, 18
    AddListMenuEntry TestKit_Text_MenuSet47, 19
    AddListMenuEntry TestKit_Text_MenuSet48, 20
    AddListMenuEntry TestKit_Text_MenuSet49, 21
    AddListMenuEntry TestKit_Text_MenuSet50, 22
    AddListMenuEntry TestKit_Text_MenuSet51, 23
    AddListMenuEntry TestKit_Text_MenuSet52, 24
    AddListMenuEntry TestKit_Text_MenuSet53, 25
    AddListMenuEntry TestKit_Text_MenuSet54, 26
    AddListMenuEntry TestKit_Text_MenuSetMore, 27
    ShowListMenu
    GoToIfEq VAR_0x8004, 0, TestKit_MoveSet28
    GoToIfEq VAR_0x8004, 1, TestKit_MoveSet29
    GoToIfEq VAR_0x8004, 2, TestKit_MoveSet30
    GoToIfEq VAR_0x8004, 3, TestKit_MoveSet31
    GoToIfEq VAR_0x8004, 4, TestKit_MoveSet32
    GoToIfEq VAR_0x8004, 5, TestKit_MoveSet33
    GoToIfEq VAR_0x8004, 6, TestKit_MoveSet34
    GoToIfEq VAR_0x8004, 7, TestKit_MoveSet35
    GoToIfEq VAR_0x8004, 8, TestKit_MoveSet36
    GoToIfEq VAR_0x8004, 9, TestKit_MoveSet37
    GoToIfEq VAR_0x8004, 10, TestKit_MoveSet38
    GoToIfEq VAR_0x8004, 11, TestKit_MoveSet39
    GoToIfEq VAR_0x8004, 12, TestKit_MoveSet40
    GoToIfEq VAR_0x8004, 13, TestKit_MoveSet41
    GoToIfEq VAR_0x8004, 14, TestKit_MoveSet42
    GoToIfEq VAR_0x8004, 15, TestKit_MoveSet43
    GoToIfEq VAR_0x8004, 16, TestKit_MoveSet44
    GoToIfEq VAR_0x8004, 17, TestKit_MoveSet45
    GoToIfEq VAR_0x8004, 18, TestKit_MoveSet46
    GoToIfEq VAR_0x8004, 19, TestKit_MoveSet47
    GoToIfEq VAR_0x8004, 20, TestKit_MoveSet48
    GoToIfEq VAR_0x8004, 21, TestKit_MoveSet49
    GoToIfEq VAR_0x8004, 22, TestKit_MoveSet50
    GoToIfEq VAR_0x8004, 23, TestKit_MoveSet51
    GoToIfEq VAR_0x8004, 24, TestKit_MoveSet52
    GoToIfEq VAR_0x8004, 25, TestKit_MoveSet53
    GoToIfEq VAR_0x8004, 26, TestKit_MoveSet54
    GoToIfEq VAR_0x8004, 27, TestKit_MoveSets3
    GoTo TestKit_Close

/* The third page, from set 55 on (2026-09-27): the second filled up with
   Shore Up, Meteor Beam, Electro Shot and Mind Blown. */
TestKit_MoveSets3:
    Message TestKit_Text_WhichSet
    InitLocalTextListMenu 1, 1, 0, VAR_0x8004
    AddListMenuEntry TestKit_Text_MenuSet55, 0
    AddListMenuEntry TestKit_Text_MenuSet56, 1
    AddListMenuEntry TestKit_Text_MenuSet57, 2
    AddListMenuEntry TestKit_Text_MenuSet58, 3
    AddListMenuEntry TestKit_Text_MenuSet59, 4
    AddListMenuEntry TestKit_Text_MenuSet60, 5
    AddListMenuEntry TestKit_Text_MenuSet61, 6
    AddListMenuEntry TestKit_Text_MenuSet62, 7
    AddListMenuEntry TestKit_Text_MenuSet63, 8
    AddListMenuEntry TestKit_Text_MenuSet64, 9
    AddListMenuEntry TestKit_Text_MenuSet65, 10
    AddListMenuEntry TestKit_Text_MenuSet66, 11
    AddListMenuEntry TestKit_Text_MenuSet67, 12
    ShowListMenu
    GoToIfEq VAR_0x8004, 0, TestKit_MoveSet55
    GoToIfEq VAR_0x8004, 1, TestKit_MoveSet56
    GoToIfEq VAR_0x8004, 2, TestKit_MoveSet57
    GoToIfEq VAR_0x8004, 3, TestKit_MoveSet58
    GoToIfEq VAR_0x8004, 4, TestKit_MoveSet59
    GoToIfEq VAR_0x8004, 5, TestKit_MoveSet60
    GoToIfEq VAR_0x8004, 6, TestKit_MoveSet61
    GoToIfEq VAR_0x8004, 7, TestKit_MoveSet62
    GoToIfEq VAR_0x8004, 8, TestKit_MoveSet63
    GoToIfEq VAR_0x8004, 9, TestKit_MoveSet64
    GoToIfEq VAR_0x8004, 10, TestKit_MoveSet65
    GoToIfEq VAR_0x8004, 11, TestKit_MoveSet66
    GoToIfEq VAR_0x8004, 12, TestKit_MoveSet67
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

/* Set 32: Electro Ball's power from the Speed ratio. Mew is over four times
   as fast as the wild Shuckle, so Electro Ball (150) hits it harder than
   Thunderbolt (90); against the wild Chansey it is one to two times as fast,
   so Electro Ball (60 or 80) hits softer, until Agility doubles Mew's Speed. */
TestKit_MoveSet32:
    SetVar VAR_0x8006, MOVE_ELECTRO_BALL
    SetVar VAR_0x8007, MOVE_THUNDERBOLT
    SetVar VAR_0x8008, MOVE_AGILITY
    SetVar VAR_0x8009, MOVE_RECOVER
    GoTo TestKit_GiveMew

/* Set 33: Stored Power and Power Trip gain 20 power for each stage
   Mew has raised a stat. One Agility triples Stored Power's damage (20 to
   60) without touching Mew's Sp. Atk, and one Iron Defense triples Power
   Trip's the same way. Against the wild Chansey or Shuckle. */
TestKit_MoveSet33:
    SetVar VAR_0x8006, MOVE_STORED_POWER
    SetVar VAR_0x8007, MOVE_POWER_TRIP
    SetVar VAR_0x8008, MOVE_AGILITY
    SetVar VAR_0x8009, MOVE_IRON_DEFENSE
    GoTo TestKit_GiveMew

/* Set 34: Retaliate doubles the turn after a battler on its side
   faints. Two Pokemon, then a wild Chansey that knows only Splash: switch
   the Jirachi in and use Memento, send Mew out, and its first Retaliate
   does about twice what the second does. Needs two free party slots. */
TestKit_MoveSet34:
    GoToIfGe VAR_0x8005, 5, TestKit_PartyFull
    GivePokemon SPECIES_JIRACHI, 50, ITEM_NONE, VAR_RESULT
    ResetPartyMonMoveSlot_Unused VAR_0x8005, 0, MOVE_MEMENTO
    ResetPartyMonMoveSlot_Unused VAR_0x8005, 1, MOVE_HEALING_WISH
    ResetPartyMonMoveSlot_Unused VAR_0x8005, 2, MOVE_SPLASH
    ResetPartyMonMoveSlot_Unused VAR_0x8005, 3, MOVE_RECOVER
    AddVar VAR_0x8005, 1
    SetVar VAR_0x8000, SPECIES_CHANSEY
    SetVar VAR_0x8001, ABILITY_NONE
    SetVar VAR_0x8002, MOVE_SPLASH
    SetVar VAR_0x8006, MOVE_RETALIATE
    SetVar VAR_0x8007, MOVE_SPLASH
    SetVar VAR_0x8008, MOVE_RECOVER
    SetVar VAR_0x8009, MOVE_SWORDS_DANCE
    GoTo TestKit_GiveMew

/* Set 35: Echoed Voice gains 40 power each turn in a row it is
   used, up to 200, and starts again at 40 after a turn without it. Against
   the wild Chansey, the third use in a row (120) passes Hyper Voice (90). */
TestKit_MoveSet35:
    SetVar VAR_0x8006, MOVE_ECHOED_VOICE
    SetVar VAR_0x8007, MOVE_HYPER_VOICE
    SetVar VAR_0x8008, MOVE_SPLASH
    SetVar VAR_0x8009, MOVE_RECOVER
    GoTo TestKit_GiveMew

/* Set 36: Stomping Tantrum and Temper Flare double the turn after
   Mew's move misses or fails. Against a wild Chansey that knows only
   Splash: Snore while awake says "But it failed!", and the Stomping
   Tantrum or Temper Flare after it does about twice what one after
   Recover does. */
TestKit_MoveSet36:
    SetVar VAR_0x8000, SPECIES_CHANSEY
    SetVar VAR_0x8001, ABILITY_NONE
    SetVar VAR_0x8002, MOVE_SPLASH
    SetVar VAR_0x8006, MOVE_STOMPING_TANTRUM
    SetVar VAR_0x8007, MOVE_TEMPER_FLARE
    SetVar VAR_0x8008, MOVE_SNORE
    SetVar VAR_0x8009, MOVE_RECOVER
    GoTo TestKit_GiveMew

/* Set 37: Last Respects gains 50 power for each fainted Pokemon in
   Mew's party. Two Pokemon, then a wild Chansey that knows only Splash:
   switch Mew in and use Last Respects, switch the Jirachi in and use
   Memento, send Mew out again, and Last Respects now does about twice what
   it did (100, from 50). Start with no fainted Pokemon in the party. */
TestKit_MoveSet37:
    GoToIfGe VAR_0x8005, 5, TestKit_PartyFull
    GivePokemon SPECIES_JIRACHI, 50, ITEM_NONE, VAR_RESULT
    ResetPartyMonMoveSlot_Unused VAR_0x8005, 0, MOVE_MEMENTO
    ResetPartyMonMoveSlot_Unused VAR_0x8005, 1, MOVE_HEALING_WISH
    ResetPartyMonMoveSlot_Unused VAR_0x8005, 2, MOVE_SPLASH
    ResetPartyMonMoveSlot_Unused VAR_0x8005, 3, MOVE_RECOVER
    AddVar VAR_0x8005, 1
    SetVar VAR_0x8000, SPECIES_CHANSEY
    SetVar VAR_0x8001, ABILITY_NONE
    SetVar VAR_0x8002, MOVE_SPLASH
    SetVar VAR_0x8006, MOVE_LAST_RESPECTS
    SetVar VAR_0x8007, MOVE_SPLASH
    SetVar VAR_0x8008, MOVE_RECOVER
    SetVar VAR_0x8009, MOVE_SWORDS_DANCE
    GoTo TestKit_GiveMew

/* Set 38: Hard Press is stronger the more HP the target has left:
   100 at full HP, falling with the target's share. Against the wild
   Chansey, the first Hard Press does a little more than Body Slam (85);
   once Chansey is below about 85% of its HP, it does less. */
TestKit_MoveSet38:
    SetVar VAR_0x8006, MOVE_HARD_PRESS
    SetVar VAR_0x8007, MOVE_BODY_SLAM
    SetVar VAR_0x8008, MOVE_RECOVER
    SetVar VAR_0x8009, MOVE_SPLASH
    GoTo TestKit_GiveMew

/* Set 39: Pika Papow and Veevee Volley now carry power 1, as Return
   does, so the type chart reads them as attacks: against the wild Skarmory
   Pika Papow is "super effective", and against the wild Shuckle Veevee
   Volley is "not very effective". */
TestKit_MoveSet39:
    SetVar VAR_0x8006, MOVE_PIKA_PAPOW
    SetVar VAR_0x8007, MOVE_VEEVEE_VOLLEY
    SetVar VAR_0x8008, MOVE_RECOVER
    SetVar VAR_0x8009, MOVE_SPLASH
    GoTo TestKit_GiveMew

/* Set 40: Lash Out doubles when one of Mew's stats fell earlier in
   the turn. Against a wild Klefki with Prankster that knows only Tail
   Whip, which therefore always goes first: while Tail Whip lowers Mew's
   Defense, Lash Out (150) does about twice what Crunch (80) does; once
   Mew's Defense is at its lowest and Tail Whip fails, less. */
TestKit_MoveSet40:
    SetVar VAR_0x8000, SPECIES_KLEFKI
    SetVar VAR_0x8001, ABILITY_PRANKSTER
    SetVar VAR_0x8002, MOVE_TAIL_WHIP
    SetVar VAR_0x8006, MOVE_LASH_OUT
    SetVar VAR_0x8007, MOVE_CRUNCH
    SetVar VAR_0x8008, MOVE_RECOVER
    SetVar VAR_0x8009, MOVE_SPLASH
    GoTo TestKit_GiveMew

/* Set 41: Grav Apple is half as strong again under Gravity. Against
   a wild Chansey given Clear Body, so Grav Apple cannot lower its Defense,
   that knows only Splash: Grav Apple (90) does a little more than Seed Bomb
   (80), and after Gravity (135) about two thirds more. */
TestKit_MoveSet41:
    SetVar VAR_0x8000, SPECIES_CHANSEY
    SetVar VAR_0x8001, ABILITY_CLEAR_BODY
    SetVar VAR_0x8002, MOVE_SPLASH
    SetVar VAR_0x8006, MOVE_GRAV_APPLE
    SetVar VAR_0x8007, MOVE_SEED_BOMB
    SetVar VAR_0x8008, MOVE_GRAVITY
    SetVar VAR_0x8009, MOVE_RECOVER
    GoTo TestKit_GiveMew

/* Set 42: Foul Play hits with the target's Attack and its stages. Against
   a wild Shuckle, whose Attack is tiny, that knows only Swords Dance: Foul
   Play does well under half what Crunch does, Mew's own Swords Dance raises
   Crunch and not Foul Play, and each of Shuckle's Swords Dances raises Foul
   Play. */
TestKit_MoveSet42:
    SetVar VAR_0x8000, SPECIES_SHUCKLE
    SetVar VAR_0x8001, ABILITY_NONE
    SetVar VAR_0x8002, MOVE_SWORDS_DANCE
    SetVar VAR_0x8006, MOVE_FOUL_PLAY
    SetVar VAR_0x8007, MOVE_CRUNCH
    SetVar VAR_0x8008, MOVE_SWORDS_DANCE
    SetVar VAR_0x8009, MOVE_RECOVER
    GoTo TestKit_GiveMew

/* Set 43: Body Press hits with the user's Defense and its stages. Against
   a wild Shuckle that knows only Splash: Body Press and Brick Break start
   close, Iron Defense doubles Body Press and leaves Brick Break alone, and
   Swords Dance does the opposite. */
TestKit_MoveSet43:
    SetVar VAR_0x8000, SPECIES_SHUCKLE
    SetVar VAR_0x8001, ABILITY_NONE
    SetVar VAR_0x8002, MOVE_SPLASH
    SetVar VAR_0x8006, MOVE_BODY_PRESS
    SetVar VAR_0x8007, MOVE_BRICK_BREAK
    SetVar VAR_0x8008, MOVE_IRON_DEFENSE
    SetVar VAR_0x8009, MOVE_SWORDS_DANCE
    GoTo TestKit_GiveMew

/* Set 44: Psyshock is a special move that hits the target's Defense.
   Against a wild Chansey, whose Defense is tiny and Sp. Def high, that
   knows only Calm Mind: Psyshock takes most of Chansey's HP where Psychic
   takes a small share, and Chansey's Calm Minds weaken Psychic and leave
   Psyshock as it was. */
TestKit_MoveSet44:
    SetVar VAR_0x8000, SPECIES_CHANSEY
    SetVar VAR_0x8001, ABILITY_NONE
    SetVar VAR_0x8002, MOVE_CALM_MIND
    SetVar VAR_0x8006, MOVE_PSYSHOCK
    SetVar VAR_0x8007, MOVE_PSYCHIC
    SetVar VAR_0x8008, MOVE_RECOVER
    SetVar VAR_0x8009, MOVE_SPLASH
    GoTo TestKit_GiveMew

/* Set 45: Sacred Sword and Darkest Lariat ignore the target's stat stages,
   Defense and evasion alike. Against a wild Skarmory that knows only Iron
   Defense and Double Team: once it has used them, Brick Break and Crunch do
   less and sometimes miss, and Sacred Sword and Darkest Lariat do what they
   did at first and never miss. */
TestKit_MoveSet45:
    SetVar VAR_0x8000, SPECIES_SKARMORY
    SetVar VAR_0x8001, ABILITY_NONE
    SetVar VAR_0x8002, MOVE_IRON_DEFENSE
    SetVar VAR_0x8003, MOVE_DOUBLE_TEAM
    SetVar VAR_0x8006, MOVE_SACRED_SWORD
    SetVar VAR_0x8007, MOVE_BRICK_BREAK
    SetVar VAR_0x8008, MOVE_DARKEST_LARIAT
    SetVar VAR_0x8009, MOVE_CRUNCH
    GoTo TestKit_GiveMew

/* Set 46: Freeze-Dry is super effective on Water, and Flying Press is
   Fighting and Flying at once. Against a wild Poliwrath (Water and
   Fighting) that knows only Splash: Freeze-Dry is "super effective" and Ice
   Beam "not very effective"; Flying Press is "super effective", from its
   Flying half, and Close Combat is neither. */
TestKit_MoveSet46:
    SetVar VAR_0x8000, SPECIES_POLIWRATH
    SetVar VAR_0x8001, ABILITY_NONE
    SetVar VAR_0x8002, MOVE_SPLASH
    SetVar VAR_0x8006, MOVE_FREEZE_DRY
    SetVar VAR_0x8007, MOVE_ICE_BEAM
    SetVar VAR_0x8008, MOVE_FLYING_PRESS
    SetVar VAR_0x8009, MOVE_CLOSE_COMBAT
    GoTo TestKit_GiveMew

/* Set 47: Flying Press against a wild Probopass (Rock and Steel) that
   knows only Splash: its Fighting half doubles twice and its Flying half
   halves twice, so it says nothing about effectiveness, where Close Combat
   is "super effective". */
TestKit_MoveSet47:
    SetVar VAR_0x8000, SPECIES_PROBOPASS
    SetVar VAR_0x8001, ABILITY_NONE
    SetVar VAR_0x8002, MOVE_SPLASH
    SetVar VAR_0x8006, MOVE_FLYING_PRESS
    SetVar VAR_0x8007, MOVE_CLOSE_COMBAT
    SetVar VAR_0x8008, MOVE_RECOVER
    SetVar VAR_0x8009, MOVE_SPLASH
    GoTo TestKit_GiveMew

/* Set 48: Rage Fist gains 50 power for each hit Mew takes from an attack
   this battle, to 350. Against a wild Registeel that knows only Double
   Kick, which hits twice: Rage Fist used turn after turn does 50, 150, 250
   and then 350, hits on Mew's Substitute add nothing, and switching Mew out
   and back in keeps the count. */
TestKit_MoveSet48:
    SetVar VAR_0x8000, SPECIES_REGISTEEL
    SetVar VAR_0x8001, ABILITY_NONE
    SetVar VAR_0x8002, MOVE_DOUBLE_KICK
    SetVar VAR_0x8006, MOVE_RAGE_FIST
    SetVar VAR_0x8007, MOVE_SUBSTITUTE
    SetVar VAR_0x8008, MOVE_RECOVER
    SetVar VAR_0x8009, MOVE_SPLASH
    GoTo TestKit_GiveMew

/* Set 49: Transform copies the whole ability, including one numbered 256
   or more. Against a wild Rattata given Toxic Debris (295) that knows only
   Tackle: once Mew has transformed, each Tackle it takes scatters poison
   spikes on the foe's side, where before the fix Mew got Inner Focus (39,
   the low byte) and nothing happened. */
TestKit_MoveSet49:
    SetVar VAR_0x8000, SPECIES_RATTATA
    SetVar VAR_0x8001, ABILITY_TOXIC_DEBRIS
    SetVar VAR_0x8002, MOVE_TACKLE
    SetVar VAR_0x8006, MOVE_TRANSFORM
    SetVar VAR_0x8007, MOVE_RECOVER
    SetVar VAR_0x8008, MOVE_SPLASH
    SetVar VAR_0x8009, MOVE_TACKLE
    GoTo TestKit_GiveMew

/* Set 50: Wonder Room trades every battler's Defense and Sp. Def for five
   turns. Against a wild Cloyster, whose Defense is high and Sp. Def low,
   that knows only Recover, so it outlasts the five turns: Swift does
   several times what Tackle does until Wonder Room goes up, then Tackle
   does several times what Swift does, and they trade back when it wears
   off five turns later, or at once if Mew uses Wonder Room again. */
TestKit_MoveSet50:
    SetVar VAR_0x8000, SPECIES_CLOYSTER
    SetVar VAR_0x8001, ABILITY_NONE
    SetVar VAR_0x8002, MOVE_RECOVER
    SetVar VAR_0x8006, MOVE_WONDER_ROOM
    SetVar VAR_0x8007, MOVE_TACKLE
    SetVar VAR_0x8008, MOVE_SWIFT
    SetVar VAR_0x8009, MOVE_SPLASH
    GoTo TestKit_GiveMew

/* Set 51: Shore Up heals half Mew's maximum HP, or two thirds in a
   sandstorm, and no other weather changes it. Against a wild Chansey that
   knows only Seismic Toss, which takes a fixed 50 HP a turn: set a weather,
   use it again (it fails) to lose another 50, then Shore Up. In sun or rain
   it heals half, where it used to heal two thirds in sun as Synthesis does;
   in a sandstorm it heals two thirds. */
TestKit_MoveSet51:
    SetVar VAR_0x8000, SPECIES_CHANSEY
    SetVar VAR_0x8001, ABILITY_NONE
    SetVar VAR_0x8002, MOVE_SEISMIC_TOSS
    SetVar VAR_0x8006, MOVE_SHORE_UP
    SetVar VAR_0x8007, MOVE_SANDSTORM
    SetVar VAR_0x8008, MOVE_SUNNY_DAY
    SetVar VAR_0x8009, MOVE_RAIN_DANCE
    GoTo TestKit_GiveMew

/* Set 52: Meteor Beam charges for a turn, raising Sp. Atk one stage, and
   attacks on the next. Against a wild Chansey that knows only Splash: the
   first turn prints "is overflowing with space power!" and "Sp. Atk rose!",
   the second hits. The set also puts a Power Herb in the bag; held, it
   raises Sp. Atk and attacks in the same turn, and is used up. */
TestKit_MoveSet52:
    AddItem ITEM_POWER_HERB, 1, VAR_RESULT
    SetVar VAR_0x8000, SPECIES_CHANSEY
    SetVar VAR_0x8001, ABILITY_NONE
    SetVar VAR_0x8002, MOVE_SPLASH
    SetVar VAR_0x8006, MOVE_METEOR_BEAM
    SetVar VAR_0x8007, MOVE_POWER_GEM
    SetVar VAR_0x8008, MOVE_RECOVER
    SetVar VAR_0x8009, MOVE_SPLASH
    GoTo TestKit_GiveMew

/* Set 53: Electro Shot charges for a turn, raising Sp. Atk one stage, and
   attacks on the next, but in rain it raises Sp. Atk and attacks in the
   same turn. Against a wild Chansey that knows only Splash: out of rain the
   first turn prints "absorbed electricity!" and "Sp. Atk rose!" and the
   second hits; after Rain Dance both happen in one turn. */
TestKit_MoveSet53:
    SetVar VAR_0x8000, SPECIES_CHANSEY
    SetVar VAR_0x8001, ABILITY_NONE
    SetVar VAR_0x8002, MOVE_SPLASH
    SetVar VAR_0x8006, MOVE_ELECTRO_SHOT
    SetVar VAR_0x8007, MOVE_RAIN_DANCE
    SetVar VAR_0x8008, MOVE_THUNDERBOLT
    SetVar VAR_0x8009, MOVE_RECOVER
    GoTo TestKit_GiveMew

/* Set 54: Mind Blown costs its user half its maximum HP once the move is
   over, hit or miss. Against a wild Chansey that knows Protect and Splash:
   each Mind Blown takes half Mew's HP ("MEW is hit with recoil!"), even when
   Chansey protects itself, and Flamethrower costs nothing. */
TestKit_MoveSet54:
    SetVar VAR_0x8000, SPECIES_CHANSEY
    SetVar VAR_0x8001, ABILITY_NONE
    SetVar VAR_0x8002, MOVE_PROTECT
    SetVar VAR_0x8003, MOVE_SPLASH
    SetVar VAR_0x8006, MOVE_MIND_BLOWN
    SetVar VAR_0x8007, MOVE_FLAMETHROWER
    SetVar VAR_0x8008, MOVE_RECOVER
    SetVar VAR_0x8009, MOVE_SPLASH
    GoTo TestKit_GiveMew

/* Set 55: Damp stops Mind Blown before it starts, and then it costs nothing.
   Against a wild Politoed given Damp that knows only Splash. */
TestKit_MoveSet55:
    SetVar VAR_0x8000, SPECIES_POLITOED
    SetVar VAR_0x8001, ABILITY_DAMP
    SetVar VAR_0x8002, MOVE_SPLASH
    SetVar VAR_0x8006, MOVE_MIND_BLOWN
    SetVar VAR_0x8007, MOVE_FLAMETHROWER
    SetVar VAR_0x8008, MOVE_RECOVER
    SetVar VAR_0x8009, MOVE_SPLASH
    GoTo TestKit_GiveMew

/* Set 56: Nature's Madness carries power 1, the mark of a move whose damage
   is worked out, so Taunt no longer takes it for a status move. Against a
   wild Chansey that knows only Taunt: once Mew is taunted, Splash cannot be
   chosen, and Nature's Madness still can and halves Chansey's HP. */
TestKit_MoveSet56:
    SetVar VAR_0x8000, SPECIES_CHANSEY
    SetVar VAR_0x8001, ABILITY_NONE
    SetVar VAR_0x8002, MOVE_TAUNT
    SetVar VAR_0x8006, MOVE_NATURES_MADNESS
    SetVar VAR_0x8007, MOVE_SPLASH
    SetVar VAR_0x8008, MOVE_RECOVER
    SetVar VAR_0x8009, MOVE_TACKLE
    GoTo TestKit_GiveMew

/* Set 57: once Scale Shot's last hit is in, its user's Defense falls and its
   Speed rises, one stage each. Against a wild Shuckle that knows only
   Splash, which Scale Shot cannot knock out: after "Hit N time(s)!", "MEW's
   Defense fell!" and "MEW's Speed rose!", once however many hits landed. */
TestKit_MoveSet57:
    SetVar VAR_0x8000, SPECIES_SHUCKLE
    SetVar VAR_0x8001, ABILITY_NONE
    SetVar VAR_0x8002, MOVE_SPLASH
    SetVar VAR_0x8006, MOVE_SCALE_SHOT
    SetVar VAR_0x8007, MOVE_DOUBLE_HIT
    SetVar VAR_0x8008, MOVE_RECOVER
    SetVar VAR_0x8009, MOVE_SPLASH
    GoTo TestKit_GiveMew

/* Set 58: Spiky Shield protects its user and hurts an attacker that makes
   contact with it by an eighth of its maximum HP. Against a wild Rattata
   that knows Tackle and Swift: a Tackle into the shield brings "The wild
   RATTATA was hurt!", a Swift only "MEW protected itself!". */
TestKit_MoveSet58:
    SetVar VAR_0x8000, SPECIES_RATTATA
    SetVar VAR_0x8001, ABILITY_NONE
    SetVar VAR_0x8002, MOVE_TACKLE
    SetVar VAR_0x8003, MOVE_SWIFT
    SetVar VAR_0x8006, MOVE_SPIKY_SHIELD
    SetVar VAR_0x8007, MOVE_RECOVER
    SetVar VAR_0x8008, MOVE_SPLASH
    SetVar VAR_0x8009, MOVE_TACKLE
    GoTo TestKit_GiveMew

/* Set 59: Baneful Bunker protects its user and poisons an attacker that
   makes contact with it. Against a wild Rattata that knows Tackle and
   Swift: the first Tackle into the bunker brings "The wild RATTATA was
   poisoned!", a Swift only "MEW protected itself!". */
TestKit_MoveSet59:
    SetVar VAR_0x8000, SPECIES_RATTATA
    SetVar VAR_0x8001, ABILITY_NONE
    SetVar VAR_0x8002, MOVE_TACKLE
    SetVar VAR_0x8003, MOVE_SWIFT
    SetVar VAR_0x8006, MOVE_BANEFUL_BUNKER
    SetVar VAR_0x8007, MOVE_RECOVER
    SetVar VAR_0x8008, MOVE_SPLASH
    SetVar VAR_0x8009, MOVE_TACKLE
    GoTo TestKit_GiveMew

/* Set 60: Salt Cure salts its target, which then loses an eighth of its HP
   at the end of every turn, a quarter as a Water or Steel type. Against a
   wild Chansey that knows only Splash: "The wild CHANSEY is being salt
   cured!", then "The wild CHANSEY is hurt by Salt Cure!" each turn; after
   Soak makes it a Water type, each loss doubles. */
TestKit_MoveSet60:
    SetVar VAR_0x8000, SPECIES_CHANSEY
    SetVar VAR_0x8001, ABILITY_NONE
    SetVar VAR_0x8002, MOVE_SPLASH
    SetVar VAR_0x8006, MOVE_SALT_CURE
    SetVar VAR_0x8007, MOVE_SOAK
    SetVar VAR_0x8008, MOVE_RECOVER
    SetVar VAR_0x8009, MOVE_SPLASH
    GoTo TestKit_GiveMew

/* Set 61: Octolock traps its target and lowers its Defense and Sp. Def by a
   stage each at the end of every turn. Against a wild Chansey that knows
   only Splash: "The wild CHANSEY can no longer escape because of
   Octolock!", then each turn "The wild CHANSEY's Defense fell!" and "The
   wild CHANSEY's Sp. Def fell!", so Tackle and Swift hit harder turn by
   turn; a second Octolock fails. */
TestKit_MoveSet61:
    SetVar VAR_0x8000, SPECIES_CHANSEY
    SetVar VAR_0x8001, ABILITY_NONE
    SetVar VAR_0x8002, MOVE_SPLASH
    SetVar VAR_0x8006, MOVE_OCTOLOCK
    SetVar VAR_0x8007, MOVE_TACKLE
    SetVar VAR_0x8008, MOVE_SWIFT
    SetVar VAR_0x8009, MOVE_RECOVER
    GoTo TestKit_GiveMew

/* Set 62: for five turns under Magic Room no held item works. Mew holds
   Leftovers; against a wild Chansey that knows only Splash. After a
   Substitute, "MEW restored a little HP using its Leftovers!" at the end of
   each turn; once "It created a bizarre area in which Pokemon's held items
   lose their effects!", no more until "Magic Room wore off, and held items'
   effects returned to normal!" five turns later, or at once if Mew uses
   Magic Room again. */
TestKit_MoveSet62:
    SetVar VAR_0x8000, SPECIES_CHANSEY
    SetVar VAR_0x8001, ABILITY_NONE
    SetVar VAR_0x8002, MOVE_SPLASH
    SetVar VAR_0x800A, SPECIES_MEW
    SetVar VAR_0x800B, ABILITY_NONE
    SetVar VAR_0x8004, ITEM_LEFTOVERS
    SetVar VAR_0x8006, MOVE_MAGIC_ROOM
    SetVar VAR_0x8007, MOVE_SUBSTITUTE
    SetVar VAR_0x8008, MOVE_SPLASH
    SetVar VAR_0x8009, MOVE_TACKLE
    GoTo TestKit_GivePokemonWithItem

/* Set 63: Teatime makes every battler on the field eat its held Berry at
   once, whether or not it would trigger. Mew holds a Liechi Berry; against
   a wild Chansey that knows only Splash. At full HP, Teatime brings "It's
   teatime! Everyone dug in to their Berries!" and then Mew's Liechi Berry
   raising its Attack; a second Teatime fails, since no Berry is left. */
TestKit_MoveSet63:
    SetVar VAR_0x8000, SPECIES_CHANSEY
    SetVar VAR_0x8001, ABILITY_NONE
    SetVar VAR_0x8002, MOVE_SPLASH
    SetVar VAR_0x800A, SPECIES_MEW
    SetVar VAR_0x800B, ABILITY_NONE
    SetVar VAR_0x8004, ITEM_LIECHI_BERRY
    SetVar VAR_0x8006, MOVE_TEATIME
    SetVar VAR_0x8007, MOVE_SPLASH
    SetVar VAR_0x8008, MOVE_RECOVER
    SetVar VAR_0x8009, MOVE_TACKLE
    GoTo TestKit_GivePokemonWithItem

/* Set 64: Core Enforcer suppresses the ability of a target that has already
   moved this turn. Against a wild Jolteon given Volt Absorb, which is faster
   than Mew and knows only Splash: Thunderbolt does nothing to it, since
   Volt Absorb takes it; after a Core Enforcer, "The wild JOLTEON's ability
   was suppressed!", and Thunderbolt hurts it from then on. */
TestKit_MoveSet64:
    SetVar VAR_0x8000, SPECIES_JOLTEON
    SetVar VAR_0x8001, ABILITY_VOLT_ABSORB
    SetVar VAR_0x8002, MOVE_SPLASH
    SetVar VAR_0x8006, MOVE_CORE_ENFORCER
    SetVar VAR_0x8007, MOVE_THUNDERBOLT
    SetVar VAR_0x8008, MOVE_RECOVER
    SetVar VAR_0x8009, MOVE_SPLASH
    GoTo TestKit_GiveMew

/* Set 65: Beak Blast heats its user's beak at the start of the turn and
   burns an attacker that makes contact with it before it strikes. Against
   a wild Rattata that knows Tackle and Swift: when Mew chooses Beak Blast,
   "MEW started heating up its beak!" comes first, and a Tackle into it
   brings "The wild RATTATA was burned!" before Beak Blast hits; a Swift
   makes no contact and burns nothing, nor does a Tackle on a turn Mew
   chooses something else. */
TestKit_MoveSet65:
    SetVar VAR_0x8000, SPECIES_RATTATA
    SetVar VAR_0x8001, ABILITY_NONE
    SetVar VAR_0x8002, MOVE_TACKLE
    SetVar VAR_0x8003, MOVE_SWIFT
    SetVar VAR_0x8006, MOVE_BEAK_BLAST
    SetVar VAR_0x8007, MOVE_RECOVER
    SetVar VAR_0x8008, MOVE_SPLASH
    SetVar VAR_0x8009, MOVE_TACKLE
    GoTo TestKit_GiveMew

/* Set 66: Sky Drop lifts its target on the first turn, and the target can
   do nothing until it is dropped on the second. Against a wild Chansey that
   knows only Tackle, slower than Mew: "MEW took the wild CHANSEY into the
   sky!", then no Tackle that turn; next turn the drop hits before Chansey
   moves, and both are back on the ground, so Chansey tackles later that
   same turn. */
TestKit_MoveSet66:
    SetVar VAR_0x8000, SPECIES_CHANSEY
    SetVar VAR_0x8001, ABILITY_NONE
    SetVar VAR_0x8002, MOVE_TACKLE
    SetVar VAR_0x8006, MOVE_SKY_DROP
    SetVar VAR_0x8007, MOVE_RECOVER
    SetVar VAR_0x8008, MOVE_SPLASH
    SetVar VAR_0x8009, MOVE_PROTECT
    GoTo TestKit_GiveMew

/* Set 67: Sky Drop can lift a Flying type but the drop does not affect it.
   Against a wild Skarmory that knows only Splash: "MEW took the wild
   SKARMORY into the sky!", then on the second turn "It doesn't affect the
   wild SKARMORY..." once both have landed. */
TestKit_MoveSet67:
    SetVar VAR_0x8000, SPECIES_SKARMORY
    SetVar VAR_0x8001, ABILITY_NONE
    SetVar VAR_0x8002, MOVE_SPLASH
    SetVar VAR_0x8006, MOVE_SKY_DROP
    SetVar VAR_0x8007, MOVE_RECOVER
    SetVar VAR_0x8008, MOVE_SPLASH
    SetVar VAR_0x8009, MOVE_PROTECT
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
    AddListMenuEntry TestKit_Text_MenuAbilityMore, 20
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
    GoToIfEq VAR_0x8004, 20, TestKit_Abilities3
    GoTo TestKit_Close

/* The third page: the hidden abilities the natives carry, which element 5
   left for a follow-up. */
TestKit_Abilities3:
    Message TestKit_Text_WhichAbility
    InitLocalTextListMenu 1, 1, 0, VAR_0x8004
    AddListMenuEntry TestKit_Text_MenuAbilityAnalytic, 0
    AddListMenuEntry TestKit_Text_MenuAbilityFlareBoost, 1
    AddListMenuEntry TestKit_Text_MenuAbilityHeavyMetal, 2
    AddListMenuEntry TestKit_Text_MenuAbilityJustified, 3
    AddListMenuEntry TestKit_Text_MenuAbilityLightMetal, 4
    AddListMenuEntry TestKit_Text_MenuAbilityMagicBounce, 5
    AddListMenuEntry TestKit_Text_MenuAbilityMoody, 6
    AddListMenuEntry TestKit_Text_MenuAbilityMoxie, 7
    AddListMenuEntry TestKit_Text_MenuAbilityMultiscale, 8
    AddListMenuEntry TestKit_Text_MenuAbilityPickpocket, 9
    AddListMenuEntry TestKit_Text_MenuAbilityPoisonTouch, 10
    AddListMenuEntry TestKit_Text_MenuAbilityRattled, 11
    AddListMenuEntry TestKit_Text_MenuAbilitySandForce, 12
    AddListMenuEntry TestKit_Text_MenuAbilitySandRush, 13
    AddListMenuEntry TestKit_Text_MenuAbilityToxicBoost, 14
    AddListMenuEntry TestKit_Text_MenuAbilityWonderSkin, 15
    ShowListMenu
    GoToIfEq VAR_0x8004, 0, TestKit_AbilityAnalytic
    GoToIfEq VAR_0x8004, 1, TestKit_AbilityFlareBoost
    GoToIfEq VAR_0x8004, 2, TestKit_AbilityHeavyMetal
    GoToIfEq VAR_0x8004, 3, TestKit_AbilityJustified
    GoToIfEq VAR_0x8004, 4, TestKit_AbilityLightMetal
    GoToIfEq VAR_0x8004, 5, TestKit_AbilityMagicBounce
    GoToIfEq VAR_0x8004, 6, TestKit_AbilityMoody
    GoToIfEq VAR_0x8004, 7, TestKit_AbilityMoxie
    GoToIfEq VAR_0x8004, 8, TestKit_AbilityMultiscale
    GoToIfEq VAR_0x8004, 9, TestKit_AbilityPickpocket
    GoToIfEq VAR_0x8004, 10, TestKit_AbilityPoisonTouch
    GoToIfEq VAR_0x8004, 11, TestKit_AbilityRattled
    GoToIfEq VAR_0x8004, 12, TestKit_AbilitySandForce
    GoToIfEq VAR_0x8004, 13, TestKit_AbilitySandRush
    GoToIfEq VAR_0x8004, 14, TestKit_AbilityToxicBoost
    GoToIfEq VAR_0x8004, 15, TestKit_AbilityWonderSkin
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

/* Analytic: the player's Snorlax (its own ability) and a
   wild Magnezone given Analytic that knows only Thunderbolt. Magnezone is
   always faster, so its Thunderbolt hits a third harder on the turns Snorlax
   uses Quick Attack, and moves first, than on the turns it uses Splash. */
TestKit_AbilityAnalytic:
    SetVar VAR_0x800A, SPECIES_SNORLAX
    SetVar VAR_0x800B, ABILITY_NONE
    SetVar VAR_0x8006, MOVE_QUICK_ATTACK
    SetVar VAR_0x8007, MOVE_SPLASH
    SetVar VAR_0x8008, MOVE_REST
    SetVar VAR_0x8009, MOVE_PROTECT
    SetVar VAR_0x8000, SPECIES_MAGNEZONE
    SetVar VAR_0x8001, ABILITY_ANALYTIC
    SetVar VAR_0x8002, MOVE_THUNDERBOLT
    GoTo TestKit_GivePokemonWithMoves

/* Flare Boost: the player's Snorlax (its own ability) and a
   wild Drifblim given Flare Boost that knows only Swift. Once Will-O-Wisp
   has burned Drifblim, its Swift takes about half again as much of Snorlax's
   HP as before. */
TestKit_AbilityFlareBoost:
    SetVar VAR_0x800A, SPECIES_SNORLAX
    SetVar VAR_0x800B, ABILITY_NONE
    SetVar VAR_0x8006, MOVE_WILL_O_WISP
    SetVar VAR_0x8007, MOVE_SPLASH
    SetVar VAR_0x8008, MOVE_REST
    SetVar VAR_0x8009, MOVE_PROTECT
    SetVar VAR_0x8000, SPECIES_DRIFBLIM
    SetVar VAR_0x8001, ABILITY_FLARE_BOOST
    SetVar VAR_0x8002, MOVE_SWIFT
    GoTo TestKit_GivePokemonWithMoves

/* Heavy Metal: the player's Machamp (its own ability) and a
   wild Aggron given Heavy Metal that knows Heavy Slam and Iron Head.
   Doubled to 720 kg, Aggron is over five times Machamp's 130 kg, so Heavy
   Slam hits at 120 and does about half again what Iron Head (80) does;
   without Heavy Metal it would hit at 60, below Iron Head. */
TestKit_AbilityHeavyMetal:
    SetVar VAR_0x800A, SPECIES_MACHAMP
    SetVar VAR_0x800B, ABILITY_NONE
    SetVar VAR_0x8006, MOVE_KARATE_CHOP
    SetVar VAR_0x8007, MOVE_SPLASH
    SetVar VAR_0x8008, MOVE_REST
    SetVar VAR_0x8009, MOVE_PROTECT
    SetVar VAR_0x8000, SPECIES_AGGRON
    SetVar VAR_0x8001, ABILITY_HEAVY_METAL
    SetVar VAR_0x8002, MOVE_HEAVY_SLAM
    SetVar VAR_0x8003, MOVE_IRON_HEAD
    GoTo TestKit_GivePokemonWithMoves

/* Justified: a wild Poochyena that knows only Bite. Each Bite
   that hits raises Lucario's Attack a stage, with a message; at +6 nothing
   more is said. */
TestKit_AbilityJustified:
    SetVar VAR_0x800A, SPECIES_LUCARIO
    SetVar VAR_0x800B, ABILITY_JUSTIFIED
    SetVar VAR_0x8006, MOVE_AURA_SPHERE
    SetVar VAR_0x8007, MOVE_SPLASH
    SetVar VAR_0x8008, MOVE_CALM_MIND
    SetVar VAR_0x8009, MOVE_FLASH_CANNON
    SetVar VAR_0x8000, SPECIES_POOCHYENA
    SetVar VAR_0x8001, ABILITY_NONE
    SetVar VAR_0x8002, MOVE_BITE
    GoTo TestKit_GivePokemonWithMoves

/* Light Metal: the player's Garchomp (its own ability) and a
   wild Metagross given Light Metal that knows Heavy Slam and Iron Head.
   Halved to 275 kg, Metagross is under three times Garchomp's 95 kg, so
   Heavy Slam hits at 60 and does less than Iron Head (80); without Light
   Metal it would hit at 120. */
TestKit_AbilityLightMetal:
    SetVar VAR_0x800A, SPECIES_GARCHOMP
    SetVar VAR_0x800B, ABILITY_NONE
    SetVar VAR_0x8006, MOVE_DRAGON_CLAW
    SetVar VAR_0x8007, MOVE_SPLASH
    SetVar VAR_0x8008, MOVE_REST
    SetVar VAR_0x8009, MOVE_PROTECT
    SetVar VAR_0x8000, SPECIES_METAGROSS
    SetVar VAR_0x8001, ABILITY_LIGHT_METAL
    SetVar VAR_0x8002, MOVE_HEAVY_SLAM
    SetVar VAR_0x8003, MOVE_IRON_HEAD
    GoTo TestKit_GivePokemonWithMoves

/* Magic Bounce: a wild Chansey that knows only Toxic. Once Espeon
   is in, each Toxic is turned back with a message, and Chansey is badly
   poisoned in Espeon's place. */
TestKit_AbilityMagicBounce:
    SetVar VAR_0x800A, SPECIES_ESPEON
    SetVar VAR_0x800B, ABILITY_MAGIC_BOUNCE
    SetVar VAR_0x8006, MOVE_PSYCHIC
    SetVar VAR_0x8007, MOVE_CALM_MIND
    SetVar VAR_0x8008, MOVE_MORNING_SUN
    SetVar VAR_0x8009, MOVE_PROTECT
    SetVar VAR_0x8000, SPECIES_CHANSEY
    SetVar VAR_0x8001, ABILITY_NONE
    SetVar VAR_0x8002, MOVE_TOXIC
    GoTo TestKit_GivePokemonWithMoves

/* Moody: a wild Chansey that knows only Splash. At the
   end of each turn with Bibarel in, one of its stats sharply rises and a
   different one falls, each with a message; accuracy and evasion never
   move. */
TestKit_AbilityMoody:
    SetVar VAR_0x800A, SPECIES_BIBAREL
    SetVar VAR_0x800B, ABILITY_MOODY
    SetVar VAR_0x8006, MOVE_SPLASH
    SetVar VAR_0x8007, MOVE_PROTECT
    SetVar VAR_0x8008, MOVE_REST
    SetVar VAR_0x8009, MOVE_WATERFALL
    SetVar VAR_0x8000, SPECIES_CHANSEY
    SetVar VAR_0x8001, ABILITY_NONE
    SetVar VAR_0x8002, MOVE_SPLASH
    GoTo TestKit_GivePokemonWithMoves

/* Moxie: knock out any wild Pokemon; straight after the
   faint message Honchkrow's Attack rises a stage, with a message. */
TestKit_AbilityMoxie:
    SetVar VAR_0x800A, SPECIES_HONCHKROW
    SetVar VAR_0x800B, ABILITY_MOXIE
    SetVar VAR_0x8006, MOVE_NIGHT_SLASH
    SetVar VAR_0x8007, MOVE_BRAVE_BIRD
    SetVar VAR_0x8008, MOVE_SUCKER_PUNCH
    SetVar VAR_0x8009, MOVE_ROOST
    GoTo TestKit_GivePokemonWithMoves

/* Multiscale: a wild Graveler that knows only Rock Throw.
   The first Rock Throw, at full HP, takes about half what the next one
   does; Roost back to full HP and the next is halved again. */
TestKit_AbilityMultiscale:
    SetVar VAR_0x800A, SPECIES_DRAGONITE
    SetVar VAR_0x800B, ABILITY_MULTISCALE
    SetVar VAR_0x8006, MOVE_ROOST
    SetVar VAR_0x8007, MOVE_DRAGON_DANCE
    SetVar VAR_0x8008, MOVE_EXTREME_SPEED
    SetVar VAR_0x8009, MOVE_PROTECT
    SetVar VAR_0x8000, SPECIES_GRAVELER
    SetVar VAR_0x8001, ABILITY_NONE
    SetVar VAR_0x8002, MOVE_ROCK_THROW
    GoTo TestKit_GivePokemonWithMoves

/* Pickpocket: the player's Snorlax (its own ability) holding
   Leftovers, and a wild Sneasel given Pickpocket that knows only Splash.
   Snorlax's first Tackle brings "The wild SNEASEL stole SNORLAX's
   Leftovers!"; Snorlax has them back after the battle. */
TestKit_AbilityPickpocket:
    SetVar VAR_0x800A, SPECIES_SNORLAX
    SetVar VAR_0x800B, ABILITY_NONE
    SetVar VAR_0x8006, MOVE_TACKLE
    SetVar VAR_0x8007, MOVE_SPLASH
    SetVar VAR_0x8008, MOVE_REST
    SetVar VAR_0x8009, MOVE_PROTECT
    SetVar VAR_0x8000, SPECIES_SNEASEL
    SetVar VAR_0x8001, ABILITY_PICKPOCKET
    SetVar VAR_0x8002, MOVE_SPLASH
    SetVar VAR_0x8004, ITEM_LEFTOVERS
    GoTo TestKit_GivePokemonWithItem

/* Poison Touch: a wild Chansey that knows only Tackle. About one Drain
   Punch or Sucker Punch in three poisons Chansey, with a message naming
   Poison Touch; Vacuum Wave, which makes no contact, never does it. */
TestKit_AbilityPoisonTouch:
    SetVar VAR_0x800A, SPECIES_TOXICROAK
    SetVar VAR_0x800B, ABILITY_POISON_TOUCH
    SetVar VAR_0x8006, MOVE_DRAIN_PUNCH
    SetVar VAR_0x8007, MOVE_SUCKER_PUNCH
    SetVar VAR_0x8008, MOVE_VACUUM_WAVE
    SetVar VAR_0x8009, MOVE_PROTECT
    SetVar VAR_0x8000, SPECIES_CHANSEY
    SetVar VAR_0x8001, ABILITY_NONE
    SetVar VAR_0x8002, MOVE_TACKLE
    GoTo TestKit_GivePokemonWithMoves

/* Rattled: a wild Poochyena that knows only Bite. Each
   Bite that hits raises Dunsparce's Speed a stage, with a message. Its
   answer to Intimidate needs the Intimidate holder to come in against it,
   which the kit's wild battle cannot arrange. */
TestKit_AbilityRattled:
    SetVar VAR_0x800A, SPECIES_DUNSPARCE
    SetVar VAR_0x800B, ABILITY_RATTLED
    SetVar VAR_0x8006, MOVE_SPLASH
    SetVar VAR_0x8007, MOVE_ROOST
    SetVar VAR_0x8008, MOVE_BODY_SLAM
    SetVar VAR_0x8009, MOVE_PROTECT
    SetVar VAR_0x8000, SPECIES_POOCHYENA
    SetVar VAR_0x8001, ABILITY_NONE
    SetVar VAR_0x8002, MOVE_BITE
    GoTo TestKit_GivePokemonWithMoves

/* Sand Force: a wild Chansey that knows only Splash. With
   Sandstorm up, Chansey is buffeted at the end of each turn and Shellos,
   a Water type, is not. Earth Power's 30% rise in the sand has no
   message. */
TestKit_AbilitySandForce:
    SetVar VAR_0x800A, SPECIES_SHELLOS
    SetVar VAR_0x800B, ABILITY_SAND_FORCE
    SetVar VAR_0x8006, MOVE_SANDSTORM
    SetVar VAR_0x8007, MOVE_EARTH_POWER
    SetVar VAR_0x8008, MOVE_RECOVER
    SetVar VAR_0x8009, MOVE_PROTECT
    SetVar VAR_0x8000, SPECIES_CHANSEY
    SetVar VAR_0x8001, ABILITY_NONE
    SetVar VAR_0x8002, MOVE_SPLASH
    GoTo TestKit_GivePokemonWithMoves

/* Sand Rush: a wild Charizard that knows only Growl, faster than
   Sandslash. Before Sandstorm, Charizard moves first; once it is up,
   Sandslash does, until the sand dies down (only a rare pairing of
   natures and IVs keeps Charizard ahead). Sandslash, a Ground type, takes
   no sand damage either way. */
TestKit_AbilitySandRush:
    SetVar VAR_0x800A, SPECIES_SANDSLASH
    SetVar VAR_0x800B, ABILITY_SAND_RUSH
    SetVar VAR_0x8006, MOVE_SANDSTORM
    SetVar VAR_0x8007, MOVE_SPLASH
    SetVar VAR_0x8008, MOVE_EARTHQUAKE
    SetVar VAR_0x8009, MOVE_PROTECT
    SetVar VAR_0x8000, SPECIES_CHARIZARD
    SetVar VAR_0x8001, ABILITY_NONE
    SetVar VAR_0x8002, MOVE_GROWL
    GoTo TestKit_GivePokemonWithMoves

/* Toxic Boost: the player's Snorlax (its own ability) and a
   wild Zangoose given Toxic Boost that knows only Mega Punch. Once Toxic
   has poisoned Zangoose, its Mega Punch takes about half again as much of
   Snorlax's HP as before. */
TestKit_AbilityToxicBoost:
    SetVar VAR_0x800A, SPECIES_SNORLAX
    SetVar VAR_0x800B, ABILITY_NONE
    SetVar VAR_0x8006, MOVE_TOXIC
    SetVar VAR_0x8007, MOVE_SPLASH
    SetVar VAR_0x8008, MOVE_REST
    SetVar VAR_0x8009, MOVE_PROTECT
    SetVar VAR_0x8000, SPECIES_ZANGOOSE
    SetVar VAR_0x8001, ABILITY_TOXIC_BOOST
    SetVar VAR_0x8002, MOVE_MEGA_PUNCH
    GoTo TestKit_GivePokemonWithMoves

/* Wonder Skin: a wild Chansey that knows only Growl. Once
   Delcatty is in, about one Growl in two misses, where it never would
   without Wonder Skin. */
TestKit_AbilityWonderSkin:
    SetVar VAR_0x800A, SPECIES_DELCATTY
    SetVar VAR_0x800B, ABILITY_WONDER_SKIN
    SetVar VAR_0x8006, MOVE_SPLASH
    SetVar VAR_0x8007, MOVE_BODY_SLAM
    SetVar VAR_0x8008, MOVE_REST
    SetVar VAR_0x8009, MOVE_PROTECT
    SetVar VAR_0x8000, SPECIES_CHANSEY
    SetVar VAR_0x8001, ABILITY_NONE
    SetVar VAR_0x8002, MOVE_GROWL
    GoTo TestKit_GivePokemonWithMoves

/* The staples survey's engine rulings (Ian, 2026-09-26): the later games'
   rules for native abilities, type immunities, critical hits, Defog and Rapid
   Spin. Each entry is built as an ability entry is, with a foe where it needs
   one. */
TestKit_Staples:
    GetPartyCount VAR_0x8005
    GoToIfGe VAR_0x8005, 6, TestKit_PartyFull
    Message TestKit_Text_WhichRule
    InitLocalTextListMenu 1, 1, 0, VAR_0x8004
    AddListMenuEntry TestKit_Text_MenuStapleSturdy, 0
    AddListMenuEntry TestKit_Text_MenuStapleLightningRod, 1
    AddListMenuEntry TestKit_Text_MenuStapleStormDrain, 2
    AddListMenuEntry TestKit_Text_MenuStapleIntimidate, 3
    AddListMenuEntry TestKit_Text_MenuStapleOblivious, 4
    AddListMenuEntry TestKit_Text_MenuStapleIlluminate, 5
    AddListMenuEntry TestKit_Text_MenuStapleSynchronize, 6
    AddListMenuEntry TestKit_Text_MenuStapleLeafGuard, 7
    AddListMenuEntry TestKit_Text_MenuStapleStench, 8
    AddListMenuEntry TestKit_Text_MenuStapleWaterAbsorb, 9
    AddListMenuEntry TestKit_Text_MenuStapleMagicGuard, 10
    AddListMenuEntry TestKit_Text_MenuStapleLiquidOoze, 11
    AddListMenuEntry TestKit_Text_MenuStapleSimple, 12
    AddListMenuEntry TestKit_Text_MenuStapleGrassPowder, 13
    AddListMenuEntry TestKit_Text_MenuStapleElectricParalysis, 14
    AddListMenuEntry TestKit_Text_MenuStapleGhostTrap, 15
    AddListMenuEntry TestKit_Text_MenuStapleCritical, 16
    AddListMenuEntry TestKit_Text_MenuStapleDefog, 17
    AddListMenuEntry TestKit_Text_MenuStapleRapidSpin, 18
    AddListMenuEntry TestKit_Text_MenuStapleProtectRun, 19
    AddListMenuEntry TestKit_Text_MenuStapleHiddenGift, 20
    AddListMenuEntry TestKit_Text_MenuStapleHiddenWild, 21
    AddListMenuEntry TestKit_Text_MenuStapleItemsRestored, 22
    AddListMenuEntry TestKit_Text_MenuStapleKaizoMoves, 23
    ShowListMenu
    GoToIfEq VAR_0x8004, 0, TestKit_StapleSturdy
    GoToIfEq VAR_0x8004, 1, TestKit_StapleLightningRod
    GoToIfEq VAR_0x8004, 2, TestKit_StapleStormDrain
    GoToIfEq VAR_0x8004, 3, TestKit_StapleIntimidate
    GoToIfEq VAR_0x8004, 4, TestKit_StapleOblivious
    GoToIfEq VAR_0x8004, 5, TestKit_StapleIlluminate
    GoToIfEq VAR_0x8004, 6, TestKit_StapleSynchronize
    GoToIfEq VAR_0x8004, 7, TestKit_StapleLeafGuard
    GoToIfEq VAR_0x8004, 8, TestKit_StapleStench
    GoToIfEq VAR_0x8004, 9, TestKit_StapleWaterAbsorb
    GoToIfEq VAR_0x8004, 10, TestKit_StapleMagicGuard
    GoToIfEq VAR_0x8004, 11, TestKit_StapleLiquidOoze
    GoToIfEq VAR_0x8004, 12, TestKit_StapleSimple
    GoToIfEq VAR_0x8004, 13, TestKit_StapleGrassPowder
    GoToIfEq VAR_0x8004, 14, TestKit_StapleElectricParalysis
    GoToIfEq VAR_0x8004, 15, TestKit_StapleGhostTrap
    GoToIfEq VAR_0x8004, 16, TestKit_StapleCritical
    GoToIfEq VAR_0x8004, 17, TestKit_StapleDefog
    GoToIfEq VAR_0x8004, 18, TestKit_StapleRapidSpin
    GoToIfEq VAR_0x8004, 19, TestKit_StapleProtectRun
    GoToIfEq VAR_0x8004, 20, TestKit_StapleHiddenGift
    GoToIfEq VAR_0x8004, 21, TestKit_StapleHiddenWild
    GoToIfEq VAR_0x8004, 22, TestKit_StapleItemsRestored
    GoToIfEq VAR_0x8004, 23, TestKit_StapleKaizoMoves
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

/* Leaf Guard and Rest: a Leafeon given Leaf Guard, against a wild Rattata
   that knows only Tackle. */
TestKit_StapleLeafGuard:
    SetVar VAR_0x800A, SPECIES_LEAFEON
    SetVar VAR_0x800B, ABILITY_LEAF_GUARD
    SetVar VAR_0x8006, MOVE_SUNNY_DAY
    SetVar VAR_0x8007, MOVE_REST
    SetVar VAR_0x8008, MOVE_LEAF_BLADE
    SetVar VAR_0x8009, MOVE_SWORDS_DANCE
    SetVar VAR_0x8000, SPECIES_RATTATA
    SetVar VAR_0x8001, ABILITY_NONE
    SetVar VAR_0x8002, MOVE_TACKLE
    GoTo TestKit_GivePokemonWithMoves

/* Stench: a Skuntank given Stench, against a wild Snorlax that knows only
   Splash. */
TestKit_StapleStench:
    SetVar VAR_0x800A, SPECIES_SKUNTANK
    SetVar VAR_0x800B, ABILITY_STENCH
    SetVar VAR_0x8006, MOVE_FURY_SWIPES
    SetVar VAR_0x8007, MOVE_SCRATCH
    SetVar VAR_0x8008, MOVE_PROTECT
    SetVar VAR_0x8009, MOVE_NIGHT_SLASH
    SetVar VAR_0x8000, SPECIES_SNORLAX
    SetVar VAR_0x8001, ABILITY_NONE
    SetVar VAR_0x8002, MOVE_SPLASH
    GoTo TestKit_GivePokemonWithMoves

/* Water Absorb and Soak: a Lapras that knows Soak, against a wild Vaporeon
   given Water Absorb that knows only Growl. */
TestKit_StapleWaterAbsorb:
    SetVar VAR_0x800A, SPECIES_LAPRAS
    SetVar VAR_0x800B, ABILITY_NONE
    SetVar VAR_0x8006, MOVE_SOAK
    SetVar VAR_0x8007, MOVE_THUNDERBOLT
    SetVar VAR_0x8008, MOVE_ICE_BEAM
    SetVar VAR_0x8009, MOVE_SING
    SetVar VAR_0x8000, SPECIES_VAPOREON
    SetVar VAR_0x8001, ABILITY_WATER_ABSORB
    SetVar VAR_0x8002, MOVE_GROWL
    GoTo TestKit_GivePokemonWithMoves

/* Magic Guard and paralysis: a Clefable given Magic Guard, against a wild
   Jolteon that knows only Thunder Wave. */
TestKit_StapleMagicGuard:
    SetVar VAR_0x800A, SPECIES_CLEFABLE
    SetVar VAR_0x800B, ABILITY_MAGIC_GUARD
    SetVar VAR_0x8006, MOVE_MOONBLAST
    SetVar VAR_0x8007, MOVE_CALM_MIND
    SetVar VAR_0x8008, MOVE_SOFTBOILED
    SetVar VAR_0x8009, MOVE_FLAMETHROWER
    SetVar VAR_0x8000, SPECIES_JOLTEON
    SetVar VAR_0x8001, ABILITY_NONE
    SetVar VAR_0x8002, MOVE_THUNDER_WAVE
    GoTo TestKit_GivePokemonWithMoves

/* Liquid Ooze and Dream Eater: a Gengar that knows Hypnosis and Dream
   Eater, against a wild Tentacruel given Liquid Ooze that knows only
   Splash. */
TestKit_StapleLiquidOoze:
    SetVar VAR_0x800A, SPECIES_GENGAR
    SetVar VAR_0x800B, ABILITY_NONE
    SetVar VAR_0x8006, MOVE_HYPNOSIS
    SetVar VAR_0x8007, MOVE_DREAM_EATER
    SetVar VAR_0x8008, MOVE_SHADOW_BALL
    SetVar VAR_0x8009, MOVE_GIGA_DRAIN
    SetVar VAR_0x8000, SPECIES_TENTACRUEL
    SetVar VAR_0x8001, ABILITY_LIQUID_OOZE
    SetVar VAR_0x8002, MOVE_SPLASH
    GoTo TestKit_GivePokemonWithMoves

/* Simple: a Bibarel given Simple, against a wild Chansey that knows only
   Growl. */
TestKit_StapleSimple:
    SetVar VAR_0x800A, SPECIES_BIBAREL
    SetVar VAR_0x800B, ABILITY_SIMPLE
    SetVar VAR_0x8006, MOVE_DEFENSE_CURL
    SetVar VAR_0x8007, MOVE_SWORDS_DANCE
    SetVar VAR_0x8008, MOVE_RETURN
    SetVar VAR_0x8009, MOVE_WATERFALL
    SetVar VAR_0x8000, SPECIES_CHANSEY
    SetVar VAR_0x8001, ABILITY_NONE
    SetVar VAR_0x8002, MOVE_GROWL
    GoTo TestKit_GivePokemonWithMoves

/* Grass and powder: a Venusaur, against a wild Parasect given Effect Spore
   that knows Spore and Stun Spore. */
TestKit_StapleGrassPowder:
    SetVar VAR_0x800A, SPECIES_VENUSAUR
    SetVar VAR_0x800B, ABILITY_NONE
    SetVar VAR_0x8006, MOVE_GIGA_DRAIN
    SetVar VAR_0x8007, MOVE_SLUDGE_BOMB
    SetVar VAR_0x8008, MOVE_BODY_SLAM
    SetVar VAR_0x8009, MOVE_SYNTHESIS
    SetVar VAR_0x8000, SPECIES_PARASECT
    SetVar VAR_0x8001, ABILITY_EFFECT_SPORE
    SetVar VAR_0x8002, MOVE_SPORE
    SetVar VAR_0x8003, MOVE_STUN_SPORE
    GoTo TestKit_GivePokemonWithMoves

/* Electric and paralysis: a Luxray, against a wild Arbok that knows Glare
   and Thunder Wave. */
TestKit_StapleElectricParalysis:
    SetVar VAR_0x800A, SPECIES_LUXRAY
    SetVar VAR_0x800B, ABILITY_NONE
    SetVar VAR_0x8006, MOVE_SPARK
    SetVar VAR_0x8007, MOVE_CRUNCH
    SetVar VAR_0x8008, MOVE_ROAR
    SetVar VAR_0x8009, MOVE_CHARGE
    SetVar VAR_0x8000, SPECIES_ARBOK
    SetVar VAR_0x8001, ABILITY_NONE
    SetVar VAR_0x8002, MOVE_GLARE
    SetVar VAR_0x8003, MOVE_THUNDER_WAVE
    GoTo TestKit_GivePokemonWithMoves

/* Ghosts and trapping: a Mismagius, against a wild Umbreon that knows Mean
   Look and Fire Spin (Wrap, a Normal move, would not touch a Ghost). */
TestKit_StapleGhostTrap:
    SetVar VAR_0x800A, SPECIES_MISMAGIUS
    SetVar VAR_0x800B, ABILITY_NONE
    SetVar VAR_0x8006, MOVE_SHADOW_BALL
    SetVar VAR_0x8007, MOVE_MYSTICAL_FIRE
    SetVar VAR_0x8008, MOVE_PROTECT
    SetVar VAR_0x8009, MOVE_TELEPORT
    SetVar VAR_0x8000, SPECIES_UMBREON
    SetVar VAR_0x8001, ABILITY_NONE
    SetVar VAR_0x8002, MOVE_MEAN_LOOK
    SetVar VAR_0x8003, MOVE_FIRE_SPIN
    GoTo TestKit_GivePokemonWithMoves

/* Critical hits: a Mew with Focus Energy and Slash, against a wild Snorlax
   that knows only Splash. Focus Energy's two stages and Slash's one make
   three, which is always a critical hit at the Generation 7 rates. */
TestKit_StapleCritical:
    SetVar VAR_0x8006, MOVE_FOCUS_ENERGY
    SetVar VAR_0x8007, MOVE_SLASH
    SetVar VAR_0x8008, MOVE_TACKLE
    SetVar VAR_0x8009, MOVE_RECOVER
    SetVar VAR_0x8000, SPECIES_SNORLAX
    SetVar VAR_0x8001, ABILITY_NONE
    SetVar VAR_0x8002, MOVE_SPLASH
    SetVar VAR_0x800A, SPECIES_MEW
    GoTo TestKit_GivePokemonWithMoves

/* Defog: a Mew with Defog, Stealth Rock and Reflect, against a wild
   Skarmory that knows Spikes and Toxic Spikes. */
TestKit_StapleDefog:
    SetVar VAR_0x8006, MOVE_DEFOG
    SetVar VAR_0x8007, MOVE_STEALTH_ROCK
    SetVar VAR_0x8008, MOVE_REFLECT
    SetVar VAR_0x8009, MOVE_RECOVER
    SetVar VAR_0x8000, SPECIES_SKARMORY
    SetVar VAR_0x8001, ABILITY_NONE
    SetVar VAR_0x8002, MOVE_SPIKES
    SetVar VAR_0x8003, MOVE_TOXIC_SPIKES
    SetVar VAR_0x800A, SPECIES_MEW
    GoTo TestKit_GivePokemonWithMoves

/* Rapid Spin: a Starmie with Rapid Spin, against a wild Skarmory that knows
   only Spikes. */
TestKit_StapleRapidSpin:
    SetVar VAR_0x800A, SPECIES_STARMIE
    SetVar VAR_0x800B, ABILITY_NONE
    SetVar VAR_0x8006, MOVE_RAPID_SPIN
    SetVar VAR_0x8007, MOVE_SURF
    SetVar VAR_0x8008, MOVE_THUNDERBOLT
    SetVar VAR_0x8009, MOVE_RECOVER
    SetVar VAR_0x8000, SPECIES_SKARMORY
    SetVar VAR_0x8001, ABILITY_NONE
    SetVar VAR_0x8002, MOVE_SPIKES
    GoTo TestKit_GivePokemonWithMoves

/* Protect in a row: a Mew with King's Shield, Spiky Shield and Protect,
   against a wild Rattata that knows only Tackle. Each of the three loses
   reliability when used in a row, the new two as Protect does (element 4
   fix, cloud/element6-changes). */
TestKit_StapleProtectRun:
    SetVar VAR_0x8006, MOVE_KINGS_SHIELD
    SetVar VAR_0x8007, MOVE_SPIKY_SHIELD
    SetVar VAR_0x8008, MOVE_PROTECT
    SetVar VAR_0x8009, MOVE_RECOVER
    SetVar VAR_0x8000, SPECIES_RATTATA
    SetVar VAR_0x8001, ABILITY_NONE
    SetVar VAR_0x8002, MOVE_TACKLE
    SetVar VAR_0x800A, SPECIES_MEW
    GoTo TestKit_GivePokemonWithMoves

/* Hidden abilities (element 8): Litten's is Intimidate, where its ordinary
   slots are both Blaze, so the summary tells them apart. The flag is taken by
   the next gift or scripted wild Pokemon and then clears itself. One Rare
   Candy takes the gift to Torracat, whose hidden ability is Intimidate too. */
TestKit_StapleHiddenGift:
    GetPartyCount VAR_0x8005
    GoToIfGe VAR_0x8005, 6, TestKit_PartyFull
    SetFlag FLAG_NEXT_MON_HIDDEN_ABILITY
    GivePokemon SPECIES_LITTEN, 15, ITEM_NONE, VAR_RESULT
    Message TestKit_Text_HiddenGift
    GoTo TestKit_WaitAndClose

/* The wild Litten's Intimidate announces itself as the battle starts. */
TestKit_StapleHiddenWild:
    Message TestKit_Text_HiddenWild
    WaitButton
    CloseMessage
    SetFlag FLAG_NEXT_MON_HIDDEN_ABILITY
    StartWildBattle SPECIES_LITTEN, 15
    GoTo TestKit_AfterBattle

/* Held items restored after battle (element 8): a Mew holding a Sitrus
   Berry, against a wild Chansey that knows only Splash. Belly Drum halves
   Mew's HP and it eats the Berry; after the battle, won or run from, its
   summary shows the Sitrus Berry again. */
TestKit_StapleItemsRestored:
    SetVar VAR_0x800A, SPECIES_MEW
    SetVar VAR_0x8004, ITEM_SITRUS_BERRY
    SetVar VAR_0x8006, MOVE_BELLY_DRUM
    SetVar VAR_0x8007, MOVE_TACKLE
    SetVar VAR_0x8008, MOVE_RECOVER
    SetVar VAR_0x8009, MOVE_SPLASH
    SetVar VAR_0x8000, SPECIES_CHANSEY
    SetVar VAR_0x8001, ABILITY_NONE
    SetVar VAR_0x8002, MOVE_SPLASH
    GoTo TestKit_GivePokemonWithItem

/* The Kaizo comparison's move data (Ian, 2026-09-27): a Mew with Extreme
   Speed and Minimize, against a wild Shuckle that knows only Fake Out.
   Fake Out is now +3 and Extreme Speed +2, so the far slower Shuckle's
   Fake Out ("But it failed!" after the first turn) comes before Mew's
   Extreme Speed every turn; before, both were +1 and Mew went first.
   Minimize raises evasion two stages ("sharply rose!"), not one. */
TestKit_StapleKaizoMoves:
    SetVar VAR_0x8006, MOVE_EXTREME_SPEED
    SetVar VAR_0x8007, MOVE_MINIMIZE
    SetVar VAR_0x8008, MOVE_PROTECT
    SetVar VAR_0x8009, MOVE_RECOVER
    SetVar VAR_0x8000, SPECIES_SHUCKLE
    SetVar VAR_0x8001, ABILITY_NONE
    SetVar VAR_0x8002, MOVE_FAKE_OUT
    SetVar VAR_0x800A, SPECIES_MEW
    GoTo TestKit_GivePokemonWithMoves

/* Element 7's items (docs/oxide/test-kit.md, "The item entries"). "All new
   items" puts one of each of the 46 in the bag, for their names, icons,
   pockets and descriptions; the entries after it set up a battle for one
   item or a group. */
TestKit_Items:
    Message TestKit_Text_WhichItems
    InitLocalTextListMenu 1, 1, 0, VAR_0x8004
    AddListMenuEntry TestKit_Text_MenuItemsAll, 0
    AddListMenuEntry TestKit_Text_MenuItemEviolite, 1
    AddListMenuEntry TestKit_Text_MenuItemAssaultVest, 2
    AddListMenuEntry TestKit_Text_MenuItemPunchingGlove, 3
    AddListMenuEntry TestKit_Text_MenuItemFairyFeather, 4
    AddListMenuEntry TestKit_Text_MenuItemRingTarget, 5
    AddListMenuEntry TestKit_Text_MenuItemSafetyGoggles, 6
    AddListMenuEntry TestKit_Text_MenuItemCovertCloak, 7
    AddListMenuEntry TestKit_Text_MenuItemClearAmulet, 8
    AddListMenuEntry TestKit_Text_MenuItemAbilityShield, 9
    AddListMenuEntry TestKit_Text_MenuItemRockyHelmet, 10
    AddListMenuEntry TestKit_Text_MenuItemAbsorbBulb, 11
    AddListMenuEntry TestKit_Text_MenuItemCellBattery, 12
    AddListMenuEntry TestKit_Text_MenuItemWeaknessPolicy, 13
    AddListMenuEntry TestKit_Text_MenuItemAirBalloon, 14
    AddListMenuEntry TestKit_Text_MenuItemBindingBand, 15
    AddListMenuEntry TestKit_Text_MenuItemLoadedDice, 16
    AddListMenuEntry TestKit_Text_MenuItemMirrorHerb, 17
    AddListMenuEntry TestKit_Text_MenuItemEjectButton, 18
    AddListMenuEntry TestKit_Text_MenuItemRedCard, 19
    AddListMenuEntry TestKit_Text_MenuItemPixiePlate, 20
    AddListMenuEntry TestKit_Text_MenuItemRoseliBerry, 21
    AddListMenuEntry TestKit_Text_MenuItemAbilities, 22
    AddListMenuEntry TestKit_Text_MenuItemMintsCaps, 23
    AddListMenuEntry TestKit_Text_MenuItemTMs, 24
    ShowListMenu
    GoToIfEq VAR_0x8004, 0, TestKit_ItemsAll
    GoToIfEq VAR_0x8004, 1, TestKit_ItemEviolite
    GoToIfEq VAR_0x8004, 2, TestKit_ItemAssaultVest
    GoToIfEq VAR_0x8004, 3, TestKit_ItemPunchingGlove
    GoToIfEq VAR_0x8004, 4, TestKit_ItemFairyFeather
    GoToIfEq VAR_0x8004, 5, TestKit_ItemRingTarget
    GoToIfEq VAR_0x8004, 6, TestKit_ItemSafetyGoggles
    GoToIfEq VAR_0x8004, 7, TestKit_ItemCovertCloak
    GoToIfEq VAR_0x8004, 8, TestKit_ItemClearAmulet
    GoToIfEq VAR_0x8004, 9, TestKit_ItemAbilityShield
    GoToIfEq VAR_0x8004, 10, TestKit_ItemRockyHelmet
    GoToIfEq VAR_0x8004, 11, TestKit_ItemAbsorbBulb
    GoToIfEq VAR_0x8004, 12, TestKit_ItemCellBattery
    GoToIfEq VAR_0x8004, 13, TestKit_ItemWeaknessPolicy
    GoToIfEq VAR_0x8004, 14, TestKit_ItemAirBalloon
    GoToIfEq VAR_0x8004, 15, TestKit_ItemBindingBand
    GoToIfEq VAR_0x8004, 16, TestKit_ItemLoadedDice
    GoToIfEq VAR_0x8004, 17, TestKit_ItemMirrorHerb
    GoToIfEq VAR_0x8004, 18, TestKit_ItemEjectButton
    GoToIfEq VAR_0x8004, 19, TestKit_ItemRedCard
    GoToIfEq VAR_0x8004, 20, TestKit_ItemPixiePlate
    GoToIfEq VAR_0x8004, 21, TestKit_ItemRoseliBerry
    GoToIfEq VAR_0x8004, 22, TestKit_ItemAbilities
    GoToIfEq VAR_0x8004, 23, TestKit_ItemMintsCaps
    GoToIfEq VAR_0x8004, 24, TestKit_ItemTMs
    GoTo TestKit_Close

TestKit_ItemsAll:
    AddItem ITEM_EVIOLITE, 1, VAR_RESULT
    AddItem ITEM_AIR_BALLOON, 1, VAR_RESULT
    AddItem ITEM_ROCKY_HELMET, 1, VAR_RESULT
    AddItem ITEM_ASSAULT_VEST, 1, VAR_RESULT
    AddItem ITEM_WEAKNESS_POLICY, 1, VAR_RESULT
    AddItem ITEM_SAFETY_GOGGLES, 1, VAR_RESULT
    AddItem ITEM_RED_CARD, 1, VAR_RESULT
    AddItem ITEM_EJECT_BUTTON, 1, VAR_RESULT
    AddItem ITEM_RING_TARGET, 1, VAR_RESULT
    AddItem ITEM_BINDING_BAND, 1, VAR_RESULT
    AddItem ITEM_ABSORB_BULB, 1, VAR_RESULT
    AddItem ITEM_CELL_BATTERY, 1, VAR_RESULT
    AddItem ITEM_COVERT_CLOAK, 1, VAR_RESULT
    AddItem ITEM_CLEAR_AMULET, 1, VAR_RESULT
    AddItem ITEM_MIRROR_HERB, 1, VAR_RESULT
    AddItem ITEM_LOADED_DICE, 1, VAR_RESULT
    AddItem ITEM_PUNCHING_GLOVE, 1, VAR_RESULT
    AddItem ITEM_ABILITY_SHIELD, 1, VAR_RESULT
    AddItem ITEM_FAIRY_FEATHER, 1, VAR_RESULT
    AddItem ITEM_PIXIE_PLATE, 1, VAR_RESULT
    AddItem ITEM_ABILITY_CAPSULE, 1, VAR_RESULT
    AddItem ITEM_ABILITY_PATCH, 1, VAR_RESULT
    AddItem ITEM_ROSELI_BERRY, 1, VAR_RESULT
    AddItem ITEM_BOTTLE_CAP, 1, VAR_RESULT
    AddItem ITEM_GOLD_BOTTLE_CAP, 1, VAR_RESULT
    AddItem ITEM_LONELY_MINT, 1, VAR_RESULT
    AddItem ITEM_ADAMANT_MINT, 1, VAR_RESULT
    AddItem ITEM_NAUGHTY_MINT, 1, VAR_RESULT
    AddItem ITEM_BRAVE_MINT, 1, VAR_RESULT
    AddItem ITEM_BOLD_MINT, 1, VAR_RESULT
    AddItem ITEM_IMPISH_MINT, 1, VAR_RESULT
    AddItem ITEM_LAX_MINT, 1, VAR_RESULT
    AddItem ITEM_RELAXED_MINT, 1, VAR_RESULT
    AddItem ITEM_MODEST_MINT, 1, VAR_RESULT
    AddItem ITEM_MILD_MINT, 1, VAR_RESULT
    AddItem ITEM_RASH_MINT, 1, VAR_RESULT
    AddItem ITEM_QUIET_MINT, 1, VAR_RESULT
    AddItem ITEM_CALM_MINT, 1, VAR_RESULT
    AddItem ITEM_GENTLE_MINT, 1, VAR_RESULT
    AddItem ITEM_CAREFUL_MINT, 1, VAR_RESULT
    AddItem ITEM_SASSY_MINT, 1, VAR_RESULT
    AddItem ITEM_TIMID_MINT, 1, VAR_RESULT
    AddItem ITEM_HASTY_MINT, 1, VAR_RESULT
    AddItem ITEM_JOLLY_MINT, 1, VAR_RESULT
    AddItem ITEM_NAIVE_MINT, 1, VAR_RESULT
    AddItem ITEM_SERIOUS_MINT, 1, VAR_RESULT
    Message TestKit_Text_ItemsAll
    GoTo TestKit_WaitAndClose

/* Element 7's held-item entries: two Lv. 50 VAR_0x800A with the four moves in
   VAR_0x8006 to VAR_0x8009 (and the ability VAR_0x800B, unless ABILITY_NONE),
   the first holding the item VAR_0x8004 and the second nothing, so each item
   is seen beside a baseline. Then, when VAR_0x8000 names one, the foe is
   fought as in TestKit_AbilityFoe. Needs two free party slots. */
TestKit_GiveItemPair:
    GetPartyCount VAR_0x8005
    GoToIfGe VAR_0x8005, 5, TestKit_PartyFull
    GivePokemon VAR_0x800A, 50, VAR_0x8004, VAR_RESULT
    CallIfNe VAR_0x800B, ABILITY_NONE, TestKit_SetAbility
    Call TestKit_SetPairMoves
    AddVar VAR_0x8005, 1
    GivePokemon VAR_0x800A, 50, ITEM_NONE, VAR_RESULT
    CallIfNe VAR_0x800B, ABILITY_NONE, TestKit_SetAbility
    Call TestKit_SetPairMoves
    BufferItemName 0, VAR_0x8004
    Message TestKit_Text_ItemPair
    GoToIfNe VAR_0x8000, SPECIES_NONE, TestKit_AbilityFoe
    GoTo TestKit_WaitAndClose

TestKit_SetPairMoves:
    ResetPartyMonMoveSlot_Unused VAR_0x8005, 0, VAR_0x8006
    ResetPartyMonMoveSlot_Unused VAR_0x8005, 1, VAR_0x8007
    ResetPartyMonMoveSlot_Unused VAR_0x8005, 2, VAR_0x8008
    ResetPartyMonMoveSlot_Unused VAR_0x8005, 3, VAR_0x8009
    Return

/* The Eviolite: Chansey, which can still evolve, against a wild Machamp
   that knows only Karate Chop. Each chop takes about two thirds as much
   from the Chansey holding it as from the other. */
TestKit_ItemEviolite:
    SetVar VAR_0x8000, SPECIES_MACHAMP
    SetVar VAR_0x8001, ABILITY_NONE
    SetVar VAR_0x8002, MOVE_KARATE_CHOP
    SetVar VAR_0x8003, MOVE_NONE
    SetVar VAR_0x800A, SPECIES_CHANSEY
    SetVar VAR_0x800B, ABILITY_NONE
    SetVar VAR_0x8004, ITEM_EVIOLITE
    SetVar VAR_0x8006, MOVE_SPLASH
    SetVar VAR_0x8007, MOVE_SOFTBOILED
    SetVar VAR_0x8008, MOVE_PROTECT
    SetVar VAR_0x8009, MOVE_SEISMIC_TOSS
    GoTo TestKit_GiveItemPair

/* The Assault Vest: Mew against a wild Magmortar that knows only
   Flamethrower. The Mew wearing it cannot choose Swords Dance or Recover
   ("The effects of the Assault Vest prevent the use of status moves!"),
   and each Flamethrower takes about two thirds as much from it as from
   the other Mew. */
TestKit_ItemAssaultVest:
    SetVar VAR_0x8000, SPECIES_MAGMORTAR
    SetVar VAR_0x8001, ABILITY_NONE
    SetVar VAR_0x8002, MOVE_FLAMETHROWER
    SetVar VAR_0x8003, MOVE_NONE
    SetVar VAR_0x800A, SPECIES_MEW
    SetVar VAR_0x800B, ABILITY_NONE
    SetVar VAR_0x8004, ITEM_ASSAULT_VEST
    SetVar VAR_0x8006, MOVE_PSYCHIC
    SetVar VAR_0x8007, MOVE_SWORDS_DANCE
    SetVar VAR_0x8008, MOVE_RECOVER
    SetVar VAR_0x8009, MOVE_TACKLE
    GoTo TestKit_GiveItemPair

/* The Punching Glove: Hitmonchan against a wild Ferrothorn given Iron
   Barbs that knows only Iron Defense. The gloved Hitmonchan's Ice Punch
   does about a tenth more than the other's and brings no Iron Barbs
   damage; its Close Combat, a kick, still does. */
TestKit_ItemPunchingGlove:
    SetVar VAR_0x8000, SPECIES_FERROTHORN
    SetVar VAR_0x8001, ABILITY_IRON_BARBS
    SetVar VAR_0x8002, MOVE_IRON_DEFENSE
    SetVar VAR_0x8003, MOVE_NONE
    SetVar VAR_0x800A, SPECIES_HITMONCHAN
    SetVar VAR_0x800B, ABILITY_NONE
    SetVar VAR_0x8004, ITEM_PUNCHING_GLOVE
    SetVar VAR_0x8006, MOVE_ICE_PUNCH
    SetVar VAR_0x8007, MOVE_MACH_PUNCH
    SetVar VAR_0x8008, MOVE_CLOSE_COMBAT
    SetVar VAR_0x8009, MOVE_BULK_UP
    GoTo TestKit_GiveItemPair

/* The Fairy Feather: Clefable against a wild Chansey that knows only
   Splash. Moonblast from the Clefable holding it does about a fifth more
   than from the other. */
TestKit_ItemFairyFeather:
    SetVar VAR_0x8000, SPECIES_CHANSEY
    SetVar VAR_0x8001, ABILITY_NONE
    SetVar VAR_0x8002, MOVE_SPLASH
    SetVar VAR_0x8003, MOVE_NONE
    SetVar VAR_0x800A, SPECIES_CLEFABLE
    SetVar VAR_0x800B, ABILITY_NONE
    SetVar VAR_0x8004, ITEM_FAIRY_FEATHER
    SetVar VAR_0x8006, MOVE_MOONBLAST
    SetVar VAR_0x8007, MOVE_DAZZLING_GLEAM
    SetVar VAR_0x8008, MOVE_CALM_MIND
    SetVar VAR_0x8009, MOVE_MOONLIGHT
    GoTo TestKit_GiveItemPair

/* The Ring Target: Skarmory against a wild Dugtrio that knows only
   Earthquake. The Skarmory holding it takes Earthquake, super effective
   through its Steel type; the other is not affected. */
TestKit_ItemRingTarget:
    SetVar VAR_0x8000, SPECIES_DUGTRIO
    SetVar VAR_0x8001, ABILITY_NONE
    SetVar VAR_0x8002, MOVE_EARTHQUAKE
    SetVar VAR_0x8003, MOVE_NONE
    SetVar VAR_0x800A, SPECIES_SKARMORY
    SetVar VAR_0x800B, ABILITY_NONE
    SetVar VAR_0x8004, ITEM_RING_TARGET
    SetVar VAR_0x8006, MOVE_ROOST
    SetVar VAR_0x8007, MOVE_SPIKES
    SetVar VAR_0x8008, MOVE_BRAVE_BIRD
    SetVar VAR_0x8009, MOVE_PROTECT
    GoTo TestKit_GiveItemPair

/* Safety Goggles: Snorlax against a wild Parasect given Effect Spore that
   knows Spore and Stun Spore. The Snorlax wearing them is not affected
   by either move, is never touched by Effect Spore when it uses Body Slam,
   and takes no damage from its own Sandstorm; the other Snorlax is. */
TestKit_ItemSafetyGoggles:
    SetVar VAR_0x8000, SPECIES_PARASECT
    SetVar VAR_0x8001, ABILITY_EFFECT_SPORE
    SetVar VAR_0x8002, MOVE_SPORE
    SetVar VAR_0x8003, MOVE_STUN_SPORE
    SetVar VAR_0x800A, SPECIES_SNORLAX
    SetVar VAR_0x800B, ABILITY_NONE
    SetVar VAR_0x8004, ITEM_SAFETY_GOGGLES
    SetVar VAR_0x8006, MOVE_SANDSTORM
    SetVar VAR_0x8007, MOVE_BODY_SLAM
    SetVar VAR_0x8008, MOVE_REST
    SetVar VAR_0x8009, MOVE_PROTECT
    GoTo TestKit_GiveItemPair

/* The Covert Cloak: Snorlax against a wild Jolteon that knows only Nuzzle,
   whose paralysis is an added effect. The cloaked Snorlax takes the damage
   and is never paralysed; the other always is. */
TestKit_ItemCovertCloak:
    SetVar VAR_0x8000, SPECIES_JOLTEON
    SetVar VAR_0x8001, ABILITY_NONE
    SetVar VAR_0x8002, MOVE_NUZZLE
    SetVar VAR_0x8003, MOVE_NONE
    SetVar VAR_0x800A, SPECIES_SNORLAX
    SetVar VAR_0x800B, ABILITY_NONE
    SetVar VAR_0x8004, ITEM_COVERT_CLOAK
    SetVar VAR_0x8006, MOVE_REST
    SetVar VAR_0x8007, MOVE_BODY_SLAM
    SetVar VAR_0x8008, MOVE_PROTECT
    SetVar VAR_0x8009, MOVE_SPLASH
    GoTo TestKit_GiveItemPair

/* The Clear Amulet: Mew against a wild Chansey that knows Growl and Sticky
   Web. Each Growl at the Mew wearing it brings "MEW's Clear Amulet prevents
   stat loss!"; the other Mew's Attack falls. Its own Swords Dance works.
   Once Chansey has laid the web, the Mew wearing it switched in is "caught
   in a sticky web!" and then the amulet prevents the loss; the other Mew's
   Speed falls. */
TestKit_ItemClearAmulet:
    SetVar VAR_0x8000, SPECIES_CHANSEY
    SetVar VAR_0x8001, ABILITY_NONE
    SetVar VAR_0x8002, MOVE_GROWL
    SetVar VAR_0x8003, MOVE_STICKY_WEB
    SetVar VAR_0x800A, SPECIES_MEW
    SetVar VAR_0x800B, ABILITY_NONE
    SetVar VAR_0x8004, ITEM_CLEAR_AMULET
    SetVar VAR_0x8006, MOVE_SWORDS_DANCE
    SetVar VAR_0x8007, MOVE_TACKLE
    SetVar VAR_0x8008, MOVE_RECOVER
    SetVar VAR_0x8009, MOVE_SPLASH
    GoTo TestKit_GiveItemPair

/* The Ability Shield: Mew against a wild Chansey that knows Worry Seed and
   Gastro Acid. Against the Mew holding it both fail ("But it failed!");
   against the other, Worry Seed gives it Insomnia and Gastro Acid
   suppresses its ability. */
TestKit_ItemAbilityShield:
    SetVar VAR_0x8000, SPECIES_CHANSEY
    SetVar VAR_0x8001, ABILITY_NONE
    SetVar VAR_0x8002, MOVE_WORRY_SEED
    SetVar VAR_0x8003, MOVE_GASTRO_ACID
    SetVar VAR_0x800A, SPECIES_MEW
    SetVar VAR_0x800B, ABILITY_NONE
    SetVar VAR_0x8004, ITEM_ABILITY_SHIELD
    SetVar VAR_0x8006, MOVE_SPLASH
    SetVar VAR_0x8007, MOVE_TACKLE
    SetVar VAR_0x8008, MOVE_RECOVER
    SetVar VAR_0x8009, MOVE_PROTECT
    GoTo TestKit_GiveItemPair

/* The Rocky Helmet: Skarmory against a wild Rattata that knows Tackle and
   Swift. Each Tackle into the helmeted Skarmory hurts Rattata by a sixth
   of its HP; Swift, which makes no contact, does not, and nor does a
   Tackle into the other Skarmory. */
TestKit_ItemRockyHelmet:
    SetVar VAR_0x8000, SPECIES_RATTATA
    SetVar VAR_0x8001, ABILITY_NONE
    SetVar VAR_0x8002, MOVE_TACKLE
    SetVar VAR_0x8003, MOVE_SWIFT
    SetVar VAR_0x800A, SPECIES_SKARMORY
    SetVar VAR_0x800B, ABILITY_NONE
    SetVar VAR_0x8004, ITEM_ROCKY_HELMET
    SetVar VAR_0x8006, MOVE_ROOST
    SetVar VAR_0x8007, MOVE_IRON_DEFENSE
    SetVar VAR_0x8008, MOVE_PROTECT
    SetVar VAR_0x8009, MOVE_SPLASH
    GoTo TestKit_GiveItemPair

/* The Absorb Bulb: Chansey against a wild Psyduck that knows only Water
   Gun. The first Water Gun into the Chansey holding it brings "The Absorb
   Bulb raised CHANSEY's Sp. Atk!", and the bulb is gone. */
TestKit_ItemAbsorbBulb:
    SetVar VAR_0x8000, SPECIES_PSYDUCK
    SetVar VAR_0x8001, ABILITY_NONE
    SetVar VAR_0x8002, MOVE_WATER_GUN
    SetVar VAR_0x8003, MOVE_NONE
    SetVar VAR_0x800A, SPECIES_CHANSEY
    SetVar VAR_0x800B, ABILITY_NONE
    SetVar VAR_0x8004, ITEM_ABSORB_BULB
    SetVar VAR_0x8006, MOVE_SOFTBOILED
    SetVar VAR_0x8007, MOVE_SPLASH
    SetVar VAR_0x8008, MOVE_PROTECT
    SetVar VAR_0x8009, MOVE_SEISMIC_TOSS
    GoTo TestKit_GiveItemPair

/* The Cell Battery: as the Absorb Bulb, for Attack, against a wild Pikachu
   that knows only Thunder Shock. */
TestKit_ItemCellBattery:
    SetVar VAR_0x8000, SPECIES_PIKACHU
    SetVar VAR_0x8001, ABILITY_NONE
    SetVar VAR_0x8002, MOVE_THUNDER_SHOCK
    SetVar VAR_0x8003, MOVE_NONE
    SetVar VAR_0x800A, SPECIES_CHANSEY
    SetVar VAR_0x800B, ABILITY_NONE
    SetVar VAR_0x8004, ITEM_CELL_BATTERY
    SetVar VAR_0x8006, MOVE_SOFTBOILED
    SetVar VAR_0x8007, MOVE_SPLASH
    SetVar VAR_0x8008, MOVE_PROTECT
    SetVar VAR_0x8009, MOVE_SEISMIC_TOSS
    GoTo TestKit_GiveItemPair

/* The Weakness Policy: Snorlax against a wild Machamp that knows only
   Karate Chop, super effective on it. The first chop into the Snorlax
   holding it sharply raises its Attack and then its Sp. Atk, and the
   policy is gone. */
TestKit_ItemWeaknessPolicy:
    SetVar VAR_0x8000, SPECIES_MACHAMP
    SetVar VAR_0x8001, ABILITY_NONE
    SetVar VAR_0x8002, MOVE_KARATE_CHOP
    SetVar VAR_0x8003, MOVE_NONE
    SetVar VAR_0x800A, SPECIES_SNORLAX
    SetVar VAR_0x800B, ABILITY_NONE
    SetVar VAR_0x8004, ITEM_WEAKNESS_POLICY
    SetVar VAR_0x8006, MOVE_REST
    SetVar VAR_0x8007, MOVE_BODY_SLAM
    SetVar VAR_0x8008, MOVE_PROTECT
    SetVar VAR_0x8009, MOVE_SPLASH
    GoTo TestKit_GiveItemPair

/* The Air Balloon: Snorlax against a wild Dugtrio that knows Earthquake and
   Scratch. Switched in, the Snorlax holding it "floats in the air with its
   Air Balloon!", Earthquake does not affect it, and the first Scratch
   pops the balloon; after that Earthquake hits it. */
TestKit_ItemAirBalloon:
    SetVar VAR_0x8000, SPECIES_DUGTRIO
    SetVar VAR_0x8001, ABILITY_NONE
    SetVar VAR_0x8002, MOVE_EARTHQUAKE
    SetVar VAR_0x8003, MOVE_SCRATCH
    SetVar VAR_0x800A, SPECIES_SNORLAX
    SetVar VAR_0x800B, ABILITY_NONE
    SetVar VAR_0x8004, ITEM_AIR_BALLOON
    SetVar VAR_0x8006, MOVE_REST
    SetVar VAR_0x8007, MOVE_BODY_SLAM
    SetVar VAR_0x8008, MOVE_PROTECT
    SetVar VAR_0x8009, MOVE_SPLASH
    GoTo TestKit_GiveItemPair

/* The Binding Band: Mew against a wild Chansey that knows only Splash. After
   the banded Mew's Wrap, Chansey loses a sixth of its HP at the end of
   each turn; after the other Mew's, an eighth. */
TestKit_ItemBindingBand:
    SetVar VAR_0x8000, SPECIES_CHANSEY
    SetVar VAR_0x8001, ABILITY_NONE
    SetVar VAR_0x8002, MOVE_SPLASH
    SetVar VAR_0x8003, MOVE_NONE
    SetVar VAR_0x800A, SPECIES_MEW
    SetVar VAR_0x800B, ABILITY_NONE
    SetVar VAR_0x8004, ITEM_BINDING_BAND
    SetVar VAR_0x8006, MOVE_WRAP
    SetVar VAR_0x8007, MOVE_SPLASH
    SetVar VAR_0x8008, MOVE_RECOVER
    SetVar VAR_0x8009, MOVE_PROTECT
    GoTo TestKit_GiveItemPair

/* The Loaded Dice: Mew against a wild Chansey that knows only Splash. From
   the Mew holding them, Bullet Seed always hits four or five times,
   Population Bomb four to ten times, and Triple Axel never misses a later
   kick; from the other, Bullet Seed mostly hits two or three times. */
TestKit_ItemLoadedDice:
    SetVar VAR_0x8000, SPECIES_CHANSEY
    SetVar VAR_0x8001, ABILITY_NONE
    SetVar VAR_0x8002, MOVE_SPLASH
    SetVar VAR_0x8003, MOVE_NONE
    SetVar VAR_0x800A, SPECIES_MEW
    SetVar VAR_0x800B, ABILITY_NONE
    SetVar VAR_0x8004, ITEM_LOADED_DICE
    SetVar VAR_0x8006, MOVE_BULLET_SEED
    SetVar VAR_0x8007, MOVE_TRIPLE_AXEL
    SetVar VAR_0x8008, MOVE_POPULATION_BOMB
    SetVar VAR_0x8009, MOVE_RECOVER
    GoTo TestKit_GiveItemPair

/* The Mirror Herb: Mew against a wild Chansey that knows only Swords Dance.
   After Chansey's first Swords Dance, the Mew holding the herb copies it
   ("MEW's Mirror Herb copied its foe's stat changes!"), its Tackle does
   about twice as much, and the herb is gone; the other Mew gets nothing. */
TestKit_ItemMirrorHerb:
    SetVar VAR_0x8000, SPECIES_CHANSEY
    SetVar VAR_0x8001, ABILITY_NONE
    SetVar VAR_0x8002, MOVE_SWORDS_DANCE
    SetVar VAR_0x8003, MOVE_NONE
    SetVar VAR_0x800A, SPECIES_MEW
    SetVar VAR_0x800B, ABILITY_NONE
    SetVar VAR_0x8004, ITEM_MIRROR_HERB
    SetVar VAR_0x8006, MOVE_TACKLE
    SetVar VAR_0x8007, MOVE_SPLASH
    SetVar VAR_0x8008, MOVE_RECOVER
    SetVar VAR_0x8009, MOVE_PROTECT
    GoTo TestKit_GiveItemPair

/* The Eject Button: Chansey against a wild Rattata that knows only Tackle.
   When a Tackle hits the Chansey holding it, "CHANSEY is switched out
   with the Eject Button!" and the party list opens for a replacement. */
TestKit_ItemEjectButton:
    SetVar VAR_0x8000, SPECIES_RATTATA
    SetVar VAR_0x8001, ABILITY_NONE
    SetVar VAR_0x8002, MOVE_TACKLE
    SetVar VAR_0x8003, MOVE_NONE
    SetVar VAR_0x800A, SPECIES_CHANSEY
    SetVar VAR_0x800B, ABILITY_NONE
    SetVar VAR_0x8004, ITEM_EJECT_BUTTON
    SetVar VAR_0x8006, MOVE_SOFTBOILED
    SetVar VAR_0x8007, MOVE_SPLASH
    SetVar VAR_0x8008, MOVE_PROTECT
    SetVar VAR_0x8009, MOVE_SEISMIC_TOSS
    GoTo TestKit_GiveItemPair

/* The Red Card: Chansey against a wild Rattata that knows only Tackle.
   When a Tackle hits the Chansey holding it, "CHANSEY held up its Red
   Card against the wild RATTATA!" and, as with Dragon Tail against a wild
   Pokemon, the battle ends. Sending a trainer's Pokemon away needs a
   trainer battle, which the kit does not have. */
TestKit_ItemRedCard:
    SetVar VAR_0x8000, SPECIES_RATTATA
    SetVar VAR_0x8001, ABILITY_NONE
    SetVar VAR_0x8002, MOVE_TACKLE
    SetVar VAR_0x8003, MOVE_NONE
    SetVar VAR_0x800A, SPECIES_CHANSEY
    SetVar VAR_0x800B, ABILITY_NONE
    SetVar VAR_0x8004, ITEM_RED_CARD
    SetVar VAR_0x8006, MOVE_SOFTBOILED
    SetVar VAR_0x8007, MOVE_SPLASH
    SetVar VAR_0x8008, MOVE_PROTECT
    SetVar VAR_0x8009, MOVE_SEISMIC_TOSS
    GoTo TestKit_GiveItemPair

/* The Pixie Plate: two Arceus with Judgment, Moonblast, Recover and Splash,
   the first holding the plate and set to its Fairy form (as giving it the
   plate from the Bag would), the second holding nothing, against a wild
   Dragonite that knows only Dragon Claw. The first is pink in its summary
   and in battle, its types read Fairy, its Judgment is a Fairy move that is
   super effective on Dragonite, and Dragon Claw does not affect it; the
   second is a Normal Arceus whose Judgment is Normal. */
TestKit_ItemPixiePlate:
    GetPartyCount VAR_0x8005
    GoToIfGe VAR_0x8005, 5, TestKit_PartyFull
    SetVar VAR_0x8000, SPECIES_DRAGONITE
    SetVar VAR_0x8001, ABILITY_NONE
    SetVar VAR_0x8002, MOVE_DRAGON_CLAW
    SetVar VAR_0x8003, MOVE_NONE
    SetVar VAR_0x800A, SPECIES_ARCEUS
    SetVar VAR_0x800B, ABILITY_NONE
    SetVar VAR_0x8004, ITEM_PIXIE_PLATE
    SetVar VAR_0x8006, MOVE_JUDGMENT
    SetVar VAR_0x8007, MOVE_MOONBLAST
    SetVar VAR_0x8008, MOVE_RECOVER
    SetVar VAR_0x8009, MOVE_SPLASH
    GivePokemon VAR_0x800A, 50, VAR_0x8004, VAR_RESULT
    Call TestKit_SetPairMoves
    TestKitSetPartyMonForm VAR_0x8005, 18    /* ARCEUS_FORM_FAIRY */
    AddVar VAR_0x8005, 1
    GivePokemon VAR_0x800A, 50, ITEM_NONE, VAR_RESULT
    Call TestKit_SetPairMoves
    BufferItemName 0, VAR_0x8004
    Message TestKit_Text_ItemPair
    GoTo TestKit_AbilityFoe

/* The Roseli Berry: Dragonite against a wild Clefable that knows only
   Moonblast, super effective on it. The first Moonblast into the Dragonite
   holding it brings "The Roseli Berry weakened Moonblast's power!" and
   does about half as much as into the other; the berry is gone. */
TestKit_ItemRoseliBerry:
    SetVar VAR_0x8000, SPECIES_CLEFABLE
    SetVar VAR_0x8001, ABILITY_NONE
    SetVar VAR_0x8002, MOVE_MOONBLAST
    SetVar VAR_0x8003, MOVE_NONE
    SetVar VAR_0x800A, SPECIES_DRAGONITE
    SetVar VAR_0x800B, ABILITY_NONE
    SetVar VAR_0x8004, ITEM_ROSELI_BERRY
    SetVar VAR_0x8006, MOVE_ROOST
    SetVar VAR_0x8007, MOVE_SPLASH
    SetVar VAR_0x8008, MOVE_PROTECT
    SetVar VAR_0x8009, MOVE_DRAGON_CLAW
    GoTo TestKit_GiveItemPair

/* The Ability Capsule and Patch: a Machamp and a Ditto, with two Ability
   Capsules and the Ability Patch in the Bag. A Capsule used on the Machamp
   swaps it between Guts and No Guard ("Machamp's Ability changed to ...!")
   and the second swaps it back; the Patch then makes it Steadfast, after
   which a Capsule has no effect. Both have no effect on the Ditto, whose
   species has one ordinary ability; the Patch would make it Imposter, so
   try the Capsule first. The summary shows the ability after each. Each
   asks first ("Change MACHAMP's Ability to ...?"); No leaves the item in
   the Bag and goes back to choosing a Pokemon. */
TestKit_ItemAbilities:
    GetPartyCount VAR_0x8005
    GoToIfGe VAR_0x8005, 5, TestKit_PartyFull
    GivePokemon SPECIES_MACHAMP, 50, ITEM_NONE, VAR_RESULT
    GivePokemon SPECIES_DITTO, 50, ITEM_NONE, VAR_RESULT
    AddItem ITEM_ABILITY_CAPSULE, 2, VAR_RESULT
    AddItem ITEM_ABILITY_PATCH, 1, VAR_RESULT
    Message TestKit_Text_ItemAbilities
    GoTo TestKit_WaitAndClose

/* The Mints and Bottle Caps: a Machamp, with two Adamant Mints, a Modest
   and a Serious Mint, two Bottle Caps and a Gold Bottle Cap in the Bag. Note its
   nature and its stats, then its IVs (R on the stat page). An Adamant Mint
   ("The Adamant Mint changed how MACHAMP's stats grow!") raises Attack and
   lowers Sp. Atk by a tenth against its base nature, and its summary still
   shows its own nature; a second Adamant Mint has no effect. A Bottle Cap
   asks for a stat and puts that IV at 31 in the viewer, raising the stat;
   on a stat already at 31 it has no effect and stays in the Bag. The Gold
   Bottle Cap does all six at once. The Machamp is Lv. 20, below the later
   games' level 50, since the caps work at any level (Ian, 2026-09-27). */
TestKit_ItemMintsCaps:
    GetPartyCount VAR_0x8005
    GoToIfGe VAR_0x8005, 6, TestKit_PartyFull
    GivePokemon SPECIES_MACHAMP, 20, ITEM_NONE, VAR_RESULT
    AddItem ITEM_ADAMANT_MINT, 2, VAR_RESULT
    AddItem ITEM_MODEST_MINT, 1, VAR_RESULT
    AddItem ITEM_SERIOUS_MINT, 1, VAR_RESULT
    AddItem ITEM_BOTTLE_CAP, 2, VAR_RESULT
    AddItem ITEM_GOLD_BOTTLE_CAP, 1, VAR_RESULT
    Message TestKit_Text_ItemMintsCaps
    GoTo TestKit_WaitAndClose

/* The TM mechanism, which now allows more than 92 TMs but has none past
   TM92 yet, so this checks that nothing moved: TM92, HM08, TM01 and HM01
   are added in that order. In the TM Case they sort as No. 01, No. 92,
   HM 01, HM 08, each with its own move (Focus Punch, Trick Room, Cut, Rock
   Climb), and using one shows ABLE and NOT ABLE beside the party as
   before. A move taught by an HM still cannot be forgotten. */
TestKit_ItemTMs:
    AddItem ITEM_TM92, 1, VAR_RESULT
    AddItem ITEM_HM08, 1, VAR_RESULT
    AddItem ITEM_TM01, 1, VAR_RESULT
    AddItem ITEM_HM01, 1, VAR_RESULT
    Message TestKit_Text_ItemTMs
    GoTo TestKit_WaitAndClose

TestKit_PartyFull:
    Message TestKit_Text_PartyFull
    GoTo TestKit_WaitAndClose

/* Element 8's level caps: puts the player in any split, including an earlier
   one, which RaiseLevelCap never does, so the cap can be checked at each
   value and put back. A new game starts in Roark's split, cap 16. */
TestKit_LevelCaps:
    Message TestKit_Text_WhichCap
    InitLocalTextListMenu 1, 1, 0, VAR_0x8004
    AddListMenuEntry TestKit_Text_MenuCapRoark, LEVEL_CAP_SPLIT_ROARK
    AddListMenuEntry TestKit_Text_MenuCapGardenia, LEVEL_CAP_SPLIT_GARDENIA
    AddListMenuEntry TestKit_Text_MenuCapFantina, LEVEL_CAP_SPLIT_FANTINA
    AddListMenuEntry TestKit_Text_MenuCapMaylene, LEVEL_CAP_SPLIT_MAYLENE
    AddListMenuEntry TestKit_Text_MenuCapWake, LEVEL_CAP_SPLIT_WAKE
    AddListMenuEntry TestKit_Text_MenuCapByron, LEVEL_CAP_SPLIT_BYRON
    AddListMenuEntry TestKit_Text_MenuCapCandice, LEVEL_CAP_SPLIT_CANDICE
    AddListMenuEntry TestKit_Text_MenuCapHQ, LEVEL_CAP_SPLIT_HQ
    AddListMenuEntry TestKit_Text_MenuCapGalactic, LEVEL_CAP_SPLIT_GALACTIC
    AddListMenuEntry TestKit_Text_MenuCapVolkner, LEVEL_CAP_SPLIT_VOLKNER
    AddListMenuEntry TestKit_Text_MenuCapBarry, LEVEL_CAP_SPLIT_BARRY
    AddListMenuEntry TestKit_Text_MenuCapLeague, LEVEL_CAP_SPLIT_LEAGUE
    AddListMenuEntry TestKit_Text_MenuCapNone, LEVEL_CAP_SPLIT_NONE
    ShowListMenu
    GoToIfGe VAR_0x8004, LEVEL_CAP_SPLIT_COUNT, TestKit_Close
    SetVar VAR_LEVEL_CAP_SPLIT, VAR_0x8004
    Message TestKit_Text_LevelCapSet
    GoTo TestKit_WaitAndClose

TestKit_WaitAndClose:
    WaitButton
TestKit_Close:
    CloseMessage
    ReleaseAll
    End
#endif

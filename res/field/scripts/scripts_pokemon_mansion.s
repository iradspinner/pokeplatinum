#include "macros/scrcmd.inc"
#include "res/text/bank/pokemon_mansion.h"
#include "res/field/events/events_pokemon_mansion.h"


    ScriptEntry PokemonMansion_OnTransition
    ScriptEntry PokemonMansion_MaidOffice
    ScriptEntry PokemonMansion_MaidTrophyGarden
    ScriptEntry PokemonMansion_MaidWest
    ScriptEntry PokemonMansion_MaidFarEast
    ScriptEntry PokemonMansion_MaidEast
    ScriptEntryEnd

PokemonMansion_OnTransition:
    SetFlag FLAG_FIRST_ARRIVAL_POKEMON_MANSION
    SetFlag FLAG_HIDE_POKEMON_MANSION_FIVE_MAID_KNOCKOUT_MAID
    SetFlag FLAG_HIDE_POKEMON_MANSION_FIVE_MAID_KNOCKOUT_BOSS
    GoToIfUnset FLAG_DAILY_SET_FIVE_MAID_KNOCKOUT_TURN_TARGET, PokemonMansion_InitFiveMaidKnockoutChallenge
    End

@ Oxide (Ian, 2026-10-31): the knockout has no turn target and no Rich Boy
@ Liam any more. The daily flag, still named for vanilla's turn target, now
@ only marks that today's challenge is open: each new day clears Lady
@ Celeste's trainer flag, so the five maids and Celeste can be fought again.
PokemonMansion_InitFiveMaidKnockoutChallenge:
    SetFlag FLAG_DAILY_SET_FIVE_MAID_KNOCKOUT_TURN_TARGET
    ClearTrainerFlag TRAINER_LADY_CELESTE
    End

PokemonMansion_MaidOffice:
    PlaySE SE_CONFIRM_sseq_3
    LockAll
    FacePlayer
    Message PokemonMansion_Text_MrBacklotOffice
    WaitButton
    CloseMessage
    ApplyMovement LOCALID_MAID_OFFICE, PokemonMansion_Movement_MaidOfficeFaceSouth
    WaitMovement
    ReleaseAll
    End

PokemonMansion_MaidTrophyGarden:
    PlaySE SE_CONFIRM_sseq_3
    LockAll
    FacePlayer
    Message PokemonMansion_Text_ThisWayTrophyGarden
    WaitButton
    CloseMessage
    ApplyMovement LOCALID_MAID_TROPHY_GARDEN, PokemonMansion_Movement_MaidTrophyGardenFaceSouth
    WaitMovement
    ReleaseAll
    End

PokemonMansion_MaidWest:
    PlaySE SE_CONFIRM_sseq_3
    LockAll
    FacePlayer
    GoToIfDefeated TRAINER_LADY_CELESTE, PokemonMansion_ChallengeDoneToday
    GetPlayerDir VAR_RESULT
    GoToIfEq VAR_RESULT, DIR_NORTH, PokemonMansion_GetInPositionNorth
    GoToIfEq VAR_RESULT, DIR_SOUTH, PokemonMansion_GetInPositionSouth
    GoTo PokemonMansion_FiveMaidKnockoutChallenge
    End

PokemonMansion_GetInPositionNorth:
    ApplyMovement LOCALID_MAID_FAR_WEST, PokemonMansion_Movement_MaidFarWestWalkOnSpotEast
    ApplyMovement LOCALID_PLAYER, PokemonMansion_Movement_PlayerGetInPositionNorth
    WaitMovement
    GoTo PokemonMansion_FiveMaidKnockoutChallenge
    End

PokemonMansion_GetInPositionSouth:
    ApplyMovement LOCALID_MAID_FAR_WEST, PokemonMansion_Movement_MaidFarWestWalkOnSpotEast2
    ApplyMovement LOCALID_PLAYER, PokemonMansion_Movement_PlayerGetInPositionSouth
    WaitMovement
    GoTo PokemonMansion_FiveMaidKnockoutChallenge
    End

@ Oxide (Ian, 2026-10-31): the five maids and then Lady Celeste, every time,
@ back to back with no healing. Celeste's trainer flag is set only when she
@ is beaten, so it means "cleared today", and a cleared challenge waits for
@ the next day.
PokemonMansion_FiveMaidKnockoutChallenge:
    CallIfUnset FLAG_STARTED_FIVE_MAID_KNOCKOUT_CHALLENGE, PokemonMansion_ExplainChallenge
    SetFlag FLAG_STARTED_FIVE_MAID_KNOCKOUT_CHALLENGE
    Message PokemonMansion_Text_TryTheChallenge
    ShowYesNoMenu VAR_RESULT
    GoToIfEq VAR_RESULT, MENU_NO, PokemonMansion_DontDoChallenge
    Message PokemonMansion_Text_OurFirstMaid
    CloseMessage
    ApplyMovement LOCALID_MAID_FAR_WEST, PokemonMansion_Movement_MaidFarWestMoveAside
    WaitMovement
    ClearFlag FLAG_HIDE_POKEMON_MANSION_FIVE_MAID_KNOCKOUT_MAID
    AddObject LOCALID_FIVE_MAID_KNOCKOUT_MAID
    ApplyMovement LOCALID_FIVE_MAID_KNOCKOUT_MAID, PokemonMansion_Movement_KnockoutTrainerEnter
    WaitMovement
    Message PokemonMansion_Text_Maid1Intro
    CloseMessage
    StartTrainerBattle TRAINER_MAID_BELINDA
    CheckWonBattle VAR_RESULT
    GoToIfEq VAR_RESULT, FALSE, PokemonMansion_BlackOut
    Message PokemonMansion_Text_Maid1Defeat
    CloseMessage
    ApplyMovement LOCALID_FIVE_MAID_KNOCKOUT_MAID, PokemonMansion_Movement_KnockoutTrainerLeave
    WaitMovement
    ApplyMovement LOCALID_FIVE_MAID_KNOCKOUT_MAID, PokemonMansion_Movement_KnockoutTrainerEnter
    WaitMovement
    Message PokemonMansion_Text_Maid2Intro
    CloseMessage
    StartTrainerBattle TRAINER_MAID_SOPHIE
    CheckWonBattle VAR_RESULT
    GoToIfEq VAR_RESULT, FALSE, PokemonMansion_BlackOut
    Message PokemonMansion_Text_Maid2Defeat
    CloseMessage
    ApplyMovement LOCALID_FIVE_MAID_KNOCKOUT_MAID, PokemonMansion_Movement_KnockoutTrainerLeave
    WaitMovement
    ApplyMovement LOCALID_FIVE_MAID_KNOCKOUT_MAID, PokemonMansion_Movement_KnockoutTrainerEnter
    WaitMovement
    Message PokemonMansion_Text_Maid3Intro
    CloseMessage
    StartTrainerBattle TRAINER_MAID_EMILY
    CheckWonBattle VAR_RESULT
    GoToIfEq VAR_RESULT, FALSE, PokemonMansion_BlackOut
    Message PokemonMansion_Text_Maid3Defeat
    CloseMessage
    ApplyMovement LOCALID_FIVE_MAID_KNOCKOUT_MAID, PokemonMansion_Movement_KnockoutTrainerLeave
    WaitMovement
    ApplyMovement LOCALID_FIVE_MAID_KNOCKOUT_MAID, PokemonMansion_Movement_KnockoutTrainerEnter
    WaitMovement
    Message PokemonMansion_Text_Maid4Intro
    CloseMessage
    StartTrainerBattle TRAINER_MAID_ELENA
    CheckWonBattle VAR_RESULT
    GoToIfEq VAR_RESULT, FALSE, PokemonMansion_BlackOut
    Message PokemonMansion_Text_Maid4Defeat
    CloseMessage
    ApplyMovement LOCALID_FIVE_MAID_KNOCKOUT_MAID, PokemonMansion_Movement_KnockoutTrainerLeave
    WaitMovement
    ApplyMovement LOCALID_MAID_FAR_WEST, PokemonMansion_Movement_MaidFarWestMoveBackInPlace
    WaitMovement
    Message PokemonMansion_Text_DefeatedFourMaids
    CloseMessage
    ApplyMovement LOCALID_MAID_FAR_WEST, PokemonMansion_Movement_MaidFarWestMoveAside
    WaitMovement
    ApplyMovement LOCALID_FIVE_MAID_KNOCKOUT_MAID, PokemonMansion_Movement_KnockoutTrainerEnter
    WaitMovement
    Message PokemonMansion_Text_Maid5Intro
    CloseMessage
    StartTrainerBattle TRAINER_MAID_CLARE
    CheckWonBattle VAR_RESULT
    GoToIfEq VAR_RESULT, FALSE, PokemonMansion_BlackOut
    Message PokemonMansion_Text_Maid5Defeat
    CloseMessage
    ApplyMovement LOCALID_FIVE_MAID_KNOCKOUT_MAID, PokemonMansion_Movement_KnockoutTrainerLeave
    WaitMovement
    RemoveObject LOCALID_FIVE_MAID_KNOCKOUT_MAID
    ApplyMovement LOCALID_MAID_FAR_WEST, PokemonMansion_Movement_MaidFarWestMoveBackInPlace
    WaitMovement
    @ The boss object takes its sprite from this var, as vanilla's random pick set it.
    SetVar VAR_OBJ_GFX_ID_0, OBJ_EVENT_GFX_LADY
    Message PokemonMansion_Text_SweptNowCeleste
    CloseMessage
    ApplyMovement LOCALID_MAID_FAR_WEST, PokemonMansion_Movement_MaidFarWestMoveAside
    WaitMovement
    ClearFlag FLAG_HIDE_POKEMON_MANSION_FIVE_MAID_KNOCKOUT_BOSS
    AddObject LOCALID_FIVE_MAID_KNOCKOUT_BOSS
    ApplyMovement LOCALID_FIVE_MAID_KNOCKOUT_BOSS, PokemonMansion_Movement_KnockoutTrainerEnter
    WaitMovement
    Message PokemonMansion_Text_CelesteIntro
    CloseMessage
    StartTrainerBattle TRAINER_LADY_CELESTE
    CheckWonBattle VAR_RESULT
    GoToIfEq VAR_RESULT, FALSE, PokemonMansion_BlackOut
    SetTrainerFlag TRAINER_LADY_CELESTE
    Message PokemonMansion_Text_CelesteDefeat
    @ The prize, straight after the first win (Ian's rule for trainer
    @ rewards): the game's one Ability Capsule, under the spare flag the
    @ reward tool hands out next, which Pastoria's Capsule ball used before.
    GoToIfSet FLAG_UNUSED_0x03CC, PokemonMansion_CelesteLeaves
    Message PokemonMansion_Text_CelesteGift
    Call PokemonMansion_GivePrize
PokemonMansion_CelesteLeaves:
    Message PokemonMansion_Text_CelesteLeaves
    CloseMessage
    ApplyMovement LOCALID_FIVE_MAID_KNOCKOUT_BOSS, PokemonMansion_Movement_KnockoutTrainerLeave
    WaitMovement
    RemoveObject LOCALID_FIVE_MAID_KNOCKOUT_BOSS
    ApplyMovement LOCALID_MAID_FAR_WEST, PokemonMansion_Movement_MaidFarWestMoveBackInPlace
    WaitMovement
    Message PokemonMansion_Text_TriumphedOverCeleste
    GoTo PokemonMansion_VisitAgainTomorrow
    End

@ After a clear the maid only asks the player back tomorrow, unless a full
@ Bag refused the Capsule, which she then hands over.
PokemonMansion_ChallengeDoneToday:
    GoToIfSet FLAG_UNUSED_0x03CC, PokemonMansion_VisitAgainTomorrow
    Message PokemonMansion_Text_KeptYourGift
    Call PokemonMansion_GivePrize
    GoTo PokemonMansion_VisitAgainTomorrow
    End

PokemonMansion_GivePrize:
    SetVar VAR_0x8004, ITEM_ABILITY_CAPSULE
    SetVar VAR_0x8005, 1
    GoToIfCannotFitItem VAR_0x8004, VAR_0x8005, VAR_RESULT, PokemonMansion_PrizeBagIsFull
    Common_GiveItemQuantity
    SetFlag FLAG_UNUSED_0x03CC
    Return

PokemonMansion_PrizeBagIsFull:
    Common_MessageBagIsFull
    Return

PokemonMansion_VisitAgainTomorrow:
    Message PokemonMansion_Text_VisitAgainTomorrow
    GoTo PokemonMansion_MaidChallengeEnd
    End

    .balign 4, 0
PokemonMansion_Movement_MaidFarWestWalkOnSpotEast:
    WalkOnSpotNormalEast
    EndMovement

    .balign 4, 0
PokemonMansion_Movement_MaidFarWestWalkOnSpotEast2:
    WalkOnSpotNormalEast
    EndMovement

    .balign 4, 0
PokemonMansion_Movement_MaidFarWestMoveAside:
    WalkNormalNorth
    WalkOnSpotNormalSouth
    EndMovement

    .balign 4, 0
PokemonMansion_Movement_MaidFarWestMoveBackInPlace:
    WalkNormalSouth
    WalkOnSpotNormalEast
    EndMovement

    .balign 4, 0
PokemonMansion_Movement_KnockoutTrainerLeave:
    WalkOnSpotNormalWest
    SetInvisible
    EndMovement

    .balign 4, 0
PokemonMansion_Movement_KnockoutTrainerEnter:
    SetVisible
    WalkOnSpotNormalEast
    EndMovement

    .balign 4, 0
PokemonMansion_Movement_PlayerGetInPositionNorth:
    WalkNormalEast
    WalkNormalNorth
    WalkOnSpotNormalWest
    EndMovement

    .balign 4, 0
PokemonMansion_Movement_PlayerGetInPositionSouth:
    WalkNormalEast
    WalkNormalSouth
    WalkOnSpotNormalWest
    EndMovement

PokemonMansion_ExplainChallenge:
    Message PokemonMansion_Text_ChallengeFiveMaids
    Return

PokemonMansion_DontDoChallenge:
    Message PokemonMansion_Text_HowDisappointing
    GoTo PokemonMansion_MaidChallengeEnd
    End

PokemonMansion_MaidChallengeEnd:
    WaitButton
    CloseMessage
    ReleaseAll
    End

PokemonMansion_BlackOut:
    BlackOutFromBattle
    ReleaseAll
    End

PokemonMansion_MaidFarEast:
    PlaySE SE_CONFIRM_sseq_3
    LockAll
    FacePlayer
    Message PokemonMansion_Text_StrictlyOffLimits
    WaitButton
    CloseMessage
    ApplyMovement LOCALID_MAID_FAR_EAST, PokemonMansion_Movement_MaidFarEastFaceWest
    WaitMovement
    ReleaseAll
    End

    .balign 4, 0
PokemonMansion_Movement_MaidOfficeFaceSouth:
    FaceSouth
    EndMovement

    .balign 4, 0
PokemonMansion_Movement_MaidTrophyGardenFaceSouth:
    FaceSouth
    EndMovement

PokemonMansion_Movement_Unused:
    FaceEast
    EndMovement

    .balign 4, 0
PokemonMansion_Movement_MaidFarEastFaceWest:
    FaceWest
    EndMovement

PokemonMansion_MaidEast:
    NPCMessage PokemonMansion_Text_BookTugsAttention
    End

    .balign 4, 0

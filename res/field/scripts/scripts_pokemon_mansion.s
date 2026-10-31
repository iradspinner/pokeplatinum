#include "macros/scrcmd.inc"
#include "res/text/bank/pokemon_mansion.h"
#include "res/field/events/events_pokemon_mansion.h"


    ScriptEntry PokemonMansion_OnTransition
    ScriptEntry PokemonMansion_MaidOffice
    ScriptEntry PokemonMansion_MaidTrophyGarden
    ScriptEntry PokemonMansion_MaidWest
    ScriptEntry PokemonMansion_MaidFarEast
    ScriptEntry PokemonMansion_MaidEast
    ScriptEntry PokemonMansion_Darach
    ScriptEntry PokemonMansion_Caitlin
    ScriptEntry PokemonMansion_DarachGate
    ScriptEntryEnd

PokemonMansion_OnTransition:
    SetFlag FLAG_FIRST_ARRIVAL_POKEMON_MANSION
    SetFlag FLAG_HIDE_POKEMON_MANSION_FIVE_MAID_KNOCKOUT_MAID
    SetFlag FLAG_HIDE_POKEMON_MANSION_FIVE_MAID_KNOCKOUT_BOSS
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
    GoToIfDefeated TRAINER_LADY_CELESTE, PokemonMansion_ChallengeCleared
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

@ Oxide (Ian, 2026-10-31): the five maids and then Lady Celeste, back to
@ back with no healing, with no turn target and no Rich Boy Liam. Celeste's
@ trainer flag is set only when she is beaten, so it means "cleared", and
@ nothing clears it again: there is no daily repeat. A loss leaves it unset,
@ so the challenge can be tried again.
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
    GoTo PokemonMansion_ChallengeClosed
    End

@ The challenge closes after the first clear (Ian, 2026-10-31): the maid no
@ longer offers it, and only hands over the Capsule if a full Bag refused it.
PokemonMansion_ChallengeCleared:
    GoToIfSet FLAG_UNUSED_0x03CC, PokemonMansion_ChallengeClosed
    Message PokemonMansion_Text_KeptYourGift
    Call PokemonMansion_GivePrize
    GoTo PokemonMansion_ChallengeClosed
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

PokemonMansion_ChallengeClosed:
    Message PokemonMansion_Text_ChallengeClosed
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

@ Oxide (Ian, 2026-09-27 and 2026-10-31): Darach and Caitlin, an optional
@ boss of Wake's split, stand at the top of the entrance hall's aisle. The
@ trigger across the aisle (the events' coord event) holds the player until
@ they are beaten, so the office, the maids and the Trophy Garden open only
@ on the win. Their fight is a double battle as one trainer. Straight after
@ the win Darach hands over the Manaphy egg, which the office maid offered
@ in the base ROM; FLAG_UNK_0x0A65 stays its received flag, so a save that
@ took the egg there gets no second one.
PokemonMansion_DarachGate:
    LockAll
    ApplyMovement LOCALID_DARACH, PokemonMansion_Movement_DarachNotice
    WaitMovement
    SetVar VAR_0x8007, 1
    GoTo PokemonMansion_DarachChallenge
    End

PokemonMansion_Darach:
    PlaySE SE_CONFIRM_sseq_3
    LockAll
    FacePlayer
    GoToIfDefeated TRAINER_DUMMY_008, PokemonMansion_DarachBeaten
    SetVar VAR_0x8007, 0
    GoTo PokemonMansion_DarachChallenge
    End

@ VAR_0x8007 is 1 when the trigger started this, so a refusal walks the
@ player back down the aisle, off the trigger.
PokemonMansion_DarachChallenge:
    Message PokemonMansion_Text_DarachIntro
    ShowYesNoMenu VAR_RESULT
    GoToIfEq VAR_RESULT, MENU_NO, PokemonMansion_DarachDeclined
    CheckHasTwoAliveMons VAR_RESULT
    GoToIfEq VAR_RESULT, FALSE, PokemonMansion_DarachNeedTwo
    Message PokemonMansion_Text_DarachBegin
    CloseMessage
    StartTrainerBattle TRAINER_DUMMY_008
    CheckWonBattle VAR_RESULT
    GoToIfEq VAR_RESULT, FALSE, PokemonMansion_BlackOut
    SetTrainerFlag TRAINER_DUMMY_008
    SetVar VAR_POKEMON_MANSION_DARACH_STATE, 1
    Message PokemonMansion_Text_DarachWin
    GoToIfSet FLAG_UNK_0x0A65, PokemonMansion_DarachEnd
    Message PokemonMansion_Text_DarachEgg
    GoTo PokemonMansion_DarachGiveEgg
    End

PokemonMansion_DarachNeedTwo:
    Message PokemonMansion_Text_DarachNeedTwo
    GoTo PokemonMansion_DarachSendBack
    End

PokemonMansion_DarachDeclined:
    Message PokemonMansion_Text_DarachDeclined
PokemonMansion_DarachSendBack:
    WaitButton
    CloseMessage
    GoToIfEq VAR_0x8007, 0, PokemonMansion_DarachRelease
    ApplyMovement LOCALID_PLAYER, PokemonMansion_Movement_PlayerStepBack
    WaitMovement
PokemonMansion_DarachRelease:
    ReleaseAll
    End

@ Once beaten, Darach still holds the egg if a full party refused it.
PokemonMansion_DarachBeaten:
    GoToIfSet FLAG_UNK_0x0A65, PokemonMansion_DarachBeatenLine
    Message PokemonMansion_Text_DarachKeptEgg
    GoTo PokemonMansion_DarachGiveEgg
    End

PokemonMansion_DarachBeatenLine:
    Message PokemonMansion_Text_DarachBeaten
    GoTo PokemonMansion_DarachEnd
    End

PokemonMansion_DarachGiveEgg:
    GetPartyCount VAR_RESULT
    GoToIfEq VAR_RESULT, 6, PokemonMansion_DarachPartyFull
    PlayFanfare SEQ_FANFA4_sseq
    WaitFanfare
    GiveEgg SPECIES_MANAPHY, 8
    SetFlag FLAG_UNK_0x0A65
    BufferPlayerName 0
    Message PokemonMansion_Text_PlayerReceivedEgg
    Message PokemonMansion_Text_DarachCareForEgg
    GoTo PokemonMansion_DarachEnd
    End

PokemonMansion_DarachPartyFull:
    Message PokemonMansion_Text_DarachPartyFull
PokemonMansion_DarachEnd:
    WaitButton
    CloseMessage
    ReleaseAll
    End

PokemonMansion_Caitlin:
    PlaySE SE_CONFIRM_sseq_3
    LockAll
    FacePlayer
    GoToIfDefeated TRAINER_DUMMY_008, PokemonMansion_CaitlinBeaten
    Message PokemonMansion_Text_CaitlinBefore
    GoTo PokemonMansion_DarachEnd
    End

PokemonMansion_CaitlinBeaten:
    Message PokemonMansion_Text_CaitlinBeaten
    GoTo PokemonMansion_DarachEnd
    End

    .balign 4, 0
PokemonMansion_Movement_DarachNotice:
    EmoteExclamationMark
    EndMovement

    .balign 4, 0
PokemonMansion_Movement_PlayerStepBack:
    WalkNormalSouth
    EndMovement

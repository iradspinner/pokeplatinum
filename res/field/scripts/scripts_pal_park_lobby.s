#include "macros/scrcmd.inc"
#include "res/text/bank/menu_entries.h"
#include "res/text/bank/pal_park_lobby.h"
#include "res/field/events/events_pal_park_lobby.h"
#include "constants/pokemon.h"
#include "constants/versions.h"


    ScriptEntry PalParkLobby_OnTransition
    ScriptEntry PalParkLobby_Worker
    ScriptEntry PalParkLobby_OnFrame_TallyScore
    ScriptEntry PalParkLobby_Record_Unused
    ScriptEntry PalParkLobby_Daughter
    ScriptEntry PalParkLobby_Dad
    ScriptEntry PalParkLobby_ShowWatcherBoy
    ScriptEntry PalParkLobby_ComplaintsLady
    ScriptEntry PalParkLobby_RecordGuy
    ScriptEntry PalParkLobby_OnFrame_ProfOak
    ScriptEntry PalParkLobby_PoketchAppLady
    ScriptEntry PalParkLobby_OnFrame_ExitPalPark
    ScriptEntry PalParkLobby_GBASlotGiftLady
    ScriptEntry PalParkLobby_OnFrame_GalacticDouble
    ScriptEntry PalParkLobby_Argenta
    ScriptEntryEnd

PalParkLobby_OnTransition:
    ClearFlag FLAG_ALT_MUSIC_PAL_PARK
    SetFlag FLAG_FIRST_ARRIVAL_POKE_PARK_FRONT_GATE
    @ Platinum Oxide (Ian, 2026-10-31): the counterpart and the two officers of
    @ the partner double load hidden; the scene adds them as they walk in. The
    @ counterpart wears the sprite of the player's opposite gender. Their hide
    @ flag is one vanilla never used, kept under its pret name so the reward
    @ placer counts it as taken (place_rewards.py, SpareFlags).
    SetFlag FLAG_UNUSED_0x054F
    GetPlayerGender VAR_MAP_LOCAL_0x01
    CallIfEq VAR_MAP_LOCAL_0x01, GENDER_MALE, PalParkLobby_SetCounterpartGraphicsDawn
    CallIfEq VAR_MAP_LOCAL_0x01, GENDER_FEMALE, PalParkLobby_SetCounterpartGraphicsLucas
    @ Argenta, the Hall Matron, stands in the north gallery only once the
    @ partner double is won (the lobby's state 2). Her hide flag is a map-local
    @ one, which the game clears on every map change, so it costs the save
    @ nothing: it is set here, before the objects load, while the double is
    @ still to come.
    CallIfLt VAR_PAL_PARK_LOBBY_STATE, 2, PalParkLobby_HideArgenta
    GoToIfNe VAR_PAL_PARK_STATE, 0, PalParkLobby_SetWorkerPosAndDir
    End

PalParkLobby_HideArgenta:
    SetFlag FLAG_MAP_LOCAL_0x01
    Return

PalParkLobby_SetCounterpartGraphicsDawn:
    SetVar VAR_OBJ_GFX_ID_0, OBJ_EVENT_GFX_PLAYER_F
    Return

PalParkLobby_SetCounterpartGraphicsLucas:
    SetVar VAR_OBJ_GFX_ID_0, OBJ_EVENT_GFX_PLAYER_M
    Return

PalParkLobby_SetWorkerPosAndDir:
    SetObjectEventPos LOCALID_WORKER, 8, 9
    SetObjectEventDir LOCALID_WORKER, DIR_WEST
    End

PalParkLobby_BufferRecord:
    GoToIfEq VAR_CATCHING_SHOW_RECORD, 2000, PalParkLobby_BufferRivalRecord
    BufferPlayerName 1
    BufferNumber 2, VAR_CATCHING_SHOW_RECORD
    Return

PalParkLobby_BufferRivalRecord:
    BufferRivalName 1
    BufferNumber 2, VAR_CATCHING_SHOW_RECORD
    Return

PalParkLobby_Worker:
    PlaySE SE_CONFIRM_sseq_3
    LockAll
    FacePlayer
    GetPlayerGender VAR_RESULT
    GoToIfEq VAR_RESULT, GENDER_MALE, PalParkLobby_Worker_PlayerMale
    GoTo PalParkLobby_Worker_PlayerFemale

PalParkLobby_Worker_PlayerMale:
    GoToIfSet FLAG_TALKED_TO_PAL_PARK_LOBBY_RECEPTIONIST, PalParkLobby_Worker_Greeting_PlayerMale
    SetFlag FLAG_TALKED_TO_PAL_PARK_LOBBY_RECEPTIONIST
    BufferPlayerName 0
    Message PalParkLobby_Text_WelcomeToPalPark_PlayerMale
    ShowYesNoMenu VAR_RESULT
    GoToIfEq VAR_RESULT, MENU_YES, PalParkLobby_Manual_FirstTime
    GoToIfEq VAR_RESULT, MENU_NO, PalParkLobby_Worker_DontParticipate
    End

PalParkLobby_Worker_PlayerFemale:
    GoToIfSet FLAG_TALKED_TO_PAL_PARK_LOBBY_RECEPTIONIST, PalParkLobby_Worker_Greeting_PlayerFemale
    SetFlag FLAG_TALKED_TO_PAL_PARK_LOBBY_RECEPTIONIST
    BufferPlayerName 0
    Message PalParkLobby_Text_WelcomeToPalPark_PlayerFemale
    ShowYesNoMenu VAR_RESULT
    GoToIfEq VAR_RESULT, MENU_YES, PalParkLobby_Manual_FirstTime
    GoToIfEq VAR_RESULT, MENU_NO, PalParkLobby_Worker_DontParticipate
    End

PalParkLobby_Manual_FirstTime:
    Message PalParkLobby_Text_LetMeExplainPalPark
    GoTo PalParkLobby_OpenManualMenu

PalParkLobby_Manual_BasicRules:
    Message PalParkLobby_Text_Manual_BasicRules
    GoTo PalParkLobby_OpenManualMenu

PalParkLobby_Manual_CatchingShow:
    Message PalParkLobby_Text_Manual_CatchingShow
    GoTo PalParkLobby_OpenManualMenu

PalParkLobby_Manual_StockingPokemon:
    Message PalParkLobby_Text_Manual_StockingPokemon
    GoTo PalParkLobby_OpenManualMenu

PalParkLobby_OpenManualMenu:
    InitGlobalTextMenu 1, 1, 0, VAR_RESULT
    AddMenuEntryImm MenuEntries_Text_PalPark_BasicRules, 0
    AddMenuEntryImm MenuEntries_Text_PalPark_CatchingShow, 1
    AddMenuEntryImm MenuEntries_Text_PalPark_StockingPokemon, 2
    AddMenuEntryImm MenuEntries_Text_PalPark_Understood, 4
    ShowMenu
    GoToIfEq VAR_RESULT, 0, PalParkLobby_Manual_BasicRules
    GoToIfEq VAR_RESULT, 1, PalParkLobby_Manual_CatchingShow
    GoToIfEq VAR_RESULT, 2, PalParkLobby_Manual_StockingPokemon
    GoTo PalParkLobby_Worker_AskParticipateFromManual

PalParkLobby_Worker_AskParticipateFromManual:
    Message PalParkLobby_Text_TakePartInCatchingShow
    ShowYesNoMenu VAR_RESULT
    GoToIfEq VAR_RESULT, MENU_NO, PalParkLobby_Worker_DontParticipate
PalParkLobby_Worker_CheckIfCanParticipate:
    SetVar VAR_RESULT, 0
    GetPCBoxesFreeSlotCount VAR_RESULT
    GoToIfLt VAR_RESULT, CATCHING_SHOW_MONS, PalParkLobby_Worker_PCBoxesFilled
    SetVar VAR_RESULT, 0
    GoToIfNotEnoughMonForCatchingShow PalParkLobby_Worker_NotEnoughPokemonMigrated
    GetPlayerGender VAR_RESULT
    GoToIfEq VAR_RESULT, GENDER_MALE, PalParkLobby_Worker_GiveParkBalls_PlayerMale
    GoTo PalParkLobby_Worker_GiveParkBalls_PlayerFemale

PalParkLobby_Worker_DontParticipate:
    Message PalParkLobby_Text_AwwThatsTooBad
    WaitButton
    CloseMessage
    ReleaseAll
    End

PalParkLobby_Worker_Greeting_PlayerMale:
    BufferPlayerName 0
    Message PalParkLobby_Text_Greeting_PlayerMale
    GoTo PalParkLobby_Worker_OpenCatchingShowMenu

PalParkLobby_Worker_Greeting_PlayerFemale:
    BufferPlayerName 0
    Message PalParkLobby_Text_Greeting_PlayerFemale
    GoTo PalParkLobby_Worker_OpenCatchingShowMenu

PalParkLobby_Worker_OpenCatchingShowMenu:
    InitGlobalTextMenu 1, 1, 0, VAR_RESULT
    AddMenuEntryImm MenuEntries_Text_PalPark_Enter, 0
    AddMenuEntryImm MenuEntries_Text_PalPark_Info, 1
    AddMenuEntryImm MenuEntries_Text_PalPark_Exit, 2
    ShowMenu
    GoToIfEq VAR_RESULT, 0, PalParkLobby_Worker_CheckIfCanParticipate
    GoToIfEq VAR_RESULT, 1, PalParkLobby_Manual
    GoToIfEq VAR_RESULT, 2, PalParkLobby_Worker_DontParticipate
    GoTo PalParkLobby_Worker_DontParticipate

PalParkLobby_Worker_GiveParkBalls_PlayerMale:
    Call PalParkLobby_BufferRecord
    BufferPlayerName 0
    Message PalParkLobby_Text_HereParkBalls_PlayerMale
    CloseMessage
    GoTo PalParkLobby_WalkInAndWarp

PalParkLobby_Worker_GiveParkBalls_PlayerFemale:
    Call PalParkLobby_BufferRecord
    BufferPlayerName 0
    Message PalParkLobby_Text_HereParkBalls_PlayerFemale
    CloseMessage
    GoTo PalParkLobby_WalkInAndWarp

PalParkLobby_WalkInAndWarp:
    ApplyMovement LOCALID_WORKER, PalParkLobby_Movement_WorkerMoveAside
    WaitMovement
    ApplyMovement LOCALID_PLAYER, PalParkLobby_Movement_PlayerEnterPalPark
    WaitMovement
    PlaySE SEQ_SE_DP_KAIDAN2_sseq
    FadeScreenOut
    WaitFadeScreen
    Warp MAP_HEADER_PAL_PARK, 24, 47, DIR_NORTH
    FadeScreenIn
    WaitFadeScreen
    ReleaseAll
    End

PalParkLobby_Worker_NotEnoughPokemonMigrated:
    Message PalParkLobby_Text_NotEnoughPokemonMigrated
    WaitButton
    CloseMessage
    ReleaseAll
    End

PalParkLobby_Manual:
    Message PalParkLobby_Text_IllReadManual
    GoTo PalParkLobby_OpenManualMenu

PalParkLobby_Worker_PCBoxesFilled:
    Message PalParkLobby_Text_PCBoxesFilled
    WaitButton
    CloseMessage
    ReleaseAll
    End

    .balign 4, 0
PalParkLobby_Movement_WorkerMoveAside:
    WalkOnSpotFastNorth
    WalkNormalNorth 2
    WalkNormalEast
    WalkOnSpotFastWest
    EndMovement

    .balign 4, 0
PalParkLobby_Movement_PlayerEnterPalPark:
    WalkNormalNorth 5
    SetInvisible
    EndMovement

PalParkLobby_OnFrame_ExitPalPark:
    LockAll
    SetVar VAR_PAL_PARK_STATE, 0
    ApplyMovement LOCALID_PLAYER, PalParkLobby_Movement_PlayerExitPalPark
    WaitMovement
    ApplyMovement LOCALID_WORKER, PalParkLobby_Movement_WorkerMoveBack
    WaitMovement
    ReleaseAll
    End

PalParkLobby_OnFrame_TallyScore:
    LockAll
    SetVar VAR_PAL_PARK_STATE, 0
    ApplyMovement LOCALID_PLAYER, PalParkLobby_Movement_PlayerWalkToWorker
    WaitMovement
    CalcCatchingShowPoints CATCHING_SHOW_CATCHING_POINTS, VAR_RESULT
    BufferNumber 0, VAR_RESULT
    CalcCatchingShowPoints CATCHING_SHOW_TIME_POINTS, VAR_RESULT
    BufferNumber 1, VAR_RESULT
    CalcCatchingShowPoints CATCHING_SHOW_TYPE_POINTS, VAR_RESULT
    BufferNumber 2, VAR_RESULT
    CalcCatchingShowPoints CATCHING_SHOW_TOTAL_POINTS, VAR_RESULT
    BufferNumber 3, VAR_RESULT
    Message PalParkLobby_Text_AllSixPokemonCaught
    CalcCatchingShowPoints CATCHING_SHOW_TOTAL_POINTS, VAR_RESULT
    GoToIfGt VAR_RESULT, VAR_CATCHING_SHOW_RECORD, PalParkLobby_Worker_RecordBroken
    Message PalParkLobby_Text_DecentRecord
    Call PalParkLobby_Worker_SetPrize
    GoTo PalParkLobby_Worker_AskStoreCaughtMon

PalParkLobby_Worker_RecordBroken:
    Message PalParkLobby_Text_OutstandingRecord
    Call PalParkLobby_Worker_SetPrize
    CalcCatchingShowPoints CATCHING_SHOW_TOTAL_POINTS, VAR_CATCHING_SHOW_RECORD
    GoTo PalParkLobby_Worker_AskStoreCaughtMon

PalParkLobby_Worker_AskStoreCaughtMon:
    Message PalParkLobby_Text_AskStoreCaughtMon
    ShowYesNoMenu VAR_RESULT
    GoToIfEq VAR_RESULT, MENU_YES, PalParkLobby_Worker_StoreCaughtMon
    Message PalParkLobby_Text_AskRedoCatchingShow
    ShowYesNoMenu VAR_RESULT
    GoToIfEq VAR_RESULT, MENU_YES, PalParkLobby_Worker_DontStoreCaughtMon
    GoTo PalParkLobby_Worker_AskStoreCaughtMon

PalParkLobby_Worker_DontStoreCaughtMon:
    Message PalParkLobby_Text_GoForBetterScore
    WaitABPress
    CloseMessage
    GoTo PalParkLobby_Worker_End

PalParkLobby_Worker_StoreCaughtMon:
    MoveCatchingShowMonsToPCBoxes
    Message PalParkLobby_Text_PokemonHaveBeenBoxed
    Message PalParkLobby_Text_ComeSeeUsAgain
    WaitABPress
    CloseMessage
    GoTo PalParkLobby_Worker_End

PalParkLobby_Worker_End:
    ApplyMovement LOCALID_PLAYER, PalParkLobby_Movement_PlayerLeaveCounter
    WaitMovement
    ApplyMovement LOCALID_WORKER, PalParkLobby_Movement_WorkerMoveBack
    WaitMovement
    ReleaseAll
    End

    .balign 4, 0
PalParkLobby_Movement_WorkerMoveBack:
    WalkNormalWest
    WalkNormalSouth 2
    EndMovement

    .balign 4, 0
PalParkLobby_Movement_PlayerExitPalPark:
    WalkNormalSouth 5
    EndMovement

    .balign 4, 0
PalParkLobby_Movement_PlayerWalkToWorker:
    WalkNormalSouth 2
    WalkOnSpotFastEast
    EndMovement

    .balign 4, 0
PalParkLobby_Movement_PlayerLeaveCounter:
    WalkNormalSouth 4
    EndMovement

PalParkLobby_Record_Unused:
    NPCMessage PalParkLobby_Text_CurrentRecordHolder
    End

PalParkLobby_Daughter:
    PlaySE SE_CONFIRM_sseq_3
    LockAll
    FacePlayer
    BufferPlayerName 0
    GoToIfEq VAR_RESULT, 2, PalParkLobby_Daughter_IHopeYouDoBetter
    GoToIfEq VAR_RESULT, 1, PalParkLobby_Daughter_YourCatchingShowWasFantastic
    GoTo PalParkLobby_Daughter_CameToSeeCatchingShow

PalParkLobby_Daughter_CameToSeeCatchingShow:
    Message PalParkLobby_Text_CameToSeeCatchingShow
    WaitButton
    CloseMessage
    ReleaseAll
    End

PalParkLobby_Daughter_YourCatchingShowWasFantastic:
    Message PalParkLobby_Text_YourCatchingShowWasFantastic
    WaitButton
    CloseMessage
    ReleaseAll
    End

PalParkLobby_Daughter_IHopeYouDoBetter:
    Message PalParkLobby_Text_IHopeYouDoBetter
    WaitButton
    CloseMessage
    ReleaseAll
    End

PalParkLobby_Dad:
    BufferPlayerName 0
    NPCMessage PalParkLobby_Text_DaughterIsBigFan
    End

PalParkLobby_ShowWatcherBoy:
    NPCMessage PalParkLobby_Text_RareAndExoticPokemon
    End

PalParkLobby_ComplaintsLady:
    NPCMessage PalParkLobby_Text_RarePokemonTakeLonger
    End

PalParkLobby_RecordGuy:
    Call PalParkLobby_BufferRecord
    NPCMessage PalParkLobby_Text_CurrentRecordHolder
    End

PalParkLobby_OnFrame_ProfOak:
    LockAll
    ClearFlag FLAG_HIDE_ETERNA_CITY_SOUTH_HOUSE_PROF_OAK
    SetVar VAR_CATCHING_SHOW_RECORD, 2000
    ApplyMovement LOCALID_PROF_OAK, PalParkLobby_Movement_ProfOakNoticePlayer
    WaitMovement
    GetPlayerGender VAR_MAP_LOCAL_0x00
    BufferPlayerName 0
    GoToIfEq VAR_MAP_LOCAL_0x00, GENDER_MALE, PalParkLobby_ThisIsPalPark_PlayerMale
    GoTo PalParkLobby_ThisIsPalPark_PlayerFemale

PalParkLobby_ThisIsPalPark_PlayerMale:
    Message PalParkLobby_Text_Oak_ThisIsPalPark_PlayerMale
    GoTo PalParkLobby_PokemonFromAroundTheCountry

PalParkLobby_ThisIsPalPark_PlayerFemale:
    Message PalParkLobby_Text_Oak_ThisIsPalPark_PlayerFemale
    GoTo PalParkLobby_PokemonFromAroundTheCountry

PalParkLobby_PokemonFromAroundTheCountry:
    Message PalParkLobby_Text_Oak_PokemonFromAroundTheCountry
    CloseMessage
    ApplyMovement LOCALID_PROF_OAK, PalParkLobby_Movement_ProfOakExclamationMark
    WaitMovement
    Message PalParkLobby_Text_Oak_GiftTrainerCounterApp
    SetVar VAR_0x8004, POKETCH_APPID_TRAINERCOUNTER
    Common_GivePoketchApp
    Message PalParkLobby_Text_Oak_InEternaForSomeTime
    CloseMessage
    WaitTime 15, VAR_RESULT
    ApplyMovement LOCALID_PLAYER, PalParkLobby_Movement_PlayerMoveAside
    WaitMovement
    ApplyMovement LOCALID_PROF_OAK, PalParkLobby_Movement_ProfOakLeave
    WaitMovement
    PlaySE SEQ_SE_DP_KAIDAN2_sseq
    RemoveObject LOCALID_PROF_OAK
    WaitSE SEQ_SE_DP_KAIDAN2_sseq
    SetVar VAR_PAL_PARK_LOBBY_STATE, 1
    ReleaseAll
    End

    .balign 4, 0
PalParkLobby_Movement_ProfOakNoticePlayer:
    EmoteExclamationMark
    Delay8
    WalkNormalSouth 3
    EndMovement

    .balign 4, 0
PalParkLobby_Movement_ProfOakExclamationMark:
    EmoteExclamationMark
    Delay8
    EndMovement

    .balign 4, 0
PalParkLobby_Movement_ProfOakLeave:
    WalkNormalSouth
    WalkOnSpotNormalSouth
    EndMovement

    .balign 4, 0
PalParkLobby_Movement_PlayerMoveAside:
    WalkNormalEast
    WalkOnSpotNormalWest
    EndMovement

@ Platinum Oxide (Ian, 2026-10-31): Pal Park is required in Byron's split. Once
@ Oak's first-entry scene is over (the lobby's state 1), Lucas or Dawn walks
@ in, two Galactic officers follow, and the player and the counterpart fight
@ them in a tag battle. The win sets both officers' trainer flags, which
@ Barry on Canalave's bridge waits for, and moves the lobby to state 2.
PalParkLobby_OnFrame_GalacticDouble:
    LockAll
    @ The scene runs from the door: the player has just come in (7, 19) or has
    @ just stepped aside for Oak (8, 19). Anywhere else, as in a save that used
    @ the park before this scene existed, the player is put back at the door
    @ and the scene starts from there.
    GetPlayerMapPos VAR_0x8004, VAR_0x8005
    GoToIfNe VAR_0x8005, 19, PalParkLobby_GalacticDouble_ReturnToDoor
    GoToIfEq VAR_0x8004, 7, PalParkLobby_GalacticDouble_FromDoor
    GoToIfEq VAR_0x8004, 8, PalParkLobby_GalacticDouble_FromBesideDoor
    GoTo PalParkLobby_GalacticDouble_ReturnToDoor

PalParkLobby_GalacticDouble_ReturnToDoor:
    FadeScreenOut
    WaitFadeScreen
    Warp MAP_HEADER_PAL_PARK_LOBBY, 7, 19, DIR_NORTH
    FadeScreenIn
    WaitFadeScreen
    ReleaseAll
    End

PalParkLobby_GalacticDouble_FromDoor:
    ApplyMovement LOCALID_PLAYER, PalParkLobby_Movement_PlayerWalkInFromDoor
    WaitMovement
    GoTo PalParkLobby_GalacticDouble_Start

PalParkLobby_GalacticDouble_FromBesideDoor:
    ApplyMovement LOCALID_PLAYER, PalParkLobby_Movement_PlayerWalkInFromBesideDoor
    WaitMovement
    GoTo PalParkLobby_GalacticDouble_Start

@ The player stands at (7, 17). The counterpart comes in by the door and
@ stops at (6, 17), beside the player, leaving the door's column clear.
PalParkLobby_GalacticDouble_Start:
    BufferCounterpartName 0
    BufferPlayerName 1
    Message PalParkLobby_Text_CounterpartWaitUp
    CloseMessage
    ApplyMovement LOCALID_PLAYER, PalParkLobby_Movement_FaceSouth
    WaitMovement
    ClearFlag FLAG_UNUSED_0x054F
    SetObjectEventPos LOCALID_COUNTERPART, 7, 19
    AddObject LOCALID_COUNTERPART
    PlaySE SEQ_SE_DP_KAIDAN2_sseq
    ApplyMovement LOCALID_COUNTERPART, PalParkLobby_Movement_CounterpartWalkIn
    WaitMovement
    ApplyMovement LOCALID_PLAYER, PalParkLobby_Movement_FaceWest
    WaitMovement
    BufferCounterpartName 0
    Message PalParkLobby_Text_CounterpartPokemonFromEverywhere
    CloseMessage
    @ Officers Phobos and Deimos, the pair from Jubilife, come in by the
    @ door: Phobos stops below the player at (7, 18), Deimos below the
    @ counterpart at (6, 18).
    ClearFlag FLAG_UNUSED_0x054F
    SetObjectEventPos LOCALID_PHOBOS, 7, 19
    AddObject LOCALID_PHOBOS
    PlaySE SEQ_SE_DP_KAIDAN2_sseq
    ApplyMovement LOCALID_PHOBOS, PalParkLobby_Movement_PhobosWalkIn
    ApplyMovement LOCALID_PLAYER, PalParkLobby_Movement_NoticeSouth
    ApplyMovement LOCALID_COUNTERPART, PalParkLobby_Movement_NoticeSouth
    WaitMovement
    ClearFlag FLAG_UNUSED_0x054F
    SetObjectEventPos LOCALID_DEIMOS, 7, 19
    AddObject LOCALID_DEIMOS
    ApplyMovement LOCALID_DEIMOS, PalParkLobby_Movement_DeimosWalkIn
    WaitMovement
    Message PalParkLobby_Text_PhobosPokemonFromOtherRegions
    Message PalParkLobby_Text_DeimosStepAside
    BufferCounterpartName 0
    BufferPlayerName 1
    Message PalParkLobby_Text_CounterpartBattleTogether
    CloseMessage
    Call PalParkLobby_GalacticDouble_Battle
    CheckWonBattle VAR_RESULT
    GoToIfEq VAR_RESULT, FALSE, PalParkLobby_GalacticDouble_BlackOut
    SetTrainerFlag TRAINER_DUMMY_009
    SetTrainerFlag TRAINER_DUMMY_050
    Message PalParkLobby_Text_OfficersFallBack
    CloseMessage
    ApplyMovement LOCALID_PHOBOS, PalParkLobby_Movement_PhobosLeave
    WaitMovement
    PlaySE SEQ_SE_DP_KAIDAN2_sseq
    RemoveObject LOCALID_PHOBOS
    ApplyMovement LOCALID_DEIMOS, PalParkLobby_Movement_DeimosLeave
    WaitMovement
    PlaySE SEQ_SE_DP_KAIDAN2_sseq
    RemoveObject LOCALID_DEIMOS
    ApplyMovement LOCALID_PLAYER, PalParkLobby_Movement_FaceWest
    ApplyMovement LOCALID_COUNTERPART, PalParkLobby_Movement_FaceEast
    WaitMovement
    BufferCounterpartName 0
    BufferPlayerName 1
    Message PalParkLobby_Text_CounterpartParkIsSafe
    CloseMessage
    ApplyMovement LOCALID_COUNTERPART, PalParkLobby_Movement_CounterpartLeave
    WaitMovement
    PlaySE SEQ_SE_DP_KAIDAN2_sseq
    RemoveObject LOCALID_COUNTERPART
    WaitSE SEQ_SE_DP_KAIDAN2_sseq
    SetVar VAR_PAL_PARK_LOBBY_STATE, 2
    @ The double is won, so Argenta takes her place in the north gallery
    @ straight away, without waiting for the player to leave and come back.
    ClearFlag FLAG_MAP_LOCAL_0x01
    AddObject LOCALID_HALL_MATRON_ARGENTA
    ReleaseAll
    End

PalParkLobby_GalacticDouble_BlackOut:
    BlackOutFromBattle
    ReleaseAll
    End

@ The partner is the counterpart of the player's opposite gender, on the
@ team for the player's starter, as at Veilstone: the Scorbunny player's
@ files are the _chimchar ones (Oxide's fire starter, Ian, 2026-09-21).
@ Each StartTagBattle names its partner, so the census sees every team.
PalParkLobby_GalacticDouble_Battle:
    GetPlayerGender VAR_RESULT
    GoToIfEq VAR_RESULT, GENDER_FEMALE, PalParkLobby_GalacticDouble_BattleLucas
    GetPlayerStarterSpecies VAR_RESULT
    GoToIfEq VAR_RESULT, SPECIES_SCORBUNNY, PalParkLobby_GalacticDouble_BattleDawnChimchar
    GoToIfEq VAR_RESULT, SPECIES_PIPLUP, PalParkLobby_GalacticDouble_BattleDawnPiplup
    StartTagBattle TRAINER_DUMMY_062, TRAINER_DUMMY_009, TRAINER_DUMMY_050
    Return

PalParkLobby_GalacticDouble_BattleDawnChimchar:
    StartTagBattle TRAINER_DUMMY_063, TRAINER_DUMMY_009, TRAINER_DUMMY_050
    Return

PalParkLobby_GalacticDouble_BattleDawnPiplup:
    StartTagBattle TRAINER_DUMMY_064, TRAINER_DUMMY_009, TRAINER_DUMMY_050
    Return

PalParkLobby_GalacticDouble_BattleLucas:
    GetPlayerStarterSpecies VAR_RESULT
    GoToIfEq VAR_RESULT, SPECIES_SCORBUNNY, PalParkLobby_GalacticDouble_BattleLucasChimchar
    GoToIfEq VAR_RESULT, SPECIES_PIPLUP, PalParkLobby_GalacticDouble_BattleLucasPiplup
    StartTagBattle TRAINER_DUMMY_051, TRAINER_DUMMY_009, TRAINER_DUMMY_050
    Return

PalParkLobby_GalacticDouble_BattleLucasChimchar:
    StartTagBattle TRAINER_DUMMY_052, TRAINER_DUMMY_009, TRAINER_DUMMY_050
    Return

PalParkLobby_GalacticDouble_BattleLucasPiplup:
    StartTagBattle TRAINER_DUMMY_054, TRAINER_DUMMY_009, TRAINER_DUMMY_050
    Return

    .balign 4, 0
PalParkLobby_Movement_PlayerWalkInFromDoor:
    WalkNormalNorth 2
    EndMovement

    .balign 4, 0
PalParkLobby_Movement_PlayerWalkInFromBesideDoor:
    WalkNormalNorth 2
    WalkNormalWest
    EndMovement

    .balign 4, 0
PalParkLobby_Movement_FaceSouth:
    WalkOnSpotNormalSouth
    EndMovement

    .balign 4, 0
PalParkLobby_Movement_FaceWest:
    WalkOnSpotNormalWest
    EndMovement

    .balign 4, 0
PalParkLobby_Movement_FaceEast:
    WalkOnSpotNormalEast
    EndMovement

    .balign 4, 0
PalParkLobby_Movement_NoticeSouth:
    WalkOnSpotNormalSouth
    EmoteExclamationMark
    Delay8
    EndMovement

    .balign 4, 0
PalParkLobby_Movement_CounterpartWalkIn:
    WalkNormalNorth
    WalkNormalWest
    WalkNormalNorth
    WalkOnSpotNormalEast
    EndMovement

    .balign 4, 0
PalParkLobby_Movement_PhobosWalkIn:
    WalkNormalNorth
    EndMovement

    .balign 4, 0
PalParkLobby_Movement_DeimosWalkIn:
    WalkNormalWest
    WalkNormalNorth
    EndMovement

    .balign 4, 0
PalParkLobby_Movement_PhobosLeave:
    WalkFastSouth
    EndMovement

    .balign 4, 0
PalParkLobby_Movement_DeimosLeave:
    WalkFastSouth
    WalkFastEast
    EndMovement

    .balign 4, 0
PalParkLobby_Movement_CounterpartLeave:
    WalkNormalSouth
    WalkNormalEast
    WalkNormalSouth
    EndMovement

@ Platinum Oxide (Ian, 2026-11-01): Argenta, the Hall Matron, an optional
@ Frontier Brain in Barry 5's stretch of Byron's split. She stands at the
@ west end of the north gallery once the partner double is won, and fights
@ only when spoken to. She asks first, since a loss ends an Oxide run, as the
@ other Brains do. Her win gives a bundle of items once, under
@ FLAG_UNUSED_0x054D: until it is set, a player who has beaten her is offered
@ the bundle again whenever they speak to her. The bundle is the item pass's
@ proposal, which waits on Ian (docs/oxide/argenta-place.md).
PalParkLobby_Argenta:
    PlaySE SE_CONFIRM_sseq_3
    LockAll
    FacePlayer
    GoToIfDefeated TRAINER_DUMMY_086, PalParkLobby_ArgentaBeaten
    Message PalParkLobby_Text_ArgentaIntro
    ShowYesNoMenu VAR_RESULT
    GoToIfEq VAR_RESULT, MENU_NO, PalParkLobby_ArgentaDeclined
    Message PalParkLobby_Text_ArgentaBegin
    CloseMessage
    StartTrainerBattle TRAINER_DUMMY_086
    CheckWonBattle VAR_RESULT
    GoToIfEq VAR_RESULT, FALSE, PalParkLobby_ArgentaBlackOut
    SetTrainerFlag TRAINER_DUMMY_086
    Message PalParkLobby_Text_ArgentaWin
    GoTo PalParkLobby_ArgentaGiveBundle
    End

PalParkLobby_ArgentaDeclined:
    Message PalParkLobby_Text_ArgentaDeclined
    GoTo PalParkLobby_ArgentaEnd
    End

PalParkLobby_ArgentaBeaten:
    GoToIfSet FLAG_UNUSED_0x054D, PalParkLobby_ArgentaBeatenLine
    Message PalParkLobby_Text_ArgentaKeptBundle
    GoTo PalParkLobby_ArgentaGiveBundle
    End

PalParkLobby_ArgentaBeatenLine:
    Message PalParkLobby_Text_ArgentaBeaten
    GoTo PalParkLobby_ArgentaEnd
    End

@ Every item is checked for room before any is given, so the bundle arrives
@ whole or not at all. Each pocket holds one of every item the game has, so
@ only a stack of 999 could refuse one; the check is kept all the same.
PalParkLobby_ArgentaGiveBundle:
    GoToIfCannotFitItem ITEM_GOLD_BOTTLE_CAP, 1, VAR_RESULT, PalParkLobby_ArgentaBagIsFull
    GoToIfCannotFitItem ITEM_ADAMANT_MINT, 1, VAR_RESULT, PalParkLobby_ArgentaBagIsFull
    GoToIfCannotFitItem ITEM_MODEST_MINT, 1, VAR_RESULT, PalParkLobby_ArgentaBagIsFull
    GoToIfCannotFitItem ITEM_JOLLY_MINT, 1, VAR_RESULT, PalParkLobby_ArgentaBagIsFull
    GoToIfCannotFitItem ITEM_TIMID_MINT, 1, VAR_RESULT, PalParkLobby_ArgentaBagIsFull
    SetVar VAR_0x8004, ITEM_GOLD_BOTTLE_CAP
    SetVar VAR_0x8005, 1
    Common_GiveItemQuantity
    SetVar VAR_0x8004, ITEM_ADAMANT_MINT
    SetVar VAR_0x8005, 1
    Common_GiveItemQuantity
    SetVar VAR_0x8004, ITEM_MODEST_MINT
    SetVar VAR_0x8005, 1
    Common_GiveItemQuantity
    SetVar VAR_0x8004, ITEM_JOLLY_MINT
    SetVar VAR_0x8005, 1
    Common_GiveItemQuantity
    SetVar VAR_0x8004, ITEM_TIMID_MINT
    SetVar VAR_0x8005, 1
    Common_GiveItemQuantity
    SetFlag FLAG_UNUSED_0x054D
    Message PalParkLobby_Text_ArgentaBeaten
    GoTo PalParkLobby_ArgentaEnd
    End

PalParkLobby_ArgentaBagIsFull:
    Message PalParkLobby_Text_ArgentaBagIsFull
PalParkLobby_ArgentaEnd:
    WaitButton
    CloseMessage
    ReleaseAll
    End

PalParkLobby_ArgentaBlackOut:
    BlackOutFromBattle
    ReleaseAll
    End

PalParkLobby_PoketchAppLady:
    PlaySE SE_CONFIRM_sseq_3
    LockAll
    FacePlayer
    GoToIfEq VAR_MAP_LOCAL_0x0A, 1, PalParkLobby_PoketchAppLady_JustReceivedKitchenTimer
    GoToIfEq VAR_MAP_LOCAL_0x0A, 2, PalParkLobby_PoketchAppLady_JustReceivedColorChanger
    CheckPoketchAppRegistered POKETCH_APPID_COLORCHANGER, VAR_RESULT
    GoToIfEq VAR_RESULT, 1, PalParkLobby_PoketchAppLady_ReceivedAllPoketchApps
    Message PalParkLobby_Text_PalParkIsScintillating
    Message PalParkLobby_Text_NeverSeenPokemon
    CheckPoketchAppRegistered POKETCH_APPID_KITCHENTIMER, VAR_RESULT
    GoToIfEq VAR_RESULT, 1, PalParkLobby_PoketchAppLady_CheckKecleon
    Message PalParkLobby_Text_PokemonThatJustEatsAndSleeps
    CheckPartyHasSpecies VAR_RESULT, SPECIES_SNORLAX
    GoToIfEq VAR_RESULT, 0, PalParkLobby_PoketchAppLady_DoesntHaveSpecies
    Message PalParkLobby_Text_ShowSnorlaxForApp
    SetVar VAR_0x8004, POKETCH_APPID_KITCHENTIMER
    Common_GivePoketchApp
    WaitButton
    SetVar VAR_MAP_LOCAL_0x0A, 1
    CloseMessage
    ReleaseAll
    End

PalParkLobby_PoketchAppLady_CheckKecleon:
    Message PalParkLobby_Text_PokemonThatChangesColor
    CheckPartyHasSpecies VAR_RESULT, SPECIES_KECLEON
    GoToIfEq VAR_RESULT, 0, PalParkLobby_PoketchAppLady_DoesntHaveSpecies
    Message PalParkLobby_Text_ShowKecleonForApp
    SetVar VAR_0x8004, POKETCH_APPID_COLORCHANGER
    Common_GivePoketchApp
    WaitButton
    SetVar VAR_MAP_LOCAL_0x0A, 2
    CloseMessage
    ReleaseAll
    End

PalParkLobby_PoketchAppLady_JustReceivedKitchenTimer:
    BufferPoketchAppName 0, POKETCH_APPID_KITCHENTIMER
    Message PalParkLobby_Text_KitchenTimerMakesYouCook
    WaitButton
    CloseMessage
    ReleaseAll
    End

PalParkLobby_PoketchAppLady_JustReceivedColorChanger:
    BufferPoketchAppName 0, POKETCH_APPID_COLORCHANGER
    Message PalParkLobby_Text_ColorsChangeMood
    WaitButton
    CloseMessage
    ReleaseAll
    End

PalParkLobby_PoketchAppLady_DoesntHaveSpecies:
    Message PalParkLobby_Text_WhatWasPokemonsName
    WaitButton
    CloseMessage
    ReleaseAll
    End

PalParkLobby_PoketchAppLady_ReceivedAllPoketchApps:
    Message PalParkLobby_Text_AreYouTakingChallenge
    WaitButton
    CloseMessage
    ReleaseAll
    End

PalParkLobby_GBASlotGiftLady:
    PlaySE SE_CONFIRM_sseq_3
    LockAll
    FacePlayer
    GoToIfEq VAR_MAP_LOCAL_0x09, 1, PalParkLobby_GBASlotGiftLady_JustReceivedGift
    GetGBACartridgeVersion VAR_RESULT
    GoToIfEq VAR_RESULT, VERSION_FIRERED, PalParkLobby_GBASlotGiftLady_FireRed
    GoToIfEq VAR_RESULT, VERSION_LEAFGREEN, PalParkLobby_GBASlotGiftLady_LeafGreen
    GoToIfEq VAR_RESULT, VERSION_SAPPHIRE, PalParkLobby_GBASlotGiftLady_Sapphire
    GoToIfEq VAR_RESULT, VERSION_RUBY, PalParkLobby_GBASlotGiftLady_Ruby
    GoToIfEq VAR_RESULT, VERSION_EMERALD, PalParkLobby_GBASlotGiftLady_Emerald
    GoTo PalParkLobby_GBASlotGiftLady_NoGBAGame
    End

PalParkLobby_GBASlotGiftLady_NoGBAGame:
    Message PalParkLobby_Text_ClashTrainerAndPokemon
    WaitButton
    CloseMessage
    ReleaseAll
    End

PalParkLobby_GBASlotGiftLady_JustReceivedGift:
    Message PalParkLobby_Text_CatchingShowsAndContests
    WaitButton
    CloseMessage
    ReleaseAll
    End

PalParkLobby_GBASlotGiftLady_FireRed:
    SetVar VAR_0x8004, ACCESSORY_CROWN
    SetVar VAR_0x8005, 1
    CanFitAccessory VAR_0x8004, VAR_0x8005, VAR_RESULT
    GoToIfEq VAR_RESULT, FALSE, PalParkLobby_GBASlotGiftLady_NoGBAGame
    Message PalParkLobby_Text_MustCrownYou
    GoTo PalParkLobby_GBASlotGiftLady_GiveAccessory
    End

PalParkLobby_GBASlotGiftLady_LeafGreen:
    SetVar VAR_0x8004, ACCESSORY_TIARA
    SetVar VAR_0x8005, 1
    CanFitAccessory VAR_0x8004, VAR_0x8005, VAR_RESULT
    GoToIfEq VAR_RESULT, FALSE, PalParkLobby_GBASlotGiftLady_NoGBAGame
    Message PalParkLobby_Text_CompelledToGiveTiara
    GoTo PalParkLobby_GBASlotGiftLady_GiveAccessory
    End

PalParkLobby_GBASlotGiftLady_Sapphire:
    SetVar VAR_0x8004, BACKDROP_SEAFLOOR
    CheckBackdrop VAR_0x8004, VAR_RESULT
    GoToIfEq VAR_RESULT, TRUE, PalParkLobby_GBASlotGiftLady_NoGBAGame
    Message PalParkLobby_Text_TakeThisSeafloorBackdrop
    GoTo PalParkLobby_GBASlotGiftLady_GiveBackdrop
    End

PalParkLobby_GBASlotGiftLady_Ruby:
    SetVar VAR_0x8004, BACKDROP_UNDERGROUND
    CheckBackdrop VAR_0x8004, VAR_RESULT
    GoToIfEq VAR_RESULT, TRUE, PalParkLobby_GBASlotGiftLady_NoGBAGame
    Message PalParkLobby_Text_TakeThisUndergroundBackdrop
    GoTo PalParkLobby_GBASlotGiftLady_GiveBackdrop
    End

PalParkLobby_GBASlotGiftLady_Emerald:
    SetVar VAR_0x8004, BACKDROP_SKY
    CheckBackdrop VAR_0x8004, VAR_RESULT
    GoToIfEq VAR_RESULT, TRUE, PalParkLobby_GBASlotGiftLady_NoGBAGame
    Message PalParkLobby_Text_TakeThisSkyBackdrop
    GoTo PalParkLobby_GBASlotGiftLady_GiveBackdrop
    End

PalParkLobby_GBASlotGiftLady_GiveAccessory:
    Common_GiveAccessoryWaitForConfirm
    SetVar VAR_MAP_LOCAL_0x09, 1
    CloseMessage
    ReleaseAll
    End

PalParkLobby_GBASlotGiftLady_GiveBackdrop:
    Common_ObtainContestBackdropWaitForConfirm
    SetVar VAR_MAP_LOCAL_0x09, 1
    CloseMessage
    ReleaseAll
    End

PalParkLobby_Worker_SetPrize:
    CalcCatchingShowPoints CATCHING_SHOW_TOTAL_POINTS, VAR_RESULT
    CallIfLt VAR_RESULT, 3000, PalParkLobby_Worker_SetPrize_Level1
    CallIfLt VAR_RESULT, 3300, PalParkLobby_Worker_SetPrize_Level2
    CallIfLt VAR_RESULT, 3500, PalParkLobby_Worker_SetPrize_Level3
    CallIfLt VAR_RESULT, 10000, PalParkLobby_Worker_SetPrize_Level4
    Return

PalParkLobby_Worker_SetPrize_Level1:
    GetRandom VAR_0x8006, 8
    CallIfEq VAR_0x8006, 0, PalParkLobby_SetPrize_CheriBerry
    CallIfEq VAR_0x8006, 1, PalParkLobby_SetPrize_ChestoBerry
    CallIfEq VAR_0x8006, 2, PalParkLobby_SetPrize_PechaBerry
    CallIfEq VAR_0x8006, 3, PalParkLobby_SetPrize_RawstBerry
    CallIfEq VAR_0x8006, 4, PalParkLobby_SetPrize_AspearBerry
    CallIfEq VAR_0x8006, 5, PalParkLobby_SetPrize_LeppaBerry
    CallIfEq VAR_0x8006, 6, PalParkLobby_SetPrize_OranBerry
    CallIfEq VAR_0x8006, 7, PalParkLobby_SetPrize_PersimBerry
    Call PalParkLobby_Worker_CheckIfCanGivePrize
    Return

PalParkLobby_Worker_SetPrize_Level2:
    GetRandom VAR_0x8006, 5
    CallIfEq VAR_0x8006, 0, PalParkLobby_SetPrize_FigyBerry
    CallIfEq VAR_0x8006, 1, PalParkLobby_SetPrize_WikiBerry
    CallIfEq VAR_0x8006, 2, PalParkLobby_SetPrize_MagoBerry
    CallIfEq VAR_0x8006, 3, PalParkLobby_SetPrize_AguavBerry
    CallIfEq VAR_0x8006, 4, PalParkLobby_SetPrize_IapapaBerry
    Call PalParkLobby_Worker_CheckIfCanGivePrize
    Return

PalParkLobby_Worker_SetPrize_Level3:
    GetRandom VAR_0x8006, 7
    CallIfEq VAR_0x8006, 0, PalParkLobby_SetPrize_RazzBerry
    CallIfEq VAR_0x8006, 1, PalParkLobby_SetPrize_BlukBerry
    CallIfEq VAR_0x8006, 2, PalParkLobby_SetPrize_NanabBerry
    CallIfEq VAR_0x8006, 3, PalParkLobby_SetPrize_WepearBerry
    CallIfEq VAR_0x8006, 4, PalParkLobby_SetPrize_PinapBerry
    CallIfEq VAR_0x8006, 5, PalParkLobby_SetPrize_LumBerry
    CallIfEq VAR_0x8006, 6, PalParkLobby_SetPrize_SitrusBerry
    Call PalParkLobby_Worker_CheckIfCanGivePrize
    Return

PalParkLobby_Worker_SetPrize_Level4:
    GetRandom VAR_0x8006, 6
    CallIfEq VAR_0x8006, 0, PalParkLobby_SetPrize_PomegBerry
    CallIfEq VAR_0x8006, 1, PalParkLobby_SetPrize_KelpsyBerry
    CallIfEq VAR_0x8006, 2, PalParkLobby_SetPrize_QualotBerry
    CallIfEq VAR_0x8006, 3, PalParkLobby_SetPrize_HondewBerry
    CallIfEq VAR_0x8006, 4, PalParkLobby_SetPrize_GrepaBerry
    CallIfEq VAR_0x8006, 5, PalParkLobby_SetPrize_TamatoBerry
    Call PalParkLobby_Worker_CheckIfCanGivePrize
    Return

PalParkLobby_Worker_CheckIfCanGivePrize:
    CanFitItem VAR_0x8006, 1, VAR_0x8007
    CallIfNe VAR_0x8007, 0, PalParkLobby_Worker_GivePrize
    SetVar VAR_RESULT, 0x2710
    Return

PalParkLobby_Worker_GivePrize:
    Message PalParkLobby_Text_TimeForPrize
    SetVar VAR_0x8004, VAR_0x8006
    SetVar VAR_0x8005, 1
    Common_GiveItemQuantity
    Return

PalParkLobby_SetPrize_CheriBerry:
    SetVar VAR_0x8006, ITEM_CHERI_BERRY
    Return

PalParkLobby_SetPrize_ChestoBerry:
    SetVar VAR_0x8006, ITEM_CHESTO_BERRY
    Return

PalParkLobby_SetPrize_PechaBerry:
    SetVar VAR_0x8006, ITEM_PECHA_BERRY
    Return

PalParkLobby_SetPrize_RawstBerry:
    SetVar VAR_0x8006, ITEM_RAWST_BERRY
    Return

PalParkLobby_SetPrize_AspearBerry:
    SetVar VAR_0x8006, ITEM_ASPEAR_BERRY
    Return

PalParkLobby_SetPrize_LeppaBerry:
    SetVar VAR_0x8006, ITEM_LEPPA_BERRY
    Return

PalParkLobby_SetPrize_OranBerry:
    SetVar VAR_0x8006, ITEM_ORAN_BERRY
    Return

PalParkLobby_SetPrize_PersimBerry:
    SetVar VAR_0x8006, ITEM_PERSIM_BERRY
    Return

PalParkLobby_SetPrize_FigyBerry:
    SetVar VAR_0x8006, ITEM_FIGY_BERRY
    Return

PalParkLobby_SetPrize_WikiBerry:
    SetVar VAR_0x8006, ITEM_WIKI_BERRY
    Return

PalParkLobby_SetPrize_MagoBerry:
    SetVar VAR_0x8006, ITEM_MAGO_BERRY
    Return

PalParkLobby_SetPrize_AguavBerry:
    SetVar VAR_0x8006, ITEM_AGUAV_BERRY
    Return

PalParkLobby_SetPrize_IapapaBerry:
    SetVar VAR_0x8006, ITEM_IAPAPA_BERRY
    Return

PalParkLobby_SetPrize_RazzBerry:
    SetVar VAR_0x8006, ITEM_RAZZ_BERRY
    Return

PalParkLobby_SetPrize_BlukBerry:
    SetVar VAR_0x8006, ITEM_BLUK_BERRY
    Return

PalParkLobby_SetPrize_NanabBerry:
    SetVar VAR_0x8006, ITEM_NANAB_BERRY
    Return

PalParkLobby_SetPrize_WepearBerry:
    SetVar VAR_0x8006, ITEM_WEPEAR_BERRY
    Return

PalParkLobby_SetPrize_PinapBerry:
    SetVar VAR_0x8006, ITEM_PINAP_BERRY
    Return

PalParkLobby_SetPrize_LumBerry:
    SetVar VAR_0x8006, ITEM_LUM_BERRY
    Return

PalParkLobby_SetPrize_SitrusBerry:
    SetVar VAR_0x8006, ITEM_SITRUS_BERRY
    Return

PalParkLobby_SetPrize_PomegBerry:
    SetVar VAR_0x8006, ITEM_POMEG_BERRY
    Return

PalParkLobby_SetPrize_KelpsyBerry:
    SetVar VAR_0x8006, ITEM_KELPSY_BERRY
    Return

PalParkLobby_SetPrize_QualotBerry:
    SetVar VAR_0x8006, ITEM_QUALOT_BERRY
    Return

PalParkLobby_SetPrize_HondewBerry:
    SetVar VAR_0x8006, ITEM_HONDEW_BERRY
    Return

PalParkLobby_SetPrize_GrepaBerry:
    SetVar VAR_0x8006, ITEM_GREPA_BERRY
    Return

PalParkLobby_SetPrize_TamatoBerry:
    SetVar VAR_0x8006, ITEM_TAMATO_BERRY
    Return

    .balign 4, 0

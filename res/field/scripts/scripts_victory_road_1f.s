#include "macros/scrcmd.inc"
#include "res/text/bank/victory_road_1f.h"
#include "res/field/events/events_victory_road_1f.h"


    ScriptEntry VictoryRoad_OnTransition
    ScriptEntry VictoryRoad_Collector
    ScriptEntry VictoryRoad1F_CoordEvent_Counterpart
    ScriptEntry VictoryRoad1F_Counterpart
    ScriptEntryEnd

VictoryRoad_OnTransition:
    SetFlag FLAG_FIRST_ARRIVAL_VICTORY_ROAD
    Call VictoryRoad1F_SetCounterpartGraphics
    GoToIfUnset FLAG_GAME_COMPLETED, VictoryRoad_DontHideCollector
    GetNationalDexEnabled VAR_MAP_LOCAL_0x00
    GoToIfEq VAR_MAP_LOCAL_0x00, FALSE, VictoryRoad_DontHideCollector
    SetFlag FLAG_HIDE_VICTORY_ROAD_1F_COLLECTOR
VictoryRoad_DontHideCollector:
    End

VictoryRoad_Collector:
    PlaySE SE_CONFIRM_sseq_3
    LockAll
    FacePlayer
    GoToIfSet FLAG_GAME_COMPLETED, VictoryRoad1F_YoullMeetManyPokemon
    Message VictoryRoad1F_Text_AimForPokemonLeague
    GoTo VictoryRoad1F_CollectorEnd
    End

VictoryRoad1F_YoullMeetManyPokemon:
    Message VictoryRoad1F_Text_YoullMeetManyPokemon
    GoTo VictoryRoad1F_CollectorEnd
    End

VictoryRoad1F_CollectorEnd:
    WaitButton
    CloseMessage
    ReleaseAll
    End

@ Oxide: Lucas or Dawn waits just inside the entrance for the level 71 fight
@ Ian designed for the start of Victory Road (trainers 779 to 784, the same
@ teams the Battleground uses after the game). The counterpart is whichever
@ of the two the player did not choose, as on Routes 202 and 207.
VictoryRoad1F_SetCounterpartGraphics:
    GetPlayerGender VAR_MAP_LOCAL_0x00
    GoToIfEq VAR_MAP_LOCAL_0x00, GENDER_MALE, VictoryRoad1F_SetCounterpartGraphicsDawn
    SetVar VAR_OBJ_GFX_ID_0, OBJ_EVENT_GFX_PLAYER_M
    Return

VictoryRoad1F_SetCounterpartGraphicsDawn:
    SetVar VAR_OBJ_GFX_ID_0, OBJ_EVENT_GFX_PLAYER_F
    Return

@ The trigger is the row just inside the entrance, which every way north
@ crosses. The player is walked in front of the counterpart first.
VictoryRoad1F_CoordEvent_Counterpart:
    LockAll
    ApplyMovement LOCALID_COUNTERPART, VictoryRoad1F_Movement_CounterpartNoticePlayer
    WaitMovement
    GetPlayerMapPos VAR_0x8004, VAR_0x8005
    CallIfEq VAR_0x8004, 13, VictoryRoad1F_PlayerWalkEastTwo
    CallIfEq VAR_0x8004, 14, VictoryRoad1F_PlayerWalkEastOne
    CallIfEq VAR_0x8004, 15, VictoryRoad1F_PlayerFaceNorth
    CallIfEq VAR_0x8004, 16, VictoryRoad1F_PlayerWalkWestOne
    CallIfEq VAR_0x8004, 17, VictoryRoad1F_PlayerWalkWestTwo
    GoTo VictoryRoad1F_CounterpartBattle
    End

@ Talking to the counterpart without crossing the trigger, which only a
@ player coming back from further in can do, starts the same fight.
VictoryRoad1F_Counterpart:
    PlaySE SE_CONFIRM_sseq_3
    LockAll
    FacePlayer
    GoTo VictoryRoad1F_CounterpartBattle
    End

VictoryRoad1F_PlayerWalkEastTwo:
    ApplyMovement LOCALID_PLAYER, VictoryRoad1F_Movement_PlayerWalkEastTwo
    WaitMovement
    Return

VictoryRoad1F_PlayerWalkEastOne:
    ApplyMovement LOCALID_PLAYER, VictoryRoad1F_Movement_PlayerWalkEastOne
    WaitMovement
    Return

VictoryRoad1F_PlayerFaceNorth:
    ApplyMovement LOCALID_PLAYER, VictoryRoad1F_Movement_PlayerFaceNorth
    WaitMovement
    Return

VictoryRoad1F_PlayerWalkWestOne:
    ApplyMovement LOCALID_PLAYER, VictoryRoad1F_Movement_PlayerWalkWestOne
    WaitMovement
    Return

VictoryRoad1F_PlayerWalkWestTwo:
    ApplyMovement LOCALID_PLAYER, VictoryRoad1F_Movement_PlayerWalkWestTwo
    WaitMovement
    Return

VictoryRoad1F_CounterpartBattle:
    Common_SetCounterpartBGM
    BufferPlayerName 0
    GetPlayerGender VAR_RESULT
    GoToIfEq VAR_RESULT, GENDER_MALE, VictoryRoad1F_Dawn
    GoTo VictoryRoad1F_Lucas
    End

@ Each counterpart has one team per starter, led by the fully evolved
@ starter the counterpart took at the start, and picked the way the
@ Battleground picks them.
VictoryRoad1F_Dawn:
    Message VictoryRoad1F_Text_DawnGetPastMeFirst
    CloseMessage
    GetPlayerStarterSpecies VAR_RESULT
    GoToIfEq VAR_RESULT, SPECIES_TURTWIG, VictoryRoad1F_BattleDawnEmpoleon
    @ Oxide: Scorbunny holds the fire starter's place (Ian, 2026-09-21).
    GoToIfEq VAR_RESULT, SPECIES_SCORBUNNY, VictoryRoad1F_BattleDawnTorterra
    GoTo VictoryRoad1F_BattleDawnInfernape
    End

VictoryRoad1F_BattleDawnEmpoleon:
    StartTrainerBattle TRAINER_DUMMY_779
    GoTo VictoryRoad1F_DawnAfterBattle
    End

VictoryRoad1F_BattleDawnTorterra:
    StartTrainerBattle TRAINER_DUMMY_780
    GoTo VictoryRoad1F_DawnAfterBattle
    End

VictoryRoad1F_BattleDawnInfernape:
    StartTrainerBattle TRAINER_DUMMY_781
    GoTo VictoryRoad1F_DawnAfterBattle
    End

VictoryRoad1F_DawnAfterBattle:
    CheckWonBattle VAR_RESULT
    GoToIfEq VAR_RESULT, FALSE, VictoryRoad1F_BlackOut
    Message VictoryRoad1F_Text_DawnYouReallyAreReady
    GoTo VictoryRoad1F_CounterpartLeave
    End

VictoryRoad1F_Lucas:
    Message VictoryRoad1F_Text_LucasLetsSeeIfYoureReady
    CloseMessage
    GetPlayerStarterSpecies VAR_RESULT
    GoToIfEq VAR_RESULT, SPECIES_TURTWIG, VictoryRoad1F_BattleLucasEmpoleon
    @ Oxide: Scorbunny holds the fire starter's place (Ian, 2026-09-21).
    GoToIfEq VAR_RESULT, SPECIES_SCORBUNNY, VictoryRoad1F_BattleLucasTorterra
    GoTo VictoryRoad1F_BattleLucasInfernape
    End

VictoryRoad1F_BattleLucasEmpoleon:
    StartTrainerBattle TRAINER_DUMMY_782
    GoTo VictoryRoad1F_LucasAfterBattle
    End

VictoryRoad1F_BattleLucasTorterra:
    StartTrainerBattle TRAINER_DUMMY_783
    GoTo VictoryRoad1F_LucasAfterBattle
    End

VictoryRoad1F_BattleLucasInfernape:
    StartTrainerBattle TRAINER_DUMMY_784
    GoTo VictoryRoad1F_LucasAfterBattle
    End

VictoryRoad1F_LucasAfterBattle:
    CheckWonBattle VAR_RESULT
    GoToIfEq VAR_RESULT, FALSE, VictoryRoad1F_BlackOut
    Message VictoryRoad1F_Text_LucasYoureReadyAllRight
    GoTo VictoryRoad1F_CounterpartLeave
    End

@ A fade rather than a walk-off, because the counterpart may have been
@ talked to from any side and a scripted walk ignores the player's tile.
VictoryRoad1F_CounterpartLeave:
    WaitButton
    CloseMessage
    FadeScreenOut
    WaitFadeScreen
    RemoveObject LOCALID_COUNTERPART
    FadeScreenIn
    WaitFadeScreen
    Common_FadeToDefaultMusic
    SetVar VAR_VICTORY_ROAD_1F_COUNTERPART_TRIGGER_STATE, 1
    ReleaseAll
    End

@ Losing leaves the trigger and the counterpart in place for another try.
VictoryRoad1F_BlackOut:
    BlackOutFromBattle
    ReleaseAll
    End

    .balign 4, 0
VictoryRoad1F_Movement_CounterpartNoticePlayer:
    EmoteExclamationMark
    EndMovement

    .balign 4, 0
VictoryRoad1F_Movement_PlayerWalkEastTwo:
    WalkNormalEast 2
    WalkOnSpotNormalNorth
    EndMovement

    .balign 4, 0
VictoryRoad1F_Movement_PlayerWalkEastOne:
    WalkNormalEast
    WalkOnSpotNormalNorth
    EndMovement

    .balign 4, 0
VictoryRoad1F_Movement_PlayerFaceNorth:
    WalkOnSpotNormalNorth
    EndMovement

    .balign 4, 0
VictoryRoad1F_Movement_PlayerWalkWestOne:
    WalkNormalWest
    WalkOnSpotNormalNorth
    EndMovement

    .balign 4, 0
VictoryRoad1F_Movement_PlayerWalkWestTwo:
    WalkNormalWest 2
    WalkOnSpotNormalNorth
    EndMovement

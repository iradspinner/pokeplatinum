#include "macros/scrcmd.inc"
#include "res/text/bank/route_214_gate_to_veilstone_city.h"
#include "res/field/events/events_route_214_gate_to_veilstone_city.h"


    ScriptEntry Route214GateToVeilstoneCity_MiddleAgedMan
    ScriptEntry Route214GateToVeilstoneCity_OnTransition
    ScriptEntry Route214GateToVeilstoneCity_Policeman
    ScriptEntry Route214GateToVeilstoneCity_PolicemanStopsPlayer
    ScriptEntryEnd

@ Oxide (Ian, 2026-10-31): a policeman closes Route 214 from Veilstone until
@ the player has Maylene's Cobble Badge. Vanilla leaves the way open, so a
@ player could walk to Pastoria first, beat Wake, and miss Barry's battle
@ outside Pastoria Gym for good. The badge is read into VAR_MAP_LOCAL_0x01
@ each time the gate loads, and the trigger across the corridor's mouth (the
@ events' coord event) runs only while it is 0.
Route214GateToVeilstoneCity_OnTransition:
    CheckBadgeAcquired BADGE_ID_COBBLE, VAR_MAP_LOCAL_0x01
    GetRandom VAR_RANDOM_INTERVIEW_QUESTION, 4
    CheckTVInterviewEligible TV_PROGRAM_SEGMENT_IN_YOUR_FACE_INTERVIEW_QUESTION_1, VAR_MAP_LOCAL_0x00
    GoToIfEq VAR_MAP_LOCAL_0x00, FALSE, Route214GateToVeilstoneCity_HideReporter
    CheckTVInterviewEligible TV_PROGRAM_SEGMENT_IN_YOUR_FACE_INTERVIEW_QUESTION_2, VAR_MAP_LOCAL_0x00
    GoToIfEq VAR_MAP_LOCAL_0x00, FALSE, Route214GateToVeilstoneCity_HideReporter
    CheckTVInterviewEligible TV_PROGRAM_SEGMENT_IN_YOUR_FACE_INTERVIEW_QUESTION_3, VAR_MAP_LOCAL_0x00
    GoToIfEq VAR_MAP_LOCAL_0x00, FALSE, Route214GateToVeilstoneCity_HideReporter
    CheckTVInterviewEligible TV_PROGRAM_SEGMENT_IN_YOUR_FACE_INTERVIEW_QUESTION_4, VAR_MAP_LOCAL_0x00
    GoToIfEq VAR_MAP_LOCAL_0x00, FALSE, Route214GateToVeilstoneCity_HideReporter
    ClearFlag FLAG_HIDE_ROUTE_214_GATE_TO_VEILSTONE_CITY_REPORTER
    End

Route214GateToVeilstoneCity_HideReporter:
    SetFlag FLAG_HIDE_ROUTE_214_GATE_TO_VEILSTONE_CITY_REPORTER
    End

Route214GateToVeilstoneCity_MiddleAgedMan:
    PlaySE SE_CONFIRM_sseq_3
    LockAll
    FacePlayer
    GetUnownFormsSeenCount VAR_MAP_LOCAL_0x00
    GoToIfGe VAR_MAP_LOCAL_0x00, 26, Route214GateToVeilstoneCity_ThatRuinManiac
    Message Route214GateToVeilstoneCity_Text_RouteIsChewedUp
    WaitButton
    CloseMessage
    ReleaseAll
    End

Route214GateToVeilstoneCity_ThatRuinManiac:
    Message Route214GateToVeilstoneCity_Text_ThatRuinManiac
    WaitButton
    CloseMessage
    ReleaseAll
    End

Route214GateToVeilstoneCity_Policeman:
    PlaySE SE_CONFIRM_sseq_3
    LockAll
    FacePlayer
    GoToIfEq VAR_MAP_LOCAL_0x01, TRUE, Route214GateToVeilstoneCity_GoOnThrough
    Message Route214GateToVeilstoneCity_Text_OnlyTrainersWithGymBadge
    GoTo Route214GateToVeilstoneCity_PolicemanEnd
    End

Route214GateToVeilstoneCity_GoOnThrough:
    Message Route214GateToVeilstoneCity_Text_GoOnThrough
Route214GateToVeilstoneCity_PolicemanEnd:
    WaitButton
    CloseMessage
    ReleaseAll
    End

@ Stepping into the corridor from Veilstone's side without the badge: the
@ policeman calls out and the player steps back north, off the trigger. A
@ player already south of the gate (a save from before this change) is let
@ through northward without a word.
Route214GateToVeilstoneCity_PolicemanStopsPlayer:
    LockAll
    GetPlayerDir VAR_0x8004
    GoToIfEq VAR_0x8004, DIR_NORTH, Route214GateToVeilstoneCity_PolicemanRelease
    ApplyMovement LOCALID_POLICEMAN, Route214GateToVeilstoneCity_Movement_PolicemanNotice
    WaitMovement
    Message Route214GateToVeilstoneCity_Text_OnlyTrainersWithGymBadge
    WaitButton
    CloseMessage
    ApplyMovement LOCALID_PLAYER, Route214GateToVeilstoneCity_Movement_PlayerStepBack
    WaitMovement
Route214GateToVeilstoneCity_PolicemanRelease:
    ReleaseAll
    End

    .balign 4, 0
Route214GateToVeilstoneCity_Movement_PolicemanNotice:
    EmoteExclamationMark
    EndMovement

    .balign 4, 0
Route214GateToVeilstoneCity_Movement_PlayerStepBack:
    WalkNormalNorth
    EndMovement

    .balign 4, 0

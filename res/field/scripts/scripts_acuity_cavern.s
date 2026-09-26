#include "macros/scrcmd.inc"
#include "res/text/bank/acuity_cavern.h"
#include "res/field/events/events_acuity_cavern.h"


    ScriptEntry AcuityCavern_OnTransition
    ScriptEntry AcuityCavern_OnLoad
    ScriptEntry AcuityCavern_Uxie
    ScriptEntryEnd

AcuityCavern_OnTransition:
    SetFlag FLAG_FIRST_ARRIVAL_ACUITY_CAVERN
    @ Oxide: a save from before the legendary pool has no draw; it meets the
    @ vanilla Uxie rather than a Pokemon with no species.
    CallIfEq VAR_LEGENDARY_POOL_ACUITY_SPECIES, SPECIES_NONE, AcuityCavern_DrawUxie
    End

AcuityCavern_DrawUxie:
    SetVar VAR_LEGENDARY_POOL_ACUITY_SPECIES, SPECIES_UXIE
    Return

AcuityCavern_OnLoad:
    GoToIfSet FLAG_MAP_LOCAL_REMOVE_OBJECT, AcuityCavern_RemoveUxie
    End

AcuityCavern_RemoveUxie:
    SetFlag FLAG_HIDE_ACUITY_CAVERN_UXIE
    RemoveObject LOCALID_UXIE
    ClearFlag FLAG_MAP_LOCAL_REMOVE_OBJECT
    End

@ Oxide: Uxie's cavern holds the legendary pool's Acuity draw, rolled once
@ per save by InitNewGame (Ian, 2026-09-26). The object keeps Uxie's sprite,
@ since the drawn species have none (Ian, 2026-09-27); the cry, the battle and
@ the name are the drawn species. FLAG_CAUGHT_UXIE now means "caught the
@ Acuity draw", which is how the Hall of Fame's respawn reads it.
AcuityCavern_Uxie:
    PlaySE SE_CONFIRM_sseq_3
    LockAll
    FacePlayer
    PlayCry VAR_LEGENDARY_POOL_ACUITY_SPECIES
    Message AcuityCavern_Text_UxieCry
    CloseMessage
    SetFlag FLAG_MAP_LOCAL_REMOVE_OBJECT
    StartLegendaryBattle VAR_LEGENDARY_POOL_ACUITY_SPECIES, 50
    ClearFlag FLAG_MAP_LOCAL_REMOVE_OBJECT
    CheckWonBattle VAR_RESULT
    GoToIfEq VAR_RESULT, FALSE, AcuityCavern_LostBattle
    CheckDidNotCapture VAR_RESULT
    GoToIfEq VAR_RESULT, TRUE, AcuityCavern_UxieDisappeared
    SetFlag FLAG_CAUGHT_UXIE
    ReleaseAll
    End

AcuityCavern_UxieDisappeared:
    BufferSpeciesNameFromVar 0, VAR_LEGENDARY_POOL_ACUITY_SPECIES, 0, 0
    Message AcuityCavern_Text_UxieDisappeared
    WaitButton
    CloseMessage
    ReleaseAll
    End

AcuityCavern_LostBattle:
    BlackOutFromBattle
    ReleaseAll
    End

    .balign 4, 0

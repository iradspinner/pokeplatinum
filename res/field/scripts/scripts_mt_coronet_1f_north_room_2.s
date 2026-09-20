#include "macros/scrcmd.inc"


    ScriptEntry MtCoronet1FNorthRoom2_Dummy1
    ScriptEntry MtCoronet1FNorthRoom2_OnTransition
    ScriptEntry MtCoronet1FNorthRoom2_OnLoad
    ScriptEntryEnd

MtCoronet1FNorthRoom2_Dummy1:
    End

MtCoronet1FNorthRoom2_OnTransition:
    CallIfNe VAR_ICEBERG_RUINS_STATE, RUINS_STATE_CAUGHT_REGI, MtCoronet1FNorthRoom2_ResetIcebergRuinsState
    End

MtCoronet1FNorthRoom2_OnLoad:
    CheckPartyHasSpecies VAR_MAP_LOCAL_0x01, SPECIES_RELICANTH
    CheckPartyHasSpecies VAR_MAP_LOCAL_0x02, SPECIES_WAILORD
    GoToIfUnset FLAG_GALACTIC_LEFT_LAKE_VALOR, MtCoronet1FNorthRoom2_RemoveWarpIcebergRuinsWithRegice
    GoToIfEq VAR_MAP_LOCAL_0x01, FALSE, MtCoronet1FNorthRoom2_RemoveWarpIcebergRuinsWithRegice
    GoToIfEq VAR_MAP_LOCAL_0x02, FALSE, MtCoronet1FNorthRoom2_RemoveWarpIcebergRuinsWithRegice
    GoTo MtCoronet1FNorthRoom2_RemoveWarpIcebergRuinsWithoutRegice

MtCoronet1FNorthRoom2_ResetIcebergRuinsState:
    SetVar VAR_ICEBERG_RUINS_STATE, 0
    Return

MtCoronet1FNorthRoom2_RemoveWarpIcebergRuinsWithRegice:
    SetWarpEventPos 3, 17, 16
    End

MtCoronet1FNorthRoom2_RemoveWarpIcebergRuinsWithoutRegice:
    SetWarpEventPos 2, 17, 16
    End

#include "macros/btlcmd.inc"


// Oxide: Meloetta switches between Aria and Pirouette after a Relic Song
// that hit, as in hg-engine (BattleFormChangeCheck). The controller sets
// BTLVAR_MSG_BATTLER_TEMP to Meloetta and BTLVAR_SCRIPT_TEMP to its new form
// (BattleControllerPlayer_TriggerAfterMoveHitEffects). The ability and types
// come from the new form's record, and the recalculation flag makes the party
// update take the stats from it too, as Shaymin's freeze does.
_000:
    UpdateMonDataFromVar OPCODE_SET, BTLSCR_MSG_BATTLER_TEMP, BATTLEMON_FORM_NUM, BTLVAR_SCRIPT_TEMP
    UpdateVar OPCODE_FLAG_ON, BTLVAR_BATTLE_CTX_STATUS_2, SYSCTL_RECALC_MON_STATS
    LoadArchivedMonData SPECIES_MELOETTA, BTLVAR_SCRIPT_TEMP, SPECIES_DATA_ABILITY_1
    UpdateMonDataFromVar OPCODE_SET, BTLSCR_MSG_BATTLER_TEMP, BATTLEMON_ABILITY, BTLVAR_CALC_TEMP
    LoadArchivedMonData SPECIES_MELOETTA, BTLVAR_SCRIPT_TEMP, SPECIES_DATA_TYPE_1
    UpdateMonDataFromVar OPCODE_SET, BTLSCR_MSG_BATTLER_TEMP, BATTLEMON_TYPE_1, BTLVAR_CALC_TEMP
    LoadArchivedMonData SPECIES_MELOETTA, BTLVAR_SCRIPT_TEMP, SPECIES_DATA_TYPE_2
    UpdateMonDataFromVar OPCODE_SET, BTLSCR_MSG_BATTLER_TEMP, BATTLEMON_TYPE_2, BTLVAR_CALC_TEMP
    Call BATTLE_SUBSCRIPT_FORM_CHANGE
    RefreshMonData BTLSCR_MSG_BATTLER_TEMP
    End

#include "macros/btlcmd.inc"


// Oxide: Parting Shot lowers the target's Attack and Special Attack, then its
// user switches out. The drop is Tickle's, the switch Baton Pass's without its
// flag, so nothing is passed on. As in the later games the user stays in when
// the drop cannot happen: a substitute, or both stats already at their lowest.
// It also stays in when it has nothing to switch to, a wild Pokemon included.
_000:
    CheckSubstitute BTLSCR_SIDE_EFFECT_MON, _fail
    CompareMonDataToValue OPCODE_NEQ, BTLSCR_SIDE_EFFECT_MON, BATTLEMON_ATTACK_STAGE, 0, _drop
    CompareMonDataToValue OPCODE_EQU, BTLSCR_SIDE_EFFECT_MON, BATTLEMON_SP_ATTACK_STAGE, 0, _lowest

_drop:
    Call BATTLE_SUBSCRIPT_ATTACK_MESSAGE_AND_ANIMATION
    UpdateVar OPCODE_FLAG_ON, BTLVAR_BATTLE_CTX_STATUS_2, SYSCTL_STAT_STAGE_CHANGE_SHOWN
    UpdateVar OPCODE_SET, BTLVAR_SIDE_EFFECT_PARAM, MOVE_SUBSCRIPT_PTR_ATTACK_DOWN_1_STAGE
    Call BATTLE_SUBSCRIPT_UPDATE_STAT_STAGE
    UpdateVar OPCODE_FLAG_ON, BTLVAR_BATTLE_CTX_STATUS, SYSCTL_TURN_OFF_MESSAGES
    UpdateVar OPCODE_SET, BTLVAR_SIDE_EFFECT_PARAM, MOVE_SUBSCRIPT_PTR_SP_ATTACK_DOWN_1_STAGE
    Call BATTLE_SUBSCRIPT_UPDATE_STAT_STAGE
    UpdateVar OPCODE_FLAG_OFF, BTLVAR_BATTLE_CTX_STATUS_2, SYSCTL_UPDATE_STAT_STAGES
    UpdateVar OPCODE_FLAG_OFF, BTLVAR_BATTLE_CTX_STATUS_2, SYSCTL_STAT_STAGE_CHANGE_SHOWN
    UpdateVar OPCODE_FLAG_OFF, BTLVAR_BATTLE_CTX_STATUS, SYSCTL_TURN_OFF_MESSAGES
    TryReplaceFaintedMon BTLSCR_ATTACKER, TRUE, _end
    TryRestoreStatusOnSwitch BTLSCR_ATTACKER, _switch
    UpdateMonData OPCODE_SET, BTLSCR_ATTACKER, BATTLEMON_STATUS, MON_CONDITION_NONE

_switch:
    DeletePokemon BTLSCR_ATTACKER
    Wait
    HealthBoxSlideOut BTLSCR_ATTACKER
    Wait
    UpdateVarFromVar OPCODE_SET, BTLVAR_SWITCHED_MON, BTLVAR_ATTACKER
    GoToSubscript BATTLE_SUBSCRIPT_SHOW_PARTY_LIST

_lowest:
    PrintAttackMessage
    Wait
    WaitButtonABTime 30
    // {0}’s stats won’t go any lower!
    PrintMessage BattleStrings_Text_PokemonsStatsWontGoAnyLower_Ally, TAG_NICKNAME, BTLSCR_SIDE_EFFECT_MON
    Wait
    WaitButtonABTime 30
    UpdateVar OPCODE_FLAG_ON, BTLVAR_MOVE_STATUS_FLAGS, MOVE_STATUS_NO_MORE_WORK
    End

_fail:
    UpdateVar OPCODE_FLAG_ON, BTLVAR_MOVE_STATUS_FLAGS, MOVE_STATUS_FAILED

_end:
    End

#include "macros/btlcmd.inc"


// Oxide: Dragon Tail and Circle Throw drag the target out after they hit. This
// is Roar's switch, from its subscript, run as a hit's side effect. Nothing
// happens if the target fainted, is behind a substitute, anchored by Suction
// Cups or Ingrain, or cannot be dragged out by TryDragonTail's rules; the hit
// has already done its damage, so none of these fails the move.
_000:
    CompareMonDataToValue OPCODE_EQU, BTLSCR_DEFENDER, BATTLEMON_CUR_HP, 0, _end
    CompareMonDataToValue OPCODE_EQU, BTLSCR_ATTACKER, BATTLEMON_CUR_HP, 0, _end
    CheckSubstitute BTLSCR_DEFENDER, _end
    CheckIgnorableAbility CHECK_HAVE, BTLSCR_DEFENDER, ABILITY_SUCTION_CUPS, _end
    CompareMonDataToValue OPCODE_FLAG_SET, BTLSCR_DEFENDER, BATTLEMON_MOVE_EFFECTS_MASK, MOVE_EFFECT_INGRAIN, _end
    TryDragonTail _end
    TryRestoreStatusOnSwitch BTLSCR_DEFENDER, _delete
    UpdateMonData OPCODE_SET, BTLSCR_DEFENDER, BATTLEMON_STATUS, MON_CONDITION_NONE

_delete:
    DeletePokemon BTLSCR_DEFENDER
    Wait
    CompareVarToValue OPCODE_FLAG_NOT, BTLVAR_BATTLE_TYPE, BATTLE_TYPE_TRAINER, _flee
    HealthBoxSlideOut BTLSCR_DEFENDER
    Wait
    SwitchAndUpdateMon BTLSCR_FORCED_OUT
    Wait
    PokemonSendOut BTLSCR_DEFENDER
    WaitTime 72
    HealthBoxSlideIn BTLSCR_DEFENDER
    Wait
    // {0} was dragged out!
    PrintMessage BattleStrings_Text_PokemonWasDraggedOut_Ally, TAG_NICKNAME, BTLSCR_DEFENDER
    Wait
    WaitButtonABTime 30
    UpdateVarFromVar OPCODE_SET, BTLVAR_SWITCHED_MON, BTLVAR_DEFENDER
    Call BATTLE_SUBSCRIPT_HAZARDS_CHECK
    End

_flee:
    FadeOutBattle
    Wait
    UpdateVar OPCODE_FLAG_ON, BTLVAR_RESULT_MASK, BATTLE_RESULT_PLAYER_FLED
    End

_end:
    End

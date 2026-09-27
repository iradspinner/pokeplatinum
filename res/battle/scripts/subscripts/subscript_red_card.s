#include "macros/btlcmd.inc"


// Oxide, element 7: the Red Card (hg-engine's subscript 491, with Oxide's
// Dragon Tail switch). BattleSystem_TriggerSwitchItem has swapped the two
// battlers, so the card's holder is the attacker here and the battler it
// sends away the defender; the real defender waits in the side-effect
// battler, and both are put back at the end. Suction Cups and Ingrain hold
// the target in place and keep the card; otherwise TryDragonTail's rules
// decide, which in a wild battle end it.
_000:
    CheckIgnorableAbility CHECK_HAVE, BTLSCR_DEFENDER, ABILITY_SUCTION_CUPS, _end
    CompareMonDataToValue OPCODE_FLAG_SET, BTLSCR_DEFENDER, BATTLEMON_MOVE_EFFECTS_MASK, MOVE_EFFECT_INGRAIN, _end
    TryDragonTail _end
    PlayBattleAnimation BTLSCR_ATTACKER, BATTLE_ANIMATION_HELD_ITEM
    Wait
    // {0} held up its Red Card against {1}!
    PrintMessage BattleStrings_Text_PokemonHeldUpItsRedCardAgainstPokemon_AllyAlly, TAG_NICKNAME_NICKNAME, BTLSCR_ATTACKER, BTLSCR_DEFENDER
    Wait
    WaitButtonABTime 30
    RemoveItem BTLSCR_ATTACKER
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
    GoTo _end

_flee:
    FadeOutBattle
    Wait
    UpdateVar OPCODE_FLAG_ON, BTLVAR_RESULT_MASK, BATTLE_RESULT_PLAYER_FLED

_end:
    UpdateVarFromVar OPCODE_SET, BTLVAR_ATTACKER, BTLVAR_DEFENDER
    UpdateVarFromVar OPCODE_SET, BTLVAR_DEFENDER, BTLVAR_SIDE_EFFECT_MON
    End

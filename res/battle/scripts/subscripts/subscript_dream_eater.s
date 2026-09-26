#include "macros/btlcmd.inc"


_000:
    UpdateVarFromVar OPCODE_SET, BTLVAR_HP_CALC_TEMP, BTLVAR_HIT_DAMAGE
    CompareVarToValue OPCODE_EQU, BTLVAR_HP_CALC_TEMP, 0, _037
    DivideVarByValue BTLVAR_HP_CALC_TEMP, 2
    CheckItemHoldEffect CHECK_NOT_HAVE, BTLSCR_ATTACKER, HOLD_EFFECT_LEECH_BOOST, _037
    GetItemEffectParam BTLSCR_ATTACKER, BTLVAR_CALC_TEMP
    UpdateVar OPCODE_ADD, BTLVAR_CALC_TEMP, 0x00000064
    UpdateVarFromVar OPCODE_MUL, BTLVAR_HP_CALC_TEMP, BTLVAR_CALC_TEMP
    UpdateVar OPCODE_DIV, BTLVAR_HP_CALC_TEMP, 100

_037:
    UpdateVarFromVar OPCODE_SET, BTLVAR_MSG_BATTLER_TEMP, BTLVAR_ATTACKER
    UpdateVar OPCODE_FLAG_ON, BTLVAR_BATTLE_CTX_STATUS, SYSCTL_SKIP_SPRITE_BLINK
    // Oxide: Liquid Ooze hurts a Dream Eater user as it hurts other draining
    // moves' users (Generation 5), Heal Block or not.
    CheckAbility CHECK_HAVE, BTLSCR_DEFENDER, ABILITY_LIQUID_OOZE, _liquid_ooze
    CompareMonDataToValue OPCODE_NEQ, BTLSCR_ATTACKER, BATTLEMON_HEAL_BLOCK_TURNS, 0, _059
    UpdateVar OPCODE_MUL, BTLVAR_HP_CALC_TEMP, -1
    Call BATTLE_SUBSCRIPT_UPDATE_HP
    // {0}’s dream was eaten!
    PrintMessage BattleStrings_Text_PokemonsDreamWasEaten_Ally, TAG_NICKNAME, BTLSCR_DEFENDER
    Wait 
    WaitButtonABTime 30
    End 

_059:
    UpdateVar OPCODE_SET, BTLVAR_MSG_MOVE_TEMP, MOVE_HEAL_BLOCK
    // {0} was prevented from healing due to {1}!
    PrintMessage BattleStrings_Text_PokemonWasPreventedFromHealingDueToMove_Ally, TAG_NICKNAME_MOVE, BTLSCR_ATTACKER, BTLSCR_MSG_TEMP
    Wait 
    WaitButtonABTime 30
    End 

_liquid_ooze:
    CheckAbility CHECK_HAVE, BTLSCR_ATTACKER, ABILITY_MAGIC_GUARD, _liquid_ooze_end
    Call BATTLE_SUBSCRIPT_UPDATE_HP
    // It sucked up the liquid ooze!
    PrintMessage BattleStrings_Text_ItSuckedUpTheLiquidOoze, TAG_NONE
    Wait 
    WaitButtonABTime 30

_liquid_ooze_end:
    End

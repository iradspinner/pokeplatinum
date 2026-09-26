#include "macros/btlcmd.inc"


_000:
    CheckSubstitute BTLSCR_DEFENDER, _034
    CompareMonDataToValue OPCODE_FLAG_SET, BTLSCR_DEFENDER, BATTLEMON_MOVE_EFFECTS_MASK, MOVE_EFFECT_ABILITY_SUPPRESSED, _034
    CompareVarToValue OPCODE_FLAG_SET, BTLVAR_MOVE_STATUS_FLAGS, MOVE_STATUS_MISSED|MOVE_STATUS_SEMI_INVULNERABLE, _034
    // Oxide: the abilities it cannot change are Ability_ChangeFails' list,
    // where Platinum listed only Multitype.
    CheckAbilityChange ABILITY_CHANGE_SUPPRESS, _034
    Call BATTLE_SUBSCRIPT_ATTACK_MESSAGE_AND_ANIMATION
    UpdateMonData OPCODE_FLAG_ON, BTLSCR_DEFENDER, BATTLEMON_MOVE_EFFECTS_MASK, MOVE_EFFECT_ABILITY_SUPPRESSED
    // {0}’s ability was suppressed!
    PrintMessage BattleStrings_Text_PokemonsAbilityWasSuppressed_Ally, TAG_NICKNAME, BTLSCR_DEFENDER
    Wait 
    WaitButtonABTime 30
    End 

_034:
    UpdateVar OPCODE_FLAG_ON, BTLVAR_MOVE_STATUS_FLAGS, MOVE_STATUS_FAILED
    End 

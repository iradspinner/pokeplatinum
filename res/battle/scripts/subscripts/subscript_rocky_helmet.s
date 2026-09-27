#include "macros/btlcmd.inc"


// Oxide, element 7: the Rocky Helmet hurts a battler that makes contact with
// its holder by a sixth of its own HP. The Jaboca Berry's subscript, less
// the item's removal: the helmet stays.
_000:
    CompareMonDataToValue OPCODE_EQU, BTLSCR_DEFENDER, BATTLEMON_CUR_HP, 0, _009
    PlayBattleAnimation BTLSCR_DEFENDER, BATTLE_ANIMATION_HELD_ITEM
    Wait

_009:
    UpdateVar OPCODE_FLAG_ON, BTLVAR_BATTLE_CTX_STATUS, SYSCTL_SKIP_SPRITE_BLINK
    UpdateVarFromVar OPCODE_SET, BTLVAR_MSG_BATTLER_TEMP, BTLVAR_ATTACKER
    Call BATTLE_SUBSCRIPT_UPDATE_HP
    // {0} is hurt by {1}’s {2}!
    PrintMessage BattleStrings_Text_PokemonIsHurtByPokemonsItem_AllyAlly, TAG_NICKNAME_NICKNAME_ITEM, BTLSCR_ATTACKER, BTLSCR_DEFENDER, BTLSCR_DEFENDER
    Wait
    WaitButtonABTime 30
    End

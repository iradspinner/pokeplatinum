#include "macros/btlcmd.inc"


// Oxide: Hospitality. The holder's partner, BTLSCR_SIDE_EFFECT_MON, gets back
// the HP BattleSystem_TriggerEffectOnSwitch left in BTLVAR_HP_CALC_TEMP.
_000:
    // {0} drank down all the matcha {1} made!
    PrintMessage BattleStrings_Text_PokemonDrankDownAllTheMatchaPokemonMade_AllyAlly, TAG_NICKNAME_NICKNAME, BTLSCR_SIDE_EFFECT_MON, BTLSCR_MSG_BATTLER_TEMP
    Wait 
    WaitButtonABTime 30
    UpdateVarFromVar OPCODE_SET, BTLVAR_MSG_BATTLER_TEMP, BTLVAR_SIDE_EFFECT_MON
    UpdateVar OPCODE_FLAG_ON, BTLVAR_BATTLE_CTX_STATUS, SYSCTL_SKIP_SPRITE_BLINK
    Call BATTLE_SUBSCRIPT_UPDATE_HP
    End 

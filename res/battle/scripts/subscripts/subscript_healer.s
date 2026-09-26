#include "macros/btlcmd.inc"


// Oxide: Healer. BTLSCR_MSG_BATTLER_TEMP is the partner it cures, abilityMon
// the holder and BTLVAR_MSG_TEMP the status, as Shed Skin's subscript has them.
_000:
    UpdateMonData OPCODE_SET, BTLSCR_MSG_BATTLER_TEMP, BATTLEMON_STATUS, MON_CONDITION_NONE
    UpdateMonData OPCODE_FLAG_OFF, BTLSCR_MSG_BATTLER_TEMP, BATTLEMON_VOLATILE_STATUS, VOLATILE_CONDITION_NIGHTMARE
    // {0} was cured of its {2} status by its ally’s {1}!
    PrintMessage BattleStrings_Text_PokemonWasCuredOfItsStatusByItsAllysAbility_Ally, TAG_NICKNAME_ABILITY_STATUS, BTLSCR_MSG_BATTLER_TEMP, BTLSCR_ABILITY_MON, BTLSCR_MSG_TEMP
    Wait 
    SetHealthBoxStatusIcon BTLSCR_MSG_BATTLER_TEMP, BATTLE_ANIMATION_NONE
    WaitButtonABTime 30
    End 

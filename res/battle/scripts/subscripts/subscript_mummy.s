#include "macros/btlcmd.inc"


// Oxide: Mummy. A contact move passes the holder's ability to the attacker,
// which BattleSystem_TriggerAbilityOnHit has checked it may take.
_000:
    UpdateMonDataFromVar OPCODE_GET, BTLSCR_DEFENDER, BATTLEMON_ABILITY, BTLVAR_CALC_TEMP
    UpdateMonDataFromVar OPCODE_SET, BTLSCR_ATTACKER, BATTLEMON_ABILITY, BTLVAR_CALC_TEMP
    // {0} acquired {1}!
    PrintMessage BattleStrings_Text_PokemonAcquiredAbility_Ally, TAG_NICKNAME_ABILITY, BTLSCR_ATTACKER, BTLSCR_ATTACKER
    Wait 
    WaitButtonABTime 30
    End 

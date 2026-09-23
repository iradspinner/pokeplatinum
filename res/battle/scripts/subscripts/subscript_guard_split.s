#include "macros/btlcmd.inc"


// Oxide: Guard Split averages the two battlers' stats, as hg-engine's does, with
// Platinum's attack message and animation first, the way its Pain Split has
// them; hg-engine's plays those from its own C.
_000:
    // A substitute blocks it, as it does Pain Split.
    CheckSubstitute BTLSCR_DEFENDER, _blocked
    Call BATTLE_SUBSCRIPT_ATTACK_MESSAGE_AND_ANIMATION
    UpdateMonDataFromVar OPCODE_GET, BTLSCR_ATTACKER, BATTLEMON_DEFENSE, BTLVAR_CALC_TEMP
    UpdateMonDataFromVar OPCODE_GET, BTLSCR_DEFENDER, BATTLEMON_DEFENSE, BTLVAR_SCRIPT_TEMP
    UpdateVarFromVar OPCODE_ADD, BTLVAR_SCRIPT_TEMP, BTLVAR_CALC_TEMP
    UpdateVar OPCODE_RIGHT_SHIFT, BTLVAR_SCRIPT_TEMP, 1
    UpdateMonDataFromVar OPCODE_SET, BTLSCR_ATTACKER, BATTLEMON_DEFENSE, BTLVAR_SCRIPT_TEMP
    UpdateMonDataFromVar OPCODE_SET, BTLSCR_DEFENDER, BATTLEMON_DEFENSE, BTLVAR_SCRIPT_TEMP
    UpdateMonDataFromVar OPCODE_GET, BTLSCR_ATTACKER, BATTLEMON_SP_DEFENSE, BTLVAR_CALC_TEMP
    UpdateMonDataFromVar OPCODE_GET, BTLSCR_DEFENDER, BATTLEMON_SP_DEFENSE, BTLVAR_SCRIPT_TEMP
    UpdateVarFromVar OPCODE_ADD, BTLVAR_SCRIPT_TEMP, BTLVAR_CALC_TEMP
    UpdateVar OPCODE_RIGHT_SHIFT, BTLVAR_SCRIPT_TEMP, 1
    UpdateMonDataFromVar OPCODE_SET, BTLSCR_ATTACKER, BATTLEMON_SP_DEFENSE, BTLVAR_SCRIPT_TEMP
    UpdateMonDataFromVar OPCODE_SET, BTLSCR_DEFENDER, BATTLEMON_SP_DEFENSE, BTLVAR_SCRIPT_TEMP
    // {0} shared its guard with the target!
    PrintMessage BattleStrings_Text_PokemonSharedItsGuardWithTheTarget_Ally, TAG_NICKNAME, BTLSCR_ATTACKER
    Wait
    WaitButtonABTime 30
    End

_blocked:
    UpdateVar OPCODE_FLAG_ON, BTLVAR_MOVE_STATUS_FLAGS, MOVE_STATUS_FAILED
    End

#include "macros/btlcmd.inc"


// Oxide: Mind Blown. The user pays half its maximum HP once the move is over,
// hit or miss, however many targets it had; the controller charges it
// (BattleControllerPlayer_FaintAfterSelfdestruct), as hg-engine does after
// the move for Mind Blown and Steel Beam. Damp stops the move before it
// starts, and then nothing is paid, as with Explosion.
_000:
    CheckIgnorableAbility CHECK_HAVE, BTLSCR_ALL_BATTLERS, ABILITY_DAMP, _damp
    UpdateVar OPCODE_FLAG_ON, BTLVAR_ATTACKER_SELF_TURN_STATUS_FLAGS, SELF_TURN_FLAG_MIND_BLOWN
    CalcCrit 
    CalcDamage 
    End 

_damp:
    PrintAttackMessage 
    Wait 
    WaitButtonABTime 30
    // {0}’s {1} prevents {2} from using {3}!
    PrintMessage BattleStrings_Text_PokemonsAbilityPreventsPokemonFromUsingMove_AllyAlly, TAG_NICKNAME_ABILITY_NICKNAME_MOVE, BTLSCR_ABILITY_MON, BTLSCR_ABILITY_MON, BTLSCR_ATTACKER, BTLSCR_ATTACKER
    Wait 
    WaitButtonABTime 30
    UpdateVar OPCODE_FLAG_ON, BTLVAR_BATTLE_CTX_STATUS, SYSCTL_CHECK_LOOP_ONLY_ONCE
    UpdateVar OPCODE_FLAG_ON, BTLVAR_MOVE_STATUS_FLAGS, MOVE_STATUS_NO_MORE_WORK
    End 

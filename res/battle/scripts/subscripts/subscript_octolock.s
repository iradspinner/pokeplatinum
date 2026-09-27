#include "macros/btlcmd.inc"


// Oxide: Octolock traps its target as Mean Look does, through the same
// volatile condition and battler, so the trap ends when the user leaves the
// field and a Ghost type can still switch out; the target is also marked, and
// the end of turn check lowers its Defense and Sp. Def each turn
// (BattleControllerPlayer_CheckMonConditions). It fails on a target already
// octolocked or behind a substitute. hg-engine has no code for it.
_000:
    CompareVarToValue OPCODE_FLAG_SET, BTLVAR_MOVE_STATUS_FLAGS, MOVE_STATUS_PROTECTED, _protected
    CompareVarToValue OPCODE_FLAG_SET, BTLVAR_MOVE_STATUS_FLAGS, MOVE_STATUS_DID_NOT_HIT, _missed
    CompareMonDataToValue OPCODE_FLAG_SET, BTLSCR_DEFENDER, BATTLEMON_OXIDE_FLAGS, OXIDE_MON_FLAG_OCTOLOCKED, _fail
    CheckSubstitute BTLSCR_DEFENDER, _fail
    Call BATTLE_SUBSCRIPT_ATTACK_MESSAGE_AND_ANIMATION
    UpdateMonData OPCODE_FLAG_ON, BTLSCR_DEFENDER, BATTLEMON_VOLATILE_STATUS, VOLATILE_CONDITION_MEAN_LOOK
    UpdateMonDataFromVar OPCODE_SET, BTLSCR_DEFENDER, BATTLEMON_MEAN_LOOK_TARGET, BTLVAR_ATTACKER
    UpdateMonData OPCODE_FLAG_ON, BTLSCR_DEFENDER, BATTLEMON_OXIDE_FLAGS, OXIDE_MON_FLAG_OCTOLOCKED
    // {0} can no longer escape because of Octolock!
    PrintMessage BattleStrings_Text_PokemonCanNoLongerEscapeBecauseOfOctolock_Ally, TAG_NICKNAME, BTLSCR_DEFENDER
    Wait 
    WaitButtonABTime 30
    End 

_missed:
    UpdateVar OPCODE_FLAG_OFF, BTLVAR_MOVE_STATUS_FLAGS, MOVE_STATUS_SEMI_INVULNERABLE
    GoTo _fail

_protected:
    UpdateVar OPCODE_FLAG_OFF, BTLVAR_MOVE_STATUS_FLAGS, MOVE_STATUS_PROTECTED

_fail:
    UpdateVar OPCODE_FLAG_ON, BTLVAR_MOVE_STATUS_FLAGS, MOVE_STATUS_FAILED
    End 

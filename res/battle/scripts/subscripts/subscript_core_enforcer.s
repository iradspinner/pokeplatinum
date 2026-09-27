#include "macros/btlcmd.inc"


// Oxide: Core Enforcer suppresses the ability of a target that has already
// moved this turn, once the hit is in, as Gastro Acid does, with the same
// list of abilities that cannot be suppressed. Nothing happens if the target
// fainted, is behind a substitute or has not moved yet. hg-engine has no code
// for it; this is Generation 7's rule.
_000:
    CompareMonDataToValue OPCODE_EQU, BTLSCR_DEFENDER, BATTLEMON_CUR_HP, 0, _end
    CheckSubstitute BTLSCR_DEFENDER, _end
    IfMovedThisTurn BTLSCR_DEFENDER, _moved
    End 

_moved:
    CompareMonDataToValue OPCODE_FLAG_SET, BTLSCR_DEFENDER, BATTLEMON_MOVE_EFFECTS_MASK, MOVE_EFFECT_ABILITY_SUPPRESSED, _end
    CheckAbilityChange ABILITY_CHANGE_SUPPRESS, _end
    UpdateMonData OPCODE_FLAG_ON, BTLSCR_DEFENDER, BATTLEMON_MOVE_EFFECTS_MASK, MOVE_EFFECT_ABILITY_SUPPRESSED
    // {0}’s ability was suppressed!
    PrintMessage BattleStrings_Text_PokemonsAbilityWasSuppressed_Ally, TAG_NICKNAME, BTLSCR_DEFENDER
    Wait 
    WaitButtonABTime 30

_end:
    End 

#include "macros/btlcmd.inc"


// Oxide: Throat Chop's hit starts the target's two-turn count
// (OXIDE_MON_THROAT_CHOP), which the end of each turn lowers
// (BattleControllerPlayer_CheckMonConditions); while it runs the target
// cannot choose or use a sound move. A count already running is not reset,
// as hg-engine has it. Nothing happens if the target fainted or is behind a
// substitute, or if Shield Dust or a Covert Cloak keeps secondary effects
// off. The later games print nothing here, and neither does this.
_000:
    CompareMonDataToValue OPCODE_EQU, BTLSCR_DEFENDER, BATTLEMON_CUR_HP, 0, _end
    CheckSubstitute BTLSCR_DEFENDER, _end
    CheckIgnorableAbility CHECK_HAVE, BTLSCR_DEFENDER, ABILITY_SHIELD_DUST, _end
    CheckItemHoldEffect CHECK_HAVE, BTLSCR_DEFENDER, HOLD_EFFECT_COVERT_CLOAK, _end
    CompareMonDataToValue OPCODE_FLAG_SET, BTLSCR_DEFENDER, BATTLEMON_OXIDE_FLAGS, OXIDE_MON_THROAT_CHOP, _end
    UpdateMonData OPCODE_FLAG_ON, BTLSCR_DEFENDER, BATTLEMON_OXIDE_FLAGS, 2 << OXIDE_MON_THROAT_CHOP_SHIFT

_end:
    End

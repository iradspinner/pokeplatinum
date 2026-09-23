#include "macros/btlcmd.inc"


// Oxide: Incinerate burns up the target's berry after it hits, unless the hit
// met a substitute. Platinum's berries are one run of item ids, Cheri to
// Rowap, so the check is a range; Gems, which it also burns in the later
// games, are not in Oxide.
_000:
    CompareMonDataToValue OPCODE_EQU, BTLSCR_DEFENDER, BATTLEMON_CUR_HP, 0, _end
    CheckSubstitute BTLSCR_DEFENDER, _end
    CompareMonDataToValue OPCODE_LTE, BTLSCR_DEFENDER, BATTLEMON_HELD_ITEM, ITEM_CHERI_BERRY - 1, _end
    CompareMonDataToValue OPCODE_GT, BTLSCR_DEFENDER, BATTLEMON_HELD_ITEM, ITEM_ROWAP_BERRY, _end
    UpdateMonDataFromVar OPCODE_GET, BTLSCR_DEFENDER, BATTLEMON_HELD_ITEM, BTLVAR_MSG_ITEM_TEMP
    UpdateMonData OPCODE_SET, BTLSCR_DEFENDER, BATTLEMON_HELD_ITEM, ITEM_NONE
    // {0}’s {1} was burned up!
    PrintMessage BattleStrings_Text_PokemonsItemWasBurnedUp_Ally, TAG_NICKNAME_ITEM, BTLSCR_DEFENDER, BTLSCR_MSG_TEMP
    Wait
    WaitButtonABTime 30

_end:
    End

#include "macros/btlcmd.inc"


// Oxide, element 7: the Eject Button (hg-engine's subscript 340). Its holder,
// BTLSCR_MSG_TEMP, goes back when hit and its trainer picks a replacement, as
// after U-turn. With nothing to send out, nothing happens and the button
// stays.
_000:
    TryReplaceFaintedMon BTLSCR_MSG_TEMP, TRUE, _end
    PlayBattleAnimation BTLSCR_MSG_TEMP, BATTLE_ANIMATION_HELD_ITEM
    Wait
    // {0} is switched out with the {1}!
    PrintMessage BattleStrings_Text_PokemonIsSwitchedOutWithTheItem_Ally, TAG_NICKNAME_ITEM, BTLSCR_MSG_TEMP, BTLSCR_MSG_TEMP
    Wait
    WaitButtonABTime 30
    RemoveItem BTLSCR_MSG_TEMP
    UpdateVarFromVar OPCODE_SET, BTLVAR_SWITCHED_MON, BTLVAR_MSG_BATTLER_TEMP
    TryRestoreStatusOnSwitch BTLSCR_MSG_TEMP, _delete
    UpdateMonData OPCODE_SET, BTLSCR_MSG_TEMP, BATTLEMON_STATUS, MON_CONDITION_NONE

_delete:
    DeletePokemon BTLSCR_MSG_TEMP
    Wait
    HealthBoxSlideOut BTLSCR_MSG_TEMP
    Wait
    GoToSubscript BATTLE_SUBSCRIPT_SHOW_PARTY_LIST

_end:
    End

#include "macros/btlcmd.inc"


_000:
    IncrementGameRecord BTLSCR_FAINTED_MON, BATTLER_TYPE_SOLO_ENEMY, RECORD_FAINTED_IN_BATTLE
    IncrementGameRecord BTLSCR_FAINTED_MON, BATTLER_TYPE_SOLO_PLAYER, RECORD_FAINTED_ENEMY_MON
    PlayFaintAnimation 
    Wait 
    HealthBoxSlideOut BTLSCR_FAINTED_MON
    // {0} fainted!
    PrintMessage BattleStrings_Text_PokemonFainted_Ally, TAG_NICKNAME, BTLSCR_FAINTED_MON
    Wait 
    WaitButtonABTime 30
    CompareVarToValue OPCODE_FLAG_SET, BTLVAR_BATTLE_CTX_STATUS_2, SYSCTL_NO_EXPERIENCE_GIVEN, _023

_023:
    // Oxide: Soul Heart raises its holder's Sp. Atk whenever another battler
    // faints. The stat-stage flag is cleared so its animation plays even when
    // the move that caused the faint already showed one.
    TrySoulHeart _end
    UpdateVar OPCODE_FLAG_OFF, BTLVAR_BATTLE_CTX_STATUS_2, SYSCTL_UPDATE_STAT_STAGES
    Call BATTLE_SUBSCRIPT_UPDATE_STAT_STAGE

_end:
    End 

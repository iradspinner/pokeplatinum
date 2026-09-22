#include "macros/btlcmd.inc"


// Oxide: Stone Axe lays Stealth Rock on the target's side after it hits,
// with Stealth Rock's own check and message. hg-engine's version also queues
// the hazard in its own ordering of entry hazards, which Platinum does not have.
_000:
    CompareVarToValue OPCODE_FLAG_SET, BTLVAR_SIDE_CONDITIONS_DEFENDER, SIDE_CONDITION_STEALTH_ROCK, _end
    UpdateVar OPCODE_FLAG_ON, BTLVAR_SIDE_CONDITIONS_DEFENDER, SIDE_CONDITION_STEALTH_ROCK
    // Pointed stones float in the air around your team!
    PrintMessage BattleStrings_Text_PointedStonesFloatInTheAirAroundYourTeam, TAG_NONE_SIDE_CONSCIOUS, BTLSCR_ATTACKER_ENEMY
    Wait
    WaitButtonABTime 30

_end:
    End

#ifndef POKEPLATINUM_GAUNTLET_H
#define POKEPLATINUM_GAUNTLET_H

#include "field/field_system_decl.h"

// Platinum Oxide: the gauntlets (Ian, 2026-09-27 and 2026-09-29;
// docs/oxide/gauntlets.md). A gauntlet section is a stretch of a dungeon the
// player walks into by its way in. While it is open, the way back is refused,
// and so are the Pocket PC, the Escape Rope, Dig, Fly and Teleport. It closes
// when the player leaves by the way forward or has beaten all its trainers.

// What the gauntlet line script command tells its script to do.
enum GauntletLineResult {
    GAUNTLET_LINE_NOTHING = 0,
    GAUNTLET_LINE_TURN_BACK,
};

void Gauntlet_OnMapChange(FieldSystem *fieldSystem, BOOL noWarp);
BOOL Gauntlet_IsOpen(FieldSystem *fieldSystem);
BOOL Gauntlet_RefusesWarp(FieldSystem *fieldSystem, int warpIndex);
enum GauntletLineResult Gauntlet_StepOnLine(FieldSystem *fieldSystem);

#endif // POKEPLATINUM_GAUNTLET_H

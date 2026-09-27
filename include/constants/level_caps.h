#ifndef POKEPLATINUM_CONSTANTS_LEVEL_CAPS_H
#define POKEPLATINUM_CONSTANTS_LEVEL_CAPS_H

// Platinum Oxide: the level-cap splits, in play order. VAR_LEVEL_CAP_SPLIT
// holds the split the player is in, starting at Roark's on a new game, and
// each split's closing fight raises it to the next with RaiseLevelCap. The
// cap for each split is in sLevelCaps in src/system_vars.c.
#define LEVEL_CAP_SPLIT_ROARK    0
#define LEVEL_CAP_SPLIT_GARDENIA 1
#define LEVEL_CAP_SPLIT_FANTINA  2
#define LEVEL_CAP_SPLIT_MAYLENE  3
#define LEVEL_CAP_SPLIT_WAKE     4
#define LEVEL_CAP_SPLIT_BYRON    5
#define LEVEL_CAP_SPLIT_CANDICE  6
#define LEVEL_CAP_SPLIT_HQ       7
#define LEVEL_CAP_SPLIT_GALACTIC 8
#define LEVEL_CAP_SPLIT_VOLKNER  9
#define LEVEL_CAP_SPLIT_BARRY    10 // after the Beacon Badge, up to the Elite Four
#define LEVEL_CAP_SPLIT_LEAGUE   11 // from entering the Elite Four
#define LEVEL_CAP_SPLIT_NONE     12 // after the Champion: no cap below level 100
#define LEVEL_CAP_SPLIT_COUNT    13

#endif // POKEPLATINUM_CONSTANTS_LEVEL_CAPS_H

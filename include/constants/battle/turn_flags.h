#ifndef POKEPLATINUM_CONSTANTS_BATTLE_TURN_FLAGS_H
#define POKEPLATINUM_CONSTANTS_BATTLE_TURN_FLAGS_H

#define SELF_TURN_FLAG_CLEAR 0
// unused: 1 << 0
#define SELF_TURN_FLAG_PLUCK_BERRY    (1 << 1)
#define SELF_TURN_FLAG_INFATUATED     (1 << 2)
#define SELF_TURN_FLAG_SUBSTITUTE_HIT (1 << 3)

// Oxide: the one-turn guard a battler raised over its side, kept in its
// TurnFlags so it clears with them at the end of the turn.
#define SIDE_GUARD_NONE          0
#define SIDE_GUARD_WIDE_GUARD    1
#define SIDE_GUARD_QUICK_GUARD   2
#define SIDE_GUARD_MAT_BLOCK     3
#define SIDE_GUARD_CRAFTY_SHIELD 4

#endif // POKEPLATINUM_CONSTANTS_BATTLE_TURN_FLAGS_H

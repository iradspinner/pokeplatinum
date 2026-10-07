#ifndef POKEPLATINUM_DATA_SOLD_TMS_H
#define POKEPLATINUM_DATA_SOLD_TMS_H

#include "constants/items.h"

#include "scrcmd_shop.h"

// Platinum Oxide: the TMs that Veilstone's TM counters and the Game Corner's
// prize counter sell, each bought once and only from a badge count (Ian,
// 2026-10-06). Written by tools/oxide/place_rewards.py from the reward table
// (docs/oxide/reward-placements.tsv); change the table and rerun the tool.
// Each TM keeps its bit in VAR_SOLD_TMS_0 and VAR_SOLD_TMS_1 for good once
// given, so a change to the list never moves a purchase a save has made.
// The last entry, ITEM_NONE, ends the list.
// place_rewards.py: sold TMs (begin)
static const SoldTM sSoldTMs[] = {
    { ITEM_TM02, 4, 2, 0 },
    { ITEM_TM05, 4, 2, 1 },
    { ITEM_TM41, 4, 1, 2 },
    { ITEM_TM45, 4, 2, 3 },
    { ITEM_TM59, 4, 2, 4 },
    { ITEM_TM61, 4, 1, 5 },
    { ITEM_TM63, 4, 1, 6 },
    { ITEM_TM73, 4, 1, 7 },
    { ITEM_TM82, 4, 2, 8 },
    { ITEM_TM91, 4, 2, 9 },
    { ITEM_HM02, 5, 1, 10 },
    { ITEM_TM23, 5, 1, 11 },
    { ITEM_TM26, 5, 1, 12 },
    { ITEM_TM29, 5, 1, 13 },
    { ITEM_TM35, 5, 1, 14 },
    { ITEM_TM53, 5, 1, 15 },
    { ITEM_TM67, 5, 1, 16 },
    { ITEM_TM71, 5, 1, 17 },
    { ITEM_TM77, 5, 1, 18 },
    { ITEM_TM07, 5, 1, 19 },
    { ITEM_TM24, 5, 1, 20 },
    { ITEM_HM08, 6, 1, 21 },
    { ITEM_TM13, 6, 1, 22 },
    { ITEM_TM49, 6, 1, 23 },
    { ITEM_TM69, 6, 1, 24 },
    { ITEM_HM03, 8, 1, 25 },
    { ITEM_TM52, 8, 1, 26 },
    { ITEM_TM04, 8, 1, 27 },
    { ITEM_NONE, 0, 0, 0 },
};
// place_rewards.py: sold TMs (end)

#endif // POKEPLATINUM_DATA_SOLD_TMS_H

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
    { ITEM_NONE, 0, 0, 0 },
};
// place_rewards.py: sold TMs (end)

#endif // POKEPLATINUM_DATA_SOLD_TMS_H

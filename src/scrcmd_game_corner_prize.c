#include "scrcmd_game_corner_prize.h"

#include <nitro.h>
#include <string.h>

#include "generated/items.h"

#include "field_script_context.h"
#include "inlines.h"
#include "scrcmd_shop.h"

typedef struct GameCornerPrize {
    u16 item;
    u16 price;
} GameCornerPrize;

// Platinum Oxide: the prize counter's list, at file scope so that
// tools/oxide/place_rewards.py can rewrite it from the reward table and its
// checker can find it in the ROM. Its TMs are sold once, from a badge count
// (include/data/sold_tms.h); a TM takes the coin price of the prize it
// replaced, for the whole purchase.
// place_rewards.py: Game Corner prizes (begin)
static const GameCornerPrize sGameCornerPrizes[] = {
    { ITEM_SILK_SCARF, 1000 },
    { ITEM_WIDE_LENS, 1000 },
    { ITEM_ZOOM_LENS, 1000 },
    { ITEM_METRONOME, 1000 },
    { ITEM_TM90, 2000 },
    { ITEM_TM58, 2000 },
    { ITEM_TM75, 4000 },
    { ITEM_TM32, 4000 },
    { ITEM_TM44, 6000 },
    { ITEM_TM89, 6000 },
    { ITEM_TM10, 6000 },
    { ITEM_TM27, 8000 },
    { ITEM_TM21, 8000 },
    { ITEM_TM35, 10000 },
    { ITEM_TM24, 10000 },
    { ITEM_TM13, 10000 },
    { ITEM_TM29, 10000 },
    { ITEM_TM74, 15000 },
    { ITEM_TM68, 20000 },
};
// place_rewards.py: Game Corner prizes (end)

// The prize at index, and its coin price. Platinum Oxide: a TM the counter
// sells once reads as ITEM_NONE until the player has its badges and after it
// is bought, and the prize script leaves it off the menu.
BOOL ScrCmd_GetGameCornerPrizeData(ScriptContext *ctx)
{
    u16 index = ScriptContext_GetVar(ctx);
    u16 *item = ScriptContext_GetVarPointer(ctx);
    u16 *price = ScriptContext_GetVarPointer(ctx);

    if (index >= NELEMS(sGameCornerPrizes)) {
        *item = ITEM_NONE;
        *price = 0;
        return FALSE;
    }

    *item = sGameCornerPrizes[index].item;
    *price = sGameCornerPrizes[index].price;

    if (SoldTMs_IsOffered(ctx->fieldSystem->saveData, *item) == FALSE) {
        *item = ITEM_NONE;
    }

    return FALSE;
}

// Platinum Oxide: how many prizes the list has, which the prize script used
// to write as a number.
BOOL ScrCmd_GetGameCornerPrizeCount(ScriptContext *ctx)
{
    u16 *count = ScriptContext_GetVarPointer(ctx);

    *count = NELEMS(sGameCornerPrizes);
    return FALSE;
}

// Platinum Oxide: how many of an item one purchase gives (a sold TM's
// copies, or one).
BOOL ScrCmd_GetSoldTMCopies(ScriptContext *ctx)
{
    u16 item = ScriptContext_GetVar(ctx);
    u16 *copies = ScriptContext_GetVarPointer(ctx);

    *copies = SoldTMs_Copies(item);
    return FALSE;
}

// Platinum Oxide: records that a sold TM has been bought, so no counter
// offers it again.
BOOL ScrCmd_MarkSoldTMBought(ScriptContext *ctx)
{
    u16 item = ScriptContext_GetVar(ctx);

    SoldTMs_MarkBought(ctx->fieldSystem->saveData, item);
    return FALSE;
}

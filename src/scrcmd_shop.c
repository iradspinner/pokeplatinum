#include "scrcmd_shop.h"

#include <nitro.h>
#include <string.h>

#include "constants/savedata/vars_flags.h"
#include "generated/badges.h"
#include "generated/mart_decor_id.h"
#include "generated/mart_frontier_id.h"
#include "generated/mart_seal_id.h"
#include "generated/mart_specialties_id.h"

#include "data/mart_items.h"
#include "data/sold_tms.h"
#include "overlay007/shop_menu.h"

#include "field_script_context.h"
#include "inlines.h"
#include "save_player.h"
#include "trainer_info.h"
#include "unk_0203D1B8.h"
#include "vars_flags.h"

// Platinum Oxide: the TMs sold once, from a badge count (Ian, 2026-10-06;
// include/data/sold_tms.h). A purchase sets the TM's bit in one of two saved
// variables that vanilla left unused, so no save layout moves.
const SoldTM *SoldTMs_Find(u16 item)
{
    for (const SoldTM *tm = sSoldTMs; tm->item != ITEM_NONE; tm++) {
        if (tm->item == item) {
            return tm;
        }
    }

    return NULL;
}

static u16 *SoldTMs_Word(SaveData *saveData, u8 bit)
{
    return VarsFlags_GetVarAddress(SaveData_GetVarsFlags(saveData), bit < 16 ? VAR_SOLD_TMS_0 : VAR_SOLD_TMS_1);
}

// Whether a counter lists the item now: anything not in the table always,
// a sold TM once the player has its badges and until it is bought.
BOOL SoldTMs_IsOffered(SaveData *saveData, u16 item)
{
    const SoldTM *tm = SoldTMs_Find(item);

    if (tm == NULL) {
        return TRUE;
    }

    if (TrainerInfo_BadgeCount(SaveData_GetTrainerInfo(saveData)) < tm->badges) {
        return FALSE;
    }

    return (*SoldTMs_Word(saveData, tm->bit) & (1 << (tm->bit % 16))) == 0;
}

void SoldTMs_MarkBought(SaveData *saveData, u16 item)
{
    const SoldTM *tm = SoldTMs_Find(item);

    if (tm != NULL) {
        *SoldTMs_Word(saveData, tm->bit) |= 1 << (tm->bit % 16);
    }
}

// How many one purchase gives: a sold TM's copies, or one of anything else.
u16 SoldTMs_Copies(u16 item)
{
    const SoldTM *tm = SoldTMs_Find(item);

    return tm != NULL ? tm->copies : 1;
}

BOOL ScrCmd_PokeMartCommon(ScriptContext *ctx)
{
    u16 shopItems[64];
    u8 requiredBadges, badgeNum, i, j;
    u16 unused = ScriptContext_GetVar(ctx);

    i = 0;
    badgeNum = 0;
    requiredBadges = 0;

    for (j = 0; j < MAX_BADGES; j++) {
        if (TrainerInfo_HasBadge(SaveData_GetTrainerInfo(ctx->fieldSystem->saveData), j) == TRUE) {
            badgeNum++;
        }
    }

    switch (badgeNum) {
    case 0:
        requiredBadges = 1;
        break;
    case 1:
    case 2:
        requiredBadges = 2;
        break;
    case 3:
    case 4:
        requiredBadges = 3;
        break;
    case 5:
    case 6:
        requiredBadges = 4;
        break;
    case 7:
        requiredBadges = 5;
        break;
    case 8:
        requiredBadges = 6;
        break;
    default:
        requiredBadges = 1;
        break;
    }

    for (j = 0; j < (NELEMS(PokeMartCommonItems)); j++) {
        if (requiredBadges >= PokeMartCommonItems[j].requiredBadges) {
            shopItems[i] = PokeMartCommonItems[j].itemID;
            i++;
        }
    }

    shopItems[i] = SHOP_ITEM_END;

    Shop_Start(ctx->task, ctx->fieldSystem, shopItems, MART_TYPE_NORMAL, FALSE);
    return TRUE;
}

BOOL ScrCmd_PokeMartSpecialties(ScriptContext *ctx)
{
    u16 martID = ScriptContext_GetVar(ctx);
    BOOL incBuyCount;
    u16 shopItems[64];
    const u16 *stock = PokeMartSpecialties[martID];
    u16 i, count = 0;

    // Platinum Oxide: a sold TM is listed only once the player has its
    // badges, and only until it is bought; anything else is always listed.
    for (i = 0; stock[i] != SHOP_ITEM_END && count < NELEMS(shopItems) - 1; i++) {
        if (SoldTMs_IsOffered(ctx->fieldSystem->saveData, stock[i])) {
            shopItems[count++] = stock[i];
        }
    }

    shopItems[count] = SHOP_ITEM_END;

    if ((martID == MART_SPECIALTIES_ID_VEILSTONE_1F_RIGHT) || (martID == MART_SPECIALTIES_ID_VEILSTONE_1F_LEFT)
        || (martID == MART_SPECIALTIES_ID_VEILSTONE_2F_UP) || (martID == MART_SPECIALTIES_ID_VEILSTONE_2F_MID)
        || (martID == MART_SPECIALTIES_ID_VEILSTONE_3F_UP) || (martID == MART_SPECIALTIES_ID_VEILSTONE_3F_DOWN)
        || (martID == MART_SPECIALTIES_ID_VEILSTONE_B1F)) {
        incBuyCount = TRUE;
    } else {
        incBuyCount = FALSE;
    }

    Shop_Start(ctx->task, ctx->fieldSystem, shopItems, MART_TYPE_NORMAL, incBuyCount);
    return TRUE;
}

// Veilstone
BOOL ScrCmd_PokeMartDecor(ScriptContext *ctx)
{
    u16 martID = ScriptContext_GetVar(ctx);
    BOOL incBuyCount;

    if ((martID == MART_DECOR_ID_VEILSTONE_4F_UP) || (martID == MART_DECOR_ID_VEILSTONE_4F_DOWN)) {
        incBuyCount = TRUE;
    } else {
        // never reached as the only two instances of this command only ever sets the
        // martID to either MART_DECOR_ID_VEILSTONE_4F_UP or MART_DECOR_ID_VEILSTONE_4F_DOWN
        // respectively.
        incBuyCount = FALSE;
    }

    Shop_Start(ctx->task, ctx->fieldSystem, (u16 *)VeilstoneDeptStoreDecorationStocks[martID], MART_TYPE_DECOR, incBuyCount);
    return TRUE;
}

// Sunyshore
BOOL ScrCmd_PokeMartSeal(ScriptContext *ctx)
{
    u16 martID = ScriptContext_GetVar(ctx);

    Shop_Start(ctx->task, ctx->fieldSystem, (u16 *)SunyshoreMarketDailyStocks[martID], MART_TYPE_SEAL, FALSE);
    return TRUE;
}

BOOL ScrCmd_ShowAccessoryShop(ScriptContext *ctx)
{
    AccessoryShop_Init(ctx->fieldSystem->task);
    return TRUE;
}

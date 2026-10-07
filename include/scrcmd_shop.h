#ifndef POKEPLATINUM_SCRCMD_SHOP_H
#define POKEPLATINUM_SCRCMD_SHOP_H

#include "field_script_context.h"
#include "savedata.h"

// Platinum Oxide: a TM a counter sells once, from a badge count
// (include/data/sold_tms.h). copies is how many one purchase gives; bit is
// its bit in VAR_SOLD_TMS_0 (0 to 15) and VAR_SOLD_TMS_1 (16 to 31).
typedef struct SoldTM {
    u16 item;
    u8 badges;
    u8 copies;
    u8 bit;
} SoldTM;

const SoldTM *SoldTMs_Find(u16 item);
BOOL SoldTMs_IsOffered(SaveData *saveData, u16 item);
void SoldTMs_MarkBought(SaveData *saveData, u16 item);
u16 SoldTMs_Copies(u16 item);

BOOL ScrCmd_PokeMartCommon(ScriptContext *ctx);
BOOL ScrCmd_PokeMartSpecialties(ScriptContext *ctx);
BOOL ScrCmd_PokeMartDecor(ScriptContext *ctx);
BOOL ScrCmd_PokeMartSeal(ScriptContext *ctx);
BOOL ScrCmd_ShowAccessoryShop(ScriptContext *ctx);

#endif // POKEPLATINUM_SCRCMD_SHOP_H

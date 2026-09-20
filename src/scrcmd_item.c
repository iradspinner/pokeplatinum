#include "scrcmd_item.h"

#include <nitro.h>
#include <string.h>

#include "constants/heap.h"

#include "field/field_system.h"

#include "bag.h"
#include "field_script_context.h"
#include "inlines.h"
#include "item.h"
#include "special_encounter.h"
#include "unk_0205DFC4.h"

BOOL ScrCmd_AddItem(ScriptContext *ctx)
{
    FieldSystem *fieldSystem = ctx->fieldSystem;
    u16 item = ScriptContext_GetVar(ctx);
    u16 count = ScriptContext_GetVar(ctx);
    u16 *destVar = ScriptContext_GetVarPointer(ctx);

    *destVar = Bag_TryAddItem(SaveData_GetBag(fieldSystem->saveData), item, count, HEAP_ID_FIELD1);
    return FALSE;
}

BOOL ScrCmd_RemoveItem(ScriptContext *ctx)
{
    FieldSystem *fieldSystem = ctx->fieldSystem;
    u16 item = ScriptContext_GetVar(ctx);
    u16 count = ScriptContext_GetVar(ctx);
    u16 *destVar = ScriptContext_GetVarPointer(ctx);

    *destVar = Bag_TryRemoveItem(SaveData_GetBag(fieldSystem->saveData), item, count, HEAP_ID_FIELD1);
    return FALSE;
}

BOOL ScrCmd_CanFitItem(ScriptContext *ctx)
{
    FieldSystem *fieldSystem = ctx->fieldSystem;
    u16 item = ScriptContext_GetVar(ctx);
    u16 count = ScriptContext_GetVar(ctx);
    u16 *destVar = ScriptContext_GetVarPointer(ctx);

    *destVar = Bag_CanFitItem(SaveData_GetBag(fieldSystem->saveData), item, count, HEAP_ID_FIELD1);
    return FALSE;
}

BOOL ScrCmd_CheckItem(ScriptContext *ctx)
{
    FieldSystem *fieldSystem = ctx->fieldSystem;
    u16 item = ScriptContext_GetVar(ctx);
    u16 count = ScriptContext_GetVar(ctx);
    u16 *destVar = ScriptContext_GetVarPointer(ctx);

    *destVar = Bag_CanRemoveItem(SaveData_GetBag(fieldSystem->saveData), item, count, HEAP_ID_FIELD2);
    return FALSE;
}

BOOL ScrCmd_GetItemQuantity(ScriptContext *ctx)
{
    FieldSystem *fieldSystem = ctx->fieldSystem;
    u16 item = ScriptContext_GetVar(ctx);
    u16 *destVar = ScriptContext_GetVarPointer(ctx);

    *destVar = Bag_GetItemQuantity(SaveData_GetBag(fieldSystem->saveData), item, HEAP_ID_FIELD2);
    return FALSE;
}

BOOL ScrCmd_IsItemTMHM(ScriptContext *ctx)
{
    FieldSystem *fieldSystem = ctx->fieldSystem;
    u16 item = ScriptContext_GetVar(ctx);
    u16 *destVar = ScriptContext_GetVarPointer(ctx);

    *destVar = Item_IsTMHM(item);
    return FALSE;
}

BOOL ScrCmd_GetItemPocket(ScriptContext *ctx)
{
    FieldSystem *fieldSystem = ctx->fieldSystem;
    u16 item = ScriptContext_GetVar(ctx);
    u16 *pocket = ScriptContext_GetVarPointer(ctx);

    *pocket = (u16)Item_LoadParam(item, ITEM_PARAM_FIELD_POCKET, HEAP_ID_FIELD2);
    return FALSE;
}

BOOL ScrCmd_Dummy081(ScriptContext *ctx)
{
    return FALSE;
}

BOOL ScrCmd_Dummy082(ScriptContext *ctx)
{
    return FALSE;
}

// Platinum Oxide: the base ROM's "Repel's effect wore off, use another one?"
// prompt needs to set the step counter from a script. It did that by poking a
// fixed scratch address with ScrCmd_Unused_007 and then running a hand-written
// routine, in place of ScrCmd_Dummy088, to copy that byte through the save
// pointer, because a script command can only write to a fixed address. Here the
// command just takes the count.
BOOL ScrCmd_SetRepelSteps(ScriptContext *ctx)
{
    FieldSystem *fieldSystem = ctx->fieldSystem;
    u16 steps = ScriptContext_GetVar(ctx);

    SpecialEncounter *speEnc = SaveData_GetSpecialEncounters(fieldSystem->saveData);
    *SpecialEncounter_GetRepelSteps(speEnc) = (u8)steps;

    return FALSE;
}

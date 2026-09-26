#include "palette.h"

#include <nitro.h>
#include <string.h>

#include "constants/heap.h"

#include "graphics.h"
#include "hardware_palette.h"
#include "heap.h"
#include "sys_task.h"
#include "sys_task_manager.h"

static u8 IsMaskedOn(u16 mask, u16 bit);
static void FlagFadedPaletteBuffer(PaletteData *paletteData, u16 bufferID);
static void FilterMaskToValidPalettes(int bufferID, PaletteBuffer *buffer, u16 *outMask);
static void SetTimedFadeParams(PaletteFadeControl *fade, u16 unfadedMask, s8 wait, u8 cur, u8 end, u16 target);
static void WaitAndApplyBlendStepToStdPaletteBuffers(PaletteData *paletteData);
static void WaitAndApplyBlendStepToExtPaletteBuffers(PaletteData *paletteData);
static void WaitAndApplyBlendStepToPaletteBuffer(PaletteData *paletteData, u16 bufferID, u16 paletteSize);
static void ApplyBlendStepToPaletteBuffer(PaletteData *paletteData, u16 bufferID, u16 paletteSize);
static void ApplyBlendStepToSinglePalette(u16 *unfaded, u16 *faded, PaletteFadeControl *fade, u32 paletteSize);
static void UpdateFadeBlendStep(PaletteData *paletteData, u8 bufferID, PaletteFadeControl *fade);

static void SysTask_FadePalette(SysTask *task, void *data);

PaletteData *PaletteData_New(enum HeapID heapID)
{
    PaletteData *paletteData = Heap_Alloc(heapID, sizeof(PaletteData));
    MI_CpuClear8(paletteData, sizeof(PaletteData));

    return paletteData;
}

void PaletteData_Free(PaletteData *paletteData)
{
    Heap_Free(paletteData);
}

void PaletteData_InitBuffer(PaletteData *paletteData, enum PaletteBufferID bufferID, void *unfaded, void *faded, u32 size)
{
    paletteData->buffers[bufferID].unfaded = (u16 *)unfaded;
    paletteData->buffers[bufferID].faded = (u16 *)faded;
    paletteData->buffers[bufferID].size = size;
}

void PaletteData_AllocBuffer(PaletteData *paletteData, enum PaletteBufferID bufferID, u32 size, enum HeapID heapID)
{
    void *unfaded = Heap_Alloc(heapID, size);
    void *faded = Heap_Alloc(heapID, size);
    PaletteData_InitBuffer(paletteData, bufferID, unfaded, faded, size);
}

void PaletteData_FreeBuffer(PaletteData *paletteData, enum PaletteBufferID bufferID)
{
    Heap_Free(paletteData->buffers[bufferID].unfaded);
    Heap_Free(paletteData->buffers[bufferID].faded);
}

void PaletteData_LoadBuffer(PaletteData *paletteData, const void *src, enum PaletteBufferID bufferID, u16 destStart, u16 srcSize)
{
    MI_CpuCopy16(src, paletteData->buffers[bufferID].unfaded + destStart, srcSize);
    MI_CpuCopy16(src, paletteData->buffers[bufferID].faded + destStart, srcSize);
}

void PaletteData_LoadBufferFromFile(PaletteData *paletteData, enum NarcID narcID, u32 narcMemberIdx, enum HeapID heapID, enum PaletteBufferID bufferID, u32 srcSize, u16 destStart, u16 srcStart)
{
    NNSG2dPaletteData *palette;
    void *ptr = Graphics_GetPlttData(narcID, narcMemberIdx, &palette, heapID);

    GF_ASSERT(ptr != NULL);

    if (srcSize == 0) {
        srcSize = palette->szByte;
    }

    GF_ASSERT(destStart * sizeof(destStart) + srcSize <= paletteData->buffers[bufferID].size);

    PaletteData_LoadBuffer(paletteData, (u16 *)palette->pRawData + srcStart, bufferID, destStart, srcSize);
    Heap_Free(ptr);
}

void PaletteData_LoadBufferFromFileStart(PaletteData *paletteData, enum NarcID narcID, u32 narcMemberIdx, enum HeapID heapID, enum PaletteBufferID bufferID, u32 srcSize, u16 destStart)
{
    PaletteData_LoadBufferFromFile(paletteData, narcID, narcMemberIdx, heapID, bufferID, srcSize, destStart, 0);
}

void PaletteData_LoadBufferFromHardware(PaletteData *paletteData, enum PaletteBufferID bufferID, u16 start, u32 size)
{
    GF_ASSERT(start * sizeof(start) + size <= paletteData->buffers[bufferID].size);

    u16 *ptr;
    switch (bufferID) {
    case PLTTBUF_MAIN_BG:
        ptr = GetHardwareMainBgPaletteAddress();
        break;

    case PLTTBUF_SUB_BG:
        ptr = GetHardwareSubBgPaletteAddress();
        break;

    case PLTTBUF_MAIN_OBJ:
        ptr = GetHardwareMainObjPaletteAddress();
        break;

    case PLTTBUF_SUB_OBJ:
        ptr = GetHardwareSubObjPaletteAddress();
        break;

    default:
        GF_ASSERT(FALSE);
        return;
    }

    PaletteData_LoadBuffer(paletteData, ptr + start, bufferID, start, size);
}

void LoadPaletteFromFile(enum NarcID narcID, u32 narcMemberIdx, enum HeapID heapID, u32 size, u16 start, void *dest)
{
    NNSG2dPaletteData *palette;
    void *ptr = Graphics_GetPlttData(narcID, narcMemberIdx, &palette, heapID);

    GF_ASSERT(ptr != NULL);

    if (size == 0) {
        size = palette->szByte;
    }

    MI_CpuCopy16((u16 *)palette->pRawData + start, dest, size);
    Heap_Free(ptr);
}

void PaletteData_CopyBuffer(PaletteData *palette, enum PaletteBufferID srcBufferID, u16 srcStart, enum PaletteBufferID destBufferID, u16 destStart, u16 size)
{
    MI_CpuCopy16(palette->buffers[srcBufferID].unfaded + srcStart, palette->buffers[destBufferID].unfaded + destStart, size);
    MI_CpuCopy16(palette->buffers[srcBufferID].unfaded + srcStart, palette->buffers[destBufferID].faded + destStart, size);
}

u16 *PaletteData_GetUnfadedBuffer(PaletteData *palette, enum PaletteBufferID bufferID)
{
    return palette->buffers[bufferID].unfaded;
}

u16 *PaletteData_GetFadedBuffer(PaletteData *palette, enum PaletteBufferID bufferID)
{
    return palette->buffers[bufferID].faded;
}

u8 PaletteData_StartFade(PaletteData *paletteData, u16 buffersToFade, u16 palettesToFade, s8 wait, u8 cur, u8 end, u16 target)
{
    u16 inPalettesToFade = palettesToFade;
    u8 palettesFaded = FALSE;
    u8 bufferID;

    for (bufferID = PLTTBUF_MAIN_BG; bufferID < PLTTBUF_MAX; bufferID++) {
        if (IsMaskedOn(buffersToFade, bufferID) == TRUE && !IsMaskedOn(paletteData->selectedBuffers, bufferID)) {
            FilterMaskToValidPalettes(bufferID, &paletteData->buffers[bufferID], &palettesToFade);
            SetTimedFadeParams(&paletteData->buffers[bufferID].selected, palettesToFade, wait, cur, end, target);
            FlagFadedPaletteBuffer(paletteData, bufferID);

            if (bufferID >= PLTTBUF_EX_BEGIN) {
                ApplyBlendStepToPaletteBuffer(paletteData, bufferID, PALETTE_SIZE_EXT);
            } else {
                ApplyBlendStepToPaletteBuffer(paletteData, bufferID, PALETTE_SIZE);
            }

            palettesToFade = inPalettesToFade;
            palettesFaded = TRUE;
        }
    }

    if (palettesFaded == TRUE) {
        paletteData->selectedBuffers |= buffersToFade;

        if (paletteData->fadeInProgress == FALSE) {
            paletteData->fadeInProgress = TRUE;
            paletteData->selectedFlag = TRUE;
            paletteData->forceExit = FALSE;

            SysTask_Start(SysTask_FadePalette, paletteData, 0xFFFFFFFE);
        }
    }

    return palettesFaded;
}

static u8 IsMaskedOn(u16 mask, u16 bit)
{
    return (mask & (1 << bit)) != 0;
}

static void FlagFadedPaletteBuffer(PaletteData *paletteData, u16 bufferID)
{
    if (IsMaskedOn(paletteData->fadedBuffers, bufferID) != TRUE) {
        paletteData->fadedBuffers |= (1 << bufferID);
    }
}

static void FilterMaskToValidPalettes(int bufferID, PaletteBuffer *buffer, u16 *outMask)
{
    u8 singlePaletteSize;
    if (bufferID < PLTTBUF_EX_BEGIN) {
        singlePaletteSize = buffer->size / (PALETTE_SIZE * 2);
    } else {
        singlePaletteSize = buffer->size / (PALETTE_SIZE_EXT * 2);
    }

    u16 validPalettesMask = 0;
    for (u8 i = 0; i < singlePaletteSize; i++) {
        validPalettesMask += (1 << i);
    }

    *outMask &= validPalettesMask;
}

static void SetTimedFadeParams(PaletteFadeControl *fade, u16 unfadedMask, s8 wait, u8 cur, u8 end, u16 target)
{
    if (wait < 0) {
        fade->step = 2 + abs(wait);
        fade->wait = 0;
    } else {
        fade->step = 2;
        fade->wait = wait;
    }

    fade->unfadedMask = unfadedMask;
    fade->cur = cur;
    fade->end = end;
    fade->target = target;
    fade->waitStep = fade->wait;

    if (cur < end) {
        fade->sign = 0;
    } else {
        fade->sign = 1;
    }
}

static void SysTask_FadePalette(SysTask *task, void *data)
{
    PaletteData *paletteData = data;

    if (paletteData->forceExit == TRUE) {
        paletteData->forceExit = FALSE;
        paletteData->fadedBuffers = 0;
        paletteData->selectedBuffers = 0;
        paletteData->fadeInProgress = FALSE;
        SysTask_Done(task);
        return;
    }

    if (paletteData->selectedFlag != TRUE) {
        return;
    }

    paletteData->fadedBuffers = paletteData->selectedBuffers;

    WaitAndApplyBlendStepToStdPaletteBuffers(paletteData);
    WaitAndApplyBlendStepToExtPaletteBuffers(paletteData);

    if (paletteData->selectedBuffers == 0) {
        paletteData->fadeInProgress = FALSE;
        SysTask_Done(task);
    }
}

static void WaitAndApplyBlendStepToStdPaletteBuffers(PaletteData *paletteData)
{
    for (u8 i = PLTTBUF_MAIN_BG; i < PLTTBUF_EX_BEGIN; i++) {
        WaitAndApplyBlendStepToPaletteBuffer(paletteData, i, PALETTE_SIZE);
    }
}

static void WaitAndApplyBlendStepToExtPaletteBuffers(PaletteData *paletteData)
{
    for (u8 i = PLTTBUF_EX_BEGIN; i < PLTTBUF_MAX; i++) {
        WaitAndApplyBlendStepToPaletteBuffer(paletteData, i, PALETTE_SIZE_EXT);
    }
}

static void WaitAndApplyBlendStepToPaletteBuffer(PaletteData *paletteData, u16 bufferID, u16 paletteSize)
{
    if (!IsMaskedOn(paletteData->selectedBuffers, bufferID)) {
        return;
    }

    if (paletteData->buffers[bufferID].selected.waitStep < paletteData->buffers[bufferID].selected.wait) {
        paletteData->buffers[bufferID].selected.waitStep++;
        return;
    }

    paletteData->buffers[bufferID].selected.waitStep = 0;
    ApplyBlendStepToPaletteBuffer(paletteData, bufferID, paletteSize);
}

static void ApplyBlendStepToPaletteBuffer(PaletteData *paletteData, u16 bufferID, u16 paletteSize)
{
    for (u32 i = 0; i < SLOTS_PER_PALETTE; i++) {
        if (!IsMaskedOn(paletteData->buffers[bufferID].selected.unfadedMask, i)) {
            continue;
        }

        ApplyBlendStepToSinglePalette(&paletteData->buffers[bufferID].unfaded[i * paletteSize], &paletteData->buffers[bufferID].faded[i * paletteSize], &paletteData->buffers[bufferID].selected, paletteSize);
    }

    UpdateFadeBlendStep(paletteData, bufferID, &paletteData->buffers[bufferID].selected);
}

static void ApplyBlendStepToSinglePalette(u16 *unfaded, u16 *faded, PaletteFadeControl *fade, u32 paletteSize)
{
    u32 i;
    u8 r, g, b;

    for (i = 0; i < paletteSize; i++) {
        r = BlendColor(ColorR(unfaded[i]), ColorR(fade->target), fade->cur);
        g = BlendColor(ColorG(unfaded[i]), ColorG(fade->target), fade->cur);
        b = BlendColor(ColorB(unfaded[i]), ColorB(fade->target), fade->cur);

        faded[i] = RGB(r, g, b);
    }
}

static void UpdateFadeBlendStep(PaletteData *paletteData, u8 bufferID, PaletteFadeControl *fade)
{
    s16 next;

    if (fade->cur == fade->end) {
        if (paletteData->selectedBuffers & (1 << bufferID)) {
            paletteData->selectedBuffers ^= (1 << bufferID);
        }
    } else if (fade->sign == 0) {
        next = fade->cur;
        next += fade->step;

        if (next > fade->end) {
            next = fade->end;
        }

        fade->cur = next;
    } else {
        next = fade->cur;
        next -= fade->step;

        if (next < fade->end) {
            next = fade->end;
        }

        fade->cur = next;
    }
}

void PaletteData_CommitFadedBuffers(PaletteData *paletteData)
{
    if (paletteData->autoTransparent == FALSE && paletteData->selectedFlag != TRUE) {
        return;
    }

    for (int bufferID = PLTTBUF_MAIN_BG; bufferID < PLTTBUF_MAX; bufferID++) {
        if (paletteData->autoTransparent == 0) {
            if ((paletteData->buffers[bufferID].faded == NULL) || (IsMaskedOn(paletteData->fadedBuffers, bufferID) == 0)) {
                continue;
            }
        }

        DC_FlushRange(paletteData->buffers[bufferID].faded, paletteData->buffers[bufferID].size);

        switch (bufferID) {
        case PLTTBUF_MAIN_BG:
            GX_LoadBGPltt(paletteData->buffers[bufferID].faded, 0, paletteData->buffers[bufferID].size);
            break;

        case PLTTBUF_SUB_BG:
            GXS_LoadBGPltt(paletteData->buffers[bufferID].faded, 0, paletteData->buffers[bufferID].size);
            break;

        case PLTTBUF_MAIN_OBJ:
            GX_LoadOBJPltt(paletteData->buffers[bufferID].faded, 0, paletteData->buffers[bufferID].size);
            break;

        case PLTTBUF_SUB_OBJ:
            GXS_LoadOBJPltt(paletteData->buffers[bufferID].faded, 0, paletteData->buffers[bufferID].size);
            break;

        case PLTTBUF_MAIN_EX_BG_0:
            GX_BeginLoadBGExtPltt();
            GX_LoadBGExtPltt(paletteData->buffers[bufferID].faded, 0x0, paletteData->buffers[bufferID].size);
            GX_EndLoadBGExtPltt();
            break;

        case PLTTBUF_MAIN_EX_BG_1:
            GX_BeginLoadBGExtPltt();
            GX_LoadBGExtPltt(paletteData->buffers[bufferID].faded, 0x2000, paletteData->buffers[bufferID].size);
            GX_EndLoadBGExtPltt();
            break;

        case PLTTBUF_MAIN_EX_BG_2:
            GX_BeginLoadBGExtPltt();
            GX_LoadBGExtPltt(paletteData->buffers[bufferID].faded, 0x4000, paletteData->buffers[bufferID].size);
            GX_EndLoadBGExtPltt();
            break;

        case PLTTBUF_MAIN_EX_BG_3:
            GX_BeginLoadBGExtPltt();
            GX_LoadBGExtPltt((const void *)paletteData->buffers[bufferID].faded, 0x6000, paletteData->buffers[bufferID].size);
            GX_EndLoadBGExtPltt();
            break;

        case PLTTBUF_SUB_EX_BG_0:
            GXS_BeginLoadBGExtPltt();
            GXS_LoadBGExtPltt((const void *)paletteData->buffers[bufferID].faded, 0x0, paletteData->buffers[bufferID].size);
            GXS_EndLoadBGExtPltt();
            break;

        case PLTTBUF_SUB_EX_BG_1:
            GXS_BeginLoadBGExtPltt();
            GXS_LoadBGExtPltt((const void *)paletteData->buffers[bufferID].faded, 0x2000, paletteData->buffers[bufferID].size);
            GXS_EndLoadBGExtPltt();
            break;

        case PLTTBUF_SUB_EX_BG_2:
            GXS_BeginLoadBGExtPltt();
            GXS_LoadBGExtPltt((const void *)paletteData->buffers[bufferID].faded, 0x4000, paletteData->buffers[bufferID].size);
            GXS_EndLoadBGExtPltt();
            break;

        case PLTTBUF_SUB_EX_BG_3:
            GXS_BeginLoadBGExtPltt();
            GXS_LoadBGExtPltt((const void *)paletteData->buffers[bufferID].faded, 0x6000, paletteData->buffers[bufferID].size);
            GXS_EndLoadBGExtPltt();
            break;

        case PLTTBUF_MAIN_EX_OBJ:
            GX_BeginLoadOBJExtPltt();
            GX_LoadOBJExtPltt((const void *)paletteData->buffers[bufferID].faded, 0, paletteData->buffers[bufferID].size);
            GX_EndLoadOBJExtPltt();
            break;

        case PLTTBUF_SUB_EX_OBJ:
            GXS_BeginLoadOBJExtPltt();
            GXS_LoadOBJExtPltt((const void *)paletteData->buffers[bufferID].faded, 0, paletteData->buffers[bufferID].size);
            GXS_EndLoadOBJExtPltt();
        }
    }

    paletteData->fadedBuffers = paletteData->selectedBuffers;

    if (paletteData->fadedBuffers == 0) {
        paletteData->selectedFlag = 0;
    }
}

u16 PaletteData_GetSelectedBuffersMask(PaletteData *paletteData)
{
    return paletteData->selectedBuffers;
}

void PaletteData_SetAutoTransparent(PaletteData *paletteData, BOOL val)
{
    paletteData->autoTransparent = val;
}

void PaletteData_SelectAll(PaletteData *paletteData, u8 val)
{
    paletteData->selectedFlag = val & 1;
    paletteData->selectedBuffers = PLTTBUF_ALL_F;
}

void PaletteData_FillBufferRange(PaletteData *paletteData, enum PaletteBufferID bufferID, enum PaletteSelector selector, u16 fillVal, u16 start, u16 end)
{
    GF_ASSERT(end * sizeof(u16) <= paletteData->buffers[bufferID].size);

    if (selector == PLTTSEL_UNFADED || selector == PLTTSEL_BOTH) {
        MI_CpuFill16(&paletteData->buffers[bufferID].unfaded[start], fillVal, (end - start) * 2);
    }

    if (selector == PLTTSEL_FADED || selector == PLTTSEL_BOTH) {
        MI_CpuFill16(&paletteData->buffers[bufferID].faded[start], fillVal, (end - start) * 2);
    }
}

u16 PaletteData_GetBufferIndexColor(PaletteData *paletteData, enum PaletteBufferID bufferID, enum PaletteSelector selector, u16 index)
{
    if (selector == PLTTSEL_UNFADED) {
        return paletteData->buffers[bufferID].unfaded[index];
    }

    if (selector == PLTTSEL_FADED) {
        return paletteData->buffers[bufferID].faded[index];
    }

    GF_ASSERT(FALSE);
    return 0;
}

void BlendPalette(const u16 *src, u16 *dest, u16 size, u8 fraction, u16 target)
{
    u16 i;
    int srcR, srcG, srcB;
    int targetR = ((RgbColor *)&target)->r;
    int targetG = ((RgbColor *)&target)->g;
    int targetB = ((RgbColor *)&target)->b;

    for (i = 0; i < size; i++) {
        srcR = ((RgbColor *)&src[i])->r;
        srcG = ((RgbColor *)&src[i])->g;
        srcB = ((RgbColor *)&src[i])->b;

        dest[i] = BlendColor(srcR, targetR, fraction) | (BlendColor(srcG, targetG, fraction) << 5) | (BlendColor(srcB, targetB, fraction) << 10);
    }
}

void PaletteData_Blend(PaletteData *paletteData, enum PaletteBufferID bufferID, u16 index, u16 size, u8 fraction, u16 target)
{
    GF_ASSERT(paletteData->buffers[bufferID].unfaded != NULL && paletteData->buffers[bufferID].faded != NULL);
    BlendPalette(&paletteData->buffers[bufferID].unfaded[index], &paletteData->buffers[bufferID].faded[index], size, fraction, target);
}

void BlendPalettes(const u16 *sources, u16 *dests, u16 toBlend, u8 fraction, u16 target)
{
    int index = 0;
    while (toBlend) {
        if (toBlend & 1) {
            BlendPalette(&sources[index], &dests[index], SLOTS_PER_PALETTE, fraction, target);
        }

        toBlend >>= 1;
        index += SLOTS_PER_PALETTE;
    }
}

void PaletteData_BlendMulti(PaletteData *paletteData, enum PaletteBufferID bufferID, u16 toBlend, u8 fraction, u16 target)
{
    int index = 0;

    GF_ASSERT(paletteData->buffers[bufferID].unfaded != NULL && paletteData->buffers[bufferID].faded != NULL);

    while (toBlend) {
        if (toBlend & 1) {
            PaletteData_Blend(paletteData, bufferID, index, SLOTS_PER_PALETTE, fraction, target);
        }

        toBlend >>= 1;
        index += SLOTS_PER_PALETTE;
    }
}

void TintPalette(u16 *palette, int numColorsToTint, int tintR, int tintG, int tintB)
{
    int i, r, g, b;
    u32 gray;

    for (i = 0; i < numColorsToTint; i++) {
        r = ColorR(*palette);
        g = ColorG(*palette);
        b = ColorB(*palette);

        // 0.3 red + 0.59 g + 0.1133 b
        gray = (76 * r + 151 * g + 29 * b) >> 8;

        r = (u16)(tintR * gray) >> 8;
        g = (u16)(tintG * gray) >> 8;
        b = (u16)(tintB * gray) >> 8;

        if (r > 31) {
            r = 31;
        }

        if (g > 31) {
            g = 31;
        }

        if (b > 31) {
            b = 31;
        }

        *palette = RGB(r, g, b);
        palette++;
    }
}

// Platinum Oxide: the base ROM's colour variation (Ian, 2026-09-27). Each
// Pokemon's sprite palette is turned round the grey axis by one of 32 steps of
// up to about 20 degrees, in the direction and by the step its personality
// picks. The table, constants and rounding are the base ROM's own, checked
// against its code on 2,560 palettes, so a Pokemon looks as it did there.
// Cosines then sines, 1.0 = 0x400.
static const u16 sHueShiftCosSin[64] = {
    0x400, 0x3FF, 0x3FF, 0x3FF, 0x3FE, 0x3FE, 0x3FD, 0x3FC, 0x3FB, 0x3FA, 0x3F9,
    0x3F8, 0x3F6, 0x3F5, 0x3F3, 0x3F1, 0x3EF, 0x3ED, 0x3EB, 0x3E8, 0x3E6, 0x3E3,
    0x3E0, 0x3DD, 0x3DA, 0x3D7, 0x3D4, 0x3D1, 0x3CD, 0x3C9, 0x3C6, 0x3C2,
    0x000, 0x00B, 0x017, 0x022, 0x02E, 0x039, 0x045, 0x050, 0x05C, 0x067, 0x073,
    0x07E, 0x089, 0x095, 0x0A0, 0x0AC, 0x0B7, 0x0C2, 0x0CE, 0x0D9, 0x0E4, 0x0EF,
    0x0FB, 0x106, 0x111, 0x11C, 0x127, 0x132, 0x13D, 0x148, 0x153, 0x15E,
};

// A channel sum in 10-bit fixed point, rounded and held to 0 to 31.
static int HueShift_Channel(int sum)
{
    sum += 1 << 9;

    if (sum < 0) {
        return 0;
    }

    if (sum >= 32 << 10) {
        return 31;
    }

    return sum >> 10;
}

void HueShiftPokemonPalette(u16 *palette, u32 personality)
{
    // Bits 16 to 20 pick the step, bit 21 the direction; step 0 changes nothing.
    int step = (personality >> 16) & 31;
    int cosine = sHueShiftCosSin[step];
    int sine = sHueShiftCosSin[32 + step];

    if ((personality >> 16) & 32) {
        sine = -sine;
    }

    // The hue-rotation matrix: one weight on the diagonal, and two off it that
    // the sine pulls apart; 341 is a third and 591 one over root three.
    int diagonal = ((682 * cosine) >> 10) + 341;
    int across = (341 * (1024 - cosine)) >> 10;
    int twist = (591 * sine) >> 10;
    int behind = across - twist;
    int ahead = across + twist;

    // Colour 0 is the transparent one and is left alone.
    for (int i = 1; i < SLOTS_PER_PALETTE; i++) {
        int r = ColorR(palette[i]) << 10;
        int g = ColorG(palette[i]) << 10;
        int b = ColorB(palette[i]) << 10;

        int newR = HueShift_Channel(((behind * g) >> 10) + ((diagonal * r) >> 10) + ((ahead * b) >> 10));
        int newG = HueShift_Channel(((diagonal * g) >> 10) + ((ahead * r) >> 10) + ((behind * b) >> 10));
        int newB = HueShift_Channel(((ahead * g) >> 10) + ((behind * r) >> 10) + ((diagonal * b) >> 10));

        palette[i] = RGB(newR, newG, newB);
    }
}

void PaletteData_LoadBufferFromFileStartWithTint(PaletteData *paletteData, enum NarcID narcID, u32 narcMemberIdx, enum HeapID heapID, enum PaletteBufferID bufferID, u32 size, u16 start, int r, int g, int b)
{
    NNSG2dPaletteData *palette;
    void *ptr = Graphics_GetPlttData(narcID, narcMemberIdx, &palette, heapID);

    GF_ASSERT(ptr != NULL);

    if (size == 0) {
        size = palette->szByte;
    }

    TintPalette(palette->pRawData, SLOTS_PER_PALETTE, r, g, b);
    PaletteData_LoadBuffer(paletteData, palette->pRawData, bufferID, start, size);
    Heap_Free(ptr);
}

// Platinum Oxide: a Pokemon palette loaded with the personality's colour
// variation (HueShiftPokemonPalette), for the copies of a Pokemon sprite that
// load their palette apart from the sprite manager.
void PaletteData_LoadBufferFromFileStartWithHueShift(PaletteData *paletteData, enum NarcID narcID, u32 narcMemberIdx, enum HeapID heapID, enum PaletteBufferID bufferID, u32 size, u16 start, u32 personality)
{
    NNSG2dPaletteData *palette;
    void *ptr = Graphics_GetPlttData(narcID, narcMemberIdx, &palette, heapID);

    GF_ASSERT(ptr != NULL);

    if (size == 0) {
        size = palette->szByte;
    }

    if (personality != 0) {
        HueShiftPokemonPalette(palette->pRawData, personality);
    }

    PaletteData_LoadBuffer(paletteData, palette->pRawData, bufferID, start, size);
    Heap_Free(ptr);
}

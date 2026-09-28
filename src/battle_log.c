#include "battle_log.h"

#include <nitro.h>
#include <string.h>

#include "constants/heap.h"
#include "constants/savedata/savedata.h"

#include "savedata/save_table.h"

#include "heap.h"
#include "math_util.h"
#include "party.h"
#include "savedata.h"

// Platinum Oxide: the last 60 trainer battles, for the OxiDex (Ian,
// 2026-09-27; docs/oxide/battle-log.md has the byte layout).
//
// The log lives in RAM in the save image's free tail, after the boxes block,
// which the main save never writes. A battle is added there when it ends, and
// the whole log goes to flash sector 44 of both halves after each save that
// writes the normal block. So a reset without saving drops the log's newest
// battles along with the rest of the unsaved game.
//
// It has its own reader and writer because SaveDataExtra_Get and
// SaveDataExtra_Save also move the main save's own sector state.

#define BATTLE_LOG_MAGIC_0 'O'
#define BATTLE_LOG_MAGIC_1 'B'
#define BATTLE_LOG_MAGIC_2 'L'
#define BATTLE_LOG_MAGIC_3 '1'

#define BATTLE_LOG_CHECKED_SIZE (sizeof(BattleLogHeader) + sizeof(BattleLogRecord) * BATTLE_LOG_CAPACITY)

#define BATTLE_LOG_PRIMARY_ADDRESS (SAVE_SECTOR_SIZE * (BATTLE_LOG_SECTOR + PRIMARY_SECTOR_START))
#define BATTLE_LOG_BACKUP_ADDRESS  (SAVE_SECTOR_SIZE * (BATTLE_LOG_SECTOR + BACKUP_SECTOR_START))

// The bytes "OXBN", read as a little-endian word.
#define OXIDE_BEACON_MAGIC 0x4E42584F

// These fail to compile (the array size goes negative) if the layout drifts
// from the one the OxiDex reads: a 58-byte record and a 0xDB8-byte copy that
// fits in one flash sector.
typedef char BattleLogRecordIs58Bytes[(sizeof(BattleLogRecord) == 58) ? 1 : -1];
typedef char BattleLogIs0xDB8Bytes[(sizeof(BattleLog) == 0xDB8) ? 1 : -1];
typedef char BattleLogFitsASector[(sizeof(BattleLog) <= SAVE_SECTOR_SIZE) ? 1 : -1];

// Found by the live export by its two magic words, so it needs no per-build
// addresses (docs/oxide/battle-log.md, "The RAM beacon").
OxideBeacon gOxideBeacon = {
    OXIDE_BEACON_MAGIC,
    ~OXIDE_BEACON_MAGIC,
    1,
    sizeof(OxideBeacon),
    NULL,
    NULL,
    NULL,
    NULL,
    NULL,
};

static BattleLog *BattleLog_Ptr(SaveData *saveData)
{
    const SaveBlockInfo *last = &saveData->blockInfo[SAVE_BLOCK_ID_MAX - 1];
    u32 offset = (last->offset + last->size + 3) & ~3;

    // The check at boot that the log fits in the free tail. It holds with
    // 0xE00 bytes free; a larger save table would have to move the log.
    GF_ASSERT(offset + sizeof(BattleLog) <= sizeof(saveData->body.data));
    return (BattleLog *)&saveData->body.data[offset];
}

static BOOL BattleLog_HeaderValid(const BattleLog *log)
{
    return log->header.magic[0] == BATTLE_LOG_MAGIC_0
        && log->header.magic[1] == BATTLE_LOG_MAGIC_1
        && log->header.magic[2] == BATTLE_LOG_MAGIC_2
        && log->header.magic[3] == BATTLE_LOG_MAGIC_3
        && log->header.version == BATTLE_LOG_VERSION
        && log->header.recordSize == sizeof(BattleLogRecord)
        && log->header.capacity == BATTLE_LOG_CAPACITY
        && log->header.count <= BATTLE_LOG_CAPACITY
        && log->header.next < BATTLE_LOG_CAPACITY;
}

static BOOL BattleLog_CopyValid(const BattleLog *log)
{
    return BattleLog_HeaderValid(log)
        && log->footer.signature == SECTOR_SIGNATURE
        && log->footer.size == BATTLE_LOG_CHECKED_SIZE
        && log->footer.id == BATTLE_LOG_FOOTER_ID
        && log->footer.checksum == CalcCRC16Checksum(log, BATTLE_LOG_CHECKED_SIZE);
}

static void BattleLog_Init(BattleLog *log)
{
    MI_CpuClear8(log, sizeof(BattleLog));

    log->header.magic[0] = BATTLE_LOG_MAGIC_0;
    log->header.magic[1] = BATTLE_LOG_MAGIC_1;
    log->header.magic[2] = BATTLE_LOG_MAGIC_2;
    log->header.magic[3] = BATTLE_LOG_MAGIC_3;
    log->header.version = BATTLE_LOG_VERSION;
    log->header.recordSize = sizeof(BattleLogRecord);
    log->header.capacity = BATTLE_LOG_CAPACITY;
}

// A new game clears the whole save image, the log's tail with it, so the RAM
// copy is set up again the first time it is needed.
static BattleLog *BattleLog_Get(SaveData *saveData)
{
    BattleLog *log = BattleLog_Ptr(saveData);

    if (BattleLog_HeaderValid(log) == FALSE) {
        BattleLog_Init(log);
    }

    return log;
}

static void BattleLog_PointBeacon(SaveData *saveData)
{
    gOxideBeacon.saveData = saveData;
    gOxideBeacon.party = SaveData_GetParty(saveData);
    gOxideBeacon.pcBoxes = SaveData_GetPCBoxes(saveData);
    gOxideBeacon.battleLog = BattleLog_Ptr(saveData);
}

void BattleLog_Load(SaveData *saveData)
{
    BattleLog *log = BattleLog_Ptr(saveData);
    BattleLog *backup = Heap_AllocAtEnd(HEAP_ID_APPLICATION, sizeof(BattleLog));

    SaveData_CardLoad(BATTLE_LOG_PRIMARY_ADDRESS, log, sizeof(BattleLog));
    SaveData_CardLoad(BATTLE_LOG_BACKUP_ADDRESS, backup, sizeof(BattleLog));

    BOOL primaryValid = BattleLog_CopyValid(log);
    BOOL backupValid = BattleLog_CopyValid(backup);

    // Of two good copies the later one counts. A save made before the log
    // existed has both sectors erased, which reads as an empty log.
    if (backupValid && (primaryValid == FALSE || backup->footer.saveCounter > log->footer.saveCounter)) {
        MI_CpuCopy8(backup, log, sizeof(BattleLog));
    } else if (primaryValid == FALSE) {
        BattleLog_Init(log);
    }

    Heap_Free(backup);
    BattleLog_PointBeacon(saveData);
}

// With no main save to go with it, an old log on the card is not read: the
// game starts with an empty one, which the first save writes over both copies.
void BattleLog_Clear(SaveData *saveData)
{
    BattleLog_Init(BattleLog_Ptr(saveData));
    BattleLog_PointBeacon(saveData);
}

void BattleLog_Write(SaveData *saveData)
{
    BattleLog *log = BattleLog_Get(saveData);

    log->footer.signature = SECTOR_SIGNATURE;
    log->footer.saveCounter++;
    log->footer.size = BATTLE_LOG_CHECKED_SIZE;
    log->footer.id = BATTLE_LOG_FOOTER_ID;
    log->footer.checksum = CalcCRC16Checksum(log, BATTLE_LOG_CHECKED_SIZE);

    // Primary first: if the power goes during it, the backup still holds the
    // log as of the last save.
    SaveData_CardSave(BATTLE_LOG_PRIMARY_ADDRESS, log, sizeof(BattleLog));
    SaveData_CardSave(BATTLE_LOG_BACKUP_ADDRESS, log, sizeof(BattleLog));

    BattleLog_PointBeacon(saveData);
}

void BattleLog_Append(SaveData *saveData, const BattleLogRecord *record)
{
    BattleLog *log = BattleLog_Get(saveData);

    log->records[log->header.next] = *record;
    log->header.next = (log->header.next + 1) % BATTLE_LOG_CAPACITY;

    if (log->header.count < BATTLE_LOG_CAPACITY) {
        log->header.count++;
    }

    BattleLog_PointBeacon(saveData);
}

void BattleLog_SetBattleContext(void *battleContext)
{
    gOxideBeacon.battleContext = battleContext;
}

u8 BattleLog_GetKnockOut(const u8 *packed, int slot)
{
    return (packed[slot / 2] >> ((slot & 1) * 4)) & 0xF;
}

void BattleLog_SetKnockOut(u8 *packed, int slot, u8 value)
{
    int shift = (slot & 1) * 4;
    packed[slot / 2] = (packed[slot / 2] & ~(0xF << shift)) | ((value & 0xF) << shift);
}

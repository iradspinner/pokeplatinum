#ifndef POKEPLATINUM_BATTLE_LOG_H
#define POKEPLATINUM_BATTLE_LOG_H

#include "constants/pokemon.h"

#include "savedata.h"

// Platinum Oxide: the last 60 trainer battles, kept in the save for the
// OxiDex (Ian, 2026-09-27). docs/oxide/battle-log.md has the byte layout,
// which the OxiDex's reader follows; change the two together.

#define BATTLE_LOG_VERSION     1
#define BATTLE_LOG_CAPACITY    60
#define BATTLE_LOG_FOOTER_ID   0x4C42
#define BATTLE_LOG_MAX_FAINTS  16

// Flash sector 44 of each half, which nothing had written before.
#define BATTLE_LOG_SECTOR 44

// Who knocked a Pokemon out, as the 4-bit values the records store. 0 to 5 is
// a slot on the other side.
#define BATTLE_LOG_KO_PARTNER  6
#define BATTLE_LOG_KO_INDIRECT 7
#define BATTLE_LOG_KO_NONE     0xF

#define BATTLE_LOG_FLAG_WON          (1 << 0)
#define BATTLE_LOG_FLAG_LOST         (1 << 1)
#define BATTLE_LOG_FLAG_DOUBLE       (1 << 2)
#define BATTLE_LOG_FLAG_AI_PARTNER   (1 << 3)
#define BATTLE_LOG_FLAG_TWO_TRAINERS (1 << 4)

// An egg is recorded as this, not as SPECIES_EGG, whose id moves whenever a
// species is added (it did with Meloetta), so an old record keeps its meaning.
#define BATTLE_LOG_SPECIES_EGG 0x7FF

typedef struct BattleLogRecord {
    u16 trainerIDs[2];
    u16 turns;
    u8 flags;
    u8 levelCapSplit;
    u16 playerSpecies[MAX_PARTY_SIZE]; // (form << 11) | species
    u8 playerPersonality[MAX_PARTY_SIZE]; // the low 8 bits
    u8 playerLevel[MAX_PARTY_SIZE];
    u16 enemySpecies[MAX_PARTY_SIZE]; // trainer A's party, then B's
    u8 enemyLevel[MAX_PARTY_SIZE];
    u8 enemyKnockedOutBy[MAX_PARTY_SIZE / 2]; // two 4-bit values a byte, low first
    u8 playerKnockedOutBy[MAX_PARTY_SIZE / 2];
    u8 playerCount;
    u8 enemyCounts; // A's in the low four bits, B's in the high four
} BattleLogRecord;

typedef struct BattleLogHeader {
    u8 magic[4];
    u16 version;
    u16 recordSize;
    u16 capacity;
    u16 count;
    u16 next;
    u16 reserved;
} BattleLogHeader;

typedef struct BattleLog {
    BattleLogHeader header;
    BattleLogRecord records[BATTLE_LOG_CAPACITY];
    SaveCheckFooter footer;
} BattleLog;

// What the live export finds in RAM by its two magic words
// (docs/oxide/battle-log.md, "The RAM beacon").
typedef struct OxideBeacon {
    u32 magic;
    u32 magicInverted;
    u16 version;
    u16 size;
    void *saveData;
    void *party;
    void *pcBoxes;
    void *battleLog;
    void *battleContext;
} OxideBeacon;

void BattleLog_Load(SaveData *saveData);
void BattleLog_Write(SaveData *saveData);
void BattleLog_Append(SaveData *saveData, const BattleLogRecord *record);
void BattleLog_SetBattleContext(void *battleContext);
u8 BattleLog_GetKnockOut(const u8 *packed, int slot);
void BattleLog_SetKnockOut(u8 *packed, int slot, u8 value);

#endif // POKEPLATINUM_BATTLE_LOG_H

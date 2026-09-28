#ifndef POKEPLATINUM_BATTLE_HALL_WIN_RECORDS_H
#define POKEPLATINUM_BATTLE_HALL_WIN_RECORDS_H

#include "constants/battle_frontier_stats.h"
#include "constants/heap.h"
#include "constants/species.h"

#include "savedata.h"

// Platinum Oxide: held at 654 streaks per challenge, the size the 159 new
// species gave it, so a save made before Meloetta keeps its Battle Hall streaks
// where they were. Every species that can enter the Hall is below SPECIES_EGG
// and fits; src/battle_hall_win_records.c refuses to compile if that stops
// being true. The sector caps this at 679 (docs/oxide/save-layout.md).
#define BATTLE_HALL_SPECIES_SLOTS 654

typedef struct BattleHallWinRecords {
    u32 alwaysNegative1;
    u16 singleStreaks[BATTLE_HALL_SPECIES_SLOTS];
    u16 doubleStreaks[BATTLE_HALL_SPECIES_SLOTS];
    u16 multiStreaks[BATTLE_HALL_SPECIES_SLOTS];
    u16 unused;
} BattleHallWinRecords;

int BattleHallWinRecords_SaveSize(void);
void BattleHallWinRecords_Init(BattleHallWinRecords *records);
BattleHallWinRecords *BattleHallWinRecords_Get(SaveData *saveData, enum HeapID heapID, int *resultCode);
int BattleHallWinRecords_Save(SaveData *saveData, BattleHallWinRecords *records);
u16 BattleHallWinRecords_GetRecordForSpecies(SaveData *saveData, BattleHallWinRecords *records, int challengeType, int species);
BOOL BattleHallWinRecords_UpdateRecord(SaveData *saveData, enum BattleFrontierStatsIndex recordIndex, enum BattleFrontierStatsIndex speciesIndex, int hostFriendID, int challengeType, enum HeapID heapID, int *resultCode, int *saveResult);

#endif // POKEPLATINUM_BATTLE_HALL_WIN_RECORDS_H

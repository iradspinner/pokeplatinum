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

// Flash sector 44 of each half, which nothing had written before. Since the
// 30 PC boxes the main save ends inside sector 43 and the extra save entries
// start at 45 (SAVE_PAGE_MAX), so this sector sits between the two.
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
    // Version 2 (2026-09-28): what the live export needs without per-build
    // addresses. Each layout entry is one of BEACON_LAYOUT_.
    void *trainerInfo;
    u16 boxCount;
    u16 layoutCount;
    const u16 *layout;
} OxideBeacon;

enum OxideBeaconLayout {
    BEACON_LAYOUT_TRAINER_ID = 0, // the u32 id in the TrainerInfo: trainer id low, secret id high
    BEACON_LAYOUT_BATTLE_MONS, // BattleContext's four BattleMons
    BEACON_LAYOUT_BATTLE_MON_SIZE,
    BEACON_LAYOUT_BATTLE_MON_SPECIES, // u16
    BEACON_LAYOUT_BATTLE_MON_LEVEL, // u8
    BEACON_LAYOUT_BATTLE_MON_CUR_HP, // s32
    BEACON_LAYOUT_BATTLE_MON_MAX_HP, // u32
    BEACON_LAYOUT_PARTY_RECORD_SIZE,
    BEACON_LAYOUT_BOX_RECORD_SIZE,
    // Added 2026-10-06 for the battle recorder: what each battler knows and
    // what it chose this turn. They go after the first nine, so a reader
    // built for nine still works; a newer reader checks layoutCount first.
    BEACON_LAYOUT_BATTLE_MON_MOVES, // four u16 move ids
    BEACON_LAYOUT_BATTLE_MON_CUR_PP, // four u8, one a move
    BEACON_LAYOUT_BATTLE_MON_STATUS, // u32, the MON_CONDITION_ bits
    BEACON_LAYOUT_BATTLE_MON_STATUS_VOLATILE, // u32, the VOLATILE_CONDITION_ bits
    BEACON_LAYOUT_BATTLE_MON_STAT_BOOSTS, // eight s8 stages, 6 meaning unchanged
    BEACON_LAYOUT_BATTLER_ACTIONS, // BattleContext's u32[4][4]: each battler's BATTLE_ACTION_ values
    BEACON_LAYOUT_MOVE_SLOTS, // BattleContext's u16[4]: each battler's chosen move slot, 0 to 3
    BEACON_LAYOUT_RECORDED_COMMAND_FLAGS, // BattleContext's u8[4]: bit 0 once a battler chose a command this turn
    BEACON_LAYOUT_TOTAL_TURNS, // BattleContext's int: turns finished
    BEACON_LAYOUT_COMMAND, // BattleContext's int: the battle controller's step
    BEACON_LAYOUT_COMMAND_NEXT, // BattleContext's int: the step a running script returns to
    BEACON_LAYOUT_CONTROL_SELECTION_INPUT, // the value of BATTLE_CONTROL_COMMAND_SELECTION_INPUT
    BEACON_LAYOUT_CONTROL_EXEC_SCRIPT, // the value of BATTLE_CONTROL_EXEC_SCRIPT
    BEACON_LAYOUT_COUNT
};

void BattleLog_Load(SaveData *saveData);
void BattleLog_Clear(SaveData *saveData);
void BattleLog_Write(SaveData *saveData);
void BattleLog_Append(SaveData *saveData, const BattleLogRecord *record);
void BattleLog_SetBattleContext(void *battleContext);
u8 BattleLog_GetKnockOut(const u8 *packed, int slot);
void BattleLog_SetKnockOut(u8 *packed, int slot, u8 value);

#endif // POKEPLATINUM_BATTLE_LOG_H

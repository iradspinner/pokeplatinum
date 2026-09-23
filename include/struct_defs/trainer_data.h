#ifndef POKEPLATINUM_STRUCT_TRAINER_DATA_H
#define POKEPLATINUM_STRUCT_TRAINER_DATA_H

/*
 * Note: *most* source files should not include this header directly, and should
 * instead including `struct_defs/trainer.h`. This header is held separately for
 * use by data-packing routines.
 */

#include "constants/moves.h"

#define TRAINER_MON_FORM_SHIFT 10

#define MAX_TRAINER_ITEMS 4
#define MAX_IV_SCALE      255

// A party member's ivScale field is 16 bits, and the IV scale only ever uses
// the low 8 (0 to MAX_IV_SCALE). Oxide keeps an optional nature in the high 8:
// 0 means roll the nature as the game always has, from the personality; n + 1
// forces nature n. So a trainer file without a nature packs exactly as before.
#define TRAINER_MON_IV_SCALE_MASK   0x00FF
#define TRAINER_MON_NATURE_SHIFT    8
#define TRAINER_MON_NATURE_DONT_CARE 0

enum TrainerDataType {
    TRDATATYPE_BASE = 0,
    TRDATATYPE_WITH_MOVES,
    TRDATATYPE_WITH_ITEM,
    TRDATATYPE_WITH_MOVES_AND_ITEM,
};

// Per-mon ability/gender overrides. 0 means "don't care" (existing behavior) in both cases.
enum TrainerMonAbility {
    TRAINER_MON_ABILITY_DONT_CARE = 0,
    TRAINER_MON_ABILITY_SLOT_1,
    TRAINER_MON_ABILITY_SLOT_2,
};

enum TrainerMonGender {
    TRAINER_MON_GENDER_DONT_CARE = 0,
    TRAINER_MON_GENDER_MALE,
    TRAINER_MON_GENDER_FEMALE,
};

typedef struct TrainerHeader {
    u8 monDataType;
    u8 trainerType;
    u8 sprite;
    u8 partySize;
    u16 items[MAX_TRAINER_ITEMS];
    u32 aiMask;
    u32 battleType;
} TrainerHeader;

typedef struct TrainerMonBase {
    u16 ivScale;
    u16 level;
    u16 species;
    u8 ability; // enum TrainerMonAbility
    u8 gender;  // enum TrainerMonGender
    u16 cbSeal;
} TrainerMonBase;

typedef struct TrainerMonWithMoves {
    u16 ivScale;
    u16 level;
    u16 species;
    u8 ability; // enum TrainerMonAbility
    u8 gender;  // enum TrainerMonGender
    u16 moves[LEARNED_MOVES_MAX];
    u16 cbSeal;
} TrainerMonWithMoves;

typedef struct TrainerMonWithItem {
    u16 ivScale;
    u16 level;
    u16 species;
    u8 ability; // enum TrainerMonAbility
    u8 gender;  // enum TrainerMonGender
    u16 item;
    u16 cbSeal;
} TrainerMonWithItem;

typedef struct TrainerMonWithMovesAndItem {
    u16 ivScale;
    u16 level;
    u16 species;
    u8 ability; // enum TrainerMonAbility
    u8 gender;  // enum TrainerMonGender
    u16 item;
    u16 moves[LEARNED_MOVES_MAX];
    u16 cbSeal;
} TrainerMonWithMovesAndItem;

#endif // POKEPLATINUM_STRUCT_TRAINER_DATA_H

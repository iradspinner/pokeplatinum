#ifndef POKEPLATINUM_SPECIES_H
#define POKEPLATINUM_SPECIES_H

// Platinum Oxide: three, not two. Slots 0 and 1 are the ordinary pair a
// Pokemon picks between on its personality; slot 2 is the hidden ability, and
// ABILITY_NONE there means the species has none.
#define MAX_ABILITIES  3
#define ABILITY_SLOT_1      0
#define ABILITY_SLOT_2      1
#define ABILITY_SLOT_HIDDEN 2
#define MAX_EGG_GROUPS 2
#define MAX_TYPES      2

// Platinum Oxide: nine, not seven. Eevee decided it: Platinum's seven slots
// were already full (Vaporeon, Jolteon, Flareon, Espeon, Umbreon, Leafeon,
// Glaceon) and Sylveon makes eight. Nine is also the donor's own slot count, so
// the record is now its 56 bytes.
#define MAX_EVOLUTIONS 9

// The packer aligns the table to four bytes, so the archive member is longer
// than the entries themselves and a whole-member read needs the rounded size.
#define SPECIES_EVOLUTIONS_MEMBER_SIZE \
    ((MAX_EVOLUTIONS * sizeof(SpeciesEvolution) + 3) & ~3u)

// Platinum Oxide: 34, not 20. The donor's level-up learnsets are 34 fixed
// slots and some new species fill more than twenty of them. The wotbl records
// are variable length, so this only sizes the buffer a lookup reads into.
#define MAX_LEARNSET_ENTRIES        34
#define LEARNSET_NO_MOVE_TO_LEARN   0
#define LEARNSET_MOVE_ALREADY_KNOWN 0xFFFE
#define LEARNSET_ALL_SLOTS_FILLED   0xFFFF
#define LEARNSET_SENTINEL_ENTRY     0xFFFF

typedef struct SpeciesBaseStats {
    u8 hp;
    u8 attack;
    u8 defense;
    u8 speed;
    u8 spAttack;
    u8 spDefense;
} SpeciesBaseStats;

typedef struct SpeciesEVYields {
    u16 hp : 2;
    u16 attack : 2;
    u16 defense : 2;
    u16 speed : 2;
    u16 spAttack : 2;
    u16 spDefense : 2;
} SpeciesEVYields;

typedef struct SpeciesWildHeldItems {
    u16 common;
    u16 rare;
} SpeciesWildHeldItems;

typedef struct SpeciesData {
    SpeciesBaseStats baseStats;
    u8 types[MAX_TYPES];
    u8 catchRate;
    // Platinum Oxide: dead. Base experience moved to the end of the record,
    // where the compiler was already leaving two bytes of padding, because
    // Generation 7 values run past 255. Widening it in place instead would have
    // shifted every field between here and the abilities for no gain.
    u8 unusedBaseExpReward;
    SpeciesEVYields evYields;
    SpeciesWildHeldItems wildHeldItems;
    u8 genderRatio;
    u8 hatchCycles;
    u8 baseFriendship;
    u8 expRate;
    u8 eggGroups[MAX_EGG_GROUPS];
    // Platinum Oxide: u16, not u8. hg-engine's ability ids run past 255 and the
    // donor ROM already stores them two bytes wide. This takes the species
    // record from 44 bytes to 48, which is why it no longer matches the base
    // ROM's; see docs/oxide/save-layout.md.
    u16 abilities[MAX_ABILITIES];
    u8 safariFleeRate;
    u8 bodyColor : 7;
    u8 flipSprite : 1;
    u16 baseExpReward; // Platinum Oxide: sits in what used to be implicit padding

    u32 tmLearnsetMasks[4]; // Bitflags for whether this pokemon can learn a TM
} SpeciesData;

typedef struct SpeciesEvolution {
    u16 method;
    u16 param;
    u16 targetSpecies;
} SpeciesEvolution;

typedef struct SpeciesLearnsetEntry {
    u16 move : 9;
    u16 level : 7;
} SpeciesLearnsetEntry;

// This struct is not explicitly used; it is provided to document and enforce the size of
// the learnset entries.
typedef struct SpeciesLearnset {
    ALIGN_4 SpeciesLearnsetEntry entries[MAX_LEARNSET_ENTRIES + 1];
} SpeciesLearnset;

typedef struct SpeciesPalPark {
    u8 landArea;
    u8 waterArea;
    u8 catchingPoints;
    u8 rarity;

    union {
        u8 asU8[2];
        u16 asU16;
    } unused;
} SpeciesPalPark;

#endif // POKEPLATINUM_SPECIES_H

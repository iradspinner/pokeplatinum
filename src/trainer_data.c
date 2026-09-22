#include "trainer_data.h"

#include "constants/battle.h"
#include "constants/pokemon.h"
#include "generated/genders.h"
#include "generated/natures.h"
#include "generated/trainer_message_types.h"

#include "struct_defs/trainer.h"

#include "data/trainer_class_genders.h"

#include "charcode_util.h"
#include "field_battle_data_transfer.h"
#include "heap.h"
#include "math_util.h"
#include "message.h"
#include "narc.h"
#include "party.h"
#include "pokemon.h"
#include "savedata.h"
#include "savedata_misc.h"
#include "string_gf.h"

static void TrainerData_BuildParty(FieldBattleDTO *dto, int battler, enum HeapID heapID);

void Trainer_Encounter(FieldBattleDTO *dto, const SaveData *saveData, enum HeapID heapID)
{
    Trainer trdata;
    MessageLoader *msgLoader = MessageLoader_Init(MSG_LOADER_LOAD_ON_DEMAND, NARC_INDEX_MSGDATA__PL_MSG, TEXT_BANK_NPC_TRAINER_NAMES, heapID);
    const charcode_t *rivalName = MiscSaveBlock_RivalName(SaveData_MiscSaveBlockConst(saveData));

    for (int i = 0; i < MAX_BATTLERS; i++) {
        if (!dto->trainerIDs[i]) {
            continue;
        }

        Trainer_Load(dto->trainerIDs[i], &trdata);
        dto->trainer[i] = trdata;

        if (trdata.header.trainerType == TRAINER_CLASS_RIVAL) {
            CharCode_Copy(dto->trainer[i].name, rivalName);
        } else {
            String *trainerName = MessageLoader_GetNewString(msgLoader, dto->trainerIDs[i]);
            String_ToChars(trainerName, dto->trainer[i].name, TRAINER_NAME_LEN + 1);
            String_Free(trainerName);
        }

        TrainerData_BuildParty(dto, i, heapID);
    }

    dto->battleType |= trdata.header.battleType;
    MessageLoader_Free(msgLoader);
}

u32 Trainer_LoadParam(int trainerID, enum TrainerDataParam paramID)
{
    // TODO: can this be trainerheader?
    u32 result;
    Trainer trdata;

    Trainer_Load(trainerID, &trdata);

    switch (paramID) {
    case TRDATA_TYPE:
        result = trdata.header.monDataType;
        break;

    case TRDATA_CLASS:
        result = trdata.header.trainerType;
        break;

    case TRDATA_SPRITE:
        result = trdata.header.sprite;
        break;

    case TRDATA_PARTY_SIZE:
        result = trdata.header.partySize;
        break;

    case TRDATA_ITEM_1:
    case TRDATA_ITEM_2:
    case TRDATA_ITEM_3:
    case TRDATA_ITEM_4:
        result = trdata.header.items[paramID - TRDATA_ITEM_1];
        break;

    case TRDATA_AI_MASK:
        result = trdata.header.aiMask;
        break;

    case TRDATA_BATTLE_TYPE:
        result = trdata.header.battleType;
        break;
    }

    return result;
}

BOOL Trainer_HasMessageType(int trainerID, enum TrainerMessageType msgType, enum HeapID heapID)
{
    NARC *narc; // must declare up here to match
    u16 offset, data[2];

    BOOL result = FALSE;
    int size = NARC_GetMemberSizeByIndexPair(NARC_INDEX_POKETOOL__TRMSG__TRTBL, 0);
    NARC_ReadFromMemberByIndexPair(&offset, NARC_INDEX_POKETOOL__TRMSG__TRTBLOFS, 0, trainerID * 2, 2);
    narc = NARC_ctor(NARC_INDEX_POKETOOL__TRMSG__TRTBL, heapID);

    while (offset != size) {
        NARC_ReadFromMember(narc, 0, offset, 4, data);

        if (data[0] == trainerID && data[1] == msgType) {
            result = TRUE;
            break;
        }

        if (data[0] != trainerID) {
            break;
        }

        offset += 4;
    }

    NARC_dtor(narc);
    return result;
}

void Trainer_LoadMessage(int trainerID, enum TrainerMessageType msgType, String *string, enum HeapID heapID)
{
    NARC *narc; // must declare up here to match
    u16 offset, data[2];

    int size = NARC_GetMemberSizeByIndexPair(NARC_INDEX_POKETOOL__TRMSG__TRTBL, 0);
    NARC_ReadFromMemberByIndexPair(&offset, NARC_INDEX_POKETOOL__TRMSG__TRTBLOFS, 0, trainerID * 2, 2);
    narc = NARC_ctor(NARC_INDEX_POKETOOL__TRMSG__TRTBL, heapID);

    while (offset != size) {
        NARC_ReadFromMember(narc, 0, offset, 4, data);

        if (data[0] == trainerID && data[1] == msgType) {
            MessageBank_GetStringFromNARC(NARC_INDEX_MSGDATA__PL_MSG, TEXT_BANK_NPC_TRAINER_MESSAGES, offset / 4, heapID, string);
            break;
        }

        offset += 4;
    }

    NARC_dtor(narc);

    if (offset == size) {
        String_Clear(string);
    }
}

void Trainer_Load(int trainerID, Trainer *trdata)
{
    NARC_ReadWholeMemberByIndexPair(trdata, NARC_INDEX_POKETOOL__TRAINER__TRDATA, trainerID);
}

void Trainer_LoadParty(int trainerID, void *trparty)
{
    NARC_ReadWholeMemberByIndexPair(trparty, NARC_INDEX_POKETOOL__TRAINER__TRPOKE, trainerID);
}

u8 TrainerClass_Gender(int trclass)
{
    return sTrainerClassGender[trclass];
}

/**
 * @brief Work out the low byte of a trainer mon's personality value.
 *
 * Ability slot is personality bit 0; a mon's own gender is the low byte
 * compared against its species' gender ratio (see SpeciesData_GetGenderOf).
 * Both live in the same byte, so honoring an explicit gender request and an
 * explicit ability request at once means picking a byte that satisfies both,
 * not applying them independently.
 *
 * @param species        The mon's species (used to resolve its gender ratio).
 * @param genderOverride enum TrainerMonGender; DONT_CARE leaves gender alone.
 * @param abilityOverride enum TrainerMonAbility; DONT_CARE leaves ability alone.
 * @param defaultLowByte The byte that would be used with no overrides (the
 *                        trainer-class-based genderMod already in use here).
 */
static u8 TrainerMon_PersonalityLowByte(u16 species, u8 genderOverride, u8 abilityOverride, u8 defaultLowByte)
{
    u8 wantBit, candidate, nudged;

    if (genderOverride == TRAINER_MON_GENDER_DONT_CARE) {
        if (abilityOverride == TRAINER_MON_ABILITY_DONT_CARE) {
            return defaultLowByte;
        }

        wantBit = (abilityOverride == TRAINER_MON_ABILITY_SLOT_2) ? 1 : 0;
        return (u8)((defaultLowByte & ~1) | wantBit);
    }

    u8 wantGender = (genderOverride == TRAINER_MON_GENDER_MALE) ? GENDER_MALE : GENDER_FEMALE;
    candidate     = (u8)sub_02074128(species, wantGender, 0);

    if (abilityOverride == TRAINER_MON_ABILITY_DONT_CARE) {
        return candidate;
    }

    wantBit = (abilityOverride == TRAINER_MON_ABILITY_SLOT_2) ? 1 : 0;
    if ((candidate & 1) == wantBit) {
        return candidate;
    }

    // Adding 1 always flips the low bit; re-verify against the species'
    // gender ratio rather than assume it stays on the same side of the
    // threshold, and fall back to the gender-correct byte if it doesn't.
    nudged = (u8)sub_02074128(species, wantGender, 1);
    if (Pokemon_GetGenderOf(species, nudged) == wantGender) {
        return nudged;
    }
    return candidate;
}

/**
 * @brief The personality a trainer's party member is built with.
 *
 * The vanilla roll: seed the LCRNG with the IV scale, level, species and
 * trainer ID, step it once per trainer class ID, and put the last value above
 * the low byte. If the trainer file names a nature (Oxide), the rolled value
 * is then stepped up until the personality lands on that nature. Only the
 * high part moves, so the low byte, which carries the gender and ability
 * requests, is untouched; and since 256 is 6 mod 25 and 6 is coprime to 25,
 * at most 24 steps reach any nature. With no nature named this is exactly
 * the roll the game has always made.
 *
 * @param ivScaleField   The party member's ivScale field: the IV scale in the
 *                       low byte, nature + 1 (or 0) in the high byte.
 */
static u32 TrainerMon_Personality(u16 ivScaleField, u16 level, u16 species, int trainerID, u8 trainerType, u8 gender, u8 ability, u8 genderMod)
{
    u32 rnd = (ivScaleField & TRAINER_MON_IV_SCALE_MASK) + level + species + trainerID;
    LCRNG_SetSeed(rnd);

    for (int j = 0; j < trainerType; j++) {
        rnd = LCRNG_Next();
    }

    u8 low = TrainerMon_PersonalityLowByte(species, gender, ability, genderMod);
    u8 nature = ivScaleField >> TRAINER_MON_NATURE_SHIFT;

    if (nature != TRAINER_MON_NATURE_DONT_CARE) {
        while (((rnd << 8) + low) % NATURE_COUNT != (u32)(nature - 1)) {
            rnd++;
        }
    }

    return (rnd << 8) + low;
}

/**
 * @brief Build the party for a trainer as loaded in the FieldBattleDTO struct.
 *
 * @param dto  The parent FieldBattleDTO struct containing trainer data.
 * @param battler       Which battler's party is to be loaded.
 * @param heapID        Heap on which to perform any allocations.
 */
static void TrainerData_BuildParty(FieldBattleDTO *dto, int battler, enum HeapID heapID)
{
    // must make declarations C89-style to match
    void *buf;
    int i, j;
    u32 genderMod, rnd, oldSeed;
    u8 ivs;
    Pokemon *mon;

    oldSeed = LCRNG_GetSeed();

    // alloc enough space to support the maximum possible data size
    Party_InitWithCapacity(dto->parties[battler], MAX_PARTY_SIZE);
    buf = Heap_Alloc(heapID, sizeof(TrainerMonWithMovesAndItem) * MAX_PARTY_SIZE);
    mon = Pokemon_New(heapID);

    Trainer_LoadParty(dto->trainerIDs[battler], buf);

    // determine which magic gender-specific modifier to use for the RNG function
    genderMod = TrainerClass_Gender(dto->trainer[battler].header.trainerType) == GENDER_FEMALE
        ? 120
        : 136;

    switch (dto->trainer[battler].header.monDataType) {
    case TRDATATYPE_BASE: {
        TrainerMonBase *trmon = (TrainerMonBase *)buf;
        for (i = 0; i < dto->trainer[battler].header.partySize; i++) {
            u16 species = trmon[i].species & 0x3FF;
            u8 form = (trmon[i].species & 0xFC00) >> TRAINER_MON_FORM_SHIFT;

            rnd = TrainerMon_Personality(trmon[i].ivScale, trmon[i].level, species, dto->trainerIDs[battler], dto->trainer[battler].header.trainerType, trmon[i].gender, trmon[i].ability, (u8)genderMod);
            ivs = (trmon[i].ivScale & TRAINER_MON_IV_SCALE_MASK) * MAX_IVS_SINGLE_STAT / MAX_IV_SCALE;

            Pokemon_InitWith(mon, species, trmon[i].level, ivs, TRUE, rnd, OTID_NOT_SHINY, 0);
            Pokemon_SetBallSeal(trmon[i].cbSeal, mon, heapID);
            Pokemon_SetValue(mon, MON_DATA_FORM, &form);
            Party_AddPokemon(dto->parties[battler], mon);
        }

        break;
    }

    case TRDATATYPE_WITH_MOVES: {
        TrainerMonWithMoves *trmon = (TrainerMonWithMoves *)buf;
        for (i = 0; i < dto->trainer[battler].header.partySize; i++) {
            u16 species = trmon[i].species & 0x3FF;
            u8 form = (trmon[i].species & 0xFC00) >> TRAINER_MON_FORM_SHIFT;

            rnd = TrainerMon_Personality(trmon[i].ivScale, trmon[i].level, species, dto->trainerIDs[battler], dto->trainer[battler].header.trainerType, trmon[i].gender, trmon[i].ability, (u8)genderMod);
            ivs = (trmon[i].ivScale & TRAINER_MON_IV_SCALE_MASK) * MAX_IVS_SINGLE_STAT / MAX_IV_SCALE;

            Pokemon_InitWith(mon, species, trmon[i].level, ivs, TRUE, rnd, OTID_NOT_SHINY, 0);

            for (j = 0; j < 4; j++) {
                Pokemon_SetMoveSlot(mon, trmon[i].moves[j], j);
            }

            Pokemon_SetBallSeal(trmon[i].cbSeal, mon, heapID);
            Pokemon_SetValue(mon, MON_DATA_FORM, &form);
            Party_AddPokemon(dto->parties[battler], mon);
        }

        break;
    }

    case TRDATATYPE_WITH_ITEM: {
        TrainerMonWithItem *trmon = (TrainerMonWithItem *)buf;
        for (i = 0; i < dto->trainer[battler].header.partySize; i++) {
            u16 species = trmon[i].species & 0x3FF;
            u8 form = (trmon[i].species & 0xFC00) >> TRAINER_MON_FORM_SHIFT;

            rnd = TrainerMon_Personality(trmon[i].ivScale, trmon[i].level, species, dto->trainerIDs[battler], dto->trainer[battler].header.trainerType, trmon[i].gender, trmon[i].ability, (u8)genderMod);
            ivs = (trmon[i].ivScale & TRAINER_MON_IV_SCALE_MASK) * MAX_IVS_SINGLE_STAT / MAX_IV_SCALE;

            Pokemon_InitWith(mon, species, trmon[i].level, ivs, TRUE, rnd, OTID_NOT_SHINY, 0);
            Pokemon_SetValue(mon, MON_DATA_HELD_ITEM, &trmon[i].item);
            Pokemon_SetBallSeal(trmon[i].cbSeal, mon, heapID);
            Pokemon_SetValue(mon, MON_DATA_FORM, &form);
            Party_AddPokemon(dto->parties[battler], mon);
        }

        break;
    }

    case TRDATATYPE_WITH_MOVES_AND_ITEM: {
        TrainerMonWithMovesAndItem *trmon = (TrainerMonWithMovesAndItem *)buf;
        for (i = 0; i < dto->trainer[battler].header.partySize; i++) {
            u16 species = trmon[i].species & 0x3FF;
            u8 form = (trmon[i].species & 0xFC00) >> TRAINER_MON_FORM_SHIFT;

            rnd = TrainerMon_Personality(trmon[i].ivScale, trmon[i].level, species, dto->trainerIDs[battler], dto->trainer[battler].header.trainerType, trmon[i].gender, trmon[i].ability, (u8)genderMod);
            ivs = (trmon[i].ivScale & TRAINER_MON_IV_SCALE_MASK) * MAX_IVS_SINGLE_STAT / MAX_IV_SCALE;

            Pokemon_InitWith(mon, species, trmon[i].level, ivs, TRUE, rnd, OTID_NOT_SHINY, 0);
            Pokemon_SetValue(mon, MON_DATA_HELD_ITEM, &trmon[i].item);

            for (j = 0; j < 4; j++) {
                Pokemon_SetMoveSlot(mon, trmon[i].moves[j], j);
            }

            Pokemon_SetBallSeal(trmon[i].cbSeal, mon, heapID);
            Pokemon_SetValue(mon, MON_DATA_FORM, &form);
            Party_AddPokemon(dto->parties[battler], mon);
        }

        break;
    }
    }

    Heap_Free(buf);
    Heap_Free(mon);
    LCRNG_SetSeed(oldSeed);
}

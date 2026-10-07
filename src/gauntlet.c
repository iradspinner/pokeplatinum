#include "gauntlet.h"

#include <nitro.h>

#include "constants/heap.h"
#include "constants/map_object.h"
#include "constants/savedata/vars_flags.h"
#include "generated/items.h"
#include "generated/map_headers.h"
#include "generated/trainers.h"

#include "field/field_system.h"

#include "bag.h"
#include "location.h"
#include "player_avatar.h"
#include "savedata.h"
#include "script_manager.h"
#include "vars_flags.h"

// Platinum Oxide: the gauntlets (Ian, 2026-09-27 and 2026-09-29). The
// sections, and why each map and warp is listed, are in docs/oxide/gauntlets.md.
//
// VAR_GAUNTLET_SECTION holds the open section's number, or GAUNTLET_NONE. A
// section opens when the player arrives through one of its ways in and one
// of its trainers is still to beat. It stays open while the player is on one
// of its maps, which include the dead-end pockets a detour leads to, so that
// stepping into a side room does not close it. It closes on arrival anywhere
// else: its way forward, a scripted warp, a whiteout. A section whose
// trainers are all beaten, or hidden by the story, counts as closed too.

enum GauntletSectionID {
    GAUNTLET_NONE = 0,
    GAUNTLET_ETERNA_BUILDING_1F_2F,
    GAUNTLET_ETERNA_BUILDING_3F,
    GAUNTLET_GALACTIC_HQ_B2F,
    GAUNTLET_GALACTIC_HQ_1F,
    GAUNTLET_GALACTIC_HQ_2F,
    GAUNTLET_GALACTIC_HQ_3F,
    GAUNTLET_MT_CORONET_TUNNEL,
    GAUNTLET_MT_CORONET_CLIMB,
    GAUNTLET_VICTORY_ROAD_NEAR,
    GAUNTLET_VICTORY_ROAD_FAR,
    GAUNTLET_SECTION_COUNT,
};

typedef struct GauntletWarp {
    u16 mapHeaderID;
    u16 warpIndex;
    // A way back is refused only while the player holds this item (ITEM_NONE:
    // always). Galactic HQ 3F's way on is a locked door, so a player without
    // the Galactic Key must still be able to turn back.
    u16 unlessMissingItem;
} GauntletWarp;

typedef struct GauntletTrainer {
    u16 trainerID;
    // The trainer's map object is hidden while this flag is set (0: never).
    u16 hideFlag;
} GauntletTrainer;

#define GAUNTLET_MAX_MAPS     8
#define GAUNTLET_MAX_WARPS    4
#define GAUNTLET_MAX_TRAINERS 5

typedef struct GauntletSection {
    u16 maps[GAUNTLET_MAX_MAPS]; // ends at the first MAP_HEADER_INVALID or the size
    GauntletWarp waysIn[GAUNTLET_MAX_WARPS];
    GauntletWarp waysBack[GAUNTLET_MAX_WARPS];
    GauntletTrainer trainers[GAUNTLET_MAX_TRAINERS];
} GauntletSection;

#define END_MAPS     MAP_HEADER_INVALID
#define END_WARPS    { MAP_HEADER_INVALID, 0, ITEM_NONE }
#define END_TRAINERS { 0, 0 }

// Today's sections (the balance plan, "The gauntlets, reworked on Ian's
// rulings"), placed on the maps as they are walked. Ian's case-by-case
// ruling on the trainers above their split's average edits the trainer lists.
static const GauntletSection sGauntletSections[GAUNTLET_SECTION_COUNT] = {
    [GAUNTLET_ETERNA_BUILDING_1F_2F] = {
        .maps = { MAP_HEADER_TEAM_GALACTIC_ETERNA_BUILDING_1F, MAP_HEADER_TEAM_GALACTIC_ETERNA_BUILDING_2F, MAP_HEADER_TEAM_GALACTIC_ETERNA_BUILDING_3F, MAP_HEADER_ROTOMS_ROOM, END_MAPS },
        .waysIn = { { MAP_HEADER_TEAM_GALACTIC_ETERNA_BUILDING_1F, 0, ITEM_NONE }, END_WARPS },
        .waysBack = { { MAP_HEADER_TEAM_GALACTIC_ETERNA_BUILDING_1F, 0, ITEM_NONE }, END_WARPS },
        .trainers = {
            { TRAINER_GALACTIC_GRUNT_TEAM_GALACTIC_ETERNA_BUILDING_1F_1, FLAG_HIDE_ETERNA_CITY_GALACTIC_GRUNTS },
            { TRAINER_GALACTIC_GRUNT_TEAM_GALACTIC_ETERNA_BUILDING_1F_2, FLAG_HIDE_ETERNA_CITY_GALACTIC_GRUNTS },
            { TRAINER_GALACTIC_GRUNT_TEAM_GALACTIC_ETERNA_BUILDING_2F_1, FLAG_HIDE_ETERNA_CITY_GALACTIC_GRUNTS },
            { TRAINER_GALACTIC_GRUNT_TEAM_GALACTIC_ETERNA_BUILDING_2F_2, FLAG_HIDE_ETERNA_CITY_GALACTIC_GRUNTS },
            END_TRAINERS,
        },
    },
    [GAUNTLET_ETERNA_BUILDING_3F] = {
        .maps = { MAP_HEADER_TEAM_GALACTIC_ETERNA_BUILDING_3F, END_MAPS },
        .waysIn = { { MAP_HEADER_TEAM_GALACTIC_ETERNA_BUILDING_3F, 2, ITEM_NONE }, END_WARPS },
        .waysBack = { { MAP_HEADER_TEAM_GALACTIC_ETERNA_BUILDING_3F, 2, ITEM_NONE }, END_WARPS },
        .trainers = {
            { TRAINER_SCIENTIST_TRAVON, FLAG_HIDE_ETERNA_CITY_GALACTIC_GRUNTS },
            { TRAINER_GALACTIC_GRUNT_TEAM_GALACTIC_ETERNA_BUILDING_3F, FLAG_HIDE_ETERNA_CITY_GALACTIC_GRUNTS },
            END_TRAINERS,
        },
    },
    // The warehouse leads into B2F, so the HQ is walked B2F, B1F, 1F, 2F, 3F.
    [GAUNTLET_GALACTIC_HQ_B2F] = {
        .maps = { MAP_HEADER_GALACTIC_HQ_B2F, END_MAPS },
        .waysIn = { { MAP_HEADER_GALACTIC_HQ_B2F, 2, ITEM_NONE }, END_WARPS },
        .waysBack = { { MAP_HEADER_GALACTIC_HQ_B2F, 2, ITEM_NONE }, END_WARPS },
        .trainers = {
            { TRAINER_GALACTIC_GRUNT_GALACTIC_HQ_B2F_1, FLAG_HIDE_GALACTIC_HQ_TEAM_GALACTIC },
            { TRAINER_GALACTIC_GRUNT_GALACTIC_HQ_B2F_2, FLAG_HIDE_GALACTIC_HQ_TEAM_GALACTIC },
            END_TRAINERS,
        },
    },
    // The front doors to Veilstone are ways back too: the Galactic Key, found
    // on B2F, opens the lobby from inside.
    [GAUNTLET_GALACTIC_HQ_1F] = {
        .maps = { MAP_HEADER_GALACTIC_HQ_1F, END_MAPS },
        .waysIn = { { MAP_HEADER_GALACTIC_HQ_1F, 7, ITEM_NONE }, END_WARPS },
        .waysBack = {
            { MAP_HEADER_GALACTIC_HQ_1F, 7, ITEM_NONE },
            { MAP_HEADER_GALACTIC_HQ_1F, 0, ITEM_NONE },
            { MAP_HEADER_GALACTIC_HQ_1F, 1, ITEM_NONE },
            END_WARPS,
        },
        .trainers = {
            { TRAINER_GALACTIC_GRUNT_GALACTIC_HQ_1F, FLAG_HIDE_GALACTIC_HQ_TEAM_GALACTIC },
            { TRAINER_SCIENTIST_FREDRICK, FLAG_HIDE_GALACTIC_HQ_TEAM_GALACTIC },
            END_TRAINERS,
        },
    },
    // Fredrick's pocket on 1F, and the dead end on B2F past it, are a detour
    // from 2F, so the lock holds there.
    [GAUNTLET_GALACTIC_HQ_2F] = {
        .maps = { MAP_HEADER_GALACTIC_HQ_2F, MAP_HEADER_GALACTIC_HQ_1F, MAP_HEADER_GALACTIC_HQ_B2F, END_MAPS },
        .waysIn = { { MAP_HEADER_GALACTIC_HQ_2F, 0, ITEM_NONE }, END_WARPS },
        .waysBack = { { MAP_HEADER_GALACTIC_HQ_2F, 0, ITEM_NONE }, END_WARPS },
        .trainers = {
            { TRAINER_GALACTIC_GRUNT_GALACTIC_HQ_2F_3, FLAG_HIDE_GALACTIC_HQ_TEAM_GALACTIC },
            { TRAINER_GALACTIC_GRUNT_GALACTIC_HQ_2F_2, FLAG_HIDE_GALACTIC_HQ_TEAM_GALACTIC },
            { TRAINER_GALACTIC_GRUNT_GALACTIC_HQ_2F_1, FLAG_HIDE_GALACTIC_HQ_TEAM_GALACTIC },
            { TRAINER_SCIENTIST_DARRIUS, FLAG_HIDE_GALACTIC_HQ_TEAM_GALACTIC },
            END_TRAINERS,
        },
    },
    // Past 3F's locked door, the hall leads back into 2F's east side, a detour
    // with no way out, so the lock holds there as well.
    [GAUNTLET_GALACTIC_HQ_3F] = {
        .maps = { MAP_HEADER_GALACTIC_HQ_3F, MAP_HEADER_GALACTIC_HQ_2F, MAP_HEADER_GALACTIC_HQ_HALL, MAP_HEADER_GALACTIC_HQ_1F, END_MAPS },
        .waysIn = { { MAP_HEADER_GALACTIC_HQ_3F, 0, ITEM_NONE }, END_WARPS },
        .waysBack = { { MAP_HEADER_GALACTIC_HQ_3F, 0, ITEM_GALACTIC_KEY }, END_WARPS },
        .trainers = {
            { TRAINER_GALACTIC_GRUNT_GALACTIC_HQ_3F_2, FLAG_HIDE_GALACTIC_HQ_TEAM_GALACTIC },
            { TRAINER_GALACTIC_GRUNT_GALACTIC_HQ_3F_3, FLAG_HIDE_GALACTIC_HQ_TEAM_GALACTIC },
            { TRAINER_GALACTIC_GRUNT_GALACTIC_HQ_3F_1, FLAG_HIDE_GALACTIC_HQ_TEAM_GALACTIC },
            { TRAINER_GALACTIC_GRUNT_GALACTIC_HQ_3F_4, FLAG_HIDE_GALACTIC_HQ_TEAM_GALACTIC },
            END_TRAINERS,
        },
    },
    // The climb has two routes that meet on the outside north ledge: this
    // tunnel from Route 211's room, and the southern one below.
    [GAUNTLET_MT_CORONET_TUNNEL] = {
        .maps = { MAP_HEADER_MT_CORONET_1F_TUNNEL_ROOM, END_MAPS },
        .waysIn = { { MAP_HEADER_MT_CORONET_1F_TUNNEL_ROOM, 1, ITEM_NONE }, END_WARPS },
        .waysBack = { { MAP_HEADER_MT_CORONET_1F_TUNNEL_ROOM, 1, ITEM_NONE }, END_WARPS },
        .trainers = {
            { TRAINER_GALACTIC_GRUNT_MT_CORONET_TUNNEL_ROOM_2, FLAG_HIDE_MT_CORONET_GALACTIC_GRUNTS },
            { TRAINER_GALACTIC_GRUNT_MT_CORONET_TUNNEL_ROOM_3, FLAG_HIDE_MT_CORONET_GALACTIC_GRUNTS },
            { TRAINER_GALACTIC_GRUNT_MT_CORONET_TUNNEL_ROOM_1, FLAG_HIDE_MT_CORONET_GALACTIC_GRUNTS },
            END_TRAINERS,
        },
    },
    // 3F, the outside ledges, 4F and 5F, up to 6F. The north ledge's cave
    // mouth into the tunnel leads back down to Route 211, so it is a way back.
    [GAUNTLET_MT_CORONET_CLIMB] = {
        .maps = { MAP_HEADER_MT_CORONET_3F, MAP_HEADER_MT_CORONET_2F, MAP_HEADER_MT_CORONET_OUTSIDE_SOUTH, MAP_HEADER_MT_CORONET_4F_ROOMS_1_AND_2, MAP_HEADER_MT_CORONET_OUTSIDE_NORTH, MAP_HEADER_MT_CORONET_4F_ROOM_3, MAP_HEADER_MT_CORONET_5F, END_MAPS },
        .waysIn = { { MAP_HEADER_MT_CORONET_3F, 0, ITEM_NONE }, END_WARPS },
        .waysBack = {
            { MAP_HEADER_MT_CORONET_3F, 0, ITEM_NONE },
            { MAP_HEADER_MT_CORONET_OUTSIDE_NORTH, 2, ITEM_NONE },
            END_WARPS,
        },
        .trainers = {
            { TRAINER_GALACTIC_GRUNT_MT_CORONET_3F_1, FLAG_HIDE_MT_CORONET_GALACTIC_GRUNTS },
            { TRAINER_GALACTIC_GRUNT_MT_CORONET_3F_2, FLAG_HIDE_MT_CORONET_GALACTIC_GRUNTS },
            { TRAINER_GALACTIC_GRUNT_MT_CORONET_4F_1, FLAG_HIDE_MT_CORONET_GALACTIC_GRUNTS },
            { TRAINER_GALACTIC_GRUNT_MT_CORONET_4F_2, FLAG_HIDE_MT_CORONET_GALACTIC_GRUNTS },
            { TRAINER_GALACTIC_GRUNT_MT_CORONET_5F_2, FLAG_HIDE_MT_CORONET_GALACTIC_GRUNTS },
        },
    },
    // Victory Road's 1F runs from the entrance to the exit on its own; 2F and
    // B1F are detours off it, so the lock holds there. The line between the
    // two halves is in sGauntletLines.
    [GAUNTLET_VICTORY_ROAD_NEAR] = {
        .maps = { MAP_HEADER_VICTORY_ROAD_1F, MAP_HEADER_VICTORY_ROAD_2F, MAP_HEADER_VICTORY_ROAD_B1F, END_MAPS },
        .waysIn = {
            { MAP_HEADER_VICTORY_ROAD_1F, 7, ITEM_NONE },
            { MAP_HEADER_VICTORY_ROAD_1F, 9, ITEM_NONE },
            { MAP_HEADER_VICTORY_ROAD_1F, 10, ITEM_NONE },
            END_WARPS,
        },
        .waysBack = {
            { MAP_HEADER_VICTORY_ROAD_1F, 7, ITEM_NONE },
            { MAP_HEADER_VICTORY_ROAD_1F, 9, ITEM_NONE },
            { MAP_HEADER_VICTORY_ROAD_1F, 10, ITEM_NONE },
            END_WARPS,
        },
        .trainers = {
            { TRAINER_PSYCHIC_BRYCE, 0 },
            { TRAINER_BIRD_KEEPER_HANA, 0 },
            { TRAINER_ACE_TRAINER_MARIAH, 0 },
            END_TRAINERS,
        },
    },
    // Entered only across the line. The back rooms lead out to Route 224.
    [GAUNTLET_VICTORY_ROAD_FAR] = {
        .maps = { MAP_HEADER_VICTORY_ROAD_1F, MAP_HEADER_VICTORY_ROAD_2F, MAP_HEADER_VICTORY_ROAD_B1F, MAP_HEADER_VICTORY_ROAD_1F_ROOM_1, MAP_HEADER_VICTORY_ROAD_1F_ROOM_2, MAP_HEADER_VICTORY_ROAD_1F_ROOM_3, END_MAPS },
        .waysIn = { END_WARPS },
        .waysBack = { { MAP_HEADER_VICTORY_ROAD_1F_ROOM_3, 1, ITEM_NONE }, END_WARPS },
        .trainers = {
            { TRAINER_BLACK_BELT_MILES, 0 },
            { TRAINER_DRAGON_TAMER_CLINTON, 0 },
            { TRAINER_VETERAN_EDGAR, 0 },
            END_TRAINERS,
        },
    },
};

// A line across a corridor that splits one map between two sections: two
// tiles one step apart, each carrying a coord event that runs the field moves
// archive's line script. Stepping onto the far tile facing the way forward
// opens the section beyond; stepping onto the near tile facing back, while
// that section is open, turns the player around.
typedef struct GauntletLine {
    u16 mapHeaderID;
    u16 nearX, nearZ;
    u16 farX, farZ;
    u8 forwardDir;
    u8 sectionBeyond;
} GauntletLine;

static const GauntletLine sGauntletLines[] = {
    { MAP_HEADER_VICTORY_ROAD_1F, 13, 27, 13, 26, DIR_NORTH, GAUNTLET_VICTORY_ROAD_FAR },
};

static u16 *GetSectionVar(FieldSystem *fieldSystem)
{
    return VarsFlags_GetVarAddress(SaveData_GetVarsFlags(fieldSystem->saveData), VAR_GAUNTLET_SECTION);
}

static BOOL SectionHasMap(const GauntletSection *section, u16 mapHeaderID)
{
    for (int i = 0; i < GAUNTLET_MAX_MAPS && section->maps[i] != MAP_HEADER_INVALID; i++) {
        if (section->maps[i] == mapHeaderID) {
            return TRUE;
        }
    }

    return FALSE;
}

static const GauntletWarp *FindWarp(const GauntletWarp *warps, u16 mapHeaderID, int warpIndex)
{
    for (int i = 0; i < GAUNTLET_MAX_WARPS && warps[i].mapHeaderID != MAP_HEADER_INVALID; i++) {
        if (warps[i].mapHeaderID == mapHeaderID && warps[i].warpIndex == warpIndex) {
            return &warps[i];
        }
    }

    return NULL;
}

// A trainer counts while unbeaten and on the map: the story hides some
// sections' trainers before or after its own part, and a section must never
// wait on a trainer the player cannot reach.
static BOOL HasTrainersLeft(FieldSystem *fieldSystem, const GauntletSection *section)
{
    VarsFlags *varsFlags = SaveData_GetVarsFlags(fieldSystem->saveData);

    for (int i = 0; i < GAUNTLET_MAX_TRAINERS && section->trainers[i].trainerID != 0; i++) {
        const GauntletTrainer *trainer = &section->trainers[i];

        if (Script_IsTrainerDefeated(fieldSystem, trainer->trainerID)) {
            continue;
        }

        if (trainer->hideFlag != 0 && VarsFlags_CheckFlag(varsFlags, trainer->hideFlag)) {
            continue;
        }

        return TRUE;
    }

    return FALSE;
}

static const GauntletSection *GetOpenSection(FieldSystem *fieldSystem)
{
    u16 id = *GetSectionVar(fieldSystem);

    if (id == GAUNTLET_NONE || id >= GAUNTLET_SECTION_COUNT) {
        return NULL;
    }

    const GauntletSection *section = &sGauntletSections[id];

    if (!SectionHasMap(section, fieldSystem->location->mapHeaderID) || !HasTrainersLeft(fieldSystem, section)) {
        return NULL;
    }

    return section;
}

static void OpenSection(FieldSystem *fieldSystem, u16 id)
{
    *GetSectionVar(fieldSystem) = HasTrainersLeft(fieldSystem, &sGauntletSections[id]) ? id : GAUNTLET_NONE;
}

// noWarp: the player walked across a seam between two overworld maps, and
// the location's warp index is left over from an earlier warp.
void Gauntlet_OnMapChange(FieldSystem *fieldSystem, BOOL noWarp)
{
    const Location *location = fieldSystem->location;
    u16 *sectionVar = GetSectionVar(fieldSystem);

    if (!noWarp && location->warpId != WARP_ID_NONE) {
        for (u16 id = GAUNTLET_NONE + 1; id < GAUNTLET_SECTION_COUNT; id++) {
            if (FindWarp(sGauntletSections[id].waysIn, location->mapHeaderID, location->warpId) != NULL) {
                OpenSection(fieldSystem, id);
                return;
            }
        }
    }

    if (*sectionVar != GAUNTLET_NONE
        && (*sectionVar >= GAUNTLET_SECTION_COUNT || !SectionHasMap(&sGauntletSections[*sectionVar], location->mapHeaderID))) {
        *sectionVar = GAUNTLET_NONE;
    }
}

BOOL Gauntlet_IsOpen(FieldSystem *fieldSystem)
{
    return GetOpenSection(fieldSystem) != NULL;
}

BOOL Gauntlet_RefusesWarp(FieldSystem *fieldSystem, int warpIndex)
{
    const GauntletSection *section = GetOpenSection(fieldSystem);

    if (section == NULL) {
        return FALSE;
    }

    const GauntletWarp *wayBack = FindWarp(section->waysBack, fieldSystem->location->mapHeaderID, warpIndex);

    if (wayBack == NULL) {
        return FALSE;
    }

    return wayBack->unlessMissingItem == ITEM_NONE
        || Bag_CanRemoveItem(SaveData_GetBag(fieldSystem->saveData), wayBack->unlessMissingItem, 1, HEAP_ID_FIELD1);
}

enum GauntletLineResult Gauntlet_StepOnLine(FieldSystem *fieldSystem)
{
    int x = PlayerAvatar_GetXPos(fieldSystem->playerAvatar);
    int z = PlayerAvatar_GetZPos(fieldSystem->playerAvatar);
    int dir = PlayerAvatar_GetFacingDir(fieldSystem->playerAvatar);

    for (int i = 0; i < NELEMS(sGauntletLines); i++) {
        const GauntletLine *line = &sGauntletLines[i];

        if (line->mapHeaderID != fieldSystem->location->mapHeaderID) {
            continue;
        }

        if (x == line->farX && z == line->farZ && dir == line->forwardDir) {
            OpenSection(fieldSystem, line->sectionBeyond);
            return GAUNTLET_LINE_NOTHING;
        }

        if (x == line->nearX && z == line->nearZ && dir != line->forwardDir
            && *GetSectionVar(fieldSystem) == line->sectionBeyond && Gauntlet_IsOpen(fieldSystem)) {
            return GAUNTLET_LINE_TURN_BACK;
        }
    }

    return GAUNTLET_LINE_NOTHING;
}

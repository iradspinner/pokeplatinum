# Platinum Oxide: Hardlove Gold engine-expansion integration into Pokemon Platinum

Design document, v0.21 (2026-09-21). This file is written for Claude to work from. Read it in full at the start of every session, then read `docs/oxide/tracker.md`, then act. Facts and rules live here; status lives in the tracker; the encounter tool's own status and findings live in `docs/oxide/encounter-tool-build-plan.md`.

## 1. What this project is

Port the engine-expansion elements of Hardlove Gold (a HeartGold hack, v0.6.9) into Pokemon Platinum, using the "Platinum Unlocked - Challenge - Adjusted v1.1" ROM as the base that receives the changes.

Two reasons, in Ian's words: to find out whether it can be done at all, and to work inside a game he knows far better than HeartGold.

This is a hobby project. No QA gate, no release schedule. The bar is "works in an emulator and Ian is happy with it."

## 2. Ground truth

Everything in this section is verified from the files, not assumed. Update it when something changes.

### Working folder

`G:\PokeROMs\Rokemon RomHack Creation Hub\Hardlove Gold-Platinum Oxide Integration Project`

| Item | What it is |
|---|---|
| `Platinum Unlocked - Challenge - Adjusted v1.1.nds` | The base ROM. 128 MB. Gamecode CPUE, rom_version 1 (US Rev 1). All changes land here. The "Unlocked" and "Challenge - Adjusted" tags are from older hand edits by Ian and have no bearing on this project; the only thing that matters is that this is not vanilla Platinum, so never assume a vanilla byte layout or vanilla values without checking the file. |
| `Platinum Unlocked - DSPRE contents\` | DSPRE extraction of the base ROM. `files\` is the NDS filesystem (NARCs), `unpacked\` is DSPRE's exploded per-record working data, `arm9\` and `arm9_overlays\` are the code. |
| `Platinum Unlocked - DSPRE contents\Platinum Oxide VSMaker2 Data\` | A VSMaker2 extraction (arm9.bin, overlays, data, unpacked). Trainer-editing tool data. A stale second extraction of the base ROM (2026-08-04), not read by DSPRE; do not source tables from it. |
| `Hardlove Gold NDS (0.6.9).nds` | The donor ROM. 192 MB. Gamecode IPKE. This is a copy; the playable original lives in `G:\PokeROMs\HeartGold Roms`. Writing to this copy is allowed (for example to test a theory about where something lives), but it stays the donor, not a deliverable. |
| `Hardlove Gold NDS (0.6.9)_DSPRE_contents\` | DSPRE extraction of the donor. Same layout. Also a copy; writable. |

Everything in this folder is a copy. Ian has confirmed (2026-09-15) that any file here, including the Hardlove ROM and its DSPRE contents, may be modified. The originals in the hub folder and in `HeartGold Roms` are untouched by this project.

Since approach C (section 4) the source of truth is the repo `iradspinner/pokeplatinum`, branch `oxide`, checked out at `~/pokeplatinum` in WSL2. The working folder is reference input (the two ROMs and their extractions) plus mirror copies of the docs, written by `tools/oxide/sync-docs.sh`. Pinned copies of the two reference ROMs live at `~/roms/base.nds` (the base ROM) and `~/roms/vanilla.nds` (a byte-exact Rev 1 build from `main`).

### Size of the gap, by the numbers

| Data | Platinum base | Hardlove donor |
|---|---|---|
| personalPokeData (species records, 44 bytes) | 508 files (`0000`..`0507`, vanilla Gen 4 count) | 1476 files (`0000`..`1475`) |
| moveData (16 bytes each) | 471 files (`0000`..`0470`, vanilla + 4 spares) | 924 files (`0000`..`0923`) |
| Ability IDs observed | vanilla, 1 byte, max 123 | up to 318, stored as u16 |
| Types | vanilla 17 | expanded (Fairy at minimum) |

Hardlove's personal struct is hg-engine's `SpeciesData`: ability 1 is a u16 at 0x16..0x17 and ability 2 is a u16 at 0x1A..0x1B (repurposed padding). Base exp and TM compat are zero in every record because hg-engine moved them out of the struct (base exp to NARC `a/0/2/8` member 9_08, TM compatibility into the learnset data). EV yields and held items being zero is Hardlove's own choice. Its personalPokeData index for Gen 5+ species is National Dex number + 50, because files 0494..0543 are form/spare slots. The full struct layout is in the project doc `claude/rom-workspace-map.md`; treat it as the reference for reading donor records.

### Filesystem layout differences (from `path_order.txt`)

Platinum keeps its data under named paths (`/poketool/personal`, `/poketool/waza`, `/fielddata/encountdata`, `/msgdata`, `/battle`, `/wazaeffect`, and so on). HeartGold (and therefore Hardlove) collapses almost everything into `/a/0/x/y` numbered NARCs. Nothing can be copied across by path name; every table has to be matched by content and purpose, then converted.

Platinum's extraction also carries `encounterExtended`, `tradeData`, `trainerParty`, `trainerTextTable`, `pokemonSpriteOffsets`, `pokeHeight` and `battleBg/battleObj` folders that the Hardlove extraction does not, and Hardlove's has `interiorBuildingModels`. Some of that is a DSPRE-version difference rather than a game difference; confirm before relying on it.

### How hg-engine (and therefore Hardlove) is put together

hg-engine is a patch kit applied to a vanilla US HeartGold ROM, not a rebuilt game. Compiled C goes into new overlays 129..151 (129 is loaded at boot as a permanent arm9 extension); ~1,370 lines of hook/repoint/byte-replacement lists and ~3,200 lines of armips patches edit the vanilla arm9 and overlays at fixed addresses; ~40 NARCs are regenerated from source data. Hardlove's extraction shows exactly this (overlays 129..151 at hg-engine's load addresses, hg-engine's species and move numbering). Full detail: `docs/oxide/phase1-hg-engine-survey.md`.

Consequence: none of hg-engine's addresses exist in Platinum. Porting means re-targeting the same design onto Platinum's binaries (or rebuilding from Platinum's decomp), not copying files.

### Tooling already built (Hardlove side)

`romtool\hardlove.py` in the hub folder has working readers and writers for the NDS filesystem, NARC pack/unpack (verified byte-identical round trip), personal, evolution, encounter and trainer layers. `Rom.write_file` refuses size-changing writes. This is HeartGold-shaped code and will need a Platinum sibling, but the NARC and ROM layers are game-agnostic and should be reused rather than rewritten. Not used so far: the repo's `tools/oxide/import_base_rom.py` grew its own NDS and NARC readers for the Platinum side, and `tools/oxide/donor.py` reads the donor (the `read-donor` skill).

## 3. Scope

Ian's broad strokes: the type expansion, pokedex expansion, move expansion, ability expansion, and "various other smaller engine changes" are wanted. The exact list of what is and is not brought over is an open item to be worked out with Ian, not decided unilaterally.

Working scope table. Status values: `wanted`, `maybe`, `out`, `undecided`.

| Element | Status | Notes |
|---|---|---|
| Type expansion (Fairy, type chart) | wanted | |
| Pokedex / species-slot expansion | wanted | Hardlove goes to 1476 slots including forms, megas, regionals |
| Move expansion (924 move records) | wanted | Includes move effects, animations, text |
| Ability expansion (u16 IDs to 318+) | wanted | Includes ability effects in the battle engine, not only the table |
| Battle AI updates | wanted | Platinum's own trainer AI (in `src/battle/trainer_ai/`) is the baseline, updated to know the new moves and abilities and with all eleven ds-pokemon-hacking battle_edits fixes applied (Ian confirmed applying the full list, 2026-09-15; see tracker Phase 4). Hardlove's AI is **not** ported. References Ian uses: lhearachel's Gen 4 AI gist (ff61af1f58c84c96592b0b8184dba096), pokemow.com/Gen4/TrainerAI/ and its switching page |
| Other engine changes | **decided 2026-09-20** | Ian answered all ten Phase 4 questions; the record is `docs/oxide/phase4-engine-change-answers.md` and the list is reproduced below. Forms use `(form << 11) \| species` encoding in encounter and trainer records |
| Hidden abilities | wanted | Full mechanic: a third ability slot per species, the script flag that lets chosen encounters roll it, and Ability Patch as the player-facing route. The base ROM's 228 duplicated second slots stay as they are for now |
| Items | wanted, curated subset | Not the 2,687-record table. New items go into Platinum's free slots, chosen by category; see the answers file for the in and out lists. Gems, Megas, extra balls, Gen 7-8 held items and new evolution items are all out |
| Evolution records | wanted | Nine slots per species, up from seven, because Eevee's seven are full and Sylveon makes eight. The 17 unreachable trade entries the base ROM left behind are stripped in the same pass. Hardlove's 19 extra evolution **methods** are not ported; the pick-list only uses methods Platinum already has |
| Save format | breaks freely | PKHeX compatibility is explicitly not a goal. 30 PC boxes, expanded dex flags, expanded bag. Fresh saves only |
| Mega Evolution | out | Gyarados M and Lopunny M are ordinary permanent evolutions, triggered by level-up holding an item entered as methods 18 and 19. No stones, no battle UI |
| Experience formula | out | Platinum's flat Gen 4 formula stays; the base ROM's trainer curve was tuned against it |
| Learnset format | wanted | Widened to (u16 level, u16 move). Forced: Platinum packs both into one u16 and caps the move id at 511, and there are 924 moves |
| Quality-of-life toggles | mixed | In: always-set battle mode, 60 fps outside battle, wild double battles, single-use items restored after battle, always national dex, script-driven level caps, a lowered friendship evolution threshold, fast text. Out: transparent textboxes, capture experience, critical capture, static HP bar. **A faster HP bar replaces the static-bar toggle** and is a base-ROM carry-over, not a new feature |
| Followers | deferred | Out of Phase 4. The species port's overworld sprite import should still cover every species so it stays possible |
| Physical/special split | n/a | Platinum already has it |

Content that rides along with the engine (Ian, 2026-09-15). This is the minimum; more may be added later.

| Content | Status | Notes |
|---|---|---|
| New species' base data | wanted, subset | Not every Hardlove species comes over. Ian will cut the chaff; the port needs a species pick-list he can edit, and the tooling must handle a sparse selection rather than a 1:1 copy of all 1476 slots |
| New moves | wanted, all | Including the move's battle script, sprites and animations, not only the 16-byte data record |
| New abilities | wanted, all | Every ability Hardlove has, effects included |
| Hardlove's randomized types, stat changes, encounter tables, trainers, story edits | out | The Platinum base keeps its own content |

## 4. Approach: DECIDED. Approach C, build from the pokeplatinum decomp (Ian, 2026-09-15)

The project's ROM is built from source in Ian's fork of `pret/pokeplatinum`. Claude edits the source tree, builds, commits and pushes from the WSL2 checkout; Ian plays the result (setup in `docs/oxide/setup-fork-and-wsl2.md`). hg-engine's source is the reference implementation for each feature; Hardlove's tables are the content source. The base ROM (`Platinum Unlocked v1.1`) is a reference for re-creating Ian's earlier edits, not the thing being patched; its inventory is `docs/oxide/phase3-base-rom-inventory.md`, and Phase 3 (the tracker) records how each of those edits was carried over.

### How this was decided

Phase 1 (2026-09-15) established that every scoped element is code plus data: type, ability, move and species expansion each depend on hooks and byte patches into HeartGold's arm9 and battle overlay, plus regenerated NARCs, so nothing in scope is achievable at the data layer alone (`docs/oxide/phase1-hg-engine-survey.md` sections 1 and 3). That ruled out approach A (data-layer only, DSPRE and scripts). Phase 2 compared the remaining two, (B) re-targeting the hg-engine patch kit onto Platinum from plat-engine's skeleton and (C) building from the pokeplatinum decomp, in `docs/oxide/phase2-approach-breakdown.md`, and recommended C after verifying that the decomp is 100% C, builds a byte-matching Rev 1 ROM in about 8 minutes, and is actively maintained. Ian approved C the same day.

The facts that carried the decision, kept here because they still shape Phase 4: hg-engine is a patch kit over vanilla HeartGold, so its addresses are useless in Platinum and only its design and C carry over; plat-engine is the same patch-kit design for Platinum, dormant since 2023 and roughly 10% along, useful only as a second address reference; pokeplatinum is the address oracle and the source base, and no public decomp-based Platinum hack has done a dex, type or ability expansion, so that part is new ground.

## 5. Working rules for Claude

These are standing instructions. Follow them every session.

1. Work on branch `oxide`. Never commit to `main`; `main` tracks upstream pret and is the vanilla reference (`git show main:<path>`).
2. Everything in the working folder is a copy and may be modified, the Hardlove ROM and its extraction included. Still, keep the donor recognizably the donor: if an experiment changes it, say so and note it in the findings log, so a later comparison against it is not silently comparing against an altered file. Nothing outside the working folder is touched by this project.
3. Never delete, move, or overwrite the base ROM (`Platinum Unlocked - Challenge - Adjusted v1.1.nds`) in the working folder, or its pinned copy `~/roms/base.nds`. It is what every verify tool compares the build against and the only source for the Phase 3 hard stops. The pinned `~/roms/vanilla.nds` is the vanilla reference for `import_base_rom.py --vanilla` and `verify_narcs.py --ref`; don't rebuild it per session.
4. Raw bytes are the source of truth. DSPRE's interpretation of a record, especially abilities and anything with a widened field, may be wrong for expanded data. Several base-ROM differences turned out to be DSPRE re-saves rather than edits; the tracker records the evidence for each.
5. Every data change is verified by rebuilding (`make rom`) and comparing the result against the reference ROM with the tools in `tools/oxide/`. Never rebuild a file's contents from a tool result that might be truncated. Read the file, modify, write. Edit `res/` JSON through `jsonstyle.py` or by hand in the same style; never reformat whole files.
6. New files live in the repo: scripts in `tools/oxide/`, notes and generated tables in `docs/oxide/`. The working folder receives mirrors from `sync-docs.sh`, never originals. Notes written on the chat surface land in the working folder's `notes\` and are brought into `docs/oxide/` when they matter to the work.
7. When something is unknown, say it is unknown. Do not fill the gap with an assumption about what the ROM contains; open the file.
8. Ian's writing preferences are listed once, in `CLAUDE.md`. Follow them.
9. Ask up front when a task branches on something only Ian can answer. He would rather be asked than watch a wrong guess get built.
10. Update the tracker at the end of every session. Update this document when a fact in section 2 changes or a decision in section 3 or 4 is made, and bump the version and date at the top. If any file under `docs/oxide/` changed this session, run `tools/oxide/sync-docs.sh`.
11. One status home per track. The tracker is for Phases 0 to 5; `docs/oxide/encounter-tool-build-plan.md` is for the encounter tool, which keeps exactly one paragraph at the top of the tracker and nothing else there. A fact is written in one place and pointed at from the others. A parallel session works on its own branch or worktree and merges into `oxide` when its tests are green.
12. Do not "improve" a carried-over map, script or table while a faithful carry-over is being verified; `checkmap.py` and the bulk tools compare against the base ROM. Cleanups are backlog items done afterwards as their own commits, so the faithful copy and the improvement are separable in the history.

## 6. Session protocol

The start-of-session and end-of-session steps are the `oxide-session` skill in `.claude/skills/`; the short form is in `CLAUDE.md`.

If the working folder on G: cannot be reached, everything needed to build and verify is in the repo and `~/roms/`; only `sync-docs.sh` is affected, and it says so and exits cleanly.

## 7. Open questions for Ian

- ~~Is Hardlove Gold built on hg-engine?~~ Answered: yes.
- ~~The exact scope list (section 3). Which of the "other engine changes" are wanted.~~ Answered 2026-09-20: `docs/oxide/phase4-engine-change-answers.md`, reproduced in section 3.
- ~~Whether Platinum Unlocked v1.1's own modifications need to be preserved.~~ Answered: the tags are irrelevant, treat it simply as a non-vanilla base.
- ~~How much of Hardlove's content is wanted alongside its engine.~~ Answered: see the content table in section 3.
- ~~Which species make the cut.~~ Answered 2026-09-15: `docs/oxide/species-pick-list.md`. Two follow-ups remain, both listed there and in the tracker: the 21 native species where the sheet and the base ROM disagree on base stats, and the evolution triggers for Gyarados M and Lopunny M.
- ~~The five **Q**s in `docs/oxide/phase3-base-rom-inventory.md` section 2 (which of the base ROM's code patches to keep).~~ Answered: `docs/oxide/phase3-answers-and-trainer-format.md`.
- ~~Fork URL and token or patch-file choice.~~ Answered: fork at `iradspinner/pokeplatinum`, pushes work from the WSL2 checkout with Ian's own credentials.
- ~~The species-ID scheme for Phase 4.~~ Answered 2026-09-20: ids are dense and appended after Arceus, `docs/oxide/species-id-scheme.md`.
- Whether any of the base-ROM differences judged to be DSPRE noise (sprite heights, encounter `unown_table`/`rate_form`) were in fact intended. Default is to leave vanilla.

## 8. Findings log

Durable facts discovered during work, newest last. Each entry: date, what was checked, what was found. Track agents only append. An entry may be deleted once its lesson lives in a working rule, a skill, a tool or a status home and the entry no longer changes what a fresh agent would do; such deletions are made in a docs pass with every track paused, because `integrate.sh` resolves a conflict in this section by keeping both sides, which would resurrect a deleted entry next to a concurrent append.

- 2026-09-20: Phase 4 element 3 started with the ability list, because the 159 species need 59 ability ids Platinum does not have and the records cannot be written before those exist. The whole donor table came across rather than those 59: ids 0 to 123 already agree with Platinum's, so importing 124 to 318 contiguously makes a donor ability number and an Oxide one the same number for good, and spares every later import a lookup table. Names, uppercase names and descriptions are in `res/text`; the effects are element 5, so all 195 are inert until then. The principle is worth reusing for moves and items: where the donor's low ids already match, take the whole contiguous table rather than a sparse subset, because the saving is a few kilobytes of text against a permanent translation layer.
- 2026-09-21: Element 3's cries were broken in a way worth recording, because the shape of the mistake will recur. Generating an asset into `res/` is not the same as registering it: a cry needs a bank and a wave archive in `res/sound/pl_sound_data.json` at its own species id, because `Sound_PlayPokemonCry` indexes that bank table by species directly, and the first pass produced 159 `cry.wav` and `cry.txt` files without adding a single entry. The symptom was silence plus a hard crash on the Pokedex cry screen, found by Ian in the emulator and not by any check in this repo. Two facts to keep. **A cry has a size ceiling**: `PLAYER_PV`'s heap is 24,200 bytes and must hold the bank and the whole wave at one byte a sample after the build's PCM8 conversion, so the practical limit is vanilla's longest cry, Jynx's 23,524 samples; HeartGold trims less and 41 donor cries were over it. **And `nitrosfx` has a latent bug**: `WriteSdat` writes the FAT, then pads the first file's data to a 0x20 boundary, but computes the FAT offsets without that padding, so every file in the archive reads a few bytes early. It never shows for the unmodified game because that padding is zero there; growing SYMB, INFO or FAT enough to move the FILE block exposes it. Fixed in `tools/nitrosfx/sdat.c` with a change that is a no-op when the padding is zero, so a matching build is unaffected. It belongs upstream.
- 2026-09-21: A process failure worth more than the bug it caused. Element 3 changed the save layout and nothing recorded it: the `Pokedex` struct sizes itself from `NATIONAL_DEX_COUNT`, so raising the species count grew it by about 239 bytes on its own, and because `gSaveTable` lays `SAVE_BLOCK_ID_NORMAL` out as a running total with the Pokedex eighth of roughly forty entries, every block after it moved. The session protocol already says a change that moves anything in the save gets a row in `docs/oxide/save-layout.md`; the rule was followed for element 2, where the move was deliberate and obvious, and missed for element 3, where it was a side effect of a constant changing. **The lesson is that the trigger for that rule is not "did I edit a save struct" but "did anything sized by a constant I changed end up in the save table".** Two hangs Ian found on 2026-09-21, Nurse Joy and the box deposit screen, are both on paths that write blocks after the Pokedex, and are waiting on a new save to say whether they are real. The row is written now, and `save-layout.md` says which blocks moved.
- 2026-09-21: The whiteout hang was a script-alignment defect, and it teaches two things. First, the ARM9 drops the low address bit on halfword loads, and field-script movement blocks are arrays of halfword commands, so a movement block at an odd offset reads as garbage actions; vanilla puts `.balign 4, 0` before every movement label for exactly this reason, and the bulk-generated scripts do not, because they reproduce the base ROM's own padding byte for byte. That is safe only while a generated file keeps its length; the Repel fix shortened `scripts_common` by 15 bytes and broke every movement block behind the edit. Second, the Windows melonDS 1.1 GDB stub is usable from WSL2 under mirrored networking but with two limits: one client per emulator session (a dropped client wedges the stub until restart) and no servicing while the CPU runs, so a target cannot be interrupted on demand; what works is connecting at the startup break, planting breakpoints, continuing, and reading memory or single-stepping at each stop. `tools/oxide/live_watch.py` does that with arm-on, hold-at, burst, auto-command and function-level trace modes, and the sequence that found this bug (heartbeat breakpoints to prove the main loop ran, then stage breakpoints to find the frame, then object and pointer reads at the script's movement commands) is a reusable method for any freeze.
- 2026-09-21: Docs pass. Thirty entries from 2026-09-15 to 2026-09-20 were deleted from this log under the rule in the paragraph above, each after checking that its lesson lives in a working rule, a skill, a tool or a status home; the commit that made the pass names every deleted entry and where its lesson now lives.
- 2026-09-21: Auditing element 3's remaining caps found one live defect and one ceiling. **The defect:** `Pokemon_GetFormNarcIndex` in `src/pokemon.c` hardcoded 496, 499, 501, 502 and 503 as the `pl_personal` and `wotbl` members that hold the twelve alternate-form records. Those two archives put the form records after every species and after EGG and BAD_EGG, so inserting 159 species moved them to 655 onward and the five literals began reading new species' records instead. The three Deoxys forms, both Wormadam forms, Giratina Origin, Shaymin Sky and the five Rotom forms would every one of them have had the wrong base stats, types, abilities and level-up learnset. They now derive as `MAX_SPECIES + n` in `include/constants/forms.h`, written beside the `MOVESET_FORM_*` block, which derives as `NATIONAL_DEX_COUNT + n` because the tutor table it indexes has no egg entries; the two bases differ by exactly those two eggs and both are now written down. Verified twice: against the pinned vanilla build, where `MAX_SPECIES + 1` is 496 and the new expression reproduces the old literals exactly, and against the current build, where 655, 658, 660, 661 and 662 hold the expected form stats. **The general rule: a literal that happens to equal a derived constant is a latent bug from the moment the constant moves**, and the species insertion moved four numbering schemes at once (species ids, dex numbers, form-record indices, tutor-table indices), so a bare number near a species-indexed table earns a check rather than a glance. Everything else audited derives correctly and needed no change, including the `zukan_enc_platinum` stride, whose archive is generated at `4 + MAX_SPECIES * 10` and already holds 6,544 members. **The ceiling:** `BattleHallWinRecords` is three `u16[MAX_SPECIES]` arrays and lives in the *extra* save table, whose entries sit at fixed sector numbers with no bounds check at all, `SaveDataExtra_Save` writing its bytes straight at `blockID * SAVE_SECTOR_SIZE`. Its entry is one sector wide, and at 654 species the struct plus footer is 3,948 of the 4,096 bytes, which caps `MAX_SPECIES` at 679 before it overruns the stored battle recordings. Nothing to do at 654; recorded in `docs/oxide/save-layout.md` so a later species addition moves the entry rather than growing into its neighbour.
- 2026-09-21: Footprints are a Generation 4 feature, which settles one of element 3's fill-in items rather than leaving it open. Black and White dropped the footprint from the Pokedex and Black 2 has no archive of them, checked by scanning every NARC in the ROM for one of the right shape. Every one of the 159 new species is Generation 5 or later, so **no game has ever drawn a footprint for any of them** and `"has": false` is the correct value, not a gap, for 147 of them. The 12 that can be done properly are the regional forms, the megas and the cross-gen evolutions, which are the same creature as a Generation 4 native and take that native's print. Two of those, Galarian Weezing and Mega Gyarados, inherit `false`, because Weezing and Gyarados have no feet. The general shape of this: before filling a gap with invented data, check whether the gap is the data. The same question is worth asking of the dex size-comparison scales, which are still defaults.
- 2026-09-21: The integration gate protects authored encounter tables only as far as `authored_encounters()` in `tools/oxide/import_base_rom.py` knows how to recognise them. Step 5 authored the surf and rod tables of eleven water-only areas, which have no land `cast`, and the importer's dry run wanted to restore the base ROM's species over them; had the gate been ignored, the next real import would have done it. Any new way of authoring a table (a new sidecar key, a new file kind) has to extend that function and `test_step0`'s mirror of it in the same commit.

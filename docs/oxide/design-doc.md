# Platinum Oxide: Hardlove Gold engine-expansion integration into Pokemon Platinum

Design document, v0.13 (2026-09-20). This file is written for Claude to work from. Read it in full at the start of every session, then read `Platinum Oxide - Tracker.md`, then act.

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
| `Platinum Unlocked - DSPRE contents\Platinum Oxide VSMaker2 Data\` | A VSMaker2 extraction (arm9.bin, overlays, data, unpacked). Trainer-editing tool data. Not yet examined. |
| `Hardlove Gold NDS (0.6.9).nds` | The donor ROM. 192 MB. Gamecode IPKE. This is a copy; the playable original lives in `G:\PokeROMs\HeartGold Roms`. Writing to this copy is allowed (for example to test a theory about where something lives), but it stays the donor, not a deliverable. |
| `Hardlove Gold NDS (0.6.9)_DSPRE_contents\` | DSPRE extraction of the donor. Same layout. Also a copy; writable. |

Everything in this folder is a copy. Ian has confirmed (2026-09-15) that any file here, including the Hardlove ROM and its DSPRE contents, may be modified. The originals in the hub folder and in `HeartGold Roms` are untouched by this project.

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

hg-engine is a patch kit applied to a vanilla US HeartGold ROM, not a rebuilt game. Compiled C goes into new overlays 129..151 (129 is loaded at boot as a permanent arm9 extension); ~1,370 lines of hook/repoint/byte-replacement lists and ~3,200 lines of armips patches edit the vanilla arm9 and overlays at fixed addresses; ~40 NARCs are regenerated from source data. Hardlove's extraction shows exactly this (overlays 129..151 at hg-engine's load addresses, hg-engine's species and move numbering). Full detail: `notes\phase1-hg-engine-survey.md`.

Consequence: none of hg-engine's addresses exist in Platinum. Porting means re-targeting the same design onto Platinum's binaries (or rebuilding from Platinum's decomp), not copying files.

### Tooling already built (Hardlove side)

`romtool\hardlove.py` in the hub folder has working readers and writers for the NDS filesystem, NARC pack/unpack (verified byte-identical round trip), personal, evolution, encounter and trainer layers. `Rom.write_file` refuses size-changing writes. This is HeartGold-shaped code and will need a Platinum sibling, but the NARC and ROM layers are game-agnostic and should be reused rather than rewritten.

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
| Other engine changes | undecided | The full menu of what hg-engine offers is in `notes\phase1-hg-engine-survey.md` section 3 (items, megas, hidden abilities, exp formula, evolution methods, trainer customization, PC boxes, 60 fps, set mode, level caps, reusable TMs, and about a dozen smaller toggles). Ian picks from that list. Forms use `(form << 11) \| species` encoding in encounter and trainer records |
| Physical/special split | n/a | Platinum already has it |

Content that rides along with the engine (Ian, 2026-09-15). This is the minimum; more may be added later.

| Content | Status | Notes |
|---|---|---|
| New species' base data | wanted, subset | Not every Hardlove species comes over. Ian will cut the chaff; the port needs a species pick-list he can edit, and the tooling must handle a sparse selection rather than a 1:1 copy of all 1476 slots |
| New moves | wanted, all | Including the move's battle script, sprites and animations, not only the 16-byte data record |
| New abilities | wanted, all | Every ability Hardlove has, effects included |
| Hardlove's randomized types, stat changes, encounter tables, trainers, story edits | out | The Platinum base keeps its own content |

## 4. Approach: DECIDED. Approach C, build from the pokeplatinum decomp (Ian, 2026-09-15)

The project's ROM is built from source in Ian's fork of `pret/pokeplatinum`. Claude edits the source tree and pushes; Ian pulls and runs `make rom` in WSL2 (setup in `notes\setup-fork-and-wsl2.md`). hg-engine's source is the reference implementation for each feature; Hardlove's tables are the content source. The base ROM (`Platinum Unlocked v1.1`) is now a reference for re-creating Ian's earlier edits, not the thing being patched; its inventory is `notes\phase3-base-rom-inventory.md`.

### Background: how this was decided

Answered by Phase 1 (2026-09-15): every scoped element is code plus data. Type, ability, move and species expansion each depend on hooks and byte patches into HeartGold's arm9 and battle overlay, plus regenerated NARCs. Nothing in scope is achievable at the data layer alone. See `notes\phase1-hg-engine-survey.md` sections 1 and 3.

The approach is not decided. Ian has asked for a detailed breakdown of the considerations before choosing; do not pick one without that conversation. The three candidates, with what Phase 1 established about each, are in the notes file section 6: (A) data-layer only, ruled out; (B) re-target the hg-engine patch kit to Platinum, starting from plat-engine's skeleton; (C) build from the pokeplatinum decomp source. The breakdown for Ian is the first Phase 2 deliverable.

Known context that bears on the choice, from `claude/engine-tooling-comparison.md`:

- **Hardlove Gold is built on hg-engine (BluRosie). Confirmed by Ian, 2026-09-15.** So "Hardlove's engine expansion elements" means hg-engine's, and the hg-engine repository (source, `CONFIG.md`, wiki) is the primary reference for what each expansion is and where it lives in the built ROM. Hardlove's own additions on top of hg-engine are content, not engine, unless investigation shows otherwise. Phase 1 should start from hg-engine's source tree rather than from blind inspection of the donor ROM.
- plat-engine (lhearachel) is a direct hg-engine-style patch kit for Platinum, not a decomp build (the earlier project note had this wrong). It has the loader, 107 Platinum function addresses, 16 hooks into arm9/ov16, a partial damage calculator, and the Fairy plate patch. It lacks the ability widening, move repoints, dex/save expansion, cries, animations and most everything else. Last commit 2023-08-19.
- pokeplatinum (pret) is 100% C (no assembly left), builds matching US Rev 0 and Rev 1 ROMs, and is actively maintained (last commit 2026-09-12). Verified 2026-09-15: a matching Rev 1 ROM built in Claude's workspace in ~8 minutes; incremental rebuild 29 s. It is the address oracle for approach B and the source base for approach C.
- Phase 2 breakdown written: `notes\phase2-approach-breakdown.md`. Recommendation: approach C. Awaiting Ian's decision and the four logistics answers in its section 7.
- DSPRE is a data editor with no path to any of the (b) items on its own.

## 5. Working rules for Claude

These are standing instructions. Follow them every session.

1. Everything in the working folder is a copy and may be modified, the Hardlove ROM and its extraction included. Still, keep the donor recognizably the donor: if an experiment changes it, say so and note it in the findings log, so a later comparison against it is not silently comparing against an altered file. Nothing outside the working folder is touched by this project.
2. Back up the base ROM before any write to it, as a timestamped copy in the working folder. Say which backup was taken.
3. Close DSPRE before any script writes to the ROM or to `files\`; DSPRE holds its own copy and will overwrite on save. Reopen it afterward.
4. Raw bytes are the source of truth. DSPRE's interpretation of a record, especially abilities and anything with a widened field, may be wrong for expanded data.
5. Never rebuild a file's contents from a tool result that might be truncated. Read the file, modify, write.
6. New files go next to their source in the working folder. Scripts go in a `tools\` subfolder; investigation notes and generated tables go in `notes\`. Do not scatter output into the DSPRE extractions.
7. When something is unknown, say it is unknown. Do not fill the gap with an assumption about what the ROM contains; open the file.
8. Match Ian's stated preferences: prose over bullets except for actual lists, no em-dashes, succinct, do not open by grading his message, do not assume he is the expert on a question he asked.
9. Ask up front when a task branches on something only Ian can answer. He would rather be asked than watch a wrong guess get built.
10. Update the tracker at the end of every session. Update this document when a fact in section 2 changes or a decision in section 3 or 4 is made. Note the version and date at the top. If any `docs/oxide/*.md` file changed this session, run `tools/oxide/sync-docs.sh` to mirror it to the project folder, which a separate chat surface works from.
11. Never delete, move, or overwrite the base ROM (`Platinum Unlocked - Challenge - Adjusted v1.1.nds`) in the working folder. It is the only source left for the carry-overs not yet done: encounters, text, items, trades, trainers, map headers, and the 91 scripts with their 158 event files. Keep it until that carry-over is finished.
12. `import_base_rom.py --vanilla` and `verify_narcs.py --ref` (for vanilla comparisons) should point at the pinned `~/roms/vanilla.nds`, a byte-exact Rev 1 build made once from `main`, rather than a freshly built ROM. Don't rebuild it per session.

## 6. Session protocol

Start: read this doc, read the tracker, confirm the working folder is reachable (list it), state in one or two sentences what this session will do.

During: keep the tracker's "In progress" line current if the session is long.

End: tick off what was done, add what was learned to section 8 of this doc if it is a durable fact, add follow-ups to the tracker's backlog, bump the version if this doc changed.

If the folder cannot be reached (the device link drops), work from whatever is already staged and say so plainly; do not reconstruct files from memory.

## 7. Open questions for Ian

- ~~Is Hardlove Gold built on hg-engine?~~ Answered: yes.
- The exact scope list (section 3). Which of the "other engine changes" are wanted.
- ~~Whether Platinum Unlocked v1.1's own modifications need to be preserved.~~ Answered: the tags are irrelevant, treat it simply as a non-vanilla base.
- ~~How much of Hardlove's content is wanted alongside its engine.~~ Answered: see the content table in section 3.
- ~~Which species make the cut.~~ Answered 2026-09-15: `docs/oxide/species-pick-list.md`. Two follow-ups remain, both listed there and in the tracker: the 21 native species where the sheet and the base ROM disagree on base stats, and the evolution triggers for Gyarados M and Lopunny M.
- ~~The five **Q**s in `notes\phase3-base-rom-inventory.md` section 2 (which of the base ROM's code patches to keep).~~ Answered: `docs/oxide/phase3-answers-and-trainer-format.md`.
- Fork URL and token or patch-file choice (`notes\setup-fork-and-wsl2.md` Part 1).

## 8. Findings log

Durable facts discovered during work, newest last. Each entry: date, what was checked, what was found.

- 2026-09-15: Folder inventory done. Counts in section 2 are from listing `unpacked\personalPokeData` and `unpacked\moveData` in both extractions. Platinum base is CPUE rev 1; Hardlove is IPKE rev 0.
- 2026-09-15: Base ROM's "Unlocked / Challenge - Adjusted" tags are old hand edits with no relevance here (Ian). Content scope set: subset of new species, all new moves with scripts/sprites/animations, all new abilities.
- 2026-09-15: Hardlove Gold is an hg-engine build (Ian confirmed). This reframes Phase 1: the engine expansions are hg-engine's, documented in its repo, and Hardlove is one instance of them plus content.
- 2026-09-15: Phase 1 survey done; full write-up in `notes\phase1-hg-engine-survey.md`. Headlines: hg-engine is a patch kit over vanilla HG (overlays 129..151, ~1,370 hook/patch lines, ~3,200 armips lines, ~40 regenerated NARCs, ~49k lines of C); Hardlove's overlay table and numbering match it exactly; every scoped element needs code patches; plat-engine is the same design for Platinum but dormant since 2023 and roughly 10% along; pokeplatinum is a matching, active decomp.
- 2026-09-15: Base ROM caution. Its `arm9.bin` and `ov016.bin` were modified on 2026-08-25 and a dozen data NARCs on 2026-08-30 (DSPRE saves). Diff arm9 and ov16 against vanilla Rev 1 before trusting any address from plat-engine or pokeplatinum.
- 2026-09-15: `Platinum Oxide VSMaker2 Data\` is a complete stale second extraction of the base ROM (2026-08-04) sitting inside the DSPRE contents folder. Not read by DSPRE. Do not source tables from it.
- 2026-09-15: Approach C feasibility verified. pokeplatinum has zero remaining assembly; `make rom` in the workspace produced SHA-1 `0862ec35b24de5c7e2dcb88c9eea0873110d755c` (retail Rev 1). Compiler is Metrowerks via metroskrew, fetched from GitHub, needs 32-bit libc on Linux. Three public decomp-based Platinum hacks exist (Coarse Platinum, Tempered Platinum's plat-hack-decomp, pokeaotea); none has done a dex/type/ability expansion. Delivery constraint: a 128 MB ROM cannot be written to Ian's folder from the workspace (20 MB per-file cap), so either Ian builds locally from a GitHub fork or Claude delivers a BPS/xdelta patch.
- 2026-09-15: Approach C approved by Ian. Base-ROM edits to preserve: overworld events, trainer edits, Pokemon stat and move edits. Battle AI is in scope as an engine change; Hardlove's AI is not wanted.
- 2026-09-15: Base ROM diffed against the vanilla build. 32 NARCs differ (409 species, 108 moves, 488 trainers with an expanded party format, 125 encounter tables, 91 scripts, 158 event files, 78 text banks, ~100 map-header weather bytes, plus tool re-saves). arm9 differs at 38 places and 11 overlays differ: a DSPRE synthetic overlay carrying EV/IV viewer, no-items, frame unlock and candy-chaining routines; a rewritten `TrainerData_BuildParty` (expanded trainer format); shiny/palette hooks; custom script commands over Battle Arcade code; vitamin EV cap 252; ov14 AI bug fixes. Full report: `notes\phase3-base-rom-inventory.md`. Raw diffs: `notes\diff\`.
- 2026-09-15: Fork `iradspinner/pokeplatinum` cloned; builds to the retail hash. Branch `oxide` holds the work. `tools/oxide/` has `jsonstyle.py` (writes the repo's JSON style and edits single keys in place so diffs stay minimal), `import_base_rom.py` (base ROM to res/ for species, moves, evolutions, learnsets) and `verify_narcs.py` (rebuilt NARC vs reference ROM). First import verified byte-identical. Note the base ROM set hatch cycles to 1 on 228 species and filled the second ability slot on 228; both carried over as-is.
- 2026-09-15: GitHub push from this session needs the repo added as a session source in the Claude app; a token file cannot be used because the app's proxy strips credentials. Until then, commits stay local to the session (and are lost with it), so push as soon as access exists.
- 2026-09-15: Platinum file map for the scoped data (from plat-engine's narcs.mk, confirmed present in the extraction): personal `poketool/personal/pl_personal.narc`, evolutions `evo.narc`, learnsets `wotbl.narc`, moves `poketool/waza/pl_waza_tbl.narc`, battle scripts `battle/skill/waza_seq.narc` / `be_seq.narc` / `sub_seq.narc`, sprites `poketool/pokegra/pl_pokegra.narc`, icons `poketool/icongra/pl_poke_icon.narc`, dex `resource/eng/zukan/zukan.narc`, text `msgdata/pl_msg.narc`, trainers `poketool/trainer/trdata.narc` + `trpoke.narc`. Type chart is `sTypeMatchupMultipliers` in pokeplatinum `src/battle/battle_lib.c` (overlay 16). Ability is a u8 in the mon struct and battle-mon struct.
- 2026-09-15: Ian answered the five Qs from `phase3-base-rom-inventory.md` section 2. Full detail in `docs/oxide/phase3-answers-and-trainer-format.md`. Headlines: port all four synthetic-overlay routines (EV/IV viewer, no items in trainer battles, frame-rate unlock, Rare Candy chaining) as ordinary C changes, hg-engine's compile-time toggles are the reference for each; the shiny-odds raise (`Pokemon_IsPersonalityShiny+0x18`, threshold 8 to 0xFF, about 1/8192 to 1/257) is a one-constant port, the separate IV/nature-driven palette hue shift is deferred as low priority and droppable if it proves opaque; the custom script commands overwritten into the Battle Arcade code region port only if the carried-over field scripts actually call them, determined during the script carry-over rather than guessed now; apply all eleven ds-pokemon-hacking battle_edits fixes (Ian applied most already and could not recall which one he skipped, so under approach C all eleven are applied fresh from the guide rather than recovered from ROM bytes).
- 2026-09-15: Correction to `phase3-base-rom-inventory.md` section 2B. The base ROM's trainer party data is **vanilla format, not expanded**: per-trainer record lengths match `partySize * perMonSize` for the vanilla per-mon sizes (8/16/24/32 bytes) on 926 of 928 trainers, the other two off by NARC alignment padding that vanilla itself also has. The earlier 16/32/48/108-byte reading was real but came from Ian giving many more trainers full six-Pokemon custom parties, not from a wider struct. The one genuine non-vanilla piece is the high byte of the per-mon `ivScale` u16 (zero in vanilla, used on 207 of 1,878 mons here): its low nibble forces gender (buggy in the base ROM's compiled patch, always takes the same branch regardless of intended direction) and its high nibble forces ability slot 1 or 2. Consequence: no trainer struct/loader expansion is needed. `res/trainers/data/*.json` already holds everything vanilla carries; the carry-over needs only two new optional per-mon fields (`ability`, `gender`) plus a trainer importer. Detail and the four-step plan: `docs/oxide/phase3-answers-and-trainer-format.md` section 2.
- 2026-09-19: EV/IV viewer ported, closing the fourth and last synthetic-overlay routine. Read out of the base ROM's own `EV+IV_Viewer` routine rather than hg-engine: `HandleInput_Main+0x34` is spliced so R cycles a mode byte at `0x023C815D` through 0/1/2 and calls `ChangeSummaryMon(screen, 0)` to redraw; `SetMonDataFromMon+0x1B2` is spliced so the seven stat reads become `MON_DATA_HP_IV..MON_DATA_SPDEF_IV` in mode 1 and `MON_DATA_HP_EV..MON_DATA_SPDEF_EV` in mode 2, both written over `curHP/maxHP/attack/...` with HP duplicated into both halves of the "cur/max" pair. In the decomp the IVs and EVs get their own arrays so the real stats survive, because overwriting them makes `DrawHealthBar` divide by zero on a mon with 0 HP EVs. Also corrected: `HandleInput_SelectMove+0x8E`, listed in the inventory as a viewer hook, is really the HM-forget edit (`Item_IsHMMove` call replaced by `nop; movs r0, #0`) and still needs porting with the other small constant edits.
- 2026-09-20: Encounter, trade and text carry-over. 125 encounter tables and both edited in-game trades imported and verified; 18 of the 78 differing text banks imported (the ones whose message count is unchanged), including the base ROM's own options-menu relabel to UNLOCK FPS / OFF / BATTLE / ALWAYS. Three separate cases of DSPRE normalisation were identified and deliberately not carried over, each with the evidence recorded in the tracker: `height.narc` (only the male offset changed on 116 species that had male == female, plus 164 bytes written into members vanilla leaves empty), the six vitamin item records (34 bytes grown to 36 with fields shifted one byte right), and the encounter `unown_table` / `rate_form` fields (a 1-based rewrite plus every Solaceon Ruins room set to the two-form secret set). The `{TRNAME}` tag the base ROM carries on every trainer name is the same kind of thing: vanilla and trainerproc leave it off for rivals, the Frontier brains and the Battleground trainers, so it is stripped on import. The relabelled menu also exposed two real defects in the frame-rate uncap: `ShouldWaitForVBlank` compared a saved-option value against `enum ButtonMode` constants (correct only by numeric coincidence), and `ApplyButtonModeToInput` still remapped for `BUTTON_MODE_L_IS_A`, which is what the "ALWAYS" entry sets, so uncapping everywhere also made L act as A and cleared L and R. The base ROM disables all button remapping outright; so does this fork now.
- 2026-09-20: Correction to the 2026-09-15 GitHub note above. That was about pushing from the Claude app's workspace. From the WSL2 checkout in `~/pokeplatinum`, `git push origin oxide` works with Ian's own credentials and has done so on every attempt, so commits are not session-local and do not need patch files as a fallback.
- 2026-09-20: Species pick-list landed in the repo (`docs/oxide/species-pick-list.md` and `.csv`), produced on the chat surface from `New Pokedex.xlsx`. 360 rows, 159 new slots, 652 species in the finished ROM. It is an availability list, not a deletion list: every Platinum native stays in the tree because the carried-over trainers use species the curated dex omits, and National Dex IDs stay as internal species IDs so the donor's dex-plus-50 rule keeps working. Its 21-row sheet-vs-base-ROM conflict table was checked against `res/pokemon` here and every base-ROM value matches what Phase 3 imported.

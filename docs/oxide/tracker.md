# Platinum Oxide: Tracker

Top-level task list. Tick items as they finish; add detail only where it changes what happens next. Companion to `Platinum Oxide - Design Doc.md`.

**In progress:** Phase 3. Species/move/evo/learnset import done, verified against `~/roms/base.nds` with a full `make rom` + `verify_narcs.py` pass (2026-09-15). Five Qs answered and the trainer format corrected to vanilla (`docs/oxide/phase3-answers-and-trainer-format.md`). Trainer ability/gender fields and game logic are done (2026-09-15); the base-ROM importer for them is not, pending an answer from Ian and a JSON-tooling decision (see Phase 3 checklist). A roadmap for the rest of Phase 3 and all of Phase 4, with file-level detail for the next several items, is in the session that did this work; ask if it needs to be written down again. Waiting on Ian: WSL2 setup confirmation, the species pick-list, the ability/gender nibble-direction question above

## Phase 0: Setup

- [x] Working folder created, both ROMs and both DSPRE extractions in place
- [x] Design doc v0.1 and this tracker written
- [x] Ian confirms Hardlove is an hg-engine build (2026-09-15)
- [x] Content scope set: species subset (Ian picks), all new moves with scripts/sprites/animations, all new abilities (2026-09-15)
- [ ] Ian finalizes the "other engine changes" list in design doc section 3
- [ ] Ian produces the species pick-list (needed before Phase 4 species port, not before)

## Phase 1: Find out where Hardlove's expansions live

Done 2026-09-15. Write-up: `notes\phase1-hg-engine-survey.md`.

- [x] Read hg-engine's repo structure, `CONFIG.md` and wiki; list every engine expansion and how each is injected
- [x] Map each scoped element to hg-engine source files and the ROM files it changes
- [x] Confirm the map against the Hardlove extraction (overlays 129..151 and numbering match; specific config toggles not determinable from the extraction)
- [x] Locate Platinum's type chart, ability field, species/move tables (named in design doc section 8; exact addresses come from a pokeplatinum build in Phase 3)
- [x] Check plat-engine's state (dormant since 2023-08, ~10% of hook surface, same architecture as hg-engine)
- [x] Inspect the VSMaker2 Data folder (stale duplicate extraction; ignore)
- [x] Write findings into design doc section 8

## Phase 2: Approach decision

- [x] Write the considerations breakdown for Ian (`notes\phase2-approach-breakdown.md`; recommends C; verified by building a matching ROM from the decomp)
- [x] Ian picks the approach: C (2026-09-15)
- [x] Ian answers the logistics questions: keep overworld/trainer/stat/move edits; has GitHub, will fork; wants a WSL2 runthrough; Phase 4 order approved; battle AI added as an engine change, Hardlove AI excluded
- [ ] Finalize the scope table in design doc section 3

## Phase 3: Tooling and setup (approach C)

- [x] Ian forks pret/pokeplatinum: https://github.com/iradspinner/pokeplatinum (2026-09-15)
- [ ] GitHub access for Claude: the token-file route does not work in this environment (the app's proxy refuses credentials for repos not added as session sources). Ian adds the repo as a source in the app; fallback is patch files
- [ ] Ian sets up WSL2 and builds the unmodified fork once (`notes\setup-fork-and-wsl2.md` Part 2)
- [x] Claude clones the fork and confirms a matching build from it (SHA-1 0862ec35..., 2026-09-15)
- [x] Diff the base ROM against vanilla (`notes\phase3-base-rom-inventory.md`)
- [x] Ian answers the inventory's five Qs (2026-09-15): port all four synthetic-overlay routines; shiny odds raise ports as a one-constant change, palette hue shift deferred/droppable; Battle Arcade script commands port only if the carried-over field scripts call them; apply all eleven battle_edits fixes. Full detail: `docs/oxide/phase3-answers-and-trainer-format.md`
- [x] Correction (2026-09-15): the base ROM's trainer party data is vanilla format, not expanded; no trainer struct/loader extension needed. See `docs/oxide/phase3-answers-and-trainer-format.md` section 2. Replaced by the four items below.
- [x] Add optional `ability` (0|1|2) and `gender` (null|"male"|"female") per-mon fields to trainer JSON and to `tools/dataproc/src/trainerproc.c` (commit 5b8958368)
- [x] Make `TrainerData_BuildParty` (`src/trainer_data.c`) honor those fields, implemented correctly (pick a personality that satisfies the requested gender for that species' ratio) rather than copying the base ROM's buggy +/-2 nudge (commit 5b8958368); verified by inspecting the built `trdata`/`trpoke` NARCs directly, unset fields decode back to ability=0/gender=0 matching prior behavior
- [ ] Extend `tools/oxide/import_base_rom.py` with a trainer importer for the 488 changed trainers, decoding `ivScale`'s low byte as `iv_scale`, high nibble as `ability`, low nibble as `gender`. Two open items found while scoping this: (1) `res/trainers/data/*.json`'s `party` is a list of objects, and the existing `jsonstyle`/`apply_diff` surgical patcher only replaces an existing key's value, so per-mon field patching needs either a new insertion helper or accepting whole-`party`-array replacement (format-fidelity against the current hand-formatted files unverified); (2) the base ROM's compiled ability/gender patch had a bug that made both low-nibble values behave identically in-game, so which raw nibble (1 or 2) was meant to mean male vs female can't be recovered from ROM bytes alone - **ask Ian** before committing the bulk carry-over
- [ ] Verify `poketool/trainer/trdata.narc` and `trpoke.narc` with `verify_narcs.py`; expect `trpoke` byte-identical apart from alignment padding once the ability/gender nibbles are re-encoded
- [ ] Port the four synthetic-overlay routines as ordinary C changes: EV/IV viewer (summary screen), no items in trainer battles, frame-rate unlock, Rare Candy chaining (hg-engine toggles: `IMPLEMENT_NEW_EV_IV_VIEWER`, `DISABLE_ITEMS_IN_TRAINER_BATTLE`, `BATTLES_UNCAPPED_FRAME_RATE`, level-cap candy behavior)
- [x] Conversion scripts for species, moves, evolutions, learnsets: `tools/oxide/import_base_rom.py` + `verify_narcs.py`; 415 species and 108 move files updated; rebuilt NARCs verified byte-identical to the base ROM (commit c69ef83 on branch `oxide`)
- [ ] Conversion scripts for encounters, heights, text, items, trades
- [ ] Carry over trainers (488 records) via the trainer importer above, once the ability/gender fields exist
- [ ] Carry over map-header weather edits (`include/data/map_headers.h`)
- [ ] Carry over scripts (91), events (158) and their text: disassemble, rewrite in the decomp's script macros, check each against its event file; ask Ian when intent is unclear. While disassembling, check whether any script calls the custom command IDs overwritten into the Battle Arcade code region (arm9 `0x05003C`-`0x0505BC`, `ScrCmd_Dummy088`); reimplement only those actually called, drop the rest
- [ ] Re-apply the small constant edits Ian wants as C changes: vitamin EV cap 100 to 252, shiny threshold 8 to 0xFF (~1/8192 to ~1/257), options defaults, HM forget
- [x] Working `git pull && make rom` loop with Ian, verified end to end with one visible change (2026-09-15): `make rom` succeeded on branch `oxide`; `verify_narcs.py` confirms personal/wotbl/evo/waza NARCs rebuild identical to `~/roms/base.nds`. Visible check pending Ian's emulator run: Shinx ability (should always be Rivalry, never Intimidate) and Bidoof/Starly egg hatch time (~255 steps, down from ~3825)

## Phase 4: Port, one element at a time

Order to be set after Phase 2. Each element gets its own checklist when it starts.

- [ ] Type expansion
- [ ] Ability expansion
- [ ] Move expansion (data, battle scripts, sprites, animations)
- [ ] Species-slot expansion (sparse: only the species on Ian's pick-list)
- [ ] Battle AI: Platinum baseline, teach it the new moves/abilities, apply all eleven battle_edits fixes (Ian confirmed applying the full list, 2026-09-15): Fire Fang vs Wonder Guard, Rage Glitch, Water Immunity vs Dry Skin check, Sunny Day check, Foresight/Odor Sleuth Ghost check, Facade status check, Leaf Guard Sunny Day logic, Water Spout/Eruption HP check, charge-turn scoring fix, Thunder scoring fix, Discharge double-battle scoring fix
- [ ] Other engine changes (Ian picks from the hg-engine menu)

## Phase 5: Verify

- [ ] Boots in emulator
- [ ] New game to first battle without crash
- [ ] A ported element visibly works in-game (for example: a Fairy-type move hits for the right effectiveness)

## Backlog / follow-ups

- Move `Platinum Oxide VSMaker2 Data\` out of the DSPRE contents folder (Ian's call; it is a stale duplicate)
- Open Hardlove's `a/0/2/8` to read the hidden-ability and base-exp tables directly (needed for the species port)
- Update the project doc `claude/engine-tooling-comparison.md`: plat-engine is a patch kit not a decomp build; pokeplatinum is matching and active
- Palette hue-shift patch (IV/nature-driven shiny or per-form palette, base ROM's eight palette-loading hooks): low priority, investigate only after Phase 4 is done; drop if it proves opaque (Ian, 2026-09-15)

## Decisions made

- 2026-09-15: Base ROM is `Platinum Unlocked - Challenge - Adjusted v1.1.nds`. Donor is Hardlove Gold 0.6.9.
- 2026-09-15: Everything in the working folder is a copy; the Hardlove ROM and its DSPRE contents may be modified. Originals elsewhere are never touched.
- 2026-09-15: Deliverables live in the working folder as markdown; the design doc is instructions for Claude, the tracker is a barebones top-level list.
- 2026-09-15: Base ROM's Unlocked / Challenge-Adjusted tags are irrelevant; it is just a non-vanilla Platinum. Content scope: species subset, all moves with assets, all abilities.
- 2026-09-15: Hardlove Gold is confirmed built on hg-engine. Phase 1 works from hg-engine's source first, donor ROM second.
- 2026-09-15: Phase 1 finding: no scoped element is achievable at the data layer. Approach A is off the table; B and C go to the breakdown.
- 2026-09-15: Approach C chosen. Fork of pret/pokeplatinum is the source of truth; Ian builds in WSL2.
- 2026-09-15: Battle AI is in scope; Platinum's AI is the baseline; Hardlove's AI is excluded.
- 2026-09-15: `docs/oxide/START-HERE-current-state.md` is now repo-tracked (was G:\-only). `tools/oxide/sync-docs.sh` mirrors `docs/oxide/*.md` to the project folder; run it whenever those files change. `~/roms/vanilla.nds` (byte-exact Rev 1, built once from `main`, checksums verified) is now pinned for `import_base_rom.py --vanilla` and `verify_narcs.py --ref`; don't rebuild it. The base ROM in the project folder must not be deleted, moved, or overwritten until the remaining carry-overs (encounters, text, items, trades, trainers, map headers, scripts/events) are done.

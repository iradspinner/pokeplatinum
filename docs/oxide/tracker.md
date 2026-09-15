# Platinum Oxide: Tracker

Top-level task list. Tick items as they finish; add detail only where it changes what happens next. Companion to `Platinum Oxide - Design Doc.md`.

**In progress:** Phase 3. Species/move/evo/learnset import done and committed locally on branch `oxide` (not yet pushed: GitHub access for this session pending). Waiting on Ian: GitHub repo added as a session source, WSL2 setup, answers to the inventory's five Qs

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
- [ ] Ian answers the inventory's five Qs (which code patches to keep; what the unknown ones are)
- [ ] Extend the decomp's trainer struct/loader for the expanded party format (needed before trainers can be carried over)
- [x] Conversion scripts for species, moves, evolutions, learnsets: `tools/oxide/import_base_rom.py` + `verify_narcs.py`; 415 species and 108 move files updated; rebuilt NARCs verified byte-identical to the base ROM (commit c69ef83 on branch `oxide`)
- [ ] Conversion scripts for encounters, heights, text, items, trades
- [ ] Carry over trainers (488 records) via the conversion scripts once the expanded format exists
- [ ] Carry over map-header weather edits (`include/data/map_headers.h`)
- [ ] Carry over scripts (91), events (158) and their text: disassemble, rewrite in the decomp's script macros, check each against its event file; ask Ian when intent is unclear
- [ ] Re-apply the small constant edits Ian wants (vitamin cap, options defaults, HM forget, shiny odds) as C changes
- [ ] Working `git pull && make rom` loop with Ian, verified end to end with one visible change

## Phase 4: Port, one element at a time

Order to be set after Phase 2. Each element gets its own checklist when it starts.

- [ ] Type expansion
- [ ] Ability expansion
- [ ] Move expansion (data, battle scripts, sprites, animations)
- [ ] Species-slot expansion (sparse: only the species on Ian's pick-list)
- [ ] Battle AI: Platinum baseline, teach it the new moves/abilities, apply the battle_edits AI fixes
- [ ] Other engine changes (Ian picks from the hg-engine menu)

## Phase 5: Verify

- [ ] Boots in emulator
- [ ] New game to first battle without crash
- [ ] A ported element visibly works in-game (for example: a Fairy-type move hits for the right effectiveness)

## Backlog / follow-ups

- Move `Platinum Oxide VSMaker2 Data\` out of the DSPRE contents folder (Ian's call; it is a stale duplicate)
- Open Hardlove's `a/0/2/8` to read the hidden-ability and base-exp tables directly (needed for the species port)
- Update the project doc `claude/engine-tooling-comparison.md`: plat-engine is a patch kit not a decomp build; pokeplatinum is matching and active

## Decisions made

- 2026-09-15: Base ROM is `Platinum Unlocked - Challenge - Adjusted v1.1.nds`. Donor is Hardlove Gold 0.6.9.
- 2026-09-15: Everything in the working folder is a copy; the Hardlove ROM and its DSPRE contents may be modified. Originals elsewhere are never touched.
- 2026-09-15: Deliverables live in the working folder as markdown; the design doc is instructions for Claude, the tracker is a barebones top-level list.
- 2026-09-15: Base ROM's Unlocked / Challenge-Adjusted tags are irrelevant; it is just a non-vanilla Platinum. Content scope: species subset, all moves with assets, all abilities.
- 2026-09-15: Hardlove Gold is confirmed built on hg-engine. Phase 1 works from hg-engine's source first, donor ROM second.
- 2026-09-15: Phase 1 finding: no scoped element is achievable at the data layer. Approach A is off the table; B and C go to the breakdown.
- 2026-09-15: Approach C chosen. Fork of pret/pokeplatinum is the source of truth; Ian builds in WSL2.
- 2026-09-15: Battle AI is in scope; Platinum's AI is the baseline; Hardlove's AI is excluded.

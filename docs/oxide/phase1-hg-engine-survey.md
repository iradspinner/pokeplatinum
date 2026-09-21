# Phase 1 survey: what hg-engine is, and what that means for porting it to Platinum

Written 2026-09-15 from the hg-engine repository (BluRosie/hg-engine, main), its wiki, plat-engine (lhearachel/plat-engine), pokeplatinum (pret), and the Hardlove Gold 0.6.9 DSPRE extraction in this folder. Everything below was read from those sources directly; nothing is from memory.

## 1. The single most important finding

hg-engine is not a rebuilt game. It is a **patch kit applied on top of a vanilla US HeartGold ROM**. The build does this, in order:

1. `ndstool` extracts the vanilla ROM (arm9, arm7, overlays, filesystem).
2. C and assembly sources are compiled with `arm-none-eabi-gcc` and linked at fixed RAM addresses (`rom.ld` lists ~500 vanilla HG function addresses the new code calls into; `src/*/linker.ld` sets where the new code lives).
3. `scripts/make.py` writes the compiled code into **new overlay files 129 through 151** and adds entries for them to the overlay table (`y9`). Overlay 129 is loaded once at boot by a 6-instruction patch in `Main()` and stays resident as an "arm9 expansion" (the Mikelan98/Nomura technique). The others are loaded on demand.
4. The same script applies four patch lists to the vanilla binaries: `hooks` (656 lines: overwrite 8 to 10 bytes at a vanilla address with a jump into new code), `armhooks` (6), `repoints` (133: rewrite a data pointer to point at a new table), `routinepointers` (10), `bytereplacement` (565: raw byte edits).
5. `armips` assembles `armips/global.s`, which includes ~3,200 lines of hand-written patches into arm9 and overlays (ability widening, move table repoints, pokedex save expansion, Fairy type plate handling, cries, level-up move format, overworld tables).
6. Around 40 NARCs are regenerated from source data and copied over the vanilla ones (species, moves, learnsets, evolutions, trainers, battle scripts, move animations, sprites, text, and so on).
7. `ndstool` repacks the ROM.

So "Hardlove's engine expansion elements" = hg-engine's patch kit + hg-engine's regenerated NARCs, applied to HeartGold. Hardlove itself is content on top of that.

**Why this matters for the port:** every one of those ~1,370 patch-list lines and ~3,200 armips lines names a specific address inside HeartGold's arm9 or overlays. None of those addresses exist in Platinum. The C code (about 49,000 lines across `src/` and `asm/`) is mostly game-logic and could in principle be recompiled for Platinum, but it calls ~500 vanilla HG functions by address (`rom.ld`), and each of those has to be re-found in Platinum's binary. The port is therefore not a data-copy job. It is a re-targeting job: same design, same C, new addresses, new hook points, plus whatever differs in Platinum's own battle code.

## 2. Confirmed: Hardlove is a stock hg-engine build

Checked against the Hardlove DSPRE extraction:

| Evidence | hg-engine source says | Hardlove has |
|---|---|---|
| Injected overlays | 129 (main), 130 (battle), 131 (field), 132 (pokedex), 133..151 (one per hooked vanilla function) | `ov129.bin` .. `ov151.bin` present; vanilla HG stops at 128 |
| Load addresses | ov129 at `0x023D8000`, ov130 at `0x023C4000`, ov131 at `0x023C8000`, ov132 at `0x021FBE60`, ov142 at `0x021E5900` | identical, per `overlays.yaml` |
| Species count | `MAX_SPECIES_INCLUDING_FORMS` = 1476, Egg = 494, Bad Egg = 495, spares to 543, Victini = 544 (dex 494 + 50), megas start at 1076 | 1476 personal files; project doc already recorded "+50 for Gen 5+" and "1076+ = megas/forms" |
| Move count | `NUM_OF_MOVES` reaches ~920 (Supercell Slam = 919, then custom slots) | 924 move files |
| Personal struct | `SpeciesData`: abilities are `u16[2]` at 0x16 and 0x1A; base exp is `baseExpRewardPadding` (moved out to a separate table); TM/HM bits are `tmHmLearnsetPadding` (moved to its own learnset file) | u16 abilities at 0x16/0x1A; base exp zeroed; TM compat zeroed |
| Base exp, hidden abilities, form tables, icon palettes | Stored in NARC `a/0/2/8` as "code addon" members 9_07 .. 9_13 | (not yet opened, but the struct evidence above is conclusive) |

Correction to earlier project notes: the zeroed base exp and TM compat fields in Hardlove's personal records are **hg-engine's layout**, not a Hardlove design choice. Base exp lives in `a/0/2/8` member 9_08; TM compatibility lives in the learnset data. The zeroed EV yields are a Hardlove choice (hg-engine keeps EVs in the struct).

Hardlove's snapshot of hg-engine is somewhat older than current main (main's species count now includes more forms), so when reading Hardlove data, prefer Hardlove's own tables over hg-engine head for exact indices.

## 3. What each scoped element actually is, in hg-engine terms

### Type expansion (Fairy)
- Not a table edit. hg-engine **replaces HG's damage calculation and type-effectiveness lookup with its own C code** (`src/battle/other_battle_calculators.c`, `battle_calc_damage.c`, `battle_pokemon.c` which defines `TypeEffectivenessTable[][3]`) and hooks the vanilla battle overlay (ov12 in HG) to call it.
- `armips/asm/fairy.s` handles the rest: Arceus plate lookup, type icon/palette repoints in arm9 and ov10/ov12, summary screen, dex icon.
- Config toggle `FAIRY_TYPE_IMPLEMENTED` in both `include/config.h` and `armips/include/config.s`.
- Platinum side: the vanilla type chart is `sTypeMatchupMultipliers[][3]` in `src/battle/battle_lib.c` (pokeplatinum), which lives in Platinum's battle overlay, **ov16**. plat-engine already hooks the effectiveness routine at `0x022558CC` in ov16.

### Ability expansion (IDs above 255, 512 slots)
- Two halves. (a) `armips/asm/abilities.s`: ~50 surgical byte edits across arm9 and ov12 that change every `ldrb`/`strb` of the ability field to `ldrh`/`strh`, move the ability field inside the battle-mon struct to an unused u16 slot (0x27 to 0x7A), and widen script-command casts. (b) The ability *effects* themselves are C in `src/battle/ability.c` (1,075 lines) plus many `src/individual/*.c` functions that fully replace vanilla functions (SwitchInAbilityCheck, MoveHitDefenderAbilityCheck, ServerFieldConditionCheck, and so on), each living in its own overlay 133..151.
- Ability names and descriptions come from the regenerated text NARC.
- Platinum side: the ability field is `u8` at 0x0D of the boxed-mon substruct and `u8` in `battle_mon.h` (pokeplatinum). Every (a)-style edit has to be re-derived for Platinum's arm9 and ov16. plat-engine has **not** done this part.

### Move expansion (924 records)
- Move data: `data/Moves.c` compiled by `movedatagen` into NARC `a/0/1/1`; `armips/asm/moves.s` repoints every vanilla reference to the move table and its size.
- Per-move content, all regenerated: battle script (`data/battle_scripts/moves/`, 923 files, into `a/0/0/0`), effect scripts (408, into `a/0/3/0`), sub-scripts (521, into `a/0/0/1`), move animation (`armips/move/move_anim/`, 923 files, into `a/0/1/0`), sub-animations (57, into `a/0/6/1`), particle graphics (`a/0/2/9`), move names/descriptions (text NARC).
- The battle script *interpreter* is also extended: `src/battle/battle_script_commands.c` adds new script commands hooked into ov12.
- Platinum side (from plat-engine's `narcs.mk`): move table is `poketool/waza/pl_waza_tbl.narc`; scripts are `battle/skill/waza_seq.narc`, `be_seq.narc`, `sub_seq.narc`; animations are under `wazaeffect/`. The script bytecode format is shared across Gen 4 with small differences, which is why plat-engine could carry 501 move scripts and 277 effect scripts over from hg-engine. Animation scripts and particle assets are the least examined part and may differ most.

### Species-slot expansion (to 1476)
- `data/Species.c` compiled by `speciesdatagen` into `a/0/0/2` (personal), plus per-species learnsets (`data/learnsets/learnsets.json`), evolutions (`a/0/3/4`), sprites (`a/0/0/4` pokegra, plus icons, footprints, height, sprite offsets), dex data (`a/1/3/3`, `a/2/1/4`, `a/1/3/8`), cries (SDAT pseudobanks from `CRY_PSEUDOBANK_START` = 778), text (names, dex entries, classifications).
- `armips/asm/pokedex.s` expands the save file's dex flags (`ALLOW_SAVE_CHANGES`; breaks PKHeX compatibility), `armips/asm/cries.s` remaps species to sound files, `armips/asm/overworlds.s` handles OW sprites.
- Forms: `a/0/2/8` members 9_11 (form data), 9_12 (form to species), 9_13 (reversion); encounter/trainer records encode `(form << 11) | species`.
- Platinum side: `poketool/personal/pl_personal.narc`, `evo.narc`, `wotbl.narc` (learnsets), `pokegra/pl_pokegra.narc`, `icongra/pl_poke_icon.narc`, `pokefoot`, `height.narc`, `poke_edit/pl_poke_data.narc` (sprite offsets), `resource/eng/zukan/zukan.narc` (dex), `msgdata/pl_msg.narc` (text). pokeplatinum has 59 code sites that reference `MAX_SPECIES`/`NATIONAL_DEX_COUNT`; each is a hard cap that has to be raised. `pms.narc` (baby mons) also exists.

### "Other engine changes" (the full hg-engine menu, from README/wiki/CONFIG.md)
Every item marked (cfg) is a compile-time toggle in hg-engine; the rest are always on.
- Item expansion (Gen 8/9 items, bag pocket expansion via save changes)
- Mega Evolution + Primal Reversion (cfg)
- Hidden Abilities with a script-flag trigger (cfg)
- Level-influenced experience formula, Gen 5/7/8 style (cfg), plus the base-exp table relocation
- Dynamic speed, accurate turn order and end-of-turn resolution (baked into the reimplemented battle engine)
- New weathers
- New evolution methods through Gen 8
- Customizable trainers (IVs, EVs, natures, shininess, explicit stats) and trainer-AI updates
- 30 PC boxes (cfg)
- 60 fps in battle or everywhere (cfg)
- Always-set battle mode (cfg), always-national-dex (cfg)
- Transparent textboxes (cfg), fast text (cfg)
- Reusable TMs, deletable HMs (cfg)
- Wild double battles (cfg), capture experience (cfg), critical capture (cfg)
- EV/IV viewer on summary screen (cfg)
- Level caps via script variable (cfg)
- Reusable repels (cfg), vitamin EV caps to 252 (cfg), no items in trainer battles (cfg), static HP bar (cfg), restore single-use items after battle (cfg), friendship evolution threshold (cfg)
- Anti-piracy patch for flashcarts (cfg), BDHCam (cfg)
- Level-up learnset format change to (u16 level, u16 move) with a configurable max
- Overworld follower/sprite system changes
Which of these Hardlove actually has switched on is not visible from the extraction alone (the config is compile-time); it would take checking specific byte patterns or just asking the Hardlove author's notes. Ian can pick from this list without that.

## 4. plat-engine: what it is and where it stopped

- **Same architecture as hg-engine, deliberately.** Credits hg-engine and the same Mikelan98/Nomura arm9-expansion technique. Loads overlay 122 at boot from a patch at `0x02000CB4` in Platinum's `Main()`, links new code at `0x023C9000` (main) and `0x023D0000` (battle, field). Uses the same `hooks` / `repoints` / `routinepointers` / `bytereplacement` file scheme (`buildsys/`).
- **Requires vanilla Platinum US Rev 1** by SHA-256 in its instructions. The Makefile itself does not appear to enforce it, but every address in it assumes vanilla code layout. The Platinum base in this folder is Rev 1 and its arm9/overlays are probably still vanilla in layout (DSPRE edits data NARCs, not code), but this has to be verified before any address from plat-engine is trusted.
- **Dormant.** Single visible commit dated 2023-08-19; nothing since.
- **What it has:** the loader; `rom.ld` with 107 Platinum function addresses (malloc, NARC readers, overlay loader, a set of battle functions); 16 hooks, all into arm9 or ov16 (damage calc, crit, type effectiveness, several ability checks, stat-boost script command, switch-in effects); 8 byte replacements (crit table); Fairy plate patch translated to Platinum (`0x02077988`); ~5,600 lines of C, mostly `src/battle/calc.c` (2,718) and `server.c` (1,706), i.e. a partial port of hg-engine's damage calculator and ability-check functions; species data as 700 JSON files (through Gen 6, same +50 numbering as hg-engine: Volcanion = 0x303 = 721 + 50); 501 move scripts, 277 effect scripts, 304 sub-scripts carried over; Platinum NARC path map in `narcs.mk`; Fairy-type graphics from Renegade Platinum.
- **What it does not have:** the u16 ability widening (`abilities.s` equivalent), the move-table repoints (`moves.s` equivalent), pokedex/save expansion, cries, learnset format change, overworlds, item expansion, mega evolution runtime (config flag exists, code does not), move animations, sprites beyond icons, trainer expansion. Its `repoints` and `routinepointers` files are literally empty with a "will be filled in" comment.
- Rough estimate by counting: plat-engine has re-targeted on the order of 10% of hg-engine's hook surface and 0% of its armips patch surface.

## 5. pokeplatinum: better than the earlier project note said

- Builds **matching** ROMs for both US Rev 0 and Rev 1 (SHA-1s in its README). Last commit 2026-09-12, so it is actively maintained.
- This is the address oracle for the port. Every function hg-engine calls by HG address, and every hook site, has a named C function in pokeplatinum whose Platinum address can be read from the build's symbol map. Finding "where does Platinum store the ability byte" is a `grep`, not a disassembly session.
- The type chart is `sTypeMatchupMultipliers` in `src/battle/battle_lib.c`; the mon struct's ability is `u8` at 0x0D of the relevant substruct (`include/struct_defs/pokemon.h`); species caps appear at 59 sites.

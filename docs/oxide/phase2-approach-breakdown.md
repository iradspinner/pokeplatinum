# Phase 2: approach breakdown

Written 2026-09-15. Companion to `phase1-hg-engine-survey.md`. Approach A (data-layer only) is discarded per Phase 1 and Ian's instruction; this compares B and C.

## Bottom line

**Approach C is feasible, and it is the better choice.** The concern that Platinum "is not fully decompiled" was true in 2023 and is not true now: pokeplatinum is 100% C (1,013 source files, ~720,000 lines, zero remaining assembly), it builds a byte-identical US Rev 1 ROM, and I verified that today by building it in my workspace. Clean build: about 8 minutes. Rebuild after editing one battle-engine file: 29 seconds. The one caveat that matters is logistics (where the source lives and who runs the build), covered in section 5.

## 1. What was verified today

| Check | Result |
|---|---|
| Decompilation coverage | `asm/` contains only macros. Every function is C. What remains unfinished is *naming*: ~1,600 files still reference auto-named symbols like `sub_0203A418`, which is a documentation gap, not a code gap. |
| Matching build | `make rom` produced `pokeplatinum.us.nds`, 134,217,728 bytes, SHA-1 `0862ec35b24de5c7e2dcb88c9eea0873110d755c`, identical to the retail Rev 1 dump. |
| Toolchain | Needs the original Metrowerks ARM compiler. The project ships it through `metroskrew` (mid-kid), a Linux/Windows wrapper fetched from GitHub releases; it ran in my workspace after installing 32-bit libc. No Wine needed on Linux or WSL. |
| Build time | ~8 min clean on 2 cores; 29 s incremental. |
| Maintenance | Last upstream commit 2026-09-12. Active. |
| Precedent | Three public hacks build on the decomp: Coarse Platinum (content and balance changes, active today), Tempered Platinum's `plat-hack-decomp` (all battle mechanics updated to Gen IX behaviour, new weather types, author describes himself as not a C programmer, active today), and pokeaotea (undocumented). None of them has done a dex, type or ability *expansion*; that part would be new ground on the decomp side. |

## 2. What each approach actually is

**B. Re-target the hg-engine patch kit onto Platinum.** Take plat-engine's skeleton (loader, 107 known Platinum addresses, 16 hooks, partial damage calculator) and finish what its author stopped in 2023: port the rest of hg-engine's ~49,000 lines of C, then re-derive every one of hg-engine's ~1,370 hook/repoint/byte-patch lines and ~3,200 lines of armips patches against Platinum's binaries. The output is a build system that takes Ian's base ROM in and emits a patched ROM, like hg-engine does with vanilla HeartGold.

**C. Build from the decomp.** Fork pokeplatinum. Make the changes as ordinary edits to C and to the data files under `res/` (species JSON, move data, learnsets, scripts, map headers, text). Use hg-engine's source as the reference implementation of *what* each feature does, and reimplement it in pokeplatinum's own functions and structs. The output is a ROM built from source.

## 3. Comparison on the dimensions that matter

**Where the work goes.** Under B, roughly half the effort is not game logic at all; it is locating addresses. Every `ldrb` of the ability byte, every `cmp #493` species cap, every table pointer has to be found in Platinum's arm9 and ov16 by disassembly or by cross-referencing the decomp, then patched by hand at a fixed offset. hg-engine's `abilities.s` alone is ~50 such edits. Under C, the same change is "find the field in the struct definition and widen it," and the compiler updates every use. The 59 code sites that reference `MAX_SPECIES` are a `grep`, and raising the constant fixes all of them at once. The decomp is not just a map for B; it is the thing B is trying to reconstruct by hand.

**Fragility.** B's patches are tied to exact byte offsets. Any other code edit that shifts bytes (including some DSPRE operations) can silently break a hook. C has no offsets; the linker places everything.

**Reuse of hg-engine.** Neither approach drops hg-engine's C in unchanged, because it is written against HeartGold's structs and function names. Under B it still has to be re-linked against Platinum addresses and its hooks re-derived; under C it is rewritten into pokeplatinum's named functions. C's rewriting is more typing but far less guessing, and the decomp's battle code is already organised the way hg-engine's replacement code is (a `battle_lib.c` with the type chart, a script interpreter, per-ability checks).

**The reference point for "what is vanilla".** This matters for Ian's base ROM. B starts from the ROM as it exists, with DSPRE's edits to `arm9.bin` and `ov016.bin` of unknown content; every address has to be checked against those edits first. C starts from source that is known to match retail, and the base ROM's data edits are re-applied as changes to source files (section 5).

**Overworld and event editing.** Under C, the work Ian has struggled with in DSPRE becomes editing named assembly scripts, JSON event files, JSON trades and a C map-header table (see the Route 201 script and the Route 212 South header in the Phase 1 discussion). Under B, it stays in DSPRE or in raw NARC bytes.

**Tooling for Ian.** DSPRE reads the *output* of either approach (both produce a normal `.nds`), so DSPRE remains usable for inspection. For editing, C's source tree is the editor; B keeps DSPRE plus the patch kit's own text formats (hg-engine's `Species.c`, `Moves.c`, trainer and encounter formats).

**Precedent and help.** B: hg-engine has a large community, but for HeartGold; plat-engine is one dormant repository. C: the pret Discord `#pokeplatinum` channel, the VoidMatrix `#decomp` channel, and at least two active decomp-based Platinum hacks, one of which already reworked the whole battle engine's mechanics.

**Risk of getting stuck.** B's failure mode is a crash with no symbols, caused by a mis-derived address, debugged by disassembly. C's failure mode is a compile error or a C bug with a debugger available (`INSTALL.md` section 4 covers debugger support). C's risk is concentrated in the expansion work no one has published yet (widening the species and ability fields through the save structure, the Pokedex, the PC, and the battle-mon struct). hg-engine shows exactly which places those are, which is the main value it still provides under C.

**Ceiling.** B's ceiling is hg-engine's feature set as of Hardlove's snapshot. C's ceiling is anything the game can do, including things hg-engine had to work around (hg-engine's RAM-expansion trick exists because it cannot relink the game; C can).

## 4. What C costs that B does not

- **Re-expressing the base ROM's edits.** DSPRE wrote into a dozen NARCs of the base on 2026-08-30 (personal data, evolutions, learnsets, move table, trainers, icons, battle backgrounds, heights, sprite offsets, trainer text) and into `arm9.bin`/`ov016.bin` on 2026-08-25. Under C those edits do not carry over automatically; each one has to be re-made in `res/` (or dumped from the NARC and converted, which is scriptable for the table-shaped ones). Ian needs to say which of them matter. If most of that work was exploratory, the cost is near zero.
- **A local build environment for Ian, or a patch-delivery step.** See section 5.
- **Learning curve.** The source tree is large. In practice Ian does not need to read it; the design doc and tracker say where things are, and edits to data files (JSON, scripts) need no C.

## 6. Recommended plan if C is approved

Phase 3 (tooling) becomes:
1. Ian forks pokeplatinum; I clone the fork and confirm a matching build from it.
2. Inventory the base ROM's DSPRE edits: dump each modified NARC, diff against vanilla, and list what Ian wants kept. Convert the keepers into `res/` edits (scripted for personal/evo/learnset/move tables).
3. Establish the build-and-test loop: I edit, push, Ian pulls and builds (or I deliver a patch); Ian plays in an emulator and reports.

Phase 4 (port) order, chosen so each step is testable on its own and the risky structural changes come first while the tree is still close to vanilla:
1. Fairy type: add to the type enum, the chart in `battle_lib.c`, type names/icons, Arceus plate handling. Test: a Fairy move hits Dragon for 2x.
2. Ability field widening to u16 and table expansion to 512: boxed-mon struct, battle-mon struct, summary screen, script commands, save. Test: give a mon ability ID 300 and see it named and working. This is the step hg-engine's `abilities.s` documents completely.
3. Species-slot expansion: raise `MAX_SPECIES`, expand personal/evo/learnset/sprite/dex/text tables, save-file dex flags, PC. Bring in Ian's picked species from Hardlove's tables (scripted conversion from the 44-byte records, which are hg-engine's layout and therefore fully understood).
4. Move expansion: move table, battle scripts, effect handlers, animations, text. Bring in Hardlove's moves; the script bytecode is shared across Gen 4 so much of hg-engine's `data/battle_scripts` converts mechanically.
5. Ability effects: reimplement the new abilities' behaviours in the decomp's battle code, using hg-engine's `ability.c` and `individual/*.c` as the spec.
6. Then the "other engine changes" Ian picks from the hg-engine menu, one at a time.

Sources consulted today, beyond the repositories themselves: [pret/pokeplatinum](https://github.com/pret/pokeplatinum), [c-crescent/Pokemon_Coarse_Platinum](https://github.com/c-crescent/Pokemon_Coarse_Platinum), [matt-newhall/plat-hack-decomp](https://github.com/matt-newhall/plat-hack-decomp), [JBerben/pokeaotea](https://github.com/JBerben/pokeaotea), [mid-kid/metroskrew](https://github.com/mid-kid/metroskrew).

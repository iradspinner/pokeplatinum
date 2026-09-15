# Phase 3: what the base ROM changed from vanilla

Written 2026-09-15 by diffing `Platinum Unlocked - Challenge - Adjusted v1.1.nds` against the byte-exact Rev 1 ROM built from pokeplatinum. Every number below comes from that comparison. The raw diff data is kept in `notes\diff\` (`file_diffs.json`, `member_diffs.json`, `synth_overlay_9.bin`).

Ian's guidance: keep overworld events, trainer edits, and Pokemon stat and move edits where possible; flag anything else. The "keep" set turns out to be larger than "about 80 fights", and there is also code in the base that Ian may or may not remember adding. Questions for Ian are marked **Q**.

## 1. Data edits (these carry over to the decomp as data-file changes)

| Table | Changed | What changed | Carry-over route |
|---|---|---|---|
| Species (`pl_personal.narc`) | 409 of 508 species | Abilities reassigned on 173 (slot 1) and 147 (slot 2); hatch cycles on 228; base stats on 43 to 102 species per stat; type on 5 | Scripted: dump the 44-byte records into pokeplatinum's `res/pokemon/<species>/data.json` |
| Moves (`pl_waza_tbl.narc`) | 108 of 471 moves | Accuracy 46, PP 37, power 24, priority 7, plus a handful of effect/target/flag tweaks | Scripted, into `res/moves/` |
| Evolutions (`evo.narc`) | 24 species | Evolution method or target changes | Scripted |
| Level-up learnsets (`wotbl.narc`) | 3 species (249, 301, 405) | Small | Scripted |
| Trainers (`trdata.narc` + `trpoke.narc`) | 488 of 928 trainer records, 561 party records | Byte 12 (AI flags) changed on 350 trainers; byte 0 (party data format: custom moves/items) on 344; class on 50. Party records use an **expanded format** (16/32/48/108-byte entries where vanilla has 8/16/24/32) | Scripted, but see section 2: the expanded trainer format depends on a code patch |
| Wild encounters (`pl_enc_data.narc`) | 125 of 183 tables | Encounter rewrites | Scripted, into `res/field/encounters/` |
| Field scripts (`scr_seq.narc`) | 91 of 1,124 script files | Mostly grew by 150 to 500 bytes each: new script content | Semi-manual: disassemble each changed script, express as edits to `res/field/scripts/scripts_<map>.s`. This is the one Ian most wants kept and the most labour-intensive |
| Overworld events (`zone_event.narc`) | 158 of 534 map event files | Growth in 32-byte steps: object events (NPCs) added | Semi-manual, into `res/field/events/events_<map>.json`; pairs with the scripts above |
| Text (`pl_msg.narc`) | 78 of 724 text banks | New or edited lines (NPC dialogue for the scripts above, and likely names/descriptions) | Scripted diff per bank, into `res/text/` |
| In-game trades (`fld_trade.narc`) | 2 of 4 trades | | Manual, into `res/npc_trades/` |
| Items (`pl_item_data.narc`) | 6 items (45 to 49, 52) | | Manual |
| Map headers (in `arm9`, `sMapHeaders`) | ~100 single-byte edits | Byte 20 of the 24-byte header = **weather**. Many maps changed 0x0E to 0x1B, some to 0x00/0x1D/0x1E, a few other fields | Manual, into `include/data/map_headers.h` (named fields, easy) |
| Pokedex encounter areas (`zukan_enc_platinum.narc`) | 276 entries | Follows the encounter edits | Regenerable from encounters, probably |
| Sprite heights (`height.narc`) | 298 entries | Sprite Y-offset tweaks | Scripted |
| Trainer BGM table (`sTrainerEncounterBGMs`) | 1 entry | | Manual |

Things that changed but look like tool side effects rather than edits (**Q** to confirm):
- `pl_pokegra.narc`: 2,788 of 2,964 sprite files differ, but only ~5 bytes each, all in the file header. That is a DSPRE re-save, not a sprite change. `pl_otherpoke.narc` (26 files), `pl_batt_bg` (78), `pl_batt_obj` (50), `batt_obj` (1), `box.narc` (8), `pl_plist_gra` (3), `titledemo` (2), `mmodel.narc` (6 building models), `trfgra` (8 trainer sprites), `item_icon` (1), `waza_particle` (1) also differ. Some of these may be real (a custom title screen? new trainer sprites for the changed classes? new building models?).

## 2. Code edits (these do NOT carry over automatically; each becomes a C change or is dropped)

The base's `arm9` differs from vanilla at 38 places and eleven overlays differ. Mapped to the decomp's function names:

**A. A synthetic overlay and its loader.** `data/weather_sys.narc` member 9 is a 90 KB block that vanilla does not have; only 578 bytes of it are used. `NitroMain+0x2D` is patched to load it at boot (DSPRE's "ARM9 expansion" patch; loader code sits over unused assertion strings at arm9 `0x0F93D0`, `0x100E20`, `0x101574`). The block contains four labelled routines: `EV+IV_Viewer`, `no_items` (no items in trainer battles), `frame_unlock_settings` (frame-rate unlock), `chain_candy` (Rare Candy chaining). Hooks that jump into it: `HandleInput_Main+0x34` and `HandleInput_SelectMove+0x8E` (summary screen, for the viewer), `PartyMenuCB_LevelUp+0x276` (candy), `SetMonDataFromMon+0x1B2`, four hooks in ov16 (battle: `+0x42`, `+0x154`, `+0x26E8`, `+0x2E6E`, `+0xDEC8`, `+0xEDE0`), one each in ov12, ov13, ov84, ov86, ov87, ov119, and two in ov5.
**Q:** These look like the ds-pokemon-hacking "code injection" patches applied through DSPRE. Which of the four do you want in the port? Under approach C each is a small C edit (hg-engine has all four as config toggles too, so the design is known). The synthetic-overlay mechanism itself is dropped; the decomp has no need for it.

**B. Expanded trainer party format.** `TrainerData_BuildParty` (1,026 bytes) is fully rewritten and `Trainer_Encounter+0x6E` is edited. This is the community "expanded trainer data" patch that lets trainer Pokemon carry custom IVs, EVs, natures, abilities and so on; it is why `trpoke.narc` entries are 16/32/48/108 bytes. **Q:** Confirm which patch this is (the DSPRE option name or the guide you followed), so the same fields can be read back correctly. Under C, pokeplatinum's trainer format is the vanilla one; the port will need the decomp's trainer struct extended to hold those fields (hg-engine's `trainer_data.h` is the model), and the 561 party records converted. This is a real chunk of Phase 3.

**C. Palette-loading hooks.** `PaletteData_LoadBufferFromFile+0x48`, `LoadPaletteWithSrcOffset+0x1E`, `BufferPokemonSpritePlttData+0x50`, `SpriteSystem_LoadPlttResObj+0x3C`, `CharacterSprite_LoadPalette+0x30`, `Pokedex_GetDisplayForm+0x2`, `Pokemon_GetValue+0x2`, `BoxPokemon_GetValue+0x2` all branch into the expansion. Together with `Pokemon_IsPersonalityShiny+0x18` changing `8` to `0xFF`, this reads as a shiny-related patch (raised shiny odds plus custom shiny palettes or per-form palettes). **Q:** What is it?

**D. Script commands over Battle Arcade code.** arm9 `0x05003C` to `0x0505BC` (~1.4 KB), which in vanilla is `ScrCmd_CallBattleArcadeLobbyFunction`, `SelectBattleArcadeChallengers` and neighbours, is overwritten with new code and a table, and `ScrCmd_Dummy088` is replaced with a 60-byte routine. Something added custom script commands by sacrificing Battle Arcade functions. **Q:** Do you know what this is? If any of the 91 edited scripts use these custom commands, the port has to reimplement them; if not, it can be dropped. (Battle Arcade would be broken in the base ROM as a result; "Unlocked" may have been intended to bypass it.)

**E. Small constant edits, all understood:**
- `Pokemon_CheckItemEffects+0x298` and `CalculateEVUpdate+0x38`: vitamin EV cap 100 to 252 (hg-engine's `UPDATE_VITAMIN_EV_CAPS`).
- `Options_Init+0x12/+0x24`: default options changed (text speed / battle style).
- `ApplyButtonModeToInput`: 2-byte change (button mode default).
- `TeachMove+0x5B`: a conditional branch made unconditional (probably "HMs can be forgotten").
- `UseVsSeekerFromMenu+0xC` (two places): a constant changed.
- ov73, ov9: one small edit each. ov14 (trainer AI): ten single-byte edits, consistent with the AI bug fixes in the ds-pokemon-hacking battle_edits guide (items 35 to 43). ov16 `+0x1309C..+0x130BE`: a 4-entry table (10, 30, 50, 70) set to 255, and `+0xEA3C`, `+0x10D58`, `+0x2D046` small edits.
**Q:** For the ov14 AI fixes, which ones did you apply? Under C they are one-line C fixes in `src/battle/trainer_ai/`, and the ones you did not apply can be applied too.

## 3. What this means for Phase 3

The data side is a scripting job I can do without help: dump each changed NARC member, convert to the decomp's `res/` format, diff against vanilla, keep the deltas. Scripts and events are the slow part because each of the 91 scripts has to be disassembled and rewritten in the decomp's macro language, then checked against the event file and text bank it references. Ian does not need to do that work, but he will be asked what specific scripts were *meant* to do when the bytecode is ambiguous.

The code side needs Ian's answers to the five **Q**s above before anything is ported, because some of those patches may be things he no longer wants, and each one that stays is a C change rather than a byte patch.

Nothing here changes the approach decision. It does make the expanded trainer format (B) a Phase 3 item rather than a "later" one, because the 488 edited trainers depend on it.

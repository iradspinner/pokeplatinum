# Phase 3: Ian's answers to the five Qs, and the trainer format resolved

Written 2026-09-15. Ian answered the five questions in `phase3-base-rom-inventory.md`
section 2. Question B (the trainer patch) he could not answer, so it was determined
from the ROM instead; that investigation is section 2 below and it **corrects an
error in the inventory doc**.

Claude Code should fold this into `docs/oxide/design-doc.md` (scope table and
findings log) and `docs/oxide/tracker.md`, then delete nothing: keep this file as
the record of how the trainer format was worked out.

## 1. The answers

**A. Synthetic overlay routines: port all four.** EV/IV viewer on the summary
screen, no items in trainer battles, frame-rate unlock, and Rare Candy chaining.
All four exist as compile-time toggles in hg-engine
(`IMPLEMENT_NEW_EV_IV_VIEWER`, `DISABLE_ITEMS_IN_TRAINER_BATTLE`,
`BATTLES_UNCAPPED_FRAME_RATE`, and candy behaviour under the level-cap options),
so hg-engine's C is the reference for each. The synthetic-overlay mechanism
itself is dropped; in the decomp these are ordinary code changes.

**B. Expanded trainer format: there is no expanded format.** See section 2.

**C. Shiny and palette patch: two separate things.**
- Shiny odds raised. Confirmed from the diff: `Pokemon_IsPersonalityShiny+0x18`
  changes the threshold from `8` to `0xFF`. Vanilla is
  `(pidHigh ^ pidLow ^ otidHigh ^ otidLow) < 8`, i.e. 8/65536 = 1/8192; with 255
  it is 255/65536, about **1/257**. This is a one-constant change in C and should
  be ported.
- A hue shift driven by IVs or nature. **Not yet investigated.** The eight palette
  hooks in the inventory (`PaletteData_LoadBufferFromFile`,
  `LoadPaletteWithSrcOffset`, `BufferPokemonSpritePlttData`,
  `SpriteSystem_LoadPlttResObj`, `CharacterSprite_LoadPalette`,
  `Pokedex_GetDisplayForm`, `Pokemon_GetValue`, `BoxPokemon_GetValue`) are
  presumably this. Ian said to drop it if it proves opaque. Recommendation: treat
  it as a separate, low-priority investigation after the scoped Phase 4 work,
  not part of the base-ROM carry-over. Porting it means understanding a
  procedural palette generator, which is a real project on its own, and nothing
  else depends on it.

**D. Custom script commands over Battle Arcade: decide from evidence, do not port
blind.** Ian's answer was "port it to be safe, I have no interest in the Battle
Arcade." The thing worth preserving is not the commands themselves but any of his
91 edited field scripts that *call* them. So: when the script carry-over happens
(already a Phase 3 item), check which command IDs those scripts use. If none of
them reach into the overwritten range, there is nothing to port and the item
closes. If some do, reimplement just those commands as new script commands in the
decomp, which has room for them without sacrificing anything. Porting ~1.4 KB of
unidentified code that may be called by nothing would be effort spent for no
behaviour, with a real chance of getting it subtly wrong.

**E. Battle edits: apply all of them, including the one he skipped.** Ian applied
most of this list and thinks he skipped one but cannot recall which:

- Fire Fang vs Wonder Guard
- Rage Glitch
- Trainer AI Basic Flag Water Immunity Check vs Dry Skin
- Trainer AI Basic Flag Sunny Day Check
- Trainer AI Expert Flag Foresight and Odor Sleuth Ghost Type Check
- Trainer AI Expert Flag Facade Status Check
- Trainer AI Expert Flag Leaf Guard Sunny Day Logic
- Trainer AI Expert Flag Water Spout and Eruption HP Check
- Trainer AI Expert Flag Charge-Turn Move Scoring Fix
- Trainer AI Expert Flag Thunder Scoring Fix
- Trainer AI Tag Strategy Flag Discharge Scoring in Double Battle Fix

Which one he skipped stops mattering under approach C: every item on that list is
a small logic fix in `src/battle/` or `src/battle/trainer_ai/`, so all eleven get
applied from the guide's descriptions rather than recovered from the old ROM's
bytes. The ten single-byte edits found in overlay 14 corroborate that the AI ones
were applied; they are not needed as a source. Source:
https://ds-pokemon-hacking.github.io/docs/generation-iv/guides/battle_edits/

## 2. The trainer format, determined from the ROM

**Correction.** `phase3-base-rom-inventory.md` section 2B claimed the base ROM
uses an expanded trainer party format, inferred from party-record sizes of
16/32/48/108 bytes where vanilla showed 8/16/24/32. That inference was wrong.

The party data is **vanilla format**. Evidence:

- Vanilla per-mon sizes from `include/struct_defs/trainer_data.h` are 8 bytes
  (base), 16 (with moves), 10 (with item), 18 (with moves and item). Checking
  every trainer's record length against `partySize * perMonSize` for its declared
  `monDataType`: **926 of 928 match exactly** in the base ROM. The two that do not
  are off by exactly 2 bytes (12 vs 10, 20 vs 18), which is NARC alignment
  padding; vanilla itself has 43 such cases.
- The 108-byte records are simply `6 mons * 18 bytes`: full six-Pokemon parties
  with custom moves and held items. The size difference from vanilla is Ian giving
  many more trainers full custom parties, not a wider struct.
- Decoding all 2,059 Pokemon across all 928 trainers with the vanilla layout
  yields zero out-of-range species and zero out-of-range moves. Levels, items and
  form bits all read sanely. Example, trainer 5 (class 86, AI mask 0x2F): six
  level-100 Pokemon, Houndoom with Fire Blast / Dark Pulse / Sludge Bomb /
  Will-O-Wisp, a form-1 Rotom, Darkrai with Dark Void, all holding items.

**The one non-vanilla thing** is the high byte of the `ivScale` u16. Vanilla leaves
it zero (1,877 of 1,878 mons; one stray 9). The base ROM uses it on 207 mons, with
values 0x01, 0x02, 0x10, 0x11, 0x12, 0x20, 0x21, 0x22: two independent nibbles,
each taking 0, 1 or 2.

Disassembling the rewritten `TrainerData_BuildParty` (arm9 `0x020793B8`) shows the
low byte used for IVs exactly as vanilla does
(`ivStat = ivScaleLow * 31 / 255`, at `0x020794AC`), and the **high byte passed in
r2 to a new helper at `0x020795A0`** along with the species, the form, and a
pointer to the personality value. That helper is 0x38 bytes and reads:

```
r4 = highByte & 0x0F        ; low nibble
r5 = highByte >> 4          ; high nibble
if (highByte == 0) return               ; vanilla behaviour
if (r4 != 0) *personality -= 2          ; gender nudge
if (r5 == 1) *personality &= ~1         ; force ability slot 1
if (r5 == 2) *personality |=  1         ; force ability slot 2
```

In Gen 4 the ability slot is chosen by bit 0 of the personality value, so the high
nibble is unambiguously **ability slot** (1 = first ability, 2 = second). The low
nibble adjusts the personality against the gender threshold, so it is **gender**
(1 and 2 being the two forced values). The 3-state range in the data matches.

Two honest caveats. The gender path is sloppily compiled: after `cmp r4, #0` the
code does `movs r2, #18` and then branches on *those* flags, which makes the
`+= 2` arm at `0x020795B8` unreachable, so every non-zero low nibble takes the
`-= 2` arm. Either the patch has a bug or it was hand-written and only ever
exercised one direction. Second, the ±2 nudge is a crude way to cross a gender
threshold and will not reliably force gender for every species' ratio. So when
this is reimplemented in the decomp, write it correctly (pick a personality that
actually satisfies the requested gender for that species' ratio) rather than
copying the ±2 behaviour, and expect a small number of Ian's trainers to end up
with a different gender than the old ROM produced. Worth telling him if any of
those 207 mons are ones he cares about.

### What this means for the carry-over

The blocking item "extend the decomp's trainer struct/loader for the expanded
party format" is **not needed** and should be replaced with a much smaller one.
`res/trainers/data/*.json` in the decomp already carries everything the vanilla
format holds, per trainer, in one file: name, class, items, `ai_flags`,
`double_battle`, and a party of `species` / `form` / `level` / `item` / `moves` /
`iv_scale` / `ball_seal`, plus the trainer's battle messages (which covers the
`trtbl`/`trtblofs` differences too). So the work is:

1. Add two optional per-mon fields to the trainer JSON and to `trainerproc`
   (`tools/dataproc/src/trainerproc.c`), for example `"ability": 0|1|2` and
   `"gender": null|"male"|"female"`.
2. Make `TrainerData_BuildParty` in `src/trainer_data.c` honour them, written
   correctly rather than as a ±2 nudge.
3. Extend `tools/oxide/import_base_rom.py` with a trainer importer that writes the
   488 changed trainers into those JSONs, decoding `ivScale` as
   `{low byte -> iv_scale, high nibble -> ability, low nibble -> gender}`.
4. Verify with `tools/oxide/verify_narcs.py` on `poketool/trainer/trdata.narc` and
   `trpoke.narc`. Expect `trpoke` to match byte-for-byte apart from alignment
   padding, once the ability and gender nibbles are re-encoded.

Step 1 and 2 are small. Step 3 follows the pattern already proven for species and
moves.

# Phase 3: Ian's answers to the five Qs, and the trainer format resolved

Written 2026-09-15. Ian answered the five questions in `phase3-base-rom-inventory.md`
section 2. Question B (the trainer patch) he could not answer, so it was determined
from the ROM instead; that investigation is section 2 below and it **corrects an
error in the inventory doc**.

## 1. The answers

Cut to this pointer in the docs pass of 2026-09-27, every answer having been acted on. The one-line summary and each outcome are under Phase 3 in `tracker-archive.md` (the four synthetic-overlay routines, the shiny threshold and the other constant edits); the palette hue shift and the Battle Arcade commands are settled in the inventory's corrections; and the eleven battle_edits fixes are in `docs/oxide/battle-ai/README.md`. The full answers are this file in git history before that pass.

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
threshold and will not reliably force gender for every species' ratio. Oxide's
`TrainerData_BuildParty` does it correctly instead, picking a personality that
satisfies the requested gender for the species' ratio (commit 5b8958368), so a
few of those 207 Pokemon may have a different gender than the old ROM gave them.

### What this meant for the carry-over

Done (tracker archive, Phase 3): all 928 trainers came over with 0 field
mismatches. The decomp did not re-encode the nibbles into `ivScale` as first
planned; each party entry gained its own `ability` and `gender` bytes
(`include/struct_defs/trainer_data.h`), so the record is 2 bytes wider and
`trpoke` is checked field by field rather than byte for byte. The trainer JSON's
optional `"ability"` (0 to 3, 3 being the hidden ability since 2026-09-27) and
`"gender"` keys are documented in `tools/dataproc/src/trainerproc.c`, and
`ivScale`'s high byte now carries an optional nature instead.

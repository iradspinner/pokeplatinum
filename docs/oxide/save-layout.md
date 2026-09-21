# Save layout: what Platinum Oxide moved, and why

Phase 4 breaks save compatibility with vanilla Platinum. Ian confirmed that is
acceptable (`phase4-engine-change-answers.md`, question 7), and PKHeX
compatibility is not a goal. This file is the running record of every field
that moved, so the damage is known rather than discovered.

**A save made before a change on this list will not read correctly after it.**
Start a new game after pulling a change recorded here.

## Boxed Pokemon, block A and block B (2026-09-20)

A boxed Pokemon is four 32-byte blocks, shuffled by personality and encrypted.
Block A was full: it ends with `ribbonsDS1`, a u32 at 0x1C, so there was no
room to widen anything in it. Block B had three spare bytes, `unused1` at 0x19
and `unused2` at 0x1A.

| Field | Was | Is | Why |
|---|---|---|---|
| ability | block A 0x0D, u8 | block B 0x1A, u16 | hg-engine's ability ids run past 255 and the donor ROM stores them two bytes wide |

Consequences:

- Block A 0x0D is now `unusedAbility` and is never read or written.
- Block B's `unused2` is gone; the `MON_DATA_UNUSED_114` parameter that was the
  only way to reach it has had its accessor cases removed. The enum member is
  left in place so no other parameter's value shifts.
- **On an old save every Pokemon's ability reads as ABILITY_NONE**, because
  block B's spare u16 was zero. `BoxPokemon_CalcAbility` runs on level-up and
  evolution, so a party would partly heal itself over time, but a battle before
  that would be played with no abilities at all. Start a new game.
- `UnkStruct_02078B40`, which mirrors block A for the party-summary path,
  carries the ability as a u16 too.
- Block B's `unused1` (0x19, HGSS shiny leaves) is still free.

## Species records, `pl_personal.narc` (2026-09-20)

Not save data, but it is the other format that moved and the two are usually
changed together.

| Field | Was | Is | Why |
|---|---|---|---|
| abilities | offset 22, `u8[2]` | offset 22, `u16[3]` | u16 ids, plus a third slot for the hidden ability |

The record grows from 44 bytes to 48. Everything after the abilities shifts by
four: `safariFleeRate` 24 to 28, the body-colour and flip-sprite byte 25 to 29,
the TM learnset masks 28 to 32. The two padding bytes stay where they were
relative to the masks.

`verify_narcs.py` can no longer compare `pl_personal.narc` against the base ROM
member for member. The check that replaced it, run once when the change was
made, reads the base ROM with the four-byte shift applied and confirms all 508
records still agree field for field. Rerun it if the record moves again.

## The Pokedex block grew, and with it every block after it (2026-09-21)

The `Pokedex` struct in `include/pokedex.h` sizes itself from
`NATIONAL_DEX_COUNT`, so raising the species count grew it without anyone
touching it:

| Field | Was | Is |
|---|---|---|
| `caughtPokemon`, `seenPokemon` | 16 u32 each | 21 u32 each |
| `recordedGenders[2]` | 16 u32 each | 21 u32 each |
| `recordedLanguages` | 496 bytes | 655 bytes |

About 239 bytes in total. That matters beyond the Pokedex itself, because
`gSaveTable` lays `SAVE_BLOCK_ID_NORMAL` out as a running total of each entry's
size and the Pokedex is eighth of about forty. **Every block after it moves**:
Daycare, Pal Pad, Misc, Field Overworld State, Underground, Regulation Battles,
Image Clips, Mailbox, Poffins, Record Mixed RNG, **Journal**, Trainer Case,
**Game Records**, Seal Case, Chatot, Frontier, Ribbons, Encounters, Global
Trade, TV Broadcast and the rest. Read an old save with the new build and all
of them are read from the wrong offset.

The PC boxes are the exception: they are their own block, `SAVE_BLOCK_ID_BOXES`,
and their offset does not depend on the Pokedex.

There is room. `SaveData_Init` asserts the whole of `SAVE_BLOCK_ID_NORMAL` fits
in `SAVE_SECTOR_SIZE * SAVE_PAGE_MAX`, 131,072 bytes, and 239 bytes does not
threaten that. The problem is compatibility, not capacity.

## The Battle Hall win records grew, and are now close to their ceiling (2026-09-21)

`BattleHallWinRecords` is three `u16[MAX_SPECIES]` arrays, so raising the
species count took it from 2,976 bytes to 3,932 without anyone touching it. It
moves nothing else: it is not in `SAVE_BLOCK_ID_NORMAL` but in the **extra** save
table, whose entries each sit at a fixed sector. This one is
`EXTRA_SAVE_TABLE_ENTRY_FRONTIER` at sector `SAVE_PAGE_MAX + 3`. An old save's
Battle Hall streaks are read from the wrong offsets inside that sector and
should be treated as lost, which matters to nobody before the Frontier opens.

The sector is the cap, and it is the only place in the save with no bounds check.
`SaveDataExtra_Save` writes `sizeFunc() + sizeof(SaveCheckFooter)` bytes straight
at `blockID * SAVE_SECTOR_SIZE`, and the next extra entry starts one sector later.
3,932 plus a 16-byte footer leaves 148 bytes of the 4,096. **`MAX_SPECIES` cannot
pass 679 without this struct overwriting the stored battle recordings.** A later
species addition has to move the entry, not grow into its neighbour.

## Not yet moved, but expected to

Listed so the next change can be planned rather than discovered:

- 30 PC boxes (Phase 4 element 8). The budget to check first: `SavePageInfo_Init`
  asserts the running total of **both** blocks against `SAVE_SECTOR_SIZE *
  SAVE_PAGE_MAX`, 131,072 bytes, and eighteen more boxes is on the order of
  70KB. There is room to raise `SAVE_PAGE_MAX`, because the primary copy starts
  at sector 0 and the backup at 64, but not to 64: the extra save table is laid
  out at `SAVE_PAGE_MAX + 0` through `+ 11`, so anything above **52** puts the
  battle recordings on top of the backup copy
- Move ids past 511 in level-up learnsets, which changes the learnset entry
  from one packed u16 to a (u16 level, u16 move) pair (Phase 4 element 4)
- The expanded bag, if the item pass outgrows Platinum's free item slots
  (Phase 4 element 7)

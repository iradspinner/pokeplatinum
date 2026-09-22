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

## Easy Chat word ids all moved, three times over (2026-09-22)

Found while element 4 was adding moves, and it covers elements 2, 3 and 4
together, because all three did the same thing and only this one noticed.

An Easy Chat word is not a per-group index. `include/applications/easy_chat/defs.h`
lays the groups end to end and makes every id a running total: `MOVE_WORD` starts
where the species names stop, `TYPE_WORD` where the move names stop, and so on
through abilities, trainer words, people, greetings, lifestyle, feelings, tough
words and the Union Room list. So **adding names to an early group shifts every
id in every later group**, and all three Phase 4 elements so far added names to an
early group: element 2 put 195 abilities in, element 3 put 161 species names in,
and element 4 puts 455 move names in.

| | Words | First id after the moves (`TYPE_WORD(0)`) |
|---|---|---|
| vanilla | 1,494 | 962 |
| after elements 2 and 3 | 1,850 | 1,123 |
| after element 4 | 2,305 | 1,578 |

The stored form is `EasyChatSentence`, whose `words[2]` are `u16`, and it is
saved in `Mail` (twenty of them in the mailbox, plus one on every Pokemon
holding mail) and in the player's trainer messages. **On an old save, every
stored word that was not a species name now names a different word**, so mail
and greetings read as nonsense rather than failing. Nothing crashes and nothing
overflows: 2,305 is far inside a `u16`, and `EASY_CHAT_WORD_COUNT` derives from
the same running total, so `EasyChatWordList`'s two `u16` arrays grew with it,
from about 7.4KB to 9.2KB on the Easy Chat app's own heap rather than in the
save.

Nothing to do at this size. It is written down because the trigger for the rule
at the top of this file is not "did I edit a save struct" but "did anything
sized by a constant I changed end up in the save", and a text bank's entry count
is exactly that kind of constant. The next element that adds names to any group
before the Union Room list moves these ids again.

## Not yet moved, but expected to

Listed so the next change can be planned rather than discovered:

- 30 PC boxes (Phase 4 element 8). The budget to check first: `SavePageInfo_Init`
  asserts the running total of **both** blocks against `SAVE_SECTOR_SIZE *
  SAVE_PAGE_MAX`, 131,072 bytes, and eighteen more boxes is on the order of
  70KB. There is room to raise `SAVE_PAGE_MAX`, because the primary copy starts
  at sector 0 and the backup at 64, but not to 64: the extra save table is laid
  out at `SAVE_PAGE_MAX + 0` through `+ 11`, so anything above **52** puts the
  battle recordings on top of the backup copy
- The expanded bag, if the item pass outgrows Platinum's free item slots
  (Phase 4 element 7)

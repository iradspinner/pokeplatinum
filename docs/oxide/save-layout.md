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

## Boxed Pokemon, the hidden ability bit (element 8)

| Field | Was | Is | Why |
|---|---|---|---|
| hasHiddenAbility | nothing (block A 0x0D, freed above) | block A 0x0D bit 0 | a Pokemon given its hidden ability keeps it through evolution and form changes |

`BoxPokemon_CalcAbility` reads the bit, so every path that recomputes an
ability (evolution, Shedinja, Giratina and Shaymin forms, the Rotom form
change) keeps the hidden slot. Bit 1 is the Ability Capsule's (next section). Old
saves read the bit as 0, which is what their Pokemon were, so this change
alone costs an old save nothing. The battle-recording copy of a Pokemon
(`UnkStruct_02078B40`) stores the ability itself, not the bit, which is all a
replay needs.

The one-shot script flag that hands a hidden ability to the next scripted wild
Pokemon, gift or egg, `FLAG_NEXT_MON_HIDDEN_ABILITY`, is flag 0x0990, which
was unused in vanilla and in the base ROM's scripts.

## Boxed Pokemon, the Ability Capsule bit (element 7)

| Field | Was | Is | Why |
|---|---|---|---|
| abilitySlotSwapped | nothing (block A 0x0D, freed above) | block A 0x0D bit 1 | an Ability Capsule swaps a Pokemon between its two ordinary abilities, and the swap has to outlive an evolution |

`BoxPokemon_CalcAbility` picks the ordinary slot from the personality's low
bit exclusive-or this bit, so the personality itself, and with it gender,
nature and shininess, never changes. Old saves read the bit as 0, which is no
swap. The Ability Patch needs no storage of its own: it sets the hidden
ability bit above. Bits 2 to 7 of the byte are Hyper Training's (next section).

## Boxed Pokemon, Mints and Hyper Training (element 7)

| Field | Was | Is | Why |
|---|---|---|---|
| hyperTrained | nothing (block A 0x0D, freed above) | block A 0x0D bits 2 to 7 | one bit per stat, in `enum PokemonStat` order (HP, Attack, Defense, Speed, Sp. Atk, Sp. Def), set by a Bottle Cap |
| statNature | block B 0x19 `unused1` (HGSS shiny leaves, never used in Platinum) | block B 0x19, u8 | 0, or one more than the nature a Mint gave the stats |

With these, block A's byte 0x0D is fully used and block B has no spare
byte left. `MON_DATA_UNUSED_113`, the only way to reach `unused1`, has had
its accessor cases removed; the enum member stays so no other parameter
shifts.

`Pokemon_CalcStats` reads both through two helpers in `pokemon.c`:
`Pokemon_GetStatIV` gives 31 for a trained stat and the stored IV
otherwise, and `Pokemon_GetStatNature` gives the Mint's nature when there
is one. The stored IVs and the personality are never changed, so Hidden
Power, breeding, the nature's name, flavours and Synchronize keep the real
values, as in the later games. The summary's IV viewer shows
`Pokemon_GetStatIV`, so it agrees with the stat page. Old saves read both
fields as 0, which is untrained and no Mint.

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

## The level-cap splits after Volkner's were renumbered (2026-09-27)

`VAR_LEVEL_CAP_SPLIT` holds the player's level-cap split as a number. The
Barry split (cap 71, from Volkner's Beacon Badge to the Elite Four) went in
between Volkner's and the League's, so the numbers after it moved up one.

| Value | Was | Is |
|---|---|---|
| 10 | League, cap 78 | Barry, cap 71 |
| 11 | no cap (after the Champion) | League, cap 78 |
| 12 | (none) | no cap |

A save made in the League split reads as the Barry split, capped at 71 until
the player enters the Elite Four again. A save made after the Champion reads
as the League split, capped at 78 until the Champion is beaten again.

## Meloetta: the species-sized save data is held, not grown (2026-09-27)

Meloetta is species 653, so the Egg and Bad Egg moved up to 654 and 655 and
`MAX_SPECIES` became 655. Three saved things were sized by the species count.
Each is now held at the size the 159 new species gave it, so a save made
before Meloetta reads exactly as it did:

| Saved data | Was sized by | Held at | Checked in |
|---|---|---|---|
| Pokedex language bytes | `MAX_SPECIES + 1` | 655, `DEX_LANGUAGE_SLOTS` | `src/pokedex.c` |
| Battle Hall streaks, three arrays | `MAX_SPECIES` | 654 each, `BATTLE_HALL_SPECIES_SLOTS` | `src/battle_hall_win_records.c` |
| Easy Chat species group (word ids) | the species name bank | 655 words, `EASY_CHAT_SPECIES_WORD_COUNT` | `include/applications/easy_chat/defs.h` |

The Pokedex would have kept its size, since padding absorbs one byte, but
the four flag bytes after the language bytes would each have moved by one,
`pokedexObtained` among them. The seen, caught and gender flags stay 21 words:
Meloetta takes bit 12 of the last word, and the Deoxys forms packed into bits
24 to 31 of that word leave room up to species 664, which `src/pokedex.c` now
checks as well. The Easy Chat hold costs no words, because the new species
were never in the Easy Chat list and the Egg words past them were never
offered. The word bank archive built after the hold is byte for byte the one
built before it.

Each hold is a compile-time check, so the next species added fails to build
until someone decides. Raising a hold moves that data on every existing save
and needs a section here.

A stored egg keeps its real species, with the egg bit beside it; the Egg's
species number is only produced when the game reads the Pokemon. So no egg in
a save changes meaning when the Egg's number moves. The daycare, the Pokedex,
the trade and hatch paths and the encounter tool's save reader all use the
constant or the egg bit, never a bare number.

One thing does move, and only on screen: mail stores each party Pokemon's
icon as its index in the icon archive. Meloetta's icon goes in before the
Egg's, so on mail written before this change, an egg, or a Deoxys, Unown,
Burmy, Wormadam, Shellos or Gastrodon in a form with its own icon, shows the
icon one place along. Giratina, Shaymin and Rotom forms are stored under their
base species' icon and are unaffected. Element 3 moved the same icons by 159
places and was not recorded here.

## The battle log, a new block in sector 44 (2026-09-28)

The last 60 trainer battles, for the OxiDex, are kept in flash sector 44 of
each half (0x2C000 and 0x6C000 in the .sav), which nothing had written
before. `docs/oxide/battle-log.md` has the byte layout. Both copies are
written after every save that writes the normal block; the main save's
blocks, sizes, footers and offsets do not change at all.

In RAM the log sits in the save image's free tail, after the boxes block
(0x1F200 today, 0xDB8 of the 0xE00 bytes free), which the main save never
writes. So a larger save table would have to move it; the game checks at
boot that it still fits.

An older save loads and plays as before: its two sectors are erased, which
reads as an empty log, and the first save writes a real one. Ian's save of
53b863005 was parsed with the new layout: both blocks valid at 0xD01C and
0x121E4, both log sectors erased. With no main save, an old log on the card
is ignored and the new game starts with an empty one.

## The Bag grew (element 7)

Vanilla sizes each Bag pocket to hold one of every item that goes in it.
Element 7's items broke that for three pockets, so they grew:

| Pocket | Kinds of item | Was | Is |
|---|---|---|---|
| Items | 186 (the Ice Stone, 2026-09-28, took one of the two spare) | 165 | 187 |
| Medicine | 61 | 40 | 63 |
| Berries | 65 | 64 | 65 |

The `Bag` struct is 184 bytes bigger (1,908 to 2,092). It is the fourth
entry of `SAVE_BLOCK_ID_NORMAL`, so every entry after it moves, which is
nearly the whole block: an old save reads wrongly from the Bag on.

The budget, measured from the build's own size functions rather than by
hand: the two blocks with their footers take 127,672 of the 131,072 bytes
`SavePageInfo_Init` allows, 3,400 spare. Vanilla's normal block was 53,036
bytes, exactly what PKHeX expects; the Pokedex's 240 and the Bag's 184 are
all it has grown.

One thing found on the way. `SaveBlockInfo_Init` also asserts that the
blocks, each rounded up to whole 4 KB sectors, number at most
`SAVE_PAGE_MAX` (32). Vanilla uses exactly 32 (13 and 19), and the Pokedex
growth already made the normal block 14, so that assert fails. It is
harmless: asserts are compiled out, the card layout packs the blocks by
bytes rather than by sector, and nothing reads the two sector fields the
assert checks. It matters only to a build with `PM_KEEP_ASSERTS`, and to
whoever raises `SAVE_PAGE_MAX` for the 30 PC boxes, who should fix or drop
that assert at the same time.

## 30 PC boxes (element 8, 2026-09-29)

`MAX_PC_BOXES` went from 18 to 30, as hg-engine has it, landing with element
7's Bag so that Ian starts one new game for both (his ruling, 2026-09-29).
`PCBoxes` keeps its shape, all the boxes' Pokemon first, then their names,
then their wallpapers, so it grows from 74,184 bytes to 123,636, and the boxes
block from 74,212 (0x121E4) to 123,664 (0x1E310). The normal block does not
change: 53,460 (0xD0D4), element 7's.

The main save no longer fits vanilla's 32 pages, so `SAVE_PAGE_MAX` is 45.
That sizes the RAM image the save loads into (131,072 bytes to 184,320), and
`HEAP_SIZE_SAVE` grew by the same 0xD000 (0x20E00 to 0x2DE00). The memory
came from main memory no heap had claimed: after the four boot heaps, the
task managers and the file table, about 164 KB of the arena was unused, and
112 KB still is. The boot-time load check borrows two image-sized buffers
from the application heap, 2 x 180 KB instead of 2 x 128 KB, at a point where
only the fonts are loaded. hg-engine did the same in HeartGold but shrank the
application heap to pay for it; Platinum had the room without that.

On the card, each half now reads:

| Sectors | What | Before |
|---|---|---|
| 0 to 43 | the main save, both blocks packed by bytes (177,124) | 0 to 31 |
| 44 | the battle log | 44 |
| 45 to 47 | Hall of Fame | 32 to 34 |
| 48 | Battle Hall win records | 35 |
| 49 to 56 | the four battle recordings | 36 to 43 |
| 57 to 63 | unused | 45 to 63 |

The extra save entries sit at `SAVE_PAGE_MAX + n`, so they moved on their
own; the battle log's sector is a constant and stayed. Its RAM copy still
lives in the image's tail, now at 0x2B3E4, with 7,196 bytes free for its
3,512. `tools/oxide/save_budget.py` measures all of this from a build and
checks it.

An older save does not load: its boxes block is not where the new layout
looks for it, and its Hall of Fame, Battle Hall records and recordings are
in sectors the game no longer reads. Element 7's Bag had already broken it.

Three smaller things moved with it. `SaveData_Erase` wiped the card with a
loop of `SAVE_PAGE_MAX * 2` sectors, which was every sector of both halves
only while the constant was 32; it now counts the 64 sectors of a half. The
names BOX 19 to BOX 30 were added at the end of the storage system's text
bank, not after BOX 18, so none of that bank's other messages moved. And the
PC screen's touch dial keeps a count, a 1 KB thumbnail and a flag for every
box, which vanilla sized and wrapped at a bare 18; they follow the constant,
and the box graphics heap grew by 16 KB for the extra 12,348 bytes.

For the OxiDex: `savefile.py` counts boxes from the boxes block's size, so a
30-box save needed only its layout, (0xD0D4, 0x1E310), in `KNOWN_LAYOUTS`; the
DPB1 payload and melonDS-oxide's live export take the count from the save and
the beacon, and read 30 with no change; and the Box sim's graveyard, the last
box, is box 30. The calculator's own Read Save did assume 18, with box 18 as
the graveyard; the encounter track's `encounter-save-30-boxes` reads as many
boxes as the block holds.

## The TM pocket grew (the TM pass, 2026-10-06)

The TM pass's list has 100 TMs: TM01 to TM94 and the six HMs left (HM01 Cut
and HM06 Rock Smash are placed nowhere), so `NUM_EXTRA_TMS` is 2 and the
Bag's TM pocket, `NUM_TMHMS` slots, grows from 100 to 102. The `Bag` struct
is 8 bytes bigger (2,092 to 2,100), and the normal block from 53,460
(0xD0D4) to 53,468 (0xD0DC); every entry after the Bag moves by 8 bytes,
the variables and flags among them (0xE64 to 0xE6C into the block). The
boxes block does not change. Ian starts a new game on the QA ROM, the first
with this change; a save from before it reads its party but not its Bag,
variables or flags.

`tools/oxide/save_budget.py` passes: the main save is 177,132 of the
image's 184,320 bytes, 3,092 short of the battle log's sector. For the
OxiDex, `savefile.py` works out the pocket's size from the build's own
headers, so it needed only the new layout, (0xD0DC, 0x1E310), as
`CURRENT_LAYOUT` and in `KNOWN_LAYOUTS` (Ian's permission, 2026-10-06), with
its test's sizes. The list comes from `tools/oxide/tm_items.py`, which also
writes the ids; a later list with a different number of TMs past TM92 moves
the save again, by 4 bytes a TM.

## Two spare variables hold the shops' purchases (2026-10-06)

The TMs the Veilstone counters and the Game Corner sell once (Ian,
2026-10-06; `include/data/sold_tms.h`) record each purchase as a bit in two
saved variables vanilla never used, renamed from `VAR_UNUSED_0x4031` and
`VAR_UNUSED_0x40A2` to `VAR_SOLD_TMS_0` and `VAR_SOLD_TMS_1`: 32 bits, one
per sold TM, given by `place_rewards.py` and kept by its TM. Nothing moves:
the variables were already in the save, and a save from before reads them
as zero, nothing bought. The Game Corner challenger takes vanilla's unused
trainer slot 6, so his defeated flag is that slot's, already in the save.

## Not yet moved, but expected to

Listed so the next change can be planned rather than discovered:

- More TMs past TM94. Each adds 4 bytes to the Bag and moves the rest of the
  normal save block (the section above). Past 120 TMs the species record
  grows by 4 bytes for each 32 more (`TM_LEARNSET_MASKS`), which is not save
  data but moves `pl_personal.narc`'s record size, and `verify_narcs.py`'s
  `PERSONAL_NEW_SIZE` would have to follow it
- The normal block, from the 30 PC boxes on (below). It may grow by at most
  3,100 bytes before the main save reaches the battle log's sector 44, and by
  3,684 before the log's RAM copy no longer fits the image's tail; the TM
  pass's 4 bytes a TM are far inside both. `tools/oxide/save_budget.py`
  measures both after any change. Past that, raise `SAVE_PAGE_MAX` and move
  the log up with it; `SAVE_PAGE_MAX` cannot pass 52, because the extra save
  table runs from `SAVE_PAGE_MAX + 0` to `+ 11` and would reach the backup
  copy at sector 64

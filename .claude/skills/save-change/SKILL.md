---
name: save-change
description: What any change to Platinum Oxide's save layout must do: keep Ian's current save loading or get his yes to a fresh start, dodge the species-count and Easy Chat traps, record the change in docs/oxide/save-layout.md, and keep the OxiDex's save reader in step. Use this before touching anything the save stores (the Pokedex, the boxes, the bag, a Pokemon's struct, flags and vars, Easy Chat words, the species count, a new saved block or extra-save sector), even if the task only says "add a species", "30 boxes" or "log battles".
---

# Changing the save

Ian plays Oxide as it is built, and the OxiDex reads his save live for Sync
and the Box sim. So a save change has three audiences: the game, his save in
progress, and the tools that parse it.

## 1. Find what moves

These have moved a save before, each found the hard way:

- **Anything sized by the species count**: the Pokedex's seen, caught and
  gender words, its per-species language bytes, the Battle Hall's win
  records and the Easy Chat species group. When the new count still fits,
  keep the stored array at its present size (Meloetta did, 2026-09-27).
- **Easy Chat word ids** are a running total across the text banks that
  hold names, so adding a name to any of them shifts every later word id
  and changes the meaning of saved mail and greetings. Meloetta took the
  never-offered EGG word slot instead of adding one.
- **A boxed Pokemon's blocks.** Block A is full. `docs/oxide/save-layout.md`
  says what is still free.
- **The bag.** Element 7 widened three pockets.
- **New saved state.** Prefer space that is already free. In each flash half,
  sectors 0 to 31 hold the main save, 32 to 43 the Hall of Fame, Frontier and
  recordings, and 44 to 63 have never been written. `SaveDataExtra_Get` and
  `SaveDataExtra_Save` also change the main save's own state, so a new block
  there wants its own reader and writer.
- **Moved constants.** When `SPECIES_EGG` or `SPECIES_BAD_EGG` moves, check
  that a stored egg keeps its real species with the egg bit, and that the
  daycare, hatching and trades use the constant. A bare number near a
  species-indexed table is a bug waiting for the constant to move.

## 2. Decide whether Ian's save survives

Ian ruled (2026-09-28, on element 7's bigger Bag) that a change which
stops his save loading costs him a fresh start, not a save converter. So
no converter is written; before the landing, tell him the change breaks
his save and which ROM starts the new game, and note it in the landing's
report. A change that can keep his save loading at no real cost still
should (Meloetta kept the Pokedex arrays at their size).

## 3. Prove it

- Parse his latest save with the new layout. His saves are in
  `~/oxide-playtest/`, and the OxiDex's watched path is in
  `~/.config/oxidex/settings.json`. The reader is
  `tools/oxide/encounters/savefile.py`; it checks the blocks, footers,
  party, boxes and flags. Work on a copy: never write to his save, and never
  commit one.
- If the normal block's size or position changes, the reader's
  `BLOCK_POSITIONS` must learn the new layout, or Sync stops reading his
  save. The box count comes from the storage block's size, so more boxes
  need no constant, but the block moves.
- Record the change in `docs/oxide/save-layout.md`: the field, what it was,
  what it is, why, and what an older save sees.
- Tell the encounter tool builder: `savefile.py` and the OxiDex's readers
  are the encounter track's files.
- Add an in-game check to `docs/oxide/ingame-checklist.md` for Ian's bug
  sweep: his save loads, and the changed thing shows.

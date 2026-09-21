---
name: read-donor
description: How to read content out of the Hardlove Gold donor ROM (an hg-engine HeartGold build) for Platinum Oxide, and carry it into the pokeplatinum fork with tools/oxide/donor.py and import_donor.py. Use this whenever a session needs a species record, learnset, evolution, ability, base experience, hidden ability, form table, move, text or any other table from Hardlove or hg-engine, including for Phase 4 elements 3 to 8, even if the user just says "bring in Sylveon" or "what does the donor say".
---

# Reading the donor

Hardlove Gold is a stock hg-engine build with content on top, so its tables are
hg-engine's layouts, not vanilla HeartGold's, and nothing can be copied by path
name: HeartGold collapses everything into numbered NARCs (`a/0/x/y`). The
readers already exist; use them rather than reopening the ROM by hand.

- Reader: `tools/oxide/donor.py` (species records, learnsets, evolutions, the
  `a/0/2/8` additions, text banks). Nothing in it writes.
- Writer: `tools/oxide/import_donor.py`, one idempotent subcommand per table,
  the counterpart of `import_base_rom.py`. Run a subcommand twice and the second
  run reports nothing to do; `--dry-run` shows what it would change.
- Evidence: `docs/oxide/donor-tables.md` records what each table and each
  `a/0/2/8` member is and how it was identified, by reading, since none of it
  came from hg-engine's source. Read it before trusting a number.
- The ROM: pinned copy at `~/roms/hardlove.nds`. The original in the G: folder
  is a copy too and may be written to for experiments, but say so in the
  findings log if you do, so a later comparison is not silently against an
  altered file.

## Facts that decide how a record is read

- Species records are 44 bytes in hg-engine's `SpeciesData` layout: ability 1
  is a u16 at 0x16 and ability 2 a u16 at 0x1A (repurposed padding); base
  experience and TM compatibility are zero in the record because hg-engine moved
  them out (base exp to `a/0/2/8` member 8, TM bits into the learnset data). EV
  yields and held items being zero is Hardlove's own choice, not a layout fact.
- Donor index for a Gen 5 and later species is National Dex number plus 50,
  because 0494 to 0543 are form and spare slots. On the Oxide side that is a
  lookup, not an identity: Oxide ids are dense after Arceus (494 to 652) in
  pick-list `dex_pos` order, `docs/oxide/species-id-map.csv` is the assignment.
- Fairy is type 9 in the donor (the dead Mystery slot); Oxide's is 18.
- **The donor is Hardlove's design, not a canonical reference.** Against the ROM
  it changes 28 of 493 natives' types and 317 of their abilities. So for the 159
  new species the split is: base stats, types and both abilities and the hidden
  ability come from `New Pokedex.xlsx`; everything else comes from the donor.
  `docs/oxide/donor-tables.md` has the table.
- **Do not read species data from the DSPRE `unpacked` folder.** It disagrees
  with the ROM on 242 of 1476 species records, at stats, types and abilities; it
  is a DSPRE working copy someone has edited. `synthOverlay` does match, but go
  through `donor.py` and the ROM anyway.
- Learnsets are 34 fixed slots of (u16 move, u16 level); level 0 means an
  evolution move, which Platinum has no concept of. Platinum packs level and
  move into one u16 with the move capped at 511; widening that format is part
  of the move expansion (element 4).
- Evolutions are 9 slots of 6 bytes plus 2 padding per species. Four donor
  methods do not exist in Platinum, two donor targets point past the end of
  Hardlove's own table, and three natives gain an evolution; the pick-list's
  evolution table (`docs/oxide/species-pick-list.md`) says what each new species
  is meant to use instead, and it never uses trade methods.
- Ability ids equal the donor's, all 319 imported, names and descriptions
  included; effects are element 5. Where Hardlove reuses a display name for
  several ids the repeats carry a numeric suffix rather than a guess.
- `a/0/2/8` members: 7 hidden abilities (u16 per species), 8 base experience
  (u16), 9 icon palettes (u8), 10 unidentified (u16, 26 non-zero; see the doc),
  11 form data (32 u16 per species, the personal indices of its forms), 12 and
  13 form-to-species and reversion. Hardlove's item table has 2,687 records;
  Oxide takes a curated subset into Platinum's free slots (element 7).
- Encounter and trainer records encode forms as `(form << 11) | species`.
- The form and alt-evolution slots on the pick-list (Alolan Ninetales 1132,
  Galarian Rapidash 1158, Gyarados M 1087, and the rest of that table) were
  found by six-stat fingerprint. Zygarde is ambiguous between 1269 and 1270.

## How to bring a table in

1. Check `donor-tables.md` for the table; if it is not there yet, read it with
   `donor.py`, work out the layout from the bytes, and add a section with the
   evidence before writing an importer for it.
2. Add a subcommand to `import_donor.py` that writes through the repo's own
   style (`jsonstyle.py` for `res/` JSON, the generated text files for enums),
   keyed by the Oxide id from `species-id-map.csv`, never by donor index.
3. Where the donor and the base ROM disagree on a native, the base ROM wins
   (that is Phase 3's carry-over) unless the tracker says otherwise; say which
   values were left alone.
4. Rebuild, verify with `verify_narcs.py` (declare intended divergence in its
   `DIVERGED` list), and record in `donor-tables.md` anything the read taught you
   about the layout.

`romtool\hardlove.py` in the G: hub folder is an older HeartGold-shaped reader
with a proven NARC round trip; `donor.py` supersedes it for this repo.

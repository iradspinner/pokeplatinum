# Species ID scheme

**Decided by Ian, 2026-09-20:** "just go numerically increasing after the end
of the Platinum Pokedex numbers". This replaces the pick-list's earlier working
assumption that National Dex numbers would double as internal ids (Snivy 495),
which would have grown every species-indexed table to 1010 slots plus forms to
hold 159 new species.

## The rule

New species are appended to `generated/species.txt` immediately after
`SPECIES_ARCEUS`, so they take ids **494 through 652**, and `SPECIES_EGG` and
`SPECIES_BAD_EGG` move up behind them to 653 and 654.

The order within that block is the pick-list's `dex_pos`, which is Ian's
designed Oxide dex order. That keeps the internal ids running in the same
direction as the dex the player sees, and because the dex already keeps
evolution families together, the families end up adjacent in id space too
(Charcadet 648, Armarouge 649, Ceruledge 650).

The assignment is in `species-id-map.csv` and is **frozen**: element 3 landed on it, and every species-indexed table, save and script now depends on those ids.
Re-ordering the dex afterwards changes the dex table, not the ids.

## Why appending before SPECIES_EGG is the whole change

Almost everything in the tree that is sized by the species count derives from
the enum rather than hard-coding a number, so putting the new block in the
right place makes the rest follow:

| | Before | After |
|---|---|---|
| `MAX_SPECIES` (= `SPECIES_BAD_EGG`) | 495 | 654 |
| `NATIONAL_DEX_COUNT` (= `MAX_SPECIES - 2`) | 493 | 652 |
| `NATIONAL_DEX_MAX` (= `SPECIES_EGG`, speciesproc) | 494 | 653 |
| `MOVESET_FORM_*` (= `NATIONAL_DEX_COUNT + 1..12`) | 494..505 | 653..664 |
| `pl_personal`, `evo`, `wotbl` members | 508 | 667 |
| sprite offsets (`4 * NATIONAL_DEX_MAX`) | 1976 | 2612 |

The registry that those archives are built from is
`[NONE, species..., EGG, BAD_EGG, the twelve alt-form records]`, in that order,
so the alt-form records stay last and their indices shift up by 159 together.

## Regional forms get their own species ids

Ten of the 159 are regional forms of species Platinum already has (Alolan
Ninetales, the Galarian birds, and so on). They are ids of their own rather than
form records on the base species, for three reasons: the pick-list gives each
one its own `dex_pos`, so Ian wants them as separate dex entries, which Gen 4's
form system cannot do; they carry their own types, stats, abilities and
learnsets; and Hardlove stores them as separate species records, so the import
is a straight copy rather than a conversion. Ten ids is a cheap price.

The two alt-evolution "megas", Gyarados M and Lopunny M, are ordinary
evolutions and get ids for the same reason.

## What this does not decide

- Which slot in the dex a species occupies is `dex_pos`, a separate number.
  Nothing in the engine should use `dex_pos` as an id or the reverse.
- Form records for the *new* species, if any need them, append to
  `alt_forms_with_data` in `speciesproc.c` after the existing twelve.

# Species ID scheme

**Decided by Ian, 2026-09-20:** "just go numerically increasing after the end
of the Platinum Pokedex numbers". This replaces the pick-list's earlier working
assumption that National Dex numbers would double as internal ids (Snivy 495),
which would have grown every species-indexed table to 1010 slots plus forms to
hold 159 new species.

## The rule

New species are appended to `generated/species.txt` immediately before
`SPECIES_EGG`. Element 3's 159 took ids **494 through 652**, and Meloetta
took **653** (2026-09-27). `SPECIES_EGG` and `SPECIES_BAD_EGG` sit behind
them, at **654 and 655** since Meloetta (653 and 654 before it).

The order within that block is the pick-list's `dex_pos`, which is Ian's
designed Oxide dex order. That keeps the internal ids running in the same
direction as the dex the player sees, and because the dex already keeps
evolution families together, the families end up adjacent in id space too
(Charcadet 648, Armarouge 649, Ceruledge 650).

The assignment is in `species-id-map.csv` and is **frozen**: element 3 landed on it, and every species-indexed table, save and script now depends on those ids.
Re-ordering the dex afterwards changes the dex table, not the ids. A species
added later goes on the end, whatever its `dex_pos`: Meloetta is 653 with
`dex_pos` 503.

Adding one moves the Egg and Bad Egg, so it touches the save. Three saved
things are sized by the species count, and each is now held at its size
with a compile-time check, so the next addition stops the build until
someone decides (`save-layout.md`, the Meloetta section).

## Why appending before SPECIES_EGG is the whole change

Almost everything in the tree that is sized by the species count derives from
the enum rather than hard-coding a number, so putting the new block in the
right place makes the rest follow:

| | Vanilla | Element 3 | Meloetta |
|---|---|---|---|
| `MAX_SPECIES` (= `SPECIES_BAD_EGG`) | 495 | 654 | 655 |
| `NATIONAL_DEX_COUNT` (= `MAX_SPECIES - 2`) | 493 | 652 | 653 |
| `NATIONAL_DEX_MAX` (= `SPECIES_EGG`, speciesproc) | 494 | 653 | 654 |
| `MOVESET_FORM_*` (= `NATIONAL_DEX_COUNT + 1..12`) | 494..505 | 653..664 | 654..665 |
| `pl_personal`, `evo`, `wotbl` members | 508 | 667 | 668 |
| sprite offsets (`4 * NATIONAL_DEX_MAX`) | 1976 | 2612 | 2616 |

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

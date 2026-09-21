---
name: port-element
description: How to port one Phase 4 engine element into the pokeplatinum decomp for Platinum Oxide (a type, the ability widening, the species-slot expansion, the move expansion, ability effects, battle AI, items, or any hg-engine feature from the Phase 4 list). Use this whenever a session is about to change the battle engine, a species-indexed or move-indexed table, a struct that reaches the save file, or generated constants in this repo, even if the user just says "do element 3" or names a feature like hidden abilities or 30 PC boxes.
---

# Porting a Phase 4 element

Each element is the same shape of job: hg-engine did it for HeartGold as a
patch kit, and here it is done as ordinary C and data changes to a decomp that
builds a byte-exact retail ROM. hg-engine's addresses are useless; its design
and its C are the reference. The Fairy type (element 1) and the ability
widening (element 2) are the worked examples; read their tracker entries and
commit messages first, they are the house style.

## Before touching code

1. Read the element's line in the tracker's Phase 4 section and the answer that
   scopes it in `docs/oxide/phase4-engine-change-answers.md`. Ian answered every
   scope question there; do not re-ask what is answered.
2. Find the reference implementation. `docs/oxide/phase1-hg-engine-survey.md`
   section 3 maps each feature to hg-engine's files (`armips/asm/*.s` for the
   byte-level sites, `src/battle/*.c` and `src/individual/*.c` for behaviour,
   `CONFIG.md` for the toggle names). Read the hg-engine source for the feature,
   not a summary of it.
3. Find every site in the decomp. The decomp has no assembly, so a struct field
   or a constant is the whole story: `grep -rn` for the constant (`MAX_SPECIES`,
   `NUM_POKEMON_TYPES`, the field name), and read `generated/` and
   `tools/dataproc/` because most counts derive from a generated enum rather than
   a literal. Element 2's lesson: the visible half (the data record) is easy, the
   half that reaches the save file is the one that breaks things.
4. If the element reads donor content, use `tools/oxide/donor.py` and
   `tools/oxide/import_donor.py` (see the `read-donor` skill), never hand-typed
   values.
5. Write down the emulator test that proves the element before writing code. If
   you cannot name one, the element is not defined yet.

## Doing it

- Make the mechanism and the content separate commits where you can (Fairy: the
  type, then the retypings). Either can then be reverted alone.
- Prefer the decomp's own idiom over hg-engine's tricks: hg-engine relocated
  data to spare NARCs and patched sizes because it could not relink; here you
  change the struct and the compiler updates every use.
- Watch the packers. The species processor buckets the dex index archive by type
  and then by body shape, so adding a type shifted every body-shape bucket; the
  learnset packer caps move ids at 511; the trainer processor sizes party records
  from a data-type byte. Anything under `tools/dataproc/` that reads a count you
  changed needs reading.
- Fixed art is the usual leftover: packed atlases and fixed grid layouts
  (Pokedex plates, search grid, Battle Hall grid) do not grow with an enum.
  Record what is left short and what the player sees instead, rather than
  silently leaving it.
- Keep the base ROM's carried-over edits. Before overwriting a species, move or
  trainer value, check whether the base ROM changed it (compare to
  `~/roms/vanilla.nds` through the importer's decoders) and say so if it did.

## Before calling it done

1. `make rom` succeeds.
2. Declare intended divergence so the integration gate keeps meaning something.
   Species and move records that now differ from the base ROM go in `DIVERGED`
   in `tools/oxide/verify_narcs.py` (member indices, allowed byte offsets, why);
   if the record layout itself changed, teach the verifier the new layout the way
   element 2 did, so it reports "0 disagreeing, N intended" rather than 506
   mismatches. Run `python3 tools/oxide/verify_narcs.py --built
   build/pokeplatinum.us.nds --ref ~/roms/base.nds` and read what it says.
3. If a save-file field moved: a row in `docs/oxide/save-layout.md` with was,
   is, why, and what an old save now reads as.
4. `python3 tools/oxide/import_base_rom.py --base ~/roms/base.nds --vanilla
   ~/roms/vanilla.nds --dry-run` still reports every count 0; if it wants to
   re-import something you changed on purpose, it needs a skip entry.
5. The three `bulk_*.py --dry-run` runs and the encounter tests still pass;
   `tools/oxide/integrate.sh --no-push` runs the whole gate in one go.
6. Tracker entry under Phase 4 in the established shape: what was done and
   where, the trap for whoever adds the next one, what is deliberately left
   short, and the emulator test Ian should run, which also goes on the "Waiting
   on Ian" list. A durable fact (a format detail, a wrong assumption corrected)
   goes in the design doc's findings log as well.
7. Commit message: why, what changed, what was verified and how, what is left.

## Things already decided, so do not re-decide them

- Species ids are dense and appended after Arceus (494 to 652, pick-list
  `dex_pos` order); `docs/oxide/species-id-scheme.md` and `species-id-map.csv`.
- Ability ids equal the donor's; the whole 319-entry table is imported.
- Fairy is type 18 here and type 9 (the dead Mystery slot) in the donor.
- Save compatibility with vanilla and PKHeX is not a goal; breaking it is fine
  as long as `save-layout.md` records it.
- Hardlove's battle AI is not ported; Platinum's AI is the baseline.

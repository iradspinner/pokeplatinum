---
name: port-element
description: How to port one Phase 4 engine element into the pokeplatinum decomp for Platinum Oxide (a type, the ability widening, the species-slot expansion, the move expansion, ability effects, battle AI, items, or any hg-engine feature from the Phase 4 list). Use this whenever a session is about to change the battle engine, a species-indexed or move-indexed table, a struct that reaches the save file, or generated constants in this repo, even if the user just says "do element 3" or names a feature like hidden abilities or 30 PC boxes.
---

# Porting a Phase 4 element

Each element is the same shape of job: hg-engine did it for HeartGold as a
patch kit, and here it is done as ordinary C and data changes to a decomp that
builds a byte-exact retail ROM. hg-engine's addresses are useless; its design
and its C are the reference. The Fairy type (element 1) and the ability
widening (element 2) are the worked examples; read their write-ups in
`docs/oxide/tracker-archive.md` (Phase 4) and their commit messages first, they
are the house style.

## Before touching code

1. Read the element's line in the tracker's Phase 4 section and the answer that
   scopes it in `docs/oxide/phase4-engine-change-answers.md`. Ian answered every
   scope question there; do not re-ask what is answered.
2. Find the reference implementation. `docs/oxide/phase1-hg-engine-survey.md`
   section 3 maps each feature to hg-engine's files (`armips/asm/*.s` for the
   byte-level sites, `src/battle/*.c` and `src/individual/*.c` for behaviour,
   `CONFIG.md` for the toggle names). Read the hg-engine source for the feature,
   not a summary of it. `~/hg-engine` is a sparse clone without `armips/asm`
   on disk; `git -C ~/hg-engine show HEAD:armips/asm/<file>` reads it.
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
  learnset packer capped move ids at 511 until element 4 widened the entry; the
  trainer processor sizes party records
  from a data-type byte. Anything under `tools/dataproc/` that reads a count you
  changed needs reading.
- Fixed art is the usual leftover: packed atlases and fixed grid layouts
  (Pokedex plates, search grid, Battle Hall grid) do not grow with an enum.
  Record what is left short and what the player sees instead, rather than
  silently leaving it.
- Keep the base ROM's carried-over edits. Before overwriting a species, move or
  trainer value, check whether the base ROM changed it (compare to
  `~/roms/vanilla.nds` through the importer's decoders) and say so if it did.
- Watch the running totals. Easy Chat word ids count across the text banks of
  names (species, then moves, then abilities and on), so a bank of names that
  grows renumbers every later group, and those ids are stored in mail and
  trainer messages. Elements 2, 3 and 4 each did it; `save-layout.md` has the
  row and the findings log (2026-09-22) the detail.

## Battle engine traps (element 4)

- New per-battler state goes in the spare bits of the battler's move-effects
  mask, not in a new field: Oxide has taken bits 19 and 20 (Laser Focus's
  countdown) and bit 31 (Smack Down's grounding). Growing `MoveEffectsData`
  moves every later field of the battle context and changes the trainer AI
  overlay in ways `romdiff.py` cannot explain. The same rule holds for other
  state: a side takes bits 11 and 15 of its conditions mask (Sticky Web,
  Aurora Veil) and fields from `SideConditions`' padding (Aurora Veil's turns,
  Belch's per-party-slot berry record); a one-turn state goes in `TurnFlags`'
  padding, which clears every turn (the side guards, Beak Blast's heat).
  The field conditions mask has bits 19 to 29 taken (Trick Room's and Wonder
  Room's permanent bits, Neutralizing Gas, Echoed Voice's five, Wonder Room's
  turns), so only 30 and 31 are free; check `condition.h` before claiming one.
  The move-effects mask is now full, so a later-games volatile state goes in
  `BattleMon.oxideFlags` (the old `padding007A`, `OXIDE_MON_FLAG_*` in
  `constants/battle/moves.h`, reached by scripts as `BATTLEMON_OXIDE_FLAGS`):
  bits 0 to 4 are taken (Salt Cure, Octolock, Sky Drop's hold and holder),
  and the word clears when the battler leaves the field. A per-action flag
  goes in `SelfTurnFlags.statusFlags` (bit 4, Mind Blown's cost). Field-wide
  state with a counter has `BattleContext`'s old padding: `magicRoomTurns`
  (was `padding0060`, script variable `BTLVAR_MAGIC_ROOM_TURNS`) and
  `teatimeNext` (three bits of the old `padding3154_01`, 28 left). A fact
  about the battler's species, worked out once as it comes in, goes beside
  `isShiny`: `BattleMon.canEvolve` took one of the two padding bits there
  (the Eviolite), one is left.
- A new battle script command is appended after `End`, so no opcode moves. New
  subscripts and side-effect pointers are appended only once implemented, and a
  stat-stage pointer only once `ChangeStatStage` names its range.
- New battle strings are appended after Platinum's own 1,269 messages (the
  converter's `HG_STRINGS` maps hg-engine's numbers onto them) and measured
  against Platinum's worst case, 196 px with a ten-letter name.
- `import_moves.py` leaves an existing `script.s` and `anim.s` alone on a rerun,
  but `--force` overwrites them, including the hand-made charge animations of
  Freeze Shock, Ice Burn and Geomancy (listed in
  `docs/oxide/move-animation-map.json`).
- Ability suppression lives in `Battler_Ability`: Gastro Acid, and Neutralizing
  Gas, which is worked out there from the battlers on the field. A reader that
  takes `battleMons[].ability` or the party's ability directly goes around it,
  as `BtlCmd_TryRestoreStatusOnSwitch` does for Natural Cure, Regenerator and
  the switch-out cures, and as the critical-hit roll did for Super Luck until
  2026-09-26. A new suppression, or a new ability read that way, has to cover
  both.
- The trainer AI keeps its own copies of many engine rules: immunities and
  absorbing abilities in `script.s`'s Basic routine, move lists (sound, powder,
  ball and bomb), computed powers in `TrainerAI_CalcDamage`, trapping in
  `TrainerAI_ShouldSwitch`. A rule change in the engine should grep
  `src/battle/trainer_ai/` for the ability, move or effect it touches and bring
  the copy along, or say so in the report for element 6 (its 2026-09-26
  catch-up is in `docs/oxide/battle-ai/README.md`). The AI is overlay 14, whose
  slot must end below the battle overlay's start (`SDK_OVERLAY.battle.START`
  in the build's `main.nef.xMAP`; 0x0223B520 on 2026-09-26, and it moves when
  the battle animation overlay grows).
- A C change is checked with `tools/oxide/romdiff.py` against the previous
  commit's ROM: every difference must be the intended members or a relink that
  the tool explains, and it exits non-zero on anything else. It looks for
  relinked branches only when an overlay changes size, so when overlay 16
  changes but keeps its size (a few bytes absorbed by alignment padding) it
  exits 0 without checking arm9 or the other overlays; run its `explain()` by
  hand with overlay 16 as the region, as the Super Luck fix did (d29a8a14).
- Each batch of effect scripts adds its move sets to the test kit in the same
  commit (`docs/oxide/test-kit.md` says how). New sets go on the move-set
  menu's second page: a field menu holds 28 entries and a 29th is written
  past its arrays, unchecked.
- `convert_battle_scripts.py --audit` cannot see a move whose effect is a
  plain hit but whose power hg-engine computes in C, keyed on the move
  (`CalcBaseDamage`): effect 0 counts as done. Those go in
  `BattleScript_ComputedMovePower` in `battle_script.c`. A move whose
  power is computed carries power 1 in its record, never 0: the type chart
  reads 0 as a status move and sets no effectiveness flags. Moves that pick
  a different stat or type are the same blind spot: the stat choosers (Foul
  Play, Body Press, Psyshock, Sacred Sword and their kin) are keyed on the
  move in `BattleSystem_CalcMoveDamage`, and the type choosers (Freeze-Dry,
  Flying Press) in `MoveChartMultiplier` and `MoveReadsChartEntry`, which
  both type chart walks read. A move that reads more than two chart
  entries needs its effectiveness flags set from the net result
  (`SetNetEffectiveness`), because Platinum's running toggle misreads four.
- The audit has a second blind spot: it triages only effect ids 277 and
  up, so a new move the importer gave a native effect is never looked at,
  however much hg-engine adds to it in C keyed on the move (Shore Up sits on
  Synthesis's effect and healed by Synthesis's weather rule). For a new move
  on a native effect, grep hg-engine's C for the move's constant.
- Before routing a move to an AI routine, read its effect script, not its
  effect's name: Meteor Beam's and Electro Shot's "charge turn" effects are
  plain hits today. Power doubled in a script (`BTLVAR_POWER_MULTI`: Hex,
  Venoshock, Acrobatics) never reaches the AI's damage estimate, so those
  follow vanilla's Facade and Brine with a +1 Expert bonus when it applies.
- dataproc's range helpers (`dp_u16range` and its siblings) crash instead of
  reporting when the value came from `dp_lookup`, because the node keeps the
  pointer and the looked-up value in one union. Compare a looked-up enum
  yourself, as `trainerproc.c` does for a nature, or fix the library first.
- A new species' cry must be registered, not only generated: a bank and a
  wave archive in `res/sound/pl_sound_data.json` at its species id, since
  `Sound_PlayPokemonCry` indexes the bank table by species (element 3's first
  pass was silent and crashed the Pokedex cry screen). A cry must fit
  `PLAYER_PV`'s 24,200-byte heap at a byte a sample, so vanilla's longest,
  Jynx's 23,524 samples, is the practical limit. `nitrosfx`'s `WriteSdat` has
  a padding fix in `tools/nitrosfx/sdat.c` that matters once SYMB, INFO or FAT
  grows enough to move the FILE block; keep it.

## Before calling it done

1. The ROM builds with `make rom`, and once pushed its SHA-1 matches GitHub's
   build of the same commit (`integrate.sh` compares them).
2. Declare intended divergence so the integration gate keeps meaning something
   (the `oxide-session` skill lists every register). Species and move records
   that now differ from the base ROM go in `DIVERGED`
   in `tools/oxide/verify_narcs.py` (member indices, allowed byte offsets, why);
   if the record layout itself changed, teach the verifier the new layout the way
   element 2 did, so it reports "0 disagreeing, N intended" rather than 506
   mismatches. Run `python3 tools/oxide/verify_narcs.py --built <ROM>
   --ref ~/roms/base.nds` and read what it says.
3. If a save-file field moved: a row in `docs/oxide/save-layout.md` with was,
   is, why, and what an old save now reads as.
4. `python3 tools/oxide/import_base_rom.py --base ~/roms/base.nds --vanilla
   ~/roms/vanilla.nds --dry-run` still reports every count 0; if it wants to
   re-import something you changed on purpose, it needs a skip entry
   (`MOVES_DIVERGED` for a move field, as Poison Gas's range has). The dry
   run rewrites `tools/oxide/import_report.md`; restore it with
   `git checkout tools/oxide/import_report.md` before committing.
5. The three `bulk_*.py --dry-run` runs and the encounter tests still pass;
   `bash tools/oxide/integrate.sh --verify-only --rom <ROM>` runs the whole
   gate in one go (a cloud session drops `--rom`).
6. Tracker entry under Phase 4 in the established shape: what was done and
   where, the trap for whoever adds the next one, what is deliberately left
   short, and the emulator test Ian should run, which goes in
   `docs/oxide/ingame-checklist.md`. A durable fact (a format detail, a wrong assumption corrected)
   goes in the design doc's findings log as well. Once a step is finished its
   write-up moves to `docs/oxide/tracker-archive.md`, which agents read only
   when pointed there, so a trap still in force must also live in this skill or
   the findings log, and a left-short list stays in the tracker as open work.
7. Commit message: why, what changed, what was verified and how, what is left.

## Things already decided, so do not re-decide them

- Species ids are dense and appended after Arceus (494 to 652, pick-list
  `dex_pos` order); `docs/oxide/species-id-scheme.md` and `species-id-map.csv`.
- Ability ids equal the donor's; the whole 319-entry table is imported.
- Fairy is type 18 here and type 9 (the dead Mystery slot) in the donor.
- Save compatibility with vanilla and PKHeX is not a goal; breaking it is fine
  as long as `save-layout.md` records it.
- Hardlove's battle AI is not ported; Platinum's AI is the baseline.
- Every damaging move carries the King's Rock flag, the new ones and the 95
  natives alike (Ian, 2026-09-22).
- A fix to a bug vanilla Platinum also has is flagged to Ian and made in its own
  commit titled VANILLA FIX, as elements 4 and 6 did.

# Platinum Oxide: start here

One page, for a fresh chat that needs to be useful without reading everything.
Written 2026-09-15, refreshed 2026-09-20. **Check the date against the repo before trusting the status
section**: the live docs are `docs/oxide/design-doc.md` and
`docs/oxide/tracker.md` on branch `oxide` of `iradspinner/pokeplatinum`, and they
move faster than this file.

## What the project is

Port the engine expansions of Hardlove Gold (a HeartGold hack built on hg-engine)
into Pokemon Platinum: Fairy type, u16 ability IDs, the expanded move table, and a
hand-picked subset of the new species, plus battle-AI updates. The chosen method
is to edit the `pret/pokeplatinum` decompilation directly and build the ROM from
source, not to patch a ROM. Hobby project, no QA gate.

## The three surfaces and who owns what

| Surface | Owns |
|---|---|
| Claude Code in WSL2, `~/pokeplatinum`, branch `oxide` | All source edits, builds, commits, pushes. The repo's `docs/oxide/` is the live design doc and tracker. |
| A chat in this project (this file's audience) | Design questions, Hardlove donor analysis, base-ROM archaeology, anything that needs a second opinion before it becomes code. Produces notes, not commits. |
| The project folder `G:\...\Hardlove Gold-Platinum Oxide Integration Project` | Both ROMs, both DSPRE extractions, and snapshot copies of the docs and notes. |

The `claude/platinum-oxide-*.md` docs in this project's knowledge are a snapshot
frozen 2026-09-15. Treat them as background, not current status.

## State as of 2026-09-20

Phase 3 is done except for the field scripts and events. Everything below was
verified against the base ROM, not just built:

- The approach, validated by building a byte-exact retail Platinum ROM from the
  decomp, and the fork building in WSL2.
- Species, moves, evolutions and learnsets imported.
- All 928 trainers carried over, including two new per-mon fields for ability
  and gender, with zero field mismatches and an emulator check on Route 202.
- All four of the base ROM's synthetic-overlay routines ported as ordinary C:
  no items in trainer battles, Rare Candy chaining, uncapped battle frame rate,
  EV/IV viewer.
- 125 wild-encounter tables, both edited in-game trades, 18 text banks, 58 map
  headers, and the small constant edits (shiny odds, vitamin EV cap, new-game
  option defaults, HMs forgettable, reusable TMs).

Three sets of base-ROM changes were deliberately **not** carried over, because
the evidence says DSPRE rewrote them rather than Ian editing them: sprite
heights, the six vitamin item records, and the encounter `unown_table` and
`rate_form` fields. Each one's reasoning is in the tracker; any of them can be
overruled.

What is left is the scripts and events, which touch 184 maps. Read
`notes/phase3-scripts-and-events-plan.md` before starting on it. A script
disassembler and an event decoder are built and verified against both ROMs; a
movement-block decoder, `.s` emission and a byte-identical round trip are not.

The species pick-list is settled and lives in `notes/species-pick-list.md`. Its
21-row stat conflict with the base ROM is tabled for a later whole-dex balance
pass, so it is not blocking anything.

## Decided, do not relitigate without reason

- Build from the decomp (approach C). Patching a ROM and DSPRE-only editing are
  both ruled out, for reasons in `phase2-approach-breakdown.md`.
- Hardlove's content comes over; Hardlove's battle AI does not. Platinum's own AI
  is the baseline, updated for the new moves and abilities.
- Ian's earlier base-ROM edits are preserved where practical: overworld events,
  trainers, species stats, move data.
- The base ROM's "Unlocked / Challenge-Adjusted" naming is meaningless history.

## Open, and who owns it

- **What the custom `Dummy088` script command is for** (Ian). The base ROM adds
  one custom script command, called three times in `scripts_common`. It writes a
  single byte. Naming it properly is the last thing blocking a faithful port of
  those three call sites.
- **Evolution triggers for Gyarados M and Lopunny M** (Ian). Slots and stat
  blocks are settled; the trigger is not.
- **Engine-change menu** (Ian). Which of hg-engine's optional features beyond the
  four scoped expansions are wanted; the full list is in
  `phase1-hg-engine-survey.md` section 3.
- **The IV/nature hue-shift patch** (deferred). Present in the base ROM, not
  understood, explicitly droppable. Revisit after Phase 4 if at all.
- ~~**Battle Arcade script commands**~~ Answered 2026-09-20: exactly one custom
  command is called, `Dummy088`, three times, all in `scripts_common`. The rest
  of the code written over that region can be dropped.

## Gotchas worth knowing before touching anything

1. **The base ROM is irreplaceable input.** `Platinum Unlocked - Challenge -
   Adjusted v1.1.nds` in the project folder is the only source for the edits not
   yet carried over. Do not delete or overwrite it until the carry-over is
   finished.
2. **The importers need a vanilla reference too.** `verify_narcs.py` and
   `import_base_rom.py --vanilla` both want a byte-exact vanilla Rev 1 ROM. Keep
   one built from `main` at a stable path rather than rebuilding per session.
3. **Two carried-over edits nobody has sanity-checked**: the base ROM set hatch
   cycles to 1 on 228 species, and filled the empty second ability slot on 228
   species, often by duplicating the first ability. Both are now in the source
   tree exactly as the old ROM had them. If either was a mass-edit accident rather
   than a design choice, now is the cheap moment to undo it.
4. **Do not reformat `res/` JSON files wholesale.** The repo's formatting is not
   uniform; `tools/oxide/jsonstyle.py` edits single keys in place so diffs stay
   readable and upstream merges stay possible.

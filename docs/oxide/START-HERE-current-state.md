# Platinum Oxide: start here

One page, for a fresh chat that needs to be useful without reading everything.
Written 2026-09-15. **Check the date against the repo before trusting the status
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

## State as of 2026-09-15

Done: approach chosen and validated by building a byte-exact retail Platinum ROM
from the decomp; the fork set up and building in WSL2; the base ROM fully diffed
against vanilla; and the first carry-over landed, 415 species files and 108 move
files imported from the base ROM into `res/`, verified by rebuilding and comparing
the resulting NARCs byte-for-byte.

Next, all in Claude Code: importers for encounters, heights, text, items and
trades; the trainer importer plus two new JSON fields for ability and gender; the
map-header weather edits; then the field scripts and events, which are the slow
part. After that Phase 4 begins, in order: Fairy type, ability widening, move
expansion, species slots, battle AI.

## Decided, do not relitigate without reason

- Build from the decomp (approach C). Patching a ROM and DSPRE-only editing are
  both ruled out, for reasons in `phase2-approach-breakdown.md`.
- Hardlove's content comes over; Hardlove's battle AI does not. Platinum's own AI
  is the baseline, updated for the new moves and abilities.
- Ian's earlier base-ROM edits are preserved where practical: overworld events,
  trainers, species stats, move data.
- The base ROM's "Unlocked / Challenge-Adjusted" naming is meaningless history.

## Open, and who owns it

- **Species pick-list** (Ian). Which of Hardlove's extra species come over. Blocks
  the species-slot port, nothing earlier.
- **Engine-change menu** (Ian). Which of hg-engine's optional features beyond the
  four scoped expansions are wanted; the full list is in
  `phase1-hg-engine-survey.md` section 3.
- **The IV/nature hue-shift patch** (deferred). Present in the base ROM, not
  understood, explicitly droppable. Revisit after Phase 4 if at all.
- **Battle Arcade script commands** (evidence pending). Whether any of Ian's 91
  edited field scripts actually call them; decided during the script carry-over.

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

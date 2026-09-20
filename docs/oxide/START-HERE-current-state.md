# Platinum Oxide: start here

One page, for a fresh chat that needs to be useful without reading everything.
Written 2026-09-15, refreshed 2026-09-20. **Check the date against the repo before trusting the status
section**: the live docs are `docs/oxide/design-doc.md` and
`docs/oxide/tracker.md` on branch `oxide` of `iradspinner/pokeplatinum`, and they
move faster than this file.

> **Branch check, first thing.** Encounter-tool work lives on
> `worktree-encounter-tool-plan`, pushed to `origin` but **not merged into
> `oxide`**. If `git log --oneline | grep "Encounter tool"` comes back empty you
> are on `oxide` and `tools/oxide/encounters/` does not exist. Merge or check out
> that branch before starting. Everything else described here is on `oxide`.

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

Done: approach chosen and validated by building a byte-exact retail Platinum ROM
from the decomp; the fork set up and building in WSL2; the base ROM fully diffed
against vanilla; 415 species files and 108 move files imported into `res/` and
verified byte-for-byte; all 928 trainers carried over, including the two new
per-mon `ability` and `gender` fields, verified field-by-field with no
mismatches; all four of the base ROM's synthetic-overlay routines ported as
ordinary C (no items in trainer battles, Rare Candy chaining, uncapped battle
frame rate, EV/IV viewer); and the encounter, trade, map-header, text and
small-constant carry-overs, with heights and the six vitamin item records
deliberately left behind as DSPRE noise.

That leaves **the field scripts and events** as the last Phase 3 item — 184 maps,
surveyed and planned in `phase3-scripts-and-events-plan.md`, with a script
disassembler as the next real piece of work. After that Phase 4 begins, in order:
Fairy type, ability widening, move expansion, species slots, battle AI.

## The encounter tool, running alongside

A separate track from the Phase 3/4 sequence above, and currently the active one.
It is a local tool for designing Oxide's wild encounter tables, built because the
Hardlove encounter rewrite produced tables that were flat, had no early-game feel,
and made repel manipulation pointless. A survey of seven datasets established that
those are the genre norm rather than execution errors, and that vanilla Platinum is
the outlier worth copying.

Three docs, in reading order:

| Doc | What it is |
|---|---|
| `encounter-tool-build-plan.md` | **Start here.** Seven milestones, current status, and a "Resuming cold" section written for exactly this situation |
| `encounter-tool-design.md` | The v1.0 spec: the engine's repel behaviour, the design model, the linter's 14 rules, the generator |
| `encounter-design-survey.md` | The measurements every number in the spec comes from |

**Status: M1 done** (round-trip I/O, 13/13 on both corpora). **M2 is next** — the
analysis engine, whose gate is a Monte-Carlo check of the repel model plus
reproducing the survey's numbers from vanilla.

The one fact that governs all of it: **the working tree holds the base ROM's
encounter tables and `main` holds vanilla**, so every calibration check reads
`--ref main`. The two differ in species on 114 of 171 tables but in levels on only
27, which means vanilla's level ladder — the thing that makes repel manips pay — is
still largely standing in the current tables.

## Decided, do not relitigate without reason

- Build from the decomp (approach C). Patching a ROM and DSPRE-only editing are
  both ruled out, for reasons in `phase2-approach-breakdown.md`.
- Hardlove's content comes over; Hardlove's battle AI does not. Platinum's own AI
  is the baseline, updated for the new moves and abilities.
- Ian's earlier base-ROM edits are preserved where practical: overworld events,
  trainers, species stats, move data.
- The base ROM's "Unlocked / Challenge-Adjusted" naming is meaningless history.

## Open, and who owns it

- ~~**Species pick-list**~~ — landed in the repo as `species-pick-list.md` / `.csv`.
  Still needs a `tier` field per line (`starter-adjacent` / `preferred` / `filler` /
  `gate`) before the encounter tool's availability rule can be enforced.
- **Encounter tool, three open items** (Ian), none of which block M2: the
  progression order for areas, those species tiers, and whether the first authored
  pass covers all 171 tables or a corridor. Detail at the foot of
  `encounter-tool-build-plan.md`.
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
5. **`res/` is not vanilla any more.** After the carry-overs, the working tree holds
   the base ROM's data. Anything that means to compare against retail Platinum must
   read `main` — `git show main:<path>`, or `--ref main` in the encounter tool.
   Calibrating a tool against the checked-out files measures the tables the project
   is trying to replace.

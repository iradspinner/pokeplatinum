# Platinum Oxide: start here

One page, for a fresh chat that needs to be useful without reading everything.
Written 2026-09-15, rewritten 2026-09-20. This file deliberately carries **no
status**: status moves faster than any snapshot, and a stale snapshot is worse
than none. For where things stand, read the top block of `docs/oxide/tracker.md`
on branch `oxide` of `iradspinner/pokeplatinum`; for the encounter tool, the
"Resuming cold" section of `docs/oxide/encounter-tool-build-plan.md`. The G:
folder holds mirrors of both, refreshed by `tools/oxide/sync-docs.sh`, and the
mirror can lag the repo by a session.

## What the project is

Port the engine expansions of Hardlove Gold (a HeartGold hack built on hg-engine)
into Pokemon Platinum: Fairy type, u16 ability IDs, the expanded move table, and a
hand-picked subset of the new species, plus battle-AI updates. The chosen method
is to edit the `pret/pokeplatinum` decompilation directly and build the ROM from
source, not to patch a ROM. Hobby project, no QA gate.

The work runs in phases. Phases 0 to 2 (setup, survey, approach) are done. Phase 3
carried Ian's earlier hand edits from an old DSPRE-edited ROM ("the base ROM") into
the source tree, so nothing of his was lost by switching to a source build. Phase 4
is the actual engine port and is under way, one element at a time. Alongside,
a separate **encounter tool** for designing the wild encounter tables is built,
and the pass that writes the tables from the species pick-list has started.

## The three surfaces and who owns what

| Surface | Owns |
|---|---|
| Claude Code in WSL2, `~/pokeplatinum`, branch `oxide` | All source edits, builds, commits, pushes. `docs/oxide/` in the repo is the live design doc, tracker and notes. |
| A chat in this project (this file's audience) | Design questions, Hardlove donor analysis, base-ROM archaeology, anything that needs a second opinion before it becomes code. Produces notes, not commits. Notes it writes land in the G: folder and are brought into `docs/oxide/` when they matter. |
| The project folder `G:\...\Hardlove Gold-Platinum Oxide Integration Project` | Both ROMs, both DSPRE extractions, and mirror copies of the docs. |

The `claude/platinum-oxide-*.md` docs in this project's knowledge are a snapshot
frozen 2026-09-15. Treat them as background, not current status.

## Reading order in the repo

1. `docs/oxide/design-doc.md`: what the project is, ground truth, scope, working rules, findings log.
2. `docs/oxide/tracker.md`: open work, next steps, what is waiting on Ian. Finished work is in `tracker-archive.md`, read when the tracker points there.
3. Only as the tracker points you there: `phase1-hg-engine-survey.md` (what hg-engine is and its feature menu), `phase2-approach-breakdown.md` (why build from the decomp, and the Phase 4 order), `phase3-base-rom-inventory.md` and `phase3-answers-and-trainer-format.md` (what the base ROM changed and what Ian said to keep), `phase3-scripts-and-events-plan.md` (how the scripts came over), `phase4-engine-change-answers.md` (what Phase 4 ports beyond the four expansions, and why), `species-pick-list.md`, `pokemon-gifts.md`.
4. For the encounter tool: `encounter-tool-build-plan.md` first, then `encounter-tool-design.md` sections 1, 2 and 6, then `encounter-design-survey.md` only for a number's provenance. For the pass that writes the tables: `encounter-authoring-plan.md`.

## Decided, do not relitigate without reason

- Build from the decomp (approach C). Patching a ROM and DSPRE-only editing are
  both ruled out, for reasons in `phase2-approach-breakdown.md`.
- Hardlove's content comes over; Hardlove's battle AI does not. Platinum's own AI
  is the baseline, updated for the new moves and abilities.
- Ian's earlier base-ROM edits are preserved: overworld events, scripts, text,
  trainers, species stats, move data, encounters, map headers. Where the evidence
  said DSPRE rewrote something rather than Ian editing it, it was not carried over
  and the evidence is in `tracker-archive.md`, under Phase 3.
- The base ROM's "Unlocked / Challenge-Adjusted" naming is meaningless history.
- The species pick-list is an availability list, not a deletion list. All 493
  Platinum natives stay in the tree. Internal ids are dense after Arceus, 494 to
  652 (`species-id-scheme.md`), not National Dex numbers.
- The remaining field scripts were generated in bulk from the base ROM's bytecode
  rather than rewritten by hand (Ian, 2026-09-20). They are byte-exact and
  unreadable; re-humanising them is backlog.
- Encounter tool: linter rule R1 is an error for authored tables only and is not
  checked against vanilla; R1b (Spearman >= 0.5) is the vanilla-calibrated form.
  Thresholds are sorted into descriptive (vanilla must pass) and aspirational
  (vanilla is expected to fail). Both accepted by Ian, 2026-09-20.

## Gotchas worth knowing before touching anything

1. **The base ROM is irreplaceable input.** `Platinum Unlocked - Challenge -
   Adjusted v1.1.nds` in the project folder (pinned copy `~/roms/base.nds`) is what
   every verify tool compares against and the only source for re-checking
   anything Phase 3 carried over. Do not delete or overwrite it.
2. **The importers need a vanilla reference too.** `~/roms/vanilla.nds` is a
   byte-exact Rev 1 build from `main`. Don't rebuild it per session.
3. **Do not reformat `res/` JSON files wholesale.** The repo's formatting is not
   uniform; `tools/oxide/jsonstyle.py` edits single keys in place so diffs stay
   readable and upstream merges stay possible.
4. **`res/` is not vanilla any more.** The working tree holds the base ROM's data.
   Anything that means to compare against retail Platinum must read `main`:
   `git show main:<path>`, or `--ref main` in the encounter tool. Calibrating a
   tool against the checked-out files measures the tables the project is trying
   to replace.
5. **86 of the field scripts are machine-generated.** Each says so in its first
   line. They are correct against the base ROM and not the repo's idiom; do not
   take them as examples of how to write a script.
6. **Two sessions in parallel means one status home each.** The tracker is for
   Phases 0 to 5, the build plan for the encounter tool. Editing the other
   track's file is how the merge conflicts happened.
7. **The build machine's CPU is degraded** until its warranty replacement
   arrives (2026-09-22). Builds can crash and pass on a retry, so GitHub builds
   every push to `oxide` and prints the ROM's SHA-1; a ROM is trusted when its
   hash matches that one. A result from the build machine that looks wrong may
   be the hardware, so rerun it before chasing it.

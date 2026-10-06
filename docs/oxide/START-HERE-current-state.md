# Platinum Oxide: start here

One page, for a fresh chat that needs to be useful without reading everything.
Written 2026-09-15, rewritten 2026-09-20. This file deliberately carries **no
status**: status moves faster than any snapshot, and a stale snapshot is worse
than none. For where things stand, read the top block of `docs/oxide/tracker.md`
on branch `oxide` of `iradspinner/pokeplatinum`; for the encounter tool, the
"Resuming cold" section of `docs/oxide/encounter-tool-build-plan.md`; for the
balance track, `docs/oxide/balance-plan.md`. The G:
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
is the actual engine port, one element at a time. Alongside run two tracks of
their own: the **Platinum OxiDex** (OxiDex for short), the encounter tool that
designs the wild encounter tables, and the **balance track**, which analyses and
tunes the whole game's balance.

## The surfaces and who owns what

| Surface | Owns |
|---|---|
| Claude Code in WSL2, `~/pokeplatinum`, branch `oxide` | Source edits, commits, pushes and merges, by several sessions at once, each on its own branch or worktree; the Oxide Overseer merges them. Builds run on GitHub while the CPU is degraded (gotcha 7). `docs/oxide/` in the repo is the live design doc, tracker and notes. |
| Claude Code cloud sessions (claude.ai/code) | Jobs on their own `cloud/<track>-<topic>` branches, built on a healthy VM; they report through the branch and the Overseer merges them (`CLAUDE.md`, "Cloud sessions"). |
| A chat in this project (this file's audience) | Design questions, Hardlove donor analysis, base-ROM archaeology, anything that needs a second opinion before it becomes code. Produces notes, not commits. Notes it writes land in the G: folder and are brought into `docs/oxide/` when they matter. |
| The project folder `G:\...\Hardlove Gold-Platinum Oxide Integration Project` | Both ROMs, both DSPRE extractions, and mirror copies of the docs. |

The `claude/platinum-oxide-*.md` docs in this project's knowledge are a snapshot
frozen 2026-09-15. Treat them as background, not current status.

## Reading order in the repo

1. `docs/oxide/design-doc.md`: what the project is, ground truth, scope, working rules, findings log.
2. `docs/oxide/tracker.md`: open work, next steps, what is waiting on Ian. Finished work is in `tracker-archive.md`, read when the tracker points there.
3. Only as the tracker points you there: `phase1-hg-engine-survey.md` (what hg-engine is and its feature menu), `phase3-base-rom-inventory.md` (what the base ROM changed, with its corrections at the top) and `phase3-answers-and-trainer-format.md` (the base ROM's trainer format), `phase4-engine-change-answers.md` (what Phase 4 ports beyond the four expansions, and why), `species-pick-list.md`, `pokemon-sources.md` (every non-land source of a Pokemon in the tree).
4. For the OxiDex: `encounter-tool-build-plan.md` first, then `encounter-tool-design.md` sections 1, 2 and 6, then `encounter-design-survey.md` only for a number's provenance. For the pass that writes the tables: `encounter-authoring-plan.md`.

## Decided, do not relitigate without reason

Ian's standing rulings, which every session follows, are in
`.claude/rules/standing-rulings.md`; this list keeps the older structural ones.

- Build from the decomp (approach C). Patching a ROM and DSPRE-only editing are
  both ruled out, for reasons in the design doc, section 4.
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

1. **The base ROM is irreplaceable input.** Since 2026-09-26 it is `Platinum Oxide
   base ROM 2026-08-31 (from Example ROM Test.nds).nds` in the project folder
   (pinned copy `~/roms/base.nds`), what every verify tool compares against and
   the only source for re-checking anything carried over. The earlier `Platinum
   Unlocked - Challenge - Adjusted v1.1.nds` stays as the record of 2026-08-11.
   Do not delete or overwrite either.
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
6. **Several sessions in parallel means one status home each.** The tracker is
   for the main track and the Overseer, `encounter-tool-build-plan.md` for the
   OxiDex, `balance-plan.md` for the balance track. Editing another track's file
   is how the merge conflicts happened.
7. **Builds are local.** The replacement CPU passed its checks on 2026-09-29
   and builds the same ROM as GitHub byte for byte. Every push to `oxide` is
   also built on GitHub, for its SHA-1 to compare with; GitHub Actions in the
   private repos are off for good (Ian, 2026-10-01).

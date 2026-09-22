---
name: oxide-session
description: Start-of-session and end-of-session protocol for the Platinum Oxide project (the pokeplatinum fork on branch oxide). Use this at the start of every session in this repo before doing anything else, and again before ending a session or handing work back to Ian, whether or not the user mentions it. Also use it whenever a session is about to commit, push, update the tracker, or record a finding, because it says where each kind of fact lives and which files a track may edit.
---

# Oxide session protocol

This project runs several Claude sessions in parallel on one branch, and the
docs drifted apart badly the first day that happened: a resume hash fifteen
commits stale, three files disagreeing on status, three merge conflicts in one
tracker. The rules below exist so that does not recur. They are short because
the facts they point at live in the docs, not here.

## Starting

1. Read `docs/oxide/design-doc.md` in full, then `docs/oxide/tracker.md`. The
   design doc is facts and rules; the tracker is status. Neither carries a commit
   hash on purpose.
2. Run `git status` and `git log -1`. The tree should be clean and `HEAD` is the
   resume point. If the tree is dirty, another session is mid-work in this
   checkout: do not touch its files and say so.
3. Work out which track you are on and where its status lives:
   - Phases 0 to 5 (the engine port and everything before it): the tracker.
   - The encounter tool and the encounter authoring pass:
     `docs/oxide/encounter-tool-build-plan.md`, plus exactly one paragraph at
     the top of the tracker. Nothing else in the tracker.
4. On a worktree branch, run `git merge oxide` before anything else, resolve
   any conflict in your own files, and run your own suites. A branch cut before
   a change on `oxide` otherwise finds out only at the integration gate: the
   encounter branch's `test_m8` still expected 468 moves when `oxide` had 923.
5. Say in one or two sentences what this session will do, then do it.
6. If the work is more than a small fix, do it on a worktree branch
   (`EnterWorktree` or `git worktree add`) and merge into `oxide` when its tests
   are green. `tools/oxide/integrate.sh` does the merge and verification;
   `/integrate` in the planning session runs it.

## While working

- Never edit `res/` JSON by hand or reformat whole files; use
  `tools/oxide/jsonstyle.py`, the encounter tool, or targeted edits in the file's
  own style. Upstream merges depend on it.
- Never delete, move or overwrite the base ROM (`~/roms/base.nds` and the G:
  original) or the pinned vanilla build (`~/roms/vanilla.nds`). Every verify tool
  compares against them.
- A change to any table the base ROM also has must be declared as intended
  divergence, or the integration gate fails: `DIVERGED` in
  `tools/oxide/verify_narcs.py` for species and moves, `AUTHORED` in
  `tools/oxide/import_base_rom.py` for encounters, `DIVERGED` in
  `tools/oxide/bulk_scripts.py` for scripts.
- A change that moves anything in the save file gets a row in
  `docs/oxide/save-layout.md`. Saves made before it will not read correctly and
  Ian needs to know to start a new game. The trigger is not "did I edit a save
  struct" but "does anything sized by a constant I changed end up in the save":
  the dex flags grow with `NATIONAL_DEX_COUNT`, and Easy Chat word ids (stored
  in mail) shift whenever a text bank of names grows. Both have been missed.
- Do not "improve" something while a faithful carry-over of it is being
  verified. Cleanups are their own commits afterwards.
- Ian's writing rules are in `~/.claude/CLAUDE.md`, which every session and
  subagent loads. A hook refuses a dash or a banned phrase in Markdown and in
  commit messages; the rest is on you.

## Ending

Run these in order; skipping one is how the next session starts confused.

1. **Tracker.** Tick what finished, add what changes what happens next, keep the
   "Where things stand" block true for `HEAD`. Keep entries short and point at
   the file that holds the detail. If you are the encounter track, edit only your
   one paragraph here.
2. **Findings.** A durable fact learned this session (a correction, a defect, a
   measurement, a format detail) goes in the design doc's section 8 findings log,
   dated, and the design doc's version and date at the top are bumped. Status
   does not go there.
3. **Waiting on Ian.** Anything only he can answer or test goes in the tracker's
   "Waiting on Ian" list, and a commit message that says "blocked on Ian" without
   a list entry is a gap.
4. **Mirror.** `bash tools/oxide/sync-docs.sh` if any file under `docs/oxide/`
   changed. It complains about a new file it has no mapping for; add the mapping.
5. **Commit and push** `oxide` (or your worktree branch). Stage files by name,
   never `git add -A` or `git add .`: sessions share this checkout, and a sweep
   commits another session's half-written files under your message (it has
   happened). Commit messages explain why and record what was verified; the
   attribution trailer is in the session's system reminder.
6. **Report** to Ian in a few sentences: what landed, what was verified and how,
   what is waiting on him. Lead with anything that failed.

## Verification, the short list

The full restart check-list is at the top of the tracker, and
`bash tools/oxide/integrate.sh --verify-only` runs all of it without merging
anything. The minimum before calling a data or engine change done is `make rom`
plus the verify tool that covers what changed, and the emulator test written
into the tracker entry for Ian. Until the replacement CPU is in, a local ROM is
trusted when its SHA-1 matches the one GitHub's build prints for the same commit
(CLAUDE.md, Build).

Emulator work is the `debug-live` skill: Ian runs melonDS on Windows and
drives, and the agent attaches over the GDB stub and reads. Never launch your
own emulator.

## Handing a task to a subagent

Ian's standing preference is that bounded tasks (a catalogue, a survey, a tool
with a clear gate, a batch of tables) go to a background general-purpose agent
on Opus, while this session writes the brief, reviews what comes back and
reports to him. Keep here anything that needs judgment across the project,
anything in another track's files, and the report itself, since a subagent's
report never reaches Ian. The agent starts cold, so the brief carries
everything:

```
Repo ~/pokeplatinum, branch <oxide, or the worktree to work in>. Invoke the
<skill> skill first.

Task: <what to produce and why, in a paragraph>.

Already there: <tools, files and earlier results to build on, with paths>.

Rules that bite: stage files by name; never edit res/ JSON by hand (use
jsonstyle.py or the tool that owns the file); never launch an emulator; edit
only <files or directories>; retry a build that crashes (degraded CPU).

Write to: <paths>. <Commit on the worktree branch / leave uncommitted>.

Done means: <the check that must pass, and its command>.

Report: failures and anything unverified first, then what changed with paths,
then what was checked and how. Under <N> words.

<paste the "Hard rules" section of ~/.claude/CLAUDE.md here>
```

Read the result before relaying it: rerun its check, look at the diff, and
say in the report what you did not verify.

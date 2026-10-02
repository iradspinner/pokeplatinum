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
   checkout: do not touch its files and say so. Then run
   `python3 tools/oxide/deferred_check.py` and read the tracker's Scheduled
   list. An entry that is due is checked against today's state before it is
   done: if its "Why:" no longer holds, or its "Unneeded if:" has come true,
   ask Ian instead of acting. A date is not an order; on 2026-10-01 a dated
   note had two workflows switched back on that the new CPU had made
   unnecessary.
3. Work out which track you are on and where its status lives:
   - Phases 0 to 5 (the engine port and everything before it): the tracker.
   - The encounter tool and the encounter authoring pass:
     `docs/oxide/encounter-tool-build-plan.md`, plus exactly one paragraph at
     the top of the tracker. Nothing else in the tracker.
   - The balance track: `docs/oxide/balance-plan.md`, and nothing in the
     tracker.
4. On a worktree branch, run `git merge oxide` before anything else, resolve
   any conflict in your own files, and run your own suites. A branch cut before
   a change on `oxide` otherwise finds out only at the integration gate: the
   encounter branch's `test_m8` still expected 468 moves when `oxide` had 923.
5. Say in one or two sentences what this session will do, then do it.
6. Unless you are the Overseer, do the work on a worktree branch
   (`EnterWorktree` or `git worktree add`) and push that branch when its tests
   are green. The Oxide Overseer lands it on `oxide` with
   `tools/oxide/merge-branch.sh`, which builds the merged tree here and runs
   the gate on that ROM.

## While working

- Never reformat a whole `res/` JSON file. Edit it through
  `tools/oxide/jsonstyle.py`, the tool that owns it (the OxiDex for encounter
  tables), or by hand in the file's own style. Upstream merges depend on it.
- Never delete, move or overwrite a base ROM (the pins in `~/roms/` and the
  originals on G:) or the pinned vanilla build (`~/roms/vanilla.nds`). Every
  verify tool compares against them.
- A change to any table the base ROM also has must be declared as intended
  divergence in the register of the tool that checks it, or the integration
  gate fails. The registers: in `tools/oxide/verify_narcs.py`, `DIVERGED`
  (species and move records) and its siblings `DIVERGED_MEMBERS`,
  `PERSONAL_ABILITIES_DIVERGED`, `MAP_HEADERS_DIVERGED` and `CONTENT_ARCHIVES`;
  in `tools/oxide/import_base_rom.py`, `AUTHORED` (encounters),
  `MOVES_DIVERGED`, `TRAINERS_DIVERGED` (with `trainers_diverged.json`) and
  `TEXT_BANKS_SKIPPED`; and `DIVERGED` in `tools/oxide/bulk_scripts.py` and
  `tools/oxide/bulk_events.py`.
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
- In a session started inside a worktree, edit files with the Edit and Write
  tools and run plain commands; do not feed a script to Python or the shell as
  inline text (a heredoc or `python3 -c`). Claude Code's worktree guard refuses
  any command it cannot prove keeps git inside the worktree, and inline text
  that merely mentions git, or is long enough to be "too complex", trips it.
  The guard stays: it keeps a worktree session's git off the shared main
  checkout, where the Overseer lands every branch (Ian, 2026-10-02).

## Ending

Run these in order; skipping one is how the next session starts confused.

1. **Tracker.** Tick what finished, then move each finished block verbatim to
   `docs/oxide/tracker-archive.md` under the same heading, leaving a one-line
   pointer, so the tracker holds open work only (`integrate.sh` warns past
   6,000 words). A trap still in force goes in a skill or the findings log
   first, because the archive is read only when pointed at. Add what changes
   what happens next, keep the "Where things stand" block true for `HEAD`, and
   keep entries short, pointing at the file that holds the detail. Anything
   to be done on a later day or once something happens goes in the Scheduled
   list with its "Why:" and "Unneeded if:". If this session changed something
   an entry rests on (hardware, a ruling, a dropped feature), update every
   entry, doc and memory resting on it in the same commit. If you are the encounter track, edit only your
   one paragraph here; the balance track edits its plan instead.
2. **Findings.** A durable fact learned this session (a correction, a defect, a
   measurement, a format detail) goes in the design doc's section 8 findings log,
   dated, and the design doc's version and date at the top are bumped. Status
   does not go there.
3. **Waiting on Ian.** Anything only he can answer goes in the tracker's
   "Waiting on Ian" list, and anything only he can test in
   `docs/oxide/ingame-checklist.md`. A commit message that says "blocked on
   Ian" without an entry is a gap.
4. **Mirror.** `bash tools/oxide/sync-docs.sh` if any file under `docs/oxide/`
   changed. It complains about a new file it has no mapping for; add the mapping.
   It runs only on `oxide` and refuses on any other branch, so a track branch
   adds the mapping and leaves the run to `merge-branch.sh`.
5. **Commit and push** your branch (only the Overseer pushes `oxide`). Stage
   files by name, never `git add -A` or `git add .`: sessions share this checkout, and a sweep
   commits another session's half-written files under your message (it has
   happened). Commit messages explain why and record what was verified; the
   attribution trailer is in the session's system reminder.
6. **Report** to Ian in a few sentences: what landed, what was verified and how,
   what is waiting on him. Lead with anything that failed.

## Verification, the short list

The full restart check-list is at the top of the tracker, and
`bash tools/oxide/integrate.sh --verify-only` builds the ROM and runs all of
it without merging anything (`--rom <ROM>` checks a ROM built already). The minimum before calling a data or engine change
done is a built ROM plus the verify tool that covers what changed, and the
emulator test written into `docs/oxide/ingame-checklist.md` for Ian.

Emulator work is the `debug-live` skill: Ian runs melonDS on Windows and
drives, and the agent attaches over the GDB stub and reads. Never launch your
own emulator.

## Handing a task to a subagent

Delegate a task to a background general-purpose agent when it can run in
parallel with other work, or when it is a long read (a catalogue, a survey, a
batch of tables) whose detail this session does not need to hold; Ian has made
that a standing preference. Do the rest inline. Ian's default model is Opus
now, so a subagent no longer saves anything by being cheaper, and it starts
cold. Keep here anything that needs judgment across the project, anything in
another track's files, and the report itself, since a subagent's report never
reaches Ian. The brief has to carry everything:

```
Repo ~/pokeplatinum, branch <oxide, or the worktree to work in>. Invoke the
<skill> skill first.

Task: <what to produce and why, in a paragraph>.

Already there: <tools, files and earlier results to build on, with paths>.

Rules that bite: stage files by name; never reformat a res/ JSON file (edit
through jsonstyle.py, the tool that owns it, or by hand in its style); never
launch an emulator; edit only <files or directories>.

Write to: <paths>. <Commit on the worktree branch / leave uncommitted>.

Done means: <the check that must pass, and its command>.

Report: failures and anything unverified first, then what changed with paths,
then what was checked and how. Under <N> words.

<paste the "Hard rules" section of ~/.claude/CLAUDE.md here>
```

Read the result before relaying it: rerun its check, look at the diff, and
say in the report what you did not verify.

---
name: cloud-job
description: How Platinum Oxide runs a job in a Claude Code cloud session, from both ends. For the Overseer, how to write the short prompt Ian pastes into claude.ai/code and how to review and merge the branch that comes back. For the cloud session itself, the rules of the job, from branch name to the report commit. Use this whenever a session is about to hand work to the cloud, is itself a cloud session (OXIDE_CLOUD=1) starting a job, or has a cloud/* branch to review or merge, even if the user just says "give me the cloud prompt" or "the cloud branch is back".
---

# A cloud job, end to end

Cloud sessions run on healthy four-core VMs, so they take the work this box's
CPU cannot: engine changes that need many builds. They cannot see the base
ROM, the vanilla ROM, the donor ROM or the balance references, and they cannot
message the Overseer. So the job has three parts: a short prompt the Overseer
writes and Ian pastes, the job itself under the rules below, and the
Overseer's review and merge, which runs the checks the cloud skipped.

## 1. The prompt (Overseer)

The prompt stays short because this skill carries the rules:

```
Use the cloud-job skill. Job: <what to do, naming the tracker entry and Ian's
rulings by date, and anything to leave alone>. Branch: cloud/<track>-<topic>,
cut from origin/oxide.
```

Before a job that rewrites game data at scale (learnsets, trainers, tables,
move data), put its outcome to Ian in one plain sentence ("this replaces 389
level-up lists with ...") and wait for a yes; the prompt is written from
that sentence, not from a recorded option. Write into the prompt the
pitfalls its source docs already name: levels past the League cap, a
reference hack's own changes to a move it teaches, dead-weight moves.

Name every exclusion Ian made, since the session cannot ask. Suggest the
model with it: Opus 5.5 at Medium for a data pass or a small engine fix, at
High for anything touching the type chart, turn order, or many abilities at
once. Record the job on the tracker's "Who is on what" board, and start a
watcher for the branch's report commit (a `git ls-remote` loop every five
minutes that stops on a commit subject containing "report").

Two jobs can run at once when they touch different files. Two that both edit
`battle_lib.c` or the effect scripts go one after the other.

## 2. The job (cloud session)

Setup: read CLAUDE.md, `docs/oxide/design-doc.md` and `docs/oxide/tracker.md`;
run `git fetch --depth=1 origin main:main` before the encounter tests; the
first `make rom` fetches the compiler. Build `origin/oxide` once before
changing anything and note its SHA-1: it should match GitHub's build of the
same commit, which shows the VM's toolchain is sound.

Rules that bite:

- Work only on the named `cloud/` branch. Never push to `oxide`.
- One commit per rule, move or fix. Build each and compare it with the
  previous commit's ROM using `tools/oxide/romdiff.py`. romdiff looks for
  relinked branches only when an overlay changes size, so when an overlay
  keeps its size, run its explain step by hand.
- Give each change a test-kit entry where the kit can show it
  (`docs/oxide/test-kit.md`), and build `make testkit` to confirm the
  ordinary ROM did not change. A field menu holds 28 entries; page a menu
  before it grows past that.
- Register every intended difference from the base ROM where the tools keep
  them: `DIVERGED` in `verify_narcs.py` and `bulk_scripts.py`, the lists in
  `import_base_rom.py` (`MOVES_DIVERGED`, `TRAINERS_DIVERGED`, the text-bank
  skips), so the Overseer's base-ROM checks stay green. Say in the report the
  counts those checks should now show.
- New battle state goes in padding bits, never a new field. The field
  condition mask's bits 19 to 25 are taken (Trick Room's permanent bit,
  Neutralizing Gas, Echoed Voice's five); check `condition.h` before
  claiming one.
- A computed power keeps table power 1, never 0: the type chart reads 0 as a
  status move and sets no effectiveness flags.
- A fix to a bug that is also in vanilla Platinum is its own commit with
  "VANILLA FIX" in the subject.
- Before editing another track's files (see `.claude/rules/standing-rulings.md`),
  stop and ask in the report. Ian answers through the Overseer.
- In-game checks go in `docs/oxide/ingame-checklist.md`, in the section
  where a playtest day meets them. Questions go under the tracker's "Waiting
  on Ian". Tick the job's own tracker item. Keep the tracker under 6,000
  words by moving finished blocks to the archive verbatim.

Gate with `bash tools/oxide/integrate.sh --verify-only`. The sync-docs
failure is expected off `oxide`; the base-ROM and balance checks are skipped
by Ian's ruling.

The last commit is the report, and its message says, in this order: failures
and anything unverified first; each commit and what it does; how each was
checked, with ROM hashes; what the Overseer must run (the skipped checks and
their expected counts, sync-docs); what waits on Ian. Nothing has been seen
in game from a cloud session, and the report says so.

## 3. The review and merge (Overseer)

1. Read the report and the diff. Check each claim the merge depends on: the
   bits and padding used, the divergence registrations, anything touched
   outside the job.
2. Run `tools/oxide/merge-branch.sh cloud/<track>-<topic>`. It merges,
   builds the merged tree on GitHub, runs the full gate on that ROM, and
   pushes only on a pass. On a conflict it stops; resolve by hand, commit,
   and rerun with `--merged`.
   - The tracker conflicts most. Keep both sides' current entries, take the
     job's ticks, and trim back under 6,000 words.
   - A design doc conflict takes the higher version line and keeps both
     findings-log entries.
3. Compare the gate's base-ROM counts with the ones the report predicted.
4. After the merge:
   - Relay any VANILLA FIX to Ian on its own, apart from Oxide's own fixes.
   - Tell the encounter track when its calculator should follow the engine.
   - Tell the balance track when scores go stale. A change to move data,
     the player's pool or the calculator needs a rescore before it merges,
     through a balance branch that carries both.
   - Fetch a test-kit ROM if the job added kit entries, and update the
     board.

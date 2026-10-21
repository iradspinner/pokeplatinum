---
description: Review, cull and realign the Platinum Oxide docs, skills and CLAUDE.md against the tree at HEAD
allowed-tools: Bash(git *), Bash(bash tools/oxide/sync-docs.sh), Bash(python3 tools/oxide/*), Read, Edit, Write, Grep, Glob
---

Audit every file under `docs/oxide/`, the skills in `.claude/skills/`, the commands in `.claude/commands/`, the rules in `.claude/rules/` and `CLAUDE.md` against the tree at `HEAD` on `oxide`. The point is that a fresh agent reads only what changes what it does, and reads nothing false.

## 1. Find out who else is working

Run `git worktree list`. For each worktree, check `git -C <path> status --porcelain` and `git rev-list --count oxide..<branch>`. A worktree with uncommitted changes or recent commits belongs to a live session. No session owns files (Ian, 2026-10-13), so what is off limits is what the live branch touches: run `git diff oxide...<branch> --stat` to see which files those are, and keep your edits out of those hunks.

## 2. Classify each file

Each file is one of four kinds:

- **The tracker:** the one home of open work (Ian, 2026-10-13); the old track plans are reference.
- **A live plan:** still being executed.
- **A reference:** something an agent or a tool reads.
- **History:** its lesson already lives in a rule, a skill, a tool or the tracker.

Then act on the classification:

- **History** is deleted, or cut to a one-line pointer.
- **Anything wrong or stale is corrected, not deleted:** a count that drifted, a thing called open that is answered, a path that moved.
- **Anything in two places** is cut to one, and the other points at it.
- **What stays is not restyled.** Rewrite only what is wrong, or what you are cutting to a pointer.

Check claims against the tree rather than against other docs. Run the dry runs, count the files, and grep for the symbol.

Check every deferred instruction. Run `python3 tools/oxide/deferred_check.py -v`. For each Scheduled entry, test its "Why:" against the tree and the latest rulings, and its "Unneeded if:" against what has happened since. An entry whose reason no longer holds goes to Ian; it is not carried out and not silently deleted. Any instruction elsewhere that waits on a day or a condition ("once X lands", "after the TM pass") moves into the Scheduled list with its reason, and the other place points at it.

## 3. The findings log

The design doc's section 8 may lose an entry only when its lesson already lives in a working rule, a skill, a tool or the tracker. If the lesson lives nowhere else, move it into the right skill first, then delete the entry. Several entries telling one story can be merged into one.

Do not touch the last two entries while any track is live. `integrate.sh` resolves a conflict in this section by keeping both sides, so an edit next to a concurrent append would resurrect what you removed.

Add one entry recording the pass, and bump the design doc's version and date.

## 4. Prove it merges

Before committing, run `git merge-tree --write-tree oxide <branch>` against every live branch. It must report no conflict. A tracker conflict would be resolved by taking the `oxide` side, which would silently drop that track's paragraph.

## 5. Commit and report

Run `bash tools/oxide/sync-docs.sh`, and map any new file it complains about. A doc the pass deletes loses its `copy` line too, since the script runs under `set -e` and stops at a line whose file is gone. It runs only on `oxide`; on a branch, add the mapping and leave the run to the merge. The commit message lists, per file:

- What went, and where its lesson now lives.
- What was corrected, and the evidence.
- What was deliberately left, and why.

Then give Ian a short report: what the pass changed, what it could not settle, and which files it left alone because a track was live. Do not integrate as part of this pass. That is `/integrate`, once Ian says the other agents have stopped.

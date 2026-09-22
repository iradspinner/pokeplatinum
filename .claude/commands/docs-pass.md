---
description: Review, cull and realign the Platinum Oxide docs, skills and CLAUDE.md against the tree at HEAD
allowed-tools: Bash(git *), Bash(bash tools/oxide/sync-docs.sh), Bash(python3 tools/oxide/*), Read, Edit, Write, Grep, Glob
---

Audit every file under `docs/oxide/`, the skills in `.claude/skills/`, the commands in `.claude/commands/` and `CLAUDE.md` against the tree at `HEAD` on `oxide`. The point is that a fresh agent reads only what changes what it does, and reads nothing false.

## 1. Find out who else is working

Run `git worktree list`. For each worktree, check `git -C <path> status --porcelain` and `git rev-list --count oxide..<branch>`. A worktree with uncommitted changes or recent commits belongs to a live track. Its files are off limits for this pass: for the encounter track, that means `tools/oxide/encounters/`, `res/field/encounters/`, `docs/oxide/encounters/`, the `encounter-*.md` docs, `pokemon-sources.*`, and its one paragraph at the top of the tracker. Run `git diff oxide...<branch> --stat` to see which shared files the live branch touches, and keep your edits out of those hunks.

## 2. Classify each file

Each file is one of four kinds:

- **A status home:** the tracker, or the encounter build plan.
- **A live plan:** still being executed.
- **A reference:** something an agent or a tool reads.
- **History:** its lesson already lives in a rule, a skill, a tool or a status home.

Then act on the classification:

- **History** is deleted, or cut to a one-line pointer.
- **Anything wrong or stale is corrected, not deleted:** a count that drifted, a thing called open that is answered, a path that moved.
- **Anything in two places** is cut to one, and the other points at it.
- **What stays is not restyled.** Rewrite only what is wrong, or what you are cutting to a pointer.

Check claims against the tree rather than against other docs. Run the dry runs, count the files, and grep for the symbol.

## 3. The findings log

The design doc's section 8 may lose an entry only when its lesson already lives in a working rule, a skill, a tool or a status home. If the lesson lives nowhere else, move it into the right skill first, then delete the entry. Several entries telling one story can be merged into one.

Do not touch the last two entries while any track is live. `integrate.sh` resolves a conflict in this section by keeping both sides, so an edit next to a concurrent append would resurrect what you removed.

Add one entry recording the pass, and bump the design doc's version and date.

## 4. Prove it merges

Before committing, run `git merge-tree --write-tree oxide <branch>` against every live branch. It must report no conflict. A tracker conflict would be resolved by taking the `oxide` side, which would silently drop that track's paragraph.

## 5. Commit and report

Run `bash tools/oxide/sync-docs.sh`, and map any new file it complains about. The commit message lists, per file:

- What went, and where its lesson now lives.
- What was corrected, and the evidence.
- What was deliberately left, and why.

Then give Ian a short report: what the pass changed, what it could not settle, and which files it left alone because a track was live. Do not integrate as part of this pass. That is `/integrate`, once Ian says the other agents have stopped.

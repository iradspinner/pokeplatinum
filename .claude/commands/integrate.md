---
description: Collect every parallel track into oxide, verify the build, and sanity-check the plan docs against what landed
allowed-tools: Bash(tools/oxide/integrate.sh *), Bash(bash tools/oxide/integrate.sh *), Bash(git *), Read, Edit, Write, Grep, Glob
---

Integrate the Platinum Oxide tracks. Run this only when Ian says the other agents are stopped. Everything mechanical is in the script; your job is the reading afterwards.

## 1. Merge and verify

Run `bash tools/oxide/integrate.sh $ARGUMENTS`. Read its summary. If it stopped at a precondition (a dirty worktree, a conflict outside the tracker, a diverged origin), report exactly what it said and stop; those are Ian's calls, not yours.

If a verification check failed, do not push and do not "fix" data files. Report which check failed, its last lines of output, and which merged branch most likely caused it (`git log --oneline` since the previous integration, per file). Then stop.

## 2. Sanity-check the docs against what landed

With the merge green, compare what the status docs say against what git says. Read, in this order: the top block of `docs/oxide/tracker.md`, the "Resuming cold" section of `docs/oxide/encounter-tool-build-plan.md`, and `git log --oneline <previous integration>..HEAD` where the previous integration is the last commit whose subject starts with "Integrate:" (or the last merge commit if there is none).

Check each of these and fix what you find, editing only the file that owns the fact (rule 11 in the design doc):

- The tracker's "Where things stand" block describes the tree at HEAD, not an earlier one, and names no commit hash.
- Every commit since the previous integration is reflected somewhere: a ticked item, a new backlog line, a findings-log entry, or a milestone outcome. A commit with no doc trace is a gap; add the trace.
- The encounter paragraph at the top of the tracker agrees with the build plan on which milestone is done and which is next.
- "Waiting on Ian" lists nothing that git shows as answered, and everything a new commit message says it is blocked on.
- The three files do not contradict each other on any count, status, or path. Paths are repo paths (`docs/oxide/...`), never `notes\`.
- Any commit message that records a new fact worth keeping (a correction, a defect, a measurement) has a findings-log entry in `docs/oxide/design-doc.md` section 8. Bump the design doc's version and date if you add one.
- A new file under `docs/oxide/` is mapped in `tools/oxide/sync-docs.sh` (the script complains if not).

Keep the tracker's encounter footprint to its one paragraph. Do not reformat anything you are not changing.

## 3. Commit and report

If you changed any doc: run `bash tools/oxide/sync-docs.sh`, then commit with a subject starting `Integrate: ` and a body listing what was merged, what the checks said, and each doc fix with the reason, and push `oxide`. If nothing needed changing, say so and do not create an empty commit.

Report to Ian in a few sentences: what merged, whether every check passed, what you corrected in the docs and why, and anything that is now waiting on him. Lead with any failure.

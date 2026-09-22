---
description: QA a range of commits on oxide: review the diff, re-check every claim the commit messages make, run the gate, and write up the findings
argument-hint: <base commit> (the pass covers base..HEAD)
allowed-tools: Bash(bash tools/oxide/integrate.sh *), Bash(git *), Bash(gh *), Bash(make rom), Read, Edit, Write, Grep, Glob
---

Run a QA pass over `$ARGUMENTS..HEAD` on `oxide`. What it produces is a findings file and fixes, not a status report. If no base commit was given, ask Ian for one; do not guess.

## 1. Scope

Run `git log --oneline $ARGUMENTS..HEAD` and `git diff --shortstat $ARGUMENTS..HEAD`. Note any vendored or generated files in the range: they get a provenance and licence check rather than a line-by-line read, and the authored code gets the time.

## 2. Review the diff

Go one commit at a time: read the message, then the code. Correctness first. These are the traps this project has actually fallen into:

- **A claim that a change is inert because the output did not change.** Check that the changed thing was in the path at all. The 2026-09-22 Python pin was "proved inert" by a byte-identical rebuild that never ran the pinned interpreter. A control that passes on both arms proves nothing.
- **`res/` data written by hand** instead of through a tool, or a whole file reformatted.
- **A deliberate divergence from the base ROM that is not registered,** or registered too broadly. The registers are the `DIVERGED` entries in `verify_narcs.py`, `AUTHORED` in `import_base_rom.py`, and the bulk tools' skip lists.
- **A generated file that its generator no longer reproduces.** Rerun the generator and diff the result.
- **A shared table that missed new entries,** such as the exclusion list Metronome, Assist, Sleep Talk and Copycat share. Also look for an enum value or range the engine has no branch for.
- **Tool plumbing.** Summary text on stdout that another tool parses, and fail-open paths that hide a failure.

## 3. Re-check every claim

Commit messages carry numbers: counts, "0 disagree", "byte-identical", "N of N passed". Rerun the command behind each one. If a claim cannot be rerun, say so in the findings rather than repeating it. Until the replacement CPU is in, a failed run gets one rerun before it counts (CLAUDE.md, Build).

## 4. Run the gate

Run `bash tools/oxide/integrate.sh --verify-only`. It builds with retries, checks the ROM's hash against GitHub's build of HEAD, and runs the full check-list without merging anything. A warning that GitHub has no run for HEAD means the range is not pushed yet.

## 5. Write it up

Write `docs/oxide/qa-review-<today>.md` and map it in `tools/oxide/sync-docs.sh`. The file covers:

- What was reviewed: the range, a table of its commits, and anything left out.
- The findings, most serious first. Each gets its evidence (a `file:line`, or the command and its output) and a status: fixed in a named commit, open, Ian's call, or out of scope.

Then put a trace in the tracker, editing only the tracker:

- One line under "Next steps" or "Waiting on Ian" points at the file.
- Each open finding goes under the element it belongs to.
- A finding that corrects a durable fact also gets an entry in the design doc's findings log.

## 6. Fix what is plainly a defect

A defect whose fix is clear gets fixed, as its own commit, with the check that proves it in the message. Leave design choices to Ian, and leave anything in another track's files to that track. Say so in the findings file for each one left.

## 7. Report

Lead with anything that failed or could not be verified. Then give the findings that need Ian's decision, then what was fixed, with the path to the findings file.

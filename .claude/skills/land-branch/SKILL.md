---
name: land-branch
description: The Oxide Overseer's routine for landing a finished branch on `oxide`. Covers the merge pre-check, tools/oxide/merge-branch.sh and what to do when it stops, and the steps after a landing (the OxiDex's ian-saves branch, restarting Ian's server, telling the sessions), plus getting an OxiDex change to Ian early and cutting a branch small enough for a cloud review. Use this whenever a track or cloud branch is ready to land, or an OxiDex change should reach Ian, even if the user only says "land it" or "merge that".
---

# Landing a branch

Tracks never push `oxide`; the Overseer lands every branch. Each landing
merges, has GitHub build the merged tree (about nine minutes), runs the full
gate on that ROM on this machine (about two minutes), and pushes only on a
pass.

## Before

1. Read the branch's report and diff. A cloud branch gets the `cloud-job`
   skill's review first. Check any claim you will repeat to Ian.
2. Pre-check the merge with `git merge-tree --write-tree origin/oxide
   origin/<branch>`, and compare it with a baseline, so you know which
   conflicts the branch brings and which already exist.
3. Several small branches can land as one. Cut a landing branch from
   `origin/oxide`, merge each in, push it, and land it once, for one gate
   instead of several.
4. Tell the sessions when the gate will start, since it reads the main
   checkout and nobody should edit there while it runs.

## Running it

From the main checkout, on `oxide`, with nothing uncommitted:

```
nohup bash tools/oxide/merge-branch.sh <branch> > <scratch>/landing.log 2>&1 &
echo "pid $!"
```

Wait on that pid. Never find it with `pgrep -f` and the branch name: the
pattern matches the watching shell's own command line, and the watcher ends
at once (2026-09-27). While it runs, edit nothing in the main checkout,
because the gate reads that tree and `sync-docs.sh` runs from it; work in a
worktree.

## When it stops

- **A conflict at the merge**: resolve it, commit the merge, and rerun with
  `--merged`. The tracker and the design doc conflict most; keep both sides'
  current entries.
- **A gate failure**: local `oxide` is merged but not pushed. Fix the
  failure on the branch, undo the local merge with `git
  reset --hard origin/oxide` in the main checkout, and land again. On
  2026-09-27 `test_scriptindex` still asserted the Chimchar check that the
  branch had just fixed.
- **A refused command**: never ask another session to do what your own
  permissions refused. Give Ian the exact command or settings line.

## After it lands

1. Merge `origin/oxide` into `ian-saves` in `.claude/worktrees/ian-tool` and
   push. Ian's OxiDex runs from that worktree.
2. If the landing changed the OxiDex server's Python, restart it from a
   checkout that has the script, with exactly
   `bash tools/oxide/encounters/restart_server.sh` (Ian's allow rule matches
   that command). The page's files update on a reload, but the Python
   process does not, and a new page against an old server fails.
3. Tell the sessions the new head and the pass count.
4. Update the tracker's "Who is on what", and move a finished block to the
   archive.

## Shortcuts

- **An OxiDex change can reach Ian before it lands**: merge its branch into
  `ian-saves`, push, and restart the server. Land it on `oxide` later.
- **A cloud ultrareview**, only when Ian asks. `/code-review ultra <PR#>`
  refuses a pull request over its size limit (element 7's 215 files). Cut a
  review branch from the merge base that carries only the code, with `git
  diff <base> <branch> -- src include res/battle/scripts ... | git apply
  --index`, and ask Ian to open the pull request, since this machine's
  GitHub token cannot create one.

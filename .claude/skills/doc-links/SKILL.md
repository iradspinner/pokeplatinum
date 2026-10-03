---
name: doc-links
description: How to point Ian at a document in Platinum Oxide so he can open it rendered in his browser with one click, on his second monitor. Covers the encounter tool's doc viewer (in the tool's own style, any branch), the GitHub fallback, which branch to link, and what to do when the server is down. Use this whenever a reply, a relayed report or a question for Ian names a doc he should read (a report, a plan, the tracker, a proposal, a skill), even if the reply only mentions it in passing.
---

# Linking a document for Ian

Ian reads reports beside the conversation on a second monitor. A bare repo
path makes him go and find the file, so every doc a reply points him at gets a
clickable link that opens it rendered (Ian, 2026-09-27). Code files that a
session edits keep the plain `path:line` form; this skill is for documents he
reads.

## 1. The link, in order of preference

**The encounter tool's doc viewer**, which renders the Markdown in the tool's
own theme:

```
http://localhost:8765/doc/<repo path>
http://localhost:8765/doc/<repo path>?ref=<branch or commit>
```

The first form reads the file in the main checkout (`/home/ian/pokeplatinum`)
as it is on disk, so a doc that exists only on an unmerged branch (a cloud
job's report, a track's branch) needs `?ref=<branch>`; without it the page is
a 404. The viewer reads that version through `git show`, trying
`origin/<branch>` when there is no local branch. Relative links keep the ref,
and a link to a code file opens on GitHub at the same branch.
`http://localhost:8765/doc` lists every doc. It serves only `docs/` and
`.claude/skills/`.

**GitHub**, when the viewer is not running or the reader is not on Ian's
machine:

```
https://github.com/iradspinner/pokeplatinum/blob/<branch>/<repo path>
```

The repo is public and GitHub renders Markdown. The branch must be pushed;
link the branch the doc is on, not `oxide`, until it merges.

## 2. Writing it into a reply

Give the link as Markdown with a short name, and the bare URL after it in
code format only if the terminal might not make it clickable:

```
The per-line report is in [learnset-pass.md](http://localhost:8765/doc/docs/oxide/learnset-pass.md?ref=cloud/balance-learnset-pass).
```

One link per doc, where the reply first names it. A section of a long doc can
be named in words after the link ("its 'Ian's answers' section").

## 3. When the viewer is down

Check with `ss -ltn | grep 8765`. If nothing listens, use the GitHub form and
say in one line that the tool's server is not running; Ian starts it with:

```
PYTHONPATH=. python3 -m tools.oxide.encounters.server
```

The server on 8765 runs from `.claude/worktrees/ian-tool` (branch
`ian-saves`), so after a landing that changes `server.py` it keeps the old
code until it is restarted with `bash tools/oxide/encounters/restart_server.sh`
(the `land-branch` skill, "After it lands").

## 4. Other sessions

A session that reports to Ian directly follows this skill. A session that
reports to the Overseer can name the path; the Overseer turns it into a link
when it relays.

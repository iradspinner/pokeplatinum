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

The first form reads the file in the main checkout as it is on disk. Add
`?ref=` when the doc is on a branch that has not merged, such as a cloud
job's report branch; the viewer reads that version through `git show`, so
the branch only needs to exist locally or on `origin` after a fetch.
`http://localhost:8765/doc` lists every doc.

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

After a landing that changes `server.py`, the running server still has the
old code until it is restarted; the Overseer restarts it.

## 4. Other sessions

A session that reports to Ian directly follows this skill. A session that
reports to the Overseer can name the path; the Overseer turns it into a link
when it relays.

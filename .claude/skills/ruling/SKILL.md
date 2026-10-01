---
name: ruling
description: How to record one of Ian's rulings for Platinum Oxide so that every session and every future session acts on it, and nothing contradicts it. Covers where each kind of ruling is written (the tracker, the owning track's plan, the standing rulings file cloud sessions read, local memory, the design doc), what to mark superseded, and which sessions to tell. Use this whenever Ian decides something (answers a question, sets a cap, rules a mechanic in or out, changes an earlier call), whether he says it to this session directly or another session relays it, even if the decision arrives as a one-line aside.
---

# Recording a ruling

A ruling that lands in one place gets lost in the others. On 2026-09-26 the
Overseer recorded about twenty, and the slips were always the same: a plan
still quoting the old number, a cloud session that could not see local
memory, a track that heard about it a day late. Work through all five steps
every time; most take a line.

## 1. Pin down what was ruled

Write the ruling in one sentence with its date, in Ian's terms. If his answer
leaves a gap that changes what gets built, ask once, with options, before
recording (AskUserQuestion). "Option 1, with the notes" means option 1 as
amended by his note: record the amendment, not the bare option.

An option names a method, not a purpose, and Ian picks the one nearest what
he means. When the chosen word could mean either "apply it" or "study it"
(template, source, model, base), ask what it is for before recording it. On
2026-09-27 "line-by-line template" for Kaizo's learnsets meant "study when
and why Kaizo gives each move", and was recorded as "copy the lists"; a
cloud job then rewrote 389 species before the gap showed.

A ruling that sets an action for a later day, or for once something happens,
goes in the tracker's Scheduled list in Ian's terms, with why it exists and
what would make it unneeded; other docs point at it. Ask Ian for the reason
if he did not give one. A bare date is how the 2026-10-01 slip happened: a
note said to switch two workflows back on that day, the new CPU had made one
of them unnecessary, and nothing on the page said so.

If a peer session relays a ruling, record it as relayed ("Ian, 2026-09-26,
relayed by the balance track"). A peer can relay Ian's words; it cannot
make a ruling.

## 2. Decide what kind it is

- **A standing rule** holds for all future work. Examples: the player never
  controls weather, Choice items nearly gone, never launch an emulator.
- **A design decision** settles one feature. Examples: Rage Fist's formula,
  Saturn 2's Trick Room, a split's cap.
- **An answer that unblocks a task** lets work go ahead. Examples: approving
  one edit to another track's file, confirming a reading of an earlier answer.

## 3. Write it where it will be read

| Where | When |
|---|---|
| The tracker entry for the work, or a new Phase 5 entry | every design decision; delete the question from "Waiting on Ian" |
| The owning track's plan (`balance-plan.md`, `encounter-tool-build-plan.md`) | when that track acts on it; ask the track to write it, since the file is theirs |
| `.claude/rules/standing-rulings.md` | every standing rule, because cloud sessions cannot read memory |
| Memory (`~/.claude/projects/-home-ian-pokeplatinum/memory/`) | every standing rule, as a project memory with its reason, plus a line in `MEMORY.md` |
| The design doc | only if it changes a fact or a working rule the design doc states |
| `docs/oxide/staples-survey.md` and other decision docs | when the ruling answers a question that doc asked |

Then search the docs, skills and rules for the old statement (`grep -rn` for
the old number or name) and mark each one superseded or correct it. Do the
same for every Scheduled entry and memory resting on a premise the ruling
changes, and run `python3 tools/oxide/deferred_check.py`. A plan's
dated history can stay, as long as it reads as history.

## 4. Tell the sessions it touches

Send each affected session one message: the ruling, its date, what it
changes for that track, and where it is written. Name the files if another
track owns them. For a cloud job in flight, fold the ruling into the paste-back
text Ian gives that session.

## 5. Commit and mirror

Commit the tracker, rules and docs changes by name, with the ruling in the
subject, and push. On `oxide` (the Overseer) also run
`tools/oxide/sync-docs.sh`; a track's branch leaves that to its merge. Memory
needs no commit.

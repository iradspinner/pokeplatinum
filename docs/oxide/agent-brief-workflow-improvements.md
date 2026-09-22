# Brief: workflow improvements, the agent side

Written 2026-09-22 by the Overseer session for a fresh agent started in
`~/pokeplatinum`. Ian reviewed the project's workflow and asked for the agent
side of it to be done. This file is a live plan: when every item is done or
ruled out, cut it to a one-line pointer in the tracker and delete it.

## Where it stands

Items 2 to 7 were done on 2026-09-22; each commit carries its check. What is
left is item 1, below, and two lines for Ian's user settings.

| Item | State |
|---|---|
| 1. Cut the tracker to open work | **Open.** Waits for Ian's word that no other session is working in the main checkout (his call, 2026-09-22) |
| 2. One memory folder | Done: the five memories and one index are in `~/.claude/projects/-home-ian-pokeplatinum/memory/`, and the old index points there. **The `autoMemoryDirectory` line is Ian's to add**: auto mode refused the session's edit to `~/.claude/settings.json` |
| 3. Safer integration | Done in `e08c178b3`: per-block tracker resolution in `integrate.sh`, `git merge oxide` as a starting step, `/qa-pass` before a track merges |
| 4. The wedge guard | Done in `2412133bf`: the rule in `.claude/hooks/oxide_guard.py`, its test, and `wedge_status.sh`. **The `statusLine` entry is Ian's to add**, for the same reason as item 2 |
| 5. Docs-only commits | Done in `95919ed6b`: `ci_hash` and `fetch-rom` use the newest ancestor that differs only in Markdown |
| 6. The test kit | Proposed in `docs/oxide/test-kit-proposal.md`, waiting on Ian |
| 7. The delegation memory | Done, in the new memory folder, and the `oxide-session` skill's paragraph matches it (`e1876ede9`) |

The two settings lines, in `~/.claude/settings.json` beside `"model"`:

```json
"autoMemoryDirectory": "~/.claude/projects/-home-ian-pokeplatinum/memory",
"statusLine": { "type": "command", "command": "sh /home/ian/pokeplatinum/.claude/hooks/wedge_status.sh" },
```

## Before you start item 1

Invoke the `oxide-session` skill, then read this whole file. Work on `oxide` in
the main checkout, and only once Ian has said no other session is working
there: a main-track session edits the tracker too, and two sessions
restructuring one file in one folder lose work. Check `git status` anyway.

`git worktree list` shows the encounter agent on `worktree-encounter-step0`.
Its files are off limits: `tools/oxide/encounters/`, `res/field/encounters/`,
`docs/oxide/encounters/`, the `encounter-*.md` docs, and its one paragraph at
the top of the tracker. Before committing any tracker or design-doc change,
run `git merge-tree --write-tree oxide worktree-encounter-step0`, which must
come back clean.

## 1. Cut the tracker down to open work

Every main-track session reads the design doc and the tracker in full before
doing anything. Measured on 2026-09-22:

| File | Words | Note |
|---|---|---|
| `docs/oxide/tracker.md` | 14,734 | the read tool reported 36,617 tokens against a 25,000 single-read limit, so agents read it in pages |
| of which, ticked items with their sub-bullets | 7,303 | finished work |
| of which, the encounter paragraph | 1,745 | a changelog, and where tracker merge conflicts start |
| `docs/oxide/design-doc.md` | 6,029 | read in full at every start |

What to do:

- Create `docs/oxide/tracker-archive.md` and move every finished item there
  verbatim, grouped under the same phase and element headings, with a
  two-line header saying what it is. The tracker keeps a one-line pointer where
  each archived block was. One example: "Elements 1 and 2 are done; their
  write-ups are in `tracker-archive.md`."
- The tracker keeps these sections:
  - the header and "Where things live"
  - "Where things stand"
  - the encounter paragraph, untouched
  - Next steps and "Waiting on Ian"
  - the restart check-list and "What clean looks like"
  - every open item, with enough context to act on it
  - the backlog
- **Before archiving an item that holds a trap or rule still in force**, make
  sure the lesson lives in a skill or the design doc. Examples are element 4's
  Easy Chat note and the "deliberately left short" lists. Otherwise the next
  agent loses it, because agents read the archive only when pointed there.
- Target: the tracker under 5,000 words.
- Add a check to `tools/oxide/integrate.sh` that warns (WARN, not FAIL) when
  `tracker.md` passes 6,000 words, so it cannot quietly grow back.
- Update every pointer to moved content: `CLAUDE.md`, `START-HERE-current-state.md`,
  the skills (`grep -rn "tracker" .claude/skills`), and design doc rule 11 if its
  wording changes. Map the new file in `tools/oxide/sync-docs.sh`, next to the
  other `notes/` lines and away from the encounter track's mapping.
- **The encounter paragraph and the encounter build plan are that track's.**
  Do not edit either. Ian decided on 2026-09-22 that the encounter agent cuts
  its own paragraph to a few sentences and gives its build plan the same
  archive split; its brief is `docs/oxide/agent-brief-encounter-docs-split.md`.

Done means: the tracker is under 5,000 words, nothing open went missing (diff
the open `- [ ]` items before and after), `integrate.sh --verify-only` is green
with the new warning in place, and the merge-tree check is clean. The gate
refuses a dirty checkout, so if another session has files modified in the main
checkout, run it in a clone on a local `oxide` branch; the clone needs a local
`main` branch too, which the encounter tools compare against.

## Report

Lead with anything that failed or could not be verified. Then what changed,
with paths, and how it was checked. Keep it under 300 words.

## Ian's writing rules (from `~/.claude/CLAUDE.md`, Hard rules)

Quoted verbatim, in a block because they name the phrases they ban:

```text
- No em-dashes or en-dashes as punctuation. Use a comma, a full stop, a colon,
  or parentheses. This applies inside code comments and commit messages too.
- No opening praise or acknowledgement ("Great question", "Good catch",
  "You're right to ask"). Start with the answer.
- No closing offers or sign-offs ("Let me know if", "Hope this helps",
  "Happy to", "Feel free to"). Stop when the content stops.
- Prose over bullets. A list is for genuinely parallel items (files, steps,
  options, findings). Argument, explanation and narrative are paragraphs.
- No bold-label bullets that are really paragraphs in disguise, and no headers
  in anything under about five hundred words.
- Do not assume Ian is the expert on a question he asked. Answer it.
- Annotate code in plain English: what it does and why, not what the syntax is.
```

# Brief: workflow improvements, the agent side

Written 2026-09-22 by the Overseer session for a fresh agent started in
`~/pokeplatinum`. Ian reviewed the project's workflow and asked for the agent
side of it to be done. This file is a live plan: when every item is done or
ruled out, cut it to a one-line pointer in the tracker and delete it.

## Before you start

Invoke the `oxide-session` skill, then read this whole file. Work on `oxide` in
the main checkout. Commit each item on its own, with the check that proves it
in the message, and push when the gate is green.

**Other sessions are live.** Check both of these before touching a file:

- `git status` in the main checkout. On 2026-09-22 a main-track session had
  `tools/oxide/convert_battle_scripts.py` modified there, which means element 4
  work in this same folder. Do not touch its files. Do not restructure the
  tracker while it is working either, because both of you would be editing
  the same file in the same folder.
- `git worktree list`. The encounter agent works on `worktree-encounter-step0`.
  Its files are off limits: `tools/oxide/encounters/`, `res/field/encounters/`,
  `docs/oxide/encounters/`, the `encounter-*.md` docs, and its one paragraph at
  the top of the tracker. Before committing any tracker or design-doc change,
  run `git merge-tree --write-tree oxide worktree-encounter-step0`, which must
  come back clean.

Order: items 2, 3, 4, 5 and 7 first, since none of them touches the tracker's
body. Then item 1, once Ian confirms no other session is working in the main
checkout. Item 6 starts as a proposal to Ian, not as code.

## 1. Cut the tracker down to open work

Every main-track session reads the design doc and the tracker in full before
doing anything. Measured on 2026-09-22:

| File | Words | Note |
|---|---|---|
| `docs/oxide/tracker.md` | 14,734 | the read tool reported 36,617 tokens against a 25,000 single-read limit, so agents read it in pages |
| of which, ticked items with their sub-bullets | 7,303 | finished work |
| of which, the encounter paragraph | 1,745 | a changelog, and where tracker merge conflicts start |
| `docs/oxide/design-doc.md` | 6,029 | read in full at every start |
| `docs/oxide/encounter-tool-build-plan.md` | 16,758 | the encounter track's start read, over the limit too |

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
  Do not edit either. Ask Ian whether to have the encounter agent cut its
  paragraph to a few sentences (its detail is in the build plan) and give its
  build plan the same archive split.

Done means: the tracker is under 5,000 words, nothing open went missing (diff
the open `- [ ]` items before and after), `integrate.sh --verify-only` is green
with the new warning in place, and the merge-tree check is clean.

## 2. One memory folder for every session

Auto-memory is stored per launch folder, so what a session remembers depends
on where Ian started it:

| Folder | Holds |
|---|---|
| `~/.claude/projects/-home-ian/memory/` | cloud-review-opt-in, emulator-piggyback-only, encounter-table-preferences, opus-subagents-for-tasks |
| `~/.claude/projects/-home-ian-pokeplatinum/memory/` | windows-interop |
| `~/.claude/projects/-home-ian-pokeplatinum--claude-worktrees-*/` | nothing: worktree sessions start with no memory |

Set `autoMemoryDirectory` in Ian's user settings (`~/.claude/settings.json`;
the key is ignored in project settings) to
`~/.claude/projects/-home-ian-pokeplatinum/memory`. Copy the four files into it
and merge both `MEMORY.md` indexes into one. Merge into the existing hooks and
settings, and read the file before writing it. Leave the old
`-home-ian/memory/MEMORY.md` with a single line pointing at the new folder,
rather than deleting it. The setting applies to every project on the machine;
Ian uses Claude Code for Oxide, and handing this brief over is his approval.

Done means: the settings file is valid JSON (parse it), all five memories and
one index are in the new folder, and the report tells Ian that the change takes
effect from the next session.

## 3. Safer integration

Three changes, each from something that went wrong on 2026-09-22.

**The tracker conflict rule.** `tools/oxide/integrate.sh` resolves any conflict
in `docs/oxide/tracker.md` with `git checkout --ours` (around line 172), which
keeps `oxide`'s whole file. On 2026-09-22 that would have silently dropped the
encounter track's update to its own paragraph; it was caught by hand with
`git merge-tree` before the merge. Resolve per conflict block instead:

- A block whose sides are both the encounter paragraph (lines starting
  `**Second track: the encounter tool.**`) takes the track's side.
- Any other conflicting block aborts the merge and stops with the block
  printed, because a silent loss is worse than a stop.

Test it in a throwaway clone, with a branch pair built to conflict in each
way; never test it on `oxide`.

**Track branches merge `oxide` as they start.** The encounter branch was cut
before element 4's move import, so its `test_m8` hard-coded 468 moves and
failed only at the gate, against a tree with 923. Add a step to the "Starting"
section of `.claude/skills/oxide-session/SKILL.md`. On a worktree branch, run
`git merge oxide` first, resolve conflicts in your own files, and run your own
suites, so drift fails on the branch.

**`/qa-pass` before a track merges.** Add a step to `.claude/commands/integrate.md`
before the script runs. For each track branch about to merge, run
`/qa-pass <merge-base>` on it unless Ian says to skip. It found two real dex
bugs on 2026-09-22 (`docs/oxide/qa-review-2026-09-22-encounter-m8.md`). Do not
add the cloud review to it or to any other procedure; Ian includes that
explicitly when he wants it.

## 4. A guard for the kernel wedge

Until the replacement CPU is in, a process can wedge in state D on
`__vma_start_write`. Anything that reads that process's details then blocks for
good, including `ps`, `pgrep`, `pkill`, `top`, `pidof`, and reads of
`/proc/<pid>/cmdline`, `status` or `stat`. The only cure is Ian running
`wsl --shutdown`. Two reads stay safe, `/proc/<pid>/comm` and `/proc/<pid>/wchan`,
and `readlink /proc/<pid>/cwd` is safe too. `integrate.sh` already uses them to
find Claude sessions. A previous session lost two shells to a blocked `ps`.

- In `.claude/hooks/oxide_guard.py`, refuse a Bash command whose first word
  (after wrappers) is `ps`, `pgrep`, `pkill`, `top`, `htop` or `pidof` while a
  wedge is live. Say which pid and command are wedged, and give the safe scan
  (`for d in /proc/[0-9]*; do cat $d/comm; done`). Scan only when the command
  matches, so ordinary commands pay nothing. Detect with a scan of
  `/proc/[0-9]*/wchan` for `__vma_start_write`. Give the scan a root-directory
  parameter, so a test can point it at a fake `/proc` tree.
- Add a status line in Ian's user settings that shows the wedged pid while one
  is live and nothing otherwise, so he knows when to run `wsl --shutdown`. None
  is configured today. Keep the script cheap, because it runs often.
- Add a line to the tracker's platform entry under "Waiting on Ian": remove
  the guard and the status line when the new chip is in. Take care, since
  that is a tracker edit; see the ordering note at the top.

Done means: the hook refuses `ps aux` against a fake wedged `/proc`, allows it
against a clean one, and allows `ls` either way. The status line prints nothing
on a clean machine.

## 5. Commits that change only Markdown

`.github/workflows/oxide-rom.yml` skips pushes that change only `**.md`. So a
docs-only commit never gets a hash. The gate's `ci_hash()` in `integrate.sh`
looks up a run for exactly `HEAD`, so after a docs commit it always warns.
`tools/oxide/fetch-rom` builds exactly the commit asked for, so it spends a
five-minute private build on a ROM identical to its parent's.

Fix both with one rule: use the newest ancestor `C` for which
`git diff --quiet C HEAD -- . ':(exclude)*.md'` holds and a successful run
exists. Keep the exclusion to `*.md`, matching the workflow's filter exactly,
because the build reads the rest of `tools/`. `fetch-rom` should say which
commit's build it reused.

Done means: after a docs-only commit, `integrate.sh --verify-only` compares
against the parent's hash rather than warning, and `fetch-rom` reuses the
parent's artifact while it is still retained.

## 6. A test kit for in-game checks (propose first)

The 116 battle effect scripts left in element 4 each need seeing in battle,
and "Waiting on Ian" already holds about ten emulator checks. Every one costs
Ian a play-through to reach. A debug-only build option would cut that to
minutes. Write a short proposal and ask Ian before building anything. It
should cover:

- The switch, for example a `make rom` variable that becomes a meson option.
  It must default off, and the playtest builds (GitHub's workflow and
  `fetch-rom`'s private builder) must never set it, so the ROM of record and
  its hash are unchanged.
- An NPC in the player's house that hands out what the waiting checks need:
  - Rare Candies
  - a Rotom, and Giratina with the Griseous Orb (the form fix)
  - an Eevee (Sylveon via Charm)
  - a Pokemon about to learn a move (the widened learnset)
  - a list-menu warp to the check locations
- Trainers whose teams use the new moves, grouped by effect, for the battle
  scripts as they land.
- Which script commands it would use (`GivePokemon`, `GiveDesignedPokemon`,
  item commands and warps already exist), and where its script and text live.

## 7. Update the delegation memory

`opus-subagents-for-tasks.md` says the main session (Fable) writes briefs and
reviews, while background Opus agents do bounded work to save Fable tokens.
Ian's default model is now Opus, so the cost reason is gone. Rewrite it: the
case for a subagent is now parallel work and keeping a long read out of the
main context, so delegate those tasks and keep the rest inline. Keep the brief
template pointer and the rule that the main session relays results to Ian.
Do this after item 2, in the new memory folder.

## Not in scope

Automated in-game tests with a scripted, windowless emulator would cover much of
the battle-effect testing. They conflict with Ian's rule that agents never run
an emulator, so they wait for his ruling. Do not start them.

## Report

Lead with anything that failed or could not be verified. Then, per item: what
changed, with paths, and how it was checked. Then what is waiting on Ian: at
least item 6's proposal, the encounter-track question from item 1, and item 1
itself if the main checkout was never free. Keep it under 400 words.

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

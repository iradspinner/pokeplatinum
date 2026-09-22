# Brief: cut the encounter track's docs down to open work

Written 2026-09-22 by the Overseer for the encounter agent, on Ian's
instruction. It is the encounter half of item 1 in
`docs/oxide/agent-brief-workflow-improvements.md`, which cuts the main
tracker; this half is yours because the files are. Delete this file, and its
line in `tools/oxide/sync-docs.sh`, in the commit that finishes it.

Every session reads its status home in full before it starts. Your build plan
is 18,159 words on `worktree-encounter-step0`, over the 25,000-token
single-read limit, so agents read it in pages. Your paragraph at the top of
`docs/oxide/tracker.md` is 1,745 words, a changelog in all but name, and it is
where tracker merge conflicts start.

Work on `worktree-encounter-step0`. Run `git merge oxide` first (the new
starting step in the `oxide-session` skill) and your suites after it.

1. Create `docs/oxide/encounter-tool-build-plan-archive.md` with a two-line
   header saying what it is, and move every finished milestone and step into
   it verbatim, under the same headings. The build plan keeps "Resuming cold",
   "The short version", whatever is still open, and a one-line pointer where
   each archived block was.
2. Before archiving a block that holds a rule or trap still in force, make
   sure the lesson lives in the `author-table` skill or in the plan's own
   standing sections. Agents read the archive only when pointed there.
3. Cut your tracker paragraph to a few sentences: what the tool is, the one
   or two things that are live now, and a pointer to the build plan. Keep its
   opening words, `**Second track: the encounter tool.**`, because
   `integrate.sh` recognises the paragraph by them and takes your side of it
   when the two tracks' versions conflict.
4. Map the archive in `tools/oxide/sync-docs.sh`, in your own block of
   `Claude outputs/` lines.

Rules that bite: stage files by name; edit only your own files and your one
tracker paragraph; never launch an emulator.

Done means: the build plan is under 8,000 words, no open item went missing
(diff the plan's open items before and after), your suites pass, and
`git merge-tree --write-tree oxide worktree-encounter-step0` is clean.

Report: failures first, then the new word counts and what moved where.
Under 250 words.

Ian's writing rules, the Hard rules from `~/.claude/CLAUDE.md`:

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

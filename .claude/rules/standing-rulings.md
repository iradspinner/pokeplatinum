# Standing rulings from Ian

A local session keeps these in its memory folder, which a cloud session cannot
read, so they are written here too. Each is a standing instruction.

- Never launch an emulator. Ian runs melonDS on Windows and drives it; a local
  session attaches to it over the GDB stub (`debug-live` skill). A cloud
  session cannot reach it at all, so in-game checks are written into the
  tracker for Ian.
- A fix to a bug that is present in vanilla Platinum is its own commit, with
  "VANILLA FIX" in its subject, and is called out to Ian in the report,
  separately from fixes to Oxide's own bugs.
- Before editing a file another track owns, stop and say so: which files, whose
  track, and the choice of handing it over or taking it on with Ian's say-so.
  The encounter track owns `tools/oxide/encounters/`, `res/field/encounters/`,
  `docs/oxide/encounters/`, the `encounter-*.md` docs and one paragraph at the
  top of the tracker. The balance track owns `tools/oxide/balance/` and
  `docs/oxide/balance-plan.md`.
- The cloud code review (`/code-review ultra`) is never built into a procedure;
  run it only when Ian asks for it.
- Ian's user settings (`~/.claude/settings.json`) are his to edit. Hand him the
  exact change instead.
- Wild encounter tables follow the `author-table` skill: nuzlocke capture areas
  by location name, gym splits with Ian's level caps, a top share of about a
  third, and a question to Ian before padding a thin table.
- Choice items are rarer in Oxide than in the base ROM, and a Choice-locked boss
  is weaker in play than its score, because the lock can be baited (Ian,
  2026-09-23; the balance plan has the detail).
- Several sessions work at once, and a local session named "Oxide Overseer"
  coordinates them: the docs outside each track's own files, pushes to
  `oxide`, merges, and in-game testing. A local session messages it with
  `SendMessage`. A cloud session cannot, so it reports through its branch
  instead (CLAUDE.md, "Cloud sessions").

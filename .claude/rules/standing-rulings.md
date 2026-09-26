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
  third, and a question to Ian before padding a thin table. Swarm, Poke Radar
  and GBA dual-slot encounters are turned off and never go in a table (Ian,
  2026-09-26).
- Choice items are to be nearly entirely gone from Oxide (Ian, 2026-09-26,
  strengthening "rarer than in the base ROM" of 2026-09-23). A Choice-locked
  boss is weaker in play than its score: its AI picks a fixed move against a
  given lead, so the player chooses the lock and switches to something immune.
  The balance plan's item and trainer passes carry it.
- Several sessions work at once, and a local session named "Oxide Overseer"
  coordinates them: the docs outside each track's own files, pushes to
  `oxide`, merges, and in-game testing. A local session messages it with
  `SendMessage`. A cloud session cannot, so it reports through its branch
  instead (CLAUDE.md, "Cloud sessions").
- The player has no way to set, change or end weather for the whole game (Ian,
  2026-09-26): no weather move in any player learnset, TM, tutor or egg list,
  and no weather-setting or weather-cancelling ability in an obtainable
  Pokemon's regular slots. The exceptions are the game's single Ability Patch
  (exactly one exists), which may give a weather ability as a hidden ability,
  and Defog, which still clears fog. Trainers keep their weather.
- Ian's super-wanted lines (the `wanted` list in
  `docs/oxide/encounters/values.json`) are never trimmed from the encounter
  tables, and a majority of them should be obtainable in a best-play run.

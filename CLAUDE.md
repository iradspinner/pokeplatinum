# Platinum Oxide

This fork of pret/pokeplatinum is the source of truth for the Platinum Oxide
project: porting the engine expansions of Hardlove Gold (an hg-engine
HeartGold hack) into Pokemon Platinum by editing this decomp directly.

Start every session by reading, in order:

1. `docs/oxide/design-doc.md`   what the project is, ground truth, scope, working rules
2. `docs/oxide/tracker.md`      what is done, what is next, decisions made
3. The `docs/oxide/phase*.md` notes only as the tracker points you to them

Then say in one or two sentences what this session will do, and do it.

## Working rules (short form; the design doc has the full list)

- Work on branch `oxide`. Never commit to `main`; `main` tracks upstream pret.
- Every data change is verified by rebuilding (`make rom`) and, where a
  reference exists, comparing the rebuilt NARC to it with
  `tools/oxide/verify_narcs.py`.
- Edit `res/` JSON files with `tools/oxide/jsonstyle.py` helpers or by hand in
  the same style; never reformat whole files (the repo's formatting is not
  uniform and reformatting makes upstream merges painful).
- Ian's writing rules are in `~/.claude/CLAUDE.md`, which every session and
  subagent loads, and a hook refuses a dash or a banned phrase in Markdown and
  commit messages. Paste its "Hard rules" into any subagent brief (the brief
  template is in the `oxide-session` skill).
- Ask before doing anything expensive to redo or hard to reverse.
- Update `docs/oxide/tracker.md` at the end of every session and commit it.
  If any `docs/oxide/*.md` file changed this session, also run
  `tools/oxide/sync-docs.sh` to mirror it to the project folder on the G:
  drive, which a separate chat surface works from.
- Never delete, move, or overwrite the base ROM in the project folder
  (`Platinum Unlocked - Challenge - Adjusted v1.1.nds`). It is what every
  verify tool compares the build against, and the only source for anything
  Phase 3 might need re-checking.
- A few files deliberately no longer match the base ROM, `scripts_common`
  first among them. The `bulk_*` tools keep their own list of these and skip
  them; do not "fix" a mismatch the tracker says is intended.
- Stage files by name when committing, never `git add -A` or `git add .`;
  sessions share this checkout and a sweep commits another session's
  in-progress files under your message.
- Two sessions may run in parallel. Each edits only its own status home: the
  tracker for Phases 0 to 5, `docs/oxide/encounter-tool-build-plan.md` for the
  encounter tool (plus its one paragraph at the top of the tracker). A second
  track works on its own branch or worktree and merges into `oxide` when its
  tests are green.
- Do not "improve" a carried-over map, script or table while a faithful
  carry-over is being verified; `checkmap.py` compares against the base ROM.
  Cleanups (re-humanising generated scripts, unifying the clown gifts) are
  backlog items done afterwards, as their own commits.

## Skills

Project skills in `.claude/skills/` hold the procedures; the docs hold the
facts. Use them by name: `oxide-session` (start and end of every session),
`port-element` (any Phase 4 engine element), `author-table` (any encounter
table work), `carry-over-map` (scripts, events and text for one map),
`read-donor` (anything from the Hardlove ROM), `oxide-spreadsheets` (Ian's
design sheets on G:, with the synced `xlsx` skill for the mechanics),
`debug-live` (any in-game bug, with Ian driving melonDS). In
`.claude/commands/`, `/integrate` merges every track into `oxide` and runs the
full verification gate, `/qa-pass <base>` reviews and re-checks a range of
commits and writes up the findings, and `/docs-pass` audits the docs, skills and
this file against the tree.

A hook in `.claude/settings.json` refuses `git add -A` or `.`, launching an
emulator, and committing a file that carries the scratch marker
(`.claude/hooks/oxide_guard.py`); a refusal from it means the rule above it in
this file applies. `.githooks/pre-commit` runs the encounter linter on any
commit that touches the encounter tables or tool; a clone enables it once with
`git config core.hooksPath .githooks`.

## Build

See `docs/oxide/setup-fork-and-wsl2.md`. `make` for a checked build of the
unmodified tree; `make rom` for an unchecked rebuild after edits. Output:
`build/pokeplatinum.us.nds`.

**This box's CPU is faulty until its warranty replacement arrives.** The
i9-14900K is degraded: capped, single-threaded work is clean, but under
all-core load compilers and Python crash or return wrong answers (design doc
findings log, 2026-09-22). So a result here is trusted only after a second run
agrees with it. GitHub builds every push to `oxide` on its own machines
(`.github/workflows/oxide-rom.yml`) and prints the ROM's SHA-1 in the run's
summary; a local ROM is trusted when its hash matches that one. This public
repo never uploads the ROM. **Ian's playtest ROMs come from
`tools/oxide/fetch-rom`**, which builds a pushed commit in the private repo
`iradspinner/oxide-rom-builder`, keeps the ROM there as a private artifact for
three days, and downloads it to `~/oxide-playtest` after checking its SHA-1.
Hand Ian that ROM, not one built on this CPU. Retry a local build that crashes,
and rerun a failed test before believing it. The `Makefile` puts the 3.13
venv first on PATH because this chip crashes it far less than the system
Python; that block goes when the new CPU is in.
`tools/oxide/python_flake_repro.py` is the check.

## Tools

`tools/oxide/import_base_rom.py` carries edits from Ian's earlier DSPRE-edited
ROM ("the base ROM") into `res/`. `tools/oxide/verify_narcs.py` proves a
rebuild reproduces a reference ROM's tables. `scriptdis.py` disassembles and
round-trips field scripts; `bulk_scripts.py`, `bulk_events.py` and
`bulk_text.py` regenerate whatever the build still gets wrong against the base
ROM (their `--dry-run` doubles as the check); `mapdiff.py` and `checkmap.py`
work one map at a time. `tools/oxide/encounters/` is the encounter tool, with
its own tests and CLI (see its build plan). `tools/oxide/live_watch.py` attaches
to Ian's melonDS on Windows over its GDB stub while Ian drives the game; never
launch your own emulator (`docs/oxide/setup-fork-and-wsl2.md` part 5b, and the
`debug-live` skill). The base ROM itself lives outside the repo (see the design
doc for its path on Ian's machine); a copy is pinned at `~/roms/base.nds`. A
byte-exact vanilla Rev 1 build (built once from `main`) is pinned at
`~/roms/vanilla.nds` for `import_base_rom.py --vanilla` and
`verify_narcs.py --ref`; don't rebuild it, reuse the pinned copy.
`tools/oxide/sync-docs.sh` mirrors `docs/oxide/` to the project folder and
complains about any file it has no mapping for. The full restart check-list
is at the top of the tracker.

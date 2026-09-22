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
- Ian's preferences: prose over bullets except for real lists, no em-dashes,
  keep replies short, do not open by praising his message, do not assume he
  is the expert on a question he asked, annotate code in plain English.
- Ask before doing anything expensive to redo or hard to reverse.
- Update `docs/oxide/tracker.md` at the end of every session and commit it.
  If any `docs/oxide/*.md` file changed this session, also run
  `tools/oxide/sync-docs.sh` to mirror it to the project folder on the G:
  drive, which a separate chat surface works from.
- Never delete, move, or overwrite the base ROM in the project folder
  (`Platinum Unlocked - Challenge - Adjusted v1.1.nds`). It is what every
  verify tool compares the build against, and and the only source for anything
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
design sheets on G:, with the synced `xlsx` skill for the mechanics). The
`/integrate` command in `.claude/commands/` merges every track into `oxide`
and runs the full verification gate.

## Build

See `docs/oxide/setup-fork-and-wsl2.md`. `make` for a checked build of the
unmodified tree; `make rom` for an unchecked rebuild after edits. Output:
`build/pokeplatinum.us.nds`.

**Run every Python script in this repo through `tools/oxide/oxide-python`, not
through `python3`**, and know what that buys. The wrapper gives every tool one
interpreter with the right packages, the `Makefile` puts it first on PATH for
the ninja steps, and `integrate.sh` goes through it.

**This box's CPU is faulty until its warranty replacement arrives.** The
i9-14900K is degraded: capped, single-threaded work is clean, but under
all-core load compilers and Python crash or return wrong answers (design doc
findings log, 2026-09-22). So a result here is trusted only after a second run
agrees with it. Retry a build that crashes, trust a ROM only when two complete
builds agree on its hash, and rerun a failed test before believing it.
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
launch your own emulator (`docs/oxide/setup-fork-and-wsl2.md` part 5b). The base ROM itself lives outside
the repo (see the design doc for its path on Ian's machine); a copy is pinned
at `~/roms/base.nds`. A byte-exact vanilla Rev 1 build (built once from
`main`) is pinned at `~/roms/vanilla.nds` for `import_base_rom.py --vanilla`
and `verify_narcs.py --ref`; don't rebuild it, reuse the pinned copy.
`tools/oxide/sync-docs.sh` mirrors `docs/oxide/` to the project folder and
complains about any file it has no mapping for. The full restart check-list
is at the top of the tracker.

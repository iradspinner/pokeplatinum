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
  (`Platinum Unlocked - Challenge - Adjusted v1.1.nds`). It's the only source
  left for edits not yet carried over (encounters, text, items, trades,
  trainers, map headers, the 91 scripts and 158 event files).

## Build

See `docs/oxide/setup-fork-and-wsl2.md`. `make` for a checked build of the
unmodified tree; `make rom` for an unchecked rebuild after edits. Output:
`build/pokeplatinum.us.nds`.

## Tools

`tools/oxide/import_base_rom.py` carries edits from Ian's earlier DSPRE-edited
ROM ("the base ROM") into `res/`. `tools/oxide/verify_narcs.py` proves a
rebuild reproduces a reference ROM's tables. The base ROM itself lives outside
the repo (see the design doc for its path on Ian's machine); a copy is pinned
at `~/roms/base.nds`. A byte-exact vanilla Rev 1 build (built once from
`main`) is pinned at `~/roms/vanilla.nds` for `import_base_rom.py --vanilla`
and `verify_narcs.py --ref`; don't rebuild it, reuse the pinned copy.
`tools/oxide/sync-docs.sh` mirrors `docs/oxide/*.md` to the project folder.

# Platinum Oxide

This fork of pret/pokeplatinum is the source of truth for the Platinum Oxide
project: porting the engine expansions of Hardlove Gold (an hg-engine
HeartGold hack) into Pokemon Platinum by editing this decomp directly.

Start every session by reading, in order:

1. `docs/oxide/design-doc.md`   what the project is, ground truth, scope, working rules
2. `docs/oxide/tracker.md`      open work, what is next, what waits on Ian
3. The `docs/oxide/phase*.md` notes and `docs/oxide/tracker-archive.md`
   (finished work) only as the tracker points you to them

Then say in one or two sentences what this session will do, and do it.

## Working rules (short form; the design doc has the full list)

- Work on `oxide` or a branch cut from it. Never commit to `main`; `main`
  tracks upstream pret.
- Every data change is verified by rebuilding (`make rom`; see Build) and,
  where a reference exists, comparing the rebuilt NARC to it with
  `tools/oxide/verify_narcs.py`.
- Edit `res/` JSON files with `tools/oxide/jsonstyle.py` helpers or by hand in
  the same style; never reformat whole files (the repo's formatting is not
  uniform and reformatting makes upstream merges painful).
- Ian's writing rules are in `~/.claude/CLAUDE.md`, which every session and
  subagent loads, and a hook refuses a dash or a banned phrase in Markdown and
  commit messages. Paste its "Hard rules" into any subagent brief (the brief
  template is in the `oxide-session` skill).
- Ask before doing anything expensive to redo or hard to reverse.
- Update your status home (below) at the end of every session and commit it;
  a finished tracker block moves verbatim to `docs/oxide/tracker-archive.md`.
  If any `docs/oxide/*.md` file changed this session, also run
  `tools/oxide/sync-docs.sh` to mirror it to the project folder on the G:
  drive, which a separate chat surface works from. It runs only on `oxide`,
  so on a track's branch the Overseer's merge runs it.
- Never delete, move, or overwrite a base ROM in the project folder. Since
  2026-09-26 the base ROM is Ian's `Test.nds` of 2026-08-31, copied there as
  `Platinum Oxide base ROM 2026-08-31 (from Example ROM Test.nds).nds`; the
  earlier `Platinum Unlocked - Challenge - Adjusted v1.1.nds` stays as the
  record of 2026-08-11. The base ROM is what every verify tool compares the
  build against (design doc, rule 3).
- A few files deliberately no longer match the base ROM, `scripts_common`
  first among them. The `bulk_*` tools keep their own list of these and skip
  them; do not "fix" a mismatch the tracker or its archive says is intended.
- Stage files by name when committing, never `git add -A` or `git add .`;
  sessions share this checkout and a sweep commits another session's
  in-progress files under your message.
- Several sessions run in parallel: the Oxide Overseer, the main track, the
  encounter track and the balance track, plus cloud sessions. Each edits only
  its own status home: the tracker for the main track and the Overseer,
  `docs/oxide/encounter-tool-build-plan.md` for the encounter tool (plus its
  one paragraph at the top of the tracker), `docs/oxide/balance-plan.md` for
  the balance track. Every track works on its own branch or worktree; the
  Overseer merges each into `oxide` with `tools/oxide/merge-branch.sh`.
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
`debug-live` (any in-game bug, with Ian driving melonDS), `cloud-job` (writing,
running or merging a cloud session's job), `ruling` (recording any decision of
Ian's everywhere it must be read), `playtest-day` (a session of in-game
checks from `docs/oxide/ingame-checklist.md`), `doc-links` (a clickable,
rendered link for any doc Ian is pointed at), `balance-rules` (Ian's
rulebook for any learnset, trainer, item or fight-scoring work),
`save-change` (anything that moves what the save stores) and `land-branch`
(the Overseer's landings). In
`.claude/commands/`, `/integrate` merges every track into `oxide` and runs the
full verification gate, `/qa-pass <base>` reviews and re-checks a range of
commits and writes up the findings, and `/docs-pass` audits the docs, skills and
this file against the tree.

A hook in `.claude/settings.json` refuses `git add -A` or `.`, launching an
emulator, and committing a file that carries the scratch marker
(`.claude/hooks/oxide_guard.py`); each refusal says which rule applies and
what to do instead. `.githooks/pre-commit` runs the encounter linter on any
commit that touches the encounter tables or tool; a clone enables it once with
`git config core.hooksPath .githooks`.

## Build

See `docs/oxide/setup-fork-and-wsl2.md`. `make` for a checked build of the
unmodified tree; `make rom` for an unchecked rebuild after edits. Output:
`build/pokeplatinum.us.nds`.

**The replacement CPU is in and passed its checks (2026-09-29).** The old
i9-14900K was degraded: under all-core load, compilers and Python crashed or
returned wrong answers (design doc findings log, 2026-09-22), and for a week
every build ran on GitHub. The new chip ran the stress check that caught the
old one with no failures, and built `oxide` from scratch twice on every core,
matching GitHub's SHA-1 both times. Local builds and parallel jobs are back
to normal, with no job limit.

Hand Ian a ROM built here from a pushed commit whose ROM matches GitHub's
SHA-1 for it, copied into `~/oxide-playtest` as
`pokeplatinum-oxide-<commit>.nds` (the test kit, from `make testkit` on the
same tree, as `pokeplatinum-oxide-testkit-<commit>.nds`), the names his saves
follow.
`tools/oxide/fetch-rom` builds a pushed commit in the private repo
`iradspinner/oxide-rom-builder` instead, and it spends Actions minutes and
storage. **No GitHub Actions in the private repos until 2026-10-01** (Ian,
2026-09-29): the account's Actions storage is used up, and he will not be
billed for more. Their workflows are switched off, so `fetch-rom` and a
melonDS-oxide build fail until then. The public repo's build on each push to
`oxide` is free and stays on.

GitHub builds every push to `oxide` on its own machines
(`.github/workflows/oxide-rom.yml`) and prints the ROM's SHA-1 in the run's
summary, and `integrate.sh` compares a local ROM with it. This public repo
never uploads the ROM.

## Cloud sessions

A Claude Code cloud session (claude.ai/code, set up on 2026-09-25) works on a
fresh Ubuntu VM with four healthy cores, so it can build and run heavy
analysis without tying up this box. Its environment runs
`tools/oxide/cloud-setup.sh` and sets `OXIDE_CLOUD=1`, and `make rom` fetches
the compiler itself on first use.

Its checkout carries only its own branch, and the encounter tools read vanilla
data from `main`, so run `git fetch --depth=1 origin main:main` before their
tests (`integrate.sh` does it itself). Its environment must also allow
`wrapdb.mesonbuild.com`, where meson fetches two subproject patches. Two
harmless oddities: a first build spends about a minute on retries, because
the session may reach only this repo on GitHub and two subproject downloads
fall back to mirrors; and the gate always warns that it found no GitHub build
to compare the ROM with, because the VM has no `gh`. The Overseer compares
the hash after the merge instead. The environment passed its smoke test on
2026-09-25: a clean build matched GitHub's SHA-1, and the gate had no failures.

It has no `~/.claude/`, so Ian's writing rules and the rulings kept in memory
are in `.claude/rules/` instead, and a repo copy of his style hook runs there.
It has none of the files outside the repo either: no base ROM, no vanilla
ROM, no donor ROM, no balance reference data. Ian ruled (2026-09-25) that
cloud sessions skip those checks. `integrate.sh` lists what it skipped under
one warning, and still checks the build, the encounter tables against their
JSON, and every test suite that needs no reference file. Anything that needs
the base ROM is checked locally after the work merges.

A cloud session works on its own branch, named `cloud/<track>-<topic>`, and
never pushes to `oxide`. It gates that branch with `bash tools/oxide/integrate.sh
--verify-only`, which checks any branch; `sync-docs.sh` stays the Overseer's. It cannot message the Overseer, so it reports
through the branch: its last commit message says what was done and checked,
failures first, and anything waiting on Ian. The Overseer, a local session,
reviews the branch, runs the base-ROM checks, and merges it. The `cloud-job`
skill holds the rules of a job from both ends, so a prompt can be short.

## Tools

`tools/oxide/import_base_rom.py` carries edits from Ian's earlier DSPRE-edited
ROM ("the base ROM") into `res/`. `tools/oxide/verify_narcs.py` proves a
rebuild reproduces a reference ROM's tables. `scriptdis.py` disassembles and
round-trips field scripts; `bulk_scripts.py`, `bulk_events.py` and
`bulk_text.py` regenerate whatever the build still gets wrong against the base
ROM (their `--dry-run` doubles as the check); `mapdiff.py` and `checkmap.py`
work one map at a time. `tools/oxide/encounters/` is the encounter tool, the Platinum OxiDex (OxiDex for short), with
its own tests and CLI (see its build plan). `tools/oxide/live_watch.py` attaches
to Ian's melonDS on Windows over its GDB stub while Ian drives the game; never
launch your own emulator (`docs/oxide/setup-fork-and-wsl2.md` part 5b, and the
`debug-live` skill). The base ROM itself lives outside the repo (see the design
doc for its path on Ian's machine); a copy is pinned at `~/roms/base.nds`,
with dated pins `~/roms/base-2026-08-31.nds` (the same file) and
`~/roms/base-2026-08-11.nds` (the base until 2026-09-26). A
byte-exact vanilla Rev 1 build (built once from `main`) is pinned at
`~/roms/vanilla.nds` for `import_base_rom.py --vanilla` and
`verify_narcs.py --ref`; don't rebuild it, reuse the pinned copy.
`tools/oxide/merge-branch.sh <branch>` lands one branch: merge, a GitHub build
of the merged tree, the gate on that ROM, and a push only on a pass.
`tools/oxide/sync-docs.sh` mirrors `docs/oxide/` to the project folder and
complains about any file it has no mapping for. The full restart check-list
is at the top of the tracker.

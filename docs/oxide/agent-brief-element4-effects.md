# Brief: element 4's battle effects, picking up from 2026-09-23

Written by the session that did this work, for the session that continues it.
Read `CLAUDE.md`, the design doc and the tracker first, as always; this brief
adds what those do not say yet and the order to do things in. Ian's writing
rules in `~/.claude/CLAUDE.md` apply to everything you write, including
commit messages, and a hook enforces the dash rule.

## Where things stand at `388331c51`

Phase 4 is on element 4, the move expansion. The move table holds 923 moves,
the 159 new species have their full level-up learnsets back, and 15 of the 116
new battle effects have real scripts. The other 101 effects are stubs. A stub
lets a damaging move do its damage without its extra, and makes a status move
print "But nothing happened!". Everything is pushed, and GitHub's builds match
local ones.

The tracker's element 4 entry under Phase 4 has the detail, including the
audit's verdict table. The design doc's findings log, entries dated
2026-09-22 and 2026-09-23, has the lessons.

## Where the ROM goes, and when it can be trusted

Ian plays from `\\wsl$\Ubuntu\home\ian\pokeplatinum\build`, which is
`build/pokeplatinum.us.nds` from `make rom`. This machine's i9-14900K is
degraded and a local build can come out wrong, so a local ROM counts only once
its SHA-1 matches GitHub's build of the same commit. Push the commit, then run:

```
tools/oxide/fetch-rom
```

It builds that commit in the private repo `iradspinner/oxide-rom-builder`, or
reuses a build from the last three days. It downloads the ROM to
`~/oxide-playtest/` after checking the hash the build machine recorded, and
prints that SHA-1. If `sha1sum build/pokeplatinum.us.nds` matches, the build
folder is good. If it does not, copy the fetched ROM over it and tell Ian the
local build was wrong. Every commit so far has matched. Retry a local build that
crashes, and rerun a failed check before believing it.

## The tools

`tools/oxide/convert_battle_scripts.py` converts hg-engine's scripts (a sparse
clone is at `~/hg-engine`) into Platinum's dialect. It has four modes:

- `--selftest` converts the 277 effects both projects ship and compares them
  with Platinum's. It should report 196 of 198 exact; String Shot and Rapid
  Spin differ because Hardlove changed them.
- `--audit` triages all 116 effects: ready (15, done), C (39), names (58),
  text (2), items (2).
- `--show N` prints one conversion.
- `--write N ...` converts effects into `res/battle/scripts/effects/` and
  refuses any the audit does not call ready.

`tools/oxide/romdiff.py OLD NEW` says what differs between two ROMs, down to
archive members. It is how each batch proves it touched only what it meant
to.

## Traps already found, so you do not find them again

1. **A name Platinum already defines is shared, never renamed.** The converter
   used to record the two games' different choices as renames, which would have
   aimed every self-targeting move at battler slot 0. The rule is in
   `derive_renames`; do not loosen it.
2. **Aim matters.** In Platinum's engine, a side effect flagged with neither
   `MOVE_SIDE_EFFECT_TO_ATTACKER` nor `TO_DEFENDER` targets battler slot 0.
   Before writing a script, check that every `MOVE_SUBSCRIPT_PTR_*` it sets is
   aimed the way Platinum's own scripts aim that pointer.
3. **Same name, different content.** A subscript can share a name with its
   hg-engine counterpart and still do something else, because Hardlove
   rewrote it. Rapid Spin is the example: hg-engine's also raises Speed. When a
   converted script leans on a subscript for its whole effect, read both
   versions of that subscript.
4. **A C reference is not always a C dependency.** hg-engine rewrote its damage
   calculation in C and ignores the script's power multiplier, so it doubles
   Venoshock in C. Platinum's calculation reads the multiplier
   (`battle_lib.c`, around line 6706), so the script alone works here. A
   reference that is just `MOVE_X,` in an array is list membership for an
   ability or item. That work belongs to elements 5 and 7, not to the move.
5. **Numbered text.** A `PrintMessage` with a bare number prints one of
   hg-engine's battle strings, which Platinum's bank does not have.
6. **Drives and Memories are not in Oxide**, so Techno Blast and Multi-Attack
   are correct as stubs: plain hits of their own type.

## Immediate next steps

1. **The C group, one effect at a time.** Run `--audit` for the current list
   with the C files hg-engine uses. For each effect, read hg-engine's C for it
   and decide which of three kinds it is:
   - a duplicate of what Platinum already does from the script, which you
     then write as it is;
   - behaviour Platinum lacks, which you port into Platinum's battle code,
     keyed on the new `BATTLE_EFFECT_*` constant the way Platinum keys its own
     effects;
   - list membership, which you leave for later elements.

   Likely easy first: Venoshock, Hex and Acrobatics (duplicates), then Triple
   Axel, whose power ramp probably lives in its script the way Triple Kick's
   does. Psyblade's boost needs Electric Terrain, so until terrain exists its
   script alone is correct. Harder: Final Gambit's self-faint and the post-move
   effects in `ServerDoPostMoveEffects.c`. Terrain (Steel Roller, Ice
   Spinner, the terrain moves) is a whole field mechanic Platinum does not
   have; scope it before starting it.
2. **The names group (58)**: 48 side-effect pointers, 6 subscripts (309, 335,
   354, 364, 380, 381) and 12 opcodes Platinum lacks. The subscript numbering
   is shared with hg-engine, so new ones append, as the effects did.
3. **The two text effects**, Poltergeist and Fickle Beam, need new battle
   strings.
4. The QA pass left four smaller items under element 4 in the tracker. The
   first is that `RANGE_ALL` has no branch in `BattleSystem_Defender`.

## How each batch is verified

The 15 were done this way, and each step caught something the others did not:

1. `--audit`, then `--show` each effect and read it, checking trap 2 above.
2. `--write` the batch, then `make rom`.
3. `romdiff.py` against the previous commit's fetched ROM. Only the intended
   members of `be_seq.narc` may differ, plus any C you changed.
4. `verify_narcs.py --built build/pokeplatinum.us.nds --ref ~/roms/base.nds`
   should report 0 disagreeing. `import_base_rom.py ... --dry-run` should
   report every count 0.
5. Update the tracker, commit, push, then `fetch-rom` for the hash match.
6. Add what Ian should try in the emulator to the tracker's "Waiting on Ian"
   list.

## Context this session relied on

Session memory lives in `~/.claude/projects/-home-ian-pokeplatinum/memory/`
now. The standing items are: emulator work is piggyback only (Ian drives
melonDS, and agents attach and never launch their own); delegate parallel or
context-heavy work to subagents; and cloud review is opt-in. The pinned ROMs
are `~/roms/base.nds`, `~/roms/vanilla.nds` and `~/roms/hardlove.nds`. Never
move or overwrite them.

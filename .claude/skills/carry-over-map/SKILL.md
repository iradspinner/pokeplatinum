---
name: carry-over-map
description: How to carry one map's field script, object events and text over from the base ROM into the pokeplatinum decomp's idiom, or re-humanise one of the 86 machine-generated scripts, for Platinum Oxide. Use this whenever a session touches res/field/scripts/*.s, res/field/events/*.json or a map's text bank in res/text/, is asked to make a generated script readable, to unify the clown gift scripts, or to check a map against the base ROM with mapdiff.py and checkmap.py.
---

# Carrying over one map

Phase 3 brought every changed map over byte-exact, six by hand and the rest
generated straight from the base ROM's bytecode. The generated ones are
correct and unreadable: machine labels (`JubilifeCity_0A4C`), numeric operands
where the repo uses `NPCMessage` and text-bank constants, objects named
`LOCALID_OBJECT_<n>`, messages named `<Bank>_Text_<n>`. Each says so in its
first line. Re-humanising them is backlog, one map at a time, and this is how
a map is done so the result still matches the base ROM.

## The unit of work is a map, across three files

A new object event is an NPC; the NPC needs a script to run when spoken to;
the script needs text. Landing one of the three alone produces a map that is
wrong in a new way. So every map is done across `res/field/events/events_<map>.json`,
`res/field/scripts/scripts_<map>.s` and `res/text/<map>.json` together, then
checked as one.

Resolve the script file through the map header's `scriptsArchiveID`, not by
name; at least two Mt Coronet maps do not line up by name.

## The workflow

```
python3 tools/oxide/mapdiff.py <map>      # all three sides of the diff, from the base ROM
# write the three files in the repo's idiom
# build the ROM (on GitHub with tools/oxide/fetch-rom until the new CPU is in)
python3 tools/oxide/checkmap.py <map>     # the rebuilt map against the base ROM
```

`checkmap.py` takes no ROM path: it reads `build/pokeplatinum.us.nds`, so copy
a fetched ROM there in your worktree's own `build/`.

`mapdiff.py` shows the events diff, the disassembled script (with symbolic
operands wherever they resolve globally) and the text bank with unreferenced
ids flagged. `checkmap.py` compares events byte for byte and the script command
by command: message ids are allowed to renumber when orphaned names are removed,
as long as every occurrence remaps the same way and the text it points at reads
the same. A map is done when `checkmap.py` is clean.

A fresh worktree has no `build/`, and `mapdiff.py` needs three things from one:
the enum headers (copy `build/generated/` from the main checkout), `msgenc`
(copy `build/tools/msgenc/msgenc`) and the library it loads (copy
`build/subprojects/yyjson-0.12.0/libyyjson.so*`). Copy them rather than
symlinking `build/`, so nothing run in the worktree writes into the shared
build. With those, one script can be assembled without a full build, which the
degraded CPU forbids: regenerate `build/generated/vars_flags.h` with the main
checkout's `subprojects/metang/metang.py` (a fresh worktree has no
subprojects) if you renamed a var or flag, generate the map's
text and events headers with `msgenc -H` and `build/tools/datagen/datagen-events`,
then run `tools/scripts/make_script_bin.sh` from `build/` with the include and
tool paths `ninja -t commands` prints for that script. Disassembling the output
with `scriptdis.emit_source` and diffing it against the base ROM's member shows
every change command by command, and catches a movement block pushed off
alignment before GitHub builds the ROM.

For a script you cannot read, `python3 tools/oxide/scriptdis.py` disassembles
any member of either ROM; `--roundtrip` proves the emitter, and
`tools/oxide/bulk_scripts.py --dry-run` must keep reporting "would write 0".

## The gotchas, each found the hard way

1. **Block order differs between look-alike maps.** The gift houses are not laid
   out identically: some roll the random number first and give last, others the
   reverse. Writing one in another's order assembles fine and is wrong; only
   `checkmap.py` catches it. Read each map's block order off its own disassembly.
2. **Trailing `.balign 4, 0`.** Several vanilla files end with it where the base
   ROM has no padding; leave it in and the file comes out two bytes long.
3. **Text changes do not reassemble scripts.** Changing a text bank regenerates
   `pl_msg.narc` but not the scripts that include its generated header, so a
   script can point at stale message ids. Touch the `.s` or build clean. The
   symptom is an empty message remap in `checkmap.py` where there should be one.
4. **Orphaned pick-event names.** Most gift houses were pick menus before Ian
   turned them into random rolls; the choice names are still in the text bank,
   unreferenced. Remove them as the map is done (the tracker's backlog lists the
   counts per map) and let the ids renumber.
5. **Some files diverge from the base ROM on purpose** and must stay that way.
   `DIVERGED` in `bulk_scripts.py` names 54 script files and the one in
   `bulk_events.py` 49 event files, each with its reason; the bulk tools skip
   them, a difference `checkmap.py` reports on one may be the intended one its
   entry names, and nobody should "fix" them. The first two were
   `scripts_common`, which uses the new `SetRepelSteps` command instead of the
   base ROM's scratch-address poke plus repurposed `Dummy088` (regenerating it
   would bring back the interpreter desync), and `scripts_init_battleground`,
   which builds the 4-byte equivalent of a terminator plus leftovers. Why each
   text bank that still differs from the base ROM is DSPRE noise rather than an
   outstanding edit is recorded under Phase 3 in `docs/oxide/tracker-archive.md`.
6. **Movement blocks must stay 4-aligned.** Vanilla writes `.balign 4, 0` before every
   movement label; the generated files do not, they copy the base ROM's padding. Any
   edit that changes a generated script's length shifts every movement block behind
   it, and an odd offset makes the ARM9 read garbage movement actions (it drops the
   low bit on halfword loads), which is how the whiteout hang happened. When you
   re-humanise or edit a generated script, add the `.balign` before each movement
   block and re-run `checkmap.py`, which compares command by command rather than
   byte by byte, so alignment padding alone should not fail it.
7. **Do not improve while carrying over.** Unifying the clown gifts or naming
   the possible Pokemon is a separate commit after the faithful version passes
   `checkmap.py`, so the two are separable in history. The gift catalogue is
   `docs/oxide/pokemon-gifts.md`.
8. **No temporary vars before a script task exists.** `InitNewGame`, and every
   map's OnTransition, OnLoad and OnResume script, runs through
   `FieldSystem_RunScript` with no script manager, so `VAR_RESULT` and every var
   from 0x8000 up write into another task's memory, silently. It hung every new
   game after the intro for a day (2026-09-27, fixed in 53b863005). Use saved
   vars for scratch there; the map-local ones are saved too.

## What to record

The tracker's backlog line for re-humanised maps: which maps, and any new
gotcha. A format fact (an operand width, a layout the disassembler did not
know) goes in the design doc's findings log. The two raw regions the
disassembler still emits as `.byte` in the vanilla ROM (`scripts_spear_pillar`
0x04b5, `scripts_common` 0x1268; the base ROM's versions of both decode
fully) are the place to start if a map's script will not decode.

After any script or event change, rerun `python3
tools/oxide/scriptindex.py` and commit `docs/oxide/script-index.md` and its
`.json`; the gate warns when they are stale. The index also shows which events
reach each script, and scripts nothing reaches.

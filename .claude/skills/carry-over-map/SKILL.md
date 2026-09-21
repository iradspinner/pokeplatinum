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
make rom
python3 tools/oxide/checkmap.py <map>     # the rebuilt map against the base ROM
```

`mapdiff.py` shows the events diff, the disassembled script (with symbolic
operands wherever they resolve globally) and the text bank with unreferenced
ids flagged. `checkmap.py` compares events byte for byte and the script command
by command: message ids are allowed to renumber when orphaned names are removed,
as long as every occurrence remaps the same way and the text it points at reads
the same. A map is done when `checkmap.py` is clean.

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
5. **Two files diverge from the base ROM on purpose** and must stay that way:
   `scripts_common` uses the new `SetRepelSteps` command instead of the base
   ROM's scratch-address poke plus repurposed `Dummy088` (regenerating it would
   bring back the interpreter desync), and `scripts_init_battleground` builds
   the 4-byte equivalent of a terminator plus leftovers. `bulk_scripts.py` skips
   both; do not "fix" them.
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

## What to record

The tracker's backlog line for re-humanised maps: which maps, and any new
gotcha. A format fact (an operand width, a layout the disassembler did not
know) goes in the design doc's findings log. The two raw regions the
disassembler still emits as `.byte` (`scripts_spear_pillar` 0x04b5,
`scripts_common` 0x1268) are the place to start if a map's script will not
decode.

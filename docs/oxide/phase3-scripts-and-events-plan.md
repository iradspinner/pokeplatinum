# Phase 3: the field scripts and events

Written 2026-09-20, after building and validating the `zone_event.narc` decoder.
This is the last Phase 3 item and much the largest. It exists because the
tracker's one-line "carry over scripts (91), events (158) and their text" hides
a job with three interlocking halves.

## The shape of it

Counted from the base ROM against the pinned vanilla build:

| | |
|---|---|
| Script files changed (`scr_seq.narc`) | 91 of 1,124 |
| Event files changed (`zone_event.narc`) | 158 of 534 |
| Text banks changed that belong to these maps | 60 of 724 |
| **Distinct maps touched** | **184** |
| ...with both script and event changes | 65 |
| ...with script changes only | 26 |
| ...with event changes only | 93 |

The three halves are not separable per map. A new object event is an NPC; the
NPC needs a script to run when you talk to it; the script needs lines of text.
Landing any one of the three alone produces a map that is wrong in a new way
rather than a map that is half right. So the unit of work is a map, not a file
type, and each map is done across all three at once.

## What is already built

`tools/oxide/import_base_rom.py` can decode `zone_event.narc` into exactly the
shape `res/field/events/*.json` holds. Validated against all 534 vanilla
records: every one round-trips, apart from seven files that spell out a
`"double_battle_id": 1` that is the default and packs identically.

Two decoding traps are handled and worth not rediscovering:

- An object event's `hidden_flag` and a coord event's `var` are ambiguous going
  back. `tools/jsoncnv/event.py` accepts either a `VarFlag` or a `MapHeaderID`
  name in those fields and the two enums overlap, so the same number spells two
  different things. Both are decoded as numbers and rendered in whichever family
  the file already uses.
- An object event's `script` field is a trainer id offset by 3000, or 5000 for
  the second trainer of a double battle, and otherwise a plain script number.

## The script disassembler (built 2026-09-20, `tools/oxide/scriptdis.py`)

Reads the command table from `include/data/scripts/scrcmd.h` (840 commands in
opcode order) and `asm/macros/scrcmd.inc` (each one's operand widths). Three
things the format does that had to be handled: six commands take a different
number of operands depending on an earlier one; `ScriptEntryEnd` is optional, so
the entry table also ends where the read position reaches the nearest offset any
entry points at; and 550 of the 1,124 members are init scripts, an unrelated
five-byte-entry format that a map header points at separately.

Verified on the pinned vanilla ROM: all 574 non-empty script files walk with no
unknown opcode and nothing running off the end, and all 550 init scripts read.
175 are accounted for byte for byte; the other 399 leave 33,206 bytes, which are
the movement blocks `ApplyMovement` points at plus short runs of unreferenced
`Noop` between scripts. The check that actually proves the widths: all 2,222
movement targets land outside decoded code, and a single collision would mean an
operand width was wrong.

On the base ROM, 573 of 574 walk cleanly. See the finding below.

### Still to build on top of it

- **A movement-block decoder.** `ApplyMovement` points at a separate encoding
  that this does not read yet. 2,222 references in vanilla.
- **Emitting `.s` text.** Labels for entries and jump targets, symbolic operands
  (text-bank entries, `LOCALID_*`, flags, vars, items, species), and matching the
  house style of `res/field/scripts/*.s`.
- **The true round trip.** Reassembling through the real build and requiring
  byte-identical output is the end-state check. Walking cleanly proves the
  widths; it does not yet prove the text that comes out reassembles.

### Finding: an unknown opcode in the base ROM's scripts_common

`scripts_common` (script 211) is the shared common-script file and the one Ian
grew most, from 5,912 bytes to 12,350. The walk hits **opcode 0x8000 at
0x1f38**. Everything else in the base ROM decodes.

That is either a custom script command or a desync caused by one, and it is the
first hard evidence on the long-open question of whether any carried-over script
calls the commands written over the Battle Arcade region (arm9
`0x05003C`-`0x0505BC`). Worth noting before assuming: 0x8000 also looks like a
variable reference rather than a command, vars starting at 0x4000, so the read
position may simply be wrong by then. Settle it by diffing the decode of
vanilla's `scripts_common` against the base ROM's and finding the first command
where they diverge, rather than by reading 0x1f38 in isolation.

## What the disassembler replaced: the original sketch

`scr_seq.narc` members are bytecode. A file opens with a table of `.long
(target - here - 4)` entries terminated by the halfword `0xFD13`, then the
script bodies. The decomp writes these as macro assembly in
`res/field/scripts/scripts_<map>.s`, one macro per command, with symbolic
labels for jump targets, text-bank entries and `LOCALID_*` object references.

Going the other way means a disassembler that knows every script command's
opcode and operand shape, because the operand widths decide where the next
command starts. `asm/macros/scrcmd.inc` is the authority on that list and is the
place to generate the opcode table from, rather than hand-writing it.

This is the real cost of the item and it is a tool-building job before it is a
carry-over job.

## Suggested order

1. ~~**Generate the opcode table**~~ Done, with the caveat above that a clean
   walk is not yet a byte-identical round trip.
2. **Do one small map end to end** as the template: events, script and text
   together, built and checked in the emulator. `oreburgh_city_middle_house`,
   `floaroma_meadow_house`, `sandgem_town_house` and
   `solaceon_town_northeast_house` are the best candidates, each one added
   object and a script that grows from about 48 bytes to about 300.
3. **The 93 events-only maps.** A first pass suggests 73 of them add objects
   that only reference scripts their map already has, which would make them
   importable without touching the script files at all. That check currently
   matches script files to maps by name; before relying on it, resolve each
   map's script file through its header's `scriptsArchiveID` instead, because at
   least two Mt Coronet maps do not line up by name.
4. **The remaining maps**, largest last.

## Open questions for Ian, to be answered as the work reaches them

- What specific scripts were *meant* to do, wherever the bytecode is ambiguous.
  This is the one place the carry-over cannot be mechanical.
- Whether any of the 91 scripts call the custom commands written over the Battle
  Arcade region (arm9 `0x05003C`-`0x0505BC`). This is the evidence that settles
  the long-standing question: if none of them do, that item closes with no work.

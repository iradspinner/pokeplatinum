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

## What is not built: the script disassembler

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

1. **Generate the opcode table** from `asm/macros/scrcmd.inc`, then write the
   disassembler and prove it by round-tripping: disassemble all 1,124 vanilla
   script files, reassemble them, and require byte-identical output. Vanilla is
   the test corpus, the same way the 534 vanilla event records validated the
   event decoder.
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

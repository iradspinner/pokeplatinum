# Phase 3: the field scripts and events

Written 2026-09-20, after building and validating the `zone_event.narc` decoder.
This is the last Phase 3 item and much the largest. It exists because the
tracker's one-line "carry over scripts (91), events (158) and their text" hides
a job with three interlocking halves.

> **Status (2026-09-20, end of day): done, with three hard stops.** Everything
> under "Still to build" and "Suggested order" below was built the same day.
> Six maps were carried over by hand in the repo's idiom, 70 events-only maps
> were patched, and then, at Ian's direction, the remaining 86 scripts, 84
> event files and 62 text banks were generated in bulk from the base ROM's
> bytecode by `tools/oxide/bulk_scripts.py`, `bulk_events.py` and
> `bulk_text.py`. Against the base ROM: events 158 of 158, scripts 90 of 91,
> text banks 72 of 78. The hard stops (`scripts_init_battleground`, the trainer
> battle messages, and the Repel prompt command below) and the cost of bulk
> generation (byte-exact but unreadable source, to be re-humanised a map at a
> time) are recorded in the tracker under Phase 3. This file stays as the record
> of the method and the formats.

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

### Built on top of it, same day

- ~~**A movement-block decoder.**~~ Done, plus a recovery pass for unreachable
  commands and unreferenced movement blocks; 98% of both ROMs' script bytes are
  accounted for, 6 regions in vanilla (90 bytes) and 4 in the base ROM (59
  bytes) are emitted as raw `.byte`.
- ~~**Emitting `.s` text.**~~ Done. Labels for entries and jump targets; symbolic
  operands for everything resolvable globally (vars, flags, sounds, items,
  species, moves, trainers, the engine-wide `LOCALID_*`), 32% of operands.
  `messageID` and map-local `localID` stay numeric unless a map is done by hand.
- ~~**The true round trip.**~~ Done: `scriptdis.py --roundtrip` reassembles every
  file through the repo's `make_script_bin.sh`; 574 of 574 byte-identical in
  both ROMs, with symbols on. Two gotchas it found: files that end with
  `.balign 4, 0` in vanilla where the base ROM has no padding, and gift houses
  that order their blocks differently from each other.

### Answered: the custom script command is a Repel prompt

The base ROM's `scripts_common` was the only file in either ROM that would not
decode. The command is opcode **0x88, `Dummy088`**, and it exists to serve a
"use another Repel?" feature.

**What the script does.** Three call sites, identical in shape, at `0x1ee8`,
`0x1f0c` and `0x1f30`:

```
AddMenuEntryImm 30, 0            @ "Repel"        (menu entries 30-32 are new text)
AddMenuEntryImm 31, 1            @ "Super Repel"
AddMenuEntryImm 32, 2            @ "Max Repel"
...
ScrCmd_Unused_007 0x023DFF28, 100/150/250
Dummy088
RemoveItem ITEM_REPEL/SUPER_REPEL/MAX_REPEL, 1, 0x8000
BufferPlayerName 0
BufferItemName 1, <the same item>
Message 72                       @ "{PLAYER} used the {ITEM}. Wild Pokemon will be repelled."
WaitButton / CloseMessage / ReleaseAll / Return
```

The whole flow, traced end to end in the base ROM's `scripts_common`:

```
0x0dc0  Message 75              @ "Repel's effect wore off... use another one?"
        ShowYesNoMenu           @ vanilla only has the wear-off line, 79, no prompt
        GoToIf yes -> 0x15bb
0x15bb  InitGlobalTextMenu
        CheckItem REPEL       -> if held, add menu entry 30 "Repel"
        CheckItem SUPER_REPEL -> if held, add menu entry 31 "Super Repel"
        CheckItem MAX_REPEL   -> if held, add menu entry 32 "Max Repel"
        ShowMenu
0x1ee8  ...the three branches above, one per Repel
```

So it only offers the Repels you are actually carrying. 100, 150 and 250 are
step counts.

**It is not "reusable Repels".** Each use still takes one from the bag, exactly
as vanilla: `RemoveItem <item>, 1` is right there in every branch. What the hack
saves is the trip back to the bag, not the item. Worth stating because the base
ROM *does* separately make TMs reusable, by skipping `Bag_TryRemoveItem` in the
party menu, and the two are easy to conflate.

**What the two commands do.** `ScrCmd_Unused_007` is a raw byte write,
`*(u8 *)addr = value`. Vanilla implements it and never uses it. The base ROM
uses it to stash the step count at `0x023DFF28`, a scratch address above the
heap. `Dummy088`'s vanilla body reads three halfwords and ignores them; the base
ROM replaces it at arm9 `0x0204EAE8` with a 60-byte routine that reads no
operands and does exactly one thing:

```
*(u8 *)(*(u32 *)0x02101D40 + 0x8087) = *(u8 *)0x023DFF28;
```

The two-step dance exists because a script command can only poke a *fixed*
address, and the destination sits behind a pointer that is not known when the
script is assembled. So the script writes the value somewhere fixed and native
code moves it through the pointer.

**What the destination is.** Established: a byte behind the pointer at
`0x02101D40`, offset `0x8087`. Inferred but not proven: the save's repel-steps
counter. `SpecialEncounter` reaches it as a `u8` at `+0x14F`, via
`SaveData_GetSpecialEncounters` (save table entry 25), and
`SaveData_SaveTable` returns `saveData + 20 + blockOffset[id]`, so this would
need `blockOffset[25] == 0x7F24`. That was not checked; nothing in the vanilla
arm9 references `0x02101D40` by literal, so the address was found by inspection
rather than taken from a symbol. The script context leaves little doubt about
the intent either way.

**Ported 2026-09-20** exactly as described below, closing Phase 3 hard stop 3.

**How to port it.** Not by reimplementing `Dummy088`. Add a proper script
command, say `SetRepelSteps <count>`, that writes through
`SpecialEncounter_GetRepelSteps`, and rewrite the three call sites to use it.
That drops the `Unused_007` scratch poke as well, since it only exists to work
around the pointer problem. The text this feature needs is part of the 16 unused
slots that gained text and were deferred earlier: `MENU_ENTRIES` 30-32 and
`COMMON_STRINGS` 75 and 79.

**This closes the Battle Arcade question.** Of the roughly 1.4 KB of custom code
written over that region, the scripts call exactly one command, three times, all
in `scripts_common`, and nothing else in either ROM calls a custom command. The
rest of the region can be dropped.

`scriptdis.py --base-rom` applies the two-byte reading via `BASE_ROM_OVERRIDES`.
With it, all 574 base-ROM script files walk, matching vanilla.

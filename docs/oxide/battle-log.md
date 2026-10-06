# The battle log in the save

Oxide keeps its last 60 trainer battles in the save, so the OxiDex can read
who knocked out whom at each in-game save (Ian, 2026-09-27). This file is the
byte layout the OxiDex's reader is written against. The engine side is
`src/battle_log.c` and `include/battle_log.h`; the save-layout note is in
`save-layout.md`.

## Where it lives

In the save file it is flash sector 44 of each half: **0x2C000** for the
primary copy and **0x6C000** for the backup. Both copies are written, primary
first, at every in-game save that writes the main save's normal block, right
after the main save succeeds. The main save's blocks, sizes and footers do
not change. A save made before this change has both sectors erased (0xFF),
which reads as an empty log.

In RAM the log sits in the save image's free tail, straight after the boxes
block: `SaveData.body.data` plus the end of the last block, which is 0x2B3E4
since the 30 PC boxes (0x1F200 before). The game checks at boot that the log
fits there. The 30 boxes left the sector where it was: the main save now ends
inside sector 43, and the Hall of Fame, Frontier and recordings moved up to
sectors 45 to 56, so sector 44 sits between them. Should the main save ever
grow into sector 44, the game stops writing the log rather than overwrite the
save (`BattleLog_SectorFree`); `tools/oxide/save_budget.py` reports the
margin, 3,100 bytes today. A battle is added to
the RAM copy when it ends, so a reset without saving loses the log's newest
battles along with the rest of the unsaved game, and the two never disagree.

Trainer battles are logged, won or lost. Wild battles, link battles, the
Battle Frontier and battle-video playback are not.

## The copy (0xDB8 bytes, little-endian)

| Offset | Size | Field |
|---|---|---|
| 0x000 | 4 | magic, the bytes `OBL1` |
| 0x004 | 2 | version, 1 |
| 0x006 | 2 | record size, 58 |
| 0x008 | 2 | capacity, 60 |
| 0x00A | 2 | count of records held, 0 to 60 |
| 0x00C | 2 | next: the record the next battle overwrites, 0 to 59 |
| 0x00E | 2 | 0 |
| 0x010 | 60 x 58 | the records, a ring |
| 0xDA8 | 4 | footer: signature 0x20060623, the game's own |
| 0xDAC | 4 | save counter, one higher at each write |
| 0xDB0 | 4 | size the checksum covers, 0xDA8 |
| 0xDB4 | 2 | id, 0x4C42 |
| 0xDB6 | 2 | CRC-16 of bytes 0x000 to 0xDA7, the main save's CRC (`CalcCRC16Checksum`, CCITT from 0xFFFF; `savefile.crc16`) |

A copy is valid when its magic, footer signature, size and CRC all check. Of
two valid copies, the one with the higher save counter is current; with
neither valid the log is empty. The newest record is at `(next + 59) % 60`,
and the records run back from there for `count` records.

## One record (58 bytes)

| Offset | Size | Field |
|---|---|---|
| 0x00 | 2 | trainer A's id |
| 0x02 | 2 | trainer B's id, 0 when there is one opposing trainer |
| 0x04 | 2 | turns the battle lasted |
| 0x06 | 1 | flags (below) |
| 0x07 | 1 | the level-cap split (`VAR_LEVEL_CAP_SPLIT`) as the battle ended |
| 0x08 | 6 x 2 | the player's six, species with the form in the top five bits: `(form << 11) \| species` |
| 0x14 | 6 x 1 | the low 8 bits of each one's personality, to tell two of a species apart |
| 0x1A | 6 x 1 | each one's level as the battle ended |
| 0x20 | 6 x 2 | the opponents, `(form << 11) \| species`: trainer A's party in order, then B's |
| 0x2C | 6 x 1 | each opponent's level as the battle ended |
| 0x32 | 3 | who knocked out each opponent: six 4-bit values, slot 0 in the low half of the first byte |
| 0x35 | 3 | who knocked out each of the player's six, packed the same way |
| 0x38 | 1 | how many Pokemon the player had |
| 0x39 | 1 | how many each opponent had: A's in the low four bits, B's in the high four |

Slots beyond a count hold species 0 and the value 0xF in the knock-out
fields. The player's six are the player's own party, in party order, which a
switch in battle does not change; an AI partner's Pokemon are not among them.
An egg in the party is recorded as 0x7FF (form 0), not as the Egg's species id, which moves whenever a species is added.

Flags: bit 0 the player won, bit 1 the player lost (both set is a draw), bit 2
a double battle, bit 3 an AI partner fought beside the player, bit 4 two
opposing trainers. The other bits are 0.

## Knock-out credit

A knock-out is credited to a Pokemon only when that Pokemon's move made the
faint, as the move ran. Everything else is indirect.

| Value | Who knocked out an opponent | Who knocked out the player's Pokemon |
|---|---|---|
| 0 to 5 | the player's Pokemon in that party slot | the opponent in that slot, numbered as in the opponents' list |
| 6 | the AI partner's Pokemon | the player's own side: the player's other Pokemon, or the partner's |
| 7 | anything else: poison, burn, weather, Leech Seed, recoil, Life Orb, Rocky Helmet, Destiny Bond, Perish Song, confusion, a move of its own side | the same |
| 0xF | not knocked out | not knocked out |

## The RAM beacon

For the live export (the melonDS fork), the game keeps one small struct in
main RAM that points at what the export reads, so the fork needs no
per-build addresses. It is found by its two magic words and rechecked on
every read.

| Offset | Size | Field |
|---|---|---|
| 0x00 | 4 | magic, the bytes `OXBN` |
| 0x04 | 4 | the same four bytes, inverted |
| 0x08 | 2 | version, 2 |
| 0x0A | 2 | size of this struct, 0x2C |
| 0x0C | 4 | the SaveData |
| 0x10 | 4 | the party |
| 0x14 | 4 | the PC boxes |
| 0x18 | 4 | the battle log's RAM copy (the table above) |
| 0x1C | 4 | during a battle, the BattleContext; otherwise 0 |
| 0x20 | 4 | the TrainerInfo |
| 0x24 | 2 | the number of PC boxes, 30 since the 30 boxes landed |
| 0x26 | 2 | entries in the layout table, 22 since 2026-10-06 (9 before) |
| 0x28 | 4 | the layout table: u16 values the compiler worked out, so a reader needs no per-build offsets |

Pointers are main-RAM addresses (0x02xxxxxx). Version 1 (2026-09-28, the
battle log's first build) stopped at 0x20. The version stays 2 when the
table grows: entries are only ever added at its end, so a reader checks the
count before it reads an entry past the ones it needs, and a reader built for
fewer entries reads the first ones as before. The layout table, in order,
with the values of the build of 2026-10-06:

| Entry | Value | Meaning |
|---|---|---|
| 0 | 0x10 | the u32 id in the TrainerInfo: trainer id in the low half, secret id in the high |
| 1 | 0x49B4 | the four battlers' BattleMon records in the BattleContext |
| 2 | 0xC4 | the size of one BattleMon |
| 3 | 0x00 | a BattleMon's species, u16 |
| 4 | 0x38 | its level, u8 |
| 5 | 0x50 | its current HP, s32 |
| 6 | 0x54 | its maximum HP, u32 |
| 7 | 0xEC | the size of a party Pokemon, 236 |
| 8 | 0x88 | the size of a boxed Pokemon, 136 |
| 9 | 0x0C | a BattleMon's four move ids, u16 each |
| 10 | 0x30 | its current PP, a byte a move |
| 11 | 0x70 | its status, u32 of `MON_CONDITION_` bits (sleep turns in bits 0 to 2, then poison, burn, freeze, paralysis, toxic) |
| 12 | 0x74 | its volatile status, u32 of `VOLATILE_CONDITION_` bits (confusion's turns in bits 0 to 2) |
| 13 | 0x18 | its eight stat stages, a byte each from 0 to 12 with 6 for unchanged, in the order HP, Attack, Defense, Speed, Sp. Atk, Sp. Def, accuracy, evasion |
| 14 | 0x3E1C | the BattleContext's `battlerActions`: four u32 a battler, battler after battler |
| 15 | 0x4D40 | its `moveSlot`: a u16 a battler, the move slot chosen, 0 to 3 |
| 16 | 0x4DD0 | its `recordedCommandFlags`: a byte a battler, bit 0 set once the battler chose a command this turn |
| 17 | 0x150 | its `totalTurns`: the turns finished, s32 |
| 18 | 0x08 | its `command`: the battle controller's current step, s32 |
| 19 | 0x0C | its `commandNext`: the step a running battle script returns to, s32 |
| 20 | 5 | the value of `BATTLE_CONTROL_COMMAND_SELECTION_INPUT` (a value, not an offset) |
| 21 | 21 | the value of `BATTLE_CONTROL_EXEC_SCRIPT` (a value, not an offset) |

The party is a Party: s32 capacity, s32 count, then six 236-byte records.
The boxes are a PCBoxes: u32 current box, then each box's 30 records of 136
bytes, box after box.

### The turn's chosen actions

Entries 9 to 21 are for the battle recorder (alpha readiness, step 11). The
battle already keeps each battler's choice from the moment it is made until
the next turn's, so the game adds no code for them, only the table entries.
A battler's four `battlerActions` are, in order: the command the turn runs
for it (a `BATTLE_CONTROL_` value, set to `BATTLE_CONTROL_MOVE_END` once it
has acted, so of no use afterwards); the target battler of its move; the
move slot plus one for a move (0 when Encore chose it), the party slot for a
switch, or for an item a `BattleItemUse` (the item in the low half, and in
the top byte the party slot it was used on plus one, or 0); and the menu
command it picked (1 fight, 2 bag, 3 Pokemon, 4 run). The last three, the
move slot and the command flag stay as they are until that battler picks
again next turn.

So the choice is read while the turn plays out. The battle is choosing a turn,
and the fields hold last turn's choice or a half-made one, while `command` is
at most entry 20's value, or is entry 21's value with `commandNext` at most
entry 20's (a trainer's message or a switch-in ability between turns). The
turn being chosen or played is `totalTurns` plus one. A battler whose command
flag is clear chose nothing: it is recharging (`VOLATILE_CONDITION_RECHARGING`)
or locked into its move (a rampage, Uproar, or a two-turn or rolling move),
and its move slot is still the one that locked it.

Known limits, none of which matter to a boss rating: Struggle reads as the
last move slot chosen (all its PP at 0 shows it); running from the move menu's
touch-screen button reads as a fight; Safari and Pal Park battles keep no
command flag and read as no choice; and a Pokemon sent in at the end of a turn
to replace a fainted one shows its predecessor's choice until the next turn,
so the recorder keeps the first choice it sees for each battler and turn.

The melonDS fork's `/battle_state` (its `beacon-moves` branch, 2026-10-06)
reads these into each battler's `moves`, `pp`, `status`, `volatile`,
`statStages` (signed, -6 to +6) and `action`, and adds the state's `turn` and
`phase`; with a ROM that gives nine entries it answers as before.

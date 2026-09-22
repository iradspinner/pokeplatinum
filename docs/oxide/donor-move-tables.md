# Hardlove's move tables, read directly

Written 2026-09-21 as groundwork for Phase 4 element 4, the move expansion.
Everything below was read out of the donor ROM and compared against this repo's
own `res/moves/*/data.json` and `generated/*.txt`, not taken from hg-engine's
source. The reader is `tools/oxide/donor_moves.py`, which sits on `donor.py` and
does not modify it. The donor ROM is pinned at `~/roms/hardlove.nds`.

**What could not be checked.** There is no stock HeartGold ROM on this machine.
`/mnt/g/PokeROMs/HeartGold Roms/` holds only Hardlove and its backups, so
nothing below is cross-referenced against vanilla HGSS. Where a comparison was
useful it is against stock Platinum (`~/roms/vanilla.nds`,
`poketool/waza/pl_waza_tbl.narc`), which shares the record layout. That is
enough for the port, but it means "hg-engine changed this" and "HGSS already
differed from Platinum here" cannot always be told apart.

## Where things are

| NARC or bank | What | Shape |
|---|---|---|
| `a/0/1/1` | move data | 924 members, 16 bytes |
| `a/0/2/7` bank 750 | move names | 923 entries |
| `a/0/2/7` bank 751 | move names, uppercase | 923 entries |
| `a/0/2/7` bank 749 | move descriptions | 923 entries |
| `a/0/2/7` bank 3 | moves used in battle | 2769 entries, three per move |

Vanilla HGSS move data is `a/0/1/1` with 16-byte records. **hg-engine did not
move it and did not widen it.** It lengthened it, from 468 usable records to
924, and left the record alone. The two padding bytes at 0x0E are zero in all
924 records, checked, so nothing was smuggled into them.

`a/0/1/0` has 923 members and `a/0/1/2` has 965. Both counts sit suspiciously
close to the move count, so they are probably the move battle scripts and the
battle sub-scripts, HGSS's equivalents of Platinum's `battle/skill/waza_seq.narc`
(501 members) and `battle/skill/sub_seq.narc` (297). **That is a guess from the
member counts alone.** Neither was decoded and neither member matches its
Platinum counterpart byte for byte, which is expected between two games but is
not evidence either way. Identifying them is its own job and element 4 will need
it.

## The move record

Identical to Platinum's `MoveTable` in `include/move_table.h`, field for field.

| Offset | Width | Field | `res/moves/*/data.json` key | Notes |
|---|---|---|---|---|
| 0x00 | u16 | battle effect | `effect.type` | agrees with Platinum for 0..276, continues to 406 |
| 0x02 | u8 | class | `class` | 0 physical, 1 special, 2 status, as Platinum |
| 0x03 | u8 | power | `power` | |
| 0x04 | u8 | type | `type` | Platinum's numbering, **except type 9 is Fairy** |
| 0x05 | u8 | accuracy | `accuracy` | 0 means never misses |
| 0x06 | u8 | PP | `pp` | |
| 0x07 | u8 | effect chance | `effect.chance` | |
| 0x08 | u16 | range | `range` | **a bitmask, not Platinum's enum index** |
| 0x0A | s8 | priority | `priority` | same encoding, values rebalanced |
| 0x0B | u8 | flags | `flags` | same eight bits, same meanings |
| 0x0C | u8 | contest effect | `contest.effect` | |
| 0x0D | u8 | contest type | `contest.type` | 0..4, agrees exactly |
| 0x0E | 2 | padding | none | zero in all 924 records |

Decoded proofs, against values that can be checked independently:

```
  85 Thunderbolt   type 13 Electric  special  power  90  acc 100  pp 15  effect 6 PARALYZE_HIT  chance 10
  33 Tackle        type  0 Normal    physical power  40  acc 100  pp 35  effect 0 HIT
  63 Hyper Beam    type  0 Normal    special  power 150  acc 100  pp  5  effect 80
 144 Transform     type  0 Normal    status   power   0  acc   0  pp 10  effect 57
 467 Shadow Force  type  7 Ghost     physical power 120  acc 100  pp  5  effect 272
```

Thunderbolt is 90 power and Tackle 40 because Hardlove carries the modern
values, not Platinum's 95 and 35. Everything else in those two lines is what it
should be, and the type, class, accuracy, PP and effect-chance fields land in the
right place for all five, so the layout is settled.

## The move count

**924 records, 923 named ids, 452 new moves.** The tracker's 924 is the record
count and is right as far as it goes, but three of the numbers matter separately:

- `a/0/1/1` has 924 members. The last one, id 923, has no name and no
  description; it is a spare.
- The three text banks have 923 entries each, so the named ids are 0..922. Id 0
  is `MOVE_NONE`, printed as `-`.
- Ids 468, 469 and 470 are named `MOVE_468`, `MOVE_469`, `MOVE_470` and
  described as `--`. Those are the three inaccessible tail records the retail
  game ships and `tools/dataproc/src/moveproc.c` reproduces in
  `pack_extra_moves()`. Hardlove kept them and started its own moves at 471,
  Hone Claws, running unbroken to 922, Malignant Chain.

So the real new content is **452 moves at ids 471..922**.

## Does the numbering agree with Platinum for 1..467

**Yes, exactly, with no lookup table needed.** This is the same answer the
ability import got, and the evidence is stronger than it was there.

The names are the decisive check. Decoding bank 750 and comparing all 468
entries against the `name` field of `res/moves/<name>/data.json`, in
`generated/moves.txt` order, gives **464 exact matches and four differences that
are the same move spelled a modern way**:

| id | Platinum | donor |
|---|---|---|
| 11 | ViceGrip | Vise Grip |
| 136 | Hi Jump Kick | High Jump Kick |
| 185 | Faint Attack | Feint Attack |
| 265 | SmellingSalt | Smelling Salts |

The data corroborates it. Comparing each donor record against the JSON,
field by field, over ids 0..467:

| Field | Records that differ, of 468 |
|---|---|
| contest type | 0 |
| class | 1 (Pain Split) |
| type | 8 |
| effect | 10 |
| priority | 14 |
| contest effect | 18 |
| range | 5 after the bitmask is decoded, 120 before |
| effect chance | 11 |
| PP | 73 |
| power | 83 |
| accuracy | 83 |
| flags | 37 ignoring King's Rock, 238 counting it |

Every one of those differences is Hardlove or hg-engine changing what a move
does, not the ids sliding. The eight type changes are the giveaway: Sweet Kiss,
Charm and Moonlight became Fairy, Curse became Ghost, and the rest are Hardlove
redesigns (Growth to Grass, Super Fang and Pain Split to Dark physical 1 power,
Covet to Fairy). Each is still the right move in the right slot.

**Conclusion: donor move id == Oxide move id for 0..467, and the new moves can be
appended contiguously from 468 up.** No translation layer, ever. Whether Oxide
fills 468, 469 and 470 with the donor's placeholders or with real moves is a free
choice, since nothing references them.

## Names and descriptions

Bank 750 names, 751 the same names uppercased, 749 the descriptions. 923 entries
each, indexed by move id directly. The descriptions are the modern games' text,
already wrapped into the game's own lines, which is the shape
`res/moves/*/data.json` wants.

```
 471 Hone Claws        The user sharpens its claws to boost its Attack and Accuracy.
 500 Echoed Voice      The user attacks the target with a harsh echo. If used every turn, power increases.
 600 Aromatic Mist     The user boosts the Sp. Def stat of an ally Pokemon by using a mysterious aroma.
 800 Expanding Force   The user attacks with its psychic power. This move's power goes up ...
 922 Malignant Chain   The user pours toxins into the target through a corrosive chain. ...
```

Only four description slots are empty or `--`: id 0 and the three retail
placeholders. Every real move has text.

Bank 3 holds the "used in battle" lines, 2769 entries, three per move id in
ally, wild, foe order, matching Platinum's `T_MOVES_USED_IN_BATTLE`. Checked on
the first few moves only, not all 923. The foe line reads "The opposing ..."
where Platinum says "The foe's ...", which is HGSS's wording. `moveproc.c`
generates the whole bank from the name anyway, so Oxide does not need to import
it.

## The effect field, which is the one that sizes element 4

**The donor's effect numbering agrees with Platinum's.** Effects 0..276 are
Platinum's `BATTLE_EFFECT_*` in the same order, and hg-engine's additions start
at 277 and run to 406.

Evidence. Of the 468 shared ids, 458 carry exactly the effect id that
`res/moves/*/data.json` gives, and that corroborates **251 of Platinum's 277
effect ids directly** (an id counts as corroborated when some move 0..467 has it
in both sources). The ten that differ are all Hardlove changing the move:

| id | move | donor effect | Platinum effect |
|---|---|---|---|
| 81 | String Shot | 60 SPEED_DOWN_2 | 20 SPEED_DOWN |
| 168 | Thief | 0 HIT | 105 STEAL_HELD_ITEM |
| 216 | Return | 0 HIT | 121 POWER_BASED_ON_FRIENDSHIP |
| 218 | Frustration | 0 HIT | 123 POWER_BASED_ON_LOW_FRIENDSHIP |
| 230 | Sweet Scent | 64 ACC_DOWN_2 | 24 EVA_DOWN |
| 294 | Tail Glow | 330 (hg-engine) | 53 SP_ATK_UP_2 |
| 336 | Howl | 385 (hg-engine) | 10 ATK_UP |
| 343 | Covet | 0 HIT | 105 STEAL_HELD_ITEM |
| 448 | Chatter | 76 CONFUSE_HIT | 267 CHATTER |
| 454 | Attack Order | 43 HIGH_CRITICAL | 2 POISON_HIT |

None of those is a renumbering. Modernised stat drops, two natives given a new
hg-engine effect, and four moves Hardlove simplified to a plain hit. The fact
that hg-engine's first added effect is exactly 277, the number Platinum stops
at, is the other half of the argument: it appended rather than rebuilt.

**The number element 4 turns on.** Of the 452 new moves:

| | Moves | Distinct effects |
|---|---|---|
| use an effect Platinum already has (id < 277) | **316** | 57 |
| use an effect Platinum does not have (id >= 277) | **136** | **114** |

So roughly seven new moves in ten can be imported as data and will work with a
battle script Oxide already has. The other 136 need 114 distinct new battle
effects written, and two natives, Tail Glow and Howl, want two more of the same
set. Ids 277..406 are used with gaps: 309, 327, 329, 331..340 and 404 never
appear.

**The caveat, stated plainly.** 251 of 277 effect ids are corroborated by a
direct match. The remaining 26 are ids no native move exercises in both sources,
so their agreement is inferred from the pattern rather than measured. Three of
them are used by new moves: 21 `SP_ATK_DOWN`, 61 `SP_ATK_DOWN_2` and
121 `POWER_BASED_ON_FRIENDSHIP`. The first two are almost certainly right, since
their neighbours in both stat-drop runs all match. 121 is worth a look when it
comes up, because Return is one of the moves Hardlove rewrote away from it.

## The fields that do not carry across as they are

### Range is a bitmask

Platinum stores a `RANGE_*` enum index, 0 to 16. The donor stores
0, 1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, and three moves store 24. That is
a bitmask: bit *n-1* means Platinum's range *n*, and 0 still means a single
target. Applying `0 -> 0`, otherwise `1 << (n-1)`, makes 463 of the 468 shared
ids agree; the five left over are Hardlove using a modern target rule (Smog to
single target, Poison Gas and Cotton Spore to adjacent opponents, Howl to the
user's side, plus Conversion 2).

The three that store 24 are Rototiller, Flower Shield and Teatime, 8|16,
all-adjacent plus the user. Platinum has no single range for that, so those three
need a decision rather than an import. `donor_moves.range_to_platinum` returns
`None` for them.

Whether hg-engine's engine really treats the field as a mask or just happens to
have assigned powers of two to a plain enum is not something the data settles;
24 says a mask, but one combination in 924 records is thin. Either way the
conversion above is what the import needs.

### King's Rock is gone

The eight flag bits are Platinum's, in Platinum's order, and
`MOVE_FLAG_MAKES_CONTACT`, `MOVE_FLAG_HIDES_HP_GAUGES` and
`MOVE_FLAG_HIDES_SHADOWS` agree on all 468 shared ids. But
`MOVE_FLAG_TRIGGERS_KINGS_ROCK` is set on **one move in the whole 924-record
table**, and on none of the 468 shared ids, where Platinum sets it on 202. That
looks like hg-engine dropping the flag rather than a coincidence, but the cause
was not traced. Ignoring that bit, only 37 of 468 flag bytes differ, mostly
Magic Coat and Snatch eligibility.

If Oxide imports the donor's flags as they are, King's Rock stops working. The
import should either keep Platinum's flag byte for natives or reinstate the bit
from the move's own class and power.

### Contest data is only half there

Contest type agrees on all 468 shared ids. Contest effect agrees on 450, and the
18 that differ are all the same case: every Platinum move with
`CONTEST_EFFECT_VOLTAGE` (8) has 7, `CONTEST_EFFECT_CONSECUTIVE_USE`, in the
donor. Value 8 never appears anywhere in the donor's 924 records, and neither
does 3. Values 9 to 23 appear and agree, so this is not a shift; one value is
simply missing from whatever table hg-engine rebuilt from. Not worth chasing.

For the 452 new moves the contest effect is only ever 0 or 5 (`NONE` or `BASIC`)
and the contest type is spread over 0..4 with no obvious rule. **hg-engine did
not author contest data for its new moves.** Oxide has Super Contests, so the 452
new moves will need a contest effect and type assigned from somewhere else, or
a default.

### Priority

Same `s8` field, range -7 to 5, but 14 of the shared ids carry modern values:
Protect, Detect and Endure at 4 rather than 3, Fake Out at 3, ExtremeSpeed at 2,
Teleport at -6, Metal Burst at 0. Platinum's priority system handles the range,
so this is a balance question rather than a format one.

## Field mapping, donor to `res/moves/*/data.json`

| Donor field | JSON key | Carries straight across |
|---|---|---|
| effect, effect chance | `effect.type`, `effect.chance` | yes for ids < 277 |
| class | `class` | yes |
| power, accuracy, PP | `power`, `accuracy`, `pp` | yes |
| type | `type` | yes, after mapping donor 9 to `TYPE_FAIRY` |
| range | `range` | after the bitmask conversion, except the three 24s |
| priority | `priority` | yes |
| flags | `flags` | yes except King's Rock |
| contest effect, contest type | `contest.effect`, `contest.type` | natives yes, new moves not authored |
| bank 750 | `name` | yes |
| bank 749 | `description` | yes, already line-wrapped |

Nothing in the donor's record has no JSON key, and no JSON key has no donor
field. The record is Platinum's record. What the JSON needs that the donor has
nowhere at all is the per-move `anim.s` and `script.s` that `moveproc.c` expects
beside each `data.json`; those are the battle and animation scripts. They were
not taken from the donor: effect scripts come from hg-engine's source through
`tools/oxide/convert_battle_scripts.py`, and every new move reuses an existing
Platinum animation (`docs/oxide/move-animation-map.json`).

## The type 9 trap

Donor type 9 is Fairy, as in the species record. **Platinum's own type 9 is
`TYPE_MYSTERY` and one Platinum move really uses it: Curse.** So the
`9 -> TYPE_FAIRY` substitution is only ever valid on a donor record, and never on
a value already in `res/`. `donor_moves.type_to_oxide` exists to make that
explicit. Four shared ids carry type 9 in the donor (Sweet Kiss, Charm, Moonlight,
Covet) and 30 of the 452 new moves do.

## What the numbers are

| | |
|---|---|
| donor move records in `a/0/1/1` | 924 |
| donor named move ids | 923 (0..922) |
| donor new moves | 452 (471..922) |
| retail tail placeholders kept | 3 (468..470) |
| shared ids whose name matches Platinum's | 464 of 468 |
| shared ids whose effect matches Platinum's | 458 of 468 |
| Platinum effect ids corroborated directly | 251 of 277 |
| highest donor effect id | 406 |
| new moves needing no new battle effect | 316 |
| new moves needing a new battle effect | 136 |
| distinct new battle effects to write | 114 |
| new moves typed Fairy | 30 |
| new moves with authored contest data | 0 |

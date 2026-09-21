# Hardlove's data tables, read directly

Written 2026-09-20 to close the Phase 4 prerequisite "read Hardlove's `a/0/2/8`
members 9_07..9_13". Everything below was read out of the donor ROM, not taken
from hg-engine's source, so it describes the build Oxide is actually importing
from. The reader is `tools/oxide/donor.py`; the donor ROM is pinned at
`~/roms/hardlove.nds`, a copy of the one in the project folder.

## Where things are

| NARC | What | Shape |
|---|---|---|
| `a/0/0/2` | species records | 1476 members, 44 bytes |
| `a/0/3/3` | level-up learnsets | one blob, 34 fixed slots per species |
| `a/0/3/4` | evolutions | 1476 members, 9 slots of 6 bytes plus 2 padding |
| `a/0/2/8` | hg-engine's added data | 20 members, 7 to 13 below |
| `a/0/2/7` | text | 854 banks; abilities are 720, 721, 722 |

DSPRE's extraction folder names map to these: `personalPokeData`, `learnsets`,
`evolutions`, `synthOverlay`, `textArchives`. The extraction is faithful, member
counts and bytes both, so either source can be used.

## The species record

hg-engine's `SpeciesData`, which is still 44 bytes but is not Platinum's layout:
ability 1 is a u16 at 0x16, ability 2 is a u16 at 0x1A in what Platinum uses as
padding, base exp at 0x09 is zero and the TM masks at 0x1C are zero. Both of
those moved elsewhere. Hardlove additionally zeroes the EV yields and the wild
held items, which is its own choice rather than hg-engine's.

**Types are Platinum's numbering with one substitution: Fairy is 9**, the dead
`TYPE_MYSTERY` slot, where Oxide put it on the end at 18. Everything else is
identical, and that is measured rather than assumed: decoding all 493 natives
with `9 -> TYPE_FAIRY` applied gives a type pair identical to `res/pokemon` for
**493 of 493**. Two things follow. Hardlove's types are not randomised, so the
earlier note in the pick-list saying they were is wrong and the donor is a
trustworthy source for the 159. And Oxide's twenty Fairy retypings from element
1 agree with Hardlove's exactly, which is a free check on that work.

Base stats, catch rate, gender ratio, hatch cycles, base friendship, exp rate,
egg groups, body colour and the flip flag are all vanilla-format and canonical.
Abilities are the official Generation 5+ ability numbers, which is why they run
past 255 and why element 2 had to widen the field.

## a/0/2/8, member by member

| Member | What | Shape | How it was identified |
|---|---|---|---|
| 7 | hidden abilities | u16 x 1476 | Bulbasaur 34 Chlorophyll, Charmander 94 Solar Power, Butterfree 110 Tinted Lens |
| 8 | base experience | u16 x 1476 | Charmander 62, Charmeleon 142, Charizard 267, the Generation 7 values |
| 9 | icon palette | u8 x 1476 | values only ever 0, 1, 2, which is Platinum's icon palette range |
| 10 | unidentified | u16 x 1076 | only 26 non-zero, values in an index space past 1476; see below |
| 11 | form data | 32 u16 x 1075 | row 38 Ninetales holds 1132, which the pick-list independently fingerprinted as Alolan Ninetales |
| 12 | form to species | u16 x 400 | 3, 6, 6, 9, 15, 18, 65, ... the Mega list in order |
| 13 | form reversion | u16 x 399 | 22 non-zero, values 1 to 6 |

The 1476 personal records are **1076 species at 0..1075 and 400 form records at
1076..1475**. Member 12 maps form record *k* to its base species, and that
record's personal index is `1076 + k`. Member 11 is the reverse: per species, up
to 32 personal indices of its forms. In member 11 the high bit marks a form that
reverts after battle, which is how the Megas and Gigantamaxes are flagged and
the Alolan forms are not. Oxide has neither, so the flagged entries are ignored.

Members 10 and 13 are not needed by the species port and are recorded here only
so nobody re-derives them. Member 10's values sit above 1476, so they index
something other than the personal table; the species it marks are the ones with
vanilla Generation 4 forms plus the Megas.

## Learnsets

One flat blob, `34 * 4` bytes per species, entries of `(u16 move, u16 level)`
padded with `(0xFFFF, 0)`. Two things Platinum cannot take as they are. Move ids
run past 511, which is all `SpeciesLearnsetEntry` can hold, so the packed
`move:9 / level:7` format has to widen. And hg-engine uses **level 0** for an
evolution move, which Platinum has no concept of.

## Evolutions

Nine slots of `(u16 method, u16 param, u16 target)`. Methods 0 to 26 are
Platinum's own `EVO_*` numbering unchanged; anything above is hg-engine's. The
159 pick-list species need ten methods, eight of which Platinum already has, and
these four it does not:

| Method | Seen on | What it is |
|---|---|---|
| 27 | Fomantis to Lurantis at 34 | level up during the day |
| 30 | Sliggoo to Goodra at 50 | level up while it is raining |
| 31 | Eevee to Sylveon, param 9 | level up knowing a move of that type, Fairy here |
| 47 | Primeape to Annihilape, param 20 | use Rage Fist twenty times |

Method 47 has no Generation 4 equivalent and no room to count move uses, so
Annihilape needs a different trigger; that is a decision for the port, not a
port of the donor's value.

**Three natives gain an evolution**: Primeape to Annihilape, Scyther to Kleavor
(method 7, use item 321, the Black Augurite) and Eevee to Sylveon.

**Two donor targets dangle.** Hisuian Sliggoo points at 2804 and Dartrix's
second branch at 2822, both past the end of Hardlove's own 1476 records, because
the table was built against a newer hg-engine. 2804 is Hisuian Goodra, which is
in the pick-list and has to be repointed at Oxide's id. 2822 is Hisuian
Decidueye, which is not in the pick-list, so that branch is dropped and Dartrix's
personality-split evolution collapses to a plain level 36.

Gyarados and Buneary have no extra evolution in the donor at all, so Gyarados M
and Lopunny M are authored rather than imported; the trigger is settled in
`phase4-engine-change-answers.md` Q4.

## Abilities

Banks 720 (names), 721 (uppercase names) and 722 (descriptions), **319 entries
each**, and ids 0 to 123 match Platinum's exactly: 65 is Overgrow, 123 is Bad
Dreams. Ids 124 up are the Generation 5 to 9 abilities in their official order,
with a handful of Hardlove's own on the end past 299.

The 159 pick-list species need 59 ability ids Platinum does not have, 93 of them
in an ordinary slot across 90 species and 84 as a hidden ability. Thirty-one of
the 159 have no hidden ability at all.

## What the numbers are

| | |
|---|---|
| donor species records | 1076 |
| donor form records | 400 |
| donor abilities | 319 |
| donor moves | 924 |
| ability ids the 159 need that Platinum lacks | 59 |
| evolution methods the 159 need that Platinum lacks | 4 |

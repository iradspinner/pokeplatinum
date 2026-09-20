# Phase 4: engine changes, questions for Ian

Written 2026-09-20 at the start of Phase 4. The Phase 1 survey listed hg-engine's
whole menu of optional features but said which ones Hardlove actually switched on
"is not visible from the extraction alone". That is only half true: the toggles
are compile-time, but several of them leave unmistakable marks in the data, and
this pass read them out of the donor ROM directly.

Each question below carries what was measured, so the answer is a judgement about
what Oxide should be rather than a guess about what Hardlove is.

## What Hardlove demonstrably has

Measured from `Hardlove Gold NDS (0.6.9).nds` against the pinned vanilla Platinum:

| | Platinum | Hardlove |
|---|---|---|
| Species records (`a/0/0/2`) | 508 x 44b | 1,476 x 44b |
| Move records (`a/0/1/1`) | 471 x 16b | 924 x 16b |
| **Item records** (`a/0/1/7`) | **446 x 34b** | **2,687 x 36b** |
| **Evolution records** (`a/0/3/4`) | **508 x 44b (7 slots)** | **1,476 x 56b (9 slots)** |
| Ability IDs | u8, max 123 | u16, up to 318 |

Two of those are new information. The item table is six times the size and each
record is two bytes wider, so the item expansion is switched on and is not a
small feature. The evolution record carries nine slots instead of seven and uses
**19 evolution methods Platinum does not have** (27, 28, 30, 31, 33 to 35, 37 to
48), so the Gen 8 evolution-method set is switched on too.

## Already done, so not worth asking about

A good part of hg-engine's menu came across with the base ROM in Phase 3 and is
already in this build: reusable TMs, HMs forgettable, no items in trainer
battles, the EV/IV viewer, uncapped battle frame rate, vitamin EV caps at 252,
the raised shiny odds, Rare Candy chaining and the Repel prompt. The menu is
shorter than it looks.

## The questions

**1. Items: how much of the expansion do you want?**
The table goes from 446 records to 2,687. Some of that is Gen 5 to 9 items, some
is almost certainly padding. Carrying it means the item table, the bag, the save's
bag pockets and every item-indexed table grow, and the save format changes.
Options as I see them: take the whole table; take only items the picked species
and moves actually need (evolution stones, held items, plates); or take none and
keep Platinum's items. **Which?** The species pick-list already names items that
must exist, and all of them are in Platinum already, so "none" is viable.

**2. Evolution methods: the full Gen 8 set, or only what the pick-list uses?**
The pick-list's evolution table needs seven methods Platinum has and a handful it
does not. Hardlove has 19 extra. Taking all 19 is more code in one go but means
later species need no new work; taking only what is used is less code now and a
second pass later. **Which?**

**3. Evolution slots: 7 or 9 per species?**
Hardlove's record holds nine. Platinum's holds seven, and the pick-list notes
Clamperl is already at six of seven. Nine costs a wider record and a rebuild of
`evo.narc`; seven risks running out on a species with many branches. **Which?**

**4. Mega Evolution.** The pick-list includes two alt-evolution "megas"
(Gyarados M, Lopunny M) which are ordinary evolutions rather than in-battle
transformations, so nothing forces real Mega support. Do you want the real
mechanic, or are the alt-evolutions the whole of it?

**5. Hidden abilities.** hg-engine gates these behind a script flag and keeps the
table in `a/0/2/8`. Reading that table is already a Phase 4 prerequisite. Do you
want hidden abilities as a mechanic, or only the widened ability IDs so the new
abilities fit?

**6. Experience formula.** hg-engine offers the Gen 5/7/8 level-influenced
formula as a toggle, and it changes pacing across the whole game. Keep
Platinum's, or take the newer one?

**7. PC boxes and the save format.** 30 boxes, the expanded bag, the expanded dex
flags and the item expansion all change the save layout, and hg-engine notes that
breaks PKHeX compatibility. Are you willing to break save compatibility, and do
you care about PKHeX? If the answer is no to either, several features have to be
cut together rather than one at a time.

**8. Quality-of-life toggles.** Cheap individually, and each is a yes or no:
always-set battle mode; always national dex; transparent textboxes; fast text by
default (the base ROM already defaults text speed to fast); wild double battles;
capture experience; critical capture; static HP bar; restore single-use items
after battle; the friendship evolution threshold; level caps driven by a script
variable; 60 fps outside battle as well as in it. **Which of these do you want?**

**9. Learnset format.** hg-engine widens level-up learnsets to (u16 level, u16
move) with a configurable cap, where Platinum packs both into one u16 and caps
the move id at 511. With 924 moves, moves above 511 cannot appear in a level-up
learnset without this change. It is therefore not optional if any picked species
learns a high-numbered move, which is likely. Confirming rather than asking:
**this one is in unless you say otherwise.**

**10. Followers and overworld sprites.** hg-engine changes the overworld follower
system. Out of scope as far as I know, but worth a yes or no since it affects
overworld sprite handling that the species port touches.

## Battle AI: Ian wants this understood properly

Recorded 2026-09-20 at Ian's request, and it changes how element 6 should be
approached. The AI is not to be treated as a list of eleven fixes to apply and
move on from. Ian wants **a rigorous understanding of how Platinum's trainer AI
actually works**, and is interested in fixing its bugs and making small
deliberate changes to its behaviour.

That means, before any of the eleven `battle_edits` fixes are applied:

- Read `src/battle/trainer_ai/` properly and write down what each scoring
  function does, what the AI flags select, and how the score thresholds interact.
  The references Ian uses are lhearachel's Gen 4 AI gist
  (`ff61af1f58c84c96592b0b8184dba096`), `pokemow.com/Gen4/TrainerAI/` and its
  switching page.
- Get the write-up to the point where a change can be predicted before it is
  made. The eleven fixes are a good test of that: each should be explainable in
  terms of the code before it is applied, not just pattern-matched from a guide.
- Keep bug fixes and behaviour changes separate. A fix restores what the code
  plainly intended; a change makes the AI play differently and is Ian's call.

The eleven fixes stay on the list, but they are the end of this work, not the
start of it. Note that 350 of the carried-over trainers had their AI flags
changed in the base ROM, so the flags themselves are already non-vanilla and the
write-up should say what each flag does.

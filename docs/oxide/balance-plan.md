# Balance plan

This is the balance track's status home. Ian put this session in charge of
balance on 2026-09-22, once element 4 had put most moves and species in the
tree. The file covers what "balanced" means for Oxide, how it gets measured,
the data behind it, and the order of work. Ian answered the scoping questions
the same day, and his answers are recorded below as decisions.

**Where it stands (2026-09-22).** Scoping is done, and the reference data is
pinned outside the repo. Nothing is built yet. The next step is B1, the data
layer. Four small questions for Ian are at the end, and none of them blocks
B1.

## The target

Ian's scale runs from 1 to 10:

| Rating | Game |
|---|---|
| 1 | FireRed |
| 3 | vanilla Platinum |
| 6 | **Oxide's target**: a Drayano hack made very slightly easier |
| 7 | Renegade Platinum (Drayano) |
| 8 | Platinum Redux |
| 9.5 | Hardlove Gold |
| 10 | Platinum Kaizo, Run & Bun, Pokemon Null |

Ian's rulings, 2026-09-22:

- **The 6 is judged as a nuzlocke under Oxide's rules**: hard level caps, no
  bag items in trainer battles, no EVs from battling, and captures by location
  name.
- **The curve ramps up slightly through the first two splits, then holds.**
  Roark's party goes to five Pokemon and Gardenia's to six. This file reads
  that as: Roark's fight sits a little under 6, Gardenia's reaches it, and
  every fight after is scored against 6. Ian can correct that reading.
- **Balance is the whole game, not only the opposition.** It covers trainers
  and AI, level caps, species stats, abilities, learnsets, TMs and tutors,
  item access by split (held items, marts, field items), and weather on
  routes and in gyms. The tracker's Phase 5 level-cap split design, TM pass
  and ability pass are therefore this track's work.
- **Maylene's cap is 39**, as the Level Caps sheet says. The caps are unevenly
  spread, and changing them is in this track's scope.

## What the first look found

**Oxide's gym caps are Renegade Platinum's gym aces.** Each leader's
highest-level Pokemon in Renegade is 16, 26, 33, 39, 44, 53, 56 and 62, and
those are Oxide's eight caps exactly. The level curve therefore comes from a
hack Ian rates 7. Oxide then adds hard caps and the item ban, which Renegade
does not have. Some of the gap to a 6 has to come from somewhere else: rosters,
items, AI, or the player's side.

The first fight of each leader and the Elite Four, read from each hack's data:

| Boss | Vanilla | Renegade | Kaizo | Oxide now |
|---|---|---|---|---|
| Roark | 14, 3 Pokemon | 16, 6 | 16, 6 | 16, 4 |
| Gardenia | 22, 3 | 26, 6 | 28, 6 | 26, 5 |
| Fantina | 26, 3 | 33, 6 | 38, 6 | 33, 5 |
| Maylene | 32, 3 | 39, 6 | 47, 6 | 39, 6 |
| Wake | 37, 3 | 44, 6 | 54, 6 | 44, 6 |
| Byron | 41, 3 | 53, 6 | 65, 6 | 53, 6 |
| Candice | 44, 4 | 56, 6 | 74, 6 | 56, 6 |
| Volkner | 50, 4 | 62, 6 | 84, 6 | 62, 6 |
| Aaron | 53, 5 | 72, 6 | not matched | 72, 6 |
| Cynthia | 62, 6 | 89, 6 | not matched | 78, 6 |

The Kaizo Elite Four and Champion rows are blank because matching by name and
trainer ID picked vanilla leftovers. Platinum Redux is left out for the same
reason, since its lowest-numbered "Gardenia" is a level 83 rematch. So B1 has
to build a checked map from each hack's records to its fights; matching by
name alone is not good enough.

Roark, set by set:

| Version | Party | IVs | Held items | Natures | Moves, in short |
|---|---|---|---|---|---|
| Vanilla | 3 | low | none | rolled | Rock Throw, Stealth Rock, Headbutt |
| Oxide now | 4 | about 27 to 30 | all | rolled | Headbutt, Leer, Constrict, Rock Throw |
| Renegade | 6 | 29 to 30 | all | chosen | coverage: Fire and Thunder Punch, Zen Headbutt |
| Kaizo | 6 | 30 | all, Focus Sash included | chosen | Head Smash, Earth Power, Accelerock |

## What gets measured

Every metric is computed the same way for every hack, from that hack's own
data, per boss fight. The bosses are the gym leaders, rival fights, Galactic
admins and bosses, and the Elite Four and Champion. Filler trainers get the
same metrics, summed per split and weighted lower. In a nuzlocke a filler
trainer can still end a run, though, so the worst filler fight in each split
is reported on its own.

The first group of metrics is structural, cheap, and carries across every
game:

- party size;
- the ace's level against the split's cap, and against the previous boss;
- IVs and EVs;
- whether natures are chosen;
- the share of the party holding an item, and which items;
- the share that is fully evolved;
- base stat totals as a percentile of what the player can own by then;
- the AI flags;
- whether the fight is a double battle, and any weather it starts in;
- a move-quality count: setup, hazards, priority, speed control, recovery,
  and the number of types the party hits super effectively.

The second group scores pressure, which is what decides how hard a fight
plays. The damage calculator already runs on Oxide's data (encounter tool
M8 D5), and its engine also runs on each reference hack's data. It measures a
boss against the **player's side at that split**: every species obtainable
by then, at the cap, with average IVs and a neutral nature. Each one gets the
moves it can know by then (level-up at the cap, plus the TMs and tutors
reachable in that split) and the best held item it can have by then. For each
boss Pokemon, the tool reports:

- the share of the player's side it knocks out in one or two hits while
  moving first;
- the share of the player's side that does the same to it.

Rolled up, the first reads as "how much of what you could bring does this
fight threaten", and the second as "how many answers you have".

The yardstick is shared. Every hack's bosses are scored against **Oxide's**
player side at the matching split, so every score answers the same question:
"if this fight were in Oxide, how hard would it be?" That keeps a trainer's
difficulty separate from differences in each hack's wild encounters, which
is what tuning needs.

The third group is the level curve, for the cap design. For each split, the
tool works out the **natural level**: where a team of a nuzlocke's usual size
ends up after beating every trainer in the split, without grinding, using
Generation 4's experience formula. The cap and the natural level should sit
close together. A cap far above the natural level means grinding; one far
below means experience is wasted and the next split starts under-levelled.
The same curve is computed for Renegade, whose levels Oxide's caps came from.

Player-side levers are scored by what they change in the pressure scores. A
species' stat change, a TM moved one split earlier, an item made available
sooner, or route weather each move the share of the player's side that
answers a fight. That is how the player's side and the trainers' side get
balanced against the same target.

## Reference data

The calculator Oxide vendored (hzla's `Dynamic-Calc-Decomps`, MIT) has a
`backups/` folder, left out when it was vendored. It holds each supported
hack's species, moves and full trainer sets: level, IVs, nature, item,
ability, moves, AI flags and location. The rated hacks' files are pinned at
`~/roms/balance-refs/`, beside the other outside-the-repo copies, with
SHA-256 sums and provenance in `MANIFEST.txt`. They are parsed as JSON and
never run.

| File | Hack | Rating | Trainer sets |
|---|---|---|---|
| `pt.js` | vanilla Platinum | 3 | 1,873 |
| `rp.js` | Renegade Platinum | 7 | 2,823 |
| `platredux.js`, `platreduxhc.js` | Platinum Redux, normal and hardcore | 8 | 2,829 each |
| `hardlove.js` | Hardlove Gold | 9.5 | 1,871 |
| `pkv5h.js` | Platinum Kaizo | 10 | 3,077 |
| `null12.js`, `null.js` | Pokemon Null 1.2 and 1.1 | 10 | 2,282 and 2,203 |
| `run-and-bun-trainer-battles.xlsx` | Run & Bun | 10 | Ian's sheet |

Run & Bun comes from Ian's own sheet, not the calculator. It has one tab per
split, from Brawly to the League, with a block per trainer giving level, held
item, ability, nature and moves. So it is scored structurally, with pressure
where its species exist in Oxide's data. Sacred Gold and Blaze Black 2 Redux
are unrated and left out. FireRed is the scale's floor and needs no data.

Hacks built on other games (Hardlove, Null, Run & Bun) do not share
Platinum's bosses. They line up by milestone: badge number, then rivals and
villain bosses by the badge they fall between, then the Elite Four and
Champion.

## Calibration

The ratings set the weights: the composite score is fitted so that each
reference lands at Ian's rating, and "6" becomes a band of scores per
milestone.

The fit is thin exactly where it matters. Vanilla at 3 is the only anchor
below the target, and the next is Renegade at 7, so the 6 band is interpolated
between them. Two things make that safer. A hack Ian rates 4 to 5 would add a
point (question 3 below). After the Roark and Gardenia splits are tuned, his
playtest of them is a direct reading at the bottom of the ramp, and the band
is corrected to it before the later splits are tuned.

## Tooling

A new tool, `tools/oxide/balance/`, is built in the same way as the encounter
tool:

- a data layer that reads Oxide (trainers, species, learnsets, TMs, items,
  the split map) and each reference into one schema;
- a metrics engine;
- a report per split, with each boss's metrics beside the same fight in the
  references.

Damage comes from the vendored calculator's own engine, run headless in Node
from the vendored copy, so the tool and the calculator Ian uses give the same
numbers. The split map (which map, trainer, item ball, mart and TM falls in
which split) starts from the encounter tool's area and split data. The trainer
side comes from the field scripts that start each battle. Each milestone has
tests and a count anyone can rerun.

The tool does not simulate the AI choosing moves. Platinum's AI is not
Showdown's, and element 6 has documented how it actually picks. So the
pressure scores assume the boss's best move, which is a ceiling, and the
report says so. Ian's playtests remain the final gate. The scores aim the
changes and catch outliers, and they are recalibrated when Ian's feel
disagrees with them.

## Order of work

- [x] **B0, scoping** (2026-09-22). Ian's answers are in, and the reference
  data is pinned.
- [ ] **B1, data layer.** This covers Oxide and every reference in one schema,
  a checked map of each hack's records to its fights, and Oxide's split map
  for trainers, items, marts and TMs. The check: trainer and set counts match
  each source, a sample of fights matches the calculator's own view of them,
  and every Oxide trainer lands in exactly one split.
- [ ] **B2, structural metrics** for every reference and for Oxide as it
  stands. The check: vanilla, Renegade and Kaizo come out in that order on
  almost every metric.
- [ ] **B3, the player's side and pressure.** This covers the pool per split
  (species, moves, items) and the pressure scores. The check: damage agrees
  with the calculator's page and with the in-game roll already waiting on Ian
  (encounter build plan, D5).
- [ ] **B4, the level curve**: the natural level per split, for Oxide and
  Renegade.
- [ ] **B5, calibration** to Ian's ratings, and the target band per milestone.
- [ ] **B6, the audit.** Where every Oxide fight sits today, and every lever
  on the player's side ranked by what it moves.

Then the design passes, in this order. Each proposal goes to Ian before it
lands, and each change is re-scored as it lands.

1. **Level caps.** A redesigned curve, from B4 and the target band. Moving a
   cap moves every wild level in that split, so the encounter track re-runs
   `cli evolve` against the new caps. That is coordinated through the
   Overseer and not done from here.
2. **Item access and TMs.** Which held items, marts and TMs each split
   offers, and how many TMs there are.
3. **Species, abilities and learnsets**, including the base ROM's 228
   duplicated second ability slots.
4. **Weather** on routes and in gyms.
5. **Trainers**, with the bosses first: Roark to five Pokemon, Gardenia to six,
   then each fight into the band. Filler trainers come after.

Trainers can now be given a chosen nature (encounter M8), which removes the
old trade-off between a nature and IVs. One open defect has to be fixed before
the trainer pass uses the field: the packer accepts `NATURE_COUNT`, and that
hangs the game (encounter build plan, QA findings).

## Questions for Ian

None of these blocks B1.

1. Platinum Redux: is the 8 for normal mode or hardcore? The data has both.
2. Null: is the 10 for 1.2 or 1.1?
3. Have you played any hack you would put at 4 or 5? The calculator's data
   also covers, among others, Luminescent Platinum, Sterling Silver, Vintage
   White, Inclement Emerald, Emerald Imperium and Radical Red's normal mode.
   One rated point between vanilla and Renegade would firm up the 6 band.
4. The ramp: does "Roark at 5" mean his party size (as read here, with his
   fight a little under 6), or a 5 out of 10 for his fight?

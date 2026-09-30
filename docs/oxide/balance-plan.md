# Balance plan

This is the balance track's status home. Ian put this session in charge of
balance on 2026-09-22, once element 4 had put most moves and species in the
tree. The file covers what "balanced" means for Oxide, how it gets measured,
the data behind it, and the order of work. Ian answered the scoping questions
the same day, and his answers are recorded below as decisions.

**Where it stands (2026-09-29).** Every score is rescored on the combined
landing branch (`balance-combined-rescore`), and two passes agreed on all
1,030. The census leaves out the test kit, the pool takes the encounter
tool's scripted sources it lacked (the fossils in Fantina's split, Acuity
Cavern's draw in Volkner's), and an item counts from the split the way to
it opens: Surf, the other field moves, the bike, its ramp jumps and
scripted arrivals (the stone correction under the item pass). Doubles
against two trainers at once are rescore units of their own (56 pairs),
and Somnu and Moira at Lake Verity are a story fight (6.2 on Ian's
scale). No story fight moved by 0.3 or more. Then (`balance-retypes-rescore`)
Ian's 17 retypes and three stat slips, field moves on their badge alone,
and the last weather abilities moved to the hidden slot, all rescored and
verified: Volkner's fight reads harder with the Electric/Fighting
Electivire and Electric/Dark Luxray, and the rank correlation with Ian's
ratings is -0.57. Then (`balance-buffs`) the buff review's decisions:
the sheet's slips, section A's junk-ability fixes, section B, and Ian's
second answers (Wormadam's Overcoat, Armaldo's abilities, Donphan,
Tangela, Politoed and Rotom's stats, and Kaizo's numbers for the species
the player cannot catch). The variants were scored in
[the review's scores](reviews/buff-review/scores.md) (no single change
moved a story fight by more than 0.1), and Ian took sections C and D,
Houndoom's line (Houndour evolving at 27) and Talonflame's Gale Wings,
with Haunter and Emolga approved by name as flagged stages; Glaceon's Ice
Scales waits for testing in play. His last answers: one fix each for the
lines whose hidden ability repeated a regular one, Kaizo's Gallade,
Drought hidden for the Slugma line, and halfway buffs for Articuno and
Suicune. All of it is rescored and verified, and landed on `oxide`.

**The scorer under review (2026-09-30, `balance-boxmodel`).** Ian flagged
that the player's side overstated the player, and it did: one of every
species obtainable by the split, each with the two strongest damaging
moves of every type it could learn, every reached TM taught to every
compatible species, and a Choice item or Life Orb in hand. The branch
gives each Pokemon four moves chosen for coverage (at most one taught,
since TMs are single-use), bans the Choice items and Life Orb from the
player's side, and weights every share by a realistic box (the encounter
tool's box simulator, 300 runs a split, stored in `boxshares.json`); the
Kaizo scorer's own box gets the same. Rescored and verified on all 1,030
units. What it showed: a fight's place on Ian's scale comes only from safe
switch-ins, which read the player's bulk, so four moves and the item ban
move no scale reading; the box weighting does, and it predicts Ian's
ratings worse (held-out error 1.52 against the whole pool's 1.36), with no
reading possible below 4.4. Ian chose neither side model (2026-09-30). He
proposed a new measure instead: a fight's difficulty is how easily a
perfect line is found, a plan that wins with no deaths whatever the RNG
does within a luck budget (every secondary status chance against the
player happens; one crit against the player may happen, never two or two
in a row; the trainer's AI picks the move worst for the player among those
it could pick). Step 1 counts how often a random six from a random whole
box has a perfect line; step 2 counts the perfect lines of the box's best
team. Movesets fill in order: best STAB, coverage or a second STAB,
coverage, then the best status move by the status tiers. A separate
session designs and prototypes it blind in `~/oxide-trials/scoring-review/`.
Until its results are in, the scale is not refitted and the average-fight
calibration, the gauntlet list and the Kaizo study's scores are held.
`balance-boxmodel` stays as it is: the four-move limit and the item ban
carry into the new scorer. Next: learnset v3, which needs no fight score,
then the TM pass.

**Where it stood (2026-09-27).** Test.nds is Oxide's base ROM, with Ian's
late boss updates and his sheet's testing teams as the baseline, merged.
The tool knows Ian's two Galactic splits (HQ 60, Galactic 65), the Battle
Zone has come down 18 levels to fit them, and Saturn 2 is scored under his
permanent Trick Room. Done: B1a, B1b, B1d, B1e, B2, B3a, B3b and B4's
tools. B5 has its readings, fits to the references and to Ian's own
ratings of sixteen fights, and his explanations of the fights the scores
misread: safe switch-ins read both best ("What B3b and B5 found", "What
Ian's ratings showed"). Every score is on the combined branch of
2026-09-27 (the calculator's items 22 and 23, the friendship and trade
evolutions, the new grass tables and sources, Heatran out of Stark
Mountain, the Kaizo move data and element 4's partly working moves, the
Sinistea split, the stone gate), and rescores are incremental. The encounter tool's team
builder scores a team through `teamscore.py`. B6 is done ("What B6 found"): the bottom band
is the one- and two-Pokemon ordinary trainers, the hyper-offense is six
fights with their damage spread across each team, and of the player's
levers only caps and map weather move the scores much. The Barry split
(cap 71) and four fixes to the player's side are scored ("The player's
side fixed, and the Barry split"). Next: the design
passes, starting with the learnset study (design pass 3). Its parts 1 and
2 have found Kaizo's patterns as rules ("What parts 1 and 2 found"), and
the generator waits on Ian's word on them. The scores weigh the stone
plan now and read Ian's three Lucas and Dawn fights as story fights, and
the gauntlet proposal (design pass 5) waits on his choice of areas and
two questions.

## The target

Ian's scale runs from 1 to 10:

| Rating | Game |
|---|---|
| 1 | FireRed |
| 3 | vanilla Platinum |
| 6 | **Oxide's target**: a Drayano hack made very slightly easier |
| 7 | Renegade Platinum (Drayano) |
| 8 | Platinum Redux, normal mode |
| 8.5 | Platinum Redux, hardcore mode |
| 9.5 | Hardlove Gold |
| 10 | Platinum Kaizo, Run & Bun, Pokemon Null 1.2 |

**Ian's goals for reaching it** (2026-09-26). Oxide's peak fights are about
right: he is happy with the hardest fights B5 ranks, except perhaps Flint
and Byron. So the 6 is not reached by lowering the peak. The goals are:

1. curb the hyper-offense;
2. more fights in the middle of his fight scale (3 to 6 or 7) and fewer at
   the bottom (0 to 2);
3. bring in the added Pokemon, moves and abilities;
4. a balance pass over everything, so that nothing is comically untuned
   or unfun.

His fight scale is a second scale, separate from the one above: how hard
he can make a fight when he designs one. His ratings of sixteen fights
("What Ian's ratings showed") are on it.

**These goals gate two legendary encounters** (Ian, 2026-09-27). Valor
Cavern and Stark Mountain hold no legendary until the difficulty has risen
enough that more legendary-tier encounters would not inflate the quality
of the player's box. When B6 or a later rescore shows the difficulty where
Ian wants it, this track says so, and the question goes back to him.

Ian named three more comparison points without a number: **Pokemon Odyssey**
as a good match for the target, though it is all double battles with many
type and move changes, and **Pokemon Unbound** and **Pokemon Insurgence** as
very slightly on the easy side. Ian confirmed the numbers this file had put on
them: Odyssey about 6, and Unbound (difficult mode, as he remembers it) and
Insurgence about 5 to 5.5.

Ian's rulings, 2026-09-22:

- **The 6 is judged as a nuzlocke under Oxide's rules**: hard level caps, no
  bag items in trainer battles, no EVs from battling, and captures by location
  name.
- **The curve ramps up slightly through the first two splits, then holds.**
  Roark's party goes to five Pokemon and Gardenia's to six (Ian confirmed
  that the five is a party size, not a rating). So Roark's fight sits a
  little under 6, Gardenia's reaches it, and every fight after is scored
  against 6.
- **Balance is the whole game, not only the opposition.** It covers trainers
  and AI, level caps, species stats, abilities, learnsets, TMs and tutors,
  item access by split (held items, marts, field items), and weather on
  routes and in gyms. The tracker's Phase 5 level-cap split design, TM pass
  and ability pass are therefore this track's work.
- **Maylene's cap is 39**, as the Level Caps sheet says. The caps are unevenly
  spread, and changing them is in this track's scope. The encounter tables stay
  at 38 until the cap redesign lands, and the encounter track then re-runs
  `cli evolve` once against the approved caps. The approved caps go to the
  Overseer, who hands them over.
- **More ordinary trainers should be required** (Ian, 2026-09-22). In the
  base ROM most route trainers can be walked around, and Ian wants that
  changed. It is a design pass of its own (trainer placement and sight
  lines), and B1e measures which trainers are avoidable today so the pass
  has a list to work from and a way to check its result.

Ian's rulings, 2026-09-23, after reading B3a:

- **A Choice item is weaker in play than its score, and Choice items should
  be rare in Oxide.** A Choice item locks its holder into one move, so the
  player can bait the lock, switch in something that walls that move, and
  win from there. B3a's finding that Choice Scarf bosses have almost no
  answers overstates them for that reason. The scores are not expected to
  model switching in full, but every table and report marks the Choice
  holders so the reader can discount them, and says that a Choice-locked
  boss plays weaker than its score. B3b, parked on `wip-balance-b3b`, adds
  one cheap adjustment (answers counting the lock). For the item pass and
  the trainer pass: Choice items are to be quite rare in Oxide, on both
  sides.
- **The rest of B3a's analysis stands.** Ian's next change to the base
  ROM's content was already going to be a slight nerf to Gardenia's
  Roserade. It is recorded here for the trainer design pass, and is not made
  in the balance tooling.

Ian's ruling, 2026-09-25 (`docs/oxide/battle-zone-plan.md` has the detail).
**Superseded** by the two Galactic splits below, HQ at 60 and then Galactic
at 65; the single Galactic split at 64 is kept here as the record.

- **A new split, Galactic, between Candice and Volkner.** It opens straight
  after Lake Acuity and holds the whole Battle Zone (the Fight Area,
  Routes 225 to 230, the Survival and Resort Areas, Stark Mountain) and
  the Galactic fights up to the Distortion World (Veilstone HQ, the Mt.
  Coronet climb, Spear Pillar). The caps are Candice 56, **Galactic 64**,
  **Volkner 68** (up from 62) and League 78. Heatran becomes a draw from the
  legendary pool; the Battleground's rematches are skipped for now and stay
  after the League. The balance tool now keeps Ian's caps itself
  (`fights.json`), since Galactic's and Volkner's run ahead of their bosses
  until the trainer pass.

Ian's answers, 2026-09-25, to the three open questions:

- **The Battle Zone comes down 18 levels**, not 14, to 55 to 60. It sits
  just before what is meant to be **the hardest stretch outside the Elite
  Four: the Galactic fights and the Mt. Coronet climb**, so the zone may
  run a little low. That also answers the curve's shape past Gardenia: it
  holds at the target, with a deliberate peak at the end of the Galactic
  split. By "the Galactic fights" Ian means everything from the Galactic
  Warehouse in Veilstone through the last fight with Cyrus: the warehouse,
  the HQ, the Mt. Coronet climb, Spear Pillar and the Distortion World.
- **IVs and natures matter, but they do not separate the ratings.** They
  make every number harder, and they come close to optimised even in games
  Ian rates 5 or 6. So B5 treats them as a floor Oxide must meet (it does:
  IVs near the ceiling, natures read as picked) rather than as a measure
  that moves a fight up the scale. Priority, speed control and recovery are
  weighted low, as B2 found.
- **B1e reads the routes as Ian played them**: Route 202's three trainers
  cannot be walked around, and Route 203's five, Route 206's nine and
  Route 218's four all can. He found the base ROM had far too few ordinary
  fights outside the gyms and bosses, and wants that addressed; the
  trainer placement pass is where it happens.

Ian's rulings, 2026-09-25, on the Galactic stretch and the base ROM:

- **Two Galactic splits: HQ at 60, then Galactic (the Battle Zone, the
  climb, Spear Pillar, the Distortion World) at 65**, with Volkner at 68.
  The tool knows both (2026-09-25, branch `balance-two-galactic-splits-v2`):
  the Warehouse and the HQ are the HQ split, closing on Cyrus 2; the Battle
  Zone, the climb, Spear Pillar and the Distortion World are Galactic,
  closing on Cyrus 3. The encounter design's split table still has one
  Galactic split at 64, which is the encounter track's to change.
- **The "[TESTING CHANGES]" teams in Ian's Boss Documentation sheet are
  Oxide's baseline.**
- **Test.nds is the base ROM.** The ROM Phase 3 carried over from was
  exported on 2026-08-11; Ian's work from 14 to 31 August (37 trainers, nine
  maps' events, six scripts, seven learnsets, Beautifly's record, the
  trainer names) was only in his DSPRE folder and in Test.nds, exported
  2026-08-31. The switch was carried over on branch
  `base-rom-2026-08-31`. Cyrus 2 and Cyrus 3's testing teams are in no ROM
  and were entered from the sheet. The six gift-house scripts Test.nds
  changed keep Oxide's versions, since Test.nds only reordered their gifts
  or made Sandgem roll, which Oxide already does. Two former dummy slots
  are now real trainers on the map (Officer Argo, Krystal), and the moved
  trainers make four more of them required (40, from 36).

Ian's rulings, 2026-09-27, on the Pocket PC:

- **Attrition lives in gauntlets.** The Pocket PC heals the party and works
  everywhere except in gauntlets: one-way areas the player must clear,
  beating a set number of trainers in a row, before leaving to heal. So
  outside a gauntlet every fight is scored from a healed party, as the
  scores already are, and any proposal that relies on attrition goes in a
  gauntlet. **This track proposes which areas become gauntlets and how
  many trainers each holds**, for Ian (the tracker's Phase 5 "Gauntlets"):
  proposed under design pass 5, "The gauntlet proposal".
- **Every PC loses its extras**: the free Move Reminder, the Online Shop,
  the Teleport System, Happiness Up, the PC move tutors (the shard tutors,
  Blast Burn and its kin and Draco Meteor from five badges) and the
  post-game resets. The tutors out in the world stay as in vanilla, and
  the TM and tutor pass works from them. The player's side reads the three
  shard-tutor houses (38 moves) but not the world's Draco Meteor or
  starter-move tutors, a gap that the tutor pass closes.
- Friendship evolutions move to methods that cannot be ground as easily;
  the encounter track proposes one per line.

Ian's rulings, 2026-09-27, on the Kaizo comparison (`docs/oxide/kaizo-comparison.md`,
"Ian's answers"):

- **Moves**: of Kaizo's numbers, only the report's short list comes in,
  as exceptions to the modern scale; the very large buffs stay out. So
  every setup move goes to 1 to 3 PP (Bulk Up, Cosmic Power, Stockpile,
  Focus Energy, Defend Order, and the new moves' Quiver Dance, Coil, Shell
  Smash, Hone Claws, Work Up, Shift Gear and the rest); the stat-lowering
  status moves take Kaizo's low PP (Screech, Metal Sound, Fake Tears,
  Charm, Feather Dance, Tickle and Captivate at 3 to 6, Sweet Scent at 2);
  every Generation 4 move whose priority changed later takes the modern
  value (Fake Out +3, Extreme Speed +2); Drill Peck, Megahorn, Dragon
  Claw, X-Scissor and Power Whip get the high critical ratio; six weak
  signature attacks (Octazooka, Mirror Shot, Magnet Bomb, Needle Arm,
  Poison Tail, Crush Claw) rise to about 80 to 90; and six mid attacks
  (Hyper Fang, Octazooka, Rock Climb, Sky Uppercut, Double Hit, Dragon
  Rush) go to 100 accuracy. Sleep moves and powders keep their accuracy.
  A cloud job writes the data. For the scores: PP changes nothing (the
  calculator carries none) and nor does the critical ratio (the scores
  leave critical hits out); the power, accuracy and priority changes
  stale only the fights where those moves appear, for an incremental
  rescore.
- **Learnsets** (answer 6 as Ian corrected it the same day): Kaizo's
  level-up lists are studied for when and why each move is given, and the
  rules become a generator that proposes lists inside Oxide's caps; the
  lists are not copied (design pass 3, "The learnset study").
  Strong moves may sit at level 1 on evolved stages, as Kaizo has them,
  which makes each worth a Heart Scale at the Move Relearner. No split has
  a ceiling on coverage power; the rescore judges each move. The move
  pool's first cut (below, design pass 3) goes into the same pass.

Ian's ruling, 2026-09-27: **the five Frontier Brains become optional
bosses**, Dahlia at the Veilstone Game Corner (Maylene's split), Darach at
the Pokemon Mansion (Wake's), Thorton at Fuego Ironworks (Byron's), and
tentatively Argenta at Pal Park (Byron's) and Palmer at the Resort Area's
entrance (Galactic's). Ian builds the teams, and this track scores each
draft as it comes, so he sees where it lands on his fight scale
(`b6.py --draft`, `--trick-room` for Thorton).

The first drafts (2026-09-27, `docs/oxide/frontier-brains.md`) name
species only, so each member is scored at the split's cap with the game's
own default moves for that level, no item and IVs of 30. That reads
softer than a finished team will, so these are a floor:

| Brain | Split (cap) | Safe switch-ins | On Ian's fight scale |
|---|---|---|---|
| Dahlia | Maylene (39) | 0.56 | about 5.3 |
| Darach | Wake (44) | 0.64 | about 4.7 |
| Thorton, under Trick Room | Byron (53) | 0.58 | about 5.1 |
| Argenta | Byron (53) | 0.54 | about 5.4 |
| Palmer | Galactic (65) | 0.21 | about 7.9 |

Dahlia's Wonder Room is not modelled, and Darach's double battle is scored
as singles, as every double is.

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
| Oxide now | 4 | about 27 to 30 | all | read as picked (B2) | Headbutt, Leer, Constrict, Rock Throw |
| Renegade | 6 | 29 to 30 | all | chosen | coverage: Fire and Thunder Punch, Zen Headbutt |
| Kaizo | 6 | 30 | all, Focus Sash included | chosen | Head Smash, Earth Power, Accelerock |

What B1a found, beyond the table above:

- **Every Platinum-based hack keeps Platinum's trainer ids**, the same ids
  Oxide uses (Roark is 246 everywhere), so a fight is looked up by id, not
  guessed. Two hacks need overrides, which `fights.json` records. Kaizo's
  League sits at level 100 in Platinum's rematch slots, after an 84 Volkner;
  the first-fight slots still hold vanilla's sets. Redux swaps the two
  Galactic HQ fights. It also has several level 100 League sets, and the one
  taken as its first run (787 to 791) is a guess until Redux's scripts or
  docs confirm it.
- The calculator's data names the rival "Pkmn Trainer Cedric".
- Oxide's aces match the Level Caps sheet for every boss the sheet lists
  except Barry 2, whose ace is 11 in the tree against 10 in the sheet.
- **Ian's base ROM already uses weather.** 57 map headers differ from
  vanilla on weather. Oreburgh Gym has a sandstorm, Pastoria Gym heavy rain,
  Snowpoint Gym a blizzard, Bertha's room a sandstorm and Flint's room
  ashfall, and several caves lost their fog. Which of these become battle
  weather is for the weather pass to read from the battle code.

What B1b found:

- **The calculator's Hardlove file is out of date.** It holds vanilla
  HeartGold's Clair and League, where Hardlove 0.6.9 has Clair at 77 and its
  League at 82. So Hardlove is read from the donor ROM, the same one the port
  reads, and the file is kept only as a cross-check: Bugsy to Pryce match it
  exactly. **Hardlove's League is Will, Koga, Karen and Lance, with Blue as
  Champion.** Lance has the Elite Four trainer class, Blue the Champion
  class, and both of Bruno's slots hold Zubat placeholders. Ian pointed at
  this ("the other elite four") and confirmed it; he adds that only two
  people have beaten Hardlove as a hardcore nuzlocke.
- **Null's eighth gym is Ex Leader Juan** (level 97), as Ian confirmed; the
  Leader Steven in the same gym is not the gym fight.
- **Hardlove rebalanced species stats**, so its fights are scored with its
  own records from the ROM, not the calculator's (its Alolan Ninetales is
  79/89/79/109/99/100 where vanilla's is 73/67/75/81/100/109). The ROM also
  gave up three details worth keeping. Its species names are cut to ten
  characters, so 14 are spelled out by hand. It has no form names, so the 44
  forms its trainers use are named in a table checked against each form's
  types. And it adds abilities past the 319 it has names for (up to 484),
  which the reader keeps as numbers.
- **The calculator lists a Mega as a seventh set** beside the Pokemon that
  becomes it; Null's leaders all looked like seven-Pokemon parties until the
  146 Mega sets were folded in.
- **Unbound's gym levels are almost Oxide's** (21, 27, 33, 37, 46, 53, 58,
  62 against 16, 26, 33, 39, 44, 53, 56, 62), with three to five Pokemon a
  leader, at a rating of 5 to 5.5. It is the cleanest reading of how much
  party size and roster quality are worth.
- **Run & Bun's sheet is whole for every boss.** 76 filler trainers in the
  later splits have no moves on the sheet itself.

What B1d found:

| Split | Trainers | Item balls | Hidden items | NPC gifts | Shop items |
|---|---|---|---|---|---|
| Roark | 43 | 38 | 12 | 39 | 11 |
| Gardenia | 38 | 30 | 26 | 14 | 20 |
| Fantina | 44 | 32 | 17 | 6 | 5 |
| Maylene | 46 | 28 | 21 | 30 | 91 |
| Wake | 75 | 43 | 38 | 12 | 5 |
| Byron | 66 | 44 | 24 | 16 | 14 |
| Candice | 27 | 17 | 12 | 4 | 5 |
| Volkner | 51 | 41 | 56 | 6 | 11 |
| League | 55 | 20 | 15 | 2 | 10 |

- **Candice's split is the thinnest in the game and Wake's the fullest.**
  Byron to Candice raises the cap by 3 with 27 trainers placed; Maylene to
  Wake raises it by 5 with 75. These are trainers placed, not trainers
  required: Ian notes most of them can be walked around, which is what B1e
  measures before B4 turns them into a level curve.
- **89 of the 92 TMs have a source**, and each has a split. Roark's gym
  gives TM76 in Roark's split, which the check anchors on. The three not
  found (TM08, TM61, TM73) are expected at the Battle Frontier's prize
  counters, which B1d does not read.
- **Only four boss fights start in weather**: Roark in sand, Wake in rain,
  Candice in hail and Bertha in sand. Map headers can only start rain, hail,
  sand or fog; Flint's ashfall starts nothing, and harsh sun and Trick Room
  come only from scripts. Twinleaf's snow means every battle there starts in
  hail.
- 179 trainers no map fields, and all are rematch copies, tag partners,
  unused rival variants or unused slots. The Pokemon Center visitors come
  from a shared script and are placed after the League, unverified.
- **18 filler trainers sit in too early a split** (found in B2). A map takes
  the split in which the player first reaches it, and part of a map can open
  later: Surf on Route 219, the bike on Route 207, Strength in Oreburgh
  Gate's basement, Surf on Route 208, and the far side of Route 210 South. A
  story revisit adds trainers too (the four grunts at Lake Verity). Each is
  above its split's cap, which a hard cap rules out, so B2 leaves them out
  and B1e places them by what the player can reach. The gym leaders'
  rematch copies are also placed, in their gyms' splits, and B2 skips them.

What B2 found, over the 28 story fights and each hack's 13 gym and League
seats (`metrics.py`; `--order` prints the check, `--filler` the filler):

| Hack | Party | IVs | Nature fit | Items | Evolved | Mean BST | Setup | Hazards | Coverage |
|---|---|---|---|---|---|---|---|---|---|
| Oxide | 5.7 | 28.7 | 0.74 | 1.00 | 0.91 | 499 | 0.31 | 0.23 | 15.3 |
| Vanilla (3) | 4.0 | 22.9 | 0.30 | 0.22 | 0.73 | 468 | 0.38 | 0.15 | 12.5 |
| Unbound (5.25) | 4.6 | 31.0 | 0.41 | 0.47 | 0.88 | 492 | 0.85 | 0.46 | 13.8 |
| Renegade (7) | 6.0 | 29.8 | 0.91 | 1.00 | 0.88 | 492 | 0.69 | 0.54 | 14.9 |
| Redux (8) | 6.0 | 16.3 | 0.87 | 1.00 | 0.86 | 533 | 1.54 | 0.15 | 15.7 |
| Hardlove (9.5) | 6.0 | 31.0 | 1.00 | 1.00 | 0.90 | 530 | 1.15 | 0.62 | 15.5 |
| Kaizo (10) | 6.0 | 30.4 | 0.55 | 1.00 | 0.92 | 534 | 1.46 | 1.00 | 15.5 |
| Null (10) | 6.2 | 30.6 | 0.85 | 1.00 | 0.99 | 548 | 2.00 | 0.85 | 15.7 |

Setup and hazards are moves per party; coverage is how many types the
party's moves hit super effectively (17 in the Platinum-based hacks, 18
elsewhere). Nature fit is the share of natures that read as picked: one
that raises something and lowers neither the attacking stat the Pokemon
uses nor its Speed (a slow Pokemon may trade Speed), and raises one of
those or lowers the attacking stat it does not use. Chance gives 8 in 25.

- **Oxide's bosses already match Renegade's on structure.** Every gym and
  League Pokemon holds an item, IVs are near the ceiling, and base stats,
  evolution and coverage are level with or just above Renegade's. Oxide is
  lighter in three places: one Pokemon fewer at Roark (4), Gardenia and
  Fantina (5 each), and about half Renegade's setup and hazard moves. So the
  roster alone does not explain a 6 against Renegade's 7. With hard caps and
  the item ban on top, B3's pressure scores are what should say where the
  gap to 6 comes from.
- **Oxide's natures read as picked**: 0.74 at the bosses and 0.6 to 0.8 in
  filler, against 0.32 for vanilla, whose natures roll. The base ROM varies
  each Pokemon's IV value (Roark's Nosepass 250, Geodude 245), and in
  Generation 4 that value feeds the nature, so these were very likely
  chosen that way. Renegade's filler reads as rolled (0.35); only its bosses
  are picked.
- **The structure metrics do not separate a 7 from a 10.** Party size,
  items, IVs and coverage are at the ceiling from Renegade up; what grows
  from 7 to 10 is level, base stats, setup and hazards. Unbound's 5.25
  shows up as smaller parties and half its Pokemon without items.
- **The plan's check held on nine of fourteen metrics.** Vanilla, Renegade
  and Kaizo come out in order on party size, ace and mean level, items,
  evolution, base stats, setup, hazards and coverage. They do not on IVs
  (Renegade and Kaizo are both at the ceiling, and Kaizo's Barry 1 keeps
  vanilla's zeros), natures (Kaizo picks less often than Renegade, 0.57
  against 0.67 over the story fights), and priority, speed control and
  recovery, which Kaizo's bosses carry less of than Renegade's. Those five
  measure style, not strength, and B5's fit should weight them low.
- **Filler compares by id only for vanilla, Renegade and Redux.** Renegade
  keeps all but one of Platinum's filler ids, Redux loses 81 of 369 to other
  trainers, and Kaizo reuses 252 of them, some at level 90 to 100, so
  Kaizo's filler needs its own map before it can be read. Oxide's filler
  runs one Pokemon smaller than Renegade's (1.3 to 2.4 against 1.8 to 3.3 a
  trainer) with higher IVs and picked natures.
- Vanilla's calculator file lists no moves for 487 of its 1,873 sets
  (default moves); `metrics.py` fills them from vanilla's learnsets the way
  the game does. One Unbound move, Leech Fang, is in no table.

What B1e found (`required.py`; `world.py` reads the collision maps). The
model follows the game's own rules for sight (a straight line up to the
trainer's range, stopped by any solid tile or object), ledges (one way) and
field moves (Surf from Byron's split, the bike from Fantina's, and so on,
each dated from where its HM is found and which badge allows it). The story
path is a hand table of 33 crossings, and a trainer counts where the player
first reaches it:

| Split | Trainers met | Required | Avoidable |
|---|---|---|---|
| Roark | 14 | 3 | 11 |
| Gardenia | 27 | 7 | 20 |
| Fantina | 26 | 3 | 23 |
| Maylene | 22 | 5 | 17 |
| Wake | 13 | 4 | 9 |
| Byron | 24 | 4 | 20 |
| Candice | 21 | 7 | 14 |
| Volkner | 11 | 1 | 10 |
| League | 13 | 2 | 11 |

- **About one trainer in five on the story path is required**: 36 of 171.
  Route 202's three are (traced by hand on its collision map: the ledges
  funnel the player past each one in turn); Route 203's five, Route 206's
  nine and Route 218's four are all avoidable. So Ian's sense that most
  route trainers can be walked around holds, and the placement pass has a
  list to work from.
- **228 trainers are outside the model.** 92 are on maps the story does not
  send the player through (Routes 211, 212 and 219 to 221, the post-game
  Routes 224 to 230, and a few buildings), 43 are in the seven gyms with moving parts, and 93 are in
  multi-floor places (Galactic HQ, Victory Road, Mt. Coronet, Iron Island's
  other rooms, Wayward Cave, the Lost Tower). Only Roark's gym is static
  enough to read, and it comes out with both trainers avoidable, which the
  flat model may get wrong (the gym has raised floors).
- **B1e places 13 of B2's 18 late visits** in the split where the player
  first reaches them, each under that split's cap: Route 207's six in
  Fantina's, the Lake Verity grunts in Candice's, the Route 210 South ninja
  boys in Byron's. The other five sit behind Surf or Rock Climb on routes
  the story never sends the player back to (Route 219's tubers, Route 208's
  Cody and Alexander, Oreburgh Gate's basement), so they are optional.
- The model reads the field flat: bridges are one level, and a trainer that
  turns or walks is taken to see every way it can face, from where it
  starts. The report names both per map. Story blockers other than Route
  210's Psyduck are taken as gone.

What B3 found (2026-09-23; `pressure.py --report` prints the table). The
calculator's engine runs headless in one Node process (`calc_headless.js`).
It loads the engine files the page loads, in the page's order, under the
page's own `require` shim, and repeats only the steps of the page's loader
that touch the engine, lifting the move-merging helper out of
`initialize.js` itself. It gives D5's five ranges exactly, and Crunch into
Bronzor comes out 42 to 50, which only this fork's chart gives. All 28
fights ran in about three minutes over nine one-process runs, the longest
(the League) 40 seconds.

The player's side (`pool.py`) takes every species caught or received by a
split's end, from the encounter tables (land, day and night, water once the
rod or Surf is in hand, honey trees from Gardenia's split) and
`pokemon-sources.csv`, plus every evolution reached at the cap by the
encounter tool's own rule. Each is at the cap with IVs of 15, no EVs, a
neutral nature and its first ability, knows every damaging move its line
learns by the cap plus the TMs and tutors reachable by then, and holds the
strongest damage item the split offers.

| Split | Cap | Species | Items held by then |
|---|---|---|---|
| Roark | 16 | 104 | 18 |
| Gardenia | 26 | 185 | 32 |
| Fantina | 33 | 257 | 40 |
| Maylene | 39 | 338 | 72 |
| Wake | 44 | 390 | 84 |
| Byron | 53 | 416 | 99 |
| Candice | 56 | 430 | 105 |
| HQ | 60 | 431 | 108 |
| Galactic | 65 | 436 | 120 |
| Volkner | 68 | 436 | 121 |
| League | 78 | 436 | 124 |

Threat is the share of that side a boss Pokemon knocks out within two
turns while moving first; answers is the share that does the same to it.
Each is the mean over the fight's Pokemon, and the last two columns are its
most threatening Pokemon and its least answered one.

| Fight | Threat | Answers | Worst threat | Fewest answers |
|---|---|---|---|---|
| Barry 1 | 0.00 | 0.96 | 0.00 | 0.92 |
| Lucas and Dawn 1 | 0.00 | 0.79 | 0.00 | 0.72 |
| Barry 2 | 0.01 | 0.63 | 0.03 | 0.51 |
| Roark | 0.14 | 0.16 | 0.42 | 0.04 |
| Mars 1 | 0.01 | 0.37 | 0.03 | 0.09 |
| Gardenia | 0.66 | 0.06 | 0.89 | 0.03 |
| Jupiter 1 | 0.13 | 0.22 | 0.20 | 0.09 |
| Lucas and Dawn 2 | 0.30 | 0.15 | 0.56 | 0.01 |
| Fantina | 0.53 | 0.09 | 0.89 | 0.00 |
| Barry 3 | 0.18 | 0.46 | 0.38 | 0.32 |
| Maylene | 0.70 | 0.20 | 0.81 | 0.07 |
| Barry 4 | 0.48 | 0.13 | 0.84 | 0.03 |
| Wake | 0.74 | 0.07 | 0.98 | 0.00 |
| Cyrus 1 | 0.38 | 0.35 | 0.56 | 0.23 |
| Barry 5 | 0.55 | 0.19 | 0.91 | 0.04 |
| Byron | 0.34 | 0.21 | 0.56 | 0.15 |
| Saturn 1 | 0.52 | 0.24 | 0.80 | 0.08 |
| Mars 2 | 0.37 | 0.14 | 0.85 | 0.04 |
| Candice | 0.66 | 0.12 | 0.93 | 0.03 |
| Cyrus 2 | 0.45 | 0.12 | 0.81 | 0.04 |
| Saturn 2 | 0.40 | 0.19 | 0.83 | 0.00 |
| Mars and Jupiter | 0.31 | 0.33 | 0.70 | 0.06 |
| Cyrus 3 | 0.52 | 0.23 | 0.82 | 0.12 |
| Volkner | 0.65 | 0.16 | 0.90 | 0.02 |
| Lucas and Dawn 3 | 0.28 | 0.39 | 0.80 | 0.03 |
| Barry 6 | 0.54 | 0.24 | 0.92 | 0.05 |
| Aaron | 0.59 | 0.17 | 0.76 | 0.08 |
| Bertha | 0.50 | 0.31 | 0.76 | 0.02 |
| Flint | 0.69 | 0.14 | 0.92 | 0.04 |
| Lucian | 0.62 | 0.27 | 0.94 | 0.03 |
| Cynthia | 0.68 | 0.13 | 0.90 | 0.01 |

Both tables were recomputed on 2026-09-27 for the combined branch (the
calculator's item 23, the friendship and trade evolutions, the new grass
tables and sources, Heatran out of Stark Mountain, then the Kaizo move
data and element 4's partly working moves, and the stone plan's and the
Underground's item removals, which cut the items each split holds, then
Ian's Sinistea split, which adds a species to every split from Fantina's,
then the stone gate, which takes each stone evolution where its stone is
first in reach), which moves no Oxide fight by more than 0.03; before that on 2026-09-26 for the calculator following the
engine's computed powers (the encounter track's item 22), which moves no
Oxide fight by more than 0.002 and leaves both tables as they were; before
that the same day for the modern move values, the
calculator's Oxide profile (element 5's damage abilities, the staples
rulings, the dual-type order) and B5's item moves; before that on 2026-09-25 for the encounter track's scarcity
pass (strong lines made scarce and the pick list at 493 species, which
grows every side, Roark's from 90 to 105 species and the League's from 364
to 439, and moves no fight by more than 0.03); before that for Ian's water ruling (seventeen
water lines back in the wild, which grows the later sides by up to 36
species and moves no fight by more than 0.02); before that for the encounter track's second
gift pass (Ian's weaker gifts, and several lines taken out of the wild),
which shrinks each side by one to four species and moves no fight by more
than 0.01; and before that for Ian's two Galactic splits, and once honey trees became one
table per badge count, each opening in its own split (the encounter track's
change; a split's side moves by one or two species). Before that they were
recomputed for Ian's baseline teams from
Test.nds and his sheet (which move Saturn 1, Mars 2, Candice and the four
Galactic fights), for the Galactic split and the
encounter track's recast tables (Roark's side went from 92 to 91 species
and Gardenia's from 140 to 142 after its one-spot fold, and Byron's and
Candice's rose by two). The HQ fights are scored at 60, the
Galactic fights at 65 and Volkner at 68, so they read softer than before: Volkner's threat fell
from 0.75 to 0.65, because the player is now scored at 68 against his
team's 62. That is the gap the trainer pass closes, not a change in his
fight. These are raw scores, not ratings: B5 turns them into a band by
scoring the reference hacks the same way. What they already show:

- **Gardenia is the largest step in the game.** Roark's fight threatens 14
  percent of the side and Gardenia's 68, level with Cynthia's 68. Her
  Roserade and Breloom each knock out 90 percent of the side within two
  turns while moving first, and 3 percent answers Roserade. The plan wants Gardenia to reach
  the target and the curve to hold after; whether 0.68 is the target is
  B5's to say, but nothing later climbs as steeply.
- **Choice Scarf and rain leave bosses with no answer.** Nothing at the cap
  outspeeds a scarfed boss, so only priority answers Wake's Poliwrath,
  Candice's Mamoswine, Volkner's Electivire, Bertha's Gliscor or Cynthia's
  Lucario (2 percent or less each). Pastoria Gym's rain doubles Floatzel's
  and Ludicolo's Speed through Swift Swim, and they come out at 1 percent
  and under.
- **Byron is soft between two peaks**: 0.34 against Wake's 0.74 and
  Candice's 0.66. The admins' first fights (Mars 1, Jupiter 1) and Barry 3
  are light too.
- **Early fights in a split read too easy**, because the player is scored
  at the split's cap: Barry 1 is level 5 against a side at 16. B4's natural
  levels should replace the cap for fights before a split's end.
- **Five moves got no number from the calculator's Generation 4
  mechanics** until the encounter track's Oxide profile (2026-09-26):
  Electro Ball, Heavy Slam, Psywave, Super Fang and Trump Card. All five are
  scored now. Since the encounter track's item 22 the calculator also
  follows the engine's computed powers (Electro Ball from the Speed ratio,
  Stored Power, Power Trip, Hard Press, Last Respects, Grav Apple under
  Gravity, Pika Papow and Veevee Volley), and hits with Freeze-Dry and
  Flying Press as plain moves, as the engine does until the main track
  gives them their type rules. Rescored for it, no fight moved by more than
  0.003 on any reading, except two reference Volkners that carry Flying
  Press or Freeze-Dry.

What the scores leave out, so they read as a ceiling for the boss:
accuracy, secondary effects, status and setup, switching, defensive items
other than a boss's Focus Sash, and the AI's real choice of move. A
charging move counts two turns a hit and a recharging one a turn between
hits. Every species counts once, so the weak unevolved stages early in the
game pull the answers down. Moves that need a condition first (Dream
Eater, Fake Out, Counter and the like) and the player's Explosion and
Hidden Power are left out; `pool.py` lists them.

B3's check, as far as it goes. The headless engine agrees with D5's figures
for the page, and those agree with a hand calculation of the Generation 4
formula. The page itself was not driven on this CPU, since a headless
browser is many processes. The calculator now applies a dual type's two
factors in the game's order, so Crunch into Bronzor comes out 43 to 51, as
the game gives (2026-09-26).

**The Battle Zone's re-levelling** (2026-09-25; Ian chose 18 off). The
tracker asked for the zone's trainers to come down from about 75 to
Galactic's cap of 64. Elsewhere a split's filler sits a median 4 to 10
levels under its cap (the League 15), and the zone sat 9 to 14 over it:

| Where | Trainers | Levels now | With 18 off |
|---|---|---|---|
| Routes 225 and 230 | 14 | 73 to 74 | 55 to 56 |
| Routes 226, 228, 229 | 16 | 73 to 77 | 55 to 59 |
| Route 227 | 4 | 76 to 78 | 58 to 60 |
| Stark Mountain, with Mars and Jupiter | 19 | 77 to 78 | 59 to 60 |
| Buck, the player's partner at Stark Mountain | 1 | 78 | 60 |

Every level of every zone trainer above the cap comes down 18. That keeps
each party's spread and the routes' order, and puts the zone at the usual
filler depth, 4 to 9 under the cap, just ahead of the Galactic fights Ian
means to be the hardest stretch before the League. The one trainer already
under the cap (Dragon Tamer Keegan on Route 228, 57) stays. So does Volkner
and Flint's tag battle at the Fight Area (74 to 75): once the main track
gates it behind the Beacon Badge it is a League-split fight, where 75
already fits a cap of 78. Until that gate lands, `splits.py` still counts
it in Galactic. **Done on 2026-09-25**, on branch
`balance-battle-zone-relevel-v2`: 139 levels in 54 trainer files, levels
only. The importer's TRAINERS_DIVERGED leaves those levels alone and
reports the 54 as diverged; with their entries removed it would carry all
54 back, 16 through its party-rewrite path. At Galactic's cap of 65 the
zone sits 5 to 10 under, medium hard.

What B3b and B5 found. Every reference hack's bosses are scored against
Oxide's side in the same seats, each Pokemon with its own game's stats and
moves (`refpressure.py`), and `calibrate.py --report` sets the readings
beside Ian's ratings of the hacks and of Oxide's own fights. The figures
here are from 2026-09-26, after the scarcity pass, the modern move values,
the calculator's Oxide profile and its computed powers (item 22); two runs
agree exactly.

B5 adds readings beside B3's, whose own numbers stay as they were
(`pressure.py` says how each is worked out):

- threat by chance: threat counted by each hit's chance to land, with
  self-lowering moves hitting softer after the first use;
- answers, baiting counted: the share of the side that beats a boss
  Pokemon one on one from a free switch-in, and for a Choice holder also
  after baiting its lock, since the AI's pick against a given lead is
  fixed (Volkner); an "after setup" variant keeps only answers that also
  beat it after one use of its setup move (Byron's Metagross);
- safe switch-ins ("safe"): the share of the side that at most one boss
  Pokemon knocks out in one hit, low when a team doubles up its coverage
  so that baiting one Pokemon draws in another with the same answer
  (Saturn 2, Cyrus 3), high when it shares a weakness (Mars 2);
- tactics: a tally of what no damage score sees (setup, Baton Pass,
  hazards, Explosion, status, evasion, recovery, pinch berries).

Bosses holding an item also keep Natural Gift and Fling, as one hit each.
A "predictable" reading, from how the AI picks moves, ran backwards
against Ian's ratings: it measured how much of a team's time goes to
attacking. It stays in `pressure.json` but is not read as difficulty.
Critical hits, and so the new rates and Keen Eye, are left out of every
score, as are all chance effects.

Over the thirteen seats every hack fills (the gyms, the Elite Four and the
Champion):

| Hack | Ian's rating | Threat by chance | Answers, baiting counted | Safe switch-ins | Tactics |
|---|---|---|---|---|---|
| Oxide today |  | 0.57 | 0.31 | 0.37 | 4.4 |
| Vanilla | 3 | 0.15 | 0.80 | 0.93 | 2.8 |
| Unbound, difficult | 5.25 | 0.51 | 0.28 | 0.62 | 4.4 |
| Renegade | 7 | 0.54 | 0.31 | 0.33 | 6.5 |
| Redux | 8 | 0.69 | 0.09 | 0.25 | 4.8 |
| Redux hardcore | 8.5 | 0.74 | 0.06 | 0.23 | 4.7 |
| Hardlove | 9.5 | 0.68 | 0.18 | 0.33 | 6.0 |
| Kaizo | 10 | 0.77 | 0.03 | 0.07 | 6.6 |
| Null | 10 | 0.92 | 0.01 | 0.01 | 5.7 |
| Run & Bun | 10 | 0.84 | 0.04 | 0.13 | 4.9 |

**Safe switch-ins read Ian's ratings best.** Its rank correlation with
the hacks' ratings is minus 0.93, level with the damage readings, and one
line fits them better than any damage line does:

```
rating = 10.5 - 8.1 x safe switch-ins, R squared 0.92
rating = 5.7 + 4.8 x (threat by chance - one-on-one answers), R squared 0.88
```

On the first, Oxide's gyms and League sit at about 7.5, and a 6 needs safe
switch-ins at about 0.56 against Oxide's 0.37; on the second, at about
7.3. Either way Oxide's gyms and League sit a point or more over the 6,
level with Renegade. Since Ian is happy with the peak fights (2026-09-26),
that gap is closed by the rest of the game, the middle and the floor, not
by softening the peak. The damage line read Unbound 1.6 too hard; the safe line reads
it within 0.3, since Unbound's teams leave far more room to switch.
Hardlove still reads 1.7 soft, most likely because the calculator does not
give its bosses' newer abilities to Pokemon from another game.

Seat by seat, safe switch-ins against the two references nearest a 6:

| Seat | Oxide | Unbound (5.25) | Renegade (7) |
|---|---|---|---|
| Roark | 0.81 | 0.83 | 0.61 |
| Gardenia | 0.37 | 0.96 | 0.46 |
| Fantina | 0.61 | 0.71 | 0.59 |
| Maylene | 0.30 | 0.92 | 0.29 |
| Wake | 0.32 | 0.48 | 0.48 |
| Byron | 0.24 | 0.51 | 0.11 |
| Candice | 0.34 | 0.59 | 0.24 |
| Volkner | 0.35 | 0.70 | 0.27 |
| Aaron | 0.48 | 0.55 | 0.33 |
| Bertha | 0.38 | 0.47 | 0.17 |
| Flint | 0.22 | 0.50 | 0.26 |
| Lucian | 0.21 | 0.43 | 0.31 |
| Cynthia | 0.18 | 0.40 | 0.22 |

Oxide leaves fewer safe switch-ins than Renegade at Gardenia, Wake,
Flint, Lucian and Cynthia, and more at Roark, Byron, Candice, Volkner,
Aaron and Bertha. Against Unbound, Oxide is tighter at every seat.

What Ian's ratings showed. Ian rated sixteen fights he has played in the
base ROM on 2026-09-25, on his fight scale: how hard he can make a fight
when he designs one, not the scale he rates whole games on (he set the two
apart on 2026-09-26). The fits below translate the readings onto that
fight scale; the game scale's 6 is the question above (`calibrate.py`,
IAN_RATINGS); he fought the Elite Four and Cynthia only blind, so they are
left out, and his "Mars/Jupiter Double" is the Spear Pillar tag battle.

| Fight | Ian | Threat by chance | Answers, baiting counted | Safe switch-ins | Tactics |
|---|---|---|---|---|---|
| Mars and Jupiter, Spear Pillar | 9 | 0.31 | 0.59 | 0.50 | 12 |
| Cyrus 3 | 8.5 | 0.50 | 0.26 | 0.24 | 5 |
| Saturn 2 | 8.5 | 0.39 | 0.35 | 0.36 | 7 |
| Candice | 8.5 | 0.65 | 0.18 | 0.34 | 9 |
| Wake | 8 | 0.74 | 0.19 | 0.32 | 2 |
| Maylene | 8 | 0.69 | 0.20 | 0.30 | 2 |
| Officer Hesperid, Lake Valor | 7 | 0.44 | 0.43 | 0.20 | 8 |
| Byron | 7 | 0.34 | 0.17 | 0.24 | 5 |
| Saturn 1 | 6.5 | 0.52 | 0.33 | 0.43 | 6 |
| Fantina | 6 | 0.53 | 0.25 | 0.61 | 5 |
| Barry 4 | 6 | 0.48 | 0.33 | 0.63 | 7 |
| Cyrus 1 | 5 | 0.38 | 0.54 | 0.60 | 5 |
| Mars 2 | 5 | 0.37 | 0.37 | 0.60 | 10 |
| Gardenia | 5 | 0.66 | 0.17 | 0.37 | 5 |
| Volkner | 3 | 0.58 | 0.51 | 0.35 | 4 |
| Roark | 2 | 0.14 | 0.21 | 0.81 | 4 |

Over the fifteen single battles, safe switch-ins correlate with his
ratings at minus 0.64 (minus 0.67 before the Galactic finales); the
damage readings sit between 0.27 and 0.35 either way, and the tactics
tally at 0.17. Safe switch-ins alone predict a rating it was not fitted on to
within 1.7 points, against a spread of 1.9 in his ratings, and no pair or
triple of readings does better on a fight held out. The line is about
9.4 minus 7.4 times safe switch-ins. Its misses say what is still
outside:

- **Volkner** reads 6.8 against Ian's 3. Baiting his three Choice locks
  shows in the answers (0.51, among the most of any fight), but not in
  safe switch-ins.
- **Gardenia** reads 6.7 against 5, the stage: Ian's scale rises through
  the game (later fights rate higher, correlation 0.42), and the scores
  are relative to each split's side by design.
- **Candice and Saturn 2** read 6.9 and 6.8 against 8.5, and Spear Pillar cannot
  be read at all, since the tool plays a double battle as singles without
  the partner. For those three, Ian's ratings are the measure.

The bellwethers now sit where Ian put them. Officer Hesperid at Lake
Valor leaves the second fewest safe switch-ins of all thirty-three fights,
where every damage reading had her in the bottom half. Volkner has the
eighth most answers once baiting counts. Maylene stays near the top on
damage and eighth on safe switch-ins: her fight is hard, but a player can
read it turn by turn.

The fights that leave the fewest safe switch-ins, so the hardest by this
reading, with Ian's rating where he has one:

| Fight | Safe switch-ins | Answers, baiting counted | Ian |
|---|---|---|---|
| Cynthia | 0.18 | 0.31 | not rated |
| Officer Hesperid, Lake Valor | 0.20 | 0.43 | 7 |
| Officer Hesperid, Mt. Coronet | 0.21 | 0.45 | not rated |
| Lucian | 0.21 | 0.48 | not rated |
| Flint | 0.22 | 0.42 | not rated |
| Byron | 0.24 | 0.17 | 7 |
| Cyrus 3 | 0.24 | 0.26 | 8.5 |
| Maylene | 0.30 | 0.20 | 8 |
| Wake | 0.32 | 0.19 | 8 |
| Candice | 0.34 | 0.18 | 8.5 |
| Volkner | 0.35 | 0.51 | 3 |
| Saturn 2 | 0.36 | 0.35 | 8.5 |
| Gardenia | 0.37 | 0.17 | 5 |

So the trainer pass reads safe switch-ins first, with answers (baiting
counted) and the tactics list beside it, translated onto Ian's fight scale
by the line above (about 9.4 minus 7.4 times safe switch-ins): a fight at
safe switch-ins of 0.94 or more sits at 2 or under, one at 0.45 to 0.85
between 3 and 6.

**Ian's explanations** (2026-09-25), for the fights where his rating and
the scores parted. They are the design reasoning the trainer pass works
from, so they are kept here in brief.

- **Gardenia (5)** is hard for a second gym, and the scores agree once the
  stage is counted. Whatever leads into Cherrim is countered by Lumineon,
  which nothing answers yet: Aqua Tail hits hard even in sun, it outspeeds
  almost everything, Swagger has no cure because no Persim Berry is in
  reach, Silver Wind can raise every stat, and Natural Gift is a boosted
  Fire move into its counters. Breloom's Rock Tomb has to be baited,
  Roserade hits hard, and Shiftry's sun Solar Beam, Natural Gift and Feint
  Attack punish its answers. "It's the lack of good answers, and
  everything is awkward."
- **Volkner (3)** is easy for three reasons. Magnezone, Luxray and
  Electivire hold Choice items, so each can be baited into a move
  something takes for free (an Electric move into a Ground type, Tri
  Attack or Cross Chop into a Ghost, Giga Impact into Protect). Jolteon
  and Rotom share Electric and Ghost coverage, and Rotom's Leaf Storm
  weakens itself. Lanturn, sash and all, has Lanturn's stats: Ian's
  Empoleon came in on Ice Beam and Earthquaked through Thunder. This fight
  is why Choice items are now to be nearly entirely gone.
- **Mars and Jupiter at Spear Pillar (9)** cannot be planned past the first
  turn or two, because Barry's moves are not the player's. Both leads
  resist everything Barry's Snorlax does, and Solrock and Lunatone can
  screen, flinch, raise every stat or crit on turn one. A locked Skuntank
  that the player walls simply beats on the partner instead. Spiritomb's
  Pursuit punishes switches, Toxic Spikes and Fake Out change every switch,
  and the Curse Bronzong stalls behind them: more than the sum of its
  parts. Ian lost four Pokemon both times he played it.
- **Saturn 2 (8.5)** is built to resist baiting: most attacking types sit
  on two Pokemon, so baiting one draws another with the same answer
  (Earthquake on Rhyperior and Wailord, Rhyperior's Aqua Tail). Every
  Pokemon hits hard and none holds a Choice item; Wailord's Water Spout
  kills any switch-in; Cresselia (Moonlight, Calm Mind, Charge Beam) and
  Wailord (Aqua Ring, Leftovers) stall. It needs slow Pokemon the player
  may not have kept. Uxie and Toxicroak are the weak part; the Wailord,
  Cresselia and Rhyperior core is the fight.
- **Cyrus 3 (8.5)** is Saturn 2 turned up. Four Pokemon carry Rock and
  Ground, near-perfect coverage together, so almost anything can be
  baited in; Gyarados' four moves are resisted by nothing in the game.
  Each Pokemon has its own threat: a fast Swagger Salamence with a King's
  Rock and three flinching moves, a Curse and Explosion Regirock with Stone
  Edge, a fast Life Orb Flygon with U-turn and Draco Meteor, Heatran's
  Magma Storm trap and Ancient Power, and Oxide's buffed Dusknoir, slow
  enough that Payback hits hard, with Will-O-Wisp, a Lum Berry and
  Levitate. Ice is its weakness, and every Pokemon in the back carries a
  Rock move for it.
- **Byron (7)** is where Ian named the principle. A fight is hard when
  the plan cannot be sure of its outcome. Against Empoleon, a player who
  knows which of its moves hurts most knows it will use it. Metagross may
  use Agility at any point, and if nothing in the box beats a +2 Speed
  Metagross, the whole fight becomes never letting it. The same goes for
  Forretress's Explosion, Bastiodon's Metal Burst (it must be knocked out
  in one hit), Magnezone's Mirror Coat behind a Focus Sash, and Sandstorm
  and Toxic Spikes changing the knockout sums.
- **Mars 2 (5)** fails on coverage. Purugly hurts only with Slash, Sucker
  Punch and Fake Out, so a Ghost walls it; Mesprit has only Psychic and
  U-turn; Bronzong's Heatproof set leaves Earthquake good against both it
  and Luxray, the team's only Ground-weak pair with no Levitate or Flying
  cover; Delcatty and Umbreon hit weakly. "A box check": it needs specific
  answers, but it has no awkward baiting and little setup that matters.

## What B6 found (2026-09-27)

B6 scores every ordinary trainer the player meets (428, 40 of them
required) and each story fight under one change at a time
(`b6.py --report`; all 463 scores verified by a second run). Every fight
is placed on Ian's fight scale by the line above, now 9.4 minus 7.4 times
safe switch-ins. The line bottoms out at 2.1: a party whose Pokemon never
double up on a knockout leaves every switch-in safe. So the bottom band
(0 to 2) is safe switch-ins of 0.94 or more.

**Goal 2, more fights in the middle and fewer at the bottom.** The story
fights are mostly in the middle already. Six sit at the bottom (Barry 1,
2 and 3, Mars 1, Jupiter 1, and Lucas and Dawn 1), and seven at the top (Byron, Cyrus 3, Flint,
Lucian, Cynthia and both Hesperid fights, 7.6 to 8.1). The ordinary
trainers are where the bottom is:

| Split | Bottom (0 to 2), all / required | Middle (3 to 7), all / required |
|---|---|---|
| Roark | 18 / 3 | 0 / 0 |
| Gardenia | 37 / 8 | 0 / 0 |
| Fantina | 43 / 3 | 1 / 0 |
| Maylene | 26 / 1 | 12 / 4 |
| Wake | 51 / 5 | 22 / 2 |
| Byron | 40 / 1 | 21 / 3 |
| Candice | 21 / 3 | 9 / 3 |
| HQ | 3 / 0 | 9 / 0 |
| Galactic | 19 / 0 | 47 / 0 |
| Volkner | 14 / 0 | 6 / 1 |
| League | 9 / 1 | 20 / 1 |

Two ordinary trainers sit at the top. Before Maylene's split, 98 of 99
ordinary trainers are at the bottom, and only 15 of the 40 required ones
reach the middle anywhere. Party size decides it: all 166 one-Pokemon
trainers are at the bottom, 86 of 139 with two, 22 of 105 with three,
and 7 of 20 with four or more. So the lever for goal 2 is the trainer
pass's party sizes, and the gauntlets, which string bottom-band fights
into one test.

**Goal 1, the hyper-offense.** Six fights meet the test (threat by chance
0.55 or more, four tactics or fewer, two thirds of turns called): Maylene,
Wake, Volkner, Flint, Lucian and Cynthia. Their damage is spread across
the team: no single boss-side change cuts a fight's threat by more than
0.09 (Maylene's Cacturne without Sucker Punch). So curbing them means
several changes in each, trading damage for the tactics the scores cannot
see, as Ian's own peak fights do. Four of the six carry Choice items
(Wake's Sharpedo, Volkner's Electivire, Flint's Infernape and Magmortar),
which Ian's ruling takes off.

**Flint and Byron, the two Ian named as perhaps too hard**, read 7.8 and
7.7. Flint's is Fire doubling up: Infernape and Magmortar knock out the
same 310 player Pokemon in one hit between them. Taking Magmortar's
Choice Specs off gives back 0.106 of safe switch-ins, and Infernape out
0.150, so the Choice ruling alone brings him down most of a point.
Byron's is Forretress's Explosion, which the scores count as a one-hit
knockout on most of the side: without it his safe switch-ins rise 0.186,
from 7.7 to about 6.3. The scores count every Explosion as a knockout, not
a one-time trade, so they overrate that part of Byron, the thing Ian
named.

**Goal 4, the player's levers.** Caps and map weather are the only strong
ones. Two cap levels move a split's fights by 0.03 to 0.11 of answers and
0.02 to 0.08 of safe switch-ins. Pastoria Gym's rain is the biggest
single lever: without it Wake's fight gains 0.124 of safe switch-ins.
Roark's and Bertha's sand cost the player about 0.07 of answers each.
Items and TMs barely move anything: Life Orb one split earlier is worth
0.05, Choice Specs 0.04, and every TM or HM one split earlier 0.014 or
less, 54 of the 91 nothing at all. So **TM timing is not a difficulty lever** and the
TM pass can place TMs for variety; and the player's Choice items going
away costs only 0.025 of answers. No species is the only sure answer to
any boss Pokemon, so no fight needs a particular catch. A fully evolved
species' median share of boss Pokemon surely answered is 0.58; three stand
far above it: Giratina 0.97, Dusknoir 0.92 and Feraligatr 0.88. Only
Unown answers nothing. The report also lists everything Ian's cuts of
2026-09-27 touch (design pass 3).

**Goal 3, the added content.** By the League, 126 of the player's 434
species are new to Oxide, but the trainers use 3 new species in about
1,050 Pokemon, and no new move or ability at all. Bringing the new
content in is the trainer pass's job.

**The legendary gate** (Ian, 2026-09-27): not yet. Nothing here has moved
the difficulty; the bottom band and the hyper-offense are as the base ROM
left them, so the question of Valor Cavern and Stark Mountain stays
closed until the trainer pass lands and is rescored.

## The player's side fixed, and the Barry split (2026-09-27)

Four faults in what the scores gave the player came to light while Ian's
capture rule was worked through, and all four are fixed together with the
Barry split, under one rescore.

The side counted slots the game never rolls. A land table with land_rate 0,
or a water kind with no rate, still lists species, and those came onto the
side early. Seven species now arrive a split later than Roark's
(Clobbopus, Dewpider, Dolliv, Dubwool, Liepard, Sandygast and Shellos), and
two or three more at each of the next three splits.

The side knew too many moves. Every level-up move of a species and its
earlier stages up to the cap counted, level 1 included. Under Ian's capture
rule it now knows its four moves at capture, then what each stage learns by
level-up afterwards, a later stage from the level it evolves at; a move only
the relearner could teach counts for nothing. Between 1 and 9 side members
a split lose a band on their best same-type move. Two of Oxide's own lists
showed up in this. A wild Alolan Ninetales, whose whole list sits at level
1, is caught knowing Tail Whip, Disable, Ice Shard and Safeguard. A Seedot
evolved at 14 has no Grass or Dark attack by Roark's cap of 16.

The side missed six evolutions. The encounter tool's reader keeps only a
stage's level evolutions when it has any, which is right for placing wild
Pokemon, and the side had borrowed it. Wooper to Clodsire (Poison Barb, from
Roark's split), Goomy to Hisuian Sliggoo and Goodra (Metal Coat), Kirlia to
Gallade and Snorunt to Froslass (Dawn Stone, from Fantina's), Slowpoke to
Slowking (King's Rock, from Wake's) and Yamask to Runerigus (Reaper Cloth,
from Candice's) now reach it.

The Fight Area's tag battle is one story fight, like Spear Pillar (Ian,
2026-09-27), and both tag fights record Barry's partner teams for the
rebuild to play. The Fight Area waits for the Beacon Badge, so it sits in
the Barry split.

The Barry split (Ian, 2026-09-27) holds every fight after the Beacon Badge
up to the Elite Four, at a cap of 71: Lucas and Dawn 3, Barry 6, the Fight
Area's tag battle, and the 27 trainers of Route 223 and Victory Road. The
Elite Four stay in the League split at 78, as the engine's table has it;
the rebuild plays each at its own ace (72 to 78), since Ian levels only to
the next fight's ace. The engine's cap and the encounter tool's split came
from the main and encounter tracks on the same branch.

The rescore recomputed every score whose inputs changed, and a second run
verified all 974 of them. The four fixes to the side barely move
the fight scale: no story fight outside the Barry split moves by more than
0.1, and the line over Ian's ratings is now 9.5 minus 7.5 times safe
switch-ins (9.4 and 7.4 before). A side that knows fewer moves and arrives a
little later still answers much the same Pokemon. Saturn 2 rises 0.2 after
Ian's edit in the team builder: Uxie trades Trick Room for Foul Play, and
Rhyperior's Choice Scarf becomes an Expert Belt. The fight's permanent
Trick Room stays.

The Barry split is what moves. Its fights are now played at 71 rather than
the League's 78:

| Fight | Before | After |
|---|---|---|
| Barry 6 | 6.2 | 7.2 |
| Lucas and Dawn 3 | 5.6 | 6.5 |
| The Fight Area's tag battle | not scored | 7.6 |

Of the 27 trainers of Route 223 and Victory Road, the fourteen in Victory
Road (aces of 63) rise, nine of them by half a point or more (Ace Trainer
Omar most, by 1.0). The thirteen with aces of 59 to 61 move by 0.35 or
less, since they sit well under either cap. The split holds 9 at the
bottom of the scale and 18 in the middle (one required in each). The
League held those 27 and the Fight Area's Volkner and Flint before, and
now holds only its story fights.

## The Galactic stretch: split shape and caps (proposal, 2026-09-25)

Ian's ruling: after Candice (cap 56) the story runs Lake Acuity, the
Galactic HQ, the Battle Zone, the Mt. Coronet climb and Spear Pillar, then
Volkner, then the League (78). His targets, relative to the caps: the HQ
hard, the Battle Zone medium hard, the climb and the last Galactic fights
very hard. `shape.py` scores each group across the gap between its
strongest Pokemon and the player's cap, with the player's side as it is at
that point (before the zone's captures for the HQ, after them for the
rest) and answers counting a Choice lock.

**Levels move a fight only a little; the roster sets its range.** Each
level of gap is worth about 0.02 of threat. The bands below are anchored
on Oxide's own fights: very hard is Wake's fight and above (threat
0.73 or more, answers 0.12 or fewer), hard is the other gym leaders
(threat 0.60 to 0.72, answers 0.20 or fewer), medium hard is Saturn 1,
Barry 5 and Bertha (threat 0.40 to 0.55, answers 0.20 to 0.30). For
ordinary trainers, medium hard sits between Wake's split's filler (threat
0.21, answers 0.49, 10 under the cap) and Candice's (0.44 and 0.26, 4
under).

| Fight | At the cap: threat, answers with the lock | 2 over the cap |
|---|---|---|
| Saturn 2 (HQ, cap 60), under Trick Room | 0.40, 0.19 | 0.40, 0.18 |
| Cyrus 2 (HQ, cap 60), with Suicune | 0.48, 0.10 | 0.52, 0.09 |
| Mars and Jupiter, Stark Mountain (Galactic, 65) | 0.48, 0.16 | 0.52, 0.13 |
| Mars and Jupiter, Spear Pillar (Galactic, 65), with Luxray | 0.41, 0.24 | 0.42, 0.21 |
| Cyrus 3 (Galactic, 65), Ian's new team | 0.64, 0.14 | 0.66, 0.11 |
| Volkner (68) | 0.75, 0.15 | 0.77, 0.14 |

These are Ian's baseline teams (the table was first run on the base ROM's
older teams). Saturn 2 is scored under Trick Room since Ian's ruling of
2026-09-25 that the fight opens in one lasting the whole battle, which no
move can end: his threat rose from 0.29 to 0.41 at the tree's levels, and
it stays flat as his levels rise, because under Trick Room a level up is
Speed that costs him turn order. His Rhyperior holds a Choice Scarf, which
under a permanent Trick Room only makes it move later, and his Uxie's own
Trick Room now always fails; Ian ruled that the trainer pass swaps both
(the design passes, item 5). **Cyrus 3 and Saturn 2 still lean on what the
scores cannot see:** Curse, Explosion, Swagger and Aqua Ring, which the
scores leave out with every status and setup move. So both read softer
here than they will play.

The zone's 52 route and Stark Mountain trainers read 0.34 and 0.39 at 10
under the cap, 0.39 and 0.34 at 7 under, 0.45 and 0.29 at 4 under: medium
hard at about 7 under. (These ordinary-trainer figures were last scored
before the scarcity pass, on a side of 322 species at Candice's split,
and were rescored on 2026-09-26 against today's 432; the means moved by
0.02 at most.)

**Two shapes work, since a cap has to rise at a story event every player
reaches and the zone is optional, so it cannot close a split of its own.**
One Galactic split with the zone inside it puts the HQ at the same cap as
the climb: the HQ's grunts and bosses jump from Candice's 56 to about 65 at
once, the HQ can only be told apart from the climb by roster, and the HQ is
scored against zone captures the player cannot have yet. **Two splits** fix
all three: an HQ split that closes on the HQ fights, then a Galactic split
holding the zone and the climb that closes on Cyrus 3. That is the
recommendation:

| Split | Cap | Closes on |
|---|---|---|
| Candice | 56 | Candice |
| HQ (Warehouse and HQ) | 60 | Cyrus 2 and Saturn 2 |
| Galactic (the zone, the climb, Spear Pillar, the Distortion World) | 65 | Cyrus 3 |
| Volkner | 68 | Volkner |
| League | 78 | Cynthia |

| Trainers | Now | Proposed | Reads as |
|---|---|---|---|
| Warehouse and HQ grunts (12) | 53 to 55 | ace 56, 4 under | Candice's filler, the hardest ordinary trainers |
| Saturn 2 and Cyrus 2 | 58 | 60, at the cap | Saturn 2 hard; Cyrus 2's answers are hard but his threat (0.45) needs roster work |
| Battle Zone (52) with Buck | 73 to 78 | 55 to 60, the parked 18 off | medium hard, about 0.39 and 0.34 |
| Mars and Jupiter, Stark Mountain | 77 to 78 | 59 to 60 | 0.36 and 0.26, on the soft side of medium hard |
| Mt. Coronet climb and Spear Pillar trainers (12) | 54 to 55 | 63 to 65, up to the cap | harder than any filler so far |
| Mars and Jupiter, Spear Pillar | 59 | 67, 2 over | 0.39 at most: levels cannot make it very hard, its roster must |
| Cyrus 3 | 60 | 67, 2 over | very hard, 0.75 and 0.10 |
| Volkner | 62 | 68, at the cap | 0.75 and 0.18 with his Choice lock counted |

So the parked 18-level drop fits this shape as it stands (the zone at 5 to
10 under a cap of 65). On levels alone, Cyrus 2 reads hard (answers 0.10),
Cyrus 3 reads hard rather than very hard, and Spear Pillar's Mars and
Jupiter stay under hard; whether Ian's teams reach his targets through the
Trick Room and setup the scores leave out is for his playtest, and if they
fall short the trainer pass adjusts rosters rather than levels, since
levels move a fight about 0.02 a level. Both tag battles are scored
without the player's partner, which flatters the bosses. The Volkner split
keeps 68.

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
| `platredux.js`, `platreduxhc.js` | Platinum Redux, normal and hardcore | 8 and 8.5 | 2,829 each |
| `hardlove.js` | Hardlove Gold | 9.5 | 1,871 |
| `pkv5h.js` | Platinum Kaizo | 10 | 3,077 |
| `null12.js` | Pokemon Null 1.2 | 10 | 2,282 |
| `run-and-bun-trainer-battles.xlsx` | Run & Bun | 10 | Ian's sheet |
| `unbound.js` | Pokemon Unbound, bosses only; difficult mode is the rated one | about 5 to 5.5 | 357 in difficult mode |
| `odyssey-4.1.1.gba` and `.hma.toml` | Pokemon Odyssey 4.1.1 | about 6 | 350 trainers, in the ROM |

Run & Bun comes from Ian's own sheet, not the calculator. It has one tab per
split, from Brawly to the League, with a block per trainer giving level, held
item, ability, nature and moves. So it is scored structurally, with pressure
where its species exist in Oxide's data. Sacred Gold and Blaze Black 2 Redux
are unrated and left out. FireRed is the scale's floor and needs no data.

Unbound's calculator file holds only bosses, about 95 trainers in each of its
three modes (difficult, expert, insane), so it calibrates the boss scores but
not filler. Odyssey is not in the calculator's data. It is a FireRed-based
ROM, and Ian's HexManiacAdvance metadata beside it gives the addresses and
layouts of its trainer table (350 trainers), species stats, level-up moves,
names and type chart, so B1 reads it straight from the ROM. Its move table is
not among the named anchors and has to be located. Because Odyssey is all
double battles, it needs the doubles version of the pressure score (spread
moves, two attackers at once). Oxide needs that anyway for its 34 double
trainer battles (wild doubles are dropped, Ian, 2026-09-29). Until the doubles score is checked,
Odyssey's weight in the fit is kept low. Insurgence is an RPG Maker game with
no data here, and Ian last played it long ago, so it is left out unless a
trainer list turns up.

Hacks built on other games (Hardlove, Null, Run & Bun) do not share
Platinum's bosses. They line up by milestone: badge number, then rivals and
villain bosses by the badge they fall between, then the Elite Four and
Champion.

## Calibration

The ratings set the weights: the composite score is fitted so that each
reference lands at Ian's rating, and "6" becomes a band of scores per
milestone.

Below Renegade's 7, the fit rests on vanilla at 3, Unbound at about 5 to 5.5
and Odyssey at about 6. Each of those is weaker than a Platinum hack would be:
Unbound has bosses only, and Odyssey is doubles only, on another game. So a
direct reading is still needed. After the Roark and Gardenia splits are tuned,
Ian's playtest of them reads the bottom of the ramp directly, and the band is
corrected to it before the later splits are tuned.

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

## The scoring rebuild (design of 2026-09-27, under way)

The headline score is a damage race that cannot see status or setup, so it
read the Galactic HQ B2F grunt above Officer Somnu's sleep team. Ian
approved a rebuild on 2026-09-27 that plays each fight out, turn by turn
and many times, and scores it by what the player loses. It replaces the
headline only when it agrees with his judgements
(`docs/oxide/pairwise-candidates.md`).

The simulator is `fightsim.py`, with the trainer's AI in `fightai.py`.
Damage comes from the calculator the scores already use, run once per fight
for every attacker, target and move, in each weather the fight can have.
Stat stages, burn, screens, critical hits, the roll and accuracy are then
applied as Generation 4 does, and so is status. The trainer chooses its
move the way the game's AI does, from its own flags, with the switch rules
and the post-faint pick (condensed from `docs/oxide/battle-ai/`). The
trainer's side is as the data has it, items included.

The player's side follows Ian's rules of 2026-09-27. It never holds a Life
Orb or a Choice item. Its best offensive item is a type booster, one per
type and only where the census finds one by the split; Leftovers and
Sitrus Berries go as the census counts them. Its moves are what each
Pokemon can have by the split (the capture rule, TMs and tutors), ranked
by their worth in play, and its status slot takes only a move the policy
uses. Each caught Pokemon has one of its regular abilities at random, never
one that sets or cancels weather (Ian, 2026-09-26: the player never
controls weather); a species whose regular slots hold only such abilities
(Tyranitar's Sand Stream, Hippowdon's, Abomasnow's Snow Warning) takes a
stand-in with no effect until the ability pass gives it one.

The player plays as Ian does (the Overseer's rules, 2026-09-27). The best
answer leads, and the move that finishes the foe soonest is used. It sets
up while the foe needs three or more hits to faint it, to +2 against a last
Pokemon and +4 with more to come. When the active Pokemon loses its
exchange, a bench member that wins it comes in, judged on the move the foe
aimed at the one it replaces. If none can take that move, it goes in
through a pivot that takes the move for a quarter of its HP or less. It
stalls out the foe's screens, Tailwind, a move's Trick Room or weather, and
a threat with four or fewer PP left, by trading places between Pokemon that
each take a fifth of their HP or less. It does this for up to 12 turns a
battle.

The player plans for the fight (Ian, 2026-09-27). The pool is the strongest
third of the split's side at the cap, plus what every run has by the split:
the starter, the gifts and eggs every run is handed, the trades that ask for
nothing, and the static battles, each as far as it evolves. A team holds
one Pokemon of each family and one starter. Candidate sixes are tried in a
pre-pass, and the best becomes the team; three candidates in four are drawn
at random, and the fourth leans toward the Pokemon that beat most of the
trainer's one on one:

| Pre-pass step | Sixes | Battles each |
|---|---|---|
| All candidates | 80 | 10 |
| The best eight | 8 | 40 more |
| The reading, on the one kept | 1 | 200 |

A single stage of ten battles picked lucky teams. On Somnu the true losses
of its pick swung from 0.16 to 0.63 a battle with the random seed.

The League split is played in two sections (Ian, 2026-09-27). Every fight
up to the Elite Four is at the Barry split's cap of 71. Each Elite Four
fight is at its own ace's level, since Ian levels only to the next fight's
ace:

| Aaron | Bertha | Flint | Lucian | Cynthia |
|---|---|---|---|---|
| 72 | 73 | 74 | 75 | 78 |

Double battles play as doubles: two slots a side, each filled from its own
trainer's party, spread moves at three quarters, and Barry beside the
player in the tag fights, driven by his own flags. Ian judged his pairs as
singles, so the fit plays them as singles.

A fight's reading is the mean number of the player's Pokemon lost, the
chance of losing three or more, the chance of a wipe, the share of battles
won, and the share of the team's HP spent. The last one separates the easy
fights, where nothing faints. The headline weights these onto Ian's 1-to-10
scale, fitted to 25 of his pairs and tested on the 15 held out. Ian's
grades are noisy by his own account, so the fit is kept simple and the
pairs it misses are read by hand.

Reading the traces of the fights the fit misses found two faults in the
player, both fixed. A Pokemon attacked with recoil or a crashing move that
would faint it: 26 of the player's 181 faints against Lucian were its own
Ceruledge's Flare Blitz, and 33 of 214 against Saturn 1 were Brave Bird,
Flare Blitz and a missed High Jump Kick. The player now takes another
attack when one does damage. And the player's Tyranitar set sand with Sand
Stream, against the weather ruling.

**Where the fit stands** (2026-09-27, all of the above in). It puts its
whole weight on the share of HP spent:

| Pairs agreeing with Ian | Count |
|---|---|
| Held out (the bar is 13) | 9 of 15 |
| All forty, by the headline | 26 of 40 |
| All forty, by Pokemon lost then HP | 24 of 40 |

Across the last four changes to the player it moved between 7 and 9 held
out and between 24 and 28 of the forty, so it is kept simple and not tuned
to the pairs; Ian judges some of his own as misjudged. The fourteen it
misses, read by hand:

| Pairs | Ian | The simulator | Why |
|---|---|---|---|
| 2, 4, 7, 11, 15, 17, 30, 31, 38, 39 | one ordinary trainer harder | both cost the planned six at most 0.12 Pokemon a battle and under a sixth of its HP | a six prepared from the strongest third has nothing at stake against these; Ian's grades come from a team that did not prepare for them |
| 16, Byron and Cyrus 1 | Byron a bit | Cyrus 1 by HP, Byron by Pokemon lost (0.69 to 0.54) | the weighting, not the reading |
| 37, Aaron and Flint | Aaron a bit | Flint, by a fifth of a point | within the noise |
| 22, Saturn 1 and Hesperid at Lake Valor | Hesperid, very close | Saturn 1 far harder (2.02 lost to 0.12) | half of Saturn 1's kills are Azelf's; Hesperid's danger is two Explosions, which Generation 4's AI rarely uses at high HP, and his levels of 49 to 52 meet a six at 56 |
| 36, Lucian and Bertha | Lucian a lot | Bertha (2.62 lost to 0.99) | a quarter of Bertha's kills are the permanent sandstorm finishing Pokemon the player never heals, and Lucian's three Choice items let the player bait a lock, the weakness Ian's own ruling names |

Two limits of the model bear on the last two rows: the player uses no
items in battle, and it plans a six for each fight. For Ian: whether his
grades of ordinary trainers assume a prepared team, which decides whether
they are read from a realistic box (the box mode) or from the planned six;
and whether the player heals with items in a boss fight.

## Open questions for Ian

Ian's ratings of sixteen fights (open question 1 until 2026-09-25) are in
"What Ian's ratings showed". None are open: Ian approved the stone plan
on 2026-09-27 (design pass 2).

## Order of work

- [x] **B0, scoping** (2026-09-22). Ian's answers are in, and the reference
  data is pinned.
- [ ] **B1, data layer.** This covers Oxide and every reference in one schema,
  a checked map of each hack's records to its fights, and Oxide's split map
  for trainers, items, marts and TMs. The check: trainer and set counts match
  each source, a sample of fights matches the calculator's own view of them,
  and every Oxide trainer lands in exactly one split.
  - [x] **B1a, the Platinum-based references and the story fights**
    (2026-09-22). `data.py` reads Oxide and every reference into one shape.
    Oxide is rebuilt per trainer by the encounter tool's `calc_trainers`, so
    its rolled natures and default moves come with it. `fights.json` lists
    the 28 story fights, in the splits Ian's Level Caps sheet gives them.
    `test_b1` checks that every pinned file is unchanged, that set counts
    match each source, and that every fight resolves in every Platinum-based
    hack. It also checks that no hack's League sits below its Volkner. That
    check fails without the per-hack overrides below, so it does test
    something.
  - [x] **B1b, the hacks built on other games** (2026-09-22). Each lines up
    with Oxide by position: its Nth gym against Oxide's Nth, its Elite Four
    in order against Aaron to Lucian, its Champion against Cynthia
    (`fights.json`, "milestones"). Their rivals and villain bosses are not
    mapped yet; the gyms and League are what calibration needs first.
    Hardlove is read from the donor ROM (`hardlove_rom.py`) and Run & Bun
    from Ian's sheet (`run_and_bun.py`); Null and Unbound from the
    calculator's files, with each Mega set folded into the Pokemon that
    becomes it.
  - [ ] **B1c**, Odyssey read from the ROM through the HexManiacAdvance
    anchors, once its move table is found.
  - [x] **B1d, Oxide's split map** (2026-09-22, `splits.py`). A map takes
    its split from its own wild table where it has one, else from its
    location name (a hand table of towns and wild-less places), else from
    the map outside its door by warps. Trainers take the splits of the maps
    that battle them. Items come from item balls, hidden items, NPC gifts,
    marts and the Game Corner. The check that matters: 27 of the 28 story
    fights land in the split Ian's sheet gives them from map data alone, and
    the 28th, Mars at Lake Verity, is a return visit to a Roark-split map.
- [x] **B1e, required trainers** (checked 2026-09-25 against Ian's own routes, `test_b1e` 7 of 7). For each split, which trainers the player
  cannot avoid. A trainer is unavoidable when no walkable path through its
  map gets from where the player enters to where they must leave without
  stepping into its sight. Everything needed is in the tree: each trainer's
  position, facing, movement pattern and sight range are in its event
  record (Route 202's Youngster Tristan looks south with a range of 5), and
  each map's walkable tiles are the collision bits in its land data, laid
  out by its map matrix. The limits are real and the report will name them:
  what the player can cross depends on the split (Cut, Rock Smash,
  Strength, Surf, Rock Climb and the bike), trainers that turn or walk see
  more than one line, ledges are one-way, and a script can force a battle
  that no sight line explains. The check: the story fights come out
  required, and a handful of route trainers Ian knows to be avoidable come
  out avoidable. It comes after B2, which scores the bosses and needs none
  of it, and before B4, whose natural levels should count only the
  experience a player cannot skip. The same reachability also gives each
  trainer the split in which the player can first reach it, which fixes
  the 18 filler trainers B1d places too early (`metrics.late_visits`).
  Built 2026-09-23 (`world.py`, `required.py`, `test_b1e`) for the story
  path's overworld routes and the simple indoor maps; see "What B1e
  found". Its check waits on Ian's examples (open question 2). Gyms with
  moving parts and multi-floor dungeons are left for later, if the
  placement pass needs them.
- [x] **B2, structural metrics** for every reference and for Oxide as it
  stands (2026-09-23, `metrics.py`, `test_b2`). The check: vanilla, Renegade
  and Kaizo come out in that order on almost every metric. It held on nine
  of fourteen, and the test pins which; see "What B2 found". The percentile
  of base stats against the player's pool moves to B3, which builds the
  pool, and the filler report skips Kaizo until its filler has a map.
- [ ] **B3, the player's side and pressure.** This covers the pool per split
  (species, moves, items) and the pressure scores. The check: damage agrees
  with the calculator's page and with the in-game roll already waiting on Ian
  (encounter build plan, D5).
  - [x] **B3a, Oxide's side and Oxide's fights** (2026-09-23, `pool.py`,
    `pressure.py`, `calc_headless.js`, `test_b3`). See "What B3 found". The
    check holds against D5's figures; the in-game roll waits on Ian.
  - [x] **B3b, the reference hacks' bosses against Oxide's side**
    (2026-09-25, `refpressure.py`, test_b3 11 of 11). Each boss Pokemon
    carries its own game's stats, types and move data into the engine; 192
    seats over nine hacks, two runs agreeing exactly. See "What B3b and B5
    found".
- [ ] **B4, the level curve**: the natural level per split, for Oxide and
  Renegade. The tools are built (2026-09-25, `levels.py`, `shape.py`,
  `test_b4` 5 of 5, twice): the natural level from trainers alone, a Rare
  Candy budget per split, and the split-shape model behind the Galactic
  proposal. Trainers alone leave a team of six far under every cap, about
  30 Rare Candies are placed before the League against 250 to 440 needed,
  and Ian's ruling that the portable PC gives infinite Rare Candies closes
  that gap, so the budget reads as how much of each cap the trainers pay
  for.

  Entering each split at the last cap, as candy-to-the-cap means, a team
  of six (medium slow) reaches this from trainers alone before candies
  close the rest (2026-09-25, on the settled split shape):

  | Split | Cap | Every placed trainer | Only unavoidable ones |
  |---|---|---|---|
  | Roark | 16 | 12 | 9 |
  | Gardenia | 26 | 21 | 18 |
  | Fantina | 33 | 29 | 26 |
  | Maylene | 39 | 37 | 34 |
  | Wake | 44 | 44 | 40 |
  | Byron | 53 | 49 | 45 |
  | Candice | 56 | 55 | 54 |
  | HQ | 60 | 57 | 56 |
  | Galactic | 65 | 65 | 60 |
  | Volkner | 68 | 65 | 65 |
  | League | 78 | 70 | 69 |

  Two splits pay for their whole cap when every trainer is fought: Wake's,
  whose 75 placed trainers are the most in the game, and Galactic's, now
  that the Battle Zone's re-levelled trainers count there. The League's
  pays least, 8 levels short even fighting everything, because Victory Road
  and Route 223 are short for a 10-level rise. Counting only the trainers
  the story path cannot avoid, every split falls 2 to 9 levels short. That
  gap is what Ian's placement change (more required ordinary trainers)
  narrows, and B1e's list says where.
- [ ] **B5, calibration** to Ian's ratings, and the target band per milestone.
  One check comes first, from Ian (2026-09-25): **the threat score may
  overrate hyper-offense**. It counts what a boss knocks out while moving
  first and ignores everything a player does besides attacking back
  (switching, priority, screens, status), so a team of fast attackers reads
  as the hardest kind of fight. Ian's tell is Maylene, whom it puts at 0.69
  threat and 0.20 answers, level with the hardest gym leaders. Calibration
  tests this against the reference hacks' hyper-offense bosses before
  trusting the ranking; if it holds, threat is weighted down or tempered by
  answers.

  Started 2026-09-25 (`pressure.py`'s B5 columns, `calibrate.py`). Ian
  rated sixteen fights and explained the ones the scores misread; from
  that came baited Choice locks, setup branches and safe switch-ins, and
  safe switch-ins read both his hack ratings (R squared 0.92) and his
  fight ratings (minus 0.58) best ("What B3b and B5 found", "What Ian's
  ratings showed"). Ian's fight scale is his own design scale, separate
  from the game scale (2026-09-26); the line above translates the readings
  onto it. Left: the double battle,
  which the tool cannot score, and the stage, which Ian's scale carries.
  The engine's computed powers reached the scores on 2026-09-26 (the
  encounter track's item 22). The seven moves that pick another stat or
  type (Foul Play, Body Press, Psyshock, Sacred Sword, Darkest Lariat,
  Freeze-Dry, Flying Press) and Rage Fist follow when a cloud session's
  engine work merges and the encounter track's item 23 teaches the
  calculator, with a smaller rescore.
- [x] **Incremental rescores** (Ian, 2026-09-27), before B6's runs. A full
  rescore costs about 45 minutes a run on this CPU and two runs must agree,
  even when a change touches a few fights. Each stored score gets a
  fingerprint of its inputs (the exact job the calculator runs, the slices
  of the calculator's data it reads, the engine files, the scorer's code)
  and a verified mark; a rescore recomputes only the scores whose
  fingerprint changed and stores them unverified, and a second pass
  recomputes the unverified ones and marks them verified when they agree.
  test_b3 checks that every fingerprint matches its inputs and nothing is
  left unverified, and each rescore reports how many scores it recomputed
  and how many it reused. Built and in use (2026-09-27, `rescore.py`):
  every score the tool stores is a unit, 507 before B6 and 965 with it,
  and the whole set is fingerprinted in about half a minute. The first
  run, on the combined branch (the calculator's item 23, the friendship
  and trade evolutions, the new grass tables and sources), recomputed all
  507 and verified all 507 with no disagreement; the classic starters'
  move that followed staled none, the Heatran fix staled the 259 built
  on the Galactic, Volkner and League sides, and the Kaizo move data with
  element 4's partly working moves staled 489, all but Roark's split. The
  engine part covers only the calculator files the runner loads, so no
  game C, battle script or AI change stales a score, and a species'
  hidden-ability slot, which no score can reach, is left out, since the
  natives' hidden abilities otherwise staled all 507 while changing none.
  Hidden items' flag numbers come from the tree's own flag list, not the
  shared build folder's header, which holds whichever tree last built it.
  test_b3 checks the scores before B6 and test_b6 checks B6's.

  ```
  PYTHONPATH=. python3 -m tools.oxide.balance.rescore            # what changed
  PYTHONPATH=. python3 -m tools.oxide.balance.rescore --verify   # the second run
  PYTHONPATH=. python3 -m tools.oxide.balance.rescore --status   # counts only
  ```
- [x] **B6, the audit**, aimed at Ian's four goals of 2026-09-26 ("The
  target"). Every Oxide fight placed on his fight scale, the required
  ordinary trainers included (they are not scored yet, and they are most of
  the 0 to 2 fights); the fights whose difficulty is all damage (high
  threat, few tactics, easy to read: Wake, Maylene, Cynthia and Volkner on
  today's scores) marked as the hyper-offense to curb; the fights sitting
  at 0 to 2 listed as the ones to raise into 3 to 6 or 7; Flint and Byron
  checked for what makes them too hard; and every lever on the player's
  side (a species' stats, a TM or item one split earlier, route weather, a
  cap) ranked by how far it moves the scores, with any lever or species
  that moves them absurdly far or not at all flagged for the balance pass.
  Built (2026-09-26, `b6.py`, `test_b6`), as rescore units: each ordinary
  trainer the player meets (428, 40 of them required), scored in the split
  B1e first reaches it in; and each story fight's levers, rerunning only
  the matchups a change touches. `b6.py --report` gives the findings by
  goal, `--content` adds the count of new species, moves and abilities on
  each side, and `--draft` scores one of Ian's Frontier Brain drafts in a
  split and places it on his fight scale. Run and verified on 2026-09-27;
  "What B6 found" has the findings. The report's own code is left out of
  B6's fingerprint (`rescore.B6_REPORT_ONLY`), so editing it stales no
  score.
- [x] **The team builder's two numbers** (Ian, 2026-09-27): the encounter
  tool's team builder edits a trainer's team and shows where it lands on
  Ian's fight scale. It calls `teamscore.py` (interface agreed with the
  encounter tool builder on 2026-09-27). `score(stem, data)` runs the full
  scorer on the trainer's fight (its story fight when it has one, else
  the split B6 places it in, in its map's weather and the engine's
  permanent Trick Room table) and returns the plan's number, with the
  same seat in each reference hack for a story fight; about 1 second
  early in the game and up to 20 late. `estimate(stem, data)` is the
  instant number, 0.01 to 0.06 seconds: each boss Pokemon against the
  split's side by the Generation 4 damage formula at the middle roll in
  plain Python (stats from base stats, level, IVs, EVs and nature; move
  power, type, STAB and effectiveness; the attack items and Choice Scarf;
  no ability, weather or critical hit), read as the plan's safe
  switch-ins, threat and answers, with safe switch-ins corrected by a line
  fitted to the full scorer over every stored fight (`teamscore.json`,
  `--fit`). A team the builder saves stales its fight's scores as usual.
  The estimate is for steering an edit, and the full score is the number
  to quote; its distance from the full score, in points of Ian's scale:

  | Fights | Mean | Worst |
  |---|---|---|
  | The 31 story fights | 0.25 | 1.0 (Maylene, read too easy) |
  | All 461 stored fights | 0.13 | |

Then the design passes, in this order. Each proposal goes to Ian before it
lands, and each change is re-scored as it lands.

1. **Level caps.** A redesigned curve, from B4 and the target band. Moving a
   cap moves every wild level in that split, so the encounter track re-runs
   `cli evolve` against the new caps. That is coordinated through the
   Overseer and not done from here.
2. **Item access and TMs.** Which held items, marts and TMs each split
   offers, and how many TMs there are. Ian's standing rule (2026-09-26,
   staples survey): the player can never set, change or end weather, so
   TM07 Hail, TM11 Sunny Day, TM18 Rain Dance and TM37 Sandstorm go or
   become other moves. The one Ability Patch in the game (for a hidden
   ability) is the only exception, and Defog still clears fog. Choice
   items are to be nearly entirely gone from the game (Ian, 2026-09-25,
   after Volkner), up from "quite rare". When a confusion cure is first in
   reach decides how Swagger plays: at Gardenia no Persim Berry is.
   **Evolution stones are a scarcity lever** (Ian, 2026-09-27): the pass
   starts with a census of every stone the player can get, where and when
   (item balls, hidden items, the Underground's dig pool, gifts, marts), and
   places one fixed Sun Stone and one fixed Moon Stone, since Espeon and
   Umbreon now evolve by those stones. **Competition for a scarce stone is
   intended** (Ian, 2026-09-27): a player with an Eevee and a Charcadet
   and one Sun Stone has to choose, which weakens the box and makes a
   decision, so the census sets the counts as a lever and never adds a
   stone just to settle a contest. The census lists each stone's
   claimants: the Sun Stone's are Espeon and Armarouge (Charcadet lives on
   Route 206 from Fantina's split and at Fuego Ironworks from Byron's), and
   Ceruledge's Dusk Stone has fixed finds in the Galactic Warehouse and on
   Victory Road. Dahlia now gates the Veilstone Game Corner (the Frontier
   Brains ruling, above), so its prize list is reviewed beside the census.

   **The census** (2026-09-26, `stones.py`, on the tree that moves Espeon
   and Umbreon onto stones). No stone is scarce today, so the one fixed
   Sun Stone and Moon Stone Ian asked for already exist several times
   over. Three sources give a full set or close to it: a woman on Route
   207 gives all nine stones at once after the player has travelled with
   Mira (Fantina's split, since the bike opens Wayward Cave); Galactic
   HQ's second basement holds one of each (HQ's split); and the
   Underground's digs give every stone but the Oval Stone with no limit,
   0.9 to 1.5 percent of digs before the National Dex and 1.4 to 5.4
   percent with it, from Gardenia's split. Each stone also has two or
   three fixed finds of its own.

   | Stone | Fixed finds before the League | Lines that want one, and from when |
   |---|---|---|
   | Fire | 5, from Fantina's split | Ninetales (Roark's), Flareon (Fantina's) |
   | Water | 5, from Fantina's | Ludicolo (Roark's), Poliwrath (Gardenia's), Vaporeon, Starmie, Cloyster |
   | Thunder | 5, from Fantina's | Vikavolt, Pawmot, Raichu (Gardenia's), Jolteon |
   | Leaf | 5, from Gardenia's | Shiftry (Roark's), Sinistcha (Fantina's; since the Sinistea ruling) |
   | Moon | 4, from Gardenia's | Nidoqueen, Nidoking, Delcatty (Roark's), Clefable, Umbreon |
   | Sun | 4, from Fantina's | Espeon and Armarouge (both Fantina's) |
   | Shiny | 5, from Fantina's | Cinccino (Roark's), Togekiss, Roserade, Florges |
   | Dusk | 4, from Fantina's | Honchkrow (Roark's), Ceruledge, Mismagius, Polteageist, Chandelure |
   | Dawn | 5, from Fantina's | Froslass (Gardenia's), Gallade |
   | Oval | 1, the Lost Tower (Maylene's); not dug | Chansey (Fantina's) |

   **Corrected** (2026-09-26, found by the main track): the first count
   took a hidden item on the border of two maps twice, since both maps'
   events list it under one flag. Route 211 west's Moon Stone is Eterna
   City's, and the Resort Area's and Route 229's Thunder Stone is one
   item; `stones.py` now counts each hidden item once, and the figures
   here are recounted.

   The census also turned up what looked like a data error, Polteageist
   evolving into Sinistcha by Dusk Stone. **Superseded** (Ian, 2026-09-27):
   Sinistea splits, a Dusk Stone making Polteageist and a Leaf Stone making
   Sinistcha, which was always his intention. So the Leaf Stone gains a
   second claimant, Sinistea for Sinistcha from Fantina's split, beside
   Shiftry, and the one Leaf Stone the plan keeps becomes a contest.

   **Ian's rulings on the census** (2026-09-27): the Underground closes,
   since the player is never given the Explorer Kit; both bulk sets go,
   Route 207's nine and Galactic HQ's; and this track proposes how many of
   each stone and where, for his approval. The main track makes the script
   changes.

   **The plan, approved by Ian** (2026-09-27) with one change: the Shiny
   Stone gets an early copy, since Roserade and Togekiss are likely in
   hand when Fantina's split starts. One stone for every two or three
   lines that want it, the first copy about a split after the first
   claimant can be owned, so every stone is a decision; every find below
   is one the tree already has, so nothing new is placed. With the
   Underground and the two sets gone, the tree has 25 stones before the
   League, 2 or 3 of each but the Oval Stone; this keeps 16. The main
   track makes the changes.

   | Stone | Keep | Take out | Lines that want it |
   |---|---|---|---|
   | Fire | Solaceon Ruins (Maylene's) | Fuego Ironworks, Stark Mountain | Ninetales, Flareon |
   | Water | Solaceon Ruins (Maylene's), Route 213 (Wake's) | Route 230 | Ludicolo, Poliwrath, Vaporeon, Starmie, Cloyster |
   | Thunder | Solaceon Ruins (Maylene's), Sunyshore (Volkner's) | the one on the Resort Area's border with Route 229 | Raichu, Vikavolt, Pawmot (all from Gardenia's), Jolteon |
   | Leaf | Floaroma Meadow (Gardenia's) | Great Marsh, Route 225 | Shiftry and, since the Sinistea ruling, Sinistcha |
   | Moon | Eterna City (Gardenia's; it is also Route 211 west's, on their border), Mt. Coronet outside north (Galactic's) | none | Nidoqueen, Nidoking, Delcatty, Clefable, Umbreon |
   | Sun | Valor Lakefront (Wake's), the one Ian asked for | Mt. Coronet 4F | Espeon, Armarouge |
   | Shiny | Route 212 south (Wake's), where the hidden Dawn Stone becomes a Shiny Stone; Iron Island B3F (Byron's); Route 228 (Galactic's) | Route 210 north | Cinccino, Togekiss, Roserade, Florges |
   | Dusk | Wayward Cave (Fantina's), the Galactic Warehouse (HQ's) | none; Victory Road's is after the League | Honchkrow, Ceruledge, Mismagius, Polteageist, Chandelure |
   | Dawn | Mt. Coronet 1F south (Fantina's) | Route 225; Route 212 south's becomes the early Shiny Stone | Froslass, Gallade |
   | Oval | the Lost Tower (Maylene's) | none | Chansey |

   The scores weigh the stones now (2026-09-27). The player's side takes
   every evolution that needs an item, a stone or an item held on
   level-up, from the split its item is first in reach, where it took
   the encounter tool's judged level of 30 or 32 before. A wild
   Pokemon's held item counts from the split its holder is first
   caught, since a catch or Thief takes it: Seadra's Dragon Scale and
   Clamperl's Deep Sea items are the only way to Kingdra, Gorebyss and
   Huntail. The side changes from Gardenia's split to Byron's:

   | Split | Side before | Side now | Earlier than before | Later than before |
   |---|---|---|---|---|
   | Gardenia | 177 | 185 | the Moon and Leaf Stone lines, Steelix, Gorebyss, Huntail | |
   | Fantina | 272 | 257 | | the Fire, Water, Thunder, Sun and Shiny Stone lines, Politoed |
   | Maylene | 348 | 338 | | the Sun and Shiny Stone lines, Politoed, Dusknoir, Gliscor, Weavile |
   | Wake | 393 | 390 | | Dusknoir, Rhyperior, Weavile |
   | Byron | 417 | 416 | | Dusknoir |

   It staled 418 of the 965 scores, all rescored and verified. Gardenia's
   fight moves most, 0.03 more safe switch-ins (6.7 on Ian's scale, from
   6.9), since the Moon and Leaf Stone lines join her split; Fantina's
   and Maylene's move 0.01 the other way. The fit to Ian's ratings
   tightens a little: the fight line is now 9.4 minus 7.4 times safe
   switch-ins, and the rank correlation over his fifteen singles minus
   0.64.

   **What else only the Underground gave** (`stones.py --underground`,
   which lists every other source of each of its 49 treasures):

   - Everstone and the four weather rocks come from nowhere else. The
     rocks go, since the player never sets weather (Ian, 2026-09-27). One
     fixed Everstone goes in Oreburgh Mine (Ian): the B2F ball that holds
     an Old Amber, one of the four fossils Ian deleted, becomes it.
   - Heart Scales, which Pastoria's Move Relearner takes one of a move,
     now that the PCs' free relearner is gone: 10 fixed finds before the
     League, 4 of them by the time the player reaches Pastoria, which stay
     as they are (Ian, 2026-09-27). The player's side still assumes every
     level-up move, the level 1 and evolution moves included, so it reads
     the relearner as free; 10 in a run covers the key moves of a nuzlocke
     box.
   - Every Plate keeps one or two fixed finds, the only Light Clay is on
     Mt. Coronet B1F (Candice's split), and the Root, Armor and Skull
     Fossils stay in Oreburgh Mine B2F; the four fossils Ian deleted go
     with their balls there too. The Pixie Plate is not in the game yet
     (element 7); when it is, it takes one fixed find like the others.
   - Money: 21 Star Pieces and 14 Nuggets stay as fixed finds.

   **Corrected** (2026-09-29, the combined rescore's census): the census
   now reaches each item as the player does, waiting for Surf, Rock Smash,
   Cut, Strength, Rock Climb, Waterfall and the bike (with ledges and bike
   ramp jumps) where its map needs them (`splits.item_reach`). Four of the
   stones the plan keeps come later than the table above says, since the
   plan read each find at its map's split:

   | Stone | Find | The plan's split | Reached in | Needs |
   |---|---|---|---|---|
   | Moon | Eterna City (hidden) | Gardenia | Byron | Surf |
   | Dawn | Mt. Coronet 1F south | Fantina | Byron | Surf |
   | Water | Route 213 | Wake | Byron | Surf |
   | Sun | Valor Lakefront (hidden) | Wake | HQ | Rock Climb |

   Solaceon's Water Stone stays Maylene's. **Ian's answer** (2026-09-29):
   case by case, at the item pass. Each of the four comes to him with a
   recommendation, to keep its timing or to move it to a nearby spot
   reached on foot (the main track's change), and what each choice does to
   the stone contests and the lines waiting on it. No stone is added
   either way.

   **Element 7's new held items** (Ian, 2026-09-29): Eviolite, Assault
   Vest, Rocky Helmet, Air Balloon and the rest are each the reward for an
   optional trainer, a spinner or another optional fight, never sold, even
   though a shop would be simpler. None is placed outside the test kit
   today, so the census has none of them and no score assumes them. When
   they are placed, the census must count a reward from its fight's split:
   `splits.gifts` gives a script's gift its map's split, so a gift given
   after a battle in the same script is to take the trainer's split (B6's
   placement) instead.

   **No Life Orb for the player** (Ian, 2026-09-27): Stark Mountain's
   outside map still has a Life Orb ball (Galactic's split). The item pass
   replaces it; the main track makes the change.
3. **Species, abilities and learnsets**, including the base ROM's 228
   duplicated second ability slots. From the same answers: no weather move
   in any player learnset, tutor or egg list, and no ability that sets or
   cancels weather (Sand Stream, Snow Warning, Cloud Nine and the rest) in
   an obtainable Pokemon's regular slots; Drizzle Pelipper and Drought
   Torkoal are weighed for trainers only. Done for the last five lines
   (Ian, 2026-09-29): Cloud Nine (Psyduck, Golduck), Snow Warning (Snover,
   Abomasnow) and Sand Stream (Hippopotas, Hippowdon, Tyranitar) are hidden
   abilities now, Tyranitar's regular one Shed Skin, and the 20 trainer
   Pokemon that bring the weather take the hidden slot; no weather ability
   is left in a regular slot. Alakazam, Ampharos, Dugtrio,
   Electrode, Farfetch'd, Jumpluff, Pikachu, Roserade and Swellow get their
   modern stat buffs, Chimecho and Staraptor go to their modern totals, and
   Cresselia keeps hers. The pass weighs Magic Guard for the Abra line.
   Since the natives' 17 hidden abilities merged (2026-09-27,
   `cloud/element5-hidden-abilities`), 91 native species carry a working
   hidden ability (Moxie, Multiscale, Magic Bounce, Sand Rush and the
   rest); the scores do not read hidden abilities, since the player's side
   takes each species' first ability and a trainer's set names its own, so
   the pass weighs them by hand, beside the one Ability Patch that reaches
   them.
   **Terrain is not ported** (Ian, 2026-09-27), so nothing the player can
   get may be dead weight: the four Terrain moves (which say "But nothing
   happened!") leave every learnset, TM and tutor list, and the four Surge
   abilities and Seed Sower are replaced wherever a species carries them.
   Steel Roller was on the list until the move survey's ruling below kept
   it, with its effect to be written. The moves that only read terrain (Ice
   Spinner, Terrain Pulse and the rest) are plain hits and stay. `b6.py
   --report` lists the worklist: Arboliva's Seed Sower, Galarian Weezing's
   hidden Misty Surge, and the obtainable lines that learn a Terrain move
   by level (Galarian Mr. Mime and Mr. Rime, Sylveon, the Smoliv line, and
   Tapu Koko and Xurkitree, whom Mesprit's roamer now draws; Tapu Koko's
   Electric Surge goes too); no TM, tutor or egg list teaches one yet, and
   the TM pass keeps it that way. The other Tapus and Xerneas stay out of
   reach.

   **The move-pool survey** (Ian, 2026-09-27; `docs/oxide/move-pool-survey.md`),
   applied in the learnset pass after B6:

   - Twelve moves leave every learnset now: Telekinesis, Ally Switch,
     Topsy-Turvy, Flower Shield, Fairy Lock, Aromatic Mist, Magnetic
     Flux, Speed Swap and the four Terrain moves.
   - Magic Room, Teatime, Octolock, Sky Drop, Salt Cure and Steel Roller
     stay; their missing effects are written in a cloud job, with the
     survey's 22 partly working moves (Mind Blown first). The doubles
     moves that work stay.
   - Splash and Teleport go, and each of their six species gets a real
     level-1 move, this track's pick: Azurill Pound, Bounsweet Leafage,
     Feebas Tackle, Hoppip Absorb, Wailmer Water Gun and Abra Confusion.
     Each is a weak attack, of the species' own type but for Feebas, which
     keeps its weakness with the Tackle it now learns at 15. Abra's is the
     one that changes play: it can fight before it evolves, where Teleport
     left it none. Magikarp has the same gap (Splash alone until Tackle at
     15) and falls under the same ruling, so it takes Tackle at 1, like
     Feebas; it is off the pick-list, so this reaches only trainers'
     default moves. Every other Splash or Teleport
     carrier (Buneary, Ralts, the Abra and Hoppip lines' evolutions,
     Delphox, and the egg lists) has another move beside it, and simply
     loses it; `b6.py --report` lists them.
   - Cut, Rock Smash and Flash leave learnsets where they were there only
     as HMs, and their TM slots become other moves in the TM pass.
   - Type-flavoured near-duplicates stay, as do Land's Wrath, Flame Burst
     and Sludge. The rest of the cull waits for the TM pass.

   **The learnset study** (Ian, 2026-09-27; `docs/oxide/kaizo-comparison.md`,
   answer 6). A study of when and why Kaizo gives each move, written as
   rules and turned into a generator that proposes level-up lists for any
   species and any move, the later generations' moves included, inside
   Oxide's caps. It writes no game data. It replaces the first reading of
   answer 6, which copied Kaizo's lists line by line: that copy
   (`cloud/balance-learnset-pass`) and this track's review of it
   (`balance-learnset-review`) stay unmerged as reference. Ian's points
   against the copy were Stone Edge at 87 when the League cap is 78, Dig
   added widely although Kaizo made Dig a one-turn 60, and wholesale
   changes while many moves are still broken.

   1. Relate, for each Kaizo line, every move's level to the move's real
      strength as Kaizo has it (`docs/oxide/kaizo-move-changes.md` first),
      to whether it is same-type or coverage, to the evolution stage, and
      to the gym split it lands in under Kaizo's own caps.
   2. Write the findings as rules (when the first strong same-type move
      arrives against a split, how coverage is timed, and the like), and
      test them by how well they predict Kaizo's own lists, some lines held
      out.
   3. Build the generator. It proposes; a sweeping pass comes only when Ian
      chooses one, after the broken moves are fixed. It keeps every level
      at or under the League cap of 78 unless a line is post-game only; it
      drops dead-weight moves by a rule that catches the ones Ian named as
      never good (Absorb, Wrap, Constrict, Barrage, Snore, Rage, Razor
      Wind, Bide, Comeuppance, vanilla Octazooka and Submission) rather
      than by the list alone; and it follows the standing rulings (no
      weather move for an obtainable species, the move pool's first cut).
      Before part 3 is built, a one-paragraph summary of the rules goes to
      Ian through the Overseer, so he can confirm the direction.

   **What parts 1 and 2 found** (2026-09-27, `learnstudy.py` and its
   `--rules`; the rules wait on Ian's word before part 3). Kaizo's 493
   lists were read as 264 lines, each along the path a player walks: a
   stage's moves count from the level it is reached. Every move is valued
   as Kaizo plays it: power, times accuracy, times hits, over the turns it
   takes. Kaizo's splits follow its gyms, which close at 16, 28, 38, 47,
   54, 65, 74 and 84, with the League running to 100.

   The typical new move grows stronger through the game, and coverage
   keeps pace with same-type moves from the start:

   | Kaizo split | Same-type median | Coverage median |
   |---|---|---|
   | Roark | 60 | 60 |
   | Gardenia | 75 | 80 |
   | Fantina | 80 | 90 |
   | Maylene | 90 | 95 |
   | Wake | 95 | 95 |
   | Byron to the League | 100 to 102 | 96 to 102 |

   Two lines in three have a same-type move of 70 or more by the end of
   Gardenia's split, and half have a strong one (85 or more) by the end of
   Fantina's, mostly on the stage the line ends at. Half the lines get a
   coverage move of 70 or more in Roark's split. Past level 1, feeble moves
   (under 50) sit almost all in Roark's split. Nine in ten damaging moves
   past level 1 are a new type or at least as strong as the best of that
   type already known; the rest are priority, pivot and spread moves.
   Stat-raising setup is nearly absent, 25 entries in all 493 lists. Kaizo
   kept vanilla's early levels, so with its higher caps a move lands a gym
   or two earlier than in vanilla.

   Each move has a usual point in Kaizo's game, and placing it there
   predicts the lists of families held out (five folds) best. A move
   Kaizo never used, as most later-generation moves are, is placed nearly
   as well by the usual point of Kaizo's moves of like strength. The stage
   and same-type barely help once the move is known.

   | Placing damaging moves, on held-out families | Mean miss, in splits | Within one split |
   |---|---|---|
   | The move's usual split | 1.25 | 67% |
   | A move Kaizo never used, by moves of like strength | 1.38 | 61% |
   | The strength curve alone | 1.74 | 57% |
   | Vanilla's timing | 2.01 | 50% |

   The dead-weight rule has five tests, each read off Kaizo's lists:
   strength under 40; under 90% accuracy on under 100 power (Kaizo's lists
   keep one such move, Mega Punch); a charging turn in the open (Kaizo's
   keep none); at most half of what the split usually gives; and Snore and
   the moves that return less than double damage (Bide, Metal Burst,
   Comeuppance). Priority, pivots, item moves, False Swipe and a certain
   stat drop or status are exempt. It catches all eleven moves Ian named,
   in every split (Octazooka at vanilla's values: Oxide's own, 85 at full
   accuracy, passes). Kaizo's own lists break it in 98 of 3,520 entries,
   most of them Tackle at its old 35 power. In Oxide's lists it catches 434
   entries of 36 moves; beyond Ian's eleven, the most common are Astonish
   (69 entries), Rollout (30), Fire Spin (28), Fury Cutter (20), Whirlpool
   (18), Sand Tomb (17), Bind (15), Sky Attack (9) and Skull Bash (6). Ian
   confirmed the rule and those nine (2026-09-27).

   **Part 3: the three analyses and the generator** (2026-09-27,
   `learngen.py`, `learnwild.py` and `kaizo_docs.py`; Ian's answers of the
   same day). Kaizo's encounter tables, evolution levels and list of wild
   hazards come from its documentation workbook on the G: drive, read once
   into `kaizo_docs.json`. Mantyke's evolution was misread as Remoraid by
   the encounter tool's readers (Remoraid is the Pokemon it needs in the
   party); the encounter track fixed them, and these tools read the result
   rightly meanwhile.

   Ian's rule of the same day judges every list: a move's worth to the
   player is what the Pokemon knows at capture (the last four its list gives
   by its level, which can include moves below the catch level) plus what it
   learns by level-up afterwards, on its form or a later one. Relearner-only
   moves, an evolved form's level-1 moves among them, count for almost
   nothing: the relearner is in Pastoria, each move costs a scarce Heart
   Scale, and each use competes with the whole box. Level-1 lists matter as
   the relearner's menu and the trainer palette. He also settled: recoil
   attacks stay real attacks, the delays stay (a wait longer than a split is
   worth it, as the best encounter boxes delay routes by several splits),
   and Hoppip takes Leafage.

   (a) Delays. A delay is a strong move (85 or more a turn) a pre-evolution
   learns at or after the level it could evolve that the evolved stage
   learns later, or only at level 1, or never. Waits within a split are the
   ones counted below; waits past it are Kaizo's list tails. The strongest
   delay, Ian's, is a move only a Pokemon kept from evolving ever gets: the
   pre-evolution learns it at or after its evolution level, and no later
   stage learns it by level-up.

   | | Kaizo | Oxide now | The proposal |
   |---|---|---|---|
   | Evolutions rewarding a wait of a split or less | 124 of 246 | 63 of 320 | 169 of 320 |
   | Median wait past the evolution level | 8 | 5 | 6 |
   | Moves only a Pokemon kept from evolving gets | 334 | 243 | 35 |
   | Of those, strong | 148 | 37 | 14 |

   The proposal turns most delays into a move the evolved stage learns a
   split later, not never: Kaizo keeps many more exclusive ones.

   (b) Wild movesets (`docs/oxide/wild-movesets.md` lists every flagged
   slot). A wild Pokemon knows the last four level-up moves at or below its
   level and picks at random, so a move that ends the encounter (Roar,
   Whirlwind, Teleport, Self-Destruct, Explosion, Memento; Kaizo's six
   hazards, and four more) comes up a quarter of the time when it is one of
   four. Ian's example holds: Kaizo's Route 207 Growlithe at 11 knows Ember,
   Bite, Tackle and Roar. A better version later is the same line in a
   later split as a stage the earlier catch cannot reach by then, or with a
   same-type move a band stronger than the earlier catch knows at capture
   or learns by then.

   | | Kaizo | Oxide now | The proposal |
   |---|---|---|---|
   | Wild slots | 4,371 | 3,867 | 3,862 |
   | Can end the encounter | 1,566 | 153 | 0 |
   | Can knock itself out (recoil, crash, a Ghost's Curse) | 740 | 261 | 533 |
   | Have a better version later | 409 | 9 | 6 |

   The first summary gave 91 for the proposal. Two things made it: my check
   followed only the first branch of a branching line (Sinistea to
   Polteageist, never Sinistcha), and an evolved stage's level 1 was ordered
   weakest first, so a wild one met soon after its evolution level, with
   fewer than four moves of its own by then, filled its four from its
   strongest level-1 moves. The branch is fixed, and level 1 is now ordered
   strongest first, so such a Pokemon takes the weakest. Oxide's own figure
   fell from 29 to 9 when Feebas stopped reading as evolving at level 170
   (its beauty requirement; the encounter track has the report).

   (c) Evolved catches with no good move (a same-type move of 70 or more
   a turn, or any of 85 or more) known at capture or learnt by level-up
   before their split's cap: 70 in Oxide now, of 18 species, 25 of them
   because the good move went only to the pre-evolution (Swadloon's Bug
   Buzz, Naclstack's Earthquake, Cinccino's Hyper Voice, Fearow's Drill
   Peck). The proposal fixes them by level-up, not level 1: a species still
   bare gets its line's earliest good move on its own list at its earliest
   bare catch's level (the newest of its four at capture), or soon after
   capture before the split's cap. Twelve species take such a move, and one
   stays bare, Fletchinder, whose line has no good move to give (Flame
   Charge, Acrobatics and Aerial Ace are all weak), so it wants a new move.

   Every catch, judged the same way: the share with a good move known at
   capture or learnt by level-up before its split's cap.

   | Split | Oxide now | The proposal |
   |---|---|---|
   | Roark | 0.08 | 0.09 |
   | Gardenia | 0.26 | 0.45 |
   | Fantina | 0.54 | 0.95 |
   | Maylene | 0.74 | 0.99 |
   | Wake | 0.87 | 0.99 |
   | Byron to the League | 0.86 to 0.93 | 1.00 |

   The generator (`learngen.py propose`, and `line <species>` for one line
   now and proposed) writes no game data. For each species it takes the
   moves its line learns now and Kaizo's for it, where Kaizo's move is the
   same move (same type, attack or not; a move one line alone learns, a
   signature such as Spacial Rend, goes to no other); drops dead weight, the
   move pool's cut, weather moves for obtainable species and any attack
   under nine tenths of a same-type one it already knows; places each attack
   at Kaizo's usual point carried onto Oxide's splits (a recharging move by
   its full one-turn power), keeping status moves where they are; gives an
   evolved stage what came before its evolution at level 1, whole and
   strongest first; gives a strong move its pre-evolution gets within a
   split of evolving to the evolved stage one split later; starts a first
   stage with an attack (the survey's picks, Hoppip's Leafage among them,
   else a weak one of its type); keeps every move that ends a wild
   encounter above the levels the species is wild at; fixes the bare
   catches as above; and stays at or under 78. Over 652 species it adds
   4,221 moves, moves 4,830 and drops 718: 397 dead weight, 234 weaker
   same-type, 67 weather and 59 the move pool's cut.

   The level-1 lists are kept whole, as the relearner's menu and the trainer
   palette; cutting them to six attacks and two status moves dropped 1,491
   entries for no gain to the player, and tidiness is all it bought. They
   are ordered strongest first, which matters in one place: a wild or
   trainer Pokemon with fewer than four moves of its own at its level fills
   from level 1, from the end. 426 of the 1,802 trainer Pokemon take default
   moves; they would get the weaker level-1 moves, which the trainer pass
   can override with sets of their own.

   For Ian before any sweeping pass: whether level 1 should be strongest
   first (wild evolved Pokemon soon after evolving are no better than one
   raised) or weakest first (such Pokemon, and trainers on default moves,
   get the strongest); whether more delays should be exclusive, as Kaizo
   has them; and a move for Fletchinder.
4. **Weather** on routes and in gyms. Weather from an ability stays for
   the whole battle, and trainers keep theirs.

Engine changes Ian has decided on, each needing every score rerun when it
lands (staples survey, 2026-09-25): native moves take their full modern
values (the Generation 5 to 7 buffs and the Generation 6 cuts), except the
base ROM's deliberate values, and Thunder Wave, Dark Void and Swagger keep
their Generation 4 accuracy; critical hits become 1.5 times at modern
rates, which the scores leave out as they leave out every critical hit;
the Generation 6 type immunities; and modern behaviour for native
abilities. Status stays as Generation 4 has it, and Hidden Power keeps its
IV formula. The calculator keeps Generation 4's formula and chart, so each
of these reaches the scores through the move data or the calculator's
Generation 4 branch, as element 5's abilities will.
5. **Trainers**, with the bosses first, Choice items coming off them (Ian,
   2026-09-25): Roark to five Pokemon, Gardenia to six,
   then each fight into the band. Filler trainers come after, and with them
   Ian's placement change: more ordinary trainers made unavoidable, checked
   against B1e's list, and **the gauntlets** (Ian, 2026-09-27): which
   one-way areas the Pocket PC refuses to work in, and how many trainers
   each holds in a row, proposed to Ian first. Also the **level 71 Lucas and Dawn fight** (trainer
   slots 779 to 784, one per starter): Ian designed it for the start of
   Victory Road, and Victory Road 1F's script starts it there now (the main
   track's `3a3472432`, which moved the Battle Zone after the Galactic HQ).
   Its level 9 and 30 counterparts (787 to 792 on Route 202; 793, 794 and
   799 to 802 on Route 207) are already where the story passes. The three
   are story fights now, Lucas and Dawn 1 to 3, one variant for each
   starter and rival, and read 2.1, 2.6 and 5.6 on Ian's scale. **Saturn 2** (Ian,
   2026-09-25): Uxie's Trick Room, which always fails under the fight's
   permanent room, and Rhyperior's Choice Scarf, which only makes it move
   later there, are each swapped for something else, chosen in the pass.
   **Element 5's abilities as Oxide has them** (Ian, 2026-09-25):
   Neutralizing Gas follows the later games, turning every other ability
   off while its holder is out; Symbiosis is not ported; Sharpness keeps
   hg-engine's longer list of slicing moves, with the five claw moves. Moving a trainer or adding a sight-line blocker edits
   map events and sometimes field scripts, which are carry-over files that
   `checkmap.py` and the bulk tools compare with the base ROM. Each change
   is registered as an intended divergence (the bulk tools' DIVERGED lists)
   in the same commit, and the Overseer is told before the pass starts so
   the gate learns about it at the same time.

   **The gauntlet proposal** (2026-09-27, `gauntlet.py`; the first reading,
   superseded by "The gauntlets, reworked" below). The
   scores read every fight from a healed party, so a gauntlet needs a
   reading of its own: random parties of six are sent through its trainers
   in order with nothing healed between them. Each boss Pokemon is met by
   the member that beats it losing the least HP, damage carries over both
   ways, and a member that falls is a nuzlocke death. The parties are sixes
   from the strongest third of the split's side by stats, closer to a
   chosen team than sixes from the whole side, which run from first stages
   to legendaries. The reading is the share of parties that clear without
   a faint, and the HP they spend, in whole members, set beside the split's
   story fights read the same way. It leaves out misses, critical hits,
   status, switching and the bag's items, so it compares gauntlets with
   fights, not with a run. Two runs gave the same readings.

   | Area | Split | Trainers | Pokemon | Clean clears | HP spent |
   |---|---|---|---|---|---|
   | Team Galactic's Eterna building, ending at Jupiter | Fantina | 6 and Jupiter | 15 | 1.00 | 0.37 |
   | Wayward Cave | Fantina | 10 | 15 | 1.00 | 0 |
   | The Lost Tower | Maylene | 6 | 12 | 1.00 | 0.54 |
   | Iron Island | Byron | 14 | 29 | 0.92 | 1.70 |
   | The Galactic HQ, its grunts | HQ | 12 | 23 | 0.95 | 1.38 |
   | The Galactic HQ, ending at Cyrus and Saturn | HQ | 12 and both | 35 | 0.36 | 4.73 |
   | The Mt. Coronet climb, its grunts | Galactic | 10 | 29 | 0.94 | 1.05 |
   | The climb, ending at Spear Pillar | Galactic | 10, Mars and Jupiter, Cyrus | 45 | 0.43 | 3.71 |
   | Stark Mountain, its first 8 | Galactic | 8 | 22 | 0.80 | 1.83 |
   | Stark Mountain, all of it | Galactic | 19 | 55 | 0.32 | 6 |
   | Victory Road | League | 14 | 44 | 0.98 | 0.84 |
   | Victory Road, opened by Ian's level 71 Dawn fight | League | the rival and 14 | 50 | 0.96 | 1.32 |

   | Story fight, from a healed party | Clean clears | HP spent |
   |---|---|---|
   | Fantina | 0.41 | 2.81 |
   | Maylene | 0.31 | 2.61 |
   | Byron | 0.59 | 1.61 |
   | Cyrus 2 | 0.94 | 1.57 |
   | Saturn 2 | 0.64 | 1.80 |
   | Cyrus 3 | 0.77 | 1.37 |
   | Flint | 0.43 | 2.86 |
   | Cynthia | 0.21 | 3.64 |

   Today's grunts and route trainers cost a chosen party almost nothing,
   however many are strung together: the Eterna building's six, Wayward
   Cave's ten and Victory Road's fourteen together spend less than one
   member's HP. So a gauntlet of them adds no attrition until the trainer
   pass raises them into the middle band, which is B6's finding again. The
   two story climbs are the exception, because they end at their bosses:
   the Galactic HQ read as one gauntlet is as testing as Maylene's fight,
   and harder than either of its bosses alone, and the Mt. Coronet climb
   is as testing as Fantina's or Flint's.

   The proposal, one gauntlet on each stretch of the story where the game
   already walks the player one way through a building or a climb:

   | Gauntlet | Split | Trainers in a row | What it asks now |
   |---|---|---|---|
   | The Galactic HQ, from the door to Cyrus and Saturn | HQ | its 12, then both | a gym-strength test already |
   | The Mt. Coronet climb, to Spear Pillar | Galactic | its 10, then Mars and Jupiter and Cyrus | a gym-strength test already |
   | Victory Road, opened by Lucas and Dawn at 71, as its script now starts | League | the rival, then its 14 | its trainers raised in the pass, to be the last test before the League |
   | Team Galactic's Eterna building, to Jupiter | Fantina | its 6, then Jupiter | the first gauntlet, kept light once its grunts are raised |

   And optional ones, each with its prize at the far end: Iron Island
   (Byron's split, the Riolu egg), all 14 trainers, a moderate test already;
   the Lost Tower (Maylene's, the Oval Stone), its 6, light; and Stark
   Mountain (the Galactic split), cut to its first 8 trainers, since a
   third of parties clear the whole climb cleanly and the median party
   loses all six. Left out:
   Wayward Cave, whose Gible is one of Ian's super-wanted lines and should
   not sit behind attrition; Eterna Forest, whose trainers are tag battles
   beside Cheryl, which the scores cannot read; and the open routes, which
   are not one-way.

   Two questions come with it. Does the bag's healing work inside a
   gauntlet (the reading assumes not, which is the harder case)? And should
   a gauntlet ask as much as its split's gym, read the same way, or less?
   Ian's level 71 Lucas and Dawn slots (779 to 784), and their level 9 and
   30 counterparts on Routes 202 and 207, sit in the trainer data's
   dummy_ files, which the balance data skipped as unused. It now reads
   every dummy_ slot a map battles, except the Maids' training battles:
   the three Lucas and Dawn fights are story fights, and Krystal (Route
   214, Wake's split) and Officer Argo (Mt. Coronet, the Galactic split)
   are ordinary trainers, both in the middle band.

   **The gauntlets, reworked on Ian's rulings** (2026-09-27; this replaces
   the proposal above, kept as the first reading). A gauntlet is 2 to 5
   mandatory trainers on the easier side of average, counted without
   optional ones; the bag may heal between its fights, so the danger is
   deaths snowballing; bosses stay outside, with gauntlets leading up to
   them; and a majority of the game's trainers should be mandatory, which
   is the trainer pass's. Ian judged the first reading too kind, because
   one team must answer several different fights.

   The second reading (`gauntlet.py`, now its default) keeps a party of six
   from the strongest third of the split's side together through a
   section and plays each fight out. A member keeps the field from one
   boss Pokemon to the next unless another answers it better; swapping in
   at a fight's start costs the incoming member a hit (after a faint and
   between boss Pokemon the game's Shift mode swaps free); every hit rolls
   its damage and its accuracy, and one in sixteen is critical. After each
   trainer the survivors heal to full and the dead stay dead. The reading
   is the share of parties that finish with no death, beside the split's
   story fights read the same way from a healed party (a rival's fight team
   by team). Two runs gave the same readings.

   | Section | Split | Trainers | Clean clears | Deaths a run |
   |---|---|---|---|---|
   | Eterna building, 1F and 2F | Fantina | 4 | 0.94 | 0.06 |
   | Eterna building, 3F | Fantina | 2 | 0.99 | 0.01 |
   | Galactic HQ, 1F | HQ | 2 | 0.68 | 0.41 |
   | Galactic HQ, 2F | HQ | 4 | 0.42 | 0.93 |
   | Galactic HQ, 3F | HQ | 4 | 0.55 | 0.83 |
   | Galactic HQ, B2F | HQ | 2 | 0.46 | 1.06 |
   | Mt. Coronet, 1F's tunnel | Galactic | 3 | 0.78 | 0.26 |
   | Mt. Coronet, 3F, 4F and Somnu on 5F | Galactic | 5 | 0.71 | 0.34 |
   | Victory Road, 1F nearer the entrance | League | 3 | 0.86 | 0.16 |
   | Victory Road, 1F's far half | League | 3 | 0.71 | 0.37 |
   | Victory Road, 2F | League | 4 | 0.54 | 0.71 |
   | Victory Road, B1F | League | 4 | 0.69 | 0.43 |

   | Story fight, read the same way | Clean clears |
   |---|---|
   | Jupiter 1, Lucas and Dawn 2, Fantina | 0.98, 0.97, 0.32 |
   | Cyrus 2, Saturn 2 | 0.60, 0.47 |
   | Mars and Jupiter, Cyrus 3 | 0.52, 0.30 |
   | Lucas and Dawn 3, Barry 6, Aaron, Bertha | 0.71, 0.48, 0.76, 0.64 |
   | Flint, Lucian, Cynthia | 0.14, 0.39, 0.06 |

   What it shows. The Eterna building's grunts cost nothing yet: its
   trainers are at the bottom of the scale, so it is a gauntlet in name
   until the trainer pass raises them, and as the first gauntlet it should
   stay the lightest. The Galactic HQ's sections are as deadly as its
   bosses, so they are not yet on the easier side: Scientist Fredrick (3.8
   on Ian's scale, against the split's 2.8) and a B2F grunt (4.0) are the
   ones to soften. Mt. Coronet takes two sections once its officers are
   left out: Hesperid is a fight Ian rated, a boss, and Moira (4.9) and
   Argo (5.2) are far above the split's 3.4; Somnu, at it, closes the
   second section, and the climb leads up to Hesperid and Spear Pillar.
   Victory Road's four sections sit on the easier side of the League's
   fights, but six of its fourteen trainers are above the split's average
   (Omar 4.7 and Henry 5.1 most), to soften or to leave optional.

   How the reading could be truer still, in order of weight: a drafted team
   rather than random strong sixes (the species that answer the split's
   fights, weighted by the encounter tables); the player's level on
   arriving rather than the split's cap; the boss AI's switches, setup and
   status rather than its hardest hit; and status, PP and held items. For
   Ian: which sections he takes, and whether the trainers above their
   split's average are softened or left optional.

Trainers can now be given a chosen nature (encounter M8), which removes the
old trade-off between a nature and IVs. One open defect has to be fixed before
the trainer pass uses the field: the packer accepts `NATURE_COUNT`, and that
hangs the game (encounter build plan, QA findings).

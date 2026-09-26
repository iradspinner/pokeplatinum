# Balance plan

This is the balance track's status home. Ian put this session in charge of
balance on 2026-09-22, once element 4 had put most moves and species in the
tree. The file covers what "balanced" means for Oxide, how it gets measured,
the data behind it, and the order of work. Ian answered the scoping questions
the same day, and his answers are recorded below as decisions.

**Where it stands (2026-09-25).** The tool knows the Galactic split Ian
ruled in on 2026-09-25 (below), on branch `balance-galactic-split`, which
merges the encounter track's branch so the two land together; every
balance suite passes there, twice (`test_b1` 43, `test_b1e` 7, `test_b2` 7,
`test_b3` 8). The pressure scores were recomputed for the new split and for
the encounter track's recast tables. Done: B1a, B1b, B1d, B1e (now checked
against Ian's routes), B2 and B3a. B3b, the reference hacks' bosses
against Oxide's side, is parked on `wip-balance-b3b` since a Node process
segfaulted on the degraded CPU with four cores busy on 2026-09-23, and
resumes on the new CPU. Ian chose to bring the Battle Zone down 18 levels;
the edit waits on the Overseer. B4, the level curve, is next. No questions
are open.

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

Ian's ruling, 2026-09-25 (`docs/oxide/battle-zone-plan.md` has the detail):

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
| Roark | 16 | 91 | 29 |
| Gardenia | 26 | 142 | 41 |
| Fantina | 33 | 217 | 47 |
| Maylene | 39 | 275 | 77 |
| Wake | 44 | 299 | 87 |
| Byron | 53 | 318 | 102 |
| Candice | 56 | 323 | 108 |
| Galactic | 64 | 330 | 123 |
| Volkner | 68 | 330 | 124 |
| League | 78 | 330 | 128 |

Threat is the share of that side a boss Pokemon knocks out within two
turns while moving first; answers is the share that does the same to it.
Each is the mean over the fight's Pokemon, and the last two columns are its
most threatening Pokemon and its least answered one.

| Fight | Threat | Answers | Worst threat | Fewest answers |
|---|---|---|---|---|
| Barry 1 | 0.00 | 0.96 | 0.00 | 0.94 |
| Barry 2 | 0.01 | 0.63 | 0.01 | 0.47 |
| Roark | 0.13 | 0.17 | 0.44 | 0.04 |
| Mars 1 | 0.01 | 0.35 | 0.01 | 0.09 |
| Gardenia | 0.68 | 0.05 | 0.91 | 0.01 |
| Jupiter 1 | 0.12 | 0.26 | 0.18 | 0.12 |
| Fantina | 0.51 | 0.11 | 0.88 | 0.01 |
| Barry 3 | 0.17 | 0.48 | 0.36 | 0.34 |
| Maylene | 0.69 | 0.20 | 0.79 | 0.08 |
| Barry 4 | 0.48 | 0.13 | 0.82 | 0.04 |
| Wake | 0.74 | 0.07 | 0.98 | 0.00 |
| Cyrus 1 | 0.38 | 0.35 | 0.59 | 0.23 |
| Barry 5 | 0.54 | 0.18 | 0.90 | 0.05 |
| Byron | 0.33 | 0.24 | 0.67 | 0.17 |
| Saturn 1 | 0.46 | 0.24 | 0.78 | 0.09 |
| Mars 2 | 0.26 | 0.15 | 0.51 | 0.04 |
| Candice | 0.73 | 0.14 | 0.97 | 0.00 |
| Cyrus 2 | 0.35 | 0.24 | 0.77 | 0.06 |
| Saturn 2 | 0.49 | 0.30 | 0.77 | 0.14 |
| Mars and Jupiter | 0.30 | 0.34 | 0.63 | 0.11 |
| Cyrus 3 | 0.65 | 0.16 | 0.95 | 0.04 |
| Volkner | 0.65 | 0.17 | 0.89 | 0.02 |
| Barry 6 | 0.54 | 0.24 | 0.91 | 0.05 |
| Aaron | 0.58 | 0.19 | 0.74 | 0.09 |
| Bertha | 0.49 | 0.30 | 0.76 | 0.01 |
| Flint | 0.69 | 0.14 | 0.92 | 0.04 |
| Lucian | 0.61 | 0.28 | 0.93 | 0.04 |
| Cynthia | 0.68 | 0.14 | 0.90 | 0.02 |

Both tables were recomputed on 2026-09-25, for the Galactic split and the
encounter track's recast tables (Roark's side went from 92 to 91 species
and Gardenia's from 140 to 142 after its one-spot fold, and Byron's and
Candice's rose by two). The Galactic fights are scored at 64
and Volkner at 68, so they read softer than before: Volkner's threat fell
from 0.75 to 0.65, because the player is now scored at 68 against his
team's 62. That is the gap the trainer pass closes, not a change in his
fight. These are raw scores, not ratings: B5 turns them into a band by
scoring the reference hacks the same way. What they already show:

- **Gardenia is the largest step in the game.** Roark's fight threatens 13
  percent of the side and Gardenia's 68, level with Cynthia's 68. Her
  Roserade alone knocks out 91 percent of the side within two turns while
  moving first, and 1 percent answers it. The plan wants Gardenia to reach
  the target and the curve to hold after; whether 0.68 is the target is
  B5's to say, but nothing later climbs as steeply.
- **Choice Scarf and rain leave bosses with no answer.** Nothing at the cap
  outspeeds a scarfed boss, so only priority answers Wake's Poliwrath,
  Candice's Mamoswine, Volkner's Electivire, Bertha's Gliscor or Cynthia's
  Lucario (2 percent or less each). Pastoria Gym's rain doubles Floatzel's
  and Ludicolo's Speed through Swift Swim, and they come out at 1 percent
  and under.
- **Byron is soft between two peaks**: 0.33 against Wake's 0.74 and
  Candice's 0.73. The admins' first fights (Mars 1, Jupiter 1) and Barry 3
  are light too.
- **Early fights in a split read too easy**, because the player is scored
  at the split's cap: Barry 1 is level 5 against a side at 16. B4's natural
  levels should replace the cap for fights before a split's end.
- **Five moves get no number from the calculator's Generation 4
  mechanics**: Electro Ball, Heavy Slam, Psywave, Super Fang and Trump Card,
  which it handles only in its later-generation code. The page runs the same
  code, so it should show nothing for them either. No boss uses them; the
  player's copies are dropped and listed per fight in `pressure.json`. A fix
  belongs to the encounter track, which owns the vendored calculator.

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
browser is many processes. The in-game roll is still Ian's (encounter build
plan, M8), and the calculator's order for a dual type's two factors (Crunch
into Bronzor 42 to 50, where the game gives 43 to 51) carries into B3 until
the encounter track's patch lands.

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
it in Galactic. The edit itself is in `res/trainers/`, which the Overseer
coordinates; it is not made yet.

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
on Oxide's own fights: very hard is Wake and Candice and above (threat
0.73 or more, answers 0.12 or fewer), hard is the other gym leaders
(threat 0.60 to 0.72, answers 0.20 or fewer), medium hard is Saturn 1,
Barry 5 and Bertha (threat 0.40 to 0.55, answers 0.20 to 0.30). For
ordinary trainers, medium hard sits between Wake's split's filler (threat
0.20, answers 0.51, 10 under the cap) and Candice's (0.42 and 0.27, 4
under).

| Fight | At the cap: threat, answers with the lock | 2 over the cap |
|---|---|---|
| Saturn 2 (HQ) | 0.60, 0.17 | 0.65, 0.14 |
| Cyrus 2 (HQ) | 0.45, 0.12 | 0.48, 0.11 |
| Mars and Jupiter, Stark Mountain | 0.47, 0.18 | 0.50, 0.16 |
| Mars and Jupiter, Spear Pillar | 0.37, 0.26 | 0.39, 0.23 |
| Cyrus 3 | 0.73, 0.12 | 0.75, 0.10 |
| Volkner | 0.75, 0.18 | 0.77, 0.16 |

The zone's 52 route and Stark Mountain trainers read 0.35 and 0.38 at 10
under the cap, 0.40 and 0.33 at 7 under, 0.45 and 0.28 at 4 under: medium
hard at about 7 under.

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
10 under a cap of 65). Two fights miss their target on levels alone and
belong to the trainer pass: Cyrus 2 at the HQ and Mars and Jupiter at Spear
Pillar, whose rosters top out below hard. Both tag battles are scored
without the player's partner, which flatters the bosses. The Volkner split
keeps 68: Volkner at the cap reads between hard and very hard once his
Choice item is counted, as Wake and Candice do.

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
trainer battles and its wild doubles. Until the doubles score is checked,
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

## Open questions for Ian

1. **The Galactic stretch** (2026-09-25, "The Galactic stretch" above): two
   splits, HQ at 60 and Galactic at 65 with Volkner at 68, and the trainer
   levels in that section's second table? Or one Galactic split at about 65?
   The parked Battle Zone re-level fits the two-split shape unchanged.

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
  - [ ] **B3b, the reference hacks' bosses against Oxide's side**, as "What
    gets measured" asks. Each hack changes species stats and moves, so the
    runner has to take a Pokemon's stats, types and moves per Pokemon
    rather than from one blob. Run it a split at a time, as B3a was.
- [ ] **B4, the level curve**: the natural level per split, for Oxide and
  Renegade. The tools are built (2026-09-25, `levels.py`, `shape.py`,
  `test_b4` 5 of 5, twice): the natural level from trainers alone, a Rare
  Candy budget per split, and the split-shape model behind the Galactic
  proposal. Trainers alone leave a team of six far under every cap, about
  30 Rare Candies are placed before the League against 250 to 440 needed,
  and Ian's ruling that the portable PC gives infinite Rare Candies closes
  that gap, so the budget reads as how much of each cap the trainers pay
  for. The per-split tables wait on the Galactic shape.
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
   then each fight into the band. Filler trainers come after, and with them
   Ian's placement change: more ordinary trainers made unavoidable, checked
   against B1e's list. Moving a trainer or adding a sight-line blocker edits
   map events and sometimes field scripts, which are carry-over files that
   `checkmap.py` and the bulk tools compare with the base ROM. Each change
   is registered as an intended divergence (the bulk tools' DIVERGED lists)
   in the same commit, and the Overseer is told before the pass starts so
   the gate learns about it at the same time.

Trainers can now be given a chosen nature (encounter M8), which removes the
old trade-off between a nature and IVs. One open defect has to be fixed before
the trainer pass uses the field: the packer accepts `NATURE_COUNT`, and that
hangs the game (encounter build plan, QA findings).

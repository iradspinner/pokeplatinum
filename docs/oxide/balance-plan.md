# Balance plan

This is the balance track's status home. Ian put this session in charge of
balance on 2026-09-22, once element 4 had put most moves and species in the
tree. The file covers what "balanced" means for Oxide, how it gets measured,
the data behind it, and the order of work. Ian answered the scoping questions
the same day, and his answers are recorded below as decisions.

**Where it stands (2026-09-25).** Test.nds is Oxide's base ROM, with Ian's
late boss updates and his sheet's testing teams as the baseline, merged.
The tool knows Ian's two Galactic splits (HQ 60, Galactic 65), the Battle
Zone has come down 18 levels to fit them, and Saturn 2 is scored under his
permanent Trick Room. Done: B1a, B1b, B1d, B1e, B2, B3a, B3b and B4's
tools. B5 has its readings, fits to the references and to Ian's own
ratings of sixteen fights, and his explanations of the fights the scores
misread: safe switch-ins read both best ("What B3b and B5 found", "What
Ian's ratings showed"). No questions are open.

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
| Roark | 16 | 105 | 30 |
| Gardenia | 26 | 176 | 42 |
| Fantina | 33 | 277 | 48 |
| Maylene | 39 | 345 | 78 |
| Wake | 44 | 392 | 88 |
| Byron | 53 | 417 | 103 |
| Candice | 56 | 432 | 109 |
| HQ | 60 | 433 | 112 |
| Galactic | 65 | 439 | 124 |
| Volkner | 68 | 439 | 125 |
| League | 78 | 439 | 128 |

Threat is the share of that side a boss Pokemon knocks out within two
turns while moving first; answers is the share that does the same to it.
Each is the mean over the fight's Pokemon, and the last two columns are its
most threatening Pokemon and its least answered one.

| Fight | Threat | Answers | Worst threat | Fewest answers |
|---|---|---|---|---|
| Barry 1 | 0.00 | 0.96 | 0.00 | 0.92 |
| Barry 2 | 0.01 | 0.63 | 0.03 | 0.51 |
| Roark | 0.14 | 0.15 | 0.43 | 0.04 |
| Mars 1 | 0.01 | 0.35 | 0.03 | 0.09 |
| Gardenia | 0.69 | 0.05 | 0.91 | 0.02 |
| Jupiter 1 | 0.12 | 0.24 | 0.19 | 0.11 |
| Fantina | 0.51 | 0.10 | 0.87 | 0.00 |
| Barry 3 | 0.18 | 0.46 | 0.38 | 0.32 |
| Maylene | 0.69 | 0.20 | 0.81 | 0.07 |
| Barry 4 | 0.48 | 0.13 | 0.83 | 0.03 |
| Wake | 0.74 | 0.07 | 0.98 | 0.00 |
| Cyrus 1 | 0.38 | 0.35 | 0.56 | 0.23 |
| Barry 5 | 0.55 | 0.19 | 0.91 | 0.04 |
| Byron | 0.34 | 0.21 | 0.56 | 0.15 |
| Saturn 1 | 0.52 | 0.24 | 0.80 | 0.08 |
| Mars 2 | 0.37 | 0.14 | 0.84 | 0.04 |
| Candice | 0.66 | 0.12 | 0.93 | 0.03 |
| Cyrus 2 | 0.45 | 0.12 | 0.81 | 0.04 |
| Saturn 2 | 0.40 | 0.19 | 0.83 | 0.00 |
| Mars and Jupiter | 0.31 | 0.33 | 0.69 | 0.06 |
| Cyrus 3 | 0.52 | 0.23 | 0.82 | 0.12 |
| Volkner | 0.65 | 0.16 | 0.90 | 0.02 |
| Barry 6 | 0.54 | 0.23 | 0.92 | 0.05 |
| Aaron | 0.59 | 0.18 | 0.76 | 0.07 |
| Bertha | 0.49 | 0.31 | 0.76 | 0.02 |
| Flint | 0.69 | 0.14 | 0.92 | 0.04 |
| Lucian | 0.62 | 0.27 | 0.94 | 0.03 |
| Cynthia | 0.68 | 0.13 | 0.90 | 0.01 |

Both tables were recomputed on 2026-09-26 for the modern move values, the
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
  Candice's 0.67. The admins' first fights (Mars 1, Jupiter 1) and Barry 3
  are light too.
- **Early fights in a split read too easy**, because the player is scored
  at the split's cap: Barry 1 is level 5 against a side at 16. B4's natural
  levels should replace the cap for fights before a split's end.
- **Five moves got no number from the calculator's Generation 4
  mechanics** until the encounter track's Oxide profile (2026-09-26):
  Electro Ball, Heavy Slam, Psywave, Super Fang and Trump Card. All five are
  scored now; Electro Ball at power 1, as the game plays it until the
  engine's variable-power work reaches the calculator.

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
here are from 2026-09-26, after the scarcity pass, the modern move values
and the calculator's Oxide profile; two runs agree exactly.

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
| Vanilla | 3 | 0.14 | 0.80 | 0.93 | 2.8 |
| Unbound, difficult | 5.25 | 0.51 | 0.28 | 0.62 | 4.4 |
| Renegade | 7 | 0.54 | 0.31 | 0.34 | 6.5 |
| Redux | 8 | 0.69 | 0.09 | 0.26 | 4.8 |
| Redux hardcore | 8.5 | 0.74 | 0.06 | 0.23 | 4.7 |
| Hardlove | 9.5 | 0.68 | 0.18 | 0.34 | 6.0 |
| Kaizo | 10 | 0.76 | 0.03 | 0.07 | 6.6 |
| Null | 10 | 0.92 | 0.01 | 0.01 | 5.7 |
| Run & Bun | 10 | 0.84 | 0.04 | 0.13 | 4.9 |

**Safe switch-ins read Ian's ratings best.** Its rank correlation with
the hacks' ratings is minus 0.93, level with the damage readings, and one
line fits them better than any damage line does:

```
rating = 10.6 - 8.1 x safe switch-ins, R squared 0.91
rating = 5.7 + 4.8 x (threat by chance - one-on-one answers), R squared 0.88
```

On the first, Oxide's gyms and League sit at about 7.5, and a 6 needs safe
switch-ins at about 0.56 against Oxide's 0.37; on the second, at about
7.3. Either way Oxide sits a point or more over the 6, level with
Renegade. The damage line read Unbound 1.6 too hard; the safe line reads
it within 0.3, since Unbound's teams leave far more room to switch.
Hardlove still reads 1.7 soft, most likely because the calculator does not
give its bosses' newer abilities to Pokemon from another game.

Seat by seat, safe switch-ins against the two references nearest a 6:

| Seat | Oxide | Unbound (5.25) | Renegade (7) |
|---|---|---|---|
| Roark | 0.81 | 0.83 | 0.63 |
| Gardenia | 0.35 | 0.95 | 0.46 |
| Fantina | 0.63 | 0.73 | 0.61 |
| Maylene | 0.30 | 0.93 | 0.30 |
| Wake | 0.32 | 0.48 | 0.48 |
| Byron | 0.24 | 0.51 | 0.11 |
| Candice | 0.35 | 0.59 | 0.24 |
| Volkner | 0.35 | 0.70 | 0.27 |
| Aaron | 0.48 | 0.55 | 0.33 |
| Bertha | 0.39 | 0.47 | 0.17 |
| Flint | 0.22 | 0.50 | 0.27 |
| Lucian | 0.22 | 0.44 | 0.31 |
| Cynthia | 0.19 | 0.40 | 0.22 |

Oxide leaves fewer safe switch-ins than Renegade at Gardenia, Wake,
Flint, Lucian and Cynthia, and more at Roark, Byron, Candice, Volkner,
Aaron and Bertha. Against Unbound, Oxide is tighter at every seat.

What Ian's ratings showed. Ian rated sixteen fights he has played in the
base ROM, on his 1 to 10 scale, on 2026-09-25 (`calibrate.py`,
IAN_RATINGS); he fought the Elite Four and Cynthia only blind, so they are
left out, and his "Mars/Jupiter Double" is the Spear Pillar tag battle.

| Fight | Ian | Threat by chance | Answers, baiting counted | Safe switch-ins | Tactics |
|---|---|---|---|---|---|
| Mars and Jupiter, Spear Pillar | 9 | 0.31 | 0.59 | 0.50 | 12 |
| Cyrus 3 | 8.5 | 0.48 | 0.26 | 0.25 | 5 |
| Saturn 2 | 8.5 | 0.39 | 0.35 | 0.36 | 7 |
| Candice | 8.5 | 0.65 | 0.18 | 0.35 | 9 |
| Wake | 8 | 0.74 | 0.19 | 0.32 | 2 |
| Maylene | 8 | 0.69 | 0.21 | 0.30 | 2 |
| Officer Hesperid, Lake Valor | 7 | 0.44 | 0.43 | 0.20 | 8 |
| Byron | 7 | 0.34 | 0.17 | 0.24 | 5 |
| Saturn 1 | 6.5 | 0.52 | 0.33 | 0.43 | 6 |
| Fantina | 6 | 0.51 | 0.27 | 0.63 | 5 |
| Barry 4 | 6 | 0.48 | 0.33 | 0.62 | 7 |
| Cyrus 1 | 5 | 0.38 | 0.54 | 0.60 | 5 |
| Mars 2 | 5 | 0.37 | 0.37 | 0.60 | 10 |
| Gardenia | 5 | 0.69 | 0.14 | 0.35 | 5 |
| Volkner | 3 | 0.58 | 0.51 | 0.35 | 4 |
| Roark | 2 | 0.14 | 0.22 | 0.81 | 4 |

Over the fifteen single battles, safe switch-ins correlate with his
ratings at minus 0.59 (minus 0.66 before the Galactic finales); the
damage readings sit between 0.27 and 0.35 either way, and the tactics
tally at 0.17. Safe switch-ins alone predict a rating it was not fitted on to
within 1.7 points, against a spread of 1.9 in his ratings, and no pair or
triple of readings does better on a fight held out. The line is about
9.3 minus 7.2 times safe switch-ins. Its misses say what is still
outside:

- **Volkner** reads 6.8 against Ian's 3. Baiting his three Choice locks
  shows in the answers (0.51, among the most of any fight), but not in
  safe switch-ins.
- **Gardenia** reads 6.8 against 5, the stage: Ian's scale rises through
  the game (later fights rate higher, correlation 0.42), and the scores
  are relative to each split's side by design.
- **Candice and Saturn 2** read 6.8 against 8.5, and Spear Pillar cannot
  be read at all, since the tool plays a double battle as singles without
  the partner. For those three, Ian's ratings are the measure.

The bellwethers now sit where Ian put them. Officer Hesperid at Lake
Valor leaves the second fewest safe switch-ins of all thirty fights,
where every damage reading had her in the bottom half. Volkner has the
eighth most answers once baiting counts. Maylene stays near the top on
damage and eighth on safe switch-ins: her fight is hard, but a player can
read it turn by turn.

The fights that leave the fewest safe switch-ins, so the hardest by this
reading, with Ian's rating where he has one:

| Fight | Safe switch-ins | Answers, baiting counted | Ian |
|---|---|---|---|
| Cynthia | 0.19 | 0.31 | not rated |
| Officer Hesperid, Lake Valor | 0.20 | 0.43 | 7 |
| Officer Hesperid, Mt. Coronet | 0.21 | 0.45 | not rated |
| Lucian | 0.22 | 0.48 | not rated |
| Flint | 0.22 | 0.42 | not rated |
| Byron | 0.24 | 0.17 | 7 |
| Cyrus 3 | 0.25 | 0.26 | 8.5 |
| Maylene | 0.30 | 0.21 | 8 |
| Wake | 0.32 | 0.19 | 8 |
| Gardenia | 0.35 | 0.14 | 5 |
| Candice | 0.35 | 0.18 | 8.5 |
| Volkner | 0.35 | 0.51 | 3 |
| Saturn 2 | 0.36 | 0.35 | 8.5 |

So the trainer pass reads safe switch-ins first, with answers (baiting
counted) and the tactics list beside it, and Ian's ratings as the target
scale; for the gyms and the League together, a 6 is about 0.56 on safe
switch-ins.

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
0.21, answers 0.50, 10 under the cap) and Candice's (0.42 and 0.27, 4
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

None. Ian's ratings of sixteen fights (open question 1 until 2026-09-25)
are in "What Ian's ratings showed".

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
  safe switch-ins read both his hack ratings (R squared 0.91) and his
  fight ratings (minus 0.59) best ("What B3b and B5 found", "What Ian's
  ratings showed"). The target: a 6 is about 0.56 on safe switch-ins over
  the gyms and the League, against Oxide's 0.37. Left: the double battle,
  which the tool cannot score, and the stage, which Ian's scale carries.
  The engine's new variable-power moves reach the scores when the
  encounter track teaches its calculator them, with one more rescore.
- [ ] **B6, the audit.** Where every Oxide fight sits today, and every lever
  on the player's side ranked by what it moves.

Then the design passes, in this order. Each proposal goes to Ian before it
lands, and each change is re-scored as it lands.

1. **Level caps.** A redesigned curve, from B4 and the target band. Moving a
   cap moves every wild level in that split, so the encounter track re-runs
   `cli evolve` against the new caps. That is coordinated through the
   Overseer and not done from here.
2. **Item access and TMs.** Which held items, marts and TMs each split
   offers, and how many TMs there are. Ian's standing rule (2026-09-25,
   staples survey): the player can never set, change or end weather, so
   TM07 Hail, TM11 Sunny Day, TM18 Rain Dance and TM37 Sandstorm go or
   become other moves. The one Ability Patch in the game (for a hidden
   ability) is the only exception, and Defog still clears fog. Choice
   items are to be nearly entirely gone from the game (Ian, 2026-09-25,
   after Volkner), up from "quite rare". When a confusion cure is first in
   reach decides how Swagger plays: at Gardenia no Persim Berry is.
3. **Species, abilities and learnsets**, including the base ROM's 228
   duplicated second ability slots. From the same answers: no weather move
   in any player learnset, tutor or egg list, and no ability that sets or
   cancels weather (Sand Stream, Snow Warning, Cloud Nine and the rest) in
   an obtainable Pokemon's regular slots; Drizzle Pelipper and Drought
   Torkoal are weighed for trainers only. Alakazam, Ampharos, Dugtrio,
   Electrode, Farfetch'd, Jumpluff, Pikachu, Roserade and Swellow get their
   modern stat buffs, Chimecho and Staraptor go to their modern totals, and
   Cresselia keeps hers. The pass weighs Magic Guard for the Abra line.
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
   against B1e's list. Also the **level 71 Lucas and Dawn fight** (trainer
   slots 779 to 784, one per starter): Ian designed it for the start of
   Victory Road, but the only script that starts it is the Battleground's,
   post-game content as in vanilla. Moving it is script and event work.
   Its level 9 and 30 counterparts (787 to 792 on Route 202, 793 to 802 on
   Route 207) are already where the story passes. **Saturn 2** (Ian,
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

Trainers can now be given a chosen nature (encounter M8), which removes the
old trade-off between a nature and IVs. One open defect has to be fixed before
the trainer pass uses the field: the packer accepts `NATURE_COUNT`, and that
hangs the game (encounter build plan, QA findings).

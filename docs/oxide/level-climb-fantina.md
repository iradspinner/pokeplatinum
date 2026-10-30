# Fantina's split: the ordinary trainers' level climb

Ian ruled on 2026-10-29 that the caps are soft, so ordinary trainers' levels climb in play order through a split, never at the cap, very rarely one under it, and with harder movesets at lower levels. The same day he asked for variety over the optimal (neutral and less common natures, items that are not the textbook pick, sets a player has not seen a thousand times) and for more of Oxide's Generation 5 and later species. This page is that pass over Fantina's split, on the branch `overseer-climb-fantina`.

## Summary

All 41 ordinary trainers of the split were rebuilt. Every one now sits two or more levels under the cap in force; none sits at the cap or one under it. Before, 22 of them topped out at the cap less one (15 at 29 under a cap of 30 on Route 206 and Route 207, and 7 at 32 under 33 on Route 208 and in the gym). Levels now rise from 23 in the Eterna building to 28 just before Lucas and Dawn 2, then from 29 on Route 208 to 31 in the gym. The sets carry the difficulty the levels gave up: status and speed control, abilities that set the plan (Skill Link, Technician, Pure Power, Huge Power, Water Bubble, Merciless, Prankster), and items picked for the member (a Thick Club Cubone, a Toxic Orb Swellow, an Air Balloon Magnemite, resist berries). Every member holds its own item and has its own nature, set by name, with no repeat inside a team.

60 species are new to their trainers, and 46 of those are Generation 5 or later. Of the split's 132 ordinary members, 49 are now post-Platinum species, about three in eight; before, 4 of 127 were.

What Ian decides:

1. The mini-bosses' honour caps. This pass used the scorer's interim values as working caps: 27 in the Eterna building (Jupiter 1), 30 from there to Lucas and Dawn 2, and 33 after them. If Jupiter 1's or Lucas and Dawn 2's cap moves, the trainers before it move with it.
2. The species changes and sets, below. Any team can go back to its old species without touching the levels.
3. The soft-cap box. The speed and damage checks here read the player's box at the cap; once Ian approves the method of a lower box for a mid-split fight, they are rerun on it (an hour).

Next steps: the Overseer lands the branch (one merge and the gate, about half an hour), then Ian plays the fights he wants to see (no new checklist item; the trainers did not move). No scorer reading was run, and none is needed unless Ian names a fight.

Trainers at the cap less one: none.

Egg-list additions wanted: none. Every move is on its species' Oxide list at its level, or is a TM the species had before the TM pass (which stays legal for trainers).

What is unverified: everything in game; the trainer AI's choices with the new sets (the AI probe was not run); the Wayward Cave pairs as doubles beside Mira; the mid-split box. Salandit's Corrosion has no reference in the engine's code and may do nothing; the set does not lean on it.

### The climb, in play order

Kinds: gauntlet (a section of `gauntlet.py`), mandatory (`required.py`, looks one way), optional (avoidable, or turns, walks or spins, which Ian counts as optional), tag (a Wayward Cave pair met beside Mira), gym.

| Trainer | Area | Kind | Cap in force | Old top | New top |
|---|---|---|---:|---:|---:|
| Galactic Grunt (1F, first) | Eterna building 1F | gauntlet, pair | 27 | 24 | 23 |
| Galactic Grunt (1F, second) | Eterna building 1F | gauntlet, pair | 27 | 24 | 24 |
| Galactic Grunt (2F, west) | Eterna building 2F | gauntlet | 27 | 24 | 24 |
| Galactic Grunt (2F, east) | Eterna building 2F | gauntlet | 27 | 24 | 24 |
| Scientist Travon | Eterna building 3F | gauntlet | 27 | 25 | 25 |
| Cyclist Axel | Route 206 | optional | 30 | 29 | 26 |
| Cyclist Megan | Route 206 | optional | 30 | 29 | 26 |
| Cyclist James | Route 206 | optional | 30 | 29 | 26 |
| Hiker Theodore | Route 206, under the bridge | optional, turns | 30 | 29 | 27 |
| Cyclist Nicole | Route 206 | optional, walks | 30 | 29 | 27 |
| Cyclist John | Route 206 | optional | 30 | 29 | 27 |
| Cyclist Ryan | Route 206 | optional | 30 | 29 | 27 |
| Cyclist Rachel | Route 206 | optional | 30 | 29 | 27 |
| Cyclist Kayla | Route 206 | optional | 30 | 29 | 28 |
| Camper Diego | Wayward Cave | tag, with Tori | 30 | 28 | 27 |
| Picnicker Tori | Wayward Cave | tag, with Diego | 30 | 28 | 27 |
| Camper Parker | Wayward Cave | tag, with Ana | 30 | 28 | 27 |
| Picnicker Ana | Wayward Cave | tag, with Parker | 30 | 28 | 27 |
| Hiker Lorenzo | Wayward Cave | tag, with Reginald | 30 | 28 | 27 |
| Hiker Reginald | Wayward Cave | tag, with Lorenzo | 30 | 28 | 28 |
| Lass Cassidy | Wayward Cave | tag, with Wayne | 30 | 28 | 27 |
| Youngster Wayne | Wayward Cave | tag, with Cassidy | 30 | 28 | 27 |
| Collector Terry | Wayward Cave | tag, with Gerald | 30 | 28 | 27 |
| Ruin Maniac Gerald | Wayward Cave | tag, with Terry | 30 | 28 | 27 |
| Hiker Kevin | Route 207 | mandatory | 30 | 29 | 27 |
| Picnicker Lauren | Route 207 | optional, pair | 30 | 29 | 27 |
| Camper Anthony | Route 207 | optional, pair | 30 | 29 | 27 |
| Youngster Austin | Route 207 | optional, walks | 30 | 29 | 28 |
| Hiker Justin | Route 207 | optional, turns | 30 | 29 | 28 |
| Battle Girl Helen | Route 207 | mandatory | 30 | 29 | 28 |
| Black Belt Kyle | Route 208 | optional, walks | 33 | 31 | 29 |
| Hiker Jonathan | Route 208 | optional, turns | 33 | 31 | 29 |
| Hiker Robert | Route 208 | mandatory | 33 | 32 | 30 |
| Aroma Lady Hannah | Route 208 | mandatory | 33 | 31 | 30 |
| Artist William | Route 208 | optional, turns | 33 | 32 | 30 |
| Youngster Donny | Hearthome Gym, room 1 | gym | 33 | 32 | 30 |
| Lass Molly | Hearthome Gym, room 1 | gym | 33 | 32 | 30 |
| School Kid Chance | Hearthome Gym, room 2 | gym | 33 | 32 | 31 |
| School Kid Mackenzie | Hearthome Gym, room 2 | gym | 33 | 32 | 30 |
| Ace Trainer Allen | Hearthome Gym, room 2 | gym, optional Ace | 33 | 30 | 30 |
| Ace Trainer Catherine | Hearthome Gym, room 2 | gym, optional Ace | 33 | 32 | 31 |

The two Eterna 2F grunts' order depends on the route the player takes through the floor; both top at 24. The gauntlet members stay at 22 to 25, the easier side of a stretch whose cap is 27.

### The teams

Every team changed in its levels and natures, and all but Artist William's in their sets and items too. A plus marks a species new to the trainer, a minus one that left; an asterisk marks Generation 5 or later.

| Trainer | Idea | Team | Species changes |
|---|---|---|---|
| Grunt 1F, first | Fake Out and paralysis, then dark cats chip | Glameow 22, Stunky 22, Liepard* 23 (Prankster Thunder Wave, Foul Play) | +Liepard, minus Skitty |
| Grunt 1F, second | poison the field, then punish the poisoned | Koffing 23, Salandit* 23, Mareanie* 24 (Merciless, Venoshock) | +Salandit, +Mareanie, minus Zubat and Stunky |
| Grunt 2F, west | hazards and grime | Glimmet* 23 (Toxic Debris, Stealth Rock), Grimer 23, Nidorina 24 | +Glimmet, minus Glameow |
| Grunt 2F, east | sleep and punish | Bronzor 22 (Hypnosis), Murkrow 22, Vullaby* 23, Croagunk 24 | +Vullaby (three became four) |
| Travon | screens and machines | Porygon 24, Charjabug* 24, Klefki* 25 (Prankster screens) | +Charjabug, +Klefki, minus Voltorb and Kadabra |
| Axel | paralysis and speed | Joltik* 25, Plusle 25, Manectric 26 | +Joltik, minus Pikachu |
| Megan | multi-hit moves through Sturdy and a Sash | Minccino* 25 (Skill Link, King's Rock), Furret 25, Trumbeak* 26 (Skill Link Rock Blast) | +Minccino, +Trumbeak, minus Staravia and Luxio |
| James | fire with burns and a Nasty Plot | Houndour 25, Braixen* 26, Growlithe 26 | +Braixen, minus Ponyta and Vulpix |
| Theodore | Stealth Rock, then rocks that hit hard | Dwebble* 26 (Custap), Larvitar 26 (Guts, Flame Orb), Graveler 27 | +Dwebble, minus Onix |
| Nicole | fairy bulk and recovery | Clefairy 26 (Eviolite, Wish), Dubwool* 26, Sylveon* 27, Wigglytuff 27 | +Dubwool, +Sylveon, minus Igglybuff and Jigglypuff |
| John | birds with status orbs and priority | Doduo 26, Corvisquire* 26, Fletchinder* 27, Swellow 27 (Guts, Toxic Orb) | +Corvisquire, +Fletchinder, minus Pidgeotto and Staravia |
| Ryan | Endure into Reversal with pinch berries | Riolu 26 (Liechi), Mienfoo* 26, Primeape 27 (Salac) | +Mienfoo, minus Monferno |
| Rachel | speed and pivots | Pachirisu 26, Raboot* 27 (Libero), Rapidash 27 | +Raboot, minus Voltorb and Ponyta |
| Kayla | steel walls with Iron Barbs and paralysis | Ferroseed* 27, Togedemaru* 27, Magnemite 28 (Air Balloon) | +Ferroseed, +Togedemaru, minus Voltorb and Bronzor |
| Diego | Technician | Kricketune 26, Clobbopus* 26, Ambipom 27 | +Kricketune, +Clobbopus, minus Aipom |
| Tori | bulky support beside a partner | Slowpoke 26, Dolliv* 26 (Harvest, Strength Sap), Alomomola* 27 | +Dolliv, +Alomomola, minus Clefairy |
| Parker | water rushers | Buizel 26, Luxio 26, Araquanid* 27 (Water Bubble) | +Araquanid |
| Ana | owls and sleep in the dark | Natu 26 (Magic Bounce), Dottler* 26, Noctowl 27 | +Natu, +Dottler, minus Hoothoot |
| Lorenzo | rock walls that slow the player | Nosepass 26, Onix 26 (Weak Armor), Carbink* 27 | +Nosepass, +Carbink, minus Geodude |
| Reginald | recoil, salt and ground | Sudowoodo 26 (Rock Head Wood Hammer), Nacli* 26, Donphan 28 | +Nacli; Bonsly and Phanpy evolved |
| Cassidy | charm and kicks | Snubbull 26, Lopunny 26, Tsareena* 27 (Queenly Majesty) | +Snubbull, +Tsareena; Buneary left |
| Wayne | fire and flight momentum | Staravia 26 (Reckless Double-Edge), Ponyta 26, Charcadet* 27 | +Charcadet, minus Growlithe |
| Terry | baby dragons | Jangmo-o* 26, Goomy* 26, Gible 27 (Rough Skin, Rocky Helmet) | +Jangmo-o, +Goomy, minus Bagon |
| Gerald | the ruins' old curses | Baltoy 26, Yamask* 26 (Mummy), Bronzor 27 | +Baltoy, +Yamask, minus Graveler |
| Kevin | ground bruisers behind Stealth Rock | Phanpy 26, Cubone 26 (Thick Club), Rhyhorn 26, Glimmet* 27 | +Rhyhorn, +Glimmet, minus Geodude, Onix and Graveler (five became four) |
| Lauren | cute electrics | Emolga* 26 (Motor Drive), Flaaffy 26, Marill 27 (Huge Power) | +Flaaffy, minus Pachirisu |
| Anthony | the Alolan starters | Dartrix* 26, Brionne* 26, Torracat* 27 (Intimidate) | the Sinnoh starters gave way to Alola's |
| Austin | tricksters: Dry Skin, Immunity, Protean | Croagunk 27, Gligar 27, Frogadier* 28 (Protean) | +Croagunk, +Frogadier, minus Buizel and Luxio |
| Justin | ground and sand | Diglett 26, Sandshrew 27 (Eviolite), Hippopotas 28 | +Hippopotas, minus Nosepass and Gligar |
| Helen | Fake Out, Pure Power and Iron Fist | Makuhita 26, Meditite 27 (Pure Power), Pawmo* 28 (Iron Fist) | +Pawmo, minus Riolu and Machoke |
| Kyle | Technician kicks and a flying ace | Hitmontop 28 (Technician), Machoke 28 (No Guard), Hawlucha* 29 (Unburden) | +Hawlucha, minus Hitmonchan |
| Jonathan | poison and ground pressure | Nidorina 28, Nidorino 28, Clodsire* 29 (Unaware, Spikes), Dugtrio 29 | +Clodsire, minus Gligar |
| Robert | walls that hit back | Steelix 29 (Sheer Force), Bastiodon 29, Naclstack* 30 | +Bastiodon, +Naclstack, minus Graveler and Sudowoodo |
| Hannah | grass status: sleep, paralysis and drain | Roselia 29, Cherrim 29, Leavanny* 29, Sinistcha* 30 (Matcha Gotcha) | +Leavanny, +Sinistcha, minus Sunflora and Jumpluff |
| William | screens, then a Protean finisher | Mime Jr. 29, Floette* 29, Kecleon 30 | none; levels and natures only (Timid, Modest and Adamant gave way) |
| Donny | ghosts that steal tempo | Duskull 29, Drifloon 29, Sinistea* 29 (White Herb), Haunter 30 | +Sinistea, minus Gastly |
| Molly | burn and wear down | Frillish* 29, Misdreavus 29, Shuppet 30 | +Frillish, minus Duskull |
| Chance | Shedinja's Wonder Guard behind a fast Ninjask | Nincada 29, Ninjask 30 (Speed Boost, Swords Dance), Shedinja 31 | none |
| Mackenzie | sand and shadows | Gastly 29, Spiritomb 30, Sandygast* 30 | all three: Shuppet, Litwick and Drifloon left |
| Allen | Prankster burns and slow ghosts | Sableye 29 (Prankster), Misdreavus 29, Duskull 29, Banette 30 | none, as the brief keeps his species |
| Catherine | burns, then a Nasty Plot and a fast finisher | Litwick* 30, Misdreavus 30, Drifblim 30, Haunter 31 | none, as the brief keeps her species |

Team sizes moved where the idea asked for it: the ten Wayward Cave trainers went from two to three each, Grunt 2F east from three to four, and James, Rachel, Justin and Helen from four to three, Kevin from five to four. The script index is regenerated for the new sizes.

## How the teams were checked

Each check below was run on the saved files, and each passed.

| Check | Result |
|---|---|
| The trainer lint, on every changed team | no errors, no warnings |
| The packer, through the team builder's save | every team packed; the importer's register records each |
| Every move legal at its level (Oxide's own lists, plus pre-TM-pass TMs) | all 528 moves legal |
| No item or nature repeated in a team, every nature named | none repeated, none missing |
| No ordinary trainer at the cap or one under it | none |
| Pairs fought alone field six at most (`pairs.pairs()`) | Lauren and Anthony 6; the two 1F grunts 6; the Wayward Cave pairs 6 each, with Mira beside the player |
| The team builder's own tests (`test_trainers`) | 44 of 44 |

The rules were read against every team: no one-hit KO move, no evasion move or evasion ability in play (Diglett and Dugtrio take Sand Force, which does nothing without sand), no trapping move or ability, no forced trade (no Explosion, Self-Destruct, Memento, Destiny Bond or Final Gambit), no Choice item and no Life Orb, and three to five Pokemon each. Oxide's own abilities were read from the species files, since several differ from the later games: Furret, Riolu and Pachirisu have Adaptability, Hitmontop has Technician, Primeape No Guard, Lopunny Scrappy, Rapidash Reckless and Steelix Sheer Force.

### Speed against the box

The box is goal 3's, rolled at its fight's cap (`plgoal3 --box`), with neutral natures and IVs of 15; the trainers' members carry their natures and their trainer's IVs. A mid-split box will sit lower once Ian approves that method, which makes every trainer below a little faster against it.

| Box at level | Fastest likely answers |
|---|---|
| 28 | Liepard 74, Haunter 70, Ninetales-Alola 65, Sharpedo 62, Luxray 62, Raboot 61, Golbat 59 |
| 30 | Liepard 79, Haunter 75, Ninetales-Alola 69, Sharpedo 66, Luxray 66, Raboot 65, Golbat 63 |
| 33 | Liepard 86, Haunter 82, Ninetales-Alola 75, Sharpedo 72, Luxray 72, Raboot 71, Golbat 69 |

The members that outrun the box's fastest answers are few, and each is its trainer's danger by design. Under the cap of 30: Ambipom 81, Swellow 79, Manectric, Frogadier and Lopunny 72, Rapidash 71, and Raboot 68 and Diglett 67 just behind them. Under the cap of 33: Ninjask 119 with Speed Boost on top, Dugtrio 90, Haunter 86 (Donny) and 82 (Catherine), and Hawlucha 80, which doubles once its Sitrus Berry is gone. In the Eterna building only the first grunt's Prankster Liepard (69) outruns nearly the whole box. Emolga 65, Pawmo 64 and Togedemaru 63 sit level with the box's middle tier (Luxray and Sharpedo, 62 at level 28); every other member sits under it, most well under Golbat.

### Damage in the key exchanges

The box's members at the stretch's cap less one or two (the level a player riding the line would have), against each trainer's danger. Ranges are a share of the defender's HP.

| Attacker | Move | Defender | Damage |
|---|---|---|---:|
| Liepard 23 (1F grunt) | Foul Play | Staravia 26 | 54 to 66% |
| Mareanie 24 | Venoshock (unpoisoned) | Grotle 26 | 41 to 48% |
| Manectric 26 (Axel) | Discharge | Staravia 28 | 175 to 208% |
| Grotle 28 | Bulldoze | Manectric 26 | 48 to 58% |
| Trumbeak 26 (Megan) | Skill Link Rock Blast | Golbat 28 | 95 to 119% |
| Houndour 25 (James) | Flamethrower, before Nasty Plot | Luxray 28 | 49 to 59% |
| Swellow 27 (John) | Facade, before its orb | Luxray 28 | 28 to 34% |
| Luxray 28 | Wild Charge | Swellow 27 | 136 to 165% |
| Araquanid 27 (Parker) | Water Bubble Waterfall | Luxray 28 | 58 to 68% |
| Cubone 26 (Kevin) | Thick Club Bonemerang | Luxray 29 | 107 to 125% |
| Grotle 29 | Razor Leaf | Cubone 26 | 55 to 70% |
| Marill 27 (Lauren) | Huge Power Play Rough | Luxray 29 | 83 to 101% |
| Meditite 27 (Helen) | Pure Power Drain Punch | Luxray 29 | 80 to 96% |
| Staravia 29 | Dual Wingbeat | Meditite 27 | 140 to 166% |
| Hawlucha 29 (Kyle) | Flying Press | Torterra 32 | 52 to 63% |
| Luxray 32 | Wild Charge | Hawlucha 29 | 112 to 131% |
| Sinistcha 30 (Hannah) | Matcha Gotcha | Quagsire 32 | 150 to 182% |
| Haunter 32 | Shadow Ball | Sinistcha 30 | 88 to 106% |
| Fletchinder 32 | Flame Charge | Sinistcha 30 | 15 to 22% (Heatproof) |
| Steelix 29 (Robert) | Sheer Force Iron Head | Ninetales-Alola 32 | 210 to 247% |
| Torterra 32 | Earthquake | Steelix 29 | 46 to 53% |

Two sets were softened after this table's first run. Salandit's Sludge Bomb took 87 to 107% from a Grotle in the gauntlet, so it became Smog, keeping the grunts on the easier side. Kevin's Cubone lost Rock Slide, so that the box's flyers, immune to Bonemerang, answer it cleanly; with Rock Slide it would have taken a Staravia in one hit as well.

The biggest single threats are ones a player sees coming and has an answer to in the box: Cubone and Araquanid are slow, Swellow and Hawlucha fall to one electric hit, Marill to an electric or grass hit, Meditite to a flyer, and Sinistcha to the box's fire, flying and ghost types.

## Out of scope and left alone

Fantina, Lucas and Dawn on Route 207 (the files dummy_793 to dummy_802), Jupiter 1 and Officer Moira are untouched. Allen's and Catherine's species stand, as asked; their levels and sets follow the climb. Camper Drew and Picnicker Cheyenne stand in the Diamond and Pearl gym rooms, which connect to nothing in Platinum, so they are left as they are. Mira, the partner in Wayward Cave, is untouched.

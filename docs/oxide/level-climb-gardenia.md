# The level climb in Gardenia's split

Ian ruled on 2026-10-29 that the caps are soft, so ordinary trainers' levels climb in play order through a split, never at the cap, very rarely one under it, with harder and less textbook sets at lower levels. He asked for it in Gardenia's split "now", after the Fantina and Maylene climbs. This page is that climb, from Jubilife's grunts after Roark to the Eterna gym, on the branch `overseer-climb-gardenia`.

## Summary

All 38 ordinary teams of the split were rebuilt. Two caps are in force. Up to Mars 1 at the Valley Windworks it is Mars 1's honour cap of 20, Ian's final value of 2026-10-29 ("a little more breathing room after roark"); after Mars 1 it is Gardenia's 26. Every ordinary trainer now tops out two or more levels under the cap in force, and none sits at the cap or one under it.

| Stretch | Cap in force | Old top levels | New top levels |
|---|---:|---:|---:|
| Jubilife grunts' tag battle, after Roark | 20 | 17 | 16 |
| Route 204 South | 20 | 17 to 18 | 17 |
| Route 204 North | 20 | 17 to 18 | 17 |
| Floaroma Meadow grunts | 20 | 18 | 18 |
| Valley Windworks grunts | 20 | 18 | 18 |
| Route 205 South, the bridge | 26 (Joseph 20, see below) | 24 to 25 | 18 to 20 |
| Route 205 South, north of the bridge | 26 | 25 | 20 to 21 |
| Eterna Forest | 26 | 24 | 22 |
| Route 205 North | 26 | 25 | 22 |
| Route 211 West (off the path) | 26 | 25 | 22 to 23 |
| Eterna Gym | 26 | 25 | 23 to 24 |

Before Mars 1 the levels barely move, since the old tops sat at 17 and 18 and the cap rose from 19 to 20. After Mars 1 they come down hard: Route 205 and the forest stood at 24 and 25, one under Gardenia's cap, straight after a boss whose ace is 20. They now start at 18 to 20 by the bridge and climb to 24 in the gym, so a player who spends the split's experience late meets each trainer a level or two under their own team.

Fisherman Joseph stands at the foot of the Route 205 bridge, where a player can reach him on the way to the Windworks before Mars 1 (the tile model reads him avoidable on that crossing and required on the way back). His team tops at 18, two under the earlier cap, so he is fair on either visit.

50 species are new to their trainers, and 38 of those are from after Platinum, so 38 of the 128 members are now later species, about three in ten; before, none of the split's 135 ordinary members was. Natures went off the textbook: Adamant, Jolly, Modest and Timid fell from 24 members to one Timid Mime Jr., and every member has a named nature where 109 had none. Every member holds its own item, where 97 held nothing.

Trainers at the cap less one: none.

Egg-list additions: none. Every move is on its species' Oxide list at its level, or is a TM the species had before the TM pass, which stays legal for trainers.

What Ian decides:

1. The teams below, as a set. Any team can go back to its old species without touching the levels.
2. Whether the drop after Mars 1 is the right size. Route 205 and the forest came down three to five levels, more than the one to three of the Fantina and Maylene climbs, because their old levels sat one under Gardenia's cap right after a boss at 20.

Next steps: the Overseer lands the branch (one merge and the gate, about half an hour), then Ian plays the fights he wants to see. No scorer reading was run, and none is needed unless Ian names a fight.

What is unverified:

- Nothing has been seen in game. The real packer accepted every team.
- The trainer AI's choices with the new sets (the AI probe was not run), and the AI does not see several held items these teams carry (Rocky Helmet, Loaded Dice, Absorb Bulb, Sticky Barb, the tracker's battle AI item 3).
- The doubles were checked as singles: the Jubilife tag battle beside Lucas or Dawn, Twins Liv and Liz, and the five Eterna Forest pairs beside Cheryl.
- The speed and damage checks read the box near the cap; the soft-cap box for a mid-split fight will sit lower once Ian approves that method, so every margin here is a little kinder to the player than the fight will be.
- The calculator does not resolve Faint Attack, and it does not double Hex against a statused target, so neither was damage-checked as it plays.
- The Eterna gym's order (Caroline and Jenna at 23, Angela and Lindsay at 24) is read from the old levels, not walked.
- Joseph's two visits come from the tile model's crossings, not the game.
- `docs/oxide/trainer-roles.tsv` still lists the old team sizes and the trainers the early placement moved; regenerating it rewrites rows other branches change, so it is left for the Overseer, as before.
- The packer used for the saves is a copy of the main checkout's build (with its yyjson library from there), since this worktree has no build of its own.

## The climb, in play order

Kinds: mandatory (`required.py`, or a story script), optional (avoidable, or turns, walks or spins, which Ian counts as optional), tag (fought beside a partner), gym.

| Trainer | Area | Kind | Cap in force | Old top | New top |
|---|---|---|---:|---:|---:|
| Galactic grunts (two) | Jubilife City | tag, beside Lucas or Dawn | 20 | 17 | 16 |
| Youngster Tyler | Route 204 South | optional | 20 | 18 | 17 |
| Lass Samantha | Route 204 South | mandatory | 20 | 18 | 17 |
| Lass Sarah | Route 204 South | optional, turns | 20 | 17 | 17 |
| Bug Catcher Brandon | Route 204 North | optional | 20 | 18 | 17 |
| Aroma Lady Taylor | Route 204 North | optional, turns | 20 | 18 | 17 |
| Twins Liv and Liz | Route 204 North | mandatory, double | 20 | 17 | 17 |
| Galactic Grunt, first | Floaroma Meadow | mandatory, scripted | 20 | 18 | 18 |
| Galactic Grunt, second | Floaroma Meadow | mandatory, straight after | 20 | 18 | 18 |
| Galactic Grunt outside | Valley Windworks | mandatory | 20 | 18 | 18 |
| Galactic Grunt inside | Valley Windworks | optional, spins | 20 | 18 | 18 |
| Fisherman Joseph | Route 205 South | optional before Mars 1, mandatory after | 20, then 26 | 25 | 18 |
| Fisherman Andrew | Route 205 South | mandatory | 26 | 24 | 20 |
| Camper Jacob | Route 205 South | optional, turns | 26 | 25 | 20 |
| Hiker Daniel | Route 205 South | optional, turns | 26 | 25 | 20 |
| Aroma Lady Elizabeth | Route 205 South | optional, spins | 26 | 25 | 20 |
| Camper Zackary | Route 205 South | optional, walks, TM62 | 26 | 25 | 21 |
| Picnicker Siena | Route 205 South | optional, wanders | 26 | 25 | 21 |
| Hiker Nicholas | Route 205 South | optional, turns | 26 | 25 | 21 |
| Battle Girl Kelsey | Route 205 South | optional, walks, pair with Karina | 26 | 25 | 21 |
| Picnicker Karina | Route 205 South | optional, TM57, pair with Kelsey | 26 | 25 | 21 |
| Bug Catcher Jack and Lass Briana | Eterna Forest | mandatory, beside Cheryl | 26 | 24 | 22 |
| Psychics Elijah and Lindsey | Eterna Forest | mandatory, beside Cheryl | 26 | 24 | 22 |
| Psychics Kody and Rachael | Eterna Forest | mandatory, beside Cheryl | 26 | 24 | 22 |
| Bug Catchers Donald and Phillip | Eterna Forest | optional, Eviolite and Absorb Bulb, beside Cheryl | 26 | 24 | 22 |
| Fisherman Zachary | Route 205 North | optional, TM88 | 26 | 25 | 22 |
| Bird Keeper Alexandra | Route 211 West | off the path, Cell Battery | 26 | 25 | 23 |
| Ninja Boy Zach | Route 211 West | off the path | 26 | 25 | 22 |
| Hiker Louis | Route 211 West | off the path, TM66 | 26 | 25 | 23 |
| Lass Caroline | Eterna Gym | gym | 26 | 25 | 23 |
| Aroma Lady Jenna | Eterna Gym | gym | 26 | 25 | 23 |
| Aroma Lady Angela | Eterna Gym | gym | 26 | 25 | 24 |
| Beauty Lindsay | Eterna Gym | gym | 26 | 25 | 24 |

## The teams

Each line gives the team in the order it is sent out and what changed. An asterisk marks a species from after Platinum.

| Trainer | Idea | Team | Species changes |
|---|---|---|---|
| Jubilife grunt, first | poison chip with a Fake Out lead beside the partner | Zubat 15, Stunky 15, Croagunk 16 (Poison Touch) | none; sets, items and natures |
| Jubilife grunt, second | sleep and Prankster paralysis | Glameow 15 (Hypnosis), Bronzor 15, Purrloin* 16 (Prankster Thunder Wave) | +Purrloin, minus Murkrow |
| Tyler | Wingull's Tailwind moves a slow water team | Wingull 16, Dewpider* 16 (Water Bubble), Psyduck 16, Barboach 17 | +Dewpider, minus Lotad |
| Samantha | status first, then Hex and drain | Budew 16, Vulpix 16 (Will-O-Wisp, Hex, Spell Tag), Flabebe* 16, Shellos 17 (Yawn) | +Flabebe, minus Ponyta |
| Sarah | cute normals that hit many times | Wooloo* 16, Minccino* 16 (Skill Link), Furret 17 | +Wooloo, +Minccino, minus Skitty, Meowth and Luxio (four became three) |
| Brandon | Sticky Web, then bugs that outpace the slowed player | Grubbin* 16, Sewaddle* 16 (Eviolite), Kricketune 16 (Technician), Beautifly 17 | +Grubbin, +Sewaddle, minus Combee, Nincada and Dustox (five became four) |
| Taylor | sleep, Leech Seed and drains that outlast | Bellsprout 16, Smoliv* 16 (Harvest), Cherubi 16, Tangela 17 (Regenerator, Rocky Helmet) | +Smoliv, minus Oddish |
| Liv and Liz | Plus and Minus with Helping Hand | Plusle 16, Minun 16, Pawmi* 17 | +Pawmi, minus Pachirisu |
| Meadow grunt, first | Glare, then pressure on the paralysed | Ekans 17, Murkrow 17 (Super Luck, Scope Lens), Salandit* 18 (Flame Burst, Shuca Berry) | +Salandit, minus Croagunk |
| Meadow grunt, second | burns and Knock Off behind bulk | Yamask* 17 (Mummy, Will-O-Wisp), Skorupi 17, Vullaby* 18 (Eviolite, Tailwind) | all three: Glameow, Stunky and Zubat left |
| Windworks grunt outside | poison walls: Stealth Rock, Toxic Debris, burns and Yawn | Koffing 17, Glimmet* 17, Gulpin 18 (Gluttony Figy Berry) | +Glimmet, minus Grimer |
| Windworks grunt inside | the Windworks' stolen power: paralysis and steel | Joltik* 17 (Compound Eyes), Magnemite 18 (Sturdy), Croagunk 18 | +Joltik, +Magnemite, minus Grimer and Koffing |
| Joseph | Toxic Spikes, a Skill Link Shellder, an Unaware Wooper | Tentacool 17, Shellder 17, Wooper 18 | +Wooper, minus Quagsire |
| Andrew | the river's catch, each with a trick | Goldeen 19 (Lightning Rod, Scald), Remoraid 19 (Hustle Rock Blast, Wide Lens), Frillish* 19, Mareanie* 19 (Regenerator, Toxic), Qwilfish 20 (Intimidate, Spikes, Barb Barrage) | +Frillish, +Mareanie, minus Magikarp, Feebas and Gyarados (six became five) |
| Jacob | fire with burns and speed, and a Magician Braixen | Growlithe 19 (Intimidate, Will-O-Wisp), Braixen* 19, Houndour 19, Larvesta* 20 (Flame Body) | +Braixen, +Larvesta, minus Ponyta and Monferno |
| Daniel | Stealth Rock and screens, then a Defense Curl Rollout | Nacli* 20 (Recover), Baltoy 20 (Light Clay), Sandygast* 20, Graveler 20 | +Nacli, +Sandygast, minus Sandshrew and Phanpy |
| Elizabeth | Sunny Day for Chlorophyll and a Solar Power Sunflora | Gloom 19 (Heat Rock), Fomantis* 19 (Leaf Guard), Sunflora 20 | +Fomantis, minus Vulpix |
| Zackary | hail from a Snow Warning Snover | Snover 21, Spheal 20 (Ice Body, Eviolite), Castform 20 | +Spheal, minus Wingull and Vulpix (four became three) |
| Siena | electric hitters behind a Switcheroo Iron Ball | Linoone 20, Electrike 20, Pachirisu 21 (Adaptability), Pawmo* 21 | +Pawmo, minus Plusle and Luxio (five became four) |
| Nicholas | ground and rock that set up | Cubone 20 (Swords Dance), Dwebble* 20 (Loaded Dice Rock Blast), Rhyhorn 21 | +Dwebble, minus Graveler |
| Kelsey | Belly Drum, Adaptability and Pure Power | Makuhita 21 (Belly Drum, Sitrus Berry), Riolu 21, Meditite 21 (Punching Glove) | none; Ian's three, sets and levels |
| Karina | the water starters of other regions | Marshtomp 21, Brionne* 21, Croconaw 21 (Dragon Dance) | +Brionne, minus Prinplup (a player's starter) |
| Jack | Compound Eyes sleep and Sniper crits beside Cheryl | Butterfree 21, Beedrill 21 (Sniper, Focus Energy), Ninjask 22 | none |
| Briana | Follow Me and Encore for her partner | Clefairy 21 (Eviolite), Floette* 21, Vigoroth 22 | +Floette, minus Marill |
| Elijah | Fake Tears into a Calm Mind Kadabra | Gothita* 21 (Competitive), Spoink 21, Kadabra 22 | +Gothita, minus Wynaut (its one ability, Shadow Tag, traps) |
| Lindsey | screens, then a Calm Mind Kirlia | Dottler* 21, Natu 21 (Magic Guard, Sticky Barb), Kirlia 22 | +Dottler, minus Exeggcute |
| Kody | Trick Room for two slow psychics | Galarian Mr. Mime* 21 (Mental Herb), Slowpoke 21 (Curse), Drowzee 22 | +Galarian Mr. Mime, minus Spoink |
| Rachael | bulky psychics that stall with Reflect and Yawn | Mime Jr. 21, Chingling 21, Bronzor 22 | +Mime Jr., +Bronzor, minus Meditite and Kadabra |
| Donald | Toxic Spikes, then bug walls that bite back | Pineco 21 (Eviolite), Charjabug* 21, Vespiquen 22 | +Charjabug, minus Skorupi |
| Phillip | Speed Boost, Toxic and a sleeping Swadloon | Yanma 21, Dustox 21, Swadloon* 22 (Absorb Bulb) | +Swadloon, minus Ninjask |
| Zachary | Tailwind for a water team, with Adaptability | Finneon 21, Chinchou 22, Corphish 22 (Ceaseless Edge), Quagsire 22 (Unaware) | none |
| Alexandra | birds with Unnerve, screens and Skill Link | Corvisquire* 22, Noctowl 22 (Tinted Lens, Light Clay), Trumbeak* 22, Swellow 23 (Scrappy Facade) | +Corvisquire, +Trumbeak, +Swellow, minus Taillow, Swablu, Murkrow and Staravia (five became four) |
| Zach | a ninja's tricks: Fake Out, Protean and Sucker Punch | Nuzleaf 22, Croagunk 22, Frogadier* 22 (Protean) | +Croagunk, +Frogadier, minus Parasect, Breloom and Ninjask (four became three) |
| Louis | the mountain's walls | Sableye 22 (Will-O-Wisp, Recover), Carbink* 22 (Stealth Rock), Mawile 23 (Intimidate, Swords Dance) | +Carbink, minus Bronzor |
| Caroline | sleep and Leech Seed, then a Calm Mind Servine | Skiploom 22, Steenee* 22, Servine* 23 | +Steenee, +Servine, minus Hoppip and Breloom |
| Jenna | poison grass: Stun Spore, Swords Dance and drain | Gloom 22, Weepinbell 22 (Gluttony Salac Berry), Cacnea 22 (Water Absorb), Carnivine 23 | +Cacnea, +Carnivine, minus Exeggutor and Nuzleaf |
| Angela | Spikes, then walls that heal | Roselia 23, Lileep 23 (Recover), Lombre 23, Dolliv* 24 (Harvest, Strength Sap) | +Lombre, +Dolliv, minus Sunflora and Ludicolo |
| Lindsay | Stealth Rock and Iron Barbs, then a Fake Out Shiftry | Ferroseed* 23 (Rocky Helmet), Tangela 23 (Eviolite), Exeggcute 23, Shiftry 24 | +Ferroseed, +Exeggcute, minus Roselia and Bellsprout |

The species that left are mostly ones Gardenia herself, Cheryl or the player's own box already field (Breloom, Exeggutor, Sunflora, Prinplup, Luxio, Staravia). Team sizes moved where the idea asked for it, and every team keeps three to five. The Floaroma Meadow grunts stay three each, six between two fights a script runs back to back with no healing, as Ian set them. Kelsey and Karina stay three each, six for the pair.

## How the teams were checked

| Check | Result |
|---|---|
| The trainer lint, on every changed team | no errors, no warnings |
| The packer, through the team builder's save | every team packed; the importer's register records each |
| Every move legal at its level (Oxide's own lists, plus pre-TM-pass TMs) | all 506 moves legal |
| No item or nature repeated in a team, every nature named, every member holding an item the calculator names | none repeated, none missing |
| No ordinary trainer at the cap or one under it | none |
| Pairs fought alone field six at most (`pairs.pairs()`) | Kelsey and Karina 6, the only such pair in the split; the forest pairs 6 each beside Cheryl |
| `test_trainers` | 44 of 44 |
| `test_m8` | 112 of 112 |

The rules were read against every team. There is no one-hit KO move, no forced trade (no Explosion, Self-Destruct, Memento or Destiny Bond), no trapping move or ability (Magnemite takes Sturdy, not Magnet Pull; Gothita takes Competitive, not Shadow Tag), and no evasion move or ability. Snorunt was tried in Zackary's hail team and taken out, since Snow Cloak raises its evasion in hail; Spheal's Ice Body replaced it. No member holds a Choice item or a Life Orb. Oxide's own abilities were read from the species files, since several differ from the later games: Furret, Riolu and Pachirisu have Adaptability, Snover has Adaptability in its first slot, and Meditite has Pure Power.

### Speed against the box

The box is goal 3's three Mars 1 and Gardenia boxes, with neutral natures and IVs of 15; the trainers' members carry their natures and their trainer's IVs.

| Box at level | Fastest likely answers |
|---|---|
| 18 | Liepard 49, Alolan Ninetales 43, Raboot 41, Pachirisu 41, Golbat 40, Tsareena 40 |
| 23 | Liepard 61, Alolan Ninetales 54, Pachirisu 52, Raboot 51, Tsareena 50, Golbat 49 |
| 26 | Liepard 69, Alolan Ninetales 60, Pachirisu 58, Raboot 57, Tsareena 56, Golbat 55 |

Before Mars 1 only the first meadow grunt's Murkrow (44) and Liv and Liz's Minun (42) outrun the box's middle tier; every other member sits at or under 40. After Mars 1 five members outrun the box's fastest answers at 23, each its trainer's danger by design: Jack's Ninjask 80 with Speed Boost, Alexandra's Swellow 68, Elijah's Kadabra 61, Zach's Frogadier 57 and Phillip's Yanma 53, also with Speed Boost. Every other member sits at or under 50.

### Damage in the key exchanges

The box's members at about the level a player riding the line would have. Ranges are a share of the defender's HP.

| Attacker | Move | Defender | Damage |
|---|---|---|---:|
| Vulpix 16 (Samantha) | Incinerate | Grotle 17 | 65 to 80% |
| Prinplup 17 | Bubble Beam | Vulpix 16 | 61 to 76% |
| Minccino 16 (Sarah) | Skill Link Fury Swipes | Staravia 17 | 43 to 56% |
| Kricketune 16 (Brandon) | Technician Bug Bite | Grotle 17 | 65 to 80% |
| Staravia 17 | Wing Attack | Kricketune 16 | 56 to 66% |
| Salandit 18 (meadow) | Flame Burst | Grotle 18 | 63 to 77% |
| Prinplup 18 | Bubble Beam | Salandit 18 | 85 to 102% |
| Joltik 17 (Windworks) | Electroweb | Staravia 18 | 72 to 88% |
| Shellder 17 (Joseph) | Skill Link Icicle Spear | Staravia 19 | 57 to 80% |
| Luxio 19 | Spark | Shellder 17 | 78 to 102% |
| Qwilfish 20 (Andrew) | Barb Barrage, before poison | Grotle 21 | 67 to 83% |
| Sunflora 20 (Elizabeth) | Solar Power Mega Drain in sun | Prinplup 21 | 72 to 88% |
| Fletchinder 21 | Flame Charge in sun | Sunflora 20 | 78 to 93% |
| Snover 21 (Zackary) | Icy Wind in hail | Staravia 21 | 119 to 147% |
| Pachirisu 21 (Siena) | Adaptability Spark | Prinplup 21 | 78 to 98% |
| Makuhita 21 (Kelsey) | Arm Thrust after Belly Drum | Grotle 22 | 92 to 110% |
| Staravia 22 | Wing Attack | Makuhita 21 | 90 to 109% |
| Croconaw 21 (Karina) | Waterfall | Raboot 22 | 85 to 104% |
| Grotle 22 | Razor Leaf | Croconaw 21 | 50 to 66% |
| Trumbeak 22 (Alexandra) | Skill Link Rock Blast | Raboot 23 | 54 to 72% |
| Luxio 23 | Spark | Swellow 23 | 72 to 84% |
| Weepinbell 22 (Jenna) | Leech Life after Swords Dance | Grotle 24 | 82 to 98% |
| Staravia 24 | Wing Attack | Weepinbell 22 | 81 to 100% |
| Shiftry 24 (Lindsay) | Leaf Tornado | Prinplup 24 | 70 to 82% |

One set was softened after this table's first run: Elizabeth's Sunflora carried Giga Drain, which took 137 to 160% of a Prinplup in sun, so it became Mega Drain. Each big threat is one a player sees coming and has an answer for in the box: Makuhita and Weepinbell must set up first and fall to one flying hit, Snover is slow and frail to fire, Salandit and Shellder fall to one water or electric hit, and Croconaw takes Grotle's Razor Leaf.

## Out of scope and left alone

Gardenia, Officer Somnu 1 (`galactic_grunt_valley_windworks_3`), Mars 1, the Lucas and Dawn partner files at Jubilife, and Cheryl and her own battle are untouched. Mars 1's ace moves to 20 on another branch.

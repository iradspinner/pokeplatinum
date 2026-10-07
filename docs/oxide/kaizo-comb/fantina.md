# The comb: Fantina's split

Every trainer of Fantina's split is combed, in walking order: 50 files beside
this one, all passing the checker. The cap is 27 through Team Galactic's
Eterna building and Jupiter 1, 30 from Route 206 to Lucas and Dawn 2 (Route
207's trainers stand before their trigger), and 33 after them. Two trainers
in `trainers.csv` are left out: Camper Drew and Picnicker Cheyenne stand only
in the old Diamond and Pearl gym rooms, which nothing in the game connects to.

The Eterna building is the first gauntlet: 1F and 2F are one section of four
grunts built on chip and status that follows the player between fights,
and 3F is a second, Scientist Travon then Officer Moira. Route 206's cyclists
are speed and pinch-berry teams, Wayward Cave's five pairs are tag battles
beside Mira, and the Hearthome gym's trainers rehearse Fantina's burns and
Ghosts. Lucas and Dawn 2 has six files, one per counterpart and starter.

None of this has been read by the scorer. The expected numbers come from my
own rough simulator (blind sixes from `blind-pools.md`, weather, Spikes, and a
six search that ranks the box on paper first), corrected against the scorer's
readings of Roark's split. They are against the scorer's boxes at 27, 30 and
33, which know no TMs, so every fight here reads harsher than it will once
the TM pass arms the box. Bosses are set against today's files, as the
Overseer advised, each a step harder than today's in my simulator: Jupiter 97
won to today's 100, Lucas and Dawn about level, Fantina 55 to today's 60
(the scorer read today's Fantina at 92). The ordinary singles average about
90 clean in the scorer's terms (75 to 99), and the two gauntlet sections read
about 65 and 63 clean as a whole, against Ian's 60.

## Decisions for Ian

Ian answered all six on 2026-10-06 (`../../ians-answers-2026-10-06.md`): the recommendations stand, and decision 5 waits for his alpha run.

| # | Decision | What the files do today | How it is checked | What Ian decides |
|---|---|---|---|---|
| 1 | Fantina is today's five plus a lead | Today's Duskull, Drifblim, Rotom, Sableye and Mismagius keep their sets, apart from Rotom's Pain Split and Mismagius's Power Gem, which Oxide's lists do not hold, and a Froslass leads with Spikes behind a Focus Sash. Duskull carries the split's forced trade, Destiny Bond, with no Sash and no priority beside it, as Ian's rule asked when it was built (he allowed both on 2026-10-06). | `leader_fantina.json`; the scorer's reading later. | Keep (recommended), or drop the trade and give Duskull Shadow Sneak back. |
| 2 | Bosses are set against today's files | On the advice relayed today, Jupiter, Lucas and Dawn and Fantina are each a step harder than today's file in my simulator, not tuned to a win rate on a box without TMs. | Today's file and mine read side by side in my simulator; the scorer's readings on the final box decide. | Nothing now; they are retooled after the scorer reads them. |
| 3 | Moira keeps her hail | Ian's own Moira: Snover's Snow Warning sets hail, a weather ability the dial holds back until Wake's split, and Slowpoke's Blizzard cannot miss in it. Her Quick Claw on Snover is restored (Ian allowed luck items again on 2026-10-06). | `galactic_grunt_team_galactic_eterna_building_3f.json`. | Keep (recommended). |
| 4 | Two special abilities on ordinary trainers | Cyclist Kayla's Magnemite has Magnet Pull (a trapping ability, allowed on an optional trainer from this split; it traps only Steel types). School Kid Chance's Shedinja has Wonder Guard, a puzzle only super-effective hits solve. | Their files. | Keep both (recommended). |
| 5 | Ordinary trainers are on the soft side (Ian: leave them for the alpha run; one pass over every split may follow it) | They average about 90 clean against Ian's 80 to 85, and will read softer still once the box has TMs. | My estimates; Ian's alpha run. | Sharpen them in one pass after the TM pass, against the box it gives (recommended), or leave them for the alpha. |
| 6 | Tag battles | Wayward Cave's five pairs are built a notch softer than their neighbours. | The scorer cannot read them yet. | Nothing now. |

No conditional attack (Dream Eater and the like) appears in this split.

No trainer of this split stands on a map with its own weather (a map's
weather is battle weather for every fight on it; the nearest such maps are
Oreburgh's gym before this split and Route 215 after it), so Moira's hail
from Snow Warning is the split's only weather.

**The legality sweep (2026-10-07).** The files were checked against the final
learnsets and TM list (origin/balance-tm-pass at 377312dbf0), with the moves
cut from the TM list kept in each species' trainer palette as Ian ruled. 23
moves the lists no longer hold were swapped for legal ones doing the same job,
nearly all small level-up moves; the tables below show the swept sets. The
expected numbers date from before the sweep, and the scorer's step 15 reading
gives the real ones. The swaps:

- Galactic Grunt's Skitty: Double Slap to Fury Swipes.
- Galactic Grunt's Skitty: Tail Whip to Baby Doll Eyes.
- Galactic Grunt's Skitty: Assist to Swift.
- Galactic Grunt's Stunky: Poison Gas to Leer.
- Galactic Grunt's Stunky: Feint to Slash.
- Galactic Grunt's Koffing: Smoke Screen to Screech.
- Jupiter 1's Delcatty: Double Slap to Fury Swipes.
- Jupiter 1's Tangela: Bind to Bullet Seed.
- Jupiter 1's Golbat: Wing Attack to Aerial Ace.
- Cyclist John's Doduo: Fury Attack to Swift.
- Cyclist Nicole's Clefairy: Double Slap to Fury Swipes.
- Cyclist Nicole's Jigglypuff: Double Slap to Fury Swipes.
- Cyclist Nicole's Wigglytuff: Double Slap to Fury Swipes.
- Hiker Reginald's Phanpy: Defense Curl to Focus Energy.
- Hiker Lorenzo's Geodude: Defense Curl to Block.
- Camper Parker's Buizel: Water Gun to Chilling Water.
- Youngster Austin's Buizel: Water Gun to Chilling Water.
- Picnicker Lauren's Marill: Defense Curl to Charm.
- Hiker Kevin's Phanpy: Defense Curl to Focus Energy.
- Hiker Kevin's Geodude: Defense Curl to Block.
- Battle Girl Helen's Riolu: Feint to Swift.
- Black Belt Kyle's Machoke: Submission to Brick Break.

## What comes next

The bosses of Maylene's split, whose box is in the folder, then the later
splits' bosses in order, then their ordinary trainers.

## Overview

| Trainer | Place | Path | Battle | Size | Levels | The idea | Expected |
|---|---|---|---|---|---|---|---|
| Galactic Grunt (1F, 1) | Eterna building 1F | gauntlet, first section | single | 3 | 23 to 24 | Hypnosis that follows you | 100 / 0.00 / 99 |
| Galactic Grunt (1F, 2) | Eterna building 1F | gauntlet, first section | single | 3 | 23 to 24 | Poison that follows you | 100 / 0.35 / 76 |
| Galactic Grunt (2F, 1) | Eterna building 2F | gauntlet, first section | single | 3 | 23 to 24 | Pursuit on two members punishes the player who switches to spare a hurt Pokemon for the next fight | 100 / 0.10 / 94 |
| Galactic Grunt (2F, 2) | Eterna building 2F | gauntlet, first section | single | 3 | 23 to 24 | Toxic and Poison Point at the end of the section | 100 / 0.25 / 84 |
| Scientist Travon | Eterna building 3F | gauntlet, second section | single | 3 | 24 to 25 | Kadabra behind a TwistedSpoon and an X Special in the bag | 100 / 0.30 / 84 |
| Galactic Officer Moira | Eterna building 3F | gauntlet, second section | single, named officer | 4 | 25 to 26 | Ian's Moira kept to her idea | about 100 / 0.2 / 83 in my simulator |
| Jupiter 1 | Eterna building 4F | on the path | single, boss | 5 | 26 to 27 | Poison and chip | about 97 / 1.7 / 12 in my simulator |
| Cyclist Axel | Route 206 | optional | single | 3 | 27 to 29 | Electric speed | 100 / 0.10 / 97 |
| Cyclist James | Route 206 | optional | single | 4 | 27 to 29 | Fire Fang on everything | 100 / 0.10 / 94 |
| Cyclist John | Route 206 | optional | single | 4 | 27 to 29 | Four birds | 100 / 0.05 / 98 |
| Cyclist Ryan | Route 206 | optional | single | 3 | 28 to 29 | Endure and a pinch berry | 100 / 0.25 / 88 |
| Cyclist Megan | Route 206 | optional | single | 3 | 28 to 29 | Luxio's Ice Fang for the Flying and Grass answers to an Electric type | 100 / 0.10 / 93 |
| Cyclist Nicole | Route 206 | optional | single | 4 | 26 to 29 | The Jigglypuff line curls and rolls | 100 / 0.25 / 85 |
| Cyclist Kayla | Route 206 | optional | single | 3 | 28 to 29 | Steel and Electric | 100 / 0.10 / 94 |
| Cyclist Rachel | Route 206 | optional | single | 4 | 27 to 29 | Fire and Electric types that roll fast | 100 / 0.10 / 95 |
| Hiker Theodore | Route 206 | optional | single | 3 | 28 to 29 | Rock Slide on all three | 100 / 0.10 / 94 |
| Camper Diego | Wayward Cave | optional | tag, with Picnicker Tori | 2 | 27 to 28 | Technician Ambipom | not readable yet (a tag battle) |
| Picnicker Tori | Wayward Cave | optional | tag, with Camper Diego | 2 | 27 to 28 | Follow Me from Clefairy beside Slowpoke's Yawn | not readable yet (a tag battle) |
| Lass Cassidy | Wayward Cave | optional | tag, with Youngster Wayne | 2 | 27 to 28 | Jump Kick and Fake Out from the Buneary line | not readable yet (a tag battle) |
| Youngster Wayne | Wayward Cave | optional | tag, with Lass Cassidy | 3 | 27 to 28 | Helping Hand from Growlithe behind Fire and Flying attackers | not readable yet (a tag battle) |
| Hiker Reginald | Wayward Cave | optional | tag, with Hiker Lorenzo | 2 | 27 to 28 | Bonsly's Block and Phanpy's Rollout | not readable yet (a tag battle) |
| Hiker Lorenzo | Wayward Cave | optional | tag, with Hiker Reginald | 2 | 27 to 28 | Onix and Geodude | not readable yet (a tag battle) |
| Collector Terry | Wayward Cave | optional | tag, with Ruin Maniac Gerald | 2 | 27 to 28 | Two young Dragons | not readable yet (a tag battle) |
| Ruin Maniac Gerald | Wayward Cave | optional | tag, with Collector Terry | 2 | 27 to 28 | Bronzor's Hypnosis beside Graveler's Rock Slide | not readable yet (a tag battle) |
| Picnicker Ana | Wayward Cave | optional | tag, with Camper Parker | 2 | 27 to 28 | Noctowl's Uproar and Reflect | not readable yet (a tag battle) |
| Camper Parker | Wayward Cave | optional | tag, with Picnicker Ana | 2 | 27 to 28 | Buizel's Aqua Jet and Luxio's Spark | not readable yet (a tag battle) |
| Youngster Austin | Route 207 | optional | single | 3 | 28 to 29 | Luxio's Ice Fang and Gligar's Dig cover each other's counters | 100 / 0.10 / 95 |
| Camper Anthony | Route 207 | optional | single | 4 | 27 to 29 | Four of the region's starter lines | 100 / 0.05 / 96 |
| Picnicker Lauren | Route 207 | optional | single | 3 | 28 to 29 | Huge Power Marill with Aqua Tail behind two Electric types | 100 / 0.00 / 99 |
| Hiker Kevin | Route 207 | optional | single | 5 | 27 to 29 | Five Rock and Ground types with Rollout | 100 / 0.05 / 97 |
| Hiker Justin | Route 207 | on the path | single | 4 | 28 to 29 | Gligar and Dugtrio-line speed | 100 / 0.05 / 96 |
| Battle Girl Helen | Route 207 | optional | single | 4 | 28 to 29 | Fighting types with Fake Out and priority | 100 / 0.50 / 80 |
| Lucas and Dawn 2 | Route 207 | on the path | single, boss | 5 | 28 to 30 | Today's four | about 99 / 0.15 / 90 in my simulator |
| Hiker Robert | Route 208 | optional | single | 3 | 31 to 32 | Sudowoodo's Wood Hammer for the Water types that wall a Rock team | 100 / 0.50 / 75 |
| Hiker Jonathan | Route 208 | on the path | single | 4 | 31 | Poison and Ground | 100 / 0.50 / 78 |
| Black Belt Kyle | Route 208 | optional | single | 3 | 30 to 31 | Three Fighting styles | 100 / 0.35 / 83 |
| Aroma Lady Hannah | Route 208 | optional | single | 4 | 30 to 31 | Sun again | 100 / 0.35 / 88 |
| Artist William | Route 208 | optional | single | 2 | 30 to 32 | Screens from Mime Jr | 100 / 0.10 / 94 |
| Lass Molly | Hearthome Gym | gym trainer | single | 3 | 31 to 32 | Burns and Ghosts | 100 / 0.25 / 86 |
| Youngster Donny | Hearthome Gym | gym trainer | single | 4 | 30 to 32 | Hypnosis and Curse from the Gastly line | 100 / 0.70 / 79 |
| School Kid Chance | Hearthome Gym | gym trainer | single | 3 | 30 to 32 | Wonder Guard | 100 / 0.05 / 96 |
| School Kid Mackenzie | Hearthome Gym | gym trainer | single | 3 | 31 to 32 | Burn | 100 / 0.05 / 97 |
| Ace Trainer Allen | Hearthome Gym | Ace Trainer | single | 4 | 29 to 30 | Ghosts with few weaknesses | 100 / 0.80 / 77 read blind |
| Ace Trainer Catherine | Hearthome Gym | Ace Trainer | single | 4 | 30 to 32 | Burn | 100 / 0.65 / 74 read blind |
| Fantina | Hearthome Gym | on the path | single, boss | 6 | 31 to 33 | Today's five with one more | about 55 / 4.6 / 0 in my simulator |

Expected numbers are won / faints a fight / clean, at real odds: for ordinary
trainers in the scorer's terms, for bosses in my simulator's own terms beside
today's file.

## Trainer by trainer

### Galactic Grunt (1F, 1): Eterna building 1F, gauntlet, first section, single, cap 27

Hypnosis that follows you: Glameow's sleep carries into the next fight of the section unless a bag item cures it, and Fake Out takes the first turn.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Skitty | 23 | none | Cute Charm | default | Fury Swipes, Baby-Doll Eyes, Swift, Fake Tears |
| Stunky | 24 | none | Aftermath | default | Fury Swipes, Leer, Screech, Slash |
| Glameow | 24 | Oran Berry | Limber | Jolly | Fake Out, Fury Swipes, Hypnosis, Faint Attack |

Today's team: Glameow 24 (Growl, Hypnosis, Faint Attack, Fury Swipes), Skitty 24 (Sing, DoubleSlap, Copycat, Assist). Expected: 100 / 0.00 / 99.

### Galactic Grunt (1F, 2): Eterna building 1F, gauntlet, first section, single, cap 27

Poison that follows you: Toxic, Poison Gas and Pursuit, so the section's later fights start with the player already worn.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Koffing | 24 | none | Levitate | default | Smog, Assurance, Toxic, Screech |
| Zubat | 23 | none | Inner Focus | default | Leech Life, Bite, Supersonic, Astonish |
| Stunky | 24 | Oran Berry | Aftermath | Adamant | Leer, Fury Swipes, Pursuit, Slash |

Today's team: Stunky 24 (Poison Gas, SmokeScreen, Feint, Slash), Koffing 24 (SmokeScreen, Assurance, Selfdestruct, Sludge). Expected: 100 / 0.35 / 76.

### Galactic Grunt (2F, 1): Eterna building 2F, gauntlet, first section, single, cap 27

Pursuit on two members punishes the player who switches to spare a hurt Pokemon for the next fight.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Murkrow | 24 | none | Insomnia | default | Wing Attack, Pursuit, Faint Attack, Astonish |
| Bronzor | 23 | none | Levitate | default | Confusion, Imprison, Confuse Ray, Rock Tomb |
| Croagunk | 24 | Oran Berry | Dry Skin | Adamant | Poison Jab, Faint Attack, Pursuit, Mud-Slap |

Today's team: Croagunk 24 (Pursuit, Faint Attack, Wake-Up Slap, Swagger). Expected: 100 / 0.10 / 94.

### Galactic Grunt (2F, 2): Eterna building 2F, gauntlet, first section, single, cap 27

Toxic and Poison Point at the end of the section, where every point of chip has been spent already.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Grimer | 24 | none | Stench | default | Toxic, Sludge, Harden, Mud-Slap |
| Glameow | 23 | none | Limber | default | Fury Swipes, Faint Attack, Growl, Scratch |
| Nidorina | 24 | Oran Berry | Poison Point | Adamant | Double Kick, Poison Sting, Bite, Fury Swipes |

Today's team: Nidorina 24 (Double Kick, Poison Sting, Super Fang, Bite). Expected: 100 / 0.25 / 84.

### Scientist Travon: Eterna building 3F, gauntlet, second section, single, cap 27

Kadabra behind a TwistedSpoon and an X Special in the bag, with Porygon's Recover and Voltorb's Screech to soften the way.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Voltorb | 24 | none | Soundproof | default | Spark, SonicBoom, Screech, Rollout |
| Porygon | 24 | none | Trace | default | Psybeam, Signal Beam, Conversion, Recover |
| Kadabra | 25 | TwistedSpoon | Inner Focus | Timid | Psybeam, Signal Beam, Disable, Reflect |

Today's team: Kadabra 24 (Psybeam, Disable, Signal Beam). Expected: 100 / 0.30 / 84.

### Galactic Officer Moira: Eterna building 3F, gauntlet, second section, single, named officer, cap 27

Ian's Moira kept to her idea: hail from Snover's Snow Warning, Blizzard that cannot miss in it, a Quick Claw on Snover (restored by Ian's ruling of 2026-10-06), Swinub's Salac Berry and Endure, Kirlia's Calm Mind. Built to the boss standard, since goal 3 reads her as a named Galactic fight, but she closes a gauntlet, so she sits on the soft side. Fire and Steel types and the Rock types shrug off the hail.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Snover | 25 | Quick Claw | Snow Warning | Adamant | Razor Leaf, Icy Wind, Avalanche, GrassWhistle |
| Swinub | 25 | Salac Berry | Thick Fat | Adamant | Endure, Mud Bomb, Icy Wind, Take Down |
| Slowpoke | 25 | Sitrus Berry | Own Tempo | Modest | Blizzard, Water Pulse, Confusion, Disable |
| Kirlia | 26 | Lum Berry | Trace | Modest | Psychic, Icy Wind, Calm Mind, Magical Leaf |

Today's team: Snover 24 (Quick Claw; Swagger, GrassWhistle, Swords Dance, Avalanche), Slowpoke 25 (Rest, Future Sight, Blizzard, Sleep Talk), Swinub 26 (Salac Berry; Ice Shard, Superpower, Dig, Endure), Kirlia 25 (Future Sight, Calm Mind, Icy Wind, Psychic). Expected: about 100 / 0.2 / 83 in my simulator; read by the scorer later.

### Jupiter 1: Eterna building 4F, on the path, single, boss, cap 27

Poison and chip, with Fake Out: today's four (Delcatty, Sableye, Tangela, Skuntank) on legal sets, plus a Golbat. Toxic from Golbat and Skuntank, Tangela's Sleep Powder and Leech Seed, Delcatty's and Sableye's Fake Outs, and Skuntank's Poison Jab at the interim cap. The Rock and Ground types and Rotom answer most of it.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Delcatty | 26 | Oran Berry | Cute Charm | default | Fake Out, Sucker Punch, Fury Swipes, Charm |
| Sableye | 26 | Leftovers | Clear Body | default | Shadow Sneak, Astonish, Payback, Knock Off |
| Tangela | 26 | Pecha Berry | Chlorophyll | default | Leech Seed, Mega Drain, Bullet Seed, Sleep Powder |
| Golbat | 26 | Oran Berry | Inner Focus | default | Toxic, Aerial Ace, Bite, Supersonic |
| Skuntank | 27 | Sitrus Berry | Aftermath | default | Slash, Poison Jab, Toxic, Screech |

Today's team: Delcatty 26 (Fake Out, Sing, Attract, Headbutt), Sableye 26 (Shadow Sneak, Fake Out, Astonish, Poison Jab), Tangela 26 (Pecha Berry; Leech Seed, Mega Drain, Bind, Sleep Powder), Skuntank 27 (Sitrus Berry; Night Slash, Toxic, Screech, SmokeScreen). Expected: about 97 / 1.7 / 12 in my simulator, where today's file reads 100 / 0.3 / 72; read by the scorer later.

### Cyclist Axel: Route 206, optional, single, cap 30

Electric speed: a Magnet Thunderbolt from Manectric, Plusle's Thunder Wave.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Plusle | 27 | none | Plus | default | Spark, Quick Attack, Thunder Wave, Helping Hand |
| Pikachu | 28 | none | Reckless | default | Thunderbolt, Quick Attack, Brick Break, Charm |
| Manectric | 29 | Magnet | Lightning Rod | Timid | Thunderbolt, Bite, Quick Attack, Howl |

Today's team: Pikachu 21 (Thunder Wave, Quick Attack, ThunderShock, Slam). Expected: 100 / 0.10 / 97.

### Cyclist James: Route 206, optional, single, cap 30

Fire Fang on everything, and a Charcoal Flamethrower Vulpix with Will-O-Wisp for the physical answers.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Ponyta | 27 | none | Run Away | default | Flame Wheel, Stomp, Fire Spin, Double Kick |
| Houndour | 28 | none | Early Bird | default | Fire Fang, Bite, Smog, Roar |
| Growlithe | 28 | none | Intimidate | default | Fire Fang, Bite, Crunch, Roar |
| Vulpix | 29 | Charcoal | Flash Fire | Timid | Flamethrower, Quick Attack, Confuse Ray, Will-O-Wisp |

Today's team: Vulpix 21 (Quick Attack, Will-O-Wisp, Confuse Ray, Ember). Expected: 100 / 0.10 / 94.

### Cyclist John: Route 206, optional, single, cap 30

Four birds, Pursuit for the switch, a Sharp Beak Staravia at the end.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Pidgeotto | 28 | none | Keen Eye | default | Air Slash, Quick Attack, Steel Wing, Gust |
| Swellow | 28 | none | Guts | default | Aerial Ace, Quick Attack, Endeavor, Growl |
| Doduo | 27 | none | Run Away | default | Swift, Pursuit, Uproar, Quick Attack |
| Staravia | 29 | Sharp Beak | Reckless | Jolly | Aerial Ace, Quick Attack, Steel Wing, Take Down |

Today's team: Pidgey 19 (Sand-Attack, Aerial Ace, Quick Attack, Whirlwind), Pidgeotto 21 (Sand-Attack, Aerial Ace, Quick Attack, Whirlwind). Expected: 100 / 0.05 / 98.

### Cyclist Ryan: Route 206, optional, single, cap 30

Endure and a pinch berry, then Reversal: Kaizo's Cyclist Ryan at 6/10, on two members. The answer is a multi-hit move or a status that breaks the chain.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Riolu | 28 | Liechi Berry | Adaptability | Adamant | Reversal, Endure, Force Palm, Quick Attack |
| Monferno | 28 | none | Blaze | default | Flame Wheel, Mach Punch, Taunt, Fury Swipes |
| Primeape | 29 | Salac Berry | No Guard | Jolly | Reversal, Endure, Karate Chop, Rock Slide |

Today's team: Shinx 21 (default moves). Expected: 100 / 0.25 / 88.

### Cyclist Megan: Route 206, optional, single, cap 30

Luxio's Ice Fang for the Flying and Grass answers to an Electric type.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Staravia | 28 | none | Reckless | default | Aerial Ace, Quick Attack, Endeavor, Steel Wing |
| Furret | 28 | none | Adaptability | default | Slash, Quick Attack, Follow Me, Helping Hand |
| Luxio | 29 | Oran Berry | Hyper Cutter | Jolly | Spark, Bite, Ice Fang, Quick Attack |

Today's team: Staravia 21 (Quick Attack, Wing Attack, Double Team, Endeavor). Expected: 100 / 0.10 / 93.

### Cyclist Nicole: Route 206, optional, single, cap 30

The Jigglypuff line curls and rolls, with one Sing and Igglybuff's Sweet Kiss.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Igglybuff | 26 | none | Cute Charm | default | Charm, Pound, Sweet Kiss, Covet |
| Clefairy | 27 | none | Magic Guard | default | Fury Swipes, Wake-Up Slap, Magical Leaf, Encore |
| Jigglypuff | 28 | none | Cute Charm | default | Rollout, Defense Curl, Sing, Fury Swipes |
| Wigglytuff | 29 | Sitrus Berry | Cute Charm | Bold | Rollout, Defense Curl, Body Slam, Fury Swipes |

Today's team: Igglybuff 17 (default moves), Jigglypuff 18 (default moves), Wigglytuff 19 (default moves). Expected: 100 / 0.25 / 85.

### Cyclist Kayla: Route 206, optional, single, cap 30

Steel and Electric: Magnemite's Magnet Thunderbolt and Flash Cannon, Bronzor's Hypnosis.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Voltorb | 28 | none | Soundproof | default | Spark, SonicBoom, Screech, Rollout |
| Bronzor | 28 | none | Levitate | default | Confusion, Hypnosis, Rock Tomb, Imprison |
| Magnemite | 29 | Magnet | Magnet Pull | Modest | Thunderbolt, Flash Cannon, SonicBoom, Thunder Wave |

Today's team: Magnemite 21 (ThunderShock, Supersonic, SonicBoom, Thunder Wave). Expected: 100 / 0.10 / 94.

### Cyclist Rachel: Route 206, optional, single, cap 30

Fire and Electric types that roll fast: Rapidash's Poison Jab and Charcoal Flame Wheel.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Voltorb | 27 | none | Soundproof | default | Spark, Rollout, Screech, SonicBoom |
| Ponyta | 28 | none | Run Away | default | Flame Wheel, Stomp, Fire Spin, Double Kick |
| Pachirisu | 28 | none | Adaptability | default | Spark, Bite, Quick Attack, Covet |
| Rapidash | 29 | Charcoal | Reckless | Adamant | Flame Wheel, Stomp, Poison Jab, Quick Attack |

Today's team: Ponyta 20 (Tail Whip, Ember, Flame Wheel, Stomp), Voltorb 21 (SonicBoom, Shock Wave, Thunder Wave, Screech). Expected: 100 / 0.10 / 95.

### Hiker Theodore: Route 206, optional, single, cap 30

Rock Slide on all three; Larvitar's Dark Pulse and Onix's Iron Head as cover. Oxide's Larvitar and Onix learn no Sandstorm, so his sand is gone.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Larvitar | 28 | none | Guts | default | Rock Slide, Bite, Dark Pulse, Screech |
| Onix | 28 | none | Rock Head | default | Rock Slide, Iron Head, Slam, Rock Tomb |
| Graveler | 29 | Hard Stone | Sturdy | Adamant | Rock Slide, Magnitude, Rollout, Defense Curl |

Today's team: Larvitar 20 (Bite, Sandstorm, Screech, Rock Slide), Onix 21 (Screech, Rock Throw, Rage, Rock Tomb). Expected: 100 / 0.10 / 94.

### Camper Diego: Wayward Cave, optional, tag, with Picnicker Tori, cap 30

Technician Ambipom: Fake Out, Covet and Swift at one and a half times.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Aipom | 27 | none | Technician | default | Fury Swipes, Swift, Covet, Screech |
| Ambipom | 28 | Silk Scarf | Technician | Jolly | Fake Out, Covet, Swift, U-turn |

Today's team: Aipom 25 (Tickle, Fury Swipes, Swift, Screech). Expected: not readable yet (a tag battle).

### Picnicker Tori: Wayward Cave, optional, tag, with Camper Diego, cap 30

Follow Me from Clefairy beside Slowpoke's Yawn.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Slowpoke | 27 | none | Oblivious | default | Confusion, Water Pulse, Yawn, Headbutt |
| Clefairy | 28 | Oran Berry | Magic Guard | default | Follow Me, Helping Hand, Encore, Magical Leaf |

Today's team: Slowpoke 24 (Growl, Water Gun, Confusion, Disable). Expected: not readable yet (a tag battle).

### Lass Cassidy: Wayward Cave, optional, tag, with Youngster Wayne, cap 30

Jump Kick and Fake Out from the Buneary line.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Buneary | 27 | none | Scrappy | default | Jump Kick, Quick Attack, Endure, Return |
| Lopunny | 28 | Oran Berry | Scrappy | Jolly | Jump Kick, Fake Out, Quick Attack, Bounce |

Today's team: Buneary 24 (Endure, Return, Quick Attack, Jump Kick). Expected: not readable yet (a tag battle).

### Youngster Wayne: Wayward Cave, optional, tag, with Lass Cassidy, cap 30

Helping Hand from Growlithe behind Fire and Flying attackers.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Staravia | 27 | none | Reckless | default | Wing Attack, Quick Attack, Endeavor, Whirlwind |
| Growlithe | 27 | none | Intimidate | default | Flame Wheel, Helping Hand, Leer, Bite |
| Ponyta | 28 | Oran Berry | Run Away | default | Flame Wheel, Stomp, Fire Spin, Take Down |

Today's team: Staravia 24 (Wing Attack, Double Team, Endeavor, Whirlwind), Growlithe 24 (Leer, Odor Sleuth, Helping Hand, Flame Wheel), Ponyta 24 (Ember, Flame Wheel, Stomp, Fire Spin). Expected: not readable yet (a tag battle).

### Hiker Reginald: Wayward Cave, optional, tag, with Hiker Lorenzo, cap 30

Bonsly's Block and Phanpy's Rollout.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Bonsly | 27 | none | Rock Head | default | Rock Throw, Block, Faint Attack, Rollout |
| Phanpy | 28 | Oran Berry | Pickup | default | Rollout, Take Down, Ice Shard, Focus Energy |

Today's team: Bonsly 25 (Rock Throw, Mimic, Block, Faint Attack), Phanpy 25 (Take Down, Rollout, Natural Gift, Slam). Expected: not readable yet (a tag battle).

### Hiker Lorenzo: Wayward Cave, optional, tag, with Hiker Reginald, cap 30

Onix and Geodude: Rock Slide spread beside Magnitude.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Onix | 28 | Oran Berry | Sturdy | default | Rock Slide, Rock Tomb, Slam, Iron Head |
| Geodude | 27 | none | Rock Head | default | Rock Throw, Magnitude, Rollout, Block |

Today's team: Onix 26 (Rage, Rock Tomb, Sandstorm, Slam). Expected: not readable yet (a tag battle).

### Collector Terry: Wayward Cave, optional, tag, with Ruin Maniac Gerald, cap 30

Two young Dragons: Gible's Dragon Claw and Sand Tomb, Bagon's Dragon Rage.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Bagon | 27 | none | Rock Head | default | Headbutt, Ember, Dragon Rage, Focus Energy |
| Gible | 28 | Oran Berry | Rough Skin | default | Dragon Claw, Sand Tomb, Take Down, Slash |

Today's team: Bagon 25 (Leer, Headbutt, Focus Energy, Ember). Expected: not readable yet (a tag battle).

### Ruin Maniac Gerald: Wayward Cave, optional, tag, with Collector Terry, cap 30

Bronzor's Hypnosis beside Graveler's Rock Slide.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Bronzor | 27 | none | Levitate | default | Extrasensory, Confuse Ray, Imprison, Hypnosis |
| Graveler | 28 | Oran Berry | Sturdy | default | Rock Slide, Magnitude, Rollout, Defense Curl |

Today's team: Bronzor 25 (Hypnosis, Imprison, Confuse Ray, Extrasensory), Graveler 25 (Rock Throw, Magnitude, Selfdestruct, Rollout). Expected: not readable yet (a tag battle).

### Picnicker Ana: Wayward Cave, optional, tag, with Camper Parker, cap 30

Noctowl's Uproar and Reflect.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Hoothoot | 27 | none | Insomnia | default | Peck, Confusion, Uproar, Reflect |
| Noctowl | 28 | Oran Berry | Insomnia | default | Uproar, Confusion, Air Cutter, Reflect |

Today's team: Noctowl 24 (Peck, Uproar, Reflect, Confusion). Expected: not readable yet (a tag battle).

### Camper Parker: Wayward Cave, optional, tag, with Picnicker Ana, cap 30

Buizel's Aqua Jet and Luxio's Spark.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Buizel | 27 | none | Swift Swim | default | Chilling Water, Swift, Quick Attack, Aqua Jet |
| Luxio | 28 | Oran Berry | Hyper Cutter | default | Spark, Bite, Roar, Charge |

Today's team: Buizel 24 (Water Gun, Swift, Quick Attack), Luxio 24 (Spark, Bite). Expected: not readable yet (a tag battle).

### Youngster Austin: Route 207, optional, single, cap 30

Luxio's Ice Fang and Gligar's Dig cover each other's counters; Buizel's Pursuit for the switch.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Buizel | 28 | none | Swift Swim | default | Aqua Jet, Chilling Water, Pursuit, Swift |
| Gligar | 28 | none | Hyper Cutter | default | Knock Off, Quick Attack, Dig, Faint Attack |
| Luxio | 29 | Oran Berry | Hyper Cutter | Adamant | Spark, Bite, Ice Fang, Roar |

Today's team: Buizel 24 (Water Gun, Pursuit, Swift, Aqua Jet), Luxio 24 (Charge, Spark, Bite, Roar), Gligar 24 (Knock Off, Quick Attack, Dig, Faint Attack). Expected: 100 / 0.10 / 95.

### Camper Anthony: Route 207, optional, single, cap 30

Four of the region's starter lines, each with one coverage move; Monferno's Charcoal Flame Wheel is the danger.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Nuzleaf | 27 | none | Chlorophyll | default | Fake Out, Razor Leaf, Payback, Rock Tomb |
| Grotle | 28 | none | Shell Armor | default | Razor Leaf, Bite, Giga Drain, Withdraw |
| Prinplup | 28 | none | Swift Swim | default | BubbleBeam, Metal Claw, Peck, Supersonic |
| Monferno | 29 | Charcoal | Blaze | Naive | Flame Wheel, Mach Punch, Taunt, Fury Swipes |

Today's team: Monferno 24 (Taunt, Mach Punch, Fury Swipes, Flame Wheel). Expected: 100 / 0.05 / 96.

### Picnicker Lauren: Route 207, optional, single, cap 30

Huge Power Marill with Aqua Tail behind two Electric types.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Pachirisu | 28 | none | Adaptability | default | Spark, Covet, Charm, Endure |
| Emolga | 28 | none | Static | default | Acrobatics, Spark, Quick Attack, Charge |
| Marill | 29 | Oran Berry | Huge Power | Adamant | Aqua Tail, Rollout, Charm, Helping Hand |

Today's team: Pachirisu 24 (Charm, ThunderPunch, Endure, Headbutt). Expected: 100 / 0.00 / 99.

### Hiker Kevin: Route 207, optional, single, cap 30

Five Rock and Ground types with Rollout, Rock Slide and Magnitude. Water and Grass types beat it.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Cubone | 27 | none | Rock Head | default | Bonemerang, Headbutt, Rock Slide, Focus Energy |
| Phanpy | 27 | none | Pickup | default | Rollout, Take Down, Ice Shard, Focus Energy |
| Geodude | 28 | none | Rock Head | default | Rock Throw, Magnitude, Rollout, Block |
| Onix | 28 | none | Rock Head | default | Rock Slide, Rock Tomb, Iron Head, Slam |
| Graveler | 29 | Hard Stone | Sturdy | Adamant | Rock Slide, Magnitude, Rollout, Defense Curl |

Today's team: Phanpy 24 (Take Down, Rollout, Natural Gift, Slam), Cubone 24 (Leer, Focus Energy, Bonemerang, Rage), Onix 24 (Rock Throw, Rage, Rock Tomb, Sandstorm), Geodude 24 (Rock Throw, Magnitude, Selfdestruct, Rollout). Expected: 100 / 0.05 / 97.

### Hiker Justin: Route 207, on the path, single, cap 30

Gligar and Dugtrio-line speed, Nosepass's Block and Thunder Wave.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Diglett | 28 | none | Sand Veil | default | Magnitude, Mud-Slap, Sucker Punch, Dig |
| Nosepass | 28 | none | Solid Rock | default | Rock Slide, Block, Thunder Wave, Shock Wave |
| Sandshrew | 28 | none | Rough Skin | default | Rock Slide, Poison Sting, Rapid Spin, Night Slash |
| Gligar | 29 | Oran Berry | Hyper Cutter | Jolly | Dig, Aerial Ace, Rock Slide, Knock Off |

Today's team: Diglett 25 (Magnitude, Mud-Slap, Dig, Sucker Punch), Nosepass 25 (Harden, Rock Throw, Block, Thunder Wave). Expected: 100 / 0.05 / 96.

### Battle Girl Helen: Route 207, optional, single, cap 30

Fighting types with Fake Out and priority; Machoke's Revenge and Meditite's Psycho Cut.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Riolu | 28 | none | Adaptability | default | Force Palm, Quick Attack, Counter, Swift |
| Makuhita | 28 | none | Thick Fat | default | Fake Out, Knock Off, SmellingSalt, Vital Throw |
| Meditite | 29 | none | Pure Power | default | Psycho Cut, Drain Punch, Bullet Punch, Force Palm |
| Machoke | 29 | Oran Berry | Guts | Adamant | Vital Throw, Revenge, Rock Slide, Brick Break |

Today's team: Makuhita 26 (Whirlwind, Knock Off, SmellingSalt, Belly Drum), Riolu 26 (Force Palm, Feint, Reversal, Screech). Expected: 100 / 0.50 / 80.

### Lucas and Dawn 2: Route 207, on the path, single, boss, cap 30

Today's four, each with a fuller set, plus Pachirisu: Lopunny's Jump Kick and Fake Out, and for a player who took Piplup, the counterpart's Jolteon, a Lovely Kiss Jynx and Monferno. It sits just above today's fight, a drop before Fantina.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Lopunny | 29 | Lum Berry | Scrappy | Jolly | Jump Kick, Quick Attack, Bounce, Fake Out |
| Pachirisu | 28 | Oran Berry | Adaptability | default | Spark, Swift, Charm, Bite |
| Jolteon | 29 | Magnet | Volt Absorb | Timid | Thunderbolt, Double Kick, Shadow Ball, Thunder Wave |
| Jynx | 29 | Oran Berry | Snow Cloak | default | Ice Punch, Confusion, Lovely Kiss, Fake Tears |
| Monferno | 30 | Charcoal | Blaze | Naive | Flame Wheel, Mach Punch, Rock Slide, Taunt |

Today's team: Lopunny 29 (Lum Berry; Jump Kick, Thunder Wave, Quick Attack, Mirror Coat), Jolteon 29 (Oran Berry; Thunder Wave, Magnet Rise, Shock Wave, Fake Tears), Jynx 30 (Icicle Plate; Icy Wind, Reflect, Lovely Kiss, Copycat), Monferno 30 (Muscle Band; Mach Punch, Flame Wheel, Fake Out, Torment). Expected: about 99 / 0.15 / 90 in my simulator, where today's file reads 100 / 0.02 / 98; read by the scorer later.

The other files share Lopunny and Pachirisu and swap the counterpart's three: Vaporeon, Electabuzz and Grotle (`dummy_793`, `dummy_800`), and Glaceon, Magmar and Prinplup (`dummy_799`, `dummy_802`); Dawn's files and Lucas's carry the same teams. In my simulator they read 100 / 0.01 / 99 and 99 / 1.1 / 10, the Glaceon file the sharpest.

### Hiker Robert: Route 208, optional, single, cap 33

Sudowoodo's Wood Hammer for the Water types that wall a Rock team.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Graveler | 31 | none | Rock Head | default | Rock Slide, Magnitude, Rollout, Defense Curl |
| Steelix | 32 | none | Rock Head | default | Iron Head, Rock Slide, Ice Fang, Screech |
| Sudowoodo | 32 | Oran Berry | Sturdy | Adamant | Wood Hammer, Rock Slide, Low Kick, Sucker Punch |

Today's team: Graveler 28 (Magnitude, Selfdestruct, Rollout, Rock Blast). Expected: 100 / 0.50 / 75.

### Hiker Jonathan: Route 208, on the path, single, cap 33

Poison and Ground: Poison Jab on three, Dugtrio's Dig and Sucker Punch.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Nidorina | 31 | none | Poison Point | default | Poison Jab, Double Kick, Bite, Toxic |
| Gligar | 31 | none | Hyper Cutter | default | Poison Jab, Aerial Ace, Dig, Knock Off |
| Nidorino | 31 | none | Poison Point | default | Poison Jab, Double Kick, Horn Attack, Sucker Punch |
| Dugtrio | 31 | none | Sand Veil | default | Dig, Sucker Punch, Rock Slide, Night Slash |

Today's team: Nidorino 27 (Double Kick, Poison Sting, Dig, Headbutt). Expected: 100 / 0.50 / 78.

### Black Belt Kyle: Route 208, optional, single, cap 33

Three Fighting styles: Hitmontop's Technician Triple Kick and Fake Out, Hitmonchan's priority punches, Machoke's Submission.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Hitmontop | 30 | none | Technician | default | Triple Kick, Fake Out, Rapid Spin, Rolling Kick |
| Hitmonchan | 30 | none | Keen Eye | default | Bullet Punch, Mach Punch, Rock Slide, Revenge |
| Machoke | 31 | none | Guts | default | Brick Break, Revenge, Rock Slide, Poison Jab |

Today's team: Machoke 29 (Foresight, Seismic Toss, Revenge, Vital Throw). Expected: 100 / 0.35 / 83.

### Aroma Lady Hannah: Route 208, optional, single, cap 33

Sun again, with Cherrim's Flower Gift and Jumpluff's sleep.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Sunflora | 30 | none | Solar Power | default | Sunny Day, Mega Drain, Ingrain, Leech Seed |
| Roselia | 30 | none | Natural Cure | default | Giga Drain, Poison Sting, Sleep Powder, Synthesis |
| Cherrim | 30 | none | Flower Gift | default | Magical Leaf, Helping Hand, Leech Seed, Tackle |
| Jumpluff | 31 | none | Chlorophyll | default | U-turn, Seed Bomb, Leech Seed, Stun Spore |

Today's team: Roselia 27 (Leech Seed, Magical Leaf, GrassWhistle, Giga Drain), Jumpluff 27 (Stun Spore, Sleep Powder, Bullet Seed, Leech Seed). Expected: 100 / 0.35 / 88.

### Artist William: Route 208, optional, single, cap 33

Screens from Mime Jr., then Kecleon's Color Change. Oxide's Smeargle knows only Sketch, so it is left out.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Mime Jr | 30 | none | Filter | default | Psybeam, Reflect, Light Screen, Encore |
| Kecleon | 32 | Oran Berry | Color Change | Adamant | Slash, Shadow Claw, Thief, AncientPower |

Today's team: Mime Jr 26 (Mimic, Light Screen, Reflect, Psybeam), Smeargle 26 (Flame Wheel, Aqua Jet, Bullet Seed). Expected: 100 / 0.10 / 94.

### Lass Molly: Hearthome Gym, gym trainer, single, cap 33

Burns and Ghosts, Fantina's tools together: Will-O-Wisp from two, Pursuit, a Spell Tag Shuppet.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Duskull | 31 | none | Levitate | default | Will-O-Wisp, Night Shade, Pursuit, Confuse Ray |
| Misdreavus | 31 | none | Levitate | default | Psybeam, Shadow Ball, Pain Split, Confuse Ray |
| Shuppet | 32 | Spell Tag | Insomnia | Adamant | Shadow Ball, Knock Off, Sucker Punch, Will-O-Wisp |

Today's team: Misdreavus 29 (Confuse Ray, Mean Look, Psybeam, Pain Split). Expected: 100 / 0.25 / 86.

### Youngster Donny: Hearthome Gym, gym trainer, single, cap 33

Hypnosis and Curse from the Gastly line, Will-O-Wisp from Duskull.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Gastly | 30 | none | Levitate | default | Night Shade, Lick, Curse, Sucker Punch |
| Drifloon | 31 | none | Unburden | default | Ominous Wind, Payback, Stockpile, Swallow |
| Duskull | 31 | none | Levitate | default | Shadow Sneak, Will-O-Wisp, Pursuit, Night Shade |
| Haunter | 32 | Oran Berry | Levitate | default | Shadow Ball, Sludge Bomb, Hypnosis, Sucker Punch |

Today's team: Gastly 27 (Night Shade, Confuse Ray, Sucker Punch, Hypnosis), Drifloon 27 (Payback, Stockpile, Swallow, Spit Up). Expected: 100 / 0.70 / 79.

### School Kid Chance: Hearthome Gym, gym trainer, single, cap 33

Wonder Guard: only a super-effective hit touches Shedinja, and Ninjask's Speed Boost runs ahead of it. Fire, Flying, Rock, Ghost and Dark moves answer.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Nincada | 30 | none | Compound Eyes | default | Fury Swipes, Leech Life, Mud-Slap, Harden |
| Ninjask | 31 | none | Speed Boost | default | X-Scissor, Aerial Ace, Leech Life, Swords Dance |
| Shedinja | 32 | Oran Berry | Wonder Guard | Adamant | Shadow Claw, X-Scissor, Sucker Punch, Aerial Ace |

Today's team: Shedinja 29 (Faint Attack, Night Slash, Bug Bite, Spite). Expected: 100 / 0.05 / 96.

### School Kid Mackenzie: Hearthome Gym, gym trainer, single, cap 33

Burn, then Hex: Litwick's Hex doubles on a burned target.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Shuppet | 31 | none | Clear Body | default | Shadow Ball, Knock Off, Will-O-Wisp, Screech |
| Litwick | 31 | none | Flash Fire | default | Hex, Smog, Will-O-Wisp, Confuse Ray |
| Drifloon | 32 | Sitrus Berry | Unburden | Modest | Ominous Wind, Thunderbolt, Will-O-Wisp, Payback |

Today's team: Shuppet 26 (Curse, Spite, Shadow Sneak, Will-O-Wisp), Duskull 26 (Astonish, Confuse Ray, Shadow Sneak, Pursuit). Expected: 100 / 0.05 / 97.

### Ace Trainer Allen: Hearthome Gym, Ace Trainer, single, cap 33

Ghosts with few weaknesses: Sableye has none in this box and opens with Fake Out, Duskull burns, Banette's Sucker Punch punishes the slow attacker.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Sableye | 30 | Leftovers | Clear Body | Impish | Knock Off, Shadow Claw, Will-O-Wisp, Fake Out |
| Misdreavus | 29 | none | Levitate | default | Psybeam, Ominous Wind, Pain Split, Astonish |
| Duskull | 30 | none | Levitate | default | Will-O-Wisp, Pursuit, Night Shade, Confuse Ray |
| Banette | 30 | none | Insomnia | default | Shadow Claw, Knock Off, Sucker Punch, Screech |

Today's team: Rotom 29 (Shadow Ball, Shock Wave, Thunder Wave, Confuse Ray), Sableye 29 (Night Shade, Sucker Punch, Hypnosis, Confuse Ray), Haunter 29 (Shadow Ball, Confuse Ray, Curse, Mean Look). Expected: 100 / 0.80 / 77 read blind; about 100 / 0.1 / 92 with a planned six in my simulator, the way goal 3 reads Ace Trainers.

### Ace Trainer Catherine: Hearthome Gym, Ace Trainer, single, cap 33

Burn, then Hex: my worked example raised a level, with Drifblim's Unburden behind a Sitrus Berry and Haunter's Sucker Punch.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Litwick | 31 | Spell Tag | Flame Body | Modest | Will-O-Wisp, Hex, Flame Burst, Confuse Ray |
| Misdreavus | 30 | none | Levitate | default | Psybeam, Ominous Wind, Pain Split, Spite |
| Drifblim | 31 | Sitrus Berry | Unburden | default | Ominous Wind, Payback, Body Slam, Stockpile |
| Haunter | 32 | Black Sludge | Levitate | Timid | Shadow Ball, Will-O-Wisp, Sucker Punch, Payback |

Today's team: Spiritomb 29 (Faint Attack, Hypnosis, Dream Eater, Ominous Wind), Misdreavus 29 (Confuse Ray, Mean Look, Psybeam, Pain Split). Expected: 100 / 0.65 / 74 read blind; about 100 / 0.2 / 82 with a planned six in my simulator.

### Fantina: Hearthome Gym, on the path, single, boss, cap 33

Today's five with one more, as the dial asks of her: a Froslass leads with Spikes behind a Focus Sash, the split's first Sash lead. Drifblim keeps Unburden and Will-O-Wisp, Rotom its Life Orb, Sableye Focus Punch and Recover, and the Mismagius ace its Expert Belt; Duskull carries the split's one forced trade, Destiny Bond, with no Sash or priority beside it. Normal and Dark types are the answers, and Rampardos and Stunky the planned box's best.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Froslass | 31 | Focus Sash | Cursed Body | default | Spikes, Icy Wind, Ominous Wind, Confuse Ray |
| Drifblim | 32 | Sitrus Berry | Unburden | default | Shadow Ball, Air Cutter, Calm Mind, Will-O-Wisp |
| Rotom | 32 | Life Orb | Levitate | default | Ominous Wind, Shock Wave, Signal Beam, Trick |
| Duskull | 32 | Leftovers | Levitate | default | Will-O-Wisp, Pursuit, Confuse Ray, Destiny Bond |
| Sableye | 32 | Leftovers | Clear Body | default | Shadow Sneak, Payback, Recover, Focus Punch |
| Mismagius | 33 | Expert Belt | Levitate | default | Shadow Ball, Psybeam, Magical Leaf, Payback |

Today's team: Duskull 32 (Focus Sash; Will-O-Wisp, Pursuit, Shadow Sneak, Confuse Ray), Drifblim 32 (Sitrus Berry; Shadow Ball, Air Cutter, Calm Mind, Will-O-Wisp), Rotom 32 (Life Orb; Ominous Wind, Shock Wave, Signal Beam, Pain Split), Sableye 32 (Leftovers; Shadow Sneak, Payback, Recover, Focus Punch), Mismagius 33 (Expert Belt; Shadow Ball, Psybeam, Magical Leaf, Power Gem). Expected: about 55 / 4.6 / 0 in my simulator, where today's file reads 60 / 4.7 / 0 (the scorer read today's at 92 won); read by the scorer later.


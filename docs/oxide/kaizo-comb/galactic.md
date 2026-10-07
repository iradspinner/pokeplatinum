# The comb: the Galactic split

**Refreshed 2026-10-07.** The expected numbers were read again after two
changes: a fix to my simulator, which had picked the player's lead by party
order when two choices looked equal and so skewed every earlier boss reading,
and the legality sweep against the final lists (origin/balance-tm-pass at
377312dbf0), which left this split unchanged: from Cyrus 3's split on, Ian allowed any move that fits a team (2026-10-07), so Cyrus 3 keeps today's Magma Storm and Draco Meteor. Ian ruled that every draft goes into step 12 as
drafted; the scorer's step 15 reading gives the real numbers, and he chooses
any retunes from them. My candidates are in `../retune-proposals-not-approved/`.

The bosses of the Galactic split are combed: Officers Somnu, Moira, Hesperid
and Argo on Mt. Coronet, Mars and Jupiter together at Spear Pillar, Cyrus in
the Distortion World, twelve Ace Trainers on Routes 225 to 229, the four Ace
tag pairs and Commanders Mars and Jupiter on Stark Mountain. All 29 files pass
the checker and the rule audit. The split's ordinary trainers follow in the
later pass.

The cap is 65. Route 228 fights in permanent sand, and its three Ace Trainers
(Jose, Moira, Meagan) are built for it, with no Sand Veil. Mt. Coronet's 3F,
4F and Somnu on 5F are a gauntlet, so Somnu sits a level lower than the
officers outside it. No other map here has its own weather. My simulator
reads the bosses against the scorer's box at this split, which knows no TMs,
so they read harsher than they will once the TM pass lands. It now also
models Outrage's lock and the confusion after it, Wonder Guard, and Galarian
forms in the box, and Ian's move reworks of 2026-10-06 (Outrage and the
other rampage moves as one-turn attacks, the recharge moves without recharge,
multi-hit moves at 25 a hit); Cyrus 3, Felix and Rodolfo carry Outrage and
were read again under them. Cyrus 3 is today's file moved up to the cap's
levels, as Ian chose, and reads about 72 won to today's 97. Somnu reads
about 84 to today's 100 with her sleep restored. Moira and Argo now sit three
under the cap with sharper sets, as Ian's rule that levels follow importance
asks of officers, and read about 99 and 83 (Moira's hail lasts the whole
fight, as Oxide's battle code has it; under my earlier five-turn rule she read
97.5); Hesperid reads 95 and both
Stark Mountain commanders 95 to 96, to today's 100. Somnu's Hypno and Darkrai keep Dream Eater, the split's conditional
attacks. Ian's four-way reading showed that most of the officers' rise came
from their levels, which led to the new rule; it applies to the finished
splits at the legality sweep, so Hesperid, Somnu and the Stark commanders
keep their levels until then.
These files are built against the learnset lists of 2026-10-06 evening; the
single legality sweep after the TM pass covers them with every other split.

## Decisions for Ian

Ian answered both on 2026-10-06: Cyrus 3 is today's file at the cap's levels,
Gyarados and Regirock included, exempt from the one-legendary rule and the
target of about 80; Somnu has more than one sleep source, her Darkrai keeping
Dark Void; and Moira and Argo get a little harder at lower levels.

| # | Decision | What the files do today | How it is checked | What Ian decides |
|---|---|---|---|---|
| 1 | Cyrus 3 (Ian: today's team at the cap's levels) | Today's six exactly, moved up by rank to 63 to 65. It has no hazard lead, which the dial asks of Cyrus, because Ian chose today's team. | `galactic_boss_cyrus_distortion_world.json`; the scorer's reading later. | Answered (2026-10-06). |
| 2 | Officers keep today's ideas, without the dice (Ian: Somnu keeps several sleep sources) | Somnu has three sleepers (Jumpluff, Hypno, and Darkrai's Dark Void, which the checker flags until the Balance Agent adds it to Darkrai's egg moves); Hesperid keeps one of today's four trades (three Explosions and a Destiny Bond); Argo keeps the Wonder Guard Shedinja and the Arena Trap Dugtrio. | The four files. | Accept (recommended). |
| 3 | Argo's Gengar | Sharper sets alone could not make Argo harder three levels down (about 98 won at best), so a Gengar takes Vespiquen's place; it reads about 83 in the corrected reading. | `dummy_834.json`. | Accept (recommended), or Vespiquen back at about 98. |
| 4 | Spear Pillar and Stark Mountain tags | Mars and Jupiter bring five each at 62 to 63, beside Barry; the four Ace pairs bring four each. | The scorer cannot read tag battles yet. | Nothing now. |

Ace Trainers stay as built (Ian, 2026-10-06): with a planned six these read
84 to 100 won in the corrected reading (Saul 84, Jose 86, the rest 98 to 100), after Jose's Swords Dance Garchomp and Saul's Curse
Snorlax (93) were taken down a notch.

## What comes next

Volkner's split's bosses, already built and being read, then Barry's and the
League's, then the ordinary trainers from Maylene's split on.

## Overview

| Trainer | Place | Path | Battle | Size | Levels | The idea | Expected |
|---|---|---|---|---|---|---|---|
| Galactic Officer Somnu | Mt. Coronet 5F | gauntlet, closing 3F to 5F | single, named officer | 6 | 62 to 64 | Somnu's sleep | about 84 / 2.5 / 0 in my simulator, where today's file reads 100 / 0.2 / 80 |
| Galactic Officer Moira | Mt. Coronet 5F | on the path | single, named officer | 6 | 60 to 62 | Moira's hail | about 99 / 2.2 / 0 in my simulator, where today's file reads 100 / 0.4 / 71 |
| Galactic Officer Hesperid | Mt. Coronet 6F | on the path | single, named officer | 6 | 63 to 65 | Today's six kept to one trade | about 95 / 1.7 / 9 in my simulator, where today's file reads 100 / 0.2 / 82 |
| Galactic Officer Argo | Mt. Coronet 6F | on the path | single, named officer | 6 | 61 to 62 | Today's puzzle box | about 83 / 3.4 / 3 in my simulator, where today's file reads 100 / 0.3 / 75 |
| Commander Mars | Spear Pillar | on the path | tag with Jupiter, beside Barry | 5 | 62 to 63 | Mars 2's core at Spear Pillar | not readable yet (a tag battle) |
| Commander Jupiter | Spear Pillar | on the path | tag with Mars, beside Barry | 5 | 62 to 63 | Jupiter's poison at Spear Pillar | not readable yet (a tag battle) |
| Cyrus 3 | Distortion World | on the path | single, boss | 6 | 63 to 65 | Today's file moved up to the cap's levels | about 72 / 3.1 / 6 in my simulator, where today's file reads 97 / 1.3 / 31 |
| Ace Trainer Rodolfo | Route 225 | optional | single, Ace Trainer | 6 | 62 to 64 | A balanced core | about 99 / 2.0 / 2 with a planned six |
| Ace Trainer Quinn | Route 225 | optional | single, Ace Trainer | 6 | 62 to 64 | Bugs behind support | about 99 / 0.6 / 60 with a planned six |
| Ace Trainer Deanna | Route 225 | optional | single, Ace Trainer | 6 | 62 to 64 | Special attackers | about 100 / 0.2 / 80 with a planned six |
| Ace Trainer Graham | Route 226 | optional | single, Ace Trainer | 6 | 62 to 64 | Fighting types | about 100 / 1.5 / 12 with a planned six |
| Ace Trainer Saul | Route 227 | optional | single, Ace Trainer | 6 | 62 to 64 | Normal types | about 84 / 3.3 / 0 with a planned six |
| Ace Trainer Mikayla | Route 227 | optional | single, Ace Trainer | 6 | 62 to 64 | Dark types | about 98 / 1.1 / 13 with a planned six |
| Ace Trainer Jose | Route 228 (sand) | optional | single, Ace Trainer | 6 | 62 to 64 | Sand | about 86 / 3.4 / 0 with a planned six in sand |
| Ace Trainer Moira | Route 228 (sand) | optional | single, Ace Trainer | 6 | 62 to 64 | Ground and Rock in the sand | about 98 / 1.4 / 1 with a planned six in sand |
| Ace Trainer Meagan | Route 228 (sand) | optional | single, Ace Trainer | 6 | 62 to 64 | Mixed in the sand | about 100 / 1.2 / 16 with a planned six in sand |
| Ace Trainer Felix | Route 229 | optional | single, Ace Trainer | 6 | 62 to 64 | Ghosts and dragons | about 100 / 2.5 / 0 with a planned six |
| Ace Trainer Dana | Route 229 | optional | single, Ace Trainer | 6 | 62 to 64 | Psychic and Dark | about 100 / 1.5 / 0 with a planned six |
| Ace Trainer Sandra | Route 229 | optional | single, Ace Trainer | 6 | 62 to 64 | Today's Ninetales | about 100 / 0.8 / 38 with a planned six |
| Ace Trainer Keenan | Stark Mountain room 2 | optional | tag with Kassandra | 4 | 62 to 63 | Primeape | not readable yet (a tag battle) |
| Ace Trainer Kassandra | Stark Mountain room 2 | optional | tag with Keenan | 4 | 62 to 63 | Jumpluff's Sleep Powder and Memento | not readable yet (a tag battle) |
| Ace Trainer Stefan | Stark Mountain room 2 | optional | tag with Jasmin | 4 | 62 to 63 | Tyranitar's Sand Stream | not readable yet (a tag battle) |
| Ace Trainer Jasmin | Stark Mountain room 2 | optional | tag with Stefan | 4 | 62 to 63 | Drapion | not readable yet (a tag battle) |
| Ace Trainer Skylar | Stark Mountain room 2 | optional | tag with Natasha | 4 | 62 to 63 | Exploud | not readable yet (a tag battle) |
| Ace Trainer Natasha | Stark Mountain room 2 | optional | tag with Skylar | 4 | 62 to 63 | Wigglytuff's screens | not readable yet (a tag battle) |
| Ace Trainer Abel | Stark Mountain room 2 | optional | tag with Monique | 4 | 62 to 63 | Glalie | not readable yet (a tag battle) |
| Ace Trainer Monique | Stark Mountain room 2 | optional | tag with Abel | 4 | 62 to 63 | Luxray | not readable yet (a tag battle) |
| Commander Mars | Stark Mountain room 1 | optional | single, boss | 6 | 63 to 65 | Mars's last stand | about 95 / 1.2 / 13 in my simulator, where today's file reads 100 / 0.0 / 100 |
| Commander Jupiter | Stark Mountain room 1 | optional | single, boss | 6 | 63 to 65 | Jupiter's last stand | about 96 / 2.0 / 6 in my simulator, where today's file reads 100 / 0.0 / 99 |

Expected numbers are won / faints a fight / clean in my simulator, beside
today's file where it was read.

## The bosses

### Galactic Officer Somnu: Mt. Coronet 5F, gauntlet, closing 3F to 5F, single, named officer, cap 65

Somnu's sleep, as Ian asked, from three sources: Jumpluff's Sleep Powder behind a Focus Sash, Hypno's Hypnosis and Dream Eater, and Darkrai's Dark Void and Dream Eater (Dark Void waits on the Balance Agent adding it to Darkrai's egg moves), with Swalot's Destiny Bond as the trade, Stantler, and a Whiscash ace. She closes a gauntlet, so she sits a level lower than the officers outside it.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Jumpluff | 62 | Focus Sash | Chlorophyll | Jolly | Sleep Powder, U-turn, Leech Seed, Encore |
| Swalot | 62 | Sitrus Berry | Gluttony | Calm | Sludge Bomb, Destiny Bond, Encore, Toxic |
| Hypno | 62 | Leftovers | Insomnia | Calm | Hypnosis, Dream Eater, Psychic, Fire Punch |
| Stantler | 62 | Sitrus Berry | Intimidate | Adamant | Take Down, Zen Headbutt, Earthquake, Sucker Punch |
| Darkrai | 63 | Lum Berry | Bad Dreams | Timid | Dark Void, Dream Eater, Dark Pulse, Focus Blast |
| Whiscash | 64 | Wacan Berry | Swift Swim | Adamant | Waterfall, Earthquake, Stone Edge, Zen Headbutt |

Today's team: Swalot 55 (Starf Berry; Amnesia, Gunk Shot, Encore, Yawn), Hypno 55 (Leftovers; Flatter, Hypnosis, Dream Eater, Drain Punch), Jumpluff 52 (Yache Berry; Cotton Spore, U-turn, Sleep Powder, Leech Seed), Stantler 54 (Sitrus Berry; Hypnosis, Return, Megahorn, Dream Eater), Darkrai 50 (Wide Lens; Dark Void, Dream Eater, Dark Pulse, Focus Blast), Whiscash 56 (Wave Incense; Dragon Dance, Aqua Tail, Earthquake, Amnesia). Expected: about 84 / 2.5 / 0 in my simulator, where today's file reads 100 / 0.2 / 80.

### Galactic Officer Moira: Mt. Coronet 5F, on the path, single, named officer, cap 65

Moira's hail, three levels under the cap with sharper sets: Abomasnow's Snow Warning, whose hail lasts the whole fight (its Icy Rock does nothing, since rocks extend only weather from a move), Blizzard that cannot miss on Abomasnow and Slowking, Mamoswine's Ice Shard, a Life Orb Gardevoir with Calm Mind, Celebi as the legendary, and a Swords Dance Absol ace with a Scope Lens.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Abomasnow | 60 | Icy Rock | Snow Warning | Modest | Blizzard, Wood Hammer, Earthquake, Ice Shard |
| Slowking | 61 | Leftovers | Regenerator | Modest | Surf, Psychic, Blizzard, Slack Off |
| Mamoswine | 61 | NeverMeltIce | Thick Fat | Adamant | Earthquake, Ice Fang, Ice Shard, Stone Edge |
| Gardevoir | 61 | Life Orb | Magic Guard | Modest | Psychic, Thunderbolt, Focus Blast, Calm Mind |
| Celebi | 61 | Leftovers | Natural Cure | Modest | Energy Ball, Psychic, Earth Power, Recover |
| Absol | 62 | Scope Lens | Super Luck | Adamant | Knock Off, Superpower, Stone Edge, Swords Dance |

Today's team: Abomasnow 54 (Occa Berry; Swagger, Earthquake, Avalanche, Endeavor), Slowking 54 (Leftovers; Calm Mind, Blizzard, Future Sight, Surf), Gardevoir 55 (Life Orb; Future Sight, Psychic, Calm Mind, Focus Blast), Mamoswine 53 (Lum Berry; Ice Shard, Earthquake, Superpower, Stone Edge), Celebi 50 (Sitrus Berry; Future Sight, AncientPower, Leaf Storm, Recover), Absol 57 (Focus Band; Pursuit, Perish Song, Future Sight, Detect). Expected: about 99 / 2.2 / 0 in my simulator, where today's file reads 100 / 0.4 / 71.

### Galactic Officer Hesperid: Mt. Coronet 6F, on the path, single, named officer, cap 65

Today's six kept to one trade: Drifblim leads behind a Focus Sash (its Explosion and Destiny Bond are gone), Weezing keeps the Explosion, Girafarig passes Agility, a Life Orb Sceptile, Rampardos's Head Smash and Rock Polish, and a Camerupt ace with Eruption and Stealth Rock.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Drifblim | 63 | Focus Sash | Unburden | Timid | Shadow Ball, Thunderbolt, Will-O-Wisp, Stockpile |
| Weezing | 63 | Black Sludge | Levitate | Bold | Sludge Bomb, Will-O-Wisp, Thunderbolt, Explosion |
| Girafarig | 63 | Starf Berry | Quick Feet | Timid | Agility, Baton Pass, Psychic, Thunderbolt |
| Sceptile | 64 | Life Orb | Overgrow | Naive | Leaf Storm, Focus Blast, Earthquake, Rock Slide |
| Rampardos | 64 | Lum Berry | Rock Head | Adamant | Head Smash, Zen Headbutt, Earthquake, Rock Polish |
| Camerupt | 65 | Passho Berry | Solid Rock | Modest | Eruption, Earth Power, Flamethrower, Stealth Rock |

Today's team: Weezing 55 (Poison Barb; Payback, Sludge Bomb, Explosion, Will-O-Wisp), Sceptile 54 (Petaya Berry; Rock Slide, Pursuit, Aerial Ace, Leaf Storm), Girafarig 52 (Starf Berry; Agility, Baton Pass, Earthquake, Thunder), Rampardos 53 (Lum Berry; Head Smash, Pursuit, Rock Polish, Zen Headbutt), Drifblim 54 (Focus Sash; Explosion, Ominous Wind, Curse, Destiny Bond), Camerupt 56 (Passho Berry; Overheat, Earthquake, Explosion, Will-O-Wisp). Expected: about 95 / 1.7 / 9 in my simulator, where today's file reads 100 / 0.2 / 82.

### Galactic Officer Argo: Mt. Coronet 6F, on the path, single, named officer, cap 65

Today's puzzle box, three levels under the cap: Protean Kecleon lays Stealth Rock, a Gengar takes Vespiquen's place, the Wonder Guard Shedinja that only super-effective hits touch, Dugtrio's Arena Trap behind a Focus Sash (the trade), Rotom with a Spooky Plate, and a Life Orb Relicanth ace with Rock Polish.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Kecleon | 61 | Lum Berry | Protean | Adamant | Stealth Rock, Shadow Claw, Drain Punch, Knock Off |
| Gengar | 61 | Wise Glasses | Levitate | Timid | Shadow Ball, Sludge Bomb, Focus Blast, Thunderbolt |
| Shedinja | 61 | SilverPowder | Wonder Guard | Adamant | X-Scissor, Shadow Sneak, Will-O-Wisp, Sucker Punch |
| Dugtrio | 61 | Focus Sash | Arena Trap | Jolly | Earthquake, Stone Edge, Sucker Punch, Aerial Ace |
| Rotom | 61 | Spooky Plate | Levitate | Timid | Thunderbolt, Shadow Ball, Will-O-Wisp, Volt Switch |
| Relicanth | 62 | Life Orb | Rock Head | Adamant | Double-Edge, Waterfall, Earthquake, Rock Polish |

Today's team: Kecleon 55 (Flame Orb; Dizzy Punch, Rock Tomb, Trick, Fling), Vespiquen 54 (SilverPowder; Attack Order, Defend Order, Heal Order), Dugtrio 57 (Focus Sash; Earthquake, Magnitude, Pursuit, Rock Slide), Shedinja 55 (Focus Sash; Sucker Punch, X-Scissor, Swagger, Shadow Sneak), Relicanth 54 (Rock Incense; Head Smash, Double-Edge, Rock Polish, Aqua Tail), Rotom 53 (Wise Glasses; Will-O-Wisp, Discharge, Overheat, Ominous Wind). Expected: about 83 / 3.4 / 3 in my simulator, where today's file reads 100 / 0.3 / 75.

### Commander Mars: Spear Pillar, on the path, tag with Jupiter, beside Barry, cap 65

Mars 2's core at Spear Pillar: Bronzong leads with Stealth Rock and Hypnosis, then Crobat, Umbreon's Toxic, a Luxray with an Expert Belt and Purugly's Fake Out at the top.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Bronzong | 62 | Leftovers | Levitate | Relaxed | Stealth Rock, Gyro Ball, Earthquake, Hypnosis |
| Crobat | 62 | Sharp Beak | Inner Focus | Jolly | Brave Bird, Cross Poison, U-turn, Roost |
| Umbreon | 62 | Leftovers | Synchronize | Calm | Payback, Toxic, Wish, Protect |
| Luxray | 62 | Expert Belt | Tinted Lens | Adamant | Thunder Fang, Crunch, Superpower, Ice Fang |
| Purugly | 63 | Silk Scarf | Defiant | Jolly | Fake Out, Body Slam, Sucker Punch, Knock Off |

Today's team: Solrock 58 (King’s Rock; Zen Headbutt, Rock Slide, Light Screen, Will-O-Wisp), Delcatty 58 (Silk Scarf; Fake Out, Copycat, Last Resort), Luxray 58 (Magnet; Thunder Fang, Ice Fang, Charge, Magnet Rise), Bronzong 58 (Sitrus Berry; Curse, Gyro Ball, Zen Headbutt, Recycle), Purugly 59 (Life Orb; Slash, Fake Out, Sucker Punch, Hypnosis). Expected: not readable yet (a tag battle).

### Commander Jupiter: Spear Pillar, on the path, tag with Mars, beside Barry, cap 65

Jupiter's poison at Spear Pillar: Drapion leads with Toxic Spikes behind a Focus Sash, then Lunatone's Calm Mind, Tangrowth's Sleep Powder, Spiritomb's Will-O-Wisp and a Skuntank ace.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Drapion | 62 | Focus Sash | Hyper Cutter | Jolly | Toxic Spikes, Cross Poison, Crunch, Earthquake |
| Lunatone | 62 | Leftovers | Levitate | Modest | Psychic, Earth Power, Ice Beam, Calm Mind |
| Tangrowth | 62 | Leftovers | Regenerator | Relaxed | Seed Bomb, Earthquake, Knock Off, Sleep Powder |
| Spiritomb | 62 | Leftovers | Pressure | Careful | Shadow Ball, Sucker Punch, Will-O-Wisp, Pain Split |
| Skuntank | 63 | Dread Plate | Aftermath | Adamant | Crunch, Poison Jab, Sucker Punch, Fire Blast |

Today's team: Lunatone 58 (Quick Claw; Psychic, AncientPower, Earth Power, Stealth Rock), Drapion 58 (Shuca Berry; Cross Poison, Toxic, Ice Fang, Earthquake), Tangrowth 58 (Toxic Orb; Facade, Power Whip, Protect, Fling), Spiritomb 58 (Leftovers; Torment, Shadow Sneak, Pursuit, Spite), Skuntank 59 (Choice Specs; Dark Pulse, Sludge Bomb, Flamethrower, Hyper Beam). Expected: not readable yet (a tag battle).

### Cyrus 3: Distortion World, on the path, single, boss, cap 65

Today's file moved up to the cap's levels, as Ian chose: Dusknoir's Will-O-Wisp, Gyarados, a Focus Sash Heatran with Magma Storm, a Life Orb Flygon with Draco Meteor, Regirock's Curse and Explosion (the trade), and Salamence at the cap with a King's Rock. Heatran and Regirock are the two legendaries Ian allowed him. Magma Storm and Draco Meteor are not in their lists at 63, which Ian's late-game ruling allows.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Dusknoir | 63 | Lum Berry | Levitate | Lonely | Shadow Punch, Payback, Earthquake, Will-O-Wisp |
| Gyarados | 63 | Wacan Berry | Intimidate | Lonely | Aqua Tail, Avalanche, Stone Edge, Earthquake |
| Heatran | 63 | Focus Sash | Flash Fire | Hasty | Magma Storm, Earth Power, Flash Cannon, AncientPower |
| Flygon | 63 | Life Orb | Levitate | Lonely | Earth Power, Draco Meteor, U-turn, Stone Edge |
| Regirock | 64 | Leftovers | Solid Rock | Brave | Curse, Explosion, Stone Edge, Fire Punch |
| Salamence | 65 | King’s Rock | Intimidate | Lonely | Rock Slide, Dragon Rush, Swagger, Fire Fang |

Today's team: Dusknoir 59 (Lum Berry; Shadow Punch, Payback, Earthquake, Will-O-Wisp), Gyarados 59 (Wacan Berry; Aqua Tail, Avalanche, Stone Edge, Earthquake), Heatran 59 (Focus Sash; Magma Storm, Earth Power, Flash Cannon, AncientPower), Flygon 59 (Life Orb; Earth Power, Draco Meteor, U-turn, Stone Edge), Regirock 59 (Leftovers; Curse, Explosion, Stone Edge, Fire Punch), Salamence 59 (King’s Rock; Rock Slide, Dragon Rush, Swagger, Fire Fang). Expected: about 72 / 3.1 / 6 in my simulator, where today's file reads 97 / 1.3 / 31.

### Ace Trainer Rodolfo: Route 225, optional, single, Ace Trainer, cap 65

A balanced core: Starmie, Venusaur's Sleep Powder, Arcanine, Gengar, Snorlax and a Flygon ace.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Starmie | 62 | Mystic Water | Magic Guard | Timid | Surf, Psychic, Ice Beam, Recover |
| Venusaur | 62 | Black Sludge | Overgrow | Modest | Sludge Bomb, Energy Ball, Earthquake, Sleep Powder |
| Arcanine | 62 | Charcoal | Intimidate | Adamant | Flare Blitz, ExtremeSpeed, Crunch, Thunder Fang |
| Gengar | 63 | Wise Glasses | Levitate | Timid | Shadow Ball, Sludge Bomb, Focus Blast, Thunderbolt |
| Snorlax | 62 | Leftovers | Thick Fat | Careful | Body Slam, Earthquake, Crunch, Fire Punch |
| Flygon | 64 | Yache Berry | Levitate | Jolly | Earthquake, Outrage, Fire Punch, U-turn |

Today's team: Starmie 55 (Surf, Recover, Psychic, Signal Beam), Flygon 55 (Outrage, Earthquake, Fire Punch, Roost), Venusaur 55 (Frenzy Plant, Sludge Bomb, Sleep Powder, Leech Seed). Expected: about 99 / 2.0 / 2 with a planned six; read blind, 38 / 5.2 / 0.

### Ace Trainer Quinn: Route 225, optional, single, Ace Trainer, cap 65

Bugs behind support: Skarmory's Spikes and Whirlwind, Lanturn, Meganium's screens, Heracross, Scizor and a Swords Dance Pinsir ace.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Skarmory | 62 | Focus Sash | Filter | Impish | Spikes, Brave Bird, Roost, Whirlwind |
| Lanturn | 62 | Leftovers | Volt Absorb | Modest | Surf, Discharge, Ice Beam, Confuse Ray |
| Meganium | 62 | Sitrus Berry | Thick Fat | Bold | Energy Ball, Earthquake, Light Screen, Reflect |
| Heracross | 63 | Lum Berry | Guts | Jolly | Close Combat, Megahorn, Stone Edge, Earthquake |
| Scizor | 62 | Metal Coat | Technician | Adamant | Bullet Punch, X-Scissor, U-turn, Swords Dance |
| Pinsir | 64 | SilverPowder | Mold Breaker | Jolly | X-Scissor, Close Combat, Stone Edge, Swords Dance |

Today's team: Pinsir 55 (Superpower, X-Scissor, Swords Dance, Rock Tomb), Lanturn 55 (Discharge, Signal Beam, Surf, Confuse Ray), Meganium 55 (Petal Dance, Light Screen, PoisonPowder, AncientPower). Expected: about 99 / 0.6 / 60 with a planned six; read blind, 29 / 4.9 / 3.

### Ace Trainer Deanna: Route 225, optional, single, Ace Trainer, cap 65

Special attackers: Ampharos's Light Screen, Tropius, Jolteon's Thunder Wave, Gyarados, Togekiss and a Lapras ace.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Ampharos | 62 | Magnet | Static | Modest | Thunderbolt, Power Gem, Signal Beam, Light Screen |
| Tropius | 62 | Leftovers | Overgrow | Modest | Air Slash, Energy Ball, Roost, Earthquake |
| Jolteon | 62 | Lum Berry | Volt Absorb | Timid | Thunderbolt, Shadow Ball, Signal Beam, Thunder Wave |
| Gyarados | 63 | Wacan Berry | Intimidate | Adamant | Waterfall, Earthquake, Ice Fang, Stone Edge |
| Togekiss | 62 | Sitrus Berry | Serene Grace | Modest | Air Slash, Aura Sphere, Flamethrower, Roost |
| Lapras | 64 | Leftovers | Shell Armor | Modest | Surf, Ice Beam, Thunderbolt, Psychic |

Today's team: Ampharos 55 (Thunderbolt, Power Gem, Signal Beam, Light Screen), Tropius 55 (SolarBeam, Air Slash, Synthesis, Sunny Day), Lapras 55 (Surf, Ice Beam, Thunderbolt). Expected: about 100 / 0.2 / 80 with a planned six; read blind, 42 / 4.6 / 1.

### Ace Trainer Graham: Route 226, optional, single, Ace Trainer, cap 65

Fighting types: the Hitmon trio led by Hitmontop's Fake Out behind a Focus Sash, Breloom's Spore, a Life Orb Lucario and a Flame Orb Machamp ace.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Hitmontop | 62 | Focus Sash | Technician | Adamant | Fake Out, Close Combat, Sucker Punch, Stone Edge |
| Hitmonchan | 62 | Black Belt | Iron Fist | Adamant | Drain Punch, Ice Punch, ThunderPunch, Mach Punch |
| Hitmonlee | 62 | Lum Berry | Reckless | Adamant | Hi Jump Kick, Stone Edge, Knock Off, Earthquake |
| Breloom | 62 | Toxic Orb | Poison Heal | Jolly | Seed Bomb, Mach Punch, Stone Edge, Spore |
| Lucario | 63 | Life Orb | Adaptability | Timid | Aura Sphere, Flash Cannon, Dark Pulse, Vacuum Wave |
| Machamp | 64 | Flame Orb | Guts | Adamant | Close Combat, Stone Edge, Ice Punch, Bullet Punch |

Today's team: Hitmonlee 56 (Endure, Reversal, Close Combat, Blaze Kick), Hitmonchan 56 (Mega Punch, Ice Punch, Counter, Close Combat), Hitmontop 56 (Bullet Punch, Detect, Close Combat, Endeavor). Expected: about 100 / 1.5 / 12 with a planned six; read blind, 46 / 4.6 / 0.

### Ace Trainer Saul: Route 227, optional, single, Ace Trainer, cap 65

Normal types: Tauros, Miltank, a Flame Orb Ursaring, an Eviolite Porygon2, Staraptor and a Snorlax ace.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Tauros | 62 | Lum Berry | Intimidate | Jolly | Take Down, Earthquake, Stone Edge, Zen Headbutt |
| Miltank | 62 | Leftovers | Thick Fat | Impish | Body Slam, Earthquake, Milk Drink, Ice Punch |
| Ursaring | 62 | Flame Orb | Guts | Adamant | Facade, Close Combat, Crunch, Earthquake |
| Porygon2 | 62 | Eviolite | Download | Calm | Tri Attack, Ice Beam, Thunderbolt, Recover |
| Staraptor | 63 | Sharp Beak | Intimidate | Jolly | Brave Bird, Close Combat, U-turn, Roost |
| Snorlax | 64 | Leftovers | Thick Fat | Careful | Body Slam, Earthquake, Crunch, Fire Punch |

Today's team: Tauros 60 (Thrash, Zen Headbutt, Swagger, Payback). Expected: about 84 / 3.3 / 0 with a planned six; read blind, 26 / 5.3 / 0.

### Ace Trainer Mikayla: Route 227, optional, single, Ace Trainer, cap 65

Dark types: Persian's Fake Out, Seviper's Glare, Honchkrow, Mightyena, Weavile and a Swords Dance Absol ace with a Scope Lens.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Persian | 62 | Silk Scarf | Technician | Jolly | Fake Out, U-turn, Knock Off, Aerial Ace |
| Seviper | 62 | Poison Barb | Shed Skin | Naive | Sludge Bomb, Crunch, Flamethrower, Glare |
| Honchkrow | 62 | Sharp Beak | Moxie | Adamant | Drill Peck, Night Slash, Sucker Punch, Heat Wave |
| Mightyena | 62 | Sitrus Berry | Intimidate | Adamant | Crunch, Sucker Punch, Ice Fang, Thunder Fang |
| Weavile | 63 | NeverMeltIce | Technician | Jolly | Night Slash, Ice Punch, Ice Shard, Brick Break |
| Absol | 64 | Scope Lens | Super Luck | Adamant | Knock Off, Superpower, Stone Edge, Swords Dance |

Today's team: Seviper 58 (Night Slash, Poison Fang, Wring Out, Glare), Persian 58 (Night Slash, Slash, Faint Attack, Fake Out), Absol 58 (Night Slash, Psycho Cut, Slash, Quick Attack). Expected: about 98 / 1.1 / 13 with a planned six; read blind, 14 / 5.5 / 0.

### Ace Trainer Jose: Route 228 (sand), optional, single, Ace Trainer, cap 65

Sand: a Sand Rush Sandslash lays Stealth Rock behind a Focus Sash, then Golduck, Manectric, Rhyperior, Steelix and a Garchomp ace.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Sandslash | 62 | Focus Sash | Sand Rush | Jolly | Stealth Rock, Earthquake, Stone Edge, Knock Off |
| Golduck | 62 | Mystic Water | Swift Swim | Modest | Surf, Ice Beam, Psychic, Calm Mind |
| Manectric | 62 | Magnet | Lightning Rod | Timid | Thunderbolt, Flamethrower, Signal Beam, Thunder Wave |
| Rhyperior | 63 | Passho Berry | Solid Rock | Adamant | Earthquake, Stone Edge, Ice Punch, Hammer Arm |
| Steelix | 62 | Leftovers | Solid Rock | Adamant | Earthquake, Iron Head, Stone Edge, Ice Fang |
| Garchomp | 64 | Yache Berry | Rough Skin | Jolly | Earthquake, Dragon Claw, Fire Fang, Stone Edge |

Today's team: Golduck 58 (Hydro Pump, Brick Break, Zen Headbutt, Screech), Sandslash 58 (Earthquake, Crush Claw, Poison Jab, Sand Tomb), Manectric 58 (Thunder Fang, Fire Fang, Quick Attack, Giga Impact). Expected: about 86 / 3.4 / 0 with a planned six in sand; read blind, 4 / 5.9 / 0.

### Ace Trainer Moira: Route 228 (sand), optional, single, Ace Trainer, cap 65

Ground and Rock in the sand: Claydol's Stealth Rock, Gastrodon, a Sand Force Dugtrio with Soft Sand, Hippowdon, Golem and a Dragon Dance Tyranitar ace.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Claydol | 62 | Leftovers | Levitate | Modest | Earth Power, Psychic, Ice Beam, Stealth Rock |
| Gastrodon | 62 | Sitrus Berry | Dry Skin | Modest | Earth Power, Surf, Ice Beam, Sludge Bomb |
| Dugtrio | 62 | Soft Sand | Sand Force | Jolly | Earthquake, Stone Edge, Sucker Punch, Aerial Ace |
| Hippowdon | 63 | Leftovers | Thick Fat | Impish | Earthquake, Crunch, Ice Fang, Slack Off |
| Golem | 62 | Hard Stone | Shell Armor | Adamant | Earthquake, Stone Edge, Sucker Punch, Fire Punch |
| Tyranitar | 64 | Chople Berry | Unnerve | Adamant | Stone Edge, Crunch, Earthquake, Dragon Dance |

Today's team: Dugtrio 58 (Earthquake, Fissure, Night Slash, Stone Edge), Gastrodon 58 (Muddy Water, Recover, Toxic, Protect), Claydol 58 (Earthquake, Psychic, AncientPower, Cosmic Power). Expected: about 98 / 1.4 / 1 with a planned six in sand; read blind, 30 / 5.0 / 1.

### Ace Trainer Meagan: Route 228 (sand), optional, single, Ace Trainer, cap 65

Mixed in the sand: Delcatty's Fake Out, an Adaptability Abomasnow, Probopass, Cacturne, a Poison Heal Gliscor and an Aggron ace.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Delcatty | 62 | Silk Scarf | Cute Charm | Jolly | Fake Out, Double-Edge, Sucker Punch, Thunder Wave |
| Abomasnow | 62 | NeverMeltIce | Adaptability | Modest | Blizzard, Energy Ball, Earthquake, Ice Shard |
| Probopass | 62 | Leftovers | Solid Rock | Modest | Power Gem, Earth Power, Flash Cannon, Thunder Wave |
| Cacturne | 63 | Miracle Seed | Water Absorb | Adamant | Seed Bomb, Sucker Punch, Drain Punch, Swords Dance |
| Gliscor | 62 | Toxic Orb | Poison Heal | Jolly | Earthquake, U-turn, Ice Fang, Stone Edge |
| Aggron | 64 | Lum Berry | Rock Head | Adamant | Double-Edge, Iron Head, Earthquake, Stone Edge |

Today's team: Delcatty 59 (Fake Out, Captivate, Faint Attack, Double-Edge), Abomasnow 59 (Ice Shard, Avalanche, Razor Leaf, Water Pulse). Expected: about 100 / 1.2 / 16 with a planned six in sand; read blind, 47 / 4.3 / 1.

### Ace Trainer Felix: Route 229, optional, single, Ace Trainer, cap 65

Ghosts and dragons: Dusknoir's Will-O-Wisp, Gengar, a Nasty Plot Houndoom, a Dragon Dance Altaria, Kingdra and a Salamence ace.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Dusknoir | 62 | Leftovers | Levitate | Adamant | Shadow Punch, Earthquake, Ice Punch, Will-O-Wisp |
| Gengar | 62 | Life Orb | Levitate | Timid | Shadow Ball, Sludge Bomb, Focus Blast, Thunderbolt |
| Houndoom | 62 | Charcoal | Flash Fire | Timid | Flamethrower, Dark Pulse, Sludge Bomb, Nasty Plot |
| Altaria | 63 | Sitrus Berry | Serene Grace | Adamant | Dragon Claw, Earthquake, Roost, Dragon Dance |
| Kingdra | 62 | Mystic Water | Sniper | Modest | Surf, Dragon Pulse, Ice Beam, Signal Beam |
| Salamence | 64 | Yache Berry | Intimidate | Adamant | Outrage, Earthquake, Fire Fang, Aerial Ace |

Today's team: Dusknoir 58 (Shadow Sneak, Payback, Curse, Will-O-Wisp), Salamence 58 (Dragon Claw, Aerial Ace, Zen Headbutt, Crunch). Expected: about 100 / 2.5 / 0 with a planned six; read blind, 32 / 5.4 / 0.

### Ace Trainer Dana: Route 229, optional, single, Ace Trainer, cap 65

Psychic and Dark: Mightyena, Roserade's Spikes, Espeon, Milotic, Umbreon and a Life Orb Gardevoir ace.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Mightyena | 62 | Sitrus Berry | Intimidate | Adamant | Crunch, Sucker Punch, Ice Fang, Thunder Fang |
| Roserade | 62 | Focus Sash | Natural Cure | Timid | Spikes, Sludge Bomb, Energy Ball, Shadow Ball |
| Espeon | 62 | TwistedSpoon | Synchronize | Timid | Psychic, Shadow Ball, Signal Beam, Calm Mind |
| Milotic | 63 | Leftovers | Filter | Bold | Surf, Ice Beam, Recover, Toxic |
| Umbreon | 62 | Leftovers | Synchronize | Calm | Payback, Toxic, Wish, Protect |
| Gardevoir | 64 | Life Orb | Magic Guard | Modest | Psychic, Thunderbolt, Focus Blast, Calm Mind |

Today's team: Mightyena 57 (Crunch, Sucker Punch, Iron Tail, Thunder Fang), Gardevoir 57 (Psychic, Magical Leaf, Shock Wave, Shadow Ball). Expected: about 100 / 1.5 / 0 with a planned six; read blind, 58 / 3.7 / 5.

### Ace Trainer Sandra: Route 229, optional, single, Ace Trainer, cap 65

Today's Ninetales, Raichu and Cacturne grown: Vaporeon's Wish, Toxicroak and a Swords Dance Leafeon ace.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Ninetales | 62 | Charcoal | Magic Guard | Timid | Flamethrower, Energy Ball, Will-O-Wisp, Nasty Plot |
| Raichu | 62 | Magnet | Lightning Rod | Timid | Thunderbolt, Grass Knot, Focus Blast, Thunder Wave |
| Cacturne | 62 | Miracle Seed | Water Absorb | Adamant | Seed Bomb, Sucker Punch, Drain Punch, Swords Dance |
| Vaporeon | 63 | Leftovers | Water Absorb | Bold | Surf, Ice Beam, Wish, Protect |
| Toxicroak | 62 | Black Sludge | Dry Skin | Adamant | Poison Jab, Cross Chop, Sucker Punch, Ice Punch |
| Leafeon | 64 | Lum Berry | Chlorophyll | Jolly | Seed Bomb, X-Scissor, Knock Off, Swords Dance |

Today's team: Cacturne 56 (Seed Bomb, ThunderPunch, Sucker Punch, Destiny Bond), Raichu 56 (Grass Knot, Hidden Power, Thunder Wave, Thunder), Ninetales 56 (Fire Blast, Will-O-Wisp, Energy Ball, Calm Mind). Expected: about 100 / 0.8 / 38 with a planned six; read blind, 64 / 3.1 / 10.

### Ace Trainer Keenan: Stark Mountain room 2, optional, tag with Kassandra, cap 65

Primeape, Electivire, Banette and Magmortar.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Primeape | 62 | Lum Berry | Defiant | Jolly | Close Combat, U-turn, Ice Punch, Stone Edge |
| Electivire | 62 | Expert Belt | Adaptability | Adamant | ThunderPunch, Ice Punch, Cross Chop, Earthquake |
| Banette | 62 | Spell Tag | Cursed Body | Adamant | Shadow Claw, Sucker Punch, Knock Off, Will-O-Wisp |
| Magmortar | 63 | Charcoal | Flame Body | Modest | Flamethrower, Thunderbolt, Focus Blast, Psychic |

Today's team: Primeape 60 (Cross Chop, Ice Punch, U-turn, Close Combat), Electivire 60 (Thunderbolt, Flamethrower, Psychic, Thunder Wave), Banette 60 (Shadow Ball, Psychic, Thunderbolt, Will-O-Wisp). Expected: not readable yet (a tag battle).

### Ace Trainer Kassandra: Stark Mountain room 2, optional, tag with Keenan, cap 65

Jumpluff's Sleep Powder and Memento, Steelix, Ampharos and Starmie.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Jumpluff | 62 | Focus Sash | Chlorophyll | Jolly | U-turn, Leech Seed, Sleep Powder, Memento |
| Steelix | 62 | Leftovers | Solid Rock | Adamant | Earthquake, Iron Head, Stone Edge, Ice Fang |
| Ampharos | 62 | Magnet | Static | Modest | Thunderbolt, Power Gem, Signal Beam, Focus Blast |
| Starmie | 63 | Mystic Water | Magic Guard | Timid | Surf, Psychic, Ice Beam, Thunderbolt |

Today's team: Jumpluff 60 (Memento, Giga Drain, Toxic, Bounce), Steelix 60 (Stone Edge, Earthquake, Iron Head, Thunder Fang), Ampharos 60 (ThunderPunch, Power Gem, Signal Beam, Fire Punch). Expected: not readable yet (a tag battle).

### Ace Trainer Stefan: Stark Mountain room 2, optional, tag with Jasmin, cap 65

Tyranitar's Sand Stream, Torterra, Xatu and Garchomp.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Tyranitar | 62 | Chople Berry | Sand Stream | Adamant | Stone Edge, Crunch, Earthquake, Ice Punch |
| Torterra | 62 | Miracle Seed | Thick Fat | Adamant | Wood Hammer, Earthquake, Stone Edge, Crunch |
| Xatu | 62 | Leftovers | Magic Guard | Timid | Psychic, Drill Peck, Heat Wave, Roost |
| Garchomp | 63 | Yache Berry | Rough Skin | Jolly | Earthquake, Dragon Claw, Fire Fang, Stone Edge |

Today's team: Tyranitar 60 (Crunch, Earthquake, Stone Edge, ThunderPunch), Torterra 60 (Synthesis, Crunch, Stone Edge, Wood Hammer), Xatu 60 (Roost, Air Cutter, Heat Wave, Psychic). Expected: not readable yet (a tag battle).

### Ace Trainer Jasmin: Stark Mountain room 2, optional, tag with Stefan, cap 65

Drapion, Magcargo, Sceptile and Vaporeon's Helping Hand.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Drapion | 62 | Black Sludge | Hyper Cutter | Jolly | Cross Poison, Crunch, Earthquake, X-Scissor |
| Magcargo | 62 | Charcoal | Solid Rock | Modest | Flamethrower, Earth Power, AncientPower, Will-O-Wisp |
| Sceptile | 62 | Miracle Seed | Overgrow | Jolly | Leaf Blade, Earthquake, Dragon Claw, X-Scissor |
| Vaporeon | 63 | Leftovers | Water Absorb | Bold | Surf, Ice Beam, Wish, Helping Hand |

Today's team: Drapion 60 (Cross Poison, Crunch, X-Scissor, Aerial Ace), Magcargo 60 (Flamethrower, Earth Power, AncientPower, Toxic), Sceptile 60 (Leaf Blade, Night Slash, Dragon Claw, ThunderPunch). Expected: not readable yet (a tag battle).

### Ace Trainer Skylar: Stark Mountain room 2, optional, tag with Natasha, cap 65

Exploud, Rampardos, Pelipper and Fearow.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Exploud | 62 | Silk Scarf | Scrappy | Modest | Hyper Voice, Flamethrower, Focus Blast, Ice Beam |
| Rampardos | 62 | Lum Berry | Rock Head | Adamant | Head Smash, Zen Headbutt, Earthquake, Fire Punch |
| Pelipper | 62 | Mystic Water | Unburden | Modest | Surf, Air Slash, Ice Beam, Roost |
| Fearow | 63 | Sharp Beak | Sniper | Jolly | Drill Peck, Tri Attack, U-turn, Heat Wave |

Today's team: Exploud 60 (Hyper Voice, Flamethrower, Focus Blast, Ice Beam), Rampardos 60 (Head Smash, Zen Headbutt, Earthquake, ThunderPunch), Pelipper 60 (Air Slash, Hydro Pump, Roost, Ice Beam). Expected: not readable yet (a tag battle).

### Ace Trainer Natasha: Stark Mountain room 2, optional, tag with Skylar, cap 65

Wigglytuff's screens, Lopunny's Fake Out, Medicham and Alakazam.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Wigglytuff | 62 | Leftovers | Cute Charm | Modest | Hyper Voice, Reflect, Light Screen, Flamethrower |
| Lopunny | 62 | Silk Scarf | Scrappy | Jolly | Fake Out, Jump Kick, Dizzy Punch, Ice Punch |
| Medicham | 62 | Black Belt | Pure Power | Adamant | Hi Jump Kick, Zen Headbutt, Ice Punch, Bullet Punch |
| Alakazam | 63 | TwistedSpoon | Magic Guard | Timid | Psychic, Focus Blast, Shadow Ball, Energy Ball |

Today's team: Wigglytuff 60 (Hyper Voice, Reflect, Light Screen, Shadow Ball), Lopunny 60 (Bounce, Jump Kick, Fire Punch, Ice Punch), Medicham 60 (Recover, Psycho Cut, Hi Jump Kick, Ice Punch). Expected: not readable yet (a tag battle).

### Ace Trainer Abel: Stark Mountain room 2, optional, tag with Monique, cap 65

Glalie, Crobat, Typhlosion's Eruption and Gyarados.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Glalie | 62 | Focus Sash | Ice Body | Jolly | Ice Shard, Crunch, Earthquake, Ice Fang |
| Crobat | 62 | Sharp Beak | Inner Focus | Jolly | Brave Bird, Cross Poison, U-turn, Confuse Ray |
| Typhlosion | 62 | Charcoal | Blaze | Timid | Eruption, Flamethrower, Focus Blast, ThunderPunch |
| Gyarados | 63 | Wacan Berry | Intimidate | Adamant | Waterfall, Earthquake, Ice Fang, Stone Edge |

Today's team: Glalie 60 (Dark Pulse, Ice Beam, Sheer Cold, Crunch), Crobat 60 (Brave Bird, Cross Poison, Confuse Ray, U-turn), Typhlosion 60 (Eruption, Focus Blast, ThunderPunch, Low Kick). Expected: not readable yet (a tag battle).

### Ace Trainer Monique: Stark Mountain room 2, optional, tag with Abel, cap 65

Luxray, a Flame Orb Ursaring, Gliscor and Kangaskhan's Fake Out.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Luxray | 62 | Magnet | Tinted Lens | Adamant | Thunder Fang, Crunch, Superpower, Ice Fang |
| Ursaring | 62 | Flame Orb | Guts | Adamant | Facade, Close Combat, Crunch, Earthquake |
| Gliscor | 62 | Toxic Orb | Poison Heal | Jolly | Earthquake, U-turn, Ice Fang, Stone Edge |
| Kangaskhan | 63 | Sitrus Berry | Scrappy | Adamant | Double-Edge, Earthquake, Sucker Punch, Fake Out |

Today's team: Luxray 60 (Discharge, Crunch, Thunder Wave, Facade), Ursaring 60 (Hammer Arm, Stone Edge, Swords Dance, Giga Impact), Gliscor 60 (Aerial Ace, X-Scissor, Earthquake, Quick Attack). Expected: not readable yet (a tag battle).

### Commander Mars: Stark Mountain room 1, optional, single, boss, cap 65

Mars's last stand: Bronzong leads with Stealth Rock and Explosion (the trade) behind a Focus Sash, then Persian's Fake Out, Crobat, Umbreon, Purugly and a Luxray ace with Howl.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Bronzong | 63 | Focus Sash | Levitate | Relaxed | Stealth Rock, Gyro Ball, Earthquake, Explosion |
| Persian | 63 | Silk Scarf | Technician | Jolly | Fake Out, U-turn, Knock Off, Aerial Ace |
| Crobat | 64 | Sharp Beak | Inner Focus | Jolly | Brave Bird, Cross Poison, U-turn, Roost |
| Umbreon | 64 | Leftovers | Synchronize | Calm | Payback, Toxic, Wish, Protect |
| Purugly | 64 | Sitrus Berry | Defiant | Jolly | Body Slam, Sucker Punch, Knock Off, U-turn |
| Luxray | 65 | Expert Belt | Tinted Lens | Adamant | Thunder Fang, Crunch, Superpower, Howl |

Today's team: Solrock 59 (Zen Headbutt, Stone Edge, Light Screen, Will-O-Wisp), Persian 59 (Fake Out, Headbutt, Aerial Ace, U-turn), Purugly 60 (Sitrus Berry; Slash, Shadow Claw, Aerial Ace, Hypnosis). Expected: about 95 / 1.2 / 13 in my simulator, where today's file reads 100 / 0.0 / 100.

### Commander Jupiter: Stark Mountain room 1, optional, single, boss, cap 65

Jupiter's last stand: Drapion's Toxic Spikes behind a Focus Sash, Lunatone's Stealth Rock, Tangrowth's Sleep Powder, Spiritomb, Crobat and a Skuntank ace.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Drapion | 63 | Focus Sash | Hyper Cutter | Jolly | Toxic Spikes, Cross Poison, Crunch, Earthquake |
| Lunatone | 63 | Leftovers | Levitate | Modest | Stealth Rock, Psychic, Earth Power, Ice Beam |
| Tangrowth | 64 | Leftovers | Regenerator | Relaxed | Seed Bomb, Earthquake, Knock Off, Sleep Powder |
| Spiritomb | 64 | Leftovers | Pressure | Careful | Shadow Ball, Sucker Punch, Will-O-Wisp, Pain Split |
| Crobat | 64 | Sharp Beak | Inner Focus | Jolly | Brave Bird, Cross Poison, U-turn, Roost |
| Skuntank | 65 | Dread Plate | Aftermath | Adamant | Crunch, Poison Jab, Fire Blast, Sucker Punch |

Today's team: Lunatone 59 (Psychic, AncientPower, Earth Power, Stealth Rock), Delcatty 59 (Ice Beam, Thunderbolt, Shadow Ball, Thunder Wave), Skuntank 60 (Sitrus Berry; Night Slash, Poison Jab, Flamethrower, SmokeScreen). Expected: about 96 / 2.0 / 6 in my simulator, where today's file reads 100 / 0.0 / 99.


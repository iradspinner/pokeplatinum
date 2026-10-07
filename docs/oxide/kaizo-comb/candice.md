# The comb: Candice's split

**Refreshed 2026-10-07.** The expected numbers were read again after two
changes: a fix to my simulator, which had picked the player's lead by party
order when two choices looked equal and so skewed every earlier boss reading,
and the legality sweep against the final lists (origin/balance-tm-pass at
377312dbf0), which changed three moves here: Hesperid's and Ace Trainer Laura's Tangrowth trade Power Whip for Seed Bomb, and Ace Trainer Olivia's Altaria trades Dragon Dance for Agility. Ian ruled that every draft goes into step 12 as
drafted; the scorer's step 15 reading gives the real numbers, and he chooses
any retunes from them. My candidates are in `../retune-proposals-not-approved/`.

The bosses of Candice's split are combed: Officer Hesperid and Saturn at
Lake Valor, the Somnu and Moira tag and Mars at Lake Verity, twelve Ace
Trainers on Routes 216 and 217 and in Snowpoint's gym, and Candice. All 19
files pass the checker and the rule audit. The split's ordinary trainers
follow in the later pass.

The cap is 56 throughout. Route 217 and Snowpoint's gym fight in permanent
hail (Ian, 2026-10-06), so Blizzard never misses there, Ice types take no
chip, and Ice Body heals; no team on those maps holds Snow Cloak, which the
evasion rule would count. Route 216, Snowpoint City and Acuity Lakefront have
changing weather and are read without it; the lakes have none. My simulator
reads the bosses against the scorer's box at Candice, which knows no TMs, so
they read harsher than they will once the TM pass lands. It now also models
trapping abilities, Counter, Mirror Coat and Destiny Bond. Saturn reads
about 80 won to today's 94, Mars about 91 to today's 100, and Hesperid about
level on wins with far more faints. Candice reads about 90 won to today's
94; today's file earns much of its difficulty with Snow Cloak and Double Team
evasion the dial bars, so mine gets close without it. Somnu's Swalot keeps Dream Eater, the split's one
conditional attack.

## Decisions for Ian

| # | Decision | What the files do today | How it is checked | What Ian decides |
|---|---|---|---|---|
| 1 | Candice is only a little harder than today's (90 won to 94) | Froslass leads with Spikes behind a Focus Sash, Walrein heals with Ice Body and phazes with Roar, then Glaceon, Mamoswine, Articuno (the legendary) and an Adaptability Abomasnow ace. She carries no trade, since Oxide's Froslass has no Destiny Bond. A Weavile in Glaceon's place read 75 won, far past a step. | `leader_candice.json`; the scorer's reading in hail later. | Accept (recommended: today's file earns its 94 with evasion the dial bars), or take the Weavile version. |
| 2 | Saturn's trap is a Shadow Tag Wobbuffet | Wobbuffet traps whatever it faces and carries Counter but not Mirror Coat; with Mirror Coat as well the fight read 69 to 77 won. The trap is Saturn's one trade. Azelf leads with Stealth Rock, and Toxicroak is the Swords Dance ace. | `commander_saturn_valor_cavern.json`; the scorer's reading later. | Accept (recommended), or give the trap to a Dugtrio (Arena Trap), which read harder still. |
| 3 | Ace Trainers, tuned on the planned reading | The dial's numbers for this split first gave readings from 47 to 100 won with a planned six. Seven teams were softened toward Byron's band (94 to 100) and now read 90 to 100, mostly by moving the non-ace members two or three levels under the ace, as Rule 2 allows, and by taking setup moves off them. Met blind they win 7 to 72 percent of fights in my simulator. | My readings now; the scorer's planned reading after the TM pass; Ian's alpha run. | The same choice as Byron's decision 3, which covers both splits. |
| 4 | Lake Verity tag | Somnu and Moira bring four each at 53 to 54 beside Lucas or Dawn, Moira's Snow Warning setting five turns of hail. | The scorer cannot read tag battles yet. | Nothing now. |

## What comes next

The bosses of the Galactic headquarters split (Cyrus 2 and Saturn 2), then
the rest in order, then the ordinary trainers from Maylene's split on.

## Overview

| Trainer | Place | Path | Battle | Size | Levels | The idea | Expected |
|---|---|---|---|---|---|---|---|
| Galactic Officer Hesperid | Lake Valor (drained) | on the path | single, named officer | 6 | 54 to 56 | Today's five without the dice | about 98 / 2.2 / 0 in my simulator, where today's file reads 100 / 0.0 / 99 |
| Saturn 1 | Valor Cavern | on the path | single, boss | 6 | 54 to 56 | A hazard lead and a trap | about 80 / 3.1 / 0 in my simulator, where today's file reads 94 / 0.9 / 56 |
| Galactic Officer Somnu | Lake Verity | on the path | tag, beside Lucas or Dawn | 4 | 53 to 54 | Somnu's sleep | not readable yet |
| Galactic Officer Moira | Lake Verity | on the path | tag, beside Lucas or Dawn | 4 | 53 to 54 | Moira's hail again | not readable yet |
| Mars 2 | Lake Verity | on the path | single, boss | 6 | 54 to 56 | Status from the lead again | about 91 / 2.5 / 1 in my simulator, where today's file reads 100 / 0.4 / 57 |
| Ace Trainer Blake | Route 216 | optional | single, Ace Trainer | 6 | 52 to 55 | Normal types | about 90 / 2.8 / 1 with a planned six |
| Ace Trainer Garrett | Route 216 | optional | single, Ace Trainer | 6 | 54 to 55 | Psychic | about 90 / 3.4 / 0 with a planned six |
| Ace Trainer Laura | Route 216 | on the path | single, Ace Trainer | 6 | 54 to 55 | Grass types | about 99 / 0.7 / 58 with a planned six |
| Ace Trainer Maria | Route 216 | optional | single, Ace Trainer | 6 | 54 to 55 | One of each element | about 100 / 0.8 / 32 with a planned six |
| Ace Trainer Dalton | Route 217 (hail) | on the path | single, Ace Trainer | 6 | 54 to 55 | The elemental pair in the hail | about 97 / 2.3 / 0 with a planned six in hail |
| Ace Trainer Olivia | Route 217 (hail) | on the path | single, Ace Trainer | 6 | 52 to 55 | Dragons and Ice | about 98 / 1.1 / 19 with a planned six in hail |
| Ace Trainer Sergio | Snowpoint Gym (hail) | gym trainer | single, Ace Trainer | 6 | 54 to 55 | Grass and Ice | about 100 / 0.8 / 46 with a planned six in hail |
| Ace Trainer Isaiah | Snowpoint Gym (hail) | gym trainer | single, Ace Trainer | 6 | 54 to 55 | Ground types with Ice moves | about 97 / 2.1 / 7 with a planned six in hail |
| Ace Trainer Savannah | Snowpoint Gym (hail) | gym trainer | single, Ace Trainer | 6 | 54 to 55 | Hail support | about 98 / 2.2 / 0 with a planned six in hail |
| Ace Trainer Alicia | Snowpoint Gym (hail) | gym trainer | single, Ace Trainer | 6 | 54 to 55 | Water and Ice | about 100 / 1.7 / 3 with a planned six in hail |
| Ace Trainer Anton | Snowpoint Gym (hail) | gym trainer | single, Ace Trainer | 6 | 54 to 55 | Today's Glalie leads with Spikes | about 99 / 2.2 / 1 with a planned six in hail |
| Ace Trainer Brenna | Snowpoint Gym (hail) | gym trainer | single, Ace Trainer | 6 | 54 to 55 | Today's Dewgong and Lapras with Froslass's Spikes and Thunder Wave | about 97 / 2.4 / 0 with a planned six in hail |
| Candice | Snowpoint Gym (hail) | on the path | single, boss | 6 | 54 to 56 | Hail and its abusers | about 90 / 3.8 / 0 in my simulator in hail, where today's file reads 94 / 4.0 / 0 |

Expected numbers are won / faints a fight / clean in my simulator, beside
today's file where it was read.

## The bosses

### Galactic Officer Hesperid: Lake Valor (drained), on the path, single, named officer, cap 56

Today's five without the dice: Sudowoodo leads with Stealth Rock behind a Focus Sash (its BrightPowder and second Explosion are gone), Weezing carries the fight's one trade, Girafarig passes Agility on a Starf Berry, Chatot loses its Choice Specs for Nasty Plot, a Tangrowth joins with Sleep Powder, and Sceptile is the Life Orb ace.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Sudowoodo | 54 | Focus Sash | Rock Head | Adamant | Stealth Rock, Stone Edge, Sucker Punch, Wood Hammer |
| Weezing | 55 | Black Sludge | Levitate | Bold | Sludge Bomb, Will-O-Wisp, Thunderbolt, Explosion |
| Girafarig | 55 | Starf Berry | Quick Feet | Timid | Agility, Baton Pass, Psychic, Thunderbolt |
| Chatot | 55 | Sharp Beak | Scrappy | Timid | Hyper Voice, Heat Wave, Chatter, Nasty Plot |
| Tangrowth | 55 | Leftovers | Regenerator | Relaxed | Seed Bomb, Earthquake, Knock Off, Sleep Powder |
| Sceptile | 56 | Life Orb | Overgrow | Naive | Leaf Storm, Focus Blast, Earthquake, Rock Slide |

Today's team: Weezing 50 (Black Sludge; Payback, Thunder, Explosion, Sludge Bomb), Sceptile 49 (Petaya Berry; Rock Slide, Pursuit, Leaf Storm, Aerial Ace), Girafarig 50 (Starf Berry; Earthquake, Agility, Baton Pass, Charge Beam), Sudowoodo 50 (BrightPowder; Stealth Rock, Explosion, Sucker Punch, Focus Punch), Chatot 52 (Choice Specs; Hyper Voice, Heat Wave, Chatter). Expected: about 98 / 2.2 / 0 in my simulator, where today's file reads 100 / 0.0 / 99.

### Saturn 1: Valor Cavern, on the path, single, boss, cap 56

A hazard lead and a trap, as the dial asks of Saturn: Azelf sets Stealth Rock and pivots out behind a Focus Sash, Mr. Mime's screens on a Light Clay, a Shadow Tag Wobbuffet with Counter (the trap and the fight's one trade), a Poison Heal Lickilicky, Rhyperior, and a Swords Dance Toxicroak at the cap.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Azelf | 54 | Focus Sash | Levitate | Timid | Stealth Rock, U-turn, Psychic, Fire Blast |
| Mr Mime | 55 | Light Clay | Filter | Timid | Reflect, Light Screen, Psychic, Thunderbolt |
| Wobbuffet | 55 | Leftovers | Shadow Tag | Bold | Counter, Encore, Safeguard, Charm |
| Lickilicky | 55 | Toxic Orb | Poison Heal | Adamant | Body Slam, Earthquake, Knock Off, Power Whip |
| Rhyperior | 55 | Passho Berry | Solid Rock | Adamant | Earthquake, Stone Edge, Hammer Arm, Ice Punch |
| Toxicroak | 56 | Lum Berry | Dry Skin | Adamant | Poison Jab, Cross Chop, Sucker Punch, Swords Dance |

Today's team: Mr Mime 52 (Light Clay; Light Screen, Reflect, Psychic, Thunderbolt), Lickilicky 52 (Toxic Orb; Toxic, Substitute, Slam, Shadow Ball), Slaking 52 (Sitrus Berry; Slash, Hammer Arm, Night Slash, Slack Off), Rhyperior 52 (Leftovers; Earthquake, Stone Edge, ThunderPunch, Superpower), Toxicroak 52 (Life Orb; Poison Jab, Cross Chop, ThunderPunch, Sucker Punch), Azelf 53 (Focus Sash; U-turn, Future Sight, Psychic, Payback). Expected: about 80 / 3.1 / 0 in my simulator, where today's file reads 94 / 0.9 / 56.

### Galactic Officer Somnu: Lake Verity, on the path, tag, beside Lucas or Dawn, cap 56

Somnu's sleep, then her trade: Swalot's Yawn and Dream Eater with Destiny Bond, Forretress's Toxic Spikes, Skuntank, and a Glaceon with Ice Body.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Swalot | 53 | Sitrus Berry | Gluttony | Calm | Sludge Bomb, Yawn, Dream Eater, Destiny Bond |
| Forretress | 53 | Leftovers | Heatproof | Relaxed | Toxic Spikes, Gyro Ball, Payback, Rapid Spin |
| Skuntank | 53 | Dread Plate | Aftermath | Adamant | Crunch, Poison Jab, Sucker Punch, Fire Blast |
| Glaceon | 54 | NeverMeltIce | Ice Body | Modest | Blizzard, Shadow Ball, Signal Beam, Toxic |

Today's team: Swalot 50 (Salac Berry; Destiny Bond, Smog, Endure, Explosion), Forretress 50 (Sitrus Berry; Toxic Spikes, Bug Bite, Protect, Double-Edge), Glaceon 52 (Shell Bell; Blizzard, Detect, Shadow Ball, Barrier). Expected: not readable yet.

### Galactic Officer Moira: Lake Verity, on the path, tag, beside Lucas or Dawn, cap 56

Moira's hail again: Abomasnow's Snow Warning and Blizzard, Slowking's Nasty Plot, Mamoswine's Ice Shard and a Magic Guard Gardevoir with a Life Orb and Hypnosis.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Abomasnow | 53 | Occa Berry | Snow Warning | Modest | Blizzard, Energy Ball, Ice Shard, Earthquake |
| Slowking | 53 | Leftovers | Regenerator | Modest | Surf, Psychic, Ice Beam, Nasty Plot |
| Mamoswine | 53 | Lum Berry | Thick Fat | Adamant | Earthquake, Ice Fang, Ice Shard, Stone Edge |
| Gardevoir | 54 | Life Orb | Magic Guard | Modest | Psychic, Thunderbolt, Focus Blast, Hypnosis |

Today's team: Abomasnow 50 (Occa Berry; Avalanche, Protect, Rock Slide, Wood Hammer), Slowking 50 (Leftovers; Nasty Plot, Future Sight, Icy Wind, Water Pulse), Gardevoir 52 (Life Orb; Hypnosis, Signal Beam, Psychic, Calm Mind). Expected: not readable yet.

### Mars 2: Lake Verity, on the path, single, boss, cap 56

Status from the lead again, now behind a hazard: Mesprit sets Stealth Rock and Thunder Wave behind a Focus Sash and pivots out, then Crobat, Bronzong (Hypnosis, and Explosion as the trade), Purugly's Fake Out, Umbreon's Toxic and Wish, and a Luxray ace with Howl.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Mesprit | 54 | Focus Sash | Magic Guard | Timid | Stealth Rock, U-turn, Psychic, Thunder Wave |
| Crobat | 55 | Sharp Beak | Inner Focus | Jolly | Brave Bird, Cross Poison, U-turn, Roost |
| Bronzong | 55 | Leftovers | Levitate | Relaxed | Gyro Ball, Earthquake, Hypnosis, Explosion |
| Purugly | 55 | Silk Scarf | Defiant | Jolly | Fake Out, Body Slam, Sucker Punch, Knock Off |
| Umbreon | 55 | Leftovers | Synchronize | Calm | Payback, Toxic, Wish, Protect |
| Luxray | 56 | Expert Belt | Tinted Lens | Adamant | Thunder Fang, Crunch, Superpower, Howl |

Today's team: Umbreon 53 (Leftovers; Protect, Payback, Heal Bell, Dig), Delcatty 53 (Chople Berry; Calm Mind, Baton Pass, Hyper Voice, Attract), Luxray 53 (Expert Belt; Thunder Fang, Crunch, Superpower, Ice Fang), Bronzong 53 (Iron Ball; Gyro Ball, Curse, Zen Headbutt, Confuse Ray), Purugly 53 (Sitrus Berry; Slash, Sucker Punch, Hypnosis, Fake Out), Mesprit 54 (Life Orb; Rest, Psychic, Sleep Talk, U-turn). Expected: about 91 / 2.5 / 1 in my simulator, where today's file reads 100 / 0.4 / 57.

### Ace Trainer Blake: Route 216, optional, single, Ace Trainer, cap 56

Normal types: Ambipom's Fake Out, an Eviolite Porygon2, Snorlax, Tauros, Kangaskhan and a Lickilicky ace.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Ambipom | 52 | Silk Scarf | Technician | Jolly | Fake Out, Double Hit, U-turn, Knock Off |
| Porygon2 | 52 | Eviolite | Download | Calm | Tri Attack, Ice Beam, Thunderbolt, Recover |
| Snorlax | 53 | Leftovers | Thick Fat | Careful | Body Slam, Earthquake, Crunch, Fire Punch |
| Tauros | 52 | Lum Berry | Intimidate | Jolly | Take Down, Earthquake, Stone Edge, Zen Headbutt |
| Kangaskhan | 53 | Sitrus Berry | Scrappy | Adamant | Double-Edge, Earthquake, Crunch, Ice Punch |
| Lickilicky | 55 | Leftovers | Poison Heal | Adamant | Body Slam, Earthquake, Ice Beam, Knock Off |

Today's team: Ambipom 48 (Double Hit, U-turn, Sand-Attack, Screech), Porygon2 48 (Psybeam, Signal Beam, Conversion 2, Recover). Expected: about 90 / 2.8 / 1 with a planned six; read blind, 31 / 5.2 / 0.

### Ace Trainer Garrett: Route 216, optional, single, Ace Trainer, cap 56

Psychic, Ghost and Steel: Mr. Mime's screens, Dusknoir's Will-O-Wisp, Alakazam, Honchkrow, Metagross and a Swords Dance Scizor ace.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Mr Mime | 54 | Leftovers | Filter | Timid | Reflect, Light Screen, Psychic, Thunderbolt |
| Dusknoir | 54 | Leftovers | Levitate | Adamant | Shadow Punch, Earthquake, Ice Punch, Will-O-Wisp |
| Alakazam | 54 | TwistedSpoon | Magic Guard | Timid | Psychic, Focus Blast, Shadow Ball, Energy Ball |
| Honchkrow | 54 | Sharp Beak | Super Luck | Adamant | Drill Peck, Night Slash, Sucker Punch, Heat Wave |
| Metagross | 54 | Shuca Berry | Clear Body | Adamant | Meteor Mash, Earthquake, Zen Headbutt, Ice Punch |
| Scizor | 55 | Metal Coat | Technician | Adamant | Bullet Punch, X-Scissor, U-turn, Swords Dance |

Today's team: Mr Mime 47 (Psychic, Thunderbolt, Reflect, Light Screen), Dusknoir 47 (Will-O-Wisp, Shadow Punch, Pursuit, Confuse Ray), Scizor 47 (Slash, X-Scissor, Bullet Punch, Night Slash). Expected: about 90 / 3.4 / 0 with a planned six; read blind, 14 / 5.6 / 0.

### Ace Trainer Laura: Route 216, on the path, single, Ace Trainer, cap 56

Grass types: Roserade leads with Spikes behind a Focus Sash, then Tropius, a Poison Heal Breloom with Spore, Tangrowth, a Swords Dance Leafeon and a Venusaur ace.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Roserade | 54 | Focus Sash | Natural Cure | Timid | Spikes, Sludge Bomb, Energy Ball, Shadow Ball |
| Tropius | 54 | Leftovers | Overgrow | Modest | Air Slash, Energy Ball, Roost, Earthquake |
| Breloom | 54 | Toxic Orb | Poison Heal | Jolly | Seed Bomb, Mach Punch, Stone Edge, Spore |
| Tangrowth | 54 | Sitrus Berry | Regenerator | Relaxed | Seed Bomb, Earthquake, Knock Off, Rock Slide |
| Leafeon | 54 | Miracle Seed | Chlorophyll | Jolly | Seed Bomb, X-Scissor, Quick Attack, Swords Dance |
| Venusaur | 55 | Black Sludge | Overgrow | Modest | Sludge Bomb, Energy Ball, Earthquake, Synthesis |

Today's team: Tropius 50 (Air Slash, Leaf Storm, Ominous Wind, Tailwind). Expected: about 99 / 0.7 / 58 with a planned six; read blind, 47 / 4.1 / 4.

### Ace Trainer Maria: Route 216, optional, single, Ace Trainer, cap 56

One of each element: Golduck's Calm Mind, Jolteon, Sudowoodo, Exeggutor's Sleep Powder, Arcanine's ExtremeSpeed and a Life Orb Rapidash ace.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Golduck | 54 | Mystic Water | Swift Swim | Modest | Surf, Ice Beam, Psychic, Calm Mind |
| Jolteon | 54 | Magnet | Volt Absorb | Timid | Thunderbolt, Shadow Ball, Signal Beam, Thunder Wave |
| Sudowoodo | 54 | Hard Stone | Rock Head | Adamant | Stone Edge, Wood Hammer, Sucker Punch, Earthquake |
| Exeggutor | 54 | Sitrus Berry | Chlorophyll | Modest | Psychic, Energy Ball, Leech Seed, Sleep Powder |
| Arcanine | 54 | Charcoal | Intimidate | Adamant | Flare Blitz, ExtremeSpeed, Crunch, Thunder Fang |
| Rapidash | 55 | Life Orb | Reckless | Jolly | Flare Blitz, Megahorn, Poison Jab, Bounce |

Today's team: Golduck 47 (Cross Chop, Ice Punch, Aqua Jet, Confuse Ray), Rapidash 47 (Fire Blast, Bounce, Poison Jab, Will-O-Wisp), Sudowoodo 47 (Stone Edge, Low Kick, Wood Hammer, ThunderPunch). Expected: about 100 / 0.8 / 32 with a planned six; read blind, 72 / 3.7 / 3.

### Ace Trainer Dalton: Route 217 (hail), on the path, single, Ace Trainer, cap 56

The elemental pair in the hail: Glalie, Magmortar's Will-O-Wisp, Abomasnow's Blizzard (sure to hit in hail), Weavile, Dewgong and an Electivire ace.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Glalie | 54 | Leftovers | Ice Body | Jolly | Ice Shard, Crunch, Earthquake, Ice Fang |
| Magmortar | 54 | Charcoal | Flame Body | Modest | Flamethrower, Thunderbolt, Focus Blast, Will-O-Wisp |
| Abomasnow | 54 | NeverMeltIce | Adaptability | Modest | Blizzard, Energy Ball, Ice Shard, Earthquake |
| Weavile | 54 | NeverMeltIce | Technician | Jolly | Ice Shard, Night Slash, Ice Punch, Brick Break |
| Dewgong | 54 | Leftovers | Ice Body | Calm | Blizzard, Surf, Aqua Jet, Toxic |
| Electivire | 55 | Magnet | Vital Spirit | Adamant | ThunderPunch, Ice Punch, Cross Chop, Earthquake |

Today's team: Electivire 52 (ThunderPunch, Earthquake, Ice Punch, Thunder Wave), Magmortar 52 (Flamethrower, Psychic, Thunderbolt, Will-O-Wisp). Expected: about 97 / 2.3 / 0 with a planned six in hail; read blind, 43 / 4.8 / 0.

### Ace Trainer Olivia: Route 217 (hail), on the path, single, Ace Trainer, cap 56

Dragons and Ice: Lapras, Glaceon's Ice Body and Yawn, Ursaring, Kingdra, an Eviolite Dragonair, and a Dragon Dance Altaria ace.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Lapras | 53 | Leftovers | Shell Armor | Modest | Blizzard, Surf, Thunderbolt, Ice Shard |
| Glaceon | 52 | NeverMeltIce | Ice Body | Modest | Blizzard, Shadow Ball, Signal Beam, Yawn |
| Ursaring | 52 | Sitrus Berry | Guts | Adamant | Take Down, Close Combat, Crunch, Earthquake |
| Kingdra | 53 | Mystic Water | Sniper | Modest | Surf, Dragon Pulse, Ice Beam, Signal Beam |
| Altaria | 55 | Sitrus Berry | Serene Grace | Adamant | Dragon Claw, Earthquake, Roost, Agility |
| Dragonair | 52 | Eviolite | Shed Skin | Adamant | Dragon Rush, Aqua Tail, Thunder Wave, Iron Tail |

Today's team: Altaria 52 (Dragon Dance, Outrage, Earthquake, Roost), Lapras 52 (Dragon Dance, Waterfall, Outrage, Rest), Ursaring 52 (Slash, Swords Dance, Stone Edge, Close Combat). Expected: about 98 / 1.1 / 19 with a planned six in hail; read blind, 46 / 4.6 / 0.

### Ace Trainer Sergio: Snowpoint Gym (hail), gym trainer, single, Ace Trainer, cap 56

Grass and Ice: Cloyster's Spikes, Jynx's Lovely Kiss, Ludicolo's Fake Out, a Quiver Dance Frosmoth, Roserade and an Abomasnow ace with Adaptability Blizzard.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Jynx | 54 | Sitrus Berry | Dry Skin | Timid | Blizzard, Psychic, Lovely Kiss, Focus Blast |
| Ludicolo | 54 | Leftovers | Swift Swim | Modest | Surf, Giga Drain, Ice Beam, Fake Out |
| Frosmoth | 54 | NeverMeltIce | Ice Scales | Modest | Blizzard, Bug Buzz, Icy Wind, Quiver Dance |
| Roserade | 54 | Life Orb | Natural Cure | Timid | Sludge Bomb, Energy Ball, Shadow Ball, Extrasensory |
| Cloyster | 54 | Focus Sash | Skill Link | Jolly | Icicle Spear, Ice Shard, Poison Jab, Spikes |
| Abomasnow | 55 | Occa Berry | Adaptability | Adamant | Blizzard, Wood Hammer, Ice Shard, Earthquake |

Today's team: Abomasnow 54 (Ice Punch, Wood Hammer, Headbutt, Leech Seed). Expected: about 100 / 0.8 / 46 with a planned six in hail; read blind, 71 / 4.0 / 0.

### Ace Trainer Isaiah: Snowpoint Gym (hail), gym trainer, single, Ace Trainer, cap 56

Ground types with Ice moves: Whiscash, Quagsire's Yawn, Swampert, Gastrodon, Steelix and a Mamoswine ace.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Whiscash | 54 | Leftovers | Swift Swim | Adamant | Earthquake, Waterfall, Stone Edge, Zen Headbutt |
| Quagsire | 54 | Leftovers | Unaware | Relaxed | Earthquake, Ice Beam, Waterfall, Yawn |
| Swampert | 54 | Rindo Berry | Torrent | Adamant | Earthquake, Waterfall, Ice Punch, Stone Edge |
| Gastrodon | 54 | Sitrus Berry | Dry Skin | Modest | Earth Power, Surf, Ice Beam, Sludge Bomb |
| Steelix | 54 | Passho Berry | Rock Head | Adamant | Earthquake, Iron Head, Ice Fang, Stone Edge |
| Mamoswine | 55 | Lum Berry | Thick Fat | Adamant | Earthquake, Ice Fang, Stone Edge, Superpower |

Today's team: Piloswine 55 (Earthquake, Bite, Ice Fang, Stone Edge). Expected: about 97 / 2.1 / 7 with a planned six in hail; read blind, 7 / 5.9 / 0.

### Ace Trainer Savannah: Snowpoint Gym (hail), gym trainer, single, Ace Trainer, cap 56

Hail support: Froslass's Spikes behind a Focus Sash, Mr. Rime's Reflect, an Adaptability Delibird, Starmie, Jynx with Dry Skin in place of Snow Cloak, and a Glaceon ace.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Froslass | 54 | Focus Sash | Cursed Body | Timid | Spikes, Blizzard, Shadow Ball, Thunderbolt |
| Mr Rime | 54 | Leftovers | Ice Body | Modest | Freeze-Dry, Psychic, Dazzling Gleam, Reflect |
| Delibird | 54 | NeverMeltIce | Adaptability | Jolly | Ice Shard, Ice Punch, Brick Break, Seed Bomb |
| Starmie | 54 | Mystic Water | Magic Guard | Timid | Surf, Ice Beam, Thunderbolt, Psychic |
| Jynx | 54 | TwistedSpoon | Dry Skin | Modest | Blizzard, Psychic, Shadow Ball, Focus Blast |
| Glaceon | 55 | Leftovers | Ice Body | Modest | Blizzard, Shadow Ball, Signal Beam, Wish |

Today's team: Delibird 54 (Present, Blizzard, Hail, Water Pulse), Jynx 54 (Blizzard, Psychic, Shadow Ball, Protect). Expected: about 98 / 2.2 / 0 with a planned six in hail; read blind, 19 / 5.5 / 0.

### Ace Trainer Alicia: Snowpoint Gym (hail), gym trainer, single, Ace Trainer, cap 56

Water and Ice: a Skill Link Cloyster with Spikes, Dewgong, Kingdra, Gyarados, Lapras and a Walrein ace.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Cloyster | 54 | Leftovers | Skill Link | Jolly | Icicle Spear, Ice Shard, Poison Jab, Spikes |
| Dewgong | 54 | Leftovers | Ice Body | Calm | Blizzard, Surf, Encore, Toxic |
| Kingdra | 54 | Mystic Water | Sniper | Modest | Surf, Dragon Pulse, Ice Beam, Signal Beam |
| Gyarados | 54 | Wacan Berry | Intimidate | Adamant | Waterfall, Ice Fang, Earthquake, Stone Edge |
| Lapras | 54 | Sitrus Berry | Shell Armor | Modest | Blizzard, Surf, Thunderbolt, Psychic |
| Walrein | 55 | Sitrus Berry | Ice Body | Modest | Blizzard, Surf, Body Slam, Toxic |

Today's team: Cloyster 54 (Surf, Ice Beam, Signal Beam, Toxic Spikes), Sealeo 55 (Sheer Cold). Expected: about 100 / 1.7 / 3 with a planned six in hail; read blind, 23 / 5.5 / 0.

### Ace Trainer Anton: Snowpoint Gym (hail), gym trainer, single, Ace Trainer, cap 56

Today's Glalie leads with Spikes, then Golem, Weavile, Lucario, Gliscor and an Eviolite Piloswine ace.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Glalie | 54 | Leftovers | Ice Body | Jolly | Spikes, Ice Shard, Crunch, Earthquake |
| Golem | 54 | Hard Stone | Shell Armor | Adamant | Stone Edge, Earthquake, Sucker Punch, Fire Punch |
| Weavile | 54 | NeverMeltIce | Technician | Jolly | Ice Shard, Night Slash, Ice Punch, Brick Break |
| Lucario | 54 | Black Belt | Iron Fist | Adamant | Close Combat, Crunch, Ice Punch, Stone Edge |
| Gliscor | 54 | Sitrus Berry | Sand Veil | Jolly | Earthquake, U-turn, Ice Fang, Stone Edge |
| Piloswine | 55 | Eviolite | Thick Fat | Adamant | Earthquake, Ice Fang, Stone Edge, Amnesia |

Today's team: Glalie 54 (Ice Shard, Crunch, Iron Head). Expected: about 99 / 2.2 / 1 with a planned six in hail; read blind, 37 / 5.0 / 0.

### Ace Trainer Brenna: Snowpoint Gym (hail), gym trainer, single, Ace Trainer, cap 56

Today's Dewgong and Lapras with Froslass's Spikes and Thunder Wave, Mr. Rime's Light Screen, a Skill Link Cloyster and a Walrein ace with Roar.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Dewgong | 54 | Leftovers | Ice Body | Calm | Blizzard, Surf, Aqua Jet, Toxic |
| Lapras | 54 | Sitrus Berry | Shell Armor | Modest | Blizzard, Surf, Thunderbolt, Psychic |
| Froslass | 54 | Focus Sash | Cursed Body | Timid | Spikes, Blizzard, Shadow Ball, Thunder Wave |
| Mr Rime | 54 | Leftovers | Ice Body | Modest | Freeze-Dry, Psychic, Dazzling Gleam, Light Screen |
| Cloyster | 54 | NeverMeltIce | Skill Link | Jolly | Icicle Spear, Ice Shard, Poison Jab, Surf |
| Walrein | 55 | Leftovers | Ice Body | Modest | Blizzard, Surf, Roar, Toxic |

Today's team: Dewgong 54 (Stockpile, Swallow, Spit Up, Perish Song), Lapras 54 (Surf, Ice Beam, Psychic, Thunderbolt). Expected: about 97 / 2.4 / 0 with a planned six in hail; read blind, 14 / 5.7 / 0.

### Candice: Snowpoint Gym (hail), on the path, single, boss, cap 56

Hail and its abusers, and phazing: Froslass leads with Spikes behind a Focus Sash, Walrein heals in hail with Ice Body and phazes with Roar, then an Ice Body Glaceon, Mamoswine, Articuno as the legendary, and an Adaptability Abomasnow ace with Swords Dance. Every Blizzard is sure to hit in the gym's hail, and no member holds Snow Cloak.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Froslass | 54 | Focus Sash | Cursed Body | Timid | Spikes, Blizzard, Shadow Ball, Thunder Wave |
| Walrein | 55 | Leftovers | Ice Body | Bold | Blizzard, Surf, Roar, Toxic |
| Glaceon | 55 | NeverMeltIce | Ice Body | Modest | Blizzard, Shadow Ball, Signal Beam, Wish |
| Mamoswine | 55 | Lum Berry | Thick Fat | Adamant | Earthquake, Ice Fang, Ice Shard, Stone Edge |
| Articuno | 55 | Charti Berry | Pressure | Modest | Blizzard, AncientPower, Roost, U-turn |
| Abomasnow | 56 | Occa Berry | Adaptability | Adamant | Blizzard, Wood Hammer, Earthquake, Swords Dance |

Today's team: Walrein 55 (Leftovers; Blizzard, Surf, Rest, Toxic), Mamoswine 55 (Lum Berry; Ice Fang, Stone Edge, Earthquake, Iron Head), Castform 55 (Life Orb; Flamethrower, Thunderbolt, Blizzard, Energy Ball), Articuno 55 (Charti Berry; AncientPower, Extrasensory, Roost, Blizzard), Glaceon 55 (Chople Berry; Blizzard, Yawn, Double Team, Baton Pass), Froslass 56 (Focus Sash; Blizzard, Destiny Bond, Shadow Ball, Psychic). Expected: about 90 / 3.8 / 0 in my simulator in hail, where today's file reads 94 / 4.0 / 0.


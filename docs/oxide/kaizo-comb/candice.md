# The comb: Candice's split

**Every trainer of Candice's split is now combed.** The bosses and twelve Ace
Trainers were combed earlier. On 2026-10-07 the 16 ordinary trainers were
added in walking order: the four Galactic grunts at the lakes, five trainers
on Route 216 and seven on Route 217. Every file passes the checker and the
rule audit.

The ordinary trainers follow Ian's ruling of 2026-10-07. Each takes Kaizo's
idea where Kaizo has the trainer, moves it into Oxide's Generation 5+ pool
where the species' lists allow, then scales it to the dial. Kaizo's
level-84 to 98 jokes and its barred tools (Endeavor, Shadow Tag, Snow Cloak
evasion, one-hit KO moves) are gone.

| Check | Result |
|---|---|
| Single battles read blind (16) | 94 to 99 won, mean 97.2 |
| Clean, in the scorer's terms (Ian's band 80 to 85) | 65 to 77, mean 71 |
| Faints a fight, in the scorer's terms (Ian's band 0.1 to 0.25) | 0.6 to 1.0, mean 0.74 |
| Move slots that are Generation 5+ | 37 of 256, 14 percent |
| Hidden abilities | 18, on 13 of 16 teams |
| Element 7 items held | 5: three Eviolites and two Rocky Helmets |

Every team carries at least one modern move. The ordinary trainers win as
often as Ian asks but cost about three times his band in faints, more than
Maylene's. Four rounds of softening brought the faints down from about 2.2 to
1.2 in my simulator. Most members now sit at 51 to 52, and only a weak or
supporting member stands at 54. The rest of the gap is the box at 56, which
knows no TMs and meets these Pokemon with level-up moves alone. Grunt Lake
Valor 3 holds the Metronome it awards, and Skier Lexie's Glalie holds her
Ability Shield.

Route 217's hail is used by three of its seven trainers, as the dial's half
allows: Shawn (Blizzard, and Alolan Ninetales's Aurora Veil), Lexie (Ice
Body) and Madison (Castform's Weather Ball). My simulator does not model
Aurora Veil or Castform's change of type, so those two teams play harder than
they read. Lake Verity's grunts preview Candice's Spikes and Toxic Spikes, and
Black Belt Luke previews her phazing, each alone, on the path before her.

## The bosses and Ace Trainers, combed earlier

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
files pass the checker and the rule audit.

The cap is 56 throughout. Route 217 and Snowpoint's gym fight in permanent
hail (Ian, 2026-10-06), so Blizzard never misses there, Ice types take no
chip, and Ice Body heals; no team on those maps holds Snow Cloak, which the
evasion rule would count. Route 216, Snowpoint City and Acuity Lakefront have
changing weather and are read without it; the lakes have none. My simulator
reads the bosses against the scorer's box at Candice, which knows no TMs, so
they read harsher than they will once the TM pass lands. It now also models
trapping abilities, Counter, Mirror Coat and Destiny Bond. Saturn and Mars
now sit three under the cap, their aces at 53 (Ian, 2026-10-07: three under
the cap), and read about 97 won and 99.5 won to today's 94 and 100 (80 and 91
at the cap, read before my simulator's patch of 2026-10-07, so the change is
partly the patch's). Hesperid reads about
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
| 4 | Lake Verity tag | Somnu and Moira bring four each at 53 to 54 beside Lucas or Dawn, Moira's Snow Warning setting hail for the whole fight. | The scorer cannot read tag battles yet. | Nothing now. |
| 5 | Ordinary trainers past the band | They win 94 to 99 percent blind, but cost about 0.74 Pokemon a fight in the scorer's terms against Ian's 0.1 to 0.25. | The scorer's step 15 reading, with a box that knows TMs. | Accept for now (recommended: the box without TMs overstates them, and the scorer's numbers decide), or soften them further now. |

## What comes next

The ordinary trainers of the Galactic headquarters split.

## Overview

| Trainer | Place | Path | Battle | Size | Levels | The idea | Expected |
|---|---|---|---|---|---|---|---|
| Galactic Grunt (Valor, 1) | Lake Valor (drained) | optional | single | 4 | 51 to 54 | Poison that lingers | 96 / 1.32 / 29 blind in my simulator, about 72 clean in the scorer's terms |
| Galactic Grunt (Valor, 3) | Lake Valor (drained) | optional | single | 4 | 52 to 54 | Glare and fangs | 94 / 1.10 / 42 blind in my simulator, about 77 clean in the scorer's terms |
| Galactic Officer Hesperid | Lake Valor (drained) | on the path | single, named officer | 6 | 54 to 56 | Today's five without the dice | about 98 / 2.2 / 0 in my simulator, where today's file reads 100 / 0.0 / 99 |
| Saturn 1 | Valor Cavern | on the path | single, boss | 6 | 51 to 53 | A hazard lead and a trap | about 97 / 1.0 / 35 in my simulator, where today's file reads 94 / 0.9 / 56 |
| Galactic Grunt (Verity, 1) | Lake Verity | on the path | single | 4 | 51 to 54 | Toxic Spikes from Drapion | 98 / 1.10 / 36 blind in my simulator, about 74 clean in the scorer's terms |
| Galactic Grunt (Verity, 2) | Lake Verity | on the path | single | 4 | 52 to 54 | Spikes from Cacturne previewing Candice's alone | 94 / 1.11 / 43 blind in my simulator, about 77 clean in the scorer's terms |
| Galactic Officer Somnu | Lake Verity | on the path | tag, beside Lucas or Dawn | 4 | 53 to 54 | Somnu's sleep | not readable yet |
| Galactic Officer Moira | Lake Verity | on the path | tag, beside Lucas or Dawn | 4 | 53 to 54 | Moira's hail again | not readable yet |
| Mars 2 | Lake Verity | on the path | single, boss | 6 | 51 to 53 | Status from the lead again | about 100 / 0.2 / 82 in my simulator, where today's file reads 100 / 0.4 / 57 |
| Ace Trainer Blake | Route 216 | optional | single, Ace Trainer | 6 | 52 to 55 | Normal types | about 90 / 2.8 / 1 with a planned six |
| Ace Trainer Garrett | Route 216 | optional | single, Ace Trainer | 6 | 54 to 55 | Psychic | about 90 / 3.4 / 0 with a planned six |
| Skier Bradley | Route 216 | optional | single | 4 | 51 to 54 | The Ice lines grown up | 99 / 1.11 / 23 blind in my simulator, about 69 clean in the scorer's terms |
| Skier Edward | Route 216 | optional | single | 4 | 51 to 54 | Stealth Rock from an Eviolite Piloswine | 97 / 1.01 / 38 blind in my simulator, about 75 clean in the scorer's terms |
| Ace Trainer Laura | Route 216 | on the path | single, Ace Trainer | 6 | 54 to 55 | Grass types | about 99 / 0.7 / 58 with a planned six |
| Skier Kaitlyn | Route 216 | optional | single | 4 | 53 to 54 | A Toxic Boost Zangoose on a Toxic Orb behind Delibird's Sash and Drill Run | 98 / 1.22 / 24 blind in my simulator, about 70 clean in the scorer's terms |
| Skier Andrea | Route 216 | optional | single | 4 | 51 to 54 | Burn then Hex from a Cursed Body Froslass | 98 / 0.95 / 36 blind in my simulator, about 74 clean in the scorer's terms |
| Ace Trainer Maria | Route 216 | optional | single, Ace Trainer | 6 | 54 to 55 | One of each element | about 100 / 0.8 / 32 with a planned six |
| Black Belt Philip | Route 216 | optional | single | 4 | 51 to 54 | A Protean Kecleon's Fake Out beside Hitmonlee's Scope Lens | 96 / 1.24 / 31 blind in my simulator, about 72 clean in the scorer's terms |
| Skier Shawn | Route 217 (hail) | optional | single | 4 | 51 to 54 | The hail | 96 / 1.66 / 17 blind in my simulator in hail, about 67 clean in the scorer's terms |
| Ace Trainer Dalton | Route 217 (hail) | on the path | single, Ace Trainer | 6 | 54 to 55 | The elemental pair in the hail | about 97 / 2.3 / 0 with a planned six in hail |
| Skier Bjorn | Route 217 (hail) | optional | single | 4 | 51 to 54 | Grass against the ice | 97 / 1.48 / 16 blind in my simulator in hail, about 66 clean in the scorer's terms |
| Skier Lexie | Route 217 (hail) | optional | single | 4 | 51 to 54 | Ice Body in the hail | 97 / 1.25 / 22 blind in my simulator in hail, about 69 clean in the scorer's terms |
| Ace Trainer Olivia | Route 217 (hail) | on the path | single, Ace Trainer | 6 | 52 to 55 | Dragons and Ice | about 98 / 1.1 / 19 with a planned six in hail |
| Skier Madison | Route 217 (hail) | optional | single | 4 | 51 to 54 | Weather Ball | 99 / 1.03 / 32 blind in my simulator in hail, about 73 clean in the scorer's terms |
| Ninja Boy Matthew | Route 217 (hail) | optional | single | 4 | 51 to 54 | Tricks | 96 / 1.67 / 13 blind in my simulator in hail, about 65 clean in the scorer's terms |
| Ninja Boy Ethan | Route 217 (hail) | optional | single | 4 | 51 to 54 | Speed Boost Ninjask behind Weezing's Will-O-Wisp | 99 / 1.26 / 24 blind in my simulator in hail, about 70 clean in the scorer's terms |
| Black Belt Luke | Route 217 (hail) | on the path | single | 4 | 51 to 54 | Fighting types with Hariyama's Whirlwind previewing Candice's phazing alone | 99 / 1.29 / 18 blind in my simulator in hail, about 67 clean in the scorer's terms |
| Ace Trainer Sergio | Snowpoint Gym (hail) | gym trainer | single, Ace Trainer | 6 | 54 to 55 | Grass and Ice | about 100 / 0.8 / 46 with a planned six in hail |
| Ace Trainer Isaiah | Snowpoint Gym (hail) | gym trainer | single, Ace Trainer | 6 | 54 to 55 | Ground types with Ice moves | about 97 / 2.1 / 7 with a planned six in hail |
| Ace Trainer Savannah | Snowpoint Gym (hail) | gym trainer | single, Ace Trainer | 6 | 54 to 55 | Hail support | about 98 / 2.2 / 0 with a planned six in hail |
| Ace Trainer Alicia | Snowpoint Gym (hail) | gym trainer | single, Ace Trainer | 6 | 54 to 55 | Water and Ice | about 100 / 1.7 / 3 with a planned six in hail |
| Ace Trainer Anton | Snowpoint Gym (hail) | gym trainer | single, Ace Trainer | 6 | 54 to 55 | Today's Glalie leads with Spikes | about 99 / 2.2 / 1 with a planned six in hail |
| Ace Trainer Brenna | Snowpoint Gym (hail) | gym trainer | single, Ace Trainer | 6 | 54 to 55 | Today's Dewgong and Lapras with Froslass's Spikes and Thunder Wave | about 97 / 2.4 / 0 with a planned six in hail |
| Candice | Snowpoint Gym (hail) | on the path | single, boss | 6 | 54 to 56 | Hail and its abusers | about 90 / 3.8 / 0 in my simulator in hail, where today's file reads 94 / 4.0 / 0 |

Expected numbers are won / faints a fight / clean in my simulator, beside
today's file where it was read. For an ordinary trainer the clean rate is also
given in the scorer's terms, by the calibration in `read_split.py`.

## The trainers

### Galactic Grunt (Valor, 1): Lake Valor (drained), optional, single, cap 56

Poison that lingers: Seviper's Glare, Weezing's Sludge Wave and Will-O-Wisp, Toxicroak, and a Poison Touch Muk on a Rocky Helmet. Today's Muk leads the idea; Kaizo has no team here.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Seviper | 52 | Sitrus Berry | Shed Skin | default | Poison Tail, Crunch, Glare, Sucker Punch |
| Weezing | 54 | Black Sludge | Levitate | default | Sludge Wave, Will-O-Wisp, Pain Split, Thunderbolt |
| Toxicroak | 51 | Leftovers | Dry Skin | default | Drain Punch, Poison Jab, Sucker Punch, Bullet Punch |
| Muk | 52 | Rocky Helmet | Poison Touch | default | Poison Jab, Shadow Sneak, Drain Punch, Curse |

Today's team: Muk 50 (Gunk Shot, Ice Punch, Shadow Punch, Shadow Sneak). Expected: 96 / 1.32 / 29 blind in my simulator, about 72 clean in the scorer's terms.

### Galactic Grunt (Valor, 3): Lake Valor (drained), optional, single, cap 56

Glare and fangs: Arbok's paralysis on the Metronome it awards, Crobat, Skuntank's Throat Chop and Drapion's Night Slash.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Crobat | 52 | Sitrus Berry | Inner Focus | default | Cross Poison, Leech Life, Air Slash, Confuse Ray |
| Skuntank | 53 | Leftovers | Aftermath | default | Throat Chop, Poison Jab, Sucker Punch, Play Rough |
| Arbok | 54 | Metronome | Intimidate | default | Poison Fang, Glare, Crunch, Ice Fang |
| Drapion | 54 | none | Hyper Cutter | default | Cross Poison, Night Slash, Ice Fang, Knock Off |

Today's team: Arbok 50 (Gunk Shot, Seed Bomb, Ice Fang, Glare). Expected: 94 / 1.10 / 42 blind in my simulator, about 77 clean in the scorer's terms.

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
| Azelf | 51 | Focus Sash | Levitate | Timid | Stealth Rock, U-turn, Psychic, Fire Blast |
| Mr Mime | 52 | Light Clay | Filter | Timid | Reflect, Light Screen, Psychic, Thunderbolt |
| Wobbuffet | 52 | Leftovers | Shadow Tag | Bold | Counter, Encore, Safeguard, Charm |
| Lickilicky | 52 | Toxic Orb | Poison Heal | Adamant | Body Slam, Earthquake, Knock Off, Power Whip |
| Rhyperior | 52 | Passho Berry | Solid Rock | Adamant | Earthquake, Stone Edge, Hammer Arm, Ice Punch |
| Toxicroak | 53 | Lum Berry | Dry Skin | Adamant | Poison Jab, Cross Chop, Sucker Punch, Swords Dance |

Today's team: Mr Mime 52 (Light Clay; Light Screen, Reflect, Psychic, Thunderbolt), Lickilicky 52 (Toxic Orb; Toxic, Substitute, Slam, Shadow Ball), Slaking 52 (Sitrus Berry; Slash, Hammer Arm, Night Slash, Slack Off), Rhyperior 52 (Leftovers; Earthquake, Stone Edge, ThunderPunch, Superpower), Toxicroak 52 (Life Orb; Poison Jab, Cross Chop, ThunderPunch, Sucker Punch), Azelf 53 (Focus Sash; U-turn, Future Sight, Psychic, Payback). Expected: about 97 / 1.0 / 35 in my simulator, where today's file reads 94 / 0.9 / 56.

### Galactic Grunt (Verity, 1): Lake Verity, on the path, single, cap 56

Toxic Spikes from Drapion, then Nidoking's coverage, Crobat's Dual Wingbeat and Skuntank's Throat Chop. Kaizo has no team here; today's Nidoking leads the idea.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Crobat | 52 | Sitrus Berry | Inner Focus | default | Cross Poison, Dual Wingbeat, U-turn, Confuse Ray |
| Skuntank | 51 | Black Sludge | Aftermath | default | Throat Chop, Poison Jab, Sucker Punch, Flamethrower |
| Nidoking | 52 | Sitrus Berry | Mold Breaker | default | Earth Power, Sludge Bomb, Ice Beam, Thunderbolt |
| Drapion | 54 | Leftovers | Hyper Cutter | default | Toxic Spikes, Knock Off, Cross Poison, Ice Fang |

Today's team: Nidoking 50 (Surf, Sludge Bomb, Thunderbolt, Earth Power). Expected: 98 / 1.10 / 36 blind in my simulator, about 74 clean in the scorer's terms.

### Galactic Grunt (Verity, 2): Lake Verity, on the path, single, cap 56

Spikes from Cacturne previewing Candice's alone, then Dark types: Mightyena's Throat Chop, Honchkrow and a Charcoal Houndoom with Will-O-Wisp.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Cacturne | 52 | Leftovers | Water Absorb | default | Spikes, Needle Arm, Sucker Punch, Drain Punch |
| Mightyena | 52 | Sitrus Berry | Intimidate | default | Throat Chop, Play Rough, Sucker Punch, Ice Fang |
| Honchkrow | 52 | none | Super Luck | default | Drill Peck, Night Slash, Sucker Punch, U-turn |
| Houndoom | 54 | Charcoal | Flash Fire | default | Flamethrower, Dark Pulse, Sludge Bomb, Will-O-Wisp |

Today's team: Houndoom 50 (Flamethrower, Dark Pulse, Shadow Ball, Will-O-Wisp). Expected: 94 / 1.11 / 43 blind in my simulator, about 77 clean in the scorer's terms.

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
| Mesprit | 51 | Focus Sash | Magic Guard | Timid | Stealth Rock, U-turn, Psychic, Thunder Wave |
| Crobat | 52 | Sharp Beak | Inner Focus | Jolly | Brave Bird, Cross Poison, U-turn, Roost |
| Bronzong | 52 | Leftovers | Levitate | Relaxed | Gyro Ball, Earthquake, Hypnosis, Explosion |
| Purugly | 52 | Silk Scarf | Defiant | Jolly | Fake Out, Body Slam, Sucker Punch, Knock Off |
| Umbreon | 52 | Leftovers | Synchronize | Calm | Payback, Toxic, Wish, Protect |
| Luxray | 53 | Expert Belt | Tinted Lens | Adamant | Thunder Fang, Crunch, Superpower, Howl |

Today's team: Umbreon 53 (Leftovers; Protect, Payback, Heal Bell, Dig), Delcatty 53 (Chople Berry; Calm Mind, Baton Pass, Hyper Voice, Attract), Luxray 53 (Expert Belt; Thunder Fang, Crunch, Superpower, Ice Fang), Bronzong 53 (Iron Ball; Gyro Ball, Curse, Zen Headbutt, Confuse Ray), Purugly 53 (Sitrus Berry; Slash, Sucker Punch, Hypnosis, Fake Out), Mesprit 54 (Life Orb; Rest, Psychic, Sleep Talk, U-turn). Expected: about 100 / 0.2 / 82 in my simulator, where today's file reads 100 / 0.4 / 57.

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

### Skier Bradley: Route 216, optional, single, cap 56

The Ice lines grown up: Glalie's Icicle Crash, Weavile's Triple Axel, Abomasnow and Piloswine. Kaizo's level-98 joke of Snow Cloak babies is gone.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Glalie | 54 | Leftovers | Ice Body | default | Icicle Crash, Crunch, Ice Shard, Taunt |
| Weavile | 52 | NeverMeltIce | Inner Focus | default | Triple Axel, Night Slash, Ice Shard, Brick Break |
| Abomasnow | 51 | Sitrus Berry | Soundproof | default | Wood Hammer, Ice Punch, Ice Shard, StompingTantrum |
| Piloswine | 51 | Sitrus Berry | Thick Fat | default | Earthquake, Ice Fang, Ice Shard, Rock Slide |

Today's team: Furret 54 (Sucker Punch, Amnesia, Baton Pass, Me First), Stantler 54 (Zen Headbutt, Imprison, Captivate, Me First), Linoone 54 (Covet, Slash, Rest, Belly Drum). Expected: 99 / 1.11 / 23 blind in my simulator, about 69 clean in the scorer's terms.

### Skier Edward: Route 216, optional, single, cap 56

Stealth Rock from an Eviolite Piloswine, then Fearow, Stantler's Wild Charge and Girafarig's Dazzling Gleam. Kaizo's Piloswine lead without its Endeavor and Sash.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Girafarig | 51 | none | Sap Sipper | default | Psychic, Dazzling Gleam, Shadow Ball, Thunderbolt |
| Stantler | 51 | Sitrus Berry | Intimidate | default | Wild Charge, Zen Headbutt, Sucker Punch, Thunder Wave |
| Fearow | 52 | none | Sniper | default | Drill Peck, Tri Attack, U-turn, Quick Attack |
| Piloswine | 54 | Eviolite | Thick Fat | default | Stealth Rock, Earthquake, Ice Shard, Throat Chop |

Today's team: Abomasnow 50 (Blizzard, Energy Ball, Focus Blast, Shadow Ball). Expected: 97 / 1.01 / 38 blind in my simulator, about 75 clean in the scorer's terms.

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

### Skier Kaitlyn: Route 216, optional, single, cap 56

A Toxic Boost Zangoose on a Toxic Orb behind Delibird's Sash and Drill Run, Pidgeot and Bellossom. Kaizo's team, with Delibird's Adaptability.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Delibird | 54 | Focus Sash | Adaptability | default | Ice Shard, Drill Peck, Drill Run, Icy Wind |
| Pidgeot | 53 | Sitrus Berry | Intimidate | default | Air Slash, U-turn, Roost, Quick Attack |
| Bellossom | 53 | Leftovers | Chlorophyll | default | Petal Dance, Dazzling Gleam, Moonlight, Sleep Powder |
| Zangoose | 53 | Toxic Orb | Toxic Boost | default | Facade, Close Combat, Knock Off, Quick Attack |

Today's team: Mamoswine 54 (Ice Fang, Headbutt, Earthquake, Superpower), Delibird 54 (Present, Blizzard, Signal Beam). Expected: 98 / 1.22 / 24 blind in my simulator, about 70 clean in the scorer's terms.

### Skier Andrea: Route 216, optional, single, cap 56

Burn then Hex from a Cursed Body Froslass, an Eviolite Porygon2, Alakazam and Meganium. Kaizo's level-98 joke is gone.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Meganium | 52 | Leftovers | Thick Fat | default | Energy Ball, StompingTantrum, Leech Seed, Synthesis |
| Froslass | 52 | Sitrus Berry | Cursed Body | default | Will-O-Wisp, Hex, Ice Beam, Thunderbolt |
| Alakazam | 51 | none | Magic Guard | default | Psychic, Shadow Ball, Dazzling Gleam, Energy Ball |
| Porygon2 | 54 | Eviolite | Analytic | default | Ice Beam, Thunderbolt, Recover, Thunder Wave |

Today's team: Froslass 55 (Shadow Ball, Thunderbolt, Thunder Wave, Blizzard). Expected: 98 / 0.95 / 36 blind in my simulator, about 74 clean in the scorer's terms.

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

### Black Belt Philip: Route 216, optional, single, cap 56

A Protean Kecleon's Fake Out beside Hitmonlee's Scope Lens, Machamp's Throat Chop and Hitmontop's Triple Axel. Kaizo's Kecleon, with the hidden Protean.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Hitmontop | 54 | Leftovers | Technician | default | Triple Axel, Rolling Kick, Sucker Punch, Rapid Spin |
| Machamp | 51 | none | Steadfast | default | Close Combat, Throat Chop, Bullet Punch, Rock Slide |
| Hitmonlee | 52 | Scope Lens | Reckless | default | Hi Jump Kick, Blaze Kick, Knock Off, Rock Slide |
| Kecleon | 51 | Sitrus Berry | Protean | default | Fake Out, Sucker Punch, Shadow Sneak, Drain Punch |

Today's team: Machamp 56 (ThunderPunch, Cross Chop, Poison Jab, Low Kick). Expected: 96 / 1.24 / 31 blind in my simulator, about 72 clean in the scorer's terms.

### Skier Shawn: Route 217 (hail), optional, single, cap 56

The hail: Glaceon's sure Blizzard, Walrein, Swampert's Roar, and an Alolan Ninetales whose Aurora Veil only works in hail. Kaizo's six cut to four; my simulator does not model Aurora Veil, so the team plays harder than it reads.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Swampert | 51 | Leftovers | Torrent | default | Liquidation, Earthquake, Avalanche, Roar |
| Walrein | 52 | Sitrus Berry | Ice Body | default | Ice Beam, Surf, Toxic, StompingTantrum |
| Glaceon | 51 | none | Ice Body | default | Blizzard, Shadow Ball, Freeze-Dry, Wish |
| Alolan Ninetales | 54 | Light Clay | Magic Guard | default | Aurora Veil, Blizzard, Dazzling Gleam, Psyshock |

Today's team: Glalie 51 (Crunch, Super Fang, Ice Shard, Headbutt). Expected: 96 / 1.66 / 17 blind in my simulator in hail, about 67 clean in the scorer's terms.

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

### Skier Bjorn: Route 217 (hail), optional, single, cap 56

Grass against the ice: Roserade's Sleep Powder, a Rocky Helmet Tangrowth with Petal Blizzard, Sceptile, and Torterra's Headlong Rush. Kaizo's lone level-84 Sceptile grown into a team.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Torterra | 51 | Leftovers | Thick Fat | default | Wood Hammer, Headlong Rush, Crunch, Synthesis |
| Sceptile | 52 | none | Overgrow | default | Leaf Blade, Dragon Claw, X-Scissor, Rock Slide |
| Roserade | 52 | Black Sludge | Natural Cure | default | Sludge Bomb, Giga Drain, Shadow Ball, Sleep Powder |
| Tangrowth | 54 | Rocky Helmet | Regenerator | default | Petal Blizzard, Knock Off, Stun Spore, AncientPower |

Today's team: Mamoswine 51 (Avalanche, Stone Edge, Earthquake, Giga Impact). Expected: 97 / 1.48 / 16 blind in my simulator in hail, about 66 clean in the scorer's terms.

### Skier Lexie: Route 217 (hail), optional, single, cap 56

Ice Body in the hail: Dewgong's sure Blizzard and Drill Run, Sealeo, Jynx's Fake Out, and a Glalie holding the Ability Shield Lexie awards.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Dewgong | 54 | Leftovers | Ice Body | default | Blizzard, Aqua Tail, Drill Run, Fake Out |
| Jynx | 51 | Sitrus Berry | Dry Skin | default | Ice Beam, Psychic, Draining Kiss, Fake Out |
| Sealeo | 51 | none | Ice Body | default | Ice Beam, Surf, Body Slam, Encore |
| Glalie | 51 | Ability Shield | Ice Body | default | Ice Fang, Crunch, Ice Shard, Taunt |

Today's team: Dewgong 51 (Dive, Waterfall, Sheer Cold, Aqua Jet), Glaceon 51 (Ice Beam, Shadow Ball, Roar, Toxic). Expected: 97 / 1.25 / 22 blind in my simulator in hail, about 69 clean in the scorer's terms.

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

### Skier Madison: Route 217 (hail), optional, single, cap 56

Weather Ball: Castform's Forecast turns it Ice in the hail, beside Exploud's Hyper Voice, a Magic Bounce Espeon and Purugly's Defiant Fake Out. Kaizo's team cut to four.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Exploud | 51 | Leftovers | Scrappy | default | Hyper Voice, Ice Beam, Flamethrower, StompingTantrum |
| Castform | 52 | none | Forecast | default | Weather Ball, Thunderbolt, Energy Ball, Flamethrower |
| Espeon | 51 | none | Magic Bounce | default | Psychic, Dazzling Gleam, Shadow Ball, Signal Beam |
| Purugly | 54 | Sitrus Berry | Defiant | default | Fake Out, Play Rough, Sucker Punch, U-turn |

Today's team: Jynx 51 (Psychic, Blizzard, Energy Ball, Perish Song). Expected: 99 / 1.03 / 32 blind in my simulator in hail, about 73 clean in the scorer's terms.

### Ninja Boy Matthew: Route 217 (hail), optional, single, cap 56

Tricks: a Poison Heal Lickilicky on a Toxic Orb, Weavile, a Prankster Sableye's Will-O-Wisp and Hex, and Haunter's Hypnosis. Kaizo's Shadow Tag Gengar and Endeavor Shedinja are gone, both barred.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Lickilicky | 52 | Toxic Orb | Poison Heal | default | Body Slam, Power Whip, Knock Off, Rock Slide |
| Weavile | 51 | BlackGlasses | Inner Focus | default | Night Slash, Triple Axel, Ice Shard, Brick Break |
| Sableye | 54 | Leftovers | Prankster | default | Will-O-Wisp, Hex, Knock Off, Recover |
| Haunter | 52 | none | Levitate | default | Shadow Ball, Sludge Bomb, Thunderbolt, Hypnosis |

Today's team: Shedinja 51 (X-Scissor, Confuse Ray, Shadow Sneak, Night Slash). Expected: 96 / 1.67 / 13 blind in my simulator in hail, about 65 clean in the scorer's terms.

### Ninja Boy Ethan: Route 217 (hail), optional, single, cap 56

Speed Boost Ninjask behind Weezing's Will-O-Wisp, an Eviolite Dusclops and an Intimidate Staraptor. Kaizo's evasion and stacked hazards are gone.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Weezing | 52 | Black Sludge | Levitate | default | Sludge Wave, Will-O-Wisp, Pain Split, Heat Wave |
| Dusclops | 53 | Eviolite | Pressure | default | Shadow Punch, Ice Punch, Will-O-Wisp, Pain Split |
| Staraptor | 51 | none | Intimidate | default | Brave Bird, Aerial Ace, U-turn, Quick Attack |
| Ninjask | 54 | SilverPowder | Speed Boost | default | X-Scissor, Aerial Ace, U-turn, Night Slash |

Today's team: Ninjask 51 (Swords Dance, Slash, Night Slash, X-Scissor). Expected: 99 / 1.26 / 24 blind in my simulator in hail, about 70 clean in the scorer's terms.

### Black Belt Luke: Route 217 (hail), on the path, single, cap 56

Fighting types with Hariyama's Whirlwind previewing Candice's phazing alone: Breloom's Low Sweep, Hitmonchan's punches and Lucario's Extreme Speed.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Breloom | 52 | Leftovers | Technician | default | Mach Punch, Seed Bomb, Stun Spore, Low Sweep |
| Hitmonchan | 51 | Lum Berry | Iron Fist | default | Drain Punch, Ice Punch, ThunderPunch, Mach Punch |
| Hariyama | 52 | Sitrus Berry | Thick Fat | default | Close Combat, Knock Off, Bullet Punch, Whirlwind |
| Lucario | 54 | none | Iron Fist | default | Meteor Mash, Close Combat, Bullet Punch, ExtremeSpeed |

Today's team: Toxicroak 51 (Dark Pulse, Nasty Plot, Vacuum Wave, Sludge Bomb), Lucario 51 (Aura Sphere, Close Combat, Dragon Pulse, ExtremeSpeed), Breloom 51 (Sky Uppercut, Spore, Seed Bomb, Mach Punch). Expected: 99 / 1.29 / 18 blind in my simulator in hail, about 67 clean in the scorer's terms.

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


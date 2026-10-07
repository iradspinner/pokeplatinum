# The comb: the Galactic headquarters split

**Every trainer of the headquarters split is now combed.** The two bosses,
Cyrus and Saturn, were combed earlier. On 2026-10-07 the twelve grunts and
scientists of the building were added, as the gauntlet `gauntlets.md` names:
four sections (1F, 2F, 3F, B2F), each fought without healing between
trainers. Every file passes the checker and the rule audit.

The gauntlet follows Ian's ruling of 2026-10-07. Kaizo's headquarters is a
Trick Room gauntlet of Explosions, Destiny Bonds and Shadow Tag, all barred
here; only Saturn keeps Trick Room, as Ian built him. What survives is
Kaizo's chip: Toxic Spikes, Spikes, Stealth Rock, Leech Seed, Will-O-Wisp,
Glare, sleep and the Toxic Orb, now with Snarl, Hex, Foul Play, Psychic Noise,
Clear Smog and Skitter Smack from the modern pool. Each tool Cyrus and Saturn
use (their Stealth Rock, Spikes, phazing, sleep, the orb) appears on a grunt
before them, alone.

| Check | Result |
|---|---|
| Sections read whole (1F, 2F, 3F, B2F) | 99.5, 92, 88 and 99 won |
| Faints a section, in the scorer's terms (Ian's band under 0.6) | 0.2, 1.0, 1.0 and 0.3 |
| Clean a section, in the scorer's terms (Ian's 60 or more) | 89, 72, 73 and 87 |
| Each trainer read blind (12) | 99 to 100 won |
| Move slots that are Generation 5+ | 15 of 96, 16 percent |
| Hidden abilities | 4 |
| Element 7 items held | 2 Rocky Helmets |

The two four-trainer sections, 2F and 3F, cost about one Pokemon each in the
scorer's terms, above Ian's band, and lose about one run in ten. They started
far worse: with three Pokemon a grunt, 2F and 3F read 8 to 13 won, because
the six meets twelve Pokemon in a row with status carried between fights.
Each grunt now brings two, as today's files do (decision 3). I also thinned
the carried status to one kind per trainer and took the bulk items (Leftovers,
Sitrus, Eviolite) off 2F and 3F. Every team carries at least one modern move.

## The bosses, combed earlier

**Refreshed 2026-10-07.** The expected numbers were read again after two
changes: a fix to my simulator, which had picked the player's lead by party
order when two choices looked equal and so skewed every earlier boss reading,
and the legality sweep against the final lists (origin/balance-tm-pass at
377312dbf0), which left this split unchanged. Ian ruled that every draft goes into step 12 as
drafted; the scorer's step 15 reading gives the real numbers, and he chooses
any retunes from them. My candidates are in `../retune-proposals-not-approved/`.

The two bosses of the headquarters split are combed: Cyrus on 4F and Saturn
in the control room. Both files pass the checker and the rule audit.

The cap is 60, and no map here has its own weather. My simulator reads the
bosses against the scorer's box at HQ, which knows no TMs, so they read
harsher than they will once the TM pass lands. Saturn fights under permanent
Trick Room for the whole battle (Ian's design of 2026-09-26, in the battle
code), so his six is built slow and bulky, on natures that lower Speed, and
both his file and today's are read under the room. Cyrus reads about 95 won
to today's 99.6. Saturn now sits three under the cap, his ace at 57 (Ian,
2026-10-07: three under the cap), and reads about 98 won to today's 99 (93 at
the cap, read before my simulator's patch of 2026-10-07). Each carries one legendary
(Suicune, Uxie) where today's Saturn carried two. The bosses carry no
conditional attack; the gauntlet's Gengar carries Dream Eater.

## Decisions for Ian

| # | Decision | What the files do today | How it is checked | What Ian decides |
|---|---|---|---|---|
| 1 | Cyrus 2's setup move sits on Houndoom, not his ace | The dial puts a boss's setup move on its ace. A Swords Dance Weavile ace read 65 to 74 won, far past a step harder, so Weavile keeps today's Fake Out and Ice Shard and the Nasty Plot sits on Houndoom. Today's Mean Look and Rest Dusknoir and Curse Suicune are gone; Magnezone's Magnet Pull stays as the trap. | `galactic_boss_cyrus_galactic_hq.json`; the scorer's reading later. | Accept (recommended), or a Swords Dance Weavile with the rest a level lower. |
| 2 | Saturn 2 is built for his permanent Trick Room | Uxie leads with Stealth Rock and Thunder Wave behind a Focus Sash, then a Shadow Tag Wobbuffet with Counter (the trap the dial asks of him, and his one trade), Lickilicky, today's Wailord with Water Spout, Rhyperior and a Toxicroak ace, all on natures that lower Speed. Cresselia is out, so he keeps one legendary. A Curse Snorlax ace read 48 won under the room, and a Bronzong with Light Clay screens in Lickilicky's place read 97. | `commander_saturn_galactic_hq.json`, read under Trick Room; the scorer's reading later, which must model the room. | Accept (recommended). |

| 3 | The gauntlet's grunts bring two Pokemon each | Rule 3 asks for four to six on ordinary trainers from Byron's split. The headquarters grunts and scientists bring two, as today's files do, because a section of four trainers is read whole without healing; with three each, 2F and 3F read 8 to 13 won. | The sections above; the scorer's gauntlet reading at step 15. | Accept (recommended), or larger teams with the levels lowered past the dial's three under. |

## What comes next

Volkner's split's ordinary trainers.

## Overview

| Trainer | Place | Path | Battle | Size | Levels | The idea | Expected |
|---|---|---|---|---|---|---|---|
| Galactic Grunt (1F) | Galactic HQ 1F | gauntlet, 1F | single | 2 | 54 to 57 | Poison that follows you | 100 / 0.17 / 84 blind in my simulator, about 94 clean in the scorer's terms |
| Scientist Fredrick | Galactic HQ 1F | gauntlet, 1F | single | 2 | 54 to 57 | Psychic status | 100 / 0.12 / 89 blind in my simulator, about 96 clean in the scorer's terms |
| Galactic Grunt (2F, 1) | Galactic HQ 2F | gauntlet, 2F | single | 2 | 54 to 57 | Leech Seed and Toxic | 100 / 0.24 / 76 blind in my simulator, about 90 clean in the scorer's terms |
| Galactic Grunt (2F, 2) | Galactic HQ 2F | gauntlet, 2F | single | 2 | 54 to 57 | Spikes and phazing | 100 / 0.14 / 86 blind in my simulator, about 94 clean in the scorer's terms |
| Galactic Grunt (2F, 3) | Galactic HQ 2F | gauntlet, 2F | single | 2 | 54 to 57 | Sun | 100 / 0.15 / 86 blind in my simulator, about 94 clean in the scorer's terms |
| Scientist Darrius | Galactic HQ 2F | gauntlet, 2F | single | 2 | 54 to 57 | Paralysis | 100 / 0.41 / 60 blind in my simulator, about 84 clean in the scorer's terms |
| Galactic Grunt (3F, 1) | Galactic HQ 3F | gauntlet, 3F | single | 2 | 54 to 57 | Sleep | 99 / 0.40 / 71 blind in my simulator, about 88 clean in the scorer's terms |
| Galactic Grunt (3F, 2) | Galactic HQ 3F | gauntlet, 3F | single | 2 | 54 to 57 | Burn | 100 / 0.08 / 92 blind in my simulator, about 97 clean in the scorer's terms |
| Galactic Grunt (3F, 3) | Galactic HQ 3F | gauntlet, 3F | single | 2 | 54 to 57 | Two Intimidates | 100 / 0.24 / 77 blind in my simulator, about 91 clean in the scorer's terms |
| Galactic Grunt (3F, 4) | Galactic HQ 3F | gauntlet, 3F | single | 2 | 54 to 57 | Stealth Rock from Bronzong | 100 / 0.06 / 95 blind in my simulator, about 98 clean in the scorer's terms |
| Cyrus 2 | Galactic HQ 4F | on the path | single, boss | 6 | 58 to 60 | Two hazards and a trap | about 95 / 1.5 / 17 in my simulator, where today's file reads 100 / 0.9 / 21 |
| Galactic Grunt (B2F, 1) | Galactic HQ B2F | gauntlet, B2F | single | 2 | 54 to 57 | Glare and Toxic Spikes | 100 / 0.16 / 85 blind in my simulator, about 94 clean in the scorer's terms |
| Galactic Grunt (B2F, 2) | Galactic HQ B2F | gauntlet, B2F | single | 2 | 55 to 57 | Saturn's orb previewed alone | 100 / 0.19 / 81 blind in my simulator, about 92 clean in the scorer's terms |
| Saturn 2 | Galactic HQ control room | on the path | single, boss, permanent Trick Room | 6 | 55 to 57 | Slow and bulky for his permanent Trick Room | about 98 / 3.0 / 0 in my simulator, where today's file reads 99 / 1.5 / 1 |

Expected numbers are won / faints a fight / clean in my simulator, beside
today's file. A gauntlet trainer's numbers are read alone; the sections'
readings are in the summary above.

## The trainers

### Galactic Grunt (1F): Galactic HQ 1F, gauntlet, 1F, single, cap 60

Poison that follows you: Qwilfish's Toxic Spikes and Crobat's Toxic, both carried into Fredrick's fight.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Qwilfish | 54 | Black Sludge | Intimidate | default | Toxic Spikes, Poison Jab, Throat Chop, Aqua Tail |
| Crobat | 57 | Sitrus Berry | Inner Focus | default | Cross Poison, Leech Life, Toxic, U-turn |

Today's team: Qwilfish 54 (Take Down, Aqua Tail, Poison Jab, Destiny Bond), Venomoth 54 (Sludge Bomb, Signal Beam, Psychic, Energy Ball). Expected: 100 / 0.17 / 84 blind in my simulator, about 94 clean in the scorer's terms.

### Scientist Fredrick: Galactic HQ 1F, gauntlet, 1F, single, cap 60

Psychic status: Gardevoir's Will-O-Wisp and Mystical Fire, Alakazam's Thunder Wave and Recover.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Gardevoir | 54 | none | Trace | default | Psychic, Mystical Fire, Will-O-Wisp, Dazzling Gleam |
| Alakazam | 57 | none | Magic Guard | default | Psychic, Shadow Ball, Recover, Thunder Wave |

Today's team: Gardevoir 53 (Psychic, Calm Mind, Hypnosis, Focus Blast), Alakazam 53 (Psychic, Energy Ball, Thunder Wave, Recover). Expected: 100 / 0.12 / 89 blind in my simulator, about 96 clean in the scorer's terms.

### Galactic Grunt (2F, 1): Galactic HQ 2F, gauntlet, 2F, single, cap 60

Leech Seed and Toxic: Roserade's poison, then a Rocky Helmet Tangrowth with Leech Seed and Petal Blizzard.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Roserade | 54 | Black Sludge | Natural Cure | default | Sludge Bomb, Giga Drain, Toxic, Synthesis |
| Tangrowth | 57 | Rocky Helmet | Regenerator | default | Leech Seed, Knock Off, Petal Blizzard, AncientPower |

Today's team: Breloom 54 (Sky Uppercut, ThunderPunch, Seed Bomb, DynamicPunch), Exeggutor 54 (Psychic, Synthesis, Sunny Day, SolarBeam). Expected: 100 / 0.24 / 76 blind in my simulator, about 90 clean in the scorer's terms.

### Galactic Grunt (2F, 2): Galactic HQ 2F, gauntlet, 2F, single, cap 60

Spikes and phazing, previewing Cyrus's Skarmory alone: a Rocky Helmet Skarmory lays Spikes and Whirlwinds, behind Sharpedo's Poison Fang.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Sharpedo | 54 | none | Tinted Lens | default | Crunch, Poison Fang, Aqua Jet, Ice Fang |
| Skarmory | 57 | Rocky Helmet | Filter | default | Spikes, Whirlwind, Dual Wingbeat, Steel Wing |

Today's team: Fearow 54 (U-turn, Steel Wing, Roost, Drill Peck), Sharpedo 54 (Aqua Jet, Ice Fang, Crunch, Skull Bash). Expected: 100 / 0.14 / 86 blind in my simulator, about 94 clean in the scorer's terms.

### Galactic Grunt (2F, 3): Galactic HQ 2F, gauntlet, 2F, single, cap 60

Sun: Exeggutor's Sunny Day on a Heat Rock, then Houndoom's Flamethrower, Will-O-Wisp and Snarl.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Exeggutor | 54 | Heat Rock | Chlorophyll | default | Sunny Day, Psychic, Giga Drain, Synthesis |
| Houndoom | 57 | none | Flash Fire | default | Flamethrower, Dark Pulse, Will-O-Wisp, Snarl |

Today's team: Houndoom 54 (Flamethrower, SolarBeam, Dark Pulse, Sunny Day), Victreebel 54 (SolarBeam, Weather Ball, Synthesis, Sludge Bomb). Expected: 100 / 0.15 / 86 blind in my simulator, about 94 clean in the scorer's terms.

### Scientist Darrius: Galactic HQ 2F, gauntlet, 2F, single, cap 60

Paralysis: Magnezone's Thunder Wave and Discharge, Porygon2's Tri Attack and Foul Play.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Magnezone | 54 | none | Levitate | default | Thunder Wave, Flash Cannon, Discharge, Tri Attack |
| Porygon2 | 57 | none | Download | default | Tri Attack, Discharge, Recover, Foul Play |

Today's team: Porygon Z 55 (Psychic, Signal Beam, Ice Beam, Tri Attack). Expected: 100 / 0.41 / 60 blind in my simulator, about 84 clean in the scorer's terms.

### Galactic Grunt (3F, 1): Galactic HQ 3F, gauntlet, 3F, single, cap 60

Sleep, then Dream Eater and Hex: Gengar's Hypnosis behind Dusknoir's Pain Split. Dream Eater is the split's one conditional attack.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Dusknoir | 54 | none | Levitate | default | Shadow Punch, Ice Punch, Pain Split, Shadow Sneak |
| Gengar | 57 | none | Levitate | default | Hypnosis, Dream Eater, Hex, Confuse Ray |

Today's team: Marowak 54 (Thick Club; Earthquake, Iron Head, Fire Punch, ThunderPunch), Gengar 54 (Shadow Ball, Hypnosis, Dark Pulse, Dream Eater). Expected: 99 / 0.40 / 71 blind in my simulator, about 88 clean in the scorer's terms.

### Galactic Grunt (3F, 2): Galactic HQ 3F, gauntlet, 3F, single, cap 60

Burn, then Hex: Mismagius's Will-O-Wisp, and Gastrodon's Clear Smog wiping the player's boosts.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Mismagius | 54 | none | Levitate | default | Will-O-Wisp, Hex, Dazzling Gleam, Thunderbolt |
| Gastrodon | 57 | none | Dry Skin | default | Muddy Water, Clear Smog, Recover, Stockpile |

Today's team: Kricketune 53 (Taunt, Night Slash, Bug Buzz, Perish Song), Gastrodon 53 (Hidden Power, Rain Dance, Body Slam, Muddy Water). Expected: 100 / 0.08 / 92 blind in my simulator, about 97 clean in the scorer's terms.

### Galactic Grunt (3F, 3): Galactic HQ 3F, gauntlet, 3F, single, cap 60

Two Intimidates: Granbull's Roar and Play Rough, then Stantler's Light Screen.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Granbull | 54 | none | Intimidate | default | Roar, Play Rough, Crunch, Thunder Fang |
| Stantler | 57 | none | Intimidate | default | Zen Headbutt, Sucker Punch, Stomp, Light Screen |

Today's team: Ursaring 54 (Slash, Focus Punch, Rest, Brick Break), Granbull 54 (Roar, Headbutt, Earthquake, Crunch). Expected: 100 / 0.24 / 77 blind in my simulator, about 91 clean in the scorer's terms.

### Galactic Grunt (3F, 4): Galactic HQ 3F, gauntlet, 3F, single, cap 60

Stealth Rock from Bronzong, previewing Cyrus's and Saturn's alone, and Grumpig's Confuse Ray.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Grumpig | 54 | none | Own Tempo | default | Psybeam, Power Gem, Confuse Ray, Rest |
| Bronzong | 57 | none | Levitate | default | Stealth Rock, Psychic Noise, Iron Defense, Payback |

Today's team: Hypno 54 (Zen Headbutt, Headbutt, Drain Punch, Ice Punch), Grumpig 54 (Confuse Ray, Shadow Ball, Power Gem, Psychic). Expected: 100 / 0.06 / 95 blind in my simulator, about 98 clean in the scorer's terms.

### Cyrus 2: Galactic HQ 4F, on the path, single, boss, cap 60

Two hazards and a trap: Skarmory lays Stealth Rock and Spikes behind a Focus Sash and phazes with Whirlwind, Magnezone's Magnet Pull traps Steel types (the fight's one trade), then Dusknoir's Will-O-Wisp, a Nasty Plot Houndoom, Suicune as the legendary, and Weavile at the cap with Fake Out and Ice Shard.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Skarmory | 58 | Focus Sash | Filter | Impish | Stealth Rock, Spikes, Whirlwind, Brave Bird |
| Magnezone | 58 | Shuca Berry | Magnet Pull | Modest | Thunderbolt, Flash Cannon, Tri Attack, Thunder Wave |
| Dusknoir | 58 | Leftovers | Levitate | Adamant | Shadow Punch, Earthquake, Ice Punch, Will-O-Wisp |
| Houndoom | 58 | Sitrus Berry | Flash Fire | Timid | Flamethrower, Dark Pulse, Sludge Bomb, Nasty Plot |
| Suicune | 58 | Leftovers | Pressure | Bold | Surf, Ice Beam, Roar, Toxic |
| Weavile | 60 | Lum Berry | Technician | Jolly | Night Slash, Ice Punch, Ice Shard, Fake Out |

Today's team: Skarmory 57 (Sitrus Berry; Stealth Rock, Steel Wing, Pluck, Tailwind), Dusknoir 57 (Chesto Berry; Shadow Punch, Brick Break, Mean Look, Rest), Houndoom 57 (Charcoal; Flamethrower, Sludge Bomb, Will-O-Wisp, Dark Pulse), Suicune 57 (Leftovers; Aqua Ring, Curse, Waterfall, Avalanche), Magnezone 57 (Shuca Berry; Magnet Rise, Flash Cannon, Charge Beam, Natural Gift), Weavile 58 (NeverMeltIce; Night Slash, Ice Punch, Ice Shard, Fake Out). Expected: about 95 / 1.5 / 17 in my simulator, where today's file reads 100 / 0.9 / 21.

### Galactic Grunt (B2F, 1): Galactic HQ B2F, gauntlet, B2F, single, cap 60

Glare and Toxic Spikes: Arbok's paralysis and Skitter Smack, Drapion's Toxic Spikes and Knock Off.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Arbok | 54 | Sitrus Berry | Intimidate | default | Glare, Poison Fang, Crunch, Skitter Smack |
| Drapion | 57 | Leftovers | Hyper Cutter | default | Toxic Spikes, Knock Off, Cross Poison, Ice Fang |

Today's team: Weezing 54 (Toxic, Flamethrower, Explosion, Sludge Bomb), Arbok 54 (Gunk Shot, Crunch, Earthquake, Glare). Expected: 100 / 0.16 / 85 blind in my simulator, about 94 clean in the scorer's terms.

### Galactic Grunt (B2F, 2): Galactic HQ B2F, gauntlet, B2F, single, cap 60

Saturn's orb previewed alone: Cacturne's Spikes and Leech Seed, then a Poison Heal Lickilicky on a Toxic Orb.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Cacturne | 55 | Leftovers | Water Absorb | default | Spikes, Leech Seed, Needle Arm, Sucker Punch |
| Lickilicky | 57 | Toxic Orb | Poison Heal | default | Body Slam, Knock Off, StompingTantrum, Rock Slide |

Today's team: Cacturne 54 (Spikes, Sucker Punch, Payback, Needle Arm), Seviper 54 (Swagger, Haze, Night Slash, Poison Jab). Expected: 100 / 0.19 / 81 blind in my simulator, about 92 clean in the scorer's terms.

### Saturn 2: Galactic HQ control room, on the path, single, boss, permanent Trick Room, cap 60

Slow and bulky for his permanent Trick Room: Uxie leads with Stealth Rock and Thunder Wave behind a Focus Sash, the Shadow Tag Wobbuffet returns with Counter (the trap and the trade), then a Poison Heal Lickilicky, Wailord's Water Spout, Rhyperior and a Swords Dance Toxicroak ace, all on natures that lower Speed.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Uxie | 55 | Focus Sash | Levitate | Relaxed | Stealth Rock, U-turn, Psychic, Thunder Wave |
| Lickilicky | 56 | Toxic Orb | Poison Heal | Brave | Body Slam, Earthquake, Knock Off, Power Whip |
| Wobbuffet | 56 | Leftovers | Shadow Tag | Relaxed | Counter, Encore, Safeguard, Charm |
| Wailord | 56 | Leftovers | Pressure | Quiet | Water Spout, Surf, Ice Beam, Toxic |
| Rhyperior | 56 | Passho Berry | Solid Rock | Brave | Earthquake, Stone Edge, Hammer Arm, Ice Punch |
| Toxicroak | 57 | Life Orb | Dry Skin | Brave | Gunk Shot, Cross Chop, Sucker Punch, Swords Dance |

Today's team: Uxie 57 (Lum Berry; Hypnosis, Future Sight, U-turn, Foul Play), Lickilicky 57 (Toxic Orb; Slam, Curse, Gyro Ball, ThunderPunch), Wailord 57 (Leftovers; Water Spout, Earthquake, Aqua Ring, Avalanche), Rhyperior 57 (Expert Belt; Earthquake, Stone Edge, Aqua Tail, Fire Punch), Cresselia 57 (Leftovers; Moonlight, Charge Beam, Calm Mind, Ice Beam), Toxicroak 58 (Life Orb; Gunk Shot, Cross Chop, Sucker Punch, Fire Punch). Expected: about 98 / 3.0 / 0 in my simulator, where today's file reads 99 / 1.5 / 1.


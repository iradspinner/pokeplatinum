# The comb: Gardenia's split

Every trainer of Gardenia's split is combed, in walking order: 39 files beside
this one, all passing the checker (Oxide species, moves including TM and tutor
lists, items, ability slots, no one-hit KO move, levels at or under the cap,
and the borrowed-attack ceiling Ian kept). The Jubilife grunts' tag battle
opens the split; their teams are in Roark's comb (`roark.md`) and are not
rebuilt here.

The cap is 19 until Mars 1 falls and 26 after him; Route 205's trainers all
stand north of the grunts who block it until then, so they meet the cap of 26.
Ordinary trainers sit one or two levels under the cap with three to six
Pokemon (Fisherman Andrew carries six), most with a danger member and coverage
aimed at the box this split reads them against. The route trainers rehearse
Gardenia's tools one at a time (sleep on Taylor, Spikes on the gym's Angela
and Lindsay), and her gym's trainers show two together.

None of this has been read by the scorer, which reads the bosses after the
learnset and TM passes land. The expected numbers come from my own rough
simulator, now drawing blind sixes from the scorer's pools and modelling
weather, and corrected against the scorer's readings of Roark's split; trust
them to about ten points. They are also against a box without TMs, so they
read harsher than the fights will once the TM pass arms it. In those terms the bosses read Somnu about 96 won,
Mars 1 about 96 and Gardenia about 90. The ordinary singles average about 89
clean (73 to 98), a little softer than Ian's 80 to 85: the Water and Rock
teams read softest, because the pool at 26 is built from Fire, Flying, Bug,
Poison and Fighting types that wall them.

## Decisions for Ian

Ian answered all four on 2026-10-06 (`../../ians-answers-2026-10-06.md`); his answers are in the table.

| # | Decision | What the files do today | How it is checked | What Ian decides |
|---|---|---|---|---|
| 1 | Gardenia has no sun (Ian: understood; retool after the scorer reads her) | Her five are Roselia (Spikes, Sleep Powder), Ludicolo, Exeggutor, Breloom and Roserade, with Ice, Psychic and Rock coverage; Sunny Day appears on Elizabeth, Jenna and Angela instead. With sun she read softer in my simulator (about 95 won), because the planned box's Fire types gain more from it than her team does. | `leader_gardenia.json`; the scorer's reading of her later. | Keep her without sun (recommended), or give her a setter and accept a softer fight. |
| 2 | Officer Somnu is built as a boss | Goal 3 reads her as a named Galactic fight, so she has items, natures and boss IVs, and her Gulpin became a Swalot. Ian answered: Dream Eater is a conditional attack and exempt from the ceiling, so her Swalot has it back, beside Yawn. | `galactic_grunt_valley_windworks_3.json`. | Answered (2026-10-06). Flagged as the split's one conditional attack. |
| 3 | Water and Rock teams read soft (Ian: they stay; he tests them in the alpha) | Karina, Nicholas, Daniel, Joseph, Zachary and Kelsey estimate 95 to 98 clean. | My estimates now; a blind reading if the scorer ever reads ordinary trainers. | Accept (recommended: the box's Grass, Electric and Fighting types are their answers), or give each an off-type danger member. |
| 4 | Doubles and tags | Twins Liv & Liz (a double) and the forest's four pairs (tag battles beside Cheryl) are built a notch softer than their neighbours. | The scorer cannot read either yet. | Nothing now; they come back when doubles can be read. |

No trainer of this split stands on a map with its own weather (a map's
weather is battle weather for every fight on it, as at Oreburgh's gym, which
fights in sand), so the split's only weather is the Sunny Day on Elizabeth,
Jenna and Angela.

**The legality sweep (2026-10-07).** The files were checked against the final
learnsets and TM list (origin/balance-tm-pass at 377312dbf0), with the moves
cut from the TM list kept in each species' trainer palette as Ian ruled. 40
moves the lists no longer hold were swapped for legal ones doing the same job,
nearly all small level-up moves; the tables below show the swept sets. The
expected numbers date from before the sweep, and the scorer's step 15 reading
gives the real ones. The swaps:

- Lass Sarah's Skitty: Tail Whip to Baby Doll Eyes.
- Lass Samantha's Budew: Absorb to Bullet Seed.
- Lass Samantha's Budew: Growth to Cotton Spore.
- Lass Samantha's Ponyta: Tail Whip to Charm.
- Lass Samantha's Ponyta: Growl to Charm.
- Youngster Tyler's Wingull: Growl to Roost.
- Youngster Tyler's Lotad: Absorb to Bullet Seed.
- Youngster Tyler's Lotad: Growl to Sweet Scent.
- Bug Catcher Brandon's Combee: Sweet Scent to Air Cutter.
- Aroma Lady Taylor's Cherubi: Growth to Synthesis.
- Aroma Lady Taylor's Bellsprout: Wrap to Bullet Seed.
- Aroma Lady Taylor's Oddish: Absorb to Bullet Seed.
- Aroma Lady Taylor's Tangela: Ingrain to Leech Seed.
- Galactic Grunt's Murkrow: Haze to Confuse Ray.
- Galactic Grunt's Stunky: Poison Gas to Leer.
- Galactic Grunt's Zubat: Wing Attack to Aerial Ace.
- Galactic Grunt's Koffing: Smoke Screen to Screech.
- Galactic Grunt's Koffing: Poison Gas to Scary Face.
- Galactic Officer Somnu's Eevee: Growl to Charm.
- Camper Jacob's Ponyta: Growl to Charm.
- Hiker Daniel's Phanpy: Defense Curl to Focus Energy.
- Battle Girl Kelsey's Meditite: Meditate to Foresight.
- Bug Catcher Jack's Beedrill: Fury Attack to Swift.
- Lass Briana's Marill: Defense Curl to Charm.
- Bug Catcher Phillip's Yanma: Detect to Endure.
- Bug Catcher Phillip's Yanma: Supersonic to Screech.
- Psychic Rachael's Chingling: Wrap to Swift.
- Psychic Rachael's Meditite: Meditate to Foresight.
- Psychic Rachael's Meditite: Detect to Endure.
- Fisherman Andrew's Magikarp: Splash to nothing (the move is dropped).
- Fisherman Andrew's Goldeen: Supersonic to Haze.
- Fisherman Joseph's Tentacool: Wrap to Rapid Spin.
- Fisherman Joseph's Shellder: Withdraw to Razor Shell.
- Aroma Lady Jenna's Weepinbell: Wrap to Bullet Seed.
- Aroma Lady Angela's Lileep: Ingrain to Confuse Ray.
- Beauty Lindsay's Bellsprout: Wrap to Bullet Seed.
- Beauty Lindsay's Tangela: Ingrain to Leech Seed.
- Gardenia's Roserade: Growth to Cotton Spore.
- Bird Keeper Alexandra's Swablu: Fury Attack to Swift.

## What comes next

Fantina's split is being combed now, then the bosses from Maylene's split on,
whose boxes are in the folder.

## Overview

| Trainer | Place | Path | Battle | Size | Levels | The idea | Expected |
|---|---|---|---|---|---|---|---|
| Galactic Grunts (two) | Jubilife City | on the path | tag, beside Dawn or Lucas | 3 and 3 | 16 to 17 | built in Roark's comb | not readable yet |
| Lass Sarah | Route 204 south | on the path | single | 4 | 16 to 17 | Fake Out first | 100 / 0.55 / 73 |
| Lass Samantha | Route 204 south | optional | single | 4 | 17 to 18 | Resist berries on the two members a player would target | 100 / 0.10 / 95 |
| Youngster Tyler | Route 204 south | optional | single | 4 | 17 to 18 | Trap and drain | 100 / 0.10 / 93 |
| Bug Catcher Brandon | Route 204 north | optional | single | 5 | 15 to 18 | Five evolved and evolving Bugs | 100 / 0.15 / 92 |
| Aroma Lady Taylor | Route 204 north | on the path | single | 4 | 16 to 18 | Sleep | 100 / 0.5 / 82 |
| Twins Liv & Liz | Route 204 north | optional | double | 3 | 16 to 17 | Plus and Minus twins | not readable yet (a double) |
| Galactic Grunt (1) | Floaroma Meadow | on the path | single | 4 | 17 to 18 | Paralysis | 100 / 0.10 / 95 |
| Galactic Grunt (2) | Floaroma Meadow | on the path | single | 4 | 17 to 18 | Fake Out and Pursuit | 100 / 0.20 / 89 |
| Galactic Grunt (3) | Valley Windworks, outside | on the path | single | 3 | 16 to 18 | Yawn forces a switch or a nap | 100 / 0.35 / 80 |
| Galactic Grunt (4) | Valley Windworks | on the path | single | 3 | 17 to 18 | Poison that lasts | 100 / 0.15 / 89 |
| Galactic Officer Somnu | Valley Windworks | on the path | single, named officer | 4 | 18 to 19 | Ian's Somnu kept to her idea | about 96 / 1.6 / 5 |
| Mars 1 | Valley Windworks | on the path | single, boss | 5 | 18 to 19 | Status from the lead and a deliberate hole | about 96 / 1.5 / 13 |
| Camper Jacob | Route 205 south | optional | single | 4 | 24 to 25 | Fire types with Fighting cover | 100 / 0.40 / 80 |
| Hiker Daniel | Route 205 south | optional | single | 4 | 24 to 25 | Rock Slide on three members | 100 / 0.10 / 96 |
| Aroma Lady Elizabeth | Route 205 south | optional | single | 3 | 24 to 25 | Sunny Day for her own Vulpix | 100 / 0.10 / 92 |
| Camper Zackary | Route 205 south | optional | single | 4 | 24 to 25 | Fire | 100 / 0.15 / 92 |
| Picnicker Siena | Route 205 south | optional | single | 5 | 23 to 25 | Electric types for the Flying and Water types | 100 / 0.40 / 85 |
| Hiker Nicholas | Route 205 south | optional | single | 3 | 25 | Rock Head and Rock Slide | 100 / 0.15 / 97 |
| Battle Girl Kelsey | Route 205 south | optional | single | 5 | 23 to 25 | Fighting types with Psychic cover | 100 / 0.05 / 96 |
| Picnicker Karina | Route 205 south | optional | single | 4 | 25 | Three starters' middle stages | 100 / 0.05 / 98 |
| Bug Catcher Jack | Eterna Forest | on the path | tag, with Lass Briana | 3 | 23 to 24 | Butterfree's Compound Eyes Sleep Powder beside a Swords Dance Ninjask and a Pursuit Beedrill | not readable yet (a tag battle) |
| Lass Briana | Eterna Forest | on the path | tag, with Bug Catcher Jack | 3 | 23 to 24 | Redirection | not readable yet (a tag battle) |
| Psychic Lindsey | Eterna Forest | on the path | tag, with Psychic Elijah | 3 | 23 to 24 | Hypnosis and Confuse Ray | not readable yet (a tag battle) |
| Psychic Elijah | Eterna Forest | on the path | tag, with Psychic Lindsey | 3 | 23 to 24 | Kadabra's Psybeam behind Wynaut's Counter and Mirror Coat | not readable yet (a tag battle) |
| Bug Catcher Phillip | Eterna Forest | optional | tag, with Bug Catcher Donald | 3 | 23 to 24 | Speed | not readable yet (a tag battle) |
| Bug Catcher Donald | Eterna Forest | optional | tag, with Bug Catcher Phillip | 3 | 23 to 24 | Bulky Bugs | not readable yet (a tag battle) |
| Psychic Kody | Eterna Forest | optional | tag, with Psychic Rachael | 3 | 23 to 24 | Yawn and Disable | not readable yet (a tag battle) |
| Psychic Rachael | Eterna Forest | optional | tag, with Psychic Kody | 3 | 23 to 24 | Wrap and Confusion | not readable yet (a tag battle) |
| Fisherman Andrew | Route 205 north | optional | single | 6 | 20 to 24 | Six fish | 100 / 0.5 / 76 |
| Fisherman Joseph | Route 205 north | optional | single | 3 | 25 | Skill Link | 100 / 0.05 / 95 |
| Fisherman Zachary | Route 205 north | optional | single | 4 | 24 to 25 | Water types that answer their counters | 100 / 0.10 / 96 |
| Aroma Lady Jenna | Eterna Gym | gym trainer | single | 4 | 24 to 25 | Sun and sleep together | 100 / 0.30 / 81 |
| Lass Caroline | Eterna Gym | gym trainer | single | 3 | 24 to 25 | Leech Seed and powders | 100 / 0.25 / 86 |
| Aroma Lady Angela | Eterna Gym | gym trainer | single | 4 | 25 | Spikes from Roselia | 100 / 0.40 / 86 |
| Beauty Lindsay | Eterna Gym | gym trainer | single | 4 | 24 to 25 | Spikes and sleep together | 100 / 0.10 / 95 |
| Gardenia | Eterna Gym | on the path | single, boss | 5 | 24 to 26 | Spikes and sleep from the lead | about 90 / 3.0 / 2 |
| Bird Keeper Alexandra | Route 211 west | optional | single | 5 | 23 to 25 | Five fliers with Pursuit for the switch and Swablu's Sing | 100 / 0.15 / 90 |
| Ninja Boy Zach | Route 211 west | optional | single | 4 | 24 to 25 | Speed Boost behind Protect | 100 / 0.35 / 85 |
| Hiker Louis | Route 211 west | optional | single | 3 | 24 to 25 | Few weaknesses | 100 / 0.30 / 83 |

Expected numbers are won / faints a fight / clean, at real odds, in the
scorer's terms.

## Trainer by trainer

### Lass Sarah: Route 204 south, on the path, single, cap 19

Fake Out first, then Normal types that hit hard: Furret's Adaptability doubles Covet and Fury Swipes. The player answers with a Rock or Steel type and does not let Furret set the pace.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Skitty | 16 | none | Cute Charm | default | Fake Out, Tackle, Baby-Doll Eyes, Sing |
| Meowth | 17 | none | Super Luck | default | Bite, Fury Swipes, Thief, Growl |
| Luxio | 17 | none | Hyper Cutter | default | Spark, Bite, Leer, Quick Attack |
| Furret | 17 | Oran Berry | Adaptability | default | Covet, Quick Attack, Fury Swipes, Defense Curl |

Today's team: Sentret 8 (default moves). Expected: 100 / 0.55 / 73, the sharpest of the early fights.

### Lass Samantha: Route 204 south, optional, single, cap 19

Resist berries on the two members a player would target: Shellos's Rindo Berry takes the Grass hit and Vulpix's Passho Berry the Water hit, so the obvious answer needs two hits.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Shellos | 18 | Rindo Berry | Dry Skin | default | Mud Bomb, Water Pulse, AncientPower, Harden |
| Budew | 17 | none | Natural Cure | default | Razor Leaf, Stun Spore, Bullet Seed, Cotton Spore |
| Ponyta | 17 | none | Run Away | default | Flame Wheel, Double Kick, Charm, Charm |
| Vulpix | 18 | Passho Berry | Flash Fire | Modest | Ember, Confuse Ray, Quick Attack, Will-O-Wisp |

Today's team: Budew 8 (default moves). Expected: 100 / 0.10 / 95.

### Youngster Tyler: Route 204 south, optional, single, cap 19

Trap and drain: Barboach's Whirlpool holds the player in while Lotad's Leech Seed and Psyduck's Disable wear it down. Grass and Electric types break it.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Wingull | 17 | none | Gluttony | default | Wing Attack, Water Pulse, Supersonic, Roost |
| Lotad | 17 | none | Swift Swim | default | Bullet Seed, Water Gun, Leech Seed, Sweet Scent |
| Psyduck | 17 | none | Damp | default | Water Pulse, Psybeam, Disable, Scratch |
| Barboach | 18 | Oran Berry | Swift Swim | Adamant | Whirlpool, Mud Bomb, Water Pulse, Amnesia |

Today's team: Magikarp 11 (default moves). Expected: 100 / 0.10 / 93.

### Bug Catcher Brandon: Route 204 north, optional, single, cap 19

Five evolved and evolving Bugs; Beautifly's Silver Wind behind a SilverPowder is the danger, Stun Spore and Poison Sting the chip. Fire and Flying types sweep it.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Combee | 15 | none | Honey Gather | default | Gust, Bug Bite, Air Cutter |
| Nincada | 16 | none | Compound Eyes | default | Fury Swipes, Leech Life, Harden, Mud-Slap |
| Kricketune | 16 | none | Hyper Cutter | default | Fury Cutter, Leech Life, Growl, Aerial Ace |
| Dustox | 17 | none | Tinted Lens | default | Confusion, Gust, Poison Sting, Protect |
| Beautifly | 18 | SilverPowder | Tinted Lens | Modest | Silver Wind, Giga Drain, Stun Spore, Gust |

Today's team: Wurmple 15 (Tackle, String Shot, Poison Sting, Bug Bite), Silcoon 15 (Bug Bite, Iron Defense, Tackle). Expected: 100 / 0.15 / 92.

### Aroma Lady Taylor: Route 204 north, on the path, single, cap 19

Sleep, then drain: Tangela's Sleep Powder and Giga Drain, with Leech Seed and Wrap around it. It rehearses Gardenia's sleep alone. The answer is a Fire or Flying type that moves first, or a spare member to sleep.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Cherubi | 16 | none | Chlorophyll | default | Leech Seed, Razor Leaf, Tackle, Synthesis |
| Bellsprout | 17 | none | Chlorophyll | default | Vine Whip, Bullet Seed, Magical Leaf, Growth |
| Oddish | 17 | none | Chlorophyll | default | Acid, Razor Leaf, Bullet Seed, PoisonPowder |
| Tangela | 18 | Oran Berry | Leaf Guard | default | Sleep Powder, Giga Drain, AncientPower, Leech Seed |

Today's team: Turtwig 13 (Razor Leaf, Withdraw, Tackle), Cherubi 13 (Bullet Seed, Growth, Leech Seed, Synthesis). Expected: 100 / 0.5 / 82; my simulator lost 6 fights in 100 to the sleep, which the scorer's player should handle better.

### Twins Liv & Liz: Route 204 north, optional, double, cap 19

Plus and Minus twins: Helping Hand behind Spark, Thunder Wave from Plusle, and Pachirisu's Adaptability Spark. A Ground type shuts the whole fight off, which is the lesson.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Plusle | 16 | none | Plus | default | Spark, Helping Hand, Quick Attack, Thunder Wave |
| Minun | 16 | none | Minus | default | Spark, Helping Hand, Quick Attack, Swift |
| Pachirisu | 17 | Oran Berry | Adaptability | Modest | Spark, Bite, Quick Attack, Charm |

Today's team: Pachirisu 15 (Thunder Wave, Spark, Quick Attack, Charm), Pichu 15 (Thunder Wave, Charm, ThunderShock). Expected: not readable yet (a double); built a notch softer than its neighbours.

### Galactic Grunt (1): Floaroma Meadow, on the path, single, cap 19

Paralysis, then bite: Ekans's Glare and Intimidate, Murkrow's Pursuit on the player who switches, Croagunk's Brick Break.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Zubat | 17 | none | Inner Focus | default | Bite, Leech Life, Astonish, Supersonic |
| Murkrow | 18 | none | Insomnia | default | Peck, Astonish, Pursuit, Confuse Ray |
| Croagunk | 17 | none | Dry Skin | default | Poison Sting, Brick Break, Mud-Slap, Astonish |
| Ekans | 18 | Oran Berry | Intimidate | Adamant | Glare, Bite, Poison Sting, Rock Tomb |

Today's team: Ekans 15 (Glare, Bide, Screech, Poison Fang). Expected: 100 / 0.10 / 95.

### Galactic Grunt (2): Floaroma Meadow, on the path, single, cap 19

Fake Out and Pursuit: Glameow takes the first turn, Stunky punishes the switch that follows, and Zubat drains with Leech Life.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Glameow | 17 | none | Limber | default | Fake Out, Scratch, Bite, Growl |
| Poochyena | 17 | none | Quick Feet | default | Bite, Howl, Tackle, Sucker Punch |
| Stunky | 18 | none | Aftermath | default | Leer, Fury Swipes, Screech, Pursuit |
| Zubat | 18 | Oran Berry | Inner Focus | Jolly | Leech Life, Bite, Aerial Ace, Astonish |

Today's team: Zubat 15 (Bite, Supersonic, Astonish, Pluck), Poochyena 15 (Bite, Howl, Sand-Attack). Expected: 100 / 0.20 / 89.

### Galactic Grunt (3): Valley Windworks, outside, on the path, single, cap 19

Yawn forces a switch or a nap; Poison Gas and Sludge chip what comes in.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Koffing | 16 | none | Levitate | default | Smog, Tackle, Screech, Scary Face |
| Grimer | 16 | none | Stench | default | Pound, Mud-Slap, Harden, Disable |
| Gulpin | 18 | Oran Berry | Gluttony | default | Yawn, Sludge, Pound, Amnesia |

Today's team: Gulpin 14 (Poison Gas, Sludge, Yawn, Pound). Expected: 100 / 0.35 / 80.

### Galactic Grunt (4): Valley Windworks, on the path, single, cap 19

Poison that lasts: Toxic from Grimer, Poison Gas and Smog from Koffing, Pursuit on Croagunk.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Grimer | 17 | none | Stench | default | Toxic, Pound, Mud-Slap, Harden |
| Croagunk | 17 | none | Dry Skin | default | Poison Sting, Faint Attack, Pursuit, Mud-Slap |
| Koffing | 18 | Oran Berry | Levitate | default | Smog, Assurance, Scary Face, Tackle |

Today's team: Grimer 15 (Poison Gas, Pound, Harden, Mud-Slap). Expected: 100 / 0.15 / 89.

### Galactic Officer Somnu: Valley Windworks, on the path, single, named officer, cap 19

Ian's Somnu kept to her idea: Toxic Spikes, then Yawn and stall. Built to the boss standard, since goal 3 reads her as a named Galactic fight. Swalot is the danger; Steenee, Pawmo and Geodude answer it.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Pineco | 18 | Oran Berry | Sturdy | Relaxed | Toxic Spikes, Rock Slide, Bug Bite, Protect |
| Eevee | 18 | Silk Scarf | Run Away | Jolly | Covet, Swift, Fake Tears, Charm |
| Barboach | 18 | Passho Berry | Swift Swim | Adamant | Water Pulse, Mud Bomb, Spark, Rock Tomb |
| Swalot | 19 | Sitrus Berry | Gluttony | Calm | Yawn, Dream Eater, Sludge Bomb, Giga Drain |

Today's team: Pineco 16 (Toxic Spikes, Pain Split, Bug Bite, String Shot), Barboach 18 (Spark, Water Gun, Mud Bomb, Amnesia), Eevee 16 (Mud-Slap, Rest, Snore, Fake Tears), Gulpin 17 (Amnesia, Sludge, Yawn, Dream Eater). Expected: about 96 / 1.6 / 5; read by the scorer later. Dream Eater is the split's one conditional attack, exempt from the ceiling by Ian's ruling.

### Mars 1: Valley Windworks, on the path, single, boss, cap 19

Status from the lead and a deliberate hole: Bronzor opens with Hypnosis but only Confusion to attack, so Vullaby walls it; behind it Golbat's Toxic, Gligar's Dig and Rock Slide, Croagunk's Poison Jab and Brick Break, and Purugly with Fake Out, Facade and Thunderbolt for the Water types.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Bronzor | 18 | Sitrus Berry | Levitate | Calm | Hypnosis, Confusion, Imprison, Confuse Ray |
| Golbat | 18 | Oran Berry | Inner Focus | Jolly | Leech Life, Air Cutter, Bite, Toxic |
| Gligar | 18 | Soft Sand | Hyper Cutter | Adamant | Dig, Rock Slide, Aerial Ace, Knock Off |
| Croagunk | 18 | Coba Berry | Dry Skin | Adamant | Brick Break, Poison Jab, Sucker Punch, Rock Tomb |
| Purugly | 19 | Lum Berry | Thick Fat | Adamant | Fake Out, Facade, Thunderbolt, Shadow Claw |

Today's team: Meowth 18 (Bite, Screech, Fake Out, Fury Swipes), Zubat 18 (Wing Attack, Supersonic, Poison Sting, Bite), Bronzor 18 (Sitrus Berry; Hypnosis, Confusion, Confuse Ray, Calm Mind), Purugly 19 (Oran Berry; Faint Attack, Scratch, Fake Out, Hypnosis). Expected: about 96 / 1.5 / 13; read by the scorer later.

### Camper Jacob: Route 205 south, optional, single, cap 26

Fire types with Fighting cover: Monferno's Mach Punch and Rock Tomb behind a Charcoal Flame Wheel. Water and Rock types answer.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Growlithe | 24 | none | Intimidate | default | Flame Wheel, Bite, Leer, Roar |
| Ponyta | 24 | none | Run Away | default | Flame Wheel, Stomp, Double Kick, Charm |
| Houndour | 24 | none | Early Bird | default | Smog, Bite, Ember, Howl |
| Monferno | 25 | Charcoal | Blaze | Naive | Mach Punch, Flame Wheel, Rock Tomb, Taunt |

Today's team: Chimchar 15 (Ember, Taunt, Fury Swipes). Expected: 100 / 0.40 / 80.

### Hiker Daniel: Route 205 south, optional, single, cap 26

Rock Slide on three members, aimed at the Fire, Flying and Bug types this split's box leans on; Baltoy's Psybeam covers the Fighting types. Water and Grass types beat it.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Baltoy | 25 | none | Levitate | default | Psybeam, Rock Tomb, Rapid Spin, Harden |
| Sandshrew | 24 | none | Rough Skin | default | Rock Slide, Poison Sting, Rapid Spin, Defense Curl |
| Phanpy | 24 | none | Pickup | default | Rollout, Focus Energy, Take Down, Ice Shard |
| Graveler | 25 | Hard Stone | Sturdy | Adamant | Rock Slide, Magnitude, Rollout, Defense Curl |

Today's team: Baltoy 15 (Psybeam, Rock Tomb, Rapid Spin, Mud-Slap), Phanpy 15 (Growl, Defense Curl, Rollout, Take Down), Sandshrew 15 (Scratch, Defense Curl, Sand-Attack, Poison Sting). Expected: 100 / 0.10 / 96, on the soft side.

### Aroma Lady Elizabeth: Route 205 south, optional, single, cap 26

Sunny Day for her own Vulpix: Sunflora sets the sun, Gloom sleeps, and a Charcoal Flamethrower comes in at one and a half times. Five turns of sun, then it fades.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Sunflora | 24 | none | Solar Power | default | Sunny Day, Mega Drain, Bullet Seed, Ingrain |
| Gloom | 24 | none | Chlorophyll | default | Sleep Powder, Acid, Mega Drain, Synthesis |
| Vulpix | 25 | Charcoal | Flash Fire | Modest | Flamethrower, Quick Attack, Confuse Ray, Will-O-Wisp |

Today's team: Roselia 16 (Leech Seed, Mega Drain, Stun Spore). Expected: 100 / 0.10 / 92.

### Camper Zackary: Route 205 south, optional, single, cap 26

Fire, Water and Ice from one team: Castform's three attacks, a Vulpix, a Wingull, and an Adaptability Snover whose Avalanche and Icy Wind hit Flying and Grass types.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Castform | 24 | none | Forecast | default | Water Pulse, Ember, Powder Snow, Tackle |
| Wingull | 24 | none | Gluttony | default | Water Pulse, Wing Attack, Supersonic, Mist |
| Vulpix | 24 | none | Flash Fire | default | Flamethrower, Confuse Ray, Quick Attack, Will-O-Wisp |
| Snover | 25 | Oran Berry | Adaptability | Adamant | Razor Leaf, Icy Wind, Avalanche, Mist |

Today's team: Castform 15 (Rain Dance, Water Pulse, Powder Snow). Expected: 100 / 0.15 / 92.

### Picnicker Siena: Route 205 south, optional, single, cap 26

Electric types for the Flying and Water types: a Magnet Spark on Luxio, Pursuit on Linoone, Helping Hand and Thunder Wave from Plusle.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Plusle | 23 | none | Plus | default | Spark, Helping Hand, Quick Attack, Thunder Wave |
| Linoone | 24 | none | Gluttony | default | Headbutt, Pursuit, Tail Whip, Growl |
| Electrike | 24 | none | Lightning Rod | default | Spark, Quick Attack, Howl, Signal Beam |
| Pachirisu | 24 | none | Adaptability | default | Spark, Bite, Quick Attack, Charm |
| Luxio | 25 | Magnet | Hyper Cutter | Adamant | Spark, Bite, Quick Attack, Leer |

Today's team: Zigzagoon 15 (Sand-Attack, Tickle, Headbutt), Electrike 15 (Thunder Fang, Thunder Wave, Leer, Howl). Expected: 100 / 0.40 / 85.

### Hiker Nicholas: Route 205 south, optional, single, cap 26

Rock Head and Rock Slide: three bruisers that hit the Fire and Flying types hard. Water and Grass types beat it.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Cubone | 25 | none | Rock Head | default | Bonemerang, Headbutt, Rock Slide, Leer |
| Rhyhorn | 25 | none | Lightning Rod | default | Horn Attack, Stomp, Rock Slide, Scary Face |
| Graveler | 25 | Oran Berry | Rock Head | Adamant | Rock Slide, Magnitude, Rollout, Defense Curl |

Today's team: Cubone 16 (Tail Whip, Bone Club, Headbutt, Leer). Expected: 100 / 0.15 / 97, on the soft side.

### Battle Girl Kelsey: Route 205 south, optional, single, cap 26

Fighting types with Psychic cover: Meditite's Pure Power doubles a Black Belt Psycho Cut and Brick Break, Makuhita opens with Fake Out.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Mankey | 23 | none | Vital Spirit | default | Karate Chop, Low Kick, Fury Swipes, Leer |
| Machop | 24 | none | Guts | default | Karate Chop, Low Kick, Rock Slide, Leer |
| Makuhita | 24 | none | Thick Fat | default | Fake Out, Arm Thrust, Vital Throw, Knock Off |
| Riolu | 24 | none | Adaptability | default | Quick Attack, Force Palm, Counter, Endure |
| Meditite | 25 | Black Belt | Pure Power | Jolly | Bullet Punch, Psycho Cut, Brick Break, Foresight |

Today's team: Meditite 16 (Meditate, Confusion, Detect, Hidden Power). Expected: 100 / 0.05 / 96.

### Picnicker Karina: Route 205 south, optional, single, cap 26

Three starters' middle stages, each with a coverage move: Croconaw's Ice Fang, Marshtomp's Ancient Power, Grotle's Bite.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Prinplup | 25 | none | Swift Swim | default | BubbleBeam, Metal Claw, Peck, Growl |
| Grotle | 25 | none | Shell Armor | default | Razor Leaf, Bite, Giga Drain, Withdraw |
| Marshtomp | 25 | none | Torrent | default | Mud Bomb, AncientPower, Water Gun, Protect |
| Croconaw | 25 | Mystic Water | Torrent | Adamant | Ice Fang, Bite, Water Gun, AncientPower |

Today's team: Piplup 16 (Bubble, Peck, Yawn). Expected: 100 / 0.05 / 98, the softest of the split; this box answers Water and Grass types easily.

### Bug Catcher Jack: Eterna Forest, on the path, tag, with Lass Briana, cap 26

Butterfree's Compound Eyes Sleep Powder beside a Swords Dance Ninjask and a Pursuit Beedrill.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Beedrill | 23 | none | Swarm | default | Swift, Twineedle, Focus Energy, Pursuit |
| Butterfree | 23 | Oran Berry | Compound Eyes | Modest | Sleep Powder, Confusion, Gust, Silver Wind |
| Ninjask | 24 | none | Speed Boost | default | Fury Cutter, Leech Life, Sand-Attack, Swords Dance |

Today's team: Kakuna 16 (Bug Bite, Iron Defense, Poison Sting), Cascoon 16 (Tackle, String Shot, Poison Sting, Bug Bite), Metapod 16 (Bug Bite, Poison Sting, Iron Defense). Expected: not readable yet (a tag battle).

### Lass Briana: Eterna Forest, on the path, tag, with Bug Catcher Jack, cap 26

Redirection: Clefairy's Follow Me draws the attacks while Vigoroth hits and Marill helps.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Clefairy | 23 | none | Magic Guard | default | Follow Me, Encore, Magical Leaf, Helping Hand |
| Marill | 23 | none | Huge Power | default | BubbleBeam, Rollout, Charm, Helping Hand |
| Vigoroth | 24 | Oran Berry | Vital Spirit | Jolly | Slash, Fury Swipes, Encore, Uproar |

Today's team: Slakoth 17 (Scratch, Yawn, Encore, Slack Off). Expected: not readable yet (a tag battle).

### Psychic Lindsey: Eterna Forest, on the path, tag, with Psychic Elijah, cap 26

Hypnosis and Confuse Ray, then Kirlia's Calm Mind.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Exeggcute | 23 | none | Chlorophyll | default | Bullet Seed, AncientPower, Leech Seed, Hypnosis |
| Natu | 23 | none | Magic Guard | default | Night Shade, Peck, Faint Attack, Confuse Ray |
| Kirlia | 24 | Oran Berry | Synchronize | Modest | Confusion, Magical Leaf, Shadow Sneak, Calm Mind |

Today's team: Exeggcute 17 (Hypnosis, Reflect, Leech Seed, Bullet Seed). Expected: not readable yet (a tag battle).

### Psychic Elijah: Eterna Forest, on the path, tag, with Psychic Lindsey, cap 26

Kadabra's Psybeam behind Wynaut's Counter and Mirror Coat. Wynaut has Telepathy (its hidden slot) rather than Shadow Tag, since a trapping ability stays off the path.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Spoink | 23 | none | Thick Fat | default | Psybeam, Icy Wind, Payback, Magic Coat |
| Wynaut | 23 | none | Telepathy | default | Counter, Mirror Coat, Safeguard, Encore |
| Kadabra | 24 | Oran Berry | Inner Focus | Timid | Psybeam, Confusion, Disable, Reflect |

Today's team: Wynaut 17 (Counter, Mirror Coat, Safeguard, Destiny Bond). Expected: not readable yet (a tag battle).

### Bug Catcher Phillip: Eterna Forest, optional, tag, with Bug Catcher Donald, cap 26

Speed: Yanma and Ninjask with Speed Boost, Dustox's Confusion.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Yanma | 23 | none | Speed Boost | default | Quick Attack, SonicBoom, Endure, Screech |
| Dustox | 23 | none | Tinted Lens | default | Confusion, Gust, Poison Sting, Protect |
| Ninjask | 24 | none | Speed Boost | default | Leech Life, Fury Cutter, Aerial Ace, Swords Dance |

Today's team: Nincada 17 (Harden, Leech Life, Sand-Attack, Fury Swipes), Butterfree 17 (PoisonPowder, Confusion, Sleep Powder, Gust), Dustox 19 (Bug Bite, Confusion, Gust, Protect). Expected: not readable yet (a tag battle).

### Bug Catcher Donald: Eterna Forest, optional, tag, with Bug Catcher Phillip, cap 26

Bulky Bugs: Pineco's Rapid Spin, Skorupi's Knock Off, Vespiquen's Power Gem.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Pineco | 23 | none | Sturdy | default | Bug Bite, Rapid Spin, Take Down, Protect |
| Skorupi | 23 | none | Battle Armor | default | Knock Off, Bite, Poison Sting, Screech |
| Vespiquen | 24 | Oran Berry | Tinted Lens | default | Power Gem, Fury Cutter, Poison Sting, Confuse Ray |

Today's team: Pineco 17 (Selfdestruct, Bug Bite, Take Down, Rapid Spin), Combee 19 (Sweet Scent, Gust, Bug Bite). Expected: not readable yet (a tag battle).

### Psychic Kody: Eterna Forest, optional, tag, with Psychic Rachael, cap 26

Yawn and Disable, with Poison Gas from Drowzee.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Slowpoke | 24 | none | Oblivious | default | Yawn, Confusion, Water Pulse, Tackle |
| Drowzee | 23 | none | Insomnia | default | Confusion, Headbutt, Disable, Poison Gas |
| Spoink | 23 | none | Thick Fat | default | Psybeam, Icy Wind, Payback, Magic Coat |

Today's team: Slowpoke 18 (Yawn, Growl, Water Gun, Confusion). Expected: not readable yet (a tag battle).

### Psychic Rachael: Eterna Forest, optional, tag, with Psychic Kody, cap 26

Wrap and Confusion: Chingling holds one target in while Meditite and Kadabra hit it.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Chingling | 23 | none | Levitate | default | Confusion, Swift, Astonish, Growl |
| Meditite | 24 | none | Pure Power | default | Confusion, Bullet Punch, Foresight, Endure |
| Kadabra | 24 | Oran Berry | Inner Focus | Timid | Psybeam, Shock Wave, Disable, Knock Off |

Today's team: Chingling 18 (Growl, Recover, Confusion, Uproar). Expected: not readable yet (a tag battle).

### Fisherman Andrew: Route 205 north, optional, single, cap 26

Six fish, five of them small: the fight is Gyarados, whose Intimidate, Bite and Dragon Rage arrive last. The only six-Pokemon ordinary team of the split.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Magikarp | 20 | none | Swift Swim | default | Tackle |
| Goldeen | 22 | none | Swift Swim | default | Horn Attack, Water Pulse, Haze, Peck |
| Remoraid | 22 | none | Hustle | default | Water Gun, Psybeam, Aurora Beam, BubbleBeam |
| Feebas | 22 | none | Swift Swim | default | Tackle, Water Pulse, Mirror Coat, DragonBreath |
| Qwilfish | 23 | none | Poison Point | default | BubbleBeam, Poison Sting, Rollout, Harden |
| Gyarados | 24 | Oran Berry | Intimidate | default | Bite, Water Pulse, Dragon Rage, Icy Wind |

Today's team: Magikarp 8 (default moves), Magikarp 10 (default moves), Magikarp 12 (default moves), Magikarp 12 (default moves), Magikarp 14 (default moves), Feebas 16 (default moves). Expected: 100 / 0.5 / 76.

### Fisherman Joseph: Route 205 north, optional, single, cap 26

Skill Link: Shellder's Icicle Spear always hits five times, the answer to Flying and Grass types. Tentacool's Aurora Beam and Quagsire's Slam beside it.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Tentacool | 25 | none | Clear Body | default | Acid, BubbleBeam, Aurora Beam, Rapid Spin |
| Quagsire | 25 | none | Unaware | default | Mud Shot, Slam, AncientPower, Amnesia |
| Shellder | 25 | NeverMeltIce | Skill Link | Adamant | Icicle Spear, BubbleBeam, Rapid Spin, Razor Shell |

Today's team: Goldeen 18 (Water Sport, Supersonic, Horn Attack, Water Pulse). Expected: 100 / 0.05 / 95, on the soft side.

### Fisherman Zachary: Route 205 north, optional, single, cap 26

Water types that answer their counters: Chinchou's Volt Absorb and Spark, Corphish's Adaptability and Ancient Power, Quagsire's Water Absorb.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Finneon | 24 | none | Swift Swim | default | Water Pulse, Gust, Psybeam, Attract |
| Quagsire | 24 | none | Unaware | default | Slam, Mud Shot, AncientPower, Amnesia |
| Chinchou | 25 | Magnet | Volt Absorb | Modest | Spark, Water Pulse, Confuse Ray, Take Down |
| Corphish | 25 | Oran Berry | Adaptability | Adamant | BubbleBeam, ViceGrip, Knock Off, AncientPower |

Today's team: Finneon 18 (Water Gun, Attract, Rain Dance, Gust), Corphish 18 (Bubble, Harden, ViceGrip, Knock Off), Chinchou 19 (Thunder Wave, Shock Wave, Water Gun, Confuse Ray). Expected: 100 / 0.10 / 96, on the soft side.

### Aroma Lady Jenna: Eterna Gym, gym trainer, single, cap 26

Sun and sleep together, the gym's rehearsal: Gloom sets Sunny Day and sleeps, Exeggutor's Seed Bomb and Nuzleaf's Rock Tomb follow.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Gloom | 25 | Oran Berry | Chlorophyll | default | Sunny Day, Giga Drain, Acid, Sleep Powder |
| Exeggutor | 25 | none | Chlorophyll | default | Seed Bomb, Confusion, AncientPower, Leech Seed |
| Weepinbell | 24 | none | Chlorophyll | default | Vine Whip, Acid, Bullet Seed, Sucker Punch |
| Nuzleaf | 25 | none | Chlorophyll | default | Fake Out, Razor Leaf, Rock Tomb, Payback |

Today's team: Cacnea 23 (Growth, Leech Seed, Grass Knot, Pin Missile), Oddish 23 (PoisonPowder, Stun Spore, Sleep Powder, Mega Drain), Lotad 23 (Nature Power, Water Gun, Natural Gift, Mega Drain). Expected: 100 / 0.30 / 81.

### Lass Caroline: Eterna Gym, gym trainer, single, cap 26

Leech Seed and powders, then Breloom's Mach Punch and Rock Tomb.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Hoppip | 24 | none | Chlorophyll | default | Bullet Seed, Leech Seed, Stun Spore, Synthesis |
| Skiploom | 25 | Oran Berry | Chlorophyll | default | Sleep Powder, Bullet Seed, Leech Seed, Tackle |
| Breloom | 25 | none | Technician | Adamant | Mach Punch, Rock Tomb, Bullet Seed, Headbutt |

Today's team: Hoppip 22 (Stun Spore, Sleep Powder, Bullet Seed, Leech Seed), Skiploom 23 (PoisonPowder, Stun Spore, Leech Seed, Bullet Seed). Expected: 100 / 0.25 / 86.

### Aroma Lady Angela: Eterna Gym, gym trainer, single, cap 26

Spikes from Roselia, Gardenia's hazard previewed, with Ludicolo and Lileep as the off-type answers to Fire and Flying types.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Sunflora | 25 | none | Solar Power | default | Sunny Day, Giga Drain, Bullet Seed, Ingrain |
| Roselia | 25 | Oran Berry | Natural Cure | default | Spikes, Mega Drain, Poison Sting, Stun Spore |
| Ludicolo | 25 | none | Swift Swim | default | Icy Wind, Giga Drain, Fake Out, Water Pulse |
| Lileep | 25 | none | Solid Rock | default | Rock Slide, Giga Drain, AncientPower, Confuse Ray |

Today's team: Sunflora 23 (Mega Drain, Leech Seed, Ingrain, Synthesis). Expected: 100 / 0.40 / 86.

### Beauty Lindsay: Eterna Gym, gym trainer, single, cap 26

Spikes and sleep together: Roselia lays Spikes, Bellsprout sleeps, Shiftry's Fake Out and Rock Slide close.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Roselia | 25 | Black Sludge | Natural Cure | Calm | Spikes, Giga Drain, Poison Sting, Stun Spore |
| Bellsprout | 24 | none | Chlorophyll | default | Bullet Seed, Vine Whip, Sleep Powder, Growth |
| Tangela | 25 | none | Chlorophyll | default | Giga Drain, AncientPower, PoisonPowder, Leech Seed |
| Shiftry | 25 | none | Chlorophyll | default | Fake Out, Razor Leaf, Rock Slide, Faint Attack |

Today's team: Roselia 19 (Mega Drain, Poison Sting, Stun Spore). Expected: 100 / 0.10 / 95.

### Gardenia: Eterna Gym, on the path, single, boss, cap 26

Spikes and sleep from the lead, then off-type answers to the Fire and Flying types a Grass gym invites: Ludicolo's Ice Beam and Water Pulse, Exeggutor's Psychic and Ancient Power, Breloom's Rock Tomb behind a Coba Berry, and a Roserade ace with Growth. No sun; see the decisions.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Roselia | 24 | Black Sludge | Natural Cure | Timid | Spikes, Sleep Powder, Giga Drain, Extrasensory |
| Ludicolo | 25 | Sitrus Berry | Swift Swim | Calm | Ice Beam, Water Pulse, Giga Drain, Fake Out |
| Exeggutor | 25 | Leftovers | Chlorophyll | Modest | Psychic, Giga Drain, AncientPower, Leech Seed |
| Breloom | 25 | Coba Berry | Technician | Adamant | Mach Punch, Rock Tomb, Bullet Seed, Stun Spore |
| Roserade | 26 | Lum Berry | Natural Cure | Modest | Sludge Bomb, Giga Drain, Shadow Ball, Cotton Spore |

Today's team: Cherrim 25 (Heat Rock; SolarBeam, Leech Seed, Sunny Day, Weather Ball), Lumineon 25 (Watmel Berry; Aqua Tail, Natural Gift, Silver Wind, Swagger), Shiftry 25 (Occa Berry; SolarBeam, Rock Tomb, Natural Gift, Faint Attack), Breloom 25 (Lum Berry; Mach Punch, Bullet Seed, Stun Spore, Rock Tomb), Roserade 26 (Poison Barb; Sludge Bomb, Mega Drain, Weather Ball, Stun Spore). Expected: about 90 / 3.0 / 2; read by the scorer later.

### Bird Keeper Alexandra: Route 211 west, optional, single, cap 26

Five fliers with Pursuit for the switch and Swablu's Sing; Staravia's Sharp Beak Aerial Ace is the danger. Rock and Electric types answer.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Taillow | 23 | none | Guts | default | Wing Attack, Quick Attack, Focus Energy, Pursuit |
| Swablu | 24 | none | Natural Cure | default | Peck, Sing, Swift, Safeguard |
| Noctowl | 24 | none | Insomnia | default | Wing Attack, Confusion, Reflect, Peck |
| Murkrow | 24 | none | Insomnia | default | Wing Attack, Faint Attack, Pursuit, Astonish |
| Staravia | 25 | Sharp Beak | Reckless | Jolly | Aerial Ace, Quick Attack, Steel Wing, Pursuit |

Today's team: Swablu 19 (Astonish, Sing, Fury Attack, Safeguard), Staravia 20 (Quick Attack, Wing Attack, Double Team, Endeavor). Expected: 100 / 0.15 / 90.

### Ninja Boy Zach: Route 211 west, optional, single, cap 26

Speed Boost behind Protect: Ninjask grows faster each turn, Breloom and Nuzleaf strike first with priority and Fake Out.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Nuzleaf | 24 | none | Chlorophyll | default | Fake Out, Razor Leaf, Payback, Rock Tomb |
| Parasect | 24 | none | Dry Skin | default | Leech Life, Cross Poison, Stun Spore, Slash |
| Breloom | 24 | none | Technician | default | Mach Punch, Bullet Seed, Rock Tomb, Headbutt |
| Ninjask | 25 | Oran Berry | Speed Boost | default | Leech Life, Aerial Ace, Fury Cutter, Protect |

Today's team: Shroomish 19 (Tackle, Stun Spore, Leech Seed, Mega Drain), Paras 19 (Stun Spore, PoisonPowder, Bug Bite, Spore), Seedot 19 (Leech Seed, Harden, Bullet Seed, Nature Power). Expected: 100 / 0.35 / 85.

### Hiker Louis: Route 211 west, optional, single, cap 26

Few weaknesses: Sableye has none in this box, Mawile and Bronzor resist most of it.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Sableye | 25 | none | Clear Body | default | Shadow Claw, Knock Off, Fake Out, Astonish |
| Mawile | 24 | none | Intimidate | default | Bite, ViceGrip, Sucker Punch, Fake Tears |
| Bronzor | 25 | Oran Berry | Levitate | default | Confusion, Rock Tomb, Extrasensory, Confuse Ray |

Today's team: Sableye 19 (Night Shade, Astonish, Fury Swipes, Fake Out), Mawile 19 (Astonish, Fake Tears, Bite, Sweet Scent). Expected: 100 / 0.30 / 83.


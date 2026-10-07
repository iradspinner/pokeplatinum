# The comb: Roark's split, redone

This is the second comb of Roark's split, rebuilt on 2026-10-06 to Ian's
answers and verdict of 2026-10-04 (`../../ians-answers-2026-10-04.md`). It
replaces the first comb of 2026-10-03, which Ian judged far too soft. Every
ordinary trainer now carries three to five Pokemon one or two levels under the
cap in force, with TM and tutor moves where they serve the idea; Barry 2 has
four Pokemon and Roark five, built to read about 93 and 90 percent won. All 22
files pass the checker (Oxide species, items, natures, ability slots, legal
moves including TM and tutor lists, no one-hit KO move, levels at or under the
cap in force). The files sit beside this one, named as in
`res/trainers/data/`.

None of these teams has been read by the scorer. The expected numbers come
from a rough simulator of my own (`../tools/sim.py`), checked against three
fights the scorer has read; the last section says how far to trust it.

Oreburgh's gym fights in permanent sand (Ian, 2026-10-06: a map's weather is
battle weather for every fight on it), so Youngsters Jonathon and Darius and
Roark himself fight in sand. Their teams are Rock types, which take no chip
and gain half again their Special Defense in it, while the player's other
types lose a sixteenth of their HP a turn. No Sand Veil sits in the gym, so
the evasion rule is untouched. The teams stand as Ian ruled; only the
readings move. The expected numbers below were made without the sand; my
simulator now reads the gym in it, against the same box:

| Trainer | Without sand | In sand |
|---|---|---|
| Youngster Jonathon, blind | 100 / 0.31 / 70 (about 88 clean in the scorer's terms) | 100 / 0.62 / 42 (about 77) |
| Youngster Darius, blind | 100 / 0.26 / 77 (about 91) | 99.9 / 0.41 / 71 (about 88) |
| Roark, planned six | 86 / 2.86 / 1 | 83 / 3.37 / 0 |

Jonathon drops just under Ian's 80 to 85 clean and Roark reads about three
points harder. I recommend leaving both: the scorer's reading of the gym in
sand, which the scoring track is fixing now, is the check, and if Jonathon
reads too hard there, his Lileep drops a level. No other map in this split
has its own weather.

## Decisions Ian should check

Each decision is a check: what the files do today, how to verify it, and
what Ian decides. Two of the checks run on the scorer's readings, which the
scoring track is taking now; the rest run on the files themselves. Every
file passes `python3 out/tools/oxide.py check <cap> <file>` and
`python3 out/tools/comb_roark.py`, which rebuilds the files and prints a line
for any illegal move, level over the cap, or attack over the ceiling in
decision 3; it prints none today.

| # | Decision | What the files do today | How it is checked | What Ian decides |
|---|---|---|---|---|
| 1 | Boss targets | Roark is built to read about 90 percent won and Barry 2 about 93; my simulator reads them at 91 and 93. | The scorer's team-search readings of `leader_roark.json` and `rival_route_203_piplup.json`: each passes at 95 or under and within five points of its target. | Whether 90 for the first gym and 93 for the rival are the right spikes. I recommend yes. If Roark reads too soft, its four non-ace members rise a level; if too hard, Lileep loses Recover. |
| 2 | Barry 2's cost | He costs about three of the player's Pokemon a fight, mostly to Munchlax (Thick Fat, Rock Tomb), a wall the level-11 box barely dents. | The same reading's faints, and where they fall: Munchlax should make most of the knockouts. | Keep it (my recommendation, since you set bosses by win rate and asked for lethality), or take the alternative: Munchlax at 9 with Amnesia for Rock Tomb, which my simulator reads at the same win rate (91) and about 1.6 faints. |
| 3 | A ceiling on borrowed attacks | No egg, TM or tutor attack above 75 power on an ordinary trainer, or above 90 on Barry 2 and Roark. Level-up moves are not limited, so Snubbull keeps its level-1 Thunder Fang. | `comb_roark.py` flags any attack over the ceiling; it flags none. | Keep the ceiling (recommended; without it a level-9 Abra could carry Psychic and a level-14 Geodude Thunder Punch) or drop it. |
| 4 | Rock and Ground trainers read softest | Mason, a Rock and Ground team with a Fighting danger member, is the softest fight at about 90 clean; the gym trainers carry a Water answer (Lileep, Kabuto). | The scorer's blind readings of the mine and gym trainers against your 80 to 85 clean. | Accept Mason on the soft side (recommended, since Water types are the niche this split rewards) or sharpen it. |
| 5 | The school kids are optional | Harrison and Christine are built as optional route trainers at cap 11. | `trainers.csv` gives their path as "unknown". | Whether either is on the path. Their teams do not change either way. |
| 6 | Roark's Geodude has no Water move | Geodude holds a Passho Berry and has Sturdy, so it survives a Water hit to curl and roll; it has no move that hits Water types. | Roark's reading: Geodude should make a share of the knockouts. In my simulator it made about a quarter. | Accept (recommended) or give it Thunder Punch, which my simulator read softer (about 96 won) because its turns went to Thunder Punch instead of Rollout. |
| 7 | The Jubilife grunts | Built for Gardenia's split at cap 19 as a tag pair: three Pokemon each, at 16 and 17. | `trainers.csv` row 23 lists them in Gardenia's split as a tag battle. The scorer cannot read a tag battle yet. | Whether three each suits a tag fight. They come back with Gardenia's split. |

## Overview

The cap is 11 until Barry 2 is beaten and 16 after him. Barry 1 and Lucas
and Dawn 1 stay as they are, by Ian's rulings (the first does not count in a
run, the second is trivial). Walking order puts the mine before the gym, as
the story sends the player to Roark in the mine first. Expected numbers are
won / faints a fight / clean, at real odds.

| Trainer | Place | Path | Size | Levels | The idea | Expected |
|---|---|---|---|---|---|---|
| Youngster Tristan | Route 202 | required | 3 | 9 | first strike | 100 / 0.10 / 89 |
| Youngster Logan | Route 202 | required | 4 | 8 to 10 | poison stingers, then the hornet | 100 / 0.15 / 83 |
| Lass Natalie | Route 202 | required | 3 | 10 | curl, then roll | 100 / 0.15 / 81 |
| School Kid Harrison | Trainers' School | optional | 3 | 9 to 10 | a paralysis lesson | 100 / 0.20 / 81 |
| School Kid Christine | Trainers' School | optional | 4 | 9 | a Disable lesson | 100 / 0.15 / 85 |
| Barry 2 | Route 203 | required, boss | 4 | 10 to 11 | complete sets, a wall, his starter last | 93 / 3.0 / 0 |
| Youngster Michael | Route 203 | optional | 4 | 14 to 15 | they heal as they hit | 100 / 0.20 / 90 |
| Lass Madeline | Route 203 | optional | 3 | 14 | Water types that confuse | 100 / 0.15 / 84 |
| Lass Kaitlin | Route 203 | optional | 5 | 13 to 14 | Intimidate first, then a special hitter | 100 / 0.15 / 85 |
| Youngster Dallas | Route 203 | optional | 4 | 14 to 15 | Electric types for your Water types | 100 / 0.15 / 88 |
| Youngster Sebastian | Route 203 | optional | 3 | 14 to 15 | Fighting types for your Normal and Rock types | 100 / 0.10 / 87 |
| Camper Curtis | Oreburgh Gate | optional | 4 | 13 to 14 | Poison Point punishes contact | 100 / 0.20 / 79 |
| Picnicker Diana | Oreburgh Gate | optional | 4 | 13 to 15 | Technician | 100 / 0.25 / 82 |
| Worker Colin | Oreburgh Mine | optional | 4 | 14 to 15 | Sturdy walls with Machop behind them | 100 / 0.15 / 83 |
| Worker Mason | Oreburgh Mine | optional | 5 | 15 | a Fighting type among the diggers | 100 / 0.10 / 90 |
| Youngster Jonathon | Oreburgh Gym | optional | 3 | 13 to 15 | Roark's lead, rehearsed | 100 / 0.15 / 77 |
| Youngster Darius | Oreburgh Gym | optional | 4 | 14 to 15 | Roark's ace, rehearsed | 100 / 0.15 / 84 |
| Roark | Oreburgh Gym | required, boss | 5 | 14 to 16 | the first hazard, two switch taxes, a wall, a setup ace | 90 / 2.3 / 5 |
| Galactic Grunts (two) | Jubilife City | required, tag; Gardenia's split | 3 and 3 | 16 to 17 | spread moves and speed control; Fake Out and sleep | not readable yet |

## The split's shape

Ordinary trainers on Route 202 sit at 8 to 10 against a cap of 11, and from
Route 203 on at 13 to 15 against 16; the gym's two trainers sit at 13 to 15.
Sizes run 3, 4, 3 on Route 202 and vary from 3 to 5 after it. Most ordinary
trainers have one danger member built to the boss standard (a nature, an
item, four moves); Logan's Beedrill and Curtis's Qwilfish go without, since
their species carry them. Ordinary trainers hold up to two items, all
berries except Aipom's Silk Scarf. IVs are 200 on ordinary trainers, 230 on
the gym's trainers and 255 on bosses. No ordinary trainer carries a hazard,
sleep, a forced trade, a trap or a real setup move (only one-stage boosts
such as Harden, Defense Curl and Growth), except the gym trainers, who
rehearse Roark's Stealth Rock, Block and Pursuit. Status runs to two moves a
team at most, and no team pairs paralysis with confusion. About one Pokemon
in six has a priority move.

Every tool Roark uses appears earlier in the split, alone: Rollout behind Defense Curl
(Natalie), Thunder Wave (Harrison), a Grass answer to Water types (Michael),
a resist berry (Darius), Pursuit and Block (the gym trainers), Stealth Rock
(Jonathon). The gym's two trainers show them together.

## Trainer by trainer

### Youngster Tristan: Route 202, on the path, single, cap 11

The game's first ordinary trainer: two Quick Attack users and a fast
Zigzagoon chip the player before Starly closes with Wing Attack, and
Sentret's Adaptability doubles its Normal moves rather than adding half. The
player answers with bulk (Squirtle, Dottler) and by keeping a healthy member
for Starly; it is the softest fight of the split by design.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Zigzagoon | 9 | none | Gluttony | default | Secret Power, Tackle, Tail Whip, Growl |
| Sentret | 9 | none | Adaptability | Jolly | Quick Attack, Scratch, Defense Curl, Charm |
| Starly | 9 | Oran Berry | Keen Eye | Jolly | Quick Attack, Wing Attack, Growl, Tackle |

Today's team: Starly 7 (default moves). Expected: 100 / 0.10 / 89.

### Youngster Logan: Route 202, on the path, single, cap 11

Three cocoon-line Bugs chip with Poison Sting and slow the player with
String Shot, then Beedrill, the danger member with 90 base Attack, arrives
against a slowed team. The answer is a Fire or Psychic type for Beedrill
(Vulpix's Ember, Dottler's Confusion) and a switch to shed the String Shot
drops before it comes. Weedle and Wurmple know only what their lists hold.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Weedle | 8 | none | Shield Dust | default | Poison Sting, String Shot |
| Wurmple | 8 | none | Shield Dust | default | Poison Sting, Tackle, String Shot |
| Kakuna | 9 | none | Shed Skin | default | Poison Sting, Harden, String Shot |
| Beedrill | 10 | none | Swarm | default | Fury Attack, Poison Sting, String Shot, Harden |

Today's team: Burmy 7 (Protect, Bug Bite, String Shot). Expected: 100 / 0.15 / 83.

### Lass Natalie: Route 202, on the path, single, cap 11

Every member curls, then rolls: Defense Curl doubles Rollout, which doubles
again with each hit, and the Simple Bidoof's curl counts twice. The player
must break each roller before its third Rollout, or switch to reset the
chain; Vulpix and Dottler, weak to Rock, should stay out of it.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Spheal | 10 | none | Thick Fat | default | Defense Curl, Rollout, Powder Snow, Water Gun |
| Phanpy | 10 | none | Pickup | default | Defense Curl, Rollout, Tackle, Ice Shard |
| Bidoof | 10 | Oran Berry | Simple | Impish | Defense Curl, Rollout, Tackle, Growl |

Today's team: Bidoof 7 (default moves). Expected: 100 / 0.15 / 81.

### School Kid Harrison: Trainers' School, optional, single, cap 11

A lesson in paralysis: Stun Spore, Static and Thunder Wave slow the player,
Shroomish's Fake Tears softens it, and Abra's Charge Beam comes in behind,
with Encore to lock a careless player into a status move. Abra is frail
(25 base HP), so any member that moves first and hits it ends the lesson.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Shroomish | 9 | none | Poison Heal | default | Stun Spore, Absorb, Tackle, Fake Tears |
| Pichu | 10 | none | Static | default | ThunderShock, Charm, Encore, Tail Whip |
| Abra | 10 | Oran Berry | Inner Focus | Timid | Charge Beam, Thunder Wave, Encore, Knock Off |

Today's team: Abra 8 (Hidden Power). The X Attack stays in the bag.
Expected: 100 / 0.20 / 81.

### School Kid Christine: Trainers' School, optional, single, cap 11

A lesson in Disable: two members lock the player's best move away, and
Meditite's Pure Power doubles a priority Bullet Punch. The player answers by
carrying a second attack on each member, and Rookidee's Peck hits Meditite
for double.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Chingling | 9 | none | Levitate | default | Astonish, Disable, Growl, Wish |
| Natu | 9 | none | Magic Guard | default | Peck, Night Shade, Leer, Faint Attack |
| Ralts | 9 | none | Synchronize | default | Confusion, Disable, Growl, Shadow Sneak |
| Meditite | 9 | Oran Berry | Pure Power | default | Bullet Punch, Confusion, Meditate, Bide |

Today's team: Ralts 8 (Confusion, Growl, Hidden Power). The Potion stays in the bag.
Expected: 100 / 0.15 / 85.

### Barry 2: Route 203, on the path, single, boss, cap 11

Complete sets on four members, his starter last at the interim cap. Starly
carries a Sharp Beak and Pursuit for the player who switches out of it,
Buizel's Brick Break covers Rock and Normal types, and Munchlax (his later
Snorlax) is the wall: Thick Fat halves Vulpix's Ember, and Rock Tomb hits the
Fire and Flying answers. The player's tools are Krabby's Vise Grip, Bidoof's
Simple Defense Curl against the physical hitters, and Dottler's Reflect. The
table is the file read against the three-gym run's box, whose starter was
Piplup; the other two files differ only in the starter.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Starly | 10 | Sharp Beak | Keen Eye | Jolly | Wing Attack, Quick Attack, Pursuit, Steel Wing |
| Buizel | 10 | Oran Berry | Swift Swim | Adamant | Water Gun, Quick Attack, Brick Break, Growl |
| Munchlax | 10 | Oran Berry | Thick Fat | Careful | Tackle, Lick, Defense Curl, Rock Tomb |
| Turtwig | 11 | Oran Berry | Shell Armor | Adamant | Giga Drain, Tackle, Withdraw, Growth |

The other two files: Barry's Chimchar (Ember, Double Kick, Scratch, Leer;
Naive) against a player who took Turtwig, and his Piplup (Water Pulse, Double
Hit, Pound, Growl; Modest) against one who took Chimchar, each level 11 with
an Oran Berry.

Today's team: Starly 10 (Quick Attack, Growl, Wing Attack), Turtwig 11 (Tackle, Withdraw, Absorb). Expected: about 93 / 3.0 / 0;
see decision 2.

### Youngster Michael: Route 203, optional, single, cap 16

They heal as they hit: Leech Life, Giga Drain and Absorb on every member.
Oddish is the danger: its Giga Drain hits the box's Water, Rock and Ground
types for double and heals off them. A six without a Fire or Flying type
struggles to break it, so the player should bring Charmander or Nidorino.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Zubat | 15 | none | Inner Focus | default | Leech Life, Bite, Astonish, Quick Attack |
| Paras | 15 | Oran Berry | Dry Skin | Adamant | Leech Life, Metal Claw, Giga Drain, Stun Spore |
| Budew | 14 | none | Natural Cure | default | Razor Leaf, Absorb, Growth, Synthesis |
| Oddish | 14 | Oran Berry | Chlorophyll | default | Giga Drain, Acid, PoisonPowder, Absorb |

Today's team: Kricketot 9 (Growl, Bide, Bug Bite), Zubat 9 (Leech Life, Supersonic, Astonish, Pluck). Expected: 100 / 0.20 / 90, on the
soft side on average, though my simulator lost two blind sixes in a hundred
to Oddish when they held no Fire type.

### Lass Madeline: Route 203, optional, single, cap 16

Water types that confuse: Confuse Ray, Supersonic, and Psybeam's and Water
Pulse's chance, while Water Absorb on Wooper and Volt Absorb on Chinchou
blunt the obvious Water and Electric answers. Steenee's Razor Leaf hits all
three, and Wooper four times over.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Psyduck | 14 | none | Damp | default | Water Pulse, Psybeam, Confuse Ray, Disable |
| Wooper | 14 | none | Water Absorb | default | Mud Shot, Water Gun, Tail Whip, Double Kick |
| Chinchou | 14 | Oran Berry | Volt Absorb | Modest | Water Pulse, Shock Wave, Supersonic, Bubble |

Today's team: Psyduck 10 (Water Sport, Scratch, Tail Whip, Water Gun). Expected: 100 / 0.15 / 84.

### Lass Kaitlin: Route 203, optional, single, cap 16

Three Intimidate leads cut the player's physical attackers, Will-O-Wisp and
Glare back them up, and Spoink hits from the special side once the player has
committed. The answer is special attackers (Charmander's Ember, Wartortle's
Bubble) and Wartortle's Bite for Spoink. Kaitlin had four Pokemon at 7; she
now has five, the largest ordinary team of the split.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Ekans | 14 | none | Intimidate | default | Bite, Poison Sting, Glare, Leer |
| Growlithe | 14 | none | Intimidate | default | Ember, Bite, Leer, Will-O-Wisp |
| Snubbull | 14 | none | Intimidate | default | Bite, Thunder Fang, Charm, Scary Face |
| Taillow | 13 | none | Guts | default | Wing Attack, Quick Attack, Peck, Growl |
| Spoink | 14 | Oran Berry | Thick Fat | Modest | Psybeam, Shock Wave, Icy Wind, Payback |

Today's team: Growlithe 7 (Bite, Roar, Ember), Sunkern 7 (Mega Drain, Growth), Taillow 7 (Peck, Growl, Focus Energy), Spoink 7 (Hidden Power, Psywave). Roar is gone, since phazing waits for
Maylene's split. Expected: 100 / 0.15 / 85.

### Youngster Dallas: Route 203, optional, single, cap 16

Electric types for the player's Water types, with Fighting coverage for the
Ground types that wall them: Elekid and Pikachu carry Brick Break and Low
Kick (which hits Onix at full weight). Steenee resists Electric and takes
Fighting neutrally, so it is the safest answer.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Shinx | 15 | none | Rivalry | default | Spark, Tackle, Leer, Quick Attack |
| Mareep | 14 | none | Static | default | ThunderShock, Thunder Wave, Tackle, Growl |
| Pikachu | 15 | none | Reckless | default | Shock Wave, Quick Attack, Brick Break, Charm |
| Elekid | 15 | Oran Berry | Static | Naive | Shock Wave, Low Kick, Brick Break, Quick Attack |

Today's team: Shinx 10 (Thunder Fang, Thunder Wave). Thunder Fang is gone; it is an
egg move above the ceiling at this split. Expected: 100 / 0.15 / 88.

### Youngster Sebastian: Route 203, optional, single, cap 16

Fighting types for the player's Normal and Rock types, with Rock Slide on
Machop for the Flying and Fire answers. Nidorino resists Fighting and is the
answer; Bibarel, Onix and Geodude should sit this one out. Three members,
the smallest team after Barry.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Makuhita | 15 | none | Thick Fat | default | Arm Thrust, Vital Throw, Rock Tomb, Knock Off |
| Mankey | 14 | none | Vital Spirit | default | Karate Chop, Covet, Low Kick, Leer |
| Machop | 14 | Oran Berry | Guts | default | Karate Chop, Low Kick, Rock Slide, Leer |

Today's team: Machop 10 (Low Kick, Leer, Karate Chop). Expected: 100 / 0.10 / 87.

### Camper Curtis: Oreburgh Gate, optional, single, cap 16

Poison Point on all four: every contact move risks poison. The answer is
special attackers, Geodude's Magnitude (Ground hits Poison for double) and
Nidorino, which cannot be poisoned. Qwilfish, with 115 base Attack in Oxide,
is the danger even at 13.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Nidoran♀ | 14 | none | Poison Point | default | Double Kick, Poison Sting, Scratch, Tail Whip |
| Nidoran♂ | 14 | Oran Berry | Poison Point | default | Double Kick, Poison Sting, Peck, Leer |
| Roselia | 14 | none | Natural Cure | default | Mega Drain, Poison Sting, Stun Spore, Growth |
| Qwilfish | 13 | none | Poison Point | default | Poison Sting, Water Gun, Tackle, Harden |

Today's team: Doduo 10 (Peck, Growl, Quick Attack, Rage), Nidoran♂ 10 (Leer, Peck, Focus Energy, Double Kick). Expected: 100 / 0.20 / 79.

### Picnicker Diana: Oreburgh Gate, optional, single, cap 16

Technician: weak moves hit hard. Aipom's Covet with a Silk Scarf and
Kricketune's Aerial Ace hit at one and a half times, and Kricketune's Rock
Smash answers the Rock types that resist the rest. Onix and Geodude still
resist most of it; Wartortle's bulk takes the rest.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Skitty | 13 | none | Cute Charm | default | Tackle, Shock Wave, Tail Whip, Growl |
| Meowth | 15 | none | Technician | default | Scratch, Bite, Thief, Growl |
| Kricketune | 15 | none | Technician | default | Fury Cutter, Aerial Ace, Rock Smash, Growl |
| Aipom | 15 | Silk Scarf | Technician | Jolly | Covet, Astonish, Scratch, Tail Whip |

Today's team: Nidoran♀ 10 (Growl, Scratch, Tail Whip, Double Kick). Expected: 100 / 0.25 / 82.

### Worker Colin: Oreburgh Mine B2F, optional, single, cap 16

Two Sturdy walls that survive any one hit, Whismur's Uproar and Shock Wave
for the Water types, and Machop behind them for the Normal and Rock types.
Each Sturdy member needs two hits, so the player wants members that hit
twice cleanly (Water and Grass types).

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Whismur | 14 | none | Scrappy | default | Uproar, Shock Wave, Astonish, Pound |
| Geodude | 15 | none | Sturdy | default | Rock Throw, Rollout, Defense Curl, Rock Tomb |
| Nacli | 15 | none | Sturdy | default | Rock Throw, Mud Shot, Smack Down, Harden |
| Machop | 15 | none | Guts | default | Karate Chop, Low Kick, Rock Tomb, Leer |

Today's team: Geodude 12 (Tackle, Defense Curl, Mud Sport, Rock Throw), Whismur 12 (Uproar, Astonish, Pound). Expected: 100 / 0.15 / 83.

### Worker Mason: Oreburgh Mine B2F, optional, single, cap 16

Four diggers and a Fighting type: Geodude's Rollout behind Sturdy and
Larvitar's Rock Slide, with Makuhita as the danger member for the Normal and
Rock types that would otherwise wall them. Water and Grass types beat most of
it outright, which is why it reads the softest of the split (decision 4).

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Diglett | 15 | none | Sand Veil | default | Magnitude, Mud Bomb, Astonish, Sucker Punch |
| Geodude | 15 | none | Sturdy | default | Rollout, Defense Curl, Rock Throw, Rock Tomb |
| Rhyhorn | 15 | none | Rock Head | default | Horn Attack, Rock Slide, Stomp, Tail Whip |
| Makuhita | 15 | Oran Berry | Thick Fat | Adamant | Arm Thrust, Vital Throw, Rock Tomb, Knock Off |
| Larvitar | 15 | none | Guts | Adamant | Rock Slide, Bite, Leer, Screech |

Today's team: Geodude 12 (Rock Throw, Defense Curl, Mud Sport, Rock Polish). Expected: 100 / 0.10 / 90.

### Youngster Jonathon: Oreburgh Gym, optional, single, cap 16

Roark's lead, rehearsed: Nosepass sets Stealth Rock and Blocks, Geodude
rolls behind Sturdy, and Lileep's Bullet Seed answers the Water types the
player brings for a Rock gym. Nidorino and Charmander take Lileep; switching
too often into the rocks is the trap.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Nosepass | 15 | Oran Berry | Solid Rock | Relaxed | Stealth Rock, Block, Rock Throw, Shock Wave |
| Geodude | 15 | none | Sturdy | default | Rock Throw, Rock Tomb, Rollout, Defense Curl |
| Lileep | 13 | none | Solid Rock | default | Bullet Seed, Acid, AncientPower, Astonish |

Today's team: Rhyhorn 13 (Fury Attack, Rock Tomb). Expected: 100 / 0.15 / 77.

### Youngster Darius: Oreburgh Gym, optional, single, cap 16

Roark's ace, rehearsed: Cranidos with a Passho Berry and Pursuit, behind
fossils that answer the Water types (Kabuto's Giga Drain) and a Shieldon that
Taunts. Cranidos survives one Water hit through its berry, so the player
needs two, or a Fighting or Ground type.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Kabuto | 15 | Oran Berry | Battle Armor | default | Giga Drain, Mud Shot, Aurora Beam, Harden |
| Shieldon | 15 | none | Solid Rock | default | Headbutt, Rock Tomb, Protect, Taunt |
| Anorith | 14 | none | Swift Swim | default | Rock Slide, Knock Off, Fury Cutter, Harden |
| Cranidos | 15 | Passho Berry | Rock Head | Adamant | Headbutt, Pursuit, Rock Slide, Leer |

Today's team: Aron 13 (Headbutt, Rock Tomb), Onix 13 (Rock Throw, Tackle, Harden). Expected: 100 / 0.15 / 84.

### Roark: Oreburgh Gym, on the path, single, boss, cap 16

Kaizo's structure at reduced lethality: a Stealth Rock lead that Blocks and
paralyses, a Rollout snowball behind Sturdy and a Passho Berry, a Lileep wall
that answers Water and Grass types and heals off them, a Larvitar for the
Fire and Steel answers, and a Rock Polish ace with Pursuit for the player who
switches out of it.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Nosepass | 14 | Leftovers | Solid Rock | Relaxed | Stealth Rock, Thunder Wave, Rock Tomb, Block |
| Geodude | 14 | Passho Berry | Sturdy | Adamant | Rock Throw, Rollout, Defense Curl, Rock Tomb |
| Lileep | 15 | Big Root | Solid Rock | Calm | Giga Drain, AncientPower, Recover, Acid |
| Larvitar | 15 | Sitrus Berry | Guts | Adamant | Rock Slide, Bite, Screech, Dig |
| Cranidos | 16 | Lum Berry | Rock Head | Adamant | Rock Slide, Zen Headbutt, Pursuit, Rock Polish |

Today's team: Nosepass 15 (Apicot Berry; Block, Rock Throw, Thunder Wave, Stealth Rock), Geodude 15 (Passho Berry; ThunderPunch, Rollout, Defense Curl, Rock Throw), Lileep 15 (Big Root; Mega Drain, Rock Tomb, Constrict, Ingrain), Cranidos 16 (Sitrus Berry; Headbutt, Pursuit, Leer, Rock Throw).

Nosepass leads with Stealth Rock, Thunder Wave and Rock Tomb for speed
control, and Block as the first switch tax. It is the deliberate hole: nothing
it carries touches a Ground type (Thunder Wave fails, Rock Tomb and Rock Throw
are resisted), so Geodude or Barboach walls it. Geodude has no move for its
Water counter; its Passho Berry and Sturdy buy the turns for Defense Curl and
a Rollout that doubles each turn (decision 6). Lileep is the team's answer to
Water and Ground types (Giga Drain, healed further by Big Root, and Recover)
and to Steenee (Acid); Nidorino's Double Kick and Prinplup's Metal Claw are
the player's answers to it. Larvitar, Dark and Ground in Oxide, answers
Charmander with Dig and Rock Slide. Cranidos is the ace at the cap with the
team's one setup move: Rock Polish doubles its Speed, Zen Headbutt answers
the Fighting and Poison types, and Pursuit is the second switch tax. Every
member holds an item with a job; one resist berry, one status move, no
priority move and no forced trade, as the dial allows before Fantina.

The planning ideas it leaves room for: bait by knockout ownership (who takes
Nosepass decides whether Geodude meets a Water type), a free switch on
Nosepass's Stealth Rock turn, running out Rollout by switching (the chain
resets), Knock Off or Pluck on Geodude's Passho Berry, and a burn on
Cranidos (Vulpix's Will-O-Wisp) before it sets up.

Expected: about 90 / 2.3 / 5. In my simulator the best six it found was
Krabby, Finneon, Nidorino, Charmander, Steenee and Geodude, and the player's
faints fell to Cranidos, Lileep and Geodude about equally, then Larvitar.

## Moved to Gardenia's split: the Jubilife grunts

The two grunts meet the player in a tag battle beside Dawn or Lucas after
the Coal Badge, so they are fought in Gardenia's split at a cap of 19 (Ian,
2026-10-04), and `trainers.csv` lists them there (row 23). Each is
built as one half of a double, from the doubles recipes: the first grunt
spreads chip over both of the player's side (Air Cutter, Poison Gas, Icy
Wind, which also slows both), the second opens with Fake Out and puts one
foe to sleep or confuses it while its partner hits. Glameow's Hypnosis is
the only sleep move, which Gardenia's split allows. Levels sit two and three
under the cap, a notch softer than their neighbours, since the scorer cannot
read a double yet. Today's files have one Pokemon each at 13.

### Galactic Grunt (1): Jubilife City, on the path, tag battle, cap 19

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Zubat | 16 | none | Inner Focus | default | Air Cutter, Bite, Leech Life, Supersonic |
| Stunky | 16 | none | Aftermath | default | Poison Gas, Smog, Fury Swipes, Screech |
| Croagunk | 17 | Oran Berry | Dry Skin | Adamant | Icy Wind, Faint Attack, Poison Sting, Brick Break |

Today's team: Stunky 13 (Scratch, Poison Gas, Screech, Fury Swipes). Expected: not readable
yet; I expect it a little softer than the split's single trainers.

### Galactic Grunt (2): Jubilife City, on the path, tag battle, cap 19

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Glameow | 16 | none | Limber | default | Fake Out, Scratch, Bite, Hypnosis |
| Bronzor | 16 | none | Levitate | default | Confusion, Rock Tomb, Confuse Ray, Tackle |
| Murkrow | 17 | Oran Berry | Insomnia | default | Wing Attack, Faint Attack, Pursuit, Astonish |

Today's team: Glameow 13 (Fake Out, Scratch, Growl, Hypnosis). Expected: not readable
yet.

## How the expected numbers were made

The scorer has not read these teams, so I wrote a rough simulator to rank the
drafts (`../tools/sim.py`): it plays the real damage formula, Oxide's moves
and items, a sketch of the trainer AI, and a player who looks one matchup
ahead instead of searching. Before trusting it I checked it against three
fights the scorer has read:

| Fight | The scorer | My simulator |
|---|---|---|
| Kaizo's Roark against the box at 16, planned six | 81 / 4.31 / 0 | 83 / 3.18 / 0 |
| Today's Roark, planned six | 100 / 0.05 / 95 | 100 / 0.14 / 88 |
| Aroma Lady Taylor at 19, blind | 100 / 0.13 / 91 | 97 / 0.35 / 84 |

So for a boss its win rate lands within two or three points of the scorer's,
and for an ordinary trainer it reads about seven points less clean and about
twice the faints, because its player uses no status or stat moves. The
expected numbers above are its readings corrected by those amounts. Ordinary
trainers were read blind against a random six of the box's stronger half: at
11, Piplup, Squirtle, Krabby, Vulpix, Dottler and Bidoof from the three-gym
run's box before Barry 2; at 16, Prinplup, Wartortle, Bibarel, Nidorino,
Onix, Charmander, Steenee and Geodude from the box the scorer read Kaizo's
Roark against, with its Flame Plate. Bosses were read with the best six the
simulator could find from the whole box. Its readings are noisy by about five
clean points, which is why each team's number is rounded and why the
scorer's reading should replace it.

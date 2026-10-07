# The TM list and the reward table (step 6, a draft for Ian)

Written by `tools/oxide/balance/rewards.py` on the branch `balance-tm-pass`. It changes no game data;
the placement tool applies the approved table in step 10.

## Summary

**Outcome.** The TM list has 100 TMs: 66 of vanilla's 92 kept, the six HMs less Cut and Rock Smash as single-use TMs, and 28 new moves. 40 are strong (one copy), 50 utility (two copies) and 10 weak (one copy, each the reward for one optional trainer). Every TM and each of element 7's 20 held items has exactly one place, by split, and every TM ball and gift in vanilla is repointed, so none gives a second copy. The reward trainers take 30 of the 46 spare story flags, and no new item ball is added. The table's own check passes.

**This list will change.** Its new TMs are ranked by the lines that gain each move they cannot learn by level-up, and the type-ladder rework of the early lists (Ian, 2026-10-06) changes those lists. The move-rework cloud job also changes the numbers of Hyper Beam, Giga Impact and the multi-hit moves, so their tiers here are read on today's data. Both rerun this list in minutes before it is final.

**Ian's action items**, each set out below:

1. Read the TM list (the first table) and mark any TM to cut, add or move.
2. Say what Veilstone Department Store's TM floor and the Game Corner's TM prizes sell instead: 28 TMs are sold there today, and a TM bought without end undoes single-use copies.
3. Pick third copies, if any, among the hazards and pivots: Stealth Rock, U-turn.
4. Approve or change the held items' splits and trainers, the weak TMs' trainers, and the gauntlet sections.

**Next steps.**

| Step | What | Who | About how long |
|---|---|---|---|
| Ladders | The early lists rebuilt on per-type move ladders, then this list rerun | Balance Agent | 4 to 5 hours |
| 7 | Ian approves the TM list, the reward table and the gauntlets | Ian | |
| 8 | Item data for the new TMs, the compatibility lists, the bigger Bag | Balance Agent | 2 to 3 hours, a build and the rescore |
| 10 | The table placed in the maps, the gauntlets filled in | main-track session | 3 to 6 hours |

## The TM list

One row per TM, by the split it first comes in. A number past 92 is new; a number vanilla used for a move that leaves the list now teaches the new move named. Power and accuracy are Oxide's today.

| TM | Move | Type | Class | Power | Accuracy | Tier | Copies | Split | Source |
|---|---|---|---|---|---|---|---|---|---|
| TM48 | Iron Defense | Steel | Status | - | never misses | strong | 1 | Roark | gift, Oreburgh Gate 1F |
| TM63 | Confuse Ray | Ghost | Status | - | 100 | strong | 1 | Roark | gift, Sandgem Town |
| TM76 | Stealth Rock | Rock | Status | - | never misses | utility | 2 | Roark | gift, Oreburgh City Gym |
| TM09 | Bullet Seed | Grass | Physical | 25 | 100 | utility | 2 | Gardenia | ball, Route 204 North |
| TM11 | Spite | Ghost | Status | - | 100 | utility | 2 | Gardenia | gift, Eterna City |
| TM12 | Taunt | Dark | Status | - | 100 | utility | 2 | Gardenia | ball, Route 211 West |
| TM17 | StompingTantrum | Ground | Physical | 75 | 100 | utility | 2 | Gardenia | gift, Eterna City Condominiums 2F |
| TM18 | Scary Face | Normal | Status | - | 100 | utility | 2 | Gardenia | gift, Floaroma Town Middle House |
| TM39 | Rock Tomb | Rock | Physical | 60 | 100 | utility | 2 | Gardenia | ball, Ravaged Path |
| TM41 | Charm | Fairy | Status | - | 100 | strong | 1 | Gardenia | ball, Mt Coronet 1F North Room 1 |
| TM46 | Knock Off | Dark | Physical | 70 | 100 | utility | 2 | Gardenia | ball, Oreburgh Gate B1F |
| TM62 | Silver Wind | Bug | Special | 60 | 100 | weak | 1 | Gardenia | reward trainer |
| TM66 | Payback | Dark | Physical | 60 | 100 | weak | 1 | Gardenia | reward trainer |
| TM78 | Captivate | Normal | Status | - | 100 | utility | 2 | Gardenia | gift, Route 204 North |
| TM86 | Grass Knot | Grass | Special | varies | 100 | utility | 2 | Gardenia | gift, Eterna City Gym |
| TM88 | Pluck | Flying | Physical | 60 | 100 | weak | 1 | Gardenia | reward trainer |
| TM03 | Water Pulse | Water | Special | 60 | 100 | weak | 1 | Fantina | reward trainer |
| TM05 | Dazzling Gleam | Fairy | Special | 80 | 100 | utility | 2 | Fantina | ball, Wayward Cave 1F |
| TM16 | Light Screen | Psychic | Status | - | never misses | utility | 2 | Fantina | ball, Amity Square |
| TM20 | Safeguard | Normal | Status | - | never misses | utility | 2 | Fantina | ball, Eterna City |
| TM31 | Brick Break | Fighting | Physical | 75 | 100 | utility | 2 | Fantina | ball, Oreburgh Gate B1F |
| TM33 | Reflect | Psychic | Status | - | never misses | utility | 2 | Fantina | ball, Eterna Forest Outside |
| TM43 | Secret Power | Normal | Physical | 70 | 100 | utility | 2 | Fantina | ball, Amity Square |
| TM61 | Will-O-Wisp | Fire | Status | - | 85 | strong | 1 | Fantina | ball, Old Chateau Back East Room |
| TM65 | Shadow Claw | Ghost | Physical | 70 | 100 | utility | 2 | Fantina | gift, Hearthome City Gym Leader Room |
| TM73 | Thunder Wave | Electric | Status | - | 100 | strong | 1 | Fantina | ball, Wayward Cave 1F |
| TM85 | Skitter Smack | Bug | Physical | 70 | 100 | utility | 2 | Fantina | ball, Route 206 |
| TM90 | Block | Normal | Status | - | never misses | strong | 1 | Fantina | ball, Route 206 |
| TM93 | Psychic Noise | Psychic | Special | 75 | 100 | utility | 2 | Fantina | ball, Route 208 |
| TM94 | Psybeam | Psychic | Special | 65 | 100 | utility | 2 | Fantina | ball, Team Galactic Eterna Building 2F |
| HM05 | Defog | Flying | Status | - | never misses | utility | 2 | Maylene | ball, Solaceon Ruins Room 7 |
| TM02 | Dragon Claw | Dragon | Physical | 80 | 100 | utility | 2 | Maylene | gift, Game Corner |
| TM10 | Hidden Power | Normal | Special | varies | 100 | weak | 1 | Maylene | reward trainer |
| TM15 | Hyper Beam | Normal | Special | 150 | 90 | utility | 2 | Maylene | ball, Route 209 Lost Tower 4F |
| TM22 | SolarBeam | Grass | Special | 120 | 100 | weak | 1 | Maylene | reward trainer |
| TM34 | Shock Wave | Electric | Special | 60 | never misses | weak | 1 | Maylene | reward trainer |
| TM40 | Aerial Ace | Flying | Physical | 60 | never misses | weak | 1 | Maylene | reward trainer |
| TM42 | Facade | Normal | Physical | 70 | 100 | utility | 2 | Maylene | gift, Route 210 South |
| TM47 | Steel Wing | Steel | Physical | 70 | 90 | utility | 2 | Maylene | ball, Route 209 |
| TM51 | Roost | Flying | Status | - | never misses | strong | 1 | Maylene | gift, Route 210 South |
| TM54 | False Swipe | Normal | Physical | 40 | 100 | utility | 2 | Maylene | ball, Route 215 |
| TM57 | Charge Beam | Electric | Special | 50 | 100 | weak | 1 | Maylene | reward trainer |
| TM60 | Drain Punch | Fighting | Physical | 75 | 100 | utility | 2 | Maylene | gift, Veilstone City Gym |
| TM68 | Giga Impact | Normal | Physical | 150 | 90 | utility | 2 | Maylene | gift, Route 215 |
| TM74 | Gyro Ball | Steel | Physical | varies | 100 | utility | 2 | Maylene | gift, Veilstone City |
| TM82 | Bounce | Flying | Physical | 85 | 100 | utility | 2 | Maylene | ball, Route 209 |
| TM83 | Expanding Force | Psychic | Special | 80 | 100 | utility | 2 | Maylene | ball, Route 210 South |
| TM06 | Toxic | Poison | Status | - | 100 | strong | 1 | Wake | ball, Route 212 South |
| TM28 | Dig | Ground | Physical | 80 | 100 | utility | 2 | Wake | ball, Ruin Maniac Cave Short |
| TM32 | Zen Headbutt | Psychic | Physical | 80 | 100 | utility | 2 | Wake | ball, Route 212 North |
| TM37 | Signal Beam | Bug | Special | 75 | 100 | utility | 2 | Wake | ball, Route 212 South |
| TM44 | Wild Charge | Electric | Physical | 90 | 100 | utility | 2 | Wake | ball, Route 213 |
| TM55 | Brine | Water | Special | 65 | 100 | utility | 2 | Wake | gift, Pastoria City Gym |
| TM72 | Avalanche | Ice | Physical | 60 | 100 | weak | 1 | Wake | reward trainer |
| TM87 | Swagger | Normal | Status | - | 90 | strong | 1 | Wake | ball, Pokemon Mansion Office |
| TM92 | Trick Room | Psychic | Status | - | never misses | utility | 2 | Wake | gift, Grand Lake Route 213 Northwest House |
| HM03 | Surf | Water | Special | 90 | 100 | strong | 1 | Byron | gift, Celestic Town Cave |
| HM04 | Strength | Normal | Physical | 80 | 100 | utility | 2 | Byron | gift, Iron Island |
| TM04 | Calm Mind | Psychic | Status | - | never misses | strong | 1 | Byron | gift, Canalave City Southeast House |
| TM07 | Curse | Mystery | Status | - | never misses | strong | 1 | Byron | ball, Ravaged Path |
| TM08 | Bulk Up | Fighting | Status | - | never misses | strong | 1 | Byron | ball, Lake Valor |
| TM19 | Giga Drain | Grass | Special | 75 | 100 | utility | 2 | Byron | ball, Route 209 |
| TM23 | Iron Tail | Steel | Physical | 100 | 75 | strong | 1 | Byron | ball, Iron Island B2F Right Room |
| TM24 | Thunderbolt | Electric | Special | 90 | 100 | strong | 1 | Byron | ball, Valley Windworks Outside |
| TM26 | Earthquake | Ground | Physical | 100 | 100 | strong | 1 | Byron | ball, Lake Verity |
| TM30 | Shadow Ball | Ghost | Special | 80 | 100 | utility | 2 | Byron | ball, Route 210 North |
| TM35 | Flamethrower | Fire | Special | 90 | 100 | strong | 1 | Byron | ball, Fuego Ironworks Building |
| TM45 | Alluring Voice | Fairy | Special | 80 | 100 | utility | 2 | Byron | gift, Route 211 East |
| TM77 | Foul Play | Dark | Physical | 95 | 100 | strong | 1 | Byron | ball, Iron Island B1F Right Room |
| TM81 | X-Scissor | Bug | Physical | 80 | 100 | utility | 2 | Byron | ball, Route 221 |
| TM84 | Poison Jab | Poison | Physical | 80 | 100 | utility | 2 | Byron | ball, Route 212 South |
| TM89 | U-turn | Bug | Physical | 70 | 100 | utility | 2 | Byron | ball, Canalave City |
| TM91 | Flash Cannon | Steel | Special | 80 | 100 | utility | 2 | Byron | gift, Canalave City Gym |
| HM08 | Rock Climb | Normal | Physical | 90 | 100 | strong | 1 | Candice | ball, Route 217 |
| TM49 | Agility | Psychic | Status | - | never misses | strong | 1 | Candice | ball, Lake Acuity |
| TM56 | Hex | Ghost | Special | 65 | 100 | utility | 2 | Candice | ball, Oreburgh Gate B1F |
| TM64 | Play Rough | Fairy | Physical | 90 | 100 | strong | 1 | Candice | ball, Route 217 |
| TM67 | Ice Punch | Ice | Physical | 95 | 100 | strong | 1 | Candice | gift, Snowpoint City Gym |
| TM69 | Rock Polish | Rock | Status | - | never misses | strong | 1 | Candice | ball, Mt Coronet 1F North Room 1 |
| HM02 | Fly | Flying | Physical | 90 | 95 | strong | 1 | HQ | ball, Veilstone City Galactic Warehouse |
| TM13 | Ice Beam | Ice | Special | 90 | 100 | strong | 1 | HQ | ball, Route 216 |
| TM14 | Blizzard | Ice | Special | 110 | 70 | strong | 1 | HQ | ball, Galactic Hq 1F |
| TM21 | Frustration | Normal | Physical | varies | 100 | strong | 1 | HQ | ball, Galactic Hq 3F |
| TM25 | Thunder | Electric | Special | 110 | 70 | strong | 1 | HQ | ball, Route 213 |
| TM27 | Return | Normal | Physical | varies | 100 | strong | 1 | HQ | ball, Valor Lakefront |
| TM29 | Psychic | Psychic | Special | 90 | 100 | strong | 1 | HQ | ball, Route 211 East |
| TM36 | Sludge Bomb | Poison | Special | 90 | 100 | strong | 1 | HQ | ball, Galactic Hq B2F |
| TM01 | Hydro Pump | Water | Special | 110 | 80 | strong | 1 | Galactic | gift, Survival Area South House |
| TM38 | Fire Blast | Fire | Special | 110 | 85 | strong | 1 | Galactic | ball, Route 228 |
| TM50 | Overheat | Fire | Special | 130 | 90 | strong | 1 | Galactic | ball, Stark Mountain Room 2 |
| TM53 | Energy Ball | Grass | Special | 90 | 100 | strong | 1 | Galactic | ball, Route 226 |
| TM80 | Rock Slide | Rock | Physical | 75 | 90 | utility | 2 | Galactic | ball, Mt Coronet 2F |
| HM07 | Waterfall | Water | Physical | 80 | 100 | strong | 1 | Volkner | gift, Sunyshore City |
| TM52 | Focus Blast | Fighting | Special | 120 | 70 | strong | 1 | Volkner | gift, Route 222 |
| TM58 | Triple Axel | Ice | Physical | 20 | 90 | strong | 1 | Volkner | gift, Sunyshore City Gym Room 3 |
| TM59 | Dragon Pulse | Dragon | Special | 85 | 100 | utility | 2 | Barry | ball, Victory Road B1F |
| TM70 | Outrage | Dragon | Physical | 120 | 100 | utility | 2 | Barry | ball, Route 223 |
| TM71 | Stone Edge | Rock | Physical | 100 | 80 | strong | 1 | Barry | ball, Victory Road 2F |
| TM75 | Meteor Beam | Rock | Special | 120 | 100 | strong | 1 | Barry | ball, Victory Road 1F |
| TM79 | Dark Pulse | Dark | Special | 80 | 100 | utility | 2 | Barry | ball, Victory Road 2F |

## What changed against vanilla

**Kept** (66): TM02 Dragon Claw, TM03 Water Pulse, TM04 Calm Mind, TM06 Toxic, TM08 Bulk Up, TM09 Bullet Seed, TM10 Hidden Power, TM12 Taunt, TM13 Ice Beam, TM14 Blizzard, TM15 Hyper Beam, TM16 Light Screen, TM19 Giga Drain, TM20 Safeguard, TM21 Frustration, TM22 SolarBeam, TM23 Iron Tail, TM24 Thunderbolt, TM25 Thunder, TM26 Earthquake, TM27 Return, TM28 Dig, TM29 Psychic, TM30 Shadow Ball, TM31 Brick Break, TM33 Reflect, TM34 Shock Wave, TM35 Flamethrower, TM36 Sludge Bomb, TM38 Fire Blast, TM39 Rock Tomb, TM40 Aerial Ace, TM42 Facade, TM43 Secret Power, TM47 Steel Wing, TM50 Overheat, TM51 Roost, TM52 Focus Blast, TM53 Energy Ball, TM54 False Swipe, TM55 Brine, TM57 Charge Beam, TM59 Dragon Pulse, TM60 Drain Punch, TM61 Will-O-Wisp, TM62 Silver Wind, TM65 Shadow Claw, TM66 Payback, TM68 Giga Impact, TM69 Rock Polish, TM71 Stone Edge, TM72 Avalanche, TM73 Thunder Wave, TM74 Gyro Ball, TM76 Stealth Rock, TM78 Captivate, TM79 Dark Pulse, TM80 Rock Slide, TM81 X-Scissor, TM84 Poison Jab, TM86 Grass Knot, TM87 Swagger, TM88 Pluck, TM89 U-turn, TM91 Flash Cannon, TM92 Trick Room.

**Former HMs**, single-use TMs now that field moves work on the badge alone: HM02 Fly (buff proposed: accuracy 95 to 100, so the two-turn hit no longer misses), HM03 Surf, HM04 Strength (buff proposed: power 80 to 90, a clean Normal hit between Body Slam and Double-Edge), HM05 Defog (buff proposed: clears hazards on both sides, as the later games do, to answer the trainers' hazards), HM07 Waterfall, HM08 Rock Climb (buff proposed: accuracy 85 to 95, so its confusion chance rides on a hit that lands). Cut and Rock Smash leave.

**Cut**:

- TM01 Focus Punch: Ian's removal
- TM05 Roar: a status move Ian rates under pretty solid
- TM07 Hail: Ian's removal
- TM11 Sunny Day: Ian's removal
- TM17 Protect: Ian's removal
- TM18 Rain Dance: Ian's removal
- TM32 Double Team: Ian's removal
- TM37 Sandstorm: Ian's removal
- TM41 Torment: a status move Ian rates under pretty solid
- TM44 Rest: a status move Ian rates under pretty solid
- TM45 Attract: a status move Ian rates under pretty solid
- TM46 Thief: Ian's removal
- TM48 Skill Swap: Ian's removal
- TM49 Snatch: Ian's removal
- TM56 Fling: hangs on a held item
- TM58 Endure: a status move Ian rates under pretty solid
- TM63 Embargo: Ian's removal
- TM64 Explosion: the user faints, which in a nuzlocke is a death
- TM67 Recycle: a status move Ian rates under pretty solid
- TM70 Flash: Ian's removal
- TM75 Swords Dance: Ian's removal
- TM77 Psych Up: a status move Ian rates under pretty solid
- TM82 Sleep Talk: random, or hangs on a rare condition
- TM83 Natural Gift: hangs on a held item
- TM85 Dream Eater: Ian's removal
- TM90 Substitute: Ian's removal

**New**, ranked by the lines without a niche each gives a real option, then by lines gained:

| TM | Move | Why |
|---|---|---|
| TM01 | Hydro Pump | 56 lines gain it that cannot learn it by level-up, 11 of them lines no boss takes today |
| TM05 | Dazzling Gleam | 22 lines gain it that cannot learn it by level-up, 9 of them lines no boss takes today |
| TM07 | Curse | 48 lines gain it that cannot learn it by level-up, 8 of them lines no boss takes today |
| TM11 | Spite | 35 lines gain it that cannot learn it by level-up, 8 of them lines no boss takes today |
| TM17 | StompingTantrum | 56 lines gain it that cannot learn it by level-up, 7 of them lines no boss takes today |
| TM18 | Scary Face | 47 lines gain it that cannot learn it by level-up, 7 of them lines no boss takes today |
| TM32 | Zen Headbutt | 34 lines gain it that cannot learn it by level-up, 6 of them lines no boss takes today |
| TM37 | Signal Beam | 33 lines gain it that cannot learn it by level-up, 6 of them lines no boss takes today |
| TM41 | Charm | 30 lines gain it that cannot learn it by level-up, 6 of them lines no boss takes today |
| TM44 | Wild Charge | 19 lines gain it that cannot learn it by level-up, 6 of them lines no boss takes today |
| TM45 | Alluring Voice | 15 lines gain it that cannot learn it by level-up, 6 of them lines no boss takes today |
| TM46 | Knock Off | 51 lines gain it that cannot learn it by level-up, 5 of them lines no boss takes today |
| TM48 | Iron Defense | 36 lines gain it that cannot learn it by level-up, 5 of them lines no boss takes today |
| TM49 | Agility | 31 lines gain it that cannot learn it by level-up, 5 of them lines no boss takes today |
| TM56 | Hex | 26 lines gain it that cannot learn it by level-up, 5 of them lines no boss takes today |
| TM58 | Triple Axel | 23 lines gain it that cannot learn it by level-up, 5 of them lines no boss takes today |
| TM63 | Confuse Ray | 21 lines gain it that cannot learn it by level-up, 5 of them lines no boss takes today |
| TM64 | Play Rough | 17 lines gain it that cannot learn it by level-up, 5 of them lines no boss takes today |
| TM67 | Ice Punch | 39 lines gain it that cannot learn it by level-up, 4 of them lines no boss takes today |
| TM70 | Outrage | 29 lines gain it that cannot learn it by level-up, 4 of them lines no boss takes today |
| TM75 | Meteor Beam | 27 lines gain it that cannot learn it by level-up, 4 of them lines no boss takes today |
| TM77 | Foul Play | 27 lines gain it that cannot learn it by level-up, 4 of them lines no boss takes today |
| TM82 | Bounce | 24 lines gain it that cannot learn it by level-up, 4 of them lines no boss takes today |
| TM83 | Expanding Force | 18 lines gain it that cannot learn it by level-up, 4 of them lines no boss takes today |
| TM85 | Skitter Smack | 18 lines gain it that cannot learn it by level-up, 4 of them lines no boss takes today |
| TM90 | Block | 17 lines gain it that cannot learn it by level-up, 4 of them lines no boss takes today |
| TM93 | Psychic Noise | 17 lines gain it that cannot learn it by level-up, 4 of them lines no boss takes today |
| TM94 | Psybeam | 17 lines gain it that cannot learn it by level-up, 4 of them lines no boss takes today |

Just below the line: Poltergeist (9 lines), ThunderPunch (47 lines), Rock Blast (31 lines), Encore (28 lines), Hurricane (27 lines), Gunk Shot (26 lines), Aqua Tail (25 lines), Psyshock (23 lines), Assurance (13 lines), Psychic Fangs (12 lines), Venoshock (12 lines), Close Combat (7 lines), Low Kick (41 lines), Fire Punch (31 lines), Earth Power (31 lines).

Left out as doing the same job as a TM in the list: Tera Blast (beside Hyper Beam), Take Down (beside Facade), Headbutt (beside Facade), Body Slam (beside Facade), Dive (beside Waterfall), Double-Edge (beside Frustration), Liquidation (beside Waterfall), Icicle Spear (beside Avalanche), Seed Bomb (beside Bullet Seed), Retaliate (beside Facade), High Horsepower (beside Dig), Scald (beside Surf), Petal Blizzard (beside Bullet Seed), Lunge (beside Skitter Smack), Leaf Storm (beside Energy Ball), Heat Wave (beside Fire Blast), Sky Attack (beside Aerial Ace), Muddy Water (beside Surf), Brave Bird (beside Fly), Low Sweep (beside Brick Break).

## The reward trainers

Each is optional (the census reads it as avoidable or off the story path) and gives its reward once, straight after the win. Held items go to the upper quarter of their split's optional trainers by reading on Ian's fight scale, an optional challenge; weak TMs to the stronger half of the easier side, the weak-to-medium trainers Ian named. At most two rewards share a map.

| Reward | Split | Trainer | Map | Reading |
|---|---|---|---|---|
| Absorb Bulb | Gardenia | Bug Catcher Phillip | Eterna Forest | 2.3 |
| Eviolite | Gardenia | Bug Catcher Donald | Eterna Forest | 2.3 |
| Cell Battery | Gardenia | Bird Keeper Alexandra | Route 211 West | 2.3 |
| Binding Band | Fantina | Cyclist Kayla | Route 206 | 2.3 |
| Fairy Feather | Fantina | Camper Anthony | Route 207 | 2.3 |
| Loaded Dice | Fantina | Picnicker Lauren | Route 207 | 2.3 |
| Air Balloon | Fantina | Artist William | Route 208 | 2.3 |
| Rocky Helmet | Fantina | Black Belt Kyle | Route 208 | 2.3 |
| Punching Glove | Maylene | Waitress Kati | Cafe | 2.3 |
| Assault Vest | Maylene | Young Couple Ty & Sue | Route 209 | 2.5 |
| Safety Goggles | Maylene | Pkmn Breeder Kahlil | Route 210 South | 2.4 |
| Weakness Policy | Wake | Scientist Shaun | Route 212 South | 3.2 |
| Covert Cloak | Wake | Fisherman Kenneth | Route 213 | 3.2 |
| Eject Button | Wake | Tuber Trenton | Route 219 | 2.9 |
| Red Card | Wake | Tuber Mariel | Route 219 | 2.8 |
| Mirror Herb | Byron | Swimmer♀ Jessica | Route 220 | 2.7 |
| Clear Amulet | Byron | Fisherman Cory | Route 221 | 2.7 |
| Ring Target | Candice | Ace Trainer Blake | Route 216 | 2.4 |
| Ability Shield | Candice | Skier Lexie | Route 217 | 2.4 |
| Pixie Plate | Volkner | Beauty Nicola | Route 222 | 2.3 |
| TM62 Silver Wind | Gardenia | Picnicker Karina | Route 205 South | 2.3 |
| TM66 Payback | Gardenia | Camper Zackary | Route 205 South | 2.3 |
| TM88 Pluck | Gardenia | Hiker Louis | Route 211 West | 2.3 |
| TM03 Water Pulse | Fantina | Hiker Theodore | Route 206 | 2.3 |
| TM40 Aerial Ace | Maylene | Collector Edwin | Cafe | 2.3 |
| TM10 Hidden Power | Maylene | Jogger Raul | Route 209 | 2.3 |
| TM22 SolarBeam | Maylene | Jogger Wyatt | Route 210 South | 2.3 |
| TM34 Shock Wave | Maylene | Ruin Maniac Calvin | Route 215 | 2.3 |
| TM57 Charge Beam | Maylene | Jogger Scott | Route 215 | 2.3 |
| TM72 Avalanche | Wake | Collector Dean | Route 212 South | 2.3 |

## The gauntlets

The sections of the gauntlet proposal (balance plan, "The gauntlets, reworked on Ian's rulings"), with their trainers in walking order. A section of 2 to 5 mandatory trainers on the easier side of its split's average; bosses stay outside. The reading is `gauntlet.py`'s second one on the lists in the tree: clean clears, then deaths a run.

| Area | Section | Split | Trainers | Reading |
|---|---|---|---|---|
| Team Galactic's Eterna building | 1F and 2F | Fantina | Galactic Grunt, Galactic Grunt, Galactic Grunt, Galactic Grunt | 1.00, 0.00 |
| Team Galactic's Eterna building | 3F | Fantina | Scientist Travon, Galactic Officer Moira | 1.00, 0.00 |
| The Galactic HQ | 1F | HQ | Galactic Grunt, Scientist Fredrick | 0.89, 0.12 |
| The Galactic HQ | 2F | HQ | Galactic Grunt, Galactic Grunt, Galactic Grunt, Scientist Darrius | 0.69, 0.43 |
| The Galactic HQ | 3F | HQ | Galactic Grunt, Galactic Grunt, Galactic Grunt, Galactic Grunt | 0.84, 0.19 |
| The Galactic HQ | B2F | HQ | Galactic Grunt, Galactic Grunt | 0.69, 0.34 |
| Mt. Coronet | 1F's tunnel | Galactic | Galactic Grunt, Galactic Grunt, Galactic Grunt | 0.95, 0.05 |
| Mt. Coronet | 3F, 4F and Somnu on 5F | Galactic | Galactic Grunt, Galactic Grunt, Galactic Grunt, Galactic Grunt, Galactic Officer Somnu | 0.95, 0.06 |
| Victory Road | 1F, the half nearer the entrance | Barry | Psychic Bryce, Bird Keeper Hana, Ace Trainer Mariah | 0.83, 0.20 |
| Victory Road | 1F, the far half | Barry | Black Belt Miles, Dragon Tamer Clinton, Veteran Edgar | 0.64, 0.47 |
| Victory Road | 2F | Barry | Ace Trainer Sydney, Veteran Clayton, Ace Trainer Omar, Double Team Al & Kay | 0.44, 1.02 |
| Victory Road | B1F | Barry | Double Team Jo & Pat, Psychic Valencia, Ace Trainer Henry, Dragon Tamer Ondrej | 0.54, 0.75 |

## The marts and the Game Corner

These sell TMs today. Each is a second source of a TM the list places, which the placement tool's check refuses, and single-use copies mean little if a TM can be bought without end. What each slot sells instead is Ian's to choose; the balance track recommends keeping the floors' theme with items not sold elsewhere, and leaving held items out, since those come from optional fights.

| Where | Split | TM sold today |
|---|---|---|
| VeilstoneDeptStoreStock_3F_UP | Maylene | TM83 Expanding Force |
| VeilstoneDeptStoreStock_3F_UP | Maylene | TM17 StompingTantrum |
| VeilstoneDeptStoreStock_3F_UP | Maylene | TM54 False Swipe |
| VeilstoneDeptStoreStock_3F_UP | Maylene | TM20 Safeguard |
| VeilstoneDeptStoreStock_3F_UP | Maylene | TM33 Reflect |
| VeilstoneDeptStoreStock_3F_UP | Maylene | TM16 Light Screen |
| VeilstoneDeptStoreStock_3F_UP | Maylene | TM70 Outrage |
| VeilstoneDeptStoreStock_3F_DOWN | Maylene | TM38 Fire Blast |
| VeilstoneDeptStoreStock_3F_DOWN | Maylene | TM25 Thunder |
| VeilstoneDeptStoreStock_3F_DOWN | Maylene | TM14 Blizzard |
| VeilstoneDeptStoreStock_3F_DOWN | Maylene | TM22 SolarBeam |
| VeilstoneDeptStoreStock_3F_DOWN | Maylene | TM52 Focus Blast |
| VeilstoneDeptStoreStock_3F_DOWN | Maylene | TM15 Hyper Beam |
| GameCornerPrizes | Maylene | TM90 Block |
| GameCornerPrizes | Maylene | TM58 Triple Axel |
| GameCornerPrizes | Maylene | TM75 Meteor Beam |
| GameCornerPrizes | Maylene | TM32 Zen Headbutt |
| GameCornerPrizes | Maylene | TM44 Wild Charge |
| GameCornerPrizes | Maylene | TM89 U-turn |
| GameCornerPrizes | Maylene | TM10 Hidden Power |
| GameCornerPrizes | Maylene | TM27 Return |
| GameCornerPrizes | Maylene | TM21 Frustration |
| GameCornerPrizes | Maylene | TM35 Flamethrower |
| GameCornerPrizes | Maylene | TM24 Thunderbolt |
| GameCornerPrizes | Maylene | TM13 Ice Beam |
| GameCornerPrizes | Maylene | TM29 Psychic |
| GameCornerPrizes | Maylene | TM74 Gyro Ball |
| GameCornerPrizes | Maylene | TM68 Giga Impact |

## Strong TMs held back

A strong TM comes no earlier than the split each flagged line that learns it has a good attack of its type by level-up, Byron's at the latest. These reach flagged stages with none by then:

- Blizzard: Absol, Arceus, Articuno, Blastoise, Castform, Cranidos, Crawdaunt, Darkrai and 35 more
- Earthquake: Aerodactyl, Arceus, Blastoise, Blaziken, Charizard, Cranidos, Dhelmise, Dialga and 35 more
- Energy Ball: Abra, Alakazam, Arceus, Armarouge, Castform, Chandelure, Chimecho, Emolga and 14 more
- Fire Blast: Absol, Aerodactyl, Arceus, Castform, Cranidos, Dialga, Flygon, Garchomp and 17 more
- Flamethrower: Absol, Aerodactyl, Arceus, Castform, Cranidos, Dialga, Electivire, Flygon and 19 more
- Fly: Aerodactyl, Arceus, Articuno, Moltres, Vikavolt, Volcarona, Zapdos
- Focus Blast: Alakazam, Ampharos, Annihilape, Arceus, Armarouge, Blaziken, Charizard, Cinccino and 29 more
- Foul Play: Abra, Absol, Alakazam, Ambipom, Arceus, Darkrai, Delphox, Haunter and 10 more
- Frustration: Abra, Absol, Alakazam, Ampharos, Annihilape, Arceus, Armaldo, Articuno and 75 more
- Hydro Pump: Arceus, Dhelmise, Grapploct, Hisuian Goodra, Palkia, Rhydon, Rhyperior, Tyranitar
- Ice Beam: Absol, Arceus, Articuno, Blastoise, Castform, Cranidos, Crawdaunt, Darkrai and 36 more
- Ice Punch: Abra, Alakazam, Ambipom, Ampharos, Annihilape, Blastoise, Electabuzz, Electivire and 33 more
- Iron Tail: Abra, Absol, Alakazam, Ambipom, Annihilape, Arceus, Armaldo, Breloom and 43 more
- Meteor Beam: Aerodactyl, Ampharos, Arceus, Armarouge, Lunatone, Metagross, Omastar, Regirock and 2 more
- Overheat: Annihilape, Arceus, Dialga, Granbull, Moltres, Primeape, Solrock, Toucannon and 1 more
- Play Rough: Absol, Cinccino, Delcatty, Donphan, Frosmoth, Liepard, Lopunny, Luxray and 6 more
- Psychic: Abra, Arceus, Chandelure, Darkrai, Electabuzz, Electivire, Florges, Froslass and 14 more
- Return: Abra, Absol, Alakazam, Ampharos, Annihilape, Arceus, Armaldo, Articuno and 75 more
- Rock Climb: Ampharos, Annihilape, Arceus, Blastoise, Blaziken, Darkrai, Electabuzz, Electivire and 15 more
- Sludge Bomb: Arceus, Carnivine, Crawdaunt, Darkrai, Glimmet, Goodra, Granbull, Haunter and 5 more
- Stone Edge: Absol, Aerodactyl, Arceus, Blaziken, Breloom, Cranidos, Dialga, Donphan and 25 more
- Surf: Arceus, Dhelmise, Garchomp, Grapploct, Hariyama, Hisuian Goodra, Krabby, Nidoking and 9 more
- Thunder: Absol, Ambipom, Annihilape, Arceus, Castform, Cinccino, Cranidos, Darkrai and 28 more
- Thunderbolt: Absol, Ambipom, Annihilape, Arceus, Castform, Cinccino, Cranidos, Darkrai and 32 more
- Triple Axel: Ambipom, Articuno, Cinccino, Empoleon, Gallade, Gardevoir, Glaceon, Leavanny and 10 more
- Waterfall: Arceus, Grapploct, Palkia

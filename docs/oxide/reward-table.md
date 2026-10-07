# The TM list and the reward table (step 6, for Ian)

Written by `tools/oxide/balance/rewards.py` on the branch `balance-tm-pass`. It changes no game data;
the placement tool applies the approved table in step 10.

## Summary

**Outcome.** The TM list Ian approved on 2026-10-06 has 100 TMs: 94 of vanilla's 92 kept, the six HMs less Cut and Rock Smash as single-use TMs, and 28 new moves, their numbers fixed. 43 are strong (one copy), 46 utility (two copies) and 11 weak (one copy, each the reward for one optional trainer). This version carries Ian's answers of the same day: his four timing notes; an even spread across the splits by their length (61 TMs by the end of Byron's split, where the first draft had 73); and the Department Store's and the Game Corner's 28 TMs sold once each, unlocked by badge count in order of usefulness. Every TM and each of element 7's 24 held items has exactly one place, every vanilla TM ball, gift and shop TM is repointed, and the reward trainers take 46 of the 46 spare story flags. The table's own check passes.

**What can still move.** The move-rework cloud job changes the numbers of Hyper Beam, Giga Impact and the multi-hit moves, so their tiers, and with them their copies and places, are read on today's data. The numbers and moves stay as they are.

**Ian's action items:** spot-check the moves that moved ("The spread") and the shop's badge tiers; third copies, if any, among Stealth Rock, U-turn.

**Next steps.**

| Step | What | Who | About how long |
|---|---|---|---|
| 8 | Every species' TM compatibility, then the one rescore after the rework job merges | Balance Agent | 2 to 3 hours and 1.5 hours of machine time |
| 8 | The bigger TM pocket and the item data for the new TMs (from `tm-list.tsv`) | main-track session | |
| 10 | The table placed in the maps and shops, the gauntlets filled in | main-track session | 3 to 6 hours |

## The TM list by number

Every number from TM01, then the HMs: the move vanilla teaches by it, the move it teaches now, the split it first comes in, and why it changed.

| Number | Vanilla | Now | Split | Why it changed |
|---|---|---|---|---|
| TM01 | Hydro Pump | Hydro Pump | Galactic |  |
| TM02 | Dragon Claw | Dragon Claw | Wake |  |
| TM03 | Water Pulse | Water Pulse | Fantina |  |
| TM04 | Calm Mind | Calm Mind | Volkner |  |
| TM05 | Dazzling Gleam | Dazzling Gleam | Wake |  |
| TM06 | Toxic | Toxic | Roark |  |
| TM07 | Curse | Curse | Candice |  |
| TM08 | Bulk Up | Bulk Up | Barry |  |
| TM09 | Bullet Seed | Bullet Seed | Gardenia |  |
| TM10 | Hidden Power | Hidden Power | Maylene |  |
| TM11 | Spite | Spite | Byron |  |
| TM12 | Taunt | Taunt | Fantina |  |
| TM13 | Ice Beam | Ice Beam | Candice |  |
| TM14 | Blizzard | Blizzard | Galactic |  |
| TM15 | Hyper Beam | Hyper Beam | Barry |  |
| TM16 | Light Screen | Light Screen | Candice |  |
| TM17 | StompingTantrum | StompingTantrum | Byron |  |
| TM18 | Scary Face | Scary Face | HQ |  |
| TM19 | Giga Drain | Giga Drain | Gardenia |  |
| TM20 | Safeguard | Safeguard | Maylene |  |
| TM21 | Frustration | Frustration | Galactic |  |
| TM22 | SolarBeam | SolarBeam | Maylene |  |
| TM23 | Iron Tail | Iron Tail | Byron |  |
| TM24 | Thunderbolt | Thunderbolt | Volkner |  |
| TM25 | Thunder | Thunder | Galactic |  |
| TM26 | Earthquake | Earthquake | Byron |  |
| TM27 | Return | Return | Galactic |  |
| TM28 | Dig | Dig | Maylene |  |
| TM29 | Psychic | Psychic | Byron |  |
| TM30 | Shadow Ball | Shadow Ball | Maylene |  |
| TM31 | Brick Break | Brick Break | Gardenia |  |
| TM32 | Zen Headbutt | Zen Headbutt | Maylene |  |
| TM33 | Reflect | Reflect | HQ |  |
| TM34 | Shock Wave | Shock Wave | Maylene |  |
| TM35 | Flamethrower | Flamethrower | Byron |  |
| TM36 | Sludge Bomb | Sludge Bomb | Byron |  |
| TM37 | Signal Beam | Signal Beam | HQ |  |
| TM38 | Fire Blast | Fire Blast | Galactic |  |
| TM39 | Rock Tomb | Rock Tomb | Gardenia |  |
| TM40 | Aerial Ace | Aerial Ace | Gardenia |  |
| TM41 | Charm | Charm | Wake |  |
| TM42 | Facade | Facade | Gardenia |  |
| TM43 | Secret Power | Secret Power | HQ |  |
| TM44 | Wild Charge | Wild Charge | Wake |  |
| TM45 | Alluring Voice | Alluring Voice | Wake |  |
| TM46 | Knock Off | Knock Off | Maylene |  |
| TM47 | Steel Wing | Steel Wing | Gardenia |  |
| TM48 | Iron Defense | Iron Defense | Barry |  |
| TM49 | Agility | Agility | Candice |  |
| TM50 | Overheat | Overheat | Galactic |  |
| TM51 | Roost | Roost | Roark |  |
| TM52 | Focus Blast | Focus Blast | Barry |  |
| TM53 | Energy Ball | Energy Ball | Byron |  |
| TM54 | False Swipe | False Swipe | Byron |  |
| TM55 | Brine | Brine | Candice |  |
| TM56 | Hex | Hex | HQ |  |
| TM57 | Charge Beam | Charge Beam | Gardenia |  |
| TM58 | Triple Axel | Triple Axel | Galactic |  |
| TM59 | Dragon Pulse | Dragon Pulse | Wake |  |
| TM60 | Drain Punch | Drain Punch | Fantina |  |
| TM61 | Will-O-Wisp | Will-O-Wisp | Wake |  |
| TM62 | Silver Wind | Silver Wind | Gardenia |  |
| TM63 | Confuse Ray | Confuse Ray | Wake |  |
| TM64 | Play Rough | Play Rough | Candice |  |
| TM65 | Shadow Claw | Shadow Claw | Maylene |  |
| TM66 | Payback | Payback | Gardenia |  |
| TM67 | Ice Punch | Ice Punch | Byron |  |
| TM68 | Giga Impact | Giga Impact | Barry |  |
| TM69 | Rock Polish | Rock Polish | Galactic |  |
| TM70 | Outrage | Outrage | Galactic |  |
| TM71 | Stone Edge | Stone Edge | Byron |  |
| TM72 | Avalanche | Avalanche | Wake |  |
| TM73 | Thunder Wave | Thunder Wave | Wake |  |
| TM74 | Gyro Ball | Gyro Ball | Candice |  |
| TM75 | Meteor Beam | Meteor Beam | Galactic |  |
| TM76 | Stealth Rock | Stealth Rock | Fantina |  |
| TM77 | Foul Play | Foul Play | Byron |  |
| TM78 | Captivate | Captivate | Barry |  |
| TM79 | Dark Pulse | Dark Pulse | Fantina |  |
| TM80 | Rock Slide | Rock Slide | Candice |  |
| TM81 | X-Scissor | X-Scissor | Wake |  |
| TM82 | Bounce | Bounce | Wake |  |
| TM83 | Expanding Force | Expanding Force | Wake |  |
| TM84 | Poison Jab | Poison Jab | Wake |  |
| TM85 | Skitter Smack | Skitter Smack | Byron |  |
| TM86 | Grass Knot | Grass Knot | Barry |  |
| TM87 | Swagger | Swagger | Roark |  |
| TM88 | Pluck | Pluck | Gardenia |  |
| TM89 | U-turn | U-turn | Barry |  |
| TM90 | Block | Block | Roark |  |
| TM91 | Flash Cannon | Flash Cannon | Fantina |  |
| TM92 | Trick Room | Trick Room | Roark |  |
| TM93 | Psychic Noise | Psychic Noise | Barry |  |
| TM94 | Psybeam | Psybeam | Byron |  |
| HM01 | Cut | - | - | leaves the list (field moves work on the badge alone) |
| HM02 | Fly | Fly | Byron |  |
| HM03 | Surf | Surf | Galactic |  |
| HM04 | Strength | Strength | Fantina |  |
| HM05 | Defog | Defog | Candice |  |
| HM06 | Rock Smash | - | - | leaves the list (field moves work on the badge alone) |
| HM07 | Waterfall | Waterfall | Galactic |  |
| HM08 | Rock Climb | Rock Climb | Candice |  |

## The spread

TMs by the split they first come in, against each split's share by its length (the trainers in it), and the first draft's count.

**What gates a TM's timing.** A TM attack comes no earlier than the split whose old power ceiling covers its power: the learnset generator's ceiling for a same-type attack, 60 in Roark's split, 75 in Gardenia's split, 80 in Fantina's split, 90 in Maylene's split, 90 in Wake's split, 100 in Byron's split, and more after. A hard gate, not a weight. A strong TM also waits for each flagged line that learns it to have a good attack of its type by level-up (Byron's split at the latest), and Ian's timing notes hold five moves later. The power gate is the lever to turn if TM timing feels off in the alpha.

| Split | Share | Now | First draft |
|---|---|---|---|
| Roark | 5.4 | 5 | 3 |
| Gardenia | 11.1 | 11 | 13 |
| Fantina | 13.2 | 7 | 14 |
| Maylene | 11.4 | 9 | 17 |
| Wake | 21.9 | 14 | 9 |
| Byron | 18.3 | 15 | 17 |
| Candice | 8.7 | 10 | 6 |
| HQ | 3.6 | 5 | 8 |
| Galactic | 20.1 | 13 | 5 |
| Volkner | 6.0 | 2 | 3 |
| Barry | 8.1 | 9 | 5 |
| League | 0.0 | 0 | 0 |

Ian's timing notes (2026-10-06), each kept as judgement, not a rule:

- Confuse Ray: from Wake's split at the earliest, now Wake; Ian: "way, way too good of a move to get this early" in Sandgem; he rates it fantastic, so it comes after Charm.
- Charm: from Maylene's split at the earliest, now Wake; Ian: "a lot of good moves ... in Gardenia split; a couple should be moved"; he rates it incredible, and it halves a physical threat.
- Knock Off: from Fantina's split at the earliest, now Maylene; the same note: the strongest utility attack in Gardenia's split, its item removal a second effect.
- Will-O-Wisp: from Maylene's split at the earliest, now Wake; Ian: "too good for fantina split".
- Thunder Wave: from Maylene's split at the earliest, now Wake; Ian: "same for thunder wave".

The TMs whose split or source changed from the first draft:

| TM | Move | Then | Now |
|---|---|---|---|
| TM06 | Toxic | Wake, ball | Roark, gift |
| TM51 | Roost | Maylene, gift | Roark, ball |
| TM87 | Swagger | Wake, ball | Roark, ball |
| TM90 | Block | Fantina, ball | Roark, gift |
| TM92 | Trick Room | Wake, gift | Roark, ball |
| TM19 | Giga Drain | Byron, ball | Gardenia, gift |
| TM31 | Brick Break | Fantina, ball | Gardenia, gift |
| TM40 | Aerial Ace | Maylene, reward trainer | Gardenia, reward trainer |
| TM42 | Facade | Maylene, gift | Gardenia, gift |
| TM47 | Steel Wing | Maylene, ball | Gardenia, gift |
| TM57 | Charge Beam | Maylene, reward trainer | Gardenia, reward trainer |
| TM62 | Silver Wind | Gardenia, reward trainer | Gardenia, reward trainer |
| TM66 | Payback | Gardenia, reward trainer | Gardenia, reward trainer |
| TM88 | Pluck | Gardenia, reward trainer | Gardenia, reward trainer |
| HM04 | Strength | Byron, gift | Fantina, ball |
| TM12 | Taunt | Gardenia, ball | Fantina, ball |
| TM60 | Drain Punch | Maylene, gift | Fantina, ball |
| TM76 | Stealth Rock | Roark, gift | Fantina, ball |
| TM79 | Dark Pulse | Barry, ball | Fantina, ball |
| TM91 | Flash Cannon | Byron, gift | Fantina, gift |
| TM10 | Hidden Power | Maylene, reward trainer | Maylene, reward trainer |
| TM20 | Safeguard | Fantina, ball | Maylene, gift |
| TM22 | SolarBeam | Maylene, reward trainer | Maylene, reward trainer |
| TM28 | Dig | Wake, ball | Maylene, reward trainer |
| TM30 | Shadow Ball | Byron, ball | Maylene, reward trainer |
| TM32 | Zen Headbutt | Wake, ball | Maylene, ball |
| TM46 | Knock Off | Gardenia, ball | Maylene, gift |
| TM65 | Shadow Claw | Fantina, gift | Maylene, ball |
| TM02 | Dragon Claw | Maylene, gift | Wake, ball |
| TM05 | Dazzling Gleam | Fantina, ball | Wake, ball |
| TM41 | Charm | Gardenia, ball | Wake, Game Corner prize, once |
| TM44 | Wild Charge | Wake, ball | Wake, ball |
| TM45 | Alluring Voice | Byron, gift | Wake, ball |
| TM59 | Dragon Pulse | Barry, ball | Wake, ball |
| TM61 | Will-O-Wisp | Fantina, ball | Wake, ball |
| TM63 | Confuse Ray | Roark, gift | Wake, Game Corner prize, once |
| TM72 | Avalanche | Wake, reward trainer | Wake, reward trainer |
| TM73 | Thunder Wave | Fantina, ball | Wake, ball |
| TM81 | X-Scissor | Byron, ball | Wake, ball |
| TM82 | Bounce | Maylene, ball | Wake, gift |
| TM83 | Expanding Force | Maylene, ball | Wake, ball |
| TM84 | Poison Jab | Byron, ball | Wake, ball |
| HM02 | Fly | HQ, ball | Byron, Department Store, once |
| TM11 | Spite | Gardenia, gift | Byron, gift |
| TM17 | StompingTantrum | Gardenia, gift | Byron, ball |
| TM23 | Iron Tail | Byron, ball | Byron, Department Store, once |
| TM26 | Earthquake | Byron, ball | Byron, Department Store, once |
| TM29 | Psychic | HQ, ball | Byron, Game Corner prize, once |
| TM35 | Flamethrower | Byron, ball | Byron, Department Store, once |
| TM36 | Sludge Bomb | HQ, ball | Byron, Game Corner prize, once |
| TM53 | Energy Ball | Galactic, ball | Byron, Department Store, once |
| TM54 | False Swipe | Maylene, ball | Byron, ball |
| TM67 | Ice Punch | Candice, gift | Byron, Department Store, once |
| TM71 | Stone Edge | Barry, ball | Byron, Department Store, once |
| TM77 | Foul Play | Byron, ball | Byron, Department Store, once |
| TM85 | Skitter Smack | Fantina, ball | Byron, gift |
| TM94 | Psybeam | Fantina, ball | Byron, gift |
| HM05 | Defog | Maylene, ball | Candice, ball |
| HM08 | Rock Climb | Candice, ball | Candice, Game Corner prize, once |
| TM07 | Curse | Byron, ball | Candice, Game Corner prize, once |
| TM13 | Ice Beam | HQ, ball | Candice, Game Corner prize, once |
| TM16 | Light Screen | Fantina, ball | Candice, ball |
| TM49 | Agility | Candice, ball | Candice, Game Corner prize, once |
| TM55 | Brine | Wake, gift | Candice, ball |
| TM64 | Play Rough | Candice, ball | Candice, Game Corner prize, once |
| TM74 | Gyro Ball | Maylene, gift | Candice, ball |
| TM80 | Rock Slide | Galactic, ball | Candice, ball |
| TM18 | Scary Face | Gardenia, gift | HQ, ball |
| TM33 | Reflect | Fantina, ball | HQ, ball |
| TM37 | Signal Beam | Wake, ball | HQ, ball |
| TM43 | Secret Power | Fantina, ball | HQ, ball |
| TM56 | Hex | Candice, ball | HQ, ball |
| HM03 | Surf | Byron, gift | Galactic, reward trainer |
| HM07 | Waterfall | Volkner, gift | Galactic, reward trainer |
| TM01 | Hydro Pump | Galactic, gift | Galactic, reward trainer |
| TM14 | Blizzard | HQ, ball | Galactic, gift |
| TM21 | Frustration | HQ, ball | Galactic, reward trainer |
| TM25 | Thunder | HQ, ball | Galactic, reward trainer |
| TM27 | Return | HQ, ball | Galactic, reward trainer |
| TM38 | Fire Blast | Galactic, ball | Galactic, ball |
| TM50 | Overheat | Galactic, ball | Galactic, reward trainer |
| TM58 | Triple Axel | Volkner, gift | Galactic, reward trainer |
| TM69 | Rock Polish | Candice, ball | Galactic, reward trainer |
| TM70 | Outrage | Barry, ball | Galactic, ball |
| TM75 | Meteor Beam | Barry, ball | Galactic, ball |
| TM04 | Calm Mind | Byron, gift | Volkner, gift |
| TM24 | Thunderbolt | Byron, ball | Volkner, gift |
| TM08 | Bulk Up | Byron, ball | Barry, Game Corner prize, once |
| TM15 | Hyper Beam | Maylene, ball | Barry, Department Store, once |
| TM48 | Iron Defense | Roark, gift | Barry, ball |
| TM52 | Focus Blast | Volkner, gift | Barry, Department Store, once |
| TM68 | Giga Impact | Maylene, gift | Barry, Department Store, once |
| TM78 | Captivate | Gardenia, gift | Barry, ball |
| TM86 | Grass Knot | Gardenia, gift | Barry, ball |
| TM89 | U-turn | Byron, ball | Barry, ball |
| TM93 | Psychic Noise | Fantina, ball | Barry, ball |

## The TM list

One row per TM, by the split it first comes in. A number past 92 is new; a number vanilla used for a move that leaves the list now teaches the new move named. Power and accuracy are Oxide's today.

| TM | Move | Type | Class | Power | Accuracy | Tier | Copies | Split | Source |
|---|---|---|---|---|---|---|---|---|---|
| TM06 | Toxic | Poison | Status | - | 100 | strong | 1 | Roark | gift, Oreburgh City Gym |
| TM51 | Roost | Flying | Status | - | never misses | strong | 1 | Roark | ball, Jubilife City |
| TM87 | Swagger | Normal | Status | - | 90 | strong | 1 | Roark | ball, Trainers School |
| TM90 | Block | Normal | Status | - | never misses | strong | 1 | Roark | gift, Sandgem Town |
| TM92 | Trick Room | Psychic | Status | - | never misses | utility | 2 | Roark | ball, Oreburgh Mine B1F |
| TM09 | Bullet Seed | Grass | Physical | 25 | 100 | utility | 2 | Gardenia | ball, Route 204 North |
| TM19 | Giga Drain | Grass | Special | 75 | 100 | utility | 2 | Gardenia | gift, Eterna City Condominiums 2F |
| TM31 | Brick Break | Fighting | Physical | 75 | 100 | utility | 2 | Gardenia | gift, Eterna City |
| TM39 | Rock Tomb | Rock | Physical | 60 | 100 | utility | 2 | Gardenia | ball, Ravaged Path |
| TM40 | Aerial Ace | Flying | Physical | 60 | never misses | weak | 1 | Gardenia | reward trainer |
| TM42 | Facade | Normal | Physical | 70 | 100 | utility | 2 | Gardenia | gift, Eterna City Gym |
| TM47 | Steel Wing | Steel | Physical | 70 | 90 | utility | 2 | Gardenia | gift, Floaroma Town Middle House |
| TM57 | Charge Beam | Electric | Special | 50 | 100 | weak | 1 | Gardenia | reward trainer |
| TM62 | Silver Wind | Bug | Special | 60 | 100 | weak | 1 | Gardenia | reward trainer |
| TM66 | Payback | Dark | Physical | 60 | 100 | weak | 1 | Gardenia | reward trainer |
| TM88 | Pluck | Flying | Physical | 60 | 100 | weak | 1 | Gardenia | reward trainer |
| HM04 | Strength | Normal | Physical | 80 | 100 | utility | 2 | Fantina | ball, Old Chateau Back East Room |
| TM03 | Water Pulse | Water | Special | 60 | 100 | weak | 1 | Fantina | reward trainer |
| TM12 | Taunt | Dark | Status | - | 100 | utility | 2 | Fantina | ball, Route 206 |
| TM60 | Drain Punch | Fighting | Physical | 75 | 100 | utility | 2 | Fantina | ball, Wayward Cave 1F |
| TM76 | Stealth Rock | Rock | Status | - | never misses | utility | 2 | Fantina | ball, Route 208 |
| TM79 | Dark Pulse | Dark | Special | 80 | 100 | utility | 2 | Fantina | ball, Amity Square |
| TM91 | Flash Cannon | Steel | Special | 80 | 100 | utility | 2 | Fantina | gift, Hearthome City Gym Leader Room |
| TM10 | Hidden Power | Normal | Special | varies | 100 | weak | 1 | Maylene | reward trainer |
| TM20 | Safeguard | Normal | Status | - | never misses | utility | 2 | Maylene | gift, Veilstone City |
| TM22 | SolarBeam | Grass | Special | 120 | 100 | weak | 1 | Maylene | reward trainer |
| TM28 | Dig | Ground | Physical | 60 | 100 | weak | 1 | Maylene | reward trainer |
| TM30 | Shadow Ball | Ghost | Special | 80 | 100 | utility | 2 | Maylene | reward trainer |
| TM32 | Zen Headbutt | Psychic | Physical | 80 | 100 | utility | 2 | Maylene | ball, Route 209 |
| TM34 | Shock Wave | Electric | Special | 60 | never misses | weak | 1 | Maylene | reward trainer |
| TM46 | Knock Off | Dark | Physical | 70 | 100 | utility | 2 | Maylene | gift, Route 210 South |
| TM65 | Shadow Claw | Ghost | Physical | 70 | 100 | utility | 2 | Maylene | ball, Route 215 |
| TM02 | Dragon Claw | Dragon | Physical | 80 | 100 | utility | 2 | Wake | ball, Ruin Maniac Cave Short |
| TM05 | Dazzling Gleam | Fairy | Special | 80 | 100 | utility | 2 | Wake | ball, Route 213 |
| TM41 | Charm | Fairy | Status | - | 100 | strong | 1 | Wake | Game Corner prize, once, Veilstone City Prize Exchange |
| TM44 | Wild Charge | Electric | Physical | 90 | 100 | utility | 2 | Wake | ball, Great Marsh 5 |
| TM45 | Alluring Voice | Fairy | Special | 80 | 100 | utility | 2 | Wake | ball, Route 212 South |
| TM59 | Dragon Pulse | Dragon | Special | 85 | 100 | utility | 2 | Wake | ball, Pokemon Mansion Office |
| TM61 | Will-O-Wisp | Fire | Status | - | 85 | strong | 1 | Wake | ball, Route 212 South |
| TM63 | Confuse Ray | Ghost | Status | - | 100 | strong | 1 | Wake | Game Corner prize, once, Veilstone City Prize Exchange |
| TM72 | Avalanche | Ice | Physical | 60 | 100 | weak | 1 | Wake | reward trainer |
| TM73 | Thunder Wave | Electric | Status | - | 100 | strong | 1 | Wake | ball, Route 212 North |
| TM81 | X-Scissor | Bug | Physical | 80 | 100 | utility | 2 | Wake | ball, Great Marsh 4 |
| TM82 | Bounce | Flying | Physical | 85 | 100 | utility | 2 | Wake | gift, Pastoria City Gym |
| TM83 | Expanding Force | Psychic | Special | 80 | 100 | utility | 2 | Wake | ball, Great Marsh 1 |
| TM84 | Poison Jab | Poison | Physical | 80 | 100 | utility | 2 | Wake | ball, Great Marsh 3 |
| HM02 | Fly | Flying | Physical | 90 | 95 | strong | 1 | Byron | Department Store, once, Veilstone Store 3F |
| TM11 | Spite | Ghost | Status | - | 100 | utility | 2 | Byron | gift, Celestic Town Cave |
| TM17 | StompingTantrum | Ground | Physical | 75 | 100 | utility | 2 | Byron | ball, Canalave City |
| TM23 | Iron Tail | Steel | Physical | 100 | 75 | strong | 1 | Byron | Department Store, once, Veilstone Store 3F |
| TM26 | Earthquake | Ground | Physical | 100 | 100 | strong | 1 | Byron | Department Store, once, Veilstone Store 3F |
| TM29 | Psychic | Psychic | Special | 90 | 100 | strong | 1 | Byron | Game Corner prize, once, Veilstone City Prize Exchange |
| TM35 | Flamethrower | Fire | Special | 90 | 100 | strong | 1 | Byron | Department Store, once, Veilstone Store 3F |
| TM36 | Sludge Bomb | Poison | Special | 90 | 100 | strong | 1 | Byron | Game Corner prize, once, Veilstone City Prize Exchange |
| TM53 | Energy Ball | Grass | Special | 90 | 100 | strong | 1 | Byron | Department Store, once, Veilstone Store 3F |
| TM54 | False Swipe | Normal | Physical | 40 | 100 | utility | 2 | Byron | ball, Fuego Ironworks Building |
| TM67 | Ice Punch | Ice | Physical | 95 | 100 | strong | 1 | Byron | Department Store, once, Veilstone Store 3F |
| TM71 | Stone Edge | Rock | Physical | 100 | 80 | strong | 1 | Byron | Department Store, once, Veilstone Store 3F |
| TM77 | Foul Play | Dark | Physical | 95 | 100 | strong | 1 | Byron | Department Store, once, Veilstone Store 3F |
| TM85 | Skitter Smack | Bug | Physical | 70 | 100 | utility | 2 | Byron | gift, Canalave City Gym |
| TM94 | Psybeam | Psychic | Special | 65 | 100 | utility | 2 | Byron | gift, Canalave City Southeast House |
| HM05 | Defog | Flying | Status | - | never misses | utility | 2 | Candice | ball, Route 217 |
| HM08 | Rock Climb | Normal | Physical | 90 | 100 | strong | 1 | Candice | Game Corner prize, once, Veilstone City Prize Exchange |
| TM07 | Curse | Mystery | Status | - | never misses | strong | 1 | Candice | Game Corner prize, once, Veilstone City Prize Exchange |
| TM13 | Ice Beam | Ice | Special | 90 | 100 | strong | 1 | Candice | Game Corner prize, once, Veilstone City Prize Exchange |
| TM16 | Light Screen | Psychic | Status | - | never misses | utility | 2 | Candice | ball, Route 217 |
| TM49 | Agility | Psychic | Status | - | never misses | strong | 1 | Candice | Game Corner prize, once, Veilstone City Prize Exchange |
| TM55 | Brine | Water | Special | 65 | 100 | utility | 2 | Candice | ball, Oreburgh Gate B1F |
| TM64 | Play Rough | Fairy | Physical | 90 | 100 | strong | 1 | Candice | Game Corner prize, once, Veilstone City Prize Exchange |
| TM74 | Gyro Ball | Steel | Physical | varies | 100 | utility | 2 | Candice | ball, Mt Coronet 1F North Room 1 |
| TM80 | Rock Slide | Rock | Physical | 75 | 90 | utility | 2 | Candice | ball, Lake Acuity |
| TM18 | Scary Face | Normal | Status | - | 100 | utility | 2 | HQ | ball, Route 211 East |
| TM33 | Reflect | Psychic | Status | - | never misses | utility | 2 | HQ | ball, Route 213 |
| TM37 | Signal Beam | Bug | Special | 75 | 100 | utility | 2 | HQ | ball, Galactic Hq 1F |
| TM43 | Secret Power | Normal | Physical | 70 | 100 | utility | 2 | HQ | ball, Galactic Hq 3F |
| TM56 | Hex | Ghost | Special | 65 | 100 | utility | 2 | HQ | ball, Galactic Hq B2F |
| HM03 | Surf | Water | Special | 90 | 100 | strong | 1 | Galactic | reward trainer |
| HM07 | Waterfall | Water | Physical | 80 | 100 | strong | 1 | Galactic | reward trainer |
| TM01 | Hydro Pump | Water | Special | 110 | 80 | strong | 1 | Galactic | reward trainer |
| TM14 | Blizzard | Ice | Special | 110 | 70 | strong | 1 | Galactic | gift, Survival Area South House |
| TM21 | Frustration | Normal | Physical | varies | 100 | strong | 1 | Galactic | reward trainer |
| TM25 | Thunder | Electric | Special | 110 | 70 | strong | 1 | Galactic | reward trainer |
| TM27 | Return | Normal | Physical | varies | 100 | strong | 1 | Galactic | reward trainer |
| TM38 | Fire Blast | Fire | Special | 110 | 85 | strong | 1 | Galactic | ball, Mt Coronet 2F |
| TM50 | Overheat | Fire | Special | 130 | 90 | strong | 1 | Galactic | reward trainer |
| TM58 | Triple Axel | Ice | Physical | 20 | 90 | strong | 1 | Galactic | reward trainer |
| TM69 | Rock Polish | Rock | Status | - | never misses | strong | 1 | Galactic | reward trainer |
| TM70 | Outrage | Dragon | Physical | 140 | 100 | strong | 1 | Galactic | ball, Stark Mountain Room 2 |
| TM75 | Meteor Beam | Rock | Special | 120 | 100 | strong | 1 | Galactic | ball, Route 226 |
| TM04 | Calm Mind | Psychic | Status | - | never misses | strong | 1 | Volkner | gift, Sunyshore City |
| TM24 | Thunderbolt | Electric | Special | 90 | 100 | strong | 1 | Volkner | gift, Route 222 |
| TM08 | Bulk Up | Fighting | Status | - | never misses | strong | 1 | Barry | Game Corner prize, once, Veilstone City Prize Exchange |
| TM15 | Hyper Beam | Normal | Special | 180 | 100 | strong | 1 | Barry | Department Store, once, Veilstone Store 3F |
| TM48 | Iron Defense | Steel | Status | - | never misses | strong | 1 | Barry | ball, Victory Road 2F |
| TM52 | Focus Blast | Fighting | Special | 120 | 70 | strong | 1 | Barry | Department Store, once, Veilstone Store 3F |
| TM68 | Giga Impact | Normal | Physical | 180 | 100 | strong | 1 | Barry | Department Store, once, Veilstone Store 3F |
| TM78 | Captivate | Normal | Status | - | 100 | utility | 2 | Barry | ball, Victory Road B1F |
| TM86 | Grass Knot | Grass | Special | varies | 100 | utility | 2 | Barry | ball, Victory Road 1F |
| TM89 | U-turn | Bug | Physical | 70 | 100 | utility | 2 | Barry | ball, Victory Road 2F |
| TM93 | Psychic Noise | Psychic | Special | 75 | 100 | utility | 2 | Barry | ball, Route 223 |

## What changed against vanilla

**Kept** (94): TM01 Hydro Pump, TM02 Dragon Claw, TM03 Water Pulse, TM04 Calm Mind, TM05 Dazzling Gleam, TM06 Toxic, TM07 Curse, TM08 Bulk Up, TM09 Bullet Seed, TM10 Hidden Power, TM11 Spite, TM12 Taunt, TM13 Ice Beam, TM14 Blizzard, TM15 Hyper Beam, TM16 Light Screen, TM17 StompingTantrum, TM18 Scary Face, TM19 Giga Drain, TM20 Safeguard, TM21 Frustration, TM22 SolarBeam, TM23 Iron Tail, TM24 Thunderbolt, TM25 Thunder, TM26 Earthquake, TM27 Return, TM28 Dig, TM29 Psychic, TM30 Shadow Ball, TM31 Brick Break, TM32 Zen Headbutt, TM33 Reflect, TM34 Shock Wave, TM35 Flamethrower, TM36 Sludge Bomb, TM37 Signal Beam, TM38 Fire Blast, TM39 Rock Tomb, TM40 Aerial Ace, TM41 Charm, TM42 Facade, TM43 Secret Power, TM44 Wild Charge, TM45 Alluring Voice, TM46 Knock Off, TM47 Steel Wing, TM48 Iron Defense, TM49 Agility, TM50 Overheat, TM51 Roost, TM52 Focus Blast, TM53 Energy Ball, TM54 False Swipe, TM55 Brine, TM56 Hex, TM57 Charge Beam, TM58 Triple Axel, TM59 Dragon Pulse, TM60 Drain Punch, TM61 Will-O-Wisp, TM62 Silver Wind, TM63 Confuse Ray, TM64 Play Rough, TM65 Shadow Claw, TM66 Payback, TM67 Ice Punch, TM68 Giga Impact, TM69 Rock Polish, TM70 Outrage, TM71 Stone Edge, TM72 Avalanche, TM73 Thunder Wave, TM74 Gyro Ball, TM75 Meteor Beam, TM76 Stealth Rock, TM77 Foul Play, TM78 Captivate, TM79 Dark Pulse, TM80 Rock Slide, TM81 X-Scissor, TM82 Bounce, TM83 Expanding Force, TM84 Poison Jab, TM85 Skitter Smack, TM86 Grass Knot, TM87 Swagger, TM88 Pluck, TM89 U-turn, TM90 Block, TM91 Flash Cannon, TM92 Trick Room, TM93 Psychic Noise, TM94 Psybeam.

**Former HMs**, single-use TMs now that field moves work on the badge alone: HM02 Fly (buff proposed: accuracy 95 to 100, so the two-turn hit no longer misses), HM03 Surf, HM04 Strength (buff proposed: power 80 to 90, a clean Normal hit between Body Slam and Double-Edge), HM05 Defog (buff proposed: clears hazards on both sides, as the later games do, to answer the trainers' hazards), HM07 Waterfall, HM08 Rock Climb (buff proposed: accuracy 85 to 95, so its confusion chance rides on a hit that lands). Cut and Rock Smash leave.

**Cut**:


**New**, ranked by the lines without a niche each gives a real option, then by lines gained:

| TM | Move | Why |
|---|---|---|
| TM01 | Hydro Pump | 56 lines gain it that cannot learn it by level-up, 11 of them lines no boss takes today |
| TM05 | Dazzling Gleam | 30 lines gain it that cannot learn it by level-up, 9 of them lines no boss takes today |
| TM07 | Curse | 48 lines gain it that cannot learn it by level-up, 8 of them lines no boss takes today |
| TM11 | Spite | 35 lines gain it that cannot learn it by level-up, 8 of them lines no boss takes today |
| TM17 | StompingTantrum | 58 lines gain it that cannot learn it by level-up, 7 of them lines no boss takes today |
| TM18 | Scary Face | 50 lines gain it that cannot learn it by level-up, 7 of them lines no boss takes today |
| TM32 | Zen Headbutt | 39 lines gain it that cannot learn it by level-up, 6 of them lines no boss takes today |
| TM37 | Signal Beam | 37 lines gain it that cannot learn it by level-up, 9 of them lines no boss takes today |
| TM41 | Charm | 31 lines gain it that cannot learn it by level-up, 7 of them lines no boss takes today |
| TM44 | Wild Charge | 19 lines gain it that cannot learn it by level-up, 6 of them lines no boss takes today |
| TM45 | Alluring Voice | 15 lines gain it that cannot learn it by level-up, 5 of them lines no boss takes today |
| TM46 | Knock Off | 55 lines gain it that cannot learn it by level-up, 6 of them lines no boss takes today |
| TM48 | Iron Defense | 38 lines gain it that cannot learn it by level-up, 5 of them lines no boss takes today |
| TM49 | Agility | 30 lines gain it that cannot learn it by level-up, 5 of them lines no boss takes today |
| TM56 | Hex | 26 lines gain it that cannot learn it by level-up, 6 of them lines no boss takes today |
| TM58 | Triple Axel | 15 lines gain it that cannot learn it by level-up, 4 of them lines no boss takes today |
| TM63 | Confuse Ray | 20 lines gain it that cannot learn it by level-up, 4 of them lines no boss takes today |
| TM64 | Play Rough | 19 lines gain it that cannot learn it by level-up, 4 of them lines no boss takes today |
| TM67 | Ice Punch | 41 lines gain it that cannot learn it by level-up, 2 of them lines no boss takes today |
| TM70 | Outrage | 30 lines gain it that cannot learn it by level-up, 4 of them lines no boss takes today |
| TM75 | Meteor Beam | 27 lines gain it that cannot learn it by level-up, 4 of them lines no boss takes today |
| TM77 | Foul Play | 35 lines gain it that cannot learn it by level-up, 5 of them lines no boss takes today |
| TM82 | Bounce | 16 lines gain it that cannot learn it by level-up, 2 of them lines no boss takes today |
| TM83 | Expanding Force | 17 lines gain it that cannot learn it by level-up, 3 of them lines no boss takes today |
| TM85 | Skitter Smack | 17 lines gain it that cannot learn it by level-up, 5 of them lines no boss takes today |
| TM90 | Block | 16 lines gain it that cannot learn it by level-up, 4 of them lines no boss takes today |
| TM93 | Psychic Noise | 19 lines gain it that cannot learn it by level-up, 5 of them lines no boss takes today |
| TM94 | Psybeam | 17 lines gain it that cannot learn it by level-up, 4 of them lines no boss takes today |

Just below the line: Tera Blast (155 lines), Uproar (54 lines), Hyper Voice (33 lines), Seed Bomb (33 lines), Earth Power (34 lines), Acrobatics (33 lines), Aqua Tail (29 lines), Poltergeist (14 lines), ThunderPunch (46 lines), Body Press (42 lines), Iron Head (28 lines), Encore (27 lines), Hurricane (27 lines), Gunk Shot (26 lines), Psyshock (26 lines).

Left out as doing the same job as a TM in the list: Body Slam (beside Facade), Take Down (beside Facade), Headbutt (beside Facade), Double-Edge (beside Frustration), Liquidation (beside Waterfall), Dive (beside Waterfall), Icicle Spear (beside Avalanche), Scald (beside Surf), Assurance (beside Payback), Retaliate (beside Facade), Low Sweep (beside Brick Break), Muddy Water (beside Surf), Leaf Storm (beside Energy Ball), Lunge (beside Skitter Smack), Water Pledge (beside Surf), Heat Wave (beside Fire Blast), Sky Attack (beside Fly), Brave Bird (beside Fly), Hydro Cannon (beside Hydro Pump), Swift (beside Hidden Power).

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
| Silk Scarf | Maylene | Jogger Raul | Route 209 | 2.3 |
| Safety Goggles | Maylene | Pkmn Breeder Kahlil | Route 210 South | 2.4 |
| Weakness Policy | Wake | Scientist Shaun | Route 212 South | 3.2 |
| Wide Lens | Wake | Fisherman Josh | Route 212 South | 3.4 |
| Covert Cloak | Wake | Fisherman Kenneth | Route 213 | 3.2 |
| Eject Button | Wake | Tuber Trenton | Route 219 | 2.9 |
| Red Card | Wake | Tuber Mariel | Route 219 | 2.8 |
| Mirror Herb | Byron | Swimmer♀ Jessica | Route 220 | 2.7 |
| Zoom Lens | Byron | Swimmer♂ Adrian | Route 220 | 2.7 |
| Clear Amulet | Byron | Fisherman Cory | Route 221 | 2.7 |
| Metronome | Candice | Galactic Grunt | Lake Valor Drained | 2.3 |
| Ring Target | Candice | Ace Trainer Blake | Route 216 | 2.4 |
| Ability Shield | Candice | Skier Lexie | Route 217 | 2.4 |
| Pixie Plate | Volkner | Beauty Nicola | Route 222 | 2.3 |
| TM66 Payback | Gardenia | Fisherman Zachary | Route 205 North | 2.3 |
| TM88 Pluck | Gardenia | Fisherman Joseph | Route 205 North | 2.3 |
| TM40 Aerial Ace | Gardenia | Picnicker Karina | Route 205 South | 2.3 |
| TM57 Charge Beam | Gardenia | Camper Zackary | Route 205 South | 2.3 |
| TM62 Silver Wind | Gardenia | Hiker Louis | Route 211 West | 2.3 |
| TM03 Water Pulse | Fantina | Hiker Theodore | Route 206 | 2.3 |
| TM28 Dig | Maylene | Collector Edwin | Cafe | 2.3 |
| TM30 Shadow Ball | Maylene | a new trainer (the main track) | Game Corner | Shadow Ball, utility; in place of the gift for ten straight bonus rounds (ITEM_TM64), a new optional trainer |
| TM10 Hidden Power | Maylene | Jogger Wyatt | Route 210 South | 2.3 |
| TM22 SolarBeam | Maylene | Ruin Maniac Calvin | Route 215 | 2.3 |
| TM34 Shock Wave | Maylene | Jogger Scott | Route 215 | 2.3 |
| TM72 Avalanche | Wake | PI Carlos | Route 214 | 2.3 |
| TM01 Hydro Pump | Galactic | Ace Trainer Deanna | Route 225 | 3.2 |
| TM25 Thunder | Galactic | Ace Trainer Quinn | Route 225 | 3.2 |
| TM27 Return | Galactic | Bird Keeper Geneva | Route 226 | 2.8 |
| TM58 Triple Axel | Galactic | Ace Trainer Jose | Route 228 | 3.2 |
| TM69 Rock Polish | Galactic | Ace Trainer Meagan | Route 228 | 2.6 |
| TM21 Frustration | Galactic | Pkmn Ranger Deshawn | Route 229 | 2.9 |
| TM50 Overheat | Galactic | Swimmer♂ Sam | Route 230 | 3.0 |
| TM58 Triple Axel | Galactic | Swimmer♀ Mallory | Route 230 | 3.1 |

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

## The Department Store and the Game Corner

Ian, 2026-10-06: each TM they sell unlocks at a badge count, in order of usefulness, and can be bought once, like any other placement. Veilstone opens in Maylene's split with three badges, so the counts run from 3 to 8; the spread chose each TM's count, and the strongest come last. Prices stay vanilla's.

| Badges | Split | Department Store | Game Corner |
|---|---|---|---|
| 3 | Maylene | - | - |
| 4 | Wake | - | TM41 Charm, TM41 Charm, TM63 Confuse Ray, TM63 Confuse Ray |
| 5 | Byron | HM02 Fly, TM23 Iron Tail, TM26 Earthquake, TM35 Flamethrower, TM53 Energy Ball, TM67 Ice Punch, TM67 Ice Punch, TM71 Stone Edge, TM77 Foul Play, TM77 Foul Play | TM07 Curse, TM29 Psychic, TM36 Sludge Bomb, TM49 Agility, TM64 Play Rough |
| 6 | Candice | - | HM08 Rock Climb, TM07 Curse, TM13 Ice Beam, TM49 Agility, TM64 Play Rough |
| 7 | HQ | - | - |
| 8 | Barry | TM15 Hyper Beam, TM52 Focus Blast, TM68 Giga Impact | TM08 Bulk Up |

The Game Corner's held items (Silk Scarf, Wide Lens, Zoom Lens, Metronome) move to optional fights, and their prize slots are dropped (Ian, 2026-10-06); the table marks each with reward ITEM_NONE and no copies. The prizes that were neither a TM nor a held item stay as they are.

## Strong TMs held back

A strong TM comes no earlier than the split each flagged line that learns it has a good attack of its type by level-up, Byron's at the latest. These reach flagged stages with none by then:

- Blizzard: Absol, Arceus, Articuno, Blastoise, Castform, Cranidos, Darkrai, Dialga and 28 more
- Earthquake: Aerodactyl, Arceus, Armaldo, Blastoise, Blaziken, Charizard, Cranidos, Dhelmise and 35 more
- Energy Ball: Abra, Alakazam, Arceus, Armarouge, Castform, Chandelure, Chimecho, Gallade and 13 more
- Fire Blast: Absol, Aerodactyl, Arceus, Castform, Cranidos, Dialga, Flygon, Garchomp and 15 more
- Flamethrower: Absol, Aerodactyl, Arceus, Castform, Cranidos, Dialga, Electivire, Flygon and 17 more
- Fly: Arceus, Articuno, Chatot, Moltres, Togekiss, Volcarona, Zapdos
- Focus Blast: Alakazam, Ampharos, Annihilape, Arceus, Armarouge, Blaziken, Charizard, Cinccino and 29 more
- Foul Play: Abra, Absol, Alakazam, Alolan Ninetales, Ambipom, Arceus, Darkrai, Delphox and 14 more
- Frustration: Abra, Absol, Alakazam, Ampharos, Arceus, Armaldo, Articuno, Blastoise and 68 more
- Giga Impact: Absol, Alakazam, Alolan Ninetales, Ampharos, Arboliva, Arceus, Armaldo, Articuno and 91 more
- Hydro Pump: Arceus, Castform, Dhelmise, Feraligatr, Floatzel, Grapploct, Hisuian Goodra, Kabutops and 7 more
- Hyper Beam: Absol, Alakazam, Alolan Ninetales, Ampharos, Arboliva, Arceus, Armaldo, Articuno and 92 more
- Ice Beam: Absol, Arceus, Articuno, Blastoise, Castform, Cranidos, Darkrai, Dialga and 29 more
- Ice Punch: Abra, Alakazam, Ambipom, Ampharos, Annihilape, Blastoise, Electabuzz, Electivire and 32 more
- Iron Tail: Abra, Absol, Alakazam, Ambipom, Annihilape, Arceus, Armaldo, Azumarill and 44 more
- Meteor Beam: Aerodactyl, Ampharos, Arceus, Armaldo, Armarouge, Kabutops, Lunatone, Metagross and 4 more
- Outrage: Ampharos, Annihilape, Arceus, Blastoise, Charizard, Dialga, Feraligatr, Granbull and 14 more
- Overheat: Annihilape, Arceus, Dialga, Granbull, Moltres, Primeape, Solrock, Toucannon and 1 more
- Play Rough: Absol, Cinccino, Donphan, Liepard, Lopunny, Luxray, Meloetta, Minun and 5 more
- Psychic: Abra, Arceus, Armarouge, Chandelure, Darkrai, Electabuzz, Electivire, Florges and 19 more
- Return: Abra, Absol, Alakazam, Ampharos, Arceus, Armaldo, Articuno, Blastoise and 68 more
- Rock Climb: Ampharos, Arceus, Blastoise, Blaziken, Darkrai, Electabuzz, Electivire, Empoleon and 10 more
- Sludge Bomb: Arceus, Carnivine, Crawdaunt, Darkrai, Gengar, Glimmet, Goodra, Granbull and 8 more
- Stone Edge: Absol, Aerodactyl, Annihilape, Arceus, Armaldo, Blaziken, Breloom, Cranidos and 28 more
- Surf: Arceus, Dhelmise, Feraligatr, Floatzel, Garchomp, Grapploct, Hariyama, Hisuian Goodra and 15 more
- Thunder: Absol, Ambipom, Annihilape, Arceus, Castform, Cinccino, Cranidos, Darkrai and 28 more
- Thunderbolt: Absol, Ambipom, Annihilape, Arceus, Castform, Cinccino, Cranidos, Darkrai and 30 more
- Triple Axel: Ambipom, Articuno, Cinccino, Frosmoth, Gallade, Gardevoir, Glaceon, Lopunny and 7 more
- Waterfall: Arceus, Feraligatr, Floatzel, Grapploct, Kabutops, Palkia, Sharpedo, Starmie

# The TM list and the reward table (step 6, for Ian)

Written by `tools/oxide/balance/rewards.py` on the branch `balance-tm-pass`. It changes no game data;
the placement tool applies the approved table in step 10.

## Summary

**Outcome.** The TM list Ian approved on 2026-10-06 has 100 TMs: 66 of vanilla's 92 kept, the six HMs less Cut and Rock Smash as single-use TMs, and 28 new moves, their numbers fixed. 40 are strong (one copy), 50 utility (two copies) and 10 weak (one copy, each the reward for one optional trainer). This version carries Ian's answers of the same day: his four timing notes; an even spread across the splits by their length (63 TMs by the end of Byron's split, where the first draft had 73); and the Department Store's and the Game Corner's 28 TMs sold once each, unlocked by badge count in order of usefulness. Every TM and each of element 7's 24 held items has exactly one place, every vanilla TM ball, gift and shop TM is repointed, and the reward trainers take 46 of the 46 spare story flags. The table's own check passes.

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
| TM01 | Focus Punch | Hydro Pump | Galactic | Focus Punch left (Ian's removal); new: 56 lines gain it that cannot learn it by level-up, 11 of them lines no boss takes |
| TM02 | Dragon Claw | Dragon Claw | Wake |  |
| TM03 | Water Pulse | Water Pulse | Fantina |  |
| TM04 | Calm Mind | Calm Mind | Barry |  |
| TM05 | Roar | Dazzling Gleam | Wake | Roar left (a status move Ian rates under pretty solid); new: 22 lines gain it that cannot learn it by level-up, 9 of them lines no boss takes |
| TM06 | Toxic | Toxic | Roark |  |
| TM07 | Hail | Curse | Byron | Hail left (Ian's removal); new: 49 lines gain it that cannot learn it by level-up, 8 of them lines no boss takes |
| TM08 | Bulk Up | Bulk Up | Volkner |  |
| TM09 | Bullet Seed | Bullet Seed | Maylene |  |
| TM10 | Hidden Power | Hidden Power | Maylene |  |
| TM11 | Sunny Day | Spite | Fantina | Sunny Day left (Ian's removal); new: 35 lines gain it that cannot learn it by level-up, 8 of them lines no boss takes |
| TM12 | Taunt | Taunt | Byron |  |
| TM13 | Ice Beam | Ice Beam | Candice |  |
| TM14 | Blizzard | Blizzard | Galactic |  |
| TM15 | Hyper Beam | Hyper Beam | Barry |  |
| TM16 | Light Screen | Light Screen | Maylene |  |
| TM17 | Protect | StompingTantrum | Maylene | Protect left (Ian's removal); new: 59 lines gain it that cannot learn it by level-up, 7 of them lines no boss takes |
| TM18 | Rain Dance | Scary Face | Barry | Rain Dance left (Ian's removal); new: 48 lines gain it that cannot learn it by level-up, 7 of them lines no boss takes |
| TM19 | Giga Drain | Giga Drain | Volkner |  |
| TM20 | Safeguard | Safeguard | Candice |  |
| TM21 | Frustration | Frustration | Galactic |  |
| TM22 | SolarBeam | SolarBeam | Maylene |  |
| TM23 | Iron Tail | Iron Tail | Byron |  |
| TM24 | Thunderbolt | Thunderbolt | Byron |  |
| TM25 | Thunder | Thunder | Galactic |  |
| TM26 | Earthquake | Earthquake | Byron |  |
| TM27 | Return | Return | Galactic |  |
| TM28 | Dig | Dig | Fantina |  |
| TM29 | Psychic | Psychic | Byron |  |
| TM30 | Shadow Ball | Shadow Ball | Wake |  |
| TM31 | Brick Break | Brick Break | Gardenia |  |
| TM32 | Double Team | Zen Headbutt | Maylene | Double Team left (Ian's removal); new: 35 lines gain it that cannot learn it by level-up, 6 of them lines no boss takes |
| TM33 | Reflect | Reflect | HQ |  |
| TM34 | Shock Wave | Shock Wave | Maylene |  |
| TM35 | Flamethrower | Flamethrower | Byron |  |
| TM36 | Sludge Bomb | Sludge Bomb | Galactic |  |
| TM37 | Sandstorm | Signal Beam | Wake | Sandstorm left (Ian's removal); new: 33 lines gain it that cannot learn it by level-up, 7 of them lines no boss takes |
| TM38 | Fire Blast | Fire Blast | Galactic |  |
| TM39 | Rock Tomb | Rock Tomb | Roark |  |
| TM40 | Aerial Ace | Aerial Ace | Maylene |  |
| TM41 | Torment | Charm | Wake | Torment left (a status move Ian rates under pretty solid); new: 28 lines gain it that cannot learn it by level-up, 6 of them lines no boss takes |
| TM42 | Facade | Facade | Candice |  |
| TM43 | Secret Power | Secret Power | Gardenia |  |
| TM44 | Rest | Wild Charge | Fantina | Rest left (a status move Ian rates under pretty solid); new: 18 lines gain it that cannot learn it by level-up, 6 of them lines no boss takes |
| TM45 | Attract | Alluring Voice | Wake | Attract left (a status move Ian rates under pretty solid); new: 15 lines gain it that cannot learn it by level-up, 5 of them lines no boss takes |
| TM46 | Thief | Knock Off | Wake | Thief left (Ian's removal); new: 55 lines gain it that cannot learn it by level-up, 6 of them lines no boss takes |
| TM47 | Steel Wing | Steel Wing | Byron |  |
| TM48 | Skill Swap | Iron Defense | Volkner | Skill Swap left (Ian's removal); new: 37 lines gain it that cannot learn it by level-up, 5 of them lines no boss takes |
| TM49 | Snatch | Agility | Candice | Snatch left (Ian's removal); new: 29 lines gain it that cannot learn it by level-up, 4 of them lines no boss takes |
| TM50 | Overheat | Overheat | Galactic |  |
| TM51 | Roost | Roost | Roark |  |
| TM52 | Focus Blast | Focus Blast | Barry |  |
| TM53 | Energy Ball | Energy Ball | Byron |  |
| TM54 | False Swipe | False Swipe | Barry |  |
| TM55 | Brine | Brine | Maylene |  |
| TM56 | Fling | Hex | HQ | Fling left (hangs on a held item); new: 26 lines gain it that cannot learn it by level-up, 6 of them lines no boss takes |
| TM57 | Charge Beam | Charge Beam | Gardenia |  |
| TM58 | Endure | Triple Axel | Galactic | Endure left (a status move Ian rates under pretty solid); new: 23 lines gain it that cannot learn it by level-up, 5 of them lines no boss takes |
| TM59 | Dragon Pulse | Dragon Pulse | Wake |  |
| TM60 | Drain Punch | Drain Punch | Galactic |  |
| TM61 | Will-O-Wisp | Will-O-Wisp | Wake |  |
| TM62 | Silver Wind | Silver Wind | Gardenia |  |
| TM63 | Embargo | Confuse Ray | Wake | Embargo left (Ian's removal); new: 19 lines gain it that cannot learn it by level-up, 3 of them lines no boss takes |
| TM64 | Explosion | Play Rough | Galactic | Explosion left (the user faints, which in a nuzlocke is a death); new: 19 lines gain it that cannot learn it by level-up, 4 of them lines no boss takes |
| TM65 | Shadow Claw | Shadow Claw | Barry |  |
| TM66 | Payback | Payback | Gardenia |  |
| TM67 | Recycle | Ice Punch | Byron | Recycle left (a status move Ian rates under pretty solid); new: 41 lines gain it that cannot learn it by level-up, 3 of them lines no boss takes |
| TM68 | Giga Impact | Giga Impact | Gardenia |  |
| TM69 | Rock Polish | Rock Polish | Candice |  |
| TM70 | Flash | Outrage | HQ | Flash left (Ian's removal); new: 29 lines gain it that cannot learn it by level-up, 4 of them lines no boss takes |
| TM71 | Stone Edge | Stone Edge | Byron |  |
| TM72 | Avalanche | Avalanche | Wake |  |
| TM73 | Thunder Wave | Thunder Wave | Wake |  |
| TM74 | Gyro Ball | Gyro Ball | Volkner |  |
| TM75 | Swords Dance | Meteor Beam | Galactic | Swords Dance left (Ian's removal); new: 27 lines gain it that cannot learn it by level-up, 4 of them lines no boss takes |
| TM76 | Stealth Rock | Stealth Rock | Gardenia |  |
| TM77 | Psych Up | Foul Play | Byron | Psych Up left (a status move Ian rates under pretty solid); new: 34 lines gain it that cannot learn it by level-up, 5 of them lines no boss takes |
| TM78 | Captivate | Captivate | Wake |  |
| TM79 | Dark Pulse | Dark Pulse | Fantina |  |
| TM80 | Rock Slide | Rock Slide | Byron |  |
| TM81 | X-Scissor | X-Scissor | Wake |  |
| TM82 | Sleep Talk | Bounce | Wake | Sleep Talk left (random, or hangs on a rare condition); new: 24 lines gain it that cannot learn it by level-up, 4 of them lines no boss takes |
| TM83 | Natural Gift | Expanding Force | Fantina | Natural Gift left (hangs on a held item); new: 18 lines gain it that cannot learn it by level-up, 4 of them lines no boss takes |
| TM84 | Poison Jab | Poison Jab | Fantina |  |
| TM85 | Dream Eater | Skitter Smack | Fantina | Dream Eater left (Ian's removal); new: 14 lines gain it that cannot learn it by level-up, 4 of them lines no boss takes |
| TM86 | Grass Knot | Grass Knot | Galactic |  |
| TM87 | Swagger | Swagger | Galactic |  |
| TM88 | Pluck | Pluck | Gardenia |  |
| TM89 | U-turn | U-turn | Wake |  |
| TM90 | Substitute | Block | Roark | Substitute left (Ian's removal); new: 16 lines gain it that cannot learn it by level-up, 4 of them lines no boss takes |
| TM91 | Flash Cannon | Flash Cannon | Wake |  |
| TM92 | Trick Room | Trick Room | Galactic |  |
| TM93 | - | Psychic Noise | Fantina | new: 17 lines gain it that cannot learn it by level-up, 4 of them lines no boss takes |
| TM94 | - | Psybeam | Candice | new: 17 lines gain it that cannot learn it by level-up, 4 of them lines no boss takes |
| HM01 | Cut | - | - | leaves the list (field moves work on the badge alone) |
| HM02 | Fly | Fly | Byron |  |
| HM03 | Surf | Surf | Barry |  |
| HM04 | Strength | Strength | Fantina |  |
| HM05 | Defog | Defog | Gardenia |  |
| HM06 | Rock Smash | - | - | leaves the list (field moves work on the badge alone) |
| HM07 | Waterfall | Waterfall | Galactic |  |
| HM08 | Rock Climb | Rock Climb | Candice |  |

## The spread

TMs by the split they first come in, against each split's share by its length (the trainers in it), and the first draft's count.

**What gates a TM's timing.** A TM attack comes no earlier than the split whose old power ceiling covers its power: the learnset generator's ceiling for a same-type attack, 60 in Roark's split, 75 in Gardenia's split, 80 in Fantina's split, 90 in Maylene's split, 90 in Wake's split, 100 in Byron's split, and more after. A hard gate, not a weight. A strong TM also waits for each flagged line that learns it to have a good attack of its type by level-up (Byron's split at the latest), and Ian's timing notes hold five moves later. The power gate is the lever to turn if TM timing feels off in the alpha.

| Split | Share | Now | First draft |
|---|---|---|---|
| Roark | 4.2 | 4 | 3 |
| Gardenia | 8.7 | 9 | 13 |
| Fantina | 10.3 | 10 | 14 |
| Maylene | 8.9 | 9 | 17 |
| Wake | 17.1 | 17 | 9 |
| Byron | 14.3 | 14 | 17 |
| Candice | 6.8 | 7 | 6 |
| HQ | 2.8 | 3 | 8 |
| Galactic | 15.7 | 16 | 5 |
| Volkner | 4.7 | 4 | 3 |
| Barry | 6.3 | 7 | 5 |
| League | 0.0 | 0 | 0 |

Ian's timing notes (2026-10-06), each kept as judgement, not a rule:

- Confuse Ray: from Wake's split at the earliest, now Wake; Ian: "way, way too good of a move to get this early" in Sandgem; he rates it fantastic, so it comes after Charm.
- Charm: from Maylene's split at the earliest, now Wake; Ian: "a lot of good moves ... in Gardenia split; a couple should be moved"; he rates it incredible, and it halves a physical threat.
- Knock Off: from Fantina's split at the earliest, now Wake; the same note: the strongest utility attack in Gardenia's split, its item removal a second effect.
- Will-O-Wisp: from Maylene's split at the earliest, now Wake; Ian: "too good for fantina split".
- Thunder Wave: from Maylene's split at the earliest, now Wake; Ian: "same for thunder wave".

The TMs whose split or source changed from the first draft:

| TM | Move | Then | Now |
|---|---|---|---|
| TM06 | Toxic | Wake, ball | Roark, gift |
| TM39 | Rock Tomb | Gardenia, ball | Roark, ball |
| TM51 | Roost | Maylene, gift | Roark, gift |
| TM90 | Block | Fantina, ball | Roark, gift |
| HM05 | Defog | Maylene, ball | Gardenia, gift |
| TM31 | Brick Break | Fantina, ball | Gardenia, gift |
| TM43 | Secret Power | Fantina, ball | Gardenia, gift |
| TM57 | Charge Beam | Maylene, reward trainer | Gardenia, reward trainer |
| TM66 | Payback | Gardenia, reward trainer | Gardenia, reward trainer |
| TM68 | Giga Impact | Maylene, gift | Gardenia, gift |
| TM76 | Stealth Rock | Roark, gift | Gardenia, ball |
| TM88 | Pluck | Gardenia, reward trainer | Gardenia, reward trainer |
| HM04 | Strength | Byron, gift | Fantina, gift |
| TM11 | Spite | Gardenia, gift | Fantina, ball |
| TM28 | Dig | Wake, ball | Fantina, ball |
| TM44 | Wild Charge | Wake, ball | Fantina, ball |
| TM79 | Dark Pulse | Barry, ball | Fantina, ball |
| TM83 | Expanding Force | Maylene, ball | Fantina, ball |
| TM84 | Poison Jab | Byron, ball | Fantina, ball |
| TM85 | Skitter Smack | Fantina, ball | Fantina, ball |
| TM93 | Psychic Noise | Fantina, ball | Fantina, ball |
| TM09 | Bullet Seed | Gardenia, ball | Maylene, ball |
| TM10 | Hidden Power | Maylene, reward trainer | Maylene, reward trainer |
| TM16 | Light Screen | Fantina, ball | Maylene, gift |
| TM17 | StompingTantrum | Gardenia, gift | Maylene, ball |
| TM22 | SolarBeam | Maylene, reward trainer | Maylene, reward trainer |
| TM32 | Zen Headbutt | Wake, ball | Maylene, reward trainer |
| TM34 | Shock Wave | Maylene, reward trainer | Maylene, reward trainer |
| TM40 | Aerial Ace | Maylene, reward trainer | Maylene, reward trainer |
| TM55 | Brine | Wake, gift | Maylene, gift |
| TM02 | Dragon Claw | Maylene, gift | Wake, Game Corner prize, once |
| TM05 | Dazzling Gleam | Fantina, ball | Wake, Game Corner prize, once |
| TM30 | Shadow Ball | Byron, ball | Wake, gift |
| TM37 | Signal Beam | Wake, ball | Wake, ball |
| TM41 | Charm | Gardenia, ball | Wake, Game Corner prize, once |
| TM45 | Alluring Voice | Byron, gift | Wake, Game Corner prize, once |
| TM46 | Knock Off | Gardenia, ball | Wake, ball |
| TM59 | Dragon Pulse | Barry, ball | Wake, Game Corner prize, once |
| TM61 | Will-O-Wisp | Fantina, ball | Wake, Game Corner prize, once |
| TM63 | Confuse Ray | Roark, gift | Wake, Game Corner prize, once |
| TM72 | Avalanche | Wake, reward trainer | Wake, reward trainer |
| TM73 | Thunder Wave | Fantina, ball | Wake, Game Corner prize, once |
| TM78 | Captivate | Gardenia, gift | Wake, ball |
| TM81 | X-Scissor | Byron, ball | Wake, gift |
| TM82 | Bounce | Maylene, ball | Wake, Game Corner prize, once |
| TM89 | U-turn | Byron, ball | Wake, ball |
| TM91 | Flash Cannon | Byron, gift | Wake, Game Corner prize, once |
| HM02 | Fly | HQ, ball | Byron, Department Store, once |
| TM07 | Curse | Byron, ball | Byron, Game Corner prize, once |
| TM12 | Taunt | Gardenia, ball | Byron, gift |
| TM23 | Iron Tail | Byron, ball | Byron, Department Store, once |
| TM24 | Thunderbolt | Byron, ball | Byron, Game Corner prize, once |
| TM26 | Earthquake | Byron, ball | Byron, Department Store, once |
| TM29 | Psychic | HQ, ball | Byron, Department Store, once |
| TM35 | Flamethrower | Byron, ball | Byron, Department Store, once |
| TM47 | Steel Wing | Maylene, ball | Byron, gift |
| TM53 | Energy Ball | Galactic, ball | Byron, Department Store, once |
| TM67 | Ice Punch | Candice, gift | Byron, Department Store, once |
| TM71 | Stone Edge | Barry, ball | Byron, Department Store, once |
| TM77 | Foul Play | Byron, ball | Byron, Department Store, once |
| TM80 | Rock Slide | Galactic, ball | Byron, ball |
| HM08 | Rock Climb | Candice, ball | Candice, Department Store, once |
| TM13 | Ice Beam | HQ, ball | Candice, Department Store, once |
| TM20 | Safeguard | Fantina, ball | Candice, ball |
| TM42 | Facade | Maylene, gift | Candice, ball |
| TM49 | Agility | Candice, ball | Candice, Game Corner prize, once |
| TM69 | Rock Polish | Candice, ball | Candice, Game Corner prize, once |
| TM94 | Psybeam | Fantina, ball | Candice, ball |
| TM33 | Reflect | Fantina, ball | HQ, ball |
| TM56 | Hex | Candice, ball | HQ, ball |
| TM70 | Outrage | Barry, ball | HQ, ball |
| HM07 | Waterfall | Volkner, gift | Galactic, reward trainer |
| TM01 | Hydro Pump | Galactic, gift | Galactic, ball |
| TM14 | Blizzard | HQ, ball | Galactic, ball |
| TM21 | Frustration | HQ, ball | Galactic, reward trainer |
| TM25 | Thunder | HQ, ball | Galactic, gift |
| TM27 | Return | HQ, ball | Galactic, reward trainer |
| TM36 | Sludge Bomb | HQ, ball | Galactic, reward trainer |
| TM50 | Overheat | Galactic, ball | Galactic, ball |
| TM58 | Triple Axel | Volkner, gift | Galactic, ball |
| TM60 | Drain Punch | Maylene, gift | Galactic, reward trainer |
| TM64 | Play Rough | Candice, ball | Galactic, reward trainer |
| TM75 | Meteor Beam | Barry, ball | Galactic, ball |
| TM86 | Grass Knot | Gardenia, gift | Galactic, reward trainer |
| TM87 | Swagger | Wake, ball | Galactic, reward trainer |
| TM92 | Trick Room | Wake, gift | Galactic, reward trainer |
| TM08 | Bulk Up | Byron, ball | Volkner, gift |
| TM19 | Giga Drain | Byron, ball | Volkner, gift |
| TM48 | Iron Defense | Roark, gift | Volkner, reward trainer |
| TM74 | Gyro Ball | Maylene, gift | Volkner, gift |
| HM03 | Surf | Byron, gift | Barry, Department Store, once |
| TM04 | Calm Mind | Byron, gift | Barry, Game Corner prize, once |
| TM15 | Hyper Beam | Maylene, ball | Barry, ball |
| TM18 | Scary Face | Gardenia, gift | Barry, ball |
| TM52 | Focus Blast | Volkner, gift | Barry, Department Store, once |
| TM54 | False Swipe | Maylene, ball | Barry, reward trainer |
| TM65 | Shadow Claw | Fantina, gift | Barry, ball |

## The TM list

One row per TM, by the split it first comes in. A number past 92 is new; a number vanilla used for a move that leaves the list now teaches the new move named. Power and accuracy are Oxide's today.

| TM | Move | Type | Class | Power | Accuracy | Tier | Copies | Split | Source |
|---|---|---|---|---|---|---|---|---|---|
| TM06 | Toxic | Poison | Status | - | 100 | strong | 1 | Roark | gift, Oreburgh City Gym |
| TM39 | Rock Tomb | Rock | Physical | 60 | 100 | utility | 2 | Roark | ball, Jubilife City |
| TM51 | Roost | Flying | Status | - | never misses | strong | 1 | Roark | gift, Sandgem Town |
| TM90 | Block | Normal | Status | - | never misses | strong | 1 | Roark | gift, Oreburgh Gate 1F |
| HM05 | Defog | Flying | Status | - | never misses | utility | 2 | Gardenia | gift, Floaroma Town Middle House |
| TM31 | Brick Break | Fighting | Physical | 75 | 100 | utility | 2 | Gardenia | gift, Eterna City |
| TM43 | Secret Power | Normal | Physical | 70 | 100 | utility | 2 | Gardenia | gift, Eterna City Gym |
| TM57 | Charge Beam | Electric | Special | 50 | 100 | weak | 1 | Gardenia | reward trainer |
| TM62 | Silver Wind | Bug | Special | 60 | 100 | weak | 1 | Gardenia | reward trainer |
| TM66 | Payback | Dark | Physical | 60 | 100 | weak | 1 | Gardenia | reward trainer |
| TM68 | Giga Impact | Normal | Physical | 150 | 90 | utility | 2 | Gardenia | gift, Eterna City Condominiums 2F |
| TM76 | Stealth Rock | Rock | Status | - | never misses | utility | 2 | Gardenia | ball, Mt Coronet 1F North Room 1 |
| TM88 | Pluck | Flying | Physical | 60 | 100 | weak | 1 | Gardenia | reward trainer |
| HM04 | Strength | Normal | Physical | 80 | 100 | utility | 2 | Fantina | gift, Hearthome City Gym Leader Room |
| TM03 | Water Pulse | Water | Special | 60 | 100 | weak | 1 | Fantina | reward trainer |
| TM11 | Spite | Ghost | Status | - | 100 | utility | 2 | Fantina | ball, Wayward Cave 1F |
| TM28 | Dig | Ground | Physical | 80 | 100 | utility | 2 | Fantina | ball, Amity Square |
| TM44 | Wild Charge | Electric | Physical | 90 | 100 | utility | 2 | Fantina | ball, Old Chateau Back East Room |
| TM79 | Dark Pulse | Dark | Special | 80 | 100 | utility | 2 | Fantina | ball, Amity Square |
| TM83 | Expanding Force | Psychic | Special | 80 | 100 | utility | 2 | Fantina | ball, Eterna City |
| TM84 | Poison Jab | Poison | Physical | 80 | 100 | utility | 2 | Fantina | ball, Eterna Forest Outside |
| TM85 | Skitter Smack | Bug | Physical | 70 | 100 | utility | 2 | Fantina | ball, Wayward Cave 1F |
| TM93 | Psychic Noise | Psychic | Special | 75 | 100 | utility | 2 | Fantina | ball, Oreburgh Gate B1F |
| TM09 | Bullet Seed | Grass | Physical | 25 | 100 | utility | 2 | Maylene | ball, Route 209 |
| TM10 | Hidden Power | Normal | Special | varies | 100 | weak | 1 | Maylene | reward trainer |
| TM16 | Light Screen | Psychic | Status | - | never misses | utility | 2 | Maylene | gift, Route 210 South |
| TM17 | StompingTantrum | Ground | Physical | 75 | 100 | utility | 2 | Maylene | ball, Route 209 Lost Tower 4F |
| TM22 | SolarBeam | Grass | Special | 120 | 100 | weak | 1 | Maylene | reward trainer |
| TM32 | Zen Headbutt | Psychic | Physical | 80 | 100 | utility | 2 | Maylene | reward trainer |
| TM34 | Shock Wave | Electric | Special | 60 | never misses | weak | 1 | Maylene | reward trainer |
| TM40 | Aerial Ace | Flying | Physical | 60 | never misses | weak | 1 | Maylene | reward trainer |
| TM55 | Brine | Water | Special | 65 | 100 | utility | 2 | Maylene | gift, Route 210 South |
| TM02 | Dragon Claw | Dragon | Physical | 80 | 100 | utility | 2 | Wake | Game Corner prize, once, Veilstone City Prize Exchange |
| TM05 | Dazzling Gleam | Fairy | Special | 80 | 100 | utility | 2 | Wake | Game Corner prize, once, Veilstone City Prize Exchange |
| TM30 | Shadow Ball | Ghost | Special | 80 | 100 | utility | 2 | Wake | gift, Grand Lake Route 213 Northwest House |
| TM37 | Signal Beam | Bug | Special | 75 | 100 | utility | 2 | Wake | ball, Route 212 North |
| TM41 | Charm | Fairy | Status | - | 100 | strong | 1 | Wake | Game Corner prize, once, Veilstone City Prize Exchange |
| TM45 | Alluring Voice | Fairy | Special | 80 | 100 | utility | 2 | Wake | Game Corner prize, once, Veilstone City Prize Exchange |
| TM46 | Knock Off | Dark | Physical | 70 | 100 | utility | 2 | Wake | ball, Pokemon Mansion Office |
| TM59 | Dragon Pulse | Dragon | Special | 85 | 100 | utility | 2 | Wake | Game Corner prize, once, Veilstone City Prize Exchange |
| TM61 | Will-O-Wisp | Fire | Status | - | 85 | strong | 1 | Wake | Game Corner prize, once, Veilstone City Prize Exchange |
| TM63 | Confuse Ray | Ghost | Status | - | 100 | strong | 1 | Wake | Game Corner prize, once, Veilstone City Prize Exchange |
| TM72 | Avalanche | Ice | Physical | 60 | 100 | weak | 1 | Wake | reward trainer |
| TM73 | Thunder Wave | Electric | Status | - | 100 | strong | 1 | Wake | Game Corner prize, once, Veilstone City Prize Exchange |
| TM78 | Captivate | Normal | Status | - | 100 | utility | 2 | Wake | ball, Route 212 South |
| TM81 | X-Scissor | Bug | Physical | 80 | 100 | utility | 2 | Wake | gift, Pastoria City Gym |
| TM82 | Bounce | Flying | Physical | 85 | 100 | utility | 2 | Wake | Game Corner prize, once, Veilstone City Prize Exchange |
| TM89 | U-turn | Bug | Physical | 70 | 100 | utility | 2 | Wake | ball, Route 212 South |
| TM91 | Flash Cannon | Steel | Special | 80 | 100 | utility | 2 | Wake | Game Corner prize, once, Veilstone City Prize Exchange |
| HM02 | Fly | Flying | Physical | 90 | 95 | strong | 1 | Byron | Department Store, once, Veilstone Store 3F |
| TM07 | Curse | Mystery | Status | - | never misses | strong | 1 | Byron | Game Corner prize, once, Veilstone City Prize Exchange |
| TM12 | Taunt | Dark | Status | - | 100 | utility | 2 | Byron | gift, Canalave City Southeast House |
| TM23 | Iron Tail | Steel | Physical | 100 | 75 | strong | 1 | Byron | Department Store, once, Veilstone Store 3F |
| TM24 | Thunderbolt | Electric | Special | 90 | 100 | strong | 1 | Byron | Game Corner prize, once, Veilstone City Prize Exchange |
| TM26 | Earthquake | Ground | Physical | 100 | 100 | strong | 1 | Byron | Department Store, once, Veilstone Store 3F |
| TM29 | Psychic | Psychic | Special | 90 | 100 | strong | 1 | Byron | Department Store, once, Veilstone Store 3F |
| TM35 | Flamethrower | Fire | Special | 90 | 100 | strong | 1 | Byron | Department Store, once, Veilstone Store 3F |
| TM47 | Steel Wing | Steel | Physical | 70 | 90 | utility | 2 | Byron | gift, Canalave City Gym |
| TM53 | Energy Ball | Grass | Special | 90 | 100 | strong | 1 | Byron | Department Store, once, Veilstone Store 3F |
| TM67 | Ice Punch | Ice | Physical | 95 | 100 | strong | 1 | Byron | Department Store, once, Veilstone Store 3F |
| TM71 | Stone Edge | Rock | Physical | 100 | 80 | strong | 1 | Byron | Department Store, once, Veilstone Store 3F |
| TM77 | Foul Play | Dark | Physical | 95 | 100 | strong | 1 | Byron | Department Store, once, Veilstone Store 3F |
| TM80 | Rock Slide | Rock | Physical | 75 | 90 | utility | 2 | Byron | ball, Canalave City |
| HM08 | Rock Climb | Normal | Physical | 90 | 100 | strong | 1 | Candice | Department Store, once, Veilstone Store 3F |
| TM13 | Ice Beam | Ice | Special | 90 | 100 | strong | 1 | Candice | Department Store, once, Veilstone Store 3F |
| TM20 | Safeguard | Normal | Status | - | never misses | utility | 2 | Candice | ball, Oreburgh Gate B1F |
| TM42 | Facade | Normal | Physical | 70 | 100 | utility | 2 | Candice | ball, Lake Acuity |
| TM49 | Agility | Psychic | Status | - | never misses | strong | 1 | Candice | Game Corner prize, once, Veilstone City Prize Exchange |
| TM69 | Rock Polish | Rock | Status | - | never misses | strong | 1 | Candice | Game Corner prize, once, Veilstone City Prize Exchange |
| TM94 | Psybeam | Psychic | Special | 65 | 100 | utility | 2 | Candice | ball, Mt Coronet 1F North Room 1 |
| TM33 | Reflect | Psychic | Status | - | never misses | utility | 2 | HQ | ball, Galactic Hq B2F |
| TM56 | Hex | Ghost | Special | 65 | 100 | utility | 2 | HQ | ball, Galactic Hq 3F |
| TM70 | Outrage | Dragon | Physical | 120 | 100 | utility | 2 | HQ | ball, Galactic Hq 1F |
| HM07 | Waterfall | Water | Physical | 80 | 100 | strong | 1 | Galactic | reward trainer |
| TM01 | Hydro Pump | Water | Special | 110 | 80 | strong | 1 | Galactic | ball, Stark Mountain Room 2 |
| TM14 | Blizzard | Ice | Special | 110 | 70 | strong | 1 | Galactic | ball, Route 226 |
| TM21 | Frustration | Normal | Physical | varies | 100 | strong | 1 | Galactic | reward trainer |
| TM25 | Thunder | Electric | Special | 110 | 70 | strong | 1 | Galactic | gift, Survival Area South House |
| TM27 | Return | Normal | Physical | varies | 100 | strong | 1 | Galactic | reward trainer |
| TM36 | Sludge Bomb | Poison | Special | 90 | 100 | strong | 1 | Galactic | reward trainer |
| TM38 | Fire Blast | Fire | Special | 110 | 85 | strong | 1 | Galactic | ball, Route 228 |
| TM50 | Overheat | Fire | Special | 130 | 90 | strong | 1 | Galactic | ball, Stark Mountain Room 1 |
| TM58 | Triple Axel | Ice | Physical | 20 | 90 | strong | 1 | Galactic | ball, Mt Coronet 2F |
| TM60 | Drain Punch | Fighting | Physical | 75 | 100 | utility | 2 | Galactic | reward trainer |
| TM64 | Play Rough | Fairy | Physical | 90 | 100 | strong | 1 | Galactic | reward trainer |
| TM75 | Meteor Beam | Rock | Special | 120 | 100 | strong | 1 | Galactic | ball, Mt Coronet 2F |
| TM86 | Grass Knot | Grass | Special | varies | 100 | utility | 2 | Galactic | reward trainer |
| TM87 | Swagger | Normal | Status | - | 90 | strong | 1 | Galactic | reward trainer |
| TM92 | Trick Room | Psychic | Status | - | never misses | utility | 2 | Galactic | reward trainer |
| TM08 | Bulk Up | Fighting | Status | - | never misses | strong | 1 | Volkner | gift, Route 222 |
| TM19 | Giga Drain | Grass | Special | 75 | 100 | utility | 2 | Volkner | gift, Sunyshore City |
| TM48 | Iron Defense | Steel | Status | - | never misses | strong | 1 | Volkner | reward trainer |
| TM74 | Gyro Ball | Steel | Physical | varies | 100 | utility | 2 | Volkner | gift, Sunyshore City Gym Room 3 |
| HM03 | Surf | Water | Special | 90 | 100 | strong | 1 | Barry | Department Store, once, Veilstone Store 3F |
| TM04 | Calm Mind | Psychic | Status | - | never misses | strong | 1 | Barry | Game Corner prize, once, Veilstone City Prize Exchange |
| TM15 | Hyper Beam | Normal | Special | 150 | 90 | utility | 2 | Barry | ball, Route 223 |
| TM18 | Scary Face | Normal | Status | - | 100 | utility | 2 | Barry | ball, Victory Road 2F |
| TM52 | Focus Blast | Fighting | Special | 120 | 70 | strong | 1 | Barry | Department Store, once, Veilstone Store 3F |
| TM54 | False Swipe | Normal | Physical | 40 | 100 | utility | 2 | Barry | reward trainer |
| TM65 | Shadow Claw | Ghost | Physical | 70 | 100 | utility | 2 | Barry | ball, Victory Road 1F |

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
| TM07 | Curse | 49 lines gain it that cannot learn it by level-up, 8 of them lines no boss takes today |
| TM11 | Spite | 35 lines gain it that cannot learn it by level-up, 8 of them lines no boss takes today |
| TM17 | StompingTantrum | 59 lines gain it that cannot learn it by level-up, 7 of them lines no boss takes today |
| TM18 | Scary Face | 48 lines gain it that cannot learn it by level-up, 7 of them lines no boss takes today |
| TM32 | Zen Headbutt | 35 lines gain it that cannot learn it by level-up, 6 of them lines no boss takes today |
| TM37 | Signal Beam | 33 lines gain it that cannot learn it by level-up, 7 of them lines no boss takes today |
| TM41 | Charm | 28 lines gain it that cannot learn it by level-up, 6 of them lines no boss takes today |
| TM44 | Wild Charge | 18 lines gain it that cannot learn it by level-up, 6 of them lines no boss takes today |
| TM45 | Alluring Voice | 15 lines gain it that cannot learn it by level-up, 5 of them lines no boss takes today |
| TM46 | Knock Off | 55 lines gain it that cannot learn it by level-up, 6 of them lines no boss takes today |
| TM48 | Iron Defense | 37 lines gain it that cannot learn it by level-up, 5 of them lines no boss takes today |
| TM49 | Agility | 29 lines gain it that cannot learn it by level-up, 4 of them lines no boss takes today |
| TM56 | Hex | 26 lines gain it that cannot learn it by level-up, 6 of them lines no boss takes today |
| TM58 | Triple Axel | 23 lines gain it that cannot learn it by level-up, 5 of them lines no boss takes today |
| TM63 | Confuse Ray | 19 lines gain it that cannot learn it by level-up, 3 of them lines no boss takes today |
| TM64 | Play Rough | 19 lines gain it that cannot learn it by level-up, 4 of them lines no boss takes today |
| TM67 | Ice Punch | 41 lines gain it that cannot learn it by level-up, 3 of them lines no boss takes today |
| TM70 | Outrage | 29 lines gain it that cannot learn it by level-up, 4 of them lines no boss takes today |
| TM75 | Meteor Beam | 27 lines gain it that cannot learn it by level-up, 4 of them lines no boss takes today |
| TM77 | Foul Play | 34 lines gain it that cannot learn it by level-up, 5 of them lines no boss takes today |
| TM82 | Bounce | 24 lines gain it that cannot learn it by level-up, 4 of them lines no boss takes today |
| TM83 | Expanding Force | 18 lines gain it that cannot learn it by level-up, 4 of them lines no boss takes today |
| TM85 | Skitter Smack | 14 lines gain it that cannot learn it by level-up, 4 of them lines no boss takes today |
| TM90 | Block | 16 lines gain it that cannot learn it by level-up, 4 of them lines no boss takes today |
| TM93 | Psychic Noise | 17 lines gain it that cannot learn it by level-up, 4 of them lines no boss takes today |
| TM94 | Psybeam | 17 lines gain it that cannot learn it by level-up, 4 of them lines no boss takes today |

Just below the line: Seed Bomb (31 lines), Hyper Voice (30 lines), Earth Power (34 lines), Acrobatics (27 lines), Air Slash (19 lines), Poltergeist (14 lines), ThunderPunch (44 lines), Rock Blast (31 lines), Aqua Tail (29 lines), Encore (27 lines), Hurricane (27 lines), Gunk Shot (26 lines), Psyshock (25 lines), Venoshock (15 lines), Psychic Fangs (13 lines).

Left out as doing the same job as a TM in the list: Tera Blast (beside Hyper Beam), Take Down (beside Facade), Body Slam (beside Facade), Headbutt (beside Facade), Double-Edge (beside Frustration), Dive (beside Waterfall), Liquidation (beside Waterfall), Icicle Spear (beside Avalanche), Assurance (beside Payback), Retaliate (beside Facade), Low Kick (beside Brick Break), High Horsepower (beside Dig), Muddy Water (beside Surf), Petal Blizzard (beside Bullet Seed), Lunge (beside Skitter Smack), Low Sweep (beside Brick Break), Leaf Storm (beside Energy Ball), Water Pledge (beside Surf), Heat Wave (beside Fire Blast), Sky Attack (beside Aerial Ace).

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
| TM88 Pluck | Gardenia | Fisherman Zachary | Route 205 North | 2.3 |
| TM57 Charge Beam | Gardenia | Picnicker Karina | Route 205 South | 2.3 |
| TM62 Silver Wind | Gardenia | Camper Zackary | Route 205 South | 2.3 |
| TM66 Payback | Gardenia | Hiker Louis | Route 211 West | 2.3 |
| TM03 Water Pulse | Fantina | Hiker Theodore | Route 206 | 2.3 |
| TM34 Shock Wave | Maylene | Collector Edwin | Cafe | 2.3 |
| TM32 Zen Headbutt | Maylene | a new trainer (the main track) | Game Corner | Zen Headbutt, utility; in place of the gift for ten straight bonus rounds (ITEM_TM64), a new optional trainer |
| TM10 Hidden Power | Maylene | Jogger Wyatt | Route 210 South | 2.3 |
| TM22 SolarBeam | Maylene | Ruin Maniac Calvin | Route 215 | 2.3 |
| TM40 Aerial Ace | Maylene | Jogger Scott | Route 215 | 2.3 |
| TM72 Avalanche | Wake | PI Carlos | Route 214 | 2.3 |
| TM21 Frustration | Galactic | Ace Trainer Deanna | Route 225 | 3.2 |
| TM27 Return | Galactic | Ace Trainer Quinn | Route 225 | 3.2 |
| TM86 Grass Knot | Galactic | Bird Keeper Geneva | Route 226 | 2.8 |
| TM87 Swagger | Galactic | Ace Trainer Mikayla | Route 227 | 2.7 |
| TM64 Play Rough | Galactic | Ace Trainer Jose | Route 228 | 3.2 |
| TM60 Drain Punch | Galactic | Pkmn Ranger Deshawn | Route 229 | 2.9 |
| TM92 Trick Room | Galactic | Ace Trainer Dana | Route 229 | 2.7 |
| TM36 Sludge Bomb | Galactic | Swimmer♀ Mallory | Route 230 | 3.1 |
| TM48 Iron Defense | Volkner | Tuber Holly | Route 222 | 2.3 |
| TM54 False Swipe | Barry | Swimmer♀ Crystal | Route 223 | 2.6 |

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
| 4 | Wake | - | TM02 Dragon Claw, TM05 Dazzling Gleam, TM41 Charm, TM45 Alluring Voice, TM59 Dragon Pulse, TM61 Will-O-Wisp, TM63 Confuse Ray, TM73 Thunder Wave, TM82 Bounce, TM91 Flash Cannon |
| 5 | Byron | HM02 Fly, TM23 Iron Tail, TM26 Earthquake, TM29 Psychic, TM35 Flamethrower, TM53 Energy Ball, TM67 Ice Punch, TM71 Stone Edge, TM77 Foul Play | TM07 Curse, TM24 Thunderbolt |
| 6 | Candice | HM08 Rock Climb, TM13 Ice Beam | TM49 Agility, TM69 Rock Polish |
| 7 | HQ | - | - |
| 8 | Barry | HM03 Surf, TM52 Focus Blast | TM04 Calm Mind |

The Game Corner's held items (Silk Scarf, Wide Lens, Zoom Lens, Metronome) move to optional fights, and their prize slots are dropped (Ian, 2026-10-06); the table marks each with reward ITEM_NONE and no copies. The prizes that were neither a TM nor a held item stay as they are.

## Strong TMs held back

A strong TM comes no earlier than the split each flagged line that learns it has a good attack of its type by level-up, Byron's at the latest. These reach flagged stages with none by then:

- Blizzard: Absol, Alolan Ninetales, Arceus, Articuno, Blastoise, Castform, Cranidos, Crawdaunt and 38 more
- Earthquake: Aerodactyl, Arceus, Armaldo, Blastoise, Blaziken, Charizard, Cranidos, Dhelmise and 36 more
- Energy Ball: Abra, Alakazam, Arceus, Armarouge, Castform, Chandelure, Chimecho, Gallade and 14 more
- Fire Blast: Absol, Aerodactyl, Arceus, Castform, Cranidos, Dialga, Flygon, Garchomp and 16 more
- Flamethrower: Absol, Aerodactyl, Arceus, Castform, Cranidos, Dialga, Electivire, Flygon and 18 more
- Fly: Aerodactyl, Arceus, Articuno, Moltres, Togekiss, Volcarona, Zapdos
- Focus Blast: Alakazam, Ampharos, Annihilape, Arceus, Armarouge, Blaziken, Charizard, Cinccino and 30 more
- Foul Play: Abra, Absol, Alakazam, Alolan Ninetales, Ambipom, Arceus, Darkrai, Delphox and 14 more
- Frustration: Abra, Absol, Alakazam, Ambipom, Ampharos, Annihilape, Arceus, Armaldo and 81 more
- Hydro Pump: Arceus, Castform, Dhelmise, Feraligatr, Floatzel, Grapploct, Hisuian Goodra, Kabutops and 7 more
- Ice Beam: Absol, Alolan Ninetales, Arceus, Articuno, Blastoise, Castform, Cranidos, Crawdaunt and 39 more
- Ice Punch: Abra, Alakazam, Ambipom, Ampharos, Annihilape, Blastoise, Electabuzz, Electivire and 34 more
- Iron Tail: Abra, Absol, Alakazam, Ambipom, Annihilape, Arceus, Armaldo, Azumarill and 44 more
- Meteor Beam: Aerodactyl, Ampharos, Arceus, Armaldo, Armarouge, Kabutops, Lunatone, Metagross and 3 more
- Overheat: Annihilape, Arceus, Dialga, Granbull, Moltres, Primeape, Solrock, Toucannon and 1 more
- Play Rough: Absol, Cinccino, Delcatty, Donphan, Liepard, Lopunny, Luxray, Meloetta and 6 more
- Psychic: Abra, Arceus, Armarouge, Chandelure, Darkrai, Electabuzz, Electivire, Florges and 19 more
- Return: Abra, Absol, Alakazam, Ambipom, Ampharos, Annihilape, Arceus, Armaldo and 81 more
- Rock Climb: Ampharos, Annihilape, Arceus, Blastoise, Blaziken, Darkrai, Electabuzz, Electivire and 15 more
- Sludge Bomb: Arceus, Carnivine, Crawdaunt, Darkrai, Gengar, Glimmet, Goodra, Granbull and 8 more
- Stone Edge: Absol, Aerodactyl, Annihilape, Arceus, Armaldo, Blaziken, Breloom, Cranidos and 29 more
- Surf: Arceus, Dhelmise, Feraligatr, Floatzel, Garchomp, Grapploct, Hariyama, Hisuian Goodra and 15 more
- Thunder: Absol, Ambipom, Annihilape, Arceus, Castform, Cinccino, Cranidos, Darkrai and 28 more
- Thunderbolt: Absol, Ambipom, Annihilape, Arceus, Castform, Cinccino, Cranidos, Darkrai and 30 more
- Triple Axel: Alolan Ninetales, Ambipom, Articuno, Cinccino, Empoleon, Frosmoth, Gallade, Gardevoir and 12 more
- Waterfall: Arceus, Feraligatr, Floatzel, Grapploct, Kabutops, Palkia, Sharpedo, Starmie

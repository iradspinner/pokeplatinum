# The comb: Wake's split

The bosses of Wake's split are combed: Barry 4 (three files), Ace Trainer
Krystal and Wake, all passing the checker and the rule audit. The split's
ordinary trainers follow in the later pass and will be added here.

The cap is 44. My simulator reads the bosses against the scorer's box at
Wake, which knows no TMs, so they read harsher than they will once the TM
pass lands. Each is set a step harder than today's file: Wake about 60 won to
today's 67, both read in his gym's rain, and Barry 4 level on wins with far
more faints than today's. Every one of Wake's six is a Water type, as Ian's
new rule asks of a gym.

Pastoria's gym fights in permanent rain (Ian, 2026-10-06: a map's weather is
battle weather for every fight on it), so Wake needs no setter, and his
Swift Swim members (Qwilfish, Ludicolo, Floatzel) move at double speed all
fight. The rain also helps the player: Fire attacks are halved, but the
box's own Water types hit harder and its Swift Swim members are fast too.
Rain cost today's Wake about 26 won points in my simulator (93 clear, 67 in
rain), which is why mine sits near 60 rather than lower. Routes 212 south and
213 have changing weather that can bring rain; their ordinary trainers come
in the later pass and are read without it. No other map in this split has
its own weather.

## Decisions for Ian

Ian answered both on 2026-10-06: Wake loses the Pelipper, since his gym is
already in rain, and Krystal stays at six with her Quick Claw restored, as
luck items are allowed again.

| # | Decision | What the files do today | How it is checked | What Ian decides |
|---|---|---|---|---|
| 1 | Wake fights in his gym's rain (Ian: no Pelipper; the gym is already in permanent rain) | Today's Wake carries two Choice items. Here a Qwilfish leads with Spikes behind a Focus Sash, then Lanturn (Volt Absorb, which walls the box's Electric answers, with Surf, Discharge and Ice Beam), Ludicolo, Gyarados, Sharpedo and Floatzel, the ace with a Life Orb and Bulk Up. The Choice Scarf and Choice Band are gone. Lanturn took Pelipper's slot after a Swift Swim Kingdra read far too hard in the rain (about 20 won). | `leader_wake.json`; the scorer's reading in rain later. | Answered (2026-10-06). |
| 2 | Krystal reads harsh blind (Ian: she stays at six) | Ian's own six (Metang, Glalie, Jumpluff, Rotom, Blaziken, Dragonair) on legal sets at 42 to 43, with fewer boosts on Rotom and Dragonair. Her Quick Claw on Metang is restored (Ian allowed luck items again on 2026-10-06); my simulator does not model it, so her numbers are unchanged. With a planned six she reads 100 won; met blind she loses about one fight in five, as today's team would. | `dummy_795.json`. | Answered (2026-10-06). |

Barry's Ambipom keeps Last Resort, the split's one conditional attack.

## What comes next

Byron's split's bosses, then the rest in order, then the ordinary trainers
from Maylene's split on.

## Overview

| Trainer | Place | Path | Battle | Size | Levels | The idea | Expected |
|---|---|---|---|---|---|---|---|
| Barry 4 | Pastoria City | on the path | single, boss | 6 | 41 to 44 | Barry's skeleton grows a member | about 100 / 2.1 / 0 in my simulator, where today's file reads 100 / 0.05 / 95 |
| Ace Trainer Krystal | Route 214 | optional | single, Ace Trainer | 6 | 42 to 43 | Ian's mixed six on legal sets | about 100 / 0.1 / 93 with a planned six |
| Wake | Pastoria Gym | on the path | single, boss | 6 | 42 to 44 | Swift Swim in his gym's permanent rain | about 60 / 4.9 / 0 in my simulator in the gym's rain, where today's file reads 67 / 4.1 / 0 in rain (93 / 2.3 / 0 clear) |

Expected numbers are won / faints a fight / clean in my simulator, beside
today's file where it was read.

## The bosses

### Barry 4: Pastoria City, on the path, single, boss, cap 44

Barry's skeleton grows a member: the Ambipom Fake Out lead, Staraptor, a new Heracross with Close Combat and Stone Edge, Floatzel, Snorlax, and his starter at the cap (Torterra, Infernape or Empoleon by the player's choice).

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Ambipom | 41 | Silk Scarf | Technician | Jolly | Fake Out, Double Hit, U-turn, Last Resort |
| Staraptor | 42 | Sharp Beak | Intimidate | Adamant | Brave Bird, Close Combat, U-turn, Roost |
| Heracross | 42 | Lum Berry | Guts | Jolly | Close Combat, Night Slash, Stone Edge, Earthquake |
| Floatzel | 42 | Mystic Water | Swift Swim | Adamant | Waterfall, Ice Fang, Crunch, Brick Break |
| Snorlax | 43 | Leftovers | Thick Fat | Careful | Body Slam, Earthquake, Curse, Ice Punch |
| Torterra | 44 | Sitrus Berry | Thick Fat | Adamant | Wood Hammer, Earthquake, Crunch, Stone Edge |

Today's team: Staraptor 41 (White Herb; Aerial Ace, Quick Attack, Close Combat, Tailwind), Starmie 41 (Expert Belt; Surf, Psychic, Signal Beam, Recover), Snorlax 41 (Body Slam, Rest, Sleep Talk, Seismic Toss), Ninetales 41 (Flamethrower, Will-O-Wisp, Energy Ball, Confuse Ray), Torterra 42 (Leftovers; Wood Hammer, Bite, Earthquake, Leech Seed). Expected: about 100 / 2.1 / 0 in my simulator, where today's file reads 100 / 0.05 / 95; read by the scorer later.

### Ace Trainer Krystal: Route 214, optional, single, Ace Trainer, cap 44

Ian's mixed six on legal sets: Metang's Bullet Punch behind his Quick Claw, Glalie's Spikes, Jumpluff's Sleep Powder and U-turn behind a Yache Berry, Rotom's Will-O-Wisp, a Liechi Berry Blaziken with Bulk Up, and Dragonair's Dragon Rush.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Metang | 42 | Quick Claw | Clear Body | Adamant | Bullet Punch, Zen Headbutt, Flash Cannon, Rock Slide |
| Glalie | 42 | none | Solid Rock | default | Ice Beam, Crunch, Ice Shard, Spikes |
| Jumpluff | 42 | Yache Berry | Chlorophyll | Jolly | U-turn, Sleep Powder, Leech Seed, Giga Drain |
| Rotom | 42 | none | Levitate | default | Thunderbolt, Shadow Ball, Will-O-Wisp, Thunder Wave |
| Blaziken | 42 | Liechi Berry | Speed Boost | Adamant | Blaze Kick, Night Slash, Rock Slide, Bulk Up |
| Dragonair | 43 | Leftovers | Shed Skin | default | Dragon Rush, Waterfall, Ice Beam, Thunder Wave |

Today's team: Metang 41 (Quick Claw; Meteor Mash, DynamicPunch, Zen Headbutt, Gravity), Glalie 39 (Icicle Plate; Blizzard, Sing, Earthquake, Weather Ball), Jumpluff 42 (Yache Berry; U-turn, Sleep Powder, Cotton Spore, Encore), Rotom 40 (Life Orb; Thunder, Overheat, Will-O-Wisp, Sunny Day), Blaziken 38 (Liechi Berry; DynamicPunch, Stone Edge, Flare Blitz, Brave Bird), Dragonair 44 (Draco Plate; ExtremeSpeed, Fire Blast, Aqua Tail, Dragon Rush). Expected: about 100 / 0.1 / 93 with a planned six; read blind, about 80 won in my simulator (decision 2).

### Wake: Pastoria Gym, on the path, single, boss, cap 44

Swift Swim in his gym's permanent rain: Qwilfish lays Spikes behind a Focus Sash, Lanturn's Volt Absorb walls the Electric answers, then Ludicolo (Fake Out, Ice Beam), Gyarados (Earthquake, Stone Edge, a Wacan Berry), Sharpedo and a Life Orb Floatzel with Bulk Up and Aqua Jet. Grass and Electric types are the answers, and Lanturn, Gyarados's Earthquake and the Ice moves are aimed at them.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Qwilfish | 42 | Focus Sash | Swift Swim | Jolly | Spikes, Waterfall, Poison Jab, Thunder Wave |
| Lanturn | 42 | Leftovers | Volt Absorb | Modest | Surf, Discharge, Ice Beam, Confuse Ray |
| Ludicolo | 43 | Coba Berry | Swift Swim | Modest | Surf, Giga Drain, Ice Beam, Fake Out |
| Gyarados | 43 | Wacan Berry | Intimidate | Adamant | Waterfall, Earthquake, Ice Fang, Stone Edge |
| Sharpedo | 43 | Leftovers | Speed Boost | Adamant | Crunch, Waterfall, Ice Fang, Earthquake |
| Floatzel | 44 | Life Orb | Swift Swim | Adamant | Waterfall, Crunch, Aqua Jet, Bulk Up |

Today's team: Ludicolo 43 (Leftovers; Surf, Giga Drain, Leech Seed, Ice Beam), Quagsire 43 (Rindo Berry; Earthquake, Ice Punch, Waterfall, Yawn), Poliwrath 43 (Choice Scarf; Brick Break, Waterfall, Ice Punch, Earthquake), Gyarados 43 (Wacan Berry; Waterfall, Earthquake, Ice Fang, Thrash), Sharpedo 43 (Choice Band; Ice Fang, Crunch, Waterfall, Aqua Jet), Floatzel 44 (Life Orb; Ice Fang, Crunch, Waterfall, Aqua Jet). Expected: about 60 / 4.9 / 0 in my simulator in the gym's rain, where today's file reads 67 / 4.1 / 0 in rain (93 / 2.3 / 0 clear); read by the scorer later.


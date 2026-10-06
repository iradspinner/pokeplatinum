# Volkner's split: what each catch knows and learns

Written by `tools/oxide/balance/learncheck.py sheets` for check 6 of the learnset baseline (`docs/oxide/learnset-checks.md`). One table per capture area first offered in Volkner's split, whose cap is 68. Each Pokemon is read at the lowest level it is found at there. "Knows at capture" is the last four moves its list gives by that level; "learns by level-up" is every entry it reaches after capture up to 68, evolving on time, with each later stage's moves under its name; "at the cap" is the stage it can be by then and the next one after. A row marked Rewrite shows the learnset rewrite's lists (the tree's) where it differs from the row marked Oxide, Oxide's lists before the learnset rewrite (`da6b92496c`); a row marked both is the same in each. Relearner-only moves and egg moves are left out.

## Acuity Cavern

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 68 | At the cap |
|---|---|---|---|---|---|---|
| Articuno | static | 50 | Oxide | AncientPower, Agility, Ice Beam, Reflect | Roost 57, Tailwind 64 | Articuno |
| Articuno | static | 50 | Rewrite | AncientPower, Agility, Ice Beam, Reflect | Roost 57, Tailwind 64, Air Slash 66 | Articuno |
| Cresselia | static | 50 | Oxide | Mist, Aurora Beam, Future Sight, Slash | Moonlight 57, Psycho Cut 66 | Cresselia |
| Cresselia | static | 50 | Rewrite | Mist, Aurora Beam, Future Sight, Slash | Moonlight 57, Psycho Cut 66, Confuse Ray 68 | Cresselia |
| Pheromosa | static | 50 | Oxide | Stomp, Agility, Lunge, Bounce | Speed Swap 55, Bug Buzz 60, Quiver Dance 65 | Pheromosa |
| Pheromosa | static | 50 | Rewrite | Stomp, Agility, Lunge, Bounce | Bug Bite 51, Bug Buzz 60, Quiver Dance 65, Throat Chop 66, Hi Jump Kick 67 | Pheromosa |

## Route 222

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 68 | At the cap |
|---|---|---|---|---|---|---|
| Remoraid | old rod | 18 | Oxide | Water Gun, Lock-On, Psybeam, Aurora Beam | BubbleBeam 19, Focus Energy 23; as Octillery: Octazooka 25, Bullet Seed 29, Wring Out 36, Signal Beam 42, Ice Beam 48, Hyper Beam 55 | Octillery (from 25) |
| Remoraid | old rod | 18 | Rewrite | Water Pulse, Lock-On, Psybeam, Aurora Beam | BubbleBeam 19, Focus Energy 23; as Octillery: Octazooka 25, Round 27, Bullet Seed 29, Mud Shot 31, Scald 35, Signal Beam 42, Seed Bomb 44, Ice Beam 48, Skitter Smack 51, Hyper Beam 55, Energy Ball 59, Psychic 61 | Octillery (from 25) |
| Tentacool | old rod | 18 | Oxide | Supersonic, Constrict, Acid, Toxic Spikes | BubbleBeam 19, Wrap 22, Barrier 26, Water Pulse 29; as Tentacruel: Poison Jab 36, Screech 42, Hydro Pump 49, Wring Out 55 | Tentacruel (from 30) |
| Tentacool | old rod | 18 | Rewrite | Supersonic, Acid, Toxic Spikes, Icy Wind | BubbleBeam 19, Barrier 26; as Tentacruel: Poison Jab 36, Surf 40, Screech 42, Psybeam 44, Sludge Bomb 50, Sludge Wave 52, Muddy Water 58, Power Gem 60, Ice Beam 66, Throat Chop 68 | Tentacruel (from 30) |
| Mantyke | old rod | 19 | Oxide | Supersonic, BubbleBeam, Headbutt, Agility | Wing Attack 22, Water Pulse 28; as Mantine: Take Down 31, Confuse Ray 37, Bounce 40, Aqua Ring 46, Hydro Pump 49 | Mantine (from 30) |
| Mantyke | old rod | 19 | Rewrite | Icy Wind, BubbleBeam, Headbutt, Agility | Wing Attack 22, Water Pulse 28; as Mantine: Take Down 31, Scald 34, Confuse Ray 37, Bounce 40, Signal Beam 42, Aqua Ring 46, Surf 50, Air Slash 52, Ice Beam 58, Psychic 60, Swagger 66, Muddy Water 68 | Mantine (from 30) |
| Psyduck | old rod | 19 | Oxide | Tail Whip, Water Gun, Disable, Confusion | Water Pulse 22, Fury Swipes 27, Screech 31; as Golduck: Psych Up 37, Zen Headbutt 44, Amnesia 50, Hydro Pump 56 | Golduck (from 33) |
| Psyduck | old rod | 19 | Rewrite | Water Pulse, Trailblaze, Disable, Confusion | Low Sweep 20, Fury Swipes 27; as Golduck: Muddy Water 34, Psych Up 37, Aurora Beam 42, Zen Headbutt 44, Amnesia 50, Power Gem 52, Ice Beam 58, Psychic 60, Flip Turn 66 | Golduck (from 33) |
| Buizel | old rod | 20 | Oxide | Quick Attack, Water Gun, Pursuit, Swift | Aqua Jet 21; as Floatzel: Crunch 26, Agility 29, Whirlpool 39, Razor Wind 50 | Floatzel (from 26) |
| Buizel | old rod | 20 | Rewrite | Quick Attack, Scary Face, Pursuit, Swift | Aqua Jet 21; as Floatzel: Crunch 26, Flip Turn 28, Icy Wind 30, Waterfall 35, Whirlpool 39, Liquidation 43, Low Sweep 45, Rock Tomb 51, Agility 52, Ice Fang 59, Wave Crash 67 | Floatzel (from 26) |
| Lanturn | good rod | 30 | Oxide | Stockpile, Swallow, Spit Up, BubbleBeam | Signal Beam 35, Discharge 40, Aqua Ring 47, Hydro Pump 52, Charge 57 | Lanturn |
| Lanturn | good rod | 30 | Rewrite | Stockpile, Swallow, Spit Up, BubbleBeam | Signal Beam 35, Scald 37, Discharge 40, Thunderbolt 42, Aqua Ring 47, Muddy Water 52, Charge 57, Flash Cannon 59, Volt Switch 61, Dazzling Gleam 66, Ice Beam 68 | Lanturn |
| Shellos | good rod | 30 | Oxide | Water Pulse, Mud Bomb, Hidden Power, Body Slam | as Gastrodon: Muddy Water 41, Recover 54 | Gastrodon (from 31) |
| Shellos | good rod | 30 | Rewrite | Water Pulse, Mud Bomb, Hidden Power, Body Slam | as Gastrodon: AncientPower 31, Clear Smog 34, Muddy Water 41, Earth Power 43, Bulldoze 45, Ice Beam 50, Recover 54, Sludge Bomb 58, Skitter Smack 60, Block 66, Rock Tomb 68 | Gastrodon (from 31) |
| Lumineon | good rod | 32 | Oxide | Gust, Water Pulse, Captivate, Safeguard | Aqua Ring 35, Whirlpool 42, U-turn 48, Bounce 53, Silver Wind 59 | Lumineon |
| Lumineon | good rod | 32 | Rewrite | Water Pulse, Captivate, Safeguard, Flip Turn | Aqua Ring 35, Aqua Tail 37, Whirlpool 42, U-turn 48, Ice Fang 50, Bounce 53, Air Slash 55, Silver Wind 59, Confuse Ray 61, Acrobatics 66 | Lumineon |
| Tentacool | good rod | 32 | Oxide | BubbleBeam, Wrap, Barrier, Water Pulse | Poison Jab 33; as Tentacruel: Poison Jab 36, Screech 42, Hydro Pump 49, Wring Out 55 | Tentacruel (from 33) |
| Tentacool | good rod | 32 | Rewrite | Toxic Spikes, Icy Wind, BubbleBeam, Barrier | Poison Jab 33; as Tentacruel: Poison Jab 36, Surf 40, Screech 42, Psybeam 44, Sludge Bomb 50, Sludge Wave 52, Muddy Water 58, Power Gem 60, Ice Beam 66, Throat Chop 68 | Tentacruel (from 33) |
| Floatzel | good rod | 34 | Oxide | Swift, Aqua Jet, Crunch, Agility | Whirlpool 39, Razor Wind 50 | Floatzel |
| Floatzel | good rod | 34 | Rewrite | Aqua Jet, Crunch, Flip Turn, Icy Wind | Waterfall 35, Whirlpool 39, Liquidation 43, Low Sweep 45, Rock Tomb 51, Agility 52, Ice Fang 59, Wave Crash 67 | Floatzel |
| Floatzel | surf | 36 | Oxide | Swift, Aqua Jet, Crunch, Agility | Whirlpool 39, Razor Wind 50 | Floatzel |
| Floatzel | surf | 36 | Rewrite | Crunch, Flip Turn, Icy Wind, Waterfall | Whirlpool 39, Liquidation 43, Low Sweep 45, Rock Tomb 51, Agility 52, Ice Fang 59, Wave Crash 67 | Floatzel |
| Mareanie | surf | 36 | Oxide | Recover, Spike Cannon, Pin Missile, Toxic | as Toxapex: Toxic 39, Venom Drench 42, Poison Jab 43, Liquidation 45 | Toxapex (from 38) |
| Mareanie | surf | 36 | Rewrite | Spike Cannon, Pin Missile, Liquidation, Toxic | as Toxapex: Toxic 39, Venom Drench 42, Poison Jab 43, Liquidation 45, Lunge 48, Sludge Bomb 50, Ice Beam 56, Iron Defense 64 | Toxapex (from 38) |
| Vikavolt | wild | 38 | Oxide | Crunch, Bite, Spark, Signal Beam | Discharge 48, Bug Buzz 55, Thunderbolt 65, Zap Cannon 66 | Vikavolt |
| Vikavolt | wild | 38 | Rewrite | Spark, Discharge, Signal Beam, Mud Shot | Flash Cannon 40, Bug Buzz 55, Energy Ball 57, Agility 62, Thunderbolt 65 | Vikavolt |
| Chatot | wild | 39 | Oxide | Taunt, Mimic, Roost, Uproar | FeatherDance 41, Hyper Voice 45 | Chatot |
| Chatot | wild | 39 | Rewrite | Roost, Round, Uproar, U-turn | FeatherDance 41, Hyper Voice 45, Air Slash 48, Steel Wing 50, Acrobatics 56, Parting Shot 58, Heat Wave 64 | Chatot |
| Corvisquire | wild | 39 | Oxide | Steel Wing, Drill Peck, FeatherDance, Revenge | as Corviknight: Defog 42, Iron Head 44, Brave Bird 49, Body Press 55, Roost 65 | Corviknight (from 40) |
| Corvisquire | wild | 39 | Rewrite | Drill Peck, FeatherDance, Low Sweep, Revenge | as Corviknight: U-turn 40, Defog 42, Iron Head 44, Body Slam 46, Brave Bird 49, Iron Defense 53, Body Press 55, Double-Edge 61, Throat Chop 63, Roost 65 | Corviknight (from 40) |
| Galvantula | wild | 39 | Oxide | Struggle Bug, Discharge, Signal Beam, Energy Ball | Sucker Punch 43, Thunderbolt 48, Bug Buzz 51, Thunder 55, Volt Switch 65 | Galvantula |
| Galvantula | wild | 39 | Rewrite | Discharge, Snarl, Signal Beam, Energy Ball | Sucker Punch 43, Giga Drain 45, Thunderbolt 48, Bug Buzz 51, Agility 54, Screech 58, Volt Switch 65, Sludge Bomb 67 | Galvantula |
| Houndoom | wild | 39 | Oxide | Bite, Odor Sleuth, Fire Fang, Faint Attack | Embargo 44, Flamethrower 48, Crunch 54, Nasty Plot 60 | Houndoom |
| Houndoom | wild | 39 | Rewrite | Odor Sleuth, Fire Fang, Fire Pledge, Faint Attack | Mud Shot 42, Embargo 44, Flamethrower 48, Dark Pulse 50, Crunch 54, Shadow Ball 58, Nasty Plot 60, Overheat 66, Sludge Bomb 68 | Houndoom |
| Liepard | wild | 39 | Oxide | Assurance, Hone Claws, Slash, Taunt | Sucker Punch 43, Nasty Plot 44, Night Slash 44, Snatch 47, Play Rough 54 | Liepard |
| Liepard | wild | 39 | Rewrite | Hone Claws, Slash, Throat Chop, Taunt | Sucker Punch 43, Night Slash 44, Snatch 47, Skitter Smack 49, Shadow Ball 51, Play Rough 54, Psycho Cut 59, Seed Bomb 61, U-turn 67 | Liepard |
| Mantine | surf | 39 | Oxide | Wing Attack, Water Pulse, Take Down, Confuse Ray | Bounce 40, Aqua Ring 46, Hydro Pump 49 | Mantine |
| Mantine | surf | 39 | Rewrite | Water Pulse, Take Down, Scald, Confuse Ray | Bounce 40, Signal Beam 42, Aqua Ring 46, Surf 50, Air Slash 52, Ice Beam 58, Psychic 60, Swagger 66, Muddy Water 68 | Mantine |
| Talonflame | wild | 39 | Oxide | Roost, Will-O-Wisp, Natural Gift, Acrobatics | Me First 42, Tailwind 46, Flare Blitz 51, Brave Bird 55 | Talonflame |
| Talonflame | wild | 39 | Rewrite | Roost, Will-O-Wisp, Natural Gift, Acrobatics | Steel Wing 40, Flamethrower 42, Tailwind 46, Flare Blitz 51, Brave Bird 55, U-turn 57, Overheat 59, Double-Edge 64, Agility 66 | Talonflame |
| Tentacruel | surf | 39 | Oxide | Wrap, Barrier, Water Pulse, Poison Jab | Screech 42, Hydro Pump 49, Wring Out 55 | Tentacruel |
| Tentacruel | surf | 39 | Rewrite | BubbleBeam, Barrier, Water Pulse, Poison Jab | Surf 40, Screech 42, Psybeam 44, Sludge Bomb 50, Sludge Wave 52, Muddy Water 58, Power Gem 60, Ice Beam 66, Throat Chop 68 | Tentacruel |
| Togedemaru | wild | 39 | Oxide | Smart Strike, Super Fang, Zing Zap, Iron Head | Electroweb 42, Wild Charge 48, Spiky Shield 55 | Togedemaru |
| Togedemaru | wild | 39 | Rewrite | Spark, Metal Claw, Zing Zap, Iron Head | Electroweb 42, U-turn 45, Wild Charge 48, Poison Jab 54, Zen Headbutt 56, Tickle 62, Assurance 64 | Togedemaru |
| Emolga | wild | 40 | Oxide | Acrobatics, Encore, Light Screen, Volt Switch | Discharge 50, Agility 50 | Emolga |
| Emolga | wild | 40 | Rewrite | Electroweb, Encore, Light Screen, Volt Switch | Agility 49, Discharge 50, Thunderbolt 52, Air Slash 54, Shadow Ball 56, Energy Ball 59, Charm 67 | Emolga |
| Luxray | wild | 40 | Oxide | Bite, Roar, Swagger, Thunder Fang | Crunch 42, Scary Face 49, Discharge 56, Double-Edge 60, Volt Tackle 64 | Luxray |
| Luxray | wild | 40 | Rewrite | Swagger, Trailblaze, Thunder Fang, Throat Chop | Crunch 42, Take Down 44, Scary Face 49, Mean Look 51, Discharge 56, Fire Fang 58, Double-Edge 60, Volt Tackle 64, Ice Fang 66, Thunder Wave 68 | Luxray |
| Mantine | super rod | 40 | Oxide | Water Pulse, Take Down, Confuse Ray, Bounce | Aqua Ring 46, Hydro Pump 49 | Mantine |
| Mantine | super rod | 40 | Rewrite | Take Down, Scald, Confuse Ray, Bounce | Signal Beam 42, Aqua Ring 46, Surf 50, Air Slash 52, Ice Beam 58, Psychic 60, Swagger 66, Muddy Water 68 | Mantine |
| Pawmot | wild | 40 | Oxide | Arm Thrust, Play Rough, Super Fang, Entrainment | Wild Charge 44, Close Combat 49, Mach Punch 55, Double Shock 61 | Pawmot |
| Pawmot | wild | 40 | Rewrite | Play Rough, Super Fang, Body Press, Entrainment | Wild Charge 44, Close Combat 49, Mach Punch 55, Rock Tomb 57, Double Shock 61, Knock Off 63, Low Sweep 65 | Pawmot |
| Toucannon | wild | 40 | Oxide | Fury Attack, Screech, Drill Peck, Bullet Seed | FeatherDance 44, Hyper Voice 50 | Toucannon |
| Toucannon | wild | 40 | Rewrite | Screech, Drill Peck, Facade, Bullet Seed | Throat Chop 42, FeatherDance 44, Hyper Voice 50, Take Down 52, Seed Bomb 58, Brick Break 60, Beak Blast 66, Temper Flare 68 | Toucannon |
| Toxapex | super rod | 40 | Oxide | Recover, Spike Cannon, Pin Missile, Toxic | Venom Drench 42, Poison Jab 43, Liquidation 45 | Toxapex |
| Toxapex | super rod | 40 | Rewrite | Recover, Spike Cannon, Pin Missile, Toxic | Venom Drench 42, Poison Jab 43, Liquidation 45, Lunge 48, Sludge Bomb 50, Ice Beam 56, Iron Defense 64 | Toxapex |
| Araquanid | wild | 41 | Oxide | Headbutt, Soak, Dive, Lunge | Scald 48, Hydro Pump 51, Liquidation 55, Leech Life 61 | Araquanid |
| Araquanid | wild | 41 | Rewrite | Soak, Dive, Skitter Smack, Lunge | Waterfall 43, Scald 48, Poison Jab 51, Liquidation 55, Crunch 59, Leech Life 61, Ice Punch 63, Body Slam 67 | Araquanid |
| Floatzel | wild | 41 | Oxide | Aqua Jet, Crunch, Agility, Whirlpool | Razor Wind 50 | Floatzel |
| Floatzel | wild | 41 | Rewrite | Flip Turn, Icy Wind, Waterfall, Whirlpool | Liquidation 43, Low Sweep 45, Rock Tomb 51, Agility 52, Ice Fang 59, Wave Crash 67 | Floatzel |
| Shellos | wild | 41 | Oxide | Mud Bomb, Hidden Power, Body Slam, Muddy Water | as Gastrodon: Recover 54 | Gastrodon (from 42) |
| Shellos | wild | 41 | Rewrite | Mud Bomb, Hidden Power, Body Slam, Muddy Water | as Gastrodon: Earth Power 43, Bulldoze 45, Ice Beam 50, Recover 54, Sludge Bomb 58, Skitter Smack 60, Block 66, Rock Tomb 68 | Gastrodon (from 42) |
| Gastrodon | surf | 42 | Oxide | Mud Bomb, Hidden Power, Body Slam, Muddy Water | Recover 54 | Gastrodon |
| Gastrodon | surf | 42 | Rewrite | Body Slam, AncientPower, Clear Smog, Muddy Water | Earth Power 43, Bulldoze 45, Ice Beam 50, Recover 54, Sludge Bomb 58, Skitter Smack 60, Block 66, Rock Tomb 68 | Gastrodon |
| Gastrodon | super rod | 43 | Oxide | Mud Bomb, Hidden Power, Body Slam, Muddy Water | Recover 54 | Gastrodon |
| Gastrodon | super rod | 43 | Rewrite | AncientPower, Clear Smog, Muddy Water, Earth Power | Bulldoze 45, Ice Beam 50, Recover 54, Sludge Bomb 58, Skitter Smack 60, Block 66, Rock Tomb 68 | Gastrodon |
| Poliwrath | super rod | 43 | Oxide | Hypnosis, DoubleSlap, Submission, DynamicPunch | Mind Reader 53 | Poliwrath |
| Poliwrath | super rod | 43 | Rewrite | Liquidation, Wake-Up Slap, Throat Chop, Brick Break | Mind Reader 53, Rock Tomb 55, Low Sweep 57, Ice Punch 62, Close Combat 64 | Poliwrath |
| Greninja | super rod | 46 | Oxide | Fling, Scald, Dark Pulse, Extrasensory | Sludge Wave 47, Gunk Shot 51, Hydro Pump 55, Hydro Cannon 65 | Greninja |
| Greninja | super rod | 46 | Rewrite | Shadow Sneak, Scald, Dark Pulse, Extrasensory | Sludge Wave 47, Surf 49, Gunk Shot 51, Ice Beam 56, Muddy Water 58, Hydro Cannon 65, Taunt 67 | Greninja |

## Sunyshore City

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 68 | At the cap |
|---|---|---|---|---|---|---|
| Mantyke | old rod | 18 | Oxide | Bubble, Supersonic, BubbleBeam, Headbutt | Agility 19, Wing Attack 22, Water Pulse 28; as Mantine: Take Down 31, Confuse Ray 37, Bounce 40, Aqua Ring 46, Hydro Pump 49 | Mantine (from 30) |
| Mantyke | old rod | 18 | Rewrite | Bubble, Icy Wind, BubbleBeam, Headbutt | Agility 19, Wing Attack 22, Water Pulse 28; as Mantine: Take Down 31, Scald 34, Confuse Ray 37, Bounce 40, Signal Beam 42, Aqua Ring 46, Surf 50, Air Slash 52, Ice Beam 58, Psychic 60, Swagger 66, Muddy Water 68 | Mantine (from 30) |
| Remoraid | old rod | 18 | Oxide | Water Gun, Lock-On, Psybeam, Aurora Beam | BubbleBeam 19, Focus Energy 23; as Octillery: Octazooka 25, Bullet Seed 29, Wring Out 36, Signal Beam 42, Ice Beam 48, Hyper Beam 55 | Octillery (from 25) |
| Remoraid | old rod | 18 | Rewrite | Water Pulse, Lock-On, Psybeam, Aurora Beam | BubbleBeam 19, Focus Energy 23; as Octillery: Octazooka 25, Round 27, Bullet Seed 29, Mud Shot 31, Scald 35, Signal Beam 42, Seed Bomb 44, Ice Beam 48, Skitter Smack 51, Hyper Beam 55, Energy Ball 59, Psychic 61 | Octillery (from 25) |
| Chinchou | old rod | 19 | Oxide | Thunder Wave, Flail, Water Gun, Confuse Ray | Spark 20, Take Down 23; as Lanturn: Stockpile 27, Swallow 27, Spit Up 27, BubbleBeam 30, Signal Beam 35, Discharge 40, Aqua Ring 47, Hydro Pump 52, Charge 57 | Lanturn (from 27) |
| Chinchou | old rod | 19 | Rewrite | Water Gun, Screech, Confuse Ray, Icy Wind | Take Down 23; as Lanturn: Stockpile 27, Swallow 28, Spit Up 29, BubbleBeam 30, Signal Beam 35, Scald 37, Discharge 40, Thunderbolt 42, Aqua Ring 47, Muddy Water 52, Charge 57, Flash Cannon 59, Volt Switch 61, Dazzling Gleam 66, Ice Beam 68 | Lanturn (from 27) |
| Shellos | old rod | 19 to 20 | Oxide | Harden, Water Pulse, Mud Bomb, Hidden Power | Body Slam 29; as Gastrodon: Muddy Water 41, Recover 54 | Gastrodon (from 30) |
| Shellos | old rod | 19 to 20 | Rewrite | Swagger, Water Pulse, Mud Bomb, Hidden Power | Body Slam 29; as Gastrodon: AncientPower 31, Clear Smog 34, Muddy Water 41, Earth Power 43, Bulldoze 45, Ice Beam 50, Recover 54, Sludge Bomb 58, Skitter Smack 60, Block 66, Rock Tomb 68 | Gastrodon (from 30) |
| Finneon | good rod | 30 | Oxide | Gust, Water Pulse, Captivate, Safeguard | as Lumineon: Aqua Ring 35, Whirlpool 42, U-turn 48, Bounce 53, Silver Wind 59 | Lumineon (from 31) |
| Finneon | good rod | 30 | Rewrite | Icy Wind, Ominous Wind, Captivate, Safeguard | as Lumineon: Flip Turn 31, Aqua Ring 35, Aqua Tail 37, Whirlpool 42, U-turn 48, Ice Fang 50, Bounce 53, Air Slash 55, Silver Wind 59, Confuse Ray 61, Acrobatics 66 | Lumineon (from 31) |
| Lanturn | good rod | 30 | Oxide | Stockpile, Swallow, Spit Up, BubbleBeam | Signal Beam 35, Discharge 40, Aqua Ring 47, Hydro Pump 52, Charge 57 | Lanturn |
| Lanturn | good rod | 30 | Rewrite | Stockpile, Swallow, Spit Up, BubbleBeam | Signal Beam 35, Scald 37, Discharge 40, Thunderbolt 42, Aqua Ring 47, Muddy Water 52, Charge 57, Flash Cannon 59, Volt Switch 61, Dazzling Gleam 66, Ice Beam 68 | Lanturn |
| Remoraid | good rod | 32 | Oxide | BubbleBeam, Focus Energy, Bullet Seed, Water Pulse | as Octillery: Wring Out 36, Signal Beam 42, Ice Beam 48, Hyper Beam 55 | Octillery (from 33) |
| Remoraid | good rod | 32 | Rewrite | Aurora Beam, BubbleBeam, Focus Energy, Bullet Seed | as Octillery: Scald 35, Signal Beam 42, Seed Bomb 44, Ice Beam 48, Skitter Smack 51, Hyper Beam 55, Energy Ball 59, Psychic 61 | Octillery (from 33) |
| Tentacool | good rod | 32 | Oxide | BubbleBeam, Wrap, Barrier, Water Pulse | Poison Jab 33; as Tentacruel: Poison Jab 36, Screech 42, Hydro Pump 49, Wring Out 55 | Tentacruel (from 33) |
| Tentacool | good rod | 32 | Rewrite | Toxic Spikes, Icy Wind, BubbleBeam, Barrier | Poison Jab 33; as Tentacruel: Poison Jab 36, Surf 40, Screech 42, Psybeam 44, Sludge Bomb 50, Sludge Wave 52, Muddy Water 58, Power Gem 60, Ice Beam 66, Throat Chop 68 | Tentacruel (from 33) |
| Frogadier | good rod | 34 | Oxide | Faint Attack, Acrobatics, Low Kick, Waterfall | Fling 35; as Greninja: Scald 37, Dark Pulse 40, Extrasensory 43, Sludge Wave 47, Gunk Shot 51, Hydro Pump 55, Hydro Cannon 65 | Greninja (from 36) |
| Frogadier | good rod | 34 | Rewrite | Faint Attack, Acrobatics, Low Kick, Waterfall | Fling 35; as Greninja: Shadow Sneak 36, Scald 37, Dark Pulse 40, Extrasensory 43, Sludge Wave 47, Surf 49, Gunk Shot 51, Ice Beam 56, Muddy Water 58, Hydro Cannon 65, Taunt 67 | Greninja (from 36) |
| Floatzel | surf | 36 | Oxide | Swift, Aqua Jet, Crunch, Agility | Whirlpool 39, Razor Wind 50 | Floatzel |
| Floatzel | surf | 36 | Rewrite | Crunch, Flip Turn, Icy Wind, Waterfall | Whirlpool 39, Liquidation 43, Low Sweep 45, Rock Tomb 51, Agility 52, Ice Fang 59, Wave Crash 67 | Floatzel |
| Tentacruel | surf | 36 | Oxide | Wrap, Barrier, Water Pulse, Poison Jab | Screech 42, Hydro Pump 49, Wring Out 55 | Tentacruel |
| Tentacruel | surf | 36 | Rewrite | BubbleBeam, Barrier, Water Pulse, Poison Jab | Surf 40, Screech 42, Psybeam 44, Sludge Bomb 50, Sludge Wave 52, Muddy Water 58, Power Gem 60, Ice Beam 66, Throat Chop 68 | Tentacruel |
| Gastrodon | surf | 39 | Oxide | Water Pulse, Mud Bomb, Hidden Power, Body Slam | Muddy Water 41, Recover 54 | Gastrodon |
| Gastrodon | surf | 39 | Rewrite | Hidden Power, Body Slam, AncientPower, Clear Smog | Muddy Water 41, Earth Power 43, Bulldoze 45, Ice Beam 50, Recover 54, Sludge Bomb 58, Skitter Smack 60, Block 66, Rock Tomb 68 | Gastrodon |
| Mantine | surf | 39 | Oxide | Wing Attack, Water Pulse, Take Down, Confuse Ray | Bounce 40, Aqua Ring 46, Hydro Pump 49 | Mantine |
| Mantine | surf | 39 | Rewrite | Water Pulse, Take Down, Scald, Confuse Ray | Bounce 40, Signal Beam 42, Aqua Ring 46, Surf 50, Air Slash 52, Ice Beam 58, Psychic 60, Swagger 66, Muddy Water 68 | Mantine |
| Floatzel | super rod | 40 | Oxide | Aqua Jet, Crunch, Agility, Whirlpool | Razor Wind 50 | Floatzel |
| Floatzel | super rod | 40 | Rewrite | Flip Turn, Icy Wind, Waterfall, Whirlpool | Liquidation 43, Low Sweep 45, Rock Tomb 51, Agility 52, Ice Fang 59, Wave Crash 67 | Floatzel |
| Mantine | super rod | 40 | Oxide | Water Pulse, Take Down, Confuse Ray, Bounce | Aqua Ring 46, Hydro Pump 49 | Mantine |
| Mantine | super rod | 40 | Rewrite | Take Down, Scald, Confuse Ray, Bounce | Signal Beam 42, Aqua Ring 46, Surf 50, Air Slash 52, Ice Beam 58, Psychic 60, Swagger 66, Muddy Water 68 | Mantine |
| Frogadier | surf | 42 | Oxide | Low Kick, Waterfall, Fling, Dark Pulse | as Greninja: Extrasensory 43, Sludge Wave 47, Gunk Shot 51, Hydro Pump 55, Hydro Cannon 65 | Greninja (from 43) |
| Frogadier | surf | 42 | Rewrite | Low Kick, Waterfall, Fling, Dark Pulse | as Greninja: Extrasensory 43, Sludge Wave 47, Surf 49, Gunk Shot 51, Ice Beam 56, Muddy Water 58, Hydro Cannon 65, Taunt 67 | Greninja (from 43) |
| Gastrodon | super rod | 43 | Oxide | Mud Bomb, Hidden Power, Body Slam, Muddy Water | Recover 54 | Gastrodon |
| Gastrodon | super rod | 43 | Rewrite | AncientPower, Clear Smog, Muddy Water, Earth Power | Bulldoze 45, Ice Beam 50, Recover 54, Sludge Bomb 58, Skitter Smack 60, Block 66, Rock Tomb 68 | Gastrodon |
| Wailord | super rod | 43 | Oxide | Rest, Brine, Water Spout, Amnesia | Dive 46, Bounce 54, Hydro Pump 62 | Wailord |
| Wailord | super rod | 43 | Rewrite | Rest, Brine, Water Spout, Amnesia | Dive 46, Rock Tomb 48, Iron Head 50, Bounce 54, Zen Headbutt 56, Body Press 58, Surf 62, Earthquake 64 | Wailord |
| Toxapex | super rod | 46 | Oxide | Toxic, Venom Drench, Poison Jab, Liquidation | nothing | Toxapex |
| Toxapex | super rod | 46 | Rewrite | Toxic, Venom Drench, Poison Jab, Liquidation | Lunge 48, Sludge Bomb 50, Ice Beam 56, Iron Defense 64 | Toxapex |

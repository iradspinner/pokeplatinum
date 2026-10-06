# Volkner's split: what each catch knows and learns

Written by `tools/oxide/balance/learncheck.py sheets` for check 6 of the learnset baseline (`docs/oxide/learnset-checks.md`). One table per capture area first offered in Volkner's split, whose cap is 68. Each Pokemon is read at the lowest level it is found at there. "Knows at capture" is the last four moves its list gives by that level; "learns by level-up" is every entry it reaches after capture up to 68, evolving on time, with each later stage's moves under its name; "at the cap" is the stage it can be by then and the next one after. A row marked Rewrite shows the learnset rewrite's lists (the tree's) where it differs from the row marked Oxide, Oxide's lists before the learnset rewrite (`da6b92496c`); a row marked both is the same in each. Relearner-only moves and egg moves are left out.

## Acuity Cavern

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 68 | At the cap |
|---|---|---|---|---|---|---|
| Articuno | static | 50 | Oxide | AncientPower, Agility, Ice Beam, Reflect | Roost 57, Tailwind 64 | Articuno |
| Articuno | static | 50 | Rewrite | AncientPower, Agility, Ice Beam, Reflect | Roost 57, Tailwind 64, Air Slash 68 | Articuno |
| Cresselia | static | 50 | Oxide | Mist, Aurora Beam, Future Sight, Slash | Moonlight 57, Psycho Cut 66 | Cresselia |
| Cresselia | static | 50 | Rewrite | Mist, Aurora Beam, Future Sight, Slash | Moonlight 57, Psycho Cut 66, Confuse Ray 68 | Cresselia |
| Pheromosa | static | 50 | Oxide | Stomp, Agility, Lunge, Bounce | Speed Swap 55, Bug Buzz 60, Quiver Dance 65 | Pheromosa |
| Pheromosa | static | 50 | Rewrite | Stomp, Agility, Lunge, Bounce | Bug Buzz 60, Quiver Dance 65, Throat Chop 66, Close Combat 67 | Pheromosa |

## Route 222

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 68 | At the cap |
|---|---|---|---|---|---|---|
| Remoraid | old rod | 18 | Oxide | Water Gun, Lock-On, Psybeam, Aurora Beam | BubbleBeam 19, Focus Energy 23; as Octillery: Octazooka 25, Bullet Seed 29, Wring Out 36, Signal Beam 42, Ice Beam 48, Hyper Beam 55 | Octillery (from 25) |
| Remoraid | old rod | 18 | Rewrite | Water Pulse, Psybeam, Screech, Aurora Beam | BubbleBeam 19, Focus Energy 23; as Octillery: Octazooka 25, Mud Shot 27, Bullet Seed 29, Round 33, Charge Beam 35, Scald 37, Skitter Smack 40, Signal Beam 42, Ice Beam 48, Psychic 54, Hyper Beam 55, Swagger 61 | Octillery (from 25) |
| Tentacool | old rod | 18 | Oxide | Supersonic, Constrict, Acid, Toxic Spikes | BubbleBeam 19, Wrap 22, Barrier 26, Water Pulse 29; as Tentacruel: Poison Jab 36, Screech 42, Hydro Pump 49, Wring Out 55 | Tentacruel (from 30) |
| Tentacool | old rod | 18 | Rewrite | Pounce, Acid, Toxic Spikes, Water Pulse | BubbleBeam 19, Barrier 26; as Tentacruel: Poison Jab 33, Aurora Beam 34, Sludge Bomb 39, Screech 42, Psybeam 44, Surf 49, Muddy Water 53, Throat Chop 54, Power Gem 56, Flip Turn 58, Ice Beam 60, Toxic 62, Skitter Smack 65, Confuse Ray 68 | Tentacruel (from 30) |
| Mantyke | old rod | 19 | Oxide | Supersonic, BubbleBeam, Headbutt, Agility | Wing Attack 22, Water Pulse 28; as Mantine: Take Down 31, Confuse Ray 37, Bounce 40, Aqua Ring 46, Hydro Pump 49 | Mantine (from 30) |
| Mantyke | old rod | 19 | Rewrite | Bubble, BubbleBeam, Headbutt, Agility | Wing Attack 22, Icy Wind 25, Water Pulse 28; as Mantine: Take Down 31, Signal Beam 34, Round 35, Confuse Ray 37, Bounce 40, Psybeam 41, Surf 43, Aqua Ring 46, Scald 49, Air Slash 54, Roost 56, Muddy Water 58, Ice Beam 60, Swagger 65 | Mantine (from 30) |
| Psyduck | old rod | 19 | Oxide | Tail Whip, Water Gun, Disable, Confusion | Water Pulse 22, Fury Swipes 27, Screech 31; as Golduck: Psych Up 37, Zen Headbutt 44, Amnesia 50, Hydro Pump 56 | Golduck (from 33) |
| Psyduck | old rod | 19 | Rewrite | Water Gun, Water Pulse, Disable, Confusion | Low Sweep 22, Fury Swipes 27; as Golduck: Surf 34, Psych Up 37, Aurora Beam 40, Zen Headbutt 44, Power Gem 47, Amnesia 50, Ice Beam 54, Muddy Water 56, Flip Turn 58, Psychic 60, Confuse Ray 65 | Golduck (from 33) |
| Buizel | old rod | 20 | Oxide | Quick Attack, Water Gun, Pursuit, Swift | Aqua Jet 21; as Floatzel: Crunch 26, Agility 29, Whirlpool 39, Razor Wind 50 | Floatzel (from 26) |
| Buizel | old rod | 20 | Rewrite | BubbleBeam, Pursuit, Scary Face, Swift | Aqua Jet 21; as Floatzel: Crunch 26, Icy Wind 29, Flip Turn 33, Waterfall 36, Whirlpool 39, Liquidation 41, Low Sweep 44, Agility 51, Rock Tomb 53, Ice Fang 56, Wave Crash 62, Ice Punch 65 | Floatzel (from 26) |
| Lanturn | good rod | 30 | Oxide | Stockpile, Swallow, Spit Up, BubbleBeam | Signal Beam 35, Discharge 40, Aqua Ring 47, Hydro Pump 52, Charge 57 | Lanturn |
| Lanturn | good rod | 30 | Rewrite | Stockpile, Swallow, Spit Up, BubbleBeam | Signal Beam 31, Scald 33, Surf 34, Thunderbolt 37, Discharge 40, Flash Cannon 43, Aqua Ring 47, Muddy Water 52, Volt Switch 54, Dazzling Gleam 55, Charge 57, Ice Beam 60, Swagger 65 | Lanturn |
| Shellos | good rod | 30 | Oxide | Water Pulse, Mud Bomb, Hidden Power, Body Slam | as Gastrodon: Muddy Water 41, Recover 54 | Gastrodon (from 31) |
| Shellos | good rod | 30 | Rewrite | Mud Bomb, Hidden Power, Swagger, Body Slam | as Gastrodon: AncientPower 33, Earth Power 35, Clear Smog 37, Muddy Water 41, Bulldoze 44, Sludge Bomb 46, Ice Beam 49, Recover 54, Skitter Smack 56, Rock Tomb 60, Block 65 | Gastrodon (from 31) |
| Lumineon | good rod | 32 | Oxide | Gust, Water Pulse, Captivate, Safeguard | Aqua Ring 35, Whirlpool 42, U-turn 48, Bounce 53, Silver Wind 59 | Lumineon |
| Lumineon | good rod | 32 | Rewrite | Water Pulse, Captivate, Safeguard, Flip Turn | Aqua Ring 33, Icy Wind 34, Aqua Tail 38, Signal Beam 40, Whirlpool 42, Ice Fang 45, U-turn 48, Bounce 53, Air Slash 54, Crunch 56, Confuse Ray 57, Silver Wind 59, Charm 65 | Lumineon |
| Tentacool | good rod | 32 | Oxide | BubbleBeam, Wrap, Barrier, Water Pulse | Poison Jab 33; as Tentacruel: Poison Jab 36, Screech 42, Hydro Pump 49, Wring Out 55 | Tentacruel (from 33) |
| Tentacool | good rod | 32 | Rewrite | Toxic Spikes, Water Pulse, BubbleBeam, Barrier | Poison Jab 33; as Tentacruel: Poison Jab 33, Aurora Beam 34, Sludge Bomb 39, Screech 42, Psybeam 44, Surf 49, Muddy Water 53, Throat Chop 54, Power Gem 56, Flip Turn 58, Ice Beam 60, Toxic 62, Skitter Smack 65, Confuse Ray 68 | Tentacruel (from 33) |
| Floatzel | good rod | 34 | Oxide | Swift, Aqua Jet, Crunch, Agility | Whirlpool 39, Razor Wind 50 | Floatzel |
| Floatzel | good rod | 34 | Rewrite | Aqua Jet, Crunch, Icy Wind, Flip Turn | Waterfall 36, Whirlpool 39, Liquidation 41, Low Sweep 44, Agility 51, Rock Tomb 53, Ice Fang 56, Wave Crash 62, Ice Punch 65 | Floatzel |
| Floatzel | surf | 36 | Oxide | Swift, Aqua Jet, Crunch, Agility | Whirlpool 39, Razor Wind 50 | Floatzel |
| Floatzel | surf | 36 | Rewrite | Crunch, Icy Wind, Flip Turn, Waterfall | Whirlpool 39, Liquidation 41, Low Sweep 44, Agility 51, Rock Tomb 53, Ice Fang 56, Wave Crash 62, Ice Punch 65 | Floatzel |
| Mareanie | surf | 36 | Oxide | Recover, Spike Cannon, Pin Missile, Toxic | as Toxapex: Toxic 39, Venom Drench 42, Poison Jab 43, Liquidation 45 | Toxapex (from 38) |
| Mareanie | surf | 36 | Rewrite | Recover, Spike Cannon, Pin Missile, Toxic | Muddy Water 38; as Toxapex: Venom Drench 42, Poison Jab 43, Liquidation 45, Lunge 53, Ice Beam 54, Sludge Bomb 56, Iron Defense 61 | Toxapex (from 38) |
| Vikavolt | wild | 38 | Oxide | Crunch, Bite, Spark, Signal Beam | Discharge 48, Bug Buzz 55, Thunderbolt 65, Zap Cannon 66 | Vikavolt |
| Vikavolt | wild | 38 | Rewrite | Crunch, Bite, Spark, Signal Beam | Pollen Puff 40, Discharge 48, Energy Ball 54, Bug Buzz 55, Air Slash 57, Flash Cannon 60, Agility 62, Thunderbolt 65, Iron Defense 66, Volt Switch 68 | Vikavolt |
| Chatot | wild | 39 | Oxide | Taunt, Mimic, Roost, Uproar | FeatherDance 41, Hyper Voice 45 | Chatot |
| Chatot | wild | 39 | Rewrite | Roost, Round, Uproar, U-turn | FeatherDance 41, Air Slash 43, Hyper Voice 45, Steel Wing 53, Parting Shot 54, Brave Bird 56, Heat Wave 61 | Chatot |
| Corvisquire | wild | 39 | Oxide | Steel Wing, Drill Peck, FeatherDance, Revenge | as Corviknight: Defog 42, Iron Head 44, Brave Bird 49, Body Press 55, Roost 65 | Corviknight (from 40) |
| Corvisquire | wild | 39 | Rewrite | Low Sweep, FeatherDance, U-turn, Revenge | as Corviknight: Defog 42, Iron Head 44, Brave Bird 49, Body Slam 52, Throat Chop 54, Body Press 55, Iron Defense 57, Swagger 60, Double-Edge 62, Roost 65, Screech 66, Scary Face 68 | Corviknight (from 40) |
| Galvantula | wild | 39 | Oxide | Struggle Bug, Discharge, Signal Beam, Energy Ball | Sucker Punch 43, Thunderbolt 48, Bug Buzz 51, Thunder 55, Volt Switch 65 | Galvantula |
| Galvantula | wild | 39 | Rewrite | Discharge, Snarl, Signal Beam, Energy Ball | Swift 40, Giga Drain 41, Sucker Punch 43, Thunderbolt 48, Bug Buzz 51, Screech 54, Agility 56, Sticky Web 60, Sludge Bomb 62, Volt Switch 65 | Galvantula |
| Houndoom | wild | 39 | Oxide | Bite, Odor Sleuth, Fire Fang, Faint Attack | Embargo 44, Flamethrower 48, Crunch 54, Nasty Plot 60 | Houndoom |
| Houndoom | wild | 39 | Rewrite | Odor Sleuth, Fire Fang, Fire Pledge, Faint Attack | Mud Shot 41, Embargo 44, Flamethrower 48, Dark Pulse 51, Crunch 54, Shadow Ball 56, BurningJealousy 58, Nasty Plot 60, Sludge Bomb 62, Overheat 65, Toxic 66, Hyper Voice 68 | Houndoom |
| Liepard | wild | 39 | Oxide | Assurance, Hone Claws, Slash, Taunt | Sucker Punch 43, Nasty Plot 44, Night Slash 44, Snatch 47, Play Rough 54 | Liepard |
| Liepard | wild | 39 | Rewrite | Nasty Plot, Slash, Throat Chop, Taunt | Sucker Punch 43, Night Slash 44, Snatch 47, Skitter Smack 50, Play Rough 54, BurningJealousy 56, Seed Bomb 58, Shadow Ball 60, U-turn 65 | Liepard |
| Mantine | surf | 39 | Oxide | Wing Attack, Water Pulse, Take Down, Confuse Ray | Bounce 40, Aqua Ring 46, Hydro Pump 49 | Mantine |
| Mantine | surf | 39 | Rewrite | Take Down, Signal Beam, Round, Confuse Ray | Bounce 40, Psybeam 41, Surf 43, Aqua Ring 46, Scald 49, Air Slash 54, Roost 56, Muddy Water 58, Ice Beam 60, Swagger 65 | Mantine |
| Talonflame | wild | 39 | Oxide | Roost, Will-O-Wisp, Natural Gift, Acrobatics | Me First 42, Tailwind 46, Flare Blitz 51, Brave Bird 55 | Talonflame |
| Talonflame | wild | 39 | Rewrite | Roost, Will-O-Wisp, Natural Gift, Acrobatics | Steel Wing 40, Flamethrower 42, Tailwind 46, Upper Hand 48, Flare Blitz 51, Overheat 54, Brave Bird 55, Agility 57, U-turn 60, Bulk Up 65 | Talonflame |
| Tentacruel | surf | 39 | Oxide | Wrap, Barrier, Water Pulse, Poison Jab | Screech 42, Hydro Pump 49, Wring Out 55 | Tentacruel |
| Tentacruel | surf | 39 | Rewrite | Water Pulse, Poison Jab, Aurora Beam, Sludge Bomb | Screech 42, Psybeam 44, Surf 49, Muddy Water 53, Throat Chop 54, Power Gem 56, Flip Turn 58, Ice Beam 60, Toxic 62, Skitter Smack 65, Confuse Ray 68 | Tentacruel |
| Togedemaru | wild | 39 | Oxide | Smart Strike, Super Fang, Zing Zap, Iron Head | Electroweb 42, Wild Charge 48, Spiky Shield 55 | Togedemaru |
| Togedemaru | wild | 39 | Rewrite | Smart Strike, Super Fang, Zing Zap, Iron Head | Electroweb 42, Wild Charge 48, U-turn 53, Zen Headbutt 54, Poison Jab 56, Tickle 58, Assurance 60, ThunderPunch 62, Wish 65 | Togedemaru |
| Emolga | wild | 40 | Oxide | Acrobatics, Encore, Light Screen, Volt Switch | Discharge 50, Agility 50 | Emolga |
| Emolga | wild | 40 | Rewrite | Electroweb, Encore, Light Screen, Volt Switch | Thunderbolt 44, Agility 49, Discharge 50, Energy Ball 54, Air Slash 56, Shadow Ball 60, Charm 65 | Emolga |
| Luxray | wild | 40 | Oxide | Bite, Roar, Swagger, Thunder Fang | Crunch 42, Scary Face 49, Discharge 56, Double-Edge 60, Volt Tackle 64 | Luxray |
| Luxray | wild | 40 | Rewrite | Thunder Fang, Throat Chop, Metal Claw, Trailblaze | Crunch 42, Mean Look 45, Scary Face 49, Headbutt 52, Fire Fang 54, Discharge 56, Ice Fang 58, Double-Edge 60, Thunder Wave 62, Volt Tackle 64 | Luxray |
| Mantine | super rod | 40 | Oxide | Water Pulse, Take Down, Confuse Ray, Bounce | Aqua Ring 46, Hydro Pump 49 | Mantine |
| Mantine | super rod | 40 | Rewrite | Signal Beam, Round, Confuse Ray, Bounce | Psybeam 41, Surf 43, Aqua Ring 46, Scald 49, Air Slash 54, Roost 56, Muddy Water 58, Ice Beam 60, Swagger 65 | Mantine |
| Pawmot | wild | 40 | Oxide | Arm Thrust, Play Rough, Super Fang, Entrainment | Wild Charge 44, Close Combat 49, Mach Punch 55, Double Shock 61 | Pawmot |
| Pawmot | wild | 40 | Rewrite | Play Rough, Super Fang, Body Press, Entrainment | Wild Charge 44, Close Combat 49, Rock Tomb 54, Mach Punch 55, ThunderPunch 56, Agility 57, Low Sweep 58, Double Shock 61, Fire Punch 65, Thunder Wave 66, Throat Chop 68 | Pawmot |
| Toucannon | wild | 40 | Oxide | Fury Attack, Screech, Drill Peck, Bullet Seed | FeatherDance 44, Hyper Voice 50 | Toucannon |
| Toucannon | wild | 40 | Rewrite | Drill Peck, Smack Down, Facade, Bullet Seed | Throat Chop 42, FeatherDance 44, Take Down 47, Hyper Voice 50, Brick Break 54, Temper Flare 56, Rock Climb 60, Brave Bird 65, Beak Blast 68 | Toucannon |
| Toxapex | super rod | 40 | Oxide | Recover, Spike Cannon, Pin Missile, Toxic | Venom Drench 42, Poison Jab 43, Liquidation 45 | Toxapex |
| Toxapex | super rod | 40 | Rewrite | Recover, Spike Cannon, Toxic, Pin Missile | Venom Drench 42, Poison Jab 43, Liquidation 45, Lunge 53, Ice Beam 54, Sludge Bomb 56, Iron Defense 61 | Toxapex |
| Araquanid | wild | 41 | Oxide | Headbutt, Soak, Dive, Lunge | Scald 48, Hydro Pump 51, Liquidation 55, Leech Life 61 | Araquanid |
| Araquanid | wild | 41 | Rewrite | Skitter Smack, Dive, Waterfall, Lunge | Poison Jab 44, Scald 48, Crunch 51, Body Slam 54, Liquidation 55, Ice Punch 58, Leech Life 61 | Araquanid |
| Floatzel | wild | 41 | Oxide | Aqua Jet, Crunch, Agility, Whirlpool | Razor Wind 50 | Floatzel |
| Floatzel | wild | 41 | Rewrite | Flip Turn, Waterfall, Whirlpool, Liquidation | Low Sweep 44, Agility 51, Rock Tomb 53, Ice Fang 56, Wave Crash 62, Ice Punch 65 | Floatzel |
| Shellos | wild | 41 | Oxide | Mud Bomb, Hidden Power, Body Slam, Muddy Water | as Gastrodon: Recover 54 | Gastrodon (from 42) |
| Shellos | wild | 41 | Rewrite | Hidden Power, Swagger, Body Slam, Muddy Water | as Gastrodon: Bulldoze 44, Sludge Bomb 46, Ice Beam 49, Recover 54, Skitter Smack 56, Rock Tomb 60, Block 65 | Gastrodon (from 42) |
| Gastrodon | surf | 42 | Oxide | Mud Bomb, Hidden Power, Body Slam, Muddy Water | Recover 54 | Gastrodon |
| Gastrodon | surf | 42 | Rewrite | AncientPower, Earth Power, Clear Smog, Muddy Water | Bulldoze 44, Sludge Bomb 46, Ice Beam 49, Recover 54, Skitter Smack 56, Rock Tomb 60, Block 65 | Gastrodon |
| Gastrodon | super rod | 43 | Oxide | Mud Bomb, Hidden Power, Body Slam, Muddy Water | Recover 54 | Gastrodon |
| Gastrodon | super rod | 43 | Rewrite | AncientPower, Earth Power, Clear Smog, Muddy Water | Bulldoze 44, Sludge Bomb 46, Ice Beam 49, Recover 54, Skitter Smack 56, Rock Tomb 60, Block 65 | Gastrodon |
| Poliwrath | super rod | 43 | Oxide | Hypnosis, DoubleSlap, Submission, DynamicPunch | Mind Reader 53 | Poliwrath |
| Poliwrath | super rod | 43 | Rewrite | Hypnosis, DoubleSlap, Liquidation, Brick Break | Mind Reader 53, Rock Tomb 54, Throat Chop 56, Close Combat 58, Ice Punch 60, Upper Hand 62, Drain Punch 65, Belly Drum 66, Earthquake 68 | Poliwrath |
| Greninja | super rod | 46 | Oxide | Fling, Scald, Dark Pulse, Extrasensory | Sludge Wave 47, Gunk Shot 51, Hydro Pump 55, Hydro Cannon 65 | Greninja |
| Greninja | super rod | 46 | Rewrite | Shadow Sneak, Scald, Dark Pulse, Extrasensory | Sludge Wave 47, Gunk Shot 51, Ice Beam 54, Surf 56, Throat Chop 58, Muddy Water 60, Taunt 62, Hydro Cannon 65 | Greninja |

## Sunyshore City

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 68 | At the cap |
|---|---|---|---|---|---|---|
| Mantyke | old rod | 18 | Oxide | Bubble, Supersonic, BubbleBeam, Headbutt | Agility 19, Wing Attack 22, Water Pulse 28; as Mantine: Take Down 31, Confuse Ray 37, Bounce 40, Aqua Ring 46, Hydro Pump 49 | Mantine (from 30) |
| Mantyke | old rod | 18 | Rewrite | Tackle, Bubble, BubbleBeam, Headbutt | Agility 19, Wing Attack 22, Icy Wind 25, Water Pulse 28; as Mantine: Take Down 31, Signal Beam 34, Round 35, Confuse Ray 37, Bounce 40, Psybeam 41, Surf 43, Aqua Ring 46, Scald 49, Air Slash 54, Roost 56, Muddy Water 58, Ice Beam 60, Swagger 65 | Mantine (from 30) |
| Remoraid | old rod | 18 | Oxide | Water Gun, Lock-On, Psybeam, Aurora Beam | BubbleBeam 19, Focus Energy 23; as Octillery: Octazooka 25, Bullet Seed 29, Wring Out 36, Signal Beam 42, Ice Beam 48, Hyper Beam 55 | Octillery (from 25) |
| Remoraid | old rod | 18 | Rewrite | Water Pulse, Psybeam, Screech, Aurora Beam | BubbleBeam 19, Focus Energy 23; as Octillery: Octazooka 25, Mud Shot 27, Bullet Seed 29, Round 33, Charge Beam 35, Scald 37, Skitter Smack 40, Signal Beam 42, Ice Beam 48, Psychic 54, Hyper Beam 55, Swagger 61 | Octillery (from 25) |
| Chinchou | old rod | 19 | Oxide | Thunder Wave, Flail, Water Gun, Confuse Ray | Spark 20, Take Down 23; as Lanturn: Stockpile 27, Swallow 27, Spit Up 27, BubbleBeam 30, Signal Beam 35, Discharge 40, Aqua Ring 47, Hydro Pump 52, Charge 57 | Lanturn (from 27) |
| Chinchou | old rod | 19 | Rewrite | Flail, Water Gun, Screech, Confuse Ray | Spark 20, Take Down 23, Icy Wind 26; as Lanturn: Stockpile 27, Swallow 28, Spit Up 29, BubbleBeam 30, Signal Beam 31, Scald 33, Surf 34, Thunderbolt 37, Discharge 40, Flash Cannon 43, Aqua Ring 47, Muddy Water 52, Volt Switch 54, Dazzling Gleam 55, Charge 57, Ice Beam 60, Swagger 65 | Lanturn (from 27) |
| Shellos | old rod | 19 to 20 | Oxide | Harden, Water Pulse, Mud Bomb, Hidden Power | Body Slam 29; as Gastrodon: Muddy Water 41, Recover 54 | Gastrodon (from 30) |
| Shellos | old rod | 19 to 20 | Rewrite | Harden, Water Pulse, Mud Bomb, Hidden Power | Swagger 22, Body Slam 29; as Gastrodon: AncientPower 33, Earth Power 35, Clear Smog 37, Muddy Water 41, Bulldoze 44, Sludge Bomb 46, Ice Beam 49, Recover 54, Skitter Smack 56, Rock Tomb 60, Block 65 | Gastrodon (from 30) |
| Finneon | good rod | 30 | Oxide | Gust, Water Pulse, Captivate, Safeguard | as Lumineon: Aqua Ring 35, Whirlpool 42, U-turn 48, Bounce 53, Silver Wind 59 | Lumineon (from 31) |
| Finneon | good rod | 30 | Rewrite | Pursuit, Gust, Captivate, Safeguard | as Lumineon: Flip Turn 31, Aqua Ring 33, Icy Wind 34, Aqua Tail 38, Signal Beam 40, Whirlpool 42, Ice Fang 45, U-turn 48, Bounce 53, Air Slash 54, Crunch 56, Confuse Ray 57, Silver Wind 59, Charm 65 | Lumineon (from 31) |
| Lanturn | good rod | 30 | Oxide | Stockpile, Swallow, Spit Up, BubbleBeam | Signal Beam 35, Discharge 40, Aqua Ring 47, Hydro Pump 52, Charge 57 | Lanturn |
| Lanturn | good rod | 30 | Rewrite | Stockpile, Swallow, Spit Up, BubbleBeam | Signal Beam 31, Scald 33, Surf 34, Thunderbolt 37, Discharge 40, Flash Cannon 43, Aqua Ring 47, Muddy Water 52, Volt Switch 54, Dazzling Gleam 55, Charge 57, Ice Beam 60, Swagger 65 | Lanturn |
| Remoraid | good rod | 32 | Oxide | BubbleBeam, Focus Energy, Bullet Seed, Water Pulse | as Octillery: Wring Out 36, Signal Beam 42, Ice Beam 48, Hyper Beam 55 | Octillery (from 33) |
| Remoraid | good rod | 32 | Rewrite | Screech, Aurora Beam, BubbleBeam, Focus Energy | as Octillery: Round 33, Charge Beam 35, Scald 37, Skitter Smack 40, Signal Beam 42, Ice Beam 48, Psychic 54, Hyper Beam 55, Swagger 61 | Octillery (from 33) |
| Tentacool | good rod | 32 | Oxide | BubbleBeam, Wrap, Barrier, Water Pulse | Poison Jab 33; as Tentacruel: Poison Jab 36, Screech 42, Hydro Pump 49, Wring Out 55 | Tentacruel (from 33) |
| Tentacool | good rod | 32 | Rewrite | Toxic Spikes, Water Pulse, BubbleBeam, Barrier | Poison Jab 33; as Tentacruel: Poison Jab 33, Aurora Beam 34, Sludge Bomb 39, Screech 42, Psybeam 44, Surf 49, Muddy Water 53, Throat Chop 54, Power Gem 56, Flip Turn 58, Ice Beam 60, Toxic 62, Skitter Smack 65, Confuse Ray 68 | Tentacruel (from 33) |
| Frogadier | good rod | 34 | Oxide | Faint Attack, Acrobatics, Low Kick, Waterfall | Fling 35; as Greninja: Scald 37, Dark Pulse 40, Extrasensory 43, Sludge Wave 47, Gunk Shot 51, Hydro Pump 55, Hydro Cannon 65 | Greninja (from 36) |
| Frogadier | good rod | 34 | Rewrite | Acrobatics, Low Kick, Mud Shot, Waterfall | Fling 35; as Greninja: Shadow Sneak 36, Scald 37, Dark Pulse 40, Extrasensory 43, Sludge Wave 47, Gunk Shot 51, Ice Beam 54, Surf 56, Throat Chop 58, Muddy Water 60, Taunt 62, Hydro Cannon 65 | Greninja (from 36) |
| Floatzel | surf | 36 | Oxide | Swift, Aqua Jet, Crunch, Agility | Whirlpool 39, Razor Wind 50 | Floatzel |
| Floatzel | surf | 36 | Rewrite | Crunch, Icy Wind, Flip Turn, Waterfall | Whirlpool 39, Liquidation 41, Low Sweep 44, Agility 51, Rock Tomb 53, Ice Fang 56, Wave Crash 62, Ice Punch 65 | Floatzel |
| Tentacruel | surf | 36 | Oxide | Wrap, Barrier, Water Pulse, Poison Jab | Screech 42, Hydro Pump 49, Wring Out 55 | Tentacruel |
| Tentacruel | surf | 36 | Rewrite | Barrier, Water Pulse, Poison Jab, Aurora Beam | Sludge Bomb 39, Screech 42, Psybeam 44, Surf 49, Muddy Water 53, Throat Chop 54, Power Gem 56, Flip Turn 58, Ice Beam 60, Toxic 62, Skitter Smack 65, Confuse Ray 68 | Tentacruel |
| Gastrodon | surf | 39 | Oxide | Water Pulse, Mud Bomb, Hidden Power, Body Slam | Muddy Water 41, Recover 54 | Gastrodon |
| Gastrodon | surf | 39 | Rewrite | Body Slam, AncientPower, Earth Power, Clear Smog | Muddy Water 41, Bulldoze 44, Sludge Bomb 46, Ice Beam 49, Recover 54, Skitter Smack 56, Rock Tomb 60, Block 65 | Gastrodon |
| Mantine | surf | 39 | Oxide | Wing Attack, Water Pulse, Take Down, Confuse Ray | Bounce 40, Aqua Ring 46, Hydro Pump 49 | Mantine |
| Mantine | surf | 39 | Rewrite | Take Down, Signal Beam, Round, Confuse Ray | Bounce 40, Psybeam 41, Surf 43, Aqua Ring 46, Scald 49, Air Slash 54, Roost 56, Muddy Water 58, Ice Beam 60, Swagger 65 | Mantine |
| Floatzel | super rod | 40 | Oxide | Aqua Jet, Crunch, Agility, Whirlpool | Razor Wind 50 | Floatzel |
| Floatzel | super rod | 40 | Rewrite | Icy Wind, Flip Turn, Waterfall, Whirlpool | Liquidation 41, Low Sweep 44, Agility 51, Rock Tomb 53, Ice Fang 56, Wave Crash 62, Ice Punch 65 | Floatzel |
| Mantine | super rod | 40 | Oxide | Water Pulse, Take Down, Confuse Ray, Bounce | Aqua Ring 46, Hydro Pump 49 | Mantine |
| Mantine | super rod | 40 | Rewrite | Signal Beam, Round, Confuse Ray, Bounce | Psybeam 41, Surf 43, Aqua Ring 46, Scald 49, Air Slash 54, Roost 56, Muddy Water 58, Ice Beam 60, Swagger 65 | Mantine |
| Frogadier | surf | 42 | Oxide | Low Kick, Waterfall, Fling, Dark Pulse | as Greninja: Extrasensory 43, Sludge Wave 47, Gunk Shot 51, Hydro Pump 55, Hydro Cannon 65 | Greninja (from 43) |
| Frogadier | surf | 42 | Rewrite | Mud Shot, Waterfall, Fling, Dark Pulse | as Greninja: Extrasensory 43, Sludge Wave 47, Gunk Shot 51, Ice Beam 54, Surf 56, Throat Chop 58, Muddy Water 60, Taunt 62, Hydro Cannon 65 | Greninja (from 43) |
| Gastrodon | super rod | 43 | Oxide | Mud Bomb, Hidden Power, Body Slam, Muddy Water | Recover 54 | Gastrodon |
| Gastrodon | super rod | 43 | Rewrite | AncientPower, Earth Power, Clear Smog, Muddy Water | Bulldoze 44, Sludge Bomb 46, Ice Beam 49, Recover 54, Skitter Smack 56, Rock Tomb 60, Block 65 | Gastrodon |
| Wailord | super rod | 43 | Oxide | Rest, Brine, Water Spout, Amnesia | Dive 46, Bounce 54, Hydro Pump 62 | Wailord |
| Wailord | super rod | 43 | Rewrite | Rest, Brine, Water Spout, Amnesia | Dive 46, Iron Head 48, Rock Tomb 50, Bounce 54, Zen Headbutt 55, Ice Beam 56, Surf 62, Earthquake 65 | Wailord |
| Toxapex | super rod | 46 | Oxide | Toxic, Venom Drench, Poison Jab, Liquidation | nothing | Toxapex |
| Toxapex | super rod | 46 | Rewrite | Pin Missile, Venom Drench, Poison Jab, Liquidation | Lunge 53, Ice Beam 54, Sludge Bomb 56, Iron Defense 61 | Toxapex |

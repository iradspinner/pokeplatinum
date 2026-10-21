# Volkner's split: what each catch knows and learns

Written by `tools/oxide/balance/learncheck.py sheets` for check 6 of the learnset baseline (`docs/oxide/learnset-checks.md`). One table per capture area first offered in Volkner's split, whose cap is 68. Each Pokemon is read at the lowest level it is found at there. "Knows at capture" is the last four moves its list gives by that level; "learns by level-up" is every entry it reaches after capture up to 68, evolving on time, with each later stage's moves under its name; "at the cap" is the stage it can be by then and the next one after. A row marked Rewrite shows the learnset rewrite's lists (the tree's) where it differs from the row marked Oxide, Oxide's lists before the learnset rewrite (`da6b92496c`); a row marked both is the same in each. Relearner-only moves and egg moves are left out.

## Acuity Cavern

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 68 | At the cap |
|---|---|---|---|---|---|---|
| Articuno | static | 50 | Oxide | AncientPower, Agility, Ice Beam, Reflect | Roost 57, Tailwind 64 | Articuno |
| Articuno | static | 50 | Rewrite | AncientPower, Agility, Ice Beam, Reflect | Glaciate 54, Roost 57, Tailwind 64, Air Slash 66 | Articuno |
| Cresselia | static | 50 | Oxide | Mist, Aurora Beam, Future Sight, Slash | Moonlight 57, Psycho Cut 66 | Cresselia |
| Cresselia | static | 50 | Rewrite | Aurora Beam, Future Sight, Slash, Esper Wing | Take Heart 54, Moonlight 57, Psycho Cut 66, Confuse Ray 68 | Cresselia |
| Pheromosa | static | 50 | Oxide | Stomp, Agility, Lunge, Bounce | Speed Swap 55, Bug Buzz 60, Quiver Dance 65 | Pheromosa |
| Pheromosa | static | 50 | Rewrite | Stomp, Agility, Lunge, Bounce | Bug Bite 51, Double Kick 52, Triple Kick 53, Bug Buzz 60, Quiver Dance 65 | Pheromosa |

## Route 222

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 68 | At the cap |
|---|---|---|---|---|---|---|
| Remoraid | old rod | 18 | Oxide | Water Gun, Lock-On, Psybeam, Aurora Beam | BubbleBeam 19, Focus Energy 23; as Octillery: Octazooka 25, Bullet Seed 29, Wring Out 36, Signal Beam 42, Ice Beam 48, Hyper Beam 55 | Octillery (from 25) |
| Remoraid | old rod | 18 | Rewrite | Screech, Lock-On, Psybeam, Aurora Beam | BubbleBeam 19, Focus Energy 23; as Octillery: Octazooka 25, Rock Blast 27, Bullet Seed 29, Scald 35, Signal Beam 42, Skitter Smack 44, Ice Beam 48, Hyper Beam 55, Snipe Shot 56, Swagger 67 | Octillery (from 25) |
| Tentacool | old rod | 18 | Oxide | Supersonic, Constrict, Acid, Toxic Spikes | BubbleBeam 19, Wrap 22, Barrier 26, Water Pulse 29; as Tentacruel: Poison Jab 36, Screech 42, Hydro Pump 49, Wring Out 55 | Tentacruel (from 30) |
| Tentacool | old rod | 18 | Rewrite | Pounce, Acid, Toxic Spikes, Icy Wind | BubbleBeam 19, Barrier 26, Water Pulse 29; as Tentacruel: Psybeam 34, Poison Jab 36, Scald 38, Screech 42, Surf 49, Sludge Wave 52, Sludge Bomb 54, Muddy Water 58, Power Gem 60, Throat Chop 66, Flip Turn 68 | Tentacruel (from 30) |
| Mantyke | old rod | 19 | Oxide | Supersonic, BubbleBeam, Headbutt, Agility | Wing Attack 22, Water Pulse 28; as Mantine: Take Down 31, Confuse Ray 37, Bounce 40, Aqua Ring 46, Hydro Pump 49 | Mantine (from 30) |
| Mantyke | old rod | 19 | Rewrite | Icy Wind, BubbleBeam, Headbutt, Agility | Wing Attack 22, Water Pulse 28; as Mantine: Take Down 31, Scald 34, Confuse Ray 37, Bounce 40, Signal Beam 42, Aqua Ring 46, Surf 50, Air Slash 52, Psychic 58, Muddy Water 60, Swagger 66 | Mantine (from 30) |
| Psyduck | old rod | 19 | Oxide | Tail Whip, Water Gun, Disable, Confusion | Water Pulse 22, Fury Swipes 27, Screech 31; as Golduck: Psych Up 37, Zen Headbutt 44, Amnesia 50, Hydro Pump 56 | Golduck (from 33) |
| Psyduck | old rod | 19 | Rewrite | Screech, Water Gun, Disable, Confusion | Water Pulse 22, Fury Swipes 27, Low Sweep 29; as Golduck: Aurora Beam 34, Psych Up 37, Scald 39, Surf 42, Zen Headbutt 44, Aqua Step 47, Amnesia 50, Muddy Water 56, Power Gem 58, Ice Beam 60, Psychic 66, Flip Turn 68 | Golduck (from 33) |
| Buizel | old rod | 20 | Oxide | Quick Attack, Water Gun, Pursuit, Swift | Aqua Jet 21; as Floatzel: Crunch 26, Agility 29, Whirlpool 39, Razor Wind 50 | Floatzel (from 26) |
| Buizel | old rod | 20 | Rewrite | Quick Attack, Scary Face, Pursuit, Swift | Aqua Jet 21; as Floatzel: Crunch 26, Low Sweep 28, Icy Wind 30, Rock Tomb 35, Whirlpool 39, BubbleBeam 43, Agility 45, Triple Dive 54, Swagger 67 | Floatzel (from 26) |
| Lanturn | good rod | 30 | Oxide | Stockpile, Swallow, Spit Up, BubbleBeam | Signal Beam 35, Discharge 40, Aqua Ring 47, Hydro Pump 52, Charge 57 | Lanturn |
| Lanturn | good rod | 30 | Rewrite | Stockpile, Swallow, Spit Up, BubbleBeam | Signal Beam 35, Discharge 40, Thunderbolt 42, Aqua Ring 47, Muddy Water 52, Charge 57, Flash Cannon 59, Scald 61, Volt Switch 66, Dazzling Gleam 68 | Lanturn |
| Shellos | good rod | 30 | Oxide | Water Pulse, Mud Bomb, Hidden Power, Body Slam | as Gastrodon: Muddy Water 41, Recover 54 | Gastrodon (from 31) |
| Shellos | good rod | 30 | Rewrite | Water Pulse, Mud Bomb, Hidden Power, Body Slam | as Gastrodon: AncientPower 31, Clear Smog 34, Muddy Water 41, Earth Power 43, Bulldoze 45, Ice Beam 50, Thousand Waves 52, Recover 54, Skitter Smack 58, Rock Tomb 60, Block 66, Sludge 68 | Gastrodon (from 31) |
| Lumineon | good rod | 32 | Oxide | Gust, Water Pulse, Captivate, Safeguard | Aqua Ring 35, Whirlpool 42, U-turn 48, Bounce 53, Silver Wind 59 | Lumineon |
| Lumineon | good rod | 32 | Rewrite | Gust, Water Pulse, Captivate, Safeguard | Aqua Ring 35, Signal Beam 37, Whirlpool 42, Fillet Away 45, U-turn 48, Crunch 50, Bounce 53, Silver Wind 59, Scald 61, Dive 66, Flip Turn 68 | Lumineon |
| Tentacool | good rod | 32 | Oxide | BubbleBeam, Wrap, Barrier, Water Pulse | Poison Jab 33; as Tentacruel: Poison Jab 36, Screech 42, Hydro Pump 49, Wring Out 55 | Tentacruel (from 33) |
| Tentacool | good rod | 32 | Rewrite | Icy Wind, BubbleBeam, Barrier, Water Pulse | Poison Jab 33; as Tentacruel: Psybeam 34, Poison Jab 36, Scald 38, Screech 42, Surf 49, Sludge Wave 52, Sludge Bomb 54, Muddy Water 58, Power Gem 60, Throat Chop 66, Flip Turn 68 | Tentacruel (from 33) |
| Floatzel | good rod | 34 | Oxide | Swift, Aqua Jet, Crunch, Agility | Whirlpool 39, Razor Wind 50 | Floatzel |
| Floatzel | good rod | 34 | Rewrite | Aqua Jet, Crunch, Low Sweep, Icy Wind | Rock Tomb 35, Whirlpool 39, BubbleBeam 43, Agility 45, Triple Dive 54, Swagger 67 | Floatzel |
| Floatzel | surf | 36 | Oxide | Swift, Aqua Jet, Crunch, Agility | Whirlpool 39, Razor Wind 50 | Floatzel |
| Floatzel | surf | 36 | Rewrite | Crunch, Low Sweep, Icy Wind, Rock Tomb | Whirlpool 39, BubbleBeam 43, Agility 45, Triple Dive 54, Swagger 67 | Floatzel |
| Mareanie | surf | 36 | Oxide | Recover, Spike Cannon, Pin Missile, Toxic | as Toxapex: Toxic 39, Venom Drench 42, Poison Jab 43, Liquidation 45 | Toxapex (from 38) |
| Mareanie | surf | 36 | Rewrite | Recover, Fury Swipes, Pin Missile, Toxic | Water Pulse 38; as Toxapex: Toxic 39, Venom Drench 42, Poison Jab 43, Liquidation 45, Sludge Bomb 48, Ice Beam 50, Iron Defense 64 | Toxapex (from 38) |
| Vikavolt | wild | 38 | Oxide | Crunch, Bite, Spark, Signal Beam | Discharge 48, Bug Buzz 55, Thunderbolt 65, Zap Cannon 66 | Vikavolt |
| Vikavolt | wild | 38 | Rewrite | Mud Shot, Spark, Signal Beam, Rising Voltage | Bug Buzz 40, Air Slash 42, Discharge 48, Agility 50, Energy Ball 56, Iron Defense 57, Thunderbolt 65, Volt Switch 67 | Vikavolt |
| Chatot | wild | 39 | Oxide | Taunt, Mimic, Roost, Uproar | FeatherDance 41, Hyper Voice 45 | Chatot |
| Chatot | wild | 39 | Rewrite | Mimic, Roost, Ominous Wind, Echoed Voice | FeatherDance 41, Hyper Voice 45, Heat Wave 48, Uproar 54, Air Slash 56, U-turn 58, Steel Wing 64, Bounce 66 | Chatot |
| Corvisquire | wild | 39 | Oxide | Steel Wing, Drill Peck, FeatherDance, Revenge | as Corviknight: Defog 42, Iron Head 44, Brave Bird 49, Body Press 55, Roost 65 | Corviknight (from 40) |
| Corvisquire | wild | 39 | Rewrite | Steel Wing, Drill Peck, FeatherDance, Revenge | Throat Chop 40; as Corviknight: Defog 42, Iron Head 44, U-turn 46, Power Trip 47, Brave Bird 49, Double-Edge 53, Body Press 55, Shift Gear 57, Body Slam 61, Roost 65 | Corviknight (from 40) |
| Galvantula | wild | 39 | Oxide | Struggle Bug, Discharge, Signal Beam, Energy Ball | Sucker Punch 43, Thunderbolt 48, Bug Buzz 51, Thunder 55, Volt Switch 65 | Galvantula |
| Galvantula | wild | 39 | Rewrite | Discharge, Giga Drain, Signal Beam, Energy Ball | Sucker Punch 43, Swift 45, Thunderbolt 48, Bug Buzz 51, Agility 54, Sludge Bomb 58, Volt Switch 65, Dark Pulse 67 | Galvantula |
| Houndoom | wild | 39 | Oxide | Bite, Odor Sleuth, Fire Fang, Faint Attack | Embargo 44, Flamethrower 48, Crunch 54, Nasty Plot 60 | Houndoom |
| Houndoom | wild | 39 | Rewrite | Odor Sleuth, Fire Fang, Fire Pledge, Faint Attack | Mud Shot 42, Embargo 44, Flamethrower 48, Dark Pulse 50, Crunch 54, Fiery Wrath 56, Shadow Ball 58, Nasty Plot 60, Toxic 62, Uproar 66, Will-O-Wisp 68 | Houndoom |
| Liepard | wild | 39 | Oxide | Assurance, Hone Claws, Slash, Taunt | Sucker Punch 43, Nasty Plot 44, Night Slash 44, Snatch 47, Play Rough 54 | Liepard |
| Liepard | wild | 39 | Rewrite | Power Trip, Slash, Dark Pulse, Taunt | Skitter Smack 40, Sucker Punch 43, Night Slash 44, Snatch 47, Throat Chop 49, Shadow Ball 51, Play Rough 54, Psycho Cut 59, U-turn 61, Nasty Plot 67 | Liepard |
| Mantine | surf | 39 | Oxide | Wing Attack, Water Pulse, Take Down, Confuse Ray | Bounce 40, Aqua Ring 46, Hydro Pump 49 | Mantine |
| Mantine | surf | 39 | Rewrite | Water Pulse, Take Down, Scald, Confuse Ray | Bounce 40, Signal Beam 42, Aqua Ring 46, Surf 50, Air Slash 52, Psychic 58, Muddy Water 60, Swagger 66 | Mantine |
| Talonflame | wild | 39 | Oxide | Roost, Will-O-Wisp, Natural Gift, Acrobatics | Me First 42, Tailwind 46, Flare Blitz 51, Brave Bird 55 | Talonflame |
| Talonflame | wild | 39 | Rewrite | Roost, Will-O-Wisp, Natural Gift, Acrobatics | Steel Wing 40, U-turn 42, Tailwind 46, Flare Blitz 51, Brave Bird 55, Overheat 57, Agility 59, Bulk Up 64 | Talonflame |
| Tentacruel | surf | 39 | Oxide | Wrap, Barrier, Water Pulse, Poison Jab | Screech 42, Hydro Pump 49, Wring Out 55 | Tentacruel |
| Tentacruel | surf | 39 | Rewrite | Water Pulse, Psybeam, Poison Jab, Scald | Screech 42, Surf 49, Sludge Wave 52, Sludge Bomb 54, Muddy Water 58, Power Gem 60, Throat Chop 66, Flip Turn 68 | Tentacruel |
| Togedemaru | wild | 39 | Oxide | Smart Strike, Super Fang, Zing Zap, Iron Head | Electroweb 42, Wild Charge 48, Spiky Shield 55 | Togedemaru |
| Togedemaru | wild | 39 | Rewrite | Twineedle, Zing Zap, Metal Claw, Iron Head | Electroweb 42, Wild Charge 48, Poison Jab 54, Zen Headbutt 56, Bounce 62, Tickle 64 | Togedemaru |
| Emolga | wild | 40 | Oxide | Acrobatics, Encore, Light Screen, Volt Switch | Discharge 50, Agility 50 | Emolga |
| Emolga | wild | 40 | Rewrite | Electro Ball, Encore, Light Screen, Volt Switch | Agility 49, Discharge 50, Energy Ball 52, Thunderbolt 54, Air Slash 59, Shadow Ball 61 | Emolga |
| Luxray | wild | 40 | Oxide | Bite, Roar, Swagger, Thunder Fang | Crunch 42, Scary Face 49, Discharge 56, Double-Edge 60, Volt Tackle 64 | Luxray |
| Luxray | wild | 40 | Rewrite | Bite, Swagger, Thunder Fang, Mean Look | Crunch 42, Fire Fang 44, Scary Face 49, Ice Fang 51, Discharge 56, Psychic Fangs 58, Double-Edge 60, Volt Tackle 64, Throat Chop 66, Thunder Wave 68 | Luxray |
| Mantine | super rod | 40 | Oxide | Water Pulse, Take Down, Confuse Ray, Bounce | Aqua Ring 46, Hydro Pump 49 | Mantine |
| Mantine | super rod | 40 | Rewrite | Take Down, Scald, Confuse Ray, Bounce | Signal Beam 42, Aqua Ring 46, Surf 50, Air Slash 52, Psychic 58, Muddy Water 60, Swagger 66 | Mantine |
| Pawmot | wild | 40 | Oxide | Arm Thrust, Play Rough, Super Fang, Entrainment | Wild Charge 44, Close Combat 49, Mach Punch 55, Double Shock 61 | Pawmot |
| Pawmot | wild | 40 | Rewrite | Arm Thrust, Play Rough, Super Fang, Entrainment | Wild Charge 44, Thunderous Kick 46, Close Combat 49, Mach Punch 55, Rock Tomb 57, Double Shock 61, Low Sweep 63, Fire Punch 65 | Pawmot |
| Toucannon | wild | 40 | Oxide | Fury Attack, Screech, Drill Peck, Bullet Seed | FeatherDance 44, Hyper Voice 50 | Toucannon |
| Toucannon | wild | 40 | Rewrite | Roost, Screech, Drill Peck, Bullet Seed | Throat Chop 42, FeatherDance 44, Hyper Voice 50, Bounce 52, Take Down 58, Body Slam 60, Rock Climb 66 | Toucannon |
| Toxapex | super rod | 40 | Oxide | Recover, Spike Cannon, Pin Missile, Toxic | Venom Drench 42, Poison Jab 43, Liquidation 45 | Toxapex |
| Toxapex | super rod | 40 | Rewrite | Venoshock, Recover, Pin Missile, Toxic | Venom Drench 42, Poison Jab 43, Liquidation 45, Sludge Bomb 48, Ice Beam 50, Iron Defense 64 | Toxapex |
| Araquanid | wild | 41 | Oxide | Headbutt, Soak, Dive, Lunge | Scald 48, Hydro Pump 51, Liquidation 55, Leech Life 61 | Araquanid |
| Araquanid | wild | 41 | Rewrite | Spider Web, Soak, Dive, Lunge | Skitter Smack 43, Scald 48, Poison Jab 51, Liquidation 55, Ice Fang 59, Leech Life 61 | Araquanid |
| Floatzel | wild | 41 | Oxide | Aqua Jet, Crunch, Agility, Whirlpool | Razor Wind 50 | Floatzel |
| Floatzel | wild | 41 | Rewrite | Low Sweep, Icy Wind, Rock Tomb, Whirlpool | BubbleBeam 43, Agility 45, Triple Dive 54, Swagger 67 | Floatzel |
| Shellos | wild | 41 | Oxide | Mud Bomb, Hidden Power, Body Slam, Muddy Water | as Gastrodon: Recover 54 | Gastrodon (from 42) |
| Shellos | wild | 41 | Rewrite | Mud Bomb, Hidden Power, Body Slam, Muddy Water | as Gastrodon: Earth Power 43, Bulldoze 45, Ice Beam 50, Thousand Waves 52, Recover 54, Skitter Smack 58, Rock Tomb 60, Block 66, Sludge 68 | Gastrodon (from 42) |
| Gastrodon | surf | 42 | Oxide | Mud Bomb, Hidden Power, Body Slam, Muddy Water | Recover 54 | Gastrodon |
| Gastrodon | surf | 42 | Rewrite | Body Slam, AncientPower, Clear Smog, Muddy Water | Earth Power 43, Bulldoze 45, Ice Beam 50, Thousand Waves 52, Recover 54, Skitter Smack 58, Rock Tomb 60, Block 66, Sludge 68 | Gastrodon |
| Gastrodon | super rod | 43 | Oxide | Mud Bomb, Hidden Power, Body Slam, Muddy Water | Recover 54 | Gastrodon |
| Gastrodon | super rod | 43 | Rewrite | AncientPower, Clear Smog, Muddy Water, Earth Power | Bulldoze 45, Ice Beam 50, Thousand Waves 52, Recover 54, Skitter Smack 58, Rock Tomb 60, Block 66, Sludge 68 | Gastrodon |
| Poliwrath | super rod | 43 | Oxide | Hypnosis, DoubleSlap, Submission, DynamicPunch | Mind Reader 53 | Poliwrath |
| Poliwrath | super rod | 43 | Rewrite | Wake-Up Slap, Circle Throw, Throat Chop, Brick Break | Body Press 45, Jet Punch 46, Victory Dance 50, Mind Reader 53, Rock Tomb 55, Low Sweep 57, Ice Punch 62, Drain Punch 64 | Poliwrath |
| Greninja | super rod | 46 | Oxide | Fling, Scald, Dark Pulse, Extrasensory | Sludge Wave 47, Gunk Shot 51, Hydro Pump 55, Hydro Cannon 65 | Greninja |
| Greninja | super rod | 46 | Rewrite | Scald, Dark Pulse, Bounce, Extrasensory | Sludge Wave 47, Water Shuriken 49, Gunk Shot 51, Throat Chop 56, Hydro Cannon 65 | Greninja |

## Sunyshore City

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 68 | At the cap |
|---|---|---|---|---|---|---|
| Mantyke | old rod | 18 | Oxide | Bubble, Supersonic, BubbleBeam, Headbutt | Agility 19, Wing Attack 22, Water Pulse 28; as Mantine: Take Down 31, Confuse Ray 37, Bounce 40, Aqua Ring 46, Hydro Pump 49 | Mantine (from 30) |
| Mantyke | old rod | 18 | Rewrite | Bubble, Icy Wind, BubbleBeam, Headbutt | Agility 19, Wing Attack 22, Water Pulse 28; as Mantine: Take Down 31, Scald 34, Confuse Ray 37, Bounce 40, Signal Beam 42, Aqua Ring 46, Surf 50, Air Slash 52, Psychic 58, Muddy Water 60, Swagger 66 | Mantine (from 30) |
| Remoraid | old rod | 18 | Oxide | Water Gun, Lock-On, Psybeam, Aurora Beam | BubbleBeam 19, Focus Energy 23; as Octillery: Octazooka 25, Bullet Seed 29, Wring Out 36, Signal Beam 42, Ice Beam 48, Hyper Beam 55 | Octillery (from 25) |
| Remoraid | old rod | 18 | Rewrite | Screech, Lock-On, Psybeam, Aurora Beam | BubbleBeam 19, Focus Energy 23; as Octillery: Octazooka 25, Rock Blast 27, Bullet Seed 29, Scald 35, Signal Beam 42, Skitter Smack 44, Ice Beam 48, Hyper Beam 55, Snipe Shot 56, Swagger 67 | Octillery (from 25) |
| Chinchou | old rod | 19 | Oxide | Thunder Wave, Flail, Water Gun, Confuse Ray | Spark 20, Take Down 23; as Lanturn: Stockpile 27, Swallow 27, Spit Up 27, BubbleBeam 30, Signal Beam 35, Discharge 40, Aqua Ring 47, Hydro Pump 52, Charge 57 | Lanturn (from 27) |
| Chinchou | old rod | 19 | Rewrite | Water Gun, Chilling Water, Confuse Ray, Icy Wind | Spark 20, Take Down 23, ParabolicCharge 25; as Lanturn: Stockpile 27, Swallow 28, Spit Up 29, BubbleBeam 30, Signal Beam 35, Discharge 40, Thunderbolt 42, Aqua Ring 47, Muddy Water 52, Charge 57, Flash Cannon 59, Scald 61, Volt Switch 66, Dazzling Gleam 68 | Lanturn (from 27) |
| Shellos | old rod | 19 to 20 | Oxide | Harden, Water Pulse, Mud Bomb, Hidden Power | Body Slam 29; as Gastrodon: Muddy Water 41, Recover 54 | Gastrodon (from 30) |
| Shellos | old rod | 19 to 20 | Rewrite | Swagger, Water Pulse, Mud Bomb, Hidden Power | Body Slam 29; as Gastrodon: AncientPower 31, Clear Smog 34, Muddy Water 41, Earth Power 43, Bulldoze 45, Ice Beam 50, Thousand Waves 52, Recover 54, Skitter Smack 58, Rock Tomb 60, Block 66, Sludge 68 | Gastrodon (from 30) |
| Finneon | good rod | 30 | Oxide | Gust, Water Pulse, Captivate, Safeguard | as Lumineon: Aqua Ring 35, Whirlpool 42, U-turn 48, Bounce 53, Silver Wind 59 | Lumineon (from 31) |
| Finneon | good rod | 30 | Rewrite | Water Pulse, Captivate, Chilling Water, Safeguard | as Lumineon: Aqua Ring 35, Signal Beam 37, Whirlpool 42, Fillet Away 45, U-turn 48, Crunch 50, Bounce 53, Silver Wind 59, Scald 61, Dive 66, Flip Turn 68 | Lumineon (from 31) |
| Lanturn | good rod | 30 | Oxide | Stockpile, Swallow, Spit Up, BubbleBeam | Signal Beam 35, Discharge 40, Aqua Ring 47, Hydro Pump 52, Charge 57 | Lanturn |
| Lanturn | good rod | 30 | Rewrite | Stockpile, Swallow, Spit Up, BubbleBeam | Signal Beam 35, Discharge 40, Thunderbolt 42, Aqua Ring 47, Muddy Water 52, Charge 57, Flash Cannon 59, Scald 61, Volt Switch 66, Dazzling Gleam 68 | Lanturn |
| Remoraid | good rod | 32 | Oxide | BubbleBeam, Focus Energy, Bullet Seed, Water Pulse | as Octillery: Wring Out 36, Signal Beam 42, Ice Beam 48, Hyper Beam 55 | Octillery (from 33) |
| Remoraid | good rod | 32 | Rewrite | BubbleBeam, Focus Energy, Bullet Seed, Water Pulse | as Octillery: Scald 35, Signal Beam 42, Skitter Smack 44, Ice Beam 48, Hyper Beam 55, Snipe Shot 56, Swagger 67 | Octillery (from 33) |
| Tentacool | good rod | 32 | Oxide | BubbleBeam, Wrap, Barrier, Water Pulse | Poison Jab 33; as Tentacruel: Poison Jab 36, Screech 42, Hydro Pump 49, Wring Out 55 | Tentacruel (from 33) |
| Tentacool | good rod | 32 | Rewrite | Icy Wind, BubbleBeam, Barrier, Water Pulse | Poison Jab 33; as Tentacruel: Psybeam 34, Poison Jab 36, Scald 38, Screech 42, Surf 49, Sludge Wave 52, Sludge Bomb 54, Muddy Water 58, Power Gem 60, Throat Chop 66, Flip Turn 68 | Tentacruel (from 33) |
| Frogadier | good rod | 34 | Oxide | Faint Attack, Acrobatics, Low Kick, Waterfall | Fling 35; as Greninja: Scald 37, Dark Pulse 40, Extrasensory 43, Sludge Wave 47, Gunk Shot 51, Hydro Pump 55, Hydro Cannon 65 | Greninja (from 36) |
| Frogadier | good rod | 34 | Rewrite | Faint Attack, Acrobatics, Low Kick, Waterfall | Fling 35; as Greninja: Shadow Sneak 36, Scald 37, Dark Pulse 40, Bounce 41, Extrasensory 43, Sludge Wave 47, Water Shuriken 49, Gunk Shot 51, Throat Chop 56, Hydro Cannon 65 | Greninja (from 36) |
| Floatzel | surf | 36 | Oxide | Swift, Aqua Jet, Crunch, Agility | Whirlpool 39, Razor Wind 50 | Floatzel |
| Floatzel | surf | 36 | Rewrite | Crunch, Low Sweep, Icy Wind, Rock Tomb | Whirlpool 39, BubbleBeam 43, Agility 45, Triple Dive 54, Swagger 67 | Floatzel |
| Tentacruel | surf | 36 | Oxide | Wrap, Barrier, Water Pulse, Poison Jab | Screech 42, Hydro Pump 49, Wring Out 55 | Tentacruel |
| Tentacruel | surf | 36 | Rewrite | Barrier, Water Pulse, Psybeam, Poison Jab | Scald 38, Screech 42, Surf 49, Sludge Wave 52, Sludge Bomb 54, Muddy Water 58, Power Gem 60, Throat Chop 66, Flip Turn 68 | Tentacruel |
| Gastrodon | surf | 39 | Oxide | Water Pulse, Mud Bomb, Hidden Power, Body Slam | Muddy Water 41, Recover 54 | Gastrodon |
| Gastrodon | surf | 39 | Rewrite | Hidden Power, Body Slam, AncientPower, Clear Smog | Muddy Water 41, Earth Power 43, Bulldoze 45, Ice Beam 50, Thousand Waves 52, Recover 54, Skitter Smack 58, Rock Tomb 60, Block 66, Sludge 68 | Gastrodon |
| Mantine | surf | 39 | Oxide | Wing Attack, Water Pulse, Take Down, Confuse Ray | Bounce 40, Aqua Ring 46, Hydro Pump 49 | Mantine |
| Mantine | surf | 39 | Rewrite | Water Pulse, Take Down, Scald, Confuse Ray | Bounce 40, Signal Beam 42, Aqua Ring 46, Surf 50, Air Slash 52, Psychic 58, Muddy Water 60, Swagger 66 | Mantine |
| Floatzel | super rod | 40 | Oxide | Aqua Jet, Crunch, Agility, Whirlpool | Razor Wind 50 | Floatzel |
| Floatzel | super rod | 40 | Rewrite | Low Sweep, Icy Wind, Rock Tomb, Whirlpool | BubbleBeam 43, Agility 45, Triple Dive 54, Swagger 67 | Floatzel |
| Mantine | super rod | 40 | Oxide | Water Pulse, Take Down, Confuse Ray, Bounce | Aqua Ring 46, Hydro Pump 49 | Mantine |
| Mantine | super rod | 40 | Rewrite | Take Down, Scald, Confuse Ray, Bounce | Signal Beam 42, Aqua Ring 46, Surf 50, Air Slash 52, Psychic 58, Muddy Water 60, Swagger 66 | Mantine |
| Frogadier | surf | 42 | Oxide | Low Kick, Waterfall, Fling, Dark Pulse | as Greninja: Extrasensory 43, Sludge Wave 47, Gunk Shot 51, Hydro Pump 55, Hydro Cannon 65 | Greninja (from 43) |
| Frogadier | surf | 42 | Rewrite | Low Kick, Waterfall, Fling, Dark Pulse | as Greninja: Extrasensory 43, Sludge Wave 47, Water Shuriken 49, Gunk Shot 51, Throat Chop 56, Hydro Cannon 65 | Greninja (from 43) |
| Gastrodon | super rod | 43 | Oxide | Mud Bomb, Hidden Power, Body Slam, Muddy Water | Recover 54 | Gastrodon |
| Gastrodon | super rod | 43 | Rewrite | AncientPower, Clear Smog, Muddy Water, Earth Power | Bulldoze 45, Ice Beam 50, Thousand Waves 52, Recover 54, Skitter Smack 58, Rock Tomb 60, Block 66, Sludge 68 | Gastrodon |
| Wailord | super rod | 43 | Oxide | Rest, Brine, Water Spout, Amnesia | Dive 46, Bounce 54, Hydro Pump 62 | Wailord |
| Wailord | super rod | 43 | Rewrite | Rest, Brine, Water Spout, Amnesia | Dive 46, Iron Head 48, Bounce 54, Zen Headbutt 56, Surf 62, Ice Beam 64 | Wailord |
| Toxapex | super rod | 46 | Oxide | Toxic, Venom Drench, Poison Jab, Liquidation | nothing | Toxapex |
| Toxapex | super rod | 46 | Rewrite | Toxic, Venom Drench, Poison Jab, Liquidation | Sludge Bomb 48, Ice Beam 50, Iron Defense 64 | Toxapex |

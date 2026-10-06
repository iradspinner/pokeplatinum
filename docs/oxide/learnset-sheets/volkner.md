# Volkner's split: what each catch knows and learns

Written by `tools/oxide/balance/learncheck.py sheets` for check 6 of the learnset baseline (`docs/oxide/learnset-checks.md`). One table per capture area first offered in Volkner's split, whose cap is 68. Each Pokemon is read at the lowest level it is found at there. "Knows at capture" is the last four moves its list gives by that level; "learns by level-up" is every entry it reaches after capture up to 68, evolving on time, with each later stage's moves under its name; "at the cap" is the stage it can be by then and the next one after. A row marked v3 shows learnset v3 (unlanded, `origin/balance-learngen-v2`) where it differs from Oxide's lists; a row marked both is the same in each. Relearner-only moves and egg moves are left out. Nothing here is in the game data.

## Acuity Cavern

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 68 | At the cap |
|---|---|---|---|---|---|---|
| Articuno | static | 50 | Oxide | AncientPower, Agility, Ice Beam, Reflect | Roost 57, Tailwind 64 | Articuno |
| Articuno | static | 50 | v3 | AncientPower, Agility, Ice Beam, Reflect | Tailwind 64 | Articuno |
| Cresselia | static | 50 | both | Mist, Aurora Beam, Future Sight, Slash | Moonlight 57, Psycho Cut 66 | Cresselia |
| Pheromosa | static | 50 | Oxide | Stomp, Agility, Lunge, Bounce | Speed Swap 55, Bug Buzz 60, Quiver Dance 65 | Pheromosa |
| Pheromosa | static | 50 | v3 | Triple Kick, Stomp, Agility, Bounce | Lunge 53, Bug Buzz 60, Quiver Dance 65 | Pheromosa |

## Route 222

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 68 | At the cap |
|---|---|---|---|---|---|---|
| Remoraid | old rod | 18 | both | Water Gun, Lock-On, Psybeam, Aurora Beam | BubbleBeam 19, Focus Energy 23; as Octillery: Octazooka 25, Bullet Seed 29, Wring Out 36, Signal Beam 42, Ice Beam 48, Hyper Beam 55 | Octillery (from 25) |
| Tentacool | old rod | 18 | Oxide | Supersonic, Constrict, Acid, Toxic Spikes | BubbleBeam 19, Wrap 22, Barrier 26, Water Pulse 29; as Tentacruel: Poison Jab 36, Screech 42, Hydro Pump 49, Wring Out 55 | Tentacruel (from 30) |
| Tentacool | old rod | 18 | v3 | Supersonic, Water Gun, Acid, Toxic Spikes | BubbleBeam 19, Barrier 26, Water Pulse 29; as Tentacruel: Poison Jab 36, Screech 42, Toxic 44, Hydro Pump 49, Wring Out 55 | Tentacruel (from 30) |
| Mantyke | old rod | 19 | Oxide | Supersonic, BubbleBeam, Headbutt, Agility | Wing Attack 22, Water Pulse 28; as Mantine: Take Down 31, Confuse Ray 37, Bounce 40, Aqua Ring 46, Hydro Pump 49 | Mantine (from 30) |
| Mantyke | old rod | 19 | v3 | Supersonic, BubbleBeam, Headbutt, Agility | Wing Attack 22, Water Pulse 28; as Mantine: Take Down 31, Confuse Ray 37, Bounce 40, Aqua Ring 46, Hydro Pump 49, Air Slash 66 | Mantine (from 30) |
| Psyduck | old rod | 19 | Oxide | Tail Whip, Water Gun, Disable, Confusion | Water Pulse 22, Fury Swipes 27, Screech 31; as Golduck: Psych Up 37, Zen Headbutt 44, Amnesia 50, Hydro Pump 56 | Golduck (from 33) |
| Psyduck | old rod | 19 | v3 | Tail Whip, Water Gun, Disable, Confusion | Water Pulse 22, Fury Swipes 27, Screech 31; as Golduck: Psych Up 37, Zen Headbutt 44, Amnesia 50, Hydro Pump 56, Psychic 68 | Golduck (from 33) |
| Buizel | old rod | 20 | Oxide | Quick Attack, Water Gun, Pursuit, Swift | Aqua Jet 21; as Floatzel: Crunch 26, Agility 29, Whirlpool 39, Razor Wind 50 | Floatzel (from 26) |
| Buizel | old rod | 20 | v3 | Quick Attack, Water Gun, Pursuit, Swift | Aqua Jet 21; as Floatzel: Crunch 26, Agility 29, Ice Punch 66 | Floatzel (from 26) |
| Lanturn | good rod | 30 | Oxide | Stockpile, Swallow, Spit Up, BubbleBeam | Signal Beam 35, Discharge 40, Aqua Ring 47, Hydro Pump 52, Charge 57 | Lanturn |
| Lanturn | good rod | 30 | v3 | Stockpile, Swallow, Spit Up, BubbleBeam | Signal Beam 35, Aqua Ring 47, Hydro Pump 52, Discharge 53, Charge 57, Thunder 65 | Lanturn |
| Shellos | good rod | 30 | Oxide | Water Pulse, Mud Bomb, Hidden Power, Body Slam | as Gastrodon: Muddy Water 41, Recover 54 | Gastrodon (from 31) |
| Shellos | good rod | 30 | v3 | Water Pulse, Mud Bomb, Hidden Power, Body Slam | as Gastrodon: Muddy Water 39, Earthquake 44, Recover 54, Rock Slide 64 | Gastrodon (from 31) |
| Lumineon | good rod | 32 | Oxide | Gust, Water Pulse, Captivate, Safeguard | Aqua Ring 35, Whirlpool 42, U-turn 48, Bounce 53, Silver Wind 59 | Lumineon |
| Lumineon | good rod | 32 | v3 | Attract, Water Pulse, Captivate, Safeguard | Aqua Ring 35, U-turn 48, Bounce 53, Silver Wind 59, Ice Fang 65 | Lumineon |
| Tentacool | good rod | 32 | Oxide | BubbleBeam, Wrap, Barrier, Water Pulse | Poison Jab 33; as Tentacruel: Poison Jab 36, Screech 42, Hydro Pump 49, Wring Out 55 | Tentacruel (from 33) |
| Tentacool | good rod | 32 | v3 | Toxic Spikes, BubbleBeam, Barrier, Water Pulse | Poison Jab 33; as Tentacruel: Poison Jab 36, Screech 42, Toxic 44, Hydro Pump 49, Wring Out 55 | Tentacruel (from 33) |
| Floatzel | good rod | 34 | Oxide | Swift, Aqua Jet, Crunch, Agility | Whirlpool 39, Razor Wind 50 | Floatzel |
| Floatzel | good rod | 34 | v3 | Swift, Aqua Jet, Crunch, Agility | Ice Punch 66 | Floatzel |
| Floatzel | surf | 36 | Oxide | Swift, Aqua Jet, Crunch, Agility | Whirlpool 39, Razor Wind 50 | Floatzel |
| Floatzel | surf | 36 | v3 | Swift, Aqua Jet, Crunch, Agility | Ice Punch 66 | Floatzel |
| Mareanie | surf | 36 | Oxide | Recover, Spike Cannon, Pin Missile, Toxic | as Toxapex: Toxic 39, Venom Drench 42, Poison Jab 43, Liquidation 45 | Toxapex (from 38) |
| Mareanie | surf | 36 | v3 | Recover, Spike Cannon, Pin Missile, Toxic | as Toxapex: Baneful Bunker on evolving, Toxic 39, Venom Drench 42, Poison Jab 43, Liquidation 45 | Toxapex (from 38) |
| Vikavolt | wild | 38 | Oxide | Crunch, Bite, Spark, Signal Beam | Discharge 48, Bug Buzz 55, Thunderbolt 65, Zap Cannon 66 | Vikavolt |
| Vikavolt | wild | 38 | v3 | Spark, Crunch, Signal Beam, Discharge | Bug Buzz 53, X-Scissor 53, Thunderbolt 65, Zap Cannon 66 | Vikavolt |
| Chatot | wild | 39 | Oxide | Taunt, Mimic, Roost, Uproar | FeatherDance 41, Hyper Voice 45 | Chatot |
| Chatot | wild | 39 | v3 | Taunt, Mimic, Roost, Uproar | FeatherDance 41, Hyper Voice 45, Air Slash 63 | Chatot |
| Corvisquire | wild | 39 | both | Steel Wing, Drill Peck, FeatherDance, Revenge | as Corviknight: Defog 42, Iron Head 44, Brave Bird 49, Body Press 55, Roost 65 | Corviknight (from 40) |
| Galvantula | wild | 39 | Oxide | Struggle Bug, Discharge, Signal Beam, Energy Ball | Sucker Punch 43, Thunderbolt 48, Bug Buzz 51, Thunder 55, Volt Switch 65 | Galvantula |
| Galvantula | wild | 39 | v3 | Gastro Acid, Struggle Bug, Discharge, Signal Beam | Sucker Punch 43, Thunderbolt 48, Bug Buzz 51, Energy Ball 53, Thunder 55, Volt Switch 65 | Galvantula |
| Houndoom | wild | 39 | Oxide | Bite, Odor Sleuth, Fire Fang, Faint Attack | Embargo 44, Flamethrower 48, Crunch 54, Nasty Plot 60 | Houndoom |
| Houndoom | wild | 39 | v3 | Bite, Odor Sleuth, Fire Fang, Faint Attack | Embargo 44, Flamethrower 53, Crunch 54, Dark Pulse 56, Nasty Plot 60 | Houndoom |
| Liepard | wild | 39 | Oxide | Assurance, Hone Claws, Slash, Taunt | Sucker Punch 43, Nasty Plot 44, Night Slash 44, Snatch 47, Play Rough 54 | Liepard |
| Liepard | wild | 39 | v3 | Assurance, Hone Claws, Slash, Taunt | Sucker Punch 43, Nasty Plot 44, Night Slash 44, Snatch 47, Play Rough 54, Snarl 67 | Liepard |
| Mantine | surf | 39 | Oxide | Wing Attack, Water Pulse, Take Down, Confuse Ray | Bounce 40, Aqua Ring 46, Hydro Pump 49 | Mantine |
| Mantine | surf | 39 | v3 | Wing Attack, Water Pulse, Take Down, Confuse Ray | Bounce 40, Aqua Ring 46, Hydro Pump 49, Air Slash 66 | Mantine |
| Talonflame | wild | 39 | Oxide | Roost, Will-O-Wisp, Natural Gift, Acrobatics | Me First 42, Tailwind 46, Flare Blitz 51, Brave Bird 55 | Talonflame |
| Talonflame | wild | 39 | v3 | Roost, Will-O-Wisp, Natural Gift, Acrobatics | Me First 42, Tailwind 46, Flare Blitz 64, Brave Bird 65 | Talonflame |
| Tentacruel | surf | 39 | Oxide | Wrap, Barrier, Water Pulse, Poison Jab | Screech 42, Hydro Pump 49, Wring Out 55 | Tentacruel |
| Tentacruel | surf | 39 | v3 | BubbleBeam, Barrier, Water Pulse, Poison Jab | Screech 42, Toxic 44, Hydro Pump 49, Wring Out 55 | Tentacruel |
| Togedemaru | wild | 39 | both | Smart Strike, Super Fang, Zing Zap, Iron Head | Electroweb 42, Wild Charge 48, Spiky Shield 55 | Togedemaru |
| Emolga | wild | 40 | both | Acrobatics, Encore, Light Screen, Volt Switch | Discharge 50, Agility 50 | Emolga |
| Luxray | wild | 40 | Oxide | Bite, Roar, Swagger, Thunder Fang | Crunch 42, Scary Face 49, Discharge 56, Double-Edge 60, Volt Tackle 64 | Luxray |
| Luxray | wild | 40 | v3 | Spark, Bite, Roar, Swagger | Crunch 42, Scary Face 49, Thunder Fang 53, Double-Edge 60, Volt Tackle 64 | Luxray |
| Mantine | super rod | 40 | Oxide | Water Pulse, Take Down, Confuse Ray, Bounce | Aqua Ring 46, Hydro Pump 49 | Mantine |
| Mantine | super rod | 40 | v3 | Water Pulse, Take Down, Confuse Ray, Bounce | Aqua Ring 46, Hydro Pump 49, Air Slash 66 | Mantine |
| Pawmot | wild | 40 | Oxide | Arm Thrust, Play Rough, Super Fang, Entrainment | Wild Charge 44, Close Combat 49, Mach Punch 55, Double Shock 61 | Pawmot |
| Pawmot | wild | 40 | v3 | Arm Thrust, Play Rough, Super Fang, Entrainment | Mach Punch 55, Close Combat 56, Wild Charge 57, Double Shock 61 | Pawmot |
| Toucannon | wild | 40 | Oxide | Fury Attack, Screech, Drill Peck, Bullet Seed | FeatherDance 44, Hyper Voice 50 | Toucannon |
| Toucannon | wild | 40 | v3 | Roost, Fury Attack, Screech, Bullet Seed | FeatherDance 44, Hyper Voice 56, Rock Blast 65 | Toucannon |
| Toxapex | super rod | 40 | both | Recover, Spike Cannon, Pin Missile, Toxic | Venom Drench 42, Poison Jab 43, Liquidation 45 | Toxapex |
| Araquanid | wild | 41 | Oxide | Headbutt, Soak, Dive, Lunge | Scald 48, Hydro Pump 51, Liquidation 55, Leech Life 61 | Araquanid |
| Araquanid | wild | 41 | v3 | Headbutt, Soak, Dive, Lunge | Hydro Pump 51, Liquidation 55, Scald 60, Leech Life 61 | Araquanid |
| Floatzel | wild | 41 | Oxide | Aqua Jet, Crunch, Agility, Whirlpool | Razor Wind 50 | Floatzel |
| Floatzel | wild | 41 | v3 | Swift, Aqua Jet, Crunch, Agility | Ice Punch 66 | Floatzel |
| Shellos | wild | 41 | Oxide | Mud Bomb, Hidden Power, Body Slam, Muddy Water | as Gastrodon: Recover 54 | Gastrodon (from 42) |
| Shellos | wild | 41 | v3 | Mud Bomb, Hidden Power, Body Slam, Muddy Water | as Gastrodon: Earthquake 44, Recover 54, Rock Slide 64 | Gastrodon (from 42) |
| Gastrodon | surf | 42 | Oxide | Mud Bomb, Hidden Power, Body Slam, Muddy Water | Recover 54 | Gastrodon |
| Gastrodon | surf | 42 | v3 | Mud Bomb, Hidden Power, Body Slam, Muddy Water | Earthquake 44, Recover 54, Rock Slide 64 | Gastrodon |
| Gastrodon | super rod | 43 | Oxide | Mud Bomb, Hidden Power, Body Slam, Muddy Water | Recover 54 | Gastrodon |
| Gastrodon | super rod | 43 | v3 | Mud Bomb, Hidden Power, Body Slam, Muddy Water | Earthquake 44, Recover 54, Rock Slide 64 | Gastrodon |
| Poliwrath | super rod | 43 | Oxide | Hypnosis, DoubleSlap, Submission, DynamicPunch | Mind Reader 53 | Poliwrath |
| Poliwrath | super rod | 43 | v3 | BubbleBeam, Hypnosis, DoubleSlap, DynamicPunch | Mind Reader 53 | Poliwrath |
| Greninja | super rod | 46 | both | Fling, Scald, Dark Pulse, Extrasensory | Sludge Wave 47, Gunk Shot 51, Hydro Pump 55, Hydro Cannon 65 | Greninja |

## Sunyshore City

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 68 | At the cap |
|---|---|---|---|---|---|---|
| Mantyke | old rod | 18 | Oxide | Bubble, Supersonic, BubbleBeam, Headbutt | Agility 19, Wing Attack 22, Water Pulse 28; as Mantine: Take Down 31, Confuse Ray 37, Bounce 40, Aqua Ring 46, Hydro Pump 49 | Mantine (from 30) |
| Mantyke | old rod | 18 | v3 | Bubble, Supersonic, BubbleBeam, Headbutt | Agility 19, Wing Attack 22, Water Pulse 28; as Mantine: Take Down 31, Confuse Ray 37, Bounce 40, Aqua Ring 46, Hydro Pump 49, Air Slash 66 | Mantine (from 30) |
| Remoraid | old rod | 18 | both | Water Gun, Lock-On, Psybeam, Aurora Beam | BubbleBeam 19, Focus Energy 23; as Octillery: Octazooka 25, Bullet Seed 29, Wring Out 36, Signal Beam 42, Ice Beam 48, Hyper Beam 55 | Octillery (from 25) |
| Chinchou | old rod | 19 | Oxide | Thunder Wave, Flail, Water Gun, Confuse Ray | Spark 20, Take Down 23; as Lanturn: Stockpile 27, Swallow 27, Spit Up 27, BubbleBeam 30, Signal Beam 35, Discharge 40, Aqua Ring 47, Hydro Pump 52, Charge 57 | Lanturn (from 27) |
| Chinchou | old rod | 19 | v3 | Thunder Wave, Flail, Water Gun, Confuse Ray | Spark 20, Take Down 23; as Lanturn: Stockpile 27, Swallow 27, Spit Up 27, BubbleBeam 30, Signal Beam 35, Aqua Ring 47, Hydro Pump 52, Discharge 53, Charge 57, Thunder 65 | Lanturn (from 27) |
| Shellos | old rod | 19 to 20 | Oxide | Harden, Water Pulse, Mud Bomb, Hidden Power | Body Slam 29; as Gastrodon: Muddy Water 41, Recover 54 | Gastrodon (from 30) |
| Shellos | old rod | 19 to 20 | v3 | Harden, Water Pulse, Mud Bomb, Hidden Power | Body Slam 29; as Gastrodon: Muddy Water 39, Earthquake 44, Recover 54, Rock Slide 64 | Gastrodon (from 30) |
| Finneon | good rod | 30 | Oxide | Gust, Water Pulse, Captivate, Safeguard | as Lumineon: Aqua Ring 35, Whirlpool 42, U-turn 48, Bounce 53, Silver Wind 59 | Lumineon (from 31) |
| Finneon | good rod | 30 | v3 | Attract, Water Pulse, Captivate, Safeguard | as Lumineon: Aqua Ring 35, U-turn 48, Bounce 53, Silver Wind 59, Ice Fang 65 | Lumineon (from 31) |
| Lanturn | good rod | 30 | Oxide | Stockpile, Swallow, Spit Up, BubbleBeam | Signal Beam 35, Discharge 40, Aqua Ring 47, Hydro Pump 52, Charge 57 | Lanturn |
| Lanturn | good rod | 30 | v3 | Stockpile, Swallow, Spit Up, BubbleBeam | Signal Beam 35, Aqua Ring 47, Hydro Pump 52, Discharge 53, Charge 57, Thunder 65 | Lanturn |
| Remoraid | good rod | 32 | both | BubbleBeam, Focus Energy, Bullet Seed, Water Pulse | as Octillery: Wring Out 36, Signal Beam 42, Ice Beam 48, Hyper Beam 55 | Octillery (from 33) |
| Tentacool | good rod | 32 | Oxide | BubbleBeam, Wrap, Barrier, Water Pulse | Poison Jab 33; as Tentacruel: Poison Jab 36, Screech 42, Hydro Pump 49, Wring Out 55 | Tentacruel (from 33) |
| Tentacool | good rod | 32 | v3 | Toxic Spikes, BubbleBeam, Barrier, Water Pulse | Poison Jab 33; as Tentacruel: Poison Jab 36, Screech 42, Toxic 44, Hydro Pump 49, Wring Out 55 | Tentacruel (from 33) |
| Frogadier | good rod | 34 | Oxide | Faint Attack, Acrobatics, Low Kick, Waterfall | Fling 35; as Greninja: Scald 37, Dark Pulse 40, Extrasensory 43, Sludge Wave 47, Gunk Shot 51, Hydro Pump 55, Hydro Cannon 65 | Greninja (from 36) |
| Frogadier | good rod | 34 | v3 | Icy Wind, Faint Attack, Acrobatics, Low Kick | Fling 35; as Greninja: Water Shuriken on evolving, Night Slash on evolving, Scald 37, Dark Pulse 40, Extrasensory 43, Sludge Wave 47, Gunk Shot 51, Hydro Pump 55, Hydro Cannon 65 | Greninja (from 36) |
| Floatzel | surf | 36 | Oxide | Swift, Aqua Jet, Crunch, Agility | Whirlpool 39, Razor Wind 50 | Floatzel |
| Floatzel | surf | 36 | v3 | Swift, Aqua Jet, Crunch, Agility | Ice Punch 66 | Floatzel |
| Tentacruel | surf | 36 | Oxide | Wrap, Barrier, Water Pulse, Poison Jab | Screech 42, Hydro Pump 49, Wring Out 55 | Tentacruel |
| Tentacruel | surf | 36 | v3 | BubbleBeam, Barrier, Water Pulse, Poison Jab | Screech 42, Toxic 44, Hydro Pump 49, Wring Out 55 | Tentacruel |
| Gastrodon | surf | 39 | Oxide | Water Pulse, Mud Bomb, Hidden Power, Body Slam | Muddy Water 41, Recover 54 | Gastrodon |
| Gastrodon | surf | 39 | v3 | Mud Bomb, Hidden Power, Body Slam, Muddy Water | Earthquake 44, Recover 54, Rock Slide 64 | Gastrodon |
| Mantine | surf | 39 | Oxide | Wing Attack, Water Pulse, Take Down, Confuse Ray | Bounce 40, Aqua Ring 46, Hydro Pump 49 | Mantine |
| Mantine | surf | 39 | v3 | Wing Attack, Water Pulse, Take Down, Confuse Ray | Bounce 40, Aqua Ring 46, Hydro Pump 49, Air Slash 66 | Mantine |
| Floatzel | super rod | 40 | Oxide | Aqua Jet, Crunch, Agility, Whirlpool | Razor Wind 50 | Floatzel |
| Floatzel | super rod | 40 | v3 | Swift, Aqua Jet, Crunch, Agility | Ice Punch 66 | Floatzel |
| Mantine | super rod | 40 | Oxide | Water Pulse, Take Down, Confuse Ray, Bounce | Aqua Ring 46, Hydro Pump 49 | Mantine |
| Mantine | super rod | 40 | v3 | Water Pulse, Take Down, Confuse Ray, Bounce | Aqua Ring 46, Hydro Pump 49, Air Slash 66 | Mantine |
| Frogadier | surf | 42 | Oxide | Low Kick, Waterfall, Fling, Dark Pulse | as Greninja: Extrasensory 43, Sludge Wave 47, Gunk Shot 51, Hydro Pump 55, Hydro Cannon 65 | Greninja (from 43) |
| Frogadier | surf | 42 | v3 | Low Kick, Fling, Waterfall, Dark Pulse | as Greninja: Water Shuriken on evolving, Night Slash on evolving, Extrasensory 43, Sludge Wave 47, Gunk Shot 51, Hydro Pump 55, Hydro Cannon 65 | Greninja (from 43) |
| Gastrodon | super rod | 43 | Oxide | Mud Bomb, Hidden Power, Body Slam, Muddy Water | Recover 54 | Gastrodon |
| Gastrodon | super rod | 43 | v3 | Mud Bomb, Hidden Power, Body Slam, Muddy Water | Earthquake 44, Recover 54, Rock Slide 64 | Gastrodon |
| Wailord | super rod | 43 | Oxide | Rest, Brine, Water Spout, Amnesia | Dive 46, Bounce 54, Hydro Pump 62 | Wailord |
| Wailord | super rod | 43 | v3 | Mist, Rest, Brine, Amnesia | Dive 46, Bounce 54, Hydro Pump 62 | Wailord |
| Toxapex | super rod | 46 | both | Toxic, Venom Drench, Poison Jab, Liquidation | nothing | Toxapex |

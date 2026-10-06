# Barry's split: what each catch knows and learns

Written by `tools/oxide/balance/learncheck.py sheets` for check 6 of the learnset baseline (`docs/oxide/learnset-checks.md`). One table per capture area first offered in Barry's split, whose cap is 71. Each Pokemon is read at the lowest level it is found at there. "Knows at capture" is the last four moves its list gives by that level; "learns by level-up" is every entry it reaches after capture up to 71, evolving on time, with each later stage's moves under its name; "at the cap" is the stage it can be by then and the next one after. A row marked Rewrite shows the learnset rewrite's lists (the tree's) where it differs from the row marked Oxide, Oxide's lists before the learnset rewrite (`da6b92496c`); a row marked both is the same in each. Relearner-only moves and egg moves are left out.

## Pokémon League

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 71 | At the cap |
|---|---|---|---|---|---|---|
| Chinchou | old rod | 20 | Oxide | Flail, Water Gun, Confuse Ray, Spark | Take Down 23; as Lanturn: Stockpile 27, Swallow 27, Spit Up 27, BubbleBeam 30, Signal Beam 35, Discharge 40, Aqua Ring 47, Hydro Pump 52, Charge 57 | Lanturn (from 27) |
| Chinchou | old rod | 20 | Rewrite | Water Gun, Screech, Confuse Ray, Icy Wind | Take Down 23; as Lanturn: Stockpile 27, Swallow 28, Spit Up 29, BubbleBeam 30, Signal Beam 35, Scald 37, Discharge 40, Thunderbolt 42, Aqua Ring 47, Muddy Water 52, Charge 57, Flash Cannon 59, Volt Switch 61, Dazzling Gleam 66, Ice Beam 68 | Lanturn (from 27) |
| Goldeen | old rod | 20 | Oxide | Water Sport, Supersonic, Horn Attack, Water Pulse | Flail 21, Aqua Ring 27, Fury Attack 31; as Seaking: Waterfall 40, Horn Drill 47, Agility 56, Megahorn 63 | Seaking (from 33) |
| Goldeen | old rod | 20 | Rewrite | Water Pulse, Flip Turn, Horn Attack, Agility | Flail 21, Aqua Ring 27; as Seaking: Bulldoze 33, Aqua Jet 35, Waterfall 40, Poison Jab 42, Throat Chop 44, Aqua Tail 50, Drill Peck 52, Agility 56, Megahorn 63 | Seaking (from 33) |
| Barboach | old rod | 21 | Oxide | Water Sport, Water Gun, Mud Bomb, Amnesia | Water Pulse 22, Magnitude 26; as Whiscash: Rest 33, Snore 33, Aqua Tail 39, Earthquake 45, Future Sight 51, Fissure 57 | Whiscash (from 30) |
| Barboach | old rod | 21 | Rewrite | Water Gun, Mud Bomb, Amnesia, Rock Tomb | Water Pulse 22, Magnitude 26; as Whiscash: Bulldoze 30, Rest 33, Zen Headbutt 35, Aqua Tail 39, Wild Charge 42, Earthquake 45, Future Sight 51, Ice Beam 53, Spark 58, Tickle 60, Swagger 66 | Whiscash (from 30) |
| Feebas | old rod | 21 to 22 | Oxide | Splash, Tackle | Flail 30; as Milotic: Hydro Pump 37, Attract 41, Safeguard 45, Aqua Ring 49 | Milotic (from 30) |
| Feebas | old rod | 21 to 22 | Rewrite | Swagger, Dragon Tail, Water Pulse, Tackle | Captivate 25, Flail 30; as Milotic: Twister 30, Recover 31, Aqua Tail 32, Aurora Beam 33, Surf 37, Attract 41, Safeguard 45, Aqua Ring 49, Alluring Voice 51, Dragon Pulse 54, Muddy Water 58, Scald 60, Earth Power 62, Hyper Voice 66, Ice Beam 68 | Milotic (from 30) |
| Barboach | good rod | 32 | Oxide | Water Pulse, Magnitude, Rest, Snore | as Whiscash: Rest 33, Snore 33, Aqua Tail 39, Earthquake 45, Future Sight 51, Fissure 57 | Whiscash (from 33) |
| Barboach | good rod | 32 | Rewrite | Rock Tomb, Water Pulse, Magnitude, Rest | as Whiscash: Rest 33, Zen Headbutt 35, Aqua Tail 39, Wild Charge 42, Earthquake 45, Future Sight 51, Ice Beam 53, Spark 58, Tickle 60, Swagger 66 | Whiscash (from 33) |
| Feebas | good rod | 32 | Oxide | Splash, Tackle, Flail | as Milotic: Hydro Pump 37, Attract 41, Safeguard 45, Aqua Ring 49 | Milotic (from 33) |
| Feebas | good rod | 32 | Rewrite | Water Pulse, Tackle, Captivate, Flail | as Milotic: Aurora Beam 33, Surf 37, Attract 41, Safeguard 45, Aqua Ring 49, Alluring Voice 51, Dragon Pulse 54, Muddy Water 58, Scald 60, Earth Power 62, Hyper Voice 66, Ice Beam 68 | Milotic (from 33) |
| Chinchou | good rod | 34 | Oxide | Take Down, BubbleBeam, Signal Beam, Discharge | as Lanturn: Signal Beam 35, Discharge 40, Aqua Ring 47, Hydro Pump 52, Charge 57 | Lanturn (from 35) |
| Chinchou | good rod | 34 | Rewrite | Take Down, BubbleBeam, Signal Beam, Discharge | as Lanturn: Signal Beam 35, Scald 37, Discharge 40, Thunderbolt 42, Aqua Ring 47, Muddy Water 52, Charge 57, Flash Cannon 59, Volt Switch 61, Dazzling Gleam 66, Ice Beam 68 | Lanturn (from 35) |
| Corphish | good rod | 34 | Oxide | BubbleBeam, Protect, Knock Off, Taunt | Night Slash 35; as Crawdaunt: Night Slash 39, Crabhammer 44, Swords Dance 52, Crunch 57, Guillotine 65 | Crawdaunt (from 35) |
| Corphish | good rod | 34 | Rewrite | Leer, Aerial Ace, Razor Shell, Knock Off | Night Slash 35; as Crawdaunt: Metal Claw 36, Night Slash 39, Throat Chop 41, Crabhammer 44, X-Scissor 46, Swords Dance 52, Crunch 57, Brick Break 59, Close Combat 66 | Crawdaunt (from 35) |
| Greninja | good rod | 36 | Oxide | Acrobatics, Low Kick, Waterfall, Fling | Scald 37, Dark Pulse 40, Extrasensory 43, Sludge Wave 47, Gunk Shot 51, Hydro Pump 55, Hydro Cannon 65 | Greninja |
| Greninja | good rod | 36 | Rewrite | Low Kick, Waterfall, Fling, Shadow Sneak | Scald 37, Dark Pulse 40, Extrasensory 43, Sludge Wave 47, Surf 49, Gunk Shot 51, Ice Beam 56, Muddy Water 58, Hydro Cannon 65, Taunt 67, Throat Chop 69 | Greninja |
| Goldeen | surf | 38 | Oxide | Flail, Aqua Ring, Fury Attack, Waterfall | as Seaking: Waterfall 40, Horn Drill 47, Agility 56, Megahorn 63 | Seaking (from 39) |
| Goldeen | surf | 38 | Rewrite | Agility, Flail, Aqua Ring, Waterfall | as Seaking: Waterfall 40, Poison Jab 42, Throat Chop 44, Aqua Tail 50, Drill Peck 52, Agility 56, Megahorn 63 | Seaking (from 39) |
| Jellicent | surf | 38 | Oxide | Imprison, Confuse Ray, Hex, Brine | Pain Split 39, Destiny Bond 45, Shadow Ball 51, Scald 55, Water Spout 65, Recover 70 | Jellicent |
| Jellicent | surf | 38 | Rewrite | Imprison, Confuse Ray, Hex, Brine | Pain Split 39, Muddy Water 45, Shadow Ball 51, Sludge Bomb 53, Scald 55, Energy Ball 61, Water Spout 65, Recover 70 | Jellicent |
| Buizel | surf | 41 | Oxide | Swift, Aqua Jet, Agility, Whirlpool | as Floatzel: Razor Wind 50 | Floatzel (from 42) |
| Buizel | surf | 41 | Rewrite | Swift, Aqua Jet, Agility, Whirlpool | as Floatzel: Liquidation 43, Low Sweep 45, Rock Tomb 51, Agility 52, Ice Fang 59, Wave Crash 67, Ice Punch 69 | Floatzel (from 42) |
| Floatzel | surf | 41 | Oxide | Aqua Jet, Crunch, Agility, Whirlpool | Razor Wind 50 | Floatzel |
| Floatzel | surf | 41 | Rewrite | Flip Turn, Icy Wind, Waterfall, Whirlpool | Liquidation 43, Low Sweep 45, Rock Tomb 51, Agility 52, Ice Fang 59, Wave Crash 67, Ice Punch 69 | Floatzel |
| Crawdaunt | super rod | 42 | Oxide | Knock Off, Swift, Taunt, Night Slash | Crabhammer 44, Swords Dance 52, Crunch 57, Guillotine 65 | Crawdaunt |
| Crawdaunt | super rod | 42 | Rewrite | Taunt, Metal Claw, Night Slash, Throat Chop | Crabhammer 44, X-Scissor 46, Swords Dance 52, Crunch 57, Brick Break 59, Close Combat 66 | Crawdaunt |
| Milotic | super rod | 42 | Oxide | Captivate, Aqua Tail, Hydro Pump, Attract | Safeguard 45, Aqua Ring 49 | Milotic |
| Milotic | super rod | 42 | Rewrite | Aqua Tail, Aurora Beam, Surf, Attract | Safeguard 45, Aqua Ring 49, Alluring Voice 51, Dragon Pulse 54, Muddy Water 58, Scald 60, Earth Power 62, Hyper Voice 66, Ice Beam 68 | Milotic |
| Greninja | surf | 44 | Oxide | Fling, Scald, Dark Pulse, Extrasensory | Sludge Wave 47, Gunk Shot 51, Hydro Pump 55, Hydro Cannon 65 | Greninja |
| Greninja | surf | 44 | Rewrite | Shadow Sneak, Scald, Dark Pulse, Extrasensory | Sludge Wave 47, Surf 49, Gunk Shot 51, Ice Beam 56, Muddy Water 58, Hydro Cannon 65, Taunt 67, Throat Chop 69 | Greninja |
| Floatzel | super rod | 45 | Oxide | Aqua Jet, Crunch, Agility, Whirlpool | Razor Wind 50 | Floatzel |
| Floatzel | super rod | 45 | Rewrite | Waterfall, Whirlpool, Liquidation, Low Sweep | Rock Tomb 51, Agility 52, Ice Fang 59, Wave Crash 67, Ice Punch 69 | Floatzel |
| Lanturn | super rod | 45 | Oxide | Spit Up, BubbleBeam, Signal Beam, Discharge | Aqua Ring 47, Hydro Pump 52, Charge 57 | Lanturn |
| Lanturn | super rod | 45 | Rewrite | Signal Beam, Scald, Discharge, Thunderbolt | Aqua Ring 47, Muddy Water 52, Charge 57, Flash Cannon 59, Volt Switch 61, Dazzling Gleam 66, Ice Beam 68 | Lanturn |
| Relicanth | super rod | 48 | Oxide | Yawn, Take Down, Mud Sport, AncientPower | Double-Edge 50, Dive 57, Rest 64, Hydro Pump 71 | Relicanth |
| Relicanth | super rod | 48 | Rewrite | Yawn, Take Down, AncientPower, Bulldoze | Double-Edge 50, Aqua Tail 54, Dive 57, Rock Slide 59, Earthquake 62, Rest 64, Muddy Water 71 | Relicanth |

## Route 223

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 71 | At the cap |
|---|---|---|---|---|---|---|
| Chinchou | old rod | 20 | Oxide | Flail, Water Gun, Confuse Ray, Spark | Take Down 23; as Lanturn: Stockpile 27, Swallow 27, Spit Up 27, BubbleBeam 30, Signal Beam 35, Discharge 40, Aqua Ring 47, Hydro Pump 52, Charge 57 | Lanturn (from 27) |
| Chinchou | old rod | 20 | Rewrite | Water Gun, Screech, Confuse Ray, Icy Wind | Take Down 23; as Lanturn: Stockpile 27, Swallow 28, Spit Up 29, BubbleBeam 30, Signal Beam 35, Scald 37, Discharge 40, Thunderbolt 42, Aqua Ring 47, Muddy Water 52, Charge 57, Flash Cannon 59, Volt Switch 61, Dazzling Gleam 66, Ice Beam 68 | Lanturn (from 27) |
| Mantyke | old rod | 20 | Oxide | Supersonic, BubbleBeam, Headbutt, Agility | Wing Attack 22, Water Pulse 28; as Mantine: Take Down 31, Confuse Ray 37, Bounce 40, Aqua Ring 46, Hydro Pump 49 | Mantine (from 30) |
| Mantyke | old rod | 20 | Rewrite | Icy Wind, BubbleBeam, Headbutt, Agility | Wing Attack 22, Water Pulse 28; as Mantine: Take Down 31, Scald 34, Confuse Ray 37, Bounce 40, Signal Beam 42, Aqua Ring 46, Surf 50, Air Slash 52, Ice Beam 58, Psychic 60, Swagger 66, Muddy Water 68 | Mantine (from 30) |
| Finneon | old rod | 21 | Oxide | Pound, Water Gun, Attract, Gust | Water Pulse 22, Captivate 26, Safeguard 29; as Lumineon: Aqua Ring 35, Whirlpool 42, U-turn 48, Bounce 53, Silver Wind 59 | Lumineon (from 31) |
| Finneon | old rod | 21 | Rewrite | Gust, Attract, Icy Wind, Ominous Wind | Captivate 26, Safeguard 29; as Lumineon: Flip Turn 31, Aqua Ring 35, Aqua Tail 37, Whirlpool 42, U-turn 48, Ice Fang 50, Bounce 53, Air Slash 55, Silver Wind 59, Confuse Ray 61, Acrobatics 66 | Lumineon (from 31) |
| Shellos | old rod | 21 | Oxide | Harden, Water Pulse, Mud Bomb, Hidden Power | Body Slam 29; as Gastrodon: Muddy Water 41, Recover 54 | Gastrodon (from 30) |
| Shellos | old rod | 21 | Rewrite | Swagger, Water Pulse, Mud Bomb, Hidden Power | Body Slam 29; as Gastrodon: AncientPower 31, Clear Smog 34, Muddy Water 41, Earth Power 43, Bulldoze 45, Ice Beam 50, Recover 54, Sludge Bomb 58, Skitter Smack 60, Block 66, Rock Tomb 68 | Gastrodon (from 30) |
| Frogadier | old rod | 22 | Oxide | Water Pulse, Icy Wind, Faint Attack, Acrobatics | Low Kick 25, Waterfall 30, Fling 35; as Greninja: Scald 37, Dark Pulse 40, Extrasensory 43, Sludge Wave 47, Gunk Shot 51, Hydro Pump 55, Hydro Cannon 65 | Greninja (from 36) |
| Frogadier | old rod | 22 | Rewrite | Icy Wind, Thief, Faint Attack, Acrobatics | Low Kick 25, Waterfall 30, Fling 35; as Greninja: Shadow Sneak 36, Scald 37, Dark Pulse 40, Extrasensory 43, Sludge Wave 47, Surf 49, Gunk Shot 51, Ice Beam 56, Muddy Water 58, Hydro Cannon 65, Taunt 67, Throat Chop 69 | Greninja (from 36) |
| Gorebyss | good rod | 32 | Oxide | Water Pulse, Amnesia, Aqua Ring, Captivate | Baton Pass 33, Dive 37, Psychic 42, Aqua Tail 46, Hydro Pump 51 | Gorebyss |
| Gorebyss | good rod | 32 | Rewrite | Water Pulse, Amnesia, Aqua Ring, Captivate | Baton Pass 33, Draining Kiss 35, Dive 37, Muddy Water 40, Psychic 42, Aqua Tail 46, Shadow Ball 48, Giga Drain 50, Scald 56, Shell Smash 64 | Gorebyss |
| Tentacool | good rod | 32 | Oxide | BubbleBeam, Wrap, Barrier, Water Pulse | Poison Jab 33; as Tentacruel: Poison Jab 36, Screech 42, Hydro Pump 49, Wring Out 55 | Tentacruel (from 33) |
| Tentacool | good rod | 32 | Rewrite | Toxic Spikes, Icy Wind, BubbleBeam, Barrier | Poison Jab 33; as Tentacruel: Poison Jab 36, Surf 40, Screech 42, Psybeam 44, Sludge Bomb 50, Sludge Wave 52, Muddy Water 58, Power Gem 60, Ice Beam 66, Throat Chop 68 | Tentacruel (from 33) |
| Mareanie | good rod | 34 | Oxide | Toxic Spikes, Recover, Spike Cannon, Pin Missile | Toxic 36; as Toxapex: Toxic 39, Venom Drench 42, Poison Jab 43, Liquidation 45 | Toxapex (from 38) |
| Mareanie | good rod | 34 | Rewrite | Toxic Spikes, Recover, Spike Cannon, Pin Missile | Liquidation 35, Toxic 36; as Toxapex: Toxic 39, Venom Drench 42, Poison Jab 43, Liquidation 45, Lunge 48, Sludge Bomb 50, Ice Beam 56, Iron Defense 64 | Toxapex (from 38) |
| Octillery | good rod | 34 | Oxide | BubbleBeam, Focus Energy, Octazooka, Bullet Seed | Wring Out 36, Signal Beam 42, Ice Beam 48, Hyper Beam 55 | Octillery |
| Octillery | good rod | 34 | Rewrite | Octazooka, Round, Bullet Seed, Mud Shot | Scald 35, Signal Beam 42, Seed Bomb 44, Ice Beam 48, Skitter Smack 51, Hyper Beam 55, Energy Ball 59, Psychic 61 | Octillery |
| Wailmer | good rod | 36 | Oxide | Mist, Rest, Brine, Water Spout | Amnesia 37; as Wailord: Dive 46, Bounce 54, Hydro Pump 62 | Wailord (from 40) |
| Wailmer | good rod | 36 | Rewrite | Mist, Rest, Brine, Water Spout | Amnesia 37; as Wailord: Dive 46, Rock Tomb 48, Iron Head 50, Bounce 54, Zen Headbutt 56, Body Press 58, Surf 62, Earthquake 64 | Wailord (from 40) |
| Mantyke | surf | 38 | Oxide | Wing Attack, Water Pulse, Take Down, Confuse Ray | as Mantine: Bounce 40, Aqua Ring 46, Hydro Pump 49 | Mantine (from 39) |
| Mantyke | surf | 38 | Rewrite | Wing Attack, Water Pulse, Take Down, Confuse Ray | as Mantine: Bounce 40, Signal Beam 42, Aqua Ring 46, Surf 50, Air Slash 52, Ice Beam 58, Psychic 60, Swagger 66, Muddy Water 68 | Mantine (from 39) |
| Tentacruel | surf | 38 | Oxide | Wrap, Barrier, Water Pulse, Poison Jab | Screech 42, Hydro Pump 49, Wring Out 55 | Tentacruel |
| Tentacruel | surf | 38 | Rewrite | BubbleBeam, Barrier, Water Pulse, Poison Jab | Surf 40, Screech 42, Psybeam 44, Sludge Bomb 50, Sludge Wave 52, Muddy Water 58, Power Gem 60, Ice Beam 66, Throat Chop 68 | Tentacruel |
| Kingdra | surf | 41 | Oxide | Agility, Twister, Brine, Hydro Pump | Dragon Dance 48, Dragon Pulse 57 | Kingdra |
| Kingdra | surf | 41 | Rewrite | Twister, Brine, Aurora Beam, Octazooka | Scald 54, Dragon Pulse 57, Wave Crash 59, Iron Head 65, Draco Meteor 67 | Kingdra |
| Mantine | surf | 41 | Oxide | Water Pulse, Take Down, Confuse Ray, Bounce | Aqua Ring 46, Hydro Pump 49 | Mantine |
| Mantine | surf | 41 | Rewrite | Take Down, Scald, Confuse Ray, Bounce | Signal Beam 42, Aqua Ring 46, Surf 50, Air Slash 52, Ice Beam 58, Psychic 60, Swagger 66, Muddy Water 68 | Mantine |
| Floatzel | super rod | 42 | Oxide | Aqua Jet, Crunch, Agility, Whirlpool | Razor Wind 50 | Floatzel |
| Floatzel | super rod | 42 | Rewrite | Flip Turn, Icy Wind, Waterfall, Whirlpool | Liquidation 43, Low Sweep 45, Rock Tomb 51, Agility 52, Ice Fang 59, Wave Crash 67, Ice Punch 69 | Floatzel |
| Gastrodon | super rod | 42 | Oxide | Mud Bomb, Hidden Power, Body Slam, Muddy Water | Recover 54 | Gastrodon |
| Gastrodon | super rod | 42 | Rewrite | Body Slam, AncientPower, Clear Smog, Muddy Water | Earth Power 43, Bulldoze 45, Ice Beam 50, Recover 54, Sludge Bomb 58, Skitter Smack 60, Block 66, Rock Tomb 68 | Gastrodon |
| Toxapex | surf | 44 | Oxide | Pin Missile, Toxic, Venom Drench, Poison Jab | Liquidation 45 | Toxapex |
| Toxapex | surf | 44 | Rewrite | Pin Missile, Toxic, Venom Drench, Poison Jab | Liquidation 45, Lunge 48, Sludge Bomb 50, Ice Beam 56, Iron Defense 64 | Toxapex |
| Jellicent | super rod | 45 | Oxide | Hex, Brine, Pain Split, Destiny Bond | Shadow Ball 51, Scald 55, Water Spout 65, Recover 70 | Jellicent |
| Jellicent | super rod | 45 | Rewrite | Hex, Brine, Pain Split, Muddy Water | Shadow Ball 51, Sludge Bomb 53, Scald 55, Energy Ball 61, Water Spout 65, Recover 70 | Jellicent |
| Lanturn | super rod | 45 to 48 | Oxide | Spit Up, BubbleBeam, Signal Beam, Discharge | Aqua Ring 47, Hydro Pump 52, Charge 57 | Lanturn |
| Lanturn | super rod | 45 to 48 | Rewrite | Signal Beam, Scald, Discharge, Thunderbolt | Aqua Ring 47, Muddy Water 52, Charge 57, Flash Cannon 59, Volt Switch 61, Dazzling Gleam 66, Ice Beam 68 | Lanturn |

## Sendoff Spring

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 71 | At the cap |
|---|---|---|---|---|---|---|
| Barboach | old rod | 22 | Oxide | Water Gun, Mud Bomb, Amnesia, Water Pulse | Magnitude 26; as Whiscash: Rest 33, Snore 33, Aqua Tail 39, Earthquake 45, Future Sight 51, Fissure 57 | Whiscash (from 30) |
| Barboach | old rod | 22 | Rewrite | Mud Bomb, Amnesia, Rock Tomb, Water Pulse | Magnitude 26; as Whiscash: Bulldoze 30, Rest 33, Zen Headbutt 35, Aqua Tail 39, Wild Charge 42, Earthquake 45, Future Sight 51, Ice Beam 53, Spark 58, Tickle 60, Swagger 66 | Whiscash (from 30) |
| Goldeen | old rod | 22 | Oxide | Supersonic, Horn Attack, Water Pulse, Flail | Aqua Ring 27, Fury Attack 31; as Seaking: Waterfall 40, Horn Drill 47, Agility 56, Megahorn 63 | Seaking (from 33) |
| Goldeen | old rod | 22 | Rewrite | Flip Turn, Horn Attack, Agility, Flail | Aqua Ring 27; as Seaking: Bulldoze 33, Aqua Jet 35, Waterfall 40, Poison Jab 42, Throat Chop 44, Aqua Tail 50, Drill Peck 52, Agility 56, Megahorn 63 | Seaking (from 33) |
| Corphish | old rod | 24 | Oxide | ViceGrip, Leer, BubbleBeam, Protect | Knock Off 26; as Crawdaunt: Swift 30, Taunt 34, Night Slash 39, Crabhammer 44, Swords Dance 52, Crunch 57, Guillotine 65 | Crawdaunt (from 30) |
| Corphish | old rod | 24 | Rewrite | ViceGrip, Leer, Aerial Ace, Razor Shell | Knock Off 26; as Crawdaunt: Swift 30, Taunt 34, Metal Claw 36, Night Slash 39, Throat Chop 41, Crabhammer 44, X-Scissor 46, Swords Dance 52, Crunch 57, Brick Break 59, Close Combat 66 | Crawdaunt (from 30) |
| Feebas | old rod | 24 | Oxide | Splash, Tackle | Flail 30; as Milotic: Hydro Pump 37, Attract 41, Safeguard 45, Aqua Ring 49 | Milotic (from 30) |
| Feebas | old rod | 24 | Rewrite | Swagger, Dragon Tail, Water Pulse, Tackle | Captivate 25, Flail 30; as Milotic: Twister 30, Recover 31, Aqua Tail 32, Aurora Beam 33, Surf 37, Attract 41, Safeguard 45, Aqua Ring 49, Alluring Voice 51, Dragon Pulse 54, Muddy Water 58, Scald 60, Earth Power 62, Hyper Voice 66, Ice Beam 68 | Milotic (from 30) |
| Frogadier | old rod | 26 | Oxide | Icy Wind, Faint Attack, Acrobatics, Low Kick | Waterfall 30, Fling 35; as Greninja: Scald 37, Dark Pulse 40, Extrasensory 43, Sludge Wave 47, Gunk Shot 51, Hydro Pump 55, Hydro Cannon 65 | Greninja (from 36) |
| Frogadier | old rod | 26 | Rewrite | Thief, Faint Attack, Acrobatics, Low Kick | Waterfall 30, Fling 35; as Greninja: Shadow Sneak 36, Scald 37, Dark Pulse 40, Extrasensory 43, Sludge Wave 47, Surf 49, Gunk Shot 51, Ice Beam 56, Muddy Water 58, Hydro Cannon 65, Taunt 67, Throat Chop 69 | Greninja (from 36) |
| Feebas | good rod | 35 | Oxide | Splash, Tackle, Flail | as Milotic: Hydro Pump 37, Attract 41, Safeguard 45, Aqua Ring 49 | Milotic (from 36) |
| Feebas | good rod | 35 | Rewrite | Water Pulse, Tackle, Captivate, Flail | as Milotic: Surf 37, Attract 41, Safeguard 45, Aqua Ring 49, Alluring Voice 51, Dragon Pulse 54, Muddy Water 58, Scald 60, Earth Power 62, Hyper Voice 66, Ice Beam 68 | Milotic (from 36) |
| Frillish | good rod | 35 | Oxide | Imprison, Confuse Ray, Hex, Brine | Pain Split 39; as Jellicent: Destiny Bond 45, Shadow Ball 51, Scald 55, Water Spout 65, Recover 70 | Jellicent (from 40) |
| Frillish | good rod | 35 | Rewrite | Imprison, Confuse Ray, Hex, Brine | Dark Pulse 36, Pain Split 39; as Jellicent: Muddy Water 45, Shadow Ball 51, Sludge Bomb 53, Scald 55, Energy Ball 61, Water Spout 65, Recover 70 | Jellicent (from 40) |
| Chinchou | good rod | 37 | Oxide | Take Down, BubbleBeam, Signal Beam, Discharge | as Lanturn: Discharge 40, Aqua Ring 47, Hydro Pump 52, Charge 57 | Lanturn (from 38) |
| Chinchou | good rod | 37 | Rewrite | Take Down, BubbleBeam, Signal Beam, Discharge | as Lanturn: Discharge 40, Thunderbolt 42, Aqua Ring 47, Muddy Water 52, Charge 57, Flash Cannon 59, Volt Switch 61, Dazzling Gleam 66, Ice Beam 68 | Lanturn (from 38) |
| Corphish | good rod | 37 | Oxide | Protect, Knock Off, Taunt, Night Slash | Crabhammer 38; as Crawdaunt: Night Slash 39, Crabhammer 44, Swords Dance 52, Crunch 57, Guillotine 65 | Crawdaunt (from 38) |
| Corphish | good rod | 37 | Rewrite | Aerial Ace, Razor Shell, Knock Off, Night Slash | Crabhammer 38; as Crawdaunt: Night Slash 39, Throat Chop 41, Crabhammer 44, X-Scissor 46, Swords Dance 52, Crunch 57, Brick Break 59, Close Combat 66 | Crawdaunt (from 38) |
| Greninja | good rod | 39 | Oxide | Low Kick, Waterfall, Fling, Scald | Dark Pulse 40, Extrasensory 43, Sludge Wave 47, Gunk Shot 51, Hydro Pump 55, Hydro Cannon 65 | Greninja |
| Greninja | good rod | 39 | Rewrite | Waterfall, Fling, Shadow Sneak, Scald | Dark Pulse 40, Extrasensory 43, Sludge Wave 47, Surf 49, Gunk Shot 51, Ice Beam 56, Muddy Water 58, Hydro Cannon 65, Taunt 67, Throat Chop 69 | Greninja |
| Frillish | surf | 40 | Oxide | Confuse Ray, Hex, Brine, Pain Split | as Jellicent: Destiny Bond 45, Shadow Ball 51, Scald 55, Water Spout 65, Recover 70 | Jellicent (from 41) |
| Frillish | surf | 40 | Rewrite | Hex, Brine, Dark Pulse, Pain Split | as Jellicent: Muddy Water 45, Shadow Ball 51, Sludge Bomb 53, Scald 55, Energy Ball 61, Water Spout 65, Recover 70 | Jellicent (from 41) |
| Jellicent | surf | 40 | Oxide | Confuse Ray, Hex, Brine, Pain Split | Destiny Bond 45, Shadow Ball 51, Scald 55, Water Spout 65, Recover 70 | Jellicent |
| Jellicent | surf | 40 | Rewrite | Confuse Ray, Hex, Brine, Pain Split | Muddy Water 45, Shadow Ball 51, Sludge Bomb 53, Scald 55, Energy Ball 61, Water Spout 65, Recover 70 | Jellicent |
| Buizel | surf | 43 | Oxide | Swift, Aqua Jet, Agility, Whirlpool | as Floatzel: Razor Wind 50 | Floatzel (from 44) |
| Buizel | surf | 43 | Rewrite | Swift, Aqua Jet, Agility, Whirlpool | as Floatzel: Low Sweep 45, Rock Tomb 51, Agility 52, Ice Fang 59, Wave Crash 67, Ice Punch 69 | Floatzel (from 44) |
| Floatzel | surf | 43 | Oxide | Aqua Jet, Crunch, Agility, Whirlpool | Razor Wind 50 | Floatzel |
| Floatzel | surf | 43 | Rewrite | Icy Wind, Waterfall, Whirlpool, Liquidation | Low Sweep 45, Rock Tomb 51, Agility 52, Ice Fang 59, Wave Crash 67, Ice Punch 69 | Floatzel |
| Crawdaunt | super rod | 45 | Oxide | Swift, Taunt, Night Slash, Crabhammer | Swords Dance 52, Crunch 57, Guillotine 65 | Crawdaunt |
| Crawdaunt | super rod | 45 | Rewrite | Metal Claw, Night Slash, Throat Chop, Crabhammer | X-Scissor 46, Swords Dance 52, Crunch 57, Brick Break 59, Close Combat 66 | Crawdaunt |
| Lanturn | super rod | 45 | Oxide | Spit Up, BubbleBeam, Signal Beam, Discharge | Aqua Ring 47, Hydro Pump 52, Charge 57 | Lanturn |
| Lanturn | super rod | 45 | Rewrite | Signal Beam, Scald, Discharge, Thunderbolt | Aqua Ring 47, Muddy Water 52, Charge 57, Flash Cannon 59, Volt Switch 61, Dazzling Gleam 66, Ice Beam 68 | Lanturn |
| Feraligatr | surf | 46 | Oxide | Agility, Crunch, Slash, Screech | Thrash 50, Aqua Tail 58, Superpower 63, Hydro Pump 71 | Feraligatr |
| Feraligatr | surf | 46 | Rewrite | Bulldoze, Slash, Brick Break, Screech | Aqua Tail 50, Superpower 63, Thrash 66, Earthquake 68, Muddy Water 71 | Feraligatr |
| Jellicent | super rod | 48 to 51 | Oxide | Hex, Brine, Pain Split, Destiny Bond | Shadow Ball 51, Scald 55, Water Spout 65, Recover 70 | Jellicent |
| Jellicent | super rod | 48 to 51 | Rewrite | Hex, Brine, Pain Split, Muddy Water | Shadow Ball 51, Sludge Bomb 53, Scald 55, Energy Ball 61, Water Spout 65, Recover 70 | Jellicent |
| Ludicolo | super rod | 48 | Oxide | Astonish, Growl, Mega Drain, Nature Power | nothing | Ludicolo |
| Ludicolo | super rod | 48 | Rewrite | Mega Drain, Nature Power, Energy Ball, Mud Shot | Muddy Water 54, Giga Drain 56, Psychic 58, Leaf Storm 62, Ice Beam 64, Leech Seed 70 | Ludicolo |
| Donphan | wild | 50 | Oxide | Fury Attack, Assurance, Scary Face, Earthquake | Giga Impact 54 | Donphan |
| Donphan | wild | 50 | Rewrite | Scary Face, Knock Off, Seed Bomb, Earthquake | Throat Chop 51, Giga Impact 54, Charm 56, Ice Fang 59, Block 67 | Donphan |
| Absol | wild | 51 to 52 | Oxide | Slash, Future Sight, Sucker Punch, Detect | Night Slash 52, Me First 57, Psycho Cut 60, Perish Song 65 | Absol |
| Absol | wild | 51 to 52 | Rewrite | Slash, Future Sight, Sucker Punch, X-Scissor | Night Slash 52, Throat Chop 54, Psycho Cut 60, Shadow Ball 62, Perish Song 65, Superpower 69, Rock Slide 71 | Absol |
| Beautifly | wild | 51 | Oxide | Attract, Silver Wind, Giga Drain, Bug Buzz | nothing | Beautifly |
| Beautifly | wild | 51 | Rewrite | Bug Buzz, Flash Cannon, Psychic, Energy Ball | Shadow Ball 57, Quiver Dance 59, Swagger 65 | Beautifly |
| Crustle | wild | 51 to 52 | Oxide | Rock Slide, StompingTantrum, Knock Off, Leech Life | Stone Edge 54, Rock Wrecker 61 | Crustle |
| Crustle | wild | 51 to 52 | Rewrite | StompingTantrum, Knock Off, Leech Life, Body Press | Shell Smash 56, Skitter Smack 58, Rock Wrecker 61, Earthquake 64, Poison Jab 66 | Crustle |
| Dhelmise | wild | 51 | Oxide | Anchor Shot, Shadow Claw, Grassy Glide, Giga Drain | Heavy Slam 55, Phantom Force 65, Power Whip 70 | Dhelmise |
| Dhelmise | wild | 51 | Rewrite | Synthesis, Bulldoze, Grassy Glide, Giga Drain | Heavy Slam 55, Liquidation 57, Petal Blizzard 59, Phantom Force 65, Poltergeist 67, Slam 69 | Dhelmise |
| Glimmora | wild | 51 | Oxide | Rock Slide, Power Gem, Acid Armor, Sludge Wave | nothing | Glimmora |
| Glimmora | wild | 51 | Rewrite | Sludge Bomb, Acid Armor, Flash Cannon, Sludge Wave | Energy Ball 56, Dazzling Gleam 58, Earth Power 64, Toxic Spikes 66 | Glimmora |
| Heracross | wild | 51 to 53 | Oxide | Take Down, Close Combat, Reversal, Feint | Megahorn 55 | Heracross |
| Heracross | wild | 51 to 53 | Rewrite | Close Combat, Reversal, Throat Chop, Lunge | Megahorn 55, Bulldoze 59, Earthquake 67 | Heracross |
| Weavile | wild | 51 to 52 | Oxide | Night Slash, Fling, Metal Claw, Dark Pulse | nothing | Weavile |
| Weavile | wild | 51 to 52 | Rewrite | Night Slash, Fling, Metal Claw, Dark Pulse | X-Scissor 61, Icicle Crash 69, Low Sweep 71 | Weavile |
| Grapploct | wild | 52 | Oxide | Taunt, Reversal, Superpower, Topsy-Turvy | nothing | Grapploct |
| Grapploct | wild | 52 | Rewrite | Taunt, Reversal, Superpower, Drain Punch | Sucker Punch 53, Waterfall 55, Close Combat 61, Ice Punch 63, Liquidation 69 | Grapploct |
| Kricketune | wild | 53 | Oxide | Taunt, Night Slash, Bug Buzz, Perish Song | nothing | Kricketune |
| Kricketune | wild | 53 | Rewrite | Night Slash, Bug Buzz, Perish Song, Lunge | Throat Chop 57, Brick Break 59, Bulldoze 61, Take Down 65, Secret Power 67 | Kricketune |
| Pawmot | wild | 53 | Oxide | Super Fang, Entrainment, Wild Charge, Close Combat | Mach Punch 55, Double Shock 61 | Pawmot |
| Pawmot | wild | 53 | Rewrite | Body Press, Entrainment, Wild Charge, Close Combat | Mach Punch 55, Rock Tomb 57, Double Shock 61, Knock Off 63, Low Sweep 65, Fire Punch 70 | Pawmot |

## Turnback Cave

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 71 | At the cap |
|---|---|---|---|---|---|---|
| Giratina | static battle | 47 | Oxide | Ominous Wind, AncientPower, Dragon Claw, Shadow Force | Heal Block 50, Earth Power 60, Slash 70 | Giratina |
| Giratina | static battle | 47 | Rewrite | Ominous Wind, AncientPower, Dragon Claw, Shadow Force | Heal Block 50, Earth Power 60, Scary Face 62, Poltergeist 66, Slash 70 | Giratina |

## Victory Road

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 71 | At the cap |
|---|---|---|---|---|---|---|
| Chinchou | old rod | 20 | Oxide | Flail, Water Gun, Confuse Ray, Spark | Take Down 23; as Lanturn: Stockpile 27, Swallow 27, Spit Up 27, BubbleBeam 30, Signal Beam 35, Discharge 40, Aqua Ring 47, Hydro Pump 52, Charge 57 | Lanturn (from 27) |
| Chinchou | old rod | 20 | Rewrite | Water Gun, Screech, Confuse Ray, Icy Wind | Take Down 23; as Lanturn: Stockpile 27, Swallow 28, Spit Up 29, BubbleBeam 30, Signal Beam 35, Scald 37, Discharge 40, Thunderbolt 42, Aqua Ring 47, Muddy Water 52, Charge 57, Flash Cannon 59, Volt Switch 61, Dazzling Gleam 66, Ice Beam 68 | Lanturn (from 27) |
| Corphish | old rod | 20 | Oxide | Harden, ViceGrip, Leer, BubbleBeam | Protect 23, Knock Off 26; as Crawdaunt: Swift 30, Taunt 34, Night Slash 39, Crabhammer 44, Swords Dance 52, Crunch 57, Guillotine 65 | Crawdaunt (from 30) |
| Corphish | old rod | 20 | Rewrite | ViceGrip, Leer, Aerial Ace, Razor Shell | Knock Off 26; as Crawdaunt: Swift 30, Taunt 34, Metal Claw 36, Night Slash 39, Throat Chop 41, Crabhammer 44, X-Scissor 46, Swords Dance 52, Crunch 57, Brick Break 59, Close Combat 66 | Crawdaunt (from 30) |
| Finneon | old rod | 21 | Oxide | Pound, Water Gun, Attract, Gust | Water Pulse 22, Captivate 26, Safeguard 29; as Lumineon: Aqua Ring 35, Whirlpool 42, U-turn 48, Bounce 53, Silver Wind 59 | Lumineon (from 31) |
| Finneon | old rod | 21 | Rewrite | Gust, Attract, Icy Wind, Ominous Wind | Captivate 26, Safeguard 29; as Lumineon: Flip Turn 31, Aqua Ring 35, Aqua Tail 37, Whirlpool 42, U-turn 48, Ice Fang 50, Bounce 53, Air Slash 55, Silver Wind 59, Confuse Ray 61, Acrobatics 66 | Lumineon (from 31) |
| Goldeen | old rod | 21 to 22 | Oxide | Supersonic, Horn Attack, Water Pulse, Flail | Aqua Ring 27, Fury Attack 31; as Seaking: Waterfall 40, Horn Drill 47, Agility 56, Megahorn 63 | Seaking (from 33) |
| Goldeen | old rod | 21 to 22 | Rewrite | Flip Turn, Horn Attack, Agility, Flail | Aqua Ring 27; as Seaking: Bulldoze 33, Aqua Jet 35, Waterfall 40, Poison Jab 42, Throat Chop 44, Aqua Tail 50, Drill Peck 52, Agility 56, Megahorn 63 | Seaking (from 33) |
| Goldeen | good rod | 32 | Oxide | Water Pulse, Flail, Aqua Ring, Fury Attack | as Seaking: Waterfall 40, Horn Drill 47, Agility 56, Megahorn 63 | Seaking (from 33) |
| Goldeen | good rod | 32 | Rewrite | Horn Attack, Agility, Flail, Aqua Ring | as Seaking: Bulldoze 33, Aqua Jet 35, Waterfall 40, Poison Jab 42, Throat Chop 44, Aqua Tail 50, Drill Peck 52, Agility 56, Megahorn 63 | Seaking (from 33) |
| Lumineon | good rod | 32 | Oxide | Gust, Water Pulse, Captivate, Safeguard | Aqua Ring 35, Whirlpool 42, U-turn 48, Bounce 53, Silver Wind 59 | Lumineon |
| Lumineon | good rod | 32 | Rewrite | Water Pulse, Captivate, Safeguard, Flip Turn | Aqua Ring 35, Aqua Tail 37, Whirlpool 42, U-turn 48, Ice Fang 50, Bounce 53, Air Slash 55, Silver Wind 59, Confuse Ray 61, Acrobatics 66 | Lumineon |
| Barboach | good rod | 34 | Oxide | Water Pulse, Magnitude, Rest, Snore | Aqua Tail 35; as Whiscash: Aqua Tail 39, Earthquake 45, Future Sight 51, Fissure 57 | Whiscash (from 35) |
| Barboach | good rod | 34 | Rewrite | Rock Tomb, Water Pulse, Magnitude, Rest | Aqua Tail 35; as Whiscash: Zen Headbutt 35, Aqua Tail 39, Wild Charge 42, Earthquake 45, Future Sight 51, Ice Beam 53, Spark 58, Tickle 60, Swagger 66 | Whiscash (from 35) |
| Feebas | good rod | 34 to 36 | Oxide | Splash, Tackle, Flail | as Milotic: Hydro Pump 37, Attract 41, Safeguard 45, Aqua Ring 49 | Milotic (from 35) |
| Feebas | good rod | 34 to 36 | Rewrite | Water Pulse, Tackle, Captivate, Flail | as Milotic: Surf 37, Attract 41, Safeguard 45, Aqua Ring 49, Alluring Voice 51, Dragon Pulse 54, Muddy Water 58, Scald 60, Earth Power 62, Hyper Voice 66, Ice Beam 68 | Milotic (from 35) |
| Corphish | surf | 38 | Oxide | Knock Off, Taunt, Night Slash, Crabhammer | as Crawdaunt: Night Slash 39, Crabhammer 44, Swords Dance 52, Crunch 57, Guillotine 65 | Crawdaunt (from 39) |
| Corphish | surf | 38 | Rewrite | Razor Shell, Knock Off, Night Slash, Crabhammer | as Crawdaunt: Night Slash 39, Throat Chop 41, Crabhammer 44, X-Scissor 46, Swords Dance 52, Crunch 57, Brick Break 59, Close Combat 66 | Crawdaunt (from 39) |
| Gastrodon | surf | 38 | Oxide | Water Pulse, Mud Bomb, Hidden Power, Body Slam | Muddy Water 41, Recover 54 | Gastrodon |
| Gastrodon | surf | 38 | Rewrite | Hidden Power, Body Slam, AncientPower, Clear Smog | Muddy Water 41, Earth Power 43, Bulldoze 45, Ice Beam 50, Recover 54, Sludge Bomb 58, Skitter Smack 60, Block 66, Rock Tomb 68 | Gastrodon |
| Rhyperior | wild | 40 to 43 | Oxide | Scary Face, Rock Blast, Take Down, Horn Drill | Hammer Arm 42, Stone Edge 45, Earthquake 49, Megahorn 57, Rock Wrecker 61 | Rhyperior |
| Rhyperior | wild | 40 to 43 | Rewrite | Stomp, Scary Face, Rock Blast, Take Down | Hammer Arm 42, Rock Slide 45, Earthquake 49, Megahorn 57, Rock Wrecker 61, Crunch 63, Dragon Rush 65, Superpower 69 | Rhyperior |
| Absol | wild | 41 to 44 | Oxide | Bite, Double Team, Slash, Future Sight | Sucker Punch 44, Detect 49, Night Slash 52, Me First 57, Psycho Cut 60, Perish Song 65 | Absol |
| Absol | wild | 41 to 44 | Rewrite | Swords Dance, Bite, Slash, Future Sight | Sucker Punch 44, X-Scissor 46, Night Slash 52, Throat Chop 54, Psycho Cut 60, Shadow Ball 62, Perish Song 65, Superpower 69, Rock Slide 71 | Absol |
| Crustle | wild | 41 | Oxide | Night Slash, X-Scissor, Rock Slide, StompingTantrum | Knock Off 45, Leech Life 48, Stone Edge 54, Rock Wrecker 61 | Crustle |
| Crustle | wild | 41 | Rewrite | Night Slash, X-Scissor, Rock Slide, StompingTantrum | Knock Off 45, Leech Life 48, Body Press 50, Shell Smash 56, Skitter Smack 58, Rock Wrecker 61, Earthquake 64, Poison Jab 66 | Crustle |
| Goldeen | surf | 41 | Oxide | Aqua Ring, Fury Attack, Waterfall, Horn Drill | as Seaking: Horn Drill 47, Agility 56, Megahorn 63 | Seaking (from 42) |
| Goldeen | surf | 41 | Rewrite | Agility, Flail, Aqua Ring, Waterfall | as Seaking: Poison Jab 42, Throat Chop 44, Aqua Tail 50, Drill Peck 52, Agility 56, Megahorn 63 | Seaking (from 42) |
| Golem | wild | 41 | Oxide | Rollout, Rock Blast, Earthquake, Explosion | Double-Edge 44, Stone Edge 49 | Golem |
| Golem | wild | 41 | Rewrite | Magnitude, Rollout, Rock Blast, Earthquake | Double-Edge 44, Sucker Punch 46, Rock Slide 49, Body Slam 53, Body Press 55, Fire Punch 61, Hammer Arm 63, Superpower 69 | Golem |
| Hariyama | wild | 41 to 42 | Oxide | SmellingSalt, Belly Drum, Force Palm, Seismic Toss | Wake-Up Slap 42, Endure 47, Close Combat 52, Reversal 57 | Hariyama |
| Hariyama | wild | 41 to 42 | Rewrite | Low Sweep, Force Palm, Bulldoze, Seismic Toss | Wake-Up Slap 42, Rock Tomb 44, Endure 47, Close Combat 52, Reversal 57, Drain Punch 59, Throat Chop 61, Headlong Rush 67, Iron Head 69 | Hariyama |
| Hawlucha | wild | 41 to 42 | Oxide | Submission, Tailwind, Dual Wingbeat, Fly | Hi Jump Kick 42, Me First 48, Acrobatics 55, Close Combat 60 | Hawlucha |
| Hawlucha | wild | 41 to 42 | Rewrite | Brick Break, Tailwind, Dual Wingbeat, Fly | Hi Jump Kick 42, Lunge 45, Air Slash 47, Acrobatics 55, Close Combat 60, Throat Chop 62, Low Sweep 64, Fire Punch 70 | Hawlucha |
| Jellicent | surf | 41 to 44 | Oxide | Confuse Ray, Hex, Brine, Pain Split | Destiny Bond 45, Shadow Ball 51, Scald 55, Water Spout 65, Recover 70 | Jellicent |
| Jellicent | surf | 41 to 44 | Rewrite | Confuse Ray, Hex, Brine, Pain Split | Muddy Water 45, Shadow Ball 51, Sludge Bomb 53, Scald 55, Energy Ball 61, Water Spout 65, Recover 70 | Jellicent |
| Skarmory | wild | 41 to 44 | Oxide | Spikes, Metal Sound, Steel Wing, Air Slash | Slash 42, Night Slash 45 | Skarmory |
| Skarmory | wild | 41 to 44 | Rewrite | Steel Wing, Air Slash, Air Cutter, Agility | Slash 42, Swift 43, Night Slash 45, Body Press 54, Drill Peck 56, Brave Bird 62, Iron Head 64, Rock Tomb 70 | Skarmory |
| Steelix | wild | 41 to 44 | Oxide | Rock Polish, DragonBreath, Curse, Iron Tail | Crunch 46, Double-Edge 49, Stone Edge 54 | Steelix |
| Steelix | wild | 41 to 44 | Rewrite | Rock Polish, Curse, Iron Head, Body Press | Crunch 46, Double-Edge 49, Rock Slide 54, Fire Fang 56, Earthquake 58, Block 64 | Steelix |
| Bronzong | wild | 42 to 43 | Oxide | Iron Defense, Safeguard, Block, Gyro Ball | Future Sight 43, Faint Attack 50, Payback 61, Heal Block 67 | Bronzong |
| Bronzong | wild | 42 to 43 | Rewrite | Safeguard, Block, Iron Head, Gyro Ball | Future Sight 43, Rock Tomb 45, Faint Attack 50, Body Press 52, Earthquake 58, Payback 61, Heal Block 67, Shadow Ball 69 | Bronzong |
| Carbink | wild | 42 to 43 | Oxide | Rock Polish, Rock Slide, Stealth Rock, Skill Swap | Light Screen 44, Power Gem 45, Moonblast 52, Stone Edge 54, Safeguard 70 | Carbink |
| Carbink | wild | 42 to 43 | Rewrite | Dazzling Gleam, Rock Slide, Stealth Rock, Skill Swap | Light Screen 44, Power Gem 45, Moonblast 52, Psychic 54, Iron Head 59, Body Press 61, Safeguard 70 | Carbink |
| Garganacl | wild | 42 | Oxide | Salt Cure, Recover, Rock Slide, Stealth Rock | Heavy Slam 44, Earthquake 49, Stone Edge 54, Explosion 60 | Garganacl |
| Garganacl | wild | 42 | Rewrite | Rock Tomb, Salt Cure, Stealth Rock, Iron Head | Heavy Slam 44, Earthquake 49, Zen Headbutt 51, Body Press 56, Block 58, Hammer Arm 64 | Garganacl |
| Gliscor | wild | 42 to 43 | Oxide | Night Slash, Swords Dance, U-turn, X-Scissor | Guillotine 45 | Gliscor |
| Gliscor | wild | 42 to 43 | Rewrite | Night Slash, Swords Dance, U-turn, X-Scissor | Earthquake 45, Acrobatics 57, Poison Jab 59, Crunch 65, Lunge 67 | Gliscor |
| Klefki | wild | 42 to 44 | Oxide | Mirror Shot, Flash Cannon, Foul Play, Play Rough | Magic Room 44, Heal Block 50, Last Resort 52 | Klefki |
| Klefki | wild | 42 to 44 | Rewrite | Iron Defense, Flash Cannon, Foul Play, Play Rough | Magic Room 44, Calm Mind 48, Heal Block 50, Last Resort 52, Psychic 56, Skitter Smack 58, Facade 64, Moonblast 66 | Klefki |
| Mienshao | wild | 42 | Oxide | Drain Punch, Vacuum Wave, Aura Sphere, Me First | Jump Kick 45, Dual Chop 48, Focus Blast 51, Acrobatics 55, Hi Jump Kick 64 | Mienshao |
| Mienshao | wild | 42 | Rewrite | Drain Punch, Vacuum Wave, Aura Sphere, Low Sweep | Jump Kick 45, Dual Chop 48, U-turn 50, Acrobatics 55, Rock Tomb 57, Hammer Arm 59, Hi Jump Kick 64 | Mienshao |
| Probopass | wild | 42 to 44 | Oxide | Magnet Bomb, Block, Thunder Wave, Rock Slide | Rest 43, Power Gem 49, Discharge 55, Stone Edge 61, Zap Cannon 67 | Probopass |
| Probopass | wild | 42 to 44 | Rewrite | Iron Defense, Magnet Bomb, Spark, Iron Head | Rest 43, Power Gem 49, Body Press 51, Discharge 55, Fire Punch 58, Earthquake 60, ThunderPunch 66 | Probopass |
| Seaking | super rod | 42 | Oxide | Flail, Aqua Ring, Fury Attack, Waterfall | Horn Drill 47, Agility 56, Megahorn 63 | Seaking |
| Seaking | super rod | 42 | Rewrite | Bulldoze, Aqua Jet, Waterfall, Poison Jab | Throat Chop 44, Aqua Tail 50, Drill Peck 52, Agility 56, Megahorn 63 | Seaking |
| Whiscash | super rod | 42 | Oxide | Magnitude, Rest, Snore, Aqua Tail | Earthquake 45, Future Sight 51, Fissure 57 | Whiscash |
| Whiscash | super rod | 42 | Rewrite | Rest, Zen Headbutt, Aqua Tail, Wild Charge | Earthquake 45, Future Sight 51, Ice Beam 53, Spark 58, Tickle 60, Swagger 66 | Whiscash |
| Weavile | wild | 43 | Oxide | Icy Wind, Night Slash, Fling, Metal Claw | Dark Pulse 49 | Weavile |
| Weavile | wild | 43 | Rewrite | Icy Wind, Night Slash, Fling, Metal Claw | Dark Pulse 49, X-Scissor 61, Icicle Crash 69, Low Sweep 71 | Weavile |
| Crawdaunt | super rod | 45 to 48 | Oxide | Swift, Taunt, Night Slash, Crabhammer | Swords Dance 52, Crunch 57, Guillotine 65 | Crawdaunt |
| Crawdaunt | super rod | 45 to 48 | Rewrite | Metal Claw, Night Slash, Throat Chop, Crabhammer | X-Scissor 46, Swords Dance 52, Crunch 57, Brick Break 59, Close Combat 66 | Crawdaunt |
| Milotic | super rod | 45 | Oxide | Aqua Tail, Hydro Pump, Attract, Safeguard | Aqua Ring 49 | Milotic |
| Milotic | super rod | 45 | Rewrite | Aurora Beam, Surf, Attract, Safeguard | Aqua Ring 49, Alluring Voice 51, Dragon Pulse 54, Muddy Water 58, Scald 60, Earth Power 62, Hyper Voice 66, Ice Beam 68 | Milotic |

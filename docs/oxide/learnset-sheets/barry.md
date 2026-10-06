# Barry's split: what each catch knows and learns

Written by `tools/oxide/balance/learncheck.py sheets` for check 6 of the learnset baseline (`docs/oxide/learnset-checks.md`). One table per capture area first offered in Barry's split, whose cap is 71. Each Pokemon is read at the lowest level it is found at there. "Knows at capture" is the last four moves its list gives by that level; "learns by level-up" is every entry it reaches after capture up to 71, evolving on time, with each later stage's moves under its name; "at the cap" is the stage it can be by then and the next one after. A row marked Rewrite shows the learnset rewrite's lists (the tree's) where it differs from the row marked Oxide, Oxide's lists before the learnset rewrite (`da6b92496c`); a row marked both is the same in each. Relearner-only moves and egg moves are left out.

## Pokémon League

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 71 | At the cap |
|---|---|---|---|---|---|---|
| Chinchou | old rod | 20 | Oxide | Flail, Water Gun, Confuse Ray, Spark | Take Down 23; as Lanturn: Stockpile 27, Swallow 27, Spit Up 27, BubbleBeam 30, Signal Beam 35, Discharge 40, Aqua Ring 47, Hydro Pump 52, Charge 57 | Lanturn (from 27) |
| Chinchou | old rod | 20 | Rewrite | Water Gun, Screech, Confuse Ray, Spark | Take Down 23, Icy Wind 26; as Lanturn: Stockpile 27, Swallow 28, Spit Up 29, BubbleBeam 30, Signal Beam 31, Scald 33, Surf 34, Thunderbolt 37, Discharge 40, Flash Cannon 43, Aqua Ring 47, Muddy Water 52, Volt Switch 54, Dazzling Gleam 55, Charge 57, Ice Beam 60, Swagger 65 | Lanturn (from 27) |
| Goldeen | old rod | 20 | Oxide | Water Sport, Supersonic, Horn Attack, Water Pulse | Flail 21, Aqua Ring 27, Fury Attack 31; as Seaking: Waterfall 40, Horn Drill 47, Agility 56, Megahorn 63 | Seaking (from 33) |
| Goldeen | old rod | 20 | Rewrite | Flip Turn, Water Pulse, Horn Attack, Swagger | Flail 21, Aqua Ring 27; as Seaking: Aqua Jet 34, Skull Bash 37, Waterfall 40, Poison Jab 44, Drill Run 47, Knock Off 50, Aqua Tail 54, Agility 56, Drill Peck 57, Throat Chop 59, Megahorn 63 | Seaking (from 33) |
| Barboach | old rod | 21 | Oxide | Water Sport, Water Gun, Mud Bomb, Amnesia | Water Pulse 22, Magnitude 26; as Whiscash: Rest 33, Snore 33, Aqua Tail 39, Earthquake 45, Future Sight 51, Fissure 57 | Whiscash (from 30) |
| Barboach | old rod | 21 | Rewrite | Water Gun, Mud Bomb, Amnesia, Rock Tomb | Water Pulse 22, Magnitude 26; as Whiscash: Bulldoze 30, Rest 33, Zen Headbutt 36, Aqua Tail 39, Earth Power 40, Wild Charge 42, Earthquake 45, Future Sight 51, Spark 54, Ice Beam 56, Tickle 60, Swagger 65 | Whiscash (from 30) |
| Feebas | old rod | 21 to 22 | Oxide | Splash, Tackle | Flail 30; as Milotic: Hydro Pump 37, Attract 41, Safeguard 45, Aqua Ring 49 | Milotic (from 30) |
| Feebas | old rod | 21 to 22 | Rewrite | Water Gun, Water Pulse, Tackle, Recover | Dragon Tail 24, Captivate 25, Flail 30; as Milotic: Twister 30, Recover 31, Aqua Tail 32, Aurora Beam 33, Dragon Pulse 35, Surf 37, Attract 41, Muddy Water 43, Safeguard 45, Aqua Ring 49, Alluring Voice 54, Scald 56, Ice Beam 58, Hyper Voice 60, Draco Meteor 62, Confuse Ray 65, Life Dew 66, Earth Power 68 | Milotic (from 30) |
| Barboach | good rod | 32 | Oxide | Water Pulse, Magnitude, Rest, Snore | as Whiscash: Rest 33, Snore 33, Aqua Tail 39, Earthquake 45, Future Sight 51, Fissure 57 | Whiscash (from 33) |
| Barboach | good rod | 32 | Rewrite | Amnesia, Rock Tomb, Water Pulse, Magnitude | as Whiscash: Rest 33, Zen Headbutt 36, Aqua Tail 39, Earth Power 40, Wild Charge 42, Earthquake 45, Future Sight 51, Spark 54, Ice Beam 56, Tickle 60, Swagger 65 | Whiscash (from 33) |
| Feebas | good rod | 32 | Oxide | Splash, Tackle, Flail | as Milotic: Hydro Pump 37, Attract 41, Safeguard 45, Aqua Ring 49 | Milotic (from 33) |
| Feebas | good rod | 32 | Rewrite | Recover, Dragon Tail, Captivate, Flail | as Milotic: Aurora Beam 33, Dragon Pulse 35, Surf 37, Attract 41, Muddy Water 43, Safeguard 45, Aqua Ring 49, Alluring Voice 54, Scald 56, Ice Beam 58, Hyper Voice 60, Draco Meteor 62, Confuse Ray 65, Life Dew 66, Earth Power 68 | Milotic (from 33) |
| Chinchou | good rod | 34 | Oxide | Take Down, BubbleBeam, Signal Beam, Discharge | as Lanturn: Signal Beam 35, Discharge 40, Aqua Ring 47, Hydro Pump 52, Charge 57 | Lanturn (from 35) |
| Chinchou | good rod | 34 | Rewrite | Take Down, Icy Wind, Signal Beam, Discharge | as Lanturn: Thunderbolt 37, Discharge 40, Flash Cannon 43, Aqua Ring 47, Muddy Water 52, Volt Switch 54, Dazzling Gleam 55, Charge 57, Ice Beam 60, Swagger 65 | Lanturn (from 35) |
| Corphish | good rod | 34 | Oxide | BubbleBeam, Protect, Knock Off, Taunt | Night Slash 35; as Crawdaunt: Night Slash 39, Crabhammer 44, Swords Dance 52, Crunch 57, Guillotine 65 | Crawdaunt (from 35) |
| Corphish | good rod | 34 | Rewrite | BubbleBeam, Leer, Razor Shell, Knock Off | as Crawdaunt: Throat Chop 35, Aerial Ace 36, Night Slash 39, X-Scissor 41, Crabhammer 44, Brick Break 48, Swords Dance 52, Rock Tomb 54, Crunch 57, Swagger 61, Close Combat 66 | Crawdaunt (from 35) |
| Greninja | good rod | 36 | Oxide | Acrobatics, Low Kick, Waterfall, Fling | Scald 37, Dark Pulse 40, Extrasensory 43, Sludge Wave 47, Gunk Shot 51, Hydro Pump 55, Hydro Cannon 65 | Greninja |
| Greninja | good rod | 36 | Rewrite | Low Kick, Waterfall, Fling, Shadow Sneak | Scald 37, Dark Pulse 40, Extrasensory 43, Sludge Wave 47, Gunk Shot 51, Ice Beam 54, Surf 55, Throat Chop 57, Muddy Water 60, Taunt 62, Hydro Cannon 65 | Greninja |
| Goldeen | surf | 38 | Oxide | Flail, Aqua Ring, Fury Attack, Waterfall | as Seaking: Waterfall 40, Horn Drill 47, Agility 56, Megahorn 63 | Seaking (from 39) |
| Goldeen | surf | 38 | Rewrite | Swagger, Flail, Aqua Ring, Waterfall | as Seaking: Waterfall 40, Poison Jab 44, Drill Run 47, Knock Off 50, Aqua Tail 54, Agility 56, Drill Peck 57, Throat Chop 59, Megahorn 63 | Seaking (from 39) |
| Jellicent | surf | 38 | Oxide | Imprison, Confuse Ray, Hex, Brine | Pain Split 39, Destiny Bond 45, Shadow Ball 51, Scald 55, Water Spout 65, Recover 70 | Jellicent |
| Jellicent | surf | 38 | Rewrite | Imprison, Confuse Ray, Hex, Brine | Pain Split 39, Muddy Water 45, Shadow Ball 51, Sludge Bomb 54, Scald 55, Ice Beam 57, Energy Ball 60, Will-O-Wisp 62, Water Spout 65, Giga Drain 67, Recover 70 | Jellicent |
| Buizel | surf | 41 | Oxide | Swift, Aqua Jet, Agility, Whirlpool | as Floatzel: Razor Wind 50 | Floatzel (from 42) |
| Buizel | surf | 41 | Rewrite | Pursuit, Scary Face, Swift, Aqua Jet | as Floatzel: Low Sweep 44, Agility 51, Rock Tomb 53, Ice Fang 56, Wave Crash 62, Ice Punch 65 | Floatzel (from 42) |
| Floatzel | surf | 41 | Oxide | Aqua Jet, Crunch, Agility, Whirlpool | Razor Wind 50 | Floatzel |
| Floatzel | surf | 41 | Rewrite | Flip Turn, Waterfall, Whirlpool, Liquidation | Low Sweep 44, Agility 51, Rock Tomb 53, Ice Fang 56, Wave Crash 62, Ice Punch 65 | Floatzel |
| Crawdaunt | super rod | 42 | Oxide | Knock Off, Swift, Taunt, Night Slash | Crabhammer 44, Swords Dance 52, Crunch 57, Guillotine 65 | Crawdaunt |
| Crawdaunt | super rod | 42 | Rewrite | Throat Chop, Aerial Ace, Night Slash, X-Scissor | Crabhammer 44, Brick Break 48, Swords Dance 52, Rock Tomb 54, Crunch 57, Swagger 61, Close Combat 66 | Crawdaunt |
| Milotic | super rod | 42 | Oxide | Captivate, Aqua Tail, Hydro Pump, Attract | Safeguard 45, Aqua Ring 49 | Milotic |
| Milotic | super rod | 42 | Rewrite | Aurora Beam, Dragon Pulse, Surf, Attract | Muddy Water 43, Safeguard 45, Aqua Ring 49, Alluring Voice 54, Scald 56, Ice Beam 58, Hyper Voice 60, Draco Meteor 62, Confuse Ray 65, Life Dew 66, Earth Power 68 | Milotic |
| Greninja | surf | 44 | Oxide | Fling, Scald, Dark Pulse, Extrasensory | Sludge Wave 47, Gunk Shot 51, Hydro Pump 55, Hydro Cannon 65 | Greninja |
| Greninja | surf | 44 | Rewrite | Shadow Sneak, Scald, Dark Pulse, Extrasensory | Sludge Wave 47, Gunk Shot 51, Ice Beam 54, Surf 55, Throat Chop 57, Muddy Water 60, Taunt 62, Hydro Cannon 65 | Greninja |
| Floatzel | super rod | 45 | Oxide | Aqua Jet, Crunch, Agility, Whirlpool | Razor Wind 50 | Floatzel |
| Floatzel | super rod | 45 | Rewrite | Waterfall, Whirlpool, Liquidation, Low Sweep | Agility 51, Rock Tomb 53, Ice Fang 56, Wave Crash 62, Ice Punch 65 | Floatzel |
| Lanturn | super rod | 45 | Oxide | Spit Up, BubbleBeam, Signal Beam, Discharge | Aqua Ring 47, Hydro Pump 52, Charge 57 | Lanturn |
| Lanturn | super rod | 45 | Rewrite | Surf, Thunderbolt, Discharge, Flash Cannon | Aqua Ring 47, Muddy Water 52, Volt Switch 54, Dazzling Gleam 55, Charge 57, Ice Beam 60, Swagger 65 | Lanturn |
| Relicanth | super rod | 48 | Oxide | Yawn, Take Down, Mud Sport, AncientPower | Double-Edge 50, Dive 57, Rest 64, Hydro Pump 71 | Relicanth |
| Relicanth | super rod | 48 | Rewrite | Yawn, Take Down, AncientPower, Bulldoze | Double-Edge 50, Aqua Tail 54, Rock Slide 55, Dive 57, Zen Headbutt 58, Earthquake 60, Body Press 62, Rest 64, Body Slam 67, Muddy Water 71 | Relicanth |

## Route 223

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 71 | At the cap |
|---|---|---|---|---|---|---|
| Chinchou | old rod | 20 | Oxide | Flail, Water Gun, Confuse Ray, Spark | Take Down 23; as Lanturn: Stockpile 27, Swallow 27, Spit Up 27, BubbleBeam 30, Signal Beam 35, Discharge 40, Aqua Ring 47, Hydro Pump 52, Charge 57 | Lanturn (from 27) |
| Chinchou | old rod | 20 | Rewrite | Water Gun, Screech, Confuse Ray, Spark | Take Down 23, Icy Wind 26; as Lanturn: Stockpile 27, Swallow 28, Spit Up 29, BubbleBeam 30, Signal Beam 31, Scald 33, Surf 34, Thunderbolt 37, Discharge 40, Flash Cannon 43, Aqua Ring 47, Muddy Water 52, Volt Switch 54, Dazzling Gleam 55, Charge 57, Ice Beam 60, Swagger 65 | Lanturn (from 27) |
| Mantyke | old rod | 20 | Oxide | Supersonic, BubbleBeam, Headbutt, Agility | Wing Attack 22, Water Pulse 28; as Mantine: Take Down 31, Confuse Ray 37, Bounce 40, Aqua Ring 46, Hydro Pump 49 | Mantine (from 30) |
| Mantyke | old rod | 20 | Rewrite | Bubble, BubbleBeam, Headbutt, Agility | Wing Attack 22, Icy Wind 25, Water Pulse 28; as Mantine: Take Down 31, Scald 34, Confuse Ray 37, Bounce 40, Psybeam 41, Signal Beam 43, Aqua Ring 46, Surf 49, Air Slash 54, Roost 56, Muddy Water 58, Ice Beam 60, Swagger 65 | Mantine (from 30) |
| Finneon | old rod | 21 | Oxide | Pound, Water Gun, Attract, Gust | Water Pulse 22, Captivate 26, Safeguard 29; as Lumineon: Aqua Ring 35, Whirlpool 42, U-turn 48, Bounce 53, Silver Wind 59 | Lumineon (from 31) |
| Finneon | old rod | 21 | Rewrite | Attract, Water Pulse, Pursuit, Gust | Captivate 26, Safeguard 29; as Lumineon: Flip Turn 31, Aqua Ring 33, Icy Wind 34, Aqua Tail 38, Signal Beam 40, Whirlpool 42, Ice Fang 45, U-turn 48, Bounce 53, Air Slash 54, Crunch 56, Confuse Ray 57, Silver Wind 59, Charm 65 | Lumineon (from 31) |
| Shellos | old rod | 21 | Oxide | Harden, Water Pulse, Mud Bomb, Hidden Power | Body Slam 29; as Gastrodon: Muddy Water 41, Recover 54 | Gastrodon (from 30) |
| Shellos | old rod | 21 | Rewrite | Harden, Water Pulse, Mud Bomb, Hidden Power | Swagger 22, Body Slam 29; as Gastrodon: AncientPower 33, Earth Power 35, Clear Smog 37, Muddy Water 41, Bulldoze 44, Sludge Bomb 46, Ice Beam 49, Recover 54, Skitter Smack 56, Rock Tomb 60, Block 65 | Gastrodon (from 30) |
| Frogadier | old rod | 22 | Oxide | Water Pulse, Icy Wind, Faint Attack, Acrobatics | Low Kick 25, Waterfall 30, Fling 35; as Greninja: Scald 37, Dark Pulse 40, Extrasensory 43, Sludge Wave 47, Gunk Shot 51, Hydro Pump 55, Hydro Cannon 65 | Greninja (from 36) |
| Frogadier | old rod | 22 | Rewrite | Icy Wind, Thief, Faint Attack, Acrobatics | Low Kick 25, Scald 27, Waterfall 30, Fling 35; as Greninja: Shadow Sneak 36, Scald 37, Dark Pulse 40, Extrasensory 43, Sludge Wave 47, Gunk Shot 51, Ice Beam 54, Surf 55, Throat Chop 57, Muddy Water 60, Taunt 62, Hydro Cannon 65 | Greninja (from 36) |
| Gorebyss | good rod | 32 | Oxide | Water Pulse, Amnesia, Aqua Ring, Captivate | Baton Pass 33, Dive 37, Psychic 42, Aqua Tail 46, Hydro Pump 51 | Gorebyss |
| Gorebyss | good rod | 32 | Rewrite | Water Pulse, Amnesia, Aqua Ring, Captivate | Baton Pass 33, Draining Kiss 35, Dive 37, Surf 40, Psychic 42, Aqua Tail 46, Muddy Water 51, Shadow Ball 54, Ice Beam 56, Shell Smash 58, Scald 60, Scary Face 62, Confuse Ray 65, Screech 68 | Gorebyss |
| Tentacool | good rod | 32 | Oxide | BubbleBeam, Wrap, Barrier, Water Pulse | Poison Jab 33; as Tentacruel: Poison Jab 36, Screech 42, Hydro Pump 49, Wring Out 55 | Tentacruel (from 33) |
| Tentacool | good rod | 32 | Rewrite | Toxic Spikes, Water Pulse, BubbleBeam, Barrier | Poison Jab 33; as Tentacruel: Poison Jab 33, Aurora Beam 34, Sludge Bomb 39, Screech 42, Psybeam 44, Surf 49, Muddy Water 53, Throat Chop 54, Power Gem 56, Flip Turn 58, Ice Beam 60, Toxic 62, Skitter Smack 65, Confuse Ray 68 | Tentacruel (from 33) |
| Mareanie | good rod | 34 | Oxide | Toxic Spikes, Recover, Spike Cannon, Pin Missile | Toxic 36; as Toxapex: Toxic 39, Venom Drench 42, Poison Jab 43, Liquidation 45 | Toxapex (from 38) |
| Mareanie | good rod | 34 | Rewrite | Toxic Spikes, Recover, Spike Cannon, Pin Missile | Toxic 36, Muddy Water 38; as Toxapex: Venom Drench 42, Poison Jab 43, Liquidation 45, Lunge 53, Ice Beam 54, Sludge Bomb 56, Iron Defense 61 | Toxapex (from 38) |
| Octillery | good rod | 34 | Oxide | BubbleBeam, Focus Energy, Octazooka, Bullet Seed | Wring Out 36, Signal Beam 42, Ice Beam 48, Hyper Beam 55 | Octillery |
| Octillery | good rod | 34 | Rewrite | Octazooka, Mud Shot, Bullet Seed, Round | Charge Beam 35, Scald 37, Skitter Smack 40, Signal Beam 42, Ice Beam 48, Psychic 54, Hyper Beam 55, Swagger 61 | Octillery |
| Wailmer | good rod | 36 | Oxide | Mist, Rest, Brine, Water Spout | Amnesia 37; as Wailord: Dive 46, Bounce 54, Hydro Pump 62 | Wailord (from 40) |
| Wailmer | good rod | 36 | Rewrite | Rest, Bulldoze, Brine, Water Spout | Amnesia 37; as Wailord: Dive 46, Iron Head 48, Rock Tomb 50, Bounce 54, Zen Headbutt 55, Ice Beam 56, Surf 62, Earthquake 65 | Wailord (from 40) |
| Mantyke | surf | 38 | Oxide | Wing Attack, Water Pulse, Take Down, Confuse Ray | as Mantine: Bounce 40, Aqua Ring 46, Hydro Pump 49 | Mantine (from 39) |
| Mantyke | surf | 38 | Rewrite | Icy Wind, Water Pulse, Take Down, Confuse Ray | as Mantine: Bounce 40, Psybeam 41, Signal Beam 43, Aqua Ring 46, Surf 49, Air Slash 54, Roost 56, Muddy Water 58, Ice Beam 60, Swagger 65 | Mantine (from 39) |
| Tentacruel | surf | 38 | Oxide | Wrap, Barrier, Water Pulse, Poison Jab | Screech 42, Hydro Pump 49, Wring Out 55 | Tentacruel |
| Tentacruel | surf | 38 | Rewrite | Barrier, Water Pulse, Poison Jab, Aurora Beam | Sludge Bomb 39, Screech 42, Psybeam 44, Surf 49, Muddy Water 53, Throat Chop 54, Power Gem 56, Flip Turn 58, Ice Beam 60, Toxic 62, Skitter Smack 65, Confuse Ray 68 | Tentacruel |
| Kingdra | surf | 41 | Oxide | Agility, Twister, Brine, Hydro Pump | Dragon Dance 48, Dragon Pulse 57 | Kingdra |
| Kingdra | surf | 41 | Rewrite | Agility, Twister, Brine, Muddy Water | Aurora Beam 44, Scald 54, Dragon Pulse 57, Wave Crash 60, Dragon Dance 62, Iron Head 65, Double-Edge 66, Draco Meteor 68, Ice Beam 69, Signal Beam 71 | Kingdra |
| Mantine | surf | 41 | Oxide | Water Pulse, Take Down, Confuse Ray, Bounce | Aqua Ring 46, Hydro Pump 49 | Mantine |
| Mantine | surf | 41 | Rewrite | Scald, Confuse Ray, Bounce, Psybeam | Signal Beam 43, Aqua Ring 46, Surf 49, Air Slash 54, Roost 56, Muddy Water 58, Ice Beam 60, Swagger 65 | Mantine |
| Floatzel | super rod | 42 | Oxide | Aqua Jet, Crunch, Agility, Whirlpool | Razor Wind 50 | Floatzel |
| Floatzel | super rod | 42 | Rewrite | Flip Turn, Waterfall, Whirlpool, Liquidation | Low Sweep 44, Agility 51, Rock Tomb 53, Ice Fang 56, Wave Crash 62, Ice Punch 65 | Floatzel |
| Gastrodon | super rod | 42 | Oxide | Mud Bomb, Hidden Power, Body Slam, Muddy Water | Recover 54 | Gastrodon |
| Gastrodon | super rod | 42 | Rewrite | AncientPower, Earth Power, Clear Smog, Muddy Water | Bulldoze 44, Sludge Bomb 46, Ice Beam 49, Recover 54, Skitter Smack 56, Rock Tomb 60, Block 65 | Gastrodon |
| Toxapex | surf | 44 | Oxide | Pin Missile, Toxic, Venom Drench, Poison Jab | Liquidation 45 | Toxapex |
| Toxapex | surf | 44 | Rewrite | Toxic, Pin Missile, Venom Drench, Poison Jab | Liquidation 45, Lunge 53, Ice Beam 54, Sludge Bomb 56, Iron Defense 61 | Toxapex |
| Jellicent | super rod | 45 | Oxide | Hex, Brine, Pain Split, Destiny Bond | Shadow Ball 51, Scald 55, Water Spout 65, Recover 70 | Jellicent |
| Jellicent | super rod | 45 | Rewrite | Hex, Brine, Pain Split, Muddy Water | Shadow Ball 51, Sludge Bomb 54, Scald 55, Ice Beam 57, Energy Ball 60, Will-O-Wisp 62, Water Spout 65, Giga Drain 67, Recover 70 | Jellicent |
| Lanturn | super rod | 45 to 48 | Oxide | Spit Up, BubbleBeam, Signal Beam, Discharge | Aqua Ring 47, Hydro Pump 52, Charge 57 | Lanturn |
| Lanturn | super rod | 45 to 48 | Rewrite | Surf, Thunderbolt, Discharge, Flash Cannon | Aqua Ring 47, Muddy Water 52, Volt Switch 54, Dazzling Gleam 55, Charge 57, Ice Beam 60, Swagger 65 | Lanturn |

## Sendoff Spring

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 71 | At the cap |
|---|---|---|---|---|---|---|
| Barboach | old rod | 22 | Oxide | Water Gun, Mud Bomb, Amnesia, Water Pulse | Magnitude 26; as Whiscash: Rest 33, Snore 33, Aqua Tail 39, Earthquake 45, Future Sight 51, Fissure 57 | Whiscash (from 30) |
| Barboach | old rod | 22 | Rewrite | Mud Bomb, Amnesia, Rock Tomb, Water Pulse | Magnitude 26; as Whiscash: Bulldoze 30, Rest 33, Zen Headbutt 36, Aqua Tail 39, Earth Power 40, Wild Charge 42, Earthquake 45, Future Sight 51, Spark 54, Ice Beam 56, Tickle 60, Swagger 65 | Whiscash (from 30) |
| Goldeen | old rod | 22 | Oxide | Supersonic, Horn Attack, Water Pulse, Flail | Aqua Ring 27, Fury Attack 31; as Seaking: Waterfall 40, Horn Drill 47, Agility 56, Megahorn 63 | Seaking (from 33) |
| Goldeen | old rod | 22 | Rewrite | Water Pulse, Horn Attack, Swagger, Flail | Aqua Ring 27; as Seaking: Aqua Jet 34, Skull Bash 37, Waterfall 40, Poison Jab 44, Drill Run 47, Knock Off 50, Aqua Tail 54, Agility 56, Drill Peck 57, Throat Chop 59, Megahorn 63 | Seaking (from 33) |
| Corphish | old rod | 24 | Oxide | ViceGrip, Leer, BubbleBeam, Protect | Knock Off 26; as Crawdaunt: Swift 30, Taunt 34, Night Slash 39, Crabhammer 44, Swords Dance 52, Crunch 57, Guillotine 65 | Crawdaunt (from 30) |
| Corphish | old rod | 24 | Rewrite | ViceGrip, BubbleBeam, Leer, Razor Shell | Knock Off 26; as Crawdaunt: Swift 30, Taunt 32, Throat Chop 35, Aerial Ace 36, Night Slash 39, X-Scissor 41, Crabhammer 44, Brick Break 48, Swords Dance 52, Rock Tomb 54, Crunch 57, Swagger 61, Close Combat 66 | Crawdaunt (from 30) |
| Feebas | old rod | 24 | Oxide | Splash, Tackle | Flail 30; as Milotic: Hydro Pump 37, Attract 41, Safeguard 45, Aqua Ring 49 | Milotic (from 30) |
| Feebas | old rod | 24 | Rewrite | Water Pulse, Tackle, Recover, Dragon Tail | Captivate 25, Flail 30; as Milotic: Twister 30, Recover 31, Aqua Tail 32, Aurora Beam 33, Dragon Pulse 35, Surf 37, Attract 41, Muddy Water 43, Safeguard 45, Aqua Ring 49, Alluring Voice 54, Scald 56, Ice Beam 58, Hyper Voice 60, Draco Meteor 62, Confuse Ray 65, Life Dew 66, Earth Power 68 | Milotic (from 30) |
| Frogadier | old rod | 26 | Oxide | Icy Wind, Faint Attack, Acrobatics, Low Kick | Waterfall 30, Fling 35; as Greninja: Scald 37, Dark Pulse 40, Extrasensory 43, Sludge Wave 47, Gunk Shot 51, Hydro Pump 55, Hydro Cannon 65 | Greninja (from 36) |
| Frogadier | old rod | 26 | Rewrite | Thief, Faint Attack, Acrobatics, Low Kick | Scald 27, Waterfall 30, Fling 35; as Greninja: Shadow Sneak 36, Scald 37, Dark Pulse 40, Extrasensory 43, Sludge Wave 47, Gunk Shot 51, Ice Beam 54, Surf 55, Throat Chop 57, Muddy Water 60, Taunt 62, Hydro Cannon 65 | Greninja (from 36) |
| Feebas | good rod | 35 | Oxide | Splash, Tackle, Flail | as Milotic: Hydro Pump 37, Attract 41, Safeguard 45, Aqua Ring 49 | Milotic (from 36) |
| Feebas | good rod | 35 | Rewrite | Recover, Dragon Tail, Captivate, Flail | as Milotic: Surf 37, Attract 41, Muddy Water 43, Safeguard 45, Aqua Ring 49, Alluring Voice 54, Scald 56, Ice Beam 58, Hyper Voice 60, Draco Meteor 62, Confuse Ray 65, Life Dew 66, Earth Power 68 | Milotic (from 36) |
| Frillish | good rod | 35 | Oxide | Imprison, Confuse Ray, Hex, Brine | Pain Split 39; as Jellicent: Destiny Bond 45, Shadow Ball 51, Scald 55, Water Spout 65, Recover 70 | Jellicent (from 40) |
| Frillish | good rod | 35 | Rewrite | Imprison, Confuse Ray, Hex, Brine | Dark Pulse 36, Pain Split 39; as Jellicent: Muddy Water 45, Shadow Ball 51, Sludge Bomb 54, Scald 55, Ice Beam 57, Energy Ball 60, Will-O-Wisp 62, Water Spout 65, Giga Drain 67, Recover 70 | Jellicent (from 40) |
| Chinchou | good rod | 37 | Oxide | Take Down, BubbleBeam, Signal Beam, Discharge | as Lanturn: Discharge 40, Aqua Ring 47, Hydro Pump 52, Charge 57 | Lanturn (from 38) |
| Chinchou | good rod | 37 | Rewrite | Take Down, Icy Wind, Signal Beam, Discharge | as Lanturn: Discharge 40, Flash Cannon 43, Aqua Ring 47, Muddy Water 52, Volt Switch 54, Dazzling Gleam 55, Charge 57, Ice Beam 60, Swagger 65 | Lanturn (from 38) |
| Corphish | good rod | 37 | Oxide | Protect, Knock Off, Taunt, Night Slash | Crabhammer 38; as Crawdaunt: Night Slash 39, Crabhammer 44, Swords Dance 52, Crunch 57, Guillotine 65 | Crawdaunt (from 38) |
| Corphish | good rod | 37 | Rewrite | BubbleBeam, Leer, Razor Shell, Knock Off | Crabhammer 38; as Crawdaunt: Night Slash 39, X-Scissor 41, Crabhammer 44, Brick Break 48, Swords Dance 52, Rock Tomb 54, Crunch 57, Swagger 61, Close Combat 66 | Crawdaunt (from 38) |
| Greninja | good rod | 39 | Oxide | Low Kick, Waterfall, Fling, Scald | Dark Pulse 40, Extrasensory 43, Sludge Wave 47, Gunk Shot 51, Hydro Pump 55, Hydro Cannon 65 | Greninja |
| Greninja | good rod | 39 | Rewrite | Waterfall, Fling, Shadow Sneak, Scald | Dark Pulse 40, Extrasensory 43, Sludge Wave 47, Gunk Shot 51, Ice Beam 54, Surf 55, Throat Chop 57, Muddy Water 60, Taunt 62, Hydro Cannon 65 | Greninja |
| Frillish | surf | 40 | Oxide | Confuse Ray, Hex, Brine, Pain Split | as Jellicent: Destiny Bond 45, Shadow Ball 51, Scald 55, Water Spout 65, Recover 70 | Jellicent (from 41) |
| Frillish | surf | 40 | Rewrite | Hex, Brine, Dark Pulse, Pain Split | as Jellicent: Muddy Water 45, Shadow Ball 51, Sludge Bomb 54, Scald 55, Ice Beam 57, Energy Ball 60, Will-O-Wisp 62, Water Spout 65, Giga Drain 67, Recover 70 | Jellicent (from 41) |
| Jellicent | surf | 40 | Oxide | Confuse Ray, Hex, Brine, Pain Split | Destiny Bond 45, Shadow Ball 51, Scald 55, Water Spout 65, Recover 70 | Jellicent |
| Jellicent | surf | 40 | Rewrite | Confuse Ray, Hex, Brine, Pain Split | Muddy Water 45, Shadow Ball 51, Sludge Bomb 54, Scald 55, Ice Beam 57, Energy Ball 60, Will-O-Wisp 62, Water Spout 65, Giga Drain 67, Recover 70 | Jellicent |
| Buizel | surf | 43 | Oxide | Swift, Aqua Jet, Agility, Whirlpool | as Floatzel: Razor Wind 50 | Floatzel (from 44) |
| Buizel | surf | 43 | Rewrite | Pursuit, Scary Face, Swift, Aqua Jet | as Floatzel: Low Sweep 44, Agility 51, Rock Tomb 53, Ice Fang 56, Wave Crash 62, Ice Punch 65 | Floatzel (from 44) |
| Floatzel | surf | 43 | Oxide | Aqua Jet, Crunch, Agility, Whirlpool | Razor Wind 50 | Floatzel |
| Floatzel | surf | 43 | Rewrite | Flip Turn, Waterfall, Whirlpool, Liquidation | Low Sweep 44, Agility 51, Rock Tomb 53, Ice Fang 56, Wave Crash 62, Ice Punch 65 | Floatzel |
| Crawdaunt | super rod | 45 | Oxide | Swift, Taunt, Night Slash, Crabhammer | Swords Dance 52, Crunch 57, Guillotine 65 | Crawdaunt |
| Crawdaunt | super rod | 45 | Rewrite | Aerial Ace, Night Slash, X-Scissor, Crabhammer | Brick Break 48, Swords Dance 52, Rock Tomb 54, Crunch 57, Swagger 61, Close Combat 66 | Crawdaunt |
| Lanturn | super rod | 45 | Oxide | Spit Up, BubbleBeam, Signal Beam, Discharge | Aqua Ring 47, Hydro Pump 52, Charge 57 | Lanturn |
| Lanturn | super rod | 45 | Rewrite | Surf, Thunderbolt, Discharge, Flash Cannon | Aqua Ring 47, Muddy Water 52, Volt Switch 54, Dazzling Gleam 55, Charge 57, Ice Beam 60, Swagger 65 | Lanturn |
| Feraligatr | surf | 46 | Oxide | Agility, Crunch, Slash, Screech | Thrash 50, Aqua Tail 58, Superpower 63, Hydro Pump 71 | Feraligatr |
| Feraligatr | surf | 46 | Rewrite | Metal Claw, Aqua Jet, Liquidation, Screech | Thrash 50, Aqua Tail 58, Earthquake 61, Superpower 63, Ice Punch 67, Muddy Water 71 | Feraligatr |
| Jellicent | super rod | 48 to 51 | Oxide | Hex, Brine, Pain Split, Destiny Bond | Shadow Ball 51, Scald 55, Water Spout 65, Recover 70 | Jellicent |
| Jellicent | super rod | 48 to 51 | Rewrite | Hex, Brine, Pain Split, Muddy Water | Shadow Ball 51, Sludge Bomb 54, Scald 55, Ice Beam 57, Energy Ball 60, Will-O-Wisp 62, Water Spout 65, Giga Drain 67, Recover 70 | Jellicent |
| Ludicolo | super rod | 48 | Oxide | Astonish, Growl, Mega Drain, Nature Power | nothing | Ludicolo |
| Ludicolo | super rod | 48 | Rewrite | Growl, Mega Drain, Nature Power, Energy Ball | Ice Beam 54, Muddy Water 56, Hyper Voice 58, Leaf Storm 60, Psychic 62, Synthesis 65, Leech Seed 66, Overheat 68 | Ludicolo |
| Donphan | wild | 50 | Oxide | Fury Attack, Assurance, Scary Face, Earthquake | Giga Impact 54 | Donphan |
| Donphan | wild | 50 | Rewrite | Iron Head, Throat Chop, Earthquake, Seed Bomb | Giga Impact 54, Charm 56, Block 61 | Donphan |
| Absol | wild | 51 to 52 | Oxide | Slash, Future Sight, Sucker Punch, Detect | Night Slash 52, Me First 57, Psycho Cut 60, Perish Song 65 | Absol |
| Absol | wild | 51 to 52 | Rewrite | Slash, Future Sight, Sucker Punch, X-Scissor | Night Slash 52, Shadow Ball 54, Throat Chop 56, Rock Slide 58, Psycho Cut 60, Air Slash 62, Perish Song 65, Rock Tomb 68 | Absol |
| Beautifly | wild | 51 | Oxide | Attract, Silver Wind, Giga Drain, Bug Buzz | nothing | Beautifly |
| Beautifly | wild | 51 | Rewrite | Giga Drain, Bug Buzz, Shadow Ball, Energy Ball | Sludge Bomb 53, Toxic 54, Quiver Dance 56, Moonlight 60, Roost 65 | Beautifly |
| Crustle | wild | 51 to 52 | Oxide | Rock Slide, StompingTantrum, Knock Off, Leech Life | Stone Edge 54, Rock Wrecker 61 | Crustle |
| Crustle | wild | 51 to 52 | Rewrite | Body Press, Shell Smash, Knock Off, Leech Life | Stone Edge 54, Skitter Smack 56, Bulldoze 57, Poison Jab 58, Rock Wrecker 61, Rock Polish 63, Earthquake 65, Lunge 68 | Crustle |
| Dhelmise | wild | 51 | Oxide | Anchor Shot, Shadow Claw, Grassy Glide, Giga Drain | Heavy Slam 55, Phantom Force 65, Power Whip 70 | Dhelmise |
| Dhelmise | wild | 51 | Rewrite | Astonish, Shadow Claw, Bulldoze, Giga Drain | Liquidation 54, Heavy Slam 55, Iron Head 57, Body Press 60, Earthquake 61, Poltergeist 62, Phantom Force 65, Petal Blizzard 67, Power Whip 70 | Dhelmise |
| Glimmora | wild | 51 | Oxide | Rock Slide, Power Gem, Acid Armor, Sludge Wave | nothing | Glimmora |
| Glimmora | wild | 51 | Rewrite | Sludge Bomb, Acid Armor, Flash Cannon, Sludge Wave | Energy Ball 54, Dazzling Gleam 56, Earth Power 60, Confuse Ray 65 | Glimmora |
| Heracross | wild | 51 to 53 | Oxide | Take Down, Close Combat, Reversal, Feint | Megahorn 55 | Heracross |
| Heracross | wild | 51 to 53 | Rewrite | Throat Chop, Reversal, Skitter Smack, Lunge | Bulldoze 54, Megahorn 55, Upper Hand 60, Earthquake 65 | Heracross |
| Weavile | wild | 51 to 52 | Oxide | Night Slash, Fling, Metal Claw, Dark Pulse | nothing | Weavile |
| Weavile | wild | 51 to 52 | Rewrite | Night Slash, Fling, Metal Claw, Dark Pulse | X-Scissor 61, Throat Chop 69, Icicle Crash 71 | Weavile |
| Grapploct | wild | 52 | Oxide | Taunt, Reversal, Superpower, Topsy-Turvy | nothing | Grapploct |
| Grapploct | wild | 52 | Rewrite | Bulk Up, Taunt, Reversal, Superpower | Drain Punch 53, Sucker Punch 54, Liquidation 56, StompingTantrum 60, Close Combat 65 | Grapploct |
| Kricketune | wild | 53 | Oxide | Taunt, Night Slash, Bug Buzz, Perish Song | nothing | Kricketune |
| Kricketune | wild | 53 | Rewrite | Pounce, Night Slash, Bug Buzz, Perish Song | Throat Chop 54, Brick Break 56, Secret Power 58, Take Down 60, Earthquake 62, Swagger 65, Sticky Web 68 | Kricketune |
| Pawmot | wild | 53 | Oxide | Super Fang, Entrainment, Wild Charge, Close Combat | Mach Punch 55, Double Shock 61 | Pawmot |
| Pawmot | wild | 53 | Rewrite | Body Press, Entrainment, Wild Charge, Close Combat | Rock Tomb 54, Mach Punch 55, ThunderPunch 56, Agility 57, Low Sweep 58, Double Shock 61, Fire Punch 65, Thunder Wave 66, Throat Chop 68 | Pawmot |

## Turnback Cave

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 71 | At the cap |
|---|---|---|---|---|---|---|
| Giratina | static battle | 47 | Oxide | Ominous Wind, AncientPower, Dragon Claw, Shadow Force | Heal Block 50, Earth Power 60, Slash 70 | Giratina |
| Giratina | static battle | 47 | Rewrite | Ominous Wind, AncientPower, Dragon Claw, Shadow Force | Heal Block 50, Earth Power 60, Scary Face 65, Draco Meteor 66, Poltergeist 67, Aura Sphere 69, Slash 70 | Giratina |

## Victory Road

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 71 | At the cap |
|---|---|---|---|---|---|---|
| Chinchou | old rod | 20 | Oxide | Flail, Water Gun, Confuse Ray, Spark | Take Down 23; as Lanturn: Stockpile 27, Swallow 27, Spit Up 27, BubbleBeam 30, Signal Beam 35, Discharge 40, Aqua Ring 47, Hydro Pump 52, Charge 57 | Lanturn (from 27) |
| Chinchou | old rod | 20 | Rewrite | Water Gun, Screech, Confuse Ray, Spark | Take Down 23, Icy Wind 26; as Lanturn: Stockpile 27, Swallow 28, Spit Up 29, BubbleBeam 30, Signal Beam 31, Scald 33, Surf 34, Thunderbolt 37, Discharge 40, Flash Cannon 43, Aqua Ring 47, Muddy Water 52, Volt Switch 54, Dazzling Gleam 55, Charge 57, Ice Beam 60, Swagger 65 | Lanturn (from 27) |
| Corphish | old rod | 20 | Oxide | Harden, ViceGrip, Leer, BubbleBeam | Protect 23, Knock Off 26; as Crawdaunt: Swift 30, Taunt 34, Night Slash 39, Crabhammer 44, Swords Dance 52, Crunch 57, Guillotine 65 | Crawdaunt (from 30) |
| Corphish | old rod | 20 | Rewrite | ViceGrip, BubbleBeam, Leer, Razor Shell | Knock Off 26; as Crawdaunt: Swift 30, Taunt 32, Throat Chop 35, Aerial Ace 36, Night Slash 39, X-Scissor 41, Crabhammer 44, Brick Break 48, Swords Dance 52, Rock Tomb 54, Crunch 57, Swagger 61, Close Combat 66 | Crawdaunt (from 30) |
| Finneon | old rod | 21 | Oxide | Pound, Water Gun, Attract, Gust | Water Pulse 22, Captivate 26, Safeguard 29; as Lumineon: Aqua Ring 35, Whirlpool 42, U-turn 48, Bounce 53, Silver Wind 59 | Lumineon (from 31) |
| Finneon | old rod | 21 | Rewrite | Attract, Water Pulse, Pursuit, Gust | Captivate 26, Safeguard 29; as Lumineon: Flip Turn 31, Aqua Ring 33, Icy Wind 34, Aqua Tail 38, Signal Beam 40, Whirlpool 42, Ice Fang 45, U-turn 48, Bounce 53, Air Slash 54, Crunch 56, Confuse Ray 57, Silver Wind 59, Charm 65 | Lumineon (from 31) |
| Goldeen | old rod | 21 to 22 | Oxide | Supersonic, Horn Attack, Water Pulse, Flail | Aqua Ring 27, Fury Attack 31; as Seaking: Waterfall 40, Horn Drill 47, Agility 56, Megahorn 63 | Seaking (from 33) |
| Goldeen | old rod | 21 to 22 | Rewrite | Water Pulse, Horn Attack, Swagger, Flail | Aqua Ring 27; as Seaking: Aqua Jet 34, Skull Bash 37, Waterfall 40, Poison Jab 44, Drill Run 47, Knock Off 50, Aqua Tail 54, Agility 56, Drill Peck 57, Throat Chop 59, Megahorn 63 | Seaking (from 33) |
| Goldeen | good rod | 32 | Oxide | Water Pulse, Flail, Aqua Ring, Fury Attack | as Seaking: Waterfall 40, Horn Drill 47, Agility 56, Megahorn 63 | Seaking (from 33) |
| Goldeen | good rod | 32 | Rewrite | Horn Attack, Swagger, Flail, Aqua Ring | as Seaking: Aqua Jet 34, Skull Bash 37, Waterfall 40, Poison Jab 44, Drill Run 47, Knock Off 50, Aqua Tail 54, Agility 56, Drill Peck 57, Throat Chop 59, Megahorn 63 | Seaking (from 33) |
| Lumineon | good rod | 32 | Oxide | Gust, Water Pulse, Captivate, Safeguard | Aqua Ring 35, Whirlpool 42, U-turn 48, Bounce 53, Silver Wind 59 | Lumineon |
| Lumineon | good rod | 32 | Rewrite | Water Pulse, Captivate, Safeguard, Flip Turn | Aqua Ring 33, Icy Wind 34, Aqua Tail 38, Signal Beam 40, Whirlpool 42, Ice Fang 45, U-turn 48, Bounce 53, Air Slash 54, Crunch 56, Confuse Ray 57, Silver Wind 59, Charm 65 | Lumineon |
| Barboach | good rod | 34 | Oxide | Water Pulse, Magnitude, Rest, Snore | Aqua Tail 35; as Whiscash: Aqua Tail 39, Earthquake 45, Future Sight 51, Fissure 57 | Whiscash (from 35) |
| Barboach | good rod | 34 | Rewrite | Amnesia, Rock Tomb, Water Pulse, Magnitude | as Whiscash: Zen Headbutt 36, Aqua Tail 39, Earth Power 40, Wild Charge 42, Earthquake 45, Future Sight 51, Spark 54, Ice Beam 56, Tickle 60, Swagger 65 | Whiscash (from 35) |
| Feebas | good rod | 34 to 36 | Oxide | Splash, Tackle, Flail | as Milotic: Hydro Pump 37, Attract 41, Safeguard 45, Aqua Ring 49 | Milotic (from 35) |
| Feebas | good rod | 34 to 36 | Rewrite | Recover, Dragon Tail, Captivate, Flail | as Milotic: Dragon Pulse 35, Surf 37, Attract 41, Muddy Water 43, Safeguard 45, Aqua Ring 49, Alluring Voice 54, Scald 56, Ice Beam 58, Hyper Voice 60, Draco Meteor 62, Confuse Ray 65, Life Dew 66, Earth Power 68 | Milotic (from 35) |
| Corphish | surf | 38 | Oxide | Knock Off, Taunt, Night Slash, Crabhammer | as Crawdaunt: Night Slash 39, Crabhammer 44, Swords Dance 52, Crunch 57, Guillotine 65 | Crawdaunt (from 39) |
| Corphish | surf | 38 | Rewrite | Leer, Razor Shell, Knock Off, Crabhammer | as Crawdaunt: Night Slash 39, X-Scissor 41, Crabhammer 44, Brick Break 48, Swords Dance 52, Rock Tomb 54, Crunch 57, Swagger 61, Close Combat 66 | Crawdaunt (from 39) |
| Gastrodon | surf | 38 | Oxide | Water Pulse, Mud Bomb, Hidden Power, Body Slam | Muddy Water 41, Recover 54 | Gastrodon |
| Gastrodon | surf | 38 | Rewrite | Body Slam, AncientPower, Earth Power, Clear Smog | Muddy Water 41, Bulldoze 44, Sludge Bomb 46, Ice Beam 49, Recover 54, Skitter Smack 56, Rock Tomb 60, Block 65 | Gastrodon |
| Rhyperior | wild | 40 to 43 | Oxide | Scary Face, Rock Blast, Take Down, Horn Drill | Hammer Arm 42, Stone Edge 45, Earthquake 49, Megahorn 57, Rock Wrecker 61 | Rhyperior |
| Rhyperior | wild | 40 to 43 | Rewrite | Stomp, Scary Face, Rock Blast, Take Down | Hammer Arm 42, Stone Edge 45, Earthquake 49, Megahorn 57, Rock Wrecker 61, Crunch 63, Rock Tomb 65, Superpower 68 | Rhyperior |
| Absol | wild | 41 to 44 | Oxide | Bite, Double Team, Slash, Future Sight | Sucker Punch 44, Detect 49, Night Slash 52, Me First 57, Psycho Cut 60, Perish Song 65 | Absol |
| Absol | wild | 41 to 44 | Rewrite | Swords Dance, Bite, Slash, Future Sight | Sucker Punch 44, X-Scissor 48, Night Slash 52, Shadow Ball 54, Throat Chop 56, Rock Slide 58, Psycho Cut 60, Air Slash 62, Perish Song 65, Rock Tomb 68 | Absol |
| Crustle | wild | 41 | Oxide | Night Slash, X-Scissor, Rock Slide, StompingTantrum | Knock Off 45, Leech Life 48, Stone Edge 54, Rock Wrecker 61 | Crustle |
| Crustle | wild | 41 | Rewrite | Night Slash, X-Scissor, Rock Slide, StompingTantrum | Body Press 42, Shell Smash 44, Knock Off 45, Leech Life 48, Stone Edge 54, Skitter Smack 56, Bulldoze 57, Poison Jab 58, Rock Wrecker 61, Rock Polish 63, Earthquake 65, Lunge 68 | Crustle |
| Goldeen | surf | 41 | Oxide | Aqua Ring, Fury Attack, Waterfall, Horn Drill | as Seaking: Horn Drill 47, Agility 56, Megahorn 63 | Seaking (from 42) |
| Goldeen | surf | 41 | Rewrite | Swagger, Flail, Aqua Ring, Waterfall | as Seaking: Poison Jab 44, Drill Run 47, Knock Off 50, Aqua Tail 54, Agility 56, Drill Peck 57, Throat Chop 59, Megahorn 63 | Seaking (from 42) |
| Golem | wild | 41 | Oxide | Rollout, Rock Blast, Earthquake, Explosion | Double-Edge 44, Stone Edge 49 | Golem |
| Golem | wild | 41 | Rewrite | Magnitude, Rollout, Rock Blast, Earthquake | Double-Edge 44, Stone Edge 49, Sucker Punch 53, Body Press 54, Body Slam 56, Fire Punch 61, Hammer Arm 65, Superpower 68 | Golem |
| Hariyama | wild | 41 to 42 | Oxide | SmellingSalt, Belly Drum, Force Palm, Seismic Toss | Wake-Up Slap 42, Endure 47, Close Combat 52, Reversal 57 | Hariyama |
| Hariyama | wild | 41 to 42 | Rewrite | Force Palm, Bulldoze, Seismic Toss, Rock Tomb | Wake-Up Slap 42, Drain Punch 44, Endure 47, Close Combat 52, Upper Hand 54, Throat Chop 55, Reversal 57, Iron Head 60, Earthquake 65, Headlong Rush 68 | Hariyama |
| Hawlucha | wild | 41 to 42 | Oxide | Submission, Tailwind, Dual Wingbeat, Fly | Hi Jump Kick 42, Me First 48, Acrobatics 55, Close Combat 60 | Hawlucha |
| Hawlucha | wild | 41 to 42 | Rewrite | Flying Press, Tailwind, Dual Wingbeat, Fly | Hi Jump Kick 42, Air Slash 45, Lunge 48, Throat Chop 54, Acrobatics 55, Low Sweep 57, Close Combat 60, Fire Punch 62, Brave Bird 65, Drain Punch 66, ThunderPunch 68, Upper Hand 69, Roost 71 | Hawlucha |
| Jellicent | surf | 41 to 44 | Oxide | Confuse Ray, Hex, Brine, Pain Split | Destiny Bond 45, Shadow Ball 51, Scald 55, Water Spout 65, Recover 70 | Jellicent |
| Jellicent | surf | 41 to 44 | Rewrite | Confuse Ray, Hex, Brine, Pain Split | Muddy Water 45, Shadow Ball 51, Sludge Bomb 54, Scald 55, Ice Beam 57, Energy Ball 60, Will-O-Wisp 62, Water Spout 65, Giga Drain 67, Recover 70 | Jellicent |
| Skarmory | wild | 41 to 44 | Oxide | Spikes, Metal Sound, Steel Wing, Air Slash | Slash 42, Night Slash 45 | Skarmory |
| Skarmory | wild | 41 to 44 | Rewrite | Spikes, Metal Sound, Steel Wing, Air Slash | Slash 42, Night Slash 45, Iron Defense 48, Body Press 54, Drill Peck 56, Iron Head 58, Brave Bird 60, Rock Tomb 62, Double-Edge 65, Drill Run 68 | Skarmory |
| Steelix | wild | 41 to 44 | Oxide | Rock Polish, DragonBreath, Curse, Iron Tail | Crunch 46, Double-Edge 49, Stone Edge 54 | Steelix |
| Steelix | wild | 41 to 44 | Rewrite | DragonBreath, Rock Polish, Curse, Iron Head | Bite 43, Crunch 46, Double-Edge 49, Stone Edge 54, Aqua Tail 56, Fire Fang 58, Earthquake 60, Block 65 | Steelix |
| Bronzong | wild | 42 to 43 | Oxide | Iron Defense, Safeguard, Block, Gyro Ball | Future Sight 43, Faint Attack 50, Payback 61, Heal Block 67 | Bronzong |
| Bronzong | wild | 42 to 43 | Rewrite | Block, Iron Head, Gyro Ball, Rock Tomb | Future Sight 43, Body Press 46, Faint Attack 50, Shadow Ball 54, Earthquake 57, Payback 61, Heal Block 67 | Bronzong |
| Carbink | wild | 42 to 43 | Oxide | Rock Polish, Rock Slide, Stealth Rock, Skill Swap | Light Screen 44, Power Gem 45, Moonblast 52, Stone Edge 54, Safeguard 70 | Carbink |
| Carbink | wild | 42 to 43 | Rewrite | Rock Tomb, Rock Slide, Stealth Rock, Skill Swap | Light Screen 44, Power Gem 45, Moonblast 52, Stone Edge 54, Psychic 56, Body Press 58, Iron Head 60, Safeguard 70 | Carbink |
| Garganacl | wild | 42 | Oxide | Salt Cure, Recover, Rock Slide, Stealth Rock | Heavy Slam 44, Earthquake 49, Stone Edge 54, Explosion 60 | Garganacl |
| Garganacl | wild | 42 | Rewrite | Rock Tomb, Salt Cure, Stealth Rock, Iron Head | Heavy Slam 44, Zen Headbutt 46, Earthquake 49, Stone Edge 54, Body Press 56, Block 58, Hammer Arm 60, Curse 65 | Garganacl |
| Gliscor | wild | 42 to 43 | Oxide | Night Slash, Swords Dance, U-turn, X-Scissor | Guillotine 45 | Gliscor |
| Gliscor | wild | 42 to 43 | Rewrite | Night Slash, Swords Dance, U-turn, X-Scissor | Earthquake 57, Bulldoze 60, Lunge 62, Poison Jab 65, Skitter Smack 66, Throat Chop 68, Brave Bird 71 | Gliscor |
| Klefki | wild | 42 to 44 | Oxide | Mirror Shot, Flash Cannon, Foul Play, Play Rough | Magic Room 44, Heal Block 50, Last Resort 52 | Klefki |
| Klefki | wild | 42 to 44 | Rewrite | Iron Defense, Flash Cannon, Foul Play, Play Rough | Magic Room 44, Calm Mind 47, Heal Block 50, Last Resort 52, Skitter Smack 54, Psychic 56, Moonblast 58, Facade 60, Thunder Wave 65 | Klefki |
| Mienshao | wild | 42 | Oxide | Drain Punch, Vacuum Wave, Aura Sphere, Me First | Jump Kick 45, Dual Chop 48, Focus Blast 51, Acrobatics 55, Hi Jump Kick 64 | Mienshao |
| Mienshao | wild | 42 | Rewrite | Drain Punch, Vacuum Wave, Aura Sphere, U-turn | Rock Tomb 43, Jump Kick 45, Dual Chop 48, Focus Blast 51, Poison Jab 54, Acrobatics 55, Upper Hand 56, Hammer Arm 60, Hi Jump Kick 64 | Mienshao |
| Probopass | wild | 42 to 44 | Oxide | Magnet Bomb, Block, Thunder Wave, Rock Slide | Rest 43, Power Gem 49, Discharge 55, Stone Edge 61, Zap Cannon 67 | Probopass |
| Probopass | wild | 42 to 44 | Rewrite | Rock Slide, Iron Head, Spark, Body Press | Rest 43, Dazzling Gleam 46, Power Gem 49, Thunderbolt 54, Discharge 55, ThunderPunch 57, Earthquake 58, Stone Edge 61, Volt Switch 65 | Probopass |
| Seaking | super rod | 42 | Oxide | Flail, Aqua Ring, Fury Attack, Waterfall | Horn Drill 47, Agility 56, Megahorn 63 | Seaking |
| Seaking | super rod | 42 | Rewrite | Aqua Ring, Aqua Jet, Skull Bash, Waterfall | Poison Jab 44, Drill Run 47, Knock Off 50, Aqua Tail 54, Agility 56, Drill Peck 57, Throat Chop 59, Megahorn 63 | Seaking |
| Whiscash | super rod | 42 | Oxide | Magnitude, Rest, Snore, Aqua Tail | Earthquake 45, Future Sight 51, Fissure 57 | Whiscash |
| Whiscash | super rod | 42 | Rewrite | Zen Headbutt, Aqua Tail, Earth Power, Wild Charge | Earthquake 45, Future Sight 51, Spark 54, Ice Beam 56, Tickle 60, Swagger 65 | Whiscash |
| Weavile | wild | 43 | Oxide | Icy Wind, Night Slash, Fling, Metal Claw | Dark Pulse 49 | Weavile |
| Weavile | wild | 43 | Rewrite | Icy Wind, Night Slash, Fling, Metal Claw | Dark Pulse 49, X-Scissor 61, Throat Chop 69, Icicle Crash 71 | Weavile |
| Crawdaunt | super rod | 45 to 48 | Oxide | Swift, Taunt, Night Slash, Crabhammer | Swords Dance 52, Crunch 57, Guillotine 65 | Crawdaunt |
| Crawdaunt | super rod | 45 to 48 | Rewrite | Aerial Ace, Night Slash, X-Scissor, Crabhammer | Brick Break 48, Swords Dance 52, Rock Tomb 54, Crunch 57, Swagger 61, Close Combat 66 | Crawdaunt |
| Milotic | super rod | 45 | Oxide | Aqua Tail, Hydro Pump, Attract, Safeguard | Aqua Ring 49 | Milotic |
| Milotic | super rod | 45 | Rewrite | Surf, Attract, Muddy Water, Safeguard | Aqua Ring 49, Alluring Voice 54, Scald 56, Ice Beam 58, Hyper Voice 60, Draco Meteor 62, Confuse Ray 65, Life Dew 66, Earth Power 68 | Milotic |

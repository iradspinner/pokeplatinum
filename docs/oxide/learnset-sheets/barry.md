# Barry's split: what each catch knows and learns

Written by `tools/oxide/balance/learncheck.py sheets` for check 6 of the learnset baseline (`docs/oxide/learnset-checks.md`). One table per capture area first offered in Barry's split, whose cap is 71. Each Pokemon is read at the lowest level it is found at there. "Knows at capture" is the last four moves its list gives by that level; "learns by level-up" is every entry it reaches after capture up to 71, evolving on time, with each later stage's moves under its name; "at the cap" is the stage it can be by then and the next one after. A row marked v3 shows learnset v3 (unlanded, `origin/balance-learngen-v2`) where it differs from Oxide's lists; a row marked both is the same in each. Relearner-only moves and egg moves are left out. Nothing here is in the game data.

## Pokémon League

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 71 | At the cap |
|---|---|---|---|---|---|---|
| Chinchou | old rod | 20 | Oxide | Flail, Water Gun, Confuse Ray, Spark | Take Down 23; as Lanturn: Stockpile 27, Swallow 27, Spit Up 27, BubbleBeam 30, Signal Beam 35, Discharge 40, Aqua Ring 47, Hydro Pump 52, Charge 57 | Lanturn (from 27) |
| Chinchou | old rod | 20 | v3 | Flail, Water Gun, Confuse Ray, Spark | Take Down 23; as Lanturn: Stockpile 27, Swallow 27, Spit Up 27, BubbleBeam 30, Signal Beam 35, Aqua Ring 47, Hydro Pump 52, Discharge 53, Charge 57, Thunder 65 | Lanturn (from 27) |
| Goldeen | old rod | 20 | Oxide | Water Sport, Supersonic, Horn Attack, Water Pulse | Flail 21, Aqua Ring 27, Fury Attack 31; as Seaking: Waterfall 40, Horn Drill 47, Agility 56, Megahorn 63 | Seaking (from 33) |
| Goldeen | old rod | 20 | v3 | Water Sport, Supersonic, Horn Attack, Water Pulse | Flail 21, Aqua Ring 27; as Seaking: Waterfall 40, Horn Drill 47, Agility 56, Megahorn 63 | Seaking (from 33) |
| Barboach | old rod | 21 | Oxide | Water Sport, Water Gun, Mud Bomb, Amnesia | Water Pulse 22, Magnitude 26; as Whiscash: Rest 33, Snore 33, Aqua Tail 39, Earthquake 45, Future Sight 51, Fissure 57 | Whiscash (from 30) |
| Barboach | old rod | 21 | v3 | Water Sport, Water Gun, Mud Bomb, Amnesia | Water Pulse 22, Magnitude 26; as Whiscash: Rest 33, Aqua Tail 39, Earthquake 45, Future Sight 51, Fissure 57, Zen Headbutt 63 | Whiscash (from 30) |
| Feebas | old rod | 21 to 22 | Oxide | Splash, Tackle | Flail 30; as Milotic: Hydro Pump 37, Attract 41, Safeguard 45, Aqua Ring 49 | Milotic (from 30) |
| Feebas | old rod | 21 to 22 | v3 | Tackle, Water Gun | Flail 30; as Milotic: Hydro Pump 37, Attract 41, Safeguard 45, Aqua Ring 49 | Milotic (from 30) |
| Barboach | good rod | 32 | Oxide | Water Pulse, Magnitude, Rest, Snore | as Whiscash: Rest 33, Snore 33, Aqua Tail 39, Earthquake 45, Future Sight 51, Fissure 57 | Whiscash (from 33) |
| Barboach | good rod | 32 | v3 | Amnesia, Water Pulse, Magnitude, Rest | as Whiscash: Rest 33, Aqua Tail 39, Earthquake 45, Future Sight 51, Fissure 57, Zen Headbutt 63 | Whiscash (from 33) |
| Feebas | good rod | 32 | Oxide | Splash, Tackle, Flail | as Milotic: Hydro Pump 37, Attract 41, Safeguard 45, Aqua Ring 49 | Milotic (from 33) |
| Feebas | good rod | 32 | v3 | Tackle, Water Gun, Flail | as Milotic: Hydro Pump 37, Attract 41, Safeguard 45, Aqua Ring 49 | Milotic (from 33) |
| Chinchou | good rod | 34 | Oxide | Take Down, BubbleBeam, Signal Beam, Discharge | as Lanturn: Signal Beam 35, Discharge 40, Aqua Ring 47, Hydro Pump 52, Charge 57 | Lanturn (from 35) |
| Chinchou | good rod | 34 | v3 | Spark, Take Down, BubbleBeam, Signal Beam | as Lanturn: Signal Beam 35, Aqua Ring 47, Hydro Pump 52, Discharge 53, Charge 57, Thunder 65 | Lanturn (from 35) |
| Corphish | good rod | 34 | Oxide | BubbleBeam, Protect, Knock Off, Taunt | Night Slash 35; as Crawdaunt: Night Slash 39, Crabhammer 44, Swords Dance 52, Crunch 57, Guillotine 65 | Crawdaunt (from 35) |
| Corphish | good rod | 34 | v3 | BubbleBeam, Protect, Knock Off, Taunt | Night Slash 35; as Crawdaunt: Night Slash 39, Crabhammer 44, Swords Dance 52, Crunch 57, Cross Chop 63, Guillotine 65 | Crawdaunt (from 35) |
| Greninja | good rod | 36 | both | Acrobatics, Low Kick, Waterfall, Fling | Scald 37, Dark Pulse 40, Extrasensory 43, Sludge Wave 47, Gunk Shot 51, Hydro Pump 55, Hydro Cannon 65 | Greninja |
| Goldeen | surf | 38 | Oxide | Flail, Aqua Ring, Fury Attack, Waterfall | as Seaking: Waterfall 40, Horn Drill 47, Agility 56, Megahorn 63 | Seaking (from 39) |
| Goldeen | surf | 38 | v3 | Water Pulse, Flail, Aqua Ring, Waterfall | as Seaking: Waterfall 40, Horn Drill 47, Agility 56, Megahorn 63 | Seaking (from 39) |
| Jellicent | surf | 38 | Oxide | Imprison, Confuse Ray, Hex, Brine | Pain Split 39, Destiny Bond 45, Shadow Ball 51, Scald 55, Water Spout 65, Recover 70 | Jellicent |
| Jellicent | surf | 38 | v3 | Imprison, Confuse Ray, Hex, Brine | Pain Split 39, Destiny Bond 45, Shadow Ball 52, Scald 53, Water Spout 65, Recover 70 | Jellicent |
| Buizel | surf | 41 | Oxide | Swift, Aqua Jet, Agility, Whirlpool | as Floatzel: Razor Wind 50 | Floatzel (from 42) |
| Buizel | surf | 41 | v3 | Pursuit, Swift, Aqua Jet, Agility | as Floatzel: Ice Punch 66 | Floatzel (from 42) |
| Floatzel | surf | 41 | Oxide | Aqua Jet, Crunch, Agility, Whirlpool | Razor Wind 50 | Floatzel |
| Floatzel | surf | 41 | v3 | Swift, Aqua Jet, Crunch, Agility | Ice Punch 66 | Floatzel |
| Crawdaunt | super rod | 42 | Oxide | Knock Off, Swift, Taunt, Night Slash | Crabhammer 44, Swords Dance 52, Crunch 57, Guillotine 65 | Crawdaunt |
| Crawdaunt | super rod | 42 | v3 | Knock Off, Swift, Taunt, Night Slash | Crabhammer 44, Swords Dance 52, Crunch 57, Cross Chop 63, Guillotine 65 | Crawdaunt |
| Milotic | super rod | 42 | both | Captivate, Aqua Tail, Hydro Pump, Attract | Safeguard 45, Aqua Ring 49 | Milotic |
| Greninja | surf | 44 | both | Fling, Scald, Dark Pulse, Extrasensory | Sludge Wave 47, Gunk Shot 51, Hydro Pump 55, Hydro Cannon 65 | Greninja |
| Floatzel | super rod | 45 | Oxide | Aqua Jet, Crunch, Agility, Whirlpool | Razor Wind 50 | Floatzel |
| Floatzel | super rod | 45 | v3 | Swift, Aqua Jet, Crunch, Agility | Ice Punch 66 | Floatzel |
| Lanturn | super rod | 45 | Oxide | Spit Up, BubbleBeam, Signal Beam, Discharge | Aqua Ring 47, Hydro Pump 52, Charge 57 | Lanturn |
| Lanturn | super rod | 45 | v3 | Swallow, Spit Up, BubbleBeam, Signal Beam | Aqua Ring 47, Hydro Pump 52, Discharge 53, Charge 57, Thunder 65 | Lanturn |
| Relicanth | super rod | 48 | Oxide | Yawn, Take Down, Mud Sport, AncientPower | Double-Edge 50, Dive 57, Rest 64, Hydro Pump 71 | Relicanth |
| Relicanth | super rod | 48 | v3 | Take Down, Mud Sport, Dive, AncientPower | Double-Edge 50, Earthquake 53, Rest 64, Hydro Pump 71 | Relicanth |

## Route 223

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 71 | At the cap |
|---|---|---|---|---|---|---|
| Chinchou | old rod | 20 | Oxide | Flail, Water Gun, Confuse Ray, Spark | Take Down 23; as Lanturn: Stockpile 27, Swallow 27, Spit Up 27, BubbleBeam 30, Signal Beam 35, Discharge 40, Aqua Ring 47, Hydro Pump 52, Charge 57 | Lanturn (from 27) |
| Chinchou | old rod | 20 | v3 | Flail, Water Gun, Confuse Ray, Spark | Take Down 23; as Lanturn: Stockpile 27, Swallow 27, Spit Up 27, BubbleBeam 30, Signal Beam 35, Aqua Ring 47, Hydro Pump 52, Discharge 53, Charge 57, Thunder 65 | Lanturn (from 27) |
| Mantyke | old rod | 20 | Oxide | Supersonic, BubbleBeam, Headbutt, Agility | Wing Attack 22, Water Pulse 28; as Mantine: Take Down 31, Confuse Ray 37, Bounce 40, Aqua Ring 46, Hydro Pump 49 | Mantine (from 30) |
| Mantyke | old rod | 20 | v3 | Supersonic, BubbleBeam, Headbutt, Agility | Wing Attack 22, Water Pulse 28; as Mantine: Take Down 31, Confuse Ray 37, Bounce 40, Aqua Ring 46, Hydro Pump 49, Air Slash 66 | Mantine (from 30) |
| Finneon | old rod | 21 | Oxide | Pound, Water Gun, Attract, Gust | Water Pulse 22, Captivate 26, Safeguard 29; as Lumineon: Aqua Ring 35, Whirlpool 42, U-turn 48, Bounce 53, Silver Wind 59 | Lumineon (from 31) |
| Finneon | old rod | 21 | v3 | Pound, Water Gun, Attract | Water Pulse 22, Captivate 26, Safeguard 29; as Lumineon: Aqua Ring 35, U-turn 48, Bounce 53, Silver Wind 59, Ice Fang 65 | Lumineon (from 31) |
| Shellos | old rod | 21 | Oxide | Harden, Water Pulse, Mud Bomb, Hidden Power | Body Slam 29; as Gastrodon: Muddy Water 41, Recover 54 | Gastrodon (from 30) |
| Shellos | old rod | 21 | v3 | Harden, Water Pulse, Mud Bomb, Hidden Power | Body Slam 29; as Gastrodon: Muddy Water 39, Earthquake 44, Recover 54, Rock Slide 64 | Gastrodon (from 30) |
| Frogadier | old rod | 22 | Oxide | Water Pulse, Icy Wind, Faint Attack, Acrobatics | Low Kick 25, Waterfall 30, Fling 35; as Greninja: Scald 37, Dark Pulse 40, Extrasensory 43, Sludge Wave 47, Gunk Shot 51, Hydro Pump 55, Hydro Cannon 65 | Greninja (from 36) |
| Frogadier | old rod | 22 | v3 | Water Pulse, Icy Wind, Faint Attack, Acrobatics | Low Kick 25, Fling 35; as Greninja: Water Shuriken on evolving, Night Slash on evolving, Scald 37, Dark Pulse 40, Extrasensory 43, Sludge Wave 47, Gunk Shot 51, Hydro Pump 55, Hydro Cannon 65 | Greninja (from 36) |
| Gorebyss | good rod | 32 | Oxide | Water Pulse, Amnesia, Aqua Ring, Captivate | Baton Pass 33, Dive 37, Psychic 42, Aqua Tail 46, Hydro Pump 51 | Gorebyss |
| Gorebyss | good rod | 32 | v3 | Water Pulse, Amnesia, Aqua Ring, Captivate | Baton Pass 33, Dive 37, Psychic 42, Aqua Tail 46, Hydro Pump 51, Ice Beam 65 | Gorebyss |
| Tentacool | good rod | 32 | Oxide | BubbleBeam, Wrap, Barrier, Water Pulse | Poison Jab 33; as Tentacruel: Poison Jab 36, Screech 42, Hydro Pump 49, Wring Out 55 | Tentacruel (from 33) |
| Tentacool | good rod | 32 | v3 | Toxic Spikes, BubbleBeam, Barrier, Water Pulse | Poison Jab 33; as Tentacruel: Poison Jab 36, Screech 42, Toxic 44, Hydro Pump 49, Wring Out 55 | Tentacruel (from 33) |
| Mareanie | good rod | 34 | Oxide | Toxic Spikes, Recover, Spike Cannon, Pin Missile | Toxic 36; as Toxapex: Toxic 39, Venom Drench 42, Poison Jab 43, Liquidation 45 | Toxapex (from 38) |
| Mareanie | good rod | 34 | v3 | Toxic Spikes, Recover, Spike Cannon, Pin Missile | Toxic 36; as Toxapex: Baneful Bunker on evolving, Toxic 39, Venom Drench 42, Poison Jab 43, Liquidation 45 | Toxapex (from 38) |
| Octillery | good rod | 34 | Oxide | BubbleBeam, Focus Energy, Octazooka, Bullet Seed | Wring Out 36, Signal Beam 42, Ice Beam 48, Hyper Beam 55 | Octillery |
| Octillery | good rod | 34 | v3 | BubbleBeam, Focus Energy, Octazooka, Bullet Seed | Wring Out 36, Signal Beam 42, Ice Beam 48, Hyper Beam 55, Gunk Shot 71 | Octillery |
| Wailmer | good rod | 36 | Oxide | Mist, Rest, Brine, Water Spout | Amnesia 37; as Wailord: Dive 46, Bounce 54, Hydro Pump 62 | Wailord (from 40) |
| Wailmer | good rod | 36 | v3 | Water Pulse, Mist, Rest, Brine | Amnesia 37; as Wailord: Dive 46, Bounce 54, Hydro Pump 62 | Wailord (from 40) |
| Mantyke | surf | 38 | Oxide | Wing Attack, Water Pulse, Take Down, Confuse Ray | as Mantine: Bounce 40, Aqua Ring 46, Hydro Pump 49 | Mantine (from 39) |
| Mantyke | surf | 38 | v3 | Wing Attack, Water Pulse, Take Down, Confuse Ray | as Mantine: Bounce 40, Aqua Ring 46, Hydro Pump 49, Air Slash 66 | Mantine (from 39) |
| Tentacruel | surf | 38 | Oxide | Wrap, Barrier, Water Pulse, Poison Jab | Screech 42, Hydro Pump 49, Wring Out 55 | Tentacruel |
| Tentacruel | surf | 38 | v3 | BubbleBeam, Barrier, Water Pulse, Poison Jab | Screech 42, Toxic 44, Hydro Pump 49, Wring Out 55 | Tentacruel |
| Kingdra | surf | 41 | both | Agility, Twister, Brine, Hydro Pump | Dragon Dance 48, Dragon Pulse 57 | Kingdra |
| Mantine | surf | 41 | Oxide | Water Pulse, Take Down, Confuse Ray, Bounce | Aqua Ring 46, Hydro Pump 49 | Mantine |
| Mantine | surf | 41 | v3 | Water Pulse, Take Down, Confuse Ray, Bounce | Aqua Ring 46, Hydro Pump 49, Air Slash 66 | Mantine |
| Floatzel | super rod | 42 | Oxide | Aqua Jet, Crunch, Agility, Whirlpool | Razor Wind 50 | Floatzel |
| Floatzel | super rod | 42 | v3 | Swift, Aqua Jet, Crunch, Agility | Ice Punch 66 | Floatzel |
| Gastrodon | super rod | 42 | Oxide | Mud Bomb, Hidden Power, Body Slam, Muddy Water | Recover 54 | Gastrodon |
| Gastrodon | super rod | 42 | v3 | Mud Bomb, Hidden Power, Body Slam, Muddy Water | Earthquake 44, Recover 54, Rock Slide 64 | Gastrodon |
| Toxapex | surf | 44 | both | Pin Missile, Toxic, Venom Drench, Poison Jab | Liquidation 45 | Toxapex |
| Jellicent | super rod | 45 | Oxide | Hex, Brine, Pain Split, Destiny Bond | Shadow Ball 51, Scald 55, Water Spout 65, Recover 70 | Jellicent |
| Jellicent | super rod | 45 | v3 | Hex, Brine, Pain Split, Destiny Bond | Shadow Ball 52, Scald 53, Water Spout 65, Recover 70 | Jellicent |
| Lanturn | super rod | 45 to 48 | Oxide | Spit Up, BubbleBeam, Signal Beam, Discharge | Aqua Ring 47, Hydro Pump 52, Charge 57 | Lanturn |
| Lanturn | super rod | 45 to 48 | v3 | Swallow, Spit Up, BubbleBeam, Signal Beam | Aqua Ring 47, Hydro Pump 52, Discharge 53, Charge 57, Thunder 65 | Lanturn |

## Sendoff Spring

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 71 | At the cap |
|---|---|---|---|---|---|---|
| Barboach | old rod | 22 | Oxide | Water Gun, Mud Bomb, Amnesia, Water Pulse | Magnitude 26; as Whiscash: Rest 33, Snore 33, Aqua Tail 39, Earthquake 45, Future Sight 51, Fissure 57 | Whiscash (from 30) |
| Barboach | old rod | 22 | v3 | Water Gun, Mud Bomb, Amnesia, Water Pulse | Magnitude 26; as Whiscash: Rest 33, Aqua Tail 39, Earthquake 45, Future Sight 51, Fissure 57, Zen Headbutt 63 | Whiscash (from 30) |
| Goldeen | old rod | 22 | Oxide | Supersonic, Horn Attack, Water Pulse, Flail | Aqua Ring 27, Fury Attack 31; as Seaking: Waterfall 40, Horn Drill 47, Agility 56, Megahorn 63 | Seaking (from 33) |
| Goldeen | old rod | 22 | v3 | Supersonic, Horn Attack, Water Pulse, Flail | Aqua Ring 27; as Seaking: Waterfall 40, Horn Drill 47, Agility 56, Megahorn 63 | Seaking (from 33) |
| Corphish | old rod | 24 | Oxide | ViceGrip, Leer, BubbleBeam, Protect | Knock Off 26; as Crawdaunt: Swift 30, Taunt 34, Night Slash 39, Crabhammer 44, Swords Dance 52, Crunch 57, Guillotine 65 | Crawdaunt (from 30) |
| Corphish | old rod | 24 | v3 | ViceGrip, Leer, BubbleBeam, Protect | Knock Off 26; as Crawdaunt: Swift 30, Taunt 34, Night Slash 39, Crabhammer 44, Swords Dance 52, Crunch 57, Cross Chop 63, Guillotine 65 | Crawdaunt (from 30) |
| Feebas | old rod | 24 | Oxide | Splash, Tackle | Flail 30; as Milotic: Hydro Pump 37, Attract 41, Safeguard 45, Aqua Ring 49 | Milotic (from 30) |
| Feebas | old rod | 24 | v3 | Tackle, Water Gun | Flail 30; as Milotic: Hydro Pump 37, Attract 41, Safeguard 45, Aqua Ring 49 | Milotic (from 30) |
| Frogadier | old rod | 26 | Oxide | Icy Wind, Faint Attack, Acrobatics, Low Kick | Waterfall 30, Fling 35; as Greninja: Scald 37, Dark Pulse 40, Extrasensory 43, Sludge Wave 47, Gunk Shot 51, Hydro Pump 55, Hydro Cannon 65 | Greninja (from 36) |
| Frogadier | old rod | 26 | v3 | Icy Wind, Faint Attack, Acrobatics, Low Kick | Fling 35; as Greninja: Water Shuriken on evolving, Night Slash on evolving, Scald 37, Dark Pulse 40, Extrasensory 43, Sludge Wave 47, Gunk Shot 51, Hydro Pump 55, Hydro Cannon 65 | Greninja (from 36) |
| Feebas | good rod | 35 | Oxide | Splash, Tackle, Flail | as Milotic: Hydro Pump 37, Attract 41, Safeguard 45, Aqua Ring 49 | Milotic (from 36) |
| Feebas | good rod | 35 | v3 | Tackle, Water Gun, Flail | as Milotic: Hydro Pump 37, Attract 41, Safeguard 45, Aqua Ring 49 | Milotic (from 36) |
| Frillish | good rod | 35 | Oxide | Imprison, Confuse Ray, Hex, Brine | Pain Split 39; as Jellicent: Destiny Bond 45, Shadow Ball 51, Scald 55, Water Spout 65, Recover 70 | Jellicent (from 40) |
| Frillish | good rod | 35 | v3 | Imprison, Confuse Ray, Hex, Brine | Pain Split 39; as Jellicent: Destiny Bond 45, Shadow Ball 52, Scald 53, Water Spout 65, Recover 70 | Jellicent (from 40) |
| Chinchou | good rod | 37 | Oxide | Take Down, BubbleBeam, Signal Beam, Discharge | as Lanturn: Discharge 40, Aqua Ring 47, Hydro Pump 52, Charge 57 | Lanturn (from 38) |
| Chinchou | good rod | 37 | v3 | Spark, Take Down, BubbleBeam, Signal Beam | Discharge 38; as Lanturn: Aqua Ring 47, Hydro Pump 52, Discharge 53, Charge 57, Thunder 65 | Lanturn (from 38) |
| Corphish | good rod | 37 | Oxide | Protect, Knock Off, Taunt, Night Slash | Crabhammer 38; as Crawdaunt: Night Slash 39, Crabhammer 44, Swords Dance 52, Crunch 57, Guillotine 65 | Crawdaunt (from 38) |
| Corphish | good rod | 37 | v3 | Protect, Knock Off, Taunt, Night Slash | Crabhammer 38; as Crawdaunt: Night Slash 39, Crabhammer 44, Swords Dance 52, Crunch 57, Cross Chop 63, Guillotine 65 | Crawdaunt (from 38) |
| Greninja | good rod | 39 | both | Low Kick, Waterfall, Fling, Scald | Dark Pulse 40, Extrasensory 43, Sludge Wave 47, Gunk Shot 51, Hydro Pump 55, Hydro Cannon 65 | Greninja |
| Frillish | surf | 40 | Oxide | Confuse Ray, Hex, Brine, Pain Split | as Jellicent: Destiny Bond 45, Shadow Ball 51, Scald 55, Water Spout 65, Recover 70 | Jellicent (from 41) |
| Frillish | surf | 40 | v3 | Confuse Ray, Hex, Brine, Pain Split | as Jellicent: Destiny Bond 45, Shadow Ball 52, Scald 53, Water Spout 65, Recover 70 | Jellicent (from 41) |
| Jellicent | surf | 40 | Oxide | Confuse Ray, Hex, Brine, Pain Split | Destiny Bond 45, Shadow Ball 51, Scald 55, Water Spout 65, Recover 70 | Jellicent |
| Jellicent | surf | 40 | v3 | Confuse Ray, Hex, Brine, Pain Split | Destiny Bond 45, Shadow Ball 52, Scald 53, Water Spout 65, Recover 70 | Jellicent |
| Buizel | surf | 43 | Oxide | Swift, Aqua Jet, Agility, Whirlpool | as Floatzel: Razor Wind 50 | Floatzel (from 44) |
| Buizel | surf | 43 | v3 | Pursuit, Swift, Aqua Jet, Agility | as Floatzel: Ice Punch 66 | Floatzel (from 44) |
| Floatzel | surf | 43 | Oxide | Aqua Jet, Crunch, Agility, Whirlpool | Razor Wind 50 | Floatzel |
| Floatzel | surf | 43 | v3 | Swift, Aqua Jet, Crunch, Agility | Ice Punch 66 | Floatzel |
| Crawdaunt | super rod | 45 | Oxide | Swift, Taunt, Night Slash, Crabhammer | Swords Dance 52, Crunch 57, Guillotine 65 | Crawdaunt |
| Crawdaunt | super rod | 45 | v3 | Swift, Taunt, Night Slash, Crabhammer | Swords Dance 52, Crunch 57, Cross Chop 63, Guillotine 65 | Crawdaunt |
| Lanturn | super rod | 45 | Oxide | Spit Up, BubbleBeam, Signal Beam, Discharge | Aqua Ring 47, Hydro Pump 52, Charge 57 | Lanturn |
| Lanturn | super rod | 45 | v3 | Swallow, Spit Up, BubbleBeam, Signal Beam | Aqua Ring 47, Hydro Pump 52, Discharge 53, Charge 57, Thunder 65 | Lanturn |
| Feraligatr | surf | 46 | Oxide | Agility, Crunch, Slash, Screech | Thrash 50, Aqua Tail 58, Superpower 63, Hydro Pump 71 | Feraligatr |
| Feraligatr | surf | 46 | v3 | Agility, Crunch, Slash, Screech | Thrash 50, Aqua Tail 58, Hydro Pump 71 | Feraligatr |
| Jellicent | super rod | 48 to 51 | Oxide | Hex, Brine, Pain Split, Destiny Bond | Shadow Ball 51, Scald 55, Water Spout 65, Recover 70 | Jellicent |
| Jellicent | super rod | 48 to 51 | v3 | Hex, Brine, Pain Split, Destiny Bond | Shadow Ball 52, Scald 53, Water Spout 65, Recover 70 | Jellicent |
| Ludicolo | super rod | 48 | Oxide | Astonish, Growl, Mega Drain, Nature Power | nothing | Ludicolo |
| Ludicolo | super rod | 48 | v3 | Growl, Mega Drain, Nature Power, Hydro Pump | Energy Ball 68 | Ludicolo |
| Donphan | wild | 50 | Oxide | Fury Attack, Assurance, Scary Face, Earthquake | Giga Impact 54 | Donphan |
| Donphan | wild | 50 | v3 | Fury Attack, Assurance, Scary Face, Earthquake | Giga Impact 54, Fire Fang 69 | Donphan |
| Absol | wild | 51 to 52 | Oxide | Slash, Future Sight, Sucker Punch, Detect | Night Slash 52, Me First 57, Psycho Cut 60, Perish Song 65 | Absol |
| Absol | wild | 51 to 52 | v3 | Slash, Future Sight, Sucker Punch, Detect | Me First 57, Psycho Cut 60, Perish Song 65 | Absol |
| Beautifly | wild | 51 | Oxide | Attract, Silver Wind, Giga Drain, Bug Buzz | nothing | Beautifly |
| Beautifly | wild | 51 | v3 | Attract, Silver Wind, Giga Drain, Bug Buzz | Venoshock 61 | Beautifly |
| Crustle | wild | 51 to 52 | both | Rock Slide, StompingTantrum, Knock Off, Leech Life | Stone Edge 54, Rock Wrecker 61 | Crustle |
| Dhelmise | wild | 51 | both | Anchor Shot, Shadow Claw, Grassy Glide, Giga Drain | Heavy Slam 55, Phantom Force 65, Power Whip 70 | Dhelmise |
| Glimmora | wild | 51 | Oxide | Rock Slide, Power Gem, Acid Armor, Sludge Wave | nothing | Glimmora |
| Glimmora | wild | 51 | v3 | Rock Slide, Power Gem, Acid Armor, Sludge Wave | Meteor Beam 71 | Glimmora |
| Heracross | wild | 51 to 53 | Oxide | Take Down, Close Combat, Reversal, Feint | Megahorn 55 | Heracross |
| Heracross | wild | 51 to 53 | v3 | Take Down, Close Combat, Reversal, Feint | Megahorn 55, Rock Slide 68 | Heracross |
| Weavile | wild | 51 to 52 | Oxide | Night Slash, Fling, Metal Claw, Dark Pulse | nothing | Weavile |
| Weavile | wild | 51 to 52 | v3 | Icy Wind, Night Slash, Fling, Dark Pulse | Assurance 69 | Weavile |
| Grapploct | wild | 52 | Oxide | Taunt, Reversal, Superpower, Topsy-Turvy | nothing | Grapploct |
| Grapploct | wild | 52 | v3 | Detect, Bulk Up, Taunt, Reversal | Brick Break 56 | Grapploct |
| Kricketune | wild | 53 | Oxide | Taunt, Night Slash, Bug Buzz, Perish Song | nothing | Kricketune |
| Kricketune | wild | 53 | v3 | Night Slash, Bug Buzz, Perish Song, Swords Dance | Brick Break 62 | Kricketune |
| Pawmot | wild | 53 | Oxide | Super Fang, Entrainment, Wild Charge, Close Combat | Mach Punch 55, Double Shock 61 | Pawmot |
| Pawmot | wild | 53 | v3 | Arm Thrust, Play Rough, Super Fang, Entrainment | Mach Punch 55, Close Combat 56, Wild Charge 57, Double Shock 61 | Pawmot |

## Turnback Cave

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 71 | At the cap |
|---|---|---|---|---|---|---|
| Giratina | static battle | 47 | Oxide | Ominous Wind, AncientPower, Dragon Claw, Shadow Force | Heal Block 50, Earth Power 60, Slash 70 | Giratina |
| Giratina | static battle | 47 | v3 | Ominous Wind, AncientPower, Dragon Claw, Shadow Force | Heal Block 50, Earthquake 56, Earth Power 60, Shadow Claw 63, Slash 70 | Giratina |

## Victory Road

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 71 | At the cap |
|---|---|---|---|---|---|---|
| Chinchou | old rod | 20 | Oxide | Flail, Water Gun, Confuse Ray, Spark | Take Down 23; as Lanturn: Stockpile 27, Swallow 27, Spit Up 27, BubbleBeam 30, Signal Beam 35, Discharge 40, Aqua Ring 47, Hydro Pump 52, Charge 57 | Lanturn (from 27) |
| Chinchou | old rod | 20 | v3 | Flail, Water Gun, Confuse Ray, Spark | Take Down 23; as Lanturn: Stockpile 27, Swallow 27, Spit Up 27, BubbleBeam 30, Signal Beam 35, Aqua Ring 47, Hydro Pump 52, Discharge 53, Charge 57, Thunder 65 | Lanturn (from 27) |
| Corphish | old rod | 20 | Oxide | Harden, ViceGrip, Leer, BubbleBeam | Protect 23, Knock Off 26; as Crawdaunt: Swift 30, Taunt 34, Night Slash 39, Crabhammer 44, Swords Dance 52, Crunch 57, Guillotine 65 | Crawdaunt (from 30) |
| Corphish | old rod | 20 | v3 | Harden, ViceGrip, Leer, BubbleBeam | Protect 23, Knock Off 26; as Crawdaunt: Swift 30, Taunt 34, Night Slash 39, Crabhammer 44, Swords Dance 52, Crunch 57, Cross Chop 63, Guillotine 65 | Crawdaunt (from 30) |
| Finneon | old rod | 21 | Oxide | Pound, Water Gun, Attract, Gust | Water Pulse 22, Captivate 26, Safeguard 29; as Lumineon: Aqua Ring 35, Whirlpool 42, U-turn 48, Bounce 53, Silver Wind 59 | Lumineon (from 31) |
| Finneon | old rod | 21 | v3 | Pound, Water Gun, Attract | Water Pulse 22, Captivate 26, Safeguard 29; as Lumineon: Aqua Ring 35, U-turn 48, Bounce 53, Silver Wind 59, Ice Fang 65 | Lumineon (from 31) |
| Goldeen | old rod | 21 to 22 | Oxide | Supersonic, Horn Attack, Water Pulse, Flail | Aqua Ring 27, Fury Attack 31; as Seaking: Waterfall 40, Horn Drill 47, Agility 56, Megahorn 63 | Seaking (from 33) |
| Goldeen | old rod | 21 to 22 | v3 | Supersonic, Horn Attack, Water Pulse, Flail | Aqua Ring 27; as Seaking: Waterfall 40, Horn Drill 47, Agility 56, Megahorn 63 | Seaking (from 33) |
| Goldeen | good rod | 32 | Oxide | Water Pulse, Flail, Aqua Ring, Fury Attack | as Seaking: Waterfall 40, Horn Drill 47, Agility 56, Megahorn 63 | Seaking (from 33) |
| Goldeen | good rod | 32 | v3 | Horn Attack, Water Pulse, Flail, Aqua Ring | as Seaking: Waterfall 40, Horn Drill 47, Agility 56, Megahorn 63 | Seaking (from 33) |
| Lumineon | good rod | 32 | Oxide | Gust, Water Pulse, Captivate, Safeguard | Aqua Ring 35, Whirlpool 42, U-turn 48, Bounce 53, Silver Wind 59 | Lumineon |
| Lumineon | good rod | 32 | v3 | Attract, Water Pulse, Captivate, Safeguard | Aqua Ring 35, U-turn 48, Bounce 53, Silver Wind 59, Ice Fang 65 | Lumineon |
| Barboach | good rod | 34 | Oxide | Water Pulse, Magnitude, Rest, Snore | Aqua Tail 35; as Whiscash: Aqua Tail 39, Earthquake 45, Future Sight 51, Fissure 57 | Whiscash (from 35) |
| Barboach | good rod | 34 | v3 | Amnesia, Water Pulse, Magnitude, Rest | Aqua Tail 35; as Whiscash: Aqua Tail 39, Earthquake 45, Future Sight 51, Fissure 57, Zen Headbutt 63 | Whiscash (from 35) |
| Feebas | good rod | 34 to 36 | Oxide | Splash, Tackle, Flail | as Milotic: Hydro Pump 37, Attract 41, Safeguard 45, Aqua Ring 49 | Milotic (from 35) |
| Feebas | good rod | 34 to 36 | v3 | Tackle, Water Gun, Flail | as Milotic: Hydro Pump 37, Attract 41, Safeguard 45, Aqua Ring 49 | Milotic (from 35) |
| Corphish | surf | 38 | Oxide | Knock Off, Taunt, Night Slash, Crabhammer | as Crawdaunt: Night Slash 39, Crabhammer 44, Swords Dance 52, Crunch 57, Guillotine 65 | Crawdaunt (from 39) |
| Corphish | surf | 38 | v3 | Knock Off, Taunt, Night Slash, Crabhammer | as Crawdaunt: Night Slash 39, Crabhammer 44, Swords Dance 52, Crunch 57, Cross Chop 63, Guillotine 65 | Crawdaunt (from 39) |
| Gastrodon | surf | 38 | Oxide | Water Pulse, Mud Bomb, Hidden Power, Body Slam | Muddy Water 41, Recover 54 | Gastrodon |
| Gastrodon | surf | 38 | v3 | Water Pulse, Mud Bomb, Hidden Power, Body Slam | Muddy Water 39, Earthquake 44, Recover 54, Rock Slide 64 | Gastrodon |
| Rhyperior | wild | 40 to 43 | Oxide | Scary Face, Rock Blast, Take Down, Horn Drill | Hammer Arm 42, Stone Edge 45, Earthquake 49, Megahorn 57, Rock Wrecker 61 | Rhyperior |
| Rhyperior | wild | 40 to 43 | v3 | Scary Face, Rock Blast, Take Down, Horn Drill | Hammer Arm 42, Stone Edge 45, Megahorn 56, Earthquake 60, Rock Wrecker 61 | Rhyperior |
| Absol | wild | 41 to 44 | Oxide | Bite, Double Team, Slash, Future Sight | Sucker Punch 44, Detect 49, Night Slash 52, Me First 57, Psycho Cut 60, Perish Song 65 | Absol |
| Absol | wild | 41 to 44 | v3 | Bite, Double Team, Slash, Future Sight | Sucker Punch 44, Detect 49, Me First 57, Psycho Cut 60, Perish Song 65 | Absol |
| Crustle | wild | 41 | both | Night Slash, X-Scissor, Rock Slide, StompingTantrum | Knock Off 45, Leech Life 48, Stone Edge 54, Rock Wrecker 61 | Crustle |
| Goldeen | surf | 41 | Oxide | Aqua Ring, Fury Attack, Waterfall, Horn Drill | as Seaking: Horn Drill 47, Agility 56, Megahorn 63 | Seaking (from 42) |
| Goldeen | surf | 41 | v3 | Flail, Aqua Ring, Waterfall, Horn Drill | as Seaking: Horn Drill 47, Agility 56, Megahorn 63 | Seaking (from 42) |
| Golem | wild | 41 | Oxide | Rollout, Rock Blast, Earthquake, Explosion | Double-Edge 44, Stone Edge 49 | Golem |
| Golem | wild | 41 | v3 | Selfdestruct, Rock Blast, Earthquake, Explosion | Double-Edge 44, Stone Edge 49, Steamroller 71 | Golem |
| Hariyama | wild | 41 to 42 | Oxide | SmellingSalt, Belly Drum, Force Palm, Seismic Toss | Wake-Up Slap 42, Endure 47, Close Combat 52, Reversal 57 | Hariyama |
| Hariyama | wild | 41 to 42 | v3 | SmellingSalt, Belly Drum, Force Palm, Seismic Toss | Wake-Up Slap 42, Endure 47, Reversal 57 | Hariyama |
| Hawlucha | wild | 41 to 42 | Oxide | Submission, Tailwind, Dual Wingbeat, Fly | Hi Jump Kick 42, Me First 48, Acrobatics 55, Close Combat 60 | Hawlucha |
| Hawlucha | wild | 41 to 42 | v3 | Sky Drop, Tailwind, Dual Wingbeat, Fly | Hi Jump Kick 42, Flying Press 44, Me First 48, Acrobatics 55, Close Combat 60 | Hawlucha |
| Jellicent | surf | 41 to 44 | Oxide | Confuse Ray, Hex, Brine, Pain Split | Destiny Bond 45, Shadow Ball 51, Scald 55, Water Spout 65, Recover 70 | Jellicent |
| Jellicent | surf | 41 to 44 | v3 | Confuse Ray, Hex, Brine, Pain Split | Destiny Bond 45, Shadow Ball 52, Scald 53, Water Spout 65, Recover 70 | Jellicent |
| Skarmory | wild | 41 to 44 | Oxide | Spikes, Metal Sound, Steel Wing, Air Slash | Slash 42, Night Slash 45 | Skarmory |
| Skarmory | wild | 41 to 44 | v3 | Spikes, Metal Sound, Steel Wing, Air Slash | Slash 42, Night Slash 45, Drill Run 68 | Skarmory |
| Steelix | wild | 41 to 44 | both | Rock Polish, DragonBreath, Curse, Iron Tail | Crunch 46, Double-Edge 49, Stone Edge 54 | Steelix |
| Bronzong | wild | 42 to 43 | Oxide | Iron Defense, Safeguard, Block, Gyro Ball | Future Sight 43, Faint Attack 50, Payback 61, Heal Block 67 | Bronzong |
| Bronzong | wild | 42 to 43 | v3 | Iron Defense, Safeguard, Block, Gyro Ball | Future Sight 43, Faint Attack 50, Earthquake 53, Payback 61, Heal Block 67 | Bronzong |
| Carbink | wild | 42 to 43 | both | Rock Polish, Rock Slide, Stealth Rock, Skill Swap | Light Screen 44, Power Gem 45, Moonblast 52, Stone Edge 54, Safeguard 70 | Carbink |
| Garganacl | wild | 42 | Oxide | Salt Cure, Recover, Rock Slide, Stealth Rock | Heavy Slam 44, Earthquake 49, Stone Edge 54, Explosion 60 | Garganacl |
| Garganacl | wild | 42 | v3 | Salt Cure, Recover, Rock Slide, Stealth Rock | Heavy Slam 44, Earthquake 49, Stone Edge 54, Explosion 60, Hammer Arm 68 | Garganacl |
| Gliscor | wild | 42 to 43 | Oxide | Night Slash, Swords Dance, U-turn, X-Scissor | Guillotine 45 | Gliscor |
| Gliscor | wild | 42 to 43 | v3 | Night Slash, Swords Dance, U-turn, X-Scissor | Guillotine 45, Earthquake 69 | Gliscor |
| Klefki | wild | 42 to 44 | Oxide | Mirror Shot, Flash Cannon, Foul Play, Play Rough | Magic Room 44, Heal Block 50, Last Resort 52 | Klefki |
| Klefki | wild | 42 to 44 | v3 | Recycle, Imprison, Foul Play, Play Rough | Magic Room 44, Heal Block 50, Mirror Shot 51, Last Resort 52, Dazzling Gleam 63 | Klefki |
| Mienshao | wild | 42 | Oxide | Drain Punch, Vacuum Wave, Aura Sphere, Me First | Jump Kick 45, Dual Chop 48, Focus Blast 51, Acrobatics 55, Hi Jump Kick 64 | Mienshao |
| Mienshao | wild | 42 | v3 | Bounce, Drain Punch, Vacuum Wave, Me First | Jump Kick 45, Dual Chop 48, Focus Blast 51, Acrobatics 55, Aura Sphere 56, Hi Jump Kick 64 | Mienshao |
| Probopass | wild | 42 to 44 | both | Magnet Bomb, Block, Thunder Wave, Rock Slide | Rest 43, Power Gem 49, Discharge 55, Stone Edge 61, Zap Cannon 67 | Probopass |
| Seaking | super rod | 42 | Oxide | Flail, Aqua Ring, Fury Attack, Waterfall | Horn Drill 47, Agility 56, Megahorn 63 | Seaking |
| Seaking | super rod | 42 | v3 | Water Pulse, Flail, Aqua Ring, Waterfall | Horn Drill 47, Agility 56, Megahorn 63 | Seaking |
| Whiscash | super rod | 42 | Oxide | Magnitude, Rest, Snore, Aqua Tail | Earthquake 45, Future Sight 51, Fissure 57 | Whiscash |
| Whiscash | super rod | 42 | v3 | Water Pulse, Magnitude, Rest, Aqua Tail | Earthquake 45, Future Sight 51, Fissure 57, Zen Headbutt 63 | Whiscash |
| Weavile | wild | 43 | Oxide | Icy Wind, Night Slash, Fling, Metal Claw | Dark Pulse 49 | Weavile |
| Weavile | wild | 43 | v3 | Nasty Plot, Icy Wind, Night Slash, Fling | Dark Pulse 49, Assurance 69 | Weavile |
| Crawdaunt | super rod | 45 to 48 | Oxide | Swift, Taunt, Night Slash, Crabhammer | Swords Dance 52, Crunch 57, Guillotine 65 | Crawdaunt |
| Crawdaunt | super rod | 45 to 48 | v3 | Swift, Taunt, Night Slash, Crabhammer | Swords Dance 52, Crunch 57, Cross Chop 63, Guillotine 65 | Crawdaunt |
| Milotic | super rod | 45 | both | Aqua Tail, Hydro Pump, Attract, Safeguard | Aqua Ring 49 | Milotic |

# Galactic's split: what each catch knows and learns

Written by `tools/oxide/balance/learncheck.py sheets` for check 6 of the learnset baseline (`docs/oxide/learnset-checks.md`). One table per capture area first offered in Galactic's split, whose cap is 65. Each Pokemon is read at the lowest level it is found at there. "Knows at capture" is the last four moves its list gives by that level; "learns by level-up" is every entry it reaches after capture up to 65, evolving on time, with each later stage's moves under its name; "at the cap" is the stage it can be by then and the next one after. A row marked v3 shows learnset v3 (unlanded, `origin/balance-learngen-v2`) where it differs from Oxide's lists; a row marked both is the same in each. Relearner-only moves and egg moves are left out. Nothing here is in the game data.

## Distortion World

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 65 | At the cap |
|---|---|---|---|---|---|---|
| Giratina | static battle | 47 | Oxide | Ominous Wind, AncientPower, Dragon Claw, Shadow Force | Heal Block 50, Earth Power 60 | Giratina |
| Giratina | static battle | 47 | v3 | Ominous Wind, AncientPower, Dragon Claw, Shadow Force | Heal Block 50, Earthquake 56, Earth Power 60, Shadow Claw 63 | Giratina |

## Mt. Coronet Mountainside

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 65 | At the cap |
|---|---|---|---|---|---|---|
| Snover | wild | 36 | Oxide | Mist, Ice Shard, Ingrain, Wood Hammer | as Abomasnow: Blizzard 47, Sheer Cold 58 | Abomasnow (from 40) |
| Snover | wild | 36 | v3 | Swagger, Mist, Ice Shard, Ingrain | Wood Hammer 39; as Abomasnow: Blizzard 47, Wood Hammer 53, Sheer Cold 58 | Abomasnow (from 40) |
| Dewgong | wild | 37 | Oxide | Aqua Jet, Brine, Sheer Cold, Take Down | Dive 41, Aqua Tail 43, Ice Beam 47, Safeguard 51 | Dewgong |
| Dewgong | wild | 37 | v3 | Aqua Jet, Brine, Sheer Cold, Take Down | Dive 41, Aqua Tail 43, Safeguard 51, Ice Beam 53 | Dewgong |
| Frosmoth | wild | 37 | Oxide | FeatherDance, Aurora Beam, Bug Buzz, Aurora Veil | Blizzard 40, Tailwind 44, Wide Guard 48, Quiver Dance 52 | Frosmoth |
| Frosmoth | wild | 37 | v3 | FeatherDance, Aurora Beam, Bug Buzz, Aurora Veil | Tailwind 44, Blizzard 45, Wide Guard 48, Quiver Dance 52 | Frosmoth |
| Hawlucha | wild | 37 | Oxide | Submission, Tailwind, Dual Wingbeat, Fly | Hi Jump Kick 42, Me First 48, Acrobatics 55, Close Combat 60 | Hawlucha |
| Hawlucha | wild | 37 | v3 | FeatherDance, Sky Drop, Tailwind, Dual Wingbeat | Fly 39, Hi Jump Kick 42, Flying Press 44, Me First 48, Acrobatics 55, Close Combat 60 | Hawlucha |
| Mienshao | wild | 37 | Oxide | Force Palm, Bounce, Drain Punch, Vacuum Wave | Aura Sphere 38, Me First 40, Jump Kick 45, Dual Chop 48, Focus Blast 51, Acrobatics 55, Hi Jump Kick 64 | Mienshao |
| Mienshao | wild | 37 | v3 | Force Palm, Bounce, Drain Punch, Vacuum Wave | Me First 40, Jump Kick 45, Dual Chop 48, Focus Blast 51, Acrobatics 55, Aura Sphere 56, Hi Jump Kick 64 | Mienshao |
| Sneasel | wild | 37 to 38 | Oxide | Fury Swipes, Agility, Icy Wind, Slash | as Weavile: Fling 38, Metal Claw 42, Dark Pulse 49 | Weavile (from 37) |
| Sneasel | wild | 37 to 38 | v3 | Fury Swipes, Agility, Icy Wind, Slash | as Weavile: Fling 38, Dark Pulse 49 | Weavile (from 37) |
| Snorunt | wild | 37 to 39 | Oxide | Protect, Ice Fang, Crunch, Ice Shard | as Glalie: Blizzard 51, Sheer Cold 59 | Glalie (from 42) |
| Snorunt | wild | 37 to 39 | Oxide | Protect, Ice Fang, Crunch, Ice Shard | as Froslass: Ice Shard 37, Blizzard 51, Destiny Bond 59 | Froslass (from 37) |
| Snorunt | wild | 37 to 39 | v3 | Protect, Ice Fang, Crunch, Ice Shard | as Glalie: Blizzard 51, Sheer Cold 59 | Glalie (from 42) |
| Snorunt | wild | 37 to 39 | v3 | Protect, Ice Fang, Crunch, Ice Shard | as Froslass: Ice Shard 37, Blizzard 51, Destiny Bond 59, Ice Beam 60 | Froslass (from 37) |
| Alolan Ninetales | wild | 38 | Oxide | Tail Whip, Disable, Ice Shard, Safeguard | nothing | Alolan Ninetales |
| Alolan Ninetales | wild | 38 | v3 | Safeguard, Icy Wind, Aurora Beam, Draining Kiss | Ice Beam 45 | Alolan Ninetales |
| Delibird | wild | 38 | Oxide | Present | nothing | Delibird |
| Delibird | wild | 38 | v3 | Present | Freeze-Dry 63 | Delibird |
| Garganacl | wild | 38 | both | Headbutt, Salt Cure, Recover, Rock Slide | Stealth Rock 40, Heavy Slam 44, Earthquake 49, Stone Edge 54, Explosion 60 | Garganacl |
| Donphan | wild | 39 | both | Slam, Fury Attack, Assurance, Scary Face | Earthquake 46, Giga Impact 54 | Donphan |
| Gliscor | wild | 39 | both | Screech, Night Slash, Swords Dance, U-turn | X-Scissor 42, Guillotine 45 | Gliscor |

## Mt. Coronet Peak

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 65 | At the cap |
|---|---|---|---|---|---|---|
| Bronzong | wild | 36 to 39 | Oxide | Extrasensory, Iron Defense, Safeguard, Block | Gyro Ball 38, Future Sight 43, Faint Attack 50, Payback 61 | Bronzong |
| Bronzong | wild | 36 to 39 | v3 | Extrasensory, Iron Defense, Safeguard, Block | Gyro Ball 38, Future Sight 43, Faint Attack 50, Earthquake 53, Payback 61 | Bronzong |
| Golbat | wild | 37 | Oxide | Wing Attack, Confuse Ray, Air Cutter, Mean Look | Poison Fang 39; as Crobat: Haze 45, Air Slash 51 | Crobat (from 40) |
| Golbat | wild | 37 | v3 | Wing Attack, Confuse Ray, Air Cutter, Mean Look | Poison Fang 39; as Crobat: Haze 45, Air Slash 51, Brave Bird 63 | Crobat (from 40) |
| Graveler | wild | 37 | Oxide | Selfdestruct, Rollout, Rock Blast, Earthquake | Explosion 38; as Golem: Double-Edge 44, Stone Edge 49 | Golem (from 40) |
| Graveler | wild | 37 | v3 | Rock Throw, Magnitude, Selfdestruct, Rock Blast | Explosion 38, Earthquake 39; as Golem: Double-Edge 44, Stone Edge 49 | Golem (from 40) |
| Hariyama | wild | 37 | Oxide | SmellingSalt, Belly Drum, Force Palm, Seismic Toss | Wake-Up Slap 42, Endure 47, Close Combat 52, Reversal 57 | Hariyama |
| Hariyama | wild | 37 | v3 | SmellingSalt, Belly Drum, Force Palm, Seismic Toss | Wake-Up Slap 42, Endure 47, Reversal 57 | Hariyama |
| Machoke | wild | 37 | Oxide | Revenge, Vital Throw, Submission, Wake-Up Slap | Cross Chop 40; as Machamp: Cross Chop 40, Scary Face 44, DynamicPunch 51 | Machamp (from 40) |
| Machoke | wild | 37 | v3 | Seismic Toss, Revenge, Vital Throw, Wake-Up Slap | as Machamp: Cross Chop 43, Scary Face 44, DynamicPunch 51 | Machamp (from 40) |
| Mienshao | wild | 37 | Oxide | Force Palm, Bounce, Drain Punch, Vacuum Wave | Aura Sphere 38, Me First 40, Jump Kick 45, Dual Chop 48, Focus Blast 51, Acrobatics 55, Hi Jump Kick 64 | Mienshao |
| Mienshao | wild | 37 | v3 | Force Palm, Bounce, Drain Punch, Vacuum Wave | Me First 40, Jump Kick 45, Dual Chop 48, Focus Blast 51, Acrobatics 55, Aura Sphere 56, Hi Jump Kick 64 | Mienshao |
| Naclstack | wild | 37 to 38 | Oxide | Headbutt, Iron Defense, Recover, Rock Slide | Stealth Rock 38; as Garganacl: Stealth Rock 40, Heavy Slam 44, Earthquake 49, Stone Edge 54, Explosion 60 | Garganacl (from 38) |
| Naclstack | wild | 37 to 38 | v3 | Headbutt, Iron Defense, Recover, Rock Slide | Stealth Rock 38; as Garganacl: Hammer Arm on evolving, Stealth Rock 40, Heavy Slam 44, Earthquake 49, Stone Edge 54, Explosion 60 | Garganacl (from 38) |
| Carbink | wild | 38 | both | AncientPower, Rock Polish, Rock Slide, Stealth Rock | Skill Swap 40, Light Screen 44, Power Gem 45, Moonblast 52, Stone Edge 54 | Carbink |
| Glimmora | wild | 38 | both | Stealth Rock, Venoshock, Selfdestruct, Rock Slide | Power Gem 39, Acid Armor 44, Sludge Wave 50 | Glimmora |
| Gliscor | wild | 39 | both | Screech, Night Slash, Swords Dance, U-turn | X-Scissor 42, Guillotine 45 | Gliscor |
| Klefki | wild | 39 | Oxide | Imprison, Mirror Shot, Flash Cannon, Foul Play | Play Rough 41, Magic Room 44, Heal Block 50, Last Resort 52 | Klefki |
| Klefki | wild | 39 | v3 | Draining Kiss, Recycle, Imprison, Foul Play | Play Rough 41, Magic Room 44, Heal Block 50, Mirror Shot 51, Last Resort 52, Dazzling Gleam 63 | Klefki |

## Resort Area

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 65 | At the cap |
|---|---|---|---|---|---|---|
| Luvdisc | old rod | 22 | Oxide | Agility, Take Down, Lucky Chant, Attract | Sweet Kiss 27; as Alomomola: Soak 33, Wish 37, Brine 41, Safeguard 45, Whirlpool 49, Helping Hand 53, Healing Wish 57, Wide Guard 61, Hydro Pump 65 | Alomomola (from 30) |
| Luvdisc | old rod | 22 | v3 | Agility, Take Down, Lucky Chant, Attract | Sweet Kiss 27; as Alomomola: Soak 33, Wish 37, Brine 41, Safeguard 45, Helping Hand 53, Healing Wish 57, Wide Guard 61, Hydro Pump 65 | Alomomola (from 30) |
| Tentacool | old rod | 22 | Oxide | Acid, Toxic Spikes, BubbleBeam, Wrap | Barrier 26, Water Pulse 29; as Tentacruel: Poison Jab 36, Screech 42, Hydro Pump 49, Wring Out 55 | Tentacruel (from 30) |
| Tentacool | old rod | 22 | v3 | Water Gun, Acid, Toxic Spikes, BubbleBeam | Barrier 26, Water Pulse 29; as Tentacruel: Poison Jab 36, Screech 42, Toxic 44, Hydro Pump 49, Wring Out 55 | Tentacruel (from 30) |
| Mantyke | old rod | 24 to 26 | both | BubbleBeam, Headbutt, Agility, Wing Attack | Water Pulse 28; as Mantine: Take Down 31, Confuse Ray 37, Bounce 40, Aqua Ring 46, Hydro Pump 49 | Mantine (from 30) |
| Remoraid | old rod | 24 | both | Psybeam, Aurora Beam, BubbleBeam, Focus Energy | as Octillery: Octazooka 25, Bullet Seed 29, Wring Out 36, Signal Beam 42, Ice Beam 48, Hyper Beam 55 | Octillery (from 25) |
| Luvdisc | good rod | 35 | Oxide | Lucky Chant, Attract, Sweet Kiss, Water Pulse | as Alomomola: Wish 37, Brine 41, Safeguard 45, Whirlpool 49, Helping Hand 53, Healing Wish 57, Wide Guard 61, Hydro Pump 65 | Alomomola (from 36) |
| Luvdisc | good rod | 35 | v3 | Lucky Chant, Attract, Sweet Kiss, Water Pulse | as Alomomola: Wish 37, Brine 41, Safeguard 45, Helping Hand 53, Healing Wish 57, Wide Guard 61, Hydro Pump 65 | Alomomola (from 36) |
| Mareanie | good rod | 35 | Oxide | Toxic Spikes, Recover, Spike Cannon, Pin Missile | Toxic 36; as Toxapex: Toxic 39, Venom Drench 42, Poison Jab 43, Liquidation 45 | Toxapex (from 38) |
| Mareanie | good rod | 35 | v3 | Toxic Spikes, Recover, Spike Cannon, Pin Missile | Toxic 36; as Toxapex: Baneful Bunker on evolving, Toxic 39, Venom Drench 42, Poison Jab 43, Liquidation 45 | Toxapex (from 38) |
| Mantyke | good rod | 37 | both | Wing Attack, Water Pulse, Take Down, Confuse Ray | as Mantine: Bounce 40, Aqua Ring 46, Hydro Pump 49 | Mantine (from 38) |
| Shellos | good rod | 37 | Oxide | Mud Bomb, Hidden Power, Body Slam, Muddy Water | as Gastrodon: Muddy Water 41, Recover 54 | Gastrodon (from 38) |
| Shellos | good rod | 37 | v3 | Mud Bomb, Hidden Power, Body Slam, Muddy Water | as Gastrodon: Muddy Water 39, Earthquake 44, Recover 54, Rock Slide 64 | Gastrodon (from 38) |
| Greninja | good rod | 39 | both | Low Kick, Waterfall, Fling, Scald | Dark Pulse 40, Extrasensory 43, Sludge Wave 47, Gunk Shot 51, Hydro Pump 55, Hydro Cannon 65 | Greninja |
| Gastrodon | surf | 40 | Oxide | Water Pulse, Mud Bomb, Hidden Power, Body Slam | Muddy Water 41, Recover 54 | Gastrodon |
| Gastrodon | surf | 40 | v3 | Mud Bomb, Hidden Power, Body Slam, Muddy Water | Earthquake 44, Recover 54, Rock Slide 64 | Gastrodon |
| Tentacool | surf | 40 | Oxide | Water Pulse, Poison Jab, Screech, Hydro Pump | as Tentacruel: Screech 42, Hydro Pump 49, Wring Out 55 | Tentacruel (from 41) |
| Tentacool | surf | 40 | v3 | Poison Jab, Screech, Toxic, Hydro Pump | as Tentacruel: Screech 42, Toxic 44, Hydro Pump 49, Wring Out 55 | Tentacruel (from 41) |
| Mantyke | surf | 43 | both | Water Pulse, Take Down, Confuse Ray, Bounce | as Mantine: Aqua Ring 46, Hydro Pump 49 | Mantine (from 44) |
| Shellos | surf | 43 | Oxide | Mud Bomb, Hidden Power, Body Slam, Muddy Water | as Gastrodon: Recover 54 | Gastrodon (from 44) |
| Shellos | surf | 43 | v3 | Mud Bomb, Hidden Power, Body Slam, Muddy Water | as Gastrodon: Earthquake 44, Recover 54, Rock Slide 64 | Gastrodon (from 44) |
| Jellicent | super rod | 45 | Oxide | Hex, Brine, Pain Split, Destiny Bond | Shadow Ball 51, Scald 55, Water Spout 65 | Jellicent |
| Jellicent | super rod | 45 | v3 | Hex, Brine, Pain Split, Destiny Bond | Shadow Ball 52, Scald 53, Water Spout 65 | Jellicent |
| Lanturn | super rod | 45 | Oxide | Spit Up, BubbleBeam, Signal Beam, Discharge | Aqua Ring 47, Hydro Pump 52, Charge 57 | Lanturn |
| Lanturn | super rod | 45 | v3 | Swallow, Spit Up, BubbleBeam, Signal Beam | Aqua Ring 47, Hydro Pump 52, Discharge 53, Charge 57, Thunder 65 | Lanturn |
| Greninja | surf | 46 | both | Fling, Scald, Dark Pulse, Extrasensory | Sludge Wave 47, Gunk Shot 51, Hydro Pump 55, Hydro Cannon 65 | Greninja |
| Gorebyss | super rod | 48 | Oxide | Baton Pass, Dive, Psychic, Aqua Tail | Hydro Pump 51 | Gorebyss |
| Gorebyss | super rod | 48 | v3 | Baton Pass, Dive, Psychic, Aqua Tail | Hydro Pump 51, Ice Beam 65 | Gorebyss |
| Lumineon | super rod | 48 | Oxide | Safeguard, Aqua Ring, Whirlpool, U-turn | Bounce 53, Silver Wind 59 | Lumineon |
| Lumineon | super rod | 48 | v3 | Captivate, Safeguard, Aqua Ring, U-turn | Bounce 53, Silver Wind 59, Ice Fang 65 | Lumineon |
| Kingdra | super rod | 51 | both | Twister, Brine, Hydro Pump, Dragon Dance | Dragon Pulse 57 | Kingdra |

## Route 225

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 65 | At the cap |
|---|---|---|---|---|---|---|
| Chinchou | old rod | 22 | Oxide | Flail, Water Gun, Confuse Ray, Spark | Take Down 23; as Lanturn: Stockpile 27, Swallow 27, Spit Up 27, BubbleBeam 30, Signal Beam 35, Discharge 40, Aqua Ring 47, Hydro Pump 52, Charge 57 | Lanturn (from 27) |
| Chinchou | old rod | 22 | v3 | Flail, Water Gun, Confuse Ray, Spark | Take Down 23; as Lanturn: Stockpile 27, Swallow 27, Spit Up 27, BubbleBeam 30, Signal Beam 35, Aqua Ring 47, Hydro Pump 52, Discharge 53, Charge 57, Thunder 65 | Lanturn (from 27) |
| Goldeen | old rod | 22 | Oxide | Supersonic, Horn Attack, Water Pulse, Flail | Aqua Ring 27, Fury Attack 31; as Seaking: Waterfall 40, Horn Drill 47, Agility 56, Megahorn 63 | Seaking (from 33) |
| Goldeen | old rod | 22 | v3 | Supersonic, Horn Attack, Water Pulse, Flail | Aqua Ring 27; as Seaking: Waterfall 40, Horn Drill 47, Agility 56, Megahorn 63 | Seaking (from 33) |
| Buizel | old rod | 24 | Oxide | Water Gun, Pursuit, Swift, Aqua Jet | as Floatzel: Crunch 26, Agility 29, Whirlpool 39, Razor Wind 50 | Floatzel (from 26) |
| Buizel | old rod | 24 | v3 | Water Gun, Pursuit, Swift, Aqua Jet | as Floatzel: Crunch 26, Agility 29 | Floatzel (from 26) |
| Carvanha | old rod | 24 | Oxide | Scary Face, Ice Fang, Screech, Swagger | Assurance 26, Crunch 28; as Sharpedo: Slash 30, Aqua Jet 34, Taunt 40, Agility 45, Skull Bash 50, Night Slash 56 | Sharpedo (from 30) |
| Carvanha | old rod | 24 | v3 | Focus Energy, Scary Face, Screech, Swagger | Assurance 26, Crunch 28; as Sharpedo: Slash 30, Aqua Jet 34, Taunt 40, Agility 45, Night Slash 56, Liquidation 63 | Sharpedo (from 30) |
| Tentacool | old rod | 26 | Oxide | Toxic Spikes, BubbleBeam, Wrap, Barrier | Water Pulse 29; as Tentacruel: Poison Jab 36, Screech 42, Hydro Pump 49, Wring Out 55 | Tentacruel (from 30) |
| Tentacool | old rod | 26 | v3 | Acid, Toxic Spikes, BubbleBeam, Barrier | Water Pulse 29; as Tentacruel: Poison Jab 36, Screech 42, Toxic 44, Hydro Pump 49, Wring Out 55 | Tentacruel (from 30) |
| Ludicolo | good rod | 35 | Oxide | Astonish, Growl, Mega Drain, Nature Power | nothing | Ludicolo |
| Ludicolo | good rod | 35 | v3 | Growl, Mega Drain, Nature Power | Hydro Pump 45 | Ludicolo |
| Wooper | good rod | 35 | Oxide | Mud Bomb, Amnesia, Yawn, Earthquake | as Quagsire: Earthquake 36, Mist 48, Haze 48, Muddy Water 53 | Quagsire (from 36) |
| Wooper | good rod | 35 | Oxide | Mud Bomb, Amnesia, Yawn, Earthquake | as Clodsire: Megahorn 36, Toxic 40, Earthquake 48, Recover 55 | Clodsire (from 35) |
| Wooper | good rod | 35 | v3 | Amnesia, Yawn, Muddy Water, Sludge Bomb | as Quagsire: Earthquake 44, Mist 48, Haze 48, Muddy Water 53, Ice Punch 62 | Quagsire (from 36) |
| Wooper | good rod | 35 | v3 | Amnesia, Yawn, Muddy Water, Sludge Bomb | as Clodsire: Poison Jab 36, Slam 37, Megahorn 39, Sludge Bomb 39, Toxic 40, Haze 43, Earthquake 44, Recover 55 | Clodsire (from 35) |
| Shellos | good rod | 37 | Oxide | Mud Bomb, Hidden Power, Body Slam, Muddy Water | as Gastrodon: Muddy Water 41, Recover 54 | Gastrodon (from 38) |
| Shellos | good rod | 37 | v3 | Mud Bomb, Hidden Power, Body Slam, Muddy Water | as Gastrodon: Muddy Water 39, Earthquake 44, Recover 54, Rock Slide 64 | Gastrodon (from 38) |
| Surskit | good rod | 37 | both | BubbleBeam, Agility, Mist, Haze | as Masquerain: Silver Wind 40, Air Slash 47, Whirlwind 54, Bug Buzz 61 | Masquerain (from 38) |
| Sharpedo | good rod | 39 | Oxide | Assurance, Crunch, Slash, Aqua Jet | Taunt 40, Agility 45, Skull Bash 50, Night Slash 56 | Sharpedo |
| Sharpedo | good rod | 39 | v3 | Assurance, Crunch, Slash, Aqua Jet | Taunt 40, Agility 45, Night Slash 56, Liquidation 63 | Sharpedo |
| Gastrodon | surf | 40 | Oxide | Water Pulse, Mud Bomb, Hidden Power, Body Slam | Muddy Water 41, Recover 54 | Gastrodon |
| Gastrodon | surf | 40 | v3 | Mud Bomb, Hidden Power, Body Slam, Muddy Water | Earthquake 44, Recover 54, Rock Slide 64 | Gastrodon |
| Masquerain | surf | 40 | Oxide | Gust, Scary Face, Stun Spore, Silver Wind | Air Slash 47, Whirlwind 54, Bug Buzz 61 | Masquerain |
| Masquerain | surf | 40 | v3 | Water Sport, Scary Face, Stun Spore, Silver Wind | Air Slash 47, Whirlwind 54, Bug Buzz 61 | Masquerain |
| Buizel | surf | 43 | Oxide | Swift, Aqua Jet, Agility, Whirlpool | as Floatzel: Razor Wind 50 | Floatzel (from 44) |
| Buizel | surf | 43 | v3 | Pursuit, Swift, Aqua Jet, Agility | nothing | Floatzel (from 44) |
| Shellos | surf | 43 | Oxide | Mud Bomb, Hidden Power, Body Slam, Muddy Water | as Gastrodon: Recover 54 | Gastrodon (from 44) |
| Shellos | surf | 43 | v3 | Mud Bomb, Hidden Power, Body Slam, Muddy Water | as Gastrodon: Earthquake 44, Recover 54, Rock Slide 64 | Gastrodon (from 44) |
| Ludicolo | super rod | 45 | Oxide | Astonish, Growl, Mega Drain, Nature Power | nothing | Ludicolo |
| Ludicolo | super rod | 45 | v3 | Growl, Mega Drain, Nature Power, Hydro Pump | nothing | Ludicolo |
| Quagsire | super rod | 45 | Oxide | Mud Bomb, Amnesia, Yawn, Earthquake | Mist 48, Haze 48, Muddy Water 53 | Quagsire |
| Quagsire | super rod | 45 | v3 | Mud Bomb, Amnesia, Yawn, Earthquake | Mist 48, Haze 48, Muddy Water 53, Ice Punch 62 | Quagsire |
| Seaking | surf | 46 | Oxide | Flail, Aqua Ring, Fury Attack, Waterfall | Horn Drill 47, Agility 56, Megahorn 63 | Seaking |
| Seaking | surf | 46 | v3 | Water Pulse, Flail, Aqua Ring, Waterfall | Horn Drill 47, Agility 56, Megahorn 63 | Seaking |
| Hariyama | wild | 47 | Oxide | Force Palm, Seismic Toss, Wake-Up Slap, Endure | Close Combat 52, Reversal 57 | Hariyama |
| Hariyama | wild | 47 | v3 | Force Palm, Seismic Toss, Wake-Up Slap, Endure | Reversal 57 | Hariyama |
| Corviknight | wild | 48 | both | FeatherDance, Revenge, Defog, Iron Head | Brave Bird 49, Body Press 55, Roost 65 | Corviknight |
| Garganacl | wild | 48 | both | Recover, Rock Slide, Stealth Rock, Heavy Slam | Earthquake 49, Stone Edge 54, Explosion 60 | Garganacl |
| Gastrodon | super rod | 48 | Oxide | Mud Bomb, Hidden Power, Body Slam, Muddy Water | Recover 54 | Gastrodon |
| Gastrodon | super rod | 48 | v3 | Hidden Power, Body Slam, Muddy Water, Earthquake | Recover 54, Rock Slide 64 | Gastrodon |
| Houndoom | wild | 48 | Oxide | Fire Fang, Faint Attack, Embargo, Flamethrower | Crunch 54, Nasty Plot 60 | Houndoom |
| Houndoom | wild | 48 | v3 | Odor Sleuth, Fire Fang, Faint Attack, Embargo | Flamethrower 53, Crunch 54, Dark Pulse 56, Nasty Plot 60 | Houndoom |
| Liepard | wild | 48 | both | Sucker Punch, Nasty Plot, Night Slash, Snatch | Play Rough 54 | Liepard |
| Mienshao | wild | 48 | Oxide | Aura Sphere, Me First, Jump Kick, Dual Chop | Focus Blast 51, Acrobatics 55, Hi Jump Kick 64 | Mienshao |
| Mienshao | wild | 48 | v3 | Vacuum Wave, Me First, Jump Kick, Dual Chop | Focus Blast 51, Acrobatics 55, Aura Sphere 56, Hi Jump Kick 64 | Mienshao |
| Seaking | super rod | 48 | Oxide | Aqua Ring, Fury Attack, Waterfall, Horn Drill | Agility 56, Megahorn 63 | Seaking |
| Seaking | super rod | 48 | v3 | Flail, Aqua Ring, Waterfall, Horn Drill | Agility 56, Megahorn 63 | Seaking |
| Talonflame | wild | 48 | Oxide | Natural Gift, Acrobatics, Me First, Tailwind | Flare Blitz 51, Brave Bird 55 | Talonflame |
| Talonflame | wild | 48 | v3 | Natural Gift, Acrobatics, Me First, Tailwind | Flare Blitz 64, Brave Bird 65 | Talonflame |
| Toucannon | wild | 48 | Oxide | Screech, Drill Peck, Bullet Seed, FeatherDance | Hyper Voice 50 | Toucannon |
| Toucannon | wild | 48 | v3 | Fury Attack, Screech, Bullet Seed, FeatherDance | Hyper Voice 56, Rock Blast 65 | Toucannon |
| Donphan | wild | 49 | both | Fury Attack, Assurance, Scary Face, Earthquake | Giga Impact 54 | Donphan |
| Dubwool | wild | 49 | Oxide | Take Down, Guard Swap, Reversal, Cotton Guard | Double-Edge 50, Last Resort 56 | Dubwool |
| Dubwool | wild | 49 | v3 | Guard Swap, Reversal, Take Down, Cotton Guard | Double-Edge 50, Last Resort 56 | Dubwool |
| Golem | wild | 49 | both | Earthquake, Explosion, Double-Edge, Stone Edge | nothing | Golem |
| Hawlucha | wild | 49 | Oxide | Dual Wingbeat, Fly, Hi Jump Kick, Me First | Acrobatics 55, Close Combat 60 | Hawlucha |
| Hawlucha | wild | 49 | v3 | Fly, Hi Jump Kick, Flying Press, Me First | Acrobatics 55, Close Combat 60 | Hawlucha |
| Grapploct | wild | 50 | Oxide | Taunt, Reversal, Superpower, Topsy-Turvy | nothing | Grapploct |
| Grapploct | wild | 50 | v3 | Detect, Bulk Up, Taunt, Reversal | Brick Break 56 | Grapploct |
| Honchkrow | wild | 50 | Oxide | Wing Attack, Swagger, Nasty Plot, Night Slash | Dark Pulse 55 | Honchkrow |
| Honchkrow | wild | 50 | v3 | Swagger, Assurance, Faint Attack, Nasty Plot | nothing | Honchkrow |
| Ninetales | wild | 50 | Oxide | Quick Attack, Confuse Ray, Safeguard, Flare Blitz | nothing | Ninetales |
| Ninetales | wild | 50 | v3 | Confuse Ray, Safeguard, Flare Blitz, Fire Blast | nothing | Ninetales |
| Greninja | super rod | 51 | both | Dark Pulse, Extrasensory, Sludge Wave, Gunk Shot | Hydro Pump 55, Hydro Cannon 65 | Greninja |

## Route 226

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 65 | At the cap |
|---|---|---|---|---|---|---|
| Meloetta | in-game trade | 1 | Oxide | Round, Quick Attack, Confusion, Sing | Quick Attack 6, Confusion 11, Sing 16, Teeter Dance 21, Acrobatics 26, Psybeam 31, Echoed Voice 36, U-turn 43, Wake-Up Slap 50, Psychic 57, Hyper Voice 64 | Meloetta |
| Meloetta | in-game trade | 1 | v3 | Round, Quick Attack, Confusion, Sing | Quick Attack 6, Confusion 11, Sing 16, Teeter Dance 21, Acrobatics 26, Psybeam 31, Psychic 39, U-turn 43, Wake-Up Slap 50, Hyper Voice 64 | Meloetta |
| Mantyke | old rod | 22 | both | BubbleBeam, Headbutt, Agility, Wing Attack | Water Pulse 28; as Mantine: Take Down 31, Confuse Ray 37, Bounce 40, Aqua Ring 46, Hydro Pump 49 | Mantine (from 30) |
| Psyduck | old rod | 22 | both | Water Gun, Disable, Confusion, Water Pulse | Fury Swipes 27, Screech 31; as Golduck: Psych Up 37, Zen Headbutt 44, Amnesia 50, Hydro Pump 56 | Golduck (from 33) |
| Finneon | old rod | 24 | Oxide | Water Gun, Attract, Gust, Water Pulse | Captivate 26, Safeguard 29; as Lumineon: Aqua Ring 35, Whirlpool 42, U-turn 48, Bounce 53, Silver Wind 59 | Lumineon (from 31) |
| Finneon | old rod | 24 | v3 | Pound, Water Gun, Attract, Water Pulse | Captivate 26, Safeguard 29; as Lumineon: Aqua Ring 35, U-turn 48, Bounce 53, Silver Wind 59, Ice Fang 65 | Lumineon (from 31) |
| Shellos | old rod | 24 | Oxide | Harden, Water Pulse, Mud Bomb, Hidden Power | Body Slam 29; as Gastrodon: Muddy Water 41, Recover 54 | Gastrodon (from 30) |
| Shellos | old rod | 24 | v3 | Harden, Water Pulse, Mud Bomb, Hidden Power | Body Slam 29; as Gastrodon: Muddy Water 39, Earthquake 44, Recover 54, Rock Slide 64 | Gastrodon (from 30) |
| Carvanha | old rod | 26 | Oxide | Ice Fang, Screech, Swagger, Assurance | Crunch 28; as Sharpedo: Slash 30, Aqua Jet 34, Taunt 40, Agility 45, Skull Bash 50, Night Slash 56 | Sharpedo (from 30) |
| Carvanha | old rod | 26 | v3 | Scary Face, Screech, Swagger, Assurance | Crunch 28; as Sharpedo: Slash 30, Aqua Jet 34, Taunt 40, Agility 45, Night Slash 56, Liquidation 63 | Sharpedo (from 30) |
| Lanturn | good rod | 35 | Oxide | Swallow, Spit Up, BubbleBeam, Signal Beam | Discharge 40, Aqua Ring 47, Hydro Pump 52, Charge 57 | Lanturn |
| Lanturn | good rod | 35 | v3 | Swallow, Spit Up, BubbleBeam, Signal Beam | Aqua Ring 47, Hydro Pump 52, Discharge 53, Charge 57, Thunder 65 | Lanturn |
| Mareanie | good rod | 35 | Oxide | Toxic Spikes, Recover, Spike Cannon, Pin Missile | Toxic 36; as Toxapex: Toxic 39, Venom Drench 42, Poison Jab 43, Liquidation 45 | Toxapex (from 38) |
| Mareanie | good rod | 35 | v3 | Toxic Spikes, Recover, Spike Cannon, Pin Missile | Toxic 36; as Toxapex: Baneful Bunker on evolving, Toxic 39, Venom Drench 42, Poison Jab 43, Liquidation 45 | Toxapex (from 38) |
| Finneon | good rod | 37 | Oxide | Water Pulse, Captivate, Safeguard, Aqua Ring | Whirlpool 38; as Lumineon: Whirlpool 42, U-turn 48, Bounce 53, Silver Wind 59 | Lumineon (from 38) |
| Finneon | good rod | 37 | v3 | Water Pulse, Captivate, Safeguard, Aqua Ring | as Lumineon: U-turn 48, Bounce 53, Silver Wind 59, Ice Fang 65 | Lumineon (from 38) |
| Tentacool | good rod | 37 | Oxide | Barrier, Water Pulse, Poison Jab, Screech | as Tentacruel: Screech 42, Hydro Pump 49, Wring Out 55 | Tentacruel (from 38) |
| Tentacool | good rod | 37 | v3 | Barrier, Water Pulse, Poison Jab, Screech | as Tentacruel: Screech 42, Toxic 44, Hydro Pump 49, Wring Out 55 | Tentacruel (from 38) |
| Greninja | good rod | 39 | both | Low Kick, Waterfall, Fling, Scald | Dark Pulse 40, Extrasensory 43, Sludge Wave 47, Gunk Shot 51, Hydro Pump 55, Hydro Cannon 65 | Greninja |
| Floatzel | surf | 40 | Oxide | Aqua Jet, Crunch, Agility, Whirlpool | Razor Wind 50 | Floatzel |
| Floatzel | surf | 40 | v3 | Swift, Aqua Jet, Crunch, Agility | nothing | Floatzel |
| Mareanie | surf | 40 | Oxide | Spike Cannon, Pin Missile, Toxic, Venom Drench | Liquidation 41, Poison Jab 41; as Toxapex: Venom Drench 42, Poison Jab 43, Liquidation 45 | Toxapex (from 41) |
| Mareanie | surf | 40 | v3 | Spike Cannon, Pin Missile, Toxic, Venom Drench | Liquidation 41, Poison Jab 41; as Toxapex: Baneful Bunker on evolving, Venom Drench 42, Poison Jab 43, Liquidation 45 | Toxapex (from 41) |
| Mantine | surf | 43 | both | Water Pulse, Take Down, Confuse Ray, Bounce | Aqua Ring 46, Hydro Pump 49 | Mantine |
| Tentacruel | surf | 43 | Oxide | Barrier, Water Pulse, Poison Jab, Screech | Hydro Pump 49, Wring Out 55 | Tentacruel |
| Tentacruel | surf | 43 | v3 | Barrier, Water Pulse, Poison Jab, Screech | Toxic 44, Hydro Pump 49, Wring Out 55 | Tentacruel |
| Mantine | super rod | 45 | both | Water Pulse, Take Down, Confuse Ray, Bounce | Aqua Ring 46, Hydro Pump 49 | Mantine |
| Toxapex | super rod | 45 | both | Toxic, Venom Drench, Poison Jab, Liquidation | nothing | Toxapex |
| Greninja | surf | 46 | both | Fling, Scald, Dark Pulse, Extrasensory | Sludge Wave 47, Gunk Shot 51, Hydro Pump 55, Hydro Cannon 65 | Greninja |
| Corviknight | wild | 47 to 50 | both | FeatherDance, Revenge, Defog, Iron Head | Brave Bird 49, Body Press 55, Roost 65 | Corviknight |
| Absol | wild | 48 | Oxide | Double Team, Slash, Future Sight, Sucker Punch | Detect 49, Night Slash 52, Me First 57, Psycho Cut 60, Perish Song 65 | Absol |
| Absol | wild | 48 | v3 | Double Team, Slash, Future Sight, Sucker Punch | Detect 49, Me First 57, Psycho Cut 60, Perish Song 65 | Absol |
| Altaria | wild | 48 | both | Natural Gift, DragonBreath, Dragon Dance, Refresh | Dragon Pulse 54, Perish Song 62 | Altaria |
| Araquanid | wild | 48 to 49 | Oxide | Soak, Dive, Lunge, Scald | Hydro Pump 51, Liquidation 55, Leech Life 61 | Araquanid |
| Araquanid | wild | 48 to 49 | v3 | Headbutt, Soak, Dive, Lunge | Hydro Pump 51, Liquidation 55, Scald 60, Leech Life 61 | Araquanid |
| Mienshao | wild | 48 | Oxide | Aura Sphere, Me First, Jump Kick, Dual Chop | Focus Blast 51, Acrobatics 55, Hi Jump Kick 64 | Mienshao |
| Mienshao | wild | 48 | v3 | Vacuum Wave, Me First, Jump Kick, Dual Chop | Focus Blast 51, Acrobatics 55, Aura Sphere 56, Hi Jump Kick 64 | Mienshao |
| Poliwrath | super rod | 48 | Oxide | Hypnosis, DoubleSlap, Submission, DynamicPunch | Mind Reader 53 | Poliwrath |
| Poliwrath | super rod | 48 | v3 | BubbleBeam, Hypnosis, DoubleSlap, DynamicPunch | Mind Reader 53 | Poliwrath |
| Relicanth | super rod | 48 | Oxide | Yawn, Take Down, Mud Sport, AncientPower | Double-Edge 50, Dive 57, Rest 64 | Relicanth |
| Relicanth | super rod | 48 | v3 | Take Down, Mud Sport, Dive, AncientPower | Double-Edge 50, Earthquake 53, Rest 64 | Relicanth |
| Skarmory | wild | 48 to 49 | both | Steel Wing, Air Slash, Slash, Night Slash | nothing | Skarmory |
| Talonflame | wild | 48 | Oxide | Natural Gift, Acrobatics, Me First, Tailwind | Flare Blitz 51, Brave Bird 55 | Talonflame |
| Talonflame | wild | 48 | v3 | Natural Gift, Acrobatics, Me First, Tailwind | Flare Blitz 64, Brave Bird 65 | Talonflame |
| Toucannon | wild | 48 to 49 | Oxide | Screech, Drill Peck, Bullet Seed, FeatherDance | Hyper Voice 50 | Toucannon |
| Toucannon | wild | 48 to 49 | v3 | Fury Attack, Screech, Bullet Seed, FeatherDance | Hyper Voice 56, Rock Blast 65 | Toucannon |
| Carbink | wild | 49 | both | Stealth Rock, Skill Swap, Light Screen, Power Gem | Moonblast 52, Stone Edge 54 | Carbink |
| Floatzel | wild | 50 | Oxide | Crunch, Agility, Whirlpool, Razor Wind | nothing | Floatzel |
| Floatzel | wild | 50 | v3 | Swift, Aqua Jet, Crunch, Agility | nothing | Floatzel |
| Shellos | wild | 50 | Oxide | Hidden Power, Body Slam, Muddy Water, Recover | as Gastrodon: Recover 54 | Gastrodon (from 51) |
| Shellos | wild | 50 | v3 | Hidden Power, Body Slam, Muddy Water, Recover | as Gastrodon: Recover 54, Rock Slide 64 | Gastrodon (from 51) |
| Kingdra | super rod | 51 | both | Twister, Brine, Hydro Pump, Dragon Dance | Dragon Pulse 57 | Kingdra |

## Route 227

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 65 | At the cap |
|---|---|---|---|---|---|---|
| Chinchou | old rod | 22 | Oxide | Flail, Water Gun, Confuse Ray, Spark | Take Down 23; as Lanturn: Stockpile 27, Swallow 27, Spit Up 27, BubbleBeam 30, Signal Beam 35, Discharge 40, Aqua Ring 47, Hydro Pump 52, Charge 57 | Lanturn (from 27) |
| Chinchou | old rod | 22 | v3 | Flail, Water Gun, Confuse Ray, Spark | Take Down 23; as Lanturn: Stockpile 27, Swallow 27, Spit Up 27, BubbleBeam 30, Signal Beam 35, Aqua Ring 47, Hydro Pump 52, Discharge 53, Charge 57, Thunder 65 | Lanturn (from 27) |
| Tentacool | old rod | 22 | Oxide | Acid, Toxic Spikes, BubbleBeam, Wrap | Barrier 26, Water Pulse 29; as Tentacruel: Poison Jab 36, Screech 42, Hydro Pump 49, Wring Out 55 | Tentacruel (from 30) |
| Tentacool | old rod | 22 | v3 | Water Gun, Acid, Toxic Spikes, BubbleBeam | Barrier 26, Water Pulse 29; as Tentacruel: Poison Jab 36, Screech 42, Toxic 44, Hydro Pump 49, Wring Out 55 | Tentacruel (from 30) |
| Barboach | old rod | 24 | Oxide | Water Gun, Mud Bomb, Amnesia, Water Pulse | Magnitude 26; as Whiscash: Rest 33, Snore 33, Aqua Tail 39, Earthquake 45, Future Sight 51, Fissure 57 | Whiscash (from 30) |
| Barboach | old rod | 24 | v3 | Water Gun, Mud Bomb, Amnesia, Water Pulse | Magnitude 26; as Whiscash: Rest 33, Aqua Tail 39, Earthquake 45, Future Sight 51, Fissure 57, Zen Headbutt 63 | Whiscash (from 30) |
| Goldeen | old rod | 24 | Oxide | Supersonic, Horn Attack, Water Pulse, Flail | Aqua Ring 27, Fury Attack 31; as Seaking: Waterfall 40, Horn Drill 47, Agility 56, Megahorn 63 | Seaking (from 33) |
| Goldeen | old rod | 24 | v3 | Supersonic, Horn Attack, Water Pulse, Flail | Aqua Ring 27; as Seaking: Waterfall 40, Horn Drill 47, Agility 56, Megahorn 63 | Seaking (from 33) |
| Frogadier | old rod | 26 | Oxide | Icy Wind, Faint Attack, Acrobatics, Low Kick | Waterfall 30, Fling 35; as Greninja: Scald 37, Dark Pulse 40, Extrasensory 43, Sludge Wave 47, Gunk Shot 51, Hydro Pump 55, Hydro Cannon 65 | Greninja (from 36) |
| Frogadier | old rod | 26 | v3 | Icy Wind, Faint Attack, Acrobatics, Low Kick | Fling 35; as Greninja: Water Shuriken on evolving, Night Slash on evolving, Scald 37, Dark Pulse 40, Extrasensory 43, Sludge Wave 47, Gunk Shot 51, Hydro Pump 55, Hydro Cannon 65 | Greninja (from 36) |
| Goldeen | good rod | 35 | Oxide | Water Pulse, Flail, Aqua Ring, Fury Attack | as Seaking: Waterfall 40, Horn Drill 47, Agility 56, Megahorn 63 | Seaking (from 36) |
| Goldeen | good rod | 35 | v3 | Horn Attack, Water Pulse, Flail, Aqua Ring | as Seaking: Waterfall 40, Horn Drill 47, Agility 56, Megahorn 63 | Seaking (from 36) |
| Golduck | good rod | 35 | both | Confusion, Water Pulse, Fury Swipes, Screech | Psych Up 37, Zen Headbutt 44, Amnesia 50, Hydro Pump 56 | Golduck |
| Barboach | good rod | 37 | Oxide | Magnitude, Rest, Snore, Aqua Tail | as Whiscash: Aqua Tail 39, Earthquake 45, Future Sight 51, Fissure 57 | Whiscash (from 38) |
| Barboach | good rod | 37 | v3 | Water Pulse, Magnitude, Rest, Aqua Tail | as Whiscash: Aqua Tail 39, Earthquake 45, Future Sight 51, Fissure 57, Zen Headbutt 63 | Whiscash (from 38) |
| Feebas | good rod | 37 | Oxide | Splash, Tackle, Flail | as Milotic: Attract 41, Safeguard 45, Aqua Ring 49 | Milotic (from 38) |
| Feebas | good rod | 37 | v3 | Tackle, Water Gun, Flail | as Milotic: Attract 41, Safeguard 45, Aqua Ring 49 | Milotic (from 38) |
| Starmie | good rod | 39 | Oxide | Rapid Spin, Recover, Swift, Confuse Ray | nothing | Starmie |
| Starmie | good rod | 39 | v3 | Rapid Spin, Recover, Swift, Confuse Ray | Light Screen 42, Hydro Pump 60 | Starmie |
| Feebas | surf | 40 | Oxide | Splash, Tackle, Flail | as Milotic: Attract 41, Safeguard 45, Aqua Ring 49 | Milotic (from 41) |
| Feebas | surf | 40 | v3 | Tackle, Water Gun, Flail | as Milotic: Attract 41, Safeguard 45, Aqua Ring 49 | Milotic (from 41) |
| Gastrodon | surf | 40 | Oxide | Water Pulse, Mud Bomb, Hidden Power, Body Slam | Muddy Water 41, Recover 54 | Gastrodon |
| Gastrodon | surf | 40 | v3 | Mud Bomb, Hidden Power, Body Slam, Muddy Water | Earthquake 44, Recover 54, Rock Slide 64 | Gastrodon |
| Corphish | surf | 43 | Oxide | Knock Off, Taunt, Night Slash, Crabhammer | Swords Dance 44; as Crawdaunt: Crabhammer 44, Swords Dance 52, Crunch 57, Guillotine 65 | Crawdaunt (from 44) |
| Corphish | surf | 43 | v3 | Knock Off, Taunt, Night Slash, Crabhammer | Swords Dance 44; as Crawdaunt: Crabhammer 44, Swords Dance 52, Crunch 57, Cross Chop 63, Guillotine 65 | Crawdaunt (from 44) |
| Goldeen | surf | 43 | Oxide | Aqua Ring, Fury Attack, Waterfall, Horn Drill | as Seaking: Horn Drill 47, Agility 56, Megahorn 63 | Seaking (from 44) |
| Goldeen | surf | 43 | v3 | Flail, Aqua Ring, Waterfall, Horn Drill | as Seaking: Horn Drill 47, Agility 56, Megahorn 63 | Seaking (from 44) |
| Seaking | super rod | 45 | Oxide | Flail, Aqua Ring, Fury Attack, Waterfall | Horn Drill 47, Agility 56, Megahorn 63 | Seaking |
| Seaking | super rod | 45 | v3 | Water Pulse, Flail, Aqua Ring, Waterfall | Horn Drill 47, Agility 56, Megahorn 63 | Seaking |
| Whiscash | super rod | 45 | Oxide | Rest, Snore, Aqua Tail, Earthquake | Future Sight 51, Fissure 57 | Whiscash |
| Whiscash | super rod | 45 | v3 | Magnitude, Rest, Aqua Tail, Earthquake | Future Sight 51, Fissure 57, Zen Headbutt 63 | Whiscash |
| Corsola | surf | 46 | Oxide | AncientPower, Aqua Ring, Spike Cannon, Power Gem | Mirror Coat 48, Earth Power 53 | Corsola |
| Corsola | surf | 46 | v3 | Rock Blast, Aqua Ring, Spike Cannon, Power Gem | Mirror Coat 48, Earth Power 53, Aqua Cutter 63 | Corsola |
| Crawdaunt | super rod | 48 | Oxide | Swift, Taunt, Night Slash, Crabhammer | Swords Dance 52, Crunch 57, Guillotine 65 | Crawdaunt |
| Crawdaunt | super rod | 48 | v3 | Swift, Taunt, Night Slash, Crabhammer | Swords Dance 52, Crunch 57, Cross Chop 63, Guillotine 65 | Crawdaunt |
| Milotic | super rod | 48 | both | Aqua Tail, Hydro Pump, Attract, Safeguard | Aqua Ring 49 | Milotic |
| Ceruledge | wild | 51 | Oxide | Lava Plume, Swords Dance, Ally Switch, Bitter Blade | Psycho Cut 56, Flare Blitz 62 | Ceruledge |
| Ceruledge | wild | 51 | v3 | Incinerate, Lava Plume, Swords Dance, Bitter Blade | Psycho Cut 56, Flare Blitz 62 | Ceruledge |
| Sharpedo | super rod | 51 | Oxide | Aqua Jet, Taunt, Agility, Skull Bash | Night Slash 56 | Sharpedo |
| Sharpedo | super rod | 51 | v3 | Slash, Aqua Jet, Taunt, Agility | Night Slash 56, Liquidation 63 | Sharpedo |
| Houndoom | wild | 52 to 53 | Oxide | Fire Fang, Faint Attack, Embargo, Flamethrower | Crunch 54, Nasty Plot 60 | Houndoom |
| Houndoom | wild | 52 to 53 | v3 | Odor Sleuth, Fire Fang, Faint Attack, Embargo | Flamethrower 53, Crunch 54, Dark Pulse 56, Nasty Plot 60 | Houndoom |
| Ninetales | wild | 52 | Oxide | Quick Attack, Confuse Ray, Safeguard, Flare Blitz | nothing | Ninetales |
| Ninetales | wild | 52 | v3 | Confuse Ray, Safeguard, Flare Blitz, Fire Blast | nothing | Ninetales |
| Rapidash | wild | 52 | Oxide | Agility, Fire Blast, Fury Attack, Bounce | Flare Blitz 56 | Rapidash |
| Rapidash | wild | 52 | v3 | Take Down, Agility, Fire Blast, Bounce | Flare Blitz 56 | Rapidash |
| Rhyperior | wild | 52 | Oxide | Horn Drill, Hammer Arm, Stone Edge, Earthquake | Megahorn 57, Rock Wrecker 61 | Rhyperior |
| Rhyperior | wild | 52 | v3 | Take Down, Horn Drill, Hammer Arm, Stone Edge | Megahorn 56, Earthquake 60, Rock Wrecker 61 | Rhyperior |
| Salazzle | wild | 52 to 53 | Oxide | Venoshock, Flamethrower, Sludge Bomb, Dragon Pulse | Fire Blast 55 | Salazzle |
| Salazzle | wild | 52 to 53 | v3 | Flame Burst, Dragon Rage, Toxic, Venoshock | Dragon Pulse 53, Flamethrower 54, Fire Blast 55, Sludge Bomb 56 | Salazzle |
| Skarmory | wild | 52 | both | Steel Wing, Air Slash, Slash, Night Slash | nothing | Skarmory |
| Weezing | wild | 52 | both | Haze, Double Hit, Explosion, Sludge Bomb | Destiny Bond 55, Memento 63 | Weezing |
| Magcargo | wild | 53 | both | Amnesia, Lava Plume, Rock Slide, Body Slam | Flamethrower 61 | Magcargo |
| Turtonator | wild | 53 | Oxide | Body Slam, Flamethrower, Dragon Pulse, Fire Spin | Explosion 55, Overheat 61 | Turtonator |
| Turtonator | wild | 53 | v3 | Rapid Spin, Body Slam, Flamethrower, Dragon Pulse | Explosion 55, Overheat 61 | Turtonator |
| Chatot | wild | 54 | Oxide | Roost, Uproar, FeatherDance, Hyper Voice | nothing | Chatot |
| Chatot | wild | 54 | v3 | Roost, Uproar, FeatherDance, Hyper Voice | Air Slash 63 | Chatot |
| Garganacl | wild | 54 | both | Stealth Rock, Heavy Slam, Earthquake, Stone Edge | Explosion 60 | Garganacl |
| Honchkrow | wild | 54 | Oxide | Wing Attack, Swagger, Nasty Plot, Night Slash | Dark Pulse 55 | Honchkrow |
| Honchkrow | wild | 54 | v3 | Swagger, Assurance, Faint Attack, Nasty Plot | nothing | Honchkrow |

## Route 228

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 65 | At the cap |
|---|---|---|---|---|---|---|
| Buizel | old rod | 22 | Oxide | Water Gun, Pursuit, Swift, Aqua Jet | as Floatzel: Crunch 26, Agility 29, Whirlpool 39, Razor Wind 50 | Floatzel (from 26) |
| Buizel | old rod | 22 | v3 | Water Gun, Pursuit, Swift, Aqua Jet | as Floatzel: Crunch 26, Agility 29 | Floatzel (from 26) |
| Goldeen | old rod | 22 | Oxide | Supersonic, Horn Attack, Water Pulse, Flail | Aqua Ring 27, Fury Attack 31; as Seaking: Waterfall 40, Horn Drill 47, Agility 56, Megahorn 63 | Seaking (from 33) |
| Goldeen | old rod | 22 | v3 | Supersonic, Horn Attack, Water Pulse, Flail | Aqua Ring 27; as Seaking: Waterfall 40, Horn Drill 47, Agility 56, Megahorn 63 | Seaking (from 33) |
| Barboach | old rod | 24 | Oxide | Water Gun, Mud Bomb, Amnesia, Water Pulse | Magnitude 26; as Whiscash: Rest 33, Snore 33, Aqua Tail 39, Earthquake 45, Future Sight 51, Fissure 57 | Whiscash (from 30) |
| Barboach | old rod | 24 | v3 | Water Gun, Mud Bomb, Amnesia, Water Pulse | Magnitude 26; as Whiscash: Rest 33, Aqua Tail 39, Earthquake 45, Future Sight 51, Fissure 57, Zen Headbutt 63 | Whiscash (from 30) |
| Krabby | old rod | 24 | both | Harden, BubbleBeam, Mud Shot, Metal Claw | Stomp 25; as Kingler: Protect 32, Guillotine 37, Slam 44, Brine 51, Crabhammer 56, Flail 63 | Kingler (from 28) |
| Clamperl | old rod | 26 | Oxide | Clamp, Water Gun, Whirlpool, Iron Defense | as Huntail: Brine 28, Baton Pass 33, Dive 37, Crunch 42, Aqua Tail 46, Hydro Pump 51 | Huntail (from 26) |
| Clamperl | old rod | 26 | Oxide | Clamp, Water Gun, Whirlpool, Iron Defense | as Gorebyss: Captivate 28, Baton Pass 33, Dive 37, Psychic 42, Aqua Tail 46, Hydro Pump 51 | Gorebyss (from 26) |
| Clamperl | old rod | 26 | v3 | Water Gun, Iron Defense | as Huntail: Brine 28, Ice Fang 32, Baton Pass 33, Dive 37, Crunch 42, Aqua Tail 46, Hydro Pump 51, Body Slam 65 | Huntail (from 26) |
| Clamperl | old rod | 26 | v3 | Water Gun, Iron Defense | as Gorebyss: Captivate 28, Baton Pass 33, Dive 37, Psychic 42, Aqua Tail 46, Hydro Pump 51, Ice Beam 65 | Gorebyss (from 26) |
| Gastrodon | good rod | 35 | Oxide | Water Pulse, Mud Bomb, Hidden Power, Body Slam | Muddy Water 41, Recover 54 | Gastrodon |
| Gastrodon | good rod | 35 | v3 | Water Pulse, Mud Bomb, Hidden Power, Body Slam | Muddy Water 39, Earthquake 44, Recover 54, Rock Slide 64 | Gastrodon |
| Goldeen | good rod | 35 | Oxide | Water Pulse, Flail, Aqua Ring, Fury Attack | as Seaking: Waterfall 40, Horn Drill 47, Agility 56, Megahorn 63 | Seaking (from 36) |
| Goldeen | good rod | 35 | v3 | Horn Attack, Water Pulse, Flail, Aqua Ring | as Seaking: Waterfall 40, Horn Drill 47, Agility 56, Megahorn 63 | Seaking (from 36) |
| Barboach | good rod | 37 | Oxide | Magnitude, Rest, Snore, Aqua Tail | as Whiscash: Aqua Tail 39, Earthquake 45, Future Sight 51, Fissure 57 | Whiscash (from 38) |
| Barboach | good rod | 37 | v3 | Water Pulse, Magnitude, Rest, Aqua Tail | as Whiscash: Aqua Tail 39, Earthquake 45, Future Sight 51, Fissure 57, Zen Headbutt 63 | Whiscash (from 38) |
| Corphish | good rod | 37 | Oxide | Protect, Knock Off, Taunt, Night Slash | Crabhammer 38; as Crawdaunt: Night Slash 39, Crabhammer 44, Swords Dance 52, Crunch 57, Guillotine 65 | Crawdaunt (from 38) |
| Corphish | good rod | 37 | v3 | Protect, Knock Off, Taunt, Night Slash | Crabhammer 38; as Crawdaunt: Night Slash 39, Crabhammer 44, Swords Dance 52, Crunch 57, Cross Chop 63, Guillotine 65 | Crawdaunt (from 38) |
| Masquerain | good rod | 39 | Oxide | Water Sport, Gust, Scary Face, Stun Spore | Silver Wind 40, Air Slash 47, Whirlwind 54, Bug Buzz 61 | Masquerain |
| Masquerain | good rod | 39 | v3 | Sweet Scent, Water Sport, Scary Face, Stun Spore | Silver Wind 40, Air Slash 47, Whirlwind 54, Bug Buzz 61 | Masquerain |
| Gastrodon | surf | 40 | Oxide | Water Pulse, Mud Bomb, Hidden Power, Body Slam | Muddy Water 41, Recover 54 | Gastrodon |
| Gastrodon | surf | 40 | v3 | Mud Bomb, Hidden Power, Body Slam, Muddy Water | Earthquake 44, Recover 54, Rock Slide 64 | Gastrodon |
| Quagsire | surf | 40 | Oxide | Mud Bomb, Amnesia, Yawn, Earthquake | Mist 48, Haze 48, Muddy Water 53 | Quagsire |
| Quagsire | surf | 40 | v3 | Slam, Mud Bomb, Amnesia, Yawn | Earthquake 44, Mist 48, Haze 48, Muddy Water 53, Ice Punch 62 | Quagsire |
| Ludicolo | surf | 43 | Oxide | Astonish, Growl, Mega Drain, Nature Power | nothing | Ludicolo |
| Ludicolo | surf | 43 | v3 | Growl, Mega Drain, Nature Power | Hydro Pump 45 | Ludicolo |
| Masquerain | surf | 43 | Oxide | Gust, Scary Face, Stun Spore, Silver Wind | Air Slash 47, Whirlwind 54, Bug Buzz 61 | Masquerain |
| Masquerain | surf | 43 | v3 | Water Sport, Scary Face, Stun Spore, Silver Wind | Air Slash 47, Whirlwind 54, Bug Buzz 61 | Masquerain |
| Seaking | super rod | 45 | Oxide | Flail, Aqua Ring, Fury Attack, Waterfall | Horn Drill 47, Agility 56, Megahorn 63 | Seaking |
| Seaking | super rod | 45 | v3 | Water Pulse, Flail, Aqua Ring, Waterfall | Horn Drill 47, Agility 56, Megahorn 63 | Seaking |
| Whiscash | super rod | 45 | Oxide | Rest, Snore, Aqua Tail, Earthquake | Future Sight 51, Fissure 57 | Whiscash |
| Whiscash | super rod | 45 | v3 | Magnitude, Rest, Aqua Tail, Earthquake | Future Sight 51, Fissure 57, Zen Headbutt 63 | Whiscash |
| Tentacruel | surf | 46 | Oxide | Barrier, Water Pulse, Poison Jab, Screech | Hydro Pump 49, Wring Out 55 | Tentacruel |
| Tentacruel | surf | 46 | v3 | Water Pulse, Poison Jab, Screech, Toxic | Hydro Pump 49, Wring Out 55 | Tentacruel |
| Crawdaunt | super rod | 48 | Oxide | Swift, Taunt, Night Slash, Crabhammer | Swords Dance 52, Crunch 57, Guillotine 65 | Crawdaunt |
| Crawdaunt | super rod | 48 | v3 | Swift, Taunt, Night Slash, Crabhammer | Swords Dance 52, Crunch 57, Cross Chop 63, Guillotine 65 | Crawdaunt |
| Lanturn | super rod | 48 | Oxide | BubbleBeam, Signal Beam, Discharge, Aqua Ring | Hydro Pump 52, Charge 57 | Lanturn |
| Lanturn | super rod | 48 | v3 | Spit Up, BubbleBeam, Signal Beam, Aqua Ring | Hydro Pump 52, Discharge 53, Charge 57, Thunder 65 | Lanturn |
| Whiscash | wild | 49 | Oxide | Rest, Snore, Aqua Tail, Earthquake | Future Sight 51, Fissure 57 | Whiscash |
| Whiscash | wild | 49 | v3 | Magnitude, Rest, Aqua Tail, Earthquake | Future Sight 51, Fissure 57, Zen Headbutt 63 | Whiscash |
| Crustle | wild | 50 | both | Rock Slide, StompingTantrum, Knock Off, Leech Life | Stone Edge 54, Rock Wrecker 61 | Crustle |
| Donphan | wild | 50 to 51 | both | Fury Attack, Assurance, Scary Face, Earthquake | Giga Impact 54 | Donphan |
| Flygon | wild | 50 | Oxide | Supersonic, DragonBreath, Screech, Dragon Claw | Hyper Beam 57 | Flygon |
| Flygon | wild | 50 | v3 | Supersonic, DragonBreath, Screech, Dragon Claw | Dragon Pulse 53, Hyper Beam 57 | Flygon |
| Golem | wild | 50 | both | Earthquake, Explosion, Double-Edge, Stone Edge | nothing | Golem |
| Houndoom | wild | 50 | Oxide | Fire Fang, Faint Attack, Embargo, Flamethrower | Crunch 54, Nasty Plot 60 | Houndoom |
| Houndoom | wild | 50 | v3 | Odor Sleuth, Fire Fang, Faint Attack, Embargo | Flamethrower 53, Crunch 54, Dark Pulse 56, Nasty Plot 60 | Houndoom |
| Palossand | wild | 50 | both | Giga Drain, Iron Defense, Shadow Ball, Earth Power | Shore Up 57 | Palossand |
| Glimmora | wild | 51 | both | Rock Slide, Power Gem, Acid Armor, Sludge Wave | nothing | Glimmora |
| Masquerain | super rod | 51 | both | Scary Face, Stun Spore, Silver Wind, Air Slash | Whirlwind 54, Bug Buzz 61 | Masquerain |
| Rhyperior | wild | 51 | Oxide | Horn Drill, Hammer Arm, Stone Edge, Earthquake | Megahorn 57, Rock Wrecker 61 | Rhyperior |
| Rhyperior | wild | 51 | v3 | Take Down, Horn Drill, Hammer Arm, Stone Edge | Megahorn 56, Earthquake 60, Rock Wrecker 61 | Rhyperior |
| Salazzle | wild | 51 | Oxide | Venoshock, Flamethrower, Sludge Bomb, Dragon Pulse | Fire Blast 55 | Salazzle |
| Salazzle | wild | 51 | v3 | Flame Burst, Dragon Rage, Toxic, Venoshock | Dragon Pulse 53, Flamethrower 54, Fire Blast 55, Sludge Bomb 56 | Salazzle |
| Carbink | wild | 52 | both | Skill Swap, Light Screen, Power Gem, Moonblast | Stone Edge 54 | Carbink |
| Garganacl | wild | 52 | both | Rock Slide, Stealth Rock, Heavy Slam, Earthquake | Stone Edge 54, Explosion 60 | Garganacl |
| Steelix | wild | 52 | both | Curse, Iron Tail, Crunch, Double-Edge | Stone Edge 54 | Steelix |

## Route 229

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 65 | At the cap |
|---|---|---|---|---|---|---|
| Barboach | old rod | 22 | Oxide | Water Gun, Mud Bomb, Amnesia, Water Pulse | Magnitude 26; as Whiscash: Rest 33, Snore 33, Aqua Tail 39, Earthquake 45, Future Sight 51, Fissure 57 | Whiscash (from 30) |
| Barboach | old rod | 22 | v3 | Water Gun, Mud Bomb, Amnesia, Water Pulse | Magnitude 26; as Whiscash: Rest 33, Aqua Tail 39, Earthquake 45, Future Sight 51, Fissure 57, Zen Headbutt 63 | Whiscash (from 30) |
| Goldeen | old rod | 22 | Oxide | Supersonic, Horn Attack, Water Pulse, Flail | Aqua Ring 27, Fury Attack 31; as Seaking: Waterfall 40, Horn Drill 47, Agility 56, Megahorn 63 | Seaking (from 33) |
| Goldeen | old rod | 22 | v3 | Supersonic, Horn Attack, Water Pulse, Flail | Aqua Ring 27; as Seaking: Waterfall 40, Horn Drill 47, Agility 56, Megahorn 63 | Seaking (from 33) |
| Corphish | old rod | 24 | Oxide | ViceGrip, Leer, BubbleBeam, Protect | Knock Off 26; as Crawdaunt: Swift 30, Taunt 34, Night Slash 39, Crabhammer 44, Swords Dance 52, Crunch 57, Guillotine 65 | Crawdaunt (from 30) |
| Corphish | old rod | 24 | v3 | ViceGrip, Leer, BubbleBeam, Protect | Knock Off 26; as Crawdaunt: Swift 30, Taunt 34, Night Slash 39, Crabhammer 44, Swords Dance 52, Crunch 57, Cross Chop 63, Guillotine 65 | Crawdaunt (from 30) |
| Poliwag | old rod | 24 | Oxide | Hypnosis, Water Gun, DoubleSlap, Body Slam | BubbleBeam 25; as Poliwrath: DynamicPunch 43, Mind Reader 53 | Poliwrath (from 25) |
| Poliwag | old rod | 24 | Oxide | Hypnosis, Water Gun, DoubleSlap, Body Slam | BubbleBeam 25; as Politoed: Swagger 27, Bounce 37, Hyper Voice 48 | Politoed (from 25) |
| Poliwag | old rod | 24 | v3 | Hypnosis, Water Gun, DoubleSlap, Body Slam | BubbleBeam 25; as Poliwrath: DynamicPunch 43, Mind Reader 53 | Poliwrath (from 25) |
| Poliwag | old rod | 24 | v3 | Hypnosis, Water Gun, DoubleSlap, Body Slam | BubbleBeam 25; as Politoed: Swagger 27, Bounce 37, Hyper Voice 48, Hydro Pump 49 | Politoed (from 25) |
| Masquerain | old rod | 26 | Oxide | Sweet Scent, Water Sport, Gust, Scary Face | Stun Spore 33, Silver Wind 40, Air Slash 47, Whirlwind 54, Bug Buzz 61 | Masquerain |
| Masquerain | old rod | 26 | v3 | Quick Attack, Sweet Scent, Water Sport, Scary Face | Stun Spore 33, Silver Wind 40, Air Slash 47, Whirlwind 54, Bug Buzz 61 | Masquerain |
| Barboach | good rod | 35 | Oxide | Magnitude, Rest, Snore, Aqua Tail | as Whiscash: Aqua Tail 39, Earthquake 45, Future Sight 51, Fissure 57 | Whiscash (from 36) |
| Barboach | good rod | 35 | v3 | Water Pulse, Magnitude, Rest, Aqua Tail | as Whiscash: Aqua Tail 39, Earthquake 45, Future Sight 51, Fissure 57, Zen Headbutt 63 | Whiscash (from 36) |
| Goldeen | good rod | 35 | Oxide | Water Pulse, Flail, Aqua Ring, Fury Attack | as Seaking: Waterfall 40, Horn Drill 47, Agility 56, Megahorn 63 | Seaking (from 36) |
| Goldeen | good rod | 35 | v3 | Horn Attack, Water Pulse, Flail, Aqua Ring | as Seaking: Waterfall 40, Horn Drill 47, Agility 56, Megahorn 63 | Seaking (from 36) |
| Chinchou | good rod | 37 | Oxide | Take Down, BubbleBeam, Signal Beam, Discharge | as Lanturn: Discharge 40, Aqua Ring 47, Hydro Pump 52, Charge 57 | Lanturn (from 38) |
| Chinchou | good rod | 37 | v3 | Spark, Take Down, BubbleBeam, Signal Beam | Discharge 38; as Lanturn: Aqua Ring 47, Hydro Pump 52, Discharge 53, Charge 57, Thunder 65 | Lanturn (from 38) |
| Corphish | good rod | 37 | Oxide | Protect, Knock Off, Taunt, Night Slash | Crabhammer 38; as Crawdaunt: Night Slash 39, Crabhammer 44, Swords Dance 52, Crunch 57, Guillotine 65 | Crawdaunt (from 38) |
| Corphish | good rod | 37 | v3 | Protect, Knock Off, Taunt, Night Slash | Crabhammer 38; as Crawdaunt: Night Slash 39, Crabhammer 44, Swords Dance 52, Crunch 57, Cross Chop 63, Guillotine 65 | Crawdaunt (from 38) |
| Ludicolo | good rod | 39 | Oxide | Astonish, Growl, Mega Drain, Nature Power | nothing | Ludicolo |
| Ludicolo | good rod | 39 | v3 | Growl, Mega Drain, Nature Power | Hydro Pump 45 | Ludicolo |
| Ludicolo | surf | 40 | Oxide | Astonish, Growl, Mega Drain, Nature Power | nothing | Ludicolo |
| Ludicolo | surf | 40 | v3 | Growl, Mega Drain, Nature Power | Hydro Pump 45 | Ludicolo |
| Quagsire | surf | 40 | Oxide | Mud Bomb, Amnesia, Yawn, Earthquake | Mist 48, Haze 48, Muddy Water 53 | Quagsire |
| Quagsire | surf | 40 | v3 | Slam, Mud Bomb, Amnesia, Yawn | Earthquake 44, Mist 48, Haze 48, Muddy Water 53, Ice Punch 62 | Quagsire |
| Goldeen | surf | 43 | Oxide | Aqua Ring, Fury Attack, Waterfall, Horn Drill | as Seaking: Horn Drill 47, Agility 56, Megahorn 63 | Seaking (from 44) |
| Goldeen | surf | 43 | v3 | Flail, Aqua Ring, Waterfall, Horn Drill | as Seaking: Horn Drill 47, Agility 56, Megahorn 63 | Seaking (from 44) |
| Masquerain | surf | 43 | Oxide | Gust, Scary Face, Stun Spore, Silver Wind | Air Slash 47, Whirlwind 54, Bug Buzz 61 | Masquerain |
| Masquerain | surf | 43 | v3 | Water Sport, Scary Face, Stun Spore, Silver Wind | Air Slash 47, Whirlwind 54, Bug Buzz 61 | Masquerain |
| Crawdaunt | super rod | 45 | Oxide | Swift, Taunt, Night Slash, Crabhammer | Swords Dance 52, Crunch 57, Guillotine 65 | Crawdaunt |
| Crawdaunt | super rod | 45 | v3 | Swift, Taunt, Night Slash, Crabhammer | Swords Dance 52, Crunch 57, Cross Chop 63, Guillotine 65 | Crawdaunt |
| Whiscash | super rod | 45 | Oxide | Rest, Snore, Aqua Tail, Earthquake | Future Sight 51, Fissure 57 | Whiscash |
| Whiscash | super rod | 45 | v3 | Magnitude, Rest, Aqua Tail, Earthquake | Future Sight 51, Fissure 57, Zen Headbutt 63 | Whiscash |
| Whiscash | surf | 46 | Oxide | Rest, Snore, Aqua Tail, Earthquake | Future Sight 51, Fissure 57 | Whiscash |
| Whiscash | surf | 46 | v3 | Magnitude, Rest, Aqua Tail, Earthquake | Future Sight 51, Fissure 57, Zen Headbutt 63 | Whiscash |
| Heracross | wild | 47 | Oxide | Counter, Take Down, Close Combat, Reversal | Feint 49, Megahorn 55 | Heracross |
| Heracross | wild | 47 | v3 | Brick Break, Take Down, Close Combat, Reversal | Feint 49, Megahorn 55 | Heracross |
| Galvantula | wild | 48 | Oxide | Signal Beam, Energy Ball, Sucker Punch, Thunderbolt | Bug Buzz 51, Thunder 55, Volt Switch 65 | Galvantula |
| Galvantula | wild | 48 | v3 | Discharge, Signal Beam, Sucker Punch, Thunderbolt | Bug Buzz 51, Energy Ball 53, Thunder 55, Volt Switch 65 | Galvantula |
| Lanturn | super rod | 48 | Oxide | BubbleBeam, Signal Beam, Discharge, Aqua Ring | Hydro Pump 52, Charge 57 | Lanturn |
| Lanturn | super rod | 48 | v3 | Spit Up, BubbleBeam, Signal Beam, Aqua Ring | Hydro Pump 52, Discharge 53, Charge 57, Thunder 65 | Lanturn |
| Leavanny | wild | 48 | Oxide | Leaf Blade, X-Scissor, Entrainment, Swords Dance | Leaf Storm 50 | Leavanny |
| Leavanny | wild | 48 | v3 | Helping Hand, X-Scissor, Entrainment, Swords Dance | Leaf Storm 50, Leaf Blade 53 | Leavanny |
| Liepard | wild | 48 | both | Sucker Punch, Nasty Plot, Night Slash, Snatch | Play Rough 54 | Liepard |
| Lopunny | wild | 48 | both | Agility, Dizzy Punch, Charm, Bounce | Healing Wish 53 | Lopunny |
| Mightyena | wild | 48 | both | Crunch, Scary Face, Taunt, Embargo | Take Down 52, Thief 57, Sucker Punch 62 | Mightyena |
| Roserade | wild | 48 | Oxide | Poison Sting, Mega Drain, Magical Leaf, Sweet Scent | nothing | Roserade |
| Roserade | wild | 48 | v3 | Poison Sting, Mega Drain, Magical Leaf, Sweet Scent | Sludge Bomb 60 | Roserade |
| Sharpedo | super rod | 48 | Oxide | Slash, Aqua Jet, Taunt, Agility | Skull Bash 50, Night Slash 56 | Sharpedo |
| Sharpedo | super rod | 48 | v3 | Slash, Aqua Jet, Taunt, Agility | Night Slash 56, Liquidation 63 | Sharpedo |
| Talonflame | wild | 48 | Oxide | Natural Gift, Acrobatics, Me First, Tailwind | Flare Blitz 51, Brave Bird 55 | Talonflame |
| Talonflame | wild | 48 | v3 | Natural Gift, Acrobatics, Me First, Tailwind | Flare Blitz 64, Brave Bird 65 | Talonflame |
| Arboliva | wild | 49 | Oxide | Seed Bomb, Energy Ball, Leech Seed, Terrain Pulse | Petal Blizzard 52, Petal Dance 58 | Arboliva |
| Arboliva | wild | 49 | v3 | Flail, Mega Drain, Leech Seed, Seed Bomb | Energy Ball 53, Petal Dance 58, Petal Blizzard 60 | Arboliva |
| Emolga | wild | 49 | both | Acrobatics, Encore, Light Screen, Volt Switch | Discharge 50, Agility 50 | Emolga |
| Tsareena | wild | 49 | Oxide | Low Sweep, Aromatherapy, Leaf Storm, Power Whip | Hi Jump Kick 55 | Tsareena |
| Tsareena | wild | 49 | v3 | Trop Kick, Low Sweep, Aromatherapy, Power Whip | Hi Jump Kick 55, Leaf Storm 60 | Tsareena |
| Vespiquen | wild | 49 | Oxide | Captivate, Attack Order, Swagger, Destiny Bond | nothing | Vespiquen |
| Vespiquen | wild | 49 | v3 | Captivate, Swagger, Attack Order, Destiny Bond | nothing | Vespiquen |
| Cherrim | wild | 50 | Oxide | Worry Seed, Take Down, SolarBeam, Lucky Chant | nothing | Cherrim |
| Cherrim | wild | 50 | v3 | Take Down, Leaf Blade, SolarBeam, Lucky Chant | nothing | Cherrim |
| Jumpluff | wild | 50 | Oxide | U-turn, Worry Seed, Giga Drain, Bounce | Memento 52 | Jumpluff |
| Jumpluff | wild | 50 | v3 | Cotton Spore, U-turn, Worry Seed, Giga Drain | Memento 52, Bounce 53, Bullet Seed 62 | Jumpluff |
| Vikavolt | wild | 50 | Oxide | Bite, Spark, Signal Beam, Discharge | Bug Buzz 55, Thunderbolt 65 | Vikavolt |
| Vikavolt | wild | 50 | v3 | Spark, Crunch, Signal Beam, Discharge | Bug Buzz 53, X-Scissor 53, Thunderbolt 65 | Vikavolt |
| Greninja | super rod | 51 | both | Dark Pulse, Extrasensory, Sludge Wave, Gunk Shot | Hydro Pump 55, Hydro Cannon 65 | Greninja |

## Route 230

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 65 | At the cap |
|---|---|---|---|---|---|---|
| Remoraid | old rod | 22 | both | Lock-On, Psybeam, Aurora Beam, BubbleBeam | Focus Energy 23; as Octillery: Octazooka 25, Bullet Seed 29, Wring Out 36, Signal Beam 42, Ice Beam 48, Hyper Beam 55 | Octillery (from 25) |
| Tentacool | old rod | 22 | Oxide | Acid, Toxic Spikes, BubbleBeam, Wrap | Barrier 26, Water Pulse 29; as Tentacruel: Poison Jab 36, Screech 42, Hydro Pump 49, Wring Out 55 | Tentacruel (from 30) |
| Tentacool | old rod | 22 | v3 | Water Gun, Acid, Toxic Spikes, BubbleBeam | Barrier 26, Water Pulse 29; as Tentacruel: Poison Jab 36, Screech 42, Toxic 44, Hydro Pump 49, Wring Out 55 | Tentacruel (from 30) |
| Barboach | old rod | 24 | Oxide | Water Gun, Mud Bomb, Amnesia, Water Pulse | Magnitude 26; as Whiscash: Rest 33, Snore 33, Aqua Tail 39, Earthquake 45, Future Sight 51, Fissure 57 | Whiscash (from 30) |
| Barboach | old rod | 24 | v3 | Water Gun, Mud Bomb, Amnesia, Water Pulse | Magnitude 26; as Whiscash: Rest 33, Aqua Tail 39, Earthquake 45, Future Sight 51, Fissure 57, Zen Headbutt 63 | Whiscash (from 30) |
| Mantyke | old rod | 24 | both | BubbleBeam, Headbutt, Agility, Wing Attack | Water Pulse 28; as Mantine: Take Down 31, Confuse Ray 37, Bounce 40, Aqua Ring 46, Hydro Pump 49 | Mantine (from 30) |
| Frogadier | old rod | 26 | Oxide | Icy Wind, Faint Attack, Acrobatics, Low Kick | Waterfall 30, Fling 35; as Greninja: Scald 37, Dark Pulse 40, Extrasensory 43, Sludge Wave 47, Gunk Shot 51, Hydro Pump 55, Hydro Cannon 65 | Greninja (from 36) |
| Frogadier | old rod | 26 | v3 | Icy Wind, Faint Attack, Acrobatics, Low Kick | Fling 35; as Greninja: Water Shuriken on evolving, Night Slash on evolving, Scald 37, Dark Pulse 40, Extrasensory 43, Sludge Wave 47, Gunk Shot 51, Hydro Pump 55, Hydro Cannon 65 | Greninja (from 36) |
| Alomomola | good rod | 35 | Oxide | Protect, Water Pulse, Wake-Up Slap, Soak | Wish 37, Brine 41, Safeguard 45, Whirlpool 49, Helping Hand 53, Healing Wish 57, Wide Guard 61, Hydro Pump 65 | Alomomola |
| Alomomola | good rod | 35 | v3 | Protect, Water Pulse, Wake-Up Slap, Soak | Wish 37, Brine 41, Safeguard 45, Helping Hand 53, Healing Wish 57, Wide Guard 61, Hydro Pump 65 | Alomomola |
| Tentacool | good rod | 35 | Oxide | Wrap, Barrier, Water Pulse, Poison Jab | Screech 36; as Tentacruel: Poison Jab 36, Screech 42, Hydro Pump 49, Wring Out 55 | Tentacruel (from 36) |
| Tentacool | good rod | 35 | v3 | BubbleBeam, Barrier, Water Pulse, Poison Jab | Screech 36; as Tentacruel: Poison Jab 36, Screech 42, Toxic 44, Hydro Pump 49, Wring Out 55 | Tentacruel (from 36) |
| Corsola | good rod | 37 | Oxide | BubbleBeam, Lucky Chant, AncientPower, Aqua Ring | Spike Cannon 40, Power Gem 44, Mirror Coat 48, Earth Power 53 | Corsola |
| Corsola | good rod | 37 | v3 | Lucky Chant, AncientPower, Rock Blast, Aqua Ring | Spike Cannon 40, Power Gem 44, Mirror Coat 48, Earth Power 53, Aqua Cutter 63 | Corsola |
| Gastrodon | good rod | 37 | Oxide | Water Pulse, Mud Bomb, Hidden Power, Body Slam | Muddy Water 41, Recover 54 | Gastrodon |
| Gastrodon | good rod | 37 | v3 | Water Pulse, Mud Bomb, Hidden Power, Body Slam | Muddy Water 39, Earthquake 44, Recover 54, Rock Slide 64 | Gastrodon |
| Wailmer | good rod | 39 | Oxide | Rest, Brine, Water Spout, Amnesia | as Wailord: Dive 46, Bounce 54, Hydro Pump 62 | Wailord (from 40) |
| Wailmer | good rod | 39 | v3 | Mist, Rest, Brine, Amnesia | as Wailord: Dive 46, Bounce 54, Hydro Pump 62 | Wailord (from 40) |
| Tentacool | surf | 40 | Oxide | Water Pulse, Poison Jab, Screech, Hydro Pump | as Tentacruel: Screech 42, Hydro Pump 49, Wring Out 55 | Tentacruel (from 41) |
| Tentacool | surf | 40 | v3 | Poison Jab, Screech, Toxic, Hydro Pump | as Tentacruel: Screech 42, Toxic 44, Hydro Pump 49, Wring Out 55 | Tentacruel (from 41) |
| Toxapex | surf | 40 | both | Recover, Spike Cannon, Pin Missile, Toxic | Venom Drench 42, Poison Jab 43, Liquidation 45 | Toxapex |
| Mantyke | surf | 43 | both | Water Pulse, Take Down, Confuse Ray, Bounce | as Mantine: Aqua Ring 46, Hydro Pump 49 | Mantine (from 44) |
| Pelipper | surf | 43 | Oxide | Stockpile, Swallow, Spit Up, Fling | Tailwind 50, Hydro Pump 57 | Pelipper |
| Pelipper | surf | 43 | v3 | Stockpile, Swallow, Spit Up, Fling | Tailwind 50, Roost 53, Hydro Pump 57, Air Slash 63 | Pelipper |
| Lanturn | super rod | 45 | Oxide | Spit Up, BubbleBeam, Signal Beam, Discharge | Aqua Ring 47, Hydro Pump 52, Charge 57 | Lanturn |
| Lanturn | super rod | 45 | v3 | Swallow, Spit Up, BubbleBeam, Signal Beam | Aqua Ring 47, Hydro Pump 52, Discharge 53, Charge 57, Thunder 65 | Lanturn |
| Lumineon | super rod | 45 | Oxide | Captivate, Safeguard, Aqua Ring, Whirlpool | U-turn 48, Bounce 53, Silver Wind 59 | Lumineon |
| Lumineon | super rod | 45 | v3 | Water Pulse, Captivate, Safeguard, Aqua Ring | U-turn 48, Bounce 53, Silver Wind 59, Ice Fang 65 | Lumineon |
| Relicanth | surf | 46 | Oxide | Yawn, Take Down, Mud Sport, AncientPower | Double-Edge 50, Dive 57, Rest 64 | Relicanth |
| Relicanth | surf | 46 | v3 | Take Down, Mud Sport, Dive, AncientPower | Double-Edge 50, Earthquake 53, Rest 64 | Relicanth |
| Galarian Rapidash | wild | 47 to 50 | both | Psybeam, Stomp, Heal Pulse, Take Down | Dazzling Gleam 49, Psychic 56, Healing Wish 63 | Galarian Rapidash |
| Absol | wild | 48 | Oxide | Double Team, Slash, Future Sight, Sucker Punch | Detect 49, Night Slash 52, Me First 57, Psycho Cut 60, Perish Song 65 | Absol |
| Absol | wild | 48 | v3 | Double Team, Slash, Future Sight, Sucker Punch | Detect 49, Me First 57, Psycho Cut 60, Perish Song 65 | Absol |
| Altaria | wild | 48 | both | Natural Gift, DragonBreath, Dragon Dance, Refresh | Dragon Pulse 54, Perish Song 62 | Altaria |
| Liepard | wild | 48 | both | Sucker Punch, Nasty Plot, Night Slash, Snatch | Play Rough 54 | Liepard |
| Octillery | super rod | 48 | both | Bullet Seed, Wring Out, Signal Beam, Ice Beam | Hyper Beam 55 | Octillery |
| Raichu | wild | 48 | Oxide | ThunderShock, Tail Whip, Quick Attack, Thunderbolt | nothing | Raichu |
| Raichu | wild | 48 | v3 | Tail Whip, Quick Attack, Thunderbolt, Thunder | nothing | Raichu |
| Talonflame | wild | 48 | Oxide | Natural Gift, Acrobatics, Me First, Tailwind | Flare Blitz 51, Brave Bird 55 | Talonflame |
| Talonflame | wild | 48 | v3 | Natural Gift, Acrobatics, Me First, Tailwind | Flare Blitz 64, Brave Bird 65 | Talonflame |
| Tentacruel | super rod | 48 | Oxide | Barrier, Water Pulse, Poison Jab, Screech | Hydro Pump 49, Wring Out 55 | Tentacruel |
| Tentacruel | super rod | 48 | v3 | Water Pulse, Poison Jab, Screech, Toxic | Hydro Pump 49, Wring Out 55 | Tentacruel |
| Toucannon | wild | 48 to 49 | Oxide | Screech, Drill Peck, Bullet Seed, FeatherDance | Hyper Voice 50 | Toucannon |
| Toucannon | wild | 48 to 49 | v3 | Fury Attack, Screech, Bullet Seed, FeatherDance | Hyper Voice 56, Rock Blast 65 | Toucannon |
| Tsareena | wild | 48 to 49 | Oxide | Low Sweep, Aromatherapy, Leaf Storm, Power Whip | Hi Jump Kick 55 | Tsareena |
| Tsareena | wild | 48 to 49 | v3 | Trop Kick, Low Sweep, Aromatherapy, Power Whip | Hi Jump Kick 55, Leaf Storm 60 | Tsareena |
| Arboliva | wild | 49 | Oxide | Seed Bomb, Energy Ball, Leech Seed, Terrain Pulse | Petal Blizzard 52, Petal Dance 58 | Arboliva |
| Arboliva | wild | 49 | v3 | Flail, Mega Drain, Leech Seed, Seed Bomb | Energy Ball 53, Petal Dance 58, Petal Blizzard 60 | Arboliva |
| Lurantis | wild | 49 | Oxide | Sweet Scent, X-Scissor, Synthesis, Leaf Blade | Solar Blade 55 | Lurantis |
| Lurantis | wild | 49 | v3 | Slash, Sweet Scent, X-Scissor, Synthesis | Solar Blade 55, Dual Chop 64 | Lurantis |
| Floatzel | wild | 50 | Oxide | Crunch, Agility, Whirlpool, Razor Wind | nothing | Floatzel |
| Floatzel | wild | 50 | v3 | Swift, Aqua Jet, Crunch, Agility | nothing | Floatzel |
| Gastrodon | wild | 50 | Oxide | Mud Bomb, Hidden Power, Body Slam, Muddy Water | Recover 54 | Gastrodon |
| Gastrodon | wild | 50 | v3 | Hidden Power, Body Slam, Muddy Water, Earthquake | Recover 54, Rock Slide 64 | Gastrodon |
| Crawdaunt | super rod | 51 | Oxide | Swift, Taunt, Night Slash, Crabhammer | Swords Dance 52, Crunch 57, Guillotine 65 | Crawdaunt |
| Crawdaunt | super rod | 51 | v3 | Swift, Taunt, Night Slash, Crabhammer | Swords Dance 52, Crunch 57, Cross Chop 63, Guillotine 65 | Crawdaunt |

## Stark Mountain

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 65 | At the cap |
|---|---|---|---|---|---|---|
| Galarian Weezing | wild | 51 to 54 | Oxide | Will-O-Wisp, Sludge Bomb, Pain Split, Strange Steam | Explosion 55 | Galarian Weezing |
| Galarian Weezing | wild | 51 to 54 | v3 | Will-O-Wisp, Sludge Bomb, Pain Split, Strange Steam | Explosion 55, Heat Wave 65 | Galarian Weezing |
| Houndoom | wild | 52 | Oxide | Fire Fang, Faint Attack, Embargo, Flamethrower | Crunch 54, Nasty Plot 60 | Houndoom |
| Houndoom | wild | 52 | v3 | Odor Sleuth, Fire Fang, Faint Attack, Embargo | Flamethrower 53, Crunch 54, Dark Pulse 56, Nasty Plot 60 | Houndoom |
| Magcargo | wild | 52 to 53 | both | Amnesia, Lava Plume, Rock Slide, Body Slam | Flamethrower 61 | Magcargo |
| Magmortar | wild | 52 to 54 | Oxide | Confuse Ray, Fire Punch, Lava Plume, Flamethrower | Fire Blast 58 | Magmortar |
| Magmortar | wild | 52 to 54 | v3 | Confuse Ray, Fire Punch, Lava Plume, Flamethrower | Fire Blast 60 | Magmortar |
| Rhyperior | wild | 52 | Oxide | Horn Drill, Hammer Arm, Stone Edge, Earthquake | Megahorn 57, Rock Wrecker 61 | Rhyperior |
| Rhyperior | wild | 52 | v3 | Take Down, Horn Drill, Hammer Arm, Stone Edge | Megahorn 56, Earthquake 60, Rock Wrecker 61 | Rhyperior |
| Salazzle | wild | 52 to 53 | Oxide | Venoshock, Flamethrower, Sludge Bomb, Dragon Pulse | Fire Blast 55 | Salazzle |
| Salazzle | wild | 52 to 53 | v3 | Flame Burst, Dragon Rage, Toxic, Venoshock | Dragon Pulse 53, Flamethrower 54, Fire Blast 55, Sludge Bomb 56 | Salazzle |
| Turtonator | wild | 52 | Oxide | Body Slam, Flamethrower, Dragon Pulse, Fire Spin | Explosion 55, Overheat 61 | Turtonator |
| Turtonator | wild | 52 | v3 | Rapid Spin, Body Slam, Flamethrower, Dragon Pulse | Explosion 55, Overheat 61 | Turtonator |
| Weezing | wild | 52 | both | Haze, Double Hit, Explosion, Sludge Bomb | Destiny Bond 55, Memento 63 | Weezing |
| Ceruledge | wild | 53 | Oxide | Lava Plume, Swords Dance, Ally Switch, Bitter Blade | Psycho Cut 56, Flare Blitz 62 | Ceruledge |
| Ceruledge | wild | 53 | v3 | Incinerate, Lava Plume, Swords Dance, Bitter Blade | Psycho Cut 56, Flare Blitz 62 | Ceruledge |
| Larvesta | wild | 54 | Oxide | Struggle Bug, Flame Wheel, Bug Bite, Take Down | as Volcarona: Flamethrower 60, Bug Buzz 61, Whirlwind 64, Overheat 65 | Volcarona (from 59) |
| Larvesta | wild | 54 | v3 | Flame Wheel, Double-Edge, Bug Bite, Take Down | as Volcarona: Flamethrower 60, Bug Buzz 61, Whirlwind 64, Overheat 65 | Volcarona (from 59) |

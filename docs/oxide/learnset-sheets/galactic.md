# Galactic's split: what each catch knows and learns

Written by `tools/oxide/balance/learncheck.py sheets` for check 6 of the learnset baseline (`docs/oxide/learnset-checks.md`). One table per capture area first offered in Galactic's split, whose cap is 65. Each Pokemon is read at the lowest level it is found at there. "Knows at capture" is the last four moves its list gives by that level; "learns by level-up" is every entry it reaches after capture up to 65, evolving on time, with each later stage's moves under its name; "at the cap" is the stage it can be by then and the next one after. A row marked Rewrite shows the learnset rewrite's lists (the tree's) where it differs from the row marked Oxide, Oxide's lists before the learnset rewrite (`da6b92496c`); a row marked both is the same in each. Relearner-only moves and egg moves are left out.

## Distortion World

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 65 | At the cap |
|---|---|---|---|---|---|---|
| Giratina | static battle | 47 | Oxide | Ominous Wind, AncientPower, Dragon Claw, Shadow Force | Heal Block 50, Earth Power 60 | Giratina |
| Giratina | static battle | 47 | Rewrite | Ominous Wind, AncientPower, Dragon Claw, Shadow Force | Heal Block 50, Earth Power 60, Scary Face 62 | Giratina |

## Mt. Coronet Mountainside

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 65 | At the cap |
|---|---|---|---|---|---|---|
| Snover | wild | 36 | Oxide | Mist, Ice Shard, Ingrain, Wood Hammer | as Abomasnow: Blizzard 47, Sheer Cold 58 | Abomasnow (from 40) |
| Snover | wild | 36 | Rewrite | Ice Shard, Bulldoze, Rock Tomb, Wood Hammer | as Abomasnow: Hammer Arm 45, Ice Beam 47, Leaf Storm 53, Ice Punch 55, Giga Drain 61, Shadow Ball 63 | Abomasnow (from 40) |
| Dewgong | wild | 37 | Oxide | Aqua Jet, Brine, Sheer Cold, Take Down | Dive 41, Aqua Tail 43, Ice Beam 47, Safeguard 51 | Dewgong |
| Dewgong | wild | 37 | Rewrite | Aqua Jet, Brine, Signal Beam, Take Down | Dive 41, Aqua Tail 43, Drill Run 45, Ice Beam 47, Safeguard 51, Bite 54, Headbutt 56, Muddy Water 58, Body Slam 64 | Dewgong |
| Frosmoth | wild | 37 | Oxide | FeatherDance, Aurora Beam, Bug Buzz, Aurora Veil | Blizzard 40, Tailwind 44, Wide Guard 48, Quiver Dance 52 | Frosmoth |
| Frosmoth | wild | 37 | Rewrite | Infestation, Defog, Aurora Veil, Aurora Beam | Ice Beam 40, Tailwind 44, Wide Guard 48, Quiver Dance 52, Calm Mind 61 | Frosmoth |
| Hawlucha | wild | 37 | Oxide | Submission, Tailwind, Dual Wingbeat, Fly | Hi Jump Kick 42, Me First 48, Acrobatics 55, Close Combat 60 | Hawlucha |
| Hawlucha | wild | 37 | Rewrite | Brick Break, Tailwind, Dual Wingbeat, Fly | Hi Jump Kick 42, Lunge 45, Acrobatics 55, Close Combat 60, Throat Chop 62, Low Sweep 64 | Hawlucha |
| Mienshao | wild | 37 | Oxide | Force Palm, Bounce, Drain Punch, Vacuum Wave | Aura Sphere 38, Me First 40, Jump Kick 45, Dual Chop 48, Focus Blast 51, Acrobatics 55, Hi Jump Kick 64 | Mienshao |
| Mienshao | wild | 37 | Rewrite | Force Palm, Bounce, Drain Punch, Vacuum Wave | Aura Sphere 38, Low Sweep 40, Jump Kick 45, Dual Chop 48, U-turn 50, Victory Dance 52, Acrobatics 55, Rock Tomb 57, Hammer Arm 59, Hi Jump Kick 64 | Mienshao |
| Sneasel | wild | 37 to 38 | Oxide | Fury Swipes, Agility, Icy Wind, Slash | as Weavile: Fling 38, Metal Claw 42, Dark Pulse 49 | Weavile (from 37) |
| Sneasel | wild | 37 to 38 | Rewrite | Agility, Icy Wind, Slash, Revenge | as Weavile: Night Slash 37, Fling 38, Metal Claw 42, Dark Pulse 49, Low Sweep 61 | Weavile (from 37) |
| Snorunt | wild | 37 to 39 | Oxide | Protect, Ice Fang, Crunch, Ice Shard | as Glalie: Blizzard 51, Sheer Cold 59 | Glalie (from 42) |
| Snorunt | wild | 37 to 39 | Oxide | Protect, Ice Fang, Crunch, Ice Shard | as Froslass: Ice Shard 37, Blizzard 51, Destiny Bond 59 | Froslass (from 37) |
| Snorunt | wild | 37 to 39 | Rewrite | Ice Fang, Crunch, Frost Breath, Ice Shard | as Glalie: Rock Blast 42, Power Gem 44, Shadow Ball 46, Bulldoze 48, Icicle Crash 53, Dark Pulse 55, Block 61, Ice Punch 63 | Glalie (from 42) |
| Snorunt | wild | 37 to 39 | Rewrite | Ice Fang, Crunch, Frost Breath, Ice Shard | as Froslass: Ice Shard 37, Frost Breath 40, Signal Beam 44, Ice Beam 51, Shadow Ball 54, Aura Sphere 57, Sweet Kiss 61, Psychic 63 | Froslass (from 37) |
| Alolan Ninetales | wild | 38 | Oxide | Tail Whip, Disable, Ice Shard, Safeguard | nothing | Alolan Ninetales |
| Alolan Ninetales | wild | 38 | Rewrite | Play Rough, Flame Wheel, Dazzling Gleam, Triple Axel | Psyshock 43, Chilling Water 45, Incinerate 51, Confuse Ray 53, Will-O-Wisp 59 | Alolan Ninetales |
| Delibird | wild | 38 | Oxide | Present | nothing | Delibird |
| Delibird | wild | 38 | Rewrite | Present, Drill Peck, Ice Beam | Drill Run 54, Swagger 56, Ice Punch 58, Bounce 60, Sky Attack 65 | Delibird |
| Garganacl | wild | 38 | Oxide | Headbutt, Salt Cure, Recover, Rock Slide | Stealth Rock 40, Heavy Slam 44, Earthquake 49, Stone Edge 54, Explosion 60 | Garganacl |
| Garganacl | wild | 38 | Rewrite | Mud Shot, Headbutt, Recover, Rock Slide | Stealth Rock 40, Heavy Slam 44, Earthquake 49, Diamond Storm 52, Rock Blast 54, Fire Punch 56, Ice Punch 58, Body Press 64 | Garganacl |
| Donphan | wild | 39 | Oxide | Slam, Fury Attack, Assurance, Scary Face | Earthquake 46, Giga Impact 54 | Donphan |
| Donphan | wild | 39 | Rewrite | Magnitude, Trailblaze, Assurance, Scary Face | Knock Off 40, Fire Fang 43, Earthquake 46, Charm 51, Giga Impact 54 | Donphan |
| Gliscor | wild | 39 | Oxide | Screech, Night Slash, Swords Dance, U-turn | X-Scissor 42, Guillotine 45 | Gliscor |
| Gliscor | wild | 39 | Rewrite | Screech, Night Slash, Swords Dance, U-turn | X-Scissor 42, Lunge 57, Throat Chop 59, Cross Poison 65 | Gliscor |

## Mt. Coronet Peak

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 65 | At the cap |
|---|---|---|---|---|---|---|
| Bronzong | wild | 36 to 39 | Oxide | Extrasensory, Iron Defense, Safeguard, Block | Gyro Ball 38, Future Sight 43, Faint Attack 50, Payback 61 | Bronzong |
| Bronzong | wild | 36 to 39 | Rewrite | Iron Defense, Safeguard, Block, Bulldoze | Gyro Ball 38, Future Sight 43, Mirror Shot 45, Faint Attack 50, Iron Head 52, Rock Tomb 58, Payback 61 | Bronzong |
| Golbat | wild | 37 | Oxide | Wing Attack, Confuse Ray, Air Cutter, Mean Look | Poison Fang 39; as Crobat: Haze 45, Air Slash 51 | Crobat (from 40) |
| Golbat | wild | 37 | Rewrite | Bite, Confuse Ray, Air Cutter, Mean Look | Poison Fang 39; as Crobat: Steel Wing 45, Air Slash 51, Poison Jab 53, Zen Headbutt 55, U-turn 61, Toxic 63 | Crobat (from 40) |
| Graveler | wild | 37 | Oxide | Selfdestruct, Rollout, Rock Blast, Earthquake | Explosion 38; as Golem: Double-Edge 44, Stone Edge 49 | Golem (from 40) |
| Graveler | wild | 37 | Rewrite | Rock Blast, Bulldoze, Earthquake, Fire Punch | as Golem: Double-Edge 44, Rock Tomb 46, Iron Head 48, ThunderPunch 53, Block 61 | Golem (from 40) |
| Hariyama | wild | 37 | Oxide | SmellingSalt, Belly Drum, Force Palm, Seismic Toss | Wake-Up Slap 42, Endure 47, Close Combat 52, Reversal 57 | Hariyama |
| Hariyama | wild | 37 | Rewrite | Low Sweep, Force Palm, Bulldoze, Seismic Toss | Wake-Up Slap 42, Rock Tomb 44, Storm Throw 46, Endure 47, Close Combat 52, Reversal 57, Drain Punch 59, Lash Out 61 | Hariyama |
| Machoke | wild | 37 | Oxide | Revenge, Vital Throw, Submission, Wake-Up Slap | Cross Chop 40; as Machamp: Cross Chop 40, Scary Face 44, DynamicPunch 51 | Machamp (from 40) |
| Machoke | wild | 37 | Rewrite | Seismic Toss, Revenge, Vital Throw, Wake-Up Slap | Close Combat 40; as Machamp: Close Combat 40, Rock Slide 42, Scary Face 44, Throat Chop 46, Fire Punch 48, Rock Tomb 53, Bulk Up 55, Swagger 61 | Machamp (from 40) |
| Mienshao | wild | 37 | Oxide | Force Palm, Bounce, Drain Punch, Vacuum Wave | Aura Sphere 38, Me First 40, Jump Kick 45, Dual Chop 48, Focus Blast 51, Acrobatics 55, Hi Jump Kick 64 | Mienshao |
| Mienshao | wild | 37 | Rewrite | Force Palm, Bounce, Drain Punch, Vacuum Wave | Aura Sphere 38, Low Sweep 40, Jump Kick 45, Dual Chop 48, U-turn 50, Victory Dance 52, Acrobatics 55, Rock Tomb 57, Hammer Arm 59, Hi Jump Kick 64 | Mienshao |
| Naclstack | wild | 37 to 38 | Oxide | Headbutt, Iron Defense, Recover, Rock Slide | Stealth Rock 38; as Garganacl: Stealth Rock 40, Heavy Slam 44, Earthquake 49, Stone Edge 54, Explosion 60 | Garganacl (from 38) |
| Naclstack | wild | 37 to 38 | Rewrite | Headbutt, Iron Defense, Recover, Rock Slide | Stealth Rock 38; as Garganacl: Hammer Arm on evolving, Stealth Rock 40, Heavy Slam 44, Earthquake 49, Diamond Storm 52, Rock Blast 54, Fire Punch 56, Ice Punch 58, Body Press 64 | Garganacl (from 38) |
| Carbink | wild | 38 | Oxide | AncientPower, Rock Polish, Rock Slide, Stealth Rock | Skill Swap 40, Light Screen 44, Power Gem 45, Moonblast 52, Stone Edge 54 | Carbink |
| Carbink | wild | 38 | Rewrite | Rock Tomb, Dazzling Gleam, Rock Slide, Stealth Rock | Skill Swap 40, Light Screen 44, Power Gem 45, Moonblast 52, Iron Head 54, Diamond Storm 56, Psychic 59, Body Press 61 | Carbink |
| Glimmora | wild | 38 | Oxide | Stealth Rock, Venoshock, Selfdestruct, Rock Slide | Power Gem 39, Acid Armor 44, Sludge Wave 50 | Glimmora |
| Glimmora | wild | 38 | Rewrite | Rock Polish, Stealth Rock, Venoshock, Rock Slide | Power Gem 39, Sludge Bomb 41, Acid Armor 44, Flash Cannon 48, Sludge Wave 50, Energy Ball 56, Dazzling Gleam 58, Confuse Ray 64 | Glimmora |
| Gliscor | wild | 39 | Oxide | Screech, Night Slash, Swords Dance, U-turn | X-Scissor 42, Guillotine 45 | Gliscor |
| Gliscor | wild | 39 | Rewrite | Screech, Night Slash, Swords Dance, U-turn | X-Scissor 42, Lunge 57, Throat Chop 59, Cross Poison 65 | Gliscor |
| Klefki | wild | 39 | Oxide | Imprison, Mirror Shot, Flash Cannon, Foul Play | Play Rough 41, Magic Room 44, Heal Block 50, Last Resort 52 | Klefki |
| Klefki | wild | 39 | Rewrite | Mirror Shot, Iron Defense, Flash Cannon, Foul Play | Play Rough 41, Magic Room 44, Calm Mind 48, Heal Block 50, Last Resort 52, Psychic 56, Skitter Smack 58, Thunder Wave 64 | Klefki |

## Resort Area

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 65 | At the cap |
|---|---|---|---|---|---|---|
| Luvdisc | old rod | 22 | Oxide | Agility, Take Down, Lucky Chant, Attract | Sweet Kiss 27; as Alomomola: Soak 33, Wish 37, Brine 41, Safeguard 45, Whirlpool 49, Helping Hand 53, Healing Wish 57, Wide Guard 61, Hydro Pump 65 | Alomomola (from 30) |
| Luvdisc | old rod | 22 | Rewrite | Lucky Chant, Icy Wind, Heart Stamp, Attract | Sweet Kiss 27; as Alomomola: Fury Swipes 30, Heal Pulse 31, Wake-Up Slap 32, Soak 33, Agility 35, Wish 37, Play Rough 39, Brine 41, Scale Shot 43, Safeguard 45, Whirlpool 49, Helping Hand 53, Bounce 55, Wide Guard 61, Muddy Water 65 | Alomomola (from 30) |
| Tentacool | old rod | 22 | Oxide | Acid, Toxic Spikes, BubbleBeam, Wrap | Barrier 26, Water Pulse 29; as Tentacruel: Poison Jab 36, Screech 42, Hydro Pump 49, Wring Out 55 | Tentacruel (from 30) |
| Tentacool | old rod | 22 | Rewrite | Acid, Toxic Spikes, Icy Wind, BubbleBeam | Barrier 26, Water Pulse 29; as Tentacruel: Psybeam 34, Poison Jab 36, Scald 38, Screech 42, Surf 49, Sludge Wave 52, Sludge Bomb 54, Muddy Water 58, Power Gem 60 | Tentacruel (from 30) |
| Mantyke | old rod | 24 to 26 | Oxide | BubbleBeam, Headbutt, Agility, Wing Attack | Water Pulse 28; as Mantine: Take Down 31, Confuse Ray 37, Bounce 40, Aqua Ring 46, Hydro Pump 49 | Mantine (from 30) |
| Mantyke | old rod | 24 to 26 | Rewrite | BubbleBeam, Headbutt, Agility, Wing Attack | Water Pulse 28; as Mantine: Take Down 31, Scald 34, Confuse Ray 37, Bounce 40, Signal Beam 42, Aqua Ring 46, Surf 50, Air Slash 52, Psychic 58, Muddy Water 60 | Mantine (from 30) |
| Remoraid | old rod | 24 | Oxide | Psybeam, Aurora Beam, BubbleBeam, Focus Energy | as Octillery: Octazooka 25, Bullet Seed 29, Wring Out 36, Signal Beam 42, Ice Beam 48, Hyper Beam 55 | Octillery (from 25) |
| Remoraid | old rod | 24 | Rewrite | Psybeam, Aurora Beam, BubbleBeam, Focus Energy | as Octillery: Octazooka 25, Rock Blast 27, Bullet Seed 29, Scald 35, Signal Beam 42, Skitter Smack 44, Ice Beam 48, Hyper Beam 55, Snipe Shot 56 | Octillery (from 25) |
| Luvdisc | good rod | 35 | Oxide | Lucky Chant, Attract, Sweet Kiss, Water Pulse | as Alomomola: Wish 37, Brine 41, Safeguard 45, Whirlpool 49, Helping Hand 53, Healing Wish 57, Wide Guard 61, Hydro Pump 65 | Alomomola (from 36) |
| Luvdisc | good rod | 35 | Rewrite | Heart Stamp, Attract, Sweet Kiss, Water Pulse | as Alomomola: Wish 37, Play Rough 39, Brine 41, Scale Shot 43, Safeguard 45, Whirlpool 49, Helping Hand 53, Bounce 55, Wide Guard 61, Muddy Water 65 | Alomomola (from 36) |
| Mareanie | good rod | 35 | Oxide | Toxic Spikes, Recover, Spike Cannon, Pin Missile | Toxic 36; as Toxapex: Toxic 39, Venom Drench 42, Poison Jab 43, Liquidation 45 | Toxapex (from 38) |
| Mareanie | good rod | 35 | Rewrite | Toxic Spikes, Recover, Fury Swipes, Pin Missile | Toxic 36, Water Pulse 38; as Toxapex: Toxic 39, Venom Drench 42, Poison Jab 43, Liquidation 45, Sludge Bomb 48, Ice Beam 50, Iron Defense 64 | Toxapex (from 38) |
| Mantyke | good rod | 37 | Oxide | Wing Attack, Water Pulse, Take Down, Confuse Ray | as Mantine: Bounce 40, Aqua Ring 46, Hydro Pump 49 | Mantine (from 38) |
| Mantyke | good rod | 37 | Rewrite | Wing Attack, Water Pulse, Take Down, Confuse Ray | as Mantine: Bounce 40, Signal Beam 42, Aqua Ring 46, Surf 50, Air Slash 52, Psychic 58, Muddy Water 60 | Mantine (from 38) |
| Shellos | good rod | 37 | Oxide | Mud Bomb, Hidden Power, Body Slam, Muddy Water | as Gastrodon: Muddy Water 41, Recover 54 | Gastrodon (from 38) |
| Shellos | good rod | 37 | Rewrite | Mud Bomb, Hidden Power, Body Slam, Muddy Water | as Gastrodon: Muddy Water 41, Earth Power 43, Bulldoze 45, Ice Beam 50, Thousand Waves 52, Recover 54, Skitter Smack 58, Rock Tomb 60 | Gastrodon (from 38) |
| Greninja | good rod | 39 | Oxide | Low Kick, Waterfall, Fling, Scald | Dark Pulse 40, Extrasensory 43, Sludge Wave 47, Gunk Shot 51, Hydro Pump 55, Hydro Cannon 65 | Greninja |
| Greninja | good rod | 39 | Rewrite | Waterfall, Fling, Shadow Sneak, Scald | Dark Pulse 40, Bounce 41, Extrasensory 43, Sludge Wave 47, Water Shuriken 49, Gunk Shot 51, Throat Chop 56, Hydro Cannon 65 | Greninja |
| Gastrodon | surf | 40 | Oxide | Water Pulse, Mud Bomb, Hidden Power, Body Slam | Muddy Water 41, Recover 54 | Gastrodon |
| Gastrodon | surf | 40 | Rewrite | Hidden Power, Body Slam, AncientPower, Clear Smog | Muddy Water 41, Earth Power 43, Bulldoze 45, Ice Beam 50, Thousand Waves 52, Recover 54, Skitter Smack 58, Rock Tomb 60 | Gastrodon |
| Tentacool | surf | 40 | Oxide | Water Pulse, Poison Jab, Screech, Hydro Pump | as Tentacruel: Screech 42, Hydro Pump 49, Wring Out 55 | Tentacruel (from 41) |
| Tentacool | surf | 40 | Rewrite | Water Pulse, Poison Jab, Screech, Surf | as Tentacruel: Screech 42, Surf 49, Sludge Wave 52, Sludge Bomb 54, Muddy Water 58, Power Gem 60 | Tentacruel (from 41) |
| Mantyke | surf | 43 | Oxide | Water Pulse, Take Down, Confuse Ray, Bounce | as Mantine: Aqua Ring 46, Hydro Pump 49 | Mantine (from 44) |
| Mantyke | surf | 43 | Rewrite | Water Pulse, Take Down, Confuse Ray, Bounce | as Mantine: Aqua Ring 46, Surf 50, Air Slash 52, Psychic 58, Muddy Water 60 | Mantine (from 44) |
| Shellos | surf | 43 | Oxide | Mud Bomb, Hidden Power, Body Slam, Muddy Water | as Gastrodon: Recover 54 | Gastrodon (from 44) |
| Shellos | surf | 43 | Rewrite | Mud Bomb, Hidden Power, Body Slam, Muddy Water | as Gastrodon: Bulldoze 45, Ice Beam 50, Thousand Waves 52, Recover 54, Skitter Smack 58, Rock Tomb 60 | Gastrodon (from 44) |
| Jellicent | super rod | 45 | Oxide | Hex, Brine, Pain Split, Destiny Bond | Shadow Ball 51, Scald 55, Water Spout 65 | Jellicent |
| Jellicent | super rod | 45 | Rewrite | Hex, Brine, Pain Split, Dark Pulse | Shadow Ball 51, Giga Drain 53, Scald 55, Sludge Bomb 61, Water Spout 65 | Jellicent |
| Lanturn | super rod | 45 | Oxide | Spit Up, BubbleBeam, Signal Beam, Discharge | Aqua Ring 47, Hydro Pump 52, Charge 57 | Lanturn |
| Lanturn | super rod | 45 | Rewrite | BubbleBeam, Signal Beam, Discharge, Thunderbolt | Aqua Ring 47, Muddy Water 52, Charge 57, Flash Cannon 59, Scald 61 | Lanturn |
| Greninja | surf | 46 | Oxide | Fling, Scald, Dark Pulse, Extrasensory | Sludge Wave 47, Gunk Shot 51, Hydro Pump 55, Hydro Cannon 65 | Greninja |
| Greninja | surf | 46 | Rewrite | Scald, Dark Pulse, Bounce, Extrasensory | Sludge Wave 47, Water Shuriken 49, Gunk Shot 51, Throat Chop 56, Hydro Cannon 65 | Greninja |
| Gorebyss | super rod | 48 | Oxide | Baton Pass, Dive, Psychic, Aqua Tail | Hydro Pump 51 | Gorebyss |
| Gorebyss | super rod | 48 | Rewrite | Scald, Psychic, Aqua Tail, Shadow Ball | Muddy Water 51, Ice Beam 56, Shell Smash 64 | Gorebyss |
| Lumineon | super rod | 48 | Oxide | Safeguard, Aqua Ring, Whirlpool, U-turn | Bounce 53, Silver Wind 59 | Lumineon |
| Lumineon | super rod | 48 | Rewrite | Signal Beam, Whirlpool, Fillet Away, U-turn | Crunch 50, Bounce 53, Silver Wind 59, Scald 61 | Lumineon |
| Kingdra | super rod | 51 | Oxide | Twister, Brine, Hydro Pump, Dragon Dance | Dragon Pulse 57 | Kingdra |
| Kingdra | super rod | 51 | Rewrite | Twister, Brine, Aurora Beam, Octazooka | Scale Shot 54, Snipe Shot 55, Dragon Pulse 57, Dragon Dance 58, Core Enforcer 62, Bounce 65 | Kingdra |

## Route 225

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 65 | At the cap |
|---|---|---|---|---|---|---|
| Chinchou | old rod | 22 | Oxide | Flail, Water Gun, Confuse Ray, Spark | Take Down 23; as Lanturn: Stockpile 27, Swallow 27, Spit Up 27, BubbleBeam 30, Signal Beam 35, Discharge 40, Aqua Ring 47, Hydro Pump 52, Charge 57 | Lanturn (from 27) |
| Chinchou | old rod | 22 | Rewrite | Chilling Water, Confuse Ray, Icy Wind, Spark | Take Down 23, ParabolicCharge 25; as Lanturn: Stockpile 27, Swallow 28, Spit Up 29, BubbleBeam 30, Signal Beam 35, Discharge 40, Thunderbolt 42, Aqua Ring 47, Muddy Water 52, Charge 57, Flash Cannon 59, Scald 61 | Lanturn (from 27) |
| Goldeen | old rod | 22 | Oxide | Supersonic, Horn Attack, Water Pulse, Flail | Aqua Ring 27, Fury Attack 31; as Seaking: Waterfall 40, Horn Drill 47, Agility 56, Megahorn 63 | Seaking (from 33) |
| Goldeen | old rod | 22 | Rewrite | Horn Attack, Water Pulse, Agility, Flail | Aqua Ring 27; as Seaking: Scale Shot 33, Skull Bash 35, Waterfall 40, Poison Jab 42, Throat Chop 44, Fillet Away 46, Flip Turn 50, Liquidation 52, Agility 56, Megahorn 63 | Seaking (from 33) |
| Buizel | old rod | 24 | Oxide | Water Gun, Pursuit, Swift, Aqua Jet | as Floatzel: Crunch 26, Agility 29, Whirlpool 39, Razor Wind 50 | Floatzel (from 26) |
| Buizel | old rod | 24 | Rewrite | Scary Face, Pursuit, Swift, Aqua Jet | as Floatzel: Crunch 26, Low Sweep 28, Icy Wind 30, Rock Tomb 35, Whirlpool 39, BubbleBeam 43, Agility 45, Triple Dive 54 | Floatzel (from 26) |
| Carvanha | old rod | 24 | Oxide | Scary Face, Ice Fang, Screech, Swagger | Assurance 26, Crunch 28; as Sharpedo: Slash 30, Aqua Jet 34, Taunt 40, Agility 45, Skull Bash 50, Night Slash 56 | Sharpedo (from 30) |
| Carvanha | old rod | 24 | Rewrite | Ice Fang, Screech, Swagger, Aqua Jet | Assurance 26, Crunch 28; as Sharpedo: Slash 30, Aqua Jet 34, Bulldoze 36, Taunt 40, Poison Fang 42, Agility 45, Skull Bash 50, Triple Dive 54, Night Slash 56, Fire Fang 58, Poison Jab 60 | Sharpedo (from 30) |
| Tentacool | old rod | 26 | Oxide | Toxic Spikes, BubbleBeam, Wrap, Barrier | Water Pulse 29; as Tentacruel: Poison Jab 36, Screech 42, Hydro Pump 49, Wring Out 55 | Tentacruel (from 30) |
| Tentacool | old rod | 26 | Rewrite | Toxic Spikes, Icy Wind, BubbleBeam, Barrier | Water Pulse 29; as Tentacruel: Psybeam 34, Poison Jab 36, Scald 38, Screech 42, Surf 49, Sludge Wave 52, Sludge Bomb 54, Muddy Water 58, Power Gem 60 | Tentacruel (from 30) |
| Ludicolo | good rod | 35 | Oxide | Astonish, Growl, Mega Drain, Nature Power | nothing | Ludicolo |
| Ludicolo | good rod | 35 | Rewrite | Mega Drain, Nature Power, Icy Wind, Scald | Mud Shot 40, Muddy Water 54, Giga Drain 56, Dark Pulse 58, Energy Ball 62, Leech Seed 64 | Ludicolo |
| Wooper | good rod | 35 | Oxide | Mud Bomb, Amnesia, Yawn, Earthquake | as Quagsire: Earthquake 36, Mist 48, Haze 48, Muddy Water 53 | Quagsire (from 36) |
| Wooper | good rod | 35 | Oxide | Mud Bomb, Amnesia, Yawn, Earthquake | as Clodsire: Megahorn 36, Toxic 40, Earthquake 48, Recover 55 | Clodsire (from 35) |
| Wooper | good rod | 35 | Rewrite | Mud Bomb, Amnesia, Yawn, Earthquake | as Quagsire: Earthquake 36, Poison Jab 38, Rock Slide 43, Thousand Waves 45, Mist 48, Ice Punch 51, Muddy Water 53, Liquidation 59, Rock Tomb 61 | Quagsire (from 36) |
| Wooper | good rod | 35 | Rewrite | Mud Bomb, Amnesia, Yawn, Earthquake | as Clodsire: Megahorn 36, Toxic 40, Iron Head 42, Earthquake 48, Zen Headbutt 50, Recover 55, Toxic Spikes 58 | Clodsire (from 35) |
| Shellos | good rod | 37 | Oxide | Mud Bomb, Hidden Power, Body Slam, Muddy Water | as Gastrodon: Muddy Water 41, Recover 54 | Gastrodon (from 38) |
| Shellos | good rod | 37 | Rewrite | Mud Bomb, Hidden Power, Body Slam, Muddy Water | as Gastrodon: Muddy Water 41, Earth Power 43, Bulldoze 45, Ice Beam 50, Thousand Waves 52, Recover 54, Skitter Smack 58, Rock Tomb 60 | Gastrodon (from 38) |
| Surskit | good rod | 37 | Oxide | BubbleBeam, Agility, Mist, Haze | as Masquerain: Silver Wind 40, Air Slash 47, Whirlwind 54, Bug Buzz 61 | Masquerain (from 38) |
| Surskit | good rod | 37 | Rewrite | Water Sport, BubbleBeam, Agility, Mist | as Masquerain: Silver Wind 40, Bug Buzz 44, Air Slash 47, Quiver Dance 52, Lunge 54, Leech Life 59, Waterfall 61 | Masquerain (from 38) |
| Sharpedo | good rod | 39 | Oxide | Assurance, Crunch, Slash, Aqua Jet | Taunt 40, Agility 45, Skull Bash 50, Night Slash 56 | Sharpedo |
| Sharpedo | good rod | 39 | Rewrite | Crunch, Slash, Aqua Jet, Bulldoze | Taunt 40, Poison Fang 42, Agility 45, Skull Bash 50, Triple Dive 54, Night Slash 56, Fire Fang 58, Poison Jab 60 | Sharpedo |
| Gastrodon | surf | 40 | Oxide | Water Pulse, Mud Bomb, Hidden Power, Body Slam | Muddy Water 41, Recover 54 | Gastrodon |
| Gastrodon | surf | 40 | Rewrite | Hidden Power, Body Slam, AncientPower, Clear Smog | Muddy Water 41, Earth Power 43, Bulldoze 45, Ice Beam 50, Thousand Waves 52, Recover 54, Skitter Smack 58, Rock Tomb 60 | Gastrodon |
| Masquerain | surf | 40 | Oxide | Gust, Scary Face, Stun Spore, Silver Wind | Air Slash 47, Whirlwind 54, Bug Buzz 61 | Masquerain |
| Masquerain | surf | 40 | Rewrite | Ominous Wind, Stun Spore, Icy Wind, Silver Wind | Bug Buzz 44, Air Slash 47, Quiver Dance 52, Lunge 54, Leech Life 59, Waterfall 61 | Masquerain |
| Buizel | surf | 43 | Oxide | Swift, Aqua Jet, Agility, Whirlpool | as Floatzel: Razor Wind 50 | Floatzel (from 44) |
| Buizel | surf | 43 | Rewrite | Swift, Aqua Jet, Agility, Whirlpool | as Floatzel: Agility 45, Triple Dive 54 | Floatzel (from 44) |
| Shellos | surf | 43 | Oxide | Mud Bomb, Hidden Power, Body Slam, Muddy Water | as Gastrodon: Recover 54 | Gastrodon (from 44) |
| Shellos | surf | 43 | Rewrite | Mud Bomb, Hidden Power, Body Slam, Muddy Water | as Gastrodon: Bulldoze 45, Ice Beam 50, Thousand Waves 52, Recover 54, Skitter Smack 58, Rock Tomb 60 | Gastrodon (from 44) |
| Ludicolo | super rod | 45 | Oxide | Astonish, Growl, Mega Drain, Nature Power | nothing | Ludicolo |
| Ludicolo | super rod | 45 | Rewrite | Nature Power, Icy Wind, Scald, Mud Shot | Muddy Water 54, Giga Drain 56, Dark Pulse 58, Energy Ball 62, Leech Seed 64 | Ludicolo |
| Quagsire | super rod | 45 | Oxide | Mud Bomb, Amnesia, Yawn, Earthquake | Mist 48, Haze 48, Muddy Water 53 | Quagsire |
| Quagsire | super rod | 45 | Rewrite | Earthquake, Poison Jab, Rock Slide, Thousand Waves | Mist 48, Ice Punch 51, Muddy Water 53, Liquidation 59, Rock Tomb 61 | Quagsire |
| Seaking | surf | 46 | Oxide | Flail, Aqua Ring, Fury Attack, Waterfall | Horn Drill 47, Agility 56, Megahorn 63 | Seaking |
| Seaking | surf | 46 | Rewrite | Waterfall, Poison Jab, Throat Chop, Fillet Away | Flip Turn 50, Liquidation 52, Agility 56, Megahorn 63 | Seaking |
| Hariyama | wild | 47 | Oxide | Force Palm, Seismic Toss, Wake-Up Slap, Endure | Close Combat 52, Reversal 57 | Hariyama |
| Hariyama | wild | 47 | Rewrite | Wake-Up Slap, Rock Tomb, Storm Throw, Endure | Close Combat 52, Reversal 57, Drain Punch 59, Lash Out 61 | Hariyama |
| Corviknight | wild | 48 | Oxide | FeatherDance, Revenge, Defog, Iron Head | Brave Bird 49, Body Press 55, Roost 65 | Corviknight |
| Corviknight | wild | 48 | Rewrite | Defog, Iron Head, U-turn, Power Trip | Brave Bird 49, Double-Edge 53, Body Press 55, Shift Gear 57, Body Slam 61, Roost 65 | Corviknight |
| Garganacl | wild | 48 | Oxide | Recover, Rock Slide, Stealth Rock, Heavy Slam | Earthquake 49, Stone Edge 54, Explosion 60 | Garganacl |
| Garganacl | wild | 48 | Rewrite | Recover, Rock Slide, Stealth Rock, Heavy Slam | Earthquake 49, Diamond Storm 52, Rock Blast 54, Fire Punch 56, Ice Punch 58, Body Press 64 | Garganacl |
| Gastrodon | super rod | 48 | Oxide | Mud Bomb, Hidden Power, Body Slam, Muddy Water | Recover 54 | Gastrodon |
| Gastrodon | super rod | 48 | Rewrite | Clear Smog, Muddy Water, Earth Power, Bulldoze | Ice Beam 50, Thousand Waves 52, Recover 54, Skitter Smack 58, Rock Tomb 60 | Gastrodon |
| Houndoom | wild | 48 | Oxide | Fire Fang, Faint Attack, Embargo, Flamethrower | Crunch 54, Nasty Plot 60 | Houndoom |
| Houndoom | wild | 48 | Rewrite | Faint Attack, Mud Shot, Embargo, Flamethrower | Dark Pulse 50, Crunch 54, Fiery Wrath 56, Shadow Ball 58, Nasty Plot 60, Toxic 62 | Houndoom |
| Liepard | wild | 48 | Oxide | Sucker Punch, Nasty Plot, Night Slash, Snatch | Play Rough 54 | Liepard |
| Liepard | wild | 48 | Rewrite | Skitter Smack, Sucker Punch, Night Slash, Snatch | Throat Chop 49, Shadow Ball 51, Play Rough 54, Psycho Cut 59, U-turn 61 | Liepard |
| Mienshao | wild | 48 | Oxide | Aura Sphere, Me First, Jump Kick, Dual Chop | Focus Blast 51, Acrobatics 55, Hi Jump Kick 64 | Mienshao |
| Mienshao | wild | 48 | Rewrite | Aura Sphere, Low Sweep, Jump Kick, Dual Chop | U-turn 50, Victory Dance 52, Acrobatics 55, Rock Tomb 57, Hammer Arm 59, Hi Jump Kick 64 | Mienshao |
| Seaking | super rod | 48 | Oxide | Aqua Ring, Fury Attack, Waterfall, Horn Drill | Agility 56, Megahorn 63 | Seaking |
| Seaking | super rod | 48 | Rewrite | Waterfall, Poison Jab, Throat Chop, Fillet Away | Flip Turn 50, Liquidation 52, Agility 56, Megahorn 63 | Seaking |
| Talonflame | wild | 48 | Oxide | Natural Gift, Acrobatics, Me First, Tailwind | Flare Blitz 51, Brave Bird 55 | Talonflame |
| Talonflame | wild | 48 | Rewrite | Acrobatics, Steel Wing, U-turn, Tailwind | Flare Blitz 51, Brave Bird 55, Overheat 57, Agility 59, Bulk Up 64 | Talonflame |
| Toucannon | wild | 48 | Oxide | Screech, Drill Peck, Bullet Seed, FeatherDance | Hyper Voice 50 | Toucannon |
| Toucannon | wild | 48 | Rewrite | Drill Peck, Bullet Seed, Throat Chop, FeatherDance | Hyper Voice 50, Bounce 52, Take Down 58, Body Slam 60 | Toucannon |
| Donphan | wild | 49 | Oxide | Fury Attack, Assurance, Scary Face, Earthquake | Giga Impact 54 | Donphan |
| Donphan | wild | 49 | Rewrite | Scary Face, Knock Off, Fire Fang, Earthquake | Charm 51, Giga Impact 54 | Donphan |
| Dubwool | wild | 49 | Oxide | Take Down, Guard Swap, Reversal, Cotton Guard | Double-Edge 50, Last Resort 56 | Dubwool |
| Dubwool | wild | 49 | Rewrite | Reversal, Raging Bull, Cotton Guard, Zen Headbutt | Double-Edge 50, Bounce 52, Wild Charge 54, Last Resort 56 | Dubwool |
| Golem | wild | 49 | Oxide | Earthquake, Explosion, Double-Edge, Stone Edge | nothing | Golem |
| Golem | wild | 49 | Rewrite | Earthquake, Double-Edge, Rock Tomb, Iron Head | ThunderPunch 53, Block 61 | Golem |
| Hawlucha | wild | 49 | Oxide | Dual Wingbeat, Fly, Hi Jump Kick, Me First | Acrobatics 55, Close Combat 60 | Hawlucha |
| Hawlucha | wild | 49 | Rewrite | Dual Wingbeat, Fly, Hi Jump Kick, Lunge | Acrobatics 55, Close Combat 60, Throat Chop 62, Low Sweep 64 | Hawlucha |
| Grapploct | wild | 50 | Oxide | Taunt, Reversal, Superpower, Topsy-Turvy | nothing | Grapploct |
| Grapploct | wild | 50 | Rewrite | Taunt, Reversal, Superpower, Drain Punch | Close Combat 53, Sucker Punch 55, Ice Punch 61, Liquidation 63 | Grapploct |
| Honchkrow | wild | 50 | Oxide | Wing Attack, Swagger, Nasty Plot, Night Slash | Dark Pulse 55 | Honchkrow |
| Honchkrow | wild | 50 | Rewrite | U-turn, Night Slash, Nasty Plot, Oblivion Wing | Sucker Punch 53, Dark Pulse 55, Heat Wave 61, Mean Look 63 | Honchkrow |
| Ninetales | wild | 50 | Oxide | Quick Attack, Confuse Ray, Safeguard, Flare Blitz | nothing | Ninetales |
| Ninetales | wild | 50 | Rewrite | Confuse Ray, Safeguard, Alluring Voice, Flare Blitz | Energy Ball 54, Extrasensory 56, Mystical Fire 62, Bite 64 | Ninetales |
| Greninja | super rod | 51 | Oxide | Dark Pulse, Extrasensory, Sludge Wave, Gunk Shot | Hydro Pump 55, Hydro Cannon 65 | Greninja |
| Greninja | super rod | 51 | Rewrite | Extrasensory, Sludge Wave, Water Shuriken, Gunk Shot | Throat Chop 56, Hydro Cannon 65 | Greninja |

## Route 226

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 65 | At the cap |
|---|---|---|---|---|---|---|
| Meloetta | in-game trade | 1 | Oxide | Round, Quick Attack, Confusion, Sing | Quick Attack 6, Confusion 11, Sing 16, Teeter Dance 21, Acrobatics 26, Psybeam 31, Echoed Voice 36, U-turn 43, Wake-Up Slap 50, Psychic 57, Hyper Voice 64 | Meloetta |
| Meloetta | in-game trade | 1 | Rewrite | Round, Quick Attack, Confusion, Sing | Quick Attack 6, Confusion 11, Sing 16, Teeter Dance 21, Acrobatics 26, Psybeam 31, U-turn 43, Wake-Up Slap 50, Psychic 57, Energy Ball 61, Charm 62, Hyper Voice 64 | Meloetta |
| Mantyke | old rod | 22 | Oxide | BubbleBeam, Headbutt, Agility, Wing Attack | Water Pulse 28; as Mantine: Take Down 31, Confuse Ray 37, Bounce 40, Aqua Ring 46, Hydro Pump 49 | Mantine (from 30) |
| Mantyke | old rod | 22 | Rewrite | BubbleBeam, Headbutt, Agility, Wing Attack | Water Pulse 28; as Mantine: Take Down 31, Scald 34, Confuse Ray 37, Bounce 40, Signal Beam 42, Aqua Ring 46, Surf 50, Air Slash 52, Psychic 58, Muddy Water 60 | Mantine (from 30) |
| Psyduck | old rod | 22 | Oxide | Water Gun, Disable, Confusion, Water Pulse | Fury Swipes 27, Screech 31; as Golduck: Psych Up 37, Zen Headbutt 44, Amnesia 50, Hydro Pump 56 | Golduck (from 33) |
| Psyduck | old rod | 22 | Rewrite | Water Gun, Disable, Confusion, Water Pulse | Fury Swipes 27, Low Sweep 29; as Golduck: Aurora Beam 34, Psych Up 37, Scald 39, Surf 42, Zen Headbutt 44, Aqua Step 47, Amnesia 50, Muddy Water 56, Power Gem 58, Ice Beam 60 | Golduck (from 33) |
| Finneon | old rod | 24 | Oxide | Water Gun, Attract, Gust, Water Pulse | Captivate 26, Safeguard 29; as Lumineon: Aqua Ring 35, Whirlpool 42, U-turn 48, Bounce 53, Silver Wind 59 | Lumineon (from 31) |
| Finneon | old rod | 24 | Rewrite | Water Gun, Attract, Icy Wind, Water Pulse | Captivate 26, Chilling Water 27, Safeguard 29; as Lumineon: Aqua Ring 35, Signal Beam 37, Whirlpool 42, Fillet Away 45, U-turn 48, Crunch 50, Bounce 53, Silver Wind 59, Scald 61 | Lumineon (from 31) |
| Shellos | old rod | 24 | Oxide | Harden, Water Pulse, Mud Bomb, Hidden Power | Body Slam 29; as Gastrodon: Muddy Water 41, Recover 54 | Gastrodon (from 30) |
| Shellos | old rod | 24 | Rewrite | Swagger, Water Pulse, Mud Bomb, Hidden Power | Body Slam 29; as Gastrodon: AncientPower 31, Clear Smog 34, Muddy Water 41, Earth Power 43, Bulldoze 45, Ice Beam 50, Thousand Waves 52, Recover 54, Skitter Smack 58, Rock Tomb 60 | Gastrodon (from 30) |
| Carvanha | old rod | 26 | Oxide | Ice Fang, Screech, Swagger, Assurance | Crunch 28; as Sharpedo: Slash 30, Aqua Jet 34, Taunt 40, Agility 45, Skull Bash 50, Night Slash 56 | Sharpedo (from 30) |
| Carvanha | old rod | 26 | Rewrite | Screech, Swagger, Aqua Jet, Assurance | Crunch 28; as Sharpedo: Slash 30, Aqua Jet 34, Bulldoze 36, Taunt 40, Poison Fang 42, Agility 45, Skull Bash 50, Triple Dive 54, Night Slash 56, Fire Fang 58, Poison Jab 60 | Sharpedo (from 30) |
| Lanturn | good rod | 35 | Oxide | Swallow, Spit Up, BubbleBeam, Signal Beam | Discharge 40, Aqua Ring 47, Hydro Pump 52, Charge 57 | Lanturn |
| Lanturn | good rod | 35 | Rewrite | Swallow, Spit Up, BubbleBeam, Signal Beam | Discharge 40, Thunderbolt 42, Aqua Ring 47, Muddy Water 52, Charge 57, Flash Cannon 59, Scald 61 | Lanturn |
| Mareanie | good rod | 35 | Oxide | Toxic Spikes, Recover, Spike Cannon, Pin Missile | Toxic 36; as Toxapex: Toxic 39, Venom Drench 42, Poison Jab 43, Liquidation 45 | Toxapex (from 38) |
| Mareanie | good rod | 35 | Rewrite | Toxic Spikes, Recover, Fury Swipes, Pin Missile | Toxic 36, Water Pulse 38; as Toxapex: Toxic 39, Venom Drench 42, Poison Jab 43, Liquidation 45, Sludge Bomb 48, Ice Beam 50, Iron Defense 64 | Toxapex (from 38) |
| Finneon | good rod | 37 | Oxide | Water Pulse, Captivate, Safeguard, Aqua Ring | Whirlpool 38; as Lumineon: Whirlpool 42, U-turn 48, Bounce 53, Silver Wind 59 | Lumineon (from 38) |
| Finneon | good rod | 37 | Rewrite | Captivate, Chilling Water, Safeguard, Aqua Ring | Whirlpool 38; as Lumineon: Whirlpool 42, Fillet Away 45, U-turn 48, Crunch 50, Bounce 53, Silver Wind 59, Scald 61 | Lumineon (from 38) |
| Tentacool | good rod | 37 | Oxide | Barrier, Water Pulse, Poison Jab, Screech | as Tentacruel: Screech 42, Hydro Pump 49, Wring Out 55 | Tentacruel (from 38) |
| Tentacool | good rod | 37 | Rewrite | Barrier, Water Pulse, Poison Jab, Screech | as Tentacruel: Scald 38, Screech 42, Surf 49, Sludge Wave 52, Sludge Bomb 54, Muddy Water 58, Power Gem 60 | Tentacruel (from 38) |
| Greninja | good rod | 39 | Oxide | Low Kick, Waterfall, Fling, Scald | Dark Pulse 40, Extrasensory 43, Sludge Wave 47, Gunk Shot 51, Hydro Pump 55, Hydro Cannon 65 | Greninja |
| Greninja | good rod | 39 | Rewrite | Waterfall, Fling, Shadow Sneak, Scald | Dark Pulse 40, Bounce 41, Extrasensory 43, Sludge Wave 47, Water Shuriken 49, Gunk Shot 51, Throat Chop 56, Hydro Cannon 65 | Greninja |
| Floatzel | surf | 40 | Oxide | Aqua Jet, Crunch, Agility, Whirlpool | Razor Wind 50 | Floatzel |
| Floatzel | surf | 40 | Rewrite | Low Sweep, Icy Wind, Rock Tomb, Whirlpool | BubbleBeam 43, Agility 45, Triple Dive 54 | Floatzel |
| Mareanie | surf | 40 | Oxide | Spike Cannon, Pin Missile, Toxic, Venom Drench | Liquidation 41, Poison Jab 41; as Toxapex: Venom Drench 42, Poison Jab 43, Liquidation 45 | Toxapex (from 41) |
| Mareanie | surf | 40 | Rewrite | Pin Missile, Toxic, Water Pulse, Venom Drench | Liquidation 41; as Toxapex: Venom Drench 42, Poison Jab 43, Liquidation 45, Sludge Bomb 48, Ice Beam 50, Iron Defense 64 | Toxapex (from 41) |
| Mantine | surf | 43 | Oxide | Water Pulse, Take Down, Confuse Ray, Bounce | Aqua Ring 46, Hydro Pump 49 | Mantine |
| Mantine | surf | 43 | Rewrite | Scald, Confuse Ray, Bounce, Signal Beam | Aqua Ring 46, Surf 50, Air Slash 52, Psychic 58, Muddy Water 60 | Mantine |
| Tentacruel | surf | 43 | Oxide | Barrier, Water Pulse, Poison Jab, Screech | Hydro Pump 49, Wring Out 55 | Tentacruel |
| Tentacruel | surf | 43 | Rewrite | Psybeam, Poison Jab, Scald, Screech | Surf 49, Sludge Wave 52, Sludge Bomb 54, Muddy Water 58, Power Gem 60 | Tentacruel |
| Mantine | super rod | 45 | Oxide | Water Pulse, Take Down, Confuse Ray, Bounce | Aqua Ring 46, Hydro Pump 49 | Mantine |
| Mantine | super rod | 45 | Rewrite | Scald, Confuse Ray, Bounce, Signal Beam | Aqua Ring 46, Surf 50, Air Slash 52, Psychic 58, Muddy Water 60 | Mantine |
| Toxapex | super rod | 45 | Oxide | Toxic, Venom Drench, Poison Jab, Liquidation | nothing | Toxapex |
| Toxapex | super rod | 45 | Rewrite | Toxic, Venom Drench, Poison Jab, Liquidation | Sludge Bomb 48, Ice Beam 50, Iron Defense 64 | Toxapex |
| Greninja | surf | 46 | Oxide | Fling, Scald, Dark Pulse, Extrasensory | Sludge Wave 47, Gunk Shot 51, Hydro Pump 55, Hydro Cannon 65 | Greninja |
| Greninja | surf | 46 | Rewrite | Scald, Dark Pulse, Bounce, Extrasensory | Sludge Wave 47, Water Shuriken 49, Gunk Shot 51, Throat Chop 56, Hydro Cannon 65 | Greninja |
| Corviknight | wild | 47 to 50 | Oxide | FeatherDance, Revenge, Defog, Iron Head | Brave Bird 49, Body Press 55, Roost 65 | Corviknight |
| Corviknight | wild | 47 to 50 | Rewrite | Defog, Iron Head, U-turn, Power Trip | Brave Bird 49, Double-Edge 53, Body Press 55, Shift Gear 57, Body Slam 61, Roost 65 | Corviknight |
| Absol | wild | 48 | Oxide | Double Team, Slash, Future Sight, Sucker Punch | Detect 49, Night Slash 52, Me First 57, Psycho Cut 60, Perish Song 65 | Absol |
| Absol | wild | 48 | Rewrite | Slash, Future Sight, Sucker Punch, X-Scissor | Kowtow Cleave 50, Night Slash 52, Shadow Ball 54, Sacred Sword 56, Psycho Cut 60, Play Rough 62, Perish Song 65 | Absol |
| Altaria | wild | 48 | Oxide | Natural Gift, DragonBreath, Dragon Dance, Refresh | Dragon Pulse 54, Perish Song 62 | Altaria |
| Altaria | wild | 48 | Rewrite | DragonBreath, Bulldoze, Refresh, Dragon Rush | Dragon Pulse 54, Draco Meteor 56, Perish Song 62 | Altaria |
| Araquanid | wild | 48 to 49 | Oxide | Soak, Dive, Lunge, Scald | Hydro Pump 51, Liquidation 55, Leech Life 61 | Araquanid |
| Araquanid | wild | 48 to 49 | Rewrite | Dive, Lunge, Skitter Smack, Scald | Poison Jab 51, Liquidation 55, Ice Fang 59, Leech Life 61 | Araquanid |
| Mienshao | wild | 48 | Oxide | Aura Sphere, Me First, Jump Kick, Dual Chop | Focus Blast 51, Acrobatics 55, Hi Jump Kick 64 | Mienshao |
| Mienshao | wild | 48 | Rewrite | Aura Sphere, Low Sweep, Jump Kick, Dual Chop | U-turn 50, Victory Dance 52, Acrobatics 55, Rock Tomb 57, Hammer Arm 59, Hi Jump Kick 64 | Mienshao |
| Poliwrath | super rod | 48 | Oxide | Hypnosis, DoubleSlap, Submission, DynamicPunch | Mind Reader 53 | Poliwrath |
| Poliwrath | super rod | 48 | Rewrite | Throat Chop, Brick Break, Body Press, Jet Punch | Victory Dance 50, Mind Reader 53, Rock Tomb 55, Low Sweep 57, Ice Punch 62, Drain Punch 64 | Poliwrath |
| Relicanth | super rod | 48 | Oxide | Yawn, Take Down, Mud Sport, AncientPower | Double-Edge 50, Dive 57, Rest 64 | Relicanth |
| Relicanth | super rod | 48 | Rewrite | Yawn, Take Down, AncientPower, Bulldoze | Double-Edge 50, Scale Shot 54, Dive 57, Aqua Tail 62, Rest 64 | Relicanth |
| Skarmory | wild | 48 to 49 | Oxide | Steel Wing, Air Slash, Slash, Night Slash | nothing | Skarmory |
| Skarmory | wild | 48 to 49 | Rewrite | Agility, Slash, Swift, Night Slash | Dual Wingbeat 54, Iron Head 56, Rock Tomb 62, Body Press 64 | Skarmory |
| Talonflame | wild | 48 | Oxide | Natural Gift, Acrobatics, Me First, Tailwind | Flare Blitz 51, Brave Bird 55 | Talonflame |
| Talonflame | wild | 48 | Rewrite | Acrobatics, Steel Wing, U-turn, Tailwind | Flare Blitz 51, Brave Bird 55, Overheat 57, Agility 59, Bulk Up 64 | Talonflame |
| Toucannon | wild | 48 to 49 | Oxide | Screech, Drill Peck, Bullet Seed, FeatherDance | Hyper Voice 50 | Toucannon |
| Toucannon | wild | 48 to 49 | Rewrite | Drill Peck, Bullet Seed, Throat Chop, FeatherDance | Hyper Voice 50, Bounce 52, Take Down 58, Body Slam 60 | Toucannon |
| Carbink | wild | 49 | Oxide | Stealth Rock, Skill Swap, Light Screen, Power Gem | Moonblast 52, Stone Edge 54 | Carbink |
| Carbink | wild | 49 | Rewrite | Stealth Rock, Skill Swap, Light Screen, Power Gem | Moonblast 52, Iron Head 54, Diamond Storm 56, Psychic 59, Body Press 61 | Carbink |
| Floatzel | wild | 50 | Oxide | Crunch, Agility, Whirlpool, Razor Wind | nothing | Floatzel |
| Floatzel | wild | 50 | Rewrite | Rock Tomb, Whirlpool, BubbleBeam, Agility | Triple Dive 54 | Floatzel |
| Shellos | wild | 50 | Oxide | Hidden Power, Body Slam, Muddy Water, Recover | as Gastrodon: Recover 54 | Gastrodon (from 51) |
| Shellos | wild | 50 | Rewrite | Hidden Power, Body Slam, Muddy Water, Recover | as Gastrodon: Thousand Waves 52, Recover 54, Skitter Smack 58, Rock Tomb 60 | Gastrodon (from 51) |
| Kingdra | super rod | 51 | Oxide | Twister, Brine, Hydro Pump, Dragon Dance | Dragon Pulse 57 | Kingdra |
| Kingdra | super rod | 51 | Rewrite | Twister, Brine, Aurora Beam, Octazooka | Scale Shot 54, Snipe Shot 55, Dragon Pulse 57, Dragon Dance 58, Core Enforcer 62, Bounce 65 | Kingdra |

## Route 227

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 65 | At the cap |
|---|---|---|---|---|---|---|
| Chinchou | old rod | 22 | Oxide | Flail, Water Gun, Confuse Ray, Spark | Take Down 23; as Lanturn: Stockpile 27, Swallow 27, Spit Up 27, BubbleBeam 30, Signal Beam 35, Discharge 40, Aqua Ring 47, Hydro Pump 52, Charge 57 | Lanturn (from 27) |
| Chinchou | old rod | 22 | Rewrite | Chilling Water, Confuse Ray, Icy Wind, Spark | Take Down 23, ParabolicCharge 25; as Lanturn: Stockpile 27, Swallow 28, Spit Up 29, BubbleBeam 30, Signal Beam 35, Discharge 40, Thunderbolt 42, Aqua Ring 47, Muddy Water 52, Charge 57, Flash Cannon 59, Scald 61 | Lanturn (from 27) |
| Tentacool | old rod | 22 | Oxide | Acid, Toxic Spikes, BubbleBeam, Wrap | Barrier 26, Water Pulse 29; as Tentacruel: Poison Jab 36, Screech 42, Hydro Pump 49, Wring Out 55 | Tentacruel (from 30) |
| Tentacool | old rod | 22 | Rewrite | Acid, Toxic Spikes, Icy Wind, BubbleBeam | Barrier 26, Water Pulse 29; as Tentacruel: Psybeam 34, Poison Jab 36, Scald 38, Screech 42, Surf 49, Sludge Wave 52, Sludge Bomb 54, Muddy Water 58, Power Gem 60 | Tentacruel (from 30) |
| Barboach | old rod | 24 | Oxide | Water Gun, Mud Bomb, Amnesia, Water Pulse | Magnitude 26; as Whiscash: Rest 33, Snore 33, Aqua Tail 39, Earthquake 45, Future Sight 51, Fissure 57 | Whiscash (from 30) |
| Barboach | old rod | 24 | Rewrite | Water Gun, Mud Bomb, Amnesia, Water Pulse | Magnitude 26, Bulldoze 27, Tickle 28; as Whiscash: Rest 33, Rock Tomb 35, Aqua Tail 39, Zen Headbutt 42, Earthquake 45, Future Sight 51, Bounce 53 | Whiscash (from 30) |
| Goldeen | old rod | 24 | Oxide | Supersonic, Horn Attack, Water Pulse, Flail | Aqua Ring 27, Fury Attack 31; as Seaking: Waterfall 40, Horn Drill 47, Agility 56, Megahorn 63 | Seaking (from 33) |
| Goldeen | old rod | 24 | Rewrite | Horn Attack, Water Pulse, Agility, Flail | Aqua Ring 27; as Seaking: Scale Shot 33, Skull Bash 35, Waterfall 40, Poison Jab 42, Throat Chop 44, Fillet Away 46, Flip Turn 50, Liquidation 52, Agility 56, Megahorn 63 | Seaking (from 33) |
| Frogadier | old rod | 26 | Oxide | Icy Wind, Faint Attack, Acrobatics, Low Kick | Waterfall 30, Fling 35; as Greninja: Scald 37, Dark Pulse 40, Extrasensory 43, Sludge Wave 47, Gunk Shot 51, Hydro Pump 55, Hydro Cannon 65 | Greninja (from 36) |
| Frogadier | old rod | 26 | Rewrite | Thief, Faint Attack, Acrobatics, Low Kick | Waterfall 30, Fling 35; as Greninja: Shadow Sneak 36, Scald 37, Dark Pulse 40, Bounce 41, Extrasensory 43, Sludge Wave 47, Water Shuriken 49, Gunk Shot 51, Throat Chop 56, Hydro Cannon 65 | Greninja (from 36) |
| Goldeen | good rod | 35 | Oxide | Water Pulse, Flail, Aqua Ring, Fury Attack | as Seaking: Waterfall 40, Horn Drill 47, Agility 56, Megahorn 63 | Seaking (from 36) |
| Goldeen | good rod | 35 | Rewrite | Water Pulse, Agility, Flail, Aqua Ring | as Seaking: Waterfall 40, Poison Jab 42, Throat Chop 44, Fillet Away 46, Flip Turn 50, Liquidation 52, Agility 56, Megahorn 63 | Seaking (from 36) |
| Golduck | good rod | 35 | Oxide | Confusion, Water Pulse, Fury Swipes, Screech | Psych Up 37, Zen Headbutt 44, Amnesia 50, Hydro Pump 56 | Golduck |
| Golduck | good rod | 35 | Rewrite | Water Pulse, Fury Swipes, Screech, Aurora Beam | Psych Up 37, Scald 39, Surf 42, Zen Headbutt 44, Aqua Step 47, Amnesia 50, Muddy Water 56, Power Gem 58, Ice Beam 60 | Golduck |
| Barboach | good rod | 37 | Oxide | Magnitude, Rest, Snore, Aqua Tail | as Whiscash: Aqua Tail 39, Earthquake 45, Future Sight 51, Fissure 57 | Whiscash (from 38) |
| Barboach | good rod | 37 | Rewrite | Bulldoze, Tickle, Rest, Aqua Tail | as Whiscash: Aqua Tail 39, Zen Headbutt 42, Earthquake 45, Future Sight 51, Bounce 53 | Whiscash (from 38) |
| Feebas | good rod | 37 | Oxide | Splash, Tackle, Flail | as Milotic: Attract 41, Safeguard 45, Aqua Ring 49 | Milotic (from 38) |
| Feebas | good rod | 37 | Rewrite | Water Pulse, Tackle, Captivate, Flail | as Milotic: Attract 41, Safeguard 45, Aqua Ring 49, Alluring Voice 51, Muddy Water 54, Scald 58, DragonBreath 60, Earth Power 62 | Milotic (from 38) |
| Starmie | good rod | 39 | Oxide | Rapid Spin, Recover, Swift, Confuse Ray | nothing | Starmie |
| Starmie | good rod | 39 | Rewrite | Swift, Icy Wind, Psybeam, Confuse Ray | Skitter Smack 45, Power Gem 54, Flash Cannon 56, Luster Purge 61, Swagger 62 | Starmie |
| Feebas | surf | 40 | Oxide | Splash, Tackle, Flail | as Milotic: Attract 41, Safeguard 45, Aqua Ring 49 | Milotic (from 41) |
| Feebas | surf | 40 | Rewrite | Water Pulse, Tackle, Captivate, Flail | as Milotic: Attract 41, Safeguard 45, Aqua Ring 49, Alluring Voice 51, Muddy Water 54, Scald 58, DragonBreath 60, Earth Power 62 | Milotic (from 41) |
| Gastrodon | surf | 40 | Oxide | Water Pulse, Mud Bomb, Hidden Power, Body Slam | Muddy Water 41, Recover 54 | Gastrodon |
| Gastrodon | surf | 40 | Rewrite | Hidden Power, Body Slam, AncientPower, Clear Smog | Muddy Water 41, Earth Power 43, Bulldoze 45, Ice Beam 50, Thousand Waves 52, Recover 54, Skitter Smack 58, Rock Tomb 60 | Gastrodon |
| Corphish | surf | 43 | Oxide | Knock Off, Taunt, Night Slash, Crabhammer | Swords Dance 44; as Crawdaunt: Crabhammer 44, Swords Dance 52, Crunch 57, Guillotine 65 | Crawdaunt (from 44) |
| Corphish | surf | 43 | Rewrite | BubbleBeam, Knock Off, Night Slash, Crabhammer | Swords Dance 44; as Crawdaunt: Crabhammer 44, Swords Dance 52, Crunch 57, Razor Shell 59, Throat Chop 61 | Crawdaunt (from 44) |
| Goldeen | surf | 43 | Oxide | Aqua Ring, Fury Attack, Waterfall, Horn Drill | as Seaking: Horn Drill 47, Agility 56, Megahorn 63 | Seaking (from 44) |
| Goldeen | surf | 43 | Rewrite | Agility, Flail, Aqua Ring, Waterfall | as Seaking: Throat Chop 44, Fillet Away 46, Flip Turn 50, Liquidation 52, Agility 56, Megahorn 63 | Seaking (from 44) |
| Seaking | super rod | 45 | Oxide | Flail, Aqua Ring, Fury Attack, Waterfall | Horn Drill 47, Agility 56, Megahorn 63 | Seaking |
| Seaking | super rod | 45 | Rewrite | Skull Bash, Waterfall, Poison Jab, Throat Chop | Fillet Away 46, Flip Turn 50, Liquidation 52, Agility 56, Megahorn 63 | Seaking |
| Whiscash | super rod | 45 | Oxide | Rest, Snore, Aqua Tail, Earthquake | Future Sight 51, Fissure 57 | Whiscash |
| Whiscash | super rod | 45 | Rewrite | Rock Tomb, Aqua Tail, Zen Headbutt, Earthquake | Future Sight 51, Bounce 53 | Whiscash |
| Corsola | surf | 46 | Oxide | AncientPower, Aqua Ring, Spike Cannon, Power Gem | Mirror Coat 48, Earth Power 53 | Corsola |
| Corsola | surf | 46 | Rewrite | Aqua Ring, Bulldoze, Power Gem, Waterfall | Mirror Coat 48, Earth Power 53, Throat Chop 55, Liquidation 57, Rock Tomb 59, Confuse Ray 65 | Corsola |
| Crawdaunt | super rod | 48 | Oxide | Swift, Taunt, Night Slash, Crabhammer | Swords Dance 52, Crunch 57, Guillotine 65 | Crawdaunt |
| Crawdaunt | super rod | 48 | Rewrite | Avalanche, Night Slash, Rock Tomb, Crabhammer | Swords Dance 52, Crunch 57, Razor Shell 59, Throat Chop 61 | Crawdaunt |
| Milotic | super rod | 48 | Oxide | Aqua Tail, Hydro Pump, Attract, Safeguard | Aqua Ring 49 | Milotic |
| Milotic | super rod | 48 | Rewrite | Icy Wind, Surf, Attract, Safeguard | Aqua Ring 49, Alluring Voice 51, Muddy Water 54, Scald 58, DragonBreath 60, Earth Power 62 | Milotic |
| Ceruledge | wild | 51 | Oxide | Lava Plume, Swords Dance, Ally Switch, Bitter Blade | Psycho Cut 56, Flare Blitz 62 | Ceruledge |
| Ceruledge | wild | 51 | Rewrite | Lava Plume, Swords Dance, Night Slash, Bitter Blade | Iron Head 53, Psycho Cut 56, Flare Blitz 62 | Ceruledge |
| Sharpedo | super rod | 51 | Oxide | Aqua Jet, Taunt, Agility, Skull Bash | Night Slash 56 | Sharpedo |
| Sharpedo | super rod | 51 | Rewrite | Taunt, Poison Fang, Agility, Skull Bash | Triple Dive 54, Night Slash 56, Fire Fang 58, Poison Jab 60 | Sharpedo |
| Houndoom | wild | 52 to 53 | Oxide | Fire Fang, Faint Attack, Embargo, Flamethrower | Crunch 54, Nasty Plot 60 | Houndoom |
| Houndoom | wild | 52 to 53 | Rewrite | Mud Shot, Embargo, Flamethrower, Dark Pulse | Crunch 54, Fiery Wrath 56, Shadow Ball 58, Nasty Plot 60, Toxic 62 | Houndoom |
| Ninetales | wild | 52 | Oxide | Quick Attack, Confuse Ray, Safeguard, Flare Blitz | nothing | Ninetales |
| Ninetales | wild | 52 | Rewrite | Confuse Ray, Safeguard, Alluring Voice, Flare Blitz | Energy Ball 54, Extrasensory 56, Mystical Fire 62, Bite 64 | Ninetales |
| Rapidash | wild | 52 | Oxide | Agility, Fire Blast, Fury Attack, Bounce | Flare Blitz 56 | Rapidash |
| Rapidash | wild | 52 | Rewrite | Bounce, Fire Lash, Poison Jab, Drill Run | Overheat 53, Flare Blitz 56, Charm 61 | Rapidash |
| Rhyperior | wild | 52 | Oxide | Horn Drill, Hammer Arm, Stone Edge, Earthquake | Megahorn 57, Rock Wrecker 61 | Rhyperior |
| Rhyperior | wild | 52 | Rewrite | Rock Blast, Take Down, Hammer Arm, Earthquake | Megahorn 57, Rock Wrecker 61 | Rhyperior |
| Salazzle | wild | 52 to 53 | Oxide | Venoshock, Flamethrower, Sludge Bomb, Dragon Pulse | Fire Blast 55 | Salazzle |
| Salazzle | wild | 52 to 53 | Rewrite | Sludge Bomb, Encore, Dragon Pulse, Nasty Plot | nothing | Salazzle |
| Skarmory | wild | 52 | Oxide | Steel Wing, Air Slash, Slash, Night Slash | nothing | Skarmory |
| Skarmory | wild | 52 | Rewrite | Agility, Slash, Swift, Night Slash | Dual Wingbeat 54, Iron Head 56, Rock Tomb 62, Body Press 64 | Skarmory |
| Weezing | wild | 52 | Oxide | Haze, Double Hit, Explosion, Sludge Bomb | Destiny Bond 55, Memento 63 | Weezing |
| Weezing | wild | 52 | Rewrite | Sludge Wave, Psybeam, Sludge Bomb, Heat Wave | Shadow Ball 56, Poison Fang 58, Thunderbolt 64 | Weezing |
| Magcargo | wild | 53 | Oxide | Amnesia, Lava Plume, Rock Slide, Body Slam | Flamethrower 61 | Magcargo |
| Magcargo | wild | 53 | Rewrite | Scorching Sands, Rock Slide, Shell Smash, Body Slam | Power Gem 56, Flamethrower 61, Torch Song 63, Energy Ball 64 | Magcargo |
| Turtonator | wild | 53 | Oxide | Body Slam, Flamethrower, Dragon Pulse, Fire Spin | Explosion 55, Overheat 61 | Turtonator |
| Turtonator | wild | 53 | Rewrite | Dragon Pulse, Shell Smash, Fire Spin, Heat Crash | Scale Shot 54, Overheat 61, Body Press 63 | Turtonator |
| Chatot | wild | 54 | Oxide | Roost, Uproar, FeatherDance, Hyper Voice | nothing | Chatot |
| Chatot | wild | 54 | Rewrite | FeatherDance, Hyper Voice, Heat Wave, Uproar | Air Slash 56, U-turn 58, Steel Wing 64 | Chatot |
| Garganacl | wild | 54 | Oxide | Stealth Rock, Heavy Slam, Earthquake, Stone Edge | Explosion 60 | Garganacl |
| Garganacl | wild | 54 | Rewrite | Heavy Slam, Earthquake, Diamond Storm, Rock Blast | Fire Punch 56, Ice Punch 58, Body Press 64 | Garganacl |
| Honchkrow | wild | 54 | Oxide | Wing Attack, Swagger, Nasty Plot, Night Slash | Dark Pulse 55 | Honchkrow |
| Honchkrow | wild | 54 | Rewrite | Night Slash, Nasty Plot, Oblivion Wing, Sucker Punch | Dark Pulse 55, Heat Wave 61, Mean Look 63 | Honchkrow |

## Route 228

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 65 | At the cap |
|---|---|---|---|---|---|---|
| Buizel | old rod | 22 | Oxide | Water Gun, Pursuit, Swift, Aqua Jet | as Floatzel: Crunch 26, Agility 29, Whirlpool 39, Razor Wind 50 | Floatzel (from 26) |
| Buizel | old rod | 22 | Rewrite | Scary Face, Pursuit, Swift, Aqua Jet | as Floatzel: Crunch 26, Low Sweep 28, Icy Wind 30, Rock Tomb 35, Whirlpool 39, BubbleBeam 43, Agility 45, Triple Dive 54 | Floatzel (from 26) |
| Goldeen | old rod | 22 | Oxide | Supersonic, Horn Attack, Water Pulse, Flail | Aqua Ring 27, Fury Attack 31; as Seaking: Waterfall 40, Horn Drill 47, Agility 56, Megahorn 63 | Seaking (from 33) |
| Goldeen | old rod | 22 | Rewrite | Horn Attack, Water Pulse, Agility, Flail | Aqua Ring 27; as Seaking: Scale Shot 33, Skull Bash 35, Waterfall 40, Poison Jab 42, Throat Chop 44, Fillet Away 46, Flip Turn 50, Liquidation 52, Agility 56, Megahorn 63 | Seaking (from 33) |
| Barboach | old rod | 24 | Oxide | Water Gun, Mud Bomb, Amnesia, Water Pulse | Magnitude 26; as Whiscash: Rest 33, Snore 33, Aqua Tail 39, Earthquake 45, Future Sight 51, Fissure 57 | Whiscash (from 30) |
| Barboach | old rod | 24 | Rewrite | Water Gun, Mud Bomb, Amnesia, Water Pulse | Magnitude 26, Bulldoze 27, Tickle 28; as Whiscash: Rest 33, Rock Tomb 35, Aqua Tail 39, Zen Headbutt 42, Earthquake 45, Future Sight 51, Bounce 53 | Whiscash (from 30) |
| Krabby | old rod | 24 | Oxide | Harden, BubbleBeam, Mud Shot, Metal Claw | Stomp 25; as Kingler: Protect 32, Guillotine 37, Slam 44, Brine 51, Crabhammer 56, Flail 63 | Kingler (from 28) |
| Krabby | old rod | 24 | Rewrite | Leer, BubbleBeam, Aqua Jet, Mud Shot | Stomp 25, Brutal Swing 27; as Kingler: Rock Tomb 34, Secret Power 36, Slam 44, Brine 51, Crabhammer 56, Ice Punch 58, Flail 63 | Kingler (from 28) |
| Clamperl | old rod | 26 | Oxide | Clamp, Water Gun, Whirlpool, Iron Defense | as Huntail: Brine 28, Baton Pass 33, Dive 37, Crunch 42, Aqua Tail 46, Hydro Pump 51 | Huntail (from 26) |
| Clamperl | old rod | 26 | Oxide | Clamp, Water Gun, Whirlpool, Iron Defense | as Gorebyss: Captivate 28, Baton Pass 33, Dive 37, Psychic 42, Aqua Tail 46, Hydro Pump 51 | Gorebyss (from 26) |
| Clamperl | old rod | 26 | Rewrite | Whirlpool, Iron Defense, Bite, Chilling Water | as Huntail: Brine 28, Bulldoze 34, Dive 37, Crunch 42, Aqua Tail 46, Shell Smash 50, Muddy Water 51, Rock Tomb 56, Sucker Punch 58, Confuse Ray 64 | Huntail (from 26) |
| Clamperl | old rod | 26 | Rewrite | Whirlpool, Iron Defense, Bite, Chilling Water | as Gorebyss: Captivate 28, Baton Pass 33, Draining Kiss 35, Dive 37, Scald 40, Psychic 42, Aqua Tail 46, Shadow Ball 48, Muddy Water 51, Ice Beam 56, Shell Smash 64 | Gorebyss (from 26) |
| Gastrodon | good rod | 35 | Oxide | Water Pulse, Mud Bomb, Hidden Power, Body Slam | Muddy Water 41, Recover 54 | Gastrodon |
| Gastrodon | good rod | 35 | Rewrite | Hidden Power, Body Slam, AncientPower, Clear Smog | Muddy Water 41, Earth Power 43, Bulldoze 45, Ice Beam 50, Thousand Waves 52, Recover 54, Skitter Smack 58, Rock Tomb 60 | Gastrodon |
| Goldeen | good rod | 35 | Oxide | Water Pulse, Flail, Aqua Ring, Fury Attack | as Seaking: Waterfall 40, Horn Drill 47, Agility 56, Megahorn 63 | Seaking (from 36) |
| Goldeen | good rod | 35 | Rewrite | Water Pulse, Agility, Flail, Aqua Ring | as Seaking: Waterfall 40, Poison Jab 42, Throat Chop 44, Fillet Away 46, Flip Turn 50, Liquidation 52, Agility 56, Megahorn 63 | Seaking (from 36) |
| Barboach | good rod | 37 | Oxide | Magnitude, Rest, Snore, Aqua Tail | as Whiscash: Aqua Tail 39, Earthquake 45, Future Sight 51, Fissure 57 | Whiscash (from 38) |
| Barboach | good rod | 37 | Rewrite | Bulldoze, Tickle, Rest, Aqua Tail | as Whiscash: Aqua Tail 39, Zen Headbutt 42, Earthquake 45, Future Sight 51, Bounce 53 | Whiscash (from 38) |
| Corphish | good rod | 37 | Oxide | Protect, Knock Off, Taunt, Night Slash | Crabhammer 38; as Crawdaunt: Night Slash 39, Crabhammer 44, Swords Dance 52, Crunch 57, Guillotine 65 | Crawdaunt (from 38) |
| Corphish | good rod | 37 | Rewrite | Metal Claw, BubbleBeam, Knock Off, Night Slash | Crabhammer 38; as Crawdaunt: Night Slash 39, Rock Tomb 42, Crabhammer 44, Swords Dance 52, Crunch 57, Razor Shell 59, Throat Chop 61 | Crawdaunt (from 38) |
| Masquerain | good rod | 39 | Oxide | Water Sport, Gust, Scary Face, Stun Spore | Silver Wind 40, Air Slash 47, Whirlwind 54, Bug Buzz 61 | Masquerain |
| Masquerain | good rod | 39 | Rewrite | Scary Face, Ominous Wind, Stun Spore, Icy Wind | Silver Wind 40, Bug Buzz 44, Air Slash 47, Quiver Dance 52, Lunge 54, Leech Life 59, Waterfall 61 | Masquerain |
| Gastrodon | surf | 40 | Oxide | Water Pulse, Mud Bomb, Hidden Power, Body Slam | Muddy Water 41, Recover 54 | Gastrodon |
| Gastrodon | surf | 40 | Rewrite | Hidden Power, Body Slam, AncientPower, Clear Smog | Muddy Water 41, Earth Power 43, Bulldoze 45, Ice Beam 50, Thousand Waves 52, Recover 54, Skitter Smack 58, Rock Tomb 60 | Gastrodon |
| Quagsire | surf | 40 | Oxide | Mud Bomb, Amnesia, Yawn, Earthquake | Mist 48, Haze 48, Muddy Water 53 | Quagsire |
| Quagsire | surf | 40 | Rewrite | Bulldoze, Yawn, Earthquake, Poison Jab | Rock Slide 43, Thousand Waves 45, Mist 48, Ice Punch 51, Muddy Water 53, Liquidation 59, Rock Tomb 61 | Quagsire |
| Ludicolo | surf | 43 | Oxide | Astonish, Growl, Mega Drain, Nature Power | nothing | Ludicolo |
| Ludicolo | surf | 43 | Rewrite | Nature Power, Icy Wind, Scald, Mud Shot | Muddy Water 54, Giga Drain 56, Dark Pulse 58, Energy Ball 62, Leech Seed 64 | Ludicolo |
| Masquerain | surf | 43 | Oxide | Gust, Scary Face, Stun Spore, Silver Wind | Air Slash 47, Whirlwind 54, Bug Buzz 61 | Masquerain |
| Masquerain | surf | 43 | Rewrite | Ominous Wind, Stun Spore, Icy Wind, Silver Wind | Bug Buzz 44, Air Slash 47, Quiver Dance 52, Lunge 54, Leech Life 59, Waterfall 61 | Masquerain |
| Seaking | super rod | 45 | Oxide | Flail, Aqua Ring, Fury Attack, Waterfall | Horn Drill 47, Agility 56, Megahorn 63 | Seaking |
| Seaking | super rod | 45 | Rewrite | Skull Bash, Waterfall, Poison Jab, Throat Chop | Fillet Away 46, Flip Turn 50, Liquidation 52, Agility 56, Megahorn 63 | Seaking |
| Whiscash | super rod | 45 | Oxide | Rest, Snore, Aqua Tail, Earthquake | Future Sight 51, Fissure 57 | Whiscash |
| Whiscash | super rod | 45 | Rewrite | Rock Tomb, Aqua Tail, Zen Headbutt, Earthquake | Future Sight 51, Bounce 53 | Whiscash |
| Tentacruel | surf | 46 | Oxide | Barrier, Water Pulse, Poison Jab, Screech | Hydro Pump 49, Wring Out 55 | Tentacruel |
| Tentacruel | surf | 46 | Rewrite | Psybeam, Poison Jab, Scald, Screech | Surf 49, Sludge Wave 52, Sludge Bomb 54, Muddy Water 58, Power Gem 60 | Tentacruel |
| Crawdaunt | super rod | 48 | Oxide | Swift, Taunt, Night Slash, Crabhammer | Swords Dance 52, Crunch 57, Guillotine 65 | Crawdaunt |
| Crawdaunt | super rod | 48 | Rewrite | Avalanche, Night Slash, Rock Tomb, Crabhammer | Swords Dance 52, Crunch 57, Razor Shell 59, Throat Chop 61 | Crawdaunt |
| Lanturn | super rod | 48 | Oxide | BubbleBeam, Signal Beam, Discharge, Aqua Ring | Hydro Pump 52, Charge 57 | Lanturn |
| Lanturn | super rod | 48 | Rewrite | Signal Beam, Discharge, Thunderbolt, Aqua Ring | Muddy Water 52, Charge 57, Flash Cannon 59, Scald 61 | Lanturn |
| Whiscash | wild | 49 | Oxide | Rest, Snore, Aqua Tail, Earthquake | Future Sight 51, Fissure 57 | Whiscash |
| Whiscash | wild | 49 | Rewrite | Rock Tomb, Aqua Tail, Zen Headbutt, Earthquake | Future Sight 51, Bounce 53 | Whiscash |
| Crustle | wild | 50 | Oxide | Rock Slide, StompingTantrum, Knock Off, Leech Life | Stone Edge 54, Rock Wrecker 61 | Crustle |
| Crustle | wild | 50 | Rewrite | StompingTantrum, Knock Off, Leech Life, Body Press | Shell Smash 56, Rock Wrecker 61, Skitter Smack 64 | Crustle |
| Donphan | wild | 50 to 51 | Oxide | Fury Attack, Assurance, Scary Face, Earthquake | Giga Impact 54 | Donphan |
| Donphan | wild | 50 to 51 | Rewrite | Scary Face, Knock Off, Fire Fang, Earthquake | Charm 51, Giga Impact 54 | Donphan |
| Flygon | wild | 50 | Oxide | Supersonic, DragonBreath, Screech, Dragon Claw | Hyper Beam 57 | Flygon |
| Flygon | wild | 50 | Rewrite | Sand Tomb, DragonBreath, Screech, Dragon Claw | Dragon Darts 54, Dragon Rush 56, Hyper Beam 57, Poison Fang 62, Fire Punch 64 | Flygon |
| Golem | wild | 50 | Oxide | Earthquake, Explosion, Double-Edge, Stone Edge | nothing | Golem |
| Golem | wild | 50 | Rewrite | Earthquake, Double-Edge, Rock Tomb, Iron Head | ThunderPunch 53, Block 61 | Golem |
| Houndoom | wild | 50 | Oxide | Fire Fang, Faint Attack, Embargo, Flamethrower | Crunch 54, Nasty Plot 60 | Houndoom |
| Houndoom | wild | 50 | Rewrite | Mud Shot, Embargo, Flamethrower, Dark Pulse | Crunch 54, Fiery Wrath 56, Shadow Ball 58, Nasty Plot 60, Toxic 62 | Houndoom |
| Palossand | wild | 50 | Oxide | Giga Drain, Iron Defense, Shadow Ball, Earth Power | Shore Up 57 | Palossand |
| Palossand | wild | 50 | Rewrite | Iron Defense, Shadow Ball, Flash Cannon, Earth Power | Sludge Bomb 53, Shore Up 57, Psychic 61, Energy Ball 63 | Palossand |
| Glimmora | wild | 51 | Oxide | Rock Slide, Power Gem, Acid Armor, Sludge Wave | nothing | Glimmora |
| Glimmora | wild | 51 | Rewrite | Sludge Bomb, Acid Armor, Flash Cannon, Sludge Wave | Energy Ball 56, Dazzling Gleam 58, Confuse Ray 64 | Glimmora |
| Masquerain | super rod | 51 | Oxide | Scary Face, Stun Spore, Silver Wind, Air Slash | Whirlwind 54, Bug Buzz 61 | Masquerain |
| Masquerain | super rod | 51 | Rewrite | Icy Wind, Silver Wind, Bug Buzz, Air Slash | Quiver Dance 52, Lunge 54, Leech Life 59, Waterfall 61 | Masquerain |
| Rhyperior | wild | 51 | Oxide | Horn Drill, Hammer Arm, Stone Edge, Earthquake | Megahorn 57, Rock Wrecker 61 | Rhyperior |
| Rhyperior | wild | 51 | Rewrite | Rock Blast, Take Down, Hammer Arm, Earthquake | Megahorn 57, Rock Wrecker 61 | Rhyperior |
| Salazzle | wild | 51 | Oxide | Venoshock, Flamethrower, Sludge Bomb, Dragon Pulse | Fire Blast 55 | Salazzle |
| Salazzle | wild | 51 | Rewrite | Flamethrower, Sludge Bomb, Encore, Dragon Pulse | Nasty Plot 52 | Salazzle |
| Carbink | wild | 52 | Oxide | Skill Swap, Light Screen, Power Gem, Moonblast | Stone Edge 54 | Carbink |
| Carbink | wild | 52 | Rewrite | Skill Swap, Light Screen, Power Gem, Moonblast | Iron Head 54, Diamond Storm 56, Psychic 59, Body Press 61 | Carbink |
| Garganacl | wild | 52 | Oxide | Rock Slide, Stealth Rock, Heavy Slam, Earthquake | Stone Edge 54, Explosion 60 | Garganacl |
| Garganacl | wild | 52 | Rewrite | Stealth Rock, Heavy Slam, Earthquake, Diamond Storm | Rock Blast 54, Fire Punch 56, Ice Punch 58, Body Press 64 | Garganacl |
| Steelix | wild | 52 | Oxide | Curse, Iron Tail, Crunch, Double-Edge | Stone Edge 54 | Steelix |
| Steelix | wild | 52 | Rewrite | Iron Head, Hard Press, Crunch, Double-Edge | Rock Slide 54, Fire Fang 56, Ice Fang 58, Block 64 | Steelix |

## Route 229

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 65 | At the cap |
|---|---|---|---|---|---|---|
| Barboach | old rod | 22 | Oxide | Water Gun, Mud Bomb, Amnesia, Water Pulse | Magnitude 26; as Whiscash: Rest 33, Snore 33, Aqua Tail 39, Earthquake 45, Future Sight 51, Fissure 57 | Whiscash (from 30) |
| Barboach | old rod | 22 | Rewrite | Water Gun, Mud Bomb, Amnesia, Water Pulse | Magnitude 26, Bulldoze 27, Tickle 28; as Whiscash: Rest 33, Rock Tomb 35, Aqua Tail 39, Zen Headbutt 42, Earthquake 45, Future Sight 51, Bounce 53 | Whiscash (from 30) |
| Goldeen | old rod | 22 | Oxide | Supersonic, Horn Attack, Water Pulse, Flail | Aqua Ring 27, Fury Attack 31; as Seaking: Waterfall 40, Horn Drill 47, Agility 56, Megahorn 63 | Seaking (from 33) |
| Goldeen | old rod | 22 | Rewrite | Horn Attack, Water Pulse, Agility, Flail | Aqua Ring 27; as Seaking: Scale Shot 33, Skull Bash 35, Waterfall 40, Poison Jab 42, Throat Chop 44, Fillet Away 46, Flip Turn 50, Liquidation 52, Agility 56, Megahorn 63 | Seaking (from 33) |
| Corphish | old rod | 24 | Oxide | ViceGrip, Leer, BubbleBeam, Protect | Knock Off 26; as Crawdaunt: Swift 30, Taunt 34, Night Slash 39, Crabhammer 44, Swords Dance 52, Crunch 57, Guillotine 65 | Crawdaunt (from 30) |
| Corphish | old rod | 24 | Rewrite | ViceGrip, Leer, Metal Claw, BubbleBeam | Knock Off 26; as Crawdaunt: Swift 30, Taunt 34, Avalanche 36, Night Slash 39, Rock Tomb 42, Crabhammer 44, Swords Dance 52, Crunch 57, Razor Shell 59, Throat Chop 61 | Crawdaunt (from 30) |
| Poliwag | old rod | 24 | Oxide | Hypnosis, Water Gun, DoubleSlap, Body Slam | BubbleBeam 25; as Poliwrath: DynamicPunch 43, Mind Reader 53 | Poliwrath (from 25) |
| Poliwag | old rod | 24 | Oxide | Hypnosis, Water Gun, DoubleSlap, Body Slam | BubbleBeam 25; as Politoed: Swagger 27, Bounce 37, Hyper Voice 48 | Politoed (from 25) |
| Poliwag | old rod | 24 | Rewrite | Bubble, Hypnosis, Fury Swipes, Body Slam | BubbleBeam 25; as Poliwhirl: Bulldoze 25; as Poliwrath: Wake-Up Slap 35, Circle Throw 38, Throat Chop 40, Brick Break 43, Body Press 45, Jet Punch 46, Victory Dance 50, Mind Reader 53, Rock Tomb 55, Low Sweep 57, Ice Punch 62, Drain Punch 64 | Poliwrath (from 25) |
| Poliwag | old rod | 24 | Rewrite | Bubble, Hypnosis, Fury Swipes, Body Slam | BubbleBeam 25; as Poliwhirl: Bulldoze 25; as Politoed: Swagger 27, Bounce 37, Scald 39, Hyper Voice 48, Ice Beam 57, Muddy Water 59, Belly Drum 65 | Politoed (from 25) |
| Masquerain | old rod | 26 | Oxide | Sweet Scent, Water Sport, Gust, Scary Face | Stun Spore 33, Silver Wind 40, Air Slash 47, Whirlwind 54, Bug Buzz 61 | Masquerain |
| Masquerain | old rod | 26 | Rewrite | Water Sport, Gust, Mud Shot, Scary Face | Ominous Wind 28, Stun Spore 33, Icy Wind 35, Silver Wind 40, Bug Buzz 44, Air Slash 47, Quiver Dance 52, Lunge 54, Leech Life 59, Waterfall 61 | Masquerain |
| Barboach | good rod | 35 | Oxide | Magnitude, Rest, Snore, Aqua Tail | as Whiscash: Aqua Tail 39, Earthquake 45, Future Sight 51, Fissure 57 | Whiscash (from 36) |
| Barboach | good rod | 35 | Rewrite | Bulldoze, Tickle, Rest, Aqua Tail | as Whiscash: Aqua Tail 39, Zen Headbutt 42, Earthquake 45, Future Sight 51, Bounce 53 | Whiscash (from 36) |
| Goldeen | good rod | 35 | Oxide | Water Pulse, Flail, Aqua Ring, Fury Attack | as Seaking: Waterfall 40, Horn Drill 47, Agility 56, Megahorn 63 | Seaking (from 36) |
| Goldeen | good rod | 35 | Rewrite | Water Pulse, Agility, Flail, Aqua Ring | as Seaking: Waterfall 40, Poison Jab 42, Throat Chop 44, Fillet Away 46, Flip Turn 50, Liquidation 52, Agility 56, Megahorn 63 | Seaking (from 36) |
| Chinchou | good rod | 37 | Oxide | Take Down, BubbleBeam, Signal Beam, Discharge | as Lanturn: Discharge 40, Aqua Ring 47, Hydro Pump 52, Charge 57 | Lanturn (from 38) |
| Chinchou | good rod | 37 | Rewrite | ParabolicCharge, BubbleBeam, Signal Beam, Discharge | as Lanturn: Discharge 40, Thunderbolt 42, Aqua Ring 47, Muddy Water 52, Charge 57, Flash Cannon 59, Scald 61 | Lanturn (from 38) |
| Corphish | good rod | 37 | Oxide | Protect, Knock Off, Taunt, Night Slash | Crabhammer 38; as Crawdaunt: Night Slash 39, Crabhammer 44, Swords Dance 52, Crunch 57, Guillotine 65 | Crawdaunt (from 38) |
| Corphish | good rod | 37 | Rewrite | Metal Claw, BubbleBeam, Knock Off, Night Slash | Crabhammer 38; as Crawdaunt: Night Slash 39, Rock Tomb 42, Crabhammer 44, Swords Dance 52, Crunch 57, Razor Shell 59, Throat Chop 61 | Crawdaunt (from 38) |
| Ludicolo | good rod | 39 | Oxide | Astonish, Growl, Mega Drain, Nature Power | nothing | Ludicolo |
| Ludicolo | good rod | 39 | Rewrite | Mega Drain, Nature Power, Icy Wind, Scald | Mud Shot 40, Muddy Water 54, Giga Drain 56, Dark Pulse 58, Energy Ball 62, Leech Seed 64 | Ludicolo |
| Ludicolo | surf | 40 | Oxide | Astonish, Growl, Mega Drain, Nature Power | nothing | Ludicolo |
| Ludicolo | surf | 40 | Rewrite | Nature Power, Icy Wind, Scald, Mud Shot | Muddy Water 54, Giga Drain 56, Dark Pulse 58, Energy Ball 62, Leech Seed 64 | Ludicolo |
| Quagsire | surf | 40 | Oxide | Mud Bomb, Amnesia, Yawn, Earthquake | Mist 48, Haze 48, Muddy Water 53 | Quagsire |
| Quagsire | surf | 40 | Rewrite | Bulldoze, Yawn, Earthquake, Poison Jab | Rock Slide 43, Thousand Waves 45, Mist 48, Ice Punch 51, Muddy Water 53, Liquidation 59, Rock Tomb 61 | Quagsire |
| Goldeen | surf | 43 | Oxide | Aqua Ring, Fury Attack, Waterfall, Horn Drill | as Seaking: Horn Drill 47, Agility 56, Megahorn 63 | Seaking (from 44) |
| Goldeen | surf | 43 | Rewrite | Agility, Flail, Aqua Ring, Waterfall | as Seaking: Throat Chop 44, Fillet Away 46, Flip Turn 50, Liquidation 52, Agility 56, Megahorn 63 | Seaking (from 44) |
| Masquerain | surf | 43 | Oxide | Gust, Scary Face, Stun Spore, Silver Wind | Air Slash 47, Whirlwind 54, Bug Buzz 61 | Masquerain |
| Masquerain | surf | 43 | Rewrite | Ominous Wind, Stun Spore, Icy Wind, Silver Wind | Bug Buzz 44, Air Slash 47, Quiver Dance 52, Lunge 54, Leech Life 59, Waterfall 61 | Masquerain |
| Crawdaunt | super rod | 45 | Oxide | Swift, Taunt, Night Slash, Crabhammer | Swords Dance 52, Crunch 57, Guillotine 65 | Crawdaunt |
| Crawdaunt | super rod | 45 | Rewrite | Avalanche, Night Slash, Rock Tomb, Crabhammer | Swords Dance 52, Crunch 57, Razor Shell 59, Throat Chop 61 | Crawdaunt |
| Whiscash | super rod | 45 | Oxide | Rest, Snore, Aqua Tail, Earthquake | Future Sight 51, Fissure 57 | Whiscash |
| Whiscash | super rod | 45 | Rewrite | Rock Tomb, Aqua Tail, Zen Headbutt, Earthquake | Future Sight 51, Bounce 53 | Whiscash |
| Whiscash | surf | 46 | Oxide | Rest, Snore, Aqua Tail, Earthquake | Future Sight 51, Fissure 57 | Whiscash |
| Whiscash | surf | 46 | Rewrite | Rock Tomb, Aqua Tail, Zen Headbutt, Earthquake | Future Sight 51, Bounce 53 | Whiscash |
| Heracross | wild | 47 | Oxide | Counter, Take Down, Close Combat, Reversal | Feint 49, Megahorn 55 | Heracross |
| Heracross | wild | 47 | Rewrite | Bulldoze, Close Combat, Reversal, Rock Tomb | Megahorn 55, Leech Life 59, Lunge 61 | Heracross |
| Galvantula | wild | 48 | Oxide | Signal Beam, Energy Ball, Sucker Punch, Thunderbolt | Bug Buzz 51, Thunder 55, Volt Switch 65 | Galvantula |
| Galvantula | wild | 48 | Rewrite | Energy Ball, Sucker Punch, Swift, Thunderbolt | Bug Buzz 51, Agility 54, Sludge Bomb 58, Volt Switch 65 | Galvantula |
| Lanturn | super rod | 48 | Oxide | BubbleBeam, Signal Beam, Discharge, Aqua Ring | Hydro Pump 52, Charge 57 | Lanturn |
| Lanturn | super rod | 48 | Rewrite | Signal Beam, Discharge, Thunderbolt, Aqua Ring | Muddy Water 52, Charge 57, Flash Cannon 59, Scald 61 | Lanturn |
| Leavanny | wild | 48 | Oxide | Leaf Blade, X-Scissor, Entrainment, Swords Dance | Leaf Storm 50 | Leavanny |
| Leavanny | wild | 48 | Rewrite | X-Scissor, Entrainment, Swords Dance, Throat Chop | Leaf Storm 50, Lunge 54, Poison Jab 58, Skitter Smack 60 | Leavanny |
| Liepard | wild | 48 | Oxide | Sucker Punch, Nasty Plot, Night Slash, Snatch | Play Rough 54 | Liepard |
| Liepard | wild | 48 | Rewrite | Skitter Smack, Sucker Punch, Night Slash, Snatch | Throat Chop 49, Shadow Ball 51, Play Rough 54, Psycho Cut 59, U-turn 61 | Liepard |
| Lopunny | wild | 48 | Oxide | Agility, Dizzy Punch, Charm, Bounce | Healing Wish 53 | Lopunny |
| Lopunny | wild | 48 | Rewrite | Dig, Charm, Bounce, Strength | Headbutt 51, Secret Power 54, Thunderous Kick 56, Low Sweep 59, Drain Punch 61 | Lopunny |
| Mightyena | wild | 48 | Oxide | Crunch, Scary Face, Taunt, Embargo | Take Down 52, Thief 57, Sucker Punch 62 | Mightyena |
| Mightyena | wild | 48 | Rewrite | Taunt, Quick Attack, Jaw Lock, Embargo | Take Down 52, Thief 57, Poison Fang 59, Sucker Punch 62 | Mightyena |
| Roserade | wild | 48 | Oxide | Poison Sting, Mega Drain, Magical Leaf, Sweet Scent | nothing | Roserade |
| Roserade | wild | 48 | Rewrite | Poison Sting, Mega Drain, Magical Leaf, Signal Beam | Shadow Ball 54, Dazzling Gleam 57, Leech Seed 59, Swagger 65 | Roserade |
| Sharpedo | super rod | 48 | Oxide | Slash, Aqua Jet, Taunt, Agility | Skull Bash 50, Night Slash 56 | Sharpedo |
| Sharpedo | super rod | 48 | Rewrite | Bulldoze, Taunt, Poison Fang, Agility | Skull Bash 50, Triple Dive 54, Night Slash 56, Fire Fang 58, Poison Jab 60 | Sharpedo |
| Talonflame | wild | 48 | Oxide | Natural Gift, Acrobatics, Me First, Tailwind | Flare Blitz 51, Brave Bird 55 | Talonflame |
| Talonflame | wild | 48 | Rewrite | Acrobatics, Steel Wing, U-turn, Tailwind | Flare Blitz 51, Brave Bird 55, Overheat 57, Agility 59, Bulk Up 64 | Talonflame |
| Arboliva | wild | 49 | Oxide | Seed Bomb, Energy Ball, Leech Seed, Terrain Pulse | Petal Blizzard 52, Petal Dance 58 | Arboliva |
| Arboliva | wild | 49 | Rewrite | Leech Seed, Alluring Voice, Terrain Pulse, Giga Drain | Petal Blizzard 52, Pollen Puff 56, Petal Dance 58, Leaf Storm 64 | Arboliva |
| Emolga | wild | 49 | Oxide | Acrobatics, Encore, Light Screen, Volt Switch | Discharge 50, Agility 50 | Emolga |
| Emolga | wild | 49 | Rewrite | Encore, Light Screen, Volt Switch, Agility | Discharge 50, Energy Ball 52, Thunderbolt 54, Air Slash 59, Shadow Ball 61 | Emolga |
| Tsareena | wild | 49 | Oxide | Low Sweep, Aromatherapy, Leaf Storm, Power Whip | Hi Jump Kick 55 | Tsareena |
| Tsareena | wild | 49 | Rewrite | Trop Kick, Leaf Storm, Zen Headbutt, Petal Blizzard | U-turn 51, Hi Jump Kick 55, Play Rough 59 | Tsareena |
| Vespiquen | wild | 49 | Oxide | Captivate, Attack Order, Swagger, Destiny Bond | nothing | Vespiquen |
| Vespiquen | wild | 49 | Rewrite | Swagger, Dual Wingbeat, U-turn, Pounce | Psychic Noise 51, Secret Power 53, Low Sweep 59 | Vespiquen |
| Cherrim | wild | 50 | Oxide | Worry Seed, Take Down, SolarBeam, Lucky Chant | nothing | Cherrim |
| Cherrim | wild | 50 | Rewrite | Take Down, Rock Slide, SolarBeam, Lucky Chant | Giga Drain 51, Pollen Puff 53, Body Slam 59, Play Rough 61 | Cherrim |
| Jumpluff | wild | 50 | Oxide | U-turn, Worry Seed, Giga Drain, Bounce | Memento 52 | Jumpluff |
| Jumpluff | wild | 50 | Rewrite | Worry Seed, Giga Drain, Bounce, Dazzling Gleam | Lunge 52 | Jumpluff |
| Vikavolt | wild | 50 | Oxide | Bite, Spark, Signal Beam, Discharge | Bug Buzz 55, Thunderbolt 65 | Vikavolt |
| Vikavolt | wild | 50 | Rewrite | Bug Buzz, Air Slash, Discharge, Agility | Energy Ball 56, Iron Defense 57, Thunderbolt 65 | Vikavolt |
| Greninja | super rod | 51 | Oxide | Dark Pulse, Extrasensory, Sludge Wave, Gunk Shot | Hydro Pump 55, Hydro Cannon 65 | Greninja |
| Greninja | super rod | 51 | Rewrite | Extrasensory, Sludge Wave, Water Shuriken, Gunk Shot | Throat Chop 56, Hydro Cannon 65 | Greninja |

## Route 230

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 65 | At the cap |
|---|---|---|---|---|---|---|
| Remoraid | old rod | 22 | Oxide | Lock-On, Psybeam, Aurora Beam, BubbleBeam | Focus Energy 23; as Octillery: Octazooka 25, Bullet Seed 29, Wring Out 36, Signal Beam 42, Ice Beam 48, Hyper Beam 55 | Octillery (from 25) |
| Remoraid | old rod | 22 | Rewrite | Lock-On, Psybeam, Aurora Beam, BubbleBeam | Focus Energy 23; as Octillery: Octazooka 25, Rock Blast 27, Bullet Seed 29, Scald 35, Signal Beam 42, Skitter Smack 44, Ice Beam 48, Hyper Beam 55, Snipe Shot 56 | Octillery (from 25) |
| Tentacool | old rod | 22 | Oxide | Acid, Toxic Spikes, BubbleBeam, Wrap | Barrier 26, Water Pulse 29; as Tentacruel: Poison Jab 36, Screech 42, Hydro Pump 49, Wring Out 55 | Tentacruel (from 30) |
| Tentacool | old rod | 22 | Rewrite | Acid, Toxic Spikes, Icy Wind, BubbleBeam | Barrier 26, Water Pulse 29; as Tentacruel: Psybeam 34, Poison Jab 36, Scald 38, Screech 42, Surf 49, Sludge Wave 52, Sludge Bomb 54, Muddy Water 58, Power Gem 60 | Tentacruel (from 30) |
| Barboach | old rod | 24 | Oxide | Water Gun, Mud Bomb, Amnesia, Water Pulse | Magnitude 26; as Whiscash: Rest 33, Snore 33, Aqua Tail 39, Earthquake 45, Future Sight 51, Fissure 57 | Whiscash (from 30) |
| Barboach | old rod | 24 | Rewrite | Water Gun, Mud Bomb, Amnesia, Water Pulse | Magnitude 26, Bulldoze 27, Tickle 28; as Whiscash: Rest 33, Rock Tomb 35, Aqua Tail 39, Zen Headbutt 42, Earthquake 45, Future Sight 51, Bounce 53 | Whiscash (from 30) |
| Mantyke | old rod | 24 | Oxide | BubbleBeam, Headbutt, Agility, Wing Attack | Water Pulse 28; as Mantine: Take Down 31, Confuse Ray 37, Bounce 40, Aqua Ring 46, Hydro Pump 49 | Mantine (from 30) |
| Mantyke | old rod | 24 | Rewrite | BubbleBeam, Headbutt, Agility, Wing Attack | Water Pulse 28; as Mantine: Take Down 31, Scald 34, Confuse Ray 37, Bounce 40, Signal Beam 42, Aqua Ring 46, Surf 50, Air Slash 52, Psychic 58, Muddy Water 60 | Mantine (from 30) |
| Frogadier | old rod | 26 | Oxide | Icy Wind, Faint Attack, Acrobatics, Low Kick | Waterfall 30, Fling 35; as Greninja: Scald 37, Dark Pulse 40, Extrasensory 43, Sludge Wave 47, Gunk Shot 51, Hydro Pump 55, Hydro Cannon 65 | Greninja (from 36) |
| Frogadier | old rod | 26 | Rewrite | Thief, Faint Attack, Acrobatics, Low Kick | Waterfall 30, Fling 35; as Greninja: Shadow Sneak 36, Scald 37, Dark Pulse 40, Bounce 41, Extrasensory 43, Sludge Wave 47, Water Shuriken 49, Gunk Shot 51, Throat Chop 56, Hydro Cannon 65 | Greninja (from 36) |
| Alomomola | good rod | 35 | Oxide | Protect, Water Pulse, Wake-Up Slap, Soak | Wish 37, Brine 41, Safeguard 45, Whirlpool 49, Helping Hand 53, Healing Wish 57, Wide Guard 61, Hydro Pump 65 | Alomomola |
| Alomomola | good rod | 35 | Rewrite | Heal Pulse, Wake-Up Slap, Soak, Agility | Wish 37, Play Rough 39, Brine 41, Scale Shot 43, Safeguard 45, Whirlpool 49, Helping Hand 53, Bounce 55, Wide Guard 61, Muddy Water 65 | Alomomola |
| Tentacool | good rod | 35 | Oxide | Wrap, Barrier, Water Pulse, Poison Jab | Screech 36; as Tentacruel: Poison Jab 36, Screech 42, Hydro Pump 49, Wring Out 55 | Tentacruel (from 36) |
| Tentacool | good rod | 35 | Rewrite | BubbleBeam, Barrier, Water Pulse, Poison Jab | Screech 36; as Tentacruel: Poison Jab 36, Scald 38, Screech 42, Surf 49, Sludge Wave 52, Sludge Bomb 54, Muddy Water 58, Power Gem 60 | Tentacruel (from 36) |
| Corsola | good rod | 37 | Oxide | BubbleBeam, Lucky Chant, AncientPower, Aqua Ring | Spike Cannon 40, Power Gem 44, Mirror Coat 48, Earth Power 53 | Corsola |
| Corsola | good rod | 37 | Rewrite | Lucky Chant, AncientPower, Aqua Cutter, Aqua Ring | Bulldoze 41, Power Gem 44, Waterfall 46, Mirror Coat 48, Earth Power 53, Throat Chop 55, Liquidation 57, Rock Tomb 59, Confuse Ray 65 | Corsola |
| Gastrodon | good rod | 37 | Oxide | Water Pulse, Mud Bomb, Hidden Power, Body Slam | Muddy Water 41, Recover 54 | Gastrodon |
| Gastrodon | good rod | 37 | Rewrite | Hidden Power, Body Slam, AncientPower, Clear Smog | Muddy Water 41, Earth Power 43, Bulldoze 45, Ice Beam 50, Thousand Waves 52, Recover 54, Skitter Smack 58, Rock Tomb 60 | Gastrodon |
| Wailmer | good rod | 39 | Oxide | Rest, Brine, Water Spout, Amnesia | as Wailord: Dive 46, Bounce 54, Hydro Pump 62 | Wailord (from 40) |
| Wailmer | good rod | 39 | Rewrite | Rest, Brine, Water Spout, Amnesia | as Wailord: Dive 46, Iron Head 48, Bounce 54, Zen Headbutt 56, Surf 62, Ice Beam 64 | Wailord (from 40) |
| Tentacool | surf | 40 | Oxide | Water Pulse, Poison Jab, Screech, Hydro Pump | as Tentacruel: Screech 42, Hydro Pump 49, Wring Out 55 | Tentacruel (from 41) |
| Tentacool | surf | 40 | Rewrite | Water Pulse, Poison Jab, Screech, Surf | as Tentacruel: Screech 42, Surf 49, Sludge Wave 52, Sludge Bomb 54, Muddy Water 58, Power Gem 60 | Tentacruel (from 41) |
| Toxapex | surf | 40 | Oxide | Recover, Spike Cannon, Pin Missile, Toxic | Venom Drench 42, Poison Jab 43, Liquidation 45 | Toxapex |
| Toxapex | surf | 40 | Rewrite | Venoshock, Recover, Pin Missile, Toxic | Venom Drench 42, Poison Jab 43, Liquidation 45, Sludge Bomb 48, Ice Beam 50, Iron Defense 64 | Toxapex |
| Mantyke | surf | 43 | Oxide | Water Pulse, Take Down, Confuse Ray, Bounce | as Mantine: Aqua Ring 46, Hydro Pump 49 | Mantine (from 44) |
| Mantyke | surf | 43 | Rewrite | Water Pulse, Take Down, Confuse Ray, Bounce | as Mantine: Aqua Ring 46, Surf 50, Air Slash 52, Psychic 58, Muddy Water 60 | Mantine (from 44) |
| Pelipper | surf | 43 | Oxide | Stockpile, Swallow, Spit Up, Fling | Tailwind 50, Hydro Pump 57 | Pelipper |
| Pelipper | surf | 43 | Rewrite | Swallow, Stockpile, Spit Up, Fling | Icy Wind 45, Tailwind 50, Fly 52, Muddy Water 57, Hurricane 58, U-turn 59, Acrobatics 61 | Pelipper |
| Lanturn | super rod | 45 | Oxide | Spit Up, BubbleBeam, Signal Beam, Discharge | Aqua Ring 47, Hydro Pump 52, Charge 57 | Lanturn |
| Lanturn | super rod | 45 | Rewrite | BubbleBeam, Signal Beam, Discharge, Thunderbolt | Aqua Ring 47, Muddy Water 52, Charge 57, Flash Cannon 59, Scald 61 | Lanturn |
| Lumineon | super rod | 45 | Oxide | Captivate, Safeguard, Aqua Ring, Whirlpool | U-turn 48, Bounce 53, Silver Wind 59 | Lumineon |
| Lumineon | super rod | 45 | Rewrite | Aqua Ring, Signal Beam, Whirlpool, Fillet Away | U-turn 48, Crunch 50, Bounce 53, Silver Wind 59, Scald 61 | Lumineon |
| Relicanth | surf | 46 | Oxide | Yawn, Take Down, Mud Sport, AncientPower | Double-Edge 50, Dive 57, Rest 64 | Relicanth |
| Relicanth | surf | 46 | Rewrite | Yawn, Take Down, AncientPower, Bulldoze | Double-Edge 50, Scale Shot 54, Dive 57, Aqua Tail 62, Rest 64 | Relicanth |
| Galarian Rapidash | wild | 47 to 50 | Oxide | Psybeam, Stomp, Heal Pulse, Take Down | Dazzling Gleam 49, Psychic 56, Healing Wish 63 | Galarian Rapidash |
| Galarian Rapidash | wild | 47 to 50 | Rewrite | Heal Pulse, Quick Attack, Take Down, Spirit Break | Throat Chop 48, Mystical Fire 50, Psychic 56, Wild Charge 58, Charm 64 | Galarian Rapidash |
| Absol | wild | 48 | Oxide | Double Team, Slash, Future Sight, Sucker Punch | Detect 49, Night Slash 52, Me First 57, Psycho Cut 60, Perish Song 65 | Absol |
| Absol | wild | 48 | Rewrite | Slash, Future Sight, Sucker Punch, X-Scissor | Kowtow Cleave 50, Night Slash 52, Shadow Ball 54, Sacred Sword 56, Psycho Cut 60, Play Rough 62, Perish Song 65 | Absol |
| Altaria | wild | 48 | Oxide | Natural Gift, DragonBreath, Dragon Dance, Refresh | Dragon Pulse 54, Perish Song 62 | Altaria |
| Altaria | wild | 48 | Rewrite | DragonBreath, Bulldoze, Refresh, Dragon Rush | Dragon Pulse 54, Draco Meteor 56, Perish Song 62 | Altaria |
| Liepard | wild | 48 | Oxide | Sucker Punch, Nasty Plot, Night Slash, Snatch | Play Rough 54 | Liepard |
| Liepard | wild | 48 | Rewrite | Skitter Smack, Sucker Punch, Night Slash, Snatch | Throat Chop 49, Shadow Ball 51, Play Rough 54, Psycho Cut 59, U-turn 61 | Liepard |
| Octillery | super rod | 48 | Oxide | Bullet Seed, Wring Out, Signal Beam, Ice Beam | Hyper Beam 55 | Octillery |
| Octillery | super rod | 48 | Rewrite | Scald, Signal Beam, Skitter Smack, Ice Beam | Hyper Beam 55, Snipe Shot 56 | Octillery |
| Raichu | wild | 48 | Oxide | ThunderShock, Tail Whip, Quick Attack, Thunderbolt | nothing | Raichu |
| Raichu | wild | 48 | Rewrite | Tail Whip, Quick Attack, Thunderbolt, Brick Break | Volt Tackle 54, Surf 56, Sweet Kiss 62, Play Rough 64 | Raichu |
| Talonflame | wild | 48 | Oxide | Natural Gift, Acrobatics, Me First, Tailwind | Flare Blitz 51, Brave Bird 55 | Talonflame |
| Talonflame | wild | 48 | Rewrite | Acrobatics, Steel Wing, U-turn, Tailwind | Flare Blitz 51, Brave Bird 55, Overheat 57, Agility 59, Bulk Up 64 | Talonflame |
| Tentacruel | super rod | 48 | Oxide | Barrier, Water Pulse, Poison Jab, Screech | Hydro Pump 49, Wring Out 55 | Tentacruel |
| Tentacruel | super rod | 48 | Rewrite | Psybeam, Poison Jab, Scald, Screech | Surf 49, Sludge Wave 52, Sludge Bomb 54, Muddy Water 58, Power Gem 60 | Tentacruel |
| Toucannon | wild | 48 to 49 | Oxide | Screech, Drill Peck, Bullet Seed, FeatherDance | Hyper Voice 50 | Toucannon |
| Toucannon | wild | 48 to 49 | Rewrite | Drill Peck, Bullet Seed, Throat Chop, FeatherDance | Hyper Voice 50, Bounce 52, Take Down 58, Body Slam 60 | Toucannon |
| Tsareena | wild | 48 to 49 | Oxide | Low Sweep, Aromatherapy, Leaf Storm, Power Whip | Hi Jump Kick 55 | Tsareena |
| Tsareena | wild | 48 to 49 | Rewrite | Trop Kick, Leaf Storm, Zen Headbutt, Petal Blizzard | U-turn 51, Hi Jump Kick 55, Play Rough 59 | Tsareena |
| Arboliva | wild | 49 | Oxide | Seed Bomb, Energy Ball, Leech Seed, Terrain Pulse | Petal Blizzard 52, Petal Dance 58 | Arboliva |
| Arboliva | wild | 49 | Rewrite | Leech Seed, Alluring Voice, Terrain Pulse, Giga Drain | Petal Blizzard 52, Pollen Puff 56, Petal Dance 58, Leaf Storm 64 | Arboliva |
| Lurantis | wild | 49 | Oxide | Sweet Scent, X-Scissor, Synthesis, Leaf Blade | Solar Blade 55 | Lurantis |
| Lurantis | wild | 49 | Rewrite | Leaf Blade, Dual Chop, Night Slash, Low Sweep | Solar Blade 55, Skitter Smack 57, Leech Life 59, Scary Face 64 | Lurantis |
| Floatzel | wild | 50 | Oxide | Crunch, Agility, Whirlpool, Razor Wind | nothing | Floatzel |
| Floatzel | wild | 50 | Rewrite | Rock Tomb, Whirlpool, BubbleBeam, Agility | Triple Dive 54 | Floatzel |
| Gastrodon | wild | 50 | Oxide | Mud Bomb, Hidden Power, Body Slam, Muddy Water | Recover 54 | Gastrodon |
| Gastrodon | wild | 50 | Rewrite | Muddy Water, Earth Power, Bulldoze, Ice Beam | Thousand Waves 52, Recover 54, Skitter Smack 58, Rock Tomb 60 | Gastrodon |
| Crawdaunt | super rod | 51 | Oxide | Swift, Taunt, Night Slash, Crabhammer | Swords Dance 52, Crunch 57, Guillotine 65 | Crawdaunt |
| Crawdaunt | super rod | 51 | Rewrite | Avalanche, Night Slash, Rock Tomb, Crabhammer | Swords Dance 52, Crunch 57, Razor Shell 59, Throat Chop 61 | Crawdaunt |

## Stark Mountain

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 65 | At the cap |
|---|---|---|---|---|---|---|
| Galarian Weezing | wild | 51 to 54 | Oxide | Will-O-Wisp, Sludge Bomb, Pain Split, Strange Steam | Explosion 55 | Galarian Weezing |
| Galarian Weezing | wild | 51 to 54 | Rewrite | Will-O-Wisp, Sludge Bomb, Pain Split, Strange Steam | Thunderbolt 54, Double Hit 56, Heat Wave 62, Overheat 64 | Galarian Weezing |
| Houndoom | wild | 52 | Oxide | Fire Fang, Faint Attack, Embargo, Flamethrower | Crunch 54, Nasty Plot 60 | Houndoom |
| Houndoom | wild | 52 | Rewrite | Mud Shot, Embargo, Flamethrower, Dark Pulse | Crunch 54, Fiery Wrath 56, Shadow Ball 58, Nasty Plot 60, Toxic 62 | Houndoom |
| Magcargo | wild | 52 to 53 | Oxide | Amnesia, Lava Plume, Rock Slide, Body Slam | Flamethrower 61 | Magcargo |
| Magcargo | wild | 52 to 53 | Rewrite | Scorching Sands, Rock Slide, Shell Smash, Body Slam | Power Gem 56, Flamethrower 61, Torch Song 63, Energy Ball 64 | Magcargo |
| Magmortar | wild | 52 to 54 | Oxide | Confuse Ray, Fire Punch, Lava Plume, Flamethrower | Fire Blast 58 | Magmortar |
| Magmortar | wild | 52 to 54 | Rewrite | Scorching Sands, Flamethrower, Psychic, Thunderbolt | Milk Drink 53, Blast Burn 58, Overheat 61 | Magmortar |
| Rhyperior | wild | 52 | Oxide | Horn Drill, Hammer Arm, Stone Edge, Earthquake | Megahorn 57, Rock Wrecker 61 | Rhyperior |
| Rhyperior | wild | 52 | Rewrite | Rock Blast, Take Down, Hammer Arm, Earthquake | Megahorn 57, Rock Wrecker 61 | Rhyperior |
| Salazzle | wild | 52 to 53 | Oxide | Venoshock, Flamethrower, Sludge Bomb, Dragon Pulse | Fire Blast 55 | Salazzle |
| Salazzle | wild | 52 to 53 | Rewrite | Sludge Bomb, Encore, Dragon Pulse, Nasty Plot | nothing | Salazzle |
| Turtonator | wild | 52 | Oxide | Body Slam, Flamethrower, Dragon Pulse, Fire Spin | Explosion 55, Overheat 61 | Turtonator |
| Turtonator | wild | 52 | Rewrite | Dragon Pulse, Shell Smash, Fire Spin, Heat Crash | Scale Shot 54, Overheat 61, Body Press 63 | Turtonator |
| Weezing | wild | 52 | Oxide | Haze, Double Hit, Explosion, Sludge Bomb | Destiny Bond 55, Memento 63 | Weezing |
| Weezing | wild | 52 | Rewrite | Sludge Wave, Psybeam, Sludge Bomb, Heat Wave | Shadow Ball 56, Poison Fang 58, Thunderbolt 64 | Weezing |
| Ceruledge | wild | 53 | Oxide | Lava Plume, Swords Dance, Ally Switch, Bitter Blade | Psycho Cut 56, Flare Blitz 62 | Ceruledge |
| Ceruledge | wild | 53 | Rewrite | Swords Dance, Night Slash, Bitter Blade, Iron Head | Psycho Cut 56, Flare Blitz 62 | Ceruledge |
| Larvesta | wild | 54 | Oxide | Struggle Bug, Flame Wheel, Bug Bite, Take Down | as Volcarona: Flamethrower 60, Bug Buzz 61, Whirlwind 64, Overheat 65 | Volcarona (from 59) |
| Larvesta | wild | 54 | Rewrite | Fire Spin, Screech, Poison Jab, Take Down | as Volcarona: Mystical Fire 59, Flamethrower 60, Bug Buzz 61, Rage Powder 62, Fiery Dance 63, Overheat 65 | Volcarona (from 59) |

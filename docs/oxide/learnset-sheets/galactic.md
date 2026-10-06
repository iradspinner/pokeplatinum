# Galactic's split: what each catch knows and learns

Written by `tools/oxide/balance/learncheck.py sheets` for check 6 of the learnset baseline (`docs/oxide/learnset-checks.md`). One table per capture area first offered in Galactic's split, whose cap is 65. Each Pokemon is read at the lowest level it is found at there. "Knows at capture" is the last four moves its list gives by that level; "learns by level-up" is every entry it reaches after capture up to 65, evolving on time, with each later stage's moves under its name; "at the cap" is the stage it can be by then and the next one after. A row marked Rewrite shows the learnset rewrite's lists (the tree's) where it differs from the row marked Oxide, Oxide's lists before the learnset rewrite (`da6b92496c`); a row marked both is the same in each. Relearner-only moves and egg moves are left out.

## Distortion World

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 65 | At the cap |
|---|---|---|---|---|---|---|
| Giratina | static battle | 47 | Oxide | Ominous Wind, AncientPower, Dragon Claw, Shadow Force | Heal Block 50, Earth Power 60 | Giratina |
| Giratina | static battle | 47 | Rewrite | Ominous Wind, AncientPower, Dragon Claw, Shadow Force | Heal Block 50, Earth Power 60, Scary Face 65 | Giratina |

## Mt. Coronet Mountainside

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 65 | At the cap |
|---|---|---|---|---|---|---|
| Snover | wild | 36 | Oxide | Mist, Ice Shard, Ingrain, Wood Hammer | as Abomasnow: Blizzard 47, Sheer Cold 58 | Abomasnow (from 40) |
| Snover | wild | 36 | Rewrite | Seed Bomb, Rock Tomb, Body Press, Wood Hammer | as Abomasnow: Ice Beam 41, Giga Drain 50, Ice Punch 53, Rock Climb 54, Shadow Ball 56, Earthquake 58, Leaf Storm 60, Double-Edge 62, Hammer Arm 65 | Abomasnow (from 40) |
| Dewgong | wild | 37 | Oxide | Aqua Jet, Brine, Sheer Cold, Take Down | Dive 41, Aqua Tail 43, Ice Beam 47, Safeguard 51 | Dewgong |
| Dewgong | wild | 37 | Rewrite | Aqua Jet, Brine, Signal Beam, Take Down | Drill Run 40, Dive 41, Aqua Tail 43, Ice Beam 47, Safeguard 51, Muddy Water 54, Bite 56, Flip Turn 58, Play Rough 60, Ice Punch 62, Knock Off 65 | Dewgong |
| Frosmoth | wild | 37 | Oxide | FeatherDance, Aurora Beam, Bug Buzz, Aurora Veil | Blizzard 40, Tailwind 44, Wide Guard 48, Quiver Dance 52 | Frosmoth |
| Frosmoth | wild | 37 | Rewrite | Bug Buzz, Defog, Aurora Beam, Aurora Veil | Ice Beam 40, Tailwind 44, Wide Guard 48, Quiver Dance 52, Air Slash 54, Giga Drain 56, Dazzling Gleam 60, Calm Mind 65 | Frosmoth |
| Hawlucha | wild | 37 | Oxide | Submission, Tailwind, Dual Wingbeat, Fly | Hi Jump Kick 42, Me First 48, Acrobatics 55, Close Combat 60 | Hawlucha |
| Hawlucha | wild | 37 | Rewrite | Flying Press, Tailwind, Dual Wingbeat, Fly | Hi Jump Kick 42, Air Slash 45, Lunge 48, Throat Chop 54, Acrobatics 55, Low Sweep 57, Close Combat 60, Fire Punch 62, Brave Bird 65 | Hawlucha |
| Mienshao | wild | 37 | Oxide | Force Palm, Bounce, Drain Punch, Vacuum Wave | Aura Sphere 38, Me First 40, Jump Kick 45, Dual Chop 48, Focus Blast 51, Acrobatics 55, Hi Jump Kick 64 | Mienshao |
| Mienshao | wild | 37 | Rewrite | Force Palm, Bounce, Drain Punch, Vacuum Wave | Aura Sphere 38, U-turn 41, Rock Tomb 43, Jump Kick 45, Dual Chop 48, Poison Jab 51, Upper Hand 54, Acrobatics 55, Hammer Arm 56, Hi Jump Kick 64 | Mienshao |
| Sneasel | wild | 37 to 38 | Oxide | Fury Swipes, Agility, Icy Wind, Slash | as Weavile: Fling 38, Metal Claw 42, Dark Pulse 49 | Weavile (from 37) |
| Sneasel | wild | 37 to 38 | Rewrite | Nasty Plot, Agility, Icy Wind, Slash | as Weavile: Night Slash 37, Fling 38, Metal Claw 42, Dark Pulse 49, X-Scissor 61 | Weavile (from 37) |
| Snorunt | wild | 37 to 39 | Oxide | Protect, Ice Fang, Crunch, Ice Shard | as Glalie: Blizzard 51, Sheer Cold 59 | Glalie (from 42) |
| Snorunt | wild | 37 to 39 | Oxide | Protect, Ice Fang, Crunch, Ice Shard | as Froslass: Ice Shard 37, Blizzard 51, Destiny Bond 59 | Froslass (from 37) |
| Snorunt | wild | 37 to 39 | Rewrite | Ice Fang, Crunch, Draining Kiss, Ice Shard | as Glalie: Rock Slide 42, Power Gem 44, Confuse Ray 48, Earth Power 53, Ice Punch 54, Shadow Ball 56, Icicle Crash 58, Sweet Kiss 60, Dark Pulse 62, Will-O-Wisp 65 | Glalie (from 42) |
| Snorunt | wild | 37 to 39 | Rewrite | Ice Fang, Crunch, Draining Kiss, Ice Shard | as Froslass: Ice Shard 37, Ice Beam 51, Aura Sphere 61, Dark Pulse 65 | Froslass (from 37) |
| Alolan Ninetales | wild | 38 | Oxide | Tail Whip, Disable, Ice Shard, Safeguard | nothing | Alolan Ninetales |
| Alolan Ninetales | wild | 38 | Rewrite | Spite, Payback, Icy Wind, Chilling Water | Dazzling Gleam 39, Extrasensory 43, Ice Beam 44, Dark Pulse 48, Mystical Fire 53, BurningJealousy 54, Moonblast 56, Will-O-Wisp 58, Confuse Ray 60, Nasty Plot 62, Charm 65 | Alolan Ninetales |
| Delibird | wild | 38 | Oxide | Present | nothing | Delibird |
| Delibird | wild | 38 | Rewrite | Present, Swagger | Ice Beam 54, Drill Run 55, Drill Peck 56, Ice Punch 58, Brave Bird 60, Seed Bomb 62, Foul Play 65 | Delibird |
| Garganacl | wild | 38 | Oxide | Headbutt, Salt Cure, Recover, Rock Slide | Stealth Rock 40, Heavy Slam 44, Earthquake 49, Stone Edge 54, Explosion 60 | Garganacl |
| Garganacl | wild | 38 | Rewrite | Headbutt, Recover, Rock Slide, Rock Tomb | Salt Cure 39, Stealth Rock 40, Iron Head 42, Heavy Slam 44, Earthquake 49, Zen Headbutt 53, Block 54, Body Press 56, Hammer Arm 60, Curse 65 | Garganacl |
| Donphan | wild | 39 | Oxide | Slam, Fury Attack, Assurance, Scary Face | Earthquake 46, Giga Impact 54 | Donphan |
| Donphan | wild | 39 | Rewrite | Rock Tomb, Assurance, Trailblaze, Scary Face | Iron Head 42, Throat Chop 44, Earthquake 46, Seed Bomb 50, Giga Impact 54, Charm 56, Block 61 | Donphan |
| Gliscor | wild | 39 | Oxide | Screech, Night Slash, Swords Dance, U-turn | X-Scissor 42, Guillotine 45 | Gliscor |
| Gliscor | wild | 39 | Rewrite | Screech, Night Slash, Swords Dance, U-turn | X-Scissor 42, Earthquake 57, Bulldoze 60, Lunge 62, Poison Jab 65 | Gliscor |

## Mt. Coronet Peak

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 65 | At the cap |
|---|---|---|---|---|---|---|
| Bronzong | wild | 36 to 39 | Oxide | Extrasensory, Iron Defense, Safeguard, Block | Gyro Ball 38, Future Sight 43, Faint Attack 50, Payback 61 | Bronzong |
| Bronzong | wild | 36 to 39 | Rewrite | Iron Defense, Safeguard, Block, Iron Head | Gyro Ball 38, Rock Tomb 40, Future Sight 43, Body Press 46, Faint Attack 50, Shadow Ball 54, Earthquake 57, Payback 61 | Bronzong |
| Golbat | wild | 37 | Oxide | Wing Attack, Confuse Ray, Air Cutter, Mean Look | Poison Fang 39; as Crobat: Haze 45, Air Slash 51 | Crobat (from 40) |
| Golbat | wild | 37 | Rewrite | Air Cutter, Poison Jab, Mean Look, Steel Wing | Poison Fang 39; as Crobat: Zen Headbutt 45, Air Slash 51, U-turn 54, Crunch 56, Tailwind 58, Toxic 60, Brave Bird 65 | Crobat (from 40) |
| Graveler | wild | 37 | Oxide | Selfdestruct, Rollout, Rock Blast, Earthquake | Explosion 38; as Golem: Double-Edge 44, Stone Edge 49 | Golem (from 40) |
| Graveler | wild | 37 | Rewrite | Rock Blast, Rock Tomb, Earthquake, Sucker Punch | Iron Head 39; as Golem: Double-Edge 44, Rock Slide 49, Body Press 53, Body Slam 56, Fire Punch 61, Hammer Arm 65 | Golem (from 40) |
| Hariyama | wild | 37 | Oxide | SmellingSalt, Belly Drum, Force Palm, Seismic Toss | Wake-Up Slap 42, Endure 47, Close Combat 52, Reversal 57 | Hariyama |
| Hariyama | wild | 37 | Rewrite | Low Sweep, Force Palm, Bulldoze, Seismic Toss | Rock Tomb 39, Wake-Up Slap 42, Drain Punch 44, Endure 47, Close Combat 52, Upper Hand 54, Throat Chop 55, Reversal 57, Iron Head 60, Earthquake 65 | Hariyama |
| Machoke | wild | 37 | Oxide | Revenge, Vital Throw, Submission, Wake-Up Slap | Cross Chop 40; as Machamp: Cross Chop 40, Scary Face 44, DynamicPunch 51 | Machamp (from 40) |
| Machoke | wild | 37 | Rewrite | Vital Throw, Bulldoze, Throat Chop, Wake-Up Slap | Close Combat 40; as Machamp: Close Combat 40, Scary Face 44, Low Sweep 48, Rock Slide 53, Rock Tomb 54, Meteor Mash 56, Bulk Up 60, Earthquake 65 | Machamp (from 40) |
| Mienshao | wild | 37 | Oxide | Force Palm, Bounce, Drain Punch, Vacuum Wave | Aura Sphere 38, Me First 40, Jump Kick 45, Dual Chop 48, Focus Blast 51, Acrobatics 55, Hi Jump Kick 64 | Mienshao |
| Mienshao | wild | 37 | Rewrite | Force Palm, Bounce, Drain Punch, Vacuum Wave | Aura Sphere 38, U-turn 41, Rock Tomb 43, Jump Kick 45, Dual Chop 48, Poison Jab 51, Upper Hand 54, Acrobatics 55, Hammer Arm 56, Hi Jump Kick 64 | Mienshao |
| Naclstack | wild | 37 to 38 | Oxide | Headbutt, Iron Defense, Recover, Rock Slide | Stealth Rock 38; as Garganacl: Stealth Rock 40, Heavy Slam 44, Earthquake 49, Stone Edge 54, Explosion 60 | Garganacl (from 38) |
| Naclstack | wild | 37 to 38 | Rewrite | Recover, Rock Polish, Rock Tomb, Rock Slide | Stealth Rock 38; as Garganacl: Rock Tomb 38, Salt Cure 39, Stealth Rock 40, Iron Head 42, Heavy Slam 44, Earthquake 49, Zen Headbutt 53, Block 54, Body Press 56, Hammer Arm 60, Curse 65 | Garganacl (from 38) |
| Carbink | wild | 38 | Oxide | AncientPower, Rock Polish, Rock Slide, Stealth Rock | Skill Swap 40, Light Screen 44, Power Gem 45, Moonblast 52, Stone Edge 54 | Carbink |
| Carbink | wild | 38 | Rewrite | Dazzling Gleam, Rock Tomb, Rock Slide, Stealth Rock | Skill Swap 40, Light Screen 44, Power Gem 45, Moonblast 52, Iron Head 54, Psychic 56, Body Press 60 | Carbink |
| Glimmora | wild | 38 | Oxide | Stealth Rock, Venoshock, Selfdestruct, Rock Slide | Power Gem 39, Acid Armor 44, Sludge Wave 50 | Glimmora |
| Glimmora | wild | 38 | Rewrite | Rock Polish, Stealth Rock, Venoshock, Rock Slide | Power Gem 39, Sludge Bomb 41, Acid Armor 44, Flash Cannon 47, Sludge Wave 50, Energy Ball 54, Dazzling Gleam 56, Earth Power 60, Confuse Ray 65 | Glimmora |
| Gliscor | wild | 39 | Oxide | Screech, Night Slash, Swords Dance, U-turn | X-Scissor 42, Guillotine 45 | Gliscor |
| Gliscor | wild | 39 | Rewrite | Screech, Night Slash, Swords Dance, U-turn | X-Scissor 42, Earthquake 57, Bulldoze 60, Lunge 62, Poison Jab 65 | Gliscor |
| Klefki | wild | 39 | Oxide | Imprison, Mirror Shot, Flash Cannon, Foul Play | Play Rough 41, Magic Room 44, Heal Block 50, Last Resort 52 | Klefki |
| Klefki | wild | 39 | Rewrite | Mirror Shot, Iron Defense, Flash Cannon, Foul Play | Play Rough 41, Magic Room 44, Calm Mind 47, Heal Block 50, Last Resort 52, Skitter Smack 54, Psychic 56, Moonblast 58, Facade 60, Thunder Wave 65 | Klefki |

## Resort Area

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 65 | At the cap |
|---|---|---|---|---|---|---|
| Luvdisc | old rod | 22 | Oxide | Agility, Take Down, Lucky Chant, Attract | Sweet Kiss 27; as Alomomola: Soak 33, Wish 37, Brine 41, Safeguard 45, Whirlpool 49, Helping Hand 53, Healing Wish 57, Wide Guard 61, Hydro Pump 65 | Alomomola (from 30) |
| Luvdisc | old rod | 22 | Rewrite | Lucky Chant, Agility, Icy Wind, Attract | Sweet Kiss 27; as Alomomola: Heal Pulse 30, Wake-Up Slap 31, Water Pulse 32, Soak 33, Play Rough 35, Wish 37, Brine 41, Zen Headbutt 43, Safeguard 45, Whirlpool 49, Helping Hand 53, Flip Turn 54, Liquidation 56, Ice Punch 57, Body Slam 58, Wide Guard 61, Muddy Water 65 | Alomomola (from 30) |
| Tentacool | old rod | 22 | Oxide | Acid, Toxic Spikes, BubbleBeam, Wrap | Barrier 26, Water Pulse 29; as Tentacruel: Poison Jab 36, Screech 42, Hydro Pump 49, Wring Out 55 | Tentacruel (from 30) |
| Tentacool | old rod | 22 | Rewrite | Acid, Toxic Spikes, Water Pulse, BubbleBeam | Barrier 26; as Tentacruel: Poison Jab 33, Aurora Beam 34, Sludge Bomb 39, Screech 42, Psybeam 44, Surf 49, Muddy Water 53, Throat Chop 54, Power Gem 56, Flip Turn 58, Ice Beam 60, Toxic 62, Skitter Smack 65 | Tentacruel (from 30) |
| Mantyke | old rod | 24 to 26 | Oxide | BubbleBeam, Headbutt, Agility, Wing Attack | Water Pulse 28; as Mantine: Take Down 31, Confuse Ray 37, Bounce 40, Aqua Ring 46, Hydro Pump 49 | Mantine (from 30) |
| Mantyke | old rod | 24 to 26 | Rewrite | BubbleBeam, Headbutt, Agility, Wing Attack | Icy Wind 25, Water Pulse 28; as Mantine: Take Down 31, Signal Beam 34, Round 35, Confuse Ray 37, Bounce 40, Psybeam 41, Surf 43, Aqua Ring 46, Scald 49, Air Slash 54, Roost 56, Muddy Water 58, Ice Beam 60, Swagger 65 | Mantine (from 30) |
| Remoraid | old rod | 24 | Oxide | Psybeam, Aurora Beam, BubbleBeam, Focus Energy | as Octillery: Octazooka 25, Bullet Seed 29, Wring Out 36, Signal Beam 42, Ice Beam 48, Hyper Beam 55 | Octillery (from 25) |
| Remoraid | old rod | 24 | Rewrite | Screech, Aurora Beam, BubbleBeam, Focus Energy | as Octillery: Octazooka 25, Mud Shot 27, Bullet Seed 29, Round 33, Charge Beam 35, Scald 37, Skitter Smack 40, Signal Beam 42, Ice Beam 48, Psychic 54, Hyper Beam 55, Swagger 61 | Octillery (from 25) |
| Luvdisc | good rod | 35 | Oxide | Lucky Chant, Attract, Sweet Kiss, Water Pulse | as Alomomola: Wish 37, Brine 41, Safeguard 45, Whirlpool 49, Helping Hand 53, Healing Wish 57, Wide Guard 61, Hydro Pump 65 | Alomomola (from 36) |
| Luvdisc | good rod | 35 | Rewrite | Agility, Icy Wind, Attract, Sweet Kiss | as Alomomola: Wish 37, Brine 41, Zen Headbutt 43, Safeguard 45, Whirlpool 49, Helping Hand 53, Flip Turn 54, Liquidation 56, Ice Punch 57, Body Slam 58, Wide Guard 61, Muddy Water 65 | Alomomola (from 36) |
| Mareanie | good rod | 35 | Oxide | Toxic Spikes, Recover, Spike Cannon, Pin Missile | Toxic 36; as Toxapex: Toxic 39, Venom Drench 42, Poison Jab 43, Liquidation 45 | Toxapex (from 38) |
| Mareanie | good rod | 35 | Rewrite | Toxic Spikes, Recover, Spike Cannon, Pin Missile | Toxic 36, Muddy Water 38; as Toxapex: Venom Drench 42, Poison Jab 43, Liquidation 45, Lunge 53, Ice Beam 54, Sludge Bomb 56, Iron Defense 61 | Toxapex (from 38) |
| Mantyke | good rod | 37 | Oxide | Wing Attack, Water Pulse, Take Down, Confuse Ray | as Mantine: Bounce 40, Aqua Ring 46, Hydro Pump 49 | Mantine (from 38) |
| Mantyke | good rod | 37 | Rewrite | Icy Wind, Water Pulse, Take Down, Confuse Ray | as Mantine: Bounce 40, Psybeam 41, Surf 43, Aqua Ring 46, Scald 49, Air Slash 54, Roost 56, Muddy Water 58, Ice Beam 60, Swagger 65 | Mantine (from 38) |
| Shellos | good rod | 37 | Oxide | Mud Bomb, Hidden Power, Body Slam, Muddy Water | as Gastrodon: Muddy Water 41, Recover 54 | Gastrodon (from 38) |
| Shellos | good rod | 37 | Rewrite | Hidden Power, Swagger, Body Slam, Muddy Water | as Gastrodon: Muddy Water 41, Bulldoze 44, Sludge Bomb 46, Ice Beam 49, Recover 54, Skitter Smack 56, Rock Tomb 60, Block 65 | Gastrodon (from 38) |
| Greninja | good rod | 39 | Oxide | Low Kick, Waterfall, Fling, Scald | Dark Pulse 40, Extrasensory 43, Sludge Wave 47, Gunk Shot 51, Hydro Pump 55, Hydro Cannon 65 | Greninja |
| Greninja | good rod | 39 | Rewrite | Waterfall, Fling, Shadow Sneak, Scald | Dark Pulse 40, Extrasensory 43, Sludge Wave 47, Gunk Shot 51, Ice Beam 54, Surf 56, Throat Chop 58, Muddy Water 60, Taunt 62, Hydro Cannon 65 | Greninja |
| Gastrodon | surf | 40 | Oxide | Water Pulse, Mud Bomb, Hidden Power, Body Slam | Muddy Water 41, Recover 54 | Gastrodon |
| Gastrodon | surf | 40 | Rewrite | Body Slam, AncientPower, Earth Power, Clear Smog | Muddy Water 41, Bulldoze 44, Sludge Bomb 46, Ice Beam 49, Recover 54, Skitter Smack 56, Rock Tomb 60, Block 65 | Gastrodon |
| Tentacool | surf | 40 | Oxide | Water Pulse, Poison Jab, Screech, Hydro Pump | as Tentacruel: Screech 42, Hydro Pump 49, Wring Out 55 | Tentacruel (from 41) |
| Tentacool | surf | 40 | Rewrite | Barrier, Poison Jab, Screech, Surf | as Tentacruel: Screech 42, Psybeam 44, Surf 49, Muddy Water 53, Throat Chop 54, Power Gem 56, Flip Turn 58, Ice Beam 60, Toxic 62, Skitter Smack 65 | Tentacruel (from 41) |
| Mantyke | surf | 43 | Oxide | Water Pulse, Take Down, Confuse Ray, Bounce | as Mantine: Aqua Ring 46, Hydro Pump 49 | Mantine (from 44) |
| Mantyke | surf | 43 | Rewrite | Water Pulse, Take Down, Confuse Ray, Bounce | as Mantine: Aqua Ring 46, Scald 49, Air Slash 54, Roost 56, Muddy Water 58, Ice Beam 60, Swagger 65 | Mantine (from 44) |
| Shellos | surf | 43 | Oxide | Mud Bomb, Hidden Power, Body Slam, Muddy Water | as Gastrodon: Recover 54 | Gastrodon (from 44) |
| Shellos | surf | 43 | Rewrite | Hidden Power, Swagger, Body Slam, Muddy Water | as Gastrodon: Bulldoze 44, Sludge Bomb 46, Ice Beam 49, Recover 54, Skitter Smack 56, Rock Tomb 60, Block 65 | Gastrodon (from 44) |
| Jellicent | super rod | 45 | Oxide | Hex, Brine, Pain Split, Destiny Bond | Shadow Ball 51, Scald 55, Water Spout 65 | Jellicent |
| Jellicent | super rod | 45 | Rewrite | Hex, Brine, Pain Split, Muddy Water | Shadow Ball 51, Sludge Bomb 54, Scald 55, Ice Beam 57, Energy Ball 60, Will-O-Wisp 62, Water Spout 65 | Jellicent |
| Lanturn | super rod | 45 | Oxide | Spit Up, BubbleBeam, Signal Beam, Discharge | Aqua Ring 47, Hydro Pump 52, Charge 57 | Lanturn |
| Lanturn | super rod | 45 | Rewrite | Surf, Thunderbolt, Discharge, Flash Cannon | Aqua Ring 47, Muddy Water 52, Volt Switch 54, Dazzling Gleam 55, Charge 57, Ice Beam 60, Swagger 65 | Lanturn |
| Greninja | surf | 46 | Oxide | Fling, Scald, Dark Pulse, Extrasensory | Sludge Wave 47, Gunk Shot 51, Hydro Pump 55, Hydro Cannon 65 | Greninja |
| Greninja | surf | 46 | Rewrite | Shadow Sneak, Scald, Dark Pulse, Extrasensory | Sludge Wave 47, Gunk Shot 51, Ice Beam 54, Surf 56, Throat Chop 58, Muddy Water 60, Taunt 62, Hydro Cannon 65 | Greninja |
| Gorebyss | super rod | 48 | Oxide | Baton Pass, Dive, Psychic, Aqua Tail | Hydro Pump 51 | Gorebyss |
| Gorebyss | super rod | 48 | Rewrite | Dive, Surf, Psychic, Aqua Tail | Muddy Water 51, Shadow Ball 54, Ice Beam 56, Shell Smash 58, Scald 60, Scary Face 62, Confuse Ray 65 | Gorebyss |
| Lumineon | super rod | 48 | Oxide | Safeguard, Aqua Ring, Whirlpool, U-turn | Bounce 53, Silver Wind 59 | Lumineon |
| Lumineon | super rod | 48 | Rewrite | Signal Beam, Whirlpool, Ice Fang, U-turn | Bounce 53, Air Slash 54, Crunch 56, Confuse Ray 57, Silver Wind 59, Charm 65 | Lumineon |
| Kingdra | super rod | 51 | Oxide | Twister, Brine, Hydro Pump, Dragon Dance | Dragon Pulse 57 | Kingdra |
| Kingdra | super rod | 51 | Rewrite | Twister, Brine, Octazooka, Aurora Beam | Scald 54, Dragon Pulse 57, Wave Crash 60, Dragon Dance 62, Iron Head 65 | Kingdra |

## Route 225

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 65 | At the cap |
|---|---|---|---|---|---|---|
| Chinchou | old rod | 22 | Oxide | Flail, Water Gun, Confuse Ray, Spark | Take Down 23; as Lanturn: Stockpile 27, Swallow 27, Spit Up 27, BubbleBeam 30, Signal Beam 35, Discharge 40, Aqua Ring 47, Hydro Pump 52, Charge 57 | Lanturn (from 27) |
| Chinchou | old rod | 22 | Rewrite | Water Gun, Screech, Confuse Ray, Spark | Take Down 23, Icy Wind 26; as Lanturn: Stockpile 27, Swallow 28, Spit Up 29, BubbleBeam 30, Signal Beam 31, Scald 33, Surf 34, Thunderbolt 37, Discharge 40, Flash Cannon 43, Aqua Ring 47, Muddy Water 52, Volt Switch 54, Dazzling Gleam 55, Charge 57, Ice Beam 60, Swagger 65 | Lanturn (from 27) |
| Goldeen | old rod | 22 | Oxide | Supersonic, Horn Attack, Water Pulse, Flail | Aqua Ring 27, Fury Attack 31; as Seaking: Waterfall 40, Horn Drill 47, Agility 56, Megahorn 63 | Seaking (from 33) |
| Goldeen | old rod | 22 | Rewrite | Water Pulse, Horn Attack, Swagger, Flail | Aqua Ring 27; as Seaking: Aqua Jet 34, Skull Bash 37, Waterfall 40, Poison Jab 44, Drill Run 47, Knock Off 50, Aqua Tail 54, Agility 56, Drill Peck 57, Throat Chop 59, Megahorn 63 | Seaking (from 33) |
| Buizel | old rod | 24 | Oxide | Water Gun, Pursuit, Swift, Aqua Jet | as Floatzel: Crunch 26, Agility 29, Whirlpool 39, Razor Wind 50 | Floatzel (from 26) |
| Buizel | old rod | 24 | Rewrite | Pursuit, Scary Face, Swift, Aqua Jet | as Floatzel: Crunch 26, Icy Wind 29, Flip Turn 33, Waterfall 36, Whirlpool 39, Liquidation 41, Low Sweep 44, Agility 51, Rock Tomb 53, Ice Fang 56, Wave Crash 62, Ice Punch 65 | Floatzel (from 26) |
| Carvanha | old rod | 24 | Oxide | Scary Face, Ice Fang, Screech, Swagger | Assurance 26, Crunch 28; as Sharpedo: Slash 30, Aqua Jet 34, Taunt 40, Agility 45, Skull Bash 50, Night Slash 56 | Sharpedo (from 30) |
| Carvanha | old rod | 24 | Rewrite | Ice Fang, Screech, Swagger, Aqua Cutter | Assurance 26, Crunch 28; as Sharpedo: Slash 30, Aqua Jet 31, Bug Bite 35, Aerial Ace 37, Taunt 40, Liquidation 41, Agility 45, Skull Bash 50, Poison Fang 54, Night Slash 56, Poison Jab 58, Flip Turn 60, Throat Chop 65 | Sharpedo (from 30) |
| Tentacool | old rod | 26 | Oxide | Toxic Spikes, BubbleBeam, Wrap, Barrier | Water Pulse 29; as Tentacruel: Poison Jab 36, Screech 42, Hydro Pump 49, Wring Out 55 | Tentacruel (from 30) |
| Tentacool | old rod | 26 | Rewrite | Toxic Spikes, Water Pulse, BubbleBeam, Barrier | as Tentacruel: Poison Jab 33, Aurora Beam 34, Sludge Bomb 39, Screech 42, Psybeam 44, Surf 49, Muddy Water 53, Throat Chop 54, Power Gem 56, Flip Turn 58, Ice Beam 60, Toxic 62, Skitter Smack 65 | Tentacruel (from 30) |
| Ludicolo | good rod | 35 | Oxide | Astonish, Growl, Mega Drain, Nature Power | nothing | Ludicolo |
| Ludicolo | good rod | 35 | Rewrite | Growl, Mega Drain, Nature Power, Energy Ball | Ice Beam 54, Muddy Water 56, Hyper Voice 58, Leaf Storm 60, Psychic 62, Synthesis 65 | Ludicolo |
| Wooper | good rod | 35 | Oxide | Mud Bomb, Amnesia, Yawn, Earthquake | as Quagsire: Earthquake 36, Mist 48, Haze 48, Muddy Water 53 | Quagsire (from 36) |
| Wooper | good rod | 35 | Oxide | Mud Bomb, Amnesia, Yawn, Earthquake | as Clodsire: Megahorn 36, Toxic 40, Earthquake 48, Recover 55 | Clodsire (from 35) |
| Wooper | good rod | 35 | Rewrite | Mud Shot, Slam, Mud Bomb, Earthquake | as Quagsire: Earthquake 36, Rock Slide 39, Toxic 40, Drain Punch 44, Mist 48, Muddy Water 53, Poison Jab 54, Aqua Tail 56, Recover 58, Rock Tomb 60, Toxic Spikes 62, Swagger 65 | Quagsire (from 36) |
| Wooper | good rod | 35 | Rewrite | Mud Shot, Slam, Mud Bomb, Earthquake | as Clodsire: Megahorn 36, Toxic 40, Drain Punch 44, Earthquake 48, Aqua Tail 51, Toxic Spikes 54, Recover 55, Swagger 61 | Clodsire (from 35) |
| Shellos | good rod | 37 | Oxide | Mud Bomb, Hidden Power, Body Slam, Muddy Water | as Gastrodon: Muddy Water 41, Recover 54 | Gastrodon (from 38) |
| Shellos | good rod | 37 | Rewrite | Hidden Power, Swagger, Body Slam, Muddy Water | as Gastrodon: Muddy Water 41, Bulldoze 44, Sludge Bomb 46, Ice Beam 49, Recover 54, Skitter Smack 56, Rock Tomb 60, Block 65 | Gastrodon (from 38) |
| Surskit | good rod | 37 | Oxide | BubbleBeam, Agility, Mist, Haze | as Masquerain: Silver Wind 40, Air Slash 47, Whirlwind 54, Bug Buzz 61 | Masquerain (from 38) |
| Surskit | good rod | 37 | Rewrite | Water Sport, BubbleBeam, Agility, Mist | as Masquerain: Giga Drain 38, Silver Wind 40, Signal Beam 41, Icy Wind 43, Air Slash 47, Lunge 53, Skitter Smack 54, Ice Beam 56, U-turn 57, Leech Life 58, Bug Buzz 61, Energy Ball 65 | Masquerain (from 38) |
| Sharpedo | good rod | 39 | Oxide | Assurance, Crunch, Slash, Aqua Jet | Taunt 40, Agility 45, Skull Bash 50, Night Slash 56 | Sharpedo |
| Sharpedo | good rod | 39 | Rewrite | Slash, Aqua Jet, Bug Bite, Aerial Ace | Taunt 40, Liquidation 41, Agility 45, Skull Bash 50, Poison Fang 54, Night Slash 56, Poison Jab 58, Flip Turn 60, Throat Chop 65 | Sharpedo |
| Gastrodon | surf | 40 | Oxide | Water Pulse, Mud Bomb, Hidden Power, Body Slam | Muddy Water 41, Recover 54 | Gastrodon |
| Gastrodon | surf | 40 | Rewrite | Body Slam, AncientPower, Earth Power, Clear Smog | Muddy Water 41, Bulldoze 44, Sludge Bomb 46, Ice Beam 49, Recover 54, Skitter Smack 56, Rock Tomb 60, Block 65 | Gastrodon |
| Masquerain | surf | 40 | Oxide | Gust, Scary Face, Stun Spore, Silver Wind | Air Slash 47, Whirlwind 54, Bug Buzz 61 | Masquerain |
| Masquerain | surf | 40 | Rewrite | Stun Spore, Surf, Giga Drain, Silver Wind | Signal Beam 41, Icy Wind 43, Air Slash 47, Lunge 53, Skitter Smack 54, Ice Beam 56, U-turn 57, Leech Life 58, Bug Buzz 61, Energy Ball 65 | Masquerain |
| Buizel | surf | 43 | Oxide | Swift, Aqua Jet, Agility, Whirlpool | as Floatzel: Razor Wind 50 | Floatzel (from 44) |
| Buizel | surf | 43 | Rewrite | Pursuit, Scary Face, Swift, Aqua Jet | as Floatzel: Low Sweep 44, Agility 51, Rock Tomb 53, Ice Fang 56, Wave Crash 62, Ice Punch 65 | Floatzel (from 44) |
| Shellos | surf | 43 | Oxide | Mud Bomb, Hidden Power, Body Slam, Muddy Water | as Gastrodon: Recover 54 | Gastrodon (from 44) |
| Shellos | surf | 43 | Rewrite | Hidden Power, Swagger, Body Slam, Muddy Water | as Gastrodon: Bulldoze 44, Sludge Bomb 46, Ice Beam 49, Recover 54, Skitter Smack 56, Rock Tomb 60, Block 65 | Gastrodon (from 44) |
| Ludicolo | super rod | 45 | Oxide | Astonish, Growl, Mega Drain, Nature Power | nothing | Ludicolo |
| Ludicolo | super rod | 45 | Rewrite | Growl, Mega Drain, Nature Power, Energy Ball | Ice Beam 54, Muddy Water 56, Hyper Voice 58, Leaf Storm 60, Psychic 62, Synthesis 65 | Ludicolo |
| Quagsire | super rod | 45 | Oxide | Mud Bomb, Amnesia, Yawn, Earthquake | Mist 48, Haze 48, Muddy Water 53 | Quagsire |
| Quagsire | super rod | 45 | Rewrite | Earthquake, Rock Slide, Toxic, Drain Punch | Mist 48, Muddy Water 53, Poison Jab 54, Aqua Tail 56, Recover 58, Rock Tomb 60, Toxic Spikes 62, Swagger 65 | Quagsire |
| Seaking | surf | 46 | Oxide | Flail, Aqua Ring, Fury Attack, Waterfall | Horn Drill 47, Agility 56, Megahorn 63 | Seaking |
| Seaking | surf | 46 | Rewrite | Aqua Jet, Skull Bash, Waterfall, Poison Jab | Drill Run 47, Knock Off 50, Aqua Tail 54, Agility 56, Drill Peck 57, Throat Chop 59, Megahorn 63 | Seaking |
| Hariyama | wild | 47 | Oxide | Force Palm, Seismic Toss, Wake-Up Slap, Endure | Close Combat 52, Reversal 57 | Hariyama |
| Hariyama | wild | 47 | Rewrite | Rock Tomb, Wake-Up Slap, Drain Punch, Endure | Close Combat 52, Upper Hand 54, Throat Chop 55, Reversal 57, Iron Head 60, Earthquake 65 | Hariyama |
| Corviknight | wild | 48 | Oxide | FeatherDance, Revenge, Defog, Iron Head | Brave Bird 49, Body Press 55, Roost 65 | Corviknight |
| Corviknight | wild | 48 | Rewrite | FeatherDance, Revenge, Defog, Iron Head | Brave Bird 49, Body Slam 52, Throat Chop 54, Body Press 55, Iron Defense 57, Swagger 60, Double-Edge 62, Roost 65 | Corviknight |
| Garganacl | wild | 48 | Oxide | Recover, Rock Slide, Stealth Rock, Heavy Slam | Earthquake 49, Stone Edge 54, Explosion 60 | Garganacl |
| Garganacl | wild | 48 | Rewrite | Salt Cure, Stealth Rock, Iron Head, Heavy Slam | Earthquake 49, Zen Headbutt 53, Block 54, Body Press 56, Hammer Arm 60, Curse 65 | Garganacl |
| Gastrodon | super rod | 48 | Oxide | Mud Bomb, Hidden Power, Body Slam, Muddy Water | Recover 54 | Gastrodon |
| Gastrodon | super rod | 48 | Rewrite | Clear Smog, Muddy Water, Bulldoze, Sludge Bomb | Ice Beam 49, Recover 54, Skitter Smack 56, Rock Tomb 60, Block 65 | Gastrodon |
| Houndoom | wild | 48 | Oxide | Fire Fang, Faint Attack, Embargo, Flamethrower | Crunch 54, Nasty Plot 60 | Houndoom |
| Houndoom | wild | 48 | Rewrite | Faint Attack, Mud Shot, Embargo, Flamethrower | Dark Pulse 51, Crunch 54, Shadow Ball 56, BurningJealousy 58, Nasty Plot 60, Sludge Bomb 62, Overheat 65 | Houndoom |
| Liepard | wild | 48 | Oxide | Sucker Punch, Nasty Plot, Night Slash, Snatch | Play Rough 54 | Liepard |
| Liepard | wild | 48 | Rewrite | Taunt, Sucker Punch, Night Slash, Snatch | Skitter Smack 50, Play Rough 54, BurningJealousy 56, Seed Bomb 58, Shadow Ball 60, U-turn 65 | Liepard |
| Mienshao | wild | 48 | Oxide | Aura Sphere, Me First, Jump Kick, Dual Chop | Focus Blast 51, Acrobatics 55, Hi Jump Kick 64 | Mienshao |
| Mienshao | wild | 48 | Rewrite | U-turn, Rock Tomb, Jump Kick, Dual Chop | Poison Jab 51, Upper Hand 54, Acrobatics 55, Hammer Arm 56, Hi Jump Kick 64 | Mienshao |
| Seaking | super rod | 48 | Oxide | Aqua Ring, Fury Attack, Waterfall, Horn Drill | Agility 56, Megahorn 63 | Seaking |
| Seaking | super rod | 48 | Rewrite | Skull Bash, Waterfall, Poison Jab, Drill Run | Knock Off 50, Aqua Tail 54, Agility 56, Drill Peck 57, Throat Chop 59, Megahorn 63 | Seaking |
| Talonflame | wild | 48 | Oxide | Natural Gift, Acrobatics, Me First, Tailwind | Flare Blitz 51, Brave Bird 55 | Talonflame |
| Talonflame | wild | 48 | Rewrite | Steel Wing, Flamethrower, Tailwind, Upper Hand | Flare Blitz 51, Overheat 54, Brave Bird 55, Agility 57, U-turn 60, Bulk Up 65 | Talonflame |
| Toucannon | wild | 48 | Oxide | Screech, Drill Peck, Bullet Seed, FeatherDance | Hyper Voice 50 | Toucannon |
| Toucannon | wild | 48 | Rewrite | Bullet Seed, Throat Chop, FeatherDance, Take Down | Hyper Voice 50, Brick Break 54, Temper Flare 56, Rock Climb 60, Brave Bird 65 | Toucannon |
| Donphan | wild | 49 | Oxide | Fury Attack, Assurance, Scary Face, Earthquake | Giga Impact 54 | Donphan |
| Donphan | wild | 49 | Rewrite | Scary Face, Iron Head, Throat Chop, Earthquake | Seed Bomb 50, Giga Impact 54, Charm 56, Block 61 | Donphan |
| Dubwool | wild | 49 | Oxide | Take Down, Guard Swap, Reversal, Cotton Guard | Double-Edge 50, Last Resort 56 | Dubwool |
| Dubwool | wild | 49 | Rewrite | Reversal, Zen Headbutt, Cotton Guard, Body Press | Double-Edge 50, Wild Charge 54, Last Resort 56, Thunder Wave 61 | Dubwool |
| Golem | wild | 49 | Oxide | Earthquake, Explosion, Double-Edge, Stone Edge | nothing | Golem |
| Golem | wild | 49 | Rewrite | Rock Blast, Earthquake, Double-Edge, Rock Slide | Body Press 53, Body Slam 56, Fire Punch 61, Hammer Arm 65 | Golem |
| Hawlucha | wild | 49 | Oxide | Dual Wingbeat, Fly, Hi Jump Kick, Me First | Acrobatics 55, Close Combat 60 | Hawlucha |
| Hawlucha | wild | 49 | Rewrite | Fly, Hi Jump Kick, Air Slash, Lunge | Throat Chop 54, Acrobatics 55, Low Sweep 57, Close Combat 60, Fire Punch 62, Brave Bird 65 | Hawlucha |
| Grapploct | wild | 50 | Oxide | Taunt, Reversal, Superpower, Topsy-Turvy | nothing | Grapploct |
| Grapploct | wild | 50 | Rewrite | Bulk Up, Taunt, Reversal, Superpower | Drain Punch 53, Sucker Punch 54, Liquidation 56, StompingTantrum 60, Close Combat 65 | Grapploct |
| Honchkrow | wild | 50 | Oxide | Wing Attack, Swagger, Nasty Plot, Night Slash | Dark Pulse 55 | Honchkrow |
| Honchkrow | wild | 50 | Rewrite | Swagger, Drill Peck, Night Slash, Nasty Plot | Heat Wave 54, Dark Pulse 55, Foul Play 57, U-turn 60, Sucker Punch 62, Brave Bird 65 | Honchkrow |
| Ninetales | wild | 50 | Oxide | Quick Attack, Confuse Ray, Safeguard, Flare Blitz | nothing | Ninetales |
| Ninetales | wild | 50 | Rewrite | Confuse Ray, Safeguard, Dazzling Gleam, Flare Blitz | Energy Ball 54, Extrasensory 56, Moonblast 58, Mystical Fire 60, Ice Beam 62, Overheat 65 | Ninetales |
| Greninja | super rod | 51 | Oxide | Dark Pulse, Extrasensory, Sludge Wave, Gunk Shot | Hydro Pump 55, Hydro Cannon 65 | Greninja |
| Greninja | super rod | 51 | Rewrite | Dark Pulse, Extrasensory, Sludge Wave, Gunk Shot | Ice Beam 54, Surf 56, Throat Chop 58, Muddy Water 60, Taunt 62, Hydro Cannon 65 | Greninja |

## Route 226

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 65 | At the cap |
|---|---|---|---|---|---|---|
| Meloetta | in-game trade | 1 | Oxide | Round, Quick Attack, Confusion, Sing | Quick Attack 6, Confusion 11, Sing 16, Teeter Dance 21, Acrobatics 26, Psybeam 31, Echoed Voice 36, U-turn 43, Wake-Up Slap 50, Psychic 57, Hyper Voice 64 | Meloetta |
| Meloetta | in-game trade | 1 | Rewrite | Round, Quick Attack, Confusion, Sing | Quick Attack 6, Confusion 11, Sing 16, Teeter Dance 21, Acrobatics 26, Psybeam 31, U-turn 43, Wake-Up Slap 50, Psychic 57, Energy Ball 61, Charm 62, Hyper Voice 64 | Meloetta |
| Mantyke | old rod | 22 | Oxide | BubbleBeam, Headbutt, Agility, Wing Attack | Water Pulse 28; as Mantine: Take Down 31, Confuse Ray 37, Bounce 40, Aqua Ring 46, Hydro Pump 49 | Mantine (from 30) |
| Mantyke | old rod | 22 | Rewrite | BubbleBeam, Headbutt, Agility, Wing Attack | Icy Wind 25, Water Pulse 28; as Mantine: Take Down 31, Signal Beam 34, Round 35, Confuse Ray 37, Bounce 40, Psybeam 41, Surf 43, Aqua Ring 46, Scald 49, Air Slash 54, Roost 56, Muddy Water 58, Ice Beam 60, Swagger 65 | Mantine (from 30) |
| Psyduck | old rod | 22 | Oxide | Water Gun, Disable, Confusion, Water Pulse | Fury Swipes 27, Screech 31; as Golduck: Psych Up 37, Zen Headbutt 44, Amnesia 50, Hydro Pump 56 | Golduck (from 33) |
| Psyduck | old rod | 22 | Rewrite | Water Pulse, Disable, Confusion, Low Sweep | Fury Swipes 27; as Golduck: Surf 34, Psych Up 37, Aurora Beam 40, Zen Headbutt 44, Power Gem 47, Amnesia 50, Ice Beam 54, Muddy Water 56, Flip Turn 58, Psychic 60, Confuse Ray 65 | Golduck (from 33) |
| Finneon | old rod | 24 | Oxide | Water Gun, Attract, Gust, Water Pulse | Captivate 26, Safeguard 29; as Lumineon: Aqua Ring 35, Whirlpool 42, U-turn 48, Bounce 53, Silver Wind 59 | Lumineon (from 31) |
| Finneon | old rod | 24 | Rewrite | Attract, Water Pulse, Pursuit, Gust | Captivate 26, Safeguard 29; as Lumineon: Flip Turn 31, Aqua Ring 33, Icy Wind 34, Aqua Tail 38, Signal Beam 40, Whirlpool 42, Ice Fang 45, U-turn 48, Bounce 53, Air Slash 54, Crunch 56, Confuse Ray 57, Silver Wind 59, Charm 65 | Lumineon (from 31) |
| Shellos | old rod | 24 | Oxide | Harden, Water Pulse, Mud Bomb, Hidden Power | Body Slam 29; as Gastrodon: Muddy Water 41, Recover 54 | Gastrodon (from 30) |
| Shellos | old rod | 24 | Rewrite | Water Pulse, Mud Bomb, Hidden Power, Swagger | Body Slam 29; as Gastrodon: AncientPower 33, Earth Power 35, Clear Smog 37, Muddy Water 41, Bulldoze 44, Sludge Bomb 46, Ice Beam 49, Recover 54, Skitter Smack 56, Rock Tomb 60, Block 65 | Gastrodon (from 30) |
| Carvanha | old rod | 26 | Oxide | Ice Fang, Screech, Swagger, Assurance | Crunch 28; as Sharpedo: Slash 30, Aqua Jet 34, Taunt 40, Agility 45, Skull Bash 50, Night Slash 56 | Sharpedo (from 30) |
| Carvanha | old rod | 26 | Rewrite | Screech, Swagger, Aqua Cutter, Assurance | Crunch 28; as Sharpedo: Slash 30, Aqua Jet 31, Bug Bite 35, Aerial Ace 37, Taunt 40, Liquidation 41, Agility 45, Skull Bash 50, Poison Fang 54, Night Slash 56, Poison Jab 58, Flip Turn 60, Throat Chop 65 | Sharpedo (from 30) |
| Lanturn | good rod | 35 | Oxide | Swallow, Spit Up, BubbleBeam, Signal Beam | Discharge 40, Aqua Ring 47, Hydro Pump 52, Charge 57 | Lanturn |
| Lanturn | good rod | 35 | Rewrite | BubbleBeam, Signal Beam, Scald, Surf | Thunderbolt 37, Discharge 40, Flash Cannon 43, Aqua Ring 47, Muddy Water 52, Volt Switch 54, Dazzling Gleam 55, Charge 57, Ice Beam 60, Swagger 65 | Lanturn |
| Mareanie | good rod | 35 | Oxide | Toxic Spikes, Recover, Spike Cannon, Pin Missile | Toxic 36; as Toxapex: Toxic 39, Venom Drench 42, Poison Jab 43, Liquidation 45 | Toxapex (from 38) |
| Mareanie | good rod | 35 | Rewrite | Toxic Spikes, Recover, Spike Cannon, Pin Missile | Toxic 36, Muddy Water 38; as Toxapex: Venom Drench 42, Poison Jab 43, Liquidation 45, Lunge 53, Ice Beam 54, Sludge Bomb 56, Iron Defense 61 | Toxapex (from 38) |
| Finneon | good rod | 37 | Oxide | Water Pulse, Captivate, Safeguard, Aqua Ring | Whirlpool 38; as Lumineon: Whirlpool 42, U-turn 48, Bounce 53, Silver Wind 59 | Lumineon (from 38) |
| Finneon | good rod | 37 | Rewrite | Gust, Captivate, Safeguard, Aqua Ring | Whirlpool 38; as Lumineon: Aqua Tail 38, Signal Beam 40, Whirlpool 42, Ice Fang 45, U-turn 48, Bounce 53, Air Slash 54, Crunch 56, Confuse Ray 57, Silver Wind 59, Charm 65 | Lumineon (from 38) |
| Tentacool | good rod | 37 | Oxide | Barrier, Water Pulse, Poison Jab, Screech | as Tentacruel: Screech 42, Hydro Pump 49, Wring Out 55 | Tentacruel (from 38) |
| Tentacool | good rod | 37 | Rewrite | BubbleBeam, Barrier, Poison Jab, Screech | as Tentacruel: Sludge Bomb 39, Screech 42, Psybeam 44, Surf 49, Muddy Water 53, Throat Chop 54, Power Gem 56, Flip Turn 58, Ice Beam 60, Toxic 62, Skitter Smack 65 | Tentacruel (from 38) |
| Greninja | good rod | 39 | Oxide | Low Kick, Waterfall, Fling, Scald | Dark Pulse 40, Extrasensory 43, Sludge Wave 47, Gunk Shot 51, Hydro Pump 55, Hydro Cannon 65 | Greninja |
| Greninja | good rod | 39 | Rewrite | Waterfall, Fling, Shadow Sneak, Scald | Dark Pulse 40, Extrasensory 43, Sludge Wave 47, Gunk Shot 51, Ice Beam 54, Surf 56, Throat Chop 58, Muddy Water 60, Taunt 62, Hydro Cannon 65 | Greninja |
| Floatzel | surf | 40 | Oxide | Aqua Jet, Crunch, Agility, Whirlpool | Razor Wind 50 | Floatzel |
| Floatzel | surf | 40 | Rewrite | Icy Wind, Flip Turn, Waterfall, Whirlpool | Liquidation 41, Low Sweep 44, Agility 51, Rock Tomb 53, Ice Fang 56, Wave Crash 62, Ice Punch 65 | Floatzel |
| Mareanie | surf | 40 | Oxide | Spike Cannon, Pin Missile, Toxic, Venom Drench | Liquidation 41, Poison Jab 41; as Toxapex: Venom Drench 42, Poison Jab 43, Liquidation 45 | Toxapex (from 41) |
| Mareanie | surf | 40 | Rewrite | Spike Cannon, Pin Missile, Toxic, Muddy Water | Liquidation 41; as Toxapex: Venom Drench 42, Poison Jab 43, Liquidation 45, Lunge 53, Ice Beam 54, Sludge Bomb 56, Iron Defense 61 | Toxapex (from 41) |
| Mantine | surf | 43 | Oxide | Water Pulse, Take Down, Confuse Ray, Bounce | Aqua Ring 46, Hydro Pump 49 | Mantine |
| Mantine | surf | 43 | Rewrite | Confuse Ray, Bounce, Psybeam, Surf | Aqua Ring 46, Scald 49, Air Slash 54, Roost 56, Muddy Water 58, Ice Beam 60, Swagger 65 | Mantine |
| Tentacruel | surf | 43 | Oxide | Barrier, Water Pulse, Poison Jab, Screech | Hydro Pump 49, Wring Out 55 | Tentacruel |
| Tentacruel | surf | 43 | Rewrite | Poison Jab, Aurora Beam, Sludge Bomb, Screech | Psybeam 44, Surf 49, Muddy Water 53, Throat Chop 54, Power Gem 56, Flip Turn 58, Ice Beam 60, Toxic 62, Skitter Smack 65 | Tentacruel |
| Mantine | super rod | 45 | Oxide | Water Pulse, Take Down, Confuse Ray, Bounce | Aqua Ring 46, Hydro Pump 49 | Mantine |
| Mantine | super rod | 45 | Rewrite | Confuse Ray, Bounce, Psybeam, Surf | Aqua Ring 46, Scald 49, Air Slash 54, Roost 56, Muddy Water 58, Ice Beam 60, Swagger 65 | Mantine |
| Toxapex | super rod | 45 | Oxide | Toxic, Venom Drench, Poison Jab, Liquidation | nothing | Toxapex |
| Toxapex | super rod | 45 | Rewrite | Pin Missile, Venom Drench, Poison Jab, Liquidation | Lunge 53, Ice Beam 54, Sludge Bomb 56, Iron Defense 61 | Toxapex |
| Greninja | surf | 46 | Oxide | Fling, Scald, Dark Pulse, Extrasensory | Sludge Wave 47, Gunk Shot 51, Hydro Pump 55, Hydro Cannon 65 | Greninja |
| Greninja | surf | 46 | Rewrite | Shadow Sneak, Scald, Dark Pulse, Extrasensory | Sludge Wave 47, Gunk Shot 51, Ice Beam 54, Surf 56, Throat Chop 58, Muddy Water 60, Taunt 62, Hydro Cannon 65 | Greninja |
| Corviknight | wild | 47 to 50 | Oxide | FeatherDance, Revenge, Defog, Iron Head | Brave Bird 49, Body Press 55, Roost 65 | Corviknight |
| Corviknight | wild | 47 to 50 | Rewrite | FeatherDance, Revenge, Defog, Iron Head | Brave Bird 49, Body Slam 52, Throat Chop 54, Body Press 55, Iron Defense 57, Swagger 60, Double-Edge 62, Roost 65 | Corviknight |
| Absol | wild | 48 | Oxide | Double Team, Slash, Future Sight, Sucker Punch | Detect 49, Night Slash 52, Me First 57, Psycho Cut 60, Perish Song 65 | Absol |
| Absol | wild | 48 | Rewrite | Slash, Future Sight, Sucker Punch, X-Scissor | Night Slash 52, Shadow Ball 54, Throat Chop 56, Rock Slide 58, Psycho Cut 60, Air Slash 62, Perish Song 65 | Absol |
| Altaria | wild | 48 | Oxide | Natural Gift, DragonBreath, Dragon Dance, Refresh | Dragon Pulse 54, Perish Song 62 | Altaria |
| Altaria | wild | 48 | Rewrite | Mirror Move, Bulldoze, Breaking Swipe, Refresh | Moonblast 50, Dragon Pulse 54, Dragon Rush 56, Flamethrower 57, Draco Meteor 59, Perish Song 62, Ice Beam 65 | Altaria |
| Araquanid | wild | 48 to 49 | Oxide | Soak, Dive, Lunge, Scald | Hydro Pump 51, Liquidation 55, Leech Life 61 | Araquanid |
| Araquanid | wild | 48 to 49 | Rewrite | Waterfall, Lunge, Poison Jab, Scald | Crunch 51, Body Slam 54, Liquidation 55, Ice Punch 58, Leech Life 61 | Araquanid |
| Mienshao | wild | 48 | Oxide | Aura Sphere, Me First, Jump Kick, Dual Chop | Focus Blast 51, Acrobatics 55, Hi Jump Kick 64 | Mienshao |
| Mienshao | wild | 48 | Rewrite | U-turn, Rock Tomb, Jump Kick, Dual Chop | Poison Jab 51, Upper Hand 54, Acrobatics 55, Hammer Arm 56, Hi Jump Kick 64 | Mienshao |
| Poliwrath | super rod | 48 | Oxide | Hypnosis, DoubleSlap, Submission, DynamicPunch | Mind Reader 53 | Poliwrath |
| Poliwrath | super rod | 48 | Rewrite | Hypnosis, DoubleSlap, Liquidation, Brick Break | Mind Reader 53, Rock Tomb 54, Throat Chop 56, Close Combat 58, Ice Punch 60, Upper Hand 62, Drain Punch 65 | Poliwrath |
| Relicanth | super rod | 48 | Oxide | Yawn, Take Down, Mud Sport, AncientPower | Double-Edge 50, Dive 57, Rest 64 | Relicanth |
| Relicanth | super rod | 48 | Rewrite | Yawn, Take Down, AncientPower, Bulldoze | Double-Edge 50, Aqua Tail 54, Rock Slide 55, Dive 57, Zen Headbutt 58, Earthquake 60, Body Press 62, Rest 64 | Relicanth |
| Skarmory | wild | 48 to 49 | Oxide | Steel Wing, Air Slash, Slash, Night Slash | nothing | Skarmory |
| Skarmory | wild | 48 to 49 | Rewrite | Air Slash, Slash, Night Slash, Iron Defense | Body Press 54, Drill Peck 56, Iron Head 58, Brave Bird 60, Rock Tomb 62, Double-Edge 65 | Skarmory |
| Talonflame | wild | 48 | Oxide | Natural Gift, Acrobatics, Me First, Tailwind | Flare Blitz 51, Brave Bird 55 | Talonflame |
| Talonflame | wild | 48 | Rewrite | Steel Wing, Flamethrower, Tailwind, Upper Hand | Flare Blitz 51, Overheat 54, Brave Bird 55, Agility 57, U-turn 60, Bulk Up 65 | Talonflame |
| Toucannon | wild | 48 to 49 | Oxide | Screech, Drill Peck, Bullet Seed, FeatherDance | Hyper Voice 50 | Toucannon |
| Toucannon | wild | 48 to 49 | Rewrite | Bullet Seed, Throat Chop, FeatherDance, Take Down | Hyper Voice 50, Brick Break 54, Temper Flare 56, Rock Climb 60, Brave Bird 65 | Toucannon |
| Carbink | wild | 49 | Oxide | Stealth Rock, Skill Swap, Light Screen, Power Gem | Moonblast 52, Stone Edge 54 | Carbink |
| Carbink | wild | 49 | Rewrite | Stealth Rock, Skill Swap, Light Screen, Power Gem | Moonblast 52, Iron Head 54, Psychic 56, Body Press 60 | Carbink |
| Floatzel | wild | 50 | Oxide | Crunch, Agility, Whirlpool, Razor Wind | nothing | Floatzel |
| Floatzel | wild | 50 | Rewrite | Waterfall, Whirlpool, Liquidation, Low Sweep | Agility 51, Rock Tomb 53, Ice Fang 56, Wave Crash 62, Ice Punch 65 | Floatzel |
| Shellos | wild | 50 | Oxide | Hidden Power, Body Slam, Muddy Water, Recover | as Gastrodon: Recover 54 | Gastrodon (from 51) |
| Shellos | wild | 50 | Rewrite | Swagger, Body Slam, Muddy Water, Recover | as Gastrodon: Recover 54, Skitter Smack 56, Rock Tomb 60, Block 65 | Gastrodon (from 51) |
| Kingdra | super rod | 51 | Oxide | Twister, Brine, Hydro Pump, Dragon Dance | Dragon Pulse 57 | Kingdra |
| Kingdra | super rod | 51 | Rewrite | Twister, Brine, Octazooka, Aurora Beam | Scald 54, Dragon Pulse 57, Wave Crash 60, Dragon Dance 62, Iron Head 65 | Kingdra |

## Route 227

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 65 | At the cap |
|---|---|---|---|---|---|---|
| Chinchou | old rod | 22 | Oxide | Flail, Water Gun, Confuse Ray, Spark | Take Down 23; as Lanturn: Stockpile 27, Swallow 27, Spit Up 27, BubbleBeam 30, Signal Beam 35, Discharge 40, Aqua Ring 47, Hydro Pump 52, Charge 57 | Lanturn (from 27) |
| Chinchou | old rod | 22 | Rewrite | Water Gun, Screech, Confuse Ray, Spark | Take Down 23, Icy Wind 26; as Lanturn: Stockpile 27, Swallow 28, Spit Up 29, BubbleBeam 30, Signal Beam 31, Scald 33, Surf 34, Thunderbolt 37, Discharge 40, Flash Cannon 43, Aqua Ring 47, Muddy Water 52, Volt Switch 54, Dazzling Gleam 55, Charge 57, Ice Beam 60, Swagger 65 | Lanturn (from 27) |
| Tentacool | old rod | 22 | Oxide | Acid, Toxic Spikes, BubbleBeam, Wrap | Barrier 26, Water Pulse 29; as Tentacruel: Poison Jab 36, Screech 42, Hydro Pump 49, Wring Out 55 | Tentacruel (from 30) |
| Tentacool | old rod | 22 | Rewrite | Acid, Toxic Spikes, Water Pulse, BubbleBeam | Barrier 26; as Tentacruel: Poison Jab 33, Aurora Beam 34, Sludge Bomb 39, Screech 42, Psybeam 44, Surf 49, Muddy Water 53, Throat Chop 54, Power Gem 56, Flip Turn 58, Ice Beam 60, Toxic 62, Skitter Smack 65 | Tentacruel (from 30) |
| Barboach | old rod | 24 | Oxide | Water Gun, Mud Bomb, Amnesia, Water Pulse | Magnitude 26; as Whiscash: Rest 33, Snore 33, Aqua Tail 39, Earthquake 45, Future Sight 51, Fissure 57 | Whiscash (from 30) |
| Barboach | old rod | 24 | Rewrite | Mud Bomb, Amnesia, Rock Tomb, Water Pulse | Magnitude 26; as Whiscash: Bulldoze 30, Rest 33, Zen Headbutt 36, Aqua Tail 39, Earth Power 40, Wild Charge 42, Earthquake 45, Future Sight 51, Spark 54, Ice Beam 56, Tickle 60, Swagger 65 | Whiscash (from 30) |
| Goldeen | old rod | 24 | Oxide | Supersonic, Horn Attack, Water Pulse, Flail | Aqua Ring 27, Fury Attack 31; as Seaking: Waterfall 40, Horn Drill 47, Agility 56, Megahorn 63 | Seaking (from 33) |
| Goldeen | old rod | 24 | Rewrite | Water Pulse, Horn Attack, Swagger, Flail | Aqua Ring 27; as Seaking: Aqua Jet 34, Skull Bash 37, Waterfall 40, Poison Jab 44, Drill Run 47, Knock Off 50, Aqua Tail 54, Agility 56, Drill Peck 57, Throat Chop 59, Megahorn 63 | Seaking (from 33) |
| Frogadier | old rod | 26 | Oxide | Icy Wind, Faint Attack, Acrobatics, Low Kick | Waterfall 30, Fling 35; as Greninja: Scald 37, Dark Pulse 40, Extrasensory 43, Sludge Wave 47, Gunk Shot 51, Hydro Pump 55, Hydro Cannon 65 | Greninja (from 36) |
| Frogadier | old rod | 26 | Rewrite | Thief, Faint Attack, Acrobatics, Low Kick | Mud Shot 27, Waterfall 30, Fling 35; as Greninja: Shadow Sneak 36, Scald 37, Dark Pulse 40, Extrasensory 43, Sludge Wave 47, Gunk Shot 51, Ice Beam 54, Surf 56, Throat Chop 58, Muddy Water 60, Taunt 62, Hydro Cannon 65 | Greninja (from 36) |
| Goldeen | good rod | 35 | Oxide | Water Pulse, Flail, Aqua Ring, Fury Attack | as Seaking: Waterfall 40, Horn Drill 47, Agility 56, Megahorn 63 | Seaking (from 36) |
| Goldeen | good rod | 35 | Rewrite | Horn Attack, Swagger, Flail, Aqua Ring | as Seaking: Skull Bash 37, Waterfall 40, Poison Jab 44, Drill Run 47, Knock Off 50, Aqua Tail 54, Agility 56, Drill Peck 57, Throat Chop 59, Megahorn 63 | Seaking (from 36) |
| Golduck | good rod | 35 | Oxide | Confusion, Water Pulse, Fury Swipes, Screech | Psych Up 37, Zen Headbutt 44, Amnesia 50, Hydro Pump 56 | Golduck |
| Golduck | good rod | 35 | Rewrite | Water Pulse, Fury Swipes, Screech, Surf | Psych Up 37, Aurora Beam 40, Zen Headbutt 44, Power Gem 47, Amnesia 50, Ice Beam 54, Muddy Water 56, Flip Turn 58, Psychic 60, Confuse Ray 65 | Golduck |
| Barboach | good rod | 37 | Oxide | Magnitude, Rest, Snore, Aqua Tail | as Whiscash: Aqua Tail 39, Earthquake 45, Future Sight 51, Fissure 57 | Whiscash (from 38) |
| Barboach | good rod | 37 | Rewrite | Amnesia, Rock Tomb, Water Pulse, Magnitude | as Whiscash: Aqua Tail 39, Earth Power 40, Wild Charge 42, Earthquake 45, Future Sight 51, Spark 54, Ice Beam 56, Tickle 60, Swagger 65 | Whiscash (from 38) |
| Feebas | good rod | 37 | Oxide | Splash, Tackle, Flail | as Milotic: Attract 41, Safeguard 45, Aqua Ring 49 | Milotic (from 38) |
| Feebas | good rod | 37 | Rewrite | Recover, Dragon Tail, Captivate, Flail | as Milotic: Attract 41, Muddy Water 43, Safeguard 45, Aqua Ring 49, Alluring Voice 54, Scald 56, Ice Beam 58, Hyper Voice 60, Draco Meteor 62, Confuse Ray 65 | Milotic (from 38) |
| Starmie | good rod | 39 | Oxide | Rapid Spin, Recover, Swift, Confuse Ray | nothing | Starmie |
| Starmie | good rod | 39 | Rewrite | Swift, Confuse Ray, Psybeam, Icy Wind | Scald 45, Power Gem 54, Signal Beam 56, Surf 58, Psychic 60, Ice Beam 62, Thunderbolt 65 | Starmie |
| Feebas | surf | 40 | Oxide | Splash, Tackle, Flail | as Milotic: Attract 41, Safeguard 45, Aqua Ring 49 | Milotic (from 41) |
| Feebas | surf | 40 | Rewrite | Recover, Dragon Tail, Captivate, Flail | as Milotic: Attract 41, Muddy Water 43, Safeguard 45, Aqua Ring 49, Alluring Voice 54, Scald 56, Ice Beam 58, Hyper Voice 60, Draco Meteor 62, Confuse Ray 65 | Milotic (from 41) |
| Gastrodon | surf | 40 | Oxide | Water Pulse, Mud Bomb, Hidden Power, Body Slam | Muddy Water 41, Recover 54 | Gastrodon |
| Gastrodon | surf | 40 | Rewrite | Body Slam, AncientPower, Earth Power, Clear Smog | Muddy Water 41, Bulldoze 44, Sludge Bomb 46, Ice Beam 49, Recover 54, Skitter Smack 56, Rock Tomb 60, Block 65 | Gastrodon |
| Corphish | surf | 43 | Oxide | Knock Off, Taunt, Night Slash, Crabhammer | Swords Dance 44; as Crawdaunt: Crabhammer 44, Swords Dance 52, Crunch 57, Guillotine 65 | Crawdaunt (from 44) |
| Corphish | surf | 43 | Rewrite | Leer, Razor Shell, Knock Off, Crabhammer | Swords Dance 44; as Crawdaunt: Crabhammer 44, Brick Break 48, Swords Dance 52, Rock Tomb 54, Crunch 57, Swagger 61 | Crawdaunt (from 44) |
| Goldeen | surf | 43 | Oxide | Aqua Ring, Fury Attack, Waterfall, Horn Drill | as Seaking: Horn Drill 47, Agility 56, Megahorn 63 | Seaking (from 44) |
| Goldeen | surf | 43 | Rewrite | Swagger, Flail, Aqua Ring, Waterfall | as Seaking: Poison Jab 44, Drill Run 47, Knock Off 50, Aqua Tail 54, Agility 56, Drill Peck 57, Throat Chop 59, Megahorn 63 | Seaking (from 44) |
| Seaking | super rod | 45 | Oxide | Flail, Aqua Ring, Fury Attack, Waterfall | Horn Drill 47, Agility 56, Megahorn 63 | Seaking |
| Seaking | super rod | 45 | Rewrite | Aqua Jet, Skull Bash, Waterfall, Poison Jab | Drill Run 47, Knock Off 50, Aqua Tail 54, Agility 56, Drill Peck 57, Throat Chop 59, Megahorn 63 | Seaking |
| Whiscash | super rod | 45 | Oxide | Rest, Snore, Aqua Tail, Earthquake | Future Sight 51, Fissure 57 | Whiscash |
| Whiscash | super rod | 45 | Rewrite | Aqua Tail, Earth Power, Wild Charge, Earthquake | Future Sight 51, Spark 54, Ice Beam 56, Tickle 60, Swagger 65 | Whiscash |
| Corsola | surf | 46 | Oxide | AncientPower, Aqua Ring, Spike Cannon, Power Gem | Mirror Coat 48, Earth Power 53 | Corsola |
| Corsola | surf | 46 | Rewrite | Aqua Ring, Spike Cannon, Throat Chop, Power Gem | Mirror Coat 48, Earth Power 53, Rock Slide 54, Rock Tomb 56, Body Slam 58, Earthquake 60, Ice Punch 62, Sucker Punch 65 | Corsola |
| Crawdaunt | super rod | 48 | Oxide | Swift, Taunt, Night Slash, Crabhammer | Swords Dance 52, Crunch 57, Guillotine 65 | Crawdaunt |
| Crawdaunt | super rod | 48 | Rewrite | Night Slash, X-Scissor, Crabhammer, Brick Break | Swords Dance 52, Rock Tomb 54, Crunch 57, Swagger 61 | Crawdaunt |
| Milotic | super rod | 48 | Oxide | Aqua Tail, Hydro Pump, Attract, Safeguard | Aqua Ring 49 | Milotic |
| Milotic | super rod | 48 | Rewrite | Surf, Attract, Muddy Water, Safeguard | Aqua Ring 49, Alluring Voice 54, Scald 56, Ice Beam 58, Hyper Voice 60, Draco Meteor 62, Confuse Ray 65 | Milotic |
| Ceruledge | wild | 51 | Oxide | Lava Plume, Swords Dance, Ally Switch, Bitter Blade | Psycho Cut 56, Flare Blitz 62 | Ceruledge |
| Ceruledge | wild | 51 | Rewrite | Shadow Claw, Lava Plume, Swords Dance, Bitter Blade | Throat Chop 52, Iron Head 54, Psycho Cut 56, Flare Blitz 62, Poltergeist 65 | Ceruledge |
| Sharpedo | super rod | 51 | Oxide | Aqua Jet, Taunt, Agility, Skull Bash | Night Slash 56 | Sharpedo |
| Sharpedo | super rod | 51 | Rewrite | Taunt, Liquidation, Agility, Skull Bash | Poison Fang 54, Night Slash 56, Poison Jab 58, Flip Turn 60, Throat Chop 65 | Sharpedo |
| Houndoom | wild | 52 to 53 | Oxide | Fire Fang, Faint Attack, Embargo, Flamethrower | Crunch 54, Nasty Plot 60 | Houndoom |
| Houndoom | wild | 52 to 53 | Rewrite | Mud Shot, Embargo, Flamethrower, Dark Pulse | Crunch 54, Shadow Ball 56, BurningJealousy 58, Nasty Plot 60, Sludge Bomb 62, Overheat 65 | Houndoom |
| Ninetales | wild | 52 | Oxide | Quick Attack, Confuse Ray, Safeguard, Flare Blitz | nothing | Ninetales |
| Ninetales | wild | 52 | Rewrite | Confuse Ray, Safeguard, Dazzling Gleam, Flare Blitz | Energy Ball 54, Extrasensory 56, Moonblast 58, Mystical Fire 60, Ice Beam 62, Overheat 65 | Ninetales |
| Rapidash | wild | 52 | Oxide | Agility, Fire Blast, Fury Attack, Bounce | Flare Blitz 56 | Rapidash |
| Rapidash | wild | 52 | Rewrite | Heat Wave, Overheat, Bounce, Psychic | Jump Kick 54, Flare Blitz 56, Zen Headbutt 58, Poison Jab 60, Morning Sun 65 | Rapidash |
| Rhyperior | wild | 52 | Oxide | Horn Drill, Hammer Arm, Stone Edge, Earthquake | Megahorn 57, Rock Wrecker 61 | Rhyperior |
| Rhyperior | wild | 52 | Rewrite | Take Down, Hammer Arm, Rock Slide, Earthquake | Megahorn 57, Rock Wrecker 61, Crunch 65 | Rhyperior |
| Salazzle | wild | 52 to 53 | Oxide | Venoshock, Flamethrower, Sludge Bomb, Dragon Pulse | Fire Blast 55 | Salazzle |
| Salazzle | wild | 52 to 53 | Rewrite | Sludge Bomb, Encore, Swagger, Dragon Pulse | Nasty Plot 54, Overheat 61, Hyper Voice 65 | Salazzle |
| Skarmory | wild | 52 | Oxide | Steel Wing, Air Slash, Slash, Night Slash | nothing | Skarmory |
| Skarmory | wild | 52 | Rewrite | Air Slash, Slash, Night Slash, Iron Defense | Body Press 54, Drill Peck 56, Iron Head 58, Brave Bird 60, Rock Tomb 62, Double-Edge 65 | Skarmory |
| Weezing | wild | 52 | Oxide | Haze, Double Hit, Explosion, Sludge Bomb | Destiny Bond 55, Memento 63 | Weezing |
| Weezing | wild | 52 | Rewrite | Sludge, Shadow Ball, Psybeam, Sludge Bomb | Strange Steam 53, Flamethrower 54, Poison Fang 56, Dark Pulse 58, Will-O-Wisp 60, Overheat 65 | Weezing |
| Magcargo | wild | 53 | Oxide | Amnesia, Lava Plume, Rock Slide, Body Slam | Flamethrower 61 | Magcargo |
| Magcargo | wild | 53 | Rewrite | Shell Smash, Scorching Sands, Rock Slide, Body Slam | BurningJealousy 54, Energy Ball 56, Yawn 57, Power Gem 58, Flamethrower 61, Overheat 63 | Magcargo |
| Turtonator | wild | 53 | Oxide | Body Slam, Flamethrower, Dragon Pulse, Fire Spin | Explosion 55, Overheat 61 | Turtonator |
| Turtonator | wild | 53 | Rewrite | Dragon Pulse, Shell Smash, Fire Spin, Body Press | Earthquake 54, BurningJealousy 56, Flash Cannon 57, Rock Tomb 58, Overheat 61, Iron Defense 63 | Turtonator |
| Chatot | wild | 54 | Oxide | Roost, Uproar, FeatherDance, Hyper Voice | nothing | Chatot |
| Chatot | wild | 54 | Rewrite | Air Slash, Hyper Voice, Steel Wing, Parting Shot | Brave Bird 56, Heat Wave 61 | Chatot |
| Garganacl | wild | 54 | Oxide | Stealth Rock, Heavy Slam, Earthquake, Stone Edge | Explosion 60 | Garganacl |
| Garganacl | wild | 54 | Rewrite | Heavy Slam, Earthquake, Zen Headbutt, Block | Body Press 56, Hammer Arm 60, Curse 65 | Garganacl |
| Honchkrow | wild | 54 | Oxide | Wing Attack, Swagger, Nasty Plot, Night Slash | Dark Pulse 55 | Honchkrow |
| Honchkrow | wild | 54 | Rewrite | Drill Peck, Night Slash, Nasty Plot, Heat Wave | Dark Pulse 55, Foul Play 57, U-turn 60, Sucker Punch 62, Brave Bird 65 | Honchkrow |

## Route 228

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 65 | At the cap |
|---|---|---|---|---|---|---|
| Buizel | old rod | 22 | Oxide | Water Gun, Pursuit, Swift, Aqua Jet | as Floatzel: Crunch 26, Agility 29, Whirlpool 39, Razor Wind 50 | Floatzel (from 26) |
| Buizel | old rod | 22 | Rewrite | Pursuit, Scary Face, Swift, Aqua Jet | as Floatzel: Crunch 26, Icy Wind 29, Flip Turn 33, Waterfall 36, Whirlpool 39, Liquidation 41, Low Sweep 44, Agility 51, Rock Tomb 53, Ice Fang 56, Wave Crash 62, Ice Punch 65 | Floatzel (from 26) |
| Goldeen | old rod | 22 | Oxide | Supersonic, Horn Attack, Water Pulse, Flail | Aqua Ring 27, Fury Attack 31; as Seaking: Waterfall 40, Horn Drill 47, Agility 56, Megahorn 63 | Seaking (from 33) |
| Goldeen | old rod | 22 | Rewrite | Water Pulse, Horn Attack, Swagger, Flail | Aqua Ring 27; as Seaking: Aqua Jet 34, Skull Bash 37, Waterfall 40, Poison Jab 44, Drill Run 47, Knock Off 50, Aqua Tail 54, Agility 56, Drill Peck 57, Throat Chop 59, Megahorn 63 | Seaking (from 33) |
| Barboach | old rod | 24 | Oxide | Water Gun, Mud Bomb, Amnesia, Water Pulse | Magnitude 26; as Whiscash: Rest 33, Snore 33, Aqua Tail 39, Earthquake 45, Future Sight 51, Fissure 57 | Whiscash (from 30) |
| Barboach | old rod | 24 | Rewrite | Mud Bomb, Amnesia, Rock Tomb, Water Pulse | Magnitude 26; as Whiscash: Bulldoze 30, Rest 33, Zen Headbutt 36, Aqua Tail 39, Earth Power 40, Wild Charge 42, Earthquake 45, Future Sight 51, Spark 54, Ice Beam 56, Tickle 60, Swagger 65 | Whiscash (from 30) |
| Krabby | old rod | 24 | Oxide | Harden, BubbleBeam, Mud Shot, Metal Claw | Stomp 25; as Kingler: Protect 32, Guillotine 37, Slam 44, Brine 51, Crabhammer 56, Flail 63 | Kingler (from 28) |
| Krabby | old rod | 24 | Rewrite | Wide Guard, BubbleBeam, Mud Shot, Metal Claw | Stomp 25; as Kingler: Waterfall 34, Razor Shell 36, Rock Tomb 39, X-Scissor 41, Slam 44, Night Slash 47, Brine 51, Liquidation 54, Crabhammer 56, Rock Slide 59, Flail 63 | Kingler (from 28) |
| Clamperl | old rod | 26 | Oxide | Clamp, Water Gun, Whirlpool, Iron Defense | as Huntail: Brine 28, Baton Pass 33, Dive 37, Crunch 42, Aqua Tail 46, Hydro Pump 51 | Huntail (from 26) |
| Clamperl | old rod | 26 | Oxide | Clamp, Water Gun, Whirlpool, Iron Defense | as Gorebyss: Captivate 28, Baton Pass 33, Dive 37, Psychic 42, Aqua Tail 46, Hydro Pump 51 | Gorebyss (from 26) |
| Clamperl | old rod | 26 | Rewrite | Whirlpool, Iron Defense, Brine, Bite | as Huntail: Brine 28, Baton Pass 33, Flip Turn 35, Dive 37, Waterfall 40, Crunch 42, Aqua Tail 46, Muddy Water 51, Rock Tomb 54, Leech Life 56, Shell Smash 58, Sucker Punch 60, Agility 62, Confuse Ray 65 | Huntail (from 26) |
| Clamperl | old rod | 26 | Rewrite | Whirlpool, Iron Defense, Brine, Bite | as Gorebyss: Captivate 28, Baton Pass 33, Draining Kiss 35, Dive 37, Surf 40, Psychic 42, Aqua Tail 46, Muddy Water 51, Shadow Ball 54, Ice Beam 56, Shell Smash 58, Scald 60, Scary Face 62, Confuse Ray 65 | Gorebyss (from 26) |
| Gastrodon | good rod | 35 | Oxide | Water Pulse, Mud Bomb, Hidden Power, Body Slam | Muddy Water 41, Recover 54 | Gastrodon |
| Gastrodon | good rod | 35 | Rewrite | Hidden Power, Body Slam, AncientPower, Earth Power | Clear Smog 37, Muddy Water 41, Bulldoze 44, Sludge Bomb 46, Ice Beam 49, Recover 54, Skitter Smack 56, Rock Tomb 60, Block 65 | Gastrodon |
| Goldeen | good rod | 35 | Oxide | Water Pulse, Flail, Aqua Ring, Fury Attack | as Seaking: Waterfall 40, Horn Drill 47, Agility 56, Megahorn 63 | Seaking (from 36) |
| Goldeen | good rod | 35 | Rewrite | Horn Attack, Swagger, Flail, Aqua Ring | as Seaking: Skull Bash 37, Waterfall 40, Poison Jab 44, Drill Run 47, Knock Off 50, Aqua Tail 54, Agility 56, Drill Peck 57, Throat Chop 59, Megahorn 63 | Seaking (from 36) |
| Barboach | good rod | 37 | Oxide | Magnitude, Rest, Snore, Aqua Tail | as Whiscash: Aqua Tail 39, Earthquake 45, Future Sight 51, Fissure 57 | Whiscash (from 38) |
| Barboach | good rod | 37 | Rewrite | Amnesia, Rock Tomb, Water Pulse, Magnitude | as Whiscash: Aqua Tail 39, Earth Power 40, Wild Charge 42, Earthquake 45, Future Sight 51, Spark 54, Ice Beam 56, Tickle 60, Swagger 65 | Whiscash (from 38) |
| Corphish | good rod | 37 | Oxide | Protect, Knock Off, Taunt, Night Slash | Crabhammer 38; as Crawdaunt: Night Slash 39, Crabhammer 44, Swords Dance 52, Crunch 57, Guillotine 65 | Crawdaunt (from 38) |
| Corphish | good rod | 37 | Rewrite | BubbleBeam, Leer, Razor Shell, Knock Off | Crabhammer 38; as Crawdaunt: Night Slash 39, X-Scissor 41, Crabhammer 44, Brick Break 48, Swords Dance 52, Rock Tomb 54, Crunch 57, Swagger 61 | Crawdaunt (from 38) |
| Masquerain | good rod | 39 | Oxide | Water Sport, Gust, Scary Face, Stun Spore | Silver Wind 40, Air Slash 47, Whirlwind 54, Bug Buzz 61 | Masquerain |
| Masquerain | good rod | 39 | Rewrite | Mud Bomb, Stun Spore, Surf, Giga Drain | Silver Wind 40, Signal Beam 41, Icy Wind 43, Air Slash 47, Lunge 53, Skitter Smack 54, Ice Beam 56, U-turn 57, Leech Life 58, Bug Buzz 61, Energy Ball 65 | Masquerain |
| Gastrodon | surf | 40 | Oxide | Water Pulse, Mud Bomb, Hidden Power, Body Slam | Muddy Water 41, Recover 54 | Gastrodon |
| Gastrodon | surf | 40 | Rewrite | Body Slam, AncientPower, Earth Power, Clear Smog | Muddy Water 41, Bulldoze 44, Sludge Bomb 46, Ice Beam 49, Recover 54, Skitter Smack 56, Rock Tomb 60, Block 65 | Gastrodon |
| Quagsire | surf | 40 | Oxide | Mud Bomb, Amnesia, Yawn, Earthquake | Mist 48, Haze 48, Muddy Water 53 | Quagsire |
| Quagsire | surf | 40 | Rewrite | Yawn, Earthquake, Rock Slide, Toxic | Drain Punch 44, Mist 48, Muddy Water 53, Poison Jab 54, Aqua Tail 56, Recover 58, Rock Tomb 60, Toxic Spikes 62, Swagger 65 | Quagsire |
| Ludicolo | surf | 43 | Oxide | Astonish, Growl, Mega Drain, Nature Power | nothing | Ludicolo |
| Ludicolo | surf | 43 | Rewrite | Growl, Mega Drain, Nature Power, Energy Ball | Ice Beam 54, Muddy Water 56, Hyper Voice 58, Leaf Storm 60, Psychic 62, Synthesis 65 | Ludicolo |
| Masquerain | surf | 43 | Oxide | Gust, Scary Face, Stun Spore, Silver Wind | Air Slash 47, Whirlwind 54, Bug Buzz 61 | Masquerain |
| Masquerain | surf | 43 | Rewrite | Giga Drain, Silver Wind, Signal Beam, Icy Wind | Air Slash 47, Lunge 53, Skitter Smack 54, Ice Beam 56, U-turn 57, Leech Life 58, Bug Buzz 61, Energy Ball 65 | Masquerain |
| Seaking | super rod | 45 | Oxide | Flail, Aqua Ring, Fury Attack, Waterfall | Horn Drill 47, Agility 56, Megahorn 63 | Seaking |
| Seaking | super rod | 45 | Rewrite | Aqua Jet, Skull Bash, Waterfall, Poison Jab | Drill Run 47, Knock Off 50, Aqua Tail 54, Agility 56, Drill Peck 57, Throat Chop 59, Megahorn 63 | Seaking |
| Whiscash | super rod | 45 | Oxide | Rest, Snore, Aqua Tail, Earthquake | Future Sight 51, Fissure 57 | Whiscash |
| Whiscash | super rod | 45 | Rewrite | Aqua Tail, Earth Power, Wild Charge, Earthquake | Future Sight 51, Spark 54, Ice Beam 56, Tickle 60, Swagger 65 | Whiscash |
| Tentacruel | surf | 46 | Oxide | Barrier, Water Pulse, Poison Jab, Screech | Hydro Pump 49, Wring Out 55 | Tentacruel |
| Tentacruel | surf | 46 | Rewrite | Aurora Beam, Sludge Bomb, Screech, Psybeam | Surf 49, Muddy Water 53, Throat Chop 54, Power Gem 56, Flip Turn 58, Ice Beam 60, Toxic 62, Skitter Smack 65 | Tentacruel |
| Crawdaunt | super rod | 48 | Oxide | Swift, Taunt, Night Slash, Crabhammer | Swords Dance 52, Crunch 57, Guillotine 65 | Crawdaunt |
| Crawdaunt | super rod | 48 | Rewrite | Night Slash, X-Scissor, Crabhammer, Brick Break | Swords Dance 52, Rock Tomb 54, Crunch 57, Swagger 61 | Crawdaunt |
| Lanturn | super rod | 48 | Oxide | BubbleBeam, Signal Beam, Discharge, Aqua Ring | Hydro Pump 52, Charge 57 | Lanturn |
| Lanturn | super rod | 48 | Rewrite | Thunderbolt, Discharge, Flash Cannon, Aqua Ring | Muddy Water 52, Volt Switch 54, Dazzling Gleam 55, Charge 57, Ice Beam 60, Swagger 65 | Lanturn |
| Whiscash | wild | 49 | Oxide | Rest, Snore, Aqua Tail, Earthquake | Future Sight 51, Fissure 57 | Whiscash |
| Whiscash | wild | 49 | Rewrite | Aqua Tail, Earth Power, Wild Charge, Earthquake | Future Sight 51, Spark 54, Ice Beam 56, Tickle 60, Swagger 65 | Whiscash |
| Crustle | wild | 50 | Oxide | Rock Slide, StompingTantrum, Knock Off, Leech Life | Stone Edge 54, Rock Wrecker 61 | Crustle |
| Crustle | wild | 50 | Rewrite | Body Press, Shell Smash, Knock Off, Leech Life | Skitter Smack 54, Poison Jab 56, Rock Polish 57, Bulldoze 58, Rock Wrecker 61, Lunge 63, Earthquake 65 | Crustle |
| Donphan | wild | 50 to 51 | Oxide | Fury Attack, Assurance, Scary Face, Earthquake | Giga Impact 54 | Donphan |
| Donphan | wild | 50 to 51 | Rewrite | Iron Head, Throat Chop, Earthquake, Seed Bomb | Giga Impact 54, Charm 56, Block 61 | Donphan |
| Flygon | wild | 50 | Oxide | Supersonic, DragonBreath, Screech, Dragon Claw | Hyper Beam 57 | Flygon |
| Flygon | wild | 50 | Rewrite | Sand Tomb, DragonBreath, Screech, Dragon Claw | Poison Fang 54, Dragon Rush 56, Hyper Beam 57, Bug Buzz 58, Fire Punch 60, FirstImpression 62, Draco Meteor 65 | Flygon |
| Golem | wild | 50 | Oxide | Earthquake, Explosion, Double-Edge, Stone Edge | nothing | Golem |
| Golem | wild | 50 | Rewrite | Rock Blast, Earthquake, Double-Edge, Rock Slide | Body Press 53, Body Slam 56, Fire Punch 61, Hammer Arm 65 | Golem |
| Houndoom | wild | 50 | Oxide | Fire Fang, Faint Attack, Embargo, Flamethrower | Crunch 54, Nasty Plot 60 | Houndoom |
| Houndoom | wild | 50 | Rewrite | Faint Attack, Mud Shot, Embargo, Flamethrower | Dark Pulse 51, Crunch 54, Shadow Ball 56, BurningJealousy 58, Nasty Plot 60, Sludge Bomb 62, Overheat 65 | Houndoom |
| Palossand | wild | 50 | Oxide | Giga Drain, Iron Defense, Shadow Ball, Earth Power | Shore Up 57 | Palossand |
| Palossand | wild | 50 | Rewrite | Iron Defense, Shadow Ball, Sludge Bomb, Earth Power | Psychic 54, Flash Cannon 55, Shore Up 57, Energy Ball 60, Confuse Ray 65 | Palossand |
| Glimmora | wild | 51 | Oxide | Rock Slide, Power Gem, Acid Armor, Sludge Wave | nothing | Glimmora |
| Glimmora | wild | 51 | Rewrite | Sludge Bomb, Acid Armor, Flash Cannon, Sludge Wave | Energy Ball 54, Dazzling Gleam 56, Earth Power 60, Confuse Ray 65 | Glimmora |
| Masquerain | super rod | 51 | Oxide | Scary Face, Stun Spore, Silver Wind, Air Slash | Whirlwind 54, Bug Buzz 61 | Masquerain |
| Masquerain | super rod | 51 | Rewrite | Silver Wind, Signal Beam, Icy Wind, Air Slash | Lunge 53, Skitter Smack 54, Ice Beam 56, U-turn 57, Leech Life 58, Bug Buzz 61, Energy Ball 65 | Masquerain |
| Rhyperior | wild | 51 | Oxide | Horn Drill, Hammer Arm, Stone Edge, Earthquake | Megahorn 57, Rock Wrecker 61 | Rhyperior |
| Rhyperior | wild | 51 | Rewrite | Take Down, Hammer Arm, Rock Slide, Earthquake | Megahorn 57, Rock Wrecker 61, Crunch 65 | Rhyperior |
| Salazzle | wild | 51 | Oxide | Venoshock, Flamethrower, Sludge Bomb, Dragon Pulse | Fire Blast 55 | Salazzle |
| Salazzle | wild | 51 | Rewrite | Sludge Bomb, Encore, Swagger, Dragon Pulse | Nasty Plot 54, Overheat 61, Hyper Voice 65 | Salazzle |
| Carbink | wild | 52 | Oxide | Skill Swap, Light Screen, Power Gem, Moonblast | Stone Edge 54 | Carbink |
| Carbink | wild | 52 | Rewrite | Skill Swap, Light Screen, Power Gem, Moonblast | Iron Head 54, Psychic 56, Body Press 60 | Carbink |
| Garganacl | wild | 52 | Oxide | Rock Slide, Stealth Rock, Heavy Slam, Earthquake | Stone Edge 54, Explosion 60 | Garganacl |
| Garganacl | wild | 52 | Rewrite | Stealth Rock, Iron Head, Heavy Slam, Earthquake | Zen Headbutt 53, Block 54, Body Press 56, Hammer Arm 60, Curse 65 | Garganacl |
| Steelix | wild | 52 | Oxide | Curse, Iron Tail, Crunch, Double-Edge | Stone Edge 54 | Steelix |
| Steelix | wild | 52 | Rewrite | Iron Head, Bite, Crunch, Double-Edge | Rock Slide 54, Aqua Tail 56, Fire Fang 58, Earthquake 60, Block 65 | Steelix |

## Route 229

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 65 | At the cap |
|---|---|---|---|---|---|---|
| Barboach | old rod | 22 | Oxide | Water Gun, Mud Bomb, Amnesia, Water Pulse | Magnitude 26; as Whiscash: Rest 33, Snore 33, Aqua Tail 39, Earthquake 45, Future Sight 51, Fissure 57 | Whiscash (from 30) |
| Barboach | old rod | 22 | Rewrite | Mud Bomb, Amnesia, Rock Tomb, Water Pulse | Magnitude 26; as Whiscash: Bulldoze 30, Rest 33, Zen Headbutt 36, Aqua Tail 39, Earth Power 40, Wild Charge 42, Earthquake 45, Future Sight 51, Spark 54, Ice Beam 56, Tickle 60, Swagger 65 | Whiscash (from 30) |
| Goldeen | old rod | 22 | Oxide | Supersonic, Horn Attack, Water Pulse, Flail | Aqua Ring 27, Fury Attack 31; as Seaking: Waterfall 40, Horn Drill 47, Agility 56, Megahorn 63 | Seaking (from 33) |
| Goldeen | old rod | 22 | Rewrite | Water Pulse, Horn Attack, Swagger, Flail | Aqua Ring 27; as Seaking: Aqua Jet 34, Skull Bash 37, Waterfall 40, Poison Jab 44, Drill Run 47, Knock Off 50, Aqua Tail 54, Agility 56, Drill Peck 57, Throat Chop 59, Megahorn 63 | Seaking (from 33) |
| Corphish | old rod | 24 | Oxide | ViceGrip, Leer, BubbleBeam, Protect | Knock Off 26; as Crawdaunt: Swift 30, Taunt 34, Night Slash 39, Crabhammer 44, Swords Dance 52, Crunch 57, Guillotine 65 | Crawdaunt (from 30) |
| Corphish | old rod | 24 | Rewrite | ViceGrip, BubbleBeam, Leer, Razor Shell | Knock Off 26; as Crawdaunt: Swift 30, Taunt 32, Throat Chop 35, Aerial Ace 36, Night Slash 39, X-Scissor 41, Crabhammer 44, Brick Break 48, Swords Dance 52, Rock Tomb 54, Crunch 57, Swagger 61 | Crawdaunt (from 30) |
| Poliwag | old rod | 24 | Oxide | Hypnosis, Water Gun, DoubleSlap, Body Slam | BubbleBeam 25; as Poliwrath: DynamicPunch 43, Mind Reader 53 | Poliwrath (from 25) |
| Poliwag | old rod | 24 | Oxide | Hypnosis, Water Gun, DoubleSlap, Body Slam | BubbleBeam 25; as Politoed: Swagger 27, Bounce 37, Hyper Voice 48 | Politoed (from 25) |
| Poliwag | old rod | 24 | Rewrite | Hypnosis, Mud Shot, DoubleSlap, Body Slam | BubbleBeam 25; as Poliwhirl: Bulldoze 25; as Poliwrath: Liquidation 34, Brick Break 43, Mind Reader 53, Rock Tomb 54, Throat Chop 56, Close Combat 58, Ice Punch 60, Upper Hand 62, Drain Punch 65 | Poliwrath (from 25) |
| Poliwag | old rod | 24 | Rewrite | Hypnosis, Mud Shot, DoubleSlap, Body Slam | BubbleBeam 25; as Poliwhirl: Bulldoze 25; as Politoed: Swagger 27, Bounce 37, Hyper Voice 48, Ice Beam 57, Muddy Water 60, Psychic 62, Belly Drum 65 | Politoed (from 25) |
| Masquerain | old rod | 26 | Oxide | Sweet Scent, Water Sport, Gust, Scary Face | Stun Spore 33, Silver Wind 40, Air Slash 47, Whirlwind 54, Bug Buzz 61 | Masquerain |
| Masquerain | old rod | 26 | Rewrite | Water Sport, Gust, BubbleBeam, Scary Face | Mud Bomb 29, Stun Spore 33, Surf 36, Giga Drain 38, Silver Wind 40, Signal Beam 41, Icy Wind 43, Air Slash 47, Lunge 53, Skitter Smack 54, Ice Beam 56, U-turn 57, Leech Life 58, Bug Buzz 61, Energy Ball 65 | Masquerain |
| Barboach | good rod | 35 | Oxide | Magnitude, Rest, Snore, Aqua Tail | as Whiscash: Aqua Tail 39, Earthquake 45, Future Sight 51, Fissure 57 | Whiscash (from 36) |
| Barboach | good rod | 35 | Rewrite | Amnesia, Rock Tomb, Water Pulse, Magnitude | as Whiscash: Zen Headbutt 36, Aqua Tail 39, Earth Power 40, Wild Charge 42, Earthquake 45, Future Sight 51, Spark 54, Ice Beam 56, Tickle 60, Swagger 65 | Whiscash (from 36) |
| Goldeen | good rod | 35 | Oxide | Water Pulse, Flail, Aqua Ring, Fury Attack | as Seaking: Waterfall 40, Horn Drill 47, Agility 56, Megahorn 63 | Seaking (from 36) |
| Goldeen | good rod | 35 | Rewrite | Horn Attack, Swagger, Flail, Aqua Ring | as Seaking: Skull Bash 37, Waterfall 40, Poison Jab 44, Drill Run 47, Knock Off 50, Aqua Tail 54, Agility 56, Drill Peck 57, Throat Chop 59, Megahorn 63 | Seaking (from 36) |
| Chinchou | good rod | 37 | Oxide | Take Down, BubbleBeam, Signal Beam, Discharge | as Lanturn: Discharge 40, Aqua Ring 47, Hydro Pump 52, Charge 57 | Lanturn (from 38) |
| Chinchou | good rod | 37 | Rewrite | Take Down, Icy Wind, Signal Beam, Discharge | as Lanturn: Discharge 40, Flash Cannon 43, Aqua Ring 47, Muddy Water 52, Volt Switch 54, Dazzling Gleam 55, Charge 57, Ice Beam 60, Swagger 65 | Lanturn (from 38) |
| Corphish | good rod | 37 | Oxide | Protect, Knock Off, Taunt, Night Slash | Crabhammer 38; as Crawdaunt: Night Slash 39, Crabhammer 44, Swords Dance 52, Crunch 57, Guillotine 65 | Crawdaunt (from 38) |
| Corphish | good rod | 37 | Rewrite | BubbleBeam, Leer, Razor Shell, Knock Off | Crabhammer 38; as Crawdaunt: Night Slash 39, X-Scissor 41, Crabhammer 44, Brick Break 48, Swords Dance 52, Rock Tomb 54, Crunch 57, Swagger 61 | Crawdaunt (from 38) |
| Ludicolo | good rod | 39 | Oxide | Astonish, Growl, Mega Drain, Nature Power | nothing | Ludicolo |
| Ludicolo | good rod | 39 | Rewrite | Growl, Mega Drain, Nature Power, Energy Ball | Ice Beam 54, Muddy Water 56, Hyper Voice 58, Leaf Storm 60, Psychic 62, Synthesis 65 | Ludicolo |
| Ludicolo | surf | 40 | Oxide | Astonish, Growl, Mega Drain, Nature Power | nothing | Ludicolo |
| Ludicolo | surf | 40 | Rewrite | Growl, Mega Drain, Nature Power, Energy Ball | Ice Beam 54, Muddy Water 56, Hyper Voice 58, Leaf Storm 60, Psychic 62, Synthesis 65 | Ludicolo |
| Quagsire | surf | 40 | Oxide | Mud Bomb, Amnesia, Yawn, Earthquake | Mist 48, Haze 48, Muddy Water 53 | Quagsire |
| Quagsire | surf | 40 | Rewrite | Yawn, Earthquake, Rock Slide, Toxic | Drain Punch 44, Mist 48, Muddy Water 53, Poison Jab 54, Aqua Tail 56, Recover 58, Rock Tomb 60, Toxic Spikes 62, Swagger 65 | Quagsire |
| Goldeen | surf | 43 | Oxide | Aqua Ring, Fury Attack, Waterfall, Horn Drill | as Seaking: Horn Drill 47, Agility 56, Megahorn 63 | Seaking (from 44) |
| Goldeen | surf | 43 | Rewrite | Swagger, Flail, Aqua Ring, Waterfall | as Seaking: Poison Jab 44, Drill Run 47, Knock Off 50, Aqua Tail 54, Agility 56, Drill Peck 57, Throat Chop 59, Megahorn 63 | Seaking (from 44) |
| Masquerain | surf | 43 | Oxide | Gust, Scary Face, Stun Spore, Silver Wind | Air Slash 47, Whirlwind 54, Bug Buzz 61 | Masquerain |
| Masquerain | surf | 43 | Rewrite | Giga Drain, Silver Wind, Signal Beam, Icy Wind | Air Slash 47, Lunge 53, Skitter Smack 54, Ice Beam 56, U-turn 57, Leech Life 58, Bug Buzz 61, Energy Ball 65 | Masquerain |
| Crawdaunt | super rod | 45 | Oxide | Swift, Taunt, Night Slash, Crabhammer | Swords Dance 52, Crunch 57, Guillotine 65 | Crawdaunt |
| Crawdaunt | super rod | 45 | Rewrite | Aerial Ace, Night Slash, X-Scissor, Crabhammer | Brick Break 48, Swords Dance 52, Rock Tomb 54, Crunch 57, Swagger 61 | Crawdaunt |
| Whiscash | super rod | 45 | Oxide | Rest, Snore, Aqua Tail, Earthquake | Future Sight 51, Fissure 57 | Whiscash |
| Whiscash | super rod | 45 | Rewrite | Aqua Tail, Earth Power, Wild Charge, Earthquake | Future Sight 51, Spark 54, Ice Beam 56, Tickle 60, Swagger 65 | Whiscash |
| Whiscash | surf | 46 | Oxide | Rest, Snore, Aqua Tail, Earthquake | Future Sight 51, Fissure 57 | Whiscash |
| Whiscash | surf | 46 | Rewrite | Aqua Tail, Earth Power, Wild Charge, Earthquake | Future Sight 51, Spark 54, Ice Beam 56, Tickle 60, Swagger 65 | Whiscash |
| Heracross | wild | 47 | Oxide | Counter, Take Down, Close Combat, Reversal | Feint 49, Megahorn 55 | Heracross |
| Heracross | wild | 47 | Rewrite | Close Combat, Throat Chop, Reversal, Skitter Smack | Lunge 49, Bulldoze 54, Megahorn 55, Upper Hand 60, Earthquake 65 | Heracross |
| Galvantula | wild | 48 | Oxide | Signal Beam, Energy Ball, Sucker Punch, Thunderbolt | Bug Buzz 51, Thunder 55, Volt Switch 65 | Galvantula |
| Galvantula | wild | 48 | Rewrite | Swift, Giga Drain, Sucker Punch, Thunderbolt | Bug Buzz 51, Screech 54, Agility 56, Sticky Web 60, Sludge Bomb 62, Volt Switch 65 | Galvantula |
| Lanturn | super rod | 48 | Oxide | BubbleBeam, Signal Beam, Discharge, Aqua Ring | Hydro Pump 52, Charge 57 | Lanturn |
| Lanturn | super rod | 48 | Rewrite | Thunderbolt, Discharge, Flash Cannon, Aqua Ring | Muddy Water 52, Volt Switch 54, Dazzling Gleam 55, Charge 57, Ice Beam 60, Swagger 65 | Lanturn |
| Leavanny | wild | 48 | Oxide | Leaf Blade, X-Scissor, Entrainment, Swords Dance | Leaf Storm 50 | Leavanny |
| Leavanny | wild | 48 | Rewrite | X-Scissor, Poison Jab, Entrainment, Swords Dance | Leaf Storm 50, Shadow Claw 54, Lunge 56, Throat Chop 58, Skitter Smack 60, Take Down 62, Slash 65 | Leavanny |
| Liepard | wild | 48 | Oxide | Sucker Punch, Nasty Plot, Night Slash, Snatch | Play Rough 54 | Liepard |
| Liepard | wild | 48 | Rewrite | Taunt, Sucker Punch, Night Slash, Snatch | Skitter Smack 50, Play Rough 54, BurningJealousy 56, Seed Bomb 58, Shadow Ball 60, U-turn 65 | Liepard |
| Lopunny | wild | 48 | Oxide | Agility, Dizzy Punch, Charm, Bounce | Healing Wish 53 | Lopunny |
| Lopunny | wild | 48 | Rewrite | Strength, Body Slam, Charm, Bounce | Crunch 49, U-turn 53, Low Sweep 54, Blaze Kick 56, Slam 58, Drain Punch 60, Fire Punch 65 | Lopunny |
| Mightyena | wild | 48 | Oxide | Crunch, Scary Face, Taunt, Embargo | Take Down 52, Thief 57, Sucker Punch 62 | Mightyena |
| Mightyena | wild | 48 | Rewrite | Strength, Taunt, Headbutt, Embargo | Take Down 52, Poison Fang 54, Fire Fang 55, Thief 57, Thunder Fang 59, Sucker Punch 62, Yawn 65 | Mightyena |
| Roserade | wild | 48 | Oxide | Poison Sting, Mega Drain, Magical Leaf, Sweet Scent | nothing | Roserade |
| Roserade | wild | 48 | Rewrite | Poison Sting, Mega Drain, Magical Leaf, Energy Ball | Shadow Ball 57, Dazzling Gleam 60, Sludge Wave 62, Leaf Storm 65 | Roserade |
| Sharpedo | super rod | 48 | Oxide | Slash, Aqua Jet, Taunt, Agility | Skull Bash 50, Night Slash 56 | Sharpedo |
| Sharpedo | super rod | 48 | Rewrite | Aerial Ace, Taunt, Liquidation, Agility | Skull Bash 50, Poison Fang 54, Night Slash 56, Poison Jab 58, Flip Turn 60, Throat Chop 65 | Sharpedo |
| Talonflame | wild | 48 | Oxide | Natural Gift, Acrobatics, Me First, Tailwind | Flare Blitz 51, Brave Bird 55 | Talonflame |
| Talonflame | wild | 48 | Rewrite | Steel Wing, Flamethrower, Tailwind, Upper Hand | Flare Blitz 51, Overheat 54, Brave Bird 55, Agility 57, U-turn 60, Bulk Up 65 | Talonflame |
| Arboliva | wild | 49 | Oxide | Seed Bomb, Energy Ball, Leech Seed, Terrain Pulse | Petal Blizzard 52, Petal Dance 58 | Arboliva |
| Arboliva | wild | 49 | Rewrite | Energy Ball, Leech Seed, Alluring Voice, Swift | Petal Blizzard 52, Hyper Voice 54, Pollen Puff 55, Petal Dance 58, Earth Power 60, Leaf Storm 65 | Arboliva |
| Emolga | wild | 49 | Oxide | Acrobatics, Encore, Light Screen, Volt Switch | Discharge 50, Agility 50 | Emolga |
| Emolga | wild | 49 | Rewrite | Light Screen, Volt Switch, Thunderbolt, Agility | Discharge 50, Energy Ball 54, Air Slash 56, Shadow Ball 60, Charm 65 | Emolga |
| Tsareena | wild | 49 | Oxide | Low Sweep, Aromatherapy, Leaf Storm, Power Whip | Hi Jump Kick 55 | Tsareena |
| Tsareena | wild | 49 | Rewrite | Aromatherapy, Zen Headbutt, Leaf Storm, Petal Blizzard | U-turn 51, Play Rough 54, Hi Jump Kick 55, Knock Off 60, Charm 65 | Tsareena |
| Vespiquen | wild | 49 | Oxide | Captivate, Attack Order, Swagger, Destiny Bond | nothing | Vespiquen |
| Vespiquen | wild | 49 | Rewrite | Swagger, U-turn, Air Slash, Poison Jab | Psychic Noise 53, Take Down 54, Sludge Bomb 56, Secret Power 60, Brave Bird 65 | Vespiquen |
| Cherrim | wild | 50 | Oxide | Worry Seed, Take Down, SolarBeam, Lucky Chant | nothing | Cherrim |
| Cherrim | wild | 50 | Rewrite | Rock Slide, SolarBeam, Petal Dance, Lucky Chant | Giga Drain 53, Body Slam 54, Pollen Puff 56, Play Rough 58, Blaze Kick 60, Leaf Storm 62, Flare Blitz 65 | Cherrim |
| Jumpluff | wild | 50 | Oxide | U-turn, Worry Seed, Giga Drain, Bounce | Memento 52 | Jumpluff |
| Jumpluff | wild | 50 | Rewrite | Energy Ball, Giga Drain, Lunge, Bounce | Dazzling Gleam 53, Headbutt 54, Take Down 56, Air Slash 58, Secret Power 60, Brave Bird 62, Leaf Storm 65 | Jumpluff |
| Vikavolt | wild | 50 | Oxide | Bite, Spark, Signal Beam, Discharge | Bug Buzz 55, Thunderbolt 65 | Vikavolt |
| Vikavolt | wild | 50 | Rewrite | Spark, Signal Beam, Pollen Puff, Discharge | Energy Ball 54, Bug Buzz 55, Air Slash 57, Flash Cannon 60, Agility 62, Thunderbolt 65 | Vikavolt |
| Greninja | super rod | 51 | Oxide | Dark Pulse, Extrasensory, Sludge Wave, Gunk Shot | Hydro Pump 55, Hydro Cannon 65 | Greninja |
| Greninja | super rod | 51 | Rewrite | Dark Pulse, Extrasensory, Sludge Wave, Gunk Shot | Ice Beam 54, Surf 56, Throat Chop 58, Muddy Water 60, Taunt 62, Hydro Cannon 65 | Greninja |

## Route 230

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 65 | At the cap |
|---|---|---|---|---|---|---|
| Remoraid | old rod | 22 | Oxide | Lock-On, Psybeam, Aurora Beam, BubbleBeam | Focus Energy 23; as Octillery: Octazooka 25, Bullet Seed 29, Wring Out 36, Signal Beam 42, Ice Beam 48, Hyper Beam 55 | Octillery (from 25) |
| Remoraid | old rod | 22 | Rewrite | Psybeam, Screech, Aurora Beam, BubbleBeam | Focus Energy 23; as Octillery: Octazooka 25, Mud Shot 27, Bullet Seed 29, Round 33, Charge Beam 35, Scald 37, Skitter Smack 40, Signal Beam 42, Ice Beam 48, Psychic 54, Hyper Beam 55, Swagger 61 | Octillery (from 25) |
| Tentacool | old rod | 22 | Oxide | Acid, Toxic Spikes, BubbleBeam, Wrap | Barrier 26, Water Pulse 29; as Tentacruel: Poison Jab 36, Screech 42, Hydro Pump 49, Wring Out 55 | Tentacruel (from 30) |
| Tentacool | old rod | 22 | Rewrite | Acid, Toxic Spikes, Water Pulse, BubbleBeam | Barrier 26; as Tentacruel: Poison Jab 33, Aurora Beam 34, Sludge Bomb 39, Screech 42, Psybeam 44, Surf 49, Muddy Water 53, Throat Chop 54, Power Gem 56, Flip Turn 58, Ice Beam 60, Toxic 62, Skitter Smack 65 | Tentacruel (from 30) |
| Barboach | old rod | 24 | Oxide | Water Gun, Mud Bomb, Amnesia, Water Pulse | Magnitude 26; as Whiscash: Rest 33, Snore 33, Aqua Tail 39, Earthquake 45, Future Sight 51, Fissure 57 | Whiscash (from 30) |
| Barboach | old rod | 24 | Rewrite | Mud Bomb, Amnesia, Rock Tomb, Water Pulse | Magnitude 26; as Whiscash: Bulldoze 30, Rest 33, Zen Headbutt 36, Aqua Tail 39, Earth Power 40, Wild Charge 42, Earthquake 45, Future Sight 51, Spark 54, Ice Beam 56, Tickle 60, Swagger 65 | Whiscash (from 30) |
| Mantyke | old rod | 24 | Oxide | BubbleBeam, Headbutt, Agility, Wing Attack | Water Pulse 28; as Mantine: Take Down 31, Confuse Ray 37, Bounce 40, Aqua Ring 46, Hydro Pump 49 | Mantine (from 30) |
| Mantyke | old rod | 24 | Rewrite | BubbleBeam, Headbutt, Agility, Wing Attack | Icy Wind 25, Water Pulse 28; as Mantine: Take Down 31, Signal Beam 34, Round 35, Confuse Ray 37, Bounce 40, Psybeam 41, Surf 43, Aqua Ring 46, Scald 49, Air Slash 54, Roost 56, Muddy Water 58, Ice Beam 60, Swagger 65 | Mantine (from 30) |
| Frogadier | old rod | 26 | Oxide | Icy Wind, Faint Attack, Acrobatics, Low Kick | Waterfall 30, Fling 35; as Greninja: Scald 37, Dark Pulse 40, Extrasensory 43, Sludge Wave 47, Gunk Shot 51, Hydro Pump 55, Hydro Cannon 65 | Greninja (from 36) |
| Frogadier | old rod | 26 | Rewrite | Thief, Faint Attack, Acrobatics, Low Kick | Mud Shot 27, Waterfall 30, Fling 35; as Greninja: Shadow Sneak 36, Scald 37, Dark Pulse 40, Extrasensory 43, Sludge Wave 47, Gunk Shot 51, Ice Beam 54, Surf 56, Throat Chop 58, Muddy Water 60, Taunt 62, Hydro Cannon 65 | Greninja (from 36) |
| Alomomola | good rod | 35 | Oxide | Protect, Water Pulse, Wake-Up Slap, Soak | Wish 37, Brine 41, Safeguard 45, Whirlpool 49, Helping Hand 53, Healing Wish 57, Wide Guard 61, Hydro Pump 65 | Alomomola |
| Alomomola | good rod | 35 | Rewrite | Wake-Up Slap, Water Pulse, Soak, Play Rough | Wish 37, Brine 41, Zen Headbutt 43, Safeguard 45, Whirlpool 49, Helping Hand 53, Flip Turn 54, Liquidation 56, Ice Punch 57, Body Slam 58, Wide Guard 61, Muddy Water 65 | Alomomola |
| Tentacool | good rod | 35 | Oxide | Wrap, Barrier, Water Pulse, Poison Jab | Screech 36; as Tentacruel: Poison Jab 36, Screech 42, Hydro Pump 49, Wring Out 55 | Tentacruel (from 36) |
| Tentacool | good rod | 35 | Rewrite | Water Pulse, BubbleBeam, Barrier, Poison Jab | Screech 36; as Tentacruel: Sludge Bomb 39, Screech 42, Psybeam 44, Surf 49, Muddy Water 53, Throat Chop 54, Power Gem 56, Flip Turn 58, Ice Beam 60, Toxic 62, Skitter Smack 65 | Tentacruel (from 36) |
| Corsola | good rod | 37 | Oxide | BubbleBeam, Lucky Chant, AncientPower, Aqua Ring | Spike Cannon 40, Power Gem 44, Mirror Coat 48, Earth Power 53 | Corsola |
| Corsola | good rod | 37 | Rewrite | Lucky Chant, Aqua Cutter, Liquidation, Aqua Ring | Spike Cannon 40, Throat Chop 42, Power Gem 44, Mirror Coat 48, Earth Power 53, Rock Slide 54, Rock Tomb 56, Body Slam 58, Earthquake 60, Ice Punch 62, Sucker Punch 65 | Corsola |
| Gastrodon | good rod | 37 | Oxide | Water Pulse, Mud Bomb, Hidden Power, Body Slam | Muddy Water 41, Recover 54 | Gastrodon |
| Gastrodon | good rod | 37 | Rewrite | Body Slam, AncientPower, Earth Power, Clear Smog | Muddy Water 41, Bulldoze 44, Sludge Bomb 46, Ice Beam 49, Recover 54, Skitter Smack 56, Rock Tomb 60, Block 65 | Gastrodon |
| Wailmer | good rod | 39 | Oxide | Rest, Brine, Water Spout, Amnesia | as Wailord: Dive 46, Bounce 54, Hydro Pump 62 | Wailord (from 40) |
| Wailmer | good rod | 39 | Rewrite | Bulldoze, Brine, Water Spout, Amnesia | as Wailord: Dive 46, Iron Head 48, Rock Tomb 50, Bounce 54, Zen Headbutt 55, Ice Beam 56, Surf 62, Earthquake 65 | Wailord (from 40) |
| Tentacool | surf | 40 | Oxide | Water Pulse, Poison Jab, Screech, Hydro Pump | as Tentacruel: Screech 42, Hydro Pump 49, Wring Out 55 | Tentacruel (from 41) |
| Tentacool | surf | 40 | Rewrite | Barrier, Poison Jab, Screech, Surf | as Tentacruel: Screech 42, Psybeam 44, Surf 49, Muddy Water 53, Throat Chop 54, Power Gem 56, Flip Turn 58, Ice Beam 60, Toxic 62, Skitter Smack 65 | Tentacruel (from 41) |
| Toxapex | surf | 40 | Oxide | Recover, Spike Cannon, Pin Missile, Toxic | Venom Drench 42, Poison Jab 43, Liquidation 45 | Toxapex |
| Toxapex | surf | 40 | Rewrite | Recover, Spike Cannon, Toxic, Pin Missile | Venom Drench 42, Poison Jab 43, Liquidation 45, Lunge 53, Ice Beam 54, Sludge Bomb 56, Iron Defense 61 | Toxapex |
| Mantyke | surf | 43 | Oxide | Water Pulse, Take Down, Confuse Ray, Bounce | as Mantine: Aqua Ring 46, Hydro Pump 49 | Mantine (from 44) |
| Mantyke | surf | 43 | Rewrite | Water Pulse, Take Down, Confuse Ray, Bounce | as Mantine: Aqua Ring 46, Scald 49, Air Slash 54, Roost 56, Muddy Water 58, Ice Beam 60, Swagger 65 | Mantine (from 44) |
| Pelipper | surf | 43 | Oxide | Stockpile, Swallow, Spit Up, Fling | Tailwind 50, Hydro Pump 57 | Pelipper |
| Pelipper | surf | 43 | Rewrite | Stockpile, Spit Up, Icy Wind, Fling | Air Slash 47, Tailwind 50, Brave Bird 53, Ice Beam 54, U-turn 55, Muddy Water 57, Bite 60, Agility 62, Knock Off 65 | Pelipper |
| Lanturn | super rod | 45 | Oxide | Spit Up, BubbleBeam, Signal Beam, Discharge | Aqua Ring 47, Hydro Pump 52, Charge 57 | Lanturn |
| Lanturn | super rod | 45 | Rewrite | Surf, Thunderbolt, Discharge, Flash Cannon | Aqua Ring 47, Muddy Water 52, Volt Switch 54, Dazzling Gleam 55, Charge 57, Ice Beam 60, Swagger 65 | Lanturn |
| Lumineon | super rod | 45 | Oxide | Captivate, Safeguard, Aqua Ring, Whirlpool | U-turn 48, Bounce 53, Silver Wind 59 | Lumineon |
| Lumineon | super rod | 45 | Rewrite | Aqua Tail, Signal Beam, Whirlpool, Ice Fang | U-turn 48, Bounce 53, Air Slash 54, Crunch 56, Confuse Ray 57, Silver Wind 59, Charm 65 | Lumineon |
| Relicanth | surf | 46 | Oxide | Yawn, Take Down, Mud Sport, AncientPower | Double-Edge 50, Dive 57, Rest 64 | Relicanth |
| Relicanth | surf | 46 | Rewrite | Yawn, Take Down, AncientPower, Bulldoze | Double-Edge 50, Aqua Tail 54, Rock Slide 55, Dive 57, Zen Headbutt 58, Earthquake 60, Body Press 62, Rest 64 | Relicanth |
| Galarian Rapidash | wild | 47 to 50 | Oxide | Psybeam, Stomp, Heal Pulse, Take Down | Dazzling Gleam 49, Psychic 56, Healing Wish 63 | Galarian Rapidash |
| Galarian Rapidash | wild | 47 to 50 | Rewrite | Heal Pulse, Overheat, Take Down, Drill Run | Dazzling Gleam 49, Jump Kick 54, Psychic 56, Play Rough 58, Poison Jab 60, Flare Blitz 63, High Horsepower 65 | Galarian Rapidash |
| Absol | wild | 48 | Oxide | Double Team, Slash, Future Sight, Sucker Punch | Detect 49, Night Slash 52, Me First 57, Psycho Cut 60, Perish Song 65 | Absol |
| Absol | wild | 48 | Rewrite | Slash, Future Sight, Sucker Punch, X-Scissor | Night Slash 52, Shadow Ball 54, Throat Chop 56, Rock Slide 58, Psycho Cut 60, Air Slash 62, Perish Song 65 | Absol |
| Altaria | wild | 48 | Oxide | Natural Gift, DragonBreath, Dragon Dance, Refresh | Dragon Pulse 54, Perish Song 62 | Altaria |
| Altaria | wild | 48 | Rewrite | Mirror Move, Bulldoze, Breaking Swipe, Refresh | Moonblast 50, Dragon Pulse 54, Dragon Rush 56, Flamethrower 57, Draco Meteor 59, Perish Song 62, Ice Beam 65 | Altaria |
| Liepard | wild | 48 | Oxide | Sucker Punch, Nasty Plot, Night Slash, Snatch | Play Rough 54 | Liepard |
| Liepard | wild | 48 | Rewrite | Taunt, Sucker Punch, Night Slash, Snatch | Skitter Smack 50, Play Rough 54, BurningJealousy 56, Seed Bomb 58, Shadow Ball 60, U-turn 65 | Liepard |
| Octillery | super rod | 48 | Oxide | Bullet Seed, Wring Out, Signal Beam, Ice Beam | Hyper Beam 55 | Octillery |
| Octillery | super rod | 48 | Rewrite | Scald, Skitter Smack, Signal Beam, Ice Beam | Psychic 54, Hyper Beam 55, Swagger 61 | Octillery |
| Raichu | wild | 48 | Oxide | ThunderShock, Tail Whip, Quick Attack, Thunderbolt | nothing | Raichu |
| Raichu | wild | 48 | Rewrite | ThunderShock, Tail Whip, Quick Attack, Thunderbolt | ThunderPunch 54, Discharge 56, Play Rough 58, Surf 60, Volt Switch 62, Volt Tackle 65 | Raichu |
| Talonflame | wild | 48 | Oxide | Natural Gift, Acrobatics, Me First, Tailwind | Flare Blitz 51, Brave Bird 55 | Talonflame |
| Talonflame | wild | 48 | Rewrite | Steel Wing, Flamethrower, Tailwind, Upper Hand | Flare Blitz 51, Overheat 54, Brave Bird 55, Agility 57, U-turn 60, Bulk Up 65 | Talonflame |
| Tentacruel | super rod | 48 | Oxide | Barrier, Water Pulse, Poison Jab, Screech | Hydro Pump 49, Wring Out 55 | Tentacruel |
| Tentacruel | super rod | 48 | Rewrite | Aurora Beam, Sludge Bomb, Screech, Psybeam | Surf 49, Muddy Water 53, Throat Chop 54, Power Gem 56, Flip Turn 58, Ice Beam 60, Toxic 62, Skitter Smack 65 | Tentacruel |
| Toucannon | wild | 48 to 49 | Oxide | Screech, Drill Peck, Bullet Seed, FeatherDance | Hyper Voice 50 | Toucannon |
| Toucannon | wild | 48 to 49 | Rewrite | Bullet Seed, Throat Chop, FeatherDance, Take Down | Hyper Voice 50, Brick Break 54, Temper Flare 56, Rock Climb 60, Brave Bird 65 | Toucannon |
| Tsareena | wild | 48 to 49 | Oxide | Low Sweep, Aromatherapy, Leaf Storm, Power Whip | Hi Jump Kick 55 | Tsareena |
| Tsareena | wild | 48 to 49 | Rewrite | Aromatherapy, Zen Headbutt, Leaf Storm, Petal Blizzard | U-turn 51, Play Rough 54, Hi Jump Kick 55, Knock Off 60, Charm 65 | Tsareena |
| Arboliva | wild | 49 | Oxide | Seed Bomb, Energy Ball, Leech Seed, Terrain Pulse | Petal Blizzard 52, Petal Dance 58 | Arboliva |
| Arboliva | wild | 49 | Rewrite | Energy Ball, Leech Seed, Alluring Voice, Swift | Petal Blizzard 52, Hyper Voice 54, Pollen Puff 55, Petal Dance 58, Earth Power 60, Leaf Storm 65 | Arboliva |
| Lurantis | wild | 49 | Oxide | Sweet Scent, X-Scissor, Synthesis, Leaf Blade | Solar Blade 55 | Lurantis |
| Lurantis | wild | 49 | Rewrite | Leaf Blade, Low Sweep, Night Slash, Poison Jab | Skitter Smack 52, Leech Life 54, Solar Blade 55, Scary Face 61 | Lurantis |
| Floatzel | wild | 50 | Oxide | Crunch, Agility, Whirlpool, Razor Wind | nothing | Floatzel |
| Floatzel | wild | 50 | Rewrite | Waterfall, Whirlpool, Liquidation, Low Sweep | Agility 51, Rock Tomb 53, Ice Fang 56, Wave Crash 62, Ice Punch 65 | Floatzel |
| Gastrodon | wild | 50 | Oxide | Mud Bomb, Hidden Power, Body Slam, Muddy Water | Recover 54 | Gastrodon |
| Gastrodon | wild | 50 | Rewrite | Muddy Water, Bulldoze, Sludge Bomb, Ice Beam | Recover 54, Skitter Smack 56, Rock Tomb 60, Block 65 | Gastrodon |
| Crawdaunt | super rod | 51 | Oxide | Swift, Taunt, Night Slash, Crabhammer | Swords Dance 52, Crunch 57, Guillotine 65 | Crawdaunt |
| Crawdaunt | super rod | 51 | Rewrite | Night Slash, X-Scissor, Crabhammer, Brick Break | Swords Dance 52, Rock Tomb 54, Crunch 57, Swagger 61 | Crawdaunt |

## Stark Mountain

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 65 | At the cap |
|---|---|---|---|---|---|---|
| Galarian Weezing | wild | 51 to 54 | Oxide | Will-O-Wisp, Sludge Bomb, Pain Split, Strange Steam | Explosion 55 | Galarian Weezing |
| Galarian Weezing | wild | 51 to 54 | Rewrite | Will-O-Wisp, Sludge Bomb, Pain Split, Strange Steam | Poison Fang 54, Heat Wave 56, Thunderbolt 58, Shadow Ball 60, Double-Edge 62, Overheat 65 | Galarian Weezing |
| Houndoom | wild | 52 | Oxide | Fire Fang, Faint Attack, Embargo, Flamethrower | Crunch 54, Nasty Plot 60 | Houndoom |
| Houndoom | wild | 52 | Rewrite | Mud Shot, Embargo, Flamethrower, Dark Pulse | Crunch 54, Shadow Ball 56, BurningJealousy 58, Nasty Plot 60, Sludge Bomb 62, Overheat 65 | Houndoom |
| Magcargo | wild | 52 to 53 | Oxide | Amnesia, Lava Plume, Rock Slide, Body Slam | Flamethrower 61 | Magcargo |
| Magcargo | wild | 52 to 53 | Rewrite | Shell Smash, Scorching Sands, Rock Slide, Body Slam | BurningJealousy 54, Energy Ball 56, Yawn 57, Power Gem 58, Flamethrower 61, Overheat 63 | Magcargo |
| Magmortar | wild | 52 to 54 | Oxide | Confuse Ray, Fire Punch, Lava Plume, Flamethrower | Fire Blast 58 | Magmortar |
| Magmortar | wild | 52 to 54 | Rewrite | BurningJealousy, Lava Plume, Flamethrower, Milk Drink | Scorching Sands 53, Thunderbolt 54, Psychic 55, Overheat 58, Swagger 62 | Magmortar |
| Rhyperior | wild | 52 | Oxide | Horn Drill, Hammer Arm, Stone Edge, Earthquake | Megahorn 57, Rock Wrecker 61 | Rhyperior |
| Rhyperior | wild | 52 | Rewrite | Take Down, Hammer Arm, Rock Slide, Earthquake | Megahorn 57, Rock Wrecker 61, Crunch 65 | Rhyperior |
| Salazzle | wild | 52 to 53 | Oxide | Venoshock, Flamethrower, Sludge Bomb, Dragon Pulse | Fire Blast 55 | Salazzle |
| Salazzle | wild | 52 to 53 | Rewrite | Sludge Bomb, Encore, Swagger, Dragon Pulse | Nasty Plot 54, Overheat 61, Hyper Voice 65 | Salazzle |
| Turtonator | wild | 52 | Oxide | Body Slam, Flamethrower, Dragon Pulse, Fire Spin | Explosion 55, Overheat 61 | Turtonator |
| Turtonator | wild | 52 | Rewrite | Flamethrower, Dragon Pulse, Shell Smash, Fire Spin | Body Press 53, Earthquake 54, BurningJealousy 56, Flash Cannon 57, Rock Tomb 58, Overheat 61, Iron Defense 63 | Turtonator |
| Weezing | wild | 52 | Oxide | Haze, Double Hit, Explosion, Sludge Bomb | Destiny Bond 55, Memento 63 | Weezing |
| Weezing | wild | 52 | Rewrite | Sludge, Shadow Ball, Psybeam, Sludge Bomb | Strange Steam 53, Flamethrower 54, Poison Fang 56, Dark Pulse 58, Will-O-Wisp 60, Overheat 65 | Weezing |
| Ceruledge | wild | 53 | Oxide | Lava Plume, Swords Dance, Ally Switch, Bitter Blade | Psycho Cut 56, Flare Blitz 62 | Ceruledge |
| Ceruledge | wild | 53 | Rewrite | Lava Plume, Swords Dance, Bitter Blade, Throat Chop | Iron Head 54, Psycho Cut 56, Flare Blitz 62, Poltergeist 65 | Ceruledge |
| Larvesta | wild | 54 | Oxide | Struggle Bug, Flame Wheel, Bug Bite, Take Down | as Volcarona: Flamethrower 60, Bug Buzz 61, Whirlwind 64, Overheat 65 | Volcarona (from 59) |
| Larvesta | wild | 54 | Rewrite | Roost, Take Down, Poison Jab, Skitter Smack | Lunge 56; as Volcarona: Mystical Fire 59, Flamethrower 60, Bug Buzz 61, Rage Powder 62, Overheat 65 | Volcarona (from 59) |

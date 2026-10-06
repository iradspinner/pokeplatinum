# Byron's split: what each catch knows and learns

Written by `tools/oxide/balance/learncheck.py sheets` for check 6 of the learnset baseline (`docs/oxide/learnset-checks.md`). One table per capture area first offered in Byron's split, whose cap is 53. Each Pokemon is read at the lowest level it is found at there. "Knows at capture" is the last four moves its list gives by that level; "learns by level-up" is every entry it reaches after capture up to 53, evolving on time, with each later stage's moves under its name; "at the cap" is the stage it can be by then and the next one after. A row marked Rewrite shows the learnset rewrite's lists (the tree's) where it differs from the row marked Oxide, Oxide's lists before the learnset rewrite (`da6b92496c`); a row marked both is the same in each. Relearner-only moves and egg moves are left out.

## Canalave City

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 53 | At the cap |
|---|---|---|---|---|---|---|
| Remoraid | old rod | 14 | Oxide | Water Gun, Lock-On, Psybeam, Aurora Beam | BubbleBeam 19, Focus Energy 23; as Octillery: Octazooka 25, Bullet Seed 29, Wring Out 36, Signal Beam 42, Ice Beam 48 | Octillery (from 25) |
| Remoraid | old rod | 14 | Rewrite | Water Pulse, Psybeam, Screech, Aurora Beam | BubbleBeam 19, Focus Energy 23; as Octillery: Octazooka 25, Mud Shot 27, Bullet Seed 29, Round 33, Charge Beam 35, Scald 37, Skitter Smack 40, Signal Beam 42, Ice Beam 48 | Octillery (from 25) |
| Tentacool | old rod | 14 | Oxide | Poison Sting, Supersonic, Constrict, Acid | Toxic Spikes 15, BubbleBeam 19, Wrap 22, Barrier 26, Water Pulse 29; as Tentacruel: Poison Jab 36, Screech 42, Hydro Pump 49 | Tentacruel (from 30) |
| Tentacool | old rod | 14 | Rewrite | Poison Sting, Supersonic, Pounce, Acid | Toxic Spikes 15, Water Pulse 16, BubbleBeam 19, Barrier 26; as Tentacruel: Poison Jab 33, Aurora Beam 34, Sludge Bomb 39, Screech 42, Psybeam 44, Surf 49, Muddy Water 53 | Tentacruel (from 30) |
| Luvdisc | old rod | 15 to 16 | Oxide | Charm, Water Gun, Agility, Take Down | Lucky Chant 17, Attract 22, Sweet Kiss 27; as Alomomola: Soak 33, Wish 37, Brine 41, Safeguard 45, Whirlpool 49, Helping Hand 53 | Alomomola (from 30) |
| Luvdisc | old rod | 15 to 16 | Rewrite | Water Gun, Aqua Jet, Draining Kiss, Take Down | Lucky Chant 17, Agility 18, Icy Wind 20, Attract 22, Sweet Kiss 27; as Alomomola: Heal Pulse 30, Wake-Up Slap 31, Water Pulse 32, Soak 33, Play Rough 35, Wish 37, Brine 41, Zen Headbutt 43, Safeguard 45, Whirlpool 49, Helping Hand 53 | Alomomola (from 30) |
| Mantyke | old rod | 15 | Oxide | Bubble, Supersonic, BubbleBeam, Headbutt | Agility 19, Wing Attack 22, Water Pulse 28; as Mantine: Take Down 31, Confuse Ray 37, Bounce 40, Aqua Ring 46, Hydro Pump 49 | Mantine (from 30) |
| Mantyke | old rod | 15 | Rewrite | Tackle, Bubble, BubbleBeam, Headbutt | Agility 19, Wing Attack 22, Icy Wind 25, Water Pulse 28; as Mantine: Take Down 31, Scald 34, Confuse Ray 37, Bounce 40, Psybeam 41, Signal Beam 43, Aqua Ring 46, Surf 49 | Mantine (from 30) |
| Chinchou | good rod | 24 | Oxide | Water Gun, Confuse Ray, Spark, Take Down | as Lanturn: Stockpile 27, Swallow 27, Spit Up 27, BubbleBeam 30, Signal Beam 35, Discharge 40, Aqua Ring 47, Hydro Pump 52 | Lanturn (from 27) |
| Chinchou | good rod | 24 | Rewrite | Screech, Confuse Ray, Spark, Take Down | Icy Wind 26; as Lanturn: Stockpile 27, Swallow 28, Spit Up 29, BubbleBeam 30, Signal Beam 31, Scald 33, Surf 34, Thunderbolt 37, Discharge 40, Flash Cannon 43, Aqua Ring 47, Muddy Water 52 | Lanturn (from 27) |
| Finneon | good rod | 24 | Oxide | Water Gun, Attract, Gust, Water Pulse | Captivate 26, Safeguard 29; as Lumineon: Aqua Ring 35, Whirlpool 42, U-turn 48, Bounce 53 | Lumineon (from 31) |
| Finneon | good rod | 24 | Rewrite | Attract, Water Pulse, Pursuit, Gust | Captivate 26, Safeguard 29; as Lumineon: Flip Turn 31, Aqua Ring 33, Icy Wind 34, Aqua Tail 38, Signal Beam 40, Whirlpool 42, Ice Fang 45, U-turn 48, Bounce 53 | Lumineon (from 31) |
| Remoraid | good rod | 26 | Oxide | Psybeam, Aurora Beam, BubbleBeam, Focus Energy | Bullet Seed 27; as Octillery: Bullet Seed 29, Wring Out 36, Signal Beam 42, Ice Beam 48 | Octillery (from 27) |
| Remoraid | good rod | 26 | Rewrite | Screech, Aurora Beam, BubbleBeam, Focus Energy | as Octillery: Mud Shot 27, Bullet Seed 29, Round 33, Charge Beam 35, Scald 37, Skitter Smack 40, Signal Beam 42, Ice Beam 48 | Octillery (from 27) |
| Tentacool | good rod | 26 | Oxide | Toxic Spikes, BubbleBeam, Wrap, Barrier | Water Pulse 29; as Tentacruel: Poison Jab 36, Screech 42, Hydro Pump 49 | Tentacruel (from 30) |
| Tentacool | good rod | 26 | Rewrite | Toxic Spikes, Water Pulse, BubbleBeam, Barrier | as Tentacruel: Poison Jab 33, Aurora Beam 34, Sludge Bomb 39, Screech 42, Psybeam 44, Surf 49, Muddy Water 53 | Tentacruel (from 30) |
| Frogadier | good rod | 28 | Oxide | Icy Wind, Faint Attack, Acrobatics, Low Kick | Waterfall 30, Fling 35; as Greninja: Scald 37, Dark Pulse 40, Extrasensory 43, Sludge Wave 47, Gunk Shot 51 | Greninja (from 36) |
| Frogadier | good rod | 28 | Rewrite | Faint Attack, Acrobatics, Low Kick, Scald | Waterfall 30, Fling 35; as Greninja: Shadow Sneak 36, Scald 37, Dark Pulse 40, Extrasensory 43, Sludge Wave 47, Gunk Shot 51 | Greninja (from 36) |
| Mantine | surf | 30 | Oxide | Headbutt, Agility, Wing Attack, Water Pulse | Take Down 31, Confuse Ray 37, Bounce 40, Aqua Ring 46, Hydro Pump 49 | Mantine |
| Mantine | surf | 30 | Rewrite | Headbutt, Agility, Wing Attack, Water Pulse | Take Down 31, Scald 34, Confuse Ray 37, Bounce 40, Psybeam 41, Signal Beam 43, Aqua Ring 46, Surf 49 | Mantine |
| Tentacruel | surf | 30 | Oxide | BubbleBeam, Wrap, Barrier, Water Pulse | Poison Jab 36, Screech 42, Hydro Pump 49 | Tentacruel |
| Tentacruel | surf | 30 | Rewrite | Toxic Spikes, BubbleBeam, Barrier, Water Pulse | Poison Jab 33, Aurora Beam 34, Sludge Bomb 39, Screech 42, Psybeam 44, Surf 49, Muddy Water 53 | Tentacruel |
| Gastrodon | surf | 33 | Oxide | Water Pulse, Mud Bomb, Hidden Power, Body Slam | Muddy Water 41 | Gastrodon |
| Gastrodon | surf | 33 | Rewrite | Mud Bomb, Hidden Power, Body Slam, AncientPower | Earth Power 35, Clear Smog 37, Muddy Water 41, Bulldoze 44, Sludge Bomb 46, Ice Beam 49 | Gastrodon |
| Tentacool | surf | 33 | Oxide | Wrap, Barrier, Water Pulse, Poison Jab | as Tentacruel: Poison Jab 36, Screech 42, Hydro Pump 49 | Tentacruel (from 34) |
| Tentacool | surf | 33 | Rewrite | Water Pulse, BubbleBeam, Barrier, Poison Jab | as Tentacruel: Aurora Beam 34, Sludge Bomb 39, Screech 42, Psybeam 44, Surf 49, Muddy Water 53 | Tentacruel (from 34) |
| Frogadier | surf | 36 | Oxide | Acrobatics, Low Kick, Waterfall, Fling | as Greninja: Scald 37, Dark Pulse 40, Extrasensory 43, Sludge Wave 47, Gunk Shot 51 | Greninja (from 37) |
| Frogadier | surf | 36 | Rewrite | Low Kick, Scald, Waterfall, Fling | as Greninja: Scald 37, Dark Pulse 40, Extrasensory 43, Sludge Wave 47, Gunk Shot 51 | Greninja (from 37) |

## Celestic Town

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 53 | At the cap |
|---|---|---|---|---|---|---|
| Corphish | old rod | 14 | Oxide | Bubble, Harden, ViceGrip, Leer | BubbleBeam 20, Protect 23, Knock Off 26; as Crawdaunt: Swift 30, Taunt 34, Night Slash 39, Crabhammer 44, Swords Dance 52 | Crawdaunt (from 30) |
| Corphish | old rod | 14 | Rewrite | Taunt, ViceGrip, BubbleBeam, Leer | Razor Shell 17, Knock Off 26; as Crawdaunt: Swift 30, Taunt 32, Throat Chop 35, Aerial Ace 36, Night Slash 39, X-Scissor 41, Crabhammer 44, Brick Break 48, Swords Dance 52 | Crawdaunt (from 30) |
| Feebas | old rod | 14 | Oxide | Splash | Tackle 15, Flail 30; as Milotic: Hydro Pump 37, Attract 41, Safeguard 45, Aqua Ring 49 | Milotic (from 30) |
| Feebas | old rod | 14 | Rewrite | Whirlpool, Water Gun, Water Pulse | Tackle 15, Recover 21, Dragon Tail 24, Captivate 25, Flail 30; as Milotic: Twister 30, Recover 31, Aqua Tail 32, Aurora Beam 33, Dragon Pulse 35, Surf 37, Attract 41, Muddy Water 43, Safeguard 45, Aqua Ring 49 | Milotic (from 30) |
| Chinchou | old rod | 15 | Oxide | Supersonic, Thunder Wave, Flail, Water Gun | Confuse Ray 17, Spark 20, Take Down 23; as Lanturn: Stockpile 27, Swallow 27, Spit Up 27, BubbleBeam 30, Signal Beam 35, Discharge 40, Aqua Ring 47, Hydro Pump 52 | Lanturn (from 27) |
| Chinchou | old rod | 15 | Rewrite | Thunder Wave, Flail, Water Gun, Screech | Confuse Ray 17, Spark 20, Take Down 23, Icy Wind 26; as Lanturn: Stockpile 27, Swallow 28, Spit Up 29, BubbleBeam 30, Signal Beam 31, Scald 33, Surf 34, Thunderbolt 37, Discharge 40, Flash Cannon 43, Aqua Ring 47, Muddy Water 52 | Lanturn (from 27) |
| Luvdisc | old rod | 15 | Oxide | Charm, Water Gun, Agility, Take Down | Lucky Chant 17, Attract 22, Sweet Kiss 27; as Alomomola: Soak 33, Wish 37, Brine 41, Safeguard 45, Whirlpool 49, Helping Hand 53 | Alomomola (from 30) |
| Luvdisc | old rod | 15 | Rewrite | Water Gun, Aqua Jet, Draining Kiss, Take Down | Lucky Chant 17, Agility 18, Icy Wind 20, Attract 22, Sweet Kiss 27; as Alomomola: Heal Pulse 30, Wake-Up Slap 31, Water Pulse 32, Soak 33, Play Rough 35, Wish 37, Brine 41, Zen Headbutt 43, Safeguard 45, Whirlpool 49, Helping Hand 53 | Alomomola (from 30) |
| Frogadier | old rod | 16 | Oxide | Quick Attack, Lick, Water Pulse, Icy Wind | Faint Attack 20, Acrobatics 22, Low Kick 25, Waterfall 30, Fling 35; as Greninja: Scald 37, Dark Pulse 40, Extrasensory 43, Sludge Wave 47, Gunk Shot 51 | Greninja (from 36) |
| Frogadier | old rod | 16 | Rewrite | Quick Attack, Lick, Water Pulse, Icy Wind | Thief 19, Faint Attack 20, Acrobatics 22, Low Kick 25, Scald 27, Waterfall 30, Fling 35; as Greninja: Shadow Sneak 36, Scald 37, Dark Pulse 40, Extrasensory 43, Sludge Wave 47, Gunk Shot 51 | Greninja (from 36) |
| Barboach | good rod | 24 | Oxide | Water Gun, Mud Bomb, Amnesia, Water Pulse | Magnitude 26; as Whiscash: Rest 33, Snore 33, Aqua Tail 39, Earthquake 45, Future Sight 51 | Whiscash (from 30) |
| Barboach | good rod | 24 | Rewrite | Mud Bomb, Amnesia, Rock Tomb, Water Pulse | Magnitude 26; as Whiscash: Bulldoze 30, Rest 33, Zen Headbutt 36, Aqua Tail 39, Earth Power 40, Wild Charge 42, Earthquake 45, Future Sight 51 | Whiscash (from 30) |
| Goldeen | good rod | 24 | Oxide | Supersonic, Horn Attack, Water Pulse, Flail | Aqua Ring 27, Fury Attack 31; as Seaking: Waterfall 40, Horn Drill 47 | Seaking (from 33) |
| Goldeen | good rod | 24 | Rewrite | Water Pulse, Horn Attack, Swagger, Flail | Aqua Ring 27; as Seaking: Aqua Jet 34, Skull Bash 37, Waterfall 40, Poison Jab 44, Drill Run 47, Knock Off 50 | Seaking (from 33) |
| Corphish | good rod | 26 | Oxide | Leer, BubbleBeam, Protect, Knock Off | as Crawdaunt: Swift 30, Taunt 34, Night Slash 39, Crabhammer 44, Swords Dance 52 | Crawdaunt (from 30) |
| Corphish | good rod | 26 | Rewrite | BubbleBeam, Leer, Razor Shell, Knock Off | as Crawdaunt: Swift 30, Taunt 32, Throat Chop 35, Aerial Ace 36, Night Slash 39, X-Scissor 41, Crabhammer 44, Brick Break 48, Swords Dance 52 | Crawdaunt (from 30) |
| Feebas | good rod | 26 | Oxide | Splash, Tackle | Flail 30; as Milotic: Hydro Pump 37, Attract 41, Safeguard 45, Aqua Ring 49 | Milotic (from 30) |
| Feebas | good rod | 26 | Rewrite | Tackle, Recover, Dragon Tail, Captivate | Flail 30; as Milotic: Twister 30, Recover 31, Aqua Tail 32, Aurora Beam 33, Dragon Pulse 35, Surf 37, Attract 41, Muddy Water 43, Safeguard 45, Aqua Ring 49 | Milotic (from 30) |
| Croconaw | good rod | 28 | Oxide | Bite, Scary Face, Ice Fang, Flail | Crunch 30; as Feraligatr: Agility 30, Crunch 32, Slash 37, Screech 45, Thrash 50 | Feraligatr (from 30) |
| Croconaw | good rod | 28 | Rewrite | Bite, Scary Face, Ice Fang, Flail | as Feraligatr: Agility 30, Crunch 32, Slash 33, Bulldoze 35, Metal Claw 39, Aqua Jet 40, Liquidation 42, Screech 45, Thrash 50 | Feraligatr (from 30) |
| Floatzel | surf | 30 | Oxide | Swift, Aqua Jet, Crunch, Agility | Whirlpool 39, Razor Wind 50 | Floatzel |
| Floatzel | surf | 30 | Rewrite | Swift, Aqua Jet, Crunch, Icy Wind | Flip Turn 33, Waterfall 36, Whirlpool 39, Liquidation 41, Low Sweep 44, Agility 51, Rock Tomb 53 | Floatzel |
| Jellicent | surf | 30 | Oxide | Water Pulse, Imprison, Confuse Ray, Hex | Brine 34, Pain Split 39, Destiny Bond 45, Shadow Ball 51 | Jellicent |
| Jellicent | surf | 30 | Rewrite | Water Pulse, Imprison, Confuse Ray, Hex | Brine 34, Pain Split 39, Muddy Water 45, Shadow Ball 51 | Jellicent |
| Buizel | surf | 33 | Oxide | Pursuit, Swift, Aqua Jet, Agility | as Floatzel: Whirlpool 39, Razor Wind 50 | Floatzel (from 34) |
| Buizel | surf | 33 | Rewrite | Pursuit, Scary Face, Swift, Aqua Jet | as Floatzel: Waterfall 36, Whirlpool 39, Liquidation 41, Low Sweep 44, Agility 51, Rock Tomb 53 | Floatzel (from 34) |
| Frillish | surf | 33 to 36 | Oxide | Water Pulse, Imprison, Confuse Ray, Hex | Brine 34, Pain Split 39; as Jellicent: Destiny Bond 45, Shadow Ball 51 | Jellicent (from 40) |
| Frillish | surf | 33 to 36 | Rewrite | Water Pulse, Imprison, Confuse Ray, Hex | Brine 34, Dark Pulse 36, Pain Split 39; as Jellicent: Muddy Water 45, Shadow Ball 51 | Jellicent (from 40) |

## Eterna City

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 53 | At the cap |
|---|---|---|---|---|---|---|
| Masquerain | surf | 22 | Oxide | Quick Attack, Sweet Scent, Water Sport, Gust | Scary Face 26, Stun Spore 33, Silver Wind 40, Air Slash 47 | Masquerain |
| Masquerain | surf | 22 | Rewrite | Bubble, Quick Attack, Water Sport, Gust | BubbleBeam 25, Scary Face 26, Mud Bomb 29, Stun Spore 33, Surf 36, Giga Drain 38, Silver Wind 40, Signal Beam 41, Icy Wind 43, Air Slash 47, Lunge 53 | Masquerain |
| Shellos | surf | 22 | Oxide | Harden, Water Pulse, Mud Bomb, Hidden Power | Body Slam 29; as Gastrodon: Muddy Water 41 | Gastrodon (from 30) |
| Shellos | surf | 22 | Rewrite | Water Pulse, Mud Bomb, Hidden Power, Swagger | Body Slam 29; as Gastrodon: AncientPower 33, Earth Power 35, Clear Smog 37, Muddy Water 41, Bulldoze 44, Sludge Bomb 46, Ice Beam 49 | Gastrodon (from 30) |
| Corphish | surf | 25 | Oxide | ViceGrip, Leer, BubbleBeam, Protect | Knock Off 26; as Crawdaunt: Swift 30, Taunt 34, Night Slash 39, Crabhammer 44, Swords Dance 52 | Crawdaunt (from 30) |
| Corphish | surf | 25 | Rewrite | ViceGrip, BubbleBeam, Leer, Razor Shell | Knock Off 26; as Crawdaunt: Swift 30, Taunt 32, Throat Chop 35, Aerial Ace 36, Night Slash 39, X-Scissor 41, Crabhammer 44, Brick Break 48, Swords Dance 52 | Crawdaunt (from 30) |
| Goldeen | surf | 25 | Oxide | Supersonic, Horn Attack, Water Pulse, Flail | Aqua Ring 27, Fury Attack 31; as Seaking: Waterfall 40, Horn Drill 47 | Seaking (from 33) |
| Goldeen | surf | 25 | Rewrite | Water Pulse, Horn Attack, Swagger, Flail | Aqua Ring 27; as Seaking: Aqua Jet 34, Skull Bash 37, Waterfall 40, Poison Jab 44, Drill Run 47, Knock Off 50 | Seaking (from 33) |
| Psyduck | surf | 28 | Oxide | Disable, Confusion, Water Pulse, Fury Swipes | Screech 31; as Golduck: Psych Up 37, Zen Headbutt 44, Amnesia 50 | Golduck (from 33) |
| Psyduck | surf | 28 | Rewrite | Disable, Confusion, Low Sweep, Fury Swipes | as Golduck: Surf 34, Psych Up 37, Aurora Beam 40, Zen Headbutt 44, Power Gem 47, Amnesia 50 | Golduck (from 33) |

## Fuego Ironworks

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 53 | At the cap |
|---|---|---|---|---|---|---|
| Barboach | old rod | 14 | Oxide | Mud Sport, Water Sport, Water Gun, Mud Bomb | Amnesia 18, Water Pulse 22, Magnitude 26; as Whiscash: Rest 33, Snore 33, Aqua Tail 39, Earthquake 45, Future Sight 51 | Whiscash (from 30) |
| Barboach | old rod | 14 | Rewrite | Scary Face, Water Sport, Water Gun, Mud Bomb | Amnesia 18, Rock Tomb 20, Water Pulse 22, Magnitude 26; as Whiscash: Bulldoze 30, Rest 33, Zen Headbutt 36, Aqua Tail 39, Earth Power 40, Wild Charge 42, Earthquake 45, Future Sight 51 | Whiscash (from 30) |
| Goldeen | old rod | 14 | Oxide | Tail Whip, Water Sport, Supersonic, Horn Attack | Water Pulse 17, Flail 21, Aqua Ring 27, Fury Attack 31; as Seaking: Waterfall 40, Horn Drill 47 | Seaking (from 33) |
| Goldeen | old rod | 14 | Rewrite | Water Sport, Flip Turn, Water Pulse, Horn Attack | Swagger 17, Flail 21, Aqua Ring 27; as Seaking: Aqua Jet 34, Skull Bash 37, Waterfall 40, Poison Jab 44, Drill Run 47, Knock Off 50 | Seaking (from 33) |
| Corphish | old rod | 15 | Oxide | Bubble, Harden, ViceGrip, Leer | BubbleBeam 20, Protect 23, Knock Off 26; as Crawdaunt: Swift 30, Taunt 34, Night Slash 39, Crabhammer 44, Swords Dance 52 | Crawdaunt (from 30) |
| Corphish | old rod | 15 | Rewrite | Taunt, ViceGrip, BubbleBeam, Leer | Razor Shell 17, Knock Off 26; as Crawdaunt: Swift 30, Taunt 32, Throat Chop 35, Aerial Ace 36, Night Slash 39, X-Scissor 41, Crabhammer 44, Brick Break 48, Swords Dance 52 | Crawdaunt (from 30) |
| Krabby | old rod | 15 | Oxide | ViceGrip, Leer, Harden, BubbleBeam | Mud Shot 19, Metal Claw 21, Stomp 25; as Kingler: Protect 32, Guillotine 37, Slam 44, Brine 51 | Kingler (from 28) |
| Krabby | old rod | 15 | Rewrite | ViceGrip, Leer, Wide Guard, BubbleBeam | Mud Shot 19, Metal Claw 21, Stomp 25; as Kingler: Waterfall 34, Razor Shell 36, Rock Tomb 39, X-Scissor 41, Slam 44, Night Slash 47, Brine 51 | Kingler (from 28) |
| Frogadier | old rod | 16 | Oxide | Quick Attack, Lick, Water Pulse, Icy Wind | Faint Attack 20, Acrobatics 22, Low Kick 25, Waterfall 30, Fling 35; as Greninja: Scald 37, Dark Pulse 40, Extrasensory 43, Sludge Wave 47, Gunk Shot 51 | Greninja (from 36) |
| Frogadier | old rod | 16 | Rewrite | Quick Attack, Lick, Water Pulse, Icy Wind | Thief 19, Faint Attack 20, Acrobatics 22, Low Kick 25, Scald 27, Waterfall 30, Fling 35; as Greninja: Shadow Sneak 36, Scald 37, Dark Pulse 40, Extrasensory 43, Sludge Wave 47, Gunk Shot 51 | Greninja (from 36) |
| Goldeen | good rod | 24 | Oxide | Supersonic, Horn Attack, Water Pulse, Flail | Aqua Ring 27, Fury Attack 31; as Seaking: Waterfall 40, Horn Drill 47 | Seaking (from 33) |
| Goldeen | good rod | 24 | Rewrite | Water Pulse, Horn Attack, Swagger, Flail | Aqua Ring 27; as Seaking: Aqua Jet 34, Skull Bash 37, Waterfall 40, Poison Jab 44, Drill Run 47, Knock Off 50 | Seaking (from 33) |
| Shellos | good rod | 24 | Oxide | Harden, Water Pulse, Mud Bomb, Hidden Power | Body Slam 29; as Gastrodon: Muddy Water 41 | Gastrodon (from 30) |
| Shellos | good rod | 24 | Rewrite | Water Pulse, Mud Bomb, Hidden Power, Swagger | Body Slam 29; as Gastrodon: AncientPower 33, Earth Power 35, Clear Smog 37, Muddy Water 41, Bulldoze 44, Sludge Bomb 46, Ice Beam 49 | Gastrodon (from 30) |
| Barboach | good rod | 26 | Oxide | Mud Bomb, Amnesia, Water Pulse, Magnitude | as Whiscash: Rest 33, Snore 33, Aqua Tail 39, Earthquake 45, Future Sight 51 | Whiscash (from 30) |
| Barboach | good rod | 26 | Rewrite | Amnesia, Rock Tomb, Water Pulse, Magnitude | as Whiscash: Bulldoze 30, Rest 33, Zen Headbutt 36, Aqua Tail 39, Earth Power 40, Wild Charge 42, Earthquake 45, Future Sight 51 | Whiscash (from 30) |
| Corphish | good rod | 26 | Oxide | Leer, BubbleBeam, Protect, Knock Off | as Crawdaunt: Swift 30, Taunt 34, Night Slash 39, Crabhammer 44, Swords Dance 52 | Crawdaunt (from 30) |
| Corphish | good rod | 26 | Rewrite | BubbleBeam, Leer, Razor Shell, Knock Off | as Crawdaunt: Swift 30, Taunt 32, Throat Chop 35, Aerial Ace 36, Night Slash 39, X-Scissor 41, Crabhammer 44, Brick Break 48, Swords Dance 52 | Crawdaunt (from 30) |
| Magby | wild | 28 | Oxide | Faint Attack, Fire Spin, Confuse Ray, Fire Punch | as Magmortar: Lava Plume 37, Flamethrower 43 | Magmortar (from 30) |
| Magby | wild | 28 | Rewrite | Faint Attack, Fire Spin, Confuse Ray, Fire Punch | as Magmortar: BurningJealousy 33, Lava Plume 37, Flamethrower 43, Milk Drink 48, Scorching Sands 53 | Magmortar (from 30) |
| Qwilfish | good rod | 28 | Oxide | Rollout, Toxic Spikes, Stockpile, Spit Up | Revenge 29, Brine 33, Pin Missile 37, Take Down 41, Aqua Tail 45, Poison Jab 49, Destiny Bond 53 | Qwilfish |
| Qwilfish | good rod | 28 | Rewrite | Rollout, Toxic Spikes, Spit Up, Stockpile | Revenge 29, Brine 33, Pin Missile 37, Take Down 41, Throat Chop 43, Aqua Tail 45, Poison Jab 49 | Qwilfish |
| Charcadet | wild | 29 | Oxide | Clear Smog, Fire Spin, Will-O-Wisp | as Armarouge: Lava Plume 32, Calm Mind 37, Ally Switch 42, Flamethrower 48 | Armarouge (from 29) |
| Charcadet | wild | 29 | Oxide | Clear Smog, Fire Spin, Will-O-Wisp | as Ceruledge: Lava Plume 32, Swords Dance 37, Ally Switch 42, Bitter Blade 48 | Ceruledge (from 29) |
| Charcadet | wild | 29 | Rewrite | Clear Smog, Fire Spin, Will-O-Wisp, Flame Charge | as Armarouge: Clear Smog 29, Fire Spin 30, Lava Plume 32, Calm Mind 37, Flamethrower 48, Psyshock 52 | Armarouge (from 29) |
| Charcadet | wild | 29 | Rewrite | Clear Smog, Fire Spin, Will-O-Wisp, Flame Charge | as Ceruledge: Bulldoze 29, Shadow Claw 30, Lava Plume 32, Swords Dance 40, Bitter Blade 48, Throat Chop 52 | Ceruledge (from 29) |
| Houndoom | wild | 29 | Oxide | Smog, Roar, Bite, Odor Sleuth | Fire Fang 32, Faint Attack 38, Embargo 44, Flamethrower 48 | Houndoom |
| Houndoom | wild | 29 | Rewrite | Smog, Roar, Bite, Odor Sleuth | Fire Fang 32, Fire Pledge 35, Faint Attack 38, Mud Shot 41, Embargo 44, Flamethrower 48, Dark Pulse 51 | Houndoom |
| Larvesta | wild | 29 | Oxide | Ember, String Shot, Flame Charge, Struggle Bug | Flame Wheel 30, Bug Bite 40, Take Down 50 | Larvesta; Volcarona in HQ |
| Larvesta | wild | 29 | Rewrite | String Shot, Flame Charge, Struggle Bug, U-turn | Flame Wheel 30, Bug Bite 40, Fire Spin 41, Roost 45, Take Down 50, Poison Jab 53 | Larvesta; Volcarona in HQ |
| Litwick | wild | 29 | Oxide | Night Shade, Clear Smog, Will-O-Wisp, Flame Burst | Hex 30, Imprison 35, Memento 40; as Chandelure: Mystical Fire 46 | Chandelure (from 41) |
| Litwick | wild | 29 | Rewrite | Night Shade, Clear Smog, Will-O-Wisp, Flame Burst | Hex 30, Imprison 35, Shadow Ball 36; as Chandelure: Mystical Fire 46 | Chandelure (from 41) |
| Magnemite | wild | 29 | Oxide | SonicBoom, Thunder Wave, Spark, Lock-On | Magnet Bomb 30; as Magneton: Magnet Bomb 30; as Magnezone: Screech 34, Discharge 40, Mirror Shot 46, Magnet Rise 50 | Magnezone (from 32) |
| Magnemite | wild | 29 | Rewrite | SonicBoom, Thunder Wave, Spark, Lock-On | Magnet Bomb 30; as Magneton: Magnet Bomb 30; as Magnezone: Screech 34, Discharge 40, Mirror Shot 46, Signal Beam 48, Magnet Rise 50 | Magnezone (from 32) |
| Ponyta | wild | 29 | Oxide | Flame Wheel, Stomp, Fire Spin, Take Down | Agility 33, Fire Blast 37; as Rapidash: Fury Attack 40, Bounce 47 | Rapidash (from 40) |
| Ponyta | wild | 29 | Oxide | Flame Wheel, Stomp, Fire Spin, Take Down | as Galarian Rapidash: Stomp 30, Heal Pulse 35, Take Down 43, Dazzling Gleam 49 | Galarian Rapidash (from 29) |
| Ponyta | wild | 29 | Rewrite | Stomp, Bulldoze, Fire Spin, Take Down | Agility 33, Blaze Kick 35, Heat Wave 37; as Rapidash: Overheat 45, Bounce 47, Psychic 51 | Rapidash (from 40) |
| Ponyta | wild | 29 | Rewrite | Stomp, Bulldoze, Fire Spin, Take Down | as Galarian Rapidash: Stomp 30, Heal Pulse 35, Overheat 40, Take Down 43, Drill Run 46, Dazzling Gleam 49 | Galarian Rapidash (from 29) |
| Vulpix | wild | 29 | Oxide | Confuse Ray, Imprison, Flamethrower, Safeguard | as Ninetales: Flare Blitz 40 | Ninetales (from 29) |
| Vulpix | wild | 29 | Rewrite | Confuse Ray, Imprison, Flamethrower, Safeguard | as Ninetales: Dazzling Gleam 34, Flare Blitz 40 | Ninetales (from 29) |
| Braixen | wild | 30 | Oxide | Psybeam, Lucky Chant, Light Screen, Flame Burst | Psyshock 34; as Delphox: Mystical Fire 36, Hypnosis 40, Will-O-Wisp 45, Flamethrower 51 | Delphox (from 36) |
| Braixen | wild | 30 | Rewrite | Charm, Lucky Chant, Light Screen, Mystical Fire | Psyshock 34; as Delphox: Mystical Fire 36, Hypnosis 39, Mud Shot 41, Shadow Ball 42, Will-O-Wisp 45, Flamethrower 51 | Delphox (from 36) |
| Quagsire | surf | 30 | Oxide | Mud Shot, Slam, Mud Bomb, Amnesia | Yawn 31, Earthquake 36, Mist 48, Haze 48, Muddy Water 53 | Quagsire |
| Quagsire | surf | 30 | Rewrite | Slam, Mud Bomb, Amnesia, Trailblaze | Yawn 31, Earthquake 36, Rock Slide 39, Toxic 40, Drain Punch 44, Mist 48, Muddy Water 53 | Quagsire |
| Rhyhorn | wild | 30 | Oxide | Stomp, Fury Attack, Scary Face, Rock Blast | Take Down 33, Horn Drill 37; as Rhydon: Hammer Arm 42; as Rhyperior: Hammer Arm 42, Stone Edge 45, Earthquake 49 | Rhyperior (from 42) |
| Rhyhorn | wild | 30 | Rewrite | Bite, Scary Face, Rock Blast, Rock Slide | Take Down 33, Body Press 36, Poison Jab 39; as Rhydon: Hammer Arm 42; as Rhyperior: Hammer Arm 42, Stone Edge 45, Earthquake 49 | Rhyperior (from 42) |
| Salazzle | wild | 30 | Oxide | Flame Burst, Dragon Rage, Toxic, Venoshock | Flamethrower 36, Sludge Bomb 42, Dragon Pulse 50 | Salazzle |
| Salazzle | wild | 30 | Rewrite | Flame Burst, Dragon Rage, Toxic, Venoshock | Flamethrower 36, BurningJealousy 39, Sludge Bomb 42, Encore 44, Swagger 47, Dragon Pulse 50 | Salazzle |
| Shellos | surf | 30 | Oxide | Water Pulse, Mud Bomb, Hidden Power, Body Slam | as Gastrodon: Muddy Water 41 | Gastrodon (from 31) |
| Shellos | surf | 30 | Rewrite | Mud Bomb, Hidden Power, Swagger, Body Slam | as Gastrodon: AncientPower 33, Earth Power 35, Clear Smog 37, Muddy Water 41, Bulldoze 44, Sludge Bomb 46, Ice Beam 49 | Gastrodon (from 31) |
| Slugma | wild | 30 | Oxide | Rock Throw, Harden, Recover, AncientPower | Amnesia 31, Lava Plume 38; as Magcargo: Lava Plume 40, Rock Slide 45, Body Slam 52 | Magcargo (from 38) |
| Slugma | wild | 30 | Rewrite | Rock Throw, Harden, Recover, AncientPower | Amnesia 31, Lava Plume 38; as Magcargo: Lava Plume 40, Shell Smash 41, Scorching Sands 42, Rock Slide 45, Body Slam 52 | Magcargo (from 38) |
| Ceruledge | wild | 31 | Oxide | Will-O-Wisp, Night Shade, Flame Charge, Incinerate | Lava Plume 32, Swords Dance 37, Ally Switch 42, Bitter Blade 48 | Ceruledge |
| Ceruledge | wild | 31 | Rewrite | Iron Defense, Incinerate, Bulldoze, Shadow Claw | Lava Plume 32, Swords Dance 40, Bitter Blade 48, Throat Chop 52 | Ceruledge |
| Machoke | wild | 31 | Oxide | Foresight, Seismic Toss, Revenge, Vital Throw | Submission 32, Wake-Up Slap 36, Cross Chop 40; as Machamp: Cross Chop 40, Scary Face 44, DynamicPunch 51 | Machamp (from 40) |
| Machoke | wild | 31 | Rewrite | Seismic Toss, Revenge, Vital Throw, Bulldoze | Throat Chop 34, Wake-Up Slap 36, Close Combat 40; as Machamp: Close Combat 40, Scary Face 44, Low Sweep 48, Rock Slide 53 | Machamp (from 40) |
| Turtonator | wild | 31 | Oxide | Endure, Incinerate, Dragon Tail, Rapid Spin | Body Slam 33, Flamethrower 38, Dragon Pulse 43, Fire Spin 47 | Turtonator |
| Turtonator | wild | 31 | Rewrite | Endure, Incinerate, Dragon Tail, Rapid Spin | Body Slam 33, Flamethrower 38, Dragon Pulse 43, Shell Smash 45, Fire Spin 47, Body Press 53 | Turtonator |
| Ludicolo | surf | 33 | Oxide | Astonish, Growl, Mega Drain, Nature Power | nothing | Ludicolo |
| Ludicolo | surf | 33 | Rewrite | Astonish, Growl, Mega Drain, Nature Power | Energy Ball 34 | Ludicolo |
| Masquerain | surf | 33 | Oxide | Water Sport, Gust, Scary Face, Stun Spore | Silver Wind 40, Air Slash 47 | Masquerain |
| Masquerain | surf | 33 | Rewrite | BubbleBeam, Scary Face, Mud Bomb, Stun Spore | Surf 36, Giga Drain 38, Silver Wind 40, Signal Beam 41, Icy Wind 43, Air Slash 47, Lunge 53 | Masquerain |
| Relicanth | surf | 36 | Oxide | Rock Tomb, Yawn, Take Down, Mud Sport | AncientPower 43, Double-Edge 50 | Relicanth |
| Relicanth | surf | 36 | Rewrite | Water Gun, Rock Tomb, Yawn, Take Down | AncientPower 43, Bulldoze 46, Double-Edge 50 | Relicanth |

## Great Marsh

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 53 | At the cap |
|---|---|---|---|---|---|---|
| Araquanid | surf | 28 to 31 | Oxide | Aqua Ring, BubbleBeam, Bug Bite, Headbutt | Soak 31, Dive 36, Lunge 41, Scald 48, Hydro Pump 51 | Araquanid |
| Araquanid | surf | 28 to 31 | Rewrite | BubbleBeam, Bug Bite, Headbutt, Spider Web | Soak 31, Skitter Smack 34, Dive 36, Waterfall 38, Lunge 41, Poison Jab 44, Scald 48, Surf 51 | Araquanid |
| Dewpider | surf | 28 | Oxide | Aqua Ring, BubbleBeam, Bug Bite, Headbutt | Soak 29; as Araquanid: Soak 31, Dive 36, Lunge 41, Scald 48, Hydro Pump 51 | Araquanid (from 29) |
| Dewpider | surf | 28 | Rewrite | Aqua Ring, BubbleBeam, Sticky Web, Bug Bite | as Araquanid: Soak 31, Skitter Smack 34, Dive 36, Waterfall 38, Lunge 41, Poison Jab 44, Scald 48, Surf 51 | Araquanid (from 29) |
| Frillish | surf | 28 to 31 | Oxide | Ominous Wind, Water Pulse, Imprison, Confuse Ray | Hex 30, Brine 34, Pain Split 39; as Jellicent: Destiny Bond 45, Shadow Ball 51 | Jellicent (from 40) |
| Frillish | surf | 28 to 31 | Rewrite | Ominous Wind, Water Pulse, Imprison, Confuse Ray | Hex 30, Brine 34, Dark Pulse 36, Pain Split 39; as Jellicent: Muddy Water 45, Shadow Ball 51 | Jellicent (from 40) |
| Lombre | surf | 28 to 31 | Oxide | Fake Out, Fury Swipes, Water Sport, BubbleBeam | nothing | Ludicolo (from 28) |
| Lombre | surf | 28 to 31 | Rewrite | Water Sport, Swagger, BubbleBeam, Giga Drain | as Ludicolo: Energy Ball 34 | Ludicolo (from 28) |
| Lotad | surf | 28 | Oxide | Mist, Natural Gift, Mega Drain, BubbleBeam | nothing | Ludicolo (from 29) |
| Lotad | surf | 28 | Rewrite | Mist, Disarming Voice, Mega Drain, BubbleBeam | as Ludicolo: Energy Ball 34 | Ludicolo (from 29) |
| Masquerain | surf | 28 to 31 | Oxide | Sweet Scent, Water Sport, Gust, Scary Face | Stun Spore 33, Silver Wind 40, Air Slash 47 | Masquerain |
| Masquerain | surf | 28 to 31 | Rewrite | Water Sport, Gust, BubbleBeam, Scary Face | Mud Bomb 29, Stun Spore 33, Surf 36, Giga Drain 38, Silver Wind 40, Signal Beam 41, Icy Wind 43, Air Slash 47, Lunge 53 | Masquerain |
| Quagsire | surf | 28 to 31 | Oxide | Mud Shot, Slam, Mud Bomb, Amnesia | Yawn 31, Earthquake 36, Mist 48, Haze 48, Muddy Water 53 | Quagsire |
| Quagsire | surf | 28 to 31 | Rewrite | Slam, Mud Bomb, Amnesia, Trailblaze | Yawn 31, Earthquake 36, Rock Slide 39, Toxic 40, Drain Punch 44, Mist 48, Muddy Water 53 | Quagsire |
| Wooper | surf | 28 to 31 | Oxide | Mud Shot, Slam, Mud Bomb, Amnesia | Yawn 29; as Quagsire: Yawn 31, Earthquake 36, Mist 48, Haze 48, Muddy Water 53 | Quagsire (from 29) |
| Wooper | surf | 28 to 31 | Oxide | Mud Shot, Slam, Mud Bomb, Amnesia | as Clodsire: Poison Jab 30, Megahorn 36, Toxic 40, Earthquake 48 | Clodsire (from 28) |
| Wooper | surf | 28 to 31 | Rewrite | Poison Sting, Mud Shot, Slam, Mud Bomb | as Quagsire: Yawn 31, Earthquake 36, Rock Slide 39, Toxic 40, Drain Punch 44, Mist 48, Muddy Water 53 | Quagsire (from 29) |
| Wooper | surf | 28 to 31 | Rewrite | Poison Sting, Mud Shot, Slam, Mud Bomb | as Clodsire: Poison Jab 30, Waterfall 34, Megahorn 36, Toxic 40, Drain Punch 44, Earthquake 48, Aqua Tail 51 | Clodsire (from 28) |
| Slowpoke | surf | 31 | Oxide | Confusion, Disable, Headbutt, Water Pulse | Zen Headbutt 34; as Slowbro: Withdraw 37, Slack Off 41, Amnesia 47 | Slowbro (from 37) |
| Slowpoke | surf | 31 | Oxide | Confusion, Disable, Headbutt, Water Pulse | as Slowking: Zen Headbutt 34, Nasty Plot 39, Swagger 43, Psychic 48, Trump Card 53 | Slowking (from 31) |
| Slowpoke | surf | 31 | Rewrite | Confusion, Disable, Headbutt, Water Pulse | Zen Headbutt 34, Bulldoze 36; as Slowbro: Withdraw 37, Aurora Beam 38, Slack Off 39, Muddy Water 40, Surf 44, Amnesia 47, Power Gem 50 | Slowbro (from 37) |
| Slowpoke | surf | 31 | Rewrite | Confusion, Disable, Headbutt, Water Pulse | as Slowking: Zen Headbutt 34, Nasty Plot 39, Power Gem 41, Swagger 43, Psychic 48, Trump Card 53 | Slowking (from 31) |
| Feraligatr | surf | 34 | Oxide | Ice Fang, Flail, Agility, Crunch | Slash 37, Screech 45, Thrash 50 | Feraligatr |
| Feraligatr | surf | 34 | Rewrite | Flail, Agility, Crunch, Slash | Bulldoze 35, Metal Claw 39, Aqua Jet 40, Liquidation 42, Screech 45, Thrash 50 | Feraligatr |
| Frogadier | surf | 34 | Oxide | Faint Attack, Acrobatics, Low Kick, Waterfall | Fling 35; as Greninja: Scald 37, Dark Pulse 40, Extrasensory 43, Sludge Wave 47, Gunk Shot 51 | Greninja (from 36) |
| Frogadier | surf | 34 | Rewrite | Acrobatics, Low Kick, Scald, Waterfall | Fling 35; as Greninja: Shadow Sneak 36, Scald 37, Dark Pulse 40, Extrasensory 43, Sludge Wave 47, Gunk Shot 51 | Greninja (from 36) |
| Kingdra | surf | 34 | Oxide | BubbleBeam, Agility, Twister, Brine | Hydro Pump 40, Dragon Dance 48 | Kingdra |
| Kingdra | surf | 34 | Rewrite | BubbleBeam, Agility, Twister, Brine | Muddy Water 40, Aurora Beam 44 | Kingdra |
| Poliwrath | surf | 34 | Oxide | BubbleBeam, Hypnosis, DoubleSlap, Submission | DynamicPunch 43, Mind Reader 53 | Poliwrath |
| Poliwrath | surf | 34 | Rewrite | BubbleBeam, Hypnosis, DoubleSlap, Liquidation | Brick Break 43, Mind Reader 53 | Poliwrath |
| Relicanth | surf | 34 | Oxide | Water Gun, Rock Tomb, Yawn, Take Down | Mud Sport 36, AncientPower 43, Double-Edge 50 | Relicanth |
| Relicanth | surf | 34 | Rewrite | Water Gun, Rock Tomb, Yawn, Take Down | AncientPower 43, Bulldoze 46, Double-Edge 50 | Relicanth |

## Iron Island

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 53 | At the cap |
|---|---|---|---|---|---|---|
| Croagunk | egg gift | 1 | Oxide | Astonish | Mud-Slap 3, Poison Sting 8, Taunt 10, Pursuit 15, Faint Attack 17, Revenge 22, Swagger 24, Mud Bomb 29, Sucker Punch 31, Nasty Plot 36; as Toxicroak: Poison Jab 41, Sludge Bomb 49 | Toxicroak (from 37) |
| Croagunk | egg gift | 1 | Rewrite | Astonish | Mud-Slap 3, Poison Sting 8, Taunt 10, Pursuit 15, Faint Attack 17, Revenge 22, Swagger 24, Mud Bomb 29, Sucker Punch 31; as Toxicroak: Poison Jab 38, Nasty Plot 40, Low Sweep 44, X-Scissor 46, Sludge Bomb 49 | Toxicroak (from 37) |
| Gligar | egg gift | 1 | Oxide | Poison Sting | as Gliscor: Sand-Attack 5, Harden 9, Knock Off 12, Quick Attack 16, Fury Cutter 20, Faint Attack 23, Screech 27, Night Slash 31, Swords Dance 34, U-turn 38, X-Scissor 42, Guillotine 45 | Gliscor (from 1) |
| Gligar | egg gift | 1 | Rewrite | Poison Sting | as Gliscor: Sand-Attack 5, Harden 9, Knock Off 12, Quick Attack 16, Fury Cutter 20, Faint Attack 23, Screech 27, Night Slash 31, Swords Dance 34, U-turn 38, X-Scissor 42 | Gliscor (from 1) |
| Hippopotas | egg gift | 1 | Oxide | Tackle, Sand-Attack | Bite 7, Yawn 13, Take Down 19, Sand Tomb 25, Crunch 31; as Hippowdon: Earthquake 40, Double-Edge 50 | Hippowdon (from 34) |
| Hippopotas | egg gift | 1 | Rewrite | Tackle, Sand-Attack | Bite 7, Yawn 13, Take Down 19, Sand Tomb 25, Bulldoze 28, Crunch 31; as Hippowdon: Earthquake 37, Iron Head 42, Rock Tomb 44, Double-Edge 50, Slack Off 52 | Hippowdon (from 34) |
| Houndour | egg gift | 1 | Oxide | Leer, Ember | Howl 4, Smog 9, Roar 14, Bite 17, Odor Sleuth 22; as Houndoom: Fire Fang 32, Faint Attack 38, Embargo 44, Flamethrower 48 | Houndoom (from 27) |
| Houndour | egg gift | 1 | Rewrite | Ember | Howl 4, Scary Face 7, Smog 9, Roar 14, Bite 16, Incinerate 20, Odor Sleuth 22; as Houndoom: Fire Fang 32, Fire Pledge 35, Faint Attack 38, Mud Shot 41, Embargo 44, Flamethrower 48, Dark Pulse 51 | Houndoom (from 27) |
| Ralts | egg gift | 1 | Oxide | Growl | Confusion 6, Double Team 10, Teleport 12, Lucky Chant 17; as Kirlia: Magical Leaf 22, Calm Mind 25; as Gardevoir: Psychic 33, Imprison 40, Future Sight 45, Captivate 53 | Gardevoir (from 30) |
| Ralts | egg gift | 1 | Oxide | Growl | Confusion 6, Double Team 10, Teleport 12, Lucky Chant 17; as Gallade: Slash 22, Swords Dance 25, Psycho Cut 31, Helping Hand 36, Feint 39, False Swipe 45, Protect 50, Close Combat 53 | Gallade (from 20) |
| Ralts | egg gift | 1 | Rewrite | Growl, Draining Kiss | Confusion 6, Lucky Chant 17, Magical Leaf 19, Dazzling Gleam 20; as Kirlia: Calm Mind 25; as Gardevoir: Wish 30, Psychic 33, Icy Wind 36, Charge Beam 38, Imprison 40, Mystical Fire 42, Future Sight 45, Captivate 53 | Gardevoir (from 30) |
| Ralts | egg gift | 1 | Rewrite | Growl, Draining Kiss | Confusion 6, Lucky Chant 17, Magical Leaf 19, Dazzling Gleam 20; as Gallade: Slash 22, Swords Dance 25, Psycho Cut 31, Helping Hand 36, False Swipe 45, Close Combat 53 | Gallade (from 20) |
| Riolu | egg gift | 1 | Oxide | Quick Attack, Foresight, Endure | Counter 6, Force Palm 11, Feint 15, Reversal 19, Screech 24; as Lucario: Me First 29, Swords Dance 33, Aura Sphere 37, Close Combat 42, Dragon Pulse 47, ExtremeSpeed 51 | Lucario (from 28) |
| Riolu | egg gift | 1 | Rewrite | Quick Attack, Foresight, Endure | Crunch 2, Counter 6, Force Palm 11, Reversal 19, Screech 24; as Lucario: Swords Dance 33, Aura Sphere 37, Close Combat 42, Dragon Pulse 47, Meteor Mash 48, ExtremeSpeed 51 | Lucario (from 28) |
| Snorunt | egg gift | 1 | Oxide | Powder Snow, Leer | Double Team 4, Bite 10, Icy Wind 13, Headbutt 19, Protect 22, Ice Fang 28, Crunch 31, Ice Shard 37; as Glalie: Blizzard 51 | Glalie (from 42) |
| Snorunt | egg gift | 1 | Oxide | Powder Snow, Leer | as Froslass: Double Team 4, Astonish 10, Icy Wind 13, Confuse Ray 19, Ominous Wind 22, Wake-Up Slap 28, Captivate 31, Ice Shard 37, Blizzard 51 | Froslass (from 1) |
| Snorunt | egg gift | 1 | Rewrite | Powder Snow, Leer | Bite 10, Icy Wind 13, Headbutt 19, Ominous Wind 22, Ice Fang 28, Crunch 31, Draining Kiss 34, Ice Shard 37; as Glalie: Rock Slide 42, Power Gem 44, Confuse Ray 48, Earth Power 53 | Glalie (from 42) |
| Snorunt | egg gift | 1 | Rewrite | Powder Snow, Leer | as Froslass: Astonish 10, Icy Wind 13, Confuse Ray 19, Ominous Wind 22, Wake-Up Slap 28, Captivate 31, Ice Shard 37, Ice Beam 51 | Froslass (from 1) |
| Swablu | egg gift | 1 | Oxide | Peck, Growl | Astonish 5, Sing 9, Fury Attack 13, Safeguard 18, Mist 23, Take Down 28, Natural Gift 32; as Altaria: DragonBreath 35, Dragon Dance 39, Refresh 46 | Altaria (from 35) |
| Swablu | egg gift | 1 | Rewrite | Peck | Astonish 5, Sing 9, Safeguard 18, Dragon Dance 20, Mist 23, Air Slash 24, Take Down 28, Natural Gift 32, Play Rough 34, Steel Wing 35; as Altaria: DragonBreath 35, Mirror Move 36, Bulldoze 40, Breaking Swipe 43, Refresh 46, Moonblast 50 | Altaria (from 35) |
| Mantyke | old rod | 14 | Oxide | Bubble, Supersonic, BubbleBeam, Headbutt | Agility 19, Wing Attack 22, Water Pulse 28; as Mantine: Take Down 31, Confuse Ray 37, Bounce 40, Aqua Ring 46, Hydro Pump 49 | Mantine (from 30) |
| Mantyke | old rod | 14 | Rewrite | Tackle, Bubble, BubbleBeam, Headbutt | Agility 19, Wing Attack 22, Icy Wind 25, Water Pulse 28; as Mantine: Take Down 31, Scald 34, Confuse Ray 37, Bounce 40, Psybeam 41, Signal Beam 43, Aqua Ring 46, Surf 49 | Mantine (from 30) |
| Remoraid | old rod | 14 | Oxide | Water Gun, Lock-On, Psybeam, Aurora Beam | BubbleBeam 19, Focus Energy 23; as Octillery: Octazooka 25, Bullet Seed 29, Wring Out 36, Signal Beam 42, Ice Beam 48 | Octillery (from 25) |
| Remoraid | old rod | 14 | Rewrite | Water Pulse, Psybeam, Screech, Aurora Beam | BubbleBeam 19, Focus Energy 23; as Octillery: Octazooka 25, Mud Shot 27, Bullet Seed 29, Round 33, Charge Beam 35, Scald 37, Skitter Smack 40, Signal Beam 42, Ice Beam 48 | Octillery (from 25) |
| Luvdisc | old rod | 15 | Oxide | Charm, Water Gun, Agility, Take Down | Lucky Chant 17, Attract 22, Sweet Kiss 27; as Alomomola: Soak 33, Wish 37, Brine 41, Safeguard 45, Whirlpool 49, Helping Hand 53 | Alomomola (from 30) |
| Luvdisc | old rod | 15 | Rewrite | Water Gun, Aqua Jet, Draining Kiss, Take Down | Lucky Chant 17, Agility 18, Icy Wind 20, Attract 22, Sweet Kiss 27; as Alomomola: Heal Pulse 30, Wake-Up Slap 31, Water Pulse 32, Soak 33, Play Rough 35, Wish 37, Brine 41, Zen Headbutt 43, Safeguard 45, Whirlpool 49, Helping Hand 53 | Alomomola (from 30) |
| Shellos | old rod | 15 | Oxide | Mud Sport, Harden, Water Pulse, Mud Bomb | Hidden Power 16, Body Slam 29; as Gastrodon: Muddy Water 41 | Gastrodon (from 30) |
| Shellos | old rod | 15 | Rewrite | Mud-Slap, Harden, Water Pulse, Mud Bomb | Hidden Power 16, Swagger 22, Body Slam 29; as Gastrodon: AncientPower 33, Earth Power 35, Clear Smog 37, Muddy Water 41, Bulldoze 44, Sludge Bomb 46, Ice Beam 49 | Gastrodon (from 30) |
| Frogadier | old rod | 16 | Oxide | Quick Attack, Lick, Water Pulse, Icy Wind | Faint Attack 20, Acrobatics 22, Low Kick 25, Waterfall 30, Fling 35; as Greninja: Scald 37, Dark Pulse 40, Extrasensory 43, Sludge Wave 47, Gunk Shot 51 | Greninja (from 36) |
| Frogadier | old rod | 16 | Rewrite | Quick Attack, Lick, Water Pulse, Icy Wind | Thief 19, Faint Attack 20, Acrobatics 22, Low Kick 25, Scald 27, Waterfall 30, Fling 35; as Greninja: Shadow Sneak 36, Scald 37, Dark Pulse 40, Extrasensory 43, Sludge Wave 47, Gunk Shot 51 | Greninja (from 36) |
| Shellder | good rod | 24 | Oxide | Supersonic, Icicle Spear, Protect, Leer | as Cloyster: Spikes 28, Spike Cannon 40 | Cloyster (from 24) |
| Shellder | good rod | 24 | Rewrite | Tackle, Icicle Spear | as Cloyster: Spikes 28, Spike Cannon 40, Icicle Crash 45, Poison Fang 49, Razor Shell 53 | Cloyster (from 24) |
| Tentacool | good rod | 24 | Oxide | Acid, Toxic Spikes, BubbleBeam, Wrap | Barrier 26, Water Pulse 29; as Tentacruel: Poison Jab 36, Screech 42, Hydro Pump 49 | Tentacruel (from 30) |
| Tentacool | good rod | 24 | Rewrite | Acid, Toxic Spikes, Water Pulse, BubbleBeam | Barrier 26; as Tentacruel: Poison Jab 33, Aurora Beam 34, Sludge Bomb 39, Screech 42, Psybeam 44, Surf 49, Muddy Water 53 | Tentacruel (from 30) |
| Mareanie | good rod | 26 | Oxide | Wide Guard, Venoshock, Toxic Spikes, Recover | Spike Cannon 29, Pin Missile 34, Toxic 36; as Toxapex: Toxic 39, Venom Drench 42, Poison Jab 43, Liquidation 45 | Toxapex (from 38) |
| Mareanie | good rod | 26 | Rewrite | Wide Guard, Venoshock, Toxic Spikes, Recover | Spike Cannon 29, Pin Missile 34, Toxic 36, Muddy Water 38; as Toxapex: Venom Drench 42, Poison Jab 43, Liquidation 45, Lunge 53 | Toxapex (from 38) |
| Remoraid | good rod | 26 | Oxide | Psybeam, Aurora Beam, BubbleBeam, Focus Energy | Bullet Seed 27; as Octillery: Bullet Seed 29, Wring Out 36, Signal Beam 42, Ice Beam 48 | Octillery (from 27) |
| Remoraid | good rod | 26 | Rewrite | Screech, Aurora Beam, BubbleBeam, Focus Energy | as Octillery: Mud Shot 27, Bullet Seed 29, Round 33, Charge Beam 35, Scald 37, Skitter Smack 40, Signal Beam 42, Ice Beam 48 | Octillery (from 27) |
| Relicanth | good rod | 28 | Oxide | Harden, Water Gun, Rock Tomb, Yawn | Take Down 29, Mud Sport 36, AncientPower 43, Double-Edge 50 | Relicanth |
| Relicanth | good rod | 28 | Rewrite | Harden, Water Gun, Rock Tomb, Yawn | Take Down 29, AncientPower 43, Bulldoze 46, Double-Edge 50 | Relicanth |
| Gastrodon | surf | 30 | Oxide | Water Pulse, Mud Bomb, Hidden Power, Body Slam | Muddy Water 41 | Gastrodon |
| Gastrodon | surf | 30 | Rewrite | Water Pulse, Mud Bomb, Hidden Power, Body Slam | AncientPower 33, Earth Power 35, Clear Smog 37, Muddy Water 41, Bulldoze 44, Sludge Bomb 46, Ice Beam 49 | Gastrodon |
| Mantine | surf | 30 | Oxide | Headbutt, Agility, Wing Attack, Water Pulse | Take Down 31, Confuse Ray 37, Bounce 40, Aqua Ring 46, Hydro Pump 49 | Mantine |
| Mantine | surf | 30 | Rewrite | Headbutt, Agility, Wing Attack, Water Pulse | Take Down 31, Scald 34, Confuse Ray 37, Bounce 40, Psybeam 41, Signal Beam 43, Aqua Ring 46, Surf 49 | Mantine |
| Steelix | wild | 30 to 33 | Oxide | Rage, Rock Tomb, Slam, Rock Polish | DragonBreath 33, Curse 38, Iron Tail 41, Crunch 46, Double-Edge 49 | Steelix |
| Steelix | wild | 30 to 33 | Rewrite | Rock Throw, Rock Tomb, Metal Claw, Slam | DragonBreath 33, Rock Polish 34, Curse 38, Iron Head 41, Bite 43, Crunch 46, Double-Edge 49 | Steelix |
| Bronzor | wild | 31 | Oxide | Confuse Ray, Extrasensory, Iron Defense, Safeguard | as Bronzong: Block 33, Gyro Ball 38, Future Sight 43, Faint Attack 50 | Bronzong (from 33) |
| Bronzor | wild | 31 | Rewrite | Extrasensory, Bulldoze, Iron Defense, Safeguard | as Bronzong: Block 33, Iron Head 35, Gyro Ball 38, Rock Tomb 40, Future Sight 43, Body Press 46, Faint Attack 50 | Bronzong (from 33) |
| Golbat | wild | 31 | Oxide | Bite, Wing Attack, Confuse Ray, Air Cutter | Mean Look 33, Poison Fang 39; as Crobat: Haze 45, Air Slash 51 | Crobat (from 40) |
| Golbat | wild | 31 | Rewrite | Wing Attack, Confuse Ray, Air Cutter, Poison Jab | Mean Look 33, Steel Wing 36, Poison Fang 39; as Crobat: Zen Headbutt 45, Air Slash 51 | Crobat (from 40) |
| Graveler | wild | 31 | Oxide | Magnitude, Selfdestruct, Rollout, Rock Blast | Earthquake 33, Explosion 38; as Golem: Double-Edge 44, Stone Edge 49 | Golem (from 40) |
| Graveler | wild | 31 | Rewrite | Rollout, Karate Chop, Rock Blast, Rock Slide | Earthquake 33, Iron Head 36, Rock Tomb 39; as Golem: Double-Edge 44, Stone Edge 49, Sucker Punch 53 | Golem (from 40) |
| Hariyama | wild | 31 | Oxide | Whirlwind, Knock Off, SmellingSalt, Belly Drum | Force Palm 32, Seismic Toss 37, Wake-Up Slap 42, Endure 47, Close Combat 52 | Hariyama |
| Hariyama | wild | 31 | Rewrite | Knock Off, SmellingSalt, Belly Drum, Low Sweep | Force Palm 32, Bulldoze 34, Seismic Toss 37, Rock Tomb 39, Wake-Up Slap 42, Drain Punch 44, Endure 47, Close Combat 52 | Hariyama |
| Lunatone | wild | 31 to 32 | Oxide | Hypnosis, Rock Polish, Psywave, Embargo | Cosmic Power 34, Heal Block 42, Psychic 45, Future Sight 53 | Lunatone |
| Lunatone | wild | 31 to 32 | Rewrite | Hypnosis, Rock Polish, Psywave, Embargo | Cosmic Power 34, Heal Block 42, Psychic 45, Aura Sphere 47, Power Gem 49, Future Sight 53 | Lunatone |
| Metang | wild | 31 | Oxide | Metal Claw, Confusion, Scary Face, Pursuit | Bullet Punch 32, Psychic 36, Iron Defense 40, Agility 44; as Metagross: Hammer Arm 45, Meteor Mash 53 | Metagross (from 45) |
| Metang | wild | 31 | Rewrite | Magnet Rise, Take Down, Metal Claw, Confusion | Bullet Punch 32, Metal Claw 33, Scary Face 34, Pursuit 35, Psychic 36, Iron Defense 40, Agility 44; as Metagross: Hammer Arm 45, Zen Headbutt 52, Meteor Mash 53 | Metagross (from 45) |
| Solrock | wild | 31 | Oxide | Fire Spin, Rock Polish, Psywave, Embargo | Cosmic Power 34, Heal Block 42, Rock Slide 45, SolarBeam 53 | Solrock |
| Solrock | wild | 31 | Rewrite | Fire Spin, Rock Polish, Psywave, Embargo | Cosmic Power 34, Heal Block 42, Rock Slide 45, Bulldoze 47, Zen Headbutt 49, SolarBeam 53 | Solrock |
| Naclstack | wild | 32 | Oxide | Rock Polish, Headbutt, Iron Defense, Recover | Rock Slide 34, Stealth Rock 38; as Garganacl: Stealth Rock 40, Heavy Slam 44, Earthquake 49 | Garganacl (from 38) |
| Naclstack | wild | 32 | Rewrite | Bulldoze, Recover, Rock Polish, Rock Tomb | Rock Slide 34, Stealth Rock 38; as Garganacl: Rock Tomb 38, Salt Cure 39, Stealth Rock 40, Iron Head 42, Heavy Slam 44, Zen Headbutt 46, Earthquake 49 | Garganacl (from 38) |
| Togedemaru | wild | 32 | Oxide | Pin Missile, Eerie Impulse, Smart Strike, Super Fang | Zing Zap 34, Iron Head 38, Electroweb 42, Wild Charge 48 | Togedemaru |
| Togedemaru | wild | 32 | Rewrite | Pin Missile, Eerie Impulse, Smart Strike, Super Fang | Zing Zap 34, Iron Head 38, Electroweb 42, Wild Charge 48, U-turn 53 | Togedemaru |
| Corsola | surf | 33 | Oxide | Rock Blast, BubbleBeam, Lucky Chant, AncientPower | Aqua Ring 37, Spike Cannon 40, Power Gem 44, Mirror Coat 48, Earth Power 53 | Corsola |
| Corsola | surf | 33 | Rewrite | Rock Blast, BubbleBeam, Lucky Chant, Aqua Cutter | Liquidation 35, Aqua Ring 37, Spike Cannon 40, Throat Chop 42, Power Gem 44, Mirror Coat 48, Earth Power 53 | Corsola |
| Klefki | wild | 33 | Oxide | Torment, Draining Kiss, Recycle, Imprison | Mirror Shot 34, Flash Cannon 36, Foul Play 38, Play Rough 41, Magic Room 44, Heal Block 50, Last Resort 52 | Klefki |
| Klefki | wild | 33 | Rewrite | Draining Kiss, Torment, Imprison, Recycle | Mirror Shot 34, Iron Defense 35, Flash Cannon 36, Foul Play 38, Play Rough 41, Magic Room 44, Calm Mind 47, Heal Block 50, Last Resort 52 | Klefki |
| Mawile | wild | 33 | Oxide | Sweet Scent, ViceGrip, Faint Attack, Baton Pass | Crunch 36, Iron Defense 41, Sucker Punch 46, Stockpile 51, Swallow 51, Spit Up 51 | Mawile |
| Mawile | wild | 33 | Rewrite | Fake Tears, Bite, ViceGrip, Faint Attack | Crunch 36, Iron Defense 41, Sucker Punch 46, Play Rough 48, Swallow 50, Stockpile 51, Spit Up 52, Meteor Mash 53 | Mawile |
| Tentacool | surf | 33 | Oxide | Wrap, Barrier, Water Pulse, Poison Jab | as Tentacruel: Poison Jab 36, Screech 42, Hydro Pump 49 | Tentacruel (from 34) |
| Tentacool | surf | 33 | Rewrite | Water Pulse, BubbleBeam, Barrier, Poison Jab | as Tentacruel: Aurora Beam 34, Sludge Bomb 39, Screech 42, Psybeam 44, Surf 49, Muddy Water 53 | Tentacruel (from 34) |
| Mareanie | surf | 36 | Oxide | Recover, Spike Cannon, Pin Missile, Toxic | as Toxapex: Toxic 39, Venom Drench 42, Poison Jab 43, Liquidation 45 | Toxapex (from 38) |
| Mareanie | surf | 36 | Rewrite | Recover, Spike Cannon, Pin Missile, Toxic | Muddy Water 38; as Toxapex: Venom Drench 42, Poison Jab 43, Liquidation 45, Lunge 53 | Toxapex (from 38) |

## Lake Valor

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 53 | At the cap |
|---|---|---|---|---|---|---|
| Chinchou | old rod | 14 | Oxide | Supersonic, Thunder Wave, Flail, Water Gun | Confuse Ray 17, Spark 20, Take Down 23; as Lanturn: Stockpile 27, Swallow 27, Spit Up 27, BubbleBeam 30, Signal Beam 35, Discharge 40, Aqua Ring 47, Hydro Pump 52 | Lanturn (from 27) |
| Chinchou | old rod | 14 | Rewrite | Thunder Wave, Flail, Water Gun, Screech | Confuse Ray 17, Spark 20, Take Down 23, Icy Wind 26; as Lanturn: Stockpile 27, Swallow 28, Spit Up 29, BubbleBeam 30, Signal Beam 31, Scald 33, Surf 34, Thunderbolt 37, Discharge 40, Flash Cannon 43, Aqua Ring 47, Muddy Water 52 | Lanturn (from 27) |
| Corphish | old rod | 14 | Oxide | Bubble, Harden, ViceGrip, Leer | BubbleBeam 20, Protect 23, Knock Off 26; as Crawdaunt: Swift 30, Taunt 34, Night Slash 39, Crabhammer 44, Swords Dance 52 | Crawdaunt (from 30) |
| Corphish | old rod | 14 | Rewrite | Taunt, ViceGrip, BubbleBeam, Leer | Razor Shell 17, Knock Off 26; as Crawdaunt: Swift 30, Taunt 32, Throat Chop 35, Aerial Ace 36, Night Slash 39, X-Scissor 41, Crabhammer 44, Brick Break 48, Swords Dance 52 | Crawdaunt (from 30) |
| Corsola | old rod | 15 | Oxide | Tackle, Harden, Bubble, Recover | Refresh 16, Rock Blast 20, BubbleBeam 25, Lucky Chant 28, AncientPower 32, Aqua Ring 37, Spike Cannon 40, Power Gem 44, Mirror Coat 48, Earth Power 53 | Corsola |
| Corsola | old rod | 15 | Rewrite | Tackle, Life Dew, Bubble, Recover | AncientPower 16, Bulldoze 18, Rock Blast 20, BubbleBeam 25, Lucky Chant 28, Aqua Cutter 33, Liquidation 35, Aqua Ring 37, Spike Cannon 40, Throat Chop 42, Power Gem 44, Mirror Coat 48, Earth Power 53 | Corsola |
| Goldeen | old rod | 15 | Oxide | Tail Whip, Water Sport, Supersonic, Horn Attack | Water Pulse 17, Flail 21, Aqua Ring 27, Fury Attack 31; as Seaking: Waterfall 40, Horn Drill 47 | Seaking (from 33) |
| Goldeen | old rod | 15 | Rewrite | Water Sport, Flip Turn, Water Pulse, Horn Attack | Swagger 17, Flail 21, Aqua Ring 27; as Seaking: Aqua Jet 34, Skull Bash 37, Waterfall 40, Poison Jab 44, Drill Run 47, Knock Off 50 | Seaking (from 33) |
| Horsea | old rod | 16 | Oxide | SmokeScreen, Leer, Water Gun, Focus Energy | BubbleBeam 18, Agility 23, Twister 26, Brine 30; as Kingdra: Hydro Pump 40, Dragon Dance 48 | Kingdra (from 32) |
| Horsea | old rod | 16 | Rewrite | Bubble, SmokeScreen, Water Gun, Focus Energy | BubbleBeam 18, Agility 23, Twister 26, Brine 30; as Kingdra: Muddy Water 40, Aurora Beam 44 | Kingdra (from 32) |
| Frillish | good rod | 24 | Oxide | Night Shade, Ominous Wind, Water Pulse, Imprison | Confuse Ray 25, Hex 30, Brine 34, Pain Split 39; as Jellicent: Destiny Bond 45, Shadow Ball 51 | Jellicent (from 40) |
| Frillish | good rod | 24 | Rewrite | Night Shade, Ominous Wind, Water Pulse, Imprison | Confuse Ray 25, Hex 30, Brine 34, Dark Pulse 36, Pain Split 39; as Jellicent: Muddy Water 45, Shadow Ball 51 | Jellicent (from 40) |
| Goldeen | good rod | 24 | Oxide | Supersonic, Horn Attack, Water Pulse, Flail | Aqua Ring 27, Fury Attack 31; as Seaking: Waterfall 40, Horn Drill 47 | Seaking (from 33) |
| Goldeen | good rod | 24 | Rewrite | Water Pulse, Horn Attack, Swagger, Flail | Aqua Ring 27; as Seaking: Aqua Jet 34, Skull Bash 37, Waterfall 40, Poison Jab 44, Drill Run 47, Knock Off 50 | Seaking (from 33) |
| Barboach | good rod | 26 | Oxide | Mud Bomb, Amnesia, Water Pulse, Magnitude | as Whiscash: Rest 33, Snore 33, Aqua Tail 39, Earthquake 45, Future Sight 51 | Whiscash (from 30) |
| Barboach | good rod | 26 | Rewrite | Amnesia, Rock Tomb, Water Pulse, Magnitude | as Whiscash: Bulldoze 30, Rest 33, Zen Headbutt 36, Aqua Tail 39, Earth Power 40, Wild Charge 42, Earthquake 45, Future Sight 51 | Whiscash (from 30) |
| Feebas | good rod | 26 | Oxide | Splash, Tackle | Flail 30; as Milotic: Hydro Pump 37, Attract 41, Safeguard 45, Aqua Ring 49 | Milotic (from 30) |
| Feebas | good rod | 26 | Rewrite | Tackle, Recover, Dragon Tail, Captivate | Flail 30; as Milotic: Twister 30, Recover 31, Aqua Tail 32, Aurora Beam 33, Dragon Pulse 35, Surf 37, Attract 41, Muddy Water 43, Safeguard 45, Aqua Ring 49 | Milotic (from 30) |
| Frogadier | good rod | 28 | Oxide | Icy Wind, Faint Attack, Acrobatics, Low Kick | Waterfall 30, Fling 35; as Greninja: Scald 37, Dark Pulse 40, Extrasensory 43, Sludge Wave 47, Gunk Shot 51 | Greninja (from 36) |
| Frogadier | good rod | 28 | Rewrite | Faint Attack, Acrobatics, Low Kick, Scald | Waterfall 30, Fling 35; as Greninja: Shadow Sneak 36, Scald 37, Dark Pulse 40, Extrasensory 43, Sludge Wave 47, Gunk Shot 51 | Greninja (from 36) |
| Frillish | surf | 30 | Oxide | Water Pulse, Imprison, Confuse Ray, Hex | Brine 34, Pain Split 39; as Jellicent: Destiny Bond 45, Shadow Ball 51 | Jellicent (from 40) |
| Frillish | surf | 30 | Rewrite | Water Pulse, Imprison, Confuse Ray, Hex | Brine 34, Dark Pulse 36, Pain Split 39; as Jellicent: Muddy Water 45, Shadow Ball 51 | Jellicent (from 40) |
| Goldeen | surf | 30 | Oxide | Horn Attack, Water Pulse, Flail, Aqua Ring | Fury Attack 31; as Seaking: Waterfall 40, Horn Drill 47 | Seaking (from 33) |
| Goldeen | surf | 30 | Rewrite | Horn Attack, Swagger, Flail, Aqua Ring | as Seaking: Aqua Jet 34, Skull Bash 37, Waterfall 40, Poison Jab 44, Drill Run 47, Knock Off 50 | Seaking (from 33) |
| Floatzel | surf | 33 | Oxide | Swift, Aqua Jet, Crunch, Agility | Whirlpool 39, Razor Wind 50 | Floatzel |
| Floatzel | surf | 33 | Rewrite | Aqua Jet, Crunch, Icy Wind, Flip Turn | Waterfall 36, Whirlpool 39, Liquidation 41, Low Sweep 44, Agility 51, Rock Tomb 53 | Floatzel |
| Jellicent | surf | 33 | Oxide | Water Pulse, Imprison, Confuse Ray, Hex | Brine 34, Pain Split 39, Destiny Bond 45, Shadow Ball 51 | Jellicent |
| Jellicent | surf | 33 | Rewrite | Water Pulse, Imprison, Confuse Ray, Hex | Brine 34, Pain Split 39, Muddy Water 45, Shadow Ball 51 | Jellicent |
| Frogadier | surf | 36 | Oxide | Acrobatics, Low Kick, Waterfall, Fling | as Greninja: Scald 37, Dark Pulse 40, Extrasensory 43, Sludge Wave 47, Gunk Shot 51 | Greninja (from 37) |
| Frogadier | surf | 36 | Rewrite | Low Kick, Scald, Waterfall, Fling | as Greninja: Scald 37, Dark Pulse 40, Extrasensory 43, Sludge Wave 47, Gunk Shot 51 | Greninja (from 37) |
| Absol | wild | 38 to 41 | Oxide | Swords Dance, Bite, Double Team, Slash | Future Sight 41, Sucker Punch 44, Detect 49, Night Slash 52 | Absol |
| Absol | wild | 38 to 41 | Rewrite | Pursuit, Swords Dance, Bite, Slash | Future Sight 41, Sucker Punch 44, X-Scissor 48, Night Slash 52 | Absol |
| Cinccino | wild | 39 | both | Pound, Baby-Doll Eyes, Helping Hand, Echoed Voice | nothing | Cinccino |
| Gothorita | wild | 39 | Oxide | Heal Block, Psych Up, Flatter, Psychic | as Gothitelle: Future Sight 44, Telekinesis 45 | Gothitelle (from 41) |
| Gothorita | wild | 39 | Rewrite | Heal Block, Psych Up, Flatter, Psychic | as Gothitelle: Shadow Ball 41, Future Sight 44 | Gothitelle (from 41) |
| Hawlucha | wild | 39 | Oxide | Submission, Tailwind, Dual Wingbeat, Fly | Hi Jump Kick 42, Me First 48 | Hawlucha |
| Hawlucha | wild | 39 | Rewrite | Flying Press, Tailwind, Dual Wingbeat, Fly | Hi Jump Kick 42, Air Slash 45, Lunge 48 | Hawlucha |
| Liepard | wild | 39 | Oxide | Assurance, Hone Claws, Slash, Taunt | Sucker Punch 43, Nasty Plot 44, Night Slash 44, Snatch 47 | Liepard |
| Liepard | wild | 39 | Rewrite | Nasty Plot, Slash, Throat Chop, Taunt | Sucker Punch 43, Night Slash 44, Snatch 47, Skitter Smack 50 | Liepard |
| Lopunny | wild | 39 | Oxide | Jump Kick, Baton Pass, Agility, Dizzy Punch | Charm 43, Bounce 46, Healing Wish 53 | Lopunny |
| Lopunny | wild | 39 | Rewrite | Bite, Agility, Dizzy Punch, Strength | Body Slam 41, Charm 43, Bounce 46, Crunch 49, U-turn 53 | Lopunny |
| Skarmory | wild | 39 to 40 | Oxide | Spikes, Metal Sound, Steel Wing, Air Slash | Slash 42, Night Slash 45 | Skarmory |
| Skarmory | wild | 39 to 40 | Rewrite | Spikes, Metal Sound, Steel Wing, Air Slash | Slash 42, Night Slash 45, Iron Defense 48 | Skarmory |
| Altaria | wild | 40 | Oxide | Take Down, Natural Gift, DragonBreath, Dragon Dance | Refresh 46 | Altaria |
| Altaria | wild | 40 | Rewrite | Natural Gift, DragonBreath, Mirror Move, Bulldoze | Breaking Swipe 43, Refresh 46, Moonblast 50 | Altaria |
| Purugly | wild | 40 | Oxide | Assist, Captivate, Slash, Swagger | Body Slam 45, Attract 53 | Purugly |
| Purugly | wild | 40 | Rewrite | Slash, Swagger, Strength, Metal Claw | Shadow Claw 42, Body Slam 45, Attract 53 | Purugly |
| Honchkrow | wild | 41 | Oxide | Haze, Wing Attack, Swagger, Nasty Plot | Night Slash 45 | Honchkrow |
| Honchkrow | wild | 41 | Rewrite | Pursuit, Wing Attack, Swagger, Drill Peck | Night Slash 45, Nasty Plot 46 | Honchkrow |
| Weavile | wild | 41 | Oxide | Nasty Plot, Icy Wind, Night Slash, Fling | Metal Claw 42, Dark Pulse 49 | Weavile |
| Weavile | wild | 41 | Rewrite | Fury Swipes, Icy Wind, Night Slash, Fling | Metal Claw 42, Dark Pulse 49 | Weavile |

## Lake Verity

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 53 | At the cap |
|---|---|---|---|---|---|---|
| Goldeen | surf | 20 | Oxide | Water Sport, Supersonic, Horn Attack, Water Pulse | Flail 21, Aqua Ring 27, Fury Attack 31; as Seaking: Waterfall 40, Horn Drill 47 | Seaking (from 33) |
| Goldeen | surf | 20 | Rewrite | Flip Turn, Water Pulse, Horn Attack, Swagger | Flail 21, Aqua Ring 27; as Seaking: Aqua Jet 34, Skull Bash 37, Waterfall 40, Poison Jab 44, Drill Run 47, Knock Off 50 | Seaking (from 33) |
| Surskit | surf | 20 | Oxide | Bubble, Quick Attack, Sweet Scent, Water Sport | as Masquerain: Gust 22, Scary Face 26, Stun Spore 33, Silver Wind 40, Air Slash 47 | Masquerain (from 22) |
| Surskit | surf | 20 | Rewrite | Quick Attack, Gust, Silver Wind, Water Sport | as Masquerain: Gust 22, BubbleBeam 25, Scary Face 26, Mud Bomb 29, Stun Spore 33, Surf 36, Giga Drain 38, Silver Wind 40, Signal Beam 41, Icy Wind 43, Air Slash 47, Lunge 53 | Masquerain (from 22) |
| Corphish | surf | 23 | Oxide | ViceGrip, Leer, BubbleBeam, Protect | Knock Off 26; as Crawdaunt: Swift 30, Taunt 34, Night Slash 39, Crabhammer 44, Swords Dance 52 | Crawdaunt (from 30) |
| Corphish | surf | 23 | Rewrite | ViceGrip, BubbleBeam, Leer, Razor Shell | Knock Off 26; as Crawdaunt: Swift 30, Taunt 32, Throat Chop 35, Aerial Ace 36, Night Slash 39, X-Scissor 41, Crabhammer 44, Brick Break 48, Swords Dance 52 | Crawdaunt (from 30) |
| Floatzel | surf | 23 | Oxide | Water Gun, Pursuit, Swift, Aqua Jet | Crunch 26, Agility 29, Whirlpool 39, Razor Wind 50 | Floatzel |
| Floatzel | surf | 23 | Rewrite | Water Gun, Pursuit, Swift, Aqua Jet | Crunch 26, Icy Wind 29, Flip Turn 33, Waterfall 36, Whirlpool 39, Liquidation 41, Low Sweep 44, Agility 51, Rock Tomb 53 | Floatzel |
| Croconaw | surf | 26 | Oxide | Bite, Scary Face, Ice Fang, Flail | Crunch 30; as Feraligatr: Agility 30, Crunch 32, Slash 37, Screech 45, Thrash 50 | Feraligatr (from 30) |
| Croconaw | surf | 26 | Rewrite | Bite, Scary Face, Ice Fang, Flail | as Feraligatr: Agility 30, Crunch 32, Slash 33, Bulldoze 35, Metal Claw 39, Aqua Jet 40, Liquidation 42, Screech 45, Thrash 50 | Feraligatr (from 30) |

## Mt. Coronet South

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 53 | At the cap |
|---|---|---|---|---|---|---|
| Buizel | surf | 24 | Oxide | Water Gun, Pursuit, Swift, Aqua Jet | as Floatzel: Crunch 26, Agility 29, Whirlpool 39, Razor Wind 50 | Floatzel (from 26) |
| Buizel | surf | 24 | Rewrite | Pursuit, Scary Face, Swift, Aqua Jet | as Floatzel: Crunch 26, Icy Wind 29, Flip Turn 33, Waterfall 36, Whirlpool 39, Liquidation 41, Low Sweep 44, Agility 51, Rock Tomb 53 | Floatzel (from 26) |
| Frillish | surf | 24 | Oxide | Night Shade, Ominous Wind, Water Pulse, Imprison | Confuse Ray 25, Hex 30, Brine 34, Pain Split 39; as Jellicent: Destiny Bond 45, Shadow Ball 51 | Jellicent (from 40) |
| Frillish | surf | 24 | Rewrite | Night Shade, Ominous Wind, Water Pulse, Imprison | Confuse Ray 25, Hex 30, Brine 34, Dark Pulse 36, Pain Split 39; as Jellicent: Muddy Water 45, Shadow Ball 51 | Jellicent (from 40) |
| Feebas | surf | 27 | Oxide | Splash, Tackle | Flail 30; as Milotic: Hydro Pump 37, Attract 41, Safeguard 45, Aqua Ring 49 | Milotic (from 30) |
| Feebas | surf | 27 | Rewrite | Tackle, Recover, Dragon Tail, Captivate | Flail 30; as Milotic: Twister 30, Recover 31, Aqua Tail 32, Aurora Beam 33, Dragon Pulse 35, Surf 37, Attract 41, Muddy Water 43, Safeguard 45, Aqua Ring 49 | Milotic (from 30) |
| Shellos | surf | 27 | Oxide | Harden, Water Pulse, Mud Bomb, Hidden Power | Body Slam 29; as Gastrodon: Muddy Water 41 | Gastrodon (from 30) |
| Shellos | surf | 27 | Rewrite | Water Pulse, Mud Bomb, Hidden Power, Swagger | Body Slam 29; as Gastrodon: AncientPower 33, Earth Power 35, Clear Smog 37, Muddy Water 41, Bulldoze 44, Sludge Bomb 46, Ice Beam 49 | Gastrodon (from 30) |
| Pelipper | surf | 30 | Oxide | Mist, Water Pulse, Payback, Protect | Roost 31, Stockpile 38, Swallow 38, Spit Up 38, Fling 43, Tailwind 50 | Pelipper |
| Pelipper | surf | 30 | Rewrite | Supersonic, Water Pulse, Payback, Liquidation | Roost 31, Surf 34, Swallow 37, Stockpile 38, Spit Up 39, Icy Wind 40, Fling 43, Air Slash 47, Tailwind 50, Brave Bird 53 | Pelipper |

## Oreburgh Gate

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 53 | At the cap |
|---|---|---|---|---|---|---|
| Jellicent | surf | 20 | Oxide | Night Shade, Ominous Wind, Water Pulse, Imprison | Confuse Ray 25, Hex 30, Brine 34, Pain Split 39, Destiny Bond 45, Shadow Ball 51 | Jellicent |
| Jellicent | surf | 20 | Rewrite | Night Shade, Ominous Wind, Water Pulse, Imprison | Confuse Ray 25, Hex 30, Brine 34, Pain Split 39, Muddy Water 45, Shadow Ball 51 | Jellicent |
| Shellos | surf | 20 | Oxide | Harden, Water Pulse, Mud Bomb, Hidden Power | Body Slam 29; as Gastrodon: Muddy Water 41 | Gastrodon (from 30) |
| Shellos | surf | 20 | Rewrite | Harden, Water Pulse, Mud Bomb, Hidden Power | Swagger 22, Body Slam 29; as Gastrodon: AncientPower 33, Earth Power 35, Clear Smog 37, Muddy Water 41, Bulldoze 44, Sludge Bomb 46, Ice Beam 49 | Gastrodon (from 30) |
| Buizel | surf | 23 | Oxide | Water Gun, Pursuit, Swift, Aqua Jet | as Floatzel: Crunch 26, Agility 29, Whirlpool 39, Razor Wind 50 | Floatzel (from 26) |
| Buizel | surf | 23 | Rewrite | Pursuit, Scary Face, Swift, Aqua Jet | as Floatzel: Crunch 26, Icy Wind 29, Flip Turn 33, Waterfall 36, Whirlpool 39, Liquidation 41, Low Sweep 44, Agility 51, Rock Tomb 53 | Floatzel (from 26) |
| Floatzel | surf | 23 | Oxide | Water Gun, Pursuit, Swift, Aqua Jet | Crunch 26, Agility 29, Whirlpool 39, Razor Wind 50 | Floatzel |
| Floatzel | surf | 23 | Rewrite | Water Gun, Pursuit, Swift, Aqua Jet | Crunch 26, Icy Wind 29, Flip Turn 33, Waterfall 36, Whirlpool 39, Liquidation 41, Low Sweep 44, Agility 51, Rock Tomb 53 | Floatzel |
| Psyduck | surf | 26 | Oxide | Water Gun, Disable, Confusion, Water Pulse | Fury Swipes 27, Screech 31; as Golduck: Psych Up 37, Zen Headbutt 44, Amnesia 50 | Golduck (from 33) |
| Psyduck | surf | 26 | Rewrite | Water Pulse, Disable, Confusion, Low Sweep | Fury Swipes 27; as Golduck: Surf 34, Psych Up 37, Aurora Beam 40, Zen Headbutt 44, Power Gem 47, Amnesia 50 | Golduck (from 33) |

## Pastoria City

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 53 | At the cap |
|---|---|---|---|---|---|---|
| Araquanid | surf | 28 | Oxide | Aqua Ring, BubbleBeam, Bug Bite, Headbutt | Soak 31, Dive 36, Lunge 41, Scald 48, Hydro Pump 51 | Araquanid |
| Araquanid | surf | 28 | Rewrite | BubbleBeam, Bug Bite, Headbutt, Spider Web | Soak 31, Skitter Smack 34, Dive 36, Waterfall 38, Lunge 41, Poison Jab 44, Scald 48, Surf 51 | Araquanid |
| Masquerain | surf | 28 | Oxide | Sweet Scent, Water Sport, Gust, Scary Face | Stun Spore 33, Silver Wind 40, Air Slash 47 | Masquerain |
| Masquerain | surf | 28 | Rewrite | Water Sport, Gust, BubbleBeam, Scary Face | Mud Bomb 29, Stun Spore 33, Surf 36, Giga Drain 38, Silver Wind 40, Signal Beam 41, Icy Wind 43, Air Slash 47, Lunge 53 | Masquerain |
| Frillish | surf | 31 to 34 | Oxide | Water Pulse, Imprison, Confuse Ray, Hex | Brine 34, Pain Split 39; as Jellicent: Destiny Bond 45, Shadow Ball 51 | Jellicent (from 40) |
| Frillish | surf | 31 to 34 | Rewrite | Water Pulse, Imprison, Confuse Ray, Hex | Brine 34, Dark Pulse 36, Pain Split 39; as Jellicent: Muddy Water 45, Shadow Ball 51 | Jellicent (from 40) |
| Quagsire | surf | 31 | Oxide | Slam, Mud Bomb, Amnesia, Yawn | Earthquake 36, Mist 48, Haze 48, Muddy Water 53 | Quagsire |
| Quagsire | surf | 31 | Rewrite | Mud Bomb, Amnesia, Trailblaze, Yawn | Earthquake 36, Rock Slide 39, Toxic 40, Drain Punch 44, Mist 48, Muddy Water 53 | Quagsire |

## Ravaged Path

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 53 | At the cap |
|---|---|---|---|---|---|---|
| Feebas | surf | 22 | Oxide | Splash, Tackle | Flail 30; as Milotic: Hydro Pump 37, Attract 41, Safeguard 45, Aqua Ring 49 | Milotic (from 30) |
| Feebas | surf | 22 | Rewrite | Water Gun, Water Pulse, Tackle, Recover | Dragon Tail 24, Captivate 25, Flail 30; as Milotic: Twister 30, Recover 31, Aqua Tail 32, Aurora Beam 33, Dragon Pulse 35, Surf 37, Attract 41, Muddy Water 43, Safeguard 45, Aqua Ring 49 | Milotic (from 30) |
| Frillish | surf | 22 | Oxide | Night Shade, Ominous Wind, Water Pulse, Imprison | Confuse Ray 25, Hex 30, Brine 34, Pain Split 39; as Jellicent: Destiny Bond 45, Shadow Ball 51 | Jellicent (from 40) |
| Frillish | surf | 22 | Rewrite | Night Shade, Ominous Wind, Water Pulse, Imprison | Confuse Ray 25, Hex 30, Brine 34, Dark Pulse 36, Pain Split 39; as Jellicent: Muddy Water 45, Shadow Ball 51 | Jellicent (from 40) |
| Corphish | surf | 25 | Oxide | ViceGrip, Leer, BubbleBeam, Protect | Knock Off 26; as Crawdaunt: Swift 30, Taunt 34, Night Slash 39, Crabhammer 44, Swords Dance 52 | Crawdaunt (from 30) |
| Corphish | surf | 25 | Rewrite | ViceGrip, BubbleBeam, Leer, Razor Shell | Knock Off 26; as Crawdaunt: Swift 30, Taunt 32, Throat Chop 35, Aerial Ace 36, Night Slash 39, X-Scissor 41, Crabhammer 44, Brick Break 48, Swords Dance 52 | Crawdaunt (from 30) |
| Shellos | surf | 25 | Oxide | Harden, Water Pulse, Mud Bomb, Hidden Power | Body Slam 29; as Gastrodon: Muddy Water 41 | Gastrodon (from 30) |
| Shellos | surf | 25 | Rewrite | Water Pulse, Mud Bomb, Hidden Power, Swagger | Body Slam 29; as Gastrodon: AncientPower 33, Earth Power 35, Clear Smog 37, Muddy Water 41, Bulldoze 44, Sludge Bomb 46, Ice Beam 49 | Gastrodon (from 30) |
| Frogadier | surf | 28 | Oxide | Icy Wind, Faint Attack, Acrobatics, Low Kick | Waterfall 30, Fling 35; as Greninja: Scald 37, Dark Pulse 40, Extrasensory 43, Sludge Wave 47, Gunk Shot 51 | Greninja (from 36) |
| Frogadier | surf | 28 | Rewrite | Faint Attack, Acrobatics, Low Kick, Scald | Waterfall 30, Fling 35; as Greninja: Shadow Sneak 36, Scald 37, Dark Pulse 40, Extrasensory 43, Sludge Wave 47, Gunk Shot 51 | Greninja (from 36) |

## Route 203

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 53 | At the cap |
|---|---|---|---|---|---|---|
| Corphish | surf | 20 | Oxide | Harden, ViceGrip, Leer, BubbleBeam | Protect 23, Knock Off 26; as Crawdaunt: Swift 30, Taunt 34, Night Slash 39, Crabhammer 44, Swords Dance 52 | Crawdaunt (from 30) |
| Corphish | surf | 20 | Rewrite | ViceGrip, BubbleBeam, Leer, Razor Shell | Knock Off 26; as Crawdaunt: Swift 30, Taunt 32, Throat Chop 35, Aerial Ace 36, Night Slash 39, X-Scissor 41, Crabhammer 44, Brick Break 48, Swords Dance 52 | Crawdaunt (from 30) |
| Goldeen | surf | 20 | Oxide | Water Sport, Supersonic, Horn Attack, Water Pulse | Flail 21, Aqua Ring 27, Fury Attack 31; as Seaking: Waterfall 40, Horn Drill 47 | Seaking (from 33) |
| Goldeen | surf | 20 | Rewrite | Flip Turn, Water Pulse, Horn Attack, Swagger | Flail 21, Aqua Ring 27; as Seaking: Aqua Jet 34, Skull Bash 37, Waterfall 40, Poison Jab 44, Drill Run 47, Knock Off 50 | Seaking (from 33) |
| Floatzel | surf | 23 | Oxide | Water Gun, Pursuit, Swift, Aqua Jet | Crunch 26, Agility 29, Whirlpool 39, Razor Wind 50 | Floatzel |
| Floatzel | surf | 23 | Rewrite | Water Gun, Pursuit, Swift, Aqua Jet | Crunch 26, Icy Wind 29, Flip Turn 33, Waterfall 36, Whirlpool 39, Liquidation 41, Low Sweep 44, Agility 51, Rock Tomb 53 | Floatzel |
| Gastrodon | surf | 23 | Oxide | Harden, Water Pulse, Mud Bomb, Hidden Power | Body Slam 29, Muddy Water 41 | Gastrodon |
| Gastrodon | surf | 23 | Rewrite | Harden, Water Pulse, Mud Bomb, Hidden Power | Body Slam 29, AncientPower 33, Earth Power 35, Clear Smog 37, Muddy Water 41, Bulldoze 44, Sludge Bomb 46, Ice Beam 49 | Gastrodon |
| Froakie | surf | 26 | Oxide | Icy Wind, Faint Attack, Acrobatics, Low Kick | as Frogadier: Waterfall 30, Fling 35; as Greninja: Scald 37, Dark Pulse 40, Extrasensory 43, Sludge Wave 47, Gunk Shot 51 | Greninja (from 36) |
| Froakie | surf | 26 | Rewrite | Icy Wind, Faint Attack, Acrobatics, Low Kick | as Frogadier: Scald 27, Waterfall 30, Fling 35; as Greninja: Shadow Sneak 36, Scald 37, Dark Pulse 40, Extrasensory 43, Sludge Wave 47, Gunk Shot 51 | Greninja (from 36) |

## Route 204

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 53 | At the cap |
|---|---|---|---|---|---|---|
| Floatzel | surf | 20 | Oxide | Quick Attack, Water Gun, Pursuit, Swift | Aqua Jet 21, Crunch 26, Agility 29, Whirlpool 39, Razor Wind 50 | Floatzel |
| Floatzel | surf | 20 | Rewrite | Quick Attack, Water Gun, Pursuit, Swift | Aqua Jet 21, Crunch 26, Icy Wind 29, Flip Turn 33, Waterfall 36, Whirlpool 39, Liquidation 41, Low Sweep 44, Agility 51, Rock Tomb 53 | Floatzel |
| Gastrodon | surf | 20 | Oxide | Harden, Water Pulse, Mud Bomb, Hidden Power | Body Slam 29, Muddy Water 41 | Gastrodon |
| Gastrodon | surf | 20 | Rewrite | Harden, Water Pulse, Mud Bomb, Hidden Power | Body Slam 29, AncientPower 33, Earth Power 35, Clear Smog 37, Muddy Water 41, Bulldoze 44, Sludge Bomb 46, Ice Beam 49 | Gastrodon |
| Buizel | surf | 22 to 23 | Oxide | Water Gun, Pursuit, Swift, Aqua Jet | as Floatzel: Crunch 26, Agility 29, Whirlpool 39, Razor Wind 50 | Floatzel (from 26) |
| Buizel | surf | 22 to 23 | Rewrite | Pursuit, Scary Face, Swift, Aqua Jet | as Floatzel: Crunch 26, Icy Wind 29, Flip Turn 33, Waterfall 36, Whirlpool 39, Liquidation 41, Low Sweep 44, Agility 51, Rock Tomb 53 | Floatzel (from 26) |
| Shellos | surf | 22 | Oxide | Harden, Water Pulse, Mud Bomb, Hidden Power | Body Slam 29; as Gastrodon: Muddy Water 41 | Gastrodon (from 30) |
| Shellos | surf | 22 | Rewrite | Water Pulse, Mud Bomb, Hidden Power, Swagger | Body Slam 29; as Gastrodon: AncientPower 33, Earth Power 35, Clear Smog 37, Muddy Water 41, Bulldoze 44, Sludge Bomb 46, Ice Beam 49 | Gastrodon (from 30) |
| Masquerain | surf | 23 | Oxide | Quick Attack, Sweet Scent, Water Sport, Gust | Scary Face 26, Stun Spore 33, Silver Wind 40, Air Slash 47 | Masquerain |
| Masquerain | surf | 23 | Rewrite | Bubble, Quick Attack, Water Sport, Gust | BubbleBeam 25, Scary Face 26, Mud Bomb 29, Stun Spore 33, Surf 36, Giga Drain 38, Silver Wind 40, Signal Beam 41, Icy Wind 43, Air Slash 47, Lunge 53 | Masquerain |
| Lotad | surf | 25 | Oxide | Mist, Natural Gift, Mega Drain, BubbleBeam | nothing | Ludicolo (from 26) |
| Lotad | surf | 25 | Rewrite | Mist, Disarming Voice, Mega Drain, BubbleBeam | as Ludicolo: Energy Ball 34 | Ludicolo (from 26) |
| Quagsire | surf | 25 | Oxide | Mud Shot, Slam, Mud Bomb, Amnesia | Yawn 31, Earthquake 36, Mist 48, Haze 48, Muddy Water 53 | Quagsire |
| Quagsire | surf | 25 | Rewrite | Mud Shot, Slam, Mud Bomb, Amnesia | Trailblaze 27, Yawn 31, Earthquake 36, Rock Slide 39, Toxic 40, Drain Punch 44, Mist 48, Muddy Water 53 | Quagsire |
| Seel | surf | 26 | Oxide | Encore, Ice Shard, Rest, Aqua Ring | Aurora Beam 27, Aqua Jet 31, Brine 33; as Dewgong: Sheer Cold 34, Take Down 37, Dive 41, Aqua Tail 43, Ice Beam 47, Safeguard 51 | Dewgong (from 34) |
| Seel | surf | 26 | Rewrite | Encore, Ice Shard, Rest, Aqua Ring | Aurora Beam 27, Aqua Jet 31, Brine 33; as Dewgong: Signal Beam 34, Take Down 37, Drill Run 40, Dive 41, Aqua Tail 43, Ice Beam 47, Safeguard 51 | Dewgong (from 34) |
| Poliwhirl | surf | 28 | Oxide | Water Gun, DoubleSlap, Body Slam, BubbleBeam | as Poliwrath: DynamicPunch 43, Mind Reader 53 | Poliwrath (from 28) |
| Poliwhirl | surf | 28 | Oxide | Water Gun, DoubleSlap, Body Slam, BubbleBeam | as Politoed: Bounce 37, Hyper Voice 48 | Politoed (from 28) |
| Poliwhirl | surf | 28 | Rewrite | Body Slam, Bulldoze, BubbleBeam, Swagger | as Poliwrath: Liquidation 34, Brick Break 43, Mind Reader 53 | Poliwrath (from 28) |
| Poliwhirl | surf | 28 | Rewrite | Body Slam, Bulldoze, BubbleBeam, Swagger | as Politoed: Bounce 37, Hyper Voice 48 | Politoed (from 28) |

## Route 205

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 53 | At the cap |
|---|---|---|---|---|---|---|
| Buizel | surf | 22 | Oxide | Water Gun, Pursuit, Swift, Aqua Jet | as Floatzel: Crunch 26, Agility 29, Whirlpool 39, Razor Wind 50 | Floatzel (from 26) |
| Buizel | surf | 22 | Rewrite | Pursuit, Scary Face, Swift, Aqua Jet | as Floatzel: Crunch 26, Icy Wind 29, Flip Turn 33, Waterfall 36, Whirlpool 39, Liquidation 41, Low Sweep 44, Agility 51, Rock Tomb 53 | Floatzel (from 26) |
| Lotad | surf | 22 | Oxide | Nature Power, Mist, Natural Gift, Mega Drain | nothing | Ludicolo (from 23) |
| Lotad | surf | 22 | Rewrite | Water Gun, Mist, Disarming Voice, Mega Drain | as Ludicolo: Energy Ball 34 | Ludicolo (from 23) |
| Shellos | surf | 22 | Oxide | Harden, Water Pulse, Mud Bomb, Hidden Power | Body Slam 29; as Gastrodon: Muddy Water 41 | Gastrodon (from 30) |
| Shellos | surf | 22 | Rewrite | Water Pulse, Mud Bomb, Hidden Power, Swagger | Body Slam 29; as Gastrodon: AncientPower 33, Earth Power 35, Clear Smog 37, Muddy Water 41, Bulldoze 44, Sludge Bomb 46, Ice Beam 49 | Gastrodon (from 30) |
| Surskit | surf | 22 | Oxide | Bubble, Quick Attack, Sweet Scent, Water Sport | as Masquerain: Scary Face 26, Stun Spore 33, Silver Wind 40, Air Slash 47 | Masquerain (from 23) |
| Surskit | surf | 22 | Rewrite | Quick Attack, Gust, Silver Wind, Water Sport | as Masquerain: BubbleBeam 25, Scary Face 26, Mud Bomb 29, Stun Spore 33, Surf 36, Giga Drain 38, Silver Wind 40, Signal Beam 41, Icy Wind 43, Air Slash 47, Lunge 53 | Masquerain (from 23) |
| Frillish | surf | 25 | Oxide | Ominous Wind, Water Pulse, Imprison, Confuse Ray | Hex 30, Brine 34, Pain Split 39; as Jellicent: Destiny Bond 45, Shadow Ball 51 | Jellicent (from 40) |
| Frillish | surf | 25 | Rewrite | Ominous Wind, Water Pulse, Imprison, Confuse Ray | Hex 30, Brine 34, Dark Pulse 36, Pain Split 39; as Jellicent: Muddy Water 45, Shadow Ball 51 | Jellicent (from 40) |
| Lombre | surf | 25 | Oxide | Fake Out, Fury Swipes, Water Sport, BubbleBeam | nothing | Ludicolo (from 25) |
| Lombre | surf | 25 | Rewrite | Natural Gift, Water Sport, Swagger, BubbleBeam | as Ludicolo: Energy Ball 34 | Ludicolo (from 25) |
| Quagsire | surf | 25 | Oxide | Mud Shot, Slam, Mud Bomb, Amnesia | Yawn 31, Earthquake 36, Mist 48, Haze 48, Muddy Water 53 | Quagsire |
| Quagsire | surf | 25 | Rewrite | Mud Shot, Slam, Mud Bomb, Amnesia | Trailblaze 27, Yawn 31, Earthquake 36, Rock Slide 39, Toxic 40, Drain Punch 44, Mist 48, Muddy Water 53 | Quagsire |
| Froakie | surf | 28 | Oxide | Icy Wind, Faint Attack, Acrobatics, Low Kick | as Frogadier: Waterfall 30, Fling 35; as Greninja: Scald 37, Dark Pulse 40, Extrasensory 43, Sludge Wave 47, Gunk Shot 51 | Greninja (from 36) |
| Froakie | surf | 28 | Rewrite | Icy Wind, Faint Attack, Acrobatics, Low Kick | as Frogadier: Waterfall 30, Fling 35; as Greninja: Shadow Sneak 36, Scald 37, Dark Pulse 40, Extrasensory 43, Sludge Wave 47, Gunk Shot 51 | Greninja (from 36) |
| Poliwhirl | surf | 28 | Oxide | Water Gun, DoubleSlap, Body Slam, BubbleBeam | as Poliwrath: DynamicPunch 43, Mind Reader 53 | Poliwrath (from 28) |
| Poliwhirl | surf | 28 | Oxide | Water Gun, DoubleSlap, Body Slam, BubbleBeam | as Politoed: Bounce 37, Hyper Voice 48 | Politoed (from 28) |
| Poliwhirl | surf | 28 | Rewrite | Body Slam, Bulldoze, BubbleBeam, Swagger | as Poliwrath: Liquidation 34, Brick Break 43, Mind Reader 53 | Poliwrath (from 28) |
| Poliwhirl | surf | 28 | Rewrite | Body Slam, Bulldoze, BubbleBeam, Swagger | as Politoed: Bounce 37, Hyper Voice 48 | Politoed (from 28) |

## Route 208

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 53 | At the cap |
|---|---|---|---|---|---|---|
| Buizel | surf | 24 | Oxide | Water Gun, Pursuit, Swift, Aqua Jet | as Floatzel: Crunch 26, Agility 29, Whirlpool 39, Razor Wind 50 | Floatzel (from 26) |
| Buizel | surf | 24 | Rewrite | Pursuit, Scary Face, Swift, Aqua Jet | as Floatzel: Crunch 26, Icy Wind 29, Flip Turn 33, Waterfall 36, Whirlpool 39, Liquidation 41, Low Sweep 44, Agility 51, Rock Tomb 53 | Floatzel (from 26) |
| Floatzel | surf | 24 | Oxide | Water Gun, Pursuit, Swift, Aqua Jet | Crunch 26, Agility 29, Whirlpool 39, Razor Wind 50 | Floatzel |
| Floatzel | surf | 24 | Rewrite | Water Gun, Pursuit, Swift, Aqua Jet | Crunch 26, Icy Wind 29, Flip Turn 33, Waterfall 36, Whirlpool 39, Liquidation 41, Low Sweep 44, Agility 51, Rock Tomb 53 | Floatzel |
| Feebas | surf | 27 | Oxide | Splash, Tackle | Flail 30; as Milotic: Hydro Pump 37, Attract 41, Safeguard 45, Aqua Ring 49 | Milotic (from 30) |
| Feebas | surf | 27 | Rewrite | Tackle, Recover, Dragon Tail, Captivate | Flail 30; as Milotic: Twister 30, Recover 31, Aqua Tail 32, Aurora Beam 33, Dragon Pulse 35, Surf 37, Attract 41, Muddy Water 43, Safeguard 45, Aqua Ring 49 | Milotic (from 30) |
| Frillish | surf | 27 | Oxide | Ominous Wind, Water Pulse, Imprison, Confuse Ray | Hex 30, Brine 34, Pain Split 39; as Jellicent: Destiny Bond 45, Shadow Ball 51 | Jellicent (from 40) |
| Frillish | surf | 27 | Rewrite | Ominous Wind, Water Pulse, Imprison, Confuse Ray | Hex 30, Brine 34, Dark Pulse 36, Pain Split 39; as Jellicent: Muddy Water 45, Shadow Ball 51 | Jellicent (from 40) |
| Mareanie | surf | 30 | Oxide | Venoshock, Toxic Spikes, Recover, Spike Cannon | Pin Missile 34, Toxic 36; as Toxapex: Toxic 39, Venom Drench 42, Poison Jab 43, Liquidation 45 | Toxapex (from 38) |
| Mareanie | surf | 30 | Rewrite | Venoshock, Toxic Spikes, Recover, Spike Cannon | Pin Missile 34, Toxic 36, Muddy Water 38; as Toxapex: Venom Drench 42, Poison Jab 43, Liquidation 45, Lunge 53 | Toxapex (from 38) |

## Route 209

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 53 | At the cap |
|---|---|---|---|---|---|---|
| Floatzel | surf | 25 | Oxide | Water Gun, Pursuit, Swift, Aqua Jet | Crunch 26, Agility 29, Whirlpool 39, Razor Wind 50 | Floatzel |
| Floatzel | surf | 25 | Rewrite | Water Gun, Pursuit, Swift, Aqua Jet | Crunch 26, Icy Wind 29, Flip Turn 33, Waterfall 36, Whirlpool 39, Liquidation 41, Low Sweep 44, Agility 51, Rock Tomb 53 | Floatzel |
| Gastrodon | surf | 25 | Oxide | Harden, Water Pulse, Mud Bomb, Hidden Power | Body Slam 29, Muddy Water 41 | Gastrodon |
| Gastrodon | surf | 25 | Rewrite | Harden, Water Pulse, Mud Bomb, Hidden Power | Body Slam 29, AncientPower 33, Earth Power 35, Clear Smog 37, Muddy Water 41, Bulldoze 44, Sludge Bomb 46, Ice Beam 49 | Gastrodon |
| Buizel | surf | 28 | Oxide | Pursuit, Swift, Aqua Jet, Agility | as Floatzel: Agility 29, Whirlpool 39, Razor Wind 50 | Floatzel (from 29) |
| Buizel | surf | 28 | Rewrite | Pursuit, Scary Face, Swift, Aqua Jet | as Floatzel: Icy Wind 29, Flip Turn 33, Waterfall 36, Whirlpool 39, Liquidation 41, Low Sweep 44, Agility 51, Rock Tomb 53 | Floatzel (from 29) |
| Masquerain | surf | 28 | Oxide | Sweet Scent, Water Sport, Gust, Scary Face | Stun Spore 33, Silver Wind 40, Air Slash 47 | Masquerain |
| Masquerain | surf | 28 | Rewrite | Water Sport, Gust, BubbleBeam, Scary Face | Mud Bomb 29, Stun Spore 33, Surf 36, Giga Drain 38, Silver Wind 40, Signal Beam 41, Icy Wind 43, Air Slash 47, Lunge 53 | Masquerain |
| Frogadier | surf | 31 | Oxide | Faint Attack, Acrobatics, Low Kick, Waterfall | Fling 35; as Greninja: Scald 37, Dark Pulse 40, Extrasensory 43, Sludge Wave 47, Gunk Shot 51 | Greninja (from 36) |
| Frogadier | surf | 31 | Rewrite | Acrobatics, Low Kick, Scald, Waterfall | Fling 35; as Greninja: Shadow Sneak 36, Scald 37, Dark Pulse 40, Extrasensory 43, Sludge Wave 47, Gunk Shot 51 | Greninja (from 36) |

## Route 210

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 53 | At the cap |
|---|---|---|---|---|---|---|
| Barboach | old rod | 14 | Oxide | Mud Sport, Water Sport, Water Gun, Mud Bomb | Amnesia 18, Water Pulse 22, Magnitude 26; as Whiscash: Rest 33, Snore 33, Aqua Tail 39, Earthquake 45, Future Sight 51 | Whiscash (from 30) |
| Barboach | old rod | 14 | Rewrite | Scary Face, Water Sport, Water Gun, Mud Bomb | Amnesia 18, Rock Tomb 20, Water Pulse 22, Magnitude 26; as Whiscash: Bulldoze 30, Rest 33, Zen Headbutt 36, Aqua Tail 39, Earth Power 40, Wild Charge 42, Earthquake 45, Future Sight 51 | Whiscash (from 30) |
| Feebas | old rod | 14 | Oxide | Splash | Tackle 15, Flail 30; as Milotic: Hydro Pump 37, Attract 41, Safeguard 45, Aqua Ring 49 | Milotic (from 30) |
| Feebas | old rod | 14 | Rewrite | Whirlpool, Water Gun, Water Pulse | Tackle 15, Recover 21, Dragon Tail 24, Captivate 25, Flail 30; as Milotic: Twister 30, Recover 31, Aqua Tail 32, Aurora Beam 33, Dragon Pulse 35, Surf 37, Attract 41, Muddy Water 43, Safeguard 45, Aqua Ring 49 | Milotic (from 30) |
| Chinchou | old rod | 15 | Oxide | Supersonic, Thunder Wave, Flail, Water Gun | Confuse Ray 17, Spark 20, Take Down 23; as Lanturn: Stockpile 27, Swallow 27, Spit Up 27, BubbleBeam 30, Signal Beam 35, Discharge 40, Aqua Ring 47, Hydro Pump 52 | Lanturn (from 27) |
| Chinchou | old rod | 15 | Rewrite | Thunder Wave, Flail, Water Gun, Screech | Confuse Ray 17, Spark 20, Take Down 23, Icy Wind 26; as Lanturn: Stockpile 27, Swallow 28, Spit Up 29, BubbleBeam 30, Signal Beam 31, Scald 33, Surf 34, Thunderbolt 37, Discharge 40, Flash Cannon 43, Aqua Ring 47, Muddy Water 52 | Lanturn (from 27) |
| Corphish | old rod | 15 | Oxide | Bubble, Harden, ViceGrip, Leer | BubbleBeam 20, Protect 23, Knock Off 26; as Crawdaunt: Swift 30, Taunt 34, Night Slash 39, Crabhammer 44, Swords Dance 52 | Crawdaunt (from 30) |
| Corphish | old rod | 15 | Rewrite | Taunt, ViceGrip, BubbleBeam, Leer | Razor Shell 17, Knock Off 26; as Crawdaunt: Swift 30, Taunt 32, Throat Chop 35, Aerial Ace 36, Night Slash 39, X-Scissor 41, Crabhammer 44, Brick Break 48, Swords Dance 52 | Crawdaunt (from 30) |
| Finneon | old rod | 16 | Oxide | Pound, Water Gun, Attract | Gust 17, Water Pulse 22, Captivate 26, Safeguard 29; as Lumineon: Aqua Ring 35, Whirlpool 42, U-turn 48, Bounce 53 | Lumineon (from 31) |
| Finneon | old rod | 16 | Rewrite | Tailwind, Attract, Water Pulse, Pursuit | Gust 17, Captivate 26, Safeguard 29; as Lumineon: Flip Turn 31, Aqua Ring 33, Icy Wind 34, Aqua Tail 38, Signal Beam 40, Whirlpool 42, Ice Fang 45, U-turn 48, Bounce 53 | Lumineon (from 31) |
| Goldeen | good rod | 24 | Oxide | Supersonic, Horn Attack, Water Pulse, Flail | Aqua Ring 27, Fury Attack 31; as Seaking: Waterfall 40, Horn Drill 47 | Seaking (from 33) |
| Goldeen | good rod | 24 | Rewrite | Water Pulse, Horn Attack, Swagger, Flail | Aqua Ring 27; as Seaking: Aqua Jet 34, Skull Bash 37, Waterfall 40, Poison Jab 44, Drill Run 47, Knock Off 50 | Seaking (from 33) |
| Psyduck | good rod | 24 | Oxide | Water Gun, Disable, Confusion, Water Pulse | Fury Swipes 27, Screech 31; as Golduck: Psych Up 37, Zen Headbutt 44, Amnesia 50 | Golduck (from 33) |
| Psyduck | good rod | 24 | Rewrite | Water Pulse, Disable, Confusion, Low Sweep | Fury Swipes 27; as Golduck: Surf 34, Psych Up 37, Aurora Beam 40, Zen Headbutt 44, Power Gem 47, Amnesia 50 | Golduck (from 33) |
| Barboach | good rod | 26 | Oxide | Mud Bomb, Amnesia, Water Pulse, Magnitude | as Whiscash: Rest 33, Snore 33, Aqua Tail 39, Earthquake 45, Future Sight 51 | Whiscash (from 30) |
| Barboach | good rod | 26 | Rewrite | Amnesia, Rock Tomb, Water Pulse, Magnitude | as Whiscash: Bulldoze 30, Rest 33, Zen Headbutt 36, Aqua Tail 39, Earth Power 40, Wild Charge 42, Earthquake 45, Future Sight 51 | Whiscash (from 30) |
| Feebas | good rod | 26 | Oxide | Splash, Tackle | Flail 30; as Milotic: Hydro Pump 37, Attract 41, Safeguard 45, Aqua Ring 49 | Milotic (from 30) |
| Feebas | good rod | 26 | Rewrite | Tackle, Recover, Dragon Tail, Captivate | Flail 30; as Milotic: Twister 30, Recover 31, Aqua Tail 32, Aurora Beam 33, Dragon Pulse 35, Surf 37, Attract 41, Muddy Water 43, Safeguard 45, Aqua Ring 49 | Milotic (from 30) |
| Hawlucha | wild | 27 to 30 | Oxide | FeatherDance, Flying Press, Sky Drop, Submission | Tailwind 28, Dual Wingbeat 32, Fly 36, Hi Jump Kick 42, Me First 48 | Hawlucha |
| Hawlucha | wild | 27 to 30 | Rewrite | Encore, FeatherDance, Sky Drop, Flying Press | Tailwind 28, Dual Wingbeat 32, Fly 36, Hi Jump Kick 42, Air Slash 45, Lunge 48 | Hawlucha |
| Braixen | wild | 28 | Oxide | Role Play, Psybeam, Lucky Chant, Light Screen | Flame Burst 29, Psyshock 34; as Delphox: Mystical Fire 36, Hypnosis 40, Will-O-Wisp 45, Flamethrower 51 | Delphox (from 36) |
| Braixen | wild | 28 | Rewrite | Charm, Lucky Chant, Light Screen, Mystical Fire | Psyshock 34; as Delphox: Mystical Fire 36, Hypnosis 39, Mud Shot 41, Shadow Ball 42, Will-O-Wisp 45, Flamethrower 51 | Delphox (from 36) |
| Charcadet | wild | 28 | Oxide | Clear Smog, Fire Spin, Will-O-Wisp | as Armarouge: Incinerate 28, Lava Plume 32, Calm Mind 37, Ally Switch 42, Flamethrower 48 | Armarouge (from 28) |
| Charcadet | wild | 28 | Oxide | Clear Smog, Fire Spin, Will-O-Wisp | as Ceruledge: Incinerate 28, Lava Plume 32, Swords Dance 37, Ally Switch 42, Bitter Blade 48 | Ceruledge (from 28) |
| Charcadet | wild | 28 | Rewrite | Clear Smog, Fire Spin, Will-O-Wisp, Flame Charge | as Armarouge: Incinerate 28, Clear Smog 29, Fire Spin 30, Lava Plume 32, Calm Mind 37, Flamethrower 48, Psyshock 52 | Armarouge (from 28) |
| Charcadet | wild | 28 | Rewrite | Clear Smog, Fire Spin, Will-O-Wisp, Flame Charge | as Ceruledge: Incinerate 28, Bulldoze 29, Shadow Claw 30, Lava Plume 32, Swords Dance 40, Bitter Blade 48, Throat Chop 52 | Ceruledge (from 28) |
| Frogadier | good rod | 28 | Oxide | Icy Wind, Faint Attack, Acrobatics, Low Kick | Waterfall 30, Fling 35; as Greninja: Scald 37, Dark Pulse 40, Extrasensory 43, Sludge Wave 47, Gunk Shot 51 | Greninja (from 36) |
| Frogadier | good rod | 28 | Rewrite | Faint Attack, Acrobatics, Low Kick, Scald | Waterfall 30, Fling 35; as Greninja: Shadow Sneak 36, Scald 37, Dark Pulse 40, Extrasensory 43, Sludge Wave 47, Gunk Shot 51 | Greninja (from 36) |
| Houndoom | wild | 28 | Oxide | Smog, Roar, Bite, Odor Sleuth | Fire Fang 32, Faint Attack 38, Embargo 44, Flamethrower 48 | Houndoom |
| Houndoom | wild | 28 | Rewrite | Smog, Roar, Bite, Odor Sleuth | Fire Fang 32, Fire Pledge 35, Faint Attack 38, Mud Shot 41, Embargo 44, Flamethrower 48, Dark Pulse 51 | Houndoom |
| Scyther | wild | 28 | Oxide | False Swipe, Agility, Wing Attack, Fury Cutter | as Scizor: Slash 29, Razor Wind 33, Iron Defense 37, X-Scissor 41, Night Slash 45, Double Hit 49, Iron Head 53 | Scizor (from 28) |
| Scyther | wild | 28 | Oxide | False Swipe, Agility, Wing Attack, Fury Cutter | as Kleavor: Dual Wingbeat 28, Rock Blast 32, X-Scissor 36, Superpower 40, Acrobatics 44, Stone Edge 48, Leech Life 51, Close Combat 53 | Kleavor (from 28) |
| Scyther | wild | 28 | Rewrite | False Swipe, Agility, Wing Attack, Fury Cutter | as Scizor: Slash 29, Skitter Smack 34, Iron Defense 37, X-Scissor 41, Night Slash 45, Double Hit 49, Iron Head 53 | Scizor (from 28) |
| Scyther | wild | 28 | Rewrite | False Swipe, Agility, Wing Attack, Fury Cutter | as Kleavor: Dual Wingbeat 28, Rock Blast 32, Rock Slide 35, X-Scissor 36, Superpower 40, Acrobatics 44, Stone Edge 48, Leech Life 51, Close Combat 53 | Kleavor (from 28) |
| Sneasel | wild | 28 | Oxide | Faint Attack, Fury Swipes, Agility, Icy Wind | Slash 35, Metal Claw 42, Ice Shard 49 | Sneasel; Weavile in HQ |
| Sneasel | wild | 28 | Rewrite | Fury Swipes, Nasty Plot, Agility, Icy Wind | Slash 35, Low Sweep 38, Poison Jab 40, Metal Claw 42, Ice Shard 49, Ice Fang 53 | Sneasel; Weavile in HQ |
| Swablu | wild | 28 | Oxide | Fury Attack, Safeguard, Mist, Take Down | Natural Gift 32; as Altaria: DragonBreath 35, Dragon Dance 39, Refresh 46 | Altaria (from 35) |
| Swablu | wild | 28 | Rewrite | Dragon Dance, Mist, Air Slash, Take Down | Natural Gift 32, Play Rough 34, Steel Wing 35; as Altaria: DragonBreath 35, Mirror Move 36, Bulldoze 40, Breaking Swipe 43, Refresh 46, Moonblast 50 | Altaria (from 35) |
| Bronzor | wild | 29 to 30 | Oxide | Imprison, Confuse Ray, Extrasensory, Iron Defense | Safeguard 30; as Bronzong: Block 33, Gyro Ball 38, Future Sight 43, Faint Attack 50 | Bronzong (from 33) |
| Bronzor | wild | 29 to 30 | Rewrite | Smart Strike, Extrasensory, Bulldoze, Iron Defense | Safeguard 30; as Bronzong: Block 33, Iron Head 35, Gyro Ball 38, Rock Tomb 40, Future Sight 43, Body Press 46, Faint Attack 50 | Bronzong (from 33) |
| Mienfoo | wild | 29 | Oxide | DoubleSlap, Force Palm, Bounce, Drain Punch | Vacuum Wave 32; as Mienshao: Aura Sphere 38, Me First 40, Jump Kick 45, Dual Chop 48, Focus Blast 51 | Mienshao (from 36) |
| Mienfoo | wild | 29 | Rewrite | Force Palm, Bounce, Drain Punch, Low Sweep | Vacuum Wave 32; as Mienshao: Aura Sphere 38, U-turn 41, Rock Tomb 43, Jump Kick 45, Dual Chop 48, Focus Blast 51 | Mienshao (from 36) |
| Turtonator | wild | 29 to 30 | Oxide | Endure, Incinerate, Dragon Tail, Rapid Spin | Body Slam 33, Flamethrower 38, Dragon Pulse 43, Fire Spin 47 | Turtonator |
| Turtonator | wild | 29 to 30 | Rewrite | Endure, Incinerate, Dragon Tail, Rapid Spin | Body Slam 33, Flamethrower 38, Dragon Pulse 43, Shell Smash 45, Fire Spin 47, Body Press 53 | Turtonator |
| Goldeen | surf | 30 | Oxide | Horn Attack, Water Pulse, Flail, Aqua Ring | Fury Attack 31; as Seaking: Waterfall 40, Horn Drill 47 | Seaking (from 33) |
| Goldeen | surf | 30 | Rewrite | Horn Attack, Swagger, Flail, Aqua Ring | as Seaking: Aqua Jet 34, Skull Bash 37, Waterfall 40, Poison Jab 44, Drill Run 47, Knock Off 50 | Seaking (from 33) |
| Jellicent | surf | 30 | Oxide | Water Pulse, Imprison, Confuse Ray, Hex | Brine 34, Pain Split 39, Destiny Bond 45, Shadow Ball 51 | Jellicent |
| Jellicent | surf | 30 | Rewrite | Water Pulse, Imprison, Confuse Ray, Hex | Brine 34, Pain Split 39, Muddy Water 45, Shadow Ball 51 | Jellicent |
| Buizel | surf | 33 | Oxide | Pursuit, Swift, Aqua Jet, Agility | as Floatzel: Whirlpool 39, Razor Wind 50 | Floatzel (from 34) |
| Buizel | surf | 33 | Rewrite | Pursuit, Scary Face, Swift, Aqua Jet | as Floatzel: Waterfall 36, Whirlpool 39, Liquidation 41, Low Sweep 44, Agility 51, Rock Tomb 53 | Floatzel (from 34) |
| Floatzel | surf | 33 | Oxide | Swift, Aqua Jet, Crunch, Agility | Whirlpool 39, Razor Wind 50 | Floatzel |
| Floatzel | surf | 33 | Rewrite | Aqua Jet, Crunch, Icy Wind, Flip Turn | Waterfall 36, Whirlpool 39, Liquidation 41, Low Sweep 44, Agility 51, Rock Tomb 53 | Floatzel |
| Frogadier | surf | 36 | Oxide | Acrobatics, Low Kick, Waterfall, Fling | as Greninja: Scald 37, Dark Pulse 40, Extrasensory 43, Sludge Wave 47, Gunk Shot 51 | Greninja (from 37) |
| Frogadier | surf | 36 | Rewrite | Low Kick, Scald, Waterfall, Fling | as Greninja: Scald 37, Dark Pulse 40, Extrasensory 43, Sludge Wave 47, Gunk Shot 51 | Greninja (from 37) |

## Route 211

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 53 | At the cap |
|---|---|---|---|---|---|---|
| Kirlia | wild | 27 to 30 | Oxide | Teleport, Lucky Chant, Magical Leaf, Calm Mind | as Gardevoir: Psychic 33, Imprison 40, Future Sight 45, Captivate 53 | Gardevoir (from 30) |
| Kirlia | wild | 27 to 30 | Oxide | Teleport, Lucky Chant, Magical Leaf, Calm Mind | as Gallade: Psycho Cut 31, Helping Hand 36, Feint 39, False Swipe 45, Protect 50, Close Combat 53 | Gallade (from 27) |
| Kirlia | wild | 27 to 30 | Rewrite | Confusion, Lucky Chant, Magical Leaf, Calm Mind | as Gardevoir: Wish 30, Psychic 33, Icy Wind 36, Charge Beam 38, Imprison 40, Mystical Fire 42, Future Sight 45, Captivate 53 | Gardevoir (from 30) |
| Kirlia | wild | 27 to 30 | Rewrite | Confusion, Lucky Chant, Magical Leaf, Calm Mind | as Gallade: Psycho Cut 31, Helping Hand 36, False Swipe 45, Close Combat 53 | Gallade (from 27) |
| Bronzor | wild | 28 | Oxide | Imprison, Confuse Ray, Extrasensory, Iron Defense | Safeguard 30; as Bronzong: Block 33, Gyro Ball 38, Future Sight 43, Faint Attack 50 | Bronzong (from 33) |
| Bronzor | wild | 28 | Rewrite | Smart Strike, Extrasensory, Bulldoze, Iron Defense | Safeguard 30; as Bronzong: Block 33, Iron Head 35, Gyro Ball 38, Rock Tomb 40, Future Sight 43, Body Press 46, Faint Attack 50 | Bronzong (from 33) |
| Dartrix | wild | 28 | Oxide | Razor Leaf, Pluck, Ominous Wind, Synthesis | Seed Bomb 32, Sucker Punch 36; as Decidueye: Sucker Punch 38, FeatherDance 48, Roost 51 | Decidueye (from 36) |
| Dartrix | wild | 28 | Rewrite | Razor Leaf, Pluck, Ominous Wind, Synthesis | Seed Bomb 32; as Decidueye: Spirit Shackle 36, Sucker Punch 38, U-turn 41, Low Sweep 44, FeatherDance 48, Roost 51 | Decidueye (from 36) |
| Ferroseed | wild | 28 | Oxide | Pin Missile, Metal Claw, Ingrain, Payback | Bullet Seed 30, Gyro Ball 35, Selfdestruct 38; as Ferrothorn: Knock Off 44, Seed Bomb 48, Iron Head 51 | Ferrothorn (from 40) |
| Ferroseed | wild | 28 | Rewrite | Assurance, Pin Missile, Metal Claw, Payback | Bullet Seed 30, Iron Defense 34, Gyro Ball 35, Seed Bomb 40; as Ferrothorn: Knock Off 44, Bulldoze 46, Seed Bomb 48, Iron Head 51 | Ferrothorn (from 40) |
| Mienfoo | wild | 28 | Oxide | DoubleSlap, Force Palm, Bounce, Drain Punch | Vacuum Wave 32; as Mienshao: Aura Sphere 38, Me First 40, Jump Kick 45, Dual Chop 48, Focus Blast 51 | Mienshao (from 36) |
| Mienfoo | wild | 28 | Rewrite | Force Palm, Bounce, Drain Punch, Low Sweep | Vacuum Wave 32; as Mienshao: Aura Sphere 38, U-turn 41, Rock Tomb 43, Jump Kick 45, Dual Chop 48, Focus Blast 51 | Mienshao (from 36) |
| Naclstack | wild | 28 | Oxide | Smack Down, Rock Polish, Headbutt, Iron Defense | Recover 30, Rock Slide 34, Stealth Rock 38; as Garganacl: Stealth Rock 40, Heavy Slam 44, Earthquake 49 | Garganacl (from 38) |
| Naclstack | wild | 28 | Rewrite | Iron Defense, Bulldoze, Recover, Rock Polish | Rock Tomb 32, Rock Slide 34, Stealth Rock 38; as Garganacl: Rock Tomb 38, Salt Cure 39, Stealth Rock 40, Iron Head 42, Heavy Slam 44, Zen Headbutt 46, Earthquake 49 | Garganacl (from 38) |
| Sneasel | wild | 28 | Oxide | Faint Attack, Fury Swipes, Agility, Icy Wind | Slash 35, Metal Claw 42, Ice Shard 49 | Sneasel; Weavile in HQ |
| Sneasel | wild | 28 | Rewrite | Fury Swipes, Nasty Plot, Agility, Icy Wind | Slash 35, Low Sweep 38, Poison Jab 40, Metal Claw 42, Ice Shard 49, Ice Fang 53 | Sneasel; Weavile in HQ |
| Turtonator | wild | 28 to 29 | Oxide | Endure, Incinerate, Dragon Tail, Rapid Spin | Body Slam 33, Flamethrower 38, Dragon Pulse 43, Fire Spin 47 | Turtonator |
| Turtonator | wild | 28 to 29 | Rewrite | Endure, Incinerate, Dragon Tail, Rapid Spin | Body Slam 33, Flamethrower 38, Dragon Pulse 43, Shell Smash 45, Fire Spin 47, Body Press 53 | Turtonator |
| Gligar | wild | 29 to 30 | Oxide | Quick Attack, Fury Cutter, Faint Attack, Screech | as Gliscor: Night Slash 31, Swords Dance 34, U-turn 38, X-Scissor 42, Guillotine 45 | Gliscor (from 29) |
| Gligar | wild | 29 to 30 | Rewrite | Rock Tomb, Fury Cutter, Faint Attack, Screech | as Gliscor: Night Slash 31, Swords Dance 34, U-turn 38, X-Scissor 42 | Gliscor (from 29) |
| Jangmo-O | wild | 29 to 30 | Oxide | Headbutt, Dragon Tail, Scary Face, Counter | Dragon Claw 33; as Hakamo-O: Sky Uppercut 36, Roar 39, Noble Roar 44; as Kommo-O: Clanging Scales 47, Scale Shot 52 | Kommo-O (from 45) |
| Jangmo-O | wild | 29 to 30 | Rewrite | Headbutt, Dragon Tail, Scary Face, Counter | Sky Uppercut 31, Dragon Claw 33; as Hakamo-O: Sky Uppercut 36, Noble Roar 44, Throat Chop 45; as Kommo-O: Clanging Scales 47, Scale Shot 52 | Kommo-O (from 45) |

## Route 212

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 53 | At the cap |
|---|---|---|---|---|---|---|
| Floatzel | surf | 28 | Oxide | Pursuit, Swift, Aqua Jet, Crunch | Agility 29, Whirlpool 39, Razor Wind 50 | Floatzel |
| Floatzel | surf | 28 | Rewrite | Pursuit, Swift, Aqua Jet, Crunch | Icy Wind 29, Flip Turn 33, Waterfall 36, Whirlpool 39, Liquidation 41, Low Sweep 44, Agility 51, Rock Tomb 53 | Floatzel |
| Gastrodon | surf | 28 | Oxide | Harden, Water Pulse, Mud Bomb, Hidden Power | Body Slam 29, Muddy Water 41 | Gastrodon |
| Gastrodon | surf | 28 | Rewrite | Harden, Water Pulse, Mud Bomb, Hidden Power | Body Slam 29, AncientPower 33, Earth Power 35, Clear Smog 37, Muddy Water 41, Bulldoze 44, Sludge Bomb 46, Ice Beam 49 | Gastrodon |
| Lombre | surf | 28 | Oxide | Fake Out, Fury Swipes, Water Sport, BubbleBeam | nothing | Ludicolo (from 28) |
| Lombre | surf | 28 | Rewrite | Water Sport, Swagger, BubbleBeam, Giga Drain | as Ludicolo: Energy Ball 34 | Ludicolo (from 28) |
| Wooper | surf | 28 | Oxide | Mud Shot, Slam, Mud Bomb, Amnesia | Yawn 29; as Quagsire: Yawn 31, Earthquake 36, Mist 48, Haze 48, Muddy Water 53 | Quagsire (from 29) |
| Wooper | surf | 28 | Oxide | Mud Shot, Slam, Mud Bomb, Amnesia | as Clodsire: Poison Jab 30, Megahorn 36, Toxic 40, Earthquake 48 | Clodsire (from 28) |
| Wooper | surf | 28 | Rewrite | Poison Sting, Mud Shot, Slam, Mud Bomb | as Quagsire: Yawn 31, Earthquake 36, Rock Slide 39, Toxic 40, Drain Punch 44, Mist 48, Muddy Water 53 | Quagsire (from 29) |
| Wooper | surf | 28 | Rewrite | Poison Sting, Mud Shot, Slam, Mud Bomb | as Clodsire: Poison Jab 30, Waterfall 34, Megahorn 36, Toxic 40, Drain Punch 44, Earthquake 48, Aqua Tail 51 | Clodsire (from 28) |
| Araquanid | surf | 31 | Oxide | BubbleBeam, Bug Bite, Headbutt, Soak | Dive 36, Lunge 41, Scald 48, Hydro Pump 51 | Araquanid |
| Araquanid | surf | 31 | Rewrite | Bug Bite, Headbutt, Spider Web, Soak | Skitter Smack 34, Dive 36, Waterfall 38, Lunge 41, Poison Jab 44, Scald 48, Surf 51 | Araquanid |
| Buizel | surf | 31 | Oxide | Pursuit, Swift, Aqua Jet, Agility | as Floatzel: Whirlpool 39, Razor Wind 50 | Floatzel (from 32) |
| Buizel | surf | 31 | Rewrite | Pursuit, Scary Face, Swift, Aqua Jet | as Floatzel: Flip Turn 33, Waterfall 36, Whirlpool 39, Liquidation 41, Low Sweep 44, Agility 51, Rock Tomb 53 | Floatzel (from 32) |
| Masquerain | surf | 31 | Oxide | Sweet Scent, Water Sport, Gust, Scary Face | Stun Spore 33, Silver Wind 40, Air Slash 47 | Masquerain |
| Masquerain | surf | 31 | Rewrite | Gust, BubbleBeam, Scary Face, Mud Bomb | Stun Spore 33, Surf 36, Giga Drain 38, Silver Wind 40, Signal Beam 41, Icy Wind 43, Air Slash 47, Lunge 53 | Masquerain |
| Alomomola | surf | 34 | Oxide | Protect, Water Pulse, Wake-Up Slap, Soak | Wish 37, Brine 41, Safeguard 45, Whirlpool 49, Helping Hand 53 | Alomomola |
| Alomomola | surf | 34 | Rewrite | Heal Pulse, Wake-Up Slap, Water Pulse, Soak | Play Rough 35, Wish 37, Brine 41, Zen Headbutt 43, Safeguard 45, Whirlpool 49, Helping Hand 53 | Alomomola |
| Frillish | surf | 34 | Oxide | Imprison, Confuse Ray, Hex, Brine | Pain Split 39; as Jellicent: Destiny Bond 45, Shadow Ball 51 | Jellicent (from 40) |
| Frillish | surf | 34 | Rewrite | Imprison, Confuse Ray, Hex, Brine | Dark Pulse 36, Pain Split 39; as Jellicent: Muddy Water 45, Shadow Ball 51 | Jellicent (from 40) |

## Route 213

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 53 | At the cap |
|---|---|---|---|---|---|---|
| Mantyke | surf | 28 | Oxide | Headbutt, Agility, Wing Attack, Water Pulse | as Mantine: Take Down 31, Confuse Ray 37, Bounce 40, Aqua Ring 46, Hydro Pump 49 | Mantine (from 30) |
| Mantyke | surf | 28 | Rewrite | Agility, Wing Attack, Icy Wind, Water Pulse | as Mantine: Take Down 31, Scald 34, Confuse Ray 37, Bounce 40, Psybeam 41, Signal Beam 43, Aqua Ring 46, Surf 49 | Mantine (from 30) |
| Tentacool | surf | 28 | Oxide | Toxic Spikes, BubbleBeam, Wrap, Barrier | Water Pulse 29; as Tentacruel: Poison Jab 36, Screech 42, Hydro Pump 49 | Tentacruel (from 30) |
| Tentacool | surf | 28 | Rewrite | Toxic Spikes, Water Pulse, BubbleBeam, Barrier | as Tentacruel: Poison Jab 33, Aurora Beam 34, Sludge Bomb 39, Screech 42, Psybeam 44, Surf 49, Muddy Water 53 | Tentacruel (from 30) |
| Frillish | surf | 31 | Oxide | Water Pulse, Imprison, Confuse Ray, Hex | Brine 34, Pain Split 39; as Jellicent: Destiny Bond 45, Shadow Ball 51 | Jellicent (from 40) |
| Frillish | surf | 31 | Rewrite | Water Pulse, Imprison, Confuse Ray, Hex | Brine 34, Dark Pulse 36, Pain Split 39; as Jellicent: Muddy Water 45, Shadow Ball 51 | Jellicent (from 40) |
| Shellos | surf | 31 | Oxide | Water Pulse, Mud Bomb, Hidden Power, Body Slam | as Gastrodon: Muddy Water 41 | Gastrodon (from 32) |
| Shellos | surf | 31 | Rewrite | Mud Bomb, Hidden Power, Swagger, Body Slam | as Gastrodon: AncientPower 33, Earth Power 35, Clear Smog 37, Muddy Water 41, Bulldoze 44, Sludge Bomb 46, Ice Beam 49 | Gastrodon (from 32) |
| Araquanid | surf | 34 | Oxide | BubbleBeam, Bug Bite, Headbutt, Soak | Dive 36, Lunge 41, Scald 48, Hydro Pump 51 | Araquanid |
| Araquanid | surf | 34 | Rewrite | Headbutt, Spider Web, Soak, Skitter Smack | Dive 36, Waterfall 38, Lunge 41, Poison Jab 44, Scald 48, Surf 51 | Araquanid |

## Route 214

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 53 | At the cap |
|---|---|---|---|---|---|---|
| Gastrodon | surf | 28 | Oxide | Harden, Water Pulse, Mud Bomb, Hidden Power | Body Slam 29, Muddy Water 41 | Gastrodon |
| Gastrodon | surf | 28 | Rewrite | Harden, Water Pulse, Mud Bomb, Hidden Power | Body Slam 29, AncientPower 33, Earth Power 35, Clear Smog 37, Muddy Water 41, Bulldoze 44, Sludge Bomb 46, Ice Beam 49 | Gastrodon |
| Masquerain | surf | 28 | Oxide | Sweet Scent, Water Sport, Gust, Scary Face | Stun Spore 33, Silver Wind 40, Air Slash 47 | Masquerain |
| Masquerain | surf | 28 | Rewrite | Water Sport, Gust, BubbleBeam, Scary Face | Mud Bomb 29, Stun Spore 33, Surf 36, Giga Drain 38, Silver Wind 40, Signal Beam 41, Icy Wind 43, Air Slash 47, Lunge 53 | Masquerain |
| Floatzel | surf | 31 | Oxide | Swift, Aqua Jet, Crunch, Agility | Whirlpool 39, Razor Wind 50 | Floatzel |
| Floatzel | surf | 31 | Rewrite | Swift, Aqua Jet, Crunch, Icy Wind | Flip Turn 33, Waterfall 36, Whirlpool 39, Liquidation 41, Low Sweep 44, Agility 51, Rock Tomb 53 | Floatzel |
| Shellos | surf | 31 | Oxide | Water Pulse, Mud Bomb, Hidden Power, Body Slam | as Gastrodon: Muddy Water 41 | Gastrodon (from 32) |
| Shellos | surf | 31 | Rewrite | Mud Bomb, Hidden Power, Swagger, Body Slam | as Gastrodon: AncientPower 33, Earth Power 35, Clear Smog 37, Muddy Water 41, Bulldoze 44, Sludge Bomb 46, Ice Beam 49 | Gastrodon (from 32) |
| Feraligatr | surf | 34 | Oxide | Ice Fang, Flail, Agility, Crunch | Slash 37, Screech 45, Thrash 50 | Feraligatr |
| Feraligatr | surf | 34 | Rewrite | Flail, Agility, Crunch, Slash | Bulldoze 35, Metal Claw 39, Aqua Jet 40, Liquidation 42, Screech 45, Thrash 50 | Feraligatr |

## Route 218

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 53 | At the cap |
|---|---|---|---|---|---|---|
| Galarian Mr Mime | wild | 28 to 31 | Oxide | Ally Switch, Icy Wind, Double Kick, Psybeam | Hypnosis 32, Mirror Coat 36, Sucker Punch 40; as Mr. Rime: Freeze-Dry 44, Psychic 48, Teeter Dance 52 | Mr. Rime (from 42) |
| Galarian Mr Mime | wild | 28 to 31 | Rewrite | Confusion, Icy Wind, Double Kick, Psybeam | Hypnosis 32, Mirror Coat 36, Sucker Punch 40, Dazzling Gleam 42; as Mr. Rime: Freeze-Dry 44, Psychic 48, Teeter Dance 52 | Mr. Rime (from 42) |
| Araquanid | wild | 29 to 30 | Oxide | Aqua Ring, BubbleBeam, Bug Bite, Headbutt | Soak 31, Dive 36, Lunge 41, Scald 48, Hydro Pump 51 | Araquanid |
| Araquanid | wild | 29 to 30 | Rewrite | BubbleBeam, Bug Bite, Headbutt, Spider Web | Soak 31, Skitter Smack 34, Dive 36, Waterfall 38, Lunge 41, Poison Jab 44, Scald 48, Surf 51 | Araquanid |
| Fletchinder | wild | 29 | Oxide | Aerial Ace, Flame Charge, Roost, Will-O-Wisp | Natural Gift 31; as Talonflame: Acrobatics 38, Me First 42, Tailwind 46, Flare Blitz 51 | Talonflame (from 36) |
| Fletchinder | wild | 29 | Rewrite | Flame Charge, Bite, Roost, Will-O-Wisp | Natural Gift 31; as Talonflame: Acrobatics 38, Steel Wing 40, Flamethrower 42, Tailwind 46, Upper Hand 48, Flare Blitz 51 | Talonflame (from 36) |
| Glameow | wild | 29 | Oxide | Faint Attack, Fury Swipes, Charm, Assist | Captivate 32, Slash 37; as Purugly: Swagger 38, Body Slam 45, Attract 53 | Purugly (from 38) |
| Glameow | wild | 29 | Rewrite | Fury Swipes, Retaliate, Charm, Aerial Ace | Captivate 32, Slash 37; as Purugly: Swagger 38, Strength 39, Metal Claw 40, Shadow Claw 42, Body Slam 45, Attract 53 | Purugly (from 38) |
| Liepard | wild | 29 to 31 | Oxide | Torment, Fake Out, Assurance, Hone Claws | Slash 34, Taunt 38, Sucker Punch 43, Nasty Plot 44, Night Slash 44, Snatch 47 | Liepard |
| Liepard | wild | 29 to 31 | Rewrite | Trailblaze, Fake Out, Hone Claws, Assurance | Dark Pulse 30, Nasty Plot 32, Slash 34, Throat Chop 36, Taunt 38, Sucker Punch 43, Night Slash 44, Snatch 47, Skitter Smack 50 | Liepard |
| Minccino | wild | 29 | Oxide | Encore, Charm, Tickle, Tail Slap | nothing | Cinccino (from 29) |
| Minccino | wild | 29 | Rewrite | Charm, Tickle, Strength, Tail Slap | nothing | Cinccino (from 29) |
| Quagsire | wild | 29 to 30 | Oxide | Mud Shot, Slam, Mud Bomb, Amnesia | Yawn 31, Earthquake 36, Mist 48, Haze 48, Muddy Water 53 | Quagsire |
| Quagsire | wild | 29 to 30 | Rewrite | Slam, Mud Bomb, Amnesia, Trailblaze | Yawn 31, Earthquake 36, Rock Slide 39, Toxic 40, Drain Punch 44, Mist 48, Muddy Water 53 | Quagsire |
| Toucannon | wild | 29 | Oxide | Supersonic, Pluck, Roost, Fury Attack | Screech 30, Drill Peck 34, Bullet Seed 40, FeatherDance 44, Hyper Voice 50 | Toucannon |
| Toucannon | wild | 29 | Rewrite | Echoed Voice, Supersonic, Pluck, Roost | Screech 30, Drill Peck 32, Smack Down 35, Facade 37, Bullet Seed 40, Throat Chop 42, FeatherDance 44, Take Down 47, Hyper Voice 50 | Toucannon |
| Chatot | wild | 30 | Oxide | Fury Attack, Chatter, Taunt, Mimic | Roost 33, Uproar 37, FeatherDance 41, Hyper Voice 45 | Chatot |
| Chatot | wild | 30 | Rewrite | Sing, Chatter, Taunt, Mimic | Roost 33, Round 34, Uproar 37, U-turn 39, FeatherDance 41, Air Slash 43, Hyper Voice 45, Steel Wing 53 | Chatot |
| Floatzel | surf | 30 | Oxide | Swift, Aqua Jet, Crunch, Agility | Whirlpool 39, Razor Wind 50 | Floatzel |
| Floatzel | surf | 30 | Rewrite | Swift, Aqua Jet, Crunch, Icy Wind | Flip Turn 33, Waterfall 36, Whirlpool 39, Liquidation 41, Low Sweep 44, Agility 51, Rock Tomb 53 | Floatzel |
| Floatzel | wild | 30 | Oxide | Swift, Aqua Jet, Crunch, Agility | Whirlpool 39, Razor Wind 50 | Floatzel |
| Floatzel | wild | 30 | Rewrite | Swift, Aqua Jet, Crunch, Icy Wind | Flip Turn 33, Waterfall 36, Whirlpool 39, Liquidation 41, Low Sweep 44, Agility 51, Rock Tomb 53 | Floatzel |
| Tentacool | surf | 30 | Oxide | BubbleBeam, Wrap, Barrier, Water Pulse | as Tentacruel: Poison Jab 36, Screech 42, Hydro Pump 49 | Tentacruel (from 31) |
| Tentacool | surf | 30 | Rewrite | Toxic Spikes, Water Pulse, BubbleBeam, Barrier | as Tentacruel: Poison Jab 33, Aurora Beam 34, Sludge Bomb 39, Screech 42, Psybeam 44, Surf 49, Muddy Water 53 | Tentacruel (from 31) |
| Shellos | wild | 31 | Oxide | Water Pulse, Mud Bomb, Hidden Power, Body Slam | as Gastrodon: Muddy Water 41 | Gastrodon (from 32) |
| Shellos | wild | 31 | Rewrite | Mud Bomb, Hidden Power, Swagger, Body Slam | as Gastrodon: AncientPower 33, Earth Power 35, Clear Smog 37, Muddy Water 41, Bulldoze 44, Sludge Bomb 46, Ice Beam 49 | Gastrodon (from 32) |
| Mantine | surf | 33 | Oxide | Agility, Wing Attack, Water Pulse, Take Down | Confuse Ray 37, Bounce 40, Aqua Ring 46, Hydro Pump 49 | Mantine |
| Mantine | surf | 33 | Rewrite | Agility, Wing Attack, Water Pulse, Take Down | Scald 34, Confuse Ray 37, Bounce 40, Psybeam 41, Signal Beam 43, Aqua Ring 46, Surf 49 | Mantine |
| Tentacruel | surf | 33 | Oxide | BubbleBeam, Wrap, Barrier, Water Pulse | Poison Jab 36, Screech 42, Hydro Pump 49 | Tentacruel |
| Tentacruel | surf | 33 | Rewrite | BubbleBeam, Barrier, Water Pulse, Poison Jab | Aurora Beam 34, Sludge Bomb 39, Screech 42, Psybeam 44, Surf 49, Muddy Water 53 | Tentacruel |
| Lanturn | surf | 36 | Oxide | Swallow, Spit Up, BubbleBeam, Signal Beam | Discharge 40, Aqua Ring 47, Hydro Pump 52 | Lanturn |
| Lanturn | surf | 36 | Rewrite | BubbleBeam, Signal Beam, Scald, Surf | Thunderbolt 37, Discharge 40, Flash Cannon 43, Aqua Ring 47, Muddy Water 52 | Lanturn |

## Route 219

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 53 | At the cap |
|---|---|---|---|---|---|---|
| Mantyke | surf | 20 | Oxide | Supersonic, BubbleBeam, Headbutt, Agility | Wing Attack 22, Water Pulse 28; as Mantine: Take Down 31, Confuse Ray 37, Bounce 40, Aqua Ring 46, Hydro Pump 49 | Mantine (from 30) |
| Mantyke | surf | 20 | Rewrite | Bubble, BubbleBeam, Headbutt, Agility | Wing Attack 22, Icy Wind 25, Water Pulse 28; as Mantine: Take Down 31, Scald 34, Confuse Ray 37, Bounce 40, Psybeam 41, Signal Beam 43, Aqua Ring 46, Surf 49 | Mantine (from 30) |
| Wingull | surf | 20 | Oxide | Supersonic, Wing Attack, Mist, Water Pulse | Quick Attack 24; as Pelipper: Protect 25, Roost 31, Stockpile 38, Swallow 38, Spit Up 38, Fling 43, Tailwind 50 | Pelipper (from 25) |
| Wingull | surf | 20 | Rewrite | Twister, Wing Attack, Tailwind, Water Pulse | Quick Attack 24; as Pelipper: Payback 25, Liquidation 28, Roost 31, Surf 34, Swallow 37, Stockpile 38, Spit Up 39, Icy Wind 40, Fling 43, Air Slash 47, Tailwind 50, Brave Bird 53 | Pelipper (from 25) |
| Gastrodon | surf | 23 | Oxide | Harden, Water Pulse, Mud Bomb, Hidden Power | Body Slam 29, Muddy Water 41 | Gastrodon |
| Gastrodon | surf | 23 | Rewrite | Harden, Water Pulse, Mud Bomb, Hidden Power | Body Slam 29, AncientPower 33, Earth Power 35, Clear Smog 37, Muddy Water 41, Bulldoze 44, Sludge Bomb 46, Ice Beam 49 | Gastrodon |
| Tentacool | surf | 23 to 26 | Oxide | Acid, Toxic Spikes, BubbleBeam, Wrap | Barrier 26, Water Pulse 29; as Tentacruel: Poison Jab 36, Screech 42, Hydro Pump 49 | Tentacruel (from 30) |
| Tentacool | surf | 23 to 26 | Rewrite | Acid, Toxic Spikes, Water Pulse, BubbleBeam | Barrier 26; as Tentacruel: Poison Jab 33, Aurora Beam 34, Sludge Bomb 39, Screech 42, Psybeam 44, Surf 49, Muddy Water 53 | Tentacruel (from 30) |

## Route 220

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 53 | At the cap |
|---|---|---|---|---|---|---|
| Chinchou | old rod | 14 | Oxide | Supersonic, Thunder Wave, Flail, Water Gun | Confuse Ray 17, Spark 20, Take Down 23; as Lanturn: Stockpile 27, Swallow 27, Spit Up 27, BubbleBeam 30, Signal Beam 35, Discharge 40, Aqua Ring 47, Hydro Pump 52 | Lanturn (from 27) |
| Chinchou | old rod | 14 | Rewrite | Thunder Wave, Flail, Water Gun, Screech | Confuse Ray 17, Spark 20, Take Down 23, Icy Wind 26; as Lanturn: Stockpile 27, Swallow 28, Spit Up 29, BubbleBeam 30, Signal Beam 31, Scald 33, Surf 34, Thunderbolt 37, Discharge 40, Flash Cannon 43, Aqua Ring 47, Muddy Water 52 | Lanturn (from 27) |
| Mantyke | old rod | 14 | Oxide | Bubble, Supersonic, BubbleBeam, Headbutt | Agility 19, Wing Attack 22, Water Pulse 28; as Mantine: Take Down 31, Confuse Ray 37, Bounce 40, Aqua Ring 46, Hydro Pump 49 | Mantine (from 30) |
| Mantyke | old rod | 14 | Rewrite | Tackle, Bubble, BubbleBeam, Headbutt | Agility 19, Wing Attack 22, Icy Wind 25, Water Pulse 28; as Mantine: Take Down 31, Scald 34, Confuse Ray 37, Bounce 40, Psybeam 41, Signal Beam 43, Aqua Ring 46, Surf 49 | Mantine (from 30) |
| Finneon | old rod | 15 | Oxide | Pound, Water Gun, Attract | Gust 17, Water Pulse 22, Captivate 26, Safeguard 29; as Lumineon: Aqua Ring 35, Whirlpool 42, U-turn 48, Bounce 53 | Lumineon (from 31) |
| Finneon | old rod | 15 | Rewrite | Tailwind, Attract, Water Pulse, Pursuit | Gust 17, Captivate 26, Safeguard 29; as Lumineon: Flip Turn 31, Aqua Ring 33, Icy Wind 34, Aqua Tail 38, Signal Beam 40, Whirlpool 42, Ice Fang 45, U-turn 48, Bounce 53 | Lumineon (from 31) |
| Shellos | old rod | 15 | Oxide | Mud Sport, Harden, Water Pulse, Mud Bomb | Hidden Power 16, Body Slam 29; as Gastrodon: Muddy Water 41 | Gastrodon (from 30) |
| Shellos | old rod | 15 | Rewrite | Mud-Slap, Harden, Water Pulse, Mud Bomb | Hidden Power 16, Swagger 22, Body Slam 29; as Gastrodon: AncientPower 33, Earth Power 35, Clear Smog 37, Muddy Water 41, Bulldoze 44, Sludge Bomb 46, Ice Beam 49 | Gastrodon (from 30) |
| Clamperl | old rod | 16 | Oxide | Clamp, Water Gun, Whirlpool, Iron Defense | as Huntail: Scary Face 19, Ice Fang 24, Brine 28, Baton Pass 33, Dive 37, Crunch 42, Aqua Tail 46, Hydro Pump 51 | Huntail (from 16) |
| Clamperl | old rod | 16 | Oxide | Clamp, Water Gun, Whirlpool, Iron Defense | as Gorebyss: Amnesia 19, Aqua Ring 24, Captivate 28, Baton Pass 33, Dive 37, Psychic 42, Aqua Tail 46, Hydro Pump 51 | Gorebyss (from 16) |
| Clamperl | old rod | 16 | Rewrite | Clamp, Water Gun, Whirlpool, Iron Defense | as Huntail: Scary Face 19, Ice Fang 24, Brine 28, Baton Pass 33, Flip Turn 35, Dive 37, Waterfall 40, Crunch 42, Aqua Tail 46, Muddy Water 51 | Huntail (from 16) |
| Clamperl | old rod | 16 | Rewrite | Clamp, Water Gun, Whirlpool, Iron Defense | as Gorebyss: Amnesia 19, Aqua Ring 24, Captivate 28, Baton Pass 33, Draining Kiss 35, Dive 37, Surf 40, Psychic 42, Aqua Tail 46, Muddy Water 51 | Gorebyss (from 16) |
| Horsea | good rod | 24 | Oxide | Water Gun, Focus Energy, BubbleBeam, Agility | Twister 26, Brine 30; as Kingdra: Hydro Pump 40, Dragon Dance 48 | Kingdra (from 32) |
| Horsea | good rod | 24 | Rewrite | Water Gun, Focus Energy, BubbleBeam, Agility | Twister 26, Brine 30; as Kingdra: Muddy Water 40, Aurora Beam 44 | Kingdra (from 32) |
| Tentacool | good rod | 24 | Oxide | Acid, Toxic Spikes, BubbleBeam, Wrap | Barrier 26, Water Pulse 29; as Tentacruel: Poison Jab 36, Screech 42, Hydro Pump 49 | Tentacruel (from 30) |
| Tentacool | good rod | 24 | Rewrite | Acid, Toxic Spikes, Water Pulse, BubbleBeam | Barrier 26; as Tentacruel: Poison Jab 33, Aurora Beam 34, Sludge Bomb 39, Screech 42, Psybeam 44, Surf 49, Muddy Water 53 | Tentacruel (from 30) |
| Mareanie | good rod | 26 to 28 | Oxide | Wide Guard, Venoshock, Toxic Spikes, Recover | Spike Cannon 29, Pin Missile 34, Toxic 36; as Toxapex: Toxic 39, Venom Drench 42, Poison Jab 43, Liquidation 45 | Toxapex (from 38) |
| Mareanie | good rod | 26 to 28 | Rewrite | Wide Guard, Venoshock, Toxic Spikes, Recover | Spike Cannon 29, Pin Missile 34, Toxic 36, Muddy Water 38; as Toxapex: Venom Drench 42, Poison Jab 43, Liquidation 45, Lunge 53 | Toxapex (from 38) |
| Octillery | good rod | 26 | Oxide | Aurora Beam, BubbleBeam, Focus Energy, Octazooka | Bullet Seed 29, Wring Out 36, Signal Beam 42, Ice Beam 48 | Octillery |
| Octillery | good rod | 26 | Rewrite | Aurora Beam, BubbleBeam, Focus Energy, Octazooka | Mud Shot 27, Bullet Seed 29, Round 33, Charge Beam 35, Scald 37, Skitter Smack 40, Signal Beam 42, Ice Beam 48 | Octillery |
| Mantyke | surf | 30 | Oxide | Headbutt, Agility, Wing Attack, Water Pulse | Take Down 31; as Mantine: Take Down 31, Confuse Ray 37, Bounce 40, Aqua Ring 46, Hydro Pump 49 | Mantine (from 31) |
| Mantyke | surf | 30 | Rewrite | Agility, Wing Attack, Icy Wind, Water Pulse | Take Down 31; as Mantine: Take Down 31, Scald 34, Confuse Ray 37, Bounce 40, Psybeam 41, Signal Beam 43, Aqua Ring 46, Surf 49 | Mantine (from 31) |
| Wailmer | surf | 30 | Oxide | Astonish, Water Pulse, Mist, Rest | Brine 31, Water Spout 34, Amnesia 37; as Wailord: Dive 46 | Wailord (from 40) |
| Wailmer | surf | 30 | Rewrite | Water Pulse, Mist, Rest, Bulldoze | Brine 31, Water Spout 34, Amnesia 37; as Wailord: Dive 46, Iron Head 48, Rock Tomb 50 | Wailord (from 40) |
| Gastrodon | surf | 33 | Oxide | Water Pulse, Mud Bomb, Hidden Power, Body Slam | Muddy Water 41 | Gastrodon |
| Gastrodon | surf | 33 | Rewrite | Mud Bomb, Hidden Power, Body Slam, AncientPower | Earth Power 35, Clear Smog 37, Muddy Water 41, Bulldoze 44, Sludge Bomb 46, Ice Beam 49 | Gastrodon |
| Tentacool | surf | 33 to 36 | Oxide | Wrap, Barrier, Water Pulse, Poison Jab | as Tentacruel: Poison Jab 36, Screech 42, Hydro Pump 49 | Tentacruel (from 34) |
| Tentacool | surf | 33 to 36 | Rewrite | Water Pulse, BubbleBeam, Barrier, Poison Jab | as Tentacruel: Aurora Beam 34, Sludge Bomb 39, Screech 42, Psybeam 44, Surf 49, Muddy Water 53 | Tentacruel (from 34) |

## Route 221

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 53 | At the cap |
|---|---|---|---|---|---|---|
| Corsola | old rod | 14 | Oxide | Tackle, Harden, Bubble, Recover | Refresh 16, Rock Blast 20, BubbleBeam 25, Lucky Chant 28, AncientPower 32, Aqua Ring 37, Spike Cannon 40, Power Gem 44, Mirror Coat 48, Earth Power 53 | Corsola |
| Corsola | old rod | 14 | Rewrite | Tackle, Life Dew, Bubble, Recover | AncientPower 16, Bulldoze 18, Rock Blast 20, BubbleBeam 25, Lucky Chant 28, Aqua Cutter 33, Liquidation 35, Aqua Ring 37, Spike Cannon 40, Throat Chop 42, Power Gem 44, Mirror Coat 48, Earth Power 53 | Corsola |
| Shellos | old rod | 14 | Oxide | Mud Sport, Harden, Water Pulse, Mud Bomb | Hidden Power 16, Body Slam 29; as Gastrodon: Muddy Water 41 | Gastrodon (from 30) |
| Shellos | old rod | 14 | Rewrite | Mud-Slap, Harden, Water Pulse, Mud Bomb | Hidden Power 16, Swagger 22, Body Slam 29; as Gastrodon: AncientPower 33, Earth Power 35, Clear Smog 37, Muddy Water 41, Bulldoze 44, Sludge Bomb 46, Ice Beam 49 | Gastrodon (from 30) |
| Finneon | old rod | 15 | Oxide | Pound, Water Gun, Attract | Gust 17, Water Pulse 22, Captivate 26, Safeguard 29; as Lumineon: Aqua Ring 35, Whirlpool 42, U-turn 48, Bounce 53 | Lumineon (from 31) |
| Finneon | old rod | 15 | Rewrite | Tailwind, Attract, Water Pulse, Pursuit | Gust 17, Captivate 26, Safeguard 29; as Lumineon: Flip Turn 31, Aqua Ring 33, Icy Wind 34, Aqua Tail 38, Signal Beam 40, Whirlpool 42, Ice Fang 45, U-turn 48, Bounce 53 | Lumineon (from 31) |
| Luvdisc | old rod | 15 | Oxide | Charm, Water Gun, Agility, Take Down | Lucky Chant 17, Attract 22, Sweet Kiss 27; as Alomomola: Soak 33, Wish 37, Brine 41, Safeguard 45, Whirlpool 49, Helping Hand 53 | Alomomola (from 30) |
| Luvdisc | old rod | 15 | Rewrite | Water Gun, Aqua Jet, Draining Kiss, Take Down | Lucky Chant 17, Agility 18, Icy Wind 20, Attract 22, Sweet Kiss 27; as Alomomola: Heal Pulse 30, Wake-Up Slap 31, Water Pulse 32, Soak 33, Play Rough 35, Wish 37, Brine 41, Zen Headbutt 43, Safeguard 45, Whirlpool 49, Helping Hand 53 | Alomomola (from 30) |
| Mantyke | old rod | 16 | Oxide | Bubble, Supersonic, BubbleBeam, Headbutt | Agility 19, Wing Attack 22, Water Pulse 28; as Mantine: Take Down 31, Confuse Ray 37, Bounce 40, Aqua Ring 46, Hydro Pump 49 | Mantine (from 30) |
| Mantyke | old rod | 16 | Rewrite | Tackle, Bubble, BubbleBeam, Headbutt | Agility 19, Wing Attack 22, Icy Wind 25, Water Pulse 28; as Mantine: Take Down 31, Scald 34, Confuse Ray 37, Bounce 40, Psybeam 41, Signal Beam 43, Aqua Ring 46, Surf 49 | Mantine (from 30) |
| Finneon | good rod | 24 | Oxide | Water Gun, Attract, Gust, Water Pulse | Captivate 26, Safeguard 29; as Lumineon: Aqua Ring 35, Whirlpool 42, U-turn 48, Bounce 53 | Lumineon (from 31) |
| Finneon | good rod | 24 | Rewrite | Attract, Water Pulse, Pursuit, Gust | Captivate 26, Safeguard 29; as Lumineon: Flip Turn 31, Aqua Ring 33, Icy Wind 34, Aqua Tail 38, Signal Beam 40, Whirlpool 42, Ice Fang 45, U-turn 48, Bounce 53 | Lumineon (from 31) |
| Remoraid | good rod | 24 | Oxide | Psybeam, Aurora Beam, BubbleBeam, Focus Energy | as Octillery: Octazooka 25, Bullet Seed 29, Wring Out 36, Signal Beam 42, Ice Beam 48 | Octillery (from 25) |
| Remoraid | good rod | 24 | Rewrite | Screech, Aurora Beam, BubbleBeam, Focus Energy | as Octillery: Octazooka 25, Mud Shot 27, Bullet Seed 29, Round 33, Charge Beam 35, Scald 37, Skitter Smack 40, Signal Beam 42, Ice Beam 48 | Octillery (from 25) |
| Luvdisc | good rod | 26 | Oxide | Agility, Take Down, Lucky Chant, Attract | Sweet Kiss 27; as Alomomola: Soak 33, Wish 37, Brine 41, Safeguard 45, Whirlpool 49, Helping Hand 53 | Alomomola (from 30) |
| Luvdisc | good rod | 26 | Rewrite | Lucky Chant, Agility, Icy Wind, Attract | Sweet Kiss 27; as Alomomola: Heal Pulse 30, Wake-Up Slap 31, Water Pulse 32, Soak 33, Play Rough 35, Wish 37, Brine 41, Zen Headbutt 43, Safeguard 45, Whirlpool 49, Helping Hand 53 | Alomomola (from 30) |
| Mareanie | good rod | 26 | Oxide | Wide Guard, Venoshock, Toxic Spikes, Recover | Spike Cannon 29, Pin Missile 34, Toxic 36; as Toxapex: Toxic 39, Venom Drench 42, Poison Jab 43, Liquidation 45 | Toxapex (from 38) |
| Mareanie | good rod | 26 | Rewrite | Wide Guard, Venoshock, Toxic Spikes, Recover | Spike Cannon 29, Pin Missile 34, Toxic 36, Muddy Water 38; as Toxapex: Venom Drench 42, Poison Jab 43, Liquidation 45, Lunge 53 | Toxapex (from 38) |
| Fomantis | wild | 28 | Oxide | Razor Leaf, Ingrain, Sweet Scent, Slash | X-Scissor 30, Synthesis 31, Leaf Blade 32; as Lurantis: Leaf Blade 34 | Lurantis (from 34) |
| Fomantis | wild | 28 | Rewrite | Leafage, Fury Cutter, Razor Leaf, Slash | X-Scissor 30, Synthesis 31, Leaf Blade 32; as Lurantis: Leaf Blade 34, Low Sweep 40, Night Slash 44, Poison Jab 49, Skitter Smack 52 | Lurantis (from 34) |
| Quagsire | good rod | 28 | Oxide | Mud Shot, Slam, Mud Bomb, Amnesia | Yawn 31, Earthquake 36, Mist 48, Haze 48, Muddy Water 53 | Quagsire |
| Quagsire | good rod | 28 | Rewrite | Slam, Mud Bomb, Amnesia, Trailblaze | Yawn 31, Earthquake 36, Rock Slide 39, Toxic 40, Drain Punch 44, Mist 48, Muddy Water 53 | Quagsire |
| Corvisquire | wild | 29 | Oxide | Sand-Attack, Pluck, Steel Wing, Drill Peck | FeatherDance 32, Revenge 38; as Corviknight: Defog 42, Iron Head 44, Brave Bird 49 | Corviknight (from 40) |
| Corvisquire | wild | 29 | Rewrite | Pluck, Steel Wing, Drill Peck, Low Sweep | FeatherDance 32, U-turn 35, Revenge 38; as Corviknight: Defog 42, Iron Head 44, Brave Bird 49, Body Slam 52 | Corviknight (from 40) |
| Dolliv | wild | 29 | Oxide | Flail, Mega Drain, Grassy Terrain, Seed Bomb | Energy Ball 34; as Arboliva: Leech Seed 39, Terrain Pulse 46, Petal Blizzard 52 | Arboliva (from 35) |
| Dolliv | wild | 29 | Rewrite | Mega Drain, Charm, Mud Shot, Seed Bomb | Giga Drain 31, Energy Ball 34; as Arboliva: Leech Seed 39, Alluring Voice 42, Swift 44, Petal Blizzard 52 | Arboliva (from 35) |
| Dubwool | wild | 29 | Oxide | Guard Split, Double Kick, Headbutt, Take Down | Guard Swap 32, Reversal 38, Cotton Guard 44, Double-Edge 50 | Dubwool |
| Dubwool | wild | 29 | Rewrite | Payback, Take Down, Swagger, Agility | Guard Swap 32, Body Slam 35, Reversal 38, Zen Headbutt 41, Cotton Guard 44, Body Press 47, Double-Edge 50 | Dubwool |
| Fletchinder | wild | 29 | Oxide | Aerial Ace, Flame Charge, Roost, Will-O-Wisp | Natural Gift 31; as Talonflame: Acrobatics 38, Me First 42, Tailwind 46, Flare Blitz 51 | Talonflame (from 36) |
| Fletchinder | wild | 29 | Rewrite | Flame Charge, Bite, Roost, Will-O-Wisp | Natural Gift 31; as Talonflame: Acrobatics 38, Steel Wing 40, Flamethrower 42, Tailwind 46, Upper Hand 48, Flare Blitz 51 | Talonflame (from 36) |
| Liepard | wild | 29 to 30 | Oxide | Torment, Fake Out, Assurance, Hone Claws | Slash 34, Taunt 38, Sucker Punch 43, Nasty Plot 44, Night Slash 44, Snatch 47 | Liepard |
| Liepard | wild | 29 to 30 | Rewrite | Trailblaze, Fake Out, Hone Claws, Assurance | Dark Pulse 30, Nasty Plot 32, Slash 34, Throat Chop 36, Taunt 38, Sucker Punch 43, Night Slash 44, Snatch 47, Skitter Smack 50 | Liepard |
| Mightyena | wild | 29 | Oxide | Bite, Odor Sleuth, Roar, Swagger | Assurance 32, Crunch 34, Scary Face 37, Taunt 42, Embargo 47, Take Down 52 | Mightyena |
| Mightyena | wild | 29 | Rewrite | Trailblaze, Roar, Swagger, Throat Chop | Assurance 32, Crunch 34, Scary Face 37, Strength 39, Taunt 42, Headbutt 44, Embargo 47, Take Down 52 | Mightyena |
| Toucannon | wild | 29 | Oxide | Supersonic, Pluck, Roost, Fury Attack | Screech 30, Drill Peck 34, Bullet Seed 40, FeatherDance 44, Hyper Voice 50 | Toucannon |
| Toucannon | wild | 29 | Rewrite | Echoed Voice, Supersonic, Pluck, Roost | Screech 30, Drill Peck 32, Smack Down 35, Facade 37, Bullet Seed 40, Throat Chop 42, FeatherDance 44, Take Down 47, Hyper Voice 50 | Toucannon |
| Donphan | wild | 30 | Oxide | Rollout, Magnitude, Slam, Fury Attack | Assurance 31, Scary Face 39, Earthquake 46 | Donphan |
| Donphan | wild | 30 | Rewrite | Slam, Rapid Spin, Magnitude, Rock Tomb | Assurance 31, Trailblaze 35, Scary Face 39, Iron Head 42, Throat Chop 44, Earthquake 46, Seed Bomb 50 | Donphan |
| Mantine | surf | 30 | Oxide | Headbutt, Agility, Wing Attack, Water Pulse | Take Down 31, Confuse Ray 37, Bounce 40, Aqua Ring 46, Hydro Pump 49 | Mantine |
| Mantine | surf | 30 | Rewrite | Headbutt, Agility, Wing Attack, Water Pulse | Take Down 31, Scald 34, Confuse Ray 37, Bounce 40, Psybeam 41, Signal Beam 43, Aqua Ring 46, Surf 49 | Mantine |
| Sandygast | wild | 30 | Oxide | Sand-Attack, Mega Drain, Bulldoze, Hypnosis | Giga Drain 35, Iron Defense 36; as Palossand: Shadow Ball 44, Earth Power 50 | Palossand (from 42) |
| Sandygast | wild | 30 | Rewrite | Sand-Attack, Mega Drain, Bulldoze, Hypnosis | Giga Drain 35, Iron Defense 36; as Palossand: Shadow Ball 44, Sludge Bomb 47, Earth Power 50 | Palossand (from 42) |
| Steenee | wild | 30 | Oxide | Sweet Scent, Magical Leaf, Teeter Dance, Stomp | Aromatic Mist 32; as Tsareena: Low Sweep 32, Aromatherapy 38, Leaf Storm 44, Power Whip 48 | Tsareena (from 32) |
| Steenee | wild | 30 | Rewrite | Draining Kiss, Magical Leaf, Teeter Dance, Stomp | as Tsareena: Low Sweep 32, Swagger 33, Trop Kick 34, Aromatherapy 38, Zen Headbutt 41, Leaf Storm 44, U-turn 49, Knock Off 52 | Tsareena (from 32) |
| Tentacool | surf | 30 | Oxide | BubbleBeam, Wrap, Barrier, Water Pulse | as Tentacruel: Poison Jab 36, Screech 42, Hydro Pump 49 | Tentacruel (from 31) |
| Tentacool | surf | 30 | Rewrite | Toxic Spikes, Water Pulse, BubbleBeam, Barrier | as Tentacruel: Poison Jab 33, Aurora Beam 34, Sludge Bomb 39, Screech 42, Psybeam 44, Surf 49, Muddy Water 53 | Tentacruel (from 31) |
| Araquanid | wild | 31 | Oxide | BubbleBeam, Bug Bite, Headbutt, Soak | Dive 36, Lunge 41, Scald 48, Hydro Pump 51 | Araquanid |
| Araquanid | wild | 31 | Rewrite | Bug Bite, Headbutt, Spider Web, Soak | Skitter Smack 34, Dive 36, Waterfall 38, Lunge 41, Poison Jab 44, Scald 48, Surf 51 | Araquanid |
| Carnivine | wild | 31 | Oxide | Faint Attack, Stockpile, Spit Up, Swallow | Crunch 37, Wring Out 41, Power Whip 47 | Carnivine |
| Carnivine | wild | 31 | Rewrite | Faint Attack, Swallow, Leaf Tornado, Stockpile | Spit Up 32, Swagger 33, Seed Bomb 35, Crunch 37, Giga Drain 40, Leech Life 42, Power Whip 47, Secret Power 53 | Carnivine |
| Shellos | wild | 31 | Oxide | Water Pulse, Mud Bomb, Hidden Power, Body Slam | as Gastrodon: Muddy Water 41 | Gastrodon (from 32) |
| Shellos | wild | 31 | Rewrite | Mud Bomb, Hidden Power, Swagger, Body Slam | as Gastrodon: AncientPower 33, Earth Power 35, Clear Smog 37, Muddy Water 41, Bulldoze 44, Sludge Bomb 46, Ice Beam 49 | Gastrodon (from 32) |
| Frillish | surf | 33 | Oxide | Water Pulse, Imprison, Confuse Ray, Hex | Brine 34, Pain Split 39; as Jellicent: Destiny Bond 45, Shadow Ball 51 | Jellicent (from 40) |
| Frillish | surf | 33 | Rewrite | Water Pulse, Imprison, Confuse Ray, Hex | Brine 34, Dark Pulse 36, Pain Split 39; as Jellicent: Muddy Water 45, Shadow Ball 51 | Jellicent (from 40) |
| Shellos | surf | 33 | Oxide | Water Pulse, Mud Bomb, Hidden Power, Body Slam | as Gastrodon: Muddy Water 41 | Gastrodon (from 34) |
| Shellos | surf | 33 | Rewrite | Mud Bomb, Hidden Power, Swagger, Body Slam | as Gastrodon: Earth Power 35, Clear Smog 37, Muddy Water 41, Bulldoze 44, Sludge Bomb 46, Ice Beam 49 | Gastrodon (from 34) |
| Lanturn | surf | 36 | Oxide | Swallow, Spit Up, BubbleBeam, Signal Beam | Discharge 40, Aqua Ring 47, Hydro Pump 52 | Lanturn |
| Lanturn | surf | 36 | Rewrite | BubbleBeam, Signal Beam, Scald, Surf | Thunderbolt 37, Discharge 40, Flash Cannon 43, Aqua Ring 47, Muddy Water 52 | Lanturn |

## Twinleaf Town

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 53 | At the cap |
|---|---|---|---|---|---|---|
| Buizel | surf | 20 | Oxide | Quick Attack, Water Gun, Pursuit, Swift | Aqua Jet 21; as Floatzel: Crunch 26, Agility 29, Whirlpool 39, Razor Wind 50 | Floatzel (from 26) |
| Buizel | surf | 20 | Rewrite | BubbleBeam, Pursuit, Scary Face, Swift | Aqua Jet 21; as Floatzel: Crunch 26, Icy Wind 29, Flip Turn 33, Waterfall 36, Whirlpool 39, Liquidation 41, Low Sweep 44, Agility 51, Rock Tomb 53 | Floatzel (from 26) |
| Lombre | surf | 20 | Oxide | Nature Power, Fake Out, Fury Swipes, Water Sport | nothing | Ludicolo (from 20) |
| Lombre | surf | 20 | Rewrite | Fake Out, Fury Swipes, Natural Gift, Water Sport | as Ludicolo: Energy Ball 34 | Ludicolo (from 20) |
| Goldeen | surf | 23 | Oxide | Supersonic, Horn Attack, Water Pulse, Flail | Aqua Ring 27, Fury Attack 31; as Seaking: Waterfall 40, Horn Drill 47 | Seaking (from 33) |
| Goldeen | surf | 23 | Rewrite | Water Pulse, Horn Attack, Swagger, Flail | Aqua Ring 27; as Seaking: Aqua Jet 34, Skull Bash 37, Waterfall 40, Poison Jab 44, Drill Run 47, Knock Off 50 | Seaking (from 33) |
| Masquerain | surf | 23 | Oxide | Quick Attack, Sweet Scent, Water Sport, Gust | Scary Face 26, Stun Spore 33, Silver Wind 40, Air Slash 47 | Masquerain |
| Masquerain | surf | 23 | Rewrite | Bubble, Quick Attack, Water Sport, Gust | BubbleBeam 25, Scary Face 26, Mud Bomb 29, Stun Spore 33, Surf 36, Giga Drain 38, Silver Wind 40, Signal Beam 41, Icy Wind 43, Air Slash 47, Lunge 53 | Masquerain |
| Squirtle | surf | 26 | Oxide | Bite, Rapid Spin, Protect, Water Pulse | as Wartortle: Water Pulse 28, Aqua Tail 32, Skull Bash 36; as Blastoise: Skull Bash 39, Iron Defense 46 | Blastoise (from 36) |
| Squirtle | surf | 26 | Rewrite | Bubble, Water Gun, Water Pulse, Bite | as Wartortle: Water Pulse 28, Rock Tomb 30, Aqua Tail 32; as Blastoise: Water Pledge 36, Skull Bash 39, Dark Pulse 42, Flash Cannon 44, Iron Defense 46, Aura Sphere 53 | Blastoise (from 36) |

## Valley Windworks

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 53 | At the cap |
|---|---|---|---|---|---|---|
| Buizel | surf | 22 | Oxide | Water Gun, Pursuit, Swift, Aqua Jet | as Floatzel: Crunch 26, Agility 29, Whirlpool 39, Razor Wind 50 | Floatzel (from 26) |
| Buizel | surf | 22 | Rewrite | Pursuit, Scary Face, Swift, Aqua Jet | as Floatzel: Crunch 26, Icy Wind 29, Flip Turn 33, Waterfall 36, Whirlpool 39, Liquidation 41, Low Sweep 44, Agility 51, Rock Tomb 53 | Floatzel (from 26) |
| Quagsire | surf | 22 | Oxide | Mud Sport, Mud Shot, Slam, Mud Bomb | Amnesia 24, Yawn 31, Earthquake 36, Mist 48, Haze 48, Muddy Water 53 | Quagsire |
| Quagsire | surf | 22 | Rewrite | Tail Whip, Mud Shot, Slam, Mud Bomb | Amnesia 24, Trailblaze 27, Yawn 31, Earthquake 36, Rock Slide 39, Toxic 40, Drain Punch 44, Mist 48, Muddy Water 53 | Quagsire |
| Lombre | surf | 25 | Oxide | Fake Out, Fury Swipes, Water Sport, BubbleBeam | nothing | Ludicolo (from 25) |
| Lombre | surf | 25 | Rewrite | Natural Gift, Water Sport, Swagger, BubbleBeam | as Ludicolo: Energy Ball 34 | Ludicolo (from 25) |
| Masquerain | surf | 25 | Oxide | Quick Attack, Sweet Scent, Water Sport, Gust | Scary Face 26, Stun Spore 33, Silver Wind 40, Air Slash 47 | Masquerain |
| Masquerain | surf | 25 | Rewrite | Quick Attack, Water Sport, Gust, BubbleBeam | Scary Face 26, Mud Bomb 29, Stun Spore 33, Surf 36, Giga Drain 38, Silver Wind 40, Signal Beam 41, Icy Wind 43, Air Slash 47, Lunge 53 | Masquerain |
| Corphish | surf | 28 | Oxide | Leer, BubbleBeam, Protect, Knock Off | as Crawdaunt: Swift 30, Taunt 34, Night Slash 39, Crabhammer 44, Swords Dance 52 | Crawdaunt (from 30) |
| Corphish | surf | 28 | Rewrite | BubbleBeam, Leer, Razor Shell, Knock Off | as Crawdaunt: Swift 30, Taunt 32, Throat Chop 35, Aerial Ace 36, Night Slash 39, X-Scissor 41, Crabhammer 44, Brick Break 48, Swords Dance 52 | Crawdaunt (from 30) |

## Honey trees

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 53 | At the cap |
|---|---|---|---|---|---|---|
| Charjabug | honey | 28 | Oxide | Mud-Slap, Bug Bite, Bite, Spark | as Vikavolt: Crunch 29, Signal Beam 36, Discharge 48 | Vikavolt (from 28) |
| Charjabug | honey | 28 | Rewrite | Bite, Spark, Sticky Web, Skitter Smack | as Vikavolt: Crunch 29, Signal Beam 36, Pollen Puff 40, Discharge 48 | Vikavolt (from 28) |
| Emolga | honey | 28 | Oxide | Spark, Shock Wave, Electro Ball, Acrobatics | Encore 36, Light Screen 39, Volt Switch 40, Discharge 50, Agility 50 | Emolga |
| Emolga | honey | 28 | Rewrite | Shock Wave, Spark, Air Cutter, Acrobatics | Electroweb 31, Encore 36, Light Screen 39, Volt Switch 40, Thunderbolt 44, Agility 49, Discharge 50 | Emolga |
| Heracross | honey | 28 | Oxide | Fury Attack, Aerial Ace, Brick Break, Counter | Take Down 31, Close Combat 37, Reversal 43, Feint 49 | Heracross |
| Heracross | honey | 28 | Rewrite | Brick Break, Pounce, Counter, Rock Tomb | Take Down 31, Leech Life 34, Close Combat 37, Throat Chop 40, Reversal 43, Skitter Smack 46, Lunge 49 | Heracross |
| Joltik | honey | 28 | Oxide | Electroweb, Bug Bite, Gastro Acid, Struggle Bug | Discharge 29; as Galvantula: Signal Beam 35, Energy Ball 39, Sucker Punch 43, Thunderbolt 48, Bug Buzz 51 | Galvantula (from 30) |
| Joltik | honey | 28 | Rewrite | Bug Bite, Gastro Acid, Struggle Bug, Sucker Punch | Discharge 29; as Galvantula: Snarl 32, Signal Beam 35, Energy Ball 39, Swift 40, Giga Drain 41, Sucker Punch 43, Thunderbolt 48, Bug Buzz 51 | Galvantula (from 30) |
| Larvesta | honey | 28 | Oxide | Ember, String Shot, Flame Charge, Struggle Bug | Flame Wheel 30, Bug Bite 40, Take Down 50 | Larvesta; Volcarona in HQ |
| Larvesta | honey | 28 | Rewrite | Ember, String Shot, Flame Charge, Struggle Bug | U-turn 29, Flame Wheel 30, Bug Bite 40, Fire Spin 41, Roost 45, Take Down 50, Poison Jab 53 | Larvesta; Volcarona in HQ |
| Nuzleaf | honey | 28 | Oxide | Growth, Nature Power, Fake Out, Torment | as Shiftry: Leaf Storm 49 | Shiftry (from 28) |
| Nuzleaf | honey | 28 | Rewrite | Chilling Water, Fake Out, Rock Tomb, Torment | as Shiftry: Leaf Blade 34, Leech Life 40, Extrasensory 43, Leaf Storm 49, Rock Slide 53 | Shiftry (from 28) |
| Scyther | honey | 28 | Oxide | False Swipe, Agility, Wing Attack, Fury Cutter | as Scizor: Slash 29, Razor Wind 33, Iron Defense 37, X-Scissor 41, Night Slash 45, Double Hit 49, Iron Head 53 | Scizor (from 28) |
| Scyther | honey | 28 | Oxide | False Swipe, Agility, Wing Attack, Fury Cutter | as Kleavor: Dual Wingbeat 28, Rock Blast 32, X-Scissor 36, Superpower 40, Acrobatics 44, Stone Edge 48, Leech Life 51, Close Combat 53 | Kleavor (from 28) |
| Scyther | honey | 28 | Rewrite | False Swipe, Agility, Wing Attack, Fury Cutter | as Scizor: Slash 29, Skitter Smack 34, Iron Defense 37, X-Scissor 41, Night Slash 45, Double Hit 49, Iron Head 53 | Scizor (from 28) |
| Scyther | honey | 28 | Rewrite | False Swipe, Agility, Wing Attack, Fury Cutter | as Kleavor: Dual Wingbeat 28, Rock Blast 32, Rock Slide 35, X-Scissor 36, Superpower 40, Acrobatics 44, Stone Edge 48, Leech Life 51, Close Combat 53 | Kleavor (from 28) |
| Snom | honey | 28 | Oxide | Powder Snow, Struggle Bug | as Frosmoth: Bug Buzz 32, Aurora Veil 36, Blizzard 40, Tailwind 44, Wide Guard 48, Quiver Dance 52 | Frosmoth (from 30) |
| Snom | honey | 28 | Rewrite | Powder Snow, Struggle Bug, Stun Spore | Fairy Wind 30; as Frosmoth: Stun Spore 30, Infestation 31, Bug Buzz 32, Defog 33, Aurora Beam 34, Aurora Veil 36, Ice Beam 40, Tailwind 44, Wide Guard 48, Quiver Dance 52 | Frosmoth (from 30) |
| Swadloon | honey | 28 | Oxide | Tackle, String Shot, Bug Bite, Razor Leaf | as Leavanny: Helping Hand 32, Leaf Blade 36, X-Scissor 39, Entrainment 43, Swords Dance 46, Leaf Storm 50 | Leavanny (from 30) |
| Swadloon | honey | 28 | Rewrite | Bug Bite, Razor Leaf, Struggle Bug, Bite | as Leavanny: Fell Stinger 30, Helping Hand 32, Leaf Blade 36, X-Scissor 39, Poison Jab 41, Entrainment 43, Swords Dance 46, Leaf Storm 50 | Leavanny (from 30) |
| Toucannon | honey | 28 | Oxide | Supersonic, Pluck, Roost, Fury Attack | Screech 30, Drill Peck 34, Bullet Seed 40, FeatherDance 44, Hyper Voice 50 | Toucannon |
| Toucannon | honey | 28 | Rewrite | Echoed Voice, Supersonic, Pluck, Roost | Screech 30, Drill Peck 32, Smack Down 35, Facade 37, Bullet Seed 40, Throat Chop 42, FeatherDance 44, Take Down 47, Hyper Voice 50 | Toucannon |
| Vespiquen | honey | 28 | Oxide | Fury Swipes, Power Gem, Heal Order, Toxic | Slash 31, Captivate 33, Attack Order 37, Swagger 39, Destiny Bond 43 | Vespiquen |
| Vespiquen | honey | 28 | Rewrite | Defend Order, Heal Order, Bug Bite, Air Cutter | Toxic 29, Slash 31, Captivate 33, Pounce 35, Attack Order 37, Swagger 39, U-turn 41, Air Slash 44, Poison Jab 48, Psychic Noise 53 | Vespiquen |
| Yanma | honey | 28 | Oxide | SonicBoom, Detect, Supersonic, Uproar | Pursuit 30, AncientPower 33; as Yanmega: Feint 38, Slash 43, Screech 46, U-turn 49 | Yanmega (from 35) |
| Yanma | honey | 28 | Rewrite | Quick Attack, SonicBoom, Roost, Uproar | Pursuit 30, AncientPower 33, Air Cutter 34, Signal Beam 35; as Yanmega: Hypnosis 38, Ominous Wind 40, Slash 43, Screech 46, U-turn 49, Psychic Noise 51 | Yanmega (from 35) |

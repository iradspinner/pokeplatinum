# Candice's split: what each catch knows and learns

Written by `tools/oxide/balance/learncheck.py sheets` for check 6 of the learnset baseline (`docs/oxide/learnset-checks.md`). One table per capture area first offered in Candice's split, whose cap is 56. Each Pokemon is read at the lowest level it is found at there. "Knows at capture" is the last four moves its list gives by that level; "learns by level-up" is every entry it reaches after capture up to 56, evolving on time, with each later stage's moves under its name; "at the cap" is the stage it can be by then and the next one after. A row marked Rewrite shows the learnset rewrite's lists (the tree's) where it differs from the row marked Oxide, Oxide's lists before the learnset rewrite (`da6b92496c`); a row marked both is the same in each. Relearner-only moves and egg moves are left out.

## Acuity Lakefront

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 56 | At the cap |
|---|---|---|---|---|---|---|
| Sneasel | wild | 32 to 35 | Oxide | Faint Attack, Fury Swipes, Agility, Icy Wind | Slash 35, Metal Claw 42, Ice Shard 49 | Sneasel; Weavile in HQ |
| Sneasel | wild | 32 to 35 | Rewrite | Fury Swipes, Nasty Plot, Agility, Icy Wind | Slash 35, Revenge 37, Poison Jab 40, Metal Claw 42, Ice Shard 49, Throat Chop 51, Ice Punch 56 | Sneasel; Weavile in HQ |
| Absol | wild | 33 to 35 | Oxide | Pursuit, Swords Dance, Bite, Double Team | Slash 36, Future Sight 41, Sucker Punch 44, Detect 49, Night Slash 52 | Absol |
| Absol | wild | 33 to 35 | Rewrite | Quick Attack, Pursuit, Swords Dance, Bite | Slash 36, Future Sight 41, Sucker Punch 44, X-Scissor 46, Night Slash 52, Throat Chop 54 | Absol |
| Alolan Ninetales | wild | 33 | Oxide | Tail Whip, Disable, Ice Shard, Safeguard | nothing | Alolan Ninetales |
| Alolan Ninetales | wild | 33 | Rewrite | Incinerate, Spite, Icy Wind, Payback | Dazzling Gleam 35, Chilling Water 37, Ice Beam 43, Extrasensory 44, Foul Play 51, Confuse Ray 53 | Alolan Ninetales |
| Delibird | wild | 33 | Oxide | Present | nothing | Delibird |
| Delibird | wild | 33 | Rewrite | Present, Drill Peck, Ice Beam | Drill Run 54, Swagger 56 | Delibird |
| Frosmoth | wild | 33 to 34 | Oxide | Defog, FeatherDance, Aurora Beam, Bug Buzz | Aurora Veil 36, Blizzard 40, Tailwind 44, Wide Guard 48, Quiver Dance 52 | Frosmoth |
| Frosmoth | wild | 33 to 34 | Rewrite | Stun Spore, Infestation, Bug Buzz, Defog | Aurora Beam 34, Aurora Veil 36, Psybeam 38, Ice Beam 40, Tailwind 44, Wide Guard 48, Giga Drain 50, Quiver Dance 52 | Frosmoth |
| Seel | wild | 33 | Oxide | Aqua Ring, Aurora Beam, Aqua Jet, Brine | as Dewgong: Sheer Cold 34, Take Down 37, Dive 41, Aqua Tail 43, Ice Beam 47, Safeguard 51 | Dewgong (from 34) |
| Seel | wild | 33 | Rewrite | Aqua Ring, Aurora Beam, Aqua Jet, Brine | as Dewgong: Signal Beam 34, Take Down 37, Dive 41, Aqua Tail 43, Drill Run 45, Ice Beam 47, Safeguard 51, Bite 54, Headbutt 56 | Dewgong (from 34) |
| Snover | wild | 33 to 34 | Oxide | Swagger, Mist, Ice Shard, Ingrain | Wood Hammer 36; as Abomasnow: Blizzard 47 | Abomasnow (from 40) |
| Snover | wild | 33 to 34 | Rewrite | Mist, Ice Shard, Rock Tomb, Seed Bomb | Wood Hammer 36; as Abomasnow: Ice Punch 45, Ice Beam 47, Body Press 53, Giga Drain 55 | Abomasnow (from 40) |
| Snorunt | wild | 34 | Oxide | Headbutt, Protect, Ice Fang, Crunch | Ice Shard 37; as Glalie: Blizzard 51 | Glalie (from 42) |
| Snorunt | wild | 34 | Oxide | Headbutt, Protect, Ice Fang, Crunch | as Froslass: Ice Shard 37, Blizzard 51 | Froslass (from 34) |
| Snorunt | wild | 34 | Rewrite | Headbutt, Ominous Wind, Ice Fang, Crunch | Draining Kiss 35, Ice Shard 37; as Glalie: Rock Slide 42, Power Gem 44, Earth Power 46, Icicle Crash 48, Shadow Ball 53, Dark Pulse 55 | Glalie (from 42) |
| Snorunt | wild | 34 | Rewrite | Headbutt, Ominous Wind, Ice Fang, Crunch | as Froslass: Ice Shard 37, Signal Beam 44, Ice Beam 51 | Froslass (from 34) |
| Jynx | wild | 35 | Oxide | Mean Look, Fake Tears, Wake-Up Slap, Avalanche | Body Slam 39, Wring Out 44, Perish Song 49, Blizzard 55 | Jynx |
| Jynx | wild | 35 | Rewrite | Fake Tears, Ice Punch, Wake-Up Slap, Avalanche | Body Slam 39, Psychic 41, Shadow Ball 43, Perish Song 49, Signal Beam 51, Ice Beam 55 | Jynx |

## Canalave City

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 56 | At the cap |
|---|---|---|---|---|---|---|
| Gastrodon | super rod | 36 | Oxide | Water Pulse, Mud Bomb, Hidden Power, Body Slam | Muddy Water 41, Recover 54 | Gastrodon |
| Gastrodon | super rod | 36 | Rewrite | Hidden Power, Body Slam, AncientPower, Clear Smog | Muddy Water 41, Earth Power 43, Bulldoze 45, Ice Beam 50, Recover 54 | Gastrodon |
| Lumineon | super rod | 36 | Oxide | Water Pulse, Captivate, Safeguard, Aqua Ring | Whirlpool 42, U-turn 48, Bounce 53 | Lumineon |
| Lumineon | super rod | 36 | Rewrite | Captivate, Safeguard, Flip Turn, Aqua Ring | Aqua Tail 37, Whirlpool 42, U-turn 48, Ice Fang 50, Bounce 53, Air Slash 55 | Lumineon |
| Jellicent | super rod | 39 | Oxide | Confuse Ray, Hex, Brine, Pain Split | Destiny Bond 45, Shadow Ball 51, Scald 55 | Jellicent |
| Jellicent | super rod | 39 | Rewrite | Confuse Ray, Hex, Brine, Pain Split | Muddy Water 45, Shadow Ball 51, Sludge Bomb 53, Scald 55 | Jellicent |
| Toxapex | super rod | 42 | Oxide | Spike Cannon, Pin Missile, Toxic, Venom Drench | Poison Jab 43, Liquidation 45 | Toxapex |
| Toxapex | super rod | 42 | Rewrite | Spike Cannon, Pin Missile, Toxic, Venom Drench | Poison Jab 43, Liquidation 45, Lunge 48, Sludge Bomb 50, Ice Beam 56 | Toxapex |

## Celestic Town

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 56 | At the cap |
|---|---|---|---|---|---|---|
| Milotic | super rod | 36 | Oxide | Twister, Recover, Captivate, Aqua Tail | Hydro Pump 37, Attract 41, Safeguard 45, Aqua Ring 49 | Milotic |
| Milotic | super rod | 36 | Rewrite | Twister, Recover, Aqua Tail, Aurora Beam | Surf 37, Attract 41, Safeguard 45, Aqua Ring 49, Alluring Voice 51, Dragon Pulse 54 | Milotic |
| Whiscash | super rod | 36 | Oxide | Water Pulse, Magnitude, Rest, Snore | Aqua Tail 39, Earthquake 45, Future Sight 51 | Whiscash |
| Whiscash | super rod | 36 | Rewrite | Magnitude, Bulldoze, Rest, Zen Headbutt | Aqua Tail 39, Wild Charge 42, Earthquake 45, Future Sight 51, Ice Beam 53 | Whiscash |
| Crawdaunt | super rod | 39 | Oxide | Knock Off, Swift, Taunt, Night Slash | Crabhammer 44, Swords Dance 52 | Crawdaunt |
| Crawdaunt | super rod | 39 | Rewrite | Swift, Taunt, Metal Claw, Night Slash | Throat Chop 41, Crabhammer 44, X-Scissor 46, Swords Dance 52 | Crawdaunt |
| Lanturn | super rod | 39 to 42 | Oxide | Swallow, Spit Up, BubbleBeam, Signal Beam | Discharge 40, Aqua Ring 47, Hydro Pump 52 | Lanturn |
| Lanturn | super rod | 39 to 42 | Rewrite | Spit Up, BubbleBeam, Signal Beam, Scald | Discharge 40, Thunderbolt 42, Aqua Ring 47, Muddy Water 52 | Lanturn |

## Eterna City

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 56 | At the cap |
|---|---|---|---|---|---|---|
| Lanturn | super rod | 30 | Oxide | Stockpile, Swallow, Spit Up, BubbleBeam | Signal Beam 35, Discharge 40, Aqua Ring 47, Hydro Pump 52 | Lanturn |
| Lanturn | super rod | 30 | Rewrite | Stockpile, Swallow, Spit Up, BubbleBeam | Signal Beam 35, Scald 37, Discharge 40, Thunderbolt 42, Aqua Ring 47, Muddy Water 52 | Lanturn |
| Sharpedo | super rod | 30 | Oxide | Swagger, Assurance, Crunch, Slash | Aqua Jet 34, Taunt 40, Agility 45, Skull Bash 50, Night Slash 56 | Sharpedo |
| Sharpedo | super rod | 30 | Rewrite | Swagger, Assurance, Crunch, Slash | Aqua Jet 34, Taunt 40, Agility 45, Liquidation 46, Skull Bash 50, Poison Jab 52, Night Slash 56 | Sharpedo |
| Alomomola | super rod | 33 | Oxide | Protect, Water Pulse, Wake-Up Slap, Soak | Wish 37, Brine 41, Safeguard 45, Whirlpool 49, Helping Hand 53 | Alomomola |
| Alomomola | super rod | 33 | Rewrite | Water Pulse, Heal Pulse, Low Sweep, Soak | Wake-Up Slap 34, Agility 35, Wish 37, Play Rough 39, Brine 41, Zen Headbutt 43, Safeguard 45, Whirlpool 49, Helping Hand 53, Liquidation 55 | Alomomola |
| Floatzel | super rod | 33 to 36 | Oxide | Swift, Aqua Jet, Crunch, Agility | Whirlpool 39, Razor Wind 50 | Floatzel |
| Floatzel | super rod | 33 to 36 | Rewrite | Aqua Jet, Crunch, Flip Turn, Icy Wind | Waterfall 35, Whirlpool 39, Liquidation 43, Low Sweep 45, Rock Tomb 51, Agility 52 | Floatzel |

## Fuego Ironworks

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 56 | At the cap |
|---|---|---|---|---|---|---|
| Seaking | super rod | 36 | Oxide | Water Pulse, Flail, Aqua Ring, Fury Attack | Waterfall 40, Horn Drill 47, Agility 56 | Seaking |
| Seaking | super rod | 36 | Rewrite | Flail, Aqua Ring, Bulldoze, Aqua Jet | Waterfall 40, Poison Jab 42, Throat Chop 44, Aqua Tail 50, Drill Peck 52, Agility 56 | Seaking |
| Whiscash | super rod | 36 | Oxide | Water Pulse, Magnitude, Rest, Snore | Aqua Tail 39, Earthquake 45, Future Sight 51 | Whiscash |
| Whiscash | super rod | 36 | Rewrite | Magnitude, Bulldoze, Rest, Zen Headbutt | Aqua Tail 39, Wild Charge 42, Earthquake 45, Future Sight 51, Ice Beam 53 | Whiscash |
| Crawdaunt | super rod | 39 | Oxide | Knock Off, Swift, Taunt, Night Slash | Crabhammer 44, Swords Dance 52 | Crawdaunt |
| Crawdaunt | super rod | 39 | Rewrite | Swift, Taunt, Metal Claw, Night Slash | Throat Chop 41, Crabhammer 44, X-Scissor 46, Swords Dance 52 | Crawdaunt |
| Lanturn | super rod | 39 | Oxide | Swallow, Spit Up, BubbleBeam, Signal Beam | Discharge 40, Aqua Ring 47, Hydro Pump 52 | Lanturn |
| Lanturn | super rod | 39 | Rewrite | Spit Up, BubbleBeam, Signal Beam, Scald | Discharge 40, Thunderbolt 42, Aqua Ring 47, Muddy Water 52 | Lanturn |
| Relicanth | super rod | 42 | Oxide | Rock Tomb, Yawn, Take Down, Mud Sport | AncientPower 43, Double-Edge 50 | Relicanth |
| Relicanth | super rod | 42 | Rewrite | Water Gun, Rock Tomb, Yawn, Take Down | AncientPower 43, Bulldoze 45, Double-Edge 50, Aqua Tail 54 | Relicanth |

## Great Marsh

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 56 | At the cap |
|---|---|---|---|---|---|---|
| Araquanid | super rod | 35 to 38 | Oxide | BubbleBeam, Bug Bite, Headbutt, Soak | Dive 36, Lunge 41, Scald 48, Hydro Pump 51, Liquidation 55 | Araquanid |
| Araquanid | super rod | 35 to 38 | Rewrite | Bug Bite, Headbutt, Spider Web, Soak | Dive 36, Skitter Smack 38, Lunge 41, Waterfall 43, Scald 48, Poison Jab 51, Liquidation 55 | Araquanid |
| Crawdaunt | super rod | 35 to 38 | Oxide | Protect, Knock Off, Swift, Taunt | Night Slash 39, Crabhammer 44, Swords Dance 52 | Crawdaunt |
| Crawdaunt | super rod | 35 to 38 | Rewrite | BubbleBeam, Knock Off, Swift, Taunt | Metal Claw 36, Night Slash 39, Throat Chop 41, Crabhammer 44, X-Scissor 46, Swords Dance 52 | Crawdaunt |
| Jellicent | super rod | 35 to 38 | Oxide | Imprison, Confuse Ray, Hex, Brine | Pain Split 39, Destiny Bond 45, Shadow Ball 51, Scald 55 | Jellicent |
| Jellicent | super rod | 35 to 38 | Rewrite | Imprison, Confuse Ray, Hex, Brine | Pain Split 39, Muddy Water 45, Shadow Ball 51, Sludge Bomb 53, Scald 55 | Jellicent |
| Kingdra | super rod | 35 | Oxide | BubbleBeam, Agility, Twister, Brine | Hydro Pump 40, Dragon Dance 48 | Kingdra |
| Kingdra | super rod | 35 | Rewrite | Agility, Twister, Brine, Aurora Beam | Octazooka 40, Scald 54 | Kingdra |
| Lombre | super rod | 35 | Oxide | Fury Swipes, Water Sport, BubbleBeam, Zen Headbutt | nothing | Ludicolo (from 35) |
| Lombre | super rod | 35 | Rewrite | Water Sport, BubbleBeam, Zen Headbutt, Icy Wind | as Ludicolo: Mud Shot 40, Muddy Water 54, Giga Drain 56 | Ludicolo (from 35) |
| Ludicolo | super rod | 35 to 38 | Oxide | Astonish, Growl, Mega Drain, Nature Power | nothing | Ludicolo |
| Ludicolo | super rod | 35 to 38 | Rewrite | Growl, Mega Drain, Nature Power, Energy Ball | Mud Shot 40, Muddy Water 54, Giga Drain 56 | Ludicolo |
| Sharpedo | super rod | 35 | Oxide | Assurance, Crunch, Slash, Aqua Jet | Taunt 40, Agility 45, Skull Bash 50, Night Slash 56 | Sharpedo |
| Sharpedo | super rod | 35 | Rewrite | Assurance, Crunch, Slash, Aqua Jet | Taunt 40, Agility 45, Liquidation 46, Skull Bash 50, Poison Jab 52, Night Slash 56 | Sharpedo |
| Wailmer | super rod | 35 | Oxide | Mist, Rest, Brine, Water Spout | Amnesia 37; as Wailord: Dive 46, Bounce 54 | Wailord (from 40) |
| Wailmer | super rod | 35 | Rewrite | Mist, Rest, Brine, Water Spout | Amnesia 37; as Wailord: Dive 46, Rock Tomb 48, Iron Head 50, Bounce 54, Zen Headbutt 56 | Wailord (from 40) |
| Kingler | super rod | 38 | Oxide | Metal Claw, Stomp, Protect, Guillotine | Slam 44, Brine 51, Crabhammer 56 | Kingler |
| Kingler | super rod | 38 | Rewrite | Stomp, Rock Tomb, Razor Shell, Waterfall | X-Scissor 42, Slam 44, Brine 51, Crabhammer 56 | Kingler |
| Quagsire | super rod | 38 | Oxide | Mud Bomb, Amnesia, Yawn, Earthquake | Mist 48, Haze 48, Muddy Water 53 | Quagsire |
| Quagsire | super rod | 38 | Rewrite | Amnesia, Bulldoze, Yawn, Earthquake | Toxic 40, Drain Punch 43, Mist 48, Aqua Tail 51, Muddy Water 53 | Quagsire |
| Qwilfish | super rod | 38 to 41 | Oxide | Spit Up, Revenge, Brine, Pin Missile | Take Down 41, Aqua Tail 45, Poison Jab 49, Destiny Bond 53 | Qwilfish |
| Qwilfish | super rod | 38 to 41 | Rewrite | Stockpile, Revenge, Brine, Pin Missile | Take Down 41, Aqua Tail 45, Poison Jab 49, Throat Chop 51 | Qwilfish |
| Whiscash | super rod | 38 | Oxide | Water Pulse, Magnitude, Rest, Snore | Aqua Tail 39, Earthquake 45, Future Sight 51 | Whiscash |
| Whiscash | super rod | 38 | Rewrite | Magnitude, Bulldoze, Rest, Zen Headbutt | Aqua Tail 39, Wild Charge 42, Earthquake 45, Future Sight 51, Ice Beam 53 | Whiscash |
| Corsola | super rod | 41 | Oxide | Lucky Chant, AncientPower, Aqua Ring, Spike Cannon | Power Gem 44, Mirror Coat 48, Earth Power 53 | Corsola |
| Corsola | super rod | 41 | Rewrite | Lucky Chant, Rock Slide, Aqua Ring, Spike Cannon | Liquidation 42, Power Gem 44, Throat Chop 46, Mirror Coat 48, Earth Power 53, Body Slam 55 | Corsola |
| Feraligatr | super rod | 41 | Oxide | Flail, Agility, Crunch, Slash | Screech 45, Thrash 50 | Feraligatr |
| Feraligatr | super rod | 41 | Rewrite | Agility, Crunch, Bulldoze, Slash | Brick Break 42, Screech 45, Aqua Tail 50 | Feraligatr |
| Greninja | super rod | 41 | Oxide | Waterfall, Fling, Scald, Dark Pulse | Extrasensory 43, Sludge Wave 47, Gunk Shot 51, Hydro Pump 55 | Greninja |
| Greninja | super rod | 41 | Rewrite | Fling, Shadow Sneak, Scald, Dark Pulse | Extrasensory 43, Sludge Wave 47, Surf 49, Gunk Shot 51, Ice Beam 56 | Greninja |
| Pelipper | super rod | 41 | Oxide | Roost, Stockpile, Swallow, Spit Up | Fling 43, Tailwind 50 | Pelipper |
| Pelipper | super rod | 41 | Rewrite | Muddy Water, Swallow, Stockpile, Spit Up | Fling 43, Icy Wind 45, Tailwind 50, Air Slash 52, Acrobatics 54 | Pelipper |

## Iron Island

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 56 | At the cap |
|---|---|---|---|---|---|---|
| Gastrodon | super rod | 36 | Oxide | Water Pulse, Mud Bomb, Hidden Power, Body Slam | Muddy Water 41, Recover 54 | Gastrodon |
| Gastrodon | super rod | 36 | Rewrite | Hidden Power, Body Slam, AncientPower, Clear Smog | Muddy Water 41, Earth Power 43, Bulldoze 45, Ice Beam 50, Recover 54 | Gastrodon |
| Jellicent | super rod | 36 | Oxide | Imprison, Confuse Ray, Hex, Brine | Pain Split 39, Destiny Bond 45, Shadow Ball 51, Scald 55 | Jellicent |
| Jellicent | super rod | 36 | Rewrite | Imprison, Confuse Ray, Hex, Brine | Pain Split 39, Muddy Water 45, Shadow Ball 51, Sludge Bomb 53, Scald 55 | Jellicent |
| Lanturn | super rod | 39 | Oxide | Swallow, Spit Up, BubbleBeam, Signal Beam | Discharge 40, Aqua Ring 47, Hydro Pump 52 | Lanturn |
| Lanturn | super rod | 39 | Rewrite | Spit Up, BubbleBeam, Signal Beam, Scald | Discharge 40, Thunderbolt 42, Aqua Ring 47, Muddy Water 52 | Lanturn |
| Lumineon | super rod | 39 to 42 | Oxide | Water Pulse, Captivate, Safeguard, Aqua Ring | Whirlpool 42, U-turn 48, Bounce 53 | Lumineon |
| Lumineon | super rod | 39 to 42 | Rewrite | Safeguard, Flip Turn, Aqua Ring, Aqua Tail | Whirlpool 42, U-turn 48, Ice Fang 50, Bounce 53, Air Slash 55 | Lumineon |

## Lake Acuity

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 56 | At the cap |
|---|---|---|---|---|---|---|
| Chinchou | old rod | 16 | Oxide | Supersonic, Thunder Wave, Flail, Water Gun | Confuse Ray 17, Spark 20, Take Down 23; as Lanturn: Stockpile 27, Swallow 27, Spit Up 27, BubbleBeam 30, Signal Beam 35, Discharge 40, Aqua Ring 47, Hydro Pump 52 | Lanturn (from 27) |
| Chinchou | old rod | 16 | Rewrite | Thunder Wave, Flail, Water Gun, Screech | Confuse Ray 17, Icy Wind 19, Take Down 23; as Lanturn: Stockpile 27, Swallow 28, Spit Up 29, BubbleBeam 30, Signal Beam 35, Scald 37, Discharge 40, Thunderbolt 42, Aqua Ring 47, Muddy Water 52 | Lanturn (from 27) |
| Clamperl | old rod | 16 | Oxide | Clamp, Water Gun, Whirlpool, Iron Defense | as Huntail: Scary Face 19, Ice Fang 24, Brine 28, Baton Pass 33, Dive 37, Crunch 42, Aqua Tail 46, Hydro Pump 51 | Huntail (from 16) |
| Clamperl | old rod | 16 | Oxide | Clamp, Water Gun, Whirlpool, Iron Defense | as Gorebyss: Amnesia 19, Aqua Ring 24, Captivate 28, Baton Pass 33, Dive 37, Psychic 42, Aqua Tail 46, Hydro Pump 51 | Gorebyss (from 16) |
| Clamperl | old rod | 16 | Rewrite | Clamp, Water Gun, Whirlpool, Iron Defense | as Huntail: Scary Face 19, Ice Fang 24, Brine 28, Flip Turn 34, Dive 37, Crunch 42, Aqua Tail 46, Shell Smash 50, Muddy Water 51, Rock Tomb 56 | Huntail (from 16) |
| Clamperl | old rod | 16 | Rewrite | Clamp, Water Gun, Whirlpool, Iron Defense | as Gorebyss: Amnesia 19, Aqua Ring 24, Captivate 28, Baton Pass 33, Draining Kiss 35, Dive 37, Muddy Water 40, Psychic 42, Aqua Tail 46, Shadow Ball 48, Giga Drain 50, Scald 56 | Gorebyss (from 16) |
| Barboach | old rod | 17 | Oxide | Mud Sport, Water Sport, Water Gun, Mud Bomb | Amnesia 18, Water Pulse 22, Magnitude 26; as Whiscash: Rest 33, Snore 33, Aqua Tail 39, Earthquake 45, Future Sight 51 | Whiscash (from 30) |
| Barboach | old rod | 17 | Rewrite | Scary Face, Water Sport, Water Gun, Mud Bomb | Amnesia 18, Rock Tomb 20, Water Pulse 22, Magnitude 26; as Whiscash: Bulldoze 30, Rest 33, Zen Headbutt 35, Aqua Tail 39, Wild Charge 42, Earthquake 45, Future Sight 51, Ice Beam 53 | Whiscash (from 30) |
| Goldeen | old rod | 17 | Oxide | Water Sport, Supersonic, Horn Attack, Water Pulse | Flail 21, Aqua Ring 27, Fury Attack 31; as Seaking: Waterfall 40, Horn Drill 47, Agility 56 | Seaking (from 33) |
| Goldeen | old rod | 17 | Rewrite | Water Sport, Water Pulse, Flip Turn, Horn Attack | Agility 20, Flail 21, Aqua Ring 27; as Seaking: Bulldoze 33, Aqua Jet 35, Waterfall 40, Poison Jab 42, Throat Chop 44, Aqua Tail 50, Drill Peck 52, Agility 56 | Seaking (from 33) |
| Frogadier | old rod | 18 | Oxide | Quick Attack, Lick, Water Pulse, Icy Wind | Faint Attack 20, Acrobatics 22, Low Kick 25, Waterfall 30, Fling 35; as Greninja: Scald 37, Dark Pulse 40, Extrasensory 43, Sludge Wave 47, Gunk Shot 51, Hydro Pump 55 | Greninja (from 36) |
| Frogadier | old rod | 18 | Rewrite | Quick Attack, Lick, Water Pulse, Icy Wind | Thief 19, Faint Attack 20, Acrobatics 22, Low Kick 25, Waterfall 30, Fling 35; as Greninja: Shadow Sneak 36, Scald 37, Dark Pulse 40, Extrasensory 43, Sludge Wave 47, Surf 49, Gunk Shot 51, Ice Beam 56 | Greninja (from 36) |
| Barboach | good rod | 28 | Oxide | Mud Bomb, Amnesia, Water Pulse, Magnitude | as Whiscash: Rest 33, Snore 33, Aqua Tail 39, Earthquake 45, Future Sight 51 | Whiscash (from 30) |
| Barboach | good rod | 28 | Rewrite | Amnesia, Rock Tomb, Water Pulse, Magnitude | as Whiscash: Bulldoze 30, Rest 33, Zen Headbutt 35, Aqua Tail 39, Wild Charge 42, Earthquake 45, Future Sight 51, Ice Beam 53 | Whiscash (from 30) |
| Feebas | good rod | 28 | Oxide | Splash, Tackle | Flail 30; as Milotic: Hydro Pump 37, Attract 41, Safeguard 45, Aqua Ring 49 | Milotic (from 30) |
| Feebas | good rod | 28 | Rewrite | Dragon Tail, Water Pulse, Tackle, Captivate | Flail 30; as Milotic: Twister 30, Recover 31, Aqua Tail 32, Aurora Beam 33, Surf 37, Attract 41, Safeguard 45, Aqua Ring 49, Alluring Voice 51, Dragon Pulse 54 | Milotic (from 30) |
| Corphish | good rod | 30 | Oxide | Leer, BubbleBeam, Protect, Knock Off | as Crawdaunt: Taunt 34, Night Slash 39, Crabhammer 44, Swords Dance 52 | Crawdaunt (from 31) |
| Corphish | good rod | 30 | Rewrite | Leer, Aerial Ace, Razor Shell, Knock Off | as Crawdaunt: Taunt 34, Metal Claw 36, Night Slash 39, Throat Chop 41, Crabhammer 44, X-Scissor 46, Swords Dance 52 | Crawdaunt (from 31) |
| Wailmer | good rod | 30 | Oxide | Astonish, Water Pulse, Mist, Rest | Brine 31, Water Spout 34, Amnesia 37; as Wailord: Dive 46, Bounce 54 | Wailord (from 40) |
| Wailmer | good rod | 30 | Rewrite | Astonish, Water Pulse, Mist, Rest | Brine 31, Water Spout 34, Amnesia 37; as Wailord: Dive 46, Rock Tomb 48, Iron Head 50, Bounce 54, Zen Headbutt 56 | Wailord (from 40) |
| Lapras | good rod | 32 | Oxide | Water Pulse, Body Slam, Perish Song, Ice Beam | Brine 37, Safeguard 43, Hydro Pump 49, Sheer Cold 55 | Lapras |
| Lapras | good rod | 32 | Rewrite | Water Pulse, Body Slam, Perish Song, Ice Beam | Confuse Ray 33, Brine 37, Safeguard 43, Muddy Water 49, Drill Run 54 | Lapras |
| Floatzel | surf | 34 | Oxide | Swift, Aqua Jet, Crunch, Agility | Whirlpool 39, Razor Wind 50 | Floatzel |
| Floatzel | surf | 34 | Rewrite | Aqua Jet, Crunch, Flip Turn, Icy Wind | Waterfall 35, Whirlpool 39, Liquidation 43, Low Sweep 45, Rock Tomb 51, Agility 52 | Floatzel |
| Jellicent | surf | 34 | Oxide | Imprison, Confuse Ray, Hex, Brine | Pain Split 39, Destiny Bond 45, Shadow Ball 51, Scald 55 | Jellicent |
| Jellicent | surf | 34 | Rewrite | Imprison, Confuse Ray, Hex, Brine | Pain Split 39, Muddy Water 45, Shadow Ball 51, Sludge Bomb 53, Scald 55 | Jellicent |
| Buizel | surf | 37 | Oxide | Swift, Aqua Jet, Agility, Whirlpool | as Floatzel: Whirlpool 39, Razor Wind 50 | Floatzel (from 38) |
| Buizel | surf | 37 | Rewrite | Swift, Aqua Jet, Agility, Whirlpool | as Floatzel: Whirlpool 39, Liquidation 43, Low Sweep 45, Rock Tomb 51, Agility 52 | Floatzel (from 38) |
| Dewgong | surf | 37 | Oxide | Aqua Jet, Brine, Sheer Cold, Take Down | Dive 41, Aqua Tail 43, Ice Beam 47, Safeguard 51 | Dewgong |
| Dewgong | surf | 37 | Rewrite | Aqua Jet, Brine, Signal Beam, Take Down | Dive 41, Aqua Tail 43, Drill Run 45, Ice Beam 47, Safeguard 51, Bite 54, Headbutt 56 | Dewgong |
| Crawdaunt | super rod | 38 | Oxide | Protect, Knock Off, Swift, Taunt | Night Slash 39, Crabhammer 44, Swords Dance 52 | Crawdaunt |
| Crawdaunt | super rod | 38 | Rewrite | Knock Off, Swift, Taunt, Metal Claw | Night Slash 39, Throat Chop 41, Crabhammer 44, X-Scissor 46, Swords Dance 52 | Crawdaunt |
| Milotic | super rod | 38 | Oxide | Recover, Captivate, Aqua Tail, Hydro Pump | Attract 41, Safeguard 45, Aqua Ring 49 | Milotic |
| Milotic | super rod | 38 | Rewrite | Recover, Aqua Tail, Aurora Beam, Surf | Attract 41, Safeguard 45, Aqua Ring 49, Alluring Voice 51, Dragon Pulse 54 | Milotic |
| Snorunt | wild | 38 to 41 | Oxide | Protect, Ice Fang, Crunch, Ice Shard | as Glalie: Blizzard 51 | Glalie (from 42) |
| Snorunt | wild | 38 to 41 | Oxide | Protect, Ice Fang, Crunch, Ice Shard | as Froslass: Blizzard 51 | Froslass (from 38) |
| Snorunt | wild | 38 to 41 | Rewrite | Ice Fang, Crunch, Draining Kiss, Ice Shard | as Glalie: Rock Slide 42, Power Gem 44, Earth Power 46, Icicle Crash 48, Shadow Ball 53, Dark Pulse 55 | Glalie (from 42) |
| Snorunt | wild | 38 to 41 | Rewrite | Ice Fang, Crunch, Draining Kiss, Ice Shard | as Froslass: Signal Beam 44, Ice Beam 51 | Froslass (from 38) |
| Absol | wild | 39 to 40 | Oxide | Swords Dance, Bite, Double Team, Slash | Future Sight 41, Sucker Punch 44, Detect 49, Night Slash 52 | Absol |
| Absol | wild | 39 to 40 | Rewrite | Pursuit, Swords Dance, Bite, Slash | Future Sight 41, Sucker Punch 44, X-Scissor 46, Night Slash 52, Throat Chop 54 | Absol |
| Alolan Ninetales | wild | 39 | Oxide | Tail Whip, Disable, Ice Shard, Safeguard | nothing | Alolan Ninetales |
| Alolan Ninetales | wild | 39 | Rewrite | Icy Wind, Payback, Dazzling Gleam, Chilling Water | Ice Beam 43, Extrasensory 44, Foul Play 51, Confuse Ray 53 | Alolan Ninetales |
| Frosmoth | wild | 39 | Oxide | FeatherDance, Aurora Beam, Bug Buzz, Aurora Veil | Blizzard 40, Tailwind 44, Wide Guard 48, Quiver Dance 52 | Frosmoth |
| Frosmoth | wild | 39 | Rewrite | Defog, Aurora Beam, Aurora Veil, Psybeam | Ice Beam 40, Tailwind 44, Wide Guard 48, Giga Drain 50, Quiver Dance 52 | Frosmoth |
| Jynx | wild | 39 | Oxide | Fake Tears, Wake-Up Slap, Avalanche, Body Slam | Wring Out 44, Perish Song 49, Blizzard 55 | Jynx |
| Jynx | wild | 39 | Rewrite | Ice Punch, Wake-Up Slap, Avalanche, Body Slam | Psychic 41, Shadow Ball 43, Perish Song 49, Signal Beam 51, Ice Beam 55 | Jynx |
| Weavile | wild | 39 to 41 | Oxide | Nasty Plot, Icy Wind, Night Slash, Fling | Metal Claw 42, Dark Pulse 49 | Weavile |
| Weavile | wild | 39 to 41 | Rewrite | Fury Swipes, Icy Wind, Night Slash, Fling | Metal Claw 42, Dark Pulse 49 | Weavile |
| Abomasnow | wild | 40 to 41 | Oxide | Mist, Ice Shard, Ingrain, Wood Hammer | Blizzard 47 | Abomasnow |
| Abomasnow | wild | 40 to 41 | Rewrite | Swagger, Mist, Ice Shard, Wood Hammer | Ice Punch 45, Ice Beam 47, Body Press 53, Giga Drain 55 | Abomasnow |
| Galarian Mr Mime | wild | 40 | Oxide | Psybeam, Hypnosis, Mirror Coat, Sucker Punch | as Mr. Rime: Freeze-Dry 44, Psychic 48, Teeter Dance 52 | Mr. Rime (from 42) |
| Galarian Mr Mime | wild | 40 | Rewrite | Psybeam, Hypnosis, Mirror Coat, Sucker Punch | Dazzling Gleam 42; as Mr. Rime: Freeze-Dry 44, Psychic 48, Teeter Dance 52, Encore 54, Ice Beam 56 | Mr. Rime (from 42) |
| Lapras | surf | 40 | Oxide | Body Slam, Perish Song, Ice Beam, Brine | Safeguard 43, Hydro Pump 49, Sheer Cold 55 | Lapras |
| Lapras | surf | 40 | Rewrite | Perish Song, Ice Beam, Confuse Ray, Brine | Safeguard 43, Muddy Water 49, Drill Run 54 | Lapras |
| Lanturn | super rod | 41 | Oxide | Spit Up, BubbleBeam, Signal Beam, Discharge | Aqua Ring 47, Hydro Pump 52 | Lanturn |
| Lanturn | super rod | 41 | Rewrite | BubbleBeam, Signal Beam, Scald, Discharge | Thunderbolt 42, Aqua Ring 47, Muddy Water 52 | Lanturn |
| Qwilfish | super rod | 41 | Oxide | Revenge, Brine, Pin Missile, Take Down | Aqua Tail 45, Poison Jab 49, Destiny Bond 53 | Qwilfish |
| Qwilfish | super rod | 41 | Rewrite | Revenge, Brine, Pin Missile, Take Down | Aqua Tail 45, Poison Jab 49, Throat Chop 51 | Qwilfish |
| Gorebyss | super rod | 44 | Oxide | Captivate, Baton Pass, Dive, Psychic | Aqua Tail 46, Hydro Pump 51 | Gorebyss |
| Gorebyss | super rod | 44 | Rewrite | Draining Kiss, Dive, Muddy Water, Psychic | Aqua Tail 46, Shadow Ball 48, Giga Drain 50, Scald 56 | Gorebyss |

## Lake Valor

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 56 | At the cap |
|---|---|---|---|---|---|---|
| Milotic | super rod | 36 | Oxide | Twister, Recover, Captivate, Aqua Tail | Hydro Pump 37, Attract 41, Safeguard 45, Aqua Ring 49 | Milotic |
| Milotic | super rod | 36 | Rewrite | Twister, Recover, Aqua Tail, Aurora Beam | Surf 37, Attract 41, Safeguard 45, Aqua Ring 49, Alluring Voice 51, Dragon Pulse 54 | Milotic |
| Whiscash | super rod | 36 | Oxide | Water Pulse, Magnitude, Rest, Snore | Aqua Tail 39, Earthquake 45, Future Sight 51 | Whiscash |
| Whiscash | super rod | 36 | Rewrite | Magnitude, Bulldoze, Rest, Zen Headbutt | Aqua Tail 39, Wild Charge 42, Earthquake 45, Future Sight 51, Ice Beam 53 | Whiscash |
| Crawdaunt | super rod | 39 | Oxide | Knock Off, Swift, Taunt, Night Slash | Crabhammer 44, Swords Dance 52 | Crawdaunt |
| Crawdaunt | super rod | 39 | Rewrite | Swift, Taunt, Metal Claw, Night Slash | Throat Chop 41, Crabhammer 44, X-Scissor 46, Swords Dance 52 | Crawdaunt |
| Lanturn | super rod | 39 | Oxide | Swallow, Spit Up, BubbleBeam, Signal Beam | Discharge 40, Aqua Ring 47, Hydro Pump 52 | Lanturn |
| Lanturn | super rod | 39 | Rewrite | Spit Up, BubbleBeam, Signal Beam, Scald | Discharge 40, Thunderbolt 42, Aqua Ring 47, Muddy Water 52 | Lanturn |
| Corsola | super rod | 42 | Oxide | Lucky Chant, AncientPower, Aqua Ring, Spike Cannon | Power Gem 44, Mirror Coat 48, Earth Power 53 | Corsola |
| Corsola | super rod | 42 | Rewrite | Rock Slide, Aqua Ring, Spike Cannon, Liquidation | Power Gem 44, Throat Chop 46, Mirror Coat 48, Earth Power 53, Body Slam 55 | Corsola |

## Lake Verity

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 56 | At the cap |
|---|---|---|---|---|---|---|
| Lanturn | super rod | 30 | Oxide | Stockpile, Swallow, Spit Up, BubbleBeam | Signal Beam 35, Discharge 40, Aqua Ring 47, Hydro Pump 52 | Lanturn |
| Lanturn | super rod | 30 | Rewrite | Stockpile, Swallow, Spit Up, BubbleBeam | Signal Beam 35, Scald 37, Discharge 40, Thunderbolt 42, Aqua Ring 47, Muddy Water 52 | Lanturn |
| Sharpedo | super rod | 30 | Oxide | Swagger, Assurance, Crunch, Slash | Aqua Jet 34, Taunt 40, Agility 45, Skull Bash 50, Night Slash 56 | Sharpedo |
| Sharpedo | super rod | 30 | Rewrite | Swagger, Assurance, Crunch, Slash | Aqua Jet 34, Taunt 40, Agility 45, Liquidation 46, Skull Bash 50, Poison Jab 52, Night Slash 56 | Sharpedo |
| Floatzel | super rod | 33 | Oxide | Swift, Aqua Jet, Crunch, Agility | Whirlpool 39, Razor Wind 50 | Floatzel |
| Floatzel | super rod | 33 | Rewrite | Aqua Jet, Crunch, Flip Turn, Icy Wind | Waterfall 35, Whirlpool 39, Liquidation 43, Low Sweep 45, Rock Tomb 51, Agility 52 | Floatzel |
| Kingler | super rod | 33 | Oxide | Mud Shot, Metal Claw, Stomp, Protect | Guillotine 37, Slam 44, Brine 51, Crabhammer 56 | Kingler |
| Kingler | super rod | 33 | Rewrite | BubbleBeam, Mud Shot, Metal Claw, Stomp | Rock Tomb 34, Razor Shell 36, Waterfall 38, X-Scissor 42, Slam 44, Brine 51, Crabhammer 56 | Kingler |
| Greninja | super rod | 36 | Oxide | Acrobatics, Low Kick, Waterfall, Fling | Scald 37, Dark Pulse 40, Extrasensory 43, Sludge Wave 47, Gunk Shot 51, Hydro Pump 55 | Greninja |
| Greninja | super rod | 36 | Rewrite | Low Kick, Waterfall, Fling, Shadow Sneak | Scald 37, Dark Pulse 40, Extrasensory 43, Sludge Wave 47, Surf 49, Gunk Shot 51, Ice Beam 56 | Greninja |

## Mt. Coronet B1F

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 56 | At the cap |
|---|---|---|---|---|---|---|
| Feebas | old rod | 18 | Oxide | Splash, Tackle | Flail 30; as Milotic: Hydro Pump 37, Attract 41, Safeguard 45, Aqua Ring 49 | Milotic (from 30) |
| Feebas | old rod | 18 | Rewrite | Swagger, Dragon Tail, Water Pulse, Tackle | Captivate 25, Flail 30; as Milotic: Twister 30, Recover 31, Aqua Tail 32, Aurora Beam 33, Surf 37, Attract 41, Safeguard 45, Aqua Ring 49, Alluring Voice 51, Dragon Pulse 54 | Milotic (from 30) |
| Horsea | old rod | 18 | Oxide | Leer, Water Gun, Focus Energy, BubbleBeam | Agility 23, Twister 26, Brine 30; as Kingdra: Hydro Pump 40, Dragon Dance 48 | Kingdra (from 32) |
| Horsea | old rod | 18 | Rewrite | SmokeScreen, Water Gun, Focus Energy, BubbleBeam | Agility 23, Twister 26, Brine 30; as Kingdra: Aurora Beam 32, Octazooka 40, Scald 54 | Kingdra (from 32) |
| Croconaw | old rod | 19 | Oxide | Water Gun, Rage, Bite, Scary Face | Ice Fang 21, Flail 24, Crunch 30; as Feraligatr: Agility 30, Crunch 32, Slash 37, Screech 45, Thrash 50 | Feraligatr (from 30) |
| Croconaw | old rod | 19 | Rewrite | Leer, Water Gun, Bite, Scary Face | Ice Fang 21, Flail 24, Crunch 30; as Feraligatr: Agility 30, Crunch 32, Bulldoze 34, Slash 37, Brick Break 42, Screech 45, Aqua Tail 50 | Feraligatr (from 30) |
| Goldeen | old rod | 19 | Oxide | Water Sport, Supersonic, Horn Attack, Water Pulse | Flail 21, Aqua Ring 27, Fury Attack 31; as Seaking: Waterfall 40, Horn Drill 47, Agility 56 | Seaking (from 33) |
| Goldeen | old rod | 19 | Rewrite | Water Sport, Water Pulse, Flip Turn, Horn Attack | Agility 20, Flail 21, Aqua Ring 27; as Seaking: Bulldoze 33, Aqua Jet 35, Waterfall 40, Poison Jab 42, Throat Chop 44, Aqua Tail 50, Drill Peck 52, Agility 56 | Seaking (from 33) |
| Seel | old rod | 20 | Oxide | Water Sport, Icy Wind, Encore, Ice Shard | Rest 21, Aqua Ring 23, Aurora Beam 27, Aqua Jet 31, Brine 33; as Dewgong: Sheer Cold 34, Take Down 37, Dive 41, Aqua Tail 43, Ice Beam 47, Safeguard 51 | Dewgong (from 34) |
| Seel | old rod | 20 | Rewrite | Water Sport, Icy Wind, Encore, Ice Shard | Rest 21, Aqua Ring 23, Aurora Beam 27, Aqua Jet 31, Brine 33; as Dewgong: Signal Beam 34, Take Down 37, Dive 41, Aqua Tail 43, Drill Run 45, Ice Beam 47, Safeguard 51, Bite 54, Headbutt 56 | Dewgong (from 34) |
| Corphish | good rod | 30 | Oxide | Leer, BubbleBeam, Protect, Knock Off | as Crawdaunt: Taunt 34, Night Slash 39, Crabhammer 44, Swords Dance 52 | Crawdaunt (from 31) |
| Corphish | good rod | 30 | Rewrite | Leer, Aerial Ace, Razor Shell, Knock Off | as Crawdaunt: Taunt 34, Metal Claw 36, Night Slash 39, Throat Chop 41, Crabhammer 44, X-Scissor 46, Swords Dance 52 | Crawdaunt (from 31) |
| Feebas | good rod | 30 | Oxide | Splash, Tackle, Flail | as Milotic: Hydro Pump 37, Attract 41, Safeguard 45, Aqua Ring 49 | Milotic (from 31) |
| Feebas | good rod | 30 | Rewrite | Water Pulse, Tackle, Captivate, Flail | as Milotic: Recover 31, Aqua Tail 32, Aurora Beam 33, Surf 37, Attract 41, Safeguard 45, Aqua Ring 49, Alluring Voice 51, Dragon Pulse 54 | Milotic (from 31) |
| Chinchou | good rod | 32 | Oxide | Spark, Take Down, BubbleBeam, Signal Beam | as Lanturn: Signal Beam 35, Discharge 40, Aqua Ring 47, Hydro Pump 52 | Lanturn (from 33) |
| Chinchou | good rod | 32 | Rewrite | Icy Wind, Take Down, BubbleBeam, Signal Beam | as Lanturn: Signal Beam 35, Scald 37, Discharge 40, Thunderbolt 42, Aqua Ring 47, Muddy Water 52 | Lanturn (from 33) |
| Frillish | good rod | 32 | Oxide | Water Pulse, Imprison, Confuse Ray, Hex | Brine 34, Pain Split 39; as Jellicent: Destiny Bond 45, Shadow Ball 51, Scald 55 | Jellicent (from 40) |
| Frillish | good rod | 32 | Rewrite | Water Pulse, Imprison, Confuse Ray, Hex | Brine 34, Dark Pulse 36, Pain Split 39; as Jellicent: Muddy Water 45, Shadow Ball 51, Sludge Bomb 53, Scald 55 | Jellicent (from 40) |
| Goomy | wild | 32 | Oxide | Life Dew, Flail, Water Pulse, Dragon Tail | Infestation 34; as Sliggoo: Body Slam 42, Muddy Water 48; as Goodra: Aqua Tail 55 | Goodra (from 50) |
| Goomy | wild | 32 | Oxide | Life Dew, Flail, Water Pulse, Dragon Tail | as Hisuian Sliggoo: Dragon Pulse 35, Curse 43, Iron Head 49; as Hisuian Goodra: Iron Tail 55 | Hisuian Goodra (from 50) |
| Goomy | wild | 32 | Rewrite | Life Dew, Flail, Water Pulse, Dragon Tail | Infestation 34; as Sliggoo: Dragon Claw 40, Body Slam 42, Muddy Water 48; as Goodra: Aqua Tail 55 | Goodra (from 50) |
| Goomy | wild | 32 | Rewrite | Life Dew, Flail, Water Pulse, Dragon Tail | as Hisuian Sliggoo: Dragon Pulse 35, Flash Cannon 42, Curse 43, Iron Head 49; as Hisuian Goodra: Smart Strike 50, Body Slam 54, Iron Head 55 | Hisuian Goodra (from 50) |
| Bronzong | wild | 33 | Oxide | Extrasensory, Iron Defense, Safeguard, Block | Gyro Ball 38, Future Sight 43, Faint Attack 50 | Bronzong |
| Bronzong | wild | 33 | Rewrite | Extrasensory, Iron Defense, Safeguard, Block | Iron Head 35, Gyro Ball 38, Future Sight 43, Rock Tomb 45, Faint Attack 50, Body Press 52 | Bronzong |
| Carbink | wild | 33 to 34 | Oxide | Reflect, Flail, AncientPower, Rock Polish | Rock Slide 35, Stealth Rock 36, Skill Swap 40, Light Screen 44, Power Gem 45, Moonblast 52, Stone Edge 54 | Carbink |
| Carbink | wild | 33 to 34 | Rewrite | AncientPower, Rock Polish, Rock Tomb, Dazzling Gleam | Rock Slide 35, Stealth Rock 36, Skill Swap 40, Light Screen 44, Power Gem 45, Moonblast 52, Psychic 54 | Carbink |
| Donphan | wild | 33 | Oxide | Magnitude, Slam, Fury Attack, Assurance | Scary Face 39, Earthquake 46, Giga Impact 54 | Donphan |
| Donphan | wild | 33 | Rewrite | Rapid Spin, Magnitude, Rock Tomb, Assurance | Scary Face 39, Knock Off 40, Seed Bomb 43, Earthquake 46, Throat Chop 51, Giga Impact 54, Charm 56 | Donphan |
| Golbat | wild | 33 to 35 | Oxide | Wing Attack, Confuse Ray, Air Cutter, Mean Look | Poison Fang 39; as Crobat: Haze 45, Air Slash 51 | Crobat (from 40) |
| Golbat | wild | 33 to 35 | Rewrite | Wing Attack, Confuse Ray, Air Cutter, Mean Look | Poison Fang 39; as Crobat: Steel Wing 45, Air Slash 51, Poison Jab 53, Zen Headbutt 55 | Crobat (from 40) |
| Hariyama | wild | 33 | Oxide | Knock Off, SmellingSalt, Belly Drum, Force Palm | Seismic Toss 37, Wake-Up Slap 42, Endure 47, Close Combat 52 | Hariyama |
| Hariyama | wild | 33 | Rewrite | SmellingSalt, Belly Drum, Low Sweep, Force Palm | Bulldoze 35, Seismic Toss 37, Wake-Up Slap 42, Rock Tomb 44, Endure 47, Close Combat 52 | Hariyama |
| Mienfoo | wild | 33 | Oxide | Force Palm, Bounce, Drain Punch, Vacuum Wave | as Mienshao: Aura Sphere 38, Me First 40, Jump Kick 45, Dual Chop 48, Focus Blast 51, Acrobatics 55 | Mienshao (from 36) |
| Mienfoo | wild | 33 | Rewrite | Force Palm, Bounce, Drain Punch, Vacuum Wave | as Mienshao: Aura Sphere 38, Low Sweep 40, Jump Kick 45, Dual Chop 48, U-turn 50, Acrobatics 55 | Mienshao (from 36) |
| Naclstack | wild | 33 | Oxide | Rock Polish, Headbutt, Iron Defense, Recover | Rock Slide 34, Stealth Rock 38; as Garganacl: Stealth Rock 40, Heavy Slam 44, Earthquake 49, Stone Edge 54 | Garganacl (from 38) |
| Naclstack | wild | 33 | Rewrite | Iron Defense, Bulldoze, Rock Polish, Recover | Rock Slide 34, Stealth Rock 38; as Garganacl: Rock Tomb 38, Salt Cure 39, Stealth Rock 40, Iron Head 42, Heavy Slam 44, Earthquake 49, Zen Headbutt 51, Body Press 56 | Garganacl (from 38) |
| Dewgong | good rod | 34 | Oxide | Aurora Beam, Aqua Jet, Brine, Sheer Cold | Take Down 37, Dive 41, Aqua Tail 43, Ice Beam 47, Safeguard 51 | Dewgong |
| Dewgong | good rod | 34 | Rewrite | Aurora Beam, Aqua Jet, Brine, Signal Beam | Take Down 37, Dive 41, Aqua Tail 43, Drill Run 45, Ice Beam 47, Safeguard 51, Bite 54, Headbutt 56 | Dewgong |
| Glimmet | wild | 34 | Oxide | Stealth Rock, Venoshock, Selfdestruct, Rock Slide | as Glimmora: Power Gem 39, Acid Armor 44, Sludge Wave 50 | Glimmora (from 35) |
| Glimmet | wild | 34 | Rewrite | Stealth Rock, Mud Shot, Venoshock, Rock Slide | as Glimmora: Power Gem 39, Sludge Bomb 41, Acid Armor 44, Flash Cannon 48, Sludge Wave 50, Energy Ball 56 | Glimmora (from 35) |
| Graveler | wild | 34 | Oxide | Selfdestruct, Rollout, Rock Blast, Earthquake | Explosion 38; as Golem: Double-Edge 44, Stone Edge 49 | Golem (from 40) |
| Graveler | wild | 34 | Rewrite | Karate Chop, Rock Blast, Rock Tomb, Earthquake | Iron Head 35; as Golem: Double-Edge 44, Sucker Punch 46, Rock Slide 49, Body Slam 53, Body Press 55 | Golem (from 40) |
| Probopass | wild | 34 | Oxide | Magnet Bomb, Block, Thunder Wave, Rock Slide | Rest 43, Power Gem 49, Discharge 55 | Probopass |
| Probopass | wild | 34 | Rewrite | Thunder Wave, Rock Slide, Iron Defense, Magnet Bomb | Spark 35, Iron Head 37, Rest 43, Power Gem 49, Body Press 51, Discharge 55 | Probopass |
| Meditite | wild | 35 | Oxide | Feint, Calm Mind, Force Palm, Hi Jump Kick | Psych Up 36; as Medicham: Power Trick 42, Reversal 49, Recover 55 | Medicham (from 37) |
| Meditite | wild | 35 | Rewrite | Mind Reader, Rock Throw, Swagger, Hi Jump Kick | Psych Up 36; as Medicham: Low Sweep 37, Bulk Up 38, Iron Head 40, Power Trick 42, Reversal 49, Recover 55 | Medicham (from 37) |
| Sandygast | wild | 35 | Oxide | Mega Drain, Bulldoze, Hypnosis, Giga Drain | Iron Defense 36; as Palossand: Shadow Ball 44, Earth Power 50 | Palossand (from 42) |
| Sandygast | wild | 35 | Rewrite | Mega Drain, Bulldoze, Hypnosis, Giga Drain | Iron Defense 36; as Palossand: Shadow Ball 44, Sludge Bomb 46, Earth Power 50, Psychic 53 | Palossand (from 42) |
| Buizel | surf | 36 | Oxide | Swift, Aqua Jet, Agility, Whirlpool | as Floatzel: Whirlpool 39, Razor Wind 50 | Floatzel (from 37) |
| Buizel | surf | 36 | Rewrite | Swift, Aqua Jet, Agility, Whirlpool | as Floatzel: Whirlpool 39, Liquidation 43, Low Sweep 45, Rock Tomb 51, Agility 52 | Floatzel (from 37) |
| Floatzel | surf | 36 | Oxide | Swift, Aqua Jet, Crunch, Agility | Whirlpool 39, Razor Wind 50 | Floatzel |
| Floatzel | surf | 36 | Rewrite | Crunch, Flip Turn, Icy Wind, Waterfall | Whirlpool 39, Liquidation 43, Low Sweep 45, Rock Tomb 51, Agility 52 | Floatzel |
| Feebas | surf | 39 | Oxide | Splash, Tackle, Flail | as Milotic: Attract 41, Safeguard 45, Aqua Ring 49 | Milotic (from 40) |
| Feebas | surf | 39 | Rewrite | Water Pulse, Tackle, Captivate, Flail | as Milotic: Attract 41, Safeguard 45, Aqua Ring 49, Alluring Voice 51, Dragon Pulse 54 | Milotic (from 40) |
| Frillish | surf | 39 | Oxide | Confuse Ray, Hex, Brine, Pain Split | as Jellicent: Destiny Bond 45, Shadow Ball 51, Scald 55 | Jellicent (from 40) |
| Frillish | surf | 39 | Rewrite | Hex, Brine, Dark Pulse, Pain Split | as Jellicent: Muddy Water 45, Shadow Ball 51, Sludge Bomb 53, Scald 55 | Jellicent (from 40) |
| Crawdaunt | super rod | 40 | Oxide | Knock Off, Swift, Taunt, Night Slash | Crabhammer 44, Swords Dance 52 | Crawdaunt |
| Crawdaunt | super rod | 40 | Rewrite | Swift, Taunt, Metal Claw, Night Slash | Throat Chop 41, Crabhammer 44, X-Scissor 46, Swords Dance 52 | Crawdaunt |
| Milotic | super rod | 40 | Oxide | Recover, Captivate, Aqua Tail, Hydro Pump | Attract 41, Safeguard 45, Aqua Ring 49 | Milotic |
| Milotic | super rod | 40 | Rewrite | Recover, Aqua Tail, Aurora Beam, Surf | Attract 41, Safeguard 45, Aqua Ring 49, Alluring Voice 51, Dragon Pulse 54 | Milotic |
| Kingdra | surf | 42 | Oxide | Agility, Twister, Brine, Hydro Pump | Dragon Dance 48 | Kingdra |
| Kingdra | surf | 42 | Rewrite | Twister, Brine, Aurora Beam, Octazooka | Scald 54 | Kingdra |
| Lanturn | super rod | 43 | Oxide | Spit Up, BubbleBeam, Signal Beam, Discharge | Aqua Ring 47, Hydro Pump 52 | Lanturn |
| Lanturn | super rod | 43 | Rewrite | Signal Beam, Scald, Discharge, Thunderbolt | Aqua Ring 47, Muddy Water 52 | Lanturn |
| Wailord | super rod | 43 | Oxide | Rest, Brine, Water Spout, Amnesia | Dive 46, Bounce 54 | Wailord |
| Wailord | super rod | 43 | Rewrite | Rest, Brine, Water Spout, Amnesia | Dive 46, Rock Tomb 48, Iron Head 50, Bounce 54, Zen Headbutt 56 | Wailord |
| Pelipper | super rod | 46 | Oxide | Stockpile, Swallow, Spit Up, Fling | Tailwind 50 | Pelipper |
| Pelipper | super rod | 46 | Rewrite | Stockpile, Spit Up, Fling, Icy Wind | Tailwind 50, Air Slash 52, Acrobatics 54 | Pelipper |

## Mt. Coronet South

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 56 | At the cap |
|---|---|---|---|---|---|---|
| Milotic | super rod | 32 | Oxide | Twister, Recover, Captivate, Aqua Tail | Hydro Pump 37, Attract 41, Safeguard 45, Aqua Ring 49 | Milotic |
| Milotic | super rod | 32 | Rewrite | Water Gun, Twister, Recover, Aqua Tail | Aurora Beam 33, Surf 37, Attract 41, Safeguard 45, Aqua Ring 49, Alluring Voice 51, Dragon Pulse 54 | Milotic |
| Whiscash | super rod | 32 | Oxide | Mud Bomb, Amnesia, Water Pulse, Magnitude | Rest 33, Snore 33, Aqua Tail 39, Earthquake 45, Future Sight 51 | Whiscash |
| Whiscash | super rod | 32 | Rewrite | Amnesia, Water Pulse, Magnitude, Bulldoze | Rest 33, Zen Headbutt 35, Aqua Tail 39, Wild Charge 42, Earthquake 45, Future Sight 51, Ice Beam 53 | Whiscash |
| Crawdaunt | super rod | 35 | Oxide | Protect, Knock Off, Swift, Taunt | Night Slash 39, Crabhammer 44, Swords Dance 52 | Crawdaunt |
| Crawdaunt | super rod | 35 | Rewrite | BubbleBeam, Knock Off, Swift, Taunt | Metal Claw 36, Night Slash 39, Throat Chop 41, Crabhammer 44, X-Scissor 46, Swords Dance 52 | Crawdaunt |
| Lanturn | super rod | 35 | Oxide | Swallow, Spit Up, BubbleBeam, Signal Beam | Discharge 40, Aqua Ring 47, Hydro Pump 52 | Lanturn |
| Lanturn | super rod | 35 | Rewrite | Swallow, Spit Up, BubbleBeam, Signal Beam | Scald 37, Discharge 40, Thunderbolt 42, Aqua Ring 47, Muddy Water 52 | Lanturn |
| Greninja | super rod | 38 | Oxide | Low Kick, Waterfall, Fling, Scald | Dark Pulse 40, Extrasensory 43, Sludge Wave 47, Gunk Shot 51, Hydro Pump 55 | Greninja |
| Greninja | super rod | 38 | Rewrite | Waterfall, Fling, Shadow Sneak, Scald | Dark Pulse 40, Extrasensory 43, Sludge Wave 47, Surf 49, Gunk Shot 51, Ice Beam 56 | Greninja |

## Oreburgh Gate

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 56 | At the cap |
|---|---|---|---|---|---|---|
| Corsola | super rod | 30 | Oxide | Refresh, Rock Blast, BubbleBeam, Lucky Chant | AncientPower 32, Aqua Ring 37, Spike Cannon 40, Power Gem 44, Mirror Coat 48, Earth Power 53 | Corsola |
| Corsola | super rod | 30 | Rewrite | Rock Blast, Aqua Cutter, BubbleBeam, Lucky Chant | Rock Slide 33, Aqua Ring 37, Spike Cannon 40, Liquidation 42, Power Gem 44, Throat Chop 46, Mirror Coat 48, Earth Power 53, Body Slam 55 | Corsola |
| Jellicent | super rod | 30 | Oxide | Water Pulse, Imprison, Confuse Ray, Hex | Brine 34, Pain Split 39, Destiny Bond 45, Shadow Ball 51, Scald 55 | Jellicent |
| Jellicent | super rod | 30 | Rewrite | Water Pulse, Imprison, Confuse Ray, Hex | Brine 34, Pain Split 39, Muddy Water 45, Shadow Ball 51, Sludge Bomb 53, Scald 55 | Jellicent |
| Seaking | super rod | 33 | Oxide | Water Pulse, Flail, Aqua Ring, Fury Attack | Waterfall 40, Horn Drill 47, Agility 56 | Seaking |
| Seaking | super rod | 33 | Rewrite | Water Pulse, Flail, Aqua Ring, Bulldoze | Aqua Jet 35, Waterfall 40, Poison Jab 42, Throat Chop 44, Aqua Tail 50, Drill Peck 52, Agility 56 | Seaking |
| Whiscash | super rod | 33 | Oxide | Water Pulse, Magnitude, Rest, Snore | Aqua Tail 39, Earthquake 45, Future Sight 51 | Whiscash |
| Whiscash | super rod | 33 | Rewrite | Water Pulse, Magnitude, Bulldoze, Rest | Zen Headbutt 35, Aqua Tail 39, Wild Charge 42, Earthquake 45, Future Sight 51, Ice Beam 53 | Whiscash |
| Wailmer | super rod | 36 | Oxide | Mist, Rest, Brine, Water Spout | Amnesia 37; as Wailord: Dive 46, Bounce 54 | Wailord (from 40) |
| Wailmer | super rod | 36 | Rewrite | Mist, Rest, Brine, Water Spout | Amnesia 37; as Wailord: Dive 46, Rock Tomb 48, Iron Head 50, Bounce 54, Zen Headbutt 56 | Wailord (from 40) |

## Pastoria City

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 56 | At the cap |
|---|---|---|---|---|---|---|
| Quagsire | super rod | 35 | Oxide | Slam, Mud Bomb, Amnesia, Yawn | Earthquake 36, Mist 48, Haze 48, Muddy Water 53 | Quagsire |
| Quagsire | super rod | 35 | Rewrite | Rock Tomb, Amnesia, Bulldoze, Yawn | Earthquake 36, Toxic 40, Drain Punch 43, Mist 48, Aqua Tail 51, Muddy Water 53 | Quagsire |
| Sharpedo | super rod | 35 | Oxide | Assurance, Crunch, Slash, Aqua Jet | Taunt 40, Agility 45, Skull Bash 50, Night Slash 56 | Sharpedo |
| Sharpedo | super rod | 35 | Rewrite | Assurance, Crunch, Slash, Aqua Jet | Taunt 40, Agility 45, Liquidation 46, Skull Bash 50, Poison Jab 52, Night Slash 56 | Sharpedo |
| Lombre | super rod | 38 | Oxide | Water Sport, BubbleBeam, Zen Headbutt, Uproar | nothing | Ludicolo (from 38) |
| Lombre | super rod | 38 | Rewrite | Zen Headbutt, Icy Wind, Giga Drain, Uproar | as Ludicolo: Mud Shot 40, Muddy Water 54, Giga Drain 56 | Ludicolo (from 38) |
| Ludicolo | super rod | 38 | Oxide | Astonish, Growl, Mega Drain, Nature Power | nothing | Ludicolo |
| Ludicolo | super rod | 38 | Rewrite | Growl, Mega Drain, Nature Power, Energy Ball | Mud Shot 40, Muddy Water 54, Giga Drain 56 | Ludicolo |
| Greninja | super rod | 41 | Oxide | Waterfall, Fling, Scald, Dark Pulse | Extrasensory 43, Sludge Wave 47, Gunk Shot 51, Hydro Pump 55 | Greninja |
| Greninja | super rod | 41 | Rewrite | Fling, Shadow Sneak, Scald, Dark Pulse | Extrasensory 43, Sludge Wave 47, Surf 49, Gunk Shot 51, Ice Beam 56 | Greninja |

## Ravaged Path

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 56 | At the cap |
|---|---|---|---|---|---|---|
| Milotic | super rod | 30 | Oxide | Twister, Recover, Captivate, Aqua Tail | Hydro Pump 37, Attract 41, Safeguard 45, Aqua Ring 49 | Milotic |
| Milotic | super rod | 30 | Rewrite | Water Gun, Twister | Recover 31, Aqua Tail 32, Aurora Beam 33, Surf 37, Attract 41, Safeguard 45, Aqua Ring 49, Alluring Voice 51, Dragon Pulse 54 | Milotic |
| Whiscash | super rod | 30 | Oxide | Mud Bomb, Amnesia, Water Pulse, Magnitude | Rest 33, Snore 33, Aqua Tail 39, Earthquake 45, Future Sight 51 | Whiscash |
| Whiscash | super rod | 30 | Rewrite | Amnesia, Water Pulse, Magnitude, Bulldoze | Rest 33, Zen Headbutt 35, Aqua Tail 39, Wild Charge 42, Earthquake 45, Future Sight 51, Ice Beam 53 | Whiscash |
| Crawdaunt | super rod | 33 | Oxide | BubbleBeam, Protect, Knock Off, Swift | Taunt 34, Night Slash 39, Crabhammer 44, Swords Dance 52 | Crawdaunt |
| Crawdaunt | super rod | 33 | Rewrite | Leer, BubbleBeam, Knock Off, Swift | Taunt 34, Metal Claw 36, Night Slash 39, Throat Chop 41, Crabhammer 44, X-Scissor 46, Swords Dance 52 | Crawdaunt |
| Lanturn | super rod | 33 | Oxide | Stockpile, Swallow, Spit Up, BubbleBeam | Signal Beam 35, Discharge 40, Aqua Ring 47, Hydro Pump 52 | Lanturn |
| Lanturn | super rod | 33 | Rewrite | Stockpile, Swallow, Spit Up, BubbleBeam | Signal Beam 35, Scald 37, Discharge 40, Thunderbolt 42, Aqua Ring 47, Muddy Water 52 | Lanturn |
| Greninja | super rod | 36 | Oxide | Acrobatics, Low Kick, Waterfall, Fling | Scald 37, Dark Pulse 40, Extrasensory 43, Sludge Wave 47, Gunk Shot 51, Hydro Pump 55 | Greninja |
| Greninja | super rod | 36 | Rewrite | Low Kick, Waterfall, Fling, Shadow Sneak | Scald 37, Dark Pulse 40, Extrasensory 43, Sludge Wave 47, Surf 49, Gunk Shot 51, Ice Beam 56 | Greninja |

## Route 203

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 56 | At the cap |
|---|---|---|---|---|---|---|
| Horsea | super rod | 30 | Oxide | BubbleBeam, Agility, Twister, Brine | as Kingdra: Hydro Pump 40, Dragon Dance 48 | Kingdra (from 32) |
| Horsea | super rod | 30 | Rewrite | BubbleBeam, Agility, Twister, Brine | as Kingdra: Aurora Beam 32, Octazooka 40, Scald 54 | Kingdra (from 32) |
| Sharpedo | super rod | 30 | Oxide | Swagger, Assurance, Crunch, Slash | Aqua Jet 34, Taunt 40, Agility 45, Skull Bash 50, Night Slash 56 | Sharpedo |
| Sharpedo | super rod | 30 | Rewrite | Swagger, Assurance, Crunch, Slash | Aqua Jet 34, Taunt 40, Agility 45, Liquidation 46, Skull Bash 50, Poison Jab 52, Night Slash 56 | Sharpedo |
| Floatzel | super rod | 33 | Oxide | Swift, Aqua Jet, Crunch, Agility | Whirlpool 39, Razor Wind 50 | Floatzel |
| Floatzel | super rod | 33 | Rewrite | Aqua Jet, Crunch, Flip Turn, Icy Wind | Waterfall 35, Whirlpool 39, Liquidation 43, Low Sweep 45, Rock Tomb 51, Agility 52 | Floatzel |
| Quagsire | super rod | 33 | Oxide | Slam, Mud Bomb, Amnesia, Yawn | Earthquake 36, Mist 48, Haze 48, Muddy Water 53 | Quagsire |
| Quagsire | super rod | 33 | Rewrite | Rock Tomb, Amnesia, Bulldoze, Yawn | Earthquake 36, Toxic 40, Drain Punch 43, Mist 48, Aqua Tail 51, Muddy Water 53 | Quagsire |
| Feraligatr | super rod | 36 | Oxide | Ice Fang, Flail, Agility, Crunch | Slash 37, Screech 45, Thrash 50 | Feraligatr |
| Feraligatr | super rod | 36 | Rewrite | Flail, Agility, Crunch, Bulldoze | Slash 37, Brick Break 42, Screech 45, Aqua Tail 50 | Feraligatr |

## Route 204

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 56 | At the cap |
|---|---|---|---|---|---|---|
| Floatzel | super rod | 30 | Oxide | Swift, Aqua Jet, Crunch, Agility | Whirlpool 39, Razor Wind 50 | Floatzel |
| Floatzel | super rod | 30 | Rewrite | Aqua Jet, Crunch, Flip Turn, Icy Wind | Waterfall 35, Whirlpool 39, Liquidation 43, Low Sweep 45, Rock Tomb 51, Agility 52 | Floatzel |
| Gastrodon | super rod | 30 to 33 | Oxide | Water Pulse, Mud Bomb, Hidden Power, Body Slam | Muddy Water 41, Recover 54 | Gastrodon |
| Gastrodon | super rod | 30 to 33 | Rewrite | Water Pulse, Mud Bomb, Hidden Power, Body Slam | AncientPower 31, Clear Smog 34, Muddy Water 41, Earth Power 43, Bulldoze 45, Ice Beam 50, Recover 54 | Gastrodon |
| Quagsire | super rod | 30 | Oxide | Mud Shot, Slam, Mud Bomb, Amnesia | Yawn 31, Earthquake 36, Mist 48, Haze 48, Muddy Water 53 | Quagsire |
| Quagsire | super rod | 30 | Rewrite | Mud Bomb, Rock Tomb, Amnesia, Bulldoze | Yawn 31, Earthquake 36, Toxic 40, Drain Punch 43, Mist 48, Aqua Tail 51, Muddy Water 53 | Quagsire |
| Seaking | super rod | 30 | Oxide | Horn Attack, Water Pulse, Flail, Aqua Ring | Fury Attack 31, Waterfall 40, Horn Drill 47, Agility 56 | Seaking |
| Seaking | super rod | 30 | Rewrite | Horn Attack, Water Pulse, Flail, Aqua Ring | Bulldoze 33, Aqua Jet 35, Waterfall 40, Poison Jab 42, Throat Chop 44, Aqua Tail 50, Drill Peck 52, Agility 56 | Seaking |
| Crawdaunt | super rod | 33 | Oxide | BubbleBeam, Protect, Knock Off, Swift | Taunt 34, Night Slash 39, Crabhammer 44, Swords Dance 52 | Crawdaunt |
| Crawdaunt | super rod | 33 | Rewrite | Leer, BubbleBeam, Knock Off, Swift | Taunt 34, Metal Claw 36, Night Slash 39, Throat Chop 41, Crabhammer 44, X-Scissor 46, Swords Dance 52 | Crawdaunt |
| Ludicolo | super rod | 33 | Oxide | Astonish, Growl, Mega Drain, Nature Power | nothing | Ludicolo |
| Ludicolo | super rod | 33 | Rewrite | Growl, Mega Drain, Nature Power, Energy Ball | Mud Shot 40, Muddy Water 54, Giga Drain 56 | Ludicolo |
| Whiscash | super rod | 33 | Oxide | Water Pulse, Magnitude, Rest, Snore | Aqua Tail 39, Earthquake 45, Future Sight 51 | Whiscash |
| Whiscash | super rod | 33 | Rewrite | Water Pulse, Magnitude, Bulldoze, Rest | Zen Headbutt 35, Aqua Tail 39, Wild Charge 42, Earthquake 45, Future Sight 51, Ice Beam 53 | Whiscash |
| Golduck | super rod | 36 | Oxide | Confusion, Water Pulse, Fury Swipes, Screech | Psych Up 37, Zen Headbutt 44, Amnesia 50, Hydro Pump 56 | Golduck |
| Golduck | super rod | 36 | Rewrite | Water Pulse, Fury Swipes, Screech, Muddy Water | Psych Up 37, Aurora Beam 42, Zen Headbutt 44, Amnesia 50, Power Gem 52 | Golduck |
| Poliwrath | super rod | 36 | Oxide | BubbleBeam, Hypnosis, DoubleSlap, Submission | DynamicPunch 43, Mind Reader 53 | Poliwrath |
| Poliwrath | super rod | 36 | Rewrite | Hypnosis, DoubleSlap, Liquidation, Wake-Up Slap | Throat Chop 40, Brick Break 43, Mind Reader 53, Rock Tomb 55 | Poliwrath |

## Route 205

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 56 | At the cap |
|---|---|---|---|---|---|---|
| Lombre | super rod | 30 | Oxide | Fake Out, Fury Swipes, Water Sport, BubbleBeam | nothing | Ludicolo (from 30) |
| Lombre | super rod | 30 | Rewrite | Fury Swipes, Swagger, Water Sport, BubbleBeam | as Ludicolo: Energy Ball 33, Mud Shot 40, Muddy Water 54, Giga Drain 56 | Ludicolo (from 30) |
| Ludicolo | super rod | 30 | Oxide | Astonish, Growl, Mega Drain, Nature Power | nothing | Ludicolo |
| Ludicolo | super rod | 30 | Rewrite | Astonish, Growl, Mega Drain, Nature Power | Energy Ball 33, Mud Shot 40, Muddy Water 54, Giga Drain 56 | Ludicolo |
| Seaking | super rod | 30 | Oxide | Horn Attack, Water Pulse, Flail, Aqua Ring | Fury Attack 31, Waterfall 40, Horn Drill 47, Agility 56 | Seaking |
| Seaking | super rod | 30 | Rewrite | Horn Attack, Water Pulse, Flail, Aqua Ring | Bulldoze 33, Aqua Jet 35, Waterfall 40, Poison Jab 42, Throat Chop 44, Aqua Tail 50, Drill Peck 52, Agility 56 | Seaking |
| Whiscash | super rod | 30 | Oxide | Mud Bomb, Amnesia, Water Pulse, Magnitude | Rest 33, Snore 33, Aqua Tail 39, Earthquake 45, Future Sight 51 | Whiscash |
| Whiscash | super rod | 30 | Rewrite | Amnesia, Water Pulse, Magnitude, Bulldoze | Rest 33, Zen Headbutt 35, Aqua Tail 39, Wild Charge 42, Earthquake 45, Future Sight 51, Ice Beam 53 | Whiscash |
| Araquanid | super rod | 33 | Oxide | BubbleBeam, Bug Bite, Headbutt, Soak | Dive 36, Lunge 41, Scald 48, Hydro Pump 51, Liquidation 55 | Araquanid |
| Araquanid | super rod | 33 | Rewrite | Bug Bite, Headbutt, Spider Web, Soak | Dive 36, Skitter Smack 38, Lunge 41, Waterfall 43, Scald 48, Poison Jab 51, Liquidation 55 | Araquanid |
| Crawdaunt | super rod | 33 | Oxide | BubbleBeam, Protect, Knock Off, Swift | Taunt 34, Night Slash 39, Crabhammer 44, Swords Dance 52 | Crawdaunt |
| Crawdaunt | super rod | 33 | Rewrite | Leer, BubbleBeam, Knock Off, Swift | Taunt 34, Metal Claw 36, Night Slash 39, Throat Chop 41, Crabhammer 44, X-Scissor 46, Swords Dance 52 | Crawdaunt |
| Jellicent | super rod | 33 | Oxide | Water Pulse, Imprison, Confuse Ray, Hex | Brine 34, Pain Split 39, Destiny Bond 45, Shadow Ball 51, Scald 55 | Jellicent |
| Jellicent | super rod | 33 | Rewrite | Water Pulse, Imprison, Confuse Ray, Hex | Brine 34, Pain Split 39, Muddy Water 45, Shadow Ball 51, Sludge Bomb 53, Scald 55 | Jellicent |
| Lanturn | super rod | 33 | Oxide | Stockpile, Swallow, Spit Up, BubbleBeam | Signal Beam 35, Discharge 40, Aqua Ring 47, Hydro Pump 52 | Lanturn |
| Lanturn | super rod | 33 | Rewrite | Stockpile, Swallow, Spit Up, BubbleBeam | Signal Beam 35, Scald 37, Discharge 40, Thunderbolt 42, Aqua Ring 47, Muddy Water 52 | Lanturn |
| Golduck | super rod | 36 | Oxide | Confusion, Water Pulse, Fury Swipes, Screech | Psych Up 37, Zen Headbutt 44, Amnesia 50, Hydro Pump 56 | Golduck |
| Golduck | super rod | 36 | Rewrite | Water Pulse, Fury Swipes, Screech, Muddy Water | Psych Up 37, Aurora Beam 42, Zen Headbutt 44, Amnesia 50, Power Gem 52 | Golduck |

## Route 208

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 56 | At the cap |
|---|---|---|---|---|---|---|
| Seaking | super rod | 32 | Oxide | Water Pulse, Flail, Aqua Ring, Fury Attack | Waterfall 40, Horn Drill 47, Agility 56 | Seaking |
| Seaking | super rod | 32 | Rewrite | Horn Attack, Water Pulse, Flail, Aqua Ring | Bulldoze 33, Aqua Jet 35, Waterfall 40, Poison Jab 42, Throat Chop 44, Aqua Tail 50, Drill Peck 52, Agility 56 | Seaking |
| Whiscash | super rod | 32 | Oxide | Mud Bomb, Amnesia, Water Pulse, Magnitude | Rest 33, Snore 33, Aqua Tail 39, Earthquake 45, Future Sight 51 | Whiscash |
| Whiscash | super rod | 32 | Rewrite | Amnesia, Water Pulse, Magnitude, Bulldoze | Rest 33, Zen Headbutt 35, Aqua Tail 39, Wild Charge 42, Earthquake 45, Future Sight 51, Ice Beam 53 | Whiscash |
| Crawdaunt | super rod | 35 | Oxide | Protect, Knock Off, Swift, Taunt | Night Slash 39, Crabhammer 44, Swords Dance 52 | Crawdaunt |
| Crawdaunt | super rod | 35 | Rewrite | BubbleBeam, Knock Off, Swift, Taunt | Metal Claw 36, Night Slash 39, Throat Chop 41, Crabhammer 44, X-Scissor 46, Swords Dance 52 | Crawdaunt |
| Milotic | super rod | 35 | Oxide | Twister, Recover, Captivate, Aqua Tail | Hydro Pump 37, Attract 41, Safeguard 45, Aqua Ring 49 | Milotic |
| Milotic | super rod | 35 | Rewrite | Twister, Recover, Aqua Tail, Aurora Beam | Surf 37, Attract 41, Safeguard 45, Aqua Ring 49, Alluring Voice 51, Dragon Pulse 54 | Milotic |
| Toxapex | super rod | 38 | Oxide | Venoshock, Recover, Spike Cannon, Pin Missile | Toxic 39, Venom Drench 42, Poison Jab 43, Liquidation 45 | Toxapex |
| Toxapex | super rod | 38 | Rewrite | Venoshock, Recover, Spike Cannon, Pin Missile | Toxic 39, Venom Drench 42, Poison Jab 43, Liquidation 45, Lunge 48, Sludge Bomb 50, Ice Beam 56 | Toxapex |

## Route 209

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 56 | At the cap |
|---|---|---|---|---|---|---|
| Floatzel | super rod | 33 | Oxide | Swift, Aqua Jet, Crunch, Agility | Whirlpool 39, Razor Wind 50 | Floatzel |
| Floatzel | super rod | 33 | Rewrite | Aqua Jet, Crunch, Flip Turn, Icy Wind | Waterfall 35, Whirlpool 39, Liquidation 43, Low Sweep 45, Rock Tomb 51, Agility 52 | Floatzel |
| Quagsire | super rod | 33 | Oxide | Slam, Mud Bomb, Amnesia, Yawn | Earthquake 36, Mist 48, Haze 48, Muddy Water 53 | Quagsire |
| Quagsire | super rod | 33 | Rewrite | Rock Tomb, Amnesia, Bulldoze, Yawn | Earthquake 36, Toxic 40, Drain Punch 43, Mist 48, Aqua Tail 51, Muddy Water 53 | Quagsire |
| Gastrodon | super rod | 36 | Oxide | Water Pulse, Mud Bomb, Hidden Power, Body Slam | Muddy Water 41, Recover 54 | Gastrodon |
| Gastrodon | super rod | 36 | Rewrite | Hidden Power, Body Slam, AncientPower, Clear Smog | Muddy Water 41, Earth Power 43, Bulldoze 45, Ice Beam 50, Recover 54 | Gastrodon |
| Ludicolo | super rod | 36 | Oxide | Astonish, Growl, Mega Drain, Nature Power | nothing | Ludicolo |
| Ludicolo | super rod | 36 | Rewrite | Growl, Mega Drain, Nature Power, Energy Ball | Mud Shot 40, Muddy Water 54, Giga Drain 56 | Ludicolo |
| Feraligatr | super rod | 39 | Oxide | Flail, Agility, Crunch, Slash | Screech 45, Thrash 50 | Feraligatr |
| Feraligatr | super rod | 39 | Rewrite | Agility, Crunch, Bulldoze, Slash | Brick Break 42, Screech 45, Aqua Tail 50 | Feraligatr |

## Route 210

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 56 | At the cap |
|---|---|---|---|---|---|---|
| Seaking | super rod | 36 | Oxide | Water Pulse, Flail, Aqua Ring, Fury Attack | Waterfall 40, Horn Drill 47, Agility 56 | Seaking |
| Seaking | super rod | 36 | Rewrite | Flail, Aqua Ring, Bulldoze, Aqua Jet | Waterfall 40, Poison Jab 42, Throat Chop 44, Aqua Tail 50, Drill Peck 52, Agility 56 | Seaking |
| Whiscash | super rod | 36 | Oxide | Water Pulse, Magnitude, Rest, Snore | Aqua Tail 39, Earthquake 45, Future Sight 51 | Whiscash |
| Whiscash | super rod | 36 | Rewrite | Magnitude, Bulldoze, Rest, Zen Headbutt | Aqua Tail 39, Wild Charge 42, Earthquake 45, Future Sight 51, Ice Beam 53 | Whiscash |
| Crawdaunt | super rod | 39 | Oxide | Knock Off, Swift, Taunt, Night Slash | Crabhammer 44, Swords Dance 52 | Crawdaunt |
| Crawdaunt | super rod | 39 | Rewrite | Swift, Taunt, Metal Claw, Night Slash | Throat Chop 41, Crabhammer 44, X-Scissor 46, Swords Dance 52 | Crawdaunt |
| Milotic | super rod | 39 | Oxide | Recover, Captivate, Aqua Tail, Hydro Pump | Attract 41, Safeguard 45, Aqua Ring 49 | Milotic |
| Milotic | super rod | 39 | Rewrite | Recover, Aqua Tail, Aurora Beam, Surf | Attract 41, Safeguard 45, Aqua Ring 49, Alluring Voice 51, Dragon Pulse 54 | Milotic |
| Lumineon | super rod | 42 | Oxide | Captivate, Safeguard, Aqua Ring, Whirlpool | U-turn 48, Bounce 53 | Lumineon |
| Lumineon | super rod | 42 | Rewrite | Flip Turn, Aqua Ring, Aqua Tail, Whirlpool | U-turn 48, Ice Fang 50, Bounce 53, Air Slash 55 | Lumineon |

## Route 212

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 56 | At the cap |
|---|---|---|---|---|---|---|
| Floatzel | super rod | 35 | Oxide | Swift, Aqua Jet, Crunch, Agility | Whirlpool 39, Razor Wind 50 | Floatzel |
| Floatzel | super rod | 35 | Rewrite | Crunch, Flip Turn, Icy Wind, Waterfall | Whirlpool 39, Liquidation 43, Low Sweep 45, Rock Tomb 51, Agility 52 | Floatzel |
| Quagsire | super rod | 35 | Oxide | Slam, Mud Bomb, Amnesia, Yawn | Earthquake 36, Mist 48, Haze 48, Muddy Water 53 | Quagsire |
| Quagsire | super rod | 35 | Rewrite | Rock Tomb, Amnesia, Bulldoze, Yawn | Earthquake 36, Toxic 40, Drain Punch 43, Mist 48, Aqua Tail 51, Muddy Water 53 | Quagsire |
| Whiscash | super rod | 35 | Oxide | Water Pulse, Magnitude, Rest, Snore | Aqua Tail 39, Earthquake 45, Future Sight 51 | Whiscash |
| Whiscash | super rod | 35 | Rewrite | Magnitude, Bulldoze, Rest, Zen Headbutt | Aqua Tail 39, Wild Charge 42, Earthquake 45, Future Sight 51, Ice Beam 53 | Whiscash |
| Gastrodon | super rod | 38 | Oxide | Water Pulse, Mud Bomb, Hidden Power, Body Slam | Muddy Water 41, Recover 54 | Gastrodon |
| Gastrodon | super rod | 38 | Rewrite | Hidden Power, Body Slam, AncientPower, Clear Smog | Muddy Water 41, Earth Power 43, Bulldoze 45, Ice Beam 50, Recover 54 | Gastrodon |
| Ludicolo | super rod | 38 | Oxide | Astonish, Growl, Mega Drain, Nature Power | nothing | Ludicolo |
| Ludicolo | super rod | 38 | Rewrite | Growl, Mega Drain, Nature Power, Energy Ball | Mud Shot 40, Muddy Water 54, Giga Drain 56 | Ludicolo |
| Sharpedo | super rod | 38 | Oxide | Assurance, Crunch, Slash, Aqua Jet | Taunt 40, Agility 45, Skull Bash 50, Night Slash 56 | Sharpedo |
| Sharpedo | super rod | 38 | Rewrite | Assurance, Crunch, Slash, Aqua Jet | Taunt 40, Agility 45, Liquidation 46, Skull Bash 50, Poison Jab 52, Night Slash 56 | Sharpedo |
| Alomomola | super rod | 41 | Oxide | Wake-Up Slap, Soak, Wish, Brine | Safeguard 45, Whirlpool 49, Helping Hand 53 | Alomomola |
| Alomomola | super rod | 41 | Rewrite | Agility, Wish, Play Rough, Brine | Zen Headbutt 43, Safeguard 45, Whirlpool 49, Helping Hand 53, Liquidation 55 | Alomomola |
| Greninja | super rod | 41 | Oxide | Waterfall, Fling, Scald, Dark Pulse | Extrasensory 43, Sludge Wave 47, Gunk Shot 51, Hydro Pump 55 | Greninja |
| Greninja | super rod | 41 | Rewrite | Fling, Shadow Sneak, Scald, Dark Pulse | Extrasensory 43, Sludge Wave 47, Surf 49, Gunk Shot 51, Ice Beam 56 | Greninja |

## Route 213

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 56 | At the cap |
|---|---|---|---|---|---|---|
| Lumineon | super rod | 35 | Oxide | Water Pulse, Captivate, Safeguard, Aqua Ring | Whirlpool 42, U-turn 48, Bounce 53 | Lumineon |
| Lumineon | super rod | 35 | Rewrite | Captivate, Safeguard, Flip Turn, Aqua Ring | Aqua Tail 37, Whirlpool 42, U-turn 48, Ice Fang 50, Bounce 53, Air Slash 55 | Lumineon |
| Tentacruel | super rod | 35 | Oxide | BubbleBeam, Wrap, Barrier, Water Pulse | Poison Jab 36, Screech 42, Hydro Pump 49, Wring Out 55 | Tentacruel |
| Tentacruel | super rod | 35 | Rewrite | Toxic Spikes, BubbleBeam, Barrier, Water Pulse | Poison Jab 36, Surf 40, Screech 42, Psybeam 44, Sludge Bomb 50, Sludge Wave 52 | Tentacruel |
| Octillery | super rod | 38 | Oxide | Focus Energy, Octazooka, Bullet Seed, Wring Out | Signal Beam 42, Ice Beam 48, Hyper Beam 55 | Octillery |
| Octillery | super rod | 38 | Rewrite | Round, Bullet Seed, Mud Shot, Scald | Signal Beam 42, Seed Bomb 44, Ice Beam 48, Skitter Smack 51, Hyper Beam 55 | Octillery |
| Toxapex | super rod | 38 | Oxide | Venoshock, Recover, Spike Cannon, Pin Missile | Toxic 39, Venom Drench 42, Poison Jab 43, Liquidation 45 | Toxapex |
| Toxapex | super rod | 38 | Rewrite | Venoshock, Recover, Spike Cannon, Pin Missile | Toxic 39, Venom Drench 42, Poison Jab 43, Liquidation 45, Lunge 48, Sludge Bomb 50, Ice Beam 56 | Toxapex |
| Quagsire | super rod | 41 | Oxide | Mud Bomb, Amnesia, Yawn, Earthquake | Mist 48, Haze 48, Muddy Water 53 | Quagsire |
| Quagsire | super rod | 41 | Rewrite | Bulldoze, Yawn, Earthquake, Toxic | Drain Punch 43, Mist 48, Aqua Tail 51, Muddy Water 53 | Quagsire |

## Route 214

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 56 | At the cap |
|---|---|---|---|---|---|---|
| Ludicolo | super rod | 35 | Oxide | Astonish, Growl, Mega Drain, Nature Power | nothing | Ludicolo |
| Ludicolo | super rod | 35 | Rewrite | Growl, Mega Drain, Nature Power, Energy Ball | Mud Shot 40, Muddy Water 54, Giga Drain 56 | Ludicolo |
| Quagsire | super rod | 35 | Oxide | Slam, Mud Bomb, Amnesia, Yawn | Earthquake 36, Mist 48, Haze 48, Muddy Water 53 | Quagsire |
| Quagsire | super rod | 35 | Rewrite | Rock Tomb, Amnesia, Bulldoze, Yawn | Earthquake 36, Toxic 40, Drain Punch 43, Mist 48, Aqua Tail 51, Muddy Water 53 | Quagsire |
| Gastrodon | super rod | 38 | Oxide | Water Pulse, Mud Bomb, Hidden Power, Body Slam | Muddy Water 41, Recover 54 | Gastrodon |
| Gastrodon | super rod | 38 | Rewrite | Hidden Power, Body Slam, AncientPower, Clear Smog | Muddy Water 41, Earth Power 43, Bulldoze 45, Ice Beam 50, Recover 54 | Gastrodon |
| Seaking | super rod | 38 | Oxide | Water Pulse, Flail, Aqua Ring, Fury Attack | Waterfall 40, Horn Drill 47, Agility 56 | Seaking |
| Seaking | super rod | 38 | Rewrite | Flail, Aqua Ring, Bulldoze, Aqua Jet | Waterfall 40, Poison Jab 42, Throat Chop 44, Aqua Tail 50, Drill Peck 52, Agility 56 | Seaking |
| Mantine | super rod | 41 | Oxide | Water Pulse, Take Down, Confuse Ray, Bounce | Aqua Ring 46, Hydro Pump 49 | Mantine |
| Mantine | super rod | 41 | Rewrite | Take Down, Scald, Confuse Ray, Bounce | Signal Beam 42, Aqua Ring 46, Surf 50, Air Slash 52 | Mantine |

## Route 216

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 56 | At the cap |
|---|---|---|---|---|---|---|
| Snover | wild | 32 | Oxide | Swagger, Mist, Ice Shard, Ingrain | Wood Hammer 36; as Abomasnow: Blizzard 47 | Abomasnow (from 40) |
| Snover | wild | 32 | Rewrite | Mist, Ice Shard, Rock Tomb, Seed Bomb | Wood Hammer 36; as Abomasnow: Ice Punch 45, Ice Beam 47, Body Press 53, Giga Drain 55 | Abomasnow (from 40) |
| Absol | wild | 33 | Oxide | Pursuit, Swords Dance, Bite, Double Team | Slash 36, Future Sight 41, Sucker Punch 44, Detect 49, Night Slash 52 | Absol |
| Absol | wild | 33 | Rewrite | Quick Attack, Pursuit, Swords Dance, Bite | Slash 36, Future Sight 41, Sucker Punch 44, X-Scissor 46, Night Slash 52, Throat Chop 54 | Absol |
| Delibird | wild | 33 | Oxide | Present | nothing | Delibird |
| Delibird | wild | 33 | Rewrite | Present, Drill Peck, Ice Beam | Drill Run 54, Swagger 56 | Delibird |
| Frosmoth | wild | 33 | Oxide | Defog, FeatherDance, Aurora Beam, Bug Buzz | Aurora Veil 36, Blizzard 40, Tailwind 44, Wide Guard 48, Quiver Dance 52 | Frosmoth |
| Frosmoth | wild | 33 | Rewrite | Stun Spore, Infestation, Bug Buzz, Defog | Aurora Beam 34, Aurora Veil 36, Psybeam 38, Ice Beam 40, Tailwind 44, Wide Guard 48, Giga Drain 50, Quiver Dance 52 | Frosmoth |
| Sneasel | wild | 33 | Oxide | Faint Attack, Fury Swipes, Agility, Icy Wind | Slash 35, Metal Claw 42, Ice Shard 49 | Sneasel; Weavile in HQ |
| Sneasel | wild | 33 | Rewrite | Fury Swipes, Nasty Plot, Agility, Icy Wind | Slash 35, Revenge 37, Poison Jab 40, Metal Claw 42, Ice Shard 49, Throat Chop 51, Ice Punch 56 | Sneasel; Weavile in HQ |
| Snorunt | wild | 33 to 34 | Oxide | Headbutt, Protect, Ice Fang, Crunch | Ice Shard 37; as Glalie: Blizzard 51 | Glalie (from 42) |
| Snorunt | wild | 33 to 34 | Oxide | Headbutt, Protect, Ice Fang, Crunch | as Froslass: Ice Shard 37, Blizzard 51 | Froslass (from 33) |
| Snorunt | wild | 33 to 34 | Rewrite | Headbutt, Ominous Wind, Ice Fang, Crunch | Draining Kiss 35, Ice Shard 37; as Glalie: Rock Slide 42, Power Gem 44, Earth Power 46, Icicle Crash 48, Shadow Ball 53, Dark Pulse 55 | Glalie (from 42) |
| Snorunt | wild | 33 to 34 | Rewrite | Headbutt, Ominous Wind, Ice Fang, Crunch | as Froslass: Ice Shard 37, Signal Beam 44, Ice Beam 51 | Froslass (from 33) |
| Alolan Ninetales | wild | 34 | Oxide | Tail Whip, Disable, Ice Shard, Safeguard | nothing | Alolan Ninetales |
| Alolan Ninetales | wild | 34 | Rewrite | Incinerate, Spite, Icy Wind, Payback | Dazzling Gleam 35, Chilling Water 37, Ice Beam 43, Extrasensory 44, Foul Play 51, Confuse Ray 53 | Alolan Ninetales |
| Golbat | wild | 34 | Oxide | Wing Attack, Confuse Ray, Air Cutter, Mean Look | Poison Fang 39; as Crobat: Haze 45, Air Slash 51 | Crobat (from 40) |
| Golbat | wild | 34 | Rewrite | Wing Attack, Confuse Ray, Air Cutter, Mean Look | Poison Fang 39; as Crobat: Steel Wing 45, Air Slash 51, Poison Jab 53, Zen Headbutt 55 | Crobat (from 40) |
| Mienfoo | wild | 34 | Oxide | Force Palm, Bounce, Drain Punch, Vacuum Wave | as Mienshao: Aura Sphere 38, Me First 40, Jump Kick 45, Dual Chop 48, Focus Blast 51, Acrobatics 55 | Mienshao (from 36) |
| Mienfoo | wild | 34 | Rewrite | Force Palm, Bounce, Drain Punch, Vacuum Wave | as Mienshao: Aura Sphere 38, Low Sweep 40, Jump Kick 45, Dual Chop 48, U-turn 50, Acrobatics 55 | Mienshao (from 36) |
| Bronzong | wild | 35 | Oxide | Extrasensory, Iron Defense, Safeguard, Block | Gyro Ball 38, Future Sight 43, Faint Attack 50 | Bronzong |
| Bronzong | wild | 35 | Rewrite | Iron Defense, Safeguard, Block, Iron Head | Gyro Ball 38, Future Sight 43, Rock Tomb 45, Faint Attack 50, Body Press 52 | Bronzong |
| Galarian Mr Mime | wild | 35 | Oxide | Icy Wind, Double Kick, Psybeam, Hypnosis | Mirror Coat 36, Sucker Punch 40; as Mr. Rime: Freeze-Dry 44, Psychic 48, Teeter Dance 52 | Mr. Rime (from 42) |
| Galarian Mr Mime | wild | 35 | Rewrite | Icy Wind, Double Kick, Psybeam, Hypnosis | Mirror Coat 36, Sucker Punch 40, Dazzling Gleam 42; as Mr. Rime: Freeze-Dry 44, Psychic 48, Teeter Dance 52, Encore 54, Ice Beam 56 | Mr. Rime (from 42) |
| Slugma | wild | 35 | Oxide | Harden, Recover, AncientPower, Amnesia | Lava Plume 38; as Magcargo: Lava Plume 40, Rock Slide 45, Body Slam 52 | Magcargo (from 38) |
| Slugma | wild | 35 | Rewrite | Harden, Recover, AncientPower, Amnesia | Lava Plume 38; as Magcargo: Lava Plume 40, Scorching Sands 42, Rock Slide 45, Shell Smash 48, Body Slam 52, Energy Ball 56 | Magcargo (from 38) |

## Route 217

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 56 | At the cap |
|---|---|---|---|---|---|---|
| Swinub | wild | 32 | Oxide | Mud Bomb, Icy Wind, Ice Shard, Take Down | as Piloswine: Fury Attack 33, Earthquake 40; as Mamoswine: Earthquake 40, Mist 48, Blizzard 56 | Mamoswine (from 40) |
| Swinub | wild | 32 | Rewrite | Mud Bomb, Icy Wind, Ice Shard, Take Down | as Piloswine: AncientPower 33, Smack Down 35, Earthquake 40; as Mamoswine: Earthquake 40, Brick Break 45, Mist 48, Icicle Crash 53, Ice Beam 56 | Mamoswine (from 40) |
| Frosmoth | wild | 33 to 34 | Oxide | Defog, FeatherDance, Aurora Beam, Bug Buzz | Aurora Veil 36, Blizzard 40, Tailwind 44, Wide Guard 48, Quiver Dance 52 | Frosmoth |
| Frosmoth | wild | 33 to 34 | Rewrite | Stun Spore, Infestation, Bug Buzz, Defog | Aurora Beam 34, Aurora Veil 36, Psybeam 38, Ice Beam 40, Tailwind 44, Wide Guard 48, Giga Drain 50, Quiver Dance 52 | Frosmoth |
| Sneasel | wild | 33 | Oxide | Faint Attack, Fury Swipes, Agility, Icy Wind | Slash 35, Metal Claw 42, Ice Shard 49 | Sneasel; Weavile in HQ |
| Sneasel | wild | 33 | Rewrite | Fury Swipes, Nasty Plot, Agility, Icy Wind | Slash 35, Revenge 37, Poison Jab 40, Metal Claw 42, Ice Shard 49, Throat Chop 51, Ice Punch 56 | Sneasel; Weavile in HQ |
| Snorunt | wild | 33 | Oxide | Headbutt, Protect, Ice Fang, Crunch | Ice Shard 37; as Glalie: Blizzard 51 | Glalie (from 42) |
| Snorunt | wild | 33 | Oxide | Headbutt, Protect, Ice Fang, Crunch | as Froslass: Ice Shard 37, Blizzard 51 | Froslass (from 33) |
| Snorunt | wild | 33 | Rewrite | Headbutt, Ominous Wind, Ice Fang, Crunch | Draining Kiss 35, Ice Shard 37; as Glalie: Rock Slide 42, Power Gem 44, Earth Power 46, Icicle Crash 48, Shadow Ball 53, Dark Pulse 55 | Glalie (from 42) |
| Snorunt | wild | 33 | Rewrite | Headbutt, Ominous Wind, Ice Fang, Crunch | as Froslass: Ice Shard 37, Signal Beam 44, Ice Beam 51 | Froslass (from 33) |
| Snover | wild | 33 | Oxide | Swagger, Mist, Ice Shard, Ingrain | Wood Hammer 36; as Abomasnow: Blizzard 47 | Abomasnow (from 40) |
| Snover | wild | 33 | Rewrite | Mist, Ice Shard, Rock Tomb, Seed Bomb | Wood Hammer 36; as Abomasnow: Ice Punch 45, Ice Beam 47, Body Press 53, Giga Drain 55 | Abomasnow (from 40) |
| Alolan Ninetales | wild | 34 | Oxide | Tail Whip, Disable, Ice Shard, Safeguard | nothing | Alolan Ninetales |
| Alolan Ninetales | wild | 34 | Rewrite | Incinerate, Spite, Icy Wind, Payback | Dazzling Gleam 35, Chilling Water 37, Ice Beam 43, Extrasensory 44, Foul Play 51, Confuse Ray 53 | Alolan Ninetales |
| Donphan | wild | 34 | Oxide | Magnitude, Slam, Fury Attack, Assurance | Scary Face 39, Earthquake 46, Giga Impact 54 | Donphan |
| Donphan | wild | 34 | Rewrite | Rapid Spin, Magnitude, Rock Tomb, Assurance | Scary Face 39, Knock Off 40, Seed Bomb 43, Earthquake 46, Throat Chop 51, Giga Impact 54, Charm 56 | Donphan |
| Mienfoo | wild | 34 | Oxide | Force Palm, Bounce, Drain Punch, Vacuum Wave | as Mienshao: Aura Sphere 38, Me First 40, Jump Kick 45, Dual Chop 48, Focus Blast 51, Acrobatics 55 | Mienshao (from 36) |
| Mienfoo | wild | 34 | Rewrite | Force Palm, Bounce, Drain Punch, Vacuum Wave | as Mienshao: Aura Sphere 38, Low Sweep 40, Jump Kick 45, Dual Chop 48, U-turn 50, Acrobatics 55 | Mienshao (from 36) |
| Galarian Mr Mime | wild | 35 | Oxide | Icy Wind, Double Kick, Psybeam, Hypnosis | Mirror Coat 36, Sucker Punch 40; as Mr. Rime: Freeze-Dry 44, Psychic 48, Teeter Dance 52 | Mr. Rime (from 42) |
| Galarian Mr Mime | wild | 35 | Rewrite | Icy Wind, Double Kick, Psybeam, Hypnosis | Mirror Coat 36, Sucker Punch 40, Dazzling Gleam 42; as Mr. Rime: Freeze-Dry 44, Psychic 48, Teeter Dance 52, Encore 54, Ice Beam 56 | Mr. Rime (from 42) |
| Meditite | wild | 35 | Oxide | Feint, Calm Mind, Force Palm, Hi Jump Kick | Psych Up 36; as Medicham: Power Trick 42, Reversal 49, Recover 55 | Medicham (from 37) |
| Meditite | wild | 35 | Rewrite | Mind Reader, Rock Throw, Swagger, Hi Jump Kick | Psych Up 36; as Medicham: Low Sweep 37, Bulk Up 38, Iron Head 40, Power Trick 42, Reversal 49, Recover 55 | Medicham (from 37) |
| Slugma | wild | 35 | Oxide | Harden, Recover, AncientPower, Amnesia | Lava Plume 38; as Magcargo: Lava Plume 40, Rock Slide 45, Body Slam 52 | Magcargo (from 38) |
| Slugma | wild | 35 | Rewrite | Harden, Recover, AncientPower, Amnesia | Lava Plume 38; as Magcargo: Lava Plume 40, Scorching Sands 42, Rock Slide 45, Shell Smash 48, Body Slam 52, Energy Ball 56 | Magcargo (from 38) |

## Route 218

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 56 | At the cap |
|---|---|---|---|---|---|---|
| Gorebyss | super rod | 36 | Oxide | Amnesia, Aqua Ring, Captivate, Baton Pass | Dive 37, Psychic 42, Aqua Tail 46, Hydro Pump 51 | Gorebyss |
| Gorebyss | super rod | 36 | Rewrite | Aqua Ring, Captivate, Baton Pass, Draining Kiss | Dive 37, Muddy Water 40, Psychic 42, Aqua Tail 46, Shadow Ball 48, Giga Drain 50, Scald 56 | Gorebyss |
| Mantine | super rod | 36 | Oxide | Agility, Wing Attack, Water Pulse, Take Down | Confuse Ray 37, Bounce 40, Aqua Ring 46, Hydro Pump 49 | Mantine |
| Mantine | super rod | 36 | Rewrite | Wing Attack, Water Pulse, Take Down, Scald | Confuse Ray 37, Bounce 40, Signal Beam 42, Aqua Ring 46, Surf 50, Air Slash 52 | Mantine |
| Gastrodon | super rod | 39 | Oxide | Water Pulse, Mud Bomb, Hidden Power, Body Slam | Muddy Water 41, Recover 54 | Gastrodon |
| Gastrodon | super rod | 39 | Rewrite | Hidden Power, Body Slam, AncientPower, Clear Smog | Muddy Water 41, Earth Power 43, Bulldoze 45, Ice Beam 50, Recover 54 | Gastrodon |
| Jellicent | super rod | 39 | Oxide | Confuse Ray, Hex, Brine, Pain Split | Destiny Bond 45, Shadow Ball 51, Scald 55 | Jellicent |
| Jellicent | super rod | 39 | Rewrite | Confuse Ray, Hex, Brine, Pain Split | Muddy Water 45, Shadow Ball 51, Sludge Bomb 53, Scald 55 | Jellicent |
| Greninja | super rod | 42 | Oxide | Waterfall, Fling, Scald, Dark Pulse | Extrasensory 43, Sludge Wave 47, Gunk Shot 51, Hydro Pump 55 | Greninja |
| Greninja | super rod | 42 | Rewrite | Fling, Shadow Sneak, Scald, Dark Pulse | Extrasensory 43, Sludge Wave 47, Surf 49, Gunk Shot 51, Ice Beam 56 | Greninja |

## Route 219

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 56 | At the cap |
|---|---|---|---|---|---|---|
| Jellicent | super rod | 30 | Oxide | Water Pulse, Imprison, Confuse Ray, Hex | Brine 34, Pain Split 39, Destiny Bond 45, Shadow Ball 51, Scald 55 | Jellicent |
| Jellicent | super rod | 30 | Rewrite | Water Pulse, Imprison, Confuse Ray, Hex | Brine 34, Pain Split 39, Muddy Water 45, Shadow Ball 51, Sludge Bomb 53, Scald 55 | Jellicent |
| Lanturn | super rod | 30 | Oxide | Stockpile, Swallow, Spit Up, BubbleBeam | Signal Beam 35, Discharge 40, Aqua Ring 47, Hydro Pump 52 | Lanturn |
| Lanturn | super rod | 30 | Rewrite | Stockpile, Swallow, Spit Up, BubbleBeam | Signal Beam 35, Scald 37, Discharge 40, Thunderbolt 42, Aqua Ring 47, Muddy Water 52 | Lanturn |
| Lumineon | super rod | 33 | Oxide | Gust, Water Pulse, Captivate, Safeguard | Aqua Ring 35, Whirlpool 42, U-turn 48, Bounce 53 | Lumineon |
| Lumineon | super rod | 33 | Rewrite | Water Pulse, Captivate, Safeguard, Flip Turn | Aqua Ring 35, Aqua Tail 37, Whirlpool 42, U-turn 48, Ice Fang 50, Bounce 53, Air Slash 55 | Lumineon |
| Tentacruel | super rod | 33 | Oxide | BubbleBeam, Wrap, Barrier, Water Pulse | Poison Jab 36, Screech 42, Hydro Pump 49, Wring Out 55 | Tentacruel |
| Tentacruel | super rod | 33 | Rewrite | Toxic Spikes, BubbleBeam, Barrier, Water Pulse | Poison Jab 36, Surf 40, Screech 42, Psybeam 44, Sludge Bomb 50, Sludge Wave 52 | Tentacruel |
| Greninja | super rod | 36 | Oxide | Acrobatics, Low Kick, Waterfall, Fling | Scald 37, Dark Pulse 40, Extrasensory 43, Sludge Wave 47, Gunk Shot 51, Hydro Pump 55 | Greninja |
| Greninja | super rod | 36 | Rewrite | Low Kick, Waterfall, Fling, Shadow Sneak | Scald 37, Dark Pulse 40, Extrasensory 43, Sludge Wave 47, Surf 49, Gunk Shot 51, Ice Beam 56 | Greninja |

## Route 220

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 56 | At the cap |
|---|---|---|---|---|---|---|
| Jellicent | super rod | 36 | Oxide | Imprison, Confuse Ray, Hex, Brine | Pain Split 39, Destiny Bond 45, Shadow Ball 51, Scald 55 | Jellicent |
| Jellicent | super rod | 36 | Rewrite | Imprison, Confuse Ray, Hex, Brine | Pain Split 39, Muddy Water 45, Shadow Ball 51, Sludge Bomb 53, Scald 55 | Jellicent |
| Lanturn | super rod | 36 | Oxide | Swallow, Spit Up, BubbleBeam, Signal Beam | Discharge 40, Aqua Ring 47, Hydro Pump 52 | Lanturn |
| Lanturn | super rod | 36 | Rewrite | Swallow, Spit Up, BubbleBeam, Signal Beam | Scald 37, Discharge 40, Thunderbolt 42, Aqua Ring 47, Muddy Water 52 | Lanturn |
| Lumineon | super rod | 39 | Oxide | Water Pulse, Captivate, Safeguard, Aqua Ring | Whirlpool 42, U-turn 48, Bounce 53 | Lumineon |
| Lumineon | super rod | 39 | Rewrite | Safeguard, Flip Turn, Aqua Ring, Aqua Tail | Whirlpool 42, U-turn 48, Ice Fang 50, Bounce 53, Air Slash 55 | Lumineon |
| Tentacruel | super rod | 39 to 42 | Oxide | Wrap, Barrier, Water Pulse, Poison Jab | Screech 42, Hydro Pump 49, Wring Out 55 | Tentacruel |
| Tentacruel | super rod | 39 to 42 | Rewrite | BubbleBeam, Barrier, Water Pulse, Poison Jab | Surf 40, Screech 42, Psybeam 44, Sludge Bomb 50, Sludge Wave 52 | Tentacruel |

## Route 221

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 56 | At the cap |
|---|---|---|---|---|---|---|
| Lanturn | super rod | 36 | Oxide | Swallow, Spit Up, BubbleBeam, Signal Beam | Discharge 40, Aqua Ring 47, Hydro Pump 52 | Lanturn |
| Lanturn | super rod | 36 | Rewrite | Swallow, Spit Up, BubbleBeam, Signal Beam | Scald 37, Discharge 40, Thunderbolt 42, Aqua Ring 47, Muddy Water 52 | Lanturn |
| Lumineon | super rod | 36 | Oxide | Water Pulse, Captivate, Safeguard, Aqua Ring | Whirlpool 42, U-turn 48, Bounce 53 | Lumineon |
| Lumineon | super rod | 36 | Rewrite | Captivate, Safeguard, Flip Turn, Aqua Ring | Aqua Tail 37, Whirlpool 42, U-turn 48, Ice Fang 50, Bounce 53, Air Slash 55 | Lumineon |
| Octillery | super rod | 39 | Oxide | Focus Energy, Octazooka, Bullet Seed, Wring Out | Signal Beam 42, Ice Beam 48, Hyper Beam 55 | Octillery |
| Octillery | super rod | 39 | Rewrite | Round, Bullet Seed, Mud Shot, Scald | Signal Beam 42, Seed Bomb 44, Ice Beam 48, Skitter Smack 51, Hyper Beam 55 | Octillery |
| Tentacruel | super rod | 39 | Oxide | Wrap, Barrier, Water Pulse, Poison Jab | Screech 42, Hydro Pump 49, Wring Out 55 | Tentacruel |
| Tentacruel | super rod | 39 | Rewrite | BubbleBeam, Barrier, Water Pulse, Poison Jab | Surf 40, Screech 42, Psybeam 44, Sludge Bomb 50, Sludge Wave 52 | Tentacruel |
| Greninja | super rod | 42 | Oxide | Waterfall, Fling, Scald, Dark Pulse | Extrasensory 43, Sludge Wave 47, Gunk Shot 51, Hydro Pump 55 | Greninja |
| Greninja | super rod | 42 | Rewrite | Fling, Shadow Sneak, Scald, Dark Pulse | Extrasensory 43, Sludge Wave 47, Surf 49, Gunk Shot 51, Ice Beam 56 | Greninja |

## Snowpoint City

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 56 | At the cap |
|---|---|---|---|---|---|---|
| Suicune | in-game trade | 1 | Oxide | Bite, Leer | BubbleBeam 8, Gust 22, Aurora Beam 29, Mist 36, Mirror Coat 43, Ice Fang 50 | Suicune |
| Suicune | in-game trade | 1 | Rewrite | Bite | BubbleBeam 8, Gust 22, Aurora Beam 29, Mist 36, Mirror Coat 43, Ice Fang 50, Calm Mind 54 | Suicune |
| Seel | old rod | 16 to 17 | Oxide | Growl, Water Sport, Icy Wind, Encore | Ice Shard 17, Rest 21, Aqua Ring 23, Aurora Beam 27, Aqua Jet 31, Brine 33; as Dewgong: Sheer Cold 34, Take Down 37, Dive 41, Aqua Tail 43, Ice Beam 47, Safeguard 51 | Dewgong (from 34) |
| Seel | old rod | 16 to 17 | Rewrite | Growl, Water Sport, Icy Wind, Encore | Ice Shard 17, Rest 21, Aqua Ring 23, Aurora Beam 27, Aqua Jet 31, Brine 33; as Dewgong: Signal Beam 34, Take Down 37, Dive 41, Aqua Tail 43, Drill Run 45, Ice Beam 47, Safeguard 51, Bite 54, Headbutt 56 | Dewgong (from 34) |
| Spheal | old rod | 16 | Oxide | Growl, Water Gun, Encore, Ice Ball | Body Slam 19, Aurora Beam 25; as Sealeo: Swagger 32, Rest 39, Snore 39; as Walrein: Ice Fang 44, Blizzard 52 | Walrein (from 44) |
| Spheal | old rod | 16 | Rewrite | Growl, Water Gun, Encore, Ice Ball | Body Slam 19, Aurora Beam 25, Signal Beam 27; as Sealeo: Swagger 32, Rest 39; as Walrein: Ice Fang 44, Crunch 46, Ice Beam 52, Body Press 54, Surf 56 | Walrein (from 44) |
| Shellos | old rod | 17 | Oxide | Harden, Water Pulse, Mud Bomb, Hidden Power | Body Slam 29; as Gastrodon: Muddy Water 41, Recover 54 | Gastrodon (from 30) |
| Shellos | old rod | 17 | Rewrite | Swagger, Water Pulse, Mud Bomb, Hidden Power | Body Slam 29; as Gastrodon: AncientPower 31, Clear Smog 34, Muddy Water 41, Earth Power 43, Bulldoze 45, Ice Beam 50, Recover 54 | Gastrodon (from 30) |
| Snorunt | old rod | 18 | Oxide | Leer, Double Team, Bite, Icy Wind | Headbutt 19, Protect 22, Ice Fang 28, Crunch 31, Ice Shard 37; as Glalie: Blizzard 51 | Glalie (from 42) |
| Snorunt | old rod | 18 | Oxide | Leer, Double Team, Bite, Icy Wind | as Froslass: Confuse Ray 19, Ominous Wind 22, Wake-Up Slap 28, Captivate 31, Ice Shard 37, Blizzard 51 | Froslass (from 18) |
| Snorunt | old rod | 18 | Rewrite | Powder Snow, Leer, Bite, Icy Wind | Headbutt 19, Ominous Wind 22, Ice Fang 28, Crunch 31, Draining Kiss 35, Ice Shard 37; as Glalie: Rock Slide 42, Power Gem 44, Earth Power 46, Icicle Crash 48, Shadow Ball 53, Dark Pulse 55 | Glalie (from 42) |
| Snorunt | old rod | 18 | Rewrite | Powder Snow, Leer, Bite, Icy Wind | as Froslass: Confuse Ray 19, Ominous Wind 22, Wake-Up Slap 28, Captivate 31, Ice Shard 37, Signal Beam 44, Ice Beam 51 | Froslass (from 18) |
| Seel | good rod | 28 to 30 | Oxide | Ice Shard, Rest, Aqua Ring, Aurora Beam | Aqua Jet 31, Brine 33; as Dewgong: Sheer Cold 34, Take Down 37, Dive 41, Aqua Tail 43, Ice Beam 47, Safeguard 51 | Dewgong (from 34) |
| Seel | good rod | 28 to 30 | Rewrite | Ice Shard, Rest, Aqua Ring, Aurora Beam | Aqua Jet 31, Brine 33; as Dewgong: Signal Beam 34, Take Down 37, Dive 41, Aqua Tail 43, Drill Run 45, Ice Beam 47, Safeguard 51, Bite 54, Headbutt 56 | Dewgong (from 34) |
| Spheal | good rod | 28 | Oxide | Encore, Ice Ball, Body Slam, Aurora Beam | as Sealeo: Swagger 32, Rest 39, Snore 39; as Walrein: Ice Fang 44, Blizzard 52 | Walrein (from 44) |
| Spheal | good rod | 28 | Rewrite | Ice Ball, Body Slam, Aurora Beam, Signal Beam | as Sealeo: Swagger 32, Rest 39; as Walrein: Ice Fang 44, Crunch 46, Ice Beam 52, Body Press 54, Surf 56 | Walrein (from 44) |
| Snover | good rod | 30 | Oxide | GrassWhistle, Swagger, Mist, Ice Shard | Ingrain 31, Wood Hammer 36; as Abomasnow: Blizzard 47 | Abomasnow (from 40) |
| Snover | good rod | 30 | Rewrite | Mist, Ice Shard, Rock Tomb, Seed Bomb | Wood Hammer 36; as Abomasnow: Ice Punch 45, Ice Beam 47, Body Press 53, Giga Drain 55 | Abomasnow (from 40) |
| Lapras | good rod | 32 | Oxide | Water Pulse, Body Slam, Perish Song, Ice Beam | Brine 37, Safeguard 43, Hydro Pump 49, Sheer Cold 55 | Lapras |
| Lapras | good rod | 32 | Rewrite | Water Pulse, Body Slam, Perish Song, Ice Beam | Confuse Ray 33, Brine 37, Safeguard 43, Muddy Water 49, Drill Run 54 | Lapras |
| Dewgong | super rod | 38 to 41 | Oxide | Aqua Jet, Brine, Sheer Cold, Take Down | Dive 41, Aqua Tail 43, Ice Beam 47, Safeguard 51 | Dewgong |
| Dewgong | super rod | 38 to 41 | Rewrite | Aqua Jet, Brine, Signal Beam, Take Down | Dive 41, Aqua Tail 43, Drill Run 45, Ice Beam 47, Safeguard 51, Bite 54, Headbutt 56 | Dewgong |
| Sealeo | super rod | 38 | Oxide | Ice Ball, Body Slam, Aurora Beam, Swagger | Rest 39, Snore 39; as Walrein: Ice Fang 44, Blizzard 52 | Walrein (from 44) |
| Sealeo | super rod | 38 | Rewrite | Ice Ball, Body Slam, Aurora Beam, Swagger | Rest 39; as Walrein: Ice Fang 44, Crunch 46, Ice Beam 52, Body Press 54, Surf 56 | Walrein (from 44) |
| Froslass | super rod | 41 | Oxide | Ominous Wind, Wake-Up Slap, Captivate, Ice Shard | Blizzard 51 | Froslass |
| Froslass | super rod | 41 | Rewrite | Ominous Wind, Wake-Up Slap, Captivate, Ice Shard | Signal Beam 44, Ice Beam 51 | Froslass |
| Lapras | super rod | 44 | Oxide | Perish Song, Ice Beam, Brine, Safeguard | Hydro Pump 49, Sheer Cold 55 | Lapras |
| Lapras | super rod | 44 | Rewrite | Ice Beam, Confuse Ray, Brine, Safeguard | Muddy Water 49, Drill Run 54 | Lapras |

## Twinleaf Town

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 56 | At the cap |
|---|---|---|---|---|---|---|
| Crawdaunt | super rod | 30 | Oxide | BubbleBeam, Protect, Knock Off, Swift | Taunt 34, Night Slash 39, Crabhammer 44, Swords Dance 52 | Crawdaunt |
| Crawdaunt | super rod | 30 | Rewrite | Leer, BubbleBeam, Knock Off, Swift | Taunt 34, Metal Claw 36, Night Slash 39, Throat Chop 41, Crabhammer 44, X-Scissor 46, Swords Dance 52 | Crawdaunt |
| Lanturn | super rod | 30 | Oxide | Stockpile, Swallow, Spit Up, BubbleBeam | Signal Beam 35, Discharge 40, Aqua Ring 47, Hydro Pump 52 | Lanturn |
| Lanturn | super rod | 30 | Rewrite | Stockpile, Swallow, Spit Up, BubbleBeam | Signal Beam 35, Scald 37, Discharge 40, Thunderbolt 42, Aqua Ring 47, Muddy Water 52 | Lanturn |
| Floatzel | super rod | 33 | Oxide | Swift, Aqua Jet, Crunch, Agility | Whirlpool 39, Razor Wind 50 | Floatzel |
| Floatzel | super rod | 33 | Rewrite | Aqua Jet, Crunch, Flip Turn, Icy Wind | Waterfall 35, Whirlpool 39, Liquidation 43, Low Sweep 45, Rock Tomb 51, Agility 52 | Floatzel |
| Sharpedo | super rod | 33 | Oxide | Swagger, Assurance, Crunch, Slash | Aqua Jet 34, Taunt 40, Agility 45, Skull Bash 50, Night Slash 56 | Sharpedo |
| Sharpedo | super rod | 33 | Rewrite | Swagger, Assurance, Crunch, Slash | Aqua Jet 34, Taunt 40, Agility 45, Liquidation 46, Skull Bash 50, Poison Jab 52, Night Slash 56 | Sharpedo |
| Swampert | super rod | 36 | Oxide | Mud Shot, Foresight, Mud Bomb, Take Down | Muddy Water 39, Protect 46, Earthquake 52 | Swampert |
| Swampert | super rod | 36 | Rewrite | Foresight, Mud Bomb, Take Down, Waterfall | Muddy Water 39, Brick Break 41, Aqua Tail 43, Poison Jab 48, Earthquake 52, Body Slam 56 | Swampert |

## Valley Windworks

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 56 | At the cap |
|---|---|---|---|---|---|---|
| Crawdaunt | super rod | 30 | Oxide | BubbleBeam, Protect, Knock Off, Swift | Taunt 34, Night Slash 39, Crabhammer 44, Swords Dance 52 | Crawdaunt |
| Crawdaunt | super rod | 30 | Rewrite | Leer, BubbleBeam, Knock Off, Swift | Taunt 34, Metal Claw 36, Night Slash 39, Throat Chop 41, Crabhammer 44, X-Scissor 46, Swords Dance 52 | Crawdaunt |
| Whiscash | super rod | 30 | Oxide | Mud Bomb, Amnesia, Water Pulse, Magnitude | Rest 33, Snore 33, Aqua Tail 39, Earthquake 45, Future Sight 51 | Whiscash |
| Whiscash | super rod | 30 | Rewrite | Amnesia, Water Pulse, Magnitude, Bulldoze | Rest 33, Zen Headbutt 35, Aqua Tail 39, Wild Charge 42, Earthquake 45, Future Sight 51, Ice Beam 53 | Whiscash |
| Lanturn | super rod | 33 | Oxide | Stockpile, Swallow, Spit Up, BubbleBeam | Signal Beam 35, Discharge 40, Aqua Ring 47, Hydro Pump 52 | Lanturn |
| Lanturn | super rod | 33 | Rewrite | Stockpile, Swallow, Spit Up, BubbleBeam | Signal Beam 35, Scald 37, Discharge 40, Thunderbolt 42, Aqua Ring 47, Muddy Water 52 | Lanturn |
| Sharpedo | super rod | 33 | Oxide | Swagger, Assurance, Crunch, Slash | Aqua Jet 34, Taunt 40, Agility 45, Skull Bash 50, Night Slash 56 | Sharpedo |
| Sharpedo | super rod | 33 | Rewrite | Swagger, Assurance, Crunch, Slash | Aqua Jet 34, Taunt 40, Agility 45, Liquidation 46, Skull Bash 50, Poison Jab 52, Night Slash 56 | Sharpedo |
| Greninja | super rod | 36 | Oxide | Acrobatics, Low Kick, Waterfall, Fling | Scald 37, Dark Pulse 40, Extrasensory 43, Sludge Wave 47, Gunk Shot 51, Hydro Pump 55 | Greninja |
| Greninja | super rod | 36 | Rewrite | Low Kick, Waterfall, Fling, Shadow Sneak | Scald 37, Dark Pulse 40, Extrasensory 43, Sludge Wave 47, Surf 49, Gunk Shot 51, Ice Beam 56 | Greninja |

## Honey trees

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 56 | At the cap |
|---|---|---|---|---|---|---|
| Frosmoth | honey | 32 | Oxide | Defog, FeatherDance, Aurora Beam, Bug Buzz | Aurora Veil 36, Blizzard 40, Tailwind 44, Wide Guard 48, Quiver Dance 52 | Frosmoth |
| Frosmoth | honey | 32 | Rewrite | Attract, Stun Spore, Infestation, Bug Buzz | Defog 33, Aurora Beam 34, Aurora Veil 36, Psybeam 38, Ice Beam 40, Tailwind 44, Wide Guard 48, Giga Drain 50, Quiver Dance 52 | Frosmoth |
| Galvantula | honey | 32 | Oxide | Bug Bite, Gastro Acid, Struggle Bug, Discharge | Signal Beam 35, Energy Ball 39, Sucker Punch 43, Thunderbolt 48, Bug Buzz 51, Thunder 55 | Galvantula |
| Galvantula | honey | 32 | Rewrite | Gastro Acid, Struggle Bug, Discharge, Snarl | Signal Beam 35, Energy Ball 39, Sucker Punch 43, Giga Drain 45, Thunderbolt 48, Bug Buzz 51, Agility 54 | Galvantula |
| Heracross | honey | 32 | Oxide | Aerial Ace, Brick Break, Counter, Take Down | Close Combat 37, Reversal 43, Feint 49, Megahorn 55 | Heracross |
| Heracross | honey | 32 | Rewrite | Brick Break, Counter, Rock Tomb, Take Down | Leech Life 35, Close Combat 37, Reversal 43, Throat Chop 45, Lunge 51, Megahorn 55 | Heracross |
| Larvesta | honey | 32 | Oxide | String Shot, Flame Charge, Struggle Bug, Flame Wheel | Bug Bite 40, Take Down 50 | Larvesta; Volcarona in HQ |
| Larvesta | honey | 32 | Rewrite | Flame Charge, Struggle Bug, U-turn, Flame Wheel | Bug Bite 40, Fire Spin 41, Screech 45, Poison Jab 47, Take Down 50 | Larvesta; Volcarona in HQ |
| Leavanny | honey | 32 | Oxide | Razor Leaf, Struggle Bug, Fell Stinger, Helping Hand | Leaf Blade 36, X-Scissor 39, Entrainment 43, Swords Dance 46, Leaf Storm 50 | Leavanny |
| Leavanny | honey | 32 | Rewrite | Razor Leaf, Struggle Bug, Fell Stinger, Helping Hand | Leaf Blade 36, X-Scissor 39, Entrainment 43, Swords Dance 46, Poison Jab 48, Leaf Storm 50, Slash 54 | Leavanny |
| Scizor | honey | 32 | Oxide | Agility, Metal Claw, Fury Cutter, Slash | Razor Wind 33, Iron Defense 37, X-Scissor 41, Night Slash 45, Double Hit 49, Iron Head 53 | Scizor |
| Scizor | honey | 32 | Rewrite | Metal Claw, Fury Cutter, Steel Wing, Slash | Iron Defense 37, X-Scissor 41, Brick Break 43, Night Slash 45, Double Hit 49, Iron Head 53, Skitter Smack 55 | Scizor |
| Shiftry | honey | 32 | Oxide | Faint Attack, Whirlwind, Nasty Plot, Razor Leaf | Leaf Storm 49 | Shiftry |
| Shiftry | honey | 32 | Rewrite | Whirlwind, Nasty Plot, Razor Leaf, Silver Wind | Leaf Blade 34, Rock Slide 40, Extrasensory 43, Leaf Storm 49, Sucker Punch 50, Throat Chop 56 | Shiftry |
| Snorlax | honey | 32 | Oxide | Yawn, Rest, Snore, Sleep Talk | Body Slam 33, Block 36, Rollout 41, Crunch 44, Giga Impact 49 | Snorlax |
| Snorlax | honey | 32 | Rewrite | Tackle, Amnesia, Lick, Yawn | Body Slam 33, Block 36, Bulldoze 38, Rollout 41, Crunch 44, Giga Impact 49, Body Press 51, Slam 56 | Snorlax |
| Toucannon | honey | 32 | Oxide | Pluck, Roost, Fury Attack, Screech | Drill Peck 34, Bullet Seed 40, FeatherDance 44, Hyper Voice 50 | Toucannon |
| Toucannon | honey | 32 | Rewrite | Supersonic, Pluck, Roost, Screech | Drill Peck 34, Facade 36, Bullet Seed 40, Throat Chop 42, FeatherDance 44, Hyper Voice 50, Take Down 52 | Toucannon |
| Vespiquen | honey | 32 | Oxide | Power Gem, Heal Order, Toxic, Slash | Captivate 33, Attack Order 37, Swagger 39, Destiny Bond 43 | Vespiquen |
| Vespiquen | honey | 32 | Rewrite | Pursuit, Heal Order, Toxic, Slash | Captivate 33, Confuse Ray 34, Attack Order 37, Swagger 39, Pounce 41, Air Slash 43, U-turn 45, Psychic Noise 51, Poison Jab 53 | Vespiquen |
| Vikavolt | honey | 32 | Oxide | Thunderbolt, Crunch, Bite, Spark | Signal Beam 36, Discharge 48, Bug Buzz 55 | Vikavolt |
| Vikavolt | honey | 32 | Rewrite | Thunderbolt, Crunch, Bite, Spark | Discharge 33, Signal Beam 36, Mud Shot 38, Flash Cannon 40, Bug Buzz 55 | Vikavolt |
| Yanma | honey | 32 | Oxide | Detect, Supersonic, Uproar, Pursuit | AncientPower 33; as Yanmega: Feint 38, Slash 43, Screech 46, U-turn 49, Air Slash 54 | Yanmega (from 35) |
| Yanma | honey | 32 | Rewrite | SonicBoom, Screech, Uproar, Pursuit | AncientPower 33, Air Slash 34, Bug Buzz 35; as Yanmega: Ominous Wind 40, Slash 43, Screech 46, U-turn 49, Psychic Noise 51, Air Slash 54 | Yanmega (from 35) |

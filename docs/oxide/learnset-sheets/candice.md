# Candice's split: what each catch knows and learns

Written by `tools/oxide/balance/learncheck.py sheets` for check 6 of the learnset baseline (`docs/oxide/learnset-checks.md`). One table per capture area first offered in Candice's split, whose cap is 56. Each Pokemon is read at the lowest level it is found at there. "Knows at capture" is the last four moves its list gives by that level; "learns by level-up" is every entry it reaches after capture up to 56, evolving on time, with each later stage's moves under its name; "at the cap" is the stage it can be by then and the next one after. A row marked Rewrite shows the learnset rewrite's lists (the tree's) where it differs from the row marked Oxide, Oxide's lists before the learnset rewrite (`da6b92496c`); a row marked both is the same in each. Relearner-only moves and egg moves are left out.

## Acuity Lakefront

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 56 | At the cap |
|---|---|---|---|---|---|---|
| Sneasel | wild | 32 to 35 | Oxide | Faint Attack, Fury Swipes, Agility, Icy Wind | Slash 35, Metal Claw 42, Ice Shard 49 | Sneasel; Weavile in HQ |
| Sneasel | wild | 32 to 35 | Rewrite | Fury Swipes, Nasty Plot, Agility, Icy Wind | Slash 35, Low Sweep 38, Poison Jab 40, Metal Claw 42, Ice Shard 49, Ice Fang 53, Night Slash 54, Ice Punch 56 | Sneasel; Weavile in HQ |
| Absol | wild | 33 to 35 | Oxide | Pursuit, Swords Dance, Bite, Double Team | Slash 36, Future Sight 41, Sucker Punch 44, Detect 49, Night Slash 52 | Absol |
| Absol | wild | 33 to 35 | Rewrite | Quick Attack, Pursuit, Swords Dance, Bite | Slash 36, Future Sight 41, Sucker Punch 44, X-Scissor 48, Night Slash 52, Shadow Ball 54, Throat Chop 56 | Absol |
| Alolan Ninetales | wild | 33 | Oxide | Tail Whip, Disable, Ice Shard, Safeguard | nothing | Alolan Ninetales |
| Alolan Ninetales | wild | 33 | Rewrite | Incinerate, Spite, Payback, Icy Wind | Chilling Water 36, Dazzling Gleam 39, Extrasensory 43, Ice Beam 44, Dark Pulse 48, Mystical Fire 53, BurningJealousy 54, Moonblast 56 | Alolan Ninetales |
| Delibird | wild | 33 | Oxide | Present | nothing | Delibird |
| Delibird | wild | 33 | Rewrite | Present | Swagger 34, Ice Beam 54, Drill Run 55, Drill Peck 56 | Delibird |
| Frosmoth | wild | 33 to 34 | Oxide | Defog, FeatherDance, Aurora Beam, Bug Buzz | Aurora Veil 36, Blizzard 40, Tailwind 44, Wide Guard 48, Quiver Dance 52 | Frosmoth |
| Frosmoth | wild | 33 to 34 | Rewrite | Stun Spore, Infestation, Bug Buzz, Defog | Aurora Beam 34, Aurora Veil 36, Ice Beam 40, Tailwind 44, Wide Guard 48, Quiver Dance 52, Air Slash 54, Giga Drain 56 | Frosmoth |
| Seel | wild | 33 | Oxide | Aqua Ring, Aurora Beam, Aqua Jet, Brine | as Dewgong: Sheer Cold 34, Take Down 37, Dive 41, Aqua Tail 43, Ice Beam 47, Safeguard 51 | Dewgong (from 34) |
| Seel | wild | 33 | Rewrite | Aqua Ring, Aurora Beam, Aqua Jet, Brine | as Dewgong: Signal Beam 34, Take Down 37, Drill Run 40, Dive 41, Aqua Tail 43, Ice Beam 47, Safeguard 51, Muddy Water 54, Bite 56 | Dewgong (from 34) |
| Snover | wild | 33 to 34 | Oxide | Swagger, Mist, Ice Shard, Ingrain | Wood Hammer 36; as Abomasnow: Blizzard 47 | Abomasnow (from 40) |
| Snover | wild | 33 to 34 | Rewrite | Mist, Ice Shard, Seed Bomb, Rock Tomb | Body Press 34, Wood Hammer 36; as Abomasnow: Ice Beam 41, Giga Drain 50, Ice Punch 53, Rock Climb 54, Shadow Ball 56 | Abomasnow (from 40) |
| Snorunt | wild | 34 | Oxide | Headbutt, Protect, Ice Fang, Crunch | Ice Shard 37; as Glalie: Blizzard 51 | Glalie (from 42) |
| Snorunt | wild | 34 | Oxide | Headbutt, Protect, Ice Fang, Crunch | as Froslass: Ice Shard 37, Blizzard 51 | Froslass (from 34) |
| Snorunt | wild | 34 | Rewrite | Ominous Wind, Ice Fang, Crunch, Draining Kiss | Ice Shard 37; as Glalie: Rock Slide 42, Power Gem 44, Confuse Ray 48, Earth Power 53, Ice Punch 54, Shadow Ball 56 | Glalie (from 42) |
| Snorunt | wild | 34 | Rewrite | Ominous Wind, Ice Fang, Crunch, Draining Kiss | as Froslass: Ice Shard 37, Ice Beam 51 | Froslass (from 34) |
| Jynx | wild | 35 | Oxide | Mean Look, Fake Tears, Wake-Up Slap, Avalanche | Body Slam 39, Wring Out 44, Perish Song 49, Blizzard 55 | Jynx |
| Jynx | wild | 35 | Rewrite | Fake Tears, Ice Punch, Wake-Up Slap, Avalanche | Body Slam 39, Aurora Beam 41, Psychic 44, Perish Song 49, Shadow Ball 52, Energy Ball 54, Ice Beam 55 | Jynx |

## Canalave City

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 56 | At the cap |
|---|---|---|---|---|---|---|
| Gastrodon | super rod | 36 | Oxide | Water Pulse, Mud Bomb, Hidden Power, Body Slam | Muddy Water 41, Recover 54 | Gastrodon |
| Gastrodon | super rod | 36 | Rewrite | Hidden Power, Body Slam, AncientPower, Earth Power | Clear Smog 37, Muddy Water 41, Bulldoze 44, Sludge Bomb 46, Ice Beam 49, Recover 54, Skitter Smack 56 | Gastrodon |
| Lumineon | super rod | 36 | Oxide | Water Pulse, Captivate, Safeguard, Aqua Ring | Whirlpool 42, U-turn 48, Bounce 53 | Lumineon |
| Lumineon | super rod | 36 | Rewrite | Safeguard, Flip Turn, Aqua Ring, Icy Wind | Aqua Tail 38, Signal Beam 40, Whirlpool 42, Ice Fang 45, U-turn 48, Bounce 53, Air Slash 54, Crunch 56 | Lumineon |
| Jellicent | super rod | 39 | Oxide | Confuse Ray, Hex, Brine, Pain Split | Destiny Bond 45, Shadow Ball 51, Scald 55 | Jellicent |
| Jellicent | super rod | 39 | Rewrite | Confuse Ray, Hex, Brine, Pain Split | Muddy Water 45, Shadow Ball 51, Sludge Bomb 54, Scald 55 | Jellicent |
| Toxapex | super rod | 42 | Oxide | Spike Cannon, Pin Missile, Toxic, Venom Drench | Poison Jab 43, Liquidation 45 | Toxapex |
| Toxapex | super rod | 42 | Rewrite | Spike Cannon, Toxic, Pin Missile, Venom Drench | Poison Jab 43, Liquidation 45, Lunge 53, Ice Beam 54, Sludge Bomb 56 | Toxapex |

## Celestic Town

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 56 | At the cap |
|---|---|---|---|---|---|---|
| Milotic | super rod | 36 | Oxide | Twister, Recover, Captivate, Aqua Tail | Hydro Pump 37, Attract 41, Safeguard 45, Aqua Ring 49 | Milotic |
| Milotic | super rod | 36 | Rewrite | Recover, Aqua Tail, Aurora Beam, Dragon Pulse | Surf 37, Attract 41, Muddy Water 43, Safeguard 45, Aqua Ring 49, Alluring Voice 54, Scald 56 | Milotic |
| Whiscash | super rod | 36 | Oxide | Water Pulse, Magnitude, Rest, Snore | Aqua Tail 39, Earthquake 45, Future Sight 51 | Whiscash |
| Whiscash | super rod | 36 | Rewrite | Magnitude, Bulldoze, Rest, Zen Headbutt | Aqua Tail 39, Earth Power 40, Wild Charge 42, Earthquake 45, Future Sight 51, Spark 54, Ice Beam 56 | Whiscash |
| Crawdaunt | super rod | 39 | Oxide | Knock Off, Swift, Taunt, Night Slash | Crabhammer 44, Swords Dance 52 | Crawdaunt |
| Crawdaunt | super rod | 39 | Rewrite | Taunt, Throat Chop, Aerial Ace, Night Slash | X-Scissor 41, Crabhammer 44, Brick Break 48, Swords Dance 52, Rock Tomb 54 | Crawdaunt |
| Lanturn | super rod | 39 to 42 | Oxide | Swallow, Spit Up, BubbleBeam, Signal Beam | Discharge 40, Aqua Ring 47, Hydro Pump 52 | Lanturn |
| Lanturn | super rod | 39 to 42 | Rewrite | Signal Beam, Scald, Surf, Thunderbolt | Discharge 40, Flash Cannon 43, Aqua Ring 47, Muddy Water 52, Volt Switch 54, Dazzling Gleam 55 | Lanturn |

## Eterna City

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 56 | At the cap |
|---|---|---|---|---|---|---|
| Lanturn | super rod | 30 | Oxide | Stockpile, Swallow, Spit Up, BubbleBeam | Signal Beam 35, Discharge 40, Aqua Ring 47, Hydro Pump 52 | Lanturn |
| Lanturn | super rod | 30 | Rewrite | Stockpile, Swallow, Spit Up, BubbleBeam | Signal Beam 31, Scald 33, Surf 34, Thunderbolt 37, Discharge 40, Flash Cannon 43, Aqua Ring 47, Muddy Water 52, Volt Switch 54, Dazzling Gleam 55 | Lanturn |
| Sharpedo | super rod | 30 | Oxide | Swagger, Assurance, Crunch, Slash | Aqua Jet 34, Taunt 40, Agility 45, Skull Bash 50, Night Slash 56 | Sharpedo |
| Sharpedo | super rod | 30 | Rewrite | Swagger, Assurance, Crunch, Slash | Aqua Jet 31, Bug Bite 35, Aerial Ace 37, Taunt 40, Liquidation 41, Agility 45, Skull Bash 50, Poison Fang 54, Night Slash 56 | Sharpedo |
| Alomomola | super rod | 33 | Oxide | Protect, Water Pulse, Wake-Up Slap, Soak | Wish 37, Brine 41, Safeguard 45, Whirlpool 49, Helping Hand 53 | Alomomola |
| Alomomola | super rod | 33 | Rewrite | Heal Pulse, Wake-Up Slap, Water Pulse, Soak | Play Rough 35, Wish 37, Brine 41, Zen Headbutt 43, Safeguard 45, Whirlpool 49, Helping Hand 53, Flip Turn 54, Liquidation 56 | Alomomola |
| Floatzel | super rod | 33 to 36 | Oxide | Swift, Aqua Jet, Crunch, Agility | Whirlpool 39, Razor Wind 50 | Floatzel |
| Floatzel | super rod | 33 to 36 | Rewrite | Aqua Jet, Crunch, Icy Wind, Flip Turn | Waterfall 36, Whirlpool 39, Liquidation 41, Low Sweep 44, Agility 51, Rock Tomb 53, Ice Fang 56 | Floatzel |

## Fuego Ironworks

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 56 | At the cap |
|---|---|---|---|---|---|---|
| Seaking | super rod | 36 | Oxide | Water Pulse, Flail, Aqua Ring, Fury Attack | Waterfall 40, Horn Drill 47, Agility 56 | Seaking |
| Seaking | super rod | 36 | Rewrite | Water Pulse, Flail, Aqua Ring, Aqua Jet | Skull Bash 37, Waterfall 40, Poison Jab 44, Drill Run 47, Knock Off 50, Aqua Tail 54, Agility 56 | Seaking |
| Whiscash | super rod | 36 | Oxide | Water Pulse, Magnitude, Rest, Snore | Aqua Tail 39, Earthquake 45, Future Sight 51 | Whiscash |
| Whiscash | super rod | 36 | Rewrite | Magnitude, Bulldoze, Rest, Zen Headbutt | Aqua Tail 39, Earth Power 40, Wild Charge 42, Earthquake 45, Future Sight 51, Spark 54, Ice Beam 56 | Whiscash |
| Crawdaunt | super rod | 39 | Oxide | Knock Off, Swift, Taunt, Night Slash | Crabhammer 44, Swords Dance 52 | Crawdaunt |
| Crawdaunt | super rod | 39 | Rewrite | Taunt, Throat Chop, Aerial Ace, Night Slash | X-Scissor 41, Crabhammer 44, Brick Break 48, Swords Dance 52, Rock Tomb 54 | Crawdaunt |
| Lanturn | super rod | 39 | Oxide | Swallow, Spit Up, BubbleBeam, Signal Beam | Discharge 40, Aqua Ring 47, Hydro Pump 52 | Lanturn |
| Lanturn | super rod | 39 | Rewrite | Signal Beam, Scald, Surf, Thunderbolt | Discharge 40, Flash Cannon 43, Aqua Ring 47, Muddy Water 52, Volt Switch 54, Dazzling Gleam 55 | Lanturn |
| Relicanth | super rod | 42 | Oxide | Rock Tomb, Yawn, Take Down, Mud Sport | AncientPower 43, Double-Edge 50 | Relicanth |
| Relicanth | super rod | 42 | Rewrite | Water Gun, Rock Tomb, Yawn, Take Down | AncientPower 43, Bulldoze 46, Double-Edge 50, Aqua Tail 54, Rock Slide 55 | Relicanth |

## Great Marsh

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 56 | At the cap |
|---|---|---|---|---|---|---|
| Araquanid | super rod | 35 to 38 | Oxide | BubbleBeam, Bug Bite, Headbutt, Soak | Dive 36, Lunge 41, Scald 48, Hydro Pump 51, Liquidation 55 | Araquanid |
| Araquanid | super rod | 35 to 38 | Rewrite | Headbutt, Spider Web, Soak, Skitter Smack | Dive 36, Waterfall 38, Lunge 41, Poison Jab 44, Scald 48, Crunch 51, Body Slam 54, Liquidation 55 | Araquanid |
| Crawdaunt | super rod | 35 to 38 | Oxide | Protect, Knock Off, Swift, Taunt | Night Slash 39, Crabhammer 44, Swords Dance 52 | Crawdaunt |
| Crawdaunt | super rod | 35 to 38 | Rewrite | Knock Off, Swift, Taunt, Throat Chop | Aerial Ace 36, Night Slash 39, X-Scissor 41, Crabhammer 44, Brick Break 48, Swords Dance 52, Rock Tomb 54 | Crawdaunt |
| Jellicent | super rod | 35 to 38 | Oxide | Imprison, Confuse Ray, Hex, Brine | Pain Split 39, Destiny Bond 45, Shadow Ball 51, Scald 55 | Jellicent |
| Jellicent | super rod | 35 to 38 | Rewrite | Imprison, Confuse Ray, Hex, Brine | Pain Split 39, Muddy Water 45, Shadow Ball 51, Sludge Bomb 54, Scald 55 | Jellicent |
| Kingdra | super rod | 35 | Oxide | BubbleBeam, Agility, Twister, Brine | Hydro Pump 40, Dragon Dance 48 | Kingdra |
| Kingdra | super rod | 35 | Rewrite | BubbleBeam, Agility, Twister, Brine | Octazooka 40, Aurora Beam 44, Scald 54 | Kingdra |
| Lombre | super rod | 35 | Oxide | Fury Swipes, Water Sport, BubbleBeam, Zen Headbutt | nothing | Ludicolo (from 35) |
| Lombre | super rod | 35 | Rewrite | BubbleBeam, Giga Drain, Zen Headbutt, Energy Ball | as Ludicolo: Ice Beam 54, Muddy Water 56 | Ludicolo (from 35) |
| Ludicolo | super rod | 35 to 38 | Oxide | Astonish, Growl, Mega Drain, Nature Power | nothing | Ludicolo |
| Ludicolo | super rod | 35 to 38 | Rewrite | Growl, Mega Drain, Nature Power, Energy Ball | Ice Beam 54, Muddy Water 56 | Ludicolo |
| Sharpedo | super rod | 35 | Oxide | Assurance, Crunch, Slash, Aqua Jet | Taunt 40, Agility 45, Skull Bash 50, Night Slash 56 | Sharpedo |
| Sharpedo | super rod | 35 | Rewrite | Crunch, Slash, Aqua Jet, Bug Bite | Aerial Ace 37, Taunt 40, Liquidation 41, Agility 45, Skull Bash 50, Poison Fang 54, Night Slash 56 | Sharpedo |
| Wailmer | super rod | 35 | Oxide | Mist, Rest, Brine, Water Spout | Amnesia 37; as Wailord: Dive 46, Bounce 54 | Wailord (from 40) |
| Wailmer | super rod | 35 | Rewrite | Rest, Bulldoze, Brine, Water Spout | Amnesia 37; as Wailord: Dive 46, Iron Head 48, Rock Tomb 50, Bounce 54, Zen Headbutt 55, Ice Beam 56 | Wailord (from 40) |
| Kingler | super rod | 38 | Oxide | Metal Claw, Stomp, Protect, Guillotine | Slam 44, Brine 51, Crabhammer 56 | Kingler |
| Kingler | super rod | 38 | Rewrite | Metal Claw, Stomp, Waterfall, Razor Shell | Rock Tomb 39, X-Scissor 41, Slam 44, Night Slash 47, Brine 51, Liquidation 54, Crabhammer 56 | Kingler |
| Quagsire | super rod | 38 | Oxide | Mud Bomb, Amnesia, Yawn, Earthquake | Mist 48, Haze 48, Muddy Water 53 | Quagsire |
| Quagsire | super rod | 38 | Rewrite | Amnesia, Trailblaze, Yawn, Earthquake | Rock Slide 39, Toxic 40, Drain Punch 44, Mist 48, Muddy Water 53, Poison Jab 54, Aqua Tail 56 | Quagsire |
| Qwilfish | super rod | 38 to 41 | Oxide | Spit Up, Revenge, Brine, Pin Missile | Take Down 41, Aqua Tail 45, Poison Jab 49, Destiny Bond 53 | Qwilfish |
| Qwilfish | super rod | 38 to 41 | Rewrite | Stockpile, Revenge, Brine, Pin Missile | Take Down 41, Throat Chop 43, Aqua Tail 45, Poison Jab 49, Flip Turn 54, Headbutt 55 | Qwilfish |
| Whiscash | super rod | 38 | Oxide | Water Pulse, Magnitude, Rest, Snore | Aqua Tail 39, Earthquake 45, Future Sight 51 | Whiscash |
| Whiscash | super rod | 38 | Rewrite | Magnitude, Bulldoze, Rest, Zen Headbutt | Aqua Tail 39, Earth Power 40, Wild Charge 42, Earthquake 45, Future Sight 51, Spark 54, Ice Beam 56 | Whiscash |
| Corsola | super rod | 41 | Oxide | Lucky Chant, AncientPower, Aqua Ring, Spike Cannon | Power Gem 44, Mirror Coat 48, Earth Power 53 | Corsola |
| Corsola | super rod | 41 | Rewrite | Aqua Cutter, Liquidation, Aqua Ring, Spike Cannon | Throat Chop 42, Power Gem 44, Mirror Coat 48, Earth Power 53, Rock Slide 54, Rock Tomb 56 | Corsola |
| Feraligatr | super rod | 41 | Oxide | Flail, Agility, Crunch, Slash | Screech 45, Thrash 50 | Feraligatr |
| Feraligatr | super rod | 41 | Rewrite | Slash, Bulldoze, Metal Claw, Aqua Jet | Liquidation 42, Screech 45 | Feraligatr |
| Greninja | super rod | 41 | Oxide | Waterfall, Fling, Scald, Dark Pulse | Extrasensory 43, Sludge Wave 47, Gunk Shot 51, Hydro Pump 55 | Greninja |
| Greninja | super rod | 41 | Rewrite | Fling, Shadow Sneak, Scald, Dark Pulse | Extrasensory 43, Sludge Wave 47, Gunk Shot 51, Ice Beam 54, Surf 56 | Greninja |
| Pelipper | super rod | 41 | Oxide | Roost, Stockpile, Swallow, Spit Up | Fling 43, Tailwind 50 | Pelipper |
| Pelipper | super rod | 41 | Rewrite | Swallow, Stockpile, Spit Up, Icy Wind | Fling 43, Air Slash 47, Tailwind 50, Brave Bird 53, Ice Beam 54, U-turn 55 | Pelipper |

## Iron Island

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 56 | At the cap |
|---|---|---|---|---|---|---|
| Gastrodon | super rod | 36 | Oxide | Water Pulse, Mud Bomb, Hidden Power, Body Slam | Muddy Water 41, Recover 54 | Gastrodon |
| Gastrodon | super rod | 36 | Rewrite | Hidden Power, Body Slam, AncientPower, Earth Power | Clear Smog 37, Muddy Water 41, Bulldoze 44, Sludge Bomb 46, Ice Beam 49, Recover 54, Skitter Smack 56 | Gastrodon |
| Jellicent | super rod | 36 | Oxide | Imprison, Confuse Ray, Hex, Brine | Pain Split 39, Destiny Bond 45, Shadow Ball 51, Scald 55 | Jellicent |
| Jellicent | super rod | 36 | Rewrite | Imprison, Confuse Ray, Hex, Brine | Pain Split 39, Muddy Water 45, Shadow Ball 51, Sludge Bomb 54, Scald 55 | Jellicent |
| Lanturn | super rod | 39 | Oxide | Swallow, Spit Up, BubbleBeam, Signal Beam | Discharge 40, Aqua Ring 47, Hydro Pump 52 | Lanturn |
| Lanturn | super rod | 39 | Rewrite | Signal Beam, Scald, Surf, Thunderbolt | Discharge 40, Flash Cannon 43, Aqua Ring 47, Muddy Water 52, Volt Switch 54, Dazzling Gleam 55 | Lanturn |
| Lumineon | super rod | 39 to 42 | Oxide | Water Pulse, Captivate, Safeguard, Aqua Ring | Whirlpool 42, U-turn 48, Bounce 53 | Lumineon |
| Lumineon | super rod | 39 to 42 | Rewrite | Flip Turn, Aqua Ring, Icy Wind, Aqua Tail | Signal Beam 40, Whirlpool 42, Ice Fang 45, U-turn 48, Bounce 53, Air Slash 54, Crunch 56 | Lumineon |

## Lake Acuity

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 56 | At the cap |
|---|---|---|---|---|---|---|
| Chinchou | old rod | 16 | Oxide | Supersonic, Thunder Wave, Flail, Water Gun | Confuse Ray 17, Spark 20, Take Down 23; as Lanturn: Stockpile 27, Swallow 27, Spit Up 27, BubbleBeam 30, Signal Beam 35, Discharge 40, Aqua Ring 47, Hydro Pump 52 | Lanturn (from 27) |
| Chinchou | old rod | 16 | Rewrite | Thunder Wave, Flail, Water Gun, Screech | Confuse Ray 17, Spark 20, Take Down 23, Icy Wind 26; as Lanturn: Stockpile 27, Swallow 28, Spit Up 29, BubbleBeam 30, Signal Beam 31, Scald 33, Surf 34, Thunderbolt 37, Discharge 40, Flash Cannon 43, Aqua Ring 47, Muddy Water 52, Volt Switch 54, Dazzling Gleam 55 | Lanturn (from 27) |
| Clamperl | old rod | 16 | Oxide | Clamp, Water Gun, Whirlpool, Iron Defense | as Huntail: Scary Face 19, Ice Fang 24, Brine 28, Baton Pass 33, Dive 37, Crunch 42, Aqua Tail 46, Hydro Pump 51 | Huntail (from 16) |
| Clamperl | old rod | 16 | Oxide | Clamp, Water Gun, Whirlpool, Iron Defense | as Gorebyss: Amnesia 19, Aqua Ring 24, Captivate 28, Baton Pass 33, Dive 37, Psychic 42, Aqua Tail 46, Hydro Pump 51 | Gorebyss (from 16) |
| Clamperl | old rod | 16 | Rewrite | Clamp, Water Gun, Whirlpool, Iron Defense | as Huntail: Scary Face 19, Ice Fang 24, Brine 28, Baton Pass 33, Flip Turn 35, Dive 37, Waterfall 40, Crunch 42, Aqua Tail 46, Muddy Water 51, Rock Tomb 54, Leech Life 56 | Huntail (from 16) |
| Clamperl | old rod | 16 | Rewrite | Clamp, Water Gun, Whirlpool, Iron Defense | as Gorebyss: Amnesia 19, Aqua Ring 24, Captivate 28, Baton Pass 33, Draining Kiss 35, Dive 37, Surf 40, Psychic 42, Aqua Tail 46, Muddy Water 51, Shadow Ball 54, Ice Beam 56 | Gorebyss (from 16) |
| Barboach | old rod | 17 | Oxide | Mud Sport, Water Sport, Water Gun, Mud Bomb | Amnesia 18, Water Pulse 22, Magnitude 26; as Whiscash: Rest 33, Snore 33, Aqua Tail 39, Earthquake 45, Future Sight 51 | Whiscash (from 30) |
| Barboach | old rod | 17 | Rewrite | Scary Face, Water Sport, Water Gun, Mud Bomb | Amnesia 18, Rock Tomb 20, Water Pulse 22, Magnitude 26; as Whiscash: Bulldoze 30, Rest 33, Zen Headbutt 36, Aqua Tail 39, Earth Power 40, Wild Charge 42, Earthquake 45, Future Sight 51, Spark 54, Ice Beam 56 | Whiscash (from 30) |
| Goldeen | old rod | 17 | Oxide | Water Sport, Supersonic, Horn Attack, Water Pulse | Flail 21, Aqua Ring 27, Fury Attack 31; as Seaking: Waterfall 40, Horn Drill 47, Agility 56 | Seaking (from 33) |
| Goldeen | old rod | 17 | Rewrite | Flip Turn, Water Pulse, Horn Attack, Swagger | Flail 21, Aqua Ring 27; as Seaking: Aqua Jet 34, Skull Bash 37, Waterfall 40, Poison Jab 44, Drill Run 47, Knock Off 50, Aqua Tail 54, Agility 56 | Seaking (from 33) |
| Frogadier | old rod | 18 | Oxide | Quick Attack, Lick, Water Pulse, Icy Wind | Faint Attack 20, Acrobatics 22, Low Kick 25, Waterfall 30, Fling 35; as Greninja: Scald 37, Dark Pulse 40, Extrasensory 43, Sludge Wave 47, Gunk Shot 51, Hydro Pump 55 | Greninja (from 36) |
| Frogadier | old rod | 18 | Rewrite | Quick Attack, Lick, Water Pulse, Icy Wind | Thief 19, Faint Attack 20, Acrobatics 22, Low Kick 25, Mud Shot 27, Waterfall 30, Fling 35; as Greninja: Shadow Sneak 36, Scald 37, Dark Pulse 40, Extrasensory 43, Sludge Wave 47, Gunk Shot 51, Ice Beam 54, Surf 56 | Greninja (from 36) |
| Barboach | good rod | 28 | Oxide | Mud Bomb, Amnesia, Water Pulse, Magnitude | as Whiscash: Rest 33, Snore 33, Aqua Tail 39, Earthquake 45, Future Sight 51 | Whiscash (from 30) |
| Barboach | good rod | 28 | Rewrite | Amnesia, Rock Tomb, Water Pulse, Magnitude | as Whiscash: Bulldoze 30, Rest 33, Zen Headbutt 36, Aqua Tail 39, Earth Power 40, Wild Charge 42, Earthquake 45, Future Sight 51, Spark 54, Ice Beam 56 | Whiscash (from 30) |
| Feebas | good rod | 28 | Oxide | Splash, Tackle | Flail 30; as Milotic: Hydro Pump 37, Attract 41, Safeguard 45, Aqua Ring 49 | Milotic (from 30) |
| Feebas | good rod | 28 | Rewrite | Tackle, Recover, Dragon Tail, Captivate | Flail 30; as Milotic: Twister 30, Recover 31, Aqua Tail 32, Aurora Beam 33, Dragon Pulse 35, Surf 37, Attract 41, Muddy Water 43, Safeguard 45, Aqua Ring 49, Alluring Voice 54, Scald 56 | Milotic (from 30) |
| Corphish | good rod | 30 | Oxide | Leer, BubbleBeam, Protect, Knock Off | as Crawdaunt: Taunt 34, Night Slash 39, Crabhammer 44, Swords Dance 52 | Crawdaunt (from 31) |
| Corphish | good rod | 30 | Rewrite | BubbleBeam, Leer, Razor Shell, Knock Off | as Crawdaunt: Taunt 32, Throat Chop 35, Aerial Ace 36, Night Slash 39, X-Scissor 41, Crabhammer 44, Brick Break 48, Swords Dance 52, Rock Tomb 54 | Crawdaunt (from 31) |
| Wailmer | good rod | 30 | Oxide | Astonish, Water Pulse, Mist, Rest | Brine 31, Water Spout 34, Amnesia 37; as Wailord: Dive 46, Bounce 54 | Wailord (from 40) |
| Wailmer | good rod | 30 | Rewrite | Water Pulse, Mist, Rest, Bulldoze | Brine 31, Water Spout 34, Amnesia 37; as Wailord: Dive 46, Iron Head 48, Rock Tomb 50, Bounce 54, Zen Headbutt 55, Ice Beam 56 | Wailord (from 40) |
| Lapras | good rod | 32 | Oxide | Water Pulse, Body Slam, Perish Song, Ice Beam | Brine 37, Safeguard 43, Hydro Pump 49, Sheer Cold 55 | Lapras |
| Lapras | good rod | 32 | Rewrite | Water Pulse, Body Slam, Perish Song, Ice Beam | Brine 37, Safeguard 43, Muddy Water 49, Life Dew 54, Drill Run 56 | Lapras |
| Floatzel | surf | 34 | Oxide | Swift, Aqua Jet, Crunch, Agility | Whirlpool 39, Razor Wind 50 | Floatzel |
| Floatzel | surf | 34 | Rewrite | Aqua Jet, Crunch, Icy Wind, Flip Turn | Waterfall 36, Whirlpool 39, Liquidation 41, Low Sweep 44, Agility 51, Rock Tomb 53, Ice Fang 56 | Floatzel |
| Jellicent | surf | 34 | Oxide | Imprison, Confuse Ray, Hex, Brine | Pain Split 39, Destiny Bond 45, Shadow Ball 51, Scald 55 | Jellicent |
| Jellicent | surf | 34 | Rewrite | Imprison, Confuse Ray, Hex, Brine | Pain Split 39, Muddy Water 45, Shadow Ball 51, Sludge Bomb 54, Scald 55 | Jellicent |
| Buizel | surf | 37 | Oxide | Swift, Aqua Jet, Agility, Whirlpool | as Floatzel: Whirlpool 39, Razor Wind 50 | Floatzel (from 38) |
| Buizel | surf | 37 | Rewrite | Pursuit, Scary Face, Swift, Aqua Jet | as Floatzel: Whirlpool 39, Liquidation 41, Low Sweep 44, Agility 51, Rock Tomb 53, Ice Fang 56 | Floatzel (from 38) |
| Dewgong | surf | 37 | Oxide | Aqua Jet, Brine, Sheer Cold, Take Down | Dive 41, Aqua Tail 43, Ice Beam 47, Safeguard 51 | Dewgong |
| Dewgong | surf | 37 | Rewrite | Aqua Jet, Brine, Signal Beam, Take Down | Drill Run 40, Dive 41, Aqua Tail 43, Ice Beam 47, Safeguard 51, Muddy Water 54, Bite 56 | Dewgong |
| Crawdaunt | super rod | 38 | Oxide | Protect, Knock Off, Swift, Taunt | Night Slash 39, Crabhammer 44, Swords Dance 52 | Crawdaunt |
| Crawdaunt | super rod | 38 | Rewrite | Swift, Taunt, Throat Chop, Aerial Ace | Night Slash 39, X-Scissor 41, Crabhammer 44, Brick Break 48, Swords Dance 52, Rock Tomb 54 | Crawdaunt |
| Milotic | super rod | 38 | Oxide | Recover, Captivate, Aqua Tail, Hydro Pump | Attract 41, Safeguard 45, Aqua Ring 49 | Milotic |
| Milotic | super rod | 38 | Rewrite | Aqua Tail, Aurora Beam, Dragon Pulse, Surf | Attract 41, Muddy Water 43, Safeguard 45, Aqua Ring 49, Alluring Voice 54, Scald 56 | Milotic |
| Snorunt | wild | 38 to 41 | Oxide | Protect, Ice Fang, Crunch, Ice Shard | as Glalie: Blizzard 51 | Glalie (from 42) |
| Snorunt | wild | 38 to 41 | Oxide | Protect, Ice Fang, Crunch, Ice Shard | as Froslass: Blizzard 51 | Froslass (from 38) |
| Snorunt | wild | 38 to 41 | Rewrite | Ice Fang, Crunch, Draining Kiss, Ice Shard | as Glalie: Rock Slide 42, Power Gem 44, Confuse Ray 48, Earth Power 53, Ice Punch 54, Shadow Ball 56 | Glalie (from 42) |
| Snorunt | wild | 38 to 41 | Rewrite | Ice Fang, Crunch, Draining Kiss, Ice Shard | as Froslass: Ice Beam 51 | Froslass (from 38) |
| Absol | wild | 39 to 40 | Oxide | Swords Dance, Bite, Double Team, Slash | Future Sight 41, Sucker Punch 44, Detect 49, Night Slash 52 | Absol |
| Absol | wild | 39 to 40 | Rewrite | Pursuit, Swords Dance, Bite, Slash | Future Sight 41, Sucker Punch 44, X-Scissor 48, Night Slash 52, Shadow Ball 54, Throat Chop 56 | Absol |
| Alolan Ninetales | wild | 39 | Oxide | Tail Whip, Disable, Ice Shard, Safeguard | nothing | Alolan Ninetales |
| Alolan Ninetales | wild | 39 | Rewrite | Payback, Icy Wind, Chilling Water, Dazzling Gleam | Extrasensory 43, Ice Beam 44, Dark Pulse 48, Mystical Fire 53, BurningJealousy 54, Moonblast 56 | Alolan Ninetales |
| Frosmoth | wild | 39 | Oxide | FeatherDance, Aurora Beam, Bug Buzz, Aurora Veil | Blizzard 40, Tailwind 44, Wide Guard 48, Quiver Dance 52 | Frosmoth |
| Frosmoth | wild | 39 | Rewrite | Bug Buzz, Defog, Aurora Beam, Aurora Veil | Ice Beam 40, Tailwind 44, Wide Guard 48, Quiver Dance 52, Air Slash 54, Giga Drain 56 | Frosmoth |
| Jynx | wild | 39 | Oxide | Fake Tears, Wake-Up Slap, Avalanche, Body Slam | Wring Out 44, Perish Song 49, Blizzard 55 | Jynx |
| Jynx | wild | 39 | Rewrite | Ice Punch, Wake-Up Slap, Avalanche, Body Slam | Aurora Beam 41, Psychic 44, Perish Song 49, Shadow Ball 52, Energy Ball 54, Ice Beam 55 | Jynx |
| Weavile | wild | 39 to 41 | Oxide | Nasty Plot, Icy Wind, Night Slash, Fling | Metal Claw 42, Dark Pulse 49 | Weavile |
| Weavile | wild | 39 to 41 | Rewrite | Fury Swipes, Icy Wind, Night Slash, Fling | Metal Claw 42, Dark Pulse 49 | Weavile |
| Abomasnow | wild | 40 to 41 | Oxide | Mist, Ice Shard, Ingrain, Wood Hammer | Blizzard 47 | Abomasnow |
| Abomasnow | wild | 40 to 41 | Rewrite | Swagger, Mist, Ice Shard, Wood Hammer | Ice Beam 41, Giga Drain 50, Ice Punch 53, Rock Climb 54, Shadow Ball 56 | Abomasnow |
| Galarian Mr Mime | wild | 40 | Oxide | Psybeam, Hypnosis, Mirror Coat, Sucker Punch | as Mr. Rime: Freeze-Dry 44, Psychic 48, Teeter Dance 52 | Mr. Rime (from 42) |
| Galarian Mr Mime | wild | 40 | Rewrite | Psybeam, Hypnosis, Mirror Coat, Sucker Punch | Dazzling Gleam 42; as Mr. Rime: Freeze-Dry 44, Psychic 48, Teeter Dance 52, Ice Beam 54, Encore 56 | Mr. Rime (from 42) |
| Lapras | surf | 40 | Oxide | Body Slam, Perish Song, Ice Beam, Brine | Safeguard 43, Hydro Pump 49, Sheer Cold 55 | Lapras |
| Lapras | surf | 40 | Rewrite | Body Slam, Perish Song, Ice Beam, Brine | Safeguard 43, Muddy Water 49, Life Dew 54, Drill Run 56 | Lapras |
| Lanturn | super rod | 41 | Oxide | Spit Up, BubbleBeam, Signal Beam, Discharge | Aqua Ring 47, Hydro Pump 52 | Lanturn |
| Lanturn | super rod | 41 | Rewrite | Scald, Surf, Thunderbolt, Discharge | Flash Cannon 43, Aqua Ring 47, Muddy Water 52, Volt Switch 54, Dazzling Gleam 55 | Lanturn |
| Qwilfish | super rod | 41 | Oxide | Revenge, Brine, Pin Missile, Take Down | Aqua Tail 45, Poison Jab 49, Destiny Bond 53 | Qwilfish |
| Qwilfish | super rod | 41 | Rewrite | Revenge, Brine, Pin Missile, Take Down | Throat Chop 43, Aqua Tail 45, Poison Jab 49, Flip Turn 54, Headbutt 55 | Qwilfish |
| Gorebyss | super rod | 44 | Oxide | Captivate, Baton Pass, Dive, Psychic | Aqua Tail 46, Hydro Pump 51 | Gorebyss |
| Gorebyss | super rod | 44 | Rewrite | Draining Kiss, Dive, Surf, Psychic | Aqua Tail 46, Muddy Water 51, Shadow Ball 54, Ice Beam 56 | Gorebyss |

## Lake Valor

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 56 | At the cap |
|---|---|---|---|---|---|---|
| Milotic | super rod | 36 | Oxide | Twister, Recover, Captivate, Aqua Tail | Hydro Pump 37, Attract 41, Safeguard 45, Aqua Ring 49 | Milotic |
| Milotic | super rod | 36 | Rewrite | Recover, Aqua Tail, Aurora Beam, Dragon Pulse | Surf 37, Attract 41, Muddy Water 43, Safeguard 45, Aqua Ring 49, Alluring Voice 54, Scald 56 | Milotic |
| Whiscash | super rod | 36 | Oxide | Water Pulse, Magnitude, Rest, Snore | Aqua Tail 39, Earthquake 45, Future Sight 51 | Whiscash |
| Whiscash | super rod | 36 | Rewrite | Magnitude, Bulldoze, Rest, Zen Headbutt | Aqua Tail 39, Earth Power 40, Wild Charge 42, Earthquake 45, Future Sight 51, Spark 54, Ice Beam 56 | Whiscash |
| Crawdaunt | super rod | 39 | Oxide | Knock Off, Swift, Taunt, Night Slash | Crabhammer 44, Swords Dance 52 | Crawdaunt |
| Crawdaunt | super rod | 39 | Rewrite | Taunt, Throat Chop, Aerial Ace, Night Slash | X-Scissor 41, Crabhammer 44, Brick Break 48, Swords Dance 52, Rock Tomb 54 | Crawdaunt |
| Lanturn | super rod | 39 | Oxide | Swallow, Spit Up, BubbleBeam, Signal Beam | Discharge 40, Aqua Ring 47, Hydro Pump 52 | Lanturn |
| Lanturn | super rod | 39 | Rewrite | Signal Beam, Scald, Surf, Thunderbolt | Discharge 40, Flash Cannon 43, Aqua Ring 47, Muddy Water 52, Volt Switch 54, Dazzling Gleam 55 | Lanturn |
| Corsola | super rod | 42 | Oxide | Lucky Chant, AncientPower, Aqua Ring, Spike Cannon | Power Gem 44, Mirror Coat 48, Earth Power 53 | Corsola |
| Corsola | super rod | 42 | Rewrite | Liquidation, Aqua Ring, Spike Cannon, Throat Chop | Power Gem 44, Mirror Coat 48, Earth Power 53, Rock Slide 54, Rock Tomb 56 | Corsola |

## Lake Verity

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 56 | At the cap |
|---|---|---|---|---|---|---|
| Lanturn | super rod | 30 | Oxide | Stockpile, Swallow, Spit Up, BubbleBeam | Signal Beam 35, Discharge 40, Aqua Ring 47, Hydro Pump 52 | Lanturn |
| Lanturn | super rod | 30 | Rewrite | Stockpile, Swallow, Spit Up, BubbleBeam | Signal Beam 31, Scald 33, Surf 34, Thunderbolt 37, Discharge 40, Flash Cannon 43, Aqua Ring 47, Muddy Water 52, Volt Switch 54, Dazzling Gleam 55 | Lanturn |
| Sharpedo | super rod | 30 | Oxide | Swagger, Assurance, Crunch, Slash | Aqua Jet 34, Taunt 40, Agility 45, Skull Bash 50, Night Slash 56 | Sharpedo |
| Sharpedo | super rod | 30 | Rewrite | Swagger, Assurance, Crunch, Slash | Aqua Jet 31, Bug Bite 35, Aerial Ace 37, Taunt 40, Liquidation 41, Agility 45, Skull Bash 50, Poison Fang 54, Night Slash 56 | Sharpedo |
| Floatzel | super rod | 33 | Oxide | Swift, Aqua Jet, Crunch, Agility | Whirlpool 39, Razor Wind 50 | Floatzel |
| Floatzel | super rod | 33 | Rewrite | Aqua Jet, Crunch, Icy Wind, Flip Turn | Waterfall 36, Whirlpool 39, Liquidation 41, Low Sweep 44, Agility 51, Rock Tomb 53, Ice Fang 56 | Floatzel |
| Kingler | super rod | 33 | Oxide | Mud Shot, Metal Claw, Stomp, Protect | Guillotine 37, Slam 44, Brine 51, Crabhammer 56 | Kingler |
| Kingler | super rod | 33 | Rewrite | BubbleBeam, Mud Shot, Metal Claw, Stomp | Waterfall 34, Razor Shell 36, Rock Tomb 39, X-Scissor 41, Slam 44, Night Slash 47, Brine 51, Liquidation 54, Crabhammer 56 | Kingler |
| Greninja | super rod | 36 | Oxide | Acrobatics, Low Kick, Waterfall, Fling | Scald 37, Dark Pulse 40, Extrasensory 43, Sludge Wave 47, Gunk Shot 51, Hydro Pump 55 | Greninja |
| Greninja | super rod | 36 | Rewrite | Low Kick, Waterfall, Fling, Shadow Sneak | Scald 37, Dark Pulse 40, Extrasensory 43, Sludge Wave 47, Gunk Shot 51, Ice Beam 54, Surf 56 | Greninja |

## Mt. Coronet B1F

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 56 | At the cap |
|---|---|---|---|---|---|---|
| Feebas | old rod | 18 | Oxide | Splash, Tackle | Flail 30; as Milotic: Hydro Pump 37, Attract 41, Safeguard 45, Aqua Ring 49 | Milotic (from 30) |
| Feebas | old rod | 18 | Rewrite | Whirlpool, Water Gun, Water Pulse, Tackle | Recover 21, Dragon Tail 24, Captivate 25, Flail 30; as Milotic: Twister 30, Recover 31, Aqua Tail 32, Aurora Beam 33, Dragon Pulse 35, Surf 37, Attract 41, Muddy Water 43, Safeguard 45, Aqua Ring 49, Alluring Voice 54, Scald 56 | Milotic (from 30) |
| Horsea | old rod | 18 | Oxide | Leer, Water Gun, Focus Energy, BubbleBeam | Agility 23, Twister 26, Brine 30; as Kingdra: Hydro Pump 40, Dragon Dance 48 | Kingdra (from 32) |
| Horsea | old rod | 18 | Rewrite | SmokeScreen, Water Gun, Focus Energy, BubbleBeam | Agility 23, Twister 26, Brine 30; as Kingdra: Octazooka 40, Aurora Beam 44, Scald 54 | Kingdra (from 32) |
| Croconaw | old rod | 19 | Oxide | Water Gun, Rage, Bite, Scary Face | Ice Fang 21, Flail 24, Crunch 30; as Feraligatr: Agility 30, Crunch 32, Slash 37, Screech 45, Thrash 50 | Feraligatr (from 30) |
| Croconaw | old rod | 19 | Rewrite | Leer, Water Gun, Bite, Scary Face | Ice Fang 21, Flail 24; as Feraligatr: Agility 30, Crunch 32, Slash 33, Bulldoze 35, Metal Claw 39, Aqua Jet 40, Liquidation 42, Screech 45 | Feraligatr (from 30) |
| Goldeen | old rod | 19 | Oxide | Water Sport, Supersonic, Horn Attack, Water Pulse | Flail 21, Aqua Ring 27, Fury Attack 31; as Seaking: Waterfall 40, Horn Drill 47, Agility 56 | Seaking (from 33) |
| Goldeen | old rod | 19 | Rewrite | Flip Turn, Water Pulse, Horn Attack, Swagger | Flail 21, Aqua Ring 27; as Seaking: Aqua Jet 34, Skull Bash 37, Waterfall 40, Poison Jab 44, Drill Run 47, Knock Off 50, Aqua Tail 54, Agility 56 | Seaking (from 33) |
| Seel | old rod | 20 | Oxide | Water Sport, Icy Wind, Encore, Ice Shard | Rest 21, Aqua Ring 23, Aurora Beam 27, Aqua Jet 31, Brine 33; as Dewgong: Sheer Cold 34, Take Down 37, Dive 41, Aqua Tail 43, Ice Beam 47, Safeguard 51 | Dewgong (from 34) |
| Seel | old rod | 20 | Rewrite | Water Sport, Icy Wind, Encore, Ice Shard | Rest 21, Aqua Ring 23, Aurora Beam 27, Aqua Jet 31, Brine 33; as Dewgong: Signal Beam 34, Take Down 37, Drill Run 40, Dive 41, Aqua Tail 43, Ice Beam 47, Safeguard 51, Muddy Water 54, Bite 56 | Dewgong (from 34) |
| Corphish | good rod | 30 | Oxide | Leer, BubbleBeam, Protect, Knock Off | as Crawdaunt: Taunt 34, Night Slash 39, Crabhammer 44, Swords Dance 52 | Crawdaunt (from 31) |
| Corphish | good rod | 30 | Rewrite | BubbleBeam, Leer, Razor Shell, Knock Off | as Crawdaunt: Taunt 32, Throat Chop 35, Aerial Ace 36, Night Slash 39, X-Scissor 41, Crabhammer 44, Brick Break 48, Swords Dance 52, Rock Tomb 54 | Crawdaunt (from 31) |
| Feebas | good rod | 30 | Oxide | Splash, Tackle, Flail | as Milotic: Hydro Pump 37, Attract 41, Safeguard 45, Aqua Ring 49 | Milotic (from 31) |
| Feebas | good rod | 30 | Rewrite | Recover, Dragon Tail, Captivate, Flail | as Milotic: Recover 31, Aqua Tail 32, Aurora Beam 33, Dragon Pulse 35, Surf 37, Attract 41, Muddy Water 43, Safeguard 45, Aqua Ring 49, Alluring Voice 54, Scald 56 | Milotic (from 31) |
| Chinchou | good rod | 32 | Oxide | Spark, Take Down, BubbleBeam, Signal Beam | as Lanturn: Signal Beam 35, Discharge 40, Aqua Ring 47, Hydro Pump 52 | Lanturn (from 33) |
| Chinchou | good rod | 32 | Rewrite | Spark, Take Down, Icy Wind, Signal Beam | as Lanturn: Scald 33, Surf 34, Thunderbolt 37, Discharge 40, Flash Cannon 43, Aqua Ring 47, Muddy Water 52, Volt Switch 54, Dazzling Gleam 55 | Lanturn (from 33) |
| Frillish | good rod | 32 | Oxide | Water Pulse, Imprison, Confuse Ray, Hex | Brine 34, Pain Split 39; as Jellicent: Destiny Bond 45, Shadow Ball 51, Scald 55 | Jellicent (from 40) |
| Frillish | good rod | 32 | Rewrite | Water Pulse, Imprison, Confuse Ray, Hex | Brine 34, Dark Pulse 36, Pain Split 39; as Jellicent: Muddy Water 45, Shadow Ball 51, Sludge Bomb 54, Scald 55 | Jellicent (from 40) |
| Goomy | wild | 32 | Oxide | Life Dew, Flail, Water Pulse, Dragon Tail | Infestation 34; as Sliggoo: Body Slam 42, Muddy Water 48; as Goodra: Aqua Tail 55 | Goodra (from 50) |
| Goomy | wild | 32 | Oxide | Life Dew, Flail, Water Pulse, Dragon Tail | as Hisuian Sliggoo: Dragon Pulse 35, Curse 43, Iron Head 49; as Hisuian Goodra: Iron Tail 55 | Hisuian Goodra (from 50) |
| Goomy | wild | 32 | Rewrite | Life Dew, Flail, Water Pulse, Dragon Tail | Infestation 34; as Sliggoo: Body Slam 42, Muddy Water 48; as Goodra: Iron Head 54, Aqua Tail 55 | Goodra (from 50) |
| Goomy | wild | 32 | Rewrite | Life Dew, Flail, Water Pulse, Dragon Tail | as Hisuian Sliggoo: Dragon Pulse 35, Flash Cannon 42, Curse 43, Iron Head 49; as Hisuian Goodra: Smart Strike 50, Sludge Bomb 54, Iron Head 55, Body Slam 56 | Hisuian Goodra (from 50) |
| Bronzong | wild | 33 | Oxide | Extrasensory, Iron Defense, Safeguard, Block | Gyro Ball 38, Future Sight 43, Faint Attack 50 | Bronzong |
| Bronzong | wild | 33 | Rewrite | Extrasensory, Iron Defense, Safeguard, Block | Iron Head 35, Gyro Ball 38, Rock Tomb 40, Future Sight 43, Body Press 46, Faint Attack 50, Shadow Ball 54 | Bronzong |
| Carbink | wild | 33 to 34 | Oxide | Reflect, Flail, AncientPower, Rock Polish | Rock Slide 35, Stealth Rock 36, Skill Swap 40, Light Screen 44, Power Gem 45, Moonblast 52, Stone Edge 54 | Carbink |
| Carbink | wild | 33 to 34 | Rewrite | AncientPower, Rock Polish, Dazzling Gleam, Rock Tomb | Rock Slide 35, Stealth Rock 36, Skill Swap 40, Light Screen 44, Power Gem 45, Moonblast 52, Iron Head 54, Psychic 56 | Carbink |
| Donphan | wild | 33 | Oxide | Magnitude, Slam, Fury Attack, Assurance | Scary Face 39, Earthquake 46, Giga Impact 54 | Donphan |
| Donphan | wild | 33 | Rewrite | Rapid Spin, Magnitude, Rock Tomb, Assurance | Trailblaze 35, Scary Face 39, Iron Head 42, Throat Chop 44, Earthquake 46, Seed Bomb 50, Giga Impact 54, Charm 56 | Donphan |
| Golbat | wild | 33 to 35 | Oxide | Wing Attack, Confuse Ray, Air Cutter, Mean Look | Poison Fang 39; as Crobat: Haze 45, Air Slash 51 | Crobat (from 40) |
| Golbat | wild | 33 to 35 | Rewrite | Confuse Ray, Air Cutter, Poison Jab, Mean Look | Steel Wing 36, Poison Fang 39; as Crobat: Zen Headbutt 45, Air Slash 51, U-turn 54, Crunch 56 | Crobat (from 40) |
| Hariyama | wild | 33 | Oxide | Knock Off, SmellingSalt, Belly Drum, Force Palm | Seismic Toss 37, Wake-Up Slap 42, Endure 47, Close Combat 52 | Hariyama |
| Hariyama | wild | 33 | Rewrite | SmellingSalt, Belly Drum, Low Sweep, Force Palm | Bulldoze 34, Seismic Toss 37, Rock Tomb 39, Wake-Up Slap 42, Drain Punch 44, Endure 47, Close Combat 52, Upper Hand 54, Throat Chop 55 | Hariyama |
| Mienfoo | wild | 33 | Oxide | Force Palm, Bounce, Drain Punch, Vacuum Wave | as Mienshao: Aura Sphere 38, Me First 40, Jump Kick 45, Dual Chop 48, Focus Blast 51, Acrobatics 55 | Mienshao (from 36) |
| Mienfoo | wild | 33 | Rewrite | Bounce, Drain Punch, Low Sweep, Vacuum Wave | as Mienshao: Aura Sphere 38, U-turn 41, Rock Tomb 43, Jump Kick 45, Dual Chop 48, Poison Jab 51, Upper Hand 54, Acrobatics 55, Hammer Arm 56 | Mienshao (from 36) |
| Naclstack | wild | 33 | Oxide | Rock Polish, Headbutt, Iron Defense, Recover | Rock Slide 34, Stealth Rock 38; as Garganacl: Stealth Rock 40, Heavy Slam 44, Earthquake 49, Stone Edge 54 | Garganacl (from 38) |
| Naclstack | wild | 33 | Rewrite | Bulldoze, Recover, Rock Polish, Rock Tomb | Rock Slide 34, Stealth Rock 38; as Garganacl: Rock Tomb 38, Salt Cure 39, Stealth Rock 40, Iron Head 42, Heavy Slam 44, Earthquake 49, Zen Headbutt 53, Block 54, Body Press 56 | Garganacl (from 38) |
| Dewgong | good rod | 34 | Oxide | Aurora Beam, Aqua Jet, Brine, Sheer Cold | Take Down 37, Dive 41, Aqua Tail 43, Ice Beam 47, Safeguard 51 | Dewgong |
| Dewgong | good rod | 34 | Rewrite | Aurora Beam, Aqua Jet, Brine, Signal Beam | Take Down 37, Drill Run 40, Dive 41, Aqua Tail 43, Ice Beam 47, Safeguard 51, Muddy Water 54, Bite 56 | Dewgong |
| Glimmet | wild | 34 | Oxide | Stealth Rock, Venoshock, Selfdestruct, Rock Slide | as Glimmora: Power Gem 39, Acid Armor 44, Sludge Wave 50 | Glimmora (from 35) |
| Glimmet | wild | 34 | Rewrite | Venoshock, Mud Shot, Toxic Spikes, Rock Slide | as Glimmora: Power Gem 39, Sludge Bomb 41, Acid Armor 44, Flash Cannon 47, Sludge Wave 50, Energy Ball 54, Dazzling Gleam 56 | Glimmora (from 35) |
| Graveler | wild | 34 | Oxide | Selfdestruct, Rollout, Rock Blast, Earthquake | Explosion 38; as Golem: Double-Edge 44, Stone Edge 49 | Golem (from 40) |
| Graveler | wild | 34 | Rewrite | Karate Chop, Rock Blast, Rock Tomb, Earthquake | Sucker Punch 36, Iron Head 39; as Golem: Double-Edge 44, Rock Slide 49, Body Press 53, Body Slam 56 | Golem (from 40) |
| Probopass | wild | 34 | Oxide | Magnet Bomb, Block, Thunder Wave, Rock Slide | Rest 43, Power Gem 49, Discharge 55 | Probopass |
| Probopass | wild | 34 | Rewrite | Magnet Bomb, Block, Thunder Wave, Rock Slide | Iron Head 35, Spark 39, Body Press 41, Rest 43, Dazzling Gleam 46, Power Gem 49, Thunderbolt 54, Discharge 55 | Probopass |
| Meditite | wild | 35 | Oxide | Feint, Calm Mind, Force Palm, Hi Jump Kick | Psych Up 36; as Medicham: Power Trick 42, Reversal 49, Recover 55 | Medicham (from 37) |
| Meditite | wild | 35 | Rewrite | Swagger, Rock Throw, Low Sweep, Hi Jump Kick | Psych Up 36; as Medicham: Power Trick 39, Poison Jab 40, Iron Head 44, Reversal 49, Zen Headbutt 52, Drain Punch 54, Recover 55 | Medicham (from 37) |
| Sandygast | wild | 35 | Oxide | Mega Drain, Bulldoze, Hypnosis, Giga Drain | Iron Defense 36; as Palossand: Shadow Ball 44, Earth Power 50 | Palossand (from 42) |
| Sandygast | wild | 35 | Rewrite | Mega Drain, Bulldoze, Hypnosis, Giga Drain | Iron Defense 36; as Palossand: Shadow Ball 44, Sludge Bomb 47, Earth Power 50, Psychic 54, Flash Cannon 55 | Palossand (from 42) |
| Buizel | surf | 36 | Oxide | Swift, Aqua Jet, Agility, Whirlpool | as Floatzel: Whirlpool 39, Razor Wind 50 | Floatzel (from 37) |
| Buizel | surf | 36 | Rewrite | Pursuit, Scary Face, Swift, Aqua Jet | as Floatzel: Whirlpool 39, Liquidation 41, Low Sweep 44, Agility 51, Rock Tomb 53, Ice Fang 56 | Floatzel (from 37) |
| Floatzel | surf | 36 | Oxide | Swift, Aqua Jet, Crunch, Agility | Whirlpool 39, Razor Wind 50 | Floatzel |
| Floatzel | surf | 36 | Rewrite | Crunch, Icy Wind, Flip Turn, Waterfall | Whirlpool 39, Liquidation 41, Low Sweep 44, Agility 51, Rock Tomb 53, Ice Fang 56 | Floatzel |
| Feebas | surf | 39 | Oxide | Splash, Tackle, Flail | as Milotic: Attract 41, Safeguard 45, Aqua Ring 49 | Milotic (from 40) |
| Feebas | surf | 39 | Rewrite | Recover, Dragon Tail, Captivate, Flail | as Milotic: Attract 41, Muddy Water 43, Safeguard 45, Aqua Ring 49, Alluring Voice 54, Scald 56 | Milotic (from 40) |
| Frillish | surf | 39 | Oxide | Confuse Ray, Hex, Brine, Pain Split | as Jellicent: Destiny Bond 45, Shadow Ball 51, Scald 55 | Jellicent (from 40) |
| Frillish | surf | 39 | Rewrite | Hex, Brine, Dark Pulse, Pain Split | as Jellicent: Muddy Water 45, Shadow Ball 51, Sludge Bomb 54, Scald 55 | Jellicent (from 40) |
| Crawdaunt | super rod | 40 | Oxide | Knock Off, Swift, Taunt, Night Slash | Crabhammer 44, Swords Dance 52 | Crawdaunt |
| Crawdaunt | super rod | 40 | Rewrite | Taunt, Throat Chop, Aerial Ace, Night Slash | X-Scissor 41, Crabhammer 44, Brick Break 48, Swords Dance 52, Rock Tomb 54 | Crawdaunt |
| Milotic | super rod | 40 | Oxide | Recover, Captivate, Aqua Tail, Hydro Pump | Attract 41, Safeguard 45, Aqua Ring 49 | Milotic |
| Milotic | super rod | 40 | Rewrite | Aqua Tail, Aurora Beam, Dragon Pulse, Surf | Attract 41, Muddy Water 43, Safeguard 45, Aqua Ring 49, Alluring Voice 54, Scald 56 | Milotic |
| Kingdra | surf | 42 | Oxide | Agility, Twister, Brine, Hydro Pump | Dragon Dance 48 | Kingdra |
| Kingdra | surf | 42 | Rewrite | Agility, Twister, Brine, Octazooka | Aurora Beam 44, Scald 54 | Kingdra |
| Lanturn | super rod | 43 | Oxide | Spit Up, BubbleBeam, Signal Beam, Discharge | Aqua Ring 47, Hydro Pump 52 | Lanturn |
| Lanturn | super rod | 43 | Rewrite | Surf, Thunderbolt, Discharge, Flash Cannon | Aqua Ring 47, Muddy Water 52, Volt Switch 54, Dazzling Gleam 55 | Lanturn |
| Wailord | super rod | 43 | Oxide | Rest, Brine, Water Spout, Amnesia | Dive 46, Bounce 54 | Wailord |
| Wailord | super rod | 43 | Rewrite | Rest, Brine, Water Spout, Amnesia | Dive 46, Iron Head 48, Rock Tomb 50, Bounce 54, Zen Headbutt 55, Ice Beam 56 | Wailord |
| Pelipper | super rod | 46 | Oxide | Stockpile, Swallow, Spit Up, Fling | Tailwind 50 | Pelipper |
| Pelipper | super rod | 46 | Rewrite | Stockpile, Spit Up, Icy Wind, Fling | Air Slash 47, Tailwind 50, Brave Bird 53, Ice Beam 54, U-turn 55 | Pelipper |

## Mt. Coronet South

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 56 | At the cap |
|---|---|---|---|---|---|---|
| Milotic | super rod | 32 | Oxide | Twister, Recover, Captivate, Aqua Tail | Hydro Pump 37, Attract 41, Safeguard 45, Aqua Ring 49 | Milotic |
| Milotic | super rod | 32 | Rewrite | Water Gun, Twister, Recover, Aqua Tail | Aurora Beam 33, Dragon Pulse 35, Surf 37, Attract 41, Muddy Water 43, Safeguard 45, Aqua Ring 49, Alluring Voice 54, Scald 56 | Milotic |
| Whiscash | super rod | 32 | Oxide | Mud Bomb, Amnesia, Water Pulse, Magnitude | Rest 33, Snore 33, Aqua Tail 39, Earthquake 45, Future Sight 51 | Whiscash |
| Whiscash | super rod | 32 | Rewrite | Amnesia, Water Pulse, Magnitude, Bulldoze | Rest 33, Zen Headbutt 36, Aqua Tail 39, Earth Power 40, Wild Charge 42, Earthquake 45, Future Sight 51, Spark 54, Ice Beam 56 | Whiscash |
| Crawdaunt | super rod | 35 | Oxide | Protect, Knock Off, Swift, Taunt | Night Slash 39, Crabhammer 44, Swords Dance 52 | Crawdaunt |
| Crawdaunt | super rod | 35 | Rewrite | Knock Off, Swift, Taunt, Throat Chop | Aerial Ace 36, Night Slash 39, X-Scissor 41, Crabhammer 44, Brick Break 48, Swords Dance 52, Rock Tomb 54 | Crawdaunt |
| Lanturn | super rod | 35 | Oxide | Swallow, Spit Up, BubbleBeam, Signal Beam | Discharge 40, Aqua Ring 47, Hydro Pump 52 | Lanturn |
| Lanturn | super rod | 35 | Rewrite | BubbleBeam, Signal Beam, Scald, Surf | Thunderbolt 37, Discharge 40, Flash Cannon 43, Aqua Ring 47, Muddy Water 52, Volt Switch 54, Dazzling Gleam 55 | Lanturn |
| Greninja | super rod | 38 | Oxide | Low Kick, Waterfall, Fling, Scald | Dark Pulse 40, Extrasensory 43, Sludge Wave 47, Gunk Shot 51, Hydro Pump 55 | Greninja |
| Greninja | super rod | 38 | Rewrite | Waterfall, Fling, Shadow Sneak, Scald | Dark Pulse 40, Extrasensory 43, Sludge Wave 47, Gunk Shot 51, Ice Beam 54, Surf 56 | Greninja |

## Oreburgh Gate

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 56 | At the cap |
|---|---|---|---|---|---|---|
| Corsola | super rod | 30 | Oxide | Refresh, Rock Blast, BubbleBeam, Lucky Chant | AncientPower 32, Aqua Ring 37, Spike Cannon 40, Power Gem 44, Mirror Coat 48, Earth Power 53 | Corsola |
| Corsola | super rod | 30 | Rewrite | Bulldoze, Rock Blast, BubbleBeam, Lucky Chant | Aqua Cutter 33, Liquidation 35, Aqua Ring 37, Spike Cannon 40, Throat Chop 42, Power Gem 44, Mirror Coat 48, Earth Power 53, Rock Slide 54, Rock Tomb 56 | Corsola |
| Jellicent | super rod | 30 | Oxide | Water Pulse, Imprison, Confuse Ray, Hex | Brine 34, Pain Split 39, Destiny Bond 45, Shadow Ball 51, Scald 55 | Jellicent |
| Jellicent | super rod | 30 | Rewrite | Water Pulse, Imprison, Confuse Ray, Hex | Brine 34, Pain Split 39, Muddy Water 45, Shadow Ball 51, Sludge Bomb 54, Scald 55 | Jellicent |
| Seaking | super rod | 33 | Oxide | Water Pulse, Flail, Aqua Ring, Fury Attack | Waterfall 40, Horn Drill 47, Agility 56 | Seaking |
| Seaking | super rod | 33 | Rewrite | Horn Attack, Water Pulse, Flail, Aqua Ring | Aqua Jet 34, Skull Bash 37, Waterfall 40, Poison Jab 44, Drill Run 47, Knock Off 50, Aqua Tail 54, Agility 56 | Seaking |
| Whiscash | super rod | 33 | Oxide | Water Pulse, Magnitude, Rest, Snore | Aqua Tail 39, Earthquake 45, Future Sight 51 | Whiscash |
| Whiscash | super rod | 33 | Rewrite | Water Pulse, Magnitude, Bulldoze, Rest | Zen Headbutt 36, Aqua Tail 39, Earth Power 40, Wild Charge 42, Earthquake 45, Future Sight 51, Spark 54, Ice Beam 56 | Whiscash |
| Wailmer | super rod | 36 | Oxide | Mist, Rest, Brine, Water Spout | Amnesia 37; as Wailord: Dive 46, Bounce 54 | Wailord (from 40) |
| Wailmer | super rod | 36 | Rewrite | Rest, Bulldoze, Brine, Water Spout | Amnesia 37; as Wailord: Dive 46, Iron Head 48, Rock Tomb 50, Bounce 54, Zen Headbutt 55, Ice Beam 56 | Wailord (from 40) |

## Pastoria City

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 56 | At the cap |
|---|---|---|---|---|---|---|
| Quagsire | super rod | 35 | Oxide | Slam, Mud Bomb, Amnesia, Yawn | Earthquake 36, Mist 48, Haze 48, Muddy Water 53 | Quagsire |
| Quagsire | super rod | 35 | Rewrite | Mud Bomb, Amnesia, Trailblaze, Yawn | Earthquake 36, Rock Slide 39, Toxic 40, Drain Punch 44, Mist 48, Muddy Water 53, Poison Jab 54, Aqua Tail 56 | Quagsire |
| Sharpedo | super rod | 35 | Oxide | Assurance, Crunch, Slash, Aqua Jet | Taunt 40, Agility 45, Skull Bash 50, Night Slash 56 | Sharpedo |
| Sharpedo | super rod | 35 | Rewrite | Crunch, Slash, Aqua Jet, Bug Bite | Aerial Ace 37, Taunt 40, Liquidation 41, Agility 45, Skull Bash 50, Poison Fang 54, Night Slash 56 | Sharpedo |
| Lombre | super rod | 38 | Oxide | Water Sport, BubbleBeam, Zen Headbutt, Uproar | nothing | Ludicolo (from 38) |
| Lombre | super rod | 38 | Rewrite | Giga Drain, Zen Headbutt, Energy Ball, Uproar | as Ludicolo: Ice Beam 54, Muddy Water 56 | Ludicolo (from 38) |
| Ludicolo | super rod | 38 | Oxide | Astonish, Growl, Mega Drain, Nature Power | nothing | Ludicolo |
| Ludicolo | super rod | 38 | Rewrite | Growl, Mega Drain, Nature Power, Energy Ball | Ice Beam 54, Muddy Water 56 | Ludicolo |
| Greninja | super rod | 41 | Oxide | Waterfall, Fling, Scald, Dark Pulse | Extrasensory 43, Sludge Wave 47, Gunk Shot 51, Hydro Pump 55 | Greninja |
| Greninja | super rod | 41 | Rewrite | Fling, Shadow Sneak, Scald, Dark Pulse | Extrasensory 43, Sludge Wave 47, Gunk Shot 51, Ice Beam 54, Surf 56 | Greninja |

## Ravaged Path

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 56 | At the cap |
|---|---|---|---|---|---|---|
| Milotic | super rod | 30 | Oxide | Twister, Recover, Captivate, Aqua Tail | Hydro Pump 37, Attract 41, Safeguard 45, Aqua Ring 49 | Milotic |
| Milotic | super rod | 30 | Rewrite | Water Gun, Twister | Recover 31, Aqua Tail 32, Aurora Beam 33, Dragon Pulse 35, Surf 37, Attract 41, Muddy Water 43, Safeguard 45, Aqua Ring 49, Alluring Voice 54, Scald 56 | Milotic |
| Whiscash | super rod | 30 | Oxide | Mud Bomb, Amnesia, Water Pulse, Magnitude | Rest 33, Snore 33, Aqua Tail 39, Earthquake 45, Future Sight 51 | Whiscash |
| Whiscash | super rod | 30 | Rewrite | Amnesia, Water Pulse, Magnitude, Bulldoze | Rest 33, Zen Headbutt 36, Aqua Tail 39, Earth Power 40, Wild Charge 42, Earthquake 45, Future Sight 51, Spark 54, Ice Beam 56 | Whiscash |
| Crawdaunt | super rod | 33 | Oxide | BubbleBeam, Protect, Knock Off, Swift | Taunt 34, Night Slash 39, Crabhammer 44, Swords Dance 52 | Crawdaunt |
| Crawdaunt | super rod | 33 | Rewrite | BubbleBeam, Knock Off, Swift, Taunt | Throat Chop 35, Aerial Ace 36, Night Slash 39, X-Scissor 41, Crabhammer 44, Brick Break 48, Swords Dance 52, Rock Tomb 54 | Crawdaunt |
| Lanturn | super rod | 33 | Oxide | Stockpile, Swallow, Spit Up, BubbleBeam | Signal Beam 35, Discharge 40, Aqua Ring 47, Hydro Pump 52 | Lanturn |
| Lanturn | super rod | 33 | Rewrite | Spit Up, BubbleBeam, Signal Beam, Scald | Surf 34, Thunderbolt 37, Discharge 40, Flash Cannon 43, Aqua Ring 47, Muddy Water 52, Volt Switch 54, Dazzling Gleam 55 | Lanturn |
| Greninja | super rod | 36 | Oxide | Acrobatics, Low Kick, Waterfall, Fling | Scald 37, Dark Pulse 40, Extrasensory 43, Sludge Wave 47, Gunk Shot 51, Hydro Pump 55 | Greninja |
| Greninja | super rod | 36 | Rewrite | Low Kick, Waterfall, Fling, Shadow Sneak | Scald 37, Dark Pulse 40, Extrasensory 43, Sludge Wave 47, Gunk Shot 51, Ice Beam 54, Surf 56 | Greninja |

## Route 203

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 56 | At the cap |
|---|---|---|---|---|---|---|
| Horsea | super rod | 30 | Oxide | BubbleBeam, Agility, Twister, Brine | as Kingdra: Hydro Pump 40, Dragon Dance 48 | Kingdra (from 32) |
| Horsea | super rod | 30 | Rewrite | BubbleBeam, Agility, Twister, Brine | as Kingdra: Octazooka 40, Aurora Beam 44, Scald 54 | Kingdra (from 32) |
| Sharpedo | super rod | 30 | Oxide | Swagger, Assurance, Crunch, Slash | Aqua Jet 34, Taunt 40, Agility 45, Skull Bash 50, Night Slash 56 | Sharpedo |
| Sharpedo | super rod | 30 | Rewrite | Swagger, Assurance, Crunch, Slash | Aqua Jet 31, Bug Bite 35, Aerial Ace 37, Taunt 40, Liquidation 41, Agility 45, Skull Bash 50, Poison Fang 54, Night Slash 56 | Sharpedo |
| Floatzel | super rod | 33 | Oxide | Swift, Aqua Jet, Crunch, Agility | Whirlpool 39, Razor Wind 50 | Floatzel |
| Floatzel | super rod | 33 | Rewrite | Aqua Jet, Crunch, Icy Wind, Flip Turn | Waterfall 36, Whirlpool 39, Liquidation 41, Low Sweep 44, Agility 51, Rock Tomb 53, Ice Fang 56 | Floatzel |
| Quagsire | super rod | 33 | Oxide | Slam, Mud Bomb, Amnesia, Yawn | Earthquake 36, Mist 48, Haze 48, Muddy Water 53 | Quagsire |
| Quagsire | super rod | 33 | Rewrite | Mud Bomb, Amnesia, Trailblaze, Yawn | Earthquake 36, Rock Slide 39, Toxic 40, Drain Punch 44, Mist 48, Muddy Water 53, Poison Jab 54, Aqua Tail 56 | Quagsire |
| Feraligatr | super rod | 36 | Oxide | Ice Fang, Flail, Agility, Crunch | Slash 37, Screech 45, Thrash 50 | Feraligatr |
| Feraligatr | super rod | 36 | Rewrite | Agility, Crunch, Slash, Bulldoze | Metal Claw 39, Aqua Jet 40, Liquidation 42, Screech 45 | Feraligatr |

## Route 204

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 56 | At the cap |
|---|---|---|---|---|---|---|
| Floatzel | super rod | 30 | Oxide | Swift, Aqua Jet, Crunch, Agility | Whirlpool 39, Razor Wind 50 | Floatzel |
| Floatzel | super rod | 30 | Rewrite | Swift, Aqua Jet, Crunch, Icy Wind | Flip Turn 33, Waterfall 36, Whirlpool 39, Liquidation 41, Low Sweep 44, Agility 51, Rock Tomb 53, Ice Fang 56 | Floatzel |
| Gastrodon | super rod | 30 to 33 | Oxide | Water Pulse, Mud Bomb, Hidden Power, Body Slam | Muddy Water 41, Recover 54 | Gastrodon |
| Gastrodon | super rod | 30 to 33 | Rewrite | Water Pulse, Mud Bomb, Hidden Power, Body Slam | AncientPower 33, Earth Power 35, Clear Smog 37, Muddy Water 41, Bulldoze 44, Sludge Bomb 46, Ice Beam 49, Recover 54, Skitter Smack 56 | Gastrodon |
| Quagsire | super rod | 30 | Oxide | Mud Shot, Slam, Mud Bomb, Amnesia | Yawn 31, Earthquake 36, Mist 48, Haze 48, Muddy Water 53 | Quagsire |
| Quagsire | super rod | 30 | Rewrite | Slam, Mud Bomb, Amnesia, Trailblaze | Yawn 31, Earthquake 36, Rock Slide 39, Toxic 40, Drain Punch 44, Mist 48, Muddy Water 53, Poison Jab 54, Aqua Tail 56 | Quagsire |
| Seaking | super rod | 30 | Oxide | Horn Attack, Water Pulse, Flail, Aqua Ring | Fury Attack 31, Waterfall 40, Horn Drill 47, Agility 56 | Seaking |
| Seaking | super rod | 30 | Rewrite | Horn Attack, Water Pulse, Flail, Aqua Ring | Aqua Jet 34, Skull Bash 37, Waterfall 40, Poison Jab 44, Drill Run 47, Knock Off 50, Aqua Tail 54, Agility 56 | Seaking |
| Crawdaunt | super rod | 33 | Oxide | BubbleBeam, Protect, Knock Off, Swift | Taunt 34, Night Slash 39, Crabhammer 44, Swords Dance 52 | Crawdaunt |
| Crawdaunt | super rod | 33 | Rewrite | BubbleBeam, Knock Off, Swift, Taunt | Throat Chop 35, Aerial Ace 36, Night Slash 39, X-Scissor 41, Crabhammer 44, Brick Break 48, Swords Dance 52, Rock Tomb 54 | Crawdaunt |
| Ludicolo | super rod | 33 | Oxide | Astonish, Growl, Mega Drain, Nature Power | nothing | Ludicolo |
| Ludicolo | super rod | 33 | Rewrite | Astonish, Growl, Mega Drain, Nature Power | Energy Ball 34, Ice Beam 54, Muddy Water 56 | Ludicolo |
| Whiscash | super rod | 33 | Oxide | Water Pulse, Magnitude, Rest, Snore | Aqua Tail 39, Earthquake 45, Future Sight 51 | Whiscash |
| Whiscash | super rod | 33 | Rewrite | Water Pulse, Magnitude, Bulldoze, Rest | Zen Headbutt 36, Aqua Tail 39, Earth Power 40, Wild Charge 42, Earthquake 45, Future Sight 51, Spark 54, Ice Beam 56 | Whiscash |
| Golduck | super rod | 36 | Oxide | Confusion, Water Pulse, Fury Swipes, Screech | Psych Up 37, Zen Headbutt 44, Amnesia 50, Hydro Pump 56 | Golduck |
| Golduck | super rod | 36 | Rewrite | Water Pulse, Fury Swipes, Screech, Surf | Psych Up 37, Aurora Beam 40, Zen Headbutt 44, Power Gem 47, Amnesia 50, Ice Beam 54, Muddy Water 56 | Golduck |
| Poliwrath | super rod | 36 | Oxide | BubbleBeam, Hypnosis, DoubleSlap, Submission | DynamicPunch 43, Mind Reader 53 | Poliwrath |
| Poliwrath | super rod | 36 | Rewrite | BubbleBeam, Hypnosis, DoubleSlap, Liquidation | Brick Break 43, Mind Reader 53, Rock Tomb 54, Throat Chop 56 | Poliwrath |

## Route 205

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 56 | At the cap |
|---|---|---|---|---|---|---|
| Lombre | super rod | 30 | Oxide | Fake Out, Fury Swipes, Water Sport, BubbleBeam | nothing | Ludicolo (from 30) |
| Lombre | super rod | 30 | Rewrite | Water Sport, Swagger, BubbleBeam, Giga Drain | as Ludicolo: Energy Ball 34, Ice Beam 54, Muddy Water 56 | Ludicolo (from 30) |
| Ludicolo | super rod | 30 | Oxide | Astonish, Growl, Mega Drain, Nature Power | nothing | Ludicolo |
| Ludicolo | super rod | 30 | Rewrite | Astonish, Growl, Mega Drain, Nature Power | Energy Ball 34, Ice Beam 54, Muddy Water 56 | Ludicolo |
| Seaking | super rod | 30 | Oxide | Horn Attack, Water Pulse, Flail, Aqua Ring | Fury Attack 31, Waterfall 40, Horn Drill 47, Agility 56 | Seaking |
| Seaking | super rod | 30 | Rewrite | Horn Attack, Water Pulse, Flail, Aqua Ring | Aqua Jet 34, Skull Bash 37, Waterfall 40, Poison Jab 44, Drill Run 47, Knock Off 50, Aqua Tail 54, Agility 56 | Seaking |
| Whiscash | super rod | 30 | Oxide | Mud Bomb, Amnesia, Water Pulse, Magnitude | Rest 33, Snore 33, Aqua Tail 39, Earthquake 45, Future Sight 51 | Whiscash |
| Whiscash | super rod | 30 | Rewrite | Amnesia, Water Pulse, Magnitude, Bulldoze | Rest 33, Zen Headbutt 36, Aqua Tail 39, Earth Power 40, Wild Charge 42, Earthquake 45, Future Sight 51, Spark 54, Ice Beam 56 | Whiscash |
| Araquanid | super rod | 33 | Oxide | BubbleBeam, Bug Bite, Headbutt, Soak | Dive 36, Lunge 41, Scald 48, Hydro Pump 51, Liquidation 55 | Araquanid |
| Araquanid | super rod | 33 | Rewrite | Bug Bite, Headbutt, Spider Web, Soak | Skitter Smack 34, Dive 36, Waterfall 38, Lunge 41, Poison Jab 44, Scald 48, Crunch 51, Body Slam 54, Liquidation 55 | Araquanid |
| Crawdaunt | super rod | 33 | Oxide | BubbleBeam, Protect, Knock Off, Swift | Taunt 34, Night Slash 39, Crabhammer 44, Swords Dance 52 | Crawdaunt |
| Crawdaunt | super rod | 33 | Rewrite | BubbleBeam, Knock Off, Swift, Taunt | Throat Chop 35, Aerial Ace 36, Night Slash 39, X-Scissor 41, Crabhammer 44, Brick Break 48, Swords Dance 52, Rock Tomb 54 | Crawdaunt |
| Jellicent | super rod | 33 | Oxide | Water Pulse, Imprison, Confuse Ray, Hex | Brine 34, Pain Split 39, Destiny Bond 45, Shadow Ball 51, Scald 55 | Jellicent |
| Jellicent | super rod | 33 | Rewrite | Water Pulse, Imprison, Confuse Ray, Hex | Brine 34, Pain Split 39, Muddy Water 45, Shadow Ball 51, Sludge Bomb 54, Scald 55 | Jellicent |
| Lanturn | super rod | 33 | Oxide | Stockpile, Swallow, Spit Up, BubbleBeam | Signal Beam 35, Discharge 40, Aqua Ring 47, Hydro Pump 52 | Lanturn |
| Lanturn | super rod | 33 | Rewrite | Spit Up, BubbleBeam, Signal Beam, Scald | Surf 34, Thunderbolt 37, Discharge 40, Flash Cannon 43, Aqua Ring 47, Muddy Water 52, Volt Switch 54, Dazzling Gleam 55 | Lanturn |
| Golduck | super rod | 36 | Oxide | Confusion, Water Pulse, Fury Swipes, Screech | Psych Up 37, Zen Headbutt 44, Amnesia 50, Hydro Pump 56 | Golduck |
| Golduck | super rod | 36 | Rewrite | Water Pulse, Fury Swipes, Screech, Surf | Psych Up 37, Aurora Beam 40, Zen Headbutt 44, Power Gem 47, Amnesia 50, Ice Beam 54, Muddy Water 56 | Golduck |

## Route 208

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 56 | At the cap |
|---|---|---|---|---|---|---|
| Seaking | super rod | 32 | Oxide | Water Pulse, Flail, Aqua Ring, Fury Attack | Waterfall 40, Horn Drill 47, Agility 56 | Seaking |
| Seaking | super rod | 32 | Rewrite | Horn Attack, Water Pulse, Flail, Aqua Ring | Aqua Jet 34, Skull Bash 37, Waterfall 40, Poison Jab 44, Drill Run 47, Knock Off 50, Aqua Tail 54, Agility 56 | Seaking |
| Whiscash | super rod | 32 | Oxide | Mud Bomb, Amnesia, Water Pulse, Magnitude | Rest 33, Snore 33, Aqua Tail 39, Earthquake 45, Future Sight 51 | Whiscash |
| Whiscash | super rod | 32 | Rewrite | Amnesia, Water Pulse, Magnitude, Bulldoze | Rest 33, Zen Headbutt 36, Aqua Tail 39, Earth Power 40, Wild Charge 42, Earthquake 45, Future Sight 51, Spark 54, Ice Beam 56 | Whiscash |
| Crawdaunt | super rod | 35 | Oxide | Protect, Knock Off, Swift, Taunt | Night Slash 39, Crabhammer 44, Swords Dance 52 | Crawdaunt |
| Crawdaunt | super rod | 35 | Rewrite | Knock Off, Swift, Taunt, Throat Chop | Aerial Ace 36, Night Slash 39, X-Scissor 41, Crabhammer 44, Brick Break 48, Swords Dance 52, Rock Tomb 54 | Crawdaunt |
| Milotic | super rod | 35 | Oxide | Twister, Recover, Captivate, Aqua Tail | Hydro Pump 37, Attract 41, Safeguard 45, Aqua Ring 49 | Milotic |
| Milotic | super rod | 35 | Rewrite | Recover, Aqua Tail, Aurora Beam, Dragon Pulse | Surf 37, Attract 41, Muddy Water 43, Safeguard 45, Aqua Ring 49, Alluring Voice 54, Scald 56 | Milotic |
| Toxapex | super rod | 38 | Oxide | Venoshock, Recover, Spike Cannon, Pin Missile | Toxic 39, Venom Drench 42, Poison Jab 43, Liquidation 45 | Toxapex |
| Toxapex | super rod | 38 | Rewrite | Recover, Spike Cannon, Toxic, Pin Missile | Venom Drench 42, Poison Jab 43, Liquidation 45, Lunge 53, Ice Beam 54, Sludge Bomb 56 | Toxapex |

## Route 209

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 56 | At the cap |
|---|---|---|---|---|---|---|
| Floatzel | super rod | 33 | Oxide | Swift, Aqua Jet, Crunch, Agility | Whirlpool 39, Razor Wind 50 | Floatzel |
| Floatzel | super rod | 33 | Rewrite | Aqua Jet, Crunch, Icy Wind, Flip Turn | Waterfall 36, Whirlpool 39, Liquidation 41, Low Sweep 44, Agility 51, Rock Tomb 53, Ice Fang 56 | Floatzel |
| Quagsire | super rod | 33 | Oxide | Slam, Mud Bomb, Amnesia, Yawn | Earthquake 36, Mist 48, Haze 48, Muddy Water 53 | Quagsire |
| Quagsire | super rod | 33 | Rewrite | Mud Bomb, Amnesia, Trailblaze, Yawn | Earthquake 36, Rock Slide 39, Toxic 40, Drain Punch 44, Mist 48, Muddy Water 53, Poison Jab 54, Aqua Tail 56 | Quagsire |
| Gastrodon | super rod | 36 | Oxide | Water Pulse, Mud Bomb, Hidden Power, Body Slam | Muddy Water 41, Recover 54 | Gastrodon |
| Gastrodon | super rod | 36 | Rewrite | Hidden Power, Body Slam, AncientPower, Earth Power | Clear Smog 37, Muddy Water 41, Bulldoze 44, Sludge Bomb 46, Ice Beam 49, Recover 54, Skitter Smack 56 | Gastrodon |
| Ludicolo | super rod | 36 | Oxide | Astonish, Growl, Mega Drain, Nature Power | nothing | Ludicolo |
| Ludicolo | super rod | 36 | Rewrite | Growl, Mega Drain, Nature Power, Energy Ball | Ice Beam 54, Muddy Water 56 | Ludicolo |
| Feraligatr | super rod | 39 | Oxide | Flail, Agility, Crunch, Slash | Screech 45, Thrash 50 | Feraligatr |
| Feraligatr | super rod | 39 | Rewrite | Crunch, Slash, Bulldoze, Metal Claw | Aqua Jet 40, Liquidation 42, Screech 45 | Feraligatr |

## Route 210

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 56 | At the cap |
|---|---|---|---|---|---|---|
| Seaking | super rod | 36 | Oxide | Water Pulse, Flail, Aqua Ring, Fury Attack | Waterfall 40, Horn Drill 47, Agility 56 | Seaking |
| Seaking | super rod | 36 | Rewrite | Water Pulse, Flail, Aqua Ring, Aqua Jet | Skull Bash 37, Waterfall 40, Poison Jab 44, Drill Run 47, Knock Off 50, Aqua Tail 54, Agility 56 | Seaking |
| Whiscash | super rod | 36 | Oxide | Water Pulse, Magnitude, Rest, Snore | Aqua Tail 39, Earthquake 45, Future Sight 51 | Whiscash |
| Whiscash | super rod | 36 | Rewrite | Magnitude, Bulldoze, Rest, Zen Headbutt | Aqua Tail 39, Earth Power 40, Wild Charge 42, Earthquake 45, Future Sight 51, Spark 54, Ice Beam 56 | Whiscash |
| Crawdaunt | super rod | 39 | Oxide | Knock Off, Swift, Taunt, Night Slash | Crabhammer 44, Swords Dance 52 | Crawdaunt |
| Crawdaunt | super rod | 39 | Rewrite | Taunt, Throat Chop, Aerial Ace, Night Slash | X-Scissor 41, Crabhammer 44, Brick Break 48, Swords Dance 52, Rock Tomb 54 | Crawdaunt |
| Milotic | super rod | 39 | Oxide | Recover, Captivate, Aqua Tail, Hydro Pump | Attract 41, Safeguard 45, Aqua Ring 49 | Milotic |
| Milotic | super rod | 39 | Rewrite | Aqua Tail, Aurora Beam, Dragon Pulse, Surf | Attract 41, Muddy Water 43, Safeguard 45, Aqua Ring 49, Alluring Voice 54, Scald 56 | Milotic |
| Lumineon | super rod | 42 | Oxide | Captivate, Safeguard, Aqua Ring, Whirlpool | U-turn 48, Bounce 53 | Lumineon |
| Lumineon | super rod | 42 | Rewrite | Icy Wind, Aqua Tail, Signal Beam, Whirlpool | Ice Fang 45, U-turn 48, Bounce 53, Air Slash 54, Crunch 56 | Lumineon |

## Route 212

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 56 | At the cap |
|---|---|---|---|---|---|---|
| Floatzel | super rod | 35 | Oxide | Swift, Aqua Jet, Crunch, Agility | Whirlpool 39, Razor Wind 50 | Floatzel |
| Floatzel | super rod | 35 | Rewrite | Aqua Jet, Crunch, Icy Wind, Flip Turn | Waterfall 36, Whirlpool 39, Liquidation 41, Low Sweep 44, Agility 51, Rock Tomb 53, Ice Fang 56 | Floatzel |
| Quagsire | super rod | 35 | Oxide | Slam, Mud Bomb, Amnesia, Yawn | Earthquake 36, Mist 48, Haze 48, Muddy Water 53 | Quagsire |
| Quagsire | super rod | 35 | Rewrite | Mud Bomb, Amnesia, Trailblaze, Yawn | Earthquake 36, Rock Slide 39, Toxic 40, Drain Punch 44, Mist 48, Muddy Water 53, Poison Jab 54, Aqua Tail 56 | Quagsire |
| Whiscash | super rod | 35 | Oxide | Water Pulse, Magnitude, Rest, Snore | Aqua Tail 39, Earthquake 45, Future Sight 51 | Whiscash |
| Whiscash | super rod | 35 | Rewrite | Water Pulse, Magnitude, Bulldoze, Rest | Zen Headbutt 36, Aqua Tail 39, Earth Power 40, Wild Charge 42, Earthquake 45, Future Sight 51, Spark 54, Ice Beam 56 | Whiscash |
| Gastrodon | super rod | 38 | Oxide | Water Pulse, Mud Bomb, Hidden Power, Body Slam | Muddy Water 41, Recover 54 | Gastrodon |
| Gastrodon | super rod | 38 | Rewrite | Body Slam, AncientPower, Earth Power, Clear Smog | Muddy Water 41, Bulldoze 44, Sludge Bomb 46, Ice Beam 49, Recover 54, Skitter Smack 56 | Gastrodon |
| Ludicolo | super rod | 38 | Oxide | Astonish, Growl, Mega Drain, Nature Power | nothing | Ludicolo |
| Ludicolo | super rod | 38 | Rewrite | Growl, Mega Drain, Nature Power, Energy Ball | Ice Beam 54, Muddy Water 56 | Ludicolo |
| Sharpedo | super rod | 38 | Oxide | Assurance, Crunch, Slash, Aqua Jet | Taunt 40, Agility 45, Skull Bash 50, Night Slash 56 | Sharpedo |
| Sharpedo | super rod | 38 | Rewrite | Slash, Aqua Jet, Bug Bite, Aerial Ace | Taunt 40, Liquidation 41, Agility 45, Skull Bash 50, Poison Fang 54, Night Slash 56 | Sharpedo |
| Alomomola | super rod | 41 | Oxide | Wake-Up Slap, Soak, Wish, Brine | Safeguard 45, Whirlpool 49, Helping Hand 53 | Alomomola |
| Alomomola | super rod | 41 | Rewrite | Soak, Play Rough, Wish, Brine | Zen Headbutt 43, Safeguard 45, Whirlpool 49, Helping Hand 53, Flip Turn 54, Liquidation 56 | Alomomola |
| Greninja | super rod | 41 | Oxide | Waterfall, Fling, Scald, Dark Pulse | Extrasensory 43, Sludge Wave 47, Gunk Shot 51, Hydro Pump 55 | Greninja |
| Greninja | super rod | 41 | Rewrite | Fling, Shadow Sneak, Scald, Dark Pulse | Extrasensory 43, Sludge Wave 47, Gunk Shot 51, Ice Beam 54, Surf 56 | Greninja |

## Route 213

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 56 | At the cap |
|---|---|---|---|---|---|---|
| Lumineon | super rod | 35 | Oxide | Water Pulse, Captivate, Safeguard, Aqua Ring | Whirlpool 42, U-turn 48, Bounce 53 | Lumineon |
| Lumineon | super rod | 35 | Rewrite | Safeguard, Flip Turn, Aqua Ring, Icy Wind | Aqua Tail 38, Signal Beam 40, Whirlpool 42, Ice Fang 45, U-turn 48, Bounce 53, Air Slash 54, Crunch 56 | Lumineon |
| Tentacruel | super rod | 35 | Oxide | BubbleBeam, Wrap, Barrier, Water Pulse | Poison Jab 36, Screech 42, Hydro Pump 49, Wring Out 55 | Tentacruel |
| Tentacruel | super rod | 35 | Rewrite | Barrier, Water Pulse, Poison Jab, Aurora Beam | Sludge Bomb 39, Screech 42, Psybeam 44, Surf 49, Muddy Water 53, Throat Chop 54, Power Gem 56 | Tentacruel |
| Octillery | super rod | 38 | Oxide | Focus Energy, Octazooka, Bullet Seed, Wring Out | Signal Beam 42, Ice Beam 48, Hyper Beam 55 | Octillery |
| Octillery | super rod | 38 | Rewrite | Bullet Seed, Round, Charge Beam, Scald | Skitter Smack 40, Signal Beam 42, Ice Beam 48, Psychic 54, Hyper Beam 55 | Octillery |
| Toxapex | super rod | 38 | Oxide | Venoshock, Recover, Spike Cannon, Pin Missile | Toxic 39, Venom Drench 42, Poison Jab 43, Liquidation 45 | Toxapex |
| Toxapex | super rod | 38 | Rewrite | Recover, Spike Cannon, Toxic, Pin Missile | Venom Drench 42, Poison Jab 43, Liquidation 45, Lunge 53, Ice Beam 54, Sludge Bomb 56 | Toxapex |
| Quagsire | super rod | 41 | Oxide | Mud Bomb, Amnesia, Yawn, Earthquake | Mist 48, Haze 48, Muddy Water 53 | Quagsire |
| Quagsire | super rod | 41 | Rewrite | Yawn, Earthquake, Rock Slide, Toxic | Drain Punch 44, Mist 48, Muddy Water 53, Poison Jab 54, Aqua Tail 56 | Quagsire |

## Route 214

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 56 | At the cap |
|---|---|---|---|---|---|---|
| Ludicolo | super rod | 35 | Oxide | Astonish, Growl, Mega Drain, Nature Power | nothing | Ludicolo |
| Ludicolo | super rod | 35 | Rewrite | Growl, Mega Drain, Nature Power, Energy Ball | Ice Beam 54, Muddy Water 56 | Ludicolo |
| Quagsire | super rod | 35 | Oxide | Slam, Mud Bomb, Amnesia, Yawn | Earthquake 36, Mist 48, Haze 48, Muddy Water 53 | Quagsire |
| Quagsire | super rod | 35 | Rewrite | Mud Bomb, Amnesia, Trailblaze, Yawn | Earthquake 36, Rock Slide 39, Toxic 40, Drain Punch 44, Mist 48, Muddy Water 53, Poison Jab 54, Aqua Tail 56 | Quagsire |
| Gastrodon | super rod | 38 | Oxide | Water Pulse, Mud Bomb, Hidden Power, Body Slam | Muddy Water 41, Recover 54 | Gastrodon |
| Gastrodon | super rod | 38 | Rewrite | Body Slam, AncientPower, Earth Power, Clear Smog | Muddy Water 41, Bulldoze 44, Sludge Bomb 46, Ice Beam 49, Recover 54, Skitter Smack 56 | Gastrodon |
| Seaking | super rod | 38 | Oxide | Water Pulse, Flail, Aqua Ring, Fury Attack | Waterfall 40, Horn Drill 47, Agility 56 | Seaking |
| Seaking | super rod | 38 | Rewrite | Flail, Aqua Ring, Aqua Jet, Skull Bash | Waterfall 40, Poison Jab 44, Drill Run 47, Knock Off 50, Aqua Tail 54, Agility 56 | Seaking |
| Mantine | super rod | 41 | Oxide | Water Pulse, Take Down, Confuse Ray, Bounce | Aqua Ring 46, Hydro Pump 49 | Mantine |
| Mantine | super rod | 41 | Rewrite | Round, Confuse Ray, Bounce, Psybeam | Surf 43, Aqua Ring 46, Scald 49, Air Slash 54, Roost 56 | Mantine |

## Route 216

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 56 | At the cap |
|---|---|---|---|---|---|---|
| Snover | wild | 32 | Oxide | Swagger, Mist, Ice Shard, Ingrain | Wood Hammer 36; as Abomasnow: Blizzard 47 | Abomasnow (from 40) |
| Snover | wild | 32 | Rewrite | Mist, Ice Shard, Seed Bomb, Rock Tomb | Body Press 34, Wood Hammer 36; as Abomasnow: Ice Beam 41, Giga Drain 50, Ice Punch 53, Rock Climb 54, Shadow Ball 56 | Abomasnow (from 40) |
| Absol | wild | 33 | Oxide | Pursuit, Swords Dance, Bite, Double Team | Slash 36, Future Sight 41, Sucker Punch 44, Detect 49, Night Slash 52 | Absol |
| Absol | wild | 33 | Rewrite | Quick Attack, Pursuit, Swords Dance, Bite | Slash 36, Future Sight 41, Sucker Punch 44, X-Scissor 48, Night Slash 52, Shadow Ball 54, Throat Chop 56 | Absol |
| Delibird | wild | 33 | Oxide | Present | nothing | Delibird |
| Delibird | wild | 33 | Rewrite | Present | Swagger 34, Ice Beam 54, Drill Run 55, Drill Peck 56 | Delibird |
| Frosmoth | wild | 33 | Oxide | Defog, FeatherDance, Aurora Beam, Bug Buzz | Aurora Veil 36, Blizzard 40, Tailwind 44, Wide Guard 48, Quiver Dance 52 | Frosmoth |
| Frosmoth | wild | 33 | Rewrite | Stun Spore, Infestation, Bug Buzz, Defog | Aurora Beam 34, Aurora Veil 36, Ice Beam 40, Tailwind 44, Wide Guard 48, Quiver Dance 52, Air Slash 54, Giga Drain 56 | Frosmoth |
| Sneasel | wild | 33 | Oxide | Faint Attack, Fury Swipes, Agility, Icy Wind | Slash 35, Metal Claw 42, Ice Shard 49 | Sneasel; Weavile in HQ |
| Sneasel | wild | 33 | Rewrite | Fury Swipes, Nasty Plot, Agility, Icy Wind | Slash 35, Low Sweep 38, Poison Jab 40, Metal Claw 42, Ice Shard 49, Ice Fang 53, Night Slash 54, Ice Punch 56 | Sneasel; Weavile in HQ |
| Snorunt | wild | 33 to 34 | Oxide | Headbutt, Protect, Ice Fang, Crunch | Ice Shard 37; as Glalie: Blizzard 51 | Glalie (from 42) |
| Snorunt | wild | 33 to 34 | Oxide | Headbutt, Protect, Ice Fang, Crunch | as Froslass: Ice Shard 37, Blizzard 51 | Froslass (from 33) |
| Snorunt | wild | 33 to 34 | Rewrite | Headbutt, Ominous Wind, Ice Fang, Crunch | Draining Kiss 34, Ice Shard 37; as Glalie: Rock Slide 42, Power Gem 44, Confuse Ray 48, Earth Power 53, Ice Punch 54, Shadow Ball 56 | Glalie (from 42) |
| Snorunt | wild | 33 to 34 | Rewrite | Headbutt, Ominous Wind, Ice Fang, Crunch | as Froslass: Ice Shard 37, Ice Beam 51 | Froslass (from 33) |
| Alolan Ninetales | wild | 34 | Oxide | Tail Whip, Disable, Ice Shard, Safeguard | nothing | Alolan Ninetales |
| Alolan Ninetales | wild | 34 | Rewrite | Incinerate, Spite, Payback, Icy Wind | Chilling Water 36, Dazzling Gleam 39, Extrasensory 43, Ice Beam 44, Dark Pulse 48, Mystical Fire 53, BurningJealousy 54, Moonblast 56 | Alolan Ninetales |
| Golbat | wild | 34 | Oxide | Wing Attack, Confuse Ray, Air Cutter, Mean Look | Poison Fang 39; as Crobat: Haze 45, Air Slash 51 | Crobat (from 40) |
| Golbat | wild | 34 | Rewrite | Confuse Ray, Air Cutter, Poison Jab, Mean Look | Steel Wing 36, Poison Fang 39; as Crobat: Zen Headbutt 45, Air Slash 51, U-turn 54, Crunch 56 | Crobat (from 40) |
| Mienfoo | wild | 34 | Oxide | Force Palm, Bounce, Drain Punch, Vacuum Wave | as Mienshao: Aura Sphere 38, Me First 40, Jump Kick 45, Dual Chop 48, Focus Blast 51, Acrobatics 55 | Mienshao (from 36) |
| Mienfoo | wild | 34 | Rewrite | Bounce, Drain Punch, Low Sweep, Vacuum Wave | as Mienshao: Aura Sphere 38, U-turn 41, Rock Tomb 43, Jump Kick 45, Dual Chop 48, Poison Jab 51, Upper Hand 54, Acrobatics 55, Hammer Arm 56 | Mienshao (from 36) |
| Bronzong | wild | 35 | Oxide | Extrasensory, Iron Defense, Safeguard, Block | Gyro Ball 38, Future Sight 43, Faint Attack 50 | Bronzong |
| Bronzong | wild | 35 | Rewrite | Iron Defense, Safeguard, Block, Iron Head | Gyro Ball 38, Rock Tomb 40, Future Sight 43, Body Press 46, Faint Attack 50, Shadow Ball 54 | Bronzong |
| Galarian Mr Mime | wild | 35 | Oxide | Icy Wind, Double Kick, Psybeam, Hypnosis | Mirror Coat 36, Sucker Punch 40; as Mr. Rime: Freeze-Dry 44, Psychic 48, Teeter Dance 52 | Mr. Rime (from 42) |
| Galarian Mr Mime | wild | 35 | Rewrite | Icy Wind, Double Kick, Psybeam, Hypnosis | Mirror Coat 36, Sucker Punch 40, Dazzling Gleam 42; as Mr. Rime: Freeze-Dry 44, Psychic 48, Teeter Dance 52, Ice Beam 54, Encore 56 | Mr. Rime (from 42) |
| Slugma | wild | 35 | Oxide | Harden, Recover, AncientPower, Amnesia | Lava Plume 38; as Magcargo: Lava Plume 40, Rock Slide 45, Body Slam 52 | Magcargo (from 38) |
| Slugma | wild | 35 | Rewrite | Harden, Recover, AncientPower, Amnesia | Lava Plume 38; as Magcargo: Lava Plume 40, Shell Smash 41, Scorching Sands 42, Rock Slide 45, Body Slam 52, BurningJealousy 54, Energy Ball 56 | Magcargo (from 38) |

## Route 217

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 56 | At the cap |
|---|---|---|---|---|---|---|
| Swinub | wild | 32 | Oxide | Mud Bomb, Icy Wind, Ice Shard, Take Down | as Piloswine: Fury Attack 33, Earthquake 40; as Mamoswine: Earthquake 40, Mist 48, Blizzard 56 | Mamoswine (from 40) |
| Swinub | wild | 32 | Rewrite | Icy Wind, Ice Fang, Ice Shard, Take Down | as Piloswine: AncientPower 33, Smack Down 36, Bulldoze 38, Earthquake 40; as Mamoswine: Earthquake 40, Mist 48, Brick Break 52, Icicle Crash 54, Ice Beam 56 | Mamoswine (from 40) |
| Frosmoth | wild | 33 to 34 | Oxide | Defog, FeatherDance, Aurora Beam, Bug Buzz | Aurora Veil 36, Blizzard 40, Tailwind 44, Wide Guard 48, Quiver Dance 52 | Frosmoth |
| Frosmoth | wild | 33 to 34 | Rewrite | Stun Spore, Infestation, Bug Buzz, Defog | Aurora Beam 34, Aurora Veil 36, Ice Beam 40, Tailwind 44, Wide Guard 48, Quiver Dance 52, Air Slash 54, Giga Drain 56 | Frosmoth |
| Sneasel | wild | 33 | Oxide | Faint Attack, Fury Swipes, Agility, Icy Wind | Slash 35, Metal Claw 42, Ice Shard 49 | Sneasel; Weavile in HQ |
| Sneasel | wild | 33 | Rewrite | Fury Swipes, Nasty Plot, Agility, Icy Wind | Slash 35, Low Sweep 38, Poison Jab 40, Metal Claw 42, Ice Shard 49, Ice Fang 53, Night Slash 54, Ice Punch 56 | Sneasel; Weavile in HQ |
| Snorunt | wild | 33 | Oxide | Headbutt, Protect, Ice Fang, Crunch | Ice Shard 37; as Glalie: Blizzard 51 | Glalie (from 42) |
| Snorunt | wild | 33 | Oxide | Headbutt, Protect, Ice Fang, Crunch | as Froslass: Ice Shard 37, Blizzard 51 | Froslass (from 33) |
| Snorunt | wild | 33 | Rewrite | Headbutt, Ominous Wind, Ice Fang, Crunch | Draining Kiss 34, Ice Shard 37; as Glalie: Rock Slide 42, Power Gem 44, Confuse Ray 48, Earth Power 53, Ice Punch 54, Shadow Ball 56 | Glalie (from 42) |
| Snorunt | wild | 33 | Rewrite | Headbutt, Ominous Wind, Ice Fang, Crunch | as Froslass: Ice Shard 37, Ice Beam 51 | Froslass (from 33) |
| Snover | wild | 33 | Oxide | Swagger, Mist, Ice Shard, Ingrain | Wood Hammer 36; as Abomasnow: Blizzard 47 | Abomasnow (from 40) |
| Snover | wild | 33 | Rewrite | Mist, Ice Shard, Seed Bomb, Rock Tomb | Body Press 34, Wood Hammer 36; as Abomasnow: Ice Beam 41, Giga Drain 50, Ice Punch 53, Rock Climb 54, Shadow Ball 56 | Abomasnow (from 40) |
| Alolan Ninetales | wild | 34 | Oxide | Tail Whip, Disable, Ice Shard, Safeguard | nothing | Alolan Ninetales |
| Alolan Ninetales | wild | 34 | Rewrite | Incinerate, Spite, Payback, Icy Wind | Chilling Water 36, Dazzling Gleam 39, Extrasensory 43, Ice Beam 44, Dark Pulse 48, Mystical Fire 53, BurningJealousy 54, Moonblast 56 | Alolan Ninetales |
| Donphan | wild | 34 | Oxide | Magnitude, Slam, Fury Attack, Assurance | Scary Face 39, Earthquake 46, Giga Impact 54 | Donphan |
| Donphan | wild | 34 | Rewrite | Rapid Spin, Magnitude, Rock Tomb, Assurance | Trailblaze 35, Scary Face 39, Iron Head 42, Throat Chop 44, Earthquake 46, Seed Bomb 50, Giga Impact 54, Charm 56 | Donphan |
| Mienfoo | wild | 34 | Oxide | Force Palm, Bounce, Drain Punch, Vacuum Wave | as Mienshao: Aura Sphere 38, Me First 40, Jump Kick 45, Dual Chop 48, Focus Blast 51, Acrobatics 55 | Mienshao (from 36) |
| Mienfoo | wild | 34 | Rewrite | Bounce, Drain Punch, Low Sweep, Vacuum Wave | as Mienshao: Aura Sphere 38, U-turn 41, Rock Tomb 43, Jump Kick 45, Dual Chop 48, Poison Jab 51, Upper Hand 54, Acrobatics 55, Hammer Arm 56 | Mienshao (from 36) |
| Galarian Mr Mime | wild | 35 | Oxide | Icy Wind, Double Kick, Psybeam, Hypnosis | Mirror Coat 36, Sucker Punch 40; as Mr. Rime: Freeze-Dry 44, Psychic 48, Teeter Dance 52 | Mr. Rime (from 42) |
| Galarian Mr Mime | wild | 35 | Rewrite | Icy Wind, Double Kick, Psybeam, Hypnosis | Mirror Coat 36, Sucker Punch 40, Dazzling Gleam 42; as Mr. Rime: Freeze-Dry 44, Psychic 48, Teeter Dance 52, Ice Beam 54, Encore 56 | Mr. Rime (from 42) |
| Meditite | wild | 35 | Oxide | Feint, Calm Mind, Force Palm, Hi Jump Kick | Psych Up 36; as Medicham: Power Trick 42, Reversal 49, Recover 55 | Medicham (from 37) |
| Meditite | wild | 35 | Rewrite | Swagger, Rock Throw, Low Sweep, Hi Jump Kick | Psych Up 36; as Medicham: Power Trick 39, Poison Jab 40, Iron Head 44, Reversal 49, Zen Headbutt 52, Drain Punch 54, Recover 55 | Medicham (from 37) |
| Slugma | wild | 35 | Oxide | Harden, Recover, AncientPower, Amnesia | Lava Plume 38; as Magcargo: Lava Plume 40, Rock Slide 45, Body Slam 52 | Magcargo (from 38) |
| Slugma | wild | 35 | Rewrite | Harden, Recover, AncientPower, Amnesia | Lava Plume 38; as Magcargo: Lava Plume 40, Shell Smash 41, Scorching Sands 42, Rock Slide 45, Body Slam 52, BurningJealousy 54, Energy Ball 56 | Magcargo (from 38) |

## Route 218

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 56 | At the cap |
|---|---|---|---|---|---|---|
| Gorebyss | super rod | 36 | Oxide | Amnesia, Aqua Ring, Captivate, Baton Pass | Dive 37, Psychic 42, Aqua Tail 46, Hydro Pump 51 | Gorebyss |
| Gorebyss | super rod | 36 | Rewrite | Aqua Ring, Captivate, Baton Pass, Draining Kiss | Dive 37, Surf 40, Psychic 42, Aqua Tail 46, Muddy Water 51, Shadow Ball 54, Ice Beam 56 | Gorebyss |
| Mantine | super rod | 36 | Oxide | Agility, Wing Attack, Water Pulse, Take Down | Confuse Ray 37, Bounce 40, Aqua Ring 46, Hydro Pump 49 | Mantine |
| Mantine | super rod | 36 | Rewrite | Water Pulse, Take Down, Signal Beam, Round | Confuse Ray 37, Bounce 40, Psybeam 41, Surf 43, Aqua Ring 46, Scald 49, Air Slash 54, Roost 56 | Mantine |
| Gastrodon | super rod | 39 | Oxide | Water Pulse, Mud Bomb, Hidden Power, Body Slam | Muddy Water 41, Recover 54 | Gastrodon |
| Gastrodon | super rod | 39 | Rewrite | Body Slam, AncientPower, Earth Power, Clear Smog | Muddy Water 41, Bulldoze 44, Sludge Bomb 46, Ice Beam 49, Recover 54, Skitter Smack 56 | Gastrodon |
| Jellicent | super rod | 39 | Oxide | Confuse Ray, Hex, Brine, Pain Split | Destiny Bond 45, Shadow Ball 51, Scald 55 | Jellicent |
| Jellicent | super rod | 39 | Rewrite | Confuse Ray, Hex, Brine, Pain Split | Muddy Water 45, Shadow Ball 51, Sludge Bomb 54, Scald 55 | Jellicent |
| Greninja | super rod | 42 | Oxide | Waterfall, Fling, Scald, Dark Pulse | Extrasensory 43, Sludge Wave 47, Gunk Shot 51, Hydro Pump 55 | Greninja |
| Greninja | super rod | 42 | Rewrite | Fling, Shadow Sneak, Scald, Dark Pulse | Extrasensory 43, Sludge Wave 47, Gunk Shot 51, Ice Beam 54, Surf 56 | Greninja |

## Route 219

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 56 | At the cap |
|---|---|---|---|---|---|---|
| Jellicent | super rod | 30 | Oxide | Water Pulse, Imprison, Confuse Ray, Hex | Brine 34, Pain Split 39, Destiny Bond 45, Shadow Ball 51, Scald 55 | Jellicent |
| Jellicent | super rod | 30 | Rewrite | Water Pulse, Imprison, Confuse Ray, Hex | Brine 34, Pain Split 39, Muddy Water 45, Shadow Ball 51, Sludge Bomb 54, Scald 55 | Jellicent |
| Lanturn | super rod | 30 | Oxide | Stockpile, Swallow, Spit Up, BubbleBeam | Signal Beam 35, Discharge 40, Aqua Ring 47, Hydro Pump 52 | Lanturn |
| Lanturn | super rod | 30 | Rewrite | Stockpile, Swallow, Spit Up, BubbleBeam | Signal Beam 31, Scald 33, Surf 34, Thunderbolt 37, Discharge 40, Flash Cannon 43, Aqua Ring 47, Muddy Water 52, Volt Switch 54, Dazzling Gleam 55 | Lanturn |
| Lumineon | super rod | 33 | Oxide | Gust, Water Pulse, Captivate, Safeguard | Aqua Ring 35, Whirlpool 42, U-turn 48, Bounce 53 | Lumineon |
| Lumineon | super rod | 33 | Rewrite | Captivate, Safeguard, Flip Turn, Aqua Ring | Icy Wind 34, Aqua Tail 38, Signal Beam 40, Whirlpool 42, Ice Fang 45, U-turn 48, Bounce 53, Air Slash 54, Crunch 56 | Lumineon |
| Tentacruel | super rod | 33 | Oxide | BubbleBeam, Wrap, Barrier, Water Pulse | Poison Jab 36, Screech 42, Hydro Pump 49, Wring Out 55 | Tentacruel |
| Tentacruel | super rod | 33 | Rewrite | BubbleBeam, Barrier, Water Pulse, Poison Jab | Aurora Beam 34, Sludge Bomb 39, Screech 42, Psybeam 44, Surf 49, Muddy Water 53, Throat Chop 54, Power Gem 56 | Tentacruel |
| Greninja | super rod | 36 | Oxide | Acrobatics, Low Kick, Waterfall, Fling | Scald 37, Dark Pulse 40, Extrasensory 43, Sludge Wave 47, Gunk Shot 51, Hydro Pump 55 | Greninja |
| Greninja | super rod | 36 | Rewrite | Low Kick, Waterfall, Fling, Shadow Sneak | Scald 37, Dark Pulse 40, Extrasensory 43, Sludge Wave 47, Gunk Shot 51, Ice Beam 54, Surf 56 | Greninja |

## Route 220

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 56 | At the cap |
|---|---|---|---|---|---|---|
| Jellicent | super rod | 36 | Oxide | Imprison, Confuse Ray, Hex, Brine | Pain Split 39, Destiny Bond 45, Shadow Ball 51, Scald 55 | Jellicent |
| Jellicent | super rod | 36 | Rewrite | Imprison, Confuse Ray, Hex, Brine | Pain Split 39, Muddy Water 45, Shadow Ball 51, Sludge Bomb 54, Scald 55 | Jellicent |
| Lanturn | super rod | 36 | Oxide | Swallow, Spit Up, BubbleBeam, Signal Beam | Discharge 40, Aqua Ring 47, Hydro Pump 52 | Lanturn |
| Lanturn | super rod | 36 | Rewrite | BubbleBeam, Signal Beam, Scald, Surf | Thunderbolt 37, Discharge 40, Flash Cannon 43, Aqua Ring 47, Muddy Water 52, Volt Switch 54, Dazzling Gleam 55 | Lanturn |
| Lumineon | super rod | 39 | Oxide | Water Pulse, Captivate, Safeguard, Aqua Ring | Whirlpool 42, U-turn 48, Bounce 53 | Lumineon |
| Lumineon | super rod | 39 | Rewrite | Flip Turn, Aqua Ring, Icy Wind, Aqua Tail | Signal Beam 40, Whirlpool 42, Ice Fang 45, U-turn 48, Bounce 53, Air Slash 54, Crunch 56 | Lumineon |
| Tentacruel | super rod | 39 to 42 | Oxide | Wrap, Barrier, Water Pulse, Poison Jab | Screech 42, Hydro Pump 49, Wring Out 55 | Tentacruel |
| Tentacruel | super rod | 39 to 42 | Rewrite | Water Pulse, Poison Jab, Aurora Beam, Sludge Bomb | Screech 42, Psybeam 44, Surf 49, Muddy Water 53, Throat Chop 54, Power Gem 56 | Tentacruel |

## Route 221

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 56 | At the cap |
|---|---|---|---|---|---|---|
| Lanturn | super rod | 36 | Oxide | Swallow, Spit Up, BubbleBeam, Signal Beam | Discharge 40, Aqua Ring 47, Hydro Pump 52 | Lanturn |
| Lanturn | super rod | 36 | Rewrite | BubbleBeam, Signal Beam, Scald, Surf | Thunderbolt 37, Discharge 40, Flash Cannon 43, Aqua Ring 47, Muddy Water 52, Volt Switch 54, Dazzling Gleam 55 | Lanturn |
| Lumineon | super rod | 36 | Oxide | Water Pulse, Captivate, Safeguard, Aqua Ring | Whirlpool 42, U-turn 48, Bounce 53 | Lumineon |
| Lumineon | super rod | 36 | Rewrite | Safeguard, Flip Turn, Aqua Ring, Icy Wind | Aqua Tail 38, Signal Beam 40, Whirlpool 42, Ice Fang 45, U-turn 48, Bounce 53, Air Slash 54, Crunch 56 | Lumineon |
| Octillery | super rod | 39 | Oxide | Focus Energy, Octazooka, Bullet Seed, Wring Out | Signal Beam 42, Ice Beam 48, Hyper Beam 55 | Octillery |
| Octillery | super rod | 39 | Rewrite | Bullet Seed, Round, Charge Beam, Scald | Skitter Smack 40, Signal Beam 42, Ice Beam 48, Psychic 54, Hyper Beam 55 | Octillery |
| Tentacruel | super rod | 39 | Oxide | Wrap, Barrier, Water Pulse, Poison Jab | Screech 42, Hydro Pump 49, Wring Out 55 | Tentacruel |
| Tentacruel | super rod | 39 | Rewrite | Water Pulse, Poison Jab, Aurora Beam, Sludge Bomb | Screech 42, Psybeam 44, Surf 49, Muddy Water 53, Throat Chop 54, Power Gem 56 | Tentacruel |
| Greninja | super rod | 42 | Oxide | Waterfall, Fling, Scald, Dark Pulse | Extrasensory 43, Sludge Wave 47, Gunk Shot 51, Hydro Pump 55 | Greninja |
| Greninja | super rod | 42 | Rewrite | Fling, Shadow Sneak, Scald, Dark Pulse | Extrasensory 43, Sludge Wave 47, Gunk Shot 51, Ice Beam 54, Surf 56 | Greninja |

## Snowpoint City

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 56 | At the cap |
|---|---|---|---|---|---|---|
| Suicune | in-game trade | 1 | Oxide | Bite, Leer | BubbleBeam 8, Gust 22, Aurora Beam 29, Mist 36, Mirror Coat 43, Ice Fang 50 | Suicune |
| Suicune | in-game trade | 1 | Rewrite | Bite | BubbleBeam 8, Gust 22, Aurora Beam 29, Mist 36, Mirror Coat 43, Ice Fang 50, Swagger 54 | Suicune |
| Seel | old rod | 16 to 17 | Oxide | Growl, Water Sport, Icy Wind, Encore | Ice Shard 17, Rest 21, Aqua Ring 23, Aurora Beam 27, Aqua Jet 31, Brine 33; as Dewgong: Sheer Cold 34, Take Down 37, Dive 41, Aqua Tail 43, Ice Beam 47, Safeguard 51 | Dewgong (from 34) |
| Seel | old rod | 16 to 17 | Rewrite | Growl, Water Sport, Icy Wind, Encore | Ice Shard 17, Rest 21, Aqua Ring 23, Aurora Beam 27, Aqua Jet 31, Brine 33; as Dewgong: Signal Beam 34, Take Down 37, Drill Run 40, Dive 41, Aqua Tail 43, Ice Beam 47, Safeguard 51, Muddy Water 54, Bite 56 | Dewgong (from 34) |
| Spheal | old rod | 16 | Oxide | Growl, Water Gun, Encore, Ice Ball | Body Slam 19, Aurora Beam 25; as Sealeo: Swagger 32, Rest 39, Snore 39; as Walrein: Ice Fang 44, Blizzard 52 | Walrein (from 44) |
| Spheal | old rod | 16 | Rewrite | Growl, Water Gun, Encore, Ice Ball | Body Slam 19, Aurora Beam 25, Signal Beam 32; as Sealeo: Swagger 32, Rest 39; as Walrein: Ice Fang 44, Body Press 48, Ice Beam 52, Aqua Tail 54, Crunch 56 | Walrein (from 44) |
| Shellos | old rod | 17 | Oxide | Harden, Water Pulse, Mud Bomb, Hidden Power | Body Slam 29; as Gastrodon: Muddy Water 41, Recover 54 | Gastrodon (from 30) |
| Shellos | old rod | 17 | Rewrite | Harden, Water Pulse, Mud Bomb, Hidden Power | Swagger 22, Body Slam 29; as Gastrodon: AncientPower 33, Earth Power 35, Clear Smog 37, Muddy Water 41, Bulldoze 44, Sludge Bomb 46, Ice Beam 49, Recover 54, Skitter Smack 56 | Gastrodon (from 30) |
| Snorunt | old rod | 18 | Oxide | Leer, Double Team, Bite, Icy Wind | Headbutt 19, Protect 22, Ice Fang 28, Crunch 31, Ice Shard 37; as Glalie: Blizzard 51 | Glalie (from 42) |
| Snorunt | old rod | 18 | Oxide | Leer, Double Team, Bite, Icy Wind | as Froslass: Confuse Ray 19, Ominous Wind 22, Wake-Up Slap 28, Captivate 31, Ice Shard 37, Blizzard 51 | Froslass (from 18) |
| Snorunt | old rod | 18 | Rewrite | Powder Snow, Leer, Bite, Icy Wind | Headbutt 19, Ominous Wind 22, Ice Fang 28, Crunch 31, Draining Kiss 34, Ice Shard 37; as Glalie: Rock Slide 42, Power Gem 44, Confuse Ray 48, Earth Power 53, Ice Punch 54, Shadow Ball 56 | Glalie (from 42) |
| Snorunt | old rod | 18 | Rewrite | Powder Snow, Leer, Bite, Icy Wind | as Froslass: Confuse Ray 19, Ominous Wind 22, Wake-Up Slap 28, Captivate 31, Ice Shard 37, Ice Beam 51 | Froslass (from 18) |
| Seel | good rod | 28 to 30 | Oxide | Ice Shard, Rest, Aqua Ring, Aurora Beam | Aqua Jet 31, Brine 33; as Dewgong: Sheer Cold 34, Take Down 37, Dive 41, Aqua Tail 43, Ice Beam 47, Safeguard 51 | Dewgong (from 34) |
| Seel | good rod | 28 to 30 | Rewrite | Ice Shard, Rest, Aqua Ring, Aurora Beam | Aqua Jet 31, Brine 33; as Dewgong: Signal Beam 34, Take Down 37, Drill Run 40, Dive 41, Aqua Tail 43, Ice Beam 47, Safeguard 51, Muddy Water 54, Bite 56 | Dewgong (from 34) |
| Spheal | good rod | 28 | Oxide | Encore, Ice Ball, Body Slam, Aurora Beam | as Sealeo: Swagger 32, Rest 39, Snore 39; as Walrein: Ice Fang 44, Blizzard 52 | Walrein (from 44) |
| Spheal | good rod | 28 | Rewrite | Encore, Ice Ball, Body Slam, Aurora Beam | Signal Beam 32; as Sealeo: Swagger 32, Rest 39; as Walrein: Ice Fang 44, Body Press 48, Ice Beam 52, Aqua Tail 54, Crunch 56 | Walrein (from 44) |
| Snover | good rod | 30 | Oxide | GrassWhistle, Swagger, Mist, Ice Shard | Ingrain 31, Wood Hammer 36; as Abomasnow: Blizzard 47 | Abomasnow (from 40) |
| Snover | good rod | 30 | Rewrite | Bulldoze, Mist, Ice Shard, Seed Bomb | Rock Tomb 31, Body Press 34, Wood Hammer 36; as Abomasnow: Ice Beam 41, Giga Drain 50, Ice Punch 53, Rock Climb 54, Shadow Ball 56 | Abomasnow (from 40) |
| Lapras | good rod | 32 | Oxide | Water Pulse, Body Slam, Perish Song, Ice Beam | Brine 37, Safeguard 43, Hydro Pump 49, Sheer Cold 55 | Lapras |
| Lapras | good rod | 32 | Rewrite | Water Pulse, Body Slam, Perish Song, Ice Beam | Brine 37, Safeguard 43, Muddy Water 49, Life Dew 54, Drill Run 56 | Lapras |
| Dewgong | super rod | 38 to 41 | Oxide | Aqua Jet, Brine, Sheer Cold, Take Down | Dive 41, Aqua Tail 43, Ice Beam 47, Safeguard 51 | Dewgong |
| Dewgong | super rod | 38 to 41 | Rewrite | Aqua Jet, Brine, Signal Beam, Take Down | Drill Run 40, Dive 41, Aqua Tail 43, Ice Beam 47, Safeguard 51, Muddy Water 54, Bite 56 | Dewgong |
| Sealeo | super rod | 38 | Oxide | Ice Ball, Body Slam, Aurora Beam, Swagger | Rest 39, Snore 39; as Walrein: Ice Fang 44, Blizzard 52 | Walrein (from 44) |
| Sealeo | super rod | 38 | Rewrite | Ice Ball, Body Slam, Aurora Beam, Swagger | Rest 39; as Walrein: Ice Fang 44, Body Press 48, Ice Beam 52, Aqua Tail 54, Crunch 56 | Walrein (from 44) |
| Froslass | super rod | 41 | Oxide | Ominous Wind, Wake-Up Slap, Captivate, Ice Shard | Blizzard 51 | Froslass |
| Froslass | super rod | 41 | Rewrite | Ominous Wind, Wake-Up Slap, Captivate, Ice Shard | Ice Beam 51 | Froslass |
| Lapras | super rod | 44 | Oxide | Perish Song, Ice Beam, Brine, Safeguard | Hydro Pump 49, Sheer Cold 55 | Lapras |
| Lapras | super rod | 44 | Rewrite | Perish Song, Ice Beam, Brine, Safeguard | Muddy Water 49, Life Dew 54, Drill Run 56 | Lapras |

## Twinleaf Town

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 56 | At the cap |
|---|---|---|---|---|---|---|
| Crawdaunt | super rod | 30 | Oxide | BubbleBeam, Protect, Knock Off, Swift | Taunt 34, Night Slash 39, Crabhammer 44, Swords Dance 52 | Crawdaunt |
| Crawdaunt | super rod | 30 | Rewrite | Leer, BubbleBeam, Knock Off, Swift | Taunt 32, Throat Chop 35, Aerial Ace 36, Night Slash 39, X-Scissor 41, Crabhammer 44, Brick Break 48, Swords Dance 52, Rock Tomb 54 | Crawdaunt |
| Lanturn | super rod | 30 | Oxide | Stockpile, Swallow, Spit Up, BubbleBeam | Signal Beam 35, Discharge 40, Aqua Ring 47, Hydro Pump 52 | Lanturn |
| Lanturn | super rod | 30 | Rewrite | Stockpile, Swallow, Spit Up, BubbleBeam | Signal Beam 31, Scald 33, Surf 34, Thunderbolt 37, Discharge 40, Flash Cannon 43, Aqua Ring 47, Muddy Water 52, Volt Switch 54, Dazzling Gleam 55 | Lanturn |
| Floatzel | super rod | 33 | Oxide | Swift, Aqua Jet, Crunch, Agility | Whirlpool 39, Razor Wind 50 | Floatzel |
| Floatzel | super rod | 33 | Rewrite | Aqua Jet, Crunch, Icy Wind, Flip Turn | Waterfall 36, Whirlpool 39, Liquidation 41, Low Sweep 44, Agility 51, Rock Tomb 53, Ice Fang 56 | Floatzel |
| Sharpedo | super rod | 33 | Oxide | Swagger, Assurance, Crunch, Slash | Aqua Jet 34, Taunt 40, Agility 45, Skull Bash 50, Night Slash 56 | Sharpedo |
| Sharpedo | super rod | 33 | Rewrite | Assurance, Crunch, Slash, Aqua Jet | Bug Bite 35, Aerial Ace 37, Taunt 40, Liquidation 41, Agility 45, Skull Bash 50, Poison Fang 54, Night Slash 56 | Sharpedo |
| Swampert | super rod | 36 | Oxide | Mud Shot, Foresight, Mud Bomb, Take Down | Muddy Water 39, Protect 46, Earthquake 52 | Swampert |
| Swampert | super rod | 36 | Rewrite | Foresight, Mud Bomb, Take Down, Waterfall | Muddy Water 39, Aqua Tail 41, Brick Break 44, Poison Jab 48, Earthquake 52, Flip Turn 54, Body Slam 56 | Swampert |

## Valley Windworks

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 56 | At the cap |
|---|---|---|---|---|---|---|
| Crawdaunt | super rod | 30 | Oxide | BubbleBeam, Protect, Knock Off, Swift | Taunt 34, Night Slash 39, Crabhammer 44, Swords Dance 52 | Crawdaunt |
| Crawdaunt | super rod | 30 | Rewrite | Leer, BubbleBeam, Knock Off, Swift | Taunt 32, Throat Chop 35, Aerial Ace 36, Night Slash 39, X-Scissor 41, Crabhammer 44, Brick Break 48, Swords Dance 52, Rock Tomb 54 | Crawdaunt |
| Whiscash | super rod | 30 | Oxide | Mud Bomb, Amnesia, Water Pulse, Magnitude | Rest 33, Snore 33, Aqua Tail 39, Earthquake 45, Future Sight 51 | Whiscash |
| Whiscash | super rod | 30 | Rewrite | Amnesia, Water Pulse, Magnitude, Bulldoze | Rest 33, Zen Headbutt 36, Aqua Tail 39, Earth Power 40, Wild Charge 42, Earthquake 45, Future Sight 51, Spark 54, Ice Beam 56 | Whiscash |
| Lanturn | super rod | 33 | Oxide | Stockpile, Swallow, Spit Up, BubbleBeam | Signal Beam 35, Discharge 40, Aqua Ring 47, Hydro Pump 52 | Lanturn |
| Lanturn | super rod | 33 | Rewrite | Spit Up, BubbleBeam, Signal Beam, Scald | Surf 34, Thunderbolt 37, Discharge 40, Flash Cannon 43, Aqua Ring 47, Muddy Water 52, Volt Switch 54, Dazzling Gleam 55 | Lanturn |
| Sharpedo | super rod | 33 | Oxide | Swagger, Assurance, Crunch, Slash | Aqua Jet 34, Taunt 40, Agility 45, Skull Bash 50, Night Slash 56 | Sharpedo |
| Sharpedo | super rod | 33 | Rewrite | Assurance, Crunch, Slash, Aqua Jet | Bug Bite 35, Aerial Ace 37, Taunt 40, Liquidation 41, Agility 45, Skull Bash 50, Poison Fang 54, Night Slash 56 | Sharpedo |
| Greninja | super rod | 36 | Oxide | Acrobatics, Low Kick, Waterfall, Fling | Scald 37, Dark Pulse 40, Extrasensory 43, Sludge Wave 47, Gunk Shot 51, Hydro Pump 55 | Greninja |
| Greninja | super rod | 36 | Rewrite | Low Kick, Waterfall, Fling, Shadow Sneak | Scald 37, Dark Pulse 40, Extrasensory 43, Sludge Wave 47, Gunk Shot 51, Ice Beam 54, Surf 56 | Greninja |

## Honey trees

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 56 | At the cap |
|---|---|---|---|---|---|---|
| Frosmoth | honey | 32 | Oxide | Defog, FeatherDance, Aurora Beam, Bug Buzz | Aurora Veil 36, Blizzard 40, Tailwind 44, Wide Guard 48, Quiver Dance 52 | Frosmoth |
| Frosmoth | honey | 32 | Rewrite | Attract, Stun Spore, Infestation, Bug Buzz | Defog 33, Aurora Beam 34, Aurora Veil 36, Ice Beam 40, Tailwind 44, Wide Guard 48, Quiver Dance 52, Air Slash 54, Giga Drain 56 | Frosmoth |
| Galvantula | honey | 32 | Oxide | Bug Bite, Gastro Acid, Struggle Bug, Discharge | Signal Beam 35, Energy Ball 39, Sucker Punch 43, Thunderbolt 48, Bug Buzz 51, Thunder 55 | Galvantula |
| Galvantula | honey | 32 | Rewrite | Gastro Acid, Struggle Bug, Discharge, Snarl | Signal Beam 35, Energy Ball 39, Swift 40, Giga Drain 41, Sucker Punch 43, Thunderbolt 48, Bug Buzz 51, Screech 54, Agility 56 | Galvantula |
| Heracross | honey | 32 | Oxide | Aerial Ace, Brick Break, Counter, Take Down | Close Combat 37, Reversal 43, Feint 49, Megahorn 55 | Heracross |
| Heracross | honey | 32 | Rewrite | Pounce, Counter, Rock Tomb, Take Down | Leech Life 34, Close Combat 37, Throat Chop 40, Reversal 43, Skitter Smack 46, Lunge 49, Bulldoze 54, Megahorn 55 | Heracross |
| Larvesta | honey | 32 | Oxide | String Shot, Flame Charge, Struggle Bug, Flame Wheel | Bug Bite 40, Take Down 50 | Larvesta; Volcarona in HQ |
| Larvesta | honey | 32 | Rewrite | Flame Charge, Struggle Bug, U-turn, Flame Wheel | Bug Bite 40, Fire Spin 41, Roost 45, Take Down 50, Poison Jab 53, Skitter Smack 54, Lunge 56 | Larvesta; Volcarona in HQ |
| Leavanny | honey | 32 | Oxide | Razor Leaf, Struggle Bug, Fell Stinger, Helping Hand | Leaf Blade 36, X-Scissor 39, Entrainment 43, Swords Dance 46, Leaf Storm 50 | Leavanny |
| Leavanny | honey | 32 | Rewrite | Razor Leaf, Struggle Bug, Fell Stinger, Helping Hand | Leaf Blade 36, X-Scissor 39, Poison Jab 41, Entrainment 43, Swords Dance 46, Leaf Storm 50, Shadow Claw 54, Lunge 56 | Leavanny |
| Scizor | honey | 32 | Oxide | Agility, Metal Claw, Fury Cutter, Slash | Razor Wind 33, Iron Defense 37, X-Scissor 41, Night Slash 45, Double Hit 49, Iron Head 53 | Scizor |
| Scizor | honey | 32 | Rewrite | Agility, Metal Claw, Fury Cutter, Slash | Skitter Smack 34, Iron Defense 37, X-Scissor 41, Night Slash 45, Double Hit 49, Iron Head 53, Leech Life 54, Brick Break 55 | Scizor |
| Shiftry | honey | 32 | Oxide | Faint Attack, Whirlwind, Nasty Plot, Razor Leaf | Leaf Storm 49 | Shiftry |
| Shiftry | honey | 32 | Rewrite | Faint Attack, Whirlwind, Nasty Plot, Razor Leaf | Leaf Blade 34, Leech Life 40, Extrasensory 43, Leaf Storm 49, Rock Slide 53, Throat Chop 54, Sucker Punch 56 | Shiftry |
| Snorlax | honey | 32 | Oxide | Yawn, Rest, Snore, Sleep Talk | Body Slam 33, Block 36, Rollout 41, Crunch 44, Giga Impact 49 | Snorlax |
| Snorlax | honey | 32 | Rewrite | Tackle, Amnesia, Lick, Yawn | Body Slam 33, Block 36, Bulldoze 38, Rollout 41, Crunch 44, Giga Impact 49, Body Press 53, Slam 56 | Snorlax |
| Toucannon | honey | 32 | Oxide | Pluck, Roost, Fury Attack, Screech | Drill Peck 34, Bullet Seed 40, FeatherDance 44, Hyper Voice 50 | Toucannon |
| Toucannon | honey | 32 | Rewrite | Pluck, Roost, Screech, Drill Peck | Smack Down 35, Facade 37, Bullet Seed 40, Throat Chop 42, FeatherDance 44, Take Down 47, Hyper Voice 50, Brick Break 54, Temper Flare 56 | Toucannon |
| Vespiquen | honey | 32 | Oxide | Power Gem, Heal Order, Toxic, Slash | Captivate 33, Attack Order 37, Swagger 39, Destiny Bond 43 | Vespiquen |
| Vespiquen | honey | 32 | Rewrite | Bug Bite, Air Cutter, Toxic, Slash | Captivate 33, Pounce 35, Attack Order 37, Swagger 39, U-turn 41, Air Slash 44, Poison Jab 48, Psychic Noise 53, Take Down 54, Sludge Bomb 56 | Vespiquen |
| Vikavolt | honey | 32 | Oxide | Thunderbolt, Crunch, Bite, Spark | Signal Beam 36, Discharge 48, Bug Buzz 55 | Vikavolt |
| Vikavolt | honey | 32 | Rewrite | Thunderbolt, Crunch, Bite, Spark | Signal Beam 36, Pollen Puff 40, Discharge 48, Energy Ball 54, Bug Buzz 55 | Vikavolt |
| Yanma | honey | 32 | Oxide | Detect, Supersonic, Uproar, Pursuit | AncientPower 33; as Yanmega: Feint 38, Slash 43, Screech 46, U-turn 49, Air Slash 54 | Yanmega (from 35) |
| Yanma | honey | 32 | Rewrite | SonicBoom, Roost, Uproar, Pursuit | AncientPower 33, Air Cutter 34, Signal Beam 35; as Yanmega: Hypnosis 38, Ominous Wind 40, Slash 43, Screech 46, U-turn 49, Psychic Noise 51, Air Slash 54, Pollen Puff 55 | Yanmega (from 35) |

# Candice's split: what each catch knows and learns

Written by `tools/oxide/balance/learncheck.py sheets` for check 6 of the learnset baseline (`docs/oxide/learnset-checks.md`). One table per capture area first offered in Candice's split, whose cap is 56. Each Pokemon is read at the lowest level it is found at there. "Knows at capture" is the last four moves its list gives by that level; "learns by level-up" is every entry it reaches after capture up to 56, evolving on time, with each later stage's moves under its name; "at the cap" is the stage it can be by then and the next one after. A row marked v3 shows learnset v3 (unlanded, `origin/balance-learngen-v2`) where it differs from Oxide's lists; a row marked both is the same in each. Relearner-only moves and egg moves are left out. Nothing here is in the game data.

## Acuity Lakefront

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 56 | At the cap |
|---|---|---|---|---|---|---|
| Sneasel | wild | 32 to 35 | Oxide | Faint Attack, Fury Swipes, Agility, Icy Wind | Slash 35, Metal Claw 42, Ice Shard 49 | Sneasel; Weavile in HQ |
| Sneasel | wild | 32 to 35 | v3 | Faint Attack, Fury Swipes, Agility, Icy Wind | Slash 35, Ice Shard 49 | Sneasel; Weavile in HQ |
| Absol | wild | 33 to 35 | Oxide | Pursuit, Swords Dance, Bite, Double Team | Slash 36, Future Sight 41, Sucker Punch 44, Detect 49, Night Slash 52 | Absol |
| Absol | wild | 33 to 35 | v3 | Pursuit, Swords Dance, Bite, Double Team | Slash 36, Future Sight 41, Sucker Punch 44, Detect 49 | Absol |
| Alolan Ninetales | wild | 33 | Oxide | Tail Whip, Disable, Ice Shard, Safeguard | nothing | Alolan Ninetales |
| Alolan Ninetales | wild | 33 | v3 | Safeguard, Icy Wind, Aurora Beam, Draining Kiss | Ice Beam 45 | Alolan Ninetales |
| Delibird | wild | 33 | both | Present | nothing | Delibird |
| Frosmoth | wild | 33 to 34 | Oxide | Defog, FeatherDance, Aurora Beam, Bug Buzz | Aurora Veil 36, Blizzard 40, Tailwind 44, Wide Guard 48, Quiver Dance 52 | Frosmoth |
| Frosmoth | wild | 33 to 34 | v3 | Defog, FeatherDance, Aurora Beam, Bug Buzz | Aurora Veil 36, Tailwind 44, Blizzard 45, Wide Guard 48, Quiver Dance 52 | Frosmoth |
| Seel | wild | 33 | Oxide | Aqua Ring, Aurora Beam, Aqua Jet, Brine | as Dewgong: Sheer Cold 34, Take Down 37, Dive 41, Aqua Tail 43, Ice Beam 47, Safeguard 51 | Dewgong (from 34) |
| Seel | wild | 33 | v3 | Aqua Ring, Aurora Beam, Aqua Jet, Brine | as Dewgong: Sheer Cold 34, Take Down 37, Dive 41, Aqua Tail 43, Safeguard 51, Ice Beam 53 | Dewgong (from 34) |
| Snover | wild | 33 to 34 | Oxide | Swagger, Mist, Ice Shard, Ingrain | Wood Hammer 36; as Abomasnow: Blizzard 47 | Abomasnow (from 40) |
| Snover | wild | 33 to 34 | v3 | Swagger, Mist, Ice Shard, Ingrain | Wood Hammer 39; as Abomasnow: Blizzard 47, Wood Hammer 53 | Abomasnow (from 40) |
| Snorunt | wild | 34 | both | Headbutt, Protect, Ice Fang, Crunch | Ice Shard 37; as Glalie: Blizzard 51 | Glalie (from 42) |
| Snorunt | wild | 34 | both | Headbutt, Protect, Ice Fang, Crunch | as Froslass: Ice Shard 37, Blizzard 51 | Froslass (from 34) |
| Jynx | wild | 35 | both | Mean Look, Fake Tears, Wake-Up Slap, Avalanche | Body Slam 39, Wring Out 44, Perish Song 49, Blizzard 55 | Jynx |

## Canalave City

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 56 | At the cap |
|---|---|---|---|---|---|---|
| Gastrodon | super rod | 36 | Oxide | Water Pulse, Mud Bomb, Hidden Power, Body Slam | Muddy Water 41, Recover 54 | Gastrodon |
| Gastrodon | super rod | 36 | v3 | Water Pulse, Mud Bomb, Hidden Power, Body Slam | Muddy Water 39, Earthquake 44, Recover 54 | Gastrodon |
| Lumineon | super rod | 36 | Oxide | Water Pulse, Captivate, Safeguard, Aqua Ring | Whirlpool 42, U-turn 48, Bounce 53 | Lumineon |
| Lumineon | super rod | 36 | v3 | Water Pulse, Captivate, Safeguard, Aqua Ring | U-turn 48, Bounce 53 | Lumineon |
| Jellicent | super rod | 39 | Oxide | Confuse Ray, Hex, Brine, Pain Split | Destiny Bond 45, Shadow Ball 51, Scald 55 | Jellicent |
| Jellicent | super rod | 39 | v3 | Confuse Ray, Hex, Brine, Pain Split | Destiny Bond 45, Shadow Ball 52, Scald 53 | Jellicent |
| Toxapex | super rod | 42 | both | Spike Cannon, Pin Missile, Toxic, Venom Drench | Poison Jab 43, Liquidation 45 | Toxapex |

## Celestic Town

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 56 | At the cap |
|---|---|---|---|---|---|---|
| Milotic | super rod | 36 | both | Twister, Recover, Captivate, Aqua Tail | Hydro Pump 37, Attract 41, Safeguard 45, Aqua Ring 49 | Milotic |
| Whiscash | super rod | 36 | Oxide | Water Pulse, Magnitude, Rest, Snore | Aqua Tail 39, Earthquake 45, Future Sight 51 | Whiscash |
| Whiscash | super rod | 36 | v3 | Amnesia, Water Pulse, Magnitude, Rest | Aqua Tail 39, Earthquake 45, Future Sight 51 | Whiscash |
| Crawdaunt | super rod | 39 | both | Knock Off, Swift, Taunt, Night Slash | Crabhammer 44, Swords Dance 52 | Crawdaunt |
| Lanturn | super rod | 39 to 42 | Oxide | Swallow, Spit Up, BubbleBeam, Signal Beam | Discharge 40, Aqua Ring 47, Hydro Pump 52 | Lanturn |
| Lanturn | super rod | 39 to 42 | v3 | Swallow, Spit Up, BubbleBeam, Signal Beam | Aqua Ring 47, Hydro Pump 52, Discharge 53 | Lanturn |

## Eterna City

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 56 | At the cap |
|---|---|---|---|---|---|---|
| Lanturn | super rod | 30 | Oxide | Stockpile, Swallow, Spit Up, BubbleBeam | Signal Beam 35, Discharge 40, Aqua Ring 47, Hydro Pump 52 | Lanturn |
| Lanturn | super rod | 30 | v3 | Stockpile, Swallow, Spit Up, BubbleBeam | Signal Beam 35, Aqua Ring 47, Hydro Pump 52, Discharge 53 | Lanturn |
| Sharpedo | super rod | 30 | Oxide | Swagger, Assurance, Crunch, Slash | Aqua Jet 34, Taunt 40, Agility 45, Skull Bash 50, Night Slash 56 | Sharpedo |
| Sharpedo | super rod | 30 | v3 | Swagger, Assurance, Crunch, Slash | Aqua Jet 34, Taunt 40, Agility 45, Night Slash 56 | Sharpedo |
| Alomomola | super rod | 33 | Oxide | Protect, Water Pulse, Wake-Up Slap, Soak | Wish 37, Brine 41, Safeguard 45, Whirlpool 49, Helping Hand 53 | Alomomola |
| Alomomola | super rod | 33 | v3 | Protect, Water Pulse, Wake-Up Slap, Soak | Wish 37, Brine 41, Safeguard 45, Helping Hand 53 | Alomomola |
| Floatzel | super rod | 33 to 36 | Oxide | Swift, Aqua Jet, Crunch, Agility | Whirlpool 39, Razor Wind 50 | Floatzel |
| Floatzel | super rod | 33 to 36 | v3 | Swift, Aqua Jet, Crunch, Agility | nothing | Floatzel |

## Fuego Ironworks

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 56 | At the cap |
|---|---|---|---|---|---|---|
| Seaking | super rod | 36 | Oxide | Water Pulse, Flail, Aqua Ring, Fury Attack | Waterfall 40, Horn Drill 47, Agility 56 | Seaking |
| Seaking | super rod | 36 | v3 | Horn Attack, Water Pulse, Flail, Aqua Ring | Waterfall 40, Horn Drill 47, Agility 56 | Seaking |
| Whiscash | super rod | 36 | Oxide | Water Pulse, Magnitude, Rest, Snore | Aqua Tail 39, Earthquake 45, Future Sight 51 | Whiscash |
| Whiscash | super rod | 36 | v3 | Amnesia, Water Pulse, Magnitude, Rest | Aqua Tail 39, Earthquake 45, Future Sight 51 | Whiscash |
| Crawdaunt | super rod | 39 | both | Knock Off, Swift, Taunt, Night Slash | Crabhammer 44, Swords Dance 52 | Crawdaunt |
| Lanturn | super rod | 39 | Oxide | Swallow, Spit Up, BubbleBeam, Signal Beam | Discharge 40, Aqua Ring 47, Hydro Pump 52 | Lanturn |
| Lanturn | super rod | 39 | v3 | Swallow, Spit Up, BubbleBeam, Signal Beam | Aqua Ring 47, Hydro Pump 52, Discharge 53 | Lanturn |
| Relicanth | super rod | 42 | Oxide | Rock Tomb, Yawn, Take Down, Mud Sport | AncientPower 43, Double-Edge 50 | Relicanth |
| Relicanth | super rod | 42 | v3 | Yawn, Take Down, Mud Sport, Dive | AncientPower 43, Double-Edge 50, Earthquake 53 | Relicanth |

## Great Marsh

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 56 | At the cap |
|---|---|---|---|---|---|---|
| Araquanid | super rod | 35 to 38 | Oxide | BubbleBeam, Bug Bite, Headbutt, Soak | Dive 36, Lunge 41, Scald 48, Hydro Pump 51, Liquidation 55 | Araquanid |
| Araquanid | super rod | 35 to 38 | v3 | BubbleBeam, Bug Bite, Headbutt, Soak | Dive 36, Lunge 41, Hydro Pump 51, Liquidation 55 | Araquanid |
| Crawdaunt | super rod | 35 to 38 | both | Protect, Knock Off, Swift, Taunt | Night Slash 39, Crabhammer 44, Swords Dance 52 | Crawdaunt |
| Jellicent | super rod | 35 to 38 | Oxide | Imprison, Confuse Ray, Hex, Brine | Pain Split 39, Destiny Bond 45, Shadow Ball 51, Scald 55 | Jellicent |
| Jellicent | super rod | 35 to 38 | v3 | Imprison, Confuse Ray, Hex, Brine | Pain Split 39, Destiny Bond 45, Shadow Ball 52, Scald 53 | Jellicent |
| Kingdra | super rod | 35 | both | BubbleBeam, Agility, Twister, Brine | Hydro Pump 40, Dragon Dance 48 | Kingdra |
| Lombre | super rod | 35 | Oxide | Fury Swipes, Water Sport, BubbleBeam, Zen Headbutt | nothing | Ludicolo (from 35) |
| Lombre | super rod | 35 | v3 | Fury Swipes, Water Sport, BubbleBeam, Zen Headbutt | as Ludicolo: Hydro Pump 45 | Ludicolo (from 35) |
| Ludicolo | super rod | 35 to 38 | Oxide | Astonish, Growl, Mega Drain, Nature Power | nothing | Ludicolo |
| Ludicolo | super rod | 35 to 38 | v3 | Growl, Mega Drain, Nature Power | Hydro Pump 45 | Ludicolo |
| Sharpedo | super rod | 35 | Oxide | Assurance, Crunch, Slash, Aqua Jet | Taunt 40, Agility 45, Skull Bash 50, Night Slash 56 | Sharpedo |
| Sharpedo | super rod | 35 | v3 | Assurance, Crunch, Slash, Aqua Jet | Taunt 40, Agility 45, Night Slash 56 | Sharpedo |
| Wailmer | super rod | 35 | Oxide | Mist, Rest, Brine, Water Spout | Amnesia 37; as Wailord: Dive 46, Bounce 54 | Wailord (from 40) |
| Wailmer | super rod | 35 | v3 | Water Pulse, Mist, Rest, Brine | Amnesia 37; as Wailord: Dive 46, Bounce 54 | Wailord (from 40) |
| Kingler | super rod | 38 | both | Metal Claw, Stomp, Protect, Guillotine | Slam 44, Brine 51, Crabhammer 56 | Kingler |
| Quagsire | super rod | 38 | Oxide | Mud Bomb, Amnesia, Yawn, Earthquake | Mist 48, Haze 48, Muddy Water 53 | Quagsire |
| Quagsire | super rod | 38 | v3 | Slam, Mud Bomb, Amnesia, Yawn | Earthquake 44, Mist 48, Haze 48, Muddy Water 53 | Quagsire |
| Qwilfish | super rod | 38 to 41 | both | Spit Up, Revenge, Brine, Pin Missile | Take Down 41, Aqua Tail 45, Poison Jab 49, Destiny Bond 53 | Qwilfish |
| Whiscash | super rod | 38 | Oxide | Water Pulse, Magnitude, Rest, Snore | Aqua Tail 39, Earthquake 45, Future Sight 51 | Whiscash |
| Whiscash | super rod | 38 | v3 | Amnesia, Water Pulse, Magnitude, Rest | Aqua Tail 39, Earthquake 45, Future Sight 51 | Whiscash |
| Corsola | super rod | 41 | Oxide | Lucky Chant, AncientPower, Aqua Ring, Spike Cannon | Power Gem 44, Mirror Coat 48, Earth Power 53 | Corsola |
| Corsola | super rod | 41 | v3 | AncientPower, Rock Blast, Aqua Ring, Spike Cannon | Power Gem 44, Mirror Coat 48, Earth Power 53 | Corsola |
| Feraligatr | super rod | 41 | both | Flail, Agility, Crunch, Slash | Screech 45, Thrash 50 | Feraligatr |
| Greninja | super rod | 41 | both | Waterfall, Fling, Scald, Dark Pulse | Extrasensory 43, Sludge Wave 47, Gunk Shot 51, Hydro Pump 55 | Greninja |
| Pelipper | super rod | 41 | Oxide | Roost, Stockpile, Swallow, Spit Up | Fling 43, Tailwind 50 | Pelipper |
| Pelipper | super rod | 41 | v3 | Protect, Stockpile, Swallow, Spit Up | Fling 43, Tailwind 50, Roost 53 | Pelipper |

## Iron Island

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 56 | At the cap |
|---|---|---|---|---|---|---|
| Gastrodon | super rod | 36 | Oxide | Water Pulse, Mud Bomb, Hidden Power, Body Slam | Muddy Water 41, Recover 54 | Gastrodon |
| Gastrodon | super rod | 36 | v3 | Water Pulse, Mud Bomb, Hidden Power, Body Slam | Muddy Water 39, Earthquake 44, Recover 54 | Gastrodon |
| Jellicent | super rod | 36 | Oxide | Imprison, Confuse Ray, Hex, Brine | Pain Split 39, Destiny Bond 45, Shadow Ball 51, Scald 55 | Jellicent |
| Jellicent | super rod | 36 | v3 | Imprison, Confuse Ray, Hex, Brine | Pain Split 39, Destiny Bond 45, Shadow Ball 52, Scald 53 | Jellicent |
| Lanturn | super rod | 39 | Oxide | Swallow, Spit Up, BubbleBeam, Signal Beam | Discharge 40, Aqua Ring 47, Hydro Pump 52 | Lanturn |
| Lanturn | super rod | 39 | v3 | Swallow, Spit Up, BubbleBeam, Signal Beam | Aqua Ring 47, Hydro Pump 52, Discharge 53 | Lanturn |
| Lumineon | super rod | 39 to 42 | Oxide | Water Pulse, Captivate, Safeguard, Aqua Ring | Whirlpool 42, U-turn 48, Bounce 53 | Lumineon |
| Lumineon | super rod | 39 to 42 | v3 | Water Pulse, Captivate, Safeguard, Aqua Ring | U-turn 48, Bounce 53 | Lumineon |

## Lake Acuity

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 56 | At the cap |
|---|---|---|---|---|---|---|
| Chinchou | old rod | 16 | Oxide | Supersonic, Thunder Wave, Flail, Water Gun | Confuse Ray 17, Spark 20, Take Down 23; as Lanturn: Stockpile 27, Swallow 27, Spit Up 27, BubbleBeam 30, Signal Beam 35, Discharge 40, Aqua Ring 47, Hydro Pump 52 | Lanturn (from 27) |
| Chinchou | old rod | 16 | v3 | Supersonic, Thunder Wave, Flail, Water Gun | Confuse Ray 17, Spark 20, Take Down 23; as Lanturn: Stockpile 27, Swallow 27, Spit Up 27, BubbleBeam 30, Signal Beam 35, Aqua Ring 47, Hydro Pump 52, Discharge 53 | Lanturn (from 27) |
| Clamperl | old rod | 16 | Oxide | Clamp, Water Gun, Whirlpool, Iron Defense | as Huntail: Scary Face 19, Ice Fang 24, Brine 28, Baton Pass 33, Dive 37, Crunch 42, Aqua Tail 46, Hydro Pump 51 | Huntail (from 16) |
| Clamperl | old rod | 16 | Oxide | Clamp, Water Gun, Whirlpool, Iron Defense | as Gorebyss: Amnesia 19, Aqua Ring 24, Captivate 28, Baton Pass 33, Dive 37, Psychic 42, Aqua Tail 46, Hydro Pump 51 | Gorebyss (from 16) |
| Clamperl | old rod | 16 | v3 | Water Gun, Iron Defense | as Huntail: Scary Face 19, Brine 28, Ice Fang 32, Baton Pass 33, Dive 37, Crunch 42, Aqua Tail 46, Hydro Pump 51 | Huntail (from 16) |
| Clamperl | old rod | 16 | v3 | Water Gun, Iron Defense | as Gorebyss: Amnesia 19, Aqua Ring 24, Captivate 28, Baton Pass 33, Dive 37, Psychic 42, Aqua Tail 46, Hydro Pump 51 | Gorebyss (from 16) |
| Barboach | old rod | 17 | Oxide | Mud Sport, Water Sport, Water Gun, Mud Bomb | Amnesia 18, Water Pulse 22, Magnitude 26; as Whiscash: Rest 33, Snore 33, Aqua Tail 39, Earthquake 45, Future Sight 51 | Whiscash (from 30) |
| Barboach | old rod | 17 | v3 | Mud Sport, Water Sport, Water Gun, Mud Bomb | Amnesia 18, Water Pulse 22, Magnitude 26; as Whiscash: Rest 33, Aqua Tail 39, Earthquake 45, Future Sight 51 | Whiscash (from 30) |
| Goldeen | old rod | 17 | Oxide | Water Sport, Supersonic, Horn Attack, Water Pulse | Flail 21, Aqua Ring 27, Fury Attack 31; as Seaking: Waterfall 40, Horn Drill 47, Agility 56 | Seaking (from 33) |
| Goldeen | old rod | 17 | v3 | Water Sport, Supersonic, Horn Attack, Water Pulse | Flail 21, Aqua Ring 27; as Seaking: Waterfall 40, Horn Drill 47, Agility 56 | Seaking (from 33) |
| Frogadier | old rod | 18 | Oxide | Quick Attack, Lick, Water Pulse, Icy Wind | Faint Attack 20, Acrobatics 22, Low Kick 25, Waterfall 30, Fling 35; as Greninja: Scald 37, Dark Pulse 40, Extrasensory 43, Sludge Wave 47, Gunk Shot 51, Hydro Pump 55 | Greninja (from 36) |
| Frogadier | old rod | 18 | v3 | Quick Attack, Lick, Water Pulse, Icy Wind | Faint Attack 20, Acrobatics 22, Low Kick 25, Fling 35; as Greninja: Water Shuriken on evolving, Night Slash on evolving, Scald 37, Dark Pulse 40, Extrasensory 43, Sludge Wave 47, Gunk Shot 51, Hydro Pump 55 | Greninja (from 36) |
| Barboach | good rod | 28 | Oxide | Mud Bomb, Amnesia, Water Pulse, Magnitude | as Whiscash: Rest 33, Snore 33, Aqua Tail 39, Earthquake 45, Future Sight 51 | Whiscash (from 30) |
| Barboach | good rod | 28 | v3 | Mud Bomb, Amnesia, Water Pulse, Magnitude | as Whiscash: Rest 33, Aqua Tail 39, Earthquake 45, Future Sight 51 | Whiscash (from 30) |
| Feebas | good rod | 28 | Oxide | Splash, Tackle | Flail 30; as Milotic: Hydro Pump 37, Attract 41, Safeguard 45, Aqua Ring 49 | Milotic (from 30) |
| Feebas | good rod | 28 | v3 | Tackle, Water Gun | Flail 30; as Milotic: Hydro Pump 37, Attract 41, Safeguard 45, Aqua Ring 49 | Milotic (from 30) |
| Corphish | good rod | 30 | both | Leer, BubbleBeam, Protect, Knock Off | as Crawdaunt: Taunt 34, Night Slash 39, Crabhammer 44, Swords Dance 52 | Crawdaunt (from 31) |
| Wailmer | good rod | 30 | Oxide | Astonish, Water Pulse, Mist, Rest | Brine 31, Water Spout 34, Amnesia 37; as Wailord: Dive 46, Bounce 54 | Wailord (from 40) |
| Wailmer | good rod | 30 | v3 | Growl, Water Pulse, Mist, Rest | Brine 31, Amnesia 37; as Wailord: Dive 46, Bounce 54 | Wailord (from 40) |
| Lapras | good rod | 32 | Oxide | Water Pulse, Body Slam, Perish Song, Ice Beam | Brine 37, Safeguard 43, Hydro Pump 49, Sheer Cold 55 | Lapras |
| Lapras | good rod | 32 | v3 | Ice Shard, Water Pulse, Body Slam, Perish Song | Brine 37, Ice Beam 39, Safeguard 43, Hydro Pump 49, Sheer Cold 55 | Lapras |
| Floatzel | surf | 34 | Oxide | Swift, Aqua Jet, Crunch, Agility | Whirlpool 39, Razor Wind 50 | Floatzel |
| Floatzel | surf | 34 | v3 | Swift, Aqua Jet, Crunch, Agility | nothing | Floatzel |
| Jellicent | surf | 34 | Oxide | Imprison, Confuse Ray, Hex, Brine | Pain Split 39, Destiny Bond 45, Shadow Ball 51, Scald 55 | Jellicent |
| Jellicent | surf | 34 | v3 | Imprison, Confuse Ray, Hex, Brine | Pain Split 39, Destiny Bond 45, Shadow Ball 52, Scald 53 | Jellicent |
| Buizel | surf | 37 | Oxide | Swift, Aqua Jet, Agility, Whirlpool | as Floatzel: Whirlpool 39, Razor Wind 50 | Floatzel (from 38) |
| Buizel | surf | 37 | v3 | Pursuit, Swift, Aqua Jet, Agility | nothing | Floatzel (from 38) |
| Dewgong | surf | 37 | Oxide | Aqua Jet, Brine, Sheer Cold, Take Down | Dive 41, Aqua Tail 43, Ice Beam 47, Safeguard 51 | Dewgong |
| Dewgong | surf | 37 | v3 | Aqua Jet, Brine, Sheer Cold, Take Down | Dive 41, Aqua Tail 43, Safeguard 51, Ice Beam 53 | Dewgong |
| Crawdaunt | super rod | 38 | both | Protect, Knock Off, Swift, Taunt | Night Slash 39, Crabhammer 44, Swords Dance 52 | Crawdaunt |
| Milotic | super rod | 38 | both | Recover, Captivate, Aqua Tail, Hydro Pump | Attract 41, Safeguard 45, Aqua Ring 49 | Milotic |
| Snorunt | wild | 38 to 41 | both | Protect, Ice Fang, Crunch, Ice Shard | as Glalie: Blizzard 51 | Glalie (from 42) |
| Snorunt | wild | 38 to 41 | both | Protect, Ice Fang, Crunch, Ice Shard | as Froslass: Blizzard 51 | Froslass (from 38) |
| Absol | wild | 39 to 40 | Oxide | Swords Dance, Bite, Double Team, Slash | Future Sight 41, Sucker Punch 44, Detect 49, Night Slash 52 | Absol |
| Absol | wild | 39 to 40 | v3 | Swords Dance, Bite, Double Team, Slash | Future Sight 41, Sucker Punch 44, Detect 49 | Absol |
| Alolan Ninetales | wild | 39 | Oxide | Tail Whip, Disable, Ice Shard, Safeguard | nothing | Alolan Ninetales |
| Alolan Ninetales | wild | 39 | v3 | Safeguard, Icy Wind, Aurora Beam, Draining Kiss | Ice Beam 45 | Alolan Ninetales |
| Frosmoth | wild | 39 | Oxide | FeatherDance, Aurora Beam, Bug Buzz, Aurora Veil | Blizzard 40, Tailwind 44, Wide Guard 48, Quiver Dance 52 | Frosmoth |
| Frosmoth | wild | 39 | v3 | FeatherDance, Aurora Beam, Bug Buzz, Aurora Veil | Tailwind 44, Blizzard 45, Wide Guard 48, Quiver Dance 52 | Frosmoth |
| Jynx | wild | 39 | both | Fake Tears, Wake-Up Slap, Avalanche, Body Slam | Wring Out 44, Perish Song 49, Blizzard 55 | Jynx |
| Weavile | wild | 39 to 41 | Oxide | Nasty Plot, Icy Wind, Night Slash, Fling | Metal Claw 42, Dark Pulse 49 | Weavile |
| Weavile | wild | 39 to 41 | v3 | Nasty Plot, Icy Wind, Night Slash, Fling | Dark Pulse 49 | Weavile |
| Abomasnow | wild | 40 to 41 | Oxide | Mist, Ice Shard, Ingrain, Wood Hammer | Blizzard 47 | Abomasnow |
| Abomasnow | wild | 40 to 41 | v3 | Swagger, Mist, Ice Shard, Ingrain | Blizzard 47, Wood Hammer 53 | Abomasnow |
| Galarian Mr Mime | wild | 40 | both | Psybeam, Hypnosis, Mirror Coat, Sucker Punch | as Mr. Rime: Freeze-Dry 44, Psychic 48, Teeter Dance 52 | Mr. Rime (from 42) |
| Lapras | surf | 40 | Oxide | Body Slam, Perish Song, Ice Beam, Brine | Safeguard 43, Hydro Pump 49, Sheer Cold 55 | Lapras |
| Lapras | surf | 40 | v3 | Body Slam, Perish Song, Brine, Ice Beam | Safeguard 43, Hydro Pump 49, Sheer Cold 55 | Lapras |
| Lanturn | super rod | 41 | Oxide | Spit Up, BubbleBeam, Signal Beam, Discharge | Aqua Ring 47, Hydro Pump 52 | Lanturn |
| Lanturn | super rod | 41 | v3 | Swallow, Spit Up, BubbleBeam, Signal Beam | Aqua Ring 47, Hydro Pump 52, Discharge 53 | Lanturn |
| Qwilfish | super rod | 41 | both | Revenge, Brine, Pin Missile, Take Down | Aqua Tail 45, Poison Jab 49, Destiny Bond 53 | Qwilfish |
| Gorebyss | super rod | 44 | both | Captivate, Baton Pass, Dive, Psychic | Aqua Tail 46, Hydro Pump 51 | Gorebyss |

## Lake Valor

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 56 | At the cap |
|---|---|---|---|---|---|---|
| Milotic | super rod | 36 | both | Twister, Recover, Captivate, Aqua Tail | Hydro Pump 37, Attract 41, Safeguard 45, Aqua Ring 49 | Milotic |
| Whiscash | super rod | 36 | Oxide | Water Pulse, Magnitude, Rest, Snore | Aqua Tail 39, Earthquake 45, Future Sight 51 | Whiscash |
| Whiscash | super rod | 36 | v3 | Amnesia, Water Pulse, Magnitude, Rest | Aqua Tail 39, Earthquake 45, Future Sight 51 | Whiscash |
| Crawdaunt | super rod | 39 | both | Knock Off, Swift, Taunt, Night Slash | Crabhammer 44, Swords Dance 52 | Crawdaunt |
| Lanturn | super rod | 39 | Oxide | Swallow, Spit Up, BubbleBeam, Signal Beam | Discharge 40, Aqua Ring 47, Hydro Pump 52 | Lanturn |
| Lanturn | super rod | 39 | v3 | Swallow, Spit Up, BubbleBeam, Signal Beam | Aqua Ring 47, Hydro Pump 52, Discharge 53 | Lanturn |
| Corsola | super rod | 42 | Oxide | Lucky Chant, AncientPower, Aqua Ring, Spike Cannon | Power Gem 44, Mirror Coat 48, Earth Power 53 | Corsola |
| Corsola | super rod | 42 | v3 | AncientPower, Rock Blast, Aqua Ring, Spike Cannon | Power Gem 44, Mirror Coat 48, Earth Power 53 | Corsola |

## Lake Verity

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 56 | At the cap |
|---|---|---|---|---|---|---|
| Lanturn | super rod | 30 | Oxide | Stockpile, Swallow, Spit Up, BubbleBeam | Signal Beam 35, Discharge 40, Aqua Ring 47, Hydro Pump 52 | Lanturn |
| Lanturn | super rod | 30 | v3 | Stockpile, Swallow, Spit Up, BubbleBeam | Signal Beam 35, Aqua Ring 47, Hydro Pump 52, Discharge 53 | Lanturn |
| Sharpedo | super rod | 30 | Oxide | Swagger, Assurance, Crunch, Slash | Aqua Jet 34, Taunt 40, Agility 45, Skull Bash 50, Night Slash 56 | Sharpedo |
| Sharpedo | super rod | 30 | v3 | Swagger, Assurance, Crunch, Slash | Aqua Jet 34, Taunt 40, Agility 45, Night Slash 56 | Sharpedo |
| Floatzel | super rod | 33 | Oxide | Swift, Aqua Jet, Crunch, Agility | Whirlpool 39, Razor Wind 50 | Floatzel |
| Floatzel | super rod | 33 | v3 | Swift, Aqua Jet, Crunch, Agility | nothing | Floatzel |
| Kingler | super rod | 33 | both | Mud Shot, Metal Claw, Stomp, Protect | Guillotine 37, Slam 44, Brine 51, Crabhammer 56 | Kingler |
| Greninja | super rod | 36 | both | Acrobatics, Low Kick, Waterfall, Fling | Scald 37, Dark Pulse 40, Extrasensory 43, Sludge Wave 47, Gunk Shot 51, Hydro Pump 55 | Greninja |

## Mt. Coronet B1F

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 56 | At the cap |
|---|---|---|---|---|---|---|
| Feebas | old rod | 18 | Oxide | Splash, Tackle | Flail 30; as Milotic: Hydro Pump 37, Attract 41, Safeguard 45, Aqua Ring 49 | Milotic (from 30) |
| Feebas | old rod | 18 | v3 | Tackle, Water Gun | Flail 30; as Milotic: Hydro Pump 37, Attract 41, Safeguard 45, Aqua Ring 49 | Milotic (from 30) |
| Horsea | old rod | 18 | Oxide | Leer, Water Gun, Focus Energy, BubbleBeam | Agility 23, Twister 26, Brine 30; as Kingdra: Hydro Pump 40, Dragon Dance 48 | Kingdra (from 32) |
| Horsea | old rod | 18 | v3 | Leer, Water Gun, Focus Energy, BubbleBeam | Agility 23, Brine 30; as Kingdra: Hydro Pump 40, Dragon Dance 48 | Kingdra (from 32) |
| Croconaw | old rod | 19 | Oxide | Water Gun, Rage, Bite, Scary Face | Ice Fang 21, Flail 24, Crunch 30; as Feraligatr: Agility 30, Crunch 32, Slash 37, Screech 45, Thrash 50 | Feraligatr (from 30) |
| Croconaw | old rod | 19 | v3 | Leer, Water Gun, Bite, Scary Face | Flail 24, Crunch 30; as Feraligatr: Agility 30, Crunch 32, Slash 37, Screech 45, Thrash 50 | Feraligatr (from 30) |
| Goldeen | old rod | 19 | Oxide | Water Sport, Supersonic, Horn Attack, Water Pulse | Flail 21, Aqua Ring 27, Fury Attack 31; as Seaking: Waterfall 40, Horn Drill 47, Agility 56 | Seaking (from 33) |
| Goldeen | old rod | 19 | v3 | Water Sport, Supersonic, Horn Attack, Water Pulse | Flail 21, Aqua Ring 27; as Seaking: Waterfall 40, Horn Drill 47, Agility 56 | Seaking (from 33) |
| Seel | old rod | 20 | Oxide | Water Sport, Icy Wind, Encore, Ice Shard | Rest 21, Aqua Ring 23, Aurora Beam 27, Aqua Jet 31, Brine 33; as Dewgong: Sheer Cold 34, Take Down 37, Dive 41, Aqua Tail 43, Ice Beam 47, Safeguard 51 | Dewgong (from 34) |
| Seel | old rod | 20 | v3 | Water Sport, Icy Wind, Encore, Ice Shard | Rest 21, Aqua Ring 23, Aurora Beam 27, Aqua Jet 31, Brine 33; as Dewgong: Sheer Cold 34, Take Down 37, Dive 41, Aqua Tail 43, Safeguard 51, Ice Beam 53 | Dewgong (from 34) |
| Corphish | good rod | 30 | both | Leer, BubbleBeam, Protect, Knock Off | as Crawdaunt: Taunt 34, Night Slash 39, Crabhammer 44, Swords Dance 52 | Crawdaunt (from 31) |
| Feebas | good rod | 30 | Oxide | Splash, Tackle, Flail | as Milotic: Hydro Pump 37, Attract 41, Safeguard 45, Aqua Ring 49 | Milotic (from 31) |
| Feebas | good rod | 30 | v3 | Tackle, Water Gun, Flail | as Milotic: Hydro Pump 37, Attract 41, Safeguard 45, Aqua Ring 49 | Milotic (from 31) |
| Chinchou | good rod | 32 | Oxide | Spark, Take Down, BubbleBeam, Signal Beam | as Lanturn: Signal Beam 35, Discharge 40, Aqua Ring 47, Hydro Pump 52 | Lanturn (from 33) |
| Chinchou | good rod | 32 | v3 | Spark, Take Down, BubbleBeam, Signal Beam | as Lanturn: Signal Beam 35, Aqua Ring 47, Hydro Pump 52, Discharge 53 | Lanturn (from 33) |
| Frillish | good rod | 32 | Oxide | Water Pulse, Imprison, Confuse Ray, Hex | Brine 34, Pain Split 39; as Jellicent: Destiny Bond 45, Shadow Ball 51, Scald 55 | Jellicent (from 40) |
| Frillish | good rod | 32 | v3 | Water Pulse, Imprison, Confuse Ray, Hex | Brine 34, Pain Split 39; as Jellicent: Destiny Bond 45, Shadow Ball 52, Scald 53 | Jellicent (from 40) |
| Goomy | wild | 32 | Oxide | Life Dew, Flail, Water Pulse, Dragon Tail | Infestation 34; as Sliggoo: Body Slam 42, Muddy Water 48; as Goodra: Aqua Tail 55 | Goodra (from 50) |
| Goomy | wild | 32 | Oxide | Life Dew, Flail, Water Pulse, Dragon Tail | as Hisuian Sliggoo: Dragon Pulse 35, Curse 43, Iron Head 49; as Hisuian Goodra: Iron Tail 55 | Hisuian Goodra (from 50) |
| Goomy | wild | 32 | v3 | Life Dew, Flail, Water Pulse, Dragon Tail | as Sliggoo: Body Slam 42; as Goodra: Aqua Tail 55 | Goodra (from 50) |
| Goomy | wild | 32 | v3 | Life Dew, Flail, Water Pulse, Dragon Tail | as Hisuian Sliggoo: Shelter on evolving, Iron Head 33, Muddy Water 39, Curse 43; as Hisuian Goodra: Power Whip 56 | Hisuian Goodra (from 50) |
| Bronzong | wild | 33 | Oxide | Extrasensory, Iron Defense, Safeguard, Block | Gyro Ball 38, Future Sight 43, Faint Attack 50 | Bronzong |
| Bronzong | wild | 33 | v3 | Extrasensory, Iron Defense, Safeguard, Block | Gyro Ball 38, Future Sight 43, Faint Attack 50, Earthquake 53 | Bronzong |
| Carbink | wild | 33 to 34 | both | Reflect, Flail, AncientPower, Rock Polish | Rock Slide 35, Stealth Rock 36, Skill Swap 40, Light Screen 44, Power Gem 45, Moonblast 52, Stone Edge 54 | Carbink |
| Donphan | wild | 33 | both | Magnitude, Slam, Fury Attack, Assurance | Scary Face 39, Earthquake 46, Giga Impact 54 | Donphan |
| Golbat | wild | 33 to 35 | both | Wing Attack, Confuse Ray, Air Cutter, Mean Look | Poison Fang 39; as Crobat: Haze 45, Air Slash 51 | Crobat (from 40) |
| Hariyama | wild | 33 | Oxide | Knock Off, SmellingSalt, Belly Drum, Force Palm | Seismic Toss 37, Wake-Up Slap 42, Endure 47, Close Combat 52 | Hariyama |
| Hariyama | wild | 33 | v3 | Knock Off, SmellingSalt, Belly Drum, Force Palm | Seismic Toss 37, Wake-Up Slap 42, Endure 47 | Hariyama |
| Mienfoo | wild | 33 | Oxide | Force Palm, Bounce, Drain Punch, Vacuum Wave | as Mienshao: Aura Sphere 38, Me First 40, Jump Kick 45, Dual Chop 48, Focus Blast 51, Acrobatics 55 | Mienshao (from 36) |
| Mienfoo | wild | 33 | v3 | Force Palm, Bounce, Vacuum Wave, Drain Punch | as Mienshao: Me First 40, Jump Kick 45, Dual Chop 48, Focus Blast 51, Acrobatics 55, Aura Sphere 56 | Mienshao (from 36) |
| Naclstack | wild | 33 | Oxide | Rock Polish, Headbutt, Iron Defense, Recover | Rock Slide 34, Stealth Rock 38; as Garganacl: Stealth Rock 40, Heavy Slam 44, Earthquake 49, Stone Edge 54 | Garganacl (from 38) |
| Naclstack | wild | 33 | v3 | Rock Polish, Headbutt, Iron Defense, Recover | Rock Slide 34, Stealth Rock 38; as Garganacl: Hammer Arm on evolving, Stealth Rock 40, Heavy Slam 44, Earthquake 49, Stone Edge 54 | Garganacl (from 38) |
| Dewgong | good rod | 34 | Oxide | Aurora Beam, Aqua Jet, Brine, Sheer Cold | Take Down 37, Dive 41, Aqua Tail 43, Ice Beam 47, Safeguard 51 | Dewgong |
| Dewgong | good rod | 34 | v3 | Aurora Beam, Aqua Jet, Brine, Sheer Cold | Take Down 37, Dive 41, Aqua Tail 43, Safeguard 51, Ice Beam 53 | Dewgong |
| Glimmet | wild | 34 | Oxide | Stealth Rock, Venoshock, Selfdestruct, Rock Slide | as Glimmora: Power Gem 39, Acid Armor 44, Sludge Wave 50 | Glimmora (from 35) |
| Glimmet | wild | 34 | v3 | Stealth Rock, Venoshock, Selfdestruct, Rock Slide | as Glimmora: Mortal Spin on evolving, Power Gem 39, Acid Armor 44, Sludge Wave 50 | Glimmora (from 35) |
| Graveler | wild | 34 | Oxide | Selfdestruct, Rollout, Rock Blast, Earthquake | Explosion 38; as Golem: Double-Edge 44, Stone Edge 49 | Golem (from 40) |
| Graveler | wild | 34 | v3 | Rock Throw, Magnitude, Selfdestruct, Rock Blast | Explosion 38, Earthquake 39; as Golem: Double-Edge 44, Stone Edge 49 | Golem (from 40) |
| Probopass | wild | 34 | both | Magnet Bomb, Block, Thunder Wave, Rock Slide | Rest 43, Power Gem 49, Discharge 55 | Probopass |
| Meditite | wild | 35 | both | Feint, Calm Mind, Force Palm, Hi Jump Kick | Psych Up 36; as Medicham: Power Trick 42, Reversal 49, Recover 55 | Medicham (from 37) |
| Sandygast | wild | 35 | Oxide | Mega Drain, Bulldoze, Hypnosis, Giga Drain | Iron Defense 36; as Palossand: Shadow Ball 44, Earth Power 50 | Palossand (from 42) |
| Sandygast | wild | 35 | v3 | Bulldoze, Hypnosis, Earth Power, Giga Drain | Iron Defense 36, Shadow Ball 39; as Palossand: Shadow Ball 44, Earth Power 50 | Palossand (from 42) |
| Buizel | surf | 36 | Oxide | Swift, Aqua Jet, Agility, Whirlpool | as Floatzel: Whirlpool 39, Razor Wind 50 | Floatzel (from 37) |
| Buizel | surf | 36 | v3 | Pursuit, Swift, Aqua Jet, Agility | nothing | Floatzel (from 37) |
| Floatzel | surf | 36 | Oxide | Swift, Aqua Jet, Crunch, Agility | Whirlpool 39, Razor Wind 50 | Floatzel |
| Floatzel | surf | 36 | v3 | Swift, Aqua Jet, Crunch, Agility | nothing | Floatzel |
| Feebas | surf | 39 | Oxide | Splash, Tackle, Flail | as Milotic: Attract 41, Safeguard 45, Aqua Ring 49 | Milotic (from 40) |
| Feebas | surf | 39 | v3 | Tackle, Water Gun, Flail | as Milotic: Attract 41, Safeguard 45, Aqua Ring 49 | Milotic (from 40) |
| Frillish | surf | 39 | Oxide | Confuse Ray, Hex, Brine, Pain Split | as Jellicent: Destiny Bond 45, Shadow Ball 51, Scald 55 | Jellicent (from 40) |
| Frillish | surf | 39 | v3 | Confuse Ray, Hex, Brine, Pain Split | as Jellicent: Destiny Bond 45, Shadow Ball 52, Scald 53 | Jellicent (from 40) |
| Crawdaunt | super rod | 40 | both | Knock Off, Swift, Taunt, Night Slash | Crabhammer 44, Swords Dance 52 | Crawdaunt |
| Milotic | super rod | 40 | both | Recover, Captivate, Aqua Tail, Hydro Pump | Attract 41, Safeguard 45, Aqua Ring 49 | Milotic |
| Kingdra | surf | 42 | both | Agility, Twister, Brine, Hydro Pump | Dragon Dance 48 | Kingdra |
| Lanturn | super rod | 43 | Oxide | Spit Up, BubbleBeam, Signal Beam, Discharge | Aqua Ring 47, Hydro Pump 52 | Lanturn |
| Lanturn | super rod | 43 | v3 | Swallow, Spit Up, BubbleBeam, Signal Beam | Aqua Ring 47, Hydro Pump 52, Discharge 53 | Lanturn |
| Wailord | super rod | 43 | Oxide | Rest, Brine, Water Spout, Amnesia | Dive 46, Bounce 54 | Wailord |
| Wailord | super rod | 43 | v3 | Mist, Rest, Brine, Amnesia | Dive 46, Bounce 54 | Wailord |
| Pelipper | super rod | 46 | Oxide | Stockpile, Swallow, Spit Up, Fling | Tailwind 50 | Pelipper |
| Pelipper | super rod | 46 | v3 | Stockpile, Swallow, Spit Up, Fling | Tailwind 50, Roost 53 | Pelipper |

## Mt. Coronet South

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 56 | At the cap |
|---|---|---|---|---|---|---|
| Milotic | super rod | 32 | both | Twister, Recover, Captivate, Aqua Tail | Hydro Pump 37, Attract 41, Safeguard 45, Aqua Ring 49 | Milotic |
| Whiscash | super rod | 32 | Oxide | Mud Bomb, Amnesia, Water Pulse, Magnitude | Rest 33, Snore 33, Aqua Tail 39, Earthquake 45, Future Sight 51 | Whiscash |
| Whiscash | super rod | 32 | v3 | Mud Bomb, Amnesia, Water Pulse, Magnitude | Rest 33, Aqua Tail 39, Earthquake 45, Future Sight 51 | Whiscash |
| Crawdaunt | super rod | 35 | both | Protect, Knock Off, Swift, Taunt | Night Slash 39, Crabhammer 44, Swords Dance 52 | Crawdaunt |
| Lanturn | super rod | 35 | Oxide | Swallow, Spit Up, BubbleBeam, Signal Beam | Discharge 40, Aqua Ring 47, Hydro Pump 52 | Lanturn |
| Lanturn | super rod | 35 | v3 | Swallow, Spit Up, BubbleBeam, Signal Beam | Aqua Ring 47, Hydro Pump 52, Discharge 53 | Lanturn |
| Greninja | super rod | 38 | both | Low Kick, Waterfall, Fling, Scald | Dark Pulse 40, Extrasensory 43, Sludge Wave 47, Gunk Shot 51, Hydro Pump 55 | Greninja |

## Oreburgh Gate

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 56 | At the cap |
|---|---|---|---|---|---|---|
| Corsola | super rod | 30 | Oxide | Refresh, Rock Blast, BubbleBeam, Lucky Chant | AncientPower 32, Aqua Ring 37, Spike Cannon 40, Power Gem 44, Mirror Coat 48, Earth Power 53 | Corsola |
| Corsola | super rod | 30 | v3 | Refresh, BubbleBeam, Recover, Lucky Chant | AncientPower 32, Rock Blast 33, Aqua Ring 37, Spike Cannon 40, Power Gem 44, Mirror Coat 48, Earth Power 53 | Corsola |
| Jellicent | super rod | 30 | Oxide | Water Pulse, Imprison, Confuse Ray, Hex | Brine 34, Pain Split 39, Destiny Bond 45, Shadow Ball 51, Scald 55 | Jellicent |
| Jellicent | super rod | 30 | v3 | Water Pulse, Imprison, Confuse Ray, Hex | Brine 34, Pain Split 39, Destiny Bond 45, Shadow Ball 52, Scald 53 | Jellicent |
| Seaking | super rod | 33 | Oxide | Water Pulse, Flail, Aqua Ring, Fury Attack | Waterfall 40, Horn Drill 47, Agility 56 | Seaking |
| Seaking | super rod | 33 | v3 | Horn Attack, Water Pulse, Flail, Aqua Ring | Waterfall 40, Horn Drill 47, Agility 56 | Seaking |
| Whiscash | super rod | 33 | Oxide | Water Pulse, Magnitude, Rest, Snore | Aqua Tail 39, Earthquake 45, Future Sight 51 | Whiscash |
| Whiscash | super rod | 33 | v3 | Amnesia, Water Pulse, Magnitude, Rest | Aqua Tail 39, Earthquake 45, Future Sight 51 | Whiscash |
| Wailmer | super rod | 36 | Oxide | Mist, Rest, Brine, Water Spout | Amnesia 37; as Wailord: Dive 46, Bounce 54 | Wailord (from 40) |
| Wailmer | super rod | 36 | v3 | Water Pulse, Mist, Rest, Brine | Amnesia 37; as Wailord: Dive 46, Bounce 54 | Wailord (from 40) |

## Pastoria City

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 56 | At the cap |
|---|---|---|---|---|---|---|
| Quagsire | super rod | 35 | Oxide | Slam, Mud Bomb, Amnesia, Yawn | Earthquake 36, Mist 48, Haze 48, Muddy Water 53 | Quagsire |
| Quagsire | super rod | 35 | v3 | Slam, Mud Bomb, Amnesia, Yawn | Earthquake 44, Mist 48, Haze 48, Muddy Water 53 | Quagsire |
| Sharpedo | super rod | 35 | Oxide | Assurance, Crunch, Slash, Aqua Jet | Taunt 40, Agility 45, Skull Bash 50, Night Slash 56 | Sharpedo |
| Sharpedo | super rod | 35 | v3 | Assurance, Crunch, Slash, Aqua Jet | Taunt 40, Agility 45, Night Slash 56 | Sharpedo |
| Lombre | super rod | 38 | Oxide | Water Sport, BubbleBeam, Zen Headbutt, Uproar | nothing | Ludicolo (from 38) |
| Lombre | super rod | 38 | v3 | Water Sport, BubbleBeam, Zen Headbutt, Uproar | as Ludicolo: Hydro Pump 45 | Ludicolo (from 38) |
| Ludicolo | super rod | 38 | Oxide | Astonish, Growl, Mega Drain, Nature Power | nothing | Ludicolo |
| Ludicolo | super rod | 38 | v3 | Growl, Mega Drain, Nature Power | Hydro Pump 45 | Ludicolo |
| Greninja | super rod | 41 | both | Waterfall, Fling, Scald, Dark Pulse | Extrasensory 43, Sludge Wave 47, Gunk Shot 51, Hydro Pump 55 | Greninja |

## Ravaged Path

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 56 | At the cap |
|---|---|---|---|---|---|---|
| Milotic | super rod | 30 | both | Twister, Recover, Captivate, Aqua Tail | Hydro Pump 37, Attract 41, Safeguard 45, Aqua Ring 49 | Milotic |
| Whiscash | super rod | 30 | Oxide | Mud Bomb, Amnesia, Water Pulse, Magnitude | Rest 33, Snore 33, Aqua Tail 39, Earthquake 45, Future Sight 51 | Whiscash |
| Whiscash | super rod | 30 | v3 | Mud Bomb, Amnesia, Water Pulse, Magnitude | Rest 33, Aqua Tail 39, Earthquake 45, Future Sight 51 | Whiscash |
| Crawdaunt | super rod | 33 | both | BubbleBeam, Protect, Knock Off, Swift | Taunt 34, Night Slash 39, Crabhammer 44, Swords Dance 52 | Crawdaunt |
| Lanturn | super rod | 33 | Oxide | Stockpile, Swallow, Spit Up, BubbleBeam | Signal Beam 35, Discharge 40, Aqua Ring 47, Hydro Pump 52 | Lanturn |
| Lanturn | super rod | 33 | v3 | Stockpile, Swallow, Spit Up, BubbleBeam | Signal Beam 35, Aqua Ring 47, Hydro Pump 52, Discharge 53 | Lanturn |
| Greninja | super rod | 36 | both | Acrobatics, Low Kick, Waterfall, Fling | Scald 37, Dark Pulse 40, Extrasensory 43, Sludge Wave 47, Gunk Shot 51, Hydro Pump 55 | Greninja |

## Route 203

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 56 | At the cap |
|---|---|---|---|---|---|---|
| Horsea | super rod | 30 | Oxide | BubbleBeam, Agility, Twister, Brine | as Kingdra: Hydro Pump 40, Dragon Dance 48 | Kingdra (from 32) |
| Horsea | super rod | 30 | v3 | Focus Energy, BubbleBeam, Agility, Brine | as Kingdra: Hydro Pump 40, Dragon Dance 48 | Kingdra (from 32) |
| Sharpedo | super rod | 30 | Oxide | Swagger, Assurance, Crunch, Slash | Aqua Jet 34, Taunt 40, Agility 45, Skull Bash 50, Night Slash 56 | Sharpedo |
| Sharpedo | super rod | 30 | v3 | Swagger, Assurance, Crunch, Slash | Aqua Jet 34, Taunt 40, Agility 45, Night Slash 56 | Sharpedo |
| Floatzel | super rod | 33 | Oxide | Swift, Aqua Jet, Crunch, Agility | Whirlpool 39, Razor Wind 50 | Floatzel |
| Floatzel | super rod | 33 | v3 | Swift, Aqua Jet, Crunch, Agility | nothing | Floatzel |
| Quagsire | super rod | 33 | Oxide | Slam, Mud Bomb, Amnesia, Yawn | Earthquake 36, Mist 48, Haze 48, Muddy Water 53 | Quagsire |
| Quagsire | super rod | 33 | v3 | Slam, Mud Bomb, Amnesia, Yawn | Earthquake 44, Mist 48, Haze 48, Muddy Water 53 | Quagsire |
| Feraligatr | super rod | 36 | both | Ice Fang, Flail, Agility, Crunch | Slash 37, Screech 45, Thrash 50 | Feraligatr |

## Route 204

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 56 | At the cap |
|---|---|---|---|---|---|---|
| Floatzel | super rod | 30 | Oxide | Swift, Aqua Jet, Crunch, Agility | Whirlpool 39, Razor Wind 50 | Floatzel |
| Floatzel | super rod | 30 | v3 | Swift, Aqua Jet, Crunch, Agility | nothing | Floatzel |
| Gastrodon | super rod | 30 to 33 | Oxide | Water Pulse, Mud Bomb, Hidden Power, Body Slam | Muddy Water 41, Recover 54 | Gastrodon |
| Gastrodon | super rod | 30 to 33 | v3 | Water Pulse, Mud Bomb, Hidden Power, Body Slam | Muddy Water 39, Earthquake 44, Recover 54 | Gastrodon |
| Quagsire | super rod | 30 | Oxide | Mud Shot, Slam, Mud Bomb, Amnesia | Yawn 31, Earthquake 36, Mist 48, Haze 48, Muddy Water 53 | Quagsire |
| Quagsire | super rod | 30 | v3 | Mud Shot, Slam, Mud Bomb, Amnesia | Yawn 31, Earthquake 44, Mist 48, Haze 48, Muddy Water 53 | Quagsire |
| Seaking | super rod | 30 | Oxide | Horn Attack, Water Pulse, Flail, Aqua Ring | Fury Attack 31, Waterfall 40, Horn Drill 47, Agility 56 | Seaking |
| Seaking | super rod | 30 | v3 | Horn Attack, Water Pulse, Flail, Aqua Ring | Waterfall 40, Horn Drill 47, Agility 56 | Seaking |
| Crawdaunt | super rod | 33 | both | BubbleBeam, Protect, Knock Off, Swift | Taunt 34, Night Slash 39, Crabhammer 44, Swords Dance 52 | Crawdaunt |
| Ludicolo | super rod | 33 | Oxide | Astonish, Growl, Mega Drain, Nature Power | nothing | Ludicolo |
| Ludicolo | super rod | 33 | v3 | Growl, Mega Drain, Nature Power | Hydro Pump 45 | Ludicolo |
| Whiscash | super rod | 33 | Oxide | Water Pulse, Magnitude, Rest, Snore | Aqua Tail 39, Earthquake 45, Future Sight 51 | Whiscash |
| Whiscash | super rod | 33 | v3 | Amnesia, Water Pulse, Magnitude, Rest | Aqua Tail 39, Earthquake 45, Future Sight 51 | Whiscash |
| Golduck | super rod | 36 | both | Confusion, Water Pulse, Fury Swipes, Screech | Psych Up 37, Zen Headbutt 44, Amnesia 50, Hydro Pump 56 | Golduck |
| Poliwrath | super rod | 36 | Oxide | BubbleBeam, Hypnosis, DoubleSlap, Submission | DynamicPunch 43, Mind Reader 53 | Poliwrath |
| Poliwrath | super rod | 36 | v3 | BubbleBeam, Hypnosis, DoubleSlap | DynamicPunch 43, Mind Reader 53 | Poliwrath |

## Route 205

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 56 | At the cap |
|---|---|---|---|---|---|---|
| Lombre | super rod | 30 | Oxide | Fake Out, Fury Swipes, Water Sport, BubbleBeam | nothing | Ludicolo (from 30) |
| Lombre | super rod | 30 | v3 | Fake Out, Fury Swipes, Water Sport, BubbleBeam | as Ludicolo: Hydro Pump 45 | Ludicolo (from 30) |
| Ludicolo | super rod | 30 | Oxide | Astonish, Growl, Mega Drain, Nature Power | nothing | Ludicolo |
| Ludicolo | super rod | 30 | v3 | Growl, Mega Drain, Nature Power | Hydro Pump 45 | Ludicolo |
| Seaking | super rod | 30 | Oxide | Horn Attack, Water Pulse, Flail, Aqua Ring | Fury Attack 31, Waterfall 40, Horn Drill 47, Agility 56 | Seaking |
| Seaking | super rod | 30 | v3 | Horn Attack, Water Pulse, Flail, Aqua Ring | Waterfall 40, Horn Drill 47, Agility 56 | Seaking |
| Whiscash | super rod | 30 | Oxide | Mud Bomb, Amnesia, Water Pulse, Magnitude | Rest 33, Snore 33, Aqua Tail 39, Earthquake 45, Future Sight 51 | Whiscash |
| Whiscash | super rod | 30 | v3 | Mud Bomb, Amnesia, Water Pulse, Magnitude | Rest 33, Aqua Tail 39, Earthquake 45, Future Sight 51 | Whiscash |
| Araquanid | super rod | 33 | Oxide | BubbleBeam, Bug Bite, Headbutt, Soak | Dive 36, Lunge 41, Scald 48, Hydro Pump 51, Liquidation 55 | Araquanid |
| Araquanid | super rod | 33 | v3 | BubbleBeam, Bug Bite, Headbutt, Soak | Dive 36, Lunge 41, Hydro Pump 51, Liquidation 55 | Araquanid |
| Crawdaunt | super rod | 33 | both | BubbleBeam, Protect, Knock Off, Swift | Taunt 34, Night Slash 39, Crabhammer 44, Swords Dance 52 | Crawdaunt |
| Jellicent | super rod | 33 | Oxide | Water Pulse, Imprison, Confuse Ray, Hex | Brine 34, Pain Split 39, Destiny Bond 45, Shadow Ball 51, Scald 55 | Jellicent |
| Jellicent | super rod | 33 | v3 | Water Pulse, Imprison, Confuse Ray, Hex | Brine 34, Pain Split 39, Destiny Bond 45, Shadow Ball 52, Scald 53 | Jellicent |
| Lanturn | super rod | 33 | Oxide | Stockpile, Swallow, Spit Up, BubbleBeam | Signal Beam 35, Discharge 40, Aqua Ring 47, Hydro Pump 52 | Lanturn |
| Lanturn | super rod | 33 | v3 | Stockpile, Swallow, Spit Up, BubbleBeam | Signal Beam 35, Aqua Ring 47, Hydro Pump 52, Discharge 53 | Lanturn |
| Golduck | super rod | 36 | both | Confusion, Water Pulse, Fury Swipes, Screech | Psych Up 37, Zen Headbutt 44, Amnesia 50, Hydro Pump 56 | Golduck |

## Route 208

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 56 | At the cap |
|---|---|---|---|---|---|---|
| Seaking | super rod | 32 | Oxide | Water Pulse, Flail, Aqua Ring, Fury Attack | Waterfall 40, Horn Drill 47, Agility 56 | Seaking |
| Seaking | super rod | 32 | v3 | Horn Attack, Water Pulse, Flail, Aqua Ring | Waterfall 40, Horn Drill 47, Agility 56 | Seaking |
| Whiscash | super rod | 32 | Oxide | Mud Bomb, Amnesia, Water Pulse, Magnitude | Rest 33, Snore 33, Aqua Tail 39, Earthquake 45, Future Sight 51 | Whiscash |
| Whiscash | super rod | 32 | v3 | Mud Bomb, Amnesia, Water Pulse, Magnitude | Rest 33, Aqua Tail 39, Earthquake 45, Future Sight 51 | Whiscash |
| Crawdaunt | super rod | 35 | both | Protect, Knock Off, Swift, Taunt | Night Slash 39, Crabhammer 44, Swords Dance 52 | Crawdaunt |
| Milotic | super rod | 35 | both | Twister, Recover, Captivate, Aqua Tail | Hydro Pump 37, Attract 41, Safeguard 45, Aqua Ring 49 | Milotic |
| Toxapex | super rod | 38 | Oxide | Venoshock, Recover, Spike Cannon, Pin Missile | Toxic 39, Venom Drench 42, Poison Jab 43, Liquidation 45 | Toxapex |
| Toxapex | super rod | 38 | v3 | Toxic Spikes, Recover, Spike Cannon, Pin Missile | Toxic 39, Venom Drench 42, Poison Jab 43, Liquidation 45 | Toxapex |

## Route 209

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 56 | At the cap |
|---|---|---|---|---|---|---|
| Floatzel | super rod | 33 | Oxide | Swift, Aqua Jet, Crunch, Agility | Whirlpool 39, Razor Wind 50 | Floatzel |
| Floatzel | super rod | 33 | v3 | Swift, Aqua Jet, Crunch, Agility | nothing | Floatzel |
| Quagsire | super rod | 33 | Oxide | Slam, Mud Bomb, Amnesia, Yawn | Earthquake 36, Mist 48, Haze 48, Muddy Water 53 | Quagsire |
| Quagsire | super rod | 33 | v3 | Slam, Mud Bomb, Amnesia, Yawn | Earthquake 44, Mist 48, Haze 48, Muddy Water 53 | Quagsire |
| Gastrodon | super rod | 36 | Oxide | Water Pulse, Mud Bomb, Hidden Power, Body Slam | Muddy Water 41, Recover 54 | Gastrodon |
| Gastrodon | super rod | 36 | v3 | Water Pulse, Mud Bomb, Hidden Power, Body Slam | Muddy Water 39, Earthquake 44, Recover 54 | Gastrodon |
| Ludicolo | super rod | 36 | Oxide | Astonish, Growl, Mega Drain, Nature Power | nothing | Ludicolo |
| Ludicolo | super rod | 36 | v3 | Growl, Mega Drain, Nature Power | Hydro Pump 45 | Ludicolo |
| Feraligatr | super rod | 39 | both | Flail, Agility, Crunch, Slash | Screech 45, Thrash 50 | Feraligatr |

## Route 210

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 56 | At the cap |
|---|---|---|---|---|---|---|
| Seaking | super rod | 36 | Oxide | Water Pulse, Flail, Aqua Ring, Fury Attack | Waterfall 40, Horn Drill 47, Agility 56 | Seaking |
| Seaking | super rod | 36 | v3 | Horn Attack, Water Pulse, Flail, Aqua Ring | Waterfall 40, Horn Drill 47, Agility 56 | Seaking |
| Whiscash | super rod | 36 | Oxide | Water Pulse, Magnitude, Rest, Snore | Aqua Tail 39, Earthquake 45, Future Sight 51 | Whiscash |
| Whiscash | super rod | 36 | v3 | Amnesia, Water Pulse, Magnitude, Rest | Aqua Tail 39, Earthquake 45, Future Sight 51 | Whiscash |
| Crawdaunt | super rod | 39 | both | Knock Off, Swift, Taunt, Night Slash | Crabhammer 44, Swords Dance 52 | Crawdaunt |
| Milotic | super rod | 39 | both | Recover, Captivate, Aqua Tail, Hydro Pump | Attract 41, Safeguard 45, Aqua Ring 49 | Milotic |
| Lumineon | super rod | 42 | Oxide | Captivate, Safeguard, Aqua Ring, Whirlpool | U-turn 48, Bounce 53 | Lumineon |
| Lumineon | super rod | 42 | v3 | Water Pulse, Captivate, Safeguard, Aqua Ring | U-turn 48, Bounce 53 | Lumineon |

## Route 212

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 56 | At the cap |
|---|---|---|---|---|---|---|
| Floatzel | super rod | 35 | Oxide | Swift, Aqua Jet, Crunch, Agility | Whirlpool 39, Razor Wind 50 | Floatzel |
| Floatzel | super rod | 35 | v3 | Swift, Aqua Jet, Crunch, Agility | nothing | Floatzel |
| Quagsire | super rod | 35 | Oxide | Slam, Mud Bomb, Amnesia, Yawn | Earthquake 36, Mist 48, Haze 48, Muddy Water 53 | Quagsire |
| Quagsire | super rod | 35 | v3 | Slam, Mud Bomb, Amnesia, Yawn | Earthquake 44, Mist 48, Haze 48, Muddy Water 53 | Quagsire |
| Whiscash | super rod | 35 | Oxide | Water Pulse, Magnitude, Rest, Snore | Aqua Tail 39, Earthquake 45, Future Sight 51 | Whiscash |
| Whiscash | super rod | 35 | v3 | Amnesia, Water Pulse, Magnitude, Rest | Aqua Tail 39, Earthquake 45, Future Sight 51 | Whiscash |
| Gastrodon | super rod | 38 | Oxide | Water Pulse, Mud Bomb, Hidden Power, Body Slam | Muddy Water 41, Recover 54 | Gastrodon |
| Gastrodon | super rod | 38 | v3 | Water Pulse, Mud Bomb, Hidden Power, Body Slam | Muddy Water 39, Earthquake 44, Recover 54 | Gastrodon |
| Ludicolo | super rod | 38 | Oxide | Astonish, Growl, Mega Drain, Nature Power | nothing | Ludicolo |
| Ludicolo | super rod | 38 | v3 | Growl, Mega Drain, Nature Power | Hydro Pump 45 | Ludicolo |
| Sharpedo | super rod | 38 | Oxide | Assurance, Crunch, Slash, Aqua Jet | Taunt 40, Agility 45, Skull Bash 50, Night Slash 56 | Sharpedo |
| Sharpedo | super rod | 38 | v3 | Assurance, Crunch, Slash, Aqua Jet | Taunt 40, Agility 45, Night Slash 56 | Sharpedo |
| Alomomola | super rod | 41 | Oxide | Wake-Up Slap, Soak, Wish, Brine | Safeguard 45, Whirlpool 49, Helping Hand 53 | Alomomola |
| Alomomola | super rod | 41 | v3 | Wake-Up Slap, Soak, Wish, Brine | Safeguard 45, Helping Hand 53 | Alomomola |
| Greninja | super rod | 41 | both | Waterfall, Fling, Scald, Dark Pulse | Extrasensory 43, Sludge Wave 47, Gunk Shot 51, Hydro Pump 55 | Greninja |

## Route 213

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 56 | At the cap |
|---|---|---|---|---|---|---|
| Lumineon | super rod | 35 | Oxide | Water Pulse, Captivate, Safeguard, Aqua Ring | Whirlpool 42, U-turn 48, Bounce 53 | Lumineon |
| Lumineon | super rod | 35 | v3 | Water Pulse, Captivate, Safeguard, Aqua Ring | U-turn 48, Bounce 53 | Lumineon |
| Tentacruel | super rod | 35 | Oxide | BubbleBeam, Wrap, Barrier, Water Pulse | Poison Jab 36, Screech 42, Hydro Pump 49, Wring Out 55 | Tentacruel |
| Tentacruel | super rod | 35 | v3 | Toxic Spikes, BubbleBeam, Barrier, Water Pulse | Poison Jab 36, Screech 42, Toxic 44, Hydro Pump 49, Wring Out 55 | Tentacruel |
| Octillery | super rod | 38 | both | Focus Energy, Octazooka, Bullet Seed, Wring Out | Signal Beam 42, Ice Beam 48, Hyper Beam 55 | Octillery |
| Toxapex | super rod | 38 | Oxide | Venoshock, Recover, Spike Cannon, Pin Missile | Toxic 39, Venom Drench 42, Poison Jab 43, Liquidation 45 | Toxapex |
| Toxapex | super rod | 38 | v3 | Toxic Spikes, Recover, Spike Cannon, Pin Missile | Toxic 39, Venom Drench 42, Poison Jab 43, Liquidation 45 | Toxapex |
| Quagsire | super rod | 41 | Oxide | Mud Bomb, Amnesia, Yawn, Earthquake | Mist 48, Haze 48, Muddy Water 53 | Quagsire |
| Quagsire | super rod | 41 | v3 | Slam, Mud Bomb, Amnesia, Yawn | Earthquake 44, Mist 48, Haze 48, Muddy Water 53 | Quagsire |

## Route 214

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 56 | At the cap |
|---|---|---|---|---|---|---|
| Ludicolo | super rod | 35 | Oxide | Astonish, Growl, Mega Drain, Nature Power | nothing | Ludicolo |
| Ludicolo | super rod | 35 | v3 | Growl, Mega Drain, Nature Power | Hydro Pump 45 | Ludicolo |
| Quagsire | super rod | 35 | Oxide | Slam, Mud Bomb, Amnesia, Yawn | Earthquake 36, Mist 48, Haze 48, Muddy Water 53 | Quagsire |
| Quagsire | super rod | 35 | v3 | Slam, Mud Bomb, Amnesia, Yawn | Earthquake 44, Mist 48, Haze 48, Muddy Water 53 | Quagsire |
| Gastrodon | super rod | 38 | Oxide | Water Pulse, Mud Bomb, Hidden Power, Body Slam | Muddy Water 41, Recover 54 | Gastrodon |
| Gastrodon | super rod | 38 | v3 | Water Pulse, Mud Bomb, Hidden Power, Body Slam | Muddy Water 39, Earthquake 44, Recover 54 | Gastrodon |
| Seaking | super rod | 38 | Oxide | Water Pulse, Flail, Aqua Ring, Fury Attack | Waterfall 40, Horn Drill 47, Agility 56 | Seaking |
| Seaking | super rod | 38 | v3 | Horn Attack, Water Pulse, Flail, Aqua Ring | Waterfall 40, Horn Drill 47, Agility 56 | Seaking |
| Mantine | super rod | 41 | both | Water Pulse, Take Down, Confuse Ray, Bounce | Aqua Ring 46, Hydro Pump 49 | Mantine |

## Route 216

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 56 | At the cap |
|---|---|---|---|---|---|---|
| Snover | wild | 32 | Oxide | Swagger, Mist, Ice Shard, Ingrain | Wood Hammer 36; as Abomasnow: Blizzard 47 | Abomasnow (from 40) |
| Snover | wild | 32 | v3 | Swagger, Mist, Ice Shard, Ingrain | Wood Hammer 39; as Abomasnow: Blizzard 47, Wood Hammer 53 | Abomasnow (from 40) |
| Absol | wild | 33 | Oxide | Pursuit, Swords Dance, Bite, Double Team | Slash 36, Future Sight 41, Sucker Punch 44, Detect 49, Night Slash 52 | Absol |
| Absol | wild | 33 | v3 | Pursuit, Swords Dance, Bite, Double Team | Slash 36, Future Sight 41, Sucker Punch 44, Detect 49 | Absol |
| Delibird | wild | 33 | both | Present | nothing | Delibird |
| Frosmoth | wild | 33 | Oxide | Defog, FeatherDance, Aurora Beam, Bug Buzz | Aurora Veil 36, Blizzard 40, Tailwind 44, Wide Guard 48, Quiver Dance 52 | Frosmoth |
| Frosmoth | wild | 33 | v3 | Defog, FeatherDance, Aurora Beam, Bug Buzz | Aurora Veil 36, Tailwind 44, Blizzard 45, Wide Guard 48, Quiver Dance 52 | Frosmoth |
| Sneasel | wild | 33 | Oxide | Faint Attack, Fury Swipes, Agility, Icy Wind | Slash 35, Metal Claw 42, Ice Shard 49 | Sneasel; Weavile in HQ |
| Sneasel | wild | 33 | v3 | Faint Attack, Fury Swipes, Agility, Icy Wind | Slash 35, Ice Shard 49 | Sneasel; Weavile in HQ |
| Snorunt | wild | 33 to 34 | both | Headbutt, Protect, Ice Fang, Crunch | Ice Shard 37; as Glalie: Blizzard 51 | Glalie (from 42) |
| Snorunt | wild | 33 to 34 | both | Headbutt, Protect, Ice Fang, Crunch | as Froslass: Ice Shard 37, Blizzard 51 | Froslass (from 33) |
| Alolan Ninetales | wild | 34 | Oxide | Tail Whip, Disable, Ice Shard, Safeguard | nothing | Alolan Ninetales |
| Alolan Ninetales | wild | 34 | v3 | Safeguard, Icy Wind, Aurora Beam, Draining Kiss | Ice Beam 45 | Alolan Ninetales |
| Golbat | wild | 34 | both | Wing Attack, Confuse Ray, Air Cutter, Mean Look | Poison Fang 39; as Crobat: Haze 45, Air Slash 51 | Crobat (from 40) |
| Mienfoo | wild | 34 | Oxide | Force Palm, Bounce, Drain Punch, Vacuum Wave | as Mienshao: Aura Sphere 38, Me First 40, Jump Kick 45, Dual Chop 48, Focus Blast 51, Acrobatics 55 | Mienshao (from 36) |
| Mienfoo | wild | 34 | v3 | Force Palm, Bounce, Vacuum Wave, Drain Punch | as Mienshao: Me First 40, Jump Kick 45, Dual Chop 48, Focus Blast 51, Acrobatics 55, Aura Sphere 56 | Mienshao (from 36) |
| Bronzong | wild | 35 | Oxide | Extrasensory, Iron Defense, Safeguard, Block | Gyro Ball 38, Future Sight 43, Faint Attack 50 | Bronzong |
| Bronzong | wild | 35 | v3 | Extrasensory, Iron Defense, Safeguard, Block | Gyro Ball 38, Future Sight 43, Faint Attack 50, Earthquake 53 | Bronzong |
| Galarian Mr Mime | wild | 35 | both | Icy Wind, Double Kick, Psybeam, Hypnosis | Mirror Coat 36, Sucker Punch 40; as Mr. Rime: Freeze-Dry 44, Psychic 48, Teeter Dance 52 | Mr. Rime (from 42) |
| Slugma | wild | 35 | both | Harden, Recover, AncientPower, Amnesia | Lava Plume 38; as Magcargo: Lava Plume 40, Rock Slide 45, Body Slam 52 | Magcargo (from 38) |

## Route 217

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 56 | At the cap |
|---|---|---|---|---|---|---|
| Swinub | wild | 32 | Oxide | Mud Bomb, Icy Wind, Ice Shard, Take Down | as Piloswine: Fury Attack 33, Earthquake 40; as Mamoswine: Earthquake 40, Mist 48, Blizzard 56 | Mamoswine (from 40) |
| Swinub | wild | 32 | v3 | Mud Bomb, Icy Wind, Ice Shard, Take Down | as Mamoswine: Mist 48, Blizzard 56 | Mamoswine (from 40) |
| Frosmoth | wild | 33 to 34 | Oxide | Defog, FeatherDance, Aurora Beam, Bug Buzz | Aurora Veil 36, Blizzard 40, Tailwind 44, Wide Guard 48, Quiver Dance 52 | Frosmoth |
| Frosmoth | wild | 33 to 34 | v3 | Defog, FeatherDance, Aurora Beam, Bug Buzz | Aurora Veil 36, Tailwind 44, Blizzard 45, Wide Guard 48, Quiver Dance 52 | Frosmoth |
| Sneasel | wild | 33 | Oxide | Faint Attack, Fury Swipes, Agility, Icy Wind | Slash 35, Metal Claw 42, Ice Shard 49 | Sneasel; Weavile in HQ |
| Sneasel | wild | 33 | v3 | Faint Attack, Fury Swipes, Agility, Icy Wind | Slash 35, Ice Shard 49 | Sneasel; Weavile in HQ |
| Snorunt | wild | 33 | both | Headbutt, Protect, Ice Fang, Crunch | Ice Shard 37; as Glalie: Blizzard 51 | Glalie (from 42) |
| Snorunt | wild | 33 | both | Headbutt, Protect, Ice Fang, Crunch | as Froslass: Ice Shard 37, Blizzard 51 | Froslass (from 33) |
| Snover | wild | 33 | Oxide | Swagger, Mist, Ice Shard, Ingrain | Wood Hammer 36; as Abomasnow: Blizzard 47 | Abomasnow (from 40) |
| Snover | wild | 33 | v3 | Swagger, Mist, Ice Shard, Ingrain | Wood Hammer 39; as Abomasnow: Blizzard 47, Wood Hammer 53 | Abomasnow (from 40) |
| Alolan Ninetales | wild | 34 | Oxide | Tail Whip, Disable, Ice Shard, Safeguard | nothing | Alolan Ninetales |
| Alolan Ninetales | wild | 34 | v3 | Safeguard, Icy Wind, Aurora Beam, Draining Kiss | Ice Beam 45 | Alolan Ninetales |
| Donphan | wild | 34 | both | Magnitude, Slam, Fury Attack, Assurance | Scary Face 39, Earthquake 46, Giga Impact 54 | Donphan |
| Mienfoo | wild | 34 | Oxide | Force Palm, Bounce, Drain Punch, Vacuum Wave | as Mienshao: Aura Sphere 38, Me First 40, Jump Kick 45, Dual Chop 48, Focus Blast 51, Acrobatics 55 | Mienshao (from 36) |
| Mienfoo | wild | 34 | v3 | Force Palm, Bounce, Vacuum Wave, Drain Punch | as Mienshao: Me First 40, Jump Kick 45, Dual Chop 48, Focus Blast 51, Acrobatics 55, Aura Sphere 56 | Mienshao (from 36) |
| Galarian Mr Mime | wild | 35 | both | Icy Wind, Double Kick, Psybeam, Hypnosis | Mirror Coat 36, Sucker Punch 40; as Mr. Rime: Freeze-Dry 44, Psychic 48, Teeter Dance 52 | Mr. Rime (from 42) |
| Meditite | wild | 35 | both | Feint, Calm Mind, Force Palm, Hi Jump Kick | Psych Up 36; as Medicham: Power Trick 42, Reversal 49, Recover 55 | Medicham (from 37) |
| Slugma | wild | 35 | both | Harden, Recover, AncientPower, Amnesia | Lava Plume 38; as Magcargo: Lava Plume 40, Rock Slide 45, Body Slam 52 | Magcargo (from 38) |

## Route 218

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 56 | At the cap |
|---|---|---|---|---|---|---|
| Gorebyss | super rod | 36 | both | Amnesia, Aqua Ring, Captivate, Baton Pass | Dive 37, Psychic 42, Aqua Tail 46, Hydro Pump 51 | Gorebyss |
| Mantine | super rod | 36 | both | Agility, Wing Attack, Water Pulse, Take Down | Confuse Ray 37, Bounce 40, Aqua Ring 46, Hydro Pump 49 | Mantine |
| Gastrodon | super rod | 39 | Oxide | Water Pulse, Mud Bomb, Hidden Power, Body Slam | Muddy Water 41, Recover 54 | Gastrodon |
| Gastrodon | super rod | 39 | v3 | Mud Bomb, Hidden Power, Body Slam, Muddy Water | Earthquake 44, Recover 54 | Gastrodon |
| Jellicent | super rod | 39 | Oxide | Confuse Ray, Hex, Brine, Pain Split | Destiny Bond 45, Shadow Ball 51, Scald 55 | Jellicent |
| Jellicent | super rod | 39 | v3 | Confuse Ray, Hex, Brine, Pain Split | Destiny Bond 45, Shadow Ball 52, Scald 53 | Jellicent |
| Greninja | super rod | 42 | both | Waterfall, Fling, Scald, Dark Pulse | Extrasensory 43, Sludge Wave 47, Gunk Shot 51, Hydro Pump 55 | Greninja |

## Route 219

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 56 | At the cap |
|---|---|---|---|---|---|---|
| Jellicent | super rod | 30 | Oxide | Water Pulse, Imprison, Confuse Ray, Hex | Brine 34, Pain Split 39, Destiny Bond 45, Shadow Ball 51, Scald 55 | Jellicent |
| Jellicent | super rod | 30 | v3 | Water Pulse, Imprison, Confuse Ray, Hex | Brine 34, Pain Split 39, Destiny Bond 45, Shadow Ball 52, Scald 53 | Jellicent |
| Lanturn | super rod | 30 | Oxide | Stockpile, Swallow, Spit Up, BubbleBeam | Signal Beam 35, Discharge 40, Aqua Ring 47, Hydro Pump 52 | Lanturn |
| Lanturn | super rod | 30 | v3 | Stockpile, Swallow, Spit Up, BubbleBeam | Signal Beam 35, Aqua Ring 47, Hydro Pump 52, Discharge 53 | Lanturn |
| Lumineon | super rod | 33 | Oxide | Gust, Water Pulse, Captivate, Safeguard | Aqua Ring 35, Whirlpool 42, U-turn 48, Bounce 53 | Lumineon |
| Lumineon | super rod | 33 | v3 | Attract, Water Pulse, Captivate, Safeguard | Aqua Ring 35, U-turn 48, Bounce 53 | Lumineon |
| Tentacruel | super rod | 33 | Oxide | BubbleBeam, Wrap, Barrier, Water Pulse | Poison Jab 36, Screech 42, Hydro Pump 49, Wring Out 55 | Tentacruel |
| Tentacruel | super rod | 33 | v3 | Toxic Spikes, BubbleBeam, Barrier, Water Pulse | Poison Jab 36, Screech 42, Toxic 44, Hydro Pump 49, Wring Out 55 | Tentacruel |
| Greninja | super rod | 36 | both | Acrobatics, Low Kick, Waterfall, Fling | Scald 37, Dark Pulse 40, Extrasensory 43, Sludge Wave 47, Gunk Shot 51, Hydro Pump 55 | Greninja |

## Route 220

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 56 | At the cap |
|---|---|---|---|---|---|---|
| Jellicent | super rod | 36 | Oxide | Imprison, Confuse Ray, Hex, Brine | Pain Split 39, Destiny Bond 45, Shadow Ball 51, Scald 55 | Jellicent |
| Jellicent | super rod | 36 | v3 | Imprison, Confuse Ray, Hex, Brine | Pain Split 39, Destiny Bond 45, Shadow Ball 52, Scald 53 | Jellicent |
| Lanturn | super rod | 36 | Oxide | Swallow, Spit Up, BubbleBeam, Signal Beam | Discharge 40, Aqua Ring 47, Hydro Pump 52 | Lanturn |
| Lanturn | super rod | 36 | v3 | Swallow, Spit Up, BubbleBeam, Signal Beam | Aqua Ring 47, Hydro Pump 52, Discharge 53 | Lanturn |
| Lumineon | super rod | 39 | Oxide | Water Pulse, Captivate, Safeguard, Aqua Ring | Whirlpool 42, U-turn 48, Bounce 53 | Lumineon |
| Lumineon | super rod | 39 | v3 | Water Pulse, Captivate, Safeguard, Aqua Ring | U-turn 48, Bounce 53 | Lumineon |
| Tentacruel | super rod | 39 to 42 | Oxide | Wrap, Barrier, Water Pulse, Poison Jab | Screech 42, Hydro Pump 49, Wring Out 55 | Tentacruel |
| Tentacruel | super rod | 39 to 42 | v3 | BubbleBeam, Barrier, Water Pulse, Poison Jab | Screech 42, Toxic 44, Hydro Pump 49, Wring Out 55 | Tentacruel |

## Route 221

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 56 | At the cap |
|---|---|---|---|---|---|---|
| Lanturn | super rod | 36 | Oxide | Swallow, Spit Up, BubbleBeam, Signal Beam | Discharge 40, Aqua Ring 47, Hydro Pump 52 | Lanturn |
| Lanturn | super rod | 36 | v3 | Swallow, Spit Up, BubbleBeam, Signal Beam | Aqua Ring 47, Hydro Pump 52, Discharge 53 | Lanturn |
| Lumineon | super rod | 36 | Oxide | Water Pulse, Captivate, Safeguard, Aqua Ring | Whirlpool 42, U-turn 48, Bounce 53 | Lumineon |
| Lumineon | super rod | 36 | v3 | Water Pulse, Captivate, Safeguard, Aqua Ring | U-turn 48, Bounce 53 | Lumineon |
| Octillery | super rod | 39 | both | Focus Energy, Octazooka, Bullet Seed, Wring Out | Signal Beam 42, Ice Beam 48, Hyper Beam 55 | Octillery |
| Tentacruel | super rod | 39 | Oxide | Wrap, Barrier, Water Pulse, Poison Jab | Screech 42, Hydro Pump 49, Wring Out 55 | Tentacruel |
| Tentacruel | super rod | 39 | v3 | BubbleBeam, Barrier, Water Pulse, Poison Jab | Screech 42, Toxic 44, Hydro Pump 49, Wring Out 55 | Tentacruel |
| Greninja | super rod | 42 | both | Waterfall, Fling, Scald, Dark Pulse | Extrasensory 43, Sludge Wave 47, Gunk Shot 51, Hydro Pump 55 | Greninja |

## Snowpoint City

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 56 | At the cap |
|---|---|---|---|---|---|---|
| Suicune | in-game trade | 1 | Oxide | Bite, Leer | BubbleBeam 8, Gust 22, Aurora Beam 29, Mist 36, Mirror Coat 43, Ice Fang 50 | Suicune |
| Suicune | in-game trade | 1 | v3 | Bite, Leer, Ice Fang | BubbleBeam 8, Aurora Beam 29, Mist 36, Mirror Coat 43 | Suicune |
| Seel | old rod | 16 to 17 | Oxide | Growl, Water Sport, Icy Wind, Encore | Ice Shard 17, Rest 21, Aqua Ring 23, Aurora Beam 27, Aqua Jet 31, Brine 33; as Dewgong: Sheer Cold 34, Take Down 37, Dive 41, Aqua Tail 43, Ice Beam 47, Safeguard 51 | Dewgong (from 34) |
| Seel | old rod | 16 to 17 | v3 | Growl, Water Sport, Icy Wind, Encore | Ice Shard 17, Rest 21, Aqua Ring 23, Aurora Beam 27, Aqua Jet 31, Brine 33; as Dewgong: Sheer Cold 34, Take Down 37, Dive 41, Aqua Tail 43, Safeguard 51, Ice Beam 53 | Dewgong (from 34) |
| Spheal | old rod | 16 | Oxide | Growl, Water Gun, Encore, Ice Ball | Body Slam 19, Aurora Beam 25; as Sealeo: Swagger 32, Rest 39, Snore 39; as Walrein: Ice Fang 44, Blizzard 52 | Walrein (from 44) |
| Spheal | old rod | 16 | v3 | Defense Curl, Powder Snow, Growl, Water Gun | Body Slam 19, Bounce 20, Aurora Beam 25, Encore 31; as Sealeo: Swagger 32, Dive 38, Rest 39; as Walrein: Ice Fang 44, Blizzard 52 | Walrein (from 44) |
| Shellos | old rod | 17 | Oxide | Harden, Water Pulse, Mud Bomb, Hidden Power | Body Slam 29; as Gastrodon: Muddy Water 41, Recover 54 | Gastrodon (from 30) |
| Shellos | old rod | 17 | v3 | Harden, Water Pulse, Mud Bomb, Hidden Power | Body Slam 29; as Gastrodon: Muddy Water 39, Earthquake 44, Recover 54 | Gastrodon (from 30) |
| Snorunt | old rod | 18 | both | Leer, Double Team, Bite, Icy Wind | Headbutt 19, Protect 22, Ice Fang 28, Crunch 31, Ice Shard 37; as Glalie: Blizzard 51 | Glalie (from 42) |
| Snorunt | old rod | 18 | both | Leer, Double Team, Bite, Icy Wind | as Froslass: Confuse Ray 19, Ominous Wind 22, Wake-Up Slap 28, Captivate 31, Ice Shard 37, Blizzard 51 | Froslass (from 18) |
| Seel | good rod | 28 to 30 | Oxide | Ice Shard, Rest, Aqua Ring, Aurora Beam | Aqua Jet 31, Brine 33; as Dewgong: Sheer Cold 34, Take Down 37, Dive 41, Aqua Tail 43, Ice Beam 47, Safeguard 51 | Dewgong (from 34) |
| Seel | good rod | 28 to 30 | v3 | Ice Shard, Rest, Aqua Ring, Aurora Beam | Aqua Jet 31, Brine 33; as Dewgong: Sheer Cold 34, Take Down 37, Dive 41, Aqua Tail 43, Safeguard 51, Ice Beam 53 | Dewgong (from 34) |
| Spheal | good rod | 28 | Oxide | Encore, Ice Ball, Body Slam, Aurora Beam | as Sealeo: Swagger 32, Rest 39, Snore 39; as Walrein: Ice Fang 44, Blizzard 52 | Walrein (from 44) |
| Spheal | good rod | 28 | v3 | Water Gun, Body Slam, Bounce, Aurora Beam | Encore 31; as Sealeo: Swagger 32, Dive 38, Rest 39; as Walrein: Ice Fang 44, Blizzard 52 | Walrein (from 44) |
| Snover | good rod | 30 | Oxide | GrassWhistle, Swagger, Mist, Ice Shard | Ingrain 31, Wood Hammer 36; as Abomasnow: Blizzard 47 | Abomasnow (from 40) |
| Snover | good rod | 30 | v3 | GrassWhistle, Swagger, Mist, Ice Shard | Ingrain 31, Wood Hammer 39; as Abomasnow: Blizzard 47, Wood Hammer 53 | Abomasnow (from 40) |
| Lapras | good rod | 32 | Oxide | Water Pulse, Body Slam, Perish Song, Ice Beam | Brine 37, Safeguard 43, Hydro Pump 49, Sheer Cold 55 | Lapras |
| Lapras | good rod | 32 | v3 | Ice Shard, Water Pulse, Body Slam, Perish Song | Brine 37, Ice Beam 39, Safeguard 43, Hydro Pump 49, Sheer Cold 55 | Lapras |
| Dewgong | super rod | 38 to 41 | Oxide | Aqua Jet, Brine, Sheer Cold, Take Down | Dive 41, Aqua Tail 43, Ice Beam 47, Safeguard 51 | Dewgong |
| Dewgong | super rod | 38 to 41 | v3 | Aqua Jet, Brine, Sheer Cold, Take Down | Dive 41, Aqua Tail 43, Safeguard 51, Ice Beam 53 | Dewgong |
| Sealeo | super rod | 38 | Oxide | Ice Ball, Body Slam, Aurora Beam, Swagger | Rest 39, Snore 39; as Walrein: Ice Fang 44, Blizzard 52 | Walrein (from 44) |
| Sealeo | super rod | 38 | v3 | Body Slam, Aurora Beam, Swagger, Dive | Rest 39; as Walrein: Ice Fang 44, Blizzard 52 | Walrein (from 44) |
| Froslass | super rod | 41 | both | Ominous Wind, Wake-Up Slap, Captivate, Ice Shard | Blizzard 51 | Froslass |
| Lapras | super rod | 44 | Oxide | Perish Song, Ice Beam, Brine, Safeguard | Hydro Pump 49, Sheer Cold 55 | Lapras |
| Lapras | super rod | 44 | v3 | Perish Song, Brine, Ice Beam, Safeguard | Hydro Pump 49, Sheer Cold 55 | Lapras |

## Twinleaf Town

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 56 | At the cap |
|---|---|---|---|---|---|---|
| Crawdaunt | super rod | 30 | both | BubbleBeam, Protect, Knock Off, Swift | Taunt 34, Night Slash 39, Crabhammer 44, Swords Dance 52 | Crawdaunt |
| Lanturn | super rod | 30 | Oxide | Stockpile, Swallow, Spit Up, BubbleBeam | Signal Beam 35, Discharge 40, Aqua Ring 47, Hydro Pump 52 | Lanturn |
| Lanturn | super rod | 30 | v3 | Stockpile, Swallow, Spit Up, BubbleBeam | Signal Beam 35, Aqua Ring 47, Hydro Pump 52, Discharge 53 | Lanturn |
| Floatzel | super rod | 33 | Oxide | Swift, Aqua Jet, Crunch, Agility | Whirlpool 39, Razor Wind 50 | Floatzel |
| Floatzel | super rod | 33 | v3 | Swift, Aqua Jet, Crunch, Agility | nothing | Floatzel |
| Sharpedo | super rod | 33 | Oxide | Swagger, Assurance, Crunch, Slash | Aqua Jet 34, Taunt 40, Agility 45, Skull Bash 50, Night Slash 56 | Sharpedo |
| Sharpedo | super rod | 33 | v3 | Swagger, Assurance, Crunch, Slash | Aqua Jet 34, Taunt 40, Agility 45, Night Slash 56 | Sharpedo |
| Swampert | super rod | 36 | Oxide | Mud Shot, Foresight, Mud Bomb, Take Down | Muddy Water 39, Protect 46, Earthquake 52 | Swampert |
| Swampert | super rod | 36 | v3 | Mud Shot, Foresight, Mud Bomb, Take Down | Muddy Water 39, Protect 46, Earthquake 56 | Swampert |

## Valley Windworks

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 56 | At the cap |
|---|---|---|---|---|---|---|
| Crawdaunt | super rod | 30 | both | BubbleBeam, Protect, Knock Off, Swift | Taunt 34, Night Slash 39, Crabhammer 44, Swords Dance 52 | Crawdaunt |
| Whiscash | super rod | 30 | Oxide | Mud Bomb, Amnesia, Water Pulse, Magnitude | Rest 33, Snore 33, Aqua Tail 39, Earthquake 45, Future Sight 51 | Whiscash |
| Whiscash | super rod | 30 | v3 | Mud Bomb, Amnesia, Water Pulse, Magnitude | Rest 33, Aqua Tail 39, Earthquake 45, Future Sight 51 | Whiscash |
| Lanturn | super rod | 33 | Oxide | Stockpile, Swallow, Spit Up, BubbleBeam | Signal Beam 35, Discharge 40, Aqua Ring 47, Hydro Pump 52 | Lanturn |
| Lanturn | super rod | 33 | v3 | Stockpile, Swallow, Spit Up, BubbleBeam | Signal Beam 35, Aqua Ring 47, Hydro Pump 52, Discharge 53 | Lanturn |
| Sharpedo | super rod | 33 | Oxide | Swagger, Assurance, Crunch, Slash | Aqua Jet 34, Taunt 40, Agility 45, Skull Bash 50, Night Slash 56 | Sharpedo |
| Sharpedo | super rod | 33 | v3 | Swagger, Assurance, Crunch, Slash | Aqua Jet 34, Taunt 40, Agility 45, Night Slash 56 | Sharpedo |
| Greninja | super rod | 36 | both | Acrobatics, Low Kick, Waterfall, Fling | Scald 37, Dark Pulse 40, Extrasensory 43, Sludge Wave 47, Gunk Shot 51, Hydro Pump 55 | Greninja |

## Honey trees

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 56 | At the cap |
|---|---|---|---|---|---|---|
| Frosmoth | honey | 32 | Oxide | Defog, FeatherDance, Aurora Beam, Bug Buzz | Aurora Veil 36, Blizzard 40, Tailwind 44, Wide Guard 48, Quiver Dance 52 | Frosmoth |
| Frosmoth | honey | 32 | v3 | Defog, FeatherDance, Aurora Beam, Bug Buzz | Aurora Veil 36, Tailwind 44, Blizzard 45, Wide Guard 48, Quiver Dance 52 | Frosmoth |
| Galvantula | honey | 32 | Oxide | Bug Bite, Gastro Acid, Struggle Bug, Discharge | Signal Beam 35, Energy Ball 39, Sucker Punch 43, Thunderbolt 48, Bug Buzz 51, Thunder 55 | Galvantula |
| Galvantula | honey | 32 | v3 | Bug Bite, Gastro Acid, Struggle Bug, Discharge | Signal Beam 35, Sucker Punch 43, Thunderbolt 48, Bug Buzz 51, Energy Ball 53, Thunder 55 | Galvantula |
| Heracross | honey | 32 | Oxide | Aerial Ace, Brick Break, Counter, Take Down | Close Combat 37, Reversal 43, Feint 49, Megahorn 55 | Heracross |
| Heracross | honey | 32 | v3 | Aerial Ace, Counter, Brick Break, Take Down | Close Combat 37, Reversal 43, Feint 49, Megahorn 55 | Heracross |
| Larvesta | honey | 32 | Oxide | String Shot, Flame Charge, Struggle Bug, Flame Wheel | Bug Bite 40, Take Down 50 | Larvesta; Volcarona in HQ |
| Larvesta | honey | 32 | v3 | String Shot, Flame Charge, Struggle Bug, Flame Wheel | Double-Edge 39, Bug Bite 40, Take Down 50 | Larvesta; Volcarona in HQ |
| Leavanny | honey | 32 | Oxide | Razor Leaf, Struggle Bug, Fell Stinger, Helping Hand | Leaf Blade 36, X-Scissor 39, Entrainment 43, Swords Dance 46, Leaf Storm 50 | Leavanny |
| Leavanny | honey | 32 | v3 | Razor Leaf, Struggle Bug, Fell Stinger, Helping Hand | X-Scissor 39, Entrainment 43, Swords Dance 46, Leaf Storm 50, Leaf Blade 53 | Leavanny |
| Scizor | honey | 32 | Oxide | Agility, Metal Claw, Fury Cutter, Slash | Razor Wind 33, Iron Defense 37, X-Scissor 41, Night Slash 45, Double Hit 49, Iron Head 53 | Scizor |
| Scizor | honey | 32 | v3 | False Swipe, Agility, Metal Claw, Slash | Iron Defense 37, Iron Head 44, Night Slash 45, Double Hit 49, X-Scissor 53 | Scizor |
| Shiftry | honey | 32 | Oxide | Faint Attack, Whirlwind, Nasty Plot, Razor Leaf | Leaf Storm 49 | Shiftry |
| Shiftry | honey | 32 | v3 | Whirlwind, Nasty Plot, Razor Leaf, Faint Attack | Leaf Storm 49 | Shiftry |
| Snorlax | honey | 32 | Oxide | Yawn, Rest, Snore, Sleep Talk | Body Slam 33, Block 36, Rollout 41, Crunch 44, Giga Impact 49 | Snorlax |
| Snorlax | honey | 32 | v3 | Belly Drum, Yawn, Rest, Sleep Talk | Body Slam 33, Block 36, Crunch 44, Giga Impact 49 | Snorlax |
| Toucannon | honey | 32 | Oxide | Pluck, Roost, Fury Attack, Screech | Drill Peck 34, Bullet Seed 40, FeatherDance 44, Hyper Voice 50 | Toucannon |
| Toucannon | honey | 32 | v3 | Pluck, Roost, Fury Attack, Screech | Bullet Seed 40, FeatherDance 44, Hyper Voice 56 | Toucannon |
| Vespiquen | honey | 32 | Oxide | Power Gem, Heal Order, Toxic, Slash | Captivate 33, Attack Order 37, Swagger 39, Destiny Bond 43 | Vespiquen |
| Vespiquen | honey | 32 | v3 | Power Gem, Heal Order, Toxic, Slash | Captivate 33, Swagger 39, Attack Order 40, Destiny Bond 43 | Vespiquen |
| Vikavolt | honey | 32 | Oxide | Thunderbolt, Crunch, Bite, Spark | Signal Beam 36, Discharge 48, Bug Buzz 55 | Vikavolt |
| Vikavolt | honey | 32 | v3 | Bug Bite, Bite, Spark, Crunch | Signal Beam 33, Discharge 34, Bug Buzz 53, X-Scissor 53 | Vikavolt |
| Yanma | honey | 32 | Oxide | Detect, Supersonic, Uproar, Pursuit | AncientPower 33; as Yanmega: Feint 38, Slash 43, Screech 46, U-turn 49, Air Slash 54 | Yanmega (from 35) |
| Yanma | honey | 32 | v3 | Detect, Supersonic, Uproar, Pursuit | AncientPower 33; as Yanmega: Feint 38, Wing Attack 42, Slash 43, Screech 46, U-turn 49 | Yanmega (from 35) |

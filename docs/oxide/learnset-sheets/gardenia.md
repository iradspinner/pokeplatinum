# Gardenia's split: what each catch knows and learns

Written by `tools/oxide/balance/learncheck.py sheets` for check 6 of the learnset baseline (`docs/oxide/learnset-checks.md`). One table per capture area first offered in Gardenia's split, whose cap is 26. Each Pokemon is read at the lowest level it is found at there. "Knows at capture" is the last four moves its list gives by that level; "learns by level-up" is every entry it reaches after capture up to 26, evolving on time, with each later stage's moves under its name; "at the cap" is the stage it can be by then and the next one after. A row marked Rewrite shows the learnset rewrite's lists (the tree's) where it differs from the row marked Oxide, Oxide's lists before the learnset rewrite (`da6b92496c`); a row marked both is the same in each. Relearner-only moves and egg moves are left out.

## Eterna City

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 26 | At the cap |
|---|---|---|---|---|---|---|
| Popplio | in-game trade | 1 | Oxide | Pound, Water Gun | Disarming Voice 4, Baby-Doll Eyes 7, Life Dew 10, Aqua Jet 14; as Brionne: Icy Wind 19, Encore 24 | Brionne (from 16); Primarina in Maylene |
| Popplio | in-game trade | 1 | Rewrite | Pound, Water Gun | BubbleBeam 2, Disarming Voice 4, Baby-Doll Eyes 7, Life Dew 10, Aqua Jet 14; as Brionne: Icy Wind 19, Encore 24 | Brionne (from 16); Primarina in Maylene |
| Barboach | old rod | 10 | Oxide | Mud-Slap, Mud Sport, Water Sport, Water Gun | Mud Bomb 14, Amnesia 18, Water Pulse 22, Magnitude 26 | Barboach; Whiscash in Fantina |
| Barboach | old rod | 10 | Rewrite | Mud-Slap, Scary Face, Water Sport, Water Gun | Mud Bomb 14, Amnesia 18, Rock Tomb 20, Water Pulse 22, Magnitude 26 | Barboach; Whiscash in Fantina |
| Froakie | old rod | 10 | Oxide | Pound, Water Gun, Growl, Quick Attack | Lick 13, Water Pulse 14, Icy Wind 16; as Frogadier: Icy Wind 16, Faint Attack 20, Acrobatics 22, Low Kick 25 | Frogadier (from 16); Greninja in Maylene |
| Froakie | old rod | 10 | Rewrite | Pound, Water Gun, Quick Attack | Lick 13, Water Pulse 14, Icy Wind 16; as Frogadier: Icy Wind 16, Thief 19, Faint Attack 20, Acrobatics 22, Low Kick 25 | Frogadier (from 16); Greninja in Maylene |
| Goldeen | old rod | 10 | Oxide | Peck, Tail Whip, Water Sport, Supersonic | Horn Attack 11, Water Pulse 17, Flail 21 | Goldeen; Seaking in Fantina |
| Goldeen | old rod | 10 | Rewrite | Peck, Water Sport, Flip Turn, Water Pulse | Horn Attack 11, Swagger 17, Flail 21 | Goldeen; Seaking in Fantina |
| Lotad | old rod | 10 | Oxide | Astonish, Growl, Absorb, Nature Power | Mist 11; as Lombre: Fury Swipes 15, Water Sport 19, BubbleBeam 25 | Lombre (from 14); Ludicolo in Maylene |
| Lotad | old rod | 10 | Rewrite | Astonish, Magical Leaf, Water Gun | Mist 11, Disarming Voice 14; as Lombre: Fake Out 14, Fury Swipes 15, Natural Gift 16, Water Sport 19, Swagger 22, BubbleBeam 25 | Lombre (from 14); Ludicolo in Maylene |
| Shellos | old rod | 10 | Oxide | Mud-Slap, Mud Sport, Harden, Water Pulse | Mud Bomb 11, Hidden Power 16 | Shellos; Gastrodon in Fantina |
| Shellos | old rod | 10 | Rewrite | Mud-Slap, Harden, Water Pulse | Mud Bomb 11, Hidden Power 16, Swagger 22 | Shellos; Gastrodon in Fantina |

## Eterna Forest

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 26 | At the cap |
|---|---|---|---|---|---|---|
| Buneary | wild | 10 | Oxide | Pound, Defense Curl, Foresight, Endure | Frustration 13, Quick Attack 16; as Lopunny: Jump Kick 23, Baton Pass 26 | Lopunny (from 20) |
| Buneary | wild | 10 | Rewrite | Covet, Endure, Baby-Doll Eyes, Power-Up Punch | Return 12, Frustration 13, Quick Attack 16; as Lopunny: Jump Kick 23, Baton Pass 26 | Lopunny (from 20) |
| Budew | wild | 11 | Oxide | Absorb, Growth, Water Sport, Stun Spore | Mega Drain 13, Worry Seed 16 | Budew; Roselia in Fantina |
| Budew | wild | 11 | Rewrite | Razor Leaf, Acid, Water Sport, Stun Spore | Mega Drain 13, Magical Leaf 15, Worry Seed 16, Confusion 18, Venoshock 20, Giga Drain 25 | Budew; Roselia in Fantina |
| Murkrow | wild | 11 | Oxide | Peck, Astonish, Pursuit, Haze | Wing Attack 15, Night Shade 21, Assurance 25 | Murkrow; Honchkrow in Fantina |
| Murkrow | wild | 11 | Rewrite | Astonish, Pursuit, Twister, Taunt | Wing Attack 15, Chilling Water 18, Night Shade 21, Assurance 25 | Murkrow; Honchkrow in Fantina |
| Rowlet | wild | 11 | Oxide | Tackle, Leafage, Growl, Peck | Astonish 12, Razor Leaf 15; as Dartrix: Pluck 19, Ominous Wind 24 | Dartrix (from 16); Decidueye in Maylene |
| Rowlet | wild | 11 | Rewrite | Tackle, Leafage, Peck | Astonish 12, Ominous Wind 13, Spite 14, Razor Leaf 15; as Dartrix: Pluck 19, Ominous Wind 24 | Dartrix (from 16); Decidueye in Maylene |
| Seedot | wild | 11 | Oxide | Bide, Harden, Growth | Nature Power 13 | Shiftry (from 14) |
| Seedot | wild | 11 | Rewrite | Razor Leaf, Fake Out, Scary Face, Trailblaze | Giga Drain 14; as Nuzleaf: Payback 14 | Shiftry (from 14) |
| Sewaddle | wild | 11 to 12 | Oxide | Tackle, String Shot, Bug Bite | Razor Leaf 12 | Swadloon (from 20); Leavanny in Fantina |
| Sewaddle | wild | 11 to 12 | Rewrite | Tackle, Sticky Web, Bug Bite | Razor Leaf 12, Pounce 16; as Swadloon: Struggle Bug 22, Bite 26 | Swadloon (from 20); Leavanny in Fantina |
| Shroomish | wild | 11 to 13 | Oxide | Absorb, Tackle, Stun Spore | Leech Seed 13, Mega Drain 17, Headbutt 21; as Breloom: Mach Punch 23, Counter 25 | Breloom (from 23) |
| Shroomish | wild | 11 to 13 | Rewrite | Tackle, Magical Leaf, Stun Spore, Mach Punch | Leech Seed 13, Mega Drain 17, Headbutt 21; as Breloom: Mach Punch 23, PoisonPowder 24, Counter 25, Bulldoze 26 | Breloom (from 23) |
| Beautifly | wild | 12 | Oxide | Absorb | Gust 13, Stun Spore 17, Morning Sun 20, Mega Drain 24, Air Slash 26 | Beautifly |
| Beautifly | wild | 12 | Rewrite | Twister | Gust 13, Bug Bite 15, Stun Spore 17, Morning Sun 20, Mega Drain 24, Air Slash 26 | Beautifly |
| Burmy | wild | 12 | Oxide | Protect, Tackle | Bug Bite 15, Hidden Power 20; as Wormadam: Hidden Power 20, Confusion 23, Razor Leaf 26 | Wormadam (from 20) |
| Burmy | wild | 12 | Oxide | Protect, Tackle | Bug Bite 15, Hidden Power 20; as Mothim: Hidden Power 20, Confusion 23, Gust 26 | Mothim (from 20) |
| Burmy | wild | 12 | Rewrite | Tackle | Bug Bite 15, Confusion 17, Roost 18, Hidden Power 20; as Wormadam: Hidden Power 20, Razor Leaf 26 | Wormadam (from 20) |
| Burmy | wild | 12 | Rewrite | Tackle | Bug Bite 15, Confusion 17, Roost 18, Hidden Power 20; as Mothim: Hidden Power 20, Gust 26 | Mothim (from 20) |
| Combee | wild | 13 | Oxide | Sweet Scent, Gust, Bug Bite | as Vespiquen: Power Gem 21, Heal Order 25 | Vespiquen (from 21) |
| Combee | wild | 13 | Rewrite | Gust, Bug Bite | Pursuit 17, Roost 21; as Vespiquen: Power Gem 21, Poison Sting 22, Confuse Ray 23, Defend Order 24, Heal Order 25 | Vespiquen (from 21) |
| Steenee | wild | 13 | Oxide | DoubleSlap, Play Nice, Rapid Spin, Razor Leaf | Sweet Scent 17, Magical Leaf 21, Teeter Dance 23, Stomp 25 | Steenee; Tsareena in Fantina |
| Steenee | wild | 13 | Rewrite | DoubleSlap, Play Nice, Rapid Spin, Razor Leaf | Draining Kiss 17, Magical Leaf 21, Teeter Dance 23, Stomp 25 | Steenee; Tsareena in Fantina |

## Floaroma Town

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 26 | At the cap |
|---|---|---|---|---|---|---|
| Combee | wild | 10 | Oxide | Sweet Scent, Gust | Bug Bite 13; as Vespiquen: Power Gem 21, Heal Order 25 | Vespiquen (from 21) |
| Combee | wild | 10 | Rewrite | Gust | Bug Bite 13, Pursuit 17, Roost 21; as Vespiquen: Power Gem 21, Poison Sting 22, Confuse Ray 23, Defend Order 24, Heal Order 25 | Vespiquen (from 21) |
| Bounsweet | wild | 11 | Oxide | Splash, Play Nice, Rapid Spin | Razor Leaf 12; as Steenee: Razor Leaf 12, Sweet Scent 17, Magical Leaf 21, Teeter Dance 23, Stomp 25 | Steenee (from 12); Tsareena in Fantina |
| Bounsweet | wild | 11 | Rewrite | Magical Leaf, Taunt, Play Nice, Rapid Spin | Razor Leaf 12; as Steenee: Razor Leaf 12, Draining Kiss 17, Magical Leaf 21, Teeter Dance 23, Stomp 25 | Steenee (from 12); Tsareena in Fantina |
| Budew | wild | 11 | Oxide | Absorb, Growth, Water Sport, Stun Spore | Mega Drain 13, Worry Seed 16 | Budew; Roselia in Fantina |
| Budew | wild | 11 | Rewrite | Razor Leaf, Acid, Water Sport, Stun Spore | Mega Drain 13, Magical Leaf 15, Worry Seed 16, Confusion 18, Venoshock 20, Giga Drain 25 | Budew; Roselia in Fantina |
| Cherubi | wild | 11 | Oxide | Tackle, Growth, Leech Seed | Helping Hand 13, Magical Leaf 19; as Cherrim: Petal Dance 25 | Cherrim (from 25) |
| Cherubi | wild | 11 | Rewrite | Tackle, Leech Seed | Helping Hand 13, Magical Leaf 19, Stun Spore 22, Draining Kiss 25 | Cherrim (from 25) |
| Murkrow | wild | 11 | Oxide | Peck, Astonish, Pursuit, Haze | Wing Attack 15, Night Shade 21, Assurance 25 | Murkrow; Honchkrow in Fantina |
| Murkrow | wild | 11 | Rewrite | Astonish, Pursuit, Twister, Taunt | Wing Attack 15, Chilling Water 18, Night Shade 21, Assurance 25 | Murkrow; Honchkrow in Fantina |
| Aipom | wild | 12 | Oxide | Tail Whip, Sand-Attack, Astonish, Baton Pass | Tickle 15, Fury Swipes 18, Swift 22, Screech 25 | Aipom; Ambipom in Fantina |
| Aipom | wild | 12 | Rewrite | Tail Whip, Sand-Attack, Astonish, Baton Pass | Tickle 15, Fury Swipes 18, Bite 20, Swift 22, Screech 25 | Aipom; Ambipom in Fantina |
| Hoppip | wild | 12 | Oxide | Synthesis, Tail Whip, Tackle, PoisonPowder | Stun Spore 14, Sleep Powder 16; as Skiploom: Bullet Seed 20, Leech Seed 24 | Skiploom (from 18); Jumpluff in Fantina |
| Hoppip | wild | 12 | Rewrite | Synthesis, Tackle | Silver Wind 13, Stun Spore 14, Sleep Powder 16, Magical Leaf 17, Acrobatics 18; as Skiploom: Bullet Seed 20, Leech Seed 24, Mega Drain 25 | Skiploom (from 18); Jumpluff in Fantina |
| Poochyena | wild | 12 | Oxide | Tackle, Howl, Sand-Attack | Bite 13, Odor Sleuth 17; as Mightyena: Roar 22 | Mightyena (from 18) |
| Poochyena | wild | 12 | Rewrite | Tackle, Howl, Scary Face, Sand-Attack | Bite 13, Odor Sleuth 17; as Mightyena: Trailblaze 19, Roar 22, Swagger 25 | Mightyena (from 18) |
| Tropius | wild | 12 | Oxide | Leer, Gust, Growth, Razor Leaf | Stomp 17, Sweet Scent 21 | Tropius |
| Tropius | wild | 12 | Rewrite | Leer, Gust, Razor Leaf | Stomp 17, Bulldoze 22 | Tropius |
| Chingling | wild | 13 | Oxide | Wrap, Growl, Astonish | Confusion 14, Uproar 17; as Chimecho: Take Down 22, Yawn 25 | Chimecho (from 20) |
| Chingling | wild | 13 | Rewrite | Growl, Astonish | Confusion 14, Uproar 17, Snarl 18; as Chimecho: Last Resort 20, Take Down 22, Yawn 25 | Chimecho (from 20) |
| Pachirisu | wild | 13 | Oxide | Bide, Quick Attack, Charm, Spark | Endure 17, Swift 21, Sweet Kiss 25 | Pachirisu |
| Pachirisu | wild | 13 | Rewrite | Quick Attack, Electroweb, Charm, Spark | Endure 17, Bite 19, Swift 21, Sweet Kiss 25 | Pachirisu |
| Skitty | wild | 13 | Oxide | Tackle, Foresight, Attract, Sing | nothing | Delcatty (from 13) |
| Skitty | wild | 13 | Rewrite | Baby-Doll Eyes, Attract, Sing, Quick Attack | as Delcatty: Faint Attack 25 | Delcatty (from 13) |

## Mt. Coronet

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 26 | At the cap |
|---|---|---|---|---|---|---|
| Feebas | special tile (rod) | 10 | Oxide | Splash | Tackle 15 | Feebas; Milotic in Fantina |
| Feebas | special tile (rod) | 10 | Rewrite | Whirlpool, Water Gun | Water Pulse 13, Tackle 15, Recover 21, Dragon Tail 24, Captivate 25 | Feebas; Milotic in Fantina |

## Mt. Coronet North

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 26 | At the cap |
|---|---|---|---|---|---|---|
| Bronzor | wild | 13 | Oxide | Tackle, Confusion, Hypnosis, Imprison | Confuse Ray 14, Extrasensory 19, Iron Defense 26 | Bronzor; Bronzong in Fantina |
| Bronzor | wild | 13 | Rewrite | Tackle, Confusion, Hypnosis, Imprison | Confuse Ray 14, Smart Strike 17, Extrasensory 19, Bulldoze 22, Iron Defense 26 | Bronzor; Bronzong in Fantina |
| Alolan Ninetales | wild | 14 to 15 | Oxide | Tail Whip, Disable, Ice Shard, Safeguard | nothing | Alolan Ninetales |
| Alolan Ninetales | wild | 14 to 15 | Rewrite | Tail Whip, Disable, Ice Shard, Safeguard | Draining Kiss 17, Incinerate 18, Spite 26 | Alolan Ninetales |
| Clefairy | wild | 14 | Oxide | Encore, Sing, DoubleSlap, Defense Curl | nothing | Clefable (from 14) |
| Clefairy | wild | 14 | Rewrite | Growl, Encore, Sing, Magical Leaf | as Clefable: Play Rough 17 | Clefable (from 14) |
| Makuhita | wild | 14 to 16 | Oxide | Sand-Attack, Arm Thrust, Vital Throw, Fake Out | Whirlwind 16, Knock Off 19, SmellingSalt 22 | Hariyama (from 24) |
| Makuhita | wild | 14 to 16 | Rewrite | Bullet Punch, Arm Thrust, Vital Throw, Fake Out | Whirlwind 16, Knock Off 19, SmellingSalt 22; as Hariyama: Belly Drum 25 | Hariyama (from 24) |
| Phanpy | wild | 14 to 16 | Oxide | Growl, Defense Curl, Flail, Take Down | Rollout 15, Natural Gift 19, Slam 24; as Donphan: Fury Attack 25 | Donphan (from 25) |
| Phanpy | wild | 14 to 16 | Rewrite | Flail, Knock Off, Take Down, Bulldoze | Rollout 15, Natural Gift 19, Slam 24; as Donphan: Rapid Spin 25, Magnitude 26 | Donphan (from 25) |
| Snorunt | wild | 14 | Oxide | Leer, Double Team, Bite, Icy Wind | Headbutt 19, Protect 22 | Snorunt; Glalie in Wake, Froslass in Byron |
| Snorunt | wild | 14 | Rewrite | Powder Snow, Leer, Bite, Icy Wind | Headbutt 19, Ominous Wind 22 | Snorunt; Glalie in Wake, Froslass in Byron |
| Zubat | wild | 14 | Oxide | Leech Life, Supersonic, Astonish, Bite | Wing Attack 17, Confuse Ray 21 | Golbat (from 22); Crobat in Wake |
| Zubat | wild | 14 | Rewrite | Wing Attack, Astonish, Screech, Bite | Venoshock 16, Confuse Ray 21; as Golbat: Air Cutter 25 | Golbat (from 22); Crobat in Wake |
| Carbink | wild | 15 | Oxide | Rock Throw, Sharpen, Smack Down, Guard Split | Reflect 18, Flail 24, AncientPower 25, Rock Polish 25 | Carbink |
| Carbink | wild | 15 | Rewrite | Tackle, Rock Throw, Smack Down, Guard Split | Bulldoze 17, Reflect 18, Draining Kiss 21, Flail 24, AncientPower 25, Rock Polish 26 | Carbink |
| Nosepass | wild | 15 | Oxide | Tackle, Harden, Rock Throw | Block 19, Thunder Wave 25 | Nosepass; Probopass in Fantina |
| Nosepass | wild | 15 | Rewrite | Tackle, Iron Defense, Smack Down, Rock Throw | Rock Tomb 16, Block 19, Bulldoze 22, Thunder Wave 25 | Nosepass; Probopass in Fantina |
| Swinub | wild | 15 | Oxide | Odor Sleuth, Mud Sport, Powder Snow, Mud-Slap | Endure 16, Mud Bomb 20, Icy Wind 25 | Swinub; Piloswine in Fantina |
| Swinub | wild | 15 | Rewrite | Tackle, Odor Sleuth, Powder Snow, Mud-Slap | Endure 16, Bite 18, Mud Bomb 20, Icy Wind 25 | Swinub; Piloswine in Fantina |
| Snover | wild | 16 | Oxide | Leer, Razor Leaf, Icy Wind, GrassWhistle | Swagger 17, Mist 21, Ice Shard 26 | Snover; Abomasnow in Wake |
| Snover | wild | 16 | Rewrite | Powder Snow, Razor Leaf, Icy Wind, GrassWhistle | Swagger 17, Bulldoze 19, Mist 21, Ice Shard 26 | Snover; Abomasnow in Wake |

## Oreburgh Gate

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 26 | At the cap |
|---|---|---|---|---|---|---|
| Barboach | old rod | 6 | Oxide | Mud-Slap, Mud Sport, Water Sport | Water Gun 10, Mud Bomb 14, Amnesia 18, Water Pulse 22, Magnitude 26 | Barboach; Whiscash in Fantina |
| Barboach | old rod | 6 | Rewrite | Mud-Slap, Scary Face, Water Sport | Water Gun 10, Mud Bomb 14, Amnesia 18, Rock Tomb 20, Water Pulse 22, Magnitude 26 | Barboach; Whiscash in Fantina |
| Clamperl | old rod | 6 | both | Clamp, Water Gun, Whirlpool, Iron Defense | as Huntail: Bite 6, Screech 10, Water Pulse 15, Scary Face 19, Ice Fang 24 | Huntail (from 6) |
| Clamperl | old rod | 6 | both | Clamp, Water Gun, Whirlpool, Iron Defense | as Gorebyss: Confusion 6, Agility 10, Water Pulse 15, Amnesia 19, Aqua Ring 24 | Gorebyss (from 6) |
| Feebas | old rod | 6 | Oxide | Splash | Tackle 15 | Feebas; Milotic in Fantina |
| Feebas | old rod | 6 | Rewrite | Whirlpool | Water Gun 9, Water Pulse 13, Tackle 15, Recover 21, Dragon Tail 24, Captivate 25 | Feebas; Milotic in Fantina |
| Geodude | wild | 6 to 9 | Oxide | Tackle, Defense Curl, Mud Sport | Rock Polish 8, Rock Throw 11, Magnitude 15, Selfdestruct 18, Rollout 22, Rock Blast 25 | Graveler (from 25); Golem in Wake |
| Geodude | wild | 6 to 9 | Rewrite | Tackle, Smack Down | Rock Throw 11, Bulldoze 12, Magnitude 15, Rock Polish 17, Rollout 22, Rock Blast 25; as Graveler: Karate Chop 25 | Graveler (from 25); Golem in Wake |
| Shellos | old rod | 6 | Oxide | Mud-Slap, Mud Sport, Harden | Water Pulse 7, Mud Bomb 11, Hidden Power 16 | Shellos; Gastrodon in Fantina |
| Shellos | old rod | 6 | Rewrite | Mud-Slap, Harden | Water Pulse 7, Mud Bomb 11, Hidden Power 16, Swagger 22 | Shellos; Gastrodon in Fantina |
| Squirtle | old rod | 6 | Oxide | Tackle, Tail Whip | Bubble 7, Withdraw 10, Water Gun 13, Bite 16; as Wartortle: Bite 16, Rapid Spin 20, Protect 24 | Wartortle (from 16); Blastoise in Maylene |
| Squirtle | old rod | 6 | Rewrite | Tackle, Life Dew | Bubble 7, Water Gun 13, Water Pulse 15, Bite 16; as Wartortle: Bite 16, Rapid Spin 20, Icy Wind 24 | Wartortle (from 16); Blastoise in Maylene |
| Dwebble | wild | 7 | both | Struggle Bug, Rock Blast, Block | Sand-Attack 10, Faint Attack 14, Slash 17, Rock Tomb 21, Bug Bite 24 | Dwebble; Crustle in Maylene |
| Phanpy | wild | 7 | Oxide | Tackle, Growl, Defense Curl, Flail | Take Down 10, Rollout 15, Natural Gift 19, Slam 24; as Donphan: Fury Attack 25 | Donphan (from 25) |
| Phanpy | wild | 7 | Rewrite | Odor Sleuth, Tackle, Flail | Knock Off 9, Take Down 10, Bulldoze 14, Rollout 15, Natural Gift 19, Slam 24; as Donphan: Rapid Spin 25, Magnitude 26 | Donphan (from 25) |
| Rhyhorn | wild | 7 to 8 | Oxide | Horn Attack, Tail Whip | Stomp 9, Fury Attack 13, Scary Face 21, Rock Blast 25 | Rhyhorn; Rhydon in Wake |
| Rhyhorn | wild | 7 to 8 | Rewrite | Horn Attack, Tail Whip | Stomp 9, Bulldoze 10, Peck 13, Smack Down 16, Bite 18, Scary Face 21, Rock Blast 25 | Rhyhorn; Rhydon in Wake |
| Carbink | wild | 8 | Oxide | Tackle, Harden, Rock Throw, Sharpen | Smack Down 10, Guard Split 15, Reflect 18, Flail 24, AncientPower 25, Rock Polish 25 | Carbink |
| Carbink | wild | 8 | Rewrite | Tackle, Rock Throw | Smack Down 10, Guard Split 15, Bulldoze 17, Reflect 18, Draining Kiss 21, Flail 24, AncientPower 25, Rock Polish 26 | Carbink |
| Glimmet | wild | 8 | Oxide | Rock Throw, Harden, Smack Down, Acid Spray | AncientPower 11, Rock Polish 15, Stealth Rock 18, Venoshock 22 | Glimmet; Glimmora in Maylene |
| Glimmet | wild | 8 | Rewrite | Rock Throw, Harden, Smack Down, Acid Spray | AncientPower 11, Rock Polish 15, Stealth Rock 18, Venoshock 22, Mud Shot 26 | Glimmet; Glimmora in Maylene |
| Mudkip | wild | 8 | Oxide | Tackle, Growl, Mud-Slap | Water Gun 10, Bide 15; as Marshtomp: Mud Shot 16, Foresight 20, Mud Bomb 25 | Marshtomp (from 16); Swampert in Maylene |
| Mudkip | wild | 8 | Rewrite | Tackle, Mud-Slap | Water Gun 10, Screech 13, Water Pulse 16; as Marshtomp: Mud Shot 16, Rock Throw 18, Foresight 20, Mud Bomb 25 | Marshtomp (from 16); Swampert in Maylene |
| Nacli | wild | 9 | Oxide | Tackle, Harden, Rock Throw, Mud Shot | Smack Down 10, Rock Polish 13, Headbutt 16, Iron Defense 20 | Naclstack (from 24); Garganacl in Maylene |
| Nacli | wild | 9 | Rewrite | Tackle, Rock Throw, Mud Shot | Smack Down 10, Headbutt 16, Iron Defense 20; as Naclstack: Bulldoze 24, Recover 25 | Naclstack (from 24); Garganacl in Maylene |
| Onix | wild | 9 | Oxide | Harden, Bind, Screech, Rock Throw | as Steelix: Rock Throw 9, Rage 14, Rock Tomb 17, Slam 25 | Steelix (from 9) |
| Onix | wild | 9 | Rewrite | Tackle, Screech, Rock Throw | as Steelix: Rock Throw 9, Rock Tomb 17, Metal Claw 21, Slam 25 | Steelix (from 9) |

## Route 204

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 26 | At the cap |
|---|---|---|---|---|---|---|
| Barboach | old rod | 8 | Oxide | Mud-Slap, Mud Sport, Water Sport | Water Gun 10, Mud Bomb 14, Amnesia 18, Water Pulse 22, Magnitude 26 | Barboach; Whiscash in Fantina |
| Barboach | old rod | 8 | Rewrite | Mud-Slap, Scary Face, Water Sport | Water Gun 10, Mud Bomb 14, Amnesia 18, Rock Tomb 20, Water Pulse 22, Magnitude 26 | Barboach; Whiscash in Fantina |
| Corphish | old rod | 8 | Oxide | Bubble, Harden | ViceGrip 10, Leer 13, BubbleBeam 20, Protect 23, Knock Off 26 | Corphish; Crawdaunt in Fantina |
| Corphish | old rod | 8 | Rewrite | Bubble, Taunt | ViceGrip 10, BubbleBeam 12, Leer 13, Razor Shell 17, Knock Off 26 | Corphish; Crawdaunt in Fantina |
| Froakie | old rod | 8 | Oxide | Pound, Water Gun, Growl | Quick Attack 10, Lick 13, Water Pulse 14, Icy Wind 16; as Frogadier: Icy Wind 16, Faint Attack 20, Acrobatics 22, Low Kick 25 | Frogadier (from 16); Greninja in Maylene |
| Froakie | old rod | 8 | Rewrite | Pound, Water Gun | Quick Attack 10, Lick 13, Water Pulse 14, Icy Wind 16; as Frogadier: Icy Wind 16, Thief 19, Faint Attack 20, Acrobatics 22, Low Kick 25 | Frogadier (from 16); Greninja in Maylene |
| Goldeen | old rod | 8 | Oxide | Peck, Tail Whip, Water Sport, Supersonic | Horn Attack 11, Water Pulse 17, Flail 21 | Goldeen; Seaking in Fantina |
| Goldeen | old rod | 8 | Rewrite | Peck, Water Sport, Flip Turn | Water Pulse 10, Horn Attack 11, Swagger 17, Flail 21 | Goldeen; Seaking in Fantina |
| Lotad | old rod | 8 | Oxide | Astonish, Growl, Absorb, Nature Power | Mist 11; as Lombre: Fury Swipes 15, Water Sport 19, BubbleBeam 25 | Lombre (from 14); Ludicolo in Maylene |
| Lotad | old rod | 8 | Rewrite | Astonish, Magical Leaf, Water Gun | Mist 11, Disarming Voice 14; as Lombre: Fake Out 14, Fury Swipes 15, Natural Gift 16, Water Sport 19, Swagger 22, BubbleBeam 25 | Lombre (from 14); Ludicolo in Maylene |
| Sewaddle | wild | 8 to 11 | Oxide | Tackle, String Shot, Bug Bite | Razor Leaf 12 | Swadloon (from 20); Leavanny in Fantina |
| Sewaddle | wild | 8 to 11 | Rewrite | Tackle, Sticky Web, Bug Bite | Razor Leaf 12, Pounce 16; as Swadloon: Struggle Bug 22, Bite 26 | Swadloon (from 20); Leavanny in Fantina |
| Budew | wild | 9 | Oxide | Absorb, Growth, Water Sport | Stun Spore 10, Mega Drain 13, Worry Seed 16 | Budew; Roselia in Fantina |
| Budew | wild | 9 | Rewrite | Razor Leaf, Acid, Water Sport | Stun Spore 10, Mega Drain 13, Magical Leaf 15, Worry Seed 16, Confusion 18, Venoshock 20, Giga Drain 25 | Budew; Roselia in Fantina |
| Litten | wild | 9 | Oxide | Scratch, Ember, Growl | Lick 10, Fire Fang 14, Double Kick 16; as Torracat: Double Kick 16, Bite 21, Scary Face 25 | Torracat (from 16); Incineroar in Maylene |
| Litten | wild | 9 | Rewrite | Scratch, Ember | Lick 10, Swagger 12, Fire Fang 14, Double Kick 16; as Torracat: Double Kick 16, Bite 21, Scary Face 25 | Torracat (from 16); Incineroar in Maylene |
| Poochyena | wild | 9 | Oxide | Tackle, Howl, Sand-Attack | Bite 13, Odor Sleuth 17; as Mightyena: Roar 22 | Mightyena (from 18) |
| Poochyena | wild | 9 | Rewrite | Tackle, Howl, Scary Face, Sand-Attack | Bite 13, Odor Sleuth 17; as Mightyena: Trailblaze 19, Roar 22, Swagger 25 | Mightyena (from 18) |
| Purrloin | wild | 9 | Oxide | Scratch, Growl, Sand-Attack, Assist | Fake Out 12, Fury Swipes 12, Pursuit 15, Torment 17; as Liepard: Fake Out 22, Assurance 26 | Liepard (from 20) |
| Purrloin | wild | 9 | Rewrite | Scratch, Taunt, Sand-Attack, Snarl | Fury Swipes 11, Fake Out 12, Pursuit 15, Torment 17; as Liepard: Trailblaze 20, Fake Out 22, Hone Claws 24, Assurance 26 | Liepard (from 20) |
| Torchic | wild | 9 | Oxide | Scratch, Growl, Focus Energy | Ember 10, Peck 16; as Combusken: Double Kick 16, Peck 17, Sand-Attack 21 | Combusken (from 16); Blaziken in Maylene |
| Torchic | wild | 9 | Rewrite | Scratch | Ember 10, Swagger 11, Flame Charge 13, Peck 16; as Combusken: Double Kick 16, Peck 17, Sand-Attack 21, Rolling Kick 24 | Combusken (from 16); Blaziken in Maylene |
| Treecko | wild | 9 | Oxide | Pound, Leer, Absorb | Quick Attack 11, Pursuit 16; as Grovyle: Fury Cutter 16, Pursuit 17, Screech 23 | Grovyle (from 16); Sceptile in Maylene |
| Treecko | wild | 9 | Rewrite | Pound | DragonBreath 10, Quick Attack 11, Screech 12, Giga Drain 13, Pursuit 16; as Grovyle: Fury Cutter 16, Pursuit 17, Screech 23 | Grovyle (from 16); Sceptile in Maylene |
| Bounsweet | wild | 10 to 11 | Oxide | Splash, Play Nice, Rapid Spin | Razor Leaf 12; as Steenee: Razor Leaf 12, Sweet Scent 17, Magical Leaf 21, Teeter Dance 23, Stomp 25 | Steenee (from 12); Tsareena in Fantina |
| Bounsweet | wild | 10 to 11 | Rewrite | Magical Leaf, Taunt, Play Nice, Rapid Spin | Razor Leaf 12; as Steenee: Razor Leaf 12, Draining Kiss 17, Magical Leaf 21, Teeter Dance 23, Stomp 25 | Steenee (from 12); Tsareena in Fantina |
| Snivy | wild | 10 | Oxide | Tackle, Vine Whip, Leer, Wrap | Hold Back 14; as Servine: Magical Leaf 19, Mega Drain 24 | Servine (from 16); Serperior in Maylene |
| Snivy | wild | 10 | Rewrite | Tackle, Vine Whip, Calm Mind, Twister | Hold Back 14, Magical Leaf 16; as Servine: Aerial Ace 17, Magical Leaf 19, Mega Drain 24 | Servine (from 16); Serperior in Maylene |
| Snubbull | wild | 10 to 11 | Oxide | Scary Face, Tail Whip, Charm, Bite | Lick 13, Headbutt 19 | Granbull (from 23) |
| Snubbull | wild | 10 to 11 | Rewrite | Scary Face, Tail Whip, Charm, Bite | Lick 13, Headbutt 19, Dazzling Gleam 23 | Granbull (from 23) |

## Route 205

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 26 | At the cap |
|---|---|---|---|---|---|---|
| Buizel | old rod | 8 to 10 | Oxide | Growl, Water Sport, Quick Attack, Water Gun | Pursuit 10, Swift 15, Aqua Jet 21; as Floatzel: Crunch 26 | Floatzel (from 26) |
| Buizel | old rod | 8 to 10 | Rewrite | Water Sport, Quick Attack, Water Gun, BubbleBeam | Pursuit 10, Scary Face 12, Swift 15, Aqua Jet 21; as Floatzel: Crunch 26 | Floatzel (from 26) |
| Carvanha | old rod | 8 to 10 | Oxide | Leer, Bite, Rage, Focus Energy | Scary Face 11, Ice Fang 16, Screech 18, Swagger 21, Assurance 26 | Carvanha; Sharpedo in Fantina |
| Carvanha | old rod | 8 to 10 | Rewrite | Leer, Bite, Focus Energy | Scary Face 11, Ice Fang 16, Screech 18, Swagger 21, Aqua Cutter 23, Assurance 26 | Carvanha; Sharpedo in Fantina |
| Chinchou | old rod | 8 to 10 | Oxide | Bubble, Supersonic, Thunder Wave | Flail 9, Water Gun 12, Confuse Ray 17, Spark 20, Take Down 23 | Chinchou; Lanturn in Fantina |
| Chinchou | old rod | 8 to 10 | Rewrite | Bubble, Supersonic, Shock Wave, Thunder Wave | Flail 9, Water Gun 12, Screech 14, Confuse Ray 17, Spark 20, Take Down 23, Icy Wind 26 | Chinchou; Lanturn in Fantina |
| Psyduck | old rod | 8 | Oxide | Water Sport, Scratch, Tail Whip | Water Gun 9, Disable 14, Confusion 18, Water Pulse 22 | Psyduck; Golduck in Fantina |
| Psyduck | old rod | 8 | Rewrite | Scratch, Screech, Trailblaze | Water Gun 9, Water Pulse 12, Disable 14, Confusion 18, Low Sweep 22 | Psyduck; Golduck in Fantina |
| Squirtle | old rod | 8 | Oxide | Tackle, Tail Whip, Bubble | Withdraw 10, Water Gun 13, Bite 16; as Wartortle: Bite 16, Rapid Spin 20, Protect 24 | Wartortle (from 16); Blastoise in Maylene |
| Squirtle | old rod | 8 | Rewrite | Tackle, Life Dew, Bubble | Water Gun 13, Water Pulse 15, Bite 16; as Wartortle: Bite 16, Rapid Spin 20, Icy Wind 24 | Wartortle (from 16); Blastoise in Maylene |
| Pachirisu | wild | 9 | Oxide | Growl, Bide, Quick Attack, Charm | Spark 13, Endure 17, Swift 21, Sweet Kiss 25 | Pachirisu |
| Pachirisu | wild | 9 | Rewrite | Growl, Quick Attack, Electroweb, Charm | Spark 13, Endure 17, Bite 19, Swift 21, Sweet Kiss 25 | Pachirisu |
| Aipom | wild | 10 | Oxide | Scratch, Tail Whip, Sand-Attack, Astonish | Baton Pass 11, Tickle 15, Fury Swipes 18, Swift 22, Screech 25 | Aipom; Ambipom in Fantina |
| Aipom | wild | 10 | Rewrite | Scratch, Tail Whip, Sand-Attack, Astonish | Baton Pass 11, Tickle 15, Fury Swipes 18, Bite 20, Swift 22, Screech 25 | Aipom; Ambipom in Fantina |
| Barboach | old rod | 10 | Oxide | Mud-Slap, Mud Sport, Water Sport, Water Gun | Mud Bomb 14, Amnesia 18, Water Pulse 22, Magnitude 26 | Barboach; Whiscash in Fantina |
| Barboach | old rod | 10 | Rewrite | Mud-Slap, Scary Face, Water Sport, Water Gun | Mud Bomb 14, Amnesia 18, Rock Tomb 20, Water Pulse 22, Magnitude 26 | Barboach; Whiscash in Fantina |
| Buneary | wild | 10 | Oxide | Pound, Defense Curl, Foresight, Endure | Frustration 13, Quick Attack 16; as Lopunny: Jump Kick 23, Baton Pass 26 | Lopunny (from 20) |
| Buneary | wild | 10 | Rewrite | Covet, Endure, Baby-Doll Eyes, Power-Up Punch | Return 12, Frustration 13, Quick Attack 16; as Lopunny: Jump Kick 23, Baton Pass 26 | Lopunny (from 20) |
| Minccino | wild | 10 | Oxide | Pound, Baby-Doll Eyes, Helping Hand | DoubleSlap 13, Sing 16, Echoed Voice 19, Swift 19, Encore 19, Charm 21, Tickle 23 | Minccino; Cinccino in Wake |
| Minccino | wild | 10 | Rewrite | Baby-Doll Eyes, Helping Hand, Chilling Water, Swift | DoubleSlap 13, Sing 16, Encore 19, Charm 21, Tickle 23 | Minccino; Cinccino in Wake |
| Mudkip | old rod | 10 | Oxide | Tackle, Growl, Mud-Slap, Water Gun | Bide 15; as Marshtomp: Mud Shot 16, Foresight 20, Mud Bomb 25 | Marshtomp (from 16); Swampert in Maylene |
| Mudkip | old rod | 10 | Rewrite | Tackle, Mud-Slap, Water Gun | Screech 13, Water Pulse 16; as Marshtomp: Mud Shot 16, Rock Throw 18, Foresight 20, Mud Bomb 25 | Marshtomp (from 16); Swampert in Maylene |
| Poochyena | wild | 10 | Oxide | Tackle, Howl, Sand-Attack | Bite 13, Odor Sleuth 17; as Mightyena: Roar 22 | Mightyena (from 18) |
| Poochyena | wild | 10 | Rewrite | Tackle, Howl, Scary Face, Sand-Attack | Bite 13, Odor Sleuth 17; as Mightyena: Trailblaze 19, Roar 22, Swagger 25 | Mightyena (from 18) |
| Skitty | wild | 10 | Oxide | Tail Whip, Tackle, Foresight, Attract | nothing | Delcatty (from 10) |
| Skitty | wild | 10 | Rewrite | Tackle, Foresight, Baby-Doll Eyes, Attract | as Delcatty: Faint Attack 25 | Delcatty (from 10) |
| Smoliv | wild | 10 | Oxide | Sweet Scent, Absorb, Growth, Razor Leaf | Helping Hand 13, Flail 16, Mega Drain 20, Grassy Terrain 23 | Dolliv (from 25); Arboliva in Maylene |
| Smoliv | wild | 10 | Rewrite | Tackle, Terrain Pulse, Razor Leaf | Helping Hand 13, Flail 16, Mega Drain 20; as Dolliv: Charm 25, Mud Shot 26 | Dolliv (from 25); Arboliva in Maylene |
| Bounsweet | wild | 11 | Oxide | Splash, Play Nice, Rapid Spin | Razor Leaf 12; as Steenee: Razor Leaf 12, Sweet Scent 17, Magical Leaf 21, Teeter Dance 23, Stomp 25 | Steenee (from 12); Tsareena in Fantina |
| Bounsweet | wild | 11 | Rewrite | Magical Leaf, Taunt, Play Nice, Rapid Spin | Razor Leaf 12; as Steenee: Razor Leaf 12, Draining Kiss 17, Magical Leaf 21, Teeter Dance 23, Stomp 25 | Steenee (from 12); Tsareena in Fantina |
| Fletchling | wild | 11 | Oxide | Tackle, Growl, Quick Attack | Aerial Ace 12; as Fletchinder: Flame Charge 17, Roost 22 | Fletchinder (from 16); Talonflame in Maylene |
| Fletchling | wild | 11 | Rewrite | Tackle, Quick Attack, Ember | Aerial Ace 12, Tailwind 16; as Fletchinder: Flame Charge 17, Bite 19, Roost 22 | Fletchinder (from 16); Talonflame in Maylene |
| Mareep | wild | 11 | Oxide | Tackle, Growl, ThunderShock | Thunder Wave 14; as Flaaffy: Cotton Spore 20, Charge 25 | Flaaffy (from 15); Ampharos in Fantina |
| Mareep | wild | 11 | Rewrite | Tackle, ThunderShock | Shock Wave 12, Swagger 13, Thunder Wave 14, AncientPower 15; as Flaaffy: Cotton Spore 20, Charge 25 | Flaaffy (from 15); Ampharos in Fantina |
| Sewaddle | wild | 11 to 13 | Oxide | Tackle, String Shot, Bug Bite | Razor Leaf 12 | Swadloon (from 20); Leavanny in Fantina |
| Sewaddle | wild | 11 to 13 | Rewrite | Tackle, Sticky Web, Bug Bite | Razor Leaf 12, Pounce 16; as Swadloon: Struggle Bug 22, Bite 26 | Swadloon (from 20); Leavanny in Fantina |
| Combee | wild | 12 | Oxide | Sweet Scent, Gust | Bug Bite 13; as Vespiquen: Power Gem 21, Heal Order 25 | Vespiquen (from 21) |
| Combee | wild | 12 | Rewrite | Gust | Bug Bite 13, Pursuit 17, Roost 21; as Vespiquen: Power Gem 21, Poison Sting 22, Confuse Ray 23, Defend Order 24, Heal Order 25 | Vespiquen (from 21) |
| Lotad | wild | 12 | Oxide | Growl, Absorb, Nature Power, Mist | as Lombre: Fury Swipes 15, Water Sport 19, BubbleBeam 25 | Lombre (from 14); Ludicolo in Maylene |
| Lotad | wild | 12 | Rewrite | Astonish, Magical Leaf, Water Gun, Mist | Disarming Voice 14; as Lombre: Fake Out 14, Fury Swipes 15, Natural Gift 16, Water Sport 19, Swagger 22, BubbleBeam 25 | Lombre (from 14); Ludicolo in Maylene |
| Pawmi | wild | 12 | Oxide | Growl, ThunderShock, Quick Attack, Nuzzle | as Pawmo: Bite 19, Spark 23, Arm Thrust 25 | Pawmo (from 18); Pawmot in Maylene |
| Pawmi | wild | 12 | Rewrite | ThunderShock, Quick Attack, Electroweb, Nuzzle | Mach Punch 15; as Pawmo: Bite 19, Spark 23, Arm Thrust 25 | Pawmo (from 18); Pawmot in Maylene |
| Pikachu | wild | 12 | Oxide | ThunderShock, Growl, Tail Whip, Thunder Wave | Quick Attack 13, Double Team 18, Slam 21, Thunderbolt 26 | Pikachu; Raichu in Maylene |
| Pikachu | wild | 12 | Rewrite | ThunderShock, Tail Whip, Thunder Wave, Sweet Kiss | Quick Attack 13, Trailblaze 17, Slam 21, Thunderbolt 26 | Pikachu; Raichu in Maylene |
| Cherubi | wild | 13 | Oxide | Tackle, Growth, Leech Seed, Helping Hand | Magical Leaf 19; as Cherrim: Petal Dance 25 | Cherrim (from 25) |
| Cherubi | wild | 13 | Rewrite | Tackle, Leech Seed, Helping Hand | Magical Leaf 19, Stun Spore 22, Draining Kiss 25 | Cherrim (from 25) |
| Hoppip | wild | 13 | Oxide | Synthesis, Tail Whip, Tackle, PoisonPowder | Stun Spore 14, Sleep Powder 16; as Skiploom: Bullet Seed 20, Leech Seed 24 | Skiploom (from 18); Jumpluff in Fantina |
| Hoppip | wild | 13 | Rewrite | Synthesis, Tackle, Silver Wind | Stun Spore 14, Sleep Powder 16, Magical Leaf 17, Acrobatics 18; as Skiploom: Bullet Seed 20, Leech Seed 24, Mega Drain 25 | Skiploom (from 18); Jumpluff in Fantina |
| Squirtle | wild | 13 | Oxide | Tail Whip, Bubble, Withdraw, Water Gun | Bite 16; as Wartortle: Bite 16, Rapid Spin 20, Protect 24 | Wartortle (from 16); Blastoise in Maylene |
| Squirtle | wild | 13 | Rewrite | Tackle, Life Dew, Bubble, Water Gun | Water Pulse 15, Bite 16; as Wartortle: Bite 16, Rapid Spin 20, Icy Wind 24 | Wartortle (from 16); Blastoise in Maylene |
| Surskit | wild | 13 | Oxide | Bubble, Quick Attack, Sweet Scent | Water Sport 19; as Masquerain: Gust 22, Scary Face 26 | Masquerain (from 22) |
| Surskit | wild | 13 | Rewrite | Sticky Web, Quick Attack, Gust, Silver Wind | Water Sport 19; as Masquerain: Gust 22, BubbleBeam 25, Scary Face 26 | Masquerain (from 22) |
| Wooper | wild | 13 to 14 | Oxide | Water Gun, Tail Whip, Mud Sport, Mud Shot | Slam 15, Mud Bomb 19; as Quagsire: Amnesia 24 | Quagsire (from 20) |
| Wooper | wild | 13 to 14 | Oxide | Water Gun, Tail Whip, Mud Sport, Mud Shot | as Clodsire: Slam 16, Yawn 21, Bulldoze 24 | Clodsire (from 13) |
| Wooper | wild | 13 to 14 | Rewrite | Water Gun, Tail Whip, Poison Sting, Mud Shot | Slam 15, Mud Bomb 19; as Quagsire: Amnesia 24 | Quagsire (from 20) |
| Wooper | wild | 13 to 14 | Rewrite | Water Gun, Tail Whip, Poison Sting, Mud Shot | as Clodsire: Slam 16, Rock Tomb 18, Yawn 21, Bulldoze 24 | Clodsire (from 13) |
| Dewpider | wild | 14 | Oxide | Bubble, Infestation, Bite, Aqua Ring | BubbleBeam 17, Bug Bite 21; as Araquanid: Headbutt 26 | Araquanid (from 22) |
| Dewpider | wild | 14 | Rewrite | Bubble, Infestation, Bite, Aqua Ring | BubbleBeam 17, Sticky Web 19, Bug Bite 21; as Araquanid: Headbutt 26 | Araquanid (from 22) |
| Marill | wild | 14 | Oxide | Tackle, Defense Curl, Tail Whip, Water Gun | Rollout 15, BubbleBeam 18; as Azumarill: BubbleBeam 20 | Azumarill (from 18) |
| Marill | wild | 14 | Rewrite | Tackle, Water Gun, Slam | Rollout 15, Bulldoze 16, Charm 17, Alluring Voice 18; as Azumarill: BubbleBeam 20, Aqua Ring 23 | Azumarill (from 18) |
| Shroomish | wild | 14 | Oxide | Absorb, Tackle, Stun Spore, Leech Seed | Mega Drain 17, Headbutt 21; as Breloom: Mach Punch 23, Counter 25 | Breloom (from 23) |
| Shroomish | wild | 14 | Rewrite | Magical Leaf, Stun Spore, Mach Punch, Leech Seed | Mega Drain 17, Headbutt 21; as Breloom: Mach Punch 23, PoisonPowder 24, Counter 25, Bulldoze 26 | Breloom (from 23) |
| Buizel | wild | 15 | Oxide | Quick Attack, Water Gun, Pursuit, Swift | Aqua Jet 21; as Floatzel: Crunch 26 | Floatzel (from 26) |
| Buizel | wild | 15 | Rewrite | BubbleBeam, Pursuit, Scary Face, Swift | Aqua Jet 21; as Floatzel: Crunch 26 | Floatzel (from 26) |
| Froakie | wild | 15 | Oxide | Growl, Quick Attack, Lick, Water Pulse | Icy Wind 16; as Frogadier: Icy Wind 16, Faint Attack 20, Acrobatics 22, Low Kick 25 | Frogadier (from 16); Greninja in Maylene |
| Froakie | wild | 15 | Rewrite | Water Gun, Quick Attack, Lick, Water Pulse | Icy Wind 16; as Frogadier: Icy Wind 16, Thief 19, Faint Attack 20, Acrobatics 22, Low Kick 25 | Frogadier (from 16); Greninja in Maylene |
| Shellos | wild | 15 | Oxide | Mud Sport, Harden, Water Pulse, Mud Bomb | Hidden Power 16 | Shellos; Gastrodon in Fantina |
| Shellos | wild | 15 | Rewrite | Mud-Slap, Harden, Water Pulse, Mud Bomb | Hidden Power 16, Swagger 22 | Shellos; Gastrodon in Fantina |

## Route 211

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 26 | At the cap |
|---|---|---|---|---|---|---|
| Alolan Ninetales | wild | 13 to 16 | Oxide | Tail Whip, Disable, Ice Shard, Safeguard | nothing | Alolan Ninetales |
| Alolan Ninetales | wild | 13 to 16 | Rewrite | Tail Whip, Disable, Ice Shard, Safeguard | Draining Kiss 17, Incinerate 18, Spite 26 | Alolan Ninetales |
| Bronzor | wild | 14 | Oxide | Confusion, Hypnosis, Imprison, Confuse Ray | Extrasensory 19, Iron Defense 26 | Bronzor; Bronzong in Fantina |
| Bronzor | wild | 14 | Rewrite | Confusion, Hypnosis, Imprison, Confuse Ray | Smart Strike 17, Extrasensory 19, Bulldoze 22, Iron Defense 26 | Bronzor; Bronzong in Fantina |
| Hoothoot | wild | 14 | Oxide | Foresight, Hypnosis, Peck, Uproar | Reflect 17; as Noctowl: Confusion 22 | Noctowl (from 20) |
| Hoothoot | wild | 14 | Rewrite | Foresight, Hypnosis, Peck, Uproar | Reflect 17, Confusion 18, Roost 19, Swift 20; as Noctowl: Take Down 25 | Noctowl (from 20) |
| Mienfoo | wild | 14 | Oxide | Pound, Rock Smash, Fake Out | DoubleSlap 17, Force Palm 20, Bounce 22, Drain Punch 25 | Mienfoo; Mienshao in Maylene |
| Mienfoo | wild | 14 | Rewrite | Pound, Rock Smash, Fake Out | DoubleSlap 17, Acrobatics 18, Agility 19, Force Palm 20, Bounce 22, Drain Punch 25 | Mienfoo; Mienshao in Maylene |
| Ponyta | wild | 14 | Oxide | Growl, Tackle, Tail Whip, Ember | Flame Wheel 15, Stomp 19, Fire Spin 24 | Ponyta; Rapidash in Wake |
| Ponyta | wild | 14 | Oxide | Growl, Tackle, Tail Whip, Ember | as Galarian Rapidash: Fairy Wind 15, Agility 20, Psybeam 25 | Galarian Rapidash (from 14) |
| Ponyta | wild | 14 | Rewrite | Tackle, Mystical Fire, Ember, Flame Charge | Flame Wheel 15, Charm 17, Stomp 19, Bulldoze 21, Fire Spin 24 | Ponyta; Rapidash in Wake |
| Ponyta | wild | 14 | Rewrite | Tackle, Mystical Fire, Ember, Flame Charge | as Galarian Rapidash: Fairy Wind 15, Draining Kiss 17, Agility 20, Psybeam 25 | Galarian Rapidash (from 14) |
| Rookidee | wild | 14 | Oxide | Peck, Leer, Fury Attack, Sand-Attack | Pluck 15; as Corvisquire: Steel Wing 20, Drill Peck 26 | Corvisquire (from 16); Corviknight in Wake |
| Rookidee | wild | 14 | Rewrite | Peck, Leer, Taunt, Sand-Attack | Pluck 15; as Corvisquire: Steel Wing 20, Drill Peck 26 | Corvisquire (from 16); Corviknight in Wake |
| Vulpix | wild | 14 to 15 | Oxide | Tail Whip, Roar, Quick Attack, Will-O-Wisp | Confuse Ray 17, Imprison 21, Flamethrower 24 | Vulpix; Ninetales in Maylene |
| Vulpix | wild | 14 to 15 | Rewrite | Tail Whip, Powder Snow, Quick Attack, Will-O-Wisp | Incinerate 16, Confuse Ray 17, Imprison 21, Flamethrower 24 | Vulpix; Ninetales in Maylene |
| Charmander | wild | 15 | Oxide | Scratch, Growl, Ember, SmokeScreen | Dragon Rage 16; as Charmeleon: Dragon Rage 17, Scary Face 21 | Charmeleon (from 16); Charizard in Maylene |
| Charmander | wild | 15 | Rewrite | Scratch, Ember, Scary Face, Metal Claw | Flame Wheel 16; as Charmeleon: Acrobatics 17, Scary Face 21, Bite 24 | Charmeleon (from 16); Charizard in Maylene |
| Chingling | wild | 15 | Oxide | Wrap, Growl, Astonish, Confusion | Uproar 17; as Chimecho: Take Down 22, Yawn 25 | Chimecho (from 20) |
| Chingling | wild | 15 | Rewrite | Growl, Astonish, Confusion | Uproar 17, Snarl 18; as Chimecho: Last Resort 20, Take Down 22, Yawn 25 | Chimecho (from 20) |
| Snover | wild | 15 | Oxide | Leer, Razor Leaf, Icy Wind, GrassWhistle | Swagger 17, Mist 21, Ice Shard 26 | Snover; Abomasnow in Wake |
| Snover | wild | 15 | Rewrite | Powder Snow, Razor Leaf, Icy Wind, GrassWhistle | Swagger 17, Bulldoze 19, Mist 21, Ice Shard 26 | Snover; Abomasnow in Wake |
| Meditite | wild | 16 | Oxide | Meditate, Confusion, Detect, Hidden Power | Mind Reader 18, Feint 22, Calm Mind 25 | Meditite; Medicham in Maylene |
| Meditite | wild | 16 | Rewrite | Confusion, Hidden Power | Force Palm 17, Mind Reader 18, Swagger 22, Rock Throw 26 | Meditite; Medicham in Maylene |
| Zubat | wild | 16 | Oxide | Leech Life, Supersonic, Astonish, Bite | Wing Attack 17, Confuse Ray 21 | Golbat (from 22); Crobat in Wake |
| Zubat | wild | 16 | Rewrite | Astonish, Screech, Bite, Venoshock | Confuse Ray 21; as Golbat: Air Cutter 25 | Golbat (from 22); Crobat in Wake |

## Valley Windworks

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 26 | At the cap |
|---|---|---|---|---|---|---|
| Buizel | old rod | 8 | Oxide | Growl, Water Sport, Quick Attack, Water Gun | Pursuit 10, Swift 15, Aqua Jet 21; as Floatzel: Crunch 26 | Floatzel (from 26) |
| Buizel | old rod | 8 | Rewrite | Water Sport, Quick Attack, Water Gun, BubbleBeam | Pursuit 10, Scary Face 12, Swift 15, Aqua Jet 21; as Floatzel: Crunch 26 | Floatzel (from 26) |
| Carvanha | old rod | 8 | Oxide | Leer, Bite, Rage, Focus Energy | Scary Face 11, Ice Fang 16, Screech 18, Swagger 21, Assurance 26 | Carvanha; Sharpedo in Fantina |
| Carvanha | old rod | 8 | Rewrite | Leer, Bite, Focus Energy | Scary Face 11, Ice Fang 16, Screech 18, Swagger 21, Aqua Cutter 23, Assurance 26 | Carvanha; Sharpedo in Fantina |
| Chinchou | old rod | 8 | Oxide | Bubble, Supersonic, Thunder Wave | Flail 9, Water Gun 12, Confuse Ray 17, Spark 20, Take Down 23 | Chinchou; Lanturn in Fantina |
| Chinchou | old rod | 8 | Rewrite | Bubble, Supersonic, Shock Wave, Thunder Wave | Flail 9, Water Gun 12, Screech 14, Confuse Ray 17, Spark 20, Take Down 23, Icy Wind 26 | Chinchou; Lanturn in Fantina |
| Mantyke | old rod | 8 | Oxide | Tackle, Bubble, Supersonic | BubbleBeam 10, Headbutt 13, Agility 19, Wing Attack 22 | Mantyke; Mantine in Fantina |
| Mantyke | old rod | 8 | Rewrite | Tackle, Bubble | BubbleBeam 10, Headbutt 13, Agility 19, Wing Attack 22, Icy Wind 25 | Mantyke; Mantine in Fantina |
| Mudkip | old rod | 8 | Oxide | Tackle, Growl, Mud-Slap | Water Gun 10, Bide 15; as Marshtomp: Mud Shot 16, Foresight 20, Mud Bomb 25 | Marshtomp (from 16); Swampert in Maylene |
| Mudkip | old rod | 8 | Rewrite | Tackle, Mud-Slap | Water Gun 10, Screech 13, Water Pulse 16; as Marshtomp: Mud Shot 16, Rock Throw 18, Foresight 20, Mud Bomb 25 | Marshtomp (from 16); Swampert in Maylene |
| Pawmi | wild | 9 to 12 | Oxide | Scratch, Growl, ThunderShock, Quick Attack | Nuzzle 12; as Pawmo: Bite 19, Spark 23, Arm Thrust 25 | Pawmo (from 18); Pawmot in Maylene |
| Pawmi | wild | 9 to 12 | Rewrite | Scratch, ThunderShock, Quick Attack, Electroweb | Nuzzle 12, Mach Punch 15; as Pawmo: Bite 19, Spark 23, Arm Thrust 25 | Pawmo (from 18); Pawmot in Maylene |
| Minccino | wild | 10 | Oxide | Pound, Baby-Doll Eyes, Helping Hand | DoubleSlap 13, Sing 16, Echoed Voice 19, Swift 19, Encore 19, Charm 21, Tickle 23 | Minccino; Cinccino in Wake |
| Minccino | wild | 10 | Rewrite | Baby-Doll Eyes, Helping Hand, Chilling Water, Swift | DoubleSlap 13, Sing 16, Encore 19, Charm 21, Tickle 23 | Minccino; Cinccino in Wake |
| Pachirisu | wild | 10 to 11 | Oxide | Growl, Bide, Quick Attack, Charm | Spark 13, Endure 17, Swift 21, Sweet Kiss 25 | Pachirisu |
| Pachirisu | wild | 10 to 11 | Rewrite | Growl, Quick Attack, Electroweb, Charm | Spark 13, Endure 17, Bite 19, Swift 21, Sweet Kiss 25 | Pachirisu |
| Pikipek | wild | 10 | Oxide | Peck, Growl, Echoed Voice, Rock Smash | Supersonic 13; as Trumbeak: Pluck 16, Roost 21, Fury Attack 24 | Trumbeak (from 14); Toucannon in Fantina |
| Pikipek | wild | 10 | Rewrite | Peck, Pluck, Echoed Voice, Rock Smash | Scary Face 11, Supersonic 13; as Trumbeak: Roost 21, Flame Charge 26 | Trumbeak (from 14); Toucannon in Fantina |
| Rookidee | wild | 10 | Oxide | Peck, Leer, Fury Attack | Sand-Attack 12, Pluck 15; as Corvisquire: Steel Wing 20, Drill Peck 26 | Corvisquire (from 16); Corviknight in Wake |
| Rookidee | wild | 10 | Rewrite | Peck, Leer, Taunt | Sand-Attack 12, Pluck 15; as Corvisquire: Steel Wing 20, Drill Peck 26 | Corvisquire (from 16); Corviknight in Wake |
| Shinx | wild | 10 to 11 | Oxide | Tackle, Leer, Charge | Spark 13; as Luxio: Bite 18, Roar 23 | Luxio (from 15); Luxray in Fantina |
| Shinx | wild | 10 to 11 | Rewrite | Tackle, Scary Face, Pursuit, Charge | Spark 13; as Luxio: Bite 18, Volt Switch 24 | Luxio (from 15); Luxray in Fantina |
| Minun | wild | 11 | Oxide | Growl, Thunder Wave, Quick Attack, Helping Hand | Spark 15, Encore 17, Charm 21, Copycat 24 | Minun |
| Minun | wild | 11 | Rewrite | Growl, Thunder Wave, Quick Attack, Helping Hand | Spark 15, Encore 17, Charm 21, Icy Wind 25 | Minun |
| Plusle | wild | 11 | Oxide | Growl, Thunder Wave, Quick Attack, Helping Hand | Spark 15, Encore 17, Fake Tears 21, Copycat 24 | Plusle |
| Plusle | wild | 11 | Rewrite | Growl, Thunder Wave, Quick Attack, Helping Hand | Spark 15, Encore 17, Fake Tears 21, Trailblaze 25 | Plusle |
| Emolga | wild | 12 | Oxide | Tail Whip, ThunderShock, Quick Attack, Double Team | ThunderShock 15, Charge 15, Nuzzle 15, Pursuit 16, Spark 22, Shock Wave 22, Electro Ball 26 | Emolga |
| Emolga | wild | 12 | Rewrite | Nuzzle, Tail Whip, ThunderShock, Quick Attack | Nuzzle 13, Charge 14, ThunderShock 15, Pursuit 16, Snarl 17, Taunt 19, Shock Wave 21, Spark 22, Air Cutter 24 | Emolga |
| Pikachu | wild | 12 | Oxide | ThunderShock, Growl, Tail Whip, Thunder Wave | Quick Attack 13, Double Team 18, Slam 21, Thunderbolt 26 | Pikachu; Raichu in Maylene |
| Pikachu | wild | 12 | Rewrite | ThunderShock, Tail Whip, Thunder Wave, Sweet Kiss | Quick Attack 13, Trailblaze 17, Slam 21, Thunderbolt 26 | Pikachu; Raichu in Maylene |

## Honey trees

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 26 | At the cap |
|---|---|---|---|---|---|---|
| Aipom | honey | 10 | Oxide | Scratch, Tail Whip, Sand-Attack, Astonish | Baton Pass 11, Tickle 15, Fury Swipes 18, Swift 22, Screech 25 | Aipom; Ambipom in Fantina |
| Aipom | honey | 10 | Rewrite | Scratch, Tail Whip, Sand-Attack, Astonish | Baton Pass 11, Tickle 15, Fury Swipes 18, Bite 20, Swift 22, Screech 25 | Aipom; Ambipom in Fantina |
| Bounsweet | honey | 10 | Oxide | Splash, Play Nice, Rapid Spin | Razor Leaf 12; as Steenee: Razor Leaf 12, Sweet Scent 17, Magical Leaf 21, Teeter Dance 23, Stomp 25 | Steenee (from 12); Tsareena in Fantina |
| Bounsweet | honey | 10 | Rewrite | Magical Leaf, Taunt, Play Nice, Rapid Spin | Razor Leaf 12; as Steenee: Razor Leaf 12, Draining Kiss 17, Magical Leaf 21, Teeter Dance 23, Stomp 25 | Steenee (from 12); Tsareena in Fantina |
| Burmy | honey | 10 | Oxide | Protect, Tackle | Bug Bite 15, Hidden Power 20; as Wormadam: Hidden Power 20, Confusion 23, Razor Leaf 26 | Wormadam (from 20) |
| Burmy | honey | 10 | Oxide | Protect, Tackle | Bug Bite 15, Hidden Power 20; as Mothim: Hidden Power 20, Confusion 23, Gust 26 | Mothim (from 20) |
| Burmy | honey | 10 | Rewrite | Tackle | Bug Bite 15, Confusion 17, Roost 18, Hidden Power 20; as Wormadam: Hidden Power 20, Razor Leaf 26 | Wormadam (from 20) |
| Burmy | honey | 10 | Rewrite | Tackle | Bug Bite 15, Confusion 17, Roost 18, Hidden Power 20; as Mothim: Hidden Power 20, Gust 26 | Mothim (from 20) |
| Cherubi | honey | 10 | Oxide | Tackle, Growth, Leech Seed | Helping Hand 13, Magical Leaf 19; as Cherrim: Petal Dance 25 | Cherrim (from 25) |
| Cherubi | honey | 10 | Rewrite | Tackle, Leech Seed | Helping Hand 13, Magical Leaf 19, Stun Spore 22, Draining Kiss 25 | Cherrim (from 25) |
| Combee | honey | 10 | Oxide | Sweet Scent, Gust | Bug Bite 13; as Vespiquen: Power Gem 21, Heal Order 25 | Vespiquen (from 21) |
| Combee | honey | 10 | Rewrite | Gust | Bug Bite 13, Pursuit 17, Roost 21; as Vespiquen: Power Gem 21, Poison Sting 22, Confuse Ray 23, Defend Order 24, Heal Order 25 | Vespiquen (from 21) |
| Dottler | honey | 10 | Oxide | Reflect, Light Screen, Confusion, Struggle Bug | Psybeam 20 | Dottler; Orbeetle in Fantina |
| Dottler | honey | 10 | Rewrite | Reflect, Light Screen, Confusion, Struggle Bug | Confusion 11, Light Screen 12, Psybeam 20, Snarl 26 | Dottler; Orbeetle in Fantina |
| Grubbin | honey | 10 | Oxide | ViceGrip, Mud-Slap, String Shot, Bug Bite | Bite 15; as Charjabug: Spark 23 | Charjabug (from 20); Vikavolt in Maylene |
| Grubbin | honey | 10 | Rewrite | ViceGrip, Mud-Slap, String Shot, Bug Bite | Bite 15; as Charjabug: Spark 23, Sticky Web 25 | Charjabug (from 20); Vikavolt in Maylene |
| Heracross | honey | 10 | Oxide | Leer, Horn Attack, Endure, Fury Attack | Aerial Ace 13, Brick Break 19, Counter 25 | Heracross |
| Heracross | honey | 10 | Rewrite | Night Slash, Tackle, Horn Attack, Endure | Aerial Ace 13, Brick Break 19, Pounce 22, Counter 25 | Heracross |
| Munchlax | honey | 10 | Oxide | Odor Sleuth, Tackle, Defense Curl, Amnesia | Lick 12, Recycle 17, Screech 20, Stockpile 25 | Munchlax; Snorlax in Maylene |
| Munchlax | honey | 10 | Rewrite | Odor Sleuth, Tackle, Amnesia | Lick 12, Recycle 17, Belly Drum 18, Screech 20, Headbutt 22, Rest 24, Stockpile 25 | Munchlax; Snorlax in Maylene |
| Seedot | honey | 10 | Oxide | Bide, Harden, Growth | Nature Power 13 | Shiftry (from 14) |
| Seedot | honey | 10 | Rewrite | Harden, Razor Leaf, Fake Out, Scary Face | Trailblaze 11, Giga Drain 14; as Nuzleaf: Payback 14 | Shiftry (from 14) |
| Sewaddle | honey | 10 | Oxide | Tackle, String Shot, Bug Bite | Razor Leaf 12 | Swadloon (from 20); Leavanny in Fantina |
| Sewaddle | honey | 10 | Rewrite | Tackle, Sticky Web, Bug Bite | Razor Leaf 12, Pounce 16; as Swadloon: Struggle Bug 22, Bite 26 | Swadloon (from 20); Leavanny in Fantina |
| Shroomish | honey | 10 | Oxide | Absorb, Tackle, Stun Spore | Leech Seed 13, Mega Drain 17, Headbutt 21; as Breloom: Mach Punch 23, Counter 25 | Breloom (from 23) |
| Shroomish | honey | 10 | Rewrite | Tackle, Magical Leaf, Stun Spore | Mach Punch 11, Leech Seed 13, Mega Drain 17, Headbutt 21; as Breloom: Mach Punch 23, PoisonPowder 24, Counter 25, Bulldoze 26 | Breloom (from 23) |

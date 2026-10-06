# Gardenia's split: what each catch knows and learns

Written by `tools/oxide/balance/learncheck.py sheets` for check 6 of the learnset baseline (`docs/oxide/learnset-checks.md`). One table per capture area first offered in Gardenia's split, whose cap is 26. Each Pokemon is read at the lowest level it is found at there. "Knows at capture" is the last four moves its list gives by that level; "learns by level-up" is every entry it reaches after capture up to 26, evolving on time, with each later stage's moves under its name; "at the cap" is the stage it can be by then and the next one after. A row marked v3 shows learnset v3 (unlanded, `origin/balance-learngen-v2`) where it differs from Oxide's lists; a row marked both is the same in each. Relearner-only moves and egg moves are left out. Nothing here is in the game data.

## Eterna City

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 26 | At the cap |
|---|---|---|---|---|---|---|
| Popplio | in-game trade | 1 | both | Pound, Water Gun | Disarming Voice 4, Baby-Doll Eyes 7, Life Dew 10, Aqua Jet 14; as Brionne: Icy Wind 19, Encore 24 | Brionne (from 16); Primarina in Maylene |
| Togepi | egg gift | 1 | both | Growl, Charm | Metronome 6, Sweet Kiss 10; as Togetic: Sweet Kiss 10, Yawn 15, Encore 19, Follow Me 24 | Togetic (from 10); Togekiss in Wake |
| Barboach | old rod | 10 | both | Mud-Slap, Mud Sport, Water Sport, Water Gun | Mud Bomb 14, Amnesia 18, Water Pulse 22, Magnitude 26 | Barboach; Whiscash in Fantina |
| Froakie | old rod | 10 | both | Pound, Water Gun, Growl, Quick Attack | Lick 13, Water Pulse 14, Icy Wind 16; as Frogadier: Icy Wind 16, Faint Attack 20, Acrobatics 22, Low Kick 25 | Frogadier (from 16); Greninja in Maylene |
| Goldeen | old rod | 10 | both | Peck, Tail Whip, Water Sport, Supersonic | Horn Attack 11, Water Pulse 17, Flail 21 | Goldeen; Seaking in Fantina |
| Lotad | old rod | 10 | Oxide | Astonish, Growl, Absorb, Nature Power | Mist 11; as Lombre: Fury Swipes 15, Water Sport 19, BubbleBeam 25 | Lombre (from 14); Ludicolo in Maylene |
| Lotad | old rod | 10 | v3 | Growl, Water Gun, Nature Power | Mist 11; as Lombre: Fury Swipes 15, Water Sport 19, BubbleBeam 25 | Lombre (from 14); Ludicolo in Maylene |
| Shellos | old rod | 10 | both | Mud-Slap, Mud Sport, Harden, Water Pulse | Mud Bomb 11, Hidden Power 16 | Shellos; Gastrodon in Fantina |

## Eterna Forest

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 26 | At the cap |
|---|---|---|---|---|---|---|
| Buneary | wild | 10 | both | Pound, Defense Curl, Foresight, Endure | Frustration 13, Quick Attack 16; as Lopunny: Jump Kick 23, Baton Pass 26 | Lopunny (from 20) |
| Budew | wild | 11 | Oxide | Absorb, Growth, Water Sport, Stun Spore | Mega Drain 13, Worry Seed 16 | Budew; Roselia in Fantina |
| Budew | wild | 11 | v3 | Growth, Water Sport, Stun Spore | Mega Drain 13, Worry Seed 16 | Budew; Roselia in Fantina |
| Murkrow | wild | 11 | Oxide | Peck, Astonish, Pursuit, Haze | Wing Attack 15, Night Shade 21, Assurance 25 | Murkrow; Honchkrow in Fantina |
| Murkrow | wild | 11 | v3 | Peck, Pursuit, Haze | Wing Attack 15, Night Shade 21 | Murkrow; Honchkrow in Fantina |
| Rowlet | wild | 11 | Oxide | Tackle, Leafage, Growl, Peck | Astonish 12, Razor Leaf 15; as Dartrix: Pluck 19, Ominous Wind 24 | Dartrix (from 16); Decidueye in Maylene |
| Rowlet | wild | 11 | v3 | Tackle, Leafage, Growl, Peck | Razor Leaf 15; as Dartrix: Pluck 19, Ominous Wind 24 | Dartrix (from 16); Decidueye in Maylene |
| Seedot | wild | 11 | Oxide | Bide, Harden, Growth | Nature Power 13 | Shiftry (from 14) |
| Seedot | wild | 11 | v3 | Harden, Growth | Nature Power 13 | Shiftry (from 14) |
| Sewaddle | wild | 11 to 12 | Oxide | Tackle, String Shot, Bug Bite | Razor Leaf 12 | Swadloon (from 20); Leavanny in Fantina |
| Sewaddle | wild | 11 to 12 | v3 | Tackle, String Shot, Bug Bite | Razor Leaf 12; as Swadloon: Protect on evolving | Swadloon (from 20); Leavanny in Fantina |
| Shroomish | wild | 11 to 13 | Oxide | Absorb, Tackle, Stun Spore | Leech Seed 13, Mega Drain 17, Headbutt 21; as Breloom: Mach Punch 23, Counter 25 | Breloom (from 23) |
| Shroomish | wild | 11 to 13 | v3 | Tackle, Stun Spore | Leech Seed 13, Mega Drain 17, Headbutt 21; as Breloom: Mach Punch 23, Counter 25 | Breloom (from 23) |
| Beautifly | wild | 12 | Oxide | Absorb | Gust 13, Stun Spore 17, Morning Sun 20, Mega Drain 24, Air Slash 26 | Beautifly |
| Beautifly | wild | 12 | v3 | nothing | Gust 13, Stun Spore 17, Morning Sun 20 | Beautifly |
| Burmy | wild | 12 | both | Protect, Tackle | Bug Bite 15, Hidden Power 20; as Wormadam: Hidden Power 20, Confusion 23, Razor Leaf 26 | Wormadam (from 20) |
| Burmy | wild | 12 | both | Protect, Tackle | Bug Bite 15, Hidden Power 20; as Mothim: Hidden Power 20, Confusion 23, Gust 26 | Mothim (from 20) |
| Combee | wild | 13 | both | Sweet Scent, Gust, Bug Bite | as Vespiquen: Power Gem 21, Heal Order 25 | Vespiquen (from 21) |
| Steenee | wild | 13 | both | DoubleSlap, Play Nice, Rapid Spin, Razor Leaf | Sweet Scent 17, Magical Leaf 21, Teeter Dance 23, Stomp 25 | Steenee; Tsareena in Fantina |

## Floaroma Town

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 26 | At the cap |
|---|---|---|---|---|---|---|
| Combee | wild | 10 | both | Sweet Scent, Gust | Bug Bite 13; as Vespiquen: Power Gem 21, Heal Order 25 | Vespiquen (from 21) |
| Bounsweet | wild | 11 | Oxide | Splash, Play Nice, Rapid Spin | Razor Leaf 12; as Steenee: Razor Leaf 12, Sweet Scent 17, Magical Leaf 21, Teeter Dance 23, Stomp 25 | Steenee (from 12); Tsareena in Fantina |
| Bounsweet | wild | 11 | v3 | Leafage, Play Nice, Rapid Spin | Razor Leaf 12; as Steenee: Razor Leaf 12, Sweet Scent 17, Magical Leaf 21, Teeter Dance 23, Stomp 25 | Steenee (from 12); Tsareena in Fantina |
| Budew | wild | 11 | Oxide | Absorb, Growth, Water Sport, Stun Spore | Mega Drain 13, Worry Seed 16 | Budew; Roselia in Fantina |
| Budew | wild | 11 | v3 | Growth, Water Sport, Stun Spore | Mega Drain 13, Worry Seed 16 | Budew; Roselia in Fantina |
| Cherubi | wild | 11 | both | Tackle, Growth, Leech Seed | Helping Hand 13, Magical Leaf 19; as Cherrim: Petal Dance 25 | Cherrim (from 25) |
| Murkrow | wild | 11 | Oxide | Peck, Astonish, Pursuit, Haze | Wing Attack 15, Night Shade 21, Assurance 25 | Murkrow; Honchkrow in Fantina |
| Murkrow | wild | 11 | v3 | Peck, Pursuit, Haze | Wing Attack 15, Night Shade 21 | Murkrow; Honchkrow in Fantina |
| Aipom | wild | 12 | Oxide | Tail Whip, Sand-Attack, Astonish, Baton Pass | Tickle 15, Fury Swipes 18, Swift 22, Screech 25 | Aipom; Ambipom in Fantina |
| Aipom | wild | 12 | v3 | Tail Whip, Sand-Attack, Tackle, Baton Pass | Tickle 15, Fury Swipes 18, Swift 22, Screech 25 | Aipom; Ambipom in Fantina |
| Hoppip | wild | 12 | Oxide | Synthesis, Tail Whip, Tackle, PoisonPowder | Stun Spore 14, Sleep Powder 16; as Skiploom: Bullet Seed 20, Leech Seed 24 | Skiploom (from 18); Jumpluff in Fantina |
| Hoppip | wild | 12 | v3 | Synthesis, Tail Whip, Tackle, PoisonPowder | Stun Spore 14, Sleep Powder 16; as Skiploom: Leech Seed 24 | Skiploom (from 18); Jumpluff in Fantina |
| Poochyena | wild | 12 | both | Tackle, Howl, Sand-Attack | Bite 13, Odor Sleuth 17; as Mightyena: Roar 22 | Mightyena (from 18) |
| Tropius | wild | 12 | both | Leer, Gust, Growth, Razor Leaf | Stomp 17, Sweet Scent 21 | Tropius |
| Chingling | wild | 13 | Oxide | Wrap, Growl, Astonish | Confusion 14, Uproar 17; as Chimecho: Take Down 22, Yawn 25 | Chimecho (from 20) |
| Chingling | wild | 13 | v3 | Growl | Confusion 14, Uproar 17; as Chimecho: Take Down 22, Yawn 25 | Chimecho (from 20) |
| Pachirisu | wild | 13 | Oxide | Bide, Quick Attack, Charm, Spark | Endure 17, Swift 21, Sweet Kiss 25 | Pachirisu |
| Pachirisu | wild | 13 | v3 | Growl, Quick Attack, Charm, Spark | Endure 17, Swift 21, Sweet Kiss 25 | Pachirisu |
| Skitty | wild | 13 | Oxide | Tackle, Foresight, Attract, Sing | nothing | Delcatty (from 13) |
| Skitty | wild | 13 | v3 | Tackle, Foresight, Attract, Sing | as Delcatty: Covet on evolving, Assist 22 | Delcatty (from 13) |

## Mt. Coronet

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 26 | At the cap |
|---|---|---|---|---|---|---|
| Feebas | special tile (rod) | 10 | Oxide | Splash | Tackle 15 | Feebas; Milotic in Fantina |
| Feebas | special tile (rod) | 10 | v3 | Tackle | Water Gun 15 | Feebas; Milotic in Fantina |

## Mt. Coronet North

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 26 | At the cap |
|---|---|---|---|---|---|---|
| Bronzor | wild | 13 | Oxide | Tackle, Confusion, Hypnosis, Imprison | Confuse Ray 14, Extrasensory 19, Iron Defense 26 | Bronzor; Bronzong in Fantina |
| Bronzor | wild | 13 | v3 | Tackle, Confusion, Hypnosis, Imprison | Confuse Ray 14, Extrasensory 19, Iron Head 20, Iron Defense 26 | Bronzor; Bronzong in Fantina |
| Alolan Ninetales | wild | 14 to 15 | Oxide | Tail Whip, Disable, Ice Shard, Safeguard | nothing | Alolan Ninetales |
| Alolan Ninetales | wild | 14 to 15 | v3 | Tail Whip, Disable, Ice Shard, Safeguard | Icy Wind 16, Aurora Beam 24 | Alolan Ninetales |
| Clefairy | wild | 14 | Oxide | Encore, Sing, DoubleSlap, Defense Curl | nothing | Clefable (from 14) |
| Clefairy | wild | 14 | v3 | Encore, Sing, DoubleSlap, Defense Curl | as Clefable: Cosmic Power 25 | Clefable (from 14) |
| Makuhita | wild | 14 to 16 | both | Sand-Attack, Arm Thrust, Vital Throw, Fake Out | Whirlwind 16, Knock Off 19, SmellingSalt 22 | Hariyama (from 24) |
| Phanpy | wild | 14 to 16 | Oxide | Growl, Defense Curl, Flail, Take Down | Rollout 15, Natural Gift 19, Slam 24; as Donphan: Fury Attack 25 | Donphan (from 25) |
| Phanpy | wild | 14 to 16 | v3 | Growl, Defense Curl, Flail, Take Down | Natural Gift 19, Slam 24; as Donphan: Fury Attack 25 | Donphan (from 25) |
| Snorunt | wild | 14 | both | Leer, Double Team, Bite, Icy Wind | Headbutt 19, Protect 22 | Snorunt; Glalie in Wake, Froslass in Byron |
| Zubat | wild | 14 | Oxide | Leech Life, Supersonic, Astonish, Bite | Wing Attack 17, Confuse Ray 21 | Golbat (from 22); Crobat in Wake |
| Zubat | wild | 14 | v3 | Leech Life, Supersonic, Acid, Bite | Wing Attack 17, Confuse Ray 21 | Golbat (from 22); Crobat in Wake |
| Carbink | wild | 15 | both | Rock Throw, Sharpen, Smack Down, Guard Split | Reflect 18, Flail 24, AncientPower 25, Rock Polish 25 | Carbink |
| Nosepass | wild | 15 | both | Tackle, Harden, Rock Throw | Block 19, Thunder Wave 25 | Nosepass; Probopass in Fantina |
| Swinub | wild | 15 | both | Odor Sleuth, Mud Sport, Powder Snow, Mud-Slap | Endure 16, Mud Bomb 20, Icy Wind 25 | Swinub; Piloswine in Fantina |
| Snover | wild | 16 | both | Leer, Razor Leaf, Icy Wind, GrassWhistle | Swagger 17, Mist 21, Ice Shard 26 | Snover; Abomasnow in Wake |

## Oreburgh Gate

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 26 | At the cap |
|---|---|---|---|---|---|---|
| Barboach | old rod | 6 | both | Mud-Slap, Mud Sport, Water Sport | Water Gun 10, Mud Bomb 14, Amnesia 18, Water Pulse 22, Magnitude 26 | Barboach; Whiscash in Fantina |
| Clamperl | old rod | 6 | Oxide | Clamp, Water Gun, Whirlpool, Iron Defense | as Huntail: Bite 6, Screech 10, Water Pulse 15, Scary Face 19, Ice Fang 24 | Huntail (from 6) |
| Clamperl | old rod | 6 | Oxide | Clamp, Water Gun, Whirlpool, Iron Defense | as Gorebyss: Confusion 6, Agility 10, Water Pulse 15, Amnesia 19, Aqua Ring 24 | Gorebyss (from 6) |
| Clamperl | old rod | 6 | v3 | Water Gun, Iron Defense | as Huntail: Bite 6, Screech 10, Water Pulse 15, Scary Face 19 | Huntail (from 6) |
| Clamperl | old rod | 6 | v3 | Water Gun, Iron Defense | as Gorebyss: Confusion 6, Agility 10, Water Pulse 15, Amnesia 19, Aqua Ring 24 | Gorebyss (from 6) |
| Feebas | old rod | 6 | Oxide | Splash | Tackle 15 | Feebas; Milotic in Fantina |
| Feebas | old rod | 6 | v3 | Tackle | Water Gun 15 | Feebas; Milotic in Fantina |
| Geodude | wild | 6 to 9 | Oxide | Tackle, Defense Curl, Mud Sport | Rock Polish 8, Rock Throw 11, Magnitude 15, Selfdestruct 18, Rollout 22, Rock Blast 25 | Graveler (from 25); Golem in Wake |
| Geodude | wild | 6 to 9 | v3 | Tackle, Defense Curl, Mud Sport | Rock Polish 8, Rock Throw 11, Magnitude 15, Selfdestruct 18, Rock Blast 25 | Graveler (from 25); Golem in Wake |
| Shellos | old rod | 6 | both | Mud-Slap, Mud Sport, Harden | Water Pulse 7, Mud Bomb 11, Hidden Power 16 | Shellos; Gastrodon in Fantina |
| Squirtle | old rod | 6 | both | Tackle, Tail Whip | Bubble 7, Withdraw 10, Water Gun 13, Bite 16; as Wartortle: Bite 16, Rapid Spin 20, Protect 24 | Wartortle (from 16); Blastoise in Maylene |
| Dwebble | wild | 7 | Oxide | Struggle Bug, Rock Blast, Block | Sand-Attack 10, Faint Attack 14, Slash 17, Rock Tomb 21, Bug Bite 24 | Dwebble; Crustle in Maylene |
| Dwebble | wild | 7 | v3 | Struggle Bug, Block | Sand-Attack 10, Faint Attack 14, Slash 17, Rock Tomb 21, Bug Bite 24 | Dwebble; Crustle in Maylene |
| Phanpy | wild | 7 | Oxide | Tackle, Growl, Defense Curl, Flail | Take Down 10, Rollout 15, Natural Gift 19, Slam 24; as Donphan: Fury Attack 25 | Donphan (from 25) |
| Phanpy | wild | 7 | v3 | Tackle, Growl, Defense Curl, Flail | Take Down 10, Natural Gift 19, Slam 24; as Donphan: Fury Attack 25 | Donphan (from 25) |
| Rhyhorn | wild | 7 to 8 | both | Horn Attack, Tail Whip | Stomp 9, Fury Attack 13, Scary Face 21, Rock Blast 25 | Rhyhorn; Rhydon in Wake |
| Carbink | wild | 8 | both | Tackle, Harden, Rock Throw, Sharpen | Smack Down 10, Guard Split 15, Reflect 18, Flail 24, AncientPower 25, Rock Polish 25 | Carbink |
| Glimmet | wild | 8 | both | Rock Throw, Harden, Smack Down, Acid Spray | AncientPower 11, Rock Polish 15, Stealth Rock 18, Venoshock 22 | Glimmet; Glimmora in Maylene |
| Mudkip | wild | 8 | Oxide | Tackle, Growl, Mud-Slap | Water Gun 10, Bide 15; as Marshtomp: Mud Shot 16, Foresight 20, Mud Bomb 25 | Marshtomp (from 16); Swampert in Maylene |
| Mudkip | wild | 8 | v3 | Tackle, Growl, Mud-Slap | Water Gun 10; as Marshtomp: Mud Shot 16, Foresight 20, Mud Bomb 25 | Marshtomp (from 16); Swampert in Maylene |
| Nacli | wild | 9 | Oxide | Tackle, Harden, Rock Throw, Mud Shot | Smack Down 10, Rock Polish 13, Headbutt 16, Iron Defense 20 | Naclstack (from 24); Garganacl in Maylene |
| Nacli | wild | 9 | v3 | Tackle, Harden, Rock Throw, Mud Shot | Smack Down 10, Rock Polish 13, Headbutt 16, Iron Defense 20; as Naclstack: Salt Cure on evolving | Naclstack (from 24); Garganacl in Maylene |
| Onix | wild | 9 | Oxide | Harden, Bind, Screech, Rock Throw | as Steelix: Rock Throw 9, Rage 14, Rock Tomb 17, Slam 25 | Steelix (from 9) |
| Onix | wild | 9 | v3 | Tackle, Harden, Screech, Rock Throw | as Steelix: Rock Throw 9, Rock Tomb 17, Slam 25 | Steelix (from 9) |

## Route 204

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 26 | At the cap |
|---|---|---|---|---|---|---|
| Barboach | old rod | 8 | both | Mud-Slap, Mud Sport, Water Sport | Water Gun 10, Mud Bomb 14, Amnesia 18, Water Pulse 22, Magnitude 26 | Barboach; Whiscash in Fantina |
| Corphish | old rod | 8 | both | Bubble, Harden | ViceGrip 10, Leer 13, BubbleBeam 20, Protect 23, Knock Off 26 | Corphish; Crawdaunt in Fantina |
| Froakie | old rod | 8 | both | Pound, Water Gun, Growl | Quick Attack 10, Lick 13, Water Pulse 14, Icy Wind 16; as Frogadier: Icy Wind 16, Faint Attack 20, Acrobatics 22, Low Kick 25 | Frogadier (from 16); Greninja in Maylene |
| Goldeen | old rod | 8 | both | Peck, Tail Whip, Water Sport, Supersonic | Horn Attack 11, Water Pulse 17, Flail 21 | Goldeen; Seaking in Fantina |
| Lotad | old rod | 8 | Oxide | Astonish, Growl, Absorb, Nature Power | Mist 11; as Lombre: Fury Swipes 15, Water Sport 19, BubbleBeam 25 | Lombre (from 14); Ludicolo in Maylene |
| Lotad | old rod | 8 | v3 | Growl, Water Gun, Nature Power | Mist 11; as Lombre: Fury Swipes 15, Water Sport 19, BubbleBeam 25 | Lombre (from 14); Ludicolo in Maylene |
| Sewaddle | wild | 8 to 11 | Oxide | Tackle, String Shot, Bug Bite | Razor Leaf 12 | Swadloon (from 20); Leavanny in Fantina |
| Sewaddle | wild | 8 to 11 | v3 | Tackle, String Shot, Bug Bite | Razor Leaf 12; as Swadloon: Protect on evolving | Swadloon (from 20); Leavanny in Fantina |
| Budew | wild | 9 | Oxide | Absorb, Growth, Water Sport | Stun Spore 10, Mega Drain 13, Worry Seed 16 | Budew; Roselia in Fantina |
| Budew | wild | 9 | v3 | Growth, Water Sport | Stun Spore 10, Mega Drain 13, Worry Seed 16 | Budew; Roselia in Fantina |
| Litten | wild | 9 | Oxide | Scratch, Ember, Growl | Lick 10, Fire Fang 14, Double Kick 16; as Torracat: Double Kick 16, Bite 21, Scary Face 25 | Torracat (from 16); Incineroar in Maylene |
| Litten | wild | 9 | v3 | Scratch, Ember, Growl | Lick 10, Double Kick 16; as Torracat: Double Kick 16, Bite 21, Scary Face 25 | Torracat (from 16); Incineroar in Maylene |
| Poochyena | wild | 9 | both | Tackle, Howl, Sand-Attack | Bite 13, Odor Sleuth 17; as Mightyena: Roar 22 | Mightyena (from 18) |
| Purrloin | wild | 9 | both | Scratch, Growl, Sand-Attack, Assist | Fake Out 12, Fury Swipes 12, Pursuit 15, Torment 17; as Liepard: Fake Out 22, Assurance 26 | Liepard (from 20) |
| Torchic | wild | 9 | Oxide | Scratch, Growl, Focus Energy | Ember 10, Peck 16; as Combusken: Double Kick 16, Peck 17, Sand-Attack 21 | Combusken (from 16); Blaziken in Maylene |
| Torchic | wild | 9 | v3 | Scratch, Growl, Focus Energy | Ember 10, Peck 16; as Combusken: Double Kick 16, Sand-Attack 21 | Combusken (from 16); Blaziken in Maylene |
| Treecko | wild | 9 | Oxide | Pound, Leer, Absorb | Quick Attack 11, Pursuit 16; as Grovyle: Fury Cutter 16, Pursuit 17, Screech 23 | Grovyle (from 16); Sceptile in Maylene |
| Treecko | wild | 9 | v3 | Pound, Leer, Leafage | Quick Attack 11, Pursuit 16; as Grovyle: Pursuit 17, Screech 23 | Grovyle (from 16); Sceptile in Maylene |
| Bounsweet | wild | 10 to 11 | Oxide | Splash, Play Nice, Rapid Spin | Razor Leaf 12; as Steenee: Razor Leaf 12, Sweet Scent 17, Magical Leaf 21, Teeter Dance 23, Stomp 25 | Steenee (from 12); Tsareena in Fantina |
| Bounsweet | wild | 10 to 11 | v3 | Leafage, Play Nice, Rapid Spin | Razor Leaf 12; as Steenee: Razor Leaf 12, Sweet Scent 17, Magical Leaf 21, Teeter Dance 23, Stomp 25 | Steenee (from 12); Tsareena in Fantina |
| Snivy | wild | 10 | Oxide | Tackle, Vine Whip, Leer, Wrap | Hold Back 14; as Servine: Magical Leaf 19, Mega Drain 24 | Servine (from 16); Serperior in Maylene |
| Snivy | wild | 10 | v3 | Tackle, Vine Whip, Leer, Leafage | Hold Back 14; as Servine: Magical Leaf 19, Mega Drain 24 | Servine (from 16); Serperior in Maylene |
| Snubbull | wild | 10 to 11 | both | Scary Face, Tail Whip, Charm, Bite | Lick 13, Headbutt 19 | Granbull (from 23) |

## Route 205

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 26 | At the cap |
|---|---|---|---|---|---|---|
| Buizel | old rod | 8 to 10 | both | Growl, Water Sport, Quick Attack, Water Gun | Pursuit 10, Swift 15, Aqua Jet 21; as Floatzel: Crunch 26 | Floatzel (from 26) |
| Carvanha | old rod | 8 to 10 | Oxide | Leer, Bite, Rage, Focus Energy | Scary Face 11, Ice Fang 16, Screech 18, Swagger 21, Assurance 26 | Carvanha; Sharpedo in Fantina |
| Carvanha | old rod | 8 to 10 | v3 | Leer, Bite, Water Gun, Focus Energy | Scary Face 11, Screech 18, Swagger 21, Assurance 26 | Carvanha; Sharpedo in Fantina |
| Chinchou | old rod | 8 to 10 | both | Bubble, Supersonic, Thunder Wave | Flail 9, Water Gun 12, Confuse Ray 17, Spark 20, Take Down 23 | Chinchou; Lanturn in Fantina |
| Psyduck | old rod | 8 | both | Water Sport, Scratch, Tail Whip | Water Gun 9, Disable 14, Confusion 18, Water Pulse 22 | Psyduck; Golduck in Fantina |
| Squirtle | old rod | 8 | both | Tackle, Tail Whip, Bubble | Withdraw 10, Water Gun 13, Bite 16; as Wartortle: Bite 16, Rapid Spin 20, Protect 24 | Wartortle (from 16); Blastoise in Maylene |
| Pachirisu | wild | 9 | Oxide | Growl, Bide, Quick Attack, Charm | Spark 13, Endure 17, Swift 21, Sweet Kiss 25 | Pachirisu |
| Pachirisu | wild | 9 | v3 | Growl, Quick Attack, Charm | Spark 13, Endure 17, Swift 21, Sweet Kiss 25 | Pachirisu |
| Aipom | wild | 10 | Oxide | Scratch, Tail Whip, Sand-Attack, Astonish | Baton Pass 11, Tickle 15, Fury Swipes 18, Swift 22, Screech 25 | Aipom; Ambipom in Fantina |
| Aipom | wild | 10 | v3 | Scratch, Tail Whip, Sand-Attack, Tackle | Baton Pass 11, Tickle 15, Fury Swipes 18, Swift 22, Screech 25 | Aipom; Ambipom in Fantina |
| Barboach | old rod | 10 | both | Mud-Slap, Mud Sport, Water Sport, Water Gun | Mud Bomb 14, Amnesia 18, Water Pulse 22, Magnitude 26 | Barboach; Whiscash in Fantina |
| Buneary | wild | 10 | both | Pound, Defense Curl, Foresight, Endure | Frustration 13, Quick Attack 16; as Lopunny: Jump Kick 23, Baton Pass 26 | Lopunny (from 20) |
| Minccino | wild | 10 | both | Pound, Baby-Doll Eyes, Helping Hand | DoubleSlap 13, Sing 16, Echoed Voice 19, Swift 19, Encore 19, Charm 21, Tickle 23 | Minccino; Cinccino in Wake |
| Mudkip | old rod | 10 | Oxide | Tackle, Growl, Mud-Slap, Water Gun | Bide 15; as Marshtomp: Mud Shot 16, Foresight 20, Mud Bomb 25 | Marshtomp (from 16); Swampert in Maylene |
| Mudkip | old rod | 10 | v3 | Tackle, Growl, Mud-Slap, Water Gun | as Marshtomp: Mud Shot 16, Foresight 20, Mud Bomb 25 | Marshtomp (from 16); Swampert in Maylene |
| Poochyena | wild | 10 | both | Tackle, Howl, Sand-Attack | Bite 13, Odor Sleuth 17; as Mightyena: Roar 22 | Mightyena (from 18) |
| Skitty | wild | 10 | Oxide | Tail Whip, Tackle, Foresight, Attract | nothing | Delcatty (from 10) |
| Skitty | wild | 10 | v3 | Tail Whip, Tackle, Foresight, Attract | as Delcatty: Covet on evolving, Assist 22 | Delcatty (from 10) |
| Smoliv | wild | 10 | Oxide | Sweet Scent, Absorb, Growth, Razor Leaf | Helping Hand 13, Flail 16, Mega Drain 20, Grassy Terrain 23 | Dolliv (from 25); Arboliva in Maylene |
| Smoliv | wild | 10 | v3 | Sweet Scent, Leafage, Growth, Razor Leaf | Helping Hand 13, Flail 16, Mega Drain 20 | Dolliv (from 25); Arboliva in Maylene |
| Bounsweet | wild | 11 | Oxide | Splash, Play Nice, Rapid Spin | Razor Leaf 12; as Steenee: Razor Leaf 12, Sweet Scent 17, Magical Leaf 21, Teeter Dance 23, Stomp 25 | Steenee (from 12); Tsareena in Fantina |
| Bounsweet | wild | 11 | v3 | Leafage, Play Nice, Rapid Spin | Razor Leaf 12; as Steenee: Razor Leaf 12, Sweet Scent 17, Magical Leaf 21, Teeter Dance 23, Stomp 25 | Steenee (from 12); Tsareena in Fantina |
| Fletchling | wild | 11 | both | Tackle, Growl, Quick Attack | Aerial Ace 12; as Fletchinder: Flame Charge 17, Roost 22 | Fletchinder (from 16); Talonflame in Maylene |
| Mareep | wild | 11 | both | Tackle, Growl, ThunderShock | Thunder Wave 14; as Flaaffy: Cotton Spore 20, Charge 25 | Flaaffy (from 15); Ampharos in Fantina |
| Sewaddle | wild | 11 to 13 | Oxide | Tackle, String Shot, Bug Bite | Razor Leaf 12 | Swadloon (from 20); Leavanny in Fantina |
| Sewaddle | wild | 11 to 13 | v3 | Tackle, String Shot, Bug Bite | Razor Leaf 12; as Swadloon: Protect on evolving | Swadloon (from 20); Leavanny in Fantina |
| Combee | wild | 12 | both | Sweet Scent, Gust | Bug Bite 13; as Vespiquen: Power Gem 21, Heal Order 25 | Vespiquen (from 21) |
| Lotad | wild | 12 | Oxide | Growl, Absorb, Nature Power, Mist | as Lombre: Fury Swipes 15, Water Sport 19, BubbleBeam 25 | Lombre (from 14); Ludicolo in Maylene |
| Lotad | wild | 12 | v3 | Growl, Water Gun, Nature Power, Mist | as Lombre: Fury Swipes 15, Water Sport 19, BubbleBeam 25 | Lombre (from 14); Ludicolo in Maylene |
| Pawmi | wild | 12 | both | Growl, ThunderShock, Quick Attack, Nuzzle | as Pawmo: Bite 19, Spark 23, Arm Thrust 25 | Pawmo (from 18); Pawmot in Maylene |
| Pikachu | wild | 12 | Oxide | ThunderShock, Growl, Tail Whip, Thunder Wave | Quick Attack 13, Double Team 18, Slam 21, Thunderbolt 26 | Pikachu; Raichu in Maylene |
| Pikachu | wild | 12 | v3 | ThunderShock, Growl, Tail Whip, Thunder Wave | Quick Attack 13, Double Team 18, Slam 21 | Pikachu; Raichu in Maylene |
| Cherubi | wild | 13 | both | Tackle, Growth, Leech Seed, Helping Hand | Magical Leaf 19; as Cherrim: Petal Dance 25 | Cherrim (from 25) |
| Hoppip | wild | 13 | Oxide | Synthesis, Tail Whip, Tackle, PoisonPowder | Stun Spore 14, Sleep Powder 16; as Skiploom: Bullet Seed 20, Leech Seed 24 | Skiploom (from 18); Jumpluff in Fantina |
| Hoppip | wild | 13 | v3 | Synthesis, Tail Whip, Tackle, PoisonPowder | Stun Spore 14, Sleep Powder 16; as Skiploom: Leech Seed 24 | Skiploom (from 18); Jumpluff in Fantina |
| Squirtle | wild | 13 | both | Tail Whip, Bubble, Withdraw, Water Gun | Bite 16; as Wartortle: Bite 16, Rapid Spin 20, Protect 24 | Wartortle (from 16); Blastoise in Maylene |
| Surskit | wild | 13 | Oxide | Bubble, Quick Attack, Sweet Scent | Water Sport 19; as Masquerain: Gust 22, Scary Face 26 | Masquerain (from 22) |
| Surskit | wild | 13 | v3 | Bubble, Quick Attack, Sweet Scent | Water Sport 19; as Masquerain: Scary Face 26 | Masquerain (from 22) |
| Wooper | wild | 13 to 14 | Oxide | Water Gun, Tail Whip, Mud Sport, Mud Shot | Slam 15, Mud Bomb 19; as Quagsire: Amnesia 24 | Quagsire (from 20) |
| Wooper | wild | 13 to 14 | Oxide | Water Gun, Tail Whip, Mud Sport, Mud Shot | as Clodsire: Slam 16, Yawn 21, Bulldoze 24 | Clodsire (from 13) |
| Wooper | wild | 13 to 14 | v3 | Water Gun, Tail Whip, Mud Sport, Mud Shot | Slam 15, Mud Bomb 19; as Quagsire: Amnesia 24 | Quagsire (from 20) |
| Wooper | wild | 13 to 14 | v3 | Water Gun, Tail Whip, Mud Sport, Mud Shot | as Clodsire: Mud Bomb 19, Yawn 21, Bulldoze 24 | Clodsire (from 13) |
| Dewpider | wild | 14 | Oxide | Bubble, Infestation, Bite, Aqua Ring | BubbleBeam 17, Bug Bite 21; as Araquanid: Headbutt 26 | Araquanid (from 22) |
| Dewpider | wild | 14 | v3 | Bubble, Water Gun, Bite, Aqua Ring | BubbleBeam 17, Bug Bite 21; as Araquanid: Headbutt 26 | Araquanid (from 22) |
| Marill | wild | 14 | Oxide | Tackle, Defense Curl, Tail Whip, Water Gun | Rollout 15, BubbleBeam 18; as Azumarill: BubbleBeam 20 | Azumarill (from 18) |
| Marill | wild | 14 | v3 | Tackle, Defense Curl, Tail Whip, Water Gun | BubbleBeam 18; as Azumarill: BubbleBeam 20 | Azumarill (from 18) |
| Shroomish | wild | 14 | Oxide | Absorb, Tackle, Stun Spore, Leech Seed | Mega Drain 17, Headbutt 21; as Breloom: Mach Punch 23, Counter 25 | Breloom (from 23) |
| Shroomish | wild | 14 | v3 | Tackle, Stun Spore, Leech Seed | Mega Drain 17, Headbutt 21; as Breloom: Mach Punch 23, Counter 25 | Breloom (from 23) |
| Buizel | wild | 15 | both | Quick Attack, Water Gun, Pursuit, Swift | Aqua Jet 21; as Floatzel: Crunch 26 | Floatzel (from 26) |
| Froakie | wild | 15 | both | Growl, Quick Attack, Lick, Water Pulse | Icy Wind 16; as Frogadier: Icy Wind 16, Faint Attack 20, Acrobatics 22, Low Kick 25 | Frogadier (from 16); Greninja in Maylene |
| Shellos | wild | 15 | both | Mud Sport, Harden, Water Pulse, Mud Bomb | Hidden Power 16 | Shellos; Gastrodon in Fantina |

## Route 211

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 26 | At the cap |
|---|---|---|---|---|---|---|
| Alolan Ninetales | wild | 13 to 16 | Oxide | Tail Whip, Disable, Ice Shard, Safeguard | nothing | Alolan Ninetales |
| Alolan Ninetales | wild | 13 to 16 | v3 | Tail Whip, Disable, Ice Shard, Safeguard | Icy Wind 16, Aurora Beam 24 | Alolan Ninetales |
| Bronzor | wild | 14 | Oxide | Confusion, Hypnosis, Imprison, Confuse Ray | Extrasensory 19, Iron Defense 26 | Bronzor; Bronzong in Fantina |
| Bronzor | wild | 14 | v3 | Confusion, Hypnosis, Imprison, Confuse Ray | Extrasensory 19, Iron Head 20, Iron Defense 26 | Bronzor; Bronzong in Fantina |
| Hoothoot | wild | 14 | both | Foresight, Hypnosis, Peck, Uproar | Reflect 17; as Noctowl: Confusion 22 | Noctowl (from 20) |
| Mienfoo | wild | 14 | Oxide | Pound, Rock Smash, Fake Out | DoubleSlap 17, Force Palm 20, Bounce 22, Drain Punch 25 | Mienfoo; Mienshao in Maylene |
| Mienfoo | wild | 14 | v3 | Pound, Rock Smash, Fake Out | DoubleSlap 17, Force Palm 20, Bounce 22 | Mienfoo; Mienshao in Maylene |
| Ponyta | wild | 14 | Oxide | Growl, Tackle, Tail Whip, Ember | Flame Wheel 15, Stomp 19, Fire Spin 24 | Ponyta; Rapidash in Wake |
| Ponyta | wild | 14 | Oxide | Growl, Tackle, Tail Whip, Ember | as Galarian Rapidash: Fairy Wind 15, Agility 20, Psybeam 25 | Galarian Rapidash (from 14) |
| Ponyta | wild | 14 | v3 | Growl, Tackle, Tail Whip, Ember | Flame Wheel 15, Stomp 19 | Ponyta; Rapidash in Wake |
| Ponyta | wild | 14 | v3 | Growl, Tackle, Tail Whip, Ember | as Galarian Rapidash: Psycho Cut on evolving, Fairy Wind 15, Agility 20, Psybeam 25 | Galarian Rapidash (from 14) |
| Rookidee | wild | 14 | Oxide | Peck, Leer, Fury Attack, Sand-Attack | Pluck 15; as Corvisquire: Steel Wing 20, Drill Peck 26 | Corvisquire (from 16); Corviknight in Wake |
| Rookidee | wild | 14 | v3 | Peck, Leer, Fury Attack, Sand-Attack | Pluck 15; as Corvisquire: Steel Wing 20 | Corvisquire (from 16); Corviknight in Wake |
| Vulpix | wild | 14 to 15 | Oxide | Tail Whip, Roar, Quick Attack, Will-O-Wisp | Confuse Ray 17, Imprison 21, Flamethrower 24 | Vulpix; Ninetales in Maylene |
| Vulpix | wild | 14 to 15 | v3 | Ember, Tail Whip, Roar, Quick Attack | Confuse Ray 17, Imprison 21, Flamethrower 24, Will-O-Wisp 26 | Vulpix; Ninetales in Maylene |
| Charmander | wild | 15 | both | Scratch, Growl, Ember, SmokeScreen | Dragon Rage 16; as Charmeleon: Dragon Rage 17, Scary Face 21 | Charmeleon (from 16); Charizard in Maylene |
| Chingling | wild | 15 | Oxide | Wrap, Growl, Astonish, Confusion | Uproar 17; as Chimecho: Take Down 22, Yawn 25 | Chimecho (from 20) |
| Chingling | wild | 15 | v3 | Growl, Confusion | Uproar 17; as Chimecho: Take Down 22, Yawn 25 | Chimecho (from 20) |
| Snover | wild | 15 | both | Leer, Razor Leaf, Icy Wind, GrassWhistle | Swagger 17, Mist 21, Ice Shard 26 | Snover; Abomasnow in Wake |
| Meditite | wild | 16 | both | Meditate, Confusion, Detect, Hidden Power | Mind Reader 18, Feint 22, Calm Mind 25 | Meditite; Medicham in Maylene |
| Zubat | wild | 16 | Oxide | Leech Life, Supersonic, Astonish, Bite | Wing Attack 17, Confuse Ray 21 | Golbat (from 22); Crobat in Wake |
| Zubat | wild | 16 | v3 | Leech Life, Supersonic, Acid, Bite | Wing Attack 17, Confuse Ray 21 | Golbat (from 22); Crobat in Wake |

## Valley Windworks

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 26 | At the cap |
|---|---|---|---|---|---|---|
| Buizel | old rod | 8 | both | Growl, Water Sport, Quick Attack, Water Gun | Pursuit 10, Swift 15, Aqua Jet 21; as Floatzel: Crunch 26 | Floatzel (from 26) |
| Carvanha | old rod | 8 | Oxide | Leer, Bite, Rage, Focus Energy | Scary Face 11, Ice Fang 16, Screech 18, Swagger 21, Assurance 26 | Carvanha; Sharpedo in Fantina |
| Carvanha | old rod | 8 | v3 | Leer, Bite, Water Gun, Focus Energy | Scary Face 11, Screech 18, Swagger 21, Assurance 26 | Carvanha; Sharpedo in Fantina |
| Chinchou | old rod | 8 | both | Bubble, Supersonic, Thunder Wave | Flail 9, Water Gun 12, Confuse Ray 17, Spark 20, Take Down 23 | Chinchou; Lanturn in Fantina |
| Mantyke | old rod | 8 | both | Tackle, Bubble, Supersonic | BubbleBeam 10, Headbutt 13, Agility 19, Wing Attack 22 | Mantyke; Mantine in Fantina |
| Mudkip | old rod | 8 | Oxide | Tackle, Growl, Mud-Slap | Water Gun 10, Bide 15; as Marshtomp: Mud Shot 16, Foresight 20, Mud Bomb 25 | Marshtomp (from 16); Swampert in Maylene |
| Mudkip | old rod | 8 | v3 | Tackle, Growl, Mud-Slap | Water Gun 10; as Marshtomp: Mud Shot 16, Foresight 20, Mud Bomb 25 | Marshtomp (from 16); Swampert in Maylene |
| Pawmi | wild | 9 to 12 | both | Scratch, Growl, ThunderShock, Quick Attack | Nuzzle 12; as Pawmo: Bite 19, Spark 23, Arm Thrust 25 | Pawmo (from 18); Pawmot in Maylene |
| Minccino | wild | 10 | both | Pound, Baby-Doll Eyes, Helping Hand | DoubleSlap 13, Sing 16, Echoed Voice 19, Swift 19, Encore 19, Charm 21, Tickle 23 | Minccino; Cinccino in Wake |
| Pachirisu | wild | 10 to 11 | Oxide | Growl, Bide, Quick Attack, Charm | Spark 13, Endure 17, Swift 21, Sweet Kiss 25 | Pachirisu |
| Pachirisu | wild | 10 to 11 | v3 | Growl, Quick Attack, Charm | Spark 13, Endure 17, Swift 21, Sweet Kiss 25 | Pachirisu |
| Pikipek | wild | 10 | both | Peck, Growl, Echoed Voice, Rock Smash | Supersonic 13; as Trumbeak: Pluck 16, Roost 21, Fury Attack 24 | Trumbeak (from 14); Toucannon in Fantina |
| Rookidee | wild | 10 | Oxide | Peck, Leer, Fury Attack | Sand-Attack 12, Pluck 15; as Corvisquire: Steel Wing 20, Drill Peck 26 | Corvisquire (from 16); Corviknight in Wake |
| Rookidee | wild | 10 | v3 | Peck, Leer, Fury Attack | Sand-Attack 12, Pluck 15; as Corvisquire: Steel Wing 20 | Corvisquire (from 16); Corviknight in Wake |
| Shinx | wild | 10 to 11 | both | Tackle, Leer, Charge | Spark 13; as Luxio: Bite 18, Roar 23 | Luxio (from 15); Luxray in Fantina |
| Minun | wild | 11 | both | Growl, Thunder Wave, Quick Attack, Helping Hand | Spark 15, Encore 17, Charm 21, Copycat 24 | Minun |
| Plusle | wild | 11 | both | Growl, Thunder Wave, Quick Attack, Helping Hand | Spark 15, Encore 17, Fake Tears 21, Copycat 24 | Plusle |
| Emolga | wild | 12 | Oxide | Tail Whip, ThunderShock, Quick Attack, Double Team | ThunderShock 15, Charge 15, Nuzzle 15, Pursuit 16, Spark 22, Shock Wave 22, Electro Ball 26 | Emolga |
| Emolga | wild | 12 | v3 | Nuzzle, Quick Attack, Tail Whip, Double Team | ThunderShock 15, Charge 15, Nuzzle 15, Pursuit 16, Spark 22, Shock Wave 22, Electro Ball 26 | Emolga |
| Pikachu | wild | 12 | Oxide | ThunderShock, Growl, Tail Whip, Thunder Wave | Quick Attack 13, Double Team 18, Slam 21, Thunderbolt 26 | Pikachu; Raichu in Maylene |
| Pikachu | wild | 12 | v3 | ThunderShock, Growl, Tail Whip, Thunder Wave | Quick Attack 13, Double Team 18, Slam 21 | Pikachu; Raichu in Maylene |

## Honey trees

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 26 | At the cap |
|---|---|---|---|---|---|---|
| Aipom | honey | 10 | Oxide | Scratch, Tail Whip, Sand-Attack, Astonish | Baton Pass 11, Tickle 15, Fury Swipes 18, Swift 22, Screech 25 | Aipom; Ambipom in Fantina |
| Aipom | honey | 10 | v3 | Scratch, Tail Whip, Sand-Attack, Tackle | Baton Pass 11, Tickle 15, Fury Swipes 18, Swift 22, Screech 25 | Aipom; Ambipom in Fantina |
| Bounsweet | honey | 10 | Oxide | Splash, Play Nice, Rapid Spin | Razor Leaf 12; as Steenee: Razor Leaf 12, Sweet Scent 17, Magical Leaf 21, Teeter Dance 23, Stomp 25 | Steenee (from 12); Tsareena in Fantina |
| Bounsweet | honey | 10 | v3 | Leafage, Play Nice, Rapid Spin | Razor Leaf 12; as Steenee: Razor Leaf 12, Sweet Scent 17, Magical Leaf 21, Teeter Dance 23, Stomp 25 | Steenee (from 12); Tsareena in Fantina |
| Burmy | honey | 10 | both | Protect, Tackle | Bug Bite 15, Hidden Power 20; as Wormadam: Hidden Power 20, Confusion 23, Razor Leaf 26 | Wormadam (from 20) |
| Burmy | honey | 10 | both | Protect, Tackle | Bug Bite 15, Hidden Power 20; as Mothim: Hidden Power 20, Confusion 23, Gust 26 | Mothim (from 20) |
| Cherubi | honey | 10 | both | Tackle, Growth, Leech Seed | Helping Hand 13, Magical Leaf 19; as Cherrim: Petal Dance 25 | Cherrim (from 25) |
| Combee | honey | 10 | both | Sweet Scent, Gust | Bug Bite 13; as Vespiquen: Power Gem 21, Heal Order 25 | Vespiquen (from 21) |
| Dottler | honey | 10 | Oxide | Reflect, Light Screen, Confusion, Struggle Bug | Psybeam 20 | Dottler; Orbeetle in Fantina |
| Dottler | honey | 10 | v3 | Struggle Bug, Reflect, Light Screen, Confusion | Psybeam 20 | Dottler; Orbeetle in Fantina |
| Grubbin | honey | 10 | Oxide | ViceGrip, Mud-Slap, String Shot, Bug Bite | Bite 15; as Charjabug: Spark 23 | Charjabug (from 20); Vikavolt in Maylene |
| Grubbin | honey | 10 | v3 | ViceGrip, Mud-Slap, String Shot, Bug Bite | Bite 15; as Charjabug: Charge on evolving, Spark 23 | Charjabug (from 20); Vikavolt in Maylene |
| Heracross | honey | 10 | Oxide | Leer, Horn Attack, Endure, Fury Attack | Aerial Ace 13, Brick Break 19, Counter 25 | Heracross |
| Heracross | honey | 10 | v3 | Leer, Horn Attack, Endure, Fury Attack | Aerial Ace 13, Counter 25, Brick Break 26 | Heracross |
| Munchlax | honey | 10 | both | Odor Sleuth, Tackle, Defense Curl, Amnesia | Lick 12, Recycle 17, Screech 20, Stockpile 25 | Munchlax; Snorlax in Maylene |
| Seedot | honey | 10 | Oxide | Bide, Harden, Growth | Nature Power 13 | Shiftry (from 14) |
| Seedot | honey | 10 | v3 | Harden, Growth | Nature Power 13 | Shiftry (from 14) |
| Sewaddle | honey | 10 | Oxide | Tackle, String Shot, Bug Bite | Razor Leaf 12 | Swadloon (from 20); Leavanny in Fantina |
| Sewaddle | honey | 10 | v3 | Tackle, String Shot, Bug Bite | Razor Leaf 12; as Swadloon: Protect on evolving | Swadloon (from 20); Leavanny in Fantina |
| Shroomish | honey | 10 | Oxide | Absorb, Tackle, Stun Spore | Leech Seed 13, Mega Drain 17, Headbutt 21; as Breloom: Mach Punch 23, Counter 25 | Breloom (from 23) |
| Shroomish | honey | 10 | v3 | Tackle, Stun Spore | Leech Seed 13, Mega Drain 17, Headbutt 21; as Breloom: Mach Punch 23, Counter 25 | Breloom (from 23) |

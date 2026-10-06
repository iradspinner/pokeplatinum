# Roark's split: what each catch knows and learns

Written by `tools/oxide/balance/learncheck.py sheets` for check 6 of the learnset baseline (`docs/oxide/learnset-checks.md`). One table per capture area first offered in Roark's split, whose cap is 16. Each Pokemon is read at the lowest level it is found at there. "Knows at capture" is the last four moves its list gives by that level; "learns by level-up" is every entry it reaches after capture up to 16, evolving on time, with each later stage's moves under its name; "at the cap" is the stage it can be by then and the next one after. A row marked v3 shows learnset v3 (unlanded, `origin/balance-learngen-v2`) where it differs from Oxide's lists; a row marked both is the same in each. Relearner-only moves and egg moves are left out. Nothing here is in the game data.

## Jubilife City

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 16 | At the cap |
|---|---|---|---|---|---|---|
| Abra | wild | 4 to 5 | Oxide | Teleport | as Kadabra: Confusion 16 | Kadabra (from 16); Alakazam in Wake |
| Abra | wild | 4 to 5 | v3 | Confusion | as Kadabra: Confusion 16 | Kadabra (from 16); Alakazam in Wake |
| Machop | wild | 5 | both | Low Kick, Leer | Focus Energy 7, Karate Chop 10, Foresight 13 | Machop; Machoke in Fantina |
| Minccino | wild | 5 | both | Pound, Baby-Doll Eyes, Helping Hand | DoubleSlap 13, Sing 16 | Minccino; Cinccino in Wake |
| Pawmi | wild | 5 | both | Scratch, Growl, ThunderShock | Quick Attack 6, Nuzzle 12 | Pawmi; Pawmo in Gardenia |
| Purrloin | wild | 5 to 6 | both | Scratch, Growl | Sand-Attack 6, Assist 6, Fake Out 12, Fury Swipes 12, Pursuit 15 | Purrloin; Liepard in Gardenia |
| Glameow | wild | 6 | both | Fake Out, Scratch | Growl 8, Hypnosis 13 | Glameow; Purugly in Maylene |
| Poochyena | wild | 6 | both | Tackle, Howl | Sand-Attack 9, Bite 13 | Poochyena; Mightyena in Gardenia |
| Rookidee | wild | 6 | both | Peck, Leer, Fury Attack | Sand-Attack 12, Pluck 15 | Corvisquire (from 16); Corviknight in Wake |
| Shinx | wild | 6 | both | Tackle, Leer | Charge 9, Spark 13 | Luxio (from 15); Luxray in Fantina |
| Starly | wild | 6 | both | Tackle, Growl, Quick Attack | Wing Attack 9, Double Team 13 | Staravia (from 14); Staraptor in Maylene |
| Murkrow | wild | 7 | Oxide | Peck, Astonish, Pursuit | Haze 11, Wing Attack 15 | Murkrow; Honchkrow in Fantina |
| Murkrow | wild | 7 | v3 | Peck, Pursuit | Haze 11, Wing Attack 15 | Murkrow; Honchkrow in Fantina |
| Skitty | wild | 7 | both | Growl, Tail Whip, Tackle, Foresight | Attract 8, Sing 11, DoubleSlap 15 | Skitty; Delcatty in Gardenia |
| Glameow | gift | 8 | both | Fake Out, Scratch, Growl | Hypnosis 13 | Glameow; Purugly in Maylene |
| Purrloin | gift | 8 | both | Scratch, Growl, Sand-Attack, Assist | Fake Out 12, Fury Swipes 12, Pursuit 15 | Purrloin; Liepard in Gardenia |
| Skitty | gift | 8 | both | Tail Whip, Tackle, Foresight, Attract | Sing 11, DoubleSlap 15 | Skitty; Delcatty in Gardenia |

## Lake Verity

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 16 | At the cap |
|---|---|---|---|---|---|---|
| Surskit | wild | 2 to 4 | both | Bubble | Quick Attack 7, Sweet Scent 13 | Surskit; Masquerain in Gardenia |
| Bidoof | wild | 3 | Oxide | Tackle | Growl 5, Defense Curl 9, Rollout 13; as Bibarel: Water Gun 15 | Bibarel (from 15) |
| Bidoof | wild | 3 | v3 | Tackle | Growl 5, Defense Curl 9; as Bibarel: Water Gun 15 | Bibarel (from 15) |
| Chinchou | old rod | 3 | both | Bubble, Supersonic | Thunder Wave 6, Flail 9, Water Gun 12 | Chinchou; Lanturn in Fantina |
| Goldeen | old rod | 3 | both | Peck, Tail Whip, Water Sport | Supersonic 7, Horn Attack 11 | Goldeen; Seaking in Fantina |
| Lotad | wild | 3 to 5 | Oxide | Astonish, Growl | Absorb 5, Nature Power 7, Mist 11; as Lombre: Fury Swipes 15 | Lombre (from 14); Ludicolo in Maylene |
| Lotad | wild | 3 to 5 | v3 | Growl | Water Gun 5, Nature Power 7, Mist 11; as Lombre: Fury Swipes 15 | Lombre (from 14); Ludicolo in Maylene |
| Mudkip | old rod | 3 | Oxide | Tackle, Growl | Mud-Slap 6, Water Gun 10, Bide 15; as Marshtomp: Mud Shot 16 | Marshtomp (from 16); Swampert in Maylene |
| Mudkip | old rod | 3 | v3 | Tackle, Growl | Mud-Slap 6, Water Gun 10; as Marshtomp: Mud Shot 16 | Marshtomp (from 16); Swampert in Maylene |
| Psyduck | old rod | 3 | both | Water Sport, Scratch | Tail Whip 5, Water Gun 9, Disable 14 | Psyduck; Golduck in Fantina |
| Purrloin | wild | 3 | both | Scratch, Growl | Sand-Attack 6, Assist 6, Fake Out 12, Fury Swipes 12, Pursuit 15 | Purrloin; Liepard in Gardenia |
| Skitty | wild | 3 | both | Fake Out, Growl, Tail Whip, Tackle | Foresight 4, Attract 8, Sing 11, DoubleSlap 15 | Skitty; Delcatty in Gardenia |
| Surskit | old rod | 3 | both | Bubble | Quick Attack 7, Sweet Scent 13 | Surskit; Masquerain in Gardenia |
| Wooloo | wild | 3 to 4 | both | Tackle, Growl | Defense Curl 4, Copycat 8, Guard Split 12, Double Kick 16 | Wooloo; Dubwool in Gardenia |
| Blipbug | wild | 4 | both | Struggle Bug | as Dottler: Reflect 10, Light Screen 10, Confusion 10 | Dottler (from 10); Orbeetle in Fantina |
| Buneary | wild | 4 | Oxide | Splash, Pound, Defense Curl, Foresight | Endure 6, Frustration 13, Quick Attack 16 | Buneary; Lopunny in Gardenia |
| Buneary | wild | 4 | v3 | Pound, Defense Curl, Foresight | Endure 6, Frustration 13, Quick Attack 16 | Buneary; Lopunny in Gardenia |
| Pikipek | wild | 4 | both | Peck, Growl | Echoed Voice 7, Rock Smash 9, Supersonic 13; as Trumbeak: Pluck 16 | Trumbeak (from 14); Toucannon in Fantina |
| Krabby | wild | 5 | both | Mud Sport, Bubble, ViceGrip | Leer 9, Harden 11, BubbleBeam 15 | Krabby; Kingler in Fantina |

## Oreburgh City

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 16 | At the cap |
|---|---|---|---|---|---|---|
| Vullaby | in-game trade | 1 | both | Gust, Leer | Fury Attack 5, Pluck 11, Flatter 12 | Vullaby; Mandibuzz in Candice |

## Oreburgh Gate

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 16 | At the cap |
|---|---|---|---|---|---|---|
| Zubat | wild | 5 to 6 | Oxide | Leech Life, Supersonic | Astonish 9, Bite 13 | Zubat; Golbat in Gardenia |
| Zubat | wild | 5 to 6 | v3 | Leech Life, Supersonic | Acid 9, Bite 13 | Zubat; Golbat in Gardenia |
| Makuhita | wild | 6 to 7 | both | Tackle, Focus Energy, Sand-Attack | Arm Thrust 7, Vital Throw 10, Fake Out 13, Whirlwind 16 | Makuhita; Hariyama in Gardenia |
| Nacli | wild | 6 | both | Tackle, Harden, Rock Throw | Mud Shot 7, Smack Down 10, Rock Polish 13, Headbutt 16 | Nacli; Naclstack in Gardenia |
| Nosepass | wild | 6 to 7 | both | Tackle | Harden 7, Rock Throw 13 | Nosepass; Probopass in Fantina |
| Nidoran♂ | wild | 7 | both | Leer, Peck, Focus Energy | Double Kick 9, Poison Sting 13 | Nidorino (from 16); Nidoking in Gardenia |
| Onix | wild | 7 | Oxide | Tackle, Harden, Bind, Screech | Rock Throw 9, Rage 14 | Onix; Steelix in Gardenia |
| Onix | wild | 7 | v3 | Mud Sport, Tackle, Harden, Screech | Rock Throw 9 | Onix; Steelix in Gardenia |
| Purrloin | wild | 7 to 8 | both | Scratch, Growl, Sand-Attack, Assist | Fake Out 12, Fury Swipes 12, Pursuit 15 | Purrloin; Liepard in Gardenia |
| Gligar | wild | 8 | both | Poison Sting, Sand-Attack | Harden 9, Knock Off 12, Quick Attack 16 | Gligar; Gliscor in Wake |

## Oreburgh Mine

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 16 | At the cap |
|---|---|---|---|---|---|---|
| Makuhita | wild | 5 to 7 | both | Tackle, Focus Energy, Sand-Attack | Arm Thrust 7, Vital Throw 10, Fake Out 13, Whirlwind 16 | Makuhita; Hariyama in Gardenia |
| Geodude | wild | 6 to 7 | both | Tackle, Defense Curl, Mud Sport | Rock Polish 8, Rock Throw 11, Magnitude 15 | Geodude; Graveler in Gardenia |
| Nacli | wild | 6 to 8 | both | Tackle, Harden, Rock Throw | Mud Shot 7, Smack Down 10, Rock Polish 13, Headbutt 16 | Nacli; Naclstack in Gardenia |
| Onix | wild | 6 | Oxide | Tackle, Harden, Bind, Screech | Rock Throw 9, Rage 14 | Onix; Steelix in Gardenia |
| Onix | wild | 6 | v3 | Mud Sport, Tackle, Harden, Screech | Rock Throw 9 | Onix; Steelix in Gardenia |
| Phanpy | wild | 6 to 7 | Oxide | Tackle, Growl, Defense Curl, Flail | Take Down 10, Rollout 15 | Phanpy; Donphan in Gardenia |
| Phanpy | wild | 6 to 7 | v3 | Tackle, Growl, Defense Curl, Flail | Take Down 10 | Phanpy; Donphan in Gardenia |
| Zubat | wild | 6 | Oxide | Leech Life, Supersonic | Astonish 9, Bite 13 | Zubat; Golbat in Gardenia |
| Zubat | wild | 6 | v3 | Leech Life, Supersonic | Acid 9, Bite 13 | Zubat; Golbat in Gardenia |
| Nosepass | wild | 7 | both | Tackle, Harden | Rock Throw 13 | Nosepass; Probopass in Fantina |
| Rhyhorn | wild | 7 | both | Horn Attack, Tail Whip | Stomp 9, Fury Attack 13 | Rhyhorn; Rhydon in Wake |
| Magby | wild | 8 | both | Smog, Leer, Ember | SmokeScreen 10, Faint Attack 16 | Magby; Magmar in Fantina |

## Ravaged Path

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 16 | At the cap |
|---|---|---|---|---|---|---|
| Zubat | wild | 3 to 4 | Oxide | Leech Life | Supersonic 5, Astonish 9, Bite 13 | Zubat; Golbat in Gardenia |
| Zubat | wild | 3 to 4 | v3 | Leech Life | Supersonic 5, Acid 9, Bite 13 | Zubat; Golbat in Gardenia |
| Geodude | wild | 4 | both | Tackle, Defense Curl, Mud Sport | Rock Polish 8, Rock Throw 11, Magnitude 15 | Geodude; Graveler in Gardenia |
| Makuhita | wild | 4 | both | Tackle, Focus Energy, Sand-Attack | Arm Thrust 7, Vital Throw 10, Fake Out 13, Whirlwind 16 | Makuhita; Hariyama in Gardenia |
| Nacli | wild | 4 to 5 | both | Tackle, Harden | Rock Throw 5, Mud Shot 7, Smack Down 10, Rock Polish 13, Headbutt 16 | Nacli; Naclstack in Gardenia |
| Nosepass | wild | 4 to 5 | both | Tackle | Harden 7, Rock Throw 13 | Nosepass; Probopass in Fantina |
| Phanpy | wild | 4 to 5 | Oxide | Odor Sleuth, Tackle, Growl, Defense Curl | Flail 6, Take Down 10, Rollout 15 | Phanpy; Donphan in Gardenia |
| Phanpy | wild | 4 to 5 | v3 | Odor Sleuth, Tackle, Growl, Defense Curl | Flail 6, Take Down 10 | Phanpy; Donphan in Gardenia |
| Barboach | old rod | 5 | both | Mud-Slap | Mud Sport 6, Water Sport 6, Water Gun 10, Mud Bomb 14 | Barboach; Whiscash in Fantina |
| Corphish | old rod | 5 | both | Bubble | Harden 7, ViceGrip 10, Leer 13 | Corphish; Crawdaunt in Fantina |
| Goldeen | old rod | 5 | both | Peck, Tail Whip, Water Sport | Supersonic 7, Horn Attack 11 | Goldeen; Seaking in Fantina |
| Lotad | wild | 5 to 6 | Oxide | Astonish, Growl, Absorb | Nature Power 7, Mist 11; as Lombre: Fury Swipes 15 | Lombre (from 14); Ludicolo in Maylene |
| Lotad | wild | 5 to 6 | v3 | Growl, Water Gun | Nature Power 7, Mist 11; as Lombre: Fury Swipes 15 | Lombre (from 14); Ludicolo in Maylene |
| Mudkip | old rod | 5 | Oxide | Tackle, Growl | Mud-Slap 6, Water Gun 10, Bide 15; as Marshtomp: Mud Shot 16 | Marshtomp (from 16); Swampert in Maylene |
| Mudkip | old rod | 5 | v3 | Tackle, Growl | Mud-Slap 6, Water Gun 10; as Marshtomp: Mud Shot 16 | Marshtomp (from 16); Swampert in Maylene |
| Onix | wild | 5 to 6 | Oxide | Mud Sport, Tackle, Harden, Bind | Screech 6, Rock Throw 9, Rage 14 | Onix; Steelix in Gardenia |
| Onix | wild | 5 to 6 | v3 | Mud Sport, Tackle, Harden | Screech 6, Rock Throw 9 | Onix; Steelix in Gardenia |
| Wooper | old rod | 5 | Oxide | Water Gun, Tail Whip, Mud Sport | Mud Shot 9, Slam 15 | Wooper; Quagsire in Gardenia |
| Wooper | old rod | 5 | Oxide | Water Gun, Tail Whip, Mud Sport | as Clodsire: Mud Shot 8, Poison Tail 12, Slam 16 | Clodsire (from 5) |
| Wooper | old rod | 5 | v3 | Water Gun, Tail Whip, Mud Sport | Mud Shot 9, Slam 15 | Wooper; Quagsire in Gardenia |
| Wooper | old rod | 5 | v3 | Water Gun, Tail Whip, Mud Sport | as Clodsire: Mud Shot 8 | Clodsire (from 5) |

## Route 201

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 16 | At the cap |
|---|---|---|---|---|---|---|
| Wooloo | wild | 2 | both | Tackle, Growl | Defense Curl 4, Copycat 8, Guard Split 12, Double Kick 16 | Wooloo; Dubwool in Gardenia |
| Blipbug | wild | 3 | both | Struggle Bug | as Dottler: Reflect 10, Light Screen 10, Confusion 10 | Dottler (from 10); Orbeetle in Fantina |
| Kricketot | wild | 3 | Oxide | Growl, Bide | as Kricketune: Fury Cutter 10, Leech Life 14 | Kricketune (from 10) |
| Kricketot | wild | 3 | v3 | Growl | nothing | Kricketune (from 10) |
| Purrloin | wild | 3 to 4 | both | Scratch, Growl | Sand-Attack 6, Assist 6, Fake Out 12, Fury Swipes 12, Pursuit 15 | Purrloin; Liepard in Gardenia |
| Rookidee | wild | 3 to 4 | both | Peck, Leer | Fury Attack 4, Sand-Attack 12, Pluck 15 | Corvisquire (from 16); Corviknight in Wake |
| Sentret | wild | 3 | both | Scratch, Foresight | Defense Curl 4, Quick Attack 7, Fury Swipes 13 | Furret (from 15) |
| Starly | wild | 3 | both | Tackle, Growl | Quick Attack 5, Wing Attack 9, Double Team 13 | Staravia (from 14); Staraptor in Maylene |
| Grubbin | wild | 4 | both | ViceGrip, Mud-Slap | String Shot 5, Bug Bite 10, Bite 15 | Grubbin; Charjabug in Gardenia |
| Nidoran♀ | wild | 4 | both | Growl, Scratch | Tail Whip 7, Double Kick 9, Poison Sting 13 | Nidorina (from 16); Nidoqueen in Gardenia |
| Nidoran♂ | wild | 4 | both | Leer, Peck | Focus Energy 7, Double Kick 9, Poison Sting 13 | Nidorino (from 16); Nidoking in Gardenia |
| Shinx | wild | 4 | both | Tackle | Leer 5, Charge 9, Spark 13 | Luxio (from 15); Luxray in Fantina |
| Fletchling | wild | 5 | both | Tackle, Growl | Quick Attack 6, Aerial Ace 12 | Fletchinder (from 16); Talonflame in Maylene |
| Pachirisu | wild | 5 | Oxide | Growl, Bide, Quick Attack | Charm 9, Spark 13 | Pachirisu |
| Pachirisu | wild | 5 | v3 | Growl, Quick Attack | Charm 9, Spark 13 | Pachirisu |
| Piplup | starter | 5 | both | Pound, Growl | Bubble 8, Water Sport 11, Peck 15; as Prinplup: Metal Claw 16 | Prinplup (from 16); Empoleon in Maylene |
| Scorbunny | starter | 5 | both | Ember, Growl | Quick Attack 6, Sand-Attack 11, Double Kick 14 | Raboot (from 16); Cinderace in Maylene |
| Turtwig | starter | 5 | Oxide | Tackle, Withdraw | Absorb 9, Razor Leaf 13 | Turtwig; Grotle in Gardenia |
| Turtwig | starter | 5 | v3 | Tackle, Withdraw | Leafage 9, Razor Leaf 13 | Turtwig; Grotle in Gardenia |

## Route 202

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 16 | At the cap |
|---|---|---|---|---|---|---|
| Shinx | wild | 2 | both | Tackle | Leer 5, Charge 9, Spark 13 | Luxio (from 15); Luxray in Fantina |
| Bidoof | wild | 3 | Oxide | Tackle | Growl 5, Defense Curl 9, Rollout 13; as Bibarel: Water Gun 15 | Bibarel (from 15) |
| Bidoof | wild | 3 | v3 | Tackle | Growl 5, Defense Curl 9; as Bibarel: Water Gun 15 | Bibarel (from 15) |
| Blipbug | wild | 3 | both | Struggle Bug | as Dottler: Reflect 10, Light Screen 10, Confusion 10 | Dottler (from 10); Orbeetle in Fantina |
| Kricketot | wild | 3 | Oxide | Growl, Bide | as Kricketune: Fury Cutter 10, Leech Life 14 | Kricketune (from 10) |
| Kricketot | wild | 3 | v3 | Growl | nothing | Kricketune (from 10) |
| Pikipek | wild | 3 | both | Peck, Growl | Echoed Voice 7, Rock Smash 9, Supersonic 13; as Trumbeak: Pluck 16 | Trumbeak (from 14); Toucannon in Fantina |
| Purrloin | wild | 3 to 4 | both | Scratch, Growl | Sand-Attack 6, Assist 6, Fake Out 12, Fury Swipes 12, Pursuit 15 | Purrloin; Liepard in Gardenia |
| Sewaddle | wild | 3 | both | Tackle, String Shot | Bug Bite 8, Razor Leaf 12 | Sewaddle; Swadloon in Gardenia |
| Wooloo | wild | 3 | both | Tackle, Growl | Defense Curl 4, Copycat 8, Guard Split 12, Double Kick 16 | Wooloo; Dubwool in Gardenia |
| Grubbin | wild | 4 | both | ViceGrip, Mud-Slap | String Shot 5, Bug Bite 10, Bite 15 | Grubbin; Charjabug in Gardenia |
| Nidoran♀ | wild | 4 | both | Growl, Scratch | Tail Whip 7, Double Kick 9, Poison Sting 13 | Nidorina (from 16); Nidoqueen in Gardenia |
| Nidoran♂ | wild | 4 | both | Leer, Peck | Focus Energy 7, Double Kick 9, Poison Sting 13 | Nidorino (from 16); Nidoking in Gardenia |
| Rookidee | wild | 4 | both | Peck, Leer, Fury Attack | Sand-Attack 12, Pluck 15 | Corvisquire (from 16); Corviknight in Wake |
| Starly | wild | 4 | both | Tackle, Growl | Quick Attack 5, Wing Attack 9, Double Team 13 | Staravia (from 14); Staraptor in Maylene |
| Budew | wild | 5 | Oxide | Absorb, Growth | Water Sport 7, Stun Spore 10, Mega Drain 13, Worry Seed 16 | Budew; Roselia in Fantina |
| Budew | wild | 5 | v3 | Growth | Water Sport 7, Stun Spore 10, Mega Drain 13, Worry Seed 16 | Budew; Roselia in Fantina |
| Smoliv | wild | 5 | Oxide | Tackle, Sweet Scent, Absorb | Growth 7, Razor Leaf 10, Helping Hand 13, Flail 16 | Smoliv; Dolliv in Gardenia |
| Smoliv | wild | 5 | v3 | Tackle, Sweet Scent, Leafage | Growth 7, Razor Leaf 10, Helping Hand 13, Flail 16 | Smoliv; Dolliv in Gardenia |

## Route 203

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 16 | At the cap |
|---|---|---|---|---|---|---|
| Barboach | old rod | 4 | both | Mud-Slap | Mud Sport 6, Water Sport 6, Water Gun 10, Mud Bomb 14 | Barboach; Whiscash in Fantina |
| Corphish | old rod | 4 | both | Bubble | Harden 7, ViceGrip 10, Leer 13 | Corphish; Crawdaunt in Fantina |
| Froakie | old rod | 4 | both | Pound | Water Gun 5, Growl 7, Quick Attack 10, Lick 13, Water Pulse 14, Icy Wind 16; as Frogadier: Icy Wind 16 | Frogadier (from 16); Greninja in Maylene |
| Poliwag | old rod | 4 | both | Water Sport | Bubble 5, Hypnosis 8, Water Gun 11, DoubleSlap 15 | Poliwag; Poliwhirl in Gardenia |
| Rookidee | wild | 4 | both | Peck, Leer, Fury Attack | Sand-Attack 12, Pluck 15 | Corvisquire (from 16); Corviknight in Wake |
| Wooper | old rod | 4 | Oxide | Water Gun, Tail Whip | Mud Sport 5, Mud Shot 9, Slam 15 | Wooper; Quagsire in Gardenia |
| Wooper | old rod | 4 | Oxide | Water Gun, Tail Whip | as Clodsire: Mud Shot 8, Poison Tail 12, Slam 16 | Clodsire (from 4) |
| Wooper | old rod | 4 | v3 | Water Gun, Tail Whip | Mud Sport 5, Mud Shot 9, Slam 15 | Wooper; Quagsire in Gardenia |
| Wooper | old rod | 4 | v3 | Water Gun, Tail Whip | as Clodsire: Mud Shot 8 | Clodsire (from 4) |
| Fletchling | wild | 5 to 7 | both | Tackle, Growl | Quick Attack 6, Aerial Ace 12 | Fletchinder (from 16); Talonflame in Maylene |
| Grubbin | wild | 5 | both | ViceGrip, Mud-Slap, String Shot | Bug Bite 10, Bite 15 | Grubbin; Charjabug in Gardenia |
| Nidoran♀ | wild | 5 | both | Growl, Scratch | Tail Whip 7, Double Kick 9, Poison Sting 13 | Nidorina (from 16); Nidoqueen in Gardenia |
| Nidoran♂ | wild | 5 | both | Leer, Peck | Focus Energy 7, Double Kick 9, Poison Sting 13 | Nidorino (from 16); Nidoking in Gardenia |
| Purrloin | wild | 5 to 6 | both | Scratch, Growl | Sand-Attack 6, Assist 6, Fake Out 12, Fury Swipes 12, Pursuit 15 | Purrloin; Liepard in Gardenia |
| Abra | wild | 6 to 7 | Oxide | Teleport | as Kadabra: Confusion 16 | Kadabra (from 16); Alakazam in Wake |
| Abra | wild | 6 to 7 | v3 | Confusion | as Kadabra: Confusion 16 | Kadabra (from 16); Alakazam in Wake |
| Makuhita | wild | 6 | both | Tackle, Focus Energy, Sand-Attack | Arm Thrust 7, Vital Throw 10, Fake Out 13, Whirlwind 16 | Makuhita; Hariyama in Gardenia |
| Shinx | wild | 6 | both | Tackle, Leer | Charge 9, Spark 13 | Luxio (from 15); Luxray in Fantina |

## Route 204

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 16 | At the cap |
|---|---|---|---|---|---|---|
| Budew | wild | 3 | Oxide | Absorb | Growth 4, Water Sport 7, Stun Spore 10, Mega Drain 13, Worry Seed 16 | Budew; Roselia in Fantina |
| Budew | wild | 3 | v3 | nothing | Growth 4, Water Sport 7, Stun Spore 10, Mega Drain 13, Worry Seed 16 | Budew; Roselia in Fantina |
| Bounsweet | wild | 4 to 5 | Oxide | Splash | Play Nice 5, Rapid Spin 9, Razor Leaf 12; as Steenee: Razor Leaf 12 | Steenee (from 12); Tsareena in Fantina |
| Bounsweet | wild | 4 to 5 | v3 | Leafage | Play Nice 5, Rapid Spin 9, Razor Leaf 12; as Steenee: Razor Leaf 12 | Steenee (from 12); Tsareena in Fantina |
| Fletchling | wild | 4 | both | Tackle, Growl | Quick Attack 6, Aerial Ace 12 | Fletchinder (from 16); Talonflame in Maylene |
| Grubbin | wild | 4 | both | ViceGrip, Mud-Slap | String Shot 5, Bug Bite 10, Bite 15 | Grubbin; Charjabug in Gardenia |
| Purrloin | wild | 4 | both | Scratch, Growl | Sand-Attack 6, Assist 6, Fake Out 12, Fury Swipes 12, Pursuit 15 | Purrloin; Liepard in Gardenia |
| Seedot | wild | 4 to 5 | Oxide | Bide, Harden | Growth 7, Nature Power 13 | Nuzleaf (from 14); Shiftry in Gardenia |
| Seedot | wild | 4 to 5 | v3 | Harden | Growth 7, Nature Power 13 | Nuzleaf (from 14); Shiftry in Gardenia |
| Sewaddle | wild | 4 to 5 | both | Tackle, String Shot | Bug Bite 8, Razor Leaf 12 | Sewaddle; Swadloon in Gardenia |
| Wurmple | wild | 4 | Oxide | Tackle, String Shot | Poison Sting 5; as Silcoon: Harden 7; as Beautifly: Absorb 10, Gust 13 | Beautifly (from 10) |
| Wurmple | wild | 4 | Oxide | Tackle, String Shot | Poison Sting 5; as Cascoon: Harden 7; as Dustox: Confusion 10, Gust 13 | Dustox (from 10) |
| Wurmple | wild | 4 | v3 | Tackle, String Shot | Poison Sting 5; as Silcoon: Harden 7; as Beautifly: Gust 13 | Beautifly (from 10) |
| Wurmple | wild | 4 | v3 | Tackle, String Shot | Poison Sting 5; as Cascoon: Harden 7; as Dustox: Confusion 10, Gust 13 | Dustox (from 10) |
| Barboach | old rod | 5 | both | Mud-Slap | Mud Sport 6, Water Sport 6, Water Gun 10, Mud Bomb 14 | Barboach; Whiscash in Fantina |
| Corphish | old rod | 5 | both | Bubble | Harden 7, ViceGrip 10, Leer 13 | Corphish; Crawdaunt in Fantina |
| Froakie | old rod | 5 | both | Pound, Water Gun | Growl 7, Quick Attack 10, Lick 13, Water Pulse 14, Icy Wind 16; as Frogadier: Icy Wind 16 | Frogadier (from 16); Greninja in Maylene |
| Goldeen | old rod | 5 | both | Peck, Tail Whip, Water Sport | Supersonic 7, Horn Attack 11 | Goldeen; Seaking in Fantina |
| Lotad | old rod | 5 | Oxide | Astonish, Growl, Absorb | Nature Power 7, Mist 11; as Lombre: Fury Swipes 15 | Lombre (from 14); Ludicolo in Maylene |
| Lotad | old rod | 5 | v3 | Growl, Water Gun | Nature Power 7, Mist 11; as Lombre: Fury Swipes 15 | Lombre (from 14); Ludicolo in Maylene |
| Lotad | wild | 5 | Oxide | Astonish, Growl, Absorb | Nature Power 7, Mist 11; as Lombre: Fury Swipes 15 | Lombre (from 14); Ludicolo in Maylene |
| Lotad | wild | 5 | v3 | Growl, Water Gun | Nature Power 7, Mist 11; as Lombre: Fury Swipes 15 | Lombre (from 14); Ludicolo in Maylene |
| Shroomish | wild | 5 | Oxide | Absorb, Tackle | Stun Spore 9, Leech Seed 13 | Shroomish; Breloom in Gardenia |
| Shroomish | wild | 5 | v3 | Tackle | Stun Spore 9, Leech Seed 13 | Shroomish; Breloom in Gardenia |
| Wooloo | wild | 5 | both | Tackle, Growl, Defense Curl | Copycat 8, Guard Split 12, Double Kick 16 | Wooloo; Dubwool in Gardenia |
| Smoliv | wild | 6 | Oxide | Tackle, Sweet Scent, Absorb | Growth 7, Razor Leaf 10, Helping Hand 13, Flail 16 | Smoliv; Dolliv in Gardenia |
| Smoliv | wild | 6 | v3 | Tackle, Sweet Scent, Leafage | Growth 7, Razor Leaf 10, Helping Hand 13, Flail 16 | Smoliv; Dolliv in Gardenia |
| Snivy | wild | 6 | Oxide | Tackle, Vine Whip, Leer | Wrap 10, Hold Back 14 | Servine (from 16); Serperior in Maylene |
| Snivy | wild | 6 | v3 | Tackle, Vine Whip, Leer | Leafage 10, Hold Back 14 | Servine (from 16); Serperior in Maylene |

## Route 207

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 16 | At the cap |
|---|---|---|---|---|---|---|
| Ponyta | wild | 5 | both | Growl, Tackle | Tail Whip 6, Ember 10, Flame Wheel 15 | Ponyta; Galarian Rapidash in Gardenia, Rapidash in Wake |
| Fletchling | wild | 6 to 7 | both | Tackle, Growl, Quick Attack | Aerial Ace 12 | Fletchinder (from 16); Talonflame in Maylene |
| Houndour | wild | 6 to 7 | both | Leer, Ember, Howl | Smog 9, Roar 14 | Houndour; Houndoom in Fantina |
| Machop | wild | 6 | both | Low Kick, Leer | Focus Energy 7, Karate Chop 10, Foresight 13 | Machop; Machoke in Fantina |
| Nacli | wild | 6 | both | Tackle, Harden, Rock Throw | Mud Shot 7, Smack Down 10, Rock Polish 13, Headbutt 16 | Nacli; Naclstack in Gardenia |
| Smoliv | wild | 6 to 7 | Oxide | Tackle, Sweet Scent, Absorb | Growth 7, Razor Leaf 10, Helping Hand 13, Flail 16 | Smoliv; Dolliv in Gardenia |
| Smoliv | wild | 6 to 7 | v3 | Tackle, Sweet Scent, Leafage | Growth 7, Razor Leaf 10, Helping Hand 13, Flail 16 | Smoliv; Dolliv in Gardenia |
| Vulpix | wild | 6 | Oxide | Ember, Tail Whip | Roar 7, Quick Attack 11, Will-O-Wisp 14 | Vulpix; Ninetales in Maylene |
| Vulpix | wild | 6 | v3 | Ember, Tail Whip | Roar 7, Quick Attack 11 | Vulpix; Ninetales in Maylene |
| Geodude | wild | 7 | both | Tackle, Defense Curl, Mud Sport | Rock Polish 8, Rock Throw 11, Magnitude 15 | Geodude; Graveler in Gardenia |
| Makuhita | wild | 7 | both | Tackle, Focus Energy, Sand-Attack, Arm Thrust | Vital Throw 10, Fake Out 13, Whirlwind 16 | Makuhita; Hariyama in Gardenia |
| Phanpy | wild | 7 | Oxide | Tackle, Growl, Defense Curl, Flail | Take Down 10, Rollout 15 | Phanpy; Donphan in Gardenia |
| Phanpy | wild | 7 | v3 | Tackle, Growl, Defense Curl, Flail | Take Down 10 | Phanpy; Donphan in Gardenia |
| Charmander | wild | 8 | both | Scratch, Growl, Ember | SmokeScreen 10, Dragon Rage 16 | Charmeleon (from 16); Charizard in Maylene |
| Fennekin | wild | 8 | both | Scratch, Tail Whip, Ember | Role Play 9, Psybeam 13 | Braixen (from 16); Delphox in Maylene |

## Route 218

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 16 | At the cap |
|---|---|---|---|---|---|---|
| Corsola | old rod | 5 | Oxide | Tackle, Harden | Bubble 8, Recover 13, Refresh 16 | Corsola |
| Corsola | old rod | 5 | v3 | Tackle, Harden | Bubble 8, Refresh 16 | Corsola |
| Finneon | old rod | 5 | both | Pound | Water Gun 6, Attract 10 | Finneon; Lumineon in Fantina |
| Krabby | old rod | 5 | both | Mud Sport, Bubble, ViceGrip | Leer 9, Harden 11, BubbleBeam 15 | Krabby; Kingler in Fantina |
| Remoraid | old rod | 5 | both | Water Gun | Lock-On 6, Psybeam 10, Aurora Beam 14 | Remoraid; Octillery in Gardenia |
| Squirtle | old rod | 5 | both | Tackle, Tail Whip | Bubble 7, Withdraw 10, Water Gun 13, Bite 16; as Wartortle: Bite 16 | Wartortle (from 16); Blastoise in Maylene |

## Route 219

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 16 | At the cap |
|---|---|---|---|---|---|---|
| Finneon | old rod | 4 | both | Pound | Water Gun 6, Attract 10 | Finneon; Lumineon in Fantina |
| Froakie | old rod | 4 | both | Pound | Water Gun 5, Growl 7, Quick Attack 10, Lick 13, Water Pulse 14, Icy Wind 16; as Frogadier: Icy Wind 16 | Frogadier (from 16); Greninja in Maylene |
| Luvdisc | old rod | 4 | both | Tackle, Charm | Water Gun 7, Agility 9, Take Down 14 | Luvdisc; Alomomola in Fantina |
| Remoraid | old rod | 4 | both | Water Gun | Lock-On 6, Psybeam 10, Aurora Beam 14 | Remoraid; Octillery in Gardenia |
| Tentacool | old rod | 4 | Oxide | Poison Sting | Supersonic 5, Constrict 8, Acid 12, Toxic Spikes 15 | Tentacool; Tentacruel in Fantina |
| Tentacool | old rod | 4 | v3 | Poison Sting | Supersonic 5, Water Gun 8, Acid 12, Toxic Spikes 15 | Tentacool; Tentacruel in Fantina |

## Sandgem Town

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 16 | At the cap |
|---|---|---|---|---|---|---|
| Kricketot | wild | 3 to 4 | Oxide | Growl, Bide | as Kricketune: Fury Cutter 10, Leech Life 14 | Kricketune (from 10) |
| Kricketot | wild | 3 to 4 | v3 | Growl | nothing | Kricketune (from 10) |
| Bidoof | wild | 4 | Oxide | Tackle | Growl 5, Defense Curl 9, Rollout 13; as Bibarel: Water Gun 15 | Bibarel (from 15) |
| Bidoof | wild | 4 | v3 | Tackle | Growl 5, Defense Curl 9; as Bibarel: Water Gun 15 | Bibarel (from 15) |
| Pikipek | wild | 4 to 5 | both | Peck, Growl | Echoed Voice 7, Rock Smash 9, Supersonic 13; as Trumbeak: Pluck 16 | Trumbeak (from 14); Toucannon in Fantina |
| Purrloin | wild | 4 | both | Scratch, Growl | Sand-Attack 6, Assist 6, Fake Out 12, Fury Swipes 12, Pursuit 15 | Purrloin; Liepard in Gardenia |
| Starly | wild | 4 | both | Tackle, Growl | Quick Attack 5, Wing Attack 9, Double Team 13 | Staravia (from 14); Staraptor in Maylene |
| Wurmple | wild | 4 | Oxide | Tackle, String Shot | Poison Sting 5; as Silcoon: Harden 7; as Beautifly: Absorb 10, Gust 13 | Beautifly (from 10) |
| Wurmple | wild | 4 | Oxide | Tackle, String Shot | Poison Sting 5; as Cascoon: Harden 7; as Dustox: Confusion 10, Gust 13 | Dustox (from 10) |
| Wurmple | wild | 4 | v3 | Tackle, String Shot | Poison Sting 5; as Silcoon: Harden 7; as Beautifly: Gust 13 | Beautifly (from 10) |
| Wurmple | wild | 4 | v3 | Tackle, String Shot | Poison Sting 5; as Cascoon: Harden 7; as Dustox: Confusion 10, Gust 13 | Dustox (from 10) |
| Blipbug | wild | 5 | both | Struggle Bug | as Dottler: Reflect 10, Light Screen 10, Confusion 10 | Dottler (from 10); Orbeetle in Fantina |
| Rookidee | wild | 5 | both | Peck, Leer, Fury Attack | Sand-Attack 12, Pluck 15 | Corvisquire (from 16); Corviknight in Wake |
| Sentret | wild | 5 | both | Scratch, Foresight, Defense Curl | Quick Attack 7, Fury Swipes 13 | Furret (from 15) |
| Wingull | wild | 5 | both | Growl, Water Gun | Supersonic 6, Wing Attack 11, Mist 16 | Wingull; Pelipper in Gardenia |
| Wooloo | wild | 5 | both | Tackle, Growl, Defense Curl | Copycat 8, Guard Split 12, Double Kick 16 | Wooloo; Dubwool in Gardenia |
| Abra | wild | 6 | Oxide | Teleport | as Kadabra: Confusion 16 | Kadabra (from 16); Alakazam in Wake |
| Abra | wild | 6 | v3 | Confusion | as Kadabra: Confusion 16 | Kadabra (from 16); Alakazam in Wake |
| Poochyena | wild | 6 | both | Tackle, Howl | Sand-Attack 9, Bite 13 | Poochyena; Mightyena in Gardenia |

## Twinleaf Town

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 16 | At the cap |
|---|---|---|---|---|---|---|
| Barboach | old rod | 3 | both | Mud-Slap | Mud Sport 6, Water Sport 6, Water Gun 10, Mud Bomb 14 | Barboach; Whiscash in Fantina |
| Buizel | old rod | 3 | both | SonicBoom, Growl, Water Sport, Quick Attack | Water Gun 6, Pursuit 10, Swift 15 | Buizel; Floatzel in Gardenia |
| Corphish | old rod | 3 | both | Bubble | Harden 7, ViceGrip 10, Leer 13 | Corphish; Crawdaunt in Fantina |
| Goldeen | old rod | 3 | both | Peck, Tail Whip, Water Sport | Supersonic 7, Horn Attack 11 | Goldeen; Seaking in Fantina |
| Squirtle | old rod | 3 | both | Tackle | Tail Whip 4, Bubble 7, Withdraw 10, Water Gun 13, Bite 16; as Wartortle: Bite 16 | Wartortle (from 16); Blastoise in Maylene |

## Verity Lakefront

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 16 | At the cap |
|---|---|---|---|---|---|---|
| Starly | wild | 2 | both | Tackle, Growl | Quick Attack 5, Wing Attack 9, Double Team 13 | Staravia (from 14); Staraptor in Maylene |
| Blipbug | wild | 3 | both | Struggle Bug | as Dottler: Reflect 10, Light Screen 10, Confusion 10 | Dottler (from 10); Orbeetle in Fantina |
| Kricketot | wild | 3 | Oxide | Growl, Bide | as Kricketune: Fury Cutter 10, Leech Life 14 | Kricketune (from 10) |
| Kricketot | wild | 3 | v3 | Growl | nothing | Kricketune (from 10) |
| Minccino | wild | 3 | both | Pound, Baby-Doll Eyes | Helping Hand 5, DoubleSlap 13, Sing 16 | Minccino; Cinccino in Wake |
| Pikipek | wild | 3 | both | Peck, Growl | Echoed Voice 7, Rock Smash 9, Supersonic 13; as Trumbeak: Pluck 16 | Trumbeak (from 14); Toucannon in Fantina |
| Purrloin | wild | 3 to 4 | both | Scratch, Growl | Sand-Attack 6, Assist 6, Fake Out 12, Fury Swipes 12, Pursuit 15 | Purrloin; Liepard in Gardenia |
| Wooloo | wild | 3 to 4 | both | Tackle, Growl | Defense Curl 4, Copycat 8, Guard Split 12, Double Kick 16 | Wooloo; Dubwool in Gardenia |
| Buneary | wild | 4 to 5 | Oxide | Splash, Pound, Defense Curl, Foresight | Endure 6, Frustration 13, Quick Attack 16 | Buneary; Lopunny in Gardenia |
| Buneary | wild | 4 to 5 | v3 | Pound, Defense Curl, Foresight | Endure 6, Frustration 13, Quick Attack 16 | Buneary; Lopunny in Gardenia |
| Sentret | wild | 4 | both | Scratch, Foresight, Defense Curl | Quick Attack 7, Fury Swipes 13 | Furret (from 15) |
| Surskit | wild | 4 | both | Bubble | Quick Attack 7, Sweet Scent 13 | Surskit; Masquerain in Gardenia |
| Vulpix | wild | 4 to 5 | Oxide | Ember, Tail Whip | Roar 7, Quick Attack 11, Will-O-Wisp 14 | Vulpix; Ninetales in Maylene |
| Vulpix | wild | 4 to 5 | v3 | Ember, Tail Whip | Roar 7, Quick Attack 11 | Vulpix; Ninetales in Maylene |

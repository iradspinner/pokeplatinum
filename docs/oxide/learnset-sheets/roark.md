# Roark's split: what each catch knows and learns

Written by `tools/oxide/balance/learncheck.py sheets` for check 6 of the learnset baseline (`docs/oxide/learnset-checks.md`). One table per capture area first offered in Roark's split, whose cap is 16. Each Pokemon is read at the lowest level it is found at there. "Knows at capture" is the last four moves its list gives by that level; "learns by level-up" is every entry it reaches after capture up to 16, evolving on time, with each later stage's moves under its name; "at the cap" is the stage it can be by then and the next one after. A row marked Rewrite shows the learnset rewrite's lists (the tree's) where it differs from the row marked Oxide, Oxide's lists before the learnset rewrite (`da6b92496c`); a row marked both is the same in each. Relearner-only moves and egg moves are left out.

## Jubilife City

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 16 | At the cap |
|---|---|---|---|---|---|---|
| Abra | wild | 4 to 5 | Oxide | Teleport | as Kadabra: Confusion 16 | Kadabra (from 16); Alakazam in Wake |
| Abra | wild | 4 to 5 | Rewrite | Psycho Cut | Confusion 5, Role Play 7, Reflect 10, Disable 13, Calm Mind 16 | Kadabra (from 16); Alakazam in Wake |
| Machop | wild | 5 | Oxide | Low Kick, Leer | Focus Energy 7, Karate Chop 10, Foresight 13 | Machop; Machoke in Fantina |
| Machop | wild | 5 | Rewrite | Low Kick, Leer | Scary Face 6, Focus Energy 7, Karate Chop 10, Foresight 13, Bullet Punch 16 | Machop; Machoke in Fantina |
| Minccino | wild | 5 | Oxide | Pound, Baby-Doll Eyes, Helping Hand | DoubleSlap 13, Sing 16 | Minccino; Cinccino in Wake |
| Minccino | wild | 5 | Rewrite | Pound, Baby-Doll Eyes, Helping Hand | Chilling Water 7, Swift 9, DoubleSlap 13, Sing 16 | Minccino; Cinccino in Wake |
| Pawmi | wild | 5 | Oxide | Scratch, Growl, ThunderShock | Quick Attack 6, Nuzzle 12 | Pawmi; Pawmo in Gardenia |
| Pawmi | wild | 5 | Rewrite | Scratch, ThunderShock | Quick Attack 6, Electroweb 9, Nuzzle 12, Mach Punch 15 | Pawmi; Pawmo in Gardenia |
| Purrloin | wild | 5 to 6 | Oxide | Scratch, Growl | Sand-Attack 6, Assist 6, Fake Out 12, Fury Swipes 12, Pursuit 15 | Purrloin; Liepard in Gardenia |
| Purrloin | wild | 5 to 6 | Rewrite | Scratch, Taunt | Sand-Attack 6, Snarl 9, Fury Swipes 11, Fake Out 12, Pursuit 15 | Purrloin; Liepard in Gardenia |
| Glameow | wild | 6 | Oxide | Fake Out, Scratch | Growl 8, Hypnosis 13 | Glameow; Purugly in Maylene |
| Glameow | wild | 6 | Rewrite | Fake Out, Scratch | Growl 8, Taunt 10, Hypnosis 13 | Glameow; Purugly in Maylene |
| Poochyena | wild | 6 | Oxide | Tackle, Howl | Sand-Attack 9, Bite 13 | Poochyena; Mightyena in Gardenia |
| Poochyena | wild | 6 | Rewrite | Tackle, Howl | Scary Face 7, Sand-Attack 9, Bite 13 | Poochyena; Mightyena in Gardenia |
| Rookidee | wild | 6 | Oxide | Peck, Leer, Fury Attack | Sand-Attack 12, Pluck 15 | Corvisquire (from 16); Corviknight in Wake |
| Rookidee | wild | 6 | Rewrite | Peck, Leer, Taunt | Sand-Attack 12, Pluck 15 | Corvisquire (from 16); Corviknight in Wake |
| Shinx | wild | 6 | Oxide | Tackle, Leer | Charge 9, Spark 13 | Luxio (from 15); Luxray in Fantina |
| Shinx | wild | 6 | Rewrite | Tackle, Scary Face, Pursuit | Charge 9, Spark 13 | Luxio (from 15); Luxray in Fantina |
| Starly | wild | 6 | Oxide | Tackle, Growl, Quick Attack | Wing Attack 9, Double Team 13 | Staravia (from 14); Staraptor in Maylene |
| Starly | wild | 6 | Rewrite | Tackle, Tailwind, Quick Attack | Wing Attack 9, Pursuit 14 | Staravia (from 14); Staraptor in Maylene |
| Murkrow | wild | 7 | Oxide | Peck, Astonish, Pursuit | Haze 11, Wing Attack 15 | Murkrow; Honchkrow in Fantina |
| Murkrow | wild | 7 | Rewrite | Peck, Astonish, Pursuit | Twister 8, Taunt 10, Wing Attack 15 | Murkrow; Honchkrow in Fantina |
| Skitty | wild | 7 | Oxide | Growl, Tail Whip, Tackle, Foresight | Attract 8, Sing 11, DoubleSlap 15 | Skitty; Delcatty in Gardenia |
| Skitty | wild | 7 | Rewrite | Fake Out, Tackle, Foresight, Baby-Doll Eyes | Attract 8, Sing 11, Quick Attack 13, DoubleSlap 15 | Skitty; Delcatty in Gardenia |
| Glameow | gift | 8 | Oxide | Fake Out, Scratch, Growl | Hypnosis 13 | Glameow; Purugly in Maylene |
| Glameow | gift | 8 | Rewrite | Fake Out, Scratch, Growl | Taunt 10, Hypnosis 13 | Glameow; Purugly in Maylene |
| Purrloin | gift | 8 | Oxide | Scratch, Growl, Sand-Attack, Assist | Fake Out 12, Fury Swipes 12, Pursuit 15 | Purrloin; Liepard in Gardenia |
| Purrloin | gift | 8 | Rewrite | Scratch, Taunt, Sand-Attack | Snarl 9, Fury Swipes 11, Fake Out 12, Pursuit 15 | Purrloin; Liepard in Gardenia |
| Skitty | gift | 8 | Oxide | Tail Whip, Tackle, Foresight, Attract | Sing 11, DoubleSlap 15 | Skitty; Delcatty in Gardenia |
| Skitty | gift | 8 | Rewrite | Tackle, Foresight, Baby-Doll Eyes, Attract | Sing 11, Quick Attack 13, DoubleSlap 15 | Skitty; Delcatty in Gardenia |

## Lake Verity

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 16 | At the cap |
|---|---|---|---|---|---|---|
| Surskit | wild | 2 to 4 | Oxide | Bubble | Quick Attack 7, Sweet Scent 13 | Surskit; Masquerain in Gardenia |
| Surskit | wild | 2 to 4 | Rewrite | Bubble | Sticky Web 3, Quick Attack 7, Gust 10, Silver Wind 13 | Surskit; Masquerain in Gardenia |
| Bidoof | wild | 3 | Oxide | Tackle | Growl 5, Defense Curl 9, Rollout 13; as Bibarel: Water Gun 15 | Bibarel (from 15) |
| Bidoof | wild | 3 | Rewrite | Tackle | Taunt 4, Aqua Jet 6, Swift 8, Rollout 13; as Bibarel: Water Gun 15 | Bibarel (from 15) |
| Chinchou | old rod | 3 | Oxide | Bubble, Supersonic | Thunder Wave 6, Flail 9, Water Gun 12 | Chinchou; Lanturn in Fantina |
| Chinchou | old rod | 3 | Rewrite | Bubble, Supersonic | Shock Wave 4, Thunder Wave 6, Flail 9, Water Gun 12, Screech 14 | Chinchou; Lanturn in Fantina |
| Goldeen | old rod | 3 | Oxide | Peck, Tail Whip, Water Sport | Supersonic 7, Horn Attack 11 | Goldeen; Seaking in Fantina |
| Goldeen | old rod | 3 | Rewrite | Peck, Water Sport | Flip Turn 4, Water Pulse 10, Horn Attack 11 | Goldeen; Seaking in Fantina |
| Lotad | wild | 3 to 5 | Oxide | Astonish, Growl | Absorb 5, Nature Power 7, Mist 11; as Lombre: Fury Swipes 15 | Lombre (from 14); Ludicolo in Maylene |
| Lotad | wild | 3 to 5 | Rewrite | Astonish | Magical Leaf 4, Water Gun 6, Mist 11, Disarming Voice 14; as Lombre: Fake Out 14, Fury Swipes 15, Natural Gift 16 | Lombre (from 14); Ludicolo in Maylene |
| Mudkip | old rod | 3 | Oxide | Tackle, Growl | Mud-Slap 6, Water Gun 10, Bide 15; as Marshtomp: Mud Shot 16 | Marshtomp (from 16); Swampert in Maylene |
| Mudkip | old rod | 3 | Rewrite | Tackle | Mud-Slap 6, Water Gun 10, Screech 13, Water Pulse 16; as Marshtomp: Mud Shot 16 | Marshtomp (from 16); Swampert in Maylene |
| Psyduck | old rod | 3 | Oxide | Water Sport, Scratch | Tail Whip 5, Water Gun 9, Disable 14 | Psyduck; Golduck in Fantina |
| Psyduck | old rod | 3 | Rewrite | Scratch | Screech 4, Trailblaze 6, Water Gun 9, Water Pulse 12, Disable 14 | Psyduck; Golduck in Fantina |
| Purrloin | wild | 3 | Oxide | Scratch, Growl | Sand-Attack 6, Assist 6, Fake Out 12, Fury Swipes 12, Pursuit 15 | Purrloin; Liepard in Gardenia |
| Purrloin | wild | 3 | Rewrite | Scratch | Taunt 4, Sand-Attack 6, Snarl 9, Fury Swipes 11, Fake Out 12, Pursuit 15 | Purrloin; Liepard in Gardenia |
| Skitty | wild | 3 | Oxide | Fake Out, Growl, Tail Whip, Tackle | Foresight 4, Attract 8, Sing 11, DoubleSlap 15 | Skitty; Delcatty in Gardenia |
| Skitty | wild | 3 | Rewrite | Fake Out, Tackle | Foresight 4, Baby-Doll Eyes 6, Attract 8, Sing 11, Quick Attack 13, DoubleSlap 15 | Skitty; Delcatty in Gardenia |
| Surskit | old rod | 3 | Oxide | Bubble | Quick Attack 7, Sweet Scent 13 | Surskit; Masquerain in Gardenia |
| Surskit | old rod | 3 | Rewrite | Bubble, Sticky Web | Quick Attack 7, Gust 10, Silver Wind 13 | Surskit; Masquerain in Gardenia |
| Wooloo | wild | 3 to 4 | Oxide | Tackle, Growl | Defense Curl 4, Copycat 8, Guard Split 12, Double Kick 16 | Wooloo; Dubwool in Gardenia |
| Wooloo | wild | 3 to 4 | Rewrite | Tackle, Round | Guard Split 12, Double Kick 16 | Wooloo; Dubwool in Gardenia |
| Blipbug | wild | 4 | Oxide | Struggle Bug | as Dottler: Reflect 10, Light Screen 10, Confusion 10 | Dottler (from 10); Orbeetle in Fantina |
| Blipbug | wild | 4 | Rewrite | Struggle Bug, Calm Mind | Trailblaze 10; as Dottler: Reflect 10, Confusion 11, Light Screen 12 | Dottler (from 10); Orbeetle in Fantina |
| Buneary | wild | 4 | Oxide | Splash, Pound, Defense Curl, Foresight | Endure 6, Frustration 13, Quick Attack 16 | Buneary; Lopunny in Gardenia |
| Buneary | wild | 4 | Rewrite | Pound, Defense Curl, Foresight | Covet 5, Endure 6, Baby-Doll Eyes 8, Power-Up Punch 9, Return 12, Frustration 13, Quick Attack 16 | Buneary; Lopunny in Gardenia |
| Pikipek | wild | 4 | Oxide | Peck, Growl | Echoed Voice 7, Rock Smash 9, Supersonic 13; as Trumbeak: Pluck 16 | Trumbeak (from 14); Toucannon in Fantina |
| Pikipek | wild | 4 | Rewrite | Peck, Pluck | Echoed Voice 7, Rock Smash 9, Scary Face 11, Supersonic 13 | Trumbeak (from 14); Toucannon in Fantina |
| Krabby | wild | 5 | Oxide | Mud Sport, Bubble, ViceGrip | Leer 9, Harden 11, BubbleBeam 15 | Krabby; Kingler in Fantina |
| Krabby | wild | 5 | Rewrite | Bubble, ViceGrip | Leer 9, Wide Guard 12, BubbleBeam 15 | Krabby; Kingler in Fantina |

## Oreburgh City

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 16 | At the cap |
|---|---|---|---|---|---|---|
| Vullaby | in-game trade | 1 | Oxide | Gust, Leer | Fury Attack 5, Pluck 11, Flatter 12 | Vullaby; Mandibuzz in Candice |
| Vullaby | in-game trade | 1 | Rewrite | Gust, Leer | Faint Attack 2, Scary Face 6, Pluck 11, Flatter 12, Mud Shot 16 | Vullaby; Mandibuzz in Candice |

## Oreburgh Gate

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 16 | At the cap |
|---|---|---|---|---|---|---|
| Zubat | wild | 5 to 6 | Oxide | Leech Life, Supersonic | Astonish 9, Bite 13 | Zubat; Golbat in Gardenia |
| Zubat | wild | 5 to 6 | Rewrite | Leech Life, Supersonic | Wing Attack 7, Astonish 9, Screech 11, Bite 13, Venoshock 16 | Zubat; Golbat in Gardenia |
| Makuhita | wild | 6 to 7 | Oxide | Tackle, Focus Energy, Sand-Attack | Arm Thrust 7, Vital Throw 10, Fake Out 13, Whirlwind 16 | Makuhita; Hariyama in Gardenia |
| Makuhita | wild | 6 to 7 | Rewrite | Focus Energy, Sand-Attack, Bulk Up, Bullet Punch | Arm Thrust 7, Vital Throw 10, Fake Out 13, Whirlwind 16 | Makuhita; Hariyama in Gardenia |
| Nacli | wild | 6 | Oxide | Tackle, Harden, Rock Throw | Mud Shot 7, Smack Down 10, Rock Polish 13, Headbutt 16 | Nacli; Naclstack in Gardenia |
| Nacli | wild | 6 | Rewrite | Tackle, Rock Throw | Mud Shot 7, Smack Down 10, Headbutt 16 | Nacli; Naclstack in Gardenia |
| Nosepass | wild | 6 to 7 | Oxide | Tackle | Harden 7, Rock Throw 13 | Nosepass; Probopass in Fantina |
| Nosepass | wild | 6 to 7 | Rewrite | Tackle, Iron Defense | Smack Down 9, Rock Throw 13, Rock Tomb 16 | Nosepass; Probopass in Fantina |
| Nidoran♂ | wild | 7 | Oxide | Leer, Peck, Focus Energy | Double Kick 9, Poison Sting 13 | Nidorino (from 16); Nidoking in Gardenia |
| Nidoran♂ | wild | 7 | Rewrite | Leer, Peck, Venoshock, Focus Energy | Double Kick 9, Poison Sting 13, Toxic Spikes 16 | Nidorino (from 16); Nidoking in Gardenia |
| Onix | wild | 7 | Oxide | Tackle, Harden, Bind, Screech | Rock Throw 9, Rage 14 | Onix; Steelix in Gardenia |
| Onix | wild | 7 | Rewrite | Tackle, Screech | Rock Throw 9, Rock Tomb 11, Bulldoze 13 | Onix; Steelix in Gardenia |
| Purrloin | wild | 7 to 8 | Oxide | Scratch, Growl, Sand-Attack, Assist | Fake Out 12, Fury Swipes 12, Pursuit 15 | Purrloin; Liepard in Gardenia |
| Purrloin | wild | 7 to 8 | Rewrite | Scratch, Taunt, Sand-Attack | Snarl 9, Fury Swipes 11, Fake Out 12, Pursuit 15 | Purrloin; Liepard in Gardenia |
| Gligar | wild | 8 | Oxide | Poison Sting, Sand-Attack | Harden 9, Knock Off 12, Quick Attack 16 | Gligar; Gliscor in Wake |
| Gligar | wild | 8 | Rewrite | Poison Sting, Sand-Attack | Harden 9, Sand Tomb 10, Rock Polish 11, Knock Off 12, Acrobatics 14, Quick Attack 16 | Gligar; Gliscor in Wake |

## Oreburgh Mine

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 16 | At the cap |
|---|---|---|---|---|---|---|
| Makuhita | wild | 5 to 7 | Oxide | Tackle, Focus Energy, Sand-Attack | Arm Thrust 7, Vital Throw 10, Fake Out 13, Whirlwind 16 | Makuhita; Hariyama in Gardenia |
| Makuhita | wild | 5 to 7 | Rewrite | Tackle, Focus Energy, Sand-Attack, Bulk Up | Bullet Punch 6, Arm Thrust 7, Vital Throw 10, Fake Out 13, Whirlwind 16 | Makuhita; Hariyama in Gardenia |
| Geodude | wild | 6 to 7 | Oxide | Tackle, Defense Curl, Mud Sport | Rock Polish 8, Rock Throw 11, Magnitude 15 | Geodude; Graveler in Gardenia |
| Geodude | wild | 6 to 7 | Rewrite | Tackle, Smack Down | Rock Throw 11, Bulldoze 12, Magnitude 15 | Geodude; Graveler in Gardenia |
| Nacli | wild | 6 to 8 | Oxide | Tackle, Harden, Rock Throw | Mud Shot 7, Smack Down 10, Rock Polish 13, Headbutt 16 | Nacli; Naclstack in Gardenia |
| Nacli | wild | 6 to 8 | Rewrite | Tackle, Rock Throw | Mud Shot 7, Smack Down 10, Headbutt 16 | Nacli; Naclstack in Gardenia |
| Onix | wild | 6 | Oxide | Tackle, Harden, Bind, Screech | Rock Throw 9, Rage 14 | Onix; Steelix in Gardenia |
| Onix | wild | 6 | Rewrite | Tackle, Screech | Rock Throw 9, Rock Tomb 11, Bulldoze 13 | Onix; Steelix in Gardenia |
| Phanpy | wild | 6 to 7 | Oxide | Tackle, Growl, Defense Curl, Flail | Take Down 10, Rollout 15 | Phanpy; Donphan in Gardenia |
| Phanpy | wild | 6 to 7 | Rewrite | Odor Sleuth, Tackle, Flail | Knock Off 9, Take Down 10, Bulldoze 14, Rollout 15 | Phanpy; Donphan in Gardenia |
| Zubat | wild | 6 | Oxide | Leech Life, Supersonic | Astonish 9, Bite 13 | Zubat; Golbat in Gardenia |
| Zubat | wild | 6 | Rewrite | Leech Life, Supersonic | Wing Attack 7, Astonish 9, Screech 11, Bite 13, Venoshock 16 | Zubat; Golbat in Gardenia |
| Nosepass | wild | 7 | Oxide | Tackle, Harden | Rock Throw 13 | Nosepass; Probopass in Fantina |
| Nosepass | wild | 7 | Rewrite | Tackle, Iron Defense | Smack Down 9, Rock Throw 13, Rock Tomb 16 | Nosepass; Probopass in Fantina |
| Rhyhorn | wild | 7 | Oxide | Horn Attack, Tail Whip | Stomp 9, Fury Attack 13 | Rhyhorn; Rhydon in Wake |
| Rhyhorn | wild | 7 | Rewrite | Horn Attack, Tail Whip | Stomp 9, Bulldoze 10, Peck 13, Smack Down 16 | Rhyhorn; Rhydon in Wake |
| Magby | wild | 8 | Oxide | Smog, Leer, Ember | SmokeScreen 10, Faint Attack 16 | Magby; Magmar in Fantina |
| Magby | wild | 8 | Rewrite | Smog, Ember | SmokeScreen 10, Scary Face 12, Flame Wheel 15, Faint Attack 16 | Magby; Magmar in Fantina |

## Ravaged Path

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 16 | At the cap |
|---|---|---|---|---|---|---|
| Zubat | wild | 3 to 4 | Oxide | Leech Life | Supersonic 5, Astonish 9, Bite 13 | Zubat; Golbat in Gardenia |
| Zubat | wild | 3 to 4 | Rewrite | Leech Life | Supersonic 5, Wing Attack 7, Astonish 9, Screech 11, Bite 13, Venoshock 16 | Zubat; Golbat in Gardenia |
| Geodude | wild | 4 | Oxide | Tackle, Defense Curl, Mud Sport | Rock Polish 8, Rock Throw 11, Magnitude 15 | Geodude; Graveler in Gardenia |
| Geodude | wild | 4 | Rewrite | Tackle | Smack Down 5, Rock Throw 11, Bulldoze 12, Magnitude 15 | Geodude; Graveler in Gardenia |
| Makuhita | wild | 4 | Oxide | Tackle, Focus Energy, Sand-Attack | Arm Thrust 7, Vital Throw 10, Fake Out 13, Whirlwind 16 | Makuhita; Hariyama in Gardenia |
| Makuhita | wild | 4 | Rewrite | Tackle, Focus Energy, Sand-Attack | Bulk Up 5, Bullet Punch 6, Arm Thrust 7, Vital Throw 10, Fake Out 13, Whirlwind 16 | Makuhita; Hariyama in Gardenia |
| Nacli | wild | 4 to 5 | Oxide | Tackle, Harden | Rock Throw 5, Mud Shot 7, Smack Down 10, Rock Polish 13, Headbutt 16 | Nacli; Naclstack in Gardenia |
| Nacli | wild | 4 to 5 | Rewrite | Tackle | Rock Throw 5, Mud Shot 7, Smack Down 10, Headbutt 16 | Nacli; Naclstack in Gardenia |
| Nosepass | wild | 4 to 5 | Oxide | Tackle | Harden 7, Rock Throw 13 | Nosepass; Probopass in Fantina |
| Nosepass | wild | 4 to 5 | Rewrite | Tackle | Iron Defense 6, Smack Down 9, Rock Throw 13, Rock Tomb 16 | Nosepass; Probopass in Fantina |
| Phanpy | wild | 4 to 5 | Oxide | Odor Sleuth, Tackle, Growl, Defense Curl | Flail 6, Take Down 10, Rollout 15 | Phanpy; Donphan in Gardenia |
| Phanpy | wild | 4 to 5 | Rewrite | Odor Sleuth, Tackle | Flail 6, Knock Off 9, Take Down 10, Bulldoze 14, Rollout 15 | Phanpy; Donphan in Gardenia |
| Barboach | old rod | 5 | Oxide | Mud-Slap | Mud Sport 6, Water Sport 6, Water Gun 10, Mud Bomb 14 | Barboach; Whiscash in Fantina |
| Barboach | old rod | 5 | Rewrite | Mud-Slap, Scary Face | Water Sport 6, Water Gun 10, Mud Bomb 14 | Barboach; Whiscash in Fantina |
| Corphish | old rod | 5 | Oxide | Bubble | Harden 7, ViceGrip 10, Leer 13 | Corphish; Crawdaunt in Fantina |
| Corphish | old rod | 5 | Rewrite | Bubble | Taunt 8, ViceGrip 10, BubbleBeam 12, Leer 13 | Corphish; Crawdaunt in Fantina |
| Goldeen | old rod | 5 | Oxide | Peck, Tail Whip, Water Sport | Supersonic 7, Horn Attack 11 | Goldeen; Seaking in Fantina |
| Goldeen | old rod | 5 | Rewrite | Peck, Water Sport, Flip Turn | Water Pulse 10, Horn Attack 11 | Goldeen; Seaking in Fantina |
| Lotad | wild | 5 to 6 | Oxide | Astonish, Growl, Absorb | Nature Power 7, Mist 11; as Lombre: Fury Swipes 15 | Lombre (from 14); Ludicolo in Maylene |
| Lotad | wild | 5 to 6 | Rewrite | Astonish, Magical Leaf | Water Gun 6, Mist 11, Disarming Voice 14; as Lombre: Fake Out 14, Fury Swipes 15, Natural Gift 16 | Lombre (from 14); Ludicolo in Maylene |
| Mudkip | old rod | 5 | Oxide | Tackle, Growl | Mud-Slap 6, Water Gun 10, Bide 15; as Marshtomp: Mud Shot 16 | Marshtomp (from 16); Swampert in Maylene |
| Mudkip | old rod | 5 | Rewrite | Tackle | Mud-Slap 6, Water Gun 10, Screech 13, Water Pulse 16; as Marshtomp: Mud Shot 16 | Marshtomp (from 16); Swampert in Maylene |
| Onix | wild | 5 to 6 | Oxide | Mud Sport, Tackle, Harden, Bind | Screech 6, Rock Throw 9, Rage 14 | Onix; Steelix in Gardenia |
| Onix | wild | 5 to 6 | Rewrite | Tackle | Screech 6, Rock Throw 9, Rock Tomb 11, Bulldoze 13 | Onix; Steelix in Gardenia |
| Wooper | old rod | 5 | Oxide | Water Gun, Tail Whip, Mud Sport | Mud Shot 9, Slam 15 | Wooper; Quagsire in Gardenia |
| Wooper | old rod | 5 | Oxide | Water Gun, Tail Whip, Mud Sport | as Clodsire: Mud Shot 8, Poison Tail 12, Slam 16 | Clodsire (from 5) |
| Wooper | old rod | 5 | Rewrite | Water Gun, Tail Whip, Poison Sting | Mud Shot 9, Slam 15 | Wooper; Quagsire in Gardenia |
| Wooper | old rod | 5 | Rewrite | Water Gun, Tail Whip, Poison Sting | as Clodsire: Mud Shot 8, Poison Tail 12, Slam 16 | Clodsire (from 5) |

## Route 201

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 16 | At the cap |
|---|---|---|---|---|---|---|
| Wooloo | wild | 2 | Oxide | Tackle, Growl | Defense Curl 4, Copycat 8, Guard Split 12, Double Kick 16 | Wooloo; Dubwool in Gardenia |
| Wooloo | wild | 2 | Rewrite | Tackle | Round 3, Guard Split 12, Double Kick 16 | Wooloo; Dubwool in Gardenia |
| Blipbug | wild | 3 | Oxide | Struggle Bug | as Dottler: Reflect 10, Light Screen 10, Confusion 10 | Dottler (from 10); Orbeetle in Fantina |
| Blipbug | wild | 3 | Rewrite | Struggle Bug | Calm Mind 4, Trailblaze 10; as Dottler: Reflect 10, Confusion 11, Light Screen 12 | Dottler (from 10); Orbeetle in Fantina |
| Kricketot | wild | 3 | Oxide | Growl, Bide | as Kricketune: Fury Cutter 10, Leech Life 14 | Kricketune (from 10) |
| Kricketot | wild | 3 | Rewrite | Growl, Fell Stinger | Struggle Bug 6, Screech 10; as Kricketune: Fury Cutter 10, Leech Life 14, Bug Bite 16 | Kricketune (from 10) |
| Purrloin | wild | 3 to 4 | Oxide | Scratch, Growl | Sand-Attack 6, Assist 6, Fake Out 12, Fury Swipes 12, Pursuit 15 | Purrloin; Liepard in Gardenia |
| Purrloin | wild | 3 to 4 | Rewrite | Scratch | Taunt 4, Sand-Attack 6, Snarl 9, Fury Swipes 11, Fake Out 12, Pursuit 15 | Purrloin; Liepard in Gardenia |
| Rookidee | wild | 3 to 4 | Oxide | Peck, Leer | Fury Attack 4, Sand-Attack 12, Pluck 15 | Corvisquire (from 16); Corviknight in Wake |
| Rookidee | wild | 3 to 4 | Rewrite | Peck, Leer | Taunt 4, Sand-Attack 12, Pluck 15 | Corvisquire (from 16); Corviknight in Wake |
| Sentret | wild | 3 | Oxide | Scratch, Foresight | Defense Curl 4, Quick Attack 7, Fury Swipes 13 | Furret (from 15) |
| Sentret | wild | 3 | Rewrite | Scratch, Foresight | Defense Curl 4, Baby-Doll Eyes 5, Pursuit 6, Quick Attack 7, Covet 10, Fury Swipes 13; as Furret: Helping Hand 16 | Furret (from 15) |
| Starly | wild | 3 | Oxide | Tackle, Growl | Quick Attack 5, Wing Attack 9, Double Team 13 | Staravia (from 14); Staraptor in Maylene |
| Starly | wild | 3 | Rewrite | Tackle, Tailwind | Quick Attack 5, Wing Attack 9, Pursuit 14 | Staravia (from 14); Staraptor in Maylene |
| Grubbin | wild | 4 | both | ViceGrip, Mud-Slap | String Shot 5, Bug Bite 10, Bite 15 | Grubbin; Charjabug in Gardenia |
| Nidoran♀ | wild | 4 | Oxide | Growl, Scratch | Tail Whip 7, Double Kick 9, Poison Sting 13 | Nidorina (from 16); Nidoqueen in Gardenia |
| Nidoran♀ | wild | 4 | Rewrite | Scratch | Sludge 5, Pursuit 7, Double Kick 9, Poison Sting 13, Toxic Spikes 16 | Nidorina (from 16); Nidoqueen in Gardenia |
| Nidoran♂ | wild | 4 | Oxide | Leer, Peck | Focus Energy 7, Double Kick 9, Poison Sting 13 | Nidorino (from 16); Nidoking in Gardenia |
| Nidoran♂ | wild | 4 | Rewrite | Leer, Peck | Venoshock 5, Focus Energy 7, Double Kick 9, Poison Sting 13, Toxic Spikes 16 | Nidorino (from 16); Nidoking in Gardenia |
| Shinx | wild | 4 | Oxide | Tackle | Leer 5, Charge 9, Spark 13 | Luxio (from 15); Luxray in Fantina |
| Shinx | wild | 4 | Rewrite | Tackle, Scary Face | Pursuit 6, Charge 9, Spark 13 | Luxio (from 15); Luxray in Fantina |
| Fletchling | wild | 5 | Oxide | Tackle, Growl | Quick Attack 6, Aerial Ace 12 | Fletchinder (from 16); Talonflame in Maylene |
| Fletchling | wild | 5 | Rewrite | Tackle | Quick Attack 6, Ember 10, Aerial Ace 12, Tailwind 16 | Fletchinder (from 16); Talonflame in Maylene |
| Pachirisu | wild | 5 | Oxide | Growl, Bide, Quick Attack | Charm 9, Spark 13 | Pachirisu |
| Pachirisu | wild | 5 | Rewrite | Growl, Quick Attack | Electroweb 7, Charm 9, Spark 13 | Pachirisu |
| Piplup | starter | 5 | Oxide | Pound, Growl | Bubble 8, Water Sport 11, Peck 15; as Prinplup: Metal Claw 16 | Prinplup (from 16); Empoleon in Maylene |
| Piplup | starter | 5 | Rewrite | Pound | Scary Face 6, Bubble 8, BubbleBeam 11, Peck 15; as Prinplup: Metal Claw 16 | Prinplup (from 16); Empoleon in Maylene |
| Scorbunny | starter | 5 | Oxide | Ember, Growl | Quick Attack 6, Sand-Attack 11, Double Kick 14 | Raboot (from 16); Cinderace in Maylene |
| Scorbunny | starter | 5 | Rewrite | Ember, Growl | Quick Attack 6, Flame Charge 8, Sand-Attack 11, Double Kick 14, Taunt 16 | Raboot (from 16); Cinderace in Maylene |
| Turtwig | starter | 5 | Oxide | Tackle, Withdraw | Absorb 9, Razor Leaf 13 | Turtwig; Grotle in Gardenia |
| Turtwig | starter | 5 | Rewrite | Tackle | Curse 6, Trailblaze 9, Razor Leaf 13, Giga Drain 16 | Turtwig; Grotle in Gardenia |

## Route 202

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 16 | At the cap |
|---|---|---|---|---|---|---|
| Shinx | wild | 2 | Oxide | Tackle | Leer 5, Charge 9, Spark 13 | Luxio (from 15); Luxray in Fantina |
| Shinx | wild | 2 | Rewrite | Tackle | Scary Face 3, Pursuit 6, Charge 9, Spark 13 | Luxio (from 15); Luxray in Fantina |
| Bidoof | wild | 3 | Oxide | Tackle | Growl 5, Defense Curl 9, Rollout 13; as Bibarel: Water Gun 15 | Bibarel (from 15) |
| Bidoof | wild | 3 | Rewrite | Tackle | Taunt 4, Aqua Jet 6, Swift 8, Rollout 13; as Bibarel: Water Gun 15 | Bibarel (from 15) |
| Blipbug | wild | 3 | Oxide | Struggle Bug | as Dottler: Reflect 10, Light Screen 10, Confusion 10 | Dottler (from 10); Orbeetle in Fantina |
| Blipbug | wild | 3 | Rewrite | Struggle Bug | Calm Mind 4, Trailblaze 10; as Dottler: Reflect 10, Confusion 11, Light Screen 12 | Dottler (from 10); Orbeetle in Fantina |
| Kricketot | wild | 3 | Oxide | Growl, Bide | as Kricketune: Fury Cutter 10, Leech Life 14 | Kricketune (from 10) |
| Kricketot | wild | 3 | Rewrite | Growl, Fell Stinger | Struggle Bug 6, Screech 10; as Kricketune: Fury Cutter 10, Leech Life 14, Bug Bite 16 | Kricketune (from 10) |
| Pikipek | wild | 3 | Oxide | Peck, Growl | Echoed Voice 7, Rock Smash 9, Supersonic 13; as Trumbeak: Pluck 16 | Trumbeak (from 14); Toucannon in Fantina |
| Pikipek | wild | 3 | Rewrite | Peck | Pluck 4, Echoed Voice 7, Rock Smash 9, Scary Face 11, Supersonic 13 | Trumbeak (from 14); Toucannon in Fantina |
| Purrloin | wild | 3 to 4 | Oxide | Scratch, Growl | Sand-Attack 6, Assist 6, Fake Out 12, Fury Swipes 12, Pursuit 15 | Purrloin; Liepard in Gardenia |
| Purrloin | wild | 3 to 4 | Rewrite | Scratch | Taunt 4, Sand-Attack 6, Snarl 9, Fury Swipes 11, Fake Out 12, Pursuit 15 | Purrloin; Liepard in Gardenia |
| Sewaddle | wild | 3 | Oxide | Tackle, String Shot | Bug Bite 8, Razor Leaf 12 | Sewaddle; Swadloon in Gardenia |
| Sewaddle | wild | 3 | Rewrite | Tackle | Sticky Web 4, Bug Bite 8, Razor Leaf 12, Pounce 16 | Sewaddle; Swadloon in Gardenia |
| Wooloo | wild | 3 | Oxide | Tackle, Growl | Defense Curl 4, Copycat 8, Guard Split 12, Double Kick 16 | Wooloo; Dubwool in Gardenia |
| Wooloo | wild | 3 | Rewrite | Tackle, Round | Guard Split 12, Double Kick 16 | Wooloo; Dubwool in Gardenia |
| Grubbin | wild | 4 | both | ViceGrip, Mud-Slap | String Shot 5, Bug Bite 10, Bite 15 | Grubbin; Charjabug in Gardenia |
| Nidoran♀ | wild | 4 | Oxide | Growl, Scratch | Tail Whip 7, Double Kick 9, Poison Sting 13 | Nidorina (from 16); Nidoqueen in Gardenia |
| Nidoran♀ | wild | 4 | Rewrite | Scratch | Sludge 5, Pursuit 7, Double Kick 9, Poison Sting 13, Toxic Spikes 16 | Nidorina (from 16); Nidoqueen in Gardenia |
| Nidoran♂ | wild | 4 | Oxide | Leer, Peck | Focus Energy 7, Double Kick 9, Poison Sting 13 | Nidorino (from 16); Nidoking in Gardenia |
| Nidoran♂ | wild | 4 | Rewrite | Leer, Peck | Venoshock 5, Focus Energy 7, Double Kick 9, Poison Sting 13, Toxic Spikes 16 | Nidorino (from 16); Nidoking in Gardenia |
| Rookidee | wild | 4 | Oxide | Peck, Leer, Fury Attack | Sand-Attack 12, Pluck 15 | Corvisquire (from 16); Corviknight in Wake |
| Rookidee | wild | 4 | Rewrite | Peck, Leer, Taunt | Sand-Attack 12, Pluck 15 | Corvisquire (from 16); Corviknight in Wake |
| Starly | wild | 4 | Oxide | Tackle, Growl | Quick Attack 5, Wing Attack 9, Double Team 13 | Staravia (from 14); Staraptor in Maylene |
| Starly | wild | 4 | Rewrite | Tackle, Tailwind | Quick Attack 5, Wing Attack 9, Pursuit 14 | Staravia (from 14); Staraptor in Maylene |
| Budew | wild | 5 | Oxide | Absorb, Growth | Water Sport 7, Stun Spore 10, Mega Drain 13, Worry Seed 16 | Budew; Roselia in Fantina |
| Budew | wild | 5 | Rewrite | Razor Leaf, Acid | Water Sport 7, Stun Spore 10, Mega Drain 13, Magical Leaf 15, Worry Seed 16 | Budew; Roselia in Fantina |
| Smoliv | wild | 5 | Oxide | Tackle, Sweet Scent, Absorb | Growth 7, Razor Leaf 10, Helping Hand 13, Flail 16 | Smoliv; Dolliv in Gardenia |
| Smoliv | wild | 5 | Rewrite | Tackle | Terrain Pulse 6, Razor Leaf 10, Helping Hand 13, Flail 16 | Smoliv; Dolliv in Gardenia |

## Route 203

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 16 | At the cap |
|---|---|---|---|---|---|---|
| Barboach | old rod | 4 | Oxide | Mud-Slap | Mud Sport 6, Water Sport 6, Water Gun 10, Mud Bomb 14 | Barboach; Whiscash in Fantina |
| Barboach | old rod | 4 | Rewrite | Mud-Slap, Scary Face | Water Sport 6, Water Gun 10, Mud Bomb 14 | Barboach; Whiscash in Fantina |
| Corphish | old rod | 4 | Oxide | Bubble | Harden 7, ViceGrip 10, Leer 13 | Corphish; Crawdaunt in Fantina |
| Corphish | old rod | 4 | Rewrite | Bubble | Taunt 8, ViceGrip 10, BubbleBeam 12, Leer 13 | Corphish; Crawdaunt in Fantina |
| Froakie | old rod | 4 | Oxide | Pound | Water Gun 5, Growl 7, Quick Attack 10, Lick 13, Water Pulse 14, Icy Wind 16; as Frogadier: Icy Wind 16 | Frogadier (from 16); Greninja in Maylene |
| Froakie | old rod | 4 | Rewrite | Pound | Water Gun 5, Quick Attack 10, Lick 13, Water Pulse 14, Icy Wind 16; as Frogadier: Icy Wind 16 | Frogadier (from 16); Greninja in Maylene |
| Poliwag | old rod | 4 | Oxide | Water Sport | Bubble 5, Hypnosis 8, Water Gun 11, DoubleSlap 15 | Poliwag; Poliwhirl in Gardenia |
| Poliwag | old rod | 4 | Rewrite | Water Sport, Water Gun | Bubble 5, Water Pulse 6, Hypnosis 8, Mud Shot 12, DoubleSlap 15 | Poliwag; Poliwhirl in Gardenia |
| Rookidee | wild | 4 | Oxide | Peck, Leer, Fury Attack | Sand-Attack 12, Pluck 15 | Corvisquire (from 16); Corviknight in Wake |
| Rookidee | wild | 4 | Rewrite | Peck, Leer, Taunt | Sand-Attack 12, Pluck 15 | Corvisquire (from 16); Corviknight in Wake |
| Wooper | old rod | 4 | Oxide | Water Gun, Tail Whip | Mud Sport 5, Mud Shot 9, Slam 15 | Wooper; Quagsire in Gardenia |
| Wooper | old rod | 4 | Oxide | Water Gun, Tail Whip | as Clodsire: Mud Shot 8, Poison Tail 12, Slam 16 | Clodsire (from 4) |
| Wooper | old rod | 4 | Rewrite | Water Gun, Tail Whip | Poison Sting 5, Mud Shot 9, Slam 15 | Wooper; Quagsire in Gardenia |
| Wooper | old rod | 4 | Rewrite | Water Gun, Tail Whip | as Clodsire: Mud Shot 8, Poison Tail 12, Slam 16 | Clodsire (from 4) |
| Fletchling | wild | 5 to 7 | Oxide | Tackle, Growl | Quick Attack 6, Aerial Ace 12 | Fletchinder (from 16); Talonflame in Maylene |
| Fletchling | wild | 5 to 7 | Rewrite | Tackle | Quick Attack 6, Ember 10, Aerial Ace 12, Tailwind 16 | Fletchinder (from 16); Talonflame in Maylene |
| Grubbin | wild | 5 | both | ViceGrip, Mud-Slap, String Shot | Bug Bite 10, Bite 15 | Grubbin; Charjabug in Gardenia |
| Nidoran♀ | wild | 5 | Oxide | Growl, Scratch | Tail Whip 7, Double Kick 9, Poison Sting 13 | Nidorina (from 16); Nidoqueen in Gardenia |
| Nidoran♀ | wild | 5 | Rewrite | Scratch, Sludge | Pursuit 7, Double Kick 9, Poison Sting 13, Toxic Spikes 16 | Nidorina (from 16); Nidoqueen in Gardenia |
| Nidoran♂ | wild | 5 | Oxide | Leer, Peck | Focus Energy 7, Double Kick 9, Poison Sting 13 | Nidorino (from 16); Nidoking in Gardenia |
| Nidoran♂ | wild | 5 | Rewrite | Leer, Peck, Venoshock | Focus Energy 7, Double Kick 9, Poison Sting 13, Toxic Spikes 16 | Nidorino (from 16); Nidoking in Gardenia |
| Purrloin | wild | 5 to 6 | Oxide | Scratch, Growl | Sand-Attack 6, Assist 6, Fake Out 12, Fury Swipes 12, Pursuit 15 | Purrloin; Liepard in Gardenia |
| Purrloin | wild | 5 to 6 | Rewrite | Scratch, Taunt | Sand-Attack 6, Snarl 9, Fury Swipes 11, Fake Out 12, Pursuit 15 | Purrloin; Liepard in Gardenia |
| Abra | wild | 6 to 7 | Oxide | Teleport | as Kadabra: Confusion 16 | Kadabra (from 16); Alakazam in Wake |
| Abra | wild | 6 to 7 | Rewrite | Psycho Cut, Confusion | Role Play 7, Reflect 10, Disable 13, Calm Mind 16 | Kadabra (from 16); Alakazam in Wake |
| Makuhita | wild | 6 | Oxide | Tackle, Focus Energy, Sand-Attack | Arm Thrust 7, Vital Throw 10, Fake Out 13, Whirlwind 16 | Makuhita; Hariyama in Gardenia |
| Makuhita | wild | 6 | Rewrite | Focus Energy, Sand-Attack, Bulk Up, Bullet Punch | Arm Thrust 7, Vital Throw 10, Fake Out 13, Whirlwind 16 | Makuhita; Hariyama in Gardenia |
| Shinx | wild | 6 | Oxide | Tackle, Leer | Charge 9, Spark 13 | Luxio (from 15); Luxray in Fantina |
| Shinx | wild | 6 | Rewrite | Tackle, Scary Face, Pursuit | Charge 9, Spark 13 | Luxio (from 15); Luxray in Fantina |

## Route 204

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 16 | At the cap |
|---|---|---|---|---|---|---|
| Budew | wild | 3 | Oxide | Absorb | Growth 4, Water Sport 7, Stun Spore 10, Mega Drain 13, Worry Seed 16 | Budew; Roselia in Fantina |
| Budew | wild | 3 | Rewrite | Razor Leaf | Acid 4, Water Sport 7, Stun Spore 10, Mega Drain 13, Magical Leaf 15, Worry Seed 16 | Budew; Roselia in Fantina |
| Bounsweet | wild | 4 to 5 | Oxide | Splash | Play Nice 5, Rapid Spin 9, Razor Leaf 12; as Steenee: Razor Leaf 12 | Steenee (from 12); Tsareena in Fantina |
| Bounsweet | wild | 4 to 5 | Rewrite | Grassy Glide | Trailblaze 5, Magical Leaf 6, Taunt 7, Play Nice 8, Rapid Spin 9, Razor Leaf 12; as Steenee: Razor Leaf 12 | Steenee (from 12); Tsareena in Fantina |
| Fletchling | wild | 4 | Oxide | Tackle, Growl | Quick Attack 6, Aerial Ace 12 | Fletchinder (from 16); Talonflame in Maylene |
| Fletchling | wild | 4 | Rewrite | Tackle | Quick Attack 6, Ember 10, Aerial Ace 12, Tailwind 16 | Fletchinder (from 16); Talonflame in Maylene |
| Grubbin | wild | 4 | both | ViceGrip, Mud-Slap | String Shot 5, Bug Bite 10, Bite 15 | Grubbin; Charjabug in Gardenia |
| Purrloin | wild | 4 | Oxide | Scratch, Growl | Sand-Attack 6, Assist 6, Fake Out 12, Fury Swipes 12, Pursuit 15 | Purrloin; Liepard in Gardenia |
| Purrloin | wild | 4 | Rewrite | Scratch, Taunt | Sand-Attack 6, Snarl 9, Fury Swipes 11, Fake Out 12, Pursuit 15 | Purrloin; Liepard in Gardenia |
| Seedot | wild | 4 to 5 | Oxide | Bide, Harden | Growth 7, Nature Power 13 | Nuzleaf (from 14); Shiftry in Gardenia |
| Seedot | wild | 4 to 5 | Rewrite | Harden, Razor Leaf | Fake Out 5, Scary Face 8, Trailblaze 11, Giga Drain 14; as Nuzleaf: Payback 14, Chilling Water 16 | Nuzleaf (from 14); Shiftry in Gardenia |
| Sewaddle | wild | 4 to 5 | Oxide | Tackle, String Shot | Bug Bite 8, Razor Leaf 12 | Sewaddle; Swadloon in Gardenia |
| Sewaddle | wild | 4 to 5 | Rewrite | Tackle, Sticky Web | Bug Bite 8, Razor Leaf 12, Pounce 16 | Sewaddle; Swadloon in Gardenia |
| Wurmple | wild | 4 | Oxide | Tackle, String Shot | Poison Sting 5; as Silcoon: Harden 7; as Beautifly: Absorb 10, Gust 13 | Beautifly (from 10) |
| Wurmple | wild | 4 | Oxide | Tackle, String Shot | Poison Sting 5; as Cascoon: Harden 7; as Dustox: Confusion 10, Gust 13 | Dustox (from 10) |
| Wurmple | wild | 4 | Rewrite | Tackle | Poison Sting 5, Stun Spore 6; as Silcoon: Harden 7; as Beautifly: Twister 10, Gust 13, Bug Bite 15 | Beautifly (from 10) |
| Wurmple | wild | 4 | Rewrite | Tackle | Poison Sting 5, Stun Spore 6; as Cascoon: Harden 7; as Dustox: Confusion 10, Gust 13, Bug Bite 15 | Dustox (from 10) |
| Barboach | old rod | 5 | Oxide | Mud-Slap | Mud Sport 6, Water Sport 6, Water Gun 10, Mud Bomb 14 | Barboach; Whiscash in Fantina |
| Barboach | old rod | 5 | Rewrite | Mud-Slap, Scary Face | Water Sport 6, Water Gun 10, Mud Bomb 14 | Barboach; Whiscash in Fantina |
| Corphish | old rod | 5 | Oxide | Bubble | Harden 7, ViceGrip 10, Leer 13 | Corphish; Crawdaunt in Fantina |
| Corphish | old rod | 5 | Rewrite | Bubble | Taunt 8, ViceGrip 10, BubbleBeam 12, Leer 13 | Corphish; Crawdaunt in Fantina |
| Froakie | old rod | 5 | Oxide | Pound, Water Gun | Growl 7, Quick Attack 10, Lick 13, Water Pulse 14, Icy Wind 16; as Frogadier: Icy Wind 16 | Frogadier (from 16); Greninja in Maylene |
| Froakie | old rod | 5 | Rewrite | Pound, Water Gun | Quick Attack 10, Lick 13, Water Pulse 14, Icy Wind 16; as Frogadier: Icy Wind 16 | Frogadier (from 16); Greninja in Maylene |
| Goldeen | old rod | 5 | Oxide | Peck, Tail Whip, Water Sport | Supersonic 7, Horn Attack 11 | Goldeen; Seaking in Fantina |
| Goldeen | old rod | 5 | Rewrite | Peck, Water Sport, Flip Turn | Water Pulse 10, Horn Attack 11 | Goldeen; Seaking in Fantina |
| Lotad | old rod | 5 | Oxide | Astonish, Growl, Absorb | Nature Power 7, Mist 11; as Lombre: Fury Swipes 15 | Lombre (from 14); Ludicolo in Maylene |
| Lotad | old rod | 5 | Rewrite | Astonish, Magical Leaf | Water Gun 6, Mist 11, Disarming Voice 14; as Lombre: Fake Out 14, Fury Swipes 15, Natural Gift 16 | Lombre (from 14); Ludicolo in Maylene |
| Lotad | wild | 5 | Oxide | Astonish, Growl, Absorb | Nature Power 7, Mist 11; as Lombre: Fury Swipes 15 | Lombre (from 14); Ludicolo in Maylene |
| Lotad | wild | 5 | Rewrite | Astonish, Magical Leaf | Water Gun 6, Mist 11, Disarming Voice 14; as Lombre: Fake Out 14, Fury Swipes 15, Natural Gift 16 | Lombre (from 14); Ludicolo in Maylene |
| Shroomish | wild | 5 | Oxide | Absorb, Tackle | Stun Spore 9, Leech Seed 13 | Shroomish; Breloom in Gardenia |
| Shroomish | wild | 5 | Rewrite | Tackle | Magical Leaf 7, Stun Spore 9, Mach Punch 11, Leech Seed 13 | Shroomish; Breloom in Gardenia |
| Wooloo | wild | 5 | Oxide | Tackle, Growl, Defense Curl | Copycat 8, Guard Split 12, Double Kick 16 | Wooloo; Dubwool in Gardenia |
| Wooloo | wild | 5 | Rewrite | Tackle, Round | Guard Split 12, Double Kick 16 | Wooloo; Dubwool in Gardenia |
| Smoliv | wild | 6 | Oxide | Tackle, Sweet Scent, Absorb | Growth 7, Razor Leaf 10, Helping Hand 13, Flail 16 | Smoliv; Dolliv in Gardenia |
| Smoliv | wild | 6 | Rewrite | Tackle, Terrain Pulse | Razor Leaf 10, Helping Hand 13, Flail 16 | Smoliv; Dolliv in Gardenia |
| Snivy | wild | 6 | Oxide | Tackle, Vine Whip, Leer | Wrap 10, Hold Back 14 | Servine (from 16); Serperior in Maylene |
| Snivy | wild | 6 | Rewrite | Tackle, Vine Whip | Calm Mind 7, Twister 10, Hold Back 14, Magical Leaf 16 | Servine (from 16); Serperior in Maylene |

## Route 207

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 16 | At the cap |
|---|---|---|---|---|---|---|
| Ponyta | wild | 5 | Oxide | Growl, Tackle | Tail Whip 6, Ember 10, Flame Wheel 15 | Ponyta; Galarian Rapidash in Gardenia, Rapidash in Wake |
| Ponyta | wild | 5 | Rewrite | Tackle | Mystical Fire 6, Ember 10, Flame Charge 14, Flame Wheel 15 | Ponyta; Galarian Rapidash in Gardenia, Rapidash in Wake |
| Fletchling | wild | 6 to 7 | Oxide | Tackle, Growl, Quick Attack | Aerial Ace 12 | Fletchinder (from 16); Talonflame in Maylene |
| Fletchling | wild | 6 to 7 | Rewrite | Tackle, Quick Attack | Ember 10, Aerial Ace 12, Tailwind 16 | Fletchinder (from 16); Talonflame in Maylene |
| Houndour | wild | 6 to 7 | Oxide | Leer, Ember, Howl | Smog 9, Roar 14 | Houndour; Houndoom in Fantina |
| Houndour | wild | 6 to 7 | Rewrite | Ember, Howl | Scary Face 7, Smog 9, Roar 14, Bite 16 | Houndour; Houndoom in Fantina |
| Machop | wild | 6 | Oxide | Low Kick, Leer | Focus Energy 7, Karate Chop 10, Foresight 13 | Machop; Machoke in Fantina |
| Machop | wild | 6 | Rewrite | Low Kick, Leer, Scary Face | Focus Energy 7, Karate Chop 10, Foresight 13, Bullet Punch 16 | Machop; Machoke in Fantina |
| Nacli | wild | 6 | Oxide | Tackle, Harden, Rock Throw | Mud Shot 7, Smack Down 10, Rock Polish 13, Headbutt 16 | Nacli; Naclstack in Gardenia |
| Nacli | wild | 6 | Rewrite | Tackle, Rock Throw | Mud Shot 7, Smack Down 10, Headbutt 16 | Nacli; Naclstack in Gardenia |
| Smoliv | wild | 6 to 7 | Oxide | Tackle, Sweet Scent, Absorb | Growth 7, Razor Leaf 10, Helping Hand 13, Flail 16 | Smoliv; Dolliv in Gardenia |
| Smoliv | wild | 6 to 7 | Rewrite | Tackle, Terrain Pulse | Razor Leaf 10, Helping Hand 13, Flail 16 | Smoliv; Dolliv in Gardenia |
| Vulpix | wild | 6 | Oxide | Ember, Tail Whip | Roar 7, Quick Attack 11, Will-O-Wisp 14 | Vulpix; Ninetales in Maylene |
| Vulpix | wild | 6 | Rewrite | Ember, Tail Whip | Powder Snow 7, Quick Attack 11, Will-O-Wisp 14, Incinerate 16 | Vulpix; Ninetales in Maylene |
| Geodude | wild | 7 | Oxide | Tackle, Defense Curl, Mud Sport | Rock Polish 8, Rock Throw 11, Magnitude 15 | Geodude; Graveler in Gardenia |
| Geodude | wild | 7 | Rewrite | Tackle, Smack Down | Rock Throw 11, Bulldoze 12, Magnitude 15 | Geodude; Graveler in Gardenia |
| Makuhita | wild | 7 | Oxide | Tackle, Focus Energy, Sand-Attack, Arm Thrust | Vital Throw 10, Fake Out 13, Whirlwind 16 | Makuhita; Hariyama in Gardenia |
| Makuhita | wild | 7 | Rewrite | Sand-Attack, Bulk Up, Bullet Punch, Arm Thrust | Vital Throw 10, Fake Out 13, Whirlwind 16 | Makuhita; Hariyama in Gardenia |
| Phanpy | wild | 7 | Oxide | Tackle, Growl, Defense Curl, Flail | Take Down 10, Rollout 15 | Phanpy; Donphan in Gardenia |
| Phanpy | wild | 7 | Rewrite | Odor Sleuth, Tackle, Flail | Knock Off 9, Take Down 10, Bulldoze 14, Rollout 15 | Phanpy; Donphan in Gardenia |
| Charmander | wild | 8 | Oxide | Scratch, Growl, Ember | SmokeScreen 10, Dragon Rage 16 | Charmeleon (from 16); Charizard in Maylene |
| Charmander | wild | 8 | Rewrite | Scratch, Ember | Scary Face 9, Metal Claw 11, Flame Wheel 16 | Charmeleon (from 16); Charizard in Maylene |
| Fennekin | wild | 8 | Oxide | Scratch, Tail Whip, Ember | Role Play 9, Psybeam 13 | Braixen (from 16); Delphox in Maylene |
| Fennekin | wild | 8 | Rewrite | Scratch, Ember | Role Play 9, Psybeam 13, Flame Charge 14 | Braixen (from 16); Delphox in Maylene |

## Route 218

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 16 | At the cap |
|---|---|---|---|---|---|---|
| Corsola | old rod | 5 | Oxide | Tackle, Harden | Bubble 8, Recover 13, Refresh 16 | Corsola |
| Corsola | old rod | 5 | Rewrite | Tackle | Life Dew 6, Bubble 8, Recover 13, AncientPower 16 | Corsola |
| Finneon | old rod | 5 | Oxide | Pound | Water Gun 6, Attract 10 | Finneon; Lumineon in Fantina |
| Finneon | old rod | 5 | Rewrite | Pound | Water Gun 6, Tailwind 8, Attract 10, Water Pulse 13, Pursuit 15 | Finneon; Lumineon in Fantina |
| Krabby | old rod | 5 | Oxide | Mud Sport, Bubble, ViceGrip | Leer 9, Harden 11, BubbleBeam 15 | Krabby; Kingler in Fantina |
| Krabby | old rod | 5 | Rewrite | Bubble, ViceGrip | Leer 9, Wide Guard 12, BubbleBeam 15 | Krabby; Kingler in Fantina |
| Remoraid | old rod | 5 | Oxide | Water Gun | Lock-On 6, Psybeam 10, Aurora Beam 14 | Remoraid; Octillery in Gardenia |
| Remoraid | old rod | 5 | Rewrite | Water Gun | Lock-On 6, Water Pulse 8, Psybeam 10, Screech 12, Aurora Beam 14 | Remoraid; Octillery in Gardenia |
| Squirtle | old rod | 5 | Oxide | Tackle, Tail Whip | Bubble 7, Withdraw 10, Water Gun 13, Bite 16; as Wartortle: Bite 16 | Wartortle (from 16); Blastoise in Maylene |
| Squirtle | old rod | 5 | Rewrite | Tackle, Life Dew | Bubble 7, Water Gun 13, Water Pulse 15, Bite 16; as Wartortle: Bite 16 | Wartortle (from 16); Blastoise in Maylene |

## Route 219

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 16 | At the cap |
|---|---|---|---|---|---|---|
| Finneon | old rod | 4 | Oxide | Pound | Water Gun 6, Attract 10 | Finneon; Lumineon in Fantina |
| Finneon | old rod | 4 | Rewrite | Pound | Water Gun 6, Tailwind 8, Attract 10, Water Pulse 13, Pursuit 15 | Finneon; Lumineon in Fantina |
| Froakie | old rod | 4 | Oxide | Pound | Water Gun 5, Growl 7, Quick Attack 10, Lick 13, Water Pulse 14, Icy Wind 16; as Frogadier: Icy Wind 16 | Frogadier (from 16); Greninja in Maylene |
| Froakie | old rod | 4 | Rewrite | Pound | Water Gun 5, Quick Attack 10, Lick 13, Water Pulse 14, Icy Wind 16; as Frogadier: Icy Wind 16 | Frogadier (from 16); Greninja in Maylene |
| Luvdisc | old rod | 4 | Oxide | Tackle, Charm | Water Gun 7, Agility 9, Take Down 14 | Luvdisc; Alomomola in Fantina |
| Luvdisc | old rod | 4 | Rewrite | Tackle, Charm | Water Gun 7, Aqua Jet 8, Draining Kiss 11, Take Down 14 | Luvdisc; Alomomola in Fantina |
| Remoraid | old rod | 4 | Oxide | Water Gun | Lock-On 6, Psybeam 10, Aurora Beam 14 | Remoraid; Octillery in Gardenia |
| Remoraid | old rod | 4 | Rewrite | Water Gun | Lock-On 6, Water Pulse 8, Psybeam 10, Screech 12, Aurora Beam 14 | Remoraid; Octillery in Gardenia |
| Tentacool | old rod | 4 | Oxide | Poison Sting | Supersonic 5, Constrict 8, Acid 12, Toxic Spikes 15 | Tentacool; Tentacruel in Fantina |
| Tentacool | old rod | 4 | Rewrite | Poison Sting | Supersonic 5, Pounce 8, Acid 12, Toxic Spikes 15, Water Pulse 16 | Tentacool; Tentacruel in Fantina |

## Sandgem Town

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 16 | At the cap |
|---|---|---|---|---|---|---|
| Kricketot | wild | 3 to 4 | Oxide | Growl, Bide | as Kricketune: Fury Cutter 10, Leech Life 14 | Kricketune (from 10) |
| Kricketot | wild | 3 to 4 | Rewrite | Growl, Fell Stinger | Struggle Bug 6, Screech 10; as Kricketune: Fury Cutter 10, Leech Life 14, Bug Bite 16 | Kricketune (from 10) |
| Bidoof | wild | 4 | Oxide | Tackle | Growl 5, Defense Curl 9, Rollout 13; as Bibarel: Water Gun 15 | Bibarel (from 15) |
| Bidoof | wild | 4 | Rewrite | Tackle, Taunt | Aqua Jet 6, Swift 8, Rollout 13; as Bibarel: Water Gun 15 | Bibarel (from 15) |
| Pikipek | wild | 4 to 5 | Oxide | Peck, Growl | Echoed Voice 7, Rock Smash 9, Supersonic 13; as Trumbeak: Pluck 16 | Trumbeak (from 14); Toucannon in Fantina |
| Pikipek | wild | 4 to 5 | Rewrite | Peck, Pluck | Echoed Voice 7, Rock Smash 9, Scary Face 11, Supersonic 13 | Trumbeak (from 14); Toucannon in Fantina |
| Purrloin | wild | 4 | Oxide | Scratch, Growl | Sand-Attack 6, Assist 6, Fake Out 12, Fury Swipes 12, Pursuit 15 | Purrloin; Liepard in Gardenia |
| Purrloin | wild | 4 | Rewrite | Scratch, Taunt | Sand-Attack 6, Snarl 9, Fury Swipes 11, Fake Out 12, Pursuit 15 | Purrloin; Liepard in Gardenia |
| Starly | wild | 4 | Oxide | Tackle, Growl | Quick Attack 5, Wing Attack 9, Double Team 13 | Staravia (from 14); Staraptor in Maylene |
| Starly | wild | 4 | Rewrite | Tackle, Tailwind | Quick Attack 5, Wing Attack 9, Pursuit 14 | Staravia (from 14); Staraptor in Maylene |
| Wurmple | wild | 4 | Oxide | Tackle, String Shot | Poison Sting 5; as Silcoon: Harden 7; as Beautifly: Absorb 10, Gust 13 | Beautifly (from 10) |
| Wurmple | wild | 4 | Oxide | Tackle, String Shot | Poison Sting 5; as Cascoon: Harden 7; as Dustox: Confusion 10, Gust 13 | Dustox (from 10) |
| Wurmple | wild | 4 | Rewrite | Tackle | Poison Sting 5, Stun Spore 6; as Silcoon: Harden 7; as Beautifly: Twister 10, Gust 13, Bug Bite 15 | Beautifly (from 10) |
| Wurmple | wild | 4 | Rewrite | Tackle | Poison Sting 5, Stun Spore 6; as Cascoon: Harden 7; as Dustox: Confusion 10, Gust 13, Bug Bite 15 | Dustox (from 10) |
| Blipbug | wild | 5 | Oxide | Struggle Bug | as Dottler: Reflect 10, Light Screen 10, Confusion 10 | Dottler (from 10); Orbeetle in Fantina |
| Blipbug | wild | 5 | Rewrite | Struggle Bug, Calm Mind | Trailblaze 10; as Dottler: Reflect 10, Confusion 11, Light Screen 12 | Dottler (from 10); Orbeetle in Fantina |
| Rookidee | wild | 5 | Oxide | Peck, Leer, Fury Attack | Sand-Attack 12, Pluck 15 | Corvisquire (from 16); Corviknight in Wake |
| Rookidee | wild | 5 | Rewrite | Peck, Leer, Taunt | Sand-Attack 12, Pluck 15 | Corvisquire (from 16); Corviknight in Wake |
| Sentret | wild | 5 | Oxide | Scratch, Foresight, Defense Curl | Quick Attack 7, Fury Swipes 13 | Furret (from 15) |
| Sentret | wild | 5 | Rewrite | Scratch, Foresight, Defense Curl, Baby-Doll Eyes | Pursuit 6, Quick Attack 7, Covet 10, Fury Swipes 13; as Furret: Helping Hand 16 | Furret (from 15) |
| Wingull | wild | 5 | Oxide | Growl, Water Gun | Supersonic 6, Wing Attack 11, Mist 16 | Wingull; Pelipper in Gardenia |
| Wingull | wild | 5 | Rewrite | Water Gun | Supersonic 6, Twister 8, Wing Attack 11, Tailwind 15 | Wingull; Pelipper in Gardenia |
| Wooloo | wild | 5 | Oxide | Tackle, Growl, Defense Curl | Copycat 8, Guard Split 12, Double Kick 16 | Wooloo; Dubwool in Gardenia |
| Wooloo | wild | 5 | Rewrite | Tackle, Round | Guard Split 12, Double Kick 16 | Wooloo; Dubwool in Gardenia |
| Abra | wild | 6 | Oxide | Teleport | as Kadabra: Confusion 16 | Kadabra (from 16); Alakazam in Wake |
| Abra | wild | 6 | Rewrite | Psycho Cut, Confusion | Role Play 7, Reflect 10, Disable 13, Calm Mind 16 | Kadabra (from 16); Alakazam in Wake |
| Poochyena | wild | 6 | Oxide | Tackle, Howl | Sand-Attack 9, Bite 13 | Poochyena; Mightyena in Gardenia |
| Poochyena | wild | 6 | Rewrite | Tackle, Howl | Scary Face 7, Sand-Attack 9, Bite 13 | Poochyena; Mightyena in Gardenia |

## Twinleaf Town

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 16 | At the cap |
|---|---|---|---|---|---|---|
| Barboach | old rod | 3 | Oxide | Mud-Slap | Mud Sport 6, Water Sport 6, Water Gun 10, Mud Bomb 14 | Barboach; Whiscash in Fantina |
| Barboach | old rod | 3 | Rewrite | Mud-Slap | Scary Face 4, Water Sport 6, Water Gun 10, Mud Bomb 14 | Barboach; Whiscash in Fantina |
| Buizel | old rod | 3 | Oxide | SonicBoom, Growl, Water Sport, Quick Attack | Water Gun 6, Pursuit 10, Swift 15 | Buizel; Floatzel in Gardenia |
| Buizel | old rod | 3 | Rewrite | SonicBoom, Water Sport, Quick Attack | Water Gun 6, BubbleBeam 8, Pursuit 10, Scary Face 12, Swift 15 | Buizel; Floatzel in Gardenia |
| Corphish | old rod | 3 | Oxide | Bubble | Harden 7, ViceGrip 10, Leer 13 | Corphish; Crawdaunt in Fantina |
| Corphish | old rod | 3 | Rewrite | Bubble | Taunt 8, ViceGrip 10, BubbleBeam 12, Leer 13 | Corphish; Crawdaunt in Fantina |
| Goldeen | old rod | 3 | Oxide | Peck, Tail Whip, Water Sport | Supersonic 7, Horn Attack 11 | Goldeen; Seaking in Fantina |
| Goldeen | old rod | 3 | Rewrite | Peck, Water Sport | Flip Turn 4, Water Pulse 10, Horn Attack 11 | Goldeen; Seaking in Fantina |
| Squirtle | old rod | 3 | Oxide | Tackle | Tail Whip 4, Bubble 7, Withdraw 10, Water Gun 13, Bite 16; as Wartortle: Bite 16 | Wartortle (from 16); Blastoise in Maylene |
| Squirtle | old rod | 3 | Rewrite | Tackle | Life Dew 4, Bubble 7, Water Gun 13, Water Pulse 15, Bite 16; as Wartortle: Bite 16 | Wartortle (from 16); Blastoise in Maylene |

## Verity Lakefront

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 16 | At the cap |
|---|---|---|---|---|---|---|
| Starly | wild | 2 | Oxide | Tackle, Growl | Quick Attack 5, Wing Attack 9, Double Team 13 | Staravia (from 14); Staraptor in Maylene |
| Starly | wild | 2 | Rewrite | Tackle | Tailwind 3, Quick Attack 5, Wing Attack 9, Pursuit 14 | Staravia (from 14); Staraptor in Maylene |
| Blipbug | wild | 3 | Oxide | Struggle Bug | as Dottler: Reflect 10, Light Screen 10, Confusion 10 | Dottler (from 10); Orbeetle in Fantina |
| Blipbug | wild | 3 | Rewrite | Struggle Bug | Calm Mind 4, Trailblaze 10; as Dottler: Reflect 10, Confusion 11, Light Screen 12 | Dottler (from 10); Orbeetle in Fantina |
| Kricketot | wild | 3 | Oxide | Growl, Bide | as Kricketune: Fury Cutter 10, Leech Life 14 | Kricketune (from 10) |
| Kricketot | wild | 3 | Rewrite | Growl, Fell Stinger | Struggle Bug 6, Screech 10; as Kricketune: Fury Cutter 10, Leech Life 14, Bug Bite 16 | Kricketune (from 10) |
| Minccino | wild | 3 | Oxide | Pound, Baby-Doll Eyes | Helping Hand 5, DoubleSlap 13, Sing 16 | Minccino; Cinccino in Wake |
| Minccino | wild | 3 | Rewrite | Pound, Baby-Doll Eyes | Helping Hand 5, Chilling Water 7, Swift 9, DoubleSlap 13, Sing 16 | Minccino; Cinccino in Wake |
| Pikipek | wild | 3 | Oxide | Peck, Growl | Echoed Voice 7, Rock Smash 9, Supersonic 13; as Trumbeak: Pluck 16 | Trumbeak (from 14); Toucannon in Fantina |
| Pikipek | wild | 3 | Rewrite | Peck | Pluck 4, Echoed Voice 7, Rock Smash 9, Scary Face 11, Supersonic 13 | Trumbeak (from 14); Toucannon in Fantina |
| Purrloin | wild | 3 to 4 | Oxide | Scratch, Growl | Sand-Attack 6, Assist 6, Fake Out 12, Fury Swipes 12, Pursuit 15 | Purrloin; Liepard in Gardenia |
| Purrloin | wild | 3 to 4 | Rewrite | Scratch | Taunt 4, Sand-Attack 6, Snarl 9, Fury Swipes 11, Fake Out 12, Pursuit 15 | Purrloin; Liepard in Gardenia |
| Wooloo | wild | 3 to 4 | Oxide | Tackle, Growl | Defense Curl 4, Copycat 8, Guard Split 12, Double Kick 16 | Wooloo; Dubwool in Gardenia |
| Wooloo | wild | 3 to 4 | Rewrite | Tackle, Round | Guard Split 12, Double Kick 16 | Wooloo; Dubwool in Gardenia |
| Buneary | wild | 4 to 5 | Oxide | Splash, Pound, Defense Curl, Foresight | Endure 6, Frustration 13, Quick Attack 16 | Buneary; Lopunny in Gardenia |
| Buneary | wild | 4 to 5 | Rewrite | Pound, Defense Curl, Foresight | Covet 5, Endure 6, Baby-Doll Eyes 8, Power-Up Punch 9, Return 12, Frustration 13, Quick Attack 16 | Buneary; Lopunny in Gardenia |
| Sentret | wild | 4 | Oxide | Scratch, Foresight, Defense Curl | Quick Attack 7, Fury Swipes 13 | Furret (from 15) |
| Sentret | wild | 4 | Rewrite | Scratch, Foresight, Defense Curl | Baby-Doll Eyes 5, Pursuit 6, Quick Attack 7, Covet 10, Fury Swipes 13; as Furret: Helping Hand 16 | Furret (from 15) |
| Surskit | wild | 4 | Oxide | Bubble | Quick Attack 7, Sweet Scent 13 | Surskit; Masquerain in Gardenia |
| Surskit | wild | 4 | Rewrite | Bubble, Sticky Web | Quick Attack 7, Gust 10, Silver Wind 13 | Surskit; Masquerain in Gardenia |
| Vulpix | wild | 4 to 5 | Oxide | Ember, Tail Whip | Roar 7, Quick Attack 11, Will-O-Wisp 14 | Vulpix; Ninetales in Maylene |
| Vulpix | wild | 4 to 5 | Rewrite | Ember, Tail Whip | Powder Snow 7, Quick Attack 11, Will-O-Wisp 14, Incinerate 16 | Vulpix; Ninetales in Maylene |

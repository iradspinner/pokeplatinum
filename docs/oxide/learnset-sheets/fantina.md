# Fantina's split: what each catch knows and learns

Written by `tools/oxide/balance/learncheck.py sheets` for check 6 of the learnset baseline (`docs/oxide/learnset-checks.md`). One table per capture area first offered in Fantina's split, whose cap is 33. Each Pokemon is read at the lowest level it is found at there. "Knows at capture" is the last four moves its list gives by that level; "learns by level-up" is every entry it reaches after capture up to 33, evolving on time, with each later stage's moves under its name; "at the cap" is the stage it can be by then and the next one after. A row marked v3 shows learnset v3 (unlanded, `origin/balance-learngen-v2`) where it differs from Oxide's lists; a row marked both is the same in each. Relearner-only moves and egg moves are left out. Nothing here is in the game data.

## Amity Square

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 33 | At the cap |
|---|---|---|---|---|---|---|
| Snubbull | wild | 8 to 11 | both | Scary Face, Tail Whip, Charm, Bite | Lick 13, Headbutt 19; as Granbull: Roar 27 | Granbull (from 23) |
| Azurill | wild | 9 to 10 | Oxide | Splash, Charm, Tail Whip | Bubble 10; as Marill: Water Gun 10, Rollout 15, BubbleBeam 18; as Azumarill: BubbleBeam 20, Aqua Ring 27, Double-Edge 33 | Azumarill (from 18) |
| Azurill | wild | 9 to 10 | v3 | Pound, Charm, Tail Whip | Bubble 10; as Marill: Water Gun 10, BubbleBeam 18; as Azumarill: BubbleBeam 20, Aqua Ring 27, Double-Edge 33 | Azumarill (from 18) |
| Buneary | wild | 9 | both | Pound, Defense Curl, Foresight, Endure | Frustration 13, Quick Attack 16; as Lopunny: Jump Kick 23, Baton Pass 26, Agility 33 | Lopunny (from 20) |
| Drifloon | wild | 9 | Oxide | Constrict, Minimize, Astonish | Gust 11, Focus Energy 14, Payback 17, Stockpile 22, Swallow 27, Spit Up 27; as Drifblim: Ominous Wind 32 | Drifblim (from 28) |
| Drifloon | wild | 9 | v3 | Minimize, Shadow Sneak | Gust 11, Focus Energy 14, Payback 17, Stockpile 22, Swallow 27, Spit Up 27; as Drifblim: Ominous Wind 32 | Drifblim (from 28) |
| Minccino | wild | 9 | both | Pound, Baby-Doll Eyes, Helping Hand | DoubleSlap 13, Sing 16, Echoed Voice 19, Swift 19, Encore 19, Charm 21, Tickle 23, Tail Slap 28, Wake-Up Slap 31 | Minccino; Cinccino in Wake |
| Purrloin | wild | 9 | both | Scratch, Growl, Sand-Attack, Assist | Fake Out 12, Fury Swipes 12, Pursuit 15, Torment 17; as Liepard: Fake Out 22, Assurance 26, Hone Claws 27 | Liepard (from 20) |
| Smoochum | wild | 9 | both | Pound, Lick, Sweet Kiss | Powder Snow 11, Confusion 15, Sing 18, Mean Look 21, Fake Tears 25, Lucky Chant 28; as Jynx: Avalanche 33 | Jynx (from 30) |
| Swablu | wild | 9 to 10 | Oxide | Peck, Growl, Astonish, Sing | Fury Attack 13, Safeguard 18, Mist 23, Take Down 28, Natural Gift 32 | Swablu; Altaria in Maylene |
| Swablu | wild | 9 to 10 | v3 | Peck, Growl, Fairy Wind, Sing | Fury Attack 13, Safeguard 18, Mist 23, Take Down 28, Natural Gift 32 | Swablu; Altaria in Maylene |
| Fomantis | wild | 10 | Oxide | Leafage, Fury Cutter, Growth | Razor Leaf 12, Ingrain 14, Sweet Scent 27, Slash 28, X-Scissor 30, Synthesis 31, Leaf Blade 32 | Fomantis; Lurantis in Maylene |
| Fomantis | wild | 10 | v3 | Leafage, Growth | Razor Leaf 12, Ingrain 14, Sweet Scent 27, Slash 28, X-Scissor 30, Synthesis 31 | Fomantis; Lurantis in Maylene |
| Glameow | wild | 10 | both | Fake Out, Scratch, Growl | Hypnosis 13, Faint Attack 17, Fury Swipes 20, Charm 25, Assist 29, Captivate 32 | Glameow; Purugly in Maylene |
| Klefki | wild | 11 | Oxide | Fairy Lock, Astonish, Tackle, Fairy Wind | Spikes 15, Metal Sound 16, Crafty Shield 19, Torment 21, Draining Kiss 21, Recycle 33, Imprison 33 | Klefki |
| Klefki | wild | 11 | v3 | Tackle, Fairy Wind | Spikes 15, Metal Sound 16, Crafty Shield 19, Torment 21, Draining Kiss 21, Recycle 33, Imprison 33 | Klefki |
| Pikachu | wild | 11 | Oxide | ThunderShock, Growl, Tail Whip, Thunder Wave | Quick Attack 13, Double Team 18, Slam 21, Thunderbolt 26, Feint 29 | Pikachu; Raichu in Maylene |
| Pikachu | wild | 11 | v3 | ThunderShock, Growl, Tail Whip, Thunder Wave | Quick Attack 13, Double Team 18, Slam 21, Feint 29, Thunderbolt 30 | Pikachu; Raichu in Maylene |

## Hearthome City

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 33 | At the cap |
|---|---|---|---|---|---|---|
| Eevee | gift | 20 | Oxide | Tackle, Helping Hand, Sand-Attack, Growl | Quick Attack 22, Bite 29 | Leafeon (from 30) |
| Eevee | gift | 20 | Oxide | Tackle, Helping Hand, Sand-Attack, Growl | Quick Attack 22, Bite 29 | Glaceon (from 30) |
| Eevee | gift | 20 | Oxide | Tackle, Helping Hand, Sand-Attack, Growl | Quick Attack 22, Bite 29 | Eevee; Flareon in Maylene, Jolteon in Maylene, Vaporeon in Maylene, Espeon in Byron |
| Eevee | gift | 20 | Oxide | Tackle, Helping Hand, Sand-Attack, Growl | as Umbreon: Quick Attack 22, Confuse Ray 29 | Umbreon (from 20) |
| Eevee | gift | 20 | Oxide | Tackle, Helping Hand, Sand-Attack, Growl | Quick Attack 22, Bite 29; as Sylveon: Misty Terrain 32, Skill Swap 33 | Sylveon (from 32) |
| Eevee | gift | 20 | v3 | Tackle, Helping Hand, Sand-Attack, Growl | Quick Attack 22, Bite 29 | Leafeon (from 30) |
| Eevee | gift | 20 | v3 | Tackle, Helping Hand, Sand-Attack, Growl | Quick Attack 22, Bite 29 | Glaceon (from 30) |
| Eevee | gift | 20 | v3 | Tackle, Helping Hand, Sand-Attack, Growl | Quick Attack 22, Bite 29 | Eevee; Flareon in Maylene, Jolteon in Maylene, Vaporeon in Maylene, Espeon in Byron |
| Eevee | gift | 20 | v3 | Tackle, Helping Hand, Sand-Attack, Growl | as Umbreon: Quick Attack 22, Bite 28, Confuse Ray 29, Body Slam 30 | Umbreon (from 20) |
| Eevee | gift | 20 | v3 | Tackle, Helping Hand, Sand-Attack, Growl | Quick Attack 22, Bite 29; as Sylveon: Draining Kiss on evolving, Disarming Voice on evolving, Fairy Wind on evolving, Dazzling Gleam 32, Skill Swap 33 | Sylveon (from 32) |

## Mining Museum

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 33 | At the cap |
|---|---|---|---|---|---|---|
| Cranidos | fossil | 20 | both | Focus Energy, Pursuit, Take Down, Scary Face | Assurance 24, AncientPower 28; as Rampardos: Endeavor 30 | Rampardos (from 30) |
| Lileep | fossil | 20 | Oxide | Astonish, Constrict, Acid, Ingrain | Confuse Ray 22, Amnesia 29 | Lileep; Cradily in Wake |
| Lileep | fossil | 20 | v3 | Acid, Ingrain | Confuse Ray 22, Amnesia 29 | Lileep; Cradily in Wake |
| Shieldon | fossil | 20 | both | Taunt, Metal Sound, Take Down, Iron Defense | Swagger 24, AncientPower 28; as Bastiodon: Block 30 | Bastiodon (from 30) |

## Mt. Coronet South

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 33 | At the cap |
|---|---|---|---|---|---|---|
| Barboach | old rod | 8 | Oxide | Mud-Slap, Mud Sport, Water Sport | Water Gun 10, Mud Bomb 14, Amnesia 18, Water Pulse 22, Magnitude 26; as Whiscash: Rest 33, Snore 33 | Whiscash (from 30) |
| Barboach | old rod | 8 | v3 | Mud-Slap, Mud Sport, Water Sport | Water Gun 10, Mud Bomb 14, Amnesia 18, Water Pulse 22, Magnitude 26; as Whiscash: Rest 33 | Whiscash (from 30) |
| Goldeen | old rod | 8 | Oxide | Peck, Tail Whip, Water Sport, Supersonic | Horn Attack 11, Water Pulse 17, Flail 21, Aqua Ring 27, Fury Attack 31 | Seaking (from 33) |
| Goldeen | old rod | 8 | v3 | Peck, Tail Whip, Water Sport, Supersonic | Horn Attack 11, Water Pulse 17, Flail 21, Aqua Ring 27 | Seaking (from 33) |
| Corphish | old rod | 9 | both | Bubble, Harden | ViceGrip 10, Leer 13, BubbleBeam 20, Protect 23, Knock Off 26; as Crawdaunt: Swift 30 | Crawdaunt (from 30) |
| Feebas | old rod | 9 | Oxide | Splash | Tackle 15, Flail 30 | Milotic (from 30) |
| Feebas | old rod | 9 | v3 | Tackle | Water Gun 15, Flail 30 | Milotic (from 30) |
| Clamperl | old rod | 10 | Oxide | Clamp, Water Gun, Whirlpool, Iron Defense | as Huntail: Screech 10, Water Pulse 15, Scary Face 19, Ice Fang 24, Brine 28, Baton Pass 33 | Huntail (from 10) |
| Clamperl | old rod | 10 | Oxide | Clamp, Water Gun, Whirlpool, Iron Defense | as Gorebyss: Agility 10, Water Pulse 15, Amnesia 19, Aqua Ring 24, Captivate 28, Baton Pass 33 | Gorebyss (from 10) |
| Clamperl | old rod | 10 | v3 | Water Gun, Iron Defense | as Huntail: Screech 10, Water Pulse 15, Scary Face 19, Brine 28, Ice Fang 32, Baton Pass 33 | Huntail (from 10) |
| Clamperl | old rod | 10 | v3 | Water Gun, Iron Defense | as Gorebyss: Agility 10, Water Pulse 15, Amnesia 19, Aqua Ring 24, Captivate 28, Baton Pass 33 | Gorebyss (from 10) |
| Glimmet | wild | 17 to 20 | both | Smack Down, Acid Spray, AncientPower, Rock Polish | Stealth Rock 18, Venoshock 22, Selfdestruct 29, Rock Slide 33 | Glimmet; Glimmora in Maylene |
| Bronzor | wild | 18 | Oxide | Confusion, Hypnosis, Imprison, Confuse Ray | Extrasensory 19, Iron Defense 26, Safeguard 30; as Bronzong: Block 33 | Bronzong (from 33) |
| Bronzor | wild | 18 | v3 | Confusion, Hypnosis, Imprison, Confuse Ray | Extrasensory 19, Iron Head 20, Iron Defense 26, Safeguard 30, Zen Headbutt 31; as Bronzong: Block 33 | Bronzong (from 33) |
| Makuhita | wild | 18 | both | Arm Thrust, Vital Throw, Fake Out, Whirlwind | Knock Off 19, SmellingSalt 22; as Hariyama: Belly Drum 27, Force Palm 32 | Hariyama (from 24) |
| Mienfoo | wild | 18 to 19 | Oxide | Pound, Rock Smash, Fake Out, DoubleSlap | Force Palm 20, Bounce 22, Drain Punch 25, Vacuum Wave 32 | Mienfoo; Mienshao in Maylene |
| Mienfoo | wild | 18 to 19 | v3 | Pound, Rock Smash, Fake Out, DoubleSlap | Force Palm 20, Bounce 22, Vacuum Wave 32, Drain Punch 33 | Mienfoo; Mienshao in Maylene |
| Nacli | wild | 18 to 19 | Oxide | Mud Shot, Smack Down, Rock Polish, Headbutt | Iron Defense 20; as Naclstack: Recover 30 | Naclstack (from 24); Garganacl in Maylene |
| Nacli | wild | 18 to 19 | v3 | Mud Shot, Smack Down, Rock Polish, Headbutt | Iron Defense 20; as Naclstack: Salt Cure on evolving, Recover 30 | Naclstack (from 24); Garganacl in Maylene |
| Phanpy | wild | 18 | Oxide | Defense Curl, Flail, Take Down, Rollout | Natural Gift 19, Slam 24; as Donphan: Fury Attack 25, Assurance 31 | Donphan (from 25) |
| Phanpy | wild | 18 | v3 | Growl, Defense Curl, Flail, Take Down | Natural Gift 19, Slam 24; as Donphan: Fury Attack 25, Assurance 31 | Donphan (from 25) |
| Snorunt | wild | 18 | both | Leer, Double Team, Bite, Icy Wind | Headbutt 19, Protect 22, Ice Fang 28, Crunch 31 | Snorunt; Glalie in Wake, Froslass in Byron |
| Zubat | wild | 18 to 19 | Oxide | Supersonic, Astonish, Bite, Wing Attack | Confuse Ray 21; as Golbat: Air Cutter 27, Mean Look 33 | Golbat (from 22); Crobat in Wake |
| Zubat | wild | 18 to 19 | v3 | Supersonic, Acid, Bite, Wing Attack | Confuse Ray 21; as Golbat: Air Cutter 27, Mean Look 33 | Golbat (from 22); Crobat in Wake |
| Carbink | wild | 19 | both | Sharpen, Smack Down, Guard Split, Reflect | Flail 24, AncientPower 25, Rock Polish 25 | Carbink |
| Seel | wild | 20 | both | Water Sport, Icy Wind, Encore, Ice Shard | Rest 21, Aqua Ring 23, Aurora Beam 27, Aqua Jet 31, Brine 33 | Seel; Dewgong in Maylene |
| Snom | wild | 20 | both | Powder Snow, Struggle Bug | as Frosmoth: Bug Buzz 32 | Frosmoth (from 30) |

## Old Chateau

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 33 | At the cap |
|---|---|---|---|---|---|---|
| Gastly | wild | 14 to 17 | Oxide | Lick, Spite, Mean Look, Curse | Night Shade 15, Confuse Ray 19, Sucker Punch 22; as Haunter: Shadow Punch 25, Payback 28, Shadow Ball 33 | Haunter (from 25); Gengar in Wake |
| Gastly | wild | 14 to 17 | v3 | Lick, Spite, Mean Look, Curse | Night Shade 15, Confuse Ray 19, Sucker Punch 22; as Haunter: Payback 28, Shadow Ball 33 | Haunter (from 25); Gengar in Wake |
| Duskull | wild | 15 | Oxide | Night Shade, Disable, Foresight, Astonish | Confuse Ray 17, Shadow Sneak 22, Pursuit 25, Curse 30, Will-O-Wisp 33 | Duskull; Dusclops in Maylene |
| Duskull | wild | 15 | v3 | Leer, Night Shade, Disable, Foresight | Confuse Ray 17, Shadow Sneak 22, Pursuit 25, Future Sight 26, Curse 30, Will-O-Wisp 33 | Duskull; Dusclops in Maylene |
| Litwick | wild | 15 | Oxide | Smog, Confuse Ray, Fire Spin, Night Shade | Clear Smog 18, Will-O-Wisp 22, Flame Burst 26, Hex 30 | Litwick; Lampent in Wake |
| Litwick | wild | 15 | v3 | Ember, Smog, Confuse Ray, Night Shade | Clear Smog 18, Will-O-Wisp 22, Flame Burst 26, Hex 30 | Litwick; Lampent in Wake |
| Misdreavus | wild | 15 to 16 | Oxide | Psywave, Spite, Astonish, Confuse Ray | nothing | Mismagius (from 15) |
| Misdreavus | wild | 15 to 16 | v3 | Psywave, Spite, Shadow Sneak, Confuse Ray | nothing | Mismagius (from 15) |
| Sinistea | wild | 15 to 17 | Oxide | Astonish, Withdraw, Aromatic Mist, Mega Drain | as Polteageist: Protect 18, Sucker Punch 24, Aromatherapy 30 | Polteageist (from 15) |
| Sinistea | wild | 15 to 17 | Oxide | Astonish, Withdraw, Aromatic Mist, Mega Drain | as Sinistcha: Foul Play 18, Mega Drain 24, Hex 30 | Sinistcha (from 15) |
| Sinistea | wild | 15 to 17 | v3 | Withdraw, Mega Drain | as Polteageist: Protect 18, Sucker Punch 24, Aromatherapy 30 | Polteageist (from 15) |
| Sinistea | wild | 15 to 17 | v3 | Withdraw, Mega Drain | as Sinistcha: Matcha Gotcha on evolving, Mega Drain 24, Aromatherapy 29, Hex 30 | Sinistcha (from 15) |
| Yamask | wild | 16 to 17 | both | Protect, Haze, Disable, Night Shade | Will-O-Wisp 18, Crafty Shield 20, Hex 20, Ominous Wind 25, Curse 32 | Yamask; Cofagrigus in Maylene, Runerigus in Candice |
| Rotom | static battle | 20 | both | ThunderShock, Confuse Ray, Uproar, Double Team | Shock Wave 22, Ominous Wind 29 | Rotom |

## Route 206

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 33 | At the cap |
|---|---|---|---|---|---|---|
| Gligar | wild | 16 | Oxide | Sand-Attack, Harden, Knock Off, Quick Attack | Fury Cutter 20, Faint Attack 23, Screech 27, Slash 31 | Gligar; Gliscor in Wake |
| Gligar | wild | 16 | v3 | Sand-Attack, Harden, Knock Off, Quick Attack | Faint Attack 23, Screech 27, Slash 31 | Gligar; Gliscor in Wake |
| Charcadet | wild | 17 | Oxide | Clear Smog, Fire Spin | Will-O-Wisp 20, Night Shade 30 | Charcadet; Armarouge in Byron |
| Charcadet | wild | 17 | Oxide | Clear Smog, Fire Spin | as Ceruledge: Night Shade 20, Flame Charge 24, Incinerate 28, Lava Plume 32 | Ceruledge (from 17) |
| Charcadet | wild | 17 | v3 | Clear Smog | Will-O-Wisp 20, Night Shade 30 | Charcadet; Armarouge in Byron |
| Charcadet | wild | 17 | v3 | Clear Smog | as Ceruledge: Shadow Claw on evolving, Night Slash on evolving, Shadow Sneak on evolving, Quick Guard on evolving, Solar Blade on evolving, Night Shade 20, Flame Charge 24, Incinerate 28, Lava Plume 32 | Ceruledge (from 17) |
| Fletchinder | wild | 17 | both | Growl, Quick Attack, Aerial Ace, Flame Charge | Roost 22, Will-O-Wisp 27, Natural Gift 31 | Fletchinder; Talonflame in Maylene |
| Houndour | wild | 17 | both | Howl, Smog, Roar, Bite | Odor Sleuth 22; as Houndoom: Fire Fang 32 | Houndoom (from 27) |
| Ponyta | wild | 17 | Oxide | Tackle, Tail Whip, Ember, Flame Wheel | Stomp 19, Fire Spin 24, Take Down 28, Agility 33 | Ponyta; Rapidash in Wake |
| Ponyta | wild | 17 | Oxide | Tackle, Tail Whip, Ember, Flame Wheel | as Galarian Rapidash: Agility 20, Psybeam 25, Stomp 30 | Galarian Rapidash (from 17) |
| Ponyta | wild | 17 | v3 | Tackle, Tail Whip, Ember, Flame Wheel | Stomp 19, Take Down 28, Agility 33 | Ponyta; Rapidash in Wake |
| Ponyta | wild | 17 | v3 | Tackle, Tail Whip, Ember, Flame Wheel | as Galarian Rapidash: Psycho Cut on evolving, Agility 20, Psybeam 25, Stomp 30 | Galarian Rapidash (from 17) |
| Stunky | wild | 17 | both | Poison Gas, Screech, Fury Swipes, SmokeScreen | Feint 18, Slash 22, Toxic 27, Night Slash 32 | Stunky; Skuntank in Maylene |
| Bonsly | wild | 18 | both | Flail, Low Kick, Rock Throw, Mimic | Block 22, Faint Attack 25, Rock Tomb 30; as Sudowoodo: Rock Slide 33 | Sudowoodo (from 32) |
| Joltik | wild | 18 | Oxide | Thunder Wave, Spider Web, Electroweb, Bug Bite | Gastro Acid 23, Struggle Bug 26, Discharge 29 | Galvantula (from 30) |
| Joltik | wild | 18 | v3 | Thunder Wave, Spider Web, Electroweb, Bug Bite | Gastro Acid 23, Struggle Bug 26 | Galvantula (from 30) |
| Onix | wild | 18 | Oxide | Screech, Rock Throw, Rage, Rock Tomb | as Steelix: Slam 25, Rock Polish 30, DragonBreath 33 | Steelix (from 18) |
| Onix | wild | 18 | v3 | Harden, Screech, Rock Throw, Rock Tomb | as Steelix: Slam 25, Rock Polish 30, DragonBreath 33 | Steelix (from 18) |
| Salandit | wild | 18 | Oxide | Ember, Sweet Scent, Venom Drench, Flame Burst | Dragon Rage 21, Toxic 24, Venoshock 29 | Salazzle (from 30) |
| Salandit | wild | 18 | v3 | Smog, Ember, Sweet Scent, Venom Drench | Dragon Rage 21, Toxic 24, Flame Burst 26, Venoshock 29 | Salazzle (from 30) |
| Dwebble | wild | 19 | Oxide | Block, Sand-Attack, Faint Attack, Slash | Rock Tomb 21, Bug Bite 24, Night Slash 27, X-Scissor 31 | Dwebble; Crustle in Maylene |
| Dwebble | wild | 19 | v3 | Block, Sand-Attack, Faint Attack, Slash | Rock Tomb 21, Bug Bite 24, Night Slash 27, X-Scissor 31, Rock Blast 33 | Dwebble; Crustle in Maylene |
| Frogadier | wild | 19 | Oxide | Quick Attack, Lick, Water Pulse, Icy Wind | Faint Attack 20, Acrobatics 22, Low Kick 25, Waterfall 30 | Frogadier; Greninja in Maylene |
| Frogadier | wild | 19 | v3 | Quick Attack, Lick, Water Pulse, Icy Wind | Faint Attack 20, Acrobatics 22, Low Kick 25 | Frogadier; Greninja in Maylene |
| Nacli | wild | 19 | Oxide | Mud Shot, Smack Down, Rock Polish, Headbutt | Iron Defense 20; as Naclstack: Recover 30 | Naclstack (from 24); Garganacl in Maylene |
| Nacli | wild | 19 | v3 | Mud Shot, Smack Down, Rock Polish, Headbutt | Iron Defense 20; as Naclstack: Salt Cure on evolving, Recover 30 | Naclstack (from 24); Garganacl in Maylene |

## Route 208

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 33 | At the cap |
|---|---|---|---|---|---|---|
| Poliwag | old rod | 8 | both | Water Sport, Bubble, Hypnosis | Water Gun 11, DoubleSlap 15, Body Slam 21, BubbleBeam 25; as Poliwhirl: BubbleBeam 27, Mud Shot 32 | Poliwhirl (from 25); Poliwrath in Maylene, Politoed in Wake |
| Wailmer | old rod | 8 | Oxide | Splash, Growl, Water Gun | Rollout 11, Whirlpool 14, Astonish 17, Water Pulse 21, Mist 24, Rest 27, Brine 31 | Wailmer; Wailord in Wake |
| Wailmer | old rod | 8 | v3 | Water Gun, Growl | Water Pulse 21, Mist 24, Rest 27, Brine 31 | Wailmer; Wailord in Wake |
| Feebas | old rod | 9 | Oxide | Splash | Tackle 15, Flail 30 | Milotic (from 30) |
| Feebas | old rod | 9 | v3 | Tackle | Water Gun 15, Flail 30 | Milotic (from 30) |
| Totodile | old rod | 9 | Oxide | Scratch, Leer, Water Gun, Rage | Bite 13, Scary Face 15; as Croconaw: Ice Fang 21, Flail 24, Crunch 30; as Feraligatr: Agility 30, Crunch 32 | Feraligatr (from 30) |
| Totodile | old rod | 9 | v3 | Scratch, Leer, Water Gun | Bite 13, Scary Face 15; as Croconaw: Flail 24, Crunch 30; as Feraligatr: Agility 30, Crunch 32 | Feraligatr (from 30) |
| Froakie | old rod | 10 | Oxide | Pound, Water Gun, Growl, Quick Attack | Lick 13, Water Pulse 14, Icy Wind 16; as Frogadier: Icy Wind 16, Faint Attack 20, Acrobatics 22, Low Kick 25, Waterfall 30 | Frogadier (from 16); Greninja in Maylene |
| Froakie | old rod | 10 | v3 | Pound, Water Gun, Growl, Quick Attack | Lick 13, Water Pulse 14, Icy Wind 16; as Frogadier: Icy Wind 16, Faint Attack 20, Acrobatics 22, Low Kick 25 | Frogadier (from 16); Greninja in Maylene |
| Fomantis | wild | 17 | Oxide | Fury Cutter, Growth, Razor Leaf, Ingrain | Sweet Scent 27, Slash 28, X-Scissor 30, Synthesis 31, Leaf Blade 32 | Fomantis; Lurantis in Maylene |
| Fomantis | wild | 17 | v3 | Leafage, Growth, Razor Leaf, Ingrain | Sweet Scent 27, Slash 28, X-Scissor 30, Synthesis 31 | Fomantis; Lurantis in Maylene |
| Budew | wild | 18 | both | Water Sport, Stun Spore, Mega Drain, Worry Seed | as Roselia: Sweet Scent 31 | Roselia (from 30); Roserade in Wake |
| Grubbin | wild | 18 | Oxide | Mud-Slap, String Shot, Bug Bite, Bite | as Charjabug: Spark 23, Sticky Web 29 | Charjabug (from 20); Vikavolt in Maylene |
| Grubbin | wild | 18 | v3 | Mud-Slap, String Shot, Bug Bite, Bite | as Charjabug: Charge on evolving, Spark 23, Sticky Web 29 | Charjabug (from 20); Vikavolt in Maylene |
| Mightyena | wild | 18 | both | Howl, Sand-Attack, Bite, Odor Sleuth | Roar 22, Swagger 27, Assurance 32 | Mightyena |
| Pachirisu | wild | 18 | Oxide | Quick Attack, Charm, Spark, Endure | Swift 21, Sweet Kiss 25, Discharge 29, Super Fang 33 | Pachirisu |
| Pachirisu | wild | 18 | v3 | Quick Attack, Charm, Spark, Endure | Swift 21, Sweet Kiss 25, Discharge 29, Thunder Fang 32, Super Fang 33 | Pachirisu |
| Purrloin | wild | 18 | both | Fake Out, Fury Swipes, Pursuit, Torment | as Liepard: Fake Out 22, Assurance 26, Hone Claws 27 | Liepard (from 20) |
| Ralts | wild | 18 | Oxide | Confusion, Double Team, Teleport, Lucky Chant | as Kirlia: Magical Leaf 22, Calm Mind 25; as Gardevoir: Psychic 33 | Gardevoir (from 30) |
| Ralts | wild | 18 | Oxide | Confusion, Double Team, Teleport, Lucky Chant | as Kirlia: Magical Leaf 22, Calm Mind 25, Psychic 31 | Kirlia (from 20); Gallade in Byron |
| Ralts | wild | 18 | v3 | Growl, Confusion, Double Team, Lucky Chant | as Kirlia: Magical Leaf 22, Calm Mind 25 | Gardevoir (from 30) |
| Ralts | wild | 18 | v3 | Growl, Confusion, Double Team, Lucky Chant | as Kirlia: Magical Leaf 22, Calm Mind 25 | Kirlia (from 20); Gallade in Byron |
| Sewaddle | wild | 18 | Oxide | Tackle, String Shot, Bug Bite, Razor Leaf | as Leavanny: Helping Hand 32 | Leavanny (from 30) |
| Sewaddle | wild | 18 | v3 | Tackle, String Shot, Bug Bite, Razor Leaf | as Swadloon: Protect on evolving; as Leavanny: Slash on evolving, Helping Hand 32 | Leavanny (from 30) |
| Combee | wild | 19 | both | Sweet Scent, Gust, Bug Bite | as Vespiquen: Power Gem 21, Heal Order 25, Toxic 27, Slash 31, Captivate 33 | Vespiquen (from 21) |
| Fletchinder | wild | 19 | both | Growl, Quick Attack, Aerial Ace, Flame Charge | Roost 22, Will-O-Wisp 27, Natural Gift 31 | Fletchinder; Talonflame in Maylene |
| Smoliv | wild | 19 | Oxide | Growth, Razor Leaf, Helping Hand, Flail | Mega Drain 20, Grassy Terrain 23; as Dolliv: Seed Bomb 29 | Dolliv (from 25); Arboliva in Maylene |
| Smoliv | wild | 19 | v3 | Growth, Razor Leaf, Helping Hand, Flail | Mega Drain 20 | Dolliv (from 25); Arboliva in Maylene |
| Steenee | wild | 19 | Oxide | Play Nice, Rapid Spin, Razor Leaf, Sweet Scent | Magical Leaf 21, Teeter Dance 23, Stomp 25, Aromatic Mist 32; as Tsareena: Low Sweep 32 | Tsareena (from 32) |
| Steenee | wild | 19 | v3 | Play Nice, Rapid Spin, Razor Leaf, Sweet Scent | Magical Leaf 21, Teeter Dance 23, Stomp 25; as Tsareena: Low Sweep 32 | Tsareena (from 32) |
| Carnivine | wild | 20 | both | Growth, Bite, Vine Whip, Sweet Scent | Ingrain 21, Faint Attack 27, Stockpile 31, Spit Up 31, Swallow 31 | Carnivine |
| Grovyle | wild | 20 | Oxide | Absorb, Quick Attack, Fury Cutter, Pursuit | Screech 23, Leaf Blade 29 | Grovyle; Sceptile in Maylene |
| Grovyle | wild | 20 | v3 | Pound, Leer, Quick Attack, Pursuit | Screech 23 | Grovyle; Sceptile in Maylene |
| Happiny | wild | 20 | both | Charm, Copycat, Refresh, Sweet Kiss | as Chansey: Minimize 20, Sing 23, Fling 27, Defense Curl 31 | Chansey (from 20); Blissey in Wake |

## Wayward Cave

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 33 | At the cap |
|---|---|---|---|---|---|---|
| Carbink | wild | 17 to 20 | both | Rock Throw, Sharpen, Smack Down, Guard Split | Reflect 18, Flail 24, AncientPower 25, Rock Polish 25 | Carbink |
| Phanpy | wild | 17 to 20 | Oxide | Defense Curl, Flail, Take Down, Rollout | Natural Gift 19, Slam 24; as Donphan: Fury Attack 25, Assurance 31 | Donphan (from 25) |
| Phanpy | wild | 17 to 20 | v3 | Growl, Defense Curl, Flail, Take Down | Natural Gift 19, Slam 24; as Donphan: Fury Attack 25, Assurance 31 | Donphan (from 25) |
| Bronzor | wild | 18 to 19 | Oxide | Confusion, Hypnosis, Imprison, Confuse Ray | Extrasensory 19, Iron Defense 26, Safeguard 30; as Bronzong: Block 33 | Bronzong (from 33) |
| Bronzor | wild | 18 to 19 | v3 | Confusion, Hypnosis, Imprison, Confuse Ray | Extrasensory 19, Iron Head 20, Iron Defense 26, Safeguard 30, Zen Headbutt 31; as Bronzong: Block 33 | Bronzong (from 33) |
| Geodude | wild | 18 | Oxide | Rock Polish, Rock Throw, Magnitude, Selfdestruct | Rollout 22, Rock Blast 25; as Graveler: Rock Blast 27, Earthquake 33 | Graveler (from 25); Golem in Wake |
| Geodude | wild | 18 | v3 | Rock Polish, Rock Throw, Magnitude, Selfdestruct | Rock Blast 25; as Graveler: Rock Blast 27 | Graveler (from 25); Golem in Wake |
| Gible | wild | 18 | Oxide | Tackle, Sand-Attack, Dragon Rage, Take Down | Sand Tomb 19; as Gabite: Slash 28, Dragon Claw 33 | Gabite (from 24); Garchomp in Byron |
| Gible | wild | 18 | v3 | Tackle, Sand-Attack, Dragon Rage, Take Down | as Gabite: Slash 28, Dragon Claw 33 | Gabite (from 24); Garchomp in Byron |
| Glimmet | wild | 18 to 19 | both | Acid Spray, AncientPower, Rock Polish, Stealth Rock | Venoshock 22, Selfdestruct 29, Rock Slide 33 | Glimmet; Glimmora in Maylene |
| Houndour | wild | 18 | both | Howl, Smog, Roar, Bite | Odor Sleuth 22; as Houndoom: Fire Fang 32 | Houndoom (from 27) |
| Meditite | wild | 18 | both | Confusion, Detect, Hidden Power, Mind Reader | Feint 22, Calm Mind 25, Force Palm 29, Hi Jump Kick 32 | Meditite; Medicham in Maylene |
| Mightyena | wild | 18 | both | Howl, Sand-Attack, Bite, Odor Sleuth | Roar 22, Swagger 27, Assurance 32 | Mightyena |
| Nosepass | wild | 18 | both | Tackle, Harden, Rock Throw | Block 19, Thunder Wave 25, Rock Slide 31 | Probopass (from 32) |
| Sandygast | wild | 18 to 19 | Oxide | Astonish, Sand Tomb, Sand-Attack, Mega Drain | Bulldoze 24, Hypnosis 28 | Sandygast; Palossand in Wake |
| Sandygast | wild | 18 to 19 | v3 | Harden, Shadow Sneak, Sand-Attack, Mega Drain | Bulldoze 24, Hypnosis 28, Earth Power 32 | Sandygast; Palossand in Wake |
| Zubat | wild | 18 to 19 | Oxide | Supersonic, Astonish, Bite, Wing Attack | Confuse Ray 21; as Golbat: Air Cutter 27, Mean Look 33 | Golbat (from 22); Crobat in Wake |
| Zubat | wild | 18 to 19 | v3 | Supersonic, Acid, Bite, Wing Attack | Confuse Ray 21; as Golbat: Air Cutter 27, Mean Look 33 | Golbat (from 22); Crobat in Wake |
| Dwebble | wild | 19 | Oxide | Block, Sand-Attack, Faint Attack, Slash | Rock Tomb 21, Bug Bite 24, Night Slash 27, X-Scissor 31 | Dwebble; Crustle in Maylene |
| Dwebble | wild | 19 | v3 | Block, Sand-Attack, Faint Attack, Slash | Rock Tomb 21, Bug Bite 24, Night Slash 27, X-Scissor 31, Rock Blast 33 | Dwebble; Crustle in Maylene |
| Hippopotas | wild | 19 | Oxide | Sand-Attack, Bite, Yawn, Take Down | Sand Tomb 25, Crunch 31 | Hippopotas; Hippowdon in Maylene |
| Hippopotas | wild | 19 | v3 | Sand-Attack, Bite, Yawn, Take Down | Crunch 31 | Hippopotas; Hippowdon in Maylene |
| Onix | wild | 19 | Oxide | Screech, Rock Throw, Rage, Rock Tomb | as Steelix: Slam 25, Rock Polish 30, DragonBreath 33 | Steelix (from 19) |
| Onix | wild | 19 | v3 | Harden, Screech, Rock Throw, Rock Tomb | as Steelix: Slam 25, Rock Polish 30, DragonBreath 33 | Steelix (from 19) |
| Stunky | wild | 19 | both | Screech, Fury Swipes, SmokeScreen, Feint | Slash 22, Toxic 27, Night Slash 32 | Stunky; Skuntank in Maylene |
| Bonsly | wild | 20 | both | Flail, Low Kick, Rock Throw, Mimic | Block 22, Faint Attack 25, Rock Tomb 30; as Sudowoodo: Rock Slide 33 | Sudowoodo (from 32) |
| Larvitar | wild | 20 | both | Leer, Screech, Rock Slide, Scary Face | Thrash 23, Dark Pulse 28 | Pupitar (from 30); Tyranitar in Candice |
| Nacli | wild | 20 | Oxide | Smack Down, Rock Polish, Headbutt, Iron Defense | as Naclstack: Recover 30 | Naclstack (from 24); Garganacl in Maylene |
| Nacli | wild | 20 | v3 | Smack Down, Rock Polish, Headbutt, Iron Defense | as Naclstack: Salt Cure on evolving, Recover 30 | Naclstack (from 24); Garganacl in Maylene |

## Honey trees

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 33 | At the cap |
|---|---|---|---|---|---|---|
| Aipom | honey | 14 | Oxide | Tail Whip, Sand-Attack, Astonish, Baton Pass | Tickle 15, Fury Swipes 18, Swift 22, Screech 25, Agility 29, Double Hit 32; as Ambipom: Double Hit 32 | Ambipom (from 32) |
| Aipom | honey | 14 | v3 | Tail Whip, Sand-Attack, Tackle, Baton Pass | Tickle 15, Fury Swipes 18, Swift 22, Screech 25, Agility 29, Double Hit 32; as Ambipom: Double Hit 32 | Ambipom (from 32) |
| Burmy | honey | 14 | both | Protect, Tackle | Bug Bite 15, Hidden Power 20; as Wormadam: Hidden Power 20, Confusion 23, Razor Leaf 26, Growth 29, Psybeam 32 | Wormadam (from 20) |
| Burmy | honey | 14 | both | Protect, Tackle | Bug Bite 15, Hidden Power 20; as Mothim: Hidden Power 20, Confusion 23, Gust 26, PoisonPowder 29, Psybeam 32 | Mothim (from 20) |
| Combee | honey | 14 | both | Sweet Scent, Gust, Bug Bite | as Vespiquen: Power Gem 21, Heal Order 25, Toxic 27, Slash 31, Captivate 33 | Vespiquen (from 21) |
| Fomantis | honey | 14 | Oxide | Fury Cutter, Growth, Razor Leaf, Ingrain | Sweet Scent 27, Slash 28, X-Scissor 30, Synthesis 31, Leaf Blade 32 | Fomantis; Lurantis in Maylene |
| Fomantis | honey | 14 | v3 | Leafage, Growth, Razor Leaf, Ingrain | Sweet Scent 27, Slash 28, X-Scissor 30, Synthesis 31 | Fomantis; Lurantis in Maylene |
| Grubbin | honey | 14 | Oxide | ViceGrip, Mud-Slap, String Shot, Bug Bite | Bite 15; as Charjabug: Spark 23, Sticky Web 29 | Charjabug (from 20); Vikavolt in Maylene |
| Grubbin | honey | 14 | v3 | ViceGrip, Mud-Slap, String Shot, Bug Bite | Bite 15; as Charjabug: Charge on evolving, Spark 23, Sticky Web 29 | Charjabug (from 20); Vikavolt in Maylene |
| Heracross | honey | 14 | Oxide | Horn Attack, Endure, Fury Attack, Aerial Ace | Brick Break 19, Counter 25, Take Down 31 | Heracross |
| Heracross | honey | 14 | v3 | Horn Attack, Endure, Fury Attack, Aerial Ace | Counter 25, Brick Break 26, Take Down 31 | Heracross |
| Joltik | honey | 14 | Oxide | Absorb, Fury Cutter, Thunder Wave, Spider Web | Electroweb 15, Bug Bite 18, Gastro Acid 23, Struggle Bug 26, Discharge 29 | Galvantula (from 30) |
| Joltik | honey | 14 | v3 | String Shot, Thunder Wave, Spider Web | Electroweb 15, Bug Bite 18, Gastro Acid 23, Struggle Bug 26 | Galvantula (from 30) |
| Munchlax | honey | 14 | both | Tackle, Defense Curl, Amnesia, Lick | Recycle 17, Screech 20, Stockpile 25, Swallow 28, Body Slam 33 | Munchlax; Snorlax in Maylene |
| Nuzleaf | honey | 14 | Oxide | Pound, Harden, Growth, Nature Power | nothing | Shiftry (from 14) |
| Nuzleaf | honey | 14 | v3 | Pound, Harden, Growth, Nature Power | as Shiftry: Faint Attack 31 | Shiftry (from 14) |
| Sewaddle | honey | 14 | Oxide | Tackle, String Shot, Bug Bite, Razor Leaf | as Leavanny: Helping Hand 32 | Leavanny (from 30) |
| Sewaddle | honey | 14 | v3 | Tackle, String Shot, Bug Bite, Razor Leaf | as Swadloon: Protect on evolving; as Leavanny: Slash on evolving, Helping Hand 32 | Leavanny (from 30) |
| Shroomish | honey | 14 | Oxide | Absorb, Tackle, Stun Spore, Leech Seed | Mega Drain 17, Headbutt 21; as Breloom: Mach Punch 23, Counter 25, Force Palm 29, Sky Uppercut 33 | Breloom (from 23) |
| Shroomish | honey | 14 | v3 | Tackle, Stun Spore, Leech Seed | Mega Drain 17, Headbutt 21; as Breloom: Mach Punch 23, Counter 25, Force Palm 29, Sky Uppercut 33 | Breloom (from 23) |
| Steenee | honey | 14 | Oxide | DoubleSlap, Play Nice, Rapid Spin, Razor Leaf | Sweet Scent 17, Magical Leaf 21, Teeter Dance 23, Stomp 25, Aromatic Mist 32; as Tsareena: Low Sweep 32 | Tsareena (from 32) |
| Steenee | honey | 14 | v3 | DoubleSlap, Play Nice, Rapid Spin, Razor Leaf | Sweet Scent 17, Magical Leaf 21, Teeter Dance 23, Stomp 25; as Tsareena: Low Sweep 32 | Tsareena (from 32) |

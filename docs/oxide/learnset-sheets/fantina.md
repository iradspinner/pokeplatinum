# Fantina's split: what each catch knows and learns

Written by `tools/oxide/balance/learncheck.py sheets` for check 6 of the learnset baseline (`docs/oxide/learnset-checks.md`). One table per capture area first offered in Fantina's split, whose cap is 33. Each Pokemon is read at the lowest level it is found at there. "Knows at capture" is the last four moves its list gives by that level; "learns by level-up" is every entry it reaches after capture up to 33, evolving on time, with each later stage's moves under its name; "at the cap" is the stage it can be by then and the next one after. A row marked Rewrite shows the learnset rewrite's lists (the tree's) where it differs from the row marked Oxide, Oxide's lists before the learnset rewrite (`da6b92496c`); a row marked both is the same in each. Relearner-only moves and egg moves are left out.

## Eterna City

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 33 | At the cap |
|---|---|---|---|---|---|---|
| Togepi | egg gift | 1 | Oxide | Growl, Charm | Metronome 6, Sweet Kiss 10; as Togetic: Sweet Kiss 10, Yawn 15, Encore 19, Follow Me 24, Wish 28, AncientPower 33 | Togetic (from 10); Togekiss in Wake |
| Togepi | egg gift | 1 | Rewrite | Growl, Charm, Fairy Wind | Dazzling Gleam 2, Magical Leaf 4, Sweet Kiss 10; as Togetic: Sweet Kiss 10, Yawn 15, Encore 19, Follow Me 24, Wish 28, Air Slash 30, AncientPower 33 | Togetic (from 10); Togekiss in Wake |

## Hearthome City

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 33 | At the cap |
|---|---|---|---|---|---|---|
| Eevee | gift | 20 | Oxide | Tackle, Helping Hand, Sand-Attack, Growl | Quick Attack 22, Bite 29 | Leafeon (from 30) |
| Eevee | gift | 20 | Oxide | Tackle, Helping Hand, Sand-Attack, Growl | Quick Attack 22, Bite 29 | Glaceon (from 30) |
| Eevee | gift | 20 | Oxide | Tackle, Helping Hand, Sand-Attack, Growl | Quick Attack 22, Bite 29 | Eevee; Flareon in Maylene, Jolteon in Maylene, Vaporeon in Maylene, Espeon in Byron |
| Eevee | gift | 20 | Oxide | Tackle, Helping Hand, Sand-Attack, Growl | as Umbreon: Quick Attack 22, Confuse Ray 29 | Umbreon (from 20) |
| Eevee | gift | 20 | Oxide | Tackle, Helping Hand, Sand-Attack, Growl | Quick Attack 22, Bite 29; as Sylveon: Misty Terrain 32, Skill Swap 33 | Sylveon (from 32) |
| Eevee | gift | 20 | Rewrite | Tackle, Helping Hand, Sand-Attack | Quick Attack 22, Charm 27, Headbutt 28, Bite 29; as Leafeon: Razor Leaf 30, Synthesis 31 | Leafeon (from 30) |
| Eevee | gift | 20 | Rewrite | Tackle, Helping Hand, Sand-Attack | Quick Attack 22, Charm 27, Headbutt 28, Bite 29; as Glaceon: Icy Wind 30, Water Pulse 32 | Glaceon (from 30) |
| Eevee | gift | 20 | Rewrite | Tackle, Helping Hand, Sand-Attack | Quick Attack 22, Charm 27, Headbutt 28, Bite 29 | Eevee; Flareon in Maylene, Jolteon in Maylene, Vaporeon in Maylene, Espeon in Byron |
| Eevee | gift | 20 | Rewrite | Tackle, Helping Hand, Sand-Attack | as Umbreon: Pursuit 20, Quick Attack 22, Snarl 24, Trailblaze 26, Charm 27, Confuse Ray 29, Dark Pulse 31 | Umbreon (from 20) |
| Eevee | gift | 20 | Rewrite | Tackle, Helping Hand, Sand-Attack | Quick Attack 22, Charm 27, Headbutt 28, Bite 29; as Sylveon: Baby-Doll Eyes 32, Skill Swap 33 | Sylveon (from 32) |

## Mining Museum

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 33 | At the cap |
|---|---|---|---|---|---|---|
| Aerodactyl | fossil | 20 | Oxide | Bite, Scary Face, Roar, Agility | AncientPower 25, Crunch 33 | Aerodactyl |
| Aerodactyl | fossil | 20 | Rewrite | Supersonic, Bite, Scary Face, Agility | AncientPower 25, Wing Attack 27, Crunch 33 | Aerodactyl |
| Anorith | fossil | 20 | Oxide | Harden, Mud Sport, Water Gun, Metal Claw | Protect 25, AncientPower 31 | Anorith; Armaldo in Wake |
| Anorith | fossil | 20 | Rewrite | Scratch, Water Gun, Metal Claw | Leech Life 27, Block 29, AncientPower 31 | Anorith; Armaldo in Wake |
| Cranidos | fossil | 20 | both | Focus Energy, Pursuit, Take Down, Scary Face | Assurance 24, AncientPower 28; as Rampardos: Endeavor 30 | Rampardos (from 30) |
| Kabuto | fossil | 20 | Oxide | Harden, Absorb, Leer, Mud Shot | Sand-Attack 21, Endure 26, Aqua Jet 31 | Kabuto; Kabutops in Wake |
| Kabuto | fossil | 20 | Rewrite | Scratch, Mud Shot, Rock Slide | Sand-Attack 21, Endure 26, Bite 28, Aqua Jet 31 | Kabuto; Kabutops in Wake |
| Lileep | fossil | 20 | Oxide | Astonish, Constrict, Acid, Ingrain | Confuse Ray 22, Amnesia 29 | Lileep; Cradily in Wake |
| Lileep | fossil | 20 | Rewrite | Astonish, Acid, Giga Drain | Confuse Ray 22, AncientPower 27, Amnesia 29 | Lileep; Cradily in Wake |
| Omanyte | fossil | 20 | both | Bite, Water Gun, Rollout, Leer | Mud Shot 25, Brine 28 | Omanyte; Omastar in Wake |
| Shieldon | fossil | 20 | Oxide | Taunt, Metal Sound, Take Down, Iron Defense | Swagger 24, AncientPower 28; as Bastiodon: Block 30 | Bastiodon (from 30) |
| Shieldon | fossil | 20 | Rewrite | Taunt, Metal Sound, Take Down, Iron Defense | Swagger 24, Bulldoze 27, AncientPower 28, Iron Head 30; as Bastiodon: Block 30 | Bastiodon (from 30) |

## Mt. Coronet South

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 33 | At the cap |
|---|---|---|---|---|---|---|
| Barboach | old rod | 8 | Oxide | Mud-Slap, Mud Sport, Water Sport | Water Gun 10, Mud Bomb 14, Amnesia 18, Water Pulse 22, Magnitude 26; as Whiscash: Rest 33, Snore 33 | Whiscash (from 30) |
| Barboach | old rod | 8 | Rewrite | Mud-Slap, Scary Face, Water Sport | Water Gun 10, Mud Bomb 14, Amnesia 18, Rock Tomb 20, Water Pulse 22, Magnitude 26; as Whiscash: Bulldoze 30, Rest 33 | Whiscash (from 30) |
| Goldeen | old rod | 8 | Oxide | Peck, Tail Whip, Water Sport, Supersonic | Horn Attack 11, Water Pulse 17, Flail 21, Aqua Ring 27, Fury Attack 31 | Seaking (from 33) |
| Goldeen | old rod | 8 | Rewrite | Peck, Water Sport, Water Pulse, Flip Turn | Horn Attack 11, Agility 20, Flail 21, Aqua Ring 27; as Seaking: Bulldoze 33 | Seaking (from 33) |
| Corphish | old rod | 9 | Oxide | Bubble, Harden | ViceGrip 10, Leer 13, BubbleBeam 20, Protect 23, Knock Off 26; as Crawdaunt: Swift 30 | Crawdaunt (from 30) |
| Corphish | old rod | 9 | Rewrite | Bubble, Taunt, BubbleBeam | ViceGrip 10, Leer 13, Aerial Ace 17, Razor Shell 19, Knock Off 26; as Crawdaunt: Swift 30 | Crawdaunt (from 30) |
| Feebas | old rod | 9 | Oxide | Splash | Tackle 15, Flail 30 | Milotic (from 30) |
| Feebas | old rod | 9 | Rewrite | Swagger, Dragon Tail | Water Pulse 13, Tackle 15, Captivate 25, Flail 30; as Milotic: Twister 30, Recover 31, Aqua Tail 32, Aurora Beam 33 | Milotic (from 30) |
| Clamperl | old rod | 10 | Oxide | Clamp, Water Gun, Whirlpool, Iron Defense | as Huntail: Screech 10, Water Pulse 15, Scary Face 19, Ice Fang 24, Brine 28, Baton Pass 33 | Huntail (from 10) |
| Clamperl | old rod | 10 | Oxide | Clamp, Water Gun, Whirlpool, Iron Defense | as Gorebyss: Agility 10, Water Pulse 15, Amnesia 19, Aqua Ring 24, Captivate 28, Baton Pass 33 | Gorebyss (from 10) |
| Clamperl | old rod | 10 | Rewrite | Clamp, Water Gun, Whirlpool, Iron Defense | as Huntail: Screech 10, Water Pulse 15, Scary Face 19, Ice Fang 24, Brine 28 | Huntail (from 10) |
| Clamperl | old rod | 10 | Rewrite | Clamp, Water Gun, Whirlpool, Iron Defense | as Gorebyss: Agility 10, Water Pulse 15, Amnesia 19, Aqua Ring 24, Captivate 28, Baton Pass 33 | Gorebyss (from 10) |
| Glimmet | wild | 17 to 20 | Oxide | Smack Down, Acid Spray, AncientPower, Rock Polish | Stealth Rock 18, Venoshock 22, Selfdestruct 29, Rock Slide 33 | Glimmet; Glimmora in Maylene |
| Glimmet | wild | 17 to 20 | Rewrite | Smack Down, Acid Spray, AncientPower, Rock Polish | Stealth Rock 18, Mud Shot 20, Venoshock 22, Rock Slide 33 | Glimmet; Glimmora in Maylene |
| Bronzor | wild | 18 | Oxide | Confusion, Hypnosis, Imprison, Confuse Ray | Extrasensory 19, Iron Defense 26, Safeguard 30; as Bronzong: Block 33 | Bronzong (from 33) |
| Bronzor | wild | 18 | Rewrite | Hypnosis, Imprison, Confuse Ray, Bulldoze | Extrasensory 19, Smart Strike 21, Iron Defense 26, Safeguard 30; as Bronzong: Block 33 | Bronzong (from 33) |
| Makuhita | wild | 18 | Oxide | Arm Thrust, Vital Throw, Fake Out, Whirlwind | Knock Off 19, SmellingSalt 22; as Hariyama: Belly Drum 27, Force Palm 32 | Hariyama (from 24) |
| Makuhita | wild | 18 | Rewrite | Arm Thrust, Vital Throw, Fake Out, Whirlwind | Knock Off 19, SmellingSalt 22; as Hariyama: Belly Drum 27, Low Sweep 29, Force Palm 32 | Hariyama (from 24) |
| Mienfoo | wild | 18 to 19 | Oxide | Pound, Rock Smash, Fake Out, DoubleSlap | Force Palm 20, Bounce 22, Drain Punch 25, Vacuum Wave 32 | Mienfoo; Mienshao in Maylene |
| Mienfoo | wild | 18 to 19 | Rewrite | Rock Smash, Fake Out, DoubleSlap, Trailblaze | Agility 19, Force Palm 20, Bounce 22, Drain Punch 25, Vacuum Wave 32 | Mienfoo; Mienshao in Maylene |
| Nacli | wild | 18 to 19 | Oxide | Mud Shot, Smack Down, Rock Polish, Headbutt | Iron Defense 20; as Naclstack: Recover 30 | Naclstack (from 24); Garganacl in Maylene |
| Nacli | wild | 18 to 19 | Rewrite | Rock Throw, Mud Shot, Smack Down, Headbutt | Iron Defense 20; as Naclstack: Bulldoze 24, Rock Polish 27, Recover 30 | Naclstack (from 24); Garganacl in Maylene |
| Phanpy | wild | 18 | Oxide | Defense Curl, Flail, Take Down, Rollout | Natural Gift 19, Slam 24; as Donphan: Fury Attack 25, Assurance 31 | Donphan (from 25) |
| Phanpy | wild | 18 | Rewrite | Flail, Ice Shard, Take Down, Rollout | Natural Gift 19, Slam 24; as Donphan: Rapid Spin 25, Magnitude 26, Rock Tomb 28, Assurance 31 | Donphan (from 25) |
| Snorunt | wild | 18 | Oxide | Leer, Double Team, Bite, Icy Wind | Headbutt 19, Protect 22, Ice Fang 28, Crunch 31 | Snorunt; Glalie in Wake, Froslass in Byron |
| Snorunt | wild | 18 | Rewrite | Powder Snow, Leer, Bite, Icy Wind | Headbutt 19, Ominous Wind 22, Ice Fang 28, Crunch 31 | Snorunt; Glalie in Wake, Froslass in Byron |
| Zubat | wild | 18 to 19 | Oxide | Supersonic, Astonish, Bite, Wing Attack | Confuse Ray 21; as Golbat: Air Cutter 27, Mean Look 33 | Golbat (from 22); Crobat in Wake |
| Zubat | wild | 18 to 19 | Rewrite | Supersonic, Screech, Astonish, Bite | Confuse Ray 21; as Golbat: Air Cutter 27, Mean Look 33 | Golbat (from 22); Crobat in Wake |
| Carbink | wild | 19 | Oxide | Sharpen, Smack Down, Guard Split, Reflect | Flail 24, AncientPower 25, Rock Polish 25 | Carbink |
| Carbink | wild | 19 | Rewrite | Draining Kiss, Smack Down, Guard Split, Reflect | Bulldoze 20, Flail 24, AncientPower 25, Rock Polish 26, Rock Tomb 27, Dazzling Gleam 29 | Carbink |
| Seel | wild | 20 | both | Water Sport, Icy Wind, Encore, Ice Shard | Rest 21, Aqua Ring 23, Aurora Beam 27, Aqua Jet 31, Brine 33 | Seel; Dewgong in Maylene |
| Snom | wild | 20 | Oxide | Powder Snow, Struggle Bug | as Frosmoth: Bug Buzz 32 | Frosmoth (from 30) |
| Snom | wild | 20 | Rewrite | Powder Snow, Struggle Bug, Stun Spore | Fairy Wind 27; as Frosmoth: Stun Spore 30, Infestation 31, Bug Buzz 32, Defog 33 | Frosmoth (from 30) |

## Old Chateau

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 33 | At the cap |
|---|---|---|---|---|---|---|
| Gastly | wild | 14 to 17 | Oxide | Lick, Spite, Mean Look, Curse | Night Shade 15, Confuse Ray 19, Sucker Punch 22; as Haunter: Shadow Punch 25, Payback 28, Shadow Ball 33 | Haunter (from 25); Gengar in Wake |
| Gastly | wild | 14 to 17 | Rewrite | Lick, Spite, Mean Look, Curse | Night Shade 15, Sludge 17, Confuse Ray 19, Sucker Punch 22, Icy Wind 24; as Haunter: Shadow Punch 25, Payback 28, Shadow Ball 33 | Haunter (from 25); Gengar in Wake |
| Duskull | wild | 15 | Oxide | Night Shade, Disable, Foresight, Astonish | Confuse Ray 17, Shadow Sneak 22, Pursuit 25, Curse 30, Will-O-Wisp 33 | Duskull; Dusclops in Maylene |
| Duskull | wild | 15 | Rewrite | Night Shade, Disable, Foresight, Astonish | Confuse Ray 17, Shadow Sneak 22, Pursuit 25, Shadow Claw 27, Curse 30, Will-O-Wisp 33 | Duskull; Dusclops in Maylene |
| Litwick | wild | 15 | both | Smog, Confuse Ray, Fire Spin, Night Shade | Clear Smog 18, Will-O-Wisp 22, Flame Burst 26, Hex 30 | Litwick; Lampent in Wake |
| Misdreavus | wild | 15 to 16 | Oxide | Psywave, Spite, Astonish, Confuse Ray | nothing | Mismagius (from 15) |
| Misdreavus | wild | 15 to 16 | Rewrite | Psywave, Spite, Astonish, Confuse Ray | as Mismagius: Magical Leaf 17, Hex 23 | Mismagius (from 15) |
| Sinistea | wild | 15 to 17 | Oxide | Astonish, Withdraw, Aromatic Mist, Mega Drain | as Polteageist: Protect 18, Sucker Punch 24, Aromatherapy 30 | Polteageist (from 15) |
| Sinistea | wild | 15 to 17 | Oxide | Astonish, Withdraw, Aromatic Mist, Mega Drain | as Sinistcha: Foul Play 18, Mega Drain 24, Hex 30 | Sinistcha (from 15) |
| Sinistea | wild | 15 to 17 | Rewrite | Astonish, Withdraw, Mega Drain | as Polteageist: Nasty Plot 17, Magical Leaf 18, Sucker Punch 24, Hex 29, Aromatherapy 30 | Polteageist (from 15) |
| Sinistea | wild | 15 to 17 | Rewrite | Astonish, Withdraw, Mega Drain | as Sinistcha: Life Dew 15, Foul Play 18, Snarl 20, Mega Drain 24, Hex 30 | Sinistcha (from 15) |
| Yamask | wild | 16 to 17 | Oxide | Protect, Haze, Disable, Night Shade | Will-O-Wisp 18, Crafty Shield 20, Hex 20, Ominous Wind 25, Curse 32 | Yamask; Cofagrigus in Maylene, Runerigus in Candice |
| Yamask | wild | 16 to 17 | Rewrite | Astonish, Disable, Night Shade, Mud Shot | Will-O-Wisp 18, Hex 19, Crafty Shield 20, Ominous Wind 25, Curse 32 | Yamask; Cofagrigus in Maylene, Runerigus in Candice |
| Rotom | static battle | 20 | Oxide | ThunderShock, Confuse Ray, Uproar, Double Team | Shock Wave 22, Ominous Wind 29 | Rotom |
| Rotom | static battle | 20 | Rewrite | Thunder Wave, ThunderShock, Confuse Ray, Uproar | Shock Wave 22, Snarl 27, Ominous Wind 29 | Rotom |

## Route 206

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 33 | At the cap |
|---|---|---|---|---|---|---|
| Gligar | wild | 16 | Oxide | Sand-Attack, Harden, Knock Off, Quick Attack | Fury Cutter 20, Faint Attack 23, Screech 27, Slash 31 | Gligar; Gliscor in Wake |
| Gligar | wild | 16 | Rewrite | Harden, Knock Off, Bulldoze, Quick Attack | Rock Tomb 18, Fury Cutter 20, Faint Attack 23, Screech 27, Slash 31 | Gligar; Gliscor in Wake |
| Charcadet | wild | 17 | Oxide | Clear Smog, Fire Spin | Will-O-Wisp 20, Night Shade 30 | Charcadet; Armarouge in Byron |
| Charcadet | wild | 17 | Oxide | Clear Smog, Fire Spin | as Ceruledge: Night Shade 20, Flame Charge 24, Incinerate 28, Lava Plume 32 | Ceruledge (from 17) |
| Charcadet | wild | 17 | Rewrite | Clear Smog, Fire Spin, Lava Plume | Will-O-Wisp 20, Flame Charge 24, Night Shade 30 | Charcadet; Armarouge in Byron |
| Charcadet | wild | 17 | Rewrite | Clear Smog, Fire Spin, Lava Plume | as Ceruledge: Clear Smog 17, Fire Spin 18, Night Shade 20, Shadow Claw 22, Flame Charge 24, Bulldoze 27, Incinerate 28, Iron Defense 30, Lava Plume 32 | Ceruledge (from 17) |
| Fletchinder | wild | 17 | Oxide | Growl, Quick Attack, Aerial Ace, Flame Charge | Roost 22, Will-O-Wisp 27, Natural Gift 31 | Fletchinder; Talonflame in Maylene |
| Fletchinder | wild | 17 | Rewrite | Growl, Quick Attack, Aerial Ace, Flame Charge | Bite 19, Roost 22, Will-O-Wisp 27, Natural Gift 31 | Fletchinder; Talonflame in Maylene |
| Houndour | wild | 17 | Oxide | Howl, Smog, Roar, Bite | Odor Sleuth 22; as Houndoom: Fire Fang 32 | Houndoom (from 27) |
| Houndour | wild | 17 | Rewrite | Bite, Smog, Scary Face, Roar | Incinerate 20, Odor Sleuth 22; as Houndoom: Fire Fang 32 | Houndoom (from 27) |
| Ponyta | wild | 17 | Oxide | Tackle, Tail Whip, Ember, Flame Wheel | Stomp 19, Fire Spin 24, Take Down 28, Agility 33 | Ponyta; Rapidash in Wake |
| Ponyta | wild | 17 | Oxide | Tackle, Tail Whip, Ember, Flame Wheel | as Galarian Rapidash: Agility 20, Psybeam 25, Stomp 30 | Galarian Rapidash (from 17) |
| Ponyta | wild | 17 | Rewrite | Flame Charge, Ember, Flame Wheel, Bulldoze | Stomp 19, Agility 20, Fire Spin 24, Take Down 28, Headbutt 30 | Ponyta; Rapidash in Wake |
| Ponyta | wild | 17 | Rewrite | Flame Charge, Ember, Flame Wheel, Bulldoze | as Galarian Rapidash: Draining Kiss 17, Agility 20, Psybeam 25, Stomp 30 | Galarian Rapidash (from 17) |
| Stunky | wild | 17 | Oxide | Poison Gas, Screech, Fury Swipes, SmokeScreen | Feint 18, Slash 22, Toxic 27, Night Slash 32 | Stunky; Skuntank in Maylene |
| Stunky | wild | 17 | Rewrite | Focus Energy, Screech, Fury Swipes, SmokeScreen | Slash 22, Toxic 27, Venoshock 28, Metal Claw 30, Night Slash 32 | Stunky; Skuntank in Maylene |
| Bonsly | wild | 18 | both | Flail, Low Kick, Rock Throw, Mimic | Block 22, Faint Attack 25, Rock Tomb 30; as Sudowoodo: Rock Slide 33 | Sudowoodo (from 32) |
| Joltik | wild | 18 | Oxide | Thunder Wave, Spider Web, Electroweb, Bug Bite | Gastro Acid 23, Struggle Bug 26, Discharge 29 | Galvantula (from 30) |
| Joltik | wild | 18 | Rewrite | Thunder Wave, Spider Web, Electroweb, Bug Bite | Gastro Acid 23, Struggle Bug 26, Sucker Punch 28, Discharge 29; as Galvantula: Snarl 31 | Galvantula (from 30) |
| Onix | wild | 18 | Oxide | Screech, Rock Throw, Rage, Rock Tomb | as Steelix: Slam 25, Rock Polish 30, DragonBreath 33 | Steelix (from 18) |
| Onix | wild | 18 | Rewrite | Bulldoze, Screech, Curse, Bite | as Steelix: Metal Claw 19, Slam 25, DragonBreath 33 | Steelix (from 18) |
| Salandit | wild | 18 | Oxide | Ember, Sweet Scent, Venom Drench, Flame Burst | Dragon Rage 21, Toxic 24, Venoshock 29 | Salazzle (from 30) |
| Salandit | wild | 18 | Rewrite | Smog, Ember, Venom Drench, Flame Burst | Dragon Rage 21, Toxic 24, Mud Shot 27, Venoshock 29 | Salazzle (from 30) |
| Dwebble | wild | 19 | both | Block, Sand-Attack, Faint Attack, Slash | Rock Tomb 21, Bug Bite 24, Night Slash 27, X-Scissor 31 | Dwebble; Crustle in Maylene |
| Frogadier | wild | 19 | Oxide | Quick Attack, Lick, Water Pulse, Icy Wind | Faint Attack 20, Acrobatics 22, Low Kick 25, Waterfall 30 | Frogadier; Greninja in Maylene |
| Frogadier | wild | 19 | Rewrite | Lick, Water Pulse, Icy Wind, Thief | Faint Attack 20, Acrobatics 22, Low Kick 25, Waterfall 30 | Frogadier; Greninja in Maylene |
| Nacli | wild | 19 | Oxide | Mud Shot, Smack Down, Rock Polish, Headbutt | Iron Defense 20; as Naclstack: Recover 30 | Naclstack (from 24); Garganacl in Maylene |
| Nacli | wild | 19 | Rewrite | Rock Throw, Mud Shot, Smack Down, Headbutt | Iron Defense 20; as Naclstack: Bulldoze 24, Rock Polish 27, Recover 30 | Naclstack (from 24); Garganacl in Maylene |

## Route 208

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 33 | At the cap |
|---|---|---|---|---|---|---|
| Poliwag | old rod | 8 | Oxide | Water Sport, Bubble, Hypnosis | Water Gun 11, DoubleSlap 15, Body Slam 21, BubbleBeam 25; as Poliwhirl: BubbleBeam 27, Mud Shot 32 | Poliwhirl (from 25); Poliwrath in Maylene, Politoed in Wake |
| Poliwag | old rod | 8 | Rewrite | BubbleBeam, Mud Shot, Icy Wind, Hypnosis | DoubleSlap 15, Body Slam 21; as Poliwhirl: Bulldoze 25, BubbleBeam 27, Swagger 28, Mud Shot 32 | Poliwhirl (from 25); Poliwrath in Maylene, Politoed in Wake |
| Wailmer | old rod | 8 | Oxide | Splash, Growl, Water Gun | Rollout 11, Whirlpool 14, Astonish 17, Water Pulse 21, Mist 24, Rest 27, Brine 31 | Wailmer; Wailord in Wake |
| Wailmer | old rod | 8 | Rewrite | Water Gun, Bulldoze | Rollout 11, Whirlpool 14, Astonish 17, Water Pulse 21, Mist 24, Rest 27, Brine 31 | Wailmer; Wailord in Wake |
| Feebas | old rod | 9 | Oxide | Splash | Tackle 15, Flail 30 | Milotic (from 30) |
| Feebas | old rod | 9 | Rewrite | Swagger, Dragon Tail | Water Pulse 13, Tackle 15, Captivate 25, Flail 30; as Milotic: Twister 30, Recover 31, Aqua Tail 32, Aurora Beam 33 | Milotic (from 30) |
| Totodile | old rod | 9 | Oxide | Scratch, Leer, Water Gun, Rage | Bite 13, Scary Face 15; as Croconaw: Ice Fang 21, Flail 24, Crunch 30; as Feraligatr: Agility 30, Crunch 32 | Feraligatr (from 30) |
| Totodile | old rod | 9 | Rewrite | Scratch, Water Gun, Flip Turn | Bite 13, Scary Face 15; as Croconaw: Ice Fang 21, Flail 24, Crunch 30; as Feraligatr: Agility 30, Crunch 32 | Feraligatr (from 30) |
| Froakie | old rod | 10 | Oxide | Pound, Water Gun, Growl, Quick Attack | Lick 13, Water Pulse 14, Icy Wind 16; as Frogadier: Icy Wind 16, Faint Attack 20, Acrobatics 22, Low Kick 25, Waterfall 30 | Frogadier (from 16); Greninja in Maylene |
| Froakie | old rod | 10 | Rewrite | Pound, Water Gun, Quick Attack | Lick 13, Water Pulse 14, Icy Wind 16; as Frogadier: Icy Wind 16, Thief 19, Faint Attack 20, Acrobatics 22, Low Kick 25, Waterfall 30 | Frogadier (from 16); Greninja in Maylene |
| Fomantis | wild | 17 | Oxide | Fury Cutter, Growth, Razor Leaf, Ingrain | Sweet Scent 27, Slash 28, X-Scissor 30, Synthesis 31, Leaf Blade 32 | Fomantis; Lurantis in Maylene |
| Fomantis | wild | 17 | Rewrite | Leafage, Fury Cutter, Razor Leaf | Slash 28, X-Scissor 30, Synthesis 31, Leaf Blade 32 | Fomantis; Lurantis in Maylene |
| Budew | wild | 18 | Oxide | Water Sport, Stun Spore, Mega Drain, Worry Seed | as Roselia: Sweet Scent 31 | Roselia (from 30); Roserade in Wake |
| Budew | wild | 18 | Rewrite | Stun Spore, Mega Drain, Worry Seed, Venoshock | Confusion 20, Giga Drain 25; as Roselia: Poison Sting 30, Leech Seed 31, Magical Leaf 32, GrassWhistle 33 | Roselia (from 30); Roserade in Wake |
| Grubbin | wild | 18 | Oxide | Mud-Slap, String Shot, Bug Bite, Bite | as Charjabug: Spark 23, Sticky Web 29 | Charjabug (from 20); Vikavolt in Maylene |
| Grubbin | wild | 18 | Rewrite | Sticky Web, String Shot, Bug Bite, Bite | as Charjabug: Spark 23, Lunge 27, Sticky Web 29, Skitter Smack 31 | Charjabug (from 20); Vikavolt in Maylene |
| Mightyena | wild | 18 | Oxide | Howl, Sand-Attack, Bite, Odor Sleuth | Roar 22, Swagger 27, Assurance 32 | Mightyena |
| Mightyena | wild | 18 | Rewrite | Howl, Sand-Attack, Bite, Odor Sleuth | Trailblaze 19, Roar 22, Swagger 27, Assurance 32 | Mightyena |
| Pachirisu | wild | 18 | Oxide | Quick Attack, Charm, Spark, Endure | Swift 21, Sweet Kiss 25, Discharge 29, Super Fang 33 | Pachirisu |
| Pachirisu | wild | 18 | Rewrite | Quick Attack, Charm, Spark, Endure | Bite 19, Swift 21, Sweet Kiss 25, Discharge 29, Super Fang 33 | Pachirisu |
| Purrloin | wild | 18 | Oxide | Fake Out, Fury Swipes, Pursuit, Torment | as Liepard: Fake Out 22, Assurance 26, Hone Claws 27 | Liepard (from 20) |
| Purrloin | wild | 18 | Rewrite | Fury Swipes, Fake Out, Pursuit, Torment | as Liepard: Trailblaze 20, Fake Out 22, Assurance 26, Hone Claws 27 | Liepard (from 20) |
| Ralts | wild | 18 | Oxide | Confusion, Double Team, Teleport, Lucky Chant | as Kirlia: Magical Leaf 22, Calm Mind 25; as Gardevoir: Psychic 33 | Gardevoir (from 30) |
| Ralts | wild | 18 | Oxide | Confusion, Double Team, Teleport, Lucky Chant | as Kirlia: Magical Leaf 22, Calm Mind 25, Psychic 31 | Kirlia (from 20); Gallade in Byron |
| Ralts | wild | 18 | Rewrite | Growl, Draining Kiss, Confusion, Lucky Chant | Dazzling Gleam 19, Magical Leaf 20; as Kirlia: Magical Leaf 22, Calm Mind 25; as Gardevoir: Psychic 33 | Gardevoir (from 30) |
| Ralts | wild | 18 | Rewrite | Growl, Draining Kiss, Confusion, Lucky Chant | Dazzling Gleam 19, Magical Leaf 20; as Kirlia: Magical Leaf 22, Calm Mind 25, Psychic 31 | Kirlia (from 20); Gallade in Byron |
| Sewaddle | wild | 18 | Oxide | Tackle, String Shot, Bug Bite, Razor Leaf | as Leavanny: Helping Hand 32 | Leavanny (from 30) |
| Sewaddle | wild | 18 | Rewrite | Pounce, Sticky Web, Bug Bite, Razor Leaf | as Swadloon: Bite 20; as Leavanny: Fell Stinger 30, Helping Hand 32 | Leavanny (from 30) |
| Combee | wild | 19 | Oxide | Sweet Scent, Gust, Bug Bite | as Vespiquen: Power Gem 21, Heal Order 25, Toxic 27, Slash 31, Captivate 33 | Vespiquen (from 21) |
| Combee | wild | 19 | Rewrite | Gust, Pursuit, Swagger, Bug Bite | as Vespiquen: Power Gem 21, Poison Sting 22, Defend Order 23, Pursuit 24, Heal Order 25, Toxic 27, Slash 31, Captivate 33 | Vespiquen (from 21) |
| Fletchinder | wild | 19 | Oxide | Growl, Quick Attack, Aerial Ace, Flame Charge | Roost 22, Will-O-Wisp 27, Natural Gift 31 | Fletchinder; Talonflame in Maylene |
| Fletchinder | wild | 19 | Rewrite | Quick Attack, Aerial Ace, Flame Charge, Bite | Roost 22, Will-O-Wisp 27, Natural Gift 31 | Fletchinder; Talonflame in Maylene |
| Smoliv | wild | 19 | Oxide | Growth, Razor Leaf, Helping Hand, Flail | Mega Drain 20, Grassy Terrain 23; as Dolliv: Seed Bomb 29 | Dolliv (from 25); Arboliva in Maylene |
| Smoliv | wild | 19 | Rewrite | Terrain Pulse, Razor Leaf, Helping Hand, Flail | Mega Drain 20; as Dolliv: Charm 25, Mud Shot 26, Seed Bomb 29 | Dolliv (from 25); Arboliva in Maylene |
| Steenee | wild | 19 | Oxide | Play Nice, Rapid Spin, Razor Leaf, Sweet Scent | Magical Leaf 21, Teeter Dance 23, Stomp 25, Aromatic Mist 32; as Tsareena: Low Sweep 32 | Tsareena (from 32) |
| Steenee | wild | 19 | Rewrite | Play Nice, Rapid Spin, Razor Leaf, Draining Kiss | Magical Leaf 21, Teeter Dance 23, Stomp 25; as Tsareena: Low Sweep 32, Swagger 33 | Tsareena (from 32) |
| Carnivine | wild | 20 | Oxide | Growth, Bite, Vine Whip, Sweet Scent | Ingrain 21, Faint Attack 27, Stockpile 31, Spit Up 31, Swallow 31 | Carnivine |
| Carnivine | wild | 20 | Rewrite | Bind, Bite, Vine Whip | Faint Attack 27, Swallow 29, Leaf Tornado 30, Stockpile 31, Spit Up 32, Swagger 33 | Carnivine |
| Grovyle | wild | 20 | Oxide | Absorb, Quick Attack, Fury Cutter, Pursuit | Screech 23, Leaf Blade 29 | Grovyle; Sceptile in Maylene |
| Grovyle | wild | 20 | Rewrite | Leer, Quick Attack, Fury Cutter, Pursuit | Screech 23, Leaf Blade 29 | Grovyle; Sceptile in Maylene |
| Happiny | wild | 20 | Oxide | Charm, Copycat, Refresh, Sweet Kiss | as Chansey: Minimize 20, Sing 23, Fling 27, Defense Curl 31 | Chansey (from 20); Blissey in Wake |
| Happiny | wild | 20 | Rewrite | Pound, Charm, Refresh, Sweet Kiss | as Chansey: Minimize 20, Sing 23, Chilling Water 25, Fling 27, Swift 29, Defense Curl 31 | Chansey (from 20); Blissey in Wake |

## Wayward Cave

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 33 | At the cap |
|---|---|---|---|---|---|---|
| Carbink | wild | 17 to 20 | Oxide | Rock Throw, Sharpen, Smack Down, Guard Split | Reflect 18, Flail 24, AncientPower 25, Rock Polish 25 | Carbink |
| Carbink | wild | 17 to 20 | Rewrite | Rock Throw, Draining Kiss, Smack Down, Guard Split | Reflect 18, Bulldoze 20, Flail 24, AncientPower 25, Rock Polish 26, Rock Tomb 27, Dazzling Gleam 29 | Carbink |
| Phanpy | wild | 17 to 20 | Oxide | Defense Curl, Flail, Take Down, Rollout | Natural Gift 19, Slam 24; as Donphan: Fury Attack 25, Assurance 31 | Donphan (from 25) |
| Phanpy | wild | 17 to 20 | Rewrite | Flail, Ice Shard, Take Down, Rollout | Natural Gift 19, Slam 24; as Donphan: Rapid Spin 25, Magnitude 26, Rock Tomb 28, Assurance 31 | Donphan (from 25) |
| Bronzor | wild | 18 to 19 | Oxide | Confusion, Hypnosis, Imprison, Confuse Ray | Extrasensory 19, Iron Defense 26, Safeguard 30; as Bronzong: Block 33 | Bronzong (from 33) |
| Bronzor | wild | 18 to 19 | Rewrite | Hypnosis, Imprison, Confuse Ray, Bulldoze | Extrasensory 19, Smart Strike 21, Iron Defense 26, Safeguard 30; as Bronzong: Block 33 | Bronzong (from 33) |
| Geodude | wild | 18 | Oxide | Rock Polish, Rock Throw, Magnitude, Selfdestruct | Rollout 22, Rock Blast 25; as Graveler: Rock Blast 27, Earthquake 33 | Graveler (from 25); Golem in Wake |
| Geodude | wild | 18 | Rewrite | Bulldoze, Rock Throw, Magnitude, Rock Polish | Rollout 22, Rock Blast 25; as Graveler: Karate Chop 25, Rock Blast 27, Rock Tomb 29, Earthquake 33 | Graveler (from 25); Golem in Wake |
| Gible | wild | 18 | Oxide | Tackle, Sand-Attack, Dragon Rage, Take Down | Sand Tomb 19; as Gabite: Slash 28, Dragon Claw 33 | Gabite (from 24); Garchomp in Byron |
| Gible | wild | 18 | Rewrite | Tackle, Sand-Attack, Dragon Rage, Take Down | Sand Tomb 19, Block 20, Dragon Claw 21, Bite 23; as Gabite: Slash 28, Dragon Claw 33 | Gabite (from 24); Garchomp in Byron |
| Glimmet | wild | 18 to 19 | Oxide | Acid Spray, AncientPower, Rock Polish, Stealth Rock | Venoshock 22, Selfdestruct 29, Rock Slide 33 | Glimmet; Glimmora in Maylene |
| Glimmet | wild | 18 to 19 | Rewrite | Acid Spray, AncientPower, Rock Polish, Stealth Rock | Mud Shot 20, Venoshock 22, Rock Slide 33 | Glimmet; Glimmora in Maylene |
| Houndour | wild | 18 | Oxide | Howl, Smog, Roar, Bite | Odor Sleuth 22; as Houndoom: Fire Fang 32 | Houndoom (from 27) |
| Houndour | wild | 18 | Rewrite | Bite, Smog, Scary Face, Roar | Incinerate 20, Odor Sleuth 22; as Houndoom: Fire Fang 32 | Houndoom (from 27) |
| Meditite | wild | 18 | Oxide | Confusion, Detect, Hidden Power, Mind Reader | Feint 22, Calm Mind 25, Force Palm 29, Hi Jump Kick 32 | Meditite; Medicham in Maylene |
| Meditite | wild | 18 | Rewrite | Confusion, Hidden Power, Force Palm, Mind Reader | Rock Throw 20, Swagger 22, Hi Jump Kick 32 | Meditite; Medicham in Maylene |
| Mightyena | wild | 18 | Oxide | Howl, Sand-Attack, Bite, Odor Sleuth | Roar 22, Swagger 27, Assurance 32 | Mightyena |
| Mightyena | wild | 18 | Rewrite | Howl, Sand-Attack, Bite, Odor Sleuth | Trailblaze 19, Roar 22, Swagger 27, Assurance 32 | Mightyena |
| Nosepass | wild | 18 | Oxide | Tackle, Harden, Rock Throw | Block 19, Thunder Wave 25, Rock Slide 31 | Probopass (from 32) |
| Nosepass | wild | 18 | Rewrite | Smack Down, Taunt, Rock Tomb, Bulldoze | Block 19, Thunder Wave 25, Rock Slide 31; as Probopass: Iron Defense 32, Magnet Bomb 33 | Probopass (from 32) |
| Sandygast | wild | 18 to 19 | both | Astonish, Sand Tomb, Sand-Attack, Mega Drain | Bulldoze 24, Hypnosis 28 | Sandygast; Palossand in Wake |
| Zubat | wild | 18 to 19 | Oxide | Supersonic, Astonish, Bite, Wing Attack | Confuse Ray 21; as Golbat: Air Cutter 27, Mean Look 33 | Golbat (from 22); Crobat in Wake |
| Zubat | wild | 18 to 19 | Rewrite | Supersonic, Screech, Astonish, Bite | Confuse Ray 21; as Golbat: Air Cutter 27, Mean Look 33 | Golbat (from 22); Crobat in Wake |
| Dwebble | wild | 19 | both | Block, Sand-Attack, Faint Attack, Slash | Rock Tomb 21, Bug Bite 24, Night Slash 27, X-Scissor 31 | Dwebble; Crustle in Maylene |
| Hippopotas | wild | 19 | Oxide | Sand-Attack, Bite, Yawn, Take Down | Sand Tomb 25, Crunch 31 | Hippopotas; Hippowdon in Maylene |
| Hippopotas | wild | 19 | Rewrite | Sand-Attack, Bite, Yawn, Take Down | Sand Tomb 25, Bulldoze 27, Crunch 31 | Hippopotas; Hippowdon in Maylene |
| Onix | wild | 19 | Oxide | Screech, Rock Throw, Rage, Rock Tomb | as Steelix: Slam 25, Rock Polish 30, DragonBreath 33 | Steelix (from 19) |
| Onix | wild | 19 | Rewrite | Screech, Curse, Bite, Breaking Swipe | as Steelix: Metal Claw 19, Slam 25, DragonBreath 33 | Steelix (from 19) |
| Stunky | wild | 19 | Oxide | Screech, Fury Swipes, SmokeScreen, Feint | Slash 22, Toxic 27, Night Slash 32 | Stunky; Skuntank in Maylene |
| Stunky | wild | 19 | Rewrite | Focus Energy, Screech, Fury Swipes, SmokeScreen | Slash 22, Toxic 27, Venoshock 28, Metal Claw 30, Night Slash 32 | Stunky; Skuntank in Maylene |
| Bonsly | wild | 20 | both | Flail, Low Kick, Rock Throw, Mimic | Block 22, Faint Attack 25, Rock Tomb 30; as Sudowoodo: Rock Slide 33 | Sudowoodo (from 32) |
| Larvitar | wild | 20 | Oxide | Leer, Screech, Rock Slide, Scary Face | Thrash 23, Dark Pulse 28 | Pupitar (from 30); Tyranitar in Candice |
| Larvitar | wild | 20 | Rewrite | Leer, Screech, Rock Slide, Scary Face | Dark Pulse 28, StompingTantrum 30 | Pupitar (from 30); Tyranitar in Candice |
| Nacli | wild | 20 | Oxide | Smack Down, Rock Polish, Headbutt, Iron Defense | as Naclstack: Recover 30 | Naclstack (from 24); Garganacl in Maylene |
| Nacli | wild | 20 | Rewrite | Mud Shot, Smack Down, Headbutt, Iron Defense | as Naclstack: Bulldoze 24, Rock Polish 27, Recover 30 | Naclstack (from 24); Garganacl in Maylene |

## Honey trees

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 33 | At the cap |
|---|---|---|---|---|---|---|
| Aipom | honey | 14 | Oxide | Tail Whip, Sand-Attack, Astonish, Baton Pass | Tickle 15, Fury Swipes 18, Swift 22, Screech 25, Agility 29, Double Hit 32; as Ambipom: Double Hit 32 | Ambipom (from 32) |
| Aipom | honey | 14 | Rewrite | Tail Whip, Sand-Attack, Astonish, Baton Pass | Tickle 15, Fury Swipes 18, Bite 20, Swift 22, Screech 25, Agility 29, Double Hit 32; as Ambipom: Double Hit 32 | Ambipom (from 32) |
| Burmy | honey | 14 | Oxide | Protect, Tackle | Bug Bite 15, Hidden Power 20; as Wormadam: Hidden Power 20, Confusion 23, Razor Leaf 26, Growth 29, Psybeam 32 | Wormadam (from 20) |
| Burmy | honey | 14 | Oxide | Protect, Tackle | Bug Bite 15, Hidden Power 20; as Mothim: Hidden Power 20, Confusion 23, Gust 26, PoisonPowder 29, Psybeam 32 | Mothim (from 20) |
| Burmy | honey | 14 | Rewrite | Roost, Confusion, Tackle | Bug Bite 15, Hidden Power 20; as Wormadam: Hidden Power 20, Confusion 23, Razor Leaf 26, Leech Life 28, Psybeam 32 | Wormadam (from 20) |
| Burmy | honey | 14 | Rewrite | Roost, Confusion, Tackle | Bug Bite 15, Hidden Power 20; as Mothim: Hidden Power 20, Confusion 23, Gust 26, PoisonPowder 29, Psybeam 32 | Mothim (from 20) |
| Combee | honey | 14 | Oxide | Sweet Scent, Gust, Bug Bite | as Vespiquen: Power Gem 21, Heal Order 25, Toxic 27, Slash 31, Captivate 33 | Vespiquen (from 21) |
| Combee | honey | 14 | Rewrite | Gust, Pursuit, Swagger, Bug Bite | as Vespiquen: Power Gem 21, Poison Sting 22, Defend Order 23, Pursuit 24, Heal Order 25, Toxic 27, Slash 31, Captivate 33 | Vespiquen (from 21) |
| Fomantis | honey | 14 | Oxide | Fury Cutter, Growth, Razor Leaf, Ingrain | Sweet Scent 27, Slash 28, X-Scissor 30, Synthesis 31, Leaf Blade 32 | Fomantis; Lurantis in Maylene |
| Fomantis | honey | 14 | Rewrite | Leafage, Fury Cutter, Razor Leaf | Slash 28, X-Scissor 30, Synthesis 31, Leaf Blade 32 | Fomantis; Lurantis in Maylene |
| Grubbin | honey | 14 | Oxide | ViceGrip, Mud-Slap, String Shot, Bug Bite | Bite 15; as Charjabug: Spark 23, Sticky Web 29 | Charjabug (from 20); Vikavolt in Maylene |
| Grubbin | honey | 14 | Rewrite | Mud-Slap, Sticky Web, String Shot, Bug Bite | Bite 15; as Charjabug: Spark 23, Lunge 27, Sticky Web 29, Skitter Smack 31 | Charjabug (from 20); Vikavolt in Maylene |
| Heracross | honey | 14 | Oxide | Horn Attack, Endure, Fury Attack, Aerial Ace | Brick Break 19, Counter 25, Take Down 31 | Heracross |
| Heracross | honey | 14 | Rewrite | Tackle, Horn Attack, Endure, Aerial Ace | Pounce 17, Brick Break 19, Counter 25, Rock Tomb 27, Take Down 31 | Heracross |
| Joltik | honey | 14 | Oxide | Absorb, Fury Cutter, Thunder Wave, Spider Web | Electroweb 15, Bug Bite 18, Gastro Acid 23, Struggle Bug 26, Discharge 29 | Galvantula (from 30) |
| Joltik | honey | 14 | Rewrite | String Shot, Fury Cutter, Thunder Wave, Spider Web | Electroweb 15, Bug Bite 18, Gastro Acid 23, Struggle Bug 26, Sucker Punch 28, Discharge 29; as Galvantula: Snarl 31 | Galvantula (from 30) |
| Munchlax | honey | 14 | Oxide | Tackle, Defense Curl, Amnesia, Lick | Recycle 17, Screech 20, Stockpile 25, Swallow 28, Body Slam 33 | Munchlax; Snorlax in Maylene |
| Munchlax | honey | 14 | Rewrite | Odor Sleuth, Tackle, Amnesia, Lick | Recycle 17, Belly Drum 18, Screech 20, Headbutt 22, Rest 24, Stockpile 25, Swallow 28, Body Slam 33 | Munchlax; Snorlax in Maylene |
| Nuzleaf | honey | 14 | Oxide | Pound, Harden, Growth, Nature Power | nothing | Shiftry (from 14) |
| Nuzleaf | honey | 14 | Rewrite | Razor Leaf, Pound, Harden, Payback | as Shiftry: Silver Wind 17 | Shiftry (from 14) |
| Sewaddle | honey | 14 | Oxide | Tackle, String Shot, Bug Bite, Razor Leaf | as Leavanny: Helping Hand 32 | Leavanny (from 30) |
| Sewaddle | honey | 14 | Rewrite | Pounce, Sticky Web, Bug Bite, Razor Leaf | as Swadloon: Bite 20; as Leavanny: Fell Stinger 30, Helping Hand 32 | Leavanny (from 30) |
| Shroomish | honey | 14 | Oxide | Absorb, Tackle, Stun Spore, Leech Seed | Mega Drain 17, Headbutt 21; as Breloom: Mach Punch 23, Counter 25, Force Palm 29, Sky Uppercut 33 | Breloom (from 23) |
| Shroomish | honey | 14 | Rewrite | Magical Leaf, Tackle, Stun Spore, Leech Seed | Mega Drain 17, Headbutt 21; as Breloom: Mach Punch 23, Counter 25, Bulldoze 27, Force Palm 29, Sky Uppercut 33 | Breloom (from 23) |
| Steenee | honey | 14 | Oxide | DoubleSlap, Play Nice, Rapid Spin, Razor Leaf | Sweet Scent 17, Magical Leaf 21, Teeter Dance 23, Stomp 25, Aromatic Mist 32; as Tsareena: Low Sweep 32 | Tsareena (from 32) |
| Steenee | honey | 14 | Rewrite | DoubleSlap, Play Nice, Rapid Spin, Razor Leaf | Draining Kiss 17, Magical Leaf 21, Teeter Dance 23, Stomp 25; as Tsareena: Low Sweep 32, Swagger 33 | Tsareena (from 32) |

# Wake's split: what each catch knows and learns

Written by `tools/oxide/balance/learncheck.py sheets` for check 6 of the learnset baseline (`docs/oxide/learnset-checks.md`). One table per capture area first offered in Wake's split, whose cap is 44. Each Pokemon is read at the lowest level it is found at there. "Knows at capture" is the last four moves its list gives by that level; "learns by level-up" is every entry it reaches after capture up to 44, evolving on time, with each later stage's moves under its name; "at the cap" is the stage it can be by then and the next one after. A row marked v3 shows learnset v3 (unlanded, `origin/balance-learngen-v2`) where it differs from Oxide's lists; a row marked both is the same in each. Relearner-only moves and egg moves are left out. Nothing here is in the game data.

## Great Marsh

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 44 | At the cap |
|---|---|---|---|---|---|---|
| Barboach | old rod | 12 to 13 | Oxide | Mud-Slap, Mud Sport, Water Sport, Water Gun | Mud Bomb 14, Amnesia 18, Water Pulse 22, Magnitude 26; as Whiscash: Rest 33, Snore 33, Aqua Tail 39 | Whiscash (from 30) |
| Barboach | old rod | 12 to 13 | v3 | Mud-Slap, Mud Sport, Water Sport, Water Gun | Mud Bomb 14, Amnesia 18, Water Pulse 22, Magnitude 26; as Whiscash: Rest 33, Aqua Tail 39 | Whiscash (from 30) |
| Carvanha | old rod | 12 to 13 | Oxide | Bite, Rage, Focus Energy, Scary Face | Ice Fang 16, Screech 18, Swagger 21, Assurance 26, Crunch 28; as Sharpedo: Slash 30, Aqua Jet 34, Taunt 40 | Sharpedo (from 30) |
| Carvanha | old rod | 12 to 13 | v3 | Bite, Water Gun, Focus Energy, Scary Face | Screech 18, Swagger 21, Assurance 26, Crunch 28; as Sharpedo: Slash 30, Aqua Jet 34, Taunt 40 | Sharpedo (from 30) |
| Goldeen | old rod | 12 to 13 | Oxide | Tail Whip, Water Sport, Supersonic, Horn Attack | Water Pulse 17, Flail 21, Aqua Ring 27, Fury Attack 31; as Seaking: Waterfall 40 | Seaking (from 33) |
| Goldeen | old rod | 12 to 13 | v3 | Tail Whip, Water Sport, Supersonic, Horn Attack | Water Pulse 17, Flail 21, Aqua Ring 27; as Seaking: Waterfall 40 | Seaking (from 33) |
| Krabby | old rod | 12 to 14 | both | Bubble, ViceGrip, Leer, Harden | BubbleBeam 15, Mud Shot 19, Metal Claw 21, Stomp 25; as Kingler: Protect 32, Guillotine 37, Slam 44 | Kingler (from 28) |
| Lotad | old rod | 12 to 13 | Oxide | Growl, Absorb, Nature Power, Mist | nothing | Ludicolo (from 14) |
| Lotad | old rod | 12 to 13 | v3 | Growl, Water Gun, Nature Power, Mist | nothing | Ludicolo (from 14) |
| Wingull | old rod | 12 to 13 | Oxide | Growl, Water Gun, Supersonic, Wing Attack | Mist 16, Water Pulse 19, Quick Attack 24; as Pelipper: Protect 25, Roost 31, Stockpile 38, Swallow 38, Spit Up 38, Fling 43 | Pelipper (from 25) |
| Wingull | old rod | 12 to 13 | v3 | Growl, Water Gun, Supersonic, Wing Attack | Mist 16, Water Pulse 19, Quick Attack 24; as Pelipper: Protect 25, Stockpile 38, Swallow 38, Spit Up 38, Fling 43 | Pelipper (from 25) |
| Wooper | old rod | 12 to 13 | Oxide | Water Gun, Tail Whip, Mud Sport, Mud Shot | Slam 15, Mud Bomb 19; as Quagsire: Amnesia 24, Yawn 31, Earthquake 36 | Quagsire (from 20) |
| Wooper | old rod | 12 to 13 | Oxide | Water Gun, Tail Whip, Mud Sport, Mud Shot | as Clodsire: Poison Tail 12, Slam 16, Yawn 21, Bulldoze 24, Poison Jab 30, Megahorn 36, Toxic 40 | Clodsire (from 12) |
| Wooper | old rod | 12 to 13 | v3 | Water Gun, Tail Whip, Mud Sport, Mud Shot | Slam 15, Mud Bomb 19; as Quagsire: Amnesia 24, Yawn 31, Earthquake 44 | Quagsire (from 20) |
| Wooper | old rod | 12 to 13 | v3 | Water Gun, Tail Whip, Mud Sport, Mud Shot | as Clodsire: Mud Bomb 19, Yawn 21, Bulldoze 24, Poison Jab 36, Slam 37, Megahorn 39, Sludge Bomb 39, Toxic 40, Haze 43, Earthquake 44 | Clodsire (from 12) |
| Poliwag | old rod | 13 | both | Water Sport, Bubble, Hypnosis, Water Gun | DoubleSlap 15, Body Slam 21, BubbleBeam 25; as Poliwrath: DynamicPunch 43 | Poliwrath (from 25) |
| Poliwag | old rod | 13 | both | Water Sport, Bubble, Hypnosis, Water Gun | DoubleSlap 15, Body Slam 21, BubbleBeam 25; as Politoed: Swagger 27, Bounce 37 | Politoed (from 25) |
| Qwilfish | old rod | 13 | Oxide | Poison Sting, Harden, Minimize, Water Gun | Rollout 17, Toxic Spikes 21, Stockpile 25, Spit Up 25, Revenge 29, Brine 33, Pin Missile 37, Take Down 41 | Qwilfish |
| Qwilfish | old rod | 13 | v3 | Poison Sting, Harden, Minimize, Water Gun | Toxic Spikes 21, Stockpile 25, Spit Up 25, Revenge 29, Brine 33, Pin Missile 37, Take Down 41 | Qwilfish |
| Froakie | old rod | 14 | Oxide | Growl, Quick Attack, Lick, Water Pulse | Icy Wind 16; as Frogadier: Icy Wind 16, Faint Attack 20, Acrobatics 22, Low Kick 25, Waterfall 30, Fling 35; as Greninja: Scald 37, Dark Pulse 40, Extrasensory 43 | Greninja (from 36) |
| Froakie | old rod | 14 | v3 | Growl, Quick Attack, Lick, Water Pulse | Icy Wind 16; as Frogadier: Icy Wind 16, Faint Attack 20, Acrobatics 22, Low Kick 25, Fling 35; as Greninja: Water Shuriken on evolving, Night Slash on evolving, Scald 37, Dark Pulse 40, Extrasensory 43 | Greninja (from 36) |
| Psyduck | old rod | 14 | both | Scratch, Tail Whip, Water Gun, Disable | Confusion 18, Water Pulse 22, Fury Swipes 27, Screech 31; as Golduck: Psych Up 37, Zen Headbutt 44 | Golduck (from 33) |
| Totodile | old rod | 14 | Oxide | Leer, Water Gun, Rage, Bite | Scary Face 15; as Croconaw: Ice Fang 21, Flail 24, Crunch 30; as Feraligatr: Agility 30, Crunch 32, Slash 37 | Feraligatr (from 30) |
| Totodile | old rod | 14 | v3 | Scratch, Leer, Water Gun, Bite | Scary Face 15; as Croconaw: Flail 24, Crunch 30; as Feraligatr: Agility 30, Crunch 32, Slash 37 | Feraligatr (from 30) |
| Barboach | good rod | 20 to 22 | Oxide | Water Sport, Water Gun, Mud Bomb, Amnesia | Water Pulse 22, Magnitude 26; as Whiscash: Rest 33, Snore 33, Aqua Tail 39 | Whiscash (from 30) |
| Barboach | good rod | 20 to 22 | v3 | Water Sport, Water Gun, Mud Bomb, Amnesia | Water Pulse 22, Magnitude 26; as Whiscash: Rest 33, Aqua Tail 39 | Whiscash (from 30) |
| Corphish | good rod | 20 to 22 | both | Harden, ViceGrip, Leer, BubbleBeam | Protect 23, Knock Off 26; as Crawdaunt: Swift 30, Taunt 34, Night Slash 39, Crabhammer 44 | Crawdaunt (from 30) |
| Dewpider | good rod | 20 | Oxide | Infestation, Bite, Aqua Ring, BubbleBeam | Bug Bite 21; as Araquanid: Headbutt 26, Soak 31, Dive 36, Lunge 41 | Araquanid (from 22) |
| Dewpider | good rod | 20 | v3 | Water Gun, Bite, Aqua Ring, BubbleBeam | Bug Bite 21; as Araquanid: Headbutt 26, Soak 31, Dive 36, Lunge 41 | Araquanid (from 22) |
| Frillish | good rod | 20 to 22 | both | Night Shade, Ominous Wind, Water Pulse, Imprison | Confuse Ray 25, Hex 30, Brine 34, Pain Split 39 | Jellicent (from 40) |
| Lotad | good rod | 20 to 22 | both | Nature Power, Mist, Natural Gift, Mega Drain | nothing | Ludicolo (from 21) |
| Slowpoke | good rod | 20 to 24 | Oxide | Growl, Water Gun, Confusion, Disable | Headbutt 25, Water Pulse 29, Zen Headbutt 34; as Slowbro: Withdraw 37, Slack Off 41 | Slowbro (from 37) |
| Slowpoke | good rod | 20 to 24 | Oxide | Growl, Water Gun, Confusion, Disable | as Slowking: Disable 20, Headbutt 25, Water Pulse 29, Zen Headbutt 34, Nasty Plot 39, Swagger 43 | Slowking (from 20) |
| Slowpoke | good rod | 20 to 24 | v3 | Growl, Water Gun, Confusion, Disable | Headbutt 25, Body Slam 26, Water Pulse 29, Zen Headbutt 30, Dive 33; as Slowbro: Withdraw 37, Psychic 44 | Slowbro (from 37) |
| Slowpoke | good rod | 20 to 24 | v3 | Growl, Water Gun, Confusion, Disable | as Slowking: Disable 20, Headbutt 25, Water Pulse 29, Zen Headbutt 34, Nasty Plot 39, Swagger 43, Psychic 44 | Slowking (from 20) |
| Surskit | good rod | 20 | Oxide | Bubble, Quick Attack, Sweet Scent, Water Sport | as Masquerain: Gust 22, Scary Face 26, Stun Spore 33, Silver Wind 40 | Masquerain (from 22) |
| Surskit | good rod | 20 | v3 | Bubble, Quick Attack, Sweet Scent, Water Sport | as Masquerain: Scary Face 26, Stun Spore 33, Silver Wind 40 | Masquerain (from 22) |
| Wooper | good rod | 20 to 22 | Oxide | Mud Sport, Mud Shot, Slam, Mud Bomb | as Quagsire: Amnesia 24, Yawn 31, Earthquake 36 | Quagsire (from 21) |
| Wooper | good rod | 20 to 22 | Oxide | Mud Sport, Mud Shot, Slam, Mud Bomb | as Clodsire: Yawn 21, Bulldoze 24, Poison Jab 30, Megahorn 36, Toxic 40 | Clodsire (from 20) |
| Wooper | good rod | 20 to 22 | v3 | Mud Sport, Mud Shot, Slam, Mud Bomb | as Quagsire: Amnesia 24, Yawn 31, Earthquake 44 | Quagsire (from 21) |
| Wooper | good rod | 20 to 22 | v3 | Mud Sport, Mud Shot, Slam, Mud Bomb | as Clodsire: Yawn 21, Bulldoze 24, Poison Jab 36, Slam 37, Megahorn 39, Sludge Bomb 39, Toxic 40, Haze 43, Earthquake 44 | Clodsire (from 20) |
| Carvanha | good rod | 22 | Oxide | Scary Face, Ice Fang, Screech, Swagger | Assurance 26, Crunch 28; as Sharpedo: Slash 30, Aqua Jet 34, Taunt 40 | Sharpedo (from 30) |
| Carvanha | good rod | 22 | v3 | Focus Energy, Scary Face, Screech, Swagger | Assurance 26, Crunch 28; as Sharpedo: Slash 30, Aqua Jet 34, Taunt 40 | Sharpedo (from 30) |
| Frogadier | good rod | 22 to 24 | Oxide | Water Pulse, Icy Wind, Faint Attack, Acrobatics | Low Kick 25, Waterfall 30, Fling 35; as Greninja: Scald 37, Dark Pulse 40, Extrasensory 43 | Greninja (from 36) |
| Frogadier | good rod | 22 to 24 | v3 | Water Pulse, Icy Wind, Faint Attack, Acrobatics | Low Kick 25, Fling 35; as Greninja: Water Shuriken on evolving, Night Slash on evolving, Scald 37, Dark Pulse 40, Extrasensory 43 | Greninja (from 36) |
| Lombre | good rod | 22 | both | Nature Power, Fake Out, Fury Swipes, Water Sport | nothing | Ludicolo (from 22) |
| Masquerain | good rod | 22 | Oxide | Quick Attack, Sweet Scent, Water Sport, Gust | Scary Face 26, Stun Spore 33, Silver Wind 40 | Masquerain |
| Masquerain | good rod | 22 | v3 | Bubble, Quick Attack, Sweet Scent, Water Sport | Scary Face 26, Stun Spore 33, Silver Wind 40 | Masquerain |
| Quagsire | good rod | 22 | Oxide | Mud Sport, Mud Shot, Slam, Mud Bomb | Amnesia 24, Yawn 31, Earthquake 36 | Quagsire |
| Quagsire | good rod | 22 | v3 | Mud Sport, Mud Shot, Slam, Mud Bomb | Amnesia 24, Yawn 31, Earthquake 44 | Quagsire |
| Clamperl | good rod | 24 | Oxide | Clamp, Water Gun, Whirlpool, Iron Defense | as Huntail: Ice Fang 24, Brine 28, Baton Pass 33, Dive 37, Crunch 42 | Huntail (from 24) |
| Clamperl | good rod | 24 | Oxide | Clamp, Water Gun, Whirlpool, Iron Defense | as Gorebyss: Aqua Ring 24, Captivate 28, Baton Pass 33, Dive 37, Psychic 42 | Gorebyss (from 24) |
| Clamperl | good rod | 24 | v3 | Water Gun, Iron Defense | as Huntail: Brine 28, Ice Fang 32, Baton Pass 33, Dive 37, Crunch 42 | Huntail (from 24) |
| Clamperl | good rod | 24 | v3 | Water Gun, Iron Defense | as Gorebyss: Aqua Ring 24, Captivate 28, Baton Pass 33, Dive 37, Psychic 42 | Gorebyss (from 24) |
| Croconaw | good rod | 24 | Oxide | Bite, Scary Face, Ice Fang, Flail | Crunch 30; as Feraligatr: Agility 30, Crunch 32, Slash 37 | Feraligatr (from 30) |
| Croconaw | good rod | 24 | v3 | Water Gun, Bite, Scary Face, Flail | Crunch 30; as Feraligatr: Agility 30, Crunch 32, Slash 37 | Feraligatr (from 30) |
| Qwilfish | good rod | 24 | Oxide | Minimize, Water Gun, Rollout, Toxic Spikes | Stockpile 25, Spit Up 25, Revenge 29, Brine 33, Pin Missile 37, Take Down 41 | Qwilfish |
| Qwilfish | good rod | 24 | v3 | Harden, Minimize, Water Gun, Toxic Spikes | Stockpile 25, Spit Up 25, Revenge 29, Brine 33, Pin Missile 37, Take Down 41 | Qwilfish |
| Castform | wild | 26 to 29 | both | Tackle, Water Gun, Ember, Powder Snow | Weather Ball 30 | Castform |
| Yanma | wild | 26 to 29 | Oxide | Double Team, SonicBoom, Detect, Supersonic | Uproar 27, Pursuit 30, AncientPower 33; as Yanmega: Feint 38, Slash 43 | Yanmega (from 35) |
| Yanma | wild | 26 to 29 | v3 | Double Team, SonicBoom, Detect, Supersonic | Uproar 27, Pursuit 30, AncientPower 33; as Yanmega: Feint 38, Wing Attack 42, Slash 43 | Yanmega (from 35) |
| Croagunk | wild | 27 to 30 | both | Pursuit, Faint Attack, Revenge, Swagger | Mud Bomb 29, Sucker Punch 31, Nasty Plot 36; as Toxicroak: Poison Jab 41 | Toxicroak (from 37) |
| Dewpider | wild | 27 to 28 | both | Aqua Ring, BubbleBeam, Bug Bite, Headbutt | as Araquanid: Soak 31, Dive 36, Lunge 41 | Araquanid (from 28) |
| Dolliv | wild | 27 | Oxide | Helping Hand, Flail, Mega Drain, Grassy Terrain | Seed Bomb 29, Energy Ball 34; as Arboliva: Leech Seed 39 | Arboliva (from 35) |
| Dolliv | wild | 27 | v3 | Razor Leaf, Helping Hand, Flail, Mega Drain | Energy Ball 34; as Arboliva: Leech Seed 39, Seed Bomb 44 | Arboliva (from 35) |
| Joltik | wild | 27 to 28 | Oxide | Electroweb, Bug Bite, Gastro Acid, Struggle Bug | Discharge 29; as Galvantula: Signal Beam 35, Energy Ball 39, Sucker Punch 43 | Galvantula (from 30) |
| Joltik | wild | 27 to 28 | v3 | Electroweb, Bug Bite, Gastro Acid, Struggle Bug | as Galvantula: Signal Beam 35, Sucker Punch 43 | Galvantula (from 30) |
| Jumpluff | wild | 27 to 30 | Oxide | Stun Spore, Sleep Powder, Bullet Seed, Leech Seed | Mega Drain 28, Cotton Spore 32, U-turn 36, Worry Seed 40, Giga Drain 44 | Jumpluff |
| Jumpluff | wild | 27 to 30 | v3 | PoisonPowder, Stun Spore, Sleep Powder, Leech Seed | Cotton Spore 32, U-turn 36, Worry Seed 40, Giga Drain 44 | Jumpluff |
| Steenee | wild | 27 to 28 | Oxide | Sweet Scent, Magical Leaf, Teeter Dance, Stomp | Aromatic Mist 32; as Tsareena: Low Sweep 32, Aromatherapy 38, Leaf Storm 44 | Tsareena (from 32) |
| Steenee | wild | 27 to 28 | v3 | Sweet Scent, Magical Leaf, Teeter Dance, Stomp | as Tsareena: Low Sweep 32, Aromatherapy 38 | Tsareena (from 32) |
| Vespiquen | wild | 27 to 29 | Oxide | Fury Swipes, Power Gem, Heal Order, Toxic | Slash 31, Captivate 33, Attack Order 37, Swagger 39, Destiny Bond 43 | Vespiquen |
| Vespiquen | wild | 27 to 29 | v3 | Fury Swipes, Power Gem, Heal Order, Toxic | Slash 31, Captivate 33, Swagger 39, Attack Order 40, Destiny Bond 43 | Vespiquen |
| Wooper | wild | 27 to 31 | Oxide | Mud Shot, Slam, Mud Bomb, Amnesia | as Quagsire: Yawn 31, Earthquake 36 | Quagsire (from 28) |
| Wooper | wild | 27 to 31 | Oxide | Mud Shot, Slam, Mud Bomb, Amnesia | as Clodsire: Poison Jab 30, Megahorn 36, Toxic 40 | Clodsire (from 27) |
| Wooper | wild | 27 to 31 | v3 | Mud Shot, Slam, Mud Bomb, Amnesia | as Quagsire: Yawn 31, Earthquake 44 | Quagsire (from 28) |
| Wooper | wild | 27 to 31 | v3 | Mud Shot, Slam, Mud Bomb, Amnesia | as Clodsire: Poison Jab 36, Slam 37, Megahorn 39, Sludge Bomb 39, Toxic 40, Haze 43, Earthquake 44 | Clodsire (from 27) |
| Breloom | wild | 28 | Oxide | Mega Drain, Headbutt, Mach Punch, Counter | Force Palm 29, Sky Uppercut 33, Mind Reader 37, Seed Bomb 41 | Breloom |
| Breloom | wild | 28 | v3 | Mega Drain, Headbutt, Mach Punch, Counter | Force Palm 29, Sky Uppercut 33, Mind Reader 37 | Breloom |
| Budew | wild | 28 to 29 | both | Water Sport, Stun Spore, Mega Drain, Worry Seed | nothing | Roserade (from 30) |
| Fomantis | wild | 28 to 29 | Oxide | Razor Leaf, Ingrain, Sweet Scent, Slash | X-Scissor 30, Synthesis 31, Leaf Blade 32; as Lurantis: Leaf Blade 34 | Lurantis (from 34) |
| Fomantis | wild | 28 to 29 | v3 | Razor Leaf, Ingrain, Sweet Scent, Slash | X-Scissor 30, Synthesis 31; as Lurantis: Petal Blizzard on evolving | Lurantis (from 34) |
| Gligar | wild | 28 | Oxide | Quick Attack, Fury Cutter, Faint Attack, Screech | as Gliscor: Night Slash 31, Swords Dance 34, U-turn 38, X-Scissor 42 | Gliscor (from 28) |
| Gligar | wild | 28 | v3 | Knock Off, Quick Attack, Faint Attack, Screech | as Gliscor: Night Slash 31, Swords Dance 34, U-turn 38, X-Scissor 42 | Gliscor (from 28) |
| Houndoom | wild | 28 | both | Smog, Roar, Bite, Odor Sleuth | Fire Fang 32, Faint Attack 38, Embargo 44 | Houndoom |
| Koffing | wild | 28 to 31 | Oxide | Assurance, Selfdestruct, Sludge, Haze | Gyro Ball 33; as Weezing: Explosion 40 | Weezing (from 35) |
| Koffing | wild | 28 to 31 | Oxide | Assurance, Selfdestruct, Sludge, Haze | as Galarian Weezing: Toxic 29, Selfdestruct 34, Will-O-Wisp 38, Sludge Bomb 42 | Galarian Weezing (from 28) |
| Koffing | wild | 28 to 31 | v3 | Assurance, Selfdestruct, Sludge, Sludge Bomb | Gyro Ball 33; as Weezing: Explosion 40 | Weezing (from 35) |
| Koffing | wild | 28 to 31 | v3 | Assurance, Selfdestruct, Sludge, Sludge Bomb | as Galarian Weezing: Draining Kiss on evolving, Toxic 29, Selfdestruct 34, Will-O-Wisp 38, Sludge Bomb 42 | Galarian Weezing (from 28) |
| Lotad | wild | 28 to 30 | both | Mist, Natural Gift, Mega Drain, BubbleBeam | nothing | Ludicolo (from 29) |
| Mightyena | wild | 28 to 30 | both | Bite, Odor Sleuth, Roar, Swagger | Assurance 32, Crunch 34, Scary Face 37, Taunt 42 | Mightyena |
| Surskit | wild | 28 to 29 | both | Quick Attack, Sweet Scent, Water Sport, BubbleBeam | as Masquerain: Stun Spore 33, Silver Wind 40 | Masquerain (from 29) |
| Swadloon | wild | 28 to 30 | Oxide | Tackle, String Shot, Bug Bite, Razor Leaf | as Leavanny: Helping Hand 32, Leaf Blade 36, X-Scissor 39, Entrainment 43 | Leavanny (from 30) |
| Swadloon | wild | 28 to 30 | v3 | Tackle, String Shot, Bug Bite, Razor Leaf | as Leavanny: Slash on evolving, Helping Hand 32, X-Scissor 39, Entrainment 43 | Leavanny (from 30) |
| Tropius | wild | 28 | both | Razor Leaf, Stomp, Sweet Scent, Whirlwind | Magical Leaf 31, Body Slam 37, Synthesis 41 | Tropius |
| Barboach | wild | 29 to 31 | Oxide | Mud Bomb, Amnesia, Water Pulse, Magnitude | as Whiscash: Rest 33, Snore 33, Aqua Tail 39 | Whiscash (from 30) |
| Barboach | wild | 29 to 31 | v3 | Mud Bomb, Amnesia, Water Pulse, Magnitude | as Whiscash: Rest 33, Aqua Tail 39 | Whiscash (from 30) |
| Salandit | wild | 29 | Oxide | Flame Burst, Dragon Rage, Toxic, Venoshock | as Salazzle: Flamethrower 36, Sludge Bomb 42 | Salazzle (from 30) |
| Salandit | wild | 29 | v3 | Dragon Rage, Toxic, Flame Burst, Venoshock | nothing | Salazzle (from 30) |
| Skorupi | wild | 29 | both | Pin Missile, Acupressure, Scary Face, Toxic Spikes | Bug Bite 34, Poison Fang 39 | Drapion (from 40) |
| Stunky | wild | 29 to 31 | Oxide | SmokeScreen, Feint, Slash, Toxic | Night Slash 32; as Skuntank: Flamethrower 34, Memento 42 | Skuntank (from 34) |
| Stunky | wild | 29 to 31 | v3 | SmokeScreen, Feint, Slash, Toxic | Night Slash 32; as Skuntank: Flamethrower 39, Memento 42 | Skuntank (from 34) |
| Tangela | wild | 29 to 30 | Oxide | Vine Whip, Bind, Mega Drain, Stun Spore | AncientPower 33; as Tangrowth: Knock Off 36, Natural Gift 40, Slam 43 | Tangrowth (from 35) |
| Tangela | wild | 29 to 30 | v3 | PoisonPowder, Vine Whip, Mega Drain, Stun Spore | AncientPower 33; as Tangrowth: Knock Off 36, Natural Gift 40, Slam 43 | Tangrowth (from 35) |
| Azumarill | wild | 30 to 31 | Oxide | Water Gun, Rollout, BubbleBeam, Aqua Ring | Double-Edge 33 | Azumarill |
| Azumarill | wild | 30 to 31 | v3 | Tail Whip, Water Gun, BubbleBeam, Aqua Ring | Double-Edge 33 | Azumarill |
| Carnivine | wild | 30 to 31 | both | Vine Whip, Sweet Scent, Ingrain, Faint Attack | Stockpile 31, Spit Up 31, Swallow 31, Crunch 37, Wring Out 41 | Carnivine |

## Maniac Tunnel

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 44 | At the cap |
|---|---|---|---|---|---|---|
| Hippopotas | wild | 21 to 24 | Oxide | Sand-Attack, Bite, Yawn, Take Down | Sand Tomb 25, Crunch 31; as Hippowdon: Earthquake 40 | Hippowdon (from 34) |
| Hippopotas | wild | 21 to 24 | v3 | Sand-Attack, Bite, Yawn, Take Down | Crunch 31 | Hippowdon (from 34) |
| Bronzor | wild | 22 | Oxide | Hypnosis, Imprison, Confuse Ray, Extrasensory | Iron Defense 26, Safeguard 30; as Bronzong: Block 33, Gyro Ball 38, Future Sight 43 | Bronzong (from 33) |
| Bronzor | wild | 22 | v3 | Imprison, Confuse Ray, Extrasensory, Iron Head | Iron Defense 26, Safeguard 30, Zen Headbutt 31; as Bronzong: Block 33, Gyro Ball 38, Future Sight 43 | Bronzong (from 33) |
| Dwebble | wild | 22 | Oxide | Sand-Attack, Faint Attack, Slash, Rock Tomb | Bug Bite 24, Night Slash 27, X-Scissor 31, Rock Slide 34; as Crustle: Rock Slide 34, StompingTantrum 40 | Crustle (from 34) |
| Dwebble | wild | 22 | v3 | Sand-Attack, Faint Attack, Slash, Rock Tomb | Bug Bite 24, Night Slash 27, X-Scissor 31, Rock Blast 33, Rock Slide 34; as Crustle: Rock Slide 34, StompingTantrum 40 | Crustle (from 34) |
| Geodude | wild | 22 | Oxide | Rock Throw, Magnitude, Selfdestruct, Rollout | Rock Blast 25; as Graveler: Rock Blast 27, Earthquake 33, Explosion 38; as Golem: Double-Edge 44 | Golem (from 40) |
| Geodude | wild | 22 | v3 | Rock Polish, Rock Throw, Magnitude, Selfdestruct | Rock Blast 25; as Graveler: Rock Blast 27, Explosion 38, Earthquake 39; as Golem: Double-Edge 44 | Golem (from 40) |
| Golbat | wild | 22 | Oxide | Astonish, Bite, Wing Attack, Confuse Ray | Air Cutter 27, Mean Look 33, Poison Fang 39 | Crobat (from 40) |
| Golbat | wild | 22 | v3 | Supersonic, Bite, Wing Attack, Confuse Ray | Air Cutter 27, Mean Look 33, Poison Fang 39 | Crobat (from 40) |
| Nosepass | wild | 22 | both | Tackle, Harden, Rock Throw, Block | Thunder Wave 25, Rock Slide 31; as Probopass: Rest 43 | Probopass (from 32) |
| Ferroseed | wild | 23 to 24 | Oxide | Assurance, Pin Missile, Metal Claw, Ingrain | Payback 26, Bullet Seed 30, Gyro Ball 35, Selfdestruct 38; as Ferrothorn: Knock Off 44 | Ferrothorn (from 40) |
| Ferroseed | wild | 23 to 24 | v3 | Assurance, Pin Missile, Metal Claw, Ingrain | Payback 26, Bullet Seed 30, Seed Bomb 32, Iron Head 33, Gyro Ball 35, Selfdestruct 38; as Ferrothorn: Knock Off 44 | Ferrothorn (from 40) |
| Nacli | wild | 23 | Oxide | Smack Down, Rock Polish, Headbutt, Iron Defense | as Naclstack: Recover 30, Rock Slide 34, Stealth Rock 38; as Garganacl: Stealth Rock 40, Heavy Slam 44 | Garganacl (from 38) |
| Nacli | wild | 23 | v3 | Smack Down, Rock Polish, Headbutt, Iron Defense | as Naclstack: Salt Cure on evolving, Recover 30, Rock Slide 34, Stealth Rock 38; as Garganacl: Hammer Arm on evolving, Stealth Rock 40, Heavy Slam 44 | Garganacl (from 38) |
| Onix | wild | 23 to 24 | Oxide | Screech, Rock Throw, Rage, Rock Tomb | as Steelix: Slam 25, Rock Polish 30, DragonBreath 33, Curse 38, Iron Tail 41 | Steelix (from 23) |
| Onix | wild | 23 to 24 | v3 | Harden, Screech, Rock Throw, Rock Tomb | as Steelix: Slam 25, Rock Polish 30, DragonBreath 33, Curse 38, Iron Tail 41 | Steelix (from 23) |

## Pastoria City

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 44 | At the cap |
|---|---|---|---|---|---|---|
| Barboach | old rod | 12 | Oxide | Mud-Slap, Mud Sport, Water Sport, Water Gun | Mud Bomb 14, Amnesia 18, Water Pulse 22, Magnitude 26; as Whiscash: Rest 33, Snore 33, Aqua Tail 39 | Whiscash (from 30) |
| Barboach | old rod | 12 | v3 | Mud-Slap, Mud Sport, Water Sport, Water Gun | Mud Bomb 14, Amnesia 18, Water Pulse 22, Magnitude 26; as Whiscash: Rest 33, Aqua Tail 39 | Whiscash (from 30) |
| Goldeen | old rod | 12 | Oxide | Tail Whip, Water Sport, Supersonic, Horn Attack | Water Pulse 17, Flail 21, Aqua Ring 27, Fury Attack 31; as Seaking: Waterfall 40 | Seaking (from 33) |
| Goldeen | old rod | 12 | v3 | Tail Whip, Water Sport, Supersonic, Horn Attack | Water Pulse 17, Flail 21, Aqua Ring 27; as Seaking: Waterfall 40 | Seaking (from 33) |
| Carvanha | old rod | 13 to 14 | Oxide | Bite, Rage, Focus Energy, Scary Face | Ice Fang 16, Screech 18, Swagger 21, Assurance 26, Crunch 28; as Sharpedo: Slash 30, Aqua Jet 34, Taunt 40 | Sharpedo (from 30) |
| Carvanha | old rod | 13 to 14 | v3 | Bite, Water Gun, Focus Energy, Scary Face | Screech 18, Swagger 21, Assurance 26, Crunch 28; as Sharpedo: Slash 30, Aqua Jet 34, Taunt 40 | Sharpedo (from 30) |
| Wooper | old rod | 13 | Oxide | Water Gun, Tail Whip, Mud Sport, Mud Shot | Slam 15, Mud Bomb 19; as Quagsire: Amnesia 24, Yawn 31, Earthquake 36 | Quagsire (from 20) |
| Wooper | old rod | 13 | Oxide | Water Gun, Tail Whip, Mud Sport, Mud Shot | as Clodsire: Slam 16, Yawn 21, Bulldoze 24, Poison Jab 30, Megahorn 36, Toxic 40 | Clodsire (from 13) |
| Wooper | old rod | 13 | v3 | Water Gun, Tail Whip, Mud Sport, Mud Shot | Slam 15, Mud Bomb 19; as Quagsire: Amnesia 24, Yawn 31, Earthquake 44 | Quagsire (from 20) |
| Wooper | old rod | 13 | v3 | Water Gun, Tail Whip, Mud Sport, Mud Shot | as Clodsire: Mud Bomb 19, Yawn 21, Bulldoze 24, Poison Jab 36, Slam 37, Megahorn 39, Sludge Bomb 39, Toxic 40, Haze 43, Earthquake 44 | Clodsire (from 13) |
| Carvanha | good rod | 20 | Oxide | Focus Energy, Scary Face, Ice Fang, Screech | Swagger 21, Assurance 26, Crunch 28; as Sharpedo: Slash 30, Aqua Jet 34, Taunt 40 | Sharpedo (from 30) |
| Carvanha | good rod | 20 | v3 | Water Gun, Focus Energy, Scary Face, Screech | Swagger 21, Assurance 26, Crunch 28; as Sharpedo: Slash 30, Aqua Jet 34, Taunt 40 | Sharpedo (from 30) |
| Lotad | good rod | 20 | both | Nature Power, Mist, Natural Gift, Mega Drain | nothing | Ludicolo (from 21) |
| Araquanid | good rod | 22 to 24 | both | Bite, Aqua Ring, BubbleBeam, Bug Bite | Headbutt 26, Soak 31, Dive 36, Lunge 41 | Araquanid |
| Masquerain | good rod | 22 | Oxide | Quick Attack, Sweet Scent, Water Sport, Gust | Scary Face 26, Stun Spore 33, Silver Wind 40 | Masquerain |
| Masquerain | good rod | 22 | v3 | Bubble, Quick Attack, Sweet Scent, Water Sport | Scary Face 26, Stun Spore 33, Silver Wind 40 | Masquerain |

## Pokémon Mansion

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 44 | At the cap |
|---|---|---|---|---|---|---|
| Manaphy | egg gift | 1 | Oxide | Tail Glow, Bubble, Water Sport | Charm 9, Supersonic 16, BubbleBeam 24, Acid Armor 31, Whirlpool 39 | Manaphy |
| Manaphy | egg gift | 1 | v3 | Tail Glow, Bubble, Water Sport | Charm 9, Supersonic 16, BubbleBeam 24, Acid Armor 31 | Manaphy |

## Route 212

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 44 | At the cap |
|---|---|---|---|---|---|---|
| Barboach | old rod | 12 | Oxide | Mud-Slap, Mud Sport, Water Sport, Water Gun | Mud Bomb 14, Amnesia 18, Water Pulse 22, Magnitude 26; as Whiscash: Rest 33, Snore 33, Aqua Tail 39 | Whiscash (from 30) |
| Barboach | old rod | 12 | v3 | Mud-Slap, Mud Sport, Water Sport, Water Gun | Mud Bomb 14, Amnesia 18, Water Pulse 22, Magnitude 26; as Whiscash: Rest 33, Aqua Tail 39 | Whiscash (from 30) |
| Carvanha | old rod | 12 to 13 | Oxide | Bite, Rage, Focus Energy, Scary Face | Ice Fang 16, Screech 18, Swagger 21, Assurance 26, Crunch 28; as Sharpedo: Slash 30, Aqua Jet 34, Taunt 40 | Sharpedo (from 30) |
| Carvanha | old rod | 12 to 13 | v3 | Bite, Water Gun, Focus Energy, Scary Face | Screech 18, Swagger 21, Assurance 26, Crunch 28; as Sharpedo: Slash 30, Aqua Jet 34, Taunt 40 | Sharpedo (from 30) |
| Chinchou | old rod | 12 | Oxide | Supersonic, Thunder Wave, Flail, Water Gun | Confuse Ray 17, Spark 20, Take Down 23; as Lanturn: Stockpile 27, Swallow 27, Spit Up 27, BubbleBeam 30, Signal Beam 35, Discharge 40 | Lanturn (from 27) |
| Chinchou | old rod | 12 | v3 | Supersonic, Thunder Wave, Flail, Water Gun | Confuse Ray 17, Spark 20, Take Down 23; as Lanturn: Stockpile 27, Swallow 27, Spit Up 27, BubbleBeam 30, Signal Beam 35 | Lanturn (from 27) |
| Horsea | old rod | 12 | Oxide | Bubble, SmokeScreen, Leer, Water Gun | Focus Energy 14, BubbleBeam 18, Agility 23, Twister 26, Brine 30; as Kingdra: Hydro Pump 40 | Kingdra (from 32) |
| Horsea | old rod | 12 | v3 | Bubble, SmokeScreen, Leer, Water Gun | Focus Energy 14, BubbleBeam 18, Agility 23, Brine 30; as Kingdra: Hydro Pump 40 | Kingdra (from 32) |
| Dewpider | old rod | 13 | Oxide | Bubble, Infestation, Bite, Aqua Ring | BubbleBeam 17, Bug Bite 21; as Araquanid: Headbutt 26, Soak 31, Dive 36, Lunge 41 | Araquanid (from 22) |
| Dewpider | old rod | 13 | v3 | Bubble, Water Gun, Bite, Aqua Ring | BubbleBeam 17, Bug Bite 21; as Araquanid: Headbutt 26, Soak 31, Dive 36, Lunge 41 | Araquanid (from 22) |
| Qwilfish | old rod | 13 | Oxide | Poison Sting, Harden, Minimize, Water Gun | Rollout 17, Toxic Spikes 21, Stockpile 25, Spit Up 25, Revenge 29, Brine 33, Pin Missile 37, Take Down 41 | Qwilfish |
| Qwilfish | old rod | 13 | v3 | Poison Sting, Harden, Minimize, Water Gun | Toxic Spikes 21, Stockpile 25, Spit Up 25, Revenge 29, Brine 33, Pin Missile 37, Take Down 41 | Qwilfish |
| Wooper | old rod | 13 | Oxide | Water Gun, Tail Whip, Mud Sport, Mud Shot | Slam 15, Mud Bomb 19; as Quagsire: Amnesia 24, Yawn 31, Earthquake 36 | Quagsire (from 20) |
| Wooper | old rod | 13 | Oxide | Water Gun, Tail Whip, Mud Sport, Mud Shot | as Clodsire: Slam 16, Yawn 21, Bulldoze 24, Poison Jab 30, Megahorn 36, Toxic 40 | Clodsire (from 13) |
| Wooper | old rod | 13 | v3 | Water Gun, Tail Whip, Mud Sport, Mud Shot | Slam 15, Mud Bomb 19; as Quagsire: Amnesia 24, Yawn 31, Earthquake 44 | Quagsire (from 20) |
| Wooper | old rod | 13 | v3 | Water Gun, Tail Whip, Mud Sport, Mud Shot | as Clodsire: Mud Bomb 19, Yawn 21, Bulldoze 24, Poison Jab 36, Slam 37, Megahorn 39, Sludge Bomb 39, Toxic 40, Haze 43, Earthquake 44 | Clodsire (from 13) |
| Frillish | old rod | 14 | Oxide | Bubble, Absorb, Night Shade, Ominous Wind | Water Pulse 15, Imprison 20, Confuse Ray 25, Hex 30, Brine 34, Pain Split 39 | Jellicent (from 40) |
| Frillish | old rod | 14 | v3 | Bubble, Night Shade, Ominous Wind | Water Pulse 15, Imprison 20, Confuse Ray 25, Hex 30, Brine 34, Pain Split 39 | Jellicent (from 40) |
| Poliwag | old rod | 14 | both | Water Sport, Bubble, Hypnosis, Water Gun | DoubleSlap 15, Body Slam 21, BubbleBeam 25; as Poliwrath: DynamicPunch 43 | Poliwrath (from 25) |
| Poliwag | old rod | 14 | both | Water Sport, Bubble, Hypnosis, Water Gun | DoubleSlap 15, Body Slam 21, BubbleBeam 25; as Politoed: Swagger 27, Bounce 37 | Politoed (from 25) |
| Barboach | good rod | 20 | Oxide | Water Sport, Water Gun, Mud Bomb, Amnesia | Water Pulse 22, Magnitude 26; as Whiscash: Rest 33, Snore 33, Aqua Tail 39 | Whiscash (from 30) |
| Barboach | good rod | 20 | v3 | Water Sport, Water Gun, Mud Bomb, Amnesia | Water Pulse 22, Magnitude 26; as Whiscash: Rest 33, Aqua Tail 39 | Whiscash (from 30) |
| Buizel | good rod | 20 | Oxide | Quick Attack, Water Gun, Pursuit, Swift | Aqua Jet 21; as Floatzel: Crunch 26, Agility 29, Whirlpool 39 | Floatzel (from 26) |
| Buizel | good rod | 20 | v3 | Quick Attack, Water Gun, Pursuit, Swift | Aqua Jet 21; as Floatzel: Crunch 26, Agility 29 | Floatzel (from 26) |
| Wooper | good rod | 20 | Oxide | Mud Sport, Mud Shot, Slam, Mud Bomb | as Quagsire: Amnesia 24, Yawn 31, Earthquake 36 | Quagsire (from 21) |
| Wooper | good rod | 20 | Oxide | Mud Sport, Mud Shot, Slam, Mud Bomb | as Clodsire: Yawn 21, Bulldoze 24, Poison Jab 30, Megahorn 36, Toxic 40 | Clodsire (from 20) |
| Wooper | good rod | 20 | v3 | Mud Sport, Mud Shot, Slam, Mud Bomb | as Quagsire: Amnesia 24, Yawn 31, Earthquake 44 | Quagsire (from 21) |
| Wooper | good rod | 20 | v3 | Mud Sport, Mud Shot, Slam, Mud Bomb | as Clodsire: Yawn 21, Bulldoze 24, Poison Jab 36, Slam 37, Megahorn 39, Sludge Bomb 39, Toxic 40, Haze 43, Earthquake 44 | Clodsire (from 20) |
| Emolga | wild | 21 | Oxide | Double Team, Charge, Nuzzle, Pursuit | Spark 22, Shock Wave 22, Electro Ball 26, Acrobatics 27, Encore 36, Light Screen 39, Volt Switch 40 | Emolga |
| Emolga | wild | 21 | v3 | ThunderShock, Charge, Nuzzle, Pursuit | Spark 22, Shock Wave 22, Electro Ball 26, Acrobatics 27, Encore 36, Light Screen 39, Volt Switch 40 | Emolga |
| Koffing | wild | 21 to 22 | Oxide | Smog, SmokeScreen, Assurance, Selfdestruct | Sludge 24, Haze 28, Gyro Ball 33; as Weezing: Explosion 40 | Weezing (from 35) |
| Koffing | wild | 21 to 22 | Oxide | Smog, SmokeScreen, Assurance, Selfdestruct | as Galarian Weezing: Payback 23, Sludge 26, Toxic 29, Selfdestruct 34, Will-O-Wisp 38, Sludge Bomb 42 | Galarian Weezing (from 21) |
| Koffing | wild | 21 to 22 | v3 | Smog, SmokeScreen, Assurance, Selfdestruct | Sludge 24, Sludge Bomb 26, Gyro Ball 33; as Weezing: Explosion 40 | Weezing (from 35) |
| Koffing | wild | 21 to 22 | v3 | Smog, SmokeScreen, Assurance, Selfdestruct | as Galarian Weezing: Draining Kiss on evolving, Payback 23, Sludge 26, Toxic 29, Selfdestruct 34, Will-O-Wisp 38, Sludge Bomb 42 | Galarian Weezing (from 21) |
| Carvanha | good rod | 22 | Oxide | Scary Face, Ice Fang, Screech, Swagger | Assurance 26, Crunch 28; as Sharpedo: Slash 30, Aqua Jet 34, Taunt 40 | Sharpedo (from 30) |
| Carvanha | good rod | 22 | v3 | Focus Energy, Scary Face, Screech, Swagger | Assurance 26, Crunch 28; as Sharpedo: Slash 30, Aqua Jet 34, Taunt 40 | Sharpedo (from 30) |
| Croagunk | wild | 22 | both | Taunt, Pursuit, Faint Attack, Revenge | Swagger 24, Mud Bomb 29, Sucker Punch 31, Nasty Plot 36; as Toxicroak: Poison Jab 41 | Toxicroak (from 37) |
| Fomantis | wild | 22 | Oxide | Fury Cutter, Growth, Razor Leaf, Ingrain | Sweet Scent 27, Slash 28, X-Scissor 30, Synthesis 31, Leaf Blade 32; as Lurantis: Leaf Blade 34 | Lurantis (from 34) |
| Fomantis | wild | 22 | v3 | Leafage, Growth, Razor Leaf, Ingrain | Sweet Scent 27, Slash 28, X-Scissor 30, Synthesis 31; as Lurantis: Petal Blizzard on evolving | Lurantis (from 34) |
| Kirlia | wild | 22 | Oxide | Double Team, Teleport, Lucky Chant, Magical Leaf | Calm Mind 25; as Gardevoir: Psychic 33, Imprison 40 | Gardevoir (from 30) |
| Kirlia | wild | 22 | Oxide | Double Team, Teleport, Lucky Chant, Magical Leaf | Calm Mind 25, Psychic 31, Imprison 36, Future Sight 39 | Kirlia; Gallade in Byron |
| Kirlia | wild | 22 | v3 | Confusion, Double Team, Lucky Chant, Magical Leaf | Calm Mind 25; as Gardevoir: Imprison 40, Psychic 44 | Gardevoir (from 30) |
| Kirlia | wild | 22 | v3 | Confusion, Double Team, Lucky Chant, Magical Leaf | Calm Mind 25, Imprison 36, Psychic 38, Future Sight 39 | Kirlia; Gallade in Byron |
| Liepard | wild | 22 | both | Fury Swipes, Pursuit, Torment, Fake Out | Assurance 26, Hone Claws 27, Slash 34, Taunt 38, Sucker Punch 43, Nasty Plot 44, Night Slash 44 | Liepard |
| Lombre | good rod | 22 | both | Nature Power, Fake Out, Fury Swipes, Water Sport | nothing | Ludicolo (from 22) |
| Lombre | wild | 22 | both | Nature Power, Fake Out, Fury Swipes, Water Sport | nothing | Ludicolo (from 22) |
| Lopunny | wild | 22 | both | Foresight, Endure, Return, Quick Attack | Jump Kick 23, Baton Pass 26, Agility 33, Dizzy Punch 36, Charm 43 | Lopunny |
| Masquerain | wild | 22 to 23 | Oxide | Quick Attack, Sweet Scent, Water Sport, Gust | Scary Face 26, Stun Spore 33, Silver Wind 40 | Masquerain |
| Masquerain | wild | 22 to 23 | v3 | Bubble, Quick Attack, Sweet Scent, Water Sport | Scary Face 26, Stun Spore 33, Silver Wind 40 | Masquerain |
| Mightyena | wild | 22 | both | Sand-Attack, Bite, Odor Sleuth, Roar | Swagger 27, Assurance 32, Crunch 34, Scary Face 37, Taunt 42 | Mightyena |
| Pachirisu | wild | 22 | Oxide | Charm, Spark, Endure, Swift | Sweet Kiss 25, Discharge 29, Super Fang 33, Last Resort 37 | Pachirisu |
| Pachirisu | wild | 22 | v3 | Charm, Spark, Endure, Swift | Sweet Kiss 25, Discharge 29, Thunder Fang 32, Super Fang 33, Last Resort 37 | Pachirisu |
| Surskit | good rod | 22 | both | Bubble, Quick Attack, Sweet Scent, Water Sport | as Masquerain: Scary Face 26, Stun Spore 33, Silver Wind 40 | Masquerain (from 23) |
| Swadloon | wild | 22 | Oxide | Tackle, String Shot, Bug Bite, Razor Leaf | as Leavanny: Helping Hand 32, Leaf Blade 36, X-Scissor 39, Entrainment 43 | Leavanny (from 30) |
| Swadloon | wild | 22 | v3 | Tackle, String Shot, Bug Bite, Razor Leaf | as Leavanny: Slash on evolving, Helping Hand 32, X-Scissor 39, Entrainment 43 | Leavanny (from 30) |
| Wooper | wild | 22 | Oxide | Mud Sport, Mud Shot, Slam, Mud Bomb | Amnesia 23; as Quagsire: Amnesia 24, Yawn 31, Earthquake 36 | Quagsire (from 23) |
| Wooper | wild | 22 | Oxide | Mud Sport, Mud Shot, Slam, Mud Bomb | as Clodsire: Bulldoze 24, Poison Jab 30, Megahorn 36, Toxic 40 | Clodsire (from 22) |
| Wooper | wild | 22 | v3 | Mud Sport, Mud Shot, Slam, Mud Bomb | Amnesia 23; as Quagsire: Amnesia 24, Yawn 31, Earthquake 44 | Quagsire (from 23) |
| Wooper | wild | 22 | v3 | Mud Sport, Mud Shot, Slam, Mud Bomb | as Clodsire: Bulldoze 24, Poison Jab 36, Slam 37, Megahorn 39, Sludge Bomb 39, Toxic 40, Haze 43, Earthquake 44 | Clodsire (from 22) |
| Araquanid | wild | 23 | both | Bite, Aqua Ring, BubbleBeam, Bug Bite | Headbutt 26, Soak 31, Dive 36, Lunge 41 | Araquanid |
| Budew | wild | 23 | both | Water Sport, Stun Spore, Mega Drain, Worry Seed | nothing | Roserade (from 30) |
| Frogadier | wild | 23 | Oxide | Water Pulse, Icy Wind, Faint Attack, Acrobatics | Low Kick 25, Waterfall 30, Fling 35; as Greninja: Scald 37, Dark Pulse 40, Extrasensory 43 | Greninja (from 36) |
| Frogadier | wild | 23 | v3 | Water Pulse, Icy Wind, Faint Attack, Acrobatics | Low Kick 25, Fling 35; as Greninja: Water Shuriken on evolving, Night Slash on evolving, Scald 37, Dark Pulse 40, Extrasensory 43 | Greninja (from 36) |
| Steenee | wild | 23 | Oxide | Razor Leaf, Sweet Scent, Magical Leaf, Teeter Dance | Stomp 25, Aromatic Mist 32; as Tsareena: Low Sweep 32, Aromatherapy 38, Leaf Storm 44 | Tsareena (from 32) |
| Steenee | wild | 23 | v3 | Razor Leaf, Sweet Scent, Magical Leaf, Teeter Dance | Stomp 25; as Tsareena: Low Sweep 32, Aromatherapy 38 | Tsareena (from 32) |
| Tropius | wild | 23 | both | Growth, Razor Leaf, Stomp, Sweet Scent | Whirlwind 27, Magical Leaf 31, Body Slam 37, Synthesis 41 | Tropius |
| Vespiquen | wild | 23 | Oxide | Defend Order, Pursuit, Fury Swipes, Power Gem | Heal Order 25, Toxic 27, Slash 31, Captivate 33, Attack Order 37, Swagger 39, Destiny Bond 43 | Vespiquen |
| Vespiquen | wild | 23 | v3 | Defend Order, Pursuit, Fury Swipes, Power Gem | Heal Order 25, Toxic 27, Slash 31, Captivate 33, Swagger 39, Attack Order 40, Destiny Bond 43 | Vespiquen |
| Yanma | wild | 23 | Oxide | Double Team, SonicBoom, Detect, Supersonic | Uproar 27, Pursuit 30, AncientPower 33; as Yanmega: Feint 38, Slash 43 | Yanmega (from 35) |
| Yanma | wild | 23 | v3 | Double Team, SonicBoom, Detect, Supersonic | Uproar 27, Pursuit 30, AncientPower 33; as Yanmega: Feint 38, Wing Attack 42, Slash 43 | Yanmega (from 35) |
| Araquanid | good rod | 24 | both | Bite, Aqua Ring, BubbleBeam, Bug Bite | Headbutt 26, Soak 31, Dive 36, Lunge 41 | Araquanid |
| Breloom | wild | 24 | Oxide | Leech Seed, Mega Drain, Headbutt, Mach Punch | Counter 25, Force Palm 29, Sky Uppercut 33, Mind Reader 37, Seed Bomb 41 | Breloom |
| Breloom | wild | 24 | v3 | Leech Seed, Mega Drain, Headbutt, Mach Punch | Counter 25, Force Palm 29, Sky Uppercut 33, Mind Reader 37 | Breloom |
| Dartrix | wild | 24 | Oxide | Astonish, Razor Leaf, Pluck, Ominous Wind | Synthesis 28, Seed Bomb 32, Sucker Punch 36; as Decidueye: Sucker Punch 38 | Decidueye (from 36) |
| Dartrix | wild | 24 | v3 | Peck, Razor Leaf, Pluck, Ominous Wind | Synthesis 28, Seed Bomb 32, Sucker Punch 36; as Decidueye: Sucker Punch 38 | Decidueye (from 36) |
| Goomy | wild | 24 | Oxide | DragonBreath, Life Dew, Flail, Water Pulse | Dragon Tail 28, Infestation 34; as Sliggoo: Body Slam 42 | Sliggoo (from 40); Goodra in Byron |
| Goomy | wild | 24 | Oxide | DragonBreath, Life Dew, Flail, Water Pulse | as Hisuian Sliggoo: Water Pulse 25, Dragon Pulse 35, Curse 43 | Hisuian Sliggoo (from 24); Hisuian Goodra in Byron |
| Goomy | wild | 24 | v3 | DragonBreath, Life Dew, Flail, Water Pulse | Dragon Tail 28; as Sliggoo: Body Slam 42 | Sliggoo (from 40); Goodra in Byron |
| Goomy | wild | 24 | v3 | DragonBreath, Life Dew, Flail, Water Pulse | as Hisuian Sliggoo: Shelter on evolving, Water Pulse 25, Dragon Tail 28, Dragon Pulse 31, Iron Head 33, Muddy Water 39, Curse 43 | Hisuian Sliggoo (from 24); Hisuian Goodra in Byron |
| Luvdisc | good rod | 24 | both | Agility, Take Down, Lucky Chant, Attract | Sweet Kiss 27; as Alomomola: Soak 33, Wish 37, Brine 41 | Alomomola (from 30) |
| Sandygast | wild | 24 | Oxide | Sand Tomb, Sand-Attack, Mega Drain, Bulldoze | Hypnosis 28, Giga Drain 35, Iron Defense 36; as Palossand: Shadow Ball 44 | Palossand (from 42) |
| Sandygast | wild | 24 | v3 | Shadow Sneak, Sand-Attack, Mega Drain, Bulldoze | Hypnosis 28, Earth Power 32, Giga Drain 35, Iron Defense 36, Shadow Ball 39; as Palossand: Shadow Ball 44 | Palossand (from 42) |
| Smoliv | wild | 24 | Oxide | Helping Hand, Flail, Mega Drain, Grassy Terrain | as Dolliv: Seed Bomb 29, Energy Ball 34; as Arboliva: Leech Seed 39 | Arboliva (from 35) |
| Smoliv | wild | 24 | v3 | Razor Leaf, Helping Hand, Flail, Mega Drain | as Dolliv: Energy Ball 34; as Arboliva: Leech Seed 39, Seed Bomb 44 | Arboliva (from 35) |
| Tangela | wild | 24 | Oxide | Growth, PoisonPowder, Vine Whip, Bind | Mega Drain 26, Stun Spore 29, AncientPower 33; as Tangrowth: Knock Off 36, Natural Gift 40, Slam 43 | Tangrowth (from 35) |
| Tangela | wild | 24 | v3 | Leafage, Growth, PoisonPowder, Vine Whip | Mega Drain 26, Stun Spore 29, AncientPower 33; as Tangrowth: Knock Off 36, Natural Gift 40, Slam 43 | Tangrowth (from 35) |

## Route 213

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 44 | At the cap |
|---|---|---|---|---|---|---|
| Qwilfish | old rod | 12 | Oxide | Tackle, Poison Sting, Harden, Minimize | Water Gun 13, Rollout 17, Toxic Spikes 21, Stockpile 25, Spit Up 25, Revenge 29, Brine 33, Pin Missile 37, Take Down 41 | Qwilfish |
| Qwilfish | old rod | 12 | v3 | Tackle, Poison Sting, Harden, Minimize | Water Gun 13, Toxic Spikes 21, Stockpile 25, Spit Up 25, Revenge 29, Brine 33, Pin Missile 37, Take Down 41 | Qwilfish |
| Tentacool | old rod | 12 | Oxide | Poison Sting, Supersonic, Constrict, Acid | Toxic Spikes 15, BubbleBeam 19, Wrap 22, Barrier 26, Water Pulse 29; as Tentacruel: Poison Jab 36, Screech 42 | Tentacruel (from 30) |
| Tentacool | old rod | 12 | v3 | Poison Sting, Supersonic, Water Gun, Acid | Toxic Spikes 15, BubbleBeam 19, Barrier 26, Water Pulse 29; as Tentacruel: Poison Jab 36, Screech 42, Toxic 44 | Tentacruel (from 30) |
| Mantyke | old rod | 13 | both | Bubble, Supersonic, BubbleBeam, Headbutt | Agility 19, Wing Attack 22, Water Pulse 28; as Mantine: Take Down 31, Confuse Ray 37, Bounce 40 | Mantine (from 30) |
| Poliwag | old rod | 13 | both | Water Sport, Bubble, Hypnosis, Water Gun | DoubleSlap 15, Body Slam 21, BubbleBeam 25; as Poliwrath: DynamicPunch 43 | Poliwrath (from 25) |
| Poliwag | old rod | 13 | both | Water Sport, Bubble, Hypnosis, Water Gun | DoubleSlap 15, Body Slam 21, BubbleBeam 25; as Politoed: Swagger 27, Bounce 37 | Politoed (from 25) |
| Staryu | old rod | 14 | Oxide | Tackle, Harden, Water Gun, Rapid Spin | as Starmie: Confuse Ray 28 | Starmie (from 14) |
| Staryu | old rod | 14 | v3 | Tackle, Harden, Water Gun, Rapid Spin | as Starmie: Confuse Ray 28, Light Screen 42 | Starmie (from 14) |
| Dewpider | good rod | 20 | Oxide | Infestation, Bite, Aqua Ring, BubbleBeam | Bug Bite 21; as Araquanid: Headbutt 26, Soak 31, Dive 36, Lunge 41 | Araquanid (from 22) |
| Dewpider | good rod | 20 | v3 | Water Gun, Bite, Aqua Ring, BubbleBeam | Bug Bite 21; as Araquanid: Headbutt 26, Soak 31, Dive 36, Lunge 41 | Araquanid (from 22) |
| Tentacool | good rod | 20 | Oxide | Constrict, Acid, Toxic Spikes, BubbleBeam | Wrap 22, Barrier 26, Water Pulse 29; as Tentacruel: Poison Jab 36, Screech 42 | Tentacruel (from 30) |
| Tentacool | good rod | 20 | v3 | Water Gun, Acid, Toxic Spikes, BubbleBeam | Barrier 26, Water Pulse 29; as Tentacruel: Poison Jab 36, Screech 42, Toxic 44 | Tentacruel (from 30) |
| Mareanie | good rod | 22 | Oxide | Bite, Wide Guard, Venoshock, Toxic Spikes | Recover 26, Spike Cannon 29, Pin Missile 34, Toxic 36; as Toxapex: Toxic 39, Venom Drench 42, Poison Jab 43 | Toxapex (from 38) |
| Mareanie | good rod | 22 | v3 | Bite, Wide Guard, Venoshock, Toxic Spikes | Recover 26, Spike Cannon 29, Pin Missile 34, Toxic 36; as Toxapex: Baneful Bunker on evolving, Toxic 39, Venom Drench 42, Poison Jab 43 | Toxapex (from 38) |
| Remoraid | good rod | 22 | both | Lock-On, Psybeam, Aurora Beam, BubbleBeam | Focus Energy 23; as Octillery: Octazooka 25, Bullet Seed 29, Wring Out 36, Signal Beam 42 | Octillery (from 25) |
| Sandygast | wild | 23 | Oxide | Astonish, Sand Tomb, Sand-Attack, Mega Drain | Bulldoze 24, Hypnosis 28, Giga Drain 35, Iron Defense 36; as Palossand: Shadow Ball 44 | Palossand (from 42) |
| Sandygast | wild | 23 | v3 | Harden, Shadow Sneak, Sand-Attack, Mega Drain | Bulldoze 24, Hypnosis 28, Earth Power 32, Giga Drain 35, Iron Defense 36, Shadow Ball 39; as Palossand: Shadow Ball 44 | Palossand (from 42) |
| Clobbopus | wild | 24 | Oxide | Feint, Bind, Detect, Brick Break | Bulk Up 25, Submission 30; as Grapploct: Taunt 35, Reversal 40 | Grapploct (from 32) |
| Clobbopus | wild | 24 | v3 | Rock Smash, Leer, Feint, Detect | Bulk Up 25, Brick Break 31; as Grapploct: Taunt 35, Reversal 40 | Grapploct (from 32) |
| Corvisquire | wild | 24 | Oxide | Fury Attack, Sand-Attack, Pluck, Steel Wing | Drill Peck 26, FeatherDance 32, Revenge 38; as Corviknight: Defog 42, Iron Head 44 | Corviknight (from 40) |
| Corvisquire | wild | 24 | v3 | Fury Attack, Sand-Attack, Pluck, Steel Wing | Drill Peck 29, FeatherDance 32, Revenge 38; as Corviknight: Defog 42, Iron Head 44 | Corviknight (from 40) |
| Dewpider | wild | 24 | both | Bite, Aqua Ring, BubbleBeam, Bug Bite | Headbutt 25; as Araquanid: Headbutt 26, Soak 31, Dive 36, Lunge 41 | Araquanid (from 25) |
| Liepard | wild | 24 | both | Fury Swipes, Pursuit, Torment, Fake Out | Assurance 26, Hone Claws 27, Slash 34, Taunt 38, Sucker Punch 43, Nasty Plot 44, Night Slash 44 | Liepard |
| Spheal | good rod | 24 | Oxide | Water Gun, Encore, Ice Ball, Body Slam | Aurora Beam 25; as Sealeo: Swagger 32, Rest 39, Snore 39; as Walrein: Ice Fang 44 | Walrein (from 44) |
| Spheal | good rod | 24 | v3 | Growl, Water Gun, Body Slam, Bounce | Aurora Beam 25, Encore 31; as Sealeo: Swagger 32, Dive 38, Rest 39; as Walrein: Ice Fang 44 | Walrein (from 44) |
| Trumbeak | wild | 24 | Oxide | Supersonic, Pluck, Roost, Fury Attack | as Toucannon: Screech 30, Drill Peck 34, Bullet Seed 40, FeatherDance 44 | Toucannon (from 28) |
| Trumbeak | wild | 24 | v3 | Supersonic, Pluck, Roost, Fury Attack | as Toucannon: Beak Blast on evolving, Screech 30, Bullet Seed 40, FeatherDance 44 | Toucannon (from 28) |
| Buizel | wild | 25 | Oxide | Water Gun, Pursuit, Swift, Aqua Jet | as Floatzel: Crunch 26, Agility 29, Whirlpool 39 | Floatzel (from 26) |
| Buizel | wild | 25 | v3 | Water Gun, Pursuit, Swift, Aqua Jet | as Floatzel: Crunch 26, Agility 29 | Floatzel (from 26) |
| Dubwool | wild | 25 | Oxide | Copycat, Guard Split, Double Kick, Headbutt | Take Down 27, Guard Swap 32, Reversal 38, Cotton Guard 44 | Dubwool |
| Dubwool | wild | 25 | v3 | Copycat, Guard Split, Double Kick, Headbutt | Guard Swap 32, Reversal 38, Take Down 39, Cotton Guard 44 | Dubwool |
| Fletchinder | wild | 25 | both | Quick Attack, Aerial Ace, Flame Charge, Roost | Will-O-Wisp 27, Natural Gift 31; as Talonflame: Acrobatics 38, Me First 42 | Talonflame (from 36) |
| Shellos | wild | 25 | Oxide | Harden, Water Pulse, Mud Bomb, Hidden Power | Body Slam 29; as Gastrodon: Muddy Water 41 | Gastrodon (from 30) |
| Shellos | wild | 25 | v3 | Harden, Water Pulse, Mud Bomb, Hidden Power | Body Slam 29; as Gastrodon: Muddy Water 39, Earthquake 44 | Gastrodon (from 30) |
| Dolliv | wild | 26 | Oxide | Helping Hand, Flail, Mega Drain, Grassy Terrain | Seed Bomb 29, Energy Ball 34; as Arboliva: Leech Seed 39 | Arboliva (from 35) |
| Dolliv | wild | 26 | v3 | Razor Leaf, Helping Hand, Flail, Mega Drain | Energy Ball 34; as Arboliva: Leech Seed 39, Seed Bomb 44 | Arboliva (from 35) |
| Mantyke | wild | 26 | both | BubbleBeam, Headbutt, Agility, Wing Attack | Water Pulse 28; as Mantine: Take Down 31, Confuse Ray 37, Bounce 40 | Mantine (from 30) |
| Quagsire | wild | 26 | Oxide | Mud Shot, Slam, Mud Bomb, Amnesia | Yawn 31, Earthquake 36 | Quagsire |
| Quagsire | wild | 26 | v3 | Mud Shot, Slam, Mud Bomb, Amnesia | Yawn 31, Earthquake 44 | Quagsire |

## Route 214

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 44 | At the cap |
|---|---|---|---|---|---|---|
| Barboach | old rod | 12 | Oxide | Mud-Slap, Mud Sport, Water Sport, Water Gun | Mud Bomb 14, Amnesia 18, Water Pulse 22, Magnitude 26; as Whiscash: Rest 33, Snore 33, Aqua Tail 39 | Whiscash (from 30) |
| Barboach | old rod | 12 | v3 | Mud-Slap, Mud Sport, Water Sport, Water Gun | Mud Bomb 14, Amnesia 18, Water Pulse 22, Magnitude 26; as Whiscash: Rest 33, Aqua Tail 39 | Whiscash (from 30) |
| Corphish | old rod | 12 | both | Bubble, Harden, ViceGrip | Leer 13, BubbleBeam 20, Protect 23, Knock Off 26; as Crawdaunt: Swift 30, Taunt 34, Night Slash 39, Crabhammer 44 | Crawdaunt (from 30) |
| Chinchou | old rod | 13 | Oxide | Supersonic, Thunder Wave, Flail, Water Gun | Confuse Ray 17, Spark 20, Take Down 23; as Lanturn: Stockpile 27, Swallow 27, Spit Up 27, BubbleBeam 30, Signal Beam 35, Discharge 40 | Lanturn (from 27) |
| Chinchou | old rod | 13 | v3 | Supersonic, Thunder Wave, Flail, Water Gun | Confuse Ray 17, Spark 20, Take Down 23; as Lanturn: Stockpile 27, Swallow 27, Spit Up 27, BubbleBeam 30, Signal Beam 35 | Lanturn (from 27) |
| Wailmer | old rod | 13 | Oxide | Splash, Growl, Water Gun, Rollout | Whirlpool 14, Astonish 17, Water Pulse 21, Mist 24, Rest 27, Brine 31, Water Spout 34, Amnesia 37 | Wailord (from 40) |
| Wailmer | old rod | 13 | v3 | Water Gun, Growl | Water Pulse 21, Mist 24, Rest 27, Brine 31, Amnesia 37 | Wailord (from 40) |
| Froakie | old rod | 14 | Oxide | Growl, Quick Attack, Lick, Water Pulse | Icy Wind 16; as Frogadier: Icy Wind 16, Faint Attack 20, Acrobatics 22, Low Kick 25, Waterfall 30, Fling 35; as Greninja: Scald 37, Dark Pulse 40, Extrasensory 43 | Greninja (from 36) |
| Froakie | old rod | 14 | v3 | Growl, Quick Attack, Lick, Water Pulse | Icy Wind 16; as Frogadier: Icy Wind 16, Faint Attack 20, Acrobatics 22, Low Kick 25, Fling 35; as Greninja: Water Shuriken on evolving, Night Slash on evolving, Scald 37, Dark Pulse 40, Extrasensory 43 | Greninja (from 36) |
| Lombre | good rod | 20 | both | Nature Power, Fake Out, Fury Swipes, Water Sport | nothing | Ludicolo (from 20) |
| Wooper | good rod | 20 | Oxide | Mud Sport, Mud Shot, Slam, Mud Bomb | as Quagsire: Amnesia 24, Yawn 31, Earthquake 36 | Quagsire (from 21) |
| Wooper | good rod | 20 | Oxide | Mud Sport, Mud Shot, Slam, Mud Bomb | as Clodsire: Yawn 21, Bulldoze 24, Poison Jab 30, Megahorn 36, Toxic 40 | Clodsire (from 20) |
| Wooper | good rod | 20 | v3 | Mud Sport, Mud Shot, Slam, Mud Bomb | as Quagsire: Amnesia 24, Yawn 31, Earthquake 44 | Quagsire (from 21) |
| Wooper | good rod | 20 | v3 | Mud Sport, Mud Shot, Slam, Mud Bomb | as Clodsire: Yawn 21, Bulldoze 24, Poison Jab 36, Slam 37, Megahorn 39, Sludge Bomb 39, Toxic 40, Haze 43, Earthquake 44 | Clodsire (from 20) |
| Frogadier | good rod | 22 | Oxide | Water Pulse, Icy Wind, Faint Attack, Acrobatics | Low Kick 25, Waterfall 30, Fling 35; as Greninja: Scald 37, Dark Pulse 40, Extrasensory 43 | Greninja (from 36) |
| Frogadier | good rod | 22 | v3 | Water Pulse, Icy Wind, Faint Attack, Acrobatics | Low Kick 25, Fling 35; as Greninja: Water Shuriken on evolving, Night Slash on evolving, Scald 37, Dark Pulse 40, Extrasensory 43 | Greninja (from 36) |
| Surskit | good rod | 22 | both | Bubble, Quick Attack, Sweet Scent, Water Sport | as Masquerain: Scary Face 26, Stun Spore 33, Silver Wind 40 | Masquerain (from 23) |
| Psyduck | good rod | 24 | both | Water Gun, Disable, Confusion, Water Pulse | Fury Swipes 27, Screech 31; as Golduck: Psych Up 37, Zen Headbutt 44 | Golduck (from 33) |
| Rhyhorn | wild | 26 | both | Stomp, Fury Attack, Scary Face, Rock Blast | Take Down 33, Horn Drill 37; as Rhydon: Hammer Arm 42 | Rhydon (from 42); Rhyperior in Byron |
| Braixen | wild | 27 | both | Role Play, Psybeam, Lucky Chant, Light Screen | Flame Burst 29, Psyshock 34; as Delphox: Mystical Fire 36, Hypnosis 40 | Delphox (from 36) |
| Houndoom | wild | 27 | both | Smog, Roar, Bite, Odor Sleuth | Fire Fang 32, Faint Attack 38, Embargo 44 | Houndoom |
| Ponyta | wild | 27 | Oxide | Ember, Flame Wheel, Stomp, Fire Spin | Take Down 28, Agility 33, Fire Blast 37; as Rapidash: Fury Attack 40 | Rapidash (from 40) |
| Ponyta | wild | 27 | Oxide | Ember, Flame Wheel, Stomp, Fire Spin | as Galarian Rapidash: Stomp 30, Heal Pulse 35, Take Down 43 | Galarian Rapidash (from 27) |
| Ponyta | wild | 27 | v3 | Tail Whip, Ember, Flame Wheel, Stomp | Take Down 28, Agility 33, Fire Blast 37 | Rapidash (from 40) |
| Ponyta | wild | 27 | v3 | Tail Whip, Ember, Flame Wheel, Stomp | as Galarian Rapidash: Psycho Cut on evolving, Stomp 30, Heal Pulse 35, Take Down 43 | Galarian Rapidash (from 27) |
| Salandit | wild | 27 | Oxide | Venom Drench, Flame Burst, Dragon Rage, Toxic | Venoshock 29; as Salazzle: Flamethrower 36, Sludge Bomb 42 | Salazzle (from 30) |
| Salandit | wild | 27 | v3 | Venom Drench, Dragon Rage, Toxic, Flame Burst | Venoshock 29 | Salazzle (from 30) |
| Seel | wild | 27 | both | Ice Shard, Rest, Aqua Ring, Aurora Beam | Aqua Jet 31, Brine 33; as Dewgong: Sheer Cold 34, Take Down 37, Dive 41, Aqua Tail 43 | Dewgong (from 34) |
| Vulpix | wild | 27 | Oxide | Confuse Ray, Imprison, Flamethrower, Safeguard | as Ninetales: Flare Blitz 40 | Ninetales (from 27) |
| Vulpix | wild | 27 | v3 | Imprison, Flamethrower, Will-O-Wisp, Safeguard | as Ninetales: Flare Blitz 40 | Ninetales (from 27) |
| Dwebble | wild | 28 | Oxide | Slash, Rock Tomb, Bug Bite, Night Slash | X-Scissor 31, Rock Slide 34; as Crustle: Rock Slide 34, StompingTantrum 40 | Crustle (from 34) |
| Dwebble | wild | 28 | v3 | Slash, Rock Tomb, Bug Bite, Night Slash | X-Scissor 31, Rock Blast 33, Rock Slide 34; as Crustle: Rock Slide 34, StompingTantrum 40 | Crustle (from 34) |
| Girafarig | wild | 28 | both | Agility, Psybeam, Baton Pass, Assurance | Double Hit 32, Psychic 37, Zen Headbutt 41 | Girafarig |
| Naclstack | wild | 28 | Oxide | Smack Down, Rock Polish, Headbutt, Iron Defense | Recover 30, Rock Slide 34, Stealth Rock 38; as Garganacl: Stealth Rock 40, Heavy Slam 44 | Garganacl (from 38) |
| Naclstack | wild | 28 | v3 | Smack Down, Rock Polish, Headbutt, Iron Defense | Recover 30, Rock Slide 34, Stealth Rock 38; as Garganacl: Hammer Arm on evolving, Stealth Rock 40, Heavy Slam 44 | Garganacl (from 38) |
| Smoochum | wild | 28 | both | Sing, Mean Look, Fake Tears, Lucky Chant | as Jynx: Avalanche 33, Body Slam 39, Wring Out 44 | Jynx (from 30) |
| Charcadet | wild | 29 | Oxide | Clear Smog, Fire Spin, Will-O-Wisp | Night Shade 30, Incinerate 40 | Charcadet; Armarouge in Byron |
| Charcadet | wild | 29 | Oxide | Clear Smog, Fire Spin, Will-O-Wisp | as Ceruledge: Lava Plume 32, Swords Dance 37, Ally Switch 42 | Ceruledge (from 29) |
| Charcadet | wild | 29 | v3 | Clear Smog, Will-O-Wisp | Night Shade 30, Incinerate 40 | Charcadet; Armarouge in Byron |
| Charcadet | wild | 29 | v3 | Clear Smog, Will-O-Wisp | as Ceruledge: Shadow Claw on evolving, Night Slash on evolving, Shadow Sneak on evolving, Quick Guard on evolving, Solar Blade on evolving, Lava Plume 32, Swords Dance 37 | Ceruledge (from 29) |
| Hariyama | wild | 29 | both | Whirlwind, Knock Off, SmellingSalt, Belly Drum | Force Palm 32, Seismic Toss 37, Wake-Up Slap 42 | Hariyama |
| Slugma | wild | 29 | both | Rock Throw, Harden, Recover, AncientPower | Amnesia 31, Lava Plume 38; as Magcargo: Lava Plume 40 | Magcargo (from 38) |

## Ruin Maniac Cave

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 44 | At the cap |
|---|---|---|---|---|---|---|
| Dwebble | wild | 21 to 24 | Oxide | Sand-Attack, Faint Attack, Slash, Rock Tomb | Bug Bite 24, Night Slash 27, X-Scissor 31, Rock Slide 34; as Crustle: Rock Slide 34, StompingTantrum 40 | Crustle (from 34) |
| Dwebble | wild | 21 to 24 | v3 | Sand-Attack, Faint Attack, Slash, Rock Tomb | Bug Bite 24, Night Slash 27, X-Scissor 31, Rock Blast 33, Rock Slide 34; as Crustle: Rock Slide 34, StompingTantrum 40 | Crustle (from 34) |
| Carbink | wild | 22 | both | Sharpen, Smack Down, Guard Split, Reflect | Flail 24, AncientPower 25, Rock Polish 25, Rock Slide 35, Stealth Rock 36, Skill Swap 40, Light Screen 44 | Carbink |
| Ferroseed | wild | 22 | Oxide | Assurance, Pin Missile, Metal Claw, Ingrain | Payback 26, Bullet Seed 30, Gyro Ball 35, Selfdestruct 38; as Ferrothorn: Knock Off 44 | Ferrothorn (from 40) |
| Ferroseed | wild | 22 | v3 | Assurance, Pin Missile, Metal Claw, Ingrain | Payback 26, Bullet Seed 30, Seed Bomb 32, Iron Head 33, Gyro Ball 35, Selfdestruct 38; as Ferrothorn: Knock Off 44 | Ferrothorn (from 40) |
| Golbat | wild | 22 to 24 | Oxide | Astonish, Bite, Wing Attack, Confuse Ray | Air Cutter 27, Mean Look 33, Poison Fang 39 | Crobat (from 40) |
| Golbat | wild | 22 to 24 | v3 | Supersonic, Bite, Wing Attack, Confuse Ray | Air Cutter 27, Mean Look 33, Poison Fang 39 | Crobat (from 40) |
| Klefki | wild | 22 | Oxide | Metal Sound, Crafty Shield, Torment, Draining Kiss | Recycle 33, Imprison 33, Mirror Shot 34, Flash Cannon 36, Foul Play 38, Play Rough 41, Magic Room 44 | Klefki |
| Klefki | wild | 22 | v3 | Metal Sound, Crafty Shield, Torment, Draining Kiss | Recycle 33, Imprison 33, Foul Play 39, Play Rough 41, Magic Room 44 | Klefki |
| Onix | wild | 22 to 23 | Oxide | Screech, Rock Throw, Rage, Rock Tomb | as Steelix: Slam 25, Rock Polish 30, DragonBreath 33, Curse 38, Iron Tail 41 | Steelix (from 22) |
| Onix | wild | 22 to 23 | v3 | Harden, Screech, Rock Throw, Rock Tomb | as Steelix: Slam 25, Rock Polish 30, DragonBreath 33, Curse 38, Iron Tail 41 | Steelix (from 22) |
| Sandygast | wild | 22 to 23 | Oxide | Astonish, Sand Tomb, Sand-Attack, Mega Drain | Bulldoze 24, Hypnosis 28, Giga Drain 35, Iron Defense 36; as Palossand: Shadow Ball 44 | Palossand (from 42) |
| Sandygast | wild | 22 to 23 | v3 | Harden, Shadow Sneak, Sand-Attack, Mega Drain | Bulldoze 24, Hypnosis 28, Earth Power 32, Giga Drain 35, Iron Defense 36, Shadow Ball 39; as Palossand: Shadow Ball 44 | Palossand (from 42) |
| Nacli | wild | 23 | Oxide | Smack Down, Rock Polish, Headbutt, Iron Defense | as Naclstack: Recover 30, Rock Slide 34, Stealth Rock 38; as Garganacl: Stealth Rock 40, Heavy Slam 44 | Garganacl (from 38) |
| Nacli | wild | 23 | v3 | Smack Down, Rock Polish, Headbutt, Iron Defense | as Naclstack: Salt Cure on evolving, Recover 30, Rock Slide 34, Stealth Rock 38; as Garganacl: Hammer Arm on evolving, Stealth Rock 40, Heavy Slam 44 | Garganacl (from 38) |
| Bronzor | wild | 24 | Oxide | Hypnosis, Imprison, Confuse Ray, Extrasensory | Iron Defense 26, Safeguard 30; as Bronzong: Block 33, Gyro Ball 38, Future Sight 43 | Bronzong (from 33) |
| Bronzor | wild | 24 | v3 | Imprison, Confuse Ray, Extrasensory, Iron Head | Iron Defense 26, Safeguard 30, Zen Headbutt 31; as Bronzong: Block 33, Gyro Ball 38, Future Sight 43 | Bronzong (from 33) |

## Trophy Garden

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 44 | At the cap |
|---|---|---|---|---|---|---|
| Pikachu | wild | 22 | both | Thunder Wave, Quick Attack, Double Team, Slam | nothing | Raichu (from 22) |
| Liepard | wild | 23 | both | Fury Swipes, Pursuit, Torment, Fake Out | Assurance 26, Hone Claws 27, Slash 34, Taunt 38, Sucker Punch 43, Nasty Plot 44, Night Slash 44 | Liepard |
| Lopunny | wild | 23 | both | Endure, Return, Quick Attack, Jump Kick | Baton Pass 26, Agility 33, Dizzy Punch 36, Charm 43 | Lopunny |
| Mime Jr. | wild | 23 | Oxide | DoubleSlap, Mimic, Light Screen, Reflect | Psybeam 25, Substitute 29, Recycle 32; as Mr. Mime: Recycle 32, Trick 36, Psychic 39, Role Play 43 | Mr. Mime (from 32) |
| Mime Jr. | wild | 23 | v3 | Meditate, Encore, DoubleSlap, Mimic | Psybeam 25, Light Screen 28, Substitute 29, Reflect 31, Recycle 32; as Mr. Mime: Recycle 32, Trick 36, Role Play 43, Psychic 44 | Mr. Mime (from 32) |
| Skitty | wild | 23 | Oxide | Sing, DoubleSlap, Copycat, Assist | as Delcatty: Hyper Voice 35 | Delcatty (from 23) |
| Skitty | wild | 23 | v3 | Sing, DoubleSlap, Copycat, Assist | as Delcatty: Covet on evolving, Covet 36 | Delcatty (from 23) |
| Smoliv | wild | 23 | Oxide | Helping Hand, Flail, Mega Drain, Grassy Terrain | as Dolliv: Seed Bomb 29, Energy Ball 34; as Arboliva: Leech Seed 39 | Arboliva (from 35) |
| Smoliv | wild | 23 | v3 | Razor Leaf, Helping Hand, Flail, Mega Drain | as Dolliv: Energy Ball 34; as Arboliva: Leech Seed 39, Seed Bomb 44 | Arboliva (from 35) |
| Steenee | wild | 23 | Oxide | Razor Leaf, Sweet Scent, Magical Leaf, Teeter Dance | Stomp 25, Aromatic Mist 32; as Tsareena: Low Sweep 32, Aromatherapy 38, Leaf Storm 44 | Tsareena (from 32) |
| Steenee | wild | 23 | v3 | Razor Leaf, Sweet Scent, Magical Leaf, Teeter Dance | Stomp 25; as Tsareena: Low Sweep 32, Aromatherapy 38 | Tsareena (from 32) |
| Fomantis | wild | 24 | Oxide | Fury Cutter, Growth, Razor Leaf, Ingrain | Sweet Scent 27, Slash 28, X-Scissor 30, Synthesis 31, Leaf Blade 32; as Lurantis: Leaf Blade 34 | Lurantis (from 34) |
| Fomantis | wild | 24 | v3 | Leafage, Growth, Razor Leaf, Ingrain | Sweet Scent 27, Slash 28, X-Scissor 30, Synthesis 31; as Lurantis: Petal Blizzard on evolving | Lurantis (from 34) |
| Galarian Mr Mime | wild | 24 | Oxide | Confusion, Ally Switch, Icy Wind, Double Kick | Psybeam 28, Hypnosis 32, Mirror Coat 36, Sucker Punch 40; as Mr. Rime: Freeze-Dry 44 | Mr. Rime (from 42) |
| Galarian Mr Mime | wild | 24 | v3 | Ice Shard, Confusion, Icy Wind, Double Kick | Psybeam 28, Hypnosis 32, Mirror Coat 36, Sucker Punch 40; as Mr. Rime: Freeze-Dry 44 | Mr. Rime (from 42) |
| Munchlax | wild | 24 | Oxide | Amnesia, Lick, Recycle, Screech | Stockpile 25, Swallow 28, Body Slam 33, Fling 36; as Snorlax: Block 36, Rollout 41, Crunch 44 | Snorlax (from 36) |
| Munchlax | wild | 24 | v3 | Amnesia, Lick, Recycle, Screech | Stockpile 25, Swallow 28, Body Slam 33, Fling 36; as Snorlax: Block 36, Crunch 44 | Snorlax (from 36) |
| Swablu | wild | 24 | both | Sing, Fury Attack, Safeguard, Mist | Take Down 28, Natural Gift 32; as Altaria: DragonBreath 35, Dragon Dance 39 | Altaria (from 35) |
| Dartrix | wild | 25 | Oxide | Astonish, Razor Leaf, Pluck, Ominous Wind | Synthesis 28, Seed Bomb 32, Sucker Punch 36; as Decidueye: Sucker Punch 38 | Decidueye (from 36) |
| Dartrix | wild | 25 | v3 | Peck, Razor Leaf, Pluck, Ominous Wind | Synthesis 28, Seed Bomb 32, Sucker Punch 36; as Decidueye: Sucker Punch 38 | Decidueye (from 36) |
| Pachirisu | wild | 25 | Oxide | Spark, Endure, Swift, Sweet Kiss | Discharge 29, Super Fang 33, Last Resort 37 | Pachirisu |
| Pachirisu | wild | 25 | v3 | Spark, Endure, Swift, Sweet Kiss | Discharge 29, Thunder Fang 32, Super Fang 33, Last Resort 37 | Pachirisu |
| Tangela | wild | 25 | Oxide | Growth, PoisonPowder, Vine Whip, Bind | Mega Drain 26, Stun Spore 29, AncientPower 33; as Tangrowth: Knock Off 36, Natural Gift 40, Slam 43 | Tangrowth (from 35) |
| Tangela | wild | 25 | v3 | Leafage, Growth, PoisonPowder, Vine Whip | Mega Drain 26, Stun Spore 29, AncientPower 33; as Tangrowth: Knock Off 36, Natural Gift 40, Slam 43 | Tangrowth (from 35) |

## Valor Lakefront

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 44 | At the cap |
|---|---|---|---|---|---|---|
| Swablu | wild | 25 | both | Sing, Fury Attack, Safeguard, Mist | Take Down 28, Natural Gift 32; as Altaria: DragonBreath 35, Dragon Dance 39 | Altaria (from 35) |
| Absol | wild | 26 | Oxide | Quick Attack, Razor Wind, Pursuit, Swords Dance | Bite 28, Double Team 33, Slash 36, Future Sight 41, Sucker Punch 44 | Absol |
| Absol | wild | 26 | v3 | Taunt, Quick Attack, Pursuit, Swords Dance | Bite 28, Double Team 33, Slash 36, Future Sight 41, Sucker Punch 44 | Absol |
| Corvisquire | wild | 26 | Oxide | Sand-Attack, Pluck, Steel Wing, Drill Peck | FeatherDance 32, Revenge 38; as Corviknight: Defog 42, Iron Head 44 | Corviknight (from 40) |
| Corvisquire | wild | 26 | v3 | Fury Attack, Sand-Attack, Pluck, Steel Wing | Drill Peck 29, FeatherDance 32, Revenge 38; as Corviknight: Defog 42, Iron Head 44 | Corviknight (from 40) |
| Fletchinder | wild | 26 | both | Quick Attack, Aerial Ace, Flame Charge, Roost | Will-O-Wisp 27, Natural Gift 31; as Talonflame: Acrobatics 38, Me First 42 | Talonflame (from 36) |
| Houndoom | wild | 26 | both | Smog, Roar, Bite, Odor Sleuth | Fire Fang 32, Faint Attack 38, Embargo 44 | Houndoom |
| Liepard | wild | 26 | both | Pursuit, Torment, Fake Out, Assurance | Hone Claws 27, Slash 34, Taunt 38, Sucker Punch 43, Nasty Plot 44, Night Slash 44 | Liepard |
| Ponyta | wild | 26 | Oxide | Ember, Flame Wheel, Stomp, Fire Spin | Take Down 28, Agility 33, Fire Blast 37; as Rapidash: Fury Attack 40 | Rapidash (from 40) |
| Ponyta | wild | 26 | Oxide | Ember, Flame Wheel, Stomp, Fire Spin | as Galarian Rapidash: Stomp 30, Heal Pulse 35, Take Down 43 | Galarian Rapidash (from 26) |
| Ponyta | wild | 26 | v3 | Tail Whip, Ember, Flame Wheel, Stomp | Take Down 28, Agility 33, Fire Blast 37 | Rapidash (from 40) |
| Ponyta | wild | 26 | v3 | Tail Whip, Ember, Flame Wheel, Stomp | as Galarian Rapidash: Psycho Cut on evolving, Stomp 30, Heal Pulse 35, Take Down 43 | Galarian Rapidash (from 26) |
| Glameow | wild | 27 | both | Hypnosis, Faint Attack, Fury Swipes, Charm | Assist 29, Captivate 32, Slash 37; as Purugly: Swagger 38 | Purugly (from 38) |
| Lopunny | wild | 27 | both | Return, Quick Attack, Jump Kick, Baton Pass | Agility 33, Dizzy Punch 36, Charm 43 | Lopunny |
| Minccino | wild | 27 | both | Swift, Encore, Charm, Tickle | nothing | Cinccino (from 27) |
| Skitty | wild | 27 | Oxide | DoubleSlap, Copycat, Assist, Charm | as Delcatty: Hyper Voice 35 | Delcatty (from 27) |
| Skitty | wild | 27 | v3 | DoubleSlap, Copycat, Assist, Charm | as Delcatty: Covet on evolving, Covet 36 | Delcatty (from 27) |
| Pachirisu | wild | 28 | Oxide | Spark, Endure, Swift, Sweet Kiss | Discharge 29, Super Fang 33, Last Resort 37 | Pachirisu |
| Pachirisu | wild | 28 | v3 | Spark, Endure, Swift, Sweet Kiss | Discharge 29, Thunder Fang 32, Super Fang 33, Last Resort 37 | Pachirisu |
| Salandit | wild | 28 | Oxide | Venom Drench, Flame Burst, Dragon Rage, Toxic | Venoshock 29; as Salazzle: Flamethrower 36, Sludge Bomb 42 | Salazzle (from 30) |
| Salandit | wild | 28 | v3 | Venom Drench, Dragon Rage, Toxic, Flame Burst | Venoshock 29 | Salazzle (from 30) |
| Tropius | wild | 28 | both | Razor Leaf, Stomp, Sweet Scent, Whirlwind | Magical Leaf 31, Body Slam 37, Synthesis 41 | Tropius |

## Honey trees

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 44 | At the cap |
|---|---|---|---|---|---|---|
| Charjabug | honey | 23 | Oxide | Mud-Slap, Bug Bite, Bite, Spark | as Vikavolt: Spark 23, Crunch 29, Signal Beam 36 | Vikavolt (from 23) |
| Charjabug | honey | 23 | v3 | Mud-Slap, Bug Bite, Bite, Spark | as Vikavolt: Spark 23, Crunch 29, Signal Beam 33, Discharge 34 | Vikavolt (from 23) |
| Fomantis | honey | 23 | Oxide | Fury Cutter, Growth, Razor Leaf, Ingrain | Sweet Scent 27, Slash 28, X-Scissor 30, Synthesis 31, Leaf Blade 32; as Lurantis: Leaf Blade 34 | Lurantis (from 34) |
| Fomantis | honey | 23 | v3 | Leafage, Growth, Razor Leaf, Ingrain | Sweet Scent 27, Slash 28, X-Scissor 30, Synthesis 31; as Lurantis: Petal Blizzard on evolving | Lurantis (from 34) |
| Heracross | honey | 23 | Oxide | Endure, Fury Attack, Aerial Ace, Brick Break | Counter 25, Take Down 31, Close Combat 37, Reversal 43 | Heracross |
| Heracross | honey | 23 | v3 | Horn Attack, Endure, Fury Attack, Aerial Ace | Counter 25, Brick Break 26, Take Down 31, Close Combat 37, Reversal 43 | Heracross |
| Joltik | honey | 23 | Oxide | Spider Web, Electroweb, Bug Bite, Gastro Acid | Struggle Bug 26, Discharge 29; as Galvantula: Signal Beam 35, Energy Ball 39, Sucker Punch 43 | Galvantula (from 30) |
| Joltik | honey | 23 | v3 | Spider Web, Electroweb, Bug Bite, Gastro Acid | Struggle Bug 26; as Galvantula: Signal Beam 35, Sucker Punch 43 | Galvantula (from 30) |
| Munchlax | honey | 23 | Oxide | Amnesia, Lick, Recycle, Screech | Stockpile 25, Swallow 28, Body Slam 33, Fling 36; as Snorlax: Block 36, Rollout 41, Crunch 44 | Snorlax (from 36) |
| Munchlax | honey | 23 | v3 | Amnesia, Lick, Recycle, Screech | Stockpile 25, Swallow 28, Body Slam 33, Fling 36; as Snorlax: Block 36, Crunch 44 | Snorlax (from 36) |
| Nuzleaf | honey | 23 | Oxide | Harden, Growth, Nature Power, Fake Out | nothing | Shiftry (from 23) |
| Nuzleaf | honey | 23 | v3 | Harden, Growth, Nature Power, Fake Out | as Shiftry: Faint Attack 31 | Shiftry (from 23) |
| Scyther | honey | 23 | Oxide | Pursuit, False Swipe, Agility, Wing Attack | as Scizor: Fury Cutter 25, Slash 29, Razor Wind 33, Iron Defense 37, X-Scissor 41 | Scizor (from 23) |
| Scyther | honey | 23 | Oxide | Pursuit, False Swipe, Agility, Wing Attack | as Kleavor: Aerial Ace 25, Dual Wingbeat 28, Rock Blast 32, X-Scissor 36, Superpower 40, Acrobatics 44 | Kleavor (from 23) |
| Scyther | honey | 23 | v3 | Pursuit, False Swipe, Agility, Wing Attack | as Scizor: Slash 29, Iron Defense 37, Iron Head 44 | Scizor (from 23) |
| Scyther | honey | 23 | v3 | Pursuit, False Swipe, Agility, Wing Attack | as Kleavor: Aerial Ace 25, Dual Wingbeat 28, Rock Blast 32, X-Scissor 36, Superpower 43, Acrobatics 44 | Kleavor (from 23) |
| Snom | honey | 23 | Oxide | Powder Snow, Struggle Bug | as Frosmoth: Bug Buzz 32, Aurora Veil 36, Blizzard 40, Tailwind 44 | Frosmoth (from 30) |
| Snom | honey | 23 | v3 | Powder Snow, Struggle Bug | as Frosmoth: Bug Buzz 32, Aurora Veil 36, Tailwind 44 | Frosmoth (from 30) |
| Swadloon | honey | 23 | Oxide | Tackle, String Shot, Bug Bite, Razor Leaf | as Leavanny: Helping Hand 32, Leaf Blade 36, X-Scissor 39, Entrainment 43 | Leavanny (from 30) |
| Swadloon | honey | 23 | v3 | Tackle, String Shot, Bug Bite, Razor Leaf | as Leavanny: Slash on evolving, Helping Hand 32, X-Scissor 39, Entrainment 43 | Leavanny (from 30) |
| Trumbeak | honey | 23 | Oxide | Rock Blast, Supersonic, Pluck, Roost | Fury Attack 24; as Toucannon: Screech 30, Drill Peck 34, Bullet Seed 40, FeatherDance 44 | Toucannon (from 28) |
| Trumbeak | honey | 23 | v3 | Rock Blast, Supersonic, Pluck, Roost | Fury Attack 24; as Toucannon: Beak Blast on evolving, Screech 30, Bullet Seed 40, FeatherDance 44 | Toucannon (from 28) |
| Vespiquen | honey | 23 | Oxide | Defend Order, Pursuit, Fury Swipes, Power Gem | Heal Order 25, Toxic 27, Slash 31, Captivate 33, Attack Order 37, Swagger 39, Destiny Bond 43 | Vespiquen |
| Vespiquen | honey | 23 | v3 | Defend Order, Pursuit, Fury Swipes, Power Gem | Heal Order 25, Toxic 27, Slash 31, Captivate 33, Swagger 39, Attack Order 40, Destiny Bond 43 | Vespiquen |
| Yanma | honey | 23 | Oxide | Double Team, SonicBoom, Detect, Supersonic | Uproar 27, Pursuit 30, AncientPower 33; as Yanmega: Feint 38, Slash 43 | Yanmega (from 35) |
| Yanma | honey | 23 | v3 | Double Team, SonicBoom, Detect, Supersonic | Uproar 27, Pursuit 30, AncientPower 33; as Yanmega: Feint 38, Wing Attack 42, Slash 43 | Yanmega (from 35) |

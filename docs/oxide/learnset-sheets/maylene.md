# Maylene's split: what each catch knows and learns

Written by `tools/oxide/balance/learncheck.py sheets` for check 6 of the learnset baseline (`docs/oxide/learnset-checks.md`). One table per capture area first offered in Maylene's split, whose cap is 39. Each Pokemon is read at the lowest level it is found at there. "Knows at capture" is the last four moves its list gives by that level; "learns by level-up" is every entry it reaches after capture up to 39, evolving on time, with each later stage's moves under its name; "at the cap" is the stage it can be by then and the next one after. A row marked Rewrite shows the learnset rewrite's lists (the tree's) where it differs from the row marked Oxide, Oxide's lists before the learnset rewrite (`da6b92496c`); a row marked both is the same in each. Relearner-only moves and egg moves are left out.

## Eterna City

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 39 | At the cap |
|---|---|---|---|---|---|---|
| Chinchou | good rod | 15 | Oxide | Supersonic, Thunder Wave, Flail, Water Gun | Confuse Ray 17, Spark 20, Take Down 23; as Lanturn: Stockpile 27, Swallow 27, Spit Up 27, BubbleBeam 30, Signal Beam 35 | Lanturn (from 27) |
| Chinchou | good rod | 15 | Rewrite | Thunder Wave, Flail, Water Gun, Screech | Confuse Ray 17, Spark 20, Take Down 23, Icy Wind 26; as Lanturn: Stockpile 27, Swallow 28, Spit Up 29, BubbleBeam 30, Signal Beam 31, Scald 33, Surf 34, Thunderbolt 37 | Lanturn (from 27) |
| Corphish | good rod | 15 | Oxide | Bubble, Harden, ViceGrip, Leer | BubbleBeam 20, Protect 23, Knock Off 26; as Crawdaunt: Swift 30, Taunt 34, Night Slash 39 | Crawdaunt (from 30) |
| Corphish | good rod | 15 | Rewrite | Taunt, ViceGrip, BubbleBeam, Leer | Razor Shell 17, Knock Off 26; as Crawdaunt: Swift 30, Taunt 32, Throat Chop 35, Aerial Ace 36, Night Slash 39 | Crawdaunt (from 30) |
| Buizel | good rod | 17 | Oxide | Quick Attack, Water Gun, Pursuit, Swift | Aqua Jet 21; as Floatzel: Crunch 26, Agility 29, Whirlpool 39 | Floatzel (from 26) |
| Buizel | good rod | 17 | Rewrite | BubbleBeam, Pursuit, Scary Face, Swift | Aqua Jet 21; as Floatzel: Crunch 26, Icy Wind 29, Flip Turn 33, Waterfall 36, Whirlpool 39 | Floatzel (from 26) |
| Carvanha | good rod | 17 | Oxide | Rage, Focus Energy, Scary Face, Ice Fang | Screech 18, Swagger 21, Assurance 26, Crunch 28; as Sharpedo: Slash 30, Aqua Jet 34 | Sharpedo (from 30) |
| Carvanha | good rod | 17 | Rewrite | Bite, Focus Energy, Scary Face, Ice Fang | Screech 18, Swagger 21, Aqua Cutter 23, Assurance 26, Crunch 28; as Sharpedo: Slash 30, Aqua Jet 31, Bug Bite 35, Aerial Ace 37 | Sharpedo (from 30) |
| Poliwag | good rod | 19 | Oxide | Bubble, Hypnosis, Water Gun, DoubleSlap | Body Slam 21, BubbleBeam 25 | Poliwrath (from 25) |
| Poliwag | good rod | 19 | Oxide | Bubble, Hypnosis, Water Gun, DoubleSlap | Body Slam 21, BubbleBeam 25; as Poliwhirl: BubbleBeam 27, Mud Shot 32, Belly Drum 37 | Poliwhirl (from 25); Politoed in Wake |
| Poliwag | good rod | 19 | Rewrite | Water Pulse, Hypnosis, Mud Shot, DoubleSlap | Body Slam 21, BubbleBeam 25; as Poliwhirl: Bulldoze 25; as Poliwrath: Liquidation 34 | Poliwrath (from 25) |
| Poliwag | good rod | 19 | Rewrite | Water Pulse, Hypnosis, Mud Shot, DoubleSlap | Body Slam 21, BubbleBeam 25; as Poliwhirl: Bulldoze 25, BubbleBeam 27, Swagger 28, Low Sweep 30, Mud Shot 32, Throat Chop 35, Liquidation 39 | Poliwhirl (from 25); Politoed in Wake |

## Lake Verity

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 39 | At the cap |
|---|---|---|---|---|---|---|
| Surskit | good rod | 15 | Oxide | Bubble, Quick Attack, Sweet Scent | Water Sport 19; as Masquerain: Gust 22, Scary Face 26, Stun Spore 33 | Masquerain (from 22) |
| Surskit | good rod | 15 | Rewrite | Sticky Web, Quick Attack, Gust, Silver Wind | Water Sport 19; as Masquerain: Gust 22, BubbleBeam 25, Scary Face 26, Mud Bomb 29, Stun Spore 33, Surf 36, Giga Drain 38 | Masquerain (from 22) |
| Wingull | good rod | 15 | Oxide | Growl, Water Gun, Supersonic, Wing Attack | Mist 16, Water Pulse 19, Quick Attack 24; as Pelipper: Protect 25, Roost 31, Stockpile 38, Swallow 38, Spit Up 38 | Pelipper (from 25) |
| Wingull | good rod | 15 | Rewrite | Supersonic, Twister, Wing Attack, Tailwind | Water Pulse 19, Quick Attack 24; as Pelipper: Payback 25, Liquidation 28, Roost 31, Surf 34, Swallow 37, Stockpile 38, Spit Up 39 | Pelipper (from 25) |
| Chinchou | good rod | 16 | Oxide | Supersonic, Thunder Wave, Flail, Water Gun | Confuse Ray 17, Spark 20, Take Down 23; as Lanturn: Stockpile 27, Swallow 27, Spit Up 27, BubbleBeam 30, Signal Beam 35 | Lanturn (from 27) |
| Chinchou | good rod | 16 | Rewrite | Thunder Wave, Flail, Water Gun, Screech | Confuse Ray 17, Spark 20, Take Down 23, Icy Wind 26; as Lanturn: Stockpile 27, Swallow 28, Spit Up 29, BubbleBeam 30, Signal Beam 31, Scald 33, Surf 34, Thunderbolt 37 | Lanturn (from 27) |
| Corphish | good rod | 16 | Oxide | Bubble, Harden, ViceGrip, Leer | BubbleBeam 20, Protect 23, Knock Off 26; as Crawdaunt: Swift 30, Taunt 34, Night Slash 39 | Crawdaunt (from 30) |
| Corphish | good rod | 16 | Rewrite | Taunt, ViceGrip, BubbleBeam, Leer | Razor Shell 17, Knock Off 26; as Crawdaunt: Swift 30, Taunt 32, Throat Chop 35, Aerial Ace 36, Night Slash 39 | Crawdaunt (from 30) |
| Wailmer | good rod | 17 | Oxide | Water Gun, Rollout, Whirlpool, Astonish | Water Pulse 21, Mist 24, Rest 27, Brine 31, Water Spout 34, Amnesia 37 | Wailmer; Wailord in Wake |
| Wailmer | good rod | 17 | Rewrite | Water Gun, Rollout, Whirlpool, Astonish | Water Pulse 21, Mist 24, Rest 27, Bulldoze 29, Brine 31, Water Spout 34, Amnesia 37 | Wailmer; Wailord in Wake |

## Mt. Coronet South

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 39 | At the cap |
|---|---|---|---|---|---|---|
| Barboach | good rod | 16 | Oxide | Mud Sport, Water Sport, Water Gun, Mud Bomb | Amnesia 18, Water Pulse 22, Magnitude 26; as Whiscash: Rest 33, Snore 33, Aqua Tail 39 | Whiscash (from 30) |
| Barboach | good rod | 16 | Rewrite | Scary Face, Water Sport, Water Gun, Mud Bomb | Amnesia 18, Rock Tomb 20, Water Pulse 22, Magnitude 26; as Whiscash: Bulldoze 30, Rest 33, Zen Headbutt 36, Aqua Tail 39 | Whiscash (from 30) |
| Goldeen | good rod | 16 | Oxide | Tail Whip, Water Sport, Supersonic, Horn Attack | Water Pulse 17, Flail 21, Aqua Ring 27, Fury Attack 31 | Seaking (from 33) |
| Goldeen | good rod | 16 | Rewrite | Water Sport, Flip Turn, Water Pulse, Horn Attack | Swagger 17, Flail 21, Aqua Ring 27; as Seaking: Aqua Jet 34, Skull Bash 37 | Seaking (from 33) |
| Corphish | good rod | 18 | Oxide | Bubble, Harden, ViceGrip, Leer | BubbleBeam 20, Protect 23, Knock Off 26; as Crawdaunt: Swift 30, Taunt 34, Night Slash 39 | Crawdaunt (from 30) |
| Corphish | good rod | 18 | Rewrite | ViceGrip, BubbleBeam, Leer, Razor Shell | Knock Off 26; as Crawdaunt: Swift 30, Taunt 32, Throat Chop 35, Aerial Ace 36, Night Slash 39 | Crawdaunt (from 30) |
| Feebas | good rod | 18 | Oxide | Splash, Tackle | Flail 30; as Milotic: Hydro Pump 37 | Milotic (from 30) |
| Feebas | good rod | 18 | Rewrite | Whirlpool, Water Gun, Water Pulse, Tackle | Recover 21, Dragon Tail 24, Captivate 25, Flail 30; as Milotic: Twister 30, Recover 31, Aqua Tail 32, Aurora Beam 33, Dragon Pulse 35, Surf 37 | Milotic (from 30) |
| Corsola | good rod | 20 | Oxide | Bubble, Recover, Refresh, Rock Blast | BubbleBeam 25, Lucky Chant 28, AncientPower 32, Aqua Ring 37 | Corsola |
| Corsola | good rod | 20 | Rewrite | Recover, AncientPower, Bulldoze, Rock Blast | BubbleBeam 25, Lucky Chant 28, Aqua Cutter 33, Liquidation 35, Aqua Ring 37 | Corsola |

## Oreburgh Gate

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 39 | At the cap |
|---|---|---|---|---|---|---|
| Chinchou | good rod | 15 | Oxide | Supersonic, Thunder Wave, Flail, Water Gun | Confuse Ray 17, Spark 20, Take Down 23; as Lanturn: Stockpile 27, Swallow 27, Spit Up 27, BubbleBeam 30, Signal Beam 35 | Lanturn (from 27) |
| Chinchou | good rod | 15 | Rewrite | Thunder Wave, Flail, Water Gun, Screech | Confuse Ray 17, Spark 20, Take Down 23, Icy Wind 26; as Lanturn: Stockpile 27, Swallow 28, Spit Up 29, BubbleBeam 30, Signal Beam 31, Scald 33, Surf 34, Thunderbolt 37 | Lanturn (from 27) |
| Frillish | good rod | 15 | Oxide | Absorb, Night Shade, Ominous Wind, Water Pulse | Imprison 20, Confuse Ray 25, Hex 30, Brine 34, Pain Split 39 | Frillish; Jellicent in Wake |
| Frillish | good rod | 15 | Rewrite | Bubble, Night Shade, Ominous Wind, Water Pulse | Imprison 20, Confuse Ray 25, Hex 30, Brine 34, Dark Pulse 36, Pain Split 39 | Frillish; Jellicent in Wake |
| Goldeen | good rod | 16 | Oxide | Tail Whip, Water Sport, Supersonic, Horn Attack | Water Pulse 17, Flail 21, Aqua Ring 27, Fury Attack 31 | Seaking (from 33) |
| Goldeen | good rod | 16 | Rewrite | Water Sport, Flip Turn, Water Pulse, Horn Attack | Swagger 17, Flail 21, Aqua Ring 27; as Seaking: Aqua Jet 34, Skull Bash 37 | Seaking (from 33) |
| Qwilfish | good rod | 16 | Oxide | Poison Sting, Harden, Minimize, Water Gun | Rollout 17, Toxic Spikes 21, Stockpile 25, Spit Up 25, Revenge 29, Brine 33, Pin Missile 37 | Qwilfish |
| Qwilfish | good rod | 16 | Rewrite | Poison Sting, Minimize, Harden, Water Gun | Rollout 17, Toxic Spikes 21, Spit Up 24, Stockpile 25, Revenge 29, Brine 33, Pin Missile 37 | Qwilfish |
| Poliwag | good rod | 17 | Oxide | Bubble, Hypnosis, Water Gun, DoubleSlap | Body Slam 21, BubbleBeam 25 | Poliwrath (from 25) |
| Poliwag | good rod | 17 | Oxide | Bubble, Hypnosis, Water Gun, DoubleSlap | Body Slam 21, BubbleBeam 25; as Poliwhirl: BubbleBeam 27, Mud Shot 32, Belly Drum 37 | Poliwhirl (from 25); Politoed in Wake |
| Poliwag | good rod | 17 | Rewrite | Water Pulse, Hypnosis, Mud Shot, DoubleSlap | Body Slam 21, BubbleBeam 25; as Poliwhirl: Bulldoze 25; as Poliwrath: Liquidation 34 | Poliwrath (from 25) |
| Poliwag | good rod | 17 | Rewrite | Water Pulse, Hypnosis, Mud Shot, DoubleSlap | Body Slam 21, BubbleBeam 25; as Poliwhirl: Bulldoze 25, BubbleBeam 27, Swagger 28, Low Sweep 30, Mud Shot 32, Throat Chop 35, Liquidation 39 | Poliwhirl (from 25); Politoed in Wake |

## Pokémon Day Care

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 39 | At the cap |
|---|---|---|---|---|---|---|
| Floette | gift | 30 | Oxide | Mega Drain, Draining Kiss, Magical Leaf, Aromatherapy | Giga Drain 31, Dazzling Gleam 36 | Floette; Florges in Wake |
| Floette | gift | 30 | Rewrite | Tearful Look, Covet, Mega Drain, Draining Kiss | Giga Drain 31, Magical Leaf 32, Aromatherapy 33, Dazzling Gleam 36, Wish 38 | Floette; Florges in Wake |

## Ravaged Path

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 39 | At the cap |
|---|---|---|---|---|---|---|
| Barboach | good rod | 15 | Oxide | Mud Sport, Water Sport, Water Gun, Mud Bomb | Amnesia 18, Water Pulse 22, Magnitude 26; as Whiscash: Rest 33, Snore 33, Aqua Tail 39 | Whiscash (from 30) |
| Barboach | good rod | 15 | Rewrite | Scary Face, Water Sport, Water Gun, Mud Bomb | Amnesia 18, Rock Tomb 20, Water Pulse 22, Magnitude 26; as Whiscash: Bulldoze 30, Rest 33, Zen Headbutt 36, Aqua Tail 39 | Whiscash (from 30) |
| Goldeen | good rod | 15 | Oxide | Tail Whip, Water Sport, Supersonic, Horn Attack | Water Pulse 17, Flail 21, Aqua Ring 27, Fury Attack 31 | Seaking (from 33) |
| Goldeen | good rod | 15 | Rewrite | Water Sport, Flip Turn, Water Pulse, Horn Attack | Swagger 17, Flail 21, Aqua Ring 27; as Seaking: Aqua Jet 34, Skull Bash 37 | Seaking (from 33) |
| Corphish | good rod | 17 | Oxide | Bubble, Harden, ViceGrip, Leer | BubbleBeam 20, Protect 23, Knock Off 26; as Crawdaunt: Swift 30, Taunt 34, Night Slash 39 | Crawdaunt (from 30) |
| Corphish | good rod | 17 | Rewrite | ViceGrip, BubbleBeam, Leer, Razor Shell | Knock Off 26; as Crawdaunt: Swift 30, Taunt 32, Throat Chop 35, Aerial Ace 36, Night Slash 39 | Crawdaunt (from 30) |
| Feebas | good rod | 17 | Oxide | Splash, Tackle | Flail 30; as Milotic: Hydro Pump 37 | Milotic (from 30) |
| Feebas | good rod | 17 | Rewrite | Whirlpool, Water Gun, Water Pulse, Tackle | Recover 21, Dragon Tail 24, Captivate 25, Flail 30; as Milotic: Twister 30, Recover 31, Aqua Tail 32, Aurora Beam 33, Dragon Pulse 35, Surf 37 | Milotic (from 30) |
| Frogadier | good rod | 19 | Oxide | Quick Attack, Lick, Water Pulse, Icy Wind | Faint Attack 20, Acrobatics 22, Low Kick 25, Waterfall 30, Fling 35; as Greninja: Scald 37 | Greninja (from 36) |
| Frogadier | good rod | 19 | Rewrite | Lick, Water Pulse, Icy Wind, Thief | Faint Attack 20, Acrobatics 22, Low Kick 25, Mud Shot 27, Waterfall 30, Fling 35; as Greninja: Shadow Sneak 36, Scald 37 | Greninja (from 36) |

## Route 203

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 39 | At the cap |
|---|---|---|---|---|---|---|
| Corphish | good rod | 15 | Oxide | Bubble, Harden, ViceGrip, Leer | BubbleBeam 20, Protect 23, Knock Off 26; as Crawdaunt: Swift 30, Taunt 34, Night Slash 39 | Crawdaunt (from 30) |
| Corphish | good rod | 15 | Rewrite | Taunt, ViceGrip, BubbleBeam, Leer | Razor Shell 17, Knock Off 26; as Crawdaunt: Swift 30, Taunt 32, Throat Chop 35, Aerial Ace 36, Night Slash 39 | Crawdaunt (from 30) |
| Wingull | good rod | 15 | Oxide | Growl, Water Gun, Supersonic, Wing Attack | Mist 16, Water Pulse 19, Quick Attack 24; as Pelipper: Protect 25, Roost 31, Stockpile 38, Swallow 38, Spit Up 38 | Pelipper (from 25) |
| Wingull | good rod | 15 | Rewrite | Supersonic, Twister, Wing Attack, Tailwind | Water Pulse 19, Quick Attack 24; as Pelipper: Payback 25, Liquidation 28, Roost 31, Surf 34, Swallow 37, Stockpile 38, Spit Up 39 | Pelipper (from 25) |
| Carvanha | good rod | 16 | Oxide | Rage, Focus Energy, Scary Face, Ice Fang | Screech 18, Swagger 21, Assurance 26, Crunch 28; as Sharpedo: Slash 30, Aqua Jet 34 | Sharpedo (from 30) |
| Carvanha | good rod | 16 | Rewrite | Bite, Focus Energy, Scary Face, Ice Fang | Screech 18, Swagger 21, Aqua Cutter 23, Assurance 26, Crunch 28; as Sharpedo: Slash 30, Aqua Jet 31, Bug Bite 35, Aerial Ace 37 | Sharpedo (from 30) |
| Chinchou | good rod | 16 | Oxide | Supersonic, Thunder Wave, Flail, Water Gun | Confuse Ray 17, Spark 20, Take Down 23; as Lanturn: Stockpile 27, Swallow 27, Spit Up 27, BubbleBeam 30, Signal Beam 35 | Lanturn (from 27) |
| Chinchou | good rod | 16 | Rewrite | Thunder Wave, Flail, Water Gun, Screech | Confuse Ray 17, Spark 20, Take Down 23, Icy Wind 26; as Lanturn: Stockpile 27, Swallow 28, Spit Up 29, BubbleBeam 30, Signal Beam 31, Scald 33, Surf 34, Thunderbolt 37 | Lanturn (from 27) |
| Froakie | good rod | 17 | Oxide | Quick Attack, Lick, Water Pulse, Icy Wind | as Frogadier: Faint Attack 20, Acrobatics 22, Low Kick 25, Waterfall 30, Fling 35; as Greninja: Scald 37 | Greninja (from 36) |
| Froakie | good rod | 17 | Rewrite | Quick Attack, Lick, Water Pulse, Icy Wind | as Frogadier: Thief 19, Faint Attack 20, Acrobatics 22, Low Kick 25, Mud Shot 27, Waterfall 30, Fling 35; as Greninja: Shadow Sneak 36, Scald 37 | Greninja (from 36) |

## Route 204

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 39 | At the cap |
|---|---|---|---|---|---|---|
| Buizel | good rod | 15 | Oxide | Quick Attack, Water Gun, Pursuit, Swift | Aqua Jet 21; as Floatzel: Crunch 26, Agility 29, Whirlpool 39 | Floatzel (from 26) |
| Buizel | good rod | 15 | Rewrite | BubbleBeam, Pursuit, Scary Face, Swift | Aqua Jet 21; as Floatzel: Crunch 26, Icy Wind 29, Flip Turn 33, Waterfall 36, Whirlpool 39 | Floatzel (from 26) |
| Corphish | good rod | 15 | Oxide | Bubble, Harden, ViceGrip, Leer | BubbleBeam 20, Protect 23, Knock Off 26; as Crawdaunt: Swift 30, Taunt 34, Night Slash 39 | Crawdaunt (from 30) |
| Corphish | good rod | 15 | Rewrite | Taunt, ViceGrip, BubbleBeam, Leer | Razor Shell 17, Knock Off 26; as Crawdaunt: Swift 30, Taunt 32, Throat Chop 35, Aerial Ace 36, Night Slash 39 | Crawdaunt (from 30) |
| Shellos | good rod | 15 | Oxide | Mud Sport, Harden, Water Pulse, Mud Bomb | Hidden Power 16, Body Slam 29 | Gastrodon (from 30) |
| Shellos | good rod | 15 | Rewrite | Mud-Slap, Harden, Water Pulse, Mud Bomb | Hidden Power 16, Swagger 22, Body Slam 29; as Gastrodon: AncientPower 33, Earth Power 35, Clear Smog 37 | Gastrodon (from 30) |
| Surskit | good rod | 15 | Oxide | Bubble, Quick Attack, Sweet Scent | Water Sport 19; as Masquerain: Gust 22, Scary Face 26, Stun Spore 33 | Masquerain (from 22) |
| Surskit | good rod | 15 | Rewrite | Sticky Web, Quick Attack, Gust, Silver Wind | Water Sport 19; as Masquerain: Gust 22, BubbleBeam 25, Scary Face 26, Mud Bomb 29, Stun Spore 33, Surf 36, Giga Drain 38 | Masquerain (from 22) |
| Lotad | good rod | 16 | Oxide | Absorb, Nature Power, Mist, Natural Gift | nothing | Ludicolo (from 17) |
| Lotad | good rod | 16 | Rewrite | Magical Leaf, Water Gun, Mist, Disarming Voice | as Ludicolo: Energy Ball 34 | Ludicolo (from 17) |
| Wooper | good rod | 16 | Oxide | Tail Whip, Mud Sport, Mud Shot, Slam | Mud Bomb 19; as Quagsire: Amnesia 24, Yawn 31, Earthquake 36 | Quagsire (from 20) |
| Wooper | good rod | 16 | Oxide | Tail Whip, Mud Sport, Mud Shot, Slam | as Clodsire: Slam 16, Yawn 21, Bulldoze 24, Poison Jab 30, Megahorn 36 | Clodsire (from 16) |
| Wooper | good rod | 16 | Rewrite | Tail Whip, Poison Sting, Mud Shot, Slam | Mud Bomb 19; as Quagsire: Amnesia 24, Trailblaze 27, Yawn 31, Earthquake 36, Rock Slide 39 | Quagsire (from 20) |
| Wooper | good rod | 16 | Rewrite | Tail Whip, Poison Sting, Mud Shot, Slam | as Clodsire: Slam 16, Rock Tomb 18, Yawn 21, Bulldoze 24, Poison Jab 30, Waterfall 34, Megahorn 36 | Clodsire (from 16) |
| Goldeen | good rod | 17 | Oxide | Water Sport, Supersonic, Horn Attack, Water Pulse | Flail 21, Aqua Ring 27, Fury Attack 31 | Seaking (from 33) |
| Goldeen | good rod | 17 | Rewrite | Flip Turn, Water Pulse, Horn Attack, Swagger | Flail 21, Aqua Ring 27; as Seaking: Aqua Jet 34, Skull Bash 37 | Seaking (from 33) |
| Poliwag | good rod | 17 | Oxide | Bubble, Hypnosis, Water Gun, DoubleSlap | Body Slam 21, BubbleBeam 25 | Poliwrath (from 25) |
| Poliwag | good rod | 17 | Oxide | Bubble, Hypnosis, Water Gun, DoubleSlap | Body Slam 21, BubbleBeam 25; as Poliwhirl: BubbleBeam 27, Mud Shot 32, Belly Drum 37 | Poliwhirl (from 25); Politoed in Wake |
| Poliwag | good rod | 17 | Rewrite | Water Pulse, Hypnosis, Mud Shot, DoubleSlap | Body Slam 21, BubbleBeam 25; as Poliwhirl: Bulldoze 25; as Poliwrath: Liquidation 34 | Poliwrath (from 25) |
| Poliwag | good rod | 17 | Rewrite | Water Pulse, Hypnosis, Mud Shot, DoubleSlap | Body Slam 21, BubbleBeam 25; as Poliwhirl: Bulldoze 25, BubbleBeam 27, Swagger 28, Low Sweep 30, Mud Shot 32, Throat Chop 35, Liquidation 39 | Poliwhirl (from 25); Politoed in Wake |
| Psyduck | good rod | 17 | Oxide | Scratch, Tail Whip, Water Gun, Disable | Confusion 18, Water Pulse 22, Fury Swipes 27, Screech 31; as Golduck: Psych Up 37 | Golduck (from 33) |
| Psyduck | good rod | 17 | Rewrite | Trailblaze, Water Gun, Water Pulse, Disable | Confusion 18, Low Sweep 22, Fury Swipes 27; as Golduck: Surf 34, Psych Up 37 | Golduck (from 33) |
| Seel | good rod | 19 | Oxide | Water Sport, Icy Wind, Encore, Ice Shard | Rest 21, Aqua Ring 23, Aurora Beam 27, Aqua Jet 31, Brine 33; as Dewgong: Sheer Cold 34, Take Down 37 | Dewgong (from 34) |
| Seel | good rod | 19 | Rewrite | Water Sport, Icy Wind, Encore, Ice Shard | Rest 21, Aqua Ring 23, Aurora Beam 27, Aqua Jet 31, Brine 33; as Dewgong: Signal Beam 34, Take Down 37 | Dewgong (from 34) |

## Route 205

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 39 | At the cap |
|---|---|---|---|---|---|---|
| Carvanha | good rod | 15 | Oxide | Bite, Rage, Focus Energy, Scary Face | Ice Fang 16, Screech 18, Swagger 21, Assurance 26, Crunch 28; as Sharpedo: Slash 30, Aqua Jet 34 | Sharpedo (from 30) |
| Carvanha | good rod | 15 | Rewrite | Leer, Bite, Focus Energy, Scary Face | Ice Fang 16, Screech 18, Swagger 21, Aqua Cutter 23, Assurance 26, Crunch 28; as Sharpedo: Slash 30, Aqua Jet 31, Bug Bite 35, Aerial Ace 37 | Sharpedo (from 30) |
| Lotad | good rod | 15 | Oxide | Absorb, Nature Power, Mist, Natural Gift | nothing | Ludicolo (from 16) |
| Lotad | good rod | 15 | Rewrite | Magical Leaf, Water Gun, Mist, Disarming Voice | as Lombre: Natural Gift 16; as Ludicolo: Energy Ball 34 | Ludicolo (from 16) |
| Shellos | good rod | 15 | Oxide | Mud Sport, Harden, Water Pulse, Mud Bomb | Hidden Power 16, Body Slam 29 | Gastrodon (from 30) |
| Shellos | good rod | 15 | Rewrite | Mud-Slap, Harden, Water Pulse, Mud Bomb | Hidden Power 16, Swagger 22, Body Slam 29; as Gastrodon: AncientPower 33, Earth Power 35, Clear Smog 37 | Gastrodon (from 30) |
| Barboach | good rod | 17 | Oxide | Mud Sport, Water Sport, Water Gun, Mud Bomb | Amnesia 18, Water Pulse 22, Magnitude 26; as Whiscash: Rest 33, Snore 33, Aqua Tail 39 | Whiscash (from 30) |
| Barboach | good rod | 17 | Rewrite | Scary Face, Water Sport, Water Gun, Mud Bomb | Amnesia 18, Rock Tomb 20, Water Pulse 22, Magnitude 26; as Whiscash: Bulldoze 30, Rest 33, Zen Headbutt 36, Aqua Tail 39 | Whiscash (from 30) |
| Dewpider | good rod | 17 | Oxide | Infestation, Bite, Aqua Ring, BubbleBeam | Bug Bite 21; as Araquanid: Headbutt 26, Soak 31, Dive 36 | Araquanid (from 22) |
| Dewpider | good rod | 17 | Rewrite | Infestation, Bite, Aqua Ring, BubbleBeam | Sticky Web 19, Bug Bite 21; as Araquanid: Headbutt 26, Spider Web 28, Soak 31, Skitter Smack 34, Dive 36, Waterfall 38 | Araquanid (from 22) |
| Goldeen | good rod | 17 | Oxide | Water Sport, Supersonic, Horn Attack, Water Pulse | Flail 21, Aqua Ring 27, Fury Attack 31 | Seaking (from 33) |
| Goldeen | good rod | 17 | Rewrite | Flip Turn, Water Pulse, Horn Attack, Swagger | Flail 21, Aqua Ring 27; as Seaking: Aqua Jet 34, Skull Bash 37 | Seaking (from 33) |
| Surskit | good rod | 17 | Oxide | Bubble, Quick Attack, Sweet Scent | Water Sport 19; as Masquerain: Gust 22, Scary Face 26, Stun Spore 33 | Masquerain (from 22) |
| Surskit | good rod | 17 | Rewrite | Sticky Web, Quick Attack, Gust, Silver Wind | Water Sport 19; as Masquerain: Gust 22, BubbleBeam 25, Scary Face 26, Mud Bomb 29, Stun Spore 33, Surf 36, Giga Drain 38 | Masquerain (from 22) |
| Froakie | good rod | 19 | Oxide | Quick Attack, Lick, Water Pulse, Icy Wind | Faint Attack 20; as Frogadier: Faint Attack 20, Acrobatics 22, Low Kick 25, Waterfall 30, Fling 35; as Greninja: Scald 37 | Greninja (from 36) |
| Froakie | good rod | 19 | Rewrite | Quick Attack, Lick, Water Pulse, Icy Wind | Faint Attack 20; as Frogadier: Faint Attack 20, Acrobatics 22, Low Kick 25, Mud Shot 27, Waterfall 30, Fling 35; as Greninja: Shadow Sneak 36, Scald 37 | Greninja (from 36) |
| Psyduck | good rod | 19 | Oxide | Tail Whip, Water Gun, Disable, Confusion | Water Pulse 22, Fury Swipes 27, Screech 31; as Golduck: Psych Up 37 | Golduck (from 33) |
| Psyduck | good rod | 19 | Rewrite | Water Gun, Water Pulse, Disable, Confusion | Low Sweep 22, Fury Swipes 27; as Golduck: Surf 34, Psych Up 37 | Golduck (from 33) |

## Route 208

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 39 | At the cap |
|---|---|---|---|---|---|---|
| Clamperl | good rod | 16 | Oxide | Clamp, Water Gun, Whirlpool, Iron Defense | as Huntail: Scary Face 19, Ice Fang 24, Brine 28, Baton Pass 33, Dive 37 | Huntail (from 16) |
| Clamperl | good rod | 16 | Oxide | Clamp, Water Gun, Whirlpool, Iron Defense | as Gorebyss: Amnesia 19, Aqua Ring 24, Captivate 28, Baton Pass 33, Dive 37 | Gorebyss (from 16) |
| Clamperl | good rod | 16 | Rewrite | Clamp, Water Gun, Whirlpool, Iron Defense | as Huntail: Scary Face 19, Ice Fang 24, Brine 28, Baton Pass 33, Flip Turn 35, Dive 37 | Huntail (from 16) |
| Clamperl | good rod | 16 | Rewrite | Clamp, Water Gun, Whirlpool, Iron Defense | as Gorebyss: Amnesia 19, Aqua Ring 24, Captivate 28, Baton Pass 33, Draining Kiss 35, Dive 37 | Gorebyss (from 16) |
| Goldeen | good rod | 16 | Oxide | Tail Whip, Water Sport, Supersonic, Horn Attack | Water Pulse 17, Flail 21, Aqua Ring 27, Fury Attack 31 | Seaking (from 33) |
| Goldeen | good rod | 16 | Rewrite | Water Sport, Flip Turn, Water Pulse, Horn Attack | Swagger 17, Flail 21, Aqua Ring 27; as Seaking: Aqua Jet 34, Skull Bash 37 | Seaking (from 33) |
| Barboach | good rod | 18 | Oxide | Water Sport, Water Gun, Mud Bomb, Amnesia | Water Pulse 22, Magnitude 26; as Whiscash: Rest 33, Snore 33, Aqua Tail 39 | Whiscash (from 30) |
| Barboach | good rod | 18 | Rewrite | Water Sport, Water Gun, Mud Bomb, Amnesia | Rock Tomb 20, Water Pulse 22, Magnitude 26; as Whiscash: Bulldoze 30, Rest 33, Zen Headbutt 36, Aqua Tail 39 | Whiscash (from 30) |
| Feebas | good rod | 18 | Oxide | Splash, Tackle | Flail 30; as Milotic: Hydro Pump 37 | Milotic (from 30) |
| Feebas | good rod | 18 | Rewrite | Whirlpool, Water Gun, Water Pulse, Tackle | Recover 21, Dragon Tail 24, Captivate 25, Flail 30; as Milotic: Twister 30, Recover 31, Aqua Tail 32, Aurora Beam 33, Dragon Pulse 35, Surf 37 | Milotic (from 30) |
| Mareanie | good rod | 20 | Oxide | Peck, Bite, Wide Guard, Venoshock | Toxic Spikes 22, Recover 26, Spike Cannon 29, Pin Missile 34, Toxic 36; as Toxapex: Toxic 39 | Toxapex (from 38) |
| Mareanie | good rod | 20 | Rewrite | Peck, Bite, Wide Guard, Venoshock | Toxic Spikes 22, Recover 26, Spike Cannon 29, Pin Missile 34, Toxic 36, Muddy Water 38 | Toxapex (from 38) |

## Route 209

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 39 | At the cap |
|---|---|---|---|---|---|---|
| Barboach | old rod | 10 | Oxide | Mud-Slap, Mud Sport, Water Sport, Water Gun | Mud Bomb 14, Amnesia 18, Water Pulse 22, Magnitude 26; as Whiscash: Rest 33, Snore 33, Aqua Tail 39 | Whiscash (from 30) |
| Barboach | old rod | 10 | Rewrite | Mud-Slap, Scary Face, Water Sport, Water Gun | Mud Bomb 14, Amnesia 18, Rock Tomb 20, Water Pulse 22, Magnitude 26; as Whiscash: Bulldoze 30, Rest 33, Zen Headbutt 36, Aqua Tail 39 | Whiscash (from 30) |
| Goldeen | old rod | 10 | Oxide | Peck, Tail Whip, Water Sport, Supersonic | Horn Attack 11, Water Pulse 17, Flail 21, Aqua Ring 27, Fury Attack 31 | Seaking (from 33) |
| Goldeen | old rod | 10 | Rewrite | Peck, Water Sport, Flip Turn, Water Pulse | Horn Attack 11, Swagger 17, Flail 21, Aqua Ring 27; as Seaking: Aqua Jet 34, Skull Bash 37 | Seaking (from 33) |
| Corphish | old rod | 11 | Oxide | Bubble, Harden, ViceGrip | Leer 13, BubbleBeam 20, Protect 23, Knock Off 26; as Crawdaunt: Swift 30, Taunt 34, Night Slash 39 | Crawdaunt (from 30) |
| Corphish | old rod | 11 | Rewrite | Bubble, Taunt, ViceGrip | BubbleBeam 12, Leer 13, Razor Shell 17, Knock Off 26; as Crawdaunt: Swift 30, Taunt 32, Throat Chop 35, Aerial Ace 36, Night Slash 39 | Crawdaunt (from 30) |
| Corsola | old rod | 11 | Oxide | Tackle, Harden, Bubble | Recover 13, Refresh 16, Rock Blast 20, BubbleBeam 25, Lucky Chant 28, AncientPower 32, Aqua Ring 37 | Corsola |
| Corsola | old rod | 11 | Rewrite | Tackle, Life Dew, Bubble | Recover 13, AncientPower 16, Bulldoze 18, Rock Blast 20, BubbleBeam 25, Lucky Chant 28, Aqua Cutter 33, Liquidation 35, Aqua Ring 37 | Corsola |
| Finneon | old rod | 12 | Oxide | Pound, Water Gun, Attract | Gust 17, Water Pulse 22, Captivate 26, Safeguard 29; as Lumineon: Aqua Ring 35 | Lumineon (from 31) |
| Finneon | old rod | 12 | Rewrite | Pound, Water Gun, Tailwind, Attract | Water Pulse 13, Pursuit 15, Gust 17, Captivate 26, Safeguard 29; as Lumineon: Flip Turn 31, Aqua Ring 33, Icy Wind 34, Aqua Tail 38 | Lumineon (from 31) |
| Duskull | wild | 17 to 20 | Oxide | Disable, Foresight, Astonish, Confuse Ray | Shadow Sneak 22, Pursuit 25, Curse 30, Will-O-Wisp 33; as Dusclops: Shadow Punch 37 | Dusclops (from 37); Dusknoir in Candice |
| Duskull | wild | 17 to 20 | Rewrite | Disable, Foresight, Astonish, Confuse Ray | Shadow Sneak 22, Pursuit 25, Shadow Claw 27, Curse 30, Will-O-Wisp 33; as Dusclops: Shadow Punch 37, Mean Look 38 | Dusclops (from 37); Dusknoir in Candice |
| Gothita | wild | 17 to 20 | Oxide | Play Nice, Tickle, Psybeam, DoubleSlap | Fake Tears 19, Embargo 19, Psyshock 22, Hypnosis 24, Faint Attack 24, Charm 30; as Gothorita: Heal Block 34, Psych Up 35, Flatter 37, Psychic 39 | Gothorita (from 32); Gothitelle in Wake |
| Gothita | wild | 17 to 20 | Rewrite | Play Nice, Tickle, Psybeam, DoubleSlap | Embargo 18, Fake Tears 19, Psyshock 22, Faint Attack 23, Hypnosis 24, Dark Pulse 27, Charm 30; as Gothorita: Heal Block 32, Psych Up 33, Flatter 37, Psychic 39 | Gothorita (from 32); Gothitelle in Wake |
| Litwick | wild | 17 to 20 | Oxide | Smog, Confuse Ray, Fire Spin, Night Shade | Clear Smog 18, Will-O-Wisp 22, Flame Burst 26, Hex 30, Imprison 35 | Litwick; Lampent in Wake |
| Litwick | wild | 17 to 20 | Rewrite | Smog, Confuse Ray, Fire Spin, Night Shade | Clear Smog 18, Will-O-Wisp 22, Flame Burst 26, Hex 30, Imprison 35, Shadow Ball 36 | Litwick; Lampent in Wake |
| Misdreavus | wild | 17 to 20 | Oxide | Psywave, Spite, Astonish, Confuse Ray | nothing | Mismagius (from 17) |
| Misdreavus | wild | 17 to 20 | Rewrite | Psywave, Spite, Astonish, Confuse Ray | as Mismagius: Hex 27, Confusion 33 | Mismagius (from 17) |
| Sinistea | wild | 17 to 20 | Oxide | Astonish, Withdraw, Aromatic Mist, Mega Drain | as Polteageist: Protect 18, Sucker Punch 24, Aromatherapy 30, Giga Drain 36 | Polteageist (from 17) |
| Sinistea | wild | 17 to 20 | Oxide | Astonish, Withdraw, Aromatic Mist, Mega Drain | as Sinistcha: Foul Play 18, Mega Drain 24, Hex 30, Rage Powder 36 | Sinistcha (from 17) |
| Sinistea | wild | 17 to 20 | Rewrite | Astonish, Withdraw, Mega Drain | as Polteageist: Sucker Punch 24, Hex 29, Aromatherapy 30, Strength Sap 33, Giga Drain 36 | Polteageist (from 17) |
| Sinistea | wild | 17 to 20 | Rewrite | Astonish, Withdraw, Mega Drain | as Sinistcha: Foul Play 18, Mega Drain 24, Snarl 27, Hex 30, Rage Powder 36 | Sinistcha (from 17) |
| Yamask | wild | 17 to 20 | Oxide | Protect, Haze, Disable, Night Shade | Will-O-Wisp 18, Crafty Shield 20, Hex 20, Ominous Wind 25, Curse 32; as Cofagrigus: Mean Look 38, Grudge 38 | Cofagrigus (from 34) |
| Yamask | wild | 17 to 20 | Oxide | Protect, Haze, Disable, Night Shade | Will-O-Wisp 18, Crafty Shield 20, Hex 20, Ominous Wind 25, Curse 32, Mean Look 35, Grudge 36, Shadow Ball 38 | Yamask; Runerigus in Candice |
| Yamask | wild | 17 to 20 | Rewrite | Destiny Bond, Astonish, Disable, Night Shade | Will-O-Wisp 18, Hex 19, Crafty Shield 20, Ominous Wind 25, Mean Look 28, Mud Shot 30, Curse 32; as Cofagrigus: Shadow Ball 34, Mean Look 38 | Cofagrigus (from 34) |
| Yamask | wild | 17 to 20 | Rewrite | Destiny Bond, Astonish, Disable, Night Shade | Will-O-Wisp 18, Hex 19, Crafty Shield 20, Ominous Wind 25, Mean Look 28, Mud Shot 30, Curse 32 | Yamask; Runerigus in Candice |
| Budew | wild | 18 | Oxide | Water Sport, Stun Spore, Mega Drain, Worry Seed | as Roselia: Sweet Scent 31, Ingrain 34, Toxic 37 | Roselia (from 30); Roserade in Wake |
| Budew | wild | 18 | Rewrite | Mega Drain, Magical Leaf, Worry Seed, Confusion | Venoshock 20, Giga Drain 25; as Roselia: Poison Sting 30, Leech Seed 31, Magical Leaf 32, GrassWhistle 33, Toxic Spikes 34, Toxic 37 | Roselia (from 30); Roserade in Wake |
| Buizel | good rod | 18 | Oxide | Quick Attack, Water Gun, Pursuit, Swift | Aqua Jet 21; as Floatzel: Crunch 26, Agility 29, Whirlpool 39 | Floatzel (from 26) |
| Buizel | good rod | 18 | Rewrite | BubbleBeam, Pursuit, Scary Face, Swift | Aqua Jet 21; as Floatzel: Crunch 26, Icy Wind 29, Flip Turn 33, Waterfall 36, Whirlpool 39 | Floatzel (from 26) |
| Buneary | wild | 18 | Oxide | Foresight, Endure, Frustration, Quick Attack | as Lopunny: Jump Kick 23, Baton Pass 26, Agility 33, Dizzy Punch 36 | Lopunny (from 20) |
| Buneary | wild | 18 | Rewrite | Power-Up Punch, Return, Frustration, Quick Attack | as Lopunny: Jump Kick 23, Baton Pass 26, Bite 29, Agility 33, Dizzy Punch 36, Strength 39 | Lopunny (from 20) |
| Dhelmise | wild | 18 to 20 | Oxide | Wrap, Mega Drain, Gyro Ball, Metal Sound | Whirlpool 22, Rapid Spin 28, Anchor Shot 34 | Dhelmise |
| Dhelmise | wild | 18 to 20 | Rewrite | Rapid Spin, Mega Drain, Gyro Ball, Metal Sound | Whirlpool 22, Rapid Spin 28, Anchor Shot 34, Synthesis 35, Seed Bomb 36, Astonish 37 | Dhelmise |
| Drifloon | wild | 18 to 20 | Oxide | Astonish, Gust, Focus Energy, Payback | Stockpile 22, Swallow 27, Spit Up 27; as Drifblim: Ominous Wind 32, Baton Pass 37 | Drifblim (from 28) |
| Drifloon | wild | 18 to 20 | Rewrite | Astonish, Gust, Focus Energy, Payback | Hex 19, Stockpile 22, Strength Sap 24, Swallow 27, Spit Up 28; as Drifblim: Spit Up 28, Ominous Wind 32, Baton Pass 33 | Drifblim (from 28) |
| Fletchinder | wild | 18 | Oxide | Growl, Quick Attack, Aerial Ace, Flame Charge | Roost 22, Will-O-Wisp 27, Natural Gift 31; as Talonflame: Acrobatics 38 | Talonflame (from 36) |
| Fletchinder | wild | 18 | Rewrite | Growl, Quick Attack, Aerial Ace, Flame Charge | Bite 19, Roost 22, Will-O-Wisp 27, Natural Gift 31; as Talonflame: Acrobatics 38 | Talonflame (from 36) |
| Gastly | wild | 18 to 20 | Oxide | Spite, Mean Look, Curse, Night Shade | Confuse Ray 19, Sucker Punch 22; as Haunter: Shadow Punch 25, Payback 28, Shadow Ball 33, Dream Eater 39 | Haunter (from 25); Gengar in Wake |
| Gastly | wild | 18 to 20 | Rewrite | Mean Look, Curse, Night Shade, Sludge | Confuse Ray 19, Sucker Punch 22, Icy Wind 24; as Haunter: Shadow Punch 25, Payback 26, Shadow Ball 33, Clear Smog 36, Dream Eater 39 | Haunter (from 25); Gengar in Wake |
| Klefki | wild | 18 | Oxide | Tackle, Fairy Wind, Spikes, Metal Sound | Crafty Shield 19, Torment 21, Draining Kiss 21, Recycle 33, Imprison 33, Mirror Shot 34, Flash Cannon 36, Foul Play 38 | Klefki |
| Klefki | wild | 18 | Rewrite | Astonish, Tackle, Fairy Wind, Spikes | Crafty Shield 19, Draining Kiss 20, Torment 21, Imprison 32, Recycle 33, Mirror Shot 34, Iron Defense 35, Flash Cannon 36, Foul Play 38 | Klefki |
| Koffing | wild | 18 to 19 | Oxide | Tackle, Smog, SmokeScreen, Assurance | Selfdestruct 19, Sludge 24, Haze 28, Gyro Ball 33 | Weezing (from 35) |
| Koffing | wild | 18 to 19 | Oxide | Tackle, Smog, SmokeScreen, Assurance | as Galarian Weezing: Belch 18, Payback 23, Sludge 26, Toxic 29, Selfdestruct 34, Will-O-Wisp 38 | Galarian Weezing (from 18) |
| Koffing | wild | 18 to 19 | Rewrite | Destiny Bond, Tackle, Smog, Assurance | Sludge 24, Gyro Ball 33, Toxic 35 | Weezing (from 35) |
| Koffing | wild | 18 to 19 | Rewrite | Destiny Bond, Tackle, Smog, Assurance | as Galarian Weezing: Belch 18, Clear Smog 19, Payback 23, Sludge 26, Toxic 29, Play Rough 34, Will-O-Wisp 38 | Galarian Weezing (from 18) |
| Murkrow | wild | 18 | Oxide | Astonish, Pursuit, Haze, Wing Attack | as Honchkrow: Swagger 25, Nasty Plot 35 | Honchkrow (from 18) |
| Murkrow | wild | 18 | Rewrite | Twister, Taunt, Wing Attack, Chilling Water | as Honchkrow: Swagger 25, Drill Peck 34 | Honchkrow (from 18) |
| Pachirisu | wild | 18 | Oxide | Quick Attack, Charm, Spark, Endure | Swift 21, Sweet Kiss 25, Discharge 29, Super Fang 33, Last Resort 37 | Pachirisu |
| Pachirisu | wild | 18 | Rewrite | Electroweb, Charm, Spark, Endure | Bite 19, Swift 21, Sweet Kiss 25, Discharge 29, Super Fang 33, Thunder Fang 35, Last Resort 37 | Pachirisu |
| Ralts | wild | 18 | Oxide | Confusion, Double Team, Teleport, Lucky Chant | as Kirlia: Magical Leaf 22, Calm Mind 25; as Gardevoir: Psychic 33 | Gardevoir (from 30) |
| Ralts | wild | 18 | Oxide | Confusion, Double Team, Teleport, Lucky Chant | as Kirlia: Magical Leaf 22, Calm Mind 25, Psychic 31, Imprison 36, Future Sight 39 | Kirlia (from 20); Gallade in Byron |
| Ralts | wild | 18 | Rewrite | Growl, Draining Kiss, Confusion, Lucky Chant | Magical Leaf 19, Dazzling Gleam 20; as Kirlia: Calm Mind 25; as Gardevoir: Wish 30, Psychic 33, Icy Wind 36, Charge Beam 38 | Gardevoir (from 30) |
| Ralts | wild | 18 | Rewrite | Growl, Draining Kiss, Confusion, Lucky Chant | Magical Leaf 19, Dazzling Gleam 20; as Kirlia: Calm Mind 25, Imprison 36, Future Sight 39 | Kirlia (from 20); Gallade in Byron |
| Sandygast | wild | 18 to 20 | both | Astonish, Sand Tomb, Sand-Attack, Mega Drain | Bulldoze 24, Hypnosis 28, Giga Drain 35, Iron Defense 36 | Sandygast; Palossand in Wake |
| Wooper | good rod | 18 | Oxide | Tail Whip, Mud Sport, Mud Shot, Slam | Mud Bomb 19; as Quagsire: Amnesia 24, Yawn 31, Earthquake 36 | Quagsire (from 20) |
| Wooper | good rod | 18 | Oxide | Tail Whip, Mud Sport, Mud Shot, Slam | as Clodsire: Yawn 21, Bulldoze 24, Poison Jab 30, Megahorn 36 | Clodsire (from 18) |
| Wooper | good rod | 18 | Rewrite | Tail Whip, Poison Sting, Mud Shot, Slam | Mud Bomb 19; as Quagsire: Amnesia 24, Trailblaze 27, Yawn 31, Earthquake 36, Rock Slide 39 | Quagsire (from 20) |
| Wooper | good rod | 18 | Rewrite | Tail Whip, Poison Sting, Mud Shot, Slam | as Clodsire: Rock Tomb 18, Yawn 21, Bulldoze 24, Poison Jab 30, Waterfall 34, Megahorn 36 | Clodsire (from 18) |
| Zubat | wild | 18 to 20 | Oxide | Supersonic, Astonish, Bite, Wing Attack | Confuse Ray 21; as Golbat: Air Cutter 27, Mean Look 33, Poison Fang 39 | Golbat (from 22); Crobat in Wake |
| Zubat | wild | 18 to 20 | Rewrite | Astonish, Screech, Bite, Venoshock | Confuse Ray 21; as Golbat: Air Cutter 25, Poison Jab 30, Mean Look 33, Steel Wing 36, Poison Fang 39 | Golbat (from 22); Crobat in Wake |
| Glameow | wild | 19 | Oxide | Scratch, Growl, Hypnosis, Faint Attack | Fury Swipes 20, Charm 25, Assist 29, Captivate 32, Slash 37; as Purugly: Swagger 38 | Purugly (from 38) |
| Glameow | wild | 19 | Rewrite | Growl, Taunt, Hypnosis, Faint Attack | Fury Swipes 20, Retaliate 22, Charm 25, Aerial Ace 28, Captivate 32, Slash 37; as Purugly: Swagger 38, Strength 39 | Purugly (from 38) |
| Minccino | wild | 19 | Oxide | Sing, Echoed Voice, Swift, Encore | Charm 21, Tickle 23, Tail Slap 28, Wake-Up Slap 31, After You 37, Slam 38, Captivate 39 | Minccino; Cinccino in Wake |
| Minccino | wild | 19 | Rewrite | Swift, DoubleSlap, Sing, Encore | Charm 21, Tickle 23, Strength 27, Tail Slap 28, Wake-Up Slap 31, Facade 33, After You 37, Slam 38, Captivate 39 | Minccino; Cinccino in Wake |
| Tangela | wild | 19 | Oxide | Absorb, Growth, PoisonPowder, Vine Whip | Bind 22, Mega Drain 26, Stun Spore 29, AncientPower 33; as Tangrowth: Knock Off 36 | Tangrowth (from 35) |
| Tangela | wild | 19 | Rewrite | Sleep Powder, PoisonPowder, Vine Whip | Mega Drain 26, Stun Spore 29, AncientPower 33, Giga Drain 34; as Tangrowth: Knock Off 36 | Tangrowth (from 35) |
| Lombre | good rod | 20 | Oxide | Nature Power, Fake Out, Fury Swipes, Water Sport | nothing | Ludicolo (from 20) |
| Lombre | good rod | 20 | Rewrite | Fake Out, Fury Swipes, Natural Gift, Water Sport | as Ludicolo: Energy Ball 34 | Ludicolo (from 20) |
| Meditite | wild | 20 | Oxide | Confusion, Detect, Hidden Power, Mind Reader | Feint 22, Calm Mind 25, Force Palm 29, Hi Jump Kick 32, Psych Up 36 | Medicham (from 37) |
| Meditite | wild | 20 | Rewrite | Confusion, Hidden Power, Force Palm, Mind Reader | Swagger 22, Rock Throw 26, Low Sweep 29, Hi Jump Kick 32, Psych Up 36; as Medicham: Power Trick 39 | Medicham (from 37) |
| Slowpoke | good rod | 20 | Oxide | Growl, Water Gun, Confusion, Disable | Headbutt 25, Water Pulse 29, Zen Headbutt 34; as Slowbro: Withdraw 37 | Slowbro (from 37) |
| Slowpoke | good rod | 20 | Oxide | Growl, Water Gun, Confusion, Disable | Headbutt 25, Water Pulse 29, Zen Headbutt 34, Slack Off 39 | Slowpoke; Slowking in Wake |
| Slowpoke | good rod | 20 | Rewrite | Growl, Water Gun, Confusion, Disable | Headbutt 25, Water Pulse 29, Zen Headbutt 34, Bulldoze 36; as Slowbro: Withdraw 37, Aurora Beam 38, Slack Off 39 | Slowbro (from 37) |
| Slowpoke | good rod | 20 | Rewrite | Growl, Water Gun, Confusion, Disable | Headbutt 25, Water Pulse 29, Zen Headbutt 34, Bulldoze 36, Slack Off 39 | Slowpoke; Slowking in Wake |
| Smoliv | wild | 20 | Oxide | Razor Leaf, Helping Hand, Flail, Mega Drain | Grassy Terrain 23; as Dolliv: Seed Bomb 29, Energy Ball 34; as Arboliva: Leech Seed 39 | Arboliva (from 35) |
| Smoliv | wild | 20 | Rewrite | Razor Leaf, Helping Hand, Flail, Mega Drain | as Dolliv: Charm 25, Mud Shot 26, Seed Bomb 29, Giga Drain 31, Energy Ball 34; as Arboliva: Leech Seed 39 | Arboliva (from 35) |
| Frogadier | good rod | 22 | Oxide | Water Pulse, Icy Wind, Faint Attack, Acrobatics | Low Kick 25, Waterfall 30, Fling 35; as Greninja: Scald 37 | Greninja (from 36) |
| Frogadier | good rod | 22 | Rewrite | Icy Wind, Thief, Faint Attack, Acrobatics | Low Kick 25, Mud Shot 27, Waterfall 30, Fling 35; as Greninja: Shadow Sneak 36, Scald 37 | Greninja (from 36) |
| Spiritomb | static battle | 25 | Oxide | Faint Attack, Hypnosis, Dream Eater, Ominous Wind | Sucker Punch 31, Nasty Plot 37 | Spiritomb |
| Spiritomb | static battle | 25 | Rewrite | Faint Attack, Hypnosis, Dream Eater, Ominous Wind | Sucker Punch 31, Silver Wind 34, Nasty Plot 37 | Spiritomb |

## Route 210

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 39 | At the cap |
|---|---|---|---|---|---|---|
| Scyther | wild | 18 | Oxide | Focus Energy, Pursuit, False Swipe, Agility | as Scizor: Metal Claw 21, Fury Cutter 25, Slash 29, Razor Wind 33, Iron Defense 37 | Scizor (from 18) |
| Scyther | wild | 18 | Oxide | Focus Energy, Pursuit, False Swipe, Agility | as Kleavor: False Swipe 18, Skitter Smack 22, Aerial Ace 25, Dual Wingbeat 28, Rock Blast 32, X-Scissor 36 | Kleavor (from 18) |
| Scyther | wild | 18 | Rewrite | Focus Energy, Pursuit, False Swipe, Agility | as Scizor: Metal Claw 21, Fury Cutter 25, Slash 29, Skitter Smack 34, Iron Defense 37 | Scizor (from 18) |
| Scyther | wild | 18 | Rewrite | Focus Energy, Pursuit, False Swipe, Agility | as Kleavor: False Swipe 18, Bug Bite 19, Rock Smash 20, Skitter Smack 22, Aerial Ace 25, Dual Wingbeat 28, Rock Blast 32, Rock Tomb 34, X-Scissor 36 | Kleavor (from 18) |
| Corvisquire | wild | 19 | Oxide | Leer, Fury Attack, Sand-Attack, Pluck | Steel Wing 20, Drill Peck 26, FeatherDance 32, Revenge 38 | Corvisquire; Corviknight in Wake |
| Corvisquire | wild | 19 | Rewrite | Peck, Leer, Sand-Attack, Pluck | Steel Wing 20, Drill Peck 26, Low Sweep 29, FeatherDance 32, U-turn 35, Revenge 38 | Corvisquire; Corviknight in Wake |
| Fletchinder | wild | 19 | Oxide | Growl, Quick Attack, Aerial Ace, Flame Charge | Roost 22, Will-O-Wisp 27, Natural Gift 31; as Talonflame: Acrobatics 38 | Talonflame (from 36) |
| Fletchinder | wild | 19 | Rewrite | Quick Attack, Aerial Ace, Flame Charge, Bite | Roost 22, Will-O-Wisp 27, Natural Gift 31; as Talonflame: Acrobatics 38 | Talonflame (from 36) |
| Hoothoot | wild | 19 | Oxide | Hypnosis, Peck, Uproar, Reflect | as Noctowl: Confusion 22, Take Down 27, Air Slash 32, Zen Headbutt 37 | Noctowl (from 20) |
| Hoothoot | wild | 19 | Rewrite | Uproar, Reflect, Confusion, Roost | Swift 20; as Noctowl: Take Down 25, Secret Power 29, Air Slash 32, Steel Wing 34, Zen Headbutt 37, Throat Chop 39 | Noctowl (from 20) |
| Ponyta | wild | 19 | Oxide | Tail Whip, Ember, Flame Wheel, Stomp | Fire Spin 24, Take Down 28, Agility 33, Fire Blast 37 | Ponyta; Rapidash in Wake |
| Ponyta | wild | 19 | Oxide | Tail Whip, Ember, Flame Wheel, Stomp | as Galarian Rapidash: Agility 20, Psybeam 25, Stomp 30, Heal Pulse 35 | Galarian Rapidash (from 19) |
| Ponyta | wild | 19 | Rewrite | Flame Charge, Flame Wheel, Charm, Stomp | Bulldoze 21, Fire Spin 24, Take Down 28, Agility 33, Blaze Kick 35, Heat Wave 37 | Ponyta; Rapidash in Wake |
| Ponyta | wild | 19 | Rewrite | Flame Charge, Flame Wheel, Charm, Stomp | as Galarian Rapidash: Agility 20, Psybeam 25, Stomp 30, Heal Pulse 35 | Galarian Rapidash (from 19) |
| Sneasel | wild | 19 to 20 | Oxide | Taunt, Quick Attack, Screech, Faint Attack | Fury Swipes 21, Agility 24, Icy Wind 28, Slash 35 | Sneasel; Weavile in HQ |
| Sneasel | wild | 19 to 20 | Rewrite | Taunt, Quick Attack, Screech, Faint Attack | Fury Swipes 21, Nasty Plot 23, Agility 24, Icy Wind 28, Slash 35, Low Sweep 38 | Sneasel; Weavile in HQ |
| Steenee | wild | 19 | Oxide | Play Nice, Rapid Spin, Razor Leaf, Sweet Scent | Magical Leaf 21, Teeter Dance 23, Stomp 25, Aromatic Mist 32; as Tsareena: Low Sweep 32, Aromatherapy 38 | Tsareena (from 32) |
| Steenee | wild | 19 | Rewrite | Play Nice, Rapid Spin, Razor Leaf, Draining Kiss | Magical Leaf 21, Teeter Dance 23, Stomp 25; as Tsareena: Low Sweep 32, Swagger 33, Trop Kick 34, Aromatherapy 38 | Tsareena (from 32) |
| Swablu | wild | 19 to 20 | Oxide | Astonish, Sing, Fury Attack, Safeguard | Mist 23, Take Down 28, Natural Gift 32; as Altaria: DragonBreath 35, Dragon Dance 39 | Altaria (from 35) |
| Swablu | wild | 19 to 20 | Rewrite | Peck, Astonish, Sing, Safeguard | Dragon Dance 20, Mist 23, Air Slash 24, Take Down 28, Natural Gift 32, Play Rough 34, Steel Wing 35; as Altaria: DragonBreath 35, Mirror Move 36 | Altaria (from 35) |
| Braixen | wild | 20 | Oxide | Ember, Role Play, Psybeam, Lucky Chant | Light Screen 24, Flame Burst 29, Psyshock 34; as Delphox: Mystical Fire 36 | Delphox (from 36) |
| Braixen | wild | 20 | Rewrite | Role Play, Psybeam, Charm, Lucky Chant | Light Screen 24, Mystical Fire 27, Psyshock 34; as Delphox: Mystical Fire 36, Hypnosis 39 | Delphox (from 36) |
| Floragato | wild | 20 | Oxide | Bite, Magical Leaf, Quick Attack, Seed Bomb | Slash 23, Worry Seed 28, Energy Ball 36; as Meowscarada: Flower Trick 36 | Meowscarada (from 36) |
| Floragato | wild | 20 | Rewrite | Bite, Magical Leaf, Quick Attack, Seed Bomb | Slash 23, Worry Seed 28, Charm 34, Energy Ball 36; as Meowscarada: Flower Trick 36, Night Slash 37, Low Sweep 39 | Meowscarada (from 36) |
| Machop | wild | 21 | Oxide | Focus Energy, Karate Chop, Foresight, Seismic Toss | Revenge 22, Vital Throw 25; as Machoke: Submission 32, Wake-Up Slap 36 | Machoke (from 28); Machamp in Wake |
| Machop | wild | 21 | Rewrite | Karate Chop, Foresight, Bullet Punch, Seismic Toss | Revenge 22, Vital Throw 25; as Machoke: Bulldoze 30, Throat Chop 34, Wake-Up Slap 36 | Machoke (from 28); Machamp in Wake |
| Slugma | wild | 21 | both | Smog, Ember, Rock Throw, Harden | Recover 23, AncientPower 26, Amnesia 31, Lava Plume 38 | Magcargo (from 38) |
| Smoliv | wild | 21 | Oxide | Razor Leaf, Helping Hand, Flail, Mega Drain | Grassy Terrain 23; as Dolliv: Seed Bomb 29, Energy Ball 34; as Arboliva: Leech Seed 39 | Arboliva (from 35) |
| Smoliv | wild | 21 | Rewrite | Razor Leaf, Helping Hand, Flail, Mega Drain | as Dolliv: Charm 25, Mud Shot 26, Seed Bomb 29, Giga Drain 31, Energy Ball 34; as Arboliva: Leech Seed 39 | Arboliva (from 35) |

## Route 215

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 39 | At the cap |
|---|---|---|---|---|---|---|
| Drifloon | wild | 19 to 22 | Oxide | Astonish, Gust, Focus Energy, Payback | Stockpile 22, Swallow 27, Spit Up 27; as Drifblim: Ominous Wind 32, Baton Pass 37 | Drifblim (from 28) |
| Drifloon | wild | 19 to 22 | Rewrite | Gust, Focus Energy, Payback, Hex | Stockpile 22, Strength Sap 24, Swallow 27, Spit Up 28; as Drifblim: Spit Up 28, Ominous Wind 32, Baton Pass 33 | Drifblim (from 28) |
| Castform | wild | 20 | Oxide | Tackle, Water Gun, Ember, Powder Snow | Weather Ball 30 | Castform |
| Castform | wild | 20 | Rewrite | Tackle, Ember, Water Gun, Powder Snow | Weather Ball 30, Swagger 39 | Castform |
| Croagunk | wild | 20 to 21 | Oxide | Poison Sting, Taunt, Pursuit, Faint Attack | Revenge 22, Swagger 24, Mud Bomb 29, Sucker Punch 31, Nasty Plot 36 | Toxicroak (from 37) |
| Croagunk | wild | 20 to 21 | Rewrite | Poison Sting, Taunt, Pursuit, Faint Attack | Revenge 22, Swagger 24, Mud Bomb 29, Sucker Punch 31; as Toxicroak: Poison Jab 38 | Toxicroak (from 37) |
| Liepard | wild | 20 | Oxide | Assist, Fury Swipes, Pursuit, Torment | Fake Out 22, Assurance 26, Hone Claws 27, Slash 34, Taunt 38 | Liepard |
| Liepard | wild | 20 | Rewrite | Fury Swipes, Pursuit, Torment, Trailblaze | Fake Out 22, Hone Claws 24, Assurance 26, Dark Pulse 30, Nasty Plot 32, Slash 34, Throat Chop 36, Taunt 38 | Liepard |
| Mienfoo | wild | 20 | Oxide | Rock Smash, Fake Out, DoubleSlap, Force Palm | Bounce 22, Drain Punch 25, Vacuum Wave 32; as Mienshao: Aura Sphere 38 | Mienshao (from 36) |
| Mienfoo | wild | 20 | Rewrite | DoubleSlap, Acrobatics, Agility, Force Palm | Bounce 22, Drain Punch 25, Low Sweep 28, Vacuum Wave 32; as Mienshao: Aura Sphere 38 | Mienshao (from 36) |
| Quagsire | wild | 20 | Oxide | Mud Sport, Mud Shot, Slam, Mud Bomb | Amnesia 24, Yawn 31, Earthquake 36 | Quagsire |
| Quagsire | wild | 20 | Rewrite | Tail Whip, Mud Shot, Slam, Mud Bomb | Amnesia 24, Trailblaze 27, Yawn 31, Earthquake 36, Rock Slide 39 | Quagsire |
| Wormadam | wild | 20 to 21 | Oxide | Tackle, Protect, Bug Bite, Hidden Power | Confusion 23, Razor Leaf 26, Growth 29, Psybeam 32, Captivate 35, Flail 38 | Wormadam |
| Wormadam | wild | 20 to 21 | Rewrite | Tackle, Bug Bite, Confusion, Hidden Power | Razor Leaf 26, Lunge 29, Psybeam 32, Stun Spore 34, Captivate 35, Flail 38 | Wormadam |
| Yanma | wild | 20 to 22 | Oxide | Quick Attack, Double Team, SonicBoom, Detect | Supersonic 22, Uproar 27, Pursuit 30, AncientPower 33; as Yanmega: Feint 38 | Yanmega (from 35) |
| Yanma | wild | 20 to 22 | Rewrite | Foresight, Quick Attack, SonicBoom, Roost | Uproar 27, Pursuit 30, AncientPower 33, Air Cutter 34, Signal Beam 35; as Yanmega: Hypnosis 38 | Yanmega (from 35) |
| Fletchinder | wild | 21 | Oxide | Growl, Quick Attack, Aerial Ace, Flame Charge | Roost 22, Will-O-Wisp 27, Natural Gift 31; as Talonflame: Acrobatics 38 | Talonflame (from 36) |
| Fletchinder | wild | 21 | Rewrite | Quick Attack, Aerial Ace, Flame Charge, Bite | Roost 22, Will-O-Wisp 27, Natural Gift 31; as Talonflame: Acrobatics 38 | Talonflame (from 36) |
| Lickitung | wild | 22 | Oxide | Defense Curl, Knock Off, Wrap, Stomp | Disable 25, Slam 29; as Lickilicky: Rollout 33, Me First 37 | Lickilicky (from 32) |
| Lickitung | wild | 22 | Rewrite | Lick, Supersonic, Knock Off, Stomp | Toxic 23, Disable 25, Slam 29; as Lickilicky: Rollout 33 | Lickilicky (from 32) |

## Route 218

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 39 | At the cap |
|---|---|---|---|---|---|---|
| Finneon | good rod | 24 | Oxide | Water Gun, Attract, Gust, Water Pulse | Captivate 26, Safeguard 29; as Lumineon: Aqua Ring 35 | Lumineon (from 31) |
| Finneon | good rod | 24 | Rewrite | Attract, Water Pulse, Pursuit, Gust | Captivate 26, Safeguard 29; as Lumineon: Flip Turn 31, Aqua Ring 33, Icy Wind 34, Aqua Tail 38 | Lumineon (from 31) |
| Remoraid | good rod | 24 | Oxide | Psybeam, Aurora Beam, BubbleBeam, Focus Energy | as Octillery: Octazooka 25, Bullet Seed 29, Wring Out 36 | Octillery (from 25) |
| Remoraid | good rod | 24 | Rewrite | Screech, Aurora Beam, BubbleBeam, Focus Energy | as Octillery: Octazooka 25, Mud Shot 27, Bullet Seed 29, Round 33, Charge Beam 35, Scald 37 | Octillery (from 25) |
| Chinchou | good rod | 26 | Oxide | Water Gun, Confuse Ray, Spark, Take Down | as Lanturn: Stockpile 27, Swallow 27, Spit Up 27, BubbleBeam 30, Signal Beam 35 | Lanturn (from 27) |
| Chinchou | good rod | 26 | Rewrite | Confuse Ray, Spark, Take Down, Icy Wind | as Lanturn: Stockpile 27, Swallow 28, Spit Up 29, BubbleBeam 30, Signal Beam 31, Scald 33, Surf 34, Thunderbolt 37 | Lanturn (from 27) |
| Shellos | good rod | 26 | Oxide | Harden, Water Pulse, Mud Bomb, Hidden Power | Body Slam 29 | Gastrodon (from 30) |
| Shellos | good rod | 26 | Rewrite | Water Pulse, Mud Bomb, Hidden Power, Swagger | Body Slam 29; as Gastrodon: AncientPower 33, Earth Power 35, Clear Smog 37 | Gastrodon (from 30) |
| Quagsire | good rod | 28 | Oxide | Mud Shot, Slam, Mud Bomb, Amnesia | Yawn 31, Earthquake 36 | Quagsire |
| Quagsire | good rod | 28 | Rewrite | Slam, Mud Bomb, Amnesia, Trailblaze | Yawn 31, Earthquake 36, Rock Slide 39 | Quagsire |

## Route 219

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 39 | At the cap |
|---|---|---|---|---|---|---|
| Shellos | good rod | 15 | Oxide | Mud Sport, Harden, Water Pulse, Mud Bomb | Hidden Power 16, Body Slam 29 | Gastrodon (from 30) |
| Shellos | good rod | 15 | Rewrite | Mud-Slap, Harden, Water Pulse, Mud Bomb | Hidden Power 16, Swagger 22, Body Slam 29; as Gastrodon: AncientPower 33, Earth Power 35, Clear Smog 37 | Gastrodon (from 30) |
| Staryu | good rod | 15 | Oxide | Harden, Water Gun, Rapid Spin, Recover | as Starmie: Confuse Ray 28 | Starmie (from 15) |
| Staryu | good rod | 15 | Rewrite | Harden, Water Gun, Rapid Spin, Recover | as Starmie: Confuse Ray 28, Psybeam 34, Icy Wind 39 | Starmie (from 15) |
| Chinchou | good rod | 16 | Oxide | Supersonic, Thunder Wave, Flail, Water Gun | Confuse Ray 17, Spark 20, Take Down 23; as Lanturn: Stockpile 27, Swallow 27, Spit Up 27, BubbleBeam 30, Signal Beam 35 | Lanturn (from 27) |
| Chinchou | good rod | 16 | Rewrite | Thunder Wave, Flail, Water Gun, Screech | Confuse Ray 17, Spark 20, Take Down 23, Icy Wind 26; as Lanturn: Stockpile 27, Swallow 28, Spit Up 29, BubbleBeam 30, Signal Beam 31, Scald 33, Surf 34, Thunderbolt 37 | Lanturn (from 27) |
| Finneon | good rod | 16 to 17 | Oxide | Pound, Water Gun, Attract | Gust 17, Water Pulse 22, Captivate 26, Safeguard 29; as Lumineon: Aqua Ring 35 | Lumineon (from 31) |
| Finneon | good rod | 16 to 17 | Rewrite | Tailwind, Attract, Water Pulse, Pursuit | Gust 17, Captivate 26, Safeguard 29; as Lumineon: Flip Turn 31, Aqua Ring 33, Icy Wind 34, Aqua Tail 38 | Lumineon (from 31) |

## Solaceon Ruins

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 39 | At the cap |
|---|---|---|---|---|---|---|
| Dwebble | wild | 20 | Oxide | Block, Sand-Attack, Faint Attack, Slash | Rock Tomb 21, Bug Bite 24, Night Slash 27, X-Scissor 31, Rock Slide 34; as Crustle: Rock Slide 34 | Crustle (from 34) |
| Dwebble | wild | 20 | Rewrite | Block, Sand-Attack, Faint Attack, Slash | Rock Tomb 21, Bug Bite 24, Night Slash 27, X-Scissor 31, Rock Slide 34; as Crustle: Rock Slide 34, StompingTantrum 39 | Crustle (from 34) |
| Unown | unown room | 20 | Oxide | Hidden Power | nothing | Unown |
| Unown | unown room | 20 | Rewrite | Hidden Power | Psychic Fangs 34, Psychic 39 | Unown |
| Carbink | wild | 21 | Oxide | Sharpen, Smack Down, Guard Split, Reflect | Flail 24, AncientPower 25, Rock Polish 25, Rock Slide 35, Stealth Rock 36 | Carbink |
| Carbink | wild | 21 | Rewrite | Guard Split, Bulldoze, Reflect, Draining Kiss | Flail 24, AncientPower 25, Rock Polish 26, Dazzling Gleam 27, Rock Tomb 30, Rock Slide 35, Stealth Rock 36 | Carbink |
| Geodude | wild | 21 | Oxide | Rock Polish, Rock Throw, Magnitude, Selfdestruct | Rollout 22, Rock Blast 25; as Graveler: Rock Blast 27, Earthquake 33, Explosion 38 | Graveler (from 25); Golem in Wake |
| Geodude | wild | 21 | Rewrite | Rock Throw, Bulldoze, Magnitude, Rock Polish | Rollout 22, Rock Blast 25; as Graveler: Karate Chop 25, Rock Blast 27, Rock Tomb 30, Earthquake 33, Sucker Punch 36, Iron Head 39 | Graveler (from 25); Golem in Wake |
| Gothita | wild | 21 | Oxide | Psybeam, DoubleSlap, Fake Tears, Embargo | Psyshock 22, Hypnosis 24, Faint Attack 24, Charm 30; as Gothorita: Heal Block 34, Psych Up 35, Flatter 37, Psychic 39 | Gothorita (from 32); Gothitelle in Wake |
| Gothita | wild | 21 | Rewrite | Psybeam, DoubleSlap, Embargo, Fake Tears | Psyshock 22, Faint Attack 23, Hypnosis 24, Dark Pulse 27, Charm 30; as Gothorita: Heal Block 32, Psych Up 33, Flatter 37, Psychic 39 | Gothorita (from 32); Gothitelle in Wake |
| Klefki | wild | 21 | Oxide | Metal Sound, Crafty Shield, Torment, Draining Kiss | Recycle 33, Imprison 33, Mirror Shot 34, Flash Cannon 36, Foul Play 38 | Klefki |
| Klefki | wild | 21 | Rewrite | Spikes, Crafty Shield, Draining Kiss, Torment | Imprison 32, Recycle 33, Mirror Shot 34, Iron Defense 35, Flash Cannon 36, Foul Play 38 | Klefki |
| Nosepass | wild | 21 to 22 | Oxide | Tackle, Harden, Rock Throw, Block | Thunder Wave 25, Rock Slide 31 | Probopass (from 32) |
| Nosepass | wild | 21 to 22 | Rewrite | Smack Down, Rock Throw, Rock Tomb, Block | Bulldoze 22, Thunder Wave 25, Rock Slide 31; as Probopass: Magnet Bomb 32, Iron Head 35, Spark 39 | Probopass (from 32) |
| Yamask | wild | 21 to 23 | Oxide | Night Shade, Will-O-Wisp, Crafty Shield, Hex | Ominous Wind 25, Curse 32; as Cofagrigus: Mean Look 38, Grudge 38 | Cofagrigus (from 34) |
| Yamask | wild | 21 to 23 | Oxide | Night Shade, Will-O-Wisp, Crafty Shield, Hex | Ominous Wind 25, Curse 32, Mean Look 35, Grudge 36, Shadow Ball 38 | Yamask; Runerigus in Candice |
| Yamask | wild | 21 to 23 | Rewrite | Night Shade, Will-O-Wisp, Hex, Crafty Shield | Ominous Wind 25, Mean Look 28, Mud Shot 30, Curse 32; as Cofagrigus: Shadow Ball 34, Mean Look 38 | Cofagrigus (from 34) |
| Yamask | wild | 21 to 23 | Rewrite | Night Shade, Will-O-Wisp, Hex, Crafty Shield | Ominous Wind 25, Mean Look 28, Mud Shot 30, Curse 32 | Yamask; Runerigus in Candice |
| Bronzor | wild | 22 | Oxide | Hypnosis, Imprison, Confuse Ray, Extrasensory | Iron Defense 26, Safeguard 30; as Bronzong: Block 33, Gyro Ball 38 | Bronzong (from 33) |
| Bronzor | wild | 22 | Rewrite | Confuse Ray, Smart Strike, Extrasensory, Bulldoze | Iron Defense 26, Safeguard 30; as Bronzong: Block 33, Iron Head 35, Gyro Ball 38 | Bronzong (from 33) |
| Onix | wild | 22 | Oxide | Screech, Rock Throw, Rage, Rock Tomb | as Steelix: Slam 25, Rock Polish 30, DragonBreath 33, Curse 38 | Steelix (from 22) |
| Onix | wild | 22 | Rewrite | Rock Throw, Rock Tomb, Bulldoze, Bite | as Steelix: Slam 25, DragonBreath 33, Rock Polish 34, Curse 38 | Steelix (from 22) |
| Phanpy | wild | 22 | Oxide | Flail, Take Down, Rollout, Natural Gift | Slam 24; as Donphan: Fury Attack 25, Assurance 31, Scary Face 39 | Donphan (from 25) |
| Phanpy | wild | 22 | Rewrite | Take Down, Bulldoze, Rollout, Natural Gift | Slam 24; as Donphan: Rapid Spin 25, Magnitude 26, Rock Tomb 28, Assurance 31, Trailblaze 35, Scary Face 39 | Donphan (from 25) |
| Glimmet | wild | 23 | Oxide | AncientPower, Rock Polish, Stealth Rock, Venoshock | Selfdestruct 29, Rock Slide 33; as Glimmora: Power Gem 39 | Glimmora (from 35) |
| Glimmet | wild | 23 | Rewrite | AncientPower, Rock Polish, Stealth Rock, Venoshock | Mud Shot 26, Toxic Spikes 29, Rock Slide 33; as Glimmora: Power Gem 39 | Glimmora (from 35) |
| Sinistea | wild | 23 | Oxide | Withdraw, Aromatic Mist, Mega Drain, Protect | as Polteageist: Sucker Punch 24, Aromatherapy 30, Giga Drain 36 | Polteageist (from 23) |
| Sinistea | wild | 23 | Oxide | Withdraw, Aromatic Mist, Mega Drain, Protect | as Sinistcha: Mega Drain 24, Hex 30, Rage Powder 36 | Sinistcha (from 23) |
| Sinistea | wild | 23 | Rewrite | Astonish, Withdraw, Mega Drain | as Polteageist: Sucker Punch 24, Hex 29, Aromatherapy 30, Strength Sap 33, Giga Drain 36 | Polteageist (from 23) |
| Sinistea | wild | 23 | Rewrite | Astonish, Withdraw, Mega Drain | as Sinistcha: Mega Drain 24, Snarl 27, Hex 30, Rage Powder 36 | Sinistcha (from 23) |

## Solaceon Town

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 39 | At the cap |
|---|---|---|---|---|---|---|
| Happiny | wild | 19 | Oxide | Charm, Copycat, Refresh, Sweet Kiss | as Chansey: Minimize 20, Sing 23, Fling 27, Defense Curl 31, Light Screen 34, Egg Bomb 38 | Chansey (from 19); Blissey in Wake |
| Happiny | wild | 19 | Rewrite | Pound, Charm, Refresh, Sweet Kiss | as Chansey: Softboiled 19, Minimize 20, Sing 23, Fling 27, Swift 28, Chilling Water 29, Defense Curl 31, Light Screen 34, Egg Bomb 38 | Chansey (from 19); Blissey in Wake |
| Chatot | wild | 20 to 21 | Oxide | Growl, Mirror Move, Sing, Fury Attack | Chatter 21, Taunt 25, Mimic 29, Roost 33, Uproar 37 | Chatot |
| Chatot | wild | 20 to 21 | Rewrite | Peck, Growl, Mirror Move, Sing | Chatter 21, Taunt 25, Mimic 29, Roost 33, Round 34, Uproar 37, U-turn 39 | Chatot |
| Girafarig | wild | 20 | both | Odor Sleuth, Stomp, Agility, Psybeam | Baton Pass 23, Assurance 28, Double Hit 32, Psychic 37 | Girafarig |
| Lickitung | wild | 20 | Oxide | Supersonic, Defense Curl, Knock Off, Wrap | Stomp 21, Disable 25, Slam 29; as Lickilicky: Rollout 33, Me First 37 | Lickilicky (from 32) |
| Lickitung | wild | 20 | Rewrite | Lick, Supersonic, Knock Off | Stomp 21, Toxic 23, Disable 25, Slam 29; as Lickilicky: Rollout 33 | Lickilicky (from 32) |
| Murkrow | wild | 20 to 21 | Oxide | Astonish, Pursuit, Haze, Wing Attack | as Honchkrow: Swagger 25, Nasty Plot 35 | Honchkrow (from 20) |
| Murkrow | wild | 20 to 21 | Rewrite | Twister, Taunt, Wing Attack, Chilling Water | as Honchkrow: Swagger 25, Drill Peck 34 | Honchkrow (from 20) |
| Trapinch | wild | 20 | Oxide | Bite, Sand-Attack, Faint Attack | Sand Tomb 25, Crunch 33; as Vibrava: DragonBreath 35 | Vibrava (from 35); Flygon in Byron |
| Trapinch | wild | 20 | Rewrite | Bite, Sand-Attack, Faint Attack | Sand Tomb 25, Crunch 33, Dragon Dance 34, Bug Bite 35; as Vibrava: DragonBreath 35, Air Slash 38 | Vibrava (from 35); Flygon in Byron |
| Mankey | wild | 21 | Oxide | Fury Swipes, Karate Chop, Seismic Toss, Screech | Assurance 25; as Primeape: Rage 28, Swagger 35 | Primeape (from 28); Annihilape in Byron |
| Mankey | wild | 21 | Rewrite | Fury Swipes, Karate Chop, Seismic Toss, Screech | Assurance 25; as Primeape: Swagger 33, Rage Fist 34 | Primeape (from 28); Annihilape in Byron |
| Mightyena | wild | 21 | Oxide | Howl, Sand-Attack, Bite, Odor Sleuth | Roar 22, Swagger 27, Assurance 32, Crunch 34, Scary Face 37 | Mightyena |
| Mightyena | wild | 21 | Rewrite | Sand-Attack, Bite, Odor Sleuth, Trailblaze | Roar 22, Swagger 25, Throat Chop 29, Assurance 32, Crunch 34, Scary Face 37, Strength 39 | Mightyena |
| Flaaffy | wild | 22 | Oxide | Growl, ThunderShock, Thunder Wave, Cotton Spore | Charge 25; as Ampharos: ThunderPunch 30, Discharge 34 | Ampharos (from 30) |
| Flaaffy | wild | 22 | Rewrite | Growl, ThunderShock, Thunder Wave, Cotton Spore | Charge 25; as Ampharos: ThunderPunch 30, Discharge 31, DragonBreath 32, Electroweb 36, Volt Switch 38 | Ampharos (from 30) |
| Smoochum | wild | 22 | Oxide | Powder Snow, Confusion, Sing, Mean Look | Fake Tears 25, Lucky Chant 28; as Jynx: Avalanche 33, Body Slam 39 | Jynx (from 30) |
| Smoochum | wild | 22 | Rewrite | Powder Snow, Confusion, Sing, Mean Look | Draining Kiss 23, Fake Tears 25, Lucky Chant 28; as Jynx: Lovely Kiss 30, Ice Punch 31, Wake-Up Slap 32, Avalanche 33, Body Slam 39 | Jynx (from 30) |
| Tropius | wild | 22 | Oxide | Growth, Razor Leaf, Stomp, Sweet Scent | Whirlwind 27, Magical Leaf 31, Body Slam 37 | Tropius |
| Tropius | wild | 22 | Rewrite | Gust, Razor Leaf, Stomp, Bulldoze | Whirlwind 27, Magical Leaf 31, Leaf Blade 34, Body Slam 37 | Tropius |

## Twinleaf Town

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 39 | At the cap |
|---|---|---|---|---|---|---|
| Barboach | good rod | 15 | Oxide | Mud Sport, Water Sport, Water Gun, Mud Bomb | Amnesia 18, Water Pulse 22, Magnitude 26; as Whiscash: Rest 33, Snore 33, Aqua Tail 39 | Whiscash (from 30) |
| Barboach | good rod | 15 | Rewrite | Scary Face, Water Sport, Water Gun, Mud Bomb | Amnesia 18, Rock Tomb 20, Water Pulse 22, Magnitude 26; as Whiscash: Bulldoze 30, Rest 33, Zen Headbutt 36, Aqua Tail 39 | Whiscash (from 30) |
| Corphish | good rod | 15 | Oxide | Bubble, Harden, ViceGrip, Leer | BubbleBeam 20, Protect 23, Knock Off 26; as Crawdaunt: Swift 30, Taunt 34, Night Slash 39 | Crawdaunt (from 30) |
| Corphish | good rod | 15 | Rewrite | Taunt, ViceGrip, BubbleBeam, Leer | Razor Shell 17, Knock Off 26; as Crawdaunt: Swift 30, Taunt 32, Throat Chop 35, Aerial Ace 36, Night Slash 39 | Crawdaunt (from 30) |
| Carvanha | good rod | 16 | Oxide | Rage, Focus Energy, Scary Face, Ice Fang | Screech 18, Swagger 21, Assurance 26, Crunch 28; as Sharpedo: Slash 30, Aqua Jet 34 | Sharpedo (from 30) |
| Carvanha | good rod | 16 | Rewrite | Bite, Focus Energy, Scary Face, Ice Fang | Screech 18, Swagger 21, Aqua Cutter 23, Assurance 26, Crunch 28; as Sharpedo: Slash 30, Aqua Jet 31, Bug Bite 35, Aerial Ace 37 | Sharpedo (from 30) |
| Chinchou | good rod | 16 | Oxide | Supersonic, Thunder Wave, Flail, Water Gun | Confuse Ray 17, Spark 20, Take Down 23; as Lanturn: Stockpile 27, Swallow 27, Spit Up 27, BubbleBeam 30, Signal Beam 35 | Lanturn (from 27) |
| Chinchou | good rod | 16 | Rewrite | Thunder Wave, Flail, Water Gun, Screech | Confuse Ray 17, Spark 20, Take Down 23, Icy Wind 26; as Lanturn: Stockpile 27, Swallow 28, Spit Up 29, BubbleBeam 30, Signal Beam 31, Scald 33, Surf 34, Thunderbolt 37 | Lanturn (from 27) |
| Squirtle | good rod | 17 | Oxide | Bubble, Withdraw, Water Gun, Bite | as Wartortle: Rapid Spin 20, Protect 24, Water Pulse 28, Aqua Tail 32, Skull Bash 36; as Blastoise: Skull Bash 39 | Blastoise (from 36) |
| Squirtle | good rod | 17 | Rewrite | Bubble, Water Gun, Water Pulse, Bite | as Wartortle: Rapid Spin 20, Icy Wind 24, Water Pulse 28, Rock Tomb 30, Aqua Tail 32; as Blastoise: Water Pledge 36, Skull Bash 39 | Blastoise (from 36) |

## Valley Windworks

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 39 | At the cap |
|---|---|---|---|---|---|---|
| Chinchou | good rod | 15 | Oxide | Supersonic, Thunder Wave, Flail, Water Gun | Confuse Ray 17, Spark 20, Take Down 23; as Lanturn: Stockpile 27, Swallow 27, Spit Up 27, BubbleBeam 30, Signal Beam 35 | Lanturn (from 27) |
| Chinchou | good rod | 15 | Rewrite | Thunder Wave, Flail, Water Gun, Screech | Confuse Ray 17, Spark 20, Take Down 23, Icy Wind 26; as Lanturn: Stockpile 27, Swallow 28, Spit Up 29, BubbleBeam 30, Signal Beam 31, Scald 33, Surf 34, Thunderbolt 37 | Lanturn (from 27) |
| Goldeen | good rod | 15 | Oxide | Tail Whip, Water Sport, Supersonic, Horn Attack | Water Pulse 17, Flail 21, Aqua Ring 27, Fury Attack 31 | Seaking (from 33) |
| Goldeen | good rod | 15 | Rewrite | Water Sport, Flip Turn, Water Pulse, Horn Attack | Swagger 17, Flail 21, Aqua Ring 27; as Seaking: Aqua Jet 34, Skull Bash 37 | Seaking (from 33) |
| Barboach | good rod | 17 | Oxide | Mud Sport, Water Sport, Water Gun, Mud Bomb | Amnesia 18, Water Pulse 22, Magnitude 26; as Whiscash: Rest 33, Snore 33, Aqua Tail 39 | Whiscash (from 30) |
| Barboach | good rod | 17 | Rewrite | Scary Face, Water Sport, Water Gun, Mud Bomb | Amnesia 18, Rock Tomb 20, Water Pulse 22, Magnitude 26; as Whiscash: Bulldoze 30, Rest 33, Zen Headbutt 36, Aqua Tail 39 | Whiscash (from 30) |
| Corphish | good rod | 17 | Oxide | Bubble, Harden, ViceGrip, Leer | BubbleBeam 20, Protect 23, Knock Off 26; as Crawdaunt: Swift 30, Taunt 34, Night Slash 39 | Crawdaunt (from 30) |
| Corphish | good rod | 17 | Rewrite | ViceGrip, BubbleBeam, Leer, Razor Shell | Knock Off 26; as Crawdaunt: Swift 30, Taunt 32, Throat Chop 35, Aerial Ace 36, Night Slash 39 | Crawdaunt (from 30) |
| Lombre | good rod | 19 | Oxide | Nature Power, Fake Out, Fury Swipes, Water Sport | nothing | Ludicolo (from 19) |
| Lombre | good rod | 19 | Rewrite | Fake Out, Fury Swipes, Natural Gift, Water Sport | as Ludicolo: Energy Ball 34 | Ludicolo (from 19) |

## Veilstone City

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 39 | At the cap |
|---|---|---|---|---|---|---|
| Elekid | gift | 25 | Oxide | Low Kick, Swift, Shock Wave, Light Screen | ThunderPunch 28; as Electivire: Discharge 37 | Electivire (from 30) |
| Elekid | gift | 25 | Rewrite | Low Kick, Swift, Shock Wave, Light Screen | ThunderPunch 28, Bulldoze 30; as Electivire: Karate Chop 34, Discharge 37 | Electivire (from 30) |

## Honey trees

| Pokemon | Found as | Level | Lists | Knows at capture | Learns by level-up by 39 | At the cap |
|---|---|---|---|---|---|---|
| Aipom | honey | 19 | Oxide | Astonish, Baton Pass, Tickle, Fury Swipes | Swift 22, Screech 25, Agility 29, Double Hit 32; as Ambipom: Double Hit 32, Fling 36, Nasty Plot 39 | Ambipom (from 32) |
| Aipom | honey | 19 | Rewrite | Astonish, Baton Pass, Tickle, Fury Swipes | Bite 20, Swift 22, Screech 25, Agility 29, Double Hit 32; as Ambipom: Double Hit 32, Low Sweep 34, Fling 36, Nasty Plot 39 | Ambipom (from 32) |
| Combee | honey | 19 | Oxide | Sweet Scent, Gust, Bug Bite | as Vespiquen: Power Gem 21, Heal Order 25, Toxic 27, Slash 31, Captivate 33, Attack Order 37, Swagger 39 | Vespiquen (from 21) |
| Combee | honey | 19 | Rewrite | Gust, Bug Bite, Pursuit | Roost 21; as Vespiquen: Power Gem 21, Poison Sting 22, Confuse Ray 23, Defend Order 24, Heal Order 25, Bug Bite 27, Air Cutter 28, Toxic 29, Slash 31, Captivate 33, Pounce 35, Attack Order 37, Swagger 39 | Vespiquen (from 21) |
| Fomantis | honey | 19 | Oxide | Fury Cutter, Growth, Razor Leaf, Ingrain | Sweet Scent 27, Slash 28, X-Scissor 30, Synthesis 31, Leaf Blade 32; as Lurantis: Leaf Blade 34 | Lurantis (from 34) |
| Fomantis | honey | 19 | Rewrite | Leafage, Fury Cutter, Razor Leaf | Slash 28, X-Scissor 30, Synthesis 31, Leaf Blade 32; as Lurantis: Leaf Blade 34 | Lurantis (from 34) |
| Grubbin | honey | 19 | both | Mud-Slap, String Shot, Bug Bite, Bite | as Vikavolt: Spark 23, Crunch 29, Signal Beam 36 | Vikavolt (from 20) |
| Heracross | honey | 19 | Oxide | Endure, Fury Attack, Aerial Ace, Brick Break | Counter 25, Take Down 31, Close Combat 37 | Heracross |
| Heracross | honey | 19 | Rewrite | Horn Attack, Endure, Aerial Ace, Brick Break | Pounce 22, Counter 25, Rock Tomb 28, Take Down 31, Leech Life 34, Close Combat 37 | Heracross |
| Joltik | honey | 19 | Oxide | Thunder Wave, Spider Web, Electroweb, Bug Bite | Gastro Acid 23, Struggle Bug 26, Discharge 29; as Galvantula: Signal Beam 35, Energy Ball 39 | Galvantula (from 30) |
| Joltik | honey | 19 | Rewrite | Thunder Wave, Spider Web, Electroweb, Bug Bite | Gastro Acid 23, Struggle Bug 26, Sucker Punch 28, Discharge 29; as Galvantula: Snarl 32, Signal Beam 35, Energy Ball 39 | Galvantula (from 30) |
| Munchlax | honey | 19 | Oxide | Defense Curl, Amnesia, Lick, Recycle | Screech 20, Stockpile 25, Swallow 28, Body Slam 33, Fling 36; as Snorlax: Block 36 | Snorlax (from 36) |
| Munchlax | honey | 19 | Rewrite | Amnesia, Lick, Recycle, Belly Drum | Screech 20, Headbutt 22, Rest 24, Stockpile 25, Swallow 28, Body Slam 33, Fling 36; as Snorlax: Block 36, Bulldoze 38 | Snorlax (from 36) |
| Nuzleaf | honey | 19 | Oxide | Harden, Growth, Nature Power, Fake Out | nothing | Shiftry (from 19) |
| Nuzleaf | honey | 19 | Rewrite | Harden, Payback, Chilling Water, Fake Out | as Shiftry: Leaf Blade 34 | Shiftry (from 19) |
| Scyther | honey | 19 | Oxide | Focus Energy, Pursuit, False Swipe, Agility | as Scizor: Metal Claw 21, Fury Cutter 25, Slash 29, Razor Wind 33, Iron Defense 37 | Scizor (from 19) |
| Scyther | honey | 19 | Oxide | Focus Energy, Pursuit, False Swipe, Agility | as Kleavor: Skitter Smack 22, Aerial Ace 25, Dual Wingbeat 28, Rock Blast 32, X-Scissor 36 | Kleavor (from 19) |
| Scyther | honey | 19 | Rewrite | Focus Energy, Pursuit, False Swipe, Agility | as Scizor: Metal Claw 21, Fury Cutter 25, Slash 29, Skitter Smack 34, Iron Defense 37 | Scizor (from 19) |
| Scyther | honey | 19 | Rewrite | Focus Energy, Pursuit, False Swipe, Agility | as Kleavor: Bug Bite 19, Rock Smash 20, Skitter Smack 22, Aerial Ace 25, Dual Wingbeat 28, Rock Blast 32, Rock Tomb 34, X-Scissor 36 | Kleavor (from 19) |
| Sewaddle | honey | 19 | Oxide | Tackle, String Shot, Bug Bite, Razor Leaf | as Leavanny: Helping Hand 32, Leaf Blade 36, X-Scissor 39 | Leavanny (from 30) |
| Sewaddle | honey | 19 | Rewrite | Sticky Web, Bug Bite, Razor Leaf, Pounce | as Swadloon: Struggle Bug 22, Bite 26; as Leavanny: Fell Stinger 30, Helping Hand 32, Leaf Blade 36, X-Scissor 39 | Leavanny (from 30) |
| Steenee | honey | 19 | Oxide | Play Nice, Rapid Spin, Razor Leaf, Sweet Scent | Magical Leaf 21, Teeter Dance 23, Stomp 25, Aromatic Mist 32; as Tsareena: Low Sweep 32, Aromatherapy 38 | Tsareena (from 32) |
| Steenee | honey | 19 | Rewrite | Play Nice, Rapid Spin, Razor Leaf, Draining Kiss | Magical Leaf 21, Teeter Dance 23, Stomp 25; as Tsareena: Low Sweep 32, Swagger 33, Trop Kick 34, Aromatherapy 38 | Tsareena (from 32) |
| Yanma | honey | 19 | Oxide | Quick Attack, Double Team, SonicBoom, Detect | Supersonic 22, Uproar 27, Pursuit 30, AncientPower 33; as Yanmega: Feint 38 | Yanmega (from 35) |
| Yanma | honey | 19 | Rewrite | Tackle, Foresight, Quick Attack, SonicBoom | Roost 20, Uproar 27, Pursuit 30, AncientPower 33, Air Cutter 34, Signal Beam 35; as Yanmega: Hypnosis 38 | Yanmega (from 35) |

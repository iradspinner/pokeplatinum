# The learnset pass

Design pass 3 of `docs/oxide/balance-plan.md`, written on `cloud/balance-learnset-pass` from `a5ca2f482` by `tools/oxide/balance/learnset_pass.py`, which regenerates this file. Every species on the pick-list has a new level-up list: the natives take Kaizo's list line by line, the new species keep their donor lists, and both take Ian's adjustments of 2026-09-27. The balance track reviews it line by line and rescores. Nothing here has been seen in game.

Each line gives what the pass added, removed or moved against today's list (the tree at `a5ca2f482`), and for a native, where the result departs from Kaizo's own list and why. A move with two levels learns at both. Level 1 on an evolved stage is its evolution and relearner slot.

## Choices the pass made that the balance track should confirm

- Kaizo's lists sometimes repeat a move. The same move twice at the same level is kept once; a move repeated at another level stays, since each copy is a prompt at that level.
- The seven level-1 picks go in where the list still carried Splash or Teleport, or had no level-1 move once Kaizo's rebuilt Absorb left: Abra, Hoppip, Bounsweet and Magikarp. Kaizo's Azurill, Feebas and Wailmer have no Splash and already open with Present, Water Pulse and Water Pulse, so their picks were not applied.
- Kaizo's Shellder and Meditite had Teleport as their only level-1 move, which would leave a low-level one with no move at all. Their first move comes down to level 1: Take Down and Karate Chop.
- Kaizo's Vise Grip becomes Liquidation, the closest to its physical Water 90 of the three moves the comparison names. Stomp becomes High Horsepower at Kaizo's level everywhere, so Ponyta has it at 6, in Roark's split; Rage becomes Brick Break, the comparison's move "for the type".
- Weather Ball stays (Ledian, Piplup, Prinplup): it reads weather and sets none.
- Cut (Zangoose), Rock Smash (Mudkip, Bagon) and Flash (nine species) stay where Kaizo teaches them by level. The ruling takes them out where they were only HMs, which is the TM pass's work.
- Kaizo's levels stand as Kaizo has them, including those past the League cap of 78; none is re-timed to Oxide's evolution levels.
- Kaizo's Wormadam (Plant) opens at 16, with no level-1 move; it is reached only by evolution at 20, so the list stands.
- Only the pick-list and Magikarp are touched. Species off the pick-list that still learn Splash or Teleport (Spoink, Grumpig, Wynaut, Natu, Xatu, Claydol, Deoxys) or a weather move (Gyarados, which `b6.py` counts as obtainable, and twelve species neither list reaches) are left for the balance track, since each change moves a trainer's default moves.

## How the rules came out

| What | Entries |
|---|---|
| Splash and Teleport go | 96 |
| the move pool's first cut | 29 |
| a weather move | 10 |
| Beat Up leaves the game | 6 |
| Kaizo's rebuilt moves turned into a real move or left out | 92 |

## Natives, on Kaizo's lists

**Charmander (4)**, 10 moves:

- New list: Scratch 1, Bite 1, Ember 2, Bite 10, Metal Claw 16, Roar 19, Dragon Claw 25, Dragon Pulse 28, Flamethrower 34, Dragon Rage 37.
- Added against today's: Bite 1,10; Metal Claw 16; Roar 19; Dragon Claw 25; Dragon Pulse 28.
- Removed against today's: Growl 1; SmokeScreen 10; Scary Face 19; Fire Fang 25; Slash 28; Fire Spin 37.
- Moved against today's: Ember 7 to 2; Dragon Rage 16 to 37.
- Against Kaizo's: the same.

**Charmeleon (5)**, 11 moves:

- New list: Scratch 1, Bite 1, Ember 1, Slash 7, Metal Claw 10, Flame Wheel 17, Roar 21, Crunch 28, Take Down 32, SmokeScreen 39, Flamethrower 43.
- Added against today's: Bite 1; Metal Claw 10; Flame Wheel 17; Roar 21; Crunch 28; Take Down 32.
- Removed against today's: Growl 1; Dragon Rage 17; Scary Face 21; Fire Fang 28; Fire Spin 43.
- Moved against today's: Ember 1,7 to 1; Slash 32 to 7; SmokeScreen 10 to 39; Flamethrower 39 to 43.
- Against Kaizo's: the same.

**Charizard (6)**, 18 moves:

- New list: Dragon Rage 1, Shadow Claw 1, Heat Wave 1, Earthquake 1, Flare Blitz 1, Fire Spin 1, Slash 1, Metal Claw 7, Crunch 10, Fire Fang 17, Wing Attack 21, Dragon Claw 28, Steel Wing 32, Fire Punch 36, Air Slash 42, Dragon Pulse 49, Seismic Toss 59, Flamethrower 66.
- Added against today's: Earthquake 1; Metal Claw 7; Crunch 10; Steel Wing 32; Fire Punch 36; Dragon Pulse 49; Seismic Toss 59.
- Removed against today's: Scratch 1; Growl 1; Ember 1,7; SmokeScreen 1,10; Scary Face 21.
- Moved against today's: Dragon Rage 17 to 1; Heat Wave 59 to 1; Flare Blitz 66 to 1; Fire Spin 49 to 1; Slash 32 to 1; Fire Fang 28 to 17; Wing Attack 36 to 21; Dragon Claw 1 to 28; Air Slash 1 to 42; Flamethrower 42 to 66.
- Against Kaizo's: the same.

**Squirtle (7)**, 14 moves:

- New list: Tackle 1, Water Gun 4, Bite 7, Powder Snow 10, Headbutt 13, BubbleBeam 18, Seismic Toss 19, Ice Punch 22, Body Slam 25, Aqua Tail 28, Crunch 31, Ice Beam 34, Brick Break 37, Hydro Pump 40.
- Added against today's: Powder Snow 10; Headbutt 13; BubbleBeam 18; Seismic Toss 19; Ice Punch 22; Body Slam 25; Crunch 31; Ice Beam 34; Brick Break 37.
- Removed against today's: Tail Whip 4; Bubble 7; Withdraw 10; Rapid Spin 19; Protect 22; Water Pulse 25; Skull Bash 31; Iron Defense 34; Rain Dance 37.
- Moved against today's: Water Gun 13 to 4; Bite 16 to 7.
- Against Kaizo's: the same.

**Wartortle (8)**, 16 moves:

- New list: Bubble 1, Water Pulse 1, Tackle 1, Bite 4, Water Gun 7, Headbutt 10, Ice Fang 13, Seismic Toss 16, BubbleBeam 20, Body Slam 24, Ice Punch 28, Crunch 32, Dive 36, Brick Break 40, Ice Beam 44, Hydro Pump 48.
- Added against today's: Headbutt 10; Ice Fang 13; Seismic Toss 16; BubbleBeam 20; Body Slam 24; Ice Punch 28; Crunch 32; Dive 36; Brick Break 40; Ice Beam 44.
- Removed against today's: Tail Whip 1,4; Withdraw 10; Rapid Spin 20; Protect 24; Aqua Tail 32; Skull Bash 36; Iron Defense 40; Rain Dance 44.
- Moved against today's: Bubble 1,7 to 1; Water Pulse 28 to 1; Bite 16 to 4; Water Gun 13 to 7.
- Against Kaizo's: the same.

**Blastoise (9)**, 17 moves:

- New list: Flash Cannon 1, Tackle 1, Bubble 1, Crunch 1, Water Gun 4, Bite 7, Headbutt 10, Aurora Beam 13, BubbleBeam 16, Iron Head 20, Body Slam 24, Ice Punch 28, Water Pulse 36, Aqua Tail 42, Dark Pulse 46, Ice Beam 53, Hydro Pump 60.
- Added against today's: Crunch 1; Headbutt 10; Aurora Beam 13; BubbleBeam 16; Iron Head 20; Body Slam 24; Ice Punch 28; Dark Pulse 46; Ice Beam 53.
- Removed against today's: Tail Whip 1,4; Withdraw 1,10; Rapid Spin 20; Protect 24; Skull Bash 39; Iron Defense 46; Rain Dance 53.
- Moved against today's: Bubble 1,7 to 1; Water Gun 13 to 4; Bite 16 to 7; Water Pulse 28 to 36; Aqua Tail 32 to 42.
- Rule: Tackle 1 listed twice; one kept.

**Pikachu (25)**, 13 moves:

- New list: Swift 1, ThunderShock 1, Tackle 5, Thunder Wave 10, Shock Wave 13, Quick Attack 18, Iron Tail 21, Seismic Toss 26, Thunderbolt 29, Thunder Wave 34, Double-Edge 37, Submission 42, Volt Tackle 45.
- Added against today's: Swift 1; Tackle 5; Shock Wave 13; Iron Tail 21; Seismic Toss 26; Double-Edge 37; Submission 42; Volt Tackle 45.
- Removed against today's: Growl 1; Tail Whip 5; Double Team 18; Slam 21; Feint 29; Agility 34; Discharge 37; Light Screen 42; Thunder 45.
- Moved against today's: Thunder Wave 10 to 10,34; Quick Attack 13 to 18; Thunderbolt 26 to 29.
- Against Kaizo's: the same.

**Raichu (26)**, 6 moves:

- New list: Surf 1, Quick Attack 1, Focus Blast 1, Discharge 1, Magnet Rise 78, Focus Blast 85.
- Added against today's: Surf 1; Focus Blast 1,85; Discharge 1; Magnet Rise 78.
- Removed against today's: ThunderShock 1; Tail Whip 1; Thunderbolt 1.
- Against Kaizo's: the same.

**Nidoran F (29)**, 13 moves:

- New list: Poison Sting 1, Scratch 1, Double Kick 7, Bite 9, Sludge 13, Dig 19, Body Slam 21, Drill Run 25, Crunch 31, Toxic 33, Earth Power 37, Poison Fang 43, Shadow Ball 45.
- Added against today's: Sludge 13; Dig 19; Body Slam 21; Drill Run 25; Toxic 33; Earth Power 37; Shadow Ball 45.
- Removed against today's: Growl 1; Tail Whip 7; Fury Swipes 19; Helping Hand 25; Toxic Spikes 31; Flatter 33; Captivate 43.
- Moved against today's: Poison Sting 13 to 1; Double Kick 9 to 7; Bite 21 to 9; Crunch 37 to 31; Poison Fang 45 to 43.
- Against Kaizo's: the same.

**Nidorina (30)**, 13 moves:

- New list: Poison Sting 1, Scratch 1, Bite 7, Double Kick 9, Sludge 13, Dig 20, Body Slam 23, Drill Run 28, Poison Jab 35, Drill Peck 38, Earth Power 43, Shadow Claw 50, Poison Fang 58.
- Added against today's: Sludge 13; Dig 20; Body Slam 23; Drill Run 28; Poison Jab 35; Drill Peck 38; Earth Power 43; Shadow Claw 50.
- Removed against today's: Growl 1; Tail Whip 7; Fury Swipes 20; Helping Hand 28; Toxic Spikes 35; Flatter 38; Crunch 43; Captivate 50.
- Moved against today's: Poison Sting 13 to 1; Bite 23 to 7.
- Against Kaizo's: the same.

**Nidoqueen (31)**, 9 moves:

- New list: Thunderbolt 1, Ice Beam 1, Earth Power 1, Superpower 1, Crunch 23, Poison Fang 48, Earthquake 58, Roar 60, Poison Tail 68.
- Added against today's: Thunderbolt 1; Ice Beam 1; Crunch 23; Poison Fang 48; Earthquake 58; Roar 60; Poison Tail 68.
- Removed against today's: Scratch 1; Tail Whip 1; Double Kick 1; Poison Sting 1; Body Slam 23.
- Moved against today's: Earth Power 43 to 1; Superpower 58 to 1.
- Against Kaizo's: the same.

**Nidoran M (32)**, 13 moves:

- New list: Acid 1, Tackle 1, Peck 7, Double Kick 9, Poison Sting 13, Fury Attack 19, Earth Power 21, Drill Peck 25, Poison Fang 31, Thrash 33, Punishment 37, Megahorn 43, Head Smash 55.
- Added against today's: Acid 1; Tackle 1; Earth Power 21; Drill Peck 25; Poison Fang 31; Thrash 33; Punishment 37; Megahorn 43; Head Smash 55.
- Removed against today's: Leer 1; Focus Energy 7; Horn Attack 21; Helping Hand 25; Toxic Spikes 31; Flatter 33; Poison Jab 37; Captivate 43; Horn Drill 45.
- Moved against today's: Peck 1 to 7.
- Against Kaizo's: the same.

**Nidorino (33)**, 13 moves:

- New list: Acid 1, Tackle 1, Peck 7, Double Kick 9, Poison Sting 13, Fury Attack 20, Earth Power 23, Drill Peck 28, Poison Fang 35, Drill Run 38, Megahorn 43, Punishment 50, Head Smash 75.
- Added against today's: Acid 1; Tackle 1; Earth Power 23; Drill Peck 28; Poison Fang 35; Drill Run 38; Megahorn 43; Punishment 50; Head Smash 75.
- Removed against today's: Leer 1; Focus Energy 7; Horn Attack 23; Helping Hand 28; Toxic Spikes 35; Flatter 38; Poison Jab 43; Captivate 50; Horn Drill 58.
- Moved against today's: Peck 1 to 7.
- Against Kaizo's: the same.

**Nidoking (34)**, 8 moves:

- New list: Poison Tail 1, Drill Peck 1, Punishment 1, Double-Edge 1, Poison Jab 23, Megahorn 43, Earthquake 58, Roar 62.
- Added against today's: Poison Tail 1; Drill Peck 1; Punishment 1; Double-Edge 1; Poison Jab 23; Earthquake 58; Roar 62.
- Removed against today's: Peck 1; Focus Energy 1; Double Kick 1; Poison Sting 1; Thrash 23; Earth Power 43.
- Moved against today's: Megahorn 58 to 43.
- Against Kaizo's: the same.

**Clefairy (35)**, 16 moves:

- New list: Pound 1, Swift 1, Lucky Chant 4, Metronome 7, DoubleSlap 10, Seismic Toss 13, Cosmic Power 19, Tri Attack 22, Wake-Up Slap 25, Psychic 28, Lucky Chant 31, Take Down 34, Meteor Mash 37, Shadow Ball 40, Gravity 43, Double-Edge 46.
- Added against today's: Swift 1; Seismic Toss 13; Tri Attack 22; Psychic 28; Take Down 34; Shadow Ball 40; Double-Edge 46.
- Removed against today's: Growl 1; Encore 4; Sing 7; Defense Curl 13; Follow Me 16; Minimize 19; Moonlight 37; Light Screen 40; Healing Wish 46.
- Moved against today's: Lucky Chant 28 to 4,31; Metronome 31 to 7; Cosmic Power 25 to 19; Wake-Up Slap 22 to 25; Meteor Mash 43 to 37; Gravity 34 to 43.
- Against Kaizo's: the same.

**Clefable (36)**, 4 moves:

- New list: ThunderPunch 1, Metronome 1, Tri Attack 1, Air Slash 55.
- Added against today's: ThunderPunch 1; Tri Attack 1; Air Slash 55.
- Removed against today's: Sing 1; DoubleSlap 1; Minimize 1.
- Rule: Teleport 1 out: Splash and Teleport go.

**Vulpix (37)**, 17 moves:

- New list: Ember 1, Quick Attack 4, Roar 7, Confuse Ray 11, Flame Wheel 14, Payback 17, Aurora Beam 19, Bite 21, Flamethrower 24, Will-O-Wisp 27, Grudge 31, Fire Blast 34, Extrasensory 37, Roar 41, Energy Ball 44, Mystical Fire 50, Blast Burn 68.
- Added against today's: Flame Wheel 14; Aurora Beam 19; Bite 21; Energy Ball 44; Mystical Fire 50; Blast Burn 68.
- Removed against today's: Tail Whip 4; Imprison 21; Safeguard 27; Fire Spin 34; Captivate 37; Flare Blitz 40.
- Moved against today's: Quick Attack 11 to 4; Roar 7 to 7,41; Confuse Ray 17 to 11; Payback 31 to 17; Will-O-Wisp 14 to 27; Grudge 41 to 31; Fire Blast 47 to 34; Extrasensory 44 to 37.
- Against Kaizo's: the same.

**Ninetales (38)**, 8 moves:

- New list: Roar 1, Confuse Ray 1, Fire Blast 1, Imprison 1, Dark Pulse 1, Disable 28, Flamethrower 40, Extrasensory 47.
- Added against today's: Roar 1; Fire Blast 1; Imprison 1; Dark Pulse 1; Disable 28; Flamethrower 40; Extrasensory 47.
- Removed against today's: Nasty Plot 1; Ember 1; Quick Attack 1; Safeguard 1; Flare Blitz 40.
- Against Kaizo's: the same.

**Zubat (41)**, 12 moves:

- New list: Leech Life 1, Supersonic 5, Wing Attack 9, Poison Sting 13, Steel Wing 17, Bite 21, Aerial Ace 25, Poison Jab 29, Confuse Ray 33, Crunch 37, Brave Bird 41, Poison Fang 45.
- Added against today's: Poison Sting 13; Steel Wing 17; Aerial Ace 25; Poison Jab 29; Crunch 37; Brave Bird 41.
- Removed against today's: Astonish 9; Air Cutter 25; Mean Look 29; Haze 37; Air Slash 41.
- Moved against today's: Wing Attack 17 to 9; Bite 13 to 21; Confuse Ray 21 to 33; Poison Fang 33 to 45.
- Against Kaizo's: the same.

**Golbat (42)**, 15 moves:

- New list: Cross Poison 1, Leech Life 1, Wing Attack 1, Poison Jab 1, Supersonic 5, Wing Attack 9, Poison Jab 13, Steel Wing 17, Whirlwind 21, Aerial Ace 27, Poison Jab 33, Confuse Ray 39, Crunch 45, Brave Bird 65, Poison Fang 70.
- Added against today's: Cross Poison 1; Poison Jab 1,13,33; Steel Wing 17; Whirlwind 21; Aerial Ace 27; Crunch 45; Brave Bird 65.
- Removed against today's: Screech 1; Astonish 1,9; Bite 13; Air Cutter 27; Mean Look 33; Haze 45; Air Slash 51.
- Moved against today's: Wing Attack 17 to 1,9; Supersonic 1,5 to 5; Confuse Ray 21 to 39; Poison Fang 39 to 70.
- Against Kaizo's: the same.

**Psyduck (54)**, 13 moves:

- New list: Water Gun 1, Scratch 1, Headbutt 5, Psybeam 9, Water Pulse 14, Disable 18, Zen Headbutt 22, Ice Punch 27, Brine 31, Submission 35, Psychic 40, Ice Beam 44, Hydro Pump 48.
- Added against today's: Headbutt 5; Psybeam 9; Ice Punch 27; Brine 31; Submission 35; Psychic 40; Ice Beam 44.
- Removed against today's: Water Sport 1; Tail Whip 5; Confusion 18; Fury Swipes 27; Screech 31; Psych Up 35; Amnesia 44.
- Moved against today's: Water Gun 9 to 1; Water Pulse 22 to 14; Disable 14 to 18; Zen Headbutt 40 to 22.
- Against Kaizo's: the same.

**Golduck (55)**, 16 moves:

- New list: Confusion 1, Water Gun 1, Scratch 1, Psybeam 1, Headbutt 1, Aurora Beam 5, Water Pulse 9, Disable 14, Cross Chop 18, Zen Headbutt 22, Ice Punch 27, Dive 33, Focus Blast 37, Psychic 44, Ice Beam 50, Hydro Pump 56.
- Added against today's: Psybeam 1; Headbutt 1; Aurora Beam 5; Cross Chop 18; Ice Punch 27; Dive 33; Focus Blast 37; Psychic 44; Ice Beam 50.
- Removed against today's: Aqua Jet 1; Water Sport 1; Tail Whip 1,5; Fury Swipes 27; Screech 31; Psych Up 37; Amnesia 50.
- Moved against today's: Confusion 18 to 1; Water Gun 1,9 to 1; Water Pulse 22 to 9; Zen Headbutt 44 to 22.
- Against Kaizo's: the same.

**Mankey (56)**, 15 moves:

- New list: Counter 1, Scratch 1, DoubleSlap 1, Uproar 1, Karate Chop 5, Faint Attack 9, Double Kick 13, Low Kick 17, Rock Throw 21, Assurance 25, Cross Chop 33, Brick Break 37, Rock Slide 41, Punishment 45, Close Combat 49.
- Added against today's: Counter 1; DoubleSlap 1; Uproar 1; Faint Attack 9; Double Kick 13; Rock Throw 21; Brick Break 37; Rock Slide 41.
- Removed against today's: Covet 1; Leer 1; Focus Energy 1; Fury Swipes 9; Seismic Toss 17; Screech 21; Swagger 33; Thrash 41.
- Moved against today's: Karate Chop 13 to 5; Low Kick 1 to 17; Cross Chop 37 to 33.
- Against Kaizo's: Kaizo's Rage 37 became Brick Break.

**Primeape (57)**, 16 moves:

- New list: Fling 1, Scratch 1, Low Kick 1, Uproar 1, Pursuit 1, Fury Swipes 9, Karate Chop 13, Seismic Toss 17, Rock Throw 21, Assurance 25, Brick Break 28, Cross Chop 35, Rock Slide 41, Brick Break 47, Punishment 69, Close Combat 70.
- Added against today's: Uproar 1; Pursuit 1; Rock Throw 21; Brick Break 28,47; Rock Slide 41.
- Removed against today's: Leer 1; Focus Energy 1; Screech 21; Rage 28; Swagger 35; Thrash 47.
- Moved against today's: Cross Chop 41 to 35; Punishment 53 to 69; Close Combat 59 to 70.
- Against Kaizo's: Kaizo's Rage 28 became Brick Break.
- Against Kaizo's: Kaizo's Rage 47 became Brick Break.

**Poliwag (60)**, 13 moves:

- New list: Pound 1, Bubble 5, Mud-Slap 8, Water Gun 11, DoubleSlap 15, BubbleBeam 18, Body Slam 21, Water Pulse 25, Mud Bomb 28, Ice Beam 31, Wake-Up Slap 35, Hydro Pump 38, Hypnosis 41.
- Added against today's: Pound 1; Mud-Slap 8; Water Pulse 25; Ice Beam 31.
- Removed against today's: Water Sport 1; Rain Dance 18; Mud Shot 28; Belly Drum 31.
- Moved against today's: BubbleBeam 25 to 18; Mud Bomb 41 to 28; Hypnosis 8 to 41.
- Against Kaizo's: the same.

**Poliwhirl (61)**, 15 moves:

- New list: Submission 1, Seismic Toss 1, Bubble 1, Bubble 5, Mud Bomb 8, Water Gun 11, DoubleSlap 15, Body Slam 21, Brick Break 25, Dive 27, Mud Shot 32, Ice Punch 37, Wake-Up Slap 43, Hydro Pump 48, Hypnosis 53.
- Added against today's: Submission 1; Seismic Toss 1; Brick Break 25; Dive 27; Ice Punch 37.
- Removed against today's: Water Sport 1; Rain Dance 18; BubbleBeam 27; Belly Drum 37.
- Moved against today's: Mud Bomb 53 to 8; Hypnosis 1,8 to 53.
- Against Kaizo's: the same.

**Poliwrath (62)**, 6 moves:

- New list: BubbleBeam 1, Hypnosis 1, Body Slam 1, Submission 1, Ice Punch 43, Hydro Pump 53.
- Added against today's: Body Slam 1; Ice Punch 43; Hydro Pump 53.
- Removed against today's: DoubleSlap 1; DynamicPunch 43; Mind Reader 53.
- Against Kaizo's: the same.

**Abra (63)**, 1 moves:

- New list: Confusion 1.
- Added against today's: Confusion 1.
- Removed against today's: Teleport 1.
- Rule: Teleport 1 out: Splash and Teleport go.
- Rule: Confusion at 1, the balance track's pick, in place of Splash or Teleport.

**Kadabra (64)**, 11 moves:

- New list: Kinesis 1, Fire Punch 1, Confusion 16, Psycho Cut 18, Disable 24, Psybeam 28, Future Sight 30, Miracle Eye 34, Psychic 40, Recover 42, Role Play 46.
- Added against today's: Fire Punch 1.
- Removed against today's: Teleport 1; Reflect 28; Trick 46.
- Moved against today's: Confusion 1,16 to 16; Psycho Cut 34 to 18; Disable 18 to 24; Psybeam 24 to 28; Future Sight 42 to 30; Miracle Eye 22 to 34; Recover 30 to 42; Role Play 36 to 46.
- Rule: Teleport 1 out: Splash and Teleport go.
- Rule: Teleport 22 out: Splash and Teleport go.
- Rule: Teleport 36 out: Splash and Teleport go.

**Alakazam (65)**, 11 moves:

- New list: Kinesis 1, Fire Punch 1, Confusion 16, Psycho Cut 18, Disable 24, Psybeam 28, Future Sight 30, Miracle Eye 34, Psychic 40, Recover 42, Role Play 46.
- Added against today's: Fire Punch 1; Role Play 46.
- Removed against today's: Teleport 1; Reflect 28; Calm Mind 36; Trick 46.
- Moved against today's: Confusion 1,16 to 16; Psycho Cut 34 to 18; Disable 18 to 24; Psybeam 24 to 28; Future Sight 42 to 30; Miracle Eye 22 to 34; Recover 30 to 42.
- Rule: Teleport 1 out: Splash and Teleport go.
- Rule: Teleport 22 out: Splash and Teleport go.
- Rule: Teleport 36 out: Splash and Teleport go.

**Machop (66)**, 14 moves:

- New list: Karate Chop 1, Pound 1, Rock Throw 7, Seismic Toss 10, Wake-Up Slap 13, Mega Punch 19, Fire Punch 22, Vital Throw 25, Low Kick 31, SmellingSalt 34, ThunderPunch 37, Ice Punch 43, Cross Chop 46, Mega Kick 52.
- Added against today's: Pound 1; Rock Throw 7; Mega Punch 19; Fire Punch 22; SmellingSalt 34; ThunderPunch 37; Ice Punch 43; Mega Kick 52.
- Removed against today's: Leer 1; Focus Energy 7; Foresight 13; Revenge 22; Submission 31; Scary Face 43; DynamicPunch 46.
- Moved against today's: Karate Chop 10 to 1; Seismic Toss 19 to 10; Wake-Up Slap 34 to 13; Low Kick 1 to 31; Cross Chop 37 to 46.
- Against Kaizo's: the same.

**Machoke (67)**, 15 moves:

- New list: Brick Break 1, Low Kick 1, Vital Throw 1, Mega Punch 7, Karate Chop 10, Fire Punch 13, Seismic Toss 19, ThunderPunch 22, Wake-Up Slap 25, SmellingSalt 32, Submission 36, Rock Slide 40, Payback 44, Cross Chop 56, Mega Kick 100.
- Added against today's: Brick Break 1; Mega Punch 7; Fire Punch 13; ThunderPunch 22; SmellingSalt 32; Rock Slide 40; Payback 44; Mega Kick 100.
- Removed against today's: Leer 1; Focus Energy 1,7; Foresight 13; Revenge 22; Scary Face 44; DynamicPunch 51.
- Moved against today's: Vital Throw 25 to 1; Wake-Up Slap 36 to 25; Submission 32 to 36; Cross Chop 40 to 56.
- Against Kaizo's: the same.

**Machamp (68)**, 15 moves:

- New list: Mach Punch 1, Close Combat 1, Bullet Punch 1, Meteor Mash 7, Feint 10, Dizzy Punch 13, Seismic Toss 19, Mega Kick 22, Mega Punch 25, Seismic Toss 32, Superpower 36, Ice Punch 40, ThunderPunch 44, Cross Chop 51, Mach Punch 99.
- Added against today's: Mach Punch 1,99; Close Combat 1; Bullet Punch 1; Meteor Mash 7; Feint 10; Dizzy Punch 13; Mega Kick 22; Mega Punch 25; Superpower 36; Ice Punch 40; ThunderPunch 44.
- Removed against today's: Low Kick 1; Leer 1; Focus Energy 1,7; Karate Chop 10; Foresight 13; Revenge 22; Vital Throw 25; Submission 32; Wake-Up Slap 36; Scary Face 44; DynamicPunch 51.
- Moved against today's: Seismic Toss 19 to 19,32; Cross Chop 40 to 51.
- Against Kaizo's: the same.

**Tentacool (72)**, 13 moves:

- New list: Poison Sting 1, Acid 5, Psybeam 8, BubbleBeam 12, Signal Beam 15, Poison Jab 19, Confuse Ray 22, Water Pulse 26, Wrap 29, Sludge Bomb 33, Ice Beam 36, Hydro Pump 40, Toxic 43.
- Added against today's: Psybeam 8; Signal Beam 15; Confuse Ray 22; Sludge Bomb 33; Ice Beam 36; Toxic 43.
- Removed against today's: Supersonic 5; Constrict 8; Toxic Spikes 15; Barrier 26; Screech 36; Wring Out 43.
- Moved against today's: Acid 12 to 5; BubbleBeam 19 to 12; Poison Jab 33 to 19; Water Pulse 29 to 26; Wrap 22 to 29.
- Against Kaizo's: the same.

**Tentacruel (73)**, 14 moves:

- New list: Power Gem 1, Aurora Beam 1, Psybeam 1, Acid 5, Water Pulse 8, Signal Beam 15, Poison Jab 19, BubbleBeam 22, Confuse Ray 26, Wrap 29, Sludge Bomb 36, Brine 42, Toxic 49, Hydro Pump 72.
- Added against today's: Power Gem 1; Aurora Beam 1; Psybeam 1; Signal Beam 15; Confuse Ray 26; Sludge Bomb 36; Brine 42; Toxic 49.
- Removed against today's: Poison Sting 1; Supersonic 1,5; Constrict 1,8; Toxic Spikes 15; Barrier 26; Screech 42; Wring Out 55.
- Moved against today's: Acid 12 to 5; Water Pulse 29 to 8; Poison Jab 36 to 19; BubbleBeam 19 to 22; Wrap 22 to 29; Hydro Pump 49 to 72.
- Against Kaizo's: Kaizo's Absorb 12 left out: Oxide has no move like it.

**Geodude (74)**, 15 moves:

- New list: Tackle 1, Rock Throw 1, Mud Bomb 4, Headbutt 8, Karate Chop 11, Selfdestruct 15, Dig 18, Rock Slide 22, Fire Punch 25, Explosion 29, Hammer Arm 32, Selfdestruct 36, Earthquake 39, Stone Edge 46, Explosion 52.
- Added against today's: Mud Bomb 4; Headbutt 8; Karate Chop 11; Dig 18; Rock Slide 22; Fire Punch 25; Hammer Arm 32.
- Removed against today's: Defense Curl 1; Mud Sport 4; Rock Polish 8; Magnitude 15; Rollout 22; Rock Blast 25; Double-Edge 36.
- Moved against today's: Rock Throw 11 to 1; Selfdestruct 18 to 15,36; Explosion 32 to 29,52; Earthquake 29 to 39; Stone Edge 39 to 46.
- Against Kaizo's: the same.

**Graveler (75)**, 15 moves:

- New list: Submission 1, Take Down 1, ThunderPunch 1, Hammer Arm 1, Dig 4, Body Slam 8, Rock Slide 11, Selfdestruct 15, Double-Edge 18, Gyro Ball 22, Rock Blast 27, Explosion 33, Selfdestruct 38, Earthquake 44, Rollout 99.
- Added against today's: Submission 1; Take Down 1; ThunderPunch 1; Hammer Arm 1; Dig 4; Body Slam 8; Rock Slide 11; Gyro Ball 22.
- Removed against today's: Tackle 1; Defense Curl 1; Mud Sport 1,4; Rock Polish 1,8; Rock Throw 11; Magnitude 15; Stone Edge 49.
- Moved against today's: Selfdestruct 18 to 15,38; Double-Edge 44 to 18; Explosion 38 to 33; Earthquake 33 to 44; Rollout 22 to 99.
- Against Kaizo's: the same.

**Golem (76)**, 15 moves:

- New list: Rock Blast 1, ThunderPunch 1, Submission 1, Roar 1, Fire Punch 4, Body Slam 8, Rock Slide 11, Selfdestruct 15, Gyro Ball 18, Rollout 22, Double-Edge 27, Explosion 33, Selfdestruct 38, Earthquake 44, Head Smash 100.
- Added against today's: ThunderPunch 1; Submission 1; Roar 1; Fire Punch 4; Body Slam 8; Rock Slide 11; Gyro Ball 18; Head Smash 100.
- Removed against today's: Tackle 1; Defense Curl 1; Mud Sport 1,4; Rock Polish 1,8; Rock Throw 11; Magnitude 15; Stone Edge 49.
- Moved against today's: Rock Blast 27 to 1; Selfdestruct 18 to 15,38; Double-Edge 44 to 27; Explosion 38 to 33; Earthquake 33 to 44.
- Against Kaizo's: the same.

**Ponyta (77)**, 12 moves:

- New list: Ember 1, Quick Attack 1, High Horsepower 6, Flame Wheel 10, Double Kick 15, Take Down 19, Bounce 24, Blaze Kick 28, Drill Run 33, Double-Edge 37, Hi Jump Kick 42, Flare Blitz 46.
- Added against today's: Quick Attack 1; High Horsepower 6; Double Kick 15; Blaze Kick 28; Drill Run 33; Double-Edge 37; Hi Jump Kick 42.
- Removed against today's: Growl 1; Tackle 1; Tail Whip 6; Stomp 19; Fire Spin 24; Agility 33; Fire Blast 37.
- Moved against today's: Ember 10 to 1; Flame Wheel 15 to 10; Take Down 28 to 19; Bounce 42 to 24.
- Against Kaizo's: Kaizo's Stomp 6 became High Horsepower.

**Rapidash (78)**, 17 moves:

- New list: Poison Jab 1, Heat Wave 1, Fire Spin 1, Quick Attack 1, Double Kick 1, Ember 1, High Horsepower 6, Body Slam 10, Flame Wheel 15, Take Down 19, Bounce 24, Drill Run 28, Blaze Kick 33, Double-Edge 37, Megahorn 40, Jump Kick 47, Flare Blitz 56.
- Added against today's: Heat Wave 1; Double Kick 1; High Horsepower 6; Body Slam 10; Drill Run 28; Blaze Kick 33; Double-Edge 37; Jump Kick 47.
- Removed against today's: Growl 1; Tail Whip 1,6; Stomp 19; Agility 33; Fire Blast 37; Fury Attack 40.
- Moved against today's: Fire Spin 24 to 1; Ember 1,10 to 1; Take Down 28 to 19; Bounce 47 to 24; Megahorn 1 to 40.
- Against Kaizo's: Kaizo's Stomp 6 became High Horsepower.

**Slowpoke (79)**, 14 moves:

- New list: Headbutt 1, Tackle 1, Water Gun 1, Confusion 11, Water Pulse 15, Disable 20, Body Slam 25, Zen Headbutt 29, Dive 34, Yawn 39, Psychic 48, Hydro Pump 53, Slack Off 57, Poison Jab 60.
- Added against today's: Body Slam 25; Dive 34; Hydro Pump 53; Poison Jab 60.
- Removed against today's: Curse 1; Growl 6; Amnesia 43; Rain Dance 53; Psych Up 57.
- Moved against today's: Headbutt 25 to 1; Water Gun 11 to 1; Confusion 15 to 11; Water Pulse 29 to 15; Zen Headbutt 34 to 29; Yawn 1 to 39; Slack Off 39 to 57.
- Against Kaizo's: Kaizo's Swallow 60 became Poison Jab.

**Slowbro (80)**, 15 moves:

- New list: Tackle 1, Swift 1, Water Gun 1, Signal Beam 1, Ice Punch 6, Headbutt 11, Confusion 15, Water Pulse 20, Body Slam 29, Zen Headbutt 34, Brine 37, Yawn 41, Psychic 54, Hydro Pump 61, Slack Off 97.
- Added against today's: Swift 1; Signal Beam 1; Ice Punch 6; Body Slam 29; Brine 37; Hydro Pump 61.
- Removed against today's: Curse 1; Growl 1,6; Disable 20; Withdraw 37; Amnesia 47; Rain Dance 61; Psych Up 67.
- Moved against today's: Water Gun 11 to 1; Headbutt 25 to 11; Water Pulse 29 to 20; Yawn 1 to 41; Slack Off 41 to 97.
- Rule: Teleport 25 out: Splash and Teleport go.
- Rule: Teleport 47 out: Splash and Teleport go.

**Magnemite (81)**, 14 moves:

- New list: Tackle 1, Supersonic 1, ThunderShock 6, SonicBoom 14, Shock Wave 23, Flash Cannon 25, Selfdestruct 27, Tri Attack 30, Magnet Bomb 33, Discharge 38, Explosion 43, Signal Beam 46, Mirror Shot 55, Zap Cannon 64.
- Added against today's: Shock Wave 23; Flash Cannon 25; Selfdestruct 27; Tri Attack 30; Explosion 43; Signal Beam 46.
- Removed against today's: Metal Sound 1; Thunder Wave 17; Spark 22; Lock-On 27; Screech 33; Magnet Rise 46; Gyro Ball 49.
- Moved against today's: Supersonic 11 to 1; Magnet Bomb 30 to 33; Mirror Shot 43 to 55; Zap Cannon 54 to 64.
- Against Kaizo's: the same.

**Magneton (82)**, 16 moves:

- New list: Iron Head 1, Wild Charge 1, Tackle 1, Gyro Ball 1, Supersonic 1, ThunderShock 6, Tri Attack 11, Thunder Wave 17, Shock Wave 22, Signal Beam 27, Selfdestruct 30, Magnet Bomb 34, Discharge 40, Explosion 46, Flash Cannon 54, Thunderbolt 60.
- Added against today's: Iron Head 1; Wild Charge 1; Shock Wave 22; Signal Beam 27; Selfdestruct 30; Explosion 46; Flash Cannon 54; Thunderbolt 60.
- Removed against today's: Metal Sound 1; SonicBoom 14; Spark 22; Lock-On 27; Screech 34; Mirror Shot 46; Magnet Rise 50; Zap Cannon 60.
- Moved against today's: Gyro Ball 54 to 1; Supersonic 1,11 to 1; ThunderShock 1,6 to 6; Tri Attack 1 to 11; Magnet Bomb 30 to 34.
- Rule: Teleport 50 out: Splash and Teleport go.

**Seel (86)**, 16 moves:

- New list: Water Gun 1, Powder Snow 3, Aurora Beam 7, BubbleBeam 11, Bite 13, Take Down 17, Aurora Beam 21, Water Pulse 23, Body Slam 27, Drill Run 31, Ice Fang 37, Aqua Tail 41, Megahorn 43, Hydro Pump 47, Ice Beam 48, Aqua Jet 71.
- Added against today's: Water Gun 1; Powder Snow 3; BubbleBeam 11; Bite 13; Water Pulse 23; Body Slam 27; Drill Run 31; Ice Fang 37; Megahorn 43; Hydro Pump 47.
- Removed against today's: Headbutt 1; Growl 3; Water Sport 7; Icy Wind 11; Encore 13; Ice Shard 17; Rest 21; Aqua Ring 23; Brine 33; Dive 41; Safeguard 51.
- Moved against today's: Aurora Beam 27 to 7,21; Take Down 37 to 17; Aqua Tail 43 to 41; Ice Beam 47 to 48; Aqua Jet 31 to 71.
- Against Kaizo's: the same.

**Dewgong (87)**, 20 moves:

- New list: Headbutt 1, Supersonic 1, Double-Edge 1, Whirlpool 1, Swift 3, Signal Beam 7, Powder Snow 11, BubbleBeam 13, Dive 17, Take Down 21, Water Pulse 23, Aurora Beam 27, Body Slam 31, Drill Run 33, Ice Fang 41, Roar 48, Double-Edge 53, Hydro Pump 58, Ice Beam 62, Megahorn 65.
- Added against today's: Supersonic 1; Double-Edge 1,53; Whirlpool 1; Swift 3; Powder Snow 11; BubbleBeam 13; Water Pulse 23; Body Slam 31; Drill Run 33; Ice Fang 41; Roar 48; Hydro Pump 58; Megahorn 65.
- Removed against today's: Growl 1,3; Icy Wind 1,11; Encore 13; Ice Shard 17; Rest 21; Aqua Ring 23; Aqua Jet 31; Brine 33; Sheer Cold 34; Aqua Tail 43; Safeguard 51.
- Moved against today's: Signal Beam 1,7 to 7; Dive 41 to 17; Take Down 37 to 21; Ice Beam 47 to 62.
- Against Kaizo's: the same.

**Shellder (90)**, 11 moves:

- New list: Take Down 1, Supersonic 8, Water Pulse 13, Powder Snow 16, Selfdestruct 25, Liquidation 28, Poison Fang 32, Explosion 37, Hydro Pump 40, Icicle Spear 49, Clamp 75.
- Added against today's: Take Down 1; Water Pulse 13; Powder Snow 16; Selfdestruct 25; Liquidation 28; Poison Fang 32; Explosion 37; Hydro Pump 40.
- Removed against today's: Tackle 1; Withdraw 4; Protect 16; Leer 20; Ice Shard 28; Aurora Beam 32; Whirlpool 37; Iron Defense 40; Brine 44; Ice Beam 49.
- Moved against today's: Icicle Spear 13 to 49; Clamp 25 to 75.
- Against Kaizo's: Kaizo's ViceGrip 28 became Liquidation.
- Rule: Teleport 1 out: Splash and Teleport go.
- Rule: Teleport 17 out: Splash and Teleport go.
- Rule: Teleport 44 out: Splash and Teleport go.
- Rule: Take Down moved from 4 to 1: Teleport or Splash was the only level-1 move (a pick for the balance track to confirm).

**Cloyster (91)**, 8 moves:

- New list: Toxic 1, Rock Blast 1, Supersonic 1, Selfdestruct 2, Explosion 3, Liquidation 28, Icicle Spear 69, Aqua Cutter 72.
- Added against today's: Toxic 1; Rock Blast 1; Selfdestruct 2; Explosion 3; Liquidation 28; Icicle Spear 69; Aqua Cutter 72.
- Removed against today's: Toxic Spikes 1; Withdraw 1; Aurora Beam 1; Protect 1; Spikes 28; Spike Cannon 40.
- Against Kaizo's: Kaizo's ViceGrip 28 became Liquidation.

**Gastly (92)**, 11 moves:

- New list: Confuse Ray 1, Shadow Claw 5, Smog 8, Dark Pulse 19, Night Shade 35, Sludge 42, Ominous Wind 49, Poison Gas 52, Sludge Bomb 56, Shadow Ball 60, Hypnosis 63.
- Added against today's: Shadow Claw 5; Smog 8; Sludge 42; Ominous Wind 49; Poison Gas 52; Sludge Bomb 56.
- Removed against today's: Lick 1; Spite 5; Mean Look 8; Curse 12; Sucker Punch 22; Payback 26; Dream Eater 33; Destiny Bond 40; Nightmare 43.
- Moved against today's: Confuse Ray 19 to 1; Dark Pulse 36 to 19; Night Shade 15 to 35; Shadow Ball 29 to 60; Hypnosis 1 to 63.
- Against Kaizo's: Kaizo's Lick 5 became Shadow Claw.
- Rule: Teleport 1 out: Splash and Teleport go.
- Rule: Teleport 39 out: Splash and Teleport go.
- Rule: Teleport 53 out: Splash and Teleport go.

**Haunter (93)**, 13 moves:

- New list: Night Shade 1, Confuse Ray 1, Shadow Claw 1, Sludge 8, Ice Punch 32, Shadow Punch 42, Poison Jab 44, Fire Punch 45, Shadow Claw 49, Toxic 52, Sludge Bomb 54, Shadow Ball 60, Hypnosis 65.
- Added against today's: Shadow Claw 1,49; Sludge 8; Ice Punch 32; Poison Jab 44; Fire Punch 45; Toxic 52; Sludge Bomb 54.
- Removed against today's: Lick 1; Spite 1,5; Mean Look 8; Curse 12; Sucker Punch 22; Payback 28; Dream Eater 39; Dark Pulse 44; Destiny Bond 50; Nightmare 55.
- Moved against today's: Night Shade 15 to 1; Confuse Ray 19 to 1; Shadow Punch 25 to 42; Shadow Ball 33 to 60; Hypnosis 1 to 65.
- Against Kaizo's: Kaizo's Lick 1 became Shadow Claw.
- Rule: Teleport 5 out: Splash and Teleport go.
- Rule: Teleport 43 out: Splash and Teleport go.
- Rule: Teleport 53 out: Splash and Teleport go.

**Gengar (94)**, 14 moves:

- New list: Confuse Ray 1, Shadow Claw 1, Sludge 5, Ice Punch 8, Mimic 12, Night Shade 15, Poison Jab 22, Fire Punch 39, Shadow Punch 42, Dark Pulse 52, Sludge Bomb 53, Submission 54, Shadow Claw 70, Explosion 75.
- Added against today's: Shadow Claw 1,70; Sludge 5; Ice Punch 8; Mimic 12; Poison Jab 22; Fire Punch 39; Sludge Bomb 53; Submission 54; Explosion 75.
- Removed against today's: Hypnosis 1; Lick 1; Spite 1,5; Mean Look 8; Curse 12; Sucker Punch 22; Payback 28; Shadow Ball 33; Dream Eater 39; Destiny Bond 50; Nightmare 55.
- Moved against today's: Confuse Ray 19 to 1; Shadow Punch 25 to 42; Dark Pulse 44 to 52.
- Against Kaizo's: Kaizo's Lick 1 became Shadow Claw.
- Rule: Teleport 1 out: Splash and Teleport go.
- Rule: Teleport 19 out: Splash and Teleport go.

**Onix (95)**, 17 moves:

- New list: Roar 1, Tackle 1, Rock Throw 1, Wrap 1, Dig 6, Roar 9, Secret Power 14, Bite 17, Rock Slide 22, Take Down 25, Selfdestruct 30, Power Gem 33, Double-Edge 38, Explosion 41, Roar 46, Earthquake 49, Stone Edge 54.
- Added against today's: Roar 1,9,46; Wrap 1; Dig 6; Secret Power 14; Bite 17; Rock Slide 22; Take Down 25; Selfdestruct 30; Power Gem 33; Explosion 41; Earthquake 49.
- Removed against today's: Mud Sport 1; Harden 1; Bind 1; Screech 6; Rage 14; Rock Tomb 17; Sandstorm 22; Slam 25; Rock Polish 30; DragonBreath 33; Curse 38; Iron Tail 41; Sand Tomb 46.
- Moved against today's: Rock Throw 9 to 1; Double-Edge 49 to 38.
- Against Kaizo's: the same.

**Krabby (98)**, 15 moves:

- New list: Scratch 1, Mud Shot 1, Metal Claw 5, BubbleBeam 9, Slash 11, Dig 15, Ice Punch 19, Dive 21, Rock Slide 25, Hammer Arm 29, Liquidation 31, Night Slash 35, Superpower 39, X-Scissor 41, Crabhammer 45.
- Added against today's: Scratch 1; Slash 11; Dig 15; Ice Punch 19; Dive 21; Rock Slide 25; Hammer Arm 29; Liquidation 31; Night Slash 35; Superpower 39; X-Scissor 41.
- Removed against today's: Mud Sport 1; Bubble 1; ViceGrip 5; Leer 9; Harden 11; Stomp 25; Protect 29; Guillotine 31; Slam 35; Brine 39; Flail 45.
- Moved against today's: Mud Shot 19 to 1; Metal Claw 21 to 5; BubbleBeam 15 to 9; Crabhammer 41 to 45.
- Against Kaizo's: Kaizo's ViceGrip 31 became Liquidation.

**Kingler (99)**, 16 moves:

- New list: False Swipe 1, Fling 1, Ice Punch 1, X-Scissor 5, Crush Claw 9, Body Slam 11, Metal Claw 15, Dive 19, Hammer Arm 21, Rock Slide 25, Slam 32, Liquidation 37, Night Slash 44, Superpower 51, Crush Claw 56, Crabhammer 63.
- Added against today's: False Swipe 1; Fling 1; Ice Punch 1; X-Scissor 5; Crush Claw 9,56; Body Slam 11; Dive 19; Hammer Arm 21; Rock Slide 25; Liquidation 37; Night Slash 44; Superpower 51.
- Removed against today's: Mud Sport 1; Bubble 1; ViceGrip 1,5; Leer 9; Harden 11; BubbleBeam 15; Mud Shot 19; Stomp 25; Protect 32; Guillotine 37; Brine 51; Flail 63.
- Moved against today's: Metal Claw 21 to 15; Slam 44 to 32; Crabhammer 56 to 63.
- Against Kaizo's: Kaizo's ViceGrip 37 became Liquidation.

**Lickitung (108)**, 14 moves:

- New list: Shadow Claw 1, Supersonic 5, High Horsepower 9, Acid 13, Wrap 17, Water Pulse 21, Disable 25, Body Slam 29, Double-Edge 33, Me First 37, Slam 41, Gastro Acid 45, Power Whip 49, Wring Out 53.
- Added against today's: Shadow Claw 1; High Horsepower 9; Acid 13; Water Pulse 21; Body Slam 29; Double-Edge 33; Gastro Acid 45.
- Removed against today's: Lick 1; Defense Curl 9; Knock Off 13; Stomp 21; Rollout 33; Refresh 41; Screech 45.
- Moved against today's: Slam 29 to 41.
- Against Kaizo's: Kaizo's Lick 1 became Shadow Claw.
- Against Kaizo's: Kaizo's Stomp 9 became High Horsepower.

**Koffing (109)**, 13 moves:

- New list: Smog 1, Toxic 1, Psybeam 6, SmokeScreen 10, Sludge 15, Selfdestruct 19, Assurance 24, Sludge Bomb 28, Gyro Ball 33, Explosion 37, Poison Gas 42, Poison Fang 46, Haze 51.
- Added against today's: Toxic 1; Psybeam 6; Poison Fang 46.
- Removed against today's: Tackle 1; Destiny Bond 46; Memento 51.
- Moved against today's: Smog 6 to 1; Sludge 24 to 15; Assurance 15 to 24; Sludge Bomb 42 to 28; Poison Gas 1 to 42; Haze 28 to 51.
- Against Kaizo's: the same.

**Weezing (110)**, 15 moves:

- New list: Heat Wave 1, Gyro Ball 1, Smog 1, Headbutt 1, Toxic 6, SmokeScreen 10, Sludge 15, Selfdestruct 19, Assurance 24, Sludge Bomb 28, Double Hit 33, Explosion 40, Poison Gas 48, Poison Fang 55, Shadow Ball 63.
- Added against today's: Heat Wave 1; Gyro Ball 1; Headbutt 1; Toxic 6; Poison Fang 55; Shadow Ball 63.
- Removed against today's: Tackle 1; Haze 28; Destiny Bond 55; Memento 63.
- Moved against today's: Smog 1,6 to 1; SmokeScreen 1,10 to 10; Sludge 24 to 15; Assurance 15 to 24; Sludge Bomb 48 to 28; Poison Gas 1 to 48.
- Against Kaizo's: the same.

**Rhyhorn (111)**, 12 moves:

- New list: Tackle 1, Rock Throw 1, Dig 9, Bite 13, Peck 21, High Horsepower 25, Rock Slide 33, Drill Run 37, Crunch 49, Megahorn 57, Earthquake 65, Stone Edge 72.
- Added against today's: Tackle 1; Rock Throw 1; Dig 9; Bite 13; Peck 21; High Horsepower 25; Rock Slide 33; Drill Run 37; Crunch 49.
- Removed against today's: Horn Attack 1; Tail Whip 1; Stomp 9; Fury Attack 13; Scary Face 21; Rock Blast 25; Take Down 33; Horn Drill 37.
- Moved against today's: Earthquake 49 to 65; Stone Edge 45 to 72.
- Against Kaizo's: Kaizo's Stomp 25 became High Horsepower.

**Rhydon (112)**, 14 moves:

- New list: Aqua Tail 1, Submission 1, Fire Punch 1, Rock Slide 1, Crunch 9, Headbutt 13, High Horsepower 21, Poison Jab 25, Rock Blast 33, Hammer Arm 37, Drill Run 42, Megahorn 67, Earthquake 75, Stone Edge 87.
- Added against today's: Aqua Tail 1; Submission 1; Fire Punch 1; Rock Slide 1; Crunch 9; Headbutt 13; High Horsepower 21; Poison Jab 25; Drill Run 42.
- Removed against today's: Horn Attack 1; Tail Whip 1; Stomp 1,9; Fury Attack 1,13; Scary Face 21; Take Down 33; Horn Drill 37.
- Moved against today's: Rock Blast 25 to 33; Hammer Arm 42 to 37; Megahorn 57 to 67; Earthquake 49 to 75; Stone Edge 45 to 87.
- Against Kaizo's: Kaizo's Stomp 21 became High Horsepower.

**Chansey (113)**, 11 moves:

- New list: Pound 1, Take Down 5, Double-Edge 9, Headbutt 12, Metronome 16, DoubleSlap 23, Fling 27, Submission 31, Double-Edge 34, Take Down 42, Seed Bomb 46.
- Added against today's: Take Down 5,42; Headbutt 12; Metronome 16; Submission 31; Seed Bomb 46.
- Removed against today's: Growl 1; Tail Whip 5; Refresh 9; Softboiled 12; Minimize 20; Sing 23; Defense Curl 31; Light Screen 34; Egg Bomb 38; Healing Wish 42.
- Moved against today's: Double-Edge 46 to 9,34; DoubleSlap 16 to 23.
- Against Kaizo's: Kaizo's Egg Bomb 46 became Seed Bomb.
- Rule: Teleport 1 out: Splash and Teleport go.
- Rule: Teleport 20 out: Splash and Teleport go.
- Rule: Teleport 38 out: Splash and Teleport go.

**Tangela (114)**, 16 moves:

- New list: Vine Whip 1, Poison Jab 1, Confusion 5, Stun Spore 12, Slam 15, Mega Drain 19, Wrap 22, Sludge Bomb 26, Stun Spore 29, Power Whip 33, AncientPower 36, Sleep Powder 40, Endeavor 43, Energy Ball 47, Wring Out 50, Frenzy Plant 74.
- Added against today's: Poison Jab 1; Confusion 5; Wrap 22; Sludge Bomb 26; Endeavor 43; Energy Ball 47; Frenzy Plant 74.
- Removed against today's: Ingrain 1; Constrict 1; Absorb 8; Growth 12; PoisonPowder 15; Bind 22; Knock Off 36; Natural Gift 40; Tickle 47.
- Moved against today's: Vine Whip 19 to 1; Stun Spore 29 to 12,29; Slam 43 to 15; Mega Drain 26 to 19; Power Whip 54 to 33; AncientPower 33 to 36; Sleep Powder 5 to 40.
- Against Kaizo's: Kaizo's Swallow 1 became Poison Jab.
- Against Kaizo's: Kaizo's Absorb 8 left out: Oxide has no move like it.

**Horsea (116)**, 12 moves:

- New list: Bubble 1, SmokeScreen 4, Water Gun 8, Twister 11, Take Down 14, Aurora Beam 18, BubbleBeam 23, DragonBreath 26, Double-Edge 30, Ice Beam 35, Octazooka 38, Dragon Pulse 42.
- Added against today's: Take Down 14; Aurora Beam 18; DragonBreath 26; Double-Edge 30; Ice Beam 35; Octazooka 38.
- Removed against today's: Leer 8; Focus Energy 14; Agility 23; Brine 30; Hydro Pump 35; Dragon Dance 38.
- Moved against today's: Water Gun 11 to 8; Twister 26 to 11; BubbleBeam 18 to 23.
- Against Kaizo's: the same.

**Seadra (117)**, 15 moves:

- New list: Water Pulse 1, Supersonic 1, Swift 1, Dragon Rage 1, SmokeScreen 4, Water Gun 8, Twister 11, Take Down 14, Aurora Beam 18, BubbleBeam 23, DragonBreath 26, Double-Edge 30, Ice Beam 40, Octazooka 48, Dragon Pulse 57.
- Added against today's: Water Pulse 1; Supersonic 1; Swift 1; Dragon Rage 1; Take Down 14; Aurora Beam 18; DragonBreath 26; Double-Edge 30; Ice Beam 40; Octazooka 48.
- Removed against today's: Bubble 1; Leer 1,8; Focus Energy 14; Agility 23; Brine 30; Hydro Pump 40; Dragon Dance 48.
- Moved against today's: SmokeScreen 1,4 to 4; Water Gun 1,11 to 8; Twister 26 to 11; BubbleBeam 18 to 23.
- Against Kaizo's: the same.

**Goldeen (118)**, 13 moves:

- New list: Tackle 1, Peck 1, Aqua Jet 1, Mud Shot 7, Psybeam 11, Dive 17, Flail 21, Aqua Ring 27, Fury Attack 31, Drill Peck 37, Poison Jab 41, Body Slam 47, Megahorn 51.
- Added against today's: Tackle 1; Aqua Jet 1; Mud Shot 7; Psybeam 11; Dive 17; Drill Peck 37; Poison Jab 41; Body Slam 47.
- Removed against today's: Tail Whip 1; Water Sport 1; Supersonic 7; Horn Attack 11; Water Pulse 17; Waterfall 37; Horn Drill 41; Agility 47.
- Against Kaizo's: the same.

**Seaking (119)**, 15 moves:

- New list: Tackle 1, Peck 1, Aqua Jet 1, Ice Beam 1, Supersonic 1, Aerial Ace 7, Psybeam 11, Aqua Tail 17, Flail 21, Aqua Ring 27, Fury Attack 31, Knock Off 40, Poison Jab 47, Body Slam 56, Megahorn 63.
- Added against today's: Tackle 1; Aqua Jet 1; Ice Beam 1; Aerial Ace 7; Psybeam 11; Aqua Tail 17; Knock Off 40; Body Slam 56.
- Removed against today's: Tail Whip 1; Water Sport 1; Horn Attack 11; Water Pulse 17; Waterfall 40; Horn Drill 47; Agility 56.
- Moved against today's: Supersonic 1,7 to 1; Poison Jab 1 to 47.
- Against Kaizo's: the same.

**Staryu (120)**, 11 moves:

- New list: Tackle 1, Water Gun 6, Swift 10, BubbleBeam 15, Take Down 24, Psybeam 28, Power Gem 33, Signal Beam 37, Double-Edge 46, Recover 51, Hydro Pump 55.
- Added against today's: Take Down 24; Psybeam 28; Signal Beam 37; Double-Edge 46.
- Removed against today's: Harden 1; Rapid Spin 10; Camouflage 19; Minimize 33; Gyro Ball 37; Light Screen 42; Cosmic Power 51.
- Moved against today's: Swift 24 to 10; BubbleBeam 28 to 15; Power Gem 46 to 33; Recover 15 to 51.
- Rule: Teleport 1 out: Splash and Teleport go.
- Rule: Teleport 19 out: Splash and Teleport go.
- Rule: Teleport 42 out: Splash and Teleport go.

**Starmie (121)**, 5 moves:

- New list: Double-Edge 1, Recover 1, Power Gem 1, Hydro Pump 55, Mega Kick 65.
- Added against today's: Double-Edge 1; Power Gem 1; Hydro Pump 55; Mega Kick 65.
- Removed against today's: Water Gun 1; Rapid Spin 1; Swift 1; Confuse Ray 28.
- Rule: Teleport 2 out: Splash and Teleport go.

**Mr Mime (122)**, 16 moves:

- New list: Thunderbolt 1, Power Swap 1, Guard Swap 1, Seismic Toss 1, Copycat 4, Barrier 8, Confusion 11, Zen Headbutt 18, Magical Leaf 22, Reflect 22, Light Screen 25, Psybeam 32, Safeguard 36, Role Play 43, Signal Beam 46, Psychic 50.
- Added against today's: Thunderbolt 1; Seismic Toss 1; Zen Headbutt 18; Signal Beam 46.
- Removed against today's: Meditate 8; Encore 11; DoubleSlap 15; Mimic 18; Substitute 29; Recycle 32; Trick 36; Baton Pass 46.
- Moved against today's: Barrier 1 to 8; Confusion 1 to 11; Magical Leaf 1 to 22; Light Screen 22 to 25; Psybeam 25 to 32; Safeguard 50 to 36; Psychic 39 to 50.
- Rule: Teleport 1 out: Splash and Teleport go.
- Rule: Teleport 15 out: Splash and Teleport go.
- Rule: Teleport 29 out: Splash and Teleport go.
- Rule: Teleport 39 out: Splash and Teleport go.

**Scyther (123)**, 18 moves:

- New list: False Swipe 1, Slash 1, Air Slash 1, Silver Wind 5, Take Down 9, Wing Attack 13, Bug Buzz 17, Brick Break 21, Double-Edge 25, Feint 29, Vacuum Wave 33, Wing Attack 37, Night Slash 41, Steel Wing 45, Pursuit 49, Aerial Ace 53, X-Scissor 57, Close Combat 77.
- Added against today's: Silver Wind 5; Take Down 9; Bug Buzz 17; Brick Break 21; Double-Edge 25; Steel Wing 45; Aerial Ace 53; Close Combat 77.
- Removed against today's: Quick Attack 1; Leer 1; Focus Energy 5; Agility 17; Fury Cutter 25; Razor Wind 33; Double Team 37; Double Hit 49; Swords Dance 57.
- Moved against today's: False Swipe 13 to 1; Slash 29 to 1; Air Slash 53 to 1; Wing Attack 21 to 13,37; Feint 61 to 29; Vacuum Wave 1 to 33; Night Slash 45 to 41; Pursuit 9 to 49; X-Scissor 41 to 57.
- Against Kaizo's: the same.

**Jynx (124)**, 17 moves:

- New list: Pound 1, Sweet Kiss 1, DoubleSlap 1, Ice Punch 1, Zen Headbutt 5, Shadow Claw 8, Powder Snow 11, Confusion 15, Teeter Dance 18, Psybeam 21, Aurora Beam 25, Wake-Up Slap 28, Sing 33, Psychic 44, Ice Beam 49, Focus Blast 51, Lovely Kiss 55.
- Added against today's: Sweet Kiss 1; Zen Headbutt 5; Shadow Claw 8; Confusion 15; Teeter Dance 18; Psybeam 21; Aurora Beam 25; Sing 33; Psychic 44; Ice Beam 49; Focus Blast 51.
- Removed against today's: Lick 1,5; Mean Look 21; Fake Tears 25; Avalanche 33; Body Slam 39; Wring Out 44; Perish Song 49; Blizzard 55.
- Moved against today's: DoubleSlap 15 to 1; Ice Punch 18 to 1; Powder Snow 1,11 to 11; Lovely Kiss 1,8 to 55.
- Against Kaizo's: Kaizo's Lick 8 became Shadow Claw.

**Electabuzz (125)**, 13 moves:

- New list: ThunderShock 1, Mega Punch 1, Wild Charge 1, Karate Chop 7, Swift 10, Shock Wave 16, Low Kick 19, Seismic Toss 25, Fire Punch 28, ThunderPunch 37, Cross Chop 43, Ice Punch 52, Thunderbolt 58.
- Added against today's: Mega Punch 1; Wild Charge 1; Karate Chop 7; Seismic Toss 25; Fire Punch 28; Cross Chop 43; Ice Punch 52.
- Removed against today's: Quick Attack 1; Leer 1; Light Screen 25; Discharge 37; Screech 52; Thunder 58.
- Moved against today's: ThunderShock 1,7 to 1; Swift 16 to 10; Shock Wave 19 to 16; Low Kick 10 to 19; ThunderPunch 28 to 37; Thunderbolt 43 to 58.
- Against Kaizo's: the same.

**Magmar (126)**, 14 moves:

- New list: Fire Spin 1, Brick Break 1, Flare Blitz 1, Mega Punch 7, Fire Punch 10, SmokeScreen 16, Faint Attack 19, Confuse Ray 25, ThunderPunch 28, Fire Punch 36, Psychic 41, Cross Chop 49, Heat Wave 54, Milk Drink 80.
- Added against today's: Brick Break 1; Flare Blitz 1; Mega Punch 7; ThunderPunch 28; Psychic 41; Cross Chop 49; Heat Wave 54; Milk Drink 80.
- Removed against today's: Smog 1; Leer 1; Ember 1,7; Lava Plume 36; Flamethrower 41; Sunny Day 49; Fire Blast 54.
- Moved against today's: Fire Spin 19 to 1; Fire Punch 28 to 10,36; SmokeScreen 10 to 16; Faint Attack 16 to 19.
- Against Kaizo's: the same.

**Lapras (131)**, 15 moves:

- New list: Roar 1, Whirlpool 1, Body Slam 1, Take Down 4, Powder Snow 7, Water Pulse 10, Roar 14, Confuse Ray 18, Aurora Beam 22, Aqua Tail 27, Double-Edge 32, Drill Run 37, Ice Beam 43, Hydro Pump 49, Sing 55.
- Added against today's: Roar 1,14; Whirlpool 1; Take Down 4; Powder Snow 7; Aurora Beam 22; Aqua Tail 27; Double-Edge 32; Drill Run 37.
- Removed against today's: Growl 1; Water Gun 1; Mist 4; Ice Shard 10; Rain Dance 22; Perish Song 27; Brine 37; Safeguard 43; Sheer Cold 55.
- Moved against today's: Body Slam 18 to 1; Water Pulse 14 to 10; Confuse Ray 7 to 18; Ice Beam 32 to 43; Sing 1 to 55.
- Against Kaizo's: the same.

**Eevee (133)**, 11 moves:

- New list: Secret Power 1, Tackle 1, Headbutt 1, Mud-Slap 8, Take Down 15, Double Kick 22, Bite 29, Body Slam 36, Iron Tail 43, Double-Edge 50, Trump Card 57.
- Added against today's: Secret Power 1; Headbutt 1; Mud-Slap 8; Double Kick 22; Body Slam 36; Iron Tail 43; Double-Edge 50.
- Removed against today's: Tail Whip 1; Helping Hand 1; Sand-Attack 8; Growl 15; Quick Attack 22; Baton Pass 36; Last Resort 50.
- Moved against today's: Take Down 43 to 15.
- Against Kaizo's: the same.

**Vaporeon (134)**, 14 moves:

- New list: Acid Armor 1, Water Pulse 1, Take Down 1, Roar 8, Ice Fang 15, Water Pulse 21, Bite 29, Body Slam 36, Ice Fang 43, Aqua Tail 50, Roar 57, Camouflage 64, Ice Beam 71, Hydro Pump 73.
- Added against today's: Water Pulse 1,21; Take Down 1; Roar 8,57; Ice Fang 15,43; Body Slam 36; Aqua Tail 50; Camouflage 64; Ice Beam 71.
- Removed against today's: Tail Whip 1; Tackle 1; Helping Hand 1; Sand-Attack 8; Water Gun 15; Quick Attack 22; Aurora Beam 36; Aqua Ring 43; Last Resort 50; Haze 57; Muddy Water 78.
- Moved against today's: Acid Armor 64 to 1; Hydro Pump 71 to 73.
- Against Kaizo's: the same.

**Jolteon (135)**, 14 moves:

- New list: ThunderShock 1, Tackle 1, Swift 1, Take Down 8, Roar 15, Bite 22, Double Kick 29, Pin Missile 36, Swift 43, Wild Charge 50, Double-Edge 57, Roar 64, Thunder Wave 71, Discharge 95.
- Added against today's: Swift 1,43; Take Down 8; Roar 15,64; Bite 22; Wild Charge 50; Double-Edge 57.
- Removed against today's: Tail Whip 1; Helping Hand 1; Sand-Attack 8; Quick Attack 22; Thunder Fang 43; Last Resort 50; Agility 64; Thunder 71.
- Moved against today's: ThunderShock 15 to 1; Thunder Wave 57 to 71; Discharge 78 to 95.
- Against Kaizo's: the same.

**Flareon (136)**, 14 moves:

- New list: Heat Wave 1, Quick Attack 1, Helping Hand 1, Roar 8, Ember 15, Quick Attack 22, Bite 29, Fire Fang 36, Iron Tail 43, Last Resort 50, Flare Blitz 57, Superpower 64, Crunch 71, Lava Plume 78.
- Added against today's: Heat Wave 1; Roar 8; Iron Tail 43; Flare Blitz 57; Superpower 64; Crunch 71.
- Removed against today's: Tail Whip 1; Tackle 1; Sand-Attack 8; Fire Spin 36; Smog 57; Scary Face 64; Fire Blast 71.
- Moved against today's: Quick Attack 22 to 1,22; Fire Fang 43 to 36.
- Against Kaizo's: the same.

**Snorlax (143)**, 15 moves:

- New list: Yawn 1, Body Slam 4, Take Down 9, Shadow Claw 12, Submission 17, Whirlwind 20, Rest 25, Sleep Talk 28, Pursuit 28, Hyper Beam 33, Selfdestruct 36, Whirlwind 41, Crunch 44, Double-Edge 50, Earthquake 84.
- Added against today's: Take Down 9; Shadow Claw 12; Submission 17; Whirlwind 20,41; Pursuit 28; Hyper Beam 33; Selfdestruct 36; Double-Edge 50; Earthquake 84.
- Removed against today's: Tackle 1; Defense Curl 4; Amnesia 9; Lick 12; Belly Drum 17; Snore 28; Block 36; Rollout 41; Giga Impact 49.
- Moved against today's: Yawn 20 to 1; Body Slam 33 to 4.
- Against Kaizo's: Kaizo's Lick 12 became Shadow Claw.

**Articuno (144)**, 14 moves:

- New list: Pluck 1, Surf 1, Whirlwind 8, Hyper Beam 15, Aurora Beam 22, Air Slash 29, Roar 36, AncientPower 43, Steel Wing 50, Ice Beam 57, Sky Attack 64, Whirlwind 71, Sleep Talk 78, Roost 85.
- Added against today's: Pluck 1; Surf 1; Whirlwind 8,71; Hyper Beam 15; Aurora Beam 22; Air Slash 29; Roar 36; Steel Wing 50; Sky Attack 64; Sleep Talk 78.
- Removed against today's: Gust 1; Powder Snow 1; Mist 8; Ice Shard 15; Mind Reader 22; Agility 36; Reflect 50; Tailwind 64; Blizzard 71; Sheer Cold 78; Hail 85.
- Moved against today's: AncientPower 29 to 43; Ice Beam 43 to 57; Roost 57 to 85.
- Against Kaizo's: Kaizo's Water Ball 1 became Surf.

**Zapdos (145)**, 14 moves:

- New list: Pluck 1, Surf 1, Air Slash 8, Whirlwind 15, Shock Wave 22, Drill Peck 29, AncientPower 36, Roar 43, Hyper Beam 50, Discharge 57, Whirlwind 64, Sky Attack 71, Sleep Talk 78, Roost 85.
- Added against today's: Surf 1; Air Slash 8; Whirlwind 15,64; Shock Wave 22; Roar 43; Hyper Beam 50; Sky Attack 71; Sleep Talk 78.
- Removed against today's: Peck 1; ThunderShock 1; Thunder Wave 8; Detect 15; Charge 36; Agility 43; Light Screen 64; Thunder 78; Rain Dance 85.
- Moved against today's: Pluck 22 to 1; Drill Peck 71 to 29; AncientPower 29 to 36; Discharge 50 to 57; Roost 57 to 85.
- Against Kaizo's: Kaizo's Water Ball 1 became Surf.

**Moltres (146)**, 14 moves:

- New list: Pluck 1, Heat Wave 1, Fire Spin 8, Hyper Beam 15, Surf 22, AncientPower 29, Air Slash 36, Roar 43, SolarBeam 50, Overheat 57, Whirlwind 64, Sky Attack 71, Sleep Talk 78, Roost 85.
- Added against today's: Pluck 1; Hyper Beam 15; Surf 22; Roar 43; Overheat 57; Whirlwind 64; Sleep Talk 78.
- Removed against today's: Wing Attack 1; Ember 1; Agility 15; Endure 22; Flamethrower 36; Safeguard 43; Sunny Day 85.
- Moved against today's: Heat Wave 64 to 1; Air Slash 50 to 36; SolarBeam 71 to 50; Sky Attack 78 to 71; Roost 57 to 85.
- Against Kaizo's: Kaizo's Water Ball 22 became Surf.

**Totodile (158)**, 15 moves:

- New list: Scratch 1, Water Gun 1, Bite 6, Hidden Power 8, Nature Power 13, BubbleBeam 15, Slash 20, Crunch 22, Dive 27, Iron Tail 29, Ice Fang 34, Thrash 36, Aqua Tail 41, Superpower 43, Hydro Pump 48.
- Added against today's: Hidden Power 8; Nature Power 13; BubbleBeam 15; Dive 27; Iron Tail 29.
- Removed against today's: Leer 1; Rage 8; Scary Face 15; Flail 22; Screech 34.
- Moved against today's: Water Gun 6 to 1; Bite 13 to 6; Slash 29 to 20; Crunch 27 to 22; Ice Fang 20 to 34.
- Against Kaizo's: the same.

**Croconaw (159)**, 16 moves:

- New list: Dragon Claw 1, Brick Break 1, Water Gun 1, Hyper Fang 6, Hidden Power 8, BubbleBeam 13, Nature Power 15, Bite 21, Headbutt 24, Hyper Fang 30, Crunch 33, Ice Fang 39, Liquidation 42, Aqua Tail 48, Superpower 51, Super Fang 57.
- Added against today's: Dragon Claw 1; Brick Break 1; Hyper Fang 6,30; Hidden Power 8; BubbleBeam 13; Nature Power 15; Headbutt 24; Liquidation 42; Super Fang 57.
- Removed against today's: Scratch 1; Leer 1; Rage 8; Scary Face 15; Flail 24; Slash 33; Screech 39; Thrash 42; Hydro Pump 57.
- Moved against today's: Water Gun 1,6 to 1; Bite 13 to 21; Crunch 30 to 33; Ice Fang 21 to 39.
- Against Kaizo's: Kaizo's ViceGrip 42 became Liquidation.

**Feraligatr (160)**, 18 moves:

- New list: Fire Fang 1, Dragon Claw 1, Iron Tail 1, Cross Chop 1, Slash 6, Thunder Fang 8, Bite 13, Metal Claw 15, Roar 21, Hyper Fang 24, Body Slam 30, Crunch 32, Ice Fang 42, Liquidation 47, Roar 50, Earthquake 58, Ice Punch 63, Aqua Tail 71.
- Added against today's: Fire Fang 1; Dragon Claw 1; Iron Tail 1; Cross Chop 1; Thunder Fang 8; Metal Claw 15; Roar 21,50; Hyper Fang 24; Body Slam 30; Liquidation 47; Earthquake 58; Ice Punch 63.
- Removed against today's: Scratch 1; Leer 1; Water Gun 1,6; Rage 1,8; Scary Face 15; Flail 24; Agility 30; Screech 45; Thrash 50; Superpower 63; Hydro Pump 71.
- Moved against today's: Slash 37 to 6; Ice Fang 21 to 42; Aqua Tail 58 to 71.
- Against Kaizo's: Kaizo's ViceGrip 47 became Liquidation.

**Sentret (161)**, 14 moves:

- New list: Quick Attack 1, Secret Power 1, Follow Me 4, Knock Off 7, Helping Hand 13, Fury Swipes 16, Slam 19, Sucker Punch 25, Thunder Wave 28, Me First 31, Hyper Voice 36, Super Fang 39, Double-Edge 42, Quick Attack 47.
- Added against today's: Secret Power 1; Knock Off 7; Thunder Wave 28; Super Fang 39; Double-Edge 42.
- Removed against today's: Scratch 1; Foresight 1; Defense Curl 4; Rest 28; Amnesia 36; Baton Pass 39.
- Moved against today's: Quick Attack 7 to 1,47; Follow Me 19 to 4; Helping Hand 16 to 13; Fury Swipes 13 to 16; Slam 25 to 19; Sucker Punch 31 to 25; Me First 42 to 31; Hyper Voice 47 to 36.
- Against Kaizo's: the same.

**Furret (162)**, 15 moves:

- New list: Quick Attack 1, Dig 1, Night Slash 1, Follow Me 4, Quick Attack 7, Fury Swipes 13, Helping Hand 17, Knock Off 21, Body Slam 28, Thunder Wave 32, Hyper Voice 36, Super Fang 42, Sucker Punch 46, Slam 50, Quick Attack 56.
- Added against today's: Dig 1; Night Slash 1; Knock Off 21; Body Slam 28; Thunder Wave 32; Super Fang 42.
- Removed against today's: Scratch 1; Foresight 1; Defense Curl 1,4; Rest 32; Amnesia 42; Baton Pass 46; Me First 50.
- Moved against today's: Quick Attack 1,7 to 1,7,56; Follow Me 21 to 4; Hyper Voice 56 to 36; Sucker Punch 36 to 46; Slam 28 to 50.
- Rule: Quick Attack 1 listed twice; one kept.

**Hoothoot (163)**, 15 moves:

- New list: Tackle 1, Peck 1, Foresight 1, Uproar 5, Steel Wing 9, Zen Headbutt 13, Aerial Ace 17, Whirlwind 21, Extrasensory 25, Take Down 27, Hypnosis 33, Roost 37, Air Slash 41, Hyper Voice 45, Psycho Shift 49.
- Added against today's: Steel Wing 9; Aerial Ace 17; Whirlwind 21; Hyper Voice 45.
- Removed against today's: Growl 1; Reflect 17; Confusion 21; Dream Eater 49.
- Moved against today's: Peck 9 to 1; Uproar 13 to 5; Zen Headbutt 33 to 13; Extrasensory 37 to 25; Take Down 25 to 27; Hypnosis 5 to 33; Roost 45 to 37; Air Slash 29 to 41; Psycho Shift 41 to 49.
- Against Kaizo's: the same.

**Noctowl (164)**, 18 moves:

- New list: Pluck 1, Hypnosis 1, Swift 1, Foresight 1, Night Shade 1, Steel Wing 5, Zen Headbutt 9, Uproar 13, Aerial Ace 17, Extrasensory 22, Take Down 29, Foresight 32, Whirlwind 37, Roost 42, Air Slash 47, Hyper Voice 52, Psycho Shift 57, Sky Attack 65.
- Added against today's: Pluck 1; Swift 1; Night Shade 1; Steel Wing 5; Aerial Ace 17; Whirlwind 37; Hyper Voice 52.
- Removed against today's: Tackle 1; Growl 1; Peck 9; Reflect 17; Confusion 22; Dream Eater 57.
- Moved against today's: Hypnosis 1,5 to 1; Foresight 1 to 1,32; Zen Headbutt 37 to 9; Extrasensory 42 to 22; Take Down 27 to 29; Roost 52 to 42; Air Slash 32 to 47; Psycho Shift 47 to 57; Sky Attack 1 to 65.
- Against Kaizo's: the same.

**Crobat (169)**, 17 moves:

- New list: Cross Poison 1, Giga Drain 1, Leech Life 1, Supersonic 1, Heat Wave 1, Wing Attack 5, Leech Life 9, Poison Jab 13, Bite 17, Steel Wing 21, Aerial Ace 27, Whirlwind 33, Confuse Ray 39, Crunch 45, Brave Bird 80, Poison Fang 85, Whirlwind 90.
- Added against today's: Giga Drain 1; Heat Wave 1; Poison Jab 13; Steel Wing 21; Aerial Ace 27; Whirlwind 33,90; Crunch 45; Brave Bird 80.
- Removed against today's: Screech 1; Astonish 1,9; Air Cutter 27; Mean Look 33; Haze 45; Air Slash 51.
- Moved against today's: Leech Life 1 to 1,9; Supersonic 1,5 to 1; Wing Attack 17 to 5; Bite 13 to 17; Confuse Ray 21 to 39; Poison Fang 39 to 85.
- Against Kaizo's: the same.

**Chinchou (170)**, 14 moves:

- New list: Bubble 1, ThunderShock 1, Supersonic 6, Thunder Wave 9, Water Gun 12, Shock Wave 17, Confuse Ray 20, Aurora Beam 23, BubbleBeam 28, Wild Charge 31, Flash 34, Signal Beam 39, Hydro Pump 42, Discharge 45.
- Added against today's: ThunderShock 1; Shock Wave 17; Aurora Beam 23; Wild Charge 31; Flash 34.
- Removed against today's: Flail 9; Spark 20; Take Down 23; Aqua Ring 39; Charge 45.
- Moved against today's: Supersonic 1 to 6; Thunder Wave 6 to 9; Confuse Ray 17 to 20; Signal Beam 31 to 39; Discharge 34 to 45.
- Against Kaizo's: the same.

**Lanturn (171)**, 18 moves:

- New list: Psybeam 1, Flash Cannon 1, Supersonic 1, Flail 6, Water Pulse 9, ThunderShock 12, Supersonic 17, Thunder Wave 20, Water Pulse 23, Confuse Ray 27, Flash 27, Attract 27, Brine 30, Shock Wave 35, Flash 40, Signal Beam 47, Hydro Pump 52, Discharge 57.
- Added against today's: Psybeam 1; Flash Cannon 1; Water Pulse 9,23; ThunderShock 12; Flash 27,40; Attract 27; Brine 30; Shock Wave 35.
- Removed against today's: Bubble 1; Water Gun 12; Spark 20; Take Down 23; Stockpile 27; Swallow 27; Spit Up 27; BubbleBeam 30; Aqua Ring 47; Charge 57.
- Moved against today's: Supersonic 1 to 1,17; Flail 9 to 6; Thunder Wave 1,6 to 20; Confuse Ray 17 to 27; Signal Beam 35 to 47; Discharge 40 to 57.
- Against Kaizo's: the same.

**Pichu (172)**, 6 moves:

- New list: ThunderShock 1, Sweet Kiss 1, Thunder Wave 5, Surf 55, Volt Tackle 65, ExtremeSpeed 75.
- Added against today's: Surf 55; Volt Tackle 65; ExtremeSpeed 75.
- Removed against today's: Charm 1; Tail Whip 5; Nasty Plot 18.
- Moved against today's: Sweet Kiss 13 to 1; Thunder Wave 10 to 5.
- Against Kaizo's: the same.

**Cleffa (173)**, 6 moves:

- New list: Pound 1, Metronome 1, Present 7, Sweet Kiss 45, Copycat 53, Sing 70.
- Added against today's: Metronome 1; Present 7.
- Removed against today's: Charm 1; Encore 4; Magical Leaf 16.
- Moved against today's: Sweet Kiss 10 to 45; Copycat 13 to 53; Sing 7 to 70.
- Against Kaizo's: the same.

**Togepi (175)**, 10 moves:

- New list: Present 1, Metronome 6, Sweet Kiss 10, Peck 15, Double-Edge 24, Magical Leaf 28, Shadow Ball 33, AncientPower 42, Tri Attack 46, Yawn 51.
- Added against today's: Present 1; Peck 15; Magical Leaf 28; Shadow Ball 33; Tri Attack 46.
- Removed against today's: Growl 1; Charm 1; Encore 19; Follow Me 24; Wish 28; Safeguard 37; Baton Pass 42; Last Resort 51.
- Moved against today's: Double-Edge 46 to 24; AncientPower 33 to 42; Yawn 15 to 51.
- Rule: Teleport 1 out: Splash and Teleport go.
- Rule: Teleport 19 out: Splash and Teleport go.
- Rule: Teleport 37 out: Splash and Teleport go.

**Togetic (176)**, 13 moves:

- New list: Present 1, Metronome 1, Sweet Kiss 1, Facade 1, Double-Edge 10, Magical Leaf 15, Shadow Ball 19, Seismic Toss 28, Steel Wing 33, Whirlwind 37, Tri Attack 42, Aura Sphere 46, Air Slash 51.
- Added against today's: Present 1; Facade 1; Shadow Ball 19; Seismic Toss 28; Steel Wing 33; Whirlwind 37; Tri Attack 42; Aura Sphere 46; Air Slash 51.
- Removed against today's: Growl 1; Charm 1; Yawn 15; Encore 19; Follow Me 24; Wish 28; AncientPower 33; Safeguard 37; Baton Pass 42; Last Resort 51.
- Moved against today's: Metronome 1,6 to 1; Sweet Kiss 1,10 to 1; Double-Edge 46 to 10; Magical Leaf 1 to 15.
- Rule: Teleport 1 out: Splash and Teleport go.
- Rule: Teleport 6 out: Splash and Teleport go.
- Rule: Teleport 24 out: Splash and Teleport go.

**Mareep (179)**, 11 moves:

- New list: ThunderShock 1, Tackle 5, Thunder Wave 10, Swift 14, Hidden Power 19, Body Slam 23, Iron Tail 28, Discharge 32, Signal Beam 37, Power Gem 41, Thunderbolt 46.
- Added against today's: Swift 14; Hidden Power 19; Body Slam 23; Iron Tail 28; Thunderbolt 46.
- Removed against today's: Growl 5; Cotton Spore 19; Charge 23; Light Screen 37; Thunder 46.
- Moved against today's: ThunderShock 10 to 1; Tackle 1 to 5; Thunder Wave 14 to 10; Discharge 28 to 32; Signal Beam 32 to 37.
- Against Kaizo's: the same.

**Flaaffy (180)**, 13 moves:

- New list: Flash 1, Tackle 1, ThunderShock 1, Swift 5, Thunder Wave 10, Shock Wave 14, Body Slam 20, Iron Tail 25, Fire Punch 33, Discharge 36, Power Gem 42, Signal Beam 47, Thunderbolt 53.
- Added against today's: Flash 1; Swift 5; Shock Wave 14; Body Slam 20; Iron Tail 25; Fire Punch 33; Thunderbolt 53.
- Removed against today's: Growl 1,5; Cotton Spore 20; Charge 25; Light Screen 42; Thunder 53.
- Moved against today's: ThunderShock 1,10 to 1; Thunder Wave 14 to 10; Discharge 31 to 36; Power Gem 47 to 42; Signal Beam 36 to 47.
- Against Kaizo's: the same.

**Ampharos (181)**, 16 moves:

- New list: Cross Chop 1, Fire Punch 1, Flash Cannon 1, ThunderPunch 1, Thunder Wave 1, Headbutt 5, Iron Tail 10, Shock Wave 14, Body Slam 20, Flash 25, Power Gem 30, Discharge 34, Signal Beam 42, Mirror Shot 51, Dragon Pulse 59, Thunderbolt 68.
- Added against today's: Cross Chop 1; Flash Cannon 1; Headbutt 5; Iron Tail 10; Shock Wave 14; Body Slam 20; Flash 25; Mirror Shot 51; Dragon Pulse 59; Thunderbolt 68.
- Removed against today's: Tackle 1; Growl 1,5; ThunderShock 1,10; Cotton Spore 20; Charge 25; Light Screen 51; Thunder 68.
- Moved against today's: ThunderPunch 30 to 1; Thunder Wave 1,14 to 1; Power Gem 59 to 30.
- Against Kaizo's: the same.

**Marill (183)**, 11 moves:

- New list: Present 1, Water Gun 12, Pound 17, BubbleBeam 20, Brick Break 25, Body Slam 28, Dive 33, Double-Edge 37, Ice Punch 42, Bounce 47, Aqua Tail 52.
- Added against today's: Present 1; Pound 17; Brick Break 25; Body Slam 28; Dive 33; Ice Punch 42; Bounce 47.
- Removed against today's: Tackle 1; Defense Curl 2; Tail Whip 7; Rollout 15; Aqua Ring 23; Rain Dance 32; Hydro Pump 42.
- Moved against today's: Water Gun 10 to 12; BubbleBeam 18 to 20; Double-Edge 27 to 37; Aqua Tail 37 to 52.
- Against Kaizo's: the same.

**Azumarill (184)**, 14 moves:

- New list: Present 1, Seismic Toss 1, Aurora Beam 1, Foresight 1, Brick Break 12, BubbleBeam 17, Body Slam 20, Iron Tail 25, Body Slam 30, Hydro Pump 37, Take Down 43, Dive 50, Ice Punch 57, Aqua Tail 80.
- Added against today's: Present 1; Seismic Toss 1; Aurora Beam 1; Foresight 1; Brick Break 12; Body Slam 20,30; Iron Tail 25; Take Down 43; Dive 50; Ice Punch 57.
- Removed against today's: Tackle 1; Defense Curl 1,2; Tail Whip 1,7; Water Gun 1,10; Rollout 15; Aqua Ring 27; Double-Edge 33; Rain Dance 40.
- Moved against today's: BubbleBeam 20 to 17; Hydro Pump 54 to 37; Aqua Tail 47 to 80.
- Against Kaizo's: the same.

**Sudowoodo (185)**, 17 moves:

- New list: Fire Punch 1, Copycat 1, ThunderPunch 1, Ice Punch 1, Block 1, Mimic 6, Low Kick 9, Faint Attack 14, Rock Slide 17, Selfdestruct 22, Brick Break 25, Take Down 30, Rock Slide 33, Explosion 38, Earthquake 41, Hammer Arm 46, Wood Hammer 49.
- Added against today's: Fire Punch 1; ThunderPunch 1; Ice Punch 1; Selfdestruct 22; Brick Break 25; Take Down 30; Explosion 38; Earthquake 41.
- Removed against today's: Flail 1,6; Rock Throw 1,14; Rock Tomb 30; Slam 38; Sucker Punch 41; Double-Edge 46.
- Moved against today's: Block 22 to 1; Mimic 17 to 6; Low Kick 1,9 to 9; Faint Attack 25 to 14; Rock Slide 33 to 17,33; Hammer Arm 49 to 46; Wood Hammer 1 to 49.
- Against Kaizo's: the same.

**Politoed (186)**, 7 moves:

- New list: Bounce 1, Hypnosis 1, BubbleBeam 1, Hyper Voice 1, Ice Beam 27, Earth Power 37, Hydro Pump 65.
- Added against today's: Ice Beam 27; Earth Power 37; Hydro Pump 65.
- Removed against today's: DoubleSlap 1; Perish Song 1; Swagger 27.
- Moved against today's: Bounce 37 to 1; Hyper Voice 48 to 1.
- Against Kaizo's: the same.

**Hoppip (187)**, 16 moves:

- New list: Absorb 1, Tackle 4, Gust 7, Confusion 10, Mega Drain 12, Headbutt 14, Whirlwind 16, PoisonPowder 18, Bullet Seed 22, Aerial Ace 25, Secret Power 28, Seed Bomb 31, Explosion 34, Double-Edge 37, Energy Ball 40, Bounce 43.
- Added against today's: Absorb 1; Gust 7; Confusion 10; Headbutt 14; Whirlwind 16; Aerial Ace 25; Secret Power 28; Seed Bomb 31; Explosion 34; Double-Edge 37; Energy Ball 40.
- Removed against today's: Splash 1; Synthesis 4; Tail Whip 7; Stun Spore 14; Sleep Powder 16; Leech Seed 22; Cotton Spore 28; U-turn 31; Worry Seed 34; Giga Drain 37; Memento 43.
- Moved against today's: Tackle 10 to 4; Mega Drain 25 to 12; PoisonPowder 12 to 18; Bullet Seed 19 to 22; Bounce 40 to 43.
- Against Kaizo's: Kaizo's Absorb 1 left out: Oxide has no move like it.
- Against Kaizo's: Kaizo's Memento 34 became Explosion.
- Rule: Absorb at 1, the balance track's pick, as its only level-1 move.

**Skiploom (188)**, 18 moves:

- New list: Double-Edge 1, Pay Day 1, Headbutt 1, Gust 4, Explosion 7, Secret Power 10, Bullet Seed 12, Confusion 14, PoisonPowder 16, Take Down 20, Whirlwind 24, Seed Bomb 28, Aerial Ace 32, Stun Spore 36, Explosion 40, Energy Ball 44, Bounce 48, Synthesis 64.
- Added against today's: Double-Edge 1; Pay Day 1; Headbutt 1; Gust 4; Explosion 7,40; Secret Power 10; Confusion 14; Take Down 20; Whirlwind 24; Seed Bomb 28; Aerial Ace 32; Energy Ball 44.
- Removed against today's: Splash 1; Tail Whip 1,7; Tackle 1,10; Sleep Powder 16; Leech Seed 24; Mega Drain 28; Cotton Spore 32; U-turn 36; Worry Seed 40; Giga Drain 44; Memento 52.
- Moved against today's: Bullet Seed 20 to 12; PoisonPowder 12 to 16; Stun Spore 14 to 36; Synthesis 1,4 to 64.
- Against Kaizo's: Kaizo's Absorb 1 left out: Oxide has no move like it.
- Against Kaizo's: Kaizo's Memento 7 became Explosion.
- Against Kaizo's: Kaizo's Memento 40 became Explosion.

**Jumpluff (189)**, 19 moves:

- New list: Helping Hand 1, Secret Power 1, Confusion 1, Pay Day 1, Synthesis 4, Double-Edge 7, Cotton Spore 10, Explosion 12, Bullet Seed 14, Headbutt 16, PoisonPowder 20, Silver Wind 24, Seed Bomb 28, Aerial Ace 32, Stun Spore 40, Explosion 48, Energy Ball 54, Bounce 60, Sleep Powder 72.
- Added against today's: Helping Hand 1; Secret Power 1; Confusion 1; Pay Day 1; Double-Edge 7; Explosion 12,48; Headbutt 16; Silver Wind 24; Seed Bomb 28; Aerial Ace 32; Energy Ball 54.
- Removed against today's: Splash 1; Tail Whip 1,7; Tackle 1,10; Leech Seed 24; Mega Drain 28; U-turn 36; Worry Seed 40; Giga Drain 44; Memento 52.
- Moved against today's: Synthesis 1,4 to 4; Cotton Spore 32 to 10; Bullet Seed 20 to 14; PoisonPowder 12 to 20; Stun Spore 14 to 40; Bounce 48 to 60; Sleep Powder 16 to 72.
- Against Kaizo's: Kaizo's Memento 12 became Explosion.
- Against Kaizo's: Kaizo's Memento 48 became Explosion.

**Aipom (190)**, 15 moves:

- New list: Astonish 1, Scratch 1, Sand-Attack 4, Swift 8, Water Gun 11, Slash 15, Faint Attack 18, Metal Claw 22, Karate Chop 25, Headbutt 29, Bite 32, Aerial Ace 36, Force Palm 49, Double Hit 63, Fake Out 77.
- Added against today's: Water Gun 11; Slash 15; Faint Attack 18; Metal Claw 22; Karate Chop 25; Headbutt 29; Bite 32; Aerial Ace 36; Force Palm 49; Fake Out 77.
- Removed against today's: Tail Whip 1; Baton Pass 11; Tickle 15; Fury Swipes 18; Screech 25; Agility 29; Fling 36; Nasty Plot 39; Last Resort 43.
- Moved against today's: Astonish 8 to 1; Swift 22 to 8; Double Hit 32 to 63.
- Against Kaizo's: the same.

**Yanma (193)**, 16 moves:

- New list: Quick Attack 1, Pursuit 1, Whirlwind 6, Leech Life 11, SonicBoom 14, Uproar 17, Supersonic 22, Whirlwind 27, Bug Bite 30, Wing Attack 33, Swift 38, Steel Wing 43, Whirlwind 46, AncientPower 49, Air Slash 54, Bug Buzz 57.
- Added against today's: Whirlwind 6,27,46; Leech Life 11; Bug Bite 30; Swift 38; Steel Wing 43.
- Removed against today's: Tackle 1; Foresight 1; Double Team 11; Detect 17; Hypnosis 38; Screech 46; U-turn 49.
- Moved against today's: Quick Attack 6 to 1; Pursuit 30 to 1; Uproar 27 to 17; Wing Attack 43 to 33; AncientPower 33 to 49.
- Against Kaizo's: the same.

**Wooper (194)**, 13 moves:

- New list: Water Gun 1, Acid 1, Mud Shot 5, Double Kick 9, Water Pulse 15, Headbutt 19, Mud Bomb 23, Muddy Water 29, Sludge Bomb 33, Rock Slide 37, Earthquake 43, Aqua Tail 43, Yawn 57.
- Added against today's: Acid 1; Double Kick 9; Water Pulse 15; Headbutt 19; Sludge Bomb 33; Rock Slide 37; Aqua Tail 43.
- Removed against today's: Tail Whip 1; Mud Sport 5; Slam 15; Amnesia 23; Rain Dance 37; Mist 43; Haze 43.
- Moved against today's: Mud Shot 9 to 5; Mud Bomb 19 to 23; Muddy Water 47 to 29; Earthquake 33 to 43; Yawn 29 to 57.
- Against Kaizo's: the same.

**Quagsire (195)**, 14 moves:

- New list: Water Gun 1, Acid 1, Sludge Bomb 1, Dig 5, Mud Shot 9, Water Pulse 15, Body Slam 19, Mud Bomb 24, Muddy Water 31, Poison Jab 40, Ice Punch 45, Earthquake 53, Aqua Tail 60, Yawn 69.
- Added against today's: Acid 1; Sludge Bomb 1; Dig 5; Water Pulse 15; Body Slam 19; Poison Jab 40; Ice Punch 45; Aqua Tail 60.
- Removed against today's: Tail Whip 1; Mud Sport 1,5; Slam 15; Amnesia 24; Rain Dance 41; Mist 48; Haze 48.
- Moved against today's: Mud Bomb 19 to 24; Muddy Water 53 to 31; Earthquake 36 to 53; Yawn 31 to 69.
- Against Kaizo's: the same.

**Espeon (196)**, 12 moves:

- New list: Mud-Slap 1, Tackle 1, Bite 8, Confusion 15, Quick Attack 22, Swift 29, Psybeam 36, Future Sight 43, Signal Beam 50, Psychic 64, Morning Sun 71, Power Swap 78.
- Added against today's: Mud-Slap 1; Bite 8; Signal Beam 50.
- Removed against today's: Tail Whip 1; Helping Hand 1; Sand-Attack 8; Last Resort 50; Psych Up 57.
- Rule: Teleport 1 out: Splash and Teleport go.
- Rule: Teleport 57 out: Splash and Teleport go.

**Umbreon (197)**, 14 moves:

- New list: Payback 1, Tackle 1, Faint Attack 1, Secret Power 8, Bite 15, Confuse Ray 22, Body Slam 29, Crunch 36, Assurance 43, Sand-Attack 50, Pursuit 57, Double Kick 64, Moonlight 71, Guard Swap 78.
- Added against today's: Payback 1; Secret Power 8; Bite 15; Body Slam 29; Crunch 36; Double Kick 64.
- Removed against today's: Tail Whip 1; Helping Hand 1; Quick Attack 22; Last Resort 50; Mean Look 57; Screech 64.
- Moved against today's: Faint Attack 36 to 1; Confuse Ray 29 to 22; Sand-Attack 8 to 50; Pursuit 15 to 57.
- Against Kaizo's: the same.

**Murkrow (198)**, 11 moves:

- New list: Air Slash 1, Pursuit 1, Whirlwind 5, Assurance 31, Drill Peck 35, Night Shade 45, Dark Pulse 50, Whirlwind 51, Brave Bird 55, Heat Wave 61, Night Slash 65.
- Added against today's: Air Slash 1; Whirlwind 5,51; Drill Peck 35; Dark Pulse 50; Brave Bird 55; Heat Wave 61; Night Slash 65.
- Removed against today's: Peck 1; Astonish 1; Haze 11; Wing Attack 15; Taunt 31; Faint Attack 35; Mean Look 41; Sucker Punch 45.
- Moved against today's: Pursuit 5 to 1; Assurance 25 to 31; Night Shade 21 to 45.
- Against Kaizo's: the same.

**Slowking (199)**, 16 moves:

- New list: Trump Card 1, Psych Up 1, Headbutt 1, Aurora Beam 1, Confusion 1, Body Slam 6, Water Pulse 11, Disable 15, Swagger 20, Power Gem 25, Zen Headbutt 29, Aqua Tail 34, Yawn 39, Psychic 48, Hydro Pump 53, Slack Off 57.
- Added against today's: Aurora Beam 1; Body Slam 6; Aqua Tail 34; Hydro Pump 53; Slack Off 57.
- Removed against today's: Hidden Power 1; Curse 1; Tackle 1; Growl 6; Water Gun 11; Nasty Plot 39.
- Moved against today's: Trump Card 53 to 1; Psych Up 57 to 1; Headbutt 25 to 1; Confusion 15 to 1; Water Pulse 29 to 11; Disable 20 to 15; Swagger 43 to 20; Power Gem 1 to 25; Zen Headbutt 34 to 29; Yawn 1 to 39.
- Rule: Teleport 43 out: Splash and Teleport go.

**Misdreavus (200)**, 11 moves:

- New list: Astonish 1, Bite 1, Uproar 5, Night Shade 14, Confuse Ray 19, Psybeam 23, Power Gem 28, Ominous Wind 32, Pain Split 41, Shadow Ball 46, Shadow Sneak 80.
- Added against today's: Bite 1; Uproar 5; Night Shade 14; Ominous Wind 32; Shadow Sneak 80.
- Removed against today's: Growl 1; Psywave 1; Spite 5; Mean Look 19; Payback 32; Perish Song 41; Grudge 46.
- Moved against today's: Astonish 10 to 1; Confuse Ray 14 to 19; Power Gem 50 to 28; Pain Split 28 to 41; Shadow Ball 37 to 46.
- Rule: Teleport 10 out: Splash and Teleport go.
- Rule: Teleport 37 out: Splash and Teleport go.

**Girafarig (203)**, 15 moves:

- New list: Double Kick 1, Odor Sleuth 1, High Horsepower 1, Confusion 1, Bite 1, Body Slam 5, Psybeam 10, Bite 14, Guard Swap 19, Sleep Talk 23, Crunch 28, Double Hit 32, Psychic 37, Earthquake 41, Power Swap 46.
- Added against today's: Double Kick 1; High Horsepower 1; Bite 1,14; Body Slam 5; Sleep Talk 23; Earthquake 41.
- Removed against today's: Astonish 1; Tackle 1; Growl 1; Stomp 10; Agility 14; Baton Pass 23; Assurance 28; Zen Headbutt 41.
- Moved against today's: Odor Sleuth 5 to 1; Psybeam 19 to 10; Guard Swap 1 to 19; Crunch 46 to 28; Power Swap 1 to 46.
- Against Kaizo's: Kaizo's Stomp 1 became High Horsepower.

**Gligar (207)**, 13 moves:

- New list: Night Slash 1, Liquidation 5, Brick Break 9, X-Scissor 12, Dig 16, Poison Sting 20, Rock Slide 23, Wing Attack 27, Aerial Ace 31, Poison Jab 34, Crunch 45, Aqua Tail 65, Earthquake 80.
- Added against today's: Night Slash 1; Liquidation 5; Brick Break 9; Dig 16; Rock Slide 23; Wing Attack 27; Aerial Ace 31; Poison Jab 34; Crunch 45; Aqua Tail 65; Earthquake 80.
- Removed against today's: Sand-Attack 5; Harden 9; Knock Off 12; Quick Attack 16; Fury Cutter 20; Faint Attack 23; Screech 27; Slash 31; Swords Dance 34; U-turn 38; Guillotine 45.
- Moved against today's: X-Scissor 42 to 12; Poison Sting 1 to 20.
- Against Kaizo's: Kaizo's ViceGrip 5 became Liquidation.

**Steelix (208)**, 20 moves:

- New list: Thunder Fang 1, Ice Fang 1, Fire Fang 1, Roar 1, Dig 1, Screech 1, Poison Jab 1, Slam 6, Roar 9, Aqua Tail 14, Iron Tail 17, Rock Slide 22, Crunch 25, Selfdestruct 30, Gyro Ball 33, Iron Head 44, Explosion 47, Roar 50, Earthquake 54, Stone Edge 70.
- Added against today's: Roar 1,9,50; Dig 1; Poison Jab 1; Aqua Tail 14; Rock Slide 22; Selfdestruct 30; Gyro Ball 33; Iron Head 44; Explosion 47; Earthquake 54.
- Removed against today's: Mud Sport 1; Tackle 1; Harden 1; Bind 1; Rock Throw 9; Rage 14; Rock Tomb 17; Sandstorm 22; Rock Polish 30; DragonBreath 33; Curse 38; Double-Edge 49.
- Moved against today's: Screech 6 to 1; Slam 25 to 6; Iron Tail 41 to 17; Crunch 46 to 25; Stone Edge 54 to 70.
- Against Kaizo's: Kaizo's Swallow 1 became Poison Jab.

**Snubbull (209)**, 15 moves:

- New list: Odor Sleuth 1, Snore 1, Pound 1, Tackle 1, Shadow Claw 1, Bite 1, Roar 1, Present 7, Metronome 13, Double Kick 19, Body Slam 25, Roar 31, Crunch 37, Seismic Toss 43, Thrash 79.
- Added against today's: Odor Sleuth 1; Snore 1; Pound 1; Shadow Claw 1; Present 7; Metronome 13; Double Kick 19; Body Slam 25; Seismic Toss 43; Thrash 79.
- Removed against today's: Ice Fang 1; Fire Fang 1; Thunder Fang 1; Scary Face 1; Tail Whip 1; Charm 1; Lick 13; Headbutt 19; Rage 31; Take Down 37; Payback 43.
- Moved against today's: Bite 7 to 1; Roar 25 to 1,31; Crunch 49 to 37.
- Against Kaizo's: Kaizo's Lick 1 became Shadow Claw.

**Granbull (210)**, 15 moves:

- New list: Ice Fang 1, Fire Fang 1, Thunder Fang 1, Tackle 1, Shadow Claw 1, Bite 1, Roar 1, Headbutt 7, Payback 13, Brick Break 19, Body Slam 27, Roar 35, Crunch 43, Earthquake 51, Double-Edge 59.
- Added against today's: Shadow Claw 1; Brick Break 19; Body Slam 27; Earthquake 51; Double-Edge 59.
- Removed against today's: Scary Face 1; Tail Whip 1; Charm 1; Lick 13; Rage 35; Take Down 43.
- Moved against today's: Bite 7 to 1; Roar 27 to 1,35; Headbutt 19 to 7; Payback 51 to 13; Crunch 59 to 43.
- Against Kaizo's: Kaizo's Lick 1 became Shadow Claw.

**Qwilfish (211)**, 18 moves:

- New list: Poison Sting 1, Toxic 1, BubbleBeam 1, Selfdestruct 9, Pin Missile 9, Shadow Ball 13, Brine 17, Explosion 21, Twineedle 25, Payback 25, Double-Edge 29, Hydro Pump 33, Poison Jab 37, Selfdestruct 41, Explosion 45, Dive 49, Poison Tail 73, Aqua Tail 87.
- Added against today's: Toxic 1; BubbleBeam 1; Selfdestruct 9,41; Shadow Ball 13; Explosion 21,45; Twineedle 25; Payback 25; Double-Edge 29; Dive 49; Poison Tail 73.
- Removed against today's: Spikes 1; Tackle 1; Harden 9; Minimize 9; Water Gun 13; Rollout 17; Toxic Spikes 21; Stockpile 25; Spit Up 25; Revenge 29; Take Down 41; Destiny Bond 53.
- Moved against today's: Pin Missile 37 to 9; Brine 33 to 17; Hydro Pump 57 to 33; Poison Jab 49 to 37; Aqua Tail 45 to 87.
- Against Kaizo's: the same.

**Scizor (212)**, 18 moves:

- New list: Double Hit 1, Flash Cannon 1, Silver Wind 1, Liquidation 5, Wing Attack 9, Bug Buzz 13, Double-Edge 17, Steel Wing 21, Brick Break 25, Aerial Ace 29, Feint 33, Metal Claw 37, Slash 41, Night Slash 45, Cross Chop 49, Iron Head 53, X-Scissor 57, Pursuit 61.
- Added against today's: Flash Cannon 1; Silver Wind 1; Liquidation 5; Wing Attack 9; Bug Buzz 13; Double-Edge 17; Steel Wing 21; Brick Break 25; Aerial Ace 29; Cross Chop 49.
- Removed against today's: Bullet Punch 1; Quick Attack 1; Leer 1; Focus Energy 5; False Swipe 13; Agility 17; Fury Cutter 25; Razor Wind 33; Iron Defense 37; Swords Dance 57.
- Moved against today's: Double Hit 49 to 1; Feint 61 to 33; Metal Claw 21 to 37; Slash 29 to 41; X-Scissor 41 to 57; Pursuit 9 to 61.
- Against Kaizo's: Kaizo's ViceGrip 5 became Liquidation.

**Heracross (214)**, 14 moves:

- New list: Close Combat 1, Leech Life 1, Seismic Toss 1, Aerial Ace 1, Karate Chop 1, Pin Missile 7, Rock Slide 13, Night Slash 19, Brick Break 25, X-Scissor 31, Facade 37, Pursuit 43, Cross Chop 49, Megahorn 55.
- Added against today's: Leech Life 1; Seismic Toss 1; Karate Chop 1; Pin Missile 7; Rock Slide 13; X-Scissor 31; Facade 37; Pursuit 43; Cross Chop 49.
- Removed against today's: Tackle 1; Leer 1; Horn Attack 1; Endure 1; Fury Attack 7; Counter 25; Take Down 31; Reversal 43; Feint 49.
- Moved against today's: Close Combat 37 to 1; Aerial Ace 13 to 1; Night Slash 1 to 19; Brick Break 19 to 25.
- Against Kaizo's: the same.

**Sneasel (215)**, 12 moves:

- New list: Scratch 1, Powder Snow 1, Dark Pulse 1, Ice Fang 10, Faint Attack 14, Slash 21, Metal Claw 24, Ice Punch 28, Night Slash 35, Aerial Ace 38, Brick Break 42, Ice Shard 99.
- Added against today's: Powder Snow 1; Dark Pulse 1; Ice Fang 10; Ice Punch 28; Night Slash 35; Aerial Ace 38; Brick Break 42.
- Removed against today's: Leer 1; Taunt 1; Quick Attack 8; Screech 10; Fury Swipes 21; Agility 24; Icy Wind 28.
- Moved against today's: Slash 35 to 21; Metal Claw 42 to 24; Ice Shard 49 to 99.
- Rule: Beat Up 8 out: Beat Up leaves the game.

**Slugma (218)**, 13 moves:

- New list: Fire Spin 1, Smog 1, Rock Throw 8, Recover 11, Rock Slide 21, Will-O-Wisp 23, Body Slam 25, Lava Plume 25, Heat Wave 38, Energy Ball 41, Earth Power 46, AncientPower 53, Magma Storm 56.
- Added against today's: Fire Spin 1; Will-O-Wisp 23; Heat Wave 38; Energy Ball 41; Magma Storm 56.
- Removed against today's: Yawn 1; Ember 8; Harden 16; Amnesia 31; Flamethrower 53.
- Moved against today's: Rock Throw 11 to 8; Recover 23 to 11; Rock Slide 41 to 21; Body Slam 46 to 25; Lava Plume 38 to 25; Earth Power 56 to 46; AncientPower 26 to 53.
- Against Kaizo's: the same.

**Magcargo (219)**, 15 moves:

- New list: Yawn 1, Selfdestruct 1, Hyper Beam 1, Fire Spin 1, Rock Throw 8, Recover 11, Lava Plume 16, Will-O-Wisp 23, Rock Slide 26, Energy Ball 31, Heat Wave 40, Explosion 45, Earth Power 52, AncientPower 61, Magma Storm 66.
- Added against today's: Selfdestruct 1; Hyper Beam 1; Fire Spin 1; Will-O-Wisp 23; Energy Ball 31; Heat Wave 40; Explosion 45; Magma Storm 66.
- Removed against today's: Smog 1; Ember 1,8; Harden 16; Amnesia 31; Body Slam 52; Flamethrower 61.
- Moved against today's: Rock Throw 1,11 to 8; Recover 23 to 11; Lava Plume 40 to 16; Rock Slide 45 to 26; Earth Power 66 to 52; AncientPower 26 to 61.
- Against Kaizo's: the same.

**Swinub (220)**, 14 moves:

- New list: Odor Sleuth 1, Powder Snow 1, Mud-Slap 4, Headbutt 8, Rock Throw 13, Aurora Beam 16, Dig 20, Rock Slide 25, Bite 28, Ice Fang 39, Earthquake 42, Crunch 45, Stone Edge 55, Icicle Spear 60.
- Added against today's: Headbutt 8; Rock Throw 13; Aurora Beam 16; Dig 20; Rock Slide 25; Bite 28; Ice Fang 39; Crunch 45; Stone Edge 55; Icicle Spear 60.
- Removed against today's: Tackle 1; Mud Sport 4; Endure 16; Mud Bomb 20; Icy Wind 25; Ice Shard 28; Take Down 32; Mist 40; Blizzard 44; Amnesia 49.
- Moved against today's: Powder Snow 8 to 1; Mud-Slap 13 to 4; Earthquake 37 to 42.
- Against Kaizo's: the same.

**Piloswine (221)**, 18 moves:

- New list: Brick Break 1, Double-Edge 1, Headbutt 1, Sand Tomb 1, Rock Throw 1, Powder Snow 4, Mud Bomb 8, Body Slam 13, Rock Slide 16, Ice Beam 20, Dig 25, Stone Edge 28, Ice Fang 32, Take Down 33, Roar 40, Crunch 48, Earthquake 56, Icicle Spear 65.
- Added against today's: Brick Break 1; Double-Edge 1; Headbutt 1; Sand Tomb 1; Rock Throw 1; Body Slam 13; Rock Slide 16; Ice Beam 20; Dig 25; Stone Edge 28; Roar 40; Crunch 48; Icicle Spear 65.
- Removed against today's: AncientPower 1; Peck 1; Odor Sleuth 1; Mud Sport 1,4; Mud-Slap 13; Endure 16; Icy Wind 25; Fury Attack 33; Mist 48; Blizzard 56; Amnesia 65.
- Moved against today's: Powder Snow 1,8 to 4; Mud Bomb 20 to 8; Ice Fang 28 to 32; Take Down 32 to 33; Earthquake 40 to 56.
- Against Kaizo's: the same.

**Corsola (222)**, 16 moves:

- New list: Rollout 1, AncientPower 4, BubbleBeam 8, Selfdestruct 13, Refresh 16, Power Gem 20, Recover 25, Muddy Water 28, Ice Beam 32, Rock Blast 37, Explosion 40, Aqua Cutter 44, Icicle Spear 48, Head Smash 53, Muddy Water 55, Scald 58.
- Added against today's: Rollout 1; Selfdestruct 13; Muddy Water 28,55; Ice Beam 32; Explosion 40; Aqua Cutter 44; Icicle Spear 48; Head Smash 53; Scald 58.
- Removed against today's: Tackle 1; Harden 4; Bubble 8; Lucky Chant 28; Aqua Ring 37; Spike Cannon 40; Mirror Coat 48; Earth Power 53.
- Moved against today's: AncientPower 32 to 4; BubbleBeam 25 to 8; Power Gem 44 to 20; Recover 13 to 25; Rock Blast 20 to 37.
- Against Kaizo's: the same.

**Remoraid (223)**, 12 moves:

- New list: Psybeam 1, Swift 3, Water Gun 5, Aurora Beam 14, Signal Beam 19, BubbleBeam 23, Water Pulse 27, Lock-On 32, Fire Blast 36, Hyper Beam 40, Hydro Pump 50, Hydro Cannon 93.
- Added against today's: Swift 3; Fire Blast 36; Hydro Pump 50; Hydro Cannon 93.
- Removed against today's: Focus Energy 23; Bullet Seed 27; Ice Beam 40.
- Moved against today's: Psybeam 10 to 1; Water Gun 1 to 5; Signal Beam 36 to 19; BubbleBeam 19 to 23; Water Pulse 32 to 27; Lock-On 6 to 32; Hyper Beam 45 to 40.
- Against Kaizo's: the same.

**Octillery (224)**, 17 moves:

- New list: Gunk Shot 1, Double-Edge 1, Mud Shot 1, SmokeScreen 1, Psybeam 1, Ice Beam 1, Wrap 6, BubbleBeam 10, Bullet Seed 14, Rock Blast 19, Signal Beam 23, Octazooka 25, Wring Out 29, Tri Attack 36, Head Smash 42, Submission 55, Hydro Pump 57.
- Added against today's: Double-Edge 1; Mud Shot 1; SmokeScreen 1; Wrap 6; Tri Attack 36; Head Smash 42; Submission 55; Hydro Pump 57.
- Removed against today's: Water Gun 1; Constrict 1,6; Aurora Beam 1,14; Focus Energy 23; Hyper Beam 55.
- Moved against today's: Psybeam 1,10 to 1; Ice Beam 48 to 1; BubbleBeam 19 to 10; Bullet Seed 29 to 14; Rock Blast 1 to 19; Signal Beam 42 to 23; Wring Out 36 to 29.
- Against Kaizo's: the same.

**Delibird (225)**, 11 moves:

- New list: Present 1, Powder Snow 4, Gust 7, Present 11, Aurora Beam 18, Icy Wind 22, Drill Run 25, Ice Beam 29, Blizzard 34, Destiny Bond 44, Spikes 80.
- Added against today's: Powder Snow 4; Gust 7; Aurora Beam 18; Icy Wind 22; Drill Run 25; Ice Beam 29; Blizzard 34; Destiny Bond 44; Spikes 80.
- Moved against today's: Present 1 to 1,11.
- Against Kaizo's: the same.

**Mantine (226)**, 18 moves:

- New list: Psybeam 1, Bullet Seed 1, Signal Beam 1, Tackle 1, Bubble 1, Supersonic 1, Twister 1, Mud-Slap 4, Bounce 10, BubbleBeam 13, Psybeam 19, Air Cutter 22, Signal Beam 28, Water Pulse 31, Confuse Ray 37, Air Slash 40, Ice Beam 46, Hydro Pump 49.
- Added against today's: Twister 1; Mud-Slap 4; Air Cutter 22; Air Slash 40; Ice Beam 46.
- Removed against today's: Headbutt 13; Agility 19; Wing Attack 22; Take Down 31; Aqua Ring 46.
- Moved against today's: Psybeam 1 to 1,19; Signal Beam 1 to 1,28; Supersonic 1,4 to 1; Bounce 40 to 10; BubbleBeam 1,10 to 13; Water Pulse 28 to 31.
- Against Kaizo's: the same.

**Skarmory (227)**, 14 moves:

- New list: Whirlwind 1, Wing Attack 1, Double-Edge 6, Roar 9, Take Down 12, Aerial Ace 17, Whirlwind 20, Flash Cannon 23, Double-Edge 28, Drill Peck 31, Roar 34, Whirlwind 39, Steel Wing 42, Brave Bird 45.
- Added against today's: Whirlwind 1,20,39; Wing Attack 1; Double-Edge 6,28; Roar 9,34; Take Down 12; Aerial Ace 17; Flash Cannon 23; Drill Peck 31; Brave Bird 45.
- Removed against today's: Leer 1; Peck 1; Sand-Attack 6; Swift 9; Agility 12; Fury Attack 17; Feint 20; Air Cutter 23; Spikes 28; Metal Sound 31; Air Slash 39; Slash 42; Night Slash 45.
- Moved against today's: Steel Wing 34 to 42.
- Against Kaizo's: the same.

**Houndour (228)**, 13 moves:

- New list: Roar 1, Pursuit 1, Smog 4, Ember 9, Bite 14, Roar 17, Double-Edge 22, Fire Fang 30, Faint Attack 35, Crunch 40, Roar 43, Flamethrower 48, Dark Pulse 53.
- Added against today's: Pursuit 1; Double-Edge 22; Dark Pulse 53.
- Removed against today's: Leer 1; Howl 4; Odor Sleuth 22; Embargo 40; Nasty Plot 53.
- Moved against today's: Roar 14 to 1,17,43; Smog 9 to 4; Ember 1 to 9; Bite 17 to 14; Crunch 48 to 40; Flamethrower 43 to 48.
- Rule: Beat Up 27 out: Beat Up leaves the game.

**Houndoom (229)**, 18 moves:

- New list: Smog 1, Pursuit 1, Ember 1, Roar 1, Sludge Bomb 1, Toxic 4, Fire Spin 9, Bite 14, Roar 17, Thunder Fang 22, Fire Fang 28, Crunch 32, Poison Fang 38, Roar 44, Flamethrower 60, Dark Pulse 70, Will-O-Wisp 90, Roar 92.
- Added against today's: Pursuit 1; Sludge Bomb 1; Toxic 4; Fire Spin 9; Poison Fang 38; Dark Pulse 70; Will-O-Wisp 90.
- Removed against today's: Leer 1; Howl 1,4; Odor Sleuth 22; Faint Attack 38; Embargo 44; Nasty Plot 60.
- Moved against today's: Smog 1,9 to 1; Roar 14 to 1,17,44,92; Bite 17 to 14; Thunder Fang 1 to 22; Fire Fang 32 to 28; Crunch 54 to 32; Flamethrower 48 to 60.
- Rule: Teleport 91 out: Splash and Teleport go.

**Kingdra (230)**, 16 moves:

- New list: Whirlpool 1, Water Pulse 1, SmokeScreen 1, Swift 1, Water Gun 1, SmokeScreen 4, Twister 8, Water Gun 11, Aurora Beam 14, Body Slam 18, Hydro Pump 23, DragonBreath 26, Double-Edge 30, Ice Beam 40, Octazooka 48, Dragon Pulse 57.
- Added against today's: Whirlpool 1; Water Pulse 1; Swift 1; Aurora Beam 14; Body Slam 18; DragonBreath 26; Double-Edge 30; Ice Beam 40; Octazooka 48.
- Removed against today's: Yawn 1; Bubble 1; Leer 1,8; Focus Energy 14; BubbleBeam 18; Agility 23; Brine 30; Dragon Dance 48.
- Moved against today's: Twister 26 to 8; Hydro Pump 40 to 23.
- Against Kaizo's: the same.

**Phanpy (231)**, 13 moves:

- New list: Odor Sleuth 1, Tackle 1, Water Gun 1, Rock Throw 1, Dig 6, Flail 10, Body Slam 15, Rock Slide 19, Bulldoze 24, Hydro Pump 28, Slam 33, Rollout 37, Earthquake 42.
- Added against today's: Water Gun 1; Rock Throw 1; Dig 6; Body Slam 15; Rock Slide 19; Bulldoze 24; Hydro Pump 28; Earthquake 42.
- Removed against today's: Growl 1; Defense Curl 1; Take Down 10; Natural Gift 19; Endure 28; Charm 33; Last Resort 37; Double-Edge 42.
- Moved against today's: Flail 6 to 10; Slam 24 to 33; Rollout 15 to 37.
- Against Kaizo's: the same.

**Donphan (232)**, 16 moves:

- New list: Fire Fang 1, Thunder Fang 1, Seed Bomb 1, Tackle 1, Rock Slide 1, Double-Edge 1, Rollout 6, Sand Tomb 10, Assurance 15, Body Slam 19, Rock Slide 24, Take Down 25, Roar 31, Slam 39, Rollout 46, Earthquake 54.
- Added against today's: Seed Bomb 1; Tackle 1; Rock Slide 1,24; Double-Edge 1; Sand Tomb 10; Body Slam 19; Take Down 25; Roar 31.
- Removed against today's: Horn Attack 1; Growl 1; Defense Curl 1; Flail 1; Rapid Spin 6; Knock Off 10; Magnitude 19; Fury Attack 25; Scary Face 39; Giga Impact 54.
- Moved against today's: Rollout 15 to 6,46; Assurance 31 to 15; Slam 24 to 39; Earthquake 46 to 54.
- Against Kaizo's: the same.

**Smoochum (238)**, 14 moves:

- New list: Pound 1, Shadow Claw 5, Sweet Kiss 8, Powder Snow 11, Confusion 15, Sweet Kiss 18, Seismic Toss 21, Psybeam 25, Aurora Beam 28, Copycat 31, Focus Blast 35, Psychic 38, Sing 41, Ice Beam 45.
- Added against today's: Shadow Claw 5; Seismic Toss 21; Psybeam 25; Aurora Beam 28; Focus Blast 35; Ice Beam 45.
- Removed against today's: Lick 5; Mean Look 21; Fake Tears 25; Lucky Chant 28; Avalanche 31; Perish Song 41; Blizzard 45.
- Moved against today's: Sweet Kiss 8 to 8,18; Copycat 38 to 31; Psychic 35 to 38; Sing 18 to 41.
- Against Kaizo's: Kaizo's Lick 5 became Shadow Claw.

**Elekid (239)**, 12 moves:

- New list: ThunderShock 1, Pound 1, Low Kick 7, Shock Wave 10, Seismic Toss 16, Swift 19, Karate Chop 25, Fire Punch 28, Cross Chop 34, Fire Punch 37, Ice Punch 43, Thunderbolt 46.
- Added against today's: Pound 1; Seismic Toss 16; Karate Chop 25; Fire Punch 28,37; Cross Chop 34; Ice Punch 43.
- Removed against today's: Quick Attack 1; Leer 1; Light Screen 25; ThunderPunch 28; Discharge 34; Screech 43; Thunder 46.
- Moved against today's: ThunderShock 7 to 1; Low Kick 10 to 7; Shock Wave 19 to 10; Swift 16 to 19; Thunderbolt 37 to 46.
- Against Kaizo's: the same.

**Magby (240)**, 12 moves:

- New list: Ember 1, Smog 1, Pound 7, Confuse Ray 10, Fire Punch 16, Faint Attack 19, ThunderPunch 25, Karate Chop 28, Lava Plume 34, Psychic 37, Cross Chop 43, Overheat 46.
- Added against today's: Pound 7; ThunderPunch 25; Karate Chop 28; Psychic 37; Cross Chop 43; Overheat 46.
- Removed against today's: Leer 1; SmokeScreen 10; Fire Spin 19; Flamethrower 37; Sunny Day 43; Fire Blast 46.
- Moved against today's: Ember 7 to 1; Confuse Ray 25 to 10; Fire Punch 28 to 16; Faint Attack 16 to 19.
- Against Kaizo's: the same.

**Blissey (242)**, 11 moves:

- New list: Pound 1, Submission 1, Take Down 9, Double-Edge 12, DoubleSlap 16, Metronome 20, Fling 27, Submission 31, Double-Edge 34, Take Down 42, Seed Bomb 46.
- Added against today's: Submission 1,31; Take Down 9,42; Metronome 20; Seed Bomb 46.
- Removed against today's: Growl 1; Tail Whip 5; Refresh 9; Softboiled 12; Minimize 20; Sing 23; Defense Curl 31; Light Screen 34; Egg Bomb 38; Healing Wish 42.
- Moved against today's: Double-Edge 46 to 12,34.
- Against Kaizo's: Kaizo's Egg Bomb 46 became Seed Bomb.
- Rule: Teleport 5 out: Splash and Teleport go.
- Rule: Teleport 23 out: Splash and Teleport go.
- Rule: Teleport 38 out: Splash and Teleport go.

**Suicune (245)**, 14 moves:

- New list: Bite 1, Ice Fang 1, Gust 8, Aurora Beam 15, BubbleBeam 22, Roar 29, Extrasensory 36, Hyper Beam 43, Air Slash 50, Brine 57, Roar 64, Ominous Wind 71, Ice Beam 78, Hydro Pump 85.
- Added against today's: Roar 29,64; Hyper Beam 43; Air Slash 50; Brine 57; Ominous Wind 71; Ice Beam 78.
- Removed against today's: Leer 1; Rain Dance 15; Mist 36; Mirror Coat 43; Tailwind 57; Calm Mind 78; Blizzard 85.
- Moved against today's: Ice Fang 50 to 1; Gust 22 to 8; Aurora Beam 29 to 15; BubbleBeam 8 to 22; Extrasensory 64 to 36; Hydro Pump 71 to 85.
- Against Kaizo's: the same.

**Larvitar (246)**, 13 moves:

- New list: Bite 1, Earth Power 1, Dark Pulse 5, Double-Edge 10, Roar 14, Bulldoze 19, Rock Slide 23, Crunch 28, Hyper Beam 32, Roar 37, Earthquake 41, Stone Edge 46, Double-Edge 50.
- Added against today's: Earth Power 1; Double-Edge 10,50; Roar 14,37; Bulldoze 19.
- Removed against today's: Leer 1; Sandstorm 5; Screech 10; Scary Face 19; Thrash 23; Payback 32.
- Moved against today's: Dark Pulse 28 to 5; Rock Slide 14 to 23; Crunch 37 to 28; Hyper Beam 50 to 32.
- Against Kaizo's: the same.

**Pupitar (247)**, 15 moves:

- New list: Assurance 1, Iron Head 1, Superpower 1, Poison Gas 1, Sand Tomb 5, Hyper Beam 10, Roar 14, Pursuit 19, Bulldoze 23, Rock Slide 28, Take Down 34, Roar 41, Earthquake 47, Stone Edge 54, Payback 60.
- Added against today's: Assurance 1; Iron Head 1; Superpower 1; Poison Gas 1; Sand Tomb 5; Roar 14,41; Pursuit 19; Bulldoze 23; Take Down 34.
- Removed against today's: Bite 1; Leer 1; Sandstorm 1,5; Screech 1,10; Scary Face 19; Thrash 23; Dark Pulse 28; Crunch 41.
- Moved against today's: Hyper Beam 60 to 10; Rock Slide 14 to 28; Payback 34 to 60.
- Against Kaizo's: the same.

**Tyranitar (248)**, 18 moves:

- New list: Thunder Fang 1, Ice Fang 1, Fire Fang 1, Bite 1, Earth Power 1, Assurance 1, Hyper Beam 1, Superpower 5, Pursuit 10, Roar 14, Take Down 19, Bulldoze 23, Rock Slide 28, Payback 34, Roar 41, Earthquake 60, Stone Edge 70, Crunch 70.
- Added against today's: Earth Power 1; Assurance 1; Superpower 5; Pursuit 10; Roar 14,41; Take Down 19; Bulldoze 23.
- Removed against today's: Leer 1; Sandstorm 1,5; Screech 1,10; Scary Face 19; Thrash 23; Dark Pulse 28.
- Moved against today's: Hyper Beam 70 to 1; Rock Slide 14 to 28; Earthquake 47 to 60; Stone Edge 54 to 70; Crunch 41 to 70.
- Against Kaizo's: the same.

**Treecko (252)**, 13 moves:

- New list: Pound 1, Mega Drain 1, Seismic Toss 6, Bite 11, Razor Leaf 17, Swift 21, Crunch 26, Secret Power 31, Magical Leaf 36, DragonBreath 41, Rock Slide 46, ThunderPunch 51, Leaf Blade 54.
- Added against today's: Seismic Toss 6; Bite 11; Razor Leaf 17; Swift 21; Crunch 26; Secret Power 31; Magical Leaf 36; DragonBreath 41; Rock Slide 46; ThunderPunch 51; Leaf Blade 54.
- Removed against today's: Leer 1; Absorb 6; Quick Attack 11; Pursuit 16; Screech 21; Agility 31; Slam 36; Detect 41; Giga Drain 46; Energy Ball 51.
- Moved against today's: Mega Drain 26 to 1.
- Against Kaizo's: the same.

**Grovyle (253)**, 15 moves:

- New list: Camouflage 1, Pound 1, Razor Leaf 1, Pursuit 1, Swift 6, Bite 11, Razor Leaf 19, Dig 23, False Swipe 27, Crunch 31, Magical Leaf 39, X-Scissor 41, Secret Power 44, ThunderPunch 53, Leaf Blade 60.
- Added against today's: Camouflage 1; Razor Leaf 1,19; Swift 6; Bite 11; Dig 23; Crunch 31; Magical Leaf 39; X-Scissor 41; Secret Power 44; ThunderPunch 53.
- Removed against today's: Leer 1; Absorb 1,6; Quick Attack 1,11; Fury Cutter 16; Screech 23; Agility 35; Slam 41; Detect 47; Leaf Storm 59.
- Moved against today's: Pursuit 17 to 1; False Swipe 53 to 27; Leaf Blade 29 to 60.
- Against Kaizo's: the same.

**Sceptile (254)**, 16 moves:

- New list: Crunch 1, Seed Bomb 1, False Swipe 1, Magical Leaf 1, Pursuit 1, Brick Break 6, Camouflage 11, Razor Leaf 16, Night Slash 17, X-Scissor 23, DragonBreath 29, Magical Leaf 41, Secret Power 47, Nature Power 53, Dragon Claw 60, Leaf Blade 70.
- Added against today's: Crunch 1; Seed Bomb 1; Magical Leaf 1,41; Brick Break 6; Camouflage 11; Razor Leaf 16; DragonBreath 29; Secret Power 47; Nature Power 53; Dragon Claw 60.
- Removed against today's: Pound 1; Leer 1; Absorb 1,6; Quick Attack 1,11; Screech 23; Agility 35; Slam 43; Detect 51; Leaf Storm 67.
- Moved against today's: False Swipe 59 to 1; Pursuit 17 to 1; Night Slash 1 to 17; X-Scissor 16 to 23; Leaf Blade 29 to 70.
- Against Kaizo's: the same.

**Torchic (255)**, 11 moves:

- New list: Scratch 1, Peck 1, Ember 7, Double Kick 10, Swift 16, Aerial Ace 17, Flame Wheel 21, Dig 28, Flamethrower 34, Mirror Move 37, Fire Blast 43.
- Added against today's: Double Kick 10; Swift 16; Aerial Ace 17; Flame Wheel 21; Dig 28; Fire Blast 43.
- Removed against today's: Growl 1; Focus Energy 7; Sand-Attack 19; Fire Spin 25; Quick Attack 28; Slash 34.
- Moved against today's: Peck 16 to 1; Ember 10 to 7; Flamethrower 43 to 34.
- Against Kaizo's: the same.

**Combusken (256)**, 16 moves:

- New list: Triple Kick 1, Hyper Voice 1, Metal Claw 1, Fire Punch 1, Swift 7, Night Slash 13, Double Kick 16, Aerial Ace 19, Flame Wheel 23, Rolling Kick 28, Slash 32, ThunderPunch 39, Flamethrower 43, Jump Kick 50, Blaze Kick 54, Brave Bird 70.
- Added against today's: Triple Kick 1; Hyper Voice 1; Metal Claw 1; Fire Punch 1; Swift 7; Night Slash 13; Aerial Ace 19; Flame Wheel 23; Rolling Kick 28; ThunderPunch 39; Flamethrower 43; Jump Kick 50; Blaze Kick 54; Brave Bird 70.
- Removed against today's: Scratch 1; Growl 1; Focus Energy 1,7; Ember 1,13; Peck 17; Sand-Attack 21; Bulk Up 28; Quick Attack 32; Mirror Move 43; Sky Uppercut 50; Flare Blitz 54.
- Moved against today's: Slash 39 to 32.
- Against Kaizo's: the same.

**Blaziken (257)**, 17 moves:

- New list: Sky Uppercut 1, Dig 1, Flamethrower 1, Fire Punch 1, Fire Spin 1, Mega Kick 7, Metal Claw 13, Double Kick 16, Flame Wheel 17, Poison Jab 21, Night Slash 28, Slash 32, Flamethrower 50, Roar 55, ThunderPunch 58, Aura Sphere 60, Blaze Kick 66.
- Added against today's: Dig 1; Flamethrower 1,50; Fire Spin 1; Mega Kick 7; Metal Claw 13; Flame Wheel 17; Poison Jab 21; Night Slash 28; Roar 55; ThunderPunch 58; Aura Sphere 60.
- Removed against today's: Scratch 1; Growl 1; Focus Energy 1,7; Ember 1,13; Peck 17; Sand-Attack 21; Bulk Up 28; Quick Attack 32; Brave Bird 49; Flare Blitz 66.
- Moved against today's: Sky Uppercut 59 to 1; Slash 42 to 32; Blaze Kick 36 to 66.
- Against Kaizo's: the same.

**Mudkip (258)**, 12 moves:

- New list: Tackle 1, Water Gun 1, Mud-Slap 6, Rock Throw 10, Rock Smash 15, BubbleBeam 19, Mud Bomb 24, Rock Slide 28, Brick Break 33, Hydro Pump 37, Superpower 42, Aqua Tail 46.
- Added against today's: Rock Throw 10; Rock Smash 15; BubbleBeam 19; Mud Bomb 24; Rock Slide 28; Brick Break 33; Superpower 42; Aqua Tail 46.
- Removed against today's: Growl 1; Bide 15; Foresight 19; Mud Sport 24; Take Down 28; Whirlpool 33; Protect 37; Endeavor 46.
- Moved against today's: Water Gun 10 to 1; Hydro Pump 42 to 37.
- Against Kaizo's: the same.

**Marshtomp (259)**, 15 moves:

- New list: Tackle 1, Water Gun 1, Mud-Slap 1, Endeavor 1, Rock Throw 6, BubbleBeam 10, Dig 15, Take Down 16, Mud Bomb 20, Muddy Water 25, Earth Power 31, Secret Power 37, Ice Beam 48, Earthquake 50, Aqua Tail 56.
- Added against today's: Rock Throw 6; BubbleBeam 10; Dig 15; Earth Power 31; Secret Power 37; Ice Beam 48; Aqua Tail 56.
- Removed against today's: Growl 1; Bide 15; Mud Shot 16; Foresight 20; Protect 42.
- Moved against today's: Water Gun 1,10 to 1; Mud-Slap 1,6 to 1; Endeavor 53 to 1; Take Down 31 to 16; Mud Bomb 25 to 20; Muddy Water 37 to 25; Earthquake 46 to 50.
- Against Kaizo's: the same.

**Swampert (260)**, 16 moves:

- New list: Superpower 1, Mud-Slap 1, Mud Shot 1, Water Gun 1, Body Slam 6, Mud Bomb 10, Hammer Arm 15, BubbleBeam 16, AncientPower 20, Earth Power 25, Ice Beam 31, Muddy Water 39, Stone Edge 60, Earthquake 68, Ice Punch 72, Aqua Tail 77.
- Added against today's: Superpower 1; Body Slam 6; BubbleBeam 16; AncientPower 20; Earth Power 25; Ice Beam 31; Stone Edge 60; Ice Punch 72; Aqua Tail 77.
- Removed against today's: Tackle 1; Growl 1; Bide 15; Foresight 20; Take Down 31; Protect 46; Endeavor 61.
- Moved against today's: Mud-Slap 1,6 to 1; Mud Shot 16 to 1; Water Gun 1,10 to 1; Mud Bomb 25 to 10; Hammer Arm 69 to 15; Earthquake 52 to 68.
- Against Kaizo's: the same.

**Poochyena (261)**, 14 moves:

- New list: Quick Attack 1, Tackle 5, Sand-Attack 9, Bite 13, Yawn 17, Odor Sleuth 21, Body Slam 25, Assurance 29, Poison Fang 33, Crunch 37, Fire Fang 41, Super Fang 49, Pursuit 53, Sucker Punch 55.
- Added against today's: Quick Attack 1; Yawn 17; Body Slam 25; Poison Fang 33; Fire Fang 41; Super Fang 49; Pursuit 53.
- Removed against today's: Howl 5; Roar 21; Swagger 25; Scary Face 33; Taunt 37; Embargo 41; Take Down 45.
- Moved against today's: Tackle 1 to 5; Odor Sleuth 17 to 21; Crunch 31 to 37; Sucker Punch 49 to 55.
- Rule: Beat Up 45 out: Beat Up leaves the game.

**Mightyena (262)**, 18 moves:

- New list: Quick Attack 1, Pursuit 1, Sand-Attack 1, Body Slam 1, Poison Fang 5, Yawn 9, Bite 13, Odor Sleuth 17, Assurance 22, Thunder Fang 27, Poison Fang 37, Crunch 49, Roar 50, Fire Fang 52, Pursuit 57, Super Fang 62, Sucker Punch 66, Roar 70.
- Added against today's: Quick Attack 1; Pursuit 1,57; Body Slam 1; Poison Fang 5,37; Yawn 9; Thunder Fang 27; Fire Fang 52; Super Fang 62.
- Removed against today's: Tackle 1; Howl 1,5; Swagger 27; Scary Face 37; Taunt 42; Embargo 47; Take Down 52; Thief 57.
- Moved against today's: Sand-Attack 1,9 to 1; Bite 1,13 to 13; Assurance 32 to 22; Crunch 34 to 49; Roar 22 to 50,70; Sucker Punch 62 to 66.
- Rule: Beat Up 42 out: Beat Up leaves the game.

**Wurmple (265)**, 4 moves:

- New list: Poison Sting 1, String Shot 1, Bug Bite 3, Tackle 5.
- Moved against today's: Poison Sting 5 to 1; Bug Bite 15 to 3; Tackle 1 to 5.
- Against Kaizo's: the same.

**Silcoon (266)**, 2 moves:

- New list: Bug Bite 1, Iron Defense 7.
- Added against today's: Bug Bite 1; Iron Defense 7.
- Removed against today's: Harden 1,7.
- Against Kaizo's: the same.

**Beautifly (267)**, 11 moves:

- New list: Leech Life 1, Mega Drain 10, Gust 11, Stun Spore 13, Morning Sun 17, Silver Wind 20, Aerial Ace 21, Attract 23, Giga Drain 24, Bug Buzz 28, Air Slash 29.
- Added against today's: Leech Life 1; Aerial Ace 21.
- Removed against today's: Absorb 1,10; Whirlwind 27.
- Moved against today's: Mega Drain 24 to 10; Gust 13 to 11; Stun Spore 17 to 13; Morning Sun 20 to 17; Silver Wind 34 to 20; Attract 31 to 23; Giga Drain 38 to 24; Bug Buzz 41 to 28; Air Slash 26 to 29.
- Against Kaizo's: the same.

**Cascoon (268)**, 2 moves:

- New list: Bug Bite 1, Iron Defense 7.
- Added against today's: Bug Bite 1; Iron Defense 7.
- Removed against today's: Harden 1,7.
- Against Kaizo's: the same.

**Dustox (269)**, 11 moves:

- New list: Bug Bite 1, Psybeam 10, Moonlight 12, PoisonPowder 15, Silver Wind 17, Sludge Bomb 20, Whirlwind 23, Toxic 25, Bug Buzz 27, Poison Fang 30, Light Screen 34.
- Added against today's: Bug Bite 1; PoisonPowder 15; Sludge Bomb 20; Poison Fang 30.
- Removed against today's: Confusion 1,10; Gust 13; Protect 17.
- Moved against today's: Psybeam 24 to 10; Moonlight 20 to 12; Silver Wind 34 to 17; Whirlwind 27 to 23; Toxic 38 to 25; Bug Buzz 41 to 27; Light Screen 31 to 34.
- Against Kaizo's: the same.

**Lotad (270)**, 11 moves:

- New list: Bubble 1, Tackle 3, Astonish 5, Razor Leaf 7, Water Gun 11, Nature Power 19, Magical Leaf 25, BubbleBeam 31, Zen Headbutt 37, Teeter Dance 45, Energy Ball 50.
- Added against today's: Bubble 1; Tackle 3; Razor Leaf 7; Water Gun 11; Magical Leaf 25; Teeter Dance 45.
- Removed against today's: Growl 3; Absorb 5; Mist 11; Natural Gift 15; Mega Drain 19; Rain Dance 37.
- Moved against today's: Astonish 1 to 5; Nature Power 7 to 19; BubbleBeam 25 to 31; Zen Headbutt 31 to 37; Energy Ball 45 to 50.
- Against Kaizo's: Kaizo's Absorb 13 left out: Oxide has no move like it.

**Lombre (271)**, 12 moves:

- New list: Uproar 1, Tackle 3, Astonish 5, Razor Leaf 7, Water Gun 11, Nature Power 21, Magical Leaf 28, BubbleBeam 35, Zen Headbutt 41, Ice Punch 45, Energy Ball 55, Hydro Pump 60.
- Added against today's: Tackle 3; Razor Leaf 7; Water Gun 11; Magical Leaf 28; Ice Punch 45; Energy Ball 55.
- Removed against today's: Growl 3; Absorb 5; Fake Out 11; Fury Swipes 15; Water Sport 19.
- Moved against today's: Uproar 37 to 1; Astonish 1 to 5; Nature Power 7 to 21; BubbleBeam 25 to 35; Zen Headbutt 31 to 41; Hydro Pump 45 to 60.
- Against Kaizo's: Kaizo's Absorb 15 left out: Oxide has no move like it.

**Ludicolo (272)**, 4 moves:

- New list: Fire Punch 1, ThunderPunch 1, Energy Ball 1, Ice Punch 1.
- Added against today's: Fire Punch 1; ThunderPunch 1; Energy Ball 1; Ice Punch 1.
- Removed against today's: Astonish 1; Growl 1; Mega Drain 1; Nature Power 1.
- Against Kaizo's: the same.

**Seedot (273)**, 6 moves:

- New list: Mega Drain 1, Leech Life 3, Selfdestruct 13, Giga Drain 21, Seed Bomb 31, Explosion 43.
- Added against today's: Mega Drain 1; Leech Life 3; Selfdestruct 13; Giga Drain 21; Seed Bomb 31.
- Removed against today's: Bide 1; Harden 3; Growth 7; Nature Power 13; Synthesis 21; Sunny Day 31.
- Against Kaizo's: Kaizo's Absorb 7 left out: Oxide has no move like it.

**Nuzleaf (274)**, 11 moves:

- New list: Fake Out 1, Nature Power 1, Silver Wind 3, Rock Slide 7, Faint Attack 13, Razor Leaf 19, Extrasensory 25, Explosion 31, Night Slash 37, Leaf Blade 43, GrassWhistle 49.
- Added against today's: Silver Wind 3; Rock Slide 7; Explosion 31; Night Slash 37; Leaf Blade 43; GrassWhistle 49.
- Removed against today's: Pound 1; Harden 3; Growth 7; Torment 25; Razor Wind 37; Swagger 43.
- Moved against today's: Fake Out 19 to 1; Nature Power 13 to 1; Faint Attack 31 to 13; Razor Leaf 1 to 19; Extrasensory 49 to 25.
- Against Kaizo's: the same.

**Shiftry (275)**, 5 moves:

- New list: Crunch 1, Whirlwind 1, Explosion 1, Heat Wave 1, Leaf Blade 55.
- Added against today's: Crunch 1; Explosion 1; Heat Wave 1; Leaf Blade 55.
- Removed against today's: Faint Attack 1; Nasty Plot 1; Razor Leaf 1; Leaf Storm 49.
- Against Kaizo's: the same.

**Wingull (278)**, 12 moves:

- New list: Peck 1, Water Gun 1, Supersonic 6, Bite 11, Wing Attack 16, Water Pulse 19, Pursuit 24, Pluck 29, Ice Beam 34, Brine 37, Air Slash 42, Hydro Pump 47.
- Added against today's: Peck 1; Bite 11; Pluck 29; Ice Beam 34; Brine 37; Hydro Pump 47.
- Removed against today's: Growl 1; Mist 16; Quick Attack 24; Roost 29; Agility 37; Aerial Ace 42.
- Moved against today's: Wing Attack 11 to 16; Pursuit 34 to 24; Air Slash 47 to 42.
- Against Kaizo's: the same.

**Pelipper (279)**, 18 moves:

- New list: Fling 1, Headbutt 1, Swift 1, Supersonic 1, Water Gun 6, Wing Attack 11, Bite 16, Pursuit 19, BubbleBeam 24, Pluck 25, Payback 31, Ice Beam 34, Brine 37, Air Slash 38, Poison Jab 53, Roost 55, Hydro Pump 60, Whirlwind 61.
- Added against today's: Headbutt 1; Swift 1; Bite 16; Pursuit 19; BubbleBeam 24; Pluck 25; Ice Beam 34; Brine 37; Air Slash 38; Poison Jab 53; Whirlwind 61.
- Removed against today's: Growl 1; Water Sport 1; Mist 16; Water Pulse 19; Protect 25; Stockpile 38; Swallow 38; Spit Up 38; Tailwind 50.
- Moved against today's: Fling 43 to 1; Supersonic 6 to 1; Water Gun 1 to 6; Wing Attack 1,11 to 11; Payback 24 to 31; Roost 31 to 55; Hydro Pump 57 to 60.
- Against Kaizo's: Kaizo's Swallow 53 became Poison Jab.

**Ralts (280)**, 11 moves:

- New list: Confusion 1, Magical Leaf 10, Psybeam 17, Future Sight 21, Lucky Chant 23, Fire Punch 28, Zen Headbutt 32, Thunderbolt 34, Psychic 39, Hypnosis 43, Mystical Fire 47.
- Added against today's: Psybeam 17; Fire Punch 28; Zen Headbutt 32; Thunderbolt 34; Mystical Fire 47.
- Removed against today's: Growl 1; Double Team 10; Teleport 12; Calm Mind 23; Imprison 32; Charm 39; Dream Eater 45.
- Moved against today's: Confusion 6 to 1; Magical Leaf 21 to 10; Future Sight 34 to 21; Lucky Chant 17 to 23; Psychic 28 to 39.
- Against Kaizo's: Kaizo's Heart Swap 45 left out: Oxide has no move like it.

**Kirlia (281)**, 13 moves:

- New list: Petal Dance 1, Blaze Kick 1, Triple Axel 1, Confusion 6, Future Sight 19, Magical Leaf 20, Lucky Chant 25, Zen Headbutt 28, Seismic Toss 31, Thunderbolt 36, Psychic 45, Hypnosis 50, Mystical Fire 55.
- Added against today's: Petal Dance 1; Blaze Kick 1; Triple Axel 1; Zen Headbutt 28; Seismic Toss 31; Thunderbolt 36; Mystical Fire 55.
- Removed against today's: Growl 1; Double Team 1,10; Teleport 1,12; Calm Mind 25; Imprison 36; Charm 45; Dream Eater 53.
- Moved against today's: Confusion 1,6 to 6; Future Sight 39 to 19; Magical Leaf 22 to 20; Lucky Chant 17 to 25; Psychic 31 to 45.
- Against Kaizo's: Kaizo's Heart Swap 53 left out: Oxide has no move like it.
- Rule: Teleport 39 out: Splash and Teleport go.

**Gardevoir (282)**, 14 moves:

- New list: Shadow Ball 1, Tri Attack 1, Signal Beam 1, Psybeam 1, Hyper Voice 1, Triple Axel 6, Mystical Fire 10, Extrasensory 12, Magical Leaf 22, Thunderbolt 25, Gravity 33, Psychic 48, Aura Sphere 70, Spacial Rend 75.
- Added against today's: Shadow Ball 1; Tri Attack 1; Signal Beam 1; Psybeam 1; Hyper Voice 1; Triple Axel 6; Mystical Fire 10; Extrasensory 12; Thunderbolt 25; Gravity 33; Aura Sphere 70; Spacial Rend 75.
- Removed against today's: Healing Wish 1; Growl 1; Confusion 1,6; Double Team 1,10; Teleport 1,12; Wish 17; Calm Mind 25; Imprison 40; Future Sight 45; Captivate 53; Hypnosis 60; Dream Eater 65.
- Moved against today's: Psychic 33 to 48.
- Against Kaizo's: Kaizo's Heart Swap 63 left out: Oxide has no move like it.

**Surskit (283)**, 9 moves:

- New list: Bubble 1, Quick Attack 7, Sweet Scent 13, Signal Beam 19, BubbleBeam 25, Bug Buzz 31, Mud Bomb 37, Stun Spore 37, Hydro Pump 43.
- Added against today's: Signal Beam 19; Bug Buzz 31; Mud Bomb 37; Stun Spore 37; Hydro Pump 43.
- Removed against today's: Water Sport 19; Agility 31; Mist 37; Haze 37; Baton Pass 43.
- Against Kaizo's: the same.

**Masquerain (284)**, 15 moves:

- New list: Ominous Wind 1, Mud Bomb 1, Quick Attack 1, Sweet Scent 1, Silver Wind 1, Water Pulse 7, Sweet Scent 13, Signal Beam 19, Air Cutter 22, Giga Drain 26, Stun Spore 33, Bug Buzz 40, Air Slash 47, Ice Beam 54, Hydro Pump 61.
- Added against today's: Mud Bomb 1; Water Pulse 7; Signal Beam 19; Air Cutter 22; Giga Drain 26; Ice Beam 54; Hydro Pump 61.
- Removed against today's: Bubble 1; Water Sport 1,19; Gust 22; Scary Face 26; Whirlwind 54.
- Moved against today's: Quick Attack 1,7 to 1; Silver Wind 40 to 1; Bug Buzz 61 to 40.
- Against Kaizo's: the same.

**Shroomish (285)**, 12 moves:

- New list: PoisonPowder 1, Mega Drain 5, Take Down 9, Stun Spore 13, Headbutt 17, Mega Drain 21, Take Down 25, Sleep Powder 49, Sludge Bomb 53, Double-Edge 57, Seed Bomb 61, Spore 100.
- Added against today's: Take Down 9,25; Sleep Powder 49; Sludge Bomb 53; Double-Edge 57.
- Removed against today's: Absorb 1; Tackle 5; Leech Seed 13; Worry Seed 29; Growth 33; Giga Drain 37.
- Moved against today's: PoisonPowder 25 to 1; Mega Drain 17 to 5,21; Stun Spore 9 to 13; Headbutt 21 to 17; Seed Bomb 41 to 61; Spore 45 to 100.
- Against Kaizo's: the same.

**Breloom (286)**, 16 moves:

- New list: Sky Uppercut 1, Tackle 1, Revenge 1, Iron Tail 1, Headbutt 5, Take Down 9, Mega Drain 13, Take Down 17, Sludge Bomb 21, Force Palm 23, Take Down 29, Giga Drain 30, Submission 60, Stun Spore 67, Seed Bomb 71, Mach Punch 100.
- Added against today's: Revenge 1; Iron Tail 1; Take Down 9,17,29; Sludge Bomb 21; Giga Drain 30; Submission 60.
- Removed against today's: Absorb 1; Leech Seed 1,13; Counter 25; Mind Reader 37; DynamicPunch 45.
- Moved against today's: Sky Uppercut 33 to 1; Tackle 1,5 to 1; Headbutt 21 to 5; Mega Drain 17 to 13; Force Palm 29 to 23; Stun Spore 1,9 to 67; Seed Bomb 41 to 71; Mach Punch 23 to 100.
- Against Kaizo's: the same.

**Makuhita (296)**, 16 moves:

- New list: Karate Chop 1, Pound 1, Sand-Attack 4, Whirlwind 7, Vital Throw 10, Take Down 13, Seismic Toss 16, Whirlwind 19, Submission 22, SmellingSalt 25, Force Palm 28, Body Slam 31, Whirlwind 34, Close Combat 52, Shadow Punch 55, Fake Out 70.
- Added against today's: Karate Chop 1; Pound 1; Take Down 13; Submission 22; Body Slam 31; Shadow Punch 55.
- Removed against today's: Tackle 1; Focus Energy 1; Arm Thrust 7; Knock Off 19; Belly Drum 25; Wake-Up Slap 34; Endure 37; Reversal 43.
- Moved against today's: Whirlwind 16 to 7,19,34; Seismic Toss 31 to 16; SmellingSalt 22 to 25; Close Combat 40 to 52; Fake Out 13 to 70.
- Against Kaizo's: the same.

**Hariyama (297)**, 19 moves:

- New list: Brine 1, Mega Punch 1, Cross Chop 1, Payback 1, Ice Punch 1, Fire Punch 4, Seismic Toss 7, Vital Throw 10, ThunderPunch 13, Body Slam 16, Whirlwind 19, SmellingSalt 22, Submission 27, Force Palm 32, Body Slam 37, Whirlwind 42, Shadow Punch 47, Close Combat 90, Fake Out 99.
- Added against today's: Mega Punch 1; Cross Chop 1; Payback 1; Ice Punch 1; Fire Punch 4; ThunderPunch 13; Body Slam 16,37; Submission 27; Shadow Punch 47.
- Removed against today's: Tackle 1; Focus Energy 1; Sand-Attack 1,4; Arm Thrust 1,7; Knock Off 19; Belly Drum 27; Wake-Up Slap 42; Endure 47; Reversal 57.
- Moved against today's: Seismic Toss 37 to 7; Whirlwind 16 to 19,42; Close Combat 52 to 90; Fake Out 13 to 99.
- Against Kaizo's: the same.

**Azurill (298)**, 6 moves:

- New list: Present 1, Water Gun 2, Pound 7, BubbleBeam 10, Slam 25, Bounce 28.
- Added against today's: Present 1; Pound 7; BubbleBeam 10; Bounce 28.
- Removed against today's: Splash 1; Charm 2; Tail Whip 7; Bubble 10.
- Moved against today's: Water Gun 18 to 2; Slam 15 to 25.
- Against Kaizo's: the same.
- Rule: Pound pick not applied: Kaizo's list has no Splash or Teleport and already starts with Present.

**Nosepass (299)**, 14 moves:

- New list: Headbutt 1, Rock Slide 7, Seismic Toss 13, Iron Head 19, Power Gem 25, Discharge 31, Selfdestruct 37, Earth Power 43, AncientPower 49, Thunder Wave 55, Explosion 61, Earthquake 67, Head Smash 73, Metal Burst 79.
- Added against today's: Headbutt 1; Seismic Toss 13; Iron Head 19; Selfdestruct 37; AncientPower 49; Explosion 61; Earthquake 67; Head Smash 73; Metal Burst 79.
- Removed against today's: Tackle 1; Harden 7; Rock Throw 13; Block 19; Sandstorm 37; Rest 43; Stone Edge 61; Zap Cannon 67; Lock-On 73.
- Moved against today's: Rock Slide 31 to 7; Power Gem 49 to 25; Discharge 55 to 31; Earth Power 79 to 43; Thunder Wave 25 to 55.
- Against Kaizo's: the same.

**Skitty (300)**, 18 moves:

- New list: Growl 1, Quick Attack 1, Present 1, Fake Out 1, Foresight 6, Attract 8, Sing 11, DoubleSlap 15, Copycat 18, Assist 22, Hyper Voice 25, Faint Attack 29, Charm 32, Wake-Up Slap 36, Heal Bell 39, Double Hit 42, Tail Whip 45, Captivate 46.
- Added against today's: Quick Attack 1; Present 1; Hyper Voice 25; Double Hit 42.
- Removed against today's: Tackle 1; Covet 36; Double-Edge 42.
- Moved against today's: Foresight 4 to 6; Charm 25 to 32; Wake-Up Slap 32 to 36; Tail Whip 1 to 45.
- Against Kaizo's: the same.

**Delcatty (301)**, 4 moves:

- New list: Fake Out 1, Assist 1, Sing 1, Copycat 1.
- Added against today's: Assist 1; Copycat 1.
- Removed against today's: Attract 1; DoubleSlap 1; Hyper Voice 35.
- Against Kaizo's: the same.

**Mawile (303)**, 14 moves:

- New list: Bite 1, False Swipe 6, Metal Claw 11, Sweet Scent 16, Fire Fang 21, Poison Fang 26, Iron Head 31, Super Fang 36, Crunch 41, Thunder Fang 46, Meteor Mash 51, Poison Jab 51, Ice Fang 51, Liquidation 56.
- Added against today's: False Swipe 6; Metal Claw 11; Fire Fang 21; Poison Fang 26; Super Fang 36; Thunder Fang 46; Meteor Mash 51; Poison Jab 51; Ice Fang 51; Liquidation 56.
- Removed against today's: Astonish 1; Fake Tears 6; ViceGrip 21; Faint Attack 26; Baton Pass 31; Iron Defense 41; Sucker Punch 46; Stockpile 51; Swallow 51; Spit Up 51.
- Moved against today's: Bite 11 to 1; Iron Head 56 to 31; Crunch 36 to 41.
- Against Kaizo's: Kaizo's Swallow 51 became Poison Jab.
- Against Kaizo's: Kaizo's ViceGrip 56 became Liquidation.

**Meditite (307)**, 11 moves:

- New list: Karate Chop 1, Confusion 8, Hidden Power 11, Secret Power 15, Rock Throw 22, Seismic Toss 25, Psybeam 29, Poison Jab 32, Zen Headbutt 49, Force Palm 54, Meditate 100.
- Added against today's: Karate Chop 1; Secret Power 15; Rock Throw 22; Seismic Toss 25; Psybeam 29; Poison Jab 32; Zen Headbutt 49.
- Removed against today's: Bide 1; Detect 11; Mind Reader 18; Feint 22; Calm Mind 25; Hi Jump Kick 32; Psych Up 36; Power Trick 39; Reversal 43; Recover 46.
- Moved against today's: Hidden Power 15 to 11; Force Palm 29 to 54; Meditate 4 to 100.
- Rule: Teleport 1 out: Splash and Teleport go.
- Rule: Teleport 18 out: Splash and Teleport go.
- Rule: Teleport 36 out: Splash and Teleport go.
- Rule: Karate Chop moved from 4 to 1: Teleport or Splash was the only level-1 move (a pick for the balance track to confirm).

**Medicham (308)**, 18 moves:

- New list: Brick Break 1, Poison Jab 1, ThunderPunch 1, Ice Punch 1, Seismic Toss 1, Body Slam 1, Hidden Power 1, Karate Chop 4, Psychic 8, Secret Power 11, Iron Head 15, Fire Punch 22, Ice Punch 25, Force Palm 29, Psychic 32, Recover 42, Jump Kick 70, Psycho Cut 77.
- Added against today's: Brick Break 1; Poison Jab 1; Seismic Toss 1; Body Slam 1; Karate Chop 4; Psychic 8,32; Secret Power 11; Iron Head 15; Jump Kick 70; Psycho Cut 77.
- Removed against today's: Bide 1; Meditate 1,4; Confusion 1,8; Detect 1,11; Mind Reader 18; Feint 22; Calm Mind 25; Hi Jump Kick 32; Psych Up 36; Power Trick 42; Reversal 49.
- Moved against today's: Ice Punch 1 to 1,25; Hidden Power 15 to 1; Fire Punch 1 to 22; Recover 55 to 42.
- Rule: Teleport 18 out: Splash and Teleport go.
- Rule: Teleport 36 out: Splash and Teleport go.

**Plusle (311)**, 16 moves:

- New list: ThunderShock 1, Thunder Wave 3, Quick Attack 7, Helping Hand 10, ThunderPunch 15, Fire Punch 17, Swift 21, Copycat 24, Wild Charge 29, Ice Punch 31, Charge 35, Hyper Voice 38, Discharge 42, Grass Knot 44, Thunderbolt 48, Fake Tears 51.
- Added against today's: ThunderShock 1; ThunderPunch 15; Fire Punch 17; Wild Charge 29; Ice Punch 31; Hyper Voice 38; Discharge 42; Grass Knot 44; Thunderbolt 48.
- Removed against today's: Growl 1; Spark 15; Encore 17; Thunder 38; Baton Pass 42; Agility 44; Last Resort 48; Nasty Plot 51.
- Moved against today's: Swift 29 to 21; Fake Tears 21,31 to 51.
- Against Kaizo's: the same.

**Minun (312)**, 16 moves:

- New list: ThunderShock 1, Thunder Wave 3, Quick Attack 7, Helping Hand 10, ThunderPunch 15, Fire Punch 17, Swift 21, Copycat 24, Wild Charge 29, Ice Punch 31, Charge 35, Hyper Voice 38, Discharge 42, Grass Knot 44, Thunderbolt 48, Charm 51.
- Added against today's: ThunderShock 1; ThunderPunch 15; Fire Punch 17; Wild Charge 29; Ice Punch 31; Hyper Voice 38; Discharge 42; Grass Knot 44; Thunderbolt 48.
- Removed against today's: Growl 1; Spark 15; Encore 17; Fake Tears 31; Thunder 38; Baton Pass 42; Agility 44; Trump Card 48; Nasty Plot 51.
- Moved against today's: Swift 29 to 21; Charm 21 to 51.
- Against Kaizo's: the same.

**Roselia (315)**, 16 moves:

- New list: Mega Drain 1, Poison Sting 4, Twineedle 7, Stun Spore 10, Mega Drain 16, DoubleSlap 19, Pin Missile 22, Toxic 25, Magical Leaf 28, Poison Jab 31, Needle Arm 33, Aromatherapy 65, GrassWhistle 70, Sludge Bomb 77, Extrasensory 85, Petal Dance 90.
- Added against today's: Twineedle 7; DoubleSlap 19; Pin Missile 22; Poison Jab 31; Needle Arm 33; Sludge Bomb 77; Extrasensory 85.
- Removed against today's: Absorb 1; Growth 4; Leech Seed 16; Giga Drain 25; Toxic Spikes 28; Sweet Scent 31; Ingrain 34; Synthesis 46.
- Moved against today's: Mega Drain 13 to 1,16; Poison Sting 7 to 4; Toxic 37 to 25; Magical Leaf 19 to 28; Aromatherapy 43 to 65; GrassWhistle 22 to 70; Petal Dance 40 to 90.
- Against Kaizo's: the same.

**Carvanha (318)**, 16 moves:

- New list: Water Gun 1, Bite 1, Brick Break 6, Bug Bite 8, Hyper Fang 11, Faint Attack 16, Aqua Cutter 18, Water Pulse 21, Payback 26, Dark Pulse 28, Poison Fang 38, Dive 44, Pursuit 50, Crunch 55, Ice Fang 60, Liquidation 66.
- Added against today's: Water Gun 1; Brick Break 6; Bug Bite 8; Hyper Fang 11; Faint Attack 16; Aqua Cutter 18; Water Pulse 21; Payback 26; Dark Pulse 28; Poison Fang 38; Dive 44; Pursuit 50; Liquidation 66.
- Removed against today's: Leer 1; Rage 6; Focus Energy 8; Scary Face 11; Screech 18; Swagger 21; Assurance 26; Aqua Jet 31; Agility 36; Take Down 38.
- Moved against today's: Crunch 28 to 55; Ice Fang 16 to 60.
- Against Kaizo's: Kaizo's Rage 6 became Brick Break.
- Against Kaizo's: Kaizo's ViceGrip 66 became Liquidation.

**Sharpedo (319)**, 19 moves:

- New list: Feint 1, Whirlpool 1, Bite 1, Brick Break 1, Night Slash 1, Aqua Tail 6, Thrash 8, Aerial Ace 11, Ice Fang 16, Fire Fang 18, Thunder Fang 21, Assurance 26, Aqua Cutter 28, Hyper Fang 30, Water Pulse 34, Pursuit 43, Crunch 45, Super Fang 66, Aqua Jet 96.
- Added against today's: Whirlpool 1; Brick Break 1; Aqua Tail 6; Thrash 8; Aerial Ace 11; Fire Fang 18; Thunder Fang 21; Aqua Cutter 28; Hyper Fang 30; Water Pulse 34; Pursuit 43; Super Fang 66.
- Removed against today's: Leer 1; Rage 1,6; Focus Energy 1,8; Scary Face 11; Screech 18; Swagger 21; Slash 30; Taunt 40; Agility 45; Skull Bash 50.
- Moved against today's: Night Slash 56 to 1; Crunch 28 to 45; Aqua Jet 34 to 96.
- Against Kaizo's: Kaizo's Rage 1 became Brick Break.

**Wailmer (320)**, 15 moves:

- New list: Water Pulse 1, Astonish 4, Body Slam 7, Whirlpool 11, Ice Ball 14, Brine 17, Hyper Voice 21, Roar 24, Poison Jab 27, Dive 31, Bounce 34, Selfdestruct 37, Roar 41, Hydro Pump 54, Water Spout 100.
- Added against today's: Body Slam 7; Ice Ball 14; Hyper Voice 21; Roar 24,41; Poison Jab 27; Selfdestruct 37.
- Removed against today's: Splash 1; Growl 4; Water Gun 7; Rollout 11; Mist 24; Rest 27; Amnesia 37.
- Moved against today's: Water Pulse 21 to 1; Astonish 17 to 4; Whirlpool 14 to 11; Brine 31 to 17; Dive 41 to 31; Bounce 44 to 34; Hydro Pump 47 to 54; Water Spout 34 to 100.
- Against Kaizo's: Kaizo's Swallow 27 became Poison Jab.
- Rule: Water Gun pick not applied: Kaizo's list has no Splash or Teleport and already starts with Water Pulse.

**Wailord (321)**, 18 moves:

- New list: Water Pulse 1, Body Slam 1, Slam 1, Ice Ball 1, Double-Edge 4, Brine 7, Astonish 11, Whirlpool 14, Astonish 17, Dive 21, Hyper Voice 24, Roar 27, Poison Jab 31, Aqua Tail 34, Bounce 37, Selfdestruct 46, Roar 54, Hydro Pump 67.
- Added against today's: Body Slam 1; Slam 1; Ice Ball 1; Double-Edge 4; Hyper Voice 24; Roar 27,54; Poison Jab 31; Aqua Tail 34; Selfdestruct 46.
- Removed against today's: Splash 1; Growl 1,4; Water Gun 1,7; Rollout 1,11; Mist 24; Rest 27; Water Spout 34; Amnesia 37.
- Moved against today's: Water Pulse 21 to 1; Brine 31 to 7; Astonish 17 to 11,17; Dive 46 to 21; Bounce 54 to 37; Hydro Pump 62 to 67.
- Against Kaizo's: Kaizo's Swallow 31 became Poison Jab.

**Trapinch (328)**, 12 moves:

- New list: Bite 1, Sand-Attack 9, Bug Bite 17, Sand Tomb 25, Crunch 33, Dig 41, Poison Fang 49, Hyper Beam 57, Earthquake 65, Fire Fang 73, Superpower 89, Gastro Acid 100.
- Added against today's: Bug Bite 17; Poison Fang 49; Fire Fang 73; Superpower 89; Gastro Acid 100.
- Removed against today's: Faint Attack 17; Sandstorm 49; Earth Power 65; Feint 81; Fissure 89.
- Moved against today's: Earthquake 73 to 65.
- Against Kaizo's: the same.

**Vibrava (329)**, 12 moves:

- New list: SonicBoom 1, Acid 1, Faint Attack 1, DragonBreath 1, Sand Tomb 9, Twister 17, Sand-Attack 25, Supersonic 33, Bug Buzz 35, Whirlwind 41, Hyper Voice 49, Earthquake 57.
- Added against today's: Acid 1; Twister 17; Bug Buzz 35; Whirlwind 41; Hyper Voice 49; Earthquake 57.
- Removed against today's: Screech 41; Sandstorm 49; Hyper Beam 57.
- Moved against today's: Faint Attack 1,17 to 1; DragonBreath 35 to 1; Sand Tomb 1,25 to 9; Sand-Attack 1,9 to 25.
- Against Kaizo's: the same.

**Flygon (330)**, 13 moves:

- New list: Bug Buzz 1, Sand-Attack 1, Sand Tomb 1, Twister 1, Supersonic 9, Faint Attack 17, Hyper Voice 25, Dragon Claw 33, Earthquake 35, Whirlwind 41, Fire Punch 45, Earth Power 49, Dragon Pulse 57.
- Added against today's: Bug Buzz 1; Twister 1; Hyper Voice 25; Earthquake 35; Whirlwind 41; Fire Punch 45; Earth Power 49; Dragon Pulse 57.
- Removed against today's: SonicBoom 1; DragonBreath 35; Screech 41; Sandstorm 49; Hyper Beam 57.
- Moved against today's: Sand-Attack 1,9 to 1; Sand Tomb 1,25 to 1; Supersonic 33 to 9; Faint Attack 1,17 to 17; Dragon Claw 45 to 33.
- Against Kaizo's: the same.

**Swablu (333)**, 13 moves:

- New list: Sing 1, Pluck 1, Astonish 5, Whirlwind 9, Swift 13, Air Cutter 18, Steel Wing 23, Hyper Voice 28, Sing 32, Mirror Move 36, Refresh 40, Dragon Pulse 45, Air Slash 50.
- Added against today's: Pluck 1; Whirlwind 9; Swift 13; Air Cutter 18; Steel Wing 23; Hyper Voice 28; Air Slash 50.
- Removed against today's: Peck 1; Growl 1; Fury Attack 13; Safeguard 18; Mist 23; Take Down 28; Natural Gift 32; Perish Song 50.
- Moved against today's: Sing 9 to 1,32.
- Against Kaizo's: the same.

**Altaria (334)**, 18 moves:

- New list: Pluck 1, Brave Bird 1, Body Slam 1, Mirror Move 1, Fire Spin 1, Twister 5, Refresh 9, Hyper Voice 13, Safeguard 18, Dragon Rush 23, Fire Blast 28, DragonBreath 35, Sing 35, Air Slash 39, Whirlwind 46, Dragon Pulse 54, Earth Power 62, Sky Attack 70.
- Added against today's: Brave Bird 1; Body Slam 1; Mirror Move 1; Fire Spin 1; Twister 5; Hyper Voice 13; Dragon Rush 23; Fire Blast 28; Air Slash 39; Whirlwind 46; Earth Power 62.
- Removed against today's: Peck 1; Growl 1; Astonish 1,5; Fury Attack 13; Mist 23; Take Down 28; Natural Gift 32; Dragon Dance 39; Perish Song 62.
- Moved against today's: Refresh 46 to 9; Sing 1,9 to 35.
- Against Kaizo's: the same.

**Lunatone (337)**, 12 moves:

- New list: Night Shade 1, Moonlight 1, Dark Pulse 1, Signal Beam 9, AncientPower 20, Hypnosis 23, Earth Power 31, Selfdestruct 34, Power Gem 42, Psychic 45, Aura Sphere 53, Explosion 56.
- Added against today's: Night Shade 1; Moonlight 1; Dark Pulse 1; Signal Beam 9; AncientPower 20; Earth Power 31; Selfdestruct 34; Power Gem 42; Aura Sphere 53.
- Removed against today's: Tackle 1; Harden 1; Confusion 1; Rock Throw 9; Rock Polish 20; Psywave 23; Embargo 31; Cosmic Power 34; Heal Block 42; Future Sight 53.
- Moved against today's: Hypnosis 12 to 23.
- Rule: Teleport 12 out: Splash and Teleport go.

**Solrock (338)**, 12 moves:

- New list: SolarBeam 1, Fire Spin 1, Sand Tomb 1, Flare Blitz 9, Will-O-Wisp 20, Psycho Cut 23, Rock Slide 31, Selfdestruct 34, Zen Headbutt 42, Earthquake 45, Stone Edge 53, Explosion 56.
- Added against today's: Sand Tomb 1; Flare Blitz 9; Will-O-Wisp 20; Psycho Cut 23; Selfdestruct 34; Zen Headbutt 42; Earthquake 45; Stone Edge 53.
- Removed against today's: Tackle 1; Harden 1; Confusion 1; Rock Throw 9; Rock Polish 20; Psywave 23; Embargo 31; Cosmic Power 34; Heal Block 42.
- Moved against today's: SolarBeam 53 to 1; Fire Spin 12 to 1; Rock Slide 45 to 31.
- Rule: Teleport 12 out: Splash and Teleport go.

**Barboach (339)**, 14 moves:

- New list: Mud-Slap 1, Water Gun 6, Tackle 6, Water Pulse 10, Headbutt 14, Mud Bomb 18, Bounce 22, Future Sight 26, Muddy Water 31, Zen Headbutt 31, Rock Slide 41, Earthquake 44, Wild Charge 47, Aqua Tail 51.
- Added against today's: Tackle 6; Headbutt 14; Bounce 22; Muddy Water 31; Zen Headbutt 31; Rock Slide 41; Wild Charge 47.
- Removed against today's: Mud Sport 6; Water Sport 6; Amnesia 18; Magnitude 26; Rest 31; Snore 31; Fissure 47.
- Moved against today's: Water Gun 10 to 6; Water Pulse 22 to 10; Mud Bomb 14 to 18; Future Sight 43 to 26; Earthquake 39 to 44; Aqua Tail 35 to 51.
- Against Kaizo's: the same.

**Whiscash (340)**, 19 moves:

- New list: Zen Headbutt 1, Whirlpool 1, Mud-Slap 1, Headbutt 1, Rock Slide 1, Bounce 6, Body Slam 6, Dive 10, Mud Bomb 14, Poison Jab 18, Muddy Water 22, Dig 26, Body Slam 33, Future Sight 33, Rock Slide 47, Earthquake 55, Wild Charge 65, Stone Edge 70, Aqua Tail 75.
- Added against today's: Whirlpool 1; Headbutt 1; Rock Slide 1,47; Bounce 6; Body Slam 6,33; Dive 10; Poison Jab 18; Muddy Water 22; Dig 26; Wild Charge 65; Stone Edge 70.
- Removed against today's: Tickle 1; Mud Sport 1,6; Water Sport 1,6; Water Gun 10; Amnesia 18; Water Pulse 22; Magnitude 26; Rest 33; Snore 33; Fissure 57.
- Moved against today's: Future Sight 51 to 33; Earthquake 45 to 55; Aqua Tail 39 to 75.
- Against Kaizo's: Kaizo's Swallow 18 became Poison Jab.

**Corphish (341)**, 14 moves:

- New list: Bubble 1, False Swipe 7, BubbleBeam 10, Secret Power 13, Aerial Ace 20, Water Pulse 23, Metal Claw 26, X-Scissor 32, Night Slash 35, Liquidation 38, Crush Claw 44, Ice Punch 47, Crunch 53, Crabhammer 55.
- Added against today's: False Swipe 7; Secret Power 13; Aerial Ace 20; Water Pulse 23; Metal Claw 26; X-Scissor 32; Liquidation 38; Crush Claw 44; Ice Punch 47.
- Removed against today's: Harden 7; ViceGrip 10; Leer 13; Protect 23; Knock Off 26; Taunt 32; Swords Dance 44; Guillotine 53.
- Moved against today's: BubbleBeam 20 to 10; Crunch 47 to 53; Crabhammer 38 to 55.
- Against Kaizo's: Kaizo's ViceGrip 38 became Liquidation.

**Crawdaunt (342)**, 18 moves:

- New list: Endeavor 1, Dark Pulse 1, Double Hit 1, Metal Claw 1, Crush Claw 7, Thrash 10, Aerial Ace 13, Seismic Toss 20, Payback 23, Liquidation 26, X-Scissor 30, Ice Punch 34, Night Slash 39, Liquidation 44, Crush Claw 57, Cross Chop 60, Crunch 65, Crabhammer 75.
- Added against today's: Endeavor 1; Dark Pulse 1; Double Hit 1; Metal Claw 1; Crush Claw 7,57; Thrash 10; Aerial Ace 13; Seismic Toss 20; Payback 23; Liquidation 26,44; X-Scissor 30; Ice Punch 34; Cross Chop 60.
- Removed against today's: Bubble 1; Harden 1,7; ViceGrip 1,10; Leer 1,13; BubbleBeam 20; Protect 23; Knock Off 26; Swift 30; Taunt 34; Swords Dance 52; Guillotine 65.
- Moved against today's: Crunch 57 to 65; Crabhammer 44 to 75.
- Against Kaizo's: Kaizo's ViceGrip 26 became Liquidation.
- Against Kaizo's: Kaizo's ViceGrip 44 became Liquidation.

**Lileep (345)**, 13 moves:

- New list: Ingrain 1, Rock Throw 1, Acid 8, Confuse Ray 15, Wring Out 22, Rock Slide 29, Brine 36, Poison Jab 43, Energy Ball 50, AncientPower 57, Earth Power 57, Gastro Acid 57, Giga Drain 64.
- Added against today's: Rock Throw 1; Rock Slide 29; Brine 36; Poison Jab 43; Earth Power 57; Giga Drain 64.
- Removed against today's: Astonish 1; Constrict 1; Amnesia 29; Stockpile 57; Spit Up 57; Swallow 57.
- Moved against today's: Ingrain 15 to 1; Confuse Ray 22 to 15; Wring Out 64 to 22; AncientPower 43 to 57; Gastro Acid 36 to 57.
- Against Kaizo's: Kaizo's Swallow 43 became Poison Jab.

**Cradily (346)**, 15 moves:

- New list: Mega Drain 1, Wrap 1, Mirror Coat 1, Ingrain 1, Gastro Acid 8, Wring Out 15, Confuse Ray 22, Stone Edge 29, Brine 36, Poison Jab 46, Energy Ball 56, AncientPower 66, Earth Power 66, Recover 66, Giga Drain 76.
- Added against today's: Mega Drain 1; Wrap 1; Mirror Coat 1; Stone Edge 29; Brine 36; Poison Jab 46; Earth Power 66; Recover 66; Giga Drain 76.
- Removed against today's: Astonish 1; Constrict 1; Acid 1,8; Amnesia 29; Stockpile 66; Spit Up 66; Swallow 66.
- Moved against today's: Ingrain 1,15 to 1; Gastro Acid 46 to 8; Wring Out 76 to 15; AncientPower 36 to 66.
- Against Kaizo's: Kaizo's Swallow 46 became Poison Jab.

**Feebas (349)**, 3 moves:

- New list: Water Pulse 1, Tackle 15, Flail 30.
- Added against today's: Water Pulse 1.
- Removed against today's: Splash 1.
- Against Kaizo's: the same.
- Rule: Tackle pick not applied: Kaizo's list has no Splash or Teleport and already starts with Water Pulse.

**Milotic (350)**, 14 moves:

- New list: Mirror Coat 1, Wrap 1, Aurora Beam 5, Whirlpool 9, Water Pulse 13, Twister 17, Aqua Tail 21, Hyper Voice 25, Refresh 29, DragonBreath 33, Hydro Pump 37, Twister 55, Ice Beam 76, Dragon Pulse 81.
- Added against today's: Mirror Coat 1; Aurora Beam 5; Whirlpool 9; Hyper Voice 25; DragonBreath 33; Ice Beam 76; Dragon Pulse 81.
- Removed against today's: Water Gun 1; Water Sport 5; Recover 21; Captivate 25; Rain Dance 33; Attract 41; Safeguard 45; Aqua Ring 49.
- Moved against today's: Twister 17 to 17,55; Aqua Tail 29 to 21; Refresh 9 to 29.
- Against Kaizo's: the same.

**Castform (351)**, 8 moves:

- New list: Nature Power 1, Water Gun 10, Ember 10, Powder Snow 10, Hydro Pump 20, Flamethrower 20, Ice Beam 20, Surf 30.
- Added against today's: Nature Power 1; Hydro Pump 20; Flamethrower 20; Ice Beam 20; Surf 30.
- Removed against today's: Tackle 1; Rain Dance 20; Sunny Day 20; Hail 20; Weather Ball 30.
- Against Kaizo's: Kaizo's Water Ball 30 became Surf.

**Duskull (355)**, 11 moves:

- New list: Astonish 1, Night Shade 1, Take Down 6, Payback 9, Confuse Ray 17, Double-Edge 22, Future Sight 25, Explosion 30, Pain Split 38, Aura Sphere 41, Shadow Sneak 100.
- Added against today's: Take Down 6; Double-Edge 22; Explosion 30; Pain Split 38; Aura Sphere 41.
- Removed against today's: Leer 1; Disable 6; Foresight 9; Pursuit 25; Curse 30; Will-O-Wisp 33; Mean Look 38.
- Moved against today's: Astonish 14 to 1; Payback 41 to 9; Future Sight 46 to 25; Shadow Sneak 22 to 100.
- Against Kaizo's: Kaizo's Memento 30 became Explosion.
- Rule: Teleport 14 out: Splash and Teleport go.
- Rule: Teleport 33 out: Splash and Teleport go.

**Dusclops (356)**, 18 moves:

- New list: Fire Punch 1, Ice Punch 1, ThunderPunch 1, Take Down 1, Mystical Fire 1, Shadow Ball 1, Night Shade 1, Future Sight 1, Hyper Beam 6, Zen Headbutt 9, Astonish 14, Shadow Ball 22, Seismic Toss 25, Payback 30, Double-Edge 33, Shadow Punch 43, Explosion 51, Earthquake 61.
- Added against today's: Take Down 1; Mystical Fire 1; Shadow Ball 1,22; Hyper Beam 6; Zen Headbutt 9; Seismic Toss 25; Double-Edge 33; Explosion 51; Earthquake 61.
- Removed against today's: Gravity 1; Bind 1; Leer 1; Disable 1,6; Foresight 9; Confuse Ray 17; Shadow Sneak 22; Pursuit 25; Curse 30; Will-O-Wisp 33; Mean Look 43.
- Moved against today's: Future Sight 61 to 1; Payback 51 to 30; Shadow Punch 37 to 43.
- Against Kaizo's: Kaizo's Memento 51 became Explosion.
- Rule: Teleport 17 out: Splash and Teleport go.
- Rule: Teleport 37 out: Splash and Teleport go.

**Tropius (357)**, 14 moves:

- New list: Seed Bomb 1, Gust 1, Body Slam 7, Nature Power 11, Sweet Scent 17, Magical Leaf 21, Aerial Ace 27, Earth Power 31, Dragon Pulse 37, Leaf Blade 41, Air Slash 47, Earthquake 51, Natural Gift 57, Leaf Storm 61.
- Added against today's: Seed Bomb 1; Nature Power 11; Aerial Ace 27; Earth Power 31; Dragon Pulse 37; Leaf Blade 41; Earthquake 51.
- Removed against today's: Leer 1; Growth 7; Razor Leaf 11; Stomp 17; Whirlwind 27; Synthesis 41; SolarBeam 51.
- Moved against today's: Body Slam 37 to 7; Sweet Scent 21 to 17; Magical Leaf 31 to 21.
- Against Kaizo's: the same.

**Chimecho (358)**, 15 moves:

- New list: Safeguard 1, Wrap 6, Uproar 9, Confuse Ray 14, Heal Bell 17, Hyper Voice 22, Yawn 25, Psychic 30, Signal Beam 33, Recover 38, Shadow Ball 41, Extrasensory 46, Aura Sphere 49, Flash Cannon 51, Metal Sound 85.
- Added against today's: Confuse Ray 14; Hyper Voice 22; Psychic 30; Signal Beam 33; Recover 38; Shadow Ball 41; Aura Sphere 49; Flash Cannon 51; Metal Sound 85.
- Removed against today's: Growl 6; Astonish 9; Confusion 14; Take Down 22; Psywave 30; Double-Edge 33; Healing Wish 49.
- Moved against today's: Safeguard 41 to 1; Wrap 1 to 6; Uproar 17 to 9; Heal Bell 38 to 17.
- Against Kaizo's: the same.

**Absol (359)**, 20 moves:

- New list: Faint Attack 1, Assurance 1, Bite 4, Dark Pulse 9, Aerial Ace 12, Slash 17, Rock Slide 20, Shadow Ball 22, Punishment 25, Future Sight 28, X-Scissor 40, Stone Edge 47, Pursuit 51, Shadow Claw 53, Zen Headbutt 55, Megahorn 60, Night Slash 67, Psycho Cut 69, Superpower 73, Shadow Sneak 99.
- Added against today's: Faint Attack 1; Assurance 1; Dark Pulse 9; Aerial Ace 12; Rock Slide 20; Shadow Ball 22; Punishment 25; X-Scissor 40; Stone Edge 47; Shadow Claw 53; Zen Headbutt 55; Megahorn 60; Superpower 73; Shadow Sneak 99.
- Removed against today's: Scratch 1; Feint 1; Leer 4; Taunt 9; Quick Attack 12; Razor Wind 17; Swords Dance 25; Double Team 33; Sucker Punch 44; Detect 49; Me First 57; Perish Song 65.
- Moved against today's: Bite 28 to 4; Slash 36 to 17; Future Sight 41 to 28; Pursuit 20 to 51; Night Slash 52 to 67; Psycho Cut 60 to 69.
- Rule: Teleport 61 out: Splash and Teleport go.

**Snorunt (361)**, 12 moves:

- New list: Powder Snow 1, Astonish 1, Bite 4, Headbutt 10, Aurora Beam 13, Secret Power 19, Nature Power 22, Ice Fang 28, Crunch 31, Double-Edge 37, Ice Beam 40, Shadow Ball 46.
- Added against today's: Astonish 1; Aurora Beam 13; Secret Power 19; Nature Power 22; Double-Edge 37; Ice Beam 40; Shadow Ball 46.
- Removed against today's: Leer 1; Double Team 4; Icy Wind 13; Protect 22; Ice Shard 37; Hail 40; Blizzard 46.
- Moved against today's: Bite 10 to 4; Headbutt 19 to 10.
- Against Kaizo's: the same.

**Glalie (362)**, 15 moves:

- New list: Powder Snow 1, Ice Ball 1, Rock Blast 1, Thunder Fang 1, Rock Slide 4, Bite 10, Ice Fang 13, Selfdestruct 19, Crunch 22, Earth Power 28, Ice Beam 31, Explosion 32, Stone Edge 55, Earthquake 60, Avalanche 75.
- Added against today's: Ice Ball 1; Rock Blast 1; Thunder Fang 1; Rock Slide 4; Selfdestruct 19; Earth Power 28; Explosion 32; Stone Edge 55; Earthquake 60; Avalanche 75.
- Removed against today's: Leer 1; Double Team 1,4; Icy Wind 13; Headbutt 19; Protect 22; Hail 40; Blizzard 51; Sheer Cold 59.
- Moved against today's: Bite 1,10 to 10; Ice Fang 28 to 13; Crunch 31 to 22; Ice Beam 37 to 31.
- Against Kaizo's: the same.

**Spheal (363)**, 13 moves:

- New list: Flatter 1, Powder Snow 1, Wake-Up Slap 1, Water Gun 1, Body Slam 7, BubbleBeam 13, Bounce 19, Gyro Ball 25, Encore 31, Ice Ball 37, Dive 37, Yawn 43, Aurora Beam 49.
- Added against today's: Flatter 1; Wake-Up Slap 1; BubbleBeam 13; Bounce 19; Gyro Ball 25; Dive 37; Yawn 43.
- Removed against today's: Defense Curl 1; Growl 1; Hail 31; Rest 37; Snore 37; Blizzard 43; Sheer Cold 49.
- Moved against today's: Body Slam 19 to 7; Encore 7 to 31; Ice Ball 13 to 37; Aurora Beam 25 to 49.
- Against Kaizo's: the same.

**Sealeo (364)**, 14 moves:

- New list: Powder Snow 1, Odor Sleuth 1, Brine 1, Secret Power 1, Gyro Ball 7, Bite 13, Body Slam 19, Aurora Beam 25, Encore 31, Ice Ball 39, Dive 39, Yawn 47, Aurora Beam 55, Flatter 58.
- Added against today's: Odor Sleuth 1; Brine 1; Secret Power 1; Gyro Ball 7; Bite 13; Dive 39; Yawn 47; Flatter 58.
- Removed against today's: Growl 1; Water Gun 1; Hail 31; Swagger 32; Rest 39; Snore 39; Blizzard 47; Sheer Cold 55.
- Moved against today's: Aurora Beam 25 to 25,55; Encore 1,7 to 31; Ice Ball 13 to 39.
- Against Kaizo's: the same.

**Walrein (365)**, 16 moves:

- New list: Body Slam 1, Brick Break 1, Brine 1, Ice Beam 1, Encore 1, Bite 7, Ice Ball 13, Brick Break 19, Icicle Spear 25, Close Combat 31, Dive 32, Super Fang 39, Ice Fang 39, Crunch 44, Aqua Tail 65, Yawn 65.
- Added against today's: Brick Break 1,19; Brine 1; Ice Beam 1; Bite 7; Icicle Spear 25; Close Combat 31; Dive 32; Super Fang 39; Aqua Tail 65; Yawn 65.
- Removed against today's: Powder Snow 1; Growl 1; Water Gun 1; Aurora Beam 25; Hail 31; Swagger 32; Rest 39; Snore 39; Blizzard 52; Sheer Cold 65.
- Moved against today's: Body Slam 19 to 1; Encore 1,7 to 1; Ice Fang 44 to 39; Crunch 1 to 44.
- Against Kaizo's: the same.

**Clamperl (366)**, 5 moves:

- New list: Bubble 1, Aurora Beam 1, Secret Power 1, Water Pulse 1, Clamp 44.
- Added against today's: Bubble 1; Aurora Beam 1; Secret Power 1; Water Pulse 1.
- Removed against today's: Water Gun 1; Whirlpool 1; Iron Defense 1.
- Moved against today's: Clamp 1 to 44.
- Against Kaizo's: the same.

**Huntail (367)**, 12 moves:

- New list: Liquidation 1, Bite 6, Hydro Pump 10, Water Pulse 15, Ice Beam 19, Bite 24, Liquidation 28, Body Slam 33, Ice Fang 37, Crunch 42, Aqua Tail 46, Poison Jab 51.
- Added against today's: Liquidation 1,28; Ice Beam 19; Body Slam 33; Poison Jab 51.
- Removed against today's: Whirlpool 1; Screech 10; Scary Face 19; Brine 28; Baton Pass 33; Dive 37.
- Moved against today's: Bite 6 to 6,24; Hydro Pump 51 to 10; Ice Fang 24 to 37.
- Against Kaizo's: Kaizo's ViceGrip 1 became Liquidation.
- Against Kaizo's: Kaizo's ViceGrip 28 became Liquidation.
- Against Kaizo's: Kaizo's Swallow 51 became Poison Jab.

**Gorebyss (368)**, 12 moves:

- New list: Liquidation 1, Confusion 6, Leech Life 10, Water Pulse 15, Aurora Beam 19, Psychic 24, Mega Drain 28, Whirlpool 33, Shadow Ball 37, Ice Beam 42, Giga Drain 46, Hydro Pump 51.
- Added against today's: Liquidation 1; Leech Life 10; Aurora Beam 19; Mega Drain 28; Shadow Ball 37; Ice Beam 42; Giga Drain 46.
- Removed against today's: Agility 10; Amnesia 19; Aqua Ring 24; Captivate 28; Baton Pass 33; Dive 37; Aqua Tail 46.
- Moved against today's: Psychic 42 to 24; Whirlpool 1 to 33.
- Against Kaizo's: Kaizo's ViceGrip 1 became Liquidation.

**Relicanth (369)**, 13 moves:

- New list: Body Slam 1, AncientPower 1, Take Down 8, Hydro Pump 15, Rock Slide 22, Double-Edge 29, Yawn 36, Dive 43, Stone Edge 50, Avalanche 57, Earthquake 64, Aqua Tail 71, Head Smash 94.
- Added against today's: Body Slam 1; Rock Slide 22; Stone Edge 50; Avalanche 57; Earthquake 64; Aqua Tail 71.
- Removed against today's: Tackle 1; Harden 1; Water Gun 8; Rock Tomb 15; Mud Sport 36; Rest 64.
- Moved against today's: AncientPower 43 to 1; Take Down 29 to 8; Hydro Pump 71 to 15; Double-Edge 50 to 29; Yawn 22 to 36; Dive 57 to 43; Head Smash 78 to 94.
- Against Kaizo's: the same.

**Luvdisc (370)**, 12 moves:

- New list: Flail 1, Charm 4, Aqua Jet 7, Water Pulse 9, Aqua Ring 14, Lucky Chant 17, Attract 22, Sweet Kiss 27, Brine 31, Safeguard 37, Captivate 40, Muddy Water 46.
- Added against today's: Aqua Jet 7; Brine 31; Muddy Water 46.
- Removed against today's: Tackle 1; Water Gun 7; Agility 9; Take Down 14.
- Moved against today's: Flail 46 to 1; Water Pulse 31 to 9; Aqua Ring 37 to 14; Safeguard 51 to 37.
- Against Kaizo's: Kaizo's Heart Swap 51 left out: Oxide has no move like it.

**Metang (375)**, 13 moves:

- New list: Magnet Bomb 1, ThunderPunch 1, Ice Punch 1, Pursuit 1, Metal Claw 20, Explosion 20, Double-Edge 28, Iron Head 32, Zen Headbutt 36, Selfdestruct 40, Psycho Cut 48, Explosion 52, Meteor Mash 56.
- Added against today's: Magnet Bomb 1; ThunderPunch 1; Ice Punch 1; Explosion 20,52; Double-Edge 28; Iron Head 32; Selfdestruct 40; Psycho Cut 48.
- Removed against today's: Magnet Rise 1; Take Down 1; Confusion 1,20; Scary Face 24; Bullet Punch 32; Psychic 36; Iron Defense 40; Agility 44; Hyper Beam 56.
- Moved against today's: Pursuit 28 to 1; Metal Claw 1,20 to 20; Zen Headbutt 52 to 36; Meteor Mash 48 to 56.
- Rule: Teleport 24 out: Splash and Teleport go.
- Rule: Teleport 44 out: Splash and Teleport go.

**Metagross (376)**, 15 moves:

- New list: Bite 1, Thunder Fang 1, Zen Headbutt 1, Magnet Bomb 1, Metal Claw 20, Body Slam 20, Ice Fang 24, Double-Edge 28, Crunch 32, Psycho Cut 40, Iron Head 44, Selfdestruct 45, Explosion 53, Hammer Arm 64, Meteor Mash 71.
- Added against today's: Bite 1; Thunder Fang 1; Magnet Bomb 1; Body Slam 20; Ice Fang 24; Double-Edge 28; Crunch 32; Psycho Cut 40; Iron Head 44; Selfdestruct 45; Explosion 53.
- Removed against today's: Magnet Rise 1; Take Down 1; Confusion 1,20; Scary Face 24; Pursuit 28; Bullet Punch 32; Psychic 36; Iron Defense 40; Agility 44; Hyper Beam 71.
- Moved against today's: Zen Headbutt 62 to 1; Metal Claw 1,20 to 20; Hammer Arm 45 to 64; Meteor Mash 53 to 71.
- Rule: Teleport 36 out: Splash and Teleport go.

**Regirock (377)**, 13 moves:

- New list: Ice Punch 1, ThunderPunch 1, Fire Punch 9, Lock-On 17, Hammer Arm 25, Rock Blast 33, Selfdestruct 41, Drain Punch 49, Stone Edge 57, Explosion 65, Earthquake 73, Superpower 81, Rock Wrecker 89.
- Added against today's: Ice Punch 1; ThunderPunch 1; Fire Punch 9; Rock Blast 33; Selfdestruct 41; Drain Punch 49; Earthquake 73; Rock Wrecker 89.
- Removed against today's: Stomp 1; Rock Throw 9; Curse 17; AncientPower 33; Iron Defense 41; Charge Beam 49; Zap Cannon 65; Hyper Beam 89.
- Moved against today's: Lock-On 57 to 17; Hammer Arm 81 to 25; Stone Edge 73 to 57; Explosion 1 to 65; Superpower 25 to 81.
- Against Kaizo's: the same.

**Regice (378)**, 12 moves:

- New list: Lock-On 1, Focus Blast 1, Earth Power 9, Tri Attack 17, Ice Beam 25, AncientPower 33, Zap Cannon 41, Selfdestruct 49, Blizzard 57, Explosion 65, Thunderbolt 73, Hyper Beam 81.
- Added against today's: Focus Blast 1; Earth Power 9; Tri Attack 17; Selfdestruct 49; Blizzard 57; Thunderbolt 73.
- Removed against today's: Stomp 1; Icy Wind 9; Curse 17; Superpower 25; Amnesia 41; Charge Beam 49; Hammer Arm 81.
- Moved against today's: Lock-On 57 to 1; Ice Beam 73 to 25; Zap Cannon 65 to 41; Explosion 1 to 65; Hyper Beam 89 to 81.
- Against Kaizo's: the same.

**Registeel (379)**, 14 moves:

- New list: Ice Punch 1, ThunderPunch 1, Metal Claw 9, Earthquake 17, AncientPower 25, DynamicPunch 33, Iron Head 41, Selfdestruct 41, Hammer Arm 57, Meteor Mash 65, Explosion 73, Stone Edge 73, Superpower 81, Gyro Ball 89.
- Added against today's: Ice Punch 1; ThunderPunch 1; Earthquake 17; DynamicPunch 33; Selfdestruct 41; Meteor Mash 65; Stone Edge 73; Gyro Ball 89.
- Removed against today's: Stomp 1; Curse 17; Iron Defense 41; Amnesia 41; Charge Beam 49; Lock-On 57; Zap Cannon 65; Flash Cannon 73; Hyper Beam 89.
- Moved against today's: AncientPower 33 to 25; Iron Head 73 to 41; Hammer Arm 81 to 57; Explosion 1 to 73; Superpower 25 to 81.
- Against Kaizo's: the same.

**Latias (380)**, 14 moves:

- New list: Triple Axel 1, Hyper Voice 5, Transform 10, Zen Headbutt 15, DragonBreath 20, Hyper Beam 25, Psycho Shift 30, Whirlwind 35, Dragon Pulse 40, Recover 45, Roar 50, Explosion 60, Outrage 65, Mist Ball 70.
- Added against today's: Triple Axel 1; Hyper Voice 5; Transform 10; Hyper Beam 25; Whirlwind 35; Roar 50; Explosion 60; Outrage 65.
- Removed against today's: Psywave 1; Wish 5; Helping Hand 10; Safeguard 15; Water Sport 25; Refresh 30; Charm 55; Healing Wish 60; Psychic 65.
- Moved against today's: Zen Headbutt 40 to 15; Psycho Shift 50 to 30; Dragon Pulse 70 to 40; Mist Ball 35 to 70.
- Against Kaizo's: Kaizo's Memento 60 became Explosion.
- Rule: Teleport 55 out: Splash and Teleport go.

**Latios (381)**, 14 moves:

- New list: Triple Axel 1, ExtremeSpeed 5, Aqua Jet 10, Zen Headbutt 15, DragonBreath 20, Hyper Beam 25, Refresh 30, Psycho Shift 35, Pursuit 40, Recover 45, Whirlwind 50, Explosion 60, Outrage 65, Luster Purge 70.
- Added against today's: Triple Axel 1; ExtremeSpeed 5; Aqua Jet 10; Hyper Beam 25; Pursuit 40; Whirlwind 50; Explosion 60; Outrage 65.
- Removed against today's: Psywave 1; Heal Block 5; Helping Hand 10; Safeguard 15; Protect 25; Dragon Dance 55; Memento 60; Psychic 65; Dragon Pulse 70.
- Moved against today's: Zen Headbutt 40 to 15; Psycho Shift 50 to 35; Luster Purge 35 to 70.
- Against Kaizo's: Kaizo's Memento 60 became Explosion.
- Rule: Teleport 55 out: Splash and Teleport go.

**Turtwig (387)**, 13 moves:

- New list: Tackle 1, Mega Drain 6, Bite 9, Rock Throw 13, Razor Leaf 15, Secret Power 17, Dig 25, Rock Slide 29, Crunch 33, Leaf Blade 37, Sand Tomb 41, Stone Edge 45, Synthesis 54.
- Added against today's: Rock Throw 13; Secret Power 17; Dig 25; Rock Slide 29; Leaf Blade 37; Sand Tomb 41; Stone Edge 45.
- Removed against today's: Withdraw 5; Absorb 9; Curse 17; Leech Seed 29; Giga Drain 41; Leaf Storm 45.
- Moved against today's: Mega Drain 25 to 6; Bite 21 to 9; Razor Leaf 13 to 15; Crunch 37 to 33; Synthesis 33 to 54.
- Against Kaizo's: the same.

**Grotle (388)**, 15 moves:

- New list: Seed Bomb 1, Headbutt 1, Mega Drain 6, Bite 9, Rock Throw 13, High Horsepower 16, Secret Power 17, Magical Leaf 22, Mud Shot 27, Rock Slide 32, Crunch 37, Leaf Blade 42, Sand Tomb 47, Stone Edge 52, Synthesis 70.
- Added against today's: Seed Bomb 1; Headbutt 1; Rock Throw 13; High Horsepower 16; Secret Power 17; Magical Leaf 22; Mud Shot 27; Rock Slide 32; Leaf Blade 42; Sand Tomb 47; Stone Edge 52.
- Removed against today's: Tackle 1; Withdraw 1,5; Absorb 9; Razor Leaf 13; Curse 17; Leech Seed 32; Giga Drain 47; Leaf Storm 52.
- Moved against today's: Mega Drain 27 to 6; Bite 22 to 9; Crunch 42 to 37; Synthesis 37 to 70.
- Against Kaizo's: Kaizo's Stomp 16 became High Horsepower.

**Torterra (389)**, 18 moves:

- New list: Leaf Storm 1, Tackle 1, Magical Leaf 1, Body Slam 1, Razor Leaf 1, Bite 5, Magical Leaf 9, Mud Shot 13, Rock Throw 17, Iron Head 22, Leaf Blade 27, Earthquake 32, Rock Slide 36, Crunch 39, Wood Hammer 45, Earthquake 51, Stone Edge 57, Double-Edge 60.
- Added against today's: Magical Leaf 1,9; Body Slam 1; Mud Shot 13; Rock Throw 17; Iron Head 22; Leaf Blade 27; Rock Slide 36; Stone Edge 57; Double-Edge 60.
- Removed against today's: Withdraw 1,5; Absorb 1,9; Curse 17; Mega Drain 27; Leech Seed 33; Synthesis 39; Giga Drain 51.
- Moved against today's: Leaf Storm 57 to 1; Razor Leaf 1,13 to 1; Bite 22 to 5; Earthquake 32 to 32,51; Crunch 45 to 39; Wood Hammer 1 to 45.
- Against Kaizo's: the same.

**Piplup (393)**, 15 moves:

- New list: Pound 1, Peck 6, Bubble 8, DoubleSlap 11, Metal Claw 13, Aurora Beam 16, Aqua Cutter 19, Helping Hand 22, Mist 25, Whirlpool 29, Roar 32, Hydro Pump 38, Weather Ball 40, Aqua Tail 43, Aqua Jet 49.
- Added against today's: DoubleSlap 11; Metal Claw 13; Aurora Beam 16; Aqua Cutter 19; Helping Hand 22; Roar 32; Weather Ball 40; Aqua Tail 43; Aqua Jet 49.
- Removed against today's: Growl 4; Water Sport 11; BubbleBeam 18; Bide 22; Fury Attack 25; Brine 29; Drill Peck 39.
- Moved against today's: Peck 15 to 6; Mist 36 to 25; Whirlpool 32 to 29; Hydro Pump 43 to 38.
- Against Kaizo's: the same.

**Prinplup (394)**, 18 moves:

- New list: Yawn 1, Dive 1, Peck 4, Bubble 8, Aurora Beam 13, BubbleBeam 14, Aqua Cutter 16, Aerial Ace 21, Natural Gift 24, Double Hit 26, Drill Peck 28, Mist 30, Knock Off 37, Haze 42, Avalanche 44, Aqua Tail 47, Weather Ball 51, Aqua Jet 55.
- Added against today's: Yawn 1; Dive 1; Aurora Beam 13; Aqua Cutter 16; Aerial Ace 21; Natural Gift 24; Double Hit 26; Knock Off 37; Haze 42; Avalanche 44; Aqua Tail 47; Weather Ball 51; Aqua Jet 55.
- Removed against today's: Tackle 1; Growl 1,4; Water Sport 11; Metal Claw 16; Bide 24; Fury Attack 28; Brine 33; Whirlpool 37; Hydro Pump 51.
- Moved against today's: Peck 15 to 4; BubbleBeam 19 to 14; Drill Peck 46 to 28; Mist 42 to 30.
- Against Kaizo's: the same.

**Empoleon (395)**, 19 moves:

- New list: Brick Break 1, Aqua Cutter 1, Night Slash 11, Double Hit 15, Hydro Pump 16, Yawn 19, Natural Gift 24, Rock Slide 28, X-Scissor 33, Steel Wing 39, Icicle Spear 40, Flash Cannon 44, Knock Off 46, Ice Beam 49, Metal Burst 55, Earthquake 64, Avalanche 70, Aqua Jet 73, Waterfall 75.
- Added against today's: Brick Break 1; Aqua Cutter 1; Night Slash 11; Double Hit 15; Yawn 19; Natural Gift 24; Rock Slide 28; X-Scissor 33; Steel Wing 39; Icicle Spear 40; Flash Cannon 44; Knock Off 46; Ice Beam 49; Metal Burst 55; Earthquake 64; Avalanche 70; Waterfall 75.
- Removed against today's: Tackle 1; Growl 1,4; Bubble 1,8; Swords Dance 11; Peck 15; Metal Claw 16; BubbleBeam 19; Swagger 24; Fury Attack 28; Brine 33; Aqua Tail 36; Whirlpool 39; Mist 46; Drill Peck 52.
- Moved against today's: Hydro Pump 59 to 16; Aqua Jet 36 to 73.
- Rule: Beat Up 1 out: Beat Up leaves the game.

**Starly (396)**, 11 moves:

- New list: Tackle 1, Sand-Attack 1, Peck 5, Swift 9, Gust 13, Headbutt 17, Wing Attack 21, Whirlwind 25, Steel Wing 29, Double-Edge 45, Brave Bird 50.
- Added against today's: Sand-Attack 1; Peck 5; Swift 9; Gust 13; Headbutt 17; Steel Wing 29; Double-Edge 45.
- Removed against today's: Growl 1; Quick Attack 5; Double Team 13; Endeavor 17; Aerial Ace 25; Take Down 29; Agility 33.
- Moved against today's: Wing Attack 9 to 21; Whirlwind 21 to 25; Brave Bird 37 to 50.
- Against Kaizo's: the same.

**Staravia (397)**, 12 moves:

- New list: Tackle 1, Sand-Attack 1, Peck 1, Peck 5, Swift 9, Bite 13, Headbutt 18, Wing Attack 23, Whirlwind 25, Steel Wing 36, Double-Edge 55, Brave Bird 60.
- Added against today's: Sand-Attack 1; Peck 1,5; Swift 9; Bite 13; Headbutt 18; Steel Wing 36; Double-Edge 55.
- Removed against today's: Growl 1; Quick Attack 1,5; Double Team 13; Endeavor 18; Aerial Ace 28; Take Down 33; Agility 38.
- Moved against today's: Wing Attack 9 to 23; Whirlwind 23 to 25; Brave Bird 43 to 60.
- Against Kaizo's: the same.

**Staraptor (398)**, 14 moves:

- New list: Tackle 1, Secret Power 1, Pluck 1, Air Slash 1, Pursuit 5, Endeavor 9, Roar 13, Headbutt 18, Steel Wing 38, Blaze Kick 40, Knock Off 50, Double-Edge 55, Close Combat 65, Brave Bird 70.
- Added against today's: Secret Power 1; Pluck 1; Air Slash 1; Pursuit 5; Roar 13; Headbutt 18; Steel Wing 38; Blaze Kick 40; Knock Off 50; Double-Edge 55.
- Removed against today's: Growl 1; Quick Attack 1,5; Wing Attack 1,9; Double Team 13; Whirlwind 23; Aerial Ace 28; Take Down 33; Agility 41.
- Moved against today's: Endeavor 18 to 9; Close Combat 34 to 65; Brave Bird 49 to 70.
- Against Kaizo's: the same.

**Bidoof (399)**, 12 moves:

- New list: Quick Attack 1, Bite 5, Water Gun 9, Headbutt 13, BubbleBeam 17, Hyper Fang 21, Dive 25, Yawn 29, Crunch 33, Super Fang 37, Superpower 41, Aqua Tail 45.
- Added against today's: Quick Attack 1; Bite 5; Water Gun 9; BubbleBeam 17; Dive 25; Crunch 33; Aqua Tail 45.
- Removed against today's: Tackle 1; Growl 5; Defense Curl 9; Rollout 13; Amnesia 29; Take Down 33; Curse 45.
- Moved against today's: Headbutt 17 to 13; Yawn 25 to 29.
- Against Kaizo's: the same.

**Bibarel (400)**, 14 moves:

- New list: Tackle 1, Mud Bomb 1, Mud Bomb 5, Bite 9, Ice Fang 13, Mud Shot 15, BubbleBeam 18, Hyper Fang 23, Dive 28, Yawn 33, Aqua Jet 38, Super Fang 40, Superpower 43, Aqua Tail 47.
- Added against today's: Mud Bomb 1,5; Bite 9; Ice Fang 13; Mud Shot 15; BubbleBeam 18; Dive 28; Aqua Jet 38; Aqua Tail 47.
- Removed against today's: Growl 1,5; Defense Curl 9; Rollout 13; Water Gun 15; Headbutt 18; Amnesia 33; Take Down 38; Curse 53.
- Moved against today's: Yawn 28 to 33; Super Fang 43 to 40; Superpower 48 to 43.
- Against Kaizo's: the same.

**Kricketot (401)**, 3 moves:

- New list: Growl 1, Bug Bite 1, Rollout 16.
- Added against today's: Rollout 16.
- Removed against today's: Bide 1.
- Moved against today's: Bug Bite 16 to 1.
- Against Kaizo's: the same.

**Kricketune (402)**, 13 moves:

- New list: Growl 1, Bug Buzz 1, False Swipe 10, Slash 14, GrassWhistle 18, Leech Life 22, Karate Chop 24, Bug Buzz 30, Sing 34, Fury Cutter 38, Night Slash 42, Brick Break 46, Swords Dance 57.
- Added against today's: False Swipe 10; GrassWhistle 18; Karate Chop 24; Brick Break 46; Swords Dance 57.
- Removed against today's: Bide 1; Focus Energy 22; X-Scissor 30; Screech 34; Taunt 38; Perish Song 50.
- Moved against today's: Bug Buzz 46 to 1,30; Slash 26 to 14; Leech Life 14 to 22; Sing 18 to 34; Fury Cutter 10 to 38.
- Against Kaizo's: the same.

**Shinx (403)**, 12 moves:

- New list: Swift 1, ThunderShock 5, Flash 9, Bite 13, Discharge 17, Roar 21, Ice Fang 30, Fire Fang 30, Crunch 36, Thunder Fang 37, Wild Charge 41, Fake Out 43.
- Added against today's: Swift 1; ThunderShock 5; Flash 9; Ice Fang 30; Fire Fang 30; Wild Charge 41; Fake Out 43.
- Removed against today's: Tackle 1; Leer 5; Charge 9; Spark 13; Swagger 25; Scary Face 37.
- Moved against today's: Bite 17 to 13; Discharge 41 to 17; Crunch 33 to 36; Thunder Fang 29 to 37.
- Against Kaizo's: the same.

**Luxio (404)**, 13 moves:

- New list: Slash 1, Flash 1, Ice Fang 5, Thunder Wave 9, Shock Wave 16, Roar 18, Metal Claw 23, Double Kick 28, Fire Fang 33, Night Slash 38, Roar 43, Wild Charge 49, Fake Out 51.
- Added against today's: Slash 1; Flash 1; Ice Fang 5; Thunder Wave 9; Shock Wave 16; Metal Claw 23; Double Kick 28; Fire Fang 33; Night Slash 38; Wild Charge 49; Fake Out 51.
- Removed against today's: Tackle 1; Leer 1,5; Charge 9; Spark 13; Bite 18; Swagger 28; Thunder Fang 33; Crunch 38; Scary Face 43; Discharge 48.
- Moved against today's: Roar 23 to 18,43.
- Against Kaizo's: the same.

**Luxray (405)**, 15 moves:

- New list: Mean Look 1, Bite 1, Fake Out 1, Feint 5, Discharge 9, Fire Fang 13, Headbutt 18, Thunderbolt 28, Faint Attack 30, Roar 42, Iron Tail 49, Lock-On 51, Thunder Fang 56, Wild Charge 66, Pursuit 71.
- Added against today's: Mean Look 1; Fake Out 1; Feint 5; Fire Fang 13; Headbutt 18; Thunderbolt 28; Faint Attack 30; Iron Tail 49; Lock-On 51; Wild Charge 66; Pursuit 71.
- Removed against today's: Tackle 1; Take Down 1; Leer 1,5; Submission 1; Charge 1,9; Spark 13; Swagger 28; Crunch 42; Scary Face 49; Double-Edge 60; Volt Tackle 64.
- Moved against today's: Bite 18 to 1; Discharge 56 to 9; Roar 23 to 42; Thunder Fang 35 to 56.
- Rule: Teleport 23 out: Splash and Teleport go.

**Budew (406)**, 6 moves:

- New list: Vine Whip 1, Poison Sting 4, PoisonPowder 7, Stun Spore 10, Razor Leaf 13, Acid 16.
- Added against today's: Vine Whip 1; Poison Sting 4; PoisonPowder 7; Razor Leaf 13; Acid 16.
- Removed against today's: Absorb 1; Growth 4; Water Sport 7; Mega Drain 13; Worry Seed 16.
- Against Kaizo's: the same.

**Roserade (407)**, 5 moves:

- New list: Power Whip 1, Sweet Scent 1, Poison Jab 1, Bullet Seed 1, Stun Spore 4.
- Added against today's: Power Whip 1; Poison Jab 1; Bullet Seed 1; Stun Spore 4.
- Removed against today's: Weather Ball 1; Poison Sting 1; Mega Drain 1; Magical Leaf 1.
- Against Kaizo's: the same.

**Cranidos (408)**, 13 moves:

- New list: Headbutt 1, Pursuit 1, Take Down 6, Rock Throw 10, Roar 15, Headbutt 19, Rock Slide 24, Assurance 28, Dig 33, Zen Headbutt 37, Roar 43, Iron Head 70, Head Smash 99.
- Added against today's: Rock Throw 10; Roar 15,43; Rock Slide 24; Dig 33; Iron Head 70.
- Removed against today's: Leer 1; Focus Energy 6; Scary Face 19; AncientPower 28; Screech 37.
- Moved against today's: Headbutt 1 to 1,19; Pursuit 10 to 1; Take Down 15 to 6; Assurance 24 to 28; Zen Headbutt 33 to 37; Head Smash 43 to 99.
- Against Kaizo's: the same.

**Rampardos (409)**, 13 moves:

- New list: Headbutt 1, Pursuit 1, Double-Edge 6, Iron Head 10, Endeavor 15, Crunch 19, Zen Headbutt 24, Iron Tail 28, Roar 30, Revenge 36, Pursuit 43, Roar 52, Stone Edge 100.
- Added against today's: Double-Edge 6; Iron Head 10; Crunch 19; Iron Tail 28; Roar 30,52; Revenge 36; Stone Edge 100.
- Removed against today's: Leer 1; Focus Energy 6; Take Down 15; Scary Face 19; Assurance 24; AncientPower 28; Screech 43; Head Smash 52.
- Moved against today's: Pursuit 10 to 1,43; Endeavor 30 to 15; Zen Headbutt 36 to 24.
- Against Kaizo's: the same.

**Shieldon (410)**, 11 moves:

- New list: Tackle 1, Flash Cannon 1, Rock Throw 6, Headbutt 10, Dig 15, Zen Headbutt 29, Stone Edge 34, Earthquake 38, Iron Head 45, Head Smash 75, Metal Burst 99.
- Added against today's: Flash Cannon 1; Rock Throw 6; Headbutt 10; Dig 15; Zen Headbutt 29; Stone Edge 34; Earthquake 38; Head Smash 75.
- Removed against today's: Protect 1; Taunt 6; Metal Sound 10; Take Down 15; Iron Defense 19; Swagger 24; AncientPower 28; Endure 33.
- Moved against today's: Iron Head 43 to 45; Metal Burst 37 to 99.
- Against Kaizo's: the same.

**Bastiodon (411)**, 14 moves:

- New list: Headbutt 1, Dig 1, Rock Throw 1, Zen Headbutt 1, Body Slam 6, Rock Slide 10, Iron Tail 15, High Horsepower 19, Double-Edge 24, Stone Edge 28, Iron Head 53, Earthquake 56, Head Smash 99, Metal Burst 100.
- Added against today's: Headbutt 1; Dig 1; Rock Throw 1; Zen Headbutt 1; Body Slam 6; Rock Slide 10; Iron Tail 15; High Horsepower 19; Double-Edge 24; Stone Edge 28; Earthquake 56; Head Smash 99.
- Removed against today's: Tackle 1; Protect 1; Taunt 1,6; Metal Sound 1,10; Take Down 15; Iron Defense 19; Swagger 24; AncientPower 28; Block 30; Endure 36.
- Moved against today's: Iron Head 52 to 53; Metal Burst 43 to 100.
- Against Kaizo's: Kaizo's Stomp 19 became High Horsepower.

**Burmy (412)**, 4 moves:

- New list: Leech Life 1, Nature Power 10, Camouflage 15, Hidden Power 20.
- Added against today's: Leech Life 1; Nature Power 10; Camouflage 15.
- Removed against today's: Protect 1; Tackle 10; Bug Bite 15.
- Against Kaizo's: the same.

**Wormadam (413)**, 14 moves:

- New list: Leech Life 16, Protect 16, Camouflage 16, Powder Snow 20, Bug Bite 23, Razor Leaf 26, Captivate 28, Iron Head 29, Sand Tomb 32, Signal Beam 35, Leaf Storm 38, Flash Cannon 41, Blizzard 44, Earth Power 47.
- Added against today's: Leech Life 16; Camouflage 16; Powder Snow 20; Iron Head 29; Sand Tomb 32; Signal Beam 35; Flash Cannon 41; Blizzard 44; Earth Power 47.
- Removed against today's: Tackle 1; Hidden Power 20; Confusion 23; Growth 29; Psybeam 32; Flail 38; Attract 41; Psychic 44.
- Moved against today's: Protect 10 to 16; Bug Bite 15 to 23; Captivate 35 to 28; Leaf Storm 47 to 38.
- Against Kaizo's: the same.
- Check: no level-1 move.

**Wormadam (sandy) (499)**, 13 moves:

- New list: Tackle 1, Protect 10, Bug Bite 15, Hidden Power 20, Protect 23, Rock Blast 26, Harden 29, Psybeam 32, Captivate 35, Flail 38, Attract 41, Psychic 44, Head Smash 47.
- Added against today's: Head Smash 47.
- Removed against today's: Confusion 23; Fissure 47.
- Moved against today's: Protect 10 to 10,23.
- Against Kaizo's: the same.

**Wormadam (trash) (500)**, 13 moves:

- New list: Tackle 1, Protect 10, Bug Bite 15, Hidden Power 20, Protect 23, Mirror Shot 26, Metal Sound 29, Psybeam 32, Captivate 35, Flail 38, Attract 41, Psychic 44, Iron Head 47.
- Removed against today's: Confusion 23.
- Moved against today's: Protect 10 to 10,23.
- Against Kaizo's: the same.

**Mothim (414)**, 13 moves:

- New list: Leech Life 1, U-turn 16, Camouflage 16, Psybeam 20, Bug Bite 23, Stun Spore 26, Aerial Ace 29, Giga Drain 32, Silver Wind 35, Sleep Powder 38, Air Slash 41, Psychic 44, Bug Buzz 47.
- Added against today's: Leech Life 1; U-turn 16; Stun Spore 26; Aerial Ace 29; Giga Drain 32; Sleep Powder 38.
- Removed against today's: Tackle 1; Protect 10; Hidden Power 20; Confusion 23; Gust 26; PoisonPowder 29.
- Moved against today's: Camouflage 35 to 16; Psybeam 32 to 20; Bug Bite 15 to 23; Silver Wind 38 to 35.
- Against Kaizo's: the same.

**Combee (415)**, 3 moves:

- New list: Bug Bite 1, Gust 1, Sweet Scent 13.
- Moved against today's: Bug Bite 13 to 1; Sweet Scent 1 to 13.
- Against Kaizo's: the same.

**Vespiquen (416)**, 16 moves:

- New list: Sweet Scent 1, Bug Bite 1, Poison Sting 3, Brick Break 7, Power Gem 9, Twineedle 13, Pursuit 15, Air Cutter 19, Whirlwind 21, Poison Jab 25, Bug Buzz 37, Air Slash 39, Roar 40, Attack Order 47, Hurricane 80, Heal Order 99.
- Added against today's: Bug Bite 1; Brick Break 7; Twineedle 13; Air Cutter 19; Whirlwind 21; Poison Jab 25; Bug Buzz 37; Air Slash 39; Roar 40; Hurricane 80.
- Removed against today's: Gust 1; Confuse Ray 7; Fury Cutter 9; Defend Order 13; Fury Swipes 19; Toxic 27; Slash 31; Captivate 33; Swagger 39; Destiny Bond 43.
- Moved against today's: Power Gem 21 to 9; Attack Order 37 to 47; Heal Order 25 to 99.
- Against Kaizo's: Kaizo's Rage 7 became Brick Break.

**Pachirisu (417)**, 14 moves:

- New list: Discharge 1, Pound 1, Bite 5, Hyper Fang 9, Shock Wave 13, Fire Fang 17, Rollout 20, Crunch 21, Ice Fang 25, Follow Me 27, Thunder Fang 35, Super Fang 45, Charm 50, Thunder 55.
- Added against today's: Pound 1; Bite 5; Hyper Fang 9; Shock Wave 13; Fire Fang 17; Rollout 20; Crunch 21; Ice Fang 25; Follow Me 27; Thunder Fang 35; Thunder 55.
- Removed against today's: Growl 1; Bide 1; Quick Attack 5; Spark 13; Endure 17; Swift 21; Sweet Kiss 25; Last Resort 37.
- Moved against today's: Discharge 29 to 1; Super Fang 33 to 45; Charm 9 to 50.
- Against Kaizo's: the same.

**Buizel (418)**, 11 moves:

- New list: Water Gun 1, Tackle 5, BubbleBeam 16, Bite 23, Water Pulse 30, Headbutt 36, Dive 41, Crunch 44, Ice Fang 48, Vital Throw 55, Aqua Tail 75.
- Added against today's: Tackle 5; BubbleBeam 16; Bite 23; Water Pulse 30; Headbutt 36; Dive 41; Crunch 44; Ice Fang 48; Vital Throw 55; Aqua Tail 75.
- Removed against today's: SonicBoom 1; Growl 1; Water Sport 1; Quick Attack 3; Pursuit 10; Swift 15; Aqua Jet 21; Agility 28; Whirlpool 36; Razor Wind 45.
- Moved against today's: Water Gun 6 to 1.
- Against Kaizo's: the same.

**Floatzel (419)**, 14 moves:

- New list: Snore 1, SonicBoom 1, Hydro Pump 1, Powder Snow 1, Swift 1, BubbleBeam 23, Bite 26, Ice Punch 30, Headbutt 35, Dive 41, Crunch 56, Ice Fang 69, Vital Throw 79, Aqua Tail 90.
- Added against today's: Snore 1; Hydro Pump 1; Powder Snow 1; BubbleBeam 23; Bite 26; Ice Punch 30; Headbutt 35; Dive 41; Vital Throw 79; Aqua Tail 90.
- Removed against today's: Growl 1; Water Sport 1; Quick Attack 1,3; Water Gun 6; Pursuit 10; Aqua Jet 21; Agility 29; Whirlpool 39; Razor Wind 50.
- Moved against today's: Swift 15 to 1; Crunch 26 to 56; Ice Fang 1 to 69.
- Against Kaizo's: the same.

**Cherubi (420)**, 10 moves:

- New list: Mega Drain 1, Headbutt 7, Morning Sun 10, Lucky Chant 13, Magical Leaf 19, Nature Power 22, Worry Seed 28, Flame Wheel 31, Seed Bomb 37, Helping Hand 40.
- Added against today's: Mega Drain 1; Headbutt 7; Morning Sun 10; Nature Power 22; Flame Wheel 31; Seed Bomb 37.
- Removed against today's: Tackle 1; Growth 7; Leech Seed 10; Sunny Day 22; Take Down 31; SolarBeam 37.
- Moved against today's: Lucky Chant 40 to 13; Helping Hand 13 to 40.
- Against Kaizo's: the same.

**Cherrim (421)**, 13 moves:

- New list: Body Slam 1, Lucky Chant 1, Rock Slide 7, Nature Power 10, Helping Hand 13, Magical Leaf 19, Stun Spore 22, Razor Leaf 25, Morning Sun 30, Blaze Kick 35, Leaf Blade 43, Petal Dance 56, Flare Blitz 60.
- Added against today's: Body Slam 1; Rock Slide 7; Nature Power 10; Stun Spore 22; Razor Leaf 25; Morning Sun 30; Blaze Kick 35; Leaf Blade 43; Flare Blitz 60.
- Removed against today's: Tackle 1; Growth 1,7; Leech Seed 10; Sunny Day 22; Worry Seed 30; Take Down 35; SolarBeam 43.
- Moved against today's: Lucky Chant 48 to 1; Petal Dance 25 to 56.
- Against Kaizo's: the same.

**Shellos (422)**, 10 moves:

- New list: Mud-Slap 1, Water Gun 2, Tackle 4, Swift 7, Mud Bomb 11, Water Pulse 16, Hidden Power 22, Body Slam 29, Muddy Water 37, Earth Power 46.
- Added against today's: Water Gun 2; Tackle 4; Swift 7; Earth Power 46.
- Removed against today's: Mud Sport 2; Harden 4; Rain Dance 22; Recover 46.
- Moved against today's: Water Pulse 7 to 16; Hidden Power 16 to 22.
- Against Kaizo's: the same.

**Gastrodon (423)**, 13 moves:

- New list: Earth Power 1, Dive 1, Secret Power 1, Brine 1, Sludge Bomb 2, Mud-Slap 4, Water Pulse 7, Mud Bomb 11, Hidden Power 16, Rock Slide 22, Body Slam 29, Muddy Water 47, Earthquake 54.
- Added against today's: Earth Power 1; Dive 1; Secret Power 1; Brine 1; Sludge Bomb 2; Rock Slide 22; Earthquake 54.
- Removed against today's: Mud Sport 1,2; Harden 1,4; Rain Dance 22; Recover 54.
- Moved against today's: Mud-Slap 1 to 4; Water Pulse 1,7 to 7; Muddy Water 41 to 47.
- Against Kaizo's: the same.

**Ambipom (424)**, 16 moves:

- New list: Last Resort 1, Astonish 1, Dig 1, Scratch 1, Sand-Attack 4, Astonish 8, Metal Claw 11, Swift 15, Faint Attack 18, Water Pulse 22, Karate Chop 25, Slash 29, Bite 34, Aerial Ace 56, Force Palm 69, Double Hit 83.
- Added against today's: Dig 1; Metal Claw 11; Faint Attack 18; Water Pulse 22; Karate Chop 25; Slash 29; Bite 34; Aerial Ace 56; Force Palm 69.
- Removed against today's: Tail Whip 1; Baton Pass 11; Tickle 15; Fury Swipes 18; Screech 25; Agility 29; Fling 36; Nasty Plot 39.
- Moved against today's: Last Resort 43 to 1; Sand-Attack 1,4 to 4; Swift 22 to 15; Double Hit 32 to 83.
- Against Kaizo's: the same.

**Drifloon (425)**, 12 moves:

- New list: Wrap 1, Gust 1, Astonish 6, Whirlwind 14, Payback 17, Selfdestruct 22, Air Cutter 27, Shadow Ball 27, Explosion 30, Air Slash 33, Focus Blast 38, Ominous Wind 43.
- Added against today's: Wrap 1; Whirlwind 14; Selfdestruct 22; Air Cutter 27; Air Slash 33; Focus Blast 38.
- Removed against today's: Constrict 1; Minimize 1; Focus Energy 14; Stockpile 22; Swallow 27; Spit Up 27; Baton Pass 33.
- Moved against today's: Gust 11 to 1; Shadow Ball 38 to 27; Explosion 43 to 30; Ominous Wind 30 to 43.
- Rule: Teleport 11 out: Splash and Teleport go.

**Drifblim (426)**, 14 moves:

- New list: Surf 1, Wrap 1, Astonish 1, Gust 1, Astonish 6, Whirlwind 14, Payback 17, Selfdestruct 22, Air Slash 27, Shadow Ball 27, Explosion 32, Air Slash 37, Focus Blast 44, Ominous Wind 51.
- Added against today's: Surf 1; Wrap 1; Whirlwind 14; Selfdestruct 22; Air Slash 27,37; Focus Blast 44.
- Removed against today's: Constrict 1; Minimize 1; Focus Energy 14; Stockpile 22; Swallow 27; Spit Up 27; Baton Pass 37.
- Moved against today's: Gust 1,11 to 1; Shadow Ball 44 to 27; Explosion 51 to 32; Ominous Wind 32 to 51.
- Against Kaizo's: Kaizo's Water Ball 1 became Surf.
- Rule: Teleport 11 out: Splash and Teleport go.

**Buneary (427)**, 14 moves:

- New list: Astonish 1, Pound 1, Rolling Kick 1, Foresight 1, Bite 6, Swift 13, DoubleSlap 16, Double Kick 23, Crunch 36, Blaze Kick 43, Dizzy Punch 46, Bounce 53, Hi Jump Kick 56, Mega Kick 65.
- Added against today's: Astonish 1; Rolling Kick 1; Bite 6; Swift 13; DoubleSlap 16; Double Kick 23; Crunch 36; Blaze Kick 43; Hi Jump Kick 56; Mega Kick 65.
- Removed against today's: Splash 1; Defense Curl 1; Endure 6; Frustration 13; Quick Attack 16; Jump Kick 23; Baton Pass 26; Agility 33; Charm 43; Healing Wish 53.
- Moved against today's: Dizzy Punch 36 to 46; Bounce 46 to 53.
- Against Kaizo's: the same.

**Lopunny (428)**, 16 moves:

- New list: Mirror Coat 1, Magic Coat 1, Rolling Kick 1, Bite 1, Body Slam 1, Foresight 1, Low Kick 6, Slash 13, Dig 16, Jump Kick 20, Crunch 36, Blaze Kick 43, Dizzy Punch 46, Bounce 53, Hi Jump Kick 60, Mega Kick 73.
- Added against today's: Rolling Kick 1; Bite 1; Body Slam 1; Low Kick 6; Slash 13; Dig 16; Crunch 36; Blaze Kick 43; Hi Jump Kick 60; Mega Kick 73.
- Removed against today's: Splash 1; Pound 1; Defense Curl 1; Endure 6; Return 13; Quick Attack 16; Baton Pass 26; Agility 33; Charm 43; Healing Wish 53.
- Moved against today's: Jump Kick 23 to 20; Dizzy Punch 36 to 46; Bounce 46 to 53.
- Against Kaizo's: the same.

**Mismagius (429)**, 5 moves:

- New list: Shadow Ball 1, Magical Leaf 1, Lucky Chant 1, Night Shade 90, Shadow Sneak 100.
- Added against today's: Shadow Ball 1; Night Shade 90; Shadow Sneak 100.
- Removed against today's: Growl 1; Psywave 1; Spite 1; Astonish 1.
- Rule: Teleport 1 out: Splash and Teleport go.

**Honchkrow (430)**, 8 moves:

- New list: Night Shade 1, Assurance 1, Chatter 1, Pursuit 1, Whirlwind 25, Brave Bird 35, Superpower 45, Punishment 55.
- Added against today's: Night Shade 1; Assurance 1; Chatter 1; Whirlwind 25; Brave Bird 35; Superpower 45; Punishment 55.
- Removed against today's: Astonish 1; Haze 1; Wing Attack 1; Swagger 25; Nasty Plot 35; Night Slash 45; Dark Pulse 55.
- Against Kaizo's: the same.

**Glameow (431)**, 13 moves:

- New list: Copycat 1, Charm 4, Scratch 5, Faint Attack 8, Aerial Ace 13, Metal Claw 17, Slash 20, Night Slash 25, Assist 29, Hypnosis 32, Fake Out 37, Sucker Punch 41, Fury Swipes 45.
- Added against today's: Copycat 1; Aerial Ace 13; Metal Claw 17; Night Slash 25.
- Removed against today's: Growl 8; Captivate 32; Attract 45.
- Moved against today's: Charm 25 to 4; Faint Attack 17 to 8; Slash 37 to 20; Hypnosis 13 to 32; Fake Out 1 to 37; Fury Swipes 20 to 45.
- Against Kaizo's: the same.

**Purugly (432)**, 15 moves:

- New list: Copycat 1, Fury Swipes 1, Bite 1, Scratch 5, Faint Attack 8, Aerial Ace 13, Metal Claw 17, Slash 20, Night Slash 25, Assist 29, Hypnosis 37, Fake Out 42, Shadow Claw 45, Body Slam 47, Sucker Punch 53.
- Added against today's: Copycat 1; Bite 1; Aerial Ace 13; Metal Claw 17; Night Slash 25; Shadow Claw 45; Sucker Punch 53.
- Removed against today's: Growl 1,8; Charm 25; Captivate 32; Swagger 38; Attract 53.
- Moved against today's: Fury Swipes 20 to 1; Scratch 1,5 to 5; Faint Attack 17 to 8; Slash 37 to 20; Hypnosis 13 to 37; Fake Out 1 to 42; Body Slam 45 to 47.
- Against Kaizo's: the same.

**Chingling (433)**, 6 moves:

- New list: Confusion 1, Wrap 6, Uproar 9, Heal Bell 14, Psybeam 17, Recover 22.
- Added against today's: Heal Bell 14; Psybeam 17; Recover 22.
- Removed against today's: Growl 6; Astonish 9; Last Resort 22.
- Moved against today's: Confusion 14 to 1; Wrap 1 to 6; Uproar 17 to 9.
- Against Kaizo's: the same.

**Stunky (434)**, 12 moves:

- New list: Scratch 1, Smog 1, Pursuit 4, Toxic 7, Selfdestruct 10, SmokeScreen 14, Metal Claw 18, Sludge 22, Explosion 27, Night Slash 32, Sludge Bomb 38, Gunk Shot 44.
- Added against today's: Smog 1; Pursuit 4; Selfdestruct 10; Metal Claw 18; Sludge 22; Sludge Bomb 38; Gunk Shot 44.
- Removed against today's: Focus Energy 1; Poison Gas 4; Screech 7; Fury Swipes 10; Feint 18; Slash 22; Memento 38.
- Moved against today's: Toxic 27 to 7; Explosion 44 to 27.
- Against Kaizo's: the same.

**Skuntank (435)**, 14 moves:

- New list: Scratch 1, Slash 1, Smog 1, Pursuit 4, Toxic 7, Metal Claw 10, Selfdestruct 14, SmokeScreen 18, Sludge Bomb 22, Sludge 27, Explosion 32, Night Slash 34, Flamethrower 42, Gunk Shot 62.
- Added against today's: Smog 1; Pursuit 4; Metal Claw 10; Selfdestruct 14; Sludge Bomb 22; Sludge 27; Gunk Shot 62.
- Removed against today's: Focus Energy 1; Poison Gas 1,4; Screech 7; Fury Swipes 10; Feint 18; Memento 42.
- Moved against today's: Slash 22 to 1; Toxic 27 to 7; SmokeScreen 14 to 18; Explosion 52 to 32; Night Slash 32 to 34; Flamethrower 34 to 42.
- Against Kaizo's: the same.

**Bronzor (436)**, 12 moves:

- New list: Confuse Ray 1, Hypnosis 1, Selfdestruct 5, Extrasensory 12, Iron Head 19, Explosion 26, Zen Headbutt 30, Payback 35, Mirror Shot 37, Selfdestruct 41, Psychic 49, Gyro Ball 52.
- Added against today's: Selfdestruct 5,41; Iron Head 19; Explosion 26; Zen Headbutt 30; Mirror Shot 37; Psychic 49.
- Removed against today's: Tackle 1; Confusion 1; Imprison 12; Iron Defense 26; Safeguard 30; Future Sight 37; Faint Attack 41; Heal Block 52.
- Moved against today's: Confuse Ray 14 to 1; Hypnosis 7 to 1; Extrasensory 19 to 12; Payback 49 to 35; Gyro Ball 35 to 52.
- Rule: Teleport 14 out: Splash and Teleport go.

**Bronzong (437)**, 15 moves:

- New list: Future Sight 1, Extrasensory 1, Psybeam 1, Flash Cannon 1, Payback 12, Iron Head 14, Zen Headbutt 19, Selfdestruct 26, Mirror Shot 30, Psychic 33, Confuse Ray 38, Explosion 43, Gyro Ball 50, Earthquake 61, Hypnosis 67.
- Added against today's: Psybeam 1; Flash Cannon 1; Iron Head 14; Zen Headbutt 19; Selfdestruct 26; Mirror Shot 30; Psychic 33; Explosion 43; Earthquake 61.
- Removed against today's: Sunny Day 1; Rain Dance 1; Tackle 1; Confusion 1; Imprison 1,12; Iron Defense 26; Safeguard 30; Block 33; Faint Attack 50; Heal Block 67.
- Moved against today's: Future Sight 43 to 1; Extrasensory 19 to 1; Payback 61 to 12; Confuse Ray 14 to 38; Gyro Ball 38 to 50; Hypnosis 1,7 to 67.
- Rule: Teleport 7 out: Splash and Teleport go.
- Rule: Extrasensory 1 listed twice; one kept.
- Rule: Future Sight 1 listed twice; one kept.

**Bonsly (438)**, 13 moves:

- New list: Rock Throw 1, Copycat 1, Mimic 6, Low Kick 9, Rock Throw 14, Selfdestruct 17, Block 22, Faint Attack 25, Rock Slide 30, Explosion 33, Wood Hammer 38, Sucker Punch 41, Fake Tears 56.
- Added against today's: Selfdestruct 17; Explosion 33; Wood Hammer 38.
- Removed against today's: Flail 6; Rock Tomb 30; Slam 38; Double-Edge 46.
- Moved against today's: Rock Throw 14 to 1,14; Mimic 17 to 6; Rock Slide 33 to 30; Fake Tears 1 to 56.
- Against Kaizo's: the same.

**Mime Jr (439)**, 15 moves:

- New list: Safeguard 1, DoubleSlap 1, Confusion 1, Copycat 4, Magical Leaf 11, Zen Headbutt 15, Mimic 18, Barrier 22, Seismic Toss 25, Psybeam 29, Light Screen 32, Reflect 36, Role Play 43, Signal Beam 46, Psychic 50.
- Added against today's: Magical Leaf 11; Zen Headbutt 15; Seismic Toss 25; Signal Beam 46.
- Removed against today's: Tickle 1; Meditate 8; Encore 11; Substitute 29; Recycle 32; Trick 36; Baton Pass 46.
- Moved against today's: Safeguard 50 to 1; DoubleSlap 15 to 1; Barrier 1 to 22; Psybeam 25 to 29; Light Screen 22 to 32; Reflect 22 to 36; Psychic 39 to 50.
- Rule: Teleport 22 out: Splash and Teleport go.
- Rule: Teleport 39 out: Splash and Teleport go.

**Happiny (440)**, 5 moves:

- New list: Pound 1, Seismic Toss 1, Copycat 5, Refresh 9, Sweet Kiss 12.
- Added against today's: Seismic Toss 1.
- Removed against today's: Charm 1.
- Against Kaizo's: the same.

**Chatot (441)**, 13 moves:

- New list: Uproar 1, Air Cutter 5, Mirror Move 9, Sing 13, Roar 17, Chatter 21, Copycat 25, Mimic 29, Mud-Slap 33, Heat Wave 37, Air Slash 41, Hyper Voice 45, Mirror Move 65.
- Added against today's: Air Cutter 5; Roar 17; Copycat 25; Mud-Slap 33; Heat Wave 37; Air Slash 41.
- Removed against today's: Peck 1; Growl 5; Fury Attack 17; Taunt 25; Roost 33; FeatherDance 41.
- Moved against today's: Uproar 37 to 1; Mirror Move 9 to 9,65.
- Against Kaizo's: the same.

**Spiritomb (442)**, 12 moves:

- New list: Pain Split 1, Pursuit 1, Confuse Ray 1, Revenge 1, Payback 1, Hypnosis 13, Silver Wind 19, Curse 20, Ominous Wind 25, Dark Pulse 37, Aura Sphere 43, Earth Power 49.
- Added against today's: Pain Split 1; Revenge 1; Payback 1; Silver Wind 19; Aura Sphere 43; Earth Power 49.
- Removed against today's: Spite 1; Shadow Sneak 1; Faint Attack 7; Dream Eater 19; Sucker Punch 31; Nasty Plot 37; Memento 43.
- Moved against today's: Curse 1 to 20; Dark Pulse 49 to 37.
- Rule: Teleport 31 out: Splash and Teleport go.

**Gible (443)**, 10 moves:

- New list: Take Down 1, Bite 3, Dragon Rage 7, Crunch 13, Sand Tomb 15, Dragon Claw 19, Roar 25, Fire Fang 27, Earthquake 31, Dragon Rush 77.
- Added against today's: Bite 3; Crunch 13; Roar 25; Fire Fang 27; Earthquake 31.
- Removed against today's: Tackle 1; Sand-Attack 3; Sandstorm 13; Slash 25; Dig 31.
- Moved against today's: Take Down 15 to 1; Sand Tomb 19 to 15; Dragon Claw 27 to 19; Dragon Rush 37 to 77.
- Against Kaizo's: the same.

**Gabite (444)**, 11 moves:

- New list: Dragon Pulse 1, Supersonic 1, Hyper Voice 3, Dragon Rage 7, Crunch 13, Sand Tomb 15, Dragon Claw 19, Roar 28, Fire Fang 33, Earthquake 40, Dragon Rush 88.
- Added against today's: Dragon Pulse 1; Supersonic 1; Hyper Voice 3; Crunch 13; Roar 28; Fire Fang 33; Earthquake 40.
- Removed against today's: Tackle 1; Sand-Attack 1,3; Sandstorm 13; Take Down 15; Slash 28; Dig 40.
- Moved against today's: Sand Tomb 19 to 15; Dragon Claw 33 to 19; Dragon Rush 49 to 88.
- Against Kaizo's: the same.

**Garchomp (445)**, 15 moves:

- New list: Pursuit 1, Block 1, Air Slash 1, Twister 1, Air Cutter 1, Fire Fang 3, Fly 7, Crunch 13, Sand Tomb 15, Dragon Claw 19, Sky Attack 28, Whirlwind 33, Roar 40, Earthquake 48, Dragon Rush 55.
- Added against today's: Pursuit 1; Block 1; Air Slash 1; Twister 1; Air Cutter 1; Fly 7; Sky Attack 28; Whirlwind 33; Roar 40; Earthquake 48.
- Removed against today's: Tackle 1; Sand-Attack 1,3; Dragon Rage 1,7; Sandstorm 1,13; Take Down 15; Slash 28; Dig 40.
- Moved against today's: Fire Fang 1 to 3; Crunch 48 to 13; Sand Tomb 19 to 15; Dragon Claw 33 to 19.
- Against Kaizo's: the same.

**Munchlax (446)**, 15 moves:

- New list: Shadow Claw 1, Whirlwind 1, Tackle 1, Metronome 4, Headbutt 9, Bite 12, Whirlwind 17, Submission 20, Take Down 25, Selfdestruct 28, Body Slam 33, Whirlwind 36, Crunch 41, Double-Edge 44, Poison Jab 100.
- Added against today's: Shadow Claw 1; Whirlwind 1,17,36; Headbutt 9; Bite 12; Submission 20; Take Down 25; Selfdestruct 28; Crunch 41; Double-Edge 44; Poison Jab 100.
- Removed against today's: Odor Sleuth 1; Defense Curl 4; Amnesia 9; Lick 12; Recycle 17; Screech 20; Stockpile 25; Swallow 28; Fling 36; Rollout 41; Natural Gift 44; Last Resort 49.
- Moved against today's: Metronome 1 to 4.
- Against Kaizo's: Kaizo's Lick 1 became Shadow Claw.
- Against Kaizo's: Kaizo's Swallow 100 became Poison Jab.

**Riolu (447)**, 9 moves:

- New list: Metal Claw 1, Force Palm 1, Bite 1, ThunderPunch 6, Iron Head 11, Aura Sphere 15, Copycat 19, Extrasensory 24, Ice Punch 29.
- Added against today's: Metal Claw 1; Bite 1; ThunderPunch 6; Iron Head 11; Aura Sphere 15; Extrasensory 24; Ice Punch 29.
- Removed against today's: Quick Attack 1; Foresight 1; Endure 1; Counter 6; Feint 15; Reversal 19; Screech 24.
- Moved against today's: Force Palm 11 to 1; Copycat 29 to 19.
- Against Kaizo's: the same.

**Lucario (448)**, 15 moves:

- New list: ExtremeSpeed 1, Extrasensory 1, Dragon Pulse 1, Iron Head 1, Metal Claw 1, Crunch 6, Force Palm 11, Feint 15, Bone Rush 19, Dark Pulse 24, Flash Cannon 29, Aura Sphere 33, Roar 42, Meteor Mash 47, Close Combat 75.
- Added against today's: Extrasensory 1; Iron Head 1; Crunch 6; Flash Cannon 29; Roar 42; Meteor Mash 47.
- Removed against today's: Quick Attack 1; Foresight 1; Detect 1; Counter 6; Metal Sound 24; Me First 29; Swords Dance 33.
- Moved against today's: ExtremeSpeed 51 to 1; Dragon Pulse 47 to 1; Dark Pulse 1 to 24; Aura Sphere 37 to 33; Close Combat 42 to 75.
- Against Kaizo's: Kaizo's Bonemerang 37 left out: Oxide has no move like it.

**Hippopotas (449)**, 10 moves:

- New list: Double-Edge 1, Whirlwind 1, Bite 7, Yawn 13, Ice Fang 19, Sand Tomb 25, Crunch 31, Roar 37, Stone Edge 44, Earthquake 50.
- Added against today's: Whirlwind 1; Ice Fang 19; Roar 37; Stone Edge 44.
- Removed against today's: Tackle 1; Sand-Attack 1; Take Down 19; Fissure 50.
- Moved against today's: Double-Edge 44 to 1; Earthquake 37 to 50.
- Against Kaizo's: the same.

**Hippowdon (450)**, 15 moves:

- New list: Ice Fang 1, Fire Fang 1, Thunder Fang 1, Body Slam 1, Sand-Attack 1, Whirlwind 1, Pursuit 1, Bite 7, Yawn 13, Double-Edge 19, Sand Tomb 25, Crunch 31, Roar 40, Stone Edge 50, Earthquake 60.
- Added against today's: Body Slam 1; Whirlwind 1; Pursuit 1; Roar 40; Stone Edge 50.
- Removed against today's: Tackle 1; Take Down 19; Fissure 60.
- Moved against today's: Bite 1,7 to 7; Yawn 1,13 to 13; Double-Edge 50 to 19; Earthquake 40 to 60.
- Against Kaizo's: the same.

**Skorupi (451)**, 12 moves:

- New list: Bite 1, Poison Sting 1, Leech Life 1, Pin Missile 6, Poison Jab 12, Slash 17, Twineedle 23, Cross Poison 28, Night Slash 34, X-Scissor 39, Aqua Tail 45, Poison Tail 65.
- Added against today's: Leech Life 1; Poison Jab 12; Slash 17; Twineedle 23; Night Slash 34; X-Scissor 39; Aqua Tail 45; Poison Tail 65.
- Removed against today's: Leer 1; Knock Off 6; Acupressure 17; Scary Face 23; Toxic Spikes 28; Bug Bite 34; Poison Fang 39; Crunch 45.
- Moved against today's: Pin Missile 12 to 6; Cross Poison 50 to 28.
- Against Kaizo's: the same.

**Drapion (452)**, 16 moves:

- New list: Thunder Fang 1, Ice Fang 1, Fire Fang 1, Bite 1, Poison Fang 1, Crush Claw 1, Bug Bite 1, Night Slash 6, Poison Jab 12, X-Scissor 17, Punishment 23, Cross Poison 28, Cross Chop 34, Crunch 39, Liquidation 49, Poison Tail 78.
- Added against today's: Crush Claw 1; Night Slash 6; Poison Jab 12; X-Scissor 17; Punishment 23; Cross Chop 34; Liquidation 49; Poison Tail 78.
- Removed against today's: Poison Sting 1; Leer 1; Knock Off 1,6; Pin Missile 12; Acupressure 17; Scary Face 23; Toxic Spikes 28.
- Moved against today's: Poison Fang 39 to 1; Bug Bite 34 to 1; Cross Poison 58 to 28; Crunch 49 to 39.
- Against Kaizo's: Kaizo's ViceGrip 49 became Liquidation.

**Croagunk (453)**, 14 moves:

- New list: Karate Chop 1, Poison Sting 3, Mud Bomb 8, Faint Attack 10, Flatter 15, Sludge Bomb 17, Rolling Kick 22, Payback 24, Poison Jab 29, Earth Power 31, Revenge 36, Pursuit 38, Gunk Shot 69, Vacuum Wave 77.
- Added against today's: Karate Chop 1; Rolling Kick 22; Payback 24; Earth Power 31; Gunk Shot 69; Vacuum Wave 77.
- Removed against today's: Astonish 1; Mud-Slap 3; Taunt 10; Swagger 24; Sucker Punch 31; Nasty Plot 36.
- Moved against today's: Poison Sting 8 to 3; Mud Bomb 29 to 8; Faint Attack 17 to 10; Flatter 45 to 15; Sludge Bomb 43 to 17; Poison Jab 38 to 29; Revenge 22 to 36; Pursuit 15 to 38.
- Against Kaizo's: the same.

**Toxicroak (454)**, 16 moves:

- New list: Assurance 1, Cross Poison 1, Flatter 1, Mud-Slap 3, Mud Bomb 8, Faint Attack 10, Twineedle 15, Sludge Bomb 17, Rolling Kick 22, Payback 24, Poison Jab 29, Earth Power 31, Revenge 45, Pursuit 51, Gunk Shot 70, Vacuum Wave 88.
- Added against today's: Assurance 1; Cross Poison 1; Twineedle 15; Rolling Kick 22; Payback 24; Earth Power 31; Gunk Shot 70; Vacuum Wave 88.
- Removed against today's: Astonish 1; Poison Sting 1,8; Taunt 10; Swagger 24; Sucker Punch 31; Nasty Plot 36.
- Moved against today's: Flatter 54 to 1; Mud-Slap 1,3 to 3; Mud Bomb 29 to 8; Faint Attack 17 to 10; Sludge Bomb 49 to 17; Poison Jab 41 to 29; Revenge 22 to 45; Pursuit 15 to 51.
- Against Kaizo's: the same.

**Carnivine (455)**, 13 moves:

- New list: Vine Whip 1, Leech Life 1, Bite 7, Sweet Scent 11, Razor Leaf 17, Faint Attack 21, Fire Fang 27, Wring Out 31, Giga Drain 31, Poison Jab 31, Crunch 37, Sleep Powder 41, Power Whip 47.
- Added against today's: Leech Life 1; Razor Leaf 17; Fire Fang 27; Giga Drain 31; Poison Jab 31; Sleep Powder 41.
- Removed against today's: Bind 1; Growth 1; Ingrain 21; Stockpile 31; Spit Up 31; Swallow 31.
- Moved against today's: Vine Whip 11 to 1; Sweet Scent 17 to 11; Faint Attack 27 to 21; Wring Out 41 to 31.
- Against Kaizo's: Kaizo's Swallow 31 became Poison Jab.

**Finneon (456)**, 15 moves:

- New list: Water Gun 1, Pound 6, Gust 10, Water Pulse 13, Pursuit 17, Flash 22, Signal Beam 26, U-turn 28, Dive 29, Bounce 33, Icy Wind 35, Ice Fang 38, Double-Edge 42, Whirlpool 45, Crunch 49.
- Added against today's: Pursuit 17; Flash 22; Signal Beam 26; Dive 29; Icy Wind 35; Ice Fang 38; Double-Edge 42; Crunch 49.
- Removed against today's: Attract 10; Rain Dance 13; Captivate 26; Safeguard 29; Aqua Ring 33; Silver Wind 49.
- Moved against today's: Water Gun 6 to 1; Pound 1 to 6; Gust 17 to 10; Water Pulse 22 to 13; U-turn 42 to 28; Bounce 45 to 33; Whirlpool 38 to 45.
- Against Kaizo's: the same.

**Lumineon (457)**, 19 moves:

- New list: Confuse Ray 1, Camouflage 1, Silver Wind 1, Brine 6, Pursuit 10, Flash 13, Bug Bite 17, Whirlpool 22, Signal Beam 26, Air Slash 28, Dive 29, U-turn 34, Ice Fang 35, Bounce 42, Silver Wind 45, Double-Edge 48, Fury Cutter 50, Aqua Tail 53, Ominous Wind 55.
- Added against today's: Confuse Ray 1; Camouflage 1; Brine 6; Pursuit 10; Flash 13; Bug Bite 17; Signal Beam 26; Air Slash 28; Dive 29; Ice Fang 35; Double-Edge 48; Fury Cutter 50; Aqua Tail 53; Ominous Wind 55.
- Removed against today's: Pound 1; Water Gun 1,6; Attract 1,10; Rain Dance 13; Gust 17; Water Pulse 22; Captivate 26; Safeguard 29; Aqua Ring 35.
- Moved against today's: Silver Wind 59 to 1,45; Whirlpool 42 to 22; U-turn 48 to 34; Bounce 53 to 42.
- Against Kaizo's: the same.

**Mantyke (458)**, 15 moves:

- New list: Wing Attack 1, Bubble 1, Supersonic 4, Water Pulse 10, Aurora Beam 13, BubbleBeam 19, Twister 22, Ice Beam 28, Roost 31, Whirlpool 37, Helping Hand 40, Air Slash 46, Hydro Pump 49, Hurricane 51, Scald 55.
- Added against today's: Aurora Beam 13; Twister 22; Ice Beam 28; Roost 31; Whirlpool 37; Helping Hand 40; Air Slash 46; Hurricane 51; Scald 55.
- Removed against today's: Tackle 1; Headbutt 13; Agility 19; Take Down 31; Confuse Ray 37; Bounce 40; Aqua Ring 46.
- Moved against today's: Wing Attack 22 to 1; Water Pulse 28 to 10; BubbleBeam 10 to 19.
- Against Kaizo's: the same.

**Snover (459)**, 12 moves:

- New list: Powder Snow 1, Razor Leaf 1, Ice Punch 5, Seed Bomb 9, Ice Beam 13, GrassWhistle 17, Focus Blast 21, Blizzard 26, Leaf Storm 31, Stone Edge 36, Avalanche 41, Wood Hammer 46.
- Added against today's: Ice Punch 5; Seed Bomb 9; Ice Beam 13; Focus Blast 21; Leaf Storm 31; Stone Edge 36; Avalanche 41.
- Removed against today's: Leer 1; Icy Wind 9; Swagger 17; Mist 21; Ice Shard 26; Ingrain 31; Sheer Cold 46.
- Moved against today's: Razor Leaf 5 to 1; GrassWhistle 13 to 17; Blizzard 41 to 26; Wood Hammer 36 to 46.
- Against Kaizo's: the same.

**Abomasnow (460)**, 15 moves:

- New list: Ice Punch 1, Hammer Arm 1, Energy Ball 1, Focus Blast 1, Stone Edge 1, Seed Bomb 5, Ice Beam 9, GrassWhistle 13, Whirlwind 17, Blizzard 21, Leaf Storm 26, Roar 31, Earthquake 36, Avalanche 47, Wood Hammer 58.
- Added against today's: Hammer Arm 1; Energy Ball 1; Focus Blast 1; Stone Edge 1; Seed Bomb 5; Ice Beam 9; Whirlwind 17; Leaf Storm 26; Roar 31; Earthquake 36; Avalanche 47.
- Removed against today's: Powder Snow 1; Leer 1; Razor Leaf 1,5; Icy Wind 1,9; Swagger 17; Mist 21; Ice Shard 26; Ingrain 31; Sheer Cold 58.
- Moved against today's: Blizzard 47 to 21; Wood Hammer 36 to 58.
- Against Kaizo's: the same.

**Weavile (461)**, 16 moves:

- New list: Revenge 1, Slash 1, Dark Pulse 1, Aurora Beam 1, Crush Claw 1, X-Scissor 1, Poison Jab 8, Assist 10, Metal Claw 14, Double-Edge 21, Ice Beam 24, Night Slash 28, Aerial Ace 35, Submission 38, Ice Punch 42, Punishment 59.
- Added against today's: Slash 1; Aurora Beam 1; Crush Claw 1; X-Scissor 1; Poison Jab 8; Assist 10; Double-Edge 21; Ice Beam 24; Aerial Ace 35; Submission 38; Ice Punch 42; Punishment 59.
- Removed against today's: Embargo 1; Assurance 1; Scratch 1; Leer 1; Taunt 1; Quick Attack 1,8; Screech 10; Faint Attack 14; Fury Swipes 21; Nasty Plot 24; Icy Wind 28; Fling 38.
- Moved against today's: Dark Pulse 49 to 1; Metal Claw 42 to 14; Night Slash 35 to 28.
- Rule: Beat Up 1 out: Beat Up leaves the game.

**Magnezone (462)**, 17 moves:

- New list: Mirror Coat 1, Tri Attack 1, Iron Head 1, Tackle 1, ThunderShock 1, Gyro Ball 1, ThunderShock 6, Supersonic 11, SonicBoom 14, Signal Beam 17, Shock Wave 22, Selfdestruct 30, Magnet Bomb 34, Discharge 40, Explosion 46, Flash Cannon 54, Thunderbolt 60.
- Added against today's: Tri Attack 1; Iron Head 1; Signal Beam 17; Shock Wave 22; Selfdestruct 30; Explosion 46; Flash Cannon 54; Thunderbolt 60.
- Removed against today's: Barrier 1; Metal Sound 1; Thunder Wave 17; Spark 22; Lock-On 27; Screech 34; Mirror Shot 46; Magnet Rise 50; Zap Cannon 60.
- Moved against today's: Gyro Ball 54 to 1; Supersonic 1,11 to 11; Magnet Bomb 30 to 34.
- Rule: Teleport 27 out: Splash and Teleport go.
- Rule: Teleport 50 out: Splash and Teleport go.

**Lickilicky (463)**, 18 moves:

- New list: Shadow Claw 1, Poison Jab 5, High Horsepower 9, Acid 13, Wrap 17, Double-Edge 21, Disable 25, Shadow Claw 29, Aqua Tail 33, Me First 37, Sludge Bomb 41, Slam 45, Power Whip 49, Zen Headbutt 51, Wring Out 53, Gastro Acid 57, Toxic 60, Shadow Claw 63.
- Added against today's: Shadow Claw 1,29,63; Poison Jab 5; High Horsepower 9; Acid 13; Double-Edge 21; Aqua Tail 33; Sludge Bomb 41; Zen Headbutt 51; Gastro Acid 57; Toxic 60.
- Removed against today's: Lick 1; Supersonic 5; Defense Curl 9; Knock Off 13; Stomp 21; Rollout 33; Refresh 41; Screech 45; Gyro Ball 57.
- Moved against today's: Slam 29 to 45.
- Against Kaizo's: Kaizo's Lick 1 became Shadow Claw.
- Against Kaizo's: Kaizo's Swallow 5 became Poison Jab.
- Against Kaizo's: Kaizo's Stomp 9 became High Horsepower.
- Against Kaizo's: Kaizo's Lick 29 became Shadow Claw.
- Against Kaizo's: Kaizo's Lick 63 became Shadow Claw.

**Rhyperior (464)**, 16 moves:

- New list: Fire Punch 1, Crush Claw 1, Roar 1, Rock Slide 1, Crunch 1, Aqua Tail 9, Submission 13, Rock Blast 21, Drill Run 25, Poison Jab 33, Hammer Arm 47, Stone Edge 49, Double-Edge 55, Megahorn 69, Earthquake 77, Rock Wrecker 100.
- Added against today's: Fire Punch 1; Crush Claw 1; Roar 1; Rock Slide 1; Crunch 1; Aqua Tail 9; Submission 13; Drill Run 25; Double-Edge 55.
- Removed against today's: Horn Attack 1; Tail Whip 1; Stomp 1,9; Fury Attack 1,13; Scary Face 21; Take Down 33; Horn Drill 37.
- Moved against today's: Rock Blast 25 to 21; Poison Jab 1 to 33; Hammer Arm 42 to 47; Stone Edge 45 to 49; Megahorn 57 to 69; Earthquake 49 to 77; Rock Wrecker 61 to 100.
- Against Kaizo's: the same.

**Tangrowth (465)**, 18 moves:

- New list: Sleep Powder 1, Wrap 1, Mega Drain 5, Sludge Bomb 8, Rock Slide 12, Slam 15, Vine Whip 19, Aerial Ace 22, AncientPower 26, Poison Jab 29, Power Whip 33, Poison Jab 36, Brick Break 40, Rock Slide 43, Energy Ball 47, Wring Out 50, Stun Spore 54, Endeavor 57.
- Added against today's: Wrap 1; Sludge Bomb 8; Rock Slide 12,43; Aerial Ace 22; Poison Jab 29,36; Brick Break 40; Energy Ball 47; Endeavor 57.
- Removed against today's: Ingrain 1; Constrict 1; Absorb 8; Growth 12; PoisonPowder 15; Bind 22; Knock Off 36; Natural Gift 40; Tickle 47; Block 57.
- Moved against today's: Sleep Powder 5 to 1; Mega Drain 26 to 5; Slam 43 to 15; AncientPower 33 to 26; Power Whip 54 to 33; Stun Spore 29 to 54.
- Against Kaizo's: Kaizo's Swallow 29 became Poison Jab.

**Electivire (466)**, 16 moves:

- New list: Flamethrower 1, Discharge 1, Psychic 1, ThunderShock 1, Hammer Arm 1, Thunderbolt 7, Low Kick 10, Swift 16, Shock Wave 19, Seismic Toss 25, ThunderPunch 28, Cross Chop 37, Fire Punch 43, Ice Punch 52, Wild Charge 65, Earthquake 69.
- Added against today's: Flamethrower 1; Psychic 1; Hammer Arm 1; Seismic Toss 25; Cross Chop 37; Ice Punch 52; Wild Charge 65; Earthquake 69.
- Removed against today's: Quick Attack 1; Leer 1; Light Screen 25; Screech 52; Thunder 58; Giga Impact 67.
- Moved against today's: Discharge 37 to 1; ThunderShock 1,7 to 1; Thunderbolt 43 to 7; Low Kick 1,10 to 10; Fire Punch 1 to 43.
- Against Kaizo's: the same.

**Magmortar (467)**, 17 moves:

- New list: Flare Blitz 1, Smog 1, Rock Slide 1, Heat Wave 1, SmokeScreen 1, Blast Burn 5, Faint Attack 7, ThunderPunch 10, Lava Plume 16, Cross Chop 19, Confuse Ray 25, Psychic 28, Thunderbolt 43, Focus Blast 52, Double-Edge 68, Fire Blast 77, Milk Drink 100.
- Added against today's: Flare Blitz 1; Rock Slide 1; Heat Wave 1; Blast Burn 5; Cross Chop 19; Psychic 28; Thunderbolt 43; Focus Blast 52; Double-Edge 68; Milk Drink 100.
- Removed against today's: Leer 1; Ember 1,7; Fire Spin 19; Fire Punch 28; Flamethrower 43; Sunny Day 52; Hyper Beam 67.
- Moved against today's: SmokeScreen 1,10 to 1; Faint Attack 16 to 7; ThunderPunch 1 to 10; Lava Plume 37 to 16; Fire Blast 58 to 77.
- Against Kaizo's: the same.

**Togekiss (468)**, 3 moves:

- New list: Whirlwind 1, Aura Sphere 1, Air Slash 1.
- Added against today's: Whirlwind 1.
- Removed against today's: Sky Attack 1; ExtremeSpeed 1.
- Rule: Teleport 1 out: Splash and Teleport go.

**Yanmega (469)**, 20 moves:

- New list: Night Slash 1, Bug Bite 1, Aerial Ace 1, Air Slash 1, Uproar 1, Whirlwind 1, Leech Life 6, Pursuit 11, Swift 14, SonicBoom 17, Supersonic 22, Whirlwind 27, Silver Wind 30, Ominous Wind 33, Air Cutter 38, Signal Beam 43, Whirlwind 46, AncientPower 49, Air Slash 54, Bug Buzz 57.
- Added against today's: Aerial Ace 1; Whirlwind 1,27,46; Leech Life 6; Swift 14; Silver Wind 30; Ominous Wind 33; Air Cutter 38; Signal Beam 43.
- Removed against today's: Tackle 1; Foresight 1; Quick Attack 1,6; Double Team 1,11; Detect 17; Feint 38; Slash 43; Screech 46; U-turn 49.
- Moved against today's: Air Slash 54 to 1,54; Uproar 27 to 1; Pursuit 30 to 11; SonicBoom 14 to 17; AncientPower 33 to 49.
- Against Kaizo's: the same.

**Leafeon (470)**, 14 moves:

- New list: Iron Tail 1, Magical Leaf 1, Bite 1, Aerial Ace 8, Leaf Blade 21, Sweet Scent 22, X-Scissor 29, Double Kick 36, Razor Leaf 43, Refresh 50, GrassWhistle 57, Double-Edge 64, Leaf Blade 71, Aromatherapy 78.
- Added against today's: Iron Tail 1; Bite 1; Aerial Ace 8; Sweet Scent 22; X-Scissor 29; Double Kick 36; Refresh 50; Double-Edge 64; Aromatherapy 78.
- Removed against today's: Tail Whip 1; Tackle 1; Helping Hand 1; Sand-Attack 8; Quick Attack 22; Synthesis 29; Giga Drain 43; Last Resort 50; Sunny Day 64; Swords Dance 78.
- Moved against today's: Magical Leaf 36 to 1; Leaf Blade 71 to 21,71; Razor Leaf 15 to 43.
- Against Kaizo's: the same.

**Glaceon (471)**, 20 moves:

- New list: Trump Card 1, Ice Fang 1, Barrier 21, Tickle 22, Nature Power 25, Aurora Beam 28, Signal Beam 29, Water Pulse 36, Earth Power 43, Ice Beam 50, Focus Blast 57, Shadow Ball 64, Mirror Coat 71, Blizzard 78, Hyper Beam 87, Mist 90, Ice Shard 92, Wish 97, Gravity 100, Trump Card 100.
- Added against today's: Trump Card 1,100; Tickle 22; Nature Power 25; Aurora Beam 28; Signal Beam 29; Water Pulse 36; Earth Power 43; Ice Beam 50; Focus Blast 57; Shadow Ball 64; Hyper Beam 87; Mist 90; Wish 97; Gravity 100.
- Removed against today's: Tail Whip 1; Tackle 1; Helping Hand 1; Sand-Attack 8; Icy Wind 15; Quick Attack 22; Bite 29; Last Resort 50; Hail 64.
- Moved against today's: Ice Fang 43 to 1; Barrier 78 to 21; Mirror Coat 57 to 71; Blizzard 71 to 78; Ice Shard 36 to 92.
- Against Kaizo's: the same.

**Gliscor (472)**, 19 moves:

- New list: Thunder Fang 1, Ice Fang 1, Fire Fang 1, Poison Jab 1, Sand-Attack 5, Sand Tomb 10, Night Slash 15, Faint Attack 20, Poison Tail 23, Cross Poison 25, Brick Break 28, X-Scissor 30, Rock Slide 33, Wing Attack 37, Steel Wing 41, Aqua Tail 44, Stone Edge 48, Aerial Ace 52, Earthquake 55.
- Added against today's: Sand Tomb 10; Poison Tail 23; Cross Poison 25; Brick Break 28; Rock Slide 33; Wing Attack 37; Steel Wing 41; Aqua Tail 44; Stone Edge 48; Aerial Ace 52; Earthquake 55.
- Removed against today's: Harden 1,9; Knock Off 1,12; Quick Attack 16; Fury Cutter 20; Screech 27; Swords Dance 34; U-turn 38; Guillotine 45.
- Moved against today's: Sand-Attack 1,5 to 5; Night Slash 31 to 15; Faint Attack 23 to 20; X-Scissor 42 to 30.
- Against Kaizo's: the same.

**Mamoswine (473)**, 18 moves:

- New list: AncientPower 1, Body Slam 1, Odor Sleuth 1, Mud-Slap 1, Powder Snow 1, Bite 4, Double-Edge 8, Earth Power 13, Rock Slide 16, Ice Beam 20, Dig 25, Stone Edge 28, Double Hit 32, Ice Fang 33, Earthquake 40, Crunch 48, Superpower 56, Icicle Spear 65.
- Added against today's: Body Slam 1; Bite 4; Double-Edge 8; Earth Power 13; Rock Slide 16; Ice Beam 20; Dig 25; Stone Edge 28; Crunch 48; Superpower 56; Icicle Spear 65.
- Removed against today's: Peck 1; Mud Sport 1,4; Endure 16; Mud Bomb 20; Hail 25; Take Down 32; Mist 48; Blizzard 56; Scary Face 65.
- Moved against today's: Mud-Slap 13 to 1; Powder Snow 1,8 to 1; Double Hit 33 to 32; Ice Fang 28 to 33.
- Against Kaizo's: the same.

**Gallade (475)**, 17 moves:

- New list: Poison Jab 1, Brick Break 1, X-Scissor 1, Psychic 1, Fire Punch 1, Ice Punch 1, ThunderPunch 6, Slash 10, Fury Cutter 12, Aqua Cutter 13, Leaf Blade 22, Zen Headbutt 25, Night Slash 31, Cross Chop 36, Psycho Cut 45, Stone Edge 50, Close Combat 53.
- Added against today's: Poison Jab 1; Brick Break 1; X-Scissor 1; Psychic 1; Fire Punch 1; Ice Punch 1; ThunderPunch 6; Aqua Cutter 13; Zen Headbutt 25; Cross Chop 36; Stone Edge 50.
- Removed against today's: Leer 1; Confusion 1,6; Double Team 1,10; Teleport 1,12; Swords Dance 25; Helping Hand 36; Feint 39; False Swipe 45; Protect 50.
- Moved against today's: Slash 22 to 10; Fury Cutter 17 to 12; Leaf Blade 1 to 22; Night Slash 1 to 31; Psycho Cut 31 to 45.
- Rule: Teleport 37 out: Splash and Teleport go.

**Probopass (476)**, 19 moves:

- New list: Head Smash 1, Tri Attack 1, Body Slam 1, Iron Head 1, Stone Edge 1, Hyper Beam 1, Earth Power 7, Seismic Toss 13, Rock Slide 19, Flash Cannon 25, Discharge 31, Selfdestruct 37, Power Gem 42, Magnet Bomb 49, Thunder Wave 55, Explosion 61, AncientPower 67, Mirror Shot 73, Metal Burst 79.
- Added against today's: Head Smash 1; Tri Attack 1; Body Slam 1; Iron Head 1; Hyper Beam 1; Seismic Toss 13; Flash Cannon 25; Selfdestruct 37; Explosion 61; AncientPower 67; Mirror Shot 73; Metal Burst 79.
- Removed against today's: Magnet Rise 1; Gravity 1; Tackle 1; Iron Defense 1,7; Block 1,19; Sandstorm 37; Rest 43; Zap Cannon 67; Lock-On 73.
- Moved against today's: Stone Edge 61 to 1; Earth Power 79 to 7; Rock Slide 31 to 19; Discharge 55 to 31; Power Gem 49 to 42; Magnet Bomb 1,13 to 49; Thunder Wave 25 to 55.
- Against Kaizo's: the same.

**Dusknoir (477)**, 18 moves:

- New list: Fire Punch 1, Ice Punch 1, ThunderPunch 1, Spacial Rend 1, Poison Jab 1, Astonish 1, Night Shade 1, Mystical Fire 1, Seismic Toss 6, Aura Sphere 9, Shadow Ball 14, Double-Edge 22, Payback 25, Submission 30, Stone Edge 33, Shadow Punch 43, Hammer Arm 51, Earthquake 61.
- Added against today's: Spacial Rend 1; Poison Jab 1; Mystical Fire 1; Seismic Toss 6; Aura Sphere 9; Shadow Ball 14; Double-Edge 22; Submission 30; Stone Edge 33; Hammer Arm 51; Earthquake 61.
- Removed against today's: Gravity 1; Bind 1; Leer 1; Disable 1,6; Foresight 9; Confuse Ray 17; Shadow Sneak 22; Pursuit 25; Curse 30; Will-O-Wisp 33; Mean Look 43; Future Sight 61.
- Moved against today's: Astonish 14 to 1; Payback 51 to 25; Shadow Punch 37 to 43.
- Against Kaizo's: Kaizo's Swallow 1 became Poison Jab.
- Rule: Teleport 17 out: Splash and Teleport go.
- Rule: Teleport 37 out: Splash and Teleport go.

**Froslass (478)**, 15 moves:

- New list: Swift 1, Powder Snow 1, Sweet Kiss 1, Water Pulse 1, Night Shade 4, Secret Power 10, Nature Power 13, Disable 17, Hyper Voice 22, Ice Fang 28, Shadow Ball 31, Roar 37, Aura Sphere 70, Ice Beam 77, Ominous Wind 85.
- Added against today's: Swift 1; Sweet Kiss 1; Water Pulse 1; Night Shade 4; Secret Power 10; Nature Power 13; Disable 17; Hyper Voice 22; Ice Fang 28; Shadow Ball 31; Roar 37; Aura Sphere 70; Ice Beam 77.
- Removed against today's: Leer 1; Double Team 1,4; Astonish 1,10; Icy Wind 13; Confuse Ray 19; Wake-Up Slap 28; Captivate 31; Ice Shard 37; Hail 40; Blizzard 51; Destiny Bond 59.
- Moved against today's: Ominous Wind 22 to 85.
- Rule: Teleport 19 out: Splash and Teleport go.

**Rotom (479)**, 11 moves:

- New list: ThunderShock 1, Uproar 1, Thunder Wave 1, Shock Wave 1, Night Shade 8, Confuse Ray 15, Shadow Ball 22, Dark Pulse 29, Signal Beam 36, Focus Blast 43, Discharge 50.
- Added against today's: Night Shade 8; Shadow Ball 22; Dark Pulse 29; Signal Beam 36; Focus Blast 43.
- Removed against today's: Trick 1; Astonish 1; Double Team 15; Ominous Wind 29; Substitute 36; Charge 43.
- Moved against today's: Uproar 8 to 1; Shock Wave 22 to 1; Confuse Ray 1 to 15.
- Rule: Teleport 1 out: Splash and Teleport go.

**Rotom (heat) (503)**, 12 moves:

- New list: Psybeam 1, Astonish 1, Thunder Wave 1, ThunderShock 1, Confuse Ray 1, Uproar 8, Shock Wave 22, Ominous Wind 29, Charge 43, Discharge 50, Will-O-Wisp 55, Flamethrower 60.
- Added against today's: Psybeam 1; Will-O-Wisp 55; Flamethrower 60.
- Removed against today's: Trick 1; Double Team 15; Substitute 36.
- Against Kaizo's: the same.

**Rotom (wash) (504)**, 12 moves:

- New list: Psybeam 1, Astonish 1, Thunder Wave 1, ThunderShock 1, Confuse Ray 1, Uproar 8, Shock Wave 22, Ominous Wind 29, Charge 43, Discharge 50, Whirlpool 55, Scald 60.
- Added against today's: Psybeam 1; Whirlpool 55; Scald 60.
- Removed against today's: Trick 1; Double Team 15; Substitute 36.
- Against Kaizo's: the same.

**Rotom (frost) (505)**, 12 moves:

- New list: Psybeam 1, Astonish 1, Thunder Wave 1, ThunderShock 1, Confuse Ray 1, Uproar 8, Shock Wave 22, Ominous Wind 29, Charge 43, Discharge 50, Ice Shard 55, Ice Beam 60.
- Added against today's: Psybeam 1; Ice Shard 55; Ice Beam 60.
- Removed against today's: Trick 1; Double Team 15; Substitute 36.
- Against Kaizo's: the same.

**Rotom (fan) (506)**, 12 moves:

- New list: Psybeam 1, Astonish 1, Thunder Wave 1, ThunderShock 1, Confuse Ray 1, Uproar 8, Shock Wave 22, Ominous Wind 29, Charge 43, Discharge 50, Hurricane 55, Defog 60.
- Added against today's: Psybeam 1; Hurricane 55; Defog 60.
- Removed against today's: Trick 1; Double Team 15; Substitute 36.
- Against Kaizo's: the same.

**Rotom (mow) (507)**, 12 moves:

- New list: Psybeam 1, Astonish 1, Thunder Wave 1, ThunderShock 1, Confuse Ray 1, Uproar 8, Shock Wave 22, Ominous Wind 29, Charge 43, Discharge 50, Giga Drain 55, Energy Ball 60.
- Added against today's: Psybeam 1; Giga Drain 55; Energy Ball 60.
- Removed against today's: Trick 1; Double Team 15; Substitute 36.
- Against Kaizo's: the same.

**Uxie (480)**, 10 moves:

- New list: Recover 1, Aura Sphere 1, Signal Beam 6, Extrasensory 16, Yawn 31, Future Sight 36, Thunder Wave 46, Psychic 51, Natural Gift 66, Explosion 76.
- Added against today's: Recover 1; Aura Sphere 1; Signal Beam 6; Thunder Wave 46; Psychic 51; Explosion 76.
- Removed against today's: Rest 1; Confusion 1; Imprison 6; Endure 16; Swift 21; Amnesia 46; Flail 61; Memento 76.
- Moved against today's: Extrasensory 51 to 16.
- Against Kaizo's: Kaizo's Memento 76 became Explosion.
- Rule: Teleport 21 out: Splash and Teleport go.
- Rule: Teleport 61 out: Splash and Teleport go.

**Mesprit (481)**, 10 moves:

- New list: Recover 1, Aura Sphere 1, Signal Beam 6, Extrasensory 16, Lucky Chant 31, Future Sight 36, Copycat 46, Psychic 51, Natural Gift 66, Focus Blast 76.
- Added against today's: Recover 1; Aura Sphere 1; Signal Beam 6; Psychic 51; Focus Blast 76.
- Removed against today's: Rest 1; Confusion 1; Imprison 6; Protect 16; Swift 21; Charm 46; Healing Wish 76.
- Moved against today's: Extrasensory 51 to 16; Copycat 61 to 46.
- Rule: Teleport 21 out: Splash and Teleport go.
- Rule: Teleport 61 out: Splash and Teleport go.

**Azelf (482)**, 11 moves:

- New list: Recover 1, Aura Sphere 1, Signal Beam 6, Extrasensory 16, Selfdestruct 21, Hyper Voice 31, Future Sight 36, Last Resort 46, Psychic 51, Natural Gift 66, Explosion 76.
- Added against today's: Recover 1; Aura Sphere 1; Signal Beam 6; Selfdestruct 21; Hyper Voice 31; Psychic 51.
- Removed against today's: Rest 1; Confusion 1; Imprison 6; Detect 16; Swift 21; Uproar 31; Nasty Plot 46.
- Moved against today's: Extrasensory 51 to 16; Last Resort 61 to 46.
- Rule: Teleport 61 out: Splash and Teleport go.

**Dialga (483)**, 11 moves:

- New list: Earth Power 1, Aura Sphere 1, Metal Claw 10, AncientPower 20, Dragon Claw 30, Roar of Time 40, DragonBreath 50, Outrage 60, Roar 70, Flash Cannon 80, Focus Blast 90.
- Added against today's: Outrage 60; Roar 70; Focus Blast 90.
- Removed against today's: Scary Face 1; Heal Block 50; Slash 70.
- Moved against today's: Earth Power 60 to 1; Aura Sphere 90 to 1; DragonBreath 1 to 50.
- Against Kaizo's: the same.

**Palkia (484)**, 11 moves:

- New list: Earth Power 1, Aura Sphere 1, Aqua Tail 10, AncientPower 20, Hydro Pump 30, Spacial Rend 40, DragonBreath 50, Outrage 60, Whirlwind 70, Whirlpool 80, Focus Blast 90.
- Added against today's: Hydro Pump 30; Outrage 60; Whirlwind 70; Whirlpool 80; Focus Blast 90.
- Removed against today's: Scary Face 1; Water Pulse 10; Dragon Claw 30; Heal Block 50; Slash 70.
- Moved against today's: Earth Power 60 to 1; Aura Sphere 90 to 1; Aqua Tail 80 to 10; DragonBreath 1 to 50.
- Against Kaizo's: the same.

**Heatran (485)**, 14 moves:

- New list: AncientPower 1, Poison Jab 5, Magma Storm 9, Fire Fang 17, Flash Cannon 25, Crunch 33, Earth Power 41, Lava Plume 49, Fire Spin 57, Iron Head 65, Explosion 73, Heat Wave 81, Stone Edge 88, Dragon Pulse 96.
- Added against today's: Poison Jab 5; Flash Cannon 25; Explosion 73; Dragon Pulse 96.
- Removed against today's: Leer 9; Metal Sound 25; Scary Face 41.
- Moved against today's: Magma Storm 96 to 9; Earth Power 73 to 41.
- Against Kaizo's: Kaizo's Swallow 5 became Poison Jab.

**Regigigas (486)**, 11 moves:

- New list: Fire Punch 1, Ice Punch 1, ThunderPunch 1, Dizzy Punch 1, Knock Off 1, Confuse Ray 1, Earthquake 1, Revenge 25, Zen Headbutt 50, Crush Grip 75, Explosion 100.
- Added against today's: Earthquake 1; Explosion 100.
- Removed against today's: Foresight 1; Giga Impact 100.
- Against Kaizo's: the same.

**Giratina (487)**, 11 moves:

- New list: DragonBreath 1, Aura Sphere 1, Ominous Wind 10, AncientPower 20, Dragon Claw 30, Shadow Force 40, Roar of Time 50, Shadow Force 60, Earthquake 70, Shadow Claw 80, Spacial Rend 90.
- Added against today's: Roar of Time 50; Earthquake 70; Spacial Rend 90.
- Removed against today's: Scary Face 1; Heal Block 50; Earth Power 60; Slash 70.
- Moved against today's: Aura Sphere 90 to 1; Shadow Force 40 to 40,60.
- Against Kaizo's: the same.

**Giratina (origin) (501)**, 11 moves:

- New list: DragonBreath 1, Scary Face 1, Ominous Wind 10, AncientPower 20, Dragon Claw 30, Shadow Force 40, Shadow Ball 50, Earth Power 60, Slash 70, Shadow Claw 80, Aura Sphere 90.
- Added against today's: Shadow Ball 50.
- Removed against today's: Heal Block 50.
- Against Kaizo's: the same.

**Cresselia (488)**, 11 moves:

- New list: Lunar Dance 1, Aura Sphere 1, Moonlight 11, Night Shade 20, Triple Axel 38, Psycho Shift 47, Psycho Cut 57, Whirlwind 66, Hyper Beam 75, Signal Beam 84, Psychic 93.
- Added against today's: Aura Sphere 1; Night Shade 20; Triple Axel 38; Whirlwind 66; Hyper Beam 75; Signal Beam 84.
- Removed against today's: Confusion 1; Double Team 1; Safeguard 11; Mist 20; Aurora Beam 29; Future Sight 38; Slash 47.
- Moved against today's: Lunar Dance 84 to 1; Moonlight 57 to 11; Psycho Shift 75 to 47; Psycho Cut 66 to 57.
- Rule: Teleport 29 out: Splash and Teleport go.

**Phione (489)**, 10 moves:

- New list: Focus Blast 1, Aqua Tail 1, Whirlwind 9, Supersonic 16, Energy Ball 24, Whirlpool 31, Earth Power 46, Ice Beam 54, Hydro Pump 61, Aura Sphere 69.
- Added against today's: Focus Blast 1; Aqua Tail 1; Whirlwind 9; Energy Ball 24; Earth Power 46; Ice Beam 54; Hydro Pump 61; Aura Sphere 69.
- Removed against today's: Bubble 1; Water Sport 1; Charm 9; BubbleBeam 24; Acid Armor 31; Water Pulse 46; Aqua Ring 54; Dive 61; Rain Dance 69.
- Moved against today's: Whirlpool 39 to 31.
- Rule: Teleport 39 out: Splash and Teleport go.

**Manaphy (490)**, 11 moves:

- New list: Aqua Tail 1, Focus Blast 1, Confuse Ray 1, Signal Beam 9, Whirlpool 16, Whirlwind 24, Energy Ball 39, Ice Beam 46, Hydro Pump 54, Earth Power 61, Aura Sphere 69.
- Added against today's: Aqua Tail 1; Focus Blast 1; Confuse Ray 1; Signal Beam 9; Whirlwind 24; Energy Ball 39; Ice Beam 46; Hydro Pump 54; Earth Power 61; Aura Sphere 69.
- Removed against today's: Tail Glow 1; Bubble 1; Water Sport 1; Charm 9; Supersonic 16; BubbleBeam 24; Acid Armor 31; Water Pulse 46; Aqua Ring 54; Dive 61; Rain Dance 69; Heart Swap 76.
- Moved against today's: Whirlpool 39 to 16.
- Against Kaizo's: Kaizo's Heart Swap 76 left out: Oxide has no move like it.
- Rule: Teleport 31 out: Splash and Teleport go.

**Darkrai (491)**, 13 moves:

- New list: Aura Sphere 1, Ominous Wind 1, Mean Look 5, Dark Pulse 11, Hypnosis 20, Faint Attack 29, Glare 35, Shadow Force 38, Dream Eater 47, Extrasensory 57, Dark Void 66, Aura Sphere 84, Dark Pulse 93.
- Added against today's: Aura Sphere 1,84; Mean Look 5; Glare 35; Shadow Force 38; Extrasensory 57.
- Removed against today's: Disable 1; Quick Attack 11; Nightmare 38; Double Team 47; Haze 57; Nasty Plot 75.
- Moved against today's: Dark Pulse 93 to 11,93; Dream Eater 84 to 47.
- Rule: Teleport 75 out: Splash and Teleport go.

**Shaymin (492)**, 12 moves:

- New list: Earth Power 1, Magical Leaf 10, Air Slash 19, Synthesis 28, Sweet Scent 37, Aura Sphere 46, Worry Seed 55, Nature Power 64, Seed Flare 73, Sweet Kiss 82, Whirlwind 91, Aromatherapy 100.
- Added against today's: Earth Power 1; Air Slash 19; Aura Sphere 46; Nature Power 64; Whirlwind 91.
- Removed against today's: Growth 1; Leech Seed 19; Natural Gift 46; Energy Ball 73; Healing Wish 91.
- Moved against today's: Seed Flare 100 to 73; Aromatherapy 64 to 100.
- Against Kaizo's: the same.

**Arceus (493)**, 14 moves:

- New list: Seismic Toss 1, Hyper Beam 1, Roar of Time 1, Punishment 1, Seed Flare 10, Earth Power 20, Hyper Voice 30, Explosion 40, Magma Storm 50, Recover 60, Earthquake 70, ExtremeSpeed 80, Shadow Force 90, Judgment 100.
- Added against today's: Roar of Time 1; Seed Flare 10; Explosion 40; Magma Storm 50; Earthquake 70; Shadow Force 90.
- Removed against today's: Cosmic Power 1; Natural Gift 1; Gravity 10; Refresh 50; Future Sight 60; Perish Song 90.
- Moved against today's: Hyper Beam 80 to 1; Recover 70 to 60; ExtremeSpeed 40 to 80.
- Against Kaizo's: the same.

## New species, on their donor lists

**Alolan Ninetales**, 19 moves:

- New list: Dazzling Gleam 1, Nasty Plot 1, Spite 1, Icy Wind 1, Confuse Ray 1, Aurora Beam 1, Extrasensory 1, Ice Beam 1, Imprison 1, Mist 1, Aurora Veil 1, Sheer Cold 1, Grudge 1, Blizzard 1, Powder Snow 1, Tail Whip 1, Disable 1, Ice Shard 1, Safeguard 1.
- Moved against today's: Dazzling Gleam 1,1 to 1.
- Rule: Dazzling Gleam 1 listed twice; one kept.

**Galarian Rapidash**, 16 moves:

- New list: Psycho Cut 1, Megahorn 1, Tackle 1, Quick Attack 1, Growl 1, Tail Whip 1, Confusion 1, Fairy Wind 15, Agility 20, Psybeam 25, Stomp 30, Heal Pulse 35, Take Down 43, Dazzling Gleam 49, Psychic 56, Healing Wish 63.
- Moved against today's: Psycho Cut 1,1 to 1.
- Rule: Psycho Cut 1 listed twice; one kept.

**Galarian Mr Mime**, 24 moves:

- New list: Copycat 1, Encore 1, Role Play 1, Protect 1, Recycle 1, Mimic 1, Light Screen 1, Reflect 1, Safeguard 1, Dazzling Gleam 1, Pound 1, Rapid Spin 1, Baton Pass 1, Ice Shard 1, Confusion 12, Icy Wind 20, Double Kick 24, Psybeam 28, Hypnosis 32, Mirror Coat 36, Sucker Punch 40, Freeze-Dry 44, Psychic 48, Teeter Dance 52.
- Removed against today's: Misty Terrain 1; Ally Switch 16.
- Rule: Misty Terrain 1 out: the move pool's first cut.
- Rule: Ally Switch 16 out: the move pool's first cut.

**Mr Rime**, 28 moves:

- New list: Fake Tears 1, Slack Off 1, After You 1, Block 1, Copycat 1, Encore 1, Role Play 1, Protect 1, Recycle 1, Mimic 1, Light Screen 1, Reflect 1, Safeguard 1, Dazzling Gleam 1, Pound 1, Rapid Spin 1, Baton Pass 1, Ice Shard 1, Confusion 12, Icy Wind 20, Double Kick 24, Psybeam 28, Hypnosis 32, Mirror Coat 36, Sucker Punch 40, Freeze-Dry 44, Psychic 48, Teeter Dance 52.
- Removed against today's: Misty Terrain 1; Ally Switch 16.
- Rule: Misty Terrain 1 out: the move pool's first cut.
- Rule: Ally Switch 16 out: the move pool's first cut.

**Sylveon**, 23 moves:

- New list: Disarming Voice 1, Fairy Wind 1, Covet 1, Bite 1, Copycat 1, Baton Pass 1, Take Down 1, Charm 1, Double-Edge 1, Helping Hand 1, Tackle 1, Growl 1, Tail Whip 1, Sand-Attack 5, Quick Attack 11, Baby-Doll Eyes 12, Swift 18, Draining Kiss 25, Light Screen 28, Skill Swap 33, Moonblast 43, Psych Up 45, Last Resort 48.
- Removed against today's: Misty Terrain 32.
- Moved against today's: Disarming Voice 1,1 to 1; Fairy Wind 1,1 to 1.
- Rule: Misty Terrain 32 out: the move pool's first cut.
- Rule: Disarming Voice 1 listed twice; one kept.
- Rule: Fairy Wind 1 listed twice; one kept.

**Lopunny M**, 20 moves:

- New list: U-turn 1, Triple Axel 1, Mirror Coat 1, Pound 1, Foresight 1, Baby-Doll Eyes 13, Quick Attack 16, Dizzy Punch 20, Bounce 22, Jump Kick 25, Return 30, Charm 34, Fake Out 38, Copycat 42, Double-Edge 48, Close Combat 55, Hi Jump Kick 60, Teeter Dance 66, Last Resort 72, Encore 83.
- Removed against today's: Splash 1.
- Rule: Splash 1 out: Splash and Teleport go.

**Swadloon**, 6 moves:

- New list: Protect 1, GrassWhistle 1, Tackle 1, String Shot 1, Bug Bite 1, Razor Leaf 1.
- Moved against today's: Protect 1,1 to 1.
- Rule: Protect 1 listed twice; one kept.

**Leavanny**, 16 moves:

- New list: Slash 1, False Swipe 1, Tackle 1, String Shot 1, Bug Bite 1, Razor Leaf 1, Bug Bite 8, Razor Leaf 15, Struggle Bug 22, Fell Stinger 29, Helping Hand 32, Leaf Blade 36, X-Scissor 39, Entrainment 43, Swords Dance 46, Leaf Storm 50.
- Moved against today's: Slash 1,1 to 1.
- Rule: Slash 1 listed twice; one kept.

**Cofagrigus**, 22 moves:

- New list: Shadow Claw 1, Scary Face 1, Astonish 1, Protect 1, Haze 1, Night Shade 1, Disable 1, Disable 8, Haze 9, Night Shade 13, Will-O-Wisp 18, Crafty Shield 20, Hex 20, Ominous Wind 25, Curse 33, Mean Look 38, Grudge 38, Shadow Ball 41, Power Split 45, Guard Split 45, Dark Pulse 50, Destiny Bond 59.
- Moved against today's: Shadow Claw 1,1 to 1; Scary Face 1,1 to 1.
- Rule: Shadow Claw 1 listed twice; one kept.
- Rule: Scary Face 1 listed twice; one kept.

**Gothita**, 19 moves:

- New list: Pound 1, Confusion 1, Confusion 3, Play Nice 5, Tickle 7, Psybeam 13, DoubleSlap 14, Fake Tears 19, Embargo 19, Psyshock 22, Hypnosis 24, Faint Attack 24, Charm 30, Psych Up 33, Heal Block 33, Flatter 34, Psychic 36, Future Sight 37, Magic Room 48.
- Removed against today's: Telekinesis 40.
- Rule: Telekinesis 40 out: the move pool's first cut.

**Gothorita**, 20 moves:

- New list: Pound 1, Confusion 1, Play Nice 1, Tickle 1, Confusion 3, Tickle 7, Psybeam 13, DoubleSlap 14, Fake Tears 19, Embargo 19, Psyshock 22, Hypnosis 24, Faint Attack 24, Charm 31, Heal Block 34, Psych Up 35, Flatter 37, Psychic 39, Future Sight 42, Magic Room 55.
- Removed against today's: Telekinesis 43.
- Rule: Telekinesis 43 out: the move pool's first cut.

**Gothitelle**, 20 moves:

- New list: Pound 1, Confusion 1, Play Nice 1, Tickle 1, Confusion 3, Tickle 7, Psybeam 13, DoubleSlap 14, Fake Tears 19, Embargo 19, Psyshock 22, Hypnosis 24, Faint Attack 24, Charm 33, Heal Block 34, Psych Up 35, Flatter 38, Psychic 39, Future Sight 44, Magic Room 61.
- Removed against today's: Telekinesis 45.
- Rule: Telekinesis 45 out: the move pool's first cut.

**Mandibuzz**, 28 moves:

- New list: Bone Rush 1, Sky Attack 1, Toxic 1, Gust 1, Leer 1, Flatter 1, Pluck 1, Mirror Move 1, Brave Bird 1, Whirlwind 1, Fury Attack 1, Fury Attack 5, Pluck 10, Flatter 19, Faint Attack 23, Knock Off 24, Tailwind 26, Punishment 28, Iron Defense 30, Nasty Plot 36, Air Slash 41, Whirlwind 45, Dark Pulse 47, Defog 49, Embargo 50, Mirror Move 70, Attract 72, Brave Bird 72.
- Moved against today's: Bone Rush 1,1 to 1.
- Rule: Bone Rush 1 listed twice; one kept.

**Delphox**, 24 moves:

- New list: Burn Up 1, Shadow Ball 1, Psych Up 1, Recycle 1, Wish 1, Scratch 1, Tail Whip 1, Ember 5, Role Play 9, Psybeam 13, Lucky Chant 19, Light Screen 24, Flame Burst 29, Psyshock 34, Mystical Fire 36, Hypnosis 40, Will-O-Wisp 45, Flamethrower 51, Psychic 55, Magic Room 61, Future Sight 64, Overheat 66, Expanding Force 72, Encore 82.
- Removed against today's: Teleport 1.
- Rule: Teleport 1 out: Splash and Teleport go.

**Florges**, 19 moves:

- New list: Energy Ball 1, Grass Knot 1, Defog 1, Wish 1, Fairy Wind 1, Absorb 1, Lucky Chant 1, Tearful Look 6, Covet 10, Mega Drain 15, Draining Kiss 21, Magical Leaf 24, Aromatherapy 26, Giga Drain 31, Dazzling Gleam 37, Helping Hand 42, Synthesis 48, SolarBeam 53, Moonblast 57.
- Removed against today's: Flower Shield 1.
- Rule: Flower Shield 1 out: the move pool's first cut.

**Hisuian Sliggoo**, 13 moves:

- New list: Shelter 1, Absorb 1, Acid Armor 1, DragonBreath 1, Tackle 1, Water Gun 1, Protect 15, Flail 20, Water Pulse 25, Dragon Pulse 35, Curse 43, Iron Head 49, Muddy Water 56.
- Removed against today's: Rain Dance 30.
- Moved against today's: Shelter 1,1 to 1.
- Rule: Rain Dance 30 out: a weather move.
- Rule: Shelter 1 listed twice; one kept.

**Klefki**, 19 moves:

- New list: Astonish 1, Tackle 1, Tackle 4, Fairy Wind 6, Astonish 8, Spikes 15, Metal Sound 16, Crafty Shield 19, Torment 21, Draining Kiss 21, Recycle 33, Imprison 33, Mirror Shot 34, Flash Cannon 36, Foul Play 38, Play Rough 41, Magic Room 44, Heal Block 50, Last Resort 52.
- Removed against today's: Fairy Lock 1.
- Rule: Fairy Lock 1 out: the move pool's first cut.

**Xerneas**, 23 moves:

- New list: Tackle 1, Gravity 1, Heal Pulse 1, Aromatherapy 1, Ingrain 1, Take Down 1, Light Screen 5, Aurora Beam 10, Gravity 18, Aromatherapy 25, Night Slash 34, Nature Power 41, Geomancy 41, Psych Up 43, Horn Leech 44, Ingrain 45, Moonblast 48, Take Down 50, Megahorn 57, Heal Pulse 65, Close Combat 77, Outrage 86, Giga Impact 86.
- Removed against today's: Misty Terrain 50.
- Rule: Misty Terrain 50 out: the move pool's first cut.

**Zygarde 10**, 20 moves:

- New list: Thousand Arrows 1, Thousand Waves 1, Core Enforcer 1, Bind 1, Bulldoze 1, DragonBreath 1, Bite 1, Glare 1, Dig 13, Safeguard 15, Bind 18, Haze 24, Land’s Wrath 37, Crunch 40, Dragon Pulse 50, Glare 56, Camouflage 59, Earthquake 68, Coil 72, Outrage 84.
- Removed against today's: Sandstorm 50.
- Rule: Sandstorm 50 out: a weather move.

**Zygarde 50**, 20 moves:

- New list: Thousand Arrows 1, Thousand Waves 1, Core Enforcer 1, Bind 1, Bulldoze 1, DragonBreath 1, Bite 1, Glare 1, Dig 13, Safeguard 15, Bind 18, Haze 24, Land’s Wrath 37, Crunch 40, Dragon Pulse 50, Glare 56, Camouflage 59, Earthquake 68, Coil 72, Outrage 84.
- Removed against today's: Sandstorm 50.
- Rule: Sandstorm 50 out: a weather move.

**Toxapex**, 18 moves:

- New list: Baneful Bunker 1, Poison Sting 1, Peck 1, Wide Guard 1, Bite 1, Toxic Spikes 1, Peck 5, Bite 9, Wide Guard 17, Venoshock 19, Toxic Spikes 22, Recover 26, Spike Cannon 29, Pin Missile 37, Toxic 39, Venom Drench 42, Poison Jab 43, Liquidation 45.
- Moved against today's: Baneful Bunker 1,1 to 1.
- Rule: Baneful Bunker 1 listed twice; one kept.

**Fomantis**, 12 moves:

- New list: Leafage 1, Fury Cutter 1, Leafage 5, Growth 9, Razor Leaf 12, Ingrain 14, Sweet Scent 27, Slash 28, X-Scissor 30, Synthesis 31, Leaf Blade 32, SolarBeam 45.
- Removed against today's: Sunny Day 45.
- Rule: Sunny Day 45 out: a weather move.

**Lurantis**, 20 moves:

- New list: Petal Blizzard 1, Night Slash 1, SolarBeam 1, Dual Chop 1, Leafage 1, Fury Cutter 1, Growth 1, Ingrain 1, X-Scissor 1, Razor Leaf 1, Leafage 5, Razor Leaf 12, Growth 14, Ingrain 19, Slash 28, Sweet Scent 29, X-Scissor 30, Synthesis 32, Leaf Blade 34, Solar Blade 55.
- Removed against today's: Sunny Day 52.
- Moved against today's: Petal Blizzard 1,1 to 1.
- Rule: Sunny Day 52 out: a weather move.
- Rule: Petal Blizzard 1 listed twice; one kept.

**Bounsweet**, 8 moves:

- New list: Leafage 1, Play Nice 5, Rapid Spin 9, Razor Leaf 12, Sweet Scent 17, Magical Leaf 21, Teeter Dance 23, Flail 29.
- Added against today's: Leafage 1.
- Removed against today's: Splash 1; Aromatic Mist 33.
- Rule: Splash 1 out: Splash and Teleport go.
- Rule: Aromatic Mist 33 out: the move pool's first cut.
- Rule: Leafage at 1, the balance track's pick, in place of Splash or Teleport.

**Steenee**, 10 moves:

- New list: DoubleSlap 1, Play Nice 5, Rapid Spin 9, Razor Leaf 12, Sweet Scent 17, Magical Leaf 21, Teeter Dance 23, Stomp 25, Aromatherapy 38, Leaf Storm 44.
- Removed against today's: Aromatic Mist 32.
- Rule: Aromatic Mist 32 out: the move pool's first cut.

**Sandygast**, 13 moves:

- New list: Absorb 1, Harden 1, Astonish 5, Sand Tomb 11, Sand-Attack 14, Mega Drain 16, Bulldoze 24, Hypnosis 28, Giga Drain 35, Iron Defense 36, Shadow Ball 43, Earth Power 47, Shore Up 52.
- Removed against today's: Sandstorm 57.
- Rule: Sandstorm 57 out: a weather move.

**Palossand**, 16 moves:

- New list: Absorb 1, Harden 1, Astonish 1, Sand Tomb 1, Sand-Attack 1, Astonish 5, Sand-Attack 14, Sand Tomb 14, Mega Drain 16, Bulldoze 24, Hypnosis 28, Giga Drain 35, Iron Defense 36, Shadow Ball 44, Earth Power 50, Shore Up 57.
- Removed against today's: Sandstorm 64.
- Rule: Sandstorm 64 out: a weather move.

**Tapu Koko**, 16 moves:

- New list: Quick Attack 1, ThunderShock 1, Withdraw 5, Fairy Wind 10, False Swipe 15, Spark 20, Shock Wave 25, Charge 30, Agility 35, Screech 40, Discharge 45, Mean Look 50, Nature’sMadness 55, Wild Charge 60, Brave Bird 65, Power Swap 70.
- Removed against today's: ElectricTerrain 75.
- Rule: ElectricTerrain 75 out: the move pool's first cut.

**Tapu Lele**, 15 moves:

- New list: Astonish 1, Confusion 1, Withdraw 5, Aromatherapy 10, Draining Kiss 15, Psybeam 20, Flatter 25, Sweet Scent 35, Extrasensory 40, Psyshock 45, Mean Look 50, Nature’sMadness 55, Moonblast 60, Tickle 65, Skill Swap 70.
- Removed against today's: Aromatic Mist 30; Psychic Terrain 75.
- Rule: Aromatic Mist 30 out: the move pool's first cut.
- Rule: Psychic Terrain 75 out: the move pool's first cut.

**Tapu Bulu**, 16 moves:

- New list: Leafage 1, Rock Smash 1, Withdraw 5, Disable 10, Leech Seed 15, Mega Drain 20, Whirlwind 25, Horn Attack 30, Scary Face 35, Horn Leech 40, Zen Headbutt 45, Mean Look 50, Nature’sMadness 55, Wood Hammer 60, Megahorn 65, Skull Bash 70.
- Removed against today's: Grassy Terrain 75.
- Rule: Grassy Terrain 75 out: the move pool's first cut.

**Tapu Fini**, 17 moves:

- New list: Disarming Voice 1, Water Gun 1, Withdraw 5, Mist 10, Haze 10, Aqua Ring 15, Water Pulse 20, Brine 25, Defog 30, Heal Pulse 35, Surf 40, Muddy Water 45, Mean Look 50, Nature’sMadness 55, Moonblast 60, Hydro Pump 65, Soak 70.
- Removed against today's: Misty Terrain 75.
- Rule: Misty Terrain 75 out: the move pool's first cut.

**Pheromosa**, 15 moves:

- New list: Feint 1, Rapid Spin 1, Leer 5, Quick Guard 10, Bug Bite 15, Low Kick 20, Double Kick 25, Triple Kick 30, Stomp 35, Agility 40, Lunge 45, Bounce 50, Bug Buzz 60, Quiver Dance 65, Hi Jump Kick 70.
- Removed against today's: Speed Swap 55.
- Rule: Speed Swap 55 out: the move pool's first cut.

**Xurkitree**, 15 moves:

- New list: Wrap 1, ThunderShock 1, Charge 5, Thunder Wave 10, Ingrain 15, Spark 20, Shock Wave 25, Hypnosis 30, Eerie Impulse 35, ThunderPunch 40, Discharge 45, Magnet Rise 50, Thunderbolt 55, Power Whip 65, Zap Cannon 70.
- Removed against today's: ElectricTerrain 60.
- Rule: ElectricTerrain 60 out: the move pool's first cut.

**Magearna**, 16 moves:

- New list: Gyro Ball 1, Helping Hand 1, Defense Curl 6, Rollout 12, Iron Defense 18, Psybeam 30, Aurora Beam 36, Lock-On 42, Shift Gear 48, Trick 54, Iron Head 60, Aura Sphere 66, Flash Cannon 72, Pain Split 78, Zap Cannon 84, Fleur Cannon 90.
- Removed against today's: Magnetic Flux 24.
- Rule: Magnetic Flux 24 out: the move pool's first cut.

**Naganadel**, 17 moves:

- New list: Air Cutter 1, Air Slash 1, Dragon Pulse 1, Peck 1, Growl 1, Helping Hand 1, Acid 1, Fury Attack 7, Fell Stinger 14, Charm 21, Venoshock 28, Venom Drench 35, Nasty Plot 42, Poison Jab 49, Gastro Acid 56, Toxic 63, Dragon Rush 70.
- Moved against today's: Air Cutter 1,1 to 1.
- Rule: Air Cutter 1 listed twice; one kept.

**Grapploct**, 13 moves:

- New list: Octolock 1, Octazooka 1, Rock Smash 1, Leer 1, Feint 1, Bind 1, Detect 15, Brick Break 20, Bulk Up 25, Submission 30, Taunt 35, Reversal 40, Superpower 45.
- Removed against today's: Topsy-Turvy 50.
- Rule: Topsy-Turvy 50 out: the move pool's first cut.

**Sinistea**, 11 moves:

- New list: Astonish 1, Withdraw 1, Mega Drain 12, Protect 18, Sucker Punch 24, Aromatherapy 30, Giga Drain 36, Nasty Plot 42, Shadow Ball 48, Memento 54, Shell Smash 60.
- Removed against today's: Aromatic Mist 6.
- Rule: Aromatic Mist 6 out: the move pool's first cut.

**Polteageist**, 14 moves:

- New list: Teatime 1, Strength Sap 1, Astonish 1, Withdraw 1, Mega Drain 1, Protect 18, Sucker Punch 24, Aromatherapy 30, Giga Drain 36, Nasty Plot 42, Shadow Ball 48, Memento 54, Shell Smash 60, Curse 66.
- Removed against today's: Aromatic Mist 1.
- Rule: Aromatic Mist 1 out: the move pool's first cut.

**Frosmoth**, 17 moves:

- New list: Icy Wind 1, Powder Snow 1, Struggle Bug 1, Helping Hand 1, Attract 1, Stun Spore 4, Infestation 8, Mist 12, Defog 16, FeatherDance 21, Aurora Beam 24, Bug Buzz 32, Aurora Veil 36, Blizzard 40, Tailwind 44, Wide Guard 48, Quiver Dance 52.
- Removed against today's: Hail 28.
- Rule: Hail 28 out: a weather move.

**Smoliv**, 12 moves:

- New list: Tackle 1, Sweet Scent 1, Absorb 5, Growth 7, Razor Leaf 10, Helping Hand 13, Flail 16, Mega Drain 20, Seed Bomb 27, Energy Ball 30, Leech Seed 34, Terrain Pulse 38.
- Removed against today's: Grassy Terrain 23.
- Rule: Grassy Terrain 23 out: the move pool's first cut.

**Dolliv**, 12 moves:

- New list: Tackle 1, Sweet Scent 1, Absorb 5, Growth 7, Razor Leaf 10, Helping Hand 13, Flail 16, Mega Drain 20, Seed Bomb 29, Energy Ball 34, Leech Seed 37, Terrain Pulse 42.
- Removed against today's: Grassy Terrain 23.
- Rule: Grassy Terrain 23 out: the move pool's first cut.

**Arboliva**, 16 moves:

- New list: Sweet Scent 1, Mirror Coat 1, Safeguard 1, Tackle 1, Absorb 5, Growth 7, Razor Leaf 10, Helping Hand 13, Flail 16, Mega Drain 20, Seed Bomb 29, Energy Ball 34, Leech Seed 39, Terrain Pulse 46, Petal Blizzard 52, Petal Dance 58.
- Removed against today's: Grassy Terrain 23.
- Rule: Grassy Terrain 23 out: the move pool's first cut.

**Armarouge**, 17 moves:

- New list: Psyshock 1, Leer 1, Ember 1, Mystical Fire 1, Astonish 1, Wide Guard 1, Clear Smog 8, Fire Spin 12, Will-O-Wisp 16, Night Shade 20, Flame Charge 24, Incinerate 28, Lava Plume 32, Calm Mind 37, Flamethrower 48, Expanding Force 56, Armor Cannon 62.
- Removed against today's: Ally Switch 42.
- Rule: Ally Switch 42 out: the move pool's first cut.

**Ceruledge**, 19 moves:

- New list: Night Slash 1, Shadow Sneak 1, Quick Guard 1, Solar Blade 1, Shadow Claw 1, Leer 1, Ember 1, Astonish 1, Clear Smog 8, Fire Spin 12, Will-O-Wisp 16, Night Shade 20, Flame Charge 24, Incinerate 28, Lava Plume 32, Swords Dance 37, Bitter Blade 48, Psycho Cut 56, Flare Blitz 62.
- Removed against today's: Ally Switch 42.
- Moved against today's: Night Slash 1,1 to 1; Shadow Sneak 1,1 to 1; Quick Guard 1,1 to 1; Solar Blade 1,1 to 1.
- Rule: Ally Switch 42 out: the move pool's first cut.
- Rule: Night Slash 1 listed twice; one kept.
- Rule: Shadow Sneak 1 listed twice; one kept.
- Rule: Quick Guard 1 listed twice; one kept.
- Rule: Solar Blade 1 listed twice; one kept.

**Glimmet**, 13 moves:

- New list: Rock Throw 1, Harden 1, Smack Down 1, Acid Spray 7, AncientPower 11, Rock Polish 15, Stealth Rock 18, Venoshock 22, Selfdestruct 29, Rock Slide 33, Power Gem 37, Acid Armor 41, Sludge Wave 46.
- Removed against today's: Sandstorm 26.
- Rule: Sandstorm 26 out: a weather move.

**Glimmora**, 16 moves:

- New list: Mortal Spin 1, Smack Down 1, Spiky Shield 1, Toxic Spikes 1, Rock Throw 1, Harden 1, Acid Spray 7, AncientPower 11, Rock Polish 15, Stealth Rock 18, Venoshock 22, Selfdestruct 29, Rock Slide 33, Power Gem 39, Acid Armor 44, Sludge Wave 50.
- Removed against today's: Sandstorm 26.
- Rule: Sandstorm 26 out: a weather move.

## Magikarp, off the pick-list

**Magikarp**, 2 moves:

- New list: Tackle 1, Flail 30.
- Removed against today's: Splash 1.
- Moved against today's: Tackle 15 to 1.
- Rule: Splash 1 out: Splash and Teleport go.
- Rule: Tackle at 1, the balance track's pick, in place of Splash or Teleport (was at 15).

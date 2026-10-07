# The comb: Volkner's split

**Every trainer of Volkner's split is now combed.** Volkner and his two Ace
Trainers were combed earlier. On 2026-10-07 the 18 ordinary trainers were
added in walking order: eleven on Route 222, Poke Kid Janet in its west
house, and six in Sunyshore's gym. Every file passes the checker and the rule
audit; the checker's only lines are moves outside the species' lists, which
Ian's late-game ruling allows from the Galactic split on.

The ordinary trainers follow Ian's ruling of 2026-10-07. Each takes Kaizo's
idea where Kaizo has the trainer (its Route 222 is a run of sunny multi
battles, here singles), moves it into Oxide's Generation 5+ pool, then scales
it to the dial. With the lists lifted, modern moves are chosen where they do
the job: Scald, Psyshock, Liquidation, Flip Turn, Hurricane, Nuzzle, Zing Zap,
Volt Switch, Sacred Sword, Moonblast and the like.

| Check | Result |
|---|---|
| Single battles read blind (18) | 93 to 99 won, mean 96.7 |
| Clean, in the scorer's terms (Ian's band 80 to 85) | 67 to 79, mean 73 |
| Faints a fight, in the scorer's terms (Ian's band 0.1 to 0.25) | 0.5 to 0.9, mean 0.73 |
| Move slots that are Generation 5+ | 66 of 288, 23 percent |
| Hidden abilities | 17, on 12 of 18 teams |
| Element 7 items held | 4: two Rocky Helmets, an Assault Vest and a Punching Glove |

Every team carries at least one modern move. As in Candice's split, the
ordinary trainers win as often as Ian asks but cost about three times his
band in faints. Two rounds of softening took the faints from about 1.8 to 1.2
in my simulator: most members sit at 63 to 64, and the member at 66 or 67 is
a supporting one. The box at 68 knows no TMs, which overstates them. Beauty
Nicola holds the Pixie Plate she awards. Rich Boy Trey's Sunny Day is the
route's one weather team, as the dial allows.

Sailor Luther, the only path trainer before the gym, previews Volkner's
paralysis alone, and School Kid Tiera in the gym's first room previews his
Volt Switch alone. The later rooms pair two of his tools each: hazards,
paralysis, Volt Switch, Will-O-Wisp and the Life Orb. Hazards appear on
three of the eighteen (Marc's Toxic Spikes, Preston's Stealth Rock and
Lonnie's Spikes), about one in six as the dial asks.

## Volkner and his Ace Trainers, combed earlier

**Refreshed 2026-10-07.** The expected numbers were read again after two
changes: a fix to my simulator, which had picked the player's lead by party
order when two choices looked equal and so skewed every earlier boss reading,
and the legality sweep against the final lists (origin/balance-tm-pass at
377312dbf0), which left this split unchanged. Ian ruled that every draft goes into step 12 as
drafted; the scorer's step 15 reading gives the real numbers, and he chooses
any retunes from them. My candidates are in `../retune-proposals-not-approved/`.

The bosses of Volkner's split are combed: Ace Trainers Zachery and Destiny in
Sunyshore's gym, and Volkner. All three files pass the checker and the rule
audit.

The cap is 68, and no map here has its own weather. My simulator reads the
bosses against the scorer's box at this split, which knows no TMs, and under
Ian's move reworks of 2026-10-06, so they read harsher than they will once
the TM pass lands. Volkner reads about 97 won with 2.6 faints to today's 100
with 0.6. His two Ace Trainers sit three under the cap with sharper sets, as
Ian's rule on levels asks. No conditional
attack appears. Ian allowed two or three legendaries per boss from Cyrus 3 on
(2026-10-06); Volkner already reads a step harder than today's without one,
so he carries none.

## Decisions for Ian

| # | Decision | What the files do today | How it is checked | What Ian decides |
|---|---|---|---|---|
| 1 | Volkner without rain or Choice items | Today's Volkner has a Damp Rock Rain Dance and three Choice items. Here Forretress leads with Stealth Rock and Spikes behind a Focus Sash and pivots out with Volt Switch, as the dial asks of him (paralysis on several members, Volt Switch); it is a Steel and Bug type carrying an Electric move, under Ian's gym-theme rule. Jolteon, Lanturn and Magnezone carry Thunder Wave, Rotom Volt Switch and Will-O-Wisp, and a Life Orb Electivire is the ace. | `leader_volkner.json`; the scorer's reading later. | Accept (recommended), or bring back the rain on Jolteon's Damp Rock. |

| 2 | Ordinary trainers past the band | They win 93 to 99 percent blind, but cost about 0.73 Pokemon a fight in the scorer's terms against Ian's 0.1 to 0.25. | The scorer's step 15 reading, with a box that knows TMs. | Accept for now (recommended), or soften them further now. |

## What comes next

Barry's split's ordinary trainers.

## Overview

| Trainer | Place | Path | Battle | Size | Levels | The idea | Expected |
|---|---|---|---|---|---|---|---|
| Fisherman Brett | Route 222 | optional | single | 4 | 63 to 66 | Water and Electric | 97 / 0.90 / 46 blind in my simulator, about 78 clean in the scorer's terms |
| Fisherman Alec | Route 222 | optional | single | 4 | 63 to 66 | Today's Gyarados beside Kingdra's Flip Turn | 93 / 1.51 / 29 blind in my simulator, about 71 clean in the scorer's terms |
| Fisherman George | Route 222 | optional | single | 4 | 63 to 66 | Politoed's Hypnosis and Encore | 99 / 0.76 / 46 blind in my simulator, about 78 clean in the scorer's terms |
| Fisherman Cole | Route 222 | optional | single | 4 | 63 to 66 | Special Water types | 98 / 1.44 / 25 blind in my simulator, about 70 clean in the scorer's terms |
| Sailor Luther | Route 222 | on the path | single | 4 | 63 to 66 | Thunder Wave from Electrode | 98 / 0.80 / 48 blind in my simulator, about 79 clean in the scorer's terms |
| Policeman Thomas | Route 222 | optional | single | 4 | 63 to 66 | Kaizo's Policeman Thomas | 99 / 1.30 / 21 blind in my simulator, about 68 clean in the scorer's terms |
| Rich Boy Trey | Route 222 | optional | single | 4 | 63 to 66 | Sun | 98 / 1.24 / 25 blind in my simulator, about 70 clean in the scorer's terms |
| Sailor Marc | Route 222 | optional | single | 4 | 63 to 66 | Toxic Spikes from Tentacruel | 98 / 1.35 / 27 blind in my simulator, about 71 clean in the scorer's terms |
| Tuber Conner | Route 222 | optional | single | 4 | 63 to 66 | Water bulk | 96 / 1.54 / 24 blind in my simulator, about 69 clean in the scorer's terms |
| Tuber Holly | Route 222 | optional | single | 4 | 63 to 66 | Kaizo's level-100 joke of one-hit KO moves grown up | 98 / 1.55 / 19 blind in my simulator, about 67 clean in the scorer's terms |
| Beauty Nicola | Route 222 | optional | single | 4 | 63 to 66 | Fairies | 93 / 1.35 / 37 blind in my simulator, about 75 clean in the scorer's terms |
| Poke Kid Janet | Route 222 west house | optional | single | 4 | 63 to 66 | Electric mice and Nuzzle | 99 / 0.90 / 40 blind in my simulator, about 76 clean in the scorer's terms |
| School Kid Tiera | Sunyshore Gym, room 1 | gym trainer | single | 4 | 64 to 67 | Volt Switch alone | 96 / 1.27 / 29 blind in my simulator, about 72 clean in the scorer's terms |
| Guitarist Jerry | Sunyshore Gym, room 2 | gym trainer | single | 4 | 64 to 67 | Volkner's Thunder Wave and Volt Switch together | 97 / 1.08 / 35 blind in my simulator, about 74 clean in the scorer's terms |
| Poke Kid Meghan | Sunyshore Gym, room 2 | gym trainer | single | 4 | 64 to 67 | Volkner's paralysis and Life Orb together | 95 / 0.89 / 48 blind in my simulator, about 79 clean in the scorer's terms |
| School Kid Forrest | Sunyshore Gym, room 2 | gym trainer | single | 4 | 64 to 67 | Volkner's Thunder Wave and Will-O-Wisp together | 97 / 1.36 / 19 blind in my simulator, about 68 clean in the scorer's terms |
| Guitarist Preston | Sunyshore Gym, room 3 | gym trainer | single | 4 | 63 to 67 | Volkner's Stealth Rock and Thunder Wave together | 93 / 1.45 / 29 blind in my simulator, about 72 clean in the scorer's terms |
| Guitarist Lonnie | Sunyshore Gym, room 3 | gym trainer | single | 4 | 64 to 67 | Volkner's Spikes and Volt Switch together | 96 / 1.09 / 39 blind in my simulator, about 76 clean in the scorer's terms |
| Ace Trainer Zachery | Sunyshore Gym | gym trainer | single, Ace Trainer | 6 | 63 to 65 | Electric types | about 99 / 1.0 / 20 with a planned six |
| Ace Trainer Destiny | Sunyshore Gym | gym trainer | single, Ace Trainer | 6 | 63 to 65 | Electric types | about 100 / 1.1 / 1 with a planned six |
| Volkner | Sunyshore Gym | on the path | single, boss | 6 | 67 to 68 | Paralysis and Volt Switch | about 97 / 2.6 / 0 in my simulator, where today's file reads 100 / 0.6 / 53 |

Expected numbers are won / faints a fight / clean in my simulator, beside
today's file where it was read. For an ordinary trainer the clean rate is also
given in the scorer's terms, by the calibration in `read_split.py`.

## The trainers

### Fisherman Brett: Route 222, optional, single, cap 68

Water and Electric: Lanturn's Thunder Wave and Scald, Qwilfish's Toxic, Golduck's Psyshock and Whiscash.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Lanturn | 63 | Leftovers | Volt Absorb | default | Scald, Discharge, Ice Beam, Thunder Wave |
| Whiscash | 63 | none | Hydration | default | Earthquake, Waterfall, Ice Beam, Aqua Tail |
| Golduck | 64 | Sitrus Berry | Cloud Nine | default | Scald, Psyshock, Ice Beam, Encore |
| Qwilfish | 66 | none | Intimidate | default | Poison Jab, Waterfall, Throat Chop, Toxic |

Today's team: Lanturn 59 (Discharge, Aqua Ring, Hydro Pump, Charge). Expected: 97 / 0.90 / 46 blind in my simulator, about 78 clean in the scorer's terms.

### Fisherman Alec: Route 222, optional, single, cap 68

Today's Gyarados beside Kingdra's Flip Turn, Sharpedo's Liquidation and Lumineon's Tailwind.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Gyarados | 63 | none | Intimidate | default | Waterfall, Earthquake, Ice Fang, Bounce |
| Kingdra | 63 | Leftovers | Sniper | default | Dragon Pulse, Scald, Ice Beam, Flip Turn |
| Sharpedo | 63 | Sitrus Berry | Tinted Lens | default | Crunch, Liquidation, Ice Fang, Aqua Jet |
| Lumineon | 66 | none | Water Veil | default | U-turn, Scald, Ice Beam, Tailwind |

Today's team: Gyarados 57 (Earthquake, Waterfall, Dragon Dance, Ice Fang), Gyarados 57 (Bounce, Iron Head, Aqua Tail, Stone Edge). Expected: 93 / 1.51 / 29 blind in my simulator, about 71 clean in the scorer's terms.

### Fisherman George: Route 222, optional, single, cap 68

Politoed's Hypnosis and Encore, an Unaware Quagsire with Recover, Ludicolo's Leech Seed and Lumineon's U-turn. Today's Perish Song is gone.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Lumineon | 63 | Sitrus Berry | Water Veil | default | U-turn, Scald, Ice Beam, Tailwind |
| Ludicolo | 64 | none | Own Tempo | default | Giga Drain, Scald, Ice Beam, Leech Seed |
| Quagsire | 64 | Leftovers | Unaware | default | Earthquake, Liquidation, Recover, Toxic |
| Politoed | 66 | none | Water Absorb | default | Scald, Ice Beam, Hypnosis, Encore |

Today's team: Politoed 58 (Perish Song, Swagger, Surf, Hyper Voice), Lumineon 58 (Aqua Ring, Whirlpool, U-turn, Bounce). Expected: 99 / 0.76 / 46 blind in my simulator, about 78 clean in the scorer's terms.

### Fisherman Cole: Route 222, optional, single, cap 68

Special Water types: Primarina's Sparkling Aria and Moonblast, Starmie's Psyshock, Octillery, and Wailord's Yawn and Body Press.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Starmie | 63 | none | Magic Guard | default | Scald, Psyshock, Ice Beam, Recover |
| Primarina | 63 | none | Liquid Voice | default | Moonblast, Sparkling Aria, Ice Beam, Encore |
| Octillery | 63 | none | Sniper | default | Scald, Ice Beam, Flamethrower, Energy Ball |
| Wailord | 66 | Leftovers | Water Veil | default | Ice Beam, Body Press, Yawn, Rest |

Today's team: Starmie 59 (Surf, Recover, Ice Beam, Confuse Ray). Expected: 98 / 1.44 / 25 blind in my simulator, about 70 clean in the scorer's terms.

### Sailor Luther: Route 222, on the path, single, cap 68

Thunder Wave from Electrode, previewing Volkner's paralysis alone, beside Pelipper's Hurricane and Tailwind, Huntail and Hariyama's Heavy Slam.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Pelipper | 63 | Sitrus Berry | Unburden | default | Hurricane, Scald, Roost, Tailwind |
| Huntail | 63 | none | Swift Swim | default | Waterfall, Sucker Punch, Ice Fang, Crunch |
| Hariyama | 64 | Leftovers | Thick Fat | default | Close Combat, Knock Off, Bullet Punch, Heavy Slam |
| Electrode | 66 | none | Soundproof | default | Thunder Wave, Thunderbolt, Foul Play, Electro Ball |

Today's team: Pelipper 56 (Swallow, Spit Up, Stockpile, Tailwind), Hariyama 56 (Bullet Punch, Ice Punch, Bulk Up, Close Combat), Huntail 56 (Dive, Crunch, Aqua Tail, Hydro Pump). Expected: 98 / 0.80 / 48 blind in my simulator, about 79 clean in the scorer's terms.

### Policeman Thomas: Route 222, optional, single, cap 68

Kaizo's Policeman Thomas: two Intimidates (Arcanine and an Assault Vest Granbull), Manectric's Volt Switch and Gallade's Sacred Sword.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Gallade | 63 | Leftovers | Justified | default | Sacred Sword, Psycho Cut, Leaf Blade, Shadow Sneak |
| Arcanine | 63 | Charcoal | Intimidate | default | Flare Blitz, ExtremeSpeed, Wild Charge, Close Combat |
| Manectric | 64 | none | Lightning Rod | default | Volt Switch, Thunderbolt, Flamethrower, Overheat |
| Granbull | 66 | Assault Vest | Intimidate | default | Play Rough, Crunch, Close Combat, Ice Fang |

Today's team: Noctowl 58 (Extrasensory, Hypnosis, Roost, Dream Eater), Gallade 58 (Night Slash, Drain Punch, Protect, Close Combat). Expected: 99 / 1.30 / 21 blind in my simulator, about 68 clean in the scorer's terms.

### Rich Boy Trey: Route 222, optional, single, cap 68

Sun, the route's one weather team, as Kaizo's route is sunny: Ninetales's Sunny Day on a Heat Rock, Charizard's Solar Beam in one turn, Shiftry's Fake Out and Grumpig.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Ninetales | 66 | Heat Rock | Magic Guard | default | Sunny Day, Flamethrower, Energy Ball, Will-O-Wisp |
| Shiftry | 64 | none | Chlorophyll | default | Leaf Blade, Sucker Punch, Knock Off, Fake Out |
| Grumpig | 64 | Sitrus Berry | Thick Fat | default | Psychic, Power Gem, Dazzling Gleam, Shadow Ball |
| Charizard | 63 | none | Blaze | default | Heat Wave, SolarBeam, Air Slash, Focus Blast |

Today's team: Luxray 57 (Thunder Fang, Crunch, Fire Fang, Superpower). Expected: 98 / 1.24 / 25 blind in my simulator, about 70 clean in the scorer's terms.

### Sailor Marc: Route 222, optional, single, cap 68

Toxic Spikes from Tentacruel, then Machamp's Punching Glove punches, a Sheer Force Kingler and Mantine's Hurricane.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Mantine | 63 | Leftovers | Water Absorb | default | Scald, Hurricane, Roost, Ice Beam |
| Machamp | 63 | Punching Glove | Steadfast | default | Close Combat, Knock Off, Bullet Punch, Ice Punch |
| Kingler | 64 | none | Sheer Force | default | Crabhammer, X-Scissor, Knock Off, Superpower |
| Tentacruel | 66 | Black Sludge | Clear Body | default | Toxic Spikes, Scald, Sludge Bomb, Rapid Spin |

Today's team: Mantine 58 (Confuse Ray, Ice Beam, Aqua Ring, Hydro Pump). Expected: 98 / 1.35 / 27 blind in my simulator, about 71 clean in the scorer's terms.

### Tuber Conner: Route 222, optional, single, cap 68

Water bulk: a Sap Sipper Azumarill, Wailord, Walrein's Yawn and Octillery's coverage.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Walrein | 63 | none | Filter | default | Ice Beam, Surf, Yawn, Body Slam |
| Octillery | 63 | none | Sniper | default | Scald, Ice Beam, Fire Blast, Gunk Shot |
| Wailord | 64 | Sitrus Berry | Water Veil | default | Water Spout, Ice Beam, Body Press, Rest |
| Azumarill | 66 | none | Sap Sipper | default | Liquidation, Play Rough, Aqua Jet, Knock Off |

Today's team: Octillery 58 (Wring Out, Signal Beam, Ice Beam, Hyper Beam). Expected: 96 / 1.54 / 24 blind in my simulator, about 69 clean in the scorer's terms.

### Tuber Holly: Route 222, optional, single, cap 68

Kaizo's level-100 joke of one-hit KO moves grown up: Kingdra's Flip Turn, Kingler's Crabhammer, Floatzel's Liquidation and Walrein.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Floatzel | 63 | none | Swift Swim | default | Liquidation, Ice Fang, Crunch, Aqua Jet |
| Kingler | 63 | Sitrus Berry | Hyper Cutter | default | Crabhammer, X-Scissor, Knock Off, Rock Slide |
| Kingdra | 63 | Leftovers | Sniper | default | Dragon Pulse, Scald, Ice Beam, Flip Turn |
| Walrein | 66 | none | Filter | default | Ice Beam, Surf, Body Slam, Aqua Tail |

Today's team: Kingdra 59 (Outrage, Iron Head, Dragon Dance, Waterfall). Expected: 98 / 1.55 / 19 blind in my simulator, about 67 clean in the scorer's terms.

### Beauty Nicola: Route 222, optional, single, cap 68

Fairies: a Gardevoir holding the Pixie Plate Nicola awards, Togekiss's Thunder Wave, Altaria's Will-O-Wisp and Lopunny's Fake Out.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Gardevoir | 63 | Pixie Plate | Trace | default | Moonblast, Psychic, Mystical Fire, Thunderbolt |
| Togekiss | 63 | Leftovers | Super Luck | default | Air Slash, Dazzling Gleam, Aura Sphere, Thunder Wave |
| Lopunny | 63 | Sitrus Berry | Scrappy | default | Fake Out, Return, Hi Jump Kick, U-turn |
| Altaria | 66 | none | Cloud Nine | default | Dazzling Gleam, Dragon Pulse, Roost, Will-O-Wisp |

Today's team: Lopunny 57 (Dizzy Punch, Quick Attack, Bounce, Charm). Expected: 93 / 1.35 / 37 blind in my simulator, about 75 clean in the scorer's terms.

### Poke Kid Janet: Route 222 west house, optional, single, cap 68

Electric mice and Nuzzle: a Light Ball Pikachu with Volt Tackle, a Rocky Helmet Togedemaru with Iron Barbs and Zing Zap, Plusle and Minun.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Plusle | 63 | none | Plus | default | Nuzzle, Thunderbolt, Encore, Alluring Voice |
| Minun | 63 | none | Volt Absorb | default | Thunderbolt, Icy Wind, Encore, Alluring Voice |
| Togedemaru | 64 | Rocky Helmet | Iron Barbs | default | Zing Zap, Iron Head, U-turn, Nuzzle |
| Pikachu | 66 | Light Ball | Lightning Rod | default | Volt Tackle, Surf, Grass Knot, Fake Out |

Today's team: Pikachu 57 (Rain Dance, Hidden Power, Light Screen, Thunder), Pikachu 57 (Substitute, Focus Punch, Fake Out, Volt Tackle). Expected: 99 / 0.90 / 40 blind in my simulator, about 76 clean in the scorer's terms.

### School Kid Tiera: Sunyshore Gym, room 1, gym trainer, single, cap 68

Volt Switch alone, from Pachirisu, beside Emolga's Acrobatics, Pawmot's punches and Raichu.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Pawmot | 64 | none | Volt Absorb | default | ThunderPunch, Close Combat, Mach Punch, Ice Punch |
| Raichu | 64 | none | Lightning Rod | default | Thunderbolt, Grass Knot, Surf, Focus Blast |
| Emolga | 64 | none | Motor Drive | default | Acrobatics, Thunderbolt, Air Slash, U-turn |
| Pachirisu | 67 | none | Adaptability | default | Volt Switch, Super Fang, Discharge, Seed Bomb |

Today's team: Pachirisu 59 (ThunderPunch, Super Fang, Seed Bomb, Sweet Kiss). Expected: 96 / 1.27 / 29 blind in my simulator, about 72 clean in the scorer's terms.

### Guitarist Jerry: Sunyshore Gym, room 2, gym trainer, single, cap 68

Volkner's Thunder Wave and Volt Switch together: Electrode, Manectric, a Compound Eyes Galvantula's Thunder and Magnezone.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Magnezone | 64 | Leftovers | Levitate | default | Flash Cannon, Thunderbolt, Discharge, Volt Switch |
| Galvantula | 64 | none | Compound Eyes | default | Thunder, Bug Buzz, Giga Drain, Thunder Wave |
| Manectric | 65 | none | Lightning Rod | default | Volt Switch, Thunderbolt, Flamethrower, Overheat |
| Electrode | 67 | none | Soundproof | default | Thunder Wave, Volt Switch, Thunderbolt, Foul Play |

Today's team: Electrode 60 (Thunderbolt, Thunder Wave, Explosion, Mirror Coat), Manectric 60 (Thunderbolt, Roar, Flamethrower, Hidden Power). Expected: 97 / 1.08 / 35 blind in my simulator, about 74 clean in the scorer's terms.

### Poke Kid Meghan: Sunyshore Gym, room 2, gym trainer, single, cap 68

Volkner's paralysis and Life Orb together: Plusle's and Minun's Nuzzle, Togedemaru's Zing Zap and a Life Orb Ampharos.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Ampharos | 64 | Life Orb | Static | default | Thunderbolt, Dragon Pulse, Power Gem, Focus Blast |
| Togedemaru | 65 | Sitrus Berry | Iron Barbs | default | Zing Zap, Iron Head, U-turn, Fake Out |
| Plusle | 65 | none | Plus | default | Nuzzle, Thunderbolt, Encore, Alluring Voice |
| Minun | 67 | none | Volt Absorb | default | Nuzzle, Thunderbolt, Encore, Icy Wind |

Today's team: Plusle 60 (Thunder, Signal Beam, Light Screen, Sweet Kiss), Minun 60 (Thunder, Fake Tears, Signal Beam, Sweet Kiss). Expected: 95 / 0.89 / 48 blind in my simulator, about 79 clean in the scorer's terms.

### School Kid Forrest: Sunyshore Gym, room 2, gym trainer, single, cap 68

Volkner's Thunder Wave and Will-O-Wisp together: Probopass, Rotom's Volt Switch, Slowking's Scald and Mr. Mime.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Rotom | 64 | none | Levitate | default | Will-O-Wisp, Thunderbolt, Shadow Ball, Volt Switch |
| Mr Mime | 64 | none | Filter | default | Psychic, Dazzling Gleam, Focus Blast, Encore |
| Slowking | 65 | none | Regenerator | default | Scald, Psychic, Slack Off, Ice Beam |
| Probopass | 67 | Leftovers | Solid Rock | default | Thunder Wave, Power Gem, Earth Power, Flash Cannon |

Today's team: Magneton 59 (Thunderbolt, Tri Attack, Flash Cannon). Expected: 97 / 1.36 / 19 blind in my simulator, about 68 clean in the scorer's terms.

### Guitarist Preston: Sunyshore Gym, room 3, gym trainer, single, cap 68

Volkner's Stealth Rock and Thunder Wave together: Golem's rocks and Bulldoze, Absol's Thunder Wave, Luxray and Lanturn's Volt Switch.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Lanturn | 64 | Leftovers | Volt Absorb | default | Scald, Discharge, Ice Beam, Volt Switch |
| Luxray | 63 | none | Reckless | default | Wild Charge, Crunch, Ice Fang, Play Rough |
| Absol | 65 | none | Super Luck | default | Knock Off, Sucker Punch, Psycho Cut, Thunder Wave |
| Golem | 67 | Sitrus Berry | Shell Armor | default | Stealth Rock, Bulldoze, Rock Slide, Sucker Punch |

Today's team: Ampharos 60 (Thunderbolt, Signal Beam, Light Screen, Power Gem). Expected: 93 / 1.45 / 29 blind in my simulator, about 72 clean in the scorer's terms.

### Guitarist Lonnie: Sunyshore Gym, room 3, gym trainer, single, cap 68

Volkner's Spikes and Volt Switch together: a Rocky Helmet Forretress, Jolteon's Thunder Wave, Electivire and Raichu.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Electivire | 64 | none | Vital Spirit | default | ThunderPunch, Ice Punch, Cross Chop, Earthquake |
| Raichu | 64 | none | Lightning Rod | default | Thunderbolt, Grass Knot, Surf, Focus Blast |
| Jolteon | 65 | none | Volt Absorb | default | Thunderbolt, Shadow Ball, Signal Beam, Thunder Wave |
| Forretress | 67 | Rocky Helmet | Heatproof | default | Spikes, Volt Switch, Gyro Ball, Rapid Spin |

Today's team: Raichu 60 (Thunderbolt, Grass Knot, Thunder Wave, Nasty Plot). Expected: 96 / 1.09 / 39 blind in my simulator, about 76 clean in the scorer's terms.

### Ace Trainer Zachery: Sunyshore Gym, gym trainer, single, Ace Trainer, cap 68

Electric types: Magnezone's Thunder Wave, Rotom's Will-O-Wisp, Ampharos's Light Screen, Manectric, a Galvantula behind a Focus Sash, and a Nasty Plot Raichu ace.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Magnezone | 64 | Shuca Berry | Levitate | Modest | Thunderbolt, Flash Cannon, Volt Switch, Thunder Wave |
| Rotom | 63 | Spooky Plate | Levitate | Timid | Thunderbolt, Shadow Ball, Will-O-Wisp, Volt Switch |
| Ampharos | 63 | Leftovers | Static | Modest | Thunderbolt, Dragon Pulse, Power Gem, Light Screen |
| Manectric | 63 | Life Orb | Lightning Rod | Timid | Thunderbolt, Flamethrower, Signal Beam, Crunch |
| Galvantula | 64 | Focus Sash | Compound Eyes | Timid | Thunderbolt, Bug Buzz, Energy Ball, Thunder Wave |
| Raichu | 65 | Lum Berry | Static | Timid | Thunderbolt, Focus Blast, Surf, Nasty Plot |

Today's team: Magnezone 60 (Thunderbolt, Flash Cannon, Tri Attack, Rain Dance), Rotom 60 (Thunderbolt, Shadow Ball, Light Screen, Will-O-Wisp). Expected: about 99 / 1.0 / 20 with a planned six; read blind, 40 / 4.5 / 4.

### Ace Trainer Destiny: Sunyshore Gym, gym trainer, single, Ace Trainer, cap 68

Electric types: Pachirisu's Super Fang and Thunder Wave, Jolteon, Luxray, Lanturn, Vikavolt and an Electivire ace.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Pachirisu | 63 | Sitrus Berry | Adaptability | Jolly | ThunderPunch, U-turn, Super Fang, Thunder Wave |
| Jolteon | 64 | Magnet | Volt Absorb | Timid | Thunderbolt, Shadow Ball, Signal Beam, Volt Switch |
| Luxray | 63 | Flame Orb | Guts | Adamant | Facade, Thunder Fang, Crunch, Superpower |
| Lanturn | 64 | Leftovers | Volt Absorb | Modest | Scald, Discharge, Ice Beam, Thunder Wave |
| Vikavolt | 63 | SilverPowder | Levitate | Modest | Thunderbolt, Bug Buzz, Energy Ball, Flash Cannon |
| Electivire | 65 | Life Orb | Adaptability | Adamant | ThunderPunch, Ice Punch, Cross Chop, Earthquake |

Today's team: Electivire 60 (ThunderPunch, Low Kick, Light Screen, Fire Punch), Jolteon 60 (Thunderbolt, Shadow Ball, Thunder Wave, Signal Beam). Expected: about 100 / 1.1 / 1 with a planned six; read blind, 32 / 5.1 / 0.

### Volkner: Sunyshore Gym, on the path, single, boss, cap 68

Paralysis and Volt Switch, as the dial asks of him: Forretress leads with Stealth Rock and Spikes behind a Focus Sash and pivots out with Volt Switch (an off-type member carrying an Electric move), then Jolteon, Lanturn and Magnezone with Thunder Wave, Rotom with Volt Switch and Will-O-Wisp, and a Life Orb Electivire ace.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Forretress | 67 | Focus Sash | Heatproof | Relaxed | Stealth Rock, Spikes, Volt Switch, Gyro Ball |
| Jolteon | 67 | Shuca Berry | Volt Absorb | Timid | Thunderbolt, Shadow Ball, Volt Switch, Thunder Wave |
| Lanturn | 67 | Leftovers | Volt Absorb | Modest | Scald, Discharge, Ice Beam, Thunder Wave |
| Rotom | 67 | Sitrus Berry | Levitate | Modest | Thunderbolt, Shadow Ball, Will-O-Wisp, Volt Switch |
| Magnezone | 67 | Shuca Berry | Levitate | Modest | Thunderbolt, Flash Cannon, Tri Attack, Thunder Wave |
| Electivire | 68 | Life Orb | Adaptability | Adamant | ThunderPunch, Ice Punch, Cross Chop, Earthquake |

Today's team: Jolteon 61 (Damp Rock; Thunder, Shadow Ball, Thunder Wave, Rain Dance), Rotom 61 (Leftovers; Thunder, Shadow Ball, Leaf Storm, Thunder Wave), Lanturn 61 (Focus Sash; Surf, Thunder, Ice Beam, Aqua Ring), Magnezone 61 (Choice Specs; Thunder, Tri Attack, Flash Cannon, Signal Beam), Luxray 61 (Choice Band; Ice Fang, Thunder Fang, Crunch, Superpower), Electivire 62 (Choice Scarf; ThunderPunch, Ice Punch, Cross Chop, Giga Impact). Expected: about 97 / 2.6 / 0 in my simulator, where today's file reads 100 / 0.6 / 53.


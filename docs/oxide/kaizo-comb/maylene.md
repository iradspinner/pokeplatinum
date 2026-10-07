# The comb: Maylene's split

**Every trainer of Maylene's split is now combed.** The bosses were combed
earlier: Barry 3, Ace Trainers Dennis and Maya, and Maylene. On 2026-10-07 I
added all 37 ordinary trainers, in walking order, among them Roughneck Rocco,
the Game Corner's new challenger. Rocco's file is from origin/balance-tm-pass
and has not reached oxide yet. Every file passes the checker and the rule
audit.

The ordinary trainers follow Ian's ruling of 2026-10-07. Each takes Kaizo's
idea where Kaizo has the trainer, moves it into Oxide's Generation 5+ pool
where the species' lists allow, then scales it to the dial. Before the
Galactic split the lists still bind, and most Generation 4 lines hold few
modern moves.

| Check | Result |
|---|---|
| Single battles read blind (29) | 94 to 100 won, mean 98.7 |
| Clean, in the scorer's terms (Ian's band 80 to 85) | 70 to 89, mean 80 |
| Faints a fight, in the scorer's terms (Ian's band 0.1 to 0.25) | 0.2 to 0.8, mean 0.47 |
| Doubles (6) and the Veilstone tag (2 files) | not readable yet |
| Move slots that are Generation 5+ | 65 of 484, 13 percent |
| Hidden abilities | 25, on 21 of 37 teams |
| Element 7 items held | 8: three Eviolites, an Assault Vest, Safety Goggles, a Rocky Helmet, a Roseli Berry and a Punching Glove |

So the ordinary trainers win as often as Ian asks but cost more Pokemon than
his band: about twice the faints. That leans toward his wish that ordinary
trainers be dangerous, and the scorer's step 15 reading decides any change.
Three optional trainers award an element 7 item: Kahlil (Safety Goggles), Ty
and Sue (Assault Vest) and Kati (Punching Glove). Each holds the item it
gives, and Raul's Swellow holds the Silk Scarf he awards.

Three teams carry no modern move although their species have one, each for a
reason:

| Team | Why no modern move |
|---|---|
| Jogger Richard | Electrode's only fitting one, Foul Play (95), is over the 90 ceiling on borrowed attacks before Byron's split. Wild Charge is physical on a special attacker. Stomping Tantrum is weaker than Dugtrio's Earthquake and Dodrio's Tri Attack. |
| Ruin Maniac Calvin | The fossils' only modern move is Meteor Beam (120), over the same ceiling. |
| Galactic Grunt (Veilstone, 2) | Venomoth's Psychic Noise and Skitter Smack are weaker than its Psychic and Signal Beam. Victreebel has none. |

My simulator gained the later items, the hidden abilities and the modern move
effects on 2026-10-07. It also had a bug: Fake Out worked on every turn
rather than only the first. The ordinary trainers were read after both
changes; the bosses' numbers below come from before them, and their re-read
follows.

## The bosses, combed earlier

**Refreshed 2026-10-07.** The expected numbers were read again after two
changes: a fix to my simulator, which had picked the player's lead by party
order when two choices looked equal and so skewed every earlier boss reading,
and the legality sweep against the final lists (origin/balance-tm-pass at
377312dbf0), which left this split unchanged. Ian ruled that every draft goes into step 12 as
drafted; the scorer's step 15 reading gives the real numbers, and he chooses
any retunes from them. My candidates are in `../retune-proposals-not-approved/`.

The bosses are Barry 3 (three files, one per starter), Ace Trainers Dennis
and Maya, and Maylene.

The cap is 39 throughout. Today's Barry 3 and Ace Trainers sit four to seven
levels under it (32 to 35); here every boss's ace stands at the cap and the
rest one or two under, as the dial's Rule 2 asks, and the Ace Trainers one
under.

My simulator reads them against the scorer's box at Maylene (box-after-fantina.md),
which knows no TMs, so these fights read harsher than they will once the TM
pass lands. Maylene now reads about 34 won to today's 96, far harder than the
step I aimed for, and Barry 3 about 98 won with three faints to today's 100
with none (84 in the Turtwig version). The Ace Trainers, which goal 3 reads with a planned six,
read 99 to 100 that way; met blind they lose about one fight in fifteen in my
simulator, which I leave as they are, since Ian asked that fights not be tuned
against a box without TMs. The blind pool at 39 is my own reckoning by the
scorer's rule, since the scoring track's pools stop at 33.

Route 215 fights in permanent rain (Ian, 2026-10-06: a map's weather is
battle weather for every fight on it), and Ace Trainers Dennis and Maya stand
there. Both already use it: Dennis's Floatzel has Swift Swim and moves at
double speed, and Maya's Gastrodon heals in rain through Dry Skin and
carries a rain-boosted Surf. In rain they read harder, Maya most of all, and
I leave both as they are, by the same reasoning as above:

| Ace Trainer | Planned six, clear | Planned six, rain | Blind, clear (scorer's terms) | Blind, rain (scorer's terms) |
|---|---|---|---|---|
| Dennis | 100 / 0.2 / 85 | 99.8 / 0.19 / 84 | 100 / 0.75 / 76 | 95 / 1.25 / 73 |
| Maya | 100 / 0.2 / 85 | 100 / 0.95 / 12 | 100 / 1.15 / 65 | 94 / 2.37 / 61 |

Route 215's ordinary trainers use the rain on three of six teams, as the
dial's half allows: Derek's Toxicroak heals through Dry Skin, Calvin's Kabutops
keeps Swift Swim, and Scott's Jolteon would have carried a sure-hitting Thunder
but for the ceiling. Swift Swim on Gregory's Poliwrath read 61 to 86 won, far
past the band, so it takes Water Absorb. The Lost Tower's 5F is in fog, but no
trainer stands there; no other map in this split has its own weather.

## Decisions for Ian

Ian answered the two boss decisions on 2026-10-06. Two new ones come from the
ordinary trainers. Glimmora is flagged off-theme, to revisit; from Wake's split on, every gym leader's members are of the gym's type or carry a move of it.

| # | Decision | What the files do today | How it is checked | What Ian decides |
|---|---|---|---|---|
| 1 | Maylene drops her rain (Ian: Glimmora stays for now but is off-theme for a Fighting gym, with no Fighting move; revisit later) | Today's Maylene opens with a Rain Dance Poliwrath on a Damp Rock; here a Glimmora leads with Stealth Rock behind a Focus Sash, since the dial keeps weather bosses to Gardenia's, Wake's and Candice's splits and the League. Heracross keeps the Flame Orb, Cacturne and Medicham stay, Toxicroak takes the Fake Out, and Lucario keeps its Black Belt with Vacuum Wave as the priority ace. | `leader_maylene.json`; the scorer's reading later. | Accept (recommended), or keep Poliwrath's rain beside the new lead. |
| 2 | Barry 3 leads with Fake Out (Ian: Ambipom stands) | The dial gives Barry a Fake Out lead from his third fight, so a Technician Ambipom joins Staraptor, Floatzel, Snorlax and his starter. Its Last Resort is the split's one conditional attack, exempt from the ceiling by Ian's ruling. | `rival_route_209_*.json`. | Accept (recommended). |
| 3 | Ordinary trainers a little past the band | They win 94 to 100 percent blind, but they cost about 0.47 Pokemon a fight in the scorer's terms against Ian's 0.1 to 0.25, mostly through one strong member each. | The scorer's step 15 reading. | Accept for now (recommended: Ian asked for dangerous ordinary trainers, and the scorer's numbers decide), or soften them now. |
| 4 | Rocco rebuilt | The TM pass's file (Persian, Clefable, Porygon2 at 37 to 38) gives Clefable Moonblast, which is not in its final lists. My version keeps the three species and the Game Corner's Metronome, and gives Porygon2 an Eviolite. It reads 99 won blind. | `game_corner_challenger.json`. | Accept (recommended), or keep the TM pass's file as it lands. |

## What comes next

The ordinary trainers of Wake's split, then each later split in turn.

## Overview

| Trainer | Place | Path | Battle | Size | Levels | The idea | Expected |
|---|---|---|---|---|---|---|---|
| Pkmn Breeder Albert | Route 209 | optional | single | 4 | 35 to 37 | Simple and Unaware | 99 / 1.00 / 37 blind in my simulator, about 75 clean in the scorer's terms |
| Pkmn Breeder Jennifer | Route 209 | on the path | single | 4 | 35 to 37 | Signature items | 100 / 0.61 / 47 blind in my simulator, about 79 clean in the scorer's terms |
| Cowgirl Shelley | Route 209 | optional | single | 4 | 35 to 37 | Ranch stock | 96 / 0.94 / 43 blind in my simulator, about 77 clean in the scorer's terms |
| Jogger Richard | Route 209 | optional | single | 3 | 36 to 37 | Speed | 100 / 0.39 / 62 blind in my simulator, about 85 clean in the scorer's terms |
| Poke Kid Danielle | Route 209 | optional | single | 3 | 35 to 37 | Cute items | 100 / 0.66 / 47 blind in my simulator, about 79 clean in the scorer's terms |
| Young Couple Ty and Sue | Route 209 | optional | double | 4 | 35 to 36 | Fake Out and an Assault Vest | not readable yet (a double) |
| Twins Emma and Lil | Route 209 | on the path | double | 4 | 35 to 36 | Fangs behind two Intimidates | not readable yet (a double) |
| Jogger Raul | Route 209 | optional | single | 3 | 36 to 37 | Normal speed | 100 / 0.51 / 56 blind in my simulator, about 82 clean in the scorer's terms |
| Barry 3 | Route 209, gate to Hearthome | on the path | single, boss | 5 | 37 to 39 | Barry's skeleton from his third fight | about 98 / 3.0 / 3 in my simulator, where today's file reads 100 / 0.0 / 100 |
| Youngster Oliver | Lost Tower 2F | optional | single | 4 | 35 to 38 | Quiver Dance | 100 / 0.35 / 74 blind in my simulator, about 89 clean in the scorer's terms |
| Roughneck Kirby | Lost Tower 3F | optional | single | 3 | 35 to 37 | Dark bruisers | 99 / 0.64 / 54 blind in my simulator, about 82 clean in the scorer's terms |
| Pokefan Leonard | Lost Tower 3F | optional | single | 4 | 35 to 37 | Electric mice | 98 / 0.56 / 66 blind in my simulator, about 87 clean in the scorer's terms |
| Pokefan Rebekah | Lost Tower 4F | optional | single | 3 | 35 to 37 | Rock Head | 100 / 0.56 / 49 blind in my simulator, about 80 clean in the scorer's terms |
| Belle and Pa Beth and Bob | Lost Tower 4F | optional | double | 3 | 35 to 36 | Sun | not readable yet (a double) |
| Young Couple Mike and Nat | Lost Tower 4F | optional | double | 4 | 35 to 37 | A spread Ground move beside immune partners | not readable yet (a double) |
| Ruin Maniac Karl | Solaceon Ruins | optional | single | 3 | 36 to 37 | Stealth Rock from Claydol | 98 / 0.63 / 64 blind in my simulator, about 86 clean in the scorer's terms |
| Pkmn Breeder Kahlil | Route 210 south | optional | single | 4 | 35 to 37 | Speed Boost Blaziken with Protect | 97 / 0.97 / 36 blind in my simulator, about 74 clean in the scorer's terms |
| Pkmn Breeder Amber | Route 210 south | optional | single | 3 | 35 to 37 | Healing Fairies | 100 / 0.65 / 51 blind in my simulator, about 81 clean in the scorer's terms |
| Twins Teri and Tia | Route 210 south | optional | double | 4 | 35 to 36 | Prankster speed | not readable yet (a double) |
| Belle and Pa Ava and Matt | Route 210 south | optional | double | 4 | 35 to 37 | Teeter Dance beside Own Tempo | not readable yet (a double) |
| Rancher Marco | Route 210 south | optional | single | 3 | 35 to 37 | Sheer Force | 100 / 0.74 / 46 blind in my simulator, about 79 clean in the scorer's terms |
| Jogger Wyatt | Route 210 south | optional | single | 3 | 36 to 37 | Fire and Electric speed | 100 / 0.82 / 41 blind in my simulator, about 76 clean in the scorer's terms |
| Black Belt Gregory | Route 215 (rain) | optional | single | 3 | 35 to 37 | Punches in the rain | 98 / 0.98 / 38 blind in my simulator in rain, about 75 clean in the scorer's terms |
| Black Belt Derek | Route 215 (rain) | optional | single | 3 | 35 to 37 | Dry Skin | 96 / 1.26 / 29 blind in my simulator in rain, about 72 clean in the scorer's terms |
| Black Belt Nathaniel | Route 215 (rain) | optional | single | 3 | 35 to 37 | Kicks | 99 / 0.95 / 42 blind in my simulator in rain, about 77 clean in the scorer's terms |
| Jogger Scott | Route 215 (rain) | optional | single | 3 | 36 to 38 | Spikes from Forretress on a Rocky Helmet | 100 / 0.43 / 67 blind in my simulator in rain, about 87 clean in the scorer's terms |
| Ace Trainer Dennis | Route 215 | on the path | single, Ace Trainer | 4 | 37 to 38 | Speed and coverage | about 100 / 0.2 / 83 with a planned six in rain |
| Ace Trainer Maya | Route 215 | on the path | single, Ace Trainer | 4 | 37 to 38 | Toxic Spikes from Roserade | about 100 / 0.9 / 13 with a planned six in rain |
| Ruin Maniac Calvin | Route 215 (rain) | optional | single | 4 | 35 to 37 | Fossils in the rain | 94 / 0.97 / 64 blind in my simulator in rain, about 86 clean in the scorer's terms |
| Jogger Craig | Route 215 (rain) | on the path | single | 3 | 35 to 37 | Stealth Rock from a fast Dugtrio | 100 / 0.94 / 44 blind in my simulator in rain, about 78 clean in the scorer's terms |
| Black Belt Colby | Veilstone Gym | gym trainer | single | 3 | 36 to 38 | Maylene's Fake Out and orb together | 100 / 0.83 / 49 blind in my simulator, about 80 clean in the scorer's terms |
| Black Belt Darren | Veilstone Gym | gym trainer | single | 3 | 36 to 37 | Maylene's Stealth Rock and priority together | 98 / 1.29 / 25 blind in my simulator, about 70 clean in the scorer's terms |
| Black Belt Rafael | Veilstone Gym | gym trainer | single | 3 | 37 to 38 | Maylene's orb and Revenge | 100 / 0.51 / 59 blind in my simulator, about 84 clean in the scorer's terms |
| Black Belt Jeffery | Veilstone Gym | gym trainer | single | 3 | 37 to 38 | Maylene's priority and resist berry | 98 / 1.02 / 42 blind in my simulator, about 77 clean in the scorer's terms |
| Maylene | Veilstone Gym | on the path | single, boss | 6 | 37 to 39 | A Stealth Rock lead with a Fake Out member behind it | about 34 / 5.3 / 0 in my simulator, where today's file reads 96 / 2.1 / 1 |
| Galactic Grunt (Veilstone, 1) | Veilstone City | on the path | tag beside Lucas or Dawn | 2 | 36 to 37 | Poison beside its partner | not readable yet (a tag battle) |
| Galactic Grunt (Veilstone, 2) | Veilstone City | on the path | tag beside Lucas or Dawn | 2 | 36 to 37 | Venomoth's Sleep Powder and Victreebel's Sucker Punch | not readable yet (a tag battle) |
| Collector Fernando | Veilstone cafe | optional | single | 3 | 35 to 37 | Few weaknesses | 97 / 0.94 / 39 blind in my simulator, about 76 clean in the scorer's terms |
| Collector Edwin | Veilstone cafe | optional | single | 3 | 35 to 37 | Rare and bulky | 100 / 1.06 / 40 blind in my simulator, about 76 clean in the scorer's terms |
| Waitress Kati | Veilstone cafe | optional | single | 3 | 35 to 37 | Punches | 99 / 0.84 / 45 blind in my simulator, about 78 clean in the scorer's terms |
| Roughneck Rocco | Veilstone Game Corner | optional | single | 3 | 37 | House odds | 99 / 0.55 / 56 blind in my simulator, about 83 clean in the scorer's terms |

Expected numbers are won / faints a fight / clean in my simulator, beside
today's file where it was read. For an ordinary trainer the clean rate is also
given in the scorer's terms, by the calibration in `read_split.py`.

## The trainers

### Pkmn Breeder Albert: Route 209, optional, single, cap 39

Simple and Unaware: Bibarel's Curse counts double behind Mr. Mime's screens, and Quagsire's Unaware ignores the player's own boosts. Kaizo's Simple family, with Dazzling Gleam on Mr. Mime.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Mr Mime | 35 | none | Filter | default | Reflect, Light Screen, Dazzling Gleam, Psybeam |
| Quagsire | 35 | Leftovers | Unaware | default | Earthquake, Waterfall, Yawn, Toxic |
| Bibarel | 36 | Sitrus Berry | Simple | Adamant | Curse, Hyper Fang, Aqua Tail, Aqua Jet |
| Slowbro | 37 | none | Regenerator | default | Psychic, Surf, Ice Beam, Thunder Wave |

Today's team: Budew 26 (Water Sport, Stun Spore, Giga Drain, Swift), Bonsly 26 (Rock Throw, Mimic, Block, Faint Attack), Pichu 26 (Tail Whip, Thunder Wave, Sweet Kiss, Volt Tackle), Eevee 26 (Headbutt, Dig, Yawn, Quick Attack). Expected: 99 / 1.00 / 37 blind in my simulator, about 75 clean in the scorer's terms.

### Pkmn Breeder Jennifer: Route 209, on the path, single, cap 39

Signature items: Marowak's Thick Club, Farfetch'd's Stick and an Eviolite Chansey, with Jynx's Fake Out previewing Maylene's alone. Kaizo's breeder of oddities, with the Eviolite and Stomping Tantrum.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Jynx | 35 | none | Dry Skin | default | Fake Out, Ice Beam, Psychic, Lovely Kiss |
| Chansey | 35 | Eviolite | Natural Cure | default | Softboiled, Toxic, Chilling Water, Light Screen |
| Farfetchd | 36 | Stick | Defiant | Adamant | Night Slash, Aerial Ace, Poison Jab, Knock Off |
| Marowak | 37 | Thick Club | Rock Head | default | Bonemerang, StompingTantrum, Rock Slide, Knock Off |

Today's team: Riolu 26 (Force Palm, Feint, Reversal, Screech), Smoochum 26 (Confusion, Sing, Mean Look, Fake Tears), Cleffa 26 (Sing, Sweet Kiss, Copycat, Magical Leaf), Eevee 26 (Headbutt, Dig, Yawn, Quick Attack). Expected: 100 / 0.61 / 47 blind in my simulator, about 79 clean in the scorer's terms.

### Cowgirl Shelley: Route 209, optional, single, cap 39

Ranch stock: Miltank's Curse behind Thick Fat, Rapidash's Flame Charge and Wild Charge, Ampharos's paralysis. Kaizo's cowgirl, with Play Rough, Wild Charge and Dazzling Gleam.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Ampharos | 35 | none | Static | default | Discharge, Dragon Pulse, Dazzling Gleam, Thunder Wave |
| Rapidash | 36 | Charcoal | Reckless | default | Flame Charge, Wild Charge, Megahorn, Poison Jab |
| Lickilicky | 35 | none | Poison Heal | default | Body Slam, Knock Off, Ice Beam, Thunderbolt |
| Miltank | 37 | Leftovers | Thick Fat | Impish | Curse, Body Slam, Milk Drink, Play Rough |

Today's team: Miltank 30 (Bide, Milk Drink, Body Slam, Zen Headbutt). Expected: 96 / 0.94 / 43 blind in my simulator, about 77 clean in the scorer's terms.

### Jogger Richard: Route 209, optional, single, cap 39

Speed: Dodrio's Tri Attack and Quick Attack, a Magnet Electrode and Dugtrio's Sucker Punch. Kaizo's trappers lose Arena Trap and Magnet Pull, which the dial keeps off ordinary trainers.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Electrode | 36 | Magnet | Static | Timid | Thunderbolt, Signal Beam, Charge Beam, Thunder Wave |
| Dugtrio | 37 | none | Sand Veil | default | Earthquake, Sucker Punch, Night Slash, Rock Slide |
| Dodrio | 37 | Sharp Beak | Quick Feet | Jolly | Tri Attack, Pluck, Knock Off, Quick Attack |

Today's team: Electabuzz 30 (Ice Punch, Low Kick, Light Screen, ThunderPunch). Expected: 100 / 0.39 / 62 blind in my simulator, about 85 clean in the scorer's terms.

### Poke Kid Danielle: Route 209, optional, single, cap 39

Cute items: a Light Ball Pikachu with Nasty Plot, an Eviolite Clefairy and a Huge Power Azumarill. Kaizo's level-1 Endeavor Pichu and Shadow Tag Ditto are gone, both barred.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Clefairy | 35 | Eviolite | Magic Guard | default | Alluring Voice, Thunder Wave, Wish, Icy Wind |
| Azumarill | 35 | none | Huge Power | default | Aqua Tail, Play Rough, Aqua Jet, Double-Edge |
| Pikachu | 37 | Light Ball | Reckless | Timid | Thunderbolt, Surf, Grass Knot, Nasty Plot |

Today's team: Clefable 30 (Sing, DoubleSlap, Minimize, Metronome). Expected: 100 / 0.66 / 47 blind in my simulator, about 79 clean in the scorer's terms.

### Young Couple Ty and Sue: Route 209, optional, double, cap 39

Fake Out and an Assault Vest: Lopunny opens, Wigglytuff's vested Dazzling Gleam hits both sides, then Altaria's Air Cutter and Floatzel. The Vest is this pair's reward, so they show what it does. A double because they stand together; a notch softer until the scorer reads doubles.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Lopunny | 36 | none | Scrappy | default | Fake Out, Return, Jump Kick, U-turn |
| Wigglytuff | 36 | Assault Vest | Cute Charm | Modest | Dazzling Gleam, Flamethrower, Ice Beam, Thunderbolt |
| Floatzel | 35 | Mystic Water | Swift Swim | default | Waterfall, Ice Fang, Crunch, Aqua Jet |
| Altaria | 35 | none | Cloud Nine | default | Dragon Pulse, Air Cutter, Flamethrower, Roost |

Today's team: Lopunny 31 (Return, Jump Kick, Quick Attack, Fire Punch), Floatzel 31 (Aqua Jet, Ice Punch, Pursuit, Waterfall). Expected: not readable yet (a double).

### Twins Emma and Lil: Route 209, on the path, double, cap 39

Fangs behind two Intimidates: Arcanine's Helping Hand and Granbull's Play Rough beside Luxray and a Speed Boost Sharpedo. Kaizo's fang team, with Wild Charge and Play Rough.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Luxray | 36 | Razor Fang | Tinted Lens | Adamant | Wild Charge, Crunch, Ice Fang, Fire Fang |
| Arcanine | 36 | none | Intimidate | default | Fire Fang, Wild Charge, Crunch, Helping Hand |
| Granbull | 35 | none | Intimidate | default | Play Rough, Ice Fang, Thunder Fang, StompingTantrum |
| Sharpedo | 35 | Mystic Water | Speed Boost | default | Crunch, Ice Fang, Aqua Jet, Waterfall |

Today's team: Magneton 29 (Screech, Metal Sound, Mirror Shot, Psych Up), Vibrava 29 (Mud Shot, Sandstorm, Silver Wind, AncientPower), Cacturne 31 (Giga Drain, Cotton Spore, Nasty Plot, Teeter Dance), Shuckle 31 (Encore, AncientPower, Bug Bite, Sand Tomb), Ninetales 29 (Psych Up, Overheat, Swift, Will-O-Wisp), Omastar 31 (Brine, Icy Wind, Rock Polish, AncientPower). Expected: not readable yet (a double).

### Jogger Raul: Route 209, optional, single, cap 39

Normal speed: a Silk Scarf Swellow with Scrappy (the Scarf is Raul's reward), Ambipom's Fake Out and Triple Axel, and Linoone. Kaizo's level-89 Spinda joke is gone.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Ambipom | 36 | none | Technician | default | Fake Out, Double Hit, U-turn, Triple Axel |
| Linoone | 36 | Sitrus Berry | Gluttony | default | Return, Seed Bomb, Shadow Claw, Play Rough |
| Swellow | 37 | Silk Scarf | Scrappy | Jolly | Return, Aerial Ace, U-turn, Quick Attack |

Today's team: Swellow 31 (Quick Attack, Brave Bird, Roost, Endeavor). Expected: 100 / 0.51 / 56 blind in my simulator, about 82 clean in the scorer's terms.

### Barry 3: Route 209, gate to Hearthome, on the path, single, boss, cap 39

Barry's skeleton from his third fight: a Fake Out lead (Technician Ambipom with Double Hit, U-turn and Last Resort), then Staraptor's Brave Bird and Close Combat behind Intimidate, Floatzel's Waterfall and Ice Fang, a Snorlax with Curse, and his starter last at the cap: Torterra for a player who took Piplup, Infernape for Turtwig, Empoleon for Chimchar.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Ambipom | 37 | Silk Scarf | Technician | Jolly | Fake Out, Double Hit, U-turn, Last Resort |
| Staraptor | 38 | Sharp Beak | Intimidate | Adamant | Brave Bird, Close Combat, U-turn, Roost |
| Floatzel | 37 | Mystic Water | Swift Swim | Adamant | Waterfall, Ice Fang, Crunch, Brick Break |
| Snorlax | 38 | Leftovers | Thick Fat | Careful | Body Slam, Earthquake, Curse, Ice Punch |
| Torterra | 39 | Sitrus Berry | Thick Fat | Adamant | Wood Hammer, Earthquake, Crunch, Stone Edge |

Today's team: Staravia 32 (Focus Sash; Aerial Ace, Quick Attack, Endeavor, Double Team), Staryu 32 (BubbleBeam, Signal Beam, Camouflage, Recover), Vulpix 32 (Flamethrower, Will-O-Wisp, Energy Ball, Confuse Ray), Grotle 33 (Sitrus Berry; Seed Bomb, Curse, Bite, Leech Seed). Expected: about 98 / 3.0 / 3 in my simulator, where today's file reads 100 / 0.0 / 100.

### Youngster Oliver: Lost Tower 2F, optional, single, cap 39

Quiver Dance: Mothim boosts behind Chatot's confusion, with Yanmega and an Adaptability Crawdaunt carrying Dual Wingbeat. Kaizo has no team here; the idea is mine.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Chatot | 35 | none | Big Pecks | default | Chatter, Air Cutter, U-turn, Roost |
| Crawdaunt | 36 | BlackGlasses | Adaptability | default | Waterfall, Night Slash, X-Scissor, Dual Wingbeat |
| Yanmega | 36 | none | Speed Boost | default | Signal Beam, Air Cutter, Psychic, Giga Drain |
| Mothim | 38 | SilverPowder | Tinted Lens | Modest | Quiver Dance, Signal Beam, Psychic, Air Cutter |

Today's team: Mothim 31 (Ominous Wind, Psychic, Signal Beam, PoisonPowder), Crawdaunt 30 (Waterfall, Dragon Dance, Knock Off, Brick Break), Chatot 31 (Air Cutter, Chatter, Roost, Mimic). Expected: 100 / 0.35 / 74 blind in my simulator, about 89 clean in the scorer's terms.

### Roughneck Kirby: Lost Tower 3F, optional, single, cap 39

Dark bruisers: Weavile's Triple Axel and Ice Shard, Houndoom's Will-O-Wisp, Skuntank's Toxic.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Skuntank | 35 | none | Aftermath | default | Poison Jab, Crunch, Sucker Punch, Toxic |
| Houndoom | 36 | Charcoal | Flash Fire | default | Flamethrower, Dark Pulse, Sludge Bomb, Will-O-Wisp |
| Weavile | 37 | NeverMeltIce | Inner Focus | Jolly | Night Slash, Ice Shard, Triple Axel, Taunt |

Today's team: Wigglytuff 33 (Sing, Psychic, Rest, Snore). Expected: 99 / 0.64 / 54 blind in my simulator, about 82 clean in the scorer's terms.

### Pokefan Leonard: Lost Tower 3F, optional, single, cap 39

Electric mice: Plusle's Electroweb and Thunder Wave, Minun's Alluring Voice, Pachirisu's Adaptability Discharge and Raichu's Fake Out.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Plusle | 35 | Sitrus Berry | Plus | default | Electroweb, Thunderbolt, Encore, Thunder Wave |
| Minun | 35 | Sitrus Berry | Volt Absorb | default | Thunderbolt, Icy Wind, Alluring Voice, Light Screen |
| Pachirisu | 36 | Sitrus Berry | Adaptability | default | Discharge, Super Fang, U-turn, Seed Bomb |
| Raichu | 37 | Magnet | Lightning Rod | Timid | Fake Out, Thunderbolt, Surf, Alluring Voice |

Today's team: Plusle 31 (Sitrus Berry; Fake Tears, Copycat, Thunderbolt, Fake Tears), Minun 31 (Sitrus Berry; Charm, Copycat, Thunderbolt, Fake Tears), Pikachu 31 (Sitrus Berry; Double Team, Slam, Thunderbolt, Feint). Expected: 98 / 0.56 / 66 blind in my simulator, about 87 clean in the scorer's terms.

### Pokefan Rebekah: Lost Tower 4F, optional, single, cap 39

Rock Head: Sudowoodo's Wood Hammer with no recoil, behind Togetic's Super Luck and a Huge Power Marill.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Togetic | 35 | none | Super Luck | default | Dazzling Gleam, Air Cutter, Aura Sphere, Wish |
| Marill | 35 | none | Huge Power | default | Aqua Tail, Play Rough, Aqua Jet, Knock Off |
| Sudowoodo | 37 | Hard Stone | Rock Head | Adamant | Wood Hammer, Rock Slide, Sucker Punch, StompingTantrum |

Today's team: Sudowoodo 33 (Sitrus Berry; Wood Hammer, Low Kick, ThunderPunch, Rock Tomb). Expected: 100 / 0.56 / 49 blind in my simulator, about 80 clean in the scorer's terms.

### Belle and Pa Beth and Bob: Lost Tower 4F, optional, double, cap 39

Sun: Exeggutor's Sunny Day on a Heat Rock, then Ninetales' spread Incinerate beside Arcanine's Flash Fire and Helping Hand.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Exeggutor | 35 | Heat Rock | Chlorophyll | default | Sunny Day, Energy Ball, Psychic, Sleep Powder |
| Ninetales | 36 | Charcoal | Magic Guard | default | Incinerate, Flamethrower, Energy Ball, Will-O-Wisp |
| Arcanine | 36 | none | Flash Fire | default | Fire Fang, Wild Charge, Crunch, Helping Hand |

Today's team: Growlithe 33 (Roar, Crunch, Fire Fang, Morning Sun), Ponyta 33 (Headbutt, Flame Wheel, Bounce, Hypnosis). Expected: not readable yet (a double).

### Young Couple Mike and Nat: Lost Tower 4F, optional, double, cap 39

A spread Ground move beside immune partners: Donphan's Magnitude beside Levitate Mismagius and Bronzong and a Moxie Honchkrow.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Donphan | 37 | Soft Sand | Battle Armor | default | Magnitude, Ice Shard, Knock Off, Rock Slide |
| Mismagius | 36 | none | Levitate | default | Shadow Ball, Dazzling Gleam, Thunderbolt, Will-O-Wisp |
| Honchkrow | 36 | none | Moxie | default | Sucker Punch, Drill Peck, U-turn, Assurance |
| Bronzong | 35 | Leftovers | Levitate | default | Gyro Ball, Extrasensory, Rock Slide, Hypnosis |

Today's team: Murkrow 33 (Drill Peck, Sucker Punch, Whirlwind, Taunt), Misdreavus 33 (Mean Look, Psychic, Pain Split, Shadow Ball). Expected: not readable yet (a double).

### Ruin Maniac Karl: Solaceon Ruins, optional, single, cap 39

Stealth Rock from Claydol, then stone and steel: Relicanth's Rock Head Take Down and Bronzong's Hypnosis.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Claydol | 36 | none | Levitate | default | Stealth Rock, Earth Power, Psychic, Rapid Spin |
| Relicanth | 37 | Hard Stone | Rock Head | Adamant | Waterfall, Rock Slide, StompingTantrum, Take Down |
| Bronzong | 37 | Leftovers | Heatproof | Relaxed | Gyro Ball, Extrasensory, Rock Slide, Hypnosis |

Today's team: Nidoking 31 (Dig, Brick Break, Poison Jab, Thrash), Donphan 31 (Earthquake, Fire Fang, Thunder Fang, Seed Bomb), Bronzor 31 (Confuse Ray, Extrasensory, Iron Defense, Safeguard). Expected: 98 / 0.63 / 64 blind in my simulator, about 86 clean in the scorer's terms.

### Pkmn Breeder Kahlil: Route 210 south, optional, single, cap 39

Speed Boost Blaziken with Protect, behind Hitmontop's Fake Out and Triple Axel and a goggled Breloom (the Goggles are Kahlil's reward). Kaizo's team, with Staraptor's Dual Wingbeat.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Hitmontop | 35 | none | Technician | default | Fake Out, Triple Axel, Rolling Kick, Sucker Punch |
| Breloom | 36 | Safety Goggles | Technician | default | Mach Punch, Bullet Seed, Rock Slide, Stun Spore |
| Staraptor | 36 | none | Reckless | default | Dual Wingbeat, Close Combat, U-turn, Quick Attack |
| Blaziken | 37 | Charcoal | Speed Boost | Adamant | Blaze Kick, Brick Break, Knock Off, Protect |

Today's team: Elekid 31 (Cross Chop, Ice Punch, Light Screen, ThunderPunch), Magby 31 (Flare Blitz, Cross Chop, Mach Punch, Fire Punch). Expected: 97 / 0.97 / 36 blind in my simulator, about 74 clean in the scorer's terms.

### Pkmn Breeder Amber: Route 210 south, optional, single, cap 39

Healing Fairies: a Calm Mind Clefable with Moonlight, Blissey's Softboiled and Toxic, Kangaskhan's Fake Out.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Kangaskhan | 36 | none | Scrappy | default | Fake Out, Double-Edge, Crunch, Sucker Punch |
| Blissey | 35 | none | Natural Cure | default | Softboiled, Toxic, Chilling Water, Dazzling Gleam |
| Clefable | 37 | Leftovers | Magic Guard | Calm | Calm Mind, Alluring Voice, Flamethrower, Moonlight |

Today's team: Happiny 31 (Counter, Copycat, Metronome, Sweet Kiss), Togepi 31 (Yawn, Extrasensory, Mirror Move, Metronome). Expected: 100 / 0.65 / 51 blind in my simulator, about 81 clean in the scorer's terms.

### Twins Teri and Tia: Route 210 south, optional, double, cap 39

Prankster speed: Illumise's priority Thunder Wave and Encore and Volbeat's priority Tail Glow, beside Plusle's Electroweb and Minun's Icy Wind. Kaizo's pair, with the hidden Prankster.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Plusle | 36 | Magnet | Plus | default | Electroweb, Thunderbolt, Helping Hand, Encore |
| Minun | 36 | none | Minus | default | Thunderbolt, Icy Wind, Helping Hand, Alluring Voice |
| Illumise | 35 | none | Prankster | default | Encore, Thunder Wave, Bug Buzz, Wish |
| Volbeat | 35 | SilverPowder | Prankster | default | Tail Glow, Bug Buzz, Thunderbolt, Helping Hand |

Today's team: Gloom 32 (Stun Spore, Sleep Powder, Giga Drain, Synthesis), Weepinbell 32 (Stun Spore, Knock Off, Sucker Punch, Seed Bomb). Expected: not readable yet (a double).

### Belle and Pa Ava and Matt: Route 210 south, optional, double, cap 39

Teeter Dance beside Own Tempo: Spinda confuses the field while Slowbro and Grumpig ignore it, and Bellossom carries Sleep Powder. Kaizo's Teeter Dance pair.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Spinda | 37 | none | Own Tempo | default | Teeter Dance, Fake Out, Psycho Cut, Sucker Punch |
| Grumpig | 36 | TwistedSpoon | Own Tempo | default | Psychic, Dazzling Gleam, Shadow Ball, Light Screen |
| Slowbro | 35 | none | Own Tempo | default | Water Pulse, Ice Beam, Psychic Noise, Flamethrower |
| Bellossom | 36 | Miracle Seed | Chlorophyll | default | Giga Drain, Dazzling Gleam, Moonlight, Sleep Powder |

Today's team: Vulpix 33 (Imprison, Flamethrower, Safeguard, Payback), Ninetales 33 (Flamethrower, Quick Attack, Confuse Ray, Safeguard). Expected: not readable yet (a double).

### Rancher Marco: Route 210 south, optional, single, cap 39

Sheer Force: Tauros's Zen Headbutt, Rock Slide and Iron Head trade their flinches for power, beside Noctowl's Moonblast and Hypnosis.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Noctowl | 36 | none | Tinted Lens | default | Air Slash, Moonblast, Hypnosis, Roost |
| Tauros | 37 | Hard Stone | Sheer Force | Adamant | Zen Headbutt, Rock Slide, Iron Head, StompingTantrum |
| Girafarig | 35 | none | Sap Sipper | default | Psychic, Thunderbolt, Shadow Ball, Calm Mind |

Today's team: Tauros 33 (Pursuit, Rest, Headbutt, Zen Headbutt). Expected: 100 / 0.74 / 46 blind in my simulator, about 79 clean in the scorer's terms.

### Jogger Wyatt: Route 210 south, optional, single, cap 39

Fire and Electric speed: Arcanine's Wild Charge, Manectric's Lightning Rod and Purugly's Defiant Fake Out. Kaizo's level-76 joke is gone.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Manectric | 36 | Magnet | Lightning Rod | default | Thunderbolt, Flamethrower, Signal Beam, Thunder Wave |
| Purugly | 36 | none | Defiant | default | Fake Out, Play Rough, Sucker Punch, U-turn |
| Arcanine | 37 | Charcoal | Intimidate | Adamant | Fire Fang, Wild Charge, Crunch, Iron Head |

Today's team: Manectric 33 (Quick Attack, Thunder Fang, Fire Fang, Crunch). Expected: 100 / 0.82 / 41 blind in my simulator, about 76 clean in the scorer's terms.

### Black Belt Gregory: Route 215 (rain), optional, single, cap 39

Punches in the rain: Hitmonchan's Iron Fist, Machoke's Close Combat, and Poliwrath with Water Absorb rather than Swift Swim, which read far past the band.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Hitmonchan | 35 | none | Iron Fist | default | Drain Punch, Ice Punch, ThunderPunch, Mach Punch |
| Machoke | 37 | none | Steadfast | default | Close Combat, Knock Off, Bullet Punch, Rock Slide |
| Poliwrath | 35 | none | Water Absorb | default | Waterfall, Drain Punch, Poison Jab, Low Sweep |

Today's team: Machop 34 (Bullet Punch, ThunderPunch, Low Kick, Wake-Up Slap), Breloom 34 (Mach Punch, Seed Bomb, ThunderPunch, Sky Uppercut), Hitmonchan 34 (Mach Punch, ThunderPunch, Ice Punch, Fire Punch). Expected: 98 / 0.98 / 38 blind in my simulator in rain, about 75 clean in the scorer's terms.

### Black Belt Derek: Route 215 (rain), optional, single, cap 39

Dry Skin: Toxicroak heals in the rain, beside Gallade's Triple Axel and Breloom's Mach Punch.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Breloom | 35 | none | Technician | default | Mach Punch, Bullet Seed, Stun Spore, Sky Uppercut |
| Gallade | 36 | none | Justified | default | Psycho Cut, Drain Punch, Leaf Blade, Triple Axel |
| Toxicroak | 37 | none | Dry Skin | default | Poison Jab, Drain Punch, Sucker Punch, Bullet Punch |

Today's team: Tyrogue 34 (Brick Break, Bullet Punch, Fake Out, Mach Punch). Expected: 96 / 1.26 / 29 blind in my simulator in rain, about 72 clean in the scorer's terms.

### Black Belt Nathaniel: Route 215 (rain), optional, single, cap 39

Kicks: Hitmonlee's Fake Out and High Jump Kick, Mienshao's Regenerator and Triple Axel, a Pure Power Medicham.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Medicham | 35 | none | Pure Power | default | Hi Jump Kick, Zen Headbutt, Bullet Punch, Ice Punch |
| Mienshao | 36 | none | Regenerator | default | Drain Punch, U-turn, Knock Off, Triple Axel |
| Hitmonlee | 37 | none | Reckless | default | Fake Out, Hi Jump Kick, Knock Off, Rock Slide |

Today's team: Croagunk 34 (Poison Jab, Bullet Punch, Low Kick, Sucker Punch), Meditite 34 (ThunderPunch, Psycho Cut, Fire Punch, Hi Jump Kick), Hitmonlee 34 (Sucker Punch, Bullet Punch, Hi Jump Kick, Fake Out). Expected: 99 / 0.95 / 42 blind in my simulator in rain, about 77 clean in the scorer's terms.

### Jogger Scott: Route 215 (rain), optional, single, cap 39

Spikes from Forretress on a Rocky Helmet, then Jolteon's Psyshock and Weezing's Will-O-Wisp. Kaizo's three-hazard lead cut to one setter.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Forretress | 36 | Rocky Helmet | Heatproof | default | Spikes, Gyro Ball, Rock Slide, Rapid Spin |
| Weezing | 36 | none | Levitate | default | Sludge Bomb, Thunderbolt, Will-O-Wisp, Pain Split |
| Jolteon | 38 | Magnet | Volt Absorb | Timid | Thunderbolt, Psyshock, Shadow Ball, Thunder Wave |

Today's team: Farfetchd 34 (Leaf Blade, Aerial Ace, Poison Jab, Night Slash). Expected: 100 / 0.43 / 67 blind in my simulator in rain, about 87 clean in the scorer's terms.

### Ace Trainer Dennis: Route 215, on the path, single, Ace Trainer, cap 39

Speed and coverage: Gliscor's Ice Fang and U-turn, Floatzel's Aqua Jet, Staraptor's Brave Bird, and Drifblim's Unburden with Thunderbolt and Will-O-Wisp.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Gliscor | 37 | none | Sand Veil | default | Knock Off, Ice Fang, U-turn, Rock Slide |
| Floatzel | 37 | none | Swift Swim | default | Waterfall, Ice Fang, Crunch, Aqua Jet |
| Staraptor | 37 | none | Reckless | default | Brave Bird, Close Combat, Quick Attack, U-turn |
| Drifblim | 38 | Sitrus Berry | Unburden | default | Shadow Ball, Thunderbolt, Will-O-Wisp, Stockpile |

Today's team: Gligar 35 (Knock Off, U-turn, Slash, Tailwind), Floatzel 35 (Ice Punch, Crunch, Aqua Jet, Brick Break), Drifblim 35 (Thunderbolt, Weather Ball, Thunder Wave, Ominous Wind). Expected: about 100 / 0.2 / 83 with a planned six in rain; read blind, 93 / 1.4 / 33.

### Ace Trainer Maya: Route 215, on the path, single, Ace Trainer, cap 39

Toxic Spikes from Roserade, then special attackers: Gastrodon's Earth Power and Surf, Lickilicky's Ice Beam and Thunderbolt, Gardevoir's Psychic.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Roserade | 37 | Black Sludge | Natural Cure | Timid | Toxic Spikes, Sludge Bomb, Giga Drain, Leech Seed |
| Gastrodon | 37 | none | Dry Skin | default | Earth Power, Surf, Sludge Bomb, Body Slam |
| Lickilicky | 37 | none | Poison Heal | default | Body Slam, Knock Off, Ice Beam, Thunderbolt |
| Gardevoir | 38 | none | Trace | default | Psychic, Thunderbolt, Energy Ball, Wish |

Today's team: Roserade 35 (Toxic Spikes, Giga Drain, Leech Seed), Gardevoir 35 (Psychic, Energy Ball, Calm Mind, Thunderbolt), Lickitung 35 (Fire Punch, Ice Punch, Zen Headbutt, ThunderPunch). Expected: about 100 / 0.9 / 13 with a planned six in rain; read blind, 96 / 2.4 / 1.

### Ruin Maniac Calvin: Route 215 (rain), optional, single, cap 39

Fossils in the rain: Cradily's Stealth Rock, then Kabutops on Swift Swim, Omastar and Armaldo. Kaizo's four Swift Swim fossils keep one.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Cradily | 37 | Leftovers | Storm Drain | default | Stealth Rock, Giga Drain, AncientPower, Recover |
| Kabutops | 35 | none | Swift Swim | default | Waterfall, Rock Slide, Aqua Jet, Knock Off |
| Omastar | 36 | none | Shell Armor | default | Surf, AncientPower, Ice Beam, Earth Power |
| Armaldo | 36 | none | Battle Armor | default | X-Scissor, Rock Slide, Aqua Tail, Knock Off |

Today's team: Bronzong 33 (Extrasensory, Iron Defense, Safeguard, AncientPower), Bastiodon 33 (Outrage, Swagger, Iron Head, Headbutt). Expected: 94 / 0.97 / 64 blind in my simulator in rain, about 86 clean in the scorer's terms.

### Jogger Craig: Route 215 (rain), on the path, single, cap 39

Stealth Rock from a fast Dugtrio, then Electric speed: Pachirisu's Electroweb and Luxray's Reckless Wild Charge. Craig is on the path, so his rocks preview Maylene's alone.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Dugtrio | 35 | none | Sand Veil | default | Stealth Rock, StompingTantrum, Sucker Punch, Rock Slide |
| Pachirisu | 36 | Sitrus Berry | Adaptability | default | Discharge, Super Fang, U-turn, Electroweb |
| Luxray | 37 | none | Reckless | default | Wild Charge, Crunch, Ice Fang, Fire Fang |

Today's team: Luxray 34 (Thunder Fang, Ice Fang, Roar, Superpower), Pachirisu 34 (ThunderPunch, Seed Bomb, Gunk Shot, Super Fang). Expected: 100 / 0.94 / 44 blind in my simulator in rain, about 78 clean in the scorer's terms.

### Black Belt Colby: Veilstone Gym, gym trainer, single, cap 39

Maylene's Fake Out and orb together: Hitmontop's Fake Out and Triple Axel, Machamp's Low Sweep, and a Guts Hariyama on a Flame Orb with Whirlwind.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Hitmontop | 37 | none | Technician | default | Fake Out, Triple Axel, Mach Punch, Sucker Punch |
| Machamp | 36 | none | Steadfast | default | Knock Off, Bullet Punch, Rock Slide, Low Sweep |
| Hariyama | 38 | Flame Orb | Guts | default | Facade, Force Palm, Bullet Punch, Whirlwind |

Today's team: Tyrogue 33 (Hi Jump Kick, Mach Punch, Bullet Punch, Fake Out), Machoke 33 (Superpower, Fire Punch, Ice Punch), Hitmonchan 33 (ThunderPunch, Ice Punch, Mach Punch, Bullet Punch). Expected: 100 / 0.83 / 49 blind in my simulator, about 80 clean in the scorer's terms.

### Black Belt Darren: Veilstone Gym, gym trainer, single, cap 39

Maylene's Stealth Rock and priority together: Primeape lays the rocks and hits with Rage Fist, then Hitmonchan's Mach Punch and Machoke's Bullet Punch.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Primeape | 37 | none | Defiant | Jolly | Stealth Rock, Rage Fist, Drain Punch, U-turn |
| Hitmonchan | 36 | none | Iron Fist | default | Drain Punch, Ice Punch, ThunderPunch, Mach Punch |
| Machoke | 37 | none | Steadfast | default | Close Combat, Knock Off, Bullet Punch, Rock Slide |

Today's team: Primeape 35 (ThunderPunch, Close Combat, Seed Bomb, U-turn), Meditite 35 (Hi Jump Kick, Psycho Cut, Ice Punch), Hitmonlee 35 (Hi Jump Kick, Rock Slide, Mach Punch, Poison Jab). Expected: 98 / 1.29 / 25 blind in my simulator, about 70 clean in the scorer's terms.

### Black Belt Rafael: Veilstone Gym, gym trainer, single, cap 39

Maylene's orb and Revenge: Toxicroak's Fake Out, Cacturne's Revenge and Spikes, and a Guts Lickilicky on a Flame Orb.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Toxicroak | 37 | none | Dry Skin | default | Fake Out, Poison Jab, Drain Punch, Sucker Punch |
| Cacturne | 37 | Occa Berry | Water Absorb | default | Revenge, Seed Bomb, Sucker Punch, Spikes |
| Lickilicky | 38 | Flame Orb | Guts | default | Facade, StompingTantrum, Rock Slide, Brick Break |

Today's team: Croagunk 26 (Swagger, Revenge, Faint Attack), Machoke 26 (Karate Chop, Foresight). Expected: 100 / 0.51 / 59 blind in my simulator, about 84 clean in the scorer's terms.

### Black Belt Jeffery: Veilstone Gym, gym trainer, single, cap 39

Maylene's priority and resist berry: Breloom's Mach Punch on a Coba Berry, Mienshao's Fake Out and Triple Axel, Heracross's Close Combat.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Breloom | 37 | Coba Berry | Technician | default | Mach Punch, Bullet Seed, Stun Spore, Rock Slide |
| Mienshao | 37 | none | Regenerator | default | Drain Punch, Triple Axel, Knock Off, Fake Out |
| Heracross | 38 | none | Guts | default | Close Combat, Pin Missile, Knock Off, Rock Slide |

Today's team: Heracross 36 (Brick Break, Aerial Ace, Bug Bite, Night Slash). Expected: 98 / 1.02 / 42 blind in my simulator, about 77 clean in the scorer's terms.

### Maylene: Veilstone Gym, on the path, single, boss, cap 39

A Stealth Rock lead with a Fake Out member behind it, an orb user and a priority ace: Glimmora sets the rocks behind a Focus Sash, Toxicroak opens with Fake Out, Heracross runs Guts on a Flame Orb, Cacturne (with Revenge) and Medicham cover the Flying and Psychic answers, and Lucario closes with Aura Sphere, Flash Cannon and Vacuum Wave. Flying, Psychic and Fairy types are the answers. Glimmora is off-theme for a Fighting gym and carries no Fighting move; Ian keeps it for now and will revisit it.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Glimmora | 37 | Focus Sash | Corrosion | Timid | Stealth Rock, Power Gem, Venoshock, Mortal Spin |
| Heracross | 38 | Flame Orb | Guts | Jolly | Close Combat, Facade, Aerial Ace, Night Slash |
| Toxicroak | 38 | Payapa Berry | Dry Skin | Adamant | Fake Out, Poison Jab, Cross Chop, Ice Punch |
| Cacturne | 38 | Sitrus Berry | Sand Veil | Adamant | Revenge, Seed Bomb, Faint Attack, Payback |
| Medicham | 38 | Coba Berry | Pure Power | Jolly | Hi Jump Kick, Psycho Cut, Fire Punch, ThunderPunch |
| Lucario | 39 | Black Belt | Adaptability | Modest | Aura Sphere, Flash Cannon, Water Pulse, Vacuum Wave |

Today's team: Poliwrath 38 (Damp Rock; Brick Break, Waterfall, Rock Slide, Rain Dance), Heracross 38 (Flame Orb; Close Combat, Facade, Aerial Ace, Bug Bite), Toxicroak 38 (Payapa Berry; Sucker Punch, Poison Jab, Cross Chop, Ice Punch), Cacturne 38 (Iron Ball; Revenge, Fling, Sucker Punch, Seed Bomb), Medicham 38 (Shell Bell; Hi Jump Kick, Psycho Cut, Fire Punch, ThunderPunch), Lucario 39 (Black Belt; Water Pulse, Vacuum Wave, Flash Cannon, Aura Sphere). Expected: about 34 / 5.3 / 0 in my simulator, where today's file reads 96 / 2.1 / 1.

### Galactic Grunt (Veilstone, 1): Veilstone City, on the path, tag beside Lucas or Dawn, cap 39

Poison beside its partner: Skuntank's Toxic then Hex, Crobat's Confuse Ray and Dual Wingbeat.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Skuntank | 36 | none | Aftermath | default | Poison Jab, Sucker Punch, Toxic, Hex |
| Crobat | 37 | Black Sludge | Inner Focus | default | Cross Poison, Leech Life, Dual Wingbeat, Confuse Ray |

Today's team: Swalot 35 (Sludge Bomb, Shadow Ball, Destiny Bond, Toxic), Skuntank 35 (Sludge Bomb, Toxic, Dark Pulse, Flamethrower). Expected: not readable yet (a tag battle).

### Galactic Grunt (Veilstone, 2): Veilstone City, on the path, tag beside Lucas or Dawn, cap 39

Venomoth's Sleep Powder and Victreebel's Sucker Punch.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Venomoth | 36 | none | Tinted Lens | default | Sludge Bomb, Psychic, Sleep Powder, Signal Beam |
| Victreebel | 37 | Black Sludge | Chlorophyll | default | Seed Bomb, Sludge Bomb, Sucker Punch, Knock Off |

Today's team: Venomoth 35 (Sludge Bomb, Psychic, Sleep Powder, Silver Wind), Victreebel 35 (Seed Bomb, Sleep Powder, Sucker Punch, Sweet Scent). Expected: not readable yet (a tag battle).

### Collector Fernando: Veilstone cafe, optional, single, cap 39

Few weaknesses: Sableye's Prankster Will-O-Wisp then Hex, Spiritomb on a Roseli Berry, Mawile's Intimidate.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Spiritomb | 35 | Roseli Berry | Pressure | default | Dark Pulse, Shadow Ball, Sucker Punch, Confuse Ray |
| Mawile | 36 | none | Intimidate | default | Play Rough, Iron Head, Sucker Punch, Crunch |
| Sableye | 37 | Leftovers | Prankster | default | Will-O-Wisp, Hex, Knock Off, Recover |

Today's team: Heracross 32 (Night Slash, Brick Break, Counter, Aerial Ace). Expected: 97 / 0.94 / 39 blind in my simulator, about 76 clean in the scorer's terms.

### Collector Edwin: Veilstone cafe, optional, single, cap 39

Rare and bulky: Snorlax's Curse, Lapras, Kangaskhan's Double-Edge.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Kangaskhan | 35 | none | Scrappy | default | Double-Edge, Crunch, Sucker Punch, Drain Punch |
| Snorlax | 36 | Leftovers | Thick Fat | Careful | Curse, Body Slam, StompingTantrum, Rest |
| Lapras | 37 | none | Shell Armor | default | Surf, Ice Beam, Thunderbolt, Body Slam |

Today's team: Munchlax 32 (Chesto Berry; Headbutt, Ice Punch, Rest, Zen Headbutt). Expected: 100 / 1.06 / 40 blind in my simulator, about 76 clean in the scorer's terms.

### Waitress Kati: Veilstone cafe, optional, single, cap 39

Punches: a Punching Glove Hitmonchan (the Glove is Kati's reward), Miltank's Milk Drink, Blissey's Toxic. Kaizo's level-90 joke is gone.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Blissey | 35 | none | Natural Cure | default | Softboiled, Chilling Water, Dazzling Gleam, Toxic |
| Hitmonchan | 36 | Punching Glove | Iron Fist | default | Drain Punch, Ice Punch, ThunderPunch, Mach Punch |
| Miltank | 37 | none | Sap Sipper | default | Body Slam, Milk Drink, Play Rough, Thunder Wave |

Today's team: Absol 33 (Sucker Punch, Swords Dance, Zen Headbutt, Superpower). Expected: 99 / 0.84 / 45 blind in my simulator, about 78 clean in the scorer's terms.

### Roughneck Rocco: Veilstone Game Corner, optional, single, cap 39

House odds: an Eviolite Porygon2 with Download, Persian's Technician Fake Out and Bite, and the Metronome kept from the file Rocco came with.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Persian | 37 | none | Technician | default | Fake Out, Bite, Play Rough, U-turn |
| Clefable | 37 | Leftovers | Magic Guard | default | Alluring Voice, Metronome, Thunder Wave, Moonlight |
| Porygon2 | 37 | Eviolite | Download | Modest | Ice Beam, Thunderbolt, Thunder Wave, Recover |

Today's team: Persian 37 (Fake Out, Slash, Bite, Screech), Clefable 37 (Moonblast, Metronome, Thunder Wave, Sing), Porygon2 38 (Tri Attack, Psybeam, Agility, Recover). Expected: 99 / 0.55 / 56 blind in my simulator, about 83 clean in the scorer's terms.


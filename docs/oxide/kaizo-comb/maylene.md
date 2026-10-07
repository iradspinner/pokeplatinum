# The comb: Maylene's split

The bosses of Maylene's split are combed: Barry 3 (three files, one per
starter), Ace Trainers Dennis and Maya, and Maylene, all passing the checker
and the rule audit. The split's ordinary trainers follow in a later pass, as
the order Ian set asks, and will be added to this file.

The cap is 39 throughout. Today's Barry 3 and Ace Trainers sit four to seven
levels under it (32 to 35); here every boss's ace stands at the cap and the
rest one or two under, as the dial's Rule 2 asks, and the Ace Trainers one
under.

My simulator reads them against the scorer's box at Maylene (box-after-fantina.md),
which knows no TMs, so these fights read harsher than they will once the TM
pass lands. Bosses are set a step harder than today's files: Maylene about 81
won to today's 94 in my simulator, Barry 3 about level on wins with far more
faints than today's. The Ace Trainers, which goal 3 reads with a planned six,
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

Route 215's ordinary trainers will be built for the rain in the later pass.
The Lost Tower's 5F is in fog, but no trainer stands there; no other map in
this split has its own weather.

## Decisions for Ian

Ian answered both on 2026-10-06. Glimmora is flagged off-theme, to revisit; from Wake's split on, every gym leader's members are of the gym's type or carry a move of it.

| # | Decision | What the files do today | How it is checked | What Ian decides |
|---|---|---|---|---|
| 1 | Maylene drops her rain (Ian: Glimmora stays for now but is off-theme for a Fighting gym, with no Fighting move; revisit later) | Today's Maylene opens with a Rain Dance Poliwrath on a Damp Rock; here a Glimmora leads with Stealth Rock behind a Focus Sash, since the dial keeps weather bosses to Gardenia's, Wake's and Candice's splits and the League. Heracross keeps the Flame Orb, Cacturne and Medicham stay, Toxicroak takes the Fake Out, and Lucario keeps its Black Belt with Vacuum Wave as the priority ace. | `leader_maylene.json`; the scorer's reading later. | Accept (recommended), or keep Poliwrath's rain beside the new lead. |
| 2 | Barry 3 leads with Fake Out (Ian: Ambipom stands) | The dial gives Barry a Fake Out lead from his third fight, so a Technician Ambipom joins Staraptor, Floatzel, Snorlax and his starter. Its Last Resort is the split's one conditional attack, exempt from the ceiling by Ian's ruling. | `rival_route_209_*.json`. | Accept (recommended). |

## What comes next

Byron's split's bosses, then the rest in order, then the ordinary
trainers of Maylene's split onward.

## Overview

| Trainer | Place | Path | Battle | Size | Levels | The idea | Expected |
|---|---|---|---|---|---|---|---|
| Barry 3 | Route 209, gate to Hearthome | on the path | single, boss | 5 | 37 to 39 | Barry's skeleton from his third fight | about 100 / 2.8 / 1 in my simulator, where today's file reads 100 / 0.0 / 100 |
| Ace Trainer Dennis | Route 215 | on the path | single, Ace Trainer | 4 | 37 to 38 | Speed and coverage | about 100 / 0.2 / 84 with a planned six in Route 215's rain |
| Ace Trainer Maya | Route 215 | on the path | single, Ace Trainer | 4 | 37 to 38 | Toxic Spikes from Roserade | about 100 / 0.95 / 12 with a planned six in Route 215's rain |
| Maylene | Veilstone Gym | on the path | single, boss | 6 | 37 to 39 | A Stealth Rock lead with a Fake Out member behind it | about 81 / 3.7 / 1 in my simulator, where today's file reads 94 / 2.4 / 0 |

Expected numbers are won / faints a fight / clean in my simulator, beside
today's file where it was read.

## The bosses

### Barry 3: Route 209, gate to Hearthome, on the path, single, boss, cap 39

Barry's skeleton from his third fight: a Fake Out lead (Technician Ambipom with Double Hit, U-turn and Last Resort), then Staraptor's Brave Bird and Close Combat behind Intimidate, Floatzel's Waterfall and Ice Fang, a Snorlax with Curse, and his starter last at the cap: Torterra for a player who took Piplup, Infernape for Turtwig, Empoleon for Chimchar.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Ambipom | 37 | Silk Scarf | Technician | Jolly | Fake Out, Double Hit, U-turn, Last Resort |
| Staraptor | 38 | Sharp Beak | Intimidate | Adamant | Brave Bird, Close Combat, U-turn, Roost |
| Floatzel | 37 | Mystic Water | Swift Swim | Adamant | Waterfall, Ice Fang, Crunch, Brick Break |
| Snorlax | 38 | Leftovers | Thick Fat | Careful | Body Slam, Earthquake, Curse, Ice Punch |
| Torterra | 39 | Sitrus Berry | Thick Fat | Adamant | Wood Hammer, Earthquake, Crunch, Stone Edge |

Today's team: Staravia 32 (Focus Sash; Aerial Ace, Quick Attack, Endeavor, Double Team), Staryu 32 (BubbleBeam, Signal Beam, Camouflage, Recover), Vulpix 32 (Flamethrower, Will-O-Wisp, Energy Ball, Confuse Ray), Grotle 33 (Sitrus Berry; Seed Bomb, Curse, Bite, Leech Seed). Expected: about 100 / 2.8 / 1 in my simulator, where today's file reads 100 / 0.0 / 100; read by the scorer later.

### Ace Trainer Dennis: Route 215, on the path, single, Ace Trainer, cap 39

Speed and coverage: Gliscor's Ice Fang and U-turn, Floatzel's Aqua Jet, Staraptor's Brave Bird, and Drifblim's Unburden with Thunderbolt and Will-O-Wisp.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Gliscor | 37 | none | Sand Veil | default | Knock Off, Ice Fang, U-turn, Rock Slide |
| Floatzel | 37 | none | Swift Swim | default | Waterfall, Ice Fang, Crunch, Aqua Jet |
| Staraptor | 37 | none | Reckless | default | Brave Bird, Close Combat, Quick Attack, U-turn |
| Drifblim | 38 | Sitrus Berry | Unburden | default | Shadow Ball, Thunderbolt, Will-O-Wisp, Stockpile |

Today's team: Gligar 35 (Knock Off, U-turn, Slash, Tailwind), Floatzel 35 (Ice Punch, Crunch, Aqua Jet, Brick Break), Drifblim 35 (Thunderbolt, Weather Ball, Thunder Wave, Ominous Wind). Expected: about 100 / 0.2 / 84 with a planned six in Route 215's rain; read blind, 95 / 1.25 / 73 in the scorer's terms.

### Ace Trainer Maya: Route 215, on the path, single, Ace Trainer, cap 39

Toxic Spikes from Roserade, then special attackers: Gastrodon's Earth Power and Surf, Lickilicky's Ice Beam and Thunderbolt, Gardevoir's Psychic.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Roserade | 37 | Black Sludge | Natural Cure | Timid | Toxic Spikes, Sludge Bomb, Giga Drain, Leech Seed |
| Gastrodon | 37 | none | Dry Skin | default | Earth Power, Surf, Sludge Bomb, Body Slam |
| Lickilicky | 37 | none | Poison Heal | default | Body Slam, Knock Off, Ice Beam, Thunderbolt |
| Gardevoir | 38 | none | Trace | default | Psychic, Thunderbolt, Energy Ball, Wish |

Today's team: Roserade 35 (Toxic Spikes, Giga Drain, Leech Seed), Gardevoir 35 (Psychic, Energy Ball, Calm Mind, Thunderbolt), Lickitung 35 (Fire Punch, Ice Punch, Zen Headbutt, ThunderPunch). Expected: about 100 / 0.95 / 12 with a planned six in Route 215's rain; read blind, 94 / 2.37 / 61 in the scorer's terms.

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

Today's team: Poliwrath 38 (Damp Rock; Brick Break, Waterfall, Rock Slide, Rain Dance), Heracross 38 (Flame Orb; Close Combat, Facade, Aerial Ace, Bug Bite), Toxicroak 38 (Payapa Berry; Sucker Punch, Poison Jab, Cross Chop, Ice Punch), Cacturne 38 (Iron Ball; Revenge, Fling, Sucker Punch, Seed Bomb), Medicham 38 (Shell Bell; Hi Jump Kick, Psycho Cut, Fire Punch, ThunderPunch), Lucario 39 (Black Belt; Water Pulse, Vacuum Wave, Flash Cannon, Aura Sphere). Expected: about 81 / 3.7 / 1 in my simulator, where today's file reads 94 / 2.4 / 0; read by the scorer later.


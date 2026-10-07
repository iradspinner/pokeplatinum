# The comb: Wake's split

**Every trainer of Wake's split is now combed except Wake himself**, whose
draft is set aside for alpha 1. The bosses were combed earlier: Barry 4 and
Ace Trainer Krystal. On 2026-10-07 I added all 72 ordinary trainers, in
walking order, from Route 214 through Route 213, Pastoria's gym and Route 212
to the Hotel Grand Lake restaurant and the Pokemon Mansion, with Route 219's
and Route 208's water trainers. The restaurant fights its 18 trainers in
pairs, two trainers against the player in one double battle (the Overseer,
from the restaurant's scripts, 2026-10-07), so each of those files is one
half of a pair, built with the dial's doubles recipes. Every file passes the checker and the rule
audit.

The ordinary trainers follow Ian's ruling of 2026-10-07. Each takes Kaizo's
idea where Kaizo has the trainer, moves it into Oxide's Generation 5+ pool
where the species' lists allow, then scales it to the dial. Kaizo has no
team for 46 of them (the restaurant, the Mansion, most of Route 212), so their
ideas are mine, built around each trainer's old species where it fits.

| Check | Result |
|---|---|
| Single battles read blind (54) | 94.6 to 100 won, mean 98.3; 46 at 97 or more |
| The restaurant's nine pairs (18 files) | not readable yet (doubles against two trainers) |
| Clean, in the scorer's terms (Ian's band 80 to 85) | 65 to 91, mean 79 |
| Faints a fight, in the scorer's terms (Ian's band 0.1 to 0.25) | 0.2 to 0.9, mean 0.50 |
| Move slots that are Generation 5+ | 126 of 820, 15 percent |
| Hidden abilities | 53, on 39 of 72 teams |
| Element 7 items held | 11: seven Eviolites, a Weakness Policy, a Covert Cloak, an Eject Button and a Red Card |
| Hazard setters | 7 of 72 teams, about one in ten |

As in Maylene's split, the ordinary trainers win as often as Ian asks but
cost about twice his band in faints, which leans toward his wish that they be
dangerous; the scorer's step 15 reading decides any change. The restaurant's
pairs use redirection (Follow Me), spread moves beside immune or resistant
partners (Discharge beside Ground types), speed control (Tailwind, Icy Wind,
Electroweb, Low Sweep), Helping Hand and screens; each half brings two
Pokemon, its top member at 41, a notch softer until the scorer reads doubles. Four trainers
award an element 7 item, and each holds it: Trenton (Eject Button), Mariel
(Red Card), Kenneth (Covert Cloak) and Shaun (Weakness Policy). Josh holds
the Wide Lens he awards. My simulator does not model the Eject Button or the
Red Card.

Three teams carry no modern move although their species have one, each for a
reason:

| Team | Why no modern move |
|---|---|
| Fisherman Josh | The modern options (Psychic Noise, Bulldoze, Stomping Tantrum, Brutal Swing) are weaker than the Psychic, Earthquake and Knock Off the team carries. |
| Scientist Shaun | Wild Charge is physical on Magnezone and weaker than Electivire's Thunder Punch; Foul Play on Porygon2 is over the 90 ceiling on borrowed attacks before Byron's split. |
| Gentleman Leonardo | Chatot's only modern move, Echoed Voice, is weaker than its Chatter and Air Cutter; Pidgeot has none. |

The weather follows the dial. Three routes carry one weather-ability team
each, as Rule 6 allows from this split: Trenton's Drizzle on Route 219,
Jared's Drizzle on Route 213 and Alexa's Drought on Route 212 south. Oxide
keeps Platinum's rule that ability weather lasts the whole battle. Swift Swim
and Chlorophyll partners sit below each team's top level, since at the top
they read far past the band. Haley keeps no rain, since none of her species
can learn Rain Dance in Oxide. Pastoria's gym fights in permanent rain, and
three of its six trainers use it: Damian's Floatzel (Swift Swim), and Walter's
Whiscash (Hydration) and Toxicroak (Dry Skin). The path previews Wake's tools
alone before the gym: Devon's Roserade lays Spikes, Abigail's Jynx opens with
Fake Out, and Jared's rain carries a Swift Swim Seaking.

## The bosses, combed earlier

**Refreshed 2026-10-07.** The expected numbers were read again after two
changes: a fix to my simulator, which had picked the player's lead by party
order when two choices looked equal and so skewed every earlier boss reading,
and the legality sweep against the final lists (origin/balance-tm-pass at
377312dbf0), which left this split unchanged. Ian ruled that every draft goes into step 12 as
drafted; the scorer's step 15 reading gives the real numbers, and he chooses
any retunes from them. My candidates are in `../retune-proposals-not-approved/`.

**Set aside for alpha 1 (Ian, 2026-10-07).** Alpha 1 keeps today's Wake team,
the one that reads about 70 won in his gym's rain. The draft below is kept,
with its readings, for the pass after the alpha, where Wake is a prime area
for changes. Barry 4 and Krystal are unaffected.

The bosses are Barry 4 (three files), Ace Trainer Krystal and Wake.

The cap is 44. My simulator reads the bosses against the scorer's box at
Wake, which knows no TMs, so they read harsher than they will once the TM
pass lands. Each is set a step harder than today's file: Wake about 55 won to
today's 71, both read in his gym's rain, and Barry 4 level on wins with far
more faints than today's. Every one of Wake's six is a Water type, as Ian's
new rule asks of a gym.

Pastoria's gym fights in permanent rain (Ian, 2026-10-06: a map's weather is
battle weather for every fight on it), so Wake needs no setter, and his
Swift Swim members (Qwilfish, Ludicolo, Floatzel) move at double speed all
fight. The rain also helps the player: Fire attacks are halved, but the
box's own Water types hit harder and its Swift Swim members are fast too.
Before the simulator's order fix, rain cost today's Wake about 26 won points
in my reading; it was not read clear again after the fix. Routes 212 south and
213 have changing weather that can bring rain, and their ordinary trainers are
read without it. No other map in this split has its own weather.

## Decisions for Ian

Ian answered the two boss decisions on 2026-10-06: Wake loses the Pelipper,
since his gym is already in rain, and Krystal stays at six with her Quick Claw
restored, as luck items are allowed again. Three new ones come from the
ordinary trainers; the third was answered the same day.

| # | Decision | What the files do today | How it is checked | What Ian decides |
|---|---|---|---|---|
| 1 | Wake fights in his gym's rain (Ian: no Pelipper; the gym is already in permanent rain) | Today's Wake carries two Choice items. Here a Qwilfish leads with Spikes behind a Focus Sash, then Lanturn (Volt Absorb, which walls the box's Electric answers, with Surf, Discharge and Ice Beam), Ludicolo, Gyarados, Sharpedo and Floatzel, the ace with a Life Orb and Bulk Up. The Choice Scarf and Choice Band are gone. Lanturn took Pelipper's slot after a Swift Swim Kingdra read far too hard in the rain (about 20 won). | `leader_wake.json`; the scorer's reading in rain later. | Answered (2026-10-06). |
| 2 | Krystal reads harsh blind (Ian: she stays at six) | Ian's own six (Metang, Glalie, Jumpluff, Rotom, Blaziken, Dragonair) on legal sets at 42 to 43, with fewer boosts on Rotom and Dragonair. Her Quick Claw on Metang is restored (Ian allowed luck items again on 2026-10-06); my simulator does not model it, so her numbers are unchanged. With a planned six she reads 100 won; met blind she loses about one fight in three in the corrected reading. | `dummy_795.json`. | Answered (2026-10-06). |
| 3 | Ordinary trainers a little past the band | They win 94.6 to 100 percent blind but cost about 0.47 Pokemon a fight in the scorer's terms against Ian's 0.1 to 0.25, mostly through one strong member each. | The scorer's step 15 reading. | Accept for now (recommended, as in Maylene's split), or soften them now. |
| 4 | Three permanent weather teams | Trenton's and Jared's Politoed set Drizzle and Alexa's Ninetales sets Drought, each lasting the whole fight under Platinum's rule. | My readings (98.8, 95.2 and 97.4 won); the scorer's reading later. | Accept (recommended: Rule 6 allows weather abilities from this split, one team per route), or change them to Rain Dance and Sunny Day, which last five turns. |
| 5 | The restaurant's format | The restaurant fights its 18 trainers in pairs, two against the player in one double (the Overseer, from its scripts, 2026-10-07). Each file is now one half of a pair, two Pokemon each, built with the doubles recipes. | The scorer cannot read doubles yet. | Answered (2026-10-07). |

Barry's Ambipom keeps Last Resort, the split's one conditional attack. Two of
the gym's trainers top out at 42 rather than one under the cap: Erick's
Gyarados and Samson's Kingler read past the band at 43 in the rain. Artist
Ismael's old Smeargle can only use Sketch under the final lists, so it gives
way to Mr. Mime, Delcatty and Gardevoir. The Pokemon Mansion's five maids keep
Clefairy at their centre and top out at 42 each, the first maid softest.

## What comes next

The ordinary trainers of the later splits, then a re-read of the bosses on
the updated simulator.

## Overview

| Trainer | Place | Path | Battle | Size | Levels | The idea | Expected |
|---|---|---|---|---|---|---|---|
| Tuber Trenton | Route 219 (by water) | optional | single | 3 | 40 to 42 | Drizzle | 99 / 1.03 / 31 blind in my simulator, about 72 clean in the scorer's terms |
| Tuber Mariel | Route 219 (by water) | optional | single | 3 | 39 to 42 | Huge Power Azumarill behind Quagsire's Unaware and Yawn and a Lanturn on the Red Card that Mariel awards | 99 / 1.00 / 31 blind in my simulator, about 72 clean in the scorer's terms |
| Fisherman Cody | Route 208 (by water) | optional | single | 3 | 41 to 43 | Moxie | 99 / 1.24 / 26 blind in my simulator, about 70 clean in the scorer's terms |
| Ruin Maniac Bryan | Route 214 | optional | single | 3 | 41 to 42 | Stealth Rock from Bastiodon with Roar | 98 / 1.15 / 34 blind in my simulator, about 74 clean in the scorer's terms |
| Ruin Maniac Ronald | Route 214 | optional | single | 4 | 40 to 42 | Sheer Force Feraligatr's Dragon Dance | 98 / 1.17 / 19 blind in my simulator, about 68 clean in the scorer's terms |
| Psychic Mitchell | Route 214 | on the path | single | 3 | 41 to 42 | Screens and a Calm Mind | 100 / 0.76 / 40 blind in my simulator, about 76 clean in the scorer's terms |
| Psychic Abigail | Route 214 | on the path | single | 3 | 41 to 42 | Fake Out and sleep | 98 / 0.88 / 45 blind in my simulator, about 78 clean in the scorer's terms |
| PI Carlos | Route 214 | optional | single | 3 | 41 to 42 | Critical hits | 98 / 0.70 / 53 blind in my simulator, about 81 clean in the scorer's terms |
| Collector Douglas | Route 214 | on the path | single | 3 | 41 to 42 | Water Spout at full HP from Wailord | 100 / 0.69 / 41 blind in my simulator, about 76 clean in the scorer's terms |
| Collector Jamal | Route 214 | optional | single | 3 | 41 to 42 | An Eviolite Porygon2 with Download | 98 / 0.47 / 71 blind in my simulator, about 88 clean in the scorer's terms |
| Beauty Devon | Route 214 | on the path | single | 3 | 41 to 42 | Spikes from Roserade | 97 / 0.82 / 51 blind in my simulator, about 81 clean in the scorer's terms |
| Ace Trainer Krystal | Route 214 | optional | single, Ace Trainer | 6 | 42 to 43 | Ian's mixed six on legal sets | about 100 / 0.1 / 91 with a planned six |
| Galactic Grunt | Valor Lakefront | optional | single | 3 | 40 to 42 | Poison from Team Galactic | 95 / 0.95 / 56 blind in my simulator, about 82 clean in the scorer's terms |
| Swimmer Sheltin | Route 213 | optional | single | 3 | 41 to 42 | Sniper Kingdra on a Scope Lens with Focus Energy | 99 / 0.70 / 50 blind in my simulator, about 80 clean in the scorer's terms |
| Swimmer Evan | Route 213 | optional | single | 3 | 41 to 42 | Burns and sleep in the water | 99 / 0.52 / 65 blind in my simulator, about 86 clean in the scorer's terms |
| Swimmer Haley | Route 213 | optional | single | 3 | 40 to 42 | Water and Psychic | 99 / 1.17 / 30 blind in my simulator, about 72 clean in the scorer's terms |
| Swimmer Mary | Route 213 | optional | single | 3 | 41 to 42 | Raichu's Fake Out | 99 / 0.89 / 35 blind in my simulator, about 74 clean in the scorer's terms |
| Tuber Jared | Route 213 | on the path | single | 3 | 39 to 42 | Drizzle and Swift Swim | 95 / 1.44 / 29 blind in my simulator, about 72 clean in the scorer's terms |
| Tuber Chelsea | Route 213 | on the path | single | 3 | 40 to 42 | Water Fairies | 100 / 0.72 / 39 blind in my simulator, about 76 clean in the scorer's terms |
| Sailor Paul | Route 213 | optional | single | 4 | 40 to 42 | Toxic Spikes from Tentacruel | 100 / 1.05 / 27 blind in my simulator, about 71 clean in the scorer's terms |
| Fisherman Kenneth | Route 213 | optional | single | 4 | 40 to 42 | Lanturn on the Covert Cloak that Kenneth awards | 98 / 1.07 / 29 blind in my simulator, about 71 clean in the scorer's terms |
| Beauty Cyndy | Route 213 | on the path | single | 4 | 41 to 42 | Stun Spore from a Focus Sash Beautifly | 98 / 1.05 / 39 blind in my simulator, about 75 clean in the scorer's terms |
| Fisherman Erick | Pastoria Gym (rain) | gym trainer | single | 3 | 39 to 42 | Wake's Spikes and Wacan Berry together | 98 / 1.46 / 12 blind in my simulator in rain, about 65 clean in the scorer's terms |
| Sailor Damian | Pastoria Gym (rain) | gym trainer | single | 3 | 41 to 43 | Swift Swim and Spikes | 95 / 1.34 / 28 blind in my simulator in rain, about 71 clean in the scorer's terms |
| Fisherman Walter | Pastoria Gym (rain) | gym trainer | single | 3 | 41 to 43 | Healing in the rain | 96 / 1.27 / 26 blind in my simulator in rain, about 70 clean in the scorer's terms |
| Sailor Samson | Pastoria Gym (rain) | gym trainer | single | 3 | 41 to 42 | Toxic Spikes from Tentacruel | 98 / 1.37 / 26 blind in my simulator in rain, about 70 clean in the scorer's terms |
| Tuber Jacky | Pastoria Gym (rain) | gym trainer | single | 3 | 41 to 43 | Poison Heal | 100 / 0.80 / 43 blind in my simulator in rain, about 77 clean in the scorer's terms |
| Tuber Caitlyn | Pastoria Gym (rain) | gym trainer | single | 3 | 40 to 42 | A Light Ball Pikachu with Fake Out | 98 / 1.17 / 22 blind in my simulator in rain, about 69 clean in the scorer's terms |
| Wake | Pastoria Gym | on the path | single, boss | 6 | 42 to 44 | Swift Swim in his gym's permanent rain | about 55 / 4.6 / 0 in my simulator in the gym's rain, where today's file reads 71 / 4.1 / 0 |
| Barry 4 | Pastoria City | on the path | single, boss | 6 | 41 to 44 | Barry's skeleton grows a member | about 100 / 2.0 / 2 in my simulator, where today's file reads 100 / 0.0 / 97 |
| Rich Boy Jason | Route 212 north | optional | single | 3 | 40 to 42 | Sheer Force Feraligatr on a Mystic Water | 97 / 0.94 / 35 blind in my simulator, about 74 clean in the scorer's terms |
| Lady Melissa | Route 212 north | optional | single | 3 | 40 to 42 | Unburden Sceptile | 98 / 0.39 / 78 blind in my simulator, about 91 clean in the scorer's terms |
| Gentleman Jeremy | Route 212 north | optional | single | 3 | 40 to 42 | Chatot's Chatter and Taunt | 99 / 0.34 / 72 blind in my simulator, about 89 clean in the scorer's terms |
| Socialite Reina | Route 212 north | optional | single | 3 | 41 to 42 | Jumpluff's Sleep Powder | 99 / 0.36 / 74 blind in my simulator, about 90 clean in the scorer's terms |
| Policeman Bobby | Route 212 north | optional | single | 3 | 40 to 42 | Police dogs and a Guts Swellow | 99 / 0.56 / 58 blind in my simulator, about 83 clean in the scorer's terms |
| Policeman Alex | Route 212 north | optional | single | 3 | 40 to 42 | Intimidate twice | 99 / 0.69 / 47 blind in my simulator, about 79 clean in the scorer's terms |
| Policeman Dylan | Route 212 north | optional | single | 3 | 40 to 42 | A Thick Club Marowak behind Dodrio's Tri Attack and Granbull's Bulk Up | 100 / 0.51 / 56 blind in my simulator, about 83 clean in the scorer's terms |
| Fisherman Juan | Route 212 south | optional | single | 3 | 40 to 42 | Gorebyss's Scald and Draining Kiss | 100 / 0.64 / 46 blind in my simulator, about 79 clean in the scorer's terms |
| Fisherman Josh | Route 212 south | optional | single | 4 | 40 to 42 | Kingler's Crabhammer on the Wide Lens that Josh awards | 98 / 1.15 / 32 blind in my simulator, about 73 clean in the scorer's terms |
| Fisherman Travis | Route 212 south | optional | single | 3 | 40 to 42 | Wailord's Water Spout at full HP behind Qwilfish's Thunder Wave and a Sniper Octillery | 100 / 0.73 / 43 blind in my simulator, about 77 clean in the scorer's terms |
| Pkmn Ranger Taylor | Route 212 south | optional | single | 3 | 40 to 42 | Grass and lightning | 100 / 0.75 / 38 blind in my simulator, about 75 clean in the scorer's terms |
| Pkmn Ranger Jeffrey | Route 212 south | optional | single | 3 | 40 to 42 | Sheer Force Tauros | 99 / 0.59 / 57 blind in my simulator, about 83 clean in the scorer's terms |
| Pkmn Ranger Allison | Route 212 south | optional | single | 3 | 40 to 42 | Leafeon's Swords Dance | 96 / 0.62 / 69 blind in my simulator, about 88 clean in the scorer's terms |
| Scientist Stefano | Route 212 south | optional | single | 3 | 40 to 42 | Rotom's Will-O-Wisp then Hex | 96 / 1.06 / 44 blind in my simulator, about 77 clean in the scorer's terms |
| Policeman Caleb | Route 212 north | optional | single | 3 | 40 to 42 | Stealth Rock from a Rough Skin Sandslash | 95 / 1.02 / 46 blind in my simulator, about 78 clean in the scorer's terms |
| Parasol Lady Alexa | Route 212 south | optional | single | 3 | 40 to 42 | Drought | 97 / 0.87 / 56 blind in my simulator, about 82 clean in the scorer's terms |
| Parasol Lady Sabrina | Route 212 south | optional | single | 4 | 40 to 42 | Flowers | 97 / 0.56 / 75 blind in my simulator, about 90 clean in the scorer's terms |
| Policeman Danny | Route 212 south | optional | single | 3 | 40 to 42 | Electivire's elemental punches | 99 / 0.91 / 40 blind in my simulator, about 76 clean in the scorer's terms |
| Collector Dean | Route 212 south | optional | single | 4 | 40 to 42 | Eeveelutions | 99 / 0.79 / 41 blind in my simulator, about 76 clean in the scorer's terms |
| Scientist Shaun | Route 212 south | optional | single | 3 | 40 to 42 | Magnezone on the Weakness Policy that Shaun awards | 98 / 0.86 / 56 blind in my simulator, about 82 clean in the scorer's terms |
| Aroma Lady Alison | Hotel Grand Lake restaurant | optional | double with Collector Eugene | 2 | 40 to 41 | Half of a double with Collector Eugene | not readable yet (a double against two trainers) |
| Artist Ismael | Hotel Grand Lake restaurant | optional | double with Beauty Harley | 2 | 40 to 41 | Half of a double with Beauty Harley | not readable yet (a double against two trainers) |
| Pkmn Breeder Kaylee | Hotel Grand Lake restaurant | optional | double with Scientist Emilio | 2 | 40 to 41 | Half of a double with Scientist Emilio | not readable yet (a double against two trainers) |
| Cameraman Darryl | Hotel Grand Lake restaurant | optional | double with Reporter Valerie | 2 | 40 to 41 | Half of a double with Reporter Valerie | not readable yet (a double against two trainers) |
| Collector Eugene | Hotel Grand Lake restaurant | optional | double with Aroma Lady Alison | 2 | 40 to 41 | Half of a double with Aroma Lady Alison | not readable yet (a double against two trainers) |
| Pokefan Meredith | Hotel Grand Lake restaurant | optional | double with School Kid Esteban | 2 | 40 to 41 | Half of a double with School Kid Esteban | not readable yet (a double against two trainers) |
| PI Kendrick | Hotel Grand Lake restaurant | optional | double with Beauty Gabriella | 2 | 40 to 41 | Half of a double with Beauty Gabriella | not readable yet (a double against two trainers) |
| Gentleman Leonardo | Hotel Grand Lake restaurant | optional | double with Socialite Rebecca | 2 | 40 to 41 | Half of a double with Socialite Rebecca | not readable yet (a double against two trainers) |
| Socialite Rebecca | Hotel Grand Lake restaurant | optional | double with Gentleman Leonardo | 2 | 40 to 41 | Half of a double with Gentleman Leonardo | not readable yet (a double against two trainers) |
| Lass Blythe | Hotel Grand Lake restaurant | optional | double with Veteran Emanuel | 2 | 40 to 41 | Half of a double with Veteran Emanuel | not readable yet (a double against two trainers) |
| Rich Boy Roman | Hotel Grand Lake restaurant | optional | double with Lady Kylie | 2 | 40 to 41 | Half of a double with Lady Kylie | not readable yet (a double against two trainers) |
| Lady Kylie | Hotel Grand Lake restaurant | optional | double with Rich Boy Roman | 2 | 40 to 41 | Half of a double with Rich Boy Roman | not readable yet (a double against two trainers) |
| Reporter Valerie | Hotel Grand Lake restaurant | optional | double with Cameraman Darryl | 2 | 40 to 41 | Half of a double with Cameraman Darryl | not readable yet (a double against two trainers) |
| School Kid Esteban | Hotel Grand Lake restaurant | optional | double with Pokefan Meredith | 2 | 40 to 41 | Half of a double with Pokefan Meredith | not readable yet (a double against two trainers) |
| Scientist Emilio | Hotel Grand Lake restaurant | optional | double with Pkmn Breeder Kaylee | 2 | 40 to 41 | Half of a double with Pkmn Breeder Kaylee | not readable yet (a double against two trainers) |
| Beauty Gabriella | Hotel Grand Lake restaurant | optional | double with PI Kendrick | 2 | 40 to 41 | Half of a double with PI Kendrick | not readable yet (a double against two trainers) |
| Beauty Harley | Hotel Grand Lake restaurant | optional | double with Artist Ismael | 2 | 40 to 41 | Half of a double with Artist Ismael | not readable yet (a double against two trainers) |
| Veteran Emanuel | Hotel Grand Lake restaurant | optional | double with Lass Blythe | 2 | 40 to 41 | Half of a double with Lass Blythe | not readable yet (a double against two trainers) |
| Rich Boy Liam | Pokemon Mansion | optional | single | 3 | 40 to 42 | Blissey's Softboiled and Toxic behind Lickilicky and a Sheer Force Tauros | 100 / 0.48 / 55 blind in my simulator, about 82 clean in the scorer's terms |
| Lady Celeste | Pokemon Mansion | optional | single | 3 | 40 to 42 | Blissey and Florges's Wish behind a Super Luck Togekiss | 99 / 0.50 / 64 blind in my simulator, about 85 clean in the scorer's terms |
| Maid Belinda | Pokemon Mansion | optional | single | 3 | 40 to 42 | The first maid | 98 / 0.46 / 72 blind in my simulator, about 89 clean in the scorer's terms |
| Maid Sophie | Pokemon Mansion | optional | single | 3 | 40 to 42 | Delcatty's Fake Out | 99 / 0.73 / 52 blind in my simulator, about 81 clean in the scorer's terms |
| Maid Emily | Pokemon Mansion | optional | single | 3 | 40 to 42 | Two Eviolite walls | 100 / 0.34 / 69 blind in my simulator, about 88 clean in the scorer's terms |
| Maid Elena | Pokemon Mansion | optional | single | 3 | 40 to 42 | Mr | 100 / 0.50 / 57 blind in my simulator, about 83 clean in the scorer's terms |
| Maid Clare | Pokemon Mansion | optional | single | 3 | 41 to 42 | The last maid | 98 / 0.43 / 74 blind in my simulator, about 89 clean in the scorer's terms |

Expected numbers are won / faints a fight / clean in my simulator, beside
today's file where it was read. For an ordinary trainer the clean rate is also
given in the scorer's terms, by the calibration in `read_split.py`.

## The trainers

### Tuber Trenton: Route 219 (by water), optional, single, cap 44

Drizzle: Politoed's rain lasts the whole fight, and Gastrodon's Dry Skin and Dewgong's Hydration feed on it. Politoed holds the Eject Button that Trenton awards.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Politoed | 42 | Eject Button | Drizzle | default | Scald, Ice Beam, Hypnosis, Low Sweep |
| Gastrodon | 41 | none | Dry Skin | default | Muddy Water, Earth Power, Ice Beam, Clear Smog |
| Dewgong | 40 | Leftovers | Hydration | default | Brine, Ice Beam, Knock Off, Encore |

Today's team: Gastrodon 43 (Hidden Power, Rain Dance, Sludge Bomb, Muddy Water), Dewgong 43 (Sheer Cold, Aqua Tail). Expected: 99 / 1.03 / 31 blind in my simulator, about 72 clean in the scorer's terms.

### Tuber Mariel: Route 219 (by water), optional, single, cap 44

Huge Power Azumarill behind Quagsire's Unaware and Yawn and a Lanturn on the Red Card that Mariel awards.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Lanturn | 41 | Red Card | Volt Absorb | default | Discharge, Surf, Ice Beam, Thunder Wave |
| Azumarill | 39 | none | Huge Power | default | Play Rough, Aqua Tail, Aqua Jet, Knock Off |
| Quagsire | 42 | Leftovers | Unaware | default | Earthquake, Waterfall, Yawn, Toxic |

Today's team: Azumarill 43 (Light Screen, Surf, Focus Blast, Ice Beam), Gastrodon 43 (Waterfall, Earthquake, Stone Edge, Sandstorm). Expected: 99 / 1.00 / 31 blind in my simulator, about 72 clean in the scorer's terms.

### Fisherman Cody: Route 208 (by water), optional, single, cap 44

Moxie: Gyarados's Thrash snowballs once it lands a knockout, behind Whiscash and a Sniper Octillery on a Scope Lens.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Whiscash | 41 | Soft Sand | Anticipation | default | Earthquake, Waterfall, Zen Headbutt, Rock Slide |
| Octillery | 41 | Scope Lens | Sniper | default | Scald, Ice Beam, Flamethrower, Energy Ball |
| Gyarados | 43 | none | Moxie | Adamant | Waterfall, Thrash, Ice Fang, Iron Head |

Today's team: Whiscash 44 (Magnitude, Rest, Snore, Aqua Tail), Gyarados 44 (Aqua Tail, Rain Dance, Crunch, Dragon Dance). Expected: 99 / 1.24 / 26 blind in my simulator, about 70 clean in the scorer's terms.

### Ruin Maniac Bryan: Route 214, optional, single, cap 44

Stealth Rock from Bastiodon with Roar, then Spiritomb's Will-O-Wisp and Hex and Torterra's Leech Seed. Kaizo's team, with Hex for its Payback.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Bastiodon | 41 | Chople Berry | Solid Rock | default | Stealth Rock, Iron Head, Rock Slide, Roar |
| Spiritomb | 41 | none | Pressure | default | Will-O-Wisp, Hex, Sucker Punch, Dark Pulse |
| Torterra | 42 | Leftovers | Thick Fat | default | Leech Seed, Wood Hammer, Earthquake, Synthesis |

Today's team: Hippowdon 36 (Leftovers; Stealth Rock, Yawn, Fire Fang, Sand Tomb), Corsola 37 (Zoom Lens; Toxic, Light Screen, Defense Curl, Rollout), Steelix 34 (Iron Plate; Iron Tail, Screech, Thunder Fang, Slam), Aerodactyl 36 (Lum Berry; Aerial Ace, Stone Edge, Thunder Fang, Tailwind), Leafeon 36 (Shell Bell; X-Scissor, Roar, Leaf Blade, Iron Tail). Expected: 98 / 1.15 / 34 blind in my simulator, about 74 clean in the scorer's terms.

### Ruin Maniac Ronald: Route 214, optional, single, cap 44

Sheer Force Feraligatr's Dragon Dance, behind Drifblim's Will-O-Wisp and Hex and a Guts Ursaring on a Flame Orb. Kaizo has no team here; today's idea, sharpened.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Drifblim | 40 | Sitrus Berry | Unburden | default | Shadow Ball, Will-O-Wisp, Thunderbolt, Hex |
| Dugtrio | 41 | none | Sand Veil | default | Earthquake, Sucker Punch, Night Slash, Rock Slide |
| Ursaring | 40 | Flame Orb | Guts | default | Facade, Crunch, Play Rough, StompingTantrum |
| Feraligatr | 42 | none | Sheer Force | default | Aqua Tail, Ice Fang, Crunch, Dragon Claw |

Today's team: Feraligatr 35 (Muscle Band; Dragon Dance, Superpower, Outrage, Aqua Tail), Drifblim 35 (Sitrus Berry; Selfdestruct, Payback, Tailwind, Shadow Ball), Dugtrio 36 (Focus Sash; Night Slash, Dig, Aerial Ace, Stone Edge), Chimecho 39 (Colbur Berry; Psychic, Calm Mind, Attract, Charge Beam), Ursaring 36 (Flame Orb; Facade, Superpower, ThunderPunch, Shadow Claw). Expected: 98 / 1.17 / 19 blind in my simulator, about 68 clean in the scorer's terms.

### Psychic Mitchell: Route 214, on the path, single, cap 44

Screens and a Calm Mind: Chimecho's Reflect and Light Screen, then Girafarig boosts behind them. Kaizo's Mitchell, with Dazzling Gleam and Alluring Voice.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Chimecho | 41 | none | Levitate | default | Reflect, Light Screen, Psychic, Dazzling Gleam |
| Raichu | 41 | Magnet | Lightning Rod | default | Thunderbolt, Surf, Alluring Voice, Thunder Wave |
| Girafarig | 42 | TwistedSpoon | Sap Sipper | Modest | Psychic, Shadow Ball, Thunderbolt, Calm Mind |

Today's team: Hypno 34 (Psycho Cut, Fire Punch, ThunderPunch, Drain Punch), Chimecho 34 (Psychic, Shadow Ball, Energy Ball, Thunder Wave). Expected: 100 / 0.76 / 40 blind in my simulator, about 76 clean in the scorer's terms.

### Psychic Abigail: Route 214, on the path, single, cap 44

Fake Out and sleep: Jynx's Fake Out and Lovely Kiss preview Wake's Fake Out, then Sableye's Prankster Will-O-Wisp and Hex, and Gardevoir's Mystical Fire.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Jynx | 41 | NeverMeltIce | Dry Skin | default | Fake Out, Ice Beam, Psychic, Lovely Kiss |
| Sableye | 41 | Leftovers | Prankster | default | Will-O-Wisp, Hex, Knock Off, Recover |
| Gardevoir | 42 | none | Magic Guard | default | Psychic, Dazzling Gleam, Mystical Fire, Thunderbolt |

Today's team: Wobbuffet 34 (Counter, Mirror Coat, Safeguard, Destiny Bond), Beldum 34 (Iron Head, Zen Headbutt), Exeggutor 34 (Energy Ball, Psychic, AncientPower, Synthesis). Expected: 98 / 0.88 / 45 blind in my simulator, about 78 clean in the scorer's terms.

### PI Carlos: Route 214, optional, single, cap 44

Critical hits: Super Luck on every member, Razor Claw and Scope Lens on high-crit moves, and Absol's Swords Dance. Kaizo's gambler loses his one-hit KO moves.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Persian | 41 | Razor Claw | Super Luck | default | Fake Out, Slash, Shadow Claw, Play Rough |
| Honchkrow | 41 | none | Super Luck | default | Drill Peck, Sucker Punch, Assurance, U-turn |
| Absol | 42 | Scope Lens | Super Luck | default | Sucker Punch, Knock Off, Slash, Shadow Claw |

Today's team: Seaking 36 (Horn Drill). Expected: 98 / 0.70 / 53 blind in my simulator, about 81 clean in the scorer's terms.

### Collector Douglas: Route 214, on the path, single, cap 44

Water Spout at full HP from Wailord, behind Typhlosion's Flash Fire and a Spell Tag Banette's Will-O-Wisp.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Typhlosion | 41 | Charcoal | Flash Fire | default | Flamethrower, Shadow Ball, Rock Slide, StompingTantrum |
| Banette | 41 | Spell Tag | Cursed Body | default | Shadow Claw, Knock Off, Sucker Punch, Will-O-Wisp |
| Wailord | 42 | none | Water Veil | Modest | Water Spout, Ice Beam, Brine, Rest |

Today's team: Banette 36 (Sticky Barb; Curse, Icy Wind, Will-O-Wisp, Shadow Sneak), Typhlosion 35 (Power Herb; Eruption, ThunderPunch, SolarBeam, Focus Blast), Octillery 37 (Scope Lens; Water Spout, Aurora Beam, Focus Energy, Signal Beam). Expected: 100 / 0.69 / 41 blind in my simulator, about 76 clean in the scorer's terms.

### Collector Jamal: Route 214, optional, single, cap 44

An Eviolite Porygon2 with Download, Noctowl's Moonblast and Hypnosis, and Grumpig's Calm Mind.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Porygon2 | 41 | Eviolite | Download | default | Thunderbolt, Ice Beam, Recover, Thunder Wave |
| Noctowl | 41 | none | Tinted Lens | default | Air Slash, Moonblast, Extrasensory, Hypnosis |
| Grumpig | 42 | Leftovers | Thick Fat | Calm | Calm Mind, Psychic, Dazzling Gleam, Shadow Ball |

Today's team: Porygon2 36 (Chople Berry; Recover, Thunderbolt, Psychic, Recycle), Noctowl 38 (Power Herb; Sky Attack, Recycle, Tailwind, Heat Wave), Grumpig 37 (Sitrus Berry; Calm Mind, Payback, Psychic, Recycle), Delibird 41 (Thick Club; Fling, Avalanche, Recycle, Gunk Shot). Expected: 98 / 0.47 / 71 blind in my simulator, about 88 clean in the scorer's terms.

### Beauty Devon: Route 214, on the path, single, cap 44

Spikes from Roserade, previewing Wake's hazard alone, then Clefable and a Marvel Scale Milotic.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Roserade | 41 | Black Sludge | Natural Cure | default | Spikes, Sludge Bomb, Giga Drain, Sleep Powder |
| Clefable | 41 | none | Magic Guard | default | Alluring Voice, Flamethrower, Moonlight, Thunder Wave |
| Milotic | 42 | Leftovers | Marvel Scale | default | Surf, Ice Beam, Dragon Pulse, Recover |

Today's team: Spinda 38 (Quick Claw; Teeter Dance, Faint Attack, Fake Out, Last Resort), Clefable 37 (Sitrus Berry; Follow Me, Belly Drum, Copycat, Last Resort). Expected: 97 / 0.82 / 51 blind in my simulator, about 81 clean in the scorer's terms.

### Ace Trainer Krystal: Route 214, optional, single, Ace Trainer, cap 44

Ian's mixed six on legal sets: Metang's Bullet Punch behind his Quick Claw, Glalie's Spikes, Jumpluff's Sleep Powder and U-turn behind a Yache Berry, Rotom's Will-O-Wisp, a Liechi Berry Blaziken with Bulk Up, and Dragonair's Dragon Rush.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Metang | 42 | Quick Claw | Clear Body | Adamant | Bullet Punch, Zen Headbutt, Flash Cannon, Rock Slide |
| Glalie | 42 | none | Solid Rock | default | Ice Beam, Crunch, Ice Shard, Spikes |
| Jumpluff | 42 | Yache Berry | Chlorophyll | Jolly | U-turn, Sleep Powder, Leech Seed, Giga Drain |
| Rotom | 42 | none | Levitate | default | Thunderbolt, Shadow Ball, Will-O-Wisp, Thunder Wave |
| Blaziken | 42 | Liechi Berry | Speed Boost | Adamant | Blaze Kick, Night Slash, Rock Slide, Bulk Up |
| Dragonair | 43 | Leftovers | Shed Skin | default | Dragon Rush, Waterfall, Ice Beam, Thunder Wave |

Today's team: Metang 41 (Quick Claw; Meteor Mash, DynamicPunch, Zen Headbutt, Gravity), Glalie 39 (Icicle Plate; Blizzard, Sing, Earthquake, Weather Ball), Jumpluff 42 (Yache Berry; U-turn, Sleep Powder, Cotton Spore, Encore), Rotom 40 (Life Orb; Thunder, Overheat, Will-O-Wisp, Sunny Day), Blaziken 38 (Liechi Berry; DynamicPunch, Stone Edge, Flare Blitz, Brave Bird), Dragonair 44 (Draco Plate; ExtremeSpeed, Fire Blast, Aqua Tail, Dragon Rush). Expected: about 100 / 0.1 / 91 with a planned six; read blind, 64 / 2.9 / 24.

### Galactic Grunt: Valor Lakefront, optional, single, cap 44

Poison from Team Galactic: Skuntank's Toxic then Hex, Crobat's Confuse Ray, and Toxicroak.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Skuntank | 40 | none | Aftermath | default | Poison Jab, Sucker Punch, Toxic, Hex |
| Crobat | 41 | Sharp Beak | Inner Focus | default | Cross Poison, Dual Wingbeat, U-turn, Confuse Ray |
| Toxicroak | 42 | Black Sludge | Poison Touch | default | Poison Jab, Drain Punch, Sucker Punch, Knock Off |

Today's team: Toxicroak 41 (Cross Chop, Sucker Punch, Ice Punch, Poison Jab). Expected: 95 / 0.95 / 56 blind in my simulator, about 82 clean in the scorer's terms.

### Swimmer Sheltin: Route 213, optional, single, cap 44

Sniper Kingdra on a Scope Lens with Focus Energy, behind Lanturn's Volt Absorb and a Speed Boost Sharpedo. Kaizo's Sniper Seadra, evolved.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Lanturn | 41 | none | Volt Absorb | default | Discharge, Surf, Dazzling Gleam, Thunder Wave |
| Sharpedo | 41 | Mystic Water | Speed Boost | default | Crunch, Waterfall, Ice Fang, Aqua Jet |
| Kingdra | 42 | Scope Lens | Sniper | Modest | Dragon Pulse, Surf, Ice Beam, Focus Energy |

Today's team: Gyarados 43 (Ice Fang, Aqua Tail, Bounce, Headbutt), Lanturn 43 (Discharge, Surf, Signal Beam, Confuse Ray), Sharpedo 43 (Crunch, Slash, Aqua Jet, Taunt). Expected: 99 / 0.70 / 50 blind in my simulator, about 80 clean in the scorer's terms.

### Swimmer Evan: Route 213, optional, single, cap 44

Burns and sleep in the water: Politoed's Scald and Hypnosis, Mantine's Water Absorb, Floatzel.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Politoed | 41 | none | Water Absorb | default | Scald, Ice Beam, Psychic, Hypnosis |
| Mantine | 41 | none | Water Absorb | default | Surf, Ice Beam, Air Cutter, Roost |
| Floatzel | 42 | Mystic Water | Swift Swim | default | Waterfall, Ice Fang, Crunch, Aqua Jet |

Today's team: Politoed 44 (Surf, Perish Song, Focus Blast, Rain Dance), Mantine 44 (Water Pulse, Signal Beam, Confuse Ray, Air Cutter). Expected: 99 / 0.52 / 65 blind in my simulator, about 86 clean in the scorer's terms.

### Swimmer Haley: Route 213, optional, single, cap 44

Water and Psychic: Golduck, Seaking's Knock Off and Slowbro's Yawn. Kaizo's rain team keeps no rain, since none of its species can learn Rain Dance in Oxide.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Golduck | 41 | Mystic Water | Damp | default | Scald, Ice Beam, Psychic, Aqua Jet |
| Seaking | 40 | none | Swift Swim | default | Waterfall, Poison Jab, Knock Off, Aqua Jet |
| Slowbro | 42 | Leftovers | Regenerator | default | Surf, Psychic, Ice Beam, Yawn |

Today's team: Golduck 43 (Aqua Jet, Zen Headbutt, Waterfall, Ice Punch), Slowbro 43 (Surf, Psychic, Shadow Ball, Slack Off). Expected: 99 / 1.17 / 30 blind in my simulator, about 72 clean in the scorer's terms.

### Swimmer Mary: Route 213, optional, single, cap 44

Raichu's Fake Out, Lumineon's U-turn and Lapras's Sing. Kaizo's Mary, with Alluring Voice.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Lumineon | 41 | none | Water Veil | default | U-turn, Surf, Ice Beam, Alluring Voice |
| Raichu | 41 | Magnet | Lightning Rod | default | Fake Out, Thunderbolt, Surf, Knock Off |
| Lapras | 42 | Leftovers | Hydration | default | Surf, Ice Beam, Sing, Thunderbolt |

Today's team: Lumineon 44 (Surf, Blizzard, Aqua Ring, Tailwind), Lapras 44 (Perish Song, Ice Beam, Brine, Safeguard). Expected: 99 / 0.89 / 35 blind in my simulator, about 74 clean in the scorer's terms.

### Tuber Jared: Route 213, on the path, single, cap 44

Drizzle and Swift Swim, previewing Wake's: Politoed's rain lasts the whole fight, Seaking moves at double speed two levels down, and Gastrodon's Dry Skin heals.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Politoed | 42 | Mystic Water | Drizzle | default | Scald, Ice Beam, Psychic, Low Sweep |
| Gastrodon | 40 | Leftovers | Dry Skin | default | Muddy Water, Earth Power, Ice Beam, Clear Smog |
| Seaking | 39 | none | Swift Swim | default | Waterfall, Poison Jab, Knock Off, Aqua Jet |

Today's team: Gastrodon 36 (Surf, Hidden Power, Rain Dance, Earth Power), Luvdisc 36 (Surf, Ice Beam, Sweet Kiss, Hidden Power), Gastrodon 36 (Waterfall, Stone Edge, Rain Dance, Earthquake). Expected: 95 / 1.44 / 29 blind in my simulator, about 72 clean in the scorer's terms.

### Tuber Chelsea: Route 213, on the path, single, cap 44

Water Fairies: a Huge Power Azumarill, Primarina's Sparkling Aria and Wigglytuff's Dazzling Gleam.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Azumarill | 40 | none | Huge Power | default | Play Rough, Aqua Tail, Aqua Jet, Knock Off |
| Wigglytuff | 41 | Sitrus Berry | Cute Charm | default | Dazzling Gleam, Flamethrower, Ice Beam, Thunderbolt |
| Primarina | 42 | none | Liquid Voice | default | Sparkling Aria, Alluring Voice, Ice Beam, Psychic |

Today's team: Azumarill 37 (Waterfall, Ice Punch, Superpower, Aqua Jet). Expected: 100 / 0.72 / 39 blind in my simulator, about 76 clean in the scorer's terms.

### Sailor Paul: Route 213, optional, single, cap 44

Toxic Spikes from Tentacruel, then Granbull's Bulk Up, Pelipper's Scald and a No Guard Machamp. Kaizo's sailor, with Play Rough and Scald.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Tentacruel | 40 | Black Sludge | Clear Body | default | Toxic Spikes, Scald, Sludge Bomb, Knock Off |
| Granbull | 41 | none | Intimidate | default | Bulk Up, Play Rough, Thunder Fang, StompingTantrum |
| Pelipper | 41 | none | Unburden | default | Scald, U-turn, Roost, Knock Off |
| Machamp | 42 | Black Belt | No Guard | default | Close Combat, Knock Off, Bullet Punch, Rock Slide |

Today's team: Tentacruel 44 (Waterfall, Acupressure, Poison Jab, Screech), Pelipper 44 (Stockpile, Swallow, Spit Up, Fly), Kingler 44 (Guillotine). Expected: 100 / 1.05 / 27 blind in my simulator, about 71 clean in the scorer's terms.

### Fisherman Kenneth: Route 213, optional, single, cap 44

Lanturn on the Covert Cloak that Kenneth awards, beside Lumineon's U-turn, Huntail and a Rock Head Relicanth. Kaizo's team, its Swift Swim gone with the rain.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Lumineon | 40 | none | Water Veil | default | U-turn, Surf, Ice Beam, Dazzling Gleam |
| Huntail | 42 | none | Water Veil | default | Crunch, Ice Fang, Aqua Tail, Sucker Punch |
| Lanturn | 41 | Covert Cloak | Volt Absorb | default | Discharge, Surf, Ice Beam, Thunder Wave |
| Relicanth | 42 | Hard Stone | Rock Head | default | Waterfall, Rock Slide, Take Down, StompingTantrum |

Today's team: Remoraid 36 (Aurora Beam, Flamethrower, Water Pulse, Signal Beam), Wailmer 36 (Rain Dance, Ice Beam, Surf, Water Spout), Gyarados 36 (Headbutt, Dragon Dance, Ice Fang, Aqua Tail). Expected: 98 / 1.07 / 29 blind in my simulator, about 71 clean in the scorer's terms.

### Beauty Cyndy: Route 213, on the path, single, cap 44

Stun Spore from a Focus Sash Beautifly, then Altaria, Lopunny's Fake Out and Triple Axel, and Mawile's Intimidate. Kaizo's Cyndy.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Beautifly | 41 | Focus Sash | Tinted Lens | default | Stun Spore, Bug Buzz, Air Slash, Energy Ball |
| Altaria | 41 | none | Cloud Nine | default | Dragon Pulse, Dazzling Gleam, Roost, Flamethrower |
| Lopunny | 41 | none | Scrappy | default | Fake Out, Return, Jump Kick, Triple Axel |
| Mawile | 42 | Silk Scarf | Intimidate | default | Play Rough, Iron Head, Sucker Punch, Crunch |

Today's team: Persian 37 (Gunk Shot, Shadow Claw, Seed Bomb, Slash). Expected: 98 / 1.05 / 39 blind in my simulator, about 75 clean in the scorer's terms.

### Fisherman Erick: Pastoria Gym (rain), gym trainer, single, cap 44

Wake's Spikes and Wacan Berry together: Qwilfish lays Spikes, Lanturn's Volt Absorb answers Electric attacks, and Gyarados holds a Wacan Berry.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Qwilfish | 41 | none | Intimidate | default | Spikes, Waterfall, Poison Jab, Thunder Wave |
| Lanturn | 39 | none | Volt Absorb | default | Discharge, Surf, Ice Beam, Dazzling Gleam |
| Gyarados | 42 | Wacan Berry | Intimidate | default | Waterfall, Ice Fang, Bounce, Iron Head |

Today's team: Lanturn 39 (Thunderbolt, Ice Beam, Surf, Signal Beam), Crawdaunt 39 (Knock Off, Waterfall, Superpower, Night Slash), Gyarados 39 (Dragon Dance, Ice Fang, Aqua Tail, Earthquake). Expected: 98 / 1.46 / 12 blind in my simulator in rain, about 65 clean in the scorer's terms.

### Sailor Damian: Pastoria Gym (rain), gym trainer, single, cap 44

Swift Swim and Spikes: Floatzel moves at double speed two levels down, and a Skill Link Cloyster lays Spikes and fires Icicle Spear.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Pelipper | 41 | Sitrus Berry | Unburden | default | Scald, U-turn, Roost, Knock Off |
| Floatzel | 41 | Mystic Water | Swift Swim | default | Waterfall, Ice Fang, Crunch, Aqua Jet |
| Cloyster | 43 | none | Skill Link | default | Icicle Spear, Rock Blast, Spikes, Ice Shard |

Today's team: Pelipper 39 (Surf, Sky Attack, Roost, Rain Dance), Cloyster 39 (Icicle Spear, Rock Blast, Poison Jab, Brine). Expected: 95 / 1.34 / 28 blind in my simulator in rain, about 71 clean in the scorer's terms.

### Fisherman Walter: Pastoria Gym (rain), gym trainer, single, cap 44

Healing in the rain: Whiscash's Hydration cures its own Rest, Toxicroak's Dry Skin heals, and Drapion's Poison Fang badly poisons.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Toxicroak | 41 | none | Dry Skin | default | Poison Jab, Drain Punch, Sucker Punch, Bullet Punch |
| Whiscash | 42 | Leftovers | Hydration | default | Earthquake, Waterfall, Rest, Zen Headbutt |
| Drapion | 43 | Black Sludge | Battle Armor | default | Poison Fang, Knock Off, Ice Fang, StompingTantrum |

Today's team: Whiscash 39 (Aqua Tail, Magnitude, Zen Headbutt). Expected: 96 / 1.27 / 26 blind in my simulator in rain, about 70 clean in the scorer's terms.

### Sailor Samson: Pastoria Gym (rain), gym trainer, single, cap 44

Toxic Spikes from Tentacruel, then Golduck and Kingler's Crabhammer.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Tentacruel | 41 | Black Sludge | Clear Body | default | Toxic Spikes, Scald, Sludge Bomb, Knock Off |
| Golduck | 41 | Leftovers | Damp | default | Surf, Ice Beam, Psychic, Aqua Jet |
| Kingler | 42 | none | Hyper Cutter | default | Crabhammer, Knock Off, X-Scissor, Rock Slide |

Today's team: Tentacruel 39 (Ice Beam, Surf, Sludge Bomb, Toxic Spikes), Kingler 39 (Metal Claw, Stomp, Knock Off, Guillotine), Golduck 39 (Aqua Jet, Zen Headbutt, Cross Chop, Ice Punch). Expected: 98 / 1.37 / 26 blind in my simulator in rain, about 70 clean in the scorer's terms.

### Tuber Jacky: Pastoria Gym (rain), gym trainer, single, cap 44

Poison Heal: Lickilicky's Toxic Orb powers Facade and heals it each turn, beside Quagsire's Unaware and Drifblim's Unburden. Kaizo's Jacky.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Drifblim | 41 | Sitrus Berry | Unburden | default | Shadow Ball, Thunderbolt, Will-O-Wisp, Hex |
| Quagsire | 42 | none | Unaware | default | Earthquake, Waterfall, Yawn, Toxic |
| Lickilicky | 43 | Toxic Orb | Poison Heal | default | Facade, Knock Off, Aqua Tail, StompingTantrum |

Today's team: Bibarel 39 (Hyper Fang, Yawn, Amnesia, Aqua Tail). Expected: 100 / 0.80 / 43 blind in my simulator in rain, about 77 clean in the scorer's terms.

### Tuber Caitlyn: Pastoria Gym (rain), gym trainer, single, cap 44

A Light Ball Pikachu with Fake Out, a Huge Power Azumarill and Politoed's Hypnosis. Kaizo's Caitlyn.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Azumarill | 40 | none | Huge Power | default | Aqua Tail, Play Rough, Aqua Jet, Knock Off |
| Politoed | 41 | Mystic Water | Water Absorb | default | Scald, Ice Beam, Psychic, Hypnosis |
| Pikachu | 42 | Light Ball | Reckless | Timid | Thunderbolt, Surf, Grass Knot, Fake Out |

Today's team: Lumineon 39 (Surf, Rain Dance, Safeguard, Aqua Ring), Seaking 39 (Poison Jab, Waterfall, Knock Off, Aqua Ring), Azumarill 39 (Belly Drum, Waterfall, Aqua Jet, Ice Punch). Expected: 98 / 1.17 / 22 blind in my simulator in rain, about 69 clean in the scorer's terms.

### Wake: Pastoria Gym, on the path, single, boss, cap 44

Swift Swim in his gym's permanent rain: Qwilfish lays Spikes behind a Focus Sash, Lanturn's Volt Absorb walls the Electric answers, then Ludicolo (Fake Out, Ice Beam), Gyarados (Earthquake, Stone Edge, a Wacan Berry), Sharpedo and a Life Orb Floatzel with Bulk Up and Aqua Jet. Grass and Electric types are the answers, and Lanturn, Gyarados's Earthquake and the Ice moves are aimed at them.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Qwilfish | 42 | Focus Sash | Swift Swim | Jolly | Spikes, Waterfall, Poison Jab, Thunder Wave |
| Lanturn | 42 | Leftovers | Volt Absorb | Modest | Surf, Discharge, Ice Beam, Confuse Ray |
| Ludicolo | 43 | Coba Berry | Swift Swim | Modest | Surf, Giga Drain, Ice Beam, Fake Out |
| Gyarados | 43 | Wacan Berry | Intimidate | Adamant | Waterfall, Earthquake, Ice Fang, Stone Edge |
| Sharpedo | 43 | Leftovers | Speed Boost | Adamant | Crunch, Waterfall, Ice Fang, Earthquake |
| Floatzel | 44 | Life Orb | Swift Swim | Adamant | Waterfall, Crunch, Aqua Jet, Bulk Up |

Today's team: Ludicolo 43 (Leftovers; Surf, Giga Drain, Leech Seed, Ice Beam), Quagsire 43 (Rindo Berry; Earthquake, Ice Punch, Waterfall, Yawn), Poliwrath 43 (Choice Scarf; Brick Break, Waterfall, Ice Punch, Earthquake), Gyarados 43 (Wacan Berry; Waterfall, Earthquake, Ice Fang, Thrash), Sharpedo 43 (Choice Band; Ice Fang, Crunch, Waterfall, Aqua Jet), Floatzel 44 (Life Orb; Ice Fang, Crunch, Waterfall, Aqua Jet). Expected: about 55 / 4.6 / 0 in my simulator in the gym's rain, where today's file reads 71 / 4.1 / 0; set aside, so today's file goes into alpha 1.

### Barry 4: Pastoria City, on the path, single, boss, cap 44

Barry's skeleton grows a member: the Ambipom Fake Out lead, Staraptor, a new Heracross with Close Combat and Stone Edge, Floatzel, Snorlax, and his starter at the cap (Torterra, Infernape or Empoleon by the player's choice).

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Ambipom | 41 | Silk Scarf | Technician | Jolly | Fake Out, Double Hit, U-turn, Last Resort |
| Staraptor | 42 | Sharp Beak | Intimidate | Adamant | Brave Bird, Close Combat, U-turn, Roost |
| Heracross | 42 | Lum Berry | Guts | Jolly | Close Combat, Night Slash, Stone Edge, Earthquake |
| Floatzel | 42 | Mystic Water | Swift Swim | Adamant | Waterfall, Ice Fang, Crunch, Brick Break |
| Snorlax | 43 | Leftovers | Thick Fat | Careful | Body Slam, Earthquake, Curse, Ice Punch |
| Torterra | 44 | Sitrus Berry | Thick Fat | Adamant | Wood Hammer, Earthquake, Crunch, Stone Edge |

Today's team: Staraptor 41 (White Herb; Aerial Ace, Quick Attack, Close Combat, Tailwind), Starmie 41 (Expert Belt; Surf, Psychic, Signal Beam, Recover), Snorlax 41 (Body Slam, Rest, Sleep Talk, Seismic Toss), Ninetales 41 (Flamethrower, Will-O-Wisp, Energy Ball, Confuse Ray), Torterra 42 (Leftovers; Wood Hammer, Bite, Earthquake, Leech Seed). Expected: about 100 / 2.0 / 2 in my simulator, where today's file reads 100 / 0.0 / 97.

### Rich Boy Jason: Route 212 north, optional, single, cap 44

Sheer Force Feraligatr on a Mystic Water, behind Persian's Technician Fake Out and Ninetales' Will-O-Wisp.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Persian | 40 | Leftovers | Technician | default | Fake Out, Bite, Play Rough, U-turn |
| Feraligatr | 41 | none | Intimidate | default | Waterfall, Ice Fang, Crunch, Dragon Claw |
| Ninetales | 42 | Charcoal | Magic Guard | default | Flamethrower, Extrasensory, Energy Ball, Will-O-Wisp |

Today's team: Feraligatr 37 (Waterfall, Aqua Jet, Crunch, Ice Punch). Expected: 97 / 0.94 / 35 blind in my simulator, about 74 clean in the scorer's terms.

### Lady Melissa: Route 212 north, optional, single, cap 44

Unburden Sceptile, faster once its Sitrus Berry is eaten, behind Bellossom's Stun Spore and a Super Luck Togekiss.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Bellossom | 40 | none | Chlorophyll | default | Giga Drain, Dazzling Gleam, Moonlight, Stun Spore |
| Togekiss | 41 | Leftovers | Super Luck | default | Air Slash, Aura Sphere, Dazzling Gleam, Roost |
| Sceptile | 42 | Sitrus Berry | Unburden | default | Leaf Blade, Dragon Claw, X-Scissor, Night Slash |

Today's team: Sceptile 37 (Night Slash, Earthquake, Leaf Blade, ThunderPunch). Expected: 98 / 0.39 / 78 blind in my simulator, about 91 clean in the scorer's terms.

### Gentleman Jeremy: Route 212 north, optional, single, cap 44

Chatot's Chatter and Taunt, Pidgeot's Air Slash, and Gardevoir's Calm Mind with Mystical Fire.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Chatot | 40 | Sitrus Berry | Big Pecks | default | Chatter, Air Cutter, U-turn, Taunt |
| Pidgeot | 41 | Sharp Beak | Intimidate | default | Air Slash, U-turn, Roost, Quick Attack |
| Gardevoir | 42 | none | Trace | default | Psychic, Dazzling Gleam, Mystical Fire, Calm Mind |

Today's team: Chatot 37 (Taunt, Mimic, Roost, Uproar). Expected: 99 / 0.34 / 72 blind in my simulator, about 89 clean in the scorer's terms.

### Socialite Reina: Route 212 north, optional, single, cap 44

Jumpluff's Sleep Powder, Leech Seed and Dual Wingbeat, behind Delcatty's Fake Out and a Defiant Purugly.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Roserade | 41 | Black Sludge | Technician | default | Magical Leaf, Sludge Bomb, Shadow Ball, Leech Seed |
| Lopunny | 41 | none | Scrappy | default | Fake Out, Return, Jump Kick, Triple Axel |
| Jumpluff | 42 | Leftovers | Chlorophyll | default | Dual Wingbeat, U-turn, Sleep Powder, Seed Bomb |

Today's team: Jumpluff 37 (Seed Bomb, Aerial Ace, Sleep Powder, U-turn). Expected: 99 / 0.36 / 74 blind in my simulator, about 90 clean in the scorer's terms.

### Policeman Bobby: Route 212 north, optional, single, cap 44

Police dogs and a Guts Swellow: Facade on a Flame Orb, Arcanine's Intimidate, Houndoom's Will-O-Wisp.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Houndoom | 40 | none | Flash Fire | default | Flamethrower, Dark Pulse, Sludge Bomb, Will-O-Wisp |
| Swellow | 41 | Flame Orb | Guts | default | Facade, Aerial Ace, U-turn, Quick Attack |
| Arcanine | 42 | none | Intimidate | default | Fire Fang, Wild Charge, Crunch, Roar |

Today's team: Swellow 34 (Quick Attack, Aerial Ace, Double Team, Endeavor), Arcanine 34 (Crunch, Roar, Fire Fang, Thunder Fang). Expected: 99 / 0.56 / 58 blind in my simulator, about 83 clean in the scorer's terms.

### Policeman Alex: Route 212 north, optional, single, cap 44

Intimidate twice, from Mightyena and Pidgeot, then Ninetales' Will-O-Wisp.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Mightyena | 40 | none | Intimidate | default | Crunch, Sucker Punch, Play Rough, Thunder Fang |
| Pidgeot | 41 | none | Intimidate | default | Air Slash, U-turn, Roost, Whirlwind |
| Ninetales | 42 | Charcoal | Magic Guard | default | Flamethrower, Extrasensory, Energy Ball, Will-O-Wisp |

Today's team: Pidgeotto 35 (Whirlwind, Aerial Ace, FeatherDance, Agility), Ninetales 35 (Flamethrower, Hidden Power, Confuse Ray, Will-O-Wisp). Expected: 99 / 0.69 / 47 blind in my simulator, about 79 clean in the scorer's terms.

### Policeman Dylan: Route 212 north, optional, single, cap 44

A Thick Club Marowak behind Dodrio's Tri Attack and Granbull's Bulk Up.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Granbull | 40 | none | Intimidate | default | Play Rough, Crunch, Thunder Fang, Bulk Up |
| Dodrio | 41 | Sharp Beak | Quick Feet | default | Tri Attack, Pluck, Knock Off, Quick Attack |
| Marowak | 42 | Thick Club | Rock Head | default | Bonemerang, StompingTantrum, Rock Slide, Knock Off |

Today's team: Dodrio 36 (Quick Attack, Brave Bird, Acupressure, Knock Off), Marowak 36 (Thick Club; Earthquake, Iron Head, ThunderPunch, Low Kick). Expected: 100 / 0.51 / 56 blind in my simulator, about 83 clean in the scorer's terms.

### Fisherman Juan: Route 212 south, optional, single, cap 44

Gorebyss's Scald and Draining Kiss, Huntail's Sucker Punch and Seaking's Scale Shot.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Seaking | 40 | none | Lightning Rod | default | Waterfall, Poison Jab, Knock Off, Scale Shot |
| Huntail | 42 | none | Water Veil | default | Crunch, Ice Fang, Aqua Tail, Sucker Punch |
| Gorebyss | 42 | Mystic Water | Hydration | default | Scald, Psychic, Ice Beam, Draining Kiss |

Today's team: Gorebyss 36 (Amnesia, Aqua Ring, Psychic, Surf). Expected: 100 / 0.64 / 46 blind in my simulator, about 79 clean in the scorer's terms.

### Fisherman Josh: Route 212 south, optional, single, cap 44

Kingler's Crabhammer on the Wide Lens that Josh awards, beside Sharpedo, Whiscash and Slowbro's Yawn. Kaizo's Josh, without Explosion.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Slowbro | 40 | none | Regenerator | default | Surf, Psychic, Ice Beam, Yawn |
| Sharpedo | 41 | Mystic Water | Speed Boost | default | Crunch, Waterfall, Ice Fang, Aqua Jet |
| Whiscash | 41 | none | Anticipation | default | Earthquake, Waterfall, Zen Headbutt, Rock Slide |
| Kingler | 42 | Wide Lens | Hyper Cutter | default | Crabhammer, Knock Off, X-Scissor, Rock Slide |

Today's team: Clamperl 35 (DeepSeaTooth; Blizzard, Surf, Confuse Ray, Hidden Power), Huntail 36 (Scary Face, Ice Fang, Aqua Tail, Sucker Punch). Expected: 98 / 1.15 / 32 blind in my simulator, about 73 clean in the scorer's terms.

### Fisherman Travis: Route 212 south, optional, single, cap 44

Wailord's Water Spout at full HP behind Qwilfish's Thunder Wave and a Sniper Octillery. Today's Qwilfish loses Explosion.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Qwilfish | 40 | none | Poison Point | default | Waterfall, Poison Jab, Taunt, Thunder Wave |
| Octillery | 41 | Scope Lens | Sniper | default | Scald, Ice Beam, Flamethrower, Energy Ball |
| Wailord | 42 | Leftovers | Water Veil | default | Water Spout, Ice Beam, Brine, Rest |

Today's team: Wailmer 38 (Rest, Brine, Water Spout, Amnesia), Qwilfish 38 (Waterfall, Poison Jab, Aqua Jet, Explosion). Expected: 100 / 0.73 / 43 blind in my simulator, about 77 clean in the scorer's terms.

### Pkmn Ranger Taylor: Route 212 south, optional, single, cap 44

Grass and lightning: Tropius's Harvest, Carnivine's Sleep Powder, and Luxray's Wild Charge.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Tropius | 40 | Sitrus Berry | Harvest | default | Leaf Blade, Air Cutter, Dragon Pulse, Synthesis |
| Carnivine | 41 | none | Levitate | default | Seed Bomb, Crunch, Sleep Powder, Knock Off |
| Luxray | 42 | BlackGlasses | Tinted Lens | default | Wild Charge, Crunch, Ice Fang, Fire Fang |

Today's team: Carnivine 28 (default moves), Luxio 30 (default moves). Expected: 100 / 0.75 / 38 blind in my simulator, about 75 clean in the scorer's terms.

### Pkmn Ranger Jeffrey: Route 212 south, optional, single, cap 44

Sheer Force Tauros, Stantler's Hypnosis and Sap Sipper, and Sudowoodo's Rock Head Wood Hammer.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Sudowoodo | 40 | none | Rock Head | default | Wood Hammer, Rock Slide, Sucker Punch, StompingTantrum |
| Stantler | 41 | Leftovers | Sap Sipper | default | Extrasensory, Thunderbolt, Shadow Ball, Hypnosis |
| Tauros | 42 | Hard Stone | Sheer Force | default | Zen Headbutt, Rock Slide, Iron Head, Wild Charge |

Today's team: Tauros 39 (Rest, Headbutt, Zen Headbutt, Earthquake). Expected: 99 / 0.59 / 57 blind in my simulator, about 83 clean in the scorer's terms.

### Pkmn Ranger Allison: Route 212 south, optional, single, cap 44

Leafeon's Swords Dance, behind Kangaskhan's Fake Out and Tsareena, whose Queenly Majesty blocks priority, with Trop Kick and Triple Axel.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Kangaskhan | 41 | none | Scrappy | default | Fake Out, Double-Edge, Crunch, Sucker Punch |
| Tsareena | 40 | Miracle Seed | Queenly Majesty | default | Trop Kick, Triple Axel, Knock Off, Rapid Spin |
| Leafeon | 42 | none | Magic Guard | default | Seed Bomb, X-Scissor, Knock Off, Swords Dance |

Today's team: Kangaskhan 39 (Dizzy Punch, Crunch, Endure, Outrage), Leafeon 39 (Razor Leaf, Quick Attack, Synthesis, Magical Leaf). Expected: 96 / 0.62 / 69 blind in my simulator, about 88 clean in the scorer's terms.

### Scientist Stefano: Route 212 south, optional, single, cap 44

Rotom's Will-O-Wisp then Hex, an Analytic Magnezone, and a Poison Touch Muk.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Rotom | 40 | Spell Tag | Levitate | default | Thunderbolt, Shadow Ball, Will-O-Wisp, Hex |
| Magnezone | 41 | none | Analytic | default | Thunderbolt, Flash Cannon, Tri Attack, Thunder Wave |
| Muk | 42 | Black Sludge | Poison Touch | default | Poison Jab, Shadow Sneak, Knock Off, Drain Punch |

Today's team: Muk 38 (Gunk Shot, Shadow Punch, Shadow Sneak, Ice Punch). Expected: 96 / 1.06 / 44 blind in my simulator, about 77 clean in the scorer's terms.

### Policeman Caleb: Route 212 north, optional, single, cap 44

Stealth Rock from a Rough Skin Sandslash, then Manectric and a Super Luck Honchkrow.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Sandslash | 42 | none | Rough Skin | default | Stealth Rock, StompingTantrum, Knock Off, Rapid Spin |
| Manectric | 40 | Magnet | Lightning Rod | default | Thunderbolt, Flamethrower, Signal Beam, Roar |
| Honchkrow | 40 | none | Super Luck | default | Drill Peck, Sucker Punch, U-turn, Dark Pulse |

Today's team: Honchkrow 35 (Haze, Aerial Ace, Swagger, Sucker Punch), Sandslash 35 (Earthquake, Crush Claw, Poison Jab, Brick Break). Expected: 95 / 1.02 / 46 blind in my simulator, about 78 clean in the scorer's terms.

### Parasol Lady Alexa: Route 212 south, optional, single, cap 44

Drought: Ninetales' sun lasts the whole fight, and Vileplume's Chlorophyll and Sunflora's Solar Power and one-turn Solar Beam feed on it. The route's one weather team.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Ninetales | 42 | Charcoal | Drought | default | Flamethrower, Energy Ball, Extrasensory, Will-O-Wisp |
| Vileplume | 40 | Black Sludge | Effect Spore | default | Giga Drain, Sludge Bomb, Sleep Powder, Moonlight |
| Sunflora | 41 | none | Solar Power | default | SolarBeam, Sludge Bomb, Dazzling Gleam, Growth |

Today's team: Vileplume 39 (Giga Drain, Sludge Bomb, Sleep Powder, Sunny Day). Expected: 97 / 0.87 / 56 blind in my simulator, about 82 clean in the scorer's terms.

### Parasol Lady Sabrina: Route 212 south, optional, single, cap 44

Flowers: Bellossom's Stun Spore and Moonlight, Florges's Wish, and a Technician Roserade.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Roserade | 40 | none | Technician | default | Magical Leaf, Sludge Bomb, Shadow Ball, Sleep Powder |
| Tsareena | 41 | none | Queenly Majesty | default | Trop Kick, Triple Axel, Knock Off, Rapid Spin |
| Bellossom | 41 | Leftovers | Chlorophyll | default | Giga Drain, Dazzling Gleam, Moonlight, Stun Spore |
| Florges | 42 | Miracle Seed | Flower Veil | default | Dazzling Gleam, Energy Ball, Psychic, Wish |

Today's team: Bellossom 39 (Energy Ball, Stun Spore, Sunny Day, Synthesis). Expected: 97 / 0.56 / 75 blind in my simulator, about 90 clean in the scorer's terms.

### Policeman Danny: Route 212 south, optional, single, cap 44

Electivire's elemental punches, Noctowl's Moonblast, and Machamp's Close Combat.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Electivire | 40 | none | Adaptability | default | ThunderPunch, Fire Punch, Brick Break, Quick Attack |
| Noctowl | 41 | Leftovers | Tinted Lens | default | Air Slash, Moonblast, Extrasensory, Roost |
| Machamp | 42 | none | Steadfast | default | Close Combat, StompingTantrum, Bullet Punch, Knock Off |

Today's team: Noctowl 37 (Heat Wave, Tailwind, Air Slash, Psychic), Machamp 37 (Cross Chop, Poison Jab, Bullet Punch, ThunderPunch). Expected: 99 / 0.91 / 40 blind in my simulator, about 76 clean in the scorer's terms.

### Collector Dean: Route 212 south, optional, single, cap 44

Eeveelutions: Umbreon's Toxic and Wish, Glaceon's Freeze-Dry, Vaporeon, and a Magic Bounce Espeon with Calm Mind.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Umbreon | 41 | Leftovers | Synchronize | default | Toxic, Wish, Snarl, Payback |
| Glaceon | 40 | none | Ice Body | default | Freeze-Dry, Ice Beam, Shadow Ball, Alluring Voice |
| Vaporeon | 41 | Leftovers | Water Absorb | default | Surf, Ice Beam, Wish, Haze |
| Espeon | 42 | none | Magic Bounce | default | Psychic, Dazzling Gleam, Shadow Ball, Calm Mind |

Today's team: Umbreon 37 (Toxic, Quick Attack, Confuse Ray, Sucker Punch), Espeon 37 (Signal Beam, Shadow Ball, Swift, Psychic). Expected: 99 / 0.79 / 41 blind in my simulator, about 76 clean in the scorer's terms.

### Scientist Shaun: Route 212 south, optional, single, cap 44

Magnezone on the Weakness Policy that Shaun awards, beside Electivire's Adaptability punches and an Eviolite Porygon2.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Electivire | 40 | none | Vital Spirit | default | ThunderPunch, Fire Punch, Brick Break, Quick Attack |
| Magnezone | 41 | Weakness Policy | Analytic | default | Thunderbolt, Flash Cannon, Tri Attack, Thunder Wave |
| Porygon2 | 42 | Eviolite | Download | default | Ice Beam, Thunderbolt, Recover, Thunder Wave |

Today's team: Magneton 37 (Flash Cannon, Thunderbolt, Tri Attack, Thunder Wave), Electabuzz 37 (Low Kick, Light Screen, ThunderPunch, Ice Punch). Expected: 98 / 0.86 / 56 blind in my simulator, about 82 clean in the scorer's terms.

### Aroma Lady Alison: Hotel Grand Lake restaurant, optional, double with Collector Eugene, cap 44

Half of a double with Collector Eugene: Bellossom's Stun Spore and a Technician Roserade's Leech Seed.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Bellossom | 40 | none | Chlorophyll | default | Giga Drain, Dazzling Gleam, Moonlight, Stun Spore |
| Roserade | 41 | Black Sludge | Technician | default | Magical Leaf, Sludge Bomb, Leech Seed, Shadow Ball |

Today's team: Roselia 28 (default moves). Expected: not readable yet (a double against two trainers).

### Artist Ismael: Hotel Grand Lake restaurant, optional, double with Beauty Harley, cap 44

Half of a double with Beauty Harley: Delcatty's Fake Out and Helping Hand, then Mr. Mime's screens over both sides of the pair.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Delcatty | 40 | none | Cute Charm | default | Fake Out, Helping Hand, Hyper Voice, Thunder Wave |
| Mr Mime | 41 | Leftovers | Filter | default | Reflect, Light Screen, Dazzling Gleam, Psychic |

Today's team: Smeargle 28 (default moves). Expected: not readable yet (a double against two trainers).

### Pkmn Breeder Kaylee: Hotel Grand Lake restaurant, optional, double with Scientist Emilio, cap 44

Half of a double with Scientist Emilio: Ambipom's Fake Out, then Altaria's spread Dazzling Gleam.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Ambipom | 40 | none | Technician | default | Fake Out, Double Hit, U-turn, Triple Axel |
| Altaria | 41 | Leftovers | Cloud Nine | default | Dazzling Gleam, Dragon Pulse, Roost, Flamethrower |

Today's team: Aipom 26 (default moves), Marill 26 (default moves), Swablu 26 (default moves). Expected: not readable yet (a double against two trainers).

### Cameraman Darryl: Hotel Grand Lake restaurant, optional, double with Reporter Valerie, cap 44

Half of a double with Reporter Valerie: Mr. Mime's screens, then an Analytic Magnezone on a Magnet.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Mr Mime | 40 | none | Filter | default | Reflect, Light Screen, Dazzling Gleam, Psybeam |
| Magnezone | 41 | Magnet | Levitate | default | Thunderbolt, Flash Cannon, Tri Attack, Thunder Wave |

Today's team: Magnemite 26 (default moves), Mr Mime 26 (default moves). Expected: not readable yet (a double against two trainers).

### Collector Eugene: Hotel Grand Lake restaurant, optional, double with Aroma Lady Alison, cap 44

Half of a double with Aroma Lady Alison: Lapras's Icy Wind slows the player's side, beside a Marvel Scale Milotic.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Lapras | 40 | none | Hydration | default | Icy Wind, Water Pulse, Ice Beam, Alluring Voice |
| Milotic | 41 | Leftovers | Marvel Scale | default | Water Pulse, Ice Beam, Dragon Pulse, Recover |

Today's team: Feebas 28 (default moves). Expected: not readable yet (a double against two trainers).

### Pokefan Meredith: Hotel Grand Lake restaurant, optional, double with School Kid Esteban, cap 44

Half of a double with School Kid Esteban: Raichu's Fake Out, then spread Discharge and Electroweb from Pachirisu beside Ground partners.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Raichu | 40 | none | Lightning Rod | default | Fake Out, Discharge, Grass Knot, Alluring Voice |
| Pachirisu | 41 | Sitrus Berry | Adaptability | default | Discharge, Electroweb, Super Fang, U-turn |

Today's team: Pichu 26 (Sitrus Berry; default moves), Pachirisu 26 (Sitrus Berry; default moves). Expected: not readable yet (a double against two trainers).

### PI Kendrick: Hotel Grand Lake restaurant, optional, double with Beauty Gabriella, cap 44

Half of a double with Beauty Gabriella: Granbull's Intimidate, then Kangaskhan's Fake Out and Silk Scarf Double-Edge.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Granbull | 40 | none | Intimidate | default | Play Rough, Thunder Fang, Crunch, StompingTantrum |
| Kangaskhan | 41 | Silk Scarf | Scrappy | default | Fake Out, Double-Edge, Crunch, Sucker Punch |

Today's team: Kangaskhan 31 (Dizzy Punch, Brick Break). Expected: not readable yet (a double against two trainers).

### Gentleman Leonardo: Hotel Grand Lake restaurant, optional, double with Socialite Rebecca, cap 44

Half of a double with Socialite Rebecca: Pidgeot's Tailwind and Chatot's spread Air Cutter and Chatter.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Chatot | 40 | none | Big Pecks | default | Chatter, Air Cutter, U-turn, Roost |
| Pidgeot | 41 | Sharp Beak | Intimidate | default | Tailwind, Air Slash, U-turn, Quick Attack |

Today's team: Chatot 27 (Mimic, Sing, Fury Attack, Roost). Expected: not readable yet (a double against two trainers).

### Socialite Rebecca: Hotel Grand Lake restaurant, optional, double with Gentleman Leonardo, cap 44

Half of a double with Gentleman Leonardo: Delcatty's Fake Out and Helping Hand, then a Defiant Purugly on a Silk Scarf.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Delcatty | 40 | none | Cute Charm | default | Fake Out, Helping Hand, Hyper Voice, Sucker Punch |
| Purugly | 41 | Silk Scarf | Defiant | default | Slash, Play Rough, Sucker Punch, Knock Off |

Today's team: Purugly 27 (default moves). Expected: not readable yet (a double against two trainers).

### Lass Blythe: Hotel Grand Lake restaurant, optional, double with Veteran Emanuel, cap 44

Half of a double with Veteran Emanuel: Clefable's Follow Me and Icy Wind, then a Silk Scarf Lopunny.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Clefable | 40 | none | Magic Guard | default | Follow Me, Alluring Voice, Icy Wind, Moonlight |
| Lopunny | 41 | Silk Scarf | Scrappy | default | Return, Jump Kick, Triple Axel, U-turn |

Today's team: Chingling 25 (default moves), Buneary 25 (default moves). Expected: not readable yet (a double against two trainers).

### Rich Boy Roman: Hotel Grand Lake restaurant, optional, double with Lady Kylie, cap 44

Half of a double with Lady Kylie: Tauros's Intimidate and spread Rock Slide, then Lickilicky.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Tauros | 40 | none | Intimidate | default | Rock Slide, Zen Headbutt, Iron Head, StompingTantrum |
| Lickilicky | 41 | Leftovers | Poison Heal | default | Body Slam, Knock Off, Ice Beam, Thunderbolt |

Today's team: Lickitung 26 (default moves). Expected: not readable yet (a double against two trainers).

### Lady Kylie: Hotel Grand Lake restaurant, optional, double with Rich Boy Roman, cap 44

Half of a double with Rich Boy Roman: Togekiss's Follow Me draws attacks while Clefable's Icy Wind slows both of the player's Pokemon.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Togekiss | 40 | none | Super Luck | default | Follow Me, Air Slash, Dazzling Gleam, Roost |
| Clefable | 41 | Leftovers | Magic Guard | default | Icy Wind, Alluring Voice, Flamethrower, Moonlight |

Today's team: Cleffa 24 (default moves), Clefairy 26 (default moves). Expected: not readable yet (a double against two trainers).

### Reporter Valerie: Hotel Grand Lake restaurant, optional, double with Cameraman Darryl, cap 44

Half of a double with Cameraman Darryl: Gardevoir's spread Dazzling Gleam behind the screens, and Rotom's Will-O-Wisp then Hex.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Rotom | 40 | none | Levitate | default | Thunderbolt, Shadow Ball, Will-O-Wisp, Hex |
| Gardevoir | 41 | Leftovers | Magic Guard | default | Dazzling Gleam, Psychic, Shadow Ball, Thunderbolt |

Today's team: Kirlia 26 (default moves). Expected: not readable yet (a double against two trainers).

### School Kid Esteban: Hotel Grand Lake restaurant, optional, double with Pokefan Meredith, cap 44

Half of a double with Pokefan Meredith: Whiscash and Quagsire are Ground types, immune to their partner's spread Discharge.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Whiscash | 40 | none | Hydration | default | Waterfall, Rock Slide, StompingTantrum, Ice Beam |
| Quagsire | 41 | Leftovers | Unaware | default | Waterfall, Ice Beam, Yawn, Toxic |

Today's team: Quagsire 26 (Mud Bomb, Slam, Water Gun, Amnesia). Expected: not readable yet (a double against two trainers).

### Scientist Emilio: Hotel Grand Lake restaurant, optional, double with Pkmn Breeder Kaylee, cap 44

Half of a double with Pkmn Breeder Kaylee: an Eviolite Porygon2's Thunder Wave and a Levitate Bronzong's spread Rock Slide and Hypnosis.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Porygon2 | 40 | Eviolite | Download | default | Ice Beam, Thunderbolt, Recover, Thunder Wave |
| Bronzong | 41 | none | Levitate | default | Gyro Ball, Psychic Noise, Rock Slide, Hypnosis |

Today's team: Kadabra 27 (default moves). Expected: not readable yet (a double against two trainers).

### Beauty Gabriella: Hotel Grand Lake restaurant, optional, double with PI Kendrick, cap 44

Half of a double with PI Kendrick: Lumineon's Tailwind, then Milotic.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Lumineon | 40 | none | Water Veil | default | Tailwind, Water Pulse, Ice Beam, Alluring Voice |
| Milotic | 41 | Leftovers | Marvel Scale | default | Water Pulse, Ice Beam, Dragon Pulse, Recover |

Today's team: Finneon 26 (default moves). Expected: not readable yet (a double against two trainers).

### Beauty Harley: Hotel Grand Lake restaurant, optional, double with Artist Ismael, cap 44

Half of a double with Artist Ismael: a Mystic Water Golduck's Scald behind the screens, and Vaporeon's Wish.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Vaporeon | 40 | Leftovers | Water Absorb | default | Water Pulse, Ice Beam, Wish, Haze |
| Golduck | 41 | Mystic Water | Damp | default | Scald, Ice Beam, Psychic, Aqua Jet |

Today's team: Psyduck 26 (default moves). Expected: not readable yet (a double against two trainers).

### Veteran Emanuel: Hotel Grand Lake restaurant, optional, double with Lass Blythe, cap 44

Half of a double with Lass Blythe: Hariyama's Fake Out, Helping Hand and Low Sweep, then Machamp's spread Rock Slide.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Hariyama | 40 | none | Thick Fat | default | Fake Out, Helping Hand, Drain Punch, Low Sweep |
| Machamp | 41 | Black Belt | No Guard | default | Close Combat, Rock Slide, Knock Off, Bullet Punch |

Today's team: Machoke 28 (Seismic Toss, Low Kick, Foresight), Bronzor 28 (Extrasensory, Tackle, Confuse Ray). Expected: not readable yet (a double against two trainers).

### Rich Boy Liam: Pokemon Mansion, optional, single, cap 44

Blissey's Softboiled and Toxic behind Lickilicky and a Sheer Force Tauros.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Lickilicky | 40 | none | Poison Heal | default | Body Slam, Knock Off, Ice Beam, Thunderbolt |
| Blissey | 41 | none | Natural Cure | default | Softboiled, Toxic, Chilling Water, Dazzling Gleam |
| Tauros | 42 | Hard Stone | Sheer Force | default | Zen Headbutt, Rock Slide, Iron Head, StompingTantrum |

Today's team: Blissey 35 (Rare Candy; default moves). Expected: 100 / 0.48 / 55 blind in my simulator, about 82 clean in the scorer's terms.

### Lady Celeste: Pokemon Mansion, optional, single, cap 44

Blissey and Florges's Wish behind a Super Luck Togekiss.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Florges | 40 | none | Flower Veil | default | Dazzling Gleam, Energy Ball, Psychic, Wish |
| Blissey | 41 | none | Natural Cure | default | Softboiled, Toxic, Chilling Water, Ice Beam |
| Togekiss | 42 | Leftovers | Super Luck | default | Air Slash, Aura Sphere, Dazzling Gleam, Roost |

Today's team: Blissey 35 (Rare Candy; Fling, Softboiled, Egg Bomb, Psychic). Expected: 99 / 0.50 / 64 blind in my simulator, about 85 clean in the scorer's terms.

### Maid Belinda: Pokemon Mansion, optional, single, cap 44

The first maid: an Eviolite Clefairy keeps today's Metronome and Sing, beside Wigglytuff and Miltank.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Clefairy | 40 | Eviolite | Magic Guard | default | Metronome, Sing, Alluring Voice, Icy Wind |
| Wigglytuff | 40 | none | Cute Charm | default | Dazzling Gleam, Flamethrower, Ice Beam, Thunderbolt |
| Miltank | 42 | Leftovers | Thick Fat | default | Body Slam, Milk Drink, Play Rough, StompingTantrum |

Today's team: Clefairy 25 (Metronome, Minimize, Meteor Mash, Endure). Expected: 98 / 0.46 / 72 blind in my simulator, about 89 clean in the scorer's terms.

### Maid Sophie: Pokemon Mansion, optional, single, cap 44

Delcatty's Fake Out, an Eviolite Clefairy, a Defiant Purugly.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Delcatty | 40 | none | Cute Charm | default | Fake Out, Hyper Voice, Sucker Punch, Thunder Wave |
| Clefairy | 40 | Eviolite | Magic Guard | default | Metronome, Alluring Voice, Icy Wind, Wish |
| Ambipom | 42 | Silk Scarf | Technician | default | Double Hit, Triple Axel, U-turn, Knock Off |

Today's team: Clefairy 27 (Metronome, Sing, Meteor Mash, Endure). Expected: 99 / 0.73 / 52 blind in my simulator, about 81 clean in the scorer's terms.

### Maid Emily: Pokemon Mansion, optional, single, cap 44

Two Eviolite walls, Chansey and Clefairy, then Lopunny's Fake Out.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Chansey | 40 | Eviolite | Natural Cure | default | Softboiled, Toxic, Chilling Water, Light Screen |
| Clefairy | 41 | Eviolite | Magic Guard | default | Metronome, Encore, Alluring Voice, Icy Wind |
| Lopunny | 42 | none | Scrappy | default | Fake Out, Return, Jump Kick, Triple Axel |

Today's team: Clefairy 29 (Metronome, Encore, Meteor Mash, Endure). Expected: 100 / 0.34 / 69 blind in my simulator, about 88 clean in the scorer's terms.

### Maid Elena: Pokemon Mansion, optional, single, cap 44

Mr. Mime's screens, Clefable, and Kangaskhan's Fake Out and Silk Scarf Double-Edge.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Mr Mime | 40 | none | Filter | default | Reflect, Light Screen, Dazzling Gleam, Psybeam |
| Clefable | 41 | none | Magic Guard | default | Metronome, Alluring Voice, Flamethrower, Moonlight |
| Kangaskhan | 42 | Silk Scarf | Scrappy | default | Fake Out, Double-Edge, Crunch, Sucker Punch |

Today's team: Clefairy 31 (Metronome, Swagger, Meteor Mash, Endure). Expected: 100 / 0.50 / 57 blind in my simulator, about 83 clean in the scorer's terms.

### Maid Clare: Pokemon Mansion, optional, single, cap 44

The last maid: Clefable's Calm Mind behind Blissey's Toxic and Miltank's Curse.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Blissey | 41 | none | Natural Cure | default | Softboiled, Toxic, Chilling Water, Dazzling Gleam |
| Miltank | 41 | Leftovers | Thick Fat | default | Body Slam, Milk Drink, Play Rough, Curse |
| Clefable | 42 | Leftovers | Magic Guard | Calm | Metronome, Alluring Voice, Calm Mind, Moonlight |

Today's team: Clefairy 33 (Metronome, Bounce, Meteor Mash, Endure). Expected: 98 / 0.43 / 74 blind in my simulator, about 89 clean in the scorer's terms.


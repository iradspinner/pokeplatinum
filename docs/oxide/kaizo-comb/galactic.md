# The comb: the Galactic split

**Every trainer of the Galactic split is now combed.** The bosses were combed
earlier. On 2026-10-07 I added all 41 ordinary trainers in walking order: the
Mt. Coronet grunts, Tyche and Hermes at Spear Pillar, and the optional
trainers of Routes 225 to 230 and Stark Mountain. Every file passes the
checker and the rule audit; the checker's only remarks are the moves outside
a species' lists that Ian's late-game ruling allows.

Kaizo has no teams for these trainers, so each idea is mine, built from
today's file. Each is moved fully into Oxide's Generation 5+ pool, since from
this split on a move need not be legal for the species (Ian, 2026-10-07), then
scaled to the dial.

| Check | Result |
|---|---|
| Single battles read blind (33) | 92 to 100 won, mean 96.8 |
| Clean, in the scorer's terms (Ian's band 80 to 85) | 62 to 94, mean 74 |
| Faints a fight, in the scorer's terms (Ian's band 0.1 to 0.25) | 0.1 to 1.3, mean 0.74 |
| Mt. Coronet's four gauntlet grunts read as one section | 93 won, 1.6 faints, 26 clean in my simulator |
| The same section with Somnu at its end | 6 won |
| Tag pairs on Stark Mountain (8 files) | not readable yet |
| Move slots that are Generation 5+ | 99 of 592, 17 percent |
| Hidden abilities | 42, on 26 of 41 teams |
| Element 7 items held | 10: eight Eviolites, a Rocky Helmet and an Assault Vest |

These trainers read harder than Ian's band and harder than Maylene's: about
three times his faints. The box at 65 knows no TMs, and against it this
split's Ace Trainers read only 4 to 64 won blind, so every fight here reads
harsh in my simulator. I softened each team until it won about 92 percent or
more, mostly by keeping the top level on the team's lead or wall and dropping
its heavy hitters, and the scorer's step 15 reading decides the rest. The
dragons read hardest: Outrage at 140 under Ian's rework is their strongest
move, and Dragon Claw in its place read harder still, since Outrage's recoil
wears the user down.

The four trainers who award a TM carry its move: Geneva's Xatu has Grass
Knot, Deshawn's Kecleon Drain Punch, Mallory's Masquerain Sludge Bomb and
Sam's Floatzel Waterfall. Only Black Belt Ray's tag pair has no modern move,
because its Gen 4 moves already do each job better: Breloom's Mach Punch and
Seed Bomb, Toxicroak's Sludge Bomb, Focus Blast and Vacuum Wave, and Lucario's
Aura Sphere and Flash Cannon.

My simulator gained the later items, the hidden abilities and the modern move
effects on 2026-10-07, and its Fake Out now works only on the first turn. The
ordinary trainers were read after those changes; the bosses' numbers below
come from before them, and their re-read follows.

## The bosses, combed earlier

**Refreshed 2026-10-07.** The expected numbers were read again after two
changes: a fix to my simulator, which had picked the player's lead by party
order when two choices looked equal and so skewed every earlier boss reading,
and the legality sweep against the final lists (origin/balance-tm-pass at
377312dbf0), which left this split unchanged: from Cyrus 3's split on, Ian allowed any move that fits a team (2026-10-07), so Cyrus 3 keeps today's Magma Storm and Draco Meteor. Ian ruled that every draft goes into step 12 as
drafted; the scorer's step 15 reading gives the real numbers, and he chooses
any retunes from them. My candidates are in `../retune-proposals-not-approved/`.

The bosses of the Galactic split are combed: Officers Somnu, Moira, Hesperid
and Argo on Mt. Coronet, Mars and Jupiter together at Spear Pillar, Cyrus in
the Distortion World, twelve Ace Trainers on Routes 225 to 229, the four Ace
tag pairs and Commanders Mars and Jupiter on Stark Mountain.

The cap is 65. Route 228 fights in permanent sand, and its three Ace Trainers
(Jose, Moira, Meagan) are built for it, with no Sand Veil. Mt. Coronet's 3F,
4F and Somnu on 5F are a gauntlet, so Somnu sits a level lower than the
officers outside it. No other map here has its own weather. My simulator
reads the bosses against the scorer's box at this split, which knows no TMs,
so they read harsher than they will once the TM pass lands. It now also
models Outrage's lock and the confusion after it, Wonder Guard, and Galarian
forms in the box, and Ian's move reworks of 2026-10-06 (Outrage and the
other rampage moves as one-turn attacks, the recharge moves without recharge,
multi-hit moves at 25 a hit); Cyrus 3, Felix and Rodolfo carry Outrage and
were read again under them. Cyrus 3 is today's file moved up to the cap's
levels, as Ian chose, and reads about 72 won to today's 97. Somnu reads
about 84 to today's 100 with her sleep restored. Moira and Argo now sit three
under the cap with sharper sets, as Ian's rule that levels follow importance
asks of officers, and read about 99 and 83 (Moira's hail lasts the whole
fight, as Oxide's battle code has it; under my earlier five-turn rule she read
97.5); Hesperid reads 95 and both
Stark Mountain commanders 95 to 96, to today's 100. Somnu's Hypno and Darkrai keep Dream Eater, the split's conditional
attacks. Ian's four-way reading showed that most of the officers' rise came
from their levels, which led to the new rule; it applies to the finished
splits at the legality sweep, so Hesperid, Somnu and the Stark commanders
keep their levels until then.
These files are built against the learnset lists of 2026-10-06 evening; the
single legality sweep after the TM pass covers them with every other split.

## Decisions for Ian

Ian answered the first four on 2026-10-06; the last three are new, from the
ordinary trainers. Cyrus 3 is today's file at the cap's levels,
Gyarados and Regirock included, exempt from the one-legendary rule and the
target of about 80; Somnu has more than one sleep source, her Darkrai keeping
Dark Void; and Moira and Argo get a little harder at lower levels.

| # | Decision | What the files do today | How it is checked | What Ian decides |
|---|---|---|---|---|
| 1 | Cyrus 3 (Ian: today's team at the cap's levels) | Today's six exactly, moved up by rank to 63 to 65. It has no hazard lead, which the dial asks of Cyrus, because Ian chose today's team. | `galactic_boss_cyrus_distortion_world.json`; the scorer's reading later. | Answered (2026-10-06). |
| 2 | Officers keep today's ideas, without the dice (Ian: Somnu keeps several sleep sources) | Somnu has three sleepers (Jumpluff, Hypno, and Darkrai's Dark Void, which the checker flags until the Balance Agent adds it to Darkrai's egg moves); Hesperid keeps one of today's four trades (three Explosions and a Destiny Bond); Argo keeps the Wonder Guard Shedinja and the Arena Trap Dugtrio. | The four files. | Accept (recommended). |
| 3 | Argo's Gengar | Sharper sets alone could not make Argo harder three levels down (about 98 won at best), so a Gengar takes Vespiquen's place; it reads about 83 in the corrected reading. | `dummy_834.json`. | Accept (recommended), or Vespiquen back at about 98. |
| 4 | Spear Pillar and Stark Mountain tags | Mars and Jupiter bring five each at 62 to 63, beside Barry; the four Ace pairs bring four each. | The scorer cannot read tag battles yet. | Nothing now. |
| 5 | Ordinary trainers past the band | They win 92 to 100 percent blind but cost about 0.74 Pokemon a fight in the scorer's terms against Ian's 0.1 to 0.25, against a box at 65 that knows no TMs. | The scorer's step 15 reading. | Accept for now (recommended), or soften them further now. |
| 6 | Mt. Coronet's gauntlet | The four grunts carry two members each, at 56 and 58, with chip and status; with three each the section read 16 to 55 won. As a section they read 93 won, but with Somnu at the end a blind six almost never gets through, since Somnu is a boss (84 won against a planned six). | My section reading; the scorer's later. | Read the section without Somnu and Somnu as a boss (recommended), or soften Somnu, which Ian's no-retune rule holds until step 15. |
| 7 | Tyche and Hermes lose Explosion | Today's named grunts carry three Explosions; the dial allows no forced trade on an ordinary trainer, so mine keep each idea (Life Orb and Sash attackers, Toxic Spikes, Light Screen, Swords Dance, Endure and Flail) without them. | `galactic_grunt_spear_pillar_1.json` and `_2.json`. | Accept (recommended), or give them back their Explosions. |

Ace Trainers stay as built (Ian, 2026-10-06): with a planned six these read
84 to 100 won in the corrected reading (Saul 84, Jose 86, the rest 98 to 100), after Jose's Swords Dance Garchomp and Saul's Curse
Snorlax (93) were taken down a notch.

## What comes next

Barry's split's ordinary trainers; Volkner's split is with another pass.

## Overview

| Trainer | Place | Path | Battle | Size | Levels | The idea | Expected |
|---|---|---|---|---|---|---|---|
| Galactic Grunt (Coronet 1F, 1) | Mt. Coronet 1F tunnel room | on the path | single | 4 | 61 to 63 | Rivals | 98 / 0.99 / 35 blind in my simulator, about 74 clean in the scorer's terms |
| Galactic Grunt (Coronet 1F, 2) | Mt. Coronet 1F tunnel room | on the path | single | 4 | 60 to 63 | Punishers | 97 / 1.34 / 33 blind in my simulator, about 73 clean in the scorer's terms |
| Galactic Grunt (Coronet 1F, 3) | Mt. Coronet 1F tunnel room | on the path | single | 4 | 61 to 63 | Water Spout and Belly Drum | 97 / 1.15 / 33 blind in my simulator, about 73 clean in the scorer's terms |
| Galactic Grunt (Coronet 3F, 1) | Mt. Coronet 3F | gauntlet, before Somnu | single | 2 | 56 to 58 | Burn | 100 / 0.15 / 85 blind in my simulator, about 94 clean in the scorer's terms |
| Galactic Grunt (Coronet 3F, 2) | Mt. Coronet 3F | gauntlet, before Somnu | single | 2 | 56 to 58 | Poison that follows you | 100 / 0.16 / 84 blind in my simulator, about 93 clean in the scorer's terms |
| Galactic Grunt (Coronet 4F, 1) | Mt. Coronet 4F | gauntlet, before Somnu | single | 2 | 56 to 58 | Bugs | 100 / 0.23 / 78 blind in my simulator, about 91 clean in the scorer's terms |
| Galactic Grunt (Coronet 4F, 2) | Mt. Coronet 4F | gauntlet, before Somnu | single | 2 | 56 to 58 | Burns and Yawn | 100 / 0.27 / 75 blind in my simulator, about 90 clean in the scorer's terms |
| Galactic Officer Moira | Mt. Coronet 5F | on the path | single, named officer | 6 | 60 to 62 | Moira's hail | about 99 / 2.2 / 0 in my simulator, where today's file reads 100 / 0.4 / 71 |
| Galactic Officer Somnu | Mt. Coronet 5F | gauntlet, closing 3F to 5F | single, named officer | 6 | 62 to 64 | Somnu's sleep | about 84 / 2.5 / 0 in my simulator, where today's file reads 100 / 0.2 / 80 |
| Galactic Officer Hesperid | Mt. Coronet 6F | on the path | single, named officer | 6 | 63 to 65 | Today's six kept to one trade | about 95 / 1.7 / 9 in my simulator, where today's file reads 100 / 0.2 / 82 |
| Galactic Officer Argo | Mt. Coronet 6F | on the path | single, named officer | 6 | 61 to 62 | Today's puzzle box | about 83 / 3.4 / 3 in my simulator, where today's file reads 100 / 0.3 / 75 |
| Galactic Grunt Tyche | Spear Pillar | on the path | single | 4 | 60 to 63 | Ian's named grunt kept to her idea | 94 / 1.70 / 21 blind in my simulator, about 68 clean in the scorer's terms |
| Galactic Grunt Hermes | Spear Pillar | on the path | single | 4 | 62 to 63 | Ian's named grunt kept to his idea | 98 / 1.23 / 22 blind in my simulator, about 69 clean in the scorer's terms |
| Commander Mars | Spear Pillar | on the path | tag with Jupiter, beside Barry | 5 | 62 to 63 | Mars 2's core at Spear Pillar | not readable yet (a tag battle) |
| Commander Jupiter | Spear Pillar | on the path | tag with Mars, beside Barry | 5 | 62 to 63 | Jupiter's poison at Spear Pillar | not readable yet (a tag battle) |
| Cyrus 3 | Distortion World | on the path | single, boss | 6 | 63 to 65 | Today's file moved up to the cap's levels | about 72 / 3.1 / 6 in my simulator, where today's file reads 97 / 1.3 / 31 |
| Bird Keeper Audrey | Route 225 | optional | single | 4 | 61 to 64 | Flying speed | 99 / 0.97 / 41 blind in my simulator, about 76 clean in the scorer's terms |
| Dragon Tamer Geoffrey | Route 225 | optional | single | 4 | 60 to 63 | Eviolite dragons | 94 / 1.74 / 18 blind in my simulator, about 67 clean in the scorer's terms |
| Ace Trainer Rodolfo | Route 225 | optional | single, Ace Trainer | 6 | 62 to 64 | A balanced core | about 99 / 2.0 / 2 with a planned six |
| Ace Trainer Quinn | Route 225 | optional | single, Ace Trainer | 6 | 62 to 64 | Bugs behind support | about 99 / 0.6 / 60 with a planned six |
| Ace Trainer Deanna | Route 225 | optional | single, Ace Trainer | 6 | 62 to 64 | Special attackers | about 100 / 0.2 / 80 with a planned six |
| Psychic Daisy | Route 225 | optional | single | 4 | 61 to 63 | Regenerator | 97 / 1.32 / 30 blind in my simulator, about 72 clean in the scorer's terms |
| Pkmn Ranger Dwayne | Route 225 | optional | single | 4 | 60 to 63 | Stealth Rock from a Rocky Helmet Skarmory | 93 / 1.66 / 22 blind in my simulator, about 69 clean in the scorer's terms |
| Pkmn Ranger Ashlee | Route 225 | optional | single | 4 | 61 to 63 | Glare | 97 / 0.97 / 40 blind in my simulator, about 76 clean in the scorer's terms |
| Bird Keeper Geneva | Route 226 | optional | single | 4 | 60 to 63 | Magic Bounce Xatu with Grass Knot (Geneva's reward TM) | 94 / 1.34 / 32 blind in my simulator, about 73 clean in the scorer's terms |
| Dragon Tamer Stanley | Route 226 | optional | single | 4 | 61 to 63 | Kingdra's Draco Meteor behind Eviolite Seadra and Dragonair and an Intimidate Gyarados | 96 / 1.35 / 29 blind in my simulator, about 72 clean in the scorer's terms |
| Ace Trainer Graham | Route 226 | optional | single, Ace Trainer | 6 | 62 to 64 | Fighting types | about 100 / 1.5 / 12 with a planned six |
| Swimmer Wade | Route 226 | optional | single | 4 | 61 to 63 | Speed Boost Sharpedo's Liquidation | 94 / 1.37 / 35 blind in my simulator, about 74 clean in the scorer's terms |
| Swimmer Lydia | Route 226 | optional | single | 4 | 60 to 63 | Water Spout from a full-health Wailord | 100 / 1.09 / 35 blind in my simulator, about 74 clean in the scorer's terms |
| Ace Trainer Saul | Route 227 | optional | single, Ace Trainer | 6 | 62 to 64 | Normal types | about 84 / 3.3 / 0 with a planned six |
| Ace Trainer Mikayla | Route 227 | optional | single, Ace Trainer | 6 | 62 to 64 | Dark types | about 98 / 1.1 / 13 with a planned six |
| Black Belt Griffin | Route 227 | optional | single | 4 | 60 to 63 | A Guts Machamp on a Flame Orb behind Hitmontop's Fake Out and Triple Axel | 97 / 1.23 / 31 blind in my simulator, about 72 clean in the scorer's terms |
| Pkmn Ranger Felicia | Route 227 | optional | single | 4 | 61 to 63 | Jumpluff's Sleep Powder and itemless Acrobatics | 98 / 1.07 / 34 blind in my simulator, about 74 clean in the scorer's terms |
| Bird Keeper Krystal | Stark Mountain room 2 | optional | tag beside Buck | 3 | 62 to 63 | Noctowl's Hypnosis then Dream Eater (the split's one conditional attack on an ordinary trainer) | not readable yet (a tag battle) |
| Dragon Tamer Darien | Stark Mountain | optional | single | 4 | 60 to 63 | Dragonite with Extreme Speed and Outrage behind an Eviolite Dragonair | 95 / 2.10 / 4 blind in my simulator, about 62 clean in the scorer's terms |
| Dragon Tamer Drake | Stark Mountain room 2 | optional | tag beside Buck | 3 | 62 to 63 | Dragon Dance Dragonite beside Kingdra's Draco Meteor and Altaria's Will-O-Wisp | not readable yet (a tag battle) |
| Dragon Tamer Kenny | Stark Mountain room 2 | optional | tag beside Buck | 3 | 62 to 63 | Salamence | not readable yet (a tag battle) |
| Ace Trainer Keenan | Stark Mountain room 2 | optional | tag with Kassandra | 4 | 62 to 63 | Primeape | not readable yet (a tag battle) |
| Ace Trainer Stefan | Stark Mountain room 2 | optional | tag with Jasmin | 4 | 62 to 63 | Tyranitar's Sand Stream | not readable yet (a tag battle) |
| Ace Trainer Skylar | Stark Mountain room 2 | optional | tag with Natasha | 4 | 62 to 63 | Exploud | not readable yet (a tag battle) |
| Ace Trainer Abel | Stark Mountain room 2 | optional | tag with Monique | 4 | 62 to 63 | Glalie | not readable yet (a tag battle) |
| Ace Trainer Kassandra | Stark Mountain room 2 | optional | tag with Keenan | 4 | 62 to 63 | Jumpluff's Sleep Powder and Memento | not readable yet (a tag battle) |
| Ace Trainer Jasmin | Stark Mountain room 2 | optional | tag with Stefan | 4 | 62 to 63 | Drapion | not readable yet (a tag battle) |
| Ace Trainer Natasha | Stark Mountain room 2 | optional | tag with Skylar | 4 | 62 to 63 | Wigglytuff's screens | not readable yet (a tag battle) |
| Ace Trainer Monique | Stark Mountain room 2 | optional | tag with Abel | 4 | 62 to 63 | Luxray | not readable yet (a tag battle) |
| Psychic Sterling | Stark Mountain room 2 | optional | tag beside Buck | 3 | 62 to 63 | Gallade's Sacred Sword behind Solrock's Will-O-Wisp and Chimecho's Yawn | not readable yet (a tag battle) |
| Psychic Chelsey | Stark Mountain room 2 | optional | tag beside Buck | 3 | 62 to 63 | Moonblast from Lunatone and Gardevoir | not readable yet (a tag battle) |
| Black Belt Ray | Stark Mountain room 2 | optional | tag beside Buck | 3 | 62 to 63 | Special fighters | not readable yet (a tag battle) |
| Black Belt Jarrett | Stark Mountain room 2 | optional | tag beside Buck | 3 | 62 to 63 | A Guts Machamp on a Flame Orb beside Blaziken's Brave Bird and Poliwrath's Liquidation and Hypnosis | not readable yet (a tag battle) |
| Veteran Harlan | Stark Mountain room 2 | optional | tag beside Buck | 3 | 62 to 63 | Raticate's Super Fang | not readable yet (a tag battle) |
| Commander Mars | Stark Mountain room 1 | optional | single, boss | 6 | 63 to 65 | Mars's last stand | about 95 / 1.2 / 13 in my simulator, where today's file reads 100 / 0.0 / 100 |
| Commander Jupiter | Stark Mountain room 1 | optional | single, boss | 6 | 63 to 65 | Jupiter's last stand | about 96 / 2.0 / 6 in my simulator, where today's file reads 100 / 0.0 / 99 |
| Dragon Tamer Keegan | Route 228 (sand) | optional | single | 4 | 60 to 63 | The Trapinch line on Eviolites | 99 / 1.68 / 8 blind in my simulator in sand, about 63 clean in the scorer's terms |
| Ace Trainer Jose | Route 228 (sand) | optional | single, Ace Trainer | 6 | 62 to 64 | Sand | about 86 / 3.4 / 0 with a planned six in sand |
| Ace Trainer Moira | Route 228 (sand) | optional | single, Ace Trainer | 6 | 62 to 64 | Ground and Rock in the sand | about 98 / 1.4 / 1 with a planned six in sand |
| Ace Trainer Meagan | Route 228 (sand) | optional | single, Ace Trainer | 6 | 62 to 64 | Mixed in the sand | about 100 / 1.2 / 16 with a planned six in sand |
| Psychic Corbin | Route 228 (sand) | optional | single | 4 | 60 to 63 | Stealth Rock from Bronzong | 92 / 1.92 / 12 blind in my simulator in sand, about 65 clean in the scorer's terms |
| Black Belt Davon | Route 228 (sand) | optional | single | 4 | 61 to 63 | Annihilape's Rage Fist | 98 / 1.60 / 16 blind in my simulator in sand, about 67 clean in the scorer's terms |
| Pkmn Ranger Kyler | Route 228 (sand) | optional | single | 4 | 61 to 63 | Sand Rush Sandslash in the sand | 97 / 1.74 / 11 blind in my simulator in sand, about 65 clean in the scorer's terms |
| Pkmn Ranger Krista | Route 228 (sand) | optional | single | 4 | 60 to 63 | Rock Head | 97 / 1.47 / 20 blind in my simulator in sand, about 68 clean in the scorer's terms |
| Ace Trainer Felix | Route 229 | optional | single, Ace Trainer | 6 | 62 to 64 | Ghosts and dragons | about 100 / 2.5 / 0 with a planned six |
| Ace Trainer Dana | Route 229 | optional | single, Ace Trainer | 6 | 62 to 64 | Psychic and Dark | about 100 / 1.5 / 0 with a planned six |
| Ace Trainer Sandra | Route 229 | optional | single, Ace Trainer | 6 | 62 to 64 | Today's Ninetales | about 100 / 0.8 / 38 with a planned six |
| Pkmn Ranger Deshawn | Route 229 | optional | single | 4 | 60 to 63 | Contrary and Protean | 95 / 1.25 / 30 blind in my simulator, about 72 clean in the scorer's terms |
| Swimmer Glenn | Route 230 | optional | single | 4 | 61 to 63 | Sniper Octillery on a Scope Lens | 97 / 1.40 / 32 blind in my simulator, about 73 clean in the scorer's terms |
| Swimmer Kurt | Route 230 | optional | single | 4 | 61 to 63 | Spikes from a Focus Sash Cloyster | 96 / 1.39 / 38 blind in my simulator, about 75 clean in the scorer's terms |
| Swimmer Sam | Route 230 | optional | single | 4 | 61 to 63 | Floatzel's Waterfall (Sam's reward HM) and Ice Spinner | 96 / 1.26 / 30 blind in my simulator, about 72 clean in the scorer's terms |
| Swimmer Joanna | Route 230 | optional | single | 4 | 60 to 63 | Rain from Luvdisc's Rain Dance on a Damp Rock | 98 / 1.37 / 28 blind in my simulator, about 71 clean in the scorer's terms |
| Swimmer Sophia | Route 230 | optional | single | 4 | 61 to 63 | Spikes from Delibird | 96 / 1.12 / 39 blind in my simulator, about 76 clean in the scorer's terms |
| Swimmer Mallory | Route 230 | optional | single | 4 | 61 to 63 | Masquerain's Quiver Dance and Sludge Bomb (Mallory's reward TM) | 93 / 1.15 / 44 blind in my simulator, about 77 clean in the scorer's terms |

Expected numbers are won / faints a fight / clean in my simulator, beside
today's file where it was read. For an ordinary trainer the clean rate is also
given in the scorer's terms, by the calibration in `read_split.py`.

## The trainers

### Galactic Grunt (Coronet 1F, 1): Mt. Coronet 1F tunnel room, on the path, single, cap 65

Rivals: a Toxic Boost Zangoose on a Toxic Orb beside Seviper's Glare, Crobat's Brave Bird and Chimecho's Yawn.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Chimecho | 61 | Leftovers | Levitate | default | Psyshock, Dazzling Gleam, Heal Bell, Yawn |
| Seviper | 61 | Black Sludge | Shed Skin | default | Gunk Shot, Sucker Punch, Glare, Earthquake |
| Crobat | 62 | Sharp Beak | Infiltrator | default | Brave Bird, Cross Poison, U-turn, Roost |
| Zangoose | 63 | Toxic Orb | Toxic Boost | default | Facade, Close Combat, Knock Off, Quick Attack |

Today's team: Zangoose 54 (Slash, Ice Punch, X-Scissor, Close Combat), Chimecho 54 (Heal Bell, Psychic, Energy Ball, Icy Wind). Expected: 98 / 0.99 / 35 blind in my simulator, about 74 clean in the scorer's terms.

### Galactic Grunt (Coronet 1F, 2): Mt. Coronet 1F tunnel room, on the path, single, cap 65

Punishers: Wobbuffet's Counter and Mirror Coat (Telepathy, not Shadow Tag, which the dial keeps off ordinary trainers), Dusknoir's Will-O-Wisp then Hex, Prankster Sableye and Spiritomb.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Wobbuffet | 60 | Sitrus Berry | Telepathy | default | Counter, Mirror Coat, Encore, Safeguard |
| Sableye | 61 | Lum Berry | Prankster | default | Foul Play, Knock Off, Recover, Taunt |
| Spiritomb | 60 | none | Infiltrator | default | Dark Pulse, Shadow Ball, Sucker Punch, Foul Play |
| Dusknoir | 63 | none | Levitate | default | Will-O-Wisp, Hex, Shadow Sneak, Pain Split |

Today's team: Wobbuffet 55 (Counter, Mirror Coat, Safeguard, Destiny Bond). Expected: 97 / 1.34 / 33 blind in my simulator, about 73 clean in the scorer's terms.

### Galactic Grunt (Coronet 1F, 3): Mt. Coronet 1F tunnel room, on the path, single, cap 65

Water Spout and Belly Drum: Wailord at full health, then Linoone's Belly Drum, Sitrus Berry and Extreme Speed, with Octillery and Floatzel's Ice Spinner.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Wailord | 62 | Sitrus Berry | Water Veil | default | Water Spout, Ice Beam, Yawn, Rest |
| Octillery | 61 | Scope Lens | Sniper | default | Hydro Pump, Ice Beam, Fire Blast, Energy Ball |
| Floatzel | 62 | Mystic Water | Water Veil | default | Liquidation, Ice Spinner, Crunch, Aqua Jet |
| Linoone | 63 | Sitrus Berry | Gluttony | default | Belly Drum, ExtremeSpeed, Seed Bomb, Shadow Claw |

Today's team: Wailord 54 (Water Spout, Amnesia, Dive, Bounce), Linoone 54 (Sitrus Berry; Shadow Claw, Slash, Seed Bomb, Belly Drum). Expected: 97 / 1.15 / 33 blind in my simulator, about 73 clean in the scorer's terms.

### Galactic Grunt (Coronet 3F, 1): Mt. Coronet 3F, gauntlet, before Somnu, single, cap 65

Burn, then Hex: Mismagius behind Drifblim. Two members, since four grunts in a row with no healing read far past the gauntlet band at three.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Drifblim | 56 | none | Unburden | default | Shadow Ball, Air Slash, Haze, Stockpile |
| Mismagius | 58 | Leftovers | Levitate | default | Will-O-Wisp, Hex, Dazzling Gleam, Mystical Fire |

Today's team: Mismagius 55 (Shadow Ball, Thunderbolt, Energy Ball, Will-O-Wisp). Expected: 100 / 0.15 / 85 blind in my simulator, about 94 clean in the scorer's terms.

### Galactic Grunt (Coronet 3F, 2): Mt. Coronet 3F, gauntlet, before Somnu, single, cap 65

Poison that follows you: Weezing's Toxic Spikes and Swalot's Toxic.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Swalot | 56 | none | Gluttony | default | Toxic, Sludge Bomb, Encore, Giga Drain |
| Weezing | 58 | Black Sludge | Levitate | default | Toxic Spikes, Sludge Bomb, Pain Split, Clear Smog |

Today's team: Swalot 55 (Gunk Shot, Seed Bomb, Fire Punch, Toxic). Expected: 100 / 0.16 / 84 blind in my simulator, about 93 clean in the scorer's terms.

### Galactic Grunt (Coronet 4F, 1): Mt. Coronet 4F, gauntlet, before Somnu, single, cap 65

Bugs: Yanmega's Bug Buzz and Pinsir's Lunge and Close Combat.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Pinsir | 56 | none | Moxie | default | Lunge, Close Combat, Stone Edge, Quick Attack |
| Yanmega | 58 | Leftovers | Tinted Lens | default | Bug Buzz, Air Slash, Giga Drain, U-turn |

Today's team: Pinsir 54 (Swords Dance, X-Scissor, Guillotine, Superpower), Heracross 54 (Stone Edge, Close Combat, Earthquake, Bulk Up). Expected: 100 / 0.23 / 78 blind in my simulator, about 91 clean in the scorer's terms.

### Galactic Grunt (Coronet 4F, 2): Mt. Coronet 4F, gauntlet, before Somnu, single, cap 65

Burns and Yawn: Camerupt's Lava Plume, then Drapion's Throat Chop and Knock Off.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Camerupt | 56 | none | Anger Point | default | Lava Plume, Earth Power, Yawn, Flash Cannon |
| Drapion | 58 | Black Sludge | Battle Armor | default | Throat Chop, Knock Off, Poison Jab, Earthquake |

Today's team: Drapion 54 (Toxic Spikes, X-Scissor, Poison Fang, Crunch), Camerupt 54 (Lava Plume, Rock Slide, Earth Power, Earthquake). Expected: 100 / 0.27 / 75 blind in my simulator, about 90 clean in the scorer's terms.

### Galactic Officer Moira: Mt. Coronet 5F, on the path, single, named officer, cap 65

Moira's hail, three levels under the cap with sharper sets: Abomasnow's Snow Warning, whose hail lasts the whole fight (its Icy Rock does nothing, since rocks extend only weather from a move), Blizzard that cannot miss on Abomasnow and Slowking, Mamoswine's Ice Shard, a Life Orb Gardevoir with Calm Mind, Celebi as the legendary, and a Swords Dance Absol ace with a Scope Lens.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Abomasnow | 60 | Icy Rock | Snow Warning | Modest | Blizzard, Wood Hammer, Earthquake, Ice Shard |
| Slowking | 61 | Leftovers | Regenerator | Modest | Surf, Psychic, Blizzard, Slack Off |
| Mamoswine | 61 | NeverMeltIce | Thick Fat | Adamant | Earthquake, Ice Fang, Ice Shard, Stone Edge |
| Gardevoir | 61 | Life Orb | Magic Guard | Modest | Psychic, Thunderbolt, Focus Blast, Calm Mind |
| Celebi | 61 | Leftovers | Natural Cure | Modest | Energy Ball, Psychic, Earth Power, Recover |
| Absol | 62 | Scope Lens | Super Luck | Adamant | Knock Off, Superpower, Stone Edge, Swords Dance |

Today's team: Abomasnow 54 (Occa Berry; Swagger, Earthquake, Avalanche, Endeavor), Slowking 54 (Leftovers; Calm Mind, Blizzard, Future Sight, Surf), Gardevoir 55 (Life Orb; Future Sight, Psychic, Calm Mind, Focus Blast), Mamoswine 53 (Lum Berry; Ice Shard, Earthquake, Superpower, Stone Edge), Celebi 50 (Sitrus Berry; Future Sight, AncientPower, Leaf Storm, Recover), Absol 57 (Focus Band; Pursuit, Perish Song, Future Sight, Detect). Expected: about 99 / 2.2 / 0 in my simulator, where today's file reads 100 / 0.4 / 71.

### Galactic Officer Somnu: Mt. Coronet 5F, gauntlet, closing 3F to 5F, single, named officer, cap 65

Somnu's sleep, as Ian asked, from three sources: Jumpluff's Sleep Powder behind a Focus Sash, Hypno's Hypnosis and Dream Eater, and Darkrai's Dark Void and Dream Eater (Dark Void waits on the Balance Agent adding it to Darkrai's egg moves), with Swalot's Destiny Bond as the trade, Stantler, and a Whiscash ace. She closes a gauntlet, so she sits a level lower than the officers outside it.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Jumpluff | 62 | Focus Sash | Chlorophyll | Jolly | Sleep Powder, U-turn, Leech Seed, Encore |
| Swalot | 62 | Sitrus Berry | Gluttony | Calm | Sludge Bomb, Destiny Bond, Encore, Toxic |
| Hypno | 62 | Leftovers | Insomnia | Calm | Hypnosis, Dream Eater, Psychic, Fire Punch |
| Stantler | 62 | Sitrus Berry | Intimidate | Adamant | Take Down, Zen Headbutt, Earthquake, Sucker Punch |
| Darkrai | 63 | Lum Berry | Bad Dreams | Timid | Dark Void, Dream Eater, Dark Pulse, Focus Blast |
| Whiscash | 64 | Wacan Berry | Swift Swim | Adamant | Waterfall, Earthquake, Stone Edge, Zen Headbutt |

Today's team: Swalot 55 (Starf Berry; Amnesia, Gunk Shot, Encore, Yawn), Hypno 55 (Leftovers; Flatter, Hypnosis, Dream Eater, Drain Punch), Jumpluff 52 (Yache Berry; Cotton Spore, U-turn, Sleep Powder, Leech Seed), Stantler 54 (Sitrus Berry; Hypnosis, Return, Megahorn, Dream Eater), Darkrai 50 (Wide Lens; Dark Void, Dream Eater, Dark Pulse, Focus Blast), Whiscash 56 (Wave Incense; Dragon Dance, Aqua Tail, Earthquake, Amnesia). Expected: about 84 / 2.5 / 0 in my simulator, where today's file reads 100 / 0.2 / 80.

### Galactic Officer Hesperid: Mt. Coronet 6F, on the path, single, named officer, cap 65

Today's six kept to one trade: Drifblim leads behind a Focus Sash (its Explosion and Destiny Bond are gone), Weezing keeps the Explosion, Girafarig passes Agility, a Life Orb Sceptile, Rampardos's Head Smash and Rock Polish, and a Camerupt ace with Eruption and Stealth Rock.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Drifblim | 63 | Focus Sash | Unburden | Timid | Shadow Ball, Thunderbolt, Will-O-Wisp, Stockpile |
| Weezing | 63 | Black Sludge | Levitate | Bold | Sludge Bomb, Will-O-Wisp, Thunderbolt, Explosion |
| Girafarig | 63 | Starf Berry | Quick Feet | Timid | Agility, Baton Pass, Psychic, Thunderbolt |
| Sceptile | 64 | Life Orb | Overgrow | Naive | Leaf Storm, Focus Blast, Earthquake, Rock Slide |
| Rampardos | 64 | Lum Berry | Rock Head | Adamant | Head Smash, Zen Headbutt, Earthquake, Rock Polish |
| Camerupt | 65 | Passho Berry | Solid Rock | Modest | Eruption, Earth Power, Flamethrower, Stealth Rock |

Today's team: Weezing 55 (Poison Barb; Payback, Sludge Bomb, Explosion, Will-O-Wisp), Sceptile 54 (Petaya Berry; Rock Slide, Pursuit, Aerial Ace, Leaf Storm), Girafarig 52 (Starf Berry; Agility, Baton Pass, Earthquake, Thunder), Rampardos 53 (Lum Berry; Head Smash, Pursuit, Rock Polish, Zen Headbutt), Drifblim 54 (Focus Sash; Explosion, Ominous Wind, Curse, Destiny Bond), Camerupt 56 (Passho Berry; Overheat, Earthquake, Explosion, Will-O-Wisp). Expected: about 95 / 1.7 / 9 in my simulator, where today's file reads 100 / 0.2 / 82.

### Galactic Officer Argo: Mt. Coronet 6F, on the path, single, named officer, cap 65

Today's puzzle box, three levels under the cap: Protean Kecleon lays Stealth Rock, a Gengar takes Vespiquen's place, the Wonder Guard Shedinja that only super-effective hits touch, Dugtrio's Arena Trap behind a Focus Sash (the trade), Rotom with a Spooky Plate, and a Life Orb Relicanth ace with Rock Polish.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Kecleon | 61 | Lum Berry | Protean | Adamant | Stealth Rock, Shadow Claw, Drain Punch, Knock Off |
| Gengar | 61 | Wise Glasses | Levitate | Timid | Shadow Ball, Sludge Bomb, Focus Blast, Thunderbolt |
| Shedinja | 61 | SilverPowder | Wonder Guard | Adamant | X-Scissor, Shadow Sneak, Will-O-Wisp, Sucker Punch |
| Dugtrio | 61 | Focus Sash | Arena Trap | Jolly | Earthquake, Stone Edge, Sucker Punch, Aerial Ace |
| Rotom | 61 | Spooky Plate | Levitate | Timid | Thunderbolt, Shadow Ball, Will-O-Wisp, Volt Switch |
| Relicanth | 62 | Life Orb | Rock Head | Adamant | Double-Edge, Waterfall, Earthquake, Rock Polish |

Today's team: Kecleon 55 (Flame Orb; Dizzy Punch, Rock Tomb, Trick, Fling), Vespiquen 54 (SilverPowder; Attack Order, Defend Order, Heal Order), Dugtrio 57 (Focus Sash; Earthquake, Magnitude, Pursuit, Rock Slide), Shedinja 55 (Focus Sash; Sucker Punch, X-Scissor, Swagger, Shadow Sneak), Relicanth 54 (Rock Incense; Head Smash, Double-Edge, Rock Polish, Aqua Tail), Rotom 53 (Wise Glasses; Will-O-Wisp, Discharge, Overheat, Ominous Wind). Expected: about 83 / 3.4 / 3 in my simulator, where today's file reads 100 / 0.3 / 75.

### Galactic Grunt Tyche: Spear Pillar, on the path, single, cap 65

Ian's named grunt kept to her idea: Tentacruel's Toxic Spikes, Crobat, Toxicroak, and a Focus Sash Gengar, which loses Explosion because the dial allows no trade on an ordinary trainer.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Tentacruel | 63 | Leftovers | Clear Body | default | Toxic Spikes, Scald, Sludge Bomb, Rapid Spin |
| Crobat | 61 | Black Sludge | Infiltrator | default | Brave Bird, Cross Poison, U-turn, Roost |
| Toxicroak | 60 | none | Dry Skin | default | Drain Punch, Gunk Shot, Sucker Punch, Knock Off |
| Gengar | 62 | Focus Sash | Levitate | default | Shadow Ball, Sludge Bomb, Focus Blast, Will-O-Wisp |

Today's team: Crobat 55 (Life Orb; Protect, Leech Life, Poison Fang, Brave Bird), Tentacruel 55 (Leftovers; Protect, Blizzard, Toxic Spikes, Muddy Water), Gengar 56 (Focus Sash; Shadow Ball, Focus Blast, Psychic, Explosion). Expected: 94 / 1.70 / 21 blind in my simulator, about 68 clean in the scorer's terms.

### Galactic Grunt Hermes: Spear Pillar, on the path, single, cap 65

Ian's named grunt kept to his idea: a Focus Sash Electrode with Light Screen and Volt Switch, Shiftry's Swords Dance on a Tanga Berry, and Dodrio's Endure, Salac Berry and Flail. Every Explosion is gone, as on Tyche.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Electrode | 63 | Focus Sash | Static | default | Thunder Wave, Volt Switch, Thunderbolt, Light Screen |
| Ambipom | 62 | Silk Scarf | Technician | default | Fake Out, Double Hit, U-turn, Knock Off |
| Shiftry | 63 | Tanga Berry | Pickpocket | default | Swords Dance, Leaf Blade, Sucker Punch, Knock Off |
| Dodrio | 63 | Salac Berry | Quick Feet | default | Endure, Flail, Brave Bird, Drill Run |

Today's team: Electrode 55 (Focus Sash; Explosion, Thunder Wave, Thunder, Light Screen), Shiftry 55 (Tanga Berry; Explosion, Swords Dance, Rock Slide, Leaf Storm), Dodrio 56 (Salac Berry; Brave Bird, Double-Edge, Endure, Flail). Expected: 98 / 1.23 / 22 blind in my simulator, about 69 clean in the scorer's terms.

### Commander Mars: Spear Pillar, on the path, tag with Jupiter, beside Barry, cap 65

Mars 2's core at Spear Pillar: Bronzong leads with Stealth Rock and Hypnosis, then Crobat, Umbreon's Toxic, a Luxray with an Expert Belt and Purugly's Fake Out at the top.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Bronzong | 62 | Leftovers | Levitate | Relaxed | Stealth Rock, Gyro Ball, Earthquake, Hypnosis |
| Crobat | 62 | Sharp Beak | Inner Focus | Jolly | Brave Bird, Cross Poison, U-turn, Roost |
| Umbreon | 62 | Leftovers | Synchronize | Calm | Payback, Toxic, Wish, Protect |
| Luxray | 62 | Expert Belt | Tinted Lens | Adamant | Thunder Fang, Crunch, Superpower, Ice Fang |
| Purugly | 63 | Silk Scarf | Defiant | Jolly | Fake Out, Body Slam, Sucker Punch, Knock Off |

Today's team: Solrock 58 (King’s Rock; Zen Headbutt, Rock Slide, Light Screen, Will-O-Wisp), Delcatty 58 (Silk Scarf; Fake Out, Copycat, Last Resort), Luxray 58 (Magnet; Thunder Fang, Ice Fang, Charge, Magnet Rise), Bronzong 58 (Sitrus Berry; Curse, Gyro Ball, Zen Headbutt, Recycle), Purugly 59 (Life Orb; Slash, Fake Out, Sucker Punch, Hypnosis). Expected: not readable yet (a tag battle).

### Commander Jupiter: Spear Pillar, on the path, tag with Mars, beside Barry, cap 65

Jupiter's poison at Spear Pillar: Drapion leads with Toxic Spikes behind a Focus Sash, then Lunatone's Calm Mind, Tangrowth's Sleep Powder, Spiritomb's Will-O-Wisp and a Skuntank ace.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Drapion | 62 | Focus Sash | Hyper Cutter | Jolly | Toxic Spikes, Cross Poison, Crunch, Earthquake |
| Lunatone | 62 | Leftovers | Levitate | Modest | Psychic, Earth Power, Ice Beam, Calm Mind |
| Tangrowth | 62 | Leftovers | Regenerator | Relaxed | Seed Bomb, Earthquake, Knock Off, Sleep Powder |
| Spiritomb | 62 | Leftovers | Pressure | Careful | Shadow Ball, Sucker Punch, Will-O-Wisp, Pain Split |
| Skuntank | 63 | Dread Plate | Aftermath | Adamant | Crunch, Poison Jab, Sucker Punch, Fire Blast |

Today's team: Lunatone 58 (Quick Claw; Psychic, AncientPower, Earth Power, Stealth Rock), Drapion 58 (Shuca Berry; Cross Poison, Toxic, Ice Fang, Earthquake), Tangrowth 58 (Toxic Orb; Facade, Power Whip, Protect, Fling), Spiritomb 58 (Leftovers; Torment, Shadow Sneak, Pursuit, Spite), Skuntank 59 (Choice Specs; Dark Pulse, Sludge Bomb, Flamethrower, Hyper Beam). Expected: not readable yet (a tag battle).

### Cyrus 3: Distortion World, on the path, single, boss, cap 65

Today's file moved up to the cap's levels, as Ian chose: Dusknoir's Will-O-Wisp, Gyarados, a Focus Sash Heatran with Magma Storm, a Life Orb Flygon with Draco Meteor, Regirock's Curse and Explosion (the trade), and Salamence at the cap with a King's Rock. Heatran and Regirock are the two legendaries Ian allowed him. Magma Storm and Draco Meteor are not in their lists at 63, which Ian's late-game ruling allows.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Dusknoir | 63 | Lum Berry | Levitate | Lonely | Shadow Punch, Payback, Earthquake, Will-O-Wisp |
| Gyarados | 63 | Wacan Berry | Intimidate | Lonely | Aqua Tail, Avalanche, Stone Edge, Earthquake |
| Heatran | 63 | Focus Sash | Flash Fire | Hasty | Magma Storm, Earth Power, Flash Cannon, AncientPower |
| Flygon | 63 | Life Orb | Levitate | Lonely | Earth Power, Draco Meteor, U-turn, Stone Edge |
| Regirock | 64 | Leftovers | Solid Rock | Brave | Curse, Explosion, Stone Edge, Fire Punch |
| Salamence | 65 | King’s Rock | Intimidate | Lonely | Rock Slide, Dragon Rush, Swagger, Fire Fang |

Today's team: Dusknoir 59 (Lum Berry; Shadow Punch, Payback, Earthquake, Will-O-Wisp), Gyarados 59 (Wacan Berry; Aqua Tail, Avalanche, Stone Edge, Earthquake), Heatran 59 (Focus Sash; Magma Storm, Earth Power, Flash Cannon, AncientPower), Flygon 59 (Life Orb; Earth Power, Draco Meteor, U-turn, Stone Edge), Regirock 59 (Leftovers; Curse, Explosion, Stone Edge, Fire Punch), Salamence 59 (King’s Rock; Rock Slide, Dragon Rush, Swagger, Fire Fang). Expected: about 72 / 3.1 / 6 in my simulator, where today's file reads 97 / 1.3 / 31.

### Bird Keeper Audrey: Route 225, optional, single, cap 65

Flying speed: a Guts Swellow on a Flame Orb, Talonflame, Farfetch'd's Stick, and Pidgeot's Hurricane on a Wide Lens.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Pidgeot | 62 | Wide Lens | Big Pecks | default | Hurricane, Heat Wave, Roost, U-turn |
| Farfetchd | 61 | Stick | Defiant | default | Leaf Blade, Brave Bird, Knock Off, Night Slash |
| Talonflame | 62 | none | Flame Body | default | Brave Bird, Flare Blitz, Roost, U-turn |
| Swellow | 64 | Flame Orb | Guts | default | Facade, Brave Bird, U-turn, Quick Attack |

Today's team: Swellow 55 (Brave Bird, Quick Attack, U-turn, Whirlwind), Farfetchd 55 (Night Slash, Leaf Blade, Quick Attack, Aerial Ace), Pidgeot 55 (Roost, Tailwind, Heat Wave, Air Slash). Expected: 99 / 0.97 / 41 blind in my simulator, about 76 clean in the scorer's terms.

### Dragon Tamer Geoffrey: Route 225, optional, single, cap 65

Eviolite dragons: Gabite and Dragonair hold Eviolites before a Levitate Flygon, with Altaria's Moonblast and Will-O-Wisp. Today's Garchomp is too strong for an ordinary trainer, so Gabite stands in.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Altaria | 63 | Leftovers | Cloud Nine | default | Moonblast, Dragon Pulse, Roost, Will-O-Wisp |
| Dragonair | 61 | Eviolite | Marvel Scale | default | Dragon Rush, ExtremeSpeed, Thunder Wave, Dragon Tail |
| Gabite | 60 | Eviolite | Rough Skin | default | Dragon Claw, Earthquake, Stone Edge, Fire Fang |
| Flygon | 61 | none | Levitate | default | Earthquake, Outrage, U-turn, Fire Punch |

Today's team: Garchomp 56 (Dragon Claw, Dig, Crunch, Dragon Rush), Altaria 56 (Fire Blast, Dragon Pulse, Hidden Power, Mirror Move). Expected: 94 / 1.74 / 18 blind in my simulator, about 67 clean in the scorer's terms.

### Ace Trainer Rodolfo: Route 225, optional, single, Ace Trainer, cap 65

A balanced core: Starmie, Venusaur's Sleep Powder, Arcanine, Gengar, Snorlax and a Flygon ace.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Starmie | 62 | Mystic Water | Magic Guard | Timid | Surf, Psychic, Ice Beam, Recover |
| Venusaur | 62 | Black Sludge | Overgrow | Modest | Sludge Bomb, Energy Ball, Earthquake, Sleep Powder |
| Arcanine | 62 | Charcoal | Intimidate | Adamant | Flare Blitz, ExtremeSpeed, Crunch, Thunder Fang |
| Gengar | 63 | Wise Glasses | Levitate | Timid | Shadow Ball, Sludge Bomb, Focus Blast, Thunderbolt |
| Snorlax | 62 | Leftovers | Thick Fat | Careful | Body Slam, Earthquake, Crunch, Fire Punch |
| Flygon | 64 | Yache Berry | Levitate | Jolly | Earthquake, Outrage, Fire Punch, U-turn |

Today's team: Starmie 55 (Surf, Recover, Psychic, Signal Beam), Flygon 55 (Outrage, Earthquake, Fire Punch, Roost), Venusaur 55 (Frenzy Plant, Sludge Bomb, Sleep Powder, Leech Seed). Expected: about 99 / 2.0 / 2 with a planned six; read blind, 38 / 5.2 / 0.

### Ace Trainer Quinn: Route 225, optional, single, Ace Trainer, cap 65

Bugs behind support: Skarmory's Spikes and Whirlwind, Lanturn, Meganium's screens, Heracross, Scizor and a Swords Dance Pinsir ace.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Skarmory | 62 | Focus Sash | Filter | Impish | Spikes, Brave Bird, Roost, Whirlwind |
| Lanturn | 62 | Leftovers | Volt Absorb | Modest | Surf, Discharge, Ice Beam, Confuse Ray |
| Meganium | 62 | Sitrus Berry | Thick Fat | Bold | Energy Ball, Earthquake, Light Screen, Reflect |
| Heracross | 63 | Lum Berry | Guts | Jolly | Close Combat, Megahorn, Stone Edge, Earthquake |
| Scizor | 62 | Metal Coat | Technician | Adamant | Bullet Punch, X-Scissor, U-turn, Swords Dance |
| Pinsir | 64 | SilverPowder | Mold Breaker | Jolly | X-Scissor, Close Combat, Stone Edge, Swords Dance |

Today's team: Pinsir 55 (Superpower, X-Scissor, Swords Dance, Rock Tomb), Lanturn 55 (Discharge, Signal Beam, Surf, Confuse Ray), Meganium 55 (Petal Dance, Light Screen, PoisonPowder, AncientPower). Expected: about 99 / 0.6 / 60 with a planned six; read blind, 29 / 4.9 / 3.

### Ace Trainer Deanna: Route 225, optional, single, Ace Trainer, cap 65

Special attackers: Ampharos's Light Screen, Tropius, Jolteon's Thunder Wave, Gyarados, Togekiss and a Lapras ace.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Ampharos | 62 | Magnet | Static | Modest | Thunderbolt, Power Gem, Signal Beam, Light Screen |
| Tropius | 62 | Leftovers | Overgrow | Modest | Air Slash, Energy Ball, Roost, Earthquake |
| Jolteon | 62 | Lum Berry | Volt Absorb | Timid | Thunderbolt, Shadow Ball, Signal Beam, Thunder Wave |
| Gyarados | 63 | Wacan Berry | Intimidate | Adamant | Waterfall, Earthquake, Ice Fang, Stone Edge |
| Togekiss | 62 | Sitrus Berry | Serene Grace | Modest | Air Slash, Aura Sphere, Flamethrower, Roost |
| Lapras | 64 | Leftovers | Shell Armor | Modest | Surf, Ice Beam, Thunderbolt, Psychic |

Today's team: Ampharos 55 (Thunderbolt, Power Gem, Signal Beam, Light Screen), Tropius 55 (SolarBeam, Air Slash, Synthesis, Sunny Day), Lapras 55 (Surf, Ice Beam, Thunderbolt). Expected: about 100 / 0.2 / 80 with a planned six; read blind, 42 / 4.6 / 1.

### Psychic Daisy: Route 225, optional, single, cap 65

Regenerator: Slowbro's Scald and Psyshock, Slowking's Nasty Plot, Gardevoir on a Pixie Plate, and Hypno's Hypnosis.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Slowbro | 62 | Leftovers | Regenerator | default | Scald, Psyshock, Slack Off, Thunder Wave |
| Hypno | 61 | Sitrus Berry | Insomnia | default | Psychic, Hypnosis, Focus Blast, Dazzling Gleam |
| Gardevoir | 62 | Pixie Plate | Trace | default | Moonblast, Psyshock, Mystical Fire, Shadow Ball |
| Slowking | 63 | none | Regenerator | default | Scald, Psychic, Flamethrower, Nasty Plot |

Today's team: Slowking 56 (Power Gem, Psychic, Surf, Shadow Ball), Slowbro 56 (Surf, Psychic, Ice Beam, Flamethrower). Expected: 97 / 1.32 / 30 blind in my simulator, about 72 clean in the scorer's terms.

### Pkmn Ranger Dwayne: Route 225, optional, single, cap 65

Stealth Rock from a Rocky Helmet Skarmory, then a vested Tangrowth, Golduck's Scald and Donphan's Earthquake.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Skarmory | 63 | Rocky Helmet | Filter | default | Stealth Rock, Brave Bird, Iron Head, Roost |
| Golduck | 61 | Mystic Water | Cloud Nine | default | Scald, Ice Beam, Psyshock, Encore |
| Tangrowth | 60 | Assault Vest | Regenerator | default | Giga Drain, Sludge Bomb, Knock Off, Earthquake |
| Donphan | 60 | none | Battle Armor | default | Earthquake, Ice Shard, Knock Off, Gunk Shot |

Today's team: Skarmory 55 (Steel Wing, Brave Bird, Stealth Rock, Night Slash), Golduck 55 (Aqua Jet, Zen Headbutt, Amnesia, Waterfall), Donphan 55 (Thunder Fang, Ice Shard, Earthquake, Giga Impact). Expected: 93 / 1.66 / 22 blind in my simulator, about 69 clean in the scorer's terms.

### Pkmn Ranger Ashlee: Route 225, optional, single, cap 65

Glare, then the hitters: Arbok's paralysis, Mightyena and Granbull's Intimidate, and a Magic Guard Leafeon.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Arbok | 62 | Black Sludge | Intimidate | default | Glare, Gunk Shot, Sucker Punch, Earthquake |
| Mightyena | 61 | BlackGlasses | Intimidate | default | Crunch, Play Rough, Sucker Punch, Ice Fang |
| Granbull | 62 | none | Intimidate | default | Play Rough, Close Combat, Earthquake, Thunder Wave |
| Leafeon | 63 | Miracle Seed | Magic Guard | default | Leaf Blade, Knock Off, X-Scissor, Synthesis |

Today's team: Linoone 55 (Slash, Rest, Belly Drum, Fling), Arbok 55 (Glare, Ice Fang, Fire Fang, Gunk Shot), Skarmory 55 (Steel Wing, Brave Bird, Roost, Night Slash). Expected: 97 / 0.97 / 40 blind in my simulator, about 76 clean in the scorer's terms.

### Bird Keeper Geneva: Route 226, optional, single, cap 65

Magic Bounce Xatu with Grass Knot (Geneva's reward TM), Fearow's Drill Run, Noctowl's Hurricane and Hypnosis, Crobat.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Xatu | 63 | none | Magic Bounce | default | Psychic, Grass Knot, Heat Wave, U-turn |
| Noctowl | 61 | Wide Lens | Tinted Lens | default | Hurricane, Moonblast, Hypnosis, Roost |
| Crobat | 62 | Black Sludge | Infiltrator | default | Brave Bird, Cross Poison, U-turn, Roost |
| Fearow | 60 | none | Sniper | default | Drill Run, Drill Peck, U-turn, Quick Attack |

Today's team: Fearow 56 (Agility, Assurance, Roost, Drill Peck), Xatu 56 (Ominous Wind, Signal Beam, Heat Wave, Psychic). Expected: 94 / 1.34 / 32 blind in my simulator, about 73 clean in the scorer's terms.

### Dragon Tamer Stanley: Route 226, optional, single, cap 65

Kingdra's Draco Meteor behind Eviolite Seadra and Dragonair and an Intimidate Gyarados.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Seadra | 61 | Eviolite | Sniper | default | Hydro Pump, Dragon Pulse, Ice Beam, Focus Energy |
| Dragonair | 63 | Eviolite | Shed Skin | default | Dragon Rush, Aqua Tail, ExtremeSpeed, Thunder Wave |
| Gyarados | 61 | none | Intimidate | default | Waterfall, Earthquake, Ice Fang, Crunch |
| Kingdra | 62 | none | Sniper | default | Draco Meteor, Scald, Ice Beam, Flip Turn |

Today's team: Kingdra 58 (Brine, Hydro Pump, Ice Beam, Dragon Pulse). Expected: 96 / 1.35 / 29 blind in my simulator, about 72 clean in the scorer's terms.

### Ace Trainer Graham: Route 226, optional, single, Ace Trainer, cap 65

Fighting types: the Hitmon trio led by Hitmontop's Fake Out behind a Focus Sash, Breloom's Spore, a Life Orb Lucario and a Flame Orb Machamp ace.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Hitmontop | 62 | Focus Sash | Technician | Adamant | Fake Out, Close Combat, Sucker Punch, Stone Edge |
| Hitmonchan | 62 | Black Belt | Iron Fist | Adamant | Drain Punch, Ice Punch, ThunderPunch, Mach Punch |
| Hitmonlee | 62 | Lum Berry | Reckless | Adamant | Hi Jump Kick, Stone Edge, Knock Off, Earthquake |
| Breloom | 62 | Toxic Orb | Poison Heal | Jolly | Seed Bomb, Mach Punch, Stone Edge, Spore |
| Lucario | 63 | Life Orb | Adaptability | Timid | Aura Sphere, Flash Cannon, Dark Pulse, Vacuum Wave |
| Machamp | 64 | Flame Orb | Guts | Adamant | Close Combat, Stone Edge, Ice Punch, Bullet Punch |

Today's team: Hitmonlee 56 (Endure, Reversal, Close Combat, Blaze Kick), Hitmonchan 56 (Mega Punch, Ice Punch, Counter, Close Combat), Hitmontop 56 (Bullet Punch, Detect, Close Combat, Endeavor). Expected: about 100 / 1.5 / 12 with a planned six; read blind, 46 / 4.6 / 0.

### Swimmer Wade: Route 226, optional, single, cap 65

Speed Boost Sharpedo's Liquidation, Whiscash's Earthquake, an Unaware Quagsire and Lanturn's Volt Switch.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Quagsire | 61 | Leftovers | Unaware | default | Scald, Earthquake, Recover, Toxic |
| Lanturn | 63 | Sitrus Berry | Volt Absorb | default | Scald, Volt Switch, Ice Beam, Thunder Wave |
| Sharpedo | 62 | none | Speed Boost | default | Liquidation, Crunch, Ice Fang, Protect |
| Whiscash | 62 | none | Anticipation | default | Earthquake, Liquidation, Stone Edge, Zen Headbutt |

Today's team: Sharpedo 56 (Ice Fang, Agility, Skull Bash, Night Slash), Whiscash 56 (Aqua Tail, Earthquake, Future Sight, Fissure). Expected: 94 / 1.37 / 35 blind in my simulator, about 74 clean in the scorer's terms.

### Swimmer Lydia: Route 226, optional, single, cap 65

Water Spout from a full-health Wailord, then Blastoise's Scald and the ice of Lapras and Dewgong. A Shell Smash Blastoise read 63 won, far past the band.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Lapras | 60 | none | Hydration | default | Ice Beam, Surf, Thunderbolt, Ice Shard |
| Dewgong | 60 | Leftovers | Thick Fat | default | Ice Beam, Surf, Flip Turn, Encore |
| Blastoise | 61 | none | Shell Armor | default | Scald, Ice Beam, Dark Pulse, Rapid Spin |
| Wailord | 63 | Sitrus Berry | Water Veil | default | Water Spout, Ice Beam, Hydro Pump, Rest |

Today's team: Blastoise 55 (Flash Cannon, Ice Beam, Rain Dance, Hydro Pump), Walrein 55 (Rest, Surf, Blizzard, Sheer Cold), Wailord 55 (Amnesia, Ice Beam, Rest, Hydro Pump). Expected: 100 / 1.09 / 35 blind in my simulator, about 74 clean in the scorer's terms.

### Ace Trainer Saul: Route 227, optional, single, Ace Trainer, cap 65

Normal types: Tauros, Miltank, a Flame Orb Ursaring, an Eviolite Porygon2, Staraptor and a Snorlax ace.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Tauros | 62 | Lum Berry | Intimidate | Jolly | Take Down, Earthquake, Stone Edge, Zen Headbutt |
| Miltank | 62 | Leftovers | Thick Fat | Impish | Body Slam, Earthquake, Milk Drink, Ice Punch |
| Ursaring | 62 | Flame Orb | Guts | Adamant | Facade, Close Combat, Crunch, Earthquake |
| Porygon2 | 62 | Eviolite | Download | Calm | Tri Attack, Ice Beam, Thunderbolt, Recover |
| Staraptor | 63 | Sharp Beak | Intimidate | Jolly | Brave Bird, Close Combat, U-turn, Roost |
| Snorlax | 64 | Leftovers | Thick Fat | Careful | Body Slam, Earthquake, Crunch, Fire Punch |

Today's team: Tauros 60 (Thrash, Zen Headbutt, Swagger, Payback). Expected: about 84 / 3.3 / 0 with a planned six; read blind, 26 / 5.3 / 0.

### Ace Trainer Mikayla: Route 227, optional, single, Ace Trainer, cap 65

Dark types: Persian's Fake Out, Seviper's Glare, Honchkrow, Mightyena, Weavile and a Swords Dance Absol ace with a Scope Lens.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Persian | 62 | Silk Scarf | Technician | Jolly | Fake Out, U-turn, Knock Off, Aerial Ace |
| Seviper | 62 | Poison Barb | Shed Skin | Naive | Sludge Bomb, Crunch, Flamethrower, Glare |
| Honchkrow | 62 | Sharp Beak | Moxie | Adamant | Drill Peck, Night Slash, Sucker Punch, Heat Wave |
| Mightyena | 62 | Sitrus Berry | Intimidate | Adamant | Crunch, Sucker Punch, Ice Fang, Thunder Fang |
| Weavile | 63 | NeverMeltIce | Technician | Jolly | Night Slash, Ice Punch, Ice Shard, Brick Break |
| Absol | 64 | Scope Lens | Super Luck | Adamant | Knock Off, Superpower, Stone Edge, Swords Dance |

Today's team: Seviper 58 (Night Slash, Poison Fang, Wring Out, Glare), Persian 58 (Night Slash, Slash, Faint Attack, Fake Out), Absol 58 (Night Slash, Psycho Cut, Slash, Quick Attack). Expected: about 98 / 1.1 / 13 with a planned six; read blind, 14 / 5.5 / 0.

### Black Belt Griffin: Route 227, optional, single, cap 65

A Guts Machamp on a Flame Orb behind Hitmontop's Fake Out and Triple Axel, Breloom's Mach Punch and a Pure Power Medicham. Today's Spore Breloom loses Spore, which the dial keeps to bosses and Ace Trainers.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Hitmontop | 61 | none | Steadfast | default | Fake Out, Triple Axel, Close Combat, Sucker Punch |
| Breloom | 62 | Coba Berry | Technician | default | Mach Punch, Seed Bomb, Rock Tomb, Stun Spore |
| Medicham | 60 | none | Pure Power | default | Hi Jump Kick, Zen Headbutt, Bullet Punch, Ice Punch |
| Machamp | 63 | Flame Orb | Guts | default | Facade, Close Combat, Knock Off, Bullet Punch |

Today's team: Breloom 58 (Spore, Mach Punch, Seed Bomb, ThunderPunch), Medicham 58 (Detect, Psycho Cut, Hi Jump Kick, Ice Punch). Expected: 97 / 1.23 / 31 blind in my simulator, about 72 clean in the scorer's terms.

### Pkmn Ranger Felicia: Route 227, optional, single, cap 65

Jumpluff's Sleep Powder and itemless Acrobatics, Roserade, Sceptile's Leaf Storm and Lopunny's Fake Out.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Jumpluff | 61 | none | Infiltrator | default | Sleep Powder, Acrobatics, U-turn, Leech Seed |
| Roserade | 62 | Black Sludge | Natural Cure | default | Sludge Bomb, Giga Drain, Shadow Ball, Dazzling Gleam |
| Sceptile | 62 | Miracle Seed | Unburden | default | Leaf Storm, Dragon Pulse, Focus Blast, Giga Drain |
| Lopunny | 63 | Silk Scarf | Scrappy | default | Hi Jump Kick, Return, Ice Punch, Fake Out |

Today's team: Jumpluff 58 (Sleep Powder, U-turn, Bounce, Seed Bomb), Lopunny 58 (Dizzy Punch, Jump Kick, Bounce, Quick Attack). Expected: 98 / 1.07 / 34 blind in my simulator, about 74 clean in the scorer's terms.

### Bird Keeper Krystal: Stark Mountain room 2, optional, tag beside Buck, cap 65

Noctowl's Hypnosis then Dream Eater (the split's one conditional attack on an ordinary trainer), Fearow's Drill Run and Staraptor.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Noctowl | 62 | Leftovers | Insomnia | default | Hypnosis, Dream Eater, Air Slash, Roost |
| Fearow | 62 | Sharp Beak | Sniper | default | Drill Run, Drill Peck, U-turn, Double-Edge |
| Staraptor | 63 | Lum Berry | Reckless | default | Brave Bird, Close Combat, U-turn, Quick Attack |

Today's team: Staraptor 60 (U-turn, Close Combat, Quick Attack, Brave Bird), Fearow 60 (Agility, U-turn, Roost, Drill Peck), Noctowl 60 (Extrasensory, Hypnosis, Roost, Dream Eater). Expected: not readable yet (a tag battle).

### Dragon Tamer Darien: Stark Mountain, optional, single, cap 65

Dragonite with Extreme Speed and Outrage behind an Eviolite Dragonair, Flygon and Altaria. Dragon Dance with Multiscale read 75 to 95 won, so Dragonite takes neither.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Altaria | 63 | Leftovers | Cloud Nine | default | Moonblast, Dragon Pulse, Roost, Will-O-Wisp |
| Dragonair | 62 | Eviolite | Shed Skin | default | Dragon Rush, ExtremeSpeed, Thunder Wave, Aqua Tail |
| Flygon | 61 | Soft Sand | Levitate | default | Earthquake, Outrage, U-turn, Fire Punch |
| Dragonite | 60 | none | Inner Focus | default | ExtremeSpeed, Outrage, Earthquake, Fire Punch |

Today's team: Dragonite 60 (Dragon Rush, Fire Punch, Dragon Dance, Wing Attack). Expected: 95 / 2.10 / 4 blind in my simulator, about 62 clean in the scorer's terms.

### Dragon Tamer Drake: Stark Mountain room 2, optional, tag beside Buck, cap 65

Dragon Dance Dragonite beside Kingdra's Draco Meteor and Altaria's Will-O-Wisp.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Altaria | 62 | Leftovers | Cloud Nine | default | Moonblast, Dragon Pulse, Roost, Will-O-Wisp |
| Kingdra | 62 | Mystic Water | Sniper | default | Draco Meteor, Surf, Ice Beam, Flip Turn |
| Dragonite | 63 | Lum Berry | Inner Focus | default | Dragon Dance, ExtremeSpeed, Outrage, Earthquake |

Today's team: Dragonite 60 (Dragon Dance, Roost, Outrage, ExtremeSpeed), Kingdra 60 (Ice Beam, Hydro Pump, Dragon Dance, Dragon Pulse), Altaria 60 (Flamethrower, Dragon Pulse, Roost, Hidden Power). Expected: not readable yet (a tag battle).

### Dragon Tamer Kenny: Stark Mountain room 2, optional, tag beside Buck, cap 65

Salamence, Flygon and Charizard's Hurricane.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Flygon | 62 | Soft Sand | Levitate | default | Earthquake, Dragon Claw, U-turn, Fire Punch |
| Charizard | 62 | Charcoal | Blaze | default | Flamethrower, Hurricane, Dragon Pulse, Roost |
| Salamence | 63 | Sitrus Berry | Intimidate | default | Outrage, Earthquake, Fire Blast, Roost |

Today's team: Salamence 60 (Earthquake, Crunch, Outrage, Flamethrower), Flygon 60 (ThunderPunch, Outrage, U-turn, Earthquake), Charizard 60 (Flare Blitz, Outrage, ThunderPunch, Roost). Expected: not readable yet (a tag battle).

### Ace Trainer Keenan: Stark Mountain room 2, optional, tag with Kassandra, cap 65

Primeape, Electivire, Banette and Magmortar.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Primeape | 62 | Lum Berry | Defiant | Jolly | Close Combat, U-turn, Ice Punch, Stone Edge |
| Electivire | 62 | Expert Belt | Adaptability | Adamant | ThunderPunch, Ice Punch, Cross Chop, Earthquake |
| Banette | 62 | Spell Tag | Cursed Body | Adamant | Shadow Claw, Sucker Punch, Knock Off, Will-O-Wisp |
| Magmortar | 63 | Charcoal | Flame Body | Modest | Flamethrower, Thunderbolt, Focus Blast, Psychic |

Today's team: Primeape 60 (Cross Chop, Ice Punch, U-turn, Close Combat), Electivire 60 (Thunderbolt, Flamethrower, Psychic, Thunder Wave), Banette 60 (Shadow Ball, Psychic, Thunderbolt, Will-O-Wisp). Expected: not readable yet (a tag battle).

### Ace Trainer Stefan: Stark Mountain room 2, optional, tag with Jasmin, cap 65

Tyranitar's Sand Stream, Torterra, Xatu and Garchomp.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Tyranitar | 62 | Chople Berry | Sand Stream | Adamant | Stone Edge, Crunch, Earthquake, Ice Punch |
| Torterra | 62 | Miracle Seed | Thick Fat | Adamant | Wood Hammer, Earthquake, Stone Edge, Crunch |
| Xatu | 62 | Leftovers | Magic Guard | Timid | Psychic, Drill Peck, Heat Wave, Roost |
| Garchomp | 63 | Yache Berry | Rough Skin | Jolly | Earthquake, Dragon Claw, Fire Fang, Stone Edge |

Today's team: Tyranitar 60 (Crunch, Earthquake, Stone Edge, ThunderPunch), Torterra 60 (Synthesis, Crunch, Stone Edge, Wood Hammer), Xatu 60 (Roost, Air Cutter, Heat Wave, Psychic). Expected: not readable yet (a tag battle).

### Ace Trainer Skylar: Stark Mountain room 2, optional, tag with Natasha, cap 65

Exploud, Rampardos, Pelipper and Fearow.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Exploud | 62 | Silk Scarf | Scrappy | Modest | Hyper Voice, Flamethrower, Focus Blast, Ice Beam |
| Rampardos | 62 | Lum Berry | Rock Head | Adamant | Head Smash, Zen Headbutt, Earthquake, Fire Punch |
| Pelipper | 62 | Mystic Water | Unburden | Modest | Surf, Air Slash, Ice Beam, Roost |
| Fearow | 63 | Sharp Beak | Sniper | Jolly | Drill Peck, Tri Attack, U-turn, Heat Wave |

Today's team: Exploud 60 (Hyper Voice, Flamethrower, Focus Blast, Ice Beam), Rampardos 60 (Head Smash, Zen Headbutt, Earthquake, ThunderPunch), Pelipper 60 (Air Slash, Hydro Pump, Roost, Ice Beam). Expected: not readable yet (a tag battle).

### Ace Trainer Abel: Stark Mountain room 2, optional, tag with Monique, cap 65

Glalie, Crobat, Typhlosion's Eruption and Gyarados.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Glalie | 62 | Focus Sash | Ice Body | Jolly | Ice Shard, Crunch, Earthquake, Ice Fang |
| Crobat | 62 | Sharp Beak | Inner Focus | Jolly | Brave Bird, Cross Poison, U-turn, Confuse Ray |
| Typhlosion | 62 | Charcoal | Blaze | Timid | Eruption, Flamethrower, Focus Blast, ThunderPunch |
| Gyarados | 63 | Wacan Berry | Intimidate | Adamant | Waterfall, Earthquake, Ice Fang, Stone Edge |

Today's team: Glalie 60 (Dark Pulse, Ice Beam, Sheer Cold, Crunch), Crobat 60 (Brave Bird, Cross Poison, Confuse Ray, U-turn), Typhlosion 60 (Eruption, Focus Blast, ThunderPunch, Low Kick). Expected: not readable yet (a tag battle).

### Ace Trainer Kassandra: Stark Mountain room 2, optional, tag with Keenan, cap 65

Jumpluff's Sleep Powder and Memento, Steelix, Ampharos and Starmie.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Jumpluff | 62 | Focus Sash | Chlorophyll | Jolly | U-turn, Leech Seed, Sleep Powder, Memento |
| Steelix | 62 | Leftovers | Solid Rock | Adamant | Earthquake, Iron Head, Stone Edge, Ice Fang |
| Ampharos | 62 | Magnet | Static | Modest | Thunderbolt, Power Gem, Signal Beam, Focus Blast |
| Starmie | 63 | Mystic Water | Magic Guard | Timid | Surf, Psychic, Ice Beam, Thunderbolt |

Today's team: Jumpluff 60 (Memento, Giga Drain, Toxic, Bounce), Steelix 60 (Stone Edge, Earthquake, Iron Head, Thunder Fang), Ampharos 60 (ThunderPunch, Power Gem, Signal Beam, Fire Punch). Expected: not readable yet (a tag battle).

### Ace Trainer Jasmin: Stark Mountain room 2, optional, tag with Stefan, cap 65

Drapion, Magcargo, Sceptile and Vaporeon's Helping Hand.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Drapion | 62 | Black Sludge | Hyper Cutter | Jolly | Cross Poison, Crunch, Earthquake, X-Scissor |
| Magcargo | 62 | Charcoal | Solid Rock | Modest | Flamethrower, Earth Power, AncientPower, Will-O-Wisp |
| Sceptile | 62 | Miracle Seed | Overgrow | Jolly | Leaf Blade, Earthquake, Dragon Claw, X-Scissor |
| Vaporeon | 63 | Leftovers | Water Absorb | Bold | Surf, Ice Beam, Wish, Helping Hand |

Today's team: Drapion 60 (Cross Poison, Crunch, X-Scissor, Aerial Ace), Magcargo 60 (Flamethrower, Earth Power, AncientPower, Toxic), Sceptile 60 (Leaf Blade, Night Slash, Dragon Claw, ThunderPunch). Expected: not readable yet (a tag battle).

### Ace Trainer Natasha: Stark Mountain room 2, optional, tag with Skylar, cap 65

Wigglytuff's screens, Lopunny's Fake Out, Medicham and Alakazam.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Wigglytuff | 62 | Leftovers | Cute Charm | Modest | Hyper Voice, Reflect, Light Screen, Flamethrower |
| Lopunny | 62 | Silk Scarf | Scrappy | Jolly | Fake Out, Jump Kick, Dizzy Punch, Ice Punch |
| Medicham | 62 | Black Belt | Pure Power | Adamant | Hi Jump Kick, Zen Headbutt, Ice Punch, Bullet Punch |
| Alakazam | 63 | TwistedSpoon | Magic Guard | Timid | Psychic, Focus Blast, Shadow Ball, Energy Ball |

Today's team: Wigglytuff 60 (Hyper Voice, Reflect, Light Screen, Shadow Ball), Lopunny 60 (Bounce, Jump Kick, Fire Punch, Ice Punch), Medicham 60 (Recover, Psycho Cut, Hi Jump Kick, Ice Punch). Expected: not readable yet (a tag battle).

### Ace Trainer Monique: Stark Mountain room 2, optional, tag with Abel, cap 65

Luxray, a Flame Orb Ursaring, Gliscor and Kangaskhan's Fake Out.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Luxray | 62 | Magnet | Tinted Lens | Adamant | Thunder Fang, Crunch, Superpower, Ice Fang |
| Ursaring | 62 | Flame Orb | Guts | Adamant | Facade, Close Combat, Crunch, Earthquake |
| Gliscor | 62 | Toxic Orb | Poison Heal | Jolly | Earthquake, U-turn, Ice Fang, Stone Edge |
| Kangaskhan | 63 | Sitrus Berry | Scrappy | Adamant | Double-Edge, Earthquake, Sucker Punch, Fake Out |

Today's team: Luxray 60 (Discharge, Crunch, Thunder Wave, Facade), Ursaring 60 (Hammer Arm, Stone Edge, Swords Dance, Giga Impact), Gliscor 60 (Aerial Ace, X-Scissor, Earthquake, Quick Attack). Expected: not readable yet (a tag battle).

### Psychic Sterling: Stark Mountain room 2, optional, tag beside Buck, cap 65

Gallade's Sacred Sword behind Solrock's Will-O-Wisp and Chimecho's Yawn.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Solrock | 62 | Leftovers | Levitate | default | Rock Slide, Zen Headbutt, Will-O-Wisp, Morning Sun |
| Chimecho | 62 | Sitrus Berry | Levitate | default | Psyshock, Dazzling Gleam, Heal Bell, Yawn |
| Gallade | 63 | Black Belt | Justified | default | Sacred Sword, Psycho Cut, Leaf Blade, Night Slash |

Today's team: Solrock 60 (Iron Head, Stone Edge, Zen Headbutt, Explosion), Gallade 60 (Earthquake, Poison Jab, Psycho Cut, Close Combat), Chimecho 60 (Energy Ball, Hidden Power, Psychic, Shadow Ball). Expected: not readable yet (a tag battle).

### Psychic Chelsey: Stark Mountain room 2, optional, tag beside Buck, cap 65

Moonblast from Lunatone and Gardevoir, Mismagius's Mystical Fire, Gardevoir's Hypnosis.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Lunatone | 62 | Leftovers | Levitate | default | Moonblast, Psychic, Earth Power, Ice Beam |
| Mismagius | 62 | Spell Tag | Levitate | default | Shadow Ball, Mystical Fire, Dazzling Gleam, Thunderbolt |
| Gardevoir | 63 | Pixie Plate | Trace | default | Moonblast, Psyshock, Mystical Fire, Hypnosis |

Today's team: Lunatone 60 (Heal Block, Psychic, Future Sight, Explosion), Gardevoir 60 (Future Sight, Captivate, Hypnosis, Dream Eater), Mismagius 60 (Shadow Ball, Thunderbolt, Psychic, Will-O-Wisp). Expected: not readable yet (a tag battle).

### Black Belt Ray: Stark Mountain room 2, optional, tag beside Buck, cap 65

Special fighters: Lucario's Nasty Plot on an Expert Belt, Toxicroak's Focus Blast and Vacuum Wave, Breloom's Mach Punch.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Breloom | 62 | Coba Berry | Technician | default | Mach Punch, Seed Bomb, Rock Tomb, Stun Spore |
| Toxicroak | 62 | Black Sludge | Dry Skin | default | Sludge Bomb, Focus Blast, Dark Pulse, Vacuum Wave |
| Lucario | 63 | Expert Belt | Adaptability | default | Aura Sphere, Flash Cannon, Dark Pulse, Nasty Plot |

Today's team: Breloom 60 (Seed Bomb, Mach Punch, ThunderPunch, Spore), Toxicroak 60 (Sludge Bomb, Nasty Plot, Focus Blast, Dark Pulse), Lucario 60 (Flash Cannon, Vacuum Wave, Psychic, Aura Sphere). Expected: not readable yet (a tag battle).

### Black Belt Jarrett: Stark Mountain room 2, optional, tag beside Buck, cap 65

A Guts Machamp on a Flame Orb beside Blaziken's Brave Bird and Poliwrath's Liquidation and Hypnosis.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Poliwrath | 62 | Leftovers | Water Absorb | default | Liquidation, Drain Punch, Ice Punch, Hypnosis |
| Blaziken | 62 | Charcoal | Blaze | default | Blaze Kick, Brave Bird, Knock Off, ThunderPunch |
| Machamp | 63 | Flame Orb | Guts | default | Facade, Close Combat, Knock Off, Bullet Punch |

Today's team: Machamp 60 (Cross Chop, Fire Punch, Ice Punch, ThunderPunch), Poliwrath 60 (DynamicPunch, Waterfall, Ice Punch, Headbutt), Blaziken 60 (Flare Blitz, Brave Bird, Sky Uppercut, ThunderPunch). Expected: not readable yet (a tag battle).

### Veteran Harlan: Stark Mountain room 2, optional, tag beside Buck, cap 65

Raticate's Super Fang, Drifblim's Will-O-Wisp then Hex, and a Life Orb Shiftry's Leaf Storm.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Raticate | 62 | Silk Scarf | Guts | default | Super Fang, Sucker Punch, Crunch, U-turn |
| Drifblim | 62 | Sitrus Berry | Unburden | default | Shadow Ball, Hex, Will-O-Wisp, Air Slash |
| Shiftry | 63 | Life Orb | Chlorophyll | default | Leaf Storm, Dark Pulse, Extrasensory, Sucker Punch |

Today's team: Raticate 60 (Endeavor, Super Fang, Crunch, Quick Attack), Drifblim 60 (Thunderbolt, Shadow Ball, Toxic, Air Cutter), Shiftry 60 (Leaf Storm, Dark Pulse, Extrasensory, Shadow Ball). Expected: not readable yet (a tag battle).

### Commander Mars: Stark Mountain room 1, optional, single, boss, cap 65

Mars's last stand: Bronzong leads with Stealth Rock and Explosion (the trade) behind a Focus Sash, then Persian's Fake Out, Crobat, Umbreon, Purugly and a Luxray ace with Howl.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Bronzong | 63 | Focus Sash | Levitate | Relaxed | Stealth Rock, Gyro Ball, Earthquake, Explosion |
| Persian | 63 | Silk Scarf | Technician | Jolly | Fake Out, U-turn, Knock Off, Aerial Ace |
| Crobat | 64 | Sharp Beak | Inner Focus | Jolly | Brave Bird, Cross Poison, U-turn, Roost |
| Umbreon | 64 | Leftovers | Synchronize | Calm | Payback, Toxic, Wish, Protect |
| Purugly | 64 | Sitrus Berry | Defiant | Jolly | Body Slam, Sucker Punch, Knock Off, U-turn |
| Luxray | 65 | Expert Belt | Tinted Lens | Adamant | Thunder Fang, Crunch, Superpower, Howl |

Today's team: Solrock 59 (Zen Headbutt, Stone Edge, Light Screen, Will-O-Wisp), Persian 59 (Fake Out, Headbutt, Aerial Ace, U-turn), Purugly 60 (Sitrus Berry; Slash, Shadow Claw, Aerial Ace, Hypnosis). Expected: about 95 / 1.2 / 13 in my simulator, where today's file reads 100 / 0.0 / 100.

### Commander Jupiter: Stark Mountain room 1, optional, single, boss, cap 65

Jupiter's last stand: Drapion's Toxic Spikes behind a Focus Sash, Lunatone's Stealth Rock, Tangrowth's Sleep Powder, Spiritomb, Crobat and a Skuntank ace.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Drapion | 63 | Focus Sash | Hyper Cutter | Jolly | Toxic Spikes, Cross Poison, Crunch, Earthquake |
| Lunatone | 63 | Leftovers | Levitate | Modest | Stealth Rock, Psychic, Earth Power, Ice Beam |
| Tangrowth | 64 | Leftovers | Regenerator | Relaxed | Seed Bomb, Earthquake, Knock Off, Sleep Powder |
| Spiritomb | 64 | Leftovers | Pressure | Careful | Shadow Ball, Sucker Punch, Will-O-Wisp, Pain Split |
| Crobat | 64 | Sharp Beak | Inner Focus | Jolly | Brave Bird, Cross Poison, U-turn, Roost |
| Skuntank | 65 | Dread Plate | Aftermath | Adamant | Crunch, Poison Jab, Fire Blast, Sucker Punch |

Today's team: Lunatone 59 (Psychic, AncientPower, Earth Power, Stealth Rock), Delcatty 59 (Ice Beam, Thunderbolt, Shadow Ball, Thunder Wave), Skuntank 60 (Sitrus Berry; Night Slash, Poison Jab, Flamethrower, SmokeScreen). Expected: about 96 / 2.0 / 6 in my simulator, where today's file reads 100 / 0.0 / 99.

### Dragon Tamer Keegan: Route 228 (sand), optional, single, cap 65

The Trapinch line on Eviolites, Trapinch and Vibrava, beside Gabite's Scale Shot and a Levitate Flygon.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Vibrava | 63 | Eviolite | Tinted Lens | default | Earth Power, Bug Buzz, Dragon Pulse, U-turn |
| Gabite | 60 | Eviolite | Rough Skin | default | Scale Shot, Earthquake, Stone Edge, Fire Fang |
| Trapinch | 60 | Eviolite | Arena Trap | default | Earthquake, Crunch, Rock Slide, Superpower |
| Flygon | 61 | none | Levitate | default | Earthquake, Outrage, U-turn, Fire Punch |

Today's team: Trapinch 55 (default moves), Vibrava 57 (default moves). Expected: 99 / 1.68 / 8 blind in my simulator in sand, about 63 clean in the scorer's terms.

### Ace Trainer Jose: Route 228 (sand), optional, single, Ace Trainer, cap 65

Sand: a Sand Rush Sandslash lays Stealth Rock behind a Focus Sash, then Golduck, Manectric, Rhyperior, Steelix and a Garchomp ace.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Sandslash | 62 | Focus Sash | Sand Rush | Jolly | Stealth Rock, Earthquake, Stone Edge, Knock Off |
| Golduck | 62 | Mystic Water | Swift Swim | Modest | Surf, Ice Beam, Psychic, Calm Mind |
| Manectric | 62 | Magnet | Lightning Rod | Timid | Thunderbolt, Flamethrower, Signal Beam, Thunder Wave |
| Rhyperior | 63 | Passho Berry | Solid Rock | Adamant | Earthquake, Stone Edge, Ice Punch, Hammer Arm |
| Steelix | 62 | Leftovers | Solid Rock | Adamant | Earthquake, Iron Head, Stone Edge, Ice Fang |
| Garchomp | 64 | Yache Berry | Rough Skin | Jolly | Earthquake, Dragon Claw, Fire Fang, Stone Edge |

Today's team: Golduck 58 (Hydro Pump, Brick Break, Zen Headbutt, Screech), Sandslash 58 (Earthquake, Crush Claw, Poison Jab, Sand Tomb), Manectric 58 (Thunder Fang, Fire Fang, Quick Attack, Giga Impact). Expected: about 86 / 3.4 / 0 with a planned six in sand; read blind, 4 / 5.9 / 0.

### Ace Trainer Moira: Route 228 (sand), optional, single, Ace Trainer, cap 65

Ground and Rock in the sand: Claydol's Stealth Rock, Gastrodon, a Sand Force Dugtrio with Soft Sand, Hippowdon, Golem and a Dragon Dance Tyranitar ace.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Claydol | 62 | Leftovers | Levitate | Modest | Earth Power, Psychic, Ice Beam, Stealth Rock |
| Gastrodon | 62 | Sitrus Berry | Dry Skin | Modest | Earth Power, Surf, Ice Beam, Sludge Bomb |
| Dugtrio | 62 | Soft Sand | Sand Force | Jolly | Earthquake, Stone Edge, Sucker Punch, Aerial Ace |
| Hippowdon | 63 | Leftovers | Thick Fat | Impish | Earthquake, Crunch, Ice Fang, Slack Off |
| Golem | 62 | Hard Stone | Shell Armor | Adamant | Earthquake, Stone Edge, Sucker Punch, Fire Punch |
| Tyranitar | 64 | Chople Berry | Unnerve | Adamant | Stone Edge, Crunch, Earthquake, Dragon Dance |

Today's team: Dugtrio 58 (Earthquake, Fissure, Night Slash, Stone Edge), Gastrodon 58 (Muddy Water, Recover, Toxic, Protect), Claydol 58 (Earthquake, Psychic, AncientPower, Cosmic Power). Expected: about 98 / 1.4 / 1 with a planned six in sand; read blind, 30 / 5.0 / 1.

### Ace Trainer Meagan: Route 228 (sand), optional, single, Ace Trainer, cap 65

Mixed in the sand: Delcatty's Fake Out, an Adaptability Abomasnow, Probopass, Cacturne, a Poison Heal Gliscor and an Aggron ace.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Delcatty | 62 | Silk Scarf | Cute Charm | Jolly | Fake Out, Double-Edge, Sucker Punch, Thunder Wave |
| Abomasnow | 62 | NeverMeltIce | Adaptability | Modest | Blizzard, Energy Ball, Earthquake, Ice Shard |
| Probopass | 62 | Leftovers | Solid Rock | Modest | Power Gem, Earth Power, Flash Cannon, Thunder Wave |
| Cacturne | 63 | Miracle Seed | Water Absorb | Adamant | Seed Bomb, Sucker Punch, Drain Punch, Swords Dance |
| Gliscor | 62 | Toxic Orb | Poison Heal | Jolly | Earthquake, U-turn, Ice Fang, Stone Edge |
| Aggron | 64 | Lum Berry | Rock Head | Adamant | Double-Edge, Iron Head, Earthquake, Stone Edge |

Today's team: Delcatty 59 (Fake Out, Captivate, Faint Attack, Double-Edge), Abomasnow 59 (Ice Shard, Avalanche, Razor Leaf, Water Pulse). Expected: about 100 / 1.2 / 16 with a planned six in sand; read blind, 47 / 4.3 / 1.

### Psychic Corbin: Route 228 (sand), optional, single, cap 65

Stealth Rock from Bronzong, then a Magic Bounce Espeon, Xatu and Gallade's Sacred Sword. A Pure Power Medicham read far past the band and left.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Bronzong | 63 | Leftovers | Levitate | default | Stealth Rock, Gyro Ball, Psychic, Hypnosis |
| Espeon | 61 | none | Magic Bounce | default | Psyshock, Dazzling Gleam, Shadow Ball, Morning Sun |
| Xatu | 60 | Sitrus Berry | Magic Bounce | default | Psychic, Heat Wave, U-turn, Roost |
| Gallade | 61 | none | Justified | default | Sacred Sword, Psycho Cut, Leaf Blade, Night Slash |

Today's team: Medicham 58 (Psycho Cut, Ice Punch, Fire Punch, Recover), Gallade 58 (Leaf Blade, X-Scissor, Night Slash, Close Combat). Expected: 92 / 1.92 / 12 blind in my simulator in sand, about 65 clean in the scorer's terms.

### Black Belt Davon: Route 228 (sand), optional, single, cap 65

Annihilape's Rage Fist, a No Guard Machamp's Cross Chop and Stone Edge, Hariyama's Whirlwind and Hitmonlee's Fake Out.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Hitmonlee | 63 | Sitrus Berry | Reckless | default | Hi Jump Kick, Knock Off, Blaze Kick, Fake Out |
| Annihilape | 62 | Leftovers | Defiant | default | Rage Fist, Drain Punch, U-turn, Ice Punch |
| Hariyama | 61 | none | Thick Fat | default | Close Combat, Knock Off, Bullet Punch, Whirlwind |
| Machamp | 62 | Sitrus Berry | No Guard | default | Cross Chop, Stone Edge, Knock Off, Bullet Punch |

Today's team: Primeape 57 (ThunderPunch, Seed Bomb, U-turn, Close Combat), Hariyama 57 (Stone Edge, Whirlwind, Close Combat, Reversal), Machamp 57 (Bullet Punch, Cross Chop, Poison Jab, Stone Edge). Expected: 98 / 1.60 / 16 blind in my simulator in sand, about 67 clean in the scorer's terms.

### Pkmn Ranger Kyler: Route 228 (sand), optional, single, cap 65

Sand Rush Sandslash in the sand, beside Exeggutor's Sleep Powder, an Intimidate Feraligatr and Zangoose.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Exeggutor | 63 | Sitrus Berry | Chlorophyll | default | Leaf Storm, Psyshock, Sleep Powder, Synthesis |
| Sandslash | 62 | none | Sand Rush | default | Earthquake, Knock Off, Stone Edge, Rapid Spin |
| Feraligatr | 61 | none | Intimidate | default | Liquidation, Crunch, Ice Punch, Aqua Jet |
| Zangoose | 62 | none | Hyper Cutter | default | Close Combat, Knock Off, Quick Attack, Body Slam |

Today's team: Exeggutor 57 (Light Screen, Synthesis, Psychic, Leaf Storm), Zangoose 57 (Detect, Slash, X-Scissor, Close Combat), Feraligatr 57 (Crunch, Aqua Tail, Superpower, Ice Fang). Expected: 97 / 1.74 / 11 blind in my simulator in sand, about 65 clean in the scorer's terms.

### Pkmn Ranger Krista: Route 228 (sand), optional, single, cap 65

Rock Head: Aggron's Head Smash and Heavy Slam with no recoil, a Thick Club Marowak, Golem and a Dry Skin Gastrodon.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Golem | 61 | Sitrus Berry | Shell Armor | default | Stone Edge, Earthquake, Sucker Punch, Rock Polish |
| Gastrodon | 63 | Leftovers | Dry Skin | default | Scald, Earth Power, Recover, Clear Smog |
| Marowak | 60 | Thick Club | Rock Head | default | Bonemerang, Stone Edge, Knock Off, Fire Punch |
| Aggron | 62 | none | Rock Head | default | Head Smash, Heavy Slam, Earthquake, Iron Defense |

Today's team: Aggron 58 (Stone Edge, Iron Head, Double-Edge, Metal Burst), Marowak 58 (Earthquake, Belly Drum, Fire Punch, ThunderPunch). Expected: 97 / 1.47 / 20 blind in my simulator in sand, about 68 clean in the scorer's terms.

### Ace Trainer Felix: Route 229, optional, single, Ace Trainer, cap 65

Ghosts and dragons: Dusknoir's Will-O-Wisp, Gengar, a Nasty Plot Houndoom, a Dragon Dance Altaria, Kingdra and a Salamence ace.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Dusknoir | 62 | Leftovers | Levitate | Adamant | Shadow Punch, Earthquake, Ice Punch, Will-O-Wisp |
| Gengar | 62 | Life Orb | Levitate | Timid | Shadow Ball, Sludge Bomb, Focus Blast, Thunderbolt |
| Houndoom | 62 | Charcoal | Flash Fire | Timid | Flamethrower, Dark Pulse, Sludge Bomb, Nasty Plot |
| Altaria | 63 | Sitrus Berry | Serene Grace | Adamant | Dragon Claw, Earthquake, Roost, Dragon Dance |
| Kingdra | 62 | Mystic Water | Sniper | Modest | Surf, Dragon Pulse, Ice Beam, Signal Beam |
| Salamence | 64 | Yache Berry | Intimidate | Adamant | Outrage, Earthquake, Fire Fang, Aerial Ace |

Today's team: Dusknoir 58 (Shadow Sneak, Payback, Curse, Will-O-Wisp), Salamence 58 (Dragon Claw, Aerial Ace, Zen Headbutt, Crunch). Expected: about 100 / 2.5 / 0 with a planned six; read blind, 32 / 5.4 / 0.

### Ace Trainer Dana: Route 229, optional, single, Ace Trainer, cap 65

Psychic and Dark: Mightyena, Roserade's Spikes, Espeon, Milotic, Umbreon and a Life Orb Gardevoir ace.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Mightyena | 62 | Sitrus Berry | Intimidate | Adamant | Crunch, Sucker Punch, Ice Fang, Thunder Fang |
| Roserade | 62 | Focus Sash | Natural Cure | Timid | Spikes, Sludge Bomb, Energy Ball, Shadow Ball |
| Espeon | 62 | TwistedSpoon | Synchronize | Timid | Psychic, Shadow Ball, Signal Beam, Calm Mind |
| Milotic | 63 | Leftovers | Filter | Bold | Surf, Ice Beam, Recover, Toxic |
| Umbreon | 62 | Leftovers | Synchronize | Calm | Payback, Toxic, Wish, Protect |
| Gardevoir | 64 | Life Orb | Magic Guard | Modest | Psychic, Thunderbolt, Focus Blast, Calm Mind |

Today's team: Mightyena 57 (Crunch, Sucker Punch, Iron Tail, Thunder Fang), Gardevoir 57 (Psychic, Magical Leaf, Shock Wave, Shadow Ball). Expected: about 100 / 1.5 / 0 with a planned six; read blind, 58 / 3.7 / 5.

### Ace Trainer Sandra: Route 229, optional, single, Ace Trainer, cap 65

Today's Ninetales, Raichu and Cacturne grown: Vaporeon's Wish, Toxicroak and a Swords Dance Leafeon ace.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Ninetales | 62 | Charcoal | Magic Guard | Timid | Flamethrower, Energy Ball, Will-O-Wisp, Nasty Plot |
| Raichu | 62 | Magnet | Lightning Rod | Timid | Thunderbolt, Grass Knot, Focus Blast, Thunder Wave |
| Cacturne | 62 | Miracle Seed | Water Absorb | Adamant | Seed Bomb, Sucker Punch, Drain Punch, Swords Dance |
| Vaporeon | 63 | Leftovers | Water Absorb | Bold | Surf, Ice Beam, Wish, Protect |
| Toxicroak | 62 | Black Sludge | Dry Skin | Adamant | Poison Jab, Cross Chop, Sucker Punch, Ice Punch |
| Leafeon | 64 | Lum Berry | Chlorophyll | Jolly | Seed Bomb, X-Scissor, Knock Off, Swords Dance |

Today's team: Cacturne 56 (Seed Bomb, ThunderPunch, Sucker Punch, Destiny Bond), Raichu 56 (Grass Knot, Hidden Power, Thunder Wave, Thunder), Ninetales 56 (Fire Blast, Will-O-Wisp, Energy Ball, Calm Mind). Expected: about 100 / 0.8 / 38 with a planned six; read blind, 64 / 3.1 / 10.

### Pkmn Ranger Deshawn: Route 229, optional, single, cap 65

Contrary and Protean: Spinda's Superpower raises its stats, Kecleon changes type with Drain Punch (Deshawn's reward TM), Persian's Fake Out and Granbull.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Kecleon | 62 | Lum Berry | Protean | default | Sucker Punch, Shadow Sneak, Knock Off, Drain Punch |
| Granbull | 62 | Leftovers | Intimidate | default | Play Rough, Close Combat, Earthquake, Thunder Wave |
| Spinda | 60 | none | Contrary | default | Superpower, Sucker Punch, Return, Ice Punch |
| Persian | 63 | Silk Scarf | Technician | default | Fake Out, Knock Off, U-turn, Play Rough |

Today's team: Spinda 56 (Sucker Punch, Double-Edge, Fire Punch, Thrash), Kecleon 56 (Substitute, Sucker Punch, Shadow Claw, Ice Punch), Granbull 56 (Headbutt, Fire Punch, Superpower, Crunch). Expected: 95 / 1.25 / 30 blind in my simulator, about 72 clean in the scorer's terms.

### Swimmer Glenn: Route 230, optional, single, cap 65

Sniper Octillery on a Scope Lens, Seaking's Megahorn, Lumineon and Politoed's Encore. Politoed keeps Water Absorb rather than Drizzle, since Joanna is the route's rain team.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Octillery | 61 | Scope Lens | Sniper | default | Hydro Pump, Ice Beam, Fire Blast, Energy Ball |
| Lumineon | 61 | Leftovers | Water Veil | default | Scald, U-turn, Ice Beam, Alluring Voice |
| Seaking | 62 | none | Lightning Rod | default | Waterfall, Megahorn, Drill Run, Knock Off |
| Politoed | 63 | Sitrus Berry | Water Absorb | default | Scald, Ice Beam, Encore, Focus Blast |

Today's team: Octillery 55 (Hydro Pump, Signal Beam, Ice Beam, Hyper Beam), Politoed 55 (Perish Song, Ice Beam, Surf, Hyper Voice). Expected: 97 / 1.40 / 32 blind in my simulator, about 73 clean in the scorer's terms.

### Swimmer Kurt: Route 230, optional, single, cap 65

Spikes from a Focus Sash Cloyster, then Kingler's and Crawdaunt's Crabhammer. Today's Guillotines are gone (no one-hit KO moves).

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Cloyster | 61 | Focus Sash | Shell Armor | default | Spikes, Icicle Crash, Liquidation, Rapid Spin |
| Omastar | 61 | Leftovers | Shell Armor | default | Scald, Ice Beam, Earth Power, AncientPower |
| Kingler | 62 | Sitrus Berry | Hyper Cutter | default | Crabhammer, Knock Off, X-Scissor, Rock Slide |
| Crawdaunt | 63 | none | Hyper Cutter | default | Crabhammer, Knock Off, Aqua Jet, X-Scissor |

Today's team: Kingler 55 (Guillotine, Superpower, Crabhammer, X-Scissor), Crawdaunt 55 (Crabhammer, Swords Dance, Crunch, Guillotine). Expected: 96 / 1.39 / 38 blind in my simulator, about 75 clean in the scorer's terms.

### Swimmer Sam: Route 230, optional, single, cap 65

Floatzel's Waterfall (Sam's reward HM) and Ice Spinner, Gastrodon's Scald and Recover, Pelipper's Hurricane, Walrein's Toxic. Today's Sheer Cold is gone.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Gastrodon | 62 | Leftovers | Dry Skin | default | Scald, Earth Power, Recover, Clear Smog |
| Pelipper | 61 | Sitrus Berry | Unburden | default | Scald, Hurricane, U-turn, Roost |
| Floatzel | 62 | Mystic Water | Water Veil | default | Waterfall, Ice Spinner, Crunch, Aqua Jet |
| Walrein | 63 | none | Filter | default | Ice Beam, Surf, Super Fang, Toxic |

Today's team: Walrein 55 (Rest, Surf, Blizzard, Sheer Cold), Gastrodon 55 (Surf, Earth Power, Hidden Power, Recover). Expected: 96 / 1.26 / 30 blind in my simulator, about 72 clean in the scorer's terms.

### Swimmer Joanna: Route 230, optional, single, cap 65

Rain from Luvdisc's Rain Dance on a Damp Rock, then Lapras's Thunder that cannot miss in it, a Swift Swim Golduck and a Hydration Vaporeon.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Luvdisc | 63 | Damp Rock | Hydration | default | Rain Dance, Scald, Draining Kiss, Charm |
| Golduck | 60 | none | Swift Swim | default | Hydro Pump, Ice Beam, Psyshock, Encore |
| Lapras | 61 | none | Hydration | default | Freeze-Dry, Surf, Thunder, Ice Shard |
| Vaporeon | 62 | Sitrus Berry | Hydration | default | Scald, Ice Beam, Wish, Protect |

Today's team: Luvdisc 55 (Aqua Ring, Surf, Rain Dance, Blizzard), Lapras 55 (Psychic, Thunder, Hydro Pump, Sheer Cold). Expected: 98 / 1.37 / 28 blind in my simulator, about 71 clean in the scorer's terms.

### Swimmer Sophia: Route 230, optional, single, cap 65

Spikes from Delibird, then Glalie's Freeze-Dry, Dewgong's Flip Turn and Mantine's Hurricane.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Delibird | 61 | NeverMeltIce | Vital Spirit | default | Spikes, Ice Shard, Drill Run, Brave Bird |
| Glalie | 61 | none | Solid Rock | default | Freeze-Dry, Earthquake, Crunch, Ice Shard |
| Dewgong | 62 | Leftovers | Thick Fat | default | Ice Beam, Surf, Flip Turn, Encore |
| Mantine | 63 | Sitrus Berry | Water Absorb | default | Scald, Hurricane, Roost, Ice Beam |

Today's team: Delibird 55 (Present, Ice Beam), Mantine 55 (Confuse Ray, Signal Beam, Aqua Ring, Hydro Pump). Expected: 96 / 1.12 / 39 blind in my simulator, about 76 clean in the scorer's terms.

### Swimmer Mallory: Route 230, optional, single, cap 65

Masquerain's Quiver Dance and Sludge Bomb (Mallory's reward TM), Tentacruel, Qwilfish's Intimidate and Ludicolo.

| Pokemon | Level | Item | Ability | Nature | Moves |
|---|---|---|---|---|---|
| Qwilfish | 61 | Black Sludge | Intimidate | default | Poison Jab, Waterfall, Thunder Wave, Aqua Jet |
| Tentacruel | 61 | Leftovers | Clear Body | default | Scald, Sludge Bomb, Knock Off, Rapid Spin |
| Masquerain | 63 | none | Intimidate | default | Bug Buzz, Hurricane, Sludge Bomb, Quiver Dance |
| Ludicolo | 61 | none | Own Tempo | default | Giga Drain, Scald, Ice Beam, Leech Seed |

Today's team: Masquerain 55 (Hydro Pump, Air Slash, Whirlwind, Bug Buzz), Ludicolo 55 (Energy Ball, Leech Seed, Rain Dance, Surf). Expected: 93 / 1.15 / 44 blind in my simulator, about 77 clean in the scorer's terms.


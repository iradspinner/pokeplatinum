# Barry 5 and Riley: drafts for Ian

The last two pieces of Byron's split, drafted on branch `overseer-barry5-riley` and answered by Ian on 2026-11-01: Barry 5 on Canalave's bridge (a boss at his honour cap of 50, after the Pal Park double) and Riley's two fights on Iron Island (both mini-bosses under Byron's cap of 53, Ian, 2026-10-31). His answers are below and applied on the branch, which lands through the Overseer. Every number comes from cheap checks; no scorer reading was run.

## Ian's answers (2026-11-01)

Riley's two fights use two slots, as built: the door battle on slot 87, the partner in his own file (decision 1). Serperior keeps Leaf Storm and now holds a Miracle Seed (decision 2). Both Barry 5 versions stay as built: "The teams look similarly hard to me, I assume it is just a box difference" (decisions 3 and 4). Riley's partner keeps four Pokemon and his Kommo-o stays (decisions 5 and 6). The grunts keep their themes and become named officers: Officer Boreas, the wind, in the male grunt's sprite, and Officer Laverna, the thieves, in the female grunt's sprite (decision 7). They carry the grunt classes with "Officer" names, as Phobos and Deimos do, the island's scene and their defeat lines name them, and their row is in `boss-shapes.md`'s officers table. As named officers they are mini-bosses, and their aces at 50 and 51, two and three under the stretch's cap of 53, stand. Riley's door fight stays out of `fights.json` (decision 8). The sections after this one are the draft's, from before these answers; where they say "the grunts", read Boreas (grunt 1) and Laverna (grunt 2).

What the answers changed in the tree, beside the Miracle Seed: both officers' names, Laverna's class, their defeat lines ("Our tailwind turned on us! How did it blow your way?" and "Robbed blind! That's my job, not yours!"), the B2F scene's speaker labels (Laverna no longer calls Boreas brother), the east object's sprite, and the map's two objects named `LOCALID_BOREAS` and `LOCALID_LAVERNA`. Each is registered: name, class and messages in `trainers_diverged.json`, text bank 277 in `import_base_rom.TEXT_BANKS_SKIPPED` for `verify_narcs --text`, and the map's events and script in `bulk_events.py` and `bulk_scripts.py`. The branch has merged `origin/oxide`, and the script index is regenerated.

## Summary

**What could not be checked.** No reading reads a tag double, so Riley's partner team and the closing tag battle against the two grunts are unread; the grunts were run one at a time as singles, which says only that each is weak alone. Nothing was seen in game. Riley's door fight was read on Byron's boxes at 53, which hold catches from after the door, so he reads a little easier than he is. The probe's numbers swing between runs: the Turtwig version's best-six wins moved from 48 to 79 when only Serperior's and Empoleon's sets changed.

**Barry 5.** Each version brings the pool doc's Barry 5 column, grown out of Barry 3's bait and setup and Ian's Barry 4: Staraptor leads, Primeape keeps Barry 3's set, Snorlax plays its last fight, the two element partners keep their Barry 4 ideas, and the ace is the starter at 50. Every move is legal at its level, with one egg-list addition (Leaf Storm on Snivy). Staraptor passes Ian's lead test in full on two boxes of three. The Scorbunny player's version reads far easier than the other two (decision 3).

**Riley.** His door battle and his partner on B2F both fought one trainer file, so they could not differ. The door battle now fights a free slot (trainer 87) and his own file is the partner (decision 1). The door six is Fighting and Steel around Lucario at 51, Steelix leading with Stealth Rock, and the lead passes Ian's test on every box but one common answer. It reads easier than Byron, as a mini-boss before the leader should. The two grunts are the wind and the thieves, four each, so the closing tag battle is ten against eight, near Veilstone's twelve against ten.

**Next steps.**

| Step | Who | Time |
|---|---|---|
| Land the branch | the Overseer | 30 minutes |
| In game: Riley's door battle (slot 87's name, sprite, no defeat line), Kecleon's Trick, the tag battle with Boreas and Laverna named and Laverna in the female sprite | Ian with the test kit | 20 minutes |

## Ian's decisions (answered above)

1. Riley's two teams: door battle in free slot 87 and partner in his own file (my pick, one script line), or one team for both fights (no script change, but the partner is then a six-member mini-boss team)?
2. Serperior: Leaf Storm under Contrary, on Snivy's egg list, with a Miracle Seed for the Big Root, which does nothing without Giga Drain (my pick; its knockouts rose from 8 to 13 to 72 to 182 a run), or Giga Drain and the Big Root as drafted first?
3. The Scorbunny version reads far easier (97 to 105 wins of 150 against 17 to 79): give Turtonator Earthquake for Iron Defense (my pick; 75 and 86, about Barry 4's), accept it, or name a stronger swap?
4. The Piplup version reads hardest (17 and 31): keep it as the rival's peak (my pick), or soften Torterra's Headlong Rush to Earthquake?
5. Riley's partner: four members (my pick, ten against eight), or three, vanilla's size (nine against eight)? B2F's four pairs fight beside the same partner.
6. Riley's Kommo-o at 50, a Dragon and Fighting type no boss uses (my pick), or Aggron for a heavier Steel lean?
7. The grunts' ideas, the wind and the thieves (my pick), or another Galactic theme?
8. Riley's door fight as a mini-boss entry in `fights.json` with no cap of its own, so the OxiDex lists it, or left out (my pick until Ian rules on how mini-bosses without caps are listed)?

## Barry 5

The ace sits at the cap of 50 and Snorlax at 49, in its last fight; the partners and Staraptor sit at 48 and Primeape at 47, which keeps it Primeape (Annihilape comes at 50). Every member has iv_scale 255, is male as in Barry 3 and 4, and holds its own item with its own nature; five natures are neutral. The AI flags stay Basic, Evaluate Attack and Expert: by the flags guide each setup move is one piece of an attacking plan, so Prioritize Extremes stays off, and there is no trade move, weather move or critical-hit idea. Speed is as the simulator builds each member.

The three shared members, the same in every version:

| Slot | Member | Level | Ability | Item | Nature | Speed | Moves | Grown from |
|---|---|---|---|---|---|---|---|---|
| Lead | Staraptor | 48 | Intimidate | Shell Bell | Docile | 120 | Brave Bird, Close Combat, U-turn, Tailwind | Barry 3's bait lead; Close Combat now hits the Rock and Steel walls that stopped it |
| 2 | Primeape | 47 | Defiant | Liechi Berry | Impish | 108 | Bulk Up, Drain Punch, Rage Fist, Ice Punch | Barry 3's set as Ian left it |
| 4 | Snorlax | 49 | Thick Fat | Chople Berry | Sassy | 44 | Curse, Body Slam, Earthquake, Crunch | Barry 4's Curse set; Crunch for the box's Ghosts |

By version (the file suffix names the starter Platinum had in the player's seat):

| Version | Slot | Member | Level | Ability | Item | Nature | Speed | Moves |
|---|---|---|---|---|---|---|---|---|
| Turtwig player (`_turtwig`) | 3 | Serperior | 48 | Contrary | Miracle Seed | Quirky | 128 | Glare, Leaf Storm, Scale Shot, Knock Off |
| | 5 | Greninja | 48 | Torrent | Expert Belt | Rash | 137 | Water Shuriken, Dark Pulse, Ice Beam, Gunk Shot |
| | Ace | Infernape | 50 | Iron Fist | Muscle Band | Hasty | 140 | Bulk Up, Fire Punch, Thunder Punch, Drain Punch |
| Scorbunny player (`_chimchar`) | 3 | Serperior | 48 | Contrary | Miracle Seed | Quirky | 128 | Glare, Leaf Storm, Scale Shot, Knock Off |
| | 5 | Turtonator | 48 | Shell Armor | Rocky Helmet | Bashful | 54 | Shell Trap, Flamethrower, Body Press, Iron Defense |
| | Ace | Empoleon | 50 | Torrent | Sitrus Berry | Lonely | 80 | Swords Dance, Waterfall, Earthquake, Drill Peck |
| Piplup player (`_piplup`) | 3 | Greninja | 48 | Torrent | Expert Belt | Rash | 137 | Water Shuriken, Dark Pulse, Ice Beam, Gunk Shot |
| | 5 | Turtonator | 48 | Shell Armor | Rocky Helmet | Bashful | 54 | Shell Trap, Flamethrower, Body Press, Iron Defense |
| | Ace | Torterra | 50 | Thick Fat | Coba Berry | Hardy | 76 | Rock Polish, Wood Hammer, Headlong Rush, Stone Edge |

Each version has four setup members (Primeape, Snorlax, one partner and the ace), as Barry 3 did, with Serperior's Leaf Storm and Scale Shot as self-boosts under Contrary. The Big Root was chosen for the first draft's Giga Drain and does nothing beside Leaf Storm; the checks below ran with it, so Serperior's Miracle Seed, Ian's answer, makes it a little stronger than read. Turtonator's Rocky Helmet fits Shell Trap: both punish a physical hit. Coba Berry is for the box's flyers (Corviknight in all 20 top sixes on box 3). Every member is past its evolution level.

### The cheap checks

The boxes are goal 3's at Barry 5's stretch, cut just before him and stood at his cap of 50; box 1 meets the Turtwig player's file, box 2 the Scorbunny player's, box 3 the Piplup player's. Each cell is the player's wins in 150 rough fights against the screen's best six, then its most-taken six (one number when they are the same six); higher is easier for the player. Barry 4 and Byron were rerun on this branch for scale and matched the boss check's numbers exactly.

| Fight, on its own boxes | Box 1 | Box 2 | Box 3 | Screen's best-six score |
|---|---|---|---|---|
| Barry 5, today's base-ROM six at 51 to 53 (boss check) | 5 | 32, 44 | 7, 8 | 8.85 and others |
| Barry 5, this draft | 79, 20 | 105, 97 | 17, 31 | 15.15, 15.70, 18.35 |
| Barry 5, the first draft (Giga Drain, Throat Chop) | 48, 23 | 116, 125 | 17, 31 | 15.15, 17.50, 18.35 |
| Barry 4 (42) | 52, 80 | 71, 45 | 59 | 12.90, 16.70, 16.35 |
| Byron (53) | 69, 81 | 67, 81 | 41, 86 | 18.15, 18.60, 19.75 |

So the Turtwig and Piplup versions read harder than Barry 4 and Byron on at least one six, and the Scorbunny version reads easier than both. Knockouts of the player's Pokemon while each member was in, per 150 fights, best six then most-taken six:

| Box | Staraptor | Primeape | Partner 1 | Snorlax | Partner 2 | Ace |
|---|---|---|---|---|---|---|
| 1 | 90, 101 | 100, 102 | Serperior 129, 72 | 136, 98 | Greninja 116, 138 | Infernape 188, 362 |
| 2 | 89, 77 | 100, 94 | Serperior 149, 182 | 149, 146 | Turtonator 63, 44 | Empoleon 174, 167 |
| 3 | 122, 110 | 141, 203 | Greninja 148, 153 | 130, 105 | Turtonator 137, 133 | Torterra 195, 148 |

The first draft's Serperior (Giga Drain) knocked out 13 and 8 on box 1, where the AI rarely sent it in; with Leaf Storm it is a real member on both boxes that carry it. The Scorbunny version's weak point is now Turtonator (44 to 63): Hippowdon and Glimmora, in 12 to 18 of the top 20 sixes, beat it at +2.5 each. A candidate with Earthquake for Iron Defense, in both versions that carry Turtonator:

| Box | Player's wins | Turtonator's knockouts | Its Earthquake picks |
|---|---|---|---|
| 2, Scorbunny player | 75, 86 (from 105, 97) | 66, 30 | 7 and 103 |
| 3, Piplup player | 19, 36 (from 17, 31) | 132, 134 | 38 and 7 |

It brings the Scorbunny version to about Barry 4's reading, mostly by letting Serperior stay in longer (179 and 303 knockouts), and leaves the Piplup version as it was within the probe's spread.

The AI plays every move. Setup picks per run: Snorlax's Curse 168 to 266, Primeape's Bulk Up 54 to 148, Empoleon's Swords Dance 31 to 48, Torterra's Rock Polish 101 to 106, Infernape's Bulk Up 30 to 41, Turtonator's Iron Defense 33 to 74. Leaf Storm was picked 115 to 308 times a run, Shell Trap 181 to 234. Staraptor opens with Close Combat or Brave Bird in most fights and Tailwind in 6 to 48.

Ian's lead test (each common answer to Staraptor, the member the AI's replacement rule draws in, and whether that member beats it):

| Box | Staraptor's answer (margin, sixes of 20) | Draws | Result |
|---|---|---|---|
| 1 | Corviknight (+1.5, 20) | Infernape, with Bulk Up | loses narrowly (+0.5) |
| 1 | Glimmora (+1.5, 15) | Greninja | beats it |
| 1 | Luxray (+0.5, 12) | Primeape, with Bulk Up | beats it |
| 2 | Hippowdon (+0.5, 17), Rotom (+1.5, 11) | Serperior | beats both |
| 2 | Glimmora (+1.5, 12), Rapidash (+0.5, 5) | Empoleon, with Swords Dance | beats both |
| 3 | Corviknight (+1.5, 20) | Turtonator, with Iron Defense | beats it |
| 3 | Carbink (+0.5, 6) | Torterra, with Rock Polish | beats it |
| 3 | Dubwool (+0.5, 5) | Primeape, with Bulk Up | beats it |

So the lead passes in full on boxes 2 and 3. On box 1 its most common answer, Corviknight, draws an Infernape that loses to it by a hair.

## Riley at the door

A mini-boss under Byron's cap of 53, in Mars 1's shape two under: Lucario at 51, Kommo-o at 50, Poliwrath at 49, the rest at 48. Riley's signature is Lucario, and his team is Fighting and Steel; it uses no line of Byron's six. iv_scale 255, AI flags Basic, Evaluate Attack and Expert (no trade move; setup is one piece of each member's plan). Mienshao sits two levels under Mienfoo's evolution at 50, which the rulings allow.

| Slot | Member | Level | Ability | Item | Nature | Speed | Moves | Role |
|---|---|---|---|---|---|---|---|---|
| Lead | Steelix | 48 | Solid Rock | Occa Berry | Brave | 43 | Stealth Rock, Iron Head, Earthquake, Ice Fang | rocks on turn one (89 to 117 fights of 150); the Occa Berry blunts the Fire moves a player carries for Byron |
| 2 | Mienshao | 48 | Regenerator | Shell Bell | Hasty | 132 | Fake Out, Drain Punch, U-turn, Poison Jab | fast pivot; Poison Jab for the Fairy answers |
| 3 | Hawlucha | 48 | Unburden | Sitrus Berry | Naive | 146 | Bulk Up, High Jump Kick, Dual Wingbeat, Stone Edge | the Sitrus Berry's use doubles its Speed (eaten in 50 to 112 fights) |
| 4 | Poliwrath | 49 | Water Absorb | Leftovers | Lax | 108 | Bulk Up, Waterfall, Ice Punch, Circle Throw | the Water and Ground answers' trap; Circle Throw drags out a boosted Pokemon |
| 5 | Kommo-o | 50 | Bulletproof | Roseli Berry | Serious | 105 | Dragon Dance, Outrage, Sky Uppercut, Poison Jab | the setup sweeper; the Roseli Berry takes the edge off its four-times Fairy weakness |
| Ace | Lucario | 51 | Adaptability | Wise Glasses | Mild | 112 | Calm Mind, Aura Sphere, Flash Cannon, Dark Pulse | aura moves on doubled STAB |

The first draft's Knock Off on Mienshao and Encore on Hawlucha were never or once picked, so they became Poison Jab and Stone Edge; every move is now picked.

On Byron's boxes the player wins 104 and 94, 127 and 103, 103 and 124 of 150, against Byron's 41 to 86, so Riley reads easier than the leader. Knockouts per run: Lucario 128 to 200, Kommo-o 92 to 180, the rest 31 to 131. The lead test: Palossand (box 1, 20 sixes) draws Poliwrath, which beats it with Bulk Up; Araquanid, Hippowdon and Octillery (box 3) draw Hawlucha, Poliwrath or Kommo-o, which beat them; Mantine (box 2, 20 sixes) and Bronzong draw Hawlucha, which loses narrowly (+0.5 and +1.5).

## The tag battle on B2F

Riley's partner team, in his own file, is four of the same six with the same items and natures, and moves for a double that never touch the player's side:

| Member | Level | Ability | Item | Nature | Moves |
|---|---|---|---|---|---|
| Mienshao | 48 | Regenerator | Shell Bell | Hasty | Fake Out, Drain Punch, U-turn, Stone Edge |
| Hawlucha | 48 | Unburden | Sitrus Berry | Naive | Tailwind, Rock Slide, High Jump Kick, Dual Wingbeat |
| Poliwrath | 49 | Water Absorb | Leftovers | Lax | Helping Hand, Icy Wind, Waterfall, Drain Punch |
| Lucario | 51 | Adaptability | Wise Glasses | Mild | Aura Sphere, Flash Cannon, Dark Pulse, Vacuum Wave |

The two grunts kept the base ROM's Yanmega and Kecleon and grew into two ideas that work as a pair. Their aces are 50 and 51, two and three under the cap, the rest 48 and 49. Each holds its own item and nature.

| Grunt | Member | Level | Ability | Item | Nature | Speed | Moves |
|---|---|---|---|---|---|---|---|
| 1, the wind | Talonflame | 48 | Gale Wings | Charti Berry | Hasty | 154 | Tailwind, Acrobatics, Flame Charge, Will-O-Wisp |
| | Mandibuzz | 48 | Overcoat | Rocky Helmet | Relaxed | 86 | Foul Play, Knock Off, Snarl, Taunt |
| | Pidgeot | 49 | Intimidate | Sharp Beak | Quirky | 119 | Heat Wave, Air Slash, U-turn, Feather Dance |
| | Yanmega (ace) | 50 | Speed Boost | Wise Glasses | Rash | 115 | Air Cutter, Signal Beam, Ancient Power, Giga Drain |
| 2, the thieves | Sableye | 48 | Prankster | Sitrus Berry | Careful | 67 | Fake Out, Knock Off, Will-O-Wisp, Recover |
| | Crawdaunt | 48 | Adaptability | Scope Lens | Brave | 64 | Crabhammer, Knock Off, Ceaseless Edge, Swords Dance |
| | Incineroar | 49 | Intimidate | Shuca Berry | Naughty | 78 | Fake Out, Darkest Lariat, Flare Blitz, Parting Shot |
| | Kecleon (ace) | 51 | Protean | Iron Ball | Impish | 30 | Trick, Knock Off, Sucker Punch, Drain Punch |

How the sides weigh. Veilstone was twelve against ten (the partner's six and the player's six against five and five), every member within two levels. Here it is ten against eight: the player's six and Riley's four against four and four, Riley's levels the grunts' own. Talonflame's Gale Wings Tailwind and Pidgeot's Intimidate open for the thieves; Sableye's and Incineroar's Fake Outs, three Knock Offs and Kecleon's Trick strip the items of the player and Riley alike (the AI's Expert routine scores Trick +5 when its user holds an Iron Ball). The player's side answers with Rock Slide and Icy Wind into four flyers, Riley's Fake Out and Tailwind, and the Fighting moves the thieves fear. Read as singles the grunts are weak (the player wins 126 to 150 of 150), which is expected of four-member halves of a double and says nothing about the pair.

Riley's partner also fights beside the player against B2F's four pairs (three and three, or Jonah and Brenda's four and four), which now face four of his Pokemon where they faced three.

## What changed in the tree

| File | Change |
|---|---|
| `rival_canalave_city_turtwig`, `_chimchar`, `_piplup` | Barry 5's six as above |
| `dummy_087` | free slot 87 becomes Riley's door battle: name Riley, class `TRAINER_CLASS_TRAINER_RILEY`, no messages (as his own file had), the six above |
| `riley_iron_island` | Riley's partner four |
| `galactic_grunt_iron_island_1`, `_2` | the wind and the thieves; since Ian's answer, Officers Boreas and Laverna |
| `scripts_iron_island.s` | the door battle fights `TRAINER_DUMMY_087` in place of trainer 609 |
| `bulk_scripts.py` | the second reason for `scripts_iron_island`'s divergence |
| `trainers_diverged.json` | the seven files, with slot 87's name, class and messages |
| `snivy/data.json`, `learnrewrite.IAN_EGG_MOVES` | Leaf Storm on Snivy's egg list |
| `test_b1.py` | Barry 5 leaves `AWAITING_REDESIGN`, now empty |

Checked: both legality checkers (the OxiDex's own lists and the Kaizo study's checker with the pre-TM-pass TMs) give every move of the seven teams at its level; the trainer lint finds nothing and the packer packs every file; test_b1 49 of 49, test_trainers 44 of 44, test_learnrewrite 6 of 6, test_learncheck 18 of 18; `make rom` builds.

## How the numbers were made

The scripts are the Byron and Brains check's, copied to `/home/ian/.claude/jobs/barry5-riley/checks/` and pointed at this worktree; none writes to `res/`. `bc.py` gains Riley's slot and the two grunts as fights read alone, and a candidate that changes a species in all three Barry files at once. `checks.py FIGHT PLACE SEED` runs the screen's top 20 sixes, the catches that beat each member, the replacement trace, damage both ways and the probe (150 rough fights against the best six and the most-taken six with a greedy player; its wins mean nothing alone). `bait.py` gives the lead test and `summarise.py` the headline numbers. The boxes come from `plgoal3.setup` with the run name `barry5-riley-study`, seeds 1 to 3: Barry 5's own at 50 for Barry 5, Byron's at 53 for Riley and the grunts, Barry 4's at 42 and Byron's at 53 for scale. The drafts were written from `/home/ian/.claude/jobs/barry5-riley/write/teams.py` through `trainers.save`, after `legal_mem.py` had checked them against both checkers.

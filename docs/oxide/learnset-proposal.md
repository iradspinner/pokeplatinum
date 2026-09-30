# The learnset proposal

Written by `learnplan.py full` (2026-09-27) for the Overseer to read before Ian. It proposes level-up lists for all 653 species; nothing here is in the game data. `docs/oxide/learnset-proposal.tsv` has every entry, now and proposed, with the reason for each change, and `learnplan.py line <species>` prints one line in full, with its delays and check list.

## The rules it applies

It starts from Oxide's lists as they are and changes an entry only where one of Ian's rules asks for it:

- Kaizo's placements count per species, translated by split: a Kaizo level goes to the same point of the same split in Oxide, so nothing lands past 78. An entry counts only where Kaizo's move is Oxide's at like values, and one that lands below the level the player can have the stage at (its evolution level, or a first stage's earliest catch, gift or hatch) means unavailable, not early.
- A species Kaizo lacks takes its placements from the Kaizo species nearest it in power at the same stage of their lines, under the same test of where the player can have it.
- A move's worth is what the Pokemon knows at capture plus what it learns by level-up after (the capture rule); a move's downsides count against it (lock-in, Uproar the worst, a recharge turn, heavy recoil and self-drops).
- A weak attack never moves later than now, and none is added.
- Status moves follow Ian's tier list (`docs/oxide/status-move-tiers.md`): S and SSS are strong, never earlier than now and added only where Kaizo gives the species the move; the instant-death moves and the hazards other than Toxic Spikes and Sticky Web are unrated.
- The power flags (base Speed over 100, or base Attack or Special Attack over 100 with a move of 100 or more of that kind the stage can have) run over the splits before Byron's: before Maylene's the line is brought to Ian by name, in Maylene's a very close look, in Wake's a close look.
- The power bar (Ian's Talonflame test, thresholds provisional): a stage at the split's cap with the moves it can have that outspeeds more than half the split's trainer Pokemon and knocks out more than a quarter in one hit.
- A flagged stage, or one over the bar, gets no strong move earlier than now on its own list and no new coverage ahead of its first good move of that type. The same holds for what a pre-evolution learns within four levels of the strong stage's evolution, since that comes along with no real wait. A pre-evolution kept back five levels or more may still reach a move sooner; that route is a delay, and it stays.
- A stage is judged strong on Oxide's lists now and again on the proposal's: one that the proposal's own moves would flag or put over the bar is proposed again as held.
- A delay counts only when waiting is a real choice: a strong move learnt past the level the stage could evolve at, that the evolved stage gets a split and five levels later or never, with no same-type move within a tenth of it between.
- No two moves on one level: a moved or added entry that shares a level goes to the nearest free level in the same split, within the other rules.
- The dead-weight rule, the move pool's first cut and the weather ruling remove entries; nothing that ends a wild encounter moves into the levels the species is met wild at.
- A strong move placed from Kaizo is never earlier than Kaizo's own level (Ian, 2026-09-27), or, where Kaizo lacks the species, its nearest lines' level, but never past the end of the Oxide split that level translates to (Houndoom's Dark Pulse, Kaizo's 70, no earlier than 56, the end of Candice's split); where that level is past 78 the translated place stays, listed below for Ian.
- No stage the player can have goes more than one split without an attack of its own type of 50 or more by effective power (Ian, 2026-09-27), counting what it brings from a pre-evolution evolved on time; a stage the player can evolve by the end of Gardenia's split is exempt, since only a player who keeps it back meets the gap. Where the proposal would break the rule, the nearest such move stays at its current level, or goes to Ian when it would reach a stage the flags or the bar hold.
- Fletchling keeps Will-O-Wisp at 25.

## What it changes

It changes the lists of 532 of the 653 species. The 187 that no source gives the player, by the League or after it (Groudon, Xerneas and the like), keep their lists but for the drops: those lists only feed trainers' default moves, which the trainer pass sets.

| Entries | Count |
|---|---|
| Kept where they are | 7575 |
| Moved | 678 |
| Added | 256 |
| Dropped | 534 |

The reasons given for the moves and additions (an entry moved twice, by Kaizo and then by the one-level rule, counts under both):

| Change | Reason | Count |
|---|---|---|
| Moved | Kaizo's own list for the species, translated by split | 129 |
| Moved | Kaizo's nearest lines, translated by split | 113 |
| Added | a move in the last splits (Ian, 2026-09-28) | 109 |
| Added | Kaizo's own list for the species, translated by split | 87 |
| Moved | the one-level rule | 55 |
| Moved | 1 to 0: the donor's evolution move, learned on evolving (Ian, 2026-09-30) | 45 |
| Moved | an exclusive delay from Kaizo | 31 |
| Added | a first stage keeps its first attack | 30 |
| Added | the one-level rule | 29 |
| Moved | a move in the last splits (Ian, 2026-09-28) | 25 |
| Added | a key move after an evolution without a level (Ian, 2026-09-28) | 23 |
| Added | an exclusive delay from Kaizo | 8 |
| Moved | a key move after an evolution without a level (Ian, 2026-09-28) | 7 |
| Added | the move-pool survey's first move | 4 |
| Moved | the move-pool survey's first move | 3 |
| Added | an evolution move, for Ian (2026-09-28) | 2 |
| Added | new at 30: Ian's list for it by name | 1 |
| Moved | new at 45: Ian's list for it by name | 1 |
| Moved | new at 48: Ian's list for it by name; moved from 65 | 1 |
| Moved | an evolution move, for Ian (2026-09-28) | 1 |
| Added | new at 32: Ian's list for it by name | 1 |

Why entries left:

| Reason | Count |
|---|---|
| Strength 20, under 40 | 68 |
| Weather, for a species the player can own | 64 |
| Strength 30, under 40 | 61 |
| Strength 35, under 40 | 60 |
| The move pool's first cut | 56 |
| Works only asleep, or returns less than double | 33 |
| Strength 27, under 40 | 32 |
| Charges a turn in the open (Kaizo's lists keep no such move) | 22 |
| Strength 38, under 40 | 22 |
| Strength 14, under 40 | 22 |
| Strength 40, at most half of Gardenia's usual 80 | 16 |
| Strength 10, under 40 | 14 |
| Strength 13, under 40 | 13 |
| 80% accurate on 80 power | 9 |
| Strength 45, at most half of Fantina's usual 90 | 5 |
| Strength 40, at most half of Fantina's usual 80 | 5 |
| Strength 50, at most half of Byron's usual 100 | 4 |
| 85% accurate on 80 power | 4 |
| 85% accurate on 18 power | 4 |
| 85% accurate on 65 power | 2 |
| Strength 40, at most half of Fantina's usual 90 | 2 |
| Strength 40, at most half of Maylene's usual 92 | 2 |
| Moved to 53 it comes after a stronger move of its type the stage has, and its Kaizo floor (53) is past its old level (36) | 2 |
| Strength 48, at most half of Wake's usual 95 | 2 |
| Moved to 56 it comes after a stronger move of its type the stage has, and its Kaizo floor (56) is past its old level (52) | 1 |
| Moved to 38 it comes after a stronger move of its type the stage has, and its Kaizo floor (39) is past its old level (12) | 1 |
| Moved to 43 it comes after a stronger move of its type the stage has, and its Kaizo floor (44) is past its old level (30) | 1 |
| Moved to 56 it comes after a stronger move of its type the stage has, and its Kaizo floor (56) is past its old level (14) | 1 |
| Moved to 59 it comes after a stronger move of its type the stage has, and its Kaizo floor (60) is past its old level (32) | 1 |
| Moved to 52 it comes after a stronger move of its type the stage has, and its Kaizo floor (53) is past its old level (22) | 1 |
| Moved to 44 it comes after a stronger move of its type the stage has, and its Kaizo floor (44) is past its old level (34) | 1 |
| Strength 40, at most half of Maylene's usual 90 | 1 |
| Strength 45, at most half of Wake's usual 95 | 1 |
| Moved to 53 it comes after a stronger move of its type the stage has, and its Kaizo floor (53) is past its old level (34) | 1 |

## The power flags

89 stages trip a flag before Byron's split. Each is held to no strong move earlier than now on its own list; the last column is what the proposal does to its strong moves, the earliest each can be known by any route, a pre-evolution kept back included.

| Stage | Split | Look | Why | Strong moves, now and proposed |
|---|---|---|---|---|
| Kadabra | Roark | brought to Ian by name | base Speed 105 | Recover 30 to 39 |
| Delcatty | Gardenia | brought to Ian by name | base Speed 112 | Hyper Voice 35 to never; Play Rough never to 66 |
| Donphan | Gardenia | brought to Ian by name | base Attack 120 with Slam (100) | Fire Fang never to 69 |
| Emolga | Gardenia | brought to Ian by name | base Speed 103 | as now |
| Floatzel | Gardenia | brought to Ian by name | base Speed 115 | Ice Punch never to 66 |
| Galarian Rapidash | Gardenia | brought to Ian by name | base Speed 110 | Megahorn never to 72 |
| Liepard | Gardenia | brought to Ian by name | base Speed 116 | as now |
| Lopunny | Gardenia | brought to Ian by name | base Speed 105 | Play Rough never to 69 |
| Minun | Gardenia | brought to Ian by name | base Speed 105 | Hyper Voice never to 61; Thunderbolt never to 43 |
| Steelix | Gardenia | brought to Ian by name | base Attack 115 with Slam (100) | Earthquake never to 76 |
| Ambipom | Fantina | brought to Ian by name | base Speed 115 | as now |
| Cranidos | Fantina | brought to Ian by name | base Attack 125 with Earthquake (100) | as now |
| Feraligatr | Fantina | brought to Ian by name | base Attack 125 with Earthquake (100) | Dive never to 30; Ice Fang 30 to 33; Superpower 43 to 39 |
| Galvantula | Fantina | brought to Ian by name | base Speed 108 | Bug Buzz 48 to 39; Discharge 30 to 38; Energy Ball 37 to 44; Signal Beam 34 to 35; Thunderbolt 45 to 41 |
| Granbull | Fantina | brought to Ian by name | base Attack 120 with Earthquake (100) | Earthquake never to 62 |
| Hariyama | Fantina | brought to Ian by name | base Attack 120 with Earthquake (100) | Close Combat 40 to 44; Shadow Punch never to 53 |
| Haunter | Fantina | brought to Ian by name | base Speed 110 | Shadow Punch 25 to 38 |
| Heracross | Fantina | brought to Ian by name | base Attack 125 with Earthquake (100) | Brick Break 19 to 26 |
| Houndoom | Fantina | brought to Ian by name | base Speed 105 | Dark Pulse never to 56; Will-O-Wisp never to 72 |
| Jumpluff | Fantina | brought to Ian by name | base Speed 110 | Seed Bomb never to 32 |
| Mismagius | Fantina | brought to Ian by name | base Speed 105 | as now |
| Nidoking | Fantina | brought to Ian by name | base Attack 102 with Earthquake (100) | Earth Power 43 to never; Earthquake never to 53; Sludge Wave never to 73 |
| Piloswine | Fantina | brought to Ian by name | base Attack 110 with Earthquake (100) | as now |
| Rampardos | Fantina | brought to Ian by name | base Attack 180 with Earthquake (100) | as now |
| Salazzle | Fantina | brought to Ian by name | base Speed 117 | Flamethrower 34 to 38; Sludge Bomb 40 to 39 |
| Sharpedo | Fantina | brought to Ian by name | base Attack 120 with Earthquake (100) | Ice Fang 30 to 53; Liquidation never to 63 |
| Sudowoodo | Fantina | brought to Ian by name | base Attack 110 with Earthquake (100) | Wood Hammer never to 62 |
| Torterra | Fantina | brought to Ian by name | base Attack 111 with Earthquake (100) | Wood Hammer never to 73 |
| Toucannon | Fantina | brought to Ian by name | base Attack 120 with Beak Blast (120) | Hyper Voice 37 to 39 |
| Ampharos | Maylene | very close look | base Special Attack 115 with Focus Blast (120) | Body Slam never to 30; Discharge 30 to 33; Thunderbolt never to 39 |
| Blastoise | Maylene | very close look | base Special Attack 110 with Focus Blast (120) | Ice Beam never to 73 |
| Blaziken | Maylene | very close look | base Attack 120 with Earthquake (100) | Brave Bird 49 to never |
| Castform | Maylene | very close look | base Special Attack 120 with Thunder (110) | Hurricane never to 69 |
| Charizard | Maylene | very close look | base Special Attack 110 with Focus Blast (120) | as now |
| Chatot | Maylene | very close look | base Speed 110 | Air Slash never to 63 |
| Cinderace | Maylene | very close look | base Speed 119 | Double-Edge 39 to 44 |
| Crawdaunt | Maylene | very close look | base Attack 120 with Crabhammer (100) | as now |
| Delphox | Maylene | very close look | base Speed 104 | as now |
| Electabuzz | Maylene | very close look | base Speed 105 | Thunderbolt 37 to 39 |
| Electivire | Maylene | very close look | base Speed 105 | Thunderbolt 37 to 39 |
| Empoleon | Maylene | very close look | base Attack 111 with Earthquake (100) | Earthquake never to 73 |
| Gardevoir | Maylene | very close look | base Special Attack 135 with Focus Blast (120) | Fire Punch never to 30; Moonblast never to 72; Psychic 30 to 38; Thunderbolt never to 33; Zen Headbutt never to 31 |
| Girafarig | Maylene | very close look | base Special Attack 110 with Thunder (110) | Earthquake never to 71 |
| Glaceon | Maylene | very close look | base Special Attack 130 with Blizzard (110) | as now |
| Gorebyss | Maylene | very close look | base Special Attack 114 with Blizzard (110) | Ice Beam never to 65 |
| Greninja | Maylene | very close look | base Speed 122 | Waterfall 36 to 39 |
| Hippowdon | Maylene | very close look | base Attack 112 with Earthquake (100) | Ice Fang never to 71 |
| Jolteon | Maylene | very close look | base Speed 130 | as now |
| Jynx | Maylene | very close look | base Special Attack 115 with Focus Blast (120) | as now |
| Kingler | Maylene | very close look | base Attack 130 with Slam (100) | Superpower never to 68 |
| Krabby | Maylene | very close look | base Attack 105 with Slam (100) | as now |
| Magcargo | Maylene | very close look | base Special Attack 109 with Fire Blast (110) | as now |
| Magmortar | Maylene | very close look | base Special Attack 125 with Focus Blast (120) | as now |
| Meowscarada | Maylene | very close look | base Speed 123 | as now |
| Mienshao | Maylene | very close look | base Speed 105 | Aura Sphere 38 to 44 |
| Ninetales | Maylene | very close look | base Special Attack 109 with Fire Blast (110) | as now |
| Octillery | Maylene | very close look | base Special Attack 108 with Fire Blast (110) | Gunk Shot never to 71 |
| Pawmot | Maylene | very close look | base Speed 105 | Close Combat 49 to 56 |
| Primeape | Maylene | very close look | base Attack 115 with Earthquake (100) | as now |
| Purugly | Maylene | very close look | base Speed 112 | as now |
| Raichu | Maylene | very close look | base Speed 110 | ThunderPunch never to 66 |
| Rotom | Maylene | very close look | base Special Attack 105 with Thunder (110) | as now |
| Sceptile | Maylene | very close look | base Speed 120 | Leaf Blade 36 to 52 |
| Scyther | Maylene | very close look | base Speed 105 | X-Scissor 41 to 52 |
| Serperior | Maylene | very close look | base Speed 113 | as now |
| Sneasel | Maylene | very close look | base Speed 115 | as now |
| Snorlax | Maylene | very close look | base Attack 110 with Earthquake (100) | Earthquake never to 75 |
| Staraptor | Maylene | very close look | base Speed 105 | Brave Bird 37 to 44; Close Combat 34 to 53 |
| Starmie | Maylene | very close look | base Speed 115 | Psychic never to 75; Recover 34 to 44 |
| Swampert | Maylene | very close look | base Attack 110 with Earthquake (100) | as now |
| Talonflame | Maylene | very close look | base Speed 126 | Brave Bird 55 to 65; Flare Blitz 51 to 64 |
| Tangrowth | Maylene | very close look | base Special Attack 110 with Focus Blast (120) | Energy Ball never to 73 |
| Toxicroak | Maylene | very close look | base Attack 106 with Earthquake (100) | Gunk Shot never to 65 |
| Vaporeon | Maylene | very close look | base Special Attack 110 with Blizzard (110) | as now |
| Absol | Wake | close look | base Special Attack 115 with Thunder (110) | Night Slash 52 to never |
| Alakazam | Wake | close look | base Speed 120 | as now |
| Cinccino | Wake | close look | base Speed 115 | as now |
| Crobat | Wake | close look | base Speed 130 | Brave Bird never to 53 |
| Gengar | Wake | close look | base Speed 110 | Sludge Bomb never to 68 |
| Golem | Wake | close look | base Attack 130 with Double-Edge (120) | as now |
| Grapploct | Wake | close look | base Attack 118 with Superpower (120) | Superpower 45 to 41 |
| Kleavor | Wake | close look | base Attack 135 with Superpower (120) | Skitter Smack 22 to never; Superpower 40 to 43 |
| Machamp | Wake | close look | base Attack 130 with Earthquake (100) | as now |
| Mamoswine | Wake | close look | base Attack 135 with Earthquake (100) | Icicle Spear never to 76 |
| Rapidash | Wake | close look | base Speed 110 | as now |
| Rhydon | Wake | close look | base Attack 130 with Earthquake (100) | Earthquake 49 to 53 |
| Togekiss | Wake | close look | base Special Attack 120 with Fire Blast (110) | Moonblast never to 75 |
| Vespiquen | Wake | close look | base Attack 102 with Attack Order (120) | Attack Order 37 to 40; Bug Buzz never to 76 |
| Wailord | Wake | close look | base Attack 110 with Earthquake (100) | Water Spout 40 to 78 |

## The power bar

194 stages with no flag pass the bar before Byron's split on Oxide's lists now, and are held the same way. The thresholds are provisional; Ian's Talonflame at 39 outsped 92 of Maylene's 93 trainer Pokemon and knocked out 38 in one hit, well over both.

| Stage | Split | Outsped | Knocked out in one hit |
|---|---|---|---|
| Barboach | Roark | 93% | 36% |
| Beautifly | Roark | 98% | 61% |
| Bibarel | Roark | 100% | 48% |
| Braixen | Roark | 100% | 48% |
| Buizel | Roark | 100% | 36% |
| Buneary | Roark | 100% | 75% |
| Charmander | Roark | 98% | 86% |
| Charmeleon | Roark | 100% | 89% |
| Corphish | Roark | 77% | 43% |
| Corsola | Roark | 77% | 36% |
| Corvisquire | Roark | 100% | 50% |
| Dottler | Roark | 68% | 32% |
| Dustox | Roark | 98% | 41% |
| Fennekin | Roark | 93% | 32% |
| Fletchinder | Roark | 100% | 55% |
| Fletchling | Roark | 96% | 39% |
| Froakie | Roark | 100% | 57% |
| Frogadier | Roark | 100% | 73% |
| Furret | Roark | 100% | 48% |
| Gligar | Roark | 100% | 32% |
| Grubbin | Roark | 91% | 34% |
| Houndour | Roark | 98% | 30% |
| Kricketune | Roark | 100% | 59% |
| Luvdisc | Roark | 100% | 32% |
| Luxio | Roark | 93% | 64% |
| Machop | Roark | 77% | 39% |
| Magby | Roark | 100% | 32% |
| Marshtomp | Roark | 91% | 41% |
| Murkrow | Roark | 100% | 64% |
| Nidoran M | Roark | 91% | 30% |
| Nidorina | Roark | 91% | 27% |
| Nidorino | Roark | 98% | 34% |
| Nosepass | Roark | 68% | 46% |
| Onix | Roark | 100% | 50% |
| Pachirisu | Roark | 100% | 66% |
| Phanpy | Roark | 84% | 34% |
| Pikipek | Roark | 98% | 55% |
| Ponyta | Roark | 100% | 50% |
| Poochyena | Roark | 77% | 34% |
| Prinplup | Roark | 91% | 43% |
| Psyduck | Roark | 91% | 27% |
| Raboot | Roark | 100% | 39% |
| Remoraid | Roark | 98% | 59% |
| Rookidee | Roark | 91% | 36% |
| Scorbunny | Roark | 100% | 27% |
| Sewaddle | Roark | 84% | 36% |
| Shinx | Roark | 89% | 64% |
| Squirtle | Roark | 89% | 27% |
| Staravia | Roark | 100% | 55% |
| Starly | Roark | 93% | 41% |
| Surskit | Roark | 98% | 50% |
| Trumbeak | Roark | 100% | 64% |
| Turtwig | Roark | 68% | 27% |
| Vullaby | Roark | 93% | 41% |
| Vulpix | Roark | 98% | 39% |
| Wartortle | Roark | 91% | 41% |
| Wingull | Roark | 100% | 46% |
| Aipom | Gardenia | 96% | 49% |
| Alolan Ninetales | Gardenia | 100% | 67% |
| Araquanid | Gardenia | 75% | 63% |
| Azumarill | Gardenia | 81% | 40% |
| Bidoof | Gardenia | 55% | 28% |
| Breloom | Gardenia | 89% | 85% |
| Brionne | Gardenia | 81% | 44% |
| Budew | Gardenia | 85% | 28% |
| Carbink | Gardenia | 81% | 33% |
| Carvanha | Gardenia | 89% | 80% |
| Charjabug | Gardenia | 63% | 64% |
| Cherrim | Gardenia | 96% | 60% |
| Cherubi | Gardenia | 63% | 32% |
| Chimecho | Gardenia | 92% | 64% |
| Chinchou | Gardenia | 89% | 29% |
| Chingling | Gardenia | 77% | 37% |
| Clefable | Gardenia | 89% | 33% |
| Combee | Gardenia | 89% | 35% |
| Combusken | Gardenia | 85% | 52% |
| Dartrix | Gardenia | 83% | 64% |
| Dolliv | Gardenia | 61% | 31% |
| Dubwool | Gardenia | 97% | 73% |
| Dwebble | Gardenia | 85% | 65% |
| Finneon | Gardenia | 89% | 25% |
| Flaaffy | Gardenia | 77% | 27% |
| Glimmet | Gardenia | 88% | 64% |
| Golbat | Gardenia | 99% | 60% |
| Goldeen | Gardenia | 89% | 27% |
| Graveler | Gardenia | 77% | 56% |
| Grotle | Gardenia | 63% | 49% |
| Grovyle | Gardenia | 99% | 55% |
| Hoothoot | Gardenia | 81% | 33% |
| Hoppip | Gardenia | 81% | 27% |
| Huntail | Gardenia | 83% | 76% |
| Litten | Gardenia | 89% | 64% |
| Lombre | Gardenia | 81% | 43% |
| Lotad | Gardenia | 52% | 32% |
| Mantyke | Gardenia | 81% | 33% |
| Marill | Gardenia | 72% | 28% |
| Masquerain | Gardenia | 88% | 55% |
| Meditite | Gardenia | 88% | 45% |
| Mienfoo | Gardenia | 89% | 71% |
| Mightyena | Gardenia | 89% | 56% |
| Mothim | Gardenia | 93% | 67% |
| Mudkip | Gardenia | 72% | 32% |
| Naclstack | Gardenia | 63% | 33% |
| Nidoqueen | Gardenia | 93% | 60% |
| Noctowl | Gardenia | 89% | 85% |
| Nuzleaf | Gardenia | 88% | 52% |
| Pawmi | Gardenia | 88% | 29% |
| Pawmo | Gardenia | 96% | 48% |
| Pelipper | Gardenia | 100% | 64% |
| Pikachu | Gardenia | 99% | 43% |
| Piplup | Gardenia | 72% | 41% |
| Plusle | Gardenia | 85% | 28% |
| Poliwag | Gardenia | 99% | 27% |
| Poliwhirl | Gardenia | 99% | 31% |
| Popplio | Gardenia | 72% | 33% |
| Purrloin | Gardenia | 89% | 25% |
| Quagsire | Gardenia | 63% | 63% |
| Rowlet | Gardenia | 75% | 55% |
| Seedot | Gardenia | 52% | 28% |
| Servine | Gardenia | 93% | 32% |
| Shellos | Gardenia | 61% | 31% |
| Shiftry | Gardenia | 93% | 64% |
| Shroomish | Gardenia | 63% | 29% |
| Skiploom | Gardenia | 93% | 32% |
| Snivy | Gardenia | 89% | 27% |
| Snorunt | Gardenia | 81% | 48% |
| Snover | Gardenia | 72% | 69% |
| Snubbull | Gardenia | 52% | 27% |
| Steenee | Gardenia | 89% | 25% |
| Swadloon | Gardenia | 75% | 41% |
| Swinub | Gardenia | 81% | 40% |
| Tentacool | Gardenia | 89% | 32% |
| Torchic | Gardenia | 77% | 36% |
| Torracat | Gardenia | 99% | 76% |
| Treecko | Gardenia | 89% | 41% |
| Tropius | Gardenia | 83% | 67% |
| Wooloo | Gardenia | 77% | 27% |
| Wormadam | Gardenia | 63% | 63% |
| Zubat | Gardenia | 85% | 40% |
| Carnivine | Fantina | 70% | 44% |
| Ceruledge | Fantina | 82% | 45% |
| Drifblim | Fantina | 99% | 28% |
| Frosmoth | Fantina | 63% | 50% |
| Gabite | Fantina | 82% | 61% |
| Gastly | Fantina | 79% | 42% |
| Golduck | Fantina | 82% | 45% |
| Honchkrow | Fantina | 84% | 55% |
| Lanturn | Fantina | 68% | 41% |
| Leafeon | Fantina | 87% | 46% |
| Leavanny | Fantina | 84% | 28% |
| Lumineon | Fantina | 84% | 28% |
| Luxray | Fantina | 87% | 65% |
| Magmar | Fantina | 86% | 45% |
| Mantine | Fantina | 70% | 34% |
| Orbeetle | Fantina | 84% | 41% |
| Seaking | Fantina | 70% | 28% |
| Sinistcha | Fantina | 70% | 46% |
| Smoochum | Fantina | 63% | 30% |
| Tentacruel | Fantina | 92% | 50% |
| Tsareena | Fantina | 84% | 47% |
| Wailmer | Fantina | 55% | 38% |
| Whiscash | Fantina | 55% | 59% |
| Abra | Maylene | 84% | 48% |
| Altaria | Maylene | 68% | 48% |
| Decidueye | Maylene | 55% | 27% |
| Dewgong | Maylene | 55% | 43% |
| Elekid | Maylene | 89% | 32% |
| Glimmora | Maylene | 76% | 46% |
| Ludicolo | Maylene | 55% | 61% |
| Mankey | Maylene | 55% | 37% |
| Medicham | Maylene | 68% | 86% |
| Milotic | Maylene | 70% | 55% |
| Misdreavus | Maylene | 76% | 33% |
| Poliwrath | Maylene | 84% | 60% |
| Qwilfish | Maylene | 76% | 37% |
| Skuntank | Maylene | 75% | 47% |
| Staryu | Maylene | 76% | 29% |
| Vibrava | Maylene | 95% | 54% |
| Yanma | Maylene | 89% | 28% |
| Yanmega | Maylene | 89% | 53% |
| Chandelure | Wake | 68% | 44% |
| Corviknight | Wake | 51% | 36% |
| Drapion | Wake | 81% | 28% |
| Florges | Wake | 61% | 29% |
| Galarian Mr Mime | Wake | 83% | 34% |
| Glalie | Wake | 83% | 41% |
| Gliscor | Wake | 81% | 32% |
| Kingdra | Wake | 71% | 37% |
| Manaphy | Wake | 83% | 38% |
| Mr Mime | Wake | 77% | 52% |
| Mr Rime | Wake | 55% | 48% |
| Politoed | Wake | 77% | 43% |
| Roserade | Wake | 77% | 57% |
| Seadra | Wake | 71% | 37% |

A further 7 stages would trip a flag or pass the bar only with the moves a first proposal gave them, so they are proposed again as held: Clefairy, Dhelmise, Grapploct, Klefki, Polteageist, Primarina, Skitty.

## Strong moves that come sooner

Every good attack or S or SSS status move that the proposal gives a stage a split or more sooner than now, or new before Byron's split: 119 in all. These are the entries to read as a player would. A stage marked held is flagged or over the bar, so its entry here is a new move no earlier than its first good one of that type.

| Stage | Move | Now | Proposed | Held |
|---|---|---|---|---|
| Anorith | Rock Blast | 49 | 44 |  |
| Anorith | X-Scissor | 61 | 53 |  |
| Armaldo | X-Scissor | 73 | 57 |  |
| Azurill | Bounce | not learnt | 26 |  |
| Bastiodon | Iron Head | 52 | 44 |  |
| Bronzor | Iron Head | not learnt | 20 |  |
| Bronzor | Zen Headbutt | not learnt | 31 |  |
| Chandelure | Shadow Ball | 65 | 48 | yes |
| Cherrim | Leaf Blade | not learnt | 39 | yes |
| Chimecho | Recover | not learnt | 34 | yes |
| Clobbopus | Superpower | 45 | 41 |  |
| Clodsire | Sludge Bomb | not learnt | 39 |  |
| Clodsire | Earthquake | 48 | 44 |  |
| Cresselia | Psychic | 93 | 74 |  |
| Croconaw | Superpower | 51 | 44 |  |
| Dewpider | Hydro Pump | 45 | 32 |  |
| Duskull | Future Sight | 46 | 26 |  |
| Espeon | Psychic | 64 | 53 |  |
| Ferroseed | Seed Bomb | 47 | 32 |  |
| Ferroseed | Iron Head | 52 | 33 |  |
| Flaaffy | Thunderbolt | not learnt | 44 | yes |
| Flareon | Lava Plume | 78 | 65 |  |
| Gastrodon | Muddy Water | 41 | 39 |  |
| Gastrodon | Earthquake | not learnt | 44 |  |
| Giratina | Shadow Claw | 80 | 63 |  |
| Goomy | Dragon Pulse | 54 | 44 |  |
| Hakamo O | Close Combat | 60 | 56 |  |
| Hisuian Goodra | Power Whip | 61 | 56 |  |
| Hisuian Goodra | Outrage | 66 | 60 |  |
| Hisuian Sliggoo | Dragon Pulse | 35 | 31 |  |
| Hisuian Sliggoo | Iron Head | 49 | 33 |  |
| Hisuian Sliggoo | Muddy Water | 56 | 39 |  |
| Honchkrow | Assurance | not learnt | 32 | yes |
| Hoothoot | Hyper Voice | not learnt | 39 | yes |
| Hoppip | Seed Bomb | not learnt | 32 | yes |
| Incineroar | Flare Blitz | 55 | 53 |  |
| Jangmo O | Outrage | 49 | 31 |  |
| Jangmo O | Scale Shot | 45 | 32 |  |
| Jellicent | Scald | 55 | 53 |  |
| Joltik | Bug Buzz | 48 | 39 |  |
| Joltik | Thunderbolt | 45 | 41 |  |
| Kabuto | Muddy Water | not learnt | 32 |  |
| Koffing | Sludge Bomb | 42 | 26 |  |
| Kommo O | Close Combat | 65 | 53 |  |
| Larvesta | Double-Edge | 72 | 39 |  |
| Larvitar | Earthquake | 41 | 39 |  |
| Lickilicky | Sludge Bomb | not learnt | 39 |  |
| Lickilicky | Power Whip | 49 | 44 |  |
| Lickitung | Body Slam | not learnt | 30 |  |
| Lickitung | Power Whip | 49 | 44 |  |
| Lunatone | Psychic | 45 | 39 |  |
| Magneton | Discharge | 40 | 39 |  |
| Magneton | Flash Cannon | not learnt | 44 |  |
| Magnezone | Flash Cannon | not learnt | 44 |  |
| Mareep | Body Slam | not learnt | 24 |  |
| Mareep | Thunderbolt | not learnt | 39 |  |
| Mawile | Thunder Fang | not learnt | 39 |  |
| Mawile | Ice Fang | not learnt | 44 |  |
| Meloetta | Psychic | 57 | 39 |  |
| Metang | Iron Head | not learnt | 31 |  |
| Metang | Zen Headbutt | 52 | 33 |  |
| Minun | Thunderbolt | not learnt | 43 | yes |
| Murkrow | Dark Pulse | not learnt | 44 | yes |
| Nacli | Stone Edge | 45 | 32 |  |
| Nidoking | Poison Jab | not learnt | 43 | yes |
| Nidoran F | Toxic | not learnt | 32 |  |
| Nidoran F | Earth Power | not learnt | 34 |  |
| Noctowl | Hyper Voice | not learnt | 44 | yes |
| Omanyte | Earth Power | not learnt | 44 |  |
| Pachirisu | Thunder Fang | not learnt | 32 | yes |
| Plusle | Thunderbolt | not learnt | 43 | yes |
| Pupitar | Earthquake | 47 | 39 |  |
| Ralts | Fire Punch | not learnt | 26 |  |
| Ralts | Zen Headbutt | not learnt | 31 |  |
| Ralts | Thunderbolt | not learnt | 33 |  |
| Regirock | Rock Blast | not learnt | 32 |  |
| Registeel | Iron Head | 73 | 39 |  |
| Registeel | Hammer Arm | 81 | 53 |  |
| Relicanth | Dive | 57 | 39 |  |
| Rhyperior | Megahorn | 57 | 56 |  |
| Riolu | ThunderPunch | not learnt | 7 |  |
| Riolu | Ice Punch | not learnt | 30 |  |
| Salandit | Sludge Bomb | 40 | 39 |  |
| Sandygast | Earth Power | 47 | 32 |  |
| Sandygast | Shadow Ball | 43 | 39 |  |
| Scizor | Iron Head | 53 | 44 |  |
| Sealeo | Dive | not learnt | 38 |  |
| Seel | Ice Beam | 47 | 44 |  |
| Sentret | Hyper Voice | 47 | 33 |  |
| Shieldon | Earthquake | not learnt | 34 |  |
| Shieldon | Iron Head | 43 | 39 |  |
| Sinistea | Shadow Ball | 48 | 33 |  |
| Sliggoo | Dragon Pulse | 55 | 53 |  |
| Slowbro | Psychic | 54 | 44 |  |
| Slowking | Psychic | 48 | 44 |  |
| Slowpoke | Body Slam | not learnt | 26 |  |
| Slowpoke | Zen Headbutt | 34 | 30 |  |
| Slowpoke | Dive | not learnt | 33 |  |
| Slowpoke | Psychic | 48 | 44 |  |
| Solrock | Zen Headbutt | not learnt | 38 |  |
| Solrock | Earthquake | not learnt | 39 |  |
| Spheal | Bounce | not learnt | 20 |  |
| Spheal | Dive | not learnt | 33 |  |
| Spiritomb | Dark Pulse | 49 | 38 |  |
| Spiritomb | Earth Power | not learnt | 44 |  |
| Swablu | Air Slash | not learnt | 44 |  |
| Sylveon | Dazzling Gleam | not learnt | 32 |  |
| Tentacool | Toxic | not learnt | 39 | yes |
| Tentacruel | Toxic | not learnt | 44 | yes |
| Totodile | Dive | not learnt | 26 |  |
| Totodile | Superpower | 43 | 39 |  |
| Trapinch | Earthquake | 73 | 53 |  |
| Umbreon | Body Slam | not learnt | 30 |  |
| Umbreon | Assurance | 43 | 39 |  |
| Vikavolt | Signal Beam | 36 | 33 |  |
| Vikavolt | Discharge | 48 | 34 |  |
| Vikavolt | Bug Buzz | 55 | 53 |  |
| Wooper | Muddy Water | 47 | 30 |  |
| Wooper | Sludge Bomb | not learnt | 33 |  |

## Delays

278 delays pass Ian's tests on the proposed lists (a strong move past the evolution level, the evolved stage a split and five levels later or never, nothing like it between). The wait is given in splits past the one the stage can evolve in.

| Pre-evolution | Evolves to | Move | Learnt at | Wait in splits | Evolved stage |
|---|---|---|---|---|---|
| Anorith | Armaldo | Rock Blast | 44 | 0 | 55 |
| Aron | Lairon | Double-Edge | 43 | 2 | 51 |
| Azurill | Marill | Slam | 15 | 0 | 27 |
| Azurill | Marill | Bounce | 26 | 1 | never |
| Bagon | Shelgon | Dragon Claw | 50 | 3 | 55 |
| Bagon | Shelgon | Double-Edge | 55 | 4 | 61 |
| Baltoy | Claydol | Earth Power | 53 | 2 | 62 |
| Barboach | Whiscash | Earthquake | 39 | 1 | 45 |
| Barboach | Whiscash | Future Sight | 43 | 2 | 51 |
| Bayleef | Meganium | Body Slam | 40 | 2 | 46 |
| Bidoof | Bibarel | Superpower | 41 | 4 | 48 |
| Bronzor | Bronzong | Future Sight | 37 | 1 | 43 |
| Bulbasaur | Ivysaur | Seed Bomb | 37 | 3 | never |
| Carvanha | Sharpedo | Ice Fang | 53 | 3 | never |
| Charmeleon | Charizard | Flamethrower | 39 | 0 | 53 |
| Chikorita | Bayleef | Body Slam | 34 | 3 | 40 |
| Chimchar | Monferno | Nasty Plot | 23 | 1 | never |
| Chimchar | Monferno | Slack Off | 39 | 3 | 46 |
| Chimchar | Monferno | Flamethrower | 41 | 4 | 49 |
| Chinchou | Lanturn | Discharge | 38 | 1 | 53 |
| Chinchou | Lanturn | Hydro Pump | 42 | 2 | 52 |
| Clobbopus | Grapploct | Superpower | 41 | 2 | 72 |
| Combusken | Blaziken | Sky Uppercut | 50 | 2 | 59 |
| Combusken | Blaziken | Flare Blitz | 54 | 3 | 66 |
| Corphish | Crawdaunt | Crabhammer | 38 | 1 | 44 |
| Corphish | Crawdaunt | Swords Dance | 44 | 2 | 52 |
| Corvisquire | Corviknight | Roost | 55 | 2 | 65 |
| Cranidos | Rampardos | Head Smash | 43 | 2 | 52 |
| Croagunk | Toxicroak | Sludge Bomb | 43 | 1 | 49 |
| Croconaw | Feraligatr | Ice Fang | 38 | 1 | never |
| Croconaw | Feraligatr | Superpower | 44 | 2 | never |
| Croconaw | Feraligatr | Aqua Tail | 48 | 3 | 58 |
| Cubone | Marowak | Double-Edge | 43 | 2 | 53 |
| Cyndaquil | Quilava | Flamethrower | 37 | 3 | 42 |
| Cyndaquil | Quilava | Eruption | 49 | 5 | 57 |
| Dartrix | Decidueye | Brave Bird | 55 | 3 | never |
| Doduo | Dodrio | Drill Peck | 41 | 2 | 47 |
| Dottler | Orbeetle | Recover | 40 | 2 | never |
| Dottler | Orbeetle | Sticky Web | 48 | 3 | never |
| Drifloon | Drifblim | Shadow Ball | 38 | 1 | 44 |
| Drowzee | Hypno | Psychic | 40 | 3 | 50 |
| Drowzee | Hypno | Nasty Plot | 43 | 3 | 55 |
| Drowzee | Hypno | Future Sight | 53 | 4 | 69 |
| Eevee | Leafeon | Baton Pass | 36 | 1 | never |
| Eevee | Glaceon | Baton Pass | 36 | 1 | never |
| Eevee | Jolteon | Baton Pass | 36 | 0 | never |
| Eevee | Vaporeon | Baton Pass | 36 | 0 | never |
| Eevee | Flareon | Baton Pass | 36 | 0 | never |
| Eevee | Umbreon | Baton Pass | 36 | 2 | never |
| Eevee | Sylveon | Baton Pass | 36 | 1 | never |
| Eevee | Leafeon | Take Down | 43 | 2 | never |
| Eevee | Glaceon | Take Down | 43 | 2 | never |
| Eevee | Jolteon | Take Down | 43 | 1 | never |
| Eevee | Vaporeon | Take Down | 43 | 1 | never |
| Eevee | Flareon | Take Down | 43 | 1 | never |
| Eevee | Sylveon | Take Down | 43 | 2 | never |
| Ekans | Arbok | Gunk Shot | 41 | 3 | 56 |
| Elekid | Electabuzz | Thunderbolt | 39 | 1 | 53 |
| Exeggcute | Exeggutor | Psychic | 47 | 4 | never |
| Fennekin | Braixen | Will-O-Wisp | 40 | 4 | 72 |
| Fletchling | Fletchinder | Defog | 33 | 2 | never |
| Floette | Florges | Moonblast | 52 | 1 | 57 |
| Floragato | Meowscarada | Play Rough | 42 | 1 | 47 |
| Fomantis | Lurantis | Leaf Blade | 39 | 0 | never |
| Gabite | Garchomp | Dragon Rush | 70 | 5 | 78 |
| Gible | Gabite | Dig | 31 | 1 | 40 |
| Gible | Gabite | Dragon Rush | 60 | 6 | 70 |
| Golbat | Crobat | Brave Bird | 53 | 1 | 63 |
| Goldeen | Seaking | Megahorn | 51 | 3 | 63 |
| Goomy | Hisuian Sliggoo | Body Slam | 41 | 3 | never |
| Goomy | Sliggoo | Dragon Pulse | 44 | 0 | 53 |
| Goomy | Sliggoo | Muddy Water | 46 | 1 | 60 |
| Gothita | Gothorita | Future Sight | 37 | 1 | 42 |
| Grimer | Muk | Gunk Shot | 44 | 1 | 54 |
| Grotle | Torterra | Leaf Storm | 52 | 3 | 57 |
| Grovyle | Sceptile | Leaf Blade | 52 | 2 | 67 |
| Grovyle | Sceptile | Leaf Storm | 59 | 4 | 67 |
| Growlithe | Arcanine | Heat Wave | 45 | 2 | never |
| Growlithe | Arcanine | Flare Blitz | 48 | 2 | never |
| Grubbin | Charjabug | X-Scissor | 39 | 2 | 53 |
| Gulpin | Swalot | Sludge Bomb | 39 | 2 | 45 |
| Hippopotas | Hippowdon | Earthquake | 37 | 0 | 53 |
| Hippopotas | Hippowdon | Double-Edge | 44 | 1 | 50 |
| Hoothoot | Noctowl | Hyper Voice | 39 | 2 | 44 |
| Hoppip | Skiploom | Bullet Seed | 23 | 0 | 44 |
| Hoppip | Skiploom | Bounce | 40 | 3 | 48 |
| Horsea | Seadra | Hydro Pump | 35 | 1 | 40 |
| Horsea | Seadra | Dragon Dance | 38 | 1 | 48 |
| Horsea | Seadra | Dragon Pulse | 42 | 2 | 57 |
| Houndour | Houndoom | Crunch | 48 | 3 | 54 |
| Houndour | Houndoom | Nasty Plot | 53 | 3 | 60 |
| Jigglypuff | Wigglytuff | Body Slam | 29 | 1 | never |
| Jigglypuff | Wigglytuff | Hyper Voice | 45 | 4 | never |
| Jigglypuff | Wigglytuff | Double-Edge | 49 | 4 | never |
| Joltik | Galvantula | Discharge | 38 | 1 | 48 |
| Joltik | Galvantula | Bug Buzz | 39 | 1 | 51 |
| Joltik | Galvantula | Thunderbolt | 41 | 2 | 48 |
| Joltik | Galvantula | Energy Ball | 44 | 2 | 53 |
| Kirlia | Gardevoir | Psychic | 38 | 1 | 44 |
| Kirlia | Gardevoir | Future Sight | 39 | 1 | 45 |
| Koffing | Galarian Weezing | Sludge Bomb | 26 | 0 | 42 |
| Krabby | Kingler | Slam | 35 | 1 | 44 |
| Krabby | Kingler | Crabhammer | 41 | 2 | 56 |
| Lairon | Aggron | Double-Edge | 51 | 1 | 57 |
| Lampent | Chandelure | Heat Wave | 65 | 4 | 72 |
| Ledyba | Ledian | Double-Edge | 38 | 2 | 48 |
| Ledyba | Ledian | Bug Buzz | 41 | 3 | 53 |
| Lileep | Cradily | Energy Ball | 50 | 1 | 56 |
| Litten | Torracat | Fire Fang | 33 | 2 | 38 |
| Lotad | Lombre | Energy Ball | 45 | 5 | never |
| Loudred | Exploud | Hyper Voice | 57 | 3 | 63 |
| Luxio | Luxray | Thunder Fang | 33 | 0 | 53 |
| Makuhita | Hariyama | Close Combat | 44 | 3 | 72 |
| Makuhita | Hariyama | Shadow Punch | 53 | 4 | never |
| Mankey | Primeape | Close Combat | 49 | 3 | 59 |
| Mareep | Flaaffy | Body Slam | 24 | 1 | never |
| Mareep | Flaaffy | Thunderbolt | 39 | 3 | 44 |
| Marill | Azumarill | Aqua Tail | 37 | 2 | 47 |
| Marill | Azumarill | Hydro Pump | 42 | 3 | 47 |
| Marshtomp | Swampert | Earthquake | 46 | 2 | 56 |
| Meditite | Medicham | Recover | 46 | 2 | 55 |
| Meowth | Persian | Nasty Plot | 38 | 1 | 44 |
| Mienfoo | Mienshao | Hi Jump Kick | 58 | 4 | 64 |
| Minccino | Cinccino | Hyper Voice | 43 | 0 | 53 |
| Misdreavus | Mismagius | Shadow Ball | 37 | 1 | 56 |
| Monferno | Infernape | Slack Off | 46 | 2 | never |
| Monferno | Infernape | Flare Blitz | 49 | 2 | 57 |
| Murkrow | Honchkrow | Taunt | 31 | 0 | never |
| Nacli | Naclstack | Recover | 25 | 0 | 30 |
| Nacli | Naclstack | Stone Edge | 32 | 1 | 51 |
| Nacli | Naclstack | Earthquake | 40 | 3 | 53 |
| Natu | Xatu | Future Sight | 36 | 2 | 42 |
| Nidoran F | Nidorina | Toxic | 32 | 2 | never |
| Nidoran F | Nidorina | Earth Power | 34 | 3 | never |
| Nidoran F | Nidorina | Poison Fang | 45 | 5 | 58 |
| Nidoran M | Nidorino | Poison Jab | 37 | 3 | 43 |
| Nidorina | Nidoqueen | Toxic Spikes | 35 | 2 | never |
| Nidorina | Nidoqueen | Poison Fang | 58 | 6 | 73 |
| Nidorino | Nidoking | Toxic Spikes | 35 | 2 | never |
| Nincada | Ninjask | Dig | 45 | 4 | never |
| Nincada | Shedinja | Dig | 45 | 4 | never |
| Nosepass | Probopass | Earth Power | 79 |  | never |
| Numel | Camerupt | Flamethrower | 45 | 3 | 57 |
| Numel | Camerupt | Double-Edge | 51 | 3 | never |
| Oddish | Gloom | Giga Drain | 37 | 2 | 47 |
| Omanyte | Omastar | Earth Power | 44 | 0 | 55 |
| Omanyte | Omastar | Rock Blast | 46 | 1 | 56 |
| Omanyte | Omastar | Hydro Pump | 52 | 1 | 67 |
| Omanyte | Omastar | Ice Beam | 53 | 1 | 60 |
| Paras | Parasect | Giga Drain | 33 | 1 | 39 |
| Pawmo | Pawmot | Wild Charge | 40 | 1 | 57 |
| Phanpy | Donphan | Double-Edge | 42 | 3 | never |
| Pichu | Pikachu | Nasty Plot | 18 | 1 | never |
| Pidgeotto | Pidgeot | Air Slash | 57 | 4 | 62 |
| Pidgey | Pidgeotto | Roost | 37 | 2 | 42 |
| Pidgey | Pidgeotto | Tailwind | 41 | 3 | 47 |
| Pidgey | Pidgeotto | Air Slash | 49 | 4 | 57 |
| Pikipek | Trumbeak | Hyper Voice | 39 | 3 | 45 |
| Piloswine | Mamoswine | Earthquake | 53 | 1 | never |
| Piplup | Prinplup | Hydro Pump | 43 | 4 | 51 |
| Poliwag | Poliwhirl | Belly Drum | 31 | 1 | 37 |
| Poliwag | Poliwhirl | Hydro Pump | 38 | 2 | 48 |
| Poliwhirl | Poliwrath | Belly Drum | 37 | 0 | never |
| Poliwhirl | Poliwrath | Hydro Pump | 48 | 2 | never |
| Ponyta | Galarian Rapidash | Fire Blast | 37 | 2 | never |
| Ponyta | Rapidash | Bounce | 42 | 0 | 47 |
| Ponyta | Galarian Rapidash | Bounce | 42 | 3 | never |
| Ponyta | Rapidash | Flare Blitz | 46 | 1 | 56 |
| Ponyta | Galarian Rapidash | Flare Blitz | 46 | 4 | never |
| Poochyena | Mightyena | Taunt | 37 | 2 | 42 |
| Popplio | Brionne | Scald | 33 | 2 | 65 |
| Primeape | Annihilape | Close Combat | 59 | 2 | never |
| Psyduck | Golduck | Hydro Pump | 48 | 3 | 56 |
| Purrloin | Liepard | Nasty Plot | 36 | 2 | 44 |
| Purrloin | Liepard | Play Rough | 44 | 3 | 54 |
| Raboot | Cinderace | Double-Edge | 44 | 1 | never |
| Ralts | Kirlia | Fire Punch | 26 | 0 | never |
| Ralts | Kirlia | Zen Headbutt | 31 | 1 | 38 |
| Ralts | Kirlia | Thunderbolt | 33 | 1 | never |
| Rattata | Raticate | Double-Edge | 31 | 1 | 39 |
| Remoraid | Octillery | Ice Beam | 40 | 3 | 48 |
| Rhyhorn | Rhydon | Earthquake | 53 | 1 | 60 |
| Riolu | Lucario | Ice Punch | 30 | 0 | never |
| Rookidee | Corvisquire | Roost | 50 | 5 | 55 |
| Rowlet | Dartrix | Roost | 40 | 4 | 47 |
| Rowlet | Dartrix | Leaf Blade | 44 | 4 | 52 |
| Rowlet | Dartrix | Brave Bird | 48 | 5 | 55 |
| Salandit | Salazzle | Flamethrower | 38 | 1 | 54 |
| Salandit | Salazzle | Sludge Bomb | 39 | 1 | 56 |
| Scorbunny | Raboot | Flare Blitz | 45 | 5 | 56 |
| Scyther | Scizor | Air Slash | 53 | 4 | never |
| Scyther | Kleavor | Swords Dance | 57 | 6 | never |
| Seel | Dewgong | Ice Beam | 44 | 1 | 53 |
| Sentret | Furret | Baton Pass | 39 | 3 | 46 |
| Servine | Serperior | Leaf Blade | 43 | 1 | 55 |
| Sewaddle | Swadloon | Sticky Web | 31 | 1 | never |
| Sewaddle | Swadloon | Bug Buzz | 36 | 2 | never |
| Shelgon | Salamence | Dragon Claw | 55 | 1 | 61 |
| Shelgon | Salamence | Double-Edge | 61 | 3 | 70 |
| Shellos | Gastrodon | Recover | 46 | 3 | 54 |
| Shieldon | Bastiodon | Earthquake | 34 | 1 | 53 |
| Shieldon | Bastiodon | Iron Head | 39 | 1 | 44 |
| Shroomish | Breloom | Giga Drain | 37 | 2 | 56 |
| Shroomish | Breloom | Spore | 78 | 10 | never |
| Sinistea | Polteageist | Shadow Ball | 33 | 0 | 65 |
| Sinistea | Sinistcha | Shadow Ball | 33 | 1 | 65 |
| Sinistea | Sinistcha | Nasty Plot | 42 | 3 | never |
| Sinistea | Sinistcha | Shell Smash | 60 | 6 | never |
| Skitty | Delcatty | Double-Edge | 42 | 3 | never |
| Sliggoo | Goodra | Dragon Pulse | 53 | 0 | 58 |
| Slowpoke | Slowbro | Slack Off | 53 | 2 | 76 |
| Slugma | Magcargo | Flamethrower | 53 | 2 | 61 |
| Slugma | Magcargo | Earth Power | 56 | 3 | 66 |
| Smoochum | Jynx | Psychic | 35 | 1 | 66 |
| Smoochum | Jynx | Blizzard | 45 | 3 | 55 |
| Snover | Abomasnow | Blizzard | 41 | 0 | 47 |
| Spearow | Fearow | Roost | 33 | 1 | 41 |
| Spearow | Fearow | Drill Peck | 37 | 2 | 47 |
| Spheal | Sealeo | Dive | 33 | 0 | 38 |
| Spinarak | Ariados | Psychic | 40 | 3 | 46 |
| Spinarak | Ariados | Poison Jab | 43 | 3 | 50 |
| Spoink | Grumpig | Psychic | 41 | 2 | 47 |
| Spoink | Grumpig | Bounce | 48 | 3 | 60 |
| Sprigatito | Floragato | Seed Bomb | 18 | 1 | 36 |
| Starly | Staravia | Brave Bird | 44 | 4 | 53 |
| Staryu | Starmie | Recover | 44 | 1 | never |
| Staryu | Starmie | Hydro Pump | 55 | 3 | 60 |
| Surskit | Masquerain | Baton Pass | 43 | 3 | never |
| Swablu | Altaria | Air Slash | 44 | 1 | never |
| Swablu | Altaria | Dragon Pulse | 45 | 2 | 54 |
| Swinub | Piloswine | Earthquake | 37 | 1 | 53 |
| Swinub | Piloswine | Blizzard | 44 | 2 | 56 |
| Taillow | Swellow | Air Slash | 53 | 4 | 61 |
| Tentacool | Tentacruel | Toxic | 39 | 1 | 44 |
| Tentacool | Tentacruel | Hydro Pump | 40 | 2 | 49 |
| Togetic | Togekiss | Baton Pass | 42 | 0 | never |
| Togetic | Togekiss | Double-Edge | 46 | 1 | never |
| Torchic | Combusken | Flamethrower | 43 | 4 | 54 |
| Torracat | Incineroar | Flamethrower | 38 | 0 | 52 |
| Torracat | Incineroar | Fire Fang | 39 | 0 | 52 |
| Totodile | Croconaw | Dive | 26 | 0 | 48 |
| Totodile | Croconaw | Ice Fang | 33 | 1 | 38 |
| Totodile | Croconaw | Superpower | 39 | 2 | 44 |
| Totodile | Croconaw | Aqua Tail | 41 | 3 | 48 |
| Trapinch | Vibrava | Dig | 41 | 1 | never |
| Trapinch | Vibrava | Earthquake | 53 | 2 | never |
| Trapinch | Vibrava | Fire Fang | 56 | 3 | never |
| Trapinch | Vibrava | Earth Power | 65 | 5 | never |
| Trapinch | Vibrava | Superpower | 71 | 7 | never |
| Treecko | Grovyle | Slam | 36 | 3 | 41 |
| Trumbeak | Toucannon | Drill Peck | 32 | 0 | never |
| Trumbeak | Toucannon | Hyper Voice | 45 | 3 | 56 |
| Turtwig | Grotle | Giga Drain | 41 | 3 | 47 |
| Venonat | Venomoth | Poison Fang | 41 | 2 | 47 |
| Venonat | Venomoth | Psychic | 47 | 3 | 55 |
| Vullaby | Mandibuzz | Brave Bird | 65 | 2 | 72 |
| Vulpix | Alolan Ninetales | Flare Blitz | 40 | 2 | never |
| Vulpix | Alolan Ninetales | Fire Blast | 47 | 3 | never |
| Wailmer | Wailord | Dive | 41 | 0 | 46 |
| Wailmer | Wailord | Bounce | 44 | 0 | 54 |
| Wailmer | Wailord | Water Spout | 78 | 7 | never |
| Wartortle | Blastoise | Hydro Pump | 48 | 2 | 60 |
| Weepinbell | Victreebel | Slam | 41 | 3 | never |
| Whismur | Loudred | Hyper Voice | 45 | 4 | 57 |
| Wingull | Pelipper | Roost | 29 | 1 | 53 |
| Wingull | Pelipper | Air Slash | 47 | 4 | 63 |
| Wooloo | Dubwool | Double-Edge | 40 | 3 | 50 |
| Wooper | Clodsire | Slam | 15 | 0 | 37 |
| Wooper | Quagsire | Muddy Water | 30 | 1 | 53 |
| Wooper | Clodsire | Muddy Water | 30 | 2 | never |
| Wooper | Quagsire | Sludge Bomb | 33 | 1 | never |
| Wooper | Clodsire | Sludge Bomb | 33 | 2 | 39 |
| Wooper | Quagsire | Earthquake | 39 | 2 | 44 |
| Wooper | Clodsire | Earthquake | 39 | 3 | 44 |
| Yanma | Yanmega | Air Slash | 54 | 3 | 70 |
| Zigzagoon | Linoone | Belly Drum | 41 | 3 | 53 |
| Zubat | Golbat | Poison Fang | 33 | 1 | 39 |
| Zubat | Golbat | Air Slash | 41 | 3 | 51 |

## The three analyses

On Oxide's lists now and on the proposal, the same readings as the first generator's:

| Reading | Kaizo | Oxide now | The proposal |
|---|---|---|---|
| Pre-evolutions that reward a wait of a split or less | 124 | 63 | 70 |
| Moves only a Pokemon kept from evolving gets | 334 | 266 | 267 |
| Of those, strong | 148 | 45 | 56 |
| Wild slots that can end the encounter | | 153 | 142 |
| Wild slots that can knock themselves out | | 263 | 237 |
| Wild slots with a better version later | | 17 | 14 |
| Evolved catches with no good move by the split's cap | | 86 | 64 |

The share of catches with a good move known at capture or learnt by level-up before the split's cap:

| Split | Oxide now | The proposal |
|---|---|---|
| Roark | 0.07 | 0.05 |
| Gardenia | 0.26 | 0.23 |
| Fantina | 0.54 | 0.69 |
| Maylene | 0.74 | 0.67 |
| Wake | 0.87 | 0.86 |
| Byron | 0.85 | 0.87 |
| Candice | 0.90 | 0.94 |
| Galactic | 0.93 | 0.96 |
| Volkner | 0.86 | 0.98 |
| Barry | 0.93 | 1.00 |

## The checks

Every family's check list, totalled over all of them:

| Check | Failures |
|---|---|
| Nothing new past 78 | 0 |
| No weather move | 0 |
| No cut move | 0 |
| No dead weight added | 0 |
| No weak attack later than now | 0 |
| No strong move earlier than now on a strong stage, nor any S or SSS status move | 1 |
| No two moves on one level that the method placed | 0 |
| No strong move placed earlier than Kaizo's level within its split | 0 |
| No stage more than one split without an attack of its own type of 50 or more | 0 |
| No move that ends a wild encounter moved into the wild levels | 0 |
| Every final stage has a real move in the last splits, or is listed for Ian | 0 |
| Every stage reached without a level learns a real move after it is first had | 0 |
| No moved entry lands after a stronger move of its type and category | 0 |

No strong move earlier than now on a strong stage, nor any S or SSS status move: Chandelure Shadow Ball.

The own-type rule keeps 1 moves at their current level, where the proposal would have left a stage more than one split without an attack of its own type of 50 or more:

| Stage | Move | In the list of | Kept at |
|---|---|---|---|
| Hippopotas | Earthquake | Hippopotas | 37 |

For Ian: 9 such moves would reach a stage the power flags or the bar hold, so they are not kept until he rules; the stages they are for go without an attack of their own type meanwhile:

| Move | In the list of | Its level now | For | Would reach |
|---|---|---|---|---|
| Air Slash | Beautifly | 26 | Beautifly | Beautifly |
| Scald | Brionne | 34 | Brionne | Brionne, Primarina |
| Leaf Blade | Grovyle | 29 | Grovyle, Sceptile | Grovyle, Sceptile |
| Earthquake | Hippowdon | 40 | Hippowdon | Hippowdon |
| Fire Fang | Litten | 14 | Torracat | Litten, Torracat |
| Earth Power | Nidoqueen | 43 | Nidoqueen | Nidoqueen |
| Thunderbolt | Pikachu | 26 | Pikachu | Pikachu, Raichu |
| Shadow Ball | Polteageist | 48 | Polteageist | Polteageist |
| Bullet Seed | Skiploom | 20 | Jumpluff, Skiploom | Skiploom, Jumpluff |

65 stages go more than one split without an attack of their own type on Oxide's lists now, and the proposal does not make it longer (stages the player can evolve by the end of Gardenia's split are exempt); the later-moves proposal fills them where a later game offers one: Alolan Ninetales, Alomomola, Braixen, Budew, Carnivine, Charcadet, Charmeleon, Clefable, Cradily, Croconaw, Delcatty, Delibird, Dhelmise, Donphan, Drifloon, Duskull, Dustox, Espeon, Feebas, Feraligatr, Flaaffy, Floatzel, Glaceon, Gligar, Gliscor, Granbull, Happiny, Hippopotas, Kabuto, Kabutops, Lileep, Lopunny, Lunatone, Luvdisc, Magby, Masquerain, Mawile, Misdreavus, Mismagius, Munchlax, Nidoking, Qwilfish, Raboot, Roselia, Seel, Shellder, Shiftry, Slugma, Solrock, Staryu, Steelix, Swablu, Sylveon, Tangela, Tangrowth, Togekiss, Togetic, Trapinch, Umbreon, Unown, Vaporeon, Vibrava, Wartortle, Yanma, Yanmega.

Where Kaizo's own level is past Oxide's 78, the rule would take the move out of play, against the rule that nothing goes past 78, so these 18 keep their translated place for Ian to decide:

| Stage | Move | Kaizo's level | Kept at |
|---|---|---|---|
| Articuno | Roost | 85 | 69 |
| Braixen | Will-O-Wisp | 90 | 72 |
| Cresselia | Psychic | 93 | 74 |
| Crobat | Brave Bird | 80 | 63 |
| Frogadier | Hydro Pump | 95 | 75 |
| Gabite | Dragon Rush | 88 | 70 |
| Giratina | Shadow Claw | 80 | 63 |
| Grapploct | Superpower | 90 | 72 |
| Hariyama | Close Combat | 90 | 72 |
| Houndoom | Will-O-Wisp | 90 | 72 |
| Moltres | Roost | 85 | 69 |
| Regirock | Superpower | 81 | 64 |
| Registeel | Superpower | 81 | 64 |
| Shroomish | Spore | 100 | 78 |
| Slowbro | Slack Off | 97 | 76 |
| Trapinch | Superpower | 89 | 71 |
| Wailmer | Water Spout | 100 | 78 |
| Zapdos | Roost | 85 | 69 |

6 moved entries found no free level in their split and share one: Clodsire's Sludge Bomb at 39; Clodsire's Megahorn at 39; Vikavolt's X-Scissor at 53; Vikavolt's Bug Buzz at 53; Sinistcha's Matcha Gotcha at 65; Sinistcha's Shadow Ball at 65.

## After an evolution without a level

Ian's ruling (2026-09-28): a stage reached by a stone, a held item, a known move, a place, a partner or Beauty gets its own sparser list after the evolution: its key moves, fewer than the pre-evolution learns after that point, so evolving early still costs moves. 30 key moves go to 22 stages; 15 candidates a rule kept out.

| Stage | Move | Level | From the source's |
|---|---|---|---|
| Alolan Ninetales | Aurora Beam | 24 | 24 |
| Alolan Ninetales | Icy Wind | 16 | 16 |
| Cinccino | Slam | 53 | 53 |
| Clefable | Cosmic Power | 25 | 25 |
| Clodsire | Haze | 43 | 43 |
| Clodsire | Mud Bomb | 19 | 19 |
| Clodsire | Sludge Bomb | 39 | 33 |
| Cloyster | Brine | 44 | 44 |
| Cloyster | Ice Beam | 49 | 49 |
| Delcatty | Assist | 22 | 22 |
| Delcatty | Covet | 36 | 36 |
| Electivire | Thunderbolt | 53 | 53 |
| Hisuian Sliggoo | Dragon Tail | 28 | 28 |
| Honchkrow | Assurance | 32 | 32 |
| Honchkrow | Faint Attack | 34 | 35 |
| Ludicolo | Hydro Pump | 45 | 45 |
| Mismagius | Shadow Ball | 56 | 37 |
| Nidoking | Poison Jab | 43 | 43 |
| Ninetales | Fire Blast | 47 | 47 |
| Politoed | Hydro Pump | 49 | 48 |
| Raichu | Thunder | 45 | 45 |
| Roserade | Sludge Bomb | 60 | 60 |
| Shiftry | Faint Attack | 31 | 31 |
| Sinistcha | Aromatherapy | 29 | 30 |
| Sinistcha | Matcha Gotcha | 65 | 61 |
| Starmie | Hydro Pump | 60 | 55 |
| Starmie | Light Screen | 42 | 42 |
| Umbreon | Bite | 28 | 29 |
| Vikavolt | X-Scissor | 53 | 53 |
| Yanmega | Wing Attack | 42 | 43 |

## Evolution moves, for Ian

A level-0 entry is taught the moment the Pokemon evolves, never known by a wild, gift or trainer Pokemon, and offered by the relearner (the engine support follows). Used sparingly, each listed here for Ian:

| Stage | Move | Why |
|---|---|---|
| Delcatty | Covet | the weakest attack of its own type that closes its gap |
| Galarian Weezing | Draining Kiss | the strongest Fairy attack that is not a strong move, from Oxide's whole move table, since nothing Galarian Weezing learns in any game fits (Ian may prefer one of its own, weaker or strong) |
| Sylveon | Draining Kiss | Ian's choice by name (2026-09-29) |

## The new species' donor evolution moves

Ian's ruling (2026-09-30): the moves the donor teaches on evolving, which Oxide's importer had written at level 1, go to level 0. 28 moves on 21 stages. A strong move learned on evolving, and a stage left with more than one level-0 move, are marked for Ian.

| Stage | Move | Strong by the rules | Level-0 moves on the stage |
|---|---|---|---|
| Alolan Ninetales | Dazzling Gleam | yes, for Ian | 1 |
| Annihilape | Shadow Punch | yes, for Ian | 1 |
| Armarouge | Psyshock | yes, for Ian | 1 |
| Ceruledge | Night Slash |  | 5, for Ian |
| Ceruledge | Quick Guard |  | 5, for Ian |
| Ceruledge | Shadow Claw | yes, for Ian | 5, for Ian |
| Ceruledge | Shadow Sneak |  | 5, for Ian |
| Ceruledge | Solar Blade |  | 5, for Ian |
| Charjabug | Charge |  | 1 |
| Cofagrigus | Scary Face |  | 2, for Ian |
| Cofagrigus | Shadow Claw | yes, for Ian | 2, for Ian |
| Galarian Rapidash | Psycho Cut |  | 1 |
| Garganacl | Hammer Arm | yes, for Ian | 1 |
| Glimmora | Mortal Spin |  | 1 |
| Greninja | Night Slash | yes, for Ian | 2, for Ian |
| Greninja | Water Shuriken |  | 2, for Ian |
| Hisuian Sliggoo | Shelter |  | 1 |
| Leavanny | Slash |  | 1 |
| Lurantis | Petal Blizzard | yes, for Ian | 1 |
| Mandibuzz | Bone Rush |  | 1 |
| Naclstack | Salt Cure |  | 1 |
| Naganadel | Air Cutter |  | 1 |
| Sinistcha | Matcha Gotcha | yes, for Ian | 1 |
| Swadloon | Protect |  | 1 |
| Sylveon | Disarming Voice |  | 3, for Ian |
| Sylveon | Fairy Wind |  | 3, for Ian |
| Toucannon | Beak Blast | yes, for Ian | 1 |
| Toxapex | Baneful Bunker |  | 1 |

## A move in the last splits

Ian's ruling (2026-09-28): every final stage the player can own learns at least one real move by level-up in the Galactic split or later (61 to 78). 134 stages had none and get one; the source of each: Kaizo's 53, the later games 41, its own level 1 21, a TM it learns 16, a tutor move it learns 3.

| Stage | Move | Level | From |
|---|---|---|---|
| Abomasnow | Ice Hammer | 66 | Legends Z-A at 1 |
| Alakazam | Focus Blast | 65 | a TM it learns |
| Alolan Ninetales | Blizzard | 76 | its own level 1 |
| Ambipom | Aerial Ace | 65 | Kaizo's Ambipom at 56 |
| Annihilape | Bulldoze | 73 | Legends Z-A at 22 |
| Azumarill | Ice Punch | 61 | Kaizo's Azumarill at 57 |
| Bastiodon | Iron Tail | 70 | a TM it learns |
| Beautifly | Venoshock | 61 | Legends Arceus at 25 |
| Bibarel | Rock Climb | 62 | a TM it learns |
| Blastoise | Ice Beam | 73 | Kaizo's Blastoise at 53 |
| Blissey | Focus Blast | 75 | a TM it learns |
| Breloom | Superpower | 63 | a tutor move it learns |
| Carnivine | Giga Drain | 66 | Kaizo's Carnivine at 31 |
| Castform | Hurricane | 69 | Legends Z-A at 45 |
| Chatot | Air Slash | 63 | Kaizo's Chatot at 41 |
| Cherrim | Flare Blitz | 70 | Kaizo's Cherrim at 60 |
| Chimecho | Psychic | 62 | Kaizo's Chimecho at 30 |
| Cinccino | Bullet Seed | 63 | its own level 1 |
| Clefable | Air Slash | 65 | Kaizo's Clefable at 55 |
| Cloyster | Razor Shell | 76 | Legends Z-A at 5 |
| Cofagrigus | Psyshock | 65 | Legends Z-A at 30 |
| Corsola | Aqua Cutter | 63 | Kaizo's Corsola at 44 |
| Crawdaunt | Cross Chop | 63 | Kaizo's Crawdaunt at 60 |
| Delcatty | Play Rough | 66 | Brilliant Diamond and Shining Pearl at 1 |
| Delibird | Freeze-Dry | 63 | Legends Z-A at 37 |
| Dewgong | Ice Fang | 68 | Kaizo's Dewgong at 41 |
| Donphan | Fire Fang | 69 | its own level 1 |
| Drapion | Thunder Fang | 68 | its own level 1 |
| Drifblim | Mystical Fire | 67 | Legends Arceus at 25 |
| Dustox | Sludge Bomb | 61 | Kaizo's Dustox at 20 |
| Empoleon | Earthquake | 73 | Kaizo's Empoleon at 64 |
| Espeon | Light Screen | 71 | a TM it learns |
| Floatzel | Ice Punch | 66 | Kaizo's Floatzel at 30 |
| Florges | Wish | 76 | its own level 1 |
| Flygon | Boomburst | 75 | Legends Z-A at 68 |
| Froslass | Hex | 71 | Scarlet and Violet at 0 |
| Furret | Coil | 62 | Legends Z-A at 1 |
| Galarian Rapidash | Megahorn | 72 | its own level 1 |
| Galarian Weezing | Heat Wave | 65 | its own level 1 |
| Gallade | Aqua Cutter | 71 | Scarlet and Violet at 1 |
| Garchomp | Dragon Rush | 78 | its own level 1 |
| Gardevoir | Moonblast | 72 | Legends Z-A at 49 |
| Garganacl | Hammer Arm | 68 | its own level 1 |
| Gastrodon | Rock Slide | 64 | Kaizo's Gastrodon at 22 |
| Gengar | Sludge Bomb | 68 | Kaizo's Gengar at 53 |
| Girafarig | Earthquake | 71 | Kaizo's Girafarig at 41 |
| Glalie | Light Screen | 71 | a TM it learns |
| Glimmora | Meteor Beam | 71 | Legends Z-A at 0 |
| Gliscor | Earthquake | 69 | Kaizo's Gliscor at 55 |
| Golduck | Psychic | 68 | Kaizo's Golduck at 44 |
| Golem | Steamroller | 71 | Legends Z-A at 10 |
| Gorebyss | Ice Beam | 65 | Kaizo's Gorebyss at 42 |
| Granbull | Earthquake | 62 | Kaizo's Granbull at 51 |
| Heracross | Rock Slide | 68 | Kaizo's Heracross at 13 |
| Hippowdon | Ice Fang | 71 | its own level 1 |
| Hisuian Goodra | Draco Meteor | 77 | its own level 1 |
| Honchkrow | Brave Bird | 75 | Kaizo's Honchkrow at 35 |
| Huntail | Body Slam | 65 | Kaizo's Huntail at 33 |
| Jumpluff | Bullet Seed | 62 | its own level 1 |
| Jynx | Psychic | 66 | Kaizo's Jynx at 44 |
| Kingdra | Ice Beam | 75 | Kaizo's Kingdra at 40 |
| Kingler | Superpower | 68 | Kaizo's Kingler at 51 |
| Kleavor | Brutal Swing | 68 | Legends Z-A at 20 |
| Klefki | Dazzling Gleam | 63 | Legends Z-A at 44 |
| Kricketune | Brick Break | 62 | Kaizo's Kricketune at 46 |
| Lanturn | Thunder | 65 | a TM it learns |
| Lapras | Drill Run | 76 | Kaizo's Lapras at 37 |
| Leavanny | Slash | 68 | its own level 1 |
| Lickilicky | Zen Headbutt | 70 | Kaizo's Lickilicky at 51 |
| Liepard | Snarl | 67 | Legends Z-A at 1 |
| Lopunny | Play Rough | 69 | Legends Arceus at 31 |
| Lucario | Bulldoze | 71 | Legends Z-A at 28 |
| Ludicolo | Energy Ball | 68 | a TM it learns |
| Lumineon | Ice Fang | 65 | Kaizo's Lumineon at 35 |
| Lunatone | Moonblast | 66 | X and Y at 50 |
| Lurantis | Dual Chop | 64 | Sword and Shield at 1 |
| Machamp | Dual Chop | 69 | Brilliant Diamond and Shining Pearl at 36 |
| Magnezone | Thunder | 73 | a TM it learns |
| Mamoswine | Icicle Spear | 76 | Kaizo's Mamoswine at 65 |
| Mantine | Air Slash | 66 | Kaizo's Mantine at 40 |
| Mawile | Play Rough | 62 | Legends Z-A at 48 |
| Medicham | Axe Kick | 62 | Scarlet and Violet at 53 |
| Milotic | Dragon Pulse | 75 | Kaizo's Milotic at 81 |
| Minun | Hyper Voice | 61 | Kaizo's Minun at 38 |
| Mismagius | Mystical Fire | 69 | Legends Z-A at 1 |
| Mothim | Aerial Ace | 63 | Kaizo's Mothim at 29 |
| Mr Mime | Dazzling Gleam | 66 | Legends Z-A at 44 |
| Mr Rime | Dazzling Gleam | 71 | Legends Z-A at 44 |
| Nidoking | Sludge Wave | 73 | Brilliant Diamond and Shining Pearl at 1 |
| Nidoqueen | Sludge Wave | 73 | Brilliant Diamond and Shining Pearl at 1 |
| Ninetales | Hex | 76 | Legends Arceus at 21 |
| Noctowl | Moonblast | 65 | Legends Z-A at 43 |
| Octillery | Gunk Shot | 71 | its own level 1 |
| Pachirisu | Thunder | 62 | Kaizo's Pachirisu at 55 |
| Pelipper | Air Slash | 63 | Kaizo's Pelipper at 38 |
| Plusle | ThunderPunch | 61 | Kaizo's Plusle at 15 |
| Politoed | Surf | 72 | a TM it learns |
| Poliwrath | Ice Punch | 72 | Kaizo's Poliwrath at 43 |
| Purugly | Shadow Claw | 66 | Kaizo's Purugly at 45 |
| Quagsire | Ice Punch | 62 | Kaizo's Quagsire at 45 |
| Qwilfish | Payback | 68 | Kaizo's Qwilfish at 25 |
| Raichu | ThunderPunch | 66 | a tutor move it learns |
| Rampardos | Revenge | 68 | Kaizo's Rampardos at 36 |
| Rapidash | Smart Strike | 72 | Legends Z-A at 0 |
| Roserade | Energy Ball | 69 | a TM it learns |
| Rotom | Dark Pulse | 71 | Kaizo's Rotom at 29 |
| Runerigus | Shadow Claw | 65 | its own level 1 |
| Serperior | Coil | 72 | Legends Z-A at 38 |
| Sharpedo | Liquidation | 63 | Legends Z-A at 44 |
| Shiftry | Leaf Blade | 64 | Kaizo's Shiftry at 55 |
| Skarmory | Drill Run | 68 | Legends Z-A at 38 |
| Skuntank | Venoshock | 67 | Legends Z-A at 21 |
| Slowking | Curse | 65 | its own level 1 |
| Snorlax | Earthquake | 75 | Kaizo's Snorlax at 84 |
| Solrock | Stone Edge | 66 | a TM it learns |
| Spiritomb | Hex | 75 | Legends Z-A at 25 |
| Staraptor | Steel Wing | 64 | a TM it learns |
| Starmie | Psychic | 75 | a TM it learns |
| Steelix | Earthquake | 76 | Kaizo's Steelix at 54 |
| Sudowoodo | Wood Hammer | 62 | Kaizo's Sudowoodo at 49 |
| Tangrowth | Energy Ball | 73 | a TM it learns |
| Tentacruel | Sludge Bomb | 73 | Kaizo's Tentacruel at 36 |
| Togekiss | Moonblast | 75 | Legends Arceus at 43 |
| Torterra | Wood Hammer | 73 | Kaizo's Torterra at 45 |
| Toucannon | Rock Blast | 65 | its own level 1 |
| Toxicroak | Gunk Shot | 65 | a tutor move it learns |
| Tsareena | Triple Axel | 72 | its own level 1 |
| Vespiquen | Bug Buzz | 76 | Kaizo's Vespiquen at 37 |
| Walrein | Liquidation | 75 | Legends Arceus at 25 |
| Weavile | Assurance | 69 | its own level 1 |
| Weezing | Thunder | 69 | a TM it learns |
| Whiscash | Zen Headbutt | 63 | its own level 1 |
| Wormadam | Blizzard | 62 | Kaizo's Wormadam at 44 |
| Yanmega | Air Slash | 70 | its own level 1 |

For Ian, with nothing that qualifies: Arboliva, Carbink, Clodsire, Dubwool, Emolga, Frosmoth, Gothitelle, Palossand, Salazzle, Sylveon, Togedemaru, Toxapex, Unown.

## By name, for Ian

Lists Ian asked for by name, placed past the flags' first-of-type test (ruling 19: a proper list for Alolan Ninetales, for the wild catch and the Ice Stone route alike): Alolan Ninetales's Draining Kiss at 30; Alolan Ninetales's Ice Beam at 45; Sylveon's Dazzling Gleam at 32; Chandelure's Shadow Ball at 48.

## What the Overseer's read changed

The Overseer read the first version of these rulings as a player (2026-09-28). A late move now has to give the stage something it lacks by then: a stronger attack of its type in its better category, one twenty points more accurate that keeps three quarters of the power, a new type, or a status move rated A or better. An attack in the weaker category across a gap of 20 in the attacking stats, a charging or out-of-reach move (unless nothing else adds), a self-knockout, partner, evasion or Protect move never counts. The late levels spread from 61 to 78 by the stage's base stat total, the weakest earliest. A moved entry that would come after a stronger move of its type and category goes back to its current level (0) or leaves (10): Kleavor's Skitter Smack (dropped, not 52); Clodsire's Poison Tail (dropped, not 38); Absol's Night Slash (dropped, not 56); Ferrothorn's Bullet Seed (dropped, not 43); Klefki's Flash Cannon (dropped, not 53); Incineroar's Fire Fang (dropped, not 56); Incineroar's Blaze Kick (dropped, not 59); Toucannon's Drill Peck (dropped, not 53); Lurantis's Leaf Blade (dropped, not 44); Orbeetle's Psyshock (dropped, not 53). Repeated entries leave every list, except what a first stage knows when first had. Evasion and Protect are never a key or late pick, so Clefable's Minimize at 19 is gone.

# The learnset proposal

Written by `learnplan.py full` (2026-09-27) for the Overseer to read before Ian. It proposes level-up lists for all 652 species; nothing here is in the game data. `docs/oxide/learnset-proposal.tsv` has every entry, now and proposed, with the reason for each change, and `learnplan.py line <species>` prints one line in full, with its delays and check list.

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

It changes the lists of 467 of the 652 species. The 185 that no source gives the player, by the League or after it (Groudon, Xerneas and the like), keep their lists but for the drops: those lists only feed trainers' default moves, which the trainer pass sets.

| Entries | Count |
|---|---|
| Kept where they are | 8346 |
| Moved | 268 |
| Added | 117 |
| Dropped | 524 |

The reasons given for the moves and additions (an entry moved twice, by Kaizo and then by the one-level rule, counts under both):

| Change | Reason | Count |
|---|---|---|
| Moved | Kaizo's own list for the species, translated by split | 128 |
| Moved | Kaizo's nearest lines, translated by split | 117 |
| Added | Kaizo's own list for the species, translated by split | 83 |
| Moved | the one-level rule | 56 |
| Moved | an exclusive delay from Kaizo | 32 |
| Added | a first stage keeps its first attack | 30 |
| Added | the one-level rule | 25 |
| Added | an exclusive delay from Kaizo | 8 |
| Added | the move-pool survey's first move | 4 |
| Moved | the move-pool survey's first move | 3 |

Why entries left:

| Reason | Count |
|---|---|
| Strength 20, under 40 | 68 |
| Weather, for a species the player can own | 65 |
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
| Strength 48, at most half of Wake's usual 95 | 2 |
| Strength 45, at most half of Wake's usual 95 | 1 |

## The power flags

86 stages trip a flag before Byron's split. Each is held to no strong move earlier than now on its own list; the last column is what the proposal does to its strong moves, the earliest each can be known by any route, a pre-evolution kept back included.

| Stage | Split | Look | Why | Strong moves, now and proposed |
|---|---|---|---|---|
| Kadabra | Roark | brought to Ian by name | base Speed 105 | Recover 30 to 39 |
| Delcatty | Gardenia | brought to Ian by name | base Speed 112 | Hyper Voice 35 to never |
| Donphan | Gardenia | brought to Ian by name | base Attack 120 with Slam (100) | as now |
| Emolga | Gardenia | brought to Ian by name | base Speed 103 | Volt Switch 40 to 53 |
| Floatzel | Gardenia | brought to Ian by name | base Speed 115 | as now |
| Houndoom | Gardenia | brought to Ian by name | base Special Attack 110 with Fire Blast (110) | Dark Pulse never to 56; Will-O-Wisp never to 72 |
| Liepard | Gardenia | brought to Ian by name | base Speed 116 | as now |
| Lopunny | Gardenia | brought to Ian by name | base Speed 105 | as now |
| Minun | Gardenia | brought to Ian by name | base Speed 105 | Thunderbolt never to 43 |
| Octillery | Gardenia | brought to Ian by name | base Special Attack 108 with Fire Blast (110) | as now |
| Steelix | Gardenia | brought to Ian by name | base Attack 115 with Slam (100) | as now |
| Ambipom | Fantina | brought to Ian by name | base Speed 115 | as now |
| Feraligatr | Fantina | brought to Ian by name | base Attack 125 with Earthquake (100) | Dive never to 30; Ice Fang 30 to 33; Superpower 43 to 39 |
| Froslass | Fantina | brought to Ian by name | base Speed 110 | Ice Beam never to 60 |
| Gallade | Fantina | brought to Ian by name | base Attack 125 with Earthquake (100) | Fire Punch never to 27; Psychic 28 to 38; Thunderbolt never to 33; Zen Headbutt never to 31 |
| Galvantula | Fantina | brought to Ian by name | base Speed 108 | Bug Buzz 48 to 39; Discharge 30 to 38; Energy Ball 37 to 44; Signal Beam 34 to 35; Thunderbolt 45 to 41 |
| Granbull | Fantina | brought to Ian by name | base Attack 120 with Earthquake (100) | as now |
| Hariyama | Fantina | brought to Ian by name | base Attack 120 with Earthquake (100) | Close Combat 40 to 44; Shadow Punch never to 53 |
| Heracross | Fantina | brought to Ian by name | base Attack 125 with Earthquake (100) | Brick Break 19 to 26 |
| Jumpluff | Fantina | brought to Ian by name | base Speed 110 | Seed Bomb never to 32 |
| Magmortar | Fantina | brought to Ian by name | base Special Attack 125 with Fire Blast (110) | as now |
| Mismagius | Fantina | brought to Ian by name | base Speed 105 | as now |
| Nidoking | Fantina | brought to Ian by name | base Attack 102 with Earthquake (100) | Earth Power 43 to never; Earthquake never to 53 |
| Piloswine | Fantina | brought to Ian by name | base Attack 110 with Earthquake (100) | as now |
| Salazzle | Fantina | brought to Ian by name | base Speed 117 | Flamethrower 34 to 38; Sludge Bomb 40 to 39 |
| Sharpedo | Fantina | brought to Ian by name | base Attack 120 with Earthquake (100) | Ice Fang 30 to 53 |
| Torterra | Fantina | brought to Ian by name | base Attack 111 with Earthquake (100) | as now |
| Ampharos | Maylene | very close look | base Special Attack 115 with Focus Blast (120) | Discharge 30 to 33; Thunderbolt never to 39 |
| Blastoise | Maylene | very close look | base Special Attack 110 with Focus Blast (120) | as now |
| Blaziken | Maylene | very close look | base Attack 120 with Earthquake (100) | Brave Bird 49 to never |
| Castform | Maylene | very close look | base Special Attack 120 with Thunder (110) | as now |
| Charizard | Maylene | very close look | base Special Attack 110 with Focus Blast (120) | as now |
| Chatot | Maylene | very close look | base Speed 110 | as now |
| Cinderace | Maylene | very close look | base Speed 119 | Double-Edge 39 to 44 |
| Crawdaunt | Maylene | very close look | base Attack 120 with Crabhammer (100) | as now |
| Delphox | Maylene | very close look | base Speed 104 | as now |
| Electabuzz | Maylene | very close look | base Speed 105 | Thunderbolt 37 to 39 |
| Electivire | Maylene | very close look | base Speed 105 | Thunderbolt 37 to 39 |
| Empoleon | Maylene | very close look | base Attack 111 with Earthquake (100) | as now |
| Gardevoir | Maylene | very close look | base Special Attack 135 with Focus Blast (120) | Fire Punch never to 30; Psychic 30 to 38; Thunderbolt never to 33; Zen Headbutt never to 31 |
| Girafarig | Maylene | very close look | base Special Attack 110 with Thunder (110) | as now |
| Glaceon | Maylene | very close look | base Special Attack 130 with Blizzard (110) | as now |
| Gorebyss | Maylene | very close look | base Special Attack 114 with Blizzard (110) | as now |
| Greninja | Maylene | very close look | base Speed 122 | Waterfall 36 to 39 |
| Hippowdon | Maylene | very close look | base Attack 112 with Earthquake (100) | as now |
| Jolteon | Maylene | very close look | base Speed 130 | as now |
| Jynx | Maylene | very close look | base Special Attack 115 with Focus Blast (120) | as now |
| Kingler | Maylene | very close look | base Attack 130 with Slam (100) | as now |
| Krabby | Maylene | very close look | base Attack 105 with Slam (100) | as now |
| Magcargo | Maylene | very close look | base Special Attack 109 with Fire Blast (110) | as now |
| Meowscarada | Maylene | very close look | base Speed 123 | as now |
| Mienshao | Maylene | very close look | base Speed 105 | as now |
| Ninetales | Maylene | very close look | base Special Attack 109 with Fire Blast (110) | as now |
| Pawmot | Maylene | very close look | base Speed 105 | Close Combat 49 to 56 |
| Primeape | Maylene | very close look | base Attack 115 with Earthquake (100) | as now |
| Purugly | Maylene | very close look | base Speed 112 | as now |
| Raichu | Maylene | very close look | base Speed 110 | as now |
| Sceptile | Maylene | very close look | base Speed 120 | Leaf Blade 36 to 52 |
| Scyther | Maylene | very close look | base Speed 105 | X-Scissor 41 to 52 |
| Serperior | Maylene | very close look | base Speed 113 | as now |
| Sneasel | Maylene | very close look | base Speed 115 | as now |
| Snorlax | Maylene | very close look | base Attack 110 with Earthquake (100) | as now |
| Staraptor | Maylene | very close look | base Speed 105 | Brave Bird 37 to 44; Close Combat 34 to 53 |
| Starmie | Maylene | very close look | base Speed 115 | Recover 34 to 44 |
| Swampert | Maylene | very close look | base Attack 110 with Earthquake (100) | as now |
| Talonflame | Maylene | very close look | base Speed 126 | Brave Bird 55 to 65; Flare Blitz 51 to 64 |
| Tangrowth | Maylene | very close look | base Special Attack 110 with Focus Blast (120) | as now |
| Toxicroak | Maylene | very close look | base Attack 106 with Earthquake (100) | as now |
| Vaporeon | Maylene | very close look | base Special Attack 110 with Blizzard (110) | as now |
| Absol | Wake | close look | base Special Attack 115 with Thunder (110) | Night Slash 52 to 56 |
| Alakazam | Wake | close look | base Speed 120 | as now |
| Cinccino | Wake | close look | base Speed 115 | as now |
| Crobat | Wake | close look | base Speed 130 | Brave Bird never to 53 |
| Espeon | Wake | close look | base Speed 110 | as now |
| Frosmoth | Wake | close look | base Special Attack 125 with Blizzard (110) | as now |
| Gengar | Wake | close look | base Speed 110 | as now |
| Golem | Wake | close look | base Attack 130 with Double-Edge (120) | as now |
| Grapploct | Wake | close look | base Attack 118 with Superpower (120) | Superpower 45 to 44 |
| Kleavor | Wake | close look | base Attack 135 with Superpower (120) | Superpower 40 to 43 |
| Machamp | Wake | close look | base Attack 130 with Earthquake (100) | as now |
| Mamoswine | Wake | close look | base Attack 135 with Earthquake (100) | as now |
| Rapidash | Wake | close look | base Speed 110 | as now |
| Rhydon | Wake | close look | base Attack 130 with Earthquake (100) | Earthquake 49 to 53 |
| Togekiss | Wake | close look | base Special Attack 120 with Fire Blast (110) | as now |
| Vespiquen | Wake | close look | base Attack 102 with Attack Order (120) | Attack Order 37 to 40 |
| Wailord | Wake | close look | base Attack 110 with Earthquake (100) | Water Spout 40 to 78 |

## The power bar

210 stages with no flag pass the bar before Byron's split on Oxide's lists now, and are held the same way. The thresholds are provisional; Ian's Talonflame at 39 outsped 92 of Maylene's 93 trainer Pokemon and knocked out 38 in one hit, well over both.

| Stage | Split | Outsped | Knocked out in one hit |
|---|---|---|---|
| Barboach | Roark | 93% | 59% |
| Beautifly | Roark | 98% | 86% |
| Bibarel | Roark | 100% | 57% |
| Braixen | Roark | 100% | 48% |
| Buizel | Roark | 100% | 59% |
| Buneary | Roark | 100% | 84% |
| Charmander | Roark | 98% | 89% |
| Charmeleon | Roark | 100% | 91% |
| Chinchou | Roark | 98% | 48% |
| Corphish | Roark | 77% | 64% |
| Corsola | Roark | 77% | 80% |
| Corvisquire | Roark | 100% | 50% |
| Dottler | Roark | 68% | 32% |
| Dustox | Roark | 98% | 41% |
| Fennekin | Roark | 93% | 32% |
| Finneon | Roark | 98% | 34% |
| Fletchinder | Roark | 100% | 55% |
| Fletchling | Roark | 96% | 39% |
| Froakie | Roark | 100% | 57% |
| Frogadier | Roark | 100% | 73% |
| Furret | Roark | 100% | 59% |
| Glameow | Roark | 100% | 27% |
| Gligar | Roark | 100% | 48% |
| Goldeen | Roark | 96% | 43% |
| Grubbin | Roark | 91% | 34% |
| Houndour | Roark | 98% | 70% |
| Kricketune | Roark | 98% | 52% |
| Lombre | Roark | 91% | 52% |
| Lotad | Roark | 68% | 30% |
| Luvdisc | Roark | 100% | 36% |
| Luxio | Roark | 93% | 64% |
| Machop | Roark | 77% | 66% |
| Magby | Roark | 100% | 66% |
| Marshtomp | Roark | 91% | 66% |
| Mudkip | Roark | 84% | 59% |
| Murkrow | Roark | 100% | 64% |
| Nidoran M | Roark | 91% | 41% |
| Nidorina | Roark | 91% | 43% |
| Nidorino | Roark | 98% | 50% |
| Nosepass | Roark | 68% | 48% |
| Nuzleaf | Roark | 93% | 48% |
| Onix | Roark | 100% | 59% |
| Pachirisu | Roark | 100% | 66% |
| Phanpy | Roark | 84% | 46% |
| Pikipek | Roark | 98% | 55% |
| Piplup | Roark | 84% | 57% |
| Poliwag | Roark | 100% | 30% |
| Ponyta | Roark | 100% | 61% |
| Poochyena | Roark | 77% | 34% |
| Prinplup | Roark | 91% | 61% |
| Psyduck | Roark | 91% | 52% |
| Raboot | Roark | 100% | 39% |
| Remoraid | Roark | 98% | 75% |
| Rookidee | Roark | 91% | 36% |
| Scorbunny | Roark | 100% | 27% |
| Sewaddle | Roark | 84% | 36% |
| Shinx | Roark | 89% | 64% |
| Skitty | Roark | 91% | 30% |
| Squirtle | Roark | 89% | 52% |
| Staravia | Roark | 100% | 55% |
| Starly | Roark | 93% | 41% |
| Surskit | Roark | 98% | 70% |
| Tentacool | Roark | 100% | 46% |
| Trumbeak | Roark | 100% | 64% |
| Turtwig | Roark | 68% | 27% |
| Vullaby | Roark | 93% | 41% |
| Vulpix | Roark | 98% | 84% |
| Wartortle | Roark | 91% | 61% |
| Wingull | Roark | 100% | 59% |
| Aipom | Gardenia | 96% | 61% |
| Alolan Ninetales | Gardenia | 100% | 35% |
| Araquanid | Gardenia | 75% | 64% |
| Azumarill | Gardenia | 81% | 57% |
| Bidoof | Gardenia | 55% | 33% |
| Breloom | Gardenia | 89% | 87% |
| Brionne | Gardenia | 81% | 48% |
| Budew | Gardenia | 85% | 28% |
| Carbink | Gardenia | 81% | 33% |
| Carvanha | Gardenia | 89% | 80% |
| Charjabug | Gardenia | 63% | 64% |
| Cherrim | Gardenia | 96% | 61% |
| Cherubi | Gardenia | 63% | 32% |
| Chimecho | Gardenia | 92% | 64% |
| Chingling | Gardenia | 77% | 41% |
| Clamperl | Gardenia | 55% | 36% |
| Clefable | Gardenia | 89% | 80% |
| Clefairy | Gardenia | 63% | 67% |
| Combee | Gardenia | 89% | 39% |
| Combusken | Gardenia | 85% | 88% |
| Dartrix | Gardenia | 83% | 64% |
| Dolliv | Gardenia | 61% | 31% |
| Dubwool | Gardenia | 97% | 73% |
| Dwebble | Gardenia | 85% | 65% |
| Flaaffy | Gardenia | 77% | 56% |
| Glimmet | Gardenia | 88% | 65% |
| Golbat | Gardenia | 99% | 60% |
| Graveler | Gardenia | 63% | 68% |
| Grotle | Gardenia | 63% | 49% |
| Grovyle | Gardenia | 99% | 57% |
| Hoothoot | Gardenia | 81% | 37% |
| Hoppip | Gardenia | 81% | 27% |
| Huntail | Gardenia | 83% | 76% |
| Litten | Gardenia | 89% | 64% |
| Mantyke | Gardenia | 81% | 37% |
| Mareep | Gardenia | 63% | 51% |
| Marill | Gardenia | 72% | 36% |
| Masquerain | Gardenia | 88% | 52% |
| Meditite | Gardenia | 88% | 64% |
| Mienfoo | Gardenia | 89% | 71% |
| Mightyena | Gardenia | 89% | 56% |
| Mothim | Gardenia | 89% | 68% |
| Naclstack | Gardenia | 63% | 33% |
| Nidoqueen | Gardenia | 93% | 81% |
| Nidoran F | Gardenia | 75% | 32% |
| Noctowl | Gardenia | 89% | 83% |
| Pawmi | Gardenia | 88% | 29% |
| Pawmo | Gardenia | 96% | 48% |
| Pelipper | Gardenia | 100% | 67% |
| Pikachu | Gardenia | 99% | 48% |
| Plusle | Gardenia | 85% | 61% |
| Poliwhirl | Gardenia | 99% | 40% |
| Popplio | Gardenia | 72% | 33% |
| Purrloin | Gardenia | 89% | 25% |
| Quagsire | Gardenia | 63% | 67% |
| Rowlet | Gardenia | 75% | 55% |
| Seedot | Gardenia | 52% | 28% |
| Servine | Gardenia | 93% | 32% |
| Shellos | Gardenia | 61% | 36% |
| Shiftry | Gardenia | 93% | 76% |
| Shroomish | Gardenia | 63% | 29% |
| Skiploom | Gardenia | 93% | 32% |
| Snivy | Gardenia | 89% | 27% |
| Snorunt | Gardenia | 81% | 53% |
| Snover | Gardenia | 72% | 65% |
| Snubbull | Gardenia | 52% | 56% |
| Steenee | Gardenia | 89% | 25% |
| Swadloon | Gardenia | 75% | 41% |
| Swinub | Gardenia | 81% | 40% |
| Togetic | Gardenia | 72% | 69% |
| Torchic | Gardenia | 77% | 76% |
| Torracat | Gardenia | 99% | 77% |
| Treecko | Gardenia | 89% | 44% |
| Tropius | Gardenia | 83% | 67% |
| Wooloo | Gardenia | 77% | 27% |
| Wormadam | Gardenia | 63% | 64% |
| Zubat | Gardenia | 85% | 40% |
| Carnivine | Fantina | 70% | 45% |
| Ceruledge | Fantina | 82% | 45% |
| Drifblim | Fantina | 99% | 36% |
| Gabite | Fantina | 82% | 63% |
| Gastly | Fantina | 79% | 52% |
| Golduck | Fantina | 82% | 45% |
| Haunter | Fantina | 87% | 59% |
| Honchkrow | Fantina | 84% | 56% |
| Lanturn | Fantina | 68% | 48% |
| Leafeon | Fantina | 87% | 47% |
| Leavanny | Fantina | 84% | 29% |
| Lumineon | Fantina | 84% | 28% |
| Luxray | Fantina | 87% | 62% |
| Magmar | Fantina | 86% | 57% |
| Mantine | Fantina | 70% | 34% |
| Milotic | Fantina | 79% | 38% |
| Orbeetle | Fantina | 84% | 42% |
| Roselia | Fantina | 63% | 26% |
| Rotom | Fantina | 84% | 49% |
| Seaking | Fantina | 68% | 26% |
| Sinistcha | Fantina | 70% | 48% |
| Smoochum | Fantina | 63% | 36% |
| Tentacruel | Fantina | 93% | 42% |
| Toucannon | Fantina | 55% | 62% |
| Tsareena | Fantina | 84% | 48% |
| Wailmer | Fantina | 55% | 39% |
| Whiscash | Fantina | 55% | 59% |
| Abra | Maylene | 84% | 50% |
| Altaria | Maylene | 68% | 54% |
| Decidueye | Maylene | 55% | 28% |
| Dewgong | Maylene | 55% | 44% |
| Elekid | Maylene | 89% | 31% |
| Glimmora | Maylene | 76% | 46% |
| Ludicolo | Maylene | 55% | 60% |
| Mankey | Maylene | 55% | 36% |
| Medicham | Maylene | 68% | 87% |
| Misdreavus | Maylene | 76% | 33% |
| Poliwrath | Maylene | 84% | 60% |
| Qwilfish | Maylene | 76% | 38% |
| Skuntank | Maylene | 75% | 48% |
| Staryu | Maylene | 76% | 30% |
| Vibrava | Maylene | 95% | 58% |
| Yanma | Maylene | 89% | 27% |
| Yanmega | Maylene | 89% | 55% |
| Armarouge | Wake | 61% | 42% |
| Chandelure | Wake | 68% | 46% |
| Corviknight | Wake | 52% | 36% |
| Drapion | Wake | 81% | 30% |
| Flareon | Wake | 50% | 53% |
| Floragato | Wake | 69% | 25% |
| Florges | Wake | 61% | 29% |
| Galarian Mr Mime | Wake | 83% | 34% |
| Glalie | Wake | 83% | 42% |
| Gliscor | Wake | 81% | 33% |
| Gothitelle | Wake | 50% | 28% |
| Kingdra | Wake | 72% | 37% |
| Manaphy | Wake | 83% | 39% |
| Mr Mime | Wake | 77% | 53% |
| Mr Rime | Wake | 56% | 50% |
| Politoed | Wake | 77% | 42% |
| Roserade | Wake | 77% | 58% |
| Scizor | Wake | 50% | 44% |
| Seadra | Wake | 72% | 37% |
| Walrein | Wake | 50% | 43% |

A further 5 stages would trip a flag or pass the bar only with the moves a first proposal gave them, so they are proposed again as held: Dhelmise, Grapploct, Klefki, Polteageist, Primarina.

## Strong moves that come sooner

Every good attack or S or SSS status move that the proposal gives a stage a split or more sooner than now, or new before Byron's split: 105 in all. These are the entries to read as a player would. A stage marked held is flagged or over the bar, so its entry here is a new move no earlier than its first good one of that type.

| Stage | Move | Now | Proposed | Held |
|---|---|---|---|---|
| Anorith | Rock Blast | 49 | 44 |  |
| Anorith | X-Scissor | 61 | 53 |  |
| Armaldo | X-Scissor | 73 | 57 |  |
| Azurill | Bounce | not learnt | 26 |  |
| Bastiodon | Iron Head | 52 | 44 |  |
| Bonsly | Wood Hammer | not learnt | 34 |  |
| Bronzor | Iron Head | not learnt | 20 |  |
| Bronzor | Zen Headbutt | not learnt | 31 |  |
| Cherrim | Leaf Blade | not learnt | 39 | yes |
| Chimecho | Recover | not learnt | 34 | yes |
| Clobbopus | Superpower | 45 | 44 |  |
| Clodsire | Earthquake | 48 | 44 |  |
| Cresselia | Psychic | 93 | 74 |  |
| Croconaw | Superpower | 51 | 44 |  |
| Dewpider | Hydro Pump | 45 | 32 |  |
| Duskull | Future Sight | 46 | 26 |  |
| Ferroseed | Seed Bomb | 47 | 32 |  |
| Ferroseed | Iron Head | 52 | 33 |  |
| Flaaffy | Thunderbolt | not learnt | 44 | yes |
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
| Hoothoot | Hyper Voice | not learnt | 39 | yes |
| Hoppip | Seed Bomb | not learnt | 32 | yes |
| Incineroar | Flare Blitz | 55 | 53 |  |
| Joltik | Bug Buzz | 48 | 39 |  |
| Joltik | Thunderbolt | 45 | 41 |  |
| Kabuto | Muddy Water | not learnt | 32 |  |
| Koffing | Sludge Bomb | 42 | 26 |  |
| Kommo O | Close Combat | 65 | 53 |  |
| Larvitar | Earthquake | 41 | 39 |  |
| Lickilicky | Sludge Bomb | not learnt | 39 |  |
| Lickilicky | Power Whip | 49 | 44 |  |
| Lickitung | Body Slam | not learnt | 30 |  |
| Lickitung | Power Whip | 49 | 44 |  |
| Lunatone | Psychic | 45 | 39 |  |
| Magneton | Discharge | 40 | 39 |  |
| Magneton | Flash Cannon | not learnt | 44 |  |
| Magnezone | Flash Cannon | not learnt | 44 |  |
| Mareep | Thunderbolt | not learnt | 39 | yes |
| Mawile | Thunder Fang | not learnt | 39 |  |
| Mawile | Ice Fang | not learnt | 44 |  |
| Metang | Iron Head | not learnt | 31 |  |
| Metang | Zen Headbutt | 52 | 33 |  |
| Minun | Thunderbolt | not learnt | 43 | yes |
| Murkrow | Dark Pulse | not learnt | 44 | yes |
| Nacli | Stone Edge | 45 | 32 |  |
| Nidoran F | Toxic | not learnt | 32 | yes |
| Noctowl | Hyper Voice | not learnt | 44 | yes |
| Omanyte | Earth Power | not learnt | 44 |  |
| Pachirisu | Thunder Fang | not learnt | 32 | yes |
| Pheromosa | Hi Jump Kick | 70 | 26 |  |
| Pheromosa | Bug Buzz | 60 | 44 |  |
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
| Seel | Ice Beam | 47 | 44 |  |
| Sentret | Hyper Voice | 47 | 33 |  |
| Shieldon | Earthquake | not learnt | 34 |  |
| Shieldon | Iron Head | 43 | 39 |  |
| Sinistea | Shadow Ball | 48 | 33 |  |
| Slowbro | Psychic | 54 | 44 |  |
| Slowking | Psychic | 48 | 44 |  |
| Slowpoke | Body Slam | not learnt | 26 |  |
| Slowpoke | Zen Headbutt | 34 | 30 |  |
| Slowpoke | Dive | not learnt | 33 |  |
| Slowpoke | Psychic | 48 | 44 |  |
| Solrock | Zen Headbutt | not learnt | 38 |  |
| Solrock | Earthquake | not learnt | 39 |  |
| Spiritomb | Dark Pulse | 49 | 38 |  |
| Spiritomb | Earth Power | not learnt | 44 |  |
| Sudowoodo | Earthquake | not learnt | 39 |  |
| Sudowoodo | Hammer Arm | 49 | 40 |  |
| Swablu | Air Slash | not learnt | 44 |  |
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

282 delays pass Ian's tests on the proposed lists (a strong move past the evolution level, the evolved stage a split and five levels later or never, nothing like it between). The wait is given in splits past the one the stage can evolve in.

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
| Bonsly | Sudowoodo | Wood Hammer | 34 | 1 | never |
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
| Clobbopus | Grapploct | Superpower | 44 | 2 | 72 |
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
| Eevee | Espeon | Take Down | 43 | 0 | never |
| Eevee | Sylveon | Take Down | 43 | 2 | never |
| Ekans | Arbok | Gunk Shot | 41 | 3 | 56 |
| Electabuzz | Electivire | Thunderbolt | 53 | 3 | never |
| Elekid | Electabuzz | Thunderbolt | 39 | 1 | 53 |
| Exeggcute | Exeggutor | Psychic | 47 | 4 | never |
| Fletchling | Fletchinder | Defog | 33 | 2 | never |
| Floette | Florges | Moonblast | 52 | 1 | 57 |
| Floragato | Meowscarada | Play Rough | 42 | 1 | 47 |
| Fomantis | Lurantis | Leaf Blade | 39 | 0 | 44 |
| Gabite | Garchomp | Dragon Rush | 70 | 5 | never |
| Gible | Gabite | Dig | 31 | 1 | 40 |
| Gible | Gabite | Dragon Rush | 60 | 6 | 70 |
| Golbat | Crobat | Brave Bird | 53 | 1 | 63 |
| Goldeen | Seaking | Megahorn | 51 | 3 | 63 |
| Goomy | Hisuian Sliggoo | Body Slam | 41 | 3 | never |
| Goomy | Sliggoo | Dragon Pulse | 44 | 0 | 55 |
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
| Houndour | Houndoom | Crunch | 48 | 4 | 54 |
| Houndour | Houndoom | Nasty Plot | 53 | 4 | 60 |
| Jigglypuff | Wigglytuff | Body Slam | 29 | 1 | never |
| Jigglypuff | Wigglytuff | Hyper Voice | 45 | 4 | never |
| Jigglypuff | Wigglytuff | Double-Edge | 49 | 4 | never |
| Joltik | Galvantula | Discharge | 38 | 1 | 48 |
| Joltik | Galvantula | Bug Buzz | 39 | 1 | 51 |
| Joltik | Galvantula | Thunderbolt | 41 | 2 | 48 |
| Joltik | Galvantula | Energy Ball | 44 | 2 | 53 |
| Kirlia | Gardevoir | Psychic | 38 | 1 | 44 |
| Kirlia | Gallade | Psychic | 38 | 1 | never |
| Kirlia | Gardevoir | Future Sight | 39 | 1 | 45 |
| Kirlia | Gallade | Future Sight | 39 | 1 | never |
| Krabby | Kingler | Slam | 35 | 1 | 44 |
| Krabby | Kingler | Crabhammer | 41 | 2 | 56 |
| Lairon | Aggron | Double-Edge | 51 | 1 | 57 |
| Lampent | Chandelure | Shadow Ball | 55 | 2 | 65 |
| Lampent | Chandelure | Heat Wave | 65 | 4 | 72 |
| Larvesta | Volcarona | Double-Edge | 72 | 4 | never |
| Larvitar | Pupitar | Stone Edge | 46 | 3 | 54 |
| Ledyba | Ledian | Double-Edge | 38 | 2 | 48 |
| Ledyba | Ledian | Bug Buzz | 41 | 3 | 53 |
| Lileep | Cradily | Energy Ball | 50 | 1 | 56 |
| Litten | Torracat | Fire Fang | 33 | 2 | 38 |
| Lombre | Ludicolo | Hydro Pump | 45 | 2 | never |
| Lotad | Lombre | Energy Ball | 45 | 5 | never |
| Loudred | Exploud | Hyper Voice | 57 | 3 | 63 |
| Luxio | Luxray | Thunder Fang | 33 | 0 | 53 |
| Magikarp | Gyarados | Bounce | 63 | 7 | never |
| Makuhita | Hariyama | Close Combat | 44 | 3 | 72 |
| Makuhita | Hariyama | Shadow Punch | 53 | 4 | never |
| Mankey | Primeape | Close Combat | 49 | 3 | 59 |
| Mareep | Flaaffy | Thunderbolt | 39 | 3 | 44 |
| Marill | Azumarill | Aqua Tail | 37 | 2 | 47 |
| Marill | Azumarill | Hydro Pump | 42 | 3 | 47 |
| Marshtomp | Swampert | Earthquake | 46 | 2 | 56 |
| Meditite | Medicham | Recover | 46 | 2 | 55 |
| Meowth | Persian | Nasty Plot | 38 | 1 | 44 |
| Mienfoo | Mienshao | Hi Jump Kick | 58 | 4 | 64 |
| Minccino | Cinccino | Hyper Voice | 43 | 0 | never |
| Misdreavus | Mismagius | Shadow Ball | 37 | 1 | never |
| Monferno | Infernape | Slack Off | 46 | 2 | never |
| Monferno | Infernape | Flare Blitz | 49 | 2 | 57 |
| Murkrow | Honchkrow | Taunt | 31 | 0 | never |
| Murkrow | Honchkrow | Assurance | 32 | 0 | never |
| Nacli | Naclstack | Recover | 25 | 0 | 30 |
| Nacli | Naclstack | Stone Edge | 32 | 1 | 51 |
| Nacli | Naclstack | Earthquake | 40 | 3 | 53 |
| Natu | Xatu | Future Sight | 36 | 2 | 42 |
| Nidoran F | Nidorina | Toxic | 32 | 2 | never |
| Nidoran F | Nidorina | Poison Fang | 45 | 5 | 58 |
| Nidoran M | Nidorino | Poison Jab | 37 | 3 | 43 |
| Nidorina | Nidoqueen | Toxic Spikes | 35 | 2 | never |
| Nidorina | Nidoqueen | Poison Fang | 58 | 6 | never |
| Nidorino | Nidoking | Toxic Spikes | 35 | 2 | never |
| Nidorino | Nidoking | Poison Jab | 43 | 3 | never |
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
| Poliwhirl | Politoed | Hydro Pump | 48 | 1 | never |
| Ponyta | Rapidash | Bounce | 42 | 0 | 47 |
| Ponyta | Rapidash | Flare Blitz | 46 | 1 | 56 |
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
| Sewaddle | Swadloon | Bug Buzz | 44 | 3 | never |
| Shelgon | Salamence | Dragon Claw | 55 | 1 | 61 |
| Shelgon | Salamence | Double-Edge | 61 | 3 | 70 |
| Shellder | Cloyster | Ice Beam | 49 | 2 | never |
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
| Slowpoke | Slowbro | Slack Off | 53 | 2 | 76 |
| Slugma | Magcargo | Flamethrower | 53 | 2 | 61 |
| Slugma | Magcargo | Earth Power | 56 | 3 | 66 |
| Smoochum | Jynx | Psychic | 35 | 1 | never |
| Smoochum | Jynx | Blizzard | 45 | 3 | 55 |
| Snorunt | Froslass | Ice Fang | 28 | 0 | 60 |
| Snover | Abomasnow | Blizzard | 41 | 0 | 47 |
| Spearow | Fearow | Roost | 33 | 1 | 41 |
| Spearow | Fearow | Drill Peck | 37 | 2 | 47 |
| Spinarak | Ariados | Psychic | 40 | 3 | 46 |
| Spinarak | Ariados | Poison Jab | 43 | 3 | 50 |
| Spoink | Grumpig | Psychic | 41 | 2 | 47 |
| Spoink | Grumpig | Bounce | 48 | 3 | 60 |
| Sprigatito | Floragato | Seed Bomb | 18 | 1 | 36 |
| Starly | Staravia | Brave Bird | 44 | 4 | 53 |
| Staryu | Starmie | Recover | 44 | 1 | never |
| Staryu | Starmie | Hydro Pump | 55 | 3 | never |
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
| Torracat | Incineroar | Flamethrower | 38 | 0 | 53 |
| Torracat | Incineroar | Fire Fang | 39 | 0 | 53 |
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
| Trumbeak | Toucannon | Drill Peck | 32 | 0 | 53 |
| Trumbeak | Toucannon | Hyper Voice | 45 | 3 | 56 |
| Turtwig | Grotle | Giga Drain | 41 | 3 | 47 |
| Venonat | Venomoth | Poison Fang | 41 | 2 | 47 |
| Venonat | Venomoth | Psychic | 47 | 3 | 55 |
| Vullaby | Mandibuzz | Brave Bird | 65 | 2 | 72 |
| Wailmer | Wailord | Dive | 41 | 0 | 46 |
| Wailmer | Wailord | Bounce | 44 | 0 | 54 |
| Wailmer | Wailord | Water Spout | 78 | 7 | never |
| Wartortle | Blastoise | Hydro Pump | 48 | 2 | 60 |
| Weepinbell | Victreebel | Slam | 41 | 3 | never |
| Whismur | Loudred | Hyper Voice | 45 | 4 | 57 |
| Wingull | Pelipper | Roost | 29 | 1 | 53 |
| Wingull | Pelipper | Air Slash | 47 | 4 | never |
| Wooloo | Dubwool | Double-Edge | 40 | 3 | 50 |
| Wooper | Clodsire | Slam | 15 | 0 | 37 |
| Wooper | Quagsire | Muddy Water | 30 | 1 | 53 |
| Wooper | Clodsire | Muddy Water | 30 | 2 | never |
| Wooper | Quagsire | Sludge Bomb | 33 | 1 | never |
| Wooper | Clodsire | Sludge Bomb | 33 | 2 | never |
| Wooper | Quagsire | Earthquake | 39 | 2 | 44 |
| Wooper | Clodsire | Earthquake | 39 | 3 | 44 |
| Yanma | Yanmega | Air Slash | 54 | 3 | never |
| Zigzagoon | Linoone | Belly Drum | 41 | 3 | 53 |
| Zubat | Golbat | Poison Fang | 33 | 1 | 39 |
| Zubat | Golbat | Air Slash | 41 | 3 | 51 |

## The three analyses

On Oxide's lists now and on the proposal, the same readings as the first generator's:

| Reading | Kaizo | Oxide now | The proposal |
|---|---|---|---|
| Pre-evolutions that reward a wait of a split or less | 124 | 63 | 70 |
| Moves only a Pokemon kept from evolving gets | 334 | 259 | 282 |
| Of those, strong | 148 | 41 | 59 |
| Wild slots that can end the encounter | | 153 | 138 |
| Wild slots that can knock themselves out | | 261 | 235 |
| Wild slots with a better version later | | 9 | 6 |
| Evolved catches with no good move by the split's cap | | 70 | 76 |

The share of catches with a good move known at capture or learnt by level-up before the split's cap:

| Split | Oxide now | The proposal |
|---|---|---|
| Roark | 0.08 | 0.06 |
| Gardenia | 0.26 | 0.22 |
| Fantina | 0.54 | 0.70 |
| Maylene | 0.74 | 0.67 |
| Wake | 0.88 | 0.86 |
| Byron | 0.88 | 0.90 |
| Candice | 0.90 | 0.90 |
| Galactic | 0.93 | 0.94 |
| Volkner | 0.86 | 0.86 |
| Barry | 0.93 | 0.93 |

## The checks

Every family's check list, totalled over all of them:

| Check | Failures |
|---|---|
| Nothing new past 78 | 0 |
| No weather move | 0 |
| No cut move | 0 |
| No dead weight added | 0 |
| No weak attack later than now | 0 |
| No strong move earlier than now on a strong stage, nor any S or SSS status move | 0 |
| No two moves on one level that the method placed | 0 |
| No strong move placed earlier than Kaizo's level within its split | 0 |
| No stage more than one split without an attack of its own type of 50 or more | 0 |
| No move that ends a wild encounter moved into the wild levels | 0 |

The own-type rule keeps 1 moves at their current level, where the proposal would have left a stage more than one split without an attack of its own type of 50 or more:

| Stage | Move | In the list of | Kept at |
|---|---|---|---|
| Hippopotas | Earthquake | Hippopotas | 37 |

For Ian: 11 such moves would reach a stage the power flags or the bar hold, so they are not kept until he rules; the stages they are for go without an attack of their own type meanwhile:

| Move | In the list of | Its level now | For | Would reach |
|---|---|---|---|---|
| Air Slash | Beautifly | 26 | Beautifly | Beautifly |
| Scald | Brionne | 34 | Brionne | Brionne, Primarina |
| Hyper Voice | Delcatty | 35 | Delcatty | Delcatty |
| Leaf Blade | Grovyle | 29 | Grovyle, Sceptile | Grovyle, Sceptile |
| Earthquake | Hippowdon | 40 | Hippowdon | Hippowdon |
| Fire Fang | Litten | 14 | Torracat | Litten, Torracat |
| Earth Power | Nidoking | 43 | Nidoking | Nidoking |
| Earth Power | Nidoqueen | 43 | Nidoqueen | Nidoqueen |
| Thunderbolt | Pikachu | 26 | Pikachu | Pikachu, Raichu |
| Shadow Ball | Polteageist | 48 | Polteageist | Polteageist |
| Bullet Seed | Skiploom | 20 | Jumpluff, Skiploom | Skiploom, Jumpluff |

62 stages go more than one split without an attack of their own type on Oxide's lists now, and the proposal does not make it longer (stages the player can evolve by the end of Gardenia's split are exempt); the later-moves proposal fills them where a later game offers one: Alolan Ninetales, Alomomola, Braixen, Budew, Carnivine, Charcadet, Charmeleon, Clefable, Cradily, Croconaw, Delibird, Dhelmise, Donphan, Drifloon, Duskull, Dustox, Feebas, Feraligatr, Flaaffy, Floatzel, Glaceon, Gligar, Gliscor, Granbull, Gyarados, Happiny, Hippopotas, Kabuto, Kabutops, Lileep, Lopunny, Lunatone, Luvdisc, Magby, Masquerain, Mawile, Misdreavus, Mismagius, Munchlax, Qwilfish, Raboot, Roselia, Seel, Shellder, Shiftry, Slugma, Solrock, Staryu, Steelix, Swablu, Sylveon, Tangela, Tangrowth, Togekiss, Togetic, Trapinch, Umbreon, Unown, Vaporeon, Wartortle, Yanma, Yanmega.

Where Kaizo's own level is past Oxide's 78, the rule would take the move out of play, against the rule that nothing goes past 78, so these 18 keep their translated place for Ian to decide:

| Stage | Move | Kaizo's level | Kept at |
|---|---|---|---|
| Articuno | Roost | 85 | 69 |
| Cresselia | Psychic | 93 | 74 |
| Crobat | Brave Bird | 80 | 63 |
| Frogadier | Hydro Pump | 95 | 75 |
| Gabite | Dragon Rush | 88 | 70 |
| Giratina | Shadow Claw | 80 | 63 |
| Grapploct | Superpower | 90 | 72 |
| Hariyama | Close Combat | 90 | 72 |
| Houndoom | Will-O-Wisp | 90 | 72 |
| Magikarp | Bounce | 80 | 63 |
| Moltres | Roost | 85 | 69 |
| Regirock | Superpower | 81 | 64 |
| Registeel | Superpower | 81 | 64 |
| Shroomish | Spore | 100 | 78 |
| Slowbro | Slack Off | 97 | 76 |
| Trapinch | Superpower | 89 | 71 |
| Wailmer | Water Spout | 100 | 78 |
| Zapdos | Roost | 85 | 69 |

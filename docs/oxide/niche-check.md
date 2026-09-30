# The niche check

Written by `niche.py` (2026-09-28) for Ian's ruling of the same day: every Pokemon should have an important niche at the point the player has it, while stronger and weaker lines stay fine. Nothing here is in the game data. Each of the 455 stages the player can own is read in the split it is first owned in, at that split's cap, with the moves it can have by then, against every trainer Pokemon of that split, by the calculator the scores use. Five roles: offense (the mean share of a foe's HP its best move takes), speed (the share of foes it outspeeds), physical wall and special wall (of the foes whose best attack on it is of that kind, the share that need three or more hits on it while it needs three or fewer on them, since a bulky stage with nothing to attack with is no wall) and status (its best status move by Ian's tiers). Each is ranked against every stage the player can own by that split; its standing is the mean of its five ranks, 0.5 being the split's average. A stage has a niche when one role, or its standing (an all-rounder), puts it in the split's top quarter. Two readings: Oxide's lists today, and the proposal (the learnset proposal with the later moves placed). `docs/oxide/niche-check.tsv` has every stage's numbers.

| Stages without a niche | Held past their first split | Evolve within it |
|---|---|---|
| On both readings | 59 | 64 |
| Today only (the proposal gives one) | 7 | 2 |
| On the proposal only (it takes one away) | 4 | 1 |

1 stages held past their first split have a niche on the proposal only as all-rounders, good at much and best at nothing; without that niche they would be findings: Surskit.

## No niche on either reading

Stages the player can evolve within the split they are first owned in are held only briefly; they are marked. Each role's rank on the proposal, the best first:

| Stage | First owned | Evolves within it | Offense | Speed | Physical wall | Special wall | Status | Standing |
|---|---|---|---|---|---|---|---|---|
| Budew | Roark |  | 0.08 | 0.39 | 0.06 | 0.04 | 0.73 | 0.26 |
| Dustox | Roark |  | 0.56 | 0.64 | 0.50 | 0.72 | 0.28 | 0.54 |
| Finneon | Roark |  | 0.26 | 0.64 | 0.52 | 0.01 | 0.73 | 0.43 |
| Goldeen | Roark |  | 0.27 | 0.56 | 0.38 | 0.33 | 0.28 | 0.36 |
| Grubbin | Roark |  | 0.41 | 0.39 | 0.33 | 0.72 | 0.28 | 0.43 |
| Luxio | Roark |  | 0.60 | 0.50 | 0.46 | 0.72 | 0.28 | 0.51 |
| Nidorina | Roark |  | 0.37 | 0.39 | 0.73 | 0.72 | 0.28 | 0.50 |
| Nosepass | Roark |  | 0.29 | 0.15 | 0.26 | 0.40 | 0.28 | 0.28 |
| Nuzleaf | Roark |  | 0.04 | 0.50 | 0.10 | 0.28 | 0.62 | 0.30 |
| Pawmi | Roark |  | 0.12 | 0.50 | 0.11 | 0.72 | 0.28 | 0.34 |
| Poochyena | Roark |  | 0.45 | 0.22 | 0.33 | 0.72 | 0.73 | 0.49 |
| Sewaddle | Roark |  | 0.44 | 0.27 | 0.17 | 0.35 | 0.28 | 0.30 |
| Skitty | Roark |  | 0.18 | 0.39 | 0.17 | 0.38 | 0.73 | 0.37 |
| Smoliv | Roark |  | 0.21 | 0.15 | 0.64 | 0.72 | 0.28 | 0.40 |
| Steenee | Roark |  | 0.28 | 0.56 | 0.64 | 0.72 | 0.62 | 0.56 |
| Vullaby | Roark |  | 0.50 | 0.50 | 0.22 | 0.72 | 0.62 | 0.51 |
| Wooloo | Roark |  | 0.17 | 0.39 | 0.59 | 0.22 | 0.62 | 0.40 |
| Zubat | Roark |  | 0.19 | 0.39 | 0.30 | 0.72 | 0.28 | 0.38 |
| Carbink | Gardenia |  | 0.23 | 0.39 | 0.63 | 0.26 | 0.60 | 0.42 |
| Dolliv | Gardenia |  | 0.12 | 0.14 | 0.15 | 0.32 | 0.05 | 0.16 |
| Flaaffy | Gardenia |  | 0.39 | 0.32 | 0.68 | 0.61 | 0.43 | 0.49 |
| Kabuto | Gardenia |  | 0.55 | 0.47 | 0.33 | 0.14 | 0.43 | 0.38 |
| Mantyke | Gardenia |  | 0.33 | 0.39 | 0.40 | 0.27 | 0.43 | 0.36 |
| Omanyte | Gardenia |  | 0.40 | 0.19 | 0.33 | 0.14 | 0.20 | 0.25 |
| Shellos | Gardenia |  | 0.18 | 0.14 | 0.35 | 0.16 | 0.20 | 0.21 |
| Snorunt | Gardenia |  | 0.50 | 0.39 | 0.52 | 0.57 | 0.60 | 0.52 |
| Swadloon | Gardenia |  | 0.36 | 0.28 | 0.19 | 0.69 | 0.60 | 0.43 |
| Swinub | Gardenia |  | 0.59 | 0.39 | 0.61 | 0.52 | 0.43 | 0.51 |
| Alomomola | Fantina |  | 0.31 | 0.57 | 0.55 | 0.35 | 0.13 | 0.38 |
| Chansey | Fantina |  | 0.03 | 0.36 | 0.05 | 0.02 | 0.63 | 0.22 |
| Fomantis | Fantina |  | 0.08 | 0.18 | 0.07 | 0.15 | 0.17 | 0.13 |
| Glaceon | Fantina |  | 0.14 | 0.57 | 0.33 | 0.58 | 0.63 | 0.45 |
| Klefki | Fantina |  | 0.09 | 0.70 | 0.38 | 0.25 | 0.13 | 0.31 |
| Mantine | Fantina |  | 0.45 | 0.66 | 0.49 | 0.64 | 0.63 | 0.57 |
| Milotic | Fantina |  | 0.20 | 0.75 | 0.36 | 0.19 | 0.63 | 0.43 |
| Roselia | Fantina |  | 0.46 | 0.57 | 0.57 | 0.44 | 0.63 | 0.54 |
| Sandygast | Fantina |  | 0.55 | 0.01 | 0.69 | 0.26 | 0.11 | 0.32 |
| Seaking | Fantina |  | 0.36 | 0.66 | 0.41 | 0.38 | 0.63 | 0.49 |
| Seel | Fantina |  | 0.21 | 0.30 | 0.32 | 0.53 | 0.63 | 0.40 |
| Stunky | Fantina |  | 0.33 | 0.69 | 0.35 | 0.42 | 0.63 | 0.48 |
| Swablu | Fantina |  | 0.06 | 0.36 | 0.15 | 0.23 | 0.63 | 0.29 |
| Wailmer | Fantina |  | 0.65 | 0.50 | 0.50 | 0.58 | 0.63 | 0.57 |
| Yamask | Fantina |  | 0.10 | 0.10 | 0.39 | 0.60 | 0.23 | 0.28 |
| Arboliva | Maylene |  | 0.42 | 0.22 | 0.62 | 0.57 | 0.17 | 0.40 |
| Decidueye | Maylene |  | 0.45 | 0.62 | 0.56 | 0.67 | 0.17 | 0.49 |
| Floette | Maylene |  | 0.25 | 0.39 | 0.27 | 0.43 | 0.17 | 0.30 |
| Frillish | Maylene |  | 0.13 | 0.22 | 0.18 | 0.59 | 0.17 | 0.26 |
| Gothorita | Maylene |  | 0.35 | 0.41 | 0.69 | 0.63 | 0.12 | 0.44 |
| Lurantis | Maylene |  | 0.37 | 0.28 | 0.64 | 0.54 | 0.17 | 0.40 |
| Toxapex | Maylene |  | 0.06 | 0.17 | 0.53 | 0.45 | 0.63 | 0.37 |
| Unown | Maylene |  | 0.00 | 0.31 | 0.00 | 0.00 | 0.04 | 0.07 |
| Chandelure | Wake |  | 0.65 | 0.69 | 0.56 | 0.52 | 0.21 | 0.53 |
| Jellicent | Wake |  | 0.17 | 0.47 | 0.63 | 0.72 | 0.14 | 0.43 |
| Kabutops | Wake |  | 0.70 | 0.69 | 0.74 | 0.54 | 0.63 | 0.66 |
| Palossand | Wake |  | 0.50 | 0.16 | 0.58 | 0.37 | 0.14 | 0.35 |
| Sliggoo | Wake |  | 0.16 | 0.47 | 0.48 | 0.71 | 0.06 | 0.38 |
| Larvesta | Byron |  | 0.19 | 0.46 | 0.32 | 0.32 | 0.02 | 0.26 |
| Lunatone | Byron |  | 0.68 | 0.60 | 0.68 | 0.53 | 0.64 | 0.63 |
| Mandibuzz | Candice |  | 0.12 | 0.70 | 0.44 | 0.60 | 0.22 | 0.41 |
| Bidoof | Roark | yes | 0.09 | 0.15 | 0.14 | 0.72 | 0.28 | 0.27 |
| Blipbug | Roark | yes | 0.03 | 0.31 | 0.01 | 0.03 | 0.28 | 0.13 |
| Bounsweet | Roark | yes | 0.16 | 0.15 | 0.49 | 0.72 | 0.62 | 0.43 |
| Cascoon | Roark | yes | 0.06 | 0.01 | 0.08 | 0.07 | 0.28 | 0.10 |
| Fletchling | Roark | yes | 0.36 | 0.56 | 0.22 | 0.72 | 0.28 | 0.43 |
| Kricketot | Roark | yes | 0.04 | 0.09 | 0.04 | 0.07 | 0.28 | 0.10 |
| Lotad | Roark | yes | 0.13 | 0.15 | 0.04 | 0.72 | 0.73 | 0.35 |
| Mudkip | Roark | yes | 0.30 | 0.27 | 0.64 | 0.11 | 0.28 | 0.32 |
| Nidoran F | Roark | yes | 0.23 | 0.27 | 0.55 | 0.72 | 0.28 | 0.41 |
| Piplup | Roark | yes | 0.35 | 0.27 | 0.64 | 0.28 | 0.28 | 0.36 |
| Rookidee | Roark | yes | 0.32 | 0.39 | 0.30 | 0.72 | 0.28 | 0.40 |
| Seedot | Roark | yes | 0.01 | 0.15 | 0.01 | 0.01 | 0.62 | 0.16 |
| Sentret | Roark | yes | 0.25 | 0.05 | 0.17 | 0.72 | 0.62 | 0.36 |
| Shinx | Roark | yes | 0.61 | 0.31 | 0.46 | 0.72 | 0.28 | 0.47 |
| Silcoon | Roark | yes | 0.06 | 0.01 | 0.08 | 0.07 | 0.28 | 0.10 |
| Snivy | Roark | yes | 0.10 | 0.56 | 0.36 | 0.11 | 0.28 | 0.28 |
| Squirtle | Roark | yes | 0.37 | 0.31 | 0.68 | 0.14 | 0.28 | 0.35 |
| Wurmple | Roark | yes | 0.15 | 0.05 | 0.08 | 0.36 | 0.28 | 0.18 |
| Burmy | Gardenia | yes | 0.03 | 0.19 | 0.10 | 0.03 | 0.60 | 0.19 |
| Cherubi | Gardenia | yes | 0.13 | 0.19 | 0.05 | 0.17 | 0.60 | 0.23 |
| Clamperl | Gardenia | yes | 0.05 | 0.13 | 0.13 | 0.03 | 0.60 | 0.19 |
| Combee | Gardenia | yes | 0.32 | 0.64 | 0.14 | 0.67 | 0.05 | 0.36 |
| Dewpider | Gardenia | yes | 0.60 | 0.07 | 0.46 | 0.50 | 0.20 | 0.36 |
| Hoothoot | Gardenia | yes | 0.45 | 0.39 | 0.30 | 0.59 | 0.60 | 0.47 |
| Hoppip | Gardenia | yes | 0.37 | 0.39 | 0.17 | 0.32 | 0.60 | 0.37 |
| Mareep | Gardenia | yes | 0.22 | 0.19 | 0.30 | 0.42 | 0.43 | 0.31 |
| Marill | Gardenia | yes | 0.09 | 0.24 | 0.43 | 0.18 | 0.20 | 0.23 |
| Rowlet | Gardenia | yes | 0.65 | 0.28 | 0.35 | 0.47 | 0.60 | 0.47 |
| Torchic | Gardenia | yes | 0.38 | 0.32 | 0.54 | 0.57 | 0.43 | 0.45 |
| Treecko | Gardenia | yes | 0.28 | 0.64 | 0.08 | 0.34 | 0.43 | 0.36 |
| Azurill | Fantina | yes | 0.48 | 0.04 | 0.34 | 0.15 | 0.63 | 0.33 |
| Bonsly | Fantina | yes | 0.57 | 0.01 | 0.71 | 0.32 | 0.63 | 0.45 |
| Charcadet | Fantina | yes | 0.07 | 0.18 | 0.23 | 0.36 | 0.23 | 0.21 |
| Eevee | Fantina | yes | 0.15 | 0.43 | 0.18 | 0.48 | 0.63 | 0.38 |
| Happiny | Fantina | yes | 0.01 | 0.10 | 0.01 | 0.00 | 0.63 | 0.15 |
| Joltik | Fantina | yes | 0.11 | 0.57 | 0.19 | 0.26 | 0.13 | 0.25 |
| Kirlia | Fantina | yes | 0.35 | 0.36 | 0.20 | 0.27 | 0.63 | 0.36 |
| Ralts | Fantina | yes | 0.20 | 0.23 | 0.05 | 0.11 | 0.63 | 0.24 |
| Salandit | Fantina | yes | 0.44 | 0.72 | 0.50 | 0.23 | 0.63 | 0.50 |
| Sinistea | Fantina | yes | 0.40 | 0.36 | 0.26 | 0.41 | 0.17 | 0.32 |
| Smoochum | Fantina | yes | 0.34 | 0.57 | 0.02 | 0.19 | 0.63 | 0.35 |
| Snom | Fantina | yes | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 |
| Totodile | Fantina | yes | 0.65 | 0.28 | 0.66 | 0.49 | 0.63 | 0.54 |
| Croagunk | Maylene | yes | 0.55 | 0.35 | 0.25 | 0.17 | 0.63 | 0.39 |
| Floragato | Maylene | yes | 0.17 | 0.73 | 0.31 | 0.32 | 0.08 | 0.32 |
| Gothita | Maylene | yes | 0.19 | 0.28 | 0.21 | 0.24 | 0.12 | 0.21 |
| Mankey | Maylene | yes | 0.57 | 0.62 | 0.10 | 0.11 | 0.63 | 0.41 |
| Mareanie | Maylene | yes | 0.04 | 0.28 | 0.30 | 0.22 | 0.63 | 0.29 |
| Slowpoke | Maylene | yes | 0.48 | 0.03 | 0.45 | 0.31 | 0.63 | 0.38 |
| Trapinch | Maylene | yes | 0.69 | 0.01 | 0.15 | 0.12 | 0.63 | 0.32 |
| Clobbopus | Wake | yes | 0.27 | 0.13 | 0.14 | 0.07 | 0.63 | 0.25 |
| Ferroseed | Wake | yes | 0.20 | 0.01 | 0.58 | 0.69 | 0.08 | 0.31 |
| Goomy | Wake | yes | 0.04 | 0.22 | 0.17 | 0.22 | 0.06 | 0.14 |
| Horsea | Wake | yes | 0.25 | 0.47 | 0.25 | 0.06 | 0.63 | 0.33 |
| Lampent | Wake | yes | 0.35 | 0.40 | 0.40 | 0.39 | 0.21 | 0.35 |
| Mime Jr | Wake | yes | 0.51 | 0.47 | 0.11 | 0.29 | 0.63 | 0.40 |
| Sealeo | Wake | yes | 0.35 | 0.28 | 0.69 | 0.58 | 0.63 | 0.51 |
| Skorupi | Wake | yes | 0.09 | 0.54 | 0.36 | 0.13 | 0.63 | 0.35 |
| Spheal | Wake | yes | 0.20 | 0.07 | 0.23 | 0.23 | 0.63 | 0.27 |
| Hakamo O | Byron | yes | 0.40 | 0.53 | 0.55 | 0.66 | 0.10 | 0.45 |
| Jangmo O | Byron | yes | 0.09 | 0.27 | 0.34 | 0.30 | 0.10 | 0.22 |
| Magnemite | Byron | yes | 0.55 | 0.27 | 0.46 | 0.36 | 0.64 | 0.45 |
| Riolu | Byron | yes | 0.63 | 0.46 | 0.16 | 0.02 | 0.64 | 0.38 |
| Shellder | Byron | yes | 0.16 | 0.21 | 0.39 | 0.24 | 0.64 | 0.33 |

## No niche today, one on the proposal

Stages the player can evolve within the split they are first owned in are held only briefly; they are marked. Each role's rank on the proposal, the best first:

| Stage | First owned | Evolves within it | Offense | Speed | Physical wall | Special wall | Status | Standing |
|---|---|---|---|---|---|---|---|---|
| Phanpy | Roark |  | 0.83 | 0.27 | 0.92 | 0.42 | 0.62 | 0.61 |
| Graveler | Gardenia |  | 0.77 | 0.32 | 0.81 | 0.20 | 0.43 | 0.51 |
| Munchlax | Gardenia |  | 0.46 | 0.00 | 0.80 | 0.45 | 0.43 | 0.43 |
| Polteageist | Fantina |  | 0.83 | 0.66 | 0.59 | 0.85 | 0.17 | 0.62 |
| Sylveon | Fantina |  | 0.72 | 0.50 | 0.90 | 0.99 | 0.13 | 0.65 |
| Umbreon | Fantina |  | 0.25 | 0.57 | 0.51 | 0.80 | 0.63 | 0.55 |
| Hisuian Sliggoo | Wake |  | 0.26 | 0.22 | 0.64 | 0.78 | 0.14 | 0.41 |
| Croconaw | Fantina | yes | 0.80 | 0.47 | 0.80 | 0.62 | 0.63 | 0.66 |
| Gastly | Fantina | yes | 0.82 | 0.75 | 0.06 | 0.08 | 0.63 | 0.47 |

## A niche today, none on the proposal

Stages the player can evolve within the split they are first owned in are held only briefly; they are marked. Each role's rank on the proposal, the best first:

| Stage | First owned | Evolves within it | Offense | Speed | Physical wall | Special wall | Status | Standing |
|---|---|---|---|---|---|---|---|---|
| Turtwig | Roark |  | 0.31 | 0.15 | 0.74 | 0.72 | 0.28 | 0.44 |
| Dwebble | Gardenia |  | 0.61 | 0.47 | 0.56 | 0.72 | 0.33 | 0.54 |
| Masquerain | Gardenia |  | 0.43 | 0.53 | 0.68 | 0.42 | 0.20 | 0.45 |
| Duskull | Fantina |  | 0.09 | 0.07 | 0.65 | 0.74 | 0.63 | 0.43 |
| Litten | Gardenia | yes | 0.32 | 0.64 | 0.71 | 0.57 | 0.05 | 0.46 |

## Ian's super-wanted lines

Each stage of the lines, in the split it is first owned in: its standing today and on the proposal (0.5 is the split's average; Ian wants these a little above it) and its niche roles on the proposal. A stage the player evolves within its first split is marked.

| Line | Stage | First owned | Evolves within it | Standing today | On the proposal | Niche on the proposal |
|---|---|---|---|---|---|---|
| Articuno | Articuno | Volkner |  | 0.66 | 0.66 | physical wall, all-rounder |
| Bounsweet | Bounsweet | Roark | yes | 0.44 | 0.43 | none |
| Bounsweet | Steenee | Roark |  | 0.58 | 0.56 | none |
| Bounsweet | Tsareena | Fantina |  | 0.66 | 0.65 | offense, speed, physical wall |
| Budew | Budew | Roark |  | 0.27 | 0.26 | none |
| Budew | Roselia | Fantina |  | 0.50 | 0.54 | none |
| Budew | Roserade | Wake |  | 0.71 | 0.70 | offense, speed, all-rounder |
| Buneary | Buneary | Roark |  | 0.79 | 0.78 | offense, speed, status, all-rounder |
| Buneary | Lopunny | Gardenia |  | 0.90 | 0.90 | offense, speed, physical wall, special wall, status, all-rounder |
| Cresselia | Cresselia | Volkner |  | 0.73 | 0.73 | physical wall, special wall, all-rounder |
| Eevee | Eevee | Fantina | yes | 0.38 | 0.38 | none |
| Eevee | Glaceon | Fantina |  | 0.38 | 0.45 | none |
| Eevee | Leafeon | Fantina |  | 0.78 | 0.77 | speed, physical wall, special wall, all-rounder |
| Eevee | Sylveon | Fantina |  | 0.31 | 0.65 | physical wall, special wall |
| Eevee | Umbreon | Fantina |  | 0.52 | 0.55 | special wall |
| Eevee | Flareon | Maylene |  | 0.76 | 0.76 | offense, special wall, all-rounder |
| Eevee | Jolteon | Maylene |  | 0.82 | 0.82 | offense, speed, physical wall, special wall, all-rounder |
| Eevee | Vaporeon | Maylene |  | 0.67 | 0.66 | special wall |
| Eevee | Espeon | Byron |  | 0.70 | 0.70 | speed, special wall, all-rounder |
| Feebas | Feebas | Gardenia |  | 0.20 | 0.20 | speed |
| Feebas | Milotic | Fantina |  | 0.30 | 0.43 | none |
| Flabebe | Floette | Maylene |  | 0.31 | 0.30 | none |
| Flabebe | Florges | Wake |  | 0.58 | 0.58 | physical wall, special wall |
| Koffing | Galarian Weezing | Maylene |  | 0.55 | 0.60 | physical wall |
| Koffing | Koffing | Maylene | yes | 0.43 | 0.45 | physical wall |
| Koffing | Weezing | Maylene |  | 0.73 | 0.73 | physical wall, special wall, all-rounder |
| Meloetta | Meloetta | Galactic |  | 0.65 | 0.65 | speed, physical wall, special wall |
| Pheromosa | Pheromosa | Volkner |  | 0.38 | 0.40 | speed |
| Ponyta | Ponyta | Roark |  | 0.56 | 0.55 | speed |
| Ponyta | Galarian Rapidash | Gardenia |  | 0.83 | 0.84 | offense, speed, physical wall, special wall, all-rounder |
| Ponyta | Rapidash | Wake |  | 0.71 | 0.71 | offense, speed, all-rounder |
| Popplio | Brionne | Gardenia |  | 0.62 | 0.60 | status |
| Popplio | Popplio | Gardenia | yes | 0.37 | 0.34 | status |
| Popplio | Primarina | Maylene |  | 0.67 | 0.65 | special wall |
| Ralts | Gardevoir | Fantina |  | 0.78 | 0.78 | offense, physical wall, special wall, all-rounder |
| Ralts | Kirlia | Fantina | yes | 0.41 | 0.36 | none |
| Ralts | Ralts | Fantina | yes | 0.28 | 0.24 | none |
| Ralts | Gallade | Byron |  | 0.81 | 0.81 | offense, physical wall, special wall, all-rounder |
| Rookidee | Corvisquire | Roark |  | 0.54 | 0.52 | speed |
| Rookidee | Rookidee | Roark | yes | 0.42 | 0.40 | none |
| Rookidee | Corviknight | Wake |  | 0.65 | 0.64 | physical wall, special wall |
| Scorbunny | Raboot | Roark |  | 0.68 | 0.66 | speed, physical wall, all-rounder |
| Scorbunny | Scorbunny | Roark | yes | 0.57 | 0.56 | speed |
| Scorbunny | Cinderace | Maylene |  | 0.72 | 0.71 | offense, speed, physical wall, special wall, all-rounder |
| Skitty | Skitty | Roark |  | 0.38 | 0.37 | none |
| Skitty | Delcatty | Gardenia |  | 0.64 | 0.71 | speed, status, all-rounder |
| Skorupi | Drapion | Wake |  | 0.75 | 0.75 | speed, physical wall, special wall, all-rounder |
| Skorupi | Skorupi | Wake | yes | 0.35 | 0.35 | none |
| Snorunt | Snorunt | Gardenia |  | 0.53 | 0.52 | none |
| Snorunt | Glalie | Wake |  | 0.66 | 0.66 | speed |
| Snorunt | Froslass | Byron |  | 0.69 | 0.68 | offense, speed, all-rounder |
| Suicune | Suicune | Candice |  | 0.76 | 0.76 | speed, physical wall, special wall, all-rounder |
| Swablu | Swablu | Fantina |  | 0.29 | 0.29 | none |
| Swablu | Altaria | Maylene |  | 0.76 | 0.75 | physical wall, special wall, all-rounder |
| Togepi | Togepi | Gardenia | yes | 0.19 | 0.23 | status |
| Togepi | Togetic | Gardenia |  | 0.24 | 0.41 | status |
| Togepi | Togekiss | Wake |  | 0.80 | 0.80 | offense, physical wall, special wall, all-rounder |
| Vulpix | Vulpix | Roark |  | 0.55 | 0.67 | status, all-rounder |
| Vulpix | Alolan Ninetales | Gardenia |  | 0.81 | 0.84 | offense, speed, special wall, status, all-rounder |
| Vulpix | Ninetales | Maylene |  | 0.86 | 0.86 | offense, speed, physical wall, special wall, all-rounder |

Super-wanted lines with no stage read here (after the story, not in the game yet, or with no source): Alolan Ninetales, Galarian Rapidash, Galarian Weezing.

The pool places these in no split: a scripted source above its location split's cap (the Mining Museum's level 20 fossils in Roark's split) or at a location it does not know (Fullmoon Island). This check reads each in the later of its location's split and the first split whose cap admits its level: Aerodactyl (Gardenia), Anorith (Gardenia), Kabuto (Gardenia), Omanyte (Gardenia).

First owned after the League or never on the story's path, so not read: Arceus, Darkrai, Dialga, Moltres, Palkia, Regice, Regigigas, Regirock, Registeel, Shaymin, Zapdos.

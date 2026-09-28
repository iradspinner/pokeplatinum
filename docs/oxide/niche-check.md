# The niche check

Written by `niche.py` (2026-09-28) for Ian's ruling of the same day: every Pokemon should have an important niche at the point the player has it, while stronger and weaker lines stay fine. Nothing here is in the game data. Each of the 454 stages the player can own is read in the split it is first owned in, at that split's cap, with the moves it can have by then, against every trainer Pokemon of that split, by the calculator the scores use. Five roles: offense (the mean share of a foe's HP its best move takes), speed (the share of foes it outspeeds), physical wall and special wall (of the foes whose best attack on it is of that kind, the share that need three or more hits on it while it needs three or fewer on them, since a bulky stage with nothing to attack with is no wall) and status (its best status move by Ian's tiers). Each is ranked against every stage the player can own by that split; its standing is the mean of its five ranks, 0.5 being the split's average. A stage has a niche when one role, or its standing (an all-rounder), puts it in the split's top quarter. Two readings: Oxide's lists today, and the proposal (the learnset proposal with the later moves placed). `docs/oxide/niche-check.tsv` has every stage's numbers.

| Stages without a niche | Held past their first split | Evolve within it |
|---|---|---|
| On both readings | 63 | 61 |
| Today only (the proposal gives one) | 6 | 1 |
| On the proposal only (it takes one away) | 1 | 1 |

## No niche on either reading

Stages the player can evolve within the split they are first owned in are held only briefly; they are marked. Each role's rank on the proposal, the best first:

| Stage | First owned | Evolves within it | Offense | Speed | Physical wall | Special wall | Status | Standing |
|---|---|---|---|---|---|---|---|---|
| Budew | Roark |  | 0.07 | 0.39 | 0.04 | 0.04 | 0.73 | 0.26 |
| Dustox | Roark |  | 0.41 | 0.64 | 0.42 | 0.71 | 0.28 | 0.49 |
| Finneon | Roark |  | 0.42 | 0.64 | 0.58 | 0.01 | 0.73 | 0.48 |
| Goldeen | Roark |  | 0.53 | 0.56 | 0.65 | 0.29 | 0.28 | 0.46 |
| Grubbin | Roark |  | 0.28 | 0.39 | 0.28 | 0.71 | 0.28 | 0.39 |
| Kricketune | Roark |  | 0.40 | 0.64 | 0.61 | 0.71 | 0.28 | 0.53 |
| Luxio | Roark |  | 0.46 | 0.50 | 0.39 | 0.71 | 0.28 | 0.47 |
| Nosepass | Roark |  | 0.26 | 0.15 | 0.31 | 0.38 | 0.28 | 0.28 |
| Nuzleaf | Roark |  | 0.27 | 0.50 | 0.46 | 0.71 | 0.62 | 0.51 |
| Pawmi | Roark |  | 0.11 | 0.50 | 0.10 | 0.71 | 0.28 | 0.34 |
| Poochyena | Roark |  | 0.32 | 0.22 | 0.28 | 0.71 | 0.73 | 0.45 |
| Sewaddle | Roark |  | 0.30 | 0.27 | 0.14 | 0.31 | 0.28 | 0.26 |
| Skitty | Roark |  | 0.23 | 0.39 | 0.55 | 0.36 | 0.73 | 0.45 |
| Smoliv | Roark |  | 0.17 | 0.15 | 0.53 | 0.71 | 0.28 | 0.37 |
| Steenee | Roark |  | 0.19 | 0.56 | 0.53 | 0.71 | 0.62 | 0.52 |
| Turtwig | Roark |  | 0.20 | 0.15 | 0.65 | 0.71 | 0.28 | 0.40 |
| Vullaby | Roark |  | 0.35 | 0.50 | 0.18 | 0.71 | 0.62 | 0.47 |
| Wooloo | Roark |  | 0.14 | 0.39 | 0.51 | 0.20 | 0.62 | 0.37 |
| Zubat | Roark |  | 0.15 | 0.39 | 0.25 | 0.71 | 0.28 | 0.35 |
| Carbink | Gardenia |  | 0.17 | 0.39 | 0.54 | 0.23 | 0.61 | 0.39 |
| Dolliv | Gardenia |  | 0.10 | 0.15 | 0.15 | 0.30 | 0.05 | 0.15 |
| Dwebble | Gardenia |  | 0.51 | 0.47 | 0.47 | 0.69 | 0.15 | 0.46 |
| Flaaffy | Gardenia |  | 0.44 | 0.33 | 0.58 | 0.40 | 0.34 | 0.42 |
| Kabuto | Gardenia |  | 0.61 | 0.47 | 0.28 | 0.13 | 0.34 | 0.37 |
| Mantyke | Gardenia |  | 0.28 | 0.39 | 0.36 | 0.25 | 0.34 | 0.33 |
| Omanyte | Gardenia |  | 0.43 | 0.20 | 0.28 | 0.15 | 0.34 | 0.28 |
| Shellos | Gardenia |  | 0.14 | 0.15 | 0.31 | 0.14 | 0.34 | 0.21 |
| Snorunt | Gardenia |  | 0.45 | 0.39 | 0.61 | 0.54 | 0.61 | 0.52 |
| Swadloon | Gardenia |  | 0.30 | 0.29 | 0.17 | 0.66 | 0.05 | 0.29 |
| Swinub | Gardenia |  | 0.50 | 0.39 | 0.52 | 0.49 | 0.34 | 0.45 |
| Alomomola | Fantina |  | 0.27 | 0.57 | 0.49 | 0.35 | 0.13 | 0.36 |
| Chansey | Fantina |  | 0.13 | 0.36 | 0.22 | 0.23 | 0.63 | 0.32 |
| Duskull | Fantina |  | 0.09 | 0.07 | 0.67 | 0.71 | 0.63 | 0.43 |
| Fomantis | Fantina |  | 0.07 | 0.18 | 0.07 | 0.12 | 0.17 | 0.12 |
| Klefki | Fantina |  | 0.08 | 0.71 | 0.35 | 0.23 | 0.13 | 0.30 |
| Litwick | Fantina |  | 0.61 | 0.04 | 0.44 | 0.61 | 0.23 | 0.38 |
| Mantine | Fantina |  | 0.44 | 0.66 | 0.50 | 0.65 | 0.63 | 0.58 |
| Roselia | Fantina |  | 0.45 | 0.57 | 0.59 | 0.48 | 0.63 | 0.54 |
| Sandygast | Fantina |  | 0.47 | 0.01 | 0.44 | 0.20 | 0.11 | 0.25 |
| Seaking | Fantina |  | 0.28 | 0.63 | 0.37 | 0.38 | 0.63 | 0.46 |
| Seel | Fantina |  | 0.18 | 0.30 | 0.31 | 0.49 | 0.63 | 0.38 |
| Stunky | Fantina |  | 0.41 | 0.69 | 0.39 | 0.39 | 0.63 | 0.50 |
| Swablu | Fantina |  | 0.14 | 0.36 | 0.27 | 0.26 | 0.63 | 0.33 |
| Sylveon | Fantina |  | 0.19 | 0.50 | 0.42 | 0.68 | 0.13 | 0.39 |
| Wailmer | Fantina |  | 0.62 | 0.50 | 0.55 | 0.57 | 0.63 | 0.57 |
| Yamask | Fantina |  | 0.10 | 0.10 | 0.37 | 0.60 | 0.23 | 0.28 |
| Arboliva | Maylene |  | 0.44 | 0.23 | 0.62 | 0.60 | 0.17 | 0.41 |
| Decidueye | Maylene |  | 0.46 | 0.62 | 0.61 | 0.68 | 0.17 | 0.51 |
| Floette | Maylene |  | 0.25 | 0.39 | 0.27 | 0.46 | 0.17 | 0.31 |
| Frillish | Maylene |  | 0.14 | 0.23 | 0.18 | 0.62 | 0.17 | 0.27 |
| Gothorita | Maylene |  | 0.38 | 0.41 | 0.72 | 0.65 | 0.12 | 0.46 |
| Lurantis | Maylene |  | 0.40 | 0.29 | 0.65 | 0.56 | 0.17 | 0.41 |
| Toxapex | Maylene |  | 0.06 | 0.17 | 0.56 | 0.40 | 0.63 | 0.36 |
| Unown | Maylene |  | 0.00 | 0.31 | 0.01 | 0.00 | 0.04 | 0.07 |
| Chandelure | Wake |  | 0.65 | 0.69 | 0.56 | 0.53 | 0.21 | 0.53 |
| Jellicent | Wake |  | 0.18 | 0.47 | 0.63 | 0.71 | 0.14 | 0.42 |
| Palossand | Wake |  | 0.50 | 0.16 | 0.64 | 0.38 | 0.14 | 0.36 |
| Sliggoo | Wake |  | 0.16 | 0.47 | 0.48 | 0.75 | 0.06 | 0.38 |
| Larvesta | Byron |  | 0.13 | 0.46 | 0.26 | 0.30 | 0.02 | 0.23 |
| Lunatone | Byron |  | 0.59 | 0.61 | 0.69 | 0.47 | 0.63 | 0.60 |
| Solrock | Byron |  | 0.68 | 0.61 | 0.74 | 0.33 | 0.63 | 0.60 |
| Delibird | Candice |  | 0.18 | 0.65 | 0.21 | 0.19 | 0.63 | 0.37 |
| Mandibuzz | Candice |  | 0.10 | 0.70 | 0.43 | 0.55 | 0.22 | 0.40 |
| Bidoof | Roark | yes | 0.08 | 0.15 | 0.12 | 0.71 | 0.28 | 0.27 |
| Blipbug | Roark | yes | 0.03 | 0.31 | 0.01 | 0.03 | 0.28 | 0.13 |
| Bounsweet | Roark | yes | 0.13 | 0.15 | 0.46 | 0.71 | 0.62 | 0.41 |
| Cascoon | Roark | yes | 0.05 | 0.01 | 0.07 | 0.07 | 0.28 | 0.10 |
| Fletchling | Roark | yes | 0.22 | 0.56 | 0.18 | 0.71 | 0.28 | 0.39 |
| Kricketot | Roark | yes | 0.04 | 0.09 | 0.04 | 0.07 | 0.28 | 0.10 |
| Lotad | Roark | yes | 0.25 | 0.15 | 0.09 | 0.71 | 0.73 | 0.38 |
| Nidoran F | Roark | yes | 0.31 | 0.27 | 0.61 | 0.71 | 0.28 | 0.43 |
| Pikipek | Roark | yes | 0.56 | 0.64 | 0.25 | 0.71 | 0.28 | 0.49 |
| Rookidee | Roark | yes | 0.21 | 0.39 | 0.25 | 0.71 | 0.28 | 0.37 |
| Seedot | Roark | yes | 0.01 | 0.15 | 0.01 | 0.01 | 0.62 | 0.16 |
| Sentret | Roark | yes | 0.39 | 0.05 | 0.43 | 0.71 | 0.62 | 0.44 |
| Shinx | Roark | yes | 0.47 | 0.31 | 0.39 | 0.71 | 0.28 | 0.43 |
| Silcoon | Roark | yes | 0.05 | 0.01 | 0.07 | 0.07 | 0.28 | 0.10 |
| Snivy | Roark | yes | 0.09 | 0.56 | 0.31 | 0.11 | 0.28 | 0.27 |
| Wurmple | Roark | yes | 0.12 | 0.05 | 0.07 | 0.33 | 0.28 | 0.17 |
| Burmy | Gardenia | yes | 0.03 | 0.20 | 0.11 | 0.03 | 0.61 | 0.20 |
| Cherubi | Gardenia | yes | 0.11 | 0.20 | 0.05 | 0.16 | 0.61 | 0.22 |
| Combee | Gardenia | yes | 0.27 | 0.65 | 0.14 | 0.64 | 0.05 | 0.35 |
| Dewpider | Gardenia | yes | 0.51 | 0.07 | 0.40 | 0.47 | 0.13 | 0.32 |
| Hoothoot | Gardenia | yes | 0.39 | 0.39 | 0.26 | 0.56 | 0.61 | 0.44 |
| Hoppip | Gardenia | yes | 0.30 | 0.39 | 0.16 | 0.30 | 0.61 | 0.35 |
| Mareep | Gardenia | yes | 0.28 | 0.20 | 0.19 | 0.17 | 0.34 | 0.23 |
| Marill | Gardenia | yes | 0.17 | 0.26 | 0.45 | 0.32 | 0.34 | 0.31 |
| Rowlet | Gardenia | yes | 0.56 | 0.29 | 0.31 | 0.45 | 0.61 | 0.44 |
| Treecko | Gardenia | yes | 0.26 | 0.65 | 0.09 | 0.33 | 0.34 | 0.33 |
| Azurill | Fantina | yes | 0.49 | 0.04 | 0.34 | 0.16 | 0.63 | 0.33 |
| Bonsly | Fantina | yes | 0.53 | 0.01 | 0.72 | 0.30 | 0.63 | 0.44 |
| Charcadet | Fantina | yes | 0.06 | 0.18 | 0.21 | 0.34 | 0.23 | 0.20 |
| Eevee | Fantina | yes | 0.12 | 0.43 | 0.18 | 0.50 | 0.63 | 0.37 |
| Happiny | Fantina | yes | 0.03 | 0.10 | 0.03 | 0.02 | 0.63 | 0.16 |
| Joltik | Fantina | yes | 0.10 | 0.57 | 0.18 | 0.24 | 0.13 | 0.25 |
| Kirlia | Fantina | yes | 0.34 | 0.36 | 0.19 | 0.26 | 0.63 | 0.35 |
| Ralts | Fantina | yes | 0.18 | 0.23 | 0.05 | 0.11 | 0.63 | 0.24 |
| Salandit | Fantina | yes | 0.42 | 0.72 | 0.47 | 0.24 | 0.63 | 0.50 |
| Sinistea | Fantina | yes | 0.39 | 0.36 | 0.25 | 0.38 | 0.17 | 0.31 |
| Smoochum | Fantina | yes | 0.39 | 0.57 | 0.02 | 0.17 | 0.63 | 0.36 |
| Snom | Fantina | yes | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 |
| Totodile | Fantina | yes | 0.63 | 0.28 | 0.69 | 0.44 | 0.63 | 0.54 |
| Croagunk | Maylene | yes | 0.54 | 0.35 | 0.25 | 0.18 | 0.63 | 0.39 |
| Floragato | Maylene | yes | 0.17 | 0.73 | 0.31 | 0.40 | 0.08 | 0.34 |
| Gothita | Maylene | yes | 0.20 | 0.29 | 0.22 | 0.28 | 0.12 | 0.22 |
| Mankey | Maylene | yes | 0.57 | 0.62 | 0.11 | 0.11 | 0.63 | 0.41 |
| Mareanie | Maylene | yes | 0.04 | 0.29 | 0.30 | 0.14 | 0.63 | 0.28 |
| Slowpoke | Maylene | yes | 0.48 | 0.03 | 0.47 | 0.38 | 0.63 | 0.40 |
| Trapinch | Maylene | yes | 0.69 | 0.01 | 0.19 | 0.08 | 0.63 | 0.32 |
| Clobbopus | Wake | yes | 0.29 | 0.13 | 0.17 | 0.08 | 0.63 | 0.26 |
| Ferroseed | Wake | yes | 0.20 | 0.01 | 0.57 | 0.69 | 0.08 | 0.31 |
| Goomy | Wake | yes | 0.04 | 0.22 | 0.16 | 0.23 | 0.06 | 0.14 |
| Horsea | Wake | yes | 0.26 | 0.47 | 0.26 | 0.06 | 0.63 | 0.34 |
| Lampent | Wake | yes | 0.36 | 0.40 | 0.39 | 0.39 | 0.21 | 0.35 |
| Mime Jr | Wake | yes | 0.50 | 0.47 | 0.11 | 0.33 | 0.63 | 0.41 |
| Sealeo | Wake | yes | 0.35 | 0.28 | 0.69 | 0.58 | 0.63 | 0.51 |
| Skorupi | Wake | yes | 0.09 | 0.54 | 0.36 | 0.13 | 0.63 | 0.35 |
| Spheal | Wake | yes | 0.20 | 0.06 | 0.23 | 0.24 | 0.63 | 0.27 |
| Hakamo O | Byron | yes | 0.42 | 0.53 | 0.57 | 0.63 | 0.10 | 0.45 |
| Jangmo O | Byron | yes | 0.10 | 0.27 | 0.36 | 0.32 | 0.10 | 0.23 |
| Magnemite | Byron | yes | 0.57 | 0.27 | 0.46 | 0.39 | 0.63 | 0.47 |
| Riolu | Byron | yes | 0.66 | 0.46 | 0.16 | 0.02 | 0.63 | 0.39 |
| Shellder | Byron | yes | 0.17 | 0.21 | 0.38 | 0.24 | 0.63 | 0.33 |
| Magikarp | Galactic | yes | 0.01 | 0.68 | 0.01 | 0.03 | 0.02 | 0.15 |

## No niche today, one on the proposal

Stages the player can evolve within the split they are first owned in are held only briefly; they are marked. Each role's rank on the proposal, the best first:

| Stage | First owned | Evolves within it | Offense | Speed | Physical wall | Special wall | Status | Standing |
|---|---|---|---|---|---|---|---|---|
| Phanpy | Roark |  | 0.67 | 0.27 | 0.91 | 0.40 | 0.62 | 0.57 |
| Grotle | Gardenia |  | 0.41 | 0.20 | 0.85 | 0.64 | 0.61 | 0.54 |
| Quagsire | Gardenia |  | 0.77 | 0.20 | 0.43 | 0.24 | 0.34 | 0.40 |
| Glaceon | Fantina |  | 0.37 | 0.57 | 0.45 | 0.77 | 0.63 | 0.56 |
| Polteageist | Fantina |  | 0.81 | 0.66 | 0.60 | 0.85 | 0.17 | 0.62 |
| Umbreon | Fantina |  | 0.22 | 0.57 | 0.52 | 0.77 | 0.63 | 0.54 |
| Croconaw | Fantina | yes | 0.77 | 0.46 | 0.79 | 0.63 | 0.63 | 0.66 |

## A niche today, none on the proposal

Stages the player can evolve within the split they are first owned in are held only briefly; they are marked. Each role's rank on the proposal, the best first:

| Stage | First owned | Evolves within it | Offense | Speed | Physical wall | Special wall | Status | Standing |
|---|---|---|---|---|---|---|---|---|
| Snover | Gardenia |  | 0.58 | 0.26 | 0.35 | 0.62 | 0.34 | 0.43 |
| Litten | Gardenia | yes | 0.26 | 0.65 | 0.61 | 0.54 | 0.05 | 0.42 |

## Ian's super-wanted lines

Each stage of the lines, in the split it is first owned in: its standing today and on the proposal (0.5 is the split's average; Ian wants these a little above it) and its niche roles on the proposal. A stage the player evolves within its first split is marked.

| Line | Stage | First owned | Evolves within it | Standing today | On the proposal | Niche on the proposal |
|---|---|---|---|---|---|---|
| Alolan Ninetales | Alolan Ninetales | Gardenia |  | 0.42 | 0.23 | speed |
| Bounsweet | Bounsweet | Roark | yes | 0.41 | 0.41 | none |
| Bounsweet | Steenee | Roark |  | 0.53 | 0.52 | none |
| Bounsweet | Tsareena | Fantina |  | 0.67 | 0.66 | speed, physical wall, special wall |
| Budew | Budew | Roark |  | 0.26 | 0.26 | none |
| Budew | Roselia | Fantina |  | 0.49 | 0.54 | none |
| Budew | Roserade | Wake |  | 0.71 | 0.70 | offense, speed, all-rounder |
| Buneary | Buneary | Roark |  | 0.80 | 0.80 | offense, speed, status, all-rounder |
| Buneary | Lopunny | Gardenia |  | 0.88 | 0.89 | offense, speed, physical wall, special wall, status, all-rounder |
| Cresselia | Cresselia | Byron |  | 0.73 | 0.73 | speed, physical wall, special wall, all-rounder |
| Eevee | Eevee | Fantina | yes | 0.37 | 0.37 | none |
| Eevee | Glaceon | Fantina |  | 0.53 | 0.56 | special wall |
| Eevee | Leafeon | Fantina |  | 0.76 | 0.76 | speed, physical wall, all-rounder |
| Eevee | Sylveon | Fantina |  | 0.23 | 0.39 | none |
| Eevee | Umbreon | Fantina |  | 0.50 | 0.54 | special wall |
| Eevee | Flareon | Maylene |  | 0.76 | 0.76 | offense, special wall, all-rounder |
| Eevee | Jolteon | Maylene |  | 0.82 | 0.82 | offense, speed, physical wall, special wall, all-rounder |
| Eevee | Vaporeon | Maylene |  | 0.69 | 0.68 | special wall, all-rounder |
| Eevee | Espeon | Wake |  | 0.75 | 0.75 | offense, speed, special wall, all-rounder |
| Feebas | Feebas | Gardenia |  | 0.23 | 0.23 | speed |
| Feebas | Milotic | Fantina |  | 0.63 | 0.62 | special wall |
| Flabebe | Floette | Maylene |  | 0.31 | 0.31 | none |
| Flabebe | Florges | Wake |  | 0.58 | 0.58 | physical wall, special wall |
| Galarian Rapidash | Galarian Rapidash | Galactic |  | 0.48 | 0.48 | speed |
| Galarian Weezing | Galarian Weezing | Galactic |  | 0.48 | 0.48 | physical wall |
| Koffing | Koffing | Maylene | yes | 0.44 | 0.45 | physical wall |
| Koffing | Weezing | Maylene |  | 0.69 | 0.69 | physical wall, all-rounder |
| Ponyta | Ponyta | Roark |  | 0.61 | 0.60 | speed |
| Ponyta | Rapidash | Wake |  | 0.71 | 0.71 | offense, speed, all-rounder |
| Popplio | Brionne | Gardenia |  | 0.57 | 0.57 | status |
| Popplio | Popplio | Gardenia | yes | 0.35 | 0.34 | status |
| Popplio | Primarina | Maylene |  | 0.67 | 0.66 | special wall |
| Ralts | Gallade | Fantina |  | 0.82 | 0.82 | offense, physical wall, special wall, all-rounder |
| Ralts | Gardevoir | Fantina |  | 0.80 | 0.78 | offense, physical wall, special wall, all-rounder |
| Ralts | Kirlia | Fantina | yes | 0.41 | 0.35 | none |
| Ralts | Ralts | Fantina | yes | 0.28 | 0.24 | none |
| Rookidee | Corvisquire | Roark |  | 0.49 | 0.48 | speed |
| Rookidee | Rookidee | Roark | yes | 0.37 | 0.37 | none |
| Rookidee | Corviknight | Wake |  | 0.64 | 0.64 | physical wall, special wall |
| Scorbunny | Raboot | Roark |  | 0.62 | 0.61 | speed, all-rounder |
| Scorbunny | Scorbunny | Roark | yes | 0.52 | 0.51 | speed |
| Scorbunny | Cinderace | Maylene |  | 0.72 | 0.71 | offense, speed, physical wall, special wall, all-rounder |
| Skitty | Skitty | Roark |  | 0.46 | 0.45 | none |
| Skitty | Delcatty | Gardenia |  | 0.78 | 0.78 | speed, physical wall, status, all-rounder |
| Skorupi | Drapion | Wake |  | 0.75 | 0.75 | speed, physical wall, special wall, all-rounder |
| Skorupi | Skorupi | Wake | yes | 0.35 | 0.35 | none |
| Snorunt | Snorunt | Gardenia |  | 0.52 | 0.52 | none |
| Snorunt | Froslass | Fantina |  | 0.79 | 0.79 | offense, speed, special wall, all-rounder |
| Snorunt | Glalie | Wake |  | 0.78 | 0.78 | speed, physical wall, special wall, all-rounder |
| Suicune | Suicune | Candice |  | 0.76 | 0.75 | speed, physical wall, special wall, all-rounder |
| Swablu | Swablu | Fantina |  | 0.33 | 0.33 | none |
| Swablu | Altaria | Maylene |  | 0.80 | 0.80 | offense, physical wall, special wall, all-rounder |
| Togepi | Togepi | Gardenia | yes | 0.43 | 0.52 | special wall, status |
| Togepi | Togetic | Gardenia |  | 0.74 | 0.76 | offense, physical wall, special wall, status, all-rounder |
| Togepi | Togekiss | Wake |  | 0.80 | 0.81 | offense, physical wall, special wall, all-rounder |
| Vulpix | Vulpix | Roark |  | 0.73 | 0.71 | offense, status, all-rounder |
| Vulpix | Ninetales | Maylene |  | 0.86 | 0.85 | offense, speed, physical wall, special wall, all-rounder |

Super-wanted lines with no stage read here (after the story, not in the game yet, or with no source): Articuno, Meloetta, Pheromosa.

The pool places these in no split: a scripted source above its location split's cap (the Mining Museum's level 20 fossils in Roark's split) or at a location it does not know (Fullmoon Island). This check reads each in the later of its location's split and the first split whose cap admits its level: Aerodactyl (Gardenia), Anorith (Gardenia), Cranidos (Gardenia), Cresselia (Byron), Kabuto (Gardenia), Lileep (Gardenia), Omanyte (Gardenia), Shieldon (Gardenia).

First owned after the League or never on the story's path, so not read: Arceus, Articuno, Darkrai, Dialga, Moltres, Palkia, Pheromosa, Regice, Regigigas, Regirock, Registeel, Shaymin, Zapdos.

# Where the 51 appended lines go in the regional dex: a proposal for Ian

Written 2026-09-30 by the encounter track. Nothing here changes the game or the
pick-list yet; it waits on Ian's choice.

On 2026-09-26 the pick-list grew by 51 lines, 110 species: the seventeen water
lines and the 34 lines of scarcity step 2. To keep every existing `dex_pos`
where it was, they were appended at the end of `docs/oxide/species-pick-list.csv`
as rows 393 to 502, and where they sit in the regional dex was left to Ian.

The proposal is to put each one where the curated dex's own rule puts it. The
first 360 rows follow one rule without exception once three wrong national dex
numbers in the file are corrected (Rotom, Manaphy and Shaymin, fixed on
2026-09-30). Each evolution line stays together, lines run in the national dex
order of their earliest member, members within a line run in national dex order
(so Pikachu, Raichu, Pichu, and Electabuzz, Elekid, Electivire), and a regional
form's line follows its base's (Ninetales, then Alolan Ninetales). Applied to the
51, that gives the table below: the regional dex becomes 463 entries (before rows 363 to 392, below), and the
appended lines scatter through it instead of trailing after the Generation 9
starters. Starly lands beside Sinnoh's other Generation 4 lines, after Empoleon;
Totodile after the legendary birds; Mr. Mime before Galarian Mr. Mime.

The alternative worth weighing is a Sinnoh-style order, like vanilla Platinum's
own dex, which runs roughly in the order the player meets each line. The OxiDex
already knows every line's first split and area, so it could generate that
order for the whole dex. It would renumber all 463 entries rather than place 51,
so it is a bigger change than this question asked for. Leaving the 51 as a block
at the end is the third option, and costs nothing.

Two things follow whichever order Ian picks. First, `dex_pos` is also the row of
`New Pokedex.xlsx` that `species_import.py` reads, so the chosen order goes into a
new `regional` column rather than renumbering `dex_pos`. Second, nothing in the
game reads this order yet: the in-game Sinnoh dex is still vanilla's 210 entries
(`res/pokemon/sinnoh_pokedex.json`), and building Oxide's own regional dex from
the pick-list is separate work that has not been planned.

Out of scope but under the same rule: rows 363 to 392 (Glimmet, Nosepass,
Geodude, Phanpy, Goldeen, Corphish, Chinchou, Carvanha, Remoraid, Buizel,
Shellos, Mantyke, Gastly and Misdreavus) have trailed the 360 since the file
landed on 2026-09-20, and would move the same way if Ian wants them folded in
too. Meloetta (row 503) stays outside the regional dex, as ruled on 2026-09-27.

## The proposed placements

Numbers are the proposed regional dex numbers with these 51 merged in and rows
363 to 392 left out. "After" is the entry just before each line in the new
order; "National" is the national dex number that places it.

| Regional | Line, in dex order | After | National | Added with |
|---|---|---|---|---|
| 16 to 18 | Clefairy, Clefable, Cleffa | Nidoking | 35 | scarcity |
| 25 to 26 | Psyduck, Golduck | Crobat | 54 | water |
| 30 to 33 | Poliwag, Poliwhirl, Poliwrath, Politoed | Annihilape | 60 | water |
| 34 to 36 | Abra, Kadabra, Alakazam | Politoed | 63 | scarcity |
| 37 to 39 | Machop, Machoke, Machamp | Alakazam | 66 | scarcity |
| 45 to 47 | Slowpoke, Slowbro, Slowking | Galarian Rapidash | 79 | water |
| 48 to 50 | Magnemite, Magneton, Magnezone | Slowking | 81 | scarcity |
| 51 to 52 | Seel, Dewgong | Magnezone | 86 | water |
| 53 to 54 | Shellder, Cloyster | Dewgong | 90 | water |
| 57 to 58 | Krabby, Kingler | Steelix | 98 | water |
| 59 to 60 | Lickitung, Lickilicky | Kingler | 108 | scarcity |
| 67 to 69 | Chansey, Blissey, Happiny | Rhyperior | 113 | scarcity |
| 70 to 71 | Tangela, Tangrowth | Happiny | 114 | scarcity |
| 72 to 74 | Horsea, Seadra, Kingdra | Tangrowth | 116 | water |
| 75 to 76 | Staryu, Starmie | Kingdra | 120 | water |
| 77 to 78 | Mr. Mime, Mime Jr. | Starmie | 122 | scarcity |
| 84 to 85 | Jynx, Smoochum | Kleavor | 124 | scarcity |
| 92 | Lapras | Magmortar | 131 | water |
| 102 to 103 | Snorlax, Munchlax | Sylveon | 143 | scarcity |
| 110 to 112 | Totodile, Croconaw, Feraligatr | Galarian Moltres | 158 | water |
| 115 to 116 | Hoothoot, Noctowl | Furret | 163 | scarcity |
| 120 to 122 | Mareep, Flaaffy, Ampharos | Togekiss | 179 | scarcity |
| 123 to 125 | Marill, Azumarill, Azurill | Ampharos | 183 | scarcity |
| 126 to 127 | Sudowoodo, Bonsly | Azurill | 185 | scarcity |
| 128 to 130 | Hoppip, Skiploom, Jumpluff | Bonsly | 187 | scarcity |
| 131 to 132 | Aipom, Ambipom | Jumpluff | 190 | scarcity |
| 138 to 139 | Murkrow, Honchkrow | Clodsire | 198 | scarcity |
| 140 | Girafarig | Honchkrow | 203 | scarcity |
| 143 to 144 | Snubbull, Granbull | Gliscor | 209 | scarcity |
| 145 | Qwilfish | Granbull | 211 | water |
| 154 | Corsola | Mamoswine | 222 | water |
| 155 | Delibird | Corsola | 225 | scarcity |
| 174 to 178 | Wurmple, Silcoon, Beautifly, Cascoon, Dustox | Mightyena | 265 | scarcity |
| 185 to 186 | Wingull, Pelipper | Shiftry | 278 | water |
| 199 | Mawile | Delcatty | 303 | scarcity |
| 200 to 201 | Meditite, Medicham | Mawile | 307 | scarcity |
| 202 | Plusle | Medicham | 311 | scarcity |
| 203 | Minun | Plusle | 312 | scarcity |
| 207 to 208 | Wailmer, Wailord | Roserade | 320 | water |
| 226 | Tropius | Dusknoir | 357 | scarcity |
| 227 to 228 | Chimecho, Chingling | Tropius | 358 | scarcity |
| 233 to 235 | Spheal, Sealeo, Walrein | Froslass | 363 | water |
| 236 to 238 | Clamperl, Huntail, Gorebyss | Walrein | 366 | water |
| 239 | Relicanth | Gorebyss | 369 | water |
| 255 to 257 | Starly, Staravia, Staraptor | Empoleon | 396 | scarcity |
| 258 to 259 | Bidoof, Bibarel | Staraptor | 399 | scarcity |
| 260 to 261 | Kricketot, Kricketune | Bibarel | 401 | scarcity |
| 269 to 271 | Burmy, Wormadam, Mothim | Bastiodon | 412 | scarcity |
| 275 to 276 | Cherubi, Cherrim | Pachirisu | 420 | scarcity |
| 288 | Chatot | Bronzong | 441 | scarcity |
| 301 | Carnivine | Toxicroak | 455 | scarcity |

## What Ian decides

1. The order: the curated rule as above (recommended, since it is the rule the
   other 360 already follow), a Sinnoh-style order by where each line is met,
   or the 51 left at the end.
2. Whether rows 363 to 392 are folded in by the same choice.

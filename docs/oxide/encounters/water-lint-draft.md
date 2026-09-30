# Water lint: the biome draft and today's counts

A draft for Ian (2026-09-29). The blind encounter review's water principles (`~/oxide-trials/encounter-review/out/principles.md`, 11 to 20) are adopted as principles, and the tables are re-authored later. The linter now carries them as aspirational warnings, R19 to R24, which change no table. The rules need one decision from Ian: the biome of each capture area's water, below, with the exceptions a place earns. The counts show how far today's tables are from the principles, so they size the water re-authoring.

Generated from `docs/oxide/encounters/design.json` (`water_biome`, `water_biome_why`, `water_earned`) and `docs/oxide/encounters/water-biomes.json`; `cli lint --rule R19,R19b,R20,R21,R22,R23,R24 --all` lists every finding.

## Today's warnings

| Rule | What it reports | Warnings |
|---|---|---|
| R19 | a line outside its biome's palette, not earned by the place (principle 11) | 395 |
| R19b | a sea line in inland water (principle 12) | 108 |
| R20 | a line in more than one of a capture area's water methods, the Super Rod 1% adult of a Good Rod line allowed (principle 14) | 262 |
| R21 | a line that is the 1% in more than three capture areas (principle 19) | 17 |
| R22 | two areas opening in one split with the same top pair (principle 16) | 22 |
| R23 | non-Water over 30% of a table outside a cave (principle 15) | 0 |
| R24 | a water table with fewer than five lines (principle 18) | 50 |
| All | | 854 |

R21's lines, by the number of capture areas where each is a water 1%:

| Line | Areas |
|---|---|
| Froakie | 36 |
| Totodile | 7 |
| Psyduck | 7 |
| Mareanie | 6 |
| Poliwag | 6 |
| Relicanth | 6 |
| Frillish | 5 |
| Buizel | 5 |
| Clamperl | 5 |
| Corsola | 5 |
| Horsea | 5 |
| Chinchou | 4 |
| Finneon | 4 |
| Wailmer | 4 |
| Carvanha | 4 |
| Mudkip | 4 |
| Tentacool | 4 |

## The draft biome of each capture area

Each area's four water tables draw from its biome's palette. "Earned" lines are the place's own exceptions, which the review names (an electric fish at the Windworks, Lapras at Acuity); each is a choice for Ian as much as the biome is. The warnings column counts R19, R19b, R20, R23 and R24 for the area.

| Capture area | Split | Biome | Why | Earned | Warnings |
|---|---|---|---|---|---|
| Lake Verity | Roark | lake | one of the three lakes, which Ian names as water places; Lake Verity after the blast, the same lake |  | 43 |
| Ravaged Path | Roark | cave_pool | a cave pool; vanilla's Surf was Psyduck and Zubat | Feebas (Feebas and Milotic are fixed here, a super-wanted line) | 13 |
| Route 203 | Roark | village_pond | the fishing pool beside the route (review) |  | 15 |
| Route 219 | Roark | beach | the beach south of Sandgem (review) |  | 10 |
| Twinleaf Town | Roark | village_pond | the village pond (review: already a pond on the Old Rod and Surf) |  | 16 |
| Eterna City | Gardenia | village_pond | the town canal, a pond's palette (review) |  | 14 |
| Oreburgh Gate | Gardenia | cave_pool | the Gate's cave pool; vanilla's Surf was Psyduck and Zubat | Frillish (a ghost in the Gate's pool, the review's 1%) | 19 |
| Route 204 | Gardenia | lowland_river | the same river, north of the Ravaged Path (review); the river south of the Ravaged Path (review) |  | 15 |
| Route 205 | Gardenia | lowland_river | the river by Eterna Forest (review); the river below the Windworks (review) |  | 27 |
| Valley Windworks | Gardenia | industrial | the power plant's water (review) | Chinchou (the one inland home of an electric fish (review)) | 24 |
| Mt. Coronet South | Fantina | cave_pool | the mountain's cave stream; vanilla's Surf was Zubat and Golbat |  | 18 |
| Route 208 | Fantina | mountain_stream | the stream down from Mt. Coronet (review) |  | 19 |
| Route 209 | Maylene | mountain_stream | the stream by the Lost Tower (review) | Frillish (a ghost jelly under the graveyard (review)) | 18 |
| Great Marsh | Wake | marsh | the Great Marsh (review: marsh-true) |  | 66 |
| Pastoria City | Wake | marsh | marsh-edge water, which the review keeps as it is |  | 12 |
| Route 212 | Wake | marsh, village_pond | the garden pond by the Pokemon Mansion (review); the rain swamp, the Froakie line's home (review) |  | 24 |
| Route 213 | Wake | beach | the beach and its tide pools (review) |  | 11 |
| Route 214 | Wake | village_pond | the pond above the cave (review) |  | 15 |
| Canalave City | Byron | harbour | the harbour (review) |  | 15 |
| Celestic Town | Byron | village_pond | the spring pond (review) | Frillish (Jellicent at 60% in the old town's pond stays (review)) | 17 |
| Fuego Ironworks | Byron | industrial | the ironworks' river (review) | Qwilfish (the poisoned fish of an industrial river (review)); Frillish (the review's 1% at the ironworks) | 21 |
| Iron Island | Byron | open_sea | the open sea round the island (review) |  | 13 |
| Lake Valor | Byron | lake | the bombed lake, one of the three lakes | Frillish (a ghost at the bombed lake (review's lake palette)) | 28 |
| Route 210 | Byron | mountain_stream | the fog stream (review) | Frillish (Jellicent in the fog stays (review)) | 18 |
| Route 218 | Byron | beach | the strait's shallows (review: Finneon and Krabby) |  | 11 |
| Route 220 | Byron | open_sea | open sea (review) |  | 11 |
| Route 221 | Byron | beach | the coast (review) |  | 10 |
| Lake Acuity | Candice | lake | the cold lake, one of the three lakes | Lapras (Lapras at Acuity (review)); Seel (the cold lake's seal (review)); Spheal (the cold lake's seal (review's 1%)) | 29 |
| Mt. Coronet B1F | Candice | cave_pool | the underground lake; vanilla's Surf was Zubat and Golbat | Feebas (Feebas and Milotic are fixed here, a super-wanted line) | 23 |
| Snowpoint City | Candice | cold_sea | the cold harbour (review) | Snover (the Ice slots through the fishing holes stay (review)) | 7 |
| Resort Area | Galactic | beach | the warm sea off the resort (review) |  | 10 |
| Route 225 | Galactic | mountain_stream | a mountain stream (review) |  | 24 |
| Route 226 | Galactic | open_sea | the sea below the cliffs (review) |  | 14 |
| Route 227 | Galactic | hot_spring | the volcanic hot springs (review) | Feebas (Feebas and Milotic are fixed here, a super-wanted line) | 16 |
| Route 228 | Galactic | hot_spring | the desert oasis (review) |  | 19 |
| Route 229 | Galactic | lowland_river | the meadow stream (review) |  | 12 |
| Route 230 | Galactic | open_sea | the tropical sea (review) |  | 9 |
| Route 222 | Volkner | beach | Sunyshore's beach (review) |  | 11 |
| Sunyshore City | Volkner | harbour | the harbour (review) |  | 16 |
| Pokémon League | Barry | mountain_stream | the mountaintop pools (review) |  | 23 |
| Route 223 | Barry | open_sea | the deep sea before the League (review) |  | 13 |
| Sendoff Spring | Barry | lake | the fogbound lake (review); vanilla's Surf was all Golduck | Frillish (a ghost at the fogbound lake (review's lake palette)) | 22 |
| Route 224 | Post | beach | not in the review: the post-game coast by the map |  | 12 |
| Victory Road | Post | cave_pool | the cave river's side room, post-game; the cave river; vanilla's Surf was Floatzel and Golbat |  | 32 |

## The palettes

A palette names lines, so any stage of a named line belongs. The sea lines are named by stage (Chinchou, Lanturn, Sharpedo, Wailmer, Wailord, Mantyke, Mantine, Tentacool, Tentacruel, Corsola, Clamperl, Huntail, Gorebyss, Luvdisc, Remoraid, Octillery, Finneon, Lumineon, Horsea, Seadra, Kingdra, Qwilfish, Staryu, Starmie, Shellder, Cloyster, Relicanth), so Carvanha may live in a pond while Sharpedo stays at sea. Grimer and Muk (Fuego Ironworks' water) and Bibarel (Routes 205 south and 218), the two unplaced lines Ian will consider, are in no palette yet; Bidoof's line is in the river palette as the review had it.

| Biome | Palette |
|---|---|
| village pond | Goldeen, Barboach, Corphish, Poliwag, Wooper, Lotad, Surskit, Psyduck, Buizel, Marill, Slowpoke, Carvanha, Shellos, Bidoof |
| lowland river | Goldeen, Barboach, Corphish, Poliwag, Wooper, Lotad, Surskit, Psyduck, Buizel, Marill, Slowpoke, Carvanha, Shellos, Bidoof |
| mountain stream | Barboach, Goldeen, Poliwag, Corphish, Goomy, Zubat, Psyduck, Wooper, Marill, Slowpoke, Buizel |
| cave pool | Barboach, Goldeen, Poliwag, Corphish, Goomy, Zubat, Psyduck, Wooper, Buizel |
| lake | Psyduck, Goldeen, Surskit, Lotad, Marill, Slowpoke, Poliwag |
| marsh | Wooper, Lotad, Surskit, Dewpider, Carvanha, Slowpoke, Barboach, Krabby, Froakie, Yanma, Croagunk, Goomy, Poliwag, Psyduck |
| industrial water | Chinchou, Qwilfish, Shellos, Drifloon, Goldeen, Psyduck |
| hot spring or oasis | Poliwag, Barboach, Corphish, Psyduck, Wooper, Goldeen |
| beach and shallows | Tentacool, Wingull, Shellos, Corsola, Staryu, Krabby, Finneon, Remoraid, Luvdisc, Mareanie, Chinchou, Mantyke, Horsea, Qwilfish, Clamperl, Dhelmise |
| harbour | Tentacool, Mantyke, Wailmer, Carvanha, Chinchou, Horsea, Finneon, Remoraid, Relicanth, Clamperl, Frillish, Lapras, Wingull, Shellder, Dhelmise, Staryu, Corsola |
| open sea | Tentacool, Mantyke, Wailmer, Carvanha, Chinchou, Horsea, Finneon, Remoraid, Relicanth, Clamperl, Frillish, Lapras, Wingull, Shellder, Dhelmise, Staryu, Corsola |
| cold sea | Seel, Spheal, Lapras, Shellder, Relicanth, Snorunt |

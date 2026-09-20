# Pokemon given to the player by a script

Generated 2026-09-20 from the base ROM with `tools/oxide/scriptdis.py`, for the
encounter tracker tool. Every `GivePokemon`, `GiveEgg` and `GivePokemonWithMoves`
the base ROM's field scripts reach, with the same list from vanilla alongside so
Ian's additions are separable from what Platinum already did.

58 distinct gifts across 19 maps. **52 are new in the base ROM**;
the rest are vanilla's own (the Togepi, Riolu and Manaphy eggs, Eevee, Porygon,
the Day Care Ditto and the starter).

The machine-readable version is `pokemon-gifts.csv`, same columns as the table
below. Regenerate both by re-running the survey in the session notes rather than
editing by hand.

Two rows do not name a species because the script picks one at runtime and passes
it in a variable: `route_201` (the starter) and `mining_museum`. Those need the
calling script read to resolve, not the command.

| Map | Species | Level | Command | New? |
|---|---|---|---|---|
| `canalave_library_2f` | SPECIES_AGGRON | 50 | GivePokemon | **yes** |
| `canalave_library_2f` | SPECIES_BANETTE | 50 | GivePokemon | **yes** |
| `canalave_library_2f` | SPECIES_DRAPION | 50 | GivePokemon | **yes** |
| `canalave_library_2f` | SPECIES_DUGTRIO | 50 | GivePokemon | **yes** |
| `canalave_library_2f` | SPECIES_DUSCLOPS | 50 | GivePokemon | **yes** |
| `canalave_library_2f` | SPECIES_HARIYAMA | 50 | GivePokemon | **yes** |
| `canalave_library_2f` | SPECIES_PRIMEAPE | 50 | GivePokemon | **yes** |
| `eterna_city` | SPECIES_TOGEPI | 11 | GiveEgg | vanilla |
| `eterna_city_condominiums_1f` | SPECIES_NUMEL | 23 | GivePokemon | **yes** |
| `eterna_city_condominiums_1f` | SPECIES_SLUGMA | 23 | GivePokemon | **yes** |
| `eterna_city_condominiums_1f` | SPECIES_TORKOAL | 23 | GivePokemon | **yes** |
| `floaroma_meadow_house` | SPECIES_CHERUBI | 18 | GivePokemon | **yes** |
| `floaroma_meadow_house` | SPECIES_COMBEE | 18 | GivePokemon | **yes** |
| `floaroma_meadow_house` | SPECIES_PACHIRISU | 18 | GivePokemon | **yes** |
| `floaroma_town_middle_house` | SPECIES_MURKROW | 18 | GivePokemon | **yes** |
| `floaroma_town_middle_house` | SPECIES_POOCHYENA | 18 | GivePokemon | **yes** |
| `floaroma_town_middle_house` | SPECIES_SEEDOT | 18 | GivePokemon | **yes** |
| `floaroma_town_middle_house` | SPECIES_STUNKY | 18 | GivePokemon | **yes** |
| `hearthome_city_northwest_house` | SPECIES_EEVEE | 20 | GivePokemon | vanilla |
| `hearthome_city_pokemon_fan_club` | SPECIES_BULBASAUR | 30 | GivePokemon | **yes** |
| `hearthome_city_pokemon_fan_club` | SPECIES_CHARMANDER | 30 | GivePokemon | **yes** |
| `hearthome_city_pokemon_fan_club` | SPECIES_CHIKORITA | 30 | GivePokemon | **yes** |
| `hearthome_city_pokemon_fan_club` | SPECIES_CYNDAQUIL | 30 | GivePokemon | **yes** |
| `hearthome_city_pokemon_fan_club` | SPECIES_MUDKIP | 30 | GivePokemon | **yes** |
| `hearthome_city_pokemon_fan_club` | SPECIES_SQUIRTLE | 30 | GivePokemon | **yes** |
| `hearthome_city_pokemon_fan_club` | SPECIES_TORCHIC | 30 | GivePokemon | **yes** |
| `hearthome_city_pokemon_fan_club` | SPECIES_TOTODILE | 30 | GivePokemon | **yes** |
| `hearthome_city_pokemon_fan_club` | SPECIES_TREECKO | 30 | GivePokemon | **yes** |
| `iron_island_b2f_left_room` | SPECIES_RIOLU | 10 | GiveEgg | vanilla |
| `jubilife_city_south_house_1f` | SPECIES_GLAMEOW | 10 | GivePokemon | **yes** |
| `jubilife_city_south_house_1f` | SPECIES_MEOWTH | 10 | GivePokemon | **yes** |
| `jubilife_city_south_house_1f` | SPECIES_SKITTY | 10 | GivePokemon | **yes** |
| `mining_museum` | (from variable 0x40b4) | 20 | GivePokemon | vanilla |
| `oreburgh_city_middle_house` | SPECIES_BELLSPROUT | 15 | GivePokemon | **yes** |
| `oreburgh_city_middle_house` | SPECIES_CACNEA | 15 | GivePokemon | **yes** |
| `oreburgh_city_middle_house` | SPECIES_ODDISH | 15 | GivePokemon | **yes** |
| `pastoria_city_north_house` | SPECIES_DEWGONG | 45 | GivePokemon | **yes** |
| `pastoria_city_north_house` | SPECIES_KINGLER | 45 | GivePokemon | **yes** |
| `pastoria_city_north_house` | SPECIES_POLITOED | 45 | GivePokemon | **yes** |
| `pastoria_city_north_house` | SPECIES_RELICANTH | 45 | GivePokemon | **yes** |
| `pastoria_city_north_house` | SPECIES_REMORAID | 45 | GivePokemon | **yes** |
| `pastoria_city_north_house` | SPECIES_SEADRA | 45 | GivePokemon | **yes** |
| `pokemon_day_care` | SPECIES_DITTO | 30 | GivePokemon | **yes** |
| `pokemon_mansion_office` | SPECIES_MANAPHY | 8 | GiveEgg | **yes** |
| `route_201` | (from variable 0x8000) | 5 | GivePokemon | changed |
| `sandgem_town_house` | SPECIES_EKANS | 5 | GivePokemon | **yes** |
| `sandgem_town_house` | SPECIES_GULPIN | 5 | GivePokemon | **yes** |
| `sandgem_town_house` | SPECIES_VENONAT | 5 | GivePokemon | **yes** |
| `solaceon_town_northeast_house` | SPECIES_CLAMPERL | 30 | GivePokemon | **yes** |
| `solaceon_town_northeast_house` | SPECIES_NATU | 30 | GivePokemon | **yes** |
| `solaceon_town_northeast_house` | SPECIES_TRAPINCH | 30 | GivePokemon | **yes** |
| `unused_jubilife_city_south_house_3f` | SPECIES_GLAMEOW | 8 | GivePokemon | **yes** |
| `unused_jubilife_city_south_house_3f` | SPECIES_MEOWTH | 8 | GivePokemon | **yes** |
| `unused_jubilife_city_south_house_3f` | SPECIES_SKITTY | 8 | GivePokemon | **yes** |
| `veilstone_city_northeast_house` | SPECIES_MASQUERAIN | 40 | GivePokemon | **yes** |
| `veilstone_city_northeast_house` | SPECIES_PINSIR | 40 | GivePokemon | **yes** |
| `veilstone_city_northeast_house` | SPECIES_PORYGON | 25 | GivePokemon | vanilla |
| `veilstone_city_northeast_house` | SPECIES_SHUCKLE | 40 | GivePokemon | **yes** |

## Note on how these are structured

Most of the new ones follow one shape, which Ian confirmed: they were originally
pick-events where the player chose, and he rewrote the scripts to roll a die
instead. The giveaway is a `GetRandom` followed by one branch per species, each
with its own party-full check. The names of the choices are usually still sitting
in the map's text bank, unreferenced, from the version where you picked.

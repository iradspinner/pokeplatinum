# Ability audit for the ability pass

A snapshot of 2026-09-27, from `tools/oxide/encounters/ability_audit.py`, which reruns it. It lists every Pokemon the player can obtain (on the species pick-list, and given by a table, a honey tree or a live scripted source, or evolved from one that is) whose abilities Oxide rules out or cannot use. Nothing here changes game data; the ability pass decides the replacements. The split is the first one the species can be had in, and the place is where; an evolved stage names the stage it comes from.

The first list is the weather abilities in a regular slot. Ian's standing rule (2026-09-26) keeps weather out of the player's hands, allowing a weather ability only as a hidden one, which the game's single Ability Patch reaches.

| Species | Slot | Ability | What it does | First split | How |
|---|---|---|---|---|---|
| Golduck | slot 2 | Cloud Nine | cancels weather | Roark | Lake Verity: Old Rod, as Psyduck; Golduck by level 33 |
| Psyduck | slot 2 | Cloud Nine | cancels weather | Roark | Lake Verity: Old Rod |
| Abomasnow | slot 1 | Snow Warning | sets snow | Gardenia | Mt. Coronet North: grass, as Snover; Abomasnow by level 40 |
| Snover | slot 1 | Snow Warning | sets snow | Gardenia | Mt. Coronet North: grass |
| Tyranitar | both slots | Sand Stream | sets a sandstorm | Fantina | Wayward Cave: grass, as Larvitar; Pupitar by level 30, then Tyranitar by level 55 |
| Hippopotas | slot 1 | Sand Stream | sets a sandstorm | Wake | Maniac Tunnel: grass |
| Hippowdon | slot 1 | Sand Stream | sets a sandstorm | Wake | Maniac Tunnel: grass, as Hippopotas; Hippowdon by level 34 |

The second list is the abilities that do nothing, because terrain is not in the game (`src/battle/battle_lib.c`). A hidden slot is listed too, since the Ability Patch can give it.

| Species | Slot | Ability | What it does | First split | How |
|---|---|---|---|---|---|
| Arboliva | both slots | Seed Sower | sets Grassy Terrain when hit | Roark | Route 202: grass, as Smoliv; Dolliv by level 25, then Arboliva by level 35 |
| Galarian Weezing | hidden | Misty Surge | sets Misty Terrain | Galactic | Stark Mountain: grass |
| Tapu Koko | both slots | Electric Surge | sets Electric Terrain | Volkner | Lake Verity's roamer: roamer, one of 7 at random (split as the Acuity draw's) |

For reference, the obtainable species whose hidden ability sets or cancels weather. The rule allows these, and lint R18 keeps any script from handing one out.

| Species | Slot | Ability | What it does | First split | How |
|---|---|---|---|---|---|
| Ninetales | hidden | Drought | sets sun | Roark | Route 207: grass, as Vulpix; Ninetales by a Fire Stone |
| Pelipper | hidden | Drizzle | sets rain | Roark | Route 219: Old Rod, as Wingull; Pelipper by level 25 |
| Politoed | hidden | Drizzle | sets rain | Roark | Route 203: Old Rod, as Poliwag; Poliwhirl by level 25, then Politoed by holding a King's Rock |
| Vulpix | hidden | Drought | sets sun | Roark | Route 207: grass |
| Alolan Ninetales | hidden | Snow Warning | sets snow | Gardenia | Mt. Coronet North: grass |
| Altaria | hidden | Cloud Nine | cancels weather | Fantina | Amity Square: grass, as Swablu; Altaria by level 35 |
| Swablu | hidden | Cloud Nine | cancels weather | Fantina | Amity Square: grass |
| Lickilicky | hidden | Cloud Nine | cancels weather | Maylene | Route 215: grass, as Lickitung; Lickilicky by knowing a set move |
| Lickitung | hidden | Cloud Nine | cancels weather | Maylene | Route 215: grass |

Flagged species with no way to obtain them now (held back, or with no source), left out of the lists above:

| Species | Slot | Ability | What it does | First split | How |
|---|---|---|---|---|---|
| Tapu Bulu | both slots | Grassy Surge | sets Grassy Terrain |  |  |
| Tapu Fini | both slots | Misty Surge | sets Misty Terrain |  |  |
| Tapu Lele | both slots | Psychic Surge | sets Psychic Terrain |  |  |

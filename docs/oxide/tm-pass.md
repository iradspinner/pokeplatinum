# The TM pass, a draft (pre-v3)

Written by `tmpass.py` (2026-09-28) for Ian's rulings of the same day. This is the pre-v3 draft, committed as it stood on 2026-09-30; a rerun on learnset v3 and the landed buff review replaces it. It writes no game data. TMs are single-use again and each placement gives a set number of copies: strong TMs one, utility two (three where Ian picks), weak ones given by a single optional trainer. Egg lists are only the trainers' palette. The TSVs beside this file hold the detail: the set (`tm-pass-set.tsv`), who learns each (`tm-pass-compat.tsv`), the items the reach fix moves (`tm-pass-reach.tsv`) and the egg lists (`tm-pass-eggs.tsv`).

## Reach

A flood-fill of every map on foot, from its warps and edges, finds 60 item balls and hidden items that need Surf; they move to the split Surf is usable in. 58 more need a field move the fill does not model (Waterfall, or a rock or a boulder in the way), listed in the TSV for a look. The TMs among them:

| Map | Item | Needs | Split then | Split now |
|---|---|---|---|---|
| LAKE_ACUITY | TM14 | Surf | Candice | Candice |
| LAKE_ACUITY_LOW_WATER | TM14 | more | Candice | Candice |
| LAKE_VALOR | TM25 | Surf | Byron | Byron |
| LAKE_VALOR_DRAINED | TM25 | more | Byron | Byron |
| LAKE_VERITY | TM38 | Surf | Roark | Byron |
| LAKE_VERITY_LOW_WATER | TM38 | more | Roark | Roark |
| OLD_CHATEAU_BACK_MIDDLE_EAST_ROOM | TM90 | more | Fantina | Fantina |
| OREBURGH_GATE_B1F | TM01 | Surf | Gardenia | Byron |
| OREBURGH_GATE_B1F | TM31 | Surf | Gardenia | Byron |
| OREBURGH_GATE_B1F | TM70 | more | Gardenia | Gardenia |
| RAVAGED_PATH | TM03 | Surf | Roark | Byron |
| ROUTE_209 | TM19 | Surf | Maylene | Byron |
| ROUTE_211_EAST | TM29 | more | Byron | Byron |
| ROUTE_212_SOUTH | TM84 | Surf | Wake | Byron |
| ROUTE_213 | TM05 | more | Wake | Wake |
| ROUTE_216 | TM13 | more | Candice | Candice |
| ROUTE_223 | TM18 | Surf | Barry | Barry |
| ROUTE_226 | TM53 | more | Galactic | Galactic |
| VALLEY_WINDWORKS_OUTSIDE | TM24 | Surf | Gardenia | Byron |
| VALOR_LAKEFRONT | TM85 | more | Wake | Wake |
| VICTORY_ROAD_2F | TM71 | more | Barry | Barry |
| VICTORY_ROAD_B1F | TM59 | more | Barry | Barry |

## The set

65 of today's 92 TMs stay; 27 go (Ian's removals, and any that no longer qualify). 35 new ones come from the later games' TM and tutor moves, ranked by how many lines with a stage that has no niche they would give a role, then by lines reached, then by worth. The line falls at 100 TMs; the 15 after it are shown so Ian can move it. The six HMs are below, and the reliable-status group apart.

Leaving: TM01 Focus Punch (Ian's removal), TM06 Toxic (Ian's removal), TM07 Hail (Ian's removal), TM11 Sunny Day (Ian's removal), TM17 Protect (Ian's removal), TM18 Rain Dance (Ian's removal), TM20 Safeguard (a status move rated under B), TM32 Double Team (Ian's removal), TM37 Sandstorm (Ian's removal), TM41 Torment (a status move rated under B), TM45 Attract (a status move rated under B), TM46 Thief (Ian's removal), TM48 Skill Swap (Ian's removal), TM49 Snatch (Ian's removal), TM56 Fling (hangs on a held item), TM61 Will-O-Wisp (Ian's removal), TM63 Embargo (Ian's removal), TM64 Explosion (the user faints, which in a nuzlocke is a death), TM67 Recycle (a status move rated under B), TM70 Flash (Ian's removal), TM75 Swords Dance (Ian's removal), TM77 Psych Up (a status move rated under B), TM78 Captivate (a status move rated under B), TM83 Natural Gift (hangs on a held item), TM85 Dream Eater (Ian's removal), TM87 Swagger (a status move rated under B), TM90 Substitute (Ian's removal).

| New TM | Tier | Lines | Lines without a niche it helps | Worth |
|---|---|---|---|---|
| Curse | utility | 72 | 17 | 100 |
| Knock Off | utility | 78 | 14 | 70 |
| Signal Beam | utility | 64 | 14 | 75 |
| Haze | utility | 40 | 14 | 100 |
| Skitter Smack | utility | 34 | 14 | 70 |
| Iron Defense | utility | 60 | 13 | 100 |
| Dazzling Gleam | utility | 44 | 13 | 80 |
| Zen Headbutt | utility | 60 | 12 | 80 |
| Baton Pass | strong | 54 | 12 | 125 |
| Hydro Pump | strong | 58 | 11 | 110 |
| Nasty Plot | strong | 49 | 11 | 125 |
| Earth Power | strong | 47 | 11 | 90 |
| Pain Split | utility | 34 | 11 | 100 |
| Scald | utility | 48 | 10 | 80 |
| Play Rough | strong | 38 | 10 | 90 |
| Synthesis | utility | 24 | 10 | 100 |
| Dive | utility | 48 | 9 | 80 |
| Crunch | utility | 47 | 8 | 80 |
| Hyper Voice | strong | 44 | 8 | 100 |
| Tailwind | strong | 42 | 8 | 125 |
| Wild Charge | utility | 25 | 8 | 76 |
| Heal Bell | utility | 21 | 8 | 100 |
| Air Slash | utility | 42 | 7 | 75 |
| Foul Play | strong | 40 | 7 | 95 |
| Dual Wingbeat | utility | 39 | 7 | 80 |
| Bounce | utility | 38 | 7 | 85 |
| StompingTantrum | utility | 64 | 6 | 75 |
| Sucker Punch | utility | 35 | 6 | 70 |
| Meteor Beam | strong | 30 | 6 | 120 |
| Poltergeist | strong | 15 | 6 | 110 |
| Ice Punch | strong | 54 | 5 | 95 |
| Iron Head | utility | 54 | 5 | 80 |
| Psybeam | utility | 37 | 5 | 65 |
| Future Sight | strong | 34 | 5 | 120 |
| Power Gem | utility | 26 | 5 | 80 |

Below the line: Venoshock (24 lines, 5), Toxic Spikes (22 lines, 5), Ice Spinner (22 lines, 5), Alluring Voice (21 lines, 5), Brave Bird (18 lines, 5), Body Press (53 lines, 4), Aqua Tail (45 lines, 4), Hurricane (29 lines, 4), Gunk Shot (28 lines, 4), Ice Fang (24 lines, 4), Bug Buzz (19 lines, 4), Leech Seed (17 lines, 4), Aurora Beam (14 lines, 4), Wish (10 lines, 4), Mega Kick (60 lines, 3).

## Strong TMs and the lines they reach early

A strong TM goes no earlier than the split in which each flagged or over-bar line it reaches has a good move of that type, capped at Byron's, where the flags stop looking. Lines it still reaches with no move of that type by then:

| TM | Placed | No earlier than | Reaches early |
|---|---|---|---|
| Baton Pass | Volkner | Byron | Absol, Aipom, Alolan Ninetales, Ambipom, Blaziken, Buizel, Buneary, Charjabug and more |
| Blizzard | Candice | Byron | Alolan Ninetales, Jynx, Mamoswine, Piloswine, Sneasel |
| Bulk Up | Byron | Byron | Blaziken, Breloom, Buizel, Ceruledge, Cinderace, Combusken, Corviknight, Decidueye and more |
| Calm Mind | Byron | Byron | Abra, Absol, Alakazam, Alolan Ninetales, Armarouge, Braixen, Carbink, Chandelure and more |
| Earth Power | - | Byron | Carbink, Dolliv, Gligar, Glimmora, Gliscor, Golem, Grotle, Magcargo and more |
| Earthquake | Candice | Byron | Altaria, Blastoise, Blaziken, Charizard, Drapion, Dwebble, Electivire, Empoleon and more |
| Energy Ball | Galactic | Byron | Abra, Alakazam, Alolan Ninetales, Armarouge, Beautifly, Breloom, Budew, Castform and more |
| Fire Blast | Byron | Byron | Absol, Altaria, Beautifly, Castform, Cinderace, Clefable, Clefairy, Combusken and more |
| Flamethrower | Byron | Byron | Absol, Altaria, Castform, Cinderace, Clefable, Clefairy, Combusken, Electivire and more |
| Focus Blast | HQ | Byron | Blaziken, Grapploct, Medicham, Pawmot, Poliwrath, Toxicroak |
| Foul Play | - | Byron | Abra, Aipom, Alakazam, Alolan Ninetales, Ambipom, Braixen, Delphox, Fennekin and more |
| Frustration | HQ | Byron | Abra, Absol, Aipom, Alakazam, Alolan Ninetales, Altaria, Ambipom, Ampharos and more |
| Future Sight | - | Byron | Armarouge, Azumarill, Castform, Chingling, Clefable, Delphox, Dottler, Golduck and more |
| Hydro Pump | Barry | Byron | Blastoise, Brionne, Buizel, Carvanha, Castform, Corsola, Feraligatr, Finneon and more |
| Hyper Voice | - | Byron | Altaria, Chingling, Clefable, Clefairy, Delcatty, Delphox, Donphan, Espeon and more |
| Ice Beam | Candice | Byron | Absol, Alolan Ninetales, Altaria, Araquanid, Azumarill, Barboach, Bibarel, Bidoof and more |
| Ice Punch | - | Byron | Abra, Aipom, Alakazam, Ambipom, Ampharos, Azumarill, Blastoise, Buizel and more |
| Iron Tail | Byron | Wake | none |
| Meteor Beam | - | Byron | Ampharos, Armarouge, Chimecho, Clefable, Clefairy, Onix, Starmie, Steelix |
| Nasty Plot | Barry | Byron | Aipom, Alakazam, Alolan Ninetales, Ambipom, Chatot, Corviknight, Corvisquire, Crawdaunt and more |
| Overheat | Galactic | Byron | Cinderace, Combusken, Fletchinder, Fletchling, Granbull, Mankey, Primeape, Rapidash and more |
| Play Rough | - | Byron | Absol, Alolan Ninetales, Altaria, Azumarill, Brionne, Buneary, Chatot, Cherrim and more |
| Poltergeist | - | Byron | Ceruledge, Chandelure, Decidueye, Froslass, Gengar, Polteageist, Rotom, Sinistcha |
| Psychic | Byron | Byron | Abra, Armarouge, Beautifly, Braixen, Carbink, Chandelure, Chingling, Clefable and more |
| Return | Candice | Byron | Abra, Absol, Aipom, Alakazam, Alolan Ninetales, Altaria, Ambipom, Ampharos and more |
| Roost | HQ | Byron | Altaria, Beautifly, Charizard, Chatot, Crobat, Dartrix, Decidueye, Dustox and more |
| Sludge Bomb | HQ | Byron | Breloom, Budew, Carnivine, Corphish, Crawdaunt, Crobat, Drapion, Dustox and more |
| Stone Edge | Barry | Byron | Magcargo, Onix |
| Tailwind | - | Byron | Altaria, Beautifly, Castform, Charizard, Chatot, Combee, Corviknight, Corvisquire and more |
| Taunt | Byron | Byron | Abra, Absol, Aipom, Alakazam, Ambipom, Armarouge, Bibarel, Bidoof and more |
| Thunder | Byron | Byron | Charjabug, Pawmot |
| Thunderbolt | Byron | Byron | Absol, Aipom, Ambipom, Bibarel, Bidoof, Buneary, Castform, Charjabug and more |

## The reliable-status group, for Ian to take or leave

Toxic, Will-O-Wisp and each status move that inflicts a major status at 90% or more, or never misses, as strong-tier TMs of one copy each:

| TM | Lines | Placed |
|---|---|---|
| Thunder Wave | 63 | Galactic: ROUTE_228 (ball, today ITEM_TM37) |
| Glare | 0 | -: no free place from that split |
| Spore | 1 | -: no free place from that split |
| Thunder Wave | 63 | -: no free place from that split |
| Toxic | 202 | -: its place today, in Wake, is before Byron; no free place from that split |
| Will-O-Wisp | 38 | -: no free place from that split |
| Yawn | 15 | -: no free place from that split |

## Placement and copies

Strong 39, utility 51, weak 16. Candidates for a third copy are marked; Ian picks. Weak TMs go behind an optional trainer on the easier side of its split, named below; marts keep selling what they sell now.

| TM | Tier | Copies | Split | Where |
|---|---|---|---|---|
| Hidden Power | weak | 1 | Roark | defeating youngster_michael (scale 2.0) |
| Rock Tomb | weak | 1 | Roark | defeating worker_colin (scale 2.0) |
| Stealth Rock | utility | 2 (3?) | Roark | OREBURGH_CITY_GYM (gift) |
| Bullet Seed | utility | 2 | Gardenia | ROUTE_204_NORTH (ball) |
| Dragon Claw | utility | 2 | Gardenia | MT_CORONET_1F_NORTH_ROOM_1 (ball) |
| False Swipe | utility | 2 | Gardenia | ROUTE_204_NORTH (gift, today ITEM_TM78) |
| Grass Knot | utility | 2 | Gardenia | ETERNA_CITY_GYM (gift) |
| Hyper Beam | utility | 2 | Gardenia | ETERNA_CITY (ball, today ITEM_TM46) |
| Light Screen | utility | 2 | Gardenia | ETERNA_CITY_CONDOMINIUMS_2F (gift, today ITEM_TM67) |
| Pluck | weak | 1 | Gardenia | defeating bug_catcher_brandon (scale 2.0) |
| Reflect | utility | 2 | Gardenia | OREBURGH_GATE_B1F (ball, today ITEM_TM70) |
| Rock Polish | weak | 1 | Gardenia | defeating youngster_tyler (scale 2.0) |
| Sleep Talk | weak | 1 | Gardenia | defeating lass_samantha (scale 2.0) |
| Curse | utility | 2 | Fantina | OLD_CHATEAU_BACK_MIDDLE_EAST_ROOM (ball, today ITEM_TM90) |
| Endure | weak | 1 | Fantina | defeating cyclist_john (scale 2.0) |
| Giga Impact | utility | 2 | Fantina | AMITY_SQUARE (ball, today ITEM_TM45) |
| Gyro Ball | utility | 2 | Fantina | OLD_CHATEAU_BACK_EAST_ROOM (ball, today ITEM_TM90) |
| Knock Off | utility | 2 | Fantina | WAYWARD_CAVE_1F (ball, today ITEM_TM32) |
| Rest | weak | 1 | Fantina | defeating cyclist_james (scale 2.0) |
| Secret Power | utility | 2 | Fantina | AMITY_SQUARE (ball) |
| Shadow Claw | utility | 2 | Fantina | HEARTHOME_CITY_DP_GYM_LEADER_ROOM (gift) |
| SolarBeam | weak | 1 | Fantina | defeating cyclist_axel (scale 2.0) |
| Drain Punch | utility | 2 | Maylene | VEILSTONE_CITY_GYM (gift) |
| Facade | utility | 2 | Maylene | ROUTE_210_SOUTH (gift) |
| Haze | utility | 2 | Maylene | SOLACEON_RUINS_ROOM_7 (ball, today ITEM_HM05) |
| Payback | weak | 1 | Maylene | defeating cowgirl_shelley (scale 2.0) |
| Shock Wave | weak | 1 | Maylene | defeating breeder_albert (scale 2.0) |
| Signal Beam | utility | 2 | Maylene | GAME_CORNER (gift, today ITEM_TM64) |
| Skitter Smack | utility | 2 | Maylene | VEILSTONE_CITY (gift, today ITEM_TM63) |
| Steel Wing | utility | 2 | Maylene | ROUTE_209 (ball) |
| Aerial Ace | weak | 1 | Wake | defeating collector_jamal (scale 2.4) |
| Brine | utility | 2 | Wake | PASTORIA_CITY_GYM (gift) |
| Dazzling Gleam | utility | 2 | Wake | ROUTE_212_NORTH (ball, today ITEM_TM11) |
| Dig | utility | 2 | Wake | MANIAC_TUNNEL (ball) |
| Iron Defense | utility | 2 | Wake | POKEMON_MANSION_OFFICE (ball, today ITEM_TM87) |
| Roar | weak | 1 | Wake | defeating pi_carlos (scale 2.0) |
| Silver Wind | weak | 1 | Wake | defeating fisherman_kenneth (scale 3.0) |
| Trick Room | utility | 2 | Wake | GRAND_LAKE_ROUTE_213_NORTHWEST_HOUSE (gift) |
| Zen Headbutt | utility | 2 | Wake | VALOR_LAKEFRONT (ball, today ITEM_TM85) |
| Brick Break | utility | 2 | Byron | OREBURGH_GATE_B1F (ball) |
| Bulk Up | strong | 1 | Byron | OREBURGH_GATE_B1F (ball, today ITEM_TM01) |
| Calm Mind | strong | 1 | Byron | CANALAVE_CITY_SOUTHEAST_HOUSE (gift, today ITEM_TM48); its place today, in Gardenia, is before Byron |
| Fire Blast | strong | 1 | Byron | LAKE_VERITY (ball) |
| Flamethrower | strong | 1 | Byron | FUEGO_IRONWORKS_BUILDING (ball) |
| Flash Cannon | utility | 2 | Byron | CANALAVE_CITY_GYM (gift) |
| Giga Drain | utility | 2 | Byron | ROUTE_209 (ball) |
| Iron Tail | strong | 1 | Byron | IRON_ISLAND_B2F_RIGHT_ROOM (ball) |
| Poison Jab | utility | 2 | Byron | ROUTE_212_SOUTH (ball) |
| Psychic | strong | 1 | Byron | ROUTE_211_EAST (ball) |
| Shadow Ball | utility | 2 | Byron | ROUTE_210_NORTH (ball) |
| Taunt | strong | 1 | Byron | ROUTE_211_EAST (gift, today ITEM_TM77); its place today, in Gardenia, is before Byron |
| Thunder | strong | 1 | Byron | LAKE_VALOR (ball) |
| Thunderbolt | strong | 1 | Byron | VALLEY_WINDWORKS_OUTSIDE (ball) |
| U-turn | utility | 2 (3?) | Byron | CANALAVE_CITY (ball) |
| Water Pulse | weak | 1 | Byron | defeating black_belt_adam (scale 2.0) |
| X-Scissor | utility | 2 | Byron | ROUTE_221 (ball) |
| Avalanche | weak | 1 | Candice | defeating skier_edward (scale 2.0) |
| Blizzard | strong | 1 | Candice | LAKE_ACUITY (ball) |
| Earthquake | strong | 1 | Candice | ROUTE_217 (ball, today ITEM_HM08); its place today, in Fantina, is before Byron |
| Ice Beam | strong | 1 | Candice | ROUTE_216 (ball) |
| Return | strong | 1 | Candice | ROUTE_217 (ball, today ITEM_TM07); its place today, in Maylene, is before Byron |
| Focus Blast | strong | 1 | HQ | VEILSTONE_CITY_GALACTIC_WAREHOUSE (ball, today ITEM_HM02) |
| Frustration | strong | 1 | HQ | GALACTIC_HQ_3F (ball) |
| Roost | strong | 1 | HQ | GALACTIC_HQ_1F (ball, today ITEM_TM49); its place today, in Maylene, is before Byron |
| Sludge Bomb | strong | 1 | HQ | GALACTIC_HQ_B2F (ball) |
| Energy Ball | strong | 1 | Galactic | ROUTE_226 (ball) |
| Overheat | strong | 1 | Galactic | STARK_MOUNTAIN_ROOM_2 (ball) |
| Rock Slide | utility | 2 | Galactic | MT_CORONET_2F (ball) |
| Thunder Wave | strong | 1 | Galactic | ROUTE_228 (ball, today ITEM_TM37) |
| Baton Pass | strong | 1 | Volkner | ROUTE_222 (gift, today ITEM_TM56) |
| Charge Beam | weak | 1 | Volkner | defeating fisherman_brett (scale 2.0) |
| Dark Pulse | utility | 2 | Barry | VICTORY_ROAD_2F (ball) |
| Dragon Pulse | utility | 2 | Barry | VICTORY_ROAD_B1F (ball) |
| Hydro Pump | strong | 1 | Barry | ROUTE_223 (ball, today ITEM_TM18) |
| Nasty Plot | strong | 1 | Barry | VICTORY_ROAD_1F (ball, today ITEM_TM41) |
| Stone Edge | strong | 1 | Barry | VICTORY_ROAD_2F (ball) |
| Air Slash | utility | 2 | - | no free place from that split |
| Bounce | utility | 2 | - | no free place from that split |
| Crunch | utility | 2 | - | no free place from that split |
| Dive | utility | 2 | - | no free place from that split |
| Dual Wingbeat | utility | 2 | - | no free place from that split |
| Earth Power | strong | 1 | - | no free place from that split |
| Foul Play | strong | 1 | - | no free place from that split |
| Future Sight | strong | 1 | - | no free place from that split |
| Glare | strong | 1 | - | no free place from that split |
| Heal Bell | utility | 2 | - | no free place from that split |
| Hyper Voice | strong | 1 | - | no free place from that split |
| Ice Punch | strong | 1 | - | no free place from that split |
| Iron Head | utility | 2 | - | no free place from that split |
| Meteor Beam | strong | 1 | - | no free place from that split |
| Pain Split | utility | 2 | - | no free place from that split |
| Play Rough | strong | 1 | - | no free place from that split |
| Poltergeist | strong | 1 | - | no free place from that split |
| Power Gem | utility | 2 | - | no free place from that split |
| Psybeam | utility | 2 | - | no free place from that split |
| Scald | utility | 2 | - | no free place from that split |
| Spore | strong | 1 | - | no free place from that split |
| StompingTantrum | utility | 2 | - | no free place from that split |
| Sucker Punch | utility | 2 | - | no free place from that split |
| Synthesis | utility | 2 | - | no free place from that split |
| Tailwind | strong | 1 | - | no free place from that split |
| Thunder Wave | strong | 1 | - | no free place from that split |
| Toxic | strong | 1 | - | its place today, in Wake, is before Byron; no free place from that split |
| Wild Charge | utility | 2 | - | no free place from that split |
| Will-O-Wisp | strong | 1 | - | no free place from that split |
| Yawn | strong | 1 | - | no free place from that split |

## The HMs

The six HMs become single-use TMs once field moves work on the badge alone (element 8), tiered like any TM. Ian's view is that apart from Surf and Waterfall they are poor moves, so each other one gets a proposed buff, which would change trainers' copies of the move too; Rock Smash, no longer an HM, is proposed as an early TM:

| HM | Move | Tier | Today | Proposal |
|---|---|---|---|---|
| HM02 | Fly | utility | 90 power, 95 accuracy, FLY | accuracy 95 to 100: a two-turn move that can still miss is poor; this makes it the reliable Flying hit |
| HM03 | Surf | strong | 90 power, 100 accuracy, DOUBLE_DAMAGE_DIVE | as it is (Ian: strong) |
| HM04 | Strength | utility | 80 power, 100 accuracy, HIT | power 80 to 90: a clean Normal hit between Body Slam and Double-Edge, with no recoil |
| HM05 | Defog | utility | - power, never misses accuracy, REMOVE_HAZARDS_SCREENS_EVA_DOWN | clear hazards on both sides as the later games do, if Oxide's does not yet; it then answers the trainers' hazards, a niche nothing else fills |
| HM07 | Waterfall | strong | 80 power, 100 accuracy, FLINCH_HIT | as it is (Ian: strong) |
| HM08 | Rock Climb | utility | 90 power, 100 accuracy, CONFUSE_HIT | accuracy 85 to 95: its 20% confusion makes it a Normal option worth a slot once it seldom misses |
| HM06 | Rock Smash | weak | 40 power, 100 accuracy, LOWER_DEFENSE_HIT | an early TM in Roark's split as it is: Fighting coverage against Roark's Rock types, with its Defense drop |

## Tutors

25 of today's 38 tutor moves stay; leaving: Mud-Slap (under 50 by effective power), Fury Cutter (under 50 by effective power), Rollout (under 50 by effective power), Gastro Acid (a status move rated under B), Snore (under 50 by effective power), Spite (a status move rated under B), Helping Hand (the move pool's cut, or a partner move), Endeavor (under 50 by effective power), Vacuum Wave (under 50 by effective power), Twister (under 50 by effective power), Magnet Rise (a status move rated under B), Last Resort (under 50 by effective power), Uproar (under 50 by effective power). The later games' tutor moves not in the TM set, ranked the same way (the first 15):

| Move | Tier | Lines | Lines without a niche it helps |
|---|---|---|---|
| Defog | strong | 50 | 12 |
| Liquidation | utility | 49 | 5 |
| Lash Out | utility | 27 | 5 |
| Ice Fang | strong | 24 | 4 |
| Sky Attack | utility | 21 | 4 |
| Low Kick | utility | 46 | 3 |
| Triple Axel | strong | 24 | 3 |
| Thunder Fang | strong | 18 | 3 |
| Drill Run | utility | 13 | 3 |
| High Horsepower | strong | 26 | 2 |
| Fire Fang | strong | 20 | 2 |
| Steel Beam | strong | 19 | 2 |
| Mystical Fire | utility | 17 | 2 |
| Psycho Cut | utility | 16 | 2 |
| Rising Voltage | utility | 14 | 2 |

## Stone contests

Ian's scarce-stone ruling accepts two lines wanting one stone. The branches he has ruled in (2026-09-28: Vulpix to Alolan Ninetales by an Ice Stone, Koffing and Ponyta to their Galarian forms by a Moon Stone) add claimants, counted here with the census's places for each stone, less the two bulk sets Ian removed (Route 207's nine, Galactic HQ B2F's):

**Moon Stone**: 2 places (Gardenia ETERNA_CITY (hidden), Galactic MT_CORONET_OUTSIDE_NORTH (hidden)); 8 claimants: Nidorina to Nidoqueen (Roark), Nidorino to Nidoking (Roark), Ponyta to Galarian Rapidash (Roark), Skitty to Delcatty (Roark), Clefairy to Clefable (Gardenia), Eevee to Umbreon (Fantina), Koffing to Galarian Weezing (Maylene), Jigglypuff to Wigglytuff (not owned on the story path).

**Ice Stone**: 0 places (none yet; the item pass places it); 1 claimants: Vulpix to Alolan Ninetales (Roark).

The Ice Stone (item 492, priced 2100 like the other stones) is placed nowhere yet, and its place is the census's call: one copy on Route 217, the snow route in Candice's split, so a Vulpix owner meets it where the Ice types live, well after Alolan Ninetales can be caught wild in Gardenia's split; the item pass picks the exact spot.


## Egg lists, the trainers' palette

549 species get the latest later game's egg moves, less what the engine does not run and the weather ruling forbids (`tm-pass-eggs.tsv`). They are for trainer design only: a nuzlocke has no breeding, the gift eggs are scripted without egg moves, and the relearner never offers them.

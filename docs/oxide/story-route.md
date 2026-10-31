# The story route, split by split, and what the base ROM added

Ian asked on 2026-10-31 for a check of the story route through the whole game before Byron's split is worked: "Story route mainly and making sure you/I aren't missing anything that is in our base rom but not in vanilla". This page is that check, made on the branch `overseer-story-route` from `origin/oxide` at 83b49e7697c. No game data changed.

## Summary

Ian answered the questions on 2026-10-31. The last section, "Ian's answers and the rechecks (2026-10-31)", records what was built from them and two rechecks that correct this page: the Regi ruins open only once the Distortion World is done, and Spring Path, Sendoff Spring and Turnback Cave are walled off until then.

What was checked. Every split from Roark's to the League was walked with a whole-world tile model built on `required.Field`: every map joined by its warps and edges, the field moves each split allows, and a hand table of the story's gates (the coord events that turn the player back, and the flag-hidden people and objects that stand in a passage, each with the point its flag clears). The same walk was run on vanilla's event data from `main`, so each early reach is labelled as vanilla's or as the base ROM's and Oxide's. Each split's mandatory fights were counted with `required.py`, `pairs.py`, the script index and the gauntlet doc. Every map's events, script and text bank were diffed between `~/roms/base.nds` and `~/roms/vanilla.nds`, and each difference on or beside the route was looked up in the docs.

What could not be checked. Nothing was seen in game. The model reads bridges flat and does not see scripts that move warps (`SetWarpEventPos`), so the Regi ruins and the Maniac caves needed reading by hand. Gyms with moving parts and the multi-floor dungeons (Galactic HQ, Mt. Coronet, Victory Road, Iron Island) are not modelled, so their counts come from the gauntlet doc's walk. The base ROM's item balls, its 752 changed text lines and its 125 changed wild tables were counted per map but not traced one by one.

Sequence breaks found:

1. **Wake before Maylene, which skips Barry 4 for good** (vanilla's own; reported to the Overseer at once). Before the Cobble Badge nothing stops the walk from Veilstone through Route 214's gate to Pastoria, and Wake's gym has no story check. Ian chose the fix the same day: Route 214's gate closes until Maylene's badge, built on `overseer-route214-gate`. This page reads Wake's split as if the gate is closed.
2. No other break skips a boss or a required story beat. Five areas open a split or more early, none of them past a boss (listed under each split): Route 218's east shore from the start, Spring Path and Sendoff Spring's shore from Wake's split, Turnback Cave's entrance from HQ's split, the Regi ruins as soon as their entrances open, and Route 223's water before Volkner.

Mandatory non-boss fights per split. Gym trainers, bosses and named Galactic officers are left out, and pairs count once. The first five are the split passes' numbers, and the rest are this page's:

| Split | Cap | Mandatory | Against 10 to 15 |
|---|---:|---:|---|
| Roark | 16 | 8 | Ian's 8 |
| Gardenia | 26 | 12 | meets |
| Fantina | 33 | 10, or 9 if Officer Moira counts as a boss | meets, or one short |
| Maylene | 39 | 11 | meets |
| Wake | 44 | 10 | meets |
| Byron | 53 | 2 | 8 short |
| Candice | 56 | 5 | 5 short |
| HQ | 60 | 4 to 8 (not modelled) | short unless all eight are on the way |
| Galactic | 65 | 4 by the tunnel, 5 by the south climb | 5 or 6 short |
| Volkner | 68 | 1 | 9 short |
| Barry | 71 | 6 | 4 short |
| League | 78 | none | no ordinary trainers |

Base-ROM differences that no doc accounts for:

- The three Regis can be caught before the League. The base ROM took the Hall of Fame and Regigigas checks out of all three ruins. Each now needs only its dot puzzle, and each ruin's entrance (Mt. Coronet, Iron Island B3F, Route 228) opens with a Wailord and a Relicanth in the party once Galactic has left Lake Valor. That is Candice's split for Regice and Registeel and Galactic's for Regirock. `pokemon-sources.md` still calls all three post-game.
- Two Strength boulders on Route 215, at (647,596) and (647,599), close the corridor's edges beside Ace Trainers Dennis and Maya, which is what makes that pair mandatory.
- Two boulders at Lake Verity, at (46,45) and (53,45), beside grunts 3 and 4. Water and the grunts hem them in, so Strength cannot move them, but `required.py` drops every boulder once Strength is held and reads the pair avoidable.
- Lucas or Dawn on Route 207 hands over a Lucky Egg after their battle, where vanilla gave the Vs. Seeker.
- A Happiny beside every gym leader heals the party, and each leader's rematch waits on the League.
- The first battles against Riley (Iron Island), Mira (Wayward Cave), Buck (Route 227) and Marley (Victory Road) appear only in the script index. Cheryl's is counted in Gardenia's split.

Ian's questions:

1. Byron's split has 2 mandatory fights: which Route 210 North and Route 218 trainers should be fixed in place or moved (the candidates are under Byron's split)?
2. Should Iron Island, which left the story path when Strength came on the badge alone, come back onto it, for example by gating the library scene on Riley?
3. Candice's split has 5: fix Route 216's and 217's turning skiers and Ninja Boys to one look, or move Lake Valor's grunts 1 and 3?
4. HQ's split: may the HQ floors be read with the tile model to settle the 4 to 8?
5. Galactic's split has 4 or 5: should a Mt. Coronet floor gain trainers, or the tunnel and the south climb be made to carry the same count?
6. Volkner's split has 1: fix Route 222's ten avoidable trainers in place?
7. Barry's split has 6: fix Route 223's swimmers Oscar and Gabrielle, or move Victory Road's side-room trainers onto 1F?
8. Do the Regis stay catchable before the League, or wait behind the legendary gate with Valor Cavern and Stark Mountain?
9. Gauntlet sections 4 and 5 (Galactic HQ 1F and 2F) each hold one mandatory trainer, under the 2 to 5. Should they be merged or extended?
10. Section 8 (Mt. Coronet 3F to 5F) holds Officers Somnu and Moira inside its lock, and section 2 (Eterna building 3F) holds Moira, against "bosses stay outside". Should they stay?
11. Do the named Galactic officers count as bosses in the mandatory count (Moira in Fantina's split)?
12. Is the Lucky Egg from Lucas or Dawn on Route 207 kept?
13. Should Spring Path and Sendoff Spring's shore from Wake's split, and Turnback Cave's entrance from HQ's, be gated? The encounter tool puts them in Barry's split and post-game.
14. May `required.py` keep a Strength boulder that cannot be pushed (Lake Verity's pair) as a wall?

Next steps:

| Step | Who | Time |
|---|---|---|
| Answer the questions above | Ian | 20 minutes |
| Land the Route 214 gate (`overseer-route214-gate`) | the Overseer | 30 minutes |
| Byron's split pass, with the answers to 1 and 2 | a worker | half a day |
| Correct `pokemon-sources.md` for the Regis, after question 8 | a routine helper | 15 minutes |

## Oxide's own changes that move the route

- **Field moves on the badge alone** (2026-09-29). Five moves open no earlier than vanilla's HMs did: Rock Smash (Coal), Cut (Forest), Rock Climb (Icicle), Waterfall (Beacon), and Fly (Cobble, where vanilla's HM02 waited in the warehouse a few steps later). Surf (Fen) would have opened straight after Wake. Since 2026-10-31 it also waits on Cyrus beaten at Celestic Town, which is right. Strength (Mine) used to come with Riley's HM04 on Iron Island, so Iron Island has left the story path (Byron's split).
- **The Pocket PC** heals anywhere outside a gauntlet and opens no paths. Its Teleport System is gone, and the 22 town and 7 dungeon Abra are hidden at new game (`FLAG_HIDE_TELEPORT_ABRA`).
- **The gym Abra shortcuts** stay, as Ian ruled. Each pair takes the player from the entrance to the leader and back. The entrance Abra works only after the leader's Abra has been talked to, so a gym cannot be skipped (checked in all five gyms' scripts).
- **The Battle Zone ferry** sails after Galactic HQ (`FLAG_FREED_GALACTIC_HQ_POKEMON`), and the zone is optional.
- **The gauntlets** block only their ways back, all of them by refused warps and Victory Road's line. No section has a one-way ledge: `gauntlets.md` explains that no existing ledge points the right way.

## Roark's split (cap 16)

| Area | What opens it | Mandatory |
|---|---|---|
| Twinleaf Town, Route 201 | the start; Barry's scenes | none |
| Sandgem Town and the lab | Rowan and Barry stand aside after the intro | none |
| Route 202 | the Pokedex; Lucas or Dawn's battle (a boss) | Tristan, Natalie, Logan |
| Jubilife City, Route 203 | open; Barry 2 on Route 203 (a boss) | Sebastian, Madeline |
| Oreburgh Gate 1F | open | Diana, Curtis |
| Oreburgh City, the mine | open | Mason (B2F) |
| Oreburgh Gym | Roark met in the mine (Barry's scene at the door) | gym trainers only |

The Ravaged Path is closed by Rock Smash rocks until the Coal Badge. The only early reach is Route 218's east shore, a step west of Jubilife, which the encounter tool already counts from Roark's split (`WATER_SPLITS`).

Base-ROM differences on or beside the route:

| Map | Difference | Accounted for |
|---|---|---|
| Route 201 | the starter briefcase and a delivery man | `pokemon-gifts.md` (the starter, "changed") |
| Route 202 | Lucas or Dawn's battle | the boss docs |
| Twinleaf Town | an esper offering 15 legendary battles, after the Hall of Fame | `pokemon-sources.md` (left out by Ian) |
| Twinleaf Town | a clown who hands over 990 Rare Candies | only the script index; the Pocket PC's 999 fill does the same |
| Twinleaf, Sandgem, Jubilife, Oreburgh | a teleporting Abra each | `pocket-pc.md`, ruling 6 (hidden) |
| Sandgem Town | the Vs. Seeker given, now the Pocket PC | `pocket-pc.md` |
| Sandgem lab | Oak's Letter, the Member Card and the Azure Flute with the National Dex | `pokemon-sources.md` |
| Jubilife, Oreburgh | an Experiencia maid each (training battles) | `trainer-survey.md` |
| Oreburgh Gym | a healing Happiny; Roark's rematch after the League | the rematch in `pocket-pc.md`; the Happiny nowhere |
| Jubilife, Oreburgh, Sandgem houses | clown gifts | `pokemon-gifts.md` |
| Oreburgh Mine B2F | seven new balls, three of them fossils | the script index |
| 11 maps | item balls re-stocked | the TM and item passes worked from these |

## Gardenia's split (cap 26)

| Area | What opens it | Mandatory |
|---|---|---|
| Jubilife City | the Coal Badge starts the grunts' scene | the grunt tag beside Lucas or Dawn |
| Route 204 South, Ravaged Path | Rock Smash (Coal) | Samantha |
| Route 204 North, Floaroma | through the Ravaged Path | Liv and Liz |
| Floaroma Meadow | open outside the scene in which two grunts stand at its mouth | the two meadow grunts |
| Valley Windworks | the Works Key from the meadow | the grunt at the door; Somnu 1 and Mars 1 are bosses |
| Route 205 South to the forest | the bridge grunts leave after the Windworks | Joseph, Andrew |
| Eterna Forest | open | Cheryl's battle, three pairs beside Cheryl |
| Route 205 North, Eterna City | through the forest | none |
| Eterna Gym | Gardenia's scene at its door | gym trainers only |

Route 206's north gate turns away anyone not on a bike, and Mt. Coronet's room off Route 211 West holds Strength boulders, so neither opens early.

Base-ROM differences: the Windworks grunt (Officer Somnu) moved to (15,4) with sight 4 (`import_report.md`). Cheryl's own battle is new and counted (`mandatory-fights-early.md`). Eterna gained a maid, an Abra and a gym Happiny, with Gardenia's rematch after the League, and Floaroma and Eterna gained clown gifts (`pokemon-gifts.md`). The Windworks' Friday Drifloon is gone, and 29 balls were re-stocked.

## Fantina's split (cap 33)

| Area | What opens it | Mandatory |
|---|---|---|
| Galactic Eterna building | the Cut trees at its door (Forest) | gauntlet sections 1 and 2: four grunts, Travon, Officer Moira; Jupiter is the boss |
| Route 206, the Cycling Road | the bike, after the building | none |
| Route 207, Mt. Coronet 1F South | the bike's slope; Lucas or Dawn 2 at the cave mouth (a boss) | Kevin, Helen |
| Route 208, Hearthome City | through the mountain | Robert, Hannah |
| Hearthome Gym | the gym guide stands aside | gym trainers only |

Gates checked: a Pokefan and a Hiker block Hearthome's way onto Route 209 until the Relic Badge (`FLAG_HIDE_HEARTHOME_CITY_ROUTE_209_BLOCKADE`). A reporter and a cameraman stand on Route 212's gate exit until the player has entered Pastoria (`FLAG_HIDE_ROUTE_212_BLOCKADE`, set by Pastoria's map script). Neither can be walked around.

The count of 10 includes the Eterna building's 3F grunt, whom the census names Officer Moira. If named officers are bosses, it is 9 (question 11).

Base-ROM differences: the building's 2F and 3F trainers were moved, and the gauntlet sections were drawn on the moved positions (`import_report.md`, `gauntlets.md`). Lucas or Dawn on Route 207 gives a Lucky Egg after their battle, in the Vs. Seeker's place, which no doc names. Route 207 also gained a scientist who sends the player to look for Mira in Wayward Cave, and an Abra listing Mt. Coronet's exits (hidden). Mira's battle in Wayward Cave is new and off the route. Hearthome gained a maid, an Abra, the Fan Club's nine starter gifts (`pokemon-gifts.md`) and a gym Happiny.

## Maylene's split (cap 39)

| Area | What opens it | Mandatory |
|---|---|---|
| Route 209 | the Relic Badge clears Hearthome's blockade; Barry 3 in the gate (a boss) | Emma and Lil, Albert, Shelley, Danielle |
| Solaceon Town, Route 210 South | open; the Psyduck block the way north | Marco, Ava and Matt, Teri and Tia |
| Route 215 | open | Dennis and Maya, Gregory, Nathaniel, Derek |
| Veilstone City and its gym | open; Wake's scene at the gym door | gym trainers only |

The break: Route 214's gate from Veilstone has no story gate in vanilla or in Oxide. From here the player can walk on to Pastoria and beat Wake before Maylene. Wake's win sets Pastoria's story to 3 and then 4, and Barry 4's trigger at the gym door waits on state 1, which only the warehouse sets later, so Barry 4 is never fought. The fix closes the gate until the Cobble Badge.

Base-ROM differences:

| Map | Difference | Accounted for |
|---|---|---|
| Route 215 | Strength boulders at (647,596) and (647,599), closing the edges of Dennis and Maya's corridor | nowhere; `mandatory-fights.md` counts the pair without saying why it is unavoidable |
| Solaceon's north house | the Utility Stop's vendors (evolution stones among them) | removed, `ingame-checklist.md`, section 4 |
| Pokemon Day Care | Experiencia's EV training, the Power items, the EV berries, a Ditto | the Ditto in `pokemon-gifts.md`; the rest only in the script index |
| Veilstone Gym | an Abra pair and a Happiny | `pocket-pc.md` (the Abra) |
| the warehouse, Solaceon Ruins | HM02's and HM05's balls re-stocked | the badge-alone field moves |
| Route 210 South | a Black Belt clone given a script | the script index |

## Wake's split (cap 44)

Read with Route 214's gate closed until the Cobble Badge, as Ian chose. `wake-split.md` holds the whole reading.

| Area | What opens it | Mandatory |
|---|---|---|
| Veilstone warehouse | the Cobble Badge makes its guards fightable; Tyche and Hermes beside Lucas or Dawn (bosses) | none |
| Route 214 | the Cobble Badge (once the fix lands) | Abigail, Mitchell, Carlos, Devon and Douglas |
| Valor Lakefront | open; the cameramen hold the lake | Jeremy, Reina |
| Route 213 | open | Cyndy, Chelsea, Jared, Travis |
| Pastoria City | open; Barry 4 at the gym door (a boss) | none |
| Pastoria Gym | open | gym trainers only |

Spring Path opens off Route 214 here, and Sendoff Spring's shore beyond it, in vanilla's data as in Oxide's. Nothing happens there until the Distortion World, and its water needs Surf. The encounter tool counts the spring in Barry's split (question 13).

Base-ROM differences: Route 214's boulders, vent, moved trainers and Krystal (`wake-split.md`). Pastoria gained a maid, an Abra pair and a Happiny in the gym, and a clown gift house. The Pokemon Mansion's maid is now the knockout (`maid-knockout.md`). 43 balls were re-stocked across the split's maps.

## Byron's split (cap 53)

| Area | What opens it | Mandatory |
|---|---|---|
| Valor Lakefront | the Fen Badge brings the grunt; Cynthia gives the SecretPotion | the grunt |
| Route 210 South, North | the SecretPotion clears the Psyduck | Alyssa |
| Celestic Town and its ruins | open; Officer Argo at the cave, then Cyrus 1 (bosses) | none |
| Surf | Cyrus beaten sets Celestic's story | none |
| Route 218 to Canalave | Surf; the blockade on its west end clears at Celestic | none |
| Canalave City | Barry 5 on the bridge (a boss) | none |
| Canalave Gym | open | gym trainers only |

The model found no way past Barry 5's bridge to the gym. Celestic's grunt and the Route 218 blockade hold until their story beats, and Mt. Coronet's way from Route 211 East to Eterna waits on Strength.

Iron Island has left the story path. In vanilla, Riley's HM04 made it needed for Strength. Canalave's story goes from Byron's win straight to the library (`VAR_CANALAVE_CITY_STATE` 2, then 3), so Riley's partner section, Jonah and Brenda, the island's ten other trainers, its two grunts and the egg are all optional. `required.py` still lists the island as a crossing.

So the split holds 2 mandatory fights. The candidates on the path are all fixes in place:

- Route 210 North's Ace Trainer Ernest, Veteran Brian, Black Belt Adam and Ninja Boys Joel, Nathan and Davido turn or walk.
- Bird Keeper Brianna and Double Team Zac and Jen look one way but can be walked round.
- Route 218's Guitarist Tony, Sailor Skyler and Fishermen Miguel and Luc can all be walked round, on a route crossed by Surf.

The Surf trainers on Routes 213, 208 and 219 are met here too, all optional.

Base-ROM differences: Riley's battle before his partner section (only the script index) and his eight-way egg (`pokemon-sources.md`). Canalave gained a maid, an Abra pair and a Happiny in the gym, and Celestic and Route 221 an Abra each (hidden). Lake Valor's grunts 1 and 2 were moved and given longer sight (`import_report.md`). Registeel's Iron Ruins hold no Hall of Fame check, behind the same Wailord and Relicanth warp script on Iron Island B3F, so Registeel opens in Candice's split. 44 balls were re-stocked.

## Candice's split (cap 56)

| Area | What opens it | Mandatory |
|---|---|---|
| Canalave Library | Byron's badge | none |
| Lake Valor | the library hides the cameramen; Officer Hesperid, Saturn 1 (bosses) | none |
| Lake Verity | the explosion; Mars 2 (a boss) | grunts 1 and 2 (a pair), grunts 3 and 4 (a pair) |
| Mt. Coronet to Route 216 | the grunts in the north room leave after Lake Verity | none |
| Route 216 | through the mountain | Laura |
| Route 217, Acuity Lakefront | open; Maylene's scene | Dalton, Olivia |
| Snowpoint City and its gym | open | gym trainers only |

Lake Acuity's scene and the Regice entrance follow. Snowpoint Temple's door is held by a script checking the Hall of Fame, which the model does not read.

So the split holds 5. The candidates, fixed in place:

- Route 216's Skiers Bradley, Kaitlyn, Edward and Andrea, Ace Trainers Garrett and Maria, and Black Belt Philip turn or walk.
- On Route 217, Skiers Shawn, Lexie, Bjorn and Madison, Ninja Boys Matthew and Ethan, and Black Belt Luke do the same.
- Lake Valor's grunt 1 can be walked round, and grunt 3 turns.

Ace Trainer Blake and Skier Lexie carry rewards, so they stay optional.

Base-ROM differences:

| Map | Difference | Accounted for |
|---|---|---|
| Lake Verity | grunts 3 and 4 moved to (46,44) and (53,44) with sight 7, and boulders at (46,45) and (53,45) beside them | nowhere; `required.py` reads the pair avoidable once Strength is held, but the boulders cannot be pushed |
| Mt. Coronet 1F North Room 2 | the Iceberg Ruins' warp waits on Galactic leaving Lake Valor and a Wailord and a Relicanth in the party | nowhere |
| Iceberg Ruins | Regice with no Hall of Fame or Regigigas check | nowhere; `pokemon-sources.md` says post-game |
| Snowpoint City | a fisherman who gives the Super Rod | the encounter tool's rods |
| Snowpoint | a maid, an Abra, and an Abra pair with a Happiny in the gym | `pocket-pc.md`, `trainer-survey.md` |

## HQ's split (cap 60)

| Area | What opens it | Mandatory |
|---|---|---|
| Lake Acuity | the Icicle Badge | none |
| Veilstone warehouse | the storage key, then Looker's door | none |
| Galactic HQ B2F, B1F, 1F, 2F, 3F | through the warehouse; gauntlet sections 3 to 6 | B2F's two grunts, 1F's grunt, one 2F grunt, up to four 3F grunts |
| HQ 4F, the control room | the Galactic Key; Cyrus 2 and Saturn 2 (bosses) | none |

The HQ is not modelled, so the 4 to 8 come from `gauntlets.md`'s walk. Scientist Fredrick, Scientist Darrius and two 2F grunts stand in pockets off the way. Mt. Coronet's climb is closed: the cave painting on 2F goes only when the HQ control room's scene hides it. Turnback Cave's entrance opens off Sendoff Spring here, in vanilla's data too (question 13).

Base-ROM differences: B2F gained ten balls, and the HQ's other balls were re-stocked. No trainer or story change.

## Galactic's split (cap 65)

| Area | What opens it | Mandatory |
|---|---|---|
| Mt. Coronet 2F | the HQ control room clears the cave painting; Rock Climb (Icicle) | none |
| the tunnel, or 3F and 4F | gauntlet section 7, or section 8 | 3 by the tunnel; 4 by the south climb |
| Mt. Coronet 5F, 6F | the two climbs meet | none; Officers Moira, Somnu, Hesperid and Argo are bosses, and the model reads all four unavoidable |
| Spear Pillar | the top of 6F | the two grunts, fought beside Barry; Mars and Jupiter, Cyrus are bosses |
| the Distortion World | Spear Pillar | none; Cyrus 3 is the boss |

The Battle Zone (Routes 225 to 230, Stark Mountain, the Survival and Resort Areas) is optional, so its trainers are not counted. So the split holds 4 or 5. Mt. Coronet has no ordinary trainers to fix. Candidates would be new placements on the climb or making the two climbs carry the same count (question 5).

Base-ROM differences: the 3F grunts were moved, and section 8 is drawn on them (`gauntlets.md`). Officer Argo was added on 6F (the tracker). The superbosses on Mt. Coronet's two outside ledges, at the Resort Area and in Stark Mountain wait on the champion's flag (`trainer-survey.md`). Buck's battle on Route 227 is new (only the script index). Route 228's Rock Peak Ruins hold Regirock with no Hall of Fame check, behind the same Wailord and Relicanth warp script. Stark Mountain room 2 gained five balls.

## Volkner's split (cap 68)

| Area | What opens it | Mandatory |
|---|---|---|
| Sandgem lab | the Distortion World's end | none |
| Valor Lakefront to Route 222 | the lab hides the collector and ends the coord event at (724,789) | Sailor Luther |
| Sunyshore City and its gym | open | gym trainers only |

Route 223's water can be surfed from Sunyshore before Volkner. The model reaches the League map's water, but not its buildings, until Waterfall. The encounter tool counts Route 223 in Barry's split.

So the split holds 1. The candidates, fixed in place: Fishermen Brett, Alec, George and Cole, Rich Boy Trey and Tuber Conner look one way but can be walked round. Beauty Nicola, Policeman Thomas, Tuber Holly and Sailor Marc turn. Marc and Conner are an eye-contact pair.

Base-ROM differences: a maid and an Abra in Sunyshore, and an Abra pair with a Happiny in the gym.

## Barry's split (cap 71)

| Area | What opens it | Mandatory |
|---|---|---|
| Route 223 | Surf, Waterfall (Beacon) | none; Oscar and Gabrielle turn, and Colton and Paige can be walked round |
| the League's south side, Victory Road 1F | through Route 223 | gauntlet sections 9 and 10: Bryce, Hana, Mariah, Miles, Edgar, Clinton |
| the League's north side | Victory Road; Barry's last battle (a boss) | none |

Victory Road's 2F and B1F hold eight fights, and its back rooms 14 more trainers, all optional. So the split holds 6. The candidates: Route 223's swimmers fixed in place, or side-room trainers moved onto 1F within the sections' limit of five.

Base-ROM differences: the League gained an Abra pair and a maid. Victory Road's balls were re-stocked, and Marley's battle in the back rooms is new (post-game).

## The League (cap 78)

The Elite Four and Cynthia, with no ordinary trainers. The champion's room sets the flag that opens the base ROM's superbosses.

## The gauntlets against the route

| # | Section | On the path | Mandatory in it | Against 2 to 5, bosses outside |
|---|---|---|---|---|
| 1 | Eterna building 1F and 2F | yes | 4 | meets |
| 2 | Eterna building 3F | yes | Travon, Officer Moira | 1 if Moira is a boss |
| 3 | HQ B2F | yes | 2 | meets |
| 4 | HQ 1F | yes | the grunt; Fredrick is in a pocket | 1, short |
| 5 | HQ 2F | yes | one grunt; three on the detour | 1, short |
| 6 | HQ 3F | yes | up to 4 | meets, not modelled |
| 7 | Mt. Coronet tunnel | one of two climbs | 3 | meets, but avoidable by the south climb |
| 8 | Mt. Coronet 3F to 5F | the other climb | 4 grunts, with Officers Somnu and Moira inside | bosses inside |
| 9 | Victory Road, near half | yes | Bryce, Hana, Mariah | meets |
| 10 | Victory Road, far half | yes | Miles, Clinton, Edgar | meets |

Every section's way back is a refused warp, or Victory Road's line, as `gauntlets.md` records.

## The base ROM's differences outside the route

Item balls were re-stocked on nearly every map with balls (347 balls on 121 maps). The TM pass and the item placements started from the tree, which already holds them. 125 of the 183 wild tables differ, and Oxide's authoring pass rewrote them all (`encounter-authoring-plan.md`). The text banks of 64 maps changed, beside the scripts above.

The Battleground, the Survival Area and the Fight Area were reworked, with the Frontier Brains, Barry and the partners placed there (`frontier-brains.md`, `barry-pool.md`, `battle-zone-plan.md`). The Hall of Origin no longer marks Arceus as caught, and Spear Pillar's script was shortened. None of these was traced further.

## How the reading was made

The base-ROM diff decoded every events file, script file and text bank in both ROMs with `import_base_rom.py`'s readers, matched object events by index, and joined the script index's base-ROM entries to each map. Land data, map matrices and the encounter archives were compared as whole files: land data and matrices are unchanged, and `pl_enc_data` differs in 125 members. Oxide's own terrain differs from vanilla in six blocks, the grass added on 2026-09-26.

The world walk joined every header through its warps, with the overworld as one field. An object on a warp tile blocks the warp. The gate table holds the cycling road's two gates, Valor Lakefront's Route 222 coord event and Veilstone's warehouse coord event. It also holds about two dozen flag-hidden blockers, each opening at the split its flag clears: the Route 209, 212 and 218 blockades, Valor Lakefront's cameramen and collector, the warehouse guards, the HQ doors and bollards, and Mt. Coronet's north-room grunts and cave painting, among others. Each blocker came from a frontier search: for every flag-hidden object beside the strict reach, the walk was rerun without it to see what it opens.

The scratch scripts are in `/home/ian/.claude/jobs/382760ce/tmp/story-route/` (`mapdiff_all.py`, `digest.py`, `worldreach.py`, `frontier.py`). The counts used `required.py` on the branch's tree, `pairs.py`, `trainer-roles.tsv` for the officers' names, and direct sight checks on Mt. Coronet 5F and 6F.

## Ian's answers and the rechecks (2026-10-31)

Built on the branch `overseer-route-fixes`, from `origin/oxide` at d1a5c1b150f. Nothing here was seen in game; each change has an in-game check in `ingame-checklist.md`.

### What was built

Iron Island is back on the story path (question 2). Barry at Canalave's library door waited for HM04 or a Pokemon knowing Strength, which vanilla's Riley gave on the island. The base ROM moved HM04 to Fantina and Oxide put Strength on the Mine Badge, so nothing sent the player there. Barry now waits until Riley's section on Iron Island B2F is done (his state 2, set once the grunts beside him are beaten, egg taken or not), and keeps vanilla's pointer: "Aww, you haven't gone to Iron Island, have you? You've got to toughen up there first, like I told you!" The gap is Oxide's own, so it is not a vanilla fix. The field model finds Canalave's library door unreachable while Barry stands at (37,719), and the gym and the sailor to the island reachable, so the split runs Byron, Iron Island, then the library. Riley's tag battle and the island's other unavoidable trainers now join Candice's split's count, which this page has not recounted.

Named officers are out of the gauntlets (questions 10 and 11). Section 8 on Mt. Coronet now ends on arrival at 5F, so Officers Somnu and Moira are met with healing allowed, nine rows past the arrival. Section 2 is not changed yet, for the reason under "Waiting on Ian".

The Lucky Egg on Route 207 is gone (question 12), with the hand menu before it; the Dowsing Machine stays. Vanilla's Vs. Seeker is not restored: Oxide's Vs. Seeker item is the Pocket PC, already given in Sandgem with the one flag anything reads.

`required.py` holds a boulder that cannot be pushed as a wall (question 14). The game moves a boulder one tile the way it is pushed, from the tile behind it on foot, unless the tile beyond has the collision bit, a wall on that side, or an object; water does not stop it. Seven of the game's 56 boulders become walls, among them Lake Verity's at (53,45) and Route 215's two. No count moved, and the earlier reading of Lake Verity was wrong twice. Its boulder at (46,45) can be pushed west onto the lake from (47,45). And grunts 3 and 4 read avoidable because Surf takes the player round them along the lake's west edge, from (44,45) to the shore at (48,43), boulders or not. So the pair is avoidable in the model whichever way the boulders go, unless a height step the model does not read stops the surf.

### The Regi ruins (question 8, rechecked)

The base ROM's entrances check `FLAG_GALACTIC_LEFT_LAKE_VALOR`, which is misnamed. It is set in one place only: Cynthia's scene at Sendoff Spring, which plays as the player comes out of the Distortion World (`scripts_sendoff_spring.s`, line 46). It is the flag that refills Lake Valor, not the explosion of Byron's split. So all three Regis open in Volkner's split, not in Candice's and Galactic's as read above.

| Regi | Ruin's door | How the player gets there |
|---|---|---|
| Regice | Iceberg Ruins, (15,16) in Mt. Coronet 1F North Room 2 | the room between B1F and Route 216's west end, on the walk to Snowpoint |
| Registeel | Iron Ruins, (14,1) on Iron Island B3F | through the island's inside from B2F, by Canalave's ferry |
| Regirock | Rock Peak Ruins, (785,340) on Route 228 | the Battle Zone ferry from Snowpoint, which sails after Galactic HQ |

Each door's script needs that flag, a Wailord and a Relicanth in the party. Without all three, the script moves the ruin's warp aside and the door leads to a small room with an item instead (NeverMeltIce, Metal Coat, Hard Stone). Inside, every ruin runs the same chain. The state resets on entry unless the Regi was fought; the seven dots each light in turn; the last one makes "something change in the air"; then touching the statue starts the battle at level 30. A catch ends it for good, and a defeat or flight re-arms it on the next entry. Vanilla's chain also needed the Hall of Fame at the statue and at the last dot, and an event Regigigas (a fateful encounter) in the party at the door, which the base ROM took out.

No Regi is in the Distortion World in either tree. Its maps from B1F down have no events, their scripts and text match vanilla, and none has a wild table. Ian's memory most likely comes from the ruins opening the moment the player leaves it. Regigigas stays post-game: Snowpoint Temple's guard needs the National Dex and the Hall of Fame, and B5F needs all three Regis in the party, as in vanilla.

So question 8 narrows: the Regis are catchable from Volkner's split, given a Wailord and a Relicanth. `pokemon-sources.md` still calls them post-game.

### Spring Path, Sendoff Spring and Turnback Cave (question 13, rechecked)

All three are gated until the Distortion World ends, in vanilla as in Oxide. Until the player leaps into the portal in Giratina's room, which sets the hidden location Spring Path (as the Hall of Fame does too), every map load swaps Spring Path's four chunks of the overworld for land data 176, which is wall on every tile (`field_map_change.c`, `MapMatrix_RevealSpringPath`; the name is the wrong way round). Route 214's east edge meets rock. Sendoff Spring is reached only through Spring Path, from Turnback Cave, or by the Distortion World dropping the player there, and Turnback Cave only through Sendoff Spring. The tile model read the unpatched matrix, which is why it found them open.

This changes the page's reading. Summary item 2 loses these three areas, and the Regi ruins move to Volkner's split. The notes under Wake's and HQ's splits are wrong: nothing opens there. Question 13 is answered by the game itself; the encounter tool's Barry's split and post-game placing is close, and Volkner's split would be exact.

### Waiting on Ian

Section 2, the Eterna building's 3F, holds Scientist Travon and Officer Moira, both on 3F. Without Moira it would hold Travon alone, under the 2 to 5, and a section holds a whole map, so no bound falls between them. Travon also sees nothing (a wall stands at his side), so a player may skip him and meet Moira inside the lock. Three ways out:

1. Drop section 2. Travon and Moira become ordinary fights with healing. Section 1 keeps its four grunts, but it lists 3F for the dead-end pocket off 2F's east stairs, so it needs a small code change to end on arrival at 3F's main side. This is the recommended one.
2. Keep section 2 with Travon alone. He stands by the entrance, and beating him lifts the lock before Moira, but the section breaks the 2 to 5 and a player who skips him still meets her locked.
3. Fold Travon into section 1 (five trainers). Moira is then met unlocked only if all five were beaten, so this does not meet the ruling.

### Ian's answers of the evening (branch `overseer-byron-prep`)

All of Iron Island now falls in Byron's split. Canalave's gym opens only once Riley's tag battle on Iron Island B2F is won, which sets his state to 2, the state Barry's library gate already reads. Each time the gym loads it reads that state, or the Mine Badge for a save that beat Byron before the change. Until then, a trigger across the row inside the entrance has the Gym Guide send the player to the island: "Byron only takes challengers who've proven themselves on Iron Island. Ask the sailor at the harbor to take you there, then come back!" Nothing on the way to the island waits on Byron. The sailor's boat from Canalave has no check. Riley outside the island reads the Mine Badge only to pick between two lines the base ROM made identical. Nothing on the island's floors or in their transition scripts reads a badge or a story state from Byron's win; only Byron in the island's house waits, on the National Dex. The field model (test_b1e) reaches the sailor and the gym door from Route 218's gate, walks the island from the boat down to Riley's grunts, finds no way past the gym's entrance row, and finds the library door shut while Barry stands at it. So the split runs Canalave, Iron Island, the gym, then the library. The island was already a crossing of Byron's split in the model, so no count moves; this corrects the note above that put its fights in Candice's split.

Section 2 of the gauntlets is dropped, as proposed under "Waiting on Ian" (option 1, which Ian approved). Section 1 keeps the Eterna building's 3F among its maps for the dead-end pocket off 2F's east stairs, and a new rule in `src/gauntlet.c` closes it on arrival through 3F's main-side stairs, at (2,3), outside Travon's and Moira's sight lines. So Scientist Travon and Officer Moira are fought with the Pocket PC working, and section 1 keeps its four grunts and its refused front door. Section 2's number stays unused, so the later sections keep theirs.

Lake Verity's model is unchanged, because the game's code allows both things Ian recalled as impossible. Surf is offered whenever the player faces a surfable tile and is not on a raised bridge (`PlayerAvatar_CanUseSurf`), and Oxide asks only for the Fen Badge and Celestic's story; vanilla also wanted a party Pokemon that knows Surf, which may be why it never came up in play. None of the likely causes holds: a tile that refuses Surf from that side, a map edge, or a height step. The water at (44,45) and the shore at (48,43) carry no collision bit and no wall behaviour, no map edge is near, and the lake's surface stands at height 8 against the shore's 16, under the 20 that stops a step. A boulder's push refuses only a collision bit, a wall behaviour, a missing tile or an object (`sub_02063E18` in `map_object_move.c`), so Lake Verity's boulder at (46,45) can go west onto the water. The model reads grunts 3 and 4 required without Surf and avoidable with it, whether or not that boulder moves (test_b1e pins this), so the totals stay 68 required, 106 avoidable and 12 never reached, and no split's count moves. If Ian wants the pair mandatory, the map has to change, for instance a collision bit on the lake tiles beside the north-east shore where the player would land (x 47 to 49, rows 36 to 43). That is his call.

# Byron's split: the map before any change

Ian asked on 2026-10-31 for a game plan before Byron's split is touched: "BEFORE WE DO ANYTHING, let's first get a gameplan for this expansive split as there are many, many areas that open up once we get surf, the split itself is super long". He also ruled that Pal Park is required in this split, since otherwise "a super large portion of the game" stays optional and no level space is left later. This page maps the split from Wake's badge (cap 44) to Byron's (cap 53). It was read on the branch `overseer-byron-map` from `origin/oxide` at e42516f671c. No game data changed.

It takes as given what the brief set: Iron Island comes before Byron's gym, because another helper is making the gym wait on Riley's closing tag battle; Surf waits on the Fen Badge and on Cyrus beaten at Celestic Town; Route 214's gate waits on Maylene's badge; the Valor Lakefront grunt belongs to this split; named officers stay outside gauntlets. Spring Path, Sendoff Spring and Turnback Cave stay shut until the Distortion World.

## Summary

What was mapped. Every area the player can reach between the two badges was walked with the story-route study's whole-world tile model, in three stages: the end of Wake's split, the Fen Badge before Surf, and Surf after Cyrus 1. Each area's trainers, current top levels, items and wild tables were read from the tree, the mandatory verdicts from `required.py` and its field model (run on eleven crossings the story path does not list), and the base ROM's changes from the story-route diff. Vanilla's teams for Routes 219 to 221 came from `main`.

What could not be checked. Nothing was seen in game. The ferry to Iron Island is a script, so the island was read room by room. Gyms are not modelled. The chokepoints named below are sight-line readings, not tested placements. The levels in the orders are illustrations for Ian to set. Pal Park has no second-floor map; the lobby's north gallery is the likeliest reading of Argenta's spot.

Three things found that change the plan. First, Pal Park is already open in this split. Its gate's two workers stand only while the National Dex is missing, and the base ROM's Sandgem lab grants the National Dex with the Pokédex, so the park opens the moment Surf reaches Route 221; it is optional today, not closed. Second, Pal Park's first-entry scene sends Prof. Oak to Eterna, and Oak there sets the three Kanto birds roaming at level 60 with no check of his own, so today a player in this split can free them. Third, Lake Valor's full table, which the OxiDex counts here, cannot be reached until the Distortion World refills the lake.

The candidate orders, with Ian's Level Caps sheet's 45 for Cyrus 1 and 49 for Barry 5 as the stretch caps:

| Order | Stretches, each closed by | Pal Park gate | Level climb |
|---|---|---|---|
| A, the south first | Route 210 to Celestic, Cyrus 1 (45); every Surf area, Routes 219 to 221, Pal Park, Route 218, Barry 5 (49); Iron Island and the gym, Byron (53) | Route 218's west-end blockade clears at Pal Park, not at Celestic | One line: each area is required in the stretch it first opens in |
| B, Canalave first | Cyrus 1 (45); Route 218, Barry 5 (49); Iron Island, the south, Pal Park, the gym, Byron (53) | the gym waits on Pal Park as well as on Riley | The south opens at Cyrus 1 but is required after Barry 5, so its trainers sit in the 45 to 48 band, soft for a player under the 53 cap, unless the south is gated too or named early but hard |
| C, the island last | Cyrus 1 (45); Route 218, Barry 5 (49); the south and Pal Park; Iron Island, the gym, Byron (53) | the ferry to Iron Island waits on Pal Park | As B, and the south may also be done before Barry 5, so its place in the climb is loose |

The ways to make Pal Park required:

1. A story gate on a Pal Park flag. Route 218's blockade is a guitarist rehearsing a show with a Clefairy and a Pikachu. Celestic's scene hides it today; the hiding moves to Pal Park's first-entry scene, which already sets its own state variable. Three scripts and one text bank change. This fits Order A.
2. A key item moved to Pal Park. No key item between Cyrus and Byron exists to move, since Surf rides on the badge and the SecretPotion comes before Surf. This way means inventing a pass and a fetch errand. It fits B or C.
3. Argenta's win opens the next stretch. Her win hides the blockade (A) or opens the ferry or the gym (B, C). That makes a Frontier Brain mandatory, against her place as an optional boss.

Recommendation: Order A with way 1, Argenta optional on the lobby's north gallery. If Ian wants the south stretch to close on a fight, way 3 is the same change with her win as the trigger.

Mandatory fights, counted as Ian counts them (every mandatory non-boss, mini-bosses included). The pool is the same in all three orders, since each requires the same maps; only the stretch each fight falls in moves.

| | A | B | C |
|---|---:|---:|---:|
| Today, with Iron Island on the path | 4 to 6 | 4 to 6 | 4 to 6 |
| Fixing three in place (no moves) | 7 to 9 | 7 to 9 | 7 to 9 |
| Adding moves to the necks on Routes 218, 221 and 210 North and the island's pairs | 11 to 16 | 11 to 16 | 11 to 16 |

The range is Riley's two fights, which Ian has not classed. The story-route page's 2 predates Iron Island's return.

Ian's decisions:

1. Which order: A (recommended), B or C?
2. Which way makes Pal Park required: the blockade on a Pal Park flag (recommended), a key item, or Argenta's win?
3. Argenta: optional on the lobby's north gallery, or the mandatory boss closing the south stretch? And is the north gallery the spot you meant?
4. The stretch caps: the sheet's 45 for Cyrus 1 and 49 for Barry 5, or a more even 47 and 50? At 49 Barry 5 fields Primeape, not Annihilape.
5. Thorton at Fuego Ironworks opens at Cyrus 1 in every order: levelled for that, or early but hard like Krystal?
6. Riley's door battle and his partner fight against the two grunts: boss, mini-boss or ordinary, each?
7. Which candidates to fix or move for the count (the table in section 4)?
8. Should Route 210 North become a gauntlet section leading up to Argo and Cyrus 1? It would need a line at its south end, like Victory Road's.
9. Eterna's Oak frees the Kanto birds at 60 as soon as the player has seen Pal Park, which is possible today: may his house wait on the Hall of Fame, so they stay post-game?
10. May the OxiDex move Lake Valor's table from Byron's split to Volkner's?

Next steps:

| Step | Who | Time |
|---|---|---|
| Answer the questions above | Ian | 30 minutes |
| The Pal Park gate and Eterna's Oak, with the field model and census tables | a worker | 2 hours |
| The fixes and moves for the count, each checked with `required.py` | a worker | 2 to 3 hours |
| The level climb and rebuild of about 60 ordinary teams, in play order | a worker | a day |
| The bosses in checked stages: Argo 1 and Cyrus 1's drafts to Ian, Barry 5 from the pool, Byron, Thorton and Argenta from Ian's sixes | the Overseer and a worker | 1 to 2 hours each, plus Ian's look |
| The in-game check of the new gates and fights | Ian | 45 minutes with the test kit |

## 1. The areas, and what opens each

The split opens in two steps. The Fen Badge brings the Valor Lakefront grunt; his defeat brings Cynthia's SecretPotion, which clears the Psyduck from Route 210 South, which opens Route 210 North, Celestic Town and Route 211 East. Argo stands at the ruins' door and Cyrus 1 waits inside. Beating Cyrus sets Celestic's story, which allows Surf and hides Route 218's blockade. Surf then opens the rest: Route 218 to Canalave, Barry 5 on Canalave's bridge, the ferry to Iron Island from beyond the bridge, the gym beyond it too, Routes 219 to 221 south of Sandgem, Fuego Ironworks down Route 205 South's river, and the water of a dozen maps from earlier splits.

### Before Surf (the Fen Badge)

| Area | Opens with | Trainers today (top levels) | Mandatory today | Capture area |
|---|---|---|---|---|
| Valor Lakefront | the Fen Badge | the grunt, one Toxicroak at 41 | the grunt (the SecretPotion follows) | Valor Lakefront, Wake's |
| Route 210 South, north end | the SecretPotion | Ninja Boys Fabian, Brennan, Bruce (41) | none; all three look every way and are still avoidable | Route 210, Maylene's |
| Route 210 North | the SecretPotion | 9 reachable, 39 to 52; Ace Trainers Alyssa and Ernest have six each at 50 to 52 | Alyssa; Veteran Brian reads required but turns | Route 210, shared with the south |
| Route 211 East | from Celestic | 4, at vanilla's 31 to 34 | none; a dead end against Mt. Coronet's Strength boulder | Route 211, Gardenia's |
| Celestic Town and the ruins | Route 210 North | Officer Argo at the ruins' door, Cyrus 1 inside (both 51 to 53 in the tree) | Argo, talked to at the door | Celestic Town, water only, after Cyrus |

Dragon Tamer Patrick on Route 210 North stands behind Rock Climb, so he is HQ's. Route 210 North's map has bridges, which the model reads flat. Base-ROM changes here are re-stocked balls on Routes 210 and 211 and in Celestic, and a hidden teleport Abra in Celestic. Route 210 North's balls hold a Smoke Ball, Wave Incense, TM30 and a Red Shard; Route 211 East's a Carbos; Celestic's a Dragon Fang.

### After Surf (Cyrus 1 beaten)

| Area | Opens with | Trainers today (top levels) | Mandatory today | Capture area |
|---|---|---|---|---|
| Route 218 | Surf; its west-end blockade clears at Celestic | Tony, Skyler, Miguel, Luc (44 to 45) | none | Route 218, water from Roark's split, grass from here |
| Canalave City | Route 218 | Barry 5 on the bridge (51 to 53) | Barry 5, a boss; the gym and the ferry both lie past the bridge | Canalave City, water only |
| Canalave Gym | past the bridge, and Riley's closing fight (the other helper's gate) | 7 gym trainers, 49 to 52; Byron 51 to 53 | gym trainers only | none |
| Iron Island | Sailor Eldritch's ferry, past the bridge | 12 trainers, 35 to 51; Riley at the door (52); two grunts (46) | Riley's door battle, Jonah and Brenda, the grunts; Picnicker Summer reads required but wanders | Iron Island, one name for seven tables |
| Routes 219 to 221 | Surf from Sandgem | 15 trainers, 43 to 52; Ace Trainers Jake and Shannon have six each at 50 to 52 | none (Swimmer Dillon reads required but wanders) | Routes 219 (fishing from Roark's), 220, 221 |
| Pal Park | Route 221; the workers at its gate stand only without the National Dex, which Oxide grants with the Pokédex | none | optional today | no wild table |
| Fuego Ironworks | Surf down Route 205 South's river | Workers Dillan, Holden, Conrad (44 to 46) | none; Mr. Fuego, a few steps in, is where Thorton goes | Fuego Ironworks |
| Old maps' water | Surf | Fisherman Cody (Route 208, 44); Swimmers Sheltin, Evan, Mary, Haley and Sailor Paul (Route 213, 43 to 44); Veteran Grant (Oreburgh Gate B1F, 45) | none | none new: each map's name was taken earlier |
| Lake Valor | not in this split | none | none | Lake Valor, closed (below) |

Iron Island runs one way. The door to 1F is the only way in, and Riley stands on the tile before it: talking to him starts the base ROM's battle (Lucario 52, Absol 50, Ursaring 50), after which he gives a Sitrus Berry and walks in. The way runs 1F, B1F's right room (Summer), then B2F's left room, where Riley joins as a partner at its top. From there every battle is a tag battle beside him, and he heals the party after each one (the game heals with a partner after every won battle). B2F holds four pairs: Hikers Damon and Maurice, Black Belt Kendal and Battle Girl Tyler, Workers Brendon and Quentin, and Ace Trainers Jonah and Brenda, the only pair the model finds unavoidable. Two grunts at the room's foot close the section with the tag battle, then the egg. B3F leads back out, and its outside door is one-way, down a ledge. B1F's left room (Camper Lawrence) and B2F's right room (Workers Noel and Braden) are dead ends. The island's balls hold a Protector, Yellow Shard, Max Repel, Escape Rope, Revive, Ultra Ball, Dusk Ball, Max Potion, HP Up, Red Shard, Magnet, Elixir, TM23 and a Shiny Stone, all re-stocked by the base ROM. The Iron Ruins' Metal Coat and Registeel wait for the Distortion World (story-route's recheck).

Surf reaches these items on older maps: TM24 and an Electirizer at Valley Windworks, a Rare Candy, Leaf Stone, Miracle Seed and Ultra Ball in Floaroma Meadow, TM03 and a Luck Incense on the Ravaged Path, an HP Up and Sea Incense on Route 204 South, a Dawn Stone and Protein in Mt. Coronet 1F South, TM31 in Oreburgh Gate B1F, TM38 at Lake Verity, a Max Revive and Water Stone on Route 213, TM84 and a Rose Incense and Iron on Route 212, a Mystic Water in Pastoria and a Rare Candy on Route 214. Three of those are evolution stones, which the stone census counts from this split. Verity Cavern opens too, with Mesprit hidden until later.

Lake Valor's state. The cameramen on Valor Lakefront hold the lake until Canalave's library scene, after Byron's badge. The explosion then drains it, and the drained map has no wild table. The full lake returns only after the Distortion World. So the full lake's table (38 to 41: Absol, Skarmory, Weavile, Honchkrow and others) is first met in Volkner's split, though the OxiDex places it in Byron's (question 10).

The wild tables here stand at 27 to 33 on land (Iron Island 30 to 33) and up to 42 on the water. The new capture areas in the split are Celestic Town and Canalave City (water only), Iron Island, Routes 220 and 221 and Fuego Ironworks; Route 218's grass and Route 219's surfing count under names first used in Roark's split.

## 2. Three play orders

An honour cap closes a stretch on its boss, as Barry 4's 42 closes the first part of Wake's split. Ian's Level Caps sheet already holds three numbers for this split: Cyrus 1 at 45, Barry 5 at 49 and Byron at 53. Cyrus 1 is also named among the mini-bosses that get an honour cap of their own (`rulings-detail.md`). Pal Park's stretch gets a cap only if Argenta becomes its required closing boss. Ordinary trainers climb under each cap, never at it and very rarely one under, so the bands below are those caps less one or two.

The tree's levels do not climb yet. Most of the split's ordinary trainers are vanilla-sized teams at the base ROM's levels, 43 to 48, beside base-ROM Ace Trainers at 50 to 52 and every boss at 51 to 53. Route 211 East is still at vanilla's 31 to 34, and the Valor Lakefront grunt has one Pokemon.

### Order A, the south first (recommended)

| Stretch | Areas | Closed by | Band for ordinary trainers |
|---|---|---|---|
| 1 | Valor Lakefront's grunt, Route 210, Route 211 East, Celestic, Argo 1 | Cyrus 1 (45) | 42 to 44 |
| 2 | every Surf area (Fuego and Thorton, the old maps' water), Routes 219 to 221, Pal Park and Argenta, Route 218 | Barry 5 (49) | 45 to 48 |
| 3 | Iron Island (Riley, the partner section, the grunts), the gym | Byron (53) | 50 to 52 |

Every area here is required in the stretch it first opens in, so the earliest-reach rule and the play order agree. The south is a dead end off Sandgem, done between Celestic and Route 218 by flying, and Fuego and the old water are side trips in the same stretch. The cost is that Canalave's arrival comes late in the stretch, with only Route 218 and Barry 5 after Pal Park; stretch 3 then carries the island alone before the gym.

### Order B, Canalave first

| Stretch | Areas | Closed by |
|---|---|---|
| 1 | as A | Cyrus 1 (45) |
| 2 | Route 218, Canalave's bridge | Barry 5 (49) |
| 3 | Iron Island, Routes 219 to 221 and Pal Park, the gym | Byron (53) |

This follows vanilla's geography most closely. But the south opens at Cyrus 1 in every order, so under the earliest-reach rule its trainers sit in stretch 2's band, while the order requires them in stretch 3. A player who honours the stretch caps reaches them under 53 and finds them soft. That holds unless Ian names the south early but hard, or a second gate holds Route 219's water (a blockade on Sandgem's beach until Riley's fight, at about A's cost again).

### Order C, Pal Park before the island

| Stretch | Areas | Closed by |
|---|---|---|
| 1 | as A | Cyrus 1 (45) |
| 2 | Route 218, Canalave's bridge | Barry 5 (49) |
| 3 | Routes 219 to 221 and Pal Park | Argenta, if required (about 51) |
| 4 | Iron Island, the gym | Byron (53) |

The ferry waits on Pal Park. B's level problem remains, and since nothing holds the south until Barry 5, the player may also do it before him, so its place in the climb is loose. It gives the split a fourth cap, which only pays if Argenta is required.

## 3. Making Pal Park required

### What is there today

| Place | In Oxide | In vanilla |
|---|---|---|
| Route 219 | Tubers Trenton (Gastrodon, Dewgong 43) and Mariel (Azumarill, Gastrodon 43) on an islet, each with a held-item reward (Eject Button, Red Card); an Antidote ball; surf and rod tables | the same two tubers with Shellos and Marill at 31 to 33 |
| Route 220 | seven swimmers, 43 to 45, one or two Pokemon each, two with rewards (Mirror Herb, Zoom Lens); Carbos, Splash Plate and Max Repel balls; water only | the same seven at 30 to 35 |
| Route 221 | Swimmers Dillon and Vanessa (46), Fisherman Cory (44, Clear Amulet reward), Collector Ivan (Togekiss 47), Ace Trainers Jake (Dusknoir 50 to Gallade 52) and Shannon (Victreebel 50 to Arcanine 52); Protein, TM81, Ultra Ball and Pure Incense balls; a land table of later species at 28 to 31 | the same trainers at 30 to 36, Jake and Shannon with two and three Pokemon |
| Route 221's house | a man who gives a Black Belt, Expert Belt or Focus Sash for a Pokemon of the day's level | the same |
| Pal Park's lobby | vanilla's, unchanged by the base ROM: Oak's first-entry scene with a Pokétch app, the Catching Show's desk, two Pokétch-app gifts for showing a Snorlax or a Kecleon, and the north gallery | the same |
| Pal Park's field | the Catching Show for six Pokemon migrated from a GBA cartridge; no wild table | the same |

Route 221's map script hides the two workers at Pal Park's gate only when the National Dex is held. Vanilla gives it after the League, so its park is post-game. The base ROM's Sandgem lab turns it on as Rowan hands over the Pokédex (`scripts_sandgem_town_pokemon_research_lab.s`, line 511), which `battle-zone-plan.md` already notes, so in Oxide the workers are gone on every visit and the park opens with Surf in this split. Oxide's own "always national dex" change touches only the Pokédex screen. The item census's gate reader (`gates.py`) still reads every National Dex check as post-game, so anything gated only on it counts later than it opens. The reward table plans TM81 for Pastoria's gym and a Lum Berry in its ball; the tree still holds TM81. The Route 221 house's Expert Belt and Focus Sash are vanilla gifts no doc mentions.

One problem comes with the park being open, and it is there today. Oak's first-entry scene in the lobby clears his hidden flag in Eterna's south house. Talking to Oak there hands over an Upgrade and sets Articuno, Zapdos and Moltres roaming at 60. His script checks nothing but its own flags, since vanilla's National Dex gate on the park did that job, so a player in Byron's split can chase three level-60 birds. A check on the Hall of Fame in Eterna's house keeps them post-game (question 9); a National Dex check would not, as it is already set.

### The three ways

1. **A story gate on a Pal Park flag**, as Barry at the library waits on Riley. Celestic's scene after Cyrus sets `FLAG_HIDE_ROUTE_218_BLOCKADE` today (`scripts_celestic_town.s`, line 66). The set moves to Pal Park's lobby, into Oak's first-entry scene, which already ends by setting `VAR_PAL_PARK_LOBBY_STATE` to 1. The blockade is a guitarist rehearsing a show with a Clefairy and a Pikachu, and a fisherman watching, on the six-tile neck by Canalave's gate. One new line can say they are rehearsing for Pal Park's show and will move once someone has seen it. It reads as a natural errand in Order A. The cost is the moved flag, Eterna's Oak, one text line, a row for the field model's gate table and the census's gate reader (`gates.py`), and new crossings for Routes 219 to 221 in `required.py`. In B the same gate goes on the gym's door beside Riley's, and in C on Eldritch's ferry; both read as arbitrary, since nothing ties Pal Park to Byron or the boat.
2. **A key item moved to Pal Park.** Nothing between Cyrus and Byron needs a key item. Surf works on the badge and Cyrus's flag, the SecretPotion comes before Surf and cannot move past it, and the library, gym and ferry ask for nothing. So this way means a new requirement: a pass for Eldritch's ferry from Pal Park's desk, say, in a spare key item's slot. It costs that item's record and text, a give script and a check, on top of the Eterna fix, and reads as a fetch errand. It suits B or C.
3. **Argenta's win opening the next stretch.** She stands on the lobby's north gallery, and her win sets the flag: the blockade in A, the ferry in C, the gym in B. It costs her trainer record from Ian's six, a placement and battle script like Dahlia's, and the Eterna fix. It gives the south stretch a closing boss and its own cap. It also turns a Frontier Brain from Ian's optional bosses (2026-09-27) into a mandatory one, and she then counts as a boss, outside the 10 to 15.

The recommendation is Order A with way 1. If Ian wants a fight at the end of the south stretch, way 3 in Order A is the same change with Argenta's win setting the flag instead of Oak's scene.

## 4. The mandatory count

Ian's rules apply: every mandatory fight that is not a boss counts, mini-bosses included; a trainer who turns, spins or walks is optional; a pair is one fight; gym trainers do not count. "Today" is the tree with Iron Island back on the path.

| Fight | Map | Kind | Today | What would make it count | Stretch in A / B / C |
|---|---|---|---|---|---|
| The grunt | Valor Lakefront | ordinary | mandatory | | 1 / 1 / 1 |
| Ace Trainer Alyssa | Route 210 North | mini-boss | mandatory | | 1 / 1 / 1 |
| Officer Argo 1 | Celestic Town | mini-boss | mandatory | | 1 / 1 / 1 |
| Riley at the door | Iron Island | not classed | mandatory | counts unless Ian makes it a boss | 3 / 3 / 4 |
| Ace Trainers Jonah and Brenda, beside Riley | Iron Island B2F | mini-boss | mandatory | | 3 / 3 / 4 |
| The two grunts, beside Riley | Iron Island B2F | not classed | mandatory | counts unless Ian makes it a boss | 3 / 3 / 4 |
| Veteran Brian | Route 210 North | ordinary | turns | fixed in place: the model reads him required | 1 / 1 / 1 |
| Picnicker Summer | Iron Island B1F | ordinary | wanders | fixed in place: required | 3 / 3 / 4 |
| Swimmer Dillon | Route 221 | ordinary | wanders | fixed in place: required | 2 / 3 / 3 |
| One of Tony, Skyler, Miguel or Luc | Route 218 | ordinary | avoidable | moved to the six-tile neck by Canalave's gate, where the blockade stands, looking along it | 2 / 2 / 2 |
| Jake and Shannon as a pair, or Ivan | Route 221 | mini-boss (pair) or ordinary | avoidable | moved beside the two-tile neck before Pal Park's gate, where the workers stand | 2 / 3 / 3 |
| One to three of Ernest, Joel, Nathan, Davido, Adam, Brianna, Zac and Jen | Route 210 North | Ernest a mini-boss, the rest ordinary | avoidable even seeing every way | moved to chokepoints, not read here | 1 / 1 / 1 |
| One or two of the B2F pairs | Iron Island B2F | ordinary, beside Riley | avoidable | fixed across the walk to the grunts | 3 / 3 / 4 |

That gives 4 to 6 today, 7 to 9 with the three fixes in place, and 11 to 16 with the moves, in every order. Routes 219 and 220 are open sea at least nine tiles wide, so their nine swimmers stay optional; Fuego's workers and Route 211 East's four are off the path. Jake and Shannon field twelve Pokemon together, so as a pair fought alone they need Ian's leave or smaller teams; Jonah and Brenda's eight are fought beside Riley, which the six-Pokemon rule does not cover.

The split holds no gauntlet section. Route 210 North is the natural one: one way to Celestic, its fights ending before Argo and Cyrus 1, both left outside. It would need a line at its south end like Victory Road's, since no warp bounds it (question 8). Iron Island's descent before Riley joins holds only Riley's door battle and Summer, too few.

## 5. The fights by kind

| Fight | Kind | Where | Today | Drafted |
|---|---|---|---|---|
| Cyrus 1 | boss (Cyrus); also on the mini-boss honour-cap list | Celestic ruins | Gliscor to Salamence, 51 to 53 | yes: Crobat 51 to Salamence 53 on `overseer-galactic-teams`, not yet put to Ian (`galactic-drafts-recheck.md`, question 8); its Salamence's sweep rate is to be reported |
| Barry 5 | boss (rival) | Canalave's bridge | Ambipom to the starter, 51 to 53 | planned: `barry-pool.md` gives the three elements, Staraptor, Snorlax and Annihilape (Primeape if his cap is under 50) |
| Byron | boss (leader) | Canalave Gym | Bastiodon to Metagross, 51 to 53 | no |
| Thorton | boss (Frontier Brain), optional | Fuego Ironworks, Mr. Fuego's spot | not placed; a dummy in the Battleground | Ian's six (Bronzong, Magnezone, Toxapex, Dhelmise, Turtonator, Guzzlord), permanent Trick Room, his prize a fully evolved starter at 40 |
| Argenta | boss (Frontier Brain), optional unless way 3 | Pal Park, tentative | not placed | Ian's six (Skarmory, Annihilape, Dubwool, Whiscash, Meowscarada, Pheromosa), items as the reward |
| Officer Argo 1 | mini-boss (named officer) | Celestic ruins' door | Kecleon to Armaldo, 51 to 53 | yes: Claydol to Polteageist, 48 to 50, on the same branch (question 7 there); Ian loves the theme and wants the White Herb Shell Smash Polteageist's sweep rate |
| Ace Trainers Alyssa, Ernest | mini-boss | Route 210 North | six each, 50 to 52 | no |
| Ace Trainers Jonah and Brenda | mini-boss (pair, beside Riley) | Iron Island B2F | four each, 50 to 51 | no |
| Ace Trainers Jake and Shannon | mini-boss | Route 221 | six each, 50 to 52 | no |
| Ace Trainers Cesar, Breanna | gym trainers | Canalave Gym | six each, to 52 | no |
| Riley at the door | not classed: he is neither a partner fight nor any kind the ruling names | Iron Island | Lucario 52, Absol 50, Ursaring 50 | no |
| Riley's partner fight | not classed (Ian, 2026-10-31) | Iron Island B2F | two grunts, three Pokemon each at 46 | no |

Every other fight here is an ordinary trainer, about 60 of them across Routes 210 to 221, Iron Island, Fuego and the old maps' water. The gym's seven guards are gym trainers.

## How this was read

The world walk reused the story-route study's `worldreach.py`, with three gate rows added: Route 218's blockade and Celestic's grunt gone once Cyrus is beaten. Its strict reading keeps every other flag-hidden object standing, which held Pal Park's two workers in place; reading Route 221's map script and the lab's corrected that. It was run for the end of Wake's split, the Fen Badge before Surf and Surf after Cyrus, and each object on every map was marked by the first stage that reaches a tile beside it (`reach.py`). Trainers came from the map events and their files, with the OxiDex's split tags (`trainers.split_map`), the census's roles and rewards (`trainer-roles.tsv`) and `required.py`'s verdicts (`trainers.py`). `required.crossing` was run on eleven crossings its table lacks: Iron Island B1F's right room and B2F's left room (to B3F and to the grunts), Routes 219, 220 and 221 (to Pal Park's lobby), Fuego Ironworks' building (to Mr. Fuego and to its TM ball), Route 218, Route 210 North and Route 211 East. The necks on Routes 218 and 221 and the open water of 219 and 220 were read off maps of each route's reachable tiles and sight lines. Items were read from each ball's script number (`items.py`). Wild tables came from `res/field/encounters/` and the OxiDex's location names, vanilla's teams from `main`, and the base ROM's changes from the story-route study's diff of every map. The Oak and bird finding comes from reading `scripts_pal_park_lobby.s` and `scripts_eterna_city_south_house.s`, and the partner heal from `encounter.c`. The scratch scripts are in `/home/ian/.claude/jobs/382760ce/tmp/byron-map/`.

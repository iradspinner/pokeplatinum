# Byron's split: mandatory fights and the level climb

Byron's split runs from Wake's badge (cap 44) to Byron's (cap 53). Ian set it on 2026-10-31 (`byron-split-map.md`, and the tracker's Scheduled entry): order A, the south first, with stretches closing at Cyrus 1 (honour cap 47), Barry 5 (50) and Byron (53); Iron Island before the gym; the Pal Park partner double opening Barry 5's fight; about 20 mandatory fights; Riley's two fights as mini-bosses; and no gauntlet on Route 210 North. This page is the split's trainer pass, done as Wake's was, on the branch `overseer-byron-trainers`. Ian answered its first draft's questions the same day, and this page records the result.

## Summary

The split counts 22 mandatory fights, gym trainers apart, mini-bosses included and a pair counted once. Oxide has 6 today, 7 with the Pal Park double the scripts helper is building. Fifteen of the 22 are this branch's: four fights fixed in place to look one way and eleven moved, ten within their own maps and one, Swimmer Vincent, from Route 220 to Route 219. 65 ordinary, mini-boss and gym teams were rebuilt and climb by stretch, their tops running 43 to 45 before Cyrus 1, 46 to 48 before Barry 5, and 50 to 52 before Byron, where only the gym's last guard reaches 52. 52 of their 231 members are Oxide's later species. No reward sits on a mandatory trainer, so none moved. Every team's AI flags are now set on purpose, by a new guide to four of them (`battle-ai/flags-guide.md`).

| Stretch, closed by | Mandatory fights | Of them, this branch's |
|---|---:|---:|
| 1, Cyrus 1 (47) | 9 | 6 |
| 2, Barry 5 (50) | 7 | 6 |
| 3, Byron (53) | 6 | 3 |

Ian's answers (2026-10-31), as applied:

1. All thirteen picks of the first draft stand: Fabian, Brianna, Zac and Jen, Ernest, Adam, Brian, Dillon, Ivan, Tony and Skyler, Summer, Kendal and Tyler, and Brendon and Quentin.
2. Ace Trainers Jake and Shannon move to Pal Park's door as a mandatory pair, three Pokemon each. Jake's lone Trick Room Dusknoir made no sense, so his three now share one idea, critical hits. Shannon's six were "extremely scary but probably too hard", so her three keep the sun and its sweeper and lose the setup.
3. One more mandatory fight in the middle stretch: Swimmer Vincent. No fixed look closes Route 219's or Route 220's sea where any swimmer stood, and Route 219's strait needs a sight of 8, which no trainer in the game has, so Vincent moved from Route 220 to the water beside Route 219's islet, which every way south crosses.
4. Grant's Golem keeps Explosion behind its Custap Berry. From here Ian allows more trade moves where a team's idea calls for one, so Veteran Brian's Cofagrigus takes Destiny Bond and Worker Gerardo's Forretress takes Explosion. Ian calls these trade moves, not forced trades, since the player can play round them.
5. Argo 1, the Pal Park double and Riley's two fights count as mini-bosses.
6. The AI flags are set on purpose for each team, by the guide, and the section on AI flags below says why each team that carries one of the four flags' moves has the flags it has.

Nothing waits on Ian from this page but the in-game checks.

Next steps:

| Step | Who | Time |
|---|---|---|
| Land the branch with `merge-branch.sh`, then `sync-docs.sh` on oxide | the Overseer | 30 minutes |
| Play the split's mandatory fights with the test kit's warps | Ian | 45 minutes |

What is unverified:

- Nothing has been seen in game. The moves come from the tile model.
- No fight was read by the scorer, under the standing ruling.
- The doubles and Riley's tag battles were checked as singles.
- The speed check below reads the box's likely fast answers as eight reference species at each cap, not goal 3's boxes, and no damage check was run.
- The flag guide's chances are worked out from the script's numbers against the best attack alone, not watched in a battle.
- The trainer AI does not see some held items these teams carry, such as Weakness Policy and Rocky Helmet.

## The mandatory fights

Ian's rules of 2026-10-29 apply, with his word of 2026-10-31 that mini-bosses count. Gym trainers do not count. A trainer who turns, spins or walks is optional. A pair, or a double against one trainer file, is one fight. Two trainers fought alone together field six Pokemon at most; a pair fought beside a partner, as on Iron Island, is a different case.

The story path in order A runs Valor Lakefront, Route 210 South's north end, Route 210 North and Celestic Town, then, with Surf, the south (Routes 219 to 221 and Pal Park), Route 218, Canalave, the ferry to Iron Island and Canalave's gym. Route 211 East is a dead end off Celestic, and Fuego Ironworks and the old maps' water are side trips, so their trainers are optional.

| # | Fight | Map | Stretch | How it is known |
|---:|---|---|---|---|
| 1 | The Galactic grunt | Valor Lakefront | 1 | a story battle; Cynthia's SecretPotion follows it |
| 2 | Ninja Boy Fabian (moved) | Route 210 South | 1 | required.py, after the move |
| 3 | Bird Keeper Brianna (moved) | Route 210 North | 1 | required.py, after the move |
| 4 | Ace Trainer Alyssa, a mini-boss | Route 210 North | 1 | required.py, unchanged |
| 5 | Zac and Jen's double (fixed) | Route 210 North | 1 | required.py without Surf, after the change |
| 6 | Ace Trainer Ernest, a mini-boss (fixed) | Route 210 North | 1 | required.py without Surf, after the change |
| 7 | Black Belt Adam (moved) | Route 210 North | 1 | required.py, after the move |
| 8 | Veteran Brian (fixed) | Route 210 North | 1 | required.py, after the change |
| 9 | Officer Argo 1, a mini-boss | Celestic Town | 1 | talked to at the ruins' door |
| 10 | Swimmer Vincent (moved from Route 220) | Route 219 | 2 | required.py, on the new Route 219 crossing |
| 11 | Swimmer Dillon (moved) | Route 221 | 2 | required.py, on the new Route 221 crossing |
| 12 | Collector Ivan (moved) | Route 221 | 2 | required.py, on the new Route 221 crossing |
| 13 | Ace Trainers Jake and Shannon, mini-bosses, one double (moved) | Route 221 | 2 | required.py and pairs.py, after the move |
| 14 | The Pal Park partner double, beside Lucas or Dawn | Pal Park | 2 | the scripts helper's gate; it opens Barry 5's fight |
| 15 | Guitarist Tony (moved) | Route 218 | 2 | required.py, after the move |
| 16 | Sailor Skyler (moved) | Route 218 | 2 | required.py, after the move |
| 17 | Riley at the door, a mini-boss | Iron Island | 3 | talked to on the tile before the only door |
| 18 | Picnicker Summer (fixed) | Iron Island B1F | 3 | required.py, on the new B1F crossing |
| 19 | Black Belt Kendal and Battle Girl Tyler, beside Riley (moved) | Iron Island B2F | 3 | required.py, after the move |
| 20 | Workers Brendon and Quentin, beside Riley (moved) | Iron Island B2F | 3 | required.py, after the move |
| 21 | Ace Trainers Jonah and Brenda, mini-bosses beside Riley | Iron Island B2F | 3 | required.py, unchanged |
| 22 | Riley's partner fight against the two grunts, a mini-boss | Iron Island B2F | 3 | a story battle that gives the egg |

The bosses are Cyrus 1, Barry 5 and Byron. Thorton and Argenta are optional Frontier Brains. Canalave's seven gym trainers are gym trainers.

### The trainers moved

Each keeps its class and script, and now looks one fixed way. A tile is written (x, z).

| Trainer | From | To | Why it is safe |
|---|---|---|---|
| Ninja Boy Fabian | Route 210 South (562, 570), disguised in the grass, seeing every way, sight 1 | (561, 546), looking east, sight 4 | The way north to Route 210 North leaves the fog through four tiles (x 562 to 565). He stands west of them and sees all four. |
| Swimmer Vincent | Route 220 (198, 911), walking east and west, facing sides | Route 219 (178, 886), in the water, looking west, sight 6 | Route 219's islet joins the north sea to the south one, and its north row (x 172 to 177) is crossed by every way south. Vincent sees all of it from the water at its east end. Tuber Trenton walks east and west on the row below, so he never looks into Vincent's row, and the two make no double. |
| Bird Keeper Brianna | Route 210 North (511, 533), looking south, sight 2 | (561, 541), looking east, sight 4 | The way in from Route 210 South is three tiles wide (x 563 to 565). She stands west of it and sees across it. |
| Zac and Jen | (537, 528) and (537, 529), Jen walking, sight 2 | the same tiles, Jen looking east, sight 6 | The clearing below the column north is crossed on row 529; Jen sees the six tiles east of her (x 538 to 543). Zac follows her and does not move. |
| Ace Trainer Ernest | (534, 522), looking north and east, sight 4 | the same tile, looking east, sight 5 | The column from the clearing reaches the long bridge's row at x 538 and 539, which he sees. |
| Black Belt Adam | (518, 540), facing sides, sight 4 | (498, 530), looking south, sight 3 | The passage to Celestic is crossed north to south between the bike bridge and Brian's line; Adam sees down column 498. |
| Veteran Brian | (494, 528), looking south and west, sight 3 | the same tile, looking south, sight 3 | South covers the passage's last crossing before Celestic. |
| Swimmer Dillon | Route 221 (235, 912), wandering north and south, sight 2 | (235, 910), looking south, sight 4 | No fixed look makes him required where he stood; two tiles north he sees down the gap between the rocks. |
| Collector Ivan | Route 221 (288, 915), looking north, sight 3 | (305, 912), looking east, sight 2 | Pal Park's gate is reached only through two tiles (x 306 and 307, row 911); Ivan sees the two tiles in front of them, where the gate's workers stand when they are shown. |
| Ace Trainer Jake | Route 221 (305, 917), looking west, sight 3 | (305, 910), looking east, sight 2 | Past the neck, the two tiles before Pal Park's door, (306, 910) and (307, 910), lead to its two warps. Jake stands west of them and Shannon east, each seeing both, so they see the player together and fight as one double of three and three. The two corner tiles behind them, (304, 910) and (309, 910), become dead ends and hold nothing. |
| Ace Trainer Shannon | Route 221 (277, 923), looking around, sight 3 | (308, 910), looking west, sight 2 | As Jake. Ivan's line, two tiles south, shares no tile with theirs, so Ivan is fought first and alone. |
| Guitarist Tony | Route 218 (80, 753), looking south, sight 4 | (71, 753), looking south, sight 4 | Canalave's gate (x 70, rows 754 and 755) is entered across column 71, which he sees. |
| Sailor Skyler | Route 218 (76, 746), looking north and east, sight 3 | (72, 757), looking north, sight 4 | Every other way to the gate crosses column 72, which she sees. Her line and Tony's share no tile, so they are two fights, never one double. |
| Picnicker Summer | Iron Island B1F (17, 16), wandering north and south, sight 3 | the same tile, looking south, sight 3 | South covers the corridor down to B2F. |
| Black Belt Kendal | Iron Island B2F (36, 18), looking south, sight 2 | (28, 21), looking south, sight 4 | The way down runs through a corridor one tile wide (x 28, rows 22 to 25). Kendal stands at its top and Tyler at its foot, each seeing all of it, so they see the player together, as a pair beside Riley must. |
| Battle Girl Tyler | (36, 21), looking north, sight 2 | (28, 26), looking north, sight 4 | As Kendal. |
| Worker Brendon | (15, 25), looking west, sight 1 | (26, 24), looking south, sight 2 | After the corridor the way turns west through column 26, rows 25 and 26. Brendon stands above and Quentin below, both seeing both tiles. |
| Worker Quentin | (14, 28), looking north, sight 3 | (26, 27), looking north, sight 2 | As Brendon. |

The checks, each run on the edited files:

- required.py reads all eighteen required. Ernest and Jen read required only without Surf. required.py gives the whole split Surf, and the river lets a surfer round them, but the player meets them before Cyrus 1, so before Surf. The census therefore lists Ernest and Zac and Jen as avoidable, and this page counts them as mandatory.
- From every warp and map edge, in Wake's, Byron's and Candice's splits, the player still reaches every tile reachable before on all eight maps, but the two dead-end corners beside Jake and Shannon.
- No moved trainer stands on a warp, sign, hidden item, trigger or another object.
- `pairs.py`'s eye-contact pairs gain exactly one, Jake and Shannon (two shared tiles, neither seeing a tile the other does not), and lose none: Iron Island's pairs stay pairs.
- No scripted walk crosses the new tiles. The scripts of Routes 210, 218, 219 and 221 and Iron Island B1F move no one, and B2F's walk only where Riley meets the player by the entrance and at the grunts.
- Route 219 (from Sandgem to Route 220), Route 221 (from Route 220 to Pal Park's lobby) and Iron Island B1F's right room are new crossings in `required.py`. `test_b1e` passes 11 of 11, its totals repinned from 68 required, 106 avoidable and 12 never reached to 83, 101 and 12. Its Route 218 example now leaves out Tony and Skyler, and its late-visit check now places 18 trainers, up from 15.
- The eight maps are declared in `bulk_events.py`'s DIVERGED.

Route 221's two workers stand at Pal Park's gate whenever the National Dex is missing. While they stand, Ivan's line stops at them, so the scripts helper's gate decides when he, and Jake and Shannon beyond him, can first be met.

The split holds no gauntlet section, as Ian ruled for Route 210 North.

### Rewards

No reward sits on a trainer now mandatory, so none moved. The split's five held-item rewards stay with Tubers Trenton (Eject Button) and Mariel (Red Card), Swimmers Jessica (Mirror Herb) and Adrian (Zoom Lens), and Fisherman Cory (Clear Amulet), all optional. `rewards.py write` regenerated `trainer-roles.tsv`; every changed row is one this branch explains. `rewards.py check` has 0 failures. Trenton's Eject Button and Mariel's Red Card now count in Byron's split, not Wake's, since Route 219 needs Surf; the census placed them in Wake's only while their teams sat at Wake's levels. `rewards.py` gains `RESPLIT` for those two rows, and no reward changes hands. The census also places the Valor Lakefront grunt in Byron's split now, by a row in `splits.py`, since he talks only once Wake is beaten.

## The level climb

Each area is levelled by the stretch it first opens in. Ordinary trainers climb in play order, never at a stretch's cap and rarely one under it. The Ace Trainer mini-bosses keep Mars 1's shape, their aces 2 or 3 under the cap. Thorton's stretch is Barry 5's. In the table, "Old" and "New" are each team's highest level, and "Size" is the old size, then the new one.

| # | Trainer | Area | Stretch | Kind | Old | New | Size |
|---:|---|---|---|---|---:|---:|---|
| 1 | Galactic Grunt | Valor Lakefront | 1, to Cyrus 1 (47) | mandatory (story) | 41 | 43 | 1 to 4 |
| 2 | Ninja Boy Brennan | Route 210 South | 1, to Cyrus 1 (47) | optional | 41 | 43 | 1 to 3 |
| 3 | Ninja Boy Bruce | Route 210 South | 1, to Cyrus 1 (47) | optional | 41 | 43 | 1 to 3 |
| 4 | Ninja Boy Fabian | Route 210 South | 1, to Cyrus 1 (47) | mandatory (moved) | 41 | 43 | 1 to 4 |
| 5 | Bird Keeper Brianna | Route 210 North | 1, to Cyrus 1 (47) | mandatory (moved) | 42 | 44 | 2 to 4 |
| 6 | Ace Trainer Alyssa | Route 210 North | 1, to Cyrus 1 (47) | mandatory, mini-boss | 52 | 44 | 6 to 5 |
| 7 | Ninja Boy Joel | Route 210 North | 1, to Cyrus 1 (47) | optional | 39 | 43 | 2 to 3 |
| 8 | Double Team Zac and Jen | Route 210 North | 1, to Cyrus 1 (47) | mandatory (fixed) | 42 | 44 | 2 to 5 |
| 9 | Ace Trainer Ernest | Route 210 North | 1, to Cyrus 1 (47) | mandatory, mini-boss (fixed) | 52 | 45 | 6 to 6 |
| 10 | Ninja Boy Nathan | Route 210 North | 1, to Cyrus 1 (47) | optional | 42 | 44 | 1 to 3 |
| 11 | Black Belt Adam | Route 210 North | 1, to Cyrus 1 (47) | mandatory (moved) | 42 | 44 | 1 to 4 |
| 12 | Ninja Boy Davido | Route 210 North | 1, to Cyrus 1 (47) | optional | 41 | 44 | 1 to 3 |
| 13 | Veteran Brian | Route 210 North | 1, to Cyrus 1 (47) | mandatory (fixed) | 43 | 45 | 3 to 4 |
| 14 | Bird Keeper Katherine | Route 211 East | 1, to Cyrus 1 (47) | optional | 34 | 45 | 1 to 3 |
| 15 | Ninja Boy Nick | Route 211 East | 1, to Cyrus 1 (47) | optional | 32 | 44 | 2 to 3 |
| 16 | Black Belt Sean | Route 211 East | 1, to Cyrus 1 (47) | optional | 31 | 45 | 3 to 4 |
| 17 | Ruin Maniac Harry | Route 211 East | 1, to Cyrus 1 (47) | optional | 32 | 45 | 3 to 4 |
| 18 | Worker Dillan | Fuego Ironworks | 2, to Barry 5 (50) | optional | 46 | 46 | 1 to 3 |
| 19 | Worker Holden | Fuego Ironworks | 2, to Barry 5 (50) | optional | 44 | 46 | 2 to 4 |
| 20 | Worker Conrad | Fuego Ironworks | 2, to Barry 5 (50) | optional | 46 | 46 | 1 to 4 |
| 21 | Fisherman Cody | Route 208 (water) | 2, to Barry 5 (50) | optional | 44 | 46 | 2 to 3 |
| 22 | Veteran Grant | Oreburgh Gate B1F (water) | 2, to Barry 5 (50) | optional | 45 | 47 | 3 to 5 |
| 23 | Swimmer Sheltin | Route 213 (water) | 2, to Barry 5 (50) | optional | 43 | 46 | 3 to 4 |
| 24 | Swimmer Evan | Route 213 (water) | 2, to Barry 5 (50) | optional | 44 | 46 | 2 to 3 |
| 25 | Swimmer Mary | Route 213 (water) | 2, to Barry 5 (50) | optional | 44 | 46 | 2 to 4 |
| 26 | Swimmer Haley | Route 213 (water) | 2, to Barry 5 (50) | optional | 43 | 46 | 2 to 3 |
| 27 | Sailor Paul | Route 213 (water) | 2, to Barry 5 (50) | optional | 44 | 47 | 3 to 4 |
| 28 | Tuber Trenton | Route 219 | 2, to Barry 5 (50) | optional (Eject Button reward) | 43 | 46 | 2 to 3 |
| 29 | Tuber Mariel | Route 219 | 2, to Barry 5 (50) | optional (Red Card reward) | 43 | 46 | 2 to 3 |
| 30 | Swimmer Vincent | Route 219 (moved from Route 220) | 2, to Barry 5 (50) | mandatory (moved) | 44 | 47 | 2 to 3 |
| 31 | Swimmer Erik | Route 220 | 2, to Barry 5 (50) | optional | 45 | 47 | 1 to 3 |
| 32 | Swimmer Jessica | Route 220 | 2, to Barry 5 (50) | optional (Mirror Herb reward) | 44 | 47 | 2 to 3 |
| 33 | Swimmer Erica | Route 220 | 2, to Barry 5 (50) | optional | 45 | 47 | 1 to 3 |
| 34 | Swimmer Adrian | Route 220 | 2, to Barry 5 (50) | optional (Zoom Lens reward) | 44 | 47 | 2 to 3 |
| 35 | Swimmer Katelyn | Route 220 | 2, to Barry 5 (50) | optional | 43 | 47 | 3 to 3 |
| 36 | Swimmer Claire | Route 220 | 2, to Barry 5 (50) | optional | 45 | 47 | 1 to 3 |
| 37 | Swimmer Dillon | Route 221 | 2, to Barry 5 (50) | mandatory (moved) | 46 | 47 | 1 to 4 |
| 38 | Swimmer Vanessa | Route 221 | 2, to Barry 5 (50) | optional | 46 | 47 | 1 to 3 |
| 39 | Fisherman Cory | Route 221 | 2, to Barry 5 (50) | optional (Clear Amulet reward) | 44 | 47 | 3 to 3 |
| 40 | Collector Ivan | Route 221 | 2, to Barry 5 (50) | mandatory (moved) | 47 | 47 | 1 to 5 |
| 41 | Ace Trainer Jake | Route 221 | 2, to Barry 5 (50) | mandatory, mini-boss pair with Shannon (moved) | 52 | 48 | 6 to 3 |
| 42 | Ace Trainer Shannon | Route 221 | 2, to Barry 5 (50) | mandatory, mini-boss pair with Jake (moved) | 52 | 47 | 6 to 3 |
| 43 | Fisherman Miguel | Route 218 | 2, to Barry 5 (50) | optional | 44 | 47 | 2 to 3 |
| 44 | Fisherman Luc | Route 218 | 2, to Barry 5 (50) | optional | 45 | 48 | 1 to 4 |
| 45 | Guitarist Tony | Route 218 | 2, to Barry 5 (50) | mandatory (moved) | 44 | 48 | 2 to 4 |
| 46 | Sailor Skyler | Route 218 | 2, to Barry 5 (50) | mandatory (moved) | 44 | 48 | 2 to 4 |
| 47 | Picnicker Summer | Iron Island B1F | 3, to Byron (53) | mandatory (fixed) | 46 | 50 | 1 to 4 |
| 48 | Camper Lawrence | Iron Island B1F, left room | 3, to Byron (53) | optional | 46 | 50 | 2 to 3 |
| 49 | Worker Noel | Iron Island B2F, right room | 3, to Byron (53) | optional | 46 | 50 | 2 to 3 |
| 50 | Worker Braden | Iron Island B2F, right room | 3, to Byron (53) | optional | 48 | 50 | 1 to 3 |
| 51 | Hiker Damon | Iron Island B2F | 3, to Byron (53) | optional, pair with Maurice beside Riley | 46 | 50 | 3 to 3 |
| 52 | Hiker Maurice | Iron Island B2F | 3, to Byron (53) | optional, pair with Damon beside Riley | 35 | 50 | 2 to 3 |
| 53 | Black Belt Kendal | Iron Island B2F | 3, to Byron (53) | mandatory, pair with Tyler beside Riley (moved) | 48 | 50 | 1 to 3 |
| 54 | Battle Girl Tyler | Iron Island B2F | 3, to Byron (53) | mandatory, pair with Kendal beside Riley (moved) | 48 | 50 | 1 to 3 |
| 55 | Worker Brendon | Iron Island B2F | 3, to Byron (53) | mandatory, pair with Quentin beside Riley (moved) | 48 | 50 | 2 to 3 |
| 56 | Worker Quentin | Iron Island B2F | 3, to Byron (53) | mandatory, pair with Brendon beside Riley (moved) | 48 | 50 | 2 to 3 |
| 57 | Ace Trainer Jonah | Iron Island B2F | 3, to Byron (53) | mandatory, mini-boss pair with Brenda beside Riley | 51 | 51 | 4 to 4 |
| 58 | Ace Trainer Brenda | Iron Island B2F | 3, to Byron (53) | mandatory, mini-boss pair with Jonah beside Riley | 51 | 50 | 4 to 4 |
| 59 | Ace Trainer Cesar | Canalave Gym | 3, to Byron (53) | gym | 52 | 50 | 6 to 5 |
| 60 | Worker Gary | Canalave Gym | 3, to Byron (53) | gym | 51 | 50 | 1 to 3 |
| 61 | Black Belt Ricky | Canalave Gym | 3, to Byron (53) | gym | 51 | 50 | 1 to 3 |
| 62 | Ace Trainer Breanna | Canalave Gym | 3, to Byron (53) | gym | 52 | 51 | 6 to 4 |
| 63 | Worker Gerardo | Canalave Gym | 3, to Byron (53) | gym | 49 | 51 | 2 to 3 |
| 64 | Black Belt David | Canalave Gym | 3, to Byron (53) | gym | 51 | 51 | 1 to 4 |
| 65 | Worker Jackson | Canalave Gym | 3, to Byron (53) | gym, the last guard | 49 | 52 | 2 to 5 |

Zac and Jen are one trainer's double of five. Jake and Shannon, fought alone together, field three and three. Iron Island's four pairs, fought beside Riley, field three and three, or four and four for Jonah and Brenda.

Not climbed, and why:

- Bosses: Cyrus 1, Barry 5 and Byron.
- Frontier Brains: Thorton and Argenta, from Ian's sixes.
- Named Galactic fights: Argo 1 and every commander and officer file.
- Riley: his door battle and his partner fight with the two grunts beside him.
- Behind Rock Climb: Dragon Tamer Patrick on Route 210 North and Hiker Alexander on Route 208, which belong to a later split.
- The Pal Park double: the scripts helper's.
- Ace Trainer Jake's and Shannon's mini-boss pair is levelled as stretch 2's, its aces 48 and 47 under Barry 5's 50.

### The teams

Each line gives the team in send-out order and its one idea.

| Trainer | Team | The idea |
|---|---|---|
| Galactic Grunt | Skuntank 42, Purugly 42, Salazzle 42, Toxicroak 43 | Galactic poison: Toxic Spikes and Corrosion, then a Dry Skin Toxicroak. |
| Ninja Boy Brennan | Galvantula 42, Drapion 42, Kleavor 43 | Webs in the fog: Sticky Web, then Compound Eyes Thunder and a Kleavor. |
| Ninja Boy Bruce | Beedrill 42, Crobat 42, Venomoth 43 | Poison wings: a Swords Dance hornet, Infiltrator Crobat, Tinted Lens sleep. |
| Ninja Boy Fabian | Ninjask 42, Liepard 42, Shiftry 42, Greninja 43 | Shinobi speed: a Speed Boost Swords Dance Ninjask, Prankster paralysis, Protean shuriken. |
| Bird Keeper Brianna | Skarmory 43, Noctowl 43, Toucannon 43, Pidgeot 44 | Skill Link and steel wings: Toucannon, a Spikes Skarmory, Tailwind. |
| Ace Trainer Alyssa | Ambipom 41, Girafarig 41, Kangaskhan 42, Ursaring 43, Torterra 44 | Normal power at the bridge foot: Fake Out, Scrappy, Guts, and a Torterra ace. |
| Ninja Boy Joel | Butterfree 42, Leavanny 42, Drapion 43 | A cut-tree ambush: sleep and Sticky Web, then a Swords Dance Drapion. |
| Double Team Zac and Jen | Pelipper 43, Raichu 43, Lanturn 43, Ludicolo 43, Gyarados 44 | Rain and lightning: Drizzle, then Thunder that cannot miss in rain. |
| Ace Trainer Ernest | Probopass 42, Ampharos 42, Scizor 42, Pawmot 43, Lucario 44, Magnezone 45 | Steel and current on the bridge: Stealth Rock, Technician Scizor, an Analytic Magnezone ace. |
| Ninja Boy Nathan | Dustox 43, Vikavolt 43, Frosmoth 44 | Frost and current in the grass: a Frosmoth behind Vikavolt. |
| Black Belt Adam | Hariyama 43, Primeape 43, Grapploct 43, Mienshao 44 | Fists: Guts, Defiant, a Bulk Up Grapploct, Regenerator Mienshao. |
| Ninja Boy Davido | Mothim 43, Crustle 43, Hawlucha 44 | Rock disguise by the bridge: Hawlucha's Unburden and a Mothim. |
| Veteran Brian | Tangrowth 44, Cofagrigus 44, Magcargo 44, Milotic 45 | The old campaigner by Celestic: Trick Room from a Cofagrigus that takes its killer with Destiny Bond, a Regenerator Tangrowth, Marvel Scale. |
| Bird Keeper Katherine | Altaria 44, Noctowl 44, Honchkrow 45 | Night flyers: a burning, healing Altaria, then Moxie Honchkrow. |
| Ninja Boy Nick | Toxicroak 44, Ariados 44, Liepard 44 | Mountain shinobi: Swords Dance Toxicroak, a Sniper spider, Prankster paralysis. |
| Black Belt Sean | Medicham 44, Breloom 44, Hitmontop 44, Machamp 45 | Cave training: Pure Power, Poison Heal, Technician, then No Guard Dynamic Punch. |
| Ruin Maniac Harry | Carbink 44, Bastiodon 44, Aerodactyl 44, Rampardos 45 | Fossil hunter: Shieldon's and Cranidos's lines, a Carbink screen. |
| Worker Dillan | Garganacl 45, Hariyama 45, Machamp 46 | Forge muscle: a Curse Garganacl, Guts, No Guard. |
| Worker Holden | Klefki 45, Magneton 45, Bronzong 45, Aggron 46 | The ironworks' metal: screens from a Prankster Klefki, Analytic, a Rock Head Aggron. |
| Worker Conrad | Torkoal 45, Armarouge 45, Camerupt 45, Magmortar 46 | The furnace: Torkoal's sun for an Armarouge and a Magmortar. |
| Fisherman Cody | Quagsire 45, Whiscash 45, Gyarados 46 | River bottom: Unaware Quagsire, a Curse Whiscash, a Moxie Gyarados. |
| Veteran Grant | Golem 46, Exploud 46, Staraptor 46, Ferrothorn 46, Lucario 47 | The cave veteran: Stealth Rock and Explosion from Golem, Scrappy Exploud, an Adaptability Lucario. |
| Swimmer Sheltin | Mantine 45, Floatzel 45, Starmie 46, Sharpedo 46 | Speed in the open water: Speed Boost Sharpedo, Analytic Starmie, Floatzel. |
| Swimmer Evan | Politoed 45, Ludicolo 46, Kingdra 46 | Rain off the hotel beach: Drizzle, Swift Swim Kingdra and Ludicolo. |
| Swimmer Mary | Alomomola 45, Lumineon 45, Lapras 46, Primarina 46 | Sea song: a Regenerator nurse, Liquid Voice Primarina, a Lapras. |
| Swimmer Haley | Slowbro 45, Golduck 46, Araquanid 46 | Slow and sticky: a Regenerator Slowbro, Water Bubble Araquanid. |
| Sailor Paul | Tentacruel 46, Hariyama 46, Kingler 46, Wailord 47 | A sailor's crew: Toxic Spikes, Sheer Force Crabhammer, a Hariyama, a Wailord. |
| Tuber Trenton | Gastrodon 46, Clodsire 46, Dewgong 46 | Sea slugs and a seal: Spikes from an Unaware Clodsire, Perish Song. |
| Tuber Mariel | Corsola 45, Floatzel 46, Azumarill 46 | Huge Power on the islet: Azumarill behind a Corsola and a Floatzel. |
| Swimmer Vincent | Relicanth 46, Crawdaunt 46, Kabutops 47 | Fossils from the sea floor: Swift Swim Kabutops, Rock Head Relicanth, Adaptability Crawdaunt. |
| Swimmer Erik | Toxapex 46, Jellicent 46, Slowking 47 | Walls in the current: Regenerator Slowking and Toxapex, Cursed Body Jellicent. |
| Swimmer Jessica | Seaking 46, Wailord 46, Milotic 47 | Big fish: Water Spout Wailord, Lightning Rod Seaking, Marvel Scale Milotic. |
| Swimmer Erica | Bibarel 46, Pelipper 46, Empoleon 47 | Sea birds and a beaver: Simple Curse, Competitive Empoleon. |
| Swimmer Adrian | Qwilfish 46, Tentacruel 46, Octillery 47 | Spikes and sniping: Sniper Octillery, Qwilfish, a Tentacruel. |
| Swimmer Katelyn | Ludicolo 46, Medicham 46, Swampert 47 | Dance on the water: a Fake Out Ludicolo, Pure Power, Swampert. |
| Swimmer Claire | Cloyster 46, Starmie 46, Omastar 47 | Shells: White Herb Shell Smash Omastar behind Spikes and a Starmie. |
| Swimmer Dillon | Floatzel 46, Lanturn 46, Toxapex 46, Vaporeon 47 | Waterproof: Volt Absorb, Regenerator Toxapex, and Vaporeon's Wish. |
| Swimmer Vanessa | Corsola 46, Alomomola 46, Araquanid 47 | Reef dwellers: Regenerator walls in front of Water Bubble. |
| Fisherman Cory | Sharpedo 46, Dragonair 46, Kingdra 47 | The dragon catch: Swift Swim Kingdra, a Speed Boost Sharpedo, Dragonair. |
| Collector Ivan | Galarian Weezing 46, Klefki 46, Glimmora 46, Polteageist 46, Togekiss 47 | The collector's oddities: a Galarian Weezing, a Prankster Klefki, Toxic Debris, a Polteageist, Togekiss. |
| Ace Trainer Jake | Absol 46, Honchkrow 47, Gallade 48 | With Shannon at Pal Park's door: the sharp edge in the dark, Super Luck with a Scope Lens and a Razor Claw behind high-critical moves, a Gallade ace. |
| Ace Trainer Shannon | Ninetales 46, Victreebel 46, Arcanine 47 | With Jake: her Drought sun for a Chlorophyll Victreebel, then an Intimidate Arcanine ace. |
| Fisherman Miguel | Lanturn 47, Whiscash 47, Starmie 47 | Rod and line: Volt Absorb, Analytic Starmie, a Hydration Whiscash. |
| Fisherman Luc | Qwilfish 47, Mantine 47, Octillery 47, Dhelmise 48 | Octopus and anchor: Sniper Octillery, Spikes, a Steelworker Dhelmise. |
| Guitarist Tony | Kricketune 47, Chatot 47, Primarina 47, Exploud 48 | The band at the neck: Hyper Voice through Scrappy, a Swords Dance Kricketune, Chatter, and Liquid Voice. |
| Sailor Skyler | Mantine 47, Machamp 47, Crawdaunt 47, Gyarados 48 | The deckhands: a Mantine, No Guard Machamp, Crawdaunt, a Moxie Gyarados. |
| Picnicker Summer | Emolga 49, Togedemaru 49, Pawmot 49, Raichu 50 | A picnic of sparks: Emolga's Encore, a Togedemaru, Iron Fist Pawmot, Raichu. |
| Camper Lawrence | Ambipom 49, Floatzel 49, Cinderace 50 | Campfire sprinters: Technician Ambipom, a Bulk Up Floatzel, a Bulk Up Cinderace. |
| Worker Noel | Klefki 49, Mawile 49, Magnezone 50 | A dead-end workshop: Magnet Pull, Intimidate Mawile, Klefki. |
| Worker Braden | Forretress 49, Ferrothorn 49, Steelix 50 | Spikes and steel: Forretress and Ferrothorn ahead of a Steelix. |
| Hiker Damon | Garganacl 49, Aggron 49, Probopass 50 | With Maurice: a Curse Garganacl, Probopass and Aggron. |
| Hiker Maurice | Glimmora 49, Golem 49, Rhyperior 50 | With Damon: Toxic Debris, Solid Rock, a Golem. |
| Black Belt Kendal | Hariyama 49, Toxicroak 49, Lucario 50 | With Tyler, in the corridor: Fake Out, Dry Skin, Bullet Punch. |
| Battle Girl Tyler | Breloom 49, Medicham 49, Hawlucha 50 | With Kendal: Spore, Pure Power and a Hawlucha. |
| Worker Brendon | Bronzong 49, Granbull 49, Steelix 50 | With Quentin, at the bend: Strong Jaw Granbull, a Steelix, Trick Room Bronzong. |
| Worker Quentin | Ursaring 49, Machamp 49, Mamoswine 50 | With Brendon: Guts Ursaring and Machamp under the Trick Room, then Mamoswine. |
| Ace Trainer Jonah | Hippowdon 48, Quagsire 48, Mamoswine 50, Torterra 51 | With Brenda: sand from Hippowdon, Unaware, Mamoswine, a Torterra ace. |
| Ace Trainer Brenda | Lopunny 48, Hitmontop 48, Medicham 49, Gardevoir 50 | With Jonah: Fake Out, Intimidate, Pure Power, a Gardevoir ace. |
| Ace Trainer Cesar | Skarmory 49, Ferrothorn 49, Mawile 50, Empoleon 50, Scizor 50 | The first guard: Spikes from Skarmory, Iron Barbs, Mawile, Empoleon, a Scizor. |
| Worker Gary | Metang 50, Probopass 50, Magnezone 50 | Magnets on the lift: Analytic Magnezone, Metang, a Sand Force Probopass. |
| Black Belt Ricky | Bastiodon 50, Aggron 50, Steelix 50 | Byron's wall: Bastiodon, Aggron, a Sheer Force Steelix. |
| Ace Trainer Breanna | Bronzong 50, Klefki 50, Corviknight 51, Empoleon 51 | Heavy armour: Trick Room Bronzong, Prankster Klefki, Mirror Armor Corviknight, Empoleon. |
| Worker Gerardo | Forretress 51, Mawile 51, Metagross 51 | Iron trap: Forretress lays Spikes and may Explode, then a Mawile and a Metagross. |
| Black Belt David | Scizor 50, Machamp 51, Lucario 51, Pawmot 51 | Steel fists: Justified Lucario, a Technician Scizor, No Guard Machamp. |
| Worker Jackson | Klefki 51, Corviknight 51, Magnezone 51, Ferrothorn 51, Bastiodon 52 | The last guard: Klefki screens, Magnezone, Corviknight, Iron Barbs, and a Bastiodon to close. |

No rebuilt team carries a one-hit KO move, an evasion move or item, a Choice item, or trapping. Sailor Paul's Guillotine and Tuber Trenton's Sheer Cold are gone. Three trade moves come in, under Ian's rulings of 2026-10-31, each where the team's idea calls for it: Veteran Grant's Golem has Explosion behind a Custap Berry, Veteran Brian's Cofagrigus has Destiny Bond after its Trick Room, and Worker Gerardo's Forretress has Explosion after its Spikes. Each can be played round: the Golem by knocking it out from above 30 percent or leaving it at an HP it rarely explodes at, the Forretress likewise, and Destiny Bond with status or by not striking the last blow while it is up. Counter moves stay too: Bastiodon's Metal Burst for Ruin Maniac Harry, Black Belt Ricky and Worker Jackson, and Magnezone's Mirror Coat for Worker Gary. Five teams set weather through an ability, as trainers may: Zac and Jen's and Swimmer Evan's Drizzle, Worker Conrad's and Ace Trainer Shannon's Drought, and Ace Trainer Jonah's Sand Stream. No team carries a weather move. Three members are Modest, the only textbook natures in the split.

### Speed against the box

These are eight fast answers a box is likely to hold, at each stretch's cap, at IV 15 with neutral natures, beside each team's fastest member at its own IVs and nature. They are reference species, not goal 3's boxes.

| Stretch, cap | Box answers at the cap |
|---|---|
| 1, 47 | Crobat 134, Talonflame 130, Weavile 129, Greninja 126, Mienshao 110, Staraptor 110, Garchomp 107, Lucario 96 |
| 2, 50 | Crobat 142, Talonflame 138, Weavile 137, Greninja 134, Mienshao 117, Staraptor 117, Garchomp 114, Lucario 102 |
| 3, 53 | Crobat 150, Talonflame 146, Weavile 145, Greninja 142, Mienshao 124, Staraptor 124, Garchomp 121, Lucario 108 |

| Stretch | Each team's fastest member, fastest first |
|---|---|
| 1 | Ninjask 167, Aerodactyl 141, Crobat 138, Hawlucha 134, Liepard 128, Ambipom 123, Mienshao 121, Pawmot 118, Galvantula 117, Pidgeot 116, Salazzle 115, Raichu 110, Drapion 99, Honchkrow 97, Milotic 89, Medicham 85, Frosmoth 73 |
| 2 | Starmie 138, Floatzel 136, Floatzel 136, Floatzel 134, Starmie 124, Staraptor 123, Chatot 121, Sharpedo 115, Ninetales 111, Tentacruel 110, Tentacruel 110, Lumineon 107, Golduck 106, Absol 106, Magmortar 104, Kabutops 102, Medicham 100, Politoed 99, Glimmora 97, Gyarados 96, Milotic 95, Qwilfish 88, Klefki 85, Bibarel 84, Gyarados 81, Jellicent 74, Dewgong 72, Alomomola 70, Machamp 68 |
| 3 | Ambipom 144, Hawlucha 138, Pawmot 136, Pawmot 134, Lopunny 132, Lucario 110, Mamoswine 100, Klefki 95, Klefki 95, Klefki 93, Metagross 90, Mamoswine 90, Glimmora 90, Skarmory 88, Magnezone 79, Aggron 63, Aggron 58, Granbull 56, Forretress 52 |

In stretch 1, Fabian's Ninjask, Harry's Aerodactyl and Bruce's Crobat outspeed every answer. In stretches 2 and 3 none does: stretch 2's fastest, Miguel's Starmie at 138, and stretch 3's, Lawrence's Ambipom at 144, sit under Crobat and Talonflame. Most teams sit under the box's fast answers.

## The AI flags

Ian asked on 2026-10-31 for every team's AI flags to be set on purpose (`battle-ai/flags-guide.md` is the guide). Every rebuilt team runs Basic, Evaluate Attack and Expert. Five lacked some of those and now have them: Bird Keeper Katherine and Ninja Boy Nick ran Basic alone, Black Belt Sean and Hiker Maurice Basic and Prioritize Extremes, and Fisherman Cody had no Evaluate Attack. Prioritize Extremes, which pushes every status move and Explosion alike, comes off the nine teams that carried it from the base ROM. Weather comes off Swimmers Vincent and Katelyn and Ace Trainer Shannon, since none carries a weather move, so the flag did nothing.

Each team adds one of the four flags only where the guide's rule fits its idea:

| Flag | Rule | Teams |
|---|---|---|
| Check HP | a trade move (Explosion, Self-Destruct, Destiny Bond) | Grant, Gerardo, Brian |
| Risky | critical hits are the idea | Jake, Nick |
| Harassment | status or hazards are the idea, with at least two of its table's status moves | Brennan, Joel, Ivan, Erik, Braden |
| Weather | a lead with a weather move to open with | none |

Every team that carries a move one of the four flags acts on, and why it has the flags it has:

| Trainer | The moves the four flags act on | Flags beyond the base | Why |
|---|---|---|---|
| Ninja Boy Brennan | high-critical: X-Scissor; status: Sticky Web, Toxic Spikes | Harassment | Harassment, since the webs in the fog are Sticky Web and Toxic Spikes. |
| Ninja Boy Bruce | high-critical: X-Scissor | base only | Its high-critical moves are coverage, not the idea, so no Risky. |
| Ninja Boy Fabian | high-critical: Night Slash, X-Scissor | base only | Its high-critical moves are coverage, not the idea, so no Risky. |
| Bird Keeper Brianna | status: Hypnosis, Spikes | base only | Its status moves support an attacking idea, so no Harassment. |
| Ace Trainer Alyssa | high-critical: Stone Edge | base only | Its high-critical moves are coverage, not the idea, so no Risky. |
| Ninja Boy Joel | high-critical: Leaf Blade, Night Slash, X-Scissor; status: Sleep Powder, Sticky Web | Harassment | Harassment, since the ambush is sleep and Sticky Web. |
| Ace Trainer Ernest | status: Thunder Wave | base only | Its status moves support an attacking idea, so no Harassment. |
| Black Belt Adam | high-critical: Stone Edge | base only | Its high-critical moves are coverage, not the idea, so no Risky. |
| Ninja Boy Davido | high-critical: X-Scissor | base only | Its high-critical moves are coverage, not the idea, so no Risky. |
| Veteran Brian | trade: Destiny Bond; status: Sleep Powder, Will-O-Wisp | Check HP | Check HP, by the guide's rule for a trade move. For Destiny Bond it changes little, since Expert already holds the bond back while Cofagrigus is above 70 percent, but it keeps Milotic's Recover for when it is hurt. Its sleep and burn serve the Trick Room, so no Harassment. |
| Bird Keeper Katherine | high-critical: Dragon Claw, Drill Peck, Night Slash | base only | Its high-critical moves are coverage, not the idea, so no Risky. |
| Ninja Boy Nick | high-critical: X-Scissor; status: Thunder Wave, Toxic Spikes | Risky | Risky, since the idea is a Sniper Ariados with a Scope Lens on X-Scissor; it also makes the team's Sucker Punches a gamble. |
| Black Belt Sean | high-critical: Stone Edge | base only | Its high-critical moves are coverage, not the idea, so no Risky. |
| Ruin Maniac Harry | counter: Metal Burst; high-critical: Stone Edge | base only | Its high-critical moves are coverage, not the idea, so no Risky; its counter move is left to Expert's own timing, since Risky would push it on half its turns. |
| Worker Dillan | high-critical: Stone Edge | base only | Its high-critical moves are coverage, not the idea, so no Risky. |
| Worker Holden | high-critical: Stone Edge; status: Thunder Wave | base only | Its high-critical moves are coverage, not the idea, so no Risky; its status moves support an attacking idea, so no Harassment. |
| Worker Conrad | high-critical: Stone Edge; status: Will-O-Wisp, Yawn | base only | Its high-critical moves are coverage, not the idea, so no Risky; its status moves support an attacking idea, so no Harassment. |
| Fisherman Cody | high-critical: Stone Edge | base only | Its high-critical moves are coverage, not the idea, so no Risky. |
| Veteran Grant | trade: Explosion; high-critical: Stone Edge | Check HP | Check HP holds Golem's Explosion until it is at 30 percent or less, the Custap Berry's range, so the player can knock it out from higher up. |
| Sailor Paul | high-critical: Crabhammer, X-Scissor | base only | Its high-critical moves are coverage, not the idea, so no Risky. |
| Tuber Trenton | status: Encore, Spikes | base only | Its status moves support an attacking idea, so no Harassment. |
| Swimmer Vincent | high-critical: Crabhammer, Stone Edge | base only | Its high-critical moves are coverage, not the idea, so no Risky. |
| Swimmer Erik | status: Toxic Spikes, Will-O-Wisp | Harassment | Harassment, since the walls win by Toxic Spikes and burns. |
| Swimmer Adrian | status: Spikes, Toxic Spikes | base only | Its status moves support an attacking idea, so no Harassment. |
| Swimmer Claire | status: Spikes, Thunder Wave | base only | Its status moves support an attacking idea, so no Harassment. |
| Swimmer Vanessa | high-critical: X-Scissor | base only | Its high-critical moves are coverage, not the idea, so no Risky. |
| Collector Ivan | status: Defog, Thunder Wave, Will-O-Wisp | Harassment | Harassment, since status carries the collector's oddities (burns, paralysis, Defog over the player's hazards). |
| Ace Trainer Jake | high-critical: Drill Peck, Leaf Blade, Night Slash, Psycho Cut, Shadow Claw, Stone Edge, X-Scissor | Risky | Risky, since the team's idea is critical hits: Super Luck, a Scope Lens and a Razor Claw behind high-critical moves, which it then reaches for even when another move hits harder. |
| Ace Trainer Shannon | high-critical: Leaf Blade | base only | Its high-critical moves are coverage, not the idea, so no Risky. |
| Fisherman Miguel | high-critical: Stone Edge | base only | Its high-critical moves are coverage, not the idea, so no Risky. |
| Guitarist Tony | high-critical: X-Scissor | base only | Its high-critical moves are coverage, not the idea, so no Risky. |
| Sailor Skyler | high-critical: Crabhammer, Stone Edge | base only | Its high-critical moves are coverage, not the idea, so no Risky. |
| Worker Noel | status: Spikes, Thunder Wave | base only | Its status moves support an attacking idea, so no Harassment. |
| Worker Braden | status: Spikes, Thunder Wave, Toxic Spikes | Harassment | Harassment, since the team's idea is hazards and paralysis ahead of a Steelix. |
| Hiker Damon | high-critical: Stone Edge | base only | Its high-critical moves are coverage, not the idea, so no Risky. |
| Hiker Maurice | high-critical: Stone Edge | base only | Its high-critical moves are coverage, not the idea, so no Risky. |
| Worker Brendon | high-critical: Stone Edge | base only | Its high-critical moves are coverage, not the idea, so no Risky. |
| Worker Quentin | high-critical: Stone Edge | base only | Its high-critical moves are coverage, not the idea, so no Risky. |
| Ace Trainer Jonah | high-critical: Stone Edge | base only | Its high-critical moves are coverage, not the idea, so no Risky. |
| Ace Trainer Cesar | status: Spikes, Thunder Wave | base only | Its status moves support an attacking idea, so no Harassment. |
| Worker Gary | counter: Mirror Coat; status: Thunder Wave | base only | Its status moves support an attacking idea, so no Harassment; its counter move is left to Expert's own timing, since Risky would push it on half its turns. |
| Black Belt Ricky | counter: Metal Burst; high-critical: Stone Edge | base only | Its high-critical moves are coverage, not the idea, so no Risky; its counter move is left to Expert's own timing, since Risky would push it on half its turns. |
| Ace Trainer Breanna | status: Spikes, Thunder Wave | base only | Its status moves support an attacking idea, so no Harassment. |
| Worker Gerardo | trade: Explosion | Check HP | Check HP holds Forretress's Explosion until it is low and away from a target already nearly down, after its Spikes are laid. |
| Black Belt David | high-critical: Stone Edge | base only | Its high-critical moves are coverage, not the idea, so no Risky. |
| Worker Jackson | counter: Metal Burst; high-critical: Stone Edge | base only | Its high-critical moves are coverage, not the idea, so no Risky; its counter move is left to Expert's own timing, since Risky would push it on half its turns. |

## How the numbers were made

The split's trainers came from the map of the split (`byron-split-map.md`) and its table of every trainer on the split's maps, read against each map's events. Play order follows order A's maps, then each trainer's tile, and in the gym the distance from the door. The mandatory verdicts are `tools.oxide.balance.required`'s field model on the edited events, run with and without Surf. Chokepoints were found by testing every free tile with each look and sight, and the pairs' places by testing every straight line of tiles the path must cross that has a free tile at each end.

The teams were written as data and checked before saving by the Kaizo study's legality reader (`out/tools/oxide.py`), pointed at this branch's `res/` and at the export from before the TM pass. A move is legal when the species or an earlier stage learns it by level at or below its level, when it is on the line's egg list, or when it is a TM or tutor move of the line, now or before the TM pass. Every team was saved through `tools.oxide.encounters.trainers.save`, which runs the trainer lint and the real packer and records the file in `trainers_diverged.json`. A second pass reread every saved file. The comb's drafts were read for ideas only.

| Check | Result |
|---|---|
| Trainer lint, all 65 changed teams | no findings |
| The real packer, through `trainers.save` | every team packed |
| Moves legal at their level | all legal |
| Item or nature repeated in a team, nature unnamed | none |
| One-hit KO, trapping, evasion, Choice item | none; three trade moves on purpose |
| AI flags, every team against the guide's table | all match |
| `test_trainers` | 44 of 44 |
| `test_b1e` | 11 of 11 |
| `test_b1` | 48 of 48 |
| `place_rewards.py check` on the built ROM | 168 rows, each found once |
| `rewards.py check` | 0 failures |
| `make rom`, then `integrate.sh --verify-only` | 53 checks pass; sync-docs fails off oxide by design; one warning, the tracker over 9,000 words, from before this branch |

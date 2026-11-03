# HQ's split: the map before any change

The Overseer asked on 2026-11-02 for HQ's split to be mapped as Byron's and Candice's were, so that its pass can be planned with Ian. The split runs from Candice's badge (cap 56) to the close of Galactic HQ (cap 60), ending on Cyrus 2 and Saturn 2; the Battle Zone opens straight after, in the Galactic split (cap 65). This page was read on the branch `overseer-hq-map` from `origin/oxide` at 9447ef458e1. No game data changed.

## Summary

Something is broken today, and it comes first. Gauntlet section 6 can shut the player in for good. It opens on arrival at the HQ's 3F by the west stairs, and while the player holds the Galactic Key it refuses those stairs, the only way off that part of 3F. It stays open until all four 3F grunts are beaten, and two of them stand on 3F's east side, which cannot be reached from the west. The Pocket PC, the Escape Rope, Dig, Fly and Teleport all refuse inside a section. So a player who fetches the key and then goes back up to 3F west (for the locked room there, or for its two grunts) before beating the east grunts cannot leave, short of losing a battle. The in-game checklist's test-kit gauntlet checks (section 2) tell Ian to do exactly that: "Then fetch the key and come back: the same stairs refuse." That check must not be run on a real save. The bug is Oxide's own, not vanilla's. The cause is a wrong walk of the HQ, described below. On Ian's word of 2026-11-02, section 6 was moved to 3F's east stairs on the branch `overseer-hq-gauntlet6`: it opens and refuses only there, holds grunts 3 and 4, and a new check in `test_b1e` walks every section for a place the player could not leave. The checklist step is rewritten there with a check of the trap. Question 4 still asks about the HQ's other sections.

What was mapped. The HQ's ten maps were walked tile by tile with `mapreach.py`, its locked doors shut and then open, and every crossing on the way to Saturn was tested with `required.py`'s sight lines; `pairs.py` gave the doubles. Everything outside the HQ was walked with the story-route study's whole-world tile model, comparing the end of Candice's split with the Icicle Badge (Rock Climb). The story's order was read from the scripts. Experience was summed with Generation 4's formula.

What could not be checked. Nothing was seen in game. The HQ's warp panels were read as warps, and the model reads the floors flat. The experience sums assume six Pokemon share every fight, with no Exp. Share or Lucky Egg. The post-pass experience is an estimate from assumed team sizes. The gauntlet code was read, not run.

What was found. The HQ is two halves. The basement run goes from the warehouse through B2F, B1F, 1F and 2F's west side, then down through Scientist Fredrick's room to B2F's north end, where the Galactic Key lies; it is a loop, and its way on is back out through the warehouse. With the key, the player walks to the HQ's front door in Veilstone and unlocks the lobby's inner door. That opens the tower: 2F's east side, the hall and Cyrus's speech, 2F's north-east nap room, 3F's east side, then 4F with Cyrus 2, the laboratory and Saturn 2 in the control room. The gauntlet doc read the HQ as one climb, B2F to 3F, with 3F's locked door leading on to 4F; in fact that door opens only a dead-end room. So today's sections 4 and 5 hold one mandatory trainer and none, the tower lies outside every section, and section 6 is the trap above.

The split holds 5 mandatory fights, all in the HQ, against Ian's 10 to 15. Rock Climb opens six optional trainers outside it: Route 216's four, which Candice's pass levelled for 60, and Hiker Alexander (Route 208) and Dragon Tamer Patrick (Route 210 North), still tagged Byron's and at 45 and 43. No officer, rival or mini-boss is fought in the split. Jupiter's scene at Lake Acuity has no battle.

The levels have room and the experience does not. The ordinary band is wide, 55 to 59. But every fight in the split together gives 108,700 experience, against 242,300 for six Pokemon to climb from 56 to 60, so today a party of six meets Cyrus 2's level-60 ace at 56 or 57. The pass's team sizes (three to six Pokemon where the HQ's grunts have two) and the added fights should bring it to roughly 215,000.

| Stretch | Areas, in play order | Closed by | Ordinary band | Experience today |
|---|---|---|---|---|
| 1 | Acuity Lakefront's climb, Lake Acuity's scene; Rock Climb's finds on Routes 208, 210 North and 216 and Mt. Coronet 2F | Jupiter's scene | 55 to 57 | 34,000, all optional |
| 2 | Veilstone's storage-key grunt and Looker, the warehouse | entering B2F | none | none |
| 3 | the basement run: B2F, B1F, 1F, 2F west (3F west a detour), Fredrick's room, B2F north, the key, out | leaving with the key | 56 to 57 | 10,000 mandatory, 16,000 optional |
| 4 | the tower: the lobby's door, 2F east, the hall, the nap room, 3F east, 4F, the laboratory, the control room | Cyrus 2 (60), then Saturn 2 (57) | 57 to 58, rarely 59 | 17,000 mandatory, 2,000 optional, 29,000 from the bosses |

| Mandatory fights, counted Ian's way (a pair once, gym trainers apart, mini-bosses included) | Count |
|---|---:|
| Today | 5 |
| Moving Fredrick, Darrius and 2F's first grunt to necks | up to 8 |
| Making talking Galactic members trainers (B1F's grunt, B2F north's grunt, Veilstone's storage-key grunt, a lab scientist) | up to 12 |
| Adding new trainers (Acuity Lakefront's climb, the lobby's key door, 4F's door corridor, a second lab scientist) | up to 16 |

Today's five are B2F's Grunts 1 and 2, the 1F grunt, 2F's pair of grunts 2 and 3, and 3F's pair of grunts 3 and 4.

Action items for Ian: answer the ten questions below; and do not run the HQ step of the checklist's gauntlet checks until it is rewritten.

| Step | Who | Time |
|---|---|---|
| Close section 6's trap and rewrite the checklist's HQ step (done on `overseer-hq-gauntlet6`, Ian's choice of 2026-11-02) | a helper | 1 hour |
| Answer the questions below | Ian | 20 to 30 minutes |
| The gauntlet rebuild of question 4, walked again with `mapreach.py`, and the nap-room bed's refusal | a worker | 2 to 3 hours |
| The count's moves and new trainers, each checked with `required.Field`, the Capsule's ball, Alexander's and Patrick's tags | a worker | 2 to 3 hours |
| The level climb and rebuild of the split's ordinary teams in play order (12 in the HQ, Alexander and Patrick, and the new ones) | a worker | half a day |
| Cyrus 2 and Saturn 2 in checked stages, to Ian's themes | the Overseer and a worker | 1 to 2 hours each, plus Ian's look |
| The in-game check of the sections, the moved trainers and the Capsule | Ian | 45 minutes with the test kit |

## Ian's decisions

1. Push every cap from Candice's on back by two (Candice 58, HQ 62, Galactic 67, Volkner 70, Barry 73, the League 80), or keep 56, 60, 65, 68, 71 and 78? Recommended: keep them. HQ's split is short of experience, not of room in its levels, so a push would leave HQ just as short and make Candice's split a little short too, and it would re-level every landed team from Candice's on (section 2 has the sums and everything the push would move).
2. An honour cap inside the split: none (recommended, since no player's experience can reach one), or 58 when the player leaves the basement with the Galactic Key?
3. The count: the recommended 11 (today's 5; B1F's talking grunt made a trainer; Fredrick and Darrius moved to necks; Veilstone's storage-key grunt fought before he drops the key; a new trainer at the foot of Acuity Lakefront's climb; one lab scientist made a trainer), or the moves alone for 7 or 8, or more of section 3's list, up to 16?
4. The HQ's gauntlets (section 6 already moved to 3F's east stairs on Ian's word, 2026-11-02): two sections drawn on the real walk, the basement run (its way back to the warehouse refused until the key is held) and the tower (its stairs back to the lobby refused, closing on arrival at 4F, the nap-room bed refusing while it is open) (recommended); or only section 6 moved to 3F's east stairs, sections 3 to 5 kept; or sections 4 to 6 dropped?
5. The Ability Capsule the Scheduled list asks for: a new ball in 3F west's locked room, past both of 3F west's optional grunts and the Galactic Key's door (recommended, once the trap is closed); or Darrius's win reward; or Fredrick's?
6. The bosses' levels: Cyrus 2's ace at the cap of 60 and Saturn 2's at 57, three under it as Ian set on 2026-10-07 (recommended); or Saturn 2 at 58, the Level Caps sheet's figure, or at 60? No named officer is in the split, and none is recommended. Jupiter is in the split only as Lake Acuity's scene: keep it with no battle (recommended), or give her a fight there?
7. Hiker Alexander and Dragon Tamer Patrick stand behind Rock Climb, so they are first met in HQ's split: tag them HQ's and level them for 60, at 56 to 57, as Route 216's four were (recommended), or leave them as Byron's at 45 and 43?
8. Mt. Coronet 2F's Rock Climb rooms, with their wild table (36 to 39) and four balls, open with the Icicle Badge: may the OxiDex move 2F's table from the Galactic split to HQ's?
9. Saturn 2 fields Uxie while the control room shows all three lake guardians sealed in its machines: keep it, as Candice's answer kept Azelf and Mesprit (recommended), or drop it in his redesign?
10. Cyrus's theme asks for 18 different Pokemon over his three fights. Today Dusknoir is on Cyrus 2 and Cyrus 3, and Salamence on Cyrus 1 and Cyrus 3. Which fight keeps each? Recommended: Cyrus 2 keeps Dusknoir and Cyrus 3 drops both, since Cyrus 1 has landed and Cyrus 3 is redesigned later anyway.

## 1. The areas, and what opens each

The split opens in four steps. Candice's badge allows Rock Climb, whose HM the player found on Route 217. Mars's win at Lake Verity already set `VAR_LAKE_ACUITY_STATE` to 1 (`scripts_lake_verity.s`), so the scene at Lake Acuity plays the moment the player arrives (`scripts_init_lake_acuity.s`, an on-frame script). It clears `FLAG_HIDE_VEILSTONE_CITY_GRUNT_M_STORAGE_KEY`, which puts a grunt by the Galactic building in Veilstone. Talking to him makes Looker appear with the Storage Key; agreeing to enter the hideout sets the warehouse's state to 3, and Looker opens the HQ's door inside the warehouse. Inside, the Galactic Key opens four doors. Saturn's win and the button in the control room set `FLAG_FREED_GALACTIC_HQ_POKEMON`, which sails the Battle Zone's ferry and clears Mt. Coronet 2F's cave painting.

### The Icicle Badge (Rock Climb)

| Area | What Rock Climb opens | Trainers (top levels) | Items | Capture area |
|---|---|---|---|---|
| Acuity Lakefront | the climb to Lake Acuity | none | Reaper Cloth | Acuity Lakefront, Candice's |
| Lake Acuity | the whole lake; Jupiter's scene with Barry, no battle | none | TM42 Facade, two | Lake Acuity, HQ's since Candice's answer 8: land 38 to 41, Surf 34 to 46 |
| Route 216, above its walls | the high ground | Skiers Bradley (three, 56), Kaitlyn (three, 57) and Andrea (three, 57), Black Belt Philip (four, 57) | Sitrus Berry, Mental Herb, HP Up, Max Potion | Route 216, Candice's |
| Route 208 | ground behind a Rock Climb wall | Hiker Alexander (Golem and Probopass, 45) | none | Route 208, Fantina's |
| Route 210 North | ground behind a Rock Climb wall | Dragon Tamer Patrick (Altaria, 43) | Zinc | Route 210 North, Byron's |
| Mt. Coronet 2F | the rooms up from 1F South, as far as the cave painting | none | Max Revive, Max Repel, TM75 Meteor Beam, TM58 Triple Axel | Mt. Coronet 2F, tagged Galactic's: land 36 to 39 |
| Elsewhere | single balls behind Rock Climb walls | none | Route 207's Iron and Timer Ball, Route 211 East's Sitrus Berry, Route 213's Protein and Lum Berry, Valor Lakefront's Iron and Lum Berry | |

Veilstone's Full Incense, beside the warehouse, comes into reach as the warehouse guards leave after Candice's gym, not by Rock Climb.

The model also reaches Sendoff Spring with Rock Climb, but the game walls Spring Path off until the Distortion World (`story-route.md`, the recheck of 2026-10-31), so that reach is not real. Uxie stays hidden in Acuity Cavern.

### Veilstone and the warehouse

Nothing here is a battle today. The storage-key grunt at (721,593) only talks ("I don't know anything about any Storage Key!"), and Looker asks whether the player will enter the hideout. The warehouse's Dusk Stone lies past the HQ's door, so it is first reached here, as the stone census counts it; the Sitrus Berry where HM02 lay is reachable from Wake's split, though the reward table counts it in HQ's. Veilstone's maid trains to 38 and is Wake's.

### The HQ

The walk, read with the four key doors shut and then open:

| Part | Maps and pockets | Trainers (top levels) | On the way? | Items |
|---|---|---|---|---|
| Basement | B2F from the warehouse to the stairs at (81,3) | Grunts 1 (Weezing, Arbok, 54) and 2 (Cacturne, Seviper, 54) | yes, both required | Zinc |
| Basement | B1F, (3,7) to (11,3) | none; a talking grunt at (5,7) | yes | |
| Basement | 1F's north-east room, panels to 1F's west room, stairs up | the 1F grunt (Qwilfish, Venomoth, 54) | yes, required | Sitrus Berry in the side pocket through the panel at (41,3) |
| Basement | 2F west, to the panel at (1,3) | Grunt 1 (Breloom, Exeggutor, 54) | yes, avoidable | |
| Basement detour | 3F west, a dead end off 2F's stairs at (12,3) | Grunts 1 (Marowak, Gengar, 54) and 2 (Kricketune, Gastrodon, 53) | no; both guard the way to the locked room | TM56 Hex, two, behind the key door at (27,19) |
| Basement | 2F's panel room, stairs down to 1F's Fredrick room | Scientist Fredrick (Gardevoir, Alakazam, 53) | yes, avoidable | Dubious Disc |
| Basement | B2F north, from the stairs at (50,3) | none; a talking grunt at (26,5) | yes | TM33 Reflect, two; the Galactic Key; the Secret Key, hidden |
| Out | B2F's key door to the main floor, the warehouse, Veilstone, the HQ's front door | none | yes | |
| Tower | the lobby, through the key door at (22,18) to the stairs at (19,14) | none; four talking members | yes | |
| Tower | 2F east, to the hall's panel at (29,13) | Grunts 2 (Fearow, Sharpedo, 54) and 3 (Houndoom, Victreebel, 54), an eye-contact pair; Scientist Darrius (Porygon-Z, 55) | yes; the pair required, Darrius avoidable | Max Revive and Green Shard in side pockets through panels |
| Tower | the hall: Looker, then Cyrus's speech, forced by the coord event at (20,12) | none; the crowd is removed after the speech | yes | |
| Tower | 2F north-east, the nap room, to the stairs at (50,3) | none | yes | the bed heals the party |
| Tower | 3F east, panels to the stairs at (10,11) | Grunts 3 (Ursaring, Granbull, 54) and 4 (Hypno, Grumpig, 54), an eye-contact pair | yes, required | Max Elixir and Protein in pockets through panels |
| Tower | 4F, through the key door at (8,14) | Cyrus 2 (six, 58 to 60), on the coord event at (8,11) | yes, a boss | |
| Tower | the laboratory, the control room | Saturn 2 (six, 55 to 57) | yes, a boss | Full Restore |

The doors decide the shape. B2F's door joins the main floor to its north end, where the key lies, so the key is first reached the long way round, down through Fredrick's room, and the door then lets the player straight out. The lobby's door is the only way into the tower, and the lobby is reached only from Veilstone. 3F's door opens a room off 3F's west side and nothing more: 3F's west and east sides share no tile. 4F's door stands between the stairs from 3F and Cyrus's office. 4F's warp panel at (8,3) leads to a sealed platform in the hall, not to the hall's floor.

After Cyrus 2 the player can still heal before Saturn 2: the Pocket PC works, the nap room is three warps back, and the lobby's front door is open.

## 2. The play order and its stretches

The order is fixed by the story, and nothing in the split can be reached ahead of its flag. The HQ waits on the warehouse's state, which waits on Looker, who waits on the storage-key grunt, who appears only after Lake Acuity. The tower waits on the Galactic Key. Earliest-access levelling therefore follows the walk: the Rock Climb finds and Lake Acuity, Veilstone, the basement run, the tower. The Rock Climb trainers can be fought at any point of the split, so they are levelled for its start.

The one choice is when the player fights the Rock Climb trainers, and it does not move any level: they are optional and met first at the split's start.

### The room in four levels

The band is not the constraint. Candice's split's last ordinary fight is at 55, and the cap is 60, so ordinary trainers have 55 to 59, with 59 rare: one level more than Candice's split had. The bosses sit at 60 and 57.

Experience is the constraint. The sums use Generation 4's formula (base experience times level over seven, half again for a trainer's Pokemon), shared by six.

| Fights | Experience | Running total |
|---|---:|---:|
| The HQ's mandatory five (seven trainers) | 26,926 | 26,926 |
| The HQ's optional five (2F's Grunt 1, Fredrick, Darrius, 3F west's two) | 18,445 | 45,371 |
| Route 216's four above the walls | 28,696 | 74,067 |
| Hiker Alexander and Dragon Tamer Patrick | 5,344 | 79,411 |
| Cyrus 2 | 15,083 | 94,494 |
| Saturn 2 | 14,200 | 108,694 |

| Climb, six Pokemon | Medium fast | Medium slow | Slow |
|---|---:|---:|---:|
| 56 to 57 | 57,462 | 59,382 | 71,826 |
| 56 to 58 | 116,976 | 121,050 | 146,220 |
| 56 to 60 | 242,304 | 251,406 | 302,880 |

So a party of six that fights everything before Cyrus 2 reaches about 57.4; one that takes only the mandatory fights, about 56.5. Wild Pokemon here are 36 to 41 and give about 1,100 a knockout. No maid trains a party past 56: the base ROM's maids follow its old caps (Snowpoint's to 56, Sunyshore's to 62), and HQ's and Galactic's splits, added by Oxide, have none.

The pass changes this. Every HQ trainer has one or two Pokemon, against the rule of three to six, and none holds an item or a nature. Rebuilt at four Pokemon each around 57, and with the six fights question 3 adds to the count (four of them new trainers), the mandatory path and the bosses give about 140,000 (a party of six near 58.3 at Saturn) and everything about 215,000 (near 59.6). That estimate is the case for question 1's answer: the experience gap closes inside the split, without moving any cap.

### What the push by two would move

| Cap | Today | Pushed |
|---|---:|---:|
| Candice | 56 | 58 |
| HQ | 60 | 62 |
| Galactic | 65 | 67 |
| Volkner | 68 | 70 |
| Barry | 71 | 73 |
| League | 78 | 80 |

It would move the engine's caps in `src/system_vars.c`, the tools' copies (`pool.caps`, `progression.DEFAULT_CAPS`, `fights.json`), every gym's cap message from Candice's on, and the Snowpoint, Sunyshore and League maids' thresholds. It would re-level what has landed: Candice's ace to 58 and her gym's six, the split's ordinary band from 52 to 55 up to as much as 57, and Route 216's four to 58 to 59. It moves the later bosses' aces: Cyrus 2 to 62, Saturn 2 to 59, Cyrus 3 to 67, Volkner to 70, Barry 6 to 73, and the Battle Zone's 52 route trainers from 55 to 64 up to 57 to 66. The honour caps already set are all earlier (Cyrus 1's 47 and Barry 5's 50 are the latest) and stay. The Elite Four's aces would run 74 to 80, past the League's 78, so either the League's cap moves to 80, or the push stops at Barry and the gap from Barry to the League shrinks from seven levels to five. The learnset rule that nothing is placed past 78 (the rewrite's check 22) is tied to the League's cap: with a League of 80 it may stay at 78, which leaves levels 79 and 80 empty, or move to 80, which reopens the 51 species' Kaizo moves listed as past the League. Every fight from Candice's on would be re-read against it, so the push is material for all of them.

It does not buy room where room is short. Candice's split would need 277,400 for six to climb 53 to 58, against the 269,500 its rebuilt teams offer with everything fought; HQ's would need 259,300 for 58 to 62.

### Where an honour cap would fit

The one natural break is the Galactic Key: the basement run ends there and the player leaves the building before the tower. A cap there could stand at 57 or 58. No player reaches it: the basement's mandatory fights give a party of six a fifth of a level today, and under one level after the pass. The tower's two bosses close the split together, Cyrus 2 at the cap and Saturn 2 under it. Lake Acuity's scene has no fight to close. So question 2 recommends none.

## 3. The mandatory count

Ian's rules apply: every mandatory fight that is not a boss counts, mini-bosses included; a pair fought together is one fight; a trainer who turns, spins or walks is optional. Nothing outside the HQ is on the way: the walk from Lake Acuity to Veilstone can be made by the Pocket PC's Teleport System, so no route is forced, and Acuity Lakefront's climb and Veilstone hold no trainer today.

| Fight | Map | Kind | Today | What would make it count | Stretch |
|---|---|---|---|---|---|
| Grunt 1 | B2F | ordinary | required | | 3 |
| Grunt 2 | B2F | ordinary | required | | 3 |
| the 1F grunt | 1F | ordinary | required | | 3 |
| Grunts 2 and 3, a pair | 2F east | ordinary | required | | 4 |
| Grunts 3 and 4, a pair | 3F east | ordinary | required | | 4 |
| the talking grunt, made a trainer | B1F | ordinary | not a trainer | a free slot at his own tile, (5,7), looking west with a sight of 2 | 3 |
| the talking grunt, made a trainer | B2F north | ordinary | not a trainer | a free slot at (26,5), looking south with a sight of 6 | 3 |
| Scientist Fredrick | 1F | ordinary | avoidable | no facing or sight up to 6 holds his own tile; moved to his room's necks, (22 to 24, 6 to 7) looking across, or (11,4) beside the stairs | 3 |
| Grunt 1 | 2F west | ordinary | avoidable | nothing holds his tile; moved beside the panel, (2,4) to (2,6) | 3 |
| Scientist Darrius | 2F east | ordinary | avoidable | nothing holds his tile; moved to the neck at (12 to 14, 14 to 15), clear of the pair's sight | 4 |
| the storage-key grunt, made a trainer | Veilstone | ordinary | talks | a battle in his script before he drops the key, in a free slot | 2 |
| a new trainer | Acuity Lakefront | ordinary | none there | a free slot at the climb's foot, (308 to 309, 230 to 232), looking across it | 1 |
| a lab scientist, made a trainer | the laboratory | ordinary | wanders | fixed at one of the lab's necks, such as (12,10) looking south | 4 |
| a guard | 1F lobby | ordinary | none there | a free slot in the key door's corridor, (19 to 22, 14 to 15) | 4 |
| a guard | 4F | ordinary | none there | a free slot in the door's corridor, (8 to 9, 12 to 15), before Cyrus | 4 |

3F west's two grunts never count, since their side of 3F is a dead end; they suit the Capsule (question 5).

That gives 5 today, 8 with the three moves, 12 with the four talking members, and 16 with every new trainer. The recommendation, question 3, comes to 11: today's 5; the B1F grunt; Fredrick and Darrius moved; the storage-key grunt; the climb's new trainer; one lab scientist. It keeps 2F's Grunt 1 and B2F north's grunt aside so that the basement section, which holds at most five trainers in its list, holds its five mandatory ones (B2F's two, B1F's, 1F's and Fredrick). It puts three fights outside every section, two of them before the HQ, so that the split's count does not all fall inside a lock. The storage-key grunt's fight needs a change to Veilstone's script, which is still the machine-shaped one `bulk_scripts.py` made from the base ROM.

### The gauntlets on the real walk

| # | Today's section | What the walk shows |
|---|---|---|
| 3 | B2F, from the warehouse | works: its two grunts are both required, and the warehouse is its way back |
| 4 | 1F, from B1F | one required trainer; Fredrick is in its list but is met later, from 2F, after the section has closed; the lobby's front doors are listed as ways back but cannot be reached from inside it |
| 5 | 2F, from 1F's west room | its only reachable trainer, Grunt 1, is avoidable; the other three stand in the tower, which is never reached while it is open, so it holds no mandatory fight |
| 6 | 3F, from 2F's west stairs | the trap: 3F west's only exit is its way back, refused once the key is held, and two of its four trainers are on the east side. Moved on Ian's word (2026-11-02) to 3F's east stairs, with grunts 3 and 4 only |

The tower lies outside every section today, and its nap-room bed heals the party halfway up it.

The recommended rebuild, question 4, draws two sections:

| Section | Maps | Way in | Way back, refused | Trainers listed | Closes |
|---|---|---|---|---|---|
| the basement run | B2F, B1F, 1F, 2F, 3F | B2F from the warehouse | the same warp, until the Galactic Key is held | B2F's Grunts 1 and 2, the B1F grunt, the 1F grunt, Fredrick | on arriving in the warehouse with the key, or all five beaten |
| the tower | 2F, the hall, 3F | 2F from the lobby's stairs | the same stairs | the 2F pair, Darrius, the 3F pair | on arrival at 4F, before Cyrus 2 |

The basement's refusal is the reverse of today's item test (refused while the key is missing, where section 6 refuses while it is held), so `src/gauntlet.c` needs one more field or flag. A player who comes back into the basement for 3F west's room, key in hand, is never shut in, since the warehouse warp then lets them go. The tower needs the nap room's bed to refuse while the section is open, as the Pocket PC does, or it heals the party between the two pairs. Each section then holds five listed trainers, with five mandatory fights in the basement and three in the tower.

## 4. The fights by kind

| Fight | Kind | Where | Today | Settled |
|---|---|---|---|---|
| Cyrus 2 | boss (Cyrus) | HQ 4F | Skarmory, Magnezone, Dusknoir, Houndoom, Suicune 58, Weavile 60 | no: the Kaizo comb's draft at Ian's boss levels; its natures differ, but Dusknoir and Suicune both hold Leftovers, against the rule of 2026-10-12. Theme: power, 18 different Pokemon over three fights with his canon picks spread among them. Dusknoir repeats in Cyrus 3 (question 10) |
| Saturn 2 | boss (commander) | the control room | Uxie 55, Lickilicky, Wobbuffet, Wailord, Rhyperior 56, Toxicroak 57 | partly: Ian removed its Trick Room and Choice Scarf in the team builder; the fight opens in a permanent Trick Room (`fights.json`). Wobbuffet and Wailord both hold Leftovers, and three members are Brave and two Relaxed. Theme: slow giants in the room; Uxie and Toxicroak do not fit it |
| the basement's and the tower's trainers | ordinary, fought inside gauntlet sections (mini-bosses as sections) | HQ | two Pokemon each (Darrius one), 53 to 55, no items or natures | no |
| Route 216's four above the walls | ordinary, optional | Route 216 | three or four each, 56 to 57, items and natures in order | yes: Candice's pass, levelled for 60 |
| Hiker Alexander, Dragon Tamer Patrick | ordinary, optional | Routes 208, 210 North | two at 45, one at 43 | no (question 7) |

No rival is fought: Barry appears at Lake Acuity without a battle. Jupiter takes Uxie at Lake Acuity and leaves without a battle. No Ace Trainer or named officer stands in the split. Charon in the control room only talks.

## 5. Differences no doc accounts for

1. The gauntlet doc, `src/gauntlet.c`'s comments and the in-game checklist all read the HQ as one climb from B2F to 3F, with 3F's locked door leading to 4F and the hall leading back into 2F's east side. The tiles say otherwise (section 1), which leaves section 6 a trap, sections 4 and 5 almost empty, and the tower outside every section. The story-route study's question 9 and its 4 to 8 rested on the same walk.
2. Hiker Alexander and Dragon Tamer Patrick are first met in HQ's split, but the OxiDex and the census tag them Byron's, at 45 and 43 with two and one Pokemon. Byron's pass noted that they stand behind Rock Climb; Candice's moved only Route 216's four.
3. Mt. Coronet 2F's Rock Climb rooms open with the Icicle Badge, so its table is first met in HQ's split, where the OxiDex counts it from the Galactic split.
4. No maid trains a party for HQ's or Galactic's cap. The base ROM's maids follow its old caps, so Snowpoint's stops at 56 and Sunyshore's at 62, under Volkner's 68.
5. `fights.json` gives Cyrus 2's ace as 58 and Saturn 2's as 58 (the Level Caps sheet); the tree has 60 and 57, which match Ian's rulings.
6. The 2F nap room's bed heals the party for free in the middle of the tower, which no doc mentions.
7. Every HQ trainer breaks the size rule (three to six) and the item and nature rule of 2026-10-12, and so do Cyrus 2 (two Leftovers) and Saturn 2 (two Leftovers, repeated natures).

No sequence break was found. Every step of the split waits on the flag the step before it sets, and the tower waits on the key.

## How this was read

The story order was read from the scripts in the tree: `scripts_lake_verity.s`, which sets Lake Acuity's state; `scripts_init_lake_acuity.s` and `scripts_lake_acuity.s` for the scene and the flag it clears; `scripts_acuity_lakefront.s` for the lake's warps; Veilstone's machine-shaped script, compared with vanilla's on `main`, for the storage-key grunt and Looker; the warehouse's script for the HQ's door; and the ten HQ scripts for the doors, the speech, the bed, Cyrus and Saturn. `scriptdis.py` was not needed, since every one of these is source in the tree. The HQ's floors were walked with `tools/oxide/mapreach.py`, its door tiles walled with `--wall` and then opened, and drawn tile by tile to place the doors. Every crossing was tested with `required.Field`'s sight lines and collision, on the split's field moves, with the standing Galactic members as objects and the doors shut until the key; each avoidable trainer and talking member was tried on its own tile in every facing with sights to six, and every tile of each crossing was tried for a new trainer with sights to four. `pairs.py` found the two eye-contact pairs. The world outside the HQ was walked with the story-route study's `worldreach.py`, comparing the end of Candice's split with the Icicle Badge, and the new reach traced back header by header. The trainers, their split tags and roles came from `res/trainers/data/`, `tools.oxide.encounters.trainers.split_map` and `trainer-roles.tsv`; the wild tables from `res/field/encounters/` and the OxiDex's split table in `progression.py`; each ball's item from its script number through `scripts_visible_items.s`; the gauntlet sections from `src/gauntlet.c`; and the experience from each species' base experience. The scratch scripts are in `/home/ian/.claude/jobs/382760ce/tmp/hq-map/`.

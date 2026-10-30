# Mandatory fights in Roark's and Gardenia's splits

Ian asked on 2026-10-29 for 8 non-boss mandatory fights in Roark's split and 12 or more in Gardenia's ("it is a long split as it is"). Both splits now reach their number. Twelve trainers moved onto the story path and none was added: each already looked one fixed way and could be walked around, so no spinner was made static. No team, class, script or text bank changed. The method and its checks are the ones of `docs/oxide/mandatory-fights.md`, which did the same for Fantina's and Maylene's splits.

## Summary

| Split | Non-boss mandatory, before | After | Bosses, counted apart |
|---|---:|---:|---|
| Roark (cap 16) | 3 | 8 | Lucas or Dawn 1, Barry 2, Roark |
| Gardenia (cap 26) | 7 | 12 | Somnu 1, Mars 1, Gardenia |

The count before agrees with the Overseer's. Two trainers that the tile model reads as required stay out of it, since each turns on the spot and so counts as optional by Ian's rule: Lass Sarah (Route 204 South) and Aroma Lady Taylor (Route 204 North). The Valley Windworks building's grunt is out for the same reason, and Hiker Daniel on Route 205 South too.

What Ian decides or does:

1. Play the new checks in `docs/oxide/ingame-checklist.md`, the items "Mandatory fights, Roark's split" and "Mandatory fights, Gardenia's split", one line per moved trainer. About 40 minutes from a new game, or less with the test kit's warps.
2. Say whether the Floaroma Meadow grunts are a pair under the six-Pokemon rule. The meadow's script fights them one after the other with no break, four Pokemon each, so the player meets eight in a row. Nothing here changed them.

Next steps: the Overseer lands the branch (a few minutes), then Ian's checks. Nothing waits on the scorer, since no boss moves.

## Each fight and how it is known

A route trainer is mandatory when `tools.oxide.balance.required` reads it "required" and it looks one fixed way: no walkable way from where the story brings the player in to where it sends them out avoids every tile it sees. Story battles were read off `docs/oxide/script-index.md` and the maps' scripts. Two trainers who fight together are one fight.

### Roark's split

| Fight | Map | How it is known |
|---|---|---|
| Youngster Tristan | Route 202 | required.py |
| Lass Natalie | Route 202 | required.py |
| Youngster Logan | Route 202 | required.py |
| Youngster Sebastian (new) | Route 203 | required.py, after the move |
| Lass Madeline (new) | Route 203 | required.py, after the move |
| Picnicker Diana (new) | Oreburgh Gate 1F | required.py, after the move |
| Camper Curtis (new) | Oreburgh Gate 1F | required.py, after the move |
| Worker Mason (new) | Oreburgh Mine B2F | required.py, after the move |

Not counted: Lass Kaitlin on Route 203 wanders. Youngsters Michael and Dallas on Route 203 and Worker Colin in the mine stay avoidable; the three needed spots were better spread over the other maps. The Oreburgh gym's two trainers are gym trainers. The Experiencia battle in Oreburgh is optional.

### Gardenia's split

| Fight | Map | How it is known |
|---|---|---|
| Galactic grunts, a tag battle beside Lucas or Dawn | Jubilife City | the script (`balance/pairs.py` lists it) |
| Lass Samantha (new) | Route 204 South | required.py, after the move |
| Twins Liv and Liz (new), one double | Route 204 North | required.py, after the move |
| Galactic grunt, first | Floaroma Meadow | the script, which starts both battles |
| Galactic grunt, second | Floaroma Meadow | the same script, straight after |
| Galactic grunt outside | Valley Windworks | the script at the door |
| Fisherman Joseph (new) | Route 205 South | required.py, after the move |
| Fisherman Andrew (new) | Route 205 South | required.py, after the move |
| Cheryl, when first met | Eterna Forest | the script; Ian confirmed it is forced |
| Bug Catcher Jack and Lass Briana, beside Cheryl | Eterna Forest | required.py; one eye-contact double |
| Psychics Elijah and Lindsey, beside Cheryl | Eterna Forest | required.py; one eye-contact double |
| Psychics Kody and Rachael (new), beside Cheryl | Eterna Forest | required.py, after the move; one eye-contact double |

Not counted: Bug Catchers Donald and Phillip in Eterna Forest carry the Eviolite and the Absorb Bulb, and Picnicker Karina, Camper Zackary and Fisherman Zachary carry TMs, so all stay optional. Route 205 South's other trainers turn or walk. Route 211 West and the Old Chateau are off the path. The Eterna gym's trainers are gym trainers.

## The trainers moved

Each keeps its team, class and script. Only position, facing and sight range changed.

| Trainer | From | To | Why it is safe |
|---|---|---|---|
| Youngster Sebastian, Route 203 (3 Pokemon, 14 to 15) | (234, 757), looking west, sight 5 | (234, 756), looking south, sight 3 | Past the bypass round Dallas, the path is four rows deep at x 234 (756 to 759), with a ledge above and a wall below. He stands on its top row and sees the other three. |
| Lass Madeline, Route 203 (3, 14) | (240, 748), looking south, sight 5 | (242, 754), looking east, sight 4 | The way north to Oreburgh Gate is a passage five tiles wide (x 242 to 246) at rows 754 and 755, since the grass to its west joins the passage only north of her row. She stands at its west edge and sees the other four. |
| Picnicker Diana, Oreburgh Gate 1F (4, 13 to 15) | (24, 21), looking south, sight 3 | (24, 20), looking south, sight 3 | The way east crosses column x 24. From where she stood a player could step round her through row 20; one step north closes that, and she sees rows 21 to 23. The tile below them is a dead end beside a breakable rock. |
| Camper Curtis, Oreburgh Gate 1F (4, 13 to 14) | (17, 25), looking north, sight 3 | (18, 25), looking north, sight 3 | The same at column x 18: from x 17 a player slipped under him through row 26, which at x 18 is a dead end. He sees rows 22 to 24, six tiles west of Diana's column. |
| Worker Mason, Oreburgh Mine B2F (5, 15) | (26, 20), looking west, sight 0 (talked to only) | (20, 16), looking west, sight 5 | The shaft from B1F comes down at x 15 to 19, and a Machop and a worker stand on row 15 east of it. Every way on crosses row 16 at x 15 to 19, which he sees from just below the Machop. The east corridor he left is not the only way to Roark: a western loop by the ledges goes round it. |
| Lass Samantha, Route 204 South (4, 17 to 18) | (171, 712), looking south, sight 5 | (170, 712), looking east, sight 3 | South of the Ravaged Path the way is four tiles wide (x 170 to 173) at rows 709 to 712. She stands at its west edge and sees the other three. |
| Twins Liv and Liz, Route 204 North (3, 16 to 17, one double) | (175, 679) and (176, 679), looking south, sights 3 and 4 | (170, 677) and (170, 676), looking east, sight 2 | The last stretch into Floaroma is three tiles wide (x 170 to 172) at rows 673 to 678. They stand side by side at its west edge; either one's row is a full crossing, so each alone makes the double required. |
| Psychics Kody and Rachael, Eterna Forest (3 each) | (74, 67) and (77, 67), facing each other across a side passage | (84, 52) and (87, 52), facing each other, sight 2 | The forest's south half joins its north half only through a corridor four tiles wide (x 84 to 87, rows 50 to 57). They stand at its two edges on row 52 and share their two sight tiles, as before, so they stay one double beside Cheryl. |
| Fisherman Joseph (3, 25) | Route 205 North's pier, (270, 532), looking south, sight 0 | Route 205 South, (219, 658), looking west, sight 3 | The bridge north from the Valley Windworks is the one way to Eterna Forest, three tiles wide (x 216 to 218) over the water. He stands on the bank beside its south end and sees its whole foot. |
| Fisherman Andrew (6, 20 to 24) | Route 205 North's pier, (274, 531), looking east, sight 0 | Route 205 South, (215, 653), looking east, sight 3 | He stands on the bank beside the bridge's north end and sees its whole top row. Before the Windworks the two grunts stand on that row and stop his sight, so he does not interrupt their scene. |

Route 205 North had no spot where a fisherman could stand by the water and guard the way: the grass north of its river is a second way to Eterna City. Its piers keep Fisherman Zachary, who carries TM88, and the fisherman who only talks.

## The checks

Every move was checked with the trainer as a solid object, in its split and a later one (Candice's for Roark's maps, Fantina's and Byron's for Gardenia's). From every warp and map edge, the player still reaches every tile reachable before, the trainer's own tile aside. The model was read twice, flat and with the bridge rule `mapreach.py` uses, and both agree on every moved trainer. No moved trainer stands on a warp, sign, item ball, hidden item, script trigger or another object. No scripted walk crosses a new tile: Roark leaves the mine along row 28, Cheryl leaves the forest at its far north end, and the Route 205 South grunts only turn on the spot.

Against `oxide`, `balance/pairs.py`'s eye-contact pairs gain and lose nothing. Kody and Rachael fight beside Cheryl, a partner double, and field six between them. No moved trainer carries a reward.

One tool changed. Route 205 South is crossed twice in Gardenia's split, to the Windworks and back to the forest, and required.py took each trainer's verdict from its first crossing only, which reads the two fishermen avoidable. A required verdict on a later crossing in the same split now wins, since the player must pass the trainer before the split ends. That also makes Hiker Daniel read required, though as a spinner he counts as optional. `test_b1e` is pinned at 64 required and 107 avoidable, and its check of Ian's walk-around reading of Route 203 now covers the three trainers that stayed.

## What is unverified

- Everything above comes from the tile model, not the game. The in-game checks are the proof.
- A twins double such as Liv and Liz fights only when the player has two Pokemon able to battle (the game's `FieldSystem_CheckForTrainersWantingBattle`). A player down to one healthy Pokemon walks past them, as past Twins Teri and Tia in Maylene's split. Ian's rules do not say whether that still counts as mandatory.
- Worker Mason now sees five tiles. The game supports up to seven, but the walk-up has not been watched.
- The fishermen stand on the riverbank with the height value of the ground objects there; that they are drawn on the ground and not at the old piers' height has not been seen.
- `docs/oxide/trainer-roles.tsv`, which `balance/rewards.py` writes, still lists the moved trainers as avoidable and the fishermen on Route 205 North, as it did for the Fantina and Maylene moves. Regenerating it also rewrites rows the team retunes in other worktrees are changing, so it is left for the Overseer to regenerate after they land.
- Gardenia's split is due its level climb (the soft caps of 2026-10-29). The fishermen's levels (Andrew 20 to 24, Joseph 25) now come before the forest's 23 to 24, which that pass should read.

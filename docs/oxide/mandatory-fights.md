# Mandatory fights in Fantina's and Maylene's splits

Ian asked on 2026-10-29 for about a dozen mandatory fights per split, 10 to 15, and the same day left gym trainers out of the count. This page counts Fantina's split (cap 33) and Maylene's split (cap 39) before and after, and lists the ten trainers moved onto the story path on branch `overseer-mandatory-fights`. No trainer was added, and no team, class or script changed.

## Summary

Both splits now have 12 non-boss mandatory fights by this count: Fantina's rose from 9 and Maylene's from 5. Bosses are counted apart and did not change: three in Fantina's split, two in Maylene's. Gym trainers are listed at the end for reference and are in neither number.

| Split | Non-boss mandatory, before | After | Bosses |
|---|---:|---:|---:|
| Fantina (cap 33) | 9 | 12 | 3 |
| Maylene (cap 39) | 5 | 12 | 2 |

What Ian decides or does:

1. Play the new checks in `docs/oxide/ingame-checklist.md` (the items "Mandatory fights, Fantina's split" and "Mandatory fights, Maylene's split"), one per moved trainer: walk the path, be seen, and find the way still open after the battle. About 40 minutes with the test kit's warps.
2. Say whether Ruin Maniac Calvin on Route 215 should move. He was not moved, because his win gives TM22 and rewards belong to optional fights. A closer reading of the raised walkway beside him (below) says the player probably cannot walk round him today, so his TM may already sit behind a mandatory fight.
3. Say whether a trainer who turns on the spot counts. Four of the "before" fights (Hikers Justin and Jonathan, Breeder Jennifer, Jogger Craig) turn or walk, so a patient player might slip past one while it faces away. They are counted here, as the tools count them.

Next steps: the Overseer lands the branch (a few minutes), then Ian's checks. Nothing waits on the scorer: no boss moves.

## How each fight is known to be mandatory

A route trainer is mandatory when `tools.oxide.balance.required` reads it "required": no walkable way from where the story brings the player in to where it sends them out avoids every tile the trainer sees. A beaten trainer still stands on its tile, so each moved trainer was also checked as a solid object. From every warp and map edge, the player can still reach every tile reachable before, apart from the trainer's own tile; this was checked in the split it is met in and in a later one. The check was run twice, once with the model's flat reading and once with the bridge rule `mapreach.py` uses (a bridge deck is entered only at its ends). Both readings agree on every moved trainer.

Gauntlet members count because Ian's brief counts them; `tools/oxide/balance/gauntlet.py` names the sections. A gauntlet locks only the way back, so the model reads the six Eterna building members as passable. Story battles were read off `docs/oxide/script-index.md` for every map of the two splits.

### Fantina's split

| Fight | Map | How it is known |
|---|---|---|
| Galactic Grunt (1F, first) | Galactic Eterna building 1F | Gauntlet, section "1F and 2F" |
| Galactic Grunt (1F, second) | Galactic Eterna building 1F | Gauntlet, section "1F and 2F" |
| Galactic Grunt (2F, first) | Galactic Eterna building 2F | Gauntlet, section "1F and 2F" |
| Galactic Grunt (2F, second) | Galactic Eterna building 2F | Gauntlet, section "1F and 2F" |
| Galactic Grunt (3F) | Galactic Eterna building 3F | Gauntlet, section "3F" |
| Scientist Travon | Galactic Eterna building 3F | Gauntlet, section "3F" |
| Hiker Justin | Route 207 | required.py (turns between north and east) |
| Hiker Robert | Route 208 | required.py |
| Hiker Jonathan | Route 208 | required.py (turns between south and west) |
| Hiker Kevin (new) | Route 207 | required.py, after the move |
| Battle Girl Helen (new) | Route 207 | required.py, after the move |
| Aroma Lady Hannah (new) | Route 208 | required.py, after the move |

Bosses: Jupiter (the building's 4F), Lucas or Dawn (the scene at Route 207's Mt. Coronet entrance, which every player walks into) and Fantina. Not counted: Wayward Cave and the Cycling Road are off the story path, and their trainers can be ridden or walked around. The Experiencia maid in Eterna City is an optional training battle.

### Maylene's split

| Fight | Map | How it is known |
|---|---|---|
| Breeder Jennifer | Route 209 | required.py (turns three ways) |
| Twins Emma and Lil | Route 209 | required.py |
| Ace Trainer Dennis | Route 215 | required.py |
| Ace Trainer Maya | Route 215 | required.py |
| Jogger Craig | Route 215 | required.py (walks a loop) |
| Breeder Albert (new) | Route 209 | required.py, after the move |
| Cowgirl Shelley (new) | Route 209 | required.py, after the move |
| Poke Kid Danielle (new) | Route 209 | required.py, after the move |
| Rancher Marco (new) | Route 210 South | required.py, after the move |
| Belle and Pa Ava and Matt (new) | Route 210 South | required.py, after the move |
| Black Belt Gregory (new) | Route 215 | required.py, after the move |
| Black Belt Nathaniel (new) | Route 215 | required.py, after the move |

Bosses: Barry (the gate from Hearthome onto Route 209) and Maylene. Not counted: the two Veilstone grunts of the tag battle beside Lucas or Dawn. The tools place them in Maylene's split by their map, but the gym script starts that scene only after Maylene's badge, so the player meets them in Wake's split. The Lost Tower, the Solaceon Ruins, the Route 210 cafe and the Game Corner are optional.

### Gym trainers, for reference only

Hearthome's gym: Lass Molly, Youngster Donny, School Kids Chance and Mackenzie, Ace Trainers Allen and Catherine. Veilstone's gym: Black Belts Colby, Darren, Jeffery and Rafael. Their gyms have moving parts the model does not read, and which of them the player must beat was not checked.

## The trainers moved

Each keeps its team, class and script. A trainer that walked, spun or turned now looks one way. Moving any of them meant changing that, because in its new place the old movement would let a player time a pass while it faces away, or would walk it out of place.

| Trainer | From | To | Why it is safe |
|---|---|---|---|
| Hiker Kevin, Route 207 | (319, 721), turning north and east, sight 2 | (307, 705), looking west, sight 5 | The way in from Route 206 is six tiles wide, x 302 to 307. He stands at its east edge and sees the other five, which stay open. His height value is now 0, as for the objects round him. |
| Battle Girl Helen, Route 207 | (336, 722), walking back and forth, sight 2 | (335, 716), looking north, sight 5 | Both ways to Mt. Coronet cross column x 335 between rows 711 and 715. She stands at its foot, in a passage six tiles wide. Rows 712 to 714 east of x 331 are kept clear for Lucas or Dawn's walk in the entrance scene. Height value 0, as for Justin beside her. |
| Aroma Lady Hannah, Route 208 | (433, 720), spinning, sight 2 | (431, 719), looking west, sight 5 | The mountain path opens into the flower field through a gap two tiles wide (x 426 and 427). She stands in the grass four tiles east of the opening and sees both its tiles as the player steps out. |
| Breeder Albert, Route 209 | (522, 725), turning north and south, sight 3 | (527, 725), looking north, sight 3 | The way east from Hearthome narrows to three rows (722 to 724) between the ledges and the pond. The ledge jump through the grass, which used to skip him, lands in the same rows. He stands just south of them, and the way past him to the fishing pier stays open. |
| Cowgirl Shelley, Route 209 | (560, 690), looking east, sight 2 | (557, 690), looking east, sight 5 | The walk north (x 557 and 558) and the bike slope (x 562) both come out on row 690. She stands at its west end and sees the five tiles east of her; the slope's top is left clear. |
| Poke Kid Danielle, Route 209 | (552, 722), looking east, sight 0 (she fought only when spoken to) | (549, 721), looking west, sight 3 | The path north to the bridge climbs a strip four tiles wide (x 546 to 549). She stands at its east edge and sees the other three. |
| Rancher Marco, Route 210 South | (555, 627), looking east, sight 3 | (557, 636), looking east, sight 6 | The way in from Solaceon is a corridor seven tiles wide (x 557 to 563). He stands at its west edge and sees the other six. |
| Belle and Pa Ava and Matt, Route 210 South | (563, 616) and (563, 615), looking west, sight 1 | (563, 619) and (563, 620), looking west, sight 6 | Both ways north (the bike slope at x 557 and the grass column at x 561 to 562) leave the meadow over row 619. Ava, first of the pair in the file, sees all of row 619, so the tool reads the pair required. Matt stands beside her and sees row 620; the two tiles east of them are a dead end. |
| Black Belt Gregory, Route 215 | (621, 578), looking west, sight 3 | (623, 583), looking east, sight 4 | The path climbs out of the grass at x 624 and turns east along row 583. He stands at the corner, at the foot of the ledges, and sees the four tiles of the turn. |
| Black Belt Nathaniel, Route 215 | (643, 582), looking west, sight 2 | (650, 582), looking south, sight 5 | Before the ledges down towards Veilstone, the path crosses column x 650 between rows 583 and 587. He stands at its top and sees down it. |

No moved trainer stands on a warp, sign, item ball, hidden item, script trigger or another object. None stands on or under a bridge, and none sees across a bridge, ledge, slope or water tile. The only scripts that move people on these maps (Lucas or Dawn on Route 207, Cynthia and the Psyduck on Route 210 South) walk elsewhere.

Not moved, and why: Black Belt Kyle (Route 208) gives the Rocky Helmet and Calvin gives TM22, and both rewards belong to optional fights (the standing rulings). The joggers each share their tile with a second, non-battling copy. The Young Couple and the Cycling Road riders carry rewards or could not be made mandatory safely.

## What is unverified

- Everything above comes from the tile model, not from the game. The in-game checks are the proof.
- Five trainers now see 5 tiles and two (Marco, the Belle and Pa) see 6. Vanilla trainers see up to 7, so the game supports it, but the walk-up has not been watched.
- The Belle and Pa now stand in the other order, Ava north of Matt. Which one walks up first after the spot was not checked.
- Calvin. The flat model, which required.py uses, reads him avoidable, because it lets the player step off Route 215's raised walkway sideways. With the bridge rule he is required where he stands. The game decides which reading is right.
- The model reads only the tiles. It does not know the bike's speed on the Route 209 slope, or a cut tree the player leaves standing. Neither can open a way round a moved trainer, though: an uncut tree only removes paths.

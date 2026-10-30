# Mandatory fights in Fantina's and Maylene's splits

Ian asked on 2026-10-29 for about a dozen mandatory fights per split, 10 to 15, and the same day left gym trainers out of the count. This page counts Fantina's split (cap 33) and Maylene's split (cap 39) before and after, by the rules Ian gave that day (below), and lists the twelve trainers moved onto the story path. No trainer was added, and no team, class or script changed for this.

## Summary

Fantina's split now has 10 non-boss mandatory fights, up from 7, and Maylene's has 11, up from 2. Bosses are counted apart and did not change: three in Fantina's split, two in Maylene's. Trainers who turn, spin or walk are optional by Ian's rule and are listed apart. Gym trainers are listed for reference and are in no number.

| Split | Non-boss mandatory, before | After | Bosses | Optional spinners on the path |
|---|---:|---:|---:|---:|
| Fantina (cap 33) | 7 | 10 | 3 | 2 |
| Maylene (cap 39) | 2 | 11 | 2 | 2 |

What Ian decides or does:

1. Play the new checks in `docs/oxide/ingame-checklist.md` (the items "Mandatory fights, Fantina's split" and "Mandatory fights, Maylene's split"), one per moved trainer: walk the path, be seen, and find the way still open after the battle. About 45 minutes with the test kit's warps.
2. Nothing else waits on him. Fantina's split stays at 10: no other trainer there has a safe, plausible spot that is not already guarded, and the rest carry rewards.

Next steps: the Overseer lands the branch (a few minutes), then Ian's checks. Nothing waits on the scorer: no boss moves.

## Ian's rules for the count (2026-10-29)

- Gym trainers and bosses are not counted.
- A trainer who turns, spins or walks is optional, not a mandatory fight, though such a trainer may be harder than normal. Hikers Justin and Jonathan, Breeder Jennifer and Jogger Craig stay spinners and are not changed.
- Two trainers who fight the player together are one fight, a tag fight: an eye-contact double (Ace Trainers Dennis and Maya) or a pair with one double-battle team (twins, couples).
- Two trainers the player fights alone together, by eye contact or by script, field six Pokemon between them at most, unless Ian allows more ("8v6 ... should not be allowed").
- Ruin Maniac Calvin stays where he is.

## How each fight is known to be mandatory

A route trainer is mandatory when `tools.oxide.balance.required` reads it "required" and it looks one fixed way: no walkable way from where the story brings the player in to where it sends them out avoids every tile the trainer sees. A beaten trainer still stands on its tile, so each moved trainer was also checked as a solid object. From every warp and map edge, the player can still reach every tile reachable before, apart from the trainer's own tile; this was checked in the split it is met in and in a later one. The check was run twice, once with the model's flat reading and once with the bridge rule `mapreach.py` uses (a bridge deck is entered only at its ends). Both readings agree on every moved trainer.

Gauntlet members count because Ian's brief counts them; `tools/oxide/balance/gauntlet.py` names the sections. A gauntlet locks only the way back, so the model reads the six Eterna building members as passable. Story battles were read off `docs/oxide/script-index.md` for every map of the two splits.

Every moved trainer was checked against `tools.oxide.balance.pairs`, comparing the branch's eye-contact pairs with those on `oxide`. The branch adds none and removes none. The first spot chosen for Battle Girl Helen (looking north from (335, 716)) shared a sight tile with Hiker Justin, which made an eye-contact pair of eight Pokemon; she now stands at the top of the same column looking south, and shares no tile with anyone.

### Fantina's split

| Fight | Map | How it is known |
|---|---|---|
| Galactic Grunt (1F, first) | Galactic Eterna building 1F | Gauntlet, section "1F and 2F" |
| Galactic Grunt (1F, second) | Galactic Eterna building 1F | Gauntlet, section "1F and 2F" |
| Galactic Grunt (2F, first) | Galactic Eterna building 2F | Gauntlet, section "1F and 2F" |
| Galactic Grunt (2F, second) | Galactic Eterna building 2F | Gauntlet, section "1F and 2F" |
| Galactic Grunt (3F) | Galactic Eterna building 3F | Gauntlet, section "3F" |
| Scientist Travon | Galactic Eterna building 3F | Gauntlet, section "3F" |
| Hiker Robert | Route 208 | required.py, looks south |
| Hiker Kevin (new) | Route 207 | required.py, after the move |
| Battle Girl Helen (new) | Route 207 | required.py, after the move |
| Aroma Lady Hannah (new) | Route 208 | required.py, after the move |

Optional spinners on the path: Hiker Justin (Route 207, turns north and east) and Hiker Jonathan (Route 208, turns south and west). Bosses: Jupiter (the building's 4F), Lucas or Dawn (the scene at Route 207's Mt. Coronet entrance, which every player walks into) and Fantina. Not counted: Wayward Cave and the Cycling Road are off the story path, and their trainers can be ridden or walked around. The Experiencia maid in Eterna City is an optional training battle.

### Maylene's split

| Fight | Map | How it is known |
|---|---|---|
| Twins Emma and Lil | Route 209 | required.py |
| Ace Trainers Dennis and Maya | Route 215 | required.py; one eye-contact double |
| Breeder Albert (new) | Route 209 | required.py, after the move |
| Cowgirl Shelley (new) | Route 209 | required.py, after the move |
| Poke Kid Danielle (new) | Route 209 | required.py, after the move |
| Rancher Marco (new) | Route 210 South | required.py, after the move |
| Belle and Pa Ava and Matt (new) | Route 210 South | required.py, after the move |
| Twins Teri and Tia (new) | Route 210 South | required.py, after the move |
| Black Belt Gregory (new) | Route 215 | required.py, after the move |
| Black Belt Nathaniel (new) | Route 215 | required.py, after the move |
| Black Belt Derek (new) | Route 215 | required.py, after the move |

Optional spinners on the path: Breeder Jennifer (Route 209, turns three ways) and Jogger Craig (Route 215, walks a loop). Bosses: Barry (the gate from Hearthome onto Route 209) and Maylene. Not counted: the two Veilstone grunts of the tag battle beside Lucas or Dawn. The tools place them in Maylene's split by their map, but the gym script starts that scene only after Maylene's badge, so the player meets them in Wake's split. The Lost Tower, the Solaceon Ruins, the Route 210 cafe and the Game Corner are optional.

### Gym trainers, for reference only

Hearthome's gym: Lass Molly, Youngster Donny, School Kids Chance and Mackenzie, Ace Trainers Allen and Catherine. Veilstone's gym: Black Belts Colby, Darren, Jeffery and Rafael. Their gyms have moving parts the model does not read, and which of them the player must beat was not checked.

## The trainers moved

Each keeps its team, class and script, and now looks one fixed way. A trainer that walked, spun or turned was changed to one fixed look, because in its new place the old movement would let a player time a pass, or would walk it out of place.

| Trainer | From | To | Why it is safe |
|---|---|---|---|
| Hiker Kevin, Route 207 | (319, 721), turning north and east, sight 2 | (307, 705), looking west, sight 5 | The way in from Route 206 is six tiles wide, x 302 to 307. He stands at its east edge and sees the other five, which stay open. His height value is now 0, as for the objects round him. |
| Battle Girl Helen, Route 207 | (336, 722), walking back and forth, sight 2 | (335, 711), looking south, sight 3 | Both ways to Mt. Coronet cross column x 335 between rows 711 and 715, and the row-715 end leads nowhere east. She stands at the top of the column, off the rows 712 to 714 where Lucas or Dawn walks in the entrance scene. Height value 0, as for Justin and the scientist near her. |
| Aroma Lady Hannah, Route 208 | (433, 720), spinning, sight 2 | (431, 719), looking west, sight 5 | The mountain path opens into the flower field through a gap two tiles wide (x 426 and 427). She stands in the grass four tiles east of the opening and sees both its tiles as the player steps out. |
| Breeder Albert, Route 209 | (522, 725), turning north and south, sight 3 | (527, 725), looking north, sight 3 | The way east from Hearthome narrows to three rows (722 to 724) between the ledges and the pond. The ledge jump through the grass, which used to skip him, lands in the same rows. He stands just south of them, and the way past him to the fishing pier stays open. |
| Cowgirl Shelley, Route 209 | (560, 690), looking east, sight 2 | (557, 690), looking east, sight 5 | The walk north (x 557 and 558) and the bike slope (x 562) both come out on row 690. She stands at its west end and sees the five tiles east of her; the slope's top is left clear. |
| Poke Kid Danielle, Route 209 | (552, 722), looking east, sight 0 (she fought only when spoken to) | (549, 721), looking west, sight 3 | The path north to the bridge climbs a strip four tiles wide (x 546 to 549). She stands at its east edge and sees the other three. |
| Rancher Marco, Route 210 South | (555, 627), looking east, sight 3 | (557, 636), looking east, sight 6 | The way in from Solaceon is a corridor seven tiles wide (x 557 to 563). He stands at its west edge and sees the other six. |
| Twins Teri and Tia, Route 210 South | (557, 609) and (558, 609), looking south, sight 3 | (557, 633) and (557, 634), looking east, sight 6 | Two rows north of Marco, at the same west edge of the corridor: Tia sees across row 634, the corridor's last row, and Teri the row above it. Tia comes first in the file, so the tool reads the pair required. |
| Belle and Pa Ava and Matt, Route 210 South | (563, 616) and (563, 615), looking west, sight 1 | (563, 619) and (563, 620), looking west, sight 6 | Both ways north (the bike slope at x 557 and the grass column at x 561 to 562) leave the meadow over row 619. Ava, first of the pair in the file, sees all of row 619, so the tool reads the pair required. Matt stands beside her and sees row 620; the two tiles east of them are a dead end. |
| Black Belt Gregory, Route 215 | (621, 578), looking west, sight 3 | (623, 583), looking east, sight 4 | The path climbs out of the grass at x 624 and turns east along row 583. He stands at the corner, at the foot of the ledges, and sees the four tiles of the turn. |
| Black Belt Nathaniel, Route 215 | (643, 582), looking west, sight 2 | (650, 582), looking south, sight 5 | Before the ledges down towards Veilstone, the path crosses column x 650 between rows 583 and 587. He stands at its top and sees down it. |
| Black Belt Derek, Route 215 | (607, 584), turning west and east, sight 3 | (606, 594), looking west, sight 2 | East of the raised walkway the path turns south down a column three tiles wide (x 604 to 606). He stands at its east edge on the top row and sees the other two. Jogger Craig's loop stays west of x 604. |

No moved trainer stands on a warp, sign, item ball, hidden item, script trigger or another object. None stands on or under a bridge, and none sees across a bridge, ledge, slope or water tile. The only scripts that move people on these maps (Lucas or Dawn on Route 207, Cynthia and the Psyduck on Route 210 South) walk elsewhere.

Not moved, and why: Black Belt Kyle (Rocky Helmet), Ruin Maniac Calvin (TM22), Breeder Kahlil (Safety Goggles) and the Young Couple Ty and Sue (Assault Vest) give rewards, which belong to optional fights (the standing rulings), and Ian keeps Calvin where he is. The joggers each share their tile with a second, non-battling copy. Breeder Amber's and Youngster Austin's only safe spots repeat a line another moved trainer already guards. The Cycling Road riders cannot be placed safely by this model, which reads the raised road flat. Dennis and Maya, and Camper Anthony and Picnicker Lauren, are existing eye-contact pairs and were left alone.

## What is unverified

- Everything above comes from the tile model, not from the game. The in-game checks are the proof.
- Four trainers now see 5 tiles, and Marco and the two pairs on Route 210 South see 6. Vanilla trainers see up to 7, so the game supports it, but the walk-up has not been watched.
- Route 210 South's way in from Solaceon now holds Marco and Teri and Tia within four rows. Whether that reads as two fights in a row or as a crowd is for Ian to judge in game.
- The Belle and Pa now stand in the other order, Ava north of Matt. Which one walks up first after the spot was not checked.
- Calvin. The flat model, which required.py uses, reads him avoidable, because it lets the player step off Route 215's raised walkway sideways. With the bridge rule he is required where he stands. He is not counted.
- The model reads only the tiles. It does not know the bike's speed on the Route 209 slope, or a cut tree the player leaves standing. Neither can open a way round a moved trainer, though: an uncut tree only removes paths.

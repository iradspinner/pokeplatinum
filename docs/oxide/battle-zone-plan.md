# The Battle Zone before the Elite Four

Scoping note, 2026-09-25, from the encounter track at Ian's request. Ian wants
the Battle Zone (the Fight Area, Routes 225 to 230, the Survival Area, the
Resort Area and Stark Mountain) open before the League, as Platinum Kaizo has
it, for the fights and the captures it adds. Nothing here is built yet. The
one decision that shapes all the rest is which split it opens in, and that is
Ian's.

## What gates it today

The only way in is the ferry from Snowpoint City. Its sailor checks two
things: the National Dex, which this game grants at the start (the Sandgem lab
turns it on with the Pokédex, a base ROM change), and `FLAG_GAME_COMPLETED`,
which only the Hall of Fame sets. That flag is checked twice in
`scripts_snowpoint_city.s`, in the sailor's two script entries. Past the ferry nothing else asks whether the game is complete,
except Stark Mountain's last room (`scripts_stark_mountain_room_3.s`, the
Heatran event, which also wants the National Dex and Buck met at the
Battleground). The Fight Area's arrival script checks only the National Dex,
which already passes. The Battleground's rematches are gated by story flags
(Galactic gone from Lake Valor, Heatran battled), not by the Hall of Fame.

## Field moves

Read from the maps' own terrain (the tile behaviours in each land data file),
not from memory:

| Field move | Needed on | Badge that unlocks it |
|---|---|---|
| Rock Climb | Routes 225, 226, 227, Stark Mountain's outside | Candice's Icicle Badge |
| Surf | Routes 226, 229, 230, the Resort Area | Wake's Fen Badge |
| Waterfall | nowhere in the zone | (Volkner's Beacon Badge) |

So the whole zone is walkable the moment Candice is beaten, which is also when
Snowpoint, and its ferry, is reached. Nothing waits on Waterfall. Stark
Mountain's inside rooms were not read; Strength and Rock Smash, both earlier
badges, are the likely needs there.

## What is in it

| | Count | Levels now |
|---|---|---|
| Route trainers (Routes 225 to 230, Stark Mountain) | 52 | 73 to 78, a few on Route 228 from 55 |
| Scripted fights: Volkner and Flint's tag battle at the Fight Area, Buck on Route 227, Mars and Jupiter at Stark Mountain | 5 trainers | 74 to 78 |
| Battleground rematches (Buck, Cheryl, Riley, Marley, Mira, the Frontier Brains, the rival) | about 20 | 59 to 90 |
| Wild tables (Routes 225 to 230, the Resort Area, Stark Mountain's three) | 10 tables, 8 capture areas | land 47 to 55, water 22 to 60 |

Route 224 stays post-game: it is reached from the League. The Battle Frontier
works at fixed levels, so its placement costs nothing.

The dialogue that assumes the League is done is small: the Fight Area's
arrival scene (Volkner's "Show me the skills that got you through the Pokémon
League!" and Buck's lines about the Elite Four), and the Snowpoint sailor's
"A great Trainer recognized by the Pokémon League". The Villa's lines about
the League are post-game content and can stay.

## The placement decision

The trainers and the wild tables were levelled for different moments. The
trainers sit at the League split's cap (78). The wild tables sit at Candice's
(56). Whichever split the zone opens in, one of the two has to move.

| | Open at Candice's split | Open after Volkner (League split) |
|---|---|---|
| Ferry gate | Icicle Badge | Beacon Badge |
| Trainers | 52 route trainers and 5 scripted fights re-levelled from about 75 to about 56 (balance track); the Battleground too | Fit as they are |
| Wild tables | Fit as they are | Raised about 20 levels, then `cli evolve` (encounter track, cheap) |
| Story | Volkner fights you at the Fight Area before you reach his Gym: move the tag battle behind his badge, or reword | Consistent; one line of Volkner's to reword |
| Captures before the League | +8, in Candice's split | +8, in the League split |
| Matches | Ian's own sheet, which puts the zone in Candice's split | Kaizo's "before the Elite Four", as Ian describes it |

The encounter track's reading: opening after Volkner is the cheaper and the
more consistent of the two, and it makes the League split, now thin (Victory
Road, Route 223, Sendoff Spring), the richest one. Opening at Candice's split
is the bigger change and makes the zone mid-game content, which is what Ian's
sheet had in mind. Either works with the tools as they are.

## The work, by track

Main track (scripts and text):

1. Replace the ferry's two `FLAG_GAME_COMPLETED` checks with the chosen badge.
2. Decide Stark Mountain's Heatran event: keep it post-game, or drop its check.
3. Reword the Fight Area arrival lines and the sailor's line, and, at
   Candice's split, gate the Volkner and Flint tag battle behind the Beacon
   Badge.
4. Level caps: the zone joins a split, so its cap applies there
   (the script-driven cap mechanism is Phase 4 element 8).

Balance track: the trainers, if Candice's split; a check that the Battleground
rematches still read as optional post-split fights either way.

Encounter track (this one):

1. Move the eight capture areas from "Post" to the chosen split in the sidecar.
2. At the League split, raise the ten tables' levels and run `cli evolve`; at
   Candice's split, leave them.
3. Recast the tables to the design rules, since they are still the base ROM's
   (they were out of scope as post-game); this is the part that takes time.
4. Recount captures before the League (73 planned, 81 with the zone).

## Open questions for Ian

1. Candice's split or the League split?
2. The Heatran event: in the zone's split, or kept post-game?
3. The Battleground rematches at 80 to 90: leave them as the zone's
   post-split challenge, or level them with the rest?

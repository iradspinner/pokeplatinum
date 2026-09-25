# The Battle Zone before the Elite Four

Scoping note, 2026-09-25, from the encounter track at Ian's request. Ian wants
the Battle Zone (the Fight Area, Routes 225 to 230, the Survival Area, the
Resort Area and Stark Mountain) open before the League, as Platinum Kaizo has
it, for the fights and the captures it adds. Ian ruled on the three open
questions the same day (below); the encounter track's first step is done,
and the rest waits on the main and balance tracks.

## Ian's rulings (2026-09-25)

1. **A new split, Galactic, straight after Lake Acuity.** It holds the whole
   Battle Zone and the Galactic fights up to the Distortion World (the Veilstone
   HQ, the Mt. Coronet climb, Spear Pillar), which spreads those fights out. Its
   cap is **64**; Candice's stays **56** and Volkner's rises from 62 to **68**.
   The League stays 78.
2. **Heatran becomes a random legendary encounter**, as Uxie and Azelf are:
   Stark Mountain's last room joins the legendary pool's statics.
3. **The Battleground rematches are skipped for now**, to come back to.

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

Kept for the record. Ian took neither option as it stands: the zone opens in a
new Galactic split straight after Lake Acuity, cap 64, with Volkner's raised to
68 (Ian's rulings, above). At 64 the trainers still come down, by about 11
levels rather than 20.

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

1. The ferry opens when the Lake Acuity event is done instead of after the Hall
   of Fame: its two `FLAG_GAME_COMPLETED` checks in `scripts_snowpoint_city.s`
   become that check. `VAR_LAKE_ACUITY_STATE` reaching 2, which
   `scripts_lake_acuity.s` sets as Jupiter's scene ends, looks like the marker;
   confirm it. Rock Climb needs the Icicle Badge, which comes before that.
2. Stark Mountain's last room: drop its Hall of Fame and National Dex checks and
   make its Heatran a draw from the legendary pool, with the lake caverns
   (the pool's scripting is already in the tracker's backlog).
3. Reword the Fight Area's arrival lines and the sailor's line, and gate the
   Volkner and Flint tag battle behind the Beacon Badge, since Volkner is now
   met at the Fight Area before his Gym.
4. The script-driven level caps (Phase 4 element 8) take the new split and the
   new caps.

Balance track:

1. The caps: Galactic 64 and Volkner 68, in the level cap design.
2. The zone's 52 route trainers and its scripted fights (Buck, Mars and Jupiter
   at Stark Mountain) from about 75 down to the Galactic cap, and the Galactic
   fights up to Spear Pillar re-read against 64 rather than 62.
3. Volkner and the split after him re-read against 68.
4. The Battleground rematches: skipped for now (ruling 3).

Encounter track (this one):

1. **Done 2026-09-25.** The sidecar's split table gains Galactic (cap 64) and
   Volkner's cap is 68. The ten Battle Zone tables move from Post to Galactic,
   and so do the eleven Mt. Coronet tables of the climb to Spear Pillar; Route 222
   and Sunyshore stay Volkner's. In progression order the Battle Zone now follows
   Snowpoint City, where its ferry leaves. Route 224 stays post-game.
2. **Reviewed 2026-09-26.** The ten tables are not the base ROM's, as this note
   first said: authoring Step 4 cast them on 2026-09-21 as post-game content. In
   the Galactic split they pass every lint rule, R12 included, and the
   availability gate, with no cap candidates, so nothing has to change. Their
   levels (land 47 to 55) are vanilla's and stay, as the authoring rules keep
   the level curve; they sit above the Mt. Coronet climb (36 to 39) the way
   vanilla's Battle Zone sits above it. Two things they now offer before Volkner
   are Ian's call: Metagross at 10% on Route 228, and the fully evolved starters
   as 1% tails (Blaziken, Incineroar, Charizard, Serperior and Meowscarada on
   land; Greninja, Primarina, Blastoise and Swampert on the Super Rod).
3. The capture count before the League: 73 planned, 81 with the zone's eight
   capture areas, once the ferry opens.
